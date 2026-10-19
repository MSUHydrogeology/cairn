# Plan: review stance and lenses — one review at every stage, and the lenses in every install

**Source proposal**: `dev/proposals/archive/2026-10-18-claude-external-is-a-maintainer-stance.md` (accepted `58f30d6c`) and `dev/proposals/archive/2026-10-18-claude-review-lenses-for-every-install.md` (accepted `fbf664f0`)
**Status**: awaiting-code-review
**Plan review**: required(Internal + Internal Security Review)
**Assurance path**: high-assurance — inherited: the change edits `doctrine/`, the governing `AGENTS.md` every adopter receives, the authoring templates and a framework anchor.
**Opened**: 2026-10-18

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

**What it touches.** 54 prose files (the two `AGENTS.md` copies, the review-loop
document, four authoring templates, three modules, three onboarding presets,
eleven doctrine files, four `dimensions/` files, the README and its figure, eight
docs pages with two installed copies, two more shipped pages, and two bootstrap
pages), two new tests, one old test retired. **No
engine file changes**, so there is no AST impact and the published install
manifest does not move.

**Order of work.** Shipped text first, because adopters receive it and never
receive `doctrine/`: the two carrier documents (C1), the authoring templates
(C2), the roster, capability floors and remaining shipped text (C3). Then the
doctrine that stands behind them (C4), the dimensions (C5), the README, figure
and docs (C6). Last the things that retire something: the old pin and the
module's duplicate text (C7). Then one full test run (C8). **Implementation is
sequential:** it starts once plans C and D have each reached
`awaiting-code-review`, so no two plans' commits interleave.

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
| Collaboration agreement pair, `model-selection` pair, `security-review` pair, legacy profile, session-start skill pair, fidelity manifest sample, `templates/modules/README.md`, `templates/optional/CONTRIBUTING.md` | 12 | C3 |
| Doctrine: `dual-review`, `plans`, `proposals`, `roles`, `rationale`, `lifecycle`, `lifecycle-contract`, `session-routines`, `onboarding`, `README`, `doc-governance` | 11 | C4 |
| `dimensions/` (four) and `bootstrap/UPGRADE.md` | 5 | C5 |
| `README.md`, the figure, eight docs pages (`glossary`, `vision`, `agent-team-onboarding`, `quickstart`, `workflow-role`, `getting-started`, `dev-tour`, `tool-usage`), and the installed copies of `agent-team-onboarding` and `dev-tour` under `dev/modules/onboarding/` (byte copies of those pages; both ship to adopters) | 12 | C6 |
| Three onboarding presets, the one installed preset copy (`dev/modules/onboarding/collaborative-team.md`), the `dual-review` module pair | 6 | C7 |
| Tests: create `bootstrap/tests/test_review_stance_in_shipped_files.py` and `bootstrap/tests/test_review_sweep_ships.py`; reword `test_review_and_verification_rules_ship.py`; delete `test_onboarding_review_tiers.py` | 4 | C1, C7 |

