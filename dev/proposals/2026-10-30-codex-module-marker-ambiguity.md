# Refuse ambiguous module task markers during repeat installation

**Author**: Codex (gpt-6.1-sol)
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Prevent repeat installation from duplicating a completed module task when its generated marker has been edited.

## Context

The accepted module-discovery proposal promises no duplicate tasks and conservative refusal for ambiguous adopter edits (`dev/proposals/archive/2026-10-29-codex-module-discovery-activation.md`). The reconciler searches only for an exact opening marker (`bootstrap/_scaffold/install.py:1375`) but the installer enters reconciliation when the broader marker substring occurs (`bootstrap/_scaffold/install.py:1569`). A public-path probe installed `reflections`, added one space before its task marker's closing `-->`, checked its task, then repeated the same install. Both calls returned 0; `dev/PLANNING.md` contained two reflections tasks, one checked and one unchecked. This was measured on 2026-10-30 using `bootstrap.scaffold.main` and an isolated temporary target. The original task was retained, but the duplicate makes first use ambiguous.

## Proposal

Treat any marker-like task or inventory entry inside the generated regions that cannot be parsed as a complete, unique entry as an ambiguity conflict. Refuse before changing the planning board, module inventory, or lockfile, and tell the adopter to save and reconcile the edited entry manually. Preserve exact valid markers, selected edited/completed entries and unrelated prose. Apply the same rule in repeat install and later adoption, including the already-adopted path. Do not attempt to repair marker spelling automatically or infer identity from task prose. This restores the existing discovery contract without adding a module or an onboarding obligation.

## Rationale

The current parser can confuse an edited generated marker for unmarked prose and append a second task. A refusal protects the adopter's completed work and gives one clear recovery action. The same ambiguity rule belongs at the shared reconciliation point so install and adoption agree.

## Alternatives considered

Accept loose marker spacing and normalize it: this fixes the measured example but keeps an open-ended grammar for malformed or conflicting identities. Delete malformed blocks and regenerate: that can erase completed or edited adopter work. Leave the behavior: duplicate first-use tasks break the accepted promise and can mislead an agent reading the board.

## Documentation / doctrine surface

The behavior belongs in `bootstrap/_scaffold/install.py`, with tests in `bootstrap/tests/`. If the existing manual recovery text does not cover this case, update the installed module guidance or error message. No doctrine rule or new module is proposed.

## Evidence / verification plan

### Tests required

Extend `bootstrap/tests/test_onboarding_seed_roster.py` with the public repeat-install probe above. Exercise the public `upgrade --adopt-module` path, including repeat adoption, in `bootstrap/tests/test_upgrade_module_additions.py`. For both tasks and inventory, vary an edited opener, edited closer, duplicate identity and harmless unrelated prose; check refusal leaves planning, inventory and lock bytes unchanged. Check a valid selected completed task remains single and checked, and an unchanged entry for a removed module still disappears. Search readers/callers of the changed parser and run their owning tests. Use a mutation that restores the current permissive behavior and confirm the new public probe fails against a passing unmutated control.

### Examples / smoke checks

Run the scaffold's real temporary install and later-adoption paths; run `scripts/check_cairn.py`, `scripts/claim_check.py` on changed prose, `scripts/link_check.py`, `scripts/sync_doc_snippets.py --check`, and the neutrality gate. Boundary B is wide on a clean committed candidate under Python 3.13 because this changes installation reconciliation. Whole-tree certification remains a separate release ceremony.

#### Security preflight — five questions, answered in writing

**S1 — Who supplied it?** The project owner can edit installed Markdown markers and the profile selects modules; the reconciler must treat that project text as untrusted state, not as authority to delete or duplicate work.

**S2 — Can it fail?** The new public probe must fail if the ambiguity guard is removed or relaxed to the current exact-only search. This mutation is proposed, not yet run.

**S3 — What fires it, over what?** `bootstrap/scaffold.py` install and `upgrade --adopt-module` invoke reconciliation over the installed planning slot and generated inventory block. The adopter-facing promise is “no duplicate tasks, no tasks for absent modules, and no silent deletion of adopter edits” in the accepted discovery proposal; a duplicate violates it.

**S4 — Which way does it break?** Unknown, malformed or conflicting markers must cause a reported refusal. A permissive fallback adds a duplicate task, granting generated content more authority than the edited adopter state.

**S5 — Who still wins?** The proposed guard handles ambiguous generated markers, not an owner who deliberately rewrites unmarked planning prose to resemble a separate task. This class is narrowed by syntax checks, not closed for arbitrary prose.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A valid checked task is reset or duplicated, unrelated prose is removed, a malformed entry still appends a new task, or refusal changes any of the three generated artifacts.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance — the scaffold engine and install contract are touched.

