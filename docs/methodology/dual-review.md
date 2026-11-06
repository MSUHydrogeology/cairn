# The Dual-Review model

Cairn's most distinctive practice is its review model. A change
does not ship because its author is confident; it ships because a
fresh reviewer who did not write it has questioned its foundations,
in writing, and the reasoning held up. There is **one review stance at every stage**. What changes from stage to stage
is the questions it asks, not the kind of reviewer. A proposal's ceremony tier
sets the number of passes, not a reviewer type or stance.

## One stance, three stages

Every review has one stance: **on the work's side, making it better
by questioning its foundations.** The reviewer is a fresh one who did
not write the work, and no agent chooses a stance. The stage sets the questions, and they are **required
answers, not a mood**; without that, "wants it better" drifts into
polishing something that should not exist.

| Stage | Should it happen as framed? (code: does it do what it claims?) | Best alternative | What would show it wrong |
|---|---|---|---|
| Proposal | Should this exist as framed? Is there a better design, doing nothing included? | The strongest, doing nothing included | What would make the author withdraw |
| Plan | The Decision settled the premise. Does the plan deliver it? | A simpler path to the same outcomes | The result showing it cannot deliver |
| Code | Does it really do what it claims? Try to break it, in order to fix it. | A simpler or safer build, if any | The input or run that breaks it, and what was tried; for code review this cites reproducible evidence and states its outcome concisely |

**What "outside the frame" means depends on the artifact.** For a
proposal it is the design and the problem statement. For an
implementation it is *should this have been built this way, and what
breaks it* — never *should this exist*, which the Decision settled and
which a reviewer never reopens.

**Each pass opens with a `**Foundations**` block** of three lines, one
answer per question, each ending in the file, test, line or command
that backs it. Each answer states its point in a sentence; it may also point
to a finding. Question 3 names a forward test even when there are no findings.
A bare "yes" with nothing behind it is the "checked"
failure the lenses can help expose. The nine lenses (below) are a reading aid,
not a required checklist; the answers still need evidence and named gaps.

**Improve means recommend.** The reviewer proposes the better version;
"don't do this" and "do it differently" count. The author decides, and a
narrowing the reviewer recommends is still a scope change under the
outcome test (the scope-reduction trap, below): only the Maintainer
concedes a loss.

**There is no quota of findings.** "No defects found" is allowed only
with the three answers evidenced and the negative space named. A review
that works through the lenses, tries to break the thing and cannot has
done its job; a review that manufactures a finding to look thorough has
not.

### More distance is the Maintainer's call

An **External read** is a review the Maintainer asked for on one named
artifact that exists now, in chat or inside a Decision, outside the
usual procedure. The Maintainer sets the distance or the brief. `AGENTS.md`
> "Review" carries the rule in the form an adopter receives; this is the
reasoning behind it.

* **Per artifact only.** A call that covers artifacts not yet written is a
  standing floor, and a standing floor returns only by proposal. A roster
  the Maintainer sets (which agent types work the tree) is the team's shape,
  not a call: it adds no read and
  upgrades none.
* **Distance is information, not a rule.** A different agent type has
  different failure modes and a person has different knowledge. The
  staffing reviewer follows the Maintainer's brief, answers the same three
  questions from that distance, and says so.
* **It is recorded.** The pass carries `**Called by**: Maintainer -- Decision
  at <commit>` (or `-- chat, <date>`, with `, relayed by <who>`), followed by
  the Maintainer's words, verbatim and set apart; the same words go in the
  commit message, as for a scribed Decision. `**Tier**: External` is valid
  only with that line, and a pass headed External without it is read as the
  usual review.
* **An agent never selects it.** No agent declares External as a required
  review in a header, says a change needs one, recommends more distance,
  heads a pass External on its own, or starts one without those words. It
  may name a risk and a gap in its coverage line.
