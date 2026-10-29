# Plan: Forward trust baseline machinery

**Source proposal**: dev/proposals/archive/2026-10-29-codex-forward-trust-baseline.md
**Status**: revising-code
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Build and test a reusable way to establish a reviewed starting point for future trust checks.

## Source proposal

The Maintainer accepted the revised contract and grouped historical loss. Build and independently review the machinery before separate v0.6 installation; existing protections remain active until then.

## Scope

Implement a no-signed-predecessor ceremony. The approved roster is `dev/plans/archive/2026-10-28-test-trust-boundary/c1b-proposed-roster.json`: 78 test files and 12 controlling Python modules, plus protected scripts, modules and fixtures. Preserve signed-prior authentication and comparisons. `dev/PLANNING.md` carries real installation. No real ref move, signing, push or historical comparison is authorized here.

**Reuse.** `scripts/repin.py` provides extraction, preparation and ceremony; `bootstrap/tests/_gate_preflight.py` independently derives static fields and `bootstrap/tests/_gate_reanchor.py` checks authority and refs. Extend these where suitable; trace changed imports and callers.

### Documentation / doctrine surface

Update `bootstrap/REANCHOR_RUNBOOK.md`; route prescriptions under `docs/DOCUMENTATION_PLAN.md`. At archive, ensure the board item retains pre-reanchor certification and `python bootstrap/security_check.py` at the clean release commit with required tools and no skip, xfail or xpass.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Define and implement candidate preparation and package | Plan reviews | Extraction, independent roster/static derivation, preparation and reader binding |
| C2 | Implement installation and forward verification | C1 | Refusal checks, signed commit and atomic ref transaction; scratch demonstrations |
| C2b | Prove refusal and future protection | C2 | Scratch controls and signed-prior behavior |
| C3 | Document and verify | C2b | Operator instructions, scoped evidence, independent code and Security Reviews |
| C4 | Actual baseline installation | MAINTAINER-ONLY: separate exact candidate, package and signer authorization | Separate v0.6 board item, not a prerequisite for this plan's archive |

## Acceptance criteria

**C1.** Add an explicit baseline preparation mode to `scripts/repin.py` `main`, using `extract`, `build_packet` and `check_record`; it never follows from failure of ordinary authentication. Extract the clean committed candidate from Git objects; check containment and membership; collect without signing credentials. Bind the independently supplied approved roster, candidate, manifest, collection, interpreter, tool hashes and reader record. Determine required AST/lockfile preparation using existing transaction checks: an implementer prepares and commits any required changes, an independent reviewer reviews them before final candidate/package review, and missing preparation refuses. Independently derive static fields; candidate-controlled expectations cannot authorize its roster.

**C2.** Add an explicit baseline installation mode to `scripts/repin.py` `main` / `run_ceremony`, retaining checked-module loading and off-list-import refusal. An independently reviewed reader record binds the launcher, installer and complete imported execution closure. Before invoking installation with signing credentials, the Maintainer compares that record, the independently approved roster and package against the exact candidate and independently supplies and authorizes the signer fingerprint; the installation entry point checks those inputs and executing bytes before signing or ref updates. Missing, malformed or mismatched independent inputs refuse. Ordinary prior-authentication failure never selects baseline mode or unsigned `--first-run`; valid ordinary signed-prior operation remains intact. Installation rechecks candidate and package, runs no candidate tests, signs once, verifies candidate parent and manifest-only change, records old anchor ID without comparison, and atomically updates both refs against observed values. 

**C2b.** Scratch public-path controls demonstrate refusal of roster substitution, missing preparation, changed executing code, wrong signer, stale reader/package, missing or invalid prior authentication without explicit baseline mode, missing independent inputs and either stale ref, with neither ref moved on refusal. Admission requires all independent inputs. Malicious paths and symlinks, changed or extra extraction files refuse; an installation candidate-test sentinel never executes. A disposable anchor demonstrates subsequent protected byte/node loss and new-marker HOLDs; ordinary changes yield notes, unrostered tests notice, and full collection and release outcome refusal remain intact. New protected tests require reviewed admission.

