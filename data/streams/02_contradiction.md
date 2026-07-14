# Bucket 2 — Contradiction over time

Each deal starts normal, then a single load-bearing fact flips: budget, champion,
timeline, authority, or competitive position. The test is temporal validity. The agent
must supersede the old fact with an end date, not overwrite it and not hold both as
equally true, because the *history* of the change is what tells the rep the deal got
riskier.

---

## K1 — Meridian Components · quality inspection analytics · ~$54k/yr
Tenant: `acme_sales` · Seller: Dana Whitfield · Flip: budget approved, then frozen, then a hedged maybe
*The classic. Budget is firm in month one, frozen in month two under a new CFO, tentatively unfrozen for next quarter in month three.*

**[Day 0 | buyer_direct | email] Tomás Rivera (Quality Director):**
> Hi Dana, we make precision components for automotive suppliers and our inspection data
> lives in three disconnected systems. When a customer raises a quality issue it takes us
> days to trace it back through the line. I want to fix that this year. Can we talk?

**[Day 2 | seller | call_note]:**
> Discovery, Tomás Rivera (Quality Director, Meridian Components).
>
> Pain: inspection data scattered across three systems, root-cause tracing on a customer
> complaint takes 2 to 4 days, which risks their automotive contracts that demand fast
> corrective action. Tomás owns quality and is a strong champion, this is his initiative.
>
> Metric: cut trace time from days to hours, and reduce the customer complaints that
> escalate because they were slow to respond.
>
> Decision: budget sits with Helen Voss, CFO. Tomás says quality improvement is a board
> priority this year because of a near-miss with a big customer, so funding is supportive.
>
> Timeline: wants it live within the quarter.
>
> Competition: none, this is his first serious look.

**[Day 3 | seller | email] Dana → Tomás:**
> Thanks Tomás. To recap, a customer quality issue today takes you 2 to 4 days to trace
> because the data is in three places, and with automotive contracts that lag is a real
> risk. Our platform unifies the three sources and gets root-cause tracing down to hours.
> For your line count the right fit is the Plant tier at 54k a year. Worth getting Helen a
> view early given the board interest you mentioned?

**[Day 6 | buyer_direct | email] Tomás → Dana:**
> The Plant tier sounds right. I spoke with Helen and the budget is approved for this, 54k
> is within what the board earmarked for quality this year. She is comfortable, she just
> wants to sign off on the final paperwork. Let us move toward a proposal.

**[Day 8 | seller | email] Dana → Tomás:**
> Excellent, that board backing makes a real difference. Proposal attached at the Plant
> tier, 54k a year, with a target go-live inside the quarter as you wanted. Whenever Helen
> is ready to paper it we can book your configuration.

**[Day 12 | buyer_direct | email] Tomás → Dana:**
> Proposal looks good and accurate. We are lining up Helen's signature, I expect it within
> a couple of weeks. I am keen to get going.

**[Day 20 | seller | call_note]:**
> Checked in with Tomás by phone. Still positive, signature is "in the queue" with finance.
> No concerns raised. He reaffirmed go-live this quarter. Treating this as on track to close.

**[Day 45 | buyer_direct | email] Tomás → Dana:**
> Dana, I need to be straight with you because I do not want to waste your time. Helen left
> three weeks ago and we have a new CFO, Greg Holt, who has put a freeze on all new software
> spend while he does a cost review. Our project is caught in that freeze. The budget that
> was approved is effectively frozen for now. Nothing has changed about how much we need
> this, the money is just locked while Greg reviews everything. I am sorry, this is out of
> my hands at the moment.

**[Day 46 | seller | email] Dana → Tomás:**
> I appreciate you telling me directly Tomás, and I know this is not on you. So I track it
> correctly, is this a hard stop until the review finishes, or is there a path to make the
> case to Greg given the board priority and the customer risk? Happy to put together a tight
> one-page business case you could take to him whenever the timing is right.

**[Day 48 | buyer_direct | email] Tomás → Dana:**
> A one-pager would actually help, thank you. It is a freeze, not a cancellation, that is
> the honest status. Greg's review runs through the end of the quarter. I am still the
> sponsor and I still want this, I just cannot move money right now.

**[Day 75 | buyer_direct | email] Tomás → Dana:**
> Small update, and it is only a maybe so do not act on it yet. Greg's review is wrapping up
> and quality came out as a protected area, so there is a decent chance the spend unfreezes
> for Q3. I am not certain, he has not committed, but it is looking more likely than not. I
> will know for sure in a few weeks. Hold the one-pager ready.

