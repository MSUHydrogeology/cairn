# Plan: Test trust boundary

**Source proposal**: dev/proposals/archive/2026-10-28-codex-test-trust-boundary.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-28
**In brief**: Protect the tests that defend trust while reporting ordinary test changes without requiring a new trust anchor.

## Source proposal

The Maintainer accepted the narrower boundary and its recorded assurance loss at `cca436a9`. The current blanket protection remains in force until a reviewed authority transition and Maintainer ceremony install the new boundary.

## Scope

Inventory and classify current tests and their dependencies; bind a protected roster to the signed anchor; change manifest production, independent static derivation, verification and both ceremony stages; test the real transition and steady state; update the runbook and high-risk rule. Retain existing script, shipped-module and fixture protection. Actual release skip, xfail and xpass outcomes still refuse.

**Reuse.** Search `bootstrap/tests/_gate_manifest.py` and `_gate_preflight.py` for `_frozen_files`, `produce`, `rederive_static_manifest` and reviewed transitions: these provide the existing collection, independent comparison and authority-closure path to extend. The runbook describes the ceremony. Do not replace its existing trust controls.

### Documentation / doctrine surface

`AGENTS.md` names protected tests and control machinery as high risk, without making ordinary tests high risk solely by location. `bootstrap/REANCHOR_RUNBOOK.md` describes the actual verifier and trigger. Governing text follows `docs/DOCUMENTATION_PLAN.md`. Changes to shared governing files wait until the model-floor and scoped-verification changes finish.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Inventory and classify | MAINTAINER-GATED: approve the exact initial classification before narrowing | Complete inventory and proposed roster in this plan's evidence folder |
| C2 | Implement and test | C1 approval; reviewed plan | Roster authority, gate changes, tests and documentation |
| C3 | Independent code and security review | C2 committed and verified; before installation where current gates permit | Reviews and dispositions |
| C4 | Install initial authority | MAINTAINER-ONLY: existing reviewed transition and re-anchor/root approval | Signed anchor and ceremony evidence |
| C5 | Prove steady state and close | C4; any required additional ceremony | Transition evidence, verification and archive |

## Acceptance criteria

### C1 — inventory

Enumerate every current Python test, controlling helper, import and fixture from the current tree and actual dependency paths, with reasons for each protected or ordinary classification. The floor includes all entries currently in `bootstrap/tests/security_manifest.py` and the ten additional tests named in the accepted contract; do not assume historical counts are complete. Include controlling `conftest.py`, `__init__.py`, `security_manifest.py`, `_ast_attest.py`, `_loader_proto.py`, current `_gate_*.py` and `_oracle*.py`, and gate/AST fixtures. Inventory existing protected scripts, shipped modules and fixture patterns. Record the exact proposed roster and dependencies in a plan-owned evidence folder. The Maintainer approves the precise initial classification before narrowing; a new protected helper is frozen and, if it decides ceremony, joins authority closure.

### C2 — design and tests

The reviewed first transition binds initial roster bytes; thereafter the trusted previous signed anchor supplies membership. Stage 1 passes that roster to candidate `produce`; trusted `rederive_static_manifest` independently checks identities against raw candidate bytes; stage 2 rebuilds the same roster and manifest. Candidate output cannot shrink membership. Missing or malformed roster, membership mismatch, collection failure or invalid authority refuses. Protected byte edits, node loss/rename and new skip/xfail markers HOLD. Ordinary edits, additions, deletions, renames and marker changes are visible nonblocking notes; a new unrostered `test_*.py` emits `UNPROTECTED-NEW` with path and nodes. A new trust test remains unprotected until reviewed roster admission and re-anchor. Preserve the full collection census and release refusal of actual skip/xfail/xpass.

### C3 — challenge

Use real `produce` → `verify` → stage 1 → stage 2 tests for new ordinary and protective files, protected losses, roster tampering and ordinary changes; demonstrate an ordinary edit's existing lifecycle lane. Prove one existing reviewed transition first. Only a measured old-checker refusal of a specific comparison permits the compatibility bridge and second reviewed transition; record that failure and extra ceremony cost, without weakening old-anchor checks. Independent code and Security Reviews challenge the evidence and remaining execution-influence risk.

### C4–C5 — authority and steady state

The Maintainer alone authorizes and performs the applicable root and re-anchor ceremony under the existing runbook. Show the initial transition and a later steady-state run against the signed roster. No claim that the new boundary is active precedes installation. The ordinary-test pilot remains blocked until the delivered roster excludes its board test file. If neither transition route preserves old-anchor checks, stop for repair; do not waive the ceremony.

## Scope delta

**Scope delta**: preserved against the accepted contract. The accepted proposal already records the loss of blanket ordinary-test byte protection and HOLDs on ordinary node and marker changes. Ordinary code can influence protected collection or execution; the new boundary is not equivalent tamper resistance.

## Verification

Boundary A uses the owning families `bootstrap/tests/test_gate_manifest.py`, `test_gate_transition.py`, `test_gate_preflight.py`, `test_reanchor_driver_disclosures.py`, `test_repin.py`, `test_repin_ceremony.py` and `test_security_marker.py`, plus tests found by tracing changed imports and fixtures. Add targeted real-path and release-outcome probes for the criteria above. Run applicable claim, link, snippet and neutrality gates for changed prose; trace each check to its trigger. Record S2 mutations and S3's actual Maintainer-run verifier command in the implementation evidence.

Boundary B is **full** because gate manifest and trust ceremony surfaces change. After the final implementation commit, run the scoped mapping and standing gates on a clean unchanged tree under `/Users/kendal30/conda_envs/lhm/bin/python3.13`; record commit, range, pre/post state, commands, counts, timing, non-pass dispositions and omissions. Set **Certified by**: pending until the next authorized certifying run supplies the full suite and quality pair. Reviewers independently falsify the recorded claims; they do not run the full suite. The installed boundary and actual ceremony remain contingent on C4.
