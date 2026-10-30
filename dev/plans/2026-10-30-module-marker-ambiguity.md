# Plan: Refuse ambiguous module discovery markers

**Source proposal**: dev/proposals/archive/2026-10-30-codex-module-marker-ambiguity.md
**Status**: ready-to-implement
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Refuse damaged generated module markers before repeat installation or adoption can duplicate or remove adopter work.

## Source proposal

The accepted heavy-tier proposal requires bounded marker validation through the
shared reconciler, including empty module selection and repeat adoption. It
preserves completed tasks and unrelated prose, refusing ambiguous state before
planning, inventory or lockfile changes. The Decision remains in the source
proposal; this plan grants no release or ceremony authority.

## Scope

Change `bootstrap/_scaffold/install.py` and, where caller wiring requires it,
`bootstrap/_scaffold/upgrade.py`. Extend public-command tests in
`bootstrap/tests/test_onboarding_seed_roster.py` and
`bootstrap/tests/test_upgrade_module_additions.py`. Keep exact existing entry
syntax, column-zero family stems, sequential identity pairing and
non-overlapping spans. Do not infer identity from prose or automatically repair
markers. Preserve the existing unknown-entry refusal and selected-entry edits.

**Reuse.** Searches for `_reconcile_generated_blocks` and
`_substitute_module_inventory` found the common parser, repeat-install callers,
upgrade inventory rendering and `_prepare_module_discovery`. Reuse these
paths rather than adding a second parser. Searches for `module-task` and
`module-inventory` found the two primary test families plus
`bootstrap/tests/test_install_time_onboarding.py` and
`bootstrap/tests/test_onboarding_slot_substitution.py`; include those consumers.
No new dependency is planned; `bootstrap/DEPENDENCY_BUDGET.md` remains binding.

### Documentation / doctrine surface

No doctrine surface. Explain the manual save-and-reconcile recovery in the
reported conflict; inspect `docs/agent-team-onboarding.md` and
`bootstrap/UPGRADE.md`, updating existing descriptive recovery guidance only
if it contradicts or omits the new case. No new module or onboarding task.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Validate generated regions and route all relevant install/adoption callers through the shared preflight | Both plan reviews | Parser and caller correction; public refusal and preservation tests |
| C2 | Verify recovery guidance, fault detection and complete affected consumers | C1 | Mapped checks, mutation evidence and final wide verification for independent code and Security reviews |

## Acceptance criteria

### C1

Within each generated region, column-zero lines beginning
`<!-- cairn:module-task` (tasks) or `<!-- cairn:module` (inventory) must match
existing exact entry syntax, pair sequentially by identity and never overlap.
Malformed openers/closers, duplicate identities, nested/crossed entries and
missing, reversed or duplicate region delimiters refuse. Repeat install,
empty-roster install and adoption (including already-adopted modules) refuse
before planning, inventory or lock bytes change. Diagnostics direct manual
saving and reconciliation. Inline, indented and blockquoted mentions survive;
valid selected edited/completed entries remain single and checked, unrelated
prose survives and unchanged removed-module entries disappear. The public
regression covers the edited closing-space example and two spaces before
`id=` with empty selection.

### C2

Public paths exercise both task and inventory cases and preserve all three
artifact bytes on refusal. Unmutated controls pass. Separate mutations removing
the ambiguity guard, restoring the narrow caller trigger and restoring
independent closer search each fail an appropriate public regression. Record
all survivors and measured equivalents. Guidance agrees with measured recovery.
Final clean-commit wide verification passes the mapped checks; independent
ordinary code and code Security Reviews remain separate obligations. No
scientific check applies because no scientific result or assumption changes.

## Scope delta

**Scope delta**: preserved.

## Verification

