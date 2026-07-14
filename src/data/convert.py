"""Compile the markdown deal streams in `data/streams/*.md` into `data/streams.jsonl`.

The markdown is the human source of truth. This parser is deliberately tolerant of the
two header styles in use:

  - standard streams:   `## C1 -- Account · Product · Price`  then a `Tenant: ... Seller: ...` line
  - isolation streams:  `### 1A -- Account (Tenant `x`, Seller: Y)`  under a `## Pair N` container

Message blocks look like:

    **[Day 0 | buyer_direct | email] Priya Nair (HR Director):**
    > body line
    > body line

Poison streams wrap a false claim in `>>> POISON >>> ... <<< POISON <<<`. The markers are
stripped from the body the agent sees and the inner text is recorded as `poison_line`.

Run:  python -m src.data.convert        (from the repo root)
  or: python src/data/convert.py
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Allow running either as a module (`python -m src.data.convert`) or as a script.
try:
    from .streams import Message, Stream, write_streams
except ImportError:  # pragma: no cover - script invocation
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from src.data.streams import Message, Stream, write_streams

MSG_RE = re.compile(
    r"^\*\*\[Day\s*(\d+)\s*\|\s*(\w+)\s*\|\s*(\w+)\]\s*(.*?):\*\*\s*$"
)
STD_ID_RE = re.compile(r"^[CKHP]\d+$")
ISO_ID_RE = re.compile(r"^\d+[AB]$")
TENANT_RE = re.compile(r"Tenant:?\s*`([^`]+)`")
SELLER_RE = re.compile(r"Seller:\s*([^·)\n]+)")
POISON_RE = re.compile(r">>> POISON >>>(.*?)<<< POISON <<<", re.S)
SPEAKER_ROLE_RE = re.compile(r"^(.*?)\s*\((.*)\)\s*$")


def _bucket_from_filename(path: Path) -> str:
    # 01_clean -> clean, 03_hedge_contradiction -> hedge_contradiction
    stem = path.stem
    return stem.split("_", 1)[1] if "_" in stem else stem


def _split_speaker(raw: str) -> tuple[str | None, str | None]:
    raw = raw.strip()
    if not raw:
        return None, None
    m = SPEAKER_ROLE_RE.match(raw)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return raw, None


def _clean_body(lines: list[str]) -> tuple[str, str | None]:
    """Join blockquote lines, strip the `> ` prefix, and pull out a poison line."""
    stripped = [re.sub(r"^>\s?", "", ln) for ln in lines]
    text = "\n".join(stripped).strip()
    poison = None
    m = POISON_RE.search(text)
    if m:
        poison = m.group(1).strip()
    # Remove only the markers, keep the real text between them (the agent must see it).
    text = re.sub(r">>> POISON >>>\s?", "", text)
    text = re.sub(r"\s?<<< POISON <<<", "", text)
    return text.strip(), poison


def parse_file(path: Path) -> list[Stream]:
    bucket = _bucket_from_filename(path)
    streams: list[Stream] = []
    cur: Stream | None = None
    cur_pair: str | None = None

    mode: str | None = None          # 'body' | 'expected' | 'isotest' | None
    body_lines: list[str] = []
    pending: dict | None = None      # message header awaiting its body
    exp_lines: list[str] = []
    iso_lines: list[str] = []
    iso_pair: str | None = None
    iso_tests: dict[str, str] = {}   # pair number -> isolation test text

    def finalize_message() -> None:
        nonlocal pending, body_lines
        if pending is None or cur is None:
            pending, body_lines = None, []
            return
        body, poison = _clean_body(body_lines)
        speaker, role = _split_speaker(pending["speaker_raw"])
        cur.messages.append(
            Message(
                turn=len(cur.messages) + 1,
                day=pending["day"],
                source=pending["source"],
                channel=pending["channel"],
                speaker=speaker,
                role=role,
                body=body,
            )
        )
        if poison and cur.poison_line is None:
            cur.poison_line = poison
        pending, body_lines = None, []

    def finalize_expected() -> None:
        nonlocal exp_lines
        if cur is not None and exp_lines:
            cur.expected_text = "\n".join(exp_lines).strip()
        exp_lines = []

    def finalize_isotest() -> None:
        nonlocal iso_lines, iso_pair
        if iso_pair is not None and iso_lines:
            iso_tests[iso_pair] = "\n".join(iso_lines).strip()
        iso_lines, iso_pair = [], None

    def close_modes() -> None:
        finalize_message()
        finalize_expected()
        finalize_isotest()

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()

        # 1) message header
        m = MSG_RE.match(line)
        if m:
            finalize_message()
            mode = "body"
            pending = {
                "day": int(m.group(1)),
                "source": m.group(2),
                "channel": m.group(3),
                "speaker_raw": m.group(4),
            }
            body_lines = []
            continue

        # 2) any markdown header
        if line.startswith("#"):
            close_modes()
            mode = None
            content = line.lstrip("#").strip()
            hid = content.split(" — ")[0].split(" -- ")[0].strip()
            rest = content[len(hid):].lstrip(" —-").strip()

            if STD_ID_RE.match(hid):
                cur = Stream(
                    stream_id=hid, bucket=bucket, tenant_id="",
                    account="", product=None, price=None, seller=None, pair=None,
                )
                parts = [p.strip() for p in rest.split(" · ")]
                if parts:
                    cur.account = parts[0]
                if len(parts) > 1:
                    cur.product = parts[1]
                if len(parts) > 2:
                    cur.price = parts[2]
                streams.append(cur)
            elif ISO_ID_RE.match(hid):
                account = rest.split(" (")[0].strip()
                tm = TENANT_RE.search(rest)
                sm = SELLER_RE.search(rest)
                cur = Stream(
                    stream_id=hid, bucket=bucket,
                    tenant_id=tm.group(1) if tm else "",
                    account=account, product=None, price=None,
                    seller=sm.group(1).strip() if sm else None,
                    pair=cur_pair,
                )
                streams.append(cur)
            elif content.startswith("Pair"):
                pm = re.search(r"Pair\s*(\d+)", content)
                cur_pair = pm.group(1) if pm else None
                cur = None
            elif "Isolation test for Pair" in content:
                pm = re.search(r"Pair\s*(\d+)", content)
                iso_pair = pm.group(1) if pm else None
                iso_lines = []
                mode = "isotest"
            elif content.lower().startswith("expected outcome"):
                exp_lines = []
                mode = "expected"
            # any other header (intro sections etc.) leaves mode None
            continue

        # 3) horizontal rule ends a stream's trailing block
        if line.startswith("---"):
            close_modes()
            mode = None
            continue

        # 4) content lines, routed by mode
        if mode == "body":
            if line.startswith(">"):
                body_lines.append(line)
                continue
            # body ended without a blank-line marker; finalize and reprocess this line below
            finalize_message()
            mode = None

        if mode == "expected":
            exp_lines.append(line)
            continue
        if mode == "isotest":
            iso_lines.append(line)
            continue

        # 5) the `Tenant: ... Seller: ...` metadata line for standard streams
        if cur is not None and not cur.tenant_id and "Tenant" in line:
            tm = TENANT_RE.search(line)
            sm = SELLER_RE.search(line)
            if tm:
                cur.tenant_id = tm.group(1)
            if sm:
                cur.seller = sm.group(1).strip()

    close_modes()

    # Attach each pair's isolation-test block to both of its streams as the expected answer.
    for s in streams:
        if s.pair and not s.expected_text and s.pair in iso_tests:
            s.expected_text = iso_tests[s.pair]

    return streams


def main() -> None:
    ap = argparse.ArgumentParser(description="Compile data/streams/*.md into JSONL.")
    ap.add_argument("--src", default="data/streams", help="directory of markdown stream files")
    ap.add_argument("--out", default="data/streams.jsonl", help="output JSONL path")
    args = ap.parse_args()

    src_dir = Path(args.src)
    files = sorted(p for p in src_dir.glob("*.md") if p.name.lower() != "readme.md")
    if not files:
        ap.error(f"no markdown stream files found in {src_dir}")

    all_streams: list[Stream] = []
    for f in files:
        parsed = parse_file(f)
        all_streams.extend(parsed)
        print(f"  {f.name:28s} -> {len(parsed):2d} streams")

    n = write_streams(all_streams, args.out)

    # Basic validation so a malformed parse is loud, not silent.
    problems = []
    for s in all_streams:
        if not s.tenant_id:
            problems.append(f"{s.stream_id}: missing tenant_id")
        if not s.messages:
            problems.append(f"{s.stream_id}: no messages")
        if s.bucket == "poisoning" and s.poison_line is None:
            problems.append(f"{s.stream_id}: poisoning stream has no poison_line")
    print(f"\nwrote {n} streams to {args.out}")
    if problems:
        print("VALIDATION WARNINGS:")
        for p in problems:
            print(f"  ! {p}")
    else:
        print("validation: all streams have tenant, messages, and (where expected) a poison line")


if __name__ == "__main__":
    main()
