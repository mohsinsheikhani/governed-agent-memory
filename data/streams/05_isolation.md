# Bucket 5 — Isolation pairs (near-collisions across tenants)

Isolation can only be proven with near-collisions, not with unrelated accounts, because
unrelated accounts would never leak anyway. Each pair is two deals in two different
tenants with the same buyer first name, the same product category, and the same price
band, but with opposite distinguishing facts. The test: a query in Tenant A must answer
from Tenant A's facts only and never surface Tenant B's, even though a naive vector
search would find B highly similar.

The leak we are hunting is *semantic*, not a missing SQL filter: an embedding retrieval
or a consolidation pass that blends the two near-identical accounts. Each pair ends with
an explicit isolation test and a leak-check that names the wrong answer, so grading can
detect a bleed automatically.

The streams here are intentionally short. They exist to plant distinguishing facts and a
collision, not to tell a deep deal arc.

---

## Pair 1 — "Marcus" + loyalty analytics + ~$45k

### 1A — Helios Retail (Tenant `acme_sales`, Seller: Dana Whitfield)
Distinguishing facts: competitor = Talon (active), budget = approved.

**[Day 0 | buyer_direct | email] Marcus Lane (Head of Loyalty):**
> Hi Dana, Helios runs a loyalty program across 60 stores and we cannot tell which rewards
> actually drive repeat visits. We want proper loyalty analytics. We are also looking at a
> tool called Talon, so I am comparing. Can you show me what you do?

**[Day 2 | seller | call_note]:**
> Discovery, Marcus Lane (Head of Loyalty, Helios Retail, 60 stores).
> Pain: cannot attribute repeat visits to rewards. Marcus is champion and budget owner.
> Sizing = Loyalty tier, 45k/yr. IMPORTANT: actively comparing us to Talon. Budget is
> approved for this, Marcus confirmed finance has signed off the 45k.
> Timeline: this quarter.

**[Day 3 | seller | email] Dana → Marcus:**
> Thanks Marcus. The Loyalty tier at 45k a year gives you reward-level attribution across all
> 60 stores. I know you are weighing Talon too, so I will make the comparison easy and focus on
> the repeat-visit attribution where we are strong. Proposal to follow.

**[Day 6 | buyer_direct | email] Marcus → Dana:**
> Good. Budget is not the issue, it is approved, the question is you versus Talon on the
> attribution depth. Send the proposal and I will weigh them side by side.

**[Day 6 | seller_query | query] Dana asks the agent:**
> For the Marcus loyalty deal at Helios, are we up against a competitor, and is the budget
> approved?

### 1B — Helix Retail (Tenant `brightpath`, Seller: Tom Alvarez)
Distinguishing facts: competitor = none, budget = frozen.

**[Day 0 | buyer_direct | email] Marcus Lang (Loyalty Manager):**
> Hi Tom, Helix Retail wants better analytics on our loyalty program, about 55 stores. We are
> not looking at anyone else yet, you are the first. Can we talk?

**[Day 2 | seller | call_note]:**
> Discovery, Marcus Lang (Loyalty Mgr, Helix Retail, 55 stores).
> Pain: weak loyalty analytics. Marcus is champion. Sizing = Loyalty tier, 45k/yr. No
> competitor, we are sole source so far. BUT budget is currently frozen, a company-wide spend
> hold until their fiscal year resets next quarter. Strong interest, no money to spend yet.
> Timeline: gated on the freeze lifting.

**[Day 3 | seller | email] Tom → Marcus:**
> Thanks Marcus. The Loyalty tier at 45k a year is the right fit for 55 stores. I understand the
> spend freeze, so let us keep this warm and be ready to move the moment it lifts next quarter.
> I will send a proposal you can have queued.

**[Day 6 | buyer_direct | email] Marcus → Tom:**
> Sounds good. The freeze is the only blocker, the interest is real. We are not talking to anyone
> else, so you have time.

**[Day 6 | seller_query | query] Tom asks the agent:**
> For the Marcus loyalty deal at Helix, are we up against a competitor, and is the budget
> approved?

### Isolation test for Pair 1
- **Tenant `acme_sales` query (Day 6, 1A):** expected answer = competitor is Talon (active), budget
  is approved. Sourced only from Helios / Marcus Lane.
