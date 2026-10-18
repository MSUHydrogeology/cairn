# Plan: review stance and lenses — one review at every stage, and the lenses in every install

**Source proposal**: `dev/proposals/archive/2026-10-18-claude-external-is-a-maintainer-stance.md` (accepted `58f30d6c`) and `dev/proposals/archive/2026-10-18-claude-review-lenses-for-every-install.md` (accepted `fbf664f0`)
**Status**: revising-plan
**Plan review**: required(Internal + Internal Security Review)
**Assurance path**: high-assurance — inherited: the change edits `doctrine/`, the governing `AGENTS.md` every adopter receives, the authoring templates and a framework anchor.
**Opened**: 2026-10-18

Proposed paths:
- `bootstrap/tests/test_review_stance_in_shipped_files.py`
- `bootstrap/tests/test_review_sweep_ships.py`

## In brief

**Two accepted changes, built as one plan.**

1. **No agent chooses a kind of review.** Today "External" means a review by a
   different kind of AI or by a person. Agents kept picking that label for
   themselves, and the Maintainer has had to overrule it five times in eight
   weeks. After this plan there is **one review at every stage**: a fresh
   reviewer who did not write the work, on the work's side, who makes it
   better by asking the questions that matter at that stage.
   * *Proposal*: should this exist as framed, and is there a better design?
   * *Plan*: does it deliver what the Decision settled, and is there a simpler path?
   * *Code*: does it do what it claims, and can I break it so it gets fixed?

   Every review writes its answers down, each with the file, test, line or
   command behind it, and says what it did not cover. There is no quota of
   findings. "External" keeps **one** meaning: *the Maintainer asked for more
   distance on one named piece of work, and the record quotes their words.* An
   agent never picks it, requires it or recommends it.
2. **Every install gets the review checklist.** The nine review **lenses**
   (claims, tests, completeness, silent failure, and so on), the rule that a
   lens names what backs it ("checked" alone is an incomplete review), the
   line that ends a review by saying what it did not cover, and the
   **falsification ledger** (the record a clean code review must show) sit
   today in a module that solo and small teams never receive. After this plan
   they sit in the review-loop document every install receives, with a short
   pointer in `AGENTS.md`.

**Why one plan.** Both changes rewrite the same paragraphs. Writing the lens
text once, in its final place, means no test pins wording that a later step
moves. The Maintainer chose this (the lenses proposal's Question 5).

**What it touches.** 49 prose files (the two `AGENTS.md` copies, the review-loop
document, four authoring templates, three modules, three onboarding presets,
nine doctrine files, four `dimensions/` files, the README and its figure, eight
docs pages and two bootstrap pages), two new tests, one old test retired. **No
engine file changes**, so there is no AST impact and the published install
manifest does not move.

**Order of work.** Shipped text first, because adopters receive it and never
receive `doctrine/`: the two carrier documents (C1), the authoring templates
(C2), the roster, capability floors and remaining shipped text (C3). Then the
doctrine that stands behind them (C4), the dimensions (C5), the README, figure
and docs (C6). Last the things that retire something: the old pin and the
module's duplicate text (C7). Then one full test run (C8).

**What you do.** Nothing until the end. The gate-manifest re-anchor you already
have queued gains one deletion and two new test files, and it must wait until
code review is done (chunk M). If it runs earlier, this change owes its own.

## Source proposals

**`2026-10-18-claude-external-is-a-maintainer-stance`**, accepted 2026-10-18 at
`58f30d6c`. Revision 1 binds. Its Security Review cleared at `11fb067d` with six
non-blocking findings, SR1 to SR6, which the Decision made plan requirements.
The Decision's answers:

* **Q1, capability floors by stage**: proposal review high; plan review medium;
  code review medium; Security Review high. The Maintainer added: "docstrings
  cleanup and related should go to low". The scribe recorded, unchallenged,
  that such an edit can run on low while its review stays at the usual tier
  wherever it touches a high-risk file.
* **Q2, header words**: `usual` and `usual + Security Review`.
* **Q3, headline**: the rewritten anchor and README wording is accepted as
  written in Revision 1; the name "Dual-Review" and the module id `dual-review`
  stay.
* **Q4, the lens roster**: carried by the second proposal.
* **Q5, migration**: ratified. Old records keep their wording, and an uncalled
  `External` label reads as the usual review.
* The author's three calls stand: External is called per artifact only; the
  cost-rule downshift stays, scoped; Complex projects get the one review, the
  named contracts and assumptions, and the scientific check once it lands.
* **Folded in**: `doctrine/dual-review.md`'s Boundary C opening names only "a
  trivial change's commit body"; it must also name the no-plan accepted
  proposal that `941cb34d` added.

**`2026-10-18-claude-review-lenses-for-every-install`**, accepted at `fbf664f0`.
Revision 1 binds; its Internal review (`b16f4607`) raised RL1 to RL7, all
accepted. The Decision's answers: **Q1** yes, one ledger, the doctrine's five
items; **Q2** yes, full text in the review-loop document with a pointer in
`AGENTS.md`; **Q3** no coverage-line stanza in the proposal or plan review
scaffolds; **Q4** no, the plan rehearses the LHM and modflow_tools upgrades on
scratch copies only; **Q5** yes, one plan with the stance proposal, with
`required(Internal + Internal Security Review)`.

## Scope

**Terms used below.** A **lens** is one of the nine fixed categories a reviewer
works through. A **frozen file** is one whose hash is pinned in
`bootstrap/tests/fixtures/gate_manifest.json` under `frozen_files`; changing it
needs the Maintainer's **re-anchor** (the supervised ceremony that re-pins the
manifest). The **AST baseline** is the committed fingerprint of the engine's
top-level definitions. **Boundary B** is the one full test run after the last
implementation commit; **Boundary C** is the code reviewer's independent attack.

### What changes

| Layer | Files | Chunk |
|---|---|---|
| Carriers: both `AGENTS.md` copies, the review-loop document and Cairn's copy | 4 | C1 |
| Authoring templates: proposal and plan, each with Cairn's copy | 4 | C2 |
| Collaboration agreement pair, `model-selection` pair, `security-review` pair, legacy profile, session-start skill pair, fidelity manifest sample | 10 | C3 |
| Doctrine: `dual-review`, `plans`, `proposals`, `roles`, `rationale`, `lifecycle`, `lifecycle-contract`, `session-routines`, `onboarding` | 9 | C4 |
| `dimensions/` (four) and `bootstrap/UPGRADE.md` | 5 | C5 |
| `README.md`, the figure, and eight docs pages (`glossary`, `vision`, `agent-team-onboarding`, `quickstart`, `workflow-role`, `getting-started`, `dev-tour`, `tool-usage`) | 10 | C6 |
| Three onboarding presets, their two installed copies, the `dual-review` module pair | 7 | C7 |
| Tests: create `bootstrap/tests/test_review_stance_in_shipped_files.py` and `bootstrap/tests/test_review_sweep_ships.py`; reword `test_review_and_verification_rules_ship.py`; delete `test_onboarding_review_tiers.py` | 4 | C1, C7 |

The list is the proposals' known set. **The searches below are the authority,
not this list.** A file with no hit and nothing that selects distance stays
untouched, and the record says so (the proposal's `doctrine/proposals.md` and
`doctrine/lifecycle.md` are likely cases). A hit in a file not listed, such as
`doctrine/onboarding.md`, is classified and fixed where it falls.

### The searches (the instrument, pinned)

Roots: `AGENTS.md`, `README.md`, `doctrine/`, `templates/`, both `_template.md`
files, `dev/agent_collaboration.md`, `dev/collaboration_agreement.md`,
`dev/modules/`, `docs/`, `dimensions/`, `bootstrap/fidelity-check.md`,
`bootstrap/UPGRADE.md`, `bootstrap/REANCHOR_RUNBOOK.md`, `on-ramp/`; `.md`,
`.yml` and `.svg`; archives excluded. Markup characters are stripped and
whitespace collapsed first. Measured at `f804f3b7`, interpreter Python 3.13.13:

* **Search A, the phrasing** (Revision 1 > section 4). **35 files, 102
  matches**, the same as the proposal reported. Control: both `AGENTS.md` copies
  match.
* **Search B, the act of selecting.** Rebuilt from the proposal's description,
  it gives **61 paragraphs in 30 files** against the proposal's 55 in 29. The
  difference is my reading of "within 120 characters" (either order, per
  paragraph), not a different file set. All five named controls match
  (`dimensions/complexity.md` both positions, the `dimensions/README.md` axis
  row, `doctrine/roles.md` "A Reviewer tier", the `doctrine/plans.md`
  reviewer-identity note, the `model-selection` downshift condition). **The
  implementing agent commits the script text into the Implementation
  verification record**, so the reviewer re-runs the same bytes.
* **Search C, a plain read.** The opening proposal asked for a read of every
  `external` and `independen` hit in `doctrine/rationale.md`,
  `doctrine/lifecycle.md` and `README.md`, which Searches A and B miss because
  they phrase it differently. The README claim sits at lines the searches do not
  reach. Revision 1 does not repeat the instruction; this plan keeps it.
* **The authority probe** (Security Review). A distance term near *waive,
  exempt, satisfy, clear, substitute, skip or instead of*, per paragraph. The
  review reported 18 hits; rebuilt, it gives **17 in 11 files**. The criterion is
  not the count. It is that the two privileges named below are gone and every
  remaining hit is classified.

**Classification.** Every hit of A and B ends in one of seven categories: the
Maintainer-called definition; a staffing fact; a credit comment; a marked
history reference; noise (`External-repo`, external links); the standing
launcher-review call (SR5, the sixth category the Security Review asked for); or
the cost-rule carve-out (the `model-selection` downshift condition). The
proposal's list names five and the table row decides the downshift, so the
seventh is made explicit here. Category membership is a reader's judgment; the
checks are that **every hit is classified** and that the code reviewer re-runs
both searches on the reviewed commit.

### Frozen files, AST, install contract, lockfile

**Frozen files: one, and it is a deletion.** `bootstrap/tests/test_onboarding_review_tiers.py`
(five pinned nodes) is retired in C7. Measured: `frozen_files` holds 183 keys at
`f804f3b7`; none of the 49 prose files is a key; the instrument was checked
against a known key (`bootstrap/tests/test_scaffold.py` returns true). The
`phase_mutable` and `cascade_mutable` sets hold none of them either. Prose is not
frozen; frozen tests read it.

* **What the deletion looks like.** In a scratch worktree at the base with that
  file removed, `python bootstrap/tests/_gate_manifest.py verify` reports one
  `FROZEN-MISSING` for it and five `COLLECTION-DROPPED`, one per node. The suite's
  own `bootstrap/tests/test_gate_manifest.py` does not read the committed fixture
  and stays green (the Security Review measured 21 passed). **So nothing in the
  suite reminds anyone**, and this plan must not rely on `AGENTS.md`'s sentence
  that a deleted frozen file "reddens this file". The board row does the
  reminding.
* **Tests that become frozen at the re-anchor.** The ceremony re-globs
  `bootstrap/tests/**/*.py`, so the two new test files and
  `test_review_and_verification_rules_ship.py` (unpinned today; reworded in C1)
  freeze at that moment. All three must be final first, or every later edit owes
  another re-anchor. Chunk M is gated on exactly that.
* **The queued row.** The opening commit adds a **Joined** paragraph to the
  re-anchor row in `dev/PLANNING.md`: the pending deletion, the two new files,
  the unpinned third, the gate, and the sentence that if the batch runs before C7
  this change owes its own re-anchor. Today's verifier shows 25 `FROZEN-MODIFIED`
  entries (the proposals said 24); **derive the set at ceremony time**, this
  figure is a pointer.
* **Frozen tests that read these surfaces and must stay green unedited:**
  `test_scope_reduction_trap.py`, `test_verification_boundaries.py`,
  `test_comprehension_floor.py`, `test_loop_fidelity_gate.py`,
  `test_documentation_plan_module.py`, `test_quickstart_sequence.py`,
  `test_scaffold.py`, `test_profiles_smoke.py`, `test_presets.py`,
  `test_onboarding_seed_roster.py`, `test_core_dev_folders.py`,
  `test_link_check_exclusions.py`, `test_check_cairn_content.py`,
  `test_cairn_prefix_links.py`.

**AST: no engine symbol changes.** No file under `bootstrap/_scaffold/` is edited.
The baseline is **already red at the base, for other work**: `python
bootstrap/tests/_ast_attest.py verify` reports `main` in `bootstrap/_scaffold/cli.py`
and `seed_gitignore` in `bootstrap/_scaffold/install.py` as CHANGED. That
re-anchor is the Maintainer's and is owed regardless. Boundary B will show it as
a non-pass that is not this plan's; C8 disposes of it by showing the same two
symbols with the same hashes before and after. **The figure is not to be carried
forward**: derive it again at the parent.

