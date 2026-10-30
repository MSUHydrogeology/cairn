# Plan: Refuse ambiguous module discovery markers

**Source proposal**: dev/proposals/archive/2026-10-30-codex-module-marker-ambiguity.md
**Status**: ready-to-archive
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

## Implementation verification -- Codex GPT-6 (Implementation) -- 2026-10-30

**Boundary B mode**: wide checkpoint; incomplete pending the adoption
public regression. The changed engine reconciles adopter-owned task and
inventory regions through install, repeat install, upgrade inventory rendering,
and both new and already-recorded module adoption. These paths cross the
scaffold write/lock boundary, so the plan-mapped owning families, public paths,
security lint, three specified mutations, and standing gates were used.

**Certified by**: pending.

**Tested commit**: `629400c1dfd419b6669a7299f41add6393f84a64`.

**Reviewed range**: `c1326b45b8b52077db1c450c993e4e07268160c4` through
`629400c1dfd419b6669a7299f41add6393f84a64`.

**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` —
Python 3.13.13.

**Pre-run state**: clean isolated clone at the tested SHA; `git status --short`
empty. **Post-run state**: clean, same clone and SHA.

| Command or check | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---|
| `pytest bootstrap/tests/test_onboarding_seed_roster.py bootstrap/tests/test_upgrade_module_additions.py bootstrap/tests/test_install_time_onboarding.py bootstrap/tests/test_onboarding_slot_substitution.py bootstrap/tests/test_upgrade.py bootstrap/tests/test_lockfile_provenance.py bootstrap/tests/test_security_lint.py -q --tb=short` | 0 | 324 passed; 0 failed, skipped, xfailed or xpassed | 66.94 s | unknown |
| `scripts/check_cairn.py`; `scripts/link_check.py`; `scripts/sync_doc_snippets.py --check`; `scripts/quality_gate.py --sub neutrality --sub redundancy` | 0 | All pass; 188 Markdown files checked, 481 snippets checked; neutrality fail=0, redundancy fail=0 | about 2 s | unknown |
| Unmutated controls: `test_refuses_ambiguous_markers_without_writes` with `-k duplicate-region`, `-k malformed-opener`, and `-k crossed-entry` | 0 each | 1 passed per node | about 4 s parallel | unknown |
| Mutation 1: allow duplicate region delimiter lines; rerun duplicate-region public node in scratch commit `2e5edcfc` | 1 | Killed: the damaged empty-roster install returned 0 instead of refusing | about 1 s | unknown |
| Mutation 2: restore the narrow task-marker caller trigger; rerun malformed-opener public node in scratch commit `629400c1` | 1 | Killed: malformed opener was accepted and install returned 0 | about 1 s | unknown |
| Mutation 3: restore independent closer searches; rerun crossed-entry public node in scratch commit `629400c1` | 1 | Killed: crossed pair was accepted and install returned 0 | about 1 s | unknown |
| `pytest bootstrap/tests/test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package -q --tb=short` | 1 | 1 expected diagnostic failure; see AST disposition below | about 0.2 s | unknown |
| AST runbook step 1 `_merge_current` / `_classify` diagnostic | 0 | CHANGED 15; MISSING 0; DUPLICATE 0; NEW 143 | about 0.2 s | unknown |

**Mutation summary**: Unmutated control passed all three public nodes. Total 3;
killed 3; survivors 0; measured equivalents 0. Each mutant failed its named
real-entry-point regression as described above. Mutation 1 used an earlier
scratch commit whose parser bytes and duplicate-region case match the tested
commit; the later intervening change only refined the malformed-opener fixture.

**Non-pass disposition**: The AST diagnostic is the plan-specified read-only
version-cut check, not a functional acceptance check. It found 15 changed
symbols, no missing or duplicate symbols, and 143 new symbols. This plan changes
`FunctionDef:install_onboarding`; `FunctionDef:_reconcile_generated_blocks`
is a known-new symbol whose digest changes under this accepted parser edit.
The diagnostic also reports known-new drift in `_check_lockfile_paths`,
`_contained_lockfile_path`, and `_refuse_if_linked`. Other changed symbols are
not modified by this plan. No baseline, known-new
manifest, protection manifest, or trust root was changed; the plan explicitly
bars those repairs. This diagnostic remains for the version cut and is not a
passing functional check. The full suite, release certification, and re-anchor
were not run or authorized.

**Plan-specific acceptance commands**: The seven owning families above passed.
The public install tests cover empty selection, malformed opener/closer,
missing/duplicate/nested/crossed entries, duplicate/reversed regions, byte
preservation, removal of clean unselected entries, and inline/indented/quoted
mentions. Existing adoption tests and the full upgrade module-additions family
passed, but a new malformed-marker refusal is not yet directly regression-tested
through `upgrade --adopt-module` for both newly adopted and already-recorded
modules. This required public-path evidence is missing; implementation remains
open and no code-review handoff is claimed. The error directs manual saving and
reconciliation. No scientific check applies because no scientific result or
assumption changed.

**Verification-contract amendment (Maintainer direction, 2026-10-30)**: The
recovery paragraph in `bootstrap/UPGRADE.md` was committed separately at
`51bd8761e4683af19c548007f2e71fd320fc144d`. It changes descriptive prose only;
the code and tests at `629400c1` are byte-identical. Following the Maintainer’s
instruction below, the 324 code tests and three mutations remain evidence for
`629400c1`; prose checks ran on clean descendant `147128ea9f0fe148cba2b7e5d63482b49375a18d`.
On that descendant, `claim_check` on the guide, `check_cairn`, `link_check`,
`sync_doc_snippets --check`, and neutrality/redundancy gates passed. The four
guide-reading test files contributed 6 passed tests. `check_cairn` first found
two stale proposed paths in the concurrent tag-release plan at `51bd8761`; its
owner corrected them at `147128ea`, then the gate passed. Link check did not
probe 91 external links. Quality gates reported informational lines only.

Maintainer instruction, quoted verbatim: “Please review the remaining v0.6 work
and make sure we're applying the cut-the-apparatus changes, removing any
unnecessary process that has crept back in.”

**Elapsed**: about 17 minutes. **Tokens**: unknown.

**Handoff**: Maintainer assigned continuation to Luna. Keep status
`implementing` until the missing adoption regression and its mapped evidence are
complete. Do not archive or start code review from this checkpoint.

**Known omissions**: malformed-marker adoption through both branches of
`upgrade --adopt-module` still needs a public regression proving planning,
inventory and lock bytes stay unchanged. Arbitrary concurrent filesystem
replacement and arbitrary adopter prose rewriting were not tested, per C2.

## Implementation verification -- Codex Luna (Implementation) -- 2026-10-30

**Boundary B mode**: wide. The only implementation delta after the prior
checkpoint is a public regression in
`bootstrap/tests/test_upgrade_module_additions.py`; production parser and
caller bytes are unchanged from `629400c1`. The added cases cover task and
inventory damage through newly adopted and already-recorded
`upgrade --adopt-module` paths, and assert the refusal leaves planning,
inventory and lock bytes unchanged. The previous 324-test owning-family run,
three killed mutations and standing gates therefore remain evidence for the
unchanged production surfaces; the complete module-additions family was rerun
on this test delta. This follows the Maintainer direction above to avoid
repeating checks where the tested implementation bytes have not changed.

**Certified by**: pending.

**Tested commit**: `66214ccc1ea72bbb77e0e75d1d15082a4526b5d9`.

**Reviewed range**: `629400c1dfd419b6669a7299f41add6393f84a64` through
`66214ccc1ea72bbb77e0e75d1d15082a4526b5d9`.

**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` —
Python 3.13.13.

