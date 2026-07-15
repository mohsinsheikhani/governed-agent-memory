"""Job 2: the seller-facing read agent.

The seller talks, the agent answers from what Job 1 built. It NEVER writes to
deal_facts. It only reads:

  - the typed verdict   -> deal_facts_resolved (what / when / how firm)
  - the evidence        -> Zep narrative graph  (why / what was said / how sure)

Division of labor (the whole point of this agent):
  - "what is true / who is the buyer / status last month"  -> the resolved table.
    Deterministic, no guessing, carries firm/hedge so the agent cannot overstate.
  - "why / how sure are you / what made you say that"       -> reason over Zep.
    The resolved table threw the sentences away; only the graph has the receipts.

Run (token + deal name + question; the token decides who you are and what you can open):
  uv run agent.py tok_dana_acme "Cobalt Software" \
      "How sure are you the buyer is serious about Enterprise, and why?"
"""

from __future__ import annotations

import asyncio
import sys
from dataclasses import dataclass
from datetime import date

import dotenv
from agents import Agent, RunContextWrapper, Runner, function_tool
from zep_cloud.client import AsyncZep

dotenv.load_dotenv()

import os
import _paths  # noqa: F401  -- adds the repo root to sys.path (see scripts/_paths.py)
import auth
from src.memory import store

MODEL = "gpt-4o"


@dataclass
class DealContext:
    """One deal in scope for the whole conversation. The seller is asking about THIS
    account, so the account_id is fixed here, not chosen by the model."""
    conn: object          # asyncpg connection
    zep: AsyncZep
    account_id: str       # tenant::account, doubles as the Zep user_id
    account: str          # display name


def _fmt(facts) -> str:
    if not facts:
        return "(no rows)"
    out = []
    for f in facts:
        closed = "" if f.is_current else f" (closed {f.invalid_at})"
        out.append(
            f"- {f.attribute} = {f.value} | status={f.status} "
            f"confidence={f.confidence:.2f} | from {f.valid_from}{closed} | source={f.source}"
        )
    return "\n".join(out)


@function_tool
async def get_current_state(ctx: RunContextWrapper[DealContext]) -> str:
    """Return the deal's CURRENT typed state: one live value per attribute with its
    status (firm / hedge / under_review) and confidence. Use this for any 'what is true
    now', 'who is the X', 'what is the status' question, and to see which slots are soft
    before you go looking for reasons."""
    facts = await store.fetch_facts(ctx.context.conn, ctx.context.account_id, "deal_facts_resolved")
    current = [f for f in facts if f.is_current]
    return _fmt(current)


@function_tool
async def get_state_at(ctx: RunContextWrapper[DealContext], on_date: str) -> str:
    """Return the typed state that was live on a specific date. `on_date` is ISO format
    YYYY-MM-DD. Use this for time-bound history: 'what was the status last month',
    'who was the buyer in March', 'before they approved it'. The deal timeline runs in
    early 2026; if you need a transition date, call get_current_state first and read the
    'from' dates."""
    try:
        asof = date.fromisoformat(on_date)
    except ValueError:
        return f"bad date {on_date!r}, expected YYYY-MM-DD"
    facts = await store.fetch_facts_asof(ctx.context.conn, ctx.context.account_id, asof)
    if facts:
        return f"State live on {asof}:\n{_fmt(facts)}"
    # Nothing on that date. Tell the model where this deal's record actually sits so it
    # can correct a wrong year/month instead of concluding "no information".
    allf = await store.fetch_facts(ctx.context.conn, ctx.context.account_id, "deal_facts_resolved")
    if not allf:
        return f"No record for {asof}, and this deal has no recorded history at all."
    dates = [f.valid_from for f in allf] + [f.invalid_at for f in allf if f.invalid_at]
    return (
        f"Nothing was recorded as of {asof}. This deal's record runs from "
        f"{min(dates)} to {max(dates)}. If you meant a time inside that range, "
        f"re-query with a date in it."
    )