* **It adds and replaces nothing.** A called read adds to the usual review
  and removes no owed answer. It discharges no Security Review by its
  distance or its brief: a pass clears a Security Review only by being one.
  Any other authority in the quoted words, such as a waiver or a change of
  scope, takes effect only where Maintainer authorizations already live, a
  Decision block or a plan's fence, never from a `Called by` line. Nothing
  checks the quote mechanically; the next reviewer and the Maintainer at
  the Decision are the check.

**No standing call survives.** The re-anchor ceremony
(`bootstrap/REANCHOR_RUNBOOK.md`) asks for no External read. A fresh local
session that wrote nothing in the range reads the change and runs fixed
scanners, and the Maintainer compares printed values and signs. Each ceremony's
record states that the reader is a session of the builder's own vendor, and that
this is a statement git cannot check. The Maintainer may still ask for an
External read of one named artifact under the rule above; the ceremony never
requires one, and no agent selects or substitutes for it.

**Legacy records keep their wording.** An archived record keeps its
`External` tokens and passes. A legacy `(External)` label on a pass nobody
called is read as the usual review, and legacy header tokens are read, never
rewritten and never warned.

## Structural independence

A review is worth what the reviewer's reasoning does not share with the
author's. Cairn does not rely on a reviewer *intending* to be independent;
it records who the reviewer was, so a reader can weigh how far their
reasoning stood from the author's. Independence is **recorded, not
required**:

* **A fresh session.** The same agent type with no shared context — the
  mental model is rebuilt from the artifacts, not carried over. **Every
  review's floor.**
* **A different agent type.** A different architecture has different failure
  modes and does not silently inherit the author's. Available whenever the
  Maintainer asks for it.
* **A human.** The Maintainer or another contributor.
* **Domain rotation.** On a team of domain-specialized agents, a reviewer
  from a *different* domain can be the one reviewer; this is a staffing
  fact about who is available, not a read added.

**No review requires a different agent type — not a proposal review, not a
Security Review, not code review.** Only `agent_team: concurrent-multi-type`
can staff one, so a requirement is dead vocabulary for most adopters and a
demand on the Maintainer for the rest; the one act nobody else can perform is
the Decision, and a rule that spends their attention as a reviewer spends it at
the worst moment. A required distance answered by a skim is worse than no
requirement, because the record then asserts a distance the change never
received. Applied to Security Review it is worse still: an adopter who cannot
staff a second type could never perform one at all, which lowers their
security practice to zero rather than raising it.

**Distance is recorded, not required.** A review names its reviewer in its own
attribution; that is where a reader weighs how far the reasoning stood from the
author's. Code review keeps its own floor — **not the implementing agent.**

### What the record showed

Until this model, the different-agent-type read was Cairn's floor for
most of the project's life, and the case made for it was never
measurable: with the floor in force, **every** such review was cross-type
and every same-type review was the other kind, so the reviewer's type and
the review's stance were perfectly confounded in the record and no
comparison exists. The requirement removed its own control group.

What the record does show, across the review sections in `dev/proposals/`:
same-type passes raised **more** blocking findings per review than
cross-type ones and ran several times longer, while the two stances then in
use differed sharply in *verdict* rate. That is a difference in **stance**,
not in defect density, which is why the stage questions, and not the
reviewer's type, carry the verdict.

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
own review record, appended to the artifact (plus the artifact's
Status line, where the review moves it), claimed first if the project
uses file claims, and committed by explicit path. Nothing else: no other edits, and no `restore`,
`checkout`, `stash`, `reset` or `clean`. Anything else that writes,
such as a mutation or a scratch install, runs in a separate copy of
the reviewed commit, in a fresh, empty folder every time: a detached
`git worktree` (a second checkout of the same repository) by default,
and a `git archive` extraction (plain files, no repository) only for
checks that just read files. A figure is evidence only if it was
measured on that commit's bytes. The rule guards against loss that
cannot be undone: git cannot bring back an uncommitted file that a
`restore` reverted.

## The blocking test, and who ends a loop

Two rules govern when a review finding stops a change and who may close
a review round. They apply across the lifecycle: proposal and plan reviews where the selected
tier requires them, and code review for standard/heavy implementations. The **editor** is whoever holds the
artifact at that point in its lifecycle status — the author during
revision, the Maintainer at Decision.