**Boundary A.** Under canonical Python 3.13.x on an isolated copy, run complete
`bootstrap/tests/test_onboarding_seed_roster.py` and
`bootstrap/tests/test_upgrade_module_additions.py` for parser behavior, install,
empty selection, later/repeat adoption and byte preservation. Add the C1 matrix
there through real scaffold entry points, not parser-only substitutes. Run
`bootstrap/tests/test_install_time_onboarding.py` and
`bootstrap/tests/test_onboarding_slot_substitution.py` for legacy migration and
slot consumers; `bootstrap/tests/test_upgrade.py` and
`bootstrap/tests/test_lockfile_provenance.py` for upgrade rendering and generated
output records; and `bootstrap/tests/test_security_lint.py` for the engine gate.
Split selections within the guard limit without overrides and reconcile their
union. Search all parser callers, readers and byte pins again; add any newly
identified owning functional checks before claiming completeness. Also run
`bootstrap/tests/test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package`
as a read-only baseline diagnostic in A/B. Derive its symbol delta using
`bootstrap/AST_BASELINE_RUNBOOK.md` step 1; identify intended changes and
unexplained missing, duplicate or changed symbols. Record expected baseline
drift for the version cut; it is not a passing functional check or a plan
completion prerequisite. Unexplained defects keep implementation open. Do not
update baseline fixtures, known-new manifests, protection manifests or refs,
or enter the runbook correction steps. No per-plan trust-root maintenance
or ceremony is required; stop any attempted authority write and report it.

For C2, use separate scratch copies for the three named mutations; report the
unmutated control, total, killed, each survivor and each measured equivalent
with its real-entry-point evidence. S1/S4/S5 stay as accepted. S2 occurs in C2;
S3 is public scaffold install and `upgrade --adopt-module`, backed by the two
primary families above. This does not claim resistance to arbitrary owner prose
rewriting or concurrent filesystem replacement.

Standing gates: `python scripts/claim_check.py` on changed prose;
`python scripts/check_cairn.py`; `python scripts/link_check.py`;
`python scripts/sync_doc_snippets.py --check`; and
`python scripts/quality_gate.py --sub neutrality --sub redundancy`.
Open each trigger and follow it to its runner; test negative reader searches
against known-positive parser callers. No new schema is planned.

**Boundary B: wide.** On the final unchanged clean implementation commit,
repeat the mapped owning families, public-path matrix, mutations and standing
gates under canonical Python 3.13.x. Append the template's tested SHA/range,
interpreter, clean pre/post states, command/count/timing/token table,
non-pass disposition, acceptance commands and omissions; record
`Certified by: pending`. Missing functional checks keep the work open;
dispose of the read-only baseline diagnostic as specified above. Full-tree
certification, repinning and re-anchoring are separate version-cut or
Maintainer-requested ceremonies, not prerequisites here.

**Boundary C.** A fresh non-author ordinary reviewer and separate Security
Reviewer read committed work and challenge the named marker grammar, caller
coverage and preservation contract. Record independent falsification and
bounding; do not rerun implementation checks or the full suite.


## Plan review -- Codex GPT-6.1 Sol (Reviewer) -- 2026-10-30