**Pre-run state**: clean detached clone at the tested SHA; `git status --short`
empty. **Post-run state**: clean, same clone and SHA.

| Command or check | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---|
| `pytest bootstrap/tests/test_upgrade_module_additions.py -q --tb=short` | 0 | 55 passed; 0 failed, skipped, xfailed or xpassed | 23.23 s | unknown |
| Four new adoption cases within that family | 0 | New/recorded adoption × planning/inventory malformed marker: all refuse with manual-reconciliation guidance and preserve all three bytes | included above | unknown |
| Prior mapped owning families at `629400c1` (recorded above) | 0 | 324 passed; 0 failed, skipped, xfailed or xpassed | 66.94 s | unknown |
| Prior three C2 mutations at `629400c1` (recorded above) | 1 each | All three killed by their named public regressions; 0 survivors or measured equivalents | about 1 s each | unknown |
| Prior standing gates at `147128ea` (recorded above) | 0 | `check_cairn`, `link_check`, `sync_doc_snippets --check`, neutrality and redundancy passed; 188 Markdown files and 481 snippets checked | about 2 s | unknown |

The plan-record commit `dc8f8944799bdfafb14180ba728cbe0a9e65c816` was
also checked in a clean detached clone with the canonical interpreter. Its
`claim_check`, `check_cairn`, `link_check`, snippet check, and neutrality /
redundancy gates all exited 0. Cairn and link checks each scanned 189 Markdown
files (90 and 91 external links were not probed, respectively); snippet check
scanned 482 documents; quality gates reported fail=0 (43 neutrality info and
1 redundancy info). Combined elapsed time was about 1.3 seconds; tokens unknown.

