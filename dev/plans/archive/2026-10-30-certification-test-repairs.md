# Plan: Repair certification test measurements

**Source proposal**: dev/proposals/archive/2026-10-30-codex-certification-test-repairs.md
**Status**: archived
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Restore five certification test measurements while retaining their adversarial controls.

## Source proposal

The accepted proposal repairs two incomplete confidentiality fixtures, one moved-plan test path, and import contamination from a real ceremony boot. It preserves the real dispatcher and ceremony assertions, production guards, and current manifest authority. Its test-file changes require the separate frozen-file ceremony; this plan neither updates a live anchor nor compares a historic one.

## Scope

Edit only `bootstrap/tests/test_security_finding_confidentiality.py`, `bootstrap/tests/test_repin.py`, and `bootstrap/tests/test_repin_ceremony.py` unless a reviewed plan correction identifies another necessary test surface. Supply the existing lockfile contract's `src` and `verbatim` fields in both hand-built dispatcher records, point the baseline test at `dev/plans/archive/2026-10-29-forward-trust-baseline.md`, and isolate the real `REPIN.boot` scenario so checked module imports cannot alter later test identities. First reproduce ceremony-then-reanchor order dependence on an isolated copy; choose subprocess isolation or a complete in-process restoration based on that evidence. Keep both committed-object record checks around the worktree rewrite. Do not change production guards, manifest hashes, protection classification, or refs.

**Reuse.** Reuse the existing real dispatcher install, baseline preparation and scratch ceremony helpers. Searches for `install_dispatcher`, `REPIN.boot`, and the named failing nodes found their owning tests and `scripts/repin.py`; no new production helper is planned.

### Documentation / doctrine surface

No doctrine or adopter-facing documentation surface. This plan is deliberation in `dev/`.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Reproduce the ordered failure and correct fixture records and archived path | Both plan reviews | Two test-file repairs and reproduction evidence |
| C2 | Isolate the real boot, then exercise positive and adversarial cases in both orders | C1 evidence | Ceremony test repair and focused checks |

## Acceptance criteria

C1: Both aggregate-report nodes reach the real dispatcher child and distinguish pristine output from the planted renderer leak, retaining exact runner hashes and child-launch assertions. The baseline node packages independently bound evidence from the archived plan and retains its credential sentinel and missing/substituted evidence refusals. The pre-repair ordered run documents the suspected interaction or identifies a different cause before C2 is chosen.

C2: The ceremony test still accepts committed records before and after a worktree rewrite. Each of `test_authority_pin_reads_v2_frozen_entry_digest` and `test_rostered_stage_b_executes_only_preflight_bytes_pinned_by_p` passes alone, immediately after the ceremony node, and in the reverse order. Bad authority digests still refuse and planted candidate preflight bytes do not execute. An unmutated control passes; the existing leaking renderer remains observable. The changed frozen files retain their separate baseline and re-anchor obligation, without a live ref update here.

## Scope delta

**Scope delta**: preserved

## Verification

Boundary A: use canonical Python 3.13.x on an isolated copy. Run `python -m pytest bootstrap/tests/test_security_finding_confidentiality.py::TestTheDispatcherAggregateReportIsANewSweptSink` for both dispatcher legs; `python -m pytest bootstrap/tests/test_repin.py::test_baseline_preparation_builds_exact_package_after_reader_binding bootstrap/tests/test_repin.py::test_baseline_preparation_requires_independent_inputs bootstrap/tests/test_repin.py::test_baseline_preparation_refuses_substituted_external_roster_before_collection` for bound evidence and refusals; and the three named ceremony/reanchor nodes alone and in both ordered selections using `--quality-gate-shuffle-seed=0` only where it preserves the requested order. If the shuffle changes order, use explicit node invocations with the shuffle plugin disabled and record collected order. Search for other consumers and byte pins of all three changed files; run the focused `bootstrap/tests/test_gate_manifest.py::test_verify_holds_on_frozen_file_modification` control during iteration and include owning manifest and security tests in the final map. Run `python scripts/claim_check.py` on changed prose, `python scripts/check_cairn.py`, `python scripts/link_check.py`, `python scripts/sync_doc_snippets.py --check` if its interface supports that flag, and `python scripts/quality_gate.py --sub neutrality --sub redundancy` as applicable standing gates; record any inapplicable gate and why. Preserve the current manifest's expected refusal as evidence of the separate ceremony, not as a passing test.

