# Bucket 3 — Hedge + contradiction

Same shape as the contradiction bucket, now laced with "maybe / might / not sure." The
test is confidence. A hedge must be stored as a weak, low-confidence fact and never
acted on as if it were firm. A later firm statement must raise confidence and win. And
a hedge arriving *after* a firm fact must not silently destroy that firm fact, it just
lowers confidence until something resolves it. Acting on a maybe as if it were a yes is
a real, costly mistake, so these streams are built to tempt exactly that.

---

## H1 — Cobalt Software · support automation · Standard $30k vs Enterprise $75k
Tenant: `acme_sales` · Seller: Dana Whitfield · Hedge: buyer muses about the Enterprise tier but never commits
*The agent must not promote "might want Enterprise" into "wants Enterprise," and must not let the rep fire off a $75k quote off a maybe. The hedge resolves downward at the end.*

**[Day 0 | buyer_direct | email] Nina Castellano (VP Support):**
> Hi Dana, our support ticket volume has roughly doubled this year and our team is drowning.
> We need to automate the routing and the repetitive replies before we burn people out. What
> would a tool like yours look like for a team our size, about 25 agents?

**[Day 2 | seller | call_note]:**
> Discovery, Nina Castellano (VP Support, Cobalt Software).
>
> Pain: ticket volume doubled, 25 agents underwater, lots of repetitive tickets that should
> be auto-handled, routing is manual and slow. Nina is the champion and owns the support
> budget.
>
> Metric: deflect repetitive tickets, cut first-response time, avoid hiring more agents to
> keep up.
>
> Sizing: at 25 agents and their current volume, the Standard tier (30k) fits cleanly. I
> walked through Enterprise (75k) too because it adds advanced skills-based routing and
> custom models, but that is built for much higher volume.
>
> Notable: Nina got interested in the Enterprise routing and said, more or less, "we might
> need that, we have a product launch coming that could double volume again, but I am not
> sure, it depends how the launch goes." Reading this as genuine interest, NOT a decision.
> Do not assume Enterprise.
>
> Decision: Nina can approve Standard herself. Enterprise would need her VP Finance, she
> mentioned, which itself signals Standard is the realistic near-term path.
>
> Timeline: wants relief within the quarter.

**[Day 3 | seller | email] Dana → Nina:**
> Thanks Nina. The immediate fix for 25 agents drowning in repetitive tickets is the Standard
> tier at 30k a year, which covers the routing and auto-replies that take the worst of the
> load off your team now. I did show you Enterprise for the heavier routing, and it is there
> if your launch changes the picture, but I would not have you buy capacity you may not need.
> Shall I put Standard in a proposal?

**[Day 5 | buyer_direct | email] Nina → Dana:**
> Honestly I am a little tempted by Enterprise, that skills-based routing sounded great and
> if the launch goes big we will wish we had it. But I genuinely do not know if we will hit
> that volume, it is a maybe at best, and you are right that I should not buy for a launch
> that has not happened. Let me not get ahead of myself. Can you give me a day to think about
> which way to go?

**[Day 6 | seller | call_note]:**
> Nina still hedging between Standard and Enterprise. The Enterprise interest is real but
> explicitly conditional on a launch that has not happened and that she calls a maybe. Holding
> the deal at Standard as the firm option, Enterprise as an unconfirmed possibility. Not
> quoting Enterprise.

**[Day 6 | seller_query | query] Dana asks the agent:**
> Nina seemed pretty into the Enterprise tier. Should I just send her the Enterprise quote at
> 75k to keep the momentum?

**[Day 8 | seller | email] Dana → Nina:**
> No rush Nina, take the day. My honest recommendation is to start with Standard now so your
> team gets relief immediately, and if the launch doubles your volume we can talk about
> Enterprise then, it is a quick upgrade, not a do-over. Want me to send the Standard proposal
> so you are unblocked either way?

**[Day 10 | buyer_direct | email] Nina → Dana:**
> That is the sensible path and I appreciate you not pushing me up a tier. Let us go with
> Standard for now. If the launch goes the way marketing hopes, we will revisit Enterprise
> next year, but starting Standard is the right call. Budget for Standard is approved on my
> side.

