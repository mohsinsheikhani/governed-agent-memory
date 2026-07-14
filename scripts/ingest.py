"""Ingest one deal stream. A single pass over the messages fans out to both stores:

  - Zep        the raw temporal record (narrative, history, why)  -> user_id tenant::account
  - DealFact   the typed decision record (Postgres)               -> structured slots

Phase 0/1, no Job 2. DealFact writes are append-only for now (no supersede), so this is
also the baseline that rots. Resolution comes next.

  uv run ingest.py            # defaults to K1
  uv run ingest.py H1
"""

import asyncio
import os
import sys
from datetime import datetime, timedelta

import dotenv
from zep_cloud import Message
from zep_cloud.client import AsyncZep

dotenv.load_dotenv()
ZEP_API_KEY = os.environ["ZEP_API_KEY"]

import _paths  # noqa: F401  -- adds the repo root to sys.path (see scripts/_paths.py)

from src.data.streams import load_streams
from src.memory import store
from src.memory.extract import extract_facts
from src.memory.resolve import resolve_account
from src.memory.schema import DealFact

BASE_DATE = datetime(2026, 1, 1)
CONTENT_SOURCES = {"buyer_direct", "buyer_forwarded", "seller"}
# Map message source to a Zep role. seller_query is Job 2 and is skipped entirely.
ZEP_ROLE = {"buyer_direct": "user", "buyer_forwarded": "user", "seller": "assistant"}


def get_stream(stream_id: str):
    for s in load_streams():
        if s.stream_id == stream_id:
            return s
    raise SystemExit(f"stream {stream_id} not found")


async def _poll_edges(client, user_id, query, expect, timeout=120):
    waited, edges = 0, []
    while waited < timeout:
        res = await client.graph.search(query=query, user_id=user_id, scope="edges", limit=25)
        edges = res.edges or []
        if len(edges) >= expect:
            return edges
        await asyncio.sleep(5)
        waited += 5
    return edges


async def main(stream_id: str) -> None:
    stream = get_stream(stream_id)
    tenant, account = stream.tenant_id, stream.account
    account_id = f"{tenant}::{account}"
    thread_id = f"{account_id}::thread"
    print(f"Stream {stream_id}: {account_id} (seller {stream.seller})\n")

    zep = AsyncZep(api_key=ZEP_API_KEY)
    conn = await store.connect()
    await store.init_schema(conn)

    # Fresh start for this deal in both stores.
    try:
        await zep.user.delete(account_id)
    except Exception:
        pass
    await zep.user.add(user_id=account_id, first_name=account)
    await zep.thread.create(thread_id=thread_id, user_id=account_id)
    await store.clear_account(conn, account_id)

    written = 0
    for m in stream.ingest_order():
        if m.source not in CONTENT_SOURCES:
            continue
        msg_date = BASE_DATE + timedelta(days=m.day)

        # 1. Raw record -> Zep.
        await zep.thread.add_messages(
            thread_id=thread_id,
            messages=[Message(
                name=m.speaker or m.source,
                role=ZEP_ROLE.get(m.source, "user"),
                content=m.body,
                created_at=msg_date.strftime("%Y-%m-%dT09:00:00Z"),
            )],
        )

        # 2. Typed record -> DealFact (append-only).
        for c in extract_facts(m.body, m.speaker):
            fact = DealFact(
                account_id=account_id,
                attribute=c.attribute,
                value=c.value,
                status=c.status,
                confidence=c.confidence,
                source=m.source,
                valid_from=msg_date.date(),
                reason=c.reason or None,
                provenance=f"{stream_id}:turn{m.turn}",
            )
            await store.insert_fact(conn, fact)
            written += 1
            print(f"  day{m.day:>3} [{m.source:14s}] {fact.attribute} = {fact.value}"
                  f"  ({fact.status}, conf {fact.confidence})")

    print(f"\n===== BEFORE: append-only ({written} rows, every one live) =====")
    for f in await store.fetch_facts(conn, account_id):
        print(f"  [{f.attribute}] {f.value}  status={f.status} from={f.valid_from} src={f.source}")

    print("\n===== AFTER: resolved (supersede + confidence) =====")
    resolved = await resolve_account(conn, account_id)
    for f in sorted(resolved, key=lambda x: (x.attribute, x.valid_from)):
        mark = "CURRENT" if f.is_current else "closed "
        act = " [actionable]" if f.is_actionable else ""
        print(f"  {mark} [{f.attribute}] {f.value}  status={f.status} conf={f.confidence:.2f} "
              f"from={f.valid_from} to={f.invalid_at}{act}")
    await conn.close()

    edges = await _poll_edges(zep, account_id, f"What is true about {account}?", expect=5)
    print(f"\n===== ZEP EDGES ({len(edges)}) =====")
    for e in sorted(edges, key=lambda x: x.valid_at or ""):
        status = "VALID" if e.invalid_at is None else "INVALIDATED"
        print(f"  [{status}] {e.fact}")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "K1"))