Boundary B: **wide**, because pinned security tests are a trust-ceremony surface. On the final clean unchanged implementation commit under canonical Python 3.13.x, run the reviewed owning families, ordered sequences, adversarial controls, manifest/security checks and standing gates, splitting selections at guard limits and reconciling the union. Record SHA/range, touched surfaces, interpreter, clean pre/post state, exact commands and counts, elapsed time, tokens or unknown, non-pass dispositions, omissions, and `Certified by: pending`. A known unmet check keeps work open. Boundary C is an independent code review with targeted falsification and a bounding verdict. Full-tree certification and re-anchor remain separately authorized ceremonies.

## Plan review -- Codex GPT-6 Internal Reviewer -- 2026-10-30

```
Reviewed commit: 172a1c6f1e73135aa34a65ff3d9e81100602cb2d
Target: opening plan, against accepted proposal and current test paths
Prior findings: none
Assurance path: high-assurance
Elapsed: about 8 minutes
Tokens: unknown
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: ACCEPT

**Foundations**

1. **Should this happen as framed?** Yes. The plan preserves all four accepted repair outcomes and the real dispatcher, record, digest and Stage B controls; it orders reproduction before choosing isolation. -- accepted proposal `## Current contract`; plan C1/C2; `bootstrap/tests/test_repin_ceremony.py:1841`.
2. **Best alternative.** Keep the repair within the three named test files, using the existing boot and dispatcher apparatus; a production or manifest edit would add authority the Decision did not grant. -- plan Scope; `bootstrap/tests/test_security_finding_confidentiality.py:1469`; `bootstrap/tests/fixtures/gate_manifest.json`.
3. **What would show it wrong.** An ordered failure after isolation, a leak that passes, bad digest accepted, candidate preflight executed, or a record check lost after the rewrite would defeat C1/C2. -- plan Acceptance criteria; `bootstrap/tests/test_gate_reanchor.py:246`; `bootstrap/tests/test_gate_reanchor.py:280`.

The mapping names the confidentiality class, three baseline nodes, ceremony node and two reanchor nodes, including both orders and standalone controls. The author should record the exact collected order when shuffle is disabled and use the smallest owning manifest selection during iteration; the planned wide final check still owes the frozen-file consequence. This is a speed recommendation, not a removed criterion.

**Covered:** claims and accepted scope (proposal contract, plan Scope); real entry points and design (dispatcher and `REPIN.boot` above); failure controls (C1/C2 and reanchor nodes); cross-document fit and drift (archived-plan path, manifest); lifecycle and satisfier (separate ceremony, Boundary A/B/C). **Not covered / low confidence:** no tests, mutation or full certification run; the suspected import interaction and effective isolation remain to be measured. This pass does not clear Internal Security Review.

## Plan review -- Codex Security (GPT-6) -- 2026-10-30