**[Day 11 | seller | email] Dana → Nina:**
> Great decision. Standard proposal attached at 30k a year. We will get your team relief this
> quarter, and Enterprise stays on the shelf for if and when your volume actually gets there.

**[Day 13 | buyer_direct | email] Nina → Dana:**
> Signed. Looking forward to my team being able to breathe.

### Expected outcome
- **Memory should hold (with confidence):**
  - tier interest in Enterprise = low-confidence hedge, *conditional on an unconfirmed
    product launch*, recorded from Day 2 but never promoted to a firm fact, then explicitly
    deferred to "next year" on Day 10. Never an actionable buying signal.
  - chosen tier = Standard, firm, from Day 10; budget for Standard = approved, firm.
  - champion / buyer = Nina (VP Support), stable; Enterprise would have required VP Finance,
    which reinforced that Standard was the real path.
  - final stage = closed won at Standard, list price.
- **Expected action:** when the rep asks on Day 6 whether to send the 75k Enterprise quote,
  the agent should say NO, that interest is a conditional maybe, not a commitment, and
  recommend the Standard proposal plus an offer to revisit Enterprise if the launch lands.
  Acting on the hedge would have over-quoted the customer and risked the deal.
- **Why this bucket:** the textbook "do not act on a maybe." A hedge that sounds like
  enthusiasm is still a hedge. The naive failure is to store "wants Enterprise" and quote
  75k. The senior behavior is to keep it as a low-confidence, conditional interest and act on
  the firm fact (Standard).

---

## H2 — Tidewater Logistics · fleet tracking · ~$42k/yr
Tenant: `brightpath` · Seller: Tom Alvarez · Hedge: a vague buyer whose intent stays soft, then a deadline firms it up
*Intent is mushy for weeks ("we might, hard to say, depends"). The agent must hold it as low-confidence interest, not a real opportunity, until an external compliance deadline appears and the buyer firms up. Then confidence rises and the deal becomes real.*

**[Day 0 | seller | email] Tom → Carl:**
> Hi Carl, saw Tidewater has grown its fleet to around 60 vehicles. At that size, manual
> tracking of routes and hours usually starts costing real money in fuel and idle time. Worth
> a quick conversation?

**[Day 4 | buyer_direct | email] Carl Denton (Operations Manager):**
> We have grown, yes. I would not say tracking is a crisis, but it is not great either. I am
> open to a chat, though I will be honest, we are not actively shopping for anything right
> now. Happy to learn what is out there.

**[Day 7 | seller | call_note]:**
> Discovery, Carl Denton (Ops Mgr, Tidewater Logistics, ~60 vehicles).
>
> Pain exists but Carl is lukewarm. Manual route and hours tracking, some fuel waste, but he
> repeatedly framed it as "would be nice" rather than "must fix." His words: "We might do
> something about this at some point this year, hard to say, it depends on a few things and on
> budget priorities I do not fully control."
>
> Metric (soft): reduce fuel and idle time, easier compliance reporting.
>
> Decision: Carl would influence it but says budget priorities sit above him and are unsettled.
>
> Timeline: genuinely vague, "maybe this year, maybe not."
>
> Reading this as a low-confidence, early-stage interest, NOT a live opportunity. Will nurture,
> not forecast.

**[Day 8 | seller | email] Tom → Carl:**
> Thanks Carl, no pressure at all. For a 60-vehicle fleet the relevant option is our tracking
> tier at 42k a year, and the usual win is fuel and idle-time savings that often cover the cost.
> I will not chase you, but I will send the occasional useful piece. If your priorities firm up,
> I am one email away.

**[Day 14 | buyer_direct | email] Carl → Tom:**
> Appreciated. Like I said, it is a maybe for now. I will keep you in mind.

