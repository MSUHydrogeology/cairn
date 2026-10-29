# Plan: Connect the content tripwire to the security dispatcher

**Source proposal**: dev/proposals/archive/2026-10-29-codex-dispatcher-content-scan.md
**Status**: archived
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Run the installed content tripwire through the local security command and report its limited evidence honestly.

## Source proposal

The Maintainer accepted the revised proposal: admit the installed content-security self-audit as an offline leg, bind its entire apparatus, preserve the direct advisory command and opt-out, and fail closed on unreliable evidence.

## Scope

Change the dispatcher registry and binding schema, content runner, installed guidance, relevant install/upgrade and security tests, and the stale security strategy claim. No installation runs a scan. Link/claim checking and credential forwarding are not included; the combined strategic gap remains open. No doctrine premise changes; installed instructions belong in module guidance, implementation description in descriptive documentation, and deliberation in the strategy record.

**Reuse.** Search `rg -n 'content_scan|security_verification' bootstrap/tests bootstrap/_scaffold/config.py` found the installed runner, scanner, dispatcher and their test owners. Extend the runner with a fixed dispatcher mode and reuse its audit; keep its ordinary invocation unchanged. Reuse the dispatcher's existing containment, symlink, digest, child execution and result validation checks for each member.

The five verbatim destinations each have a `dev/.cairn/cairn-lock.yml` file record keyed by `dst`; the dispatcher reads its `hash` before launch. `scripts/content_scan_runner.py` is the source-owned runner and reads/imports `scripts/content_scan.py`; those two are executable apparatus maintained by Cairn. The runner reads `scripts/content_scan_roots.txt`, `scripts/content_scan_residuals.txt`, and `scripts/content_scan_allowlist.txt`: adopter-reviewed policy, installed with Cairn defaults. The lock writer records each destination; scoped finalize advances its `hash`; upgrade classifies verbatim changes using `base_hash`, preserving the upstream baseline. The dispatcher binds all five before launching the runner, which imports the scanner only afterward.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Bind and exercise the dependency group and child result | Plan reviews complete | Schema, runner mode, tests and registry entry |
| C2 | Reconcile installation, upgrade and guidance | C1 | Policy maintenance instructions, installed-path tests, strategy correction |
| C3 | Verify and hand off | C2 | Stable change evidence; independent usual and Security code reviews |

## Acceptance criteria

### C1

The fixed source registry selects content-security only when installed. Extend the required registry schema with a fixed tuple of additional immutable-digest paths: scanner plus roots, residuals and allowlist; retain the existing immutable runner binding. Every member has an exact lock record, regular file, contained path and no symlink ancestor, and its bytes match that record before child launch. Reject duplicate, unsafe, missing, altered, wrongly typed or unrecognized bindings and records. No adopter input chooses executable paths or arguments. A digest and lock controlled by the same attacker do not authenticate a checkout.

The fixed child mode emits one bounded schema-valid JSON document on stdout; diagnostics cannot corrupt it. Preserve timeout, output cap, exit/result agreement and terminal escaping. Any remaining scanner flag, including an accepted residual, is `FINDINGS`; zero flags is `CLEAN` only after a valid nonempty audit and current baseline. Invalid, stale, missing or failed evidence cannot yield `CLEAN`. Preserve other legs and precedence.

### C2

Document this procedure: review the intended policy edits, then from the Cairn checkout run `python bootstrap/scaffold.py upgrade --target <adopter-root> --finalize <selected-policy-path>`, naming each changed destination explicitly; review and commit the policy and resulting lock diff together. Scoped finalize attests current bytes, not the fact of review; never use bare finalize to accept policy drift. The original `base_hash` remains the upstream baseline. Test that selected reconciliation leaves unrelated drift unblessed, the real dispatcher accepts the intended policy, and a subsequent upstream policy change preserves the customized file without silently trusting or overwriting it. First prove the existing upgrade behavior; if it cannot satisfy this, stop for a reviewed plan correction before changing the engine. Verify fresh default and opted-out installs and API/web combinations via `python scripts/run_security_verification.py local`; preserve `python scripts/content_scan_runner.py` behavior.

