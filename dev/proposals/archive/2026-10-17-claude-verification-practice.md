# Verification practice: what a review reads, how it tests, what unplanned work runs

**Author**: Claude (Strategy)
**Status**: accepted
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

* `dev/plans/archive/2026-10-17-code-review-engine-advice-defects.md`, row 10 and
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
  (`dev/plans/archive/2026-10-17-code-review-engine-advice-defects.md:46`). The
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

## Response -- Claude (author) -- 2026-10-17

All four findings are accepted. VP2 is closed by adopting the review's strongest
rejected alternative. Revision 1 below carries the complete current contract.

* **[VP1] accepted.** Item 1 now names the one write a reviewer makes in a shared
  tree: its own review record, appended to the artifact or created as its own
  review file, claimed first and committed by explicit path. Everything else that
  writes stays in a separate copy, as drafted.
* **[VP2] accepted, by adopting the alternative.** Item 3 no longer builds a
  parallel tier in Boundary A. Instead, Boundary B's bounded mode reaches a
  trivial change. B says it governs every implementation, a trivial change
  included; a trivial change's mapping is its owning tests, and its record is its
  commit body. The bounded record names test files or nodes, not only counts.
  Boundary C then needs no new clause: its record check, its Bounding verdict
  and its six triggers apply as written. The 429-against-286 gap (`6894ed0c`) is
  why the record names files.
* **[VP3] accepted.** The fence is now written in words the installed file
  defines. Both `AGENTS.md` copies define a trust-ceremony surface as "any
  high-risk surface this file names, or release or security ceremony work". The
  work covered is named "a trivial change, with no proposal or plan", the shipped
  proposal template's word for it; no shipped template mentions change notes.
  Defining the term in Boundary B also repairs B's fence for an adopter's
  *planned* work, which until now named a surface the adopter's file never
  defined.
* **[VP4] accepted.** #17's reopening now rests on the failed premise. The
  sweep's accepted target was an inner loop of about two minutes
  (`dev/proposals/archive/2026-08-25-claude-subtraction-sweep.md:95`), and the
  full suite the boundaries price took 692 s. [EA1] and [EA2] show the practice
  working without a rule, and [EA2] is mutation evidence, not a set-completeness
  instance. For #12, the one data-loss event was recovered, so question 3 now
  asks about the class.

**Why the alternative wins.** Cairn already has one way to run less than the
full suite, and it is fenced, adjudicated and pinned.
`test_bounded_boundary_b_contract_reaches_every_surface` guards its fence and
mode field on five surfaces, and `test_boundary_c_adjudicates_a_bounded_record`
guards the reviewer's verdict on three. A second scope rule would be one more
thing to drift. The opening left B untouched because the issue's scope guard
asked it to. That guard protects B's refusal triggers and "uncertainty resolves
to full", and neither moves. B gains a statement of which work it governs and a
definition of a term it already used. Its default stays `full`. The cost is a
commit body about three lines longer.

**One more alternative, dismissed: reach the sweep's two-minute target.** That
would dissolve #25 for Cairn only. #25 is about an adopter's suite (LHM's
"multi-thousand-test suite"), and Cairn's suite speed does not touch it.

**Falsification evidence, measured for this Response.**

* *The search rule, against its own counterexample.* At `2432bf86^`, searching
  `bootstrap/tests/*.py` for readers of the touched files (`AGENTS.md`, the
  proposal and plan templates) returns 42 of 121 test files. They include all
  seven files the repair named, among them the five its author had missed, so
  the rule would have caught the miss. The cost shows too: for a governing file,
  the owning set is wide.
* *The full suite after the recent trivial changes.* The run was at
  `396e001b`, after `f3c839a7`, `6894ed0c`, `223f6b40` and the AST re-anchor.
  Run in a `git archive` extraction under Python 3.13.13, it took 660 s and
  gave 3,201 passed, 17 failed and 18 errors, out of 3,236. I reran those 35
  nodes in a clone at the same commit, with the gate anchor fetched, and 34
  passed; they need a git repository, which an extraction lacks. The last one,
  `bootstrap/tests/test_replacement_tools.py::TestTheBoardReadsHeadersAndJudgesNothing::test_it_lists_the_active_artifacts`,
  failed because nothing was in flight at that commit. It is a test defect that
  `4edd7778` has since fixed, and none of the three changes caused it. So at
  these commits the scoped runs missed nothing, and the claim survives one test.
  The run does not show that the search rule picks the same sets the authors
  picked.