**Non-pass disposition**: An initial `git archive` scratch run lacked Git
metadata; the unrelated `--to HEAD` test could not resolve its explicit ref
and 1 of 55 tests failed. The complete family then passed in a clean detached
Git clone at the tested SHA, where `HEAD` resolves. This was a scratch harness
limitation, not a product failure. The AST diagnostic disposition remains as
recorded above: 15 changed symbols, no missing or duplicate symbols, and 143
new symbols; no authority-bearing baseline or trust-root file was changed.

**Plan-specific acceptance commands**: the malformed-marker adoption regression
ran through the public command for both adoption branches and both generated
surfaces, checking refusal and byte preservation for planning, inventory and
lock. The full module-additions family passed. The prior install/parser family,
three C2 mutations, and mapped consumers remain valid because production
parser and caller bytes are unchanged since their tested commit.

**Known omissions**: arbitrary concurrent filesystem replacement and
arbitrary adopter prose rewriting remain outside the plan's accepted scope.
No production source changed in this follow-up.

## Response to code review -- Codex Luna (Implementation) -- 2026-10-30

| Finding | Disposition | Evidence |
|---|---|---|
| F1: complete task and inventory damage matrix | Accepted; fixed | `test_refuses_ambiguous_markers_without_writes` now crosses both surfaces with malformed opener/closer, missing closer, duplicate identity, nested/crossed entries, and duplicate/reversed/missing region delimiters. Every public refusal checks planning, inventory and lock bytes. |
| F2: region conflicts need recovery direction | Accepted; fixed | Both missing/malformed/duplicate and malformed/reversed region diagnostics direct the adopter to save the files and reconcile manually before retrying. Public region-conflict cases assert the direction. |

Scope delta remains preserved. The existing shared reconciler and adoption
preflight remain in use; no second parser, new dependency, or automatic repair
was introduced. This response closes the findings without a clearing ordinary
review. The separate Internal Security Review remains owed.

## Implementation verification -- Codex Luna (F1/F2 response) -- 2026-10-30

**Boundary B mode**: wide. The change touches the shared marker reconciler and
the public install/adoption matrix; all mapped owning families and their
install, repeat-install, adoption and upgrade consumers were rerun because the
engine bytes changed. No full-tree suite or re-anchor was run.

**Certified by**: pending.

**Tested commit**: `022f6abe7824b961e9b1ae383f5a956cc65fe4ba`.

**Reviewed range**: `629400c1dfd419b6669a7299f41add6393f84a64` through
`022f6abe7824b961e9b1ae383f5a956cc65fe4ba`.