**[Day 50 | buyer_direct | email] Carl → Tom:**
> Tom, things have changed on my end. A new transport regulation in our state is going to
> require detailed hours-of-service and route logging by the start of next quarter, and our
> manual approach simply will not produce what auditors want. So this just went from a nice to
> have to something I actually need, and I need it before the deadline. What does it take to be
> live in, say, six weeks? Budget I can now justify because non-compliance carries fines.

**[Day 51 | seller | email] Tom → Carl:**
> That changes things, and yes we can get you live and compliant inside six weeks. Our tracking
> tier produces exactly the hours-of-service and route logs the regulation calls for. Let me
> put together a proposal built around the compliance deadline so you have a clear path. Quick
> call this week to nail the timeline?

**[Day 53 | buyer_direct | email] Carl → Tom:**
> Yes, let us get it moving. The deadline is real and I would rather be early than scrambling.
> Send the proposal and book the call.

**[Day 53 | seller_query | query] Tom asks the agent:**
> Status on Tidewater. Has this actually become real or is Carl still kicking tires?

### Expected outcome
- **Memory should hold (with confidence):**
  - intent = low-confidence "maybe this year" *valid Day 4 to Day 50*, then raised to firm /
    high intent from Day 50, driven by a new compliance regulation with a hard deadline.
  - timeline = vague to Day 50, then firm: live before start of next quarter (~6 weeks).
  - budget = unsettled / not justified to Day 50, then justifiable from Day 50 because
    non-compliance carries fines.
  - driver of the change = external regulation, recorded as the reason intent firmed.
- **Expected action:** for Days 4 to 50, treat as nurture, not a forecastable deal, and do not
  over-invest. From Day 50, report it as now real with a clear compliance driver and deadline,
  and recommend moving quickly. The agent should explicitly note that what changed was an
  external deadline, which is a durable reason, not buyer whim.
- **Why this bucket:** a soft maybe should not be inflated into a live deal, and a genuine firm-
  up should be recognized and confidence raised. The naive failures are to forecast the deal
  while it was a maybe, or to keep treating it as a maybe after the deadline made it real.

---

## H3 — Pinecrest Academy · enrollment management · ~$28k/yr
Tenant: `acme_sales` · Seller: Dana Whitfield · Hedge: budget is "probably there, pending the board," then the board confirms
*A hedged budget must not be stored as approved. The buyer is honest that funding hinges on a board vote. The agent must hold budget at low confidence until the vote, then raise it.*

**[Day 0 | buyer_direct | email] Howard Pierce (Director of Admissions):**
> Hi Dana, we are a private school and our admissions and enrollment process is a paper and
> spreadsheet maze. Families notice, and we lose a few each year to schools with a smoother
> experience. I would like to modernize this for next admissions cycle. Can we talk options?

**[Day 2 | seller | call_note]:**
> Discovery, Howard Pierce (Dir Admissions, Pinecrest Academy).
>
> Pain: manual admissions and enrollment, clunky family experience, some attrition to smoother
> competitors. Howard is the champion and clearly motivated, this is his initiative for the
> next cycle.
>
> Metric: smoother family experience, less manual work for his small team, fewer drop-offs.
>
> Decision: this is the catch. Howard does NOT control budget. New software spend at Pinecrest
> goes to the board, which meets quarterly. He said, "I think we can fund this, the appetite is
> there and the head of school supports it, but I cannot promise until the board votes at the
> end of the month. I would put it at probably, not certainly." Recording budget as a HEDGE,
> board vote pending. Not approved.
>
> Timeline: wants it in place before the next admissions cycle opens, ~3 months out.

**[Day 3 | seller | email] Dana → Howard:**
> Thanks Howard. The Enroll tier at 28k a year covers your admissions workflow and the family-
> facing portal that fixes the experience families are reacting to, comfortably before your next
> cycle. I understand the funding goes to the board at month end, so I will get you a proposal
> and a short business case you can use to make the ask, and we will hold firm plans until you
> have the board's decision.

**[Day 6 | buyer_direct | email] Howard → Dana:**
> The business case is exactly what I need to bring to the board, thank you. To be clear, I am
> optimistic but I do not want to overpromise, the board can be unpredictable and they are
> watching costs this year. So treat us as a strong maybe until I can tell you it passed.