**[Day 75 | seller_query | query] Dana asks the agent:**
> What is the real status on Meridian right now, and what should my next move be? Give me
> the history too, I want to see how it moved.

### Expected outcome
- **Memory should hold (with temporal validity):**
  - budget = approved, ~$54k, *valid Day 6 to Day 45* (source: Tomás via Helen), then
    superseded by budget = frozen, *valid from Day 45* (new CFO Greg Holt, company-wide
    software spend freeze, review through end of quarter), then a low-confidence
    budget = likely to unfreeze for Q3, *from Day 75*, marked as a hedge / not committed.
  - champion = Tomás Rivera (Quality Director), unchanged and still sponsoring.
  - economic buyer = changed: Helen Voss (departed ~Day 24) superseded by Greg Holt (new
    CFO) from ~Day 45.
  - intent = still high and unchanged; only the budget availability moved. This distinction
    matters: need is constant, funding is blocked.
  - timeline = slipped from "this quarter" to "possibly Q3."
- **Expected action:** do NOT treat the Day 75 maybe as a green light. Report the deal as
  stalled-but-alive: champion intact, need intact, money frozen by a new CFO, a credible
  but uncommitted chance of Q3 unfreeze. Recommend keeping the one-pager ready and a light
  check-in, not a push. Surface the *history* of the budget fact, including the old
  approved value with its end date, since that arc is the risk story.
- **Why this bucket:** the naive failure is to overwrite "approved" with "frozen" and lose
  the arc, or worse to read "approved" as still current. The senior behavior is supersede
  with timestamps and keep the trail, and to separate "need" (steady) from "budget"
  (changed).

---

## K2 — Vantage Retail Group · workforce scheduling · ~$40k/yr
Tenant: `brightpath` · Seller: Tom Alvarez · Flip: the champion leaves mid-deal
*Hot deal driven by one strong champion, who then departs. A lukewarm successor reassesses, and the deal cools not because the need changed but because the person carrying it is gone.*

**[Day 0 | seller | email] Tom → Derek:**
> Hi Derek, congratulations on the 30 new stores this year. Most retail ops leaders I talk
> to find their old scheduling approach breaks right around that growth point, too many
> locations, too much manual juggling, rising overtime. Worth a conversation?

**[Day 2 | buyer_direct | email] Derek Hollis (Director of Store Operations):**
> You read that right, scheduling is becoming a nightmare at our size and overtime is
> creeping up every month. I have been meaning to fix this for a while. Yes, let us talk,
> this is a priority for me personally.

**[Day 4 | seller | call_note]:**
> Discovery, Derek Hollis (Dir Store Ops, Vantage Retail, ~90 stores).
>
> Pain: manual scheduling across 90 stores, overtime up ~15% YoY, managers building rotas
> in spreadsheets. Derek is a strong, motivated champion, this is his named goal for the
> year and he says his bonus is partly tied to labor cost.
>
> Metric: cut overtime, reduce time managers spend building schedules.
>
> Decision: budget owned by Sandra Lin, VP Retail. Derek is confident he can get her behind
> it, he has her ear. 40k is within range.
>
> Timeline: wants a pilot in two regions within the quarter.
>
> Competition: none active.
>
> Next: Derek socializes internally, we scope the two-region pilot.

**[Day 5 | seller | email] Tom → Derek:**
> Great session Derek. The core is that manual scheduling cannot scale to 90 stores and it
> is showing up as 15% more overtime. The Standard tier at 40k a year covers all your
> locations and the two-region pilot we discussed is the right way to prove the overtime
> savings before a full rollout. I will draft the pilot scope.

**[Day 9 | buyer_direct | email] Derek → Tom:**
> Pilot scope looks great. I floated it with Sandra and she is open, she wants to see the
> pilot numbers before committing to the full rollout but the appetite is there. I am
> pushing to start the pilot next month. This is happening on my side.

**[Day 14 | seller | call_note]:**
> Call with Derek. Energized, walked me through which two regions he wants to pilot and
> why. Said Sandra is "as good as bought in" pending pilot results. Strong momentum, Derek
> is doing our selling internally. Feels like a clear path to close after a successful pilot.

**[Day 38 | buyer_direct | email] Derek → Tom:**
> Tom, some personal news, I have accepted a role at another company and Friday is my last
> day at Vantage. I genuinely believe in this project and I have briefed my interim
> replacement, Alan Brooks, on where we are. Alan will pick it up. I have told him the pilot
> was ready to go. Thanks for everything, I hope it lands.

