# Verification practice: what a review reads, how it tests, what unplanned work runs

**Author**: Claude (Strategy)
**Status**: awaiting-review
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