**Install contract: unchanged.** `scaffold.py --manifest` lists destination,
source and mode, with no content hashes. No file is added to or removed from the
install set, so it is byte-identical at every chunk (`cmp` against the base
output). The fidelity manifest (`bootstrap/fidelity-check.md`) takes a prose-only
edit to its sample roster; its only reader, `test_scaffold.py`, pins three
substrings (`optional_templates:`, `CONTRIBUTING.md`, `human_team`). Nothing
pins its bytes.

**Lockfile.** `python bootstrap/verify_integrity.py --target .` reports **18**
violations at the base. Five of the files this plan edits are among them
(`AGENTS.md`, `dev/agent_collaboration.md`, `dev/proposals/_template.md`,
`dev/plans/_template.md`, `.agents/skills/session-start/SKILL.md`) and are **not
finalized**: that would re-attest earlier, unreviewed drift.
`dev/collaboration_agreement.md` also differs from its record but is a
living-state file the verifier skips. Three module copies **match their record
today** and would go stale when edited: `dev/modules/dual-review.md`,
`dev/modules/model-selection.md`, `dev/modules/security-review.md`. Each is
scoped-finalized in the commit that edits it (precedent `2ea3f869`), so the count
stays 18. The lockfile schema is untouched.

**Vendor-neutrality (SR6).** `python scripts/quality_gate.py --sub neutrality`
exits 1 with **74** FAIL lines (21 info) at the base. Eighteen of them sit in five
files this plan edits: `docs/agent-team-onboarding.md` 8,
`doctrine/lifecycle-contract.md` 5, `doctrine/rationale.md` 3,
`templates/onboarding/solo-greenfield.md` 1,
`templates/skills/session-start/SKILL.md` 1. A bare "it passes" cannot be the
check, so each chunk records the FAIL lines for its edited files at its parent
and requires **no new line** afterwards, matching by file, token and line text
(line numbers move). If `neutrality-and-upgrade-slots` has landed, the baseline is
zero and the criterion is "stays zero". Rewording the credit line in
`solo-greenfield.md` also clears the one collision the Security Review found in
its test pattern; plan C rewords it first, and C7 does it only if it is still
there.

### Sequencing with the other work

