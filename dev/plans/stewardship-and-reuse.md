# Plan: Fix easy defects and reuse what already exists

**Source proposal**: `dev/proposals/archive/2026-10-18-claude-stewardship-and-reuse.md`
**Status**: ready-to-implement
**Plan review**: required(Internal)
**Assurance path**: high-assurance
**Opened**: 2026-10-19
**In brief**: Agents will fix small defects that break an existing promise, explain why work must wait, and look for reusable code before adding more.

## Source proposal

Revision 1 of the source proposal binds **as narrowed by its Decision**. The
Maintainer accepted promise-only defect fixes with no date cutoff, made the
per-plan total a warning sign, declined a mandatory Known-defects cell, and
requested one small ship test. Cheap counts steps needing a person rather
than test runtime. The reuse rule is one sentence in each `AGENTS.md` copy.
The rate-limit gate is **waived, not met**; the defect-fix rule rests on the
Maintainer's direction alone. The work follows the combined review-stance
plan and does not fold into it.

The binding authorization, quoted verbatim:

> "Accept, with my changes: promise-only defect fixes with no date cut-off; the per-plan total becomes a warning sign; no mandatory Known-defects cell; one small ship test. Answers to Q1–Q5 as recommended. The rate-limit gate is waived, not met."

### Opening-order allowance -- Maintainer, chat, 2026-10-19

The accepted source normally waits to open until the combined plan archives.
That plan was reopened at `01a8f73c` for Maintainer-requested follow-ups while
this draft was prepared. The Maintainer authorized opening now in response
to the explicit question about early opening with implementation still gated:

> Open now; keep implementation gated

This changes opening/review timing only. The implementation dependency below
remains in force; no accepted outcome is removed and no new Decision is scribed.

## Scope

Implement the four accepted outcomes: justified deferrals, small fixes to
broken promises, capture guidance that points at the one defect-fix rule,
and reuse as an author/reviewer duty. Preserve existing approval fences,
accepted-scope floors, review independence, disposition eligibility and
verification requirements. An issue or review note never supplies the
promise that authorizes a defect fix.

| Surface | Changes |
|---|---|
| `AGENTS.md`, `templates/core/AGENTS.md` | Add the compact defect-fix rule and person-step cost bar in Git and commit workflow; add the exception pointer to the existing deviation bullet. Put the accepted reuse rule in Project-specific conventions as one sentence. Cairn's own conventions give local ceremony examples; the shipped copy contains no Cairn-only paths. |
| `dev/plans/_template.md`, `templates/core/dev/plans/_template.md` | Add the defect-fix pointer beside the deviation rule, a Reuse question under Scope, and the three deferral reasons plus the open-plan home under Dispositions. Add no mandatory Known-defects cell. |
| `dev/agent_collaboration.md`, `templates/core/dev/agent_collaboration.md` | Explain that non-blocking is not permission to defer; extend lens 5's existing cross-document/reuse duty, keeping nine lenses. |
| `doctrine/lifecycle.md` | Canonical explanation of the three deferral reasons, cheap defects versus consequence-based eligibility, and a receiving open plan as an authorized live home. Preserve the no-required-order rule. |
| `doctrine/plans.md`, `doctrine/proposals.md` | Both deferral block shapes name a reason and the Maintainer's quote; plans doctrine also conforms the nit label, sharpening paragraph, deviation pointer and open-plan home list. |
| `doctrine/dual-review.md` | Conform the blocking test, deviation pointer, and the existing lens-5 description to the same duties; add no lens or new review tier. |
| `templates/modules/team-gated/issue-capture.md`, `dev/modules/issue-capture.md`, `doctrine/roles.md` | Replace capture-first guidance with the pointer to the one operational rule; retain the User Agent's scope-not-size boundary. Keep the module twins byte-identical. |
| `templates/core/dev/PLANNING.md` | Conform the deferral-home bullet and add a thin pointer to the governing reasons; no second definition of the rule. |
| `bootstrap/tests/test_stewardship_rules_ship.py` | One small test of the load-bearing sentences, including a real fresh install selecting issue-capture. No carrier-by-carrier mutation framework or exhaustive clause matrix. |
| `dev/PLANNING.md`, `CHANGELOG.md` | At archive only: conform Cairn's archive-precondition mirror, record the new test's final collection/blob handoff on the standing re-anchor row, and write the changelog entry. |