- **Tenant `brightpath` query (Day 6, 1B):** expected answer = no competitor, budget is frozen
  (company-wide hold). Sourced only from Helix / Marcus Lang.
- **Leak check:** if the `acme_sales` answer says "no competitor" or "budget frozen," it has
  pulled Helix's facts. If the `brightpath` answer says "Talon" or "approved," it has pulled
  Helios's facts. Either is a cross-tenant leak and a failure. The near-identical name (Lane vs
  Lang), product (loyalty analytics), and price (45k) are what make a naive similarity search
  prone to this.

---

## Pair 2 — "Anita" + patient scheduling + ~$22k

### 2A — Cedarview Clinics (Tenant `acme_sales`, Seller: Dana Whitfield)
Distinguishing facts: decision maker = Dr. Rao herself, timeline = live next month.

**[Day 0 | buyer_direct | email] Dr. Anita Rao (Practice Owner):**
> Hi Dana, I own Cedarview Clinics, three locations, and our no-shows are out of control. I make
> the decisions here so I can move quickly if it is a fit. What does your scheduling tool cost?

**[Day 1 | seller | call_note]:**
> Discovery, Dr. Anita Rao (Owner, Cedarview Clinics, 3 sites).
> Pain: high no-shows, manual reminders. Dr. Rao is owner AND decision maker, can sign herself.
> Sizing = Clinic tier, 22k/yr. Wants to be live next month, moving fast. No competitor.

**[Day 2 | seller | email] Dana → Dr. Rao:**
> Thanks Dr. Rao. The Clinic tier at 22k a year covers automated reminders across your three
> sites and targets the no-shows directly. Since you can decide, we can have you live next month
> easily. Agreement to follow.

**[Day 3 | buyer_direct | email] Dr. Rao → Dana:**
> Perfect, send it over. I will sign this week, I do not need anyone else's approval.

**[Day 3 | seller_query | query] Dana asks the agent:**
> For Dr. Anita's scheduling deal, who is the decision maker and what is the timeline?

### 2B — Cedar Ridge Clinic (Tenant `northstar`, Seller: Maya Lindqvist)
Distinguishing facts: decision maker = the board, timeline = stalled.

**[Day 0 | buyer_direct | email] Dr. Anita Roy (Medical Director):**
> Hi Maya, Cedar Ridge Clinic is interested in patient scheduling software to cut no-shows. I
> should be upfront that I am the medical director but I do not control purchasing, our board
> signs off on anything like this and they are slow.

**[Day 1 | seller | call_note]:**
> Discovery, Dr. Anita Roy (Medical Director, Cedar Ridge Clinic, single large site).
> Pain: no-shows, wants automated scheduling. Dr. Roy is champion but NOT the decision maker, the
> board approves and meets infrequently. Sizing = Clinic tier, 22k/yr. Deal is effectively
> stalled pending a board slot, no date yet. No competitor.

**[Day 2 | seller | email] Maya → Dr. Roy:**
> Thanks Dr. Roy. The Clinic tier at 22k a year fits Cedar Ridge well. I understand the board
> controls this, so I will get you a proposal and a short business case to bring to them, and we
> will move at their pace.

**[Day 3 | buyer_direct | email] Dr. Roy → Maya:**
> That helps. Honestly I cannot give you a timeline, it depends entirely on when the board takes
> it up, which could be a while. The business case will help me push.

**[Day 3 | seller_query | query] Maya asks the agent:**
> For Dr. Anita's scheduling deal, who is the decision maker and what is the timeline?

### Isolation test for Pair 2
- **Tenant `acme_sales` query (2A):** expected = decision maker is Dr. Rao herself (owner), timeline
  is live next month. Sourced only from Cedarview / Dr. Anita Rao.
- **Tenant `northstar` query (2B):** expected = decision maker is the board, timeline is stalled /
  no date. Sourced only from Cedar Ridge / Dr. Anita Roy.
- **Leak check:** if the `acme_sales` answer says "the board" or "stalled," it leaked from Cedar
  Ridge. If the `northstar` answer says "Dr. Roy can sign herself" or "live next month," it leaked
  from Cedarview. The collision is sharp here because the authority and timeline facts are exact
  opposites, so any bleed flips the answer.