Describe only tracked Markdown/text under configured roots, excluding archives and base cache; untracked files and bare URLs in discussion prose are blind spots. A clean result is a pattern tripwire, not a safety or checkout-authenticity guarantee. Meet the six admission conditions in `templates/modules/default-on/security-verification.md`, including reviewed execution evidence and registry Security Review.

### C3

Record the tests and mutations below on the final implementation commit. A false clean, hidden finding, silent selected-leg loss, broken direct command or unmaintainable reviewed policy keeps the work open. An independent usual code review and Security Review assess the registry and evidence; no scientific result is involved.

## Scope delta

**Scope delta**: preserved

## Verification

Boundary A and B use the canonical Python 3.13 interpreter. This is a contract and trust surface: Boundary B is wide, on a clean final implementation commit, with `Certified by: pending`. Run the owning families `bootstrap/tests/test_security_verification.py`, `bootstrap/tests/test_security_stack.py`, `bootstrap/tests/test_default_security_stance.py`, `bootstrap/tests/test_module_merge_lockfile.py`, and `bootstrap/tests/test_notice_install.py`; search again for changed mappings and lock consumers and add any owner found. Split selections at the guard limit and reconcile the executed union. Include real temporary default and opt-out installs and the local command, clean and flagged content, API/web combinations, direct runner and upgrade.

Map existing nodes: `bootstrap/tests/test_security_verification.py::TestRegistryIntegrity::test_every_admission_field_is_required` covers required fields; `::TestParentComputedBinding::test_runner_or_policy_digest_mismatch_is_degraded` and `::TestParentComputedBinding::test_symlinked_runner_or_policy_is_refused` cover existing binding; `::TestComposition::test_the_dispatcher_runs_from_a_real_fresh_scaffold` covers the public command; `::TestDispatchBehavior` covers isolation and child failures. `bootstrap/tests/test_security_stack.py::TestRunnerExitContract` and `::TestAuditRootsManifest` cover direct behavior and audited roots. Add focused nodes for the new tuple's closed shape and each member, real default/opt-out/combined selection, flags including residuals, and scoped finalize plus subsequent upstream upgrade. Include `bootstrap/tests/test_lockfile_provenance.py` and search finalize/upgrade owners for the reconciliation path; retain owning families above for the wide run.

Add negative controls for every new schema field and bound member: missing, changed, unsafe or symlinked member, malformed or duplicate records, policy edits before and after reviewed reconciliation, empty/invalid roots and stale baseline. Exercise malformed child JSON, exit mismatch, timeout, output cap, precedence, and accepted residual findings. Mutate each bound member and child evidence separately and record the failing control with an unmutated control; this does not claim protection against an attacker replacing both lock and files. Verify the actual audited set against the documentation.

Run `python scripts/check_cairn.py`, `python scripts/claim_check.py` on changed documents, `python scripts/link_check.py`, and `python scripts/quality_gate.py --sub neutrality` for prose and standing checks; run other standing gates found for touched surfaces. Record commands, counts, non-pass dispositions, elapsed times, pre/post state, tested SHA and known omissions in the implementation verification record. Independent code review performs targeted falsification rather than repeating Boundary B. Certification and re-anchor are separate authorized ceremonies; do not run the full suite here.


## Plan review -- Codex (gpt-6.1-sol, ordinary reviewer) -- 2026-10-29

**Reviewed commit**: a204f67d
**Tier**: Internal
**Findings**: 1 blocking
**Verdict**: REVISE

**Foundations**

1. **Does the plan deliver the Decision?** Not yet: it postpones the accepted dependency, ownership and lock-reader mapping and exact test-node map until implementation, leaving policy reconciliation and its evidence unspecified -- accepted proposal, Evidence / verification plan; plan C2 and Verification.
2. **Best alternative.** Keep the existing runner and dispatcher binding mechanisms as planned, but map the five installed paths to their lock records, readers and policy owner, decide the reviewed edit and upgrade procedure, and name existing test nodes plus new behaviors before implementation; this is a clarification, not a new subsystem -- `bootstrap/_scaffold/config.py`, content-security mapping; `bootstrap/_scaffold/install.py::write_install_lockfile`; `bootstrap/tests/test_security_verification.py`.
3. **What would show it cannot deliver?** A reviewed policy edit that cannot be reconciled without silently accepting drift, or a changed input that still yields clean, would defeat the accepted outcome -- plan C2 and Verification; `templates/modules/team-gated/content_scan_runner.py::_load_content_scan`.