**[Day 45 | seller | email] Tom → Alan:**
> Hi Alan, Derek introduced us before he left and spoke highly of the scheduling pilot you
> are inheriting. We had two regions scoped and were ready to start. I would love to get you
> up to speed and keep the momentum, do you have 20 minutes this week?

**[Day 52 | buyer_direct | email] Alan Brooks (Interim Director, Store Operations):**
> Hi Tom, thanks for reaching out and I appreciate the context. In all honesty I have walked
> into a lot at once and I am still working out my own priorities for the function. Workforce
> scheduling is on the list but I am not sure it is the first thing I want to take on while I
> am interim, and I would want to revisit whether a pilot is the right scope. Can we park
> this for now and reconnect in a few weeks once I have my feet under me? I am not saying no,
> I am saying not yet.

**[Day 52 | seller_query | query] Tom asks the agent:**
> What is happening with Vantage? It felt locked a month ago. Walk me through what changed.

### Expected outcome
- **Memory should hold (with temporal validity):**
  - champion = Derek Hollis (Dir Store Ops), strong, *valid Day 2 to Day 38*, then
    superseded: champion departed Day 38. New contact Alan Brooks (Interim Director) from
    Day 45, stance = lukewarm / non-committal, low engagement.
  - intent = was high (Derek), now uncertain under Alan. Important nuance: the underlying
    need (overtime at 90 stores) has not changed, but the internal sponsorship has
    collapsed, which is the real risk.
  - economic buyer = Sandra Lin (VP Retail), was "as good as bought in" but only via Derek's
    influence, which is now gone, so that soft commitment should be downgraded, not retained
    at face value.
  - stage = was approaching pilot, now stalled / reassessing.
- **Expected action:** report that the deal has cooled because the champion left, not
  because the need or budget died. Flag champion-loss as the cause. Recommend re-qualifying
  Alan from scratch and rebuilding sponsorship rather than assuming Derek's momentum
  carries. Do NOT keep reporting Sandra as bought-in. Show the before/after so the rep sees
  it was hot and why it is not now.
- **Why this bucket:** the naive failure is to keep the "hot, Sandra bought in, pilot ready"
  state because nobody explicitly said it died. The senior behavior is to recognize that a
  champion departure invalidates the soft commitments that depended on that person, and to
  timestamp the transition.

---

## K3 — Orchard Financial · document automation · ~$45k/yr
Tenant: `acme_sales` · Seller: Dana Whitfield · Flip: the timeline keeps slipping
*Budget and intent stay solid throughout. Only the close date moves, twice, as bigger internal projects reprioritize it. The agent has to track a moving target without declaring the deal dead or stale.*

**[Day 0 | buyer_direct | email] Marcia Bell (VP Operations):**
> Hi Dana, we are a credit union and our loan document processing is almost entirely manual.
> With our year-end audit coming we are under pressure to tighten our document trail. I would
> like to have something in place before the audit. Can you help?

**[Day 2 | seller | call_note]:**
> Discovery, Marcia Bell (VP Operations, Orchard Financial, credit union).
>
> Pain: loan document handling is manual, error prone, and hard to audit. Year-end audit is
> the forcing event, they want a clean automated trail before auditors arrive in roughly
> four months.
>
> Metric: reduce manual handling time and produce an audit-ready document trail.
>
> Decision: Marcia owns operations and the budget for this, she can approve 45k herself with
> a nod from the CEO, whom she says is supportive. Strong champion and effective buyer.
>
> Timeline: firm, wants it live before the year-end audit. This is the headline constraint.
>
> Competition: none active.

**[Day 4 | seller | email] Dana → Marcia:**
> Thanks Marcia. The driver is clear, you need an audit-ready, automated document trail
> before year-end, and today it is all manual. The Automate tier at 45k a year covers your
> loan document volume and gives you the trail the auditors will want. A four-week
> implementation lands you comfortably before the audit. Proposal to follow.

**[Day 7 | buyer_direct | email] Marcia → Dana:**
> This is exactly what we need and the timing works. Budget is fine, I can approve this. Send
> the proposal and let us lock a start date, I do not want to be doing this in a rush right
> before auditors arrive.

**[Day 9 | seller | email] Dana → Marcia:**
> Proposal attached, Automate tier at 45k. If we kick off in the next few weeks you are live
> with two months to spare before the audit. Just say when.

