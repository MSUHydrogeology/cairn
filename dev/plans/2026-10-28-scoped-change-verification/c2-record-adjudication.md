# C2 illustrative record and omission variants

**Plan**: [`../2026-10-28-scoped-change-verification.md`](../2026-10-28-scoped-change-verification.md)
**Purpose**: Give an independent reviewer concrete evidence to judge whether the record rule accepts complete evidence and keeps two incomplete records open. These are examples of the C1/C2 record contract, not a tree certification or a claim that the plan is ready to archive.

## Example A — complete scoped record

**Boundary B mode**: wide  
**Tested SHA**: `69b8bc7e4f86fd6c669fd765a1ffe7951e9e10d9`  
**Range**: `2ed8ddabc80c985ebc93171c7e628a7ec070459f..69b8bc7e4f86fd6c669fd765a1ffe7951e9e10d9`  
**Certified by**: pending  
**Copy and state**: detached worktree `/private/tmp/cairn-scope-worktree-69b8bc7e`; clean before and after; HEAD unchanged at tested SHA; `refs/cairn/gate-anchor` present at `443de20f81169fabe36c4ca3cc620206f7850254`.  
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` — Python 3.13.13.  
**Producer**: the source-derived reader search and 47-module collection/split, recorded with explicit module list, commands, timings, outcomes, and exact node-union comparison in [`c2-split-execution.md`](c2-split-execution.md).  
**Consumer**: `bootstrap/tests/test_review_and_verification_rules_ship.py::test_agents_md_carries_the_obligation`, exercising the shipped adopter-facing rule; it ran in the 47-module selection and in the focused rule selection.  
**Mandatory security check**: these three mapped nodes ran at the same SHA and interpreter: `bootstrap/tests/test_gate_preflight.py::TestCandidateCodeCannotSignFromStageOne::test_the_candidate_position_cannot_sign_through_a_live_agent`, `bootstrap/tests/test_gate_preflight.py::TestCandidateCodeCannotSignFromStageOne::test_the_same_key_signs_when_the_socket_is_present`, and `bootstrap/tests/test_security_verification.py::TestNoCapabilityContract::test_a_socket_opening_child_is_excluded_by_admission_not_blocked_at_runtime`; 3 passed in 0.61s with the required elevated local permissions.  
**Commands and outcomes**: original collection selected 47 explicit files and collected 2,700 nodes in 1.33s. Split 1: 2,129 passed and 3 environment-denied security checks in 234.85s. Split 2: 568 passed in 71.31s. Executed union: 2,700 unique IDs, zero missing/extra; normalized collected and executed lists share SHA-256 `56be3c2e7c2507e68c3faac1f93dd28f6f65946f1cb11cd291a6cb7f28ca3052`. The three environment-denied nodes passed in the same-SHA elevated rerun above. The five mapped broad-run guard nodes passed (5, 3.44s); documentation gates passed (check_cairn and link_check each 184 files with no issues; neutrality/redundancy zero failures); 13 claim checks passed.  
**Criteria**: mapped owning families, adopter consumer, cross-family selection, public paths, exact guard behavior, mandatory security nodes, and documentation gates were exercised. The >40 selection was split into invocations within the existing guard; no override, parser, selector, or marker change was used.  
**Omissions/status**: no whole-tree suite; `CAIRN_FULL_SUITE=1` was not set. `Certified by` remains pending. Frozen-file gate-manifest/re-anchor ceremony, independent C2 adjudication, and code review remain pending. No known mapped consumer or mandatory security check remains unrun.

## Example B — consumer omitted

**Command**:

```sh
python3.13 -m pytest -q bootstrap/tests/test_certifying_run_rule.py --tb=short
```

**Outcome**: 13 passed in 0.02s at the same tested SHA and interpreter.  
**Omitted consumer**: `bootstrap/tests/test_review_and_verification_rules_ship.py::test_agents_md_carries_the_obligation` was not selected. That is an adopter-facing consumer of the shipped rule and is explicitly mapped by the plan.  
**Disposition requested from reviewer**: decide whether the green producer/rule module alone is sufficient. The record contract says missing mapped consumer coverage keeps the work open.

## Example C — mandatory security check omitted

**Command**:

```sh
python3.13 -m pytest -q \
  bootstrap/tests/test_verification_boundaries.py \
  bootstrap/tests/test_certifying_run_rule.py \
  bootstrap/tests/test_review_and_verification_rules_ship.py \
  --tb=short
```

**Outcome**: 129 passed in 0.17s at the same tested SHA and interpreter.  
**Omitted mandatory security checks**: all three nodes listed in Example A were omitted. The result says nothing about the mandatory gate-preflight and no-capability obligations.  
**Disposition requested from reviewer**: decide whether this green focused run can close the record. The record contract says omitted mandatory security checks keep the work open.

## Independent adjudication — pending

**Reviewer name and model**: pending  
**Reviewed commit**: pending  
**Example A verdict**: pending  
**Example B verdict and missing check**: pending  
**Example C verdict and missing check**: pending  
**Coverage limit**: pending  

The independent reviewer must supply their own judgments. This file does not attribute or pre-fill a review on their behalf.
