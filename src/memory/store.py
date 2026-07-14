"""Postgres persistence for DealFact rows.

Phase 0 is append-only: every extracted fact becomes a row, valid_from set, invalid_at
null. No supersede yet. That is the baseline that rots. Phase 1 adds the resolution step
(close old rows, move confidence) on top of these same tables.
"""

from __future__ import annotations

import os

import asyncpg

from src.memory.schema import DealFact

# Two tables, same shape:
#   deal_facts           append-only, every extracted fact, invalid_at always null (the "before")
#   deal_facts_resolved  the resolution pass output: superseded rows closed, hedges kept,
#                        confidence moved (the "after")
_COLUMNS = """
    id          BIGSERIAL PRIMARY KEY,
    account_id  TEXT        NOT NULL,
    attribute   TEXT        NOT NULL,
    value       TEXT        NOT NULL,
    status      TEXT        NOT NULL,
    confidence  REAL        NOT NULL,
    source      TEXT        NOT NULL,
    valid_from  DATE        NOT NULL,
    invalid_at  DATE,
    reason      TEXT,
    provenance  TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
"""

DDL = f"""
CREATE TABLE IF NOT EXISTS deal_facts ({_COLUMNS});
CREATE INDEX IF NOT EXISTS deal_facts_account_attr ON deal_facts (account_id, attribute);
CREATE TABLE IF NOT EXISTS deal_facts_resolved ({_COLUMNS});
CREATE INDEX IF NOT EXISTS deal_facts_resolved_account_attr ON deal_facts_resolved (account_id, attribute);
"""


async def connect() -> asyncpg.Connection:
    return await asyncpg.connect(os.environ["DATABASE_URL"])


async def init_schema(conn: asyncpg.Connection) -> None:
    await conn.execute(DDL)


async def clear_account(conn: asyncpg.Connection, account_id: str, table: str = "deal_facts") -> None:
    """Wipe one deal's rows from a table so a run starts clean."""
    await conn.execute(f"DELETE FROM {table} WHERE account_id = $1", account_id)


async def insert_fact(conn: asyncpg.Connection, fact: DealFact, table: str = "deal_facts") -> int:
    return await conn.fetchval(
        f"""
        INSERT INTO {table}
            (account_id, attribute, value, status, confidence, source,
             valid_from, invalid_at, reason, provenance)
        VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)
        RETURNING id
        """,
        fact.account_id, fact.attribute, fact.value, fact.status, fact.confidence,
        fact.source, fact.valid_from, fact.invalid_at, fact.reason, fact.provenance,
    )


def _rows_to_facts(rows) -> list[DealFact]:
    return [
        DealFact(
            account_id=r["account_id"], attribute=r["attribute"], value=r["value"],
            status=r["status"], confidence=r["confidence"], source=r["source"],
            valid_from=r["valid_from"], invalid_at=r["invalid_at"],
            reason=r["reason"], provenance=r["provenance"],
        )
        for r in rows
    ]


_SELECT = """
    SELECT account_id, attribute, value, status, confidence, source,
           valid_from, invalid_at, reason, provenance
"""


async def fetch_facts(conn: asyncpg.Connection, account_id: str, table: str = "deal_facts") -> list[DealFact]:
    rows = await conn.fetch(
        f"""
        {_SELECT}
        FROM {table}
        WHERE account_id = $1
        ORDER BY attribute, valid_from, id
        """,
        account_id,
    )
    return _rows_to_facts(rows)


async def fetch_facts_asof(
    conn: asyncpg.Connection, account_id: str, asof, table: str = "deal_facts_resolved"
) -> list[DealFact]:
    """The rows that were the live value on `asof`: opened on or before it and not yet closed."""
    rows = await conn.fetch(
        f"""
        {_SELECT}
        FROM {table}
        WHERE account_id = $1
          AND valid_from <= $2
          AND (invalid_at IS NULL OR invalid_at > $2)
        ORDER BY attribute, valid_from, id
        """,
        account_id, asof,
    )
    return _rows_to_facts(rows)
