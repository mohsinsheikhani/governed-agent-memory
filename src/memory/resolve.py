"""Phase 1 resolution: turn the append-only rows into resolved slots.

Reads `deal_facts` (append-only, the baseline) in time order and writes
`deal_facts_resolved` where each slot has one current value with its history closed
behind it. This is the confidence/hedge layer Zep does not provide.

Split of labor:
  - the LLM judges ONLY the fuzzy comparison: does the new fact restate / replace /
    qualify the current value (Helen vs Helen Voss, approved vs frozen vs under review).
  - Python applies the deterministic rules on status + confidence and supersession.

The transitions (see the confidence/hedge layer table):
  restate   same value            -> refresh; a firm restatement upgrades a prior hedge
  qualify   same value, certainty  -> keep value, move status (firm<->under_review), H5
  replace   different value, firm  -> supersede: close old with invalid_at, open new
  replace   different value, hedge -> keep current firm value, store the hedge alongside
                                       (never act on a maybe)
"""

from __future__ import annotations

import os
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel

from src.memory import store
from src.memory.schema import DealFact

MODEL = "gpt-4o"

# Confidence levels the layer settles on after a transition.
FIRM = 0.9
RESTORED = 0.85
REVIEW = 0.4

_client: OpenAI | None = None


def _client_() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return _client


class Relation(BaseModel):
    relation: Literal["restate", "replace", "qualify"]
    canonical_value: str   # best single phrasing to keep (prefer the fuller/clearer one)


_REL_SYSTEM = """You compare two facts about the SAME attribute of a sales deal and decide \
their relationship.

- restate: the new fact states the same value as the current one, just worded differently \
or repeated (e.g. "Helen" vs "Helen Voss"; "54k" vs "54k a year"; "approved" vs "approved").
- replace: the value genuinely CHANGED to a new state (e.g. economic_buyer "Helen" -> \
"Greg"; budget_status "approved" -> "frozen"; timeline "this quarter" -> "next year").
- qualify: the value is UNCHANGED but the certainty around it changed (e.g. budget_status \
"approved" -> "under review": the budget is still the approved one, it is just being \
re-checked, not a new state).

The key distinction between replace and qualify: replace = a different real-world value; \
qualify = same value, different confidence.

Return the relation and canonical_value, the single best phrasing of the value to keep."""

_cache: dict[tuple, Relation] = {}


def _relation(attribute: str, current: DealFact, new: DealFact) -> Relation:
    if current.value.strip().lower() == new.value.strip().lower():
        return Relation(relation="restate", canonical_value=current.value)
    key = (attribute, current.value, current.status, new.value, new.status)
    if key in _cache:
        return _cache[key]
    completion = _client_().chat.completions.parse(
        model=MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": _REL_SYSTEM},
            {"role": "user", "content": (
                f"attribute: {attribute}\n"
                f"current: value={current.value!r} status={current.status}\n"
                f"new:     value={new.value!r} status={new.status}"
            )},
        ],
        response_format=Relation,
    )
    rel = completion.choices[0].message.parsed
    _cache[key] = rel
    return rel


def _copy(fact: DealFact, **changes) -> DealFact:
    fields = dict(
        account_id=fact.account_id, attribute=fact.attribute, value=fact.value,
        status=fact.status, confidence=fact.confidence, source=fact.source,
        valid_from=fact.valid_from, invalid_at=fact.invalid_at,
        reason=fact.reason, provenance=fact.provenance,
    )
    fields.update(changes)
    return DealFact(**fields)


def _resolve_attribute(candidates: list[DealFact]) -> list[DealFact]:
    """Walk one slot's facts in time order, return the resolved rows for that slot."""
    rows: list[DealFact] = []          # everything we keep (closed + open)
    current: DealFact | None = None    # the open primary (firm or under_review) row

    for c in candidates:
        if current is None:
            current = _copy(c)
            rows.append(current)
            continue

        rel = _relation(c.attribute, current, c)

        if rel.relation == "restate":
            current.value = rel.canonical_value
            if c.status == "firm" and current.status != "firm":
                current.status, current.confidence = "firm", max(RESTORED, c.confidence)
            else:
                current.confidence = max(current.confidence, c.confidence)

        elif rel.relation == "qualify":
            current.value = rel.canonical_value
            if c.status == "firm":
                current.status, current.confidence = "firm", max(RESTORED, c.confidence)
            else:  # a hedge over a firm value dents confidence but does not flip it (H5)
                current.status, current.confidence = "under_review", REVIEW

        else:  # replace
            if c.status == "firm":
                current.invalid_at = c.valid_from          # close the old value
                current = _copy(c, confidence=max(FIRM, c.confidence))
                rows.append(current)                        # open the new current
            else:
                rows.append(_copy(c))                       # keep the hedge alongside, do not supersede

    return rows


async def resolve_account(conn, account_id: str) -> list[DealFact]:
    raw = await store.fetch_facts(conn, account_id, table="deal_facts")
    by_attr: dict[str, list[DealFact]] = {}
    for f in raw:
        by_attr.setdefault(f.attribute, []).append(f)

    resolved: list[DealFact] = []
    for attr, facts in by_attr.items():
        facts.sort(key=lambda f: f.valid_from)
        resolved.extend(_resolve_attribute(facts))

    await store.clear_account(conn, account_id, table="deal_facts_resolved")
    for f in resolved:
        await store.insert_fact(conn, f, table="deal_facts_resolved")
    return resolved


if __name__ == "__main__":
    import asyncio
    import sys

    import dotenv
    dotenv.load_dotenv()

    async def _run(account_id: str):
        conn = await store.connect()
        await store.init_schema(conn)
        resolved = await resolve_account(conn, account_id)
        for f in sorted(resolved, key=lambda x: (x.attribute, x.valid_from)):
            mark = "CURRENT " if f.is_current else "closed  "
            act = " [actionable]" if f.is_actionable else ""
            print(f"  {mark}[{f.attribute}] {f.value}  status={f.status} conf={f.confidence:.2f} "
                  f"from={f.valid_from} to={f.invalid_at}{act}")
        await conn.close()

    asyncio.run(_run(sys.argv[1] if len(sys.argv) > 1 else "acme_sales::Meridian Components"))