The list is the proposals' known set. **The searches below are the authority,
not this list.** A file with no hit and nothing that selects distance stays
untouched, and the record says so (the proposal's `doctrine/proposals.md` and
`doctrine/lifecycle.md` are likely cases). A hit in a file not listed, such as
`doctrine/onboarding.md`, is classified and fixed where it falls. Search D
(below) adds four files the proposals' list does not name: `doctrine/README.md`
and `doctrine/doc-governance.md` (C4), `templates/modules/README.md` and
`templates/optional/CONTRIBUTING.md` (C3), the last an opt-in file adopters
receive.

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
* **Search D, the old description.** The two searches above find rules that
  *pick* a more distant reviewer. The headline the Maintainer approved also
  removes the old *description* ("two-tier", "a structurally-independent tier"),
  which they do not reach. Same roots and stripping, paragraphs Search A does not
  already match: `two[- ]tiers?|two review tiers|single tier|structural(ly)?[- ]independen|Internal (tier|review|pass|Reviewer)`.
  Rebuilt, it gives **57 paragraphs in 29 files** (the plan reviewer's own build
  gave 63 in 33; the readings differ and are not reconciled, so the implementing
  agent commits the script text like Search B's). Control: it finds anchor 4's
  "Two-tier review" in `doctrine/rationale.md` and the README's alt text. Besides
  files already in the list it reaches `doctrine/README.md`,
  `doctrine/doc-governance.md`, `templates/modules/README.md`,
  `templates/optional/CONTRIBUTING.md`, `docs/DOCUMENTATION_PLAN.md` and
  `templates/modules/default-on/documentation_plan_template.md`; each is
  classified, and fixed where it states the old description as current.
* **The authority probe** (Security Review). A distance term near *waive,
  exempt, satisfy, clear, substitute, skip or instead of*, per paragraph. The
  review reported 18 hits; rebuilt, it gives **17 in 11 files**. The criterion is
  not the count. It is that the two privileges named below are gone and every
  remaining hit is classified.

**Classification.** Every hit of A, B and D ends in one of nine categories (D adds
the last two: a *stale description* to reword, and a *ruled plan-review token*,
since `Plan review: required(Internal)` keeps its tokens). For A and B, seven: the
Maintainer-called definition; a staffing fact; a credit comment; a marked
history reference; noise (`External-repo`, external links); the standing
launcher-review call (SR5, the sixth category the Security Review asked for); or
the cost-rule carve-out (the `model-selection` downshift condition). The
proposal's list names five and the table row decides the downshift, so the
seventh is made explicit here. No file in the install set (`templates/`,
`dev/modules/`, both `AGENTS.md` copies, both loop documents) may be exempted from
the completeness check in C7 on the strength of a category. Category membership is a reader's judgment; the
checks are that **every hit is classified** and that the code reviewer re-runs
both searches on the reviewed commit.

### Frozen files, AST, install contract, lockfile

**Frozen files: one, and it is a deletion.** `bootstrap/tests/test_onboarding_review_tiers.py`
(five pinned nodes) is retired in C7. Measured: `frozen_files` holds 183 keys at
`f804f3b7`; none of the 54 prose files is a key; the instrument was checked
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
  another re-anchor. Chunk M is gated on exactly that. Node IDs do not detect a
  change of bytes, so the archive note also records the git blob id of each of the
  three files at the code-reviewed commit (`git ls-tree <sha> -- <paths>`), and
  the board row asks the ceremony to confirm it pins those bytes.
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
stays 18 at every chunk. That includes C1, which strikes a clause from
`dev/modules/dual-review.md`: measured on a copy of the opening commit, that one
edit takes the count from 18 to 19, so C1 finalizes the record in the same
commit and C7 finalizes it again. An unscoped finalize is never the fix: it would
re-attest the 18 drifted files. The lockfile schema is untouched.

**Vendor-neutrality (SR6).** `python scripts/quality_gate.py --sub neutrality`
exits 1 with **74** FAIL lines (21 info) at the base. Eighteen of them sit in five
files this plan edits: `docs/agent-team-onboarding.md` 8,
`doctrine/lifecycle-contract.md` 5, `doctrine/rationale.md` 3,
`templates/onboarding/solo-greenfield.md` 1,
`templates/skills/session-start/SKILL.md` 1. Plan C
zeroes the gate, and this plan starts only after plan C has reached
`awaiting-code-review`, so the expected baseline at C1's parent is **zero and the
criterion is "stays zero"**: a new failure is this plan's. Check the figure at
C1's parent. If it is not zero, fall back: a bare "it passes" cannot be the
check, so each chunk records the FAIL lines for its edited files at its parent
and requires **no new line** afterwards, matching by file, token and line text
(line numbers move). Rewording the credit line in
`solo-greenfield.md` also clears the one collision the Security Review found in
its test pattern; plan C rewords it first, and C7 does it only if it is still
there.

### Sequencing with the other work

The accepted work around this plan: `neutrality-and-upgrade-slots` (plan C),
`independent-scientific-check` (plan D), `model-mapping-install-path` and
`board-as-basis` (accepted, no plan yet), and `stewardship-and-reuse` (a
proposal, issue #30). Plans C and D each list *this* plan last, after
`model-mapping-install-path` and `board-as-basis`; the order recommended below is
this plan's advice for the Maintainer's board, which is his to set, and changes
neither list. Plans C and D have had their plan reviews (`0389a14e`, `d7fe5d6a`,
both REVISE, since folded; C is implementing and D is `ready-to-implement`), so
every chunk here re-reads the files it edits at edit time. Files shared, read from
each one's own text at `f804f3b7`; the rows that bind are `solo-greenfield.md`,
the marker lines in three files, the old pin's ordering with C, D's template cells
and Complexity cell, and the lens-5 anchors:

| Other work | Files shared with this plan | What each edits | Effect |
|---|---|---|---|
| **C: `neutrality-and-upgrade-slots`** | `templates/onboarding/solo-greenfield.md` | C rewords the credit line (its C5); this plan rewords the External-tier paragraphs (C7) | C first: this plan finds the line reworded and compares against zero |
| | `templates/skills/session-start/SKILL.md` and `.agents/skills/session-start/SKILL.md` | one phrase near the top (its C2); this plan changes "review tier, plan-review tier" in the board paragraph (C3) | different sentences; the twins stay byte-identical |
| | `doctrine/rationale.md`, `doctrine/lifecycle-contract.md`, `docs/agent-team-onboarding.md` | same-line `vendor-ok` markers on hit lines (its C6); this plan rewrites the anchor, wording and examples | a marked line this plan rewrites keeps or drops its marker on purpose, and the gate says which; `dev/modules/onboarding/agent-team-onboarding.md` is a `cmp`-identical copy of the docs page, so a marker added to one must reach the other and C6 keeps the pair equal |
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
  a 54-file change, for a gain (reviewing two nearly finished plans under the new
  stance) that is small.
* **Against going last**, the later plans' overlaps with this one are small and in
  different sections (table above), so nothing is saved by waiting, and the three
  heaviest reviews would run under rules that are about to change.
* **Implementation is sequential; the slot stays third.** C1's files overlap
  neither plan C nor plan D (both list `AGENTS.md` as not touched), so a rebase is
  not what holds it back. The reason to wait is that every plan commits to the same
  `master`: interleaving this plan's commits with C's or D's would make each plan's
  Boundary B tested range, and each code review's range, ambiguous. So **C1 starts
  once plan C and plan D have each reached `awaiting-code-review` or later**, and
  the later chunks follow C1 in order. A `revising-code` commit from C or D that
  lands while this plan is implementing is listed by SHA in the Boundary B record
  as outside this plan's range. The cost is that every session until C1 lands
  reads today's text, which still says an External code review is an escalation;
  nothing ships until the Maintainer pushes. Plan review ran alongside C's and D's
  implementation, which is allowed because a review writes only its own section.

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
* **`AGENTS.md`'s pitfall sentence is already corrected.** The Security Review
  found that the operational pitfall about a deleted frozen file ("fails loudly
  ... reddens this file") was wrong for the suite and said it needed its own
  correction, separate from this change. That landed at `69d3ac59` (Cairn's root
  `AGENTS.md` only; the shipped template has no such bullet). This plan neither
  edits it nor relies on the old wording.
* **Search D and four more files.** The plan reviewer showed that the approved
  headline removes a description as well as a rule, and that the two searches see
  only the rule. Search D is added with the same classification, and the four files
  it names are placed in C3 and C4. This widens verification and the file list; no
  accepted outcome moves.

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
lines. **Chunks run in order, and none starts before plans C and D have each
reached `awaiting-code-review` or later** (*Recommended slot*); the gates below
add only what is specific to a chunk.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | **The carriers.** The one stance, the three stage questions, the Maintainer-called read (with SR1's four statements), the reviewer roster, and **the review sweep** (lenses, scope sentence, citation rule, coverage line, floor, project probes, the single ledger) land together in `templates/core/AGENTS.md`, `AGENTS.md`, `templates/core/dev/agent_collaboration.md` and `dev/agent_collaboration.md`. The pointer goes in both `AGENTS.md` files. The privilege clause leaves both module copies, with a scoped lockfile finalize of `dev/modules/dual-review.md`. Creates both new tests (carrier groups, the real-install group) and rewords the unpinned rules test. | `ready-to-implement`; plans C and D each at `awaiting-code-review` or later | one commit |
| C2 | **The authoring templates.** Review preamble, header grammar (`usual`, `usual + Security Review`; `**Tier**:` values; External only with `**Called by**`), the Plan review and Code review skeletons with their Foundations questions, the called-read statements, the two-pass and obligation-line sentences. No coverage-line stanza. | C1; re-read each file at edit time | one commit |
| C3 | **Roster, floors and the rest of the shipped text.** Collaboration agreement pair, `model-selection` pair (stage rows, the low row, the cost-rule carve-out), `security-review` pair, legacy profile, session-start skill pair, fidelity manifest sample, `templates/modules/README.md`, `templates/optional/CONTRIBUTING.md`. Two scoped lockfile finalizes. | C1 | one commit |
| C4 | **Doctrine.** The eleven doctrine files, the two privilege strikes, the launcher-call sentence, the verbatim anchor, the Boundary C opening, the lenses' two doctrine edits, the checker-that-does-not-exist conformed. Appends the search classification. | C1 to C3 | one commit |
| C5 | **Dimensions and the plan-pass schema rows.** Complexity positions, the axis row, the team axes, `bootstrap/UPGRADE.md`. | C4 | one commit |
| C6 | **The headline.** README, the redrawn figure, the docs pages and the two installed copies. | C4 | one commit |
| C7 | **Retire and thin.** Three presets and the installed preset copy reworded; `test_onboarding_review_tiers.py` deleted; the stance test's preset group and completeness check; the module pair thinned, its External paragraphs replaced by a pointer; the sweep test's module group; a scoped finalize. The last chunk that changes test bytes. | C1 to C6 | up to two commits, in that order |
| C8 | **Boundary B, then the record.** One full run on the finished work, written down (*Verification*), with the adopter rehearsal. Status to `awaiting-code-review`. | C7 | one commit |
| M | **MAINTAINER-ONLY — no new ceremony.** The *re-anchor* is the supervised ceremony, run only by the Maintainer, that brings the gate manifest up to date with changed tests (`bootstrap/REANCHOR_RUNBOOK.md`). The deletion of `test_onboarding_review_tiers.py`, the two new test files and the reworded unpinned one join the row already queued on `dev/PLANNING.md`, so M needs no Waiting line in this plan: that row declares the wait. **Gate: code review cleared and every `revising-code` commit landed, so no test byte can change afterwards; the archive note then records the blob id of each of the three test files and asks the ceremony to confirm it pins those bytes.** If the batch runs before C7, this change owes its own. **An implementing agent must not perform it.** The agent's part is the board note at archive. | code review cleared | Maintainer |

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

**W2. The Maintainer-called read**, for the shipped `AGENTS.md` and the four
templates. Four short bullets, one rule each; every label in C1 and C2 maps to a
bullet. It does not spell the header value the forbidden-phrasing group forbids,
and it avoids "External ... by default" in any form, which the unpinned rules
test forbids:

> **More distance is the Maintainer's call, and only theirs.**
>
> * **What it is.** An *External read* is a review the Maintainer asked for on one
>   named artifact that exists now, in chat or inside a Decision, outside the usual
>   procedure. A call that covers artifacts not yet written is a standing floor (a
>   rule that applies without being asked), and a standing floor returns only by
>   proposal. A roster the Maintainer sets in `dev/collaboration_agreement.md`
>   (which agent types work the tree) is the team's shape, not a call: it adds no
>   read and upgrades none. Distance is information, not a rule: a different agent
>   type has different failure modes and a person has different knowledge. The
>   staffing reviewer follows the Maintainer's brief, answers the same three
>   questions from that distance, and says so.
> * **How it is recorded.** The pass carries `**Called by**: Maintainer -- Decision
>   at <commit>` (or `-- chat, <date>`, with `, relayed by <who>` where it was
>   relayed), followed by the Maintainer's words, verbatim and set apart. The same
>   words go in the commit message, as for a scribed Decision. `**Tier**: External`
>   is valid only with that line, and a pass headed External without it is read as
>   the usual review.
> * **What an agent never does.** Declare External as a required review in a
>   header, say a change needs one, recommend more distance, head a pass External
>   on its own, or start one without those words. It may name a risk and a gap in
>   its coverage line.
> * **What a called read never does to the other reviews.** It adds to the usual
>   review and replaces nothing. Its brief may add focus; it removes no owed
>   answer, and it discharges no Security Review by its distance or its brief (a
>   pass clears a Security Review only by being one). Any other authority in the
>   quoted words, such as a waiver or a change of scope, takes effect only where
>   Maintainer authorizations already live, a Decision block or a plan's fence, and
>   never from a `Called by` line. Nothing checks the quote mechanically, in the
>   pass or in the commit message: the next reviewer and the Maintainer at the
>   Decision are the check.

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

**W5. The surviving standing call** (SR5), one passage in `doctrine/dual-review.md`
beside the Maintainer-called definition:

> **One standing call survives, and it is the Maintainer's.** The re-anchor
> ceremony (`bootstrap/REANCHOR_RUNBOOK.md`) requires its launcher to be read by
> an External Security review. The ceremony's own record sets that requirement,
> the Maintainer chooses the reader each time, and no agent selects or
> substitutes for it. That review's record carries `**Called by**` with the
> Maintainer's commissioning words, and it is a Security Review: it clears the
> launcher obligation by being one, not by its distance. Nothing else in the
> procedure works this way.

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

**W9. The low row for cleanup** (the Maintainer's "docstrings cleanup and related
should go to low"), in the `model-selection` pair and `doctrine/roles.md`. It keeps
the word "usual" out, because `usual` is now the header token meaning no Security
Review. I read the scribe's "its review stays at the usual tier wherever it touches
a high-risk file" as: a review is never lowered, and a high-risk surface still owes
its Security Review. The row lowers the writing step only. The Maintainer confirmed
this reading on 2026-10-18, verbatim: "Just keep reviews at the same level always
unless Security". So no review of cleanup runs at low, on any file:

> **Docstring and comment cleanup, and related edits, may be written at low.**
> This covers an edit that changes only docstrings, comments and other
> non-executable wording: no executable token, and no bytes that a test, manifest
> or attestation pins. It lowers the writing step only. The review keeps its
> stage's floor (medium for code review), and where the edit touches a surface
> this project's `AGENTS.md` names as high-risk it also owes the Security Review
> that surface already requires, at high. Nothing in this row lowers a review or
> removes a Security Review.

**W10. The plan security obligation** (`AGENTS.md` pair and both plan templates),
replacing "never by a heading the checker cannot parse", which credits a checker
that does not exist:

> A plan whose surface calls for security treatment declares `Plan review:
> required(Internal + Internal Security Review)`. Only an appended `## Plan review`
> pass whose `**Obligation**` line matches clears it, never an ordinary Internal
> pass. No tool reads that line: the next reviewer, the code reviewer and the
> Maintainer check it.

**W11. The two-pass rule** (`AGENTS.md` pair and both proposal templates),
replacing the `required(A + B)` sentence that this plan retires:

> A high-risk surface takes a Security Review. `usual + Security Review` in a
> header means two passes: the usual pass and a Security Review pass that names its
> own obligation. The usual pass never clears the second.

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
* **Neutrality** (SR6): `python scripts/quality_gate.py --sub neutrality` reads
  zero at C1's parent (plan C has zeroed it) and stays zero. If it does not read
  zero there, the fallback is the baseline diff: the FAIL lines for the chunk's
  edited files at its parent, then at its commit, matched by file, token and line
  text. *Red when:* a failure appears that was not there.
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
  `a-clean-code-review-shows-a-falsification-ledger`;
  `code-review-never-reopens-the-decision`. *Red when:* any label is absent from
  either copy.
* **The Security Review stays its own pass** (W10, W11). Both copies carry the
  labels `a-high-risk-surface-takes-a-security-review`;
  `usual-plus-security-review-is-two-passes-and-the-usual-pass-never-clears-the-second`;
  `a-plan-security-obligation-is-cleared-only-by-a-matching-obligation-line`; and
  `no-tool-reads-the-obligation-line-a-reader-does`. The words "the checker cannot
  parse" are gone from both copies: no checker reads the line, and the text says
  who does. *Red when:* a label is absent, or a sentence credits a tool with
  checking the `Obligation` line.
* **The Maintainer-called read is stated, with SR1's four statements.** Both
  copies carry the sixteen labels, one or more per W2 bullet:
  *what it is*: `external-means-the-maintainer-called-it`;
  `a-call-names-one-artifact-that-exists-now`;
  `a-standing-call-is-a-floor-and-returns-only-by-proposal`;
  `a-roster-you-set-is-not-a-call`;
  `distance-is-information-and-the-staffing-reviewer-follows-the-brief-and-says-so`;
  *how it is recorded*: `called-by-carries-the-maintainers-words-verbatim`;
  `called-by-quote-is-repeated-in-the-commit-body`;
  `called-by-names-where-the-words-live`;
  `tier-external-needs-called-by-else-read-as-the-usual-review`;
  *what an agent never does*:
  `no-agent-declares-external-required-or-recommends-distance`;
  *what a called read never does to the other reviews*:
  `a-called-read-adds-and-replaces-nothing`;
  `a-called-brief-adds-focus-and-removes-no-owed-answer`;
  `a-called-read-discharges-no-security-review-by-distance-or-brief`;
  `other-authority-lives-in-a-decision-or-a-plan-fence`;
  `a-called-by-line-never-confers-authority`;
  `nothing-checks-the-quote-a-reader-does`. The shipped text agrees with W2 and
  implies no tool, hook or gate validates the quote, in the pass or in the commit
  message. *Red when:* a label is absent, or a sentence says a tool checks
  `Called by`.
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
* **Size is bounded and recorded.** The sweep adds 85 to 95 lines to the loop
  document (152 to about 240); each pointer is about 7 lines. **`AGENTS.md` grows
  by at most 40 lines net per copy** over the whole file (`templates/core/AGENTS.md`
  419 and `AGENTS.md` 438 at the base), counting the stance block, W2, W3, W10 and
  W11 and netting out the lines they replace: the Internal and External bullets,
  the "A tier is a stance" paragraph, the plan-review paragraph's escalation
  sentence and the `structural independence` phrases. Both files are read at every
  session start, and the Maintainer asked to keep them lean. Outside a range or
  the ceiling is a signal with a sentence in the commit body, not a failure of the
  chunk; the figures are recorded before and after.
* **The privilege clause is struck from the module, and only that.** "Or is
  confirmed by a second independent different-agent-type pass" is gone from both
  module copies. C1's module group in the stance test holds this one literal and
  nothing wider: the module's External paragraphs stay until C7, and C1 must not
  be red on them. `dev/modules/dual-review.md` is scoped-finalized in the same
  commit and `verify_integrity.py --target .` reads 18 (it reads 19 without the
  finalize). *Red when:* the clause survives in either copy, the count is not 18,
  or the group is wider than the literal.
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
  above, with a forbidden-phrasing group for the four carrier files (and, for the
  two module copies, the privilege-clause literal only), each pattern shown to match its pre-change string and to fire
  when the string is inserted into a copy. The sweep test pins the install
  results above and the same obligations over the four source surfaces. Patterns
  are literals, not derived from the files they check. Mutants, each beside an
  unmutated control, each of which must turn a named node red: delete lens 4 from
  a template copy; delete the "Not covered" half; delete the scope sentence;
  delete the sentence that `Called by` never confers authority; delete the
  plan-obligation sentence (W10) from one `AGENTS.md` copy; add
  `required(External)` to a carrier copy. Because W2 does not spell that
  string, the unmutated control is green. *Red when:* any mutant survives, or the
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
  Foundations block, improve-means-recommend, and W2 (all sixteen called-read
  labels). They also carry W11 (proposal templates) and W10 (plan templates) with
  their labels, and `code-review-floor-is-not-the-implementing-agent` in both plan
  templates, in the preamble and in the Code review skeleton. *Red when:* a label
  is missing from any of the four, or the two-pass or obligation sentence is
  absent from its templates.
* **Header grammar.** The proposal templates' `**Review**:` line offers `usual`
  and `usual + Security Review` and no other value; the pass skeleton's
  `**Tier**:` offers `usual | Security Review`, plus External only beside a
  `**Called by**` line. `required(External)` appears in none of the four. The
  `**Plan review**:` line keeps its ruled tokens, `required(Internal)` and
  `required(Internal + Internal Security Review)`, and the plan-pass skeleton keeps
  `<Internal | Internal Security Review>`. The skeleton shows the line as
  `**Called by**: Maintainer -- Decision at <commit>`. The word "standard" is not
  used as a token (it collides with the lifecycle's "standard lane"). *Red when:*
  an old value is offered, a ruled token changes, "standard" appears as a value, or
  the skeleton omits where the words live.
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
* **Plan D's cells are untouched.** Plan D has landed before C1 starts, so its
  test file (the scientific-check guidance pin) passes unedited, and the added lines of C2 do not
  fall inside the block D adds to the proposal templates or the paragraph D adds to
  the plan templates' *Acceptance criteria*. *Red when:* D's test fails or a C2 hunk
  overlaps its cells.
* The stance test gains the template group (obligations and forbidden
  phrasings) with the same controls as C1, and two more mutants, each beside an
  unmutated control and each turning a named node red: delete the two-pass
  sentence (W11) from one proposal-template copy; delete the obligation sentence
  (W10) from one plan-template copy.

### C3 — Roster, floors and the rest of the shipped text

* **The collaboration agreement pair** no longer says External is a read from a
  different agent type or "makes it prove it should land" at an External tier;
  Cairn's roster slot says the team's shape and nothing about earned
  independence. *Red when:* Search A or B finds the old sentences.
* **Capability floors by stage** in both `model-selection` copies: rows for
  proposal review (high; the premise is still movable and a wrong one is cheapest
  to catch here), plan review (medium), code review (medium; floor "not the
  implementing agent"), Security Review (high); the "External Review" and
  "Internal Review" rows are gone. **The row for docstring and
  comment cleanup, and related edits, is W9**, quoted: low for the writing step,
  the review keeps its stage's floor, a high-risk surface still owes its Security
  Review, and the word "usual" is not in it. The bright-line list keeps "the
  high-risk trust boundaries" with one clause naming this row as the only
  exception, and only for the writing step; the four downshift conditions and the
  exclusion list ("does not apply to ... security-sensitive changes") are
  unchanged apart from W4's words. "Adversarial premise-checking" reads
  "premise-checking" (`grep -c 'adversarial premise'` is 0 in both copies;
  `doctrine/roles.md` is C4's). The pair is byte-identical. *Red when:* an old row
  or "adversarial premise-checking" remains, the row says "usual", the bright-line
  list or an exclusion is lost, or the copies differ.
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
* **Two more shipped pages (Search D).** `templates/modules/README.md` no longer
  says the module "adds the second, structurally-independent tier", and
  `templates/optional/CONTRIBUTING.md` no longer says every substantive change is
  "reviewed across structural independence" (an opt-in file adopters receive).
  Each says what is now true: an independent reviewer beside the author. *Red
  when:* either states the old description as current.
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
  **W5** and **W6** are present; the obligation paragraph and the "Security Reviews
  wherever they attach" bullet of "Plan review is Internal, always" **survive**,
  reworded only to drop the checker names (below); the "Domain rotation" bullet and
  the minimal-team lines are staffing facts, none reading as independence earned or
  a read added; "a try-to-kill brief narrows the pass to that" is not carried (the
  phrase `narrows the pass` reads 0 in `doctrine/`); "Adaptation" says the sweep and the trap
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
* **No checker is credited that does not exist.** After C4 and C1, a grep for
  `_pass_headings|normalize_required_obligations|the checker cannot parse` over
  live documents (archives and records excluded) reads 0, or each hit is marked as
  history; in `*.py` those names appear only in a comment in
  `scripts/gen_legacy_passes.py`, which is not edited. `doctrine/lifecycle.md` no
  longer says a plan obligation is satisfied by a `## Security review (Internal)`
  record; it agrees with `doctrine/plans.md` that only an appended `## Plan review`
  pass whose `**Obligation**` line matches clears it. *Red when:* a hit survives
  unmarked, or `lifecycle.md` still names the other heading.
* **`doctrine/roles.md`.** One Reviewer role carries the briefing duty; "External
  Reviewer" leaves; "A Reviewer tier" and its "pick the tier from the change's
  risk" go; capability floors are the four stage rows plus the low cleanup row;
  W4 and W9 are present; "Diversity within tier" is reworded;
  `grep -c 'adversarial premise' doctrine/roles.md` is 0 (it is 1 at the base).
  *Red when:* any of those survives.
* **`doctrine/rationale.md`.** Anchor 4 equals W7 byte for byte after whitespace
  collapse (compare against the proposal's block); the name "Dual-Review" and the
  module id are unchanged. Search C: every `external` and `independen` hit in this
  file and in `doctrine/lifecycle.md` is read and classified. *Red when:* the
  anchor differs, or a hit is unclassified.
* **Two more doctrine pages (Search D).** `doctrine/README.md` ("the two-tier
  model and structural independence") and `doctrine/doc-governance.md` ("the review
  tiers and structural-independence floors") describe the review as it is now.
  *Red when:* either states the old description as current.
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
  from it. Search D's hits are in it too, as *stale description*, *history*,
  *staffing fact* or *ruled plan-review token*.
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
  assumptions it touches, and the independent scientific check. **Plan D has
  landed before any chunk here starts (the plan-level gate), so the sentence uses
  D's wording and points at the block D adds to the proposal template.** *Red when:*
  "reserved" or "mandatory" survives, or the check is not named.
* **`dimensions/README.md`.** The Complexity cell reads "review weight and
  verification depth" and keeps a mention of the check (plan D asks for it); the
  minimal-team sentence is a staffing fact. **`dimensions/agent-team.md` and
  `dimensions/human-team.md`** say who is available to be the one reviewer, not
  that an External tier is filled. The team-gated bullet that reads "the full
  two-tier Dual-Review apparatus with structural-independence floors" says what the
  module now adds (staffing guidance for a called read, and the trap) with no
  "tier". *Red when:* any still says a tier is "wanted", "filled" or "mandatory", or
  the "two-tier" bullet survives.
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
  line numbers still hold (they do at `f804f3b7`). **The "Lines 53-54" span is a
  sentence, not two whole lines:** the paragraph reads "Two things differ, and both
  favour the code case. Independence is easier to establish — ... 'no recent
  co-authorship.' And review happens ...", and W8's sentence replaces only the
  sentence from "Independence is easier to establish" through
  `co-authorship."`; the lead-in sentence and "And review happens ..." stay. The
  other five spans are whole lines or bullets. Search C: every `external`,
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
  `**N unfilled block slots**`) with N still true. The glossary's Dual-Review
  entry, `docs/vision.md` and `docs/workflow-role.md` no longer say "two-tier"
  (Search D); `dimensions/` is C5's. **The two installed copies**
  (`dev/modules/onboarding/agent-team-onboarding.md` and
  `dev/modules/onboarding/dev-tour.md`) are `cmp`-equal to their pages after the
  chunk, as they are today; both pages reach every install that selects a preset.
  *Red when:* the quickstart test fails, the redundancy gate fails, a page still
  states the old floor or the old description, or a copy differs from its page.
* `python scripts/check_cairn.py` on README and each docs page resolves every link
  and anchor, including the image path. *Red when:* a link breaks.

### C7 — Retire and thin

* **The presets stop saying anyone fills an External tier.** The three
  `templates/onboarding/*.md` presets and the one installed preset copy,
  `dev/modules/onboarding/collaborative-team.md` (which also differs from its
  template by conditionals), are reworded so the External tier is not "staffed" by
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
  `dev/modules/onboarding/` copies (the two docs copies there are scanned too),
  asserting the glob is non-empty and holds at least the three shipped presets. A preset added later cannot escape it. The test
  does not rely on the "strip every match" control alone, which takes its mutation
  from the pattern under test; it says which controls are independent of the
  pattern. **The five nodes of the retired test each have a stated fate**, recorded
  in the commit body: the non-empty glob and the two forbidden wordings are
  re-homed here; "exactly three staffed paragraphs" retires with its premise; the
  negative fixture becomes the two literals' controls; and the positive fixture's
  job, proving the literals do not flag a correctly worded sentence, is kept by one
  control that a correct sentence passes. *Red when:* either literal is dropped to
  clear the credit line, the glob misses a preset, a control passes vacuously, or
  the positive-sentence control is missing.
* **Completeness.** The stance test lists the pinned path set by glob and fails
  unless every file with a Search A hit is scanned or sits in an explicit
  exemption table (path and reason). **No file in the install set** (`templates/`,
  `dev/modules/`, both `AGENTS.md` copies, both loop documents) **may be in the
  table**; it holds only files that do not ship, such as history or a ceremony
  document. Controls: remove a file from the table, insert a phrase into a scanned
  copy, and add an install-set file to the table; each turns a node red. *Red
  when:* a file with a hit is neither scanned nor exempted, or an install-set file
  is exempted.
* **The deletion is visible where the suite is blind.** In a scratch worktree at
  C7 the verifier reports `FROZEN-MISSING` for exactly this file and
  `COLLECTION-DROPPED` for exactly its five nodes (beside the existing batch), and
  `pytest bootstrap/tests/test_gate_manifest.py` stays green; both are recorded.
  *Red when:* another frozen file is missing or another node is dropped.
* **The module is thinned, and its External paragraphs go.** Both copies drop the
  roster, the citation rule and the ledger for a two-line pointer to "The review
  sweep" and shrink from 152 and 151 lines to about 84 (recorded). The paragraphs
  that select a more distant reviewer by risk are **struck, not kept**: "A change
  touching a contract or a load-bearing assumption gets an External review in
  addition ...", "a human fills the External tier", "make it prove itself", "The
  External tier layers ...", and the header and closing lines that call the module
  the "two-tier" model. In their place the module says what it is now for, in one
  sentence with no "tier": how a two-agent-type or multi-human team staffs a read
  the Maintainer has called, pointing at `AGENTS.md` for the one definition of the
  Maintainer-called read. **Both copies are under every Search A pattern.** The
  module keeps what the frozen trap test pins: the scope-cut-means-claim-correction clause beside
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
* **Expected checker flags (amended: three, see *Deviation request* at the end).** `python scripts/check_cairn.py` with the two
  archived source proposals named explicitly reports exactly two new line-bound
  flags at C7, the module citations in the stance proposal's Security Review
  (module lines 132-133 and 131-132, in files that are now about 84 lines), and
  nothing else new. They are expected and recorded; that record is append-only and
  is not edited. The default run skips archives, so it never shows them. *Red
  when:* a flag appears that is not these two.
* **Lockfile.** A second scoped finalize for `dev/modules/dual-review.md` only
  (the first was C1's). `verify_integrity` still reports 18.
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
| External is the Maintainer's call, per artifact; `Called by` verbatim and repeated in the commit body; never-does list; a roster is not a call; what distance buys and the staffing reviewer following the brief; a standing call is a floor | C1, C2, C4 |
| Header and record grammar (`usual`, `Tier` values, legacy read never rewritten) | C2 (C1 for the read rule) |
| No rule selects more distance: Search A, Search B, the thirteen-row table | C1 to C7; classification appended at C4 |
| The reviewer roster after the change; code review never reopens the Decision | C1, C3, C4 |
| Capability floors by stage; the low cleanup row; "premise-checking" | C3, C4 |
| Migration table | C1, C2 (the read rule), `git diff` checks in C2 |
| Reaching adopters: shipped text first | the order of C1 to C4 |
| Headline: anchor and README verbatim, figure, descriptive pages | C4, C6 |
| Tests: retire; add; reword; keep the trap test green; every test file that mentions External has a disposition | C1, C7; table in *Verification* |
| Evidence plan: Searches A and B with controls, falsifiers, smoke checks | C1 to C8 |
| Security preflight S1 to S5 | *Verification*; S3's quoted sentence is W2 |
| Not in the proposal: engine gate and comment, runbook and credit comments, stale planner text | untouched; *Dispositions* for the board row |
| The sweep, citation rule, coverage line and ledger in the loop document; the pointer; the scope and project-probes sentences | C1 |
| The module keeps what is about multi-type teams (staffing a called read, and the trap) and points at `AGENTS.md` for the one definition of the called read; its External paragraphs are struck; thinned last | C7 |
| Cairn's own copies follow | C1, C7 |
| "Domain rotation" and the minimal-team lines kept as staffing facts, none reading as independence earned or a read added | C4, C5 |
| The two doctrine sentences ("Adaptation") and the pointer retarget | C4 |
| The lenses test, positive and negative, with the six mutants | C1, C7 |
| Boundary C opening names the no-plan proposal | C4 |
| Q3 of the lenses: no coverage-line stanza in the scaffolds | C2 (negative check) |
| Q4 of the lenses: rehearsal on scratch copies, no real upgrade | C8 |

**The Security Review's six findings.**

| Finding | Where it becomes a criterion |
|---|---|
| SR1: a `Called by` quote authorizes the read it heads and nothing else; four statements; the two privileges struck | W2 (now also the commit-body copy and a provenance line); C1 (carriers, module clause), C2 (templates), C4 (`doctrine/plans.md`), C8 (probe) |
| SR2: the retired test's two wordings carry over only as literals; glob the presets and the installed copies | C7 |
| SR3: the deletion is silent in the suite; final test bytes and the deletion in one chunk before the re-anchor; board line | the opening commit's row; C7; M (with blob ids at archive); *Scope* |
| SR4: the carve-out says "architecture", is never a lifecycle pass, sits under the data-governance gate | W4; C3, C4 |
| SR5: the launcher review is the one surviving standing call; a sixth category; the runbook untouched | W5 (its record carries `Called by` and is a Security Review); C4; *Verification* (runbook and launcher files byte-identical) |
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
  Maintainer answers the question at the top of the Response.
* **"Plain".** Whether the new Review text reads plain to the Maintainer is the
  plan reviewer's and the Maintainer's call. The plan holds the line counts and
  the vocabulary, not the reading.
* **"A tree that never runs `upgrade` gets nothing."** True and unfixable here.

**Scope delta**: preserved. Nothing either proposal committed to is dropped. The
additions the plan makes are expansions of verification or of the files that a
stated outcome reaches, and declining any would not be a reduction: the module
clause in C1, the all-profiles install test, the completeness check, Search D and
its four files, the `Called by` provenance line, conforming the paragraphs that
credit a checker that does not exist, and the blob-id record at archive.

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
| C3 | `test_model_selection_stub.py`, `test_upgrade_module.py`, `test_profile_grammar.py`, `test_security_stack.py`, `test_onboarding_seed_roster.py`, `test_presets.py`, `test_profiles_smoke.py`, `test_scaffold.py` (also the fidelity manifest and the optional templates), `test_module_roster.py`, and the skill tests (`test_skills_install.py`, `test_skills_fanout.py`, `test_skills_upgrade.py`, `test_skills_self_heal.py`, `test_skill_contract.py`, `test_session_routines.py`, `test_session_failsafe.py`, `test_first_session_report.py`) |
| C4 | `test_scope_reduction_trap.py`, `test_verification_boundaries.py`, `test_comprehension_floor.py`, `test_loop_fidelity_gate.py`, `test_check_cairn_content.py`, `test_claim_check_module.py`, `test_incident_trackers_module.py`, `test_replacement_tools.py`, `test_skill_contract.py`, `test_onboarding_activation_helper.py`, `test_deferred_task_store.py`; gates: redundancy, body coverage |
| C5 | `test_scope_reduction_trap.py`, plan D's scientific-check test file; gates: redundancy |
| C6 | `test_quickstart_sequence.py`, `test_doc_governance.py`, `test_check_cairn_content.py`, `test_link_check_exclusions.py`, `test_core_dev_folders.py`, `test_module_roster.py`, `test_scaffold.py`, `test_onboarding_activation_helper.py`, `test_onboarding_slot_substitution.py` (they read the docs pages and copies); gates: redundancy, `check_cairn.py` |
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

**Reviewed range.** The record names this plan's own commits by SHA, from the
parent of C1 to the tested commit. Because the plan starts only after plans C and
D have reached `awaiting-code-review`, a `revising-code` commit from either that
lands inside the span is listed by SHA as outside the range, and is in the tree
the suite runs against.

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

* **The neutrality leg** exits 1 at the opening commit with 74 FAIL lines and is
  expected to read zero by C1's parent, plan C having zeroed it. Record the figure
  at C1's parent and at the tested commit: zero stays zero, or (fallback) no line
  is in a file this plan edited and was not there before.
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

Also worth attacking: a `Called by` quote that carries a waiver or says "no
Security Review needed"; a usual pass offered as clearing a Security Review or a
plan obligation; a preset added later that the glob should catch; the completeness
exemption table used to hide a hit; a module External paragraph left behind; the
cleanup row read as lowering a review; the dangling-heading and checker-name greps;
the adopter staged trees.

**Security preflight, re-answered where the chunking changes an answer.** The
proposal's S1, S4 and S5 stand; the one addition to S1 is that the `Called by`
line now says where the words live, so a quote taken from a Decision can be
checked by the next reader against a committed block, while a quote taken from chat
stays a reader's trust. **S2** (can it fail?): the stance and sweep
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
  test files, the final statement about the deletion, that M waited for code
  review, and the git blob id of each of the three test files at the code-reviewed
  commit (`git ls-tree <sha> -- <paths>`), asking the ceremony to confirm it pins
  those bytes.
* **Board rows deposited at archive**, each under a `defer` request with the
  Maintainer's quoted authorization. The accepted text assigns both to this plan:
  (a) the engine's `_TEAM_STAFFING_GATES` comment ("fill its External tier") and
  the matching comment in `bootstrap/tests/test_presets.py` are now false and are
  left alone here (stance proposal, *Not in this proposal* and the Response to the
  standard review); (b) retiring the module's duplicate trap paragraphs and their
  pins (lenses proposal, *Not in this proposal*). Authorizations to quote: "accept
  both as descried" and "I accept all five of your recommendations. Accept as
  recommended". The `defer` batch is put as one batch; the Waiting line is written
  in the header block when it is put and deleted when the Maintainer answers.
* **The ten-review check** (the stance proposal's "reviews read as polish" signal)
  gets its owner. The Maintainer answered the Response's question on 2026-10-18,
  verbatim: "Yes, we should keep watching." So a board row is deposited at archive
  in the same batch, with those words quoted. It carries the default the Response
  describes: the goodnight roadmap-scrub owner counts once ten proposal reviews
  carry the new header, logs the pattern if it shows, and puts it to the
  Maintainer, with the other three signals noted on the same row.
* **This plan carries no Waiting line at archive.** The open wait, the re-anchor, is
  declared on its marked board row.
* **Left open by this plan.** `dev/proposals/2026-10-18-claude-stewardship-and-reuse.md:689` cites lens 5 at
  lines 58 to 60 of `templates/modules/team-gated/dual-review.md`, a range the accepted thinning removes. The
  additions-only marker maintenance (`f3abb787`) cannot clear a line-range citation, and the proposal
  is another author's append-only record, so I did not reword it. Its plan, which writes against the
  lenses' final home, rewords the bullet or the Maintainer asks for an erratum. `check_cairn.py` reports it.
* **Found in passing, not this plan's.** `dev/modules/security-review.md:181` links
  `content_scan.py` relative to `dev/modules/`, where no such file exists
  (`scripts/content_scan.py` does). `check_cairn.py` reports it, and did at the base. It is put
  to the Maintainer as a board row in the archive-time `defer` batch.

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

## Plan review -- Claude Sonnet 5.5 (Internal) -- 2026-10-18

```
Reviewed commit: 8cc124b5f537ca14742216e53224cfd7e2d4345c
Target: the whole plan (header through Dispositions), read against both accepted Decisions, the stance proposal's Revision 1 and Security Review (SR1 to SR6), and the lenses proposal's Revision 1 and review (RL1 to RL7); every figure below measured on that commit's bytes in a detached worktree
Prior findings: none (the Internal Security Review pass at fe079291 is a separate obligation; where my findings overlap its RS-SR ones I cross-reference them and close none)
Assurance path: high-assurance
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised (11: 2 blocking, 3 medium, 2 low-medium, 4 low)

Distance: a fresh session. I wrote neither the plan nor either proposal and no earlier review of them. This is the Internal pass only. It is not External, and it does not do the Security Review's job. I read the Security pass after my findings were drawn, only to avoid repeating it. The plan answers in its cells, per the template, so each fix below names the cell to change.

### In plain terms

The plan delivers what both Decisions accepted, with one sentence dropped and one place where its own wording fails its own checks. Every number I could re-measure reproduced.

* **Dropped:** the Maintainer's quote must also appear in the commit message, not only in the review (RS-PR2). The Security pass found the same gap (RS-SR4), so one edit closes both.
* **Self-contradiction:** the paragraph the plan tells the implementer to paste into six shipped files contains the exact text `required(External)`, and the plan's own tests are written to fail on that text (RS-PR1). As written, a faithful implementer cannot make the plan's first chunk green.
* **A blind spot:** the plan's two searches find rules that *pick* a more distant reviewer. The headline the Maintainer approved also removes the old *description* ("two-tier", "structurally independent tier"), and four files outside the plan's list still carry it (RS-PR4).
* **The slot is right, but the first chunk does not need to wait.** Chunk C1 touches no file that plans C or D touch (RS-PR5). Today's `AGENTS.md` still says an External code review is an escalation, so every session before C1 lands can pick it again.
* **No materially simpler path exists.** The weight is the 49-file spread the Decisions prescribe. I found three small trims (RS-PR11) and one cost the plan does not budget: how much longer `AGENTS.md` gets (RS-PR8).

### What I measured

Each in a detached worktree of `8cc124b5` under my scratchpad (removed when done), with the instrument first shown to find a known case.

* **Search A: 35 files, 102 matches. Confirmed.** Rebuilt from the proposal's pattern, with markup stripped and whitespace collapsed. Control: both `AGENTS.md` copies match. **Search B: 61 paragraphs in 30 files. Confirmed**, rebuilt from the proposal's description; every file it hits is either in the plan's list or noise (`dev/modules/claim-check.md`, `doctrine/runtime-contract.md`, `on-ramp/README.md`). The authority probe, rebuilt, gave 14 paragraphs in 11 files against the plan's 17 in 11. The plan says the count is not the criterion, and both privileges (`doctrine/plans.md` "Tier ordering" and the archive branch, and the module clause in both copies) are among my hits.
* **The frozen file: confirmed, and it is a deletion.** `gate_manifest.json` > `frozen_files` holds 183 keys. Control: `bootstrap/tests/test_scaffold.py` is a key. None of the 49 prose files is a key (the one `.md` key is `bootstrap/tests/fixtures/skills/README.md`, which this plan does not edit); the retired test is. `_gate_manifest.py verify --no-collect` reports 0 `FROZEN-MISSING` and 25 `FROZEN-MODIFIED` on the unchanged tree. After removing that one file in my copy it reports 1 `FROZEN-MISSING`, and the collecting run adds exactly five `COLLECTION-DROPPED`, one for each of the five node ids the fixture lists. The plan's 25 reproduced.
* **Lockfile: 18 violations, as stated.** The five edited files the plan names are among them; `dev/modules/dual-review.md`, `model-selection.md` and `security-review.md` are tracked and match today. **Neutrality: 74 FAIL**, 18 of them in the five files the plan names (8, 5, 3, 1, 1). **`cairn:slot` counts** match the plan in all eight files.
* **A real install of each profile** (`bootstrap/scaffold.py --config bootstrap/profiles/<name>.yml --non-interactive`, all three exit 0). `solo-greenfield`'s loop document holds none of "Name the satisfier", "Silent failure", "Cross-document consistency", "Falsifiable coverage", "coverage line"; "falsification ledger" is in `AGENTS.md` only. The `dual-review` module installed by the other two profiles matches every one of those patterns, so the absences are real.
* **W7 and W8 equal Revision 1's wording** byte for byte after whitespace collapse (script). The nine lens labels and their order match `doctrine/dual-review.md` and the module. The ten trap-test node names C7 lists exist (five per module copy). The 19 test files that mention External are all in the plan's disposition table.

### Findings

**RS-PR1 -- Blocking. The paragraph the plan pastes into six shipped files contains the text its own checks forbid.**
* **Evidence.** W2 says "An agent never writes `required(External)`" (`dev/plans/review-stance-and-lenses.md:424-425`). With markup stripped, Search A's first alternative `required\(external` matches it. I ran Search A's patterns over W2 to W8: only W2 matches, once.
* **What goes red.** C1 requires Search A's patterns to "return nothing" in the four carrier files (`:576-585`), so both `AGENTS.md` copies fail on W2. C2 requires `required(External)` to appear "in none of the four" templates (`:689-691`), while also requiring W2 in all four (`:683-686`). C1's mutant "add `required(External)` to a copy" (`:659-660`) cannot be told apart from W2's own copy, so its unmutated control is already red.
* **Fix (C1 and C2 criteria, W2).** Either (a) reword W2 so the string is not spelled, for example "never declares External as a required review in a header", and point the label `no-agent-writes-required-external-or-recommends-distance` at the new words; or (b) keep the example and scope the forbidden pattern to a header line or a `{{ ... }}` choice list that offers `required(External)`, with the mutant inserting it there. I recommend (a): the pins stay plain literals (the plan's own S2 rule), and it costs a few words.

**RS-PR2 -- Blocking (scope floor). W2 drops the commit-message copy of the Maintainer's quote.** Same finding as RS-SR4; one edit closes both.
* **Evidence.** Revision 1, section 2, which the Decision says binds: the pass carries `**Called by**: Maintainer` followed by the words, "and the same quote in the commit body, as for a scribed Decision" (`dev/proposals/archive/2026-10-18-claude-external-is-a-maintainer-stance.md:973-976`). W2 (`:421-423`) and the label `called-by-carries-the-maintainers-words-verbatim` (`:565-566`) say only the pass. A search of the plan for "commit body" finds four unrelated lines (`:86`, `:471`, `:632`, `:664`). The Scope delta calls this scope "preserved" (`:1046`).
* **Fix (W2, C1 and C2 labels).** Add "and the same words in the commit message, as for a scribed Decision" to W2 and a label `called-by-quote-is-repeated-in-the-commit-body`. The unmade check stays unmade: nothing reads the commit message either, and W2's last sentence already says so.

**RS-PR3 -- Medium. W2 and its twelve labels disagree, and four more Revision 1 statements have no home.**
* **Evidence.** C1 and C2 require twelve called-read labels in six files (`:562-575`, `:683-686`). Label 7, `a-roster-you-set-is-not-a-call`, has no sentence in W2 (`:419-435`). Revision 1 has it: a roster you set "adds no read and upgrades none, so it is not a call" (stance proposal `:981-982`). A pasted W2 cannot satisfy its own label list. Four more statements the Decision made binding have no label or criterion:
  * "What distance buys is information for you, not a rule ... The staffing agent follows your brief, answers the same three questions from that distance, and says so" (stance proposal `:983-986`). Revision 1's table says of the struck "recommended wherever it can be staffed" that "the information moves to section 2" (`:1033`). Nothing in the plan moves it.
  * Code review "never reopens the Decision" (`:946`). Today it is only in `doctrine/dual-review.md:47`; Revision 1 restates it "where reviewers will meet it first".
  * The "Domain rotation" row (`:1039`, "kept as staffing facts ... reworded so none reads as independence earned"). `doctrine/dual-review.md:63` reads "independence by rotation rather than by model type"; neither search hits it and C4 does not name it.
  * The module row says it "keeps ... the Maintainer-called read" (`:1035`). The lenses Decision supersedes the lenses and ledger part, not this part. The plan is silent; say that `AGENTS.md` carries the one definition and the module points.
* **Fix.** Add the roster sentence to W2 (naming `dev/collaboration_agreement.md`, which every install has). Give each of the four a line in C4's criteria, or a row in the Scope delta table naming where it lives. While W2 is open: it is one 200-word paragraph carrying twelve rules, and "floor" is used three ways in the same file. Four short bullets (what a called read is, how it is recorded, what an agent never does, what it never does to the other reviews) read faster, and each label maps to a bullet. Say "standing rule" once beside "standing floor".

**RS-PR4 -- Medium. The two searches find rules that pick a more distant reviewer; nothing searches for the old description, which the approved headline also removes.**
* **Evidence.** I ran a third search, same roots and stripping, over the paragraphs Search A does not already match: `two[- ]tiers?|two review tiers|single tier|structural(ly)?[- ]independen|Internal (tier|review|pass|Reviewer)`. It reports 63 paragraphs in 33 files. Control: it finds anchor 4's "Two-tier review" (`doctrine/rationale.md:364`) and the README's alt text. Stale claims in files the plan's list does not name, where neither search can reach them:
  * `doctrine/README.md:20`: "the two-tier model and structural independence".
  * `templates/modules/README.md:49-50`: the module "adds the second, structurally-independent tier when the team can staff it".
  * `templates/optional/CONTRIBUTING.md:31`: every substantive change is "reviewed across structural independence" (an opt-in adopter file, `bootstrap/_scaffold/config.py:622`).
  * `doctrine/doc-governance.md:64`: "the review tiers and structural-independence floors".
* **In listed files with no criterion that removes them.** The module's header and tail (`templates/modules/team-gated/dual-review.md:5`, `:10`, `:151`: "two-tier Dual-Review model", "makes review two-tier and structurally independent"); `dimensions/README.md:67-69` ("the full two-tier Dual-Review apparatus with structural-independence floors", while C5 names only the Complexity cell); `docs/glossary.md:54`, `docs/vision.md:37`, `docs/workflow-role.md:19` (C6 lists the pages but its criterion forbids only "different agent type or a person" as a requirement, `:866-873`). RS-SR2 covers the module's External paragraph; this adds its header and tail.
* **Fix (The searches, C4 to C7).** Add this as Search D with the same classification (stale, history, staffing fact), add the four files to the chunk that fits (C4 for the two doctrine files, C3 for the two shipped ones), and give the thinned module in C7 one sentence saying what it is now for, with no "tier" in it.

**RS-PR5 -- Medium. Third is the right slot; the first chunk's gate is stricter than its files require.**
* **Evidence.** C1's files are the two `AGENTS.md` copies, the two loop documents, the two module copies (one clause), and three tests. I searched plan C and plan D, in both the reviewed version and the folded versions (`d0647d5f`, `89f82f3f`), for each: none edits any of them, and both list `AGENTS.md` only under "Not touched". Every shared file in the plan's table (`:260-283`) sits in C2 to C7 (plus the opening and archive commits). Yet C1's gate is "C and D landed" (`:371`), and the slot paragraph holds all implementation until then (`:313-315`).
* **Why it matters.** The text agents choose External from is the text C1 replaces: `AGENTS.md:96-97` ("An External code review is an escalation") and `:69-70` ("recommended wherever it can be staffed"). Each session until C1 lands reads it. Waiting buys nothing, since there is nothing to rebase.
* **The order is the Maintainer's.** Plan C's "Sequencing with the later plans" and plan D's "Sequencing with the other accepted work" each list this plan *last*, after `model-mapping-install-path` and `board-as-basis`. The plan's "in the order its authors wrote down" (`:251`) leaves that out. The reasons for third (`:289-315`) are sound, but they ask to reorder two other authors' lists.
* **Fix (Sequence C1 row, slot paragraph).** C1's gate reads `ready-to-implement` only; C2 and C5 keep D's gate; C3, C6 and C7 keep C's. Say that C and D name this plan last, that "third" is a recommendation for the Maintainer's board order, and that C1 first needs no rebase. Plan C is now implementing (its C1 is `1fb06ea6`) and D is `ready-to-implement`, so the choice is live.

**RS-PR6 -- Low-medium. W8's "Lines 53-54" cannot be applied as cited.**
* **Evidence.** `README.md:53-55`: line 53 reads "Two things differ, and both favour the code case. Independence is easier to", line 54 continues, and line 55 begins `co-authorship." And review happens`. W8 replaces "Lines 53-54" with the single sentence "Distance is easier to record ..." (`:496-497`). Swapped literally, that deletes "Two things differ, and both favour the code case." and leaves "co-authorship." at the start of line 55. C6 compares "the text at the six cited places" with W8 (`:854-859`). The other five spans (lines 10, 49, 51, 102-104, 176-181) are whole lines or whole bullets and apply cleanly.
* **Fix (C6).** Name the span as the sentence "Independence is easier to establish ... 'no recent co-authorship.'" and keep the lead-in and the sentence after it.

**RS-PR7 -- Low-medium. Two docs pages ship to adopters as byte copies, and the plan names neither the copies nor the page's shipped status.**
* **Evidence.** `docs/agent-team-onboarding.md` and `docs/dev-tour.md` are copied byte for byte into every install that selects a preset (`bootstrap/_scaffold/install.py:1012-1016`). Cairn's copies, `dev/modules/onboarding/agent-team-onboarding.md` and `dev-tour.md`, are `cmp`-identical to them today, and precedent `9c0e002a` edited the pair together. The first copy has three Search A hits. C6 names only the docs pages (`:866-873`). C7 speaks of "the two installed copies" of the presets (`:883-884`, table row `:118`), but `dev/modules/onboarding/` holds three files: one preset copy (`collaborative-team.md`, which also differs from its template by `cairn:if` conditionals) and the two docs copies. Plan C also edits `docs/agent-team-onboarding.md`, and its text does not name the copy.
* **Fix.** C6 lists the two copies and requires `cmp` equal to the page after the chunk. C7's count reads one preset copy. These two pages reach adopters, so say so in the layer table (`:110-119`, rows `:117-118`).

**RS-PR8 -- Low. `AGENTS.md` growth is unbudgeted.**
* **Evidence.** The plan budgets the loop document (85 to 95 lines) and "each pointer about 7 lines" (`:629-632`). The stance block has no ceiling. The wording the plan pastes into `AGENTS.md` is W1's table (6 lines), W2 (17) and W3 (7), 30 lines, plus seven more labelled statements in C1 (`:552-561`), against the 13 lines of External and Internal text they replace (`AGENTS.md:59-71`). My estimate is +35 to +50 lines per copy, read at every session start. The Maintainer asked to keep `AGENTS.md` lean (lenses proposal, Question 2).
* **Fix (C1 size bullet).** State a ceiling (for example net +40 per copy), name the lines the stance block replaces, and keep "outside the range is a signal". If W2 becomes four bullets (RS-PR3) the ceiling is easier to meet.

**RS-PR9 -- Low. The two "needs your call at archive" items: one is overtaken, one is sound but asked too late.**
* **(a) The `AGENTS.md` pitfall sentence is already corrected.** Commit `69d3ac59` on master (after the reviewed commit; Cairn's root `AGENTS.md` only) says both a changed and a deleted frozen file stay green and names `_gate_manifest.py verify` as the only comparison. I read the new text; it matches what I measured. Drop item (a) and the plan decision at `:348-352`, or restate them as closed. RS-SR8 says the same.
* **(b) The ten-review tally is the right thing to name, and `defer` is the right disposition** (a plan that archives takes its watch with it; a guard is not possible, the signal is a judgment). The weakness is timing: put to the Maintainer at archive (`:1182-1191`), there is no chunk left to act on the answer. Put it with the plan's response, with a default: one board row naming the owner and the trigger ("tally the `Should this happen as framed?` lines of the first ten proposal reviews after the stance lands; the goodnight roadmap-scrub owner runs the one grep on the tenth and logs per the proposal's second signal"). The `defer` batch needs a Waiting-line moment (`dev/plans/_template.md`, *Dispositions*); the plan's "no Waiting line at archive" (`:1192-1193`) should say it is written when the batch is put and deleted when answered.

**RS-PR10 -- Low. Three small corrections.**
* **C3 names a C4 file.** C3 requires `grep -c 'adversarial premise'` to be 0 "in `doctrine/roles.md`" (`:735-737`), but C4 edits that file (`:799-802`; `doctrine/roles.md:222` still has the phrase). Move that clause to C4, as the plan already does for the dangling headings (`:751-757`).
* **The low row narrows "and related".** The Maintainer said "docstrings cleanup and related should go to low" (stance Decision, Q1). C3 writes "docstring and comment cleanup" (`:732-734`). Use their words, or say what "related" covers. The shipped table already has a low row, "Non-substantive doc tweaks" (`templates/modules/team-gated/model-selection.md:56`); extending it may be simpler than adding one. The `usual` wording problem in the same row is RS-SR3.
* **The retired test's five nodes have no stated fate.** The plan re-homes the glob and the two literals and retires the "exactly three staffed paragraphs" node with its premise, but never lists all five. The fifth, the positive fixture, has no home: its job was to prove the literals do not flag a correctly worded sentence (the old test's docstring says the original spec "false-positives on legitimate text" in two presets). Add a five-row table to C7, and one control that a correct sentence passes.

**RS-PR11 -- Low (optional). Three trims; none cuts an accepted outcome.**
* **Merge C5 into C6.** Both are prose with the same gates (redundancy, `check_cairn.py`) and no pin beyond the trap test and D's test. C5's gate "D landed" duplicates the plan-level gate. One chunk, one Boundary A row, one set of repeats.
* **Lead the neutrality check with "stays zero".** Plan C's checker is landing and is meant to zero the gate, so by the time this plan's C1 runs the baseline is zero. Keep the per-chunk FAIL-line diff as the fallback paragraph, not the main text (`:235-247`, and the repeat at `:528-530`).
* **Trim the sequencing table to its real collisions** (`:260-283`). About half of its 22 rows say "none", "different sections" or "commit by path". Plans C and D are mid-revision, so the table will be stale within days; the rule "re-read the file at edit time" already covers them. Keep the six rows that bind: `solo-greenfield.md`, the marker lines in three files, `test_onboarding_review_tiers.py` ordering, D's template cells and the Complexity cell, and the lens-5 anchors.

### Answers to the two questions

**1. Does this plan deliver what both Decisions accepted, all of it?** Yes, with exceptions that are fixes to the plan's cells, not a redesign.
* **Carried exactly.** Stance Q1 (proposal high, plan medium, code medium, Security high, docstring cleanup low), Q2 (`usual`, `usual + Security Review`, `Tier` values, External only beside `Called by`), Q3 (anchor and README wording, equal to Revision 1 after whitespace collapse; the name and module id kept), Q5 (migration), the three calls, and the Boundary C fix. Lenses Q1 to Q5, including no coverage-line stanza in the scaffolds (C2's negative check) and the scratch-only rehearsal (C8). SR1 to SR6 and RL1 to RL7 each map to a criterion or a named disposition.
* **Dropped or unplaced.** The commit-message copy of the quote (RS-PR2); the roster sentence and four other Revision 1 statements (RS-PR3); the old description in files the searches do not reach (RS-PR4).
* **Added beyond the Decisions.** Only to verification: the module clause in C1 (the Revision 1 strike, applied early), the all-profiles install test, and the completeness check with its exemption table. The plan declares all three, and none widens what ships. The exemption table is the one that can hide a hit (RS-SR2 asks that install-set files may not use it); I agree.
* **"Scope delta: preserved"** is right once RS-PR2 and RS-PR3 are folded.

**2. Is there a simpler path to the same outcome?** Not in structure. The 49 files are the per-layer counts of Revision 1 section 7 (24, 8, 4, 10, 2, which sum to 48) plus `doctrine/onboarding.md`. Joining the two proposals already saved a plan cycle and the double writing. The six copies of the called-read paragraph (two `AGENTS.md`, four templates) follow from SR1, which asks for it in `AGENTS.md` and both templates. The remaining weight is mandated: a mutation ledger for set claims (`AGENTS.md`), Boundary B in full mode (a contract surface is touched), the scratch rehearsal (lenses Q4). The three trims are in RS-PR11 and the one cost the plan hides in a chunk row is RS-PR8.

### The five checks

1. **"Written once."** The lens text: yes. One shipped place (the loop document, plus Cairn's copy), a pointer in `AGENTS.md`, and the module stripped in C7. Between C1 and C7 two of the three profiles install both (measured: the module matches every lens pattern in `collaborative-team` and `high-rigor-legacy`), by design. The stance questions and the called-read paragraph are *not* written once: `AGENTS.md` carries all three rows of W1, each template carries its own row, and W2 sits in six files. That is the Decisions' design (SR1; Revision 1 section 7), pinned by labels, not sentences. **Could an early test pin wording a later chunk moves?** I found no case in the shipped surfaces: after C1 only C7 touches a C1-pinned file (the module copies), and the pins there are absences that C7 satisfies more, not less. The places where an early check meets a later move are three: W2 against its own pins (RS-PR1), the module group in C1 against the External paragraph that stays until C7 (RS-SR2), and the lock count between C1 and C3 (RS-SR7).
2. **The single frozen file is a deletion.** Confirmed (above), with the method shown on a known key and on the deletion itself. The five nodes: the non-empty glob and the two literals are re-homed in C7; "exactly three staffed paragraphs" retires with its premise; the positive fixture has no stated home (RS-PR10); the negative fixture becomes the literals' controls.
3. **The Maintainer's tier answers.** Carried exactly, except "and related" (RS-PR10) and the `usual` wording in the low row (RS-SR3). The header words and `Called by` rule are W2 and C2, with the commit-message gap (RS-PR2).
4. **The sequencing.** The shared-file table matches both plans' own scope lists, with one omission: the installed copy of `docs/agent-team-onboarding.md` (RS-PR7). Third is right for the plan as a whole; C1 can start now (RS-PR5).
5. **The five items the author could not make checkable.** Sound. The quote's genuineness cannot fail a test, and the plan says so in the shipped sentence. Classification is a reader's judgment, with completeness and a re-run as the checks, though Search D (RS-PR4) widens what is classified. The four signals are future observations; the first is made countable and the last mechanical, and the watch needs its live home asked for earlier (RS-PR9). "A tree that never runs `upgrade` gets nothing" is true and unfixable here. **"Plain"** is the one the plan leaves to the plan reviewer: the plan's own *In brief* is plain and short. The shipped W2 is not yet (RS-PR3), and `AGENTS.md` gets longer (RS-PR8). The two "your call" items are RS-PR9.

### What I did not cover

* The Security reading of the plan: the trust apparatus, the launcher call (W5), the low row's authority leak. That is the Internal Security Review's (RS-SR1 to RS-SR8).
* I did not run the full suite or the plan's 22-file mapped set; Boundary B is the implementer's. Run only: the gate-manifest verifier, `verify_integrity`, the neutrality gate, `claim_check` on the plan, three real installs, and my own rebuilds of Searches A and B, the authority probe and Search D.
* The two new test files do not exist. Their controls and mutants are judged by design only, apart from the one collision in RS-PR1.
* I did not read the figure `docs/assets/dual-review-independence.svg` beyond its Search A hits, or the docs pages beyond the lines cited. I did not rewrite any of the README, doctrine or docs sentences to test C4 to C6 criteria, and the chunk criteria for those files rest on the searches.
* I did not run the adopter rehearsal, the AST verifier, the body-coverage probe, or `check_cairn.py`.
* My Search B and authority-probe counts come from my own reading of the proposal's description, not the plan's script, which the plan says the implementer commits into the record.
* Later commits overtake some plan statements and I did not re-review the plan against them: `69d3ac59` (RS-PR9), plan C's `implementing` status and its C1, plan D's fold (`89f82f3f`). I read plans C and D at those later commits only for the file overlap in RS-PR5.

## Response to plan review -- Claude Sonnet 5.5 (author) -- 2026-10-18

Answers the Internal Security Review at `fe079291` (REVISE; RS-SR1 to RS-SR4
block) and the Internal review at `ef08e2a4` (REVISE; RS-PR1 and RS-PR2 block).
Per the template, the corrections are folded into the operative cells above and
this section is a disposition table that points at them. Neither review section
was edited. There is no second round, so Status moves to `ready-to-implement`.

### One question for the Maintainer

**Should the "reviews read as polish" check have an owner after this plan
archives? Recommended default: yes.** The accepted proposal says that after the new
rule lands you count the first ten proposal reviews. If every first answer (the
"Should this happen as framed?" line) is a plain "yes" and the author adopts none
of the reviews' alternatives, the reviews have turned into a form, and the
proposal says to log that and tell you. Once this plan archives, nothing owns that
count, and a watch that lives only in an archived file is lost. The default is one
board row in `dev/PLANNING.md`: whoever runs the goodnight roadmap scrub does the
count with one search once ten proposal reviews carry the new header (the chunk
that edits the proposal template makes the label the same everywhere), logs it in
the incident tracker if the pattern shows, and puts it to you. The other three
signals (a defect a more distant read would have caught; you asking for External
reads on most proposals; an agent writing External again) go on the same row as
things to notice, not to count. The alternative is to drop the watch, in which
case nothing checks whether the new reviews have become a form. If you agree, the
row is deposited at archive with your answer quoted, in the same batch as the two
rows the accepted text already assigns to this plan.

### Calls I made near your line

* **The cleanup row lowers the writing step only** (W9). You said "docstrings
  cleanup and related should go to low". I read the scribe's note, "its review
  stays at the usual tier wherever it touches a high-risk file", as: the review is
  never lowered and a high-risk surface still owes its Security Review. If you also
  meant that reviews of cleanup away from high-risk files may run at low, that is a
  one-line change to the row. It must be said in words, because lowering a review
  should not be left to inference.
* **54 files, not 49.** A third search for the old description ("two-tier", "a
  structurally-independent tier") found four more pages that say it as current:
  two doctrine pages and two shipped pages, one of them an opt-in file adopters
  receive. They are in C3 and C4. No accepted outcome moved.

### Dispositions

| Finding | Disposition | Where it changed |
|---|---|---|
| RS-SR1 (blocking): a Security Review's two-pass rule and plan obligation line are unpinned, in paragraphs the plan rewrites | accept | W10 and W11 added; labels in C1 (both `AGENTS.md`) and C2 (all four templates); the code-review floor label extended to both plan templates in C2; two mutants (C1, C2); C4 criterion that the obligation paragraph and the "Security Reviews wherever they attach" bullet survive |
| RS-SR2 (blocking): the module's External-selecting paragraph is assigned to no chunk | accept | C7 "The module is thinned" now strikes those paragraphs and puts both copies under every Search A pattern; C7 completeness forbids exempting an install-set file; C1 states its module group holds only the privilege-clause literal; Scope delta row; *Classification* |
| RS-SR3 (blocking): "usual stage tier" can lower the review of a high-risk edit | accept, with the call above | W9 quoted without "usual"; two C3 criteria (the bright-line list and the downshift exclusions survive); `roles.md` clause in C4 |
| RS-SR4 (blocking, scope floor): the commit-body copy of the quote is dropped | accept; closes RS-PR2 with it | W2 "How it is recorded"; labels `called-by-quote-is-repeated-in-the-commit-body` and `called-by-names-where-the-words-live` (C1, C2); the `Called by -- Decision at <commit>` provenance line is accepted as cheap hardening, an addition; W2's never-list now also covers "head a pass External on its own" and declaring External required in a header |
| RS-SR5: W2 and W5 disagree about the launcher review | accept | W5 (its record carries `Called by` and is a Security Review); W2 "discharges no Security Review by its distance or its brief"; C4 `narrows the pass` reads 0; runbook untouched (*Verification*) |
| RS-SR6: paragraphs credit a checker that does not exist; one page names the wrong satisfier | accept | W10; C1 label `no-tool-reads-the-obligation-line-a-reader-does`; C4 "No checker is credited" bullet, including conforming `doctrine/lifecycle.md` |
| RS-SR7: C1's module edit takes the lockfile count to 19 | accept (re-measured: 19) | *Scope > Lockfile*; C1 criterion; C7 second finalize; Sequence C1 row |
| RS-SR8: the C7 to M window; stale disposition | accept | blob ids: *Scope > Frozen files*, M row, *Dispositions*; the pitfall item dropped, closed at `69d3ac59` (*Plan decisions*) |
| RS-PR1 (blocking): W2 contains the text its own checks forbid | accept, option (a) | W2 no longer spells `required(External)`; re-checked against Search A and the by-default pin; the C1 mutant's control is now green |
| RS-PR2 (blocking, scope floor): commit-message copy dropped | accept; same edit as RS-SR4 | as RS-SR4 |
| RS-PR3: W2 and its labels disagree; four Revision 1 statements unplaced | accept | W2 rewritten as four bullets with the roster sentence; sixteen labels; C1 label `code-review-never-reopens-the-decision`; C4 "Domain rotation" and minimal-team lines; C7 module points at `AGENTS.md`; Scope delta rows. "Standing floor" is defined once beside "a rule that applies without being asked"; the other uses of "floor" are different named things in the doctrine and stay |
| RS-PR4: nothing searches for the old description | accept | Search D with its classification (*Scope*); four files in C3 and C4; `dimensions/README.md`, glossary, vision, workflow-role and the module header and tail in C5, C6, C7 |
| RS-PR5: C1's start gate is stricter than its files require | **modify** | *Recommended slot* last bullet and the Sequence C1 row. The reviewer is right that C1's files overlap neither plan C nor plan D. But plans commit to the same `master`, and interleaving this plan's commits with C's or D's would make each plan's Boundary B tested range and each code review's range ambiguous. So C1 waits until plans C and D have each reached `awaiting-code-review` or later, and the chunks follow in order. The slot stays third; the board order is the Maintainer's, and this plan's text now says C and D list it last |
| RS-PR6: W8 "Lines 53-54" cannot be applied as cited | accept | C6 README bullet names the span as a sentence |
| RS-PR7: two docs pages ship as byte copies | accept | *What changes* table (C6 12 files, C7 6); C6 requires the copies `cmp`-equal; the plan C row notes the pair |
| RS-PR8: `AGENTS.md` growth unbudgeted | accept | C1 size bullet: at most 40 lines net per copy, naming the lines it replaces |
| RS-PR9: the two archive items | (a) accept; (b) **modify** | (a) dropped, closed at `69d3ac59`. (b) the question and default above; *Dispositions* says the batch's Waiting line is written when it is put and deleted when answered |
| RS-PR10: three small corrections | accept all three | `roles.md` grep moved to C4; W9 uses "and related"; C7 states each retired node's fate and keeps a positive-sentence control |
| RS-PR11: three optional trims | **modify** | Trim 2 accepted: the neutrality check leads with "stays zero" (*Scope*, *Checks every chunk repeats*). Trim 1 declined: merging C5 into C6 would renumber chunk labels that the committed board row (C7) and both reviews cite; the duplicate "D landed" gate in C5 is removed instead. Trim 3 declined: naming every shared file is what the brief asked for; the table now says which rows bind |

**Scope delta**: preserved. Accepted scope is a floor and nothing here removes any
of it. The corrections add: sixteen labels, four statements, Search D with four
files, the provenance line, the checker-name conformance, the blob-id record, and
the sequential-start rule.

## Search classification -- Claude Sonnet 5.5 (implementer) -- 2026-10-19

The classification the plan owes at C4. It lists every hit of Searches A and B, the
old-description search (D) and the authority probe, grouped by file with a count, a
category and what happens to it. It is written by a script that stops on any
file with a hit and no entry, so no group is left out, and the counts below are the
tool's own. The tree is `HEAD` after C3 plus the C4 edits.

**Instrument.** Python 3.13.13. The script text for Search B and the authority probe
(Searches A and D use the plan's patterns as written):

```python
# Roots: AGENTS.md, README.md, doctrine/, templates/, dev/{proposals,plans}/_template.md,
# dev/agent_collaboration.md, dev/collaboration_agreement.md, dev/modules/, docs/,
# dimensions/, bootstrap/{fidelity-check,UPGRADE,REANCHOR_RUNBOOK}.md, on-ramp/;
# .md .yml .svg; archives excluded. Markup characters (* _ ` >) stripped, whitespace collapsed.
SEARCH_A = re.compile(r"required\(external|external[ -](floor|tier|review|reviewer|independence|stance|code review)"
                      r"|declared-external|a human fills|different-agent-type (pass|round)"
                      r"|escalate to the external|External Review Norms", re.I)
DIST = (r"(external|different (agent|model|vendor)|another (agent|model) type|second agent type"
        r"|model famil\w*|architectur\w* +diverse|diverse (a different|cross-(agent-)?type)"
        r"|structural(ly)? independen\w*|a human|human or|or a person)")
SEL  = (r"(reserved|mandatory|require(d|s)?|escalat\w*|pick|choose|need(s)?|warrant(s)?"
        r"|only when|preferred|recommended|floor|wants|calls for)")
SEARCH_B = re.compile(rf"{DIST}.{{0,120}}{SEL}|{SEL}.{{0,120}}{DIST}", re.I)   # per paragraph, either order
SEARCH_D = re.compile(r"two[- ]tiers?|two review tiers|single tier|structural(ly)?[- ]independen"
                      r"|Internal (tier|review|pass|Reviewer)", re.I)         # paragraphs A does not match
AUTH     = (r"(waive\w*|exempt\w*|satisf\w*|clear\w*|substitut\w*|skip\w*|instead of"
            r"|replac\w*|discharg\w*|confirm\w*)")
PROBE    = re.compile(rf"{DIST}.{{0,120}}{AUTH}|{AUTH}.{{0,120}}{DIST}", re.I)  # per paragraph
# A paragraph is a run of lines between blank lines (a bare '>' line counts as blank).
```

**Calibration, measured at `f804f3b7`** (the plan's reference commit): Search A 35 files,
102 hits (the plan's figure); Search D 29 files, 57 hits (the plan's figure); Search B
30 files, 64 hits (the plan reports 61, which it says it did not reconcile); the authority
probe 11 files, 13 hits (the plan reports 17 in 11 files; the file count agrees, the hit
count does not, and the plan says the count is not the criterion). Control: both
`AGENTS.md` copies match Search A at the parent of C1.

**Categories.** The seven of the plan: *Maintainer-called definition*, *staffing fact*,
*credit comment*, *marked history reference*, *noise*, *standing launcher-review call*,
*cost-rule carve-out*. Search D adds *stale description* and *ruled plan-review token*.
*Selection rule (to strike)* marks the paragraphs a later chunk removes; it is not a
resting place, and the end-state addendum appended after C7 shows none left.

**Search A, the phrasing** -- 17 files, 56 hits.

| File | Hits | Category | Disposition |
|---|---|---|---|
| `bootstrap/UPGRADE.md` | 2 | stale planner text, External rows | fix in C5 (Internal examples) |
| `dev/modules/dual-review.md` | 9 | selection rule (to strike) | fix in C7 (struck; module thinned) |
| `dev/modules/onboarding/agent-team-onboarding.md` | 3 | stale description | fix in C6 (page and byte copy together) |
| `dev/modules/onboarding/collaborative-team.md` | 5 | selection rule (to strike) | fix in C7 (presets reworded) |
| `dimensions/README.md` | 2 | selection rule (to strike) | fix in C5 |
| `dimensions/agent-team.md` | 2 | selection rule (to strike) | fix in C5 |
| `dimensions/complexity.md` | 2 | selection rule (to strike) | fix in C5 |
| `dimensions/human-team.md` | 1 | selection rule (to strike) | fix in C5 |
| `docs/agent-team-onboarding.md` | 3 | stale description | fix in C6 (page and byte copy together) |
| `docs/assets/dual-review-independence.svg` | 4 | stale description | fix in C6 |
| `docs/glossary.md` | 2 | stale description | fix in C6 |
| `doctrine/lifecycle-contract.md` | 1 | marked history reference | kept: the sentence is prefixed 'History:' |
| `doctrine/onboarding.md` | 1 | credit comment | kept: 'per the round-1 External-Review disposition' credits an earlier review |
| `templates/modules/team-gated/dual-review.md` | 9 | selection rule (to strike) | fix in C7 (struck; module thinned) |
| `templates/onboarding/collaborative-team.md` | 5 | selection rule (to strike) | fix in C7 (presets reworded) |
| `templates/onboarding/high-rigor-legacy.md` | 2 | selection rule (to strike) | fix in C7 (presets reworded) |
| `templates/onboarding/solo-greenfield.md` | 3 | selection rule (to strike) | fix in C7 (presets reworded) |

**Search B, the act of selecting** -- 32 files, 54 hits.

| File | Hits | Category | Disposition |
|---|---|---|---|
| `AGENTS.md` | 2 | Maintainer-called definition / staffing fact | kept: the called-read paragraph; 'Why this is stated positively' names 'a human' as the fence, a staffing fact |
| `bootstrap/UPGRADE.md` | 1 | stale planner text | fix in C5 |
| `dev/agent_collaboration.md` | 1 | staffing fact | kept: 'no review requires a different agent type' |
| `dev/modules/claim-check.md` | 1 | noise | kept: 'external' means outside the repo or the checker, or 'a different agent' means the next session |
| `dev/modules/dual-review.md` | 3 | selection rule (to strike) | fix in C7 (struck; module thinned) |
| `dev/modules/model-selection.md` | 2 | cost-rule carve-out | kept: the cost rule's check, which is not a review (the carve-out paragraph) |
| `dev/plans/_template.md` | 1 | Maintainer-called definition / staffing fact | kept: the called-read paragraph; 'Why this is stated positively' names 'a human' as the fence, a staffing fact |
| `dev/proposals/_template.md` | 1 | Maintainer-called definition / staffing fact | kept: the called-read paragraph; 'Why this is stated positively' names 'a human' as the fence, a staffing fact |
| `dimensions/README.md` | 1 | selection rule (to strike) | fix in C5 |
| `dimensions/agent-team.md` | 1 | selection rule (to strike) | fix in C5 |
| `dimensions/complexity.md` | 2 | selection rule (to strike) | fix in C5 |
| `dimensions/human-team.md` | 1 | staffing fact | kept: 'one designated Maintainer' is a staffing fact; reread in C5 |
| `docs/assets/dual-review-independence.svg` | 1 | stale description | fix in C6 |
| `docs/glossary.md` | 1 | stale description | fix in C6 |
| `doctrine/doc-governance.md` | 1 | noise | kept: 'external' means outside the repo or the checker, or 'a different agent' means the next session |
| `doctrine/dual-review.md` | 5 | Maintainer-called definition / standing launcher-review call / staffing fact | reworded in C4: per-artifact call, the surviving launcher-review call, 'no review requires a different agent type', 'a fresh session is the floor' |
| `doctrine/lifecycle.md` | 2 | noise | kept: 'external' means outside the repo or the checker, or 'a different agent' means the next session |
| `doctrine/plans.md` | 4 | staffing fact / stale planner text | reworded in C4: denials of a mandated different-agent-type read; the 'Normalizing' paragraph is retired-planner text, kept |
| `doctrine/proposals.md` | 1 | ruled plan-review token | reworded in C4: the ruled Plan review tokens |
| `doctrine/roles.md` | 3 | Maintainer-called definition / cost-rule carve-out | reworded in C4: distance is on request; the cost rule's check is not a review |
| `doctrine/runtime-contract.md` | 2 | noise | kept: 'external' means outside the repo or the checker, or 'a different agent' means the next session |
| `doctrine/session-routines.md` | 1 | noise | kept: 'external' means outside the repo or the checker, or 'a different agent' means the next session |
| `on-ramp/README.md` | 1 | stale description | fix in C6 (entry layer; not in the proposals' list, found by the search) |
| `templates/core/AGENTS.md` | 2 | Maintainer-called definition / staffing fact | kept: the called-read paragraph; 'Why this is stated positively' names 'a human' as the fence, a staffing fact |
| `templates/core/dev/agent_collaboration.md` | 1 | staffing fact | kept: 'no review requires a different agent type' |
| `templates/core/dev/plans/_template.md` | 1 | Maintainer-called definition / staffing fact | kept: the called-read paragraph; 'Why this is stated positively' names 'a human' as the fence, a staffing fact |
| `templates/core/dev/proposals/_template.md` | 1 | Maintainer-called definition / staffing fact | kept: the called-read paragraph; 'Why this is stated positively' names 'a human' as the fence, a staffing fact |
| `templates/core/dev/upstream/README.md` | 1 | noise | kept: 'external' means outside the repo or the checker, or 'a different agent' means the next session |
| `templates/modules/default-on/claim-check.md` | 1 | noise | kept: 'external' means outside the repo or the checker, or 'a different agent' means the next session |
| `templates/modules/team-gated/dual-review.md` | 3 | selection rule (to strike) | fix in C7 (struck; module thinned) |
| `templates/modules/team-gated/model-selection.md` | 2 | cost-rule carve-out | kept: the cost rule's check, which is not a review (the carve-out paragraph) |
| `templates/onboarding/solo-greenfield.md` | 3 | selection rule (to strike) | fix in C7 |

**Search D, the old description** -- 23 files, 37 hits.

| File | Hits | Category | Disposition |
|---|---|---|---|
| `AGENTS.md` | 2 | ruled plan-review token / staffing fact | kept: 'usual + Security Review', 'Internal Security Review' tokens; the attribution sentence 'a structurally-independent read is only independent if its author is its committer' |
| `README.md` | 2 | stale description | fix in C6 |
| `bootstrap/UPGRADE.md` | 1 | stale planner text | fix in C5 |
| `dev/agent_collaboration.md` | 1 | staffing fact | kept: the same attribution sentence |
| `dev/modules/dual-review.md` | 2 | stale description | fix in C7 |
| `dev/modules/onboarding/collaborative-team.md` | 1 | noise | kept: the 'first-cross-type-review' trigger matches a vendor name in a review heading, not the word |
| `dev/plans/_template.md` | 1 | ruled plan-review token | kept: the plan-security obligation sentence |
| `dimensions/README.md` | 1 | stale description | fix in C5 |
| `docs/DOCUMENTATION_PLAN.md` | 1 | stale description | fix in C6 |
| `docs/assets/dual-review-independence.svg` | 4 | stale description | fix in C6 |
| `docs/getting-started.md` | 1 | stale description | fix in C6 |
| `docs/glossary.md` | 3 | stale description | fix in C6 |
| `docs/vision.md` | 2 | stale description | fix in C6 |
| `docs/workflow-role.md` | 1 | stale description | fix in C6 |
| `doctrine/dual-review.md` | 3 | ruled plan-review token / history | reworded in C4: the heading 'Structural independence' stays (it now says independence is recorded, not required); the ruled tokens; the retired lifecycle planner |
| `doctrine/onboarding.md` | 1 | noise | kept: a docs page cited by name |
| `doctrine/plans.md` | 2 | ruled plan-review token / noise | kept: 'Assurance path does not change the plan review'; Boundary B reuse text |
| `templates/core/AGENTS.md` | 2 | ruled plan-review token / staffing fact | kept: 'usual + Security Review', 'Internal Security Review' tokens; the attribution sentence 'a structurally-independent read is only independent if its author is its committer' |
| `templates/core/dev/agent_collaboration.md` | 1 | staffing fact | kept: the same attribution sentence |
| `templates/core/dev/plans/_template.md` | 1 | ruled plan-review token | kept: the plan-security obligation sentence |
| `templates/modules/default-on/documentation_plan_template.md` | 1 | noise | kept: 'the adopter's AGENTS.md' routing text; 'Internal' there means the repo's own layer |
| `templates/modules/team-gated/dual-review.md` | 2 | stale description | fix in C7 |
| `templates/onboarding/collaborative-team.md` | 1 | noise | kept: the 'first-cross-type-review' trigger matches a vendor name in a review heading, not the word |

**authority probe** -- 9 files, 11 hits.

| File | Hits | Category | Disposition |
|---|---|---|---|
| `bootstrap/REANCHOR_RUNBOOK.md` | 2 | standing launcher-review call / noise | kept, byte-identical: the runbook is a ceremony document |
| `dev/modules/claim-check.md` | 1 | noise | kept: 'clear' is about flags or markers, 'external' is about scope |
| `dev/modules/doc-drift-prevention.md` | 1 | noise | kept: 'clear' is about flags or markers, 'external' is about scope |
| `docs/quickstart.md` | 1 | stale description | fix in C6 ('a second reviewer' is offered as a requirement-shaped step) |
| `doctrine/dual-review.md` | 2 | Maintainer-called definition / staffing fact | reworded in C4: neither privilege remains; the code-review floor is cleared by a same-type fresh session |
| `doctrine/lifecycle.md` | 1 | noise | kept: 'clear' is about flags or markers, 'external' is about scope |
| `templates/codebase-readiness-report.md` | 1 | noise | kept: 'clear' is about flags or markers, 'external' is about scope |
| `templates/modules/default-on/claim-check.md` | 1 | noise | kept: 'clear' is about flags or markers, 'external' is about scope |
| `templates/modules/team-gated/doc-drift-prevention.md` | 1 | noise | kept: 'clear' is about flags or markers, 'external' is about scope |


**Search C, a plain read** (`doctrine/rationale.md`, `doctrine/lifecycle.md`, `README.md`).
`rationale.md`: line 84 "independently" is noise; line 238 ("turned reviewer independence
into a structural, checkable tier") was a stale description and now reads "turned review
into a recorded, checkable step"; anchor 4 (lines 365 to 373) is replaced with the
accepted wording. `lifecycle.md`: line 189 `External-repo` is noise; line 282 "independent
eye" is generic and stays; line 307 named the wrong satisfier for a plan obligation and
now agrees with `doctrine/plans.md`; line 364 "delivery is independent" is noise.
`README.md` is read in C6.

**Files read and changed or not.** `doctrine/proposals.md` and `doctrine/lifecycle.md`
changed only where a search reached them: three phrases in `proposals.md` (the review
"tier" wording and the pointer sentence) and the satisfier paragraph and the `required(<tier>)`
token in `lifecycle.md`. `on-ramp/README.md` is not in the proposals' list and is
classified here as a stale description; it is fixed in C6, where the other entry-layer
pages are.

**The pre-existing flag.** `python scripts/check_cairn.py dev/modules/security-review.md`
reports one broken link (`content_scan.py`, line 181) at the parent of C1 as well. It is
not in a line this plan touches, and is left for the Maintainer's board.

## Deviation request -- Claude Sonnet 5.5 (implementer) -- 2026-10-19

**What cannot be met as written.** C7's *Expected checker flags* criterion says
`check_cairn.py` over the two archived source proposals reports "exactly two new
line-bound flags" at C7, "and nothing else new", and is red "when a flag appears
that is not these two". With the module thinned as C7 requires, it reports
**three**. The third is in the lenses proposal's Internal review (line 313): it
cites lines 136 to 144 of `templates/modules/team-gated/dual-review.md`, the module's
old four-item ledger, which the thinning removes. It is the same kind of flag as the
other two (a line-bound citation into the module, inside an archived append-only
record), and it appears for any thinned size below 144 lines, so the plan's own
"about 84" module would raise it too. The plan counted the stance proposal's two
citations and missed this one. Measured on a clean worktree of the parent of C7b
(three flags, all about the deleted test) and of C7b (those three plus these
three).

**Options.**

* **(A) Accept it, recommended.** Record the third flag beside the other two as
  expected, edit no archive, and finish C7b and C8 as planned. This changes
  neither scope nor any outcome; it corrects a count in a criterion.
* **(B) Keep the module at 144 lines or more.** This contradicts the accepted
  thinning (the lenses proposal's item 3) and keeps two definitions of the ledger.
* **(C) Edit the archived record.** It is append-only, and the plan already says
  not to.

**Where the work stands.** C7a landed (the presets, the deleted test, the preset
group). C7b is built and tested in a scratch worktree and kept, uncommitted to
`master`, at `refs/rsl/c7b-draft` (`5ce3b1dc`): the thinned module pair, now 59
lines each and byte-identical, the module and completeness groups, and the
scoped finalize of `dev/modules/dual-review.md` (lock count 18). 2741 mapped tests
pass on it. Two other readings for the Maintainer to see with this request: the
thinned module is 59 lines, not about 84, because the lens-9 satisfier text left
with the roster; and `check_module_body_coverage.py` reads 11 missing topics
after C7b against 8 at the base, because the probe matches doctrine heading text
and the thinned module no longer repeats three of those headings (the content
they name now sits in the review-loop document).

Untracked paths: `bootstrap/tests/test_onboarding_review_tiers.py` -- deleted by
C7a, so a fresh checkout does not carry it; this plan cites it throughout as the
frozen file whose removal the re-anchor must handle.

### Allowance -- Anthony Kendall (Maintainer), relayed by the coordinator -- 2026-10-19

The Maintainer answered the deviation request above. The question he was shown
and the option he chose, quoted verbatim and set apart:

> "The combined review plan's C7 thins the dual-review module, as accepted. One
> acceptance check expected exactly two 'stale line citation' flags in archived
> proposals afterwards, but a third appears: an archived review that cites the
> module's old line numbers. No archived file can be edited (append-only), so the
> criterion can't be met as written. How should the implementer proceed?"

> "Accept a 3rd expected flag (Recommended)" -- "Same kind as the other two: an
> archived record pointing at module lines that the accepted thinning removes. No
> archive is edited, and C7 and C8 finish as planned."

**The amended criterion.** C7's *Expected checker flags* now reads: `python
scripts/check_cairn.py` with the two archived source proposals named explicitly
reports exactly **three** new line-bound flags at C7 and nothing else new: the two
module citations in the stance proposal's Security Review (module lines 132-133
and 131-132) and the lenses proposal's Internal review (line 313, module lines
136-144), all in files that are now 59 lines. They are expected and recorded;
the records are append-only and are not edited. It is red when a flag appears
that is not these three. Everything else in C7 stands. The original cell above is
left as written, with a pointer to this amendment, because the plan's operative
cells are append-only once implementation has begun.

**Signals the plan defines, recorded here so the code reviewer can weigh them
(neither is a failure).** `AGENTS.md` grew by 49 lines per copy against the
40-line ceiling (the quoted called-read text alone is 28 lines). And
`check_module_body_coverage.py` reads 11 missing topics against 8 at the base,
because three doctrine headings the module used to repeat now live in the
review-loop document.

Untracked paths: `templates/modules/team-gated/dual-review.md:136-144` -- the old
module's ledger lines, quoted in the deviation request above; the thinned module
has 59 lines, so the range no longer exists.

## Implementation verification -- Claude Sonnet 5.5 (implementer) -- 2026-10-19

* **Boundary B mode**: `full`. A contract surface is touched (a frozen gate test is
  deleted, which drops five pinned nodes, and the fidelity manifest's sample roster
  is edited); two trust-ceremony adjacencies apply (the plan carries an Internal
  Security Review obligation, and vendor-neutrality and the install contract are
  high-risk surfaces in shipped prose); no mapping bounds 57 test files that render
  the shipped templates; both accepted proposals say `full`; the lockfile is touched
  by two scoped finalizes. Uncertainty resolves to `full`.
  **How it is met.** By the Maintainer's instruction of 2026-10-19 the full suite runs only as a
  certifying run, once per integration point (before a push, before his re-anchor ceremony, before
  the release cut, or when he asks), and one green run at a commit certifies every change at or
  before it. So where this plan asks for a full Boundary B, this scoped record plus that later
  certifying run satisfies it. This record lists what was run; it certifies nothing beyond that.
* **Certified by**: pending (the coordinator's certifying run).
* **Tested commit**: `fd66c988fff3250ac113943ee981fee2e511edb1` (C7b, the last commit
  that changes test bytes). Commits after it are prose only: one claim-marker maintenance
  commit (`f3abb787`, additions only) and this record.
* **Reviewed range**: base `92421911` (the Status commit, the parent of C1 `b69a9887`)
  to `fd66c988`: 43 commits, 12 mine and 31 not mine.
  * Mine, in order:
  * `b69a9887` review-stance-and-lenses C1: the carriers -- one stance at every stage, the review sweep in every install
  * `b5b049d0` review-stance-and-lenses C2: the authoring templates carry the stance and the called-read rules
  * `08c946a6` review-stance-and-lenses C3: roster, capability floors and the rest of the shipped text
  * `e4b4dbb5` review-stance-and-lenses C4: the doctrine states one stance, and the two old privileges are gone
  * `ac7d92f3` review-stance-and-lenses C5: the dimensions pages and the plan-pass example say one review
  * `2e1c9b3b` review-stance-and-lenses C6: the headline -- README, figure and descriptive pages say one review
  * `467ddcbd` review-stance-and-lenses C7a: the presets stop saying anyone fills a review tier; the old pin is retired
  * `5c77c11b` review-stance-and-lenses C2 fix: no one-word placeholder the engine cannot fill in the proposal template
  * `5ad39c5a` dev/PLANNING.md: declare the deleted frozen test as an untracked path
  * `96d967b4` review-stance-and-lenses: C7b stops for a deviation request -- a third expected checker flag
  * `8ccb8836` review-stance-and-lenses: the Maintainer allows a third expected checker flag; Waiting line removed
  * `fd66c988` review-stance-and-lenses C7b: the dual-review module is thinned; the lens text exists once
  * **Not mine, outside this plan's range though inside the tested tree** (31):
  * `f9e1d572` neutrality-and-upgrade-slots: response to code review (NU-CR1 to NU-CR8, NU-CSR1 to NU-CSR6)
  * `87607d28` strategy: core-and-two-profiles -- opened (draft)
  * `3c50940d` Review core-and-two-profiles strategy against committed contracts
  * `598aa6be` Security Review: session kernel writes (7e6a14e5) -- cleared, 9 findings
  * `960f90e3` Code review: session kernel writes (7e6a14e5) -- no blocking findings, 8 findings
  * `5ed51cdf` Code review: independent-scientific-check -- REVISE, 6 findings
  * `fce8e653` strategy: core-and-two-profiles -- append Antigravity review (assai split + crux v3.5)
  * `26653324` Release path: 0.4 goes public after the current batch, external test waived
  * `f949e342` verify_integrity: the existing report prints lockfile text escaped (the Maintainer's instruction)
  * `c504fca8` neutrality-and-upgrade-slots: addendum to the response -- the report's lockfile paths, at the Mainta
  * `86db42ae` independent-scientific-check: the test also pins layout and place (SC-CR1)
  * `e2978e44` independent-scientific-check: the promise sentences use the block's own gate (SC-CR4)
  * `550750fb` independent-scientific-check: the positive-control example matches rate, distance and schedule (SC-C
  * `1e4f1e96` Response to code review: independent-scientific-check -- all six findings taken
  * `c41edbad` Rewrite and rename strategy around Cairn and assai
  * `a95b9b31` Session kernel: a binding that git tracks is not run
  * `03c36a4b` neutrality-and-upgrade-slots: second implementation verification -- awaiting-code-review
  * `dc089258` Proposal open: remove the collaboration agreement
  * `cf707e2a` Installer fan-out: no copy, quarantine or probe write goes through a link or leaves the project
  * `c1c92ccc` independent-scientific-check: second Boundary B record; Status to awaiting-code-review
  * `a003bd4e` Security verification of the revision: neutrality-and-upgrade-slots -- cleared, 4 findings
  * `ba15a599` Design assai runtime architecture as a Cairn strategy note
  * `72248e15` Repository renamed: MSUHydrogeology/cairn-scientist-ai-teams -> MSUHydrogeology/cairn
  * `14f4403d` Verification of the revision: neutrality-and-upgrade-slots -- NU-CR1 to NU-CR8 closed, Status stays 
  * `42e41c84` Release path: board-as-basis and model-mapping-install-path join 0.4
  * `ab086789` verify_integrity: a line break from the lockfile cannot forge a report line; a failing stdout keeps 
  * `57ebfc13` Security Review: remove the collaboration agreement -- revise, 7 findings
  * `fcfaffc5` neutrality-and-upgrade-slots: correction to the second verification record, and the response to the 
  * `e12b22d9` Security Review: engine copy fallback (cf707e2a) -- cleared, 5 findings
  * `003dd23c` Verification of the revision: independent-scientific-check -- REVISE, 1 new finding (C1 briefs)
  * `cc887cd3` Review (Internal): remove the collaboration agreement -- REVISE, 6 findings
  * **None of those commits touches a hunk of mine, but six files in my chunk list were
    touched by both.** Each overlap, with the other commit and where its hunk sits:
    `dev/.cairn/cairn-lock.yml` (`a95b9b31`, one record at line 521; mine are the two module
    records); `dev/PLANNING.md` (`26653324`, `c41edbad`, `72248e15`, `42e41c84`, hunks from line 421
    on; mine is one added line block at 268); `dev/proposals/_template.md` and
    `templates/core/dev/proposals/_template.md` (`550750fb`, plan D's check block near line 297,
    after my Review section and before my pass skeleton); `dimensions/complexity.md` (`e2978e44`,
    plan D's wording, which my C5 kept verbatim); `docs/quickstart.md` (`72248e15`, the clone URL at
    line 61; mine is the Dual-Review bullet near line 316). Every hunk pair is disjoint, and the later
    commit of each pair was built on a tree that already held the earlier one. No other session's
    uncommitted hunk entered any of my commits: six commits (C3, C5, C6, C7a, the C2 fix and C7b)
    were built in a clean worktree and fast-forwarded for that reason, because the shared lockfile,
    `bootstrap/UPGRADE.md` and `docs/quickstart.md` carried other sessions' edits at the time.
* **Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13.
* **Pre-run state** and **Post-run state**: a detached worktree at `fd66c988`, created for this
  run in a uniquely named folder; `git status --short` printed nothing before the run and
  nothing after every leg; `HEAD` was `fd66c988` before and after. The gate anchor
  `refs/cairn/gate-anchor` (`bd66a70c`) was present through the shared refs.

| Command | Exit | Outcomes | Elapsed |
|---|---|---|---|
| `python -m pytest <the 50 owning and mapped test files>`, two batches of 25 (the broad-run guard allows 40 files), each under the shared run lock, no full-suite variable | 0, 0 | **3450 passed**, 0 failed, 0 skipped, 0 xfail, 0 xpass (batch A 2929 in 39.61 s; batch B 521 in 69.61 s) | 109 s of test time; 191 s with queueing |
| `python scripts/quality_gate.py --sub neutrality --sub redundancy` | 0 | neutrality `fail=0` (`info=56`); redundancy `fail=0` | 2 s |
| `python scripts/check_cairn.py` (whole tree, defaults) | 1 | 7 issues in 188 files at the tested commit: **3 caused by this plan** (the deleted test cited in a measurement record; this plan's own quotation of the old module range; the stewardship proposal's lens-5 line numbers) and 4 `tools/__pycache__` citations in other sessions' records. Clean (182 files) at the base. On master after `f3abb787` and this commit: **1 left**, the stewardship proposal's bullet (see Dispositions) | 4 s |
| `python scripts/check_cairn.py <the 58 edited .md paths>` | 1 | 2 issues: `dev/modules/security-review.md:181` (a broken link that predates this plan, see Dispositions) and this plan's own quotation of the old module range, which a claim marker cannot clear (a marker exempts a path, not a line range into a file that exists); this commit rewords that one phrase in the plan's own deviation request | 3 s |
| `python scripts/claim_check.py <file>` for each of the 58 edited documents | 0 | no flag in any (one prints an exemption note: the plan's declaration of the deleted test) | 3 s |
| `python bootstrap/scaffold.py --manifest`, `cmp` against the base output | 0 | byte-identical | <1 s |
| `python bootstrap/check_module_body_coverage.py --target . --cairn-root .` | 1 | **11 missing topics (8 at the base)**, see Signals | <1 s |
| `python bootstrap/verify_integrity.py --target .` | 1 | 18 violations, **the same 18 files as the base** | <1 s |
| `python bootstrap/tests/_ast_attest.py verify <baseline> bootstrap/_scaffold/*.py --known-new <known-new>` | 1 | base 5 symbols CHANGED, tested 7; none is this plan's (see AST) | <1 s |
| `python bootstrap/tests/_gate_manifest.py verify` | 1 | HOLD 449 at the base, 495 here; six of the 46 new lines are the retired test (see Frozen) | 7 s |

**The 50 files of the scoped run, with node counts at the tested commit** (the union of every chunk's owning
and mapped files from *Verification*; `test_onboarding_review_tiers` is gone with its test): `test_review_stance_in_shipped_files` 1850, `test_review_sweep_ships` 192, `test_review_and_verification_rules_ship` 125, `test_verification_boundaries` 40, `test_comprehension_floor` 10, `test_scope_reduction_trap` 99, `test_loop_fidelity_gate` 8, `test_documentation_plan_module` 15, `test_quickstart_sequence` 8, `test_scaffold` 67, `test_profiles_smoke` 15, `test_presets` 34, `test_onboarding_seed_roster` 7, `test_cairn_prefix_links` 3, `test_check_cairn_content` 4, `test_quality_gate_neutrality` 59, `test_manifest` 9, `test_module_roster` 1, `test_module_merge` 15, `test_merge_module` 6, `test_upgrade` 106, `test_lockfile_module` 7, `test_verify_integrity` 161, `test_claim_check_module` 78, `test_core_dev_folders` 10, `test_incident_trackers_module` 10, `test_install_module` 10, `test_session_routines` 26, `test_trigger_evaluation_action` 18, `test_replacement_tools` 20, `test_scientific_check_guidance_ships` 1, `test_model_selection_stub` 25, `test_upgrade_module` 10, `test_profile_grammar` 45, `test_security_stack` 131, `test_skills_install` 5, `test_skills_fanout` 9, `test_skills_upgrade` 11, `test_skills_self_heal` 11, `test_skill_contract` 6, `test_session_failsafe` 28, `test_first_session_report` 3, `test_onboarding_activation_helper` 31, `test_deferred_task_store` 6, `test_doc_governance` 27, `test_link_check_exclusions` 18, `test_onboarding_slot_substitution` 28, `test_active_surfacing_render` 13, `test_active_surfacing_mechanism` 8, `test_gate_manifest` 21.

**Non-pass disposition.**

* The scoped run had no failure, skip, xfail or xpass. `test_ast_attest.py` is not among the owning or
  mapped files (no engine file is edited), so the scoped set does not run it. The AST gate is red at
  the base for five engine symbols and for seven at the tested commit (below); **no
  `bootstrap/_scaffold/` file is edited by any commit of mine.** Its re-anchor is the Maintainer's and
  is owed whatever this plan does. The certifying run will show those two nodes red until then.
* `scripts/check_cairn.py` and `claim_check` findings are dispositioned in the table.
* The verifier, `verify_integrity` and the body-coverage probe exit 1 for reasons named in
  their rows; none is a new failure of this plan except the body-coverage count (a signal).

**One full run, made before the instruction, kept as information and not offered as certification.** I ran the
whole suite once at the tested commit in a clean worktree, with `--quality-gate-shuffle-seed=0`, before the
Maintainer's instruction arrived: **5773 passed, 2 failed, 0 skipped, in 855.02 s (0:14:15)**. The two
failures are the AST nodes above and no others; `test_a_t4_output_is_bounded` passed. It was red, so it
certifies nothing, and I have not repeated it.

**AST set, at the base and at the tested commit** (same command, each in its own worktree).
Base `92421911` (5): `_cmd_adopt_module` and `cmd_upgrade` in `upgrade.py`; `create_dev_tree`,
`seed_gitignore` in `install.py`; `main` in `cli.py`. Tested `fd66c988` (7): those five and
**two more**, `_emit_skill_copy_fallback` and `_symlinks_available` in `install.py`, added by
another session's engine commit (`cf707e2a`, the installer fan-out). My commits touch **0**
files under `bootstrap/_scaffold/`.

**Frozen files and the re-anchor (chunk M, Maintainer-only; not performed).**
`bootstrap/tests/test_onboarding_review_tiers.py` is deleted. Against the base the verifier gains
exactly one `FROZEN-MISSING` for it and five `COLLECTION-DROPPED`, one per node; against the
parent of C7a (the clean comparison) it gains exactly those six lines and HOLD goes 479 to 485.
`test_gate_manifest.py` stays green (21 passed in the full run), so nothing in the suite says a
re-anchor is owed; the board row says it. The other new lines against the base belong to other
sessions' test files (`test_lockfile_provenance.py`, `test_session_binding_untracked.py`,
`test_verify_integrity.py`). The three test files that freeze at the ceremony, by git blob id at the
tested commit (`git ls-tree fd66c988 -- <paths>`): `test_review_and_verification_rules_ship.py`
`fd948b657af4978d872aeb2eb674f5e43fd37983`; `test_review_stance_in_shipped_files.py`
`a7ae88e54988cfa99f1a2bd3a42c4cbb91020bfb`; `test_review_sweep_ships.py`
`80815dbbba19620a54b6fca75e363c73d8ec263c`. These are the bytes if no `revising-code` commit
changes a test; the archive note records them again at the code-reviewed commit. No frozen file
other than the retired one is touched by my commits (checked against `frozen_files`).

**Untouched surfaces, measured over the range.** `bootstrap/REANCHOR_RUNBOOK.md`, `reanchor.sh`,
`reanchor-launcher.template.sh` and `_gate_reanchor.py`: no change. `scripts/check_model_selection.py`,
its shipped twin and `dev/.cairn/model-selection-mapping.yml`: no change. `scaffold.py --manifest`:
byte-identical. Slot counts: shipped `AGENTS.md` 5, shipped loop document 3, both proposal templates 5,
both plan templates 3, Cairn's `AGENTS.md` and loop document 0, as at the base. Neutrality: zero at
the base, zero here. My commit `b5b049d0` (C2) touched the four templates and the stance test only.

**Plan-specific acceptance commands.** The searches (script text and calibration in the *Search
classification* above; the end state is the next section); the authority probe, re-run on the tested
commit: neither privilege remains (`doctrine/plans.md` "Tier ordering" and the confirming-pass clause
are gone, and the module clause is struck in both copies; each is a node in the stance test), and every
remaining hit is classified in the end-state section; the adopter rehearsal; and the mutation ledger.

### Mutation ledger (final state, `fd66c988`, real files edited in a separate worktree)

Control first, unmutated: the two new test files, **2042 passed in 9.39 s**. Each mutant edits one real
file, runs the same two files, and is restored. *Killed* means every node named in the criterion went
red; none survived and none was argued equivalent.

| Mutant | File | Named nodes red | Nodes red in all | Verdict |
|---|---|---|---|---|
| CONTROL (unmutated) | `--` | -- | 0 | GREEN |
| C1-1 delete lens 4 from the shipped loop document | `templates/core/dev/agent_collaboration.md` | 2/2 | 13 | KILLED |
| C1-2 delete the 'Not covered' half from the shipped loop document | `templates/core/dev/agent_collaboration.md` | 1/1 | 10 | KILLED |
| C1-3 delete the scope sentence from the shipped loop document | `templates/core/dev/agent_collaboration.md` | 1/1 | 12 | KILLED |
| C1-4 delete the 'Called by never confers authority' sentence from Cairn's AGENTS.md | `AGENTS.md` | 1/1 | 36 | KILLED |
| C1-5 delete the plan-obligation sentence from the shipped AGENTS.md | `templates/core/AGENTS.md` | 1/1 | 35 | KILLED |
| C1-6 add required(External) to Cairn's loop document | `dev/agent_collaboration.md` | 1/1 | 24 | KILLED |
| C2-1 delete the two-pass sentence from Cairn's proposal template | `dev/proposals/_template.md` | 1/1 | 27 | KILLED |
| C2-2 delete the obligation sentence from the shipped plan template | `templates/core/dev/plans/_template.md` | 1/1 | 31 | KILLED |
| C2-3 put a one-word placeholder back in the shipped proposal template | `templates/core/dev/proposals/_template.md` | 2/2 | 5 | KILLED |
| C7-1 restore the lens roster into the shipped module | `templates/modules/team-gated/dual-review.md` | 1/1 | 4 | KILLED |
| C7-2 restore the citation rule into Cairn's module | `dev/modules/dual-review.md` | 1/1 | 4 | KILLED |
| C7-3 restore the ledger into the shipped module | `templates/modules/team-gated/dual-review.md` | 1/1 | 4 | KILLED |
| C7-4 restore the privilege clause into Cairn's module | `dev/modules/dual-review.md` | 1/1 | 30 | KILLED |
| C7-5 put 'a human fills the External tier' into a shipped preset | `templates/onboarding/solo-greenfield.md` | 1/1 | 8 | KILLED |

The set claims the plan names for the code reviewer (every profile, every Search A root, every carrier)
are covered by the install group (3 profiles by 25 items), the carrier groups and the completeness
check, not re-mutated member by member here; Boundary C owns that.

### Adopter rehearsal (read-only; scratch copies; no real upgrade)

For LHM (`~/Code/lhm`, `d3b5bd0f`) and modflow_tools (`~/Code/modflow_tools`, `2f74ad30`): `git archive HEAD
dev AGENTS.md CLAUDE.md` into fresh folders, then `upgrade --plan` and `--stage` from Cairn at the base
(`92421911`) and at the tested commit (`fd66c988`), each in its own worktree. Neither repository changed:
`HEAD`, branch, the hash of `git status --porcelain --ignored`, the reflog tip, the stash count and the
index timestamp were identical before and after.

| | LHM, base | LHM, tested | modflow_tools, base | modflow_tools, tested |
|---|---|---|---|---|
| `AGENTS.md` | merges clean | **conflict, 1 hunk** | merges clean | merges clean |
| `dev/agent_collaboration.md` | conflict, 1 hunk | conflict, 1 hunk | merges clean | merges clean |
| `dev/modules/dual-review.md` | untouched | untouched | untouched | untouched |
| other conflicts | `dev/upstream/README.md` (1) | `dev/upstream/README.md` (1) | `dev/PLANNING.md` (1) | `dev/PLANNING.md` (1), **`dev/collaboration_agreement.md` (1)** |
| conflict hunks in all | 2 | 3 | 1 | 2 |

* **LHM, loop document.** As at the base, the hunk is LHM's own text (a decision-support round, its own
  clean-pass trap, its four-part ledger, briefs, restricted-verification and its HDF5 and MATLAB probes,
  117 lines) against an **empty** upstream side. The shipped sweep merges in above it with no markers.
  Until resolved the staged file therefore holds the shipped ledger and LHM's own, and the shipped
  clean-pass statement beside LHM's trap. That is the state the plan predicted; the advice resolves it:
  take the shipped sweep, keep the domain probes, drop LHM's duplicate ledger and clean-pass statement.
  One roster (one Reviewer role), the old Internal and External Reviewer role lines are gone.
* **modflow_tools, loop document, `AGENTS.md`, module.** Clean, as at the base. The staged loop document has
  one sweep, one ledger of five items, one Reviewer role, one trap, and no Internal or External Reviewer line.
* **Signal 1, outside the review-loop region: LHM `AGENTS.md`.** One hunk in "Git and commit workflow". My
  rewording of the last sentence of "Why this is stated positively" ("the review tier" became "what a review
  must show") sits directly above a bullet LHM added on its own ("Doctrine surfaces stay Maintainer-gated
  regardless"), so the two edits meet. Resolution is one line: take the upstream sentence and keep LHM's bullet.
  The plan's red-when names this case and says to report it, not hide it.
* **Signal 2, outside the region: modflow_tools `dev/collaboration_agreement.md`.** One hunk that covers the
  whole body: modflow_tools' agreement is entirely its own text (a shared purpose, core commitments, review
  norms), with no counterpart to the template's norms list. At the base upstream's file was unchanged, so the
  merge was clean; my one-sentence edit to the "Review is honest" norm (C3) is a change on both sides of a
  file that shares no text. Resolution: keep the local file; the changed sentence has no place in it.
* The conflicts in `dev/PLANNING.md` (modflow_tools) and `dev/upstream/README.md` (LHM) are the same at the base.

### Node IDs (`pytest --collect-only -q`, at the tested commit)

`bootstrap/tests/test_review_stance_in_shipped_files.py`: 1850 nodes.

```
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-call-names-one-artifact-that-exists-now-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-call-names-one-artifact-that-exists-now-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-called-brief-adds-focus-and-removes-no-owed-answer-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-called-brief-adds-focus-and-removes-no-owed-answer-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-called-by-line-never-confers-authority-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-called-by-line-never-confers-authority-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-called-read-adds-and-replaces-nothing-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-called-read-adds-and-replaces-nothing-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-called-read-discharges-no-security-review-by-distance-or-brief-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-called-read-discharges-no-security-review-by-distance-or-brief-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-clean-code-review-shows-a-falsification-ledger-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-clean-code-review-shows-a-falsification-ledger-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-clean-pass-needs-evidenced-answers-and-named-gaps-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-clean-pass-needs-evidenced-answers-and-named-gaps-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-fresh-reviewer-on-the-works-side-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-fresh-reviewer-on-the-works-side-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-high-risk-surface-takes-a-security-review-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-high-risk-surface-takes-a-security-review-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-narrowing-is-a-scope-change-only-the-maintainer-concedes-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-narrowing-is-a-scope-change-only-the-maintainer-concedes-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-plan-security-obligation-is-cleared-only-by-a-matching-obligation-line-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-plan-security-obligation-is-cleared-only-by-a-matching-obligation-line-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-roster-you-set-is-not-a-call-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-roster-you-set-is-not-a-call-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-standing-call-is-a-floor-and-returns-only-by-proposal-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[a-standing-call-is-a-floor-and-returns-only-by-proposal-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[called-by-carries-the-maintainers-words-verbatim-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[called-by-carries-the-maintainers-words-verbatim-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[called-by-names-where-the-words-live-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[called-by-names-where-the-words-live-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[called-by-quote-is-repeated-in-the-commit-body-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[called-by-quote-is-repeated-in-the-commit-body-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[code-review-floor-is-not-the-implementing-agent-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[code-review-floor-is-not-the-implementing-agent-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[code-review-never-reopens-the-decision-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[code-review-never-reopens-the-decision-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[distance-is-information-and-the-staffing-reviewer-follows-the-brief-and-says-so-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[distance-is-information-and-the-staffing-reviewer-follows-the-brief-and-says-so-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[external-means-the-maintainer-called-it-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[external-means-the-maintainer-called-it-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[foundations-block-three-answers-each-with-its-evidence-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[foundations-block-three-answers-each-with-its-evidence-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[improve-means-recommend-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[improve-means-recommend-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[no-agent-declares-external-required-or-recommends-distance-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[no-agent-declares-external-required-or-recommends-distance-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[no-quota-of-findings-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[no-quota-of-findings-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[no-tool-reads-the-obligation-line-a-reader-does-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[no-tool-reads-the-obligation-line-a-reader-does-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[nothing-checks-the-quote-a-reader-does-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[nothing-checks-the-quote-a-reader-does-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[one-stance-at-every-stage-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[one-stance-at-every-stage-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[other-authority-lives-in-a-decision-or-a-plan-fence-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[other-authority-lives-in-a-decision-or-a-plan-fence-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[the-stage-sets-three-questions-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[the-stage-sets-three-questions-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[tier-external-needs-called-by-else-read-as-the-usual-review-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[tier-external-needs-called-by-else-read-as-the-usual-review-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[usual-plus-security-review-is-two-passes-and-the-usual-pass-never-clears-the-second-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation[usual-plus-security-review-is-two-passes-and-the-usual-pass-never-clears-the-second-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-call-names-one-artifact-that-exists-now-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-call-names-one-artifact-that-exists-now-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-called-brief-adds-focus-and-removes-no-owed-answer-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-called-brief-adds-focus-and-removes-no-owed-answer-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-called-by-line-never-confers-authority-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-called-by-line-never-confers-authority-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-called-read-adds-and-replaces-nothing-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-called-read-adds-and-replaces-nothing-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-called-read-discharges-no-security-review-by-distance-or-brief-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-called-read-discharges-no-security-review-by-distance-or-brief-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-clean-code-review-shows-a-falsification-ledger-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-clean-code-review-shows-a-falsification-ledger-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-clean-pass-needs-evidenced-answers-and-named-gaps-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-clean-pass-needs-evidenced-answers-and-named-gaps-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-fresh-reviewer-on-the-works-side-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-fresh-reviewer-on-the-works-side-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-high-risk-surface-takes-a-security-review-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-high-risk-surface-takes-a-security-review-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-narrowing-is-a-scope-change-only-the-maintainer-concedes-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-narrowing-is-a-scope-change-only-the-maintainer-concedes-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-plan-security-obligation-is-cleared-only-by-a-matching-obligation-line-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-plan-security-obligation-is-cleared-only-by-a-matching-obligation-line-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-roster-you-set-is-not-a-call-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-roster-you-set-is-not-a-call-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-standing-call-is-a-floor-and-returns-only-by-proposal-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[a-standing-call-is-a-floor-and-returns-only-by-proposal-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[called-by-carries-the-maintainers-words-verbatim-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[called-by-carries-the-maintainers-words-verbatim-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[called-by-names-where-the-words-live-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[called-by-names-where-the-words-live-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[called-by-quote-is-repeated-in-the-commit-body-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[called-by-quote-is-repeated-in-the-commit-body-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[code-review-floor-is-not-the-implementing-agent-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[code-review-floor-is-not-the-implementing-agent-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[code-review-never-reopens-the-decision-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[code-review-never-reopens-the-decision-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[distance-is-information-and-the-staffing-reviewer-follows-the-brief-and-says-so-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[distance-is-information-and-the-staffing-reviewer-follows-the-brief-and-says-so-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[external-means-the-maintainer-called-it-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[external-means-the-maintainer-called-it-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[foundations-block-three-answers-each-with-its-evidence-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[foundations-block-three-answers-each-with-its-evidence-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[improve-means-recommend-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[improve-means-recommend-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[no-agent-declares-external-required-or-recommends-distance-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[no-agent-declares-external-required-or-recommends-distance-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[no-quota-of-findings-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[no-quota-of-findings-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[no-tool-reads-the-obligation-line-a-reader-does-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[no-tool-reads-the-obligation-line-a-reader-does-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[nothing-checks-the-quote-a-reader-does-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[nothing-checks-the-quote-a-reader-does-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[one-stance-at-every-stage-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[one-stance-at-every-stage-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[other-authority-lives-in-a-decision-or-a-plan-fence-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[other-authority-lives-in-a-decision-or-a-plan-fence-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[the-stage-sets-three-questions-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[the-stage-sets-three-questions-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[tier-external-needs-called-by-else-read-as-the-usual-review-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[tier-external-needs-called-by-else-read-as-the-usual-review-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[usual-plus-security-review-is-two-passes-and-the-usual-pass-never-clears-the-second-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_the_obligation_is_reported[usual-plus-security-review-is-two-passes-and-the-usual-pass-never-clears-the-second-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_stance_sits_in_the_review_section_only_once[shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_stance_sits_in_the_review_section_only_once[own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_loop_document_roster_carries_the_obligation[a-fresh-session-is-every-reviews-floor-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_loop_document_roster_carries_the_obligation[a-fresh-session-is-every-reviews-floor-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_loop_document_roster_carries_the_obligation[distance-is-read-from-attribution-and-the-maintainer-may-ask-for-more-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_loop_document_roster_carries_the_obligation[distance-is-read-from-attribution-and-the-maintainer-may-ask-for-more-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_loop_document_roster_carries_the_obligation[one-reviewer-role-on-the-works-side-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_loop_document_roster_carries_the_obligation[one-reviewer-role-on-the-works-side-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_loop_document_roster_carries_the_obligation[security-review-and-user-agent-stay-on-the-roster-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_loop_document_roster_carries_the_obligation[security-review-and-user-agent-stay-on-the-roster-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_loop_document_roster_carries_the_obligation[the-reviewer-carries-the-neutral-briefing-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_loop_document_roster_carries_the_obligation[the-reviewer-carries-the-neutral-briefing-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_roster_obligation_is_reported[a-fresh-session-is-every-reviews-floor-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_roster_obligation_is_reported[a-fresh-session-is-every-reviews-floor-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_roster_obligation_is_reported[distance-is-read-from-attribution-and-the-maintainer-may-ask-for-more-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_roster_obligation_is_reported[distance-is-read-from-attribution-and-the-maintainer-may-ask-for-more-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_roster_obligation_is_reported[one-reviewer-role-on-the-works-side-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_roster_obligation_is_reported[one-reviewer-role-on-the-works-side-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_roster_obligation_is_reported[security-review-and-user-agent-stay-on-the-roster-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_roster_obligation_is_reported[security-review-and-user-agent-stay-on-the-roster-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_roster_obligation_is_reported[the-reviewer-carries-the-neutral-briefing-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_roster_obligation_is_reported[the-reviewer-carries-the-neutral-briefing-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_carrier_omits_the_old_vocabulary[shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_carrier_omits_the_old_vocabulary[own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_carrier_omits_the_old_vocabulary[shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_carrier_omits_the_old_vocabulary[own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[a-different-agent-type-pass-or-round-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[a-different-agent-type-pass-or-round-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[a-different-agent-type-pass-or-round-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[a-different-agent-type-pass-or-round-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[a-human-fills-a-tier-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[a-human-fills-a-tier-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[a-human-fills-a-tier-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[a-human-fills-a-tier-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[a-tool-is-credited-with-checking-the-quote-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[a-tool-is-credited-with-checking-the-quote-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[a-tool-is-credited-with-checking-the-quote-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[a-tool-is-credited-with-checking-the-quote-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[across-structural-independence-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[across-structural-independence-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[across-structural-independence-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[across-structural-independence-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[code-review-is-not-external-by-default-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[code-review-is-not-external-by-default-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[code-review-is-not-external-by-default-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[code-review-is-not-external-by-default-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[declared-external-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[declared-external-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[declared-external-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[declared-external-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[escalate-to-the-external-tier-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[escalate-to-the-external-tier-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[escalate-to-the-external-tier-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[escalate-to-the-external-tier-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-code-review-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-code-review-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-code-review-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-code-review-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-floor-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-floor-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-floor-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-floor-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-independence-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-independence-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-independence-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-independence-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-review-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-review-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-review-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-review-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-review-norms-heading-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-review-norms-heading-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-review-norms-heading-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-review-norms-heading-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-stance-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-stance-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-stance-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-stance-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-tier-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-tier-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-tier-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[external-tier-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[internal-reviewer-role-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[internal-reviewer-role-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[internal-reviewer-role-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[internal-reviewer-role-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[required-external-in-a-header-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[required-external-in-a-header-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[required-external-in-a-header-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[required-external-in-a-header-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[the-checker-cannot-parse-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[the-checker-cannot-parse-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[the-checker-cannot-parse-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[the-checker-cannot-parse-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[the-reviewer-tiers-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[the-reviewer-tiers-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[the-reviewer-tiers-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[the-reviewer-tiers-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[tiers-are-stances-sentence-shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[tiers-are-stances-sentence-own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[tiers-are-stances-sentence-shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_is_reported[tiers-are-stances-sentence-own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_by_default_pin_ignores_case_and_wrapping[plain]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_by_default_pin_ignores_case_and_wrapping[capitals]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_by_default_pin_ignores_case_and_wrapping[wrapped]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_by_default_pin_ignores_case_and_wrapping[hyphenated]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_sentence_saying_no_tool_reads_the_line_is_not_flagged
bootstrap/tests/test_review_stance_in_shipped_files.py::test_module_omits_the_old_vocabulary[shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_module_omits_the_old_vocabulary[own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[a-confirming-pass-never-stands-in-for-a-falsification-ledger-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[a-confirming-pass-never-stands-in-for-a-falsification-ledger-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[a-different-agent-type-pass-or-round-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[a-different-agent-type-pass-or-round-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[a-human-fills-a-tier-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[a-human-fills-a-tier-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[a-structurally-independent-tier-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[a-structurally-independent-tier-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[a-tool-is-credited-with-checking-the-quote-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[a-tool-is-credited-with-checking-the-quote-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[across-structural-independence-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[across-structural-independence-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[code-review-is-not-external-by-default-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[code-review-is-not-external-by-default-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[declared-external-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[declared-external-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[escalate-to-the-external-tier-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[escalate-to-the-external-tier-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[external-code-review-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[external-code-review-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[external-floor-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[external-floor-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[external-independence-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[external-independence-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[external-review-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[external-review-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[external-review-norms-heading-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[external-review-norms-heading-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[external-stance-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[external-stance-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[external-tier-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[external-tier-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[internal-reviewer-role-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[internal-reviewer-role-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[make-it-prove-itself-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[make-it-prove-itself-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[required-external-in-a-header-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[required-external-in-a-header-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[the-checker-cannot-parse-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[the-checker-cannot-parse-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[the-reviewer-tiers-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[the-reviewer-tiers-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[tiers-are-stances-sentence-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_the_module_is_reported[tiers-are-stances-sentence-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_module_says_what_it_is_for[agents-md-holds-the-one-definition-of-the-call-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_module_says_what_it_is_for[the-module-is-for-staffing-a-read-the-maintainer-called-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_module_says_what_it_is_for[the-module-never-lets-an-agent-pick-a-reviewer-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_module_says_what_it_is_for[the-sweep-and-the-trap-are-in-every-install-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_module_says_what_it_is_for[agents-md-holds-the-one-definition-of-the-call-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_module_says_what_it_is_for[the-module-is-for-staffing-a-read-the-maintainer-called-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_module_says_what_it_is_for[the-module-never-lets-an-agent-pick-a-reviewer-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_module_says_what_it_is_for[the-sweep-and-the-trap-are-in-every-install-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_module_statement_is_reported[agents-md-holds-the-one-definition-of-the-call-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_module_statement_is_reported[the-module-is-for-staffing-a-read-the-maintainer-called-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_module_statement_is_reported[the-module-never-lets-an-agent-pick-a-reviewer-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_module_statement_is_reported[the-sweep-and-the-trap-are-in-every-install-shipped-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_module_statement_is_reported[agents-md-holds-the-one-definition-of-the-call-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_module_statement_is_reported[the-module-is-for-staffing-a-read-the-maintainer-called-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_module_statement_is_reported[the-module-never-lets-an-agent-pick-a-reviewer-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_module_statement_is_reported[the-sweep-and-the-trap-are-in-every-install-own-module]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_deleting_the_called_by_authority_sentence_is_reported[shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_deleting_the_called_by_authority_sentence_is_reported[own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_deleting_the_plan_obligation_sentence_is_reported[shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_deleting_the_plan_obligation_sentence_is_reported[own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_deleting_the_two_pass_sentence_is_reported[shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_deleting_the_two_pass_sentence_is_reported[own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_adding_required_external_to_a_carrier_is_reported[shipped-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_adding_required_external_to_a_carrier_is_reported[own-agents]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_adding_required_external_to_a_carrier_is_reported[shipped-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_adding_required_external_to_a_carrier_is_reported[own-loop]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-call-names-one-artifact-that-exists-now-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-called-brief-adds-focus-and-removes-no-owed-answer-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-called-by-line-never-confers-authority-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-called-read-adds-and-replaces-nothing-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-called-read-discharges-no-security-review-by-distance-or-brief-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-clean-pass-needs-evidenced-answers-and-named-gaps-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-fresh-reviewer-on-the-works-side-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-high-risk-surface-takes-a-security-review-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-proposal-review-asks-whether-it-should-exist-as-framed-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-roster-you-set-is-not-a-call-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-standing-call-is-a-floor-and-returns-only-by-proposal-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[called-by-carries-the-maintainers-words-verbatim-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[called-by-names-where-the-words-live-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[called-by-quote-is-repeated-in-the-commit-body-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[distance-is-information-and-the-staffing-reviewer-follows-the-brief-and-says-so-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[external-means-the-maintainer-called-it-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[foundations-block-three-answers-each-with-its-evidence-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[improve-means-recommend-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[no-agent-declares-external-required-or-recommends-distance-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[no-quota-of-findings-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[nothing-checks-the-quote-a-reader-does-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[one-stance-at-every-stage-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[other-authority-lives-in-a-decision-or-a-plan-fence-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[tier-external-needs-called-by-else-read-as-the-usual-review-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[usual-plus-security-review-is-two-passes-and-the-usual-pass-never-clears-the-second-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-call-names-one-artifact-that-exists-now-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-called-brief-adds-focus-and-removes-no-owed-answer-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-called-by-line-never-confers-authority-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-called-read-adds-and-replaces-nothing-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-called-read-discharges-no-security-review-by-distance-or-brief-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-clean-pass-needs-evidenced-answers-and-named-gaps-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-fresh-reviewer-on-the-works-side-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-high-risk-surface-takes-a-security-review-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-proposal-review-asks-whether-it-should-exist-as-framed-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-roster-you-set-is-not-a-call-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-standing-call-is-a-floor-and-returns-only-by-proposal-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[called-by-carries-the-maintainers-words-verbatim-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[called-by-names-where-the-words-live-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[called-by-quote-is-repeated-in-the-commit-body-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[distance-is-information-and-the-staffing-reviewer-follows-the-brief-and-says-so-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[external-means-the-maintainer-called-it-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[foundations-block-three-answers-each-with-its-evidence-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[improve-means-recommend-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[no-agent-declares-external-required-or-recommends-distance-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[no-quota-of-findings-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[nothing-checks-the-quote-a-reader-does-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[one-stance-at-every-stage-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[other-authority-lives-in-a-decision-or-a-plan-fence-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[tier-external-needs-called-by-else-read-as-the-usual-review-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[usual-plus-security-review-is-two-passes-and-the-usual-pass-never-clears-the-second-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-call-names-one-artifact-that-exists-now-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-called-brief-adds-focus-and-removes-no-owed-answer-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-called-by-line-never-confers-authority-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-called-read-adds-and-replaces-nothing-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-called-read-discharges-no-security-review-by-distance-or-brief-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-clean-code-review-shows-a-falsification-ledger-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-clean-pass-needs-evidenced-answers-and-named-gaps-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-code-review-asks-whether-it-does-what-it-claims-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-fresh-reviewer-on-the-works-side-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-plan-review-asks-whether-the-plan-delivers-the-decision-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-plan-security-obligation-is-cleared-only-by-a-matching-obligation-line-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-roster-you-set-is-not-a-call-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-standing-call-is-a-floor-and-returns-only-by-proposal-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[called-by-carries-the-maintainers-words-verbatim-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[called-by-names-where-the-words-live-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[called-by-quote-is-repeated-in-the-commit-body-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[code-review-floor-is-not-the-implementing-agent-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[code-review-never-reopens-the-decision-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[distance-is-information-and-the-staffing-reviewer-follows-the-brief-and-says-so-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[external-means-the-maintainer-called-it-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[foundations-block-three-answers-each-with-its-evidence-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[improve-means-recommend-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[no-agent-declares-external-required-or-recommends-distance-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[no-quota-of-findings-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[no-tool-reads-the-obligation-line-a-reader-does-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[nothing-checks-the-quote-a-reader-does-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[one-stance-at-every-stage-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[other-authority-lives-in-a-decision-or-a-plan-fence-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[tier-external-needs-called-by-else-read-as-the-usual-review-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-call-names-one-artifact-that-exists-now-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-called-brief-adds-focus-and-removes-no-owed-answer-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-called-by-line-never-confers-authority-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-called-read-adds-and-replaces-nothing-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-called-read-discharges-no-security-review-by-distance-or-brief-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-clean-code-review-shows-a-falsification-ledger-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-clean-pass-needs-evidenced-answers-and-named-gaps-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-code-review-asks-whether-it-does-what-it-claims-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-fresh-reviewer-on-the-works-side-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-plan-review-asks-whether-the-plan-delivers-the-decision-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-plan-security-obligation-is-cleared-only-by-a-matching-obligation-line-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-roster-you-set-is-not-a-call-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[a-standing-call-is-a-floor-and-returns-only-by-proposal-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[called-by-carries-the-maintainers-words-verbatim-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[called-by-names-where-the-words-live-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[called-by-quote-is-repeated-in-the-commit-body-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[code-review-floor-is-not-the-implementing-agent-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[code-review-never-reopens-the-decision-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[distance-is-information-and-the-staffing-reviewer-follows-the-brief-and-says-so-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[external-means-the-maintainer-called-it-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[foundations-block-three-answers-each-with-its-evidence-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[improve-means-recommend-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[no-agent-declares-external-required-or-recommends-distance-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[no-quota-of-findings-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[no-tool-reads-the-obligation-line-a-reader-does-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[nothing-checks-the-quote-a-reader-does-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[one-stance-at-every-stage-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[other-authority-lives-in-a-decision-or-a-plan-fence-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_review_section_carries_the_obligation[tier-external-needs-called-by-else-read-as-the-usual-review-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-call-names-one-artifact-that-exists-now-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-called-brief-adds-focus-and-removes-no-owed-answer-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-called-by-line-never-confers-authority-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-called-read-adds-and-replaces-nothing-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-called-read-discharges-no-security-review-by-distance-or-brief-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-clean-pass-needs-evidenced-answers-and-named-gaps-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-fresh-reviewer-on-the-works-side-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-high-risk-surface-takes-a-security-review-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-proposal-review-asks-whether-it-should-exist-as-framed-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-roster-you-set-is-not-a-call-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-standing-call-is-a-floor-and-returns-only-by-proposal-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[called-by-carries-the-maintainers-words-verbatim-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[called-by-names-where-the-words-live-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[called-by-quote-is-repeated-in-the-commit-body-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[distance-is-information-and-the-staffing-reviewer-follows-the-brief-and-says-so-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[external-means-the-maintainer-called-it-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[foundations-block-three-answers-each-with-its-evidence-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[improve-means-recommend-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[no-agent-declares-external-required-or-recommends-distance-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[no-quota-of-findings-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[nothing-checks-the-quote-a-reader-does-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[one-stance-at-every-stage-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[other-authority-lives-in-a-decision-or-a-plan-fence-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[tier-external-needs-called-by-else-read-as-the-usual-review-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[usual-plus-security-review-is-two-passes-and-the-usual-pass-never-clears-the-second-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-call-names-one-artifact-that-exists-now-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-called-brief-adds-focus-and-removes-no-owed-answer-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-called-by-line-never-confers-authority-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-called-read-adds-and-replaces-nothing-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-called-read-discharges-no-security-review-by-distance-or-brief-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-clean-pass-needs-evidenced-answers-and-named-gaps-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-fresh-reviewer-on-the-works-side-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-high-risk-surface-takes-a-security-review-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-proposal-review-asks-whether-it-should-exist-as-framed-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-roster-you-set-is-not-a-call-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-standing-call-is-a-floor-and-returns-only-by-proposal-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[called-by-carries-the-maintainers-words-verbatim-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[called-by-names-where-the-words-live-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[called-by-quote-is-repeated-in-the-commit-body-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[distance-is-information-and-the-staffing-reviewer-follows-the-brief-and-says-so-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[external-means-the-maintainer-called-it-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[foundations-block-three-answers-each-with-its-evidence-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[improve-means-recommend-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[no-agent-declares-external-required-or-recommends-distance-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[no-quota-of-findings-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[nothing-checks-the-quote-a-reader-does-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[one-stance-at-every-stage-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[other-authority-lives-in-a-decision-or-a-plan-fence-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[tier-external-needs-called-by-else-read-as-the-usual-review-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[usual-plus-security-review-is-two-passes-and-the-usual-pass-never-clears-the-second-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-call-names-one-artifact-that-exists-now-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-called-brief-adds-focus-and-removes-no-owed-answer-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-called-by-line-never-confers-authority-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-called-read-adds-and-replaces-nothing-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-called-read-discharges-no-security-review-by-distance-or-brief-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-clean-code-review-shows-a-falsification-ledger-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-clean-pass-needs-evidenced-answers-and-named-gaps-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-code-review-asks-whether-it-does-what-it-claims-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-fresh-reviewer-on-the-works-side-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-plan-review-asks-whether-the-plan-delivers-the-decision-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-plan-security-obligation-is-cleared-only-by-a-matching-obligation-line-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-roster-you-set-is-not-a-call-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-standing-call-is-a-floor-and-returns-only-by-proposal-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[called-by-carries-the-maintainers-words-verbatim-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[called-by-names-where-the-words-live-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[called-by-quote-is-repeated-in-the-commit-body-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[code-review-floor-is-not-the-implementing-agent-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[code-review-never-reopens-the-decision-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[distance-is-information-and-the-staffing-reviewer-follows-the-brief-and-says-so-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[external-means-the-maintainer-called-it-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[foundations-block-three-answers-each-with-its-evidence-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[improve-means-recommend-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[no-agent-declares-external-required-or-recommends-distance-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[no-quota-of-findings-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[no-tool-reads-the-obligation-line-a-reader-does-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[nothing-checks-the-quote-a-reader-does-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[one-stance-at-every-stage-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[other-authority-lives-in-a-decision-or-a-plan-fence-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[tier-external-needs-called-by-else-read-as-the-usual-review-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-call-names-one-artifact-that-exists-now-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-called-brief-adds-focus-and-removes-no-owed-answer-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-called-by-line-never-confers-authority-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-called-read-adds-and-replaces-nothing-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-called-read-discharges-no-security-review-by-distance-or-brief-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-clean-code-review-shows-a-falsification-ledger-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-clean-pass-needs-evidenced-answers-and-named-gaps-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-code-review-asks-whether-it-does-what-it-claims-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-fresh-reviewer-on-the-works-side-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-plan-review-asks-whether-the-plan-delivers-the-decision-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-plan-security-obligation-is-cleared-only-by-a-matching-obligation-line-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-roster-you-set-is-not-a-call-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[a-standing-call-is-a-floor-and-returns-only-by-proposal-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[called-by-carries-the-maintainers-words-verbatim-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[called-by-names-where-the-words-live-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[called-by-quote-is-repeated-in-the-commit-body-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[code-review-floor-is-not-the-implementing-agent-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[code-review-never-reopens-the-decision-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[distance-is-information-and-the-staffing-reviewer-follows-the-brief-and-says-so-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[external-means-the-maintainer-called-it-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[foundations-block-three-answers-each-with-its-evidence-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[improve-means-recommend-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[no-agent-declares-external-required-or-recommends-distance-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[no-quota-of-findings-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[no-tool-reads-the-obligation-line-a-reader-does-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[nothing-checks-the-quote-a-reader-does-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[one-stance-at-every-stage-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[other-authority-lives-in-a-decision-or-a-plan-fence-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_template_obligation_is_reported[tier-external-needs-called-by-else-read-as-the-usual-review-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_omits_the_old_vocabulary[shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_omits_the_old_vocabulary[own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_omits_the_old_vocabulary[shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_template_omits_the_old_vocabulary[own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[a-different-agent-type-pass-or-round-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[a-different-agent-type-pass-or-round-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[a-different-agent-type-pass-or-round-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[a-different-agent-type-pass-or-round-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[a-human-fills-a-tier-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[a-human-fills-a-tier-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[a-human-fills-a-tier-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[a-human-fills-a-tier-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[a-plan-review-is-internal-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[a-plan-review-is-internal-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[a-plan-review-is-internal-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[a-plan-review-is-internal-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[a-same-type-agent-in-an-independent-context-clears-the-floor-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[a-same-type-agent-in-an-independent-context-clears-the-floor-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[a-same-type-agent-in-an-independent-context-clears-the-floor-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[a-same-type-agent-in-an-independent-context-clears-the-floor-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[a-tool-is-credited-with-checking-the-quote-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[a-tool-is-credited-with-checking-the-quote-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[a-tool-is-credited-with-checking-the-quote-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[a-tool-is-credited-with-checking-the-quote-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[across-structural-independence-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[across-structural-independence-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[across-structural-independence-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[across-structural-independence-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[code-review-is-not-external-by-default-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[code-review-is-not-external-by-default-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[code-review-is-not-external-by-default-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[code-review-is-not-external-by-default-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[declared-external-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[declared-external-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[declared-external-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[declared-external-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[escalate-to-the-external-tier-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[escalate-to-the-external-tier-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[escalate-to-the-external-tier-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[escalate-to-the-external-tier-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-code-review-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-code-review-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-code-review-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-code-review-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-floor-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-floor-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-floor-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-floor-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-independence-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-independence-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-independence-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-independence-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-review-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-review-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-review-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-review-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-review-norms-heading-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-review-norms-heading-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-review-norms-heading-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-review-norms-heading-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-stance-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-stance-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-stance-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-stance-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-tier-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-tier-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-tier-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[external-tier-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[internal-review-strengthens-the-change-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[internal-review-strengthens-the-change-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[internal-review-strengthens-the-change-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[internal-review-strengthens-the-change-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[internal-reviewer-role-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[internal-reviewer-role-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[internal-reviewer-role-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[internal-reviewer-role-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[required-external-in-a-header-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[required-external-in-a-header-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[required-external-in-a-header-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[required-external-in-a-header-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[the-checker-cannot-parse-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[the-checker-cannot-parse-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[the-checker-cannot-parse-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[the-checker-cannot-parse-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[the-reviewer-tiers-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[the-reviewer-tiers-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[the-reviewer-tiers-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[the-reviewer-tiers-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[tiers-are-stances-sentence-shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[tiers-are-stances-sentence-own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[tiers-are-stances-sentence-shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_the_old_wording_into_a_template_is_reported[tiers-are-stances-sentence-own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_proposal_header_offers_only_usual_values[shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_proposal_header_offers_only_usual_values[own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_plan_templates_keep_their_ruled_review_tokens[shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_plan_templates_keep_their_ruled_review_tokens[own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_template_offers_external_only_beside_called_by[shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_template_offers_external_only_beside_called_by[own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_template_offers_external_only_beside_called_by[shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_template_offers_external_only_beside_called_by[own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_proposal_pass_skeleton_asks_the_proposal_questions[shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_proposal_pass_skeleton_asks_the_proposal_questions[own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_plan_pass_skeletons_ask_the_plan_and_code_questions[shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_plan_pass_skeletons_ask_the_plan_and_code_questions[own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_template_has_no_coverage_line_stanza[shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_template_has_no_coverage_line_stanza[own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_template_has_no_coverage_line_stanza[shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_template_has_no_coverage_line_stanza[own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_deleting_the_two_pass_sentence_from_a_proposal_template_is_reported[shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_deleting_the_two_pass_sentence_from_a_proposal_template_is_reported[own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_deleting_the_obligation_sentence_from_a_plan_template_is_reported[shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_deleting_the_obligation_sentence_from_a_plan_template_is_reported[own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[review-honesty-questions-foundations-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[review-honesty-questions-foundations-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[the-roster-slot-states-the-teams-shape-only-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[bright-line-keeps-the-high-risk-trust-boundaries-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[cleanup-keeps-the-reviews-stage-floor-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[cleanup-may-be-written-at-low-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[cleanup-on-a-high-risk-surface-still-owes-its-security-review-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[code-review-floor-is-medium-and-not-the-implementing-agent-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[condition-a-is-a-different-model-architecture-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[conditions-b-c-and-d-are-unchanged-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[diversity-within-tier-is-distance-on-request-not-a-default-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[plan-review-floor-is-medium-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[proposal-review-floor-is-high-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[security-review-floor-is-high-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[the-cleanup-row-is-the-only-exception-and-only-for-the-writing-step-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[the-cost-rule-check-is-not-a-review-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[the-data-governance-gate-applies-first-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[the-exclusion-list-is-unchanged-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[bright-line-keeps-the-high-risk-trust-boundaries-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[cleanup-keeps-the-reviews-stage-floor-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[cleanup-may-be-written-at-low-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[cleanup-on-a-high-risk-surface-still-owes-its-security-review-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[code-review-floor-is-medium-and-not-the-implementing-agent-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[condition-a-is-a-different-model-architecture-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[conditions-b-c-and-d-are-unchanged-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[diversity-within-tier-is-distance-on-request-not-a-default-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[plan-review-floor-is-medium-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[proposal-review-floor-is-high-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[security-review-floor-is-high-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[the-cleanup-row-is-the-only-exception-and-only-for-the-writing-step-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[the-cost-rule-check-is-not-a-review-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[the-data-governance-gate-applies-first-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[the-exclusion-list-is-unchanged-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[the-reviewer-surfaces-the-list-the-author-decides-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[the-reviewer-surfaces-the-list-the-author-decides-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[peer-review-gates-are-a-fresh-reviewer-at-every-stage-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[the-board-columns-are-named-by-what-they-are-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[the-board-columns-are-named-by-what-they-are-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[the-kernel-review-is-a-fresh-reviewer-who-did-not-write-the-work-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[the-module-adds-guidance-for-staffing-a-called-read-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[a-change-is-reviewed-by-an-independent-reviewer-beside-its-author-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[every-change-is-reviewed-by-a-fresh-reviewer-who-did-not-write-it-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_carries_the_obligation[the-maintainer-may-ask-for-more-distance-on-one-named-piece-of-work-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[review-honesty-questions-foundations-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[review-honesty-questions-foundations-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[the-roster-slot-states-the-teams-shape-only-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[bright-line-keeps-the-high-risk-trust-boundaries-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[cleanup-keeps-the-reviews-stage-floor-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[cleanup-may-be-written-at-low-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[cleanup-on-a-high-risk-surface-still-owes-its-security-review-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[code-review-floor-is-medium-and-not-the-implementing-agent-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[condition-a-is-a-different-model-architecture-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[conditions-b-c-and-d-are-unchanged-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[diversity-within-tier-is-distance-on-request-not-a-default-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[plan-review-floor-is-medium-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[proposal-review-floor-is-high-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[security-review-floor-is-high-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[the-cleanup-row-is-the-only-exception-and-only-for-the-writing-step-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[the-cost-rule-check-is-not-a-review-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[the-data-governance-gate-applies-first-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[the-exclusion-list-is-unchanged-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[bright-line-keeps-the-high-risk-trust-boundaries-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[cleanup-keeps-the-reviews-stage-floor-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[cleanup-may-be-written-at-low-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[cleanup-on-a-high-risk-surface-still-owes-its-security-review-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[code-review-floor-is-medium-and-not-the-implementing-agent-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[condition-a-is-a-different-model-architecture-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[conditions-b-c-and-d-are-unchanged-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[diversity-within-tier-is-distance-on-request-not-a-default-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[plan-review-floor-is-medium-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[proposal-review-floor-is-high-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[security-review-floor-is-high-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[the-cleanup-row-is-the-only-exception-and-only-for-the-writing-step-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[the-cost-rule-check-is-not-a-review-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[the-data-governance-gate-applies-first-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[the-exclusion-list-is-unchanged-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[the-reviewer-surfaces-the-list-the-author-decides-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[the-reviewer-surfaces-the-list-the-author-decides-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[peer-review-gates-are-a-fresh-reviewer-at-every-stage-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[the-board-columns-are-named-by-what-they-are-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[the-board-columns-are-named-by-what-they-are-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[the-kernel-review-is-a-fresh-reviewer-who-did-not-write-the-work-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[the-module-adds-guidance-for-staffing-a-called-read-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[a-change-is-reviewed-by-an-independent-reviewer-beside-its-author-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[every-change-is-reviewed-by-a-fresh-reviewer-who-did-not-write-it-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_shipped_text_obligation_is_reported[the-maintainer-may-ask-for-more-distance-on-one-named-piece-of-work-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_omits_the_old_wording[shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_omits_the_old_wording[own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_omits_the_old_wording[shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_omits_the_old_wording[own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_omits_the_old_wording[shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_omits_the_old_wording[own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_omits_the_old_wording[legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_omits_the_old_wording[shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_omits_the_old_wording[own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_omits_the_old_wording[fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_omits_the_old_wording[modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_shipped_text_omits_the_old_wording[contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-constructive-internal-read-and-an-external-read-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-constructive-internal-read-and-an-external-read-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-constructive-internal-read-and-an-external-read-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-constructive-internal-read-and-an-external-read-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-constructive-internal-read-and-an-external-read-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-constructive-internal-read-and-an-external-read-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-constructive-internal-read-and-an-external-read-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-constructive-internal-read-and-an-external-read-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-constructive-internal-read-and-an-external-read-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-constructive-internal-read-and-an-external-read-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-constructive-internal-read-and-an-external-read-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-constructive-internal-read-and-an-external-read-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-pass-or-round-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-pass-or-round-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-pass-or-round-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-pass-or-round-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-pass-or-round-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-pass-or-round-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-pass-or-round-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-pass-or-round-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-pass-or-round-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-pass-or-round-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-pass-or-round-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-pass-or-round-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-than-the-author-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-than-the-author-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-than-the-author-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-than-the-author-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-than-the-author-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-than-the-author-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-than-the-author-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-than-the-author-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-than-the-author-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-than-the-author-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-than-the-author-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-agent-type-than-the-author-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-model-family-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-model-family-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-model-family-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-model-family-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-model-family-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-model-family-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-model-family-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-model-family-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-model-family-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-model-family-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-model-family-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-different-model-family-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-human-fills-a-tier-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-human-fills-a-tier-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-human-fills-a-tier-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-human-fills-a-tier-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-human-fills-a-tier-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-human-fills-a-tier-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-human-fills-a-tier-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-human-fills-a-tier-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-human-fills-a-tier-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-human-fills-a-tier-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-human-fills-a-tier-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-human-fills-a-tier-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-review-tier-column-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-review-tier-column-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-review-tier-column-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-review-tier-column-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-review-tier-column-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-review-tier-column-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-review-tier-column-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-review-tier-column-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-review-tier-column-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-review-tier-column-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-review-tier-column-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-review-tier-column-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-structurally-independent-tier-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-structurally-independent-tier-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-structurally-independent-tier-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-structurally-independent-tier-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-structurally-independent-tier-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-structurally-independent-tier-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-structurally-independent-tier-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-structurally-independent-tier-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-structurally-independent-tier-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-structurally-independent-tier-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-structurally-independent-tier-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-structurally-independent-tier-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-tool-is-credited-with-checking-the-quote-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-tool-is-credited-with-checking-the-quote-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-tool-is-credited-with-checking-the-quote-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-tool-is-credited-with-checking-the-quote-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-tool-is-credited-with-checking-the-quote-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-tool-is-credited-with-checking-the-quote-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-tool-is-credited-with-checking-the-quote-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-tool-is-credited-with-checking-the-quote-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-tool-is-credited-with-checking-the-quote-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-tool-is-credited-with-checking-the-quote-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-tool-is-credited-with-checking-the-quote-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[a-tool-is-credited-with-checking-the-quote-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[across-structural-independence-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[across-structural-independence-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[across-structural-independence-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[across-structural-independence-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[across-structural-independence-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[across-structural-independence-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[across-structural-independence-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[across-structural-independence-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[across-structural-independence-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[across-structural-independence-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[across-structural-independence-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[across-structural-independence-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[adversarial-premise-checking-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[adversarial-premise-checking-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[adversarial-premise-checking-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[adversarial-premise-checking-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[adversarial-premise-checking-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[adversarial-premise-checking-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[adversarial-premise-checking-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[adversarial-premise-checking-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[adversarial-premise-checking-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[adversarial-premise-checking-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[adversarial-premise-checking-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[adversarial-premise-checking-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[code-review-is-not-external-by-default-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[code-review-is-not-external-by-default-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[code-review-is-not-external-by-default-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[code-review-is-not-external-by-default-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[code-review-is-not-external-by-default-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[code-review-is-not-external-by-default-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[code-review-is-not-external-by-default-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[code-review-is-not-external-by-default-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[code-review-is-not-external-by-default-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[code-review-is-not-external-by-default-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[code-review-is-not-external-by-default-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[code-review-is-not-external-by-default-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[declared-external-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[declared-external-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[declared-external-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[declared-external-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[declared-external-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[declared-external-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[declared-external-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[declared-external-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[declared-external-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[declared-external-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[declared-external-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[declared-external-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[escalate-to-the-external-tier-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[escalate-to-the-external-tier-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[escalate-to-the-external-tier-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[escalate-to-the-external-tier-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[escalate-to-the-external-tier-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[escalate-to-the-external-tier-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[escalate-to-the-external-tier-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[escalate-to-the-external-tier-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[escalate-to-the-external-tier-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[escalate-to-the-external-tier-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[escalate-to-the-external-tier-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[escalate-to-the-external-tier-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-code-review-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-code-review-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-code-review-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-code-review-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-code-review-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-code-review-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-code-review-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-code-review-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-code-review-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-code-review-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-code-review-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-code-review-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-floor-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-floor-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-floor-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-floor-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-floor-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-floor-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-floor-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-floor-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-floor-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-floor-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-floor-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-floor-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-independence-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-independence-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-independence-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-independence-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-independence-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-independence-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-independence-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-independence-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-independence-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-independence-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-independence-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-independence-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-norms-heading-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-norms-heading-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-norms-heading-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-norms-heading-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-norms-heading-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-norms-heading-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-norms-heading-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-norms-heading-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-norms-heading-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-norms-heading-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-norms-heading-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-review-norms-heading-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-stance-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-stance-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-stance-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-stance-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-stance-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-stance-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-stance-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-stance-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-stance-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-stance-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-stance-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-stance-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-tier-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-tier-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-tier-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-tier-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-tier-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-tier-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-tier-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-tier-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-tier-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-tier-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-tier-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[external-tier-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-and-external-tiers-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-and-external-tiers-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-and-external-tiers-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-and-external-tiers-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-and-external-tiers-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-and-external-tiers-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-and-external-tiers-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-and-external-tiers-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-and-external-tiers-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-and-external-tiers-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-and-external-tiers-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-and-external-tiers-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-reviewer-role-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-reviewer-role-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-reviewer-role-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-reviewer-role-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-reviewer-role-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-reviewer-role-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-reviewer-role-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-reviewer-role-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-reviewer-role-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-reviewer-role-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-reviewer-role-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[internal-reviewer-role-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[required-external-in-a-header-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[required-external-in-a-header-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[required-external-in-a-header-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[required-external-in-a-header-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[required-external-in-a-header-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[required-external-in-a-header-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[required-external-in-a-header-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[required-external-in-a-header-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[required-external-in-a-header-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[required-external-in-a-header-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[required-external-in-a-header-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[required-external-in-a-header-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[reviewed-across-structural-independence-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[reviewed-across-structural-independence-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[reviewed-across-structural-independence-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[reviewed-across-structural-independence-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[reviewed-across-structural-independence-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[reviewed-across-structural-independence-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[reviewed-across-structural-independence-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[reviewed-across-structural-independence-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[reviewed-across-structural-independence-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[reviewed-across-structural-independence-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[reviewed-across-structural-independence-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[reviewed-across-structural-independence-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-checker-cannot-parse-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-checker-cannot-parse-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-checker-cannot-parse-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-checker-cannot-parse-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-checker-cannot-parse-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-checker-cannot-parse-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-checker-cannot-parse-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-checker-cannot-parse-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-checker-cannot-parse-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-checker-cannot-parse-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-checker-cannot-parse-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-checker-cannot-parse-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-diversity-within-tier-rule-applies-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-diversity-within-tier-rule-applies-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-diversity-within-tier-rule-applies-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-diversity-within-tier-rule-applies-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-diversity-within-tier-rule-applies-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-diversity-within-tier-rule-applies-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-diversity-within-tier-rule-applies-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-diversity-within-tier-rule-applies-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-diversity-within-tier-rule-applies-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-diversity-within-tier-rule-applies-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-diversity-within-tier-rule-applies-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-diversity-within-tier-rule-applies-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-reviewer-tiers-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-reviewer-tiers-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-reviewer-tiers-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-reviewer-tiers-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-reviewer-tiers-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-reviewer-tiers-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-reviewer-tiers-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-reviewer-tiers-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-reviewer-tiers-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-reviewer-tiers-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-reviewer-tiers-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[the-reviewer-tiers-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[tiers-are-stances-sentence-shipped-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[tiers-are-stances-sentence-own-agreement]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[tiers-are-stances-sentence-shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[tiers-are-stances-sentence-own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[tiers-are-stances-sentence-shipped-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[tiers-are-stances-sentence-own-security]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[tiers-are-stances-sentence-legacy-profile]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[tiers-are-stances-sentence-shipped-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[tiers-are-stances-sentence-own-skill]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[tiers-are-stances-sentence-fidelity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[tiers-are-stances-sentence-modules-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_shipped_text_is_reported[tiers-are-stances-sentence-contributing]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_model_selection_pair_is_byte_identical
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_session_start_twins_are_byte_identical
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_cleanup_row_never_says_usual[shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_cleanup_row_never_says_usual[own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_cleanup_row_sits_in_the_role_table[shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_cleanup_row_sits_in_the_role_table[own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_old_role_rows_are_gone[shipped-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_old_role_rows_are_gone[own-model]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_fidelity_sample_roster_agrees_with_the_loop_document
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_sample_roster_with_an_old_role_is_reported
bootstrap/tests/test_review_stance_in_shipped_files.py::test_doctrine_carries_the_statement[a-brief-may-state-the-stage-questions]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_doctrine_carries_the_statement[a-clean-pass-with-evidenced-answers-does-not-deserve-skepticism]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_doctrine_carries_the_statement[boundary-c-names-the-no-plan-accepted-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_doctrine_carries_the_statement[cleanup-may-be-written-at-low-and-no-review-is-lowered]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_doctrine_carries_the_statement[no-tool-reads-the-obligation-line]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_doctrine_carries_the_statement[one-standing-call-survives-and-it-is-the-maintainers]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_doctrine_carries_the_statement[the-cost-rule-check-is-not-a-review]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_doctrine_carries_the_statement[the-plan-obligation-is-cleared-only-by-a-matching-obligation-line]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_doctrine_carries_the_statement[the-stage-questions-are-in-the-doctrine]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_doctrine_carries_the_statement[the-sweep-and-the-trap-are-no-longer-team-gated]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_doctrine_statement_is_reported[a-brief-may-state-the-stage-questions]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_doctrine_statement_is_reported[a-clean-pass-with-evidenced-answers-does-not-deserve-skepticism]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_doctrine_statement_is_reported[boundary-c-names-the-no-plan-accepted-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_doctrine_statement_is_reported[cleanup-may-be-written-at-low-and-no-review-is-lowered]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_doctrine_statement_is_reported[no-tool-reads-the-obligation-line]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_doctrine_statement_is_reported[one-standing-call-survives-and-it-is-the-maintainers]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_doctrine_statement_is_reported[the-cost-rule-check-is-not-a-review]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_doctrine_statement_is_reported[the-plan-obligation-is-cleared-only-by-a-matching-obligation-line]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_doctrine_statement_is_reported[the-stage-questions-are-in-the-doctrine]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_doctrine_statement_is_reported[the-sweep-and-the-trap-are-no-longer-team-gated]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_doctrine_omits_the_retired_privilege[a-brief-narrows-the-pass]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_doctrine_omits_the_retired_privilege[a-confirming-second-different-agent-type-pass-clears-a-gate]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_doctrine_omits_the_retired_privilege[a-security-review-internal-record-satisfies-a-plan-obligation]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_doctrine_omits_the_retired_privilege[adversarial-premise-checking-in-the-bright-line-list]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_doctrine_omits_the_retired_privilege[an-external-pass-satisfies-a-required-internal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_doctrine_omits_the_retired_privilege[escalate-to-the-external-review-tier]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_doctrine_omits_the_retired_privilege[external-independence-lives-at-the-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_doctrine_omits_the_retired_privilege[recommended-wherever-it-can-be-staffed]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_doctrine_omits_the_retired_privilege[the-external-floor-lives-at-the-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_doctrine_omits_the_retired_privilege[tier-ordering-lets-external-satisfy-a-required-internal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_putting_a_retired_privilege_back_is_reported[a-brief-narrows-the-pass]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_putting_a_retired_privilege_back_is_reported[a-confirming-second-different-agent-type-pass-clears-a-gate]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_putting_a_retired_privilege_back_is_reported[a-security-review-internal-record-satisfies-a-plan-obligation]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_putting_a_retired_privilege_back_is_reported[adversarial-premise-checking-in-the-bright-line-list]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_putting_a_retired_privilege_back_is_reported[an-external-pass-satisfies-a-required-internal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_putting_a_retired_privilege_back_is_reported[escalate-to-the-external-review-tier]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_putting_a_retired_privilege_back_is_reported[external-independence-lives-at-the-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_putting_a_retired_privilege_back_is_reported[recommended-wherever-it-can-be-staffed]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_putting_a_retired_privilege_back_is_reported[the-external-floor-lives-at-the-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_putting_a_retired_privilege_back_is_reported[tier-ordering-lets-external-satisfy-a-required-internal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_anchor_equals_the_approved_wording
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_reworded_anchor_is_reported
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_two_trap_headings_are_adjacent_and_in_order
bootstrap/tests/test_review_stance_in_shipped_files.py::test_no_live_document_cites_a_heading_that_does_not_exist
bootstrap/tests/test_review_stance_in_shipped_files.py::test_no_live_document_credits_a_checker_that_does_not_exist
bootstrap/tests/test_review_stance_in_shipped_files.py::test_dimensions_omit_the_old_wording[complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_dimensions_omit_the_old_wording[dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_dimensions_omit_the_old_wording[agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_dimensions_omit_the_old_wording[human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[a-different-agent-type-pass-or-round-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[a-different-agent-type-pass-or-round-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[a-different-agent-type-pass-or-round-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[a-different-agent-type-pass-or-round-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[a-human-fills-a-tier-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[a-human-fills-a-tier-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[a-human-fills-a-tier-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[a-human-fills-a-tier-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[a-tier-the-agent-team-fills-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[a-tier-the-agent-team-fills-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[a-tier-the-agent-team-fills-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[a-tier-the-agent-team-fills-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[a-tier-wanting-structural-independence-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[a-tier-wanting-structural-independence-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[a-tier-wanting-structural-independence-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[a-tier-wanting-structural-independence-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[a-tool-is-credited-with-checking-the-quote-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[a-tool-is-credited-with-checking-the-quote-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[a-tool-is-credited-with-checking-the-quote-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[a-tool-is-credited-with-checking-the-quote-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[across-structural-independence-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[across-structural-independence-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[across-structural-independence-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[across-structural-independence-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[code-review-is-not-external-by-default-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[code-review-is-not-external-by-default-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[code-review-is-not-external-by-default-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[code-review-is-not-external-by-default-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[declared-external-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[declared-external-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[declared-external-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[declared-external-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[escalate-to-the-external-tier-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[escalate-to-the-external-tier-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[escalate-to-the-external-tier-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[escalate-to-the-external-tier-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-code-review-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-code-review-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-code-review-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-code-review-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-floor-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-floor-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-floor-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-floor-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-independence-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-independence-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-independence-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-independence-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-review-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-review-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-review-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-review-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-review-is-mandatory-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-review-is-mandatory-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-review-is-mandatory-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-review-is-mandatory-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-review-is-reserved-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-review-is-reserved-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-review-is-reserved-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-review-is-reserved-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-review-norms-heading-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-review-norms-heading-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-review-norms-heading-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-review-norms-heading-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-stance-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-stance-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-stance-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-stance-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-tier-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-tier-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-tier-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[external-tier-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[internal-reviewer-role-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[internal-reviewer-role-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[internal-reviewer-role-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[internal-reviewer-role-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[required-external-in-a-header-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[required-external-in-a-header-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[required-external-in-a-header-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[required-external-in-a-header-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[the-checker-cannot-parse-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[the-checker-cannot-parse-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[the-checker-cannot-parse-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[the-checker-cannot-parse-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[the-make-it-prove-itself-tier-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[the-make-it-prove-itself-tier-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[the-make-it-prove-itself-tier-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[the-make-it-prove-itself-tier-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[the-review-tiers-still-hold-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[the-review-tiers-still-hold-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[the-review-tiers-still-hold-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[the-review-tiers-still-hold-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[the-reviewer-tiers-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[the-reviewer-tiers-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[the-reviewer-tiers-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[the-reviewer-tiers-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[the-two-tier-apparatus-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[the-two-tier-apparatus-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[the-two-tier-apparatus-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[the-two-tier-apparatus-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[tiers-are-stances-sentence-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[tiers-are-stances-sentence-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[tiers-are-stances-sentence-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_dimensions_page_is_reported[tiers-are-stances-sentence-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_dimensions_page_carries_the_obligation[complex-has-the-one-review-with-the-scientific-trust-lens-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_dimensions_page_carries_the_obligation[complex-keeps-the-independent-scientific-check-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_dimensions_page_carries_the_obligation[complex-no-agent-adds-a-more-distant-read-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_dimensions_page_carries_the_obligation[complex-proposal-names-the-contracts-and-assumptions-it-touches-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_dimensions_page_carries_the_obligation[simple-has-the-one-review-with-a-thinner-evidence-plan-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_dimensions_page_carries_the_obligation[the-agent-team-cell-names-who-can-be-the-one-reviewer-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_dimensions_page_carries_the_obligation[the-complexity-cell-is-review-weight-and-verification-depth-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_dimensions_page_carries_the_obligation[the-team-gated-bullet-says-what-the-module-adds-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_dimensions_page_carries_the_obligation[a-single-agent-has-the-one-review-filled-by-time-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_dimensions_page_carries_the_obligation[more-distance-is-staffable-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_dimensions_page_carries_the_obligation[other-humans-are-available-to-be-the-one-reviewer-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_dimensions_obligation_is_reported[complex-has-the-one-review-with-the-scientific-trust-lens-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_dimensions_obligation_is_reported[complex-keeps-the-independent-scientific-check-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_dimensions_obligation_is_reported[complex-no-agent-adds-a-more-distant-read-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_dimensions_obligation_is_reported[complex-proposal-names-the-contracts-and-assumptions-it-touches-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_dimensions_obligation_is_reported[simple-has-the-one-review-with-a-thinner-evidence-plan-complexity]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_dimensions_obligation_is_reported[the-agent-team-cell-names-who-can-be-the-one-reviewer-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_dimensions_obligation_is_reported[the-complexity-cell-is-review-weight-and-verification-depth-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_dimensions_obligation_is_reported[the-team-gated-bullet-says-what-the-module-adds-dimensions-readme]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_dimensions_obligation_is_reported[a-single-agent-has-the-one-review-filled-by-time-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_dimensions_obligation_is_reported[more-distance-is-staffable-agent-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_dimensions_obligation_is_reported[other-humans-are-available-to-be-the-one-reviewer-human-team]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_complexity_cell_still_names_the_scientific_check
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_upgrade_guides_plan_pass_examples_are_not_external
bootstrap/tests/test_review_stance_in_shipped_files.py::test_putting_an_external_example_back_in_the_upgrade_guide_is_reported
bootstrap/tests/test_review_stance_in_shipped_files.py::test_readme_carries_the_accepted_wording[line-ten-says-a-fresh-session-by-default-and-more-on-request]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_readme_carries_the_accepted_wording[the-conflict-of-interest-row-says-the-record-names-the-reviewer]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_readme_carries_the_accepted_wording[the-distance-sentence-says-distance-is-easier-to-record]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_readme_carries_the_accepted_wording[the-figure-text-says-one-review-at-every-stage]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_readme_carries_the_accepted_wording[the-lead-in-sentence-before-the-distance-sentence-stays]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_readme_carries_the_accepted_wording[the-one-agent-paragraph-says-a-fresh-session-is-your-reviewer]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_readme_carries_the_accepted_wording[the-referee-row-says-a-reviewer-who-did-not-write-the-work]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_readme_carries_the_accepted_wording[the-sentence-after-the-distance-sentence-stays]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_readme_carries_the_accepted_wording[the-what-you-get-bullet-says-the-reviewer-is-not-the-author]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_reworded_readme_span_is_reported[line-ten-says-a-fresh-session-by-default-and-more-on-request]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_reworded_readme_span_is_reported[the-conflict-of-interest-row-says-the-record-names-the-reviewer]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_reworded_readme_span_is_reported[the-distance-sentence-says-distance-is-easier-to-record]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_reworded_readme_span_is_reported[the-figure-text-says-one-review-at-every-stage]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_reworded_readme_span_is_reported[the-lead-in-sentence-before-the-distance-sentence-stays]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_reworded_readme_span_is_reported[the-one-agent-paragraph-says-a-fresh-session-is-your-reviewer]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_reworded_readme_span_is_reported[the-referee-row-says-a-reviewer-who-did-not-write-the-work]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_reworded_readme_span_is_reported[the-sentence-after-the-distance-sentence-stays]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_reworded_readme_span_is_reported[the-what-you-get-bullet-says-the-reviewer-is-not-the-author]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_readme_alt_text_equals_the_figures_accessible_title
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_figure_parses_and_keeps_its_embed_geometry
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_figure_carries_no_old_phrase[two tiers]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_figure_carries_no_old_phrase[Internal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_figure_carries_no_old_phrase[External]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_figure_carries_no_old_phrase[different agent type or human]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_descriptive_page_omits_the_old_wording[readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_descriptive_page_omits_the_old_wording[docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_descriptive_page_omits_the_old_wording[docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_descriptive_page_omits_the_old_wording[docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_descriptive_page_omits_the_old_wording[dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_descriptive_page_omits_the_old_wording[docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_descriptive_page_omits_the_old_wording[docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_descriptive_page_omits_the_old_wording[docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_descriptive_page_omits_the_old_wording[docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_descriptive_page_omits_the_old_wording[dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_descriptive_page_omits_the_old_wording[docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_descriptive_page_omits_the_old_wording[on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_descriptive_page_omits_the_old_wording[docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_descriptive_page_omits_the_old_wording[templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_descriptive_page_omits_the_old_wording[docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-or-a-human-as-the-floor-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-or-a-human-as-the-floor-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-or-a-human-as-the-floor-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-or-a-human-as-the-floor-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-or-a-human-as-the-floor-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-or-a-human-as-the-floor-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-or-a-human-as-the-floor-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-or-a-human-as-the-floor-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-or-a-human-as-the-floor-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-or-a-human-as-the-floor-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-or-a-human-as-the-floor-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-or-a-human-as-the-floor-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-or-a-human-as-the-floor-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-or-a-human-as-the-floor-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-or-a-human-as-the-floor-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-pass-or-round-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-pass-or-round-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-pass-or-round-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-pass-or-round-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-pass-or-round-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-pass-or-round-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-pass-or-round-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-pass-or-round-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-pass-or-round-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-pass-or-round-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-pass-or-round-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-pass-or-round-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-pass-or-round-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-pass-or-round-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-different-agent-type-pass-or-round-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-floor-of-a-different-agent-type-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-floor-of-a-different-agent-type-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-floor-of-a-different-agent-type-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-floor-of-a-different-agent-type-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-floor-of-a-different-agent-type-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-floor-of-a-different-agent-type-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-floor-of-a-different-agent-type-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-floor-of-a-different-agent-type-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-floor-of-a-different-agent-type-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-floor-of-a-different-agent-type-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-floor-of-a-different-agent-type-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-floor-of-a-different-agent-type-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-floor-of-a-different-agent-type-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-floor-of-a-different-agent-type-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-floor-of-a-different-agent-type-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-human-fills-a-tier-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-human-fills-a-tier-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-human-fills-a-tier-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-human-fills-a-tier-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-human-fills-a-tier-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-human-fills-a-tier-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-human-fills-a-tier-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-human-fills-a-tier-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-human-fills-a-tier-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-human-fills-a-tier-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-human-fills-a-tier-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-human-fills-a-tier-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-human-fills-a-tier-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-human-fills-a-tier-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-human-fills-a-tier-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-review-tier-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-review-tier-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-review-tier-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-review-tier-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-review-tier-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-review-tier-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-review-tier-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-review-tier-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-review-tier-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-review-tier-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-review-tier-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-review-tier-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-review-tier-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-review-tier-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-review-tier-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-reviewer-structurally-independent-of-the-author-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-reviewer-structurally-independent-of-the-author-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-reviewer-structurally-independent-of-the-author-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-reviewer-structurally-independent-of-the-author-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-reviewer-structurally-independent-of-the-author-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-reviewer-structurally-independent-of-the-author-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-reviewer-structurally-independent-of-the-author-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-reviewer-structurally-independent-of-the-author-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-reviewer-structurally-independent-of-the-author-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-reviewer-structurally-independent-of-the-author-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-reviewer-structurally-independent-of-the-author-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-reviewer-structurally-independent-of-the-author-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-reviewer-structurally-independent-of-the-author-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-reviewer-structurally-independent-of-the-author-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-reviewer-structurally-independent-of-the-author-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-review-from-a-different-model-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-review-from-a-different-model-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-review-from-a-different-model-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-review-from-a-different-model-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-review-from-a-different-model-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-review-from-a-different-model-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-review-from-a-different-model-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-review-from-a-different-model-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-review-from-a-different-model-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-review-from-a-different-model-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-review-from-a-different-model-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-review-from-a-different-model-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-review-from-a-different-model-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-review-from-a-different-model-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-review-from-a-different-model-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-reviewer-who-must-be-a-different-agent-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-reviewer-who-must-be-a-different-agent-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-reviewer-who-must-be-a-different-agent-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-reviewer-who-must-be-a-different-agent-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-reviewer-who-must-be-a-different-agent-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-reviewer-who-must-be-a-different-agent-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-reviewer-who-must-be-a-different-agent-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-reviewer-who-must-be-a-different-agent-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-reviewer-who-must-be-a-different-agent-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-reviewer-who-must-be-a-different-agent-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-reviewer-who-must-be-a-different-agent-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-reviewer-who-must-be-a-different-agent-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-reviewer-who-must-be-a-different-agent-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-reviewer-who-must-be-a-different-agent-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-second-reviewer-who-must-be-a-different-agent-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-tool-is-credited-with-checking-the-quote-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-tool-is-credited-with-checking-the-quote-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-tool-is-credited-with-checking-the-quote-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-tool-is-credited-with-checking-the-quote-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-tool-is-credited-with-checking-the-quote-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-tool-is-credited-with-checking-the-quote-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-tool-is-credited-with-checking-the-quote-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-tool-is-credited-with-checking-the-quote-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-tool-is-credited-with-checking-the-quote-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-tool-is-credited-with-checking-the-quote-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-tool-is-credited-with-checking-the-quote-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-tool-is-credited-with-checking-the-quote-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-tool-is-credited-with-checking-the-quote-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-tool-is-credited-with-checking-the-quote-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[a-tool-is-credited-with-checking-the-quote-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[across-structural-independence-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[across-structural-independence-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[across-structural-independence-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[across-structural-independence-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[across-structural-independence-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[across-structural-independence-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[across-structural-independence-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[across-structural-independence-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[across-structural-independence-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[across-structural-independence-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[across-structural-independence-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[across-structural-independence-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[across-structural-independence-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[across-structural-independence-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[across-structural-independence-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[code-review-is-not-external-by-default-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[code-review-is-not-external-by-default-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[code-review-is-not-external-by-default-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[code-review-is-not-external-by-default-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[code-review-is-not-external-by-default-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[code-review-is-not-external-by-default-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[code-review-is-not-external-by-default-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[code-review-is-not-external-by-default-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[code-review-is-not-external-by-default-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[code-review-is-not-external-by-default-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[code-review-is-not-external-by-default-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[code-review-is-not-external-by-default-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[code-review-is-not-external-by-default-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[code-review-is-not-external-by-default-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[code-review-is-not-external-by-default-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[declared-external-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[declared-external-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[declared-external-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[declared-external-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[declared-external-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[declared-external-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[declared-external-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[declared-external-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[declared-external-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[declared-external-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[declared-external-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[declared-external-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[declared-external-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[declared-external-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[declared-external-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[escalate-to-the-external-tier-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[escalate-to-the-external-tier-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[escalate-to-the-external-tier-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[escalate-to-the-external-tier-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[escalate-to-the-external-tier-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[escalate-to-the-external-tier-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[escalate-to-the-external-tier-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[escalate-to-the-external-tier-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[escalate-to-the-external-tier-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[escalate-to-the-external-tier-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[escalate-to-the-external-tier-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[escalate-to-the-external-tier-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[escalate-to-the-external-tier-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[escalate-to-the-external-tier-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[escalate-to-the-external-tier-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-code-review-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-code-review-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-code-review-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-code-review-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-code-review-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-code-review-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-code-review-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-code-review-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-code-review-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-code-review-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-code-review-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-code-review-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-code-review-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-code-review-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-code-review-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-floor-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-floor-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-floor-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-floor-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-floor-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-floor-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-floor-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-floor-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-floor-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-floor-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-floor-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-floor-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-floor-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-floor-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-floor-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-independence-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-independence-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-independence-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-independence-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-independence-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-independence-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-independence-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-independence-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-independence-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-independence-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-independence-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-independence-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-independence-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-independence-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-independence-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-norms-heading-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-norms-heading-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-norms-heading-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-norms-heading-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-norms-heading-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-norms-heading-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-norms-heading-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-norms-heading-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-norms-heading-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-norms-heading-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-norms-heading-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-norms-heading-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-norms-heading-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-norms-heading-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-review-norms-heading-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-stance-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-stance-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-stance-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-stance-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-stance-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-stance-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-stance-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-stance-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-stance-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-stance-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-stance-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-stance-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-stance-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-stance-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-stance-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-tier-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-tier-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-tier-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-tier-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-tier-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-tier-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-tier-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-tier-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-tier-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-tier-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-tier-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-tier-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-tier-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-tier-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[external-tier-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[independence-you-can-check-by-model-type-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[independence-you-can-check-by-model-type-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[independence-you-can-check-by-model-type-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[independence-you-can-check-by-model-type-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[independence-you-can-check-by-model-type-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[independence-you-can-check-by-model-type-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[independence-you-can-check-by-model-type-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[independence-you-can-check-by-model-type-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[independence-you-can-check-by-model-type-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[independence-you-can-check-by-model-type-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[independence-you-can-check-by-model-type-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[independence-you-can-check-by-model-type-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[independence-you-can-check-by-model-type-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[independence-you-can-check-by-model-type-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[independence-you-can-check-by-model-type-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-review-as-a-kind-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-review-as-a-kind-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-review-as-a-kind-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-review-as-a-kind-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-review-as-a-kind-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-review-as-a-kind-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-review-as-a-kind-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-review-as-a-kind-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-review-as-a-kind-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-review-as-a-kind-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-review-as-a-kind-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-review-as-a-kind-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-review-as-a-kind-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-review-as-a-kind-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-review-as-a-kind-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-reviewer-role-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-reviewer-role-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-reviewer-role-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-reviewer-role-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-reviewer-role-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-reviewer-role-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-reviewer-role-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-reviewer-role-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-reviewer-role-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-reviewer-role-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-reviewer-role-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-reviewer-role-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-reviewer-role-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-reviewer-role-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[internal-reviewer-role-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[required-external-in-a-header-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[required-external-in-a-header-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[required-external-in-a-header-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[required-external-in-a-header-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[required-external-in-a-header-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[required-external-in-a-header-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[required-external-in-a-header-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[required-external-in-a-header-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[required-external-in-a-header-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[required-external-in-a-header-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[required-external-in-a-header-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[required-external-in-a-header-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[required-external-in-a-header-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[required-external-in-a-header-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[required-external-in-a-header-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[review-has-to-come-from-a-different-model-or-person-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[review-has-to-come-from-a-different-model-or-person-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[review-has-to-come-from-a-different-model-or-person-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[review-has-to-come-from-a-different-model-or-person-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[review-has-to-come-from-a-different-model-or-person-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[review-has-to-come-from-a-different-model-or-person-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[review-has-to-come-from-a-different-model-or-person-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[review-has-to-come-from-a-different-model-or-person-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[review-has-to-come-from-a-different-model-or-person-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[review-has-to-come-from-a-different-model-or-person-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[review-has-to-come-from-a-different-model-or-person-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[review-has-to-come-from-a-different-model-or-person-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[review-has-to-come-from-a-different-model-or-person-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[review-has-to-come-from-a-different-model-or-person-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[review-has-to-come-from-a-different-model-or-person-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-as-process-content-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-as-process-content-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-as-process-content-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-as-process-content-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-as-process-content-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-as-process-content-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-as-process-content-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-as-process-content-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-as-process-content-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-as-process-content-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-as-process-content-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-as-process-content-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-as-process-content-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-as-process-content-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-as-process-content-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-tiers-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-tiers-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-tiers-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-tiers-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-tiers-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-tiers-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-tiers-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-tiers-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-tiers-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-tiers-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-tiers-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-tiers-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-tiers-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-tiers-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[structural-independence-tiers-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-checker-cannot-parse-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-checker-cannot-parse-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-checker-cannot-parse-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-checker-cannot-parse-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-checker-cannot-parse-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-checker-cannot-parse-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-checker-cannot-parse-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-checker-cannot-parse-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-checker-cannot-parse-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-checker-cannot-parse-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-checker-cannot-parse-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-checker-cannot-parse-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-checker-cannot-parse-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-checker-cannot-parse-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-checker-cannot-parse-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-reviewer-tiers-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-reviewer-tiers-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-reviewer-tiers-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-reviewer-tiers-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-reviewer-tiers-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-reviewer-tiers-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-reviewer-tiers-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-reviewer-tiers-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-reviewer-tiers-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-reviewer-tiers-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-reviewer-tiers-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-reviewer-tiers-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-reviewer-tiers-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-reviewer-tiers-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-reviewer-tiers-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-second-tier-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-second-tier-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-second-tier-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-second-tier-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-second-tier-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-second-tier-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-second-tier-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-second-tier-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-second-tier-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-second-tier-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-second-tier-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-second-tier-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-second-tier-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-second-tier-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-second-tier-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-two-tier-description-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-two-tier-description-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-two-tier-description-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-two-tier-description-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-two-tier-description-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-two-tier-description-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-two-tier-description-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-two-tier-description-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-two-tier-description-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-two-tier-description-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-two-tier-description-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-two-tier-description-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-two-tier-description-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-two-tier-description-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[the-two-tier-description-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[tiers-are-stances-sentence-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[tiers-are-stances-sentence-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[tiers-are-stances-sentence-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[tiers-are-stances-sentence-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[tiers-are-stances-sentence-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[tiers-are-stances-sentence-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[tiers-are-stances-sentence-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[tiers-are-stances-sentence-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[tiers-are-stances-sentence-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[tiers-are-stances-sentence-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[tiers-are-stances-sentence-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[tiers-are-stances-sentence-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[tiers-are-stances-sentence-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[tiers-are-stances-sentence-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[tiers-are-stances-sentence-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[two-review-tiers-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[two-review-tiers-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[two-review-tiers-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[two-review-tiers-docs-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[two-review-tiers-dev-modules-onboarding-agent-team-onboarding-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[two-review-tiers-docs-quickstart-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[two-review-tiers-docs-workflow-role-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[two-review-tiers-docs-getting-started-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[two-review-tiers-docs-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[two-review-tiers-dev-modules-onboarding-dev-tour-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[two-review-tiers-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[two-review-tiers-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[two-review-tiers-docs-documentation-plan-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[two-review-tiers-templates-modules-default-on-documentation-plan-template-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_inserting_old_wording_into_a_descriptive_page_is_reported[two-review-tiers-docs-assets-dual-review-independence-svg]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_descriptive_page_carries_the_obligation[a-called-read-is-the-maintainers-call-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_descriptive_page_carries_the_obligation[dual-review-is-an-independent-reviewer-beside-the-author-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_descriptive_page_carries_the_obligation[review-is-one-stance-at-every-stage-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_descriptive_page_carries_the_obligation[structural-independence-is-recorded-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_descriptive_page_carries_the_obligation[the-vision-names-one-review-at-every-stage-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_descriptive_page_carries_the_obligation[the-board-names-the-review-lines-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_descriptive_page_carries_the_obligation[more-distance-is-added-on-request-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_descriptive_obligation_is_reported[a-called-read-is-the-maintainers-call-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_descriptive_obligation_is_reported[dual-review-is-an-independent-reviewer-beside-the-author-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_descriptive_obligation_is_reported[review-is-one-stance-at-every-stage-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_descriptive_obligation_is_reported[structural-independence-is-recorded-docs-glossary-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_descriptive_obligation_is_reported[the-vision-names-one-review-at-every-stage-docs-vision-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_descriptive_obligation_is_reported[the-board-names-the-review-lines-docs-tool-usage-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_a_descriptive_obligation_is_reported[more-distance-is-added-on-request-on-ramp-readme-md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_an_installed_onboarding_copy_equals_its_page[docs/agent-team-onboarding.md-dev/modules/onboarding/agent-team-onboarding.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_an_installed_onboarding_copy_equals_its_page[docs/dev-tour.md-dev/modules/onboarding/dev-tour.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_copy_that_drifts_from_its_page_is_reported
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_preset_glob_holds_every_shipped_preset
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_preset_names_no_review_tier_anyone_fills[templates-onboarding-collaborative-team.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_preset_names_no_review_tier_anyone_fills[templates-onboarding-high-rigor-legacy.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_preset_names_no_review_tier_anyone_fills[templates-onboarding-solo-greenfield.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_preset_names_no_review_tier_anyone_fills[dev-modules-onboarding-agent-team-onboarding.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_preset_names_no_review_tier_anyone_fills[dev-modules-onboarding-collaborative-team.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_preset_names_no_review_tier_anyone_fills[dev-modules-onboarding-dev-tour.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_each_retired_literal_matches_its_historic_sentence[a-fresh-session-external-review-tier]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_each_retired_literal_matches_its_historic_sentence[an-external-tier-currently-filled-by-a-fresh-session]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_putting_a_retired_sentence_back_in_a_preset_is_reported[a-fresh-session-external-review-tier-solo-greenfield.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_putting_a_retired_sentence_back_in_a_preset_is_reported[a-fresh-session-external-review-tier-collaborative-team.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_putting_a_retired_sentence_back_in_a_preset_is_reported[a-fresh-session-external-review-tier-high-rigor-legacy.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_putting_a_retired_sentence_back_in_a_preset_is_reported[an-external-tier-currently-filled-by-a-fresh-session-solo-greenfield.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_putting_a_retired_sentence_back_in_a_preset_is_reported[an-external-tier-currently-filled-by-a-fresh-session-collaborative-team.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_putting_a_retired_sentence_back_in_a_preset_is_reported[an-external-tier-currently-filled-by-a-fresh-session-high-rigor-legacy.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_correctly_worded_sentence_is_not_flagged
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_mergeable_template_has_no_one_word_placeholder_the_engine_cannot_fill[templates-core-AGENTS.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_mergeable_template_has_no_one_word_placeholder_the_engine_cannot_fill[templates-core-NOTICE.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_mergeable_template_has_no_one_word_placeholder_the_engine_cannot_fill[templates-core-VENDOR.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_mergeable_template_has_no_one_word_placeholder_the_engine_cannot_fill[templates-core-dev-NEXT_SESSION.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_mergeable_template_has_no_one_word_placeholder_the_engine_cannot_fill[templates-core-dev-PLANNING.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_mergeable_template_has_no_one_word_placeholder_the_engine_cannot_fill[templates-core-dev-README.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_mergeable_template_has_no_one_word_placeholder_the_engine_cannot_fill[templates-core-dev-agent_collaboration.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_mergeable_template_has_no_one_word_placeholder_the_engine_cannot_fill[templates-core-dev-collaboration_agreement.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_mergeable_template_has_no_one_word_placeholder_the_engine_cannot_fill[templates-core-dev-measurement-README.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_mergeable_template_has_no_one_word_placeholder_the_engine_cannot_fill[templates-core-dev-plans-_template.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_mergeable_template_has_no_one_word_placeholder_the_engine_cannot_fill[templates-core-dev-proposals-_template.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_mergeable_template_has_no_one_word_placeholder_the_engine_cannot_fill[templates-core-dev-rules-README.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_mergeable_template_has_no_one_word_placeholder_the_engine_cannot_fill[templates-core-dev-strategy-README.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_mergeable_template_has_no_one_word_placeholder_the_engine_cannot_fill[templates-core-dev-strategy-_template.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_mergeable_template_has_no_one_word_placeholder_the_engine_cannot_fill[templates-core-dev-upstream-README.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_mergeable_template_has_no_one_word_placeholder_the_engine_cannot_fill[templates-core-dev-upstream-_template.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_mergeable_template_has_no_one_word_placeholder_the_engine_cannot_fill[dev-proposals-_template.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_mergeable_template_has_no_one_word_placeholder_the_engine_cannot_fill[dev-plans-_template.md]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_mergeable_template_list_covers_the_authoring_templates
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_one_word_placeholder_in_an_authoring_template_is_reported[shipped-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_one_word_placeholder_in_an_authoring_template_is_reported[own-proposal]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_one_word_placeholder_in_an_authoring_template_is_reported[shipped-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_one_word_placeholder_in_an_authoring_template_is_reported[own-plan]
bootstrap/tests/test_review_stance_in_shipped_files.py::test_every_file_with_a_phrasing_hit_is_exempt_for_a_reason
bootstrap/tests/test_review_stance_in_shipped_files.py::test_no_exemption_is_stale
bootstrap/tests/test_review_stance_in_shipped_files.py::test_no_file_an_adopter_receives_is_exempt
bootstrap/tests/test_review_stance_in_shipped_files.py::test_removing_an_exemption_is_reported
bootstrap/tests/test_review_stance_in_shipped_files.py::test_a_phrase_inserted_into_a_scanned_copy_is_reported
bootstrap/tests/test_review_stance_in_shipped_files.py::test_exempting_an_installed_file_is_reported
bootstrap/tests/test_review_stance_in_shipped_files.py::test_the_walk_reaches_the_roots_it_claims
```

`bootstrap/tests/test_review_sweep_ships.py`: 192 nodes.

```
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[a-bare-checked-is-an-incomplete-review-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[a-bare-checked-is-an-incomplete-review-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[a-clean-code-review-shows-a-falsification-ledger-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[a-clean-code-review-shows-a-falsification-ledger-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[a-clean-pass-is-treated-with-skepticism-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[a-clean-pass-is-treated-with-skepticism-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[a-lens-is-where-the-evidence-for-the-three-answers-comes-from-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[a-lens-is-where-the-evidence-for-the-three-answers-comes-from-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[a-lens-names-the-file-test-line-or-command-that-backs-it-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[a-lens-names-the-file-test-line-or-command-that-backs-it-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[a-project-adds-its-own-probes-after-the-nine-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[a-project-adds-its-own-probes-after-the-nine-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[a-reviewer-who-tried-to-break-it-has-cleared-the-gate-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[a-reviewer-who-tried-to-break-it-has-cleared-the-gate-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[coverage-line-covered-half-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[coverage-line-covered-half-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[coverage-line-does-not-end-in-a-recommendation-for-more-review-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[coverage-line-does-not-end-in-a-recommendation-for-more-review-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[coverage-line-not-covered-half-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[coverage-line-not-covered-half-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[ledger-mutation-is-reported-against-an-unmutated-control-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[ledger-mutation-is-reported-against-an-unmutated-control-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[ledger-mutation-when-a-claim-names-a-set-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[ledger-mutation-when-a-claim-names-a-set-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[ledger-negative-or-edge-case-attempt-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[ledger-negative-or-edge-case-attempt-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[ledger-residual-risk-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[ledger-residual-risk-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[ledger-surfaces-probed-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[ledger-surfaces-probed-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[ledger-verification-run-or-consciously-not-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[ledger-verification-run-or-consciously-not-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[lens-1-claims-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[lens-1-claims-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[lens-2-production-path-exercised-by-tests-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[lens-2-production-path-exercised-by-tests-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[lens-3-design-completeness-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[lens-3-design-completeness-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[lens-4-silent-failure-fail-closed-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[lens-4-silent-failure-fail-closed-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[lens-5-cross-document-consistency-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[lens-5-cross-document-consistency-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[lens-6-drift-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[lens-6-drift-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[lens-7-lifecycle-process-placement-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[lens-7-lifecycle-process-placement-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[lens-8-domain-scientific-validity-and-scope-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[lens-8-domain-scientific-validity-and-scope-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[lens-9-name-the-satisfier-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[lens-9-name-the-satisfier-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[the-sweep-applies-to-the-reviews-the-lifecycle-calls-for-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[the-sweep-applies-to-the-reviews-the-lifecycle-calls-for-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[the-sweep-is-a-floor-never-a-downgrade-of-a-declared-tier-shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_source_sweep_carries_the_obligation[the-sweep-is-a-floor-never-a-downgrade-of-a-declared-tier-own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_the_sweep_precedes_the_scope_reduction_trap[shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_the_sweep_precedes_the_scope_reduction_trap[own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_the_lens_roster_is_exactly_nine_in_the_doctrines_order[shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_the_lens_roster_is_exactly_nine_in_the_doctrines_order[own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_the_anchors_a_follower_writes_against_are_present[shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_the_anchors_a_follower_writes_against_are_present[own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_the_ledger_is_defined_once_with_five_items[shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_the_ledger_is_defined_once_with_five_items[own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_the_sweep_leaves_the_doctrines_reasoning_out[shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_the_sweep_leaves_the_doctrines_reasoning_out[own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_the_leak_pattern_matches_the_doctrine_it_guards_against
bootstrap/tests/test_review_sweep_ships.py::test_the_sweep_is_body_text_not_a_slot[shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_the_sweep_is_body_text_not_a_slot[own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_agents_md_pointer_carries_the_obligation[pointer-names-the-sweep-in-the-loop-document-shipped-agents]
bootstrap/tests/test_review_sweep_ships.py::test_agents_md_pointer_carries_the_obligation[pointer-names-the-sweep-in-the-loop-document-own-agents]
bootstrap/tests/test_review_sweep_ships.py::test_agents_md_pointer_carries_the_obligation[pointer-says-a-bare-checked-is-an-incomplete-review-shipped-agents]
bootstrap/tests/test_review_sweep_ships.py::test_agents_md_pointer_carries_the_obligation[pointer-says-a-bare-checked-is-an-incomplete-review-own-agents]
bootstrap/tests/test_review_sweep_ships.py::test_agents_md_pointer_carries_the_obligation[pointer-says-the-answers-rest-on-nine-standing-lenses-shipped-agents]
bootstrap/tests/test_review_sweep_ships.py::test_agents_md_pointer_carries_the_obligation[pointer-says-the-answers-rest-on-nine-standing-lenses-own-agents]
bootstrap/tests/test_review_sweep_ships.py::test_agents_md_pointer_carries_the_obligation[pointer-says-the-coverage-line-names-what-was-not-covered-shipped-agents]
bootstrap/tests/test_review_sweep_ships.py::test_agents_md_pointer_carries_the_obligation[pointer-says-the-coverage-line-names-what-was-not-covered-own-agents]
bootstrap/tests/test_review_sweep_ships.py::test_the_pointer_names_no_test_path[shipped-agents]
bootstrap/tests/test_review_sweep_ships.py::test_the_pointer_names_no_test_path[own-agents]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[a-bare-checked-is-an-incomplete-review-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[a-bare-checked-is-an-incomplete-review-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[a-bare-checked-is-an-incomplete-review-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[a-clean-code-review-shows-a-falsification-ledger-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[a-clean-code-review-shows-a-falsification-ledger-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[a-clean-code-review-shows-a-falsification-ledger-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[a-clean-pass-is-treated-with-skepticism-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[a-clean-pass-is-treated-with-skepticism-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[a-clean-pass-is-treated-with-skepticism-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[a-lens-is-where-the-evidence-for-the-three-answers-comes-from-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[a-lens-is-where-the-evidence-for-the-three-answers-comes-from-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[a-lens-is-where-the-evidence-for-the-three-answers-comes-from-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[a-lens-names-the-file-test-line-or-command-that-backs-it-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[a-lens-names-the-file-test-line-or-command-that-backs-it-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[a-lens-names-the-file-test-line-or-command-that-backs-it-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[a-project-adds-its-own-probes-after-the-nine-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[a-project-adds-its-own-probes-after-the-nine-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[a-project-adds-its-own-probes-after-the-nine-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[a-reviewer-who-tried-to-break-it-has-cleared-the-gate-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[a-reviewer-who-tried-to-break-it-has-cleared-the-gate-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[a-reviewer-who-tried-to-break-it-has-cleared-the-gate-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[coverage-line-covered-half-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[coverage-line-covered-half-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[coverage-line-covered-half-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[coverage-line-does-not-end-in-a-recommendation-for-more-review-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[coverage-line-does-not-end-in-a-recommendation-for-more-review-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[coverage-line-does-not-end-in-a-recommendation-for-more-review-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[coverage-line-not-covered-half-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[coverage-line-not-covered-half-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[coverage-line-not-covered-half-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[ledger-mutation-is-reported-against-an-unmutated-control-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[ledger-mutation-is-reported-against-an-unmutated-control-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[ledger-mutation-is-reported-against-an-unmutated-control-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[ledger-mutation-when-a-claim-names-a-set-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[ledger-mutation-when-a-claim-names-a-set-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[ledger-mutation-when-a-claim-names-a-set-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[ledger-negative-or-edge-case-attempt-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[ledger-negative-or-edge-case-attempt-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[ledger-negative-or-edge-case-attempt-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[ledger-residual-risk-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[ledger-residual-risk-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[ledger-residual-risk-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[ledger-surfaces-probed-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[ledger-surfaces-probed-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[ledger-surfaces-probed-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[ledger-verification-run-or-consciously-not-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[ledger-verification-run-or-consciously-not-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[ledger-verification-run-or-consciously-not-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-1-claims-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-1-claims-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-1-claims-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-2-production-path-exercised-by-tests-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-2-production-path-exercised-by-tests-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-2-production-path-exercised-by-tests-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-3-design-completeness-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-3-design-completeness-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-3-design-completeness-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-4-silent-failure-fail-closed-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-4-silent-failure-fail-closed-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-4-silent-failure-fail-closed-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-5-cross-document-consistency-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-5-cross-document-consistency-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-5-cross-document-consistency-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-6-drift-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-6-drift-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-6-drift-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-7-lifecycle-process-placement-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-7-lifecycle-process-placement-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-7-lifecycle-process-placement-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-8-domain-scientific-validity-and-scope-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-8-domain-scientific-validity-and-scope-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-8-domain-scientific-validity-and-scope-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-9-name-the-satisfier-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-9-name-the-satisfier-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[lens-9-name-the-satisfier-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[the-sweep-applies-to-the-reviews-the-lifecycle-calls-for-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[the-sweep-applies-to-the-reviews-the-lifecycle-calls-for-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[the-sweep-applies-to-the-reviews-the-lifecycle-calls-for-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[the-sweep-is-a-floor-never-a-downgrade-of-a-declared-tier-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[the-sweep-is-a-floor-never-a-downgrade-of-a-declared-tier-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_loop_document_carries_the_obligation[the-sweep-is-a-floor-never-a-downgrade-of-a-declared-tier-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_agents_md_carries_the_pointer[pointer-names-the-sweep-in-the-loop-document-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_agents_md_carries_the_pointer[pointer-names-the-sweep-in-the-loop-document-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_agents_md_carries_the_pointer[pointer-names-the-sweep-in-the-loop-document-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_agents_md_carries_the_pointer[pointer-says-a-bare-checked-is-an-incomplete-review-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_agents_md_carries_the_pointer[pointer-says-a-bare-checked-is-an-incomplete-review-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_agents_md_carries_the_pointer[pointer-says-a-bare-checked-is-an-incomplete-review-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_agents_md_carries_the_pointer[pointer-says-the-answers-rest-on-nine-standing-lenses-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_agents_md_carries_the_pointer[pointer-says-the-answers-rest-on-nine-standing-lenses-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_agents_md_carries_the_pointer[pointer-says-the-answers-rest-on-nine-standing-lenses-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_installed_agents_md_carries_the_pointer[pointer-says-the-coverage-line-names-what-was-not-covered-collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_installed_agents_md_carries_the_pointer[pointer-says-the-coverage-line-names-what-was-not-covered-high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_installed_agents_md_carries_the_pointer[pointer-says-the-coverage-line-names-what-was-not-covered-solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_an_install_without_the_sweep_is_reported[collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_an_install_without_the_sweep_is_reported[high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_an_install_without_the_sweep_is_reported[solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_deleting_lens_4_is_reported[shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_deleting_lens_4_is_reported[own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_deleting_the_not_covered_half_is_reported[shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_deleting_the_not_covered_half_is_reported[own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_deleting_the_scope_sentence_is_reported[shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_deleting_the_scope_sentence_is_reported[own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_adding_a_sixth_ledger_item_is_reported[shipped-loop]
bootstrap/tests/test_review_sweep_ships.py::test_adding_a_sixth_ledger_item_is_reported[own-loop]
bootstrap/tests/test_review_sweep_ships.py::test_an_install_leaves_no_placeholder_the_engine_cannot_fill[collaborative-team]
bootstrap/tests/test_review_sweep_ships.py::test_an_install_leaves_no_placeholder_the_engine_cannot_fill[high-rigor-legacy]
bootstrap/tests/test_review_sweep_ships.py::test_an_install_leaves_no_placeholder_the_engine_cannot_fill[solo-greenfield]
bootstrap/tests/test_review_sweep_ships.py::test_the_module_carries_no_lens_citation_rule_or_ledger[shipped-module]
bootstrap/tests/test_review_sweep_ships.py::test_the_module_carries_no_lens_citation_rule_or_ledger[own-module]
bootstrap/tests/test_review_sweep_ships.py::test_restoring_the_roster_into_the_module_is_reported[shipped-module]
bootstrap/tests/test_review_sweep_ships.py::test_restoring_the_roster_into_the_module_is_reported[own-module]
bootstrap/tests/test_review_sweep_ships.py::test_restoring_the_citation_rule_into_the_module_is_reported[shipped-module]
bootstrap/tests/test_review_sweep_ships.py::test_restoring_the_citation_rule_into_the_module_is_reported[own-module]
bootstrap/tests/test_review_sweep_ships.py::test_restoring_the_ledger_into_the_module_is_reported[shipped-module]
bootstrap/tests/test_review_sweep_ships.py::test_restoring_the_ledger_into_the_module_is_reported[own-module]
```

### Signals the plan defines (not failures; the code reviewer weighs them)

* `AGENTS.md` grew by **49 lines per copy** (shipped 419 to 468, Cairn's 443 to 492) against the 40-line
  ceiling. The quoted called-read text alone is 28 lines; the stage questions, the Foundations
  paragraph, the evidence pointer and the two security sentences account for the rest.
* The loop document grew from 152 to 242 lines (Cairn's 134 to 224); the sweep is 89 lines (the plan: 85 to 95).
* The dual-review module is **59 lines** in both copies (from 152 and 151; the plan said about 84).
* `check_module_body_coverage.py` reads **11 missing topics against 8 at the base**: it matches doctrine heading
  text, and three headings the module used to repeat (Structural independence, Code review, the clean-pass trap)
  now live in the review-loop document under other names. It was 8 at C4.
* Three expected line-bound flags in the archived source proposals (the Maintainer's allowance above): confirmed.

### Known omissions

No full-suite run is offered as certification; the certifying run is pending (**Certified by**: pending). The
scoped run was made at the tested commit only; it was not repeated after the prose commits that follow it
(`f3abb787`'s additions-only claim markers, and this record), which change no test, template or fixture byte.
The mutation ledger ran the two new test files (2042 nodes) per mutant; its driver set the broad-run variable
although scoped files do not need it, before the instruction, and it is not repeated.
**After the tested commit, another session changed files this plan lists** (`dffc13d1`, on the Maintainer's own
README instruction, recorded in the *Scope delta -- README presentation* section it appended): `README.md`
and the README group of `test_review_stance_in_shipped_files.py`. The node IDs, node count and blob id of that
test at the code-reviewed commit therefore differ from the tested-commit values recorded here; the values
here are correct for `fd66c988`, and the archive note records them again at the code-reviewed commit.
I did not mutate the code reviewer's set claims member by member (Boundary C). The adopter rehearsal used the
committed trees of both repositories, not their working trees, and ran no `--apply`. Plan D and plan C's
own `revising-code` commits that land after the tested commit are not in the tested tree.

## Search classification -- end state -- Claude Sonnet 5.5 (implementer) -- 2026-10-19

The end state of the classification above, built the same way (the script stops on any file with a hit and
no entry, and on any entry with no hit) over a clean worktree of the tested commit `fd66c988`. Searches A, B,
D and the authority probe, with the instrument and calibration unchanged. **Search A: 2 files, 2 hits, both
exempt in the stance test for a stated reason; no hit selects a more distant reviewer.** A hit marked *kept*
is the Maintainer-called definition, a staffing fact, a credit comment, a history reference, noise, the
standing launcher-review call, the cost-rule carve-out, or a ruled plan-review token; the *Disposition* says
which and why.

**Search A, the phrasing** -- 2 files, 2 hits.

| File | Hits | Category | Disposition |
|---|---|---|---|
| `doctrine/lifecycle-contract.md` | 1 | marked history reference | kept: the sentence is introduced by 'History:'; exempt in the stance test with that reason |
| `doctrine/onboarding.md` | 1 | credit comment | kept: it credits an earlier review's disposition by name; exempt in the stance test with that reason |

**Search B, the act of selecting** -- 26 files, 41 hits.

| File | Hits | Category | Disposition |
|---|---|---|---|
| `AGENTS.md` | 2 | Maintainer-called definition / staffing fact | kept: the called-read paragraph; 'a human' in 'Why this is stated positively' is the commit fence |
| `bootstrap/UPGRADE.md` | 1 | stale planner text (retired planner; untouched) | kept: the paragraph describes the retired planner's tier parse |
| `dev/agent_collaboration.md` | 1 | staffing fact | kept: 'no review requires a different agent type' |
| `dev/modules/claim-check.md` | 1 | noise | kept: 'external' means outside the repo or the checker; 'a different agent' means the next session |
| `dev/modules/model-selection.md` | 2 | cost-rule carve-out | kept: the cost rule's check, which is not a review (the carve-out paragraph and its condition) |
| `dev/plans/_template.md` | 1 | Maintainer-called definition | kept: the called-read paragraph (one rule, four copies) |
| `dev/proposals/_template.md` | 1 | Maintainer-called definition | kept: the called-read paragraph (one rule, four copies) |
| `dimensions/agent-team.md` | 1 | staffing fact | kept: who is available for which role |
| `docs/assets/dual-review-independence.svg` | 1 | Maintainer-called definition | kept: the figure's comment says a different model or a person adds distance only when the maintainer asks |
| `docs/workflow-role.md` | 1 | Maintainer-called definition | kept: 'how far from the author the Maintainer wants them' |
| `doctrine/doc-governance.md` | 1 | noise | kept: 'external' means outside the repo or the checker; 'a different agent' means the next session |
| `doctrine/dual-review.md` | 5 | Maintainer-called definition / standing launcher-review call / staffing fact | kept: per-artifact call, the surviving launcher-review call, 'no review requires a different agent type', 'a fresh session is the floor' |
| `doctrine/lifecycle.md` | 2 | noise | kept: 'external' means outside the repo or the checker; 'a different agent' means the next session |
| `doctrine/plans.md` | 4 | staffing fact / stale planner text (retired planner; untouched) | kept: denials of a mandated different-agent-type read; the 'Normalizing' paragraph is retired-planner text |
| `doctrine/proposals.md` | 1 | ruled plan-review token | kept: the ruled Plan review tokens |
| `doctrine/roles.md` | 3 | Maintainer-called definition / cost-rule carve-out | kept: distance on request; the cost rule's check is not a review |
| `doctrine/runtime-contract.md` | 2 | noise | kept: 'external' means outside the repo or the checker; 'a different agent' means the next session |
| `doctrine/session-routines.md` | 1 | noise | kept: 'external' means outside the repo or the checker; 'a different agent' means the next session |
| `on-ramp/README.md` | 1 | Maintainer-called definition | kept: more distance 'whenever you ask for it; it is never required' |
| `templates/core/AGENTS.md` | 2 | Maintainer-called definition / staffing fact | kept: the called-read paragraph; 'a human' in 'Why this is stated positively' is the commit fence |
| `templates/core/dev/agent_collaboration.md` | 1 | staffing fact | kept: 'no review requires a different agent type' |
| `templates/core/dev/plans/_template.md` | 1 | Maintainer-called definition | kept: the called-read paragraph (one rule, four copies) |
| `templates/core/dev/proposals/_template.md` | 1 | Maintainer-called definition | kept: the called-read paragraph (one rule, four copies) |
| `templates/core/dev/upstream/README.md` | 1 | noise | kept: 'external' means outside the repo or the checker; 'a different agent' means the next session |
| `templates/modules/default-on/claim-check.md` | 1 | noise | kept: 'external' means outside the repo or the checker; 'a different agent' means the next session |
| `templates/modules/team-gated/model-selection.md` | 2 | cost-rule carve-out | kept: the cost rule's check, which is not a review (the carve-out paragraph and its condition) |

**Search D, the old description** -- 11 files, 16 hits.

| File | Hits | Category | Disposition |
|---|---|---|---|
| `AGENTS.md` | 2 | ruled plan-review token / staffing fact | kept: the 'usual + Security Review' and 'Internal Security Review' tokens; 'a structurally-independent read is only independent if its author is its committer' |
| `bootstrap/UPGRADE.md` | 1 | stale planner text (retired planner; untouched) | kept: 'What the gate does not do' describes the retired planner |
| `dev/agent_collaboration.md` | 1 | staffing fact | kept: the same attribution sentence |
| `dev/plans/_template.md` | 1 | ruled plan-review token | kept: the plan-security obligation sentence |
| `docs/glossary.md` | 1 | term kept, redefined | kept: 'Structural independence' is defined as recorded, not required |
| `doctrine/dual-review.md` | 3 | ruled plan-review token / history | kept: the heading 'Structural independence' (now says independence is recorded), the ruled tokens, the retired lifecycle planner |
| `doctrine/onboarding.md` | 1 | noise | kept: a docs page cited by name |
| `doctrine/plans.md` | 2 | ruled plan-review token / noise | kept: 'Assurance path does not change the plan review'; Boundary B reuse text |
| `templates/core/AGENTS.md` | 2 | ruled plan-review token / staffing fact | kept: the 'usual + Security Review' and 'Internal Security Review' tokens; 'a structurally-independent read is only independent if its author is its committer' |
| `templates/core/dev/agent_collaboration.md` | 1 | staffing fact | kept: the same attribution sentence |
| `templates/core/dev/plans/_template.md` | 1 | ruled plan-review token | kept: the plan-security obligation sentence |

**authority probe** -- 8 files, 10 hits.

| File | Hits | Category | Disposition |
|---|---|---|---|
| `bootstrap/REANCHOR_RUNBOOK.md` | 2 | standing launcher-review call / noise | kept, byte-identical to the base (the runbook is a ceremony document) |
| `dev/modules/claim-check.md` | 1 | noise | kept: 'clear' is about flags or markers, 'external' is about scope |
| `dev/modules/doc-drift-prevention.md` | 1 | noise | kept: 'clear' is about flags or markers, 'external' is about scope |
| `doctrine/dual-review.md` | 2 | Maintainer-called definition / staffing fact | kept: neither privilege remains; the code-review floor is cleared by a same-type fresh session |
| `doctrine/lifecycle.md` | 1 | noise | kept: 'clear' is about flags or markers, 'external' is about scope |
| `templates/codebase-readiness-report.md` | 1 | noise | kept: 'clear' is about flags or markers, 'external' is about scope |
| `templates/modules/default-on/claim-check.md` | 1 | noise | kept: 'clear' is about flags or markers, 'external' is about scope |
| `templates/modules/team-gated/doc-drift-prevention.md` | 1 | noise | kept: 'clear' is about flags or markers, 'external' is about scope |


**Search C, `README.md` end state.** The six places equal the accepted wording (the stance test pins each);
the remaining `independen` hits (the problem statement, "someone independent checks", an
independent adoption, an independent correctness probe) are generic uses and stay.

## Scope delta -- README presentation -- Maintainer instruction, 2026-10-19

The Maintainer requested a new README presentation in chat, verbatim:

> Can you re-work the Cairn README page, it's focus on an external, independently-structured AI agent/human is too strong. It also could use some de-AI-ification.

This replaces the README-only exact-copy and figure-placement requirements in
Q3/C6. The front page may remove the repeated reviewer-distance pitch, journal
analogy and review figure, and lead with research-software work, recorded
decisions and session continuity. The framework anchor, review rules and other
C6 surfaces are unchanged. No scientific or review outcome is removed.

The README tests now check the retained contract: a fresh non-author reviewer,
same-tool fresh-session sufficiency, the Maintainer's choice of additional
distance, and recorded review authorship/evidence. Deletion controls must fail;
equivalent wording must pass. They no longer pin repeated marketing sentences
or require this figure on this page. The figure itself remains accessible and
tested, without changing its bytes.

This is a presentation follow-up, not a completed integration run or code-review
clearance. C8 and the queued gate-manifest re-anchor still apply, including the
changed test file and test-node set. The plan's status is not advanced here.

The plan's claim checker still reports the historical range quoted under
"Left open by this plan" above. That paragraph already says the range was
removed; it is not a claim that the current file has those lines. This follow-up
does not edit the quotation, suppress the check, or resolve the source proposal's
separately recorded citation debt.

The README test changes invalidate reuse of the earlier full-run record for
the updated tree. A fresh full integration run for this follow-up is owed before
its verification is complete; the scoped checks alone do not clear C8.

### README follow-up verification disposition -- 2026-10-19

The Maintainer superseded the preceding full-rerun requirement for this README
follow-up in chat:

> We just don't need a complete verification of this sort

The full run was stopped at the Maintainer's request and is not passing
integration evidence. The 1,844 passing focused tests and document checks are
sufficient for this follow-up; no full rerun is outstanding for it. This does
not change the rest of the plan's verification or re-anchor obligations.