**C3.** Document operator commands, checks, limitations and independent inputs. Record controls, mutations and omissions. Ordinary and Security code reviews challenge controls and public paths. Archive does not claim installation.

**C4.** The Maintainer authorizes and performs installation for the exact candidate, package and signer after certification. C4 is separate; release security remains required.

## Scope delta

**Scope delta**: preserved. The source Decision permits the grouped historical losses; the separate board item carries real installation and its release dependency.

## Verification

Boundary A and B use canonical Python 3.13. Run the following focused owning files with `python -m pytest <file ...>` in guard-compliant batches, reconciling their union; add public-mode tests in the named files:

- `bootstrap/tests/test_repin.py` and `bootstrap/tests/test_repin_ceremony.py`: preparation and installation entry points, checked loading/off-list imports, containment and membership including malicious paths, symlinks and changed or extra extracted files; an installation sentinel proves candidate tests do not run.
- `bootstrap/tests/test_gate_preflight.py` and `bootstrap/tests/test_gate_transition.py`: independently supplied roster, static derivation, authority closure, ordinary signed-prior success and refusal without valid prior authority or explicit baseline selection.
- `bootstrap/tests/test_gate_reanchor.py`, `bootstrap/tests/test_reanchor.py` and `bootstrap/tests/test_reanchor_driver_disclosures.py`: reader and executing-code binding, independent signer, stale package and each ref, atomic no-move refusal, manifest-only signed parent, and later signed-prior comparisons. Add missing preparation and input refusal tests here or in the public ceremony family.
- `bootstrap/tests/test_gate_manifest.py`: protected bytes, nodes and markers, ordinary notes, unrostered notice and full collection; `bootstrap/tests/test_security_check.py` and `bootstrap/tests/test_security_marker.py`: release skip, xfail and xpass refusal.

Use disposable repositories for public preparation, installation and subsequent protected-loss checks; record each mutation and its passing control. Add discovered callers and fixtures to the implementation record. Run `python scripts/claim_check.py <changed-document>` for claims, `python scripts/check_cairn.py` for prose and internal links, `python scripts/link_check.py` for cross references, `python scripts/sync_doc_snippets.py --check` for snippet drift, and `python scripts/quality_gate.py --sub neutrality --sub redundancy` for prose neutrality and duplication; confirm each command's supported arguments before use. Record omissions and non-passes.
Boundary B is **wide** for this trust ceremony: run the mapping on the final clean commit; record SHA, range, interpreter, pre/post state, timings, outcomes, omissions and `Certified by: pending`. A missing required check keeps the work open. The separate installation item retains certification. Boundary C belongs to independent reviewers, who falsify the claims and assess the mapping without running the full suite.

## Plan review -- Codex (gpt-6.1-sol) -- 2026-10-29