Proposed paths:
* `bootstrap/tests/test_stewardship_rules_ship.py` — one small ship test, created during implementation.

**Reuse.** No runtime code is added. The one test reuses pytest's `tmp_path`
and the existing public scaffold CLI, with an explicit profile selecting
`issue-capture`; it does not introduce an installer helper. I searched
`bootstrap/tests/` for `AGENTS.md`, `agent_collaboration.md`, the plan-template
paths and `issue-capture.md`, then opened the readers. The comparison cases
are `test_review_and_verification_rules_ship.py` (collapsed-text sentence
pins) and `test_review_sweep_ships.py` (real CLI installs). Adapt their small
patterns locally; importing another test's private helpers or adding a
shared abstraction for one test buys nothing. Existing intentionally
byte-identical self-hosted twins remain twins, not accidental near-copies.
The reuse check is a reviewer action; the redundancy gate is not described
as a duplicate-code detector.

### Operative wording boundaries

The compact rule in both operational references must say, in substance:

* A defect breaks something the file, its docstring, tests or governing text
  already promises. A fix restores that promise; a note, issue or review
  comment cannot manufacture it. There is **no date cutoff**.
* The fix stays in a file the work already edits, adds no file, function,
  option or public name, changes no rule text, and carries its own test in
  the range independently reviewed. Its own defect lines and test are the
  scope. A plan's explicit fence still wins; this does not authorize removing
  accepted scope. The same promise/cost/test/review conditions govern work
  with no accepted proposal or plan.
* The commit body records one line:
  `Defect fix: <promise> -> <file> -- test <path::node> -- changes no rule text`.
  The code reviewer finds these lines in the reviewed range and checks each
  promise against the actual file/tests/governing text, the existing file
  scope, the test and the no-rule-change claim. No age check is owed.
* Cheap excludes high-risk, contract and hash-pinned surfaces, Maintainer-only
  steps, Security Review, new proposals and decisions. Uncertainty about
  needing one means not cheap. Test runtime is machine time, never a reason
  by itself to defer; this changes no verification trigger or schedule.

Keep the operational addition compact, roughly the Decision's dozen lines
of rule and cost-bar text rather than Revision 1's nested procedure. Put
explanation in doctrine and pointers in the module and templates. The reuse
rule is **one sentence** covering searching for and using/extending existing
code, naming the search in a plan or commit body, and an existing project map
where present. Add no new slot. Plans may name fixes in Scope without a
compulsory new cell.

A growing total of incidental fixes is a **warning sign**, recorded in plans
doctrine alongside the scope pointer, not a hard quota or a route to
permission by size. A missing promise, a new public name, changed rule text,
an off-path file or an unmet fence remains a finding regardless of size.

### Current-tree accounting and documentation placement

At `f5ac63815cb88e524dfc96a588731d3c8b7d6053`, a whitespace-collapsed,
markup-stripped search over tracked Markdown outside archives, reflections,
reviews and live deliberation records for `struck chunk`, `deviating from an
accepted plan`, `deviation gate` or `deviated from approved scope` finds six
carriers: the `AGENTS.md` pair, the plan-template pair, `doctrine/plans.md`
and `doctrine/dual-review.md`. The `doctrine/plans.md` match is the positive
control for wrapped words. Preserve the six pointers; the Decision struck
the six-file mutation program, not these content changes.

