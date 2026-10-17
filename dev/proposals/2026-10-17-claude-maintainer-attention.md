# What waits on the Maintainer: one board view, one turn rule, and no work left in archived plans

**Author**: Claude (Strategy)
**Status**: revising
**Review**: required(External)
**Plan review**: required(Internal) — prose, two templates and one small shipped tool; no security surface (see the preflight)
**Opened**: 2026-10-17

## In brief

Three open issues ask one question: *what needs the Maintainer, and where will
they see it?* Today the answer is scattered: file bodies, your memory, and
archived plans nobody re-reads. All three issues are covered, with parts of #13
and #28 left out for stated reasons.

1. **A list of what waits on you** (#27): `python tools/board.py --maintainer`.
   It shows proposals at `awaiting-decision` and plans whose header says they
   wait on you. The board still reports only what authors wrote.
2. **Agents take their own turns** (#13). An agent told "work the board as
   <role>" takes its role's turns, so you no longer carry commit references
   between agents. It stops at everything on your list, and at every push.
3. **Nothing still to do may live only in an archived file** (#28). Work handed
   to an unopened plan gets a board row; the archive commit writes its changelog.

## Questions for the Maintainer

1. **When work moves to a later plan your acceptance already covered, may the
   agent quote that acceptance rather than ask you again?** *Recommended: yes*,
   if the accepted proposal's own text names the work. Anything else still comes
   to you in the archive batch.
2. **Should a board-driven agent stop before every archive, even one needing
   nothing from you?** *Recommended: no.* Today an implementer archives without
   you unless a deferral or scope cut needs your words, and those will be on
   your list.
3. **Close #13 once this is decided?** *Recommended: yes.* Your 2026-08-25
   triage note says to close it when sweep chunk 2 lands, and it has
   (`dev/plans/archive/subtraction-sweep.md`, C1–C9). This proposal carries the
   part still open.

## Context

**Terms.** A *header line* is a bold `**Field**: value` line at the top of a
proposal or plan. `tools/board.py` reads these lines and nothing else. A
*fence* is a plan chunk marked MAINTAINER-GATED or MAINTAINER-ONLY, which does
not run until you authorize it. A *`defer`* is the archive-time disposition that
puts leftover work on the board. It needs your words, quoted
(`dev/plans/_template.md` > Dispositions).

**The status field promises more than it delivers.** `doctrine/lifecycle.md` >
"The proposal lifecycle" says one "can tell from the status alone whose move it
is". That is true for proposals. For plans it fails at a fence (the subtraction
sweep's C8 and C9 were your moves while the plan read `implementing`), at a
`defer` batch, and at a deviation request. Pushes appear in no artifact at all.
To answer "what waits on me?", LHM built a tracker outside the repository. It
works for one vendor's agents only, and outside the reviewed record (#27).

**So the Maintainer is the courier.** Each review leg reaches the next agent
because you carry its commit reference (#13). The convergent-lifecycle contract
(`dev/proposals/archive/2026-08-21-claude-convergent-lifecycle.md`) made loops
end without you. The one-round rule (`doctrine/dual-review.md` > "The blocking
test, and who ends a loop") cut the number of legs. Neither removed the relay.

**Work can live only in an archived file** (#28). Most of the rule exists:
`doctrine/plans.md` > "Lasting-truth migration doctrine" says "an item with no
landing place outside the plan is a `defer`, and needs a row". Two gaps remain:

* **Sequencing across plans.** "Sequencing is free" (`doctrine/plans.md` >
  "Accepted scope is a floor") meant chunks within one plan. LHM read it as
  covering moves between plans. Work held for plans 2–6, none of them opened,
  became "sequencing, not reduction", pointing at an archived proposal. You
  caught it only by asking. Cairn has the same shape: a Class C security
  follow-on, never opened, was lost for two months, and two archived artifacts
  each declined it (`dev/PLANNING.md` > Queued, "Four deferred Maintainer
  questions").
* **The changelog line owed at the next goodnight.** At LHM, four plans in one
  week each owed one. In Cairn,
  `dev/plans/archive/interpreter-trust-root-fallback.md` deferred one to "the
  next goodnight-routine scrub", and fork-advisory-semantics' owed line needed
  your explicit "Yes, please proceed with that CHANGELOG line" (`6912d526`).

## Proposal

### A. One header line and one board view (#27)

* **Plans and change notes gain an optional header line,**
  `**Waiting on Maintainer**: <what, in one line>`. The holder writes it when
  the next move becomes yours: a fenced chunk, a `defer` batch, or a deviation
  request. The holder deletes it when you answer. Plan headers are already
  mutable, like Status. Proposals need no such line, because
  `awaiting-decision` already names you.
* **lifecycle.md's status sentence names this line as its exception.**
* **`board.py --maintainer` lists artifacts carrying the line, plus every
  `awaiting-decision` row.** The plain board shows the line as a column, as it
  does for every field.
* **The footer names pushes rather than counting them:** *"pushes are not
  listed; `git status` shows them, and pushing is always the Maintainer's."*
  Counting would give a tool that adopters execute its first subprocess, only to
  print what `git status` already prints.

**The board still judges nothing, and this is why.** #27 suggests deriving fence
and `defer` state from body text, using a "gate cleared" convention. The board
would then decide whether quoted words clear a gate. Its docstring disclaims
that judgment, and `TestTheBoardReadsHeadersAndJudgesNothing` pins the
disclaimer. Body-text parsing also fails the dangerous way. Fences appear 57
times across 15 archived plans, in headings, table cells and prose, mostly as
discussion. No convention says what a cleared one looks like; #27 proposes
inventing one. A parser that missed a fence would print "nothing waiting", and
nobody would notice. So the holder declares and the board reports, the same
split as Status. The board's one built-in mapping, `awaiting-decision` to the
Maintainer, is the vocabulary's own definition.

### B. The status field is the turn token (#13, vendor-neutral half)

A *turn token* says whose move it is. Status already is one. This change adds a
paragraph to `doctrine/session-routines.md` > "Session start" (move 4). It also
adds one sentence each to `AGENTS.md` > Session routines and to its twin:

* **Standing direction.** Under "work the board as <role>", an agent takes each
  turn the board shows its role holding: a review at `awaiting-review`, a
  Response at `revising`. It finds the commit with `git log` on the artifact,
  so nobody relays a reference.
* **Bright lines, kept from #13.** It **stops at every Maintainer gate**: every
  `--maintainer` row, any deviation or override, and every push. It **never
  takes a turn on its own work**: the independence floors in
  `doctrine/dual-review.md` are unchanged. It **fails toward a human**: an
  unknown status, an unparseable header, or a turn it doubts is its role's
  counts as a gate, so it stops and says so.
* **Already covered.** The one-round rule caps runaway loops. A review taken
  off the board has no brief, so nobody can steer it
  (`doctrine/dual-review.md` > "Briefs to reviewers — don't telegraph the lens").

**The background watcher is left out.** #13 also proposes a watcher that
notices a turn mid-session. #13 itself homes that mechanism in each tool's
wrapper, outside the vendor-neutral core. By #13's own stated limits, it lives
inside a running session and cannot start a stopped agent. #13 says it "wants a
live two-agent drive before scoping". And it would be a new mechanism, against
"build nothing new". Pulling turns at session start removes the relay without
it.

### C. An archived artifact is a record, not a to-do list (#28)

1. **The rule:** *nothing still to be done may have an archived artifact as its
   only home.* A live home is an open proposal or plan that names the item in
   its own text, an issue by number, or a board row; a pointer to an archived
   artifact or an unopened plan is not one. It lands in `doctrine/lifecycle.md` >
   "Archive precondition", with a pointer from `dev/plans/_template.md` >
   Dispositions, and one line in the board's restatement, which already points
   at its source (#26).
2. **Sequencing stays within a live plan.** `doctrine/plans.md` and
   `dev/plans/_template.md` > Scope delta gain the phrase "between chunks of a
   live plan". Work handed to an unopened plan is a `defer` to that work's board
   row, listing the items. If the accepted proposal's text names the work, its
   quoted Decision authorizes the defer (Question 1). There is precedent: the
   board's gate-manifest row ("Joined 2026-10-17") already quotes a Decision
   this way.
3. **The archive commit writes the plan's changelog entry.** `AGENTS.md` already
   makes an archive a changelog serialization point. When two same-day archives
   both edit `Unreleased`, `doctrine/coordination.md` > "Required signal+read for
   coordination-surface files" already applies. The goodnight still verifies the
   changelog.

**Two parts of #28 are left out.** *"Other owed notes go to the next-session
handoff file"*: the queued 2026-10-16 row makes `NEXT_SESSION.md` a local,
untracked file, and `doctrine/plans.md` already rules it out as an archive-time
home, so such notes go to a board row. *The `claim_check` soft-flag*: the
precondition is documentary by design (`doctrine/lifecycle.md` > "Recording
it"), and a flag would be new machinery.

## Rationale

**Why one proposal.** A gives you the list. B makes that list the agents' stop
sign, so you stop being the courier. C keeps work out of archived files, which
the board never reads. Each part leans on another: without A, B has no stop
list, and without C, A misses whatever the archives swallowed.

**The cost** is about twenty lines of board code, four tests, and a dozen
sentences of prose. **In return**, one command replaces your memory of what is
pending, you stop relaying commit references, and "was anything left behind?"
stops being your question. The only new mechanism is a flag and a column on an
existing tool, so accepting this is the go-ahead "build nothing new" asks for.

## Alternatives considered

* **Derive gate state from body text** (#27's suggestion). This is the strongest
  alternative, because authors write nothing extra and a forgotten declaration
  still gets caught. It lost on three counts: it makes the board judge; it fails
  silently on any fence spelling it does not know; and the "gate cleared"
  heading it needs costs authors as much as the header line.
* **A new `awaiting-maintainer` status.** It hides which chunk is waiting. It
  needs transitions in both lifecycle diagrams and in every template. And each
  fence costs two transitions, where one line carries the same information.
* **Do nothing.** You stay the courier, and the out-of-repo tracker stays the
  only answer. Homeless work is found only when you think to ask.

## Documentation / doctrine surface

* **Doctrine:** `doctrine/lifecycle.md` (A, C1), `doctrine/plans.md` (C2),
  `doctrine/session-routines.md` (B).
* **Governing text and templates:** `AGENTS.md` and `templates/core/AGENTS.md`
  (B); `dev/plans/_template.md` and `templates/core/dev/plans/_template.md` (A, C).
* **Board and tool:** `dev/PLANNING.md` (one line, at a serialization point);
  `tools/board.py` and its byte-identical twin, `templates/skills/_lib/board.py`.

Routing follows `docs/DOCUMENTATION_PLAN.md`. `doctrine/proposals.md` is
untouched, because it defers to lifecycle.md.

### Doctrine-change rate-limit

`doctrine/rationale.md` > "How the doctrine evolves under evidence" requires
recurrence or a routine-boundary synthesis. I claim recurrence:

* **C:** the same shape at LHM and in Cairn's lost Class C follow-on, and owed
  changelog lines four times at LHM in a week and twice in Cairn's archives.
* **A:** it corrects a claim that every fenced plan falsifies, a standing
  defect rather than an incident.
* **B is the thinnest.** It answers no incident, only the relay paid on every
  review leg; #13's evidence is a replay of real loops in an adopter. If you
  judge that too thin, B separates cleanly from A and C.

## Evidence / verification plan

### Tests required

Four new nodes go in `bootstrap/tests/test_replacement_tools.py` >
`TestTheBoardReadsHeadersAndJudgesNothing`:

1. `--maintainer` lists an `awaiting-decision` proposal and a plan carrying the
   line, and nothing else.
2. A plan whose *body* names an uncleared MAINTAINER-GATED chunk, with no header
   line, is **not** listed. This pins that the board reads no body text.
3. The footer names pushes as unlisted.
4. The new field passes through the shared encoder.

The plan maps the tests that read the changed prose. Grep finds four candidates:
`test_scope_reduction_trap.py`, `test_claim_check_module.py`,
`test_loop_fidelity_gate.py` and `test_skill_contract.py`. **Boundary B runs
full**, because a shipped executable template changes.

### Examples / smoke checks

`python tools/board.py --maintainer` on the live tree (empty is valid) and on a
fixture tree; `python scripts/check_cairn.py`; `python scripts/claim_check.py`
per changed document; `python scripts/quality_gate.py --sub neutrality --sub
redundancy`.

**What would falsify it:** something waits on you that `--maintainer` did not
list. Record each case. Two in the first month mean declaring is the wrong
design.

#### Security preflight — five questions, answered in writing

N/A: no trust boundary added, moved, or widened. The new field passes through
the existing header regex and `encode_display` encoder. The board gains no
subprocess and no new file reads.

## Signals the change is wrong

* **A miss:** something waits on you that the list did not show.
* **Stale lines:** `Waiting on Maintainer` lines routinely outlive their answer.
  That is safe, but it means the instrument is wrong.
* **Over-halting:** agents halt so often that pings outnumber relays saved.
* **A wrong turn:** an agent takes a turn outside its role, such as reviewing
  its own work. If so, withdraw B.
* **Pile-up:** sibling-plan `defer` rows accumulate unopened, which is the
  one-way board lifecycle.md warns against.

## Scope delta

**Scope delta**: preserved. This is the opening scope. What is left out of #13
and #28 is named under Proposal, because an issue is input, not this proposal's
baseline.

## Assurance path

**Assurance path**: high-assurance — mandatory, because this edits `doctrine/`,
the authoring templates, and a tool that adopters execute.

## Review -- Claude (External) -- 2026-10-17

**Model**: Claude Opus 5.5 — a fresh session of the author's own agent type: no
shared context, and no cross-type distance.

```
Reviewed commit: adae47616642eac2af5d0b54cc6f45ac9b085971
Target: the whole proposal, In brief through Assurance path; facts checked against the working tree on 2026-10-17
Prior findings: none
Assurance path: high-assurance
```

**Tier**: External
**Findings**: raised (3 blocking, 4 non-blocking)
**Verdict**: REVISE

### Verdict in brief

**Parts A and C should happen. Part B should not happen in this proposal.**

* **A** is the right shape, but as written its list would be empty today while
  three of your deferred questions and the gate re-anchor wait on you (MA-1).
  Its central promise — one command replaces your memory of what is pending —
  is false until it reads where part C sends the work.
* **C** is small, sound and well evidenced. One condition in Question 1 needs
  tightening (MA-4).
* **B** lets agents act on a field the record shows going stale, with no rule
  for two agents who both think it is their turn (MA-2). By the author's own
  account it answers no incident, which the doctrine rate-limit asks for
  (MA-3). It should come back on its own, after the live two-agent trial #13
  itself asks for.
* **Doing nothing** leaves you reconstructing pending work from memory (A) and
  leaves LHM's lost-leftovers failure open (C). For B, doing nothing costs
  about two short hand-offs per proposal, now that the one-round rule caps the
  legs.

**The strongest rejected alternative** is *declare and check* (MA-5), not the
pure body-text parsing the proposal rejected.

**What would falsify the central claim** — that `--maintainer` shows everything
waiting on you — is one item waiting that the view did not list. The live tree
already supplies two (MA-1). After revision, the test should be an archive-time
check a code reviewer runs, not your memory (MA-6).

### Steelman

You are the one role that cannot be parallelized, and today you hold three
kinds of state in your head: what waits for a Decision, which fences are yours,
and what was deferred. The proposal answers this while keeping the board
honest. The holder declares and the board reports, the same split Status
already uses, so the tool never decides whether a gate cleared. It rejects a
heavyweight new status, and it adds almost no machinery: one field, one flag,
one footer, a dozen sentences. C closes a real hole by reusing the existing
`defer` vocabulary. That restraint is right, and most of what follows asks for
less, not more.

### Findings

#### MA-1 — BLOCKING: the "waiting on you" list would be empty today while things wait on you, and part C sends more of them where it never looks

**Plain:** run on today's tree, `--maintainer` would print nothing. Yet three of
your deferred questions and the gate re-anchor wait on you right now, in
`dev/PLANNING.md`, which the board does not read. A list titled "waiting on
you" that comes back empty teaches you to trust the empty list. That is the
*silent miss* — a failure that looks like a clean result — which the proposal
itself calls the dangerous failure.

* `tools/board.py` reads only `dev/proposals/*.md` and `dev/plans/*.md`
  (`_rows`, line 77). Today there is no active plan and no proposal at
  `awaiting-decision`, so the view would have zero rows.
* `dev/PLANNING.md:469` holds "Four deferred Maintainer questions", three still
  open since 2026-08-03. `dev/PLANNING.md:156` holds the gate-manifest
  re-anchor, which is Maintainer-only and says of itself "This will not
  announce itself" (line 166). Pushes are a third class, and the footer names
  only that one.
* C makes this worse. Every `defer` lands on a `dev/PLANNING.md` row
  (`dev/plans/_template.md` > Dispositions), and C2 sends work for unopened
  plans there too. So the moment a plan archives, everything it deferred to you
  drops out of the view. The Rationale's "without C, A misses whatever the
  archives swallowed" has it backwards: C moves work to the one place A cannot
  see.
* The proposal's own test — two misses in the first month — is met before it
  ships.

**Closes it:** either (1) give a `dev/PLANNING.md` row the same declared marker
on its first line, and have `--maintainer` read that one file for that one
marker; or (2) say plainly that the view lists only what artifact headers
declare, and have the footer name every class it does not list (board rows,
undeclared fences, pushes). Option 1 is still "declare, don't judge", but it
adds a file read, so the security preflight's "no new file reads" needs
updating. Either way, add a fixture test that pins the choice. I recommend 1,
because C's design sends your deferrals there.

#### MA-2 — BLOCKING: part B lets agents act unattended on the status field, but that field has been wrong on the record and cannot name two holders at once

**Plain:** under B, an agent reads a status and acts on it with nobody in the
loop. Twice in August a plan's status sat wrong while work landed. B would have
shown an implementer a plan with nothing started, and a reviewer a plan still
awaiting review that had already been built. B also has no rule for two agents
who both think it is their turn.

* **Stale tokens.** `full-suite-interception` read `ready-to-implement` while
  two chunks landed and a Security Review ran and closed. Its fix commit
  `495c6a7f` gives the cause: "The header field has no moment attached to it,
  and nothing checks the two agree". `subtraction-sweep` read
  `awaiting-plan-review` from plan-open through C7 (`a516bcdc`). B's "fails
  toward a human" fires on an *unknown* status, not on a stale valid one.
* **Two holders.** A `required(A + B)` review owes two passes, but
  `awaiting-review` names one holder. One is live today:
  `2026-10-17-claude-neutrality-and-upgrade-slots` declares
  `required(External + Security Review)`. After the first pass sets
  `revising`, an author working the board can answer it and move it to
  `awaiting-decision` with the second pass still owed. Two sessions in one
  role can race, because a work intent is "a courtesy signal, not a lock"
  (`doctrine/coordination.md:109`). #13 itself lists "cross-agent turn
  arbitration" as the unsolved deployment work.
* **Uncommitted drafts.** The board reads the working tree. During this review
  it listed that same proposal at `awaiting-review` while it was still
  untracked: another session was opening it. B would send a reviewer to a
  draft that has no commit to put in `Reviewed commit:`.
* **The stop list is incomplete by design.** B stops at "every `--maintainer`
  row", and MA-1 shows that set is incomplete. The stop set should be
  `AGENTS.md`'s four approval points (push, Decision, deviation, a plan's
  fence), read from the artifact itself.
* **The preflight's N/A covers the board, not B.** The board treats header
  text as "untrusted for display purposes" (`tools/board.py:46`). B turns that
  same text into the trigger for agent action. Asked of B, preflight question
  S4 — "which way does it break?" — has an answer: toward more action.

**Closes it:** B states that, before acting, the agent:

* checks the status against the artifact's own record (its recent commits, the
  chunk markers, every clause of the declared review line), and treats any
  disagreement as a gate;
* claims a work intent first, and stops if another session already holds one;
* acts only on committed artifacts;
* stops at the `AGENTS.md` approval points, not at the view.

It also answers the five preflight questions for B. Or MA-3's route is taken
instead.

#### MA-3 — BLOCKING: part B has not earned a doctrine change, and should leave this proposal

**Plain:** Cairn's rule is that doctrine changes only after a failure recurs.
By the author's own account, B answers no failure. You already judged #13 done
in substance in August. And B quietly reverses the session-start rule that the
board is never an instruction to act.

* **The rate-limit gate** — Cairn's brake on doctrine churn
  (`doctrine/rationale.md:407`) — needs a recurring *failure*, or a synthesis
  at a routine boundary. The proposal says B "answers no incident, only the
  relay paid on every review leg". A recurring cost is not a recurring failure.
* **Your own triage.** Your 2026-08-25 note on #13 reads: "Implemented in
  substance by the accepted `convergent-lifecycle` contract". B reopens that
  call, but Question 3 asks only whether to close the issue, not whether you
  still want B.
* **It reverses standing doctrine without listing it.**
  `doctrine/session-routines.md:66` says the board is "never a mandate to
  act". Lines 79–80 say session start is "orientation, not execution", and to
  "await the operator's direction". "Work the board as <role>" is a standing
  direction that hands the choice of artifact to the agent. That may be right,
  but it amends those sentences, and the proposal does not name them in its
  doctrine surface.
* **The saving is small.** You still start every session and name its role. B
  removes only the naming of the artifact and the commit.
* **The evidence is missing.** #13 says it "wants a live two-agent drive before
  scoping". That drive is exactly what B lacks.

**Closes it:** move B into its own proposal, opened after a recorded two-agent
drive, and record the move in Scope delta (narrowing before a Decision is
legitimate when it is recorded). Question 2 moves with B. The proposal says "B
separates cleanly", and nothing in A or C depends on it.

#### MA-4 — non-blocking: Question 1's condition is always met, so any accepted work could drift to a plan that never opens without you seeing it

**Plain:** the condition is "if the accepted proposal's own text names the
work". But all accepted work is named in the accepted text — that is what
accepted scope is. So as worded, an agent could push any accepted outcome to an
unopened "later plan" by quoting your old acceptance. The board calls such a
deposit "a scope decision" (`dev/PLANNING.md:594`), and scope decisions are
yours.

**Closes it:** make the condition "the accepted text *assigns* this work to that
later plan" — that is, you accepted that sequencing. The defer line then quotes
the sentence that assigns the work, not only the Decision. LHM's six-plan case
and the gate-manifest precedent both meet that bar; a plan that simply came up
short does not. Change the recommended answer to Question 1 to match.

#### MA-5 — non-blocking: the strongest alternative was rejected for the wrong reason, because a forgotten header line fails just as silently as a parser that misses a fence

**Plain:** the proposal rejects reading plan bodies because a missed fence
would print "nothing waiting" and nobody would notice. But a holder who forgets
to write the new line produces exactly the same silence, and MA-2 shows that
header lines do get forgotten.

* The Alternatives section concedes the alternative's merit: "a forgotten
  declaration still gets caught".
* The fear of unknown spellings is not borne out. All 15 fenced archived plans
  use the two template tokens: a grep for `MAINTAINER-GATED` and
  `MAINTAINER-ONLY` finds 57 lines. The hard part is telling a cleared fence
  from an open one, not finding the fence.
* **Not weighed: declare *and* check.** Keep the header line as the source of
  truth. Add one advisory footer line naming any active plan whose body carries
  a fence token but whose header declares no wait: *mentions a fence, declares
  no wait — open it*. That judges nothing about clearing; it only turns the
  forgotten-line miss from silent into visible. Active plans are few (none
  today), so the noise is bounded. Proposed test 2 would then pin that footer
  line instead of pinning the silence.

**Closes it:** adopt the check, or answer it in Alternatives with the reason it
loses.

#### MA-6 — non-blocking: the failure test relies on your memory, the very thing the tool replaces

**Plain:** "Record each case" names no place to record a miss and no one whose
job is to notice it. The tool cannot see its own misses by construction, so only
you would catch one, by remembering. `AGENTS.md` asks that a check whose only
trigger is a human remembering be described that way.

**Closes it:** make it an archive-time step for the code reviewer. For each
fenced chunk, `defer` batch or deviation request the plan records, `git log -p`
on the plan file shows whether a Waiting line was ever written. A missing line
is a miss, recorded in a named file. The "two in the first month" threshold then
has an instrument behind it.

#### MA-7 — non-blocking: four factual corrections

1. **New fields do not get a column automatically.** "The plain board shows the
   line as a column, as it does for every field" is not true today. `_FIELDS` is
   a fixed list (`tools/board.py:33`), and the module says any other field
   "simply has no column" (line 32), so the change must add the field to that
   list. Cells are cut at 48 characters (`_encode`), so "<what, in one line>"
   needs a length budget.
2. **Plan headers are not generally mutable.** "Plan headers are already
   mutable, like Status" overstates the rule. `doctrine/plans.md` > "Mutability
   rule" lists `Status` and the last-update date, not other header lines. The
   new line needs adding to that list, and plans.md's surface entry should name
   A as well as C2.
3. **Cairn's second changelog example is weaker than cited.** It (`6912d526`)
   needed your explicit yes because of the commit rule then in force, which let
   agents commit without asking only inside `dev/` (the commit body says so).
   That rule has since been replaced. Cairn's own evidence for C3 is therefore
   one archive, and the recurrence rests on LHM. That still clears the gate.
4. **B relies on a board column that does not exist.** B's paragraph lands in
   the section of `doctrine/session-routines.md` that already promises an
   "owner role" column the board lacks (line 52, open as IB4 in
   `dev/reviews/2026-10-17-code-review-issue-batch.md`). B's phrase "the board
   shows its role holding" leans on that column. The board shows Status only.
   The status-to-holder mapping lives in `doctrine/lifecycle.md` prose, and
   `Author` is not a column.

### Questions for the Maintainer

1. **Should part B leave this proposal and return after a recorded two-agent
   trial, as #13 itself asks?** *Recommended: yes.* A and C do not need it, and
   your August triage already counted #13 as done in substance. If yes, keep
   #13 open as B's home (this changes the proposal's Question 3).
2. **(Replaces Question 1.) May an agent quote your acceptance as the authority
   to defer work to a later plan *only* when the accepted text assigned that
   work to that plan?** *Recommended: yes, only then.* Anything else comes to
   you in the archive batch.
3. **Should the waiting list also read `dev/PLANNING.md` for rows marked as
   waiting on you?** *Recommended: yes* — that is where every deferral you
   authorize ends up.

### Coverage

**Covered.**

* *Claims*, each checked against the tree:
  * the doctrine quotes and anchors: `doctrine/lifecycle.md:145`,
    `doctrine/plans.md:438`, "Lasting-truth migration doctrine" and its
    exclusion of `NEXT_SESSION.md`, and the `dual-review.md` and
    `coordination.md` anchors;
  * the `PLANNING.md` rows: `dev/PLANNING.md:469` and the "Joined 2026-10-17"
    Decision quote;
  * the archived examples: `interpreter-trust-root-fallback.md:183`,
    `6912d526`, and the sweep's C8/C9 at `implementing` (`a516bcdc` to
    `636e3817`, with C1–C9 landed and C2 the constitution rewrite);
  * the fence count: 57 lines, 58 occurrences, 15 plans;
  * the tool: `board.py` reads headers only and runs no subprocess, its twin is
    byte-identical, and `TestTheBoardReadsHeadersAndJudgesNothing` exists.
* *Silent failure:* MA-1, MA-5 and MA-6.
* *Cross-document consistency:* `session-routines.md`, `PLANNING.md`, and the
  `plans.md` Mutability rule.
* *Lifecycle placement:* MA-3 and MA-6.
* *Satisfiers:* named in every finding.

**Not covered / low confidence.**

* No suite or fixture run, per the brief. The one board run was read-only, on
  the live tree.
* The LHM and modflow_tools trees were not read: their incidents and #13's
  replay are taken as the issues state them.
* A same-type reviewer: this review has no cross-type distance.
* The background-watcher exclusion was not weighed beyond agreeing it is out of
  scope.
