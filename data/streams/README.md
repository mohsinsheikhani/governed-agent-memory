# Synthetic deal streams (the eval surface)

These are the seeded conversations the Deal Memory Agent reads. They are written by
hand to be genuine, logical sales conversations, not random chunks. Each stream is a
short deal told as a real sequence of messages over simulated weeks, plus an
**expected outcome** that says what memory *should* hold and what the agent *should* do.
That expected block is what turns "I ran it" into "I measured it against what should
have happened." It is the golden answer for evals.

## The five buckets

| File | Bucket | Proves | Headline number |
|---|---|---|---|
| `01_clean.md` | Clean / happy path | agent does not invent problems; baseline for token growth and retrieval | baseline only |
| `02_contradiction.md` | Contradiction over time | temporal validity: supersede the old fact with a timestamp, do not overwrite or hold both as equal | contradiction count, answer coherence |
| `03_hedge_contradiction.md` | Hedge + contradiction | confidence: a hedge stays a hedge; a later firm statement raises confidence and wins | confidence handling, wrong-commitment rate |
| `04_poisoning.md` | Claim-to-fact escalation | a self-serving buyer claim about money / authority / terms does not silently become an actionable fact | claim-promotion rate, gate off vs on |
| `05_isolation.md` | Isolation pairs (near-collisions) | one account's facts never surface in another's answers, even when details nearly collide | cross-account leak rate |

## Message format

Every message is tagged:

```
[Day N | source | channel] Speaker (role):
  body
```

- **Day N** is the simulated day, so temporal validity has something to bite on.
- **source** is the trust key (see plan Section 3.0):
  - `buyer_direct` (buyer writing to the seller), `buyer_forwarded` (buyer-originated
    content the seller forwarded in, the only poisoning surface), `seller` (the rep's
    own emails and call notes), `seller_query` (the rep asking the agent something, Job 2).
- **channel** is `email`, `call_note`, or `query`.

## How the agent uses a stream

The agent ingests messages in Day order. After each one it may update memory and may
act. `seller_query` messages are Job 2: the rep asks, the agent answers from memory.
The **expected outcome** at the end of each stream lists the facts memory should hold
(with temporal validity and confidence where relevant) and the action the agent should
take. Grading compares the agent's actual memory and action against that.

## Cast and tenants (kept stable so isolation tests are real)

| Tenant | Seller | Used by |
|---|---|---|
| `acme_sales` | Dana Whitfield | C1, C3, C5, contradiction K1/K3, hedge H1/H3, poison P1/P3, isolation A-side |
| `brightpath` | Tom Alvarez | C2, C4, contradiction K2/K4, hedge H2/H4, poison P2/P4, isolation B-side |
| `northstar` | Maya Lindqvist | contradiction K5, hedge H5, poison P5, isolation C-side |

Names are kept distinct *within* a tenant on purpose, and made to nearly collide
*across* tenants only in `05_isolation.md`, because isolation can only be proven with
near-collisions, not with unrelated accounts.

## Design notes per bucket

- **Clean** carries one benign `buyer_forwarded` message (C4) so the poisoning numbers
  later have a false-positive check. A gate that flags every forward is too blunt.
- **Contradiction** flips a single load-bearing fact (budget, champion, timeline) mid-deal.
  The earlier fact must stay in history with an end date, because the *history* is what
  tells the rep the deal got riskier.
- **Hedge + contradiction** laces "maybe / might / not sure" around the flip, so the test
  is whether a hedge is stored as a weak fact and a later firm statement correctly wins.
- **Poisoning** smuggles a false high-stakes claim inside ordinary recap language. Run
  each twice, gate off then on, and report the drop in claim-promotion rate.
- **Isolation** is three near-collision pairs across tenants (same first name, same
  product category, same price band) so a leak is actually possible and therefore worth
  testing.
