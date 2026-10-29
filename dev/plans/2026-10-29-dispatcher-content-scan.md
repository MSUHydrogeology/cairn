# Plan: Connect the content tripwire to the security dispatcher

**Source proposal**: dev/proposals/archive/2026-10-29-codex-dispatcher-content-scan.md
**Status**: revising-plan
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Run the installed content tripwire through the local security command and report its limited evidence honestly.

## Source proposal

The Maintainer accepted the revised proposal: admit the installed content-security self-audit as an offline leg, bind its entire apparatus, preserve the direct advisory command and opt-out, and fail closed on unreliable evidence.

## Scope

Change the dispatcher registry and binding schema, content runner, installed guidance, relevant install/upgrade and security tests, and the stale security strategy claim. No installation runs a scan. Link/claim checking and credential forwarding are not included; the combined strategic gap remains open. No doctrine premise changes; installed instructions belong in module guidance, implementation description in descriptive documentation, and deliberation in the strategy record.

**Reuse.** Search `rg -n 'content_scan|security_verification' bootstrap/tests bootstrap/_scaffold/config.py` found the installed runner, scanner, dispatcher and their test owners. Extend the runner with a fixed dispatcher mode and reuse its audit; keep its ordinary invocation unchanged. Reuse the dispatcher's existing containment, symlink, digest, child execution and result validation checks for each member.

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

Document a deliberate policy edit as a reviewed change to the policy and its corresponding lock digest together, with the command or exact supported procedure established from the existing lock writer; no automatic trust of changed bytes. Test that ordinary reviewed edits can be reconciled and survive upgrade without silently accepting drift; if the existing upgrade cannot preserve this, implement and test the necessary reconciliation without broadening authority. Verify fresh default and opted-out installs and API/web combinations via `python scripts/run_security_verification.py local`; preserve `python scripts/content_scan_runner.py` behavior.

Describe only tracked Markdown/text under configured roots, excluding archives and base cache; untracked files and bare URLs in discussion prose are blind spots. A clean result is a pattern tripwire, not a safety or checkout-authenticity guarantee. Meet the six admission conditions in `templates/modules/default-on/security-verification.md`, including reviewed execution evidence and registry Security Review.

### C3

Record the tests and mutations below on the final implementation commit. A false clean, hidden finding, silent selected-leg loss, broken direct command or unmaintainable reviewed policy keeps the work open. An independent usual code review and Security Review assess the registry and evidence; no scientific result is involved.

## Scope delta

**Scope delta**: preserved

## Verification

Boundary A and B use the canonical Python 3.13 interpreter. This is a contract and trust surface: Boundary B is wide, on a clean final implementation commit, with `Certified by: pending`. Run the owning families `bootstrap/tests/test_security_verification.py`, `bootstrap/tests/test_security_stack.py`, `bootstrap/tests/test_default_security_stance.py`, `bootstrap/tests/test_module_merge_lockfile.py`, and `bootstrap/tests/test_notice_install.py`; search again for changed mappings and lock consumers and add any owner found. Split selections at the guard limit and reconcile the executed union. Include real temporary default and opt-out installs and the local command, clean and flagged content, API/web combinations, direct runner and upgrade.

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
