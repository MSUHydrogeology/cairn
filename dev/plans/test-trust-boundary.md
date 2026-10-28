# Plan: Test trust boundary

**Source proposal**: dev/proposals/archive/2026-10-28-codex-test-trust-boundary.md
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-28
**In brief**: Protect the tests that defend trust while reporting ordinary test changes without requiring a new trust anchor.

## Source proposal

The Maintainer accepted the narrower boundary and its recorded assurance loss at `cca436a9`. Blanket protection remains in force until a reviewed authority transition and Maintainer ceremony install the new boundary.

## Scope

Inventory tests and dependencies; bind a protected roster to the signed anchor; change manifest production, independent derivation, verification and both ceremony stages; test transition and steady state; update the runbook and high-risk rule. Retain existing script, shipped-module and fixture byte protection. Actual release skip, xfail and xpass outcomes still refuse.

**Reuse.** Search `bootstrap/tests/_gate_manifest.py` and `_gate_preflight.py` for `_frozen_files`, `produce`, `rederive_static_manifest` and reviewed transitions: these provide the collection, independent comparison and authority-closure path to extend. 

### Documentation / doctrine surface

`AGENTS.md` names protected tests and control machinery as high risk, without making ordinary tests high risk solely by location. Governing text states that the re-anchor verifier freezes named security and trust tests, records full collection, and holds on lost or newly skipped protected nodes. `bootstrap/REANCHOR_RUNBOOK.md` describes the actual human-triggered launcher and its checks. Route by `docs/DOCUMENTATION_PLAN.md`. All source and governing writes wait for model-floor and scoped-verification code reviews to finish.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1a | Factual inventory | Reviewed plan | Current dependency evidence in a plan-owned folder |
| C1b | Security classification | C1a; high-tier security judgment | Proposed exact roster and reasons |
| C1c | Approve classification | MAINTAINER-GATED: approve exact initial roster before narrowing | Maintainer's decision on roster |
| C2 | Implement and test | C1c approval | Authority, gate changes, tests and documentation |
| C3 | Independent code and security review | C2 committed and verified; before installation where current gates permit | Reviews and dispositions |
| C4 | Install initial authority | MAINTAINER-ONLY: existing reviewed transition and re-anchor/root approval | Signed anchor and ceremony evidence |
| C5 | Prove steady state and close | C4; any required additional ceremony | Transition evidence, verification and archive |

## Acceptance criteria

### C1a — inventory

Enumerate every current Python test, controlling helper, import, dynamic loading path and fixture using current tree and actual dependency paths; identify existing protected scripts, shipped modules and fixture patterns. Include all current `bootstrap/tests/security_manifest.py` entries and the ten additional tests named in the accepted contract, not historical counts. Record evidence in a plan-owned folder.

### C1b–C1c — classify and approve

A high-tier agent proposes each protected or ordinary classification with reasons and roster. Include controlling `conftest.py`, `__init__.py`, `security_manifest.py`, `_ast_attest.py`, `_loader_proto.py`, current `_gate_*.py` and `_oracle*.py`, and gate/AST fixtures. The Maintainer approves the precise initial classification before narrowing. A new protected helper is frozen and, if it decides ceremony, joins authority closure; candidate labels cannot classify it.

### C2 — design and tests

Reviewed initial transition binds approved roster bytes; thereafter the trusted previous signed anchor supplies membership. Stage 1 passes it to candidate `produce`; trusted `rederive_static_manifest` checks identity against raw candidate bytes; stage 2 rebuilds the same roster and manifest. Preserve closure validation, static comparison and stage-2 manifest-byte equality. Missing/malformed roster or manifest, membership mismatch, collection error or invalid authority refuses. Protected bytes, node loss/rename and new skip/xfail markers HOLD. Ordinary edits, additions, deletions, renames and marker changes are visible nonblocking notes; new unrostered `test_*.py` emits `UNPROTECTED-NEW` with path and nodes. A new trust test stays unprotected until reviewed admission and re-anchor. Preserve full collection and actual release skip/xfail/xpass refusal.

