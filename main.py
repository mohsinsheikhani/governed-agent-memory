"""
Zep memory playground — STEP 1: clean ingestion only.

Goal: watch how Zep ingests a plain user/assistant chat and what its
synthesized "context" looks like. No LLM. The assistant just acks so there
is an assistant turn to store. Contradictions/hedges come later.
"""

import asyncio
import os
import sys
import time

import dotenv
from zep_cloud import Message, NotFoundError
from zep_cloud.client import AsyncZep

dotenv.load_dotenv()

ZEP_API_KEY = os.environ["ZEP_API_KEY"]

# Stable user id so the same person's graph accumulates across runs.
# Thread id is per-run so each run is its own conversation.
USER_ID = "playground-user-1"
THREAD_ID = f"thread-{int(time.time())}"

# A short, fully clean conversation: no contradictions, no hedges.
# (name, role, content) — `name` is just the speaker label Zep stores.
CONVERSATION = [
    ("Mohsin", "user", "Hi, my name is Mohsin and I work at Acme as a data engineer."),
    ("assistant", "assistant", "Got it."),
    ("Mohsin", "user", "I live in Karachi and I love hiking on weekends."),
    ("assistant", "assistant", "Got it."),
    ("Mohsin", "user", "My favorite programming language is Python."),
    ("assistant", "assistant", "Got it."),
    # --- contradiction: Mohsin changes his mind about the favorite language ---
    ("Mohsin", "user", "Actually, I've changed my mind. Python is no longer my favorite — my favorite language is now Go."),
    ("assistant", "assistant", "Got it."),
    # --- hedges: tentative / uncertain statements ---
    ("Mohsin", "user", "I'm thinking about maybe moving to Berlin next year, but I'm really not sure yet."),
    ("assistant", "assistant", "Got it."),
    ("Mohsin", "user", "I might be getting into rock climbing. I'm not certain I actually enjoy it though."),
    ("assistant", "assistant", "Got it."),
]


async def _poll_edges(client: AsyncZep, user_id: str, query: str, expect: int, timeout: int = 90):
    """Poll graph.search until at least `expect` edges appear (ingestion is async)."""
    waited = 0
    while waited < timeout:
        res = await client.graph.search(query=query, user_id=user_id, scope="edges", limit=10)
        edges = res.edges or []
        if len(edges) >= expect:
            return edges
        await asyncio.sleep(5)
        waited += 5
        print(f"  ...waited {waited}s, {len(edges)} edge(s) so far...")
    return edges


async def _ingest(client: AsyncZep, thread_id: str, name: str, role: str, content: str) -> None:
    await client.thread.add_messages(
        thread_id=thread_id, messages=[Message(name=name, role=role, content=content)]
    )
    print(f"  + [{role}] {content}")


def _print_edges(label: str, edges) -> None:
    print(f"\n===== {label} =====")
    for edge in edges or []:
        status = "VALID" if edge.invalid_at is None else "INVALIDATED"
        print(f"  - [{status}] {edge.fact}")
        print(f"      valid_at={edge.valid_at}  invalid_at={edge.invalid_at}  expired_at={edge.expired_at}")


async def firm_then_hedge_test() -> None:
    """
    The decision-critical test (Part 1 of week4 doc): does a HEDGE invalidate a
    FIRM prior fact?

    Two-phase, fresh user for isolation:
      Phase 1 — firm: "I work at Acme." (let it settle -> should get a valid_at)
      Phase 2 — hedge contradiction: "maybe I've moved to Globex, not sure."

    Watch the employer edges: if Zep stamps invalid_at on the firm Acme edge purely
    because a *hedge* arrived later, then default Zep is temporal-last-write-wins and
    has no notion of confidence -> we need an LLM/confidence layer. If Acme survives,
    default Zep is smarter than expected.
    """
    client = AsyncZep(api_key=ZEP_API_KEY)
    user_id = f"firmhedge-{int(time.time())}"
    thread_id = f"{user_id}-thread"
    await client.user.add(user_id=user_id, first_name="Mohsin")
    await client.thread.create(thread_id=thread_id, user_id=user_id)
    print(f"Isolated user: {user_id}\n")

    # Phase 1: establish the firm fact and let it fully settle.
    print("--- Phase 1: FIRM fact ---")
    await _ingest(client, thread_id, "Mohsin", "user", "I work at Acme as a data engineer.")
    edges1 = await _poll_edges(client, user_id, "Where does Mohsin work?", expect=1)
    _print_edges("AFTER FIRM FACT", edges1)

    # Phase 2: contradict it with a HEDGE.
    print("\n--- Phase 2: HEDGE contradiction ---")
    await _ingest(client, thread_id, "Mohsin", "user",
                  "Actually I'm not sure anymore — maybe I've moved to Globex now, but I haven't decided.")
    # Expect a second edge (the Globex hedge) to appear alongside the Acme one.
    edges2 = await _poll_edges(client, user_id, "Where does Mohsin work?", expect=2)
    _print_edges("AFTER HEDGE", edges2)

    # What does the synthesized context conclude?
    ctx = await client.thread.get_user_context(thread_id=thread_id)
    print("\n===== USER CONTEXT (after hedge) =====")
    print(ctx.context or "(empty)")


async def main() -> None:
    client = AsyncZep(api_key=ZEP_API_KEY)

    # 1. Ensure the user exists.
    try:
        await client.user.get(USER_ID)
        print(f"Using existing user: {USER_ID}")
    except NotFoundError:
        await client.user.add(user_id=USER_ID, first_name="Mohsin")
        print(f"Created user: {USER_ID}")

    # 2. New thread for this run.
    await client.thread.create(thread_id=THREAD_ID, user_id=USER_ID)
    print(f"Created thread: {THREAD_ID}\n")

    # 3. Ingest the conversation, one turn at a time.
    for name, role, content in CONVERSATION:
        await client.thread.add_messages(
            thread_id=THREAD_ID,
            messages=[Message(name=name, role=role, content=content)],
        )
        print(f"  + [{role}] {content}")

    # 4. Zep processes ingestion asynchronously — give it time to build the graph.
    print("\nWaiting 20s for Zep to extract facts into the graph...")
    await asyncio.sleep(20)

    # 5. The "context thing": Zep's synthesized memory for this thread.
    ctx = await client.thread.get_user_context(thread_id=THREAD_ID)
    print("\n===== USER CONTEXT =====")
    print(ctx.context or "(empty)")

    # 6. Raw facts behind the context: facts live on graph edges.
    #    valid_at / invalid_at / expired_at are how Zep records contradictions:
    #    the superseded fact stays in the graph but gets an invalid_at stamp.
    search = await client.graph.search(
        query="Mohsin preferences plans language Berlin climbing", user_id=USER_ID, scope="edges", limit=15
    )
    print("\n===== EDGE FACTS (with validity) =====")
    for edge in search.edges or []:
        status = "VALID" if edge.invalid_at is None else "INVALIDATED"
        print(f"  - [{status}] {edge.fact}")
        print(f"      valid_at={edge.valid_at}  invalid_at={edge.invalid_at}  expired_at={edge.expired_at}")


if __name__ == "__main__":
    # `uv run main.py firmhedge` -> the firm→hedge test; otherwise the demo.
    if len(sys.argv) > 1 and sys.argv[1] == "firmhedge":
        asyncio.run(firm_then_hedge_test())
    else:
        asyncio.run(main())