```
Reviewed commit: 58e22babfe4b06988ce270010e47c03b7fc0e2a3
Target: opening plan, scope, sequence, acceptance criteria and verification
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** The sequence preserves separate Maintainer-only installation and future comparisons, but its verification map is not yet reviewable. -- Source proposal / Current contract; plan C1–C4 and Verification.
2. **Best alternative.** Extend existing ceremony paths with a narrowly selected baseline mode; preserve signed-prior checks rather than building a parallel ceremony. -- `scripts/repin.py` (`build_packet`, `run_ceremony`); `bootstrap/tests/_gate_reanchor.py` (`promote_data_only`).
3. **What would show it wrong?** A substituted roster or stale authority admitted through the public path, or a protected loss missed after installation, would defeat the accepted forward guarantee. -- plan C1–C2.

**F1 — Blocking: make the verification mapping reviewable before implementation.** Verification lists families and says to map changed callers and exact nodes before implementation, but does not map the stated invariants and public paths to checks, name commands and their properties, or identify standing gates. The plan template requires that mapping to be reviewed before implementation; a later implementer-created map cannot receive this plan review. Name the existing relevant nodes or files against each behavior and public path, the intended new checks where none exists, and concrete applicable gate commands and properties. Keep the scope focused on affected behavior and prescribed ceremony checks; do not substitute a full suite. -- `dev/plans/_template.md`, Verification; plan C1–C3 and Verification.

**F2 — Blocking: identify the installation execution path and its binding trigger.** C2 requires the launcher, installer and complete imported closure to be bound and compared, but names neither the proposed entry points nor where the independent reader record and approval are checked before execution and signing. This leaves the proposal review's accepted S1 and the security preflight's trigger unresolved at the point the plan is reviewed. Identify the intended existing entry points and how the independently reviewed closure and signer expectation reach the check, including any new mode or boundary whose exact implementation can be refined in code. -- proposal Response S1; `scripts/repin.py` (`run_ceremony`, `check_record`); `bootstrap/tests/_gate_reanchor.py` (`_verify_executing_authority_code`).

**Covered:** claims, completeness and refusal (lenses 1, 3, 4: plan C1–C2 and accepted Current contract); public paths (2: plan Verification and F1); reuse, consistency and drift (5, 6: named ceremony functions and runbook scope); lifecycle and scope (7, 8: C4 and proposal Decision); satisfiers (9: F1–F2). **Not covered / low confidence:** no execution, mutations, signing or ref changes; closure feasibility and host containment remain for implementation and Security Review. This pass clears only the ordinary plan-review obligation.


## Plan review -- Codex (gpt-6.1-sol), Security reviewer -- 2026-10-29

```
Reviewed commit: 5c42b8cb5584629f8a9eefec026503a6defeb42a
Target: operative plan, accepted source contract, ordinary plan review
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** The plan preserves the accepted forward guarantee and separate installation authority, but leaves the bootstrap authority trigger unspecified; implementation must wait for that correction. -- plan C1–C4; source proposal Current contract and Response S1; ordinary review F2.
2. **Best alternative.** Add an explicit baseline mode within the existing ceremony, with independently approved authority inputs and unchanged ordinary signed-prior checks. Reuse object extraction and the atomic transaction rather than weakening the existing first-run path. -- `scripts/repin.py`, `extract`, `run_ceremony`; `bootstrap/tests/_gate_preflight.py`, `check`.
3. **What would show it wrong?** An ordinary invocation obtaining baseline authority after prior authentication fails, a candidate choosing its own reader/signer expectations, or substituted executing code reaching signing defeats the accepted separation. -- source proposal security preflight S1–S4; `scripts/repin.py`, `check_record`, `run_ceremony`.

**S1 — Blocking: specify the independent authority and mode boundary.** Ordinary F2 correctly identifies the missing execution path. Make its security requirements concrete in the operative cells: name the planned preparation/installation entry points and explicit mode; identify where independent roster, reader record, reviewed closure and signer expectation enter, and who compares/authorizes them before execution with signing credentials. A digest in a candidate-generated package is consistency evidence, not independent permission. State that missing, malformed or mismatched independent inputs refuse and that ordinary authentication failure never selects baseline mode or the existing unsigned `--first-run` route. Add public-path controls for valid ordinary signed-prior operation, invalid/missing prior authentication without explicit baseline selection, and baseline admission only with the independent inputs; show neither ref moves on refusal. This closes accepted preflight S3–S4 without requiring historical comparison. -- `scripts/repin.py`, `check_record`, `run_ceremony`, `main`; source proposal Response S1 and Current contract.

**S2 — Blocking: retain extraction and execution-boundary checks in the mapping.** Ordinary F1's mapping must include the new mode's containment/membership and no-candidate-execution promises, not only package substitutions. Name public-path tests for malicious tracked paths/symlinks, changed or extra extracted files, and an installation candidate-test sentinel that must never execute. Preserve existing checked-module loading and off-list-import refusal on any reused boot path. Existing extraction tests establish useful owners, but do not establish the new mode reaches those controls. This asks for file containment and phase separation, not host isolation: hostile collection remains an acknowledged risk. -- `scripts/repin.py`, `extract`, `run_ceremony`; `bootstrap/tests/test_repin.py`, `test_a_tracked_symlink_or_submodule_refuses_before_import`, `test_an_unusable_tracked_path_refuses_and_writes_nothing_outside_the_extraction`, `test_a_loaded_local_module_outside_the_list_refuses`.

