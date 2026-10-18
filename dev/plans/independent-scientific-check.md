# Plan: independent scientific check — one check per scientific change, shown able to fail

**Source proposal**: `dev/proposals/archive/2026-10-17-claude-independent-scientific-check.md`
**Status**: awaiting-plan-review
**Plan review**: required(Internal)
**Assurance path**: high-assurance — inherited: the change edits the authoring templates and the axis prose that adopters' bootstrap reads.
**Opened**: 2026-10-18

Proposed paths:
- `bootstrap/tests/test_scientific_check_guidance_ships.py`

External-repo paths:
- `dev/proposals/archive/2026-08-27-claude-stor-modflow-flopy-layer.md`
- `dev/proposals/2026-08-27-claude-stor-modflow-flopy-layer.md`
- `dev/plans/archive/stor-modflow-correctness.md`
- `dev/plans/archive/2026-10-01-claude-assemble-part-a.md`

## In brief

**The problem.** Code, tests and reviewers can all agree and all be wrong about
the world. A recharge array in inches per year, in a model built in feet and
days, still closes its water budget, because the solver balances whatever it is
given. A stream–aquifer exchange with its sign reversed passes a test written
from the same reading of the convention. Agreement between agents shows the
work is consistent, not that it is correct. What breaks the tie is an expected
value that does not come from the code under review.

**What this plan puts in place.** When a proposal changes a scientific
assumption, or a result the project publishes or acts on, its template asks for
**one independent scientific check** and four short answers about it:

1. **What it compares**: the quantity, the expected value, the tolerance and
   where the tolerance comes from, and whether the data behind the expected
   value is actually in hand and has been looked at.
2. **Why the expected value is independent**: neither the code nor a test
   written from the same understanding computes it. The basis is one of five:
   an analytical or manufactured solution; a conservation law chosen against
   the error this change risks; a trusted observation; an independent
   implementation or the model's own saved output; a domain expert's
   expectation written down before the result is seen.
3. **The error it would catch**: the plausible mistake (a reversed sign, a unit
   slip, a missed warm-up) under which the check fails. At implementation, the
   implementer makes that mistake on purpose and records the failing output.
4. **When the result is "no effect"** *(added at the Maintainer's instruction;
   see Scope)*: a check that finds no change is evidence only if it could have
   found one. The analysis must first detect a known effect of the size that
   matters (a **positive control**: the same analysis run on a case where the
   answer is known to be non-zero), or say plainly that it cannot.

The plan template then says the check is accepted scope. If it has to be
replaced, the replacement must fail under the same error. If nothing qualifies,
dropping it is a scope reduction that needs the Maintainer's quoted allowance.
"The result now rests on the implementation" does not settle it.

**Why this is worth a plan.** Twice in LHM a check could not fail under the error
that mattered. In the first case a structural review caught the resulting drift
later, and at higher cost, than the lost check would have. Separately, the
`dimensions/` pages promise a "scientific-trust review lens" that no module
installs. This plan repoints those three sentences at the check, which every
adopter does receive.

**What it does not do.** No `doctrine/` edit, no new axis, no engine change, no
new review round, and no planted-error scheme. The rule carries no doctrine
weight; it is template guidance. The doctrine sentence waits on the board.

**Order of work.** First, before any file changes, the wording is tried on two
past LHM plans. If it would have helped on neither, the plan stops and the
Maintainer decides. Then the proposal template, the plan template, the three
promise sentences, and last one full test run.

**What the Maintainer does.** Nothing now. At the end, the gate-manifest
re-anchor you already have queued gains one new test.

## Source proposal

Accepted 2026-10-18 at `019d2bbc`. **Revision 1 binds**, with every recommended
answer:

* **Q1 yes.** The check lands as template guidance. The lens-8 doctrine
  sentence is deferred; its board row is in `dev/PLANNING.md` (deposited at
  `07bd9950`).
* **Q2 yes.** A gated paragraph in an existing template is outside the guide
  star's "before any further expansion" gate.
* **Q3 yes.** Issue #18 is closed as a duplicate of #19, not as met. This was
  done on 2026-10-18 (state `CLOSED`, a comment quoting Q3, read with `gh issue
  view 18` before this plan opened). #19 stays open. #18's export-safety
  affirmation stays the Maintainer's to sign, and this plan does not touch it.
* **Q4 yes.** The `deliverable` axis is revisited when the third-party probe
  row moves, or at the Maintainer's call once about ten real checks exist.
* **`Plan review: required(Internal)`** is ratified as declared.

The lens-8 sentence in `doctrine/dual-review.md` is not in this plan's baseline.

## Scope

**Touched.**

* `templates/core/dev/proposals/_template.md` and its twin
  `dev/proposals/_template.md`: one new H3 block, *Independent scientific
  check*, between the security preflight and *Signals the change is wrong*.
* `templates/core/dev/plans/_template.md` and its twin
  `dev/plans/_template.md`: one paragraph in *Acceptance criteria*.
* `dimensions/complexity.md` (the Complex position), `dimensions/README.md` (the
  Complexity row of the axis table) and `bootstrap/BOOTSTRAP.md` (the I-2
  paragraph): one sentence each, repointed at the check.
* One new test file, `bootstrap/tests/test_scientific_check_guidance_ships.py`,
  holding **one** test (C2, extended in C3).
* This plan: the C1 record and the Boundary B record are appended to it.
* At archive only (see *Dispositions*): the guide star's open-gap entry,
  `CHANGELOG.md`, and two rows of `dev/PLANNING.md`.