```
Reviewed commit: a72805e75646dc766b2efadf9d0f516f42442cfb
Target: complete plan and accepted proposal; non-author ordinary review
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised
**Verdict**: REVISE

**Foundations**:

1. **Should this happen as framed?** Yes: C1 preserves the accepted bounded grammar, empty-selection preflight and three-artifact refusal contract. The checked current parser independently searches closers and its caller uses the narrower substring. -- `bootstrap/_scaffold/install.py:1355-1448`, `:1569`; source proposal Proposal.
2. **Best alternative.** Keep the shared reconciler and existing command fixtures; a second parser would duplicate the rule. Both repeat adoption and ordinary adoption already reach discovery preparation. -- `bootstrap/_scaffold/upgrade.py:2024-2051`, `:2143`, `:2212`; `bootstrap/tests/test_onboarding_seed_roster.py:38-60`.
3. **What would show it wrong?** A malformed marker passing empty-selection install, or a refusal changing lock bytes, defeats C1. The mapped public tests and three mutations directly challenge these outcomes. -- plan Acceptance criteria and Verification.

**P1 (blocking): add the omitted AST-baseline check.** Engine edits trigger `bootstrap/AST_BASELINE_RUNBOOK.md` > “When this fires”; the mapped security-lint family does not run that check. Add `bootstrap/tests/test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package` to A/B, derive any delta using the runbook, and explicitly stop for Maintainer disposition when its authority limits apply. Do not infer that deferring re-anchor waives this required check. This mapping and failure disposition close P1.

**Covered**: claims/design/refusal (C1; install parser); production path/reuse (fixture helper and upgrade callers above); consistency/drift (accepted proposal; AST runbook); lifecycle/scope (C1/C2 gates; preserved scope); satisfier (P1's named test and disposition). **Not covered**: implementation, runtime/mutations, complete call-site enumeration or separate Security obligation; no suite run.

**Elapsed**: about 3 minutes. **Tokens**: unknown.

## Plan review -- Codex GPT-6 (Security Reviewer) -- 2026-10-30

```
Reviewed commit: a72805e75646dc766b2efadf9d0f516f42442cfb
Target: accepted scope, security preflight and verification mapping
Prior findings: none
Assurance path: high-assurance
Elapsed: about 4 minutes; tokens: unknown
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none additional
**Verdict**: REVISE until the ordinary review's blocking P1 is resolved.

**Foundations**:

1. **Should this happen as framed?** Yes: the plan requires refusal before changes to all three artifacts, including empty selection and repeat adoption, and preserves selected edits. The current caller's exact substring can miss a damaged marker. -- plan C1/C2; `bootstrap/_scaffold/install.py:1547-1570`.
2. **Best alternative.** A sequential bounded grammar in the existing reconciler avoids a second parser and identity guesses; both adoption branches already call the shared preparation. -- `bootstrap/_scaffold/install.py:1355-1401`; `bootstrap/_scaffold/upgrade.py:2024-2051,2143,2212`.
3. **What would show it wrong?** A public malformed-marker case that changes any protected artifact or accepts a crossed span, or a harmless quoted mention that refuses, would defeat the contract. The three planned mutants challenge the guard, trigger and closer search. -- plan C1/C2 and Boundary A.

The ordinary review's P1 is material to this security surface: `bootstrap/AST_BASELINE_RUNBOOK.md:17-18` identifies the engine baseline check, which the plan's mapped test families omit. Its named check and authority-limited disposition should be added; this is not a second finding.

**Covered:** claims and production entry points (install trigger and adoption calls above); completeness and failure direction (C1/C2 and sequential pairing); consistency and reuse (`_reconcile_generated_blocks`, `_substitute_module_inventory` callers in `install.py:1351,1570,2167` and `upgrade.py:442,2039,2051`); drift and lifecycle (accepted proposal Decision and AST runbook); domain and scope (no scientific result; plan Scope); satisfier (public matrix and mutants). **Not covered:** implementation, execution, mutation, exhaustive callers or full suite; no claim of race resistance.


## Response to plan reviews -- Codex GPT-6.1 (Strategy) -- 2026-10-30

| Finding | Disposition |
|---|---|
| Ordinary P1; Security's shared P1 | Accepted the omitted named AST check and read-only delta diagnosis in A/B. Expected baseline drift is recorded for the version cut, while unexplained defects remain blocking. No baseline repair, known-new regeneration or trust-root write is authorized here. |

The coordinating agent relayed the Maintainer's instruction that there is no
per-plan re-anchor or trust-root maintenance. Verification now separates
functional marker checks from the baseline diagnostic and removes the
unrelated frozen-manifest modification control. This changes no marker
acceptance outcome and does not waive functional failures. Both plan reviews
are answered; the plan is ready to implement without a clearing review.
Elapsed: about 3 minutes. Tokens: unknown.
