"""Typed model + JSONL loader for the synthetic deal streams.

The markdown in `data/streams/*.md` is the human source of truth. `convert.py` compiles
it to JSONL; this module defines the records and reads them back for an agent run.

A run replays a stream's `messages` in order. A message whose `source == "seller_query"`
is a Job 2 trigger (the rep asking the agent). The runner never reads `expected_text` /
`poison_line` / `expected_facts` -- those are for the grader.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator

# Source tags double as the trust key (see IMPLEMENTATION_PLAN.md Section 3.0).
SOURCES = {"buyer_direct", "buyer_forwarded", "seller", "seller_query"}
CHANNELS = {"email", "call_note", "query"}


@dataclass
class Message:
    turn: int          # 1-based order within the stream
    day: int           # simulated day, gives temporal validity something to bite on
    source: str        # one of SOURCES (the trust key)
    channel: str       # one of CHANNELS
    speaker: str | None
    role: str | None
    body: str          # poison markers already stripped; the agent sees exactly this

    @property
    def is_query(self) -> bool:
        return self.source == "seller_query"

    def to_dict(self) -> dict:
        return {
            "turn": self.turn,
            "day": self.day,
            "source": self.source,
            "channel": self.channel,
            "speaker": self.speaker,
            "role": self.role,
            "body": self.body,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Message":
        return cls(
            turn=d["turn"],
            day=d["day"],
            source=d["source"],
            channel=d["channel"],
            speaker=d.get("speaker"),
            role=d.get("role"),
            body=d["body"],
        )


@dataclass
class Stream:
    stream_id: str          # C1, K3, H5, P2, 1A ...
    bucket: str             # clean | contradiction | hedge_contradiction | poisoning | isolation
    tenant_id: str
    account: str
    product: str | None
    price: str | None
    seller: str | None
    messages: list[Message] = field(default_factory=list)
    expected_text: str = ""        # the golden answer block, raw markdown (grader reads this)
    expected_facts: list[dict] = field(default_factory=list)  # optional structured facts (added later)
    poison_line: str | None = None  # the extracted false claim, for the promotion check
    pair: str | None = None         # isolation pair number, else None

    @property
    def queries(self) -> list[Message]:
        return [m for m in self.messages if m.is_query]

    def ingest_order(self) -> list[Message]:
        """Messages in replay order (document order, stable within a day)."""
        return sorted(self.messages, key=lambda m: (m.day, m.turn))

    def to_dict(self) -> dict:
        return {
            "stream_id": self.stream_id,
            "bucket": self.bucket,
            "tenant_id": self.tenant_id,
            "account": self.account,
            "product": self.product,
            "price": self.price,
            "seller": self.seller,
            "messages": [m.to_dict() for m in self.messages],
            "expected_text": self.expected_text,
            "expected_facts": self.expected_facts,
            "poison_line": self.poison_line,
            "pair": self.pair,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Stream":
        return cls(
            stream_id=d["stream_id"],
            bucket=d["bucket"],
            tenant_id=d["tenant_id"],
            account=d["account"],
            product=d.get("product"),
            price=d.get("price"),
            seller=d.get("seller"),
            messages=[Message.from_dict(m) for m in d.get("messages", [])],
            expected_text=d.get("expected_text", ""),
            expected_facts=d.get("expected_facts", []),
            poison_line=d.get("poison_line"),
            pair=d.get("pair"),
        )


DEFAULT_JSONL = Path("data/streams.jsonl")


def load_streams(path: str | Path = DEFAULT_JSONL) -> list[Stream]:
    """Read all streams from a JSONL file."""
    path = Path(path)
    streams: list[Stream] = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                streams.append(Stream.from_dict(json.loads(line)))
    return streams


def iter_streams(path: str | Path = DEFAULT_JSONL) -> Iterator[Stream]:
    """Stream them one at a time without holding all in memory."""
    path = Path(path)
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield Stream.from_dict(json.loads(line))


def write_streams(streams: Iterable[Stream], path: str | Path = DEFAULT_JSONL) -> int:
    """Write streams to JSONL, one object per line. Returns the count."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w", encoding="utf-8") as fh:
        for s in streams:
            fh.write(json.dumps(s.to_dict(), ensure_ascii=False) + "\n")
            n += 1
    return n


def by_tenant(streams: Iterable[Stream]) -> dict[str, list[Stream]]:
    out: dict[str, list[Stream]] = {}
    for s in streams:
        out.setdefault(s.tenant_id, []).append(s)
    return out


def by_bucket(streams: Iterable[Stream]) -> dict[str, list[Stream]]:
    out: dict[str, list[Stream]] = {}
    for s in streams:
        out.setdefault(s.bucket, []).append(s)
    return out


if __name__ == "__main__":
    # Smoke summary of whatever has been compiled.
    streams = load_streams()
    print(f"{len(streams)} streams loaded from {DEFAULT_JSONL}\n")
    for bucket, group in by_bucket(streams).items():
        ids = ", ".join(s.stream_id for s in group)
        print(f"  {bucket:20s} {len(group):2d}  [{ids}]")
    poisons = [s for s in streams if s.poison_line]
    print(f"\n  streams with a poison line: {len(poisons)}  [{', '.join(s.stream_id for s in poisons)}]")
    queries = sum(len(s.queries) for s in streams)
    print(f"  seller_query (Job 2) messages: {queries}")