### P1 -- Map the authority and verification before execution

The accepted proposal explicitly requires the plan to map dependencies, policy ownership, lock records and readers, and to name exact test nodes. C1 names a binding tuple and C2 asks the implementer to establish a procedure from the existing writer, but neither identifies the records and readers or determines how a reviewed policy edit is made authoritative and survives upgrade. The Verification section names whole families and says to search again; it does not map existing nodes to the new contract or identify which behaviors require new nodes. For example, `TestParentComputedBinding::test_runner_or_policy_digest_mismatch_is_degraded` and `TestComposition::test_the_dispatcher_runs_from_a_real_fresh_scaffold` already exercise relevant but narrower paths. Without the map a reviewer cannot assess whether the planned authority transition or specific evidence reaches the accepted outcome.

Recommend an explicit path → record → reader → owner map for the runner, scanner and three policy files; establish the supported reviewed policy/lock reconciliation and upgrade path, or identify the precise change needed and its authority boundary. Map existing nodes and proposed new tests to selection, every bound member and schema field, real installs, direct invocation, policy reconciliation, upgrade and failure behavior. Retain the wide contract-surface verification and the guard-limit union; do not replace it with an unrequested full suite. If the procedure cannot be established safely, leave implementation blocked rather than choosing an unreviewed authority during C2.

**Coverage:** Read the committed plan and accepted proposal, installed mapping, runner dependencies, dispatcher test names, and lock writer locations for claims, completeness, scope, verification and alternatives. This is a plan review; no implementation or runtime checks were performed. The separate Internal Security Review remains owed.


## Plan review -- Codex (gpt-6.1-sol, Security reviewer) -- 2026-10-29

Reviewed commit: 426fb26ccfce8255075e4a7df66e967b2161e80c
Target: operative plan; dependency execution and reviewed policy authority
Prior findings: ordinary P1 (not discharged by this pass)
Assurance path: high-assurance

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: 1 blocking
**Verdict**: REVISE

**Foundations**

1. **Does the plan deliver the Decision?** Its fixed dependency tuple, pre-launch checks and strict child result deliver the intended narrowing, but reviewed policy authority is still deferred to implementation -- plan C1/C2; accepted proposal, Response and Evidence / verification plan.
2. **Best alternative.** Establish the existing scoped finalize path and preserved upstream baseline before inventing another reconciliation mechanism; bind all five files without extending living-state exceptions -- `bootstrap/_scaffold/upgrade.py::_cmd_finalize_lockfile`, `bootstrap/_scaffold/lockfile.py::classify_verbatim`.
3. **What would show it wrong.** A finalized roots/residual/allowlist edit that becomes silently overwritten or an altered apparatus member launched unchecked defeats the security outcome -- `bootstrap/_scaffold/upgrade.py::_compute_upgrade`, `templates/modules/default-on/run_security_verification.py::_bind_runner`.

### S1 -- Settle the policy authority transition before implementation

This reinforces ordinary P1 rather than adding a second mechanism. C2 leaves the supported procedure and possible upgrade change to the implementer. That is a security design decision: which reviewed bytes the dispatcher accepts, and whether upgrade preserves them. The install writer is not a reconciliation command: `bootstrap/_scaffold/install.py::write_install_lockfile` refuses diverged installed bytes. All five content apparatus files are currently verbatim installs -- `bootstrap/_scaffold/config.py`, content-security mapping.

There is already a practical candidate. `bootstrap/_scaffold/upgrade.py::_cmd_finalize_lockfile` supports named paths, advances their `hash`, preserves the original verbatim `base_hash`, and refuses unmatched names. Upgrade classifies verbatim files against `base_hash` where available, so a deliberate policy fork should remain locally modified rather than become replaceable merely because its accepted `hash` advanced. Scoped finalize skips the whole-tree dirty check; it is deliberate re-attestation, not proof that a review happened. The guidance must name the human review and exact selected paths before that command, then review/commit the resulting lock change. Neither bare finalize nor the API/web living-state exception should become an automatic policy acceptance step.