**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` —
Python 3.13.13.

**Pre-run state**: clean detached clone at the tested SHA; `git status --short`
empty. **Post-run state**: clean, same clone and SHA.

| Command or check | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---|
| `pytest bootstrap/tests/test_onboarding_seed_roster.py bootstrap/tests/test_upgrade_module_additions.py bootstrap/tests/test_install_time_onboarding.py bootstrap/tests/test_onboarding_slot_substitution.py bootstrap/tests/test_upgrade.py bootstrap/tests/test_lockfile_provenance.py bootstrap/tests/test_security_lint.py -q --tb=short` | 0 | 340 passed; 0 failed, skipped, xfailed or xpassed | 77.40 s | unknown |
| New public matrix: both surfaces × 10 damage forms, in the mapped command above | 0 | 20 passed; each refusal preserved planning, inventory and lock bytes | included above; focused pre-run 1.19 s | unknown |
| Mutation 1: permit duplicate region delimiters; rerun public `-k duplicate-region` nodes in isolated clone | 1 | Killed: both task and inventory cases returned success instead of refusing; unmutated matrix passed in the control | under 1 s | unknown |
| Mutation 2: restore the narrow task opener substring trigger; rerun public `-k malformed-opener` nodes in isolated clone | 1 | Killed: task case returned success instead of refusing; inventory control passed | under 1 s | unknown |
| Mutation 3: restore the pre-sequential independent-closer parser from `43af2e12^`; rerun public `-k crossed-entry` nodes in isolated clone | 1 | Killed: both task and inventory cases returned success instead of refusing | under 1 s | unknown |
| `test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package` | 1 | 1 expected read-only diagnostic failure; see disposition below | 0.14 s | unknown |
| AST runbook step 1 `_merge_current` / `_classify` | 0 | CHANGED 15; MISSING 0; DUPLICATE 0; NEW 143 | 0.2 s | unknown |
| `claim_check dev/plans/2026-10-30-module-marker-ambiguity.md`; `check_cairn.py`; `link_check.py`; `sync_doc_snippets.py --check`; `quality_gate.py --sub neutrality --sub redundancy` | 0 | Claim check no flags; Cairn/link 189 Markdown files (88/89 external links not probed); snippet check 482 docs; quality fail=0 (43 neutrality info, 1 redundancy info) | about 1.3 s in parallel | unknown |

**Mutation summary**: The unmutated mapped control passed 340 tests. Total 3;
killed 3; survivors 0; measured equivalents 0. Mutation 1 failed both public
region cases, Mutation 2 failed the malformed-task public case while its
inventory control passed, and Mutation 3 failed both crossed-entry public
cases. Each mutant ran in its own detached scratch clone.

**Non-pass disposition**: The AST diagnostic remains a version-cut diagnostic,
not a functional failure. The existing 15 changed symbols, 0 missing, 0
duplicate and 143 new are recorded from the required read-only derivation. This
patch intentionally changes the known-new digest for
`FunctionDef:_reconcile_generated_blocks` by adding the recovery direction;
the prior `_check_lockfile_paths`, `_contained_lockfile_path` and
`_refuse_if_linked` known-new drift is unchanged. No baseline, known-new
manifest, protection manifest, or trust root was modified. A pre-commit shared
worktree run had 93 passes and one source-fidelity refusal because its edited
engine differed from `HEAD`; the clean detached candidate run above passed.

**Plan-specific acceptance commands**: the seven mapped test families above
pass, including the public install matrix and previously added public adoption
cases for both adoption branches. The three C2 mutations are killed through
public install regressions. No schema, snippets, doctrine or shipped template
changed; no scientific result or assumption changed.

**Known omissions**: arbitrary concurrent filesystem replacement and
arbitrary adopter prose rewriting remain outside the accepted scope. The
separate Internal Security Review is outstanding.

## Code review -- Codex GPT-6.1 (Reviewer) -- 2026-10-30

**Reviewed commit**: `4a097b18` (implementation `629400c1`, adoption tests `66214ccc`). **Obligation**: Internal. **Verdict**: REVISE. **Findings**: two blocking.

**Foundations**:

1. **Should this happen as framed?** Yes. Sequential identity pairing in `bootstrap/_scaffold/install.py:1425-1474` closes the independent-closer ambiguity while retaining selected blocks at `:1513-1520`.
2. **Best alternative.** Reuse the shared reconciler: both adoption branches call `_prepare_module_discovery` (`bootstrap/_scaffold/upgrade.py:2143,2212`), which preflights both surfaces (`:2024-2051`). A second parser adds drift.
3. **What would show it wrong?** Acceptance of a crossed or malformed marker, a write on refusal, or loss of selected work would contradict C1. The public tests and three killed mutants in the verification record challenge these outcomes, but see F1 and F2.

**F1 (blocking): complete the accepted public matrix.** The source proposal's Tests required calls for opener, closer, duplicate identity, nested/crossed markers and duplicate region delimiters for *both* surfaces. `test_onboarding_seed_roster.py:164-171` tests these primarily for tasks and only malformed closer for inventory; the adoption regression adds malformed openers only. Add the missing public surface/damage combinations with three-artifact byte preservation to meet that required check.

**F2 (blocking): give recovery guidance for region conflicts.** `install.py:1401-1407` reports missing, malformed or duplicate region markers without directing manual saving and reconciliation; `cli.py:596-598` prints that message unchanged. C1 requires that direction on conflicts. Supply it for these errors and verify it through the public path.

**Falsification ledger**: Inspected the sequential parser, install trigger, both adoption callers, public test parameters and recorded mutation outcomes. The missing inventory matrix and unhelpful region errors falsify complete acceptance; no implementation tests were rerun. **Bounding**: WIDER RUN REQUIRED for the missing required public combinations. Verification records identify clean commits, Python 3.13.13, mapped checks and the expected AST diagnostic disposition; unchanged implementation evidence is retained under the recorded Maintainer direction.

**Covered**: claims, public path, completeness and failure direction, consistency and reuse, drift, lifecycle and scope, domain, and satisfier (paths and evidence above; no scientific change). **Not covered**: arbitrary prose rewriting, concurrent replacement, full suite, or the separate Security Review. **Elapsed**: about 4 minutes. **Tokens**: unknown.

## Code Security Review -- Codex GPT-6.1 Sol -- 2026-10-30

**Reviewed implementation**: `022f6abe`; verification `d310b0f4` / `a5fd365e`; handoff `bcdaa398`. **Obligation**: Internal Security Review. **Verdict**: ACCEPT. **Findings**: none.

**Foundations**:

1. **Should this happen as framed?** Yes. Sequential active-entry validation rejects nested/crossed identities before reconciliation; install preflights inventory before task writes, and adoption prepares both before applying either (`install.py:1400-1481,1621-1639`; `upgrade.py:2024-2057,2143,2212`). This protects adopter work without automatic repair.
2. **Best alternative.** Keep the shared reconciler and bounded column-zero grammar. Independent closer searches permit overlapping spans; fuzzy recovery would guess ownership. The existing wrapper also serves upgrade rendering and lock precomputation (`install.py:1351,2249`; `upgrade.py:442`).
3. **What would show it wrong?** Acceptance of malformed boundaries or any discovery/lock write during refusal would falsify the preservation contract. Public probes below challenged both outcomes.

**Falsification ledger**: An isolated archive of `022f6abe`, using Python 3.13.13 at `/Users/kendal30/conda_envs/lhm/bin/python3.13`, passed six clean public-install controls. Six independent repeat-install probes crossed task/inventory with unknown identity, tab-suffixed closer and malformed region suffix. All returned 2 and preserved planning, inventory and lock bytes. These additional boundary cases did not rerun the implementation suite; no code mutations were performed.

**Bounding**: sufficient for this security pass. The committed wide verification names 340 passing mapped tests, three killed public-path mutants, clean candidate state and standing gates; its expected read-only AST drift remains explicitly separate from functional acceptance. F1/F2 responses add the missing matrix and recovery direction without expanding trust authority.

**Covered**: committed parser, callers, write ordering, refusal probes and verification record. **Not covered**: arbitrary owner rewriting, concurrent replacement, full-tree certification, re-anchor or independent repetition of implementation checks. **Elapsed**: about 5 minutes. **Tokens**: unknown.