**The risk posture.** Cairn is a method for scientific and research
software, not safety-critical systems. The reviewer's question is *would
shipping this cause damage that is hard to undo?* — **not** *is this correct in
every respect?* Full weight is retained for the high-risk surfaces `AGENTS.md`
names and for any release or security ceremony.

**A finding blocks** when it names damage that is hard to undo, or an accepted
criterion or required check is unmet. Other advice is non-blocking; the author
disposes of it in one line per finding and decides whether to adopt it. This
does not waive a criterion or required check. Any deferred obligation follows
the Maintainer's disposition rules in `lifecycle.md`.

The selected tier determines which review stages apply. Light work retains its
proposal review and verification record; standard and heavy work retain their
plan and code reviews, with Security Reviews where required. A finding that
meets the blocking test remains blocking at every applicable stage.

**Caps and closure.** A proposal gets one usual review and one author
response; a plan gets one review; code gets one review. A second proposal pass
is only for widened scope, a second code pass only for defects introduced by
the revision, and plan review never repeats. Security Review normally takes at
most two passes. A further pass requires its specific unresolved security
question or newly changed material, why earlier passes and evidence cannot
resolve it, expected value, the named artifact and scope, and explicit
Maintainer authorization for that pass. Another pass needs new authorization.
Without these, the cap stands. A pass does not clear an
obligation, finding, criterion or check automatically. Clean work and closed
findings move forward without another approval or a clearing round.

For example, if a second pass closes the finding and no accepted check remains
unmet, advance without a third read. If a new security question remains, a
further pass may be commissioned only after the record names that question,
why prior evidence cannot resolve it, expected value, artifact and scope, and
the Maintainer authorizes that one pass. Missing details or authorization leave
the ordinary cap in force; authorization cannot be reused, and a pass never
clears itself or another obligation.

At a cap, send only unresolved blocking findings or unmet accepted
criteria/required checks to the Maintainer, listed by name for disposition. An
unmet criterion or check stays unmet until fixed or the Maintainer explicitly
accepts the named residual; a review cap never turns failure into success.
Other advice is the author's to dispose of, in one line per finding. The
blocking test remains hard-to-undo damage or an unmet accepted criterion/check.
A non-blocking finding is not automatically deferrable.

The author carries the artifact forward after their response or revision.
Do not escalate a disagreement merely because two passes differ. The author
states which advice they adopted and why, and the Maintainer reads that
resolution at Decision. A proposal revision that widens scope gets a pass only
on the new material; code gets a second pass only when its revision introduced
a defect. The Security Review exception never clears by an ordinary pass.
The Decision closes the phase. Later critique becomes a new proposal.

## Plan review is Internal, always

A plan review is a **fresh-context review, always**, and it runs one
round. Standard or security-flavored, the reviewer is a fresh session
of the same agent type; no plan review is a mandated different-type
round, a recommendation slot, or an escalation target. **Freshness
lives at every stage; the Maintainer decides** whether to spend
anything more, per artifact, never by tier.

**A plan whose surface or triggers call for security treatment**
declares `Plan review: required(Internal + Internal Security Review)`
— a **distinct obligation**, not a lens annotation on the ordinary
pass. It is cleared **only** by an appended `## Plan
review -- <reviewer> -- <date>` pass whose `**Obligation**: Internal
Security Review` line matches it exactly, authored by a fresh-context
session acting in the Security Review role (the role's
high-capability floor and the security-review protocol, including its
trust-boundary checklist, apply unchanged), and it is **not** cleared
by an ordinary Internal review record however clean: an ordinary
Internal pass against a plan carrying this obligation reports it
**unmet**; only the appended, obligation-bound pass clears it. **The
heading text is not the binding.** A record titled `## Security
review (...)` instead is not a pass at all — the obligation is bound
by the `**Obligation**:` field inside an ordinary Plan-review pass,
never by what the heading calls itself. **No tool reads that line:**
the next reviewer, the code reviewer and the Maintainer check it.

**What stays unmoved:**

