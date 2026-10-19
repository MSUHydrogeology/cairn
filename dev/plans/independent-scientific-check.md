# Plan: independent scientific check — one check per scientific change, shown able to fail

**Source proposal**: `dev/proposals/archive/2026-10-17-claude-independent-scientific-check.md`
**Status**: revising-code
**Plan review**: required(Internal)
**Assurance path**: high-assurance — inherited: the change edits the authoring templates and the axis prose that adopters' bootstrap reads.
**Opened**: 2026-10-18

External-repo paths:
- `dev/proposals/archive/2026-08-27-claude-stor-modflow-flopy-layer.md`
- `dev/proposals/2026-08-27-claude-stor-modflow-flopy-layer.md`
- `dev/plans/archive/stor-modflow-correctness.md`
- `dev/plans/archive/2026-10-01-claude-assemble-part-a.md`
- `dev/proposals/archive/2026-10-01-claude-assemble-full-port.md`
- `dev/proposals/2026-10-01-claude-assemble-full-port.md`

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
4. **When the check passes by finding nothing** *(added at the Maintainer's
   instruction; see Scope)*: a check that passes on "no change", "no
   difference" or "no effect" is evidence only if it could have found a change.
   The analysis must show it can detect a known effect of the size that matters
   (a **positive control**: the same analysis run on a case where the answer is
   known to be non-zero), or say plainly that it cannot. The failing run from
   answer 3 is that control whenever the mistake it makes produces an effect of
   that size, so most checks owe no second run.

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
new review round, and no scheme for planting errors. The rule carries no doctrine
weight; it is template guidance. The doctrine sentence waits on the board.

**Order of work.** First, before any file changes, the wording is tried on two
past LHM plans, using only the text each proposal had when it was opened. If it
would have helped on neither, the plan stops and the Maintainer decides. Then the
two templates (with the one new test), the three promise sentences, and last one
full test run.

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
  holding **one** test (created in C2, given its fourth group in C3).
* This plan: the C1 record and the Boundary B record are appended to it, and the
  C2 commit drops the `Proposed paths:` line above once that path resolves.
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

**Added at the Maintainer's instruction: the positive control for a check that
passes by finding nothing.**

*What was put to the Maintainer.* On 2026-10-18, in chat, the coordinating
session (Claude, `claude-opus-5-5`) was reviewing a separate concept document of
the Maintainer's, a research-ecosystem idea called assai, and wrote this, quoted
verbatim:

> "**A negative result needs a positive control.** Cairn has a rule: before trusting an absence, show that the instrument could have detected it. A 'no effect' record should show the analysis would have found an effect of plausible size. Without that, 'not worth pursuing' outputs, which you rightly accept, can carry false nulls into the record."

Under "What could fold back into Cairn" it listed two items: "Planted errors as a
way to grade reviewers" and "The positive-control idea from point 5 belongs in
the scientific-check guidance. That plan is being written right now". It offered
to pass the positive-control point to this plan's author.

*The Maintainer's answer*, verbatim:

> "Pass the positive control point yes, let's not do planted errors."

*Reading, separate from the quoted words.* "The positive control point" is the
quoted point 5. "Planted errors" is the other item: grading reviewers by planting
errors for them to find. The Maintainer declined it, and no artifact takes it up,
so it is out of scope here. It is **not** the deliberate break in the check block,
where the implementer makes the change's own plausible mistake on purpose
(security preflight S2); that is accepted scope. *Provenance.* The chat and the
concept document are not on file in this repository. The two quotations are the
coordinating session's own record, relayed to this plan's author on 2026-10-18,
and are written down here because the plan review could not find the question the
answer belongs to. This is an **addition** to the accepted scope, not a removal;
it owes no disposition, and *Scope delta* records it as an addition. It has no
occurred incident behind it, so, like the independent-basis half of the block, it
rests on argument: AGENTS.md already says "Confirm the instrument before trusting
an absence" for Cairn's own tooling, and this carries the same rule into a
scientific result.

*How the plan settles what the quoted words leave open.*

* **Trigger: the check's pass condition, not the result.** Whether a result is
  "no effect" is unknown at proposal time, and for a refactor "no change" is the
  expected pass. What is known at proposal time is whether the check **passes by
  finding nothing** (no change, no difference, no flow, no effect). The bullet is
  keyed to that. A published null is a result the project acts on, so the change
  that reports one is inside the block's gate, has a check, and, if that check
  passes by finding nothing, this bullet applies to it.
* **Relation to the deliberate break: one record, not two.** The failing run
  proves a check *can fail*. For a check that passes by finding nothing, that is
  already half a positive control. It serves as the control when the mistake it
  makes produces an effect of the size that matters. A second run is owed only
  when it does not, for instance when the break is large and the effect to be ruled
  out is small. Otherwise the bullet asks the author to say plainly that the
  analysis cannot detect it. A refactor whose pass is "output unchanged" is the
  same case: perturb an input by the tolerance and show the comparison fails, and
  that run is both its deliberate break and its control.
* **Who runs it, and where it is recorded.** At implementation, the implementer
  records the control with the failing run, in the plan's *Implementation
  verification* record under its plan-specific acceptance commands. The code
  reviewer verifies it where one is owed, as it verifies the failing run, and
  re-runs both when that is cheap. Showing the control already at the proposal,
  when its data exists then, is allowed and not required.

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
re-anchor already queued on `dev/PLANNING.md`. The re-anchor re-globs the test
folder, so the file freezes at that ceremony, and an edit to it afterwards owes
another. **The re-anchor is Maintainer-only and supervised; an implementing
agent must not perform it.** Because no frozen file changes, `dev/PLANNING.md`
is not edited when this plan opens; the node note is the archive commit's
(chunk M).

**AST: no engine symbol changes.** No file under `bootstrap/_scaffold/` is
edited. The AST attestation baseline (`bootstrap/tests/fixtures/scaffold_ast_baseline.json`,
enforced by `test_ast_attest.py`) is **already red at the parent**, and not
because of this plan. Derived at `b16f4607` in a clean copy by the method in
`bootstrap/AST_BASELINE_RUNBOOK.md` (Step 1): CHANGED 2, MISSING 0, DUPLICATE 0.
The two are `main` in `bootstrap/_scaffold/cli.py` and `seed_gitignore` in
`bootstrap/_scaffold/install.py`. That re-anchor is the Maintainer's and is
owed regardless. Boundary B will therefore show one non-pass that is not this
plan's; C4 disposes of it by showing the same two symbols, with the same
hashes, before and after. **The figure is not to be carried forward**: derive it
again at the parent.

**Lockfile.** Both Cairn template copies already report a hash mismatch in
`python bootstrap/verify_integrity.py --target .` (18 files at `7f1bcdf0`, the
two templates among them). They are **not finalized**: that would re-attest
earlier, unreviewed drift. The set of 18 must be the same before and after C2.

**Install contract: unchanged.** The published `scaffold.py --manifest` lists
destination, source and mode, with no content hashes. No file is added to or
removed from the install set, so `_CORE_MAPPINGS` is untouched. C2 shows
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

Measured on the drafted wording, applied to a clean copy of the plan-review
commit: the eight files above, plus `test_comprehension_floor.py` (which reads
`AGENTS.md`, not these templates, and is run as a control), pass **372** with the
edit and on the unedited control, and **373** with a prototype of the new test
added. The prototype passes on the edited copy and fails on the unedited one with
a missing-marker message. `claim_check.py` exits 0 on all seven edited
documents, and the neutrality leg reports 74 failures on both, none in a file
this plan edits.

### Found while planning, not widened

* **The accepted smoke sentence cannot show a block install.** Revision 1 says
  `scaffold.py --summary --config <profile>` and `--dry-run` "show the block
  installing". Both were run: they print the profile, the tokens and the module
  roster and never open a template. The outcome, that an adopter receives the
  block, is delivered more directly by a real install into a scratch tree and a
  `diff` of the installed region (C2). That is stronger, not weaker, and
  `--summary` and `--dry-run` still run and are recorded.
* **How an existing adopter receives the block.** Measured on the drafted
  wording: install from the parent into a scratch tree, fill the
  `documentation-tier-home` slot in both installed templates, commit, then run
  `scaffold.py upgrade --plan` and `--stage` against the edited tree. `--plan`
  reports both templates "locally-modified (merged clean)". The staged file holds
  the block once, the adopter's slot fill once, and no conflict marker. C2
  repeats this on the real commit.
* **Two small wording choices beyond the quoted drafts.** (a) The plan paragraph
  opens "If the proposal names one, it becomes an acceptance criterion". The
  draft's unconditional "It becomes an acceptance criterion" would read as a
  demand on a proposal that wrote N/A. (b) The *Reviewers* paragraph says the
  Maintainer judges "whether this is the right check and the expected value is
  right" at the Decision. That is Revision 1's *Who does what*, which the quoted
  block draft omits. Neither adds an obligation; both are for the code reviewer to
  strike if they disagree.
* **The "Hydrology examples" in *Who does what* stay out of the template**
  (Theis, Glover–Balmer, an inversion recovering a synthetic truth, a
  post-processor against the model's saved budget). Neither quoted draft carries
  them, and the proposal names "the block grows discipline sub-lists" as a sign
  the change is wrong. The one example the template does carry is the
  streamflow-depletion case that came with the Maintainer's addition, since a
  positive control is the least familiar idea in the block.
* **The I-2 sentence is worded to what is true.** The first draft said the profile
  sections "drive ... which changes must name an independent scientific check".
  The check is gated by the change, not by the profile, and nothing downstream
  reads those sections to decide. The sentence now says the sections show which
  changes touch a scientific assumption and so need the check, which is the same
  claim the complexity text makes ("gated on the change, not on this axis").
* **`check_cairn.py` is not clean at the parent.** At the time of this revision it
  reports an issue in another plan (`dev/plans/neutrality-and-upgrade-slots.md`, an
  imperative-override phrase). Criteria below therefore ask for no issue **in a
  file this plan edits**, with any other issue recorded and shown unchanged.
* **`doctrine/rationale.md` still calls scientific-error detection "without the
  Maintainer in the loop" an open problem.** That stays true: the check puts the
  Maintainer in the loop on purpose. No edit.
* **The nearest live home of the revisit is a row that says nothing about it.**
  `dev/PLANNING.md` > "0.3 external correctness test (R-H third-party probe)"
  does not mention the axis revisit. Adding it is the archive commit's (see
  *Dispositions*), because the Decision says "At archive, the plan adds".

### Sequencing with the other accepted work

Implementation order, as the Maintainer set it on 2026-10-18:
**`neutrality-and-upgrade-slots` (plan C), then this plan**, then the combined
plan `review-stance-and-lenses` (for `external-is-a-maintainer-stance` and
`review-lenses-for-every-install`), then `board-as-basis`, then
`model-mapping-install-path`, then `stewardship-and-reuse`. **This plan rebases
on plan C.** Plan C is
open as `dev/plans/neutrality-and-upgrade-slots.md`; its file list names none of
the template or `dimensions/` files this plan edits (read at the plan-review
commit). Each chunk still re-reads the files it edits at edit time (`git log -3
-- <file>`). `maintainer-attention` and `verification-practice` are archived and
their edits are already in the tree: `dev/plans/_template.md` and its twin carry
the Waiting-line preamble and the `verification-commands` slot, both outside the
*Acceptance criteria* paragraph edited here.

| Plan | Shared with this plan | Effect |
|---|---|---|
| `neutrality-and-upgrade-slots` (before) | **The neutrality checker**: it gets stricter (whole-line HTML comments, `.json` and `.txt` under `templates/`, four more names), and runs in this plan's Boundary B. **`bootstrap/verify_integrity.py`** and `bootstrap/UPGRADE.md`, which this plan does not edit. **`dev/PLANNING.md`** and **`CHANGELOG.md`**, each plan adding to them at its own archive. | The new text names no vendor, comments included, and contains no HTML comment. Plan C's own check that `verify_integrity --target .` still lists 18 files holds here, since both Cairn template copies are on that list already. |
| `model-mapping-install-path` (after) | **`bootstrap/BOOTSTRAP.md`**: it edits II-5 and the allowed-match list; this plan edits the I-2 paragraph. **`dev/PLANNING.md`** at archive. | Different sections, so a textual rebase only. |
| `board-as-basis` (after) | **All four template files**: it adds an `**In brief**:` prompt beside each header; this plan edits other regions. **`dev/PLANNING.md`** and **`CHANGELOG.md`** at archive. | Different regions of the same files, so a textual rebase only. This plan's test reads only the block and the paragraph, not the headers. |
| `review-stance-and-lenses` (after; `dev/plans/review-stance-and-lenses.md`) | **Both template pairs** (the review-tier lines and plan skeletons), **`dimensions/README.md`** (the same Complexity cell), **`dimensions/complexity.md`** (the neighbouring Complex-position bullets), and **`dev/PLANNING.md`**. | That plan rebases on this one and already says the reworded cell must keep naming the check. Here the requirement has a trigger: this plan's test holds the block and the plan paragraph **word for word** and requires `independent scientific check` in all three promise sites. So that plan runs this test, and an edit to either pinned text owes a test edit and, if the re-anchor has run by then, a second re-anchor. It edits neither text. |

`stewardship-and-reuse` (open, not accepted) edits the plan templates' *Scope*,
*Dispositions* and deviation sentence, not *Acceptance criteria*, so it shares no
cell with this plan.

## Sequence

C1 is a gate: it can stop the plan. Every later chunk lands one commit.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | **Try the wording on two past plans, before any file changes.** A fresh-context agent that is not the implementer drafts the block from the wording below and **the proposal as it was first opened**, for two archived LHM plans, with no other access. A second fresh agent scores each draft against a statement of the error later found, written into the record beforehand. Stop if neither would have named a check that fails under that error. | `ready-to-implement` | one commit: the appended `## Retroactive application` record; Status to `implementing` |
| C2 | **Both templates, and the test.** The proposal-template block (with the "passes by finding nothing" bullet) in both proposal copies; the plan-template paragraph in both plan copies; the new test with its first three groups. | C1 not "neither" | one commit |
| C3 | **Repoint the three promise sentences** at the check; the test gains its fourth group. | C2 (the block they name must exist) | one commit |
| C4 | **Boundary B, then the record.** One full run on the finished work, written down. Status to `awaiting-code-review`. | C2, C3 | one commit |
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
  with its source. Say whether you have opened the data and confirmed it holds
  what the check needs; if not, name what you would open to confirm it. If the
  check depends on data that does not exist yet, say so.
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
* **When the check passes by finding nothing.** A check that passes on "no
  change", "no difference" or "no effect" is evidence only if it could have
  found a change. Show the same analysis detecting a known effect of the size
  that matters (a positive control), or say plainly that it cannot. The failing
  run above serves as the control when the mistake it makes produces an effect
  of that size. At implementation, the implementer records the control with the
  failing run. For example, an analysis that reports no streamflow depletion
  from a pumping well first recovers the depletion of a synthetic well at the
  same rate, distance and schedule.

**Reviewers.** The proposal reviewer challenges whether the basis is really
independent of the code under review. The code reviewer verifies the recorded
failing run and, where one is owed, the positive control, and re-runs them when
that is cheap. The Maintainer judges at the Decision whether this is the right
check and the expected value is right. If no independent basis exists, say so;
the Maintainer weighs that, and it is not a reason to invent one.
```

**C2 — the paragraph.** Inserted in *Acceptance criteria*, directly after the
paragraph that begins `A security-touching plan re-answers` (it ends with the
words "fires the" / "check)." across two lines, so anchor on its first words, not
on its last sentence) and before the `acceptance-doc-tooling` slot, keeping the
blank lines the file already has:

```text
**An independent scientific check is accepted scope.** If the proposal names
one, it becomes an acceptance criterion. A replacement qualifies only if it
fails under the error the original names. If nothing qualifies, dropping the
check is a scope reduction under *Scope delta* and needs the Maintainer's
quoted allowance. Saying that the result now rests on the implementation does
not settle it. When the check fails for real during implementation, one line
records whether anything else would have shown the error.
```

**C3 — the three promise sentences.** Each replaces the sentence that promises a
"scientific-trust review lens" that no module installs.

`dimensions/complexity.md`, Complex position, in place of the bullet beginning
"A **scientific-trust review lens** is in the roster":

```text
* The proposal template's **independent scientific check** is expected
  of every change that touches a scientific assumption or a result the
  project publishes or acts on: one check whose expected value neither
  the code nor its tests compute, shown to fail under the mistake it
  names. The block is gated on the change, not on this axis. Here, an
  unexplained "N/A" on a change that touches a scientific assumption or
  a result the project publishes or acts on is a review finding.
```

`dimensions/README.md`, the Complexity row of the axis table. The one line
changes in its last clause only ("whether a scientific-trust review lens is in
the roster."):

```text
| **Complexity** (`complexity.md`) | simple ↔ complex | Review weight and verification depth — how often External review is mandatory, whether an unexplained "N/A" on the independent scientific check is a review finding. |
```

`bootstrap/BOOTSTRAP.md`, I-2. The three lines beginning "Fill the template."
end "... those drive the legacy-agent and / scientific-trust-reviewer decisions
downstream. If uncertain," and become four:

```text
Fill the template. Do not skimp on the scientific-surface and
documentation-trust sections — those drive the legacy-agent decision,
and the scientific-surface section shows which changes touch a
scientific assumption or a result the project publishes or acts on, and
so need the proposal template's independent scientific check. If
uncertain,
```

**The new test** (`bootstrap/tests/test_scientific_check_guidance_ships.py`) has
**one** function, `test_the_check_guidance_reaches_every_copy_and_promise_site`,
following the shape of `test_installed_templates_carry_security_preflight_questions`
in `test_scaffold.py`: the groups accumulate into one failure list, so every
group runs every time. It holds the two fenced C2 texts above as literals
(`_PROPOSAL_BLOCK`, `_PLAN_PARAGRAPH`), as the accepted text asks ("holds the
block and the plan sentence word-for-word"). That pins every word, including the
ones a clause-level anchor would miss ("only if", "becomes", "written down before
the result is seen"), at the price of editing the test whenever either text
changes. Its docstring says why (the two pairs must not drift, and a clause
deleted from both copies at once must not go unnoticed) and cites no finding,
chunk or plan row. It reads the files by path from the repository root, the way
`test_scope_reduction_trap.py` does.

* **(a) The block.** In each proposal copy the block is the lines from the
  heading line (`### Independent scientific check`, the whole line) up to, not
  including, the next line that starts `## `. Its whitespace-collapsed text must
  equal `_PROPOSAL_BLOCK`'s. Equality, not containment, so a sentence added to one
  copy is also caught.
* **(b) The paragraph.** In each plan copy the paragraph is the lines from the one
  starting `**An independent scientific check is accepted scope.**` to the next
  blank line. Its whitespace-collapsed text must equal `_PLAN_PARAGRAPH`'s.
* **(c) Placement.** In each proposal copy the block heading lies after the line
  that starts `**Prospective only.**`, which ends the security-preflight slice,
  and the block holds no `cairn:slot` or `cairn:end` marker. In each plan copy the
  paragraph holds none either.
* **(d) The promise sites** *(added in C3)*. Each of `dimensions/complexity.md`,
  `dimensions/README.md` and `bootstrap/BOOTSTRAP.md` contains `independent
  scientific check` in its whitespace-collapsed text, and `dimensions/complexity.md`
  contains the sentence `an unexplained "N/A" on a change that touches a
  scientific assumption or a result the project publishes or acts on is a review
  finding`. **Presence only, never absence**, so the later plan
  may reword the Complexity cell without touching this group, provided it keeps
  naming the check.
* A heading or lead line that occurs other than once, or a block with no closing
  `## ` line, raises an `AssertionError` naming it. It never yields an empty
  region, since two empty regions would be equal. A failure names the copy and the
  first sentence that differs.

## Acceptance criteria

**Reading these criteria.** Each ends with *Red when*: a change that turns it
red. Every "mutate" step runs in a **throwaway `git worktree`** at the chunk's
commit, in a fresh, empty folder: the new test and `test_scaffold.py` read the
files of the tree they sit in, so a scratch copy of one file would never be
read. Each mutant is reported as killed, survived or equivalent, beside an
unmutated control run in the same worktree, and a mutation harness is checked on a
case known to be live (a deletion made in the wrong place of the file is not a
survivor, it is a bad mutant). The files under test are the four template copies
and the three promise sites, listed from the tree (`git ls-files` for
`_template.md` under `dev/` and `templates/core/dev/`; `git grep` for the old
phrases), not from the diff. Doc tooling: `python scripts/check_cairn.py` is the
prose smoke, and `python scripts/claim_check.py <file>` runs on every edited
document.

### C1