**Covered:** claims, public paths, completeness and refusal (lenses 1–4: S1–S2 and committed functions above); reuse, consistency and drift (5–6: extraction, reader record, first-run handling and source contract); lifecycle/scope (7–8: C4 and accepted grouped historical loss); satisfiers (9: concrete cell and test additions in S1–S2). **Not covered / low confidence:** design inspection only; no execution, mutations, signing, ref changes or host-isolation proof. No historic-anchor comparison or broad run is requested. This records the Security plan-review pass; findings require author disposition before implementation.


## Response to plan review -- Codex (gpt-6.1-sol) -- 2026-10-29

| Finding | Disposition |
|---|---|
| F1 | Accepted: Verification maps each invariant and public path to owning files, planned tests and gate commands. |
| F2 | Accepted: C1–C2 name the explicit entry points, independent inputs and pre-signing checks. |
| S1 | Accepted: C1–C2 specify selection, independent approval and refusal, including no fallback from ordinary authentication. |
| S2 | Accepted: C2 and Verification require public-path containment, checked loading, off-list refusal and a no-candidate-test sentinel. |

Both plan-review passes are recorded, including the Internal Security Review obligation. Their blocking findings are folded into the operative cells; implementation follows the single plan-review round. Host compromise and hostile collection remain limitations, not claims of containment.

## Author correction -- Codex -- 2026-10-29

The Scope line's `c1b-proposed-roster.json` path is stale: its own recorded status is proposed, and it predates the exact approval below. Use the Maintainer-approved `dev/plans/archive/2026-10-28-test-trust-boundary/c1b-roster-6cc95fa7.json`, committed at `884e6d53b4f6ff6329a1148dc49a32294628109f`, raw SHA-256 `188fa76d82744be571bdc7ca91a43d605776b9df5ba0ac729e2cf22af66b8cc4`. The approval is recorded in `dev/plans/archive/2026-10-28-test-trust-boundary.md`, `C1c roster approval`; its bytes match `bootstrap/tests/fixtures/protected_test_roster.json` and `_APPROVED_INITIAL_ROSTER_SHA256`. The roster itself is unchanged.


## Prerequisite Security Review -- Codex (gpt-6.1-sol) -- 2026-10-29

```
Reviewed commits: 26b12c92888b426170e529fb92f3a3a01af04b27 and e87c8d2d6fa1835dee5b6f62446bc17248d8d394
Target: C1 committed AST fixture preparation only
Prior findings: none
```

**Obligation**: C1 independent review of required preparation.
**Findings**: none within this preparation boundary.

**Foundations**

1. **Does it do what it claims?** Both commits contain exactly the two fixture outputs generated by the existing baseline transaction from their respective committed parents; neither changes engine, lockfile, authority code or refs. -- `git show` on the two reviewed commits; `scripts/repin.py`, `build_transaction`.
2. **Best alternative.** Keep the existing transaction and preserve the baseline's key set rather than regenerate the baseline. These commits already take that path. -- `scripts/repin.py`, `build_transaction`, `render_changes`.
3. **What would show it wrong?** A hidden output, incomplete engine enumeration or a fixture alteration escaping the owed-preparation check would defeat this prerequisite. -- falsification ledger below.