Satisfier: fold the exact reviewed edit/finalize/lock-review procedure and the five-path record/reader/owner map into C2; name tests proving selected policy reconciliation leaves unrelated drift unblessed, the real dispatcher then accepts the intended bytes, and a later upstream policy change preserves the customized policy without silently trusting or overwriting it. Determine whether existing behavior suffices before authorizing any engine change. This preserves accepted scope.

The remaining security design is proportionate: validate scanner and policy siblings before child import, keep argv source-owned, preserve isolated Python and closed child environment, and map any flag to FINDINGS. Existing same-user check/use races and host Git provenance remain trusted-tree limits, not new authentication promises -- `templates/modules/default-on/run_security_verification.py::_is_regular_and_unsymlinked`, `_run_child`; `templates/modules/team-gated/content_scan_runner.py::_resolve_git`.

**Coverage:** Covered claims, public-path evidence design, completeness, fail-closed behavior, drift, lifecycle, scope and satisfiers through the cited bindings, install/finalize/upgrade owners, accepted proposal and `bootstrap/tests/test_security_verification.py::TestComposition`. Not covered: runtime implementation, mutations or certification; no tests or full suite run, and no scientific result is involved. This records the Security plan pass; the author must fold findings before implementation.

## Response to plan review -- Codex (gpt-6.1-sol) -- 2026-10-29

| Finding | Disposition |
|---|---|
| P1 | Folded: Scope maps the five records, readers and owners; C2 specifies reviewed scoped finalize and upgrade proof; Verification maps existing nodes and new controls. |
| S1 | Folded: C2 preserves `base_hash`, requires review of policy and lock, excludes unscoped finalize, and stops for plan correction if existing upgrade cannot preserve policy. |

The Security plan pass is recorded above; its findings are addressed in the operative cells. Plan review has one round.

## Implementation verification -- Codex (gpt-6.1-sol) -- 2026-10-29

**Boundary B mode**: wide. The changed dispatcher registry and runner form a contract and trust surface; the affected set includes install selection, lockfile provenance/finalize and upgrade preservation, child execution, the shipped local command, direct runner behavior, and installed guidance. The five owning families below plus `test_lockfile_provenance.py`, real default/opt-out installs, API/web combinations, and the local dispatcher cover the mapped integrations and public paths. The exact contract cannot be bounded to one test module.