* **The inputs are fixed first, as the proposals were first opened.** A block is
  filled in when a proposal is opened, before any reviewer speaks, so a draft is
  only a test if it sees that text and nothing later. Before any draft is read, the
  record names, with commits:
  * the wording (the "Wording each chunk lands" texts at the commit where C1
    starts);
  * for `dev/plans/archive/stor-modflow-correctness.md`: the source proposal
    `dev/proposals/archive/2026-08-27-claude-stor-modflow-flopy-layer.md` **as
    opened**, LHM commit `b9d4c59a` (`git show b9d4c59a:` plus its unarchived path
    `dev/proposals/2026-08-27-claude-stor-modflow-flopy-layer.md`, in the LHM
    repository; 427 lines, no review in it, no mention of priming, and it already
    holds the unverified claim that the 137 MB run output "carries the model's own
    `unsatStorage`"). **Not** the text at its Decision, `9dc9acfb`: that file is
    1,907 lines and holds two External reviews and four responses, which name the
    priming and RAMP defects the exercise asks about;
  * for the second plan, the source proposal as opened and the part this plan
    implements (see the next bullet).
  *Red when:* any input is chosen after a draft is read, or the stor-modflow input
  is the Decision-time text.
* **The second plan is chosen by a rule, before the exercise.** The rule: among
  archived LHM plans, newest first **by archive commit date**, the first in which a
  code review or a later record found an error in a **computed result** (not in
  structure, tests or documents). Applied at plan review, it picks
  `dev/plans/archive/2026-10-01-claude-assemble-part-a.md` (archive commit
  `72ccf3db`, 2026-10-15): its code review CR1 found that the default build writes
  NaN land-use weights from a 0/0 renormalization when no cell is partly covered.
  The implementer re-applies the rule and records the result and why it
  qualifies. Its source proposal is
  `dev/proposals/archive/2026-10-01-claude-assemble-full-port.md`, as opened at LHM
  commit `dde80719` (`git show dde80719:` plus its unarchived path
  `dev/proposals/2026-10-01-claude-assemble-full-port.md`; 360 lines), which
  covers six plans. The brief names the part this plan implements: plan 1 of 6, the
  foundation. If **no** LHM plan qualifies, the implementer does not substitute
  one from another repository: that is a deviation request to the Maintainer
  (Waiting line). *Red when:* the plan is picked for how well the block fits it.
* **The draft is blind, and has nothing else to read.** A fresh-context agent that
  is neither the implementer nor a later scorer receives **two texts and no
  repository access**: the wording, and the proposal text at the named commit,
  pasted into the brief. No path into the LHM repository, no error statement, no
  review. Its draft goes into the record **verbatim** before any scoring. *Red
  when:* the brief holds anything else, or the draft is paraphrased.
* **The errors are stated in advance.** Before drafting, the record holds one or
  two sentences per plan stating the error later found, with its citation. For
  stor-modflow: the percolation stack was not primed, which offset the
  domain-mean unsaturated anomaly by about 14.9 kg m⁻² (the full-series mean went
  from +13.5 to −1.2), and the RAMP-period shift was left out (about −0.15);
  both were found by the External code review at LHM `983d6c58` and fixed at
  `6dcc0cc5`, and the reference array the first check relied on had never been
  saved (found by the Internal plan review at `dae97b43`, withdrawn at `7a9771f5`).
  For the second plan: the CR1 finding above. *Red when:* a statement is written
  after a draft is read.
* **A third agent scores.** A fresh-context agent that is neither the drafter nor
  the implementer receives each draft verbatim and the matching error statement,
  and answers two questions, **quoting the draft sentence that carries each
  "yes"**:
  * **(A)** Does the draft name a check that fails under that error?
  * **(B)** Is that a check that could have been run? The draft's data-status
    statement must either confirm the data in hand and name what was opened, or say
    the data is not confirmed **and name what would be opened to confirm it** (a
    file or an array). A stock hedge that names nothing does not count. Where the
    record shows the draft's data claim to be false or never checked (for
    stor-modflow, that the run's saved output carried `unsatStorage`), a draft that
    repeats the claim as "in hand" fails (B).

  A plan's verdict is **yes** when (A) and (B) are both yes. Whether the basis is
  one the block lists, and independent of the code under review, is recorded for
  each draft and **not scored**. *Red when:* a "yes" has no quoted sentence, or the
  scorer is the drafter or the implementer.
* **The reading of the accepted test is stated, and its effect is reported.** The
  accepted question is whether an author following the block "would have named a
  check that fails under the error later found". This plan reads "a check that
  fails" as a check that can be run, which is why (B) is part of the verdict:
  without it (A) is "yes" for any draft that repeats the original compare-with-saved-
  output check, and the exercise could not fail on stor-modflow, the very ritual it
  exists to detect. The record also reports each plan's verdict on (A) alone, so
  the Maintainer sees whether (B) decided it. *Red when:* the record gives only the
  combined verdict.
* **The stop rule is the accepted one.** If both verdicts are **no**, the block is
  judged ritual: the plan stops, and nothing in C2–C4 is committed. If at least
  one is **yes**, the plan proceeds, and the record says in plain words which plan
  it was and what the other showed. One "no" is reported to the Maintainer in the
  record and in the archive commit; it does not stop the plan. *Red when:* the
  stop is softened to a warning, or hardened to "either".
* **The null-result bullet is not claimed as tested.** Neither plan found a
  false null, so the record says the "passes by finding nothing" bullet has no
  occurred instance behind it and rests on argument. *Red when:* the record cites
  either plan as support for it.
* **The record is appended, once.** An H2 `## Retroactive application -- <agent>
  -- YYYY-MM-DD`, with the items above. `claim_check` on this plan is clean after
  it, with the LHM paths on the `External-repo paths:` line. The commit sets
  Status to `implementing`.

### C2

* **The block is where the wording says, once, in both proposal copies.**
  `grep -c '^### Independent scientific check$'` prints 1 for each of
  `dev/proposals/_template.md` and `templates/core/dev/proposals/_template.md`,
  and the heading sits after the line starting `**Prospective only.**` and before
  `## Signals the change is wrong`. *Red when:* it sits before that line (inside
  the preflight slice) or in a slot.
* **The paragraph is where the wording says, once, in both plan copies.** The line
  starting `**An independent scientific check is accepted scope.**` occurs once in
  `dev/plans/_template.md` and in `templates/core/dev/plans/_template.md`, after
  the paragraph that begins `A security-touching plan re-answers` and before the
  `acceptance-doc-tooling` slot. *Red when:* it sits inside the slot or above the
  security-preflight paragraph.
* **The preflight slice is unchanged.** Extract the slice from each proposal copy
  with `_extract_security_preflight` (imported from `test_scaffold.py` in a
  throwaway snippet) at C2's parent and at C2's commit: the two slices are
  byte-identical in each copy. *Red when:* the slice grows. This is the "must not
  swallow the block" property, measured.
* **The bytes are the reviewed bytes, three ways.** After trimming trailing blank
  lines, the block extracted from each proposal copy and the paragraph extracted
  from each plan copy are `diff`-identical (exit 0) to the fenced C2 texts in this
  plan; and the literals in the test, whitespace-collapsed, equal the same fenced
  texts. *Red when:* any word differs; the implementer then revises the plan, not
  the template.
* **The "passes by finding nothing" bullet is whole.** In each proposal copy it
  occurs once, opens "When the check passes by finding nothing", names the three
  absences ("no change", "no difference" or "no effect"), says the control is the
  failing run above when that run's mistake produces an effect of the size that
  matters, says the implementer records the control with the failing run, and
  keeps the streamflow example. The *Reviewers* paragraph names the positive
  control "where one is owed". *Red when:* the bullet is keyed to "the result" and
  not the check's pass condition, or the owner or the recording place is missing.
  The test (a) catches each by the literal.
* **The new test is one node, and it can fail.** `pytest --collect-only -q
  bootstrap/tests/test_scientific_check_guidance_ships.py` lists exactly one test,
  and it passes at C2 (groups a to c). In the worktree at C2, with an unmutated
  control run first (passes), the following are each run and reported:
  * (m1) change one word of the block in the Cairn proposal copy only; (m2) the
    same in the shipped copy only; (m3) change one word of the paragraph in one
    plan copy only; (m4) delete the paragraph from one plan copy;
  * (m5) delete **each sentence or list item** of the block, in turn, from
    **both** proposal copies, and (m6) each sentence of the paragraph from **both**
    plan copies. The set is listed from the fenced texts, not from memory, and each
    deletion is made inside the block's own region, not at the first occurrence in
    the file (the words `For every other change, one line` also open a sentence of
    the security preflight);
  * (m7) weaken "qualifies only if" to "qualifies if" in both plan copies; (m8)
    weaken "it becomes" to "it may become" in both plan copies;
  * (m9) remove the block heading from both proposal copies; (m10) move the
    heading above the `**Prospective only.**` line in both.

  Expected: every one killed (m4 and m9 by the missing-marker message, m10 by
  group c). A prototype of the test, run at planning time against an equivalent set
  of 50 mutants, killed every one once a mutant applied at the wrong place in the
  file was redone. *Red when:* any survives; a survivor is reported as a survivor.
* **Existing pins pass unedited.** The eight files named under *Tests that read
  the touched files*, plus `test_comprehension_floor.py`, pass with the same
  count as the unedited parent (372 at planning time; the implementer records both
  figures at the parent and at C2).
* **No vendor or project name.** The neutrality leg's `file:line` list at C2 is
  **identical** to the parent's (a count can match while the set changes), and no
  line is in a file this plan edits. A `grep -n -E
  'Claude|Codex|Anthropic|OpenAI|Gemini|Cursor|LHM|modflow_tools'` over the added
  lines prints nothing; first run it over a line known to hold one (the instrument
  check). *Red when:* the pattern finds a known hit on neither run, or the lists
  differ.
* **The install contract is unchanged.** `python bootstrap/scaffold.py --manifest`
  at C2 and at its parent `diff` to exit 0.
* **An adopter receives both texts.** Install into an empty scratch tree
  (`bootstrap/profiles/solo-greenfield.yml`, `--non-interactive --allow-dev`). The
  installed `dev/proposals/_template.md` holds the block and the installed
  `dev/plans/_template.md` holds the paragraph, each `diff`-identical to the
  source, with no `{{` inside either. `--summary` and `--dry-run` are also run and
  recorded; they cannot show content. *Red when:* an installed region differs.
* **An existing adopter's upgrade keeps their work.** Install from the parent, fill
  the `documentation-tier-home` slot in both templates, commit, then `upgrade
  --plan --cairn-root <C2 tree>` and `--stage`: each template is classified
  "locally-modified (merged clean)", and each staged file holds its new text once,
  the slot fill once, and zero `<<<<<<<` markers. *Red when:* a conflict marker
  appears or a slot fill is lost.
* **The lockfile is left alone.** `python bootstrap/verify_integrity.py --target .`
  reports the same findings at C2 and at its parent (18 at planning time), none
  newly attributable to this chunk; no finalize is run.
* **The plan template's own pins stand.** `test_scope_reduction_trap.py` and
  `test_verification_boundaries.py` pass unedited, the plan template still holds no
  `## Implementation verification` H2, and `grep -nE '^ *([*-] )?\*\*Waiting on
  Maintainer\*\*' dev/plans/_template.md templates/core/dev/plans/_template.md`
  prints nothing, as at the parent.
* **The prose gates are clean where this plan wrote.** `python
  scripts/claim_check.py` exits 0 on the four template copies, and `python
  scripts/check_cairn.py` reports no issue in a file this plan edits. Any issue
  elsewhere (one, in another plan, at the time of this revision) is recorded by
  file and line and shown unchanged from the parent.
* **This plan's own header is tidied.** The C2 commit drops the `Proposed paths:`
  line for the test file, because the path now resolves (the checker flags a
  stale declaration), and `claim_check` on this plan is clean.

### C3

* **The old promise is gone from all three sites, and the new one is in them.**
  `git grep -n -i 'scientific-trust' -- dimensions bootstrap/BOOTSTRAP.md` prints
  three lines at the parent (the instrument check) and **nothing** at C3.
  `independent scientific check` occurs in each of the three files. *Red when:*
  any site still names the lens, or any lacks the check.
* **The complex-project finding is stated.** `dimensions/complexity.md` holds the
  sentence about an unexplained "N/A" on a change that touches a scientific
  assumption or a result the project publishes or acts on being a review finding,
  once, in the Complex position, and the "gated on the
  change, not on this axis" sentence. *Red when:* it sits in Simple, or either
  sentence is missing.
* **The I-2 sentence says what is true.** It says the profile sections show which
  changes touch a scientific assumption, and does not say the profile decides
  which changes need the check. *Red when:* the sentence says the sections "drive"
  or "decide" which changes name a check.
* **No axis, axis value or gate-table row changed.** `git diff -U0` over the three
  files shows exactly three hunks, none inside the I-4 or I-5 tables or the axis
  rubric; `dimensions/README.md`'s edited row has the same number of `|`
  separators as at the parent. *Red when:* a fourth hunk appears or the row's cell
  count changes.
* **The text is bytes-as-reviewed.** In `git diff -U0`, the added lines of each
  hunk equal the fenced C3 text exactly, and the removed lines are exactly the
  old ones named above. *Red when:* a word differs or a hunk removes anything else.
* **The test's fourth group is live, and stays one node.** The collection still
  shows one test and it passes at C3. In a worktree at C3, with a control: replace
  `independent scientific check` by `review` at each of the three sites in turn
  (3 mutants), and change `review finding` to `note` in `dimensions/complexity.md`;
  all four are killed by group d. A fifth, restoring the old phrase "scientific-trust
  review lens" **beside** the check in one site, passes (presence only, by design).
  *Red when:* a replacement survives, or the fifth is killed.
* **The line that is not a promise stays.** `templates/modules/team-gated/architecture_review_template.md`
  still carries its own "Scientific Trust" lens line; this plan does not edit it,
  because that module does ship a lens set. *Red when:* the file is in the
  chunk's `git diff --stat`.
* **Gates.** `test_profile_grammar.py` passes; `check_cairn.py` reports no issue in
  a file this plan edits; `claim_check.py` exits 0 on each of the three; the
  neutrality `file:line` list is identical to the parent's; no vendor or project
  name on any added line (same instrument check as C2).

### C4

* **The record is complete.** `## Implementation verification -- <agent> --
  YYYY-MM-DD` carries each field *Verification* lists: mode, tested commit,
  reviewed range, interpreter, pre-run and post-run state, the command table with
  exit, outcomes and elapsed, the non-pass disposition, the plan-specific commands,
  and known omissions. It lists the new test's node ID, which matches `pytest
  --collect-only -q` for the added node, and the mutation ledgers of C2 and C3.
  Where the implementation ran a check that passes by finding nothing, its control
  is recorded here, beside the failing run. *Red when:* a field label is absent or
  the node ID differs.
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
| Edit 2: the plan paragraph (accepted scope; a replacement qualifies only if it fails under the original's error; scope reduction and the Maintainer's quoted allowance; "rests on the implementation" does not settle it; one line when the check fails for real) | C2 |
| Edit 4: the promise repointed at the check alone, at `dimensions/complexity.md`, `dimensions/README.md` and `bootstrap/BOOTSTRAP.md`, with the complex-project "N/A" finding and no axis, value or gate-table change | C3 |
| Both template pairs match outside their slots; one new test holds the block and the plan sentence word-for-word identical across the twins | C2 (groups a to c) |
| The falsification test that runs before landing (two plans; stop if neither) | C1 |
| Done-when gates: claim check, prose integrity, neutrality and redundancy, no vendor named | C2–C4 |
| Smoke: the block installs | C2 (a real install; see *Found while planning*) |
| Boundary B full, Python 3.13.x | C4 |
| Archive: the guide star's open-gap entry, a CHANGELOG line, the axis revisit added to the third-party probe row | *Dispositions* |
| The revisit's trigger, falsifiers and signals have a live home; #19 stays open | *Dispositions* |

**Already conceded, not re-opened here.** Edit 3, the lens-8 doctrine sentence, was
removed by the proposal's own Scope delta and conceded by the Maintainer's Q1
answer. Its disposition is `defer`, homed on the board row "The
independent-scientific-check rule as doctrine (#19)" in `dev/PLANNING.md`, with
the Decision quoted there. This plan removes nothing further, so it owes no
`disposition` lines.

**Additions beyond the baseline, none of them a removal.** (1) The positive
control for a check that passes by finding nothing, at the Maintainer's
instruction, recorded under *Scope* (the bullet and one reviewer clause, C2; held
word for word by the test). "Planted errors" is out of scope. (2) The test's
fourth group, which pins the three promise sentences (C3): the accepted evidence
names one test, and this is a group inside it, so the node count is unchanged. (3)
The C1 verdict reads "a check that fails" as a check that can be run, stated in
C1 and reported beside the plain reading so it cannot hide a result.

## Verification

**Boundary A (iteration, scoped).** Each chunk runs the tests that own the files
it touches, plus `python scripts/check_cairn.py` and `python
scripts/claim_check.py` on each edited document. All tests are in
`bootstrap/tests/`.

| Chunk | Tests and gates |
|---|---|
| C1 | `claim_check.py` and `check_cairn.py` on this plan; no pytest |
| C2 | the new test; `test_scaffold.py` (installed-template and preflight-slice tests); `test_scope_reduction_trap.py`; `test_verification_boundaries.py`; `test_documentation_plan_module.py`; `test_core_dev_folders.py`; `test_quickstart_sequence.py`; `test_claim_check_module.py`; the neutrality and redundancy legs; the scratch installs and the upgrade probe |
| C3 | the new test; `test_profile_grammar.py`; the prose gates; the neutrality and redundancy legs |
| C4 | the full suite (below) |

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

**How it runs.** After the last implementation chunk (C3), against a clean,
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

then `claim_check.py` on each edited document, the scratch installs, the upgrade
probe, and `verify_integrity --target .` before and after.

**Expected non-pass**, each disposed of rather than treated as noise. These are
the ones known at planning time; **derive the real list from a full run at the
parent**, in the same way, and do not carry this list forward:

* **`test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package`**
  is red at the parent on two symbols (see *AST*). The record shows the set is
  unchanged by this plan.
* **The neutrality leg** carries 74 pre-existing failures at `7f1bcdf0`, until plan
  C lands (it is meant to bring the count to zero). Record the `file:line` list at
  the tested commit and confirm it equals the parent's, with no hit in a file this
  plan edits or on a line it added.
* **`check_cairn.py`** reports an issue in another plan at the time of this
  revision. Record any such issue by file and line; it is not this plan's.
* **`test_gate_manifest.py`** has no expected failure: changed frozen bytes do not
  redden it, and no frozen file changes here.

**Known omissions.**

* **The promise sites are pinned for presence only.** The test requires the check
  to be named at all three sites and the "N/A" finding to be stated in
  `dimensions/complexity.md`. It does not forbid the old lens phrase from
  returning, by design: the later plan that rewords the same cell must be free to
  do so while keeping the check. A lens promise restored beside the check would go
  unnoticed by the suite; C3's grep and Boundary C look for it once.
* **The block and the paragraph are pinned word for word.** Any later edit to
  either owes an edit to the test and, once a re-anchor has frozen the file,
  another re-anchor. That is the cost of pinning every word, and the reason the
  sibling plan is told to leave both texts alone.

**Boundary C** is the code reviewer's, run after Boundary B. The points worth
attacking:

* **Is the independence real?** Pick one bullet of the five and try to write a
  "check" that satisfies the words and still shares the code's wrong convention.
  If that is easy, the block is a ritual (the F2 sign).
* **Does the null-result bullet misfire, or duplicate?** It should ask for a
  control only where the check passes by finding nothing. Read it against a
  tooling change, against a change whose check finds an effect, and against a
  refactor whose pass is "output unchanged". For each, is the deliberate break
  enough, with no second run owed? Where it is not, does the bullet say a second
  run or a plain "cannot"? And can an implementer tell, from the bullet alone, who
  records the control and where?
* **The gate.** Does the opening sentence send a pure-tooling change to N/A, and a
  change that touches a computed result to a check? Both ways, with the proposal's
  own "gate misfires" sign in mind.
* **Read cold as an adopter.** A solo scientist with one agent has no `doctrine/`,
  no dual-review module, and no second reviewer. Can they follow the block, and the
  plan paragraph, from the shipped templates alone?
* **The set.** Re-run C2's sentence-by-sentence deletion on the reviewed commit,
  listing the sentences from the tree, and mutate each of the three promise sites
  separately; report anything nothing catches.
* **The upgrade.** Re-run the stage probe on the reviewed commit with an adopter
  who has *edited the block*, not only a slot, and see what the merge does.
* **The C1 record.** Is each "yes" supported by a quoted sentence of the blind
  draft, were the inputs the proposals as opened, and was the second plan chosen
  by the rule? Does the record show the verdict on (A) alone beside the combined
  one?

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
  falsifiers and the warning signs are not left in an archived file:
  * **Falsifiers.** **F1** every failing check's record names something else that
    already showed the error; **F2** most bases are "the Maintainer's
    expectation"; **F3** changes that touched an assumption carry N/A; **F4**
    recorded failing runs are absent or cannot be reproduced; **F5** failing
    checks keep coinciding with errors code review also catches (a smaller claim,
    still worth having); and **F6**, added by this plan with the positive control:
    no check that passes by finding nothing carries a control or a plain statement
    that none exists. "If nothing fails and no later error surfaces, the result is
    inconclusive, not a pass."
  * **Signals the change is wrong**, the proposal's four: checks are written after
    the code, with the expected value shifting at code review to match the result;
    a data status reads "in hand" and is not; the gate misfires (N/A on changes
    that touch results, or a ritual check on tooling); and the block grows
    discipline sub-lists, which is the axis arriving by accretion.
  * The revisit also reads the C1 record.
* **It adds the new test's node ID to the queued re-anchor row** (chunk M), under
  the same rule as the earlier plans: one node, in a new file the re-anchor will
  freeze, dropping none. The ceremony itself stays the Maintainer's.
* **It confirms the issues' state** and edits neither: #18 `CLOSED` (done
  2026-10-18), #19 `OPEN`. #18's export-safety affirmation is not touched.
* **This plan carries no Waiting line at archive**: the open wait, the re-anchor,
  is declared on its marked board row.
* **Not owed:** the deferred doctrine sentence (already on its own board row), the
  `deliverable` axis and its disciplines (#19), and the AST and neutrality
  baselines (not this plan's).

## Plan review -- Claude Sonnet 5.5 (Internal) -- 2026-10-18

**In plain terms.** The plan delivers what the Decision accepted, and its edits are small and in the right files. I applied its exact wording to a scratch copy and the existing tests, the prose gates and the install manifest did not move. Nine findings follow; three matter most. The blind-draft gate (C1) shows its drafter the very error it is meant to test, so it cannot fail on its own terms. The new test would stay green if a key sentence of the block were deleted from both copies. And the "no effect" addition, which the Maintainer asked for, does not say who runs the positive control, or when. None of these changes what the plan sets out to do. This is one Internal round, so the author folds the fixes into the plan's cells and the plan goes to `ready-to-implement` without a second pass.

```
Reviewed commit: 5ee3c9efff43dcb3a7c68e84e78f88319ae3daad
Target: the whole plan (Source proposal through Dispositions), read against Revision 1 and the Decision of the archived source proposal, plus the Maintainer's quoted addition; the quoted wording was applied to a detached copy of this commit
Prior findings: none
Assurance path: high-assurance (inherited, as the plan declares)
```

**Obligation**: `**Plan review**: required(Internal)` -- the one fresh-context Internal plan-review pass; no second round
**Tier**: Internal
**Findings**: raised

### The two foundational questions

**1. Does the plan deliver everything the Decision accepted, and nothing it did not?** Yes on outcomes, with four gaps in how they are delivered.

* *Delivered.* Revision 1's three edits map to C2, C3 and C4. Its done-when conditions map to C2 to C5. Its archive duties (guide-star entry, changelog line, axis revisit on the third-party probe row with falsifiers F1 to F5, issues #18 and #19) are in *Dispositions*. I read both issues: #18 is closed, with a comment saying "Closed as a duplicate of #19", and #19 is open. The lens-8 sentence is correctly outside the baseline, as the proposal's own scope delta and the Maintainer's Q1 settle.
* *The smoke sentence cannot be met as written, and the plan is right to say so.* Revision 1 says `--summary` and `--dry-run` "show the block installing". I ran both against a tree that holds the block: neither output contains it (0 matches in 21 and 9 lines). The plan's replacement, a real install into a scratch folder plus a `diff`, does deliver the outcome. I ran it: the installed proposal and plan templates hold the block and paragraph verbatim.
* *Quietly reworded or dropped.* The plan discloses its two wording choices (`:249-256`) and its decision to leave the hydrology examples out of the template (`:257-263`). I accept all three: the examples are illustration, not an outcome, and the proposal's own fourth warning sign is the block growing sub-lists. One thing is **not** disclosed: Revision 1's four "Signals the change is wrong" are accepted contract text, and only part of one (gate misfires, via F3) has a home after archive (SC-PR8).
* *Added beyond the Decision and the quoted addition.* The "yes" condition (b) in C1's verdict is stricter than the accepted test, while `:515` calls the stop rule "exactly the accepted one" (SC-PR2). The test's *duties* group is an addition to "identical across the twins", and it is the weakest part of the test (SC-PR3). F6 and the streamflow example are disclosed and belong to the Maintainer's addition.
* *The addition is recorded as one.* *Scope* (`:121-135`) and *Scope delta* (`:694-697`) both say it adds to the floor and removes nothing, and it carries the Maintainer's words verbatim. It is not fully specified (SC-PR4).

**2. Is there a simpler path to the same outcome?** Not for the outcome the Decision accepted. Four template files, three sentences and one test is already the minimum, and C1 is accepted scope. The weight is in verification (36 acceptance bullets, two mutation ledgers, three install probes). Three trims lose nothing: (a) fold C3 into C2, so the test is written once and the install and upgrade probes run once on the finished templates; (b) replace the thirty-one short duty anchors with the ten or so clause-level ones in SC-PR3, which covers more with less; (c) pin the promise sentences in the same test node (SC-PR5) instead of relying on a reviewer's memory. I do not recommend dropping or shrinking C1. I recommend making it able to fail.

### Findings

**SC-PR1 -- High -- C1's "blind" draft can read the error it is meant to be blind to.**
* *Evidence.* `:475-487` fixes the stor-modflow input as LHM commit `9dc9acfb`, the proposal "as it stood at its Decision". `:498-503` says the drafter gets "nothing from ... a review". At `9dc9acfb` that file is 1,907 lines, with two External reviews and four responses inside it (the first `## Review` is at line 429). The Round-2 review says, at lines 1422 to 1425, "Cold start vs 365-day priming -- a defect ... Must fix: prime over the same window". The RAMP concern is at lines 583 to 597. Priming and the RAMP shift are exactly the two errors C1 asks whether the block would have caught. The proposal as first opened is LHM commit `b9d4c59a` (`git show b9d4c59a:dev/proposals/2026-08-27-claude-stor-modflow-flopy-layer.md`): 427 lines, no reviews, no mention of priming, and it already holds the unverified data claim (lines 168 to 180: the 137 MB `OUTS` file "carries the model's own `unsatStorage`").
* *Why it matters.* The block is filled in when a proposal is opened, before any reviewer speaks. A draft written after reading the reviewers' "must fix" tells you nothing about the block. The gate would pass for the wrong reason. The same applies to the second plan: its source proposal (the assemble-full-port proposal in LHM) covers six plans, and the draft needs to know which part it is drafting for.
* *Fix.* In the C1 criteria: (1) the input is the proposal as opened, naming `b9d4c59a` for stor-modflow and, for the second plan, the commit that opened its source proposal and the part the plan implements, all recorded before any draft is read; (2) the drafter gets that text and the wording, with no repository access beyond it; (3) "newest first" means by archive commit date. By that rule `dev/plans/archive/2026-10-01-claude-assemble-part-a.md` (archived 2026-10-15) is first, and its CR1 (NaN land-use weights from a 0/0 fill) is a computed-result error, so the "consider first" hint at `:491-493` can go.

**SC-PR2 -- Medium -- The C1 verdict is the implementer's to give, and the rubric leaves room.**
* *Evidence.* `:504-520`. (1) The person who knows the error and wants the plan to proceed scores the draft; only code review, after C2 to C5 have landed, can check it. (2) Question (a) is "if its data were in hand, does it fail under the error". For stor-modflow the opening text already contained a compare-with-saved-output check, so (a) is "yes" for nearly any draft, and that plan's verdict rests on (b) alone. (3) Question (c), independence, is asked but is not in the verdict rule. (4) The verdict needs (a) and (b), which is stricter than the accepted test ("a check that fails under the error later found"), yet `:515` says the stop rule is "exactly the accepted one".
* *Fix.* Someone other than the drafter and the implementer scores: a fresh agent, given the draft verbatim and a one-or-two-sentence statement of each error written into the record before drafting. Each "yes" quotes the draft sentence that carries it. For (b), the quote is the draft's own statement of data status, and "not confirmed in hand" counts only if it names what would be opened to confirm it (a file or an array), so a stock hedge does not pass. Say that (c) is recorded and not scored. Either keep `:515`'s wording and drop (b) from the verdict, or say that (b) is an added condition that can only make the plan stop more often, and report it as such in the C1 record.

**SC-PR3 -- Medium -- The test's *duties* group does not catch what its docstring promises (measured).**
* *Evidence.* I built a throwaway version of the test from `:431-458` (parity, 24 + 7 duty anchors, placement), outside the repository. On the wording applied to a copy of this commit it passes; on the unedited parent it fails with four missing-marker messages (the instrument works). Mutants m1 to m10 from the plan behave as the plan predicts, with one slip: m9 is killed by the missing-marker message, not by parity as `:605-611` says. Then I deleted one clause from **both** copies at a time, so parity could not notice. Survivors (every anchor still found, parity equal): the independence definition "Neither the proposed code nor a test written from the same understanding computes it"; "(a closed budget does not catch a wrong input)"; "written down before the result is seen"; "the Maintainer weighs that, and it is not a reason to invent one"; "and the tolerance with its source"; the trigger list ("a governing equation ... between models"); and in the plan paragraph, "qualifies only if" changed to "qualifies if" and "it becomes" changed to "it may become" an acceptance criterion. The anchors name the topic of each duty, not the clause that makes it binding.
* *Why it matters.* The docstring the plan prescribes says a duty deleted from both copies must not go unnoticed. The first four survivors are the rule the Decision accepted: what independence means, why a closed budget is not a check, that the expert's expectation comes before the result, and the guard against inventing an independent basis.
* *Fix.* Add clause-level anchors for at least: `Neither the proposed code nor a test written from the same understanding computes it`; `a closed budget does not catch a wrong input`; `written down before the result is seen`; `it is not a reason to invent one`; `tolerance with its source`; and in the plan paragraph `qualifies only if it fails under the error the original names` and `it becomes an acceptance criterion`. The sibling test `bootstrap/tests/test_review_and_verification_rules_ship.py` matches each obligation by pattern and keeps node IDs fixed so rewording never drops a node; this plan's single node is already stable, so this adds anchors, not nodes. The simpler alternative is to hold each region as one whitespace-collapsed literal in the test; that pins every word, at the cost of editing the test whenever the block changes. Either is acceptable.

**SC-PR4 -- Medium -- The positive-control addition is not fully specified.**
* *Authority.* The quote (`:121-135`) is a reply to a question the plan does not record: "Pass the positive control point yes, let's not do planted errors." I searched `dev/`, `doctrine/` and `docs/`: "planted errors" appears nowhere before this plan, and "the positive control point" is not in the source proposal or its reviews. A later reader cannot tell what was put to the Maintainer or what was declined, and the relayer is unnamed. `AGENTS.md` asks a scribe to act only on an instruction that is unambiguous; that rule is written for Decisions, but a scope addition deserves the same care. *Fix:* add two or three sentences in the plan's own words saying what the point was, what "planted errors" would have been, who relayed it, and when; if the summary the Maintainer saw is not on file, say so.
* *Trigger.* The block says "When the result is 'no effect'" (`:359`). At proposal time the result is not known, and for a refactor, "no change" is the expected pass. *Fix:* "If the check passes by finding nothing (no change, no flow, no effect) ...".
* *Owner and timing.* The error bullet says the implementer makes the mistake and records the failing output (`:357-358`). The "no effect" bullet does not say who runs the positive control, or where it is recorded, yet the *Reviewers* paragraph (`:367-368`) has the code reviewer verify "the recorded failing run and the positive-control run". *Fix:* one clause, parallel to the error bullet: at implementation the implementer runs it and records the output beside the failing run (or, if the data exists when the proposal is written, the author shows it there). Add an anchor for that clause (SC-PR3).

**SC-PR5 -- Medium -- The three promise sentences stay unpinned, and the stated reason does not hold.**
* *Evidence.* `:759-763` says a second pin file "is a larger ceremony". A fourth group inside the one test needs no second file and no new node. I replaced `independent scientific check` with `review` at all three promise sites in the scratch copy: `test_profile_grammar.py`, `test_scope_reduction_trap.py` and `test_scaffold.py` (211 tests) and `check_cairn.py` all stayed green. The one constraint that matters, that the External-stance plan keep the check named in the Complexity cell, is a note "for its author" (`:289`) with no trigger. That plan is accepted and binds itself to this: its Decision keeps "the scientific check once it lands" in the Complex position (`dev/proposals/2026-10-18-claude-external-is-a-maintainer-stance.md:776-779` and the Decision at `:1511-1514`). Nothing makes its author see this plan.
* *Fix.* A fourth group in `test_every_template_copy_carries_the_same_check_guidance`: each of the three files contains `independent scientific check`, and `dimensions/complexity.md` contains the unexplained-"N/A" finding. Presence only, not absence, so the later plan can restore a lens mention without touching the group. Update the *Known omission* paragraph.

**SC-PR6 -- Low -- The repointed I-2 sentence repeats the kind of overclaim the plan removes.**
* *Evidence.* `:411-420` says the profile sections "drive ... which changes must name an independent scientific check". The check is gated by the change, not by the profile; the plan's own complexity text says so ("gated on the change, not on this axis"). Nothing downstream of the profile reads those sections to decide which changes need a check.
* *Fix.* Say what is true, for example: "those drive the legacy-agent decision, and tell an author which changes touch a scientific assumption (see the independent scientific check). If uncertain,". The wording is the plan's to choose; it is fixed before implementation, so it is a revision now.

**SC-PR7 -- Low -- The sequencing section is out of date, and the test's later cost is not named.**
* *Evidence.* `:276` says plan C is not open. It is (`dev/plans/neutrality-and-upgrade-slots.md`, opened after this plan). I read its file list: it edits none of this plan's template or `dimensions/` files, so the conclusion stands. The Sequencing section does not name the combined review-stance-and-lenses plan. The accepted stance proposal (`dev/proposals/2026-10-18-claude-external-is-a-maintainer-stance.md:776-779`) and the lenses proposal edit the same two `dimensions/` cells and both template pairs. The stance proposal warns (`:1068`) that its re-anchor re-globs the test folder, so a new test is frozen from then on and "each later edit owes another re-anchor". The new test file falls under the same frozen glob as the sibling test (`bootstrap/tests/_gate_manifest.py:339-362`), which the glob finds and the committed manifest does not yet list, so it is a note-only addition until the re-anchor.
* *Fix.* Replace `:276-277` with the current fact, name the combined plan in the table, and say that this plan's test pins the block's reviewer-duty wording and the plan paragraph, so the combined plan runs it and, if the re-anchor has happened by then, owes a second one. Clause-level anchors (SC-PR3) keep that cost small.

**SC-PR8 -- Low -- Four accepted "Signals the change is wrong" have no home after archive.**
* *Evidence.* Revision 1 lists: checks written after the code; a data status that reads "in hand" and is not; the gate misfiring; the block growing discipline sub-lists. *Dispositions* (`:794-828`) homes F1 to F6 on the board row. F3 covers part of "gate misfires". The others appear only in Boundary C's attack list, which ends with this plan.
* *Fix.* One sentence on the same board row listing the four, so the revisit reads them. `dev/plans/neutrality-and-upgrade-slots.md` records where its own signals live.

**SC-PR9 -- Low -- Mechanical slips in the acceptance criteria.**
* *C3 insertion point.* `:374-377` and `:597-601` anchor on the paragraph ending "(which gate command fires the check)." That string appears in neither template; it wraps ("fires the" / "check)."). Applying the plan literally fails to find it. Anchor on the `_PLAN_CLAUSE_SENTENCE` in `test_scaffold.py` (already whitespace-tolerant) or on "the paragraph that begins `A security-touching plan re-answers`".
* *Neutrality count.* `:571-572` compares a failure count to the parent's. A count can match while the set changes. Compare the `file:line` lists; the gate output is identical between my edited and unedited copies (74 failures, no line in an edited file).
* *Extracted block versus fenced text.* `:543-545` says the extracted block is `diff`-identical to the fenced text. The test's region runs to the next `## ` line and so ends with a blank line the fenced text lacks. Say "after trimming trailing blank lines".

### What I measured, and how

All in detached copies of `5ee3c9ef` created under my scratch folder (the shared tree was not used); the copies are removed.
* **Frozen files.** The committed manifest has 183 `frozen_files` keys, as the plan says. None of the 12 paths I tested (the plan's 11 plus the plan file itself) is a key. Control: `bootstrap/tests/test_scaffold.py` is a key. The live glob (`_frozen_files`) finds 184: `test_review_and_verification_rules_ship.py` is in the glob and not the manifest, the same state the new test would have.
* **Engine symbols.** `test_ast_attest.py` fails at this commit with CHANGED `main` (`cli.py`) and `seed_gitignore` (`install.py`), as the plan says. The plan edits nothing under `bootstrap/_scaffold/`.
* **Wording applied.** The quoted C2, C3 and C4 text went into a copy, in the places the plan names. The nine test files (eight pinned plus the control) pass 372 on the edited copy and 372 on the unedited one. `check_cairn.py` reports OK on 180 files; `claim_check.py` exits 0 on all seven edited documents; `scaffold.py --manifest` is byte-identical; `verify_integrity --target .` lists the same 18 violations, the two templates among them, before and after; the neutrality leg is 74 failures on both with identical lines.
* **Adopter delivery.** A `solo-greenfield` install from the edited copy holds the block and the paragraph verbatim. An install from the parent, with the `documentation-tier-home` slot filled and committed, then `upgrade --plan --stage` against the edited copy: the proposal template is "locally-modified (merged clean)", the staged file has the block once, the slot fill once, and no conflict marker.
* **Test design.** The mutants in SC-PR3.
* **The `scientific-trust` search.** `git grep` finds exactly three hits in `dimensions/` and `bootstrap/BOOTSTRAP.md` at this commit, and none after C4. A wider search for the lens promise found no fourth site; the module template that still names a "Scientific Trust" lens is the one the plan says stays.
* **C1 inputs.** The five LHM commits the plan cites exist and carry the messages the plan describes (I did not re-read the findings inside them). The second-plan rule resolves to `assemble-part-a` by archive date.

### What I did not cover

* The Boundary B full run: it is the implementer's, after C4. I ran only the nine files, the gates, and the probes above.
* The blind draft itself. I could not run the C1 exercise, so I cannot say how either plan would score.
* The combined review-stance-and-lenses plan: it was not written when I read the tree, so SC-PR7 rests on the accepted proposals. The newer `stewardship-and-reuse` proposal (open, not accepted) says it edits *Scope*, *Dispositions* and the deviation sentence of the plan templates, not *Acceptance criteria*; I did not read it further.
* The scientific content of the block, apart from the positive-control bullet, which reads correctly to me (a null result is evidence only with a known-positive run of the same analysis). Whether the five bases are the right five is the Maintainer's, as the Decision records.
* What the Maintainer was actually asked about the positive control (SC-PR4); that is not on file.
* `doctrine/` and the rate-limit gate: the plan edits no doctrine, and I did not test the plan's argument that the `dimensions/` edit falls outside the gate.

## Response to plan review -- Claude Sonnet 5.5 (author) -- 2026-10-18

Responds to the Internal plan review at `d7fe5d6a`. **All nine findings are
accepted; none is rejected.** Two are met by a different shape than the review
proposed, and the table says so. As the lifecycle asks, the corrections are folded
into the operative cells (*Scope*, *Sequence*, *Acceptance criteria*,
*Verification*, *Dispositions*), and this section only points at them. The review
section above is untouched. Nothing was dropped to make a finding go away: every
Revision 1 outcome still has a chunk, and the *Scope delta* table is re-mapped to
the new chunk labels. Status moves to `ready-to-implement`; there is no second
plan-review round.

| Finding | Disposition | Where it landed |
|---|---|---|
| **SC-PR1** The blind draft could read the error | **accept** | *Acceptance criteria* > C1: "The inputs are fixed first, as the proposals were first opened" (stor-modflow now `b9d4c59a`, not `9dc9acfb`; the second plan's proposal as opened at `dde80719`, with the part it implements); "The second plan is chosen by a rule" (newest by archive commit date, which picks `assemble-part-a`; the "consider first" hint is gone); "The draft is blind, and has nothing else to read" (two pasted texts, no repository access). *Sequence* C1 row, *In brief* > Order of work, and the `External-repo paths:` line (two paths added). Facts re-checked in the LHM repository: the opened file is 427 lines with no review and no mention of priming; the Decision-time file is 1,907 lines with two External reviews in it. |
| **SC-PR2** The verdict is the implementer's to give | **accept, in a third shape** | C1: "The errors are stated in advance" and "A third agent scores" (not the drafter, not the implementer; each "yes" quotes a draft sentence; "not confirmed in hand" counts only if it names what would be opened). Question (c) is recorded and not scored. For (b), the review offered two options: drop it from the verdict, or call it an added condition. I took neither. "A check that fails under the error" is read as a check that can be run, so the data-status test is part of the one accepted question, and C1 requires the record to report each plan's verdict on (A) alone beside the combined one ("The reading of the accepted test is stated, and its effect is reported"). I did not drop it because without it stor-modflow passes for any draft that repeats the original check, which is the ritual the exercise exists to detect. This reading is also listed under *Scope delta* as an addition so the code reviewer or the Maintainer can overrule it. |
| **SC-PR3** The duties group lets clauses survive | **accept** (the review's simpler alternative) | *Sequence* > "The new test": the test now holds the block and the paragraph as whole literals and compares each copy by **equality**, not clause anchors. That pins every word, including all the survivors the review measured ("Neither the proposed code ...", "a closed budget ...", "written down before the result is seen", "it is not a reason to invent one", "tolerance with its source", "qualifies only if", "it becomes"). It also matches the accepted text, which says the test "holds the block and the plan sentence word-for-word". The thirty-one anchors are gone. C2 > "The new test is one node, and it can fail" now has a mutation ledger over the **set** (each sentence or list item, in both copies), plus the two weakened-word cases. A prototype of the test and an equivalent 50-mutant set was run at planning time: all killed. The review's slip on m9 is corrected (killed by the missing-marker message). |
| **SC-PR4** The positive control is not fully specified | **accept** | *Scope* > "Added at the Maintainer's instruction": the question the answer belongs to (quoted verbatim, with the coordinating session named as the relayer), what "planted errors" was and that it is declined, that the chat is not on file, and a settled design under "How the plan settles what the quoted words leave open": **trigger** keyed to the check's pass condition ("passes by finding nothing"), not the result; **relation to the deliberate break** (the failing run serves as the control when its mistake produces an effect of the size that matters, so one record; a second run only otherwise; a refactor is the same case); **owner and place** (the implementer records it with the failing run, in the *Implementation verification* record; the code reviewer verifies it). The bullet and the *Reviewers* sentence are rewritten in *Sequence* > "Wording each chunk lands"; *In brief* item 4; C2 criterion "The 'passes by finding nothing' bullet is whole"; *Verification* > Boundary C. |
| **SC-PR5** The promise sentences stay unpinned | **accept** | *Sequence* > "The new test", group (d), added in C3: presence of `independent scientific check` at all three sites and of the "N/A" finding in `dimensions/complexity.md`; presence only. C3 criterion "The test's fourth group is live, and stays one node". *Verification* > Known omissions rewritten. The sequencing row for `review-stance-and-lenses` now says the requirement has a trigger. |
| **SC-PR6** The I-2 sentence overclaims | **accept** | *Sequence* > C3 wording (the sentence now says the sections "show which changes touch a scientific assumption and so need the proposal template's independent scientific check"); C3 criterion "The I-2 sentence says what is true"; *Found while planning*. |
| **SC-PR7** Sequencing out of date; the test's later cost not named | **accept** | *Scope* > "Sequencing with the other accepted work": plan C named as open, `review-stance-and-lenses` named and tabled, the cost of a word-for-word pin named; *Frozen files* paragraph (the file freezes at the re-anchor); *Verification* > Known omissions. |
| **SC-PR8** Four signals have no home | **accept** | *Dispositions* > the third bullet: the proposal's four "Signals the change is wrong" are listed on the same board row as F1 to F6. |
| **SC-PR9** Mechanical slips | **accept**, all three | (1) The insertion point is now "the paragraph that begins `A security-touching plan re-answers`" in *Sequence* and in C2's criteria. (2) The neutrality check compares `file:line` lists, not counts (C2, C3, *Verification* > Expected non-pass). (3) The bytes criterion says "after trimming trailing blank lines". |

**The review's three trims.**

* **(a) Fold C3 into C2: accepted.** C2 now ships both template pairs and the test;
  the install and upgrade probes run once. Former C4 and C5 are now **C3** and
  **C4**. The review's references to "C3" in SC-PR9 therefore point at C2.
* **(b) Replace the anchors: accepted**, by holding the whole text (above).
* **(c) Pin the promise sentences in the same node: accepted** (SC-PR5).
* **C1 is neither dropped nor shrunk**, as the review recommends. It is made able to
  fail.

**Found by the author while folding, not raised by the review.**

* **`board-as-basis` shares all four template files.** It adds an `**In brief**:`
  prompt beside each header. The sequencing table said "None" for it; it now
  names the files and says the regions differ.
* **`check_cairn.py` is not clean at the parent**, for an issue in another plan.
  The criteria in C2, C3 and C4 now ask for no issue in a file this plan edits,
  with others recorded and shown unchanged.
* **Creating the test makes the `Proposed paths:` line stale**, which the checker
  flags. C2 now drops it.
* **The measured claims were redone on the revised wording**, in a clean copy of
  the plan-review commit: the existing tests pass 372 with and without the edit,
  the prototype test makes 373, `claim_check` exits 0 on all seven edited
  documents, and the neutrality leg is unchanged at 74.

## Retroactive application -- Claude Sonnet 5.5 (implementer) -- 2026-10-18

**In plain terms.** C1 tries the new wording on two past LHM plans, with a blind
drafter and a separate scorer, before anything ships. This first part of the
record fixes what the drafter will be shown and what the scorer will judge
against. It is committed **before any draft exists**, so no input can be
chosen after seeing one. Nothing has been drafted or scored yet. The drafts
(verbatim), the scores, the verdicts and the stop-rule outcome are appended
under this same heading in later commits: one section, written in more than one
commit, because the inputs have to be on the record first.

### Where C1 starts

C1 starts at commit `396c13d6` (Status to `implementing`, 2026-10-18). The
wording is read at that commit.

### The inputs, fixed

**1. The wording.** The fenced text under "C2 — the block" in *Wording each
chunk lands*: lines 395 to 439 of this plan at `396c13d6`, 45 lines, starting
`### Independent scientific check`. Its content is identical at `cca86a86`, and
at `89f82f3f` (where the plan review was folded in; the line numbers there
differ). SHA-256 of the 45 lines, as a plain file:
`327d0b175cafb40e43dc421a0894403edfa4e44854e4e1f1871200fa55c6f947`.
The other fenced texts in that section (the plan-template paragraph, the three
promise sentences, the test description) are **not** given to the drafter: they
concern what an author does at plan time or in the repository, not what a
proposal author fills in, and withholding them can only give the drafter less.
The block cites "security preflight S2", which is not in the drafter's two
texts; that is how the wording was reviewed and it is left as is.

**2. The stor-modflow source proposal, as first opened.** LHM commit
`b9d4c59a` (2026-08-27 09:15, "proposal-open", the commit that created the
file; the first review of it is `99317e5a` at 09:36). Taken with `git show
b9d4c59a:dev/proposals/2026-08-27-claude-stor-modflow-flopy-layer.md` in the LHM
repository, read only. 427 lines (the plan expected 427); SHA-256
`6971f5191097e17df6940dfde5a424921aa7f062b247770d111afb8e4e4cc46b`. Checked on
the text:
* **No review of it.** Its headings are Context, Proposed paths, Proposal
  (sections 1 to 10), Rationale, Alternatives, Evidence, Signals; its header says
  "Plan review: not required". Its Context paragraph recounts reviews of the
  *earlier* STOR implementation (lines 22 to 31) and lists five defects of the
  hand-rolled MODFLOW handling; none is about priming.
* **No mention of priming.** Searched case-insensitively for `prim`, `spin`,
  `cold`, `warm`, `burn`, `equilib` and `initial state/condition`. The only hits
  are "primitive" (line 89), "burned" (line 345, figurative) and, for `steady`,
  the stress-period flag (line 59). Section 5 (lines 152 to 168) says to carry
  a rolling `maxDelay`-deep stack "which is what `unsaturated_zone_module.m`
  does" and says nothing about filling it first. The instrument was checked:
  the same search for `unsaturated` finds 8 lines.
* **One mention of RAMP, in a different role.** Line 148 (section 4, on the date
  axis) says pairing by containment "removes the need to guess at the RAMP
  virtual period". It is not about the unsaturated store, so it does not state
  the shift that was later found missing, but the drafter will see the word.
* **The unverified data claim is present.** Lines 172 to 173: the OUTS file
  "carries the model's own `unsatStorage`".

**3. The assemble-full-port source proposal, as first opened.** LHM commit
`dde80719` (2026-10-01 11:11, "proposal: assemble-full-port -- opened
(awaiting-review)", the commit that created the file; its reviews are
`b427e221` and `5c7597f3`, later). Taken with `git show
dde80719:dev/proposals/2026-10-01-claude-assemble-full-port.md`, read only. 360
lines (the plan expected 360); SHA-256
`3f36d81bea2f946b3e93399f3f3845bc53e5550a1b9049568a3464e9d39c795f`. Status
`awaiting-review`; no review section in it. The part this plan implements, as
the drafter's brief will name it, in this one sentence: *The plan you are
drafting for implements Part A of this proposal ("The stage's foundation", A1 to
A3). It is plan 1 of 6 for the whole proposal.*

**What each brief holds, and nothing else.** Stor-modflow drafter: input 1 and
input 2. Assemble drafter: input 1, input 3 and the sentence above. No path into
the LHM repository, no error statement, no review.

### The second plan, by the rule

The rule (C1): among archived LHM plans, newest first **by archive commit date**,
the first in which a code review or a later record found an error in a
**computed result**.

* **Applied.** For each of the 46 files in LHM's `dev/plans/archive/` (at `master`
  `d3b5bd0f`), the commit where it first appears at its archive path
  (`git log --diff-filter=AR -M`), sorted by committer date. The newest is
  `assemble-part-a`, archived at `72ccf3db` (2026-10-15 12:12). The next is
  `cedar-creek-test-dataset` (`5e038956`, 2026-10-14 15:17). A search of all
  branches (`git log --all`) finds no archive commit later than `72ccf3db`.
* **It qualifies.** Its first code review (`4782e001`, 2026-10-14) raised **CR1**,
  blocking: in the default (production) LAND build, when no model cell counts as
  truly partly covered by land use, the fill for uncovered cells is
  `sum(weights[partial]) / numPartial`, which is 0/0, so the land-use weights
  written for those cells are NaN, stored as the file's missing-data code, with
  only a `RuntimeWarning`. That is an error in a computed result (an array the
  model reads), not in structure, tests or documents. The reviewer's probe P2
  showed it on Cedar Creek with the partial threshold patched so no cell counted
  as partial: the build completed and the weights held 200 missing entries (20
  cells by 10 types). The fix is `5b6676af`; the second code review (`87fd7e2e`,
  2026-10-15) closed it, with 8 mutations caught.
* **Result: the rule picks `assemble-part-a`, as the plan expected.** The rule
  stops at the first plan that qualifies, so no older plan was read.

### The errors, stated before any draft

These are the statements the scorer will be given beside each draft. Each was
checked against the LHM commits it cites.

**Stor-modflow** (`dev/plans/archive/stor-modflow-correctness.md`): *The
unsaturated-zone store was computed from a percolation stack that was never
primed, so the model's own 365-day warm-up pass (`unsaturated_zone_module.m`
lines 296 to 352) had no counterpart, which offset the domain-mean unsaturated
anomaly by about 14.9 kg m-2 for the rest of the series (the full-series mean
was +13.5 before the fix and -1.2 after), and the model's RAMP virtual-period
shift was left out (about -0.15 kg m-2); the External code review found both at
LHM `983d6c58` (findings P20 and P21), and they were fixed in code at `0b2ca707`
and recorded with the decomposition at `6dcc0cc5`. Separately, the reference
array the first check relied on, `unsatStorage` in the run's OUTS file, had never
been saved (the run log says "Variable 'unsatStorage' was not saved", the array
being 2.80 GB, over the 2 GB limit of the file format used); the Internal plan
review found this at `dae97b43` (P1) and the check was withdrawn at `7a9771f5`.*

**Assemble part A** (`dev/plans/archive/2026-10-01-claude-assemble-part-a.md`):
*In the default LAND build, when no model cell counts as truly partly covered by
land use, the fill for uncovered cells is 0/0, so the build wrote NaN
(missing-data) land-use weights for every uncovered cell, with only a warning
(200 missing entries on Cedar Creek when its partial threshold was patched so none
counted as partial; Cedar as run has 13 truly partial cells and was unaffected).
The first code review found it as CR1 (blocking) at LHM `4782e001`; it was
fixed at `5b6676af` and closed at the second review, `87fd7e2e`.*

### Noted before drafting, not scored

* **One citation corrected against the plan's wording.** The plan says the
  priming and RAMP defects were "fixed at `6dcc0cc5`". That commit is the
  author's response that records the fix; the code change is `0b2ca707`
  (`6dcc0cc5` says "[P20]-[P24] fixed in 0b2ca707"). The statement cites both.
  The figures in the plan (14.9, +13.5 to -1.2, -0.15) match `6dcc0cc5`: priming
  alone +14.91, RAMP shift alone -0.15, full-series mean +13.5 before and -1.2
  after.
* **How CR1 came to be reachable.** The rule that emptied the "partial" set
  (a 1e-4 shortfall threshold, ledger row L25) was added to the plan on
  2026-10-14, at `15978a3f`, after the proposal was opened on 2026-10-01. The
  proposal as opened says nothing about partial cells or a fill value. So a draft
  made from it cannot name the 0/0 itself; a "yes" on question (A) for this plan
  would need a check that fails whenever the land-use weights contain a missing
  value, on a region without partial cells. This is recorded so the verdict is
  read with it. It is not a reason to pick another plan: the plan was picked by
  the rule, and the rule is not to be tuned to how well the block fits.
* **The stor-modflow plan implements the first of two plans** from its proposal
  (sections 1 to 7 and items from an earlier proposal; the helper-extraction plan
  takes sections 8 to 10), by the Decision's sequencing, which postdates the
  opened text. The opened text has all ten sections and names no split, and
  neither input here names one, so the drafter drafts for the proposal as written.

### The blind drafts, verbatim

Both drafts are in. **Nothing has been scored.** A separate fresh agent scores
them next, and its output, the verdicts on (A) and (B) alone and combined, and
the stop-rule outcome are appended below in a later commit.

**How each drafter was briefed** (the coordinating session's account; I did not
see the briefs):
* Each drafter was a fresh-context Sonnet agent, neither the implementer nor the
  scorer.
* Each was told it could read exactly two files with the Read tool: the wording
  (input 1) and its proposal as opened (input 2 or 3), both in one folder. It was
  told to read, search and list nothing else, run no commands and use no web.
* The assemble drafter's brief also carried the part-naming sentence from input
  3, verbatim.
* Each drafter made **3 tool calls in total**: the two reads and the hand-back.
  The coordinating session extracted each draft byte for byte from the drafter's
  hand-back (the input of that tool call) into a file, and checked its copy of the
  first against the raw transcript.
* **Limitation.** Blindness rests on the instruction and on that observed tool
  count. It was not enforced by a sandbox, and a negative cannot be proved beyond
  the count.
* **Order.** The error statements above were committed in this record at
  `0ac2b567` (2026-10-18 17:51:45). The draft files were extracted at 17:54, after
  that commit. By the briefing above, neither drafter was given an error
  statement or any review.

Each draft is the text between its fences, byte for byte; no draft contains a
fence of its own. A draft's headings are inside the fence and are not headings
of this plan.

#### Draft 1: stor-modflow (38 lines)

Drafter: fresh Sonnet agent. File: `draft-stor-modflow.raw.md`. Input: the
wording and the stor-modflow proposal as opened (`b9d4c59a`). SHA-256 of the
file: `06ff7a020870d225066ac427ef12af2abc40d6264366a0ee159bbfe946e97837`.

```text
### Independent scientific check

**The check: the recomputed unsaturated-zone store against the model's own saved `unsatStorage`** (§6, `OUTS_newBC_v5-2000-2025_20260219.mat`).

* **What it compares.** The monthly `unsaturated_zone_water` this script builds from PERC, `vk` and the stress-period lengths, against the `unsatStorage` the MATLAB model saved for the same run. The comparison covers all 312 months, cell by cell on the 798×647 surface grid and as a domain total.
  * **Expected value.** Agreement, with a residual of zero up to numerical precision. No residual has ever been computed, for the current code or the new code.
  * **Tolerance.** The proposal gives none, and I cannot source one from what I have in hand. What I would write into the plan before the first run is the worst-case rounding from PERC's integer quantization, summed over the `maxDelay`-deep stack (26 deep, per the proposal's description of `unsaturated_zone_module.m`), plus the float precision of the stored arrays. The source is the quantization step in PERC's `/lookup` and the dtype in OUTS. I have read neither.
  * **The Signals criterion is not a tolerance.** "Does not shrink materially against the current implementation" is a relative test. A residual can shrink and still be wrong, so that test stays a secondary signal and the absolute bound above is the check.
  * **Data in hand.** The file is named and sized (137 MB), and the accepted proposal says it holds `unsatStorage`. This proposal's recon table has no OUTS row, so nobody has recorded opening it.
  * **Not checked:**
    * that the variable exists;
    * its units (depth or mass), its grid, and its time coverage;
    * whether it is an end-of-month value or a monthly mean, which decides whether a correct recomputation agrees;
    * that it comes from the same run as PERC.
  * **To confirm.** Open OUTS and `unsaturated_zone_module.m`, and record these facts before the check is relied on.

* **Why the expectation is independent.** The expected value is produced by the MATLAB model, not by this script and not by a test written from my reading of that module. Its basis is the saved output of the model the code reads. That makes it independent of the port, not of the model's physics. A pass shows the product reports what the model computed. It does not show the model's unsaturated zone is right about the aquifer. PERC is read from the file here, where MATLAB used its own in-memory copy, so a reading error (dequantization, a shifted time axis) can show up instead of cancelling.

* **The error it would catch.** The hardcoded 1-day stress-period length where `perlen` is `[1, 5, 7]`. It would also catch a scalar-mean `vk` in place of layer-1 `vk` regridded, `vka` read as a conductivity when it is a ratio, and a one-day offset in the PERC time axis.
  * **At implementation:** restore the hardcoded `1.0` on purpose, run the check, and record the failing output.
  * **How large the error may be.** The recon numbers (1358 periods, 9498 step totims, `perlen` in {1, 5, 7}) imply, if steps are daily, that nearly all periods are 7 days. I have not seen the per-period counts. If so, the mutant should be far off.
  * **If the mutant stays inside the tolerance,** the check cannot see this error, and the record must say so.

* **When the check passes by finding nothing.** A near-zero residual is a "no difference" result.
  * **Positive control.** The mutant run above is the control. The current implementation's residual against OUTS (never computed) is the second. If the current code is already inside the tolerance, this check cannot discriminate the §5 fixes.
  * **Guard against a vacuous pass.** The comparison must assert that it compared a nonzero count of finite cells in every month, and that the compared fields are not constant.
  * **An absent OUTS is not a pass.** §6 makes OUTS an optional source. The smoke-check acceptance requires the residual to be reported, so a run where OUTS is absent or skipped fails acceptance.

**What this does not cover.** It covers the unsaturated store only. The unsaturated store lives on the surface grid and is built from PERC, with no heads, so these items do not pass through it:
* the overhang fix (§3);
* month-to-head pairing (§4);
* units and `ibound` from the DIS and BAS6 (§2);
* the groundwater ΔS.

That leaves four of the five defects in Context without an independent expected value, and I am not inventing one.
* **Overhang.** The arithmetic agrees with the FloPy-measured offset. 1637×1313 at 500 m is 818.5 × 656.5 km against 798 × 647 km, which gives 20.5 km north and 9.5 km east. Both numbers come from one grid description, so this is a consistency check, not an independent one.
* **Mass conservation.** The proposal's "mass conserved where grids align" invariant is a closed budget and would not catch a wrong input.
* **A basis I would open.** I would check whether the run's MODFLOW listing file prints the volumetric budget with STORAGE terms. The cell-budget files lack one, but the listing file is a separate output. I have not seen whether it exists for this run. If it does, domain-total ΔS per stress period against the listing would be an independent check on the groundwater half. The Maintainer should weigh that this proposal currently has no such check for that half.
```

#### Draft 2: assemble part A (18 lines)

Drafter: fresh Sonnet agent. File: `draft-assemble-part-a.raw.md`. Input: the
wording, the assemble-full-port proposal as opened (`dde80719`) and the
part-naming sentence. SHA-256 of the file:
`212fc76e4a9fbd814cae8ff9addaab9d0492840235bc0c4db14111de4bc76207`.

```text
### Independent scientific check

This part is gated in. A2 makes the corrected area-weighted `helper/zonal.cell_statistics` the single implementation that every LAND loader uses, and its output becomes model input. A3 also says that when a fix breaks a parity check, the MATLAB import is fixed too and its baselines are rebuilt. After that, MATLAB parity for this function shows that two implementations agree. It does not show that either places data correctly. This check is the one that can.

* **What it compares.** It compares the area-weighted mean per coarse cell from `cell_statistics` (production path, `matlabParity=False`) against the exact mean of a known field.
  * **Fixture.** The fine grid is synthetic and generated in the test: 11 × 11 fine cells. The coarse grid is 4 × 4 cells, each exactly 3 × 3 fine cells, aligned to the fine cell edges. The last coarse row and column therefore cover only 2 of 3 fine cells and test the "edge cells kept" claim.
  * **Field.** Each fine cell holds a linear field, `f = 100 + 2·(x) − 3·(y)`, sampled at the fine cell centre. Positions are in fine-cell widths from the grid origin, and y is northing. The slopes differ in sign and size so a swapped, transposed or reversed axis cannot cancel out. The values are illustrative and are fixed in the plan.
  * **Expected value.** For an interior coarse cell, it is `f` at the centre of the coarse cell. For an edge cell, it is `f` at the centre of the overlapped rectangle, with weights normalised by the overlapped area. The helper's contract for edge cells (mean over the overlap, not over the full coarse cell) is my reading of "edge cells kept", and the test pins it.
  * **Reuse across grids.** The same call runs three layers with different slopes, to exercise the geometry that is "computed once and reused across grids".
  * **Tolerance.** The identity is exact in real arithmetic, so the tolerance is round-off only. It is 1e-9 absolute on values near 100 if the helper works in float64, where the actual round-off over at most 9 terms is around 1e-13. If the helper works in float32, it is about 1e-4. Both are far below the 1.5 value-unit effect of the mistake below. The tolerance's source is the working dtype of the helper, which I have not opened and the plan must read off the code.
  * **Data.** It needs no external data. The expected values are worked out by hand from the grid numbers and committed in the test before the helper is run against it. At opening they do not exist, so nothing has been checked.
* **Why the expectation is independent.** Its basis is an analytical solution. The mean of a linear function over a rectangle equals its value at the rectangle's centroid. That follows from the field and the grid numbers alone, and neither the helper nor MATLAB computes it. Because the field is not constant, the check cannot pass by default: a constant field is unchanged by a shift.
  * **What is still shared.** The test and the helper share one assumption: row 0 is the northern edge, as the raster header convention has it. The fixture states that convention in its own comments, not through `raster.get_raster_header`, so the reviewer can challenge it.
  * **Not covered.** The check does not cover non-integer or misaligned grid ratios. A mistake that appears only there is left to the helper's existing tests and to A3's Cedar comparisons. Those comparisons run against MATLAB baselines that are rebuilt under the same corrected understanding, so they are independent of the port but not of that understanding.
  * **Unopened.** I have not opened `helper/zonal.py` or its tests under `tests/helper/`. I also have not checked whether Cedar's real fine-to-coarse ratio is an integer, or what the `sum` and `majority` options return on this fixture. The plan opens those first. If the ratio is not an integer, the fixture would not resemble the data the loaders actually aggregate.
  * **Time axis.** The merge of the datenum conversions is also outside this check. It rests on MATLAB bytes only, and one cheap additional anchor would be the known `datenum(1970,1,1) = 719529`.
* **The error it would catch.** Rows placed half a fine cell high, which is the MATLAB placement the corrected algorithm removes. The consolidation could bring it back, for example by routing the default path through the parity branch, or by reusing geometry built for one extent on another grid. With a y slope of 3 per fine cell, the shift moves every coarse mean by about 1.5 value units, nine orders of magnitude above the tolerance. It also changes the edge cells, because the overlapped rectangle moves. At implementation the implementer makes this mistake on purpose, in a separate copy of the code. They record the failing output, which should name the cells and show differences near 1.5, beside an unmutated control run.
* **When the check passes by finding nothing.** It does not. It passes by matching distinct, nonzero expected values in every cell, and it fails whenever any cell moves. The deliberate half-cell-high run serves as the positive control, since its effect (about 1.5) is far larger than the effect that matters (anything above round-off). The implementer records it with the failing run.
```

### The scores, verbatim

**The scorer.** A fresh Sonnet agent, neither the implementer nor either
drafter (the coordinating session's account). It could read only the two drafts
and the two error statements, and made 5 tool calls: four reads and the
hand-back. As for the drafters, blindness rests on the instruction and on that
observed count, not on a sandbox. Its rubric was this plan's questions (A) and
(B) as written in C1, including that a draft repeating the data claim as "in
hand" fails (B), and that every "yes" quotes a sentence of the draft. The basis
kind and its independence were recorded and not scored. The coordinating session
extracted the output byte for byte from the scorer's hand-back (11 lines,
SHA-256 `6d0ff759a17cb644d5fa5552c2ecb30e68e28b56e056da2cf62cf86f9f286fb5`).
The text between the fences is that output; it contains no fence of its own.

```text
#### Draft 1 (stor-modflow)
- **(A):** yes. The check compares the recomputed monthly unsaturated store against the model's own saved array and expects a near-zero residual. The error is an unprimed percolation stack (no 365-day warm-up), which offsets the domain-mean anomaly by about 14.9 kg m-2 for the whole series, plus a smaller RAMP shift of about -0.15. Either would leave a residual far above the rounding-level tolerance the draft proposes. The check never names the warm-up as a target, but it would fail under it. Quoted: "Agreement, with a residual of zero up to numerical precision." and "The monthly `unsaturated_zone_water` this script builds from PERC, `vk` and the stress-period lengths, against the `unsatStorage` the MATLAB model saved for the same run."
- **(B):** yes, narrowly. The error statement says `unsatStorage` was never saved (2.80 GB, over the 2 GB file-format limit), so the draft's premise that the model saved it is false. The draft does not claim it verified that. Under a heading labelled "Data in hand", it says nobody has recorded opening the file, lists "that the variable exists" as not checked, and names the file to open (OUTS). That meets the "not confirmed, and names what would be opened" branch. The "What it compares" line does assert the array as saved, but the draft's own "Not checked" list overrides it. Quoted: "This proposal's recon table has no OUTS row, so nobody has recorded opening it." and "**To confirm.** Open OUTS and `unsaturated_zone_module.m`, and record these facts before the check is relied on."
- **Verdict:** yes.
- **Basis (not scored):** the saved output of the model the code reads. It is independent of the port code under review. The draft itself notes it is not independent of the model's physics.

#### Draft 2 (assemble-part-a)
- **(A):** no. The check runs `cell_statistics` on a synthetic 11 × 11 linear field aggregated onto a 4 × 4 coarse grid. Every coarse cell, including the edge cells, overlaps the fine grid with nonzero area. The error is a land-use weight build whose fill is 0/0 for cells with no partial land-use coverage, giving NaN weights for uncovered cells. The fixture has no land-use classes, no partial-coverage threshold and no uncovered cells, so that branch never runs and the check would pass with the error in place. No draft sentence reaches this failure, so none can be quoted.
- **(B):** yes. The fixture is synthetic and generated in the test, so the check could have been run. The draft says no external data is needed and names the files the plan would open for what it has not read. Nothing in the error statement contradicts its data claims. Quoted: "It needs no external data. The expected values are worked out by hand from the grid numbers and committed in the test before the helper is run against it." and "I have not opened `helper/zonal.py` or its tests under `tests/helper/`." and "The plan opens those first."
- **Verdict:** no.
- **Basis (not scored):** an analytical solution (the mean of a linear field over a rectangle equals its value at the centroid). It is independent of the code under review.
```

**The quotes check out.** I looked up each sentence the scorer quotes in the
draft it names (a plain string search against the two draft files): all are
there, word for word. Every "yes" carries a quoted sentence.

### The verdicts, and the stop rule

| Plan | (A) alone: a check that fails under the error | (B): could it have been run | Combined verdict |
|---|---|---|---|
| stor-modflow | yes | yes, narrowly | **yes** |
| assemble part A | no | yes | **no** |

* **(B) did not decide either plan.** Read on (A) alone the table is the same:
  stor-modflow yes, assemble part A no. For stor-modflow (B) was the closer call:
  the draft's bullet is headed "Data in hand", but its text says nobody has
  recorded opening the file and lists "that the variable exists" as not checked,
  and it names the file to open. The scorer read the text over the label and
  passed it by the "not confirmed, and names what would be opened" branch. A
  draft that had said the array was in hand would have failed (B), and the plan's
  reading of the accepted question exists for that case. The code reviewer can
  look at that call.
* **The stop rule, as written.** Stop only if **both** verdicts are no. One is
  yes, so **the plan proceeds.** The plan that passed is **stor-modflow**. The
  other, **assemble part A**, is a **no**, reported here to the Maintainer; the
  archive commit repeats it (the plan requires it in both places). It does not
  stop the plan, and the stop was neither softened to a warning nor hardened to
  "either".

**What the "no" showed, in plain words.** The assemble draft chose a good check
for the change the proposal describes (the corrected area-weighted average of
the grids, tested against the exact mean of a known field), built to fail under
a half-cell shift, and one that could be run with no outside data. But the error
the plan later hit lives in a different place, the fill for uncovered land-use
cells, and the proposal as opened says nothing about it (see "Noted before
drafting"). So the draft's check would have passed with that error in place. The
block did not fail here for lack of a good check; it was pointed at a different
risk.

**What the "yes" showed, and what it did not.** The stor-modflow "yes" rests on
a check against the model's own saved `unsatStorage` array, and per the error
statement that array had never been saved. The scorer's verdict is the verdict:
yes. The plain addition is this: **what the block would have caught is the
missing reference array, earlier, not the priming defect directly.** The block's
data-status prompt would have sent the author to open the OUTS file at the
outset; the array's absence would have shown up before three responses repeated
the claim, and the author would have had to find another basis. Whether a check
whose reference turns out not to exist counts as one that "fails under the
error" is the judgment the plan says is not mechanical. The Maintainer can weigh
it at archive.

**The null-result bullet is not claimed as tested.** Neither plan found a false
null. The "passes by finding nothing" bullet has no occurred instance behind it
and rests on argument. Neither plan is cited as support for it.

**Limits of the exercise.** One drafter and one scorer per plan, two plans, and
blindness by instruction. The result is a go/no-go gate, not a measurement of how
often the block helps.

### C1 verdict

**C1 says continue.** One plan passed and one did not, which under the accepted
stop rule does not stop the plan. Status stays `implementing`; no Waiting line is
written. C2 to C4 follow, one commit each.

## Implementation verification -- Claude Sonnet 5.5 (implementer) -- 2026-10-18

**In plain terms.** The work is done and verified once, in full. The new test
passes and was shown able to fail: 43 deliberate breaks of the two templates'
new text, then 48 once the three promise sentences were pinned, were each caught
(the one exception is a break that is meant to pass). The full suite has two
red tests, the same two that are red before this work, both about a separate
repair of five engine functions that this plan does not touch. Nothing in the
install contract, the lockfile findings, the vendor-neutrality list or the frozen
files moved. The part C1 flagged for the Maintainer is unchanged: one of the two
past plans said no.

**Boundary B mode**: full. Reasons are those the plan gives: the accepted text
says so, shipped templates are edited, the collection grows by one test, and
vendor-neutrality is a named high-risk surface.

**Tested commit**: `531084a1f638ad54f5e8d9e7a543411ad89c0f2a` (C3).

**Reviewed range**: base `33df0cb8722cc7b76bb12cf66f0358afe56ce189` (the last C1
commit, and the parent of C2) to tested `531084a1f638ad54f5e8d9e7a543411ad89c0f2a`.
It holds two commits: C2 `27feca344a581e66314fa9d8aedbb1ea77d0d77f` and C3
`531084a1f638ad54f5e8d9e7a543411ad89c0f2a`. The C1 record is `396c13d6` to
`33df0cb8` and changes only this plan.

**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python
3.13.13 (conda-forge), pytest 9.0.3.

**Pre-run state**: the full suite ran in a fresh detached `git worktree` at the
tested commit, `git status --short` empty (0 lines), `HEAD` the tested commit.
Other sessions' uncommitted files are not in a worktree. **Post-run state**:
`git status --short` empty (0 lines), `HEAD` unchanged. The mutation ledgers and
the other probes ran in separate worktrees at the same commit (or at C2's commit,
for C2's ledger), so nothing mutated the tested worktree.

| Command | Exit | Outcomes | Elapsed |
|---|---|---|---|
| `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0 -rsfExX` at the tested commit | 1 | **2 failed, 3510 passed**, 0 skipped, 0 xfail, 0 xpass, 3 warnings | 595.3 s (18:09:02 to 18:18:59) |
| the same command at the base `33df0cb8` | 1 | 2 failed, **3509 passed**, 0 skipped, 0 xfail, 0 xpass, 3 warnings | 603.5 s |
| `python scripts/quality_gate.py --sub neutrality --sub redundancy` | 0 | neutrality `fail=0 info=56`; redundancy `fail=0 info=0`. The neutrality output is identical to the base's, line for line | 1.2 s |
| `python scripts/check_cairn.py` | 0 | OK, 182 files, no issues | 1.9 s |
| `python bootstrap/scaffold.py --manifest` | 0 | byte-identical to the base's (98 lines) | under 1 s |
| `python bootstrap/verify_integrity.py --target .` | 1 | 18 violations, output identical to the base's (the two Cairn templates among them, as at planning time); `--finalize` not run | 0.1 s |
| `python scripts/claim_check.py <file>` on the four template copies, the three promise sites and this plan | 0 each | OK, no flags | under 1 s each |
| `python -m pytest -q bootstrap/tests/test_scientific_check_guidance_ships.py` | 0 | 1 passed | 0.4 s |

The `-rsfExX` flag only adds summary lines for failures, skips, xfail and xpass;
it changes no selection. The full runs were done one after the other, not at the
same time, so neither was slowed by the other.

**Node ID of the added test** (matches `pytest --collect-only -q`, which lists
this one test and no other from the file):
`bootstrap/tests/test_scientific_check_guidance_ships.py::test_the_check_guidance_reaches_every_copy_and_promise_site`

**Non-pass disposition.** Two failures, each disposed of rather than treated as
noise.
* `bootstrap/tests/test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package`
  and `bootstrap/tests/test_ast_attest.py::test_ast_gate_passes_over_the_full_scaffold_module_set`.
  Both are red at the base too: the full run at `33df0cb8` fails exactly these two
  and no other, and passes 3509 where the tested commit passes 3510, the one
  extra being the new test. The failure text is the same in both runs (compared
  after removing the worktree path and the memory addresses of the function
  objects).
* The CHANGED set derived by the runbook's Step 1 method at the base and at the
  tested commit is the same: **CHANGED 5, MISSING 0, DUPLICATE 0, NEW 86** at
  both, the same five symbols with the same hashes (baseline hash, then current
  hash):
  * `FunctionDef:_cmd_adopt_module` in `upgrade.py`: `92290a6b95389cc2` then `c637af9f6ad93565`
  * `FunctionDef:cmd_upgrade` in `upgrade.py`: `d98eff085ea46b43` then `d9c59a4db630c49e`
  * `FunctionDef:create_dev_tree` in `install.py`: `0e8c4e4f41b5bcb8` then `9de03f6ae0c0c469`
  * `FunctionDef:main` in `cli.py`: `5c197afe8ee049d4` then `bd3724f284d16af0`
  * `FunctionDef:seed_gitignore` in `install.py`: `55a95c62ab693619` then `12ca0b5cd49ed2d7`
* `git diff --stat 33df0cb8..531084a1 -- bootstrap/_scaffold bootstrap/tests/fixtures`
  is empty. The range changes nine paths and no others: the four template
  copies, `dimensions/complexity.md`, `dimensions/README.md`,
  `bootstrap/BOOTSTRAP.md`, the new test and this plan. The five symbols belong to
  a separate repair; re-anchoring the AST baseline is the Maintainer's and was
  not done here.
* No skip, xfail or xpass was reported by either run. The test that is sometimes
  flaky under load, `test_a_t4_output_is_bounded`, passed in both runs, so no
  solo rerun was owed.
* The 3 warnings are the same third-party deprecation notice in both runs.

**Plan-specific acceptance commands.** Run at the commit named, in a worktree
holding its bytes.

| Criterion | Command or method | Result |
|---|---|---|
| C2: heading once, in the right place, both proposal copies | line search for `### Independent scientific check` against the `**Prospective only.**` and `## Signals the change is wrong` lines | once each; after the first, before the second |
| C2: paragraph once, in the right place, both plan copies | line search against `A security-touching plan re-answers` and the doc-tooling slot | once each; after the first, before the slot |
| C2: the preflight slice is unchanged | `_extract_security_preflight` imported from `test_scaffold.py`, run at C2 and its parent | byte-identical in both proposal copies (41 lines) |
| C2: the bytes are the reviewed bytes, three ways | extracted block and paragraph against the fenced C2 texts; the test's literals, whitespace-collapsed, against the same; removing the inserted text gives the parent byte for byte | all equal (block 45 lines, paragraph 7) |
| C2: the null-result bullet is whole | text search in each proposal copy | the bullet, its three absences, the control rule, the recording place, the streamflow example and the reviewer clause each occur once |
| C2: existing pins pass unedited | the nine files (`test_scaffold`, `test_scope_reduction_trap`, `test_verification_boundaries`, `test_documentation_plan_module`, `test_claim_check_module`, `test_core_dev_folders`, `test_quickstart_sequence`, `test_profile_grammar`, `test_comprehension_floor`) | 372 passed at the base and 372 at C2 |
| C2 and C3: no vendor or project name | `grep -E 'Claude\|Codex\|Anthropic\|OpenAI\|Gemini\|Cursor\|LHM\|modflow_tools'` over every added line of C2 and C3; control: a line holding `Cursor` | 0 hits; control line 1 hit |
| C2: install contract unchanged | `scaffold.py --manifest` at base, C2 and tested | byte-identical |
| C2: an adopter receives both texts | real install from the tested commit into an empty scratch folder (`solo-greenfield`, `--non-interactive --allow-dev`) | installed proposal and plan templates are byte-identical to the shipped source; the block and paragraph are in them; `--summary` and `--dry-run` also ran (exit 0; the dry run wrote nothing) |
| C2: an existing adopter's upgrade keeps their work | install from the base, fill `documentation-tier-home` in both templates, commit, `upgrade --plan --cairn-root <tested tree>`, then `--stage` | both templates "locally-modified (merged clean)"; each staged file holds its new text once, the slot fill once, and no conflict marker |
| C2: lockfile left alone | `verify_integrity --target .` at base, C2 and tested | the same 18 violations each time |
| C2: plan-template pins stand | `## Implementation verification` H2 and `**Waiting on Maintainer**` lines in both plan templates | 0 and 0, as at the base (the phrase appears only in prose) |
| C2: header tidied | the `Proposed paths:` declaration dropped; `claim_check` on this plan | clean |
| C3: the old promise is gone, the new one is in | `git grep -n -i 'scientific-trust' -- dimensions bootstrap/BOOTSTRAP.md` | 3 lines at the base, none at tested; `independent scientific check` occurs once in each of the three files |
| C3: the finding and the gate sentence | whitespace-collapsed search of `dimensions/complexity.md` | each once, after the `### Complex` heading |
| C3: no axis, value or gate-table row changed | `git diff -U0` over the three files; separator count in the README row | exactly three hunks (the I-2 lines, the README Complexity row, the Complex-position bullet); the row has 4 `\|` before and after |
| C3: bytes as reviewed | added lines of each hunk against the fenced C3 text; removed lines against the old ones | the README row and the complexity bullet are added whole; the I-2 hunk adds 3 lines and keeps the first line of the fenced 4 unchanged; the removed lines are exactly the old ones named in the plan |
| C3: the line that is not a promise stays | `git diff --stat` for `templates/modules/team-gated/architecture_review_template.md` | empty; it still carries its "Scientific Trust" lens line |
| C3: gates | `test_profile_grammar.py`; `check_cairn.py`; `claim_check.py`; neutrality list | 45 passed (46 together with the new test); clean; clean; identical to the base |
| C4: no frozen file changed | the range's changed paths against the 183 `frozen_files` keys in `bootstrap/tests/fixtures/gate_manifest.json`; control: `bootstrap/tests/test_scaffold.py` is a key | the intersection is empty; the new test file is not a key |
| Not touched | `git diff --stat 33df0cb8..531084a1` over `doctrine/`, `AGENTS.md`, `templates/modules/`, `docs/`, `scripts/`, `tools/`, `dev/.cairn/`, `dev/PLANNING.md`, `CHANGELOG.md`; control: the same command over `dimensions/` | empty; the control shows 3 lines |

**Mutation ledgers.** Run by a throwaway harness that refuses to run outside a
scratch worktree, changes files only inside the region it targets (it fails if a
mutant leaves a file unchanged, and checks the files are restored byte for byte
after each one), and runs the new test file alone against each. The block's and
the paragraph's sentences and list items were listed from the fenced texts by
splitting them, and the harness checks that the pieces cover the whole text, so
none is left out. Each deletion is made inside the block's own region.
* **C2, at `27feca34`: 43 mutants, 43 killed, none survived, none equivalent**,
  with the unmutated control passing before and after.
* **C3, at `531084a1`: 48 mutants.** The same 43, all killed again, plus the five
  group-d mutants: `independent scientific check` replaced by `review` at each of
  the three sites in turn (3 killed), `review finding` replaced by `note` in
  `dimensions/complexity.md` (killed), and the old lens phrase restored beside the
  check in the README row (**passes, by design: presence only**). 47 killed, 1
  passed as expected, control passing before and after.
* Beyond the plan's list: m11 wraps the block in a slot in both proposal copies,
  m12 moves the paragraph into the doc-tooling slot in one plan copy, m13 adds a
  sentence to one proposal copy. All killed. The harness itself is not committed;
  each ledger row names its mutation.

C2's ledger, rows in order:

```text
PASSED  control (before)
KILLED  m1 block word changed, Cairn copy only
KILLED  m2 block word changed, shipped copy only
KILLED  m3 paragraph word changed, one plan copy
KILLED  m4 paragraph deleted, one plan copy
KILLED  m5.00 block unit deleted from both: '### Independent scientific check'
KILLED  m5.01 block unit deleted from both: '*Gated to a change that touches a scientific ass'
KILLED  m5.02 block unit deleted from both: 'For every other change, one line — "N/A: no scie'
KILLED  m5.03 block unit deleted from both: 'Name **one** check that could show the change is'
KILLED  m5.04 block unit deleted from both: '* **What it compares.** The quantity, the expect'
KILLED  m5.05 block unit deleted from both: 'Say whether the data behind the expected value i'
KILLED  m5.06 block unit deleted from both: 'If the check depends on data that does not exist'
KILLED  m5.07 block unit deleted from both: '* **Why the expectation is independent.** Neithe'
KILLED  m5.08 block unit deleted from both: 'Its basis is one of these:'
KILLED  m5.09 block unit deleted from both: '* an analytical or manufactured solution;'
KILLED  m5.10 block unit deleted from both: '* a conservation law chosen against the error th'
KILLED  m5.11 block unit deleted from both: '* a trusted observation or benchmark;'
KILLED  m5.12 block unit deleted from both: '* an independent implementation, or the saved ou'
KILLED  m5.13 block unit deleted from both: "* a domain expert's expectation, written down be"
KILLED  m5.14 block unit deleted from both: '* **The error it would catch.** The plausible mi'
KILLED  m5.15 block unit deleted from both: 'This is security preflight S2\'s "Can it fail?", '
KILLED  m5.16 block unit deleted from both: 'At implementation, the implementer makes that mi'
KILLED  m5.17 block unit deleted from both: '* **When the check passes by finding nothing.** '
KILLED  m5.18 block unit deleted from both: 'Show the same analysis detecting a known effect '
KILLED  m5.19 block unit deleted from both: 'The failing\n  run above serves as the control wh'
KILLED  m5.20 block unit deleted from both: 'At implementation, the implementer records the c'
KILLED  m5.21 block unit deleted from both: 'For example, an analysis that reports no streamf'
KILLED  m5.22 block unit deleted from both: '**Reviewers.** The proposal reviewer challenges '
KILLED  m5.23 block unit deleted from both: 'The code reviewer verifies the recorded\nfailing '
KILLED  m5.24 block unit deleted from both: 'The Maintainer judges at the Decision whether th'
KILLED  m5.25 block unit deleted from both: 'If no independent basis exists, say so;'
KILLED  m5.26 block unit deleted from both: 'the Maintainer weighs that, and it is not a reas'
KILLED  m6.00 paragraph unit deleted from both: '**An independent scientific check is accepted sc'
KILLED  m6.01 paragraph unit deleted from both: 'A replacement qualifies only if it\nfails under t'
KILLED  m6.02 paragraph unit deleted from both: 'If nothing qualifies, dropping the\ncheck is a sc'
KILLED  m6.03 paragraph unit deleted from both: 'Saying that the result now rests on the implemen'
KILLED  m6.04 paragraph unit deleted from both: 'When the check fails for real during implementat'
KILLED  m7 'qualifies only if' -> 'qualifies if', both plan copies
KILLED  m8 'it becomes' -> 'it may become', both plan copies
KILLED  m9 block heading removed, both proposal copies
KILLED  m10 block heading moved above '**Prospective only.**', both
KILLED  m11 block wrapped in a slot, both proposal copies
KILLED  m12 paragraph moved inside the doc-tooling slot, one plan copy
KILLED  m13 sentence added to one proposal copy
PASSED  control (after)
```

C3's ledger, rows in order:

```text
PASSED  control (before)
KILLED  m1 block word changed, Cairn copy only
KILLED  m2 block word changed, shipped copy only
KILLED  m3 paragraph word changed, one plan copy
KILLED  m4 paragraph deleted, one plan copy
KILLED  m5.00 block unit deleted from both: '### Independent scientific check'
KILLED  m5.01 block unit deleted from both: '*Gated to a change that touches a scientific ass'
KILLED  m5.02 block unit deleted from both: 'For every other change, one line — "N/A: no scie'
KILLED  m5.03 block unit deleted from both: 'Name **one** check that could show the change is'
KILLED  m5.04 block unit deleted from both: '* **What it compares.** The quantity, the expect'
KILLED  m5.05 block unit deleted from both: 'Say whether the data behind the expected value i'
KILLED  m5.06 block unit deleted from both: 'If the check depends on data that does not exist'
KILLED  m5.07 block unit deleted from both: '* **Why the expectation is independent.** Neithe'
KILLED  m5.08 block unit deleted from both: 'Its basis is one of these:'
KILLED  m5.09 block unit deleted from both: '* an analytical or manufactured solution;'
KILLED  m5.10 block unit deleted from both: '* a conservation law chosen against the error th'
KILLED  m5.11 block unit deleted from both: '* a trusted observation or benchmark;'
KILLED  m5.12 block unit deleted from both: '* an independent implementation, or the saved ou'
KILLED  m5.13 block unit deleted from both: "* a domain expert's expectation, written down be"
KILLED  m5.14 block unit deleted from both: '* **The error it would catch.** The plausible mi'
KILLED  m5.15 block unit deleted from both: 'This is security preflight S2\'s "Can it fail?", '
KILLED  m5.16 block unit deleted from both: 'At implementation, the implementer makes that mi'
KILLED  m5.17 block unit deleted from both: '* **When the check passes by finding nothing.** '
KILLED  m5.18 block unit deleted from both: 'Show the same analysis detecting a known effect '
KILLED  m5.19 block unit deleted from both: 'The failing\n  run above serves as the control wh'
KILLED  m5.20 block unit deleted from both: 'At implementation, the implementer records the c'
KILLED  m5.21 block unit deleted from both: 'For example, an analysis that reports no streamf'
KILLED  m5.22 block unit deleted from both: '**Reviewers.** The proposal reviewer challenges '
KILLED  m5.23 block unit deleted from both: 'The code reviewer verifies the recorded\nfailing '
KILLED  m5.24 block unit deleted from both: 'The Maintainer judges at the Decision whether th'
KILLED  m5.25 block unit deleted from both: 'If no independent basis exists, say so;'
KILLED  m5.26 block unit deleted from both: 'the Maintainer weighs that, and it is not a reas'
KILLED  m6.00 paragraph unit deleted from both: '**An independent scientific check is accepted sc'
KILLED  m6.01 paragraph unit deleted from both: 'A replacement qualifies only if it\nfails under t'
KILLED  m6.02 paragraph unit deleted from both: 'If nothing qualifies, dropping the\ncheck is a sc'
KILLED  m6.03 paragraph unit deleted from both: 'Saying that the result now rests on the implemen'
KILLED  m6.04 paragraph unit deleted from both: 'When the check fails for real during implementat'
KILLED  m7 'qualifies only if' -> 'qualifies if', both plan copies
KILLED  m8 'it becomes' -> 'it may become', both plan copies
KILLED  m9 block heading removed, both proposal copies
KILLED  m10 block heading moved above '**Prospective only.**', both
KILLED  m11 block wrapped in a slot, both proposal copies
KILLED  m12 paragraph moved inside the doc-tooling slot, one plan copy
KILLED  m13 sentence added to one proposal copy
KILLED  d1 'independent scientific check' -> 'review' at dimensions/complexity.md
KILLED  d1 'independent scientific check' -> 'review' at dimensions/README.md
KILLED  d1 'independent scientific check' -> 'review' at bootstrap/BOOTSTRAP.md
KILLED  d2 'review finding' -> 'note' in dimensions/complexity.md
PASSED  d3 old lens phrase restored beside the check, README (expected to pass)
PASSED  control (after)
```

**A check that passes by finding nothing.** None was run for the plan's own
sake: this plan touches no scientific assumption or computed result, so it
carries no independent scientific check of its own (N/A: no scientific
assumption or result touched). The new test passes when the copies are equal, and
the mutation ledgers above are the proof that it can fail.

**Known omissions.**
* **Boundary C is not done here.** In particular, the upgrade probe covered an
  adopter who filled a slot, not one who edited the block itself, and the
  reviewer's own sentence-by-sentence deletion on the reviewed commit is theirs.
* **C1's (B) call for stor-modflow was narrow** (see the C1 record), and the
  one "no" from C1 is to be reported again in the archive commit.
* **The gate manifest is not re-anchored.** The new file is one node added to the
  collection and is not yet a `frozen_files` key; the re-anchor is the
  Maintainer's and was not performed.
* **Timings of the small commands** are single runs, rounded.
* **The C2 and C3 byte and probe checks ran in worktrees at C2 and at C3 for
  their own chunk**, and were repeated at the tested commit where the tested
  commit differs from the chunk's (C3). The nine pin files were run alone at C2
  and are inside the full suite at the tested commit.

## Code review -- Claude Sonnet 5.5 -- 2026-10-18

```
Reviewed commit: 531084a1f638ad54f5e8d9e7a543411ad89c0f2a
Target: this plan's implementation range 33df0cb8..531084a1 (C2 27feca34, C3 531084a1, the tested commit) read against its parent 33df0cb8; the C1 record (0ac2b567, 4d9d632c, 33df0cb8); and the Boundary B record (2764eccd, which changes only this plan). Other sessions' commits in between are not read.
Prior findings: none
```

**Obligation**: Code review (the floor: not the implementing agent)
**Tier**: Internal
**Bounding**: not owed. Boundary B ran in `full` mode, and the field adjudicates a `bounded` record. I reproduced the full run on the tested commit (below). A fresh full run **is** owed after the revision, because SC-CR1 changes test bytes and SC-CR3 to SC-CR4, if taken, change executable template and test bytes.
**Findings**: raised (0 blocking, 1 medium, 5 low)
**Verdict**: REVISE -> `revising-code`. No answer the plan promised is wrong today. SC-CR1 is worth doing now because the new test is not yet frozen by the Maintainer's re-anchor, and an edit made after that ceremony owes a second one. The other five are for the author to take or answer with a reason.
**Model**: claude-sonnet-5-5

Distance: a fresh session of the implementer's agent type (Claude Sonnet 5.5). I wrote none of the code, the record, the plan or its reviews, and I am not the implementer. This is the Internal code review, whose job is falsification. It is not External: I ask whether the work meets the plan, not whether the plan should have been made. Interpreter for every figure: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13, in detached `git worktree`s of `531084a1` and `33df0cb8` in a fresh folder of my own (removed at the end). `git diff` on this plan file was empty when I claimed it and again just before I appended.

### In plain terms

**The work does what the plan said, and the recorded test run holds up.** I ran the full suite again on the tested commit and got the same numbers: 3510 passed, 2 failed, the same two AST tests that are red before this work too. The check text sits in the right place in all four template copies, byte for byte; an adopter who installs gets it; an adopter who has edited it keeps their edits on upgrade, or is shown a conflict, never silently overwritten.

**The new test is strong on words and weak on everything else.** I deleted every one of the 534 words of the two pinned texts, one at a time, in both copies, plus every sentence, and the test caught all of them. But it cannot see how the text is laid out or where it sits: flatten the list of five bases, delete one blank line, or move the block or the plan paragraph under a different heading, and the whole suite stays green (SC-CR1, medium). That matters because the test is the only lasting guard, and the cheap moment to strengthen it ends when the file is frozen.

**C1 stands, but read the "yes" with its caveat.** Every input was fixed before any draft; the scorer's quotes are real; the stop rule was applied as written. The stor-modflow "yes" is correct by the plan's rules and rests on a reference array that had never been saved. What the block showed there is that it made a blind author flag the false data claim, not that it produced a check that catches the priming error (SC-CR6).

Five smaller findings follow: a missing guard on one of the five bases, a hydrology point on the positive-control example, three wording mismatches in the promise sentences, the C1 briefs not being on file, and a sentence the archive commit should carry.

### The Boundary B record, checked against the tested commit

* **Right bytes.** The range is two commits (C2, C3), nine paths: the four templates, the three promise sites, the new test and this plan. `git diff --stat` over `bootstrap/_scaffold`, `bootstrap/tests/fixtures`, `bootstrap/verify_integrity.py`, `scripts`, `tools`, `doctrine`, `templates/modules`, `docs`, `AGENTS.md`, `dev/PLANNING.md`, `CHANGELOG.md` and `dev/.cairn` is empty. The range's changed paths and the manifest's 183 `frozen_files` keys do not intersect (control: `bootstrap/tests/test_scaffold.py` is a key).
* **3510 passed, 2 failed: reproduced.** `CAIRN_FULL_SUITE=1 ... --quality-gate-shuffle-seed=0 -rsfExX`, a fresh worktree of `531084a1`, clean before and after (0 lines of `git status --short`): **2 failed, 3510 passed, 3 warnings in 650.7 s**, 0 skipped, 0 xfail, 0 xpass. The two failures are `test_ast_attest.py::test_ast_gate_passes_over_the_full_scaffold_module_set` and `...::test_committed_baseline_accounted_for_across_the_engine_package`.
* **The same two at the base.** At `33df0cb8` the AST file gives 2 failed, 28 passed, the same two tests, and the failure text is identical once the worktree path and memory addresses are removed. The run's CHANGED list names the same five symbols with the same baseline and current hashes as the record (`_cmd_adopt_module`, `cmd_upgrade`, `create_dev_tree`, `main`, `seed_gitignore`). The engine bytes are identical across the range, so the set cannot differ.
* **One node added, and only one.** `pytest --collect-only -q bootstrap/tests` lists 3511 nodes at the base and 3512 at the tested commit; the difference is exactly `bootstrap/tests/test_scientific_check_guidance_ships.py::test_the_check_guidance_reaches_every_copy_and_promise_site`, the node ID in the record. That matches 3509 + 2 and 3510 + 2. I did not re-run the base's full suite; the collection difference and the AST file are what I checked there.
* **Gates.** Neutrality `fail=0 info=56` and redundancy `fail=0 info=0`, output identical to the base's after removing the worktree path. Instrument check: a vendor name put into the shipped proposal template turns the neutrality leg to `fail=1`, naming the line. `check_cairn.py` OK (182 files). `claim_check.py` exits 0 on the four templates and the three promise sites. `scaffold.py --manifest` is byte-identical to the base's (98 lines). A `grep -E 'Claude|Codex|Anthropic|OpenAI|Gemini|Cursor|LHM|modflow_tools'` over every added line in the range prints nothing, and prints a hit on a line known to hold `Cursor`.
* **The test's own text.** Its docstring carries no finding id, chunk letter or plan row (searched), and the test is named for the property it pins.

### The set, listed from the tree

The copies that must carry the guidance, from `git ls-files` and `git grep`, not from the diff: two proposal templates (`dev/proposals/_template.md`, `templates/core/dev/proposals/_template.md`), two plan templates, and three promise sites. No other file in the tree holds the `**Prospective only.**` line or the `A security-touching plan re-answers` sentence, so there is no third copy to miss. `git grep -i 'scientific[- ]trust'` outside archives finds only the module template the plan deliberately leaves (`templates/modules/team-gated/architecture_review_template.md`) and a mention in another open plan. Each promise site holds the phrase `independent scientific check` exactly once, so a replace-all in one site is as precise as a single-spot edit.

### Falsification ledger

A *mutant* is one deliberate break, made to see whether any check notices. It is *killed* if some check fails on it, *survived* if every check still passes, and *equivalent* only if measured to change no behaviour; I report an unmeasured equivalence as a survivor. Every mutant ran the **real** `pytest` on the **real** files in a worktree at `531084a1`, restored with `git checkout` and confirmed clean after each. My harness is my own, not the implementer's; it refuses to run outside my folder, and asserts that every mutant changed the files it meant to. Each run is beside an unmutated control that passed (six controls, before and after each of three drivers).

| Family | Mutants | Killed | Survived |
|---|---|---|---|
| Delete each sentence or list item of the block (27 pieces, listed from the tree), in both copies, the first copy only, the second only | 81 | 81 | 0 |
| The same for the plan paragraph (5 pieces) | 15 | 15 | 0 |
| Delete **each word** of the block (453), both copies at once | 453 | 453 | 0 |
| Delete **each word** of the plan paragraph (81), both copies at once | 81 | 81 | 0 |
| Markup and characters: indent the block by four spaces, `*` to `-`, a zero-width space, a Cyrillic `a`, an HTML comment inside the block, bold removed from the paragraph lead or from `one`, a sentence appended to one paragraph, the block moved above `**Prospective only.**` (two positions) | 10 | 10 | 0 |
| Promise sites: the phrase replaced at each of three sites; each site reverted to its pre-C3 text; `review finding` to `note`; the finding sentence deleted; `a computed result` to `any computed result`; `the independent` to `the Independent` | 10 | 10 | 0 |
| **Layout and place (below)** | 23 | 0 | **23** |

Total: 673 mutants, 650 killed, 23 survived. The positive-control bullet's 106 words and the *Reviewers* paragraph's 77 words, including `where one is owed`, are all among the killed. The first five rows say that the claim in the test's docstring is true: a clause deleted from both copies at once is noticed.

**The 23 survivors.** None is an error today; each is a way for the text to change that nothing notices.

| Survivor | What it does to the reader |
|---|---|
| S1: de-indent the five bases to top level (both proposal copies) | Not equivalent. Rendered with a CommonMark renderer, the nested list becomes one flat list (2 `<ul>` become 1) |
| S2.3: remove the blank line before `**Reviewers.**` | Not equivalent. Rendered, the *Reviewers* paragraph becomes part of the last bullet (the positive-control bullet) |
| S2.0, S2.1, S2.2, S2.4: remove each of the other four blank lines | Not rendered; reported as survivors. The block's last blank line and the one after the heading are likely harmless |
| S5: one space replaced by a non-breaking space | Prints the same. Harmless survivor |
| S10: a new sentence added as its **own paragraph** straight after the plan paragraph | By design (outside the pinned paragraph); noted so nobody thinks the paragraph is closed against additions |
| P1 x4: the whole block moved under `## Signals the change is wrong` (before `## Scope delta`), before `## Assurance path`, before `## Review`, before `## Decision` | The block stays word-perfect and sits after `**Prospective only.**`, so the test passes. C2's own criterion says it sits directly before `## Signals the change is wrong` |
| P2 x7: the plan paragraph moved above the security-touching paragraph, before `## Source proposal`, before `## Scope`, `## Scope delta`, `## Verification`, `## Dispositions`, `## Plan review` | Passes. C2's criterion says it sits after the security-touching paragraph, with "Red when ... above" it |
| D4: the check bullet moved from the Complex position to the Simple position | By design (presence only) |
| D5, D6: the I-2 sentence put back to the old lens promise with the phrase planted elsewhere; or reworded to the overclaim "decide which changes must name" | By design (presence only); C3's "says what is true" criterion is held once at C3, not by the test |
| D9: the old lens phrase restored beside the check in the README row | By design, as the plan says |

**Does anything else catch them?** The nine pin files named in the plan, the new test and `check_cairn.py`, run on seven of the layout survivors one at a time: 373 passed every time, `check_cairn.py` exit 0 every time. Then I applied six together (S1, S2.3, the block under *Signals*, the paragraph before *Verification*, D4, D6) and ran the **full suite** on that tree: **2 failed, 3510 passed**, the same two AST tests and the same count as the unmutated run. Nothing in the suite sees them.

### The upgrade probe: an adopter who edited the check itself

The implementer's probe covered an adopter who filled a slot. I asked what the merge does when the adopter changed the check text. I installed from the tested tree (`solo-greenfield`, `--non-interactive --allow-dev`) into fresh scratch repositories, edited the installed template, committed, and upgraded with `upgrade --plan` and `--stage` to a simulated next release: a copy of `531084a1` in which I changed three short phrases of the block and the paragraph (my own edits, not a real later plan).

| Adopter edit | `--plan` says | The staged copy |
|---|---|---|
| none (control) | no conflict | unchanged |
| a block line the release does not touch | locally-modified (merged clean) | classified only; I did not read the staged file |
| the same line the release changes | **conflict** | one conflict region; the adopter's line on the `ours` side, the release's on `theirs`; `--apply` refuses: "staged file ... still has conflict markers" |
| the whole block replaced by "N/A" | **conflict** | one region; the adopter's N/A against the whole new block |
| a plan-paragraph line the release does not touch | merged clean | classified only |
| the same plan-paragraph line | **conflict** | one region, both versions shown |
| first receipt, from the base tree: the adopter had hand-written their own scientific-check section in the same spot | **conflict** | one region, both kept |
| the same, but in another place | merged clean | one block, the adopter's section kept, no marker |

An edit is never lost and never overwritten silently; where the two overlap, the merge stops and says so. This is the engine behaving as designed and needs nothing from this plan.

### C1, the go/no-go exercise

* **Inputs fixed before the drafts: yes.** The order is `396c13d6` (17:49:02), `0ac2b567` (17:51:45, the inputs, the rule applied and the error statements), drafts extracted 17:54 (the record's time), `4d9d632c` (17:56:10, the drafts), `33df0cb8` (17:58:51, the scores). I recomputed every hash the record states and each matches: the 45-line wording (327d0b17...), the stor-modflow proposal at LHM `b9d4c59a` (427 lines, the commit that creates the file, 6971f519...), the assemble proposal at `dde80719` (360 lines, 3f36d81b...), both drafts and the scorer's output (taken from the fenced text in this plan). **The shipped block is byte-equal to those 45 lines** (the input the record names for the drafters), in both proposal copies, and so includes the positive-control bullet.
* **The opened texts hold no review and no mention of the defect.** I searched the stor-modflow text for `prim`, `warm`, `spin`, `cold start` and `ramp`: the only hits are the one RAMP mention on the date axis the record already names and the word "primitive". The draft's phrase "the accepted proposal" is the opened text's own reference to an earlier accepted proposal, so it is not a leak.
* **The second plan was chosen by the rule.** I re-applied it in LHM: of 46 archived plan files, the newest by archive commit is the assemble Part A plan (`72ccf3db`, 2026-10-15 12:12), then the Cedar Creek plan (2026-10-14 15:17). Its first code review's CR1 is the 0/0 fill that writes missing-data weights. I also read the stor-modflow error statement against the commits it cites: the "not saved" message and the 2.80 GB figure are in `dae97b43`, and the +14.91, +13.5 and -1.2 figures in `6dcc0cc5`.
* **Blind: attested, not shown.** The record says so itself: the briefs are the coordinating session's account and the implementer did not see them. I cannot see them either, so I tested the drafts instead. Every concrete fact in both drafts (file name, 137 MB, 798 x 647, 312 months, 26-deep stack, 1358 periods, `matlabParity`, `cell_statistics`, the Cedar mention) is in the text as opened, and neither draft contains any of the words only the later reviews use. That is consistent with blindness and cannot prove it. See SC-CR5.
* **The scorer was separate, and every "yes" has a real quote.** I checked each quoted sentence by string search against the draft it names: all are verbatim. The record also gives the (A)-alone column beside the combined verdict, as C1 demands.
* **The stop rule was applied as written.** Stop only if both are "no"; one is "yes"; the "no" is reported; neither softened to a warning nor hardened to "either".
* **The (B) call, which I would have made the same way.** The draft's bullet is headed "Data in hand", but its text says nobody has recorded opening the file, lists "that the variable exists" as not checked, and names the file to open. That is the plan's "not confirmed, and names what would be opened" branch; reading the text over the label is right. I would not call it narrow. It is the case the rule was written for: the exercise could have failed this draft (it is exactly the compare-with-saved-output shape the plan feared) and the draft passed because the block's own data-status prompt made its author write the doubt.
* **Where I would press instead: (A), and what the "yes" shows.** (A) is "yes" only on the condition that the array exists, and it did not. Asked what error it would catch, the draft names a different mistake (a hard-coded one-day stress period), says it cannot source a tolerance, and after "Open OUTS" offers no fallback basis for the unsaturated store. So the honest reading of the stor-modflow "yes" is the implementer's caveat, sharpened: the block would have exposed the false data claim earlier, and the author would then have owed "no independent basis exists, say so", which the block allows. It would not by itself have produced a check that catches priming. That is worth having, and it is a smaller thing than "the block yields a check that catches the error". The assemble "no" is as the record says: a good check for the change the proposal describes, aimed at a different risk than the one that later bit.
* **My overall view.** The exercise was run properly and the plan was right to continue. It is weak positive evidence for the block's data-status prompt and no evidence yet for the independent-basis half, which the record already says. The archive commit should say that in the same sentence as the "no" (SC-CR6).

### The two judgment calls beyond the spec

* **The drafters saw only the C2 block.** C1 says "the wording (the 'Wording each chunk lands' texts ...)", plural. The implementer gave the proposal-template block alone and said so before any draft existed, with a reason. I judge it within the plan and the more faithful test: a proposal author fills in the proposal template and never sees the plan paragraph, the promise sentences or the test description, and the plan's own *In brief* says the wording is tried "using only the text each proposal had when it was opened". Withholding the rest can only give the drafter less, and the draft quality does not suggest it was short of anything. No finding.
* **Slot containment, and three extra mutants.** The plan's group (c) says the block and paragraph "hold no marker". The implementer added a check that neither sits *inside* a slot (`_inside_a_slot`), and mutants m11 to m13 (wrapped in a slot, the paragraph moved into the doc-tooling slot, a sentence added). That is the plan's own "Red when: ... in a slot" made executable, adds no node, and cannot go red on any layout the plan allows. The controls show no false red from it. Within the plan; the extra mutants only strengthen the ledger. No finding.

### The positive-control addition

* **Exactly as fixed.** The shipped bullet is the plan's fenced text, byte for byte (the same comparison as above). It opens "When the check passes by finding nothing", names the three absences ("no change", "no difference", "no effect"), says the failing run is the control when its mistake produces an effect of that size, says the implementer records the control with the failing run, and keeps the streamflow example. The *Reviewers* paragraph says the code reviewer verifies the control "where one is owed". The word "planted" appears nowhere in the shipped text, as the Maintainer's "let's not do planted errors" requires.
* **Pinned.** All 106 words of the bullet and 77 of the *Reviewers* paragraph are among the 453 single-word deletions, every one killed, and every sentence-level deletion that touches the bullet is killed in each copy. Its placement and layout fall under SC-CR1 like the rest of the block.
* **Read against the three cases the plan names.** A tooling change goes to the gate's N/A before the bullet matters. A change whose check finds an effect is outside the bullet, which is keyed to the check's pass condition ("passes on no change") and not the result. A refactor whose pass is "output unchanged" is the bullet's own case: the failing run (perturb an input by the tolerance) is both the deliberate break and the control, so no second run is owed, and the bullet says who records it and with what. I found no misfire. One hydrology point on its example is SC-CR3.

### The plan's other Boundary C questions

* **Is the independence real?** I tried the five bases in turn. Four carry a guard in their own words: the conservation basis ("a closed budget does not catch a wrong input"), the independent implementation or saved output ("independent of the port, not of the model's physics"), the analytical or manufactured solution, and the "trusted" observation. The fifth, "a domain expert's expectation, written down before the result is seen", guards the timing and not who the expert is (SC-CR2).
* **The gate.** The opening sentence sends a pure tooling change to N/A and a change that touches a governing equation, unit, sign convention, boundary condition, parameter default, calibration or coupling to a check, in both directions, and the N/A line it prescribes is worded so it can be written truthfully. Data-processing steps whose output becomes model input are not named in the list; the assemble draft treated one as in-gate. That is a reading the block permits, not a gap I would fix. The Complex-position sentence is wider than the gate (SC-CR4).
* **Read cold as an adopter.** A solo scientist with one agent and no `doctrine/` can follow the block and the paragraph from the shipped templates: the only outside reference is "security preflight S2", which sits in the same template about forty lines above, and *Scope delta* is a heading in the plan template. The one thing they cannot tell is whether the "domain expert" may be the agent (SC-CR2).

### Findings

None blocks. SC-CR1 should be taken before the re-anchor; the rest are the author's call.

#### SC-CR1 -- Medium -- The test pins words, not layout or place, and nothing else does either

**Plain.** The test proves every word of the two texts is present in all four copies. It does not prove the list is still a nested list, that the *Reviewers* paragraph is still its own paragraph, or that the block and the paragraph still sit where the plan put them. Each of those can break with the suite green.

**Precision.** (1) Whitespace is collapsed before comparing (the plan fixed that), so S1 and S2.3 survive and, rendered, change the page: the five bases flatten, and *Reviewers* is swallowed into the last bullet. (2) Group (c) checks that the block is *after* `**Prospective only.**` and that neither text is *inside a slot*, as the plan specified. C2's acceptance criteria, which the implementer held once by a line search, also say the block sits before `## Signals the change is wrong` and the paragraph after the security-touching paragraph, with "Red when" conditions for the opposite. The test holds neither: P1 (four places) and P2 (seven places) survive, including the block under the *Signals* heading and the paragraph under *Verification*. (3) The full suite on six of these together is unchanged (3510 passed, the same two AST failures). (4) The docstring says "It also pins where the text sits"; that is true of the block's lower bound and the slot rule, and not of the rest. (5) The test is not yet in the gate manifest. The re-anchor will freeze it, and every edit after that owes another re-anchor, so this is the cheap moment.

**Closes when** the test also holds: (a) no `## ` line between the `**Prospective only.**` line and the block heading, and the next `## ` line after the block is `## Signals the change is wrong`; (b) in each plan copy, the nearest `## ` line above the paragraph is `## Acceptance criteria`, and the paragraph comes after the line starting `A security-touching plan re-answers`; (c) beside the collapsed words, the *shape* of each region: for every blank line and every line that starts a list item, its position in the sequence, indent width and marker, leaving line wrapping free. S1, S2.3, the four P1 and the seven P2 mutants then die (re-run them: the harness is a few lines per mutant). It stays one node. If the author would rather not, the docstring must say exactly what is and is not pinned, and the *Known omissions* paragraph must name layout and place, with the reason.

#### SC-CR2 -- Low -- "A domain expert's expectation" has no guard against the author being the expert

**Plain.** Four of the five bases say what stops them being circular. The fifth does not say that the expert is someone other than whoever wrote the code. With one human and one agent, the agent can write "I expect about 0.003 ft/d" from the same reading of the units as its code, before running anything, and meet every word of the basis.

**Precision.** This is the Boundary C independence attack, tried on each basis; the expert basis is the soft one. The lead sentence ("a test written from the same understanding") excludes it if the reader applies it, and the Maintainer's Decision-time judgment and falsifier F2 ("most bases are the Maintainer's expectation") both watch for it, so it is not a hole, only the place a ritual check would enter.

**Recommended.** Do not edit the accepted text for this alone. Add to the revisit row's F2 (in *Dispositions*) the exact mode to look for: "the expert is the author of the change, or the agent". If the author is revising the block text anyway for SC-CR3, add "someone other than the author of the change" in the same commit; it costs one clause in each of the three places the text lives.

#### SC-CR3 -- Low -- The positive-control example matches the rate, but detectability depends on more

**Plain.** The example says an analysis that reports no streamflow depletion from a pumping well should first recover "the depletion of a synthetic well of comparable rate". Whether a depletion is detectable depends on the well's distance from the stream, how long it pumps, the streambed conductance and the noise in what is measured, not on the rate alone. A synthetic well of the same rate placed closer, or pumped longer, shows a larger effect than the real one, and the control would pass while the real, smaller effect would be missed.

**Precision.** The bullet's rule is sound ("a known effect of the size that matters"); the example under-specifies how to reach that size. This is the Maintainer's home ground, so it is put as a plain question with a default: **leave as is, or change the example?** Recommended default: change "a synthetic well of comparable rate" to "a synthetic well at the real well's rate, distance from the stream and pumping schedule". The edit is the same three places as any wording change (both proposal templates, the test's block literal, this plan's fenced text), made in one commit, and the full run after the revision covers it.

#### SC-CR4 -- Low -- Three triggers for one gate in the promise sentences, and the test's phrase match is case-sensitive

**Plain.** The block's gate is "a scientific assumption, or a result the project publishes or acts on", and its N/A line says no "scientific assumption or result touched". `dimensions/complexity.md` says "a scientific assumption or a published result", and then pins "an unexplained "N/A" on a change that touches a computed result is a review finding". A project that computes an intermediate it neither publishes nor acts on may truthfully write N/A under the block, while the Complex position reads that as a finding. "Unexplained" softens it; a reviewer still cannot tell which reading governs.

**Precision.** (1) The pinned sentence is wider than the gate it enforces. (2) The `bootstrap/BOOTSTRAP.md` I-2 sentence says "those" (the scientific-surface *and* documentation-trust sections) "show which changes touch a scientific assumption"; only the first does. (3) Group (d) tests `independent scientific check` as an exact lower-case string (D8): a harmless rewrite that starts a sentence with "Independent scientific check" turns it red, and the sibling plan that rewords the same Complexity cell is now implementing.

**Recommended.** Align the pinned sentence to the block ("... on a change that touches a result the project publishes or acts on is a review finding") and change `_COMPLEXITY_FINDING` in the same commit; make group (d) compare lower-cased text; in I-2, say "the scientific-surface section shows ...". Only the first two edit pinned bytes.

#### SC-CR5 -- Low -- The C1 briefs are not on file

**Plain.** C1 asked that the drafter and scorer get two pasted texts and no repository access. They got a read tool, two files in a folder, and an instruction. The record discloses that, and counts three tool calls per drafter and five for the scorer. The briefs themselves, and who confirmed them, rest on the coordinating session's account.

**Precision.** My own leak test (every concrete fact in the drafts is in the opened text; none of the later reviews' vocabulary appears) found nothing, so I do not think the result is wrong. But blindness is the property C1 exists for, and a reader a year on can only take it on trust.

**Recommended.** If the coordinating session still holds the three briefs, append them (or their SHA-256) to the record; if not, one line saying so. No re-run.

#### SC-CR6 -- Low -- The archive duty carries the "no" and not the caveat on the "yes"

**Plain.** C1 says the one "no" is repeated to the Maintainer in the archive commit, and *Dispositions* says the revisit also reads the C1 record. Neither repeats the caveat that the stor-modflow "yes" rests on a reference array that had never been saved.

**Recommended.** Add one sentence to *Dispositions*' archive bullet: the archive commit and the board row also say that stor-modflow's "yes" rested on an array that was never saved, so what the block showed there is that its data-status prompt made a blind author flag the false claim, not that it yielded a check that catches the priming error. Otherwise a later reader takes the one "yes" as support for the independent-basis half.

### Waiting-line check

`git log -p` on this plan over `396c13d6^..2764eccd` adds no `**Waiting on Maintainer**` line (the only match is a table cell describing the template check). The one fenced chunk, M (the re-anchor), is not reached by this range, and its wait is declared on the marked board row, as the chunk says. The range makes no deviation request: the narrowed wording and the extra mutants are within the plan, as above.

### What I did not cover

* I did not read the coordinating session's transcripts, so the drafter and scorer briefs are unseen (SC-CR5).
* I did not re-run the base's full suite; I checked its AST file, its collection and its gates, and took its 3509 from the record. I did not re-run the exercise, or judge the drafts beyond the scorer's two questions.
* Rendering was measured with one CommonMark renderer for S1 and S2.3 only; the other layout survivors are reported as survivors, not as equivalent or harmful.
* The next release in the upgrade probe is my own small edit, not a real later plan, and I read the staged file for four of the eight rows only. I did not run the combined survivors through every install-family test one at a time; the full-suite run on six together is the evidence.
* I read the error statements against the LHM commits for the figures and the missing array (and the assemble CR1), not the full reviews in LHM, and not the run output.
* I did not try Windows line endings, or a template read by a different Markdown tool than CommonMark.
* The scientific content: I read the positive-control bullet and its example as a hydrogeologist would (SC-CR3). Whether the five bases are the right five, and the Complex-position policy, are the Maintainer's.
* The gate-manifest re-anchor and the AST re-anchor: not run, and not mine to run.

## Response to code review -- Claude Sonnet 5.5 (implementer) -- 2026-10-19

**In plain terms.** All six findings are taken; none is declined. The one that
mattered (SC-CR1) is fixed: the test now also notices a flattened list, a lost
blank line, or the block or plan paragraph moved to the wrong place, and it
still sits in one test. Each of the reviewer's survivors that I could rebuild
was killed, and three small wording fixes and one new rule for the archive
commit are in. The positive-control example now reads as the Maintainer chose.
Nothing is pushed. The full suite is run again afterwards, because test bytes
changed; its record follows this section.

**The code commits of this revision** (parent `c504fca8`, the last commit before
the first of them):

| Finding | Commit | What changed |
|---|---|---|
| SC-CR1 | `86db42ae` | the test pins layout and place |
| SC-CR4 | `e2978e44` | one trigger in the three promise sentences; case-insensitive match |
| SC-CR3 | `550750fb` | the example wording, at the Maintainer's instruction |

| Finding | Disposition | Where it landed |
|---|---|---|
| **SC-CR1** (medium) the test pins words, not layout or place | **accept, in full** | `86db42ae`. See below. |
| **SC-CR2** (low) the expert basis has no guard against the author being the expert | **accept the recommendation: no text edit** | An archive duty (below): name the mode under F2 on the revisit row. |
| **SC-CR3** (low) the example matches the rate only | **accept, at the Maintainer's instruction** | `550750fb`. His question and answer, verbatim, below. |
| **SC-CR4** (low) three triggers for one gate; case-sensitive match | **accept** | `e2978e44`. See below. |
| **SC-CR5** (low) the C1 briefs are not on file | **accept** | The three briefs are recorded verbatim below, with SHA-256. |
| **SC-CR6** (low) the archive duty carries the "no" and not the caveat on the "yes" | **accept** | An archive duty (below), sharpened by what the briefs show. |

### SC-CR1: layout and place, pinned

The test (still the one function, still one node) now compares, beside the
collapsed words:
* **Layout.** The blank lines, the headings, the list items (with their indent
  and marker) and the paragraph starts of each region, in order. Line wrapping is
  the only thing left free. The block must end with exactly one blank line before
  the next `## ` line, and its heading and the plan paragraph must follow a blank
  line.
* **Place, proposal templates.** No `## ` line between the `**Prospective only.**`
  line and the block, and the line after the block is `## Signals the change is
  wrong`.
* **Place, plan templates.** The nearest `## ` line above the paragraph is `##
  Acceptance criteria`; the paragraph follows the paragraph starting `A
  security-touching plan re-answers`; and it sits before the opening of the
  `acceptance-doc-tooling` slot.
* **Whitespace.** The collapse now treats only ASCII space, tab and line breaks
  as whitespace, so a non-breaking space counts as a change.

**One departure from the reviewer's recipe, with the reason.** The review's
closing rule for the plan paragraph (nearest `## ` is `## Acceptance criteria`,
and after the security paragraph) leaves one of its own seven P2 mutants alive:
the paragraph moved to just before `## Scope delta`, which is still under
Acceptance criteria but after the slot. The plan's own C2 criterion says "before
the acceptance-doc-tooling slot", so I made that third rule part of the test. It
costs one coupling: if a later plan renames that slot, the test says so.

**What the mutants say.** The reviewer's harness was not available, so I rebuilt
the survivors from the review's table: S1; S2.0 to S2.4; S5; P1 (four places);
P2 (seven places). Against the committed test before this revision, **those 18
survive** (the harness is sound: they are the reviewer's survivors), as do two of
my own (a loose list; the first bullet indented). Against the revised test **all
20 are killed**. Re-wrapping a sentence, and re-wrapping the plan paragraph,
still pass, as intended. The full ledger at the tested commit is in the
verification record that follows.

**What is still not pinned, said plainly.** Text added as its own paragraph
beside the pinned ones (S10); the check bullet's position among the Simple and
Complex bullets (D4); the I-2 sentence's wording beyond the check's name (D5,
D6); and, after SC-CR4, the first sentence of the Complex-position bullet and the
I-2 trigger (their gate phrase is not pinned; the pinned N/A finding carries it).
These are the "presence only" choices the plan made so a later plan may reword
the cells, and the test's docstring says what is and is not pinned.

**For the sibling plan.** The test now holds the block's position directly before
`## Signals the change is wrong`, the plan paragraph under `## Acceptance
criteria`, and the layout of both texts. A plan that moves or reshapes either
has to edit this test in the same commit. The test is still not in the gate
manifest (checked: the new file is not among the 183 `frozen_files` keys), so
these edits owe no second re-anchor.

### SC-CR3: a wording change at the Maintainer's instruction

The coordinating session put this question to the Maintainer, and he answered.
Verbatim, as relayed to me on 2026-10-19:

> "Plan D's positive-control example currently reads: an analysis reporting no streamflow depletion 'first recovers the depletion of a synthetic well of comparable rate'. The reviewer notes that detectability also depends on distance to the stream, the pumping schedule and streambed conductance. Change the wording?"

His choice, verbatim:

> "Same rate, distance, schedule (Recommended)". That option read: "'…of a synthetic well at the same rate, distance and schedule'."

**What changed (`550750fb`).** In both proposal templates, and in the test's
pinned block, and in this plan's fenced C2 wording, the example sentence ends
"...first recovers the depletion of a synthetic well at the same rate, distance
and schedule." where it ended "...of a synthetic well of comparable rate." The
plan templates did not hold the example and are untouched. Two new mutants (the
example put back to "comparable rate"; "distance" dropped) are killed.

### SC-CR4: one trigger, and a case-insensitive match

The block's gate is "a scientific assumption, or a result the project publishes
or acts on". The promise sentences now say that and no other (`e2978e44`):
* `dimensions/complexity.md`, Complex position. The bullet: "expected of every
  change that touches a scientific assumption or a result the project publishes
  or acts on" (it said "a published result"). The pinned finding: "an
  unexplained "N/A" on a change that touches a scientific assumption or a result
  the project publishes or acts on is a review finding" (it said "a computed
  result").
* `bootstrap/BOOTSTRAP.md`, I-2. "those drive the legacy-agent decision, and the
  scientific-surface section shows which changes touch a scientific assumption or
  a result the project publishes or acts on, and so need the proposal template's
  independent scientific check." (It said "those" show it; only the
  scientific-surface section does.)
* The test's fourth group lower-cases both sides, and pins the new finding
  sentence. Presence only still holds. The README Complexity row never carried a
  trigger and is unchanged.

### Where the plan's fixed wording changed, and why

The "Wording each chunk lands" texts are the bytes the test is generated from and
the bytes a reviewer compares against. Two changes after implementation began
were made to them **in place**, to keep one source of truth, and are listed here
so the change is not silent. What was reviewed is in git at `531084a1` and
`2764eccd`.
* The C2 block's example sentence (SC-CR3; `550750fb`): "of a synthetic well of
  comparable rate" became "at the same rate, distance and schedule".
* The C3 Complex-position bullet and the C3 I-2 text (SC-CR4; `e2978e44`), to the
  texts above, and the two sentences elsewhere in the plan that quote the pinned
  finding (the fourth group's description, and the C3 criterion "The complex-
  project finding is stated"). The C3 criterion on bytes now means the revised
  fenced text.

Every other cell, and the review sections, are untouched.

### SC-CR5: the C1 briefs, on file

The coordinating session extracted the three prompts it sent from its own
transcript on 2026-10-19 and handed them to me; I did not see them when I wrote
the C1 record. All three agents were Sonnet. Verbatim, each with the SHA-256 of
the file it was taken from, and no fence of its own:

**Drafter, stor-modflow** (15 lines). SHA-256
`2ab39e8efa508aacffeec221844fbf37ddba0ff1204714ab72e90810b5640a7a`.

```text
You are the author of a scientific-software proposal, filling in one section of it. This is a blind exercise. **You may read exactly two files, and nothing else.** Read them with the Read tool:

1. `/private/tmp/claude-501/-Users-kendal30-Code-cairn/79ada448-b159-4255-b0ea-444b74328be1/scratchpad/c1-inputs/wording-independent-scientific-check-block.md`: the instructions for a section called "Independent scientific check".
2. `/private/tmp/claude-501/-Users-kendal30-Code-cairn/79ada448-b159-4255-b0ea-444b74328be1/scratchpad/c1-inputs/stor-modflow-proposal-as-opened.md`: your proposal, exactly as you opened it.

**Rules:**
- Do not read, search or list any other file or directory.
- Do not run commands.
- Do not use the web.
- Work only from those two texts.
- If you would want to check something, the data behind it for example, you cannot. Say so in the section, as its instructions ask, and name what you would open to confirm it.

**Task.** Following the section's instructions exactly, write the "Independent scientific check" section for this proposal, as its author would at the moment the proposal was opened. Be concrete: the quantity, the expected value and tolerance with its source, whether the data behind it is in hand, why the expectation is independent, the plausible mistake under which the check would fail, and the positive-control clause if your check passes by finding nothing. If you judge that no independent basis exists, say so plainly. Don't invent one.

**Reply** with only the filled section, in Markdown, starting with its `### Independent scientific check` heading. Add no commentary before or after it.
```

**Drafter, assemble part A** (17 lines). SHA-256
`6e1a6eb6018845418944e2211a0a7ccfd5df315f518df9af1b3aaa505a0c5b66`. The part
sentence in it is the one fixed in the C1 record, word for word.

```text
You are the author of a scientific-software proposal, filling in one section of it. This is a blind exercise. **You may read exactly two files, and nothing else.** Read them with the Read tool:

1. `/private/tmp/claude-501/-Users-kendal30-Code-cairn/79ada448-b159-4255-b0ea-444b74328be1/scratchpad/c1-inputs/wording-independent-scientific-check-block.md`: the instructions for a section called "Independent scientific check".
2. `/private/tmp/claude-501/-Users-kendal30-Code-cairn/79ada448-b159-4255-b0ea-444b74328be1/scratchpad/c1-inputs/assemble-full-port-proposal-as-opened.md`: your proposal, exactly as you opened it.

**Which part you are drafting for:** The plan you are drafting for implements Part A of this proposal ("The stage's foundation", A1 to A3). It is plan 1 of 6 for the whole proposal.

**Rules:**
- Do not read, search or list any other file or directory.
- Do not run commands.
- Do not use the web.
- Work only from those two texts and the sentence above.
- If you would want to check something, the data behind it for example, you cannot. Say so in the section, as its instructions ask, and name what you would open to confirm it.

**Task.** Following the section's instructions exactly, write the "Independent scientific check" section for Part A of this proposal, as its author would at the moment the proposal was opened. Be concrete: the quantity, the expected value and tolerance with its source, whether the data behind it is in hand, why the expectation is independent, the plausible mistake under which the check would fail, and the positive-control clause if your check passes by finding nothing. If you judge that no independent basis exists, say so plainly. Don't invent one.

**Reply** with only the filled section, in Markdown, starting with its `### Independent scientific check` heading. Add no commentary before or after it.
```

**Scorer** (38 lines). SHA-256
`43f273d91f5f20694573d07d2ad61d12296670d0b5472bbe6d449ea09113aea7`.

```text
You are a **scorer** in a small blind exercise. You are not the person who drafted the texts you score, nor the person who will record your answers. **You may read exactly four files, and nothing else.** Read them with the Read tool, all in `/private/tmp/claude-501/-Users-kendal30-Code-cairn/79ada448-b159-4255-b0ea-444b74328be1/scratchpad/c1-inputs/`:
1. `draft-stor-modflow.raw.md`: draft 1.
2. `error-stor-modflow.txt`: the error later found in the work draft 1 was written for.
3. `draft-assemble-part-a.raw.md`: draft 2.
4. `error-assemble-part-a.txt`: the error later found in the work draft 2 was written for.

**Rules:**
- Read, search or list no other file or directory.
- Run no commands.
- Do not use the web.

**Background.** Each draft is an "Independent scientific check" written by a proposal's author, at the moment the proposal was opened, before any code existed or any review happened. The check is meant to be one that could show the change is wrong about the world. The error file says what actually went wrong later, as found by a reviewer.

**For each draft, answer two questions. Every "yes" must quote, verbatim, the draft sentence that carries it.** A "yes" with no quoted sentence does not count.
- **(A) Does the draft name a check that fails under that error?** That is: if the check described were run on the work as it was with the error in place, would it fail? Reason it through concretely from the error statement.
- **(B) Is that a check that could have been run?** The draft's data-status statement must do one of two things:
  - confirm the data is in hand and name what was opened; or
  - say the data is not confirmed **and name what would be opened to confirm it** (a file or an array).

  A stock hedge that names nothing does not count. Also: **where the error statement shows the draft's data claim to be false or never checked, a draft that repeats the claim as "in hand" fails (B).** For example, the stor-modflow error statement says something about whether a reference array was ever saved.

**The verdict** for a draft is **yes** only when (A) and (B) are both yes.

**Record, but do not score:** whether the check's basis is one of these listed kinds, and whether it is independent of the code under review:
- an analytical or manufactured solution;
- a conservation law chosen against the error;
- a trusted observation or benchmark;
- an independent implementation, or the saved output of the model the code reads;
- a domain expert's written expectation.

**Reply** with only this, in Markdown, for each draft in turn:
- `#### Draft N (<name>)`
- **(A):** yes or no, then one to three sentences of reasoning, then the quoted draft sentence if yes.
- **(B):** yes or no, then reasoning, then the quoted draft sentence if yes.
- **Verdict:** yes or no.
- **Basis (not scored):** which kind, and whether it is independent of the code.

Add nothing else.
```

**What the briefs show.**
* The record's account was right. Each drafter was told to read exactly two named
  files, to read, search and list nothing else, to run no commands and to use no
  web; the scorer, to read exactly four named files. No brief names a path into
  the LHM repository, an error statement or a review (the scorer's brief points
  at the stor-modflow error statement because the scorer reads it). Blindness is
  still by instruction and by the observed tool counts, not by a sandbox.
* **A disclosure the review could not make, and it matters to SC-CR6.** The
  drafter briefs add a sentence the block does not carry: if the drafter would
  want to check something, the data behind it for example, it cannot; it should
  say so in the section "and name what you would open to confirm it". That is
  nearly word for word the branch of (B) the scorer's rubric accepts ("not
  confirmed, and names what would be opened"). So the drafters' hedges on data
  status, and the stor-modflow draft's narrow pass of (B) in particular, owe part
  of their form to the brief and not only to the block's own data-status prompt.
  The block asks the author to say whether the data is in hand and has been
  checked, and to say so if the data does not exist yet; it does not tell an
  author to name the file to open.

### SC-CR6 and SC-CR2: duties for the archive commit

*Dispositions* is filled at archive-preparation and is not edited here (the plan
is past the point where its cells revise in place). The archive preparer finds
these two additions to its duties in this section:

1. **Repeat the "no" and the caveat on the "yes", together, in the archive commit
   and on the revisit row.** Suggested wording: *C1 ran on two past LHM plans.
   Assemble part A said no: its draft was a good check for the change the
   proposal described, aimed at a different risk than the one that later bit
   (the fill for uncovered land-use cells), which the proposal as opened never
   mentioned. Stor-modflow said yes, but its check was against an array that had
   never been saved, and the drafters' briefs told them to name what they would
   open to confirm any data they could not check. What that showed is that the
   block's data-status prompt, with that help, made a blind author flag the false
   data claim. It is weak positive evidence for that prompt, none yet for the
   independent-basis half, and not evidence that the block yields a check that
   catches the priming error.* The revisit reads the C1 record with this in view.
2. **Name the author-as-expert mode under falsifier F2.** On the revisit row (the
   "0.3 external correctness test (R-H third-party probe)" row in
   `dev/PLANNING.md`), F2 reads "most bases are the Maintainer's expectation".
   Add the mode the review found: *or the "domain expert" is the author of the
   change, or the agent that wrote the code.* No edit to the accepted block text.

## Implementation verification -- Claude Sonnet 5.5 (implementer) -- 2026-10-19

This is the second record. The first (2026-10-18) covers the original work and
stands. This one covers the revision made after the code review; test bytes
changed in it, so a fresh full run is owed and is recorded here.

**In plain terms.** The full suite gives the same result before and after the
revision: 4432 passed, 2 failed, and the 2 failures are the same two AST tests
that were red at the revision's base, on the same five engine functions. The
revised test was run against 80 deliberate breaks of the templates and the
three promise sites; 74 were caught and the 6 that pass do so by design. One
thing outside this plan turned up and is reported below, not fixed.

**Boundary B mode**: full. The same four reasons as the first record hold; the
revision changes test bytes and two shipped templates.

**Tested commit**: `550750fb6c45a769077b62500e56d3aef407c57a` (the last code
commit of the revision).

**Reviewed range**: base `c504fca86a9ce17b2160bbdd30e71a4e81aba91e` to tested
`550750fb6c45a769077b62500e56d3aef407c57a`. Three commits:
`86db42ae86b0dec2d748cf3c7ba38537dbb17449` (layout and place),
`e2978e446f16dcb64ebf3645c26eaa93b2511696` (one trigger),
`550750fb6c45a769077b62500e56d3aef407c57a` (the example wording). The range
changes six paths: `bootstrap/BOOTSTRAP.md`, `dimensions/complexity.md`, the two
proposal templates, the test and this plan. The Response commit
`1e4f1e968fc9a112c664dbe10e5c6a336d0be367` follows the tested commit and changes
only this plan.

**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python
3.13.13 (conda-forge), pytest 9.0.3.

**Pre-run state**: each full run was in a fresh detached `git worktree`, `git
status --short` empty (0 lines), `HEAD` the commit named. **Post-run state**:
`git status --short` empty (0 lines), `HEAD` unchanged. The mutation ledgers and
the probes ran in other worktrees at the same commits, so nothing mutated a
worktree that a full run used. The two full runs were done one after the other.

| Command | Exit | Outcomes | Elapsed |
|---|---|---|---|
| `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0 -rsfExX` at the tested commit | 1 | **2 failed, 4432 passed**, 0 skipped, 0 xfail, 0 xpass, 3 warnings | 793.0 s (10:50:08 to 11:03:22) |
| the same command at the base `c504fca8` | 1 | **2 failed, 4432 passed**, 0 skipped, 0 xfail, 0 xpass, 3 warnings | 870.8 s (11:03:33 to 11:18:10) |
| `python scripts/quality_gate.py --sub neutrality --sub redundancy` | 0 | neutrality `fail=0 info=56`, redundancy `fail=0 info=0`; the neutrality output is identical to the base's, line for line | 1.4 s |
| `python scripts/check_cairn.py` | 1 | one issue, in `dev/reviews/2026-10-18-security-review-session-writes.md:131` (the path `tools/__pycache__`, which exists only in a working tree that has run Python); the same issue at the base; none in a file this revision edits | 2.2 s |
| `python bootstrap/scaffold.py --manifest` | 0 | byte-identical to the base's (98 lines) | under 1 s |
| `python bootstrap/verify_integrity.py --target .` | 1 | 18 violations, output identical to the base's; `--finalize` not run | 0.1 s |
| `python scripts/claim_check.py <file>` on the four template copies, `dimensions/complexity.md`, `dimensions/README.md`, `bootstrap/BOOTSTRAP.md` and this plan | 0 each | OK, no flags | under 1 s each |
| `python -m pytest --collect-only -q bootstrap/tests/test_scientific_check_guidance_ships.py` | 0 | 1 test collected | 0.0 s |

`check_cairn.py` exits 1 in a clean worktree because of an issue in another
session's review file. It is the same at the base, so it is not this revision's.
In the shared working tree, where `tools/__pycache__` exists, it reports OK.

**Node ID** (unchanged, one node): `bootstrap/tests/test_scientific_check_guidance_ships.py::test_the_check_guidance_reaches_every_copy_and_promise_site`.
The full-suite counts are equal at the base and the tested commit (4432 + 2), as
they should be: the revision adds and removes no test. They differ from the first
record's 3510 + 2 because other plans have since landed tests.

**Non-pass disposition.**
* The two failures are `test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package`
  and `test_ast_attest.py::test_ast_gate_passes_over_the_full_scaffold_module_set`.
  Both fail at the base `c504fca8` in the full run, with the same failure text
  as at the tested commit (compared after removing the worktree path and the
  memory addresses of function objects).
* The CHANGED set by the runbook's Step 1 method is the same at the base and at
  the tested commit: **CHANGED 5, MISSING 0, DUPLICATE 0, NEW 86**, the same five
  symbols with the same hashes as in the first record (`_cmd_adopt_module` and
  `cmd_upgrade` in `upgrade.py`; `create_dev_tree` and `seed_gitignore` in
  `install.py`; `main` in `cli.py`). `git diff --stat c504fca8..550750fb` over
  `bootstrap/_scaffold` and `bootstrap/tests/fixtures` is empty.
* No skip, xfail or xpass in either run. `test_a_t4_output_is_bounded` passed in
  both. The 3 warnings are the same third-party deprecation notice in both.
* Re-anchoring the AST baseline is the Maintainer's and was not done.

**Frozen files and nodes.** The range's changed paths and the 183 `frozen_files`
keys in `bootstrap/tests/fixtures/gate_manifest.json` do not intersect (control:
`bootstrap/tests/test_scaffold.py` is a key). The new test file is still not a
key, so this revision's edits to it owe no second re-anchor. No node was added or
dropped by this revision.

**Not touched.** `git diff --stat c504fca8..550750fb` over `doctrine/`,
`AGENTS.md`, `templates/modules/`, `docs/`, `scripts/`, `tools/`, `dev/.cairn/`,
`dev/PLANNING.md`, `CHANGELOG.md`, `dimensions/README.md` and both plan templates
is empty (control: the same command over `dimensions/complexity.md` prints a
line). A `grep -E 'Claude|Codex|Anthropic|OpenAI|Gemini|Cursor|LHM|modflow_tools'`
over the 171 added lines of the range prints nothing; a control line holding
`Gemini` is found.

**Plan-specific acceptance commands.**

| Criterion | Method | Result |
|---|---|---|
| SC-CR1: the reviewer's survivors die | the survivors rebuilt from the review's table, run against the test at the base and at the tested commit | at the base **20 survive** (the review's 18, plus a loose list and an indented first bullet of mine); at the tested commit **all 20 are killed** |
| Block and paragraph are the fenced bytes | extracted block and paragraph against the plan's fenced C2 text; the test's literals, collapsed, against the same | equal in both proposal and both plan copies (45 and 7 lines); the example reads "at the same rate, distance and schedule" and "comparable rate" is gone |
| Promise sites are the fenced bytes | the plan's fenced C3 texts against the three shipped files | each occurs once |
| The block is where the test says | the heading once, followed by `## Signals the change is wrong`, in both proposal copies | yes |
| An adopter receives the revised texts | real install from the tested commit into an empty scratch folder; `--summary` and `--dry-run` also run | the installed proposal and plan templates are byte-identical to the shipped source; the dry run wrote nothing |
| The sentence change reaches an existing adopter | install from `531084a1`, fill `documentation-tier-home` in both templates, commit, `upgrade --plan` then `--stage` against a copy of `531084a1` changed only by the new example sentence | the proposal template is "locally-modified (merged clean)"; the staged file holds the block once, the new sentence once, no "comparable rate", the adopter's fill once, no conflict marker |
| Upgrade of the proposal template from the revision's own base | install from `c504fca8`, fill the slots, `upgrade --plan` against `c504fca8` itself, then against the tested tree | **needs-value** in both (see the observation below); the plan template merges clean |

**An observation outside this plan, reported and not fixed.** At the revision's
base, `upgrade --plan` classes the Cairn proposal template as `needs-value`
even when planned against the very tree it was installed from, so an existing
adopter's proposal template cannot advance. The cause is a `{{evidence}}` token
in the template's review skeleton with no recorded value; it was added by
`b5b049d0` (the review-stance-and-lenses plan's second chunk) and is not in this
plan's text. It showed on the first record's date as "merged clean" and no longer
does. This revision neither causes nor fixes it, and the sentence-change probe
above isolates this plan's edit from it. It is the sibling plan's to answer.

**Mutation ledger at the tested commit.** Run by the same throwaway harness (it
refuses to run outside a scratch worktree, checks every mutant really changed the
files, and checks the files are byte-identical after each one). **80 mutants: 74
killed, none survived unexpectedly.** Six pass by design: the old lens phrase
restored beside the check in the README row; one sentence re-wrapped; the plan
paragraph re-wrapped (wrapping is free); the check name written with a capital
(letter case is ignored); the Complex bullet's first-sentence trigger narrowed;
and the I-2 trigger narrowed (the last two are not pinned; the pinned N/A finding
carries the gate). Unmutated controls before and after pass. The set is the first
record's 48, then the reviewer's survivors (S1, S2.0 to S2.4, S5, four P1, seven
P2), my five layout mutants, the promise-site mutants and the two example
mutants. Rows, in order:

```text
PASSED  control (before)
KILLED  m1 block word changed, Cairn copy only
KILLED  m2 block word changed, shipped copy only
KILLED  m3 paragraph word changed, one plan copy
KILLED  m4 paragraph deleted, one plan copy
KILLED  m5.00 block unit deleted from both: '### Independent scientific check'
KILLED  m5.01 block unit deleted from both: '*Gated to a change that touches a scientific ass'
KILLED  m5.02 block unit deleted from both: 'For every other change, one line — "N/A: no scie'
KILLED  m5.03 block unit deleted from both: 'Name **one** check that could show the change is'
KILLED  m5.04 block unit deleted from both: '* **What it compares.** The quantity, the expect'
KILLED  m5.05 block unit deleted from both: 'Say whether the data behind the expected value i'
KILLED  m5.06 block unit deleted from both: 'If the check depends on data that does not exist'
KILLED  m5.07 block unit deleted from both: '* **Why the expectation is independent.** Neithe'
KILLED  m5.08 block unit deleted from both: 'Its basis is one of these:'
KILLED  m5.09 block unit deleted from both: '* an analytical or manufactured solution;'
KILLED  m5.10 block unit deleted from both: '* a conservation law chosen against the error th'
KILLED  m5.11 block unit deleted from both: '* a trusted observation or benchmark;'
KILLED  m5.12 block unit deleted from both: '* an independent implementation, or the saved ou'
KILLED  m5.13 block unit deleted from both: "* a domain expert's expectation, written down be"
KILLED  m5.14 block unit deleted from both: '* **The error it would catch.** The plausible mi'
KILLED  m5.15 block unit deleted from both: 'This is security preflight S2\'s "Can it fail?", '
KILLED  m5.16 block unit deleted from both: 'At implementation, the implementer makes that mi'
KILLED  m5.17 block unit deleted from both: '* **When the check passes by finding nothing.** '
KILLED  m5.18 block unit deleted from both: 'Show the same analysis detecting a known effect '
KILLED  m5.19 block unit deleted from both: 'The failing\n  run above serves as the control wh'
KILLED  m5.20 block unit deleted from both: 'At implementation, the implementer records the c'
KILLED  m5.21 block unit deleted from both: 'For example, an analysis that reports no streamf'
KILLED  m5.22 block unit deleted from both: '**Reviewers.** The proposal reviewer challenges '
KILLED  m5.23 block unit deleted from both: 'The code reviewer verifies the recorded\nfailing '
KILLED  m5.24 block unit deleted from both: 'The Maintainer judges at the Decision whether th'
KILLED  m5.25 block unit deleted from both: 'If no independent basis exists, say so;'
KILLED  m5.26 block unit deleted from both: 'the Maintainer weighs that, and it is not a reas'
KILLED  m6.00 paragraph unit deleted from both: '**An independent scientific check is accepted sc'
KILLED  m6.01 paragraph unit deleted from both: 'A replacement qualifies only if it\nfails under t'
KILLED  m6.02 paragraph unit deleted from both: 'If nothing qualifies, dropping the\ncheck is a sc'
KILLED  m6.03 paragraph unit deleted from both: 'Saying that the result now rests on the implemen'
KILLED  m6.04 paragraph unit deleted from both: 'When the check fails for real during implementat'
KILLED  m7 'qualifies only if' -> 'qualifies if', both plan copies
KILLED  m8 'it becomes' -> 'it may become', both plan copies
KILLED  m9 block heading removed, both proposal copies
KILLED  m10 block heading moved above '**Prospective only.**', both
KILLED  m11 block wrapped in a slot, both proposal copies
KILLED  m12 paragraph moved inside the doc-tooling slot, one plan copy
KILLED  m13 sentence added to one proposal copy
KILLED  d1 'independent scientific check' -> 'review' at dimensions/complexity.md
KILLED  d1 'independent scientific check' -> 'review' at dimensions/README.md
KILLED  d1 'independent scientific check' -> 'review' at bootstrap/BOOTSTRAP.md
KILLED  d2 'review finding' -> 'note' in dimensions/complexity.md
PASSED  d3 old lens phrase restored beside the check, README (expected to pass)
KILLED  S1 the five bases de-indented to top level, both proposal copies
KILLED  S2.0 blank line 1 of 5 removed from the block, both proposal copies
KILLED  S2.1 blank line 2 of 5 removed from the block, both proposal copies
KILLED  S2.2 blank line 3 of 5 removed from the block, both proposal copies
KILLED  S2.3 blank line 4 of 5 removed from the block, both proposal copies
KILLED  S2.4 blank line 5 of 5 removed from the block, both proposal copies
KILLED  S5 one space replaced by a non-breaking space in the block, both copies
KILLED  P1 block moved before '## Scope delta', both proposal copies
KILLED  P1 block moved before '## Assurance path', both proposal copies
KILLED  P1 block moved before '## Review --', both proposal copies
KILLED  P1 block moved before '## Decision --', both proposal copies
KILLED  P2 plan paragraph moved before 'A security-touching plan re-answers', both plan copies
KILLED  P2 plan paragraph moved before '## Source proposal', both plan copies
KILLED  P2 plan paragraph moved before '## Scope', both plan copies
KILLED  P2 plan paragraph moved before '## Scope delta', both plan copies
KILLED  P2 plan paragraph moved before '## Verification', both plan copies
KILLED  P2 plan paragraph moved before '## Dispositions', both plan copies
KILLED  P2 plan paragraph moved before '## Plan review --', both plan copies
KILLED  L1 top-level bullet markers '*' -> '-' for the first bullet, both copies
KILLED  L2 a blank line inserted between two top-level bullets (loose list), both copies
KILLED  L3 first top-level bullet indented by two spaces, both copies
KILLED  L4 plan paragraph split in two by a blank line, both plan copies
KILLED  L5 block heading made an H4, both proposal copies
PASSED  W1 one sentence re-wrapped onto one line, both copies (wrapping is free: expected to pass)
PASSED  W2 plan paragraph re-wrapped (two lines joined), both copies (wrapping is free: expected to pass)
PASSED  D8 'independent scientific check' written 'Independent scientific check' in README (case-insensitive: expected to pass)
KILLED  D10 the finding sentence narrowed back to 'a computed result' in complexity.md
PASSED  D11 the bullet's first-sentence trigger narrowed back to 'a published result' in complexity.md (not pinned: expected to pass)
KILLED  D12 the finding sentence loses the scientific-assumption half of the gate in complexity.md
PASSED  D13 the I-2 trigger loses 'or a result the project publishes or acts on' (not pinned: expected to pass)
KILLED  X1 the positive-control example reverted to 'comparable rate', both proposal copies
KILLED  X2 the positive-control example loses 'distance', both proposal copies
PASSED  control (after)
```

**A check that passes by finding nothing.** None for the plan's own sake (see the
first record). The test's controls are the ledger's.

**Known omissions.**
* **Boundary C is the reviewer's.** The revision is for the same reviewer, or
  another fresh one, to falsify; in particular the third place rule I added
  (before the doc-tooling slot) and the claim that nothing else needs pinning.
* **The reviewer's families D4, D5, D6, D9 and S10 are not re-run.** They are the
  presence-only choices; they still pass, by design.
* **The harness is not committed;** each ledger row names its mutation.
* **The review's upgrade probe with an adopter who edited the block itself** was
  not repeated; the revision changes one sentence and the engine is unchanged.
* **The archive duties** (the caveat on the stor-modflow "yes" and the F2 mode)
  are in the Response and are not yet done; they belong to the archive commit.
* **The first record's omissions** about the gate-manifest re-anchor still hold.

## Verification of the revision -- Claude Sonnet 5.5 -- 2026-10-19

```
Reviewed commit: 550750fb6c45a769077b62500e56d3aef407c57a
Target: the revision range c504fca8..550750fb (86db42ae, e2978e44, 550750fb), the Response 1e4f1e96 and the second Boundary B record c1c92ccc, read against SC-CR1 to SC-CR6 of my code review (5ed51cdf)
Prior findings: SC-CR1 to SC-CR6
```

**Obligation**: Verification of the revision (not a second review round)
**Tier**: Internal
**Bounding**: not owed. The second Boundary B record is a `full` run, and I reproduced it on the tested commit (below). It is the fresh full run my first review said the revision owed.
**Findings**: raised (1 new medium, 1 new low); SC-CR1 to SC-CR5 closed, SC-CR6 closed with a correction
**Verdict**: REVISE -> `revising-code`, for SC-VR1 only. The code and template changes are clean. What is not clean is the C1 exercise, because of what the drafters' briefs (now on file) turn out to say.
**Model**: claude-sonnet-5-5

Distance: a fresh session of the implementer's agent type (Claude Sonnet 5.5), the same reviewer as the code review above. I wrote none of the revision. This is Internal and not External. I did not re-review the whole plan: SC-VR1 comes from material I could not read in the first round (SC-CR5 was the missing briefs), not from a defect the revision introduced. Interpreter for every figure: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13, in detached worktrees of `550750fb`, `c504fca8` and `c1c92ccc` in a fresh folder of my own (removed at the end). `git diff` on this plan file was empty when I claimed it and again before I appended.

### In plain terms

**The fixes hold.** Every layout and place mutant that survived last time (18 of them) is now caught, the two new wording changes are in all the right places byte for byte, the full suite gives the same result the second record states, and I found no new defect in the test, the templates or the promise sentences. The third placement rule the implementer added ("before the doc-tooling slot") is not too tight.

**One thing is not settled, and it is about C1.** The briefs show the two drafters were told to do exactly what question (B) rewards: say the data is unconfirmed and name what they would open. That makes (B) impossible to fail for a draft that follows the brief. So the stor-modflow "yes" tells us nothing about whether the block's own data prompt works, and the exercise did not get its fair chance to fail on stor-modflow. I said in the first review that I "would not call it narrow" and that the draft passed "because the block's own data-status prompt made its author write the doubt". I withdraw both: I could not see the briefs then. The remedy is small and quick: re-draft stor-modflow once with a brief that does not carry the nudge, and score it (SC-VR1).

### The six closures

| Finding | State | Evidence |
|---|---|---|
| SC-CR1 (medium) layout and place | **closed** | 18 of 18 rebuilt survivors killed at `550750fb`; no new defect (below) |
| SC-CR2 (low) expert basis | **closed** as I recommended | No text edit. The F2 wording is an archive duty in the Response, still to be done by the archive commit |
| SC-CR3 (low) control example | **closed** | `550750fb`; the sentence reads "at the same rate, distance and schedule" in both proposal copies, in the test and in the plan's fenced text; "comparable rate" is gone. The Maintainer's question and choice are quoted in the Response (as relayed, the same provenance as his earlier answer) |
| SC-CR4 (low) one trigger | **closed** | `e2978e44`; the three shipped promise texts equal the plan's revised fenced texts, each once; the test lower-cases and pins the new finding sentence |
| SC-CR5 (low) briefs on file | **closed**, and it matters | All three briefs are in the Response; their SHA-256 recompute from the fenced text (2ab39e8e..., 6e1a6eb6..., 43f273d9...). See SC-VR1 |
| SC-CR6 (low) archive caveat | **closed with a correction** | The duty exists, but its suggested wording still credits the block's prompt. SC-VR1 supersedes that sentence |

### SC-CR1 against the tested commit

I rebuilt my harness (my earlier one was removed with its folder) and ran the **real** `pytest` on the **real** files in worktrees at `550750fb`, each mutant restored by `git checkout` and checked clean, each run beside an unmutated control (seven controls, all passing).

| Family | Mutants | Killed | Survived |
|---|---|---|---|
| Delete each sentence or list item of the block (27) and paragraph (5), both copies, first only, second only | 96 | 96 | 0 |
| Delete **each word** of the block (457) and the paragraph (81), both copies | 538 | 538 | 0 |
| Markup and characters (indent, `*` to `-`, zero-width space, Cyrillic `a`, HTML comment, bold removed, heading removed, word appended, block wrapped in a slot); the SC-CR3 sentence put back to "comparable rate", and "distance" dropped from it | 12 | 12 | 0 |
| Promise sites: phrase to `review` at each of three sites; each site reverted to its pre-change text; `review finding` to `note`; finding sentence deleted; trigger narrowed to `a computed result`; the `scientific assumption` half dropped | 10 | 10 | 0 |
| **My first-pass survivors, rebuilt**: S1, S2.0 to S2.4, S5 (non-breaking space), P1 x4, P2 x7 | 18 | **18** | 0 |
| My first-pass survivors that are presence-only by design: S10 (a new paragraph beside the pinned one), D4 (bullet moved to the Simple position), D5, D6 (I-2 text), D9 (old lens phrase beside the check) | 5 | 0 | 5 |
| New probes aimed at the revised rules (below) | 11 | 6 | 5 |
| README capital `I` (case ignored: expected to pass) | 1 | 0 | 1 |

Total: 691 mutants, 680 killed, 11 survived. The 18 rebuilt survivors die with a specific message, for example "a '## ' heading sits between the line starting '**Prospective only.**' and the block", "the paragraph sits under '## Source proposal', not '## Acceptance criteria'", "the block's layout differs from the reviewed text, at layout element 9: expected ('item', 2, '*')". The five by-design survivors are the ones the Response and the test's docstring say are not pinned.

**New probes, and what they say about the revised test.**

* **Killed (6):** nested bullets indented three spaces; a nested marker `*` to `+`; two blank lines where one stood; the plan paragraph duplicated elsewhere (marker repeated); the doc-tooling slot **renamed** in both plan copies; the slot moved **above** the paragraph.
* **Survived (5), none a defect:** a blank line holding three spaces; trailing spaces at a line end; a tab in place of a space inside a line (all three render the same); an H3 heading inserted before the plan paragraph (still under Acceptance criteria); an H3 heading and a line of text inserted between `**Prospective only.**` and the block (same H2). The last two are placements the rule deliberately leaves free, since only `## ` headings bound it. The docstring's phrase "the headings do not bound" is a little loose about H3s; harmless.
* **One cosmetic strictness:** an extra blank line mid-block renders identically and turns the test red. A false red that costs one deleted blank line is acceptable; I note it so nobody is surprised.

**The third placement rule is not too tight.** The question was whether a later slot rename would turn the test red for no good reason. A rename does turn it red, with "missing marker: no line opening the 'acceptance-doc-tooling' slot", and the fix is one constant. But the rename is not a cosmetic event: the merge engine keys adopters' filled slots by name (`cairn:slot NAME` pairs; `bootstrap/UPGRADE.md` says slots are adopter-owned), so renaming a slot is an install-contract change and a test that notices it is doing work. The rule asks only "before the slot's opening", not adjacency, so inserting text or another paragraph before the slot passes. It is the plan's own C2 criterion made executable. A rename-proof form (no slot opening between `## Acceptance criteria` and the paragraph) would kill the same P2 mutant, but it would turn red on any new slot placed earlier in that section, which is the same cost with less information. Keep the rule as written. The test also passes at `c1c92ccc` (the current head of this plan's history, carrying the sibling plan's template and dimensions commits so far), so the sibling work has not tripped it.

### The second Boundary B record, checked against `550750fb`

* **Right bytes.** The range changes six paths: `bootstrap/BOOTSTRAP.md`, `dimensions/complexity.md`, the two proposal templates, the test and this plan. `git diff --stat` over `doctrine`, `AGENTS.md`, `templates/modules`, `docs`, `scripts`, `tools`, `dev/.cairn`, `dev/PLANNING.md`, `CHANGELOG.md`, `dimensions/README.md`, both plan templates, `bootstrap/_scaffold`, `bootstrap/tests/fixtures` and `bootstrap/verify_integrity.py` is empty. The range's paths and the 183 `frozen_files` keys do not intersect (control: `bootstrap/tests/test_scaffold.py` is a key; the new test is still not one). A vendor-name grep over the 160 added lines in the changed template, dimensions, bootstrap and test files prints nothing; the control line is found.
* **4432 passed, 2 failed: reproduced.** `CAIRN_FULL_SUITE=1 ... --quality-gate-shuffle-seed=0 -rsfExX`, a fresh worktree of `550750fb`, clean before and after: **2 failed, 4432 passed, 3 warnings in 879.7 s** (the record's 793.0 s; mine ran alongside about 700 mutant runs), 0 skipped, 0 xfail, 0 xpass. The two failures are the same two AST tests.
* **The same two at the base.** At `c504fca8` the AST file gives 2 failed, 28 passed, with the same text once worktree paths are removed. My run's CHANGED list names the same five symbols with the same baseline and current hashes as both records.
* **No node added or dropped.** `pytest --collect-only` lists 4434 nodes at both commits (4432 + 2), identical sets.
* **Gates and contract.** Neutrality `fail=0 info=56` and redundancy `fail=0 info=0`, output identical to the base's. `scaffold.py --manifest` byte-identical (98 lines). `verify_integrity.py --target .` output identical (23 lines). `check_cairn.py` reports one issue at both commits, in another session's review file (a path under `tools/__pycache__` that exists only in a tree that has run Python), none in a file this revision edits, as the record says.
* **The block and the paragraph are the plan's fenced bytes.** The revised fenced C2 block occurs once in each proposal copy and the paragraph once in each plan copy.

### C1 and the briefs

The briefs are what I asked for in SC-CR5, and they are better evidence than I had. What they show:

* **Blindness is as the record said.** Each drafter was told to read exactly two named files, nothing else, no commands, no web. No brief names a path into the LHM repository, an error statement or a review. The assemble drafter's brief carries the part-naming sentence word for word.
* **The briefs also tell the drafter how to handle data, in terms the block does not use.** Both drafter briefs say: if you would want to check something, the data behind it for example, you cannot; "Say so in the section, as its instructions ask, and name what you would open to confirm it." The block's instruction is "Say whether the data behind the expected value is in hand and has been checked. If the check depends on data that does not exist yet, say so." It does not ask the author to name what to open. The brief attributes that to the block ("as its instructions ask") when the block does not carry it.
* **That sentence is, nearly word for word, the pass branch of (B).** The scorer's rubric accepts a draft that says the data is "not confirmed, and names what would be opened". A draft that follows the brief therefore passes (B) by construction. The only way to fail (B) was to state that the data was in hand, against the brief's own instruction.
* **The plan designed (B) to prevent exactly this.** C1 says that without (B), "(A) is 'yes' for any draft that repeats the original compare-with-saved-output check, and the exercise could not fail on stor-modflow, the very ritual it exists to detect." With the brief as written, it could not fail on stor-modflow after all. The stor-modflow draft's "Data in hand" heading over text that says nothing was checked passed (B) on the strength of text that follows the brief.

**Does it change my view? Yes, and more than the implementer's wording says.** The Response says the draft's pass "owes part of its form to the brief". I would say the (B) pass owes its whole form to it: the exercise cannot tell the block's data prompt from the brief's. So:

* The stor-modflow "yes" is now (A) alone, and (A) is "yes" only on the condition that the reference array had existed, which it never did. It says nothing about the block's data-status prompt, for or against.
* The Response's suggested archive sentence ("the block's data-status prompt, with that help, made a blind author flag the false data claim. It is weak positive evidence for that prompt") credits the prompt. On this run it is no evidence either way. Also, the draft flagged the variable's existence as *unchecked*, not as *false*.
* The assemble "no" is untouched by this (the same nudge could only have helped it).
* The stop rule was applied as written to the record it was given: one yes, one no, proceed. The record is not a fair run of the test the plan designed.

I do not read this as the implementer's fault: the disclosure was made unprompted and is precise. It is what I would have asked for.

### Findings

#### SC-VR1 -- Medium -- The drafters' briefs handed over the pass condition of question (B), so the stor-modflow "yes" is not a fair result

**Plain.** The go/no-go exercise exists to catch a block that is a ritual. Its one real chance to catch it on stor-modflow was whether the draft admitted what it had not checked. The briefs told the drafters to admit it and name the file. The "yes" proves the drafter could follow an instruction, not that the block works.

**Precision.** Evidence is the two drafter briefs (both carry the sentence), the block text, the scorer's (B) branch and C1's own paragraph on why (B) exists, all quoted above. C1's red condition for the blind draft includes "the brief holds anything else". The record already softened "pasted into the brief, no repository access" to a read tool and an instruction, and disclosed it. A sentence that hands over the rubric's pass condition is the one addition that changes the result. Plan C1 is a Decision-relevant gate ("stop if neither"), so its result should not rest on a nudge. Nothing is pushed, so the cost of getting this right is a re-draft, not a revert.

**Closes when** the stor-modflow draft is redone once, under C1's rules, as a dated sub-section appended under the `## Retroactive application` record:
1. A fresh drafter that is none of: the implementer, me, either of the first two drafters, or the scorer, given the same two inputs (checked against the recorded SHA-256 of the wording and of the proposal as opened), and a brief identical to the first **except** that the last rule reads only "If the instructions ask for something you cannot do from these two texts, say so in the section." The brief must not say "name", "open" or "confirm" about data, and must not say what the block's instructions ask.
2. The same scorer brief to a fresh scorer, with the same two error statements.
3. Both briefs (SHA-256 each), the draft and the score, appended verbatim. The first stor-modflow draft and score stay on file, labelled as made under a brief that helped.
4. The stop rule applied to {assemble part A: no, stor-modflow re-run}. If the re-run is **yes** on (A) and (B), C1 stands; the archive sentence then says the "yes" came from a re-run after the first brief was found to help. If it is **no**, both plans are no and the accepted rule applies as written: the block is judged ritual, the implementer writes the Waiting line, and the Maintainer decides what happens to the committed, unpushed C2 to C4.
5. The Response's suggested archive sentence is replaced, after the re-run, by one that credits the prompt only if the re-run does.

A single re-draft is a sample of one, as the first was. The plan accepted that ("a go/no-go gate, not a measurement"), and the point is to run the gate it designed, not a better one.

#### SC-VR2 -- Low -- The `needs-value` regression has no live home, and it stands between this plan's block and existing adopters

**Plain.** The second record reports, and does not fix, that an existing adopter's proposal template cannot advance: the upgrade plan classes it `needs-value`. I reproduced it: an install from `c504fca8` (`solo-greenfield`), then `upgrade --plan` against `550750fb`, and again against `c1c92ccc`, lists `dev/proposals/_template.md` as `needs-value`. The cause is the new `{{evidence}}` tokens at lines 335 and 336 of the shipped proposal template at `550750fb`, from the sibling plan's second chunk. Until that is answered, the block reaches a new install but not an existing one.

**Precision.** It is not this plan's defect, and this plan's own probe isolates its sentence from it. But the plan template's rule is that nothing still to be done may have an archived file as its only home. Searching `dev/plans/review-stance-and-lenses.md` and `dev/PLANNING.md` for `needs-value` and `{{evidence}}` finds nothing; the only home is this plan's second record.

**Closes when** the item is named in the sibling plan (which owns the template change) or on a board row, before this plan archives, saying that an existing adopter's proposal template stops at `needs-value` and that this plan's block is among what is held back. This does not block the plan.

### Observations (no finding)

* **Operative cells were revised in place after execution began.** The Response edited the plan's fenced wording and the C3 criterion in place (the SC-CR3 example, the SC-CR4 texts) and listed each change. The plan template says changes append once execution of a chunk begins. The text as reviewed is recoverable at `531084a1` and `2764eccd`, and the list is complete, so I do not ask for a revert. One side effect: the cell that describes the test's groups (a) to (d) still reads as the old spec; the layout and place rules live in the test's docstring and the Response.
* **The Response's suggested archive sentence and the F2 wording** (SC-CR2) are duties for the archive commit and are not done yet; the second record says so.

### What I did not cover

* I did not run the re-draft or the re-score myself. That is the implementer's chunk, run by agents that are neither the implementer nor me; SC-VR1 gives the recipe.
* I did not re-read the whole plan or re-run last round's upgrade table for an adopter who edited the block itself. The revision changes one sentence of the block and no engine code, and my `needs-value` probe used the installed proposal template as it stands.
* I did not run the base's full suite; I checked its AST file, collection and gates.
* The Maintainer's chat answer on the control example is as the Response quotes it; I cannot see the chat.
* Last round's other omissions still hold: rendering was measured for the survivors I named, not for every whitespace variant, and the scientific content beyond the positive-control bullet is the Maintainer's.

## Retroactive application, the stor-modflow draft to be redone -- Claude Sonnet 5.5 (implementer) -- 2026-10-19

This continues the C1 record under `## Retroactive application` above, which is
not edited. It is appended here because the sections after that record have been
written since.

**In plain terms.** The verification of the revision found a flaw in how C1 was
run, and the coordinating session is fixing it by running the stor-modflow draft
again. The flaw: the drafters' briefs told them to say what they could not check
and to name what they would open to confirm it. That is the very thing question
(B) rewards. So the stor-modflow "yes" was not a fair test of the block, and I set
it aside. This section records the new brief and why. **It is written before the
new draft exists.** Nothing is scored. C1's outcome is therefore **open** until
the new draft is scored, and I will not treat it as settled. If the new draft
says yes, C1 stands; if it says no, both plans are no and the plan stops (see the
stop rule below).

### Why the first stor-modflow result is set aside

* **What the briefs did.** The first stor-modflow drafter's brief (on file in the
  Response, SHA-256 `2ab39e8e…0a7a`) said: if you would want to check
  something, the data behind it for example, you cannot; "Say so in the section,
  as its instructions ask, and name what you would open to confirm it." The
  block's own instruction is "Say whether the data behind the expected value is
  in hand and has been checked. If the check depends on data that does not exist
  yet, say so." It does not ask for a name or a file to open, and the brief
  credited that sentence to the block.
* **Why it decides the result.** The scorer's rubric passes (B) for a draft that
  says the data is not confirmed **and names what would be opened**. A drafter
  who followed the brief therefore passed (B) by construction; the only way to
  fail was to claim the data was in hand against the brief's own instruction.
  C1 added (B) so that stor-modflow could fail; with that brief it could not.
* **What I said before, corrected.** The Response said the pass "owes part of its
  form to the brief". The verification reads it as the whole form, and I agree.
  With the brief as written, the exercise cannot tell the block's data prompt from
  the brief's. The stor-modflow "yes" is then (A) alone, and (A) is "yes" only on
  the condition that the reference array had existed, which it never did. It is no
  evidence about the block's data-status prompt, for or against.
* **What stays on file.** The first stor-modflow draft, its score, the verdicts
  and the stop-rule application above are kept exactly as written, and are
  labelled here as **made under a brief that helped**. The assemble part A draft,
  its brief and its "no" are untouched: the same nudge could only have helped it.
* **The stop rule, as applied then.** It was applied correctly to the record it
  was given (one yes, one no). That record was not a fair run of the test the plan
  designed. This section re-opens that question; it does not change the earlier
  text.

### The re-run brief, on file before the draft exists

Sent by the coordinating session to a fresh drafter. The coordinating session's
account is that the drafter is fresh and that the inputs are the same as the first
run's; I have not seen the drafter. The brief is below verbatim, with no fence of
its own (15 lines). SHA-256:
`d2b91c209f2615fd512ca325f91ac6ef4dea6095120f81bff137383954f51944`.

```text
You are the author of a scientific-software proposal, filling in one section of it. This is a blind exercise. **You may read exactly two files, and nothing else.** Read them with the Read tool:

1. `/private/tmp/claude-501/-Users-kendal30-Code-cairn/79ada448-b159-4255-b0ea-444b74328be1/scratchpad/c1-inputs/wording-independent-scientific-check-block.md`: the instructions for a section called "Independent scientific check".
2. `/private/tmp/claude-501/-Users-kendal30-Code-cairn/79ada448-b159-4255-b0ea-444b74328be1/scratchpad/c1-inputs/stor-modflow-proposal-as-opened.md`: your proposal, exactly as you opened it.

**Rules:**
- Do not read, search or list any other file or directory.
- Do not run commands.
- Do not use the web.
- Work only from those two texts.
- If the instructions ask for something you cannot do from these two texts, say so in the section.

**Task.** Following the section's instructions exactly, write the "Independent scientific check" section for this proposal, as its author would at the moment the proposal was opened. Be concrete: the quantity, the expected value and tolerance with its source, whether the data behind it is in hand, why the expectation is independent, the plausible mistake under which the check would fail, and the positive-control clause if your check passes by finding nothing. If you judge that no independent basis exists, say so plainly. Don't invent one.

**Reply** with only the filled section, in Markdown, starting with its `### Independent scientific check` heading. Add no commentary before or after it.
```

* **Against the first brief, one rule differs.** `diff` of the two files shows a
  single changed line, the last rule, which read "If you would want to check
  something, the data behind it for example, you cannot. Say so in the section, as
  its instructions ask, and name what you would open to confirm it." and now
  reads "If the instructions ask for something you cannot do from these two texts,
  say so in the section." Every other line, the two file paths included, is the
  same.
* **It carries none of the nudge.** Searched case-insensitively for `name`,
  `open` and `confirm`: the first brief holds `name` and `confirm` once each and
  `open` four times; the re-run holds `name` and `confirm` not at all, and `open`
  only in "exactly as you opened it" and "at the moment the proposal was opened",
  which are about the proposal. The task paragraph still asks "whether the data
  behind it is in hand", as in the first brief and as the block's own wording
  does; that is the data-status prompt under test and was left in on purpose.
* **The inputs are the same bytes.** I recomputed their SHA-256 today: the wording
  `327d0b175cafb40e43dc421a0894403edfa4e44854e4e1f1871200fa55c6f947` and the
  stor-modflow proposal as opened
  `6971f5191097e17df6940dfde5a424921aa7f062b247770d111afb8e4e4cc46b`, as recorded
  in the C1 inputs above.
* **Next, by the coordinating session's plan.** The draft goes into this record
  verbatim before any scoring; a fresh scorer then gets the same scorer brief and
  the same two error statements; the result is appended here; and the stop rule is
  applied to {assemble part A: no, stor-modflow re-run}. **Yes** on both (A) and
  (B): C1 stands, and the archive sentence says the yes came from a re-run after
  the first brief was found to help. **No**: both plans are no, the block is
  judged ritual, I write `**Waiting on Maintainer**: block judged ritual; plan
  stopped` beside Status and stop, and the Maintainer decides what happens to C2
  to C4, which are committed and not pushed.

### The suggested archive wording, corrected

The Response's first archive duty suggested a sentence that said the block's
data-status prompt, "with that help", made a blind author flag the false data
claim, and that this was weak positive evidence for the prompt. **That sentence is
withdrawn.** It credited the block for a result the brief produced. The
replacement below does not credit the prompt for the first "yes". It is interim:
its last sentence is completed from the re-run's record once the re-run is scored.

> C1 ran on two past LHM plans. Assemble part A said no: its draft was a good
> check for the change the proposal described, aimed at a different risk than the
> one that later bit (the fill for uncovered land-use cells), which the proposal
> as opened never mentioned. Stor-modflow's first draft said yes, and that result
> was set aside: the drafters' briefs had told them to name what they would open
> to confirm any data they could not check, which is the pass condition of the
> data-status question, so the yes showed only that a drafter can follow a brief.
> It is no evidence about the block's data-status prompt, for or against. The
> stor-modflow draft was redone once with a brief that did not carry that
> sentence. *(Complete from the re-run's record: its verdict on (A) alone and
> combined, and the stop rule's result. If it is yes, add: the yes came from a
> re-run after the first brief was found to help; it is weak positive evidence
> for the data-status prompt and none yet for the independent-basis half, and it
> is not evidence that the block yields a check that catches the priming error.
> If it is no, the block is judged ritual and this archive wording is moot.)*

The second archive duty (name the author-as-expert mode under falsifier F2 on the
revisit row) is unchanged and still to do at archive.

### The upgrade regression is fixed elsewhere

The second Boundary B record reported that an existing adopter's proposal template
stopped at `needs-value` on upgrade, because of `{{evidence}}` tokens added by the
review-stance-and-lenses plan's second chunk. The verification asked for it to
have a live home. It has been fixed by that plan at `5c77c11b` ("no one-word
placeholder the engine cannot fill in the proposal template"): the three tokens
became `<evidence>`, and guard tests scan every shipped template and Cairn's
authoring copies against the engine's own token rules. I checked it today: an
install from `c504fca8`, planned against the current head `8ccb8836`, lists no
`needs-value` file, and the new test and `test_profile_grammar` pass there (46
passed). This plan's block therefore reaches existing adopters again, and the item
needs no further home.

### The stor-modflow re-draft, verbatim

The re-run brief above was committed (`67529e35`) before this draft existed. The
draft is in. **Nothing is scored.** A fresh scorer, given the same scorer brief,
scores it next; its output, the verdicts on (A) alone and combined, and the stop
rule's result are appended below in a later commit.

**The facts** (the coordinating session's account; I did not see the briefing):
* The drafter is a fresh Sonnet agent: not the implementer, not the first
  drafters, not any scorer.
* It was given the same two input files as the first stor-modflow run (the
  wording and the proposal as opened; their SHA-256 are recomputed above and equal
  the recorded ones) and the re-run brief recorded above.
* It made 3 tool calls: the two reads and the hand-back. As before, blindness
  rests on the instruction and on that observed count, not on a sandbox.
* The coordinating session extracted the draft byte for byte from the drafter's
  hand-back into a file of 39 lines, SHA-256
  `bef1a783ce3c2889fc7f1e4bb8c996e4edfffd881ad71084b381121545af951b`. I
  recomputed the hash and the line count; they match.
* The text between the fences below is that file. It contains no fence of its
  own, and its headings are inside the fence and are not headings of this plan.
* This is the neutral-brief draft. The first stor-modflow draft (made under the
  brief that helped) stays on file above, labelled as such.

```text
### Independent scientific check

This change touches a unit convention (length and time units taken from the model's DIS file), a parameter source (`vk`, and `Sy` and `Ss`), and a result the project publishes (the storage product). The check applies. I name one check below. It covers the unsaturated-zone half of the proposal only, and I say what it leaves uncovered.

* **What it compares.**
  * **Quantity.** Unsaturated-zone water as recomputed by the Python code after §5 (the PERC percolation grids passed through the delay, with `vk` from layer 1). It is compared with the model's own `unsatStorage` in `OUTS_newBC_v5-2000-2025_20260219.mat`, for run `newBC/v5-2000-2025`.
  * **How.** Compare per surface cell and per month, and also as a domain total. A domain total alone could hide cell-level errors that cancel.
  * **Expected value.** The `unsatStorage` values in OUTS, after any unit or orientation conversion is checked.
  * **Tolerance.** I have none, and no source for one. The proposal's only threshold is "does not shrink materially." That is relative to the current implementation, which has never completed a build because it needs ~78 GB, so that baseline may not exist. It is not a tolerance either way.
    * The one floor I can name is the rounding left by PERC's integer quantization and OUTS's stored precision. Those numbers are in the files, not in either text I was given.
    * Anything above that floor is a judgment about the science. I ask the Maintainer to write the tolerance down before the first comparison is seen, and I won't supply a number here.
  * **Data in hand, and checked?** In hand but not checked.
    * The proposal gives OUTS's size (137 MB). It takes "carries `unsatStorage`" from the accepted proposal's §3.
    * Nothing in this proposal records the variable's shape, units, time axis, or orientation, or that this OUTS comes from the same model state as the OUTF and PERC files. The recon table has no OUTS row.
    * This run has already hit inverted dimensions and a MAT v7.3 reader that never fired. An integration assertion on OUTS's shape and orientation comes before any residual is read.

* **Why the expectation is independent.** The basis is the saved output of the model the code reads. MATLAB's `unsaturated_zone_module.m` wrote `unsatStorage`; neither the proposed Python nor a test from the same understanding computes it. It is independent of the port, not of the model's physics.
  * If the MATLAB module's physics is wrong, this check still passes.
  * Both sides read the same PERC and UPW files, so a wrong input file would not be caught either.
  * It also won't settle whether `vka` is a conductivity or a ratio, if the module and the port read it the same way. It tests whether the port reproduces the model, not whether the model is right about the world. I know of no independent unsaturated-zone observation behind this run.

* **The error it would catch.** The check fails if the recomputation does not reproduce the model's own unsaturated storage. The plausible mistakes, all in §5 and the units work in §2, are:
  * The delay uses the hardcoded 1-day stress-period length instead of the period's real length (`perlen` is 1, 5 or 7).
  * `vk` is a scalar mean over all three layers, inactive cells included, instead of layer 1 regridded.
  * A length-unit slip, for example feet read as metres.

  At implementation the implementer makes the first mistake on purpose, then each of the others, and records the failing residual for each. I expect the hardcoded-1.0 mistake to matter a lot:
  * The recon shows 9 497 daily grids over 1 358 stress periods, about 7 days per period on average, so 1.0 is probably wrong for most of the run.
  * I have not seen how `perlen` enters the delay, so that is an expectation to be measured, not a result.

* **When the check passes by finding nothing.** It does: a small residual means "no difference found." So it is evidence only if the same comparison shows a known error.
  * The deliberate mistakes above are the control, if they push the residual out of tolerance. The implementer records the correct code's residual and each injected mistake's residual side by side, per cell and as a domain total.
  * If a mistake stays inside tolerance on the domain total but not per cell, the per-cell comparison is the check, and that is recorded.
  * If a mistake stays inside tolerance on both, the check cannot see that mistake, and the record says so.

* **What this check does not cover.** I identify no independent basis for the groundwater-side changes (§3 overhang fix, §4 head-to-month pairing, heads-to-storage-change).
  * Their invariants in the Evidence section are geometry or arithmetic over objects built by the same understanding, so they test the code, not the world.
  * A budget-closure check is not available: the run saves no storage term (recon, Alternative 3), and a closed budget would not catch a wrong input anyway.
  * A domain expert could write down the expected range of the groundwater storage anomaly before the build completes. I have no such value and do not supply one. The Maintainer weighs this gap at the Decision.
```

### The re-score, verbatim

**The scorer** (the coordinating session's account; I did not see the briefing).
A fresh Sonnet agent: not the implementer, not any drafter, and not the first
scorer. Its brief was identical to the first scorer's except for the folder it
reads, which held the re-run draft, byte-identical copies of the assemble draft
and both error statements (each copy's SHA-256 equal to its original's). It made
5 tool calls: four reads and the hand-back. As before, blindness rests on the
instruction and on that observed count, not on a sandbox. The coordinating session
extracted its output byte for byte (11 lines, SHA-256
`c735e8d62813edfc6d2523a9728e697c21fd80b673a2e54a121aa76678cb1147`); I
recomputed the hash and line count and they match. The text between the fences is
that output, with no fence of its own.

```text
#### Draft 1 (stor-modflow)
- **(A):** yes. The error is an unprimed percolation stack, with no counterpart to the model's 365-day warm-up and no RAMP shift. That offsets the domain-mean unsaturated anomaly by about 14.9 kg m-2. The check compares the recomputed storage per cell and per month, and as a domain total, against the model's own `unsatStorage`, which does include the warm-up. A uniform offset of that size is far above the rounding floor the draft names, so the comparison would fail with the error in place. The check is also not tied to the draft's three listed "plausible mistakes", which do not include the warm-up. Quoted: "The check fails if the recomputation does not reproduce the model's own unsaturated storage."
- **(B):** no. The error statement says `unsatStorage` "had never been saved" in the OUTS file (2.80 GB, over the 2 GB limit of the file format used), and the Internal plan review found this. The draft's data claim is therefore false. The draft repeats it as "In hand but not checked." It does name the OUTS file and promises an assertion on its shape and orientation before any residual is read. But it still asserts the array is in hand, and it takes "carries `unsatStorage`" from the accepted proposal's §3 without opening anything. Under the stated rule, repeating a false claim as "in hand" fails (B). No sentence qualifies.
- **Verdict:** no.
- **Basis (not scored):** the saved output of the model the code reads (the MATLAB module's `unsatStorage` in OUTS). It is independent of the Python port, as the draft says, but not of the model's physics or input files. The array it relies on never existed.

#### Draft 2 (assemble-part-a)
- **(A):** no. The error is in the land-use weights. When no model cell counts as partly covered, the fill for uncovered cells is 0/0, so the build wrote NaN land-use weights. It appeared with a patched partial threshold on Cedar Creek. The check never touches that path. It runs `cell_statistics` on a synthetic continuous linear field (11 × 11 fine cells, 4 × 4 coarse cells, aligned) and looks for a half-cell row shift of about 1.5 value units. There are no land-use categories, no partial-coverage threshold and no uncovered-cell fill. The partial-coverage threshold is never varied, so the NaN fill is never reached. The check would pass with the error in place. No sentence qualifies.
- **(B):** yes. The data claim is not contradicted by the error statement. The check needs no external data, and the draft says what is unopened and that the plan opens it first. Quoted: "It needs no external data. The expected values are worked out by hand from the grid numbers and committed in the test before the helper is run against it." and "I have not opened `helper/zonal.py` or its tests under `tests/helper/`." and "The plan opens those first."
- **Verdict:** no. (B) is satisfied, but (A) fails.
- **Basis (not scored):** an analytical solution (the mean of a linear field over a rectangle equals its value at the centroid). It is independent of the code under review. The draft names one shared assumption, that row 0 is the northern edge, and says the fixture states that convention itself.
```

### The verdicts, and the stop rule applied as the plan states it

| Plan | (A) alone: a check that fails under the error | (B): could it have been run | Combined verdict |
|---|---|---|---|
| assemble part A | no | yes | **no** |
| stor-modflow, first draft (set aside: made under a brief that helped) | yes | yes, narrowly | yes, set aside |
| stor-modflow, re-run (neutral brief) | **yes** | **no** | **no** |

The first scorer's rows are as recorded above. The re-run scorer quotes no
sentence for a "yes" on (B), and none is owed for a "no". Its "yes" on (A) quotes
"The check fails if the recomputation does not reproduce the model's own
unsaturated storage.", which is in the re-draft word for word.

**The stop rule, as C1 states it.** "If both verdicts are **no**, the block is
judged ritual: the plan stops, and nothing in C2 to C4 is committed. If at least
one is **yes**, the plan proceeds." The pair to which it is now applied is
{assemble part A: no, stor-modflow re-run: no}. Both are no. **The block is judged
ritual under the plan's reading, and the plan stops.** The stop was neither
softened to a warning nor hardened to "either".

**What that leaves, said plainly.** The rule says nothing in C2 to C4 is
committed. They are committed, because the earlier verdict said continue, and they
are not pushed. I have reverted nothing and started no archive. What happens to
those commits is the Maintainer's. The interim archive wording above is moot
unless he overrules the reading.

### Two facts for the Maintainer, recorded and not argued

1. **(A) alone.** The stor-modflow re-run has (A) **yes**. The accepted
   proposal's stop test asked whether an author following the block "would have
   named a check that fails under the error later found". That is (A). The plan
   added (B) by interpretation, so that stor-modflow could fail by repeating the
   saved-output check on data that was not there, and listed that reading under
   *Scope delta* as an addition "so the code reviewer or the Maintainer can
   overrule it". On (A) alone the re-run is yes, and C1 would continue.
2. **The two scorers read nearly the same kind of data statement differently.**
   The first scorer gave (B) **yes** to the first draft's "This proposal's recon
   table has no OUTS row, so nobody has recorded opening it." and its "To confirm.
   Open OUTS...". The re-run scorer gave (B) **no** to the re-draft's "In hand but
   not checked.", because of the words "in hand". The re-draft also names the OUTS
   file, says nothing in the proposal records the variable's shape, units, time
   axis or orientation, and requires "An integration assertion on OUTS's shape and
   orientation" before any residual is read. The two scorers had the same brief.
   The first draft was written under a drafter brief that had pointed at the pass
   condition; the re-draft was written under one that had not.

One drafter and one scorer per plan, two plans; the plan called this a go/no-go
gate and not a measurement of how often the block helps.

### What the Maintainer decides

* Whether the block is judged ritual on the plan's reading ((A) and (B)
  together), which stops the plan, and what then happens to C2 to C4: committed,
  not pushed, with their tests and records.
* Or whether the (B) reading is overruled, in which case (A) alone applies and
  C1 would continue.

I have taken neither step. The Status line is unchanged. The Waiting line, as C1
prescribes, is in the header block beside Status.

## Decision on the C1 outcome -- the Maintainer's instruction, scribed by Claude Sonnet 5.5 (implementer) -- 2026-10-19

**In plain terms.** The re-score said no, so by the plan's stop rule the block
was judged ritual and the plan stopped. The Maintainer has decided otherwise: the
go/no-go exercise is not data to package. It is evidence for one change to the
template, and the plan goes on with that change. The block is kept and sharpened,
not dropped. This section records his words and what they do; the change itself,
the evidence summary and the archive wording follow in their own commits.

**Provenance.** The chat is not on file in this repository. The words below are
the coordinating session's record of what the Maintainer wrote, relayed to me on
2026-10-19, as with his earlier answers recorded in this plan.

**His words, verbatim (chat, 2026-10-19):**

> "This doesn't really seem worth packaging data for, unless it will be used in the future"
>
> "But rather evidence for a change to Cairn"

**The coordinating session's confirming question, verbatim:**

> "Here's my reading of what you said: the go/no-go test isn't data to keep or ship. It's evidence, and what it shows is that the template's data prompt should say what my brief said. So: change the template sentence (option 2), and record C1 in the plan as the evidence for that change, as a short summary (verdicts, what each draft got right, the hashes), not more verbatim material. Is that right?"

**His choice:** "Yes, do that". That option read:

> "The data prompt becomes 'Say whether you have opened the data and confirmed it holds what the check needs; if not, name what you would open to confirm it.' C1 is recorded as the evidence for that change. The code reviewer re-checks the one sentence and its test, and then the plan archives."

**What this does.**
* **It supersedes the stop rule's outcome.** C1's rule said that with both plans
  no the block is judged ritual and the plan stops. By the Maintainer's
  instruction the block is kept and sharpened instead. The C1 record above stands
  as written; this section overrides only its consequence.
* **The Waiting line is deleted.** He has answered.
* **C2 to C4 stay as committed,** unpushed. Nothing is reverted.
* **One sentence of the block's data prompt changes,** in both proposal
  templates, the plan's fixed wording and the test's pinned text, and C1 is
  recorded as the evidence for it.
* **Scope delta.** This is an **addition** to the accepted scope, made at the
  Maintainer's instruction. It removes nothing, so it owes no *disposition*.
* **After it,** the code reviewer re-checks only that sentence and its test, and
  the plan archives. The archive duties recorded in the Response, as corrected in
  the sections that follow, still hold.
