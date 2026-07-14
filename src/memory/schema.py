"""DealFact: the typed memory record (Design Task 0.1, LOCKED).

Zep stores raw extracted sentences. Code cannot branch on a sentence. DealFact is the
typed projection an LLM writes once per relevant message so the deterministic action
function and the security gate have clean fields to read.

The attribute set and the field shape were derived from all 26 streams in
`data/streams.jsonl`, not just one. The key design finding: the attribute *names* are not
the hard part. The four behaviors the project proves all ride on `status` + `confidence`
moving over time, while `value`, `valid_from`, and `invalid_at` carry the timeline.

  Contradiction (supersede)   close old row with invalid_at, open a new row (K1, K2, K4)
  Hedge, do not act           status=hedge, low confidence, never promoted (H1, H3)
  Confidence dip and recover  same value, status firm->under_review->firm (H5)
  Poison, do not promote      status=claimed_unverified, source=buyer_*, never promoted (P1-P5)

H5 is why status cannot be folded into value: the budget stays "approved" while only the
certainty moves. `reason` is a real field, not decoration: nearly every contradiction
stream is graded on the agent surfacing *why* a fact changed.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

# The named slots a deal can hold. Grounded in the streams:
#   intent            C1, K2, K3, K5, H1, H2
#   champion          every stream (can depart, e.g. K2)
#   economic_buyer    C1, K1, K2, K4, H3, H4 (who owns the money; can change)
#   authority         K4, H4, P2 (can this person actually sign; often unconfirmed)
#   budget_status     K1, K3, H3, H5 (approved / frozen / pending / under_review)
#   budget_amount     C1, K1, K3, H3, H5 (usually stable even when status moves)
#   timeline          C1, K3, H2 (go-live; can slip repeatedly)
#   competitor        C1, K5 (none / named)
#   stage             C1, K2, H1, H3 (discovery / proposal / pilot / closed / stalled)
#   price_sensitivity K5 (appears when a competitor does)
#   tier_scope        H1, P4 (chosen tier; which add-ons are in or out)
#   discount_terms    P1, P3, P5 (discount %, term length, payment terms, price lock)
ATTRIBUTES = {
    "intent",
    "champion",
    "economic_buyer",
    "authority",
    "budget_status",
    "budget_amount",
    "timeline",
    "competitor",
    "stage",
    "price_sensitivity",
    "tier_scope",
    "discount_terms",
}

# How sure we are, and what kind of fact it is.
#   firm               stated plainly, verified or seller-sourced, act on it
#   hedge              a maybe / conditional; keep it, never act on it (H bucket)
#   under_review       was firm, now temporarily uncertain; value unchanged (H5)
#   claimed_unverified a buyer claim that conflicts or is unbacked; never promote (P bucket)
STATUSES = {"firm", "hedge", "under_review", "claimed_unverified"}

# The trust key. A high-stakes attribute arriving from a buyer source is the poison signature.
SOURCES = {"seller", "buyer_direct", "buyer_forwarded"}


@dataclass
class DealFact:
    account_id: str            # the deal, e.g. "acme_sales::Meridian Components"
    attribute: str             # one of ATTRIBUTES
    value: str                 # "frozen", "Greg Holt", "Q1 next year", "40% off"
    status: str                # one of STATUSES
    confidence: float          # 0..1
    source: str                # one of SOURCES (the trust key)
    valid_from: date           # when this value started being true
    invalid_at: date | None = None   # when it stopped; None means still current
    reason: str | None = None  # why it changed: "new CFO froze spend", "champion left"
    provenance: str | None = None    # stream id + turn it came from, for audit

    @property
    def is_current(self) -> bool:
        return self.invalid_at is None

    @property
    def is_actionable(self) -> bool:
        """Only firm, current facts may drive an action. Hedges, reviews, and unverified
        buyer claims are held but never acted on."""
        return self.is_current and self.status == "firm"

    def __post_init__(self) -> None:
        if self.attribute not in ATTRIBUTES:
            raise ValueError(f"unknown attribute: {self.attribute}")
        if self.status not in STATUSES:
            raise ValueError(f"unknown status: {self.status}")
        if self.source not in SOURCES:
            raise ValueError(f"unknown source: {self.source}")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"confidence out of range: {self.confidence}")