**The `check_cairn` flag at line 64 is harmless, and this Response exempts it.**
The flagged line continues a list item: "row 10 and" / "[EA2]: four legs …".
`link_check`'s `_REFDEF_RE` (`scripts/link_check.py:76`) reads any line that
begins `[label]:` as a link definition, so it sees a link to `four`. CommonMark
does not, because a link definition cannot interrupt a paragraph. Measured with
`markdown-it-py` 4.0.0: a valid definition on its own line registers
(`{'EA2': {'href': 'four'}}`), while the same text wrapped inside a list item
registers nothing and renders as text. The earlier section is not edited.
Instead, the directive below exempts that one target, and no new line in this
Response or the revision begins with `[label]:`.

<!-- link-check-allow: four -->

**Scope.** This revision does not widen scope. Every change answers a finding.
The one move beyond the opening text, amending Boundary B, is the review's own
named alternative and the satisfier for VP2(a). The status therefore moves to
`awaiting-decision`.

## Revision 1 -- Claude -- 2026-10-17 -- the complete current contract

The opening **Context** stands, with the VP4 corrections recorded in the ledger
at the end. Everything below replaces the opening's contract sections.

### Proposal

Four edits, made to both `AGENTS.md` copies in lockstep and to the doctrine
behind them. The quoted wording is the intent; the plan fixes the bytes.

