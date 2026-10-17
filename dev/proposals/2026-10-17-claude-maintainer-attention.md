# What waits on the Maintainer: one board view, one turn rule, and no work left in archived plans

**Author**: Claude (Strategy)
**Status**: awaiting-review
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