## Review -- Codex (gpt-6.1-sol) -- 2026-10-30

**Reviewed commit**: ae80c5de

**Tier**: usual

**Verdict**: SUPPORT, with one non-blocking clarification.
**Elapsed**: about 6 minutes; **tokens**: unknown.

**Foundations**:

1. **Should this happen as framed?** Yes. On a temporary target, a public `bootstrap.scaffold.main` repeat install returned 0 after I added a space to a checked reflections task opener; the board then had two reflections tasks, one checked and one unchecked. This violates the accepted no-duplicates promise in `dev/proposals/archive/2026-10-29-codex-module-discovery-activation.md`.
2. **Best alternative.** A single preflight grammar check within `_reconcile_generated_blocks` is simpler than adding tolerant spelling or identity inference in both install and adoption. The exact opener parser and broader caller trigger currently disagree at `bootstrap/_scaffold/install.py` lines 1375 and 1569.
3. **What would show it wrong?** If preflight rejects unrelated prose or permits a malformed identity to duplicate work, the rule misses its purpose. Public tests should assert both outcomes through `bootstrap/tests/test_onboarding_seed_roster.py` and `bootstrap/tests/test_upgrade_module_additions.py`.

**Finding 1 — non-blocking.** Define “marker-like” as a line anchored to a Cairn module marker stem inside the generated region, and state how malformed openers, closers and duplicate region delimiters are classified. Otherwise an ordinary note quoting marker text could be refused, or a near-spelling could be missed. A short grammar statement and a public harmless-prose example would close this; `bootstrap/_scaffold/install.py::_reconcile_generated_blocks` is the implementation home.

**Coverage**: Claims and public path: temporary repeat-install probe above; completeness and fail-closed: `install.py:1360-1450,1560-1590`; consistency and drift: archived discovery proposal and `bootstrap/tests/test_onboarding_seed_roster.py`; lifecycle and scope: this proposal's install/adoption and documentation sections; satisfier: Finding 1. No scientific claim applies. I did not run the suite, mutate code, or verify every malformed spelling; implementation and the separate Security Review remain open.

## Review -- Codex (GPT-6) -- 2026-10-30

**Reviewed commit**: ae80c5dec2a1a56b2817d3d26d31db727b7b0d2c  
**Target**: proposal and installation/adoption reconciliation boundary  
**Prior findings**: none  
**Assurance path**: high-assurance  
**Tier**: Security Review  
**Findings**: raised  
**Verdict**: REVISE  
**Elapsed**: approximately 3 minutes  
**Tokens**: unknown

**Foundations**:

1. **Should this happen as framed?** Yes: edited owner state can be mistaken for missing generated work; refusing before writes protects that state, and the engine is a high-risk surface (`bootstrap/_scaffold/install.py:1375-1401`, `dev/proposals/archive/2026-10-29-codex-module-discovery-activation.md`).
2. **Best alternative.** A bounded, line-anchored marker grammar at the shared reconciler is less costly and safer than fuzzy recovery; arbitrary prose cannot reliably identify a module (`bootstrap/_scaffold/upgrade.py:1908-1935`).
3. **What would show it wrong?** A public install or adoption that accepts ambiguous markers and changes discovery bytes, or refuses ordinary unrelated prose, falsifies the intended boundary (`bootstrap/tests/test_onboarding_seed_roster.py`, `bootstrap/tests/test_upgrade_module_additions.py`).

**Finding 1 — non-blocking.** In addition to defining marker-like syntax, specify that entry spans must be non-overlapping and properly paired, and test nested or crossed markers through a public path. The current parser independently searches for each matching closer (`bootstrap/_scaffold/install.py:1382-1401`), so a complete-looking opener can be inside another entry; the later deletion loop uses those spans independently. A sequential pairing rule and a refusal test that preserves all three artifact bytes close this gap.

**Finding 2 — non-blocking.** Cover the repeat-install preflight when no modules are selected and an opener is malformed: the caller decides whether to reconcile using the exact substring (`bootstrap/_scaffold/install.py:1566-1571`), so a guard solely inside the reconciler may never run. Specify the intended trigger and test the public path, including unchanged bytes on refusal. The owner controls this local text; this is preservation of work, not a claim of protection against a malicious owner.

**Coverage**: Claims and public path: proposal probe and `install.py:1566-1590`; completeness and fail-closed: `install.py:1375-1445` and `upgrade.py:1908-1935,2025-2035`; consistency and drift: archived discovery proposal and the two named test files; lifecycle and scope: high-assurance declaration and engine ownership in `dev/proposals/_template.md`; scientific scope: no scientific result; satisfiers: findings above. Not covered: execution, mutation, every malformed spelling, or filesystem race behavior; this is a proposal review, not implementation verification.