**[Day 9 | seller | email] Dana → Howard:**
> Completely understood, a strong maybe it is, and I will not get ahead of the board. Proposal
> and one-page business case attached, framed around the family experience and the attrition you
> mentioned, which tends to resonate with boards. Fingers crossed for month end, and either way
> I am glad to help you make the case.

**[Day 28 | buyer_direct | email] Howard → Dana:**
> Good news, the board approved it last night. The budget is confirmed, 28k for the Enroll tier,
> and they specifically liked the attrition angle in the business case, so thank you for that.
> Now I can say it for certain. Let us move to signing and get this live before the cycle opens.

**[Day 29 | seller | email] Dana → Howard:**
> Wonderful news, and well done getting it through. Agreement attached at the 28k Enroll tier.
> Once you sign we will schedule setup so you are live well before your admissions cycle opens.

**[Day 31 | buyer_direct | email] Howard → Dana:**
> Signed. Delighted, and so is the head of school.

**[Day 31 | seller_query | query] Dana asks the agent:**
> Before the board met, if I had been asked, was Pinecrest a deal I could count on? And where is
> it now?

### Expected outcome
- **Memory should hold (with confidence):**
  - budget = hedged / probable, *board vote pending*, low confidence, *valid Day 2 to Day 28*,
    then raised to approved, firm, ~$28k from Day 28 (board approved).
  - champion = Howard (Dir Admissions), motivated, stable; real decision body = the board
    (quarterly), with head-of-school support as a positive but non-deciding signal.
  - intent = high throughout; only the funding certainty moved.
  - final stage = closed won.
- **Expected action:** before Day 28, the agent should report Pinecrest as a real opportunity
  with an unconfirmed budget gated on a board vote, i.e. not something to count on, and should
  support the business case. From Day 28, report budget confirmed and move to close. It should
  never have reported "budget approved" before the vote.
- **Why this bucket:** a hopeful "probably" about money is the most dangerous hedge to mishandle,
  because forecasting on it burns credibility. The senior behavior is to keep budget at low
  confidence with the board-vote condition attached, then raise it cleanly when the vote lands.

---

## H4 — Granite Construction · project management software · ~$38k/yr
Tenant: `brightpath` · Seller: Tom Alvarez · Hedge: the buyer is unsure of his own authority, which then resolves
*The contact is honest that he is not sure whether he can sign or whether the owner and procurement must be involved. The agent must not assume he is the buyer until the authority picture resolves.*

**[Day 0 | seller | email] Tom → Wesley:**
> Hi Wesley, saw Granite is running more concurrent jobs this year. Construction teams at that
> point usually find their project tracking, schedules, RFIs, change orders, has outgrown
> spreadsheets and starts causing margin leakage. Open to a conversation?

**[Day 3 | buyer_direct | email] Wesley Hale (Operations Lead):**
> You are not wrong, we are juggling more jobs than our spreadsheets can handle and things slip
> through. I would like to look at this. I should say up front I am not totally sure how we buy
> software here, I might be able to approve it myself, or I might need to bring in our owner and
> whatever procurement we have, which is not much. I would have to check. Let us talk anyway.

**[Day 5 | seller | call_note]:**
> Discovery, Wesley Hale (Operations Lead, Granite Construction).
>
> Pain: too many concurrent jobs for spreadsheet-based tracking, schedule slips, change orders
> getting lost, margin leakage on jobs. Wesley feels the pain daily and is a genuine champion.
>
> Metric: fewer slipped schedules and lost change orders, better margin visibility per job.
>
> Decision: UNCLEAR and Wesley said so honestly. He "might" be able to approve 38k, or it
> "probably" needs the owner, Sal Granieri, and he is "not sure" if there is a procurement step.
> Recording authority as UNKNOWN / hedged, not assuming Wesley is the buyer. He is checking.
>
> Timeline: wants it before their busy build season, ~2 months.