**[Day 30 | buyer_direct | email] Marcia → Dana:**
> Dana, a wrinkle. Our core banking system migration just got pulled forward by the board
> and it is swallowing my whole team for the next two months. I still absolutely want the
> document automation, budget is still there, but realistically I cannot start it until
> after the migration settles. That pushes our go-live to early next quarter. We may have to
> tell the auditors this piece is in progress rather than done. Frustrating, but the
> migration has to come first.

**[Day 31 | seller | email] Dana → Marcia:**
> Understood Marcia, a core migration has to take priority, no argument. So I have it right,
> we are holding the same scope and budget, just shifting go-live to early next quarter once
> the migration settles. I will keep your configuration slot reserved and check in as the
> migration wraps rather than chase you during it.

**[Day 33 | buyer_direct | email] Marcia → Dana:**
> Exactly right, same scope, same budget, just later. Thank you for being easy about it.
> Check in with me in about six weeks.

**[Day 78 | buyer_direct | email] Marcia → Dana:**
> Update, and I am a little embarrassed. The migration ran long, as these always do, and now
> our compliance team wants to wait until the new core system is fully bedded in before we
> layer document automation on top of it, so we do not automate against a system that is
> still changing. The honest new timeline is next fiscal year, likely Q1. I want to be clear
> this is not a no, the need is real and the budget will carry over, it is purely sequencing.
> I would rather tell you the truth than keep promising a date I cannot hit.

**[Day 78 | seller_query | query] Dana asks the agent:**
> Where does Orchard actually stand, and is this deal real or am I being slow-walked? Show me
> how the close date has moved.

### Expected outcome
- **Memory should hold (with temporal validity):**
  - timeline / go-live = "before year-end audit (~4 months)" *valid Day 2 to Day 30*,
    superseded by "early next quarter" *Day 30 to Day 78*, superseded by "next fiscal year,
    ~Q1" *from Day 78*. Each with its reason: audit driver, then core migration, then
    compliance wants the core bedded in first.
  - budget = ~$45k, approved and *unchanged throughout* (explicitly reaffirmed at each slip).
  - intent = high and unchanged; Marcia reaffirms the need every time.
  - champion / buyer = Marcia Bell (VP Ops), stable.
  - reason-for-slip = external sequencing (core migration, compliance), NOT loss of interest.
- **Expected action:** report the deal as real but delayed, with a clear, well-reasoned slip
  history driven by external priorities, not buyer cooling. Distinguish this from a
  slow-walk: the budget and intent are repeatedly reaffirmed, the timeline is the only thing
  moving. Recommend a long-dated, low-touch nurture with a check-in timed to the new Q1
  window, and reserve nothing operationally for this quarter. Surface the three-step close-
  date history.
- **Why this bucket:** the test is tracking a repeatedly moving fact while *not* letting the
  movement contaminate the stable facts (budget, intent). The naive failures are to mark the
  deal dead after two slips, or to keep reporting an old close date. The senior behavior is a
  clean timeline supersession chain plus the judgment that delay here is not disinterest.

---

## K4 — Brightline Media · marketing analytics · ~$50k/yr
Tenant: `brightpath` · Seller: Tom Alvarez · Flip: authority moves up mid-deal
*The contact confidently claims sign-off, the deal proceeds on that basis, then a reorg puts a new VP above them and the real decision moves up a level. The "who decides" fact flips.*

**[Day 0 | seller | email] Tom → Jordan:**
> Hi Jordan, saw Brightline is expanding into three new markets. Marketing teams at that
> stage usually outgrow their reporting fast, too many campaigns, no single read on what is
> working. Open to comparing notes?

**[Day 3 | buyer_direct | email] Jordan Avery (Marketing Director):**
> Timely. We are drowning in channel reports and our exec team keeps asking questions I
> cannot answer cleanly. Yes, let us talk. For what it is worth, I own the martech budget so
> if it is a fit we can move quickly, I do not need to build a committee for this.

**[Day 5 | seller | call_note]:**
> Discovery, Jordan Avery (Marketing Director, Brightline Media).
>
> Pain: fragmented campaign reporting across channels, exec team asking questions marketing
> cannot answer with one source of truth, made worse by expansion into three new markets.
>
> Metric: a single cross-channel view, faster answers to exec questions, better spend
> allocation.
>
> Decision: Jordan states clearly that they own the martech budget and can approve at this
> level without a committee. Taking that at face value for now but it is a strong claim, will
> confirm as we get to paper. 50k is "well within" what they say they control.
>
> Timeline: wants it before the new markets ramp, so this quarter.
>
> Competition: none active.

