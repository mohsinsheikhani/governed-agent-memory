"""LLM extraction: one message in, zero or more candidate facts out.

The extractor reads a SINGLE message in isolation. It cannot know what is already in
memory, so it only judges `firm` vs `hedge` from the wording. The Phase 1 resolution step
is what later downgrades a fact to `under_review` or flags a `claimed_unverified` buyer
claim by comparing against history.

Deterministic fields (source, valid_from, provenance) are NOT the LLM's job. The caller
sets them. The LLM only decides attribute, value, status, confidence, reason.

Uses OpenAI structured outputs (strict schema), so the attribute set and the firm/hedge
enum are enforced by the API, not hand-validated here.
"""

from __future__ import annotations

import os
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel

from src.memory.schema import ATTRIBUTES

MODEL = "gpt-4o"

# The schema enum is the API contract. Keep it in lockstep with schema.ATTRIBUTES.
Attribute = Literal[
    "intent",
    "champion",
    "economic_buyer",
    "authority",
    "budget_status",
    "budget_amount",
    "timeline",
    "competitor",
    "stage",
    "price_sensitivity",
    "tier_scope",
    "discount_terms",
]
assert set(Attribute.__args__) == ATTRIBUTES, "extract.Attribute drifted from schema.ATTRIBUTES"


class Fact(BaseModel):
    attribute: Attribute
    value: str                      # short phrase, not a sentence
    status: Literal["firm", "hedge"]
    confidence: float               # 0.8-0.95 firm, 0.3-0.5 hedge
    reason: str | None              # why it changed, only if the message says; else null


class Extraction(BaseModel):
    facts: list[Fact]


_client: OpenAI | None = None


def _client_() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return _client


_ATTR_HELP = """\
- intent: how serious the buyer is. e.g. serious, high, lukewarm, uncertain, low
- champion: the person inside the buyer advocating for the deal (a name)
- economic_buyer: the person who owns the budget / final yes (a name)
- authority: whether a named person can actually sign. e.g. "Wesley can sign", "needs owner Sal", "requires procurement"
- budget_status: state of the money. e.g. approved, frozen, pending, under board review
- budget_amount: the figure. e.g. "54k/yr"
- timeline: target go-live or decision date. e.g. "live this quarter", "Q1 next year"
- competitor: who else they are considering. e.g. none, "Benchpoint", "Talon"
- stage: where the deal is. e.g. discovery, proposal, pilot, closed won, stalled
- price_sensitivity: how price-driven they are. e.g. high, "cost-focused COO"
- tier_scope: chosen tier or what is in/out of scope. e.g. "Standard tier", "add-ons are paid extra"
- discount_terms: any discount, term length, payment terms, price lock. e.g. "40% off", "3-year auto-renew", "net-90\""""

SYSTEM = f"""You read one message from a B2B sales deal and extract durable facts about \
the deal.

Map each fact to exactly one of these attributes:
{_ATTR_HELP}

Rules:
- Extract a fact only if THIS message actually states or changes it. Do not infer beyond \
the text, and do not repeat background unless this message asserts it.
- Most messages contain no durable fact (logistics, scheduling, thanks). Return an empty \
list for those.
- status is "firm" if stated plainly as fact, or "hedge" if tentative ("maybe", "probably", \
"thinking about", "not sure", "might", or conditional on something unconfirmed).
- confidence: 0.8 to 0.95 for firm, 0.3 to 0.5 for a hedge.
- reason: a short phrase for WHY, only if the message gives one (e.g. "new CFO froze \
spend", "champion left"). Else null.
- value is a short phrase, not a sentence."""


def extract_facts(body: str, speaker: str | None) -> list[Fact]:
    """Return the candidate facts the model found in this one message (may be empty)."""
    who = f"Speaker: {speaker}\n" if speaker else ""
    completion = _client_().chat.completions.parse(
        model=MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"{who}Message:\n{body}"},
        ],
        response_format=Extraction,
    )
    parsed = completion.choices[0].message.parsed
    return parsed.facts if parsed else []