### C3 — challenge

Real `produce` → `verify` → stage 1 → stage 2 tests prove approved first roster, prior-anchor steady state, candidate substitution refusal at each stage, and new ordinary and protective admission. Exercise separately protected and ordinary edits, additions, deletions, renames and new markers, plus missing/malformed inputs and collection errors; demonstrate an ordinary edit's lifecycle lane. Try one existing reviewed transition first. Only a measured old-checker refusal of a specific comparison permits the compatibility bridge and second transition; record failure and extra ceremony cost, without weakening old-anchor checks. Independent code and Security Reviews challenge evidence and execution-influence risk.

### C4–C5 — authority and steady state

The Maintainer alone authorizes and performs the applicable root and re-anchor ceremony under the existing runbook. Show initial transition and later steady state against the signed roster. No claim that the new boundary is active precedes installation. The ordinary-test pilot remains blocked until the delivered roster excludes its board test file. If neither route preserves old-anchor checks, stop for repair; do not waive ceremony.

## Scope delta

**Scope delta**: preserved against the accepted contract. The Decision accepted loss of blanket ordinary-test byte protection and HOLDs on ordinary node and marker changes. Ordinary code can influence protected collection or execution; this is not equivalent tamper resistance.

## Verification

Boundary A mapping: `bootstrap/tests/test_gate_manifest.py` owns produce/verify, protected and ordinary changes, roster/manifest refusal and collection errors; `test_gate_transition.py` and `test_gate_preflight.py` own authority closure, initial roster, static re-derivation, candidate substitution and transition; `test_gate_reanchor.py` owns real stage 1/stage 2, byte equality and steady state; `test_security_check.py` and `test_security_marker.py` own actual release skip/xfail/xpass refusal. Add cases in those families as needed. `test_reanchor_driver_disclosures.py`, `test_repin.py` and `test_repin_ceremony.py` cover ceremony surfaces; trace changed imports and fixtures for further owners. Run applicable claim, link, snippet, neutrality and prose-integrity gates. Trace the runbook's actual human-invoked launcher through functions and tests to protected HOLDs, full census and ordinary notes; do not claim the unused external verifier invocation runs.

Boundary B is **full** for gate manifest and trust ceremony surfaces. After the final implementation commit, run the scoped mapping and standing gates on a clean unchanged tree under `/Users/kendal30/conda_envs/lhm/bin/python3.13`; record commit, range, pre/post state, commands, counts, timing, non-pass dispositions and omissions. Set **Certified by**: pending until the next authorized certifying run supplies the full suite and quality pair. Reviewers independently falsify the evidence; they do not run the full suite.

## Plan review -- Codex (gpt-6.1-terra), Internal reviewer -- 2026-10-28