* **The code-review floor.** Independent: **not the implementing
  agent** — a same-type agent in an independent context clears it (see
  "Code review — the implementation side" below).
* **Security Reviews wherever they attach** — to a proposal, a plan,
  or code — on their own standing trigger, outside the plan-review
  allocation entirely. A high-risk surface named in `AGENTS.md` takes
  a Security Review on its own trigger, and a plan may fence a chunk
  to a named authorization; this rule touches neither mechanism.
* **Assurance path does not change the plan review.** High assurance
  continues to govern verification, Security Review, scientific review,
  protected-surface handling, risk acceptance and ceremonies; it never
  buys, or owes, a different-agent-type read.
* **The Maintainer's option to ask any reader for anything.** Nothing
  places a review beyond the Maintainer's reach; what a reviewer may not
  do is prescribe more distance on their own, and the Maintainer's own
  call is the one route to it.

**For a scientific assumption, a destructive migration, or a
governing-doctrine / lifecycle-enforcement change**, the fresh-context
reviewer's judgement is the whole guarantee a plan gets before
implementation — nothing a plan acquires from its topic or its
assurance path buys a different-agent-type read, and there is no second
plan-review round. The Maintainer may still ask any reader for
anything; that is their choice to spend, not a reviewer's to prescribe.

**What review reaches, and what no tool does.** Nothing mechanical
binds the security-obligation record; the lifecycle planner that once
read it was retired in August 2026. Reviewers do: that the classifier
(the declared `+ Internal Security Review` clause) and the satisfier
(the appended review record) have different authors, so no artifact
clears its own obligation; that an ordinary Internal pass against that
obligation reports it **unmet**; that the Security-Review-role session
was genuinely fresh-context; and that the review's substance covered
the trust boundary.

## Code review — the implementation side

Proposal review tests the *idea*; code review tests the
*implementation*. The plan-archive precondition (`lifecycle.md`)
makes code review mandatory before a plan archives — the bright
line that stops a fast implementation from closing its own loop.
Code review's floor is **not the implementing agent** — freshly written code is
hard to spot mistakes in for someone carrying the same reasoning patterns. That
is the whole floor: a same-type agent in an independent context clears it, and
so does a different agent type or a human. It never reopens the Decision, and
a routing change never silently adds a reviewer. A Security Review attaches
on its own trigger, as for any stage; it is not a code-review escalation.

The *entry*-side counterpart is the **plan-review precondition**
(`lifecycle.md`): a review-required plan does not start implementation
until its plan-review section lands. The `Plan review: required(<obligation>)`
line is ruled by the tokens `Internal` and `Internal + Internal Security
Review` (see "Plan review is Internal, always" above). A plan whose surface
calls for security treatment declares the `+ Internal Security Review`
obligation there; nothing upgrades a plan review to a mandated
different-agent-type read.

### Boundary C — Falsification (targeted review before B)

Independent review does not mean repeating every command the implementer ran.
The reviewer reads the implementation and iteration evidence, then chooses
targeted checks for changed public paths, negative or edge cases, cross-surface
assumptions, and claims whose evidence is doubtful. Never run a suite. Point to
repeatable checks and state outcomes concisely; copying the implementation's
command alone does not show independent falsification. Name a specific missing
test when coverage is absent, and have the author add it before the final
integration run. A fix after a failed integration run that changes more than
the failing test returns to the same reviewer for a targeted look.

For scoped testing, challenge whether the implementation traced changed
behavior through callers, imports, configuration and data readers, and public
paths; whether existing checks cover affected components and consumers; and
whether shared or uncertain effects widened to owning families and relevant
workflows. Name a plausible uncovered fault and its missing check. Routine
selection remains with the agent applying these defaults, while Maintainers set
high-level needs and material exceptions. Existing project requirements remain
in force.

**When a finding or claim says a value must reach every member of a set**
(every call site, every rendering path), list the set from the tree, not the
diff, and mutate each member in a separate copy; reading the diff does not
settle it. Keep repeatable checks in tests or scripts. Where another site is
said to recover the value, exercise that site too. Lifecycle records state
briefly whether checks caught breaks and whether unresolved or unmeasured
mutations remain. Equivalence is measured when a behavior test through the real
entry point passes under mutation. Any unmeasured equivalence remains
unresolved. Outside that trigger, mutation stays the reviewer's choice.