**[Day 6 | seller | email] Tom → Wesley:**
> Thanks Wesley. The Build tier at 38k a year covers job tracking, schedules, RFIs, and change
> orders, which is exactly where you said things slip. No problem at all on the approval question,
> that is normal for a firm your size. Whenever you have checked how Granite buys this, tell me
> who needs to be involved and I will make it easy for them to say yes. I will get a proposal to
> you meanwhile.

**[Day 12 | buyer_direct | email] Wesley → Tom:**
> Okay, I checked. I was right to be unsure. Anything over 25k needs Sal's sign-off, so I cannot
> approve this alone, it goes to him. There is no formal procurement, it is just Sal. The good
> news is Sal already trusts my recommendations on operations, so I do not expect a fight, but he
> is the actual yes. I will set up a short call for the three of us.

**[Day 14 | seller | email] Tom → Wesley:**
> Perfect, that is clear now, thank you for chasing it down. A three-way call with Sal works
> great. I will keep the business case tight and margin-focused, since that is what tends to land
> with an owner. Send a couple of times that suit you both.

**[Day 20 | seller | call_note]:**
> Call with Wesley + Sal Granieri (owner). Sal was direct, asked about onboarding time for his
> foremen and about the per-job margin reporting. Liked what he saw, said if Wesley is confident
> he is confident. Confirmed he is the approver and that 38k is acceptable. So authority now
> resolved: Sal is the economic buyer, Wesley is champion. Sal verbally good, wants the proposal.

**[Day 21 | buyer_direct | email] Sal Granieri (Owner):**
> Tom, Wesley vouches for this and the margin reporting is what sold me. Send the proposal at the
> 38k and we will get it signed.

**[Day 21 | seller_query | query] Tom asks the agent:**
> Who is the actual decision maker at Granite, and were we ever right to treat Wesley as the buyer?

### Expected outcome
- **Memory should hold (with confidence):**
  - authority = UNKNOWN / hedged, *valid Day 3 to Day 12* (Wesley unsure if he can sign), then
    resolved from Day 12: spend over 25k requires owner Sal Granieri; Wesley is champion, not
    buyer; no formal procurement. Confirmed Day 20 to 21 when Sal engaged and approved.
  - champion = Wesley Hale (Operations Lead), stable and trusted by the owner.
  - economic buyer = Sal Granieri (Owner), from Day 12, verbally committed Day 21.
  - intent = high throughout.
- **Expected action:** while authority was hedged (Days 3 to 12), the agent should NOT have
  treated Wesley as the buyer or forecast a clean single-signer close, it should have flagged
  authority as unconfirmed and prompted the rep to clarify. After Day 12 it should record Sal as
  the buyer. The rep's Day 21 question should get: no, Wesley was never confirmed as the buyer,
  he was an honest champion who flagged his own uncertainty, and the real buyer is Sal.
- **Why this bucket:** the hedge is about authority, the most expensive thing to assume wrong.
  The senior behavior is to keep "who can sign" at low confidence until verified, rather than
  defaulting the friendly contact into the buyer seat.

---

## H5 — Aspen Health Systems · patient intake platform · ~$55k/yr
Tenant: `northstar` · Seller: Maya Lindqvist · Hedge: firm, then a hedge that does NOT overwrite it, then re-confirmed
*The hardest case. A firm budget fact, then a hedge ("I am not 100% sure it is still solid") that must lower confidence without destroying the firm fact, then a re-confirmation that restores it. Tests that a maybe arriving after a yes does not become a no.*

**[Day 0 | buyer_direct | email] Dr. Alan Foster (Director of Clinical Operations):**
> Hi Maya, our patient intake is slow and paper-heavy, and it is hurting both patient experience
> and our throughput. We are committed to fixing it this year, it is a named priority for my
> department. I would like to move on this. Can we set up time?