@function_tool
async def search_conversation(ctx: RunContextWrapper[DealContext], query: str) -> str:
    """Search the actual deal conversation for what was said. Returns narrative facts
    from the buyer/seller exchange. Use this for 'why', 'how sure are you', 'what made
    you conclude that' questions, where you must cite real lines and not the typed field.
    `query` is a natural-language search like 'enterprise tier interest' or 'budget'."""
    res = await ctx.context.zep.graph.search(
        query=query, user_id=ctx.context.account_id, scope="edges", limit=15
    )
    edges = res.edges or []
    if not edges:
        return "(no matching conversation found)"
    lines = []
    for e in edges:
        tag = "current" if e.invalid_at is None else f"no longer true (since {e.invalid_at})"
        lines.append(f"- {e.fact} [{tag}]")
    return "\n".join(lines)


INSTRUCTIONS = """You are a sales assistant talking to a busy salesperson about one of \
their deals. Answer like a sharp colleague who has been following the deal, not like a \
database. Give them the answer they actually want.

You have two ways to look things up. Use them, but never talk about them:

1. get_current_state / get_state_at give you the current and past facts of the deal and \
how settled each one is. Use these to know WHAT is true, WHO is involved, WHEN things \
changed, and how solid each fact is.

2. search_conversation gives you what the buyer and seller actually said. Use this to \
understand WHY things are the way they are and to judge how the buyer really feels.

How to decide which to use:
- 'What / who / when' questions: look up the facts and answer plainly.
- For any question about a PAST time ('back in January', 'last month', 'at the start'), \
do not assume what year or month it is. First call get_current_state to see the deal's \
real dates, then call get_state_at with a date that actually falls inside that period.
- 'Why / how sure / is the buyer serious' questions: first glance at the facts to see \
which part of the deal is shaky, THEN read the conversation and reason from what was \
actually said. Your judgement must come from the discussion, not from any stored number.

Hard rules:
- Talk like a human. NEVER mention 'state', 'status', 'confidence', 'rows', percentages, \
or how the data is stored. The salesperson does not care. Just answer.
- Do not recite a confidence number as if it were a reason. If you say the buyer is not \
fully committed, back it with what they actually said ('she called it a maybe', 'she \
tied it to a launch that hasn't happened'), not with a score.
- If something was only floated as a maybe, say so plainly and do not present it as \
decided. If the deal record genuinely has nothing on what was asked, say you don't have \
anything on it rather than guessing.
- Lead with the answer in plain language, then a sentence or two of why."""


async def main(token: str, deal: str, question: str) -> None:
    # Identity and scope are settled here, from the token, before any agent exists. The
    # tenant is never taken from input; the deal must be granted. A breach is impossible
    # to even express, because account_id is built from the principal's own tenant.
    principal, account_id = auth.open_deal(token, deal)
    account = deal

    conn = await store.connect()
    zep = AsyncZep(api_key=os.environ["ZEP_API_KEY"])
    ctx = DealContext(conn=conn, zep=zep, account_id=account_id, account=account)

    dated = f"Today's date is {date.today().isoformat()}. Resolve any relative time the " \
            f"seller mentions ('last month', 'back in January') against today's date, " \
            f"not against any assumed year.\n\n" + INSTRUCTIONS
    agent = Agent[DealContext](
        name="deal assistant",
        instructions=dated,
        model=MODEL,
        tools=[get_current_state, get_state_at, search_conversation],
    )

    print(f"Seller: {principal.name} ({principal.tenant_id})")
    print(f"Deal: {account_id}\nSeller asks: {question}\n")
    result = await Runner.run(agent, question, context=ctx)
    print(result.final_output)
    await conn.close()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise SystemExit('usage: uv run agent.py <token> "<deal>" "<question>"')
    try:
        asyncio.run(main(sys.argv[1], sys.argv[2], sys.argv[3]))
    except (auth.AuthError, auth.AccessDenied) as e:
        raise SystemExit(f"DENIED: {e}")