Searches for `defer-OK`, `genuinely one-line`, `There is no required order`,
`Every deferred item` and `scope, not size` find the old labels and module
wording and the constraints to preserve in the named surfaces. The module
twins are identical. The published doctrine also contains lens 5, so its
existing description must agree with the two loop documents. The thin
installed dual-review module already points at the loop document; no change
there is planned. Re-read these facts after the predecessor archives and
before editing; counts in the proposal are historical measurements.

The 14 governing/module Markdown files named above have **no intersection**
with the committed gate manifest's `frozen_files` keys at that commit.
Existing tests read this prose and run unedited. The new test becomes frozen
at the next re-anchor. Re-measure before C1: an owning test that cannot stay
green unedited is a newly discovered changed surface, not authority to edit
a frozen test silently. Append the changed-surface/ceremony assessment and
obtain the existing deviation authorization if it changes this plan's fence.
No engine symbol or public manifest row is expected to change.

Per `docs/DOCUMENTATION_PLAN.md`, the operational rule belongs in the
`AGENTS.md` pair, its rationale in doctrine, the team/review duty in the loop
documents, and authoring prompts in the plan templates. This plan and its
source are deliberation. No README, profile, descriptive-doc or runtime
change is planned. The new test is dev-only and adds no dependency.

## Sequence

**Predecessor fence.** Implementation waits for the combined
`review-stance-and-lenses` plan to be archived, with its review findings
answered. Read the archived record, not an assumed active-path location.
Before C1 verify the sweep heading, lens 5's label and the nine-lens count.
The source's description of the broader ordering is stale: the predecessor's
"Recommended slot: third" actually places it before model-mapping, board and
this work. Decision Q4 supplies this plan's explicit dependency on the combined
plan; no new completion gate for the model-mapping engine work is invented.
Board-as-basis is archived at `60bf7cab`; model-mapping is now implementing.
Coordinate their shared communication files at serialization points. Opening
or reviewing this plan does not authorize starting C1 before its predecessor
fence is satisfied.

Re-read and claim every shared file at edit time. The live
`remove-collaboration-agreement` plan changes the same operational
references, loop documents, templates, plans/dual-review doctrine and board;
its existing text is preserved whichever edit lands second. A dirty shared
file is not included in this plan's commit. No chunk performs a re-anchor,
push, release operation or real-adopter upgrade.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Land the compact promise-only rule/cost bar, all six deviation pointers, module pointer and User Agent reconciliation together. | Fresh Internal plan review and author fold; predecessor fence; renewed reader/frozen-file search. | One explicit-path implementation commit; source and shipped rule/module agree. |
| C2 | Land justified deferrals, both home shapes, label/sharpening corrections, the Reuse question and one-sentence operational reminder, and lens-5 duties; add the one small ship test. | C1; re-read all twins and any agreement-removal edits. | One explicit-path implementation commit; all accepted outcomes present, live board mirror reserved for archive. |
| C3 | Run the reviewed scope, install/upgrade smokes and documentary dry run on the committed result; append evidence and move Status to awaiting-code-review. | C2; no implementation/test byte changes after measurement. | One plan-record commit; Certified by pending. |

Archive is its normal separate lifecycle transition after code review and
responses: perform board/changelog serialization, re-anchor handoff and
complete Dispositions. No extra human approval is invented for ordinary
implementation commits.

## Acceptance criteria

**C1.** Both operational references contain the same promise-only permission,
compact cost bar and commit-line form; they contain neither a record-created
permission nor a cutoff or cumulative cap. Each of the six deviation
carriers points at the one operational rule while preserving existing
approval requirements. The module twins are equal and point at that rule;
`doctrine/roles.md` retains its scope-not-size sentence. No extra behavioral
permission is independently restated in the module.