**Falsification ledger.** Probes used canonical `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13), the transaction implementation at e87c8d2d, raw-object extraction of each preparation commit's parent, and fresh temporary folders outside the shared checkout. A detached checkout at e87c8d2d supplied the review code. No engine code was imported.

| Probe | Result |
|---|---|
| Enumerate the complete committed top-level engine module set, then derive each parent's transaction | 10 modules each; 26b12c92: 7 changed, 12 added, 1 rekeyed; e87c8d2d: 1 changed, 0 added, 1 rekeyed. Both: 0 missing, duplicate or dropped keys; 169 baseline keys. |
| Compare generated output paths and exact bytes against each commit's full changed-path set | Both commits match exactly; only the two AST fixtures, with no lockfile output owed. |
| Substitute the committed prepared fixture bytes into each isolated extraction and derive again | Passing controls: both yield no transaction. |
| Corrupt the final install_onboarding baseline digest in the isolated extraction | Detected: preparation becomes owed again. |
| Remove the final _reconcile_generated_blocks known-new entry in the isolated extraction | Detected: preparation becomes owed again. |

**Bounding**: ACCEPTED for C1 fixture preparation only. This does not clear final code or Security Review, independently approve the reader closure, authorize installation, or certify the tree.

**Covered:** claims, completeness, drift and reuse (lenses 1, 3, 5, 6: exact output comparison and existing transaction); fail-closed behavior (4: two perturbations against passing controls); lifecycle and scope (7, 8: C1 preparation remains separate from C4); satisfier (9: no finding). **Not covered / low confidence:** public installation/preparation integration (2), semantic re-review of the underlying engine changes, final reader/package authority, historical reconciliation and real installation. No signing, anchor movement, full suite or broad suite was run. Final implementation verification and the plan's ordinary and Security code reviews remain open.

## Implementation verification -- Codex (gpt-6.1-sol) -- 2026-10-29

**Boundary B mode**: wide
**Certified by**: pending

**Tested commit**: `dccaf4e6b43b63ce98577307065464214a5d754e`
**Range**: `1867e666..dccaf4e6b43b63ce98577307065464214a5d754e`
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` -- Python 3.13.13
**Clean pre/post state**: detached worktree at the tested commit had no status output before or after mapped tests; the implementation checkout retained only unrelated untracked `.claude/` and `dev/measurement/collision_log.md` files.