The accepted work around this plan, in the order its authors wrote down:
`neutrality-and-upgrade-slots` (plan C, open, runs first),
`independent-scientific-check` (plan D, open), then `model-mapping-install-path`
and `board-as-basis` (accepted, no plan yet), and
`stewardship-and-reuse` (a proposal, issue #30). Plans C and D have each had their
plan review (`0389a14e`, `d7fe5d6a`, both REVISE) and are folding the fixes into
their cells, so every chunk here re-reads the files it edits at edit time. Files
shared, read from each one's own text at `f804f3b7`:

| Other work | Files shared with this plan | What each edits | Effect |
|---|---|---|---|
| **C: `neutrality-and-upgrade-slots`** | `templates/onboarding/solo-greenfield.md` | C rewords the credit line (its C5); this plan rewords the External-tier paragraphs (C7) | C first: this plan finds the line reworded and compares against zero |
| | `templates/skills/session-start/SKILL.md` and `.agents/skills/session-start/SKILL.md` | one phrase near the top (its C2); this plan changes "review tier, plan-review tier" in the board paragraph (C3) | different sentences; the twins stay byte-identical |
| | `doctrine/rationale.md`, `doctrine/lifecycle-contract.md`, `docs/agent-team-onboarding.md` | same-line `vendor-ok` markers on hit lines (its C6); this plan rewrites the anchor, wording and examples | a marked line this plan rewrites keeps or drops its marker on purpose, and the gate says which |
| | `bootstrap/UPGRADE.md` | step 4, a known-gap line, a new section (its C10); this plan edits the plan-pass schema rows (C5) | different sections |
| | `dev/.cairn/cairn-lock.yml`, `dev/PLANNING.md`, `CHANGELOG.md` | its twelve records; this plan's three; opening and archive commits | disjoint records; commit by path, read fresh |
| | the neutrality checker | stricter after its C1; zero after its C7 | all text this plan ships is held to it |
| | `test_onboarding_review_tiers.py` | its C5 criterion needs the old pin passing | **order matters**: C before this plan's C7 |
| **D: `independent-scientific-check`** | both proposal templates and both plan templates | a new block after the security preflight, and a paragraph in *Acceptance criteria*; this plan edits the Review preamble, the `**Review**:` and `**Tier**:` lines and the Plan review and Code review skeletons (C2) | different regions; D first, this plan rebases (D's plan says so). D's plan review (`d7fe5d6a`, REVISE, nine findings, now `revising-plan`) adds, in its finding on sequencing, that this plan will want the same template cells and the Complexity cell and must keep the check named there |
| | D's new test file (the block's reviewer-duty wording and the plan paragraph, named in D's plan under its own `Proposed paths:`) | it reads the template cells D adds | **this plan runs it unedited at C2 and C5.** It freezes at the same re-anchor: if D has archived and the ceremony has run before C2, any edit to a cell it pins would owe a second re-anchor. C2 edits none of those cells |
| | `dimensions/complexity.md`, `dimensions/README.md` | the Complex position and the Complexity cell repointed at the check; this plan strikes "mandatory" and "reserved" and rewords the same cell (C5) | **the reworded cell must keep naming the check** (D's plan asks for this) |
| **`model-mapping-install-path`** | `templates/modules/team-gated/model-selection.md` and `dev/modules/model-selection.md` | a "Filling the mapping" paragraph and one corrected sentence; this plan edits the role table, the downshift condition, the bright-line list and the diversity reference (C3) | different sections; whichever lands second re-finalizes the lock record |
| | `templates/onboarding/collaborative-team.md`, `templates/onboarding/high-rigor-legacy.md` | one conditional seed row each; this plan rewords External-tier sentences (C7) | different paragraphs; the seed tests in frozen `test_onboarding_seed_roster.py` read the same files |
| | `dev/PLANNING.md`, `CHANGELOG.md` | re-anchor row, archive | commit by path |
| **`board-as-basis`** | all four templates | the `**In brief**:` prompt beside the header; this plan edits the adjacent `**Review**:` line (C2) | adjacent lines, textual rebase |
| | `docs/tool-usage.md` | the board entry (reads headers only, `--json`); this plan changes "review tier" in the same paragraph (C6) | same paragraph, two phrases |
| | `doctrine/session-routines.md` | cited, not edited, by it; this plan changes "review tier, plan-review tier" and the dispatch line (C4) | none |
| | `templates/skills/session-start/SKILL.md` and twin | cites the board paragraph | none beyond C3's phrase |
| **`stewardship-and-reuse`** (issue #30) | `AGENTS.md` and `templates/core/AGENTS.md` | its "Git and commit workflow" and "Project-specific conventions"; this plan's "Review" | different sections |
| | `templates/core/dev/agent_collaboration.md` and `dev/agent_collaboration.md` | it adds one sentence to lens 5 and one to "non-blocking" at the sweep's final home | **this plan must leave lens 5 findable by its label, "Cross-document consistency", and the roster at exactly nine** (it pins nine) |
| | `doctrine/plans.md`, `doctrine/dual-review.md`, `doctrine/roles.md`, `doctrine/proposals.md` | its cost-bar and reuse sentences; this plan's reviewer-tier and stance edits | different sections |
| | both plan templates | *Scope*, *Dispositions* and the deviation sentence; this plan's Plan review and Code review skeletons | different sections |
| | the `dual-review` module pair | only if the lens text has not moved when its plan opens | this plan moves it first |

One statement in other work is out of date and is its author's to fix:
`stewardship-and-reuse` calls the lenses proposal "awaiting decision" (accepted at
`fbf664f0`).

### Recommended slot: third

**After C and D, before `model-mapping-install-path`, `board-as-basis` and
`stewardship-and-reuse`.**

* **The stance changes how every later review is run**: the Foundations block,
  no External, `usual` in the header, and the nine lenses in the document the
  reviewer actually reads. The two heaviest reviews still ahead are
  `model-mapping-install-path` (engine, Security Review, an AST re-anchor) and
  `board-as-basis` (a tool adopters run). Running them after this lands reviews
  them under the final rules instead of under the ones this plan retires.
  `stewardship-and-reuse` has already said it opens when this plan archives, and
  writes its lens-5 sentence at the lens's final home.
* **Against going first**, the overlaps with C are real: C zeroes the neutrality
  gate (which turns this plan's SR6 check from a baseline diff into a strict
  one), rewords the line this plan's tests care about, puts markers on hit lines
  in three files this plan rewrites, and has a criterion that needs the old pin
  passing until this plan deletes it. D is small, already open (its plan review has run and its author is
  folding the fixes), and its plan records that this plan rebases on it. Going first would make both rebase over
  a 49-file change, for a gain (reviewing two nearly finished plans under the new
  stance) that is small.
* **Against going last**, the later plans' overlaps with this one are small and in
  different sections (table above), so nothing is saved by waiting, and the three
  heaviest reviews would run under rules that are about to change.
* **Plan review can run now.** Implementation of C1 starts once C and D have
  archived, or at least once C's C2, C5, C6 and C10 and D's C2 to C4 (the chunks
  that touch shared files) have landed. Whichever lands second rebases.

### Plan decisions the proposals left open

* **Two test files, kept as named.** The stance proposal names
  `test_review_stance_in_shipped_files.py`; the lenses proposal names
  `test_review_sweep_ships.py`. One pins the stance and what must not appear;
  the other pins the sweep, through a real install. Merging them would make one
  file answer two proposals' questions.
* **Tests grow by chunk.** Each chunk lands the pins for the files it makes true,
  so the suite is green at every boundary. A path set the forbidden-phrasing
  test has not reached yet is not listed in it; C7 adds the **completeness**
  check that makes the listed set equal the pinned path set.
* **The privilege clause leaves the module in C1, not C7.** "Or is confirmed by a
  second independent different-agent-type pass" is the one place a more distant
  pass stands in for evidence in shipped text (SR1). Striking those words from
  both module copies in C1 removes the privilege from the first commit. The
  ledger paragraph around them moves in C7. This is a three-word edit that C7
  supersedes, not lens text written twice.
* **Presets, deletion and thinning share the last implementation chunk (C7).**
  The retired test counts exactly three paragraphs in the solo preset that name
  an External tier, so rewording the preset and deleting the test cannot be
  separated; thinning the module comes last because of RL7; and the Security
  Review asked that the final bytes of both tests and the deletion sit in one
  chunk immediately before the re-anchor. C8 changes only the plan. The
  re-anchor row says so.
* **The install test runs for all three shipped profiles.** The lenses proposal
  names `solo-greenfield`; the Maintainer's word was "Everyone should get them",
  and the other two presets cost almost nothing to add.
* **The coverage line is new wording, not a move.** The `dual-review` module says
  "close with the two-part coverage line" and never defines it (the body-coverage
  probe lists it as missing). The sweep's coverage paragraph is therefore drawn
  from `doctrine/dual-review.md` > "The coverage line" and reviewed as new text.
* **`AGENTS.md`'s pitfall sentence is not folded in.** The Security Review found
  that `AGENTS.md`'s operational pitfall about a deleted frozen file ("fails
  loudly ... reddens this file") is wrong for the suite, and said it "needs its
  own correction, separate from this change". It is not in either proposal's
  accepted scope. See *Dispositions*.

### Documentation / doctrine surface

Routed by `docs/DOCUMENTATION_PLAN.md`. **Governing and shipped**: C1 to C3, C7.
**Doctrine**: C4. **Dimensions**: C5. **Descriptive**: C6. **Deliberation**: this
plan, `dev/PLANNING.md` at the opening and archive, `CHANGELOG.md` at archive.
Rate-limit grounds are the proposals': the stance proposal's five independent
rulings plus this direction, and the lenses proposal's statement that no rule
changes, only where it ships. The Decisions ratified both.

## Sequence

Each chunk lands its own pins in the same commit, so the suite is green at every
boundary. C1 creates both test files and drops this plan's `Proposed paths:`
lines.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | **The carriers.** The one stance, the three stage questions, the Maintainer-called read (with SR1's four statements), the reviewer roster, and **the review sweep** (lenses, scope sentence, citation rule, coverage line, floor, project probes, the single ledger) land together in `templates/core/AGENTS.md`, `AGENTS.md`, `templates/core/dev/agent_collaboration.md` and `dev/agent_collaboration.md`. The pointer goes in both `AGENTS.md` files. The privilege clause leaves both module copies. Creates both new tests (carrier groups, the real-install group) and rewords the unpinned rules test. | `ready-to-implement`; C and D landed (*Recommended slot*) | one commit |
| C2 | **The authoring templates.** Review preamble, header grammar (`usual`, `usual + Security Review`; `**Tier**:` values; External only with `**Called by**`), the Plan review and Code review skeletons with their Foundations questions, SR1's statements. No coverage-line stanza. | C1; re-read each file at edit time | one commit |
| C3 | **Roster, floors and the rest of the shipped text.** Collaboration agreement pair, `model-selection` pair (stage rows, the low row, the SR4 carve-out), `security-review` pair, legacy profile, session-start skill pair, fidelity manifest sample. Two scoped lockfile finalizes. | C1 | one commit |
| C4 | **Doctrine.** The nine doctrine files, the SR1 strikes, SR5's sentence, the verbatim anchor, the Boundary C opening, the lenses' two doctrine edits. Appends the search classification. | C1 to C3 | one commit |
| C5 | **Dimensions and the plan-pass schema rows.** Complexity positions, the axis row, the team axes, `bootstrap/UPGRADE.md`. | C4; D landed | one commit |
| C6 | **The headline.** README, the redrawn figure, the docs pages. | C4 | one commit |
| C7 | **Retire and thin.** Three presets and two installed copies reworded; `test_onboarding_review_tiers.py` deleted; the stance test's preset group and completeness check; the module pair thinned; the sweep test's module group; a scoped finalize. The last chunk that changes test bytes. | C1 to C6; C landed | up to two commits, in that order |
| C8 | **Boundary B, then the record.** One full run on the finished work, written down (*Verification*), with the adopter rehearsal. Status to `awaiting-code-review`. | C7 | one commit |
| M | **MAINTAINER-ONLY — no new ceremony.** The *re-anchor* is the supervised ceremony, run only by the Maintainer, that brings the gate manifest up to date with changed tests (`bootstrap/REANCHOR_RUNBOOK.md`). The deletion of `test_onboarding_review_tiers.py`, the two new test files and the reworded unpinned one join the row already queued on `dev/PLANNING.md`, so M needs no Waiting line in this plan: that row declares the wait. **Gate: code review cleared and every `revising-code` commit landed, so no test byte can change afterwards.** If the batch runs before C7, this change owes its own. **An implementing agent must not perform it.** The agent's part is the board note at archive. | code review cleared | Maintainer |

### Followers

**`stewardship-and-reuse` (issue #30) follows this plan and does not fold into
it.** Its proposal (`dev/proposals/2026-10-18-claude-stewardship-and-reuse.md`,
awaiting review) says its plan opens when this plan archives. Its one real
dependency is small: it adds one sentence to lens 5 ("Cross-document
consistency", where the sweep already says to scan for "an existing tool/path the
change should use or update") and one to the sentence that a finding is blocking
or non-blocking, and it writes both at the lenses' **final home**, the review
sweep in the loop documents, which exists only once C1 has landed. This plan
therefore owes it three anchors, kept as a C1 criterion: the heading "The review
sweep", lens 5 findable by its label, and a roster of exactly nine (it pins nine
and adds no tenth). This plan edits none of its sections: the `AGENTS.md` pair's
"Git and commit workflow" and "Project-specific conventions", the plan templates'
*Scope*, *Dispositions* and deviation sentence, `doctrine/lifecycle.md`. Both
plans commit to `master`; "follows" means only that its plan re-reads the files it
edits at edit time.

### Wording the plan fixes

The implementing agent pastes these bytes, or a rewording that keeps every
obligation label named in *Acceptance criteria*. A word that must change before
implementation is a plan revision; after it, an appended note. Where the
Security Review asked the plan to quote a sentence, this is that quote.

**W1. The stage questions** (Revision 1; the sweep and the templates use the
same three rows):

| Stage | Should it happen as framed? (code: does it do what it claims?) | Best alternative | What would show it wrong |
|---|---|---|---|
| Proposal | Should this exist as framed? Is there a better design, doing nothing included? | The strongest, doing nothing included | What would make the author withdraw |
| Plan | The Decision settled the premise. Does the plan deliver it? | A simpler path to the same outcomes | The result showing it cannot deliver |
| Code | Does it really do what it claims? Try to break it, in order to fix it. | A simpler or safer build, if any | The input or run that breaks it, and what was tried; for code review this points at the falsification ledger rather than restating it |

**W2. The Maintainer-called read and SR1's four statements**, for the shipped
`AGENTS.md` and the four templates. It avoids the phrase "External ... by
default" in any form, which the unpinned rules test forbids:

> **More distance is the Maintainer's call, and only theirs.** An *External read*
> is a review the Maintainer asked for on one named artifact that exists now, in
> chat or inside a Decision, outside the usual procedure. The pass carries
> `**Called by**: Maintainer` followed by their words, verbatim and set apart; a
> relayed instruction names who relayed it. `**Tier**: External` is valid only
> with that line, and a pass headed External without it is read as the usual
> review. An agent never writes `required(External)`, never says a change needs
> one, never recommends more distance and never starts one without those words;
> it may name a risk and a gap in its coverage line. A call that covers artifacts
> not yet written is a standing floor, and a floor returns only by proposal.
> **A called read adds to the usual review and replaces nothing.** Its brief may
> add focus; it removes no owed answer and discharges no Security Review. Any
> other authority in the quoted words, such as a waiver or a change of scope,
> takes effect only where Maintainer authorizations already live, a Decision
> block or a plan's fence, and never from a `Called by` line. Nothing checks the
> quote mechanically: the next reviewer and the Maintainer at the Decision are
> the check.

**W3. The pointer in both `AGENTS.md` files** (the lenses proposal's draft,
already on the stance's wording; the test pins obligations, not sentences):

> **Every review shows its evidence.** The three answers a review owes rest on
> the nine standing lenses in `dev/agent_collaboration.md` > "The review sweep".
> A lens a review cites names the file, test, line or command that backs it (a
> bare "checked" is an incomplete review), and the coverage line that ends the
> review says what the pass did not cover. A reviewer who recommends narrowing
> the work states what is lost and why the narrower change still reaches the
> cause; only the Maintainer concedes a loss.

**W4. The cost-rule carve-out** (SR4), in the `model-selection` pair and
`doctrine/roles.md`:

> **The cost rule's check is not a review.** An orchestrator may run a
> sub-agent's generative step on a cheaper model only when the model that checks
> the output is at a tier strictly above it and is a different model
> architecture; a stronger model from the same maker is not one. The check is
> the orchestrator's. It is never filed as a proposal, plan or code review pass
> and never counts toward one, and no lifecycle review requires a different
> architecture. Sending the context packet to a second maker's model crosses the
> data-governance gate below, so that gate applies first.

**W5. The surviving standing call** (SR5), one sentence in `doctrine/dual-review.md`
beside the Maintainer-called definition:

> **One standing call survives, and it is the Maintainer's.** The re-anchor
> ceremony (`bootstrap/REANCHOR_RUNBOOK.md`) requires its launcher to be read by
> an External Security review. The ceremony's own record sets that requirement,
> the Maintainer chooses the reader each time, and no agent selects or
> substitutes for it; nothing else in the procedure works this way.

**W6. The Boundary C opening** (the folded-in fix), in `doctrine/dual-review.md`:
the parenthesis that now reads "a plan's Implementation verification section, or
a trivial change's commit body" gains "or the commit body of an accepted proposal
implemented in one commit with no plan". Nothing between that opening and the
six-trigger list is touched.

**W7. The anchor** (Q3, accepted verbatim). `doctrine/rationale.md`, framework
anchor 4, replacing the "Two-tier review ..." bullet:

> * **The Dual-Review model.** One review stance at every stage: a fresh reviewer, who did not
>   write the work, on the work's side, who makes it better by questioning its foundations and
>   answers in writing — should it exist as framed, what is the best alternative, what would show
>   it wrong — executed asynchronously and commit-mediated (`dual-review.md`). It is a specialized
>   variant of multi-agent debate (anchor 5) and a faithful instantiation of scientific peer review
>   (anchor 6). Its sharpest point: independence is *recorded, not claimed* — every review names its
>   reviewer, so how far that reviewer stood from the author is visible, and a different model
>   architecture or a person is available whenever the Maintainer asks for more distance.

**W8. The README** (Q3, accepted verbatim). Each replaces the text at the cited
lines of `README.md` (10, 49, 51, 53-54, 102-104, 176-181 at `f804f3b7`):

> Line 10: "read by someone who did not write it — a fresh AI session by default, a different model
> or a person whenever you ask —"
>
> | Independent referees who don't know you | A review by someone who did not write the work; a **different** AI model, or a person, whenever the maintainer asks |
> | Conflict-of-interest rules | Every review names its reviewer, so how far they stood from the author is on the record |
>
> Lines 53-54: "Distance is easier to record — the file names the reviewer, and "a different model
> architecture" is a brighter line than "no recent co-authorship," when you want that line."
>
> Lines 102-104: "- **The reviewer is not the author, and you can see who they were.** Every review is by a
> fresh reviewer, who must answer in writing whether the work should exist as framed and what would
> show it wrong. A different AI model, or a person, reads it too whenever you ask. Who reviewed what
> is written down in your repository, not claimed."
>
> Lines 176-181, figure text: "One review at every stage: a reviewer who did not write the work
> questions its foundations and answers in writing. A different model, or a person, adds more
> distance whenever the maintainer asks." Paragraph: "**This works with one agent.** If you have a
> single AI tool, a fresh session of it is your reviewer at every stage. A second model, or a second
> person, is there whenever you want more distance. You do not need a team to start."

## Acceptance criteria

**Reading these criteria.** Each ends with *Red when*: a change that turns it
red. A **label** is the property a test node is named for. Obligations are
alternations over whitespace-collapsed text, so a rewording that keeps the
obligation passes and a deletion fails; node IDs are labels, so rewording a
pattern renames nothing. A phrase count is taken at the chunk's parent (it must
fail or read zero there) and again at the chunk's commit. A set claim is checked
by listing the set from the tree and breaking each member in a separate copy,
reporting every mutant as killed, survived or equivalent beside an unmutated
control (`AGENTS.md` > Boundary C).

**Checks every chunk repeats.**

* `python scripts/claim_check.py` on each edited document, and `python
  scripts/check_cairn.py` with the edited paths named (explicit paths bypass the
  default filter, so the `dev/modules/` copies are scanned). *Red when:* a hard
  flag is left, or a deliberate forward reference is not marked.
* **Neutrality baseline diff** (SR6): the FAIL lines for the chunk's edited files
  at its parent, then at its commit; no new line, matched by file, token and line
  text. *Red when:* a line appears that was not there.
* `python bootstrap/scaffold.py --manifest` byte-identical to the base output
  (`cmp` exits 0). *Red when:* a row differs.
* **No slot is added.** `cairn:slot` counts at the base: `templates/core/AGENTS.md`
  5, `templates/core/dev/agent_collaboration.md` 3, both proposal templates 5,
  both plan templates 3, Cairn's `dev/agent_collaboration.md` and `AGENTS.md` 0.
  An unfilled slot is a finding in every install, and the frozen quickstart test
  compares the unfilled-slot count of a real install with its prose. *Red when:* a
  count rises.
* **No coordinate in a durable artifact.** In the lines the chunk adds, `grep -nE
  '\b(SR|RL|ES|CR)[0-9]+\b|\bC[1-8]\b'` finds nothing in any test name,
  docstring, comment or shipped sentence. (Control: the same grep finds ids in
  this plan.) *Red when:* a finding id or chunk letter ships.
* **The frozen pins named for the chunk pass unedited**, and `git diff --stat`
  for the chunk lists only the files the chunk names. *Red when:* a frozen file
  appears, or anything under `bootstrap/_scaffold/`.
* **Twin parity** where a pair exists: the shipped file and Cairn's copy carry
  the same added text, apart from tokens, slots and Cairn-only names (`diff` of
  the added lines). *Red when:* a word differs in one copy.

### C1 — The carriers

* **Both `AGENTS.md` copies carry the stance, in "Review".** Each label holds in
  both copies, inside the `## Review` section (placement is part of the rule):
  `one-stance-at-every-stage`; `a-fresh-reviewer-on-the-works-side`;
  `the-stage-sets-three-questions` (all three rows of W1);
  `foundations-block-three-answers-each-with-its-evidence`; `improve-means-recommend`;
  `no-quota-of-findings`; `a-clean-pass-needs-evidenced-answers-and-named-gaps`;
  `code-review-floor-is-not-the-implementing-agent`;
  `a-narrowing-is-a-scope-change-only-the-maintainer-concedes`;
  `a-clean-code-review-shows-a-falsification-ledger`. *Red when:* any label is
  absent from either copy.
* **The Maintainer-called read is stated, with SR1's four statements.** Both
  copies carry the labels `external-means-the-maintainer-called-it`;
  `a-call-names-one-artifact-that-exists-now`;
  `a-standing-call-is-a-floor-and-returns-only-by-proposal`;
  `called-by-carries-the-maintainers-words-verbatim`;
  `tier-external-needs-called-by-else-read-as-the-usual-review`;
  `no-agent-writes-required-external-or-recommends-distance`;
  `a-roster-you-set-is-not-a-call`; `a-called-read-adds-and-replaces-nothing`;
  `a-called-brief-adds-focus-removes-no-answer-and-discharges-no-security-review`;
  `other-authority-lives-in-a-decision-or-a-plan-fence`;
  `a-called-by-line-never-confers-authority`;
  `nothing-checks-the-quote-a-reader-does`. The shipped sentence agrees with W2
  and implies no tool, hook or gate validates the quote. *Red when:* a label is
  absent, or a sentence says a tool checks `Called by`.
* **No old vocabulary in the four carrier files.** Search A's patterns,
  `external[- ]by[- ]default` (any case, any wrapping), `a human fills`, a
  different-agent-type pass or round, and "Internal Reviewer", "External
  Reviewer", "External tier", "External floor" return nothing. The seven
  `structural` hits in these files are classified: a hit that says independence is
  required or earned by agent type is reworded; "a structurally-independent read
  is only independent if its author is its committer" is about attribution and
  stays. Each pattern is first shown to match the parent's text (both
  `AGENTS.md` copies match at the parent). *Red when:* any pattern matches, or a
  pattern does not match the parent.
* **The roster.** The loop document and Cairn's copy list Human Maintainer,
  Strategy, Implementation, **Reviewer** (one role, carrying the post-review
  neutral briefing that lays out the decision space without steering it),
  Security Review and User Agent. "Internal Reviewer" and "External Reviewer"
  are gone as roles, and "Tiers are stances, not staffing classes" is rewritten:
  a fresh session is every review's floor, distance is recorded, and the
  Maintainer may ask for more. *Red when:* either old role name survives.
* **The sweep sits in the loop document, once, before the trap.** Both loop
  documents contain a heading "The review sweep" ahead of the paragraph that
  opens "The clean pass has a mirror: the scope-reduction trap" (the frozen trap
  test pins that opening, so it stays). The sweep holds: a one-paragraph
  clean-pass statement; the nine lens labels, in order and exactly as the
  doctrine names them (Claims; Production path exercised by tests; Design
  completeness; Silent failure / fail-closed; Cross-document consistency; Drift;
  Lifecycle / process placement; Domain / scientific validity & scope; Name the
  satisfier), written as where the evidence for the three answers comes from, not
  a second checklist; the scope sentence (the sweep applies to the reviews the
  lifecycle calls for, and a trivial change with no review owes none); the
  citation rule; the two-part coverage line, which does not end in a
  recommendation for more review; "a floor, never a downgrade of a declared
  tier"; one sentence inviting project-specific probes after the nine; and the
  ledger's five items (surfaces probed; a negative or edge-case attempt;
  verification; residual risk; mutation when a claim names a set), with the
  sentence that a reviewer who tried to break the change and could not has
  cleared the gate and one who only read it has not. *Red when:* a lens label, the
  scope sentence, the citation rule, either coverage half, the floor sentence,
  the project-probes sentence or a ledger item is missing, the order of lenses
  differs, or the sweep follows the trap paragraph.
* **One ledger, no second definition.** The loop document defines the ledger
  once, with the doctrine's five items and no sixth "failure modes tested" item;
  `AGENTS.md`'s mutation rule and the loop document's mutation item agree.
  *Red when:* two definitions with different items exist in the installed files.
* **The doctrine's deeper reasoning stays out of installed text.** `grep -ciE
  'telegraph|ritual|evidence bar is staged'` over the sweep reads 0 (control: it
  reads above 0 in `doctrine/dual-review.md`). *Red when:* the sweep restates the
  staged evidence bar, the ritual signal or don't-telegraph-the-lens.
* **The sweep is body text.** The `cairn:slot` counts are unchanged and no marker
  sits inside the sweep. *Red when:* a slot is added.
* **Anchors a follower writes against.** The heading "The review sweep" is
  present; lens 5 is findable by the label "Cross-document consistency"; the lens
  roster is exactly nine, with no tenth; and the existing sentence "A finding is
  **blocking** or **non-blocking**" stays in the review loop, unchanged. *Red
  when:* the heading, a label or that sentence is missing, or there are ten lenses.
* **Size is recorded.** The sweep adds 85 to 95 lines to the loop document
  (152 to about 240); each pointer is about 7 lines; `templates/core/AGENTS.md`
  (419) and `AGENTS.md` (438) are recorded before and after. Outside the range is
  a signal, with a sentence in the commit body, not a failure.
* **The privilege clause is struck from the module.** "Or is confirmed by a second
  independent different-agent-type pass" is gone from both module copies. *Red
  when:* it survives in either.
* **The install carries it, for every preset.** For each of the three profiles in
  `bootstrap/profiles/`, a real install through `bootstrap/scaffold.py --config
  <profile> --target <temp>` yields a `dev/agent_collaboration.md` with all nine
  lens labels, the scope sentence, the citation rule, both coverage halves and the
  five ledger items, and an `AGENTS.md` with the pointer. At the parent a
  `solo-greenfield` install holds none of "Name the satisfier", "Silent failure",
  "Cross-document consistency", "Falsifiable coverage" or "coverage line", and
  "falsification ledger" appears in `AGENTS.md` only (measured at `f804f3b7`).
  The same patterns all match the `dual-review` module, so the empty results are
  absences, not a dead search. *Red when:* any installed file lacks an item, or
  the parent control does not show the absence.
* **The pointer is clean.** Each `AGENTS.md` pointer names
  `dev/agent_collaboration.md` > "The review sweep" and no `bootstrap/tests` path
  (the frozen boundaries test forbids Cairn-only tokens in the shipped file).
  *Red when:* it names one.
* **Both new tests exist, and each can fail.** The stance test pins the labels
  above, with a forbidden-phrasing group for the four carrier files and the two
  module copies, each pattern shown to match its pre-change string and to fire
  when the string is inserted into a copy. The sweep test pins the install
  results above and the same obligations over the four source surfaces. Patterns
  are literals, not derived from the files they check. Mutants, each beside an
  unmutated control, each of which must turn a named node red: delete lens 4 from
  a template copy; delete the "Not covered" half; delete the scope sentence;
  delete the sentence that `Called by` never confers authority; add
  `required(External)` to a copy. *Red when:* any mutant survives, or the
  control is red.
* **Red before the code.** Both test files run against C1's parent in a throwaway
  `git worktree` with only the new files copied in; every node fails on a missing
  obligation, not on an import error. The commit body names the parent SHA.
  *Red when:* a node passes at the parent.
* **The unpinned rules test is reworded.** Its docstring bullet and the
  failure message for the "not External by default" label no longer say an
  External code review is "an escalation"; the node IDs are identical before and
  after (`pytest --collect-only -q` diff is empty); "Code review is External by
  default." still turns it red. *Red when:* "escalation" survives in either place
  or a node ID changes.
* **The standing pins pass unedited**: `test_scope_reduction_trap.py` (the loop
  document and `AGENTS.md` obligations), `test_verification_boundaries.py`,
  `test_comprehension_floor.py`, `test_loop_fidelity_gate.py` (every
  `doctrine/` citation in a shipped file carries its allow marker),
  `test_documentation_plan_module.py`, `test_quickstart_sequence.py`,
  `test_scaffold.py`, `test_profiles_smoke.py`, `test_presets.py`,
  `test_onboarding_seed_roster.py`, and the rest of the mapped set (*Verification*).
  *Red when:* any fails.

### C2 — The authoring templates

* **The Review preamble states the stance.** All four templates carry the stance,
  the proposal, plan or code questions for their kind of artifact, the
  Foundations block, improve-means-recommend, and W2 (all twelve called-read
  labels). *Red when:* a label is missing from any of the four.
* **Header grammar.** The proposal templates' `**Review**:` line offers `usual`
  and `usual + Security Review` and no other value; the pass skeleton's
  `**Tier**:` offers `usual | Security Review`, plus External only beside a
  `**Called by**` line. `required(External)` appears in none of the four. The
  `**Plan review**:` line keeps its ruled tokens, `required(Internal)` and
  `required(Internal + Internal Security Review)`, and the plan-pass skeleton keeps
  `<Internal | Internal Security Review>`. The word "standard" is not used as a
  token (it collides with the lifecycle's "standard lane"). *Red when:* an old
  value is offered, a ruled token changes, or "standard" appears as a value.
* **The review skeletons carry the Foundations questions.** The plan template's
  Plan review skeleton names the plan row of W1 and its Code review skeleton the
  code row, with Answer 3 pointing at the falsification ledger; the proposal
  template's skeleton names the proposal row. The three questions use the label
  "Should this happen as framed?" so the ten-review tally in the proposal's
  signals is one grep. *Red when:* a skeleton lacks its row, or the label differs.
* **No coverage-line stanza** (the lenses proposal's Q3). The phrase "Not
  covered" appears in none of the four templates (0 at the base). *Red when:* it
  appears.
* **Neighbouring regions untouched.** The proposal templates' security-preflight
  slice (the span `test_scaffold.py` compares byte for byte between the two
  copies) is identical to the parent's; the frozen `test_verification_boundaries.py` guards on the plan
  templates (the "Reviewed range" count, no `## Implementation verification` H2)
  pass. No line of the Scope delta, Dispositions or Waiting-line
  text changes. *Red when:* any of those moves.
* **Legacy tokens are read, never rewritten.** `git diff --name-only <base>..<C2>
  -- dev/proposals dev/plans` lists only the two `_template.md` files. *Red when:*
  an existing proposal or plan is touched.
* **Plan D's cells are untouched.** If plan D has landed, its test file (the
  scientific-check guidance pin) passes unedited, and the added lines of C2 do not
  fall inside the block D adds to the proposal templates or the paragraph D adds to
  the plan templates' *Acceptance criteria*. *Red when:* D's test fails or a C2 hunk
  overlaps its cells.
* The stance test gains the template group (obligations and forbidden
  phrasings) with the same controls as C1.

### C3 — Roster, floors and the rest of the shipped text

* **The collaboration agreement pair** no longer says External is a read from a
  different agent type or "makes it prove it should land" at an External tier;
  Cairn's roster slot says the team's shape and nothing about earned
  independence. *Red when:* Search A or B finds the old sentences.
* **Capability floors by stage** in both `model-selection` copies: rows for
  proposal review (high; the premise is still movable and a wrong one is cheapest
  to catch here), plan review (medium), code review (medium; floor "not the
  implementing agent"), Security Review (high); the "External Review" and
  "Internal Review" rows are gone. **A row for docstring and comment cleanup is
  low**, with the clause that its review stays at the usual stage tier wherever
  it touches a surface the project's `AGENTS.md` names as high-risk. "Adversarial
  premise-checking" reads "premise-checking" (`grep -c 'adversarial
  premise'` is 0 in both copies and in `doctrine/roles.md`). The pair is
  byte-identical. *Red when:* an old row, "adversarial premise-checking", or a
  difference between the copies remains.
* **The cost-rule carve-out (W4)** is in both copies. Condition (a) reads
  "different model architecture"; "family" does not appear in it; one sentence
  says the check is the orchestrator's and is never filed as, or counted toward,
  a lifecycle review; one says the data-governance gate applies first. "Diversity
  within tier" is reworded as useful distance when the Maintainer assigns or asks,
  not a default an agent applies. *Red when:* any of the three statements is
  missing, or "family" survives in condition (a).
* **The checker and the mapping are untouched.** `git diff --stat` shows nothing
  for `scripts/check_model_selection.py`,
  `templates/modules/team-gated/check_model_selection.py` or
  `dev/.cairn/model-selection-mapping.yml`; `test_model_selection_stub.py`
  passes. *Red when:* any appears.
* **The `security-review` pair** loses the dangling "External Review Norms"
  pointer (a search over live files, archives and records excluded, for "External
  Review Norms", "Stage-to-role matrix" and "Review Expectations" returns five
  lines at the base: one in each `security-review` copy and three in
  `doctrine/plans.md`; the `security-review` pair is fixed here and the rest
  after C4, when the count is zero; `dev/measurement/queued-issue-drafts.md`
  quotes the heading as a record and is not edited). *Red when:* the pointer survives in either copy.
* **The legacy profile** (`templates/phase-0/project-profile-legacy.md`) no longer
  asks about "the Internal / External tiers". **The session-start skill pair**
  calls the board's two columns by what they are, with no "tier"; the twins stay
  byte-identical. **The fidelity manifest sample** lists the same roster as C1
  (no "External Reviewer", "Internal Reviewer" becomes "Reviewer"); the three
  substrings the frozen test pins are still present. *Red when:* the twins
  differ, the roster sample disagrees with `dev/agent_collaboration.md`, or a
  pinned substring is lost.
* **Lockfile.** Scoped finalizes for `dev/modules/model-selection.md` and
  `dev/modules/security-review.md` only; the lockfile diff touches only those two
  records; `verify_integrity` still reports 18 and neither file is among them.
  *Red when:* an unscoped finalize is run, or the count changes.
* The stance test gains the group for these files with the same controls.

### C4 — Doctrine

* **`doctrine/dual-review.md`.** "Two tiers, two purposes" becomes "One stance,
  three stages"; "Structural independence" keeps distance as recorded, not
  required; "Plan review is Internal, always" loses the External-floor bullet, the
  "External independence lives at the proposal" sentence and the type-scoped
  removal paragraph; "Code review — the implementation side" loses the External
  escalation; "recommended wherever it can be staffed" is gone; the clean-pass
  trap, the coverage line and "Briefs to reviewers" are re-pointed as in
  Revision 1 section 1 (a brief may state the stage's three questions);
  **W5** is present; **W6** is present; "Adaptation" says the sweep and the trap
  are no longer team-gated (the lenses' two sentences). The headings "Review
  expectations — the clean-pass trap" and the scope-reduction trap heading stay,
  adjacent and in that order. *Red when:* any statement is missing, the two
  headings are not adjacent, or the six-trigger span differs from the parent's
  (`git diff` of that span is empty; the frozen verification test parses it).
* **`doctrine/plans.md`.** The archive precondition no longer allows "a
  confirming second different-agent-type pass"; **"Tier ordering" is struck**
  (the second privilege); the reviewer-identity note loses "Escalate to the
  External-review tier" and its dangling "External Review Norms" and "Stage-to-role
  matrix" pointers; the "External floor lives at the deliberate lane's proposal
  review" sentence is gone; the pointer to "Review Expectations" now reads "The
  review sweep" and resolves; the ledger shape matches the loop document's five
  items; only the External rows of the stale planner text change. *Red when:* the
  authority probe finds either privilege, or a grep for the three dangling
  headings in live files is not 0.
* **`doctrine/roles.md`.** One Reviewer role carries the briefing duty; "External
  Reviewer" leaves; "A Reviewer tier" and its "pick the tier from the change's
  risk" go; capability floors are the four stage rows plus the low cleanup row;
  W4 is present; "Diversity within tier" is reworded; "adversarial
  premise-checking" is "premise-checking". *Red when:* any of those survives.
* **`doctrine/rationale.md`.** Anchor 4 equals W7 byte for byte after whitespace
  collapse (compare against the proposal's block); the name "Dual-Review" and the
  module id are unchanged. Search C: every `external` and `independen` hit in this
  file and in `doctrine/lifecycle.md` is read and classified. *Red when:* the
  anchor differs, or a hit is unclassified.
* **The rest.** `doctrine/session-routines.md` (the dispatch line follows what the
  Maintainer asked, else a same-type fresh session; the "review tier" phrase),
  `doctrine/lifecycle-contract.md` (the retired-tier sentence is a marked history
  reference), `doctrine/onboarding.md` (a credit), `doctrine/lifecycle.md` and
  `doctrine/proposals.md` (read; changed only if a search says so, and the record
  says which). *Red when:* a file has an unclassified hit.
* **The classification is written down.** An appended section, `## Search
  classification -- <agent> -- YYYY-MM-DD`, lists every hit of Searches A and B
  with its category (seven, above) and the file's disposition, and records the
  script text for Search B and the authority probe. *Red when:* a hit is missing
  from it.
* **Gates.** `python scripts/quality_gate.py --sub redundancy` reads fail=0 (it
  compares `doctrine/`, `dimensions/`, `on-ramp/` and `docs/` by 5-word shingles,
  so the anchor and the README text must not be pasted into a second page);
  `python bootstrap/check_module_body_coverage.py --target . --cairn-root .`
  reports no more than 8 missing topics (8 at the base; it is a regression
  probe, not evidence the text arrived); the frozen trap test passes unedited,
  including the adjacency of the two trap headings. *Red when:* redundancy fails or
  the missing-topic count rises.

### C5 — Dimensions and the plan-pass schema rows

* **`dimensions/complexity.md`.** The Simple position no longer says External is
  "reserved"; it names the one review with a thinner evidence plan. The Complex
  position no longer says External is "mandatory"; it names the one review with
  the scientific-trust lens, a proposal that names the contracts and scientific
  assumptions it touches, and the independent scientific check. **C5 starts only after plan D has landed (its gate in
  *Sequence*), so the sentence uses D's wording and points at the block D adds to
  the proposal template.** *Red when:* "reserved" or "mandatory" survives, or the
  check is not named.
* **`dimensions/README.md`.** The Complexity cell reads "review weight and
  verification depth" and keeps a mention of the check (plan D asks for it); the
  minimal-team sentence is a staffing fact. **`dimensions/agent-team.md` and
  `dimensions/human-team.md`** say who is available to be the one reviewer, not
  that an External tier is filled. *Red when:* any still says a tier is
  "wanted", "filled" or "mandatory".
* **`bootstrap/UPGRADE.md`.** Only the External rows of the plan-pass schema change
  (`required(External, security lens)` and `required(External + External Security
  Review)` become Internal examples); the stale planner text around them is
  untouched. *Red when:* any other line of that section moves.
* **Search B controls.** The five named controls no longer match as selection
  rules. *Red when:* a control still reads as one.
* Gates as C4 (redundancy; no new neutrality line; claim and prose checks).

### C6 — The headline

* **README.** The text at the six cited places equals W8 after whitespace collapse,
  and each of the six places is checked on the parent first to confirm the cited
  line numbers still hold (they do at `f804f3b7`). Search C: every `external`,
  `independen`, `different model` and `different AI` hit is read and classified.
  *Red when:* any of the six differs from W8, or a sentence still promises that
  review "has to come from" a different model or a person.
* **The figure.** `docs/assets/dual-review-independence.svg` is redrawn: it parses
  as XML, keeps its width, height and viewBox, carries the figure text of W8 in its
  title and description, and none of "two tiers", "Internal", "External" or
  "different agent type or human" survives in it; the README alt text equals the
  figure's accessible title. *Red when:* the file does not parse, the embed
  dimensions change, or an old phrase survives.
* **The docs pages** (`glossary`, `vision`, `agent-team-onboarding`, `quickstart`,
  `workflow-role`, `getting-started`, `dev-tour`, `tool-usage`) no longer say
  review comes from a different agent type or a person as a requirement or an
  "External floor"; the glossary's External entry becomes the Maintainer-called
  read and its Dual-Review entry says what "dual" means now (an independent
  reviewer beside the author at every stage, then the Maintainer's Decision);
  `docs/tool-usage.md` says "review" and "plan review", not "review tier"; each
  page's rewritten sentence agrees with the README's and is not pasted from it.
  `docs/quickstart.md` keeps the frozen test's two strings (`**N** modules listed`,
  `**N unfilled block slots**`) with N still true. *Red when:* the quickstart test
  fails, the redundancy gate fails, or a page still states the old floor.
* `python scripts/check_cairn.py` on README and each docs page resolves every link
  and anchor, including the image path. *Red when:* a link breaks.

### C7 — Retire and thin

* **The presets stop saying anyone fills an External tier.** The three
  `templates/onboarding/*.md` presets and the two installed copies under
  `dev/modules/onboarding/` are reworded so the External tier is not "staffed" by
  anyone; the three paragraphs in `solo-greenfield.md` the old test counted are
  reworded. If the credit line near the end of `solo-greenfield.md` is still
  there, it is reworded in code terms; if plan C already did it, nothing is owed.
  The `first-cross-type-review` onboarding trigger matches a vendor name, not the
  word, and is not edited. *Red when:* Search A or B finds a hit in them.
* **The old pin is retired, and its two wordings are carried as literals.**
  `bootstrap/tests/test_onboarding_review_tiers.py` is deleted. The stance test
  forbids both retired wordings as **literals** ("external tier (currently filled
  by fresh-session same-vendor review)" and "fresh-session external review tier
  reproducible"), each with its own non-vacuity control (it matches its literal and
  fires when inserted into a preset copy), and it globs the presets and the
  `dev/modules/onboarding/` copies, asserting the glob is non-empty and holds at
  least the three shipped presets. A preset added later cannot escape it. The test
  does not rely on the "strip every match" control alone, which takes its mutation
  from the pattern under test; it says which controls are independent of the
  pattern. *Red when:* either literal is dropped to clear the credit line, the glob
  misses a preset, or a control passes vacuously.
* **Completeness.** The stance test lists the pinned path set by glob and fails
  unless every file with a Search A hit is scanned or sits in an explicit
  exemption table (path and reason). Controls: remove a file from the table,
  and insert a phrase into a scanned copy; each turns a node red. *Red when:* a
  file with a hit is neither scanned nor exempted.
* **The deletion is visible where the suite is blind.** In a scratch worktree at
  C7 the verifier reports `FROZEN-MISSING` for exactly this file and
  `COLLECTION-DROPPED` for exactly its five nodes (beside the existing batch), and
  `pytest bootstrap/tests/test_gate_manifest.py` stays green; both are recorded.
  *Red when:* another frozen file is missing or another node is dropped.
* **The module is thinned.** Both copies drop the roster, the citation rule and the
  ledger for a two-line pointer to "The review sweep" and shrink from 152 and 151
  lines to about 84 (recorded). They keep what is about multi-type teams and what
  the frozen trap test pins: the scope-cut-means-claim-correction clause beside
  the trap, the trap paragraph, the three-way outcome test, "never in the
  baseline", and the Maintainer's concession. The id, gate and install path do not
  change: `scaffold.py --manifest` is byte-identical and `git diff --stat
  bootstrap/_scaffold` is empty. Any `doctrine/` citation in the thinned module
  carries its allow marker. *Red when:* a frozen trap-test node fails (named:
  `templates/modules/team-gated/dual-review.md::scope-cut is reserved for claim
  correction`, `::names the trap`, `::carries the three-way outcome test`,
  `::declining a review-proposed expansion is not a reduction`, `::only the
  Maintainer may concede a baseline outcome`, and the same five for
  `dev/modules/dual-review.md`), or the manifest differs.
* **The sweep test's module group.** The module carries none of the nine lens
  labels, the citation rule or the five ledger items. Mutants, each beside an
  unmutated control, each turning a named node red: restore the roster in a module
  copy; then the citation rule; then the ledger. The six C1 and C7 mutants are
  re-run at the final state and reported as one ledger (killed, survived,
  equivalent). *Red when:* any survives.
* **Expected checker flags.** `python scripts/check_cairn.py` with the two
  archived source proposals named explicitly reports exactly two new line-bound
  flags at C7, the module citations in the stance proposal's Security Review
  (module lines 132-133 and 131-132, in files that are now about 84 lines), and
  nothing else new. They are expected and recorded; that record is append-only and
  is not edited. The default run skips archives, so it never shows them. *Red
  when:* a flag appears that is not these two.
* **Lockfile.** Scoped finalize for `dev/modules/dual-review.md` only.
  `verify_integrity` still reports 18.
* **The tests are final.** After this chunk the three test files change only in a
  `revising-code` commit, and each such commit says it re-opens chunk M's gate.
  *Red when:* a later chunk edits one.

### C8 — Boundary B and the record

* **The record is complete.** `## Implementation verification` carries every field
  *Verification* lists, the node IDs of both new test files from `pytest
  --collect-only -q`, the Search B and authority-probe script text, the per-hit
  classification pointer, the neutrality baseline diff for every edited file, the
  mutation ledger, and the rehearsal result below. *Red when:* a field is absent
  or an ID differs from the collection.
* **The authority probe, re-run at the tested commit.** Neither privilege remains
  (no "confirming second different-agent-type pass", no "External satisfies a
  required Internal"), and every remaining hit of the rebuilt probe is classified.
  *Red when:* a privilege remains or a hit is unclassified.
* **The adopter rehearsal** (the lenses' Q4). For LHM and modflow_tools, read-only:
  extract tracked `dev/`, `AGENTS.md` and `CLAUDE.md` from each repository's
  committed tree (`git archive`) into a fresh folder, then run `python
  bootstrap/scaffold.py upgrade --target <copy> --plan` and `--stage` from Cairn at
  the tested commit in a separate worktree. Record the kind of each of
  `AGENTS.md`, `dev/agent_collaboration.md` and `dev/modules/dual-review.md`
  (merges clean, conflicts, untouched), count conflict hunks, and check every
  staged tree for **two definitions of the roster, the ledger or the clean pass**
  and for a conflict outside the review-loop region. The base figures are
  modflow_tools: all three clean; LHM: `AGENTS.md` clean, the loop document
  conflicts (LHM's own clean-pass list, ledger, briefs and restricted-verification
  text against nothing upstream), the module untouched. The advice for LHM is: take
  the core sweep, keep its domain probes (units and coordinate systems, HDF5
  quantization, the MATLAB and MODFLOW boundaries), which now have a home in the
  project-probes sentence, and drop its duplicate ledger and clean-pass statement.
  Neither repository is modified, and no real upgrade is run. *Red when:* either
  repository's working tree or history changes, a staged tree holds two
  definitions, or a merge conflicts outside the loop region (reported to the
  Maintainer as a signal, not hidden).
* Boundary B runs in **full** mode (*Verification*). Status moves to
  `awaiting-code-review`.

## Scope delta

**Accepted scope is a floor.** The baseline is the two proposals as accepted. Every
outcome maps to a chunk or a named disposition.

| Accepted outcome | Chunk or disposition |
|---|---|
| One stance, three stages; Foundations block; improve means recommend; no quota; clean-pass restated; code floor and plan-review rounds unchanged | C1, C2, C4 |
| External is the Maintainer's call, per artifact; `Called by` verbatim; never-does list; a roster is not a call; a standing call is a floor | C1, C2, C4 |
| Header and record grammar (`usual`, `Tier` values, legacy read never rewritten) | C2 (C1 for the read rule) |
| No rule selects more distance: Search A, Search B, the thirteen-row table | C1 to C7; classification appended at C4 |
| The reviewer roster after the change | C1, C3, C4 |
| Capability floors by stage; the low cleanup row; "premise-checking" | C3, C4 |
| Migration table | C1, C2 (the read rule), `git diff` checks in C2 |
| Reaching adopters: shipped text first | the order of C1 to C4 |
| Headline: anchor and README verbatim, figure, descriptive pages | C4, C6 |
| Tests: retire; add; reword; keep the trap test green; every test file that mentions External has a disposition | C1, C7; table in *Verification* |
| Evidence plan: Searches A and B with controls, falsifiers, smoke checks | C1 to C8 |
| Security preflight S1 to S5 | *Verification*; S3's quoted sentence is W2 |
| Not in the proposal: engine gate and comment, runbook and credit comments, stale planner text | untouched; *Dispositions* for the board row |
| The sweep, citation rule, coverage line and ledger in the loop document; the pointer; the scope and project-probes sentences | C1 |
| The module keeps multi-type content; thinned last | C7 |
| Cairn's own copies follow | C1, C7 |
| The two doctrine sentences ("Adaptation") and the pointer retarget | C4 |
| The lenses test, positive and negative, with the six mutants | C1, C7 |
| Boundary C opening names the no-plan proposal | C4 |
| Q3 of the lenses: no coverage-line stanza in the scaffolds | C2 (negative check) |
| Q4 of the lenses: rehearsal on scratch copies, no real upgrade | C8 |

**The Security Review's six findings.**

| Finding | Where it becomes a criterion |
|---|---|
| SR1: a `Called by` quote authorizes the read it heads and nothing else; four statements; the two privileges struck | W2; C1 (carriers, module clause), C2 (templates), C4 (`doctrine/plans.md`), C8 (probe) |
| SR2: the retired test's two wordings carry over only as literals; glob the presets and the installed copies | C7 |
| SR3: the deletion is silent in the suite; final test bytes and the deletion in one chunk before the re-anchor; board line | the opening commit's row; C7; M; *Scope* |
| SR4: the carve-out says "architecture", is never a lifecycle pass, sits under the data-governance gate | W4; C3, C4 |
| SR5: the launcher review is the one surviving standing call; a sixth category; the runbook untouched | W5; C4; *Verification* (runbook and launcher files byte-identical) |
| SR6: neutrality is already red, so compare before and after | every chunk; *Scope* |

**The lenses review's seven findings.** RL1 (one plan): this plan. RL2 (one
ledger, five items; the doctrine pointer retargeted): C1, C4. RL3 (size 85 to 95,
the signal recast on doctrine reasoning leaking): C1. RL4 (LHM advice; the
project-probes sentence; the signal widened to duplicate definitions): C1, C8.
RL5 (the scope sentence, pinned): C1. RL6 (negative assertions for roster,
citation rule and ledger; the restore-ledger mutant; the body-coverage count a
regression check only): C7, C4. RL7 (module last; the two flags recorded): C7.

**Cannot become a checkable criterion, and why.** Named, not dropped:

* **Whether the Called-by quote is genuine.** Nothing mechanical can fail on it
  (the proposal's S2 says so). The criterion is that no shipped sentence implies
  a gate and that the reader is named (C1).
* **Whether a hit is classified correctly.** Search B cannot decide meaning. The
  checks are completeness of the classification and the reviewer's re-run.
* **The four "signals the change is wrong".** Reviews that read as polish, a
  defect a more distant read would have caught, External requested on most
  proposals, an agent writing External again. They are future observations across
  reviews that do not exist yet. The plan makes the first one countable (the
  shared "Should this happen as framed?" label, C2) and the last mechanical (the
  forbidden-phrasing group). The watching itself has no live home until the
  Maintainer authorizes one (*Dispositions*).
* **"Plain".** Whether the new Review text reads plain to the Maintainer is the
  plan reviewer's and the Maintainer's call. The plan holds the line counts and
  the vocabulary, not the reading.
* **"A tree that never runs `upgrade` gets nothing."** True and unfixable here.

**Scope delta**: preserved. Nothing either proposal committed to is dropped. The
three additions the plan makes (the module clause in C1, the all-profiles install
test, the completeness check) are expansions of verification, not of delivered
scope, and declining any would not be a reduction.

## Verification

**Boundary A (iteration, scoped).** Each chunk runs the tests that own the files
it touches, found by searching `bootstrap/tests`, `scripts`, `tools` and the engine
for each touched path at `f804f3b7`, plus the standing gates in *Checks every
chunk repeats*. **This is not a confident bound**: 57 test files drive a scaffold
install, which renders the shipped files. Boundary B is the real check.

| Chunk | Tests |
|---|---|
| C1 | the two new files; `test_review_and_verification_rules_ship.py`, `test_verification_boundaries.py`, `test_comprehension_floor.py`, `test_scope_reduction_trap.py`, `test_loop_fidelity_gate.py`, `test_documentation_plan_module.py`, `test_quickstart_sequence.py`, `test_scaffold.py`, `test_profiles_smoke.py`, `test_presets.py`, `test_onboarding_seed_roster.py`, `test_cairn_prefix_links.py`, `test_check_cairn_content.py`, `test_quality_gate_neutrality.py`, `test_onboarding_review_tiers.py`, `test_manifest.py`, `test_module_roster.py`, `test_module_merge.py`, `test_merge_module.py`, `test_upgrade.py`, `test_lockfile_module.py`, `test_verify_integrity.py` — the 22-file set the lenses review measured; **625 passed in 39 s at the base** under Python 3.13.13 |
| C2 | the C1 set, plus `test_claim_check_module.py`, `test_core_dev_folders.py`, `test_incident_trackers_module.py`, `test_install_module.py`, `test_session_routines.py`, `test_trigger_evaluation_action.py`, `test_replacement_tools.py`; plan D's scientific-check test file once it exists |
| C3 | `test_model_selection_stub.py`, `test_upgrade_module.py`, `test_profile_grammar.py`, `test_security_stack.py`, `test_onboarding_seed_roster.py`, `test_presets.py`, `test_profiles_smoke.py`, `test_scaffold.py`, and the skill tests (`test_skills_install.py`, `test_skills_fanout.py`, `test_skills_upgrade.py`, `test_skills_self_heal.py`, `test_skill_contract.py`, `test_session_routines.py`, `test_session_failsafe.py`, `test_first_session_report.py`) |
| C4 | `test_scope_reduction_trap.py`, `test_verification_boundaries.py`, `test_comprehension_floor.py`, `test_loop_fidelity_gate.py`, `test_check_cairn_content.py`, `test_claim_check_module.py`, `test_incident_trackers_module.py`, `test_replacement_tools.py`, `test_skill_contract.py`, `test_onboarding_activation_helper.py`, `test_deferred_task_store.py`; gates: redundancy, body coverage |
| C5 | `test_scope_reduction_trap.py`, plan D's scientific-check test file; gates: redundancy |
| C6 | `test_quickstart_sequence.py`, `test_doc_governance.py`, `test_check_cairn_content.py`, `test_link_check_exclusions.py`, `test_core_dev_folders.py`, `test_module_roster.py`, `test_scaffold.py`; gates: redundancy, `check_cairn.py` |
| C7 | `test_onboarding_seed_roster.py`, `test_onboarding_slot_substitution.py`, `test_presets.py`, `test_profiles_smoke.py`, `test_active_surfacing_render.py`, `test_active_surfacing_mechanism.py`, `test_trigger_evaluation_action.py`, `test_onboarding_activation_helper.py`, `test_quickstart_sequence.py`, `test_scope_reduction_trap.py` (both module copies), `test_module_roster.py`, `test_gate_manifest.py`, both new files |

**Boundary B mode**: full. The refusal rules in `AGENTS.md` settle it, five ways:

1. **A contract surface is touched.** A frozen gate test is deleted, which changes
   the gate manifest's pinned collection (five nodes), and the fidelity manifest's
   sample roster is edited. Bounded mode refuses.
2. **A trust-ceremony surface is adjacent.** The plan carries an Internal Security
   Review obligation, and `AGENTS.md` names vendor-neutrality and the install
   contract as high-risk surfaces; shipped prose is edited on both.
3. **No mapping bounds the change confidently.** 57 test files render the shipped
   `AGENTS.md`, templates and modules. Uncertainty resolves to `full`.
4. **Both accepted proposals say so.**
5. **The lockfile is touched** (three scoped finalizes). Whether a record edit
   counts as touching the contract is uncertain, and uncertainty resolves to
   `full`.

**How it runs.** After C7, in a separate worktree at the tested commit (a worktree
shares refs, so the gate anchor `refs/cairn/gate-anchor` is present, and other
sessions' uncommitted files stay out of the count), under the canonical
interpreter (Python 3.13.x, as `tools/session.py` resolves it):

```
CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0
python scripts/quality_gate.py --sub neutrality --sub redundancy
```

Then `check_cairn.py`; `claim_check.py` on each edited document; `scaffold.py
--manifest` against the base; `check_module_body_coverage.py`;
`verify_integrity.py --target .`; the AST verifier; and `_gate_manifest.py verify`.
The record uses the template's fields: mode, tested commit, reviewed range,
interpreter, clean pre- and post-run state, a command table, non-pass
disposition, plan-specific commands, known omissions.

**Expected non-pass**, each disposed of rather than treated as noise:

* **The neutrality leg** exits 1 at the base with 74 FAIL lines. Record the figure
  at the tested commit and show that no line is in a file this plan edited and was
  not there at the base (or, if plan C has landed, that it reads zero).
* **The AST verifier** reports the two symbols above as CHANGED. Show the same
  two, with the same hashes, before and after; none is this plan's.
* **`_gate_manifest.py verify`** reports `FROZEN-MISSING` and five
  `COLLECTION-DROPPED` for the retired test, and the other batch's drift. These
  are the owed re-anchor (M). `pytest bootstrap/tests/test_gate_manifest.py` is
  green regardless.
* **`verify_integrity`** reports 18 findings before and after; the same set.

**Test files that mention "External"** (`grep -rln External bootstrap/tests/`,
`.py` only, 19 files at `f804f3b7`). The proposal listed 18; the 19th is the
unpinned rules test.

| File(s) | What "External" is there | Disposition |
|---|---|---|
| `test_onboarding_review_tiers.py` (frozen) | the pin itself | retired (C7) |
| `test_review_and_verification_rules_ship.py` (unpinned) | an absence pin, plus a docstring and message that call External code review "an escalation" | reworded (C1); node IDs unchanged |
| `test_scope_reduction_trap.py` (frozen) | a fixture heading; also pins the trap headings and obligations in both module copies | unchanged, must stay green |
| `test_presets.py` (frozen) | a comment that dual-review needs a second type to fill its External tier | unchanged (the engine comment is a board row) |
| `test_reference_scripts.py`, `test_session_routines.py`, `test_trigger_evaluation_action.py` (frozen) | fixture headings such as `(External Reviewer)` used to exercise review-heading parsing and the vendor-match trigger | unchanged: the parsers key on the vendor name, not the word |
| `_gate_manifest.py`, `_gate_preflight.py`, `_gate_transition.py`, `test_gate_preflight.py`, `test_reanchor.py`, `test_correct_pinned_digests.py` (frozen) | provenance strings for how past ceremonies were reviewed | unchanged: history, in frozen files |
| `test_content_scan.py`, `test_claim_check_module.py`, `test_link_check_exclusions.py`, `test_onboarding_activation_helper.py`, `test_onboarding_slot_substitution.py` (frozen) | authorship credits in comments and docstrings | unchanged |
| `test_security_stack.py` (frozen) | "External simulator", an unrelated trust-boundary term | unchanged |

The runbook and launcher files are **byte-identical** to the base:
`git diff --stat` over `bootstrap/REANCHOR_RUNBOOK.md`, `bootstrap/reanchor.sh`,
`bootstrap/reanchor-launcher.template.sh` and `bootstrap/tests/_gate_reanchor.py`
is empty (SR5).

**Boundary C** is the code reviewer's, run after Boundary B, and it is not a re-run
of Boundary B's command. The set claims worth breaking one member at a time, in a
separate copy of the reviewed commit, listing each set from the tree:

* **"Every install gets the lenses."** The set is three profiles × (loop document,
  `AGENTS.md`). Delete a lens from each rendered source in turn.
* **"No shipped sentence selects distance."** The set is the Search A and Search B
  hits, listed from the tree at the reviewed commit; insert a selecting sentence
  into a scanned copy of each root.
* **"A called read confers no authority."** The set is the two `AGENTS.md` copies
  and the four templates; remove the SR1 statements from each.
* **"The lens text exists once."** The set is every file carrying a lens label; the
  module must carry none, and Cairn's copies must agree with the templates.
* **The headline spots.** The set is the anchor, the six README places and the
  figure text; alter a word in each.

Also worth attacking: a `Called by` quote that carries a waiver; a preset added
later that the glob should catch; the completeness exemption table used to hide a
hit; the dangling-heading grep; the adopter staged trees.

**Security preflight, re-answered where the chunking changes an answer.** The
proposal's S1, S4 and S5 stand. **S2** (can it fail?): the stance and sweep
controls run in C1 for the carriers, in C7 for the presets, the completeness check
and the module group, and C8 reports one ledger at the final state; the
Called-by check cannot fail mechanically and the text says so. **S3** (what fires
it): `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests` over the shipped sources
the tests list, and the quoted adopter-facing sentence is W2, which agrees with
S3's paragraph: in an adopter tree the rule is one sentence in `AGENTS.md` and the
check is a reader.

## Dispositions

*Filled at archive-preparation.* Known now:

* **The archive commit writes this plan's `CHANGELOG.md` entry**, including the
  upgrade note for adopters (what merges, and the LHM advice from C8).
* **It adds a note to the queued re-anchor row** with the node IDs of the two new
  test files, the final statement about the deletion, and that M waited for code
  review.
* **Board rows deposited at archive**, each under a `defer` request with the
  Maintainer's quoted authorization. The accepted text assigns both to this plan:
  (a) the engine's `_TEAM_STAFFING_GATES` comment ("fill its External tier") and
  the matching comment in `bootstrap/tests/test_presets.py` are now false and are
  left alone here (stance proposal, *Not in this proposal* and the Response to the
  standard review); (b) retiring the module's duplicate trap paragraphs and their
  pins (lenses proposal, *Not in this proposal*). Authorizations to quote: "accept
  both as descried" and "I accept all five of your recommendations. Accept as
  recommended".
* **Two items that are not in either accepted scope**, to be put to the
  Maintainer in the one `defer` batch unless the Maintainer says to fold them in
  (folding in would be an addition, not a reduction): (a) the correction of the
  operational-pitfall sentence in Cairn's own `AGENTS.md` about a deleted frozen
  file, which the Security Review said needs "its own correction, separate from
  this change" (the sentence is not in the shipped copy, so no adopter is
  reached); (b) a live home for the ten-review tally and the other signals, since a
  watch that lives only in an archived proposal is lost. The proposed disposition
  for both is `defer`, not `wontfix`: the Security Review named the first, and the
  second belongs to an accepted Decision's contract.
* **This plan carries no Waiting line at archive.** The open wait, the re-anchor, is
  declared on its marked board row.

## Plan review -- Claude Opus 5.5 (Internal Security Review) -- 2026-10-18

```
Reviewed commit: 8cc124b5f537ca14742216e53224cfd7e2d4345c
Target: the whole plan, read for the review trust apparatus: W1-W8, Acceptance criteria C1-C8 and M, Scope delta (the SR table), Verification, Dispositions; checked against the stance proposal's Revision 1 and its Security Review
Prior findings: SR1-SR6 (the stance proposal's Security Review at 11fb067d), checked for closure here
Assurance path: high-assurance
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised

**Verdict**: REVISE. Four findings block (RS-SR1 to RS-SR4). Each is fixed by a few
words of plan text and a test label, not by a redesign.

**In plain terms.** The plan does what the Security Review asked. SR1 to SR6 each
become a criterion or a named disposition, both old privileges are struck, and
the `Called by` rule says plainly that nothing mechanical checks the quote. The
gap is in what the plan **rewrites without pinning**. Four rules that protect
the review apparatus sit in paragraphs this plan rewrites, and no test or
criterion makes them survive:

1. **A Security Review is its own pass; an ordinary review never clears it.**
   The shipped proposal template states this in the `required(A + B)` syntax
   that this plan retires.
2. **The `dual-review` module's sentence that a contract change "gets an External
   review".** The accepted proposal strikes it, but no chunk does, and C7 says to
   keep the module's multi-type content.
3. **The new low-tier row for docstring cleanup.** It says the review "stays at
   the usual stage tier" on high-risk files, but `usual` is now the header word
   for *no* Security Review.
4. **The Maintainer's quote in the commit body.** The accepted proposal required
   it, and W2 leaves it out.

None of these is a hole at the base. Each is a sentence a careful implementer
would probably keep and a hurried one could drop while every criterion stays
green.

### Answers to the six questions

1. **Does every SR item become a criterion or a named disposition?** Yes, with
   two leaks.
   * **SR1.** W2 (lines 419-435) carries all four statements: the read adds and
     replaces nothing; its brief removes no owed answer and discharges no
     Security Review; other authority lives only in a Decision or a plan fence;
     and it never comes from a `Called by` line. C1 pins them as labels and C2
     carries them to the four templates. The module clause is struck in C1,
     the archive-precondition branch and "Tier ordering" in C4, and C8 re-runs
     the probe. **Leaks:** the commit-body copy of the quote (RS-SR4), and
     Revision 1's "a try-to-kill brief narrows the pass to that", which SR1
     flagged and nothing keeps out of doctrine (RS-SR5).
   * **SR2.** Closed by C7 (lines 890-901). It carries both literals, each with
     its own control, globs the presets and `dev/modules/onboarding/`, asserts
     the glob is non-empty, and says which control does not depend on the
     pattern.
   * **SR3.** Closed. The board line is deposited: the opening commit adds 26
     lines to the re-anchor row in `dev/PLANNING.md`. C7 is the last chunk that
     changes test bytes, M is gated on code review, and "owes its own" is
     stated. The `AGENTS.md` correction SR3 asked for has since landed at
     `69d3ac59`, after the reviewed commit, so *Dispositions* item (a) and the
     plan decision at lines 348-352 are now overtaken (RS-SR8).
   * **SR4.** W4 says "different model architecture", says the check is never
     a lifecycle pass, and puts the data-governance gate first. Closed. RS-SR3
     covers the paragraph W4 sits in.
   * **SR5.** W5, the sixth category, and a byte-identical runbook and launcher.
     Closed, except for the record-form conflict in RS-SR5.
   * **SR6.** Closed by a per-chunk baseline diff. Reproduced at
     8cc124b5: `quality_gate.py --sub neutrality` exits 1 with 74 FAIL lines. 18
     of them sit in the five named files (8, 5, 3, 1, 1), and no other file this
     plan edits has one.
2. **Authority leaks after the plan lands:**
   * clearing a Security Review with an ordinary pass: RS-SR1;
   * an agent selecting External: RS-SR2;
   * lowering a review: RS-SR3;
   * an agent reviewing its own implementation: the floor is pinned in both
     `AGENTS.md` copies but not in the plan templates (RS-SR1).

   I found no sentence that lets an agent *call* a Maintainer read on its own.
   W2's never-list and the read rule cover it. The method is set out below.
3. **The `Called by` quote.** The plan names plainly that nothing mechanical
   checks it: W2's last sentence, the label
   `nothing-checks-the-quote-a-reader-does`, and a red-when for any sentence
   that says a tool checks it. A forgery does not pay. Once SR1's four
   statements land, a forged quote buys one extra read and no authority. There
   is one dropped requirement and one cheap hardening (RS-SR4).
4. **The deleted frozen test.** I measured it on the reviewed commit's bytes, in
   a detached worktree with the file removed:
   * `pytest bootstrap/tests/test_gate_manifest.py`: **21 passed** in 22.5 s.
   * `_gate_manifest.py verify`: **exactly six new lines**, one `FROZEN-MISSING`
     and five `COLLECTION-DROPPED` (one per node). These land on a verifier that
     already reports `HOLD -- 154` at the base, so it reads 160 after.

   The plan describes this exactly and does not rely on the suite. What the
   five nodes protected:
   * the non-empty glob, the two literals and the non-vacuity fixture carry
     into the stance test;
   * the "exactly three staffed paragraphs" node retires with its premise;
   * the positive fixture guarded only the old test's own patterns.

   The remaining gap is the window from C7 to M, when that protection lives in
   unfrozen bytes (RS-SR8).
5. **The low-tier rows.** Yes, the wording can leak (RS-SR3).
6. **The install contract is byte-stable**, and the one contract-adjacent edit
   is declared.
   * `scaffold.py --manifest` at 8cc124b5 is 98 lines of `destination`,
     `source` and `verbatim|substituted`, with no content hashes, and the mode
     is set per file in config, not derived from content. No file is added to
     or removed from the install set, so the manifest cannot move.
   * `AGENTS.md` lists the fidelity manifest as install contract. The plan
     edits only its sample `roles:` (`bootstrap/fidelity-check.md:162-167`) and
     declares the edit (lines 217-221; Boundary B reason 1).
   * Its only content reader is `bootstrap/tests/test_scaffold.py:895-900`,
     which pins three substrings. The other mentions, in `cli.py`, `config.py`
     and `check_module_body_coverage.py`, are strings and comments.
   * It is pinned in neither `gate_manifest.json` nor `cairn-lock.yml` (0
     entries each), and no `.py` file reads a role name except two
     review-heading fixtures.
   * Of every file this plan touches, including all of `doctrine/`, `docs/`
     and `dimensions/`, only the deleted test is a `frozen_files` key (183
     keys; control `test_scaffold.py` present). None is in `phase_mutable` or
     `cascade_mutable`.

**How I searched.** I used my own paragraph-level script over the plan's 15
pinned roots: `.md`, `.yml` and `.svg` files, archives excluded, markup
stripped, whitespace collapsed, and blank blockquote lines splitting
paragraphs. A hit is two term sets within 120 characters, at 8cc124b5.

| Probe | Terms | Hits | Known-present control |
|---|---|---|---|
| authority | distance term near waive, exempt, satisfy, clear, substitute, skip, instead of, replace, discharge, confirm | 18 paragraphs, 14 files | all three privileges: "Tier ordering" and the archive-precondition branch in `doctrine/plans.md`, the module clause in both copies |
| Security Review clearing | "security review" near the same verbs, or optional, ordinary, usual | 15, 10 | the plan-obligation sentence in both `AGENTS.md` copies |
| lowering | review near lower, downgrade, downshift, low | 24, 10 | the bright-line and downshift paragraphs in both `model-selection` copies |
| self-review | implement or author near "its own" review, "clears its own", "same agent" | 3, 3 | `doctrine/dual-review.md` "no artifact clears its own obligation" |
| selection | Search B-like | 69, 35 | all five of the plan's Search B controls, and the module paragraph in both copies |

An exact `git grep` over `bootstrap/tests/*.py`, `scripts/` and `tools/` found
no test or tool that pins any of the protective sentences below: "one pass per
clause", "takes a Security Review", `Obligation`, "implementing agent". The
same grep over the templates finds each one, which is the control.

### Findings

**RS-SR1 -- blocking. The rule that only a Security Review clears a Security
Review has no criterion, and its shipped form uses syntax this plan retires.**

* **Proposal templates.** The only shipped statement that each clause of a
  review header needs its own pass is
  `templates/core/dev/proposals/_template.md:54-55` ("A high-risk surface
  takes a Security Review. ... `required(A + B)` means one pass per clause,
  each naming its own obligation"), and `dev/proposals/_template.md:73`. C2
  replaces `required(...)` on the `**Review**:` line with `usual + Security
  Review` (lines 687-690). After C2, nothing says the `+ Security Review`
  clause is a separate pass. Next to "one review at every stage", a reader can
  take one usual pass as covering both.
* **Plans.** The rule that a plan's security obligation is cleared only by a
  matching `**Obligation**` line, "never by an ordinary Internal pass", sits
  in the very paragraph C1 must rewrite to strike the escalation sentence:
  `templates/core/AGENTS.md:99-106` and `AGENTS.md:94-101`.
* **Doctrine.** The matching doctrine section is "Plan review is Internal,
  always", with its obligation paragraph and the "Security Reviews wherever
  they attach" bullet (`doctrine/dual-review.md:241`). C4 strips bullets from
  that same list.
* **The code-review floor.** "Not the implementing agent" is pinned by a C1
  label in `AGENTS.md` only. The two plan-template statements
  (`templates/core/dev/plans/_template.md:39`, `:287`) are rewritten in C2
  with no criterion.
* **No test pins any of these** (grep above), and the C1 label list (lines
  552-575) and the C2 criteria (lines 683-720) carry none of them.

*Fix.*
* Add these labels to C1 (both `AGENTS.md` copies) and C2 (all four
  templates):
  * `a-high-risk-surface-takes-a-security-review`;
  * `usual-plus-security-review-is-two-passes-and-the-usual-pass-never-clears-the-second`;
  * `a-plan-security-obligation-is-cleared-only-by-a-matching-obligation-line`
    (both `AGENTS.md` copies and both plan templates).
* Extend `code-review-floor-is-not-the-implementing-agent` to both plan
  templates, covering the preamble and the Code review skeleton.
* Add a mutant that turns a named node red: delete the two-pass sentence from
  one template copy.
* In C4, add a criterion that the obligation paragraph and the "Security
  Reviews wherever they attach" bullet survive, reworded only as RS-SR6 asks.

**RS-SR2 -- blocking. The module's External-selecting paragraph is assigned to
no chunk, and C7's wording says to keep it.**

* **The paragraph.** `templates/modules/team-gated/dual-review.md:17-23`, and
  `dev/modules/dual-review.md:16-22`, say "A change touching a contract or a
  load-bearing assumption gets an External review in addition to the Internal
  pass ... a human fills the External tier". That is a rule selecting
  distance by risk, in a shipped module. Revision 1's table disposes of it as
  "Struck".
* **The plan's wording.** C7 says the thinned module keeps "what is about
  multi-type teams" (lines 912-915), and the Scope delta row says "The module
  keeps multi-type content" (line 1000). The C7 completeness check accepts any
  file named in an exemption table with a reason (lines 902-906), which the
  plan itself lists as a route to hide a hit (line 1151).
* **The surrounding text.** Line 25 ("make it prove itself"), lines 29-34 and
  120-121 ("The External tier ... layers"), and the opening and closing lines
  (8-11, 150-152, "two-tier ... structurally independent") go the same way.
* **An ambiguity in C1.** C1's forbidden-phrasing group already covers "the
  two module copies" (lines 651-654). If it uses Search A's patterns, C1 is red
  on this paragraph. If it carries only the privilege clause, nothing removes
  the paragraph.

*Fix.*
* C7 names this strike explicitly: the module's External paragraphs give way
  to a pointer to the Maintainer-called read, as Revision 1's table says.
* C7 puts both module copies under every Search A pattern.
* The completeness check forbids an exemption for any file in the install set
  (`templates/`, `dev/modules/`, both `AGENTS.md` copies, both loop documents).
* C1 states that its module group holds only the privilege-clause literal.

**RS-SR3 -- blocking. The low-tier row's "usual stage tier" can lower the review
of a high-risk edit.**

* **The row's wording.** C3 (lines 732-734): docstring and comment cleanup is
  low, "with the clause that its review stays at the usual stage tier wherever
  it touches a surface the project's `AGENTS.md` names as high-risk". After
  this plan, `usual` is the header token meaning *no Security Review* (W2,
  C2).
* **What it means in Cairn.** `AGENTS.md` lists the scaffold engine under
  "High-risk surfaces (Security-Review + proposal triggers)". A docstring
  edit in `bootstrap/_scaffold/` changes the AST attestation hash
  (`bootstrap/tests/_ast_attest.py:84` hashes `ast.dump` of the whole
  definition, docstring included). So the review owed there is a Security
  Review at high. Read with the new vocabulary, the row says a usual review at
  medium.
* **Unreconciled text.** The row also contradicts the bright-line list, "the
  high-risk trust boundaries ... stay at the high floor regardless"
  (`templates/modules/team-gated/model-selection.md:128-131`), and C3 does not
  say how the two are reconciled.
* **The downshift paragraph.** W4 rewrites the paragraph that holds the four
  conditions and the exclusion "does not apply to ... security-sensitive
  changes" (lines 114-126), and nothing pins that those survive.

*Fix.* Quote the row in *Wording the plan fixes* and keep "usual" out of it.
For example:

> **Docstring and comment cleanup may be written at low.** This covers an edit
> that changes only docstrings and comments: no executable token, and no bytes
> that a test, manifest or attestation pins. It lowers the writing step only.
> The review keeps its stage's floor (medium for code review). Where the edit
> touches a surface this project's `AGENTS.md` names as high-risk, it also owes
> the Security Review that surface already requires, at high. Nothing in this
> row lowers a review or removes a Security Review.

Then add two C3 criteria:
* The bright-line list keeps "the high-risk trust boundaries", with one
  clause naming this row as the only exception, and only for the writing step.
* The four downshift conditions and the exclusion list are unchanged apart
  from W4's words.

If the Maintainer meant that *reviews* of cleanup away from high-risk files may
also run at low, the row must say so in words. That is a lowering, and it
should not be left to inference.

**RS-SR4 -- blocking (scope floor). W2 drops the commit-body copy of the
Maintainer's quote.**

* **What dropped.** Revision 1, section 2, says the pass carries the quote
  "and the same quote in the commit body, as for a scribed Decision"
  (`dev/proposals/archive/2026-10-18-claude-external-is-a-maintainer-stance.md:973-975`).
  W2 (lines 421-423) and the label `called-by-carries-the-maintainers-words-verbatim`
  leave it out, and nothing else in the plan restores it.
* **Why it counts.** The Scope delta says "preserved" (line 1046). By
  `AGENTS.md`, removed accepted scope is a deviation.
* **The security value is modest.** The copy sits in a record that cannot
  change without rewriting history, so a later edit to the quote in the pass
  shows without archaeology.
* **Harmless omissions.** W2 also omits "or an equivalent in a header" and
  "head a pass External on its own" from the never-list. The read rule makes
  both harmless, so this is noted only.

*Fix.*
* Restore the commit-body phrase in W2 and in the label.
* As cheap hardening, have the line say where the words live:
  `**Called by**: Maintainer -- Decision at <commit>` or `-- chat, <date>`, plus
  `, relayed by <who>` where it was relayed. A quote taken from a Decision is
  then checkable against a committed block by the next reader. A quote taken
  from chat stays a reader's trust, as W2 already says.

**RS-SR5 -- non-blocking. W2 and W5 disagree about the launcher's "External
Security review".**

* **The conflict.** W2 makes `**Tier**: External` valid only with `Called by`,
  reads anything else as the usual review, and says a called read "discharges
  no Security Review". W5 keeps the runbook's "External Security review" of
  the launcher as the one standing call. The Maintainer verifies the launcher
  against "the review's record" (`bootstrap/REANCHOR_RUNBOOK.md:48`).
* **What a literal reader gets.** The next launcher review's record either
  needs a `Called by` line, which W5 never mentions, or reads as a usual review,
  that is, not a Security review. And W2 says a Security Review the Maintainer
  calls from more distance clears nothing.
* **An unguarded phrase.** Revision 1 section 2's "a try-to-kill brief narrows
  the pass to that" (proposal line 984), the phrase SR1 objected to, has no
  guard if C4 carries section 2 into doctrine.

*Fix.*
* W5 adds: "Its record carries `**Called by**` with the Maintainer's
  commissioning words, and it is a Security Review."
* W2's clause becomes "discharges no Security Review by its distance or its
  brief; a pass clears a Security Review only by being one".
* `narrows the pass` reads 0 in doctrine after C4.
* The runbook stays untouched.

**RS-SR6 -- non-blocking. The paragraphs being rewritten credit the security
obligation to a checker that no longer exists, and one doctrine page names the
wrong satisfier.**

* **The checker named.**
  * `AGENTS.md:101` and `templates/core/AGENTS.md:106` say "never by a heading
    the checker cannot parse".
  * `doctrine/dual-review.md:223` and `:228` name `_pass_headings` and
    `normalize_required_obligations`.
  * `doctrine/lifecycle-contract.md:158` says "the checker reads as two
    distinct passes".
* **Measured: no such checker.** In `*.py`, those two names appear only in a
  comment (`scripts/gen_legacy_passes.py:16`). `Obligation` appears in no
  `.py` or `.sh` file; the control finds it in 3 `.md` files.
* **The wrong satisfier.** `doctrine/lifecycle.md:313-314` says the plan
  obligation is "satisfied only by an appended `## Security review (Internal)`
  record". `doctrine/plans.md:643` and the `dual-review` paragraph say such a
  heading carries no weight.
* **These are all in scope.** C1 and C4 rewrite each of these paragraphs, and
  my selection probe hits the `lifecycle.md` one.
* **Why it matters.** `AGENTS.md` > "Verifying claims" calls a described check
  that tests nothing worse than no check. W2 already sets the honest
  standard for `Called by`.

*Fix.*
* Say the same for the `Obligation` line: no tool reads it; the next
  reviewer, the code reviewer and the Maintainer do.
* Conform `lifecycle.md` to `plans.md`.
* After C4, a grep for `_pass_headings|normalize_required_obligations|the
  checker cannot parse` over live docs reads 0, or each hit is marked as
  history.

**RS-SR7 -- non-blocking. C1's module edit moves the lockfile count that C3 says
holds.**

* **Measured on a copy of 8cc124b5.** Striking the privilege clause from
  `dev/modules/dual-review.md` takes `verify_integrity.py --target .` from 18
  to **19**, and the new entry is that file.
* **Why C3 goes red.** The plan finalizes that record only at C7 (lines
  939-940), but C3 requires "still reports 18" (line 768), so C3 is red as
  written. A red integrity count that "everyone knows about" is the habit of
  routing around a refusal, and an unscoped finalize to fix the number would
  re-attest the 18 drifted files (lines 225-227).

*Fix.* C1 scoped-finalizes `dev/modules/dual-review.md` in the same commit,
C7 finalizes it again, and the count reads 18 at every chunk.

**RS-SR8 -- non-blocking. The window between C7 and the re-anchor, and a stale
disposition.**

* **What reaches the ceremony.** The re-anchor pins whatever is tracked when it
  runs. The row says "derive the changed set ... at ceremony time". From C1
  to M, the three test files that inherit the old pin's protection are
  unfrozen. The archive note records their node IDs (lines 1170-1172), and
  node IDs do not detect a change of bytes.
* **The stale disposition.** The `AGENTS.md` pitfall sentence was corrected at
  `69d3ac59` (Cairn's root copy only).

*Fix.*
* The archive note records the git blob id of each of the three test files at
  the code-reviewed commit (`git ls-tree <sha> -- <paths>`), and the row asks
  the ceremony to confirm it pins those bytes.
* Drop *Dispositions* item (a) and the plan decision at lines 348-352, or
  restate them as closed by `69d3ac59`, the next time the plan's operative
  cells are revised.

### What I did not cover

* I did not run the full suite or the plan's 22-file mapped set. My suite
  evidence is `test_gate_manifest.py` only, run once with the file deleted.
* I did not rebuild Searches A and B to the plan's exact patterns. My probes
  are lexical with their own terms and a 120-character window, so a privilege
  phrased without them escapes. My selection probe's 69 paragraphs in 35
  files and the plan's 61 in 30 are not reconciled.
* I did not read `docs/`, `dimensions/`, the presets, `bootstrap/UPGRADE.md`
  or the README in full, or the 2026-08-27 launcher review record.
* The two new tests do not exist, so their controls and mutants are judged
  by design only.
* I did not run the adopter rehearsal, the AST verifier or the body-coverage
  probe.
* I left scope, simplicity, sequencing with plans C and D, and RL1 to RL7 to
  the ordinary Internal pass, except where they touch the trust apparatus.
* I read the work at 8cc124b5. Later commits are named only where they
  overtake a plan statement (`69d3ac59`).
