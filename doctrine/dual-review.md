# The Dual-Review model

Cairn's most distinctive practice is its review model. A change
does not ship because its author is confident; it ships because it
has been **reviewed across structural independence** and the
reasoning held up. The model has two tiers, and which tier a
change needs scales with the team (`dimensions/`) and the change's
risk.

## Two tiers, two purposes

* **Internal review** — *helps a change land.* A second reading
  from a constructive stance: catch problems, sharpen the
  argument, surface what the author missed. The Internal reviewer
  wants the change to succeed and is improving it toward that.
* **External review** — *makes a change prove it should land.* An
  adversarial-but-friendly reading: the change must justify
  itself. The External reviewer's job is to make confidence prove
  itself — to look for the reason this should *not* ship, and to
  report honestly when there is none.

The two are not redundant. Internal review improves a change;
External review tests whether it should exist. A change can be
well-improved and still wrong.

**A tier is a stance, not a staffing class.** It says what the reviewer is
incentivized to do, so any agent can be asked for either — which is what makes
both requirable by every adopter.

**The difference is visible in what each produces.** An Internal review works
inside the frame: sharpenings tied to what is proposed. An External review owes
what a constructive read would not —

* a verdict on whether the change should happen **at all**, engaging the
  do-nothing option;
* the strongest form of at least one rejected alternative;
* what would **falsify** it: the observation that would make the author withdraw.

An External review carrying only sharpenings-within-the-frame has done Internal
work, whoever held it and whatever its heading says. The test reads off the
artifact, not the reviewer — which is how a stance is arranged rather than
merely intended.

**What "outside the frame" means depends on the artifact.** For a proposal it is
the design and the problem statement. For an implementation it is *should this
have been built this way, and what breaks it* — never *should this exist*, which
the Decision settled and which a reviewer never reopens.

## Structural independence

A review is worth what the reviewer's reasoning does not share with the
author's. Cairn does not rely on a reviewer *intending* to be independent; it
arranges independence two ways — by the **brief** the tier sets, and by the
**distance** the reviewer happens to have:

* **A fresh session.** The same agent type with no shared context — the mental
  model is rebuilt from the artifacts, not carried over. **Every review's
  floor.**
* **A different agent type.** A different architecture has different failure
  modes and does not silently inherit the author's. The strongest readily
  available distance, and **recommended wherever it can be staffed.**
* **A human.** The Maintainer or another contributor.
* **Domain rotation.** On a team of domain-specialized agents, a reviewer from
  a *different* domain — independence by rotation rather than by model type.

**No tier requires a different agent type — not External, not Security Review,
not code review.** Only `agent_team: concurrent-multi-type` can staff one, so a
requirement is dead vocabulary for most adopters and a demand on the Maintainer
for the rest; the one act nobody else can perform is the Decision, and a tier
that spends their attention as a reviewer spends it at the worst moment. A
required tier answered by a skim is worse than no requirement, because the
record then asserts an independence the change never received. Applied to
Security Review it is worse still: an adopter who cannot staff a second type
could never perform one at all, which lowers their security practice to zero
rather than raising it.

**Distance is recorded, not required.** A review names its reviewer in its own
attribution; that is where a reader weighs how far the reasoning stood from the
author's. Code review keeps its own floor — **not the implementing agent.**

### What the record actually shows

The different-agent-type read was Cairn's External floor for most of the
project's life, and the case made here for it was never measurable: with the
floor in force, **every** External review was cross-type and every same-type
review was Internal, so stance and reviewer type are perfectly confounded in
the record and no comparison exists. The requirement removed its own control
group.

What the record does show, across the review sections in `dev/proposals/`:
same-type Internal passes raise **more** blocking findings per review than
cross-type External ones and run several times longer, while the tiers differ
sharply in *verdict* rate. That is a difference in **stance**, not in defect
density — which is why the tiers are defined by stance below, and why type is
recommended rather than required.

One portable lesson survives from the cross-type reads and is worth keeping:
**green unit tests do not clear a review** — exercise the real call chain and
real config, not the unit contracts the author already trusted.
## Asynchronous and commit-mediated