**Certified by**: pending
**Tested commit**: `3dcb5806a0442b959a81cc3287a9ded9c5b44a4a`
**Reviewed range**: `a6c151f1..3dcb5806a0442b959a81cc3287a9ded9c5b44a4a` (module-discovery integration base through final dispatcher implementation)
**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` -- Python 3.13.13

**Pre-run state**: fresh local clone at the tested commit; detached `HEAD` matched the tested SHA; `git status --short` empty.
**Post-run state**: same `HEAD`; `git status --short` empty and `git diff --stat` empty. Pytest cache and all temporary adopter installs were ignored or created outside the clone.

| Command | Exit | Outcomes | Elapsed |
|---|---:|---|---:|
| `python3.13 -m pytest bootstrap/tests/test_security_verification.py bootstrap/tests/test_security_stack.py bootstrap/tests/test_default_security_stance.py` | 0 | 290 passed | 22.55 s |
| `python3.13 -m pytest bootstrap/tests/test_module_merge_lockfile.py bootstrap/tests/test_notice_install.py bootstrap/tests/test_lockfile_provenance.py` | 0 | 38 passed | 1.47 s |
| `python3.13 -m pytest -q bootstrap/tests/test_security_verification.py::TestNoCapabilityContract::test_a_socket_opening_child_is_excluded_by_admission_not_blocked_at_runtime` (loopback-enabled rerun) | 0 | 1 passed | 0.05 s |
| `python3.13 scripts/check_cairn.py` | 0 | 187 Markdown files; no issues; 83 external links not probed | not timed |
| `python3.13 scripts/claim_check.py <each changed plan/module/strategy document>` | 0 | all four documents OK; security-verification module had two declared path exemptions | not timed |
| `python3.13 scripts/link_check.py <six changed plan/module/template Markdown files>` | 0 | 6 files; no issues | not timed |
| `python3.13 scripts/quality_gate.py --sub neutrality` | 0 | 0 failures; 43 informational findings | not timed |

**Plan-specific acceptance commands**: the two owning-family commands above cover the required wide mapping. They include real temporary adopter installs, opt-out, API/web combinations, direct runner and dispatcher behavior, child failure handling, scoped finalize and upgrade preservation. `bootstrap/tests/test_security_verification.py::TestRegistryIntegrity::test_content_entry_binds_every_immutable_apparatus_member` is the positive control; its 25 per-member mutation cases all fail closed before child launch. The full mutation ledger is [implementation-verification.md](2026-10-29-dispatcher-content-scan/implementation-verification.md).

**Non-pass disposition**: the first restricted-environment run of the first command produced 289 passed and one failure because its force-injected child could not bind a loopback socket. The test passed alone with loopback access enabled, then the complete mapped command passed (290 passed) with that same access. This is environmental, not waived. No skips, xfails or xpasses were reported in the successful runs.

**Known omissions**: no whole-tree certification, re-anchor, historical-anchor reconciliation, live-reference probe, or push was performed; those are outside this plan's Boundary B. `check_cairn.py` did not probe its 83 external links. The checks do not authenticate a checkout against an attacker able to replace both apparatus bytes and lock records, as stated in C1.


## Code review -- Codex (gpt-6.1-sol, independent reviewer) -- 2026-10-29

**Reviewed commit**: 902cf35f
**Target**: implementation range `a6c151f1..3dcb5806a0442b959a81cc3287a9ded9c5b44a4a` and verification at `902cf35f`
**Prior findings**: none

**Foundations**

1. **Does it do what it claims?** The content leg binds the five installed paths before launching the child and maps flags to findings, but the stated reviewed range includes additional onboarding changes without their owning tests in the author's verification record -- `templates/modules/default-on/run_security_verification.py::_bind_runner`, `scripts/content_scan_runner.py::main`, and the verification record above.
2. **Best alternative.** Keep the existing runner and fixed registry; accurately delimit the change or add the missing author-owned evidence, and correct the runner path in the ledger -- `bootstrap/_scaffold/install.py` and `dev/plans/archive/2026-10-29-dispatcher-content-scan/implementation-verification.md`.
3. **What would show it wrong.** A changed onboarding behavior failing its owning tests, or a bound member reaching the child after drift, would falsify the claims -- see the falsification ledger below.

**Bounding**: WIDER RUN REQUIRED -- the stated range includes `d3c9b80a` and `258dbb26`, which change `bootstrap/_scaffold/install.py` and onboarding, preset and scaffold tests. The Boundary B record lists neither those owning test families nor a separate evidence record for them. The author must either establish the correct independently verified range and cite evidence for every change in it, or record the missing checks on the candidate commit. My passing run below does not substitute for the author's record.

### Findings

**CR1 -- Verification does not cover the stated range.** The verification names `a6c151f1..3dcb5806`, but that range includes the no-preset onboarding implementation and changed tests. Its commands omit `test_install_time_onboarding.py`, `test_onboarding_slot_substitution.py`, `test_presets.py`, and `test_scaffold.py`. The stated wide coverage therefore does not establish all changed behavior. Supply an author-owned change-specific record or establish the narrower range and cite the separate record covering the omitted changes.

**CR2 -- Ledger identifies the wrong bound runner.** The first five rows of the implementation ledger name `templates/modules/default-on/run_security_verification.py`; the test obtains `entry.runner_repository_path`, which is `scripts/content_scan_runner.py`. Correct the rows so the evidence identifies the member actually mutated.

### Falsification ledger

* Challenged the unrecorded onboarding surface in a fresh local clone detached at `3dcb5806`: `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q bootstrap/tests/test_install_time_onboarding.py bootstrap/tests/test_onboarding_slot_substitution.py bootstrap/tests/test_presets.py bootstrap/tests/test_scaffold.py` passed 182 tests in 4.40 seconds. This challenges CR1's consequence but does not repair the missing author record.
* Compared the five-member control and mutations in `bootstrap/tests/test_security_verification.py::TestRegistryIntegrity` to the registry and ledger: the actual runner is `scripts/content_scan_runner.py`; the ledger labels another file. This produced CR2.
* Read `scripts/content_scan_runner.py::run_content_scan` and `main`: any remaining flag returns 1 and maps to FINDINGS; stale evidence returns 3 and maps to DEGRADED. Reviewed installed selection, opt-out, combinations and policy-finalize test paths in `TestComposition` and the verification record; did not independently repeat those mapped tests.

**Waiting-line check:** No Maintainer-gated chunk or deviation request is declared in the reviewed plan range; `git log -p -- dev/plans/2026-10-29-dispatcher-content-scan.md` was inspected.

**Coverage:** Reviewed registry and binding, result mapping, selected installed paths, policy retention tests, and recorded evidence; challenged onboarding tests and ledger naming as above. Did not run the whole suite, independently mutate every member, or assess the separate Security Review obligation. No scientific result is involved.

## Response to code review -- Codex (gpt-6.1-sol) -- 2026-10-29

| Finding | Disposition |
|---|---|
| CR1 | Addressed with separately attributed evidence. On clean commit `3dcb5806`, the author ran the four omitted onboarding, preset and scaffold test files: 182 passed. The module-discovery changes have independent wide evidence on clean commit `eee603a6`, recorded in `dev/plans/2026-10-29-module-discovery-activation.md` and committed at `f51b84b1`; that record names all mapped tests, gates, interpreter and mutation outcomes. The supplemental record distinguishes dispatcher-owned commits `dc309b0e` and `3dcb5806` from module-owned changes and identifies the integrated tested candidate. See `dev/plans/archive/2026-10-29-dispatcher-content-scan/implementation-verification.md` for commands and attribution.
| CR2 | Corrected: the mutated runner is `scripts/content_scan_runner.py`, the value of `entry.runner_repository_path`; all five ledger rows now name that path. |

The original Boundary B record remains the author's result on `3dcb5806`; the later module agent run is cited as independent coverage, not represented as the author's run. The usual code-review response is recorded. The required Security Review remains pending; no `Bounding: ACCEPTED` determination or archive transition is made here.


## Code review -- Codex (gpt-6.1-sol, independent Security reviewer) -- 2026-10-29

**Reviewed commit**: `3dcb5806a0442b959a81cc3287a9ded9c5b44a4a`
**Target**: dispatcher-owned implementation commits `dc309b0e` and `3dcb5806`; plan and corrected evidence through `7a541182`
**Prior findings**: none in this Security code pass
**Obligation**: Security Review of registry admission, apparatus binding and child evidence
**Tier**: Internal Security Review
**Findings**: none

**Foundations**

1. **Does it do what it claims?** Yes within its trusted-checkout boundary: all five members bind before launch, policy drift requires explicit reconciliation, and uncertain child evidence degrades -- `templates/modules/default-on/run_security_verification.py::_bind_runner`, `_evaluate_capability`; `bootstrap/tests/test_security_stack.py::TestContentPolicyReconciliation`.
2. **Best alternative.** Retain the fixed registry and existing scoped finalize rather than introduce another policy authority; the original upstream baseline remains distinct from accepted local bytes -- `bootstrap/_scaffold/upgrade.py::_cmd_finalize_lockfile`, `bootstrap/_scaffold/lockfile.py::classify_verbatim`.
3. **What would show it wrong.** Unchecked apparatus launch, hidden residual findings or an empty audit accepted as clean would defeat admission -- see the falsification ledger below.

**Bounding**: ACCEPTED -- challenged each bound member and child evidence independently; the wide author record and its range correction identify the owning integration paths and separately attributed module evidence. Certification remains pending.

### Falsification ledger

Python 3.13.13 at `/Users/kendal30/conda_envs/lhm/bin/python3.13`; control in a fresh detached worktree at the reviewed commit; each mutant in a separate fresh local clone of those bytes. No broad suite was run.

* Unmutated control: `python3.13 -m pytest -q bootstrap/tests/test_security_verification.py::TestRegistryIntegrity bootstrap/tests/test_security_verification.py::TestDispatchBehavior::test_process_exit_and_result_must_agree bootstrap/tests/test_security_stack.py::TestRunnerExitContract` -- 58 passed, 1.06 s.
* Enumerated the complete member set from `_REGISTRY["content-security"]`, then bypassed binding for exactly one member per clone. Ran `TestRegistryIntegrity::test_content_apparatus_member_failure_refuses_before_launch` in each clone: `scripts/content_scan_runner.py` killed; `scripts/content_scan.py` killed; `scripts/content_scan_roots.txt` killed; `scripts/content_scan_residuals.txt` killed; `scripts/content_scan_allowlist.txt` killed. Each mutant produced 5 failed / 20 passed: the checks detect removal of each member's guard.
* Removed the nonempty-files condition in both byte-identical runner copies: `TestRunnerExitContract::test_empty_audit_cannot_become_clean_dispatcher_evidence` killed the mutant (1 failed).
* Changed residual-only FINDINGS to CLEAN in both runner copies: `TestRunnerExitContract::test_dispatcher_mode_emits_one_closed_result_document` killed the mutant (1 failed).

**Waiting-line check:** No fenced chunk or deviation request in this plan's reviewed range; its sequence is C1–C3 without a Maintainer fence.

**Coverage:** Claims, production paths, completeness and fail-closed evidence: registry/binding, above controls and mutations, and the recorded installed-command tests. Consistency, reuse and drift: fixed registry reuses `_bind_runner`, paired runner sources, installed policy guidance and corrected ledger at `7a541182`. Lifecycle, scope and satisfiers: scoped-finalize authority and C1–C3; no findings require a satisfier. No scientific calculation is involved. **Not covered / low confidence:** did not repeat the author's install/upgrade families, authenticate host Git or a checkout whose attacker controls both lock and apparatus, close the documented same-user check/use race, run certification or perform a re-anchor. These are limits, not clean security claims.

## Lasting-truth migration -- 2026-10-29

**Dispositions**:

* Link/claim-check legs -> defer (they remain separate security-verification work; the accepted content leg does not provide them) -> `dev/PLANNING.md` > Security cluster strategic items. Maintainer authorization, 2026-10-27: *"Let's add those security items to v0.6"*.
* API/web credential pass-through -> defer (the separate trust question remains open; no credentials are forwarded by this change) -> `dev/PLANNING.md` > Security cluster strategic items. Maintainer authorization, 2026-10-27: *"Let's add those security items to v0.6"*.

**Evidence shipped**: Boundary B wide test families and standing gates at `3dcb5806`; the author’s separate onboarding/preset/scaffold selection (182 passed); independent module-discovery integration evidence at `eee603a6` (`dev/plans/2026-10-29-module-discovery-activation.md`, committed at `f51b84b1`); 25 per-member binding mutants with a positive control; and the Security Review’s fresh control and independent binding/child-evidence mutations. Implementation evidence and exact outcomes are recorded in this plan and its archived `implementation-verification.md` file.

**Evidence deferred**: no whole-tree certifying run or re-anchor was performed. The plan explicitly treats certification as a separate integration ceremony; `Certified by: pending` remains in the Boundary B record. The local link gate did not probe external URLs (83 were reported unprobed); the plan required local link integrity, not an external-link probe. No Boundary B acceptance check remains unmet.

**Deferred evidence home**: certification status remains in the Boundary B record and follows the authorized integration-point rule in `AGENTS.md` > Verification boundaries. The separate link/claim and credential follow-ups are on the Security cluster row in `dev/PLANNING.md`; no other evidence was left without a required home.

**Fidelity sign-off**: dispatcher implementation commits `dc309b0ee7efa68cc345f6d7776e41df3e1f9dbf` and `3dcb5806a0442b959a81cc3287a9ded9c5b44a4a` implement the accepted Revised `## Proposal` section in `dev/proposals/archive/2026-10-29-codex-dispatcher-content-scan.md` at `a204f67d`. Concurrent module-discovery changes are separately attributed and verified in the module-discovery plan; they are not represented as dispatcher-owned commits.
