# Verification practice: what a review reads, how it tests, what unplanned work runs

**Author**: Claude (Strategy)
**Status**: revising
**Review**: required(External)
**Plan review**: required(Internal) — the tier the derived plan will declare, decided here where the surface is still visible
**Opened**: 2026-10-17

## Context

**In plain terms.** Three open issues name gaps in how Cairn checks work. A
reviewer sharing the author's working folder can wipe the author's unsaved work
(#12). Reviewers miss one kind of bug because they read a change instead of
trying to break it (#17). The rule on how many tests to run makes a one-line fix
pay for the whole test suite (#25). Each fix is a few sentences. All three meet
in one place, the code review of a fix that has no plan, so one proposal covers
them.

* **Boundaries A, B, C** are the three verification steps in `AGENTS.md` >
  "Verification boundaries". A covers the tests an implementer runs while
  working, B is one recorded broad run before code review, and C is the code
  reviewer's own attempt to break the change ("falsification").
* **Mutation** means deliberately breaking one piece of code (deleting a line,
  restoring the old bug) and re-running the tests. If no test fails, the tests
  could not catch that break if it happened by accident. A mutation a test
  catches is *killed*; one no test catches *survives*. An **equivalent mutant**
  cannot change behaviour at all (deleting a line that has become redundant, for
  example), so it survives with nothing missing.
* A **set-completeness defect** is a value that must reach every member of a set
  of places in the code and reaches most of them. The missing place is a line
  that is not there, so a reader of the diff has nothing to see.

### #12 — a review on a shared working tree

A review is "commit-mediated" (`AGENTS.md:77-78`), and its basis block names a
`Reviewed commit:`. Nothing says the reviewer must work on that commit and not on
the shared folder, or must not write to it. Two events:

* **2026-08-18, `modflow_tools`.** An external-review session ran `git restore`
  and reverted 5 of the author's 6 uncommitted files, which were recovered from
  session context.
* **2026-08-05, here.** An implementation's suite figure counted 22 tests from a
  concurrent session's uncommitted file. A reviewer working in a detached
  worktree at the reviewed commit caught it
  (`dev/plans/archive/board-drain-guards.md:1223-1233`).

In the first, the reviewer wrote to the shared tree; in the second, evidence was
read from it. The 2026-08-25 triage folded #12 into the sweep's constitution
rewrite (C2: `9f0c6856`, `5be48c52`), which landed without the sentence. No
review rule in either `AGENTS.md`, `dev/agent_collaboration.md`, `doctrine/` or
the templates mentions a committed diff or a shared working tree.

### #17 — mutation as Boundary C's instrument

Boundary C says only what falsification is *not*: "copying Boundary B's broad
command is not a falsification ledger" (`AGENTS.md:214-216`). The issue reports
six set-completeness defects in one adopter plan, all found by mutating code or
listing call sites and none by reading a diff. Ten mutations restoring the bug
at once left the full suite at its identical pass count.

Cairn's own reviews already mutate, with no rule behind it:

* `dev/reviews/2026-10-17-code-review-engine-advice-defects.md`, row 10 and
  [EA2]: four legs of a fix survived mutation, because its tests pinned only one
  leg. Row 6 and [EA1] are a set-completeness defect, found by comparing the
  rendering sites: a strip step reaches the install and its lockfile check but
  not the review-copy renderer, and the same gap sits in a fourth site.
* `dev/plans/archive/adopter-path-consolidation.md:681`: restoring each deleted
  trigger turned the test red, against an unmutated control.

Both reviews ran every mutation in `git archive` extractions, off the working
tree (the review's line 11; the plan's line 649). That is #12's rule, practised
but unwritten.

The triage marked #17 superseded, expecting the Boundary bookkeeping to go once
the suite ran in about two minutes
(`dev/strategy/2026-08-21-claude-nimbleness-recovery.md:364-366`). The
boundaries stayed, and the suite took 692 s on 2026-10-16
(`dev/plans/archive/adopter-path-consolidation.md:519`). [EA1] and [EA2] meet the
triage's own condition for reopening: the same gap, seen in practice.

### #25 — Boundary A has no tier for work with no plan

Boundary A runs "the tests and probes the reviewed plan maps" and says "if a
substantive surface has no reviewed mapping, run the full suite"
(`AGENTS.md:188-190`, `templates/core/AGENTS.md:192-194`,
`doctrine/plans.md:291-293`). A **trivial-lane** change has no proposal, plan or
change note, only code, a test and one code review (`doctrine/lifecycle.md` >
"Three lanes"). Read literally, it always pays for the full suite, and its code
review pays again: Boundary C's first trigger is "no valid Boundary B record
exists", and that record lives in a plan. The section's opener says the opposite,
"do not pay for the same broad run at every one" (`AGENTS.md:186-187`).

Practice already departs from the text. The last two trivial-lane fixes ran
their engine test family, 429 and 329 tests (the `6894ed0c` and `f3c839a7`
commit bodies), and neither review ran the full suite.
`doctrine/lifecycle.md:52-58` already names the scope a defect repair needs, "the
touched surface's own test family", but Boundary A never points to it.
"Substantive surface" is defined nowhere, and `doctrine/plans.md` and both plan
templates say "substantive code surface".

**Counter-evidence.** In `2432bf86`, a template rewrite was verified against the
test files its author *expected* to pin it, and it missed ten failures pinned in
four other files. Choosing a scoped run by expectation is this tier's known
failure.

## Proposal

The proposal makes four edits, to both `AGENTS.md` copies and the doctrine behind
them. The quoted wording is the intent; the plan fixes the exact bytes.

**1. A review reads a commit, and never writes to a shared tree (#12).**

> A review reads a commit, never a shared working tree. The author commits what
> is to be reviewed before handing it over — locally; committing is not pushing
> — and the review names that commit. A reviewer sharing the author's working
> tree treats it as read-only: no edits, and no `restore`, `checkout`, `stash`,
> `reset` or `clean`. Anything that writes, such as a mutation or a scratch
> install, runs in a separate copy of the reviewed commit (a `git archive`
> extraction or a separate worktree). A figure is evidence only if it was
> measured on that commit's bytes.

Committing alone is not enough. An author who commits and keeps working has new
uncommitted files the moment the review starts, and the reviewer's half of the
rule is what protects them.

**2. Mutation for set-completeness, and an honest ledger (#17).**

> When a finding or claim says a value must reach every member of a set (every
> call site, every rendering path), list the set from the tree, not the diff,
> and mutate each member; reading the diff does not settle it. A mutation ledger
> reports each mutant as killed, survived or equivalent, beside an unmutated
> control run, and never as a bare "N of M killed". Equivalence is measured, not
> argued: a behaviour test through the real entry point passes under the
> mutation, and where another site is said to recover the value, mutating that
> site fails. Any equivalence that was not measured is reported as a survivor.

Outside that trigger, mutation stays the reviewer's choice.

**3. A tier for work with no plan (#25).**

> Trivial-lane work has no reviewed mapping by construction, so the fallback
> above does not apply. Run the tests that own each touched surface, found by
> searching for what imports or reads the touched files rather than by
> expectation, plus that surface's standing gates. State the scope, counts and
> interpreter in the commit body; that line is the record Boundary C checks.
> Run the full suite once, on the final commit, only if the change touches a
> contract or trust-ceremony surface (Boundary B's fence) or you cannot name the
> owning tests.

"Trust-ceremony" already covers every high-risk surface `AGENTS.md` names
(`doctrine/plans.md:314-316`). Boundary C gains one clause: for trivial-lane
work, the commit body's verification line is the record its first trigger asks
about. The six triggers stay six, and Boundary B does not change.

**4. One term (#25).** "Substantive surface" is defined once, as anything that is
not ordinary prose under the prose-only rule. That covers code, tests, executable
templates and snippets, fixtures, manifests, and prose a test or manifest pins.
`doctrine/plans.md` and both plan templates drop "code" from "substantive code
surface". The narrower phrase is wrong in exactly the `2432bf86` case: prose a
test pins.

## Rationale

**Each edit writes down a practice the record already shows working.** The
engine-advice review is the shared case: a trivial-lane review that needs a
record (#25), uses an instrument that edits source (#17), and ran it off the
shared tree (#12).

**Mutation does not make the reviewer "a second implementer"** (`AGENTS.md:73-75`).
It does not repeat the author's verification. It tests whether that
verification can fail, which is Boundary C's job.

**Item 3 keeps one full run where full weight belongs.** The risk posture keeps
full weight on high-risk surfaces (`doctrine/dual-review.md:124-128`), and
`2432bf86` shows that scoped runs miss pins. The full run moves from every
iteration to once, on the final commit, which is where Boundary B already pays
for it.

**The rules go in the shipped `AGENTS.md`, because adopters never receive
`doctrine/`.** `python bootstrap/scaffold.py --manifest` lists no path under
`doctrine/`, but it lists `AGENTS.md` and both templates. #12 and #17 came from
an adopter, and a rule kept only in doctrine never reaches that adopter's agent.

## Alternatives considered

* **#25 as drafted in the issue, ending "Boundary B still runs full before any
  code review".** That clause sends every trivial-lane fix back to a full run,
  which is the very cost the issue removes. I kept the issue's fence and dropped
  that clause.
* **The strongest rival for #25: the owning test family only, never a full
  run.** It is the cheapest option and matches what the last two engine fixes
  did. It loses on the risk posture and on `2432bf86`: on the scaffold engine, a
  missed pin reaches every adopter. See question 1.
* **Mutation for every claim that a test pins a fix.** This is stronger, and the
  security preflight's S2 already asks it of authors. It loses to the issue's own
  warning that "mutate everything" is worse than the status quo. The narrow
  trigger covers the class of defect that reading cannot see.
* **#12 by tooling** (a helper that extracts the reviewed commit, or a hook that
  refuses `git restore`). Not yet: build it if the two sentences fail in practice.
* **Do nothing.** #12 stays a live way to lose data, mutation ledgers stay
  unreported, and Boundary A keeps describing a practice nobody follows.

## Documentation / doctrine surface

The governing layer is edited in lockstep: `AGENTS.md` and
`templates/core/AGENTS.md`.

| Edit | Both `AGENTS.md` copies | Doctrine and templates |
|---|---|---|
| 1 | Review | `doctrine/dual-review.md` > "Asynchronous and commit-mediated" |
| 2 | Boundary C | `doctrine/dual-review.md` > "Boundary C"; the ledger shape in `doctrine/plans.md` > "Code review — doctrine" |
| 3 | Boundary A; one clause in C | `doctrine/plans.md` > "Boundary A" and "Boundary C" |
| 4 | Boundary A | `doctrine/plans.md` > "Boundary A"; one word in both plan templates |

Not touched: `doctrine/lifecycle.md` (it is already right, and Boundary A will
point to it), Boundary B, the six fresh-run triggers, and the security preflight.

### Doctrine-change rate-limit

**Applies.** #17 rests on **recurrence**: six instances in one adopter plan,
plus [EA1] and [EA2] here. #12 rests on **recurrence of one shape**: both times,
a shared working tree was treated as if it were the commit under review. If a
reviewer judges the two events too different to count, the fallback is the
Maintainer classifying #12 as a data-loss surface
(`doctrine/rationale.md:419-428`; question 3). #25 is **not incident-driven**:
it repairs a contradiction between the section's opener and its fallback.

## Evidence / verification plan

It works if the next trivial-lane fix and its review can follow the text
literally and do what `6894ed0c` and its review did, plus a full run where the
fence applies. It is falsified if a reader can still derive "run the full suite"
for a trivial fix on an ordinary surface, or if item 1 leaves a reviewer no
permitted way to mutate.

### Tests required

* `bootstrap/tests/test_verification_boundaries.py` passes **unedited**, so
  every phrase it pins survives.
* New pins, each with a guard showing it fails when its clause is removed, go in
  a **new** file: the existing one is frozen in
  `bootstrap/tests/fixtures/gate_manifest.json`, and editing it would queue a
  Maintainer re-anchor for nothing.
* Every test that reads a touched file, found by search (the `2432bf86` lesson).

### Examples / smoke checks

`python scripts/claim_check.py` on each edited file, `python scripts/check_cairn.py`,
and `python scripts/quality_gate.py --sub neutrality --sub redundancy` (no new hit
on an edited line). Boundary B mode is the plan's call; I recommend `full`, which
costs about 12 minutes and ends any argument over the shipped template.

#### Security preflight — five questions, answered in writing

N/A: no trust boundary added, moved, or widened.

## Signals the change is wrong

* A trivial-lane commit body names one test file for a change whose importers
  span several, or a code review finds a pin that the stated scope missed.
* Mutation ledgers grow long on changes that make no set-completeness claim.
* "Equivalent" appears in a ledger without the test that measured it.
* Reviewers stop probing altogether, because an isolated copy feels costly.

## Scope delta

**Scope delta**: preserved. This is the opening scope; nothing has been removed.

## Assurance path

**Assurance path**: high-assurance. The change edits `doctrine/` and a shipped
template, both mandatory triggers. It touches no executable, no trust root and
no install-contract artifact.

## Questions for the Maintainer

1. **Should a trivial-lane fix on a high-risk surface (the scaffold engine, for
   example) run the full suite once before its code review?** Recommended:
   **yes**, once, on the final commit; about 12 minutes here.
2. **Should mutation be required only for "this must reach every X"
   findings?** Recommended: **yes**; elsewhere it stays the reviewer's choice.
3. **Do you classify #12 as a data-loss surface?** Recommended: **yes**. A
   reverted, uncommitted file cannot be brought back with git, and the
   classification settles the rate-limit question either way.

## Review -- Claude Opus 5.5 (External, fresh session) -- 2026-10-17

```
Reviewed commit: 2065793187ce5558ab87e9192733c4488ecd394f
Target: the complete proposal (Context through Questions for the Maintainer), checked against issues #12, #17 and #25 and the tree at the reviewed commit
Prior findings: none
Assurance path: high-assurance
```

**Tier**: External
**Findings**: raised (3 blocking, 1 non-blocking)
**Verdict**: REVISE

Distance: a fresh session of the author's agent type, not a different type.

### In plain terms

All three parts should happen: each issue names a real gap, and each fix is a
few sentences. As written, though, two of the four edits would not do what they
say. Edit 1 forbids a reviewer to write anything in a shared folder, but writing
the review into the proposal file is a write, so every review would break the
rule as it began, this one included. Edit 3 tells the author of a small fix
which tests to run, but it leaves the next step still saying "no plan means the
full suite", and it never asks the code reviewer to check the author's choice
of tests. The one safeguard in edit 3, a full run when a fix touches risky code,
uses words the adopters' copy never defines. So for adopters, who are where #25
came from, the safeguard would never fire. Each of these takes a sentence or two
to fix.

### The proposal at its strongest

The three issues share one setting: a small fix with no plan, reviewed by a
second session in the same folder. There, nothing written stops the reviewer
from reverting the author's unsaved files (#12). The best tool for one class of
bug, deliberately breaking code to see whether a test notices, is practised but
unwritten (#17). And the test-scope rule, read literally, prices a three-line
fix at a twelve-minute full run that nobody performs (#25). The proposal writes
down what Cairn's recent reviews already do, and it puts the rules in the
`AGENTS.md` that adopters install, because they never receive `doctrine/`.

### Findings

#### [VP1] blocking — edit 1 forbids the review it governs

**Plain.** The new rule says a reviewer in a shared folder makes "no edits".
But a Cairn review *is* an edit: a section appended to the proposal or plan in
that folder, then committed. Read literally, no review could be recorded in a
shared folder. A rule that every reviewer breaks on first use teaches reviewers
to treat it as advice. The half that would wear away first is the half that
prevents data loss.

**Precision.** `AGENTS.md:77-78` and `doctrine/dual-review.md` > "Asynchronous
and commit-mediated" define a review as an appended, committed section.
`dev/agent_collaboration.md:114` tells a session on a shared worktree to claim
files before editing them, which assumes it edits there. Item 1's "anything
that writes ... runs in a separate copy" would move the review itself into a
separate worktree. That review's commit would then have to reach the shared
branch, and the proposal describes no step for that. The proposal's falsifier,
"no permitted way to mutate", is the narrow case. The wide case is no permitted
way to record the review.

**Closes when** item 1 names the one write a reviewer does make in the shared
tree: appending its own section, or creating its own review file, claimed first
and committed by explicit path. Everything else stays out, as drafted.

#### [VP2] blocking — edit 3 fixes the first step and leaves the next two saying the opposite

**Plain.** The new tier tells the author of a small fix to run the tests that
own the touched code. But Boundary B, the next step, is left unchanged, and it
still says that without a plan the full suite runs. So a reader can still derive
"run the full suite" for any small fix, which is the proposal's own falsifier.
And Boundary C, the code reviewer's step, is never told to challenge the
author's choice of tests. The author picks the tests, runs them and vouches for
them, and nobody checks the choice. That is the failure `2432bf86`, the
proposal's own counter-evidence, describes.

**Precision.**

* *Boundary B.* Its opener names no lane: "after the final implementation
  commit and before code review". A trivial-lane fix has both. Its default is
  the full suite, and "if a substantive surface has no reviewed mapping ... the
  full suite runs" (`AGENTS.md:197-199`). Item 3 says trivial-lane work "has no
  reviewed mapping by construction". The proposal says "Boundary B does not
  change", and it also says the fenced full run happens "where Boundary B
  already pays for it". With B unchanged, that second sentence yields a full
  run on every trivial fix. The issue's scope guard protects B's refusal
  triggers. Saying which work B governs moves none of them.
* *Boundary C.* A bounded (less-than-full) scope is acceptable today because
  someone else rules on it. Boundary C records `**Bounding**: ACCEPTED | FULL
  RUN REQUIRED` after challenging a named surface or test
  (`AGENTS.md:217-219`). `doctrine/plans.md:326-328` gives the reason: the
  implementer chooses the scope and captures the saving. Item 3 makes the
  commit-body line "the record" that C's first trigger asks about. It does not
  say that line is a bounded record that takes the Bounding verdict. The record
  shows why the files must be named. `f3c839a7`'s body names its seven test
  files, and its review reproduced the count, 329 against 329 (`bab80098`).
  `6894ed0c`'s body says only "engine family (11 files) 429 passed". Its
  review's own 11-file run counted 286, of which 285 passed and 1 failed
  (`dev/reviews/2026-10-17-code-review-engine-advice-defects.md:46`). The
  record cannot reconcile the two figures, and the review does not mention the
  gap.

**Closes when** the text the plan will fix does two things. (a) Boundary B says
which work it governs, so that the trivial-lane line replaces B and does not add
to it. (b) The commit-body line names test files or nodes, not only counts, and
is a bounded record on which Boundary C records the Bounding verdict. Each is
one clause, and the six triggers stay six.

#### [VP3] blocking — the full-run safeguard is written in words adopters never receive

**Plain.** Edit 3's safeguard is a full run when a fix touches "a contract or
trust-ceremony surface (Boundary B's fence)". In the `AGENTS.md` adopters
install, the contract list names Cairn's own installer files, which an
adopter's project does not have. "Trust-ceremony surface" is never defined
there. Its meaning, any high-risk surface the governing file names, lives only
in `doctrine/plans.md:313-315`. "Trivial lane" is defined only in
`doctrine/lifecycle.md`. So for an adopter the safeguard matches nothing. Edit 3
then becomes the option the proposal rejected: owning tests only, never a full
run. The proposal gives its reason for shipping in `AGENTS.md`: a rule kept only
in doctrine never reaches the adopter's agent. That reason applies to the
definitions its own rule depends on.

**Precision.** `templates/core/AGENTS.md:204-206` lists the install contract,
the fidelity and gate manifests, the lockfile schema and `scaffold.py
--manifest`, then names "**trust-ceremony surface**" without defining it.
Neither `AGENTS.md` copy defines it anywhere. The shipped word for small work is
"a trivial change" (`templates/core/dev/proposals/_template.md:6-8`), and no
shipped file names lanes or the defect-repair carve-out. An adopter does have
high-risk surfaces: it names them in the project-conventions slot
(`templates/core/AGENTS.md:334-336`). But nothing links "trust-ceremony" to
that slot. The recommended "yes" to Question 1 would therefore bind Cairn, and
not the adopters #25 came from.

**Closes when** item 3's shipped wording states the safeguard in terms the
installed file defines, such as "a contract surface, or any high-risk surface
this file names". It should also name the work it covers in shipped words: "a
trivial change, with no proposal or plan".

#### [VP4] non-blocking — two supports are stretched; rest the case on what holds

**Plain.** The case for #17 and #12 is sound, but two supports are weaker than
stated, and one bears on Question 3. The review *found* EA1 and EA2, so they
show the practice working without a rule, not a reviewer missing the defect.
EA2 is also a different kind of gap: tests that pinned one of four parts of a
fix, not a value missing from one place. And the two #12 events differ: one
destroyed files by writing, the other miscounted tests by reading. In the one
data-loss event, the files were recovered.

**Precision.** The triage's condition for reopening #17 was that the new review
form "shows the same set-completeness gap in practice" (issue #17, first
comment). The proposal's other basis holds by itself: the premise failed. The
boundaries stayed, and the suite takes 692 s, against the sweep's accepted
target of about 2 minutes
(`dev/proposals/archive/2026-08-25-claude-subtraction-sweep.md:95`). For #12,
`doctrine/rationale.md:426-428` sets the data-loss bar at work that "can't be
rebuilt". The class meets it, because git cannot bring back an uncommitted file
that it reverted. The one event did not meet it, because the files were rebuilt
from session context.

**Closes when** the Response rests #17's reopening on the failed premise and
counts EA2 as mutation evidence, not as a set-completeness instance. Question 3
should ask about classifying the class, and say that the one event was
recovered.

### Should this happen at all

Yes. Each part answers a gap with a source, and the cost is a few sentences of
governing text. Items 2 and 4 are ready. Item 1 needs one carve-out (VP1).
Item 3 needs VP2 and VP3. If the Response cannot close item 3 cleanly, split it
off rather than hold #12, the only part that guards against data loss.

### The strongest rejected alternative

**Extend Boundary B's bounded mode to work with no plan, instead of building a
new tier in Boundary A.** Cairn already has one way to run less than the full
suite: a bounded Boundary B record. It is refused on contract and
trust-ceremony surfaces, ruled on by Boundary C's Bounding verdict, and pinned
by `test_bounded_boundary_b_contract_reaches_every_surface` and
`test_boundary_c_adjudicates_a_bounded_record` in
`bootstrap/tests/test_verification_boundaries.py`. One sentence, "work with no
plan records its bounded scope in the commit body", would give the trivial lane
all of it: the fence, the reviewer's challenge and the six triggers. There would
be no second definition of scope to drift away from the first. Item 3 instead
builds a parallel scope rule with its own fence and its own record, and then
needs VP2's two clauses to reconnect it. The alternative's cost is that it
amends Boundary B's text, which the issue asked to leave alone, and a bounded
record runs a few lines longer than a commit-body line. I would choose it. If
the proposal keeps its own design and closes VP2, the two designs converge.

The proposal should also name and dismiss one more alternative: hit the sweep's
accepted 2-minute suite target, which would dissolve #25 for Cairn. That loses,
because #25 is about an adopter's suite cost (LHM's "multi-thousand-test
suite"), which Cairn's suite speed does not touch. The proposal should say so.

### What would falsify the central claim

The central claim is that these edits write down a practice that already works,
and lose no safety.

* **Item 3's safety.** Take the recent trivial-lane commits (`f3c839a7`,
  `6894ed0c` and its follow-up `223f6b40`). Apply item 3's search rule to name
  the owning tests, then run the full suite once at each commit. A failure
  outside the searched set falsifies "searching for importers and readers finds
  the owning tests". It costs about twelve minutes a commit, the run is the
  author's, and it is the evidence I would most want before the Decision.
* **Item 1.** A review that, following the text, cannot record itself. As
  worded, this is already met (VP1).
* **Item 2.** A set-completeness defect, a value that reaches most of the places
  it must but not all, that ships past a review in which no finding or claim
  named the set. The trigger fires only once someone names the set. If the
  costly defects are the ones nobody named, listing the set has to fire on the
  change itself, whenever a fix touches one member of a set.

### Claims checked

These hold at the reviewed commit:

* `scaffold.py --manifest` (run read-only) lists no `doctrine/` path, and it
  does list `AGENTS.md` and both templates.
* The 692 s figure is in the 2026-10-16 Boundary B record.
* The quoted lines in `AGENTS.md`, `templates/core/AGENTS.md` and
  `doctrine/plans.md` are as quoted, and so are the cited lines in
  `doctrine/lifecycle.md`, `doctrine/dual-review.md` and
  `doctrine/rationale.md`.
* The test file is in the gate manifest's `frozen_files`.
* The 429 and 329 figures match the commit bodies, and neither review ran the
  full suite.
* The C2 commits contain no shared-working-tree sentence.

Two qualifications: VP4, and VP2's 429-against-286 mismatch.

### Not covered

I ran no tests and no mutations, and I did not open the plan-template lines that
item 4 will edit beyond confirming the phrase.