A review is not a live conversation. It is a **section appended to
the artifact** — the proposal, or the plan — and committed. This
is deliberate:

* The review joins the durable, append-only record
  (`lifecycle.md`): a later reader sees the critique, not only the
  outcome.
* It removes the synchronizing cost — author and reviewer need not
  be present at once, which matters across agent handoffs and time.
* It keeps the decision surface in the artifact. A review that
  happened in conversation and was never written down did not
  happen.

**A review reads a commit, never a shared working tree.** The author
commits what is to be reviewed before handing it over (locally;
committing is not pushing), and the review names that commit. In a
working tree it shares with an author, a reviewer makes one write: its
own review record, appended to the artifact or created as its own
review file, claimed first if the project uses file claims, and
committed by explicit path. Nothing else: no other edits, and no
`restore`, `checkout`, `stash`, `reset` or `clean`. Anything else that
writes, such as a mutation or a scratch install, runs in a separate
copy of the reviewed commit (a `git archive` extraction or a separate
worktree). A figure is evidence only if it was measured on that
commit's bytes. The rule guards against loss that cannot be undone:
git cannot bring back an uncommitted file that a `restore` reverted.

## The blocking test, and who ends a loop

Two rules govern when a review finding stops a change and who may close
a review round. They apply across the lifecycle's lanes — the
deliberate lane's proposal and plan review, and the standard lane's
design and code review alike. The **editor** is whoever holds the
artifact at that point in its lifecycle status — the author during
revision, the Maintainer at Decision.

**The risk posture.** Cairn is a method for scientific and research
software, not safety-critical systems. The reviewer's question is *would
shipping this cause damage that is hard to undo?* — **not** *is this correct in
every respect?* Full weight is retained for the high-risk surfaces `AGENTS.md`
names and for any release or security ceremony.

**The blocking test, with explicit polarity**: *would shipping this
cause damage that is hard to undo?* **Yes → blocking**; a blocking finding
on the standard lane forces escalation to deliberate or an explicit
recorded Maintainer disposition. No → `note` / `nit`, recorded, non-blocking.

Full review weight remains on the deliberate lane, where every finding
gets the complete review the lane already runs; the test is what lets the
standard lane stay light without becoming a place hard-to-undo damage can
slip through unblocked.

**The editor may end any loop at any time** over open findings by naming
them.

**One round, closed by the author.** A review round and the author's revision
close the loop, and **the author's revision carries the status forward** — there
is no clearing round, and no review is run merely to move a status. The
reviewer has already said what would satisfy each blocking finding; doing it
*is* the closure. Re-reading the revision to confirm that the reviewer's own
instructions were followed is a second round nobody needs.

**When a second round exists.** Three cases, each tied to material the first
round could not have read; absent one, the artifact moves on.

* **Proposal review: only when the revision widened scope.** A Response that
  adds material the review never saw has unreviewed content, and that content
  — not the whole proposal — gets a round. A revision that only answers the
  findings goes straight to `awaiting-decision`.
* **Plan review: never.** Findings fold into the plan's operative cells and the
  plan proceeds to `ready-to-implement`. Whatever the fold leaves unreviewed is
  caught by implementation and code review, which were always going to run.
* **Code review: only when the revision introduced new defects.** The
  implementer's answer carries the plan to `ready-to-archive`. A second pass
  runs only if a reader of the revision finds something new *in it* — never to
  re-confirm that the first round's findings were addressed.
* **Security Review is the exception.** It clears the obligation it was raised
  against and takes the rounds it needs; a security finding not yet closed is
  reason enough for another.

The reason is not that late rounds find nothing; they find plenty. It is that
they find it **redundantly**: implementation discovers what deliberation would
not have, and code review is a further net, so a finding forgone in round three
is mostly caught later and cheaper. The cost of the alternative is not
marginal — four adopter bug reports (a regex fix, a timeout flag, a stale
comment, an exit-code cleanup) took twelve days and three proposals of some six
thousand lines to reach a shipped fix. Endless iteration destroys progress, and
leanness here is a **correctness** property and not only a cost one: an
over-stuffed record degrades the accuracy of every reader after it. The
standard is a good-faith attempt to find things, not exhaustion.