**C2.** The canonical archive rule and its pointers name all three reasons:
needs a Maintainer decision, belongs to work already in motion, or exceeds
the cost bar. Non-blocking/nit/low-priority labels and reviewer-suggested
homes are not reasons. Both block examples carry a reason and the verbatim
authorization; the in-motion form names a receiving open plan, and the
quoted permission covers the scope added there. Items are actually appended
to that plan; a pointer to an unopened or archived plan is not a live home.
Keep consequence-based wontfix exclusions and no prescribed disposition order.
A true cheap defect is fixed unless fixing it needs a decision; a label alone
cannot turn it into wontfix. Remove `defer-OK` from plans doctrine.

Both plan templates ask Reuse, accept N/A for no code added, and add no
mandatory Known-defects cell or slot. The operational reuse rule is one
sentence in each copy. Lens 5 keeps its name and number, requires checking
the author's search and a reviewer-chosen search with a known positive
control, and treats an accidental near-copy as a finding with reuse or
generalization as satisfier. Exactly nine lenses remain.

**Small test boundary.** One test in the proposed test file reads a real
installed `AGENTS.md` and issue-capture module, plus the canonical deferral
text and plans-doctrine label. It pins only the three reasons, the
promise-restoring defect sentence/cost bar, the module's pointer and absence
of `defer-OK`. Expectations are literal and independent of source extraction.
No generated clause matrix, per-token parametrization, negative-test copy
framework or six-carrier mutation program is introduced. Remaining wording,
reuse duty and authority limits are reviewed against the Decision and the
owning tests, without claiming this small test proves all policy semantics.

**C3.** The public `scaffold.py --manifest` is byte-identical to the
pre-implementation committed baseline. A fresh explicit issue-capture
install receives the new operational rule and module pointer and passes
integrity verification. Existing project edits survive scratch upgrade
stage/apply; report any conflicts and do not bless them automatically.
Re-evaluate the six baseline wontfix examples in the archived
`verification-practice` and `maintainer-attention` plans, as identified in the
source's Revision 1 Evidence: preserve their outcomes, separating the
frozen-file person-step from test runtime in the rationale. Record the
comparison; do not edit those archives.

The verification record carries tested commit/range, canonical interpreter,
clean unchanged pre/post state, exact commands, counts and timing, every
non-pass disposition and omissions. It lists the new test's actual node
and code-reviewed blob for the archive handoff. It claims no certifying
suite from this scoped run.

**Independent scientific check:** N/A: no scientific assumption or result
touched. Security preflight remains N/A as in the accepted source: no new
executable trust boundary or named high-risk surface is introduced. The
Internal reviewer must challenge the changed authority rule, especially the
promise-versus-note distinction and the rule-text/fence exclusions. Review
is required(Internal), not Internal Security Review.

## Scope delta

**Scope delta**: preserved against Revision 1 **as narrowed by the Decision**.
The struck date/record route, mandatory cell, hard total and expansive test
program are not accepted scope. No remaining accepted outcome is deferred.
The person-step bar and all four substantive outcomes remain. A future
request to change a rule, add behavior nobody promised, alter a frozen test
or remove an accepted outcome uses the existing deviation path.

## Verification

