"""Phase 4 proof: recontamination-proof erasure of one person from a deal.

A buyer-side contact (Helen Voss) exercises the right to erasure. She must disappear from
every store, while the deal and its non-personal audit (budget 54k) survive.

The test reproduces the recontamination bug, then closes it:

  RED  (naive)   delete Helen from the resolved VIEW only, then re-run consolidation.
                 She comes back, rebuilt from the append-only source. Not erased.
  GREEN (cascade) erase_subject: tombstone + delete from source AND view + redact free
                 text + delete Zep edges. Re-run consolidation, attempt a re-ingest of
                 Helen. She stays gone, and the deal's budget is untouched.

Postgres assertions are deterministic and hard. The Zep leg runs the real per-edge delete
against a freshly seeded graph; because Zep ingestion is async, it is best-effort and
reported, not hard-asserted on timing.

  uv run test_erasure_cascade.py
"""

import asyncio
import os
from datetime import date, timedelta

import dotenv

dotenv.load_dotenv()

from zep_cloud import Message
from zep_cloud.client import AsyncZep

import _paths  # noqa: F401  -- adds the repo root to sys.path (see scripts/_paths.py)

from src.memory import erase, store
from src.memory.resolve import resolve_account
from src.memory.schema import DealFact

ACCOUNT = "acme_sales::__erasure_demo__"
THREAD = f"{ACCOUNT}::thread"
SUBJECT = "Helen Voss"


def _fact(attribute: str, value: str, day: int, reason: str | None = None) -> DealFact:
    return DealFact(
        account_id=ACCOUNT, attribute=attribute, value=value, status="firm",
        confidence=0.9, source="seller", valid_from=date(2026, 1, 1) + timedelta(days=day),
        reason=reason, provenance="erasure-test",
    )


def _values(facts) -> list[str]:
    return [f.value for f in facts]


def _mentions(facts, name: str) -> bool:
    n = name.lower()
    return any(n in (f.value or "").lower() or n in (f.reason or "").lower() for f in facts)


async def _seed_zep(zep) -> None:
    try:
        await zep.user.delete(ACCOUNT)
    except Exception:
        pass
    await zep.user.add(user_id=ACCOUNT, first_name="erasure demo")
    await zep.thread.create(thread_id=THREAD, user_id=ACCOUNT)
    await zep.thread.add_messages(thread_id=THREAD, messages=[Message(
        name="seller", role="assistant",
        content="Helen Voss was the economic buyer and signed off on the 54k budget.",
        created_at="2026-01-02T09:00:00Z",
    )])
    # Zep ingestion is async; wait (bounded) for the edge to exist so erasure has something
    # real to delete. If it never lands, the Postgres proof still stands on its own.
    for _ in range(24):
        res = await zep.graph.search(query=SUBJECT, user_id=ACCOUNT, scope="edges", limit=10)
        if any(SUBJECT.lower() in (e.fact or "").lower() for e in (res.edges or [])):
            return
        await asyncio.sleep(5)


async def main() -> None:
    conn = await store.connect()
    await store.init_schema(conn)
    await erase.init_tombstones(conn)
    await store.clear_account(conn, ACCOUNT, table="deal_facts")
    await store.clear_account(conn, ACCOUNT, table="deal_facts_resolved")
    await conn.execute("DELETE FROM erasures WHERE account_id = $1", ACCOUNT)

    # Seed: Helen is the economic buyer, then Greg takes over (reason names Helen). Budget
    # 54k is non-personal and must survive erasure.
    await store.insert_fact(conn, _fact("economic_buyer", "Helen Voss", 1))
    await store.insert_fact(conn, _fact("economic_buyer", "Greg Holt", 45,
                                        reason="took over after Helen Voss left"))
    await store.insert_fact(conn, _fact("budget_amount", "54k", 1))
    await resolve_account(conn, ACCOUNT)

    resolved = await store.fetch_facts(conn, ACCOUNT, "deal_facts_resolved")
    assert _mentions(resolved, SUBJECT), "setup: Helen should be in the resolved record"
    print(f"Seeded. Resolved economic_buyer history: "
          f"{[f.value for f in resolved if f.attribute == 'economic_buyer']}\n")

    # ---- RED: naive delete of the resolved VIEW only ----
    await conn.execute(
        "DELETE FROM deal_facts_resolved WHERE account_id = $1 AND value ILIKE '%' || $2 || '%'",
        ACCOUNT, SUBJECT,
    )
    gone = await store.fetch_facts(conn, ACCOUNT, "deal_facts_resolved")
    assert SUBJECT not in _values(gone), "naive delete should clear the value from the view"
    # routine re-consolidation runs...
    await resolve_account(conn, ACCOUNT)
    rebuilt = await store.fetch_facts(conn, ACCOUNT, "deal_facts_resolved")
    assert SUBJECT in _values(rebuilt), "expected recontamination from the source"
    print("  RED  naive delete: cleared the view, then re-resolve REBUILT Helen from the "
          "source. Recontaminated.")

    # ---- GREEN: full cascade ----
    zep = AsyncZep(api_key=os.environ["ZEP_API_KEY"])
    await _seed_zep(zep)
    report = await erase.erase_subject(conn, zep, ACCOUNT, SUBJECT, request_id="dsr-001")

    await resolve_account(conn, ACCOUNT)  # re-consolidate again, the recontamination path
    blocked = await erase.guarded_insert(conn, _fact("economic_buyer", "Helen Voss", 60))  # re-ingest

    src = await store.fetch_facts(conn, ACCOUNT, "deal_facts")
    view = await store.fetch_facts(conn, ACCOUNT, "deal_facts_resolved")
    budget_alive = any(f.attribute == "budget_amount" and f.value == "54k" for f in view)

    assert not _mentions(src, SUBJECT), "Helen still in the source after cascade"
    assert not _mentions(view, SUBJECT), "Helen still in the view after cascade + re-resolve"
    assert blocked is None, "re-ingest of an erased subject should be refused"
    assert budget_alive, "the deal's non-personal audit must survive erasure"
    assert await erase.is_erased(conn, ACCOUNT, SUBJECT), "tombstone missing"

    print(f"  GREEN cascade: deleted from source+view, redacted free text, removed "
          f"{report['zep_edges_deleted']} Zep edge(s), tombstoned.")
    print( "        re-resolve did NOT rebuild her; re-ingest was refused; budget 54k intact.")
    print(f"\nResolved economic_buyer after erasure: "
          f"{[f.value for f in view if f.attribute == 'economic_buyer']}")
    print("\nPASS: recontamination-proof. Source + view + graph scrubbed, deal audit kept.")

    await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