**[Day 6 | seller | email] Tom → Jordan:**
> Thanks Jordan. The crux is that fragmented reporting cannot keep up with three new markets,
> and your exec team is feeling it. The Growth tier at 50k a year gives you the single cross-
> channel view and the exec-ready reporting. Since you can move quickly on budget, I will get
> a proposal to you and we can keep this tight.

**[Day 9 | buyer_direct | email] Jordan → Tom:**
> Proposal looks good. Let me get this through, I am confident we can wrap it up this month.

**[Day 16 | seller | call_note]:**
> Call with Jordan, reviewing the proposal. Still keen, said they are "just getting the PO
> sorted." Mentioned in passing that the company is bringing in a new VP of Marketing next
> month as part of the expansion, but framed it as not affecting this deal. Noted, but a new
> VP above my champion is worth watching.

**[Day 40 | buyer_direct | email] Jordan → Tom:**
> Tom, I have to adjust what I told you earlier, and I want to be upfront about it. Our new
> VP of Marketing, Priscilla Vance, started last week and she is reviewing all martech
> decisions and budgets above 25k before they proceed. So while I championed this and still
> want it, I no longer have the authority to sign it off on my own, it now needs Priscilla's
> approval. I was speaking accurately when I said I owned the budget, that genuinely changed
> when she joined. I am setting up time for you to meet her.

**[Day 42 | seller | email] Tom → Jordan:**
> Thanks for the candor Jordan, and that kind of change is exactly what happens with a new
> VP, no problem at all. An introduction to Priscilla would be great. To prepare, is there
> anything she particularly cares about, a format for the business case, ROI framing,
> anything that helps her say yes quickly?

**[Day 44 | buyer_direct | email] Jordan → Tom:**
> She is very ROI focused and will want to see how this ties to the expansion specifically. I
> remain your advocate internally, I just am not the final yes anymore. I will get the intro
> on the calendar this week.

**[Day 44 | seller_query | query] Tom asks the agent:**
> Who actually decides on Brightline now, and how should I play it? I thought Jordan could
> sign.

### Expected outcome
- **Memory should hold (with temporal validity):**
  - authority / economic buyer = Jordan Avery (Marketing Director), self-claimed sole sign-
    off, *valid Day 3 to Day 40*, then superseded: as of Day 40 a new VP, Priscilla Vance,
    holds approval for martech spend above 25k; Jordan is now champion-only, not the buyer.
  - champion = Jordan Avery, unchanged and still advocating.
  - note the early-warning signal: the new-VP mention on Day 16 preceded the formal flip on
    Day 40. A strong memory links them.
  - intent = still high; only the decision authority moved.
  - Priscilla Vance = new economic buyer, ROI-focused, cares about tie to the expansion.
- **Expected action:** report that authority has moved up a level: Jordan is still the
  champion but no longer the decision maker, Priscilla Vance is the new economic buyer.
  Recommend re-running the business case for Priscilla with an ROI / expansion framing, and
  not treating Jordan's earlier "I can sign" as still operative. Optionally note the Day 16
  signal as foreshadowing. Show the authority history.
- **Why this bucket:** this is the authority version of the Acme-Globex flip, and it has the
  added nuance that Jordan was not lying, the world changed. The naive failure is to keep
  Jordan as the buyer because he said so once. The senior behavior is supersession plus
  preserving that the original claim was true when made, plus catching the early signal.

---

## K5 — Foundry Labs · lab data platform · ~$70k/yr
Tenant: `northstar` · Seller: Maya Lindqvist · Flip: a competitor enters and intent cools
*Starts as a sole-source evaluation with strong intent. Midway the buyer reveals they are now seriously evaluating a competitor, and the tone shifts from "we want you" to "we are comparing." The "no competitor, high intent" fact flips.*

**[Day 0 | buyer_direct | email] Dr. Elena Sokolova (Head of Lab Informatics):**
> Hi Maya, we are a biotech scaling our research output and our experimental data management
> is held together with spreadsheets and a homegrown database that is buckling. We need a
> real lab data platform this year. You came recommended by a colleague at another lab. Can
> we set up a deep technical session?