**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`;
confirm the path and 3.13.x version in the evidence record.
**Boundary B mode**: full, retaining the source's conservative classification.
**Boundary B execution**: the scoped mapping below on a clean committed tree.
**Certified by**: pending. The full suite runs only at the next authorized
certifying point; nobody sets its switch for this plan's own run.

### Reviewed mapping for Boundaries A and B

The reader search uses file references and actual reads, not test filenames
alone. Re-search after intervening work and before C1. File names below are
under `bootstrap/tests/`; run them in explicit batches of at most 25 files
so the broad-run guard remains in force.

| Changed property/path | Owning tests and checks |
|---|---|
| AGENTS pair, deviation rule, compact cost/reuse addition | `test_review_and_verification_rules_ship.py`, `test_verification_boundaries.py`, `test_certifying_run_rule.py`, `test_comprehension_floor.py`, `test_scope_reduction_trap.py`, `test_review_stance_in_shipped_files.py`. |
| Loop documents, blocking wording and nine-lens interface | `test_review_sweep_ships.py`, `test_review_stance_in_shipped_files.py`, `test_scope_reduction_trap.py`; compare the two operative sections with slot/local differences accounted for. |
| Plan templates and canonical doctrine | `test_scientific_check_guidance_ships.py`, `test_scope_reduction_trap.py`, `test_verification_boundaries.py`, `test_certifying_run_rule.py`, `test_documentation_plan_module.py`. Check both defer examples and all six pointers by reading the actual final text. |
| Installed rule/module, core and board-template delivery, manifest | New small ship test; `test_scaffold.py`, `test_scaffold_substrate.py`, `test_core_dev_folders.py`, `test_module_merge_lockfile.py`, `test_manifest.py`, `test_notice_install.py`, `test_quickstart_sequence.py`, `test_presets.py`, `test_profiles_smoke.py`. |
| Upgrade merge and integrity | `test_upgrade.py`, `test_verify_integrity.py`, `test_lockfile_module.py`; scratch rehearsals below. |

`test_loop_fidelity_gate.py` is also a scoped regression check for the doc
checker used here; its similarly named scratch templates are not evidence
that it reads this plan's source files. The roles/module and board-mirror
wording has no dedicated semantic owner found beyond the proposed small
ship test/module delivery and the document gates. Say so in the final record;
the pending certifying run supplies broader integration coverage, not a
claim that a pattern test proves the rule's soundness.

**Standing document gates:** claim-check on each authored document; prose
integrity via `python scripts/check_cairn.py` with edited paths explicitly
named; `python scripts/link_check.py` on those paths;
`python scripts/sync_doc_snippets.py --check` on edited Markdown; and
`python scripts/quality_gate.py --sub neutrality --sub redundancy` (these
legs do not dispatch pytest). Record baseline and final flags by identity,
not merely equal counts. Assess R1 duplication for the canonical lifecycle
paragraph versus its pointers. Resolve new live flags before code review;
identify inherited archive-history flags rather than editing old records.

**Public-path smokes:** capture manifest output at the clean implementation
base and final commit and compare exact bytes. Run summary/dry-run for each
of the three shipped profiles. Install an explicit issue-capture profile in
a fresh scratch directory and read the actual installed files. Rehearse
upgrade plan/stage/apply on separate scratch copies of LHM and modflow_tools,
never in their real checkouts; where pre-existing drift blocks apply, record
that limit and exercise preservation on a scratch project with deliberate
local edits. Report conflicts; do not automatically finalize modified
project governance. The six baseline disposition comparisons are a written
check, not a new parser.

**Boundary C:** a fresh non-implementing code reviewer checks the Decision
against the final rule, the six pointers, the compact test and evidence.
The six-carrier mutation program is explicitly struck; do not reinstate it
as plan acceptance. Any independent targeted falsification remains governed
by the standing review rules. If repairs change implementation/test bytes,
repeat the affected scoped stable run and retain certification as pending.

## Dispositions

At archive, attest every follow-up with a `Dispositions:` line and actual
live home where owed; no outstanding task is left only in an archived plan.
Conform Cairn's live archive-precondition mirror at that serialization
point, preserving surrounding board work. Add the changelog entry in the
archive commit. The source's rate-limit waiver is recorded above, not
reported as recurrence evidence.

The new test joins the standing gate-manifest re-anchor row at archive:
record its actual node ID and final git blob at the code-reviewed commit.
No existing frozen file or engine symbol is expected to change. If the
Maintainer re-anchors before that test is final, another re-anchor is owed;
this plan records that consequence and never performs the ceremony. Quote
the accepted source authorization on the board deposit. Verify the actual
frozen intersection again, so any additional obligation is named explicitly.

## Plan review -- Antigravity (Gemini 3.8 Flash, fresh session) -- 2026-10-19

```
Reviewed commit: d140ad2fc4ef407cf11bbcef25f0ed6c6c9922a3
Target: the entire opened plan against the accepted proposal's Revision 1 and Decision
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: ACCEPT