```
Reviewed commit: 1640a3595aec0d36e48e65de3d184aefb66b42d4
Target: opening plan, Source proposal through Verification
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** The plan follows the accepted narrower boundary, but its classification gate, verification mapping and governing-text criterion need clarification before it can reliably deliver it. -- plan C1, Verification and Documentation / doctrine surface; accepted proposal Complete current contract and S3.
2. **Best alternative.** Produce the inventory first, then gate narrowing on approval; use the existing reviewed transition first and the existing test families for a specific mapping. This keeps all accepted outcomes. -- plan Sequence and C3; `bootstrap/tests/test_gate_preflight.py:2111`; `bootstrap/tests/test_gate_reanchor.py`.
3. **What would show it wrong.** A real transition that cannot retain the old anchor's admission checks, a protected loss that passes, or ordinary maintenance still held after installation would defeat the plan. -- accepted proposal Complete current contract; `bootstrap/tests/_gate_preflight.py:3204`; `bootstrap/tests/_gate_manifest.py:671`.

**F1 -- Blocking: order the classification approval after its evidence exists.** C1 is itself marked Maintainer-gated to approve an exact classification, yet C1 is the chunk that produces the inventory and proposed roster. That makes the gate's input unavailable when the chunk starts. **Satisfier:** separate inventory and proposed classification from the approval fence, and put the fence after that evidence exists and before any narrowing; explicitly trace actual dependency paths including dynamic imports and fixtures. Retain the stated floors and give the Maintainer the precise classification to approve. -- plan Sequence and C1; `bootstrap/tests/test_gate_preflight.py:810`.

**F2 -- Blocking: map the accepted verification to owning paths.** Verification names several families and generic real-path and release probes, but does not map each invariant and public path to its test file or node. It omits the accepted proposal's named `test_gate_reanchor.py` and `test_security_check.py` from the listed families even though they own two-stage and actual release-outcome behavior. C3's broad “ordinary changes” also leaves the accepted separate edit, addition, deletion, rename and marker cases implicit. **Satisfier:** map the accepted cases and each stage to specific owning test files or nodes, including these families, and identify where new real-path cases will be added; retain the separate ordinary and protected cases and actual skip/xfail/xpass release probes. -- accepted proposal Tests required and Verification and withdrawal; `bootstrap/tests/test_gate_reanchor.py:94`; `bootstrap/tests/test_security_check.py:624`; plan C3 and Verification.

**F3 -- Blocking: carry the accepted governing statement.** The plan says the high-risk rule will name protected tests and machinery, but does not require the separate S3 statement describing what the re-anchor verifier freezes, records and holds. A correct roster rule alone would not satisfy that accepted documentation outcome. **Satisfier:** require that governing text convey the accepted S3 statement and that the runbook's actual human-triggered verifier invocation agrees. -- accepted proposal S3; plan Documentation / doctrine surface; `bootstrap/REANCHOR_RUNBOOK.md:173`.

**Coverage.** Covered claims and current behavior (#1: `bootstrap/tests/_gate_manifest.py:337`, `:402`, `:678`); production paths and refusal design (#2–4: `bootstrap/tests/_gate_preflight.py:1933`, `:2097`, `:3425`; `bootstrap/tests/conftest.py:421`); reuse, drift and lifecycle placement (#5–7: plan Reuse and Sequence; `bootstrap/REANCHOR_RUNBOOK.md:173`; `dev/plans/ordinary-test-maintenance.md` C1); accepted scope and satisfiers (#8–9: accepted proposal Complete current contract and findings above). Not covered: no test execution, complete dependency inventory, or future implementation; the separate Internal Security Review remains open.

## Plan review -- Codex (Sol, high), Internal Security reviewer -- 2026-10-28

```
Reviewed commit: 1640a3595aec0d36e48e65de3d184aefb66b42d4
Target: opening plan, Source proposal through Verification
Prior findings: none for this obligation
Assurance path: high-assurance
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** Yes, after the clarifications below. The accepted
   assurance loss is settled; the plan retains anchor-owned membership, independent
   derivation and Maintainer installation. -- Decision `cca436a9`; plan C2 and C4–C5;
   `bootstrap/tests/_gate_preflight.py:1933`.
2. **Best alternative.** Use the existing reviewed transition first; add the bridge only
   for a measured old-checker refusal. This preserves every accepted outcome with
   potentially one ceremony. -- plan C3; `bootstrap/tests/test_gate_preflight.py:2111`.
3. **What would show it wrong.** An approved roster replaced by candidate expectations,
   a protected loss passing, or ordinary maintenance still held after installation
   defeats the boundary. -- accepted proposal Complete current contract;
   `bootstrap/tests/_gate_manifest.py:671`; `bootstrap/tests/_gate_preflight.py:3425`.

**S1 — Blocking: make classification precede its approval fence.** Agree with ordinary
F1: C1 currently gates the chunk producing its own approval input. **Satisfier:** permit
evidence collection first, then have a high-tier agent make the security/trust
classification judgment, then seek Maintainer approval of the exact roster before
narrowing. Inventory current imports, dynamic loading, fixtures and controlling helpers,
not only filenames or the historical floor. Keep new unrostered test paths ordinary by
default; classify new protected helpers through the controlled roster/authority path,
never candidate labels. -- plan C1; `AGENTS.md` Model tier;
`bootstrap/tests/_gate_preflight.py:1815`.