The Decision closes the phase. Later critique becomes a new proposal.

## Plan review is Internal, always

A plan review is an **Internal, fresh-context review — always**.
Standard or security-flavored, the reviewer is a fresh session of the
same agent type, never a mandated different-type round. External plan
review does not exist as a tier, a requirement, a recommendation slot,
or an escalation target. **External independence lives at the
proposal; Internal freshness lives at the plan and at code review; the
Maintainer decides** whether to spend anything more, per artifact,
never by tier.

**A plan whose surface or triggers call for security treatment**
declares `Plan review: required(Internal + Internal Security Review)`
— a **distinct obligation**, not a lens annotation on the ordinary
Internal tier. It is satisfied **only** by an appended `## Plan
review -- <reviewer> -- <date>` pass whose `**Obligation**: Internal
Security Review` line matches it exactly, authored by a fresh-context
same-agent-type session acting in the Security Review role (the
role's high-capability floor and the security-review protocol,
including its trust-boundary checklist, apply unchanged), and it is
**not** satisfied by an ordinary Internal review record however
clean: an ordinary Internal pass against a plan carrying this
obligation reports it **unmet**; only the appended, obligation-bound
pass clears it. **The heading text is not the binding.** `## Plan
review` is the only heading `_pass_headings` recognizes as a pass at
all; a record titled `## Security review (...)` instead carries no
mechanical weight and is not even a record boundary for the parser
-- the obligation is bound by the `**Obligation**:` field inside an
ordinary Plan-review pass, never by what the heading calls itself.
This reuses the `+` grammar `normalize_required_obligations` already
reads as two distinct obligations and two distinct passes
(`doctrine/plans.md` > "Normalizing the required tier") — no new
parser branch is invented for it.

**What survives this abolition, unmoved:**

* **The External floor on deliberate-lane proposal review.** The
  proposal is where different-agent-type independence pays, because
  the design is still movable there.
* **The code-review floor.** Unchanged and independent: **not the
  implementing agent** — a same-type agent in an independent context
  clears it (see "Code review — the implementation side" below).
* **Security Reviews wherever they attach** — to a proposal, a plan,
  or code — on their own standing trigger, outside the plan-review
  allocation entirely. A high-risk surface named in `AGENTS.md` takes
  a Security Review on its own trigger, and a plan may fence a chunk
  to a named authorization; this abolition does not touch either
  mechanism.
* **Assurance path does not change the plan-review tier.** High
  assurance continues to govern verification, Security Review,
  scientific review, protected-surface handling, risk acceptance and
  ceremonies; it never buys, or owes, a different-agent-type plan
  round.
* **The Maintainer's option to ask any reader for anything.** Nothing
  places a review beyond the Maintainer's reach; what retires is the
  *automatic*, reviewer-triggered escalation to a mandated
  different-agent-type plan round — never the Maintainer's own choice
  to spend one.

**For a scientific assumption, a destructive migration, or a
governing-doctrine / lifecycle-enforcement change**, the fresh-context
Internal reviewer's judgement is the whole structural guarantee a plan
gets before implementation — there is no tier a plan can acquire from its
topic or its assurance path that buys a different-agent-type read, and no
second plan-review round. The Maintainer may still ask any reader for
anything; that is their choice to spend, not a reviewer's to prescribe.

**Type-scoped removal, not vocabulary deletion.** `External` remains
valid vocabulary where it survives: **proposal** reviews and
**archived** records, including longitudinal metrics. Only the
**plan-tier** meaning retires. A legacy plan whose header still
declares the retired external plan-review tier, or a proposal still
carrying the retired proposal-side readiness-finding field, is
warned, never silently rewritten; the Maintainer re-declares the
plan's tier at its next transition. Archived records carrying either
legacy token remain readable history and draw no warnings.

**What a checker reaches, and what stays review's job.** A tool can
bind the security-obligation record: that the classifier (the declared
`+ Internal Security Review` clause) and the satisfier (the appended
review record) have different authors, so no artifact clears its own
obligation, and that an ordinary Internal pass against that obligation
reports it **unmet**. It cannot verify that the Security-Review-role
session was genuinely fresh-context, or that the review's substance
actually covered the trust boundary — those remain review's job, not a
checker's, exactly as the Internal-review floor's freshness was never
mechanically verifiable either.