```
Reviewed commit: c71a586c
Target: plan and usual plan review against accepted proposal
Prior findings: none
Elapsed: about 2 minutes
Tokens: unknown
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none
**Verdict**: ACCEPT

**Foundations**

1. **Should this happen as framed?** Yes. The plan restores reachability of the real dispatcher and preserves the leak, independent evidence, bad-pin and candidate-execution controls. The real fixture omits the required record fields (`bootstrap/tests/test_security_finding_confidentiality.py::install_dispatcher`); the plan's C1/C2 require the security outcomes.
2. **Best alternative.** A child process for the real boot gives checked imports a contained lifetime while retaining both committed-object checks (`bootstrap/tests/test_repin_ceremony.py::test_record_check_uses_committed_objects_after_worktree_rewrite`). The plan correctly permits another complete isolation after reproducing the failure.
3. **What would show it wrong?** An undetected planted leak, accepted bad authority digest, executed candidate preflight, lost post-rewrite check, or order dependence after repair would falsify it (`bootstrap/tests/test_gate_reanchor.py::test_authority_pin_reads_v2_frozen_entry_digest` and `::test_rostered_stage_b_executes_only_preflight_bytes_pinned_by_p`; plan C1/C2).

The separate frozen-file consequence is accurately retained without making repinning or re-anchoring a prerequisite. The mapped wide verification includes owning security and manifest checks, with expected refusal recorded rather than misrepresented as a pass. Use focused selections and reconcile their union to respect guard limits and avoid unnecessary runtime.

**Covered:** input and failure direction (dispatcher fixture and C1); real entry points and trust boundaries (ceremony and reanchor nodes above); alternatives and completeness (Scope and C2); drift and lifecycle (accepted proposal Current contract and plan Verification); domain and satisfiers (no scientific change, C1/C2). **Not covered / low confidence:** no tests, mutation, independent reproduction, historical-anchor comparison, or full certification run; implementation isolation remains to be measured. This clears only the plan's Internal Security Review obligation.

## Response to plan review -- Codex (GPT-6.1 Sol) -- 2026-10-30

Both required reviews accepted with no findings. I accepted the ordinary review's focused-manifest advice in Boundary A; its exact-order recording was already required there. I accepted the Security Review's advice to keep selections focused and reconcile their union, while leaving the isolation mechanism conditional on the ordered reproduction. The wide final mapping and all C1/C2 outcomes remain. Elapsed time: about 3 minutes. Token use: unknown.

## Implementation verification -- Codex (GPT-6) -- 2026-10-30

```
Mode: wide
Certified by: pending
Implementation commit: f26b903d4308d6da7c9304ec2469e999cf984c4b
Code range: 5cdd39afe36d7c512ab3633a5925d6e7d280f292..f26b903d4308d6da7c9304ec2469e999cf984c4b
Interpreter: /Users/kendal30/conda_envs/lhm/bin/python3.13 -- Python 3.13.13
Verification copy: /private/tmp/cairn-cert-repair-final
Clean pre-state: `git status --short` empty at f26b903d
Clean post-state: `git status --short` empty at f26b903d after all mapped checks
Touched surfaces: the three test files named in Scope
Elapsed: about 29 minutes. Tokens: unknown.
```

**Focused checks.** On the clean verification copy, the dispatcher aggregate-report selection passed both pristine and planted-renderer cases (2 passed); the three baseline evidence/refusal nodes passed (3 passed); each of the ceremony record node, authority-pin node and Stage B node passed alone (3 passed); and the four explicit ordered pairs passed (8 passed). `--collect-only` confirmed each pair stayed in the requested order without a shuffle. The frozen-file modification control passed (1 passed). The real ceremony and both committed-object checks remain in the child process.

**Owning families.** `test_security_finding_confidentiality.py` passed 40; `test_security_verification.py` passed 136; `test_gate_reanchor.py` passed 17; `test_gate_manifest.py` passed 37; and `test_repin.py` passed 114. The complete `test_repin_ceremony.py` family passed 151 in 656.05 seconds with host access. Before that host run, its restricted-run attempt was interrupted at 47% after 432.91 seconds: 24 failed and 56 passed out of 151 collected; 71 nodes did not run. The first failure showed the scratch SSH signer rejecting the passphrase sent through the test pseudo-terminal. Under host access, `test_a_full_ceremony_signs_once_with_the_typed_passphrase` passed (1, 10.66 seconds) and `test_a_loaded_key_refuses_before_stage_one` passed (1, 11.64 seconds), followed by the full-family pass. This diagnoses the restricted-run non-pass as terminal delivery; the full required family is green under host access.

**Manifest consequence.** `test_gate_manifest.py::test_verify_holds_on_frozen_file_modification` passed as the focused refusal control. Direct `bootstrap/tests/_gate_manifest.py verify --target-repo . --no-collect` exited 1 with `HOLD — 130 gate-integrity violations`, including `FROZEN-MODIFIED` and `FROZEN-OID` for all three changed test files among existing candidate drift. No anchor was supplied to this diagnostic. This is the expected separate frozen-file/baseline consequence, recorded as a refusal rather than a passing test; no manifest, live ref or historical anchor was changed or compared.

**Standing gates.** `check_cairn.py` passed (199 Markdown files; 94 external links not probed); `link_check.py` passed (199 Markdown files; 95 external links not probed); `sync_doc_snippets.py --check` passed (476 documents, no drift); and `quality_gate.py --sub neutrality --sub redundancy` exited 0 with zero failures (43 neutrality information items and one redundancy information item). `claim_check.py` passed on this updated plan before commit.

**Omissions and disposition.** No full-tree suite, live ref update, re-anchor or historical-anchor comparison was run. The separate frozen-file ceremony remains at the Maintainer's version-cut/request point. The restricted terminal attempt was fully rerun under host access and the required owning family passed; no test failure remains open from that attempt. Boundary C remains for independent code review.

## Code review -- Codex (GPT-6.1 Sol) -- 2026-10-30

```
Reviewed implementation: f26b903d4308d6da7c9304ec2469e999cf984c4b
Boundary B record: 8d0a6caf
Tier: Internal; obligation: ordinary code review
Elapsed: about 13 minutes; tokens: unknown
```

**Verdict: REVISE.** One blocking finding. **Bounding: WIDER RUN REQUIRED** after repair: include the inherited-marker order case in new clean-commit Boundary B evidence.

**Foundations.** (1) Fixture fields and archived path match C1, but C2 isolation depends on ambient state (`test_security_finding_confidentiality.py:1492`, `test_repin.py:251`, `test_repin_ceremony.py:1847`). (2) Keep real boot in a child with a discriminator ambient environment alone cannot activate; retain both record checks (`test_repin_ceremony.py:1856-1862`). (3) Order failure, an undetected planted leak, or lost post-rewrite check would disprove the repair (plan C1/C2).

**P1 — inherited marker disables isolation.** `test_repin_ceremony.py:1847` treats `CAIRN_REPIN_RECORD_CHECK_CHILD=1` as proof of a spawned child. In a separate clone of f26b903d, ceremony→authority passed normally (2/2, Python 3.13.13). With that inherited variable set, ceremony passed in the outer process and authority failed on `trusted import package conflicts at _gate_manifest` (1 passed, 1 failed). C2 remains unmet. Ensure an inherited marker cannot bypass isolation; pass both orders with it set.

**Falsification ledger:** unmutated control, 2 passed; hostile environment probe, 1 passed/1 failed. No source mutant. `scripts/repin.py:1993-2037` reads extracted committed bytes; the child retains both calls.

**Coverage:** claims and drift—f26b903d diff and Boundary B SHA/range; production path and failure direction—`REPIN.boot`, `check_record`, dispatcher fixture and planted-leak node; completeness and satisfier—inherited-marker probe; consistency, lifecycle and scope—proposal Current contract, plan C1/C2, frozen-file ceremony; scientific domain—none changed. **Not covered:** full suite, re-anchor, historical comparison, all owning families, or renderer/record-reader mutation. Separate code Security Review remains owed.

## Response to code review -- Codex (GPT-6) -- 2026-10-30

I removed the environment-selected child branch. The record test now always invokes a direct child process for the real `REPIN.boot` and both committed-object checks around the rewrite. The new adversarial test sets the former marker and asserts that the parent retains its `_gate_manifest` module and package attribute while the child performs the same checks. On the final commit, the new node and all four ceremony/reanchor orderings passed with `CAIRN_REPIN_RECORD_CHECK_CHILD=1`. The separate code Security Review remains the next review obligation; I did not request a second ordinary clearing pass. Elapsed: about 23 minutes. Tokens: unknown.

## Implementation verification -- Codex (GPT-6) -- 2026-10-30

```
Mode: wide
Certified by: pending
Implementation commit: 20b01625207d46171a95d42886936eeb2aa13378
Code range: 35d03e868b16bdc98aa4553c05550641127ae228..20b01625207d46171a95d42886936eeb2aa13378
Interpreter: /Users/kendal30/conda_envs/lhm/bin/python3.13 -- Python 3.13.13
Verification copy: /private/tmp/cairn-cert-repair-final-reviewfix
Verification branch: codex/verify-cert-repair-20b
Pre-run state: clean tree at 20b01625
Post-run state: clean tree at the same 20b01625
Touched surface: bootstrap/tests/test_repin_ceremony.py
Elapsed: about 23 minutes. Tokens: unknown.
```

The marker-on regression keeps the real boot and both record checks in the child while asserting that the parent package and `bootstrap.tests._gate_manifest` object are unchanged. All four two-node selections collected in the requested order without shuffling.

| Command | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---|
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q bootstrap/tests/test_security_finding_confidentiality.py::TestTheDispatcherAggregateReportIsANewSweptSink` | 0 | 2 passed: pristine and planted renderer | 0.25s | unknown |
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q bootstrap/tests/test_repin.py::test_baseline_preparation_builds_exact_package_after_reader_binding bootstrap/tests/test_repin.py::test_baseline_preparation_requires_independent_inputs bootstrap/tests/test_repin.py::test_baseline_preparation_refuses_substituted_external_roster_before_collection` | 0 | 3 passed after using an attached local verification branch | 33.79s | unknown |
| `CAIRN_REPIN_RECORD_CHECK_CHILD=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q bootstrap/tests/test_repin_ceremony.py::test_inherited_child_marker_does_not_bypass_record_check_isolation` | 0 | 1 passed | 1.41s | unknown |
| `CAIRN_REPIN_RECORD_CHECK_CHILD=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q bootstrap/tests/test_repin_ceremony.py::test_record_check_uses_committed_objects_after_worktree_rewrite` | 0 | 1 passed | 1.51s | unknown |
| `CAIRN_REPIN_RECORD_CHECK_CHILD=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q bootstrap/tests/test_gate_reanchor.py::test_authority_pin_reads_v2_frozen_entry_digest` | 0 | 1 passed | 0.21s | unknown |
| `CAIRN_REPIN_RECORD_CHECK_CHILD=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q bootstrap/tests/test_gate_reanchor.py::test_rostered_stage_b_executes_only_preflight_bytes_pinned_by_p` | 0 | 1 passed | 15.92s | unknown |
| (1) `CAIRN_REPIN_RECORD_CHECK_CHILD=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q bootstrap/tests/test_repin_ceremony.py::test_record_check_uses_committed_objects_after_worktree_rewrite bootstrap/tests/test_gate_reanchor.py::test_authority_pin_reads_v2_frozen_entry_digest`<br>(2) Same prefix, ceremony node then `bootstrap/tests/test_gate_reanchor.py::test_rostered_stage_b_executes_only_preflight_bytes_pinned_by_p`<br>(3) Same prefix, authority node then ceremony node<br>(4) Same prefix, Stage B node then ceremony node | 0 | 8 passed | 1.59s, 16.12s, 1.54s, 16.74s | unknown |
| Four corresponding `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest --collect-only -q` commands with marker and the same four explicit node pairs | 0 | 2 nodes each, collected in requested order | 0.04–0.05s each | unknown |
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q bootstrap/tests/test_gate_manifest.py::test_verify_holds_on_frozen_file_modification` | 0 | 1 passed | 4.14s | unknown |
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q bootstrap/tests/test_security_finding_confidentiality.py` (host access) | 0 | 40 passed | 20.02s | unknown |
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q bootstrap/tests/test_security_verification.py` (host access) | 0 | 136 passed | 5.07s | unknown |
| `PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q bootstrap/tests/test_gate_reanchor.py` | 0 | 17 passed | 29.12s | unknown |
| `PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q bootstrap/tests/test_gate_manifest.py` | 0 | 37 passed | 11.26s | unknown |
| `PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q bootstrap/tests/test_repin.py` | 0 | 114 passed | 151.11s | unknown |
| `PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q bootstrap/tests/test_repin_ceremony.py` (host access) | 0 | 152 passed | 637.61s | unknown |
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 bootstrap/tests/_gate_manifest.py verify --target-repo . --no-collect` | 1 | Expected HOLD: 130 integrity violations, including FROZEN-MODIFIED and FROZEN-OID for the changed ceremony file; no anchor supplied | 0.2s | unknown |
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py` | 0 | 196 Markdown files clean; 94 external links not probed | <1s | unknown |
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 scripts/link_check.py` | 0 | 196 Markdown files clean; 95 external links not probed | <1s | unknown |
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 scripts/sync_doc_snippets.py --check` | 0 | 477 docs, no drift | <1s | unknown |
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 scripts/quality_gate.py --sub neutrality --sub redundancy` | 0 | Zero failures; neutrality info 43, redundancy info 1 | <1s | unknown |

**Non-pass disposition.** The first baseline-family attempt used a detached temporary clone; its nested clone could not resolve `git symbolic-ref HEAD`. I attached a local branch at the same tested commit and reran the three baseline nodes successfully. The restricted attempts of the confidentiality and security-verification families were blocked by denied loopback binds (35 failed/5 passed and 1 failed/135 passed); both families passed in full with host access. The current-manifest refusal is the separate frozen-file/baseline consequence, not a passing test. `claim_check.py` passed on this updated plan before commit.

**Omissions.** No full-tree suite, live ref update, re-anchor or historical-anchor comparison was run. The separate frozen-file ceremony remains at the Maintainer's version-cut/request point. No test failure remains open from this implementation correction. The next holder is the separate code Security Review.

## Code Security Review -- Codex (GPT-6) -- 2026-10-30

```
Reviewed implementation: 20b01625207d46171a95d42886936eeb2aa13378
Earlier implementation: f26b903d4308d6da7c9304ec2469e999cf984c4b
Boundary B record: e1b604ab
Tier: Internal Security Review
Elapsed: about 5 minutes; tokens: unknown
```

**Verdict: ACCEPT. Bounding: bounded mapping sufficient. Findings: none.** The wide Boundary B mapping covers the changed trust-ceremony tests and their consumers; its recorded manifest HOLD remains a separate ceremony obligation, not a pass.

**Foundations.** (1) The repair should ship as framed: the dispatcher records now provide `src` and `verbatim`, and the real record checks run on either side of the rewrite (`test_security_finding_confidentiality.py:1492`, `test_repin_ceremony.py:1856-1860`). (2) A dedicated child contains checked imports without changing production guards; always launching it avoids the prior inherited-marker bypass (`test_repin_ceremony.py:1862-1887`). (3) A leak missed by the dispatcher, an accepted bad pin, or a post-rewrite check that is not reached would disprove the outcome (C1/C2 and `test_gate_reanchor.py::test_authority_pin_reads_v2_frozen_entry_digest`).

**Falsification ledger.** On an isolated copy of e1b604ab, Python 3.13.13: unmutated record-check node 1 passed. Total mutants: 1; killed: 1; survivors: 0; measured equivalents: 0. Replacing the second child `check_record` call with a deliberate exception made that node fail with the exception, demonstrating the post-rewrite position is reached and child failure propagates. This probe does not establish the semantics of `check_record` itself.

**Coverage:** claims and production path: implementation diff and `scripts/repin.py:1993`; completeness and fail-closed behavior: child return-code assertion and marker regression at `test_repin_ceremony.py:1868-1887`; cross-document consistency and reuse: plan Scope and searches for `install_dispatcher`, `REPIN.boot`, and `check_record`; drift and lifecycle: Boundary B at e1b604ab and separate manifest HOLD; domain and scope: three test files in the implementation diff, no scientific method changed; satisfier: C1/C2 and Boundary B mapped checks. **Not covered:** full suite, re-anchor, historic anchor comparison, independent renderer mutation, or rerunning the author's implementation checks.

## Dispositions -- archive preparation -- 2026-10-30

Dispositions: the separate frozen-file ceremony is deferred to the existing v0.6 forward-baseline work item; the plan explicitly assigns trust-anchor changes to that separate process, and `dev/PLANNING.md` > “Earlier frozen-test changes” now names these three changed files. Maintainer authorization on that board item: “They can each build the machinery, the new baseline does not need to be part of their plans. It can be a work board item for v0.6.” No other follow-up remains open.

**Evidence shipped**: repaired dispatcher records and archived-plan path (`f26b903d`); isolated real ceremony boot and inherited-marker adversarial regression (`20b01625`); wide final-commit results and focused controls (this plan's `Implementation verification`); ordinary and Security code reviews (`6d29c86e`, `544b873f`).

**Evidence deferred**: the full-tree certification run and frozen-file baseline ceremony were not run in this plan; both remain separate authorized v0.6 integration work.

**Deferred evidence home**: `dev/PLANNING.md` > “Establish the v0.6 forward baseline” and “Earlier frozen-test changes,” which now lists `bootstrap/tests/test_security_finding_confidentiality.py`, `bootstrap/tests/test_repin.py`, and `bootstrap/tests/test_repin_ceremony.py`.

**Fidelity sign-off**: implementation commits `f26b903d4308d6da7c9304ec2469e999cf984c4b` and `20b01625207d46171a95d42886936eeb2aa13378` deliver the accepted proposal's `## Current contract` as revised at Decision commit `322eafb5` (proposal archive, `2026-10-30-codex-certification-test-repairs.md`): fixture fields and archived path are repaired; real boot and both record checks remain isolated; refusal, adversarial and ordering controls remain. No accepted outcome was removed.