The reviewed map covers the baseline preparation and installation public paths, ordinary signed-prior and refusal behavior, extraction and checked loading, stale inputs and atomic ref refusal, post-install protected bytes/nodes/markers, ordinary notes and unrostered notices, and release skip/xfail/xpass outcomes. Commands ran against the clean detached worktree with `PYTHONDONTWRITEBYTECODE=1`; scratch repositories and keys only:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_repin.py -q
PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest --lf bootstrap/tests/test_repin_ceremony.py -q
PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_repin_ceremony.py -q  # dynamically deselect first 37 already-run nodes
PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_gate_preflight.py bootstrap/tests/test_gate_transition.py bootstrap/tests/test_gate_reanchor.py bootstrap/tests/test_reanchor.py bootstrap/tests/test_reanchor_driver_disclosures.py bootstrap/tests/test_gate_manifest.py bootstrap/tests/test_security_check.py bootstrap/tests/test_security_marker.py -q
```

The 109 `test_repin.py` nodes passed (119.93s). The ceremony family had 151 nodes: 31 passed in the first mapped attempt, six scratch signing cases initially failed because the regular sandbox could not deliver the PTY passphrase to `ssh-keygen`, then all six passed under approved host execution (one representative node and the other five with `--lf`); the remaining 114 passed with the first 37 nodes deselected (404.08s). The eight remaining mapped files passed 766 nodes (305.07s). Total mapped outcomes: **1,026 passed**. The first sandbox attempt was interrupted after the six diagnosed failures; no unresolved test failure remains. The eight-file run emitted three existing `stevedore` deprecation warnings. No live key, live ref, push, historical-anchor comparison, candidate signing, or full suite was used.

The reader-input and runbook change also passed Python 3.13 `py_compile`; its focused public-path and credential-scrub nodes passed 2/2. `claim_check.py`, `check_cairn.py`, `link_check.py`, `sync_doc_snippets.py --check`, and the neutrality/redundancy quality gates passed for the changed runbook (0 failures; one unrelated redundancy information item). The separate C4 Maintainer-only installation remains unperformed.


## Code review -- Codex (gpt-6.1-sol) -- 2026-10-29

```
Reviewed commit: dccaf4e6b43b63ce98577307065464214a5d754e
Target: forward-baseline changes in 1867e666..dccaf4e6 and verification at e71cb267
Prior findings: none
```

**Findings**: raised

**Foundations**

1. **Does it do what it claims?** The explicit preparation and installation paths bind candidate, independent record and signer, but malformed reader input escapes the intended refusal path. -- `scripts/repin.py`, `baseline_prepare`; F1.
2. **Best alternative.** Keep the existing explicit modes and shared transaction; validate the reader's JSON type before inspecting fields. -- `scripts/repin.py`, `baseline_prepare` and `baseline_install`.
3. **What would show it wrong?** A malformed independent input that escapes the advertised refusal, or substituted roster accepted by preparation. -- falsification ledger below.

**F1 -- malformed reader JSON produces an unhandled traceback.** `baseline-prepare` calls `reader.get` without checking that parsed JSON is an object. A valid JSON array (`[]`) exits 1 with `AttributeError` and a traceback instead of the command's explicit malformed-input refusal and exit 2. The probe stopped before package creation; this is an operator-facing failure, not evidence of an authority bypass. Check the type before field access and cover non-object JSON through the public command. -- `scripts/repin.py`, `baseline_prepare`; probe below.

**Falsification ledger.** On a fresh detached checkout of dccaf4e6, canonical Python 3.13.13 ran the existing public preparation controls for a substituted roster and missing reader: 2 passed. A separate scratch test using the same public `bed.run` entry point supplied an approved roster and reader bytes `[]`: it failed its expected exit-2 assertion, reporting exit 1 and `AttributeError: 'list' object has no attribute 'get'`. No output package was reached. These are targeted checks, not the Boundary B replay; no live refs, signing, historical comparison or full suite were used.

**Bounding**: ACCEPTED for the recorded wide mapping, subject to F1 and change-specific verification of its repair. The record identifies the mapped families, interpreter, scratch signing disposition and omissions; the targeted malformed-input probe exposed a behavior the mapped passing results did not establish. C4 is a separately gated item, not reached in the reviewed range; the plan's verification preserves its separate certification.

**Covered:** claims, public path and refusal (lenses 1–4: preparation code and ledger); reuse and consistency (5–6: transaction and reader checks); lifecycle and scope (7–8: separate C4); satisfier (9: F1). **Not covered / low confidence:** independent signing and atomic-ref mutation tests, all extraction attacks, actual installation and host containment; the Security Review remains separate. The runbook's operator sequence was read, but no real ceremony was performed.


## Code review -- Codex (gpt-6.1-sol), Security reviewer -- 2026-10-29

```
Reviewed commit: dccaf4e6b43b63ce98577307065464214a5d754e
Target: forward-baseline changes in 1867e666..dccaf4e6; verification at e71cb267
Prior findings: none
```

**Obligation**: Security code review of C1–C3.
**Tier**: Internal Security Review
**Findings**: none additional to ordinary F1; this pass does not dispose F1.

**Foundations**

1. **Does it do what it claims?** The explicit installer checks independent reader/package agreement and signer identity before signing; checked extraction supplies its imports and the existing expected-old transaction updates both refs. The targeted adversarial run retained those refusals and successful installation. -- `scripts/repin.py`, `baseline_install`, `load_listed`; ledger below.
2. **Best alternative.** Retain the shared signing, constructed-commit verification and atomic-ref helpers; the baseline's separate explicit entry avoids weakening ordinary prior authentication. No simpler substitute preserves these boundaries. -- `scripts/repin.py`, `main`; `bootstrap/tests/_gate_preflight.py`, `_construct_signed_commit`, `verify_constructed`, `_advance_both_refs`.
3. **What would show it wrong?** A changed execution closure reaching signing without the independent reader's agreement, candidate parent-package execution at installation, or partial ref update would defeat the separation. -- falsification ledger below.

**Falsification ledger.** A fresh detached worktree at the reviewed commit supplied unchanged implementation bytes. Canonical Python 3.13.13 ran one augmented scratch harness, `python -m pytest bootstrap/tests/test_repin.py::test_baseline_preparation_builds_exact_package_after_reader_binding -q`: **1 passed, 27.78s**. Only the disposable test was augmented; scratch repositories, refs and generated keys were used.

| Surface / attempted break | Observed result |
|---|---|
| Add `../outside.py` or an absolute outside path to package tool hashes; recompute the independently confirmed package digest, leaving the reader unchanged | Both refused at reader binding; refs unchanged. A new package digest alone cannot authorize changed tools. |
| Commit a candidate `scripts` package initializer writing a marker, then clear the marker before installation | Successful public installation left the marker absent. Candidate-test credential sentinel also stayed absent. |
| Harness controls: wrong fingerprint, changed installer hidden from status, stale reader/package, symlinked inputs, missing reader, late anchor creation and stale branch | All retained refusal/no-move assertions; both ref-race controls left the competing writer's value intact. |
| Passing control: explicit installation, then protected byte/node/marker losses and ordinary added test | Manifest-only signed child and equal branch/anchor; losses HOLD, ordinary addition notices. |

An earlier bootstrap-parent initializer experiment made collection fail and preparation refused; a collection-only diagnostic identified an existing import assumption. It was replaced with the collecting scripts-parent case. The detached-source harness also needed an explicit scratch branch. These were probe setup corrections, not implementation failures.

**Bounding**: ACCEPTED for the recorded wide mapping, subject to ordinary F1 and its repair evidence. Static inspection traced approved-roster parsing, reader/tool closure binding and no ordinary-to-baseline fallback. C4 remains separately fenced; no Waiting line is owed for installation this range did not reach.

**Covered:** claims, public paths, completeness and refusal (lenses 1–4: ledger and installer); reuse, consistency and drift (5–6: shared helpers and `bootstrap/REANCHOR_RUNBOOK.md`, forward-baseline sequence); lifecycle/scope (7–8: explicit modes and separate C4); satisfier (9: no additional finding). **Not covered / low confidence:** host compromise, candidate collection containment, real installation, historical-anchor comparison, full-suite certification and exhaustive hostile-path permutations. Reader independence remains a human authorization boundary; hashes do not authenticate its author. No live key/ref, push or full test suite was used.

## Response to code review -- Codex (gpt-6.1-sol) -- 2026-10-29

F1: accepted. Commit `7287e628` checks that the reader record is a JSON object before reading its fields. Public-command tests cover an array, null, a string, a number and a boolean: each refuses with exit 2, without a traceback or package. The earlier wide verification predates this repair; the focused results below do not replace the plan's required final-commit verification. The plan remains in `revising-code` pending that evidence.

## Repair checks -- Codex (gpt-6.1-sol) -- 2026-10-29

At `9c9a4679ee0da6ffe66e37ac58384d4fab4a65ef`, containing repair `7287e628`, canonical `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13) ran:

| Command | Exit | Outcomes | Elapsed |
|---|---:|---|---:|
| `PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q bootstrap/tests/test_repin.py -k 'baseline_preparation_refuses_nonobject_reader_record or baseline_preparation_refuses_substituted_external_roster_before_collection or baseline_preparation_requires_independent_inputs'` | 0 | 7 passed, 107 deselected; no skips, xfails or xpasses | 1.60s |

Tracked files and HEAD were unchanged before and after; unrelated untracked `.claude/` and `dev/measurement/collision_log.md` were present throughout. These checks cover the changed refusal and two adjacent controls, not the plan's full wide mapping. No live refs, signing or full suite were used. **Certified by**: pending. The final-commit Boundary B record and its prescribed checks remain outstanding.
