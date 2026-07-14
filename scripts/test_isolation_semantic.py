"""Phase 4 proof: the cross-account leak is SEMANTIC, not a missing SQL filter.

Two deals in the SAME tenant (acme_sales), each with its own economic_buyer:

    acme_sales::Northwind Logistics   economic_buyer = Alan Pierce
    acme_sales::Cobalt Software       economic_buyer = Brenda Cole

The leak does not happen at the row filter. Both rows already carry the right
account_id. It happens in CONSOLIDATION: resolve walks the economic_buyer facts and
merges them into one timeline, and that merge is account-blind. The only thing that
decides whether Cobalt's buyer bleeds into Northwind's history is the SCOPE of the
candidate set handed to the merge.

  - vulnerable: widen the candidate set to the seller's deals (a cross-deal view, the
    natural feature that introduces the bug). Northwind's resolved economic_buyer now
    ends on Brenda Cole, Cobalt's buyer. LEAK.
  - guarded:    scope the candidate set to one account_id before merging (what
    resolve_account already does). Northwind's timeline holds only Alan Pierce. CLEAN.

The merge code is identical in both runs. Only the scope of what we feed it changes.
That is the whole point: WHERE tenant_id is not enough, because both deals are the same
tenant. The fence has to sit in front of the consolidation, on account_id.

  uv run test_isolation_semantic.py
"""

import asyncio
from datetime import date

import dotenv

dotenv.load_dotenv()

import _paths  # noqa: F401  -- adds the repo root to sys.path (see scripts/_paths.py)

from src.memory import store
from src.memory.resolve import _resolve_attribute
from src.memory.schema import DealFact

TENANT = "acme_sales"
ACCOUNT_A = f"{TENANT}::Northwind Logistics"
ACCOUNT_B = f"{TENANT}::Cobalt Software"
LEAKED_VALUE = "Brenda Cole"   # B's buyer; must never appear in A's resolved history


def _buyer(account_id: str, value: str, day: int) -> DealFact:
    return DealFact(
        account_id=account_id, attribute="economic_buyer", value=value,
        status="firm", confidence=0.9, source="seller",
        valid_from=date(2026, 1, day), provenance="isolation-test",
    )


def _consolidate(candidates: list[DealFact]) -> list[DealFact]:
    """The real merge (resolve._resolve_attribute), run over whatever candidate set it is
    given. resolve_account feeds it ONE account's facts. The leak is what happens when the
    candidate set is wider than that."""
    by_attr: dict[str, list[DealFact]] = {}
    for f in candidates:
        by_attr.setdefault(f.attribute, []).append(f)
    resolved: list[DealFact] = []
    for facts in by_attr.values():
        facts.sort(key=lambda f: f.valid_from)
        resolved.extend(_resolve_attribute(facts))
    return resolved


def _buyer_values(resolved: list[DealFact]) -> list[str]:
    return [f.value for f in resolved if f.attribute == "economic_buyer"]


async def main() -> None:
    conn = await store.connect()
    await store.init_schema(conn)

    # Seed: each deal has its own buyer, in the same tenant.
    for acc in (ACCOUNT_A, ACCOUNT_B):
        await store.clear_account(conn, acc, table="deal_facts")
    await store.insert_fact(conn, _buyer(ACCOUNT_A, "Alan Pierce", 1))
    await store.insert_fact(conn, _buyer(ACCOUNT_B, LEAKED_VALUE, 10))

    a_facts = await store.fetch_facts(conn, ACCOUNT_A, table="deal_facts")
    b_facts = await store.fetch_facts(conn, ACCOUNT_B, table="deal_facts")

    # VULNERABLE: candidate set = the seller's deals (A + B). Same merge, wider scope.
    widened = a_facts + b_facts
    leaked = _consolidate(widened)
    leaked_buyers = _buyer_values(leaked)

    # GUARDED: candidate set scoped to one account_id before the merge.
    guarded = _consolidate(a_facts)
    guarded_buyers = _buyer_values(guarded)

    print("Northwind's resolved economic_buyer history:\n")
    print(f"  BEFORE guard (candidate set widened to the seller's deals): {leaked_buyers}")
    print(f"  AFTER guard  (candidate set scoped to one account_id):      {guarded_buyers}\n")

    # Acceptance: actively try to leak. It must leak before the guard, not after.
    assert LEAKED_VALUE in leaked_buyers, (
        "expected the widened consolidation to blend Cobalt's buyer into Northwind"
    )
    print(f"  LEAK reproduced: {LEAKED_VALUE!r} (Cobalt's buyer) is in Northwind's history.")

    assert LEAKED_VALUE not in guarded_buyers, (
        "guard failed: Cobalt's buyer still reached Northwind's resolved history"
    )
    print(f"  LEAK closed:     {LEAKED_VALUE!r} is absent once the merge is scoped to the account.")
    print("\nPASS: the leak is in consolidation, and account-scoped candidates close it.")

    await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