**S2 — Blocking: specify the refusal and provenance tests.** Agree with ordinary F2;
“roster tampering” and “ordinary changes” leave consequential cases implicit.
**Satisfier:** map protected and ordinary edit/add/delete/rename/new-marker cases,
missing/malformed roster and manifest, collection errors, and actual release
skip/xfail/xpass to owning tests. Name real stage-1/stage-2 transition and steady-state
cases proving the first roster matches approved reviewed bytes and later membership
comes from the verified prior anchor; candidate membership substitution must refuse in
each stage. Include `bootstrap/tests/test_gate_reanchor.py`, `test_gate_preflight.py`
and `test_security_check.py`. Preserve closure validation, static comparison and stage-2
manifest-byte equality rather than bypassing them to demonstrate success. --
`bootstrap/tests/_gate_preflight.py:2097`, `:3204`, `:3425`;
`bootstrap/tests/test_security_check.py:684`.

**S3 — Blocking: connect the governing promise to the actual trigger.** Agree with
ordinary F3: require the accepted S3 governing statement and its exact human-run
verifier invocation. The current runbook's executable page calls the launcher; its later
reference describes external `verify --trusted-repo` as unused. **Satisfier:** trace the
delivered command through its real entry point and tests to protected HOLDs, full census
and ordinary notes; do not imply an automatic or existing invocation that does not run.
Keep narrowed mode inactive until the verified Maintainer ceremony installs it. --
accepted proposal S3; `bootstrap/REANCHOR_RUNBOOK.md:24`, `:228`; plan C4–C5.

**Coverage.** Claims, production paths, completeness and refusal (#1–4): cited producer,
static comparison, both stages and release tests; reuse, drift and placement (#5–7):
repeated Reuse search, launcher/runbook and S3; scope and satisfiers (#8–9): accepted
contract and S1–S3. Source files cited above are unchanged between reviewed commit and
`0ac350c0`. No pytest, mutation, complete inventory or future implementation validation
performed. This pass supplies the Security Review; the author must fold its findings
before implementation.

## Response to plan review -- Codex (gpt-6.1-terra) -- 2026-10-28

| Findings | Disposition | Operative cells |
|---|---|---|
| F1, S1 | Accepted | Sequence; C1a–C1c |
| F2, S2 | Accepted | C2–C3; Verification |
| F3, S3 | Accepted | Documentation / doctrine surface; Verification |

## Implementation log -- C1a factual inventory -- Codex (Luna, low) -- 2026-10-28

Measured the committed source tree `7f12a3f648c525446b041f523ae967b4f1d20cae`. A read-only archive collection with `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest --collect-only -q --disable-warnings bootstrap/tests` collected 5,479 node IDs across 129 test files; all 129 test files yielded nodes. The syntactic dependency scan covers all 141 Python paths under `bootstrap/tests`, resolving import candidates against 227 repository Python paths and recording fixture definitions/arguments, dynamic-load calls and path-like literals with exact matches separated from basename candidates. The exact node list and per-file hashes/references are in `dev/plans/test-trust-boundary/c1a-node-inventory.jsonl` and `c1a-dependency-inventory.json`.

The source manifest has 17 entries and the accepted contract adds 10 distinct test paths (27-floor union). Existing byte-freeze discovery yields 197 paths across its five source patterns; seven Python authority-closure members are joined by the runbook, launcher, re-anchor script and allowed-signers file (11 total). The inventory records the fixture files and excluded frozen paths. Positive controls found a collected `test_gate_manifest.py` node and the `conftest.py` manifest load. Collection only ran; no test body ran and `CAIRN_FULL_SUITE` was not set.

This is factual input, not a completed protected-set decision. The high-tier pass still needs to decide which import/collection/execution dependencies require protected membership beyond the already-required floor, how to treat path-level fixtures and helper modules, and which new trust helpers enter authority closure. The scan is syntactic and does not establish runtime reachability or security classification.