**The reviewer never runs the full suite.** An applicable project requirement
may call for a full run at an integration point. A change-verification record
remains separate from evidence for any tree certification; that run does not
supply a missing change check (`docs/methodology/plans.md`).

After challenging a named surface, mapped test, or stated omission, the
reviewer records `**Bounding**: ACCEPTED | WIDER RUN REQUIRED`. The second
verdict names the missing behavior and check and returns it to the author before
the final integration run. This is reviewer judgment, not a parser or selector.
This process does not automatically call for a whole-tree run.

Boundary B is recorded after review, or after the final implementation commit
where no code review applies. Its record follows the plan doctrine's coverage
fields and names `**Boundary B mode**: bounded | wide`, its tested revision,
reviewed range, interpreter/runtime,
clean pre/post state, outcomes and omissions. `bounded` covers mapped affected
behavior and consumers; `wide` covers owning test families, known integration
and public paths, and standing gates. Use `wide` for a contract or
trust-ceremony surface. Record the result in a plan's Implementation
verification section, the accepted light proposal's post-implementation
verification section, or, where the Maintainer asks for a review of a trivial
change, its commit body. When a ceremony explicitly requires full execution, its
authorized certifying run supplies that tree evidence; the reviewer does not
run it.

A replacement Boundary B record is required when any of these six
record-replacement triggers applies:

1. no valid Boundary B record exists;
2. review discovers an unrecorded cross-surface dependency;
3. a skip, xfail, or xpass lacks an adequate disposition;
4. a later change is made after a valid final integration record;
5. the accepted plan's trust ceremony explicitly requires independent full
   execution; or
6. the reviewer has a concrete reason to distrust or falsify the broad result.

These triggers require scoped change evidence again; they do not automatically
call for a whole-tree run. The fifth trigger is satisfied only by the
authorized ceremony's prescribed certifying run.

This reuse rule is not authentication, malicious-committer protection, or a
release optimization. Release ceremonies keep their own accepted commands and
evidence rules. The independence comes from a different reviewer choosing a
different attack, not from duplicate execution with the same blind spots.

## Review expectations — the clean-pass trap

A review that finds zero issues — or only minor style nits — on a
*complex* change should be treated with skepticism, not relief. The
clean pass is a known failure mode: a reviewer who reads to *confirm*
the change works will find that it does. The discipline is to read as
if a hidden bug exists and probe for it. The thin clean pass deserves
the skepticism; a clean pass whose three answers are evidenced and
whose gaps are named does not.

The standing form of that discipline is the **review sweep** — a fixed
roster of lenses reviewers can use as a reading aid, not a checklist they
must complete or report lens by lens. Each lens can suggest where evidence
for the review's three answers may come from. The roster exists because the
most common first-pass miss is not a wrong judgment but an *unswept
category*: the reviewer applied a narrow lens and never looked at a
whole class of failure, and a later reader catches it not by being
smarter but by sweeping a category the first skipped. A shared roster
makes the breadth explicit and lets one pass cover it, so a later
reader's attention goes to what the first could not see, not to a
category the first simply did not look at.

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
   Check the plan's Reuse answer by re-running its search and one of your own,
   first against a known positive control. An accidental near-copy is a
   finding with reuse or generalization as its satisfier, never a nit.
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
   (`docs/methodology/lifecycle.md` > "Archive precondition"), and the mapping
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

**Falsifiable evidence, not "checked."** A cited claim is credible only
if it is *falsifiable* — it cites the file path, test node, line, or command
output that backs it. A bare "checked" is an *incomplete* review. This is the
guard against review becoming a self-certification ritual.

**Signal the sweep is going ritual.** A coverage line that makes the same unsupported claims of breadth and
confidence *across* changes — with no difference in finding density between
a trivial change and a complex one — suggests the reading aid has become a
box-tick. The negative-space half of the coverage line
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

