"""Phase 1 measurement: append-only vs resolved, across all seeded streams.

There is no structured gold answer per stream (expected_text is prose), so this does not
claim graded accuracy. It measures the thing the resolution layer actually exists to fix:
whether a store gives ONE consistent current answer per deal fact, or a contradictory pile.

For each attribute slot, look at the values that read as current AND firm:
  - append-only: every extracted fact stays live (invalid_at is always null), so a slot
    whose value changed (approved -> frozen) shows BOTH as current. Ambiguous.
  - resolved: supersession closes the old value and hedges are parked as non-actionable,
    so a slot reads as one current firm answer.

A slot is "clean" when it yields exactly one current firm value. The headline is the
clean rate: how much of the deal you can answer without tripping over a contradiction.

No Zep, no DB writes. Extraction runs in memory per stream, then the real resolve merge.

  uv run measure.py
"""

from __future__ import annotations

import asyncio
from collections import defaultdict
from datetime import datetime, timedelta

import dotenv

dotenv.load_dotenv()

import _paths  # noqa: F401  -- adds the repo root to sys.path (see scripts/_paths.py)

from src.data.streams import load_streams
from src.memory.extract import extract_facts
from src.memory.resolve import _resolve_attribute
from src.memory.schema import DealFact

BASE_DATE = datetime(2026, 1, 1)
CONTENT_SOURCES = {"buyer_direct", "buyer_forwarded", "seller"}
BUCKETS = ["clean", "contradiction", "hedge_contradiction", "poisoning", "isolation"]


def _append_only(stream) -> list[DealFact]:
    """Run extraction over the stream's messages into append-only facts (all live)."""
    facts: list[DealFact] = []
    for m in stream.ingest_order():
        if m.source not in CONTENT_SOURCES:
            continue
        day = BASE_DATE + timedelta(days=m.day)
        for c in extract_facts(m.body, m.speaker):
            facts.append(DealFact(
                account_id=stream.stream_id, attribute=c.attribute, value=c.value,
                status=c.status, confidence=c.confidence, source=m.source,
                valid_from=day.date(), reason=c.reason or None,
            ))
    return facts


def _resolve(facts: list[DealFact]) -> list[DealFact]:
    by_attr: dict[str, list[DealFact]] = defaultdict(list)
    for f in facts:
        by_attr[f.attribute].append(f)
    out: list[DealFact] = []
    for slot in by_attr.values():
        slot.sort(key=lambda f: f.valid_from)
        out.extend(_resolve_attribute(slot))
    return out


def _clean(facts: list[DealFact]) -> tuple[int, int]:
    """(clean slots, answerable slots). A slot is answerable if it has any current firm
    value, clean if it has exactly one distinct current firm value."""
    vals: dict[str, set[str]] = defaultdict(set)
    for f in facts:
        if f.is_current and f.status == "firm":
            vals[f.attribute].add(f.value.strip().lower())
    answerable = len(vals)
    clean = sum(1 for v in vals.values() if len(v) == 1)
    return clean, answerable


async def main() -> None:
    streams = load_streams()
    per_bucket: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0])  # base_clean, res_clean, answerable
    tot = [0, 0, 0]

    print(f"Measuring {len(streams)} streams (extracting, then resolving)...\n")
    print(f"{'stream':6} {'bucket':20} {'slots':5} {'append-only':>12} {'resolved':>10}")
    for s in streams:
        ao = _append_only(s)
        rs = _resolve(ao)
        b_clean, answerable = _clean(ao)
        r_clean, _ = _clean(rs)
        per_bucket[s.bucket][0] += b_clean
        per_bucket[s.bucket][1] += r_clean
        per_bucket[s.bucket][2] += answerable
        tot[0] += b_clean; tot[1] += r_clean; tot[2] += answerable
        print(f"{s.stream_id:6} {s.bucket:20} {answerable:5} "
              f"{b_clean:>5}/{answerable:<3} {r_clean:>5}/{answerable:<3}")

    def pct(n, d): return f"{100*n/d:.0f}%" if d else "n/a"

    print(f"\n{'bucket':20} {'append-only':>12} {'resolved':>10}")
    for b in BUCKETS:
        bc, rc, an = per_bucket[b]
        if an:
            print(f"{b:20} {pct(bc,an):>12} {pct(rc,an):>10}")

    print(f"\nOVERALL single-current-answer rate across {len(streams)} streams "
          f"({tot[2]} deal-fact slots):")
    print(f"  append-only: {pct(tot[0], tot[2])}   ({tot[0]}/{tot[2]} slots unambiguous)")
    print(f"  resolved:    {pct(tot[1], tot[2])}   ({tot[1]}/{tot[2]} slots unambiguous)")


if __name__ == "__main__":
    asyncio.run(main())