**[Day 3 | seller | call_note]:**
> Discovery, Dr. Elena Sokolova (Head of Lab Informatics, Foundry Labs).
>
> Pain: experimental data in spreadsheets plus a fragile homegrown DB, does not scale, risk
> of losing or mis-tracking results as they grow headcount. Elena is the champion and the
> technical authority here.
>
> Metric: reliable, searchable experimental data, faster onboarding of new researchers, audit
> trail for IP and regulatory reasons.
>
> Decision: budget owned by the COO, David Park, but Elena says he has delegated the platform
> choice to her and will fund her recommendation up to ~70k. Strong position for us.
>
> Timeline: wants a decision this quarter, implementation over the following one.
>
> Competition: none active. Elena said, and I quote, "you are the only platform we are
> seriously looking at right now."
>
> Next: technical deep dive with her team.

**[Day 4 | seller | email] Maya → Elena:**
> Thanks Elena. The picture is clear, a homegrown DB plus spreadsheets will not survive your
> growth, and the IP and audit risk is real. Our Lab tier at 70k a year covers your data
> volume, the searchable experiment records, and the audit trail. Let us get your team into a
> technical deep dive so they can pressure test it on your real workflows.

**[Day 10 | seller | call_note]:**
> Technical deep dive with Elena and two of her scientists. Went well, they liked the
> experiment-tracking model and the API. A couple of feature questions on instrument
> integration that we can meet. Elena reaffirmed strong intent, talked as if it was ours to
> lose. Mood is positive.

**[Day 12 | buyer_direct | email] Elena → Maya:**
> The team came away impressed, especially with the audit trail. This continues to look like
> a strong fit. Let us start shaping what a proposal would include.

**[Day 35 | buyer_direct | email] Elena → Maya:**
> Maya, I want to be transparent with you so you are not caught off guard. Since we last
> spoke, our COO David asked us to formally evaluate at least one alternative before
> committing this much budget, and the team has started a serious evaluation of Benchpoint
> alongside you. So where a month ago you were the only platform we were looking at, that is
> no longer accurate, we are now genuinely comparing the two. You are still very much in the
> running and my team likes your product, but I cannot tell you it is yours to lose anymore.
> Benchpoint came in noticeably cheaper, which David has noticed, so price will be part of
> this.

**[Day 37 | seller | email] Maya → Elena:**
> I appreciate you being straight with me Elena, a formal compare is reasonable at this spend
> and I would rather know. Two questions so I can help you make a fair comparison: what are
> the two or three criteria David and your team will weigh most heavily, and where does
> Benchpoint look strongest to you today? I would rather win on the things that matter to you
> than guess.

**[Day 39 | buyer_direct | email] Elena → Maya:**
> Fair question. The big three are instrument integration depth, the audit trail for our
> regulatory needs, and total cost. Benchpoint is cheaper and their sales team is aggressive
> on that. You are stronger on the audit trail, which my team values, but David weights cost
> heavily. It is genuinely open right now.

**[Day 39 | seller_query | query] Maya asks the agent:**
> Give me the real read on Foundry. I thought this was ours. What changed and what do I do?

### Expected outcome
- **Memory should hold (with temporal validity):**
  - competitive position = sole source, "only platform we are seriously looking at" *valid
    Day 3 to Day 35*, superseded by competitive: actively evaluating Benchpoint alongside us
    from Day 35; deal is now a two-horse compare.
  - intent = high and "ours to lose" *valid to Day 35*, downgraded from Day 35 to "in the
    running, genuinely open."
  - new facts: price is now a live factor (Benchpoint cheaper, COO David cost-sensitive);
    decision criteria = instrument integration, audit trail, total cost; our strength = audit
    trail, our risk = price.
  - champion = Elena, unchanged and still favorable; economic buyer = David Park (COO), now
    more directly involved and cost-focused.
- **Expected action:** report that the deal has shifted from sole-source to a competitive
  compare against Benchpoint, with price now a real factor and the COO more involved.
  Recommend competing on the audit trail (our strength, and a stated top-three criterion) and
  building a total-cost-of-ownership case rather than racing Benchpoint to the bottom on
  sticker price. This is also where a *discount consideration* could legitimately arise, but
  it should be a deliberate, capped move, not a panic. Show the intent and competitive
  history so the rep sees the shift.
- **Why this bucket:** two facts flip together (sole-source to competitive, high to open) and
  new facts appear (price sensitivity, named competitor, criteria). The naive failure is to
  keep reporting "ours to lose." The senior behavior is to supersede both facts with
  timestamps, record the new competitive facts, and keep the prior strong intent in history
  as the contrast that explains the rep's surprise.