**Foundations**:

1. **Should this happen as framed?** Yes; the plan delivers the Decision's premise faithfully: promise-only defect fixes with no date cut-off, the per-plan total as a warning sign, no mandatory Known-defects cell in plan templates, a single-sentence reuse duty in both `AGENTS.md` copies, and one small ship test without an expansive mutation matrix -- `dev/proposals/archive/2026-10-18-claude-stewardship-and-reuse.md:1388-1428`; `dev/plans/stewardship-and-reuse.md:12-24, 39-44, 77-110, 207-216`.
2. **Best alternative.** The plan already chose the simplest path: compact operational additions in `AGENTS.md` and `templates/core/AGENTS.md` (~a dozen lines), thin pointers in the six deviation carriers, issue-capture guidance pointing at the single operational rule, and a single small ship test reusing pytest's `tmp_path` and scaffold CLI rather than new test infrastructure -- `dev/plans/stewardship-and-reuse.md:46-58, 62-73, 98-105, 207-216`.
3. **What would show it wrong.** A test treating notes, issues, or review comments as manufacturing an authorized promise; silent deletion or unapproved dropping of accepted scope; drift between module twins; or installed module text failing integrity verification -- `dev/plans/stewardship-and-reuse.md:79-87, 181-187, 218-221`; `bootstrap/tests/test_scope_reduction_trap.py`.

The plan adheres strictly to the narrowed contract established by the Maintainer Decision. The four accepted outcomes (justified deferrals, small fixes to broken promises, capture guidance pointing at the one defect-fix rule, and reuse as an author/reviewer duty) are mapped with precision.

Observations across the nine lenses:
* **Claims and drift (#1, #6):** All references, commit citations (`d140ad2f`, `60bf7cab`, `01a8f73c`, `f5ac6381`), source proposal paths, verbatim Decision and chat allowance quotes, and proposed test paths match the repository state.
* **Production path exercised by tests (#2):** Public entry point `bootstrap/scaffold.py` installing `issue-capture` profile into a fresh scratch directory and verifying integrity is explicitly exercised in C3 and in `test_stewardship_rules_ship.py`.
* **Design completeness (#3):** The scope boundaries, cheap cost-bar definition (counting person-steps rather than machine runtime), commit-line format, warning-sign status, and carrier inventory are stated completely.
* **Silent failure / fail-closed (#4):** Fences remain binding; promises cannot be manufactured by review notes or issues; uncertainty resolves to not-cheap; Boundary B mode is full (retaining source classification) with certifying run pending.
* **Cross-document consistency (#5):** All 6 deviation carriers (`AGENTS.md`, `templates/core/AGENTS.md`, `dev/plans/_template.md`, `templates/core/dev/plans/_template.md`, `doctrine/plans.md`, `doctrine/dual-review.md`) are mapped. Module twins are kept byte-identical. Lens 5 is updated consistently across loop documents and dual-review doctrine without changing the nine-lens interface.
* **Lifecycle / process placement (#7):** C1-C3 chunks are cleanly sequenced. Predecessor fence (`review-stance-and-lenses` archived) is tracked and satisfied on master (`0974a4de`). Archive ceremony tasks (re-anchor row update with actual node ID/blob, board deposit quoting Decision, changelog) are correctly assigned to the archive transition.
* **Domain / scientific validity & scope (#8):** Scientific validity is N/A (no scientific result or calculation touched). Scope delta is preserved as narrowed by the Decision; no accepted scope is dropped.
* **Name the satisfier (#9):** No defects found; 0 findings raised.

**Coverage -- Covered:** claims #1-#9; scope boundaries against Decision; carrier inventory; predecessor fence status (confirmed archived at `0974a4de`); small test boundary; doc gates. Not covered / low confidence: no implementation exists to execute; no suite, mutation, install, real-project upgrade, or ceremony was run for this plan review.