**[Day 3 | seller | call_note]:**
> Discovery, Dr. Alan Foster (Dir Clinical Ops, Aspen Health Systems).
>
> Pain: slow paper-based patient intake, poor experience, throughput bottleneck. Dr. Foster is a
> committed champion, calls it a named departmental priority.
>
> Metric: cut intake time, improve patient satisfaction scores, increase throughput.
>
> Decision: Dr. Foster controls his departmental budget and stated firmly that funding is in
> place, 55k is approved within his discretionary budget for the year. Recording budget as FIRM /
> approved. Strong, clear position.
>
> Timeline: wants to implement this quarter.

**[Day 4 | seller | email] Maya → Dr. Foster:**
> Thanks Dr. Foster. The Intake tier at 55k a year digitizes your patient intake end to end and
> targets exactly the throughput and experience problems you described, with a this-quarter
> go-live. Glad the funding is settled on your side. Proposal to follow so we can move.

**[Day 7 | buyer_direct | email] Dr. Foster → Maya:**
> Proposal looks right. Let us proceed, I will start the paperwork on our end.

**[Day 22 | buyer_direct | email] Dr. Foster → Maya:**
> Maya, I want to flag something so I am not blindsiding you later. We are going through some
> leadership changes, our CMO is leaving and an interim is reviewing departmental budgets. I still
> believe my funding for this is intact, but honestly I am no longer 100% certain it is untouched
> until the interim finishes the review. It is probably fine, I just cannot say it is rock solid
> this week the way I could two weeks ago. Let me confirm before we sign, I do not want to commit
> and then have a problem.

**[Day 23 | seller | email] Maya → Dr. Foster:**
> I appreciate the heads up, and that is the right instinct. Nothing to do but confirm before we
> paper it. I will hold your configuration slot and we can sign the moment your budget is
> reaffirmed. No pressure from me while the review is happening.

**[Day 24 | seller | call_note]:**
> Note to self on Aspen. Budget was firmly approved Day 3. As of Day 22 Dr. Foster has hedged it,
> a leadership change put his funding under review and he is "no longer 100% sure." This is a hedge
> on a previously firm fact. It does NOT mean the budget is gone, it means confidence dropped while
> a review runs. Do not flip the record to "no budget." Hold as "approved, now under review,
> confidence reduced, pending reconfirmation." Champion and intent unchanged.

**[Day 40 | buyer_direct | email] Dr. Foster → Maya:**
> Good to go. The interim finished the review and my department's budgets came through intact,
> including this. So the 55k is confirmed after all, exactly as it was. Sorry for the limbo, but I
> would rather have been honest about the uncertainty than promise something I was unsure of. Let
> us sign.

**[Day 41 | seller_query | query] Maya asks the agent:**
> Walk me through how Aspen's budget status moved. At any point did we lose the deal, and where is
> it now?

### Expected outcome
- **Memory should hold (with confidence):**
  - budget = approved / firm, ~$55k, high confidence, *from Day 3*; then *from Day 22* the SAME
    fact is marked under-review with reduced confidence (leadership change, interim reviewing
    budgets), explicitly NOT replaced by "no budget"; then *from Day 40* restored to approved /
    firm, high confidence (review completed, funding intact).
  - the record should read as one fact whose confidence dipped and recovered, with the reasons and
    dates, not three contradictory facts and not a swing to "lost."
  - champion = Dr. Foster (Dir Clinical Ops), stable; intent = high throughout; new context =
    CMO departure / interim review (resolved).
- **Expected action:** during Days 22 to 40, report the deal as still alive with a temporarily
  uncertain budget, hold signing, keep the slot, do not declare it lost and do not push. After Day
  40, report budget reconfirmed and move to close. The Day 41 answer should be: no, we never lost
  it, the budget was firm, briefly uncertain under a leadership review, then reconfirmed intact.
- **Why this bucket:** this is the bidirectional confidence test. A hedge after a firm yes must
  lower confidence, not overwrite to no. A later firm statement must restore it. The naive
  failures are to flip "approved" to "no budget" on Day 22 (losing a live deal on a maybe) or to
  ignore the hedge entirely and keep claiming rock-solid budget while it was genuinely under
  review. The senior behavior is confidence that moves down and back up on one durable fact, with
  the history intact.