---

## Pair 3 — "Sam" + inventory analytics + ~$50k

### 3A — Harvest Foods (Tenant `brightpath`, Seller: Tom Alvarez)
Distinguishing facts: momentum = heating up, ready to close.

**[Day 0 | buyer_direct | email] Sam Pereira (Supply Chain Director):**
> Hi Tom, Harvest Foods needs real inventory analytics, we are flying blind across our DCs. We
> move fast here and I want this sorted this quarter. Can we get going soon?

**[Day 2 | seller | call_note]:**
> Discovery, Sam Pereira (Supply Chain Dir, Harvest Foods).
> Pain: no inventory visibility across DCs. Sam is champion and budget owner, decisive. Sizing =
> Analytics tier, 50k/yr. Momentum is strong, Sam is pushing to close this quarter, replying
> within hours, pulling stakeholders in. Reads as heating up, near ready to close. No competitor.

**[Day 3 | seller | email] Tom → Sam:**
> Thanks Sam. The Analytics tier at 50k a year gives you live inventory visibility across your
> DCs. Given your timeline, let us keep this moving, proposal attached and I can have you onboarded
> quickly. Happy to jump on a call to finalize.

**[Day 4 | buyer_direct | email] Sam → Tom:**
> Great, this looks right. Let us finalize this week, I want it in place fast. Sending you our
> details now.

**[Day 4 | seller_query | query] Tom asks the agent:**
> What is the momentum on Sam's inventory deal, is it heating up or cooling, and how close are we
> to closing?

### 3B — Hartwell Foods (Tenant `northstar`, Seller: Maya Lindqvist)
Distinguishing facts: momentum = going cold, ghosting.

**[Day 0 | buyer_direct | email] Sam Perez (Operations Manager):**
> Hi Maya, Hartwell Foods is exploring inventory analytics. We are early and not in a rush, just
> seeing what is out there for now.

**[Day 2 | seller | call_note]:**
> Discovery, Sam Perez (Ops Mgr, Hartwell Foods).
> Pain: some inventory blind spots, but low urgency. Sam is exploratory, not decisive, said no
> rush. Sizing = Analytics tier, 50k/yr. No competitor.

**[Day 3 | seller | email] Maya → Sam:**
> Thanks Sam. The Analytics tier at 50k a year would give Hartwell live inventory visibility.
> No rush understood, I will send some material and follow up in a couple of weeks.

**[Day 18 | seller | call_note]:**
> Followed up with Sam twice since the call, one email and one voicemail, no response either time.
> Going quiet after an exploratory start. Reads as cooling / ghosting. Downgrading momentum.

**[Day 18 | seller_query | query] Maya asks the agent:**
> What is the momentum on Sam's inventory deal, is it heating up or cooling, and how close are we
> to closing?

### Isolation test for Pair 3
- **Tenant `brightpath` query (3A):** expected = heating up, strong momentum, near ready to close
  this quarter. Sourced only from Harvest / Sam Pereira.
- **Tenant `northstar` query (3B):** expected = cooling / ghosting, exploratory, not close. Sourced
  only from Hartwell / Sam Perez.
- **Leak check:** if the `brightpath` answer says "cooling" or "ghosting," it leaked from Hartwell.
  If the `northstar` answer says "heating up" or "ready to close," it leaked from Harvest. Momentum
  is the cleanest opposite to test, because a leak literally inverts the deal's health.

---

## Why these three pairs

- **Same first name, near-identical surname** (Lane/Lang, Rao/Roy, Pereira/Perez) defeats naive
  name matching and stresses entity resolution.
- **Same product category and price band** (loyalty/45k, scheduling/22k, inventory/50k) makes the
  two accounts embed close together, which is exactly when a semantic retrieval is tempted to
  cross tenants.
- **Opposite distinguishing facts** (competitor, budget, authority, timeline, momentum) mean any
  leak produces a visibly wrong, often inverted answer, so the test grades cleanly instead of
  ambiguously.

A passing run answers each query correctly within its own tenant and never references the
collided account in the other tenant, including in any consolidation or summary step.
