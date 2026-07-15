"""GDPR Art. 17 erasure cascade: scrub one PERSON from a deal without destroying the deal.

The erasure trigger in B2B sales is not "delete the deal" and not "a seller left" (that is
access revocation, handled by the authority layer). It is a buyer-side individual exercising
their right to erasure. So the job is selective: remove that person's personal data across
every store, while the deal's non-personal audit (budget approved at 54k) survives.

The hard property is recontamination-proofness. DealFact is two tables: deal_facts (the
append-only SOURCE) and deal_facts_resolved (the view consolidation rebuilds from it). Zep
holds the same person in its graph. Deleting one store is not erasure:

  - delete only the resolved view -> the next resolve_account rebuilds the person from deal_facts
  - delete Postgres but not Zep   -> search_conversation surfaces the person from the graph
  - delete the rows but not record it -> a later re-ingest re-adds the person

So the cascade (1) writes a TOMBSTONE that future writes consult, (2) deletes the person
from the source and every derived store, and (3) redacts the person from surviving rows'
free text. After it runs, re-resolving or re-ingesting cannot bring the person back.

Scope: vector erasure is delegated to Zep (deleting an edge drops its embedding with it).
There is no summary store yet; the tombstone is what would protect one when it is added.
"""

from __future__ import annotations

import asyncpg

from src.memory import store
from src.memory.schema import DealFact

TOMBSTONE_DDL = """
CREATE TABLE IF NOT EXISTS erasures (
    id          BIGSERIAL PRIMARY KEY,
    account_id  TEXT        NOT NULL,
    subject     TEXT        NOT NULL,
    request_id  TEXT,
    erased_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (account_id, subject)
);
"""

REDACTED = "[erased]"


async def init_tombstones(conn: asyncpg.Connection) -> None:
    await conn.execute(TOMBSTONE_DDL)


async def is_erased(conn: asyncpg.Connection, account_id: str, text: str) -> bool:
    """True if `text` references any erased subject for this account. Write paths call this
    so a re-ingest that mentions an erased person is refused, not silently re-added."""
    hit = await conn.fetchval(
        "SELECT 1 FROM erasures WHERE account_id = $1 AND $2 ILIKE '%' || subject || '%' LIMIT 1",
        account_id, text,
    )
    return hit is not None


async def erased_subjects(conn: asyncpg.Connection, account_id: str) -> list[str]:
    rows = await conn.fetch(
        "SELECT subject, request_id, erased_at FROM erasures WHERE account_id = $1 ORDER BY erased_at",
        account_id,
    )
    return [r["subject"] for r in rows]


async def guarded_insert(conn: asyncpg.Connection, fact: DealFact, table: str = "deal_facts") -> int | None:
    """store.insert_fact, but refuses to write anything that references an erased subject.
    This is the hook ingest uses so erasure survives re-ingestion of the same stream."""
    if await is_erased(conn, fact.account_id, fact.value) or (
        fact.reason and await is_erased(conn, fact.account_id, fact.reason)
    ):
        return None
    return await store.insert_fact(conn, fact, table)


async def _erase_from_postgres(conn: asyncpg.Connection, account_id: str, subject: str) -> dict[str, str]:
    """Delete rows whose VALUE is the subject (those rows are about the person), and redact
    the subject out of surviving rows' free text (reason). Runs on both tables: the source
    AND the derived view, so re-resolution cannot reintroduce the person."""
    out: dict[str, str] = {}
    for table in ("deal_facts", "deal_facts_resolved"):
        deleted = await conn.execute(
            f"DELETE FROM {table} WHERE account_id = $1 AND value ILIKE '%' || $2 || '%'",
            account_id, subject,
        )
        await conn.execute(
            f"UPDATE {table} SET reason = $3 WHERE account_id = $1 AND reason ILIKE '%' || $2 || '%'",
            account_id, subject, REDACTED,
        )
        out[table] = deleted
    return out


async def _erase_from_zep(zep, account_id: str, subject: str) -> int:
    """Delete the graph edges that mention the subject, scoped to this deal's user_id.
    Deleting the edge drops its embedding with it, so this is the vector erasure too. The
    deal's other edges (and the user) are untouched."""
    res = await zep.graph.search(query=subject, user_id=account_id, scope="edges", limit=50)
    hits = [e for e in (res.edges or []) if subject.lower() in (e.fact or "").lower()]
    for e in hits:
        await zep.graph.edge.delete(e.uuid_)
    return len(hits)


async def erase_subject(
    conn: asyncpg.Connection, zep, account_id: str, subject: str, request_id: str | None = None
) -> dict:
    """The cascade. Tombstone first (so the audit exists and concurrent writes are blocked),
    then delete from every store. Idempotent: re-running it is a no-op."""
    await conn.execute(
        "INSERT INTO erasures (account_id, subject, request_id) VALUES ($1, $2, $3) "
        "ON CONFLICT (account_id, subject) DO NOTHING",
        account_id, subject, request_id,
    )
    pg = await _erase_from_postgres(conn, account_id, subject)
    zep_edges = await _erase_from_zep(zep, account_id, subject) if zep is not None else 0
    return {"postgres": pg, "zep_edges_deleted": zep_edges}