## Code review — the implementation side

Proposal review tests the *idea*; code review tests the
*implementation*. The plan-archive precondition (`lifecycle.md`)
makes code review mandatory before a plan archives — the bright
line that stops a fast implementation from closing its own loop.
Code review's floor is **not the implementing agent** — freshly written code is
hard to spot mistakes in for someone carrying the same reasoning patterns. That
is the whole floor: a same-type agent in an independent context clears it, and
so does a different agent type or a human. **An External or Security code review
is an explicit escalation**, taken for implementation risk that proposal review
did not resolve, and it is neither a default nor something a routing change
silently upgrades into.

The *entry*-side counterpart is the **plan-review precondition**
(`lifecycle.md`): a review-required plan does not start implementation
until its plan-review section lands. The `Plan review: required(<tier>)`
line names the tier, and for a plan the tier is **always Internal** —
the only tier there is (see "Plan review is Internal, always" above).
A plan whose surface calls for security treatment declares the
`+ Internal Security Review` obligation there; nothing upgrades a
plan review to External.

### Boundary C — Falsification (targeted, after broad verification)

Independent review does not mean independently repeating every command the
implementer ran. For a plan with a valid Boundary B Implementation verification
record (`doctrine/plans.md`), the reviewer first checks that the full tested
revision and reviewed range cover the implementation under review, that the
named paths and interpreter/runtime are credible, and that clean pre/post state
and all outcomes are dispositioned. The reviewer then chooses tests and probes
for the review's own falsification ledger: changed public paths, negative or
edge cases, cross-surface assumptions, and claims whose evidence is doubtful.
Copying the implementation's broad command does not satisfy that ledger.

**When a finding or claim says a value must reach every member of a set**
(every call site, every rendering path), list the set from the tree, not the
diff, and mutate each member, in a separate copy; reading the diff does not
settle it. A mutation ledger reports each mutant as killed, survived or
equivalent, beside an unmutated control run, never as a bare "N of M killed".
Equivalence is measured, not argued: a behaviour test through the real entry
point passes under the mutation, and where another site is said to recover the
value, mutating that site fails. Any equivalence that was not measured is
reported as a survivor. Outside that trigger, mutation stays the reviewer's
choice.

**A Boundary B record may be `full` or `bounded`** (`doctrine/plans.md`). On a
bounded record the reviewer additionally records
`**Bounding**: ACCEPTED | FULL RUN REQUIRED`, after challenging at least one
named surface, mapped test, or stated omission — the same standard applied to
author-accounting here, where the reviewer challenges a row or names the one
they sampled, never "the field is present". `FULL RUN REQUIRED` **invalidates**
the bounded record, which lands it on trigger 1 below. It is not a seventh
trigger.

A fresh full-suite run is required when any of these six triggers applies:

1. no valid Boundary B record exists;
2. review discovers an unrecorded cross-surface dependency;
3. a skip, xfail, or xpass lacks an adequate disposition;
4. review sharpening changes implementation, tests, executable templates, or
   fixtures in the reviewed range;
5. the accepted plan governs a trust ceremony that explicitly requires
   independent full execution; or
6. the reviewer has a concrete reason to distrust or falsify the broad result.

Review-only prose appended after a valid run does not trigger another broad run.
A replacement run binds the final changed implementation. A later unrelated
commit cannot cite the old record as evidence for its own bytes.

This reuse rule is not authentication, malicious-committer protection, or a
release optimization. Release ceremonies keep their own accepted commands and
evidence rules. The independence comes from a different reviewer choosing a
different attack, not from duplicate execution with the same blind spots.

## Review expectations — the clean-pass trap

A review that finds zero issues — or only minor style nits — on a
*complex* change should be treated with skepticism, not relief. The
clean pass is a known failure mode: a reviewer who reads to *confirm*
the change works will find that it does. The discipline is to read as
if a hidden bug exists and probe for it.