**Documentation / doctrine surface.** Governing layer: the two template pairs,
which are what actually binds an adopter. Prose: one axis position, one matrix
row, one bootstrap sentence. **No doctrine surface**: nothing under `doctrine/`
is edited, so no doctrine copy has to be kept in step. The templates carry no
doctrine weight and the `dimensions/` edit corrects a claim to match what ships,
so the doctrine rate-limit gate is not the route; if a reviewer thinks it
reaches the `dimensions/` edit, the Decision ratified the proposal's argument
from recurrence (two occurrences in LHM's plan records). Descriptive layer: none.

**Added at the Maintainer's instruction: the positive control for "no effect"
results.** Relayed by the coordinating agent on 2026-10-18. The Maintainer's
words, verbatim:

> "Pass the positive control point yes, let's not do planted errors."

*Scribe's note, separate from the quoted words.* The first half adds one bullet
to the proposal-template block and one clause to its reviewer paragraph (C2). The
second half, "planted errors", names a separate idea that no artifact takes up,
so it is out of scope here. This is an **addition** to the accepted scope, not a
removal; it owes no disposition, and it is recorded in *Scope delta* as an
addition. It has no occurred incident behind it, so, like the independent-basis
half of the block, it rests on argument: AGENTS.md already says "Confirm the
instrument before trusting an absence" for Cairn's own tooling, and this carries
the same rule into a scientific result.

**Not touched**, each to be checked by `git diff --stat` over the implementation
range:

* `doctrine/` (including lens 8 in `doctrine/dual-review.md`), both `AGENTS.md`
  copies, `templates/modules/` (including the `dual-review` module), and
  `docs/`.
* `bootstrap/_scaffold/`, `bootstrap/verify_integrity.py`, `scripts/` and
  `tools/`.
* Every existing test file, including the frozen ones that read these
  templates.
* No axis, axis value, or gate-table row changes (`dimensions/` tables,
  `bootstrap/BOOTSTRAP.md` I-4 and I-5).
* `dev/.cairn/cairn-lock.yml` and `dev/.cairn/base/`.

### Frozen files, AST, lockfile, install contract

**Frozen files: none edited.** *Frozen* means listed under `frozen_files` in
`bootstrap/tests/fixtures/gate_manifest.json`, the set `test_gate_manifest.py`
reads (183 keys at `7f1bcdf0` and at `b16f4607`). Measured: none of the 11 files
this plan edits or creates is a key. The instrument was checked against a known
key (`bootstrap/tests/test_scaffold.py` returns true). Frozen files that **read**
these surfaces and are **not edited**: `test_scaffold.py`,
`test_scope_reduction_trap.py`, `test_verification_boundaries.py`,
`test_documentation_plan_module.py`, `test_claim_check_module.py`,
`test_core_dev_folders.py`, `test_quickstart_sequence.py`,
`test_profile_grammar.py`. The new test file adds one node to the pinned
collection (recorded as an addition, not held), so it joins the gate-manifest
re-anchor already queued on `dev/PLANNING.md`. **The re-anchor is
Maintainer-only and supervised; an implementing agent must not perform it.**
Because no frozen file changes, `dev/PLANNING.md` is not edited when this plan
opens; the node note is the archive commit's (chunk M).

**AST: no engine symbol changes.** No file under `bootstrap/_scaffold/` is
edited. The AST attestation baseline (`bootstrap/tests/fixtures/scaffold_ast_baseline.json`,
enforced by `test_ast_attest.py`) is **already red at the parent**, and not
because of this plan. Derived at `b16f4607` in a clean copy by the method in
`bootstrap/AST_BASELINE_RUNBOOK.md` (Step 1): CHANGED 2, MISSING 0, DUPLICATE 0.
The two are `main` in `bootstrap/_scaffold/cli.py` and `seed_gitignore` in
`bootstrap/_scaffold/install.py`. That re-anchor is the Maintainer's and is
owed regardless. Boundary B will therefore show one non-pass that is not this
plan's; C5 disposes of it by showing the same two symbols, with the same
hashes, before and after. **The figure is not to be carried forward**: derive it
again at the parent.

**Lockfile.** Both Cairn template copies already report a hash mismatch in
`python bootstrap/verify_integrity.py --target .` (18 files at `7f1bcdf0`, the
two templates among them). They are **not finalized**: that would re-attest
earlier, unreviewed drift. The set of 18 must be the same before and after each
template chunk.

**Install contract: unchanged.** The published `scaffold.py --manifest` lists
destination, source and mode, with no content hashes. No file is added to or
removed from the install set, so `_CORE_MAPPINGS` is untouched. C2 and C3 show
`--manifest` output byte-identical to the parent's.

### Tests that read the touched files

Found by searching `bootstrap/tests/*.py` for every touched path, as literals
and as `Path` joins, at `7f1bcdf0`; not by expectation. The proposal said
twelve files read the templates, and a search for `_template.md` does return
twelve. Which of them *assert on template text*:

* **`test_scaffold.py`** (frozen). The security-preflight slice is the lines
  from the `#### Security preflight` heading up to the first later line that
  starts `**Prospective only.**`, compared byte-for-byte between the two
  proposal templates. A block inside that span would be swallowed into it, and
  no test would go red, since both copies grow alike. So the block sits **after**
  that line, and C2 shows the slice is unchanged.
* **`test_scope_reduction_trap.py`** (frozen). Presence patterns over whole
  normalized text of all four copies. They are not windowed across the sections
  edited here.
* **`test_verification_boundaries.py`** (frozen). Pins tokens in the plan
  templates and "speed alone does not establish affected coverage" in the
  proposal templates. One guard asserts the plan template carries no
  `## Implementation verification` H2, and another replaces the *first*
  "Reviewed range" in Cairn's plan template; the new plan paragraph contains
  neither.
* **`test_documentation_plan_module.py`** (frozen). Slot markers in the shipped
  templates; the new text sits outside every slot.
* **`test_claim_check_module.py`**, **`test_core_dev_folders.py`**,
  **`test_quickstart_sequence.py`** (frozen). Existence and liveness-exemption
  only; no text assertions on the edited passages.
* **`test_profile_grammar.py`** (frozen). Reads `bootstrap/BOOTSTRAP.md` through
  two marked example fences only; the I-2 paragraph is outside both.
* No test reads `dimensions/*.md`. Searched `bootstrap/tests/*.py` for
  `dimensions` and found one comment.
* **The install family.** The `verification-practice` plan counted 57 test files
  that drive a scaffold install and so render the shipped templates. No mapping
  bounds that confidently, which is why Boundary B is full.

Measured on the drafted wording, applied to a clean copy of `7f1bcdf0`: the eight
files above, plus `test_comprehension_floor.py` (which reads `AGENTS.md`, not
these templates, and is run as a control), pass **372** with the edit and **372**
on the unedited control. `check_cairn.py` reports OK on both (180 files), and the
neutrality leg reports 74 failures on both, none in a file this plan edits.

### Found while planning, not widened

* **The accepted smoke sentence cannot show a block install.** Revision 1 says
  `scaffold.py --summary --config <profile>` and `--dry-run` "show the block
  installing". Both were run: they print the profile, the tokens and the module
  roster and never open a template. The outcome, that an adopter receives the
  block, is delivered more directly by a real install into a scratch tree and a
  `diff` of the installed region (C2, C3). That is stronger, not weaker, and
  `--summary` and `--dry-run` still run and are recorded.
* **How an existing adopter receives the block.** Measured on the drafted
  wording: install from the parent into a scratch tree, fill the
  `documentation-tier-home` slot in both installed templates, commit, then run
  `scaffold.py upgrade --plan` and `--stage` against the edited tree. `--plan`
  reports both templates "locally-modified (merged clean)". The staged file holds
  the block once, the adopter's slot fill once, and no conflict marker. C2 and C3
  repeat this on the real commits.
* **Two small wording choices beyond the quoted drafts.** (a) The plan paragraph
  opens "If the proposal names one, it becomes an acceptance criterion". The
  draft's unconditional "It becomes an acceptance criterion" would read as a
  demand on a proposal that wrote N/A. (b) The *Reviewers* paragraph says the
  Maintainer judges "whether this is the right check and the expected value is
  right" at the Decision. That is Revision 1's *Who does what*, which the quoted
  block draft omits. Neither adds an obligation; both are for the plan reviewer to
  strike if they disagree.
* **The "Hydrology examples" in *Who does what* stay out of the template**
  (Theis, Glover–Balmer, an inversion recovering a synthetic truth, a
  post-processor against the model's saved budget). Neither quoted draft carries
  them, and the proposal names "the block grows discipline sub-lists" as a sign
  the change is wrong. The one example the template does carry is the
  streamflow-depletion case that came with the Maintainer's addition, since a
  positive control is the least familiar idea in the block.
* **`doctrine/rationale.md` still calls scientific-error detection "without the
  Maintainer in the loop" an open problem.** That stays true: the check puts the
  Maintainer in the loop on purpose. No edit.
* **The nearest live home of the revisit is a row that says nothing about it.**
  `dev/PLANNING.md` > "0.3 external correctness test (R-H third-party probe)"
  does not mention the axis revisit. Adding it is the archive commit's (see
  *Dispositions*), because the Decision says "At archive, the plan adds".

### Sequencing with the other accepted work

Implementation order: **`neutrality-and-upgrade-slots` (plan C), then this plan**,
then `model-mapping-install-path`, `board-as-basis`,
`external-is-a-maintainer-stance`. **This plan rebases on plan C.** Plan C is not
open yet as this plan is written, so each chunk re-reads the files it edits at
edit time (`git log -3 -- <file>`). `maintainer-attention` and
`verification-practice` are archived and their edits are already in the tree:
`dev/plans/_template.md` and its twin carry the Waiting-line preamble and the
`verification-commands` slot, both outside the *Acceptance criteria* paragraph
edited here.

| Plan | Shared with this plan | Effect |
|---|---|---|
| `neutrality-and-upgrade-slots` (before) | **The neutrality checker**: it gets stricter (whole-line HTML comments, `.json` and `.txt` under `templates/`, four more names), and runs in this plan's Boundary B. **`bootstrap/verify_integrity.py`** and `bootstrap/UPGRADE.md`, which this plan does not edit. **`dev/PLANNING.md`** and **`CHANGELOG.md`**, each plan adding to them at its own archive. | The new text names no vendor, comments included, and contains no HTML comment. Plan C's own check that `verify_integrity --target .` still lists 18 files holds here, since both Cairn template copies are on that list already. |
| `model-mapping-install-path` (after) | **`bootstrap/BOOTSTRAP.md`**: it edits II-5 and the allowed-match list; this plan edits the I-2 paragraph. **`dev/PLANNING.md`** at archive. | Different sections, so a textual rebase only. |
| `board-as-basis` (after) | **`dev/PLANNING.md`** and **`CHANGELOG.md`** at archive only. | None. |
| `external-is-a-maintainer-stance` (after) | **Both template pairs** (its External and tier wording), **`dimensions/README.md`** (the same Complexity cell), **`dimensions/complexity.md`** (the Complex position's neighbouring bullet), and **`dev/PLANNING.md`** (the re-anchor row). | That plan rebases on this one. Its rewording of the Complexity cell ("review weight and verification depth") must keep a mention of the check, or the promise site stops naming it. This is noted here for its author; it is not planned here. |

`review-lenses-for-every-install` was accepted (`fbf664f0`) after the order above
was set, and is not in it. It edits the `AGENTS.md` pointer, the review-loop
document, the `dual-review` module and one doctrine section, and names
`bootstrap/BOOTSTRAP.md` and the proposal and plan templates as outside its scope,
so no file is shared. It delivers the existing lenses, lens 8 among them and
unchanged, to every install; this plan edits no lens text.

## Sequence

C1 is a gate: it can stop the plan. Every later chunk lands one commit.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | **Try the wording on two past plans, before any file changes.** A fresh-context agent that is not the implementer drafts the block from the wording below and the proposal text as it stood at its Decision, for two archived LHM plans. The implementer compares each draft with the error later found. Stop if neither would have named a check that fails under that error. | `ready-to-implement` | one commit: the appended `## Retroactive application` record; Status to `implementing` |
| C2 | **The proposal-template block**, in both copies, with the positive-control bullet; and the new test with its proposal-side groups. | C1 not "neither" | one commit |
| C3 | **The plan-template paragraph**, in both copies; the same test gains its plan-side groups. | C2 | one commit |
| C4 | **Repoint the three promise sentences** at the check. | C2 (the block they name must exist) | one commit |
| C5 | **Boundary B, then the record.** One full run on the finished work, written down. Status to `awaiting-code-review`. | C2–C4 | one commit |
| M | **MAINTAINER-ONLY — no new ceremony.** The *re-anchor* is the supervised ceremony, run only by the Maintainer, that brings the gate manifest up to date with changed tests (`bootstrap/REANCHOR_RUNBOOK.md`). The new test's node joins the row already queued on `dev/PLANNING.md`, so M needs no Waiting line in this plan: that row declares the wait. **An implementing agent must not perform it.** The agent's part is the board note at archive. | code review cleared | Maintainer |

If C1 ends "neither", the implementer writes `**Waiting on Maintainer**: block
judged ritual; plan stopped` in the header block beside Status and stops. Nothing
is landed.

### Wording each chunk lands

This is the plan's settling of the wording Revision 1 left to it. The implementer
pastes these bytes. A word that must change is a plan revision before
implementation begins, and an appended note after. The block is **identical in
both proposal templates** and the paragraph **identical in both plan templates**:
neither sits in a slot, so there is no reason for the copies to differ. The new
text has no `{{` token, no HTML comment, no backticked path and no vendor or
project name.

**C2 — the block.** Inserted as a new H3, directly after the line that ends the
security preflight (the paragraph beginning `**Prospective only.**`) and its
blank line, and directly before `## Signals the change is wrong`:

```text
### Independent scientific check

*Gated to a change that touches a scientific assumption, or a result the
project publishes or acts on: a governing equation, a unit or sign convention,
a boundary condition, a parameter default, a calibration setup, or a coupling
between models. For every other change, one line — "N/A: no scientific
assumption or result touched" — is the correct entry.*

Name **one** check that could show the change is wrong about the world, not
only about itself:

* **What it compares.** The quantity, the expected value, and the tolerance
  with its source. Say whether the data behind the expected value is in hand
  and has been checked. If the check depends on data that does not exist yet,
  say so.
* **Why the expectation is independent.** Neither the proposed code nor a test
  written from the same understanding computes it. Its basis is one of these:
  * an analytical or manufactured solution;
  * a conservation law chosen against the error this change risks (a closed
    budget does not catch a wrong input);
  * a trusted observation or benchmark;
  * an independent implementation, or the saved output of the model the code
    reads (independent of the port, not of the model's physics);
  * a domain expert's expectation, written down before the result is seen.
* **The error it would catch.** The plausible mistake under which the check
  fails (a reversed sign, a unit slip, a misplaced boundary, a missed
  warm-up). This is security preflight S2's "Can it fail?", asked of a
  scientific check. At implementation, the implementer makes that mistake on
  purpose and records the check's failing output.
* **When the result is "no effect".** A check that finds no change is evidence
  only if it could have found one. Show the same analysis detecting a known
  effect of the size that matters (a positive control), or say plainly that it
  cannot. For example, an analysis that reports no streamflow depletion from a
  pumping well first recovers the depletion of a synthetic well of comparable
  rate.

**Reviewers.** The proposal reviewer challenges whether the basis is really
independent of the code under review. The code reviewer verifies the recorded
failing run and the positive-control run, and re-runs them when that is cheap.
The Maintainer judges at the Decision whether this is the right check and the
expected value is right. If no independent basis exists, say so; the
Maintainer weighs that, and it is not a reason to invent one.
```

**C3 — the paragraph.** Inserted in *Acceptance criteria*, directly after the
paragraph ending "(which gate command fires the check)." and before the
`acceptance-doc-tooling` slot, keeping the blank lines the file already has:

```text
**An independent scientific check is accepted scope.** If the proposal names
one, it becomes an acceptance criterion. A replacement qualifies only if it
fails under the error the original names. If nothing qualifies, dropping the
check is a scope reduction under *Scope delta* and needs the Maintainer's
quoted allowance. Saying that the result now rests on the implementation does
not settle it. When the check fails for real during implementation, one line
records whether anything else would have shown the error.
```

**C4 — the three promise sentences.** Each replaces the sentence that promises a
"scientific-trust review lens" that no module installs.

`dimensions/complexity.md`, Complex position, in place of the bullet beginning
"A **scientific-trust review lens** is in the roster":

```text
* The proposal template's **independent scientific check** is expected
  of every change that touches a scientific assumption or a published
  result: one check whose expected value neither the code nor its
  tests compute, shown to fail under the mistake it names. The block
  is gated on the change, not on this axis. Here, an unexplained "N/A"
  on a change that touches a computed result is a review finding.
```

`dimensions/README.md`, the Complexity row of the axis table. The one line
changes in its last clause only ("whether a scientific-trust review lens is in
the roster."):

```text
| **Complexity** (`complexity.md`) | simple ↔ complex | Review weight and verification depth — how often External review is mandatory, whether an unexplained "N/A" on the independent scientific check is a review finding. |
```

`bootstrap/BOOTSTRAP.md`, I-2. The three lines beginning "Fill the template." end
"... those drive the legacy-agent and / scientific-trust-reviewer decisions
downstream. If uncertain," and become four:

```text
Fill the template. Do not skimp on the scientific-surface and
documentation-trust sections — those drive the legacy-agent decision,
and which changes must name an independent scientific check,
downstream. If uncertain,
```

**The new test** (`bootstrap/tests/test_scientific_check_guidance_ships.py`) has
**one** function, `test_every_template_copy_carries_the_same_check_guidance`,
following the shape of `test_installed_templates_carry_security_preflight_questions`
in `test_scaffold.py`: three groups accumulate into one failure list, so every
group runs every time. Its docstring says why (the two pairs must not drift, and
a duty deleted from both copies at once must not go unnoticed) and cites no
finding, chunk or plan row. It reads the four files by path from the repository
root, the way `test_scope_reduction_trap.py` does.

* **Parity.** The proposal block is the lines from the heading line (`###
  Independent scientific check`, the whole line) up to, not including, the next
  line that starts `## `. The
  plan paragraph is the lines from the one starting `**An independent scientific
  check is accepted scope.**` to the next blank line. Each region's
  whitespace-collapsed text must be equal between the Cairn copy and the shipped
  copy. A missing marker or a heading that occurs other than once raises an
  `AssertionError` naming it, never an empty region (two missing regions would
  be equal).
* **Duties.** Each copy must contain every anchor below, as a substring of its
  whitespace-collapsed region. *Proposal block:* `Gated to a change that touches
  a scientific assumption`; `N/A: no scientific assumption or result touched`;
  `What it compares`; `in hand and has been checked`; `does not exist yet`;
  `Why the expectation is independent`; `analytical or manufactured solution`;
  `conservation law`; `trusted observation or benchmark`; `independent
  implementation`; `not of the model's physics`; `domain expert's expectation`;
  `The error it would catch`; `Can it fail?`; `on purpose`; `records the check's
  failing output`; `When the result is "no effect"`; `could have found one`;
  `positive control`; `say plainly that it cannot`; `Reviewers.`; `challenges
  whether the basis is really independent`; `verifies the recorded failing run
  and the positive-control run`; `If no independent basis exists, say so`.
  *Plan paragraph:* `An independent scientific check is accepted scope.`;
  `acceptance criterion`; `fails under the error the original names`; `scope
  reduction`; `quoted allowance`; `does not settle it`; `one line records whether
  anything else would have shown the error`.
* **Placement.** In each proposal copy the block heading lies after the line
  that starts `**Prospective only.**`, which is the end of the security-preflight
  slice, and the block region holds no `cairn:slot` or `cairn:end` marker.

## Acceptance criteria

**Reading these criteria.** Each ends with *Red when*: a change that turns it
red. Every "mutate" step runs in a **throwaway `git worktree`** at the chunk's
commit, in a fresh, empty folder: the new test and `test_scaffold.py` read the
files of the tree they sit in, so a scratch copy of one file would never be
read. Each mutant is reported as killed, survived or equivalent, beside an
unmutated control run in the same worktree. The files under test are the four
template copies and the three promise sites, listed from the tree
(`git ls-files` for `_template.md` under `dev/` and `templates/core/dev/`;
`git grep` for the old phrases), not from the diff. Doc tooling:
`python scripts/check_cairn.py` is the prose smoke, and `python
scripts/claim_check.py <file>` runs on every edited document.

### C1

* **The inputs are fixed first.** Before any draft is read, the record names: the
  wording (this plan's commit), and, for each plan, the source-proposal commit and
  the error later found, each with its citation. For
  `dev/plans/archive/stor-modflow-correctness.md`: the source proposal
  `dev/proposals/archive/2026-08-27-claude-stor-modflow-flopy-layer.md`, as it
  stood at its Decision, LHM commit `9dc9acfb` (`git show 9dc9acfb:` plus its
  unarchived path, `dev/proposals/2026-08-27-claude-stor-modflow-flopy-layer.md`,
  in the LHM repository); the errors are priming the percolation stack and the
  RAMP-period shift, found by the External code review at LHM `983d6c58` and
  fixed at `6dcc0cc5`, plus the check that was lost at plan revision `7a9771f5`
  after the Internal plan review at `dae97b43` found the reference array had never
  been saved. *Red when:* the error is chosen after the draft is read.
* **The second plan is chosen by a rule, in the record, before the exercise.**
  The rule: an archived LHM plan, newest first, in which a code review or a later
  record found an error in a **computed result** (not in structure, tests or
  documents). Candidates to consider first:
  `dev/plans/archive/2026-10-01-claude-assemble-part-a.md` (code reviews of
  2026-10-14 and 2026-10-15) and the other 2026-10 LHM plans.
  The record names the plan, the finding, and why it qualifies. If **no** LHM plan
  qualifies, the implementer does not substitute one from another repository:
  that is a deviation request to the Maintainer (Waiting line). *Red when:* the
  plan is picked for how well the block fits it.
* **The draft is blind.** A fresh-context agent that is neither the implementer
  nor a reviewer of this plan receives only the wording above and the proposal
  text at the named commit, with nothing from the plan, a review, or the code
  review that followed. Its draft goes into the record **verbatim** before the
  comparison is written. *Red when:* the brief mentions the error, or the draft is
  paraphrased.
* **Each plan gets three plain answers.** (a) Does the drafted check, if its data
  were in hand, fail under the error later found? (b) Where the record shows a
  claim about the data that was false or never checked (for
  `stor-modflow-correctness`, that the run's saved output carried the model's own
  `unsatStorage`), does the drafted "in hand and has been checked" answer surface
  it, by saying the data is not confirmed in hand instead of asserting it? Where
  the record shows no such claim, (b) is "not applicable". (c) Is the basis one the
  block lists, and independent of the code under review? A plan's verdict is
  **yes** when (a) is yes and (b) is yes or not applicable, and **no** otherwise,
  each with its reason in one or two sentences. *Red when:* a verdict has no
  reason, or "yes" rests on an answer the draft does not support.
* **The stop rule is exactly the accepted one.** If both verdicts are **no**, the
  block is judged ritual: the plan stops, and nothing in C2–C5 is committed. If at
  least one is **yes**, the plan proceeds, and the record says in plain words which
  plan it was and what the other showed. One "no" is reported to the Maintainer in
  the record and in the archive commit; it does not stop the plan. *Red when:* the
  stop is softened to a warning, or hardened to "either".
* **The null-result bullet is not claimed as tested.** Neither plan found a
  false null, so the record says the positive-control bullet has no occurred
  instance behind it and rests on argument. *Red when:* the record cites either
  plan as support for it.
* **The record is appended, once.** An H2 `## Retroactive application -- <agent>
  -- YYYY-MM-DD`, with the six items above. `claim_check` on this plan is clean
  after it, with the LHM paths on the `External-repo paths:` line. The commit sets
  Status to `implementing`.

### C2

* **The block is where the wording says, once, in both copies.** `grep -c
  '^### Independent scientific check$'` prints 1 for each of
  `dev/proposals/_template.md` and `templates/core/dev/proposals/_template.md`,
  and the heading sits after the line starting `**Prospective only.**` and before
  `## Signals the change is wrong`. *Red when:* it sits before that line (inside
  the preflight slice) or in a slot.
* **The preflight slice is unchanged.** Extract the slice from each copy with
  `_extract_security_preflight` (imported from `test_scaffold.py` in a throwaway
  snippet) at C2's parent and at C2's commit: the two slices are byte-identical
  in each copy. *Red when:* the slice grows. This is the "must not swallow the
  block" property, measured.
* **The bytes are the reviewed bytes.** The block extracted from each copy is
  `diff`-identical (exit 0) to the fenced C2 text in this plan. *Red when:* any
  word differs; the implementer then revises the plan, not the template.
* **The two copies are the same.** The two extracted blocks `diff` to exit 0.
* **The duties are all present, including the Maintainer's addition.** Each
  anchor in the test's proposal list occurs in each copy's block. The bullet
  `When the result is "no effect"` occurs once per copy, says a check "is
  evidence only if it could have found one", and the *Reviewers* paragraph names
  "the positive-control run". *Red when:* the bullet or the reviewer clause is
  missing from a copy.
* **The new test is one node.** `pytest --collect-only -q
  bootstrap/tests/test_scientific_check_guidance_ships.py` lists exactly one
  test, and it passes at C2 (proposal side). *Red when:* it is parametrized or
  split.
* **The test can fail.** In the worktree at C2, with an unmutated control run
  first (passes): (m1) change one word of the block in the Cairn copy only; (m2)
  the same in the shipped copy only; (m3) delete the `no effect` bullet from
  **both** copies; (m4) delete the *Reviewers* paragraph from both; (m5) move the
  heading above the `**Prospective only.**` line in both; (m6) remove the heading
  from both. Expected: m1 and m2 killed by parity; m3 and m4 killed by duties
  while parity stays green; m5 killed by placement while parity and duties stay
  green; m6 killed with a message naming the missing marker. Any survivor is
  reported as a survivor. *Red when:* m3 or m4 survives (a duty can leave both
  copies unnoticed), or m6 passes (an empty region compares equal).
* **Existing pins pass unedited.** The eight files named under *Tests that read
  the touched files*, plus `test_comprehension_floor.py`, pass with the same
  count as the unedited parent (372 at planning time on the drafted wording; the
  implementer records both figures at the parent and at C2).
* **No vendor or project name.** The neutrality leg's failure count at C2 is not
  higher than at the parent, and none is in a file this plan edits. A `grep -n -E
  'Claude|Codex|Anthropic|OpenAI|Gemini|Cursor|LHM|modflow_tools'` over the added
  lines prints nothing; first run it over a line known to hold one (the instrument
  check). *Red when:* the pattern finds a known hit on neither run.
* **The install contract is unchanged.** `python bootstrap/scaffold.py --manifest`
  at C2 and at its parent `diff` to exit 0.
* **An adopter receives the block.** Install into an empty scratch tree
  (`bootstrap/profiles/solo-greenfield.yml`, `--non-interactive --allow-dev`). The
  installed `dev/proposals/_template.md` holds the block `diff`-identical to the
  source, with no `{{` inside it. `--summary` and `--dry-run` are also run and
  recorded; they cannot show content. *Red when:* the installed region differs.
* **An existing adopter's upgrade keeps their work.** Install from the parent, fill
  the `documentation-tier-home` slot, commit, then `upgrade --plan --cairn-root
  <C2 tree>` and `--stage`: the template is classified "locally-modified (merged
  clean)", and the staged file holds the block once, the slot fill once, and zero
  `<<<<<<<` markers. *Red when:* a conflict marker appears or the slot fill is
  lost.
* **The lockfile is left alone.** `python bootstrap/verify_integrity.py --target .`
  reports the same findings at C2 and at its parent (18 at planning time), none
  newly attributable to this chunk; no finalize is run.
* **The prose gates are clean.** `python scripts/claim_check.py` exits 0 on both
  copies and `python scripts/check_cairn.py` reports no issues.

### C3

* **The paragraph is where the wording says, once, in both copies.** The line
  starting `**An independent scientific check is accepted scope.**` occurs once in
  each plan template, after the security-preflight paragraph and before the
  `acceptance-doc-tooling` slot, and is `diff`-identical (exit 0) to the fenced C3
  text. *Red when:* it sits inside the slot, or a word differs.
* **The two copies are the same, and every duty is present.** The anchors in the
  test's plan list occur in both. *Red when:* "scope reduction" or "quoted
  allowance" is missing from one copy.
* **The test grows, and stays one node.** The same function now covers the plan
  pair; the collection still shows one test. Mutants run in a worktree at C3,
  beside a control: (m7) change one word in one plan copy only; (m8) delete the
  `scope reduction` sentence from both; (m9) delete the whole paragraph from one
  copy; (m10) delete it from both. Expected: m7 and m9 killed by parity, m8 killed
  by duties with parity green, m10 killed with the missing-marker message.
  *Red when:* m8 or m10 survives.
* **The plan template's own pins stand.** `test_scope_reduction_trap.py` and
  `test_verification_boundaries.py` pass unedited, and the template still holds
  no `## Implementation verification` H2.
* **Same smoke as C2 for the plan template.** The installed plan template carries
  the paragraph; the manifest `diff` is empty; the upgrade stage keeps the slot
  fill and has no conflict marker; `verify_integrity` lists the same findings.
* **The header block is untouched.** The template's `**Plan review**:` line, and
  the absence of any line-initial `**Waiting on Maintainer**` in either plan
  template, are as at the parent (`grep -nE '^ *([*-] )?\*\*Waiting on
  Maintainer\*\*' dev/plans/_template.md templates/core/dev/plans/_template.md`
  prints nothing, as at the parent).

### C4

* **The old promise is gone from all three sites, and the new one is in them.**
  `git grep -n -i 'scientific-trust' -- dimensions bootstrap/BOOTSTRAP.md` prints
  three lines at the parent (the instrument check) and **nothing** at C4.
  `independent scientific check` occurs in each of the three files. *Red when:*
  any site still names the lens, or any lacks the check.
* **The complex-project finding is stated.** `dimensions/complexity.md` holds the
  sentence about an unexplained "N/A" on a change that touches a computed result
  being a review finding, once, in the Complex position. *Red when:* it sits in
  Simple, or the "gated on the change, not on this axis" sentence is missing.
* **No axis, axis value or gate-table row changed.** `git diff -U0` over the three
  files shows exactly three hunks, none inside the I-4 or I-5 tables or the axis
  rubric; `dimensions/README.md`'s edited row has the same number of `|`
  separators as at the parent. *Red when:* a fourth hunk appears or the row's cell
  count changes.
* **The text is bytes-as-reviewed.** In `git diff -U0`, the added lines of each
  hunk equal the fenced C4 text exactly, and the removed lines are exactly the
  old ones named above. *Red when:* a word differs or a hunk removes anything else.
* **The line that is not a promise stays.** `templates/modules/team-gated/architecture_review_template.md`
  still carries its own "Scientific Trust" lens line; this plan does not edit it,
  because that module does ship a lens set. *Red when:* the file is in the
  chunk's `git diff --stat`.
* **Gates.** `test_profile_grammar.py` passes; `check_cairn.py` reports no issues;
  `claim_check.py` exits 0 on each of the three; the neutrality and redundancy
  legs are not worse than at the parent; no vendor or project name on any added
  line (same instrument check as C2).

### C5

* **The record is complete.** `## Implementation verification -- <agent> --
  YYYY-MM-DD` carries each field *Verification* lists: mode, tested commit,
  reviewed range, interpreter, pre-run and post-run state, the command table with
  exit, outcomes and elapsed, the non-pass disposition, the plan-specific commands,
  and known omissions. It lists the new test's node ID, which matches `pytest
  --collect-only -q` for the added node, and the mutation ledgers of C2 and C3.
  *Red when:* a field label is absent or the node ID differs.
* **The AST non-pass is disposed of, not hidden.** The record shows the AST
  CHANGED set at the tested commit equals the set at the parent (the same symbols,
  the same hashes), and that `git diff --stat` over the implementation range is
  empty for `bootstrap/_scaffold/` and `bootstrap/tests/fixtures/`. *Red when:*
  the sets differ or the range touches either path.
* **No frozen file changed.** The intersection of the range's changed paths with
  the manifest's `frozen_files` keys is empty. *Red when:* it is not.

## Scope delta

**Scope delta**: preserved. The baseline is Revision 1 as accepted. Every
outcome in it maps to a chunk:

| Accepted outcome | Chunk |
|---|---|
| Edit 1: the gated block in both proposal templates, with its three fields, the five bases (the reference-implementation basis with its limit), the data-in-hand statement, the implementer's deliberate break and recorded failing output, and the reviewer duties (including "if no independent basis exists, say so") | C2 |
| Edit 2: the plan paragraph (accepted scope; a replacement qualifies only if it fails under the original's error; scope reduction and the Maintainer's quoted allowance; "rests on the implementation" does not settle it; one line when the check fails for real) | C3 |
| Edit 4: the promise repointed at the check alone, at `dimensions/complexity.md`, `dimensions/README.md` and `bootstrap/BOOTSTRAP.md`, with the complex-project "N/A" finding and no axis, value or gate-table change | C4 |
| Both template pairs match outside their slots; one new test holds the block and the plan sentence word-for-word identical across the twins | C2, C3 |
| The falsification test that runs before landing (two plans; stop if neither) | C1 |
| Done-when gates: claim check, prose integrity, neutrality and redundancy, no vendor named | C2–C5 |
| Smoke: the block installs | C2, C3 (a real install; see *Found while planning*) |
| Boundary B full, Python 3.13.x | C5 |
| Archive: the guide star's open-gap entry, a CHANGELOG line, the axis revisit added to the third-party probe row | *Dispositions* |
| The revisit's trigger and falsifiers have a live home; #19 stays open | *Dispositions* |

**Already conceded, not re-opened here.** Edit 3, the lens-8 doctrine sentence, was
removed by the proposal's own Scope delta and conceded by the Maintainer's Q1
answer. Its disposition is `defer`, homed on the board row "The
independent-scientific-check rule as doctrine (#19)" in `dev/PLANNING.md`, with
the Decision quoted there. This plan removes nothing further, so it owes no
`disposition` lines.

**One addition, at the Maintainer's instruction**, recorded under *Scope*: the
positive control for "no effect" results (the bullet and one reviewer clause, C2;
its anchors in the test, C2). It adds to the floor and removes nothing. "Planted
errors" is out of scope.

## Verification

**Boundary A (iteration, scoped).** Each chunk runs the tests that own the files
it touches, plus `python scripts/check_cairn.py` and `python
scripts/claim_check.py` on each edited document. All tests are in
`bootstrap/tests/`.

| Chunk | Tests and gates |
|---|---|
| C1 | `claim_check.py` and `check_cairn.py` on this plan; no pytest |
| C2 | the new test; `test_scaffold.py` (installed-template and preflight-slice tests); `test_scope_reduction_trap.py`; `test_verification_boundaries.py`; `test_documentation_plan_module.py`; `test_core_dev_folders.py`; `test_quickstart_sequence.py`; `test_claim_check_module.py`; the neutrality and redundancy legs; the two scratch installs and the upgrade probe |
| C3 | the same set, with the plan-template smoke |
| C4 | `test_profile_grammar.py`; the prose gates; the neutrality and redundancy legs |
| C5 | the full suite (below) |

**The install family is the reason this is not a confident bound.** Most of the
suite renders the shipped templates, so Boundary B is the real check.

**Boundary B mode**: full. The refusal rules in `AGENTS.md` settle it:

1. **The accepted text says so.** "Test bytes change, so Boundary B runs the full
   suite under Python 3.13.x."
2. **A shipped template is edited.** Four template files, two of which reach every
   adopter and are rendered by most of the install family. No mapping bounds that
   confidently, and uncertainty resolves to `full`.
3. **The collection grows.** A new test node joins the gated collection.
4. **A high-risk surface governs the text.** Vendor-neutrality is one of
   `AGENTS.md`'s named high-risk surfaces, and these templates are inside its
   gate. This plan adds no name and changes no rule of the gate, but bounded mode
   refuses on the surface.

**How it runs.** After the last implementation chunk (C4), against a clean,
unchanged commit, under the canonical interpreter
(`/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.x), from a separate
`git worktree` at the tested commit (a worktree shares refs, so the gate anchor
is present, and other sessions' uncommitted files stay out of the count):

```
CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0
python scripts/quality_gate.py --sub neutrality --sub redundancy
python scripts/check_cairn.py
python bootstrap/scaffold.py --manifest
```

then `claim_check.py` on each edited document, the two scratch installs, the
upgrade probe, and `verify_integrity --target .` before and after.

**Expected non-pass**, each disposed of rather than treated as noise. These are
the ones known at planning time; **derive the real list from a full run at the
parent**, in the same way, and do not carry this list forward:

* **`test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package`**
  is red at the parent on two symbols (see *AST*). The record shows the set is
  unchanged by this plan.
* **The neutrality leg** carries 74 pre-existing failures at `7f1bcdf0`, until plan
  C lands (it is meant to bring the count to zero). Record the figure at the tested
  commit and confirm no hit is in a file this plan edits or on a line it added.
* **`test_gate_manifest.py`** has no expected failure: changed frozen bytes do not
  redden it, and no frozen file changes here.

**Known omission.** Nothing standing pins the three promise sentences, because the
accepted evidence names **one** new test and a second pin file is a larger
ceremony. They are checked once by C4's counts and again by Boundary C. A later
edit that restores a lens promise would go unnoticed by the suite; the live risk is
`external-is-a-maintainer-stance`, which rewords the same Complexity cell next.

**Boundary C** is the code reviewer's, run after Boundary B. The points worth
attacking:

* **Is the independence real?** Pick one bullet of the five and try to write a
  "check" that satisfies the words and still shares the code's wrong convention.
  If that is easy, the block is a ritual (the F2 sign).
* **Does the null-result bullet misfire?** It should ask for a positive control
  only where the result is "no effect". Read it against a tooling change and
  against a change that finds an effect.
* **The gate.** Does the opening sentence send a pure-tooling change to N/A, and a
  change that touches a computed result to a check? Both ways, with the proposal's
  own "gate misfires" sign in mind.
* **Read cold as an adopter.** A solo scientist with one agent has no `doctrine/`,
  no dual-review module, and no second reviewer. Can they follow the block, and the
  plan paragraph, from the shipped templates alone?
* **The set.** Mutate each of the four copies and each of the three promise sites
  separately; confirm which gate catches each, and report the ones nothing catches.
* **The upgrade.** Re-run the stage probe on the reviewed commit with an adopter
  who has *edited the block*, not only a slot, and see what the merge does.
* **The C1 record.** Is each "yes" supported by the blind draft as written, and was
  the second plan chosen by the rule?

**Security preflight.** N/A: no trust boundary is added, moved or widened. The new
test reads fixed repository paths and runs no subprocess; the scratch installs and
upgrade probe run the existing, unchanged scaffold against a scratch folder. The
chunking changes no answer.

## Dispositions

*Filled at archive-preparation.* The items known now, so that none lives only in
this plan:

* **The archive commit writes its own `CHANGELOG.md` entry**, under *Unreleased*,
  one line, linking this plan's archived file.
* **It updates the guide star's open-gap entry** in
  `dev/strategy/2026-05-14-claude-human-ai-team-development-framework.md` ("No
  scientific acceptance check grounded outside the implementation"): the
  one-check form has landed as template guidance, with the date and this plan's
  stem. The gap stays named: the `deliverable` axis, its disciplines, the
  governance reframe and the doctrine statement remain open.
* **It adds the revisit to the third-party probe row**, "0.3 external correctness
  test (R-H third-party probe)" in `dev/PLANNING.md`, so the trigger has a live
  home: *the `deliverable` axis is revisited when this row moves, or at the
  Maintainer's call once about ten real (non-N/A) checks exist across two projects.
  Nothing counts them; the Maintainer remembers.* The same row carries, so the
  falsifiers are not left in an archived file: **F1** every failing check's record
  names something else that already showed the error; **F2** most bases are "the
  Maintainer's expectation"; **F3** changes that touched an assumption carry N/A;
  **F4** recorded failing runs are absent or cannot be reproduced; **F5** failing
  checks keep coinciding with errors code review also catches (a smaller claim,
  still worth having); and **F6**, added by this plan with the positive control:
  no "no effect" result carries a positive control or a plain statement that none
  exists. "If nothing fails and no later error surfaces, the result is
  inconclusive, not a pass." That revisit also reads the C1 record.
* **It adds the new test's node ID to the queued re-anchor row** (chunk M), under
  the same rule as the earlier plans: one node, in an unfrozen new file, dropping
  none. The ceremony itself stays the Maintainer's.
* **It confirms the issues' state** and edits neither: #18 `CLOSED` (done
  2026-10-18), #19 `OPEN`. #18's export-safety affirmation is not touched.
* **This plan carries no Waiting line at archive**: the open wait, the re-anchor,
  is declared on its marked board row.
* **Not owed:** the deferred doctrine sentence (already on its own board row), the
  `deliverable` axis and its disciplines (#19), and the AST and neutrality
  baselines (not this plan's).
