# Plan: independent scientific check — one check per scientific change, shown able to fail

**Source proposal**: `dev/proposals/archive/2026-10-17-claude-independent-scientific-check.md`
**Status**: ready-to-implement
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
* **When the check passes by finding nothing.** A check that passes on "no
  change", "no difference" or "no effect" is evidence only if it could have
  found a change. Show the same analysis detecting a known effect of the size
  that matters (a positive control), or say plainly that it cannot. The failing
  run above serves as the control when the mistake it makes produces an effect
  of that size. At implementation, the implementer records the control with the
  failing run. For example, an analysis that reports no streamflow depletion
  from a pumping well first recovers the depletion of a synthetic well of
  comparable rate.

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

`bootstrap/BOOTSTRAP.md`, I-2. The three lines beginning "Fill the template."
end "... those drive the legacy-agent and / scientific-trust-reviewer decisions
downstream. If uncertain," and become four:

```text
Fill the template. Do not skimp on the scientific-surface and
documentation-trust sections — those drive the legacy-agent decision,
and show which changes touch a scientific assumption and so need the
proposal template's independent scientific check. If uncertain,
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
  contains the sentence `an unexplained "N/A" on a change that touches a computed
  result is a review finding`. **Presence only, never absence**, so the later plan
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
  sentence about an unexplained "N/A" on a change that touches a computed result
  being a review finding, once, in the Complex position, and the "gated on the
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