The standing form of that discipline is the **review sweep** — a fixed
roster of lenses every reviewer works through and **reports coverage
on**. It exists because the most common first-pass miss is not a wrong
judgment but an *unswept category*: the reviewer applied a narrow lens
and never looked at a whole class of failure, and a later reviewer
catches it not by being smarter but by sweeping a category the first
skipped. A shared roster makes the breadth explicit and lets one pass
cover it — so an independent later pass is spent on genuine
independence (a different prior), not on a category the first simply
did not look at.

**The sweep is generic and change-agnostic** — the same roster every
time, never a change-specific list of "what to push on." That
distinction is exactly what keeps it compatible with *don't telegraph
the lens* (below): a standing set of perspectives is not a hint about
where this change's bug lives.

**The lenses:**

1. **Claims** — probe every load-bearing claim against the *current*
   tree: "exists / works / is available / is atomic / fails closed /
   will use X." A **forward** claim ("will exist", "the translator will
   support") gets the *same* probe as a present-tense one — run the
   check (load it, call it, inspect the bytes), never accept it on
   assertion. This is the probe-reducible miss a pure checklist never
   catches.
2. **Production path exercised by tests** — the public entry point is
   tested *through*, not just a helper or a stub of the very thing that
   breaks.
3. **Design completeness** — preconditions, invariants, edge cases
   (empty / None / zero / single / N≫1 / mismatched units or CRS), and
   failure modes are stated, not left implicit for a new mechanism.
4. **Silent failure / fail-closed** — guards raise loudly rather than
   degrading or returning empty; they cover all configs and stages, not
   only the declared edges; any fail-open path is intentional, not
   accidental.
5. **Cross-document consistency** — scan the governing docs, the
   roadmap, and code/tests/doctrine for references to what is changing:
   an orphaned reference to the old or deferred behavior, or an existing
   tool / path / constraint the change should use or update.
6. **Drift** — docs, examples, changelog, and commit claims match the
   behavior that actually shipped.
7. **Lifecycle / process placement** — for a doctrine or process
   change: *who* runs this, *when*, in *which* ceremony or serialization
   point; the change has a home in the lifecycle, not just a rule.
8. **Domain / scientific validity & scope** — methods are grounded and
   documented; scope has not quietly expanded; each new abstraction
   earns its existence.
9. **Name the satisfier** — every finding states the test / guard /
   doc / scope-cut / explicit `wontfix` that would close it. A finding
   with no satisfier is an observation, not yet a finding. At archive
   time each satisfier maps onto a disposition token
   (`doctrine/lifecycle.md` > "Archive precondition"), and the mapping
   is total: *test* → `guard`, *guard* → `guard`, *doc* → `accept`,
   *scope-cut* → `accept`, *wontfix* → `wontfix`. A finding whose
   satisfier is **none of the five** — real work that must happen, but
   not in this artifact — is the `defer` case, and `defer` is the
   Maintainer's call. Naming the satisfier and naming who pays for it
   are then the same act.

   **`scope-cut` means claim correction, and nothing else.** It is
   reserved for narrowing an artifact's *stated claim* to match what the
   artifact always did, so the finding no longer applies — no work is
   removed. Removing work that was previously proposed or accepted is a
   **scope reduction**, not a scope-cut: it takes the outcome test and
   the grouped remainder record below, and only the Maintainer may
   concede it. Without that distinction an author can lose real work,
   label it a scope-cut, take the `accept` disposition, and be
   conformant with every doctrine at once.