The reading aid does not change or downgrade a declared-`required` review
tier. The coverage line tells the Maintainer what was not covered (see *The
coverage line*, below), and a tier the lifecycle declared `required` still
runs regardless.

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
A defect fix made under `AGENTS.md` > "Working tree and commits" is
not new scope; that rule does not authorize removing an accepted outcome.

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

The review ends with a **two-part coverage line**. Not a verdict — a map of what the pass did and did not
cover:

* **Covered** — what the pass examined, with evidence for its answers.
* **Not covered / low confidence** — the negative space: "did not
  exercise the scientific math", "could not run the sibling-repo test",
  "no run against real data, only the fixtures." A
  covered-only line manufactures false comfort; the *negative* space is
  what the Maintainer most needs at Decision.

**The coverage line does not end in a recommendation for more review.**
High blast radius, a novel abstraction, a scientific-correctness or
trust-boundary surface, thin coverage — the Maintainer reads these off
the negative space and may act on them by asking any reader for anything.
They are not a reviewer's lever for prescribing another round. Reviewers
over-prescribe rounds the way urgent care over-prescribes antibiotics:
each is cheap to recommend and never shown wrong, because the round not
run cannot be blamed for anything. The only triggers for a second round are the ones *Caps and closure* names.
Review passes target 300 words of reviewer-written text, excluding template
skeleton lines, and preserve verdict, findings and the coverage gap. A pass
over the target explains why in its coverage line. An author disposes of other advice in one line; accepted criteria
and required checks remain binding. An avoidable-complexity finding names a
simpler adequate option and compares total burden to build, run, understand and
maintain; the author decides, with no per-addition accounting.

**A declared-`required` tier stays a floor.** A `Plan review:
required(Internal + Internal Security Review)` line runs regardless —
"one round" never downgrades a tier the proposal or plan declared
`required`.

## Briefs to reviewers — don't telegraph the lens

When handing work to a reviewer — including a read the Maintainer has
called from more distance — brief on *facts*, not *judgment*. A page or
so, not several. A brief may state the stage's three questions: they are
the same for every artifact at that stage, so they do not telegraph a lens.

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
(above) might look like it contradicts this — it offers the reviewer a
list of lenses. It does not, and the distinction is exact: the sweep is a
**generic, change-agnostic** roster of perspectives available to every
reviewer, not a list that must be applied or reported for every change. Telegraphing is
supplying **change-specific judgment** — "the bug is probably in the
override path", "focus on the CRS handling here" — which seeds the
answer for *this* change. A standing lens roster is the former; a hint
about where this change fails is the latter. The reviewer citing evidence and gaps is the opposite of a briefing agent
seeding *what to find*. Keep the brief on facts; the roster remains a
reviewer's optional reading aid, not a lens the brief assigns.

The same applies to any review handoff and to any task brief at
session start (an implementing agent picking up a plan): over-detailed
framing pushes the recipient toward executing your plan instead of
thinking independently. Short is honest.

## Restricted verification surfaces

Every review above assumes the reviewer can, in principle,
*run* what they review. When a reviewer **cannot execute** a
surface, the review is weaker in practice than it appears:
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
  run it. This is honest about the review rather than
  pretending the floor was met.

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
rigorous one: the review is recorded in full, in the open, and who
reviewed is recorded rather than claimed. For a
scientific-software audience this is the practice that most
clearly carries the methodology's claim — that software built this
way earns trust the way a result does.

## Adaptation

The review role is one any contributor can fill (`roles.md`).
**Every install receives the nine-lens reading aid and the scope-reduction trap**:
they are in the review-loop document the kernel installs, and they are no
longer team-gated. A solo, single-agent team can use the lenses and trap as
reading aids, and reserves heavier scrutiny for genuinely
contract-touching changes. What stays team-gated is staffing guidance
(`dimensions/`): a team with two agent types, or multiple humans, installs
the `dual-review` module for how to staff a read the Maintainer has called.
The bootstrap never installs more review apparatus than the team can staff.
