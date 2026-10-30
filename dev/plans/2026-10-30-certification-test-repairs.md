# Plan: Repair certification test measurements

**Source proposal**: dev/proposals/archive/2026-10-30-codex-certification-test-repairs.md
**Status**: ready-to-implement
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