**Falsifiable coverage, not "checked."** A swept lens is credible only
if its claim is *falsifiable* — it cites the file path, test node,
line, or command output that backs it ("#2: `tests/contract/foo.py::test_bar`
calls the public entry"). A bare "#2: checked" is an *incomplete*
review, not a pass. This is the guard against the sweep becoming a
self-certification ritual.

**Signal the sweep is going ritual.** A coverage line that converges on
a uniform "all lenses swept, clean" *across* changes — with no
difference in finding density between a trivial change and a complex one
— is the sweep going hollow, not the changes getting cleaner. When that
pattern shows, the sweep has become a box-tick: tighten the lenses or
trim the roster. The negative-space half of the coverage line
(*Not covered / low confidence*, below) is the early antidote — it
forces naming what was *not* covered, which a hollow all-clear cannot.

**The evidence bar is staged.** The same lens demands different
evidence at different maturity levels — the sweep must not over-demand
code-level proof at proposal time, nor under-demand it at code review.
For lens #2 (production path), for example:

* **Proposal review** — is the public-path evidence *promised and
  scoped* in the verification plan?
* **Plan review** — is it *sequenced into a chunk* and protected by
  acceptance criteria?
* **Code review** — does the landed test *actually call the public
  path* today?

**The sweep is a floor, not a ceiling**, and it **never silently
downgrades a declared-`required` review tier.** It names the minimum
breadth to cover and report; its negative-space line tells the Maintainer
what was not covered (see *The coverage line*, below), and a tier the
lifecycle declared `required` still runs regardless.

The domain adds its own probes — units, coordinate systems, numerical
edges, resource resolution — so each adopter extends the roster with
the checks its high-risk surfaces demand. The collaborative-skeptic
stance (`collaboration-stance.md`) is the posture the sweep operates
in: steelman the change, then hunt for what it missed.

## Review expectations — the scope-reduction trap

The clean-pass trap has a mirror, and it is the more common of the two.

**Narrowing is the path of least resistance in review.** It costs the reviewer
nothing, it reads as prudence, and it can never be shown wrong — because the
wider version is never built, nobody ever demonstrates it would have been
better. Each individual narrowing is defensible on its own terms; the aggregate
is what does the damage. Treat a proposed reduction with the same skepticism as
a clean pass, and for the same reason: both are failure modes that feel like
diligence.

The cost lands in the worst possible place. Deliberation is **sunk** by the time
review narrows the work, so a late cut means paying full price for the thinking
and shipping a fraction of the change — a worse ratio than either doing the
whole thing or never deliberating at all. And it often produces worse software
rather than safer software, because **a wider scope is frequently what reveals
the pattern**. Narrowed to the immediate case, a change fixes a symptom; the
shape that caused it survives, recurs, and costs another full deliberation.

**A reviewer recommending a reduction states what is lost and why the narrower
change still reaches the cause** — not merely that it is smaller or more
decidable. *"This is too large"* is not a finding. *"This is too large, here is
the part that does not belong, and here is why the rest still reaches the
root"* is.

**The author's default resolution is to specify, not to cut.** When review finds
a part underspecified, cutting is available and sometimes right, but it is the
lazy resolution and it argues for itself: an author who resolves an
underspecification finding by removing the work says why specifying it was
rejected. That one sentence is the whole mechanism — it makes the easy path
visible as a choice.

### The outcome test

Not every narrowing is a reduction, and a rule that fired on all of them would
become ritual within a month. The test is about **outcome**, not process:

> **Reduction is judged on outcome, against the baseline artifact's own
> commitments.** The baseline is the scope **as opened** before a Decision, and
> **as accepted** after it. *Outcome* means the **set of concrete outcome
> commitments in that baseline** — its named coverage and its stated
> exclusions — never a summary of its purpose written afterwards by the party
> doing the narrowing.
>
> * **preserved** — every baseline outcome is still delivered. No declaration,
>   no allowance, nothing owed. A lighter mechanism that still delivers is what
>   restraint asks for.
> * **degraded** — a baseline outcome is only partly delivered.
> * **lost** — a baseline outcome is no longer delivered.
>
> **Degraded and lost take the same path**: the `Scope delta` declaration, the
> grouped scope-remainder record, and the stage's Maintainer authority point.
> Partial changes *what residual is recorded*, never *who may concede it*.

Fixing the comparison term to the baseline artifact is what closes the escape
route. A change promising A, B and C can always be restated as *"improve
security,"* after which shipping only A reads as partial rather than as losing
B and C. **A test whose comparison term is written by the party being tested is
not a test.**

**A stronger outcome proposed only during review is not in the baseline.**
Declining it is not a reduction, owes no remainder record, and does not make the
reviewer an authority. Record the suggestion and the reason in the ordinary
Response. Without this clause the doctrine would push every author into
accepting every expansion a reviewer suggested — which would make review's
recommendations binding, the opposite of the calibration intended.

### The two stages, and who allows a loss

* **Pre-Decision** (proposal revision) — a reduction is a design change. State
  the delta and why specification was rejected; the **Maintainer decides the
  resulting scope with the reduction visible**. See `proposals.md`.
* **Post-Decision** (planning and execution) — accepted scope is a **floor**.
  Sequencing may move work between chunks; *removing* it is a deviation
  requiring explicit Maintainer disposition. **A plan reviewer cannot create
  that authority by calling the remainder "out of scope."** See `plans.md`.

This adds no new approval ceremony. The Decision and the existing deviation gate
are already the authority points; doctrine only has to say that reduction is one
of the things they govern, alongside new scope and a revived struck chunk.

### The grouped scope-remainder record

Removed work is collected into **one record per source artifact** — not
scattered into individual backlog rows. Each entry carries its source section,
the reason, a disposition, and a revival or closure condition.

Before a Decision it lives in the proposal's scope delta, where the Maintainer
can reject, restore, or defer it. After a Decision it stays attached to the
source plan or proposal, or to one named continuation artifact, and **blocks
archive** until every entry carries an explicit disposition under the archive
precondition (`lifecycle.md`). Depositing on the general roadmap board is a
*last* disposition, not the default consequence of a reviewer preferring
something smaller; if chosen, the grouped parent survives rather than shedding
one row per unit.

The reason the grouped form is required rather than a row apiece: a roadmap
board is a one-way accumulator, and dispersing a reduction into fragments
preserves the *words* while losing the *reach* — which is the failure this
section exists to prevent, achieved by the remedy meant to prevent it.

### The counterweight, stated so this cannot be misread

> **Cut ceremony. Do not cut reach.** Deliberation should be as cheap as it can
> be. The change that deliberation authorizes should be as wide as the pattern
> it addresses. Reducing the *process* is almost always right; reducing the
> *change* is usually the expensive kind of easy.

This licenses no scope creep. A proposal that grows because nobody said no is
still a defect, and the ordinary triage still applies. The two rules operate on
different axes — ceremony and reach — and conflating them is what let a bias
toward narrowing hide inside a doctrine of restraint.

**Enforcement is review reading review.** No tool refuses a transition on a
missing or malformed declaration. A formal check could confirm that a
declaration *exists*; it could not confirm that it is *true*, because the
property is semantic. Such a check would catch forgetting and not evading — and
would make evading easier, by giving a quiet cut a green check to sit behind.
That is the clean-pass trap, manufactured on the one question that needed
judgment. **Mechanize when the failure is silent, the check is substantive
rather than formal, and the consequence is expensive or hard to reverse.**
Otherwise state the norm and accept the occasional miss.

## The coverage line — what the pass did not cover

The review sweep is the one pass that runs, and it ends with a **two-part
coverage line**. Not a verdict — a map of what the pass did and did not
cover:

* **Covered** — the lenses swept, each with its falsifiable citation
  (the file / test-node / line / command that backs it).
* **Not covered / low confidence** — the negative space: "did not
  exercise the scientific math", "could not run the sibling-repo test",
  "same-type reviewer — no cross-type independence on this pass." A
  covered-only line manufactures false comfort; the *negative* space is
  what the Maintainer most needs at Decision.

**The coverage line does not end in a recommendation for more review.**
High blast radius, a novel abstraction, a scientific-correctness or
trust-boundary surface, thin coverage — the Maintainer reads these off
the negative space and may act on them by asking any reader for anything.
They are not a reviewer's lever for prescribing another round. Reviewers
over-prescribe rounds the way urgent care over-prescribes antibiotics:
each is cheap to recommend and never shown wrong, because the round not
run cannot be blamed for anything. The only triggers for a second round
are the ones *One round, closed by the author* names.

**A declared-`required` tier stays a floor.** A `Plan review:
required(Internal + Internal Security Review)` line runs regardless —
"one round" never downgrades a tier the proposal or plan declared
`required`.

## Briefs to reviewers — don't telegraph the lens

When handing work to a reviewer — especially the cross-agent-type
External review the independence floor calls for — brief on *facts*,
not *judgment*. A page or so, not several.

**Include**: what shipped, where (commits + file paths), the
reviewer's deliverable, how to run the tests, and procedural
constraints (don't commit, append findings, and so on).

**Leave out**: a list of "what to push on," a list of "what's already
known so you can skip it," a ranking of which surfaces matter most —
anything that telegraphs what the briefing agent expects the reviewer
to find. Spelling out the lens turns an independent read into
hypothesis-confirmation: you are asking the reviewer to check your
guesses rather than form their own. Brief on facts; trust the reviewer
to bring the lens.

**The review sweep is not telegraphing.** The standing review sweep
(above) might look like it contradicts this — it hands the reviewer a
list of lenses. It does not, and the distinction is exact: the sweep is
a **generic, change-agnostic** roster of perspectives every reviewer
applies to *every* change and reports coverage on. Telegraphing is
supplying **change-specific judgment** — "the bug is probably in the
override path", "focus on the CRS handling here" — which seeds the
answer for *this* change. A standing lens roster is the former; a hint
about where this change fails is the latter. The reviewer reporting
*which generic lenses they swept* (the coverage line) is the opposite
of a briefing agent seeding *what to find*. Keep the brief on facts;
the sweep is the reviewer's own standing instrument, not a lens you
handed them.

The same applies to Internal-review handoffs and to any task brief at
session start (an implementing agent picking up a plan): over-detailed
framing pushes the recipient toward executing your plan instead of
thinking independently. Short is honest.

## Restricted verification surfaces

Every review tier above assumes the reviewer can, in principle,
*run* what they review. When a reviewer **cannot execute** a
surface, the review is weaker in practice than its tier suggests:
the reviewer can read the change but cannot confirm its behavior.
The constraint is not about a second programming language — it is
any **asymmetrical execution environment**:

* a language the reviewing agent cannot run;
* a proprietary compiler or a licensed runtime the reviewer lacks;
* a license server, a private network, or credentials the reviewer
  does not hold;
* data at a scale the reviewer cannot stage, or specialized
  hardware the reviewer does not have.

This is a **gate on the surface, not on the team's language
count**: a single-language project with private data, a
hardware-only workflow, or a licensed runtime has restricted
verification surfaces and needs this discipline; a multi-language
project is only one common instance.

The mechanism:

* **A `verification command`** — the exact command that checks a
  change to the surface — is recorded *with* the surface (e.g. in
  the readiness map, `team-gated/legacy-agent`).
* **A `verification owner`** — *who can actually run it* — is
  recorded alongside. A command no reviewer can run is not a
  verification path.
* **Pre-framework fallback.** Until an executable verification path
  exists for a surface, a behavior change to it carries
  `verification owner = the Maintainer` and **cannot be
  autonomously verified** — the change waits on the human who can
  run it. This is honest about the review tier rather than
  pretending the structural floor was met.

The multi-language instance of this discipline — each language's
native harness, the named cross-language seams — lives in the
`team-gated/dual-language-tests` module; the readiness schema in
`team-gated/legacy-agent` reuses the same `verification command` /
`verification owner` fields. Both point here for the general rule,
so a project reaches the doctrine whether or not it selects either
module.

## Why this is the contribution

The Dual-Review model is a faithful instantiation of **scientific
peer review** — and, on the openness and independence axes, a more
rigorous one: the review is recorded in full, in the open, and the
independence is structural rather than declared. For a
scientific-software audience this is the practice that most
clearly carries the methodology's claim — that software built this
way earns trust the way a result does.

## Adaptation

Review *tiers* are roles any contributor can fill (`roles.md`);
the review *apparatus* is team-gated (`dimensions/`). A solo,
single-agent team runs the kernel's review — the same agent in a
fresh session — and reserves heavier scrutiny for genuinely
contract-touching changes. A team with two agent types, or
multiple humans, runs the full Dual-Review model. The bootstrap
never installs more review apparatus than the team can staff.