**1. A review reads a commit (#12).** Added to the Review section and to
`doctrine/dual-review.md` > "Asynchronous and commit-mediated":

> A review reads a commit, never a shared working tree. The author commits what
> is to be reviewed before handing it over (locally; committing is not pushing),
> and the review names that commit. In a working tree it shares with an author,
> a reviewer makes one write: its own review record, appended to the artifact or
> created as its own review file, claimed first and committed by explicit path.
> Nothing else: no other edits, and no `restore`, `checkout`, `stash`, `reset`
> or `clean`. Anything else that writes, such as a mutation or a scratch
> install, runs in a separate copy of the reviewed commit (a `git archive`
> extraction or a separate worktree). A figure is evidence only if it was
> measured on that commit's bytes.

**2. Mutation for set-completeness, and an honest ledger (#17).** This item is
unchanged from the opening. It is added to Boundary C and to
`doctrine/dual-review.md` > "Boundary C", and the ledger rule also goes into the
ledger shape in `doctrine/plans.md` > "Code review — doctrine".

> When a finding or claim says a value must reach every member of a set (every
> call site, every rendering path), list the set from the tree, not the diff,
> and mutate each member; reading the diff does not settle it. A mutation ledger
> reports each mutant as killed, survived or equivalent, beside an unmutated
> control run, never as a bare "N of M killed". Equivalence is measured, not
> argued: a behaviour test through the real entry point passes under the
> mutation, and where another site is said to recover the value, mutating that
> site fails. Any equivalence that was not measured is reported as a survivor.

Outside that trigger, mutation stays the reviewer's choice.

**3. Boundary B's bounded mode reaches a trivial change (#25).** In Boundary A,
in both copies and in `doctrine/plans.md`:

> Run the tests and probes the reviewed plan maps — or, for a trivial change,
> with no proposal or plan, the tests that own each touched surface, found by
> searching for what imports or reads the touched files rather than by
> expectation — plus standing gates for every touched surface. If a substantive
> surface has no such mapping, run the full suite.

In Boundary B, in the same three places:

> Boundary B governs every implementation, a trivial change included. A trivial
> change's mapping is the owning tests Boundary A names, and Boundary C's
> Bounding verdict reviews it afterwards. Its record is its commit body,
> measured on exactly the bytes being committed: a tree clean apart from the
> change, or a separate copy holding only it.

B's existing text takes three further edits:

* "Unless the plan's reviewed mapping bounds" becomes "unless the mapping
  bounds", so the clause covers both kinds of work. The pinned token is only
  "bounds the change's effects confidently".
* On `bounded`, the record names "the test files or nodes and the gates run,
  with counts".
* The fence's "**trust-ceremony surface**" is defined in place as "any
  high-risk surface this file names, or release or security ceremony work".

B's default (`full`), its refusal, "uncertainty resolves to `full`" and every
pinned phrase stay as they are. In `doctrine/dual-review.md` > "Boundary C",
the opening "for a plan with a valid Boundary B ... record" becomes "for work
with a valid Boundary B record (a plan's Implementation verification section,
or a trivial change's commit body)". Boundary C's rule, its Bounding verdict and
its six triggers do not change.

**4. One term (#25).** Unchanged from the opening. "Substantive surface" means
anything that is not ordinary prose under the prose-only rule: code, tests,
executable templates and snippets, fixtures, manifests, and prose a test or
manifest pins. `doctrine/plans.md` and both plan templates drop "code" from
"substantive code surface".

### Rationale

* **Each edit writes down a practice the record already shows working.** The
  engine-advice review is the shared case: the review of a trivial change that
  needs a record (#25), using an instrument that edits source (#17), run off the
  shared tree (#12).
* **There is one scope mechanism, not two.** A trivial change takes the bounded
  path plans already take: one fence, one record, one independent verdict, all
  already pinned. On a high-risk surface, bounded mode refuses, so the change
  runs the full suite once. That fits the risk posture
  (`doctrine/dual-review.md:124-128`) and the lesson of `2432bf86`.
* **Mutation is not re-running the author's verification** (`AGENTS.md:73-75`).
  It tests whether that verification can fail, which is Boundary C's job.
* **Every rule, and every term it depends on, ships in `AGENTS.md`.** Adopters
  never receive `doctrine/`: `python bootstrap/scaffold.py --manifest` lists no
  path under it.

### Alternatives considered

* **A parallel no-plan tier in Boundary A** (the opening's design). Rejected,
  because it needed its own fence and record, and then two clauses (VP2) to
  reconnect them to B and C.
* **Owning tests only, never a full run.** The cheapest option, and what the
  last two engine fixes did. Rejected on the risk posture and on `2432bf86`: on
  a high-risk surface, a missed pin reaches every adopter.
* **Reach the two-minute suite target.** Rejected: it fixes Cairn's cost, not an
  adopter's, and #25 came from an adopter.
* **Mutation for every claim that a test pins a fix.** Rejected on the issue's
  own warning that "mutate everything" is worse than the status quo.
* **#12 by tooling** (a helper that extracts the commit, or a hook that refuses
  `git restore`). Deferred: build it if the rule fails in practice.
* **Do nothing.** #12 stays a live way to lose work, mutation ledgers stay
  unreported, and Boundary A keeps prescribing a practice nobody follows.

### Documentation / doctrine surface

| Edit | Both `AGENTS.md` copies | Doctrine and templates |
|---|---|---|
| 1 | Review | `doctrine/dual-review.md` > "Asynchronous and commit-mediated" |
| 2 | Boundary C | `doctrine/dual-review.md` > "Boundary C"; `doctrine/plans.md` > "Code review — doctrine" |
| 3 | Boundaries A and B | `doctrine/plans.md` > "Boundary A" and "Boundary B"; one sentence of `doctrine/dual-review.md` > "Boundary C" |
| 4 | Boundary A | `doctrine/plans.md` > "Boundary A"; one word in both plan templates |

Not touched: `doctrine/lifecycle.md`, Boundary B's fence list and refusal rule,
the six fresh-run triggers, and the security preflight.

### Doctrine-change rate-limit

**Applies.** Each item's ground:

* **#17 rests on recurrence**: six instances of one shape in one adopter plan,
  across five review rounds.
* **#12 rests on the Maintainer classifying the class as a data-loss surface**
  (`doctrine/rationale.md:419-428`; question 3). Git cannot bring back an
  uncommitted file it reverted. The one event (2026-08-18) was recovered from
  session context. A second event (2026-08-05, evidence read from a shared
  tree) has the same root but lost no work.
* **#25 is not incident-driven.** It repairs a contradiction between the
  section's opener and its fallback.

### Evidence / verification plan

It works if the next trivial change and its review can follow the text
literally and end up where `6894ed0c` and its review did, with a record that
names files and carries a Bounding verdict. It is falsified if a reader can
still derive "run the full suite" for a trivial change on an ordinary surface,
if an adopter's file leaves the fence undefined, or if a review that follows
item 1 cannot record itself.

#### Tests required

* `bootstrap/tests/test_verification_boundaries.py` must pass **unedited**. Its
  bounded-mode pins keep guarding the fence and the mode field on all five
  surfaces.
* New pins go in a **new** file, because the existing one is frozen in
  `bootstrap/tests/fixtures/gate_manifest.json`. Each pin comes with a guard
  showing it fails when its clause is removed. The pins check that both
  `AGENTS.md` copies carry:
  * the review-reads-a-commit rule, with its one-write carve-out;
  * the ledger clause;
  * B's reach to a trivial change;
  * the trust-ceremony definition;
  * the "substantive surface" definition.
* Every test that reads a touched file, found by search.

#### Examples / smoke checks

Run `python scripts/claim_check.py` on each edited file, then
`python scripts/check_cairn.py`, then
`python scripts/quality_gate.py --sub neutrality --sub redundancy` (no new hit
on an edited line). Boundary B: `full`.

#### Security preflight

N/A: no trust boundary added, moved, or widened.

### Signals the change is wrong

* A trivial change's record names one test file for a change whose readers span
  several, or a review finds a pin the record missed.
* A set-completeness defect ships past a review in which nobody named the set.
  The trigger would then have to fire on the change itself.
* Mutation ledgers grow long on changes that make no set-completeness claim, or
  "equivalent" appears without the test that measured it.
* Reviewers stop probing, because an isolated copy feels costly.

### Scope delta

**Scope delta**: preserved. Every outcome the opening committed to is still
delivered; item 3 now reaches its outcome through Boundary B rather than a new
tier.

### Assurance path

**Assurance path**: high-assurance. The change edits `doctrine/` and a shipped
template. It touches no executable, no trust root and no install-contract
artifact.

### Questions for the Maintainer

1. **A trivial change on a high-risk surface runs the full suite once, before
   its code review. Agreed?** Recommended: **yes**. Here that takes about 12
   minutes. An adopter runs their own suite, and only on contract surfaces and
   the surfaces they named as high-risk.
2. **Mutation is required only when a finding or claim names a set. Agreed?**
   Recommended: **yes**; elsewhere it stays the reviewer's choice.
3. **Do you classify the class "a reviewer's write reverts uncommitted work in a
   shared tree" as a data-loss surface?** Recommended: **yes**. The one incident
   behind #12 was recovered from session context, so the classification rests on
   the class, not on a loss that happened. Without it, item 1 waits for a second
   event, and items 2 to 4 land without it.

### Withdrawn / superseded commitments

* The parallel no-plan tier in Boundary A, with its own fence and record. It is
  superseded by item 3 (VP2).
* "Boundary C gains one clause: for trivial-lane work, the commit body's
  verification line is the record". Superseded: the commit body is now a
  Boundary B record (VP2).
* "Boundary B does not change". Withdrawn: B now states which work it governs,
  names where a trivial change's record goes, lists test files or nodes, and
  defines a trust-ceremony surface (VP2, VP3).
* Item 1's unqualified "no edits". Replaced by the one-write carve-out (VP1).
* The shipped use of "trivial lane". Replaced by "a trivial change, with no
  proposal or plan" (VP3).
* Context: "[EA1] and [EA2] meet the triage's own condition for reopening".
  Withdrawn; the reopening rests on the failed premise (VP4).
* Context: [EA2] as set-completeness evidence. Corrected to mutation evidence;
  [EA1] alone is a set-completeness instance (VP4).
* Rate-limit: #12 as "recurrence of one shape". Demoted; #12 now rests on
  question 3 (VP4).

## Decision -- Anthony Kendall (Maintainer) -- 2026-10-18

**ACCEPTED.** The Maintainer's authorization, quoted **verbatim and visually
isolated**:

> "Accept A, B, C and D as revised, with every recommended answer, including B’s scope cut and D’s scope delta."

*Scribe's note, separate from the quoted words.* The four proposals of
2026-10-17 were put to the Maintainer as one batch, labelled A
(verification practice), B (Maintainer attention), C (neutrality and upgrade
slots) and D (independent scientific check). This proposal is **A**.
"Every recommended answer" means the recommended default of each question in
its newest revision, as put to the Maintainer:

* **Revision 1 binds.**
* **Q1 -- yes.** A trivial change on a high-risk surface runs the full suite
  once, before its code review.
* **Q2 -- yes.** Mutation is required only when a finding or claim names a
  set; elsewhere it stays the reviewer's choice.
* **Q3 -- yes.** The class "a reviewer's write reverts uncommitted work in a
  shared tree" is classified as a data-loss surface. The one incident behind
  #12 was recovered, so the classification rests on the class. Item 1 lands
  with the rest.
* **`Plan review: required(Internal)`** is ratified as declared.

Scribed by Claude (claude-opus-5-5) on the Maintainer's explicit instruction.
Nothing else lands in this commit.
