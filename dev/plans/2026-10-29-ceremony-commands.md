# Plan: Reusable ceremony commands

**Author**: Codex (gpt-6.1-terra)
**Source proposal**: [dev/proposals/archive/2026-10-29-codex-ceremony-commands.md](../proposals/archive/2026-10-29-codex-ceremony-commands.md)
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Give the Maintainer reusable commands for checking and carrying out trust ceremonies with human approval.

## Source proposal

The accepted proposal supplies reusable reanchor and repin commands and the trust plan's full verifier, preserving the staged ceremony, independent checks, explicit human decisions and separately authorized authority transitions.

## Scope

Extend `scripts/repin.py`, `scripts/reanchor_ceremony.py`, `bootstrap/reanchor.sh`, their launcher and tests; document inputs, preparer and independent checker in `bootstrap/REANCHOR_RUNBOOK.md`. A maintained human-runnable entry point prepares the details; it does not push or automatically commit AST changes without explicit Maintainer authorization. The verifier must work before the narrowed trust boundary is installed, because it is that plan's S3 prerequisite; the trust plan remains open through its own review and installation.

**Reuse.** Searching `rg 'repin|reanchor|scan-digest' scripts bootstrap` found the v0.5 driver, read-only preflight, staged launcher and prior-P scan. Extend those paths and preserve the ordinary boot refusal on changed authority; do not replace them with candidate-controlled authority.

### Documentation / doctrine surface

Operator description belongs in the runbook; deliberation here. No doctrine change is assumed; governing text changes require their own authority.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Preparation and verifier | Both plan reviews | Reusable preparation, authenticated P and raw C checks, full report and dispositions |
| C2 | Ceremony entry paths | C1 | Ordinary and separately reviewed transition paths, staged checks and scratch demonstrations |
| C3 | Verification and review | C2 | Wide Boundary B, independent code and Security Reviews |
| C4 | Actual installation | MAINTAINER-ONLY; separately authorized each transition | Human-run signing and root installation under the trust plan |

## Acceptance criteria

**C1.** With key away, authenticate signed immutable prior P, its manifest, `_gate_manifest.py` verifier, `_gate_preflight.py` E7 scanner and their full dependency bytes; an independent reader checks provenance. Prepare a separate clean target independently checked against exact committed C using raw object bytes and hashes. The documented human command invokes P's verifier using the verified external trusted repository and P for trusted and anchor references, `--require-anchor`, full collection, empty environment and Python `-E -s`. It runs before signing, including before narrowed authority is installed. Show exact and grouped protected HOLDs and ordinary notes; bind each explicit human disposition to displayed items, P, C and verified report/collection. Changed evidence or new unexplained HOLDs require fresh review; missing inputs, inconsistent bytes, collection errors or unresolved HOLDs refuse. No automatic waiver; all 83 pending candidate reports require actual disposition. Document candidate-code execution influence.

**C2.** Reusable scripts prepare values, packet, launcher and reader inputs; the runbook names each preparer and independent checker. Demonstrate ordinary and changed-authority paths through reviewed AST deletion, reader record before write, exact-path commit, stop, interruption and fresh-package rerun without improvised commands. The Maintainer runs commands, compares hashes, approves bounded evidence and enters the passphrase; no automatic AST commit without explicit authorization, and push is separate. Preserve Y1–Y5, stage 1, raw and expected E1–E6, H and K comparisons, approval, stage 2 and signature verification with one passphrase. E5 independently checks launcher bytes. E7 independently runs authenticated old-P scanner and agrees with the report before signing. Dormant-roster and active-checker bridges each have their own candidate, packet, reader record, comparisons and authorization. Preserve prior scanner semantics; refuse unsafe transitions.

**C3.** Documented public commands run in scratch repositories with throwaway keys and passing controls. Mutate P signature, verifier, dependency and manifest; raw C hashes, roster, collection and anchor settings; report, disposition, new HOLD, packet, launcher, package and comparisons. Each stale or substituted binding refuses before signing; exercise path containment, symlink refusal, interruption and fresh-package reruns. Each bridge's altered candidate scan digest fails E7 against its passing control. Verify one signing prompt, signature and no push; no real key or ref changes.

**C4.** No implementation agent performs actual signing or ref installation. Each bridge needs its own authorization and evidence; neither authorization implies the other, a HOLD waiver or a push.

## Scope delta

**Scope delta**: preserved; no accepted outcome is removed.

## Verification

Boundary A: extend v0.5 `scripts/repin.py` callers `boot`, `manifest_status`, `build_packet`, `check_stop_records`, `run_ceremony` and the staged launcher; trace affected fixtures and consumers before implementation. Existing controls: `bootstrap/tests/test_repin.py::test_a_tracked_symlink_or_submodule_refuses_before_import`, `::test_a_symlinked_target_or_parent_is_not_followed`, `::test_the_apply_step_makes_no_commit_and_stops`; `bootstrap/tests/test_repin_ceremony.py::test_a_full_ceremony_signs_once_with_the_typed_passphrase`, `::test_a_package_rewritten_between_the_report_and_the_yes_refuses`, `::test_the_launcher_is_hashed_again_before_each_of_its_two_runs`, `::test_an_owed_ast_pin_is_written_the_stop_line_printed_and_a_rerun_proceeds`, and `::test_a_candidate_checker_that_hides_the_scan_cannot_change_what_the_page_prints`. Add public-entry controls and mutations for C1–C3 to these families, including both bridge E7 cases and full-verifier trigger. `bootstrap/tests/test_gate_manifest.py::test_trusted_verifier_detects_tamper_in_separate_target_tree`, `::test_anchor_from_trusted_repo_refuses_target_owned_forge`, `::test_require_anchor_holds_without_ref` and protected/ordinary tests own verifier behavior; `bootstrap/tests/test_gate_transition.py::test_altered_checker_rejected` owns transition substitution. Run owning families `bootstrap/tests/test_gate_preflight.py`, `bootstrap/tests/test_gate_reanchor.py`, `bootstrap/tests/test_ceremony_review_report.py`, `bootstrap/tests/test_reanchor.py`, and `bootstrap/tests/test_reanchor_driver_disclosures.py` for stage, report and launcher consumers.

Run `python scripts/check_cairn.py`, `python scripts/claim_check.py <changed-doc>`, `python scripts/link_check.py`, `python scripts/sync_doc_snippets.py --check`, and `python scripts/quality_gate.py --sub neutrality` for prose, claims, links, snippets and neutrality.

Boundary B is **wide** for this trust ceremony: run the mapped families, documented scratch entry paths, mutation controls and standing gates on the clean final implementation SHA with canonical Python 3.13; record exact SHA, range, commands, timings, counts, omissions and non-passes, clean pre/post state, and **Certified by**: pending. No full-suite certification is implied. Fresh independent Terra plan review and Sol Internal Security Review precede implementation; independent code and Security Reviews falsify the final range. C4 stays fenced.

## Plan review -- Codex (gpt-6.1-terra) -- 2026-10-29

```
Reviewed commit: df4f9ac5290fae5260db52c9016ae918be7c2f68
Target: opening plan, accepted contract, verifier and ceremony paths
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** The staged reuse and fenced installation fit the Decision, but the verifier identity, operator handoff and reviewed test map need correction to establish delivery. -- Plan C1–C4; `bootstrap/REANCHOR_RUNBOOK.md:74`.
2. **Best alternative.** Extend the shipped driver and launcher, using the existing prior verifier and scanner for their distinct jobs; a manual-only path does not deliver the approved reusable commands. -- `scripts/repin.py:971`; `bootstrap/REANCHOR_RUNBOOK.md:74`.
3. **What would show it wrong.** A documented public workflow that cannot prepare and independently check its inputs, invokes the wrong prior tool, or reaches signing after a damaged comparison would fail the accepted outcome. -- Complete current contract; `bootstrap/REANCHOR_RUNBOOK.md:74`.

**F1 — Blocking: identify and isolate the full verifier.** C1 names P's `_gate_preflight.py` and manifest, but the existing human-run full verifier is P's `_gate_manifest.py verify`; the former supplies the independent E7 scan. A plan could satisfy its wording by authenticating the scanner while executing an unverified verifier. The runbook also requires a separate clean target, independently checked against C, and an empty environment with Python `-E -s`. **Satisfier:** bind and independently check the signed P verifier's raw bytes and manifest separately from the E7 scanner; require a prepared, human-runnable command on a separate clean C target with the existing isolation and full-collection/anchor settings, and demonstrate that this documented command triggers the verifier before signing. Preserve the stated residual candidate-code influence. -- Plan C1–C2; `bootstrap/REANCHOR_RUNBOOK.md:64`, `:74`; source contract.

**F2 — Blocking: make preparation and checks demonstrable.** C2 says to document preparation and a reader record, but does not require scripts to prepare values, packets, launcher and reader inputs or identify the preparer and independent checker of each. Nor does it require the Maintainer's actions to fit the accepted run, compare, approve and passphrase workflow. The current driver still requires reader handoff and an AST commit after a stop. **Satisfier:** carry these explicit outcomes into C1–C2 and demonstrate both documented paths through reviewed deletion, record, exact-path commit, interruption and fresh-package rerun without improvising per-ceremony commands; keep the no-automatic-commit and push boundaries. -- source Complete current contract; `scripts/repin.py:971`, `:1027`; Plan C2.

**F3 — Blocking: map behavior to checks before implementation.** Verification lists broad families and defers tracing callers, while the accepted contract requires exact nodes and callers and the template requires a reviewed invariant/public-path mapping. A family list cannot show which check exercises each refusal or documented command. **Satisfier:** map existing exact nodes and changed callers, identify where new public-entry nodes will be added, and associate each planned control and mutation with its owning family, including both bridge E7 controls and the actual full-verifier trigger. Trace affected fixtures and consumers before implementation; preserve wide Boundary B. -- Plan Verification; `dev/plans/_template.md` Verification; `bootstrap/tests/test_repin_ceremony.py:1533`.

**Covered:** claims and completeness (1,3): runbook verifier and source contract; production path and refusal (2,4): `scripts/repin.py:971`, `:1063`, runbook E5/E7 and F1–F3; cross-document and drift (5,6): plan, source contract, trust plan S3 and runbook; lifecycle (7): plan C3–C4 and trust plan C4–C5; scope/domain (8): source contract and plan Scope delta, no scientific result; satisfiers (9): F1–F3. Reuse searches `rg 'repin|reanchor|scan-digest' scripts bootstrap` and `rg 'def (boot|run_ceremony|build_packet|check_stop_records)|commit|delet' scripts/repin.py` have known matches.

**Not covered / low confidence:** review is source inspection only; no tests, mutations, signing or ref changes. This pass does not discharge Internal Security Review.

## Plan review -- Codex (gpt-6.1-sol, high), Security Reviewer -- 2026-10-29

```
Reviewed commit: df4f9ac5290fae5260db52c9016ae918be7c2f68
Target: opening plan and inherited trust-ceremony contract
Prior findings: none for this obligation
Assurance path: high-assurance
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** The plan retains both separately authorized bridges, independent E5/E7 and human signing, but must identify the full verifier and bind reusable approvals to their evidence. -- C1–C4; `bootstrap/REANCHOR_RUNBOOK.md:74`.
2. **Best alternative.** Extend the existing raw-object extraction, staged launcher and prior tools; preserve ordinary boot refusal and add a reviewed transition path rather than bypassing it. This delivers the accepted outcomes. -- `scripts/repin.py:273`; `bootstrap/reanchor-launcher.template.sh:704`.
3. **What would show it wrong.** Candidate verifier substitution, a replayed approval covering a new HOLD, or signing after stale evidence would defeat the trust boundary. -- `bootstrap/tests/_gate_manifest.py:666`; `bootstrap/tests/test_repin_ceremony.py:381`.

The strongest design choice is keeping signed prior authority separate from
candidate evidence and retaining two distinct bridge ceremonies. C1 explicitly
requires full collection before signing with the key away; Scope avoids making
installation a prerequisite for its own verifier. Host-capable candidate tests
remain an admitted limitation, not an isolation claim.

**S1 — Blocking: authenticate the verifier that actually checks HOLDs.** C1
names P's `_gate_preflight.py`, the E7 scanner, but omits P's
`_gate_manifest.py`, which performs the prior-manifest verification. Authenticating
one does not authenticate the other. **Satisfier:** name and independently check
both tools and their required dependency bytes from immutable signature-verified
P, together with P's manifest. Require the prepared public command to invoke
P's manifest verifier on a separately clean, exact C target, with immutable P
for both trusted/anchor references, the verified trusted repository,
`--require-anchor`, full collection and the runbook's empty environment and
Python `-E -s`. Test substituted verifier/manifest and omitted collection or
anchor settings through that command with passing controls; preserve independent
E7. This agrees with ordinary F1. -- C1; `bootstrap/REANCHOR_RUNBOOK.md:74`;
`bootstrap/tests/_gate_manifest.py:666`.

**S2 — Blocking: specify stale-evidence and recovery refusals.** “Mutation of
… disposition” does not establish what a reusable approval authorizes or whether
rerunning after a stop can reuse it. **Satisfier:** map public-entry controls
proving dispositions name exact displayed items and bind P, C and the verified
report/collection; changed evidence or a new/unexplained HOLD requires fresh
review and disposition before signing. Map packet, launcher and package/report
substitution between stages, and interrupted/fresh-package reruns, to explicit
refusal cases. Preserve raw-object extraction, path containment and symlink
refusal in preparation and demonstrate those guards with controls. Reuse the
existing package-rewrite, launcher-revalidation and safe-extraction cases;
these detect mistakes without claiming containment against code running as the
operator. -- C1–C3; `scripts/repin.py:168`;
`bootstrap/tests/test_repin_ceremony.py:381`, `:1054`;
`bootstrap/tests/test_repin.py:324`, `:953`.

**Covered:** claims/reuse/drift (1,5,6): committed `git grep` for `boot`,
`verify`, `scan-digest`, cited prior tools and runbook; public paths,
completeness/refusal (2–4): cited launcher, verifier and tampering tests;
lifecycle (7): C4 and runbook's two bridges; scope/domain (8): accepted source
contract and trust-plan installation boundary; satisfiers (9): S1–S2.
**Not covered / low confidence:** source inspection only; no implementation,
tests, mutations, actual signing, ref movement, certification or push performed.
This review authorizes no ceremony and claims no protection from same-user
compromise.

## Response to plan review -- Codex (gpt-6.1-terra) -- 2026-10-29

| Finding | Disposition | Operative cells |
|---|---|---|
| F1, S1 | Accepted | C1, C3 and Verification distinguish authenticated verifier and scanner and test the human trigger. |
| F2 | Accepted | C1–C2 specify preparation, independent checks and complete operator workflow. |
| F3 | Accepted | Verification maps callers, existing nodes, new public-entry tests and consumers. |
| S2 | Accepted | C1–C3 bind dispositions and require tamper, extraction and recovery controls. |

## Implementation verification -- Codex (gpt-6-luna) -- 2026-10-29

**C1 commit**: `efcc3a46ef7072ec8a832d8259ed2119f79a4bad` (range `b6eae8655a3ede9083f3e59beaa2718fb1ea20d8..efcc3a46ef7072ec8a832d8259ed2119f79a4bad`). The tested C1 bytes are the committed bytes. Canonical interpreter: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13). Before the C1 commit, its three claimed source paths were the only tracked changes; after commit they are clean. The unrelated untracked `.claude/` and `dev/measurement/collision_log.md` were preserved.

**Maintainer direction** (2026-10-29):

> Well, also with the runbook it should just point to scripts

C1 adds and documents the prior-verifier entrypoints, while retaining the working interim ceremony checks. C2 must provide the remaining reusable ordinary and transition ceremony paths before the runbook can become pointer-only; no C2 capability is claimed here.

**Boundary A mode**: bounded for C1 preparation and full-verifier evidence. `bootstrap/tests/test_repin_ceremony.py -q`: 142 passed in 459.17s. This includes direct P CLI comparison for pass and HOLD, independent wrong-fingerprint refusal, P/observer/target tamper refusal, stale disposition refusal, ordinary collection additions, protected marker HOLDs, and stale/malformed/multiple/error capture controls. `bootstrap/tests/test_repin.py::test_a_tracked_symlink_or_submodule_refuses_before_import`, `::test_a_symlinked_target_or_parent_is_not_followed`, `::test_the_apply_step_makes_no_commit_and_stops`: 4 passed. Runbook/page/parser nodes: 8 passed. Additional C1 controls: 10 passed. `py_compile`, `claim_check`, `git diff --check`, `check_cairn.py` (187 Markdown), `link_check.py` (187 Markdown), `sync_doc_snippets.py --check` (423 docs), and neutrality (0 failures) passed.

One earlier normal sandbox run reported 133 passed and 5 failures: four stale wording assertions were corrected without removing their safety semantics; the stage-two fixture failed to supply its dummy passphrase. That stage-two node also failed from an archived pre-C1 `HEAD` under the same sandbox, passed when rerun with host PTY/signing access, and passed within the final 142-test family run. A separate temporary encrypted-key check confirmed local signing capability. This is retained as evidence, not an outstanding C1 failure. No full-suite or `CAIRN_FULL_SUITE` run was made. C2, wide Boundary B on the final SHA, independent code/Security Reviews, and C4 remain open.

## C2 scratch-anchor probe -- Codex (GPT-6.1 Sol) -- 2026-10-29

This probe checks existing public ceremony paths using the test fixture's
throwaway signed anchor and key. The fixture creates a scratch repository under
pytest's temporary directory. Its ref movement cannot change the shared
checkout. This does not compare or reconcile P443 history.

**Tested commit**: `83444e568ea215f6e6b8dc7451a15b2f2a399590`. No implementation
bytes changed for this probe; it is progress evidence, not C2 completion or
Boundary B.

**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(Python 3.13.13).

**Pre-run state**: no tracked changes; unrelated untracked `.claude/` and
`dev/measurement/collision_log.md` were present and preserved. **Post-run
state**: same tracked and untracked state.

| Command | Exit | Outcome | Elapsed |
|---|---:|---|---:|
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q bootstrap/tests/test_repin_ceremony.py::test_a_full_ceremony_signs_once_with_the_typed_passphrase bootstrap/tests/test_repin_ceremony.py::test_transition_packet_uses_signed_prior_authority_and_preserves_ordinary_refusal` | 0 | 2 passed | 10.90 s |

The first node signs and advances only the fixture's scratch anchor. The second
confirms ordinary packet refusal and transition packet/reader-input preparation
against a signed fixture anchor; it does not sign or install a transition. No
real key, live ref, push, old-HOLD disposition, bridge installation, full-suite
run, or certification was performed. The runbook still requires the separate
bridge paths, and the newer v0.6 forward-baseline direction still needs a
lifecycle-aligned scope decision before further transition-specific code.

**Applicable prose gates**: `claim_check.py` passed for this plan; `link_check.py`
scanned 192 Markdown files with no issues (84 external links were not probed);
`sync_doc_snippets.py --check` scanned 428 documents with no drift; neutrality
reported 0 failures and 43 information rows. `check_cairn.py` exited 1 for an
imperative-override phrase at line 100 of the unrelated
`dev/proposals/2026-10-29-codex-dispatcher-content-scan.md`; I left that file
untouched. Searching `bootstrap/tests` found no test reading this plan; the
same search matched this plan as its positive control.

## Scope amendment -- Codex (GPT-6.1 Sol) -- 2026-10-29

The Maintainer directs the plans to finish before the v0.6 baseline. The
following supersedes conflicting historical-transition and installation gates
above; the earlier record remains intact.

> “They can each build the machinery, the new baseline does not need to be part of their plans. It can be a work board item for v0.6.”
>
> “If you want, build an anchor now to test that their machinery works properly. I'm okay either way. Remember: correctness of function is what matters, not of the trust root itself.”
>
> “Remove those requirements from the plans”

**Scope delta**: degraded. **Disposition**: defer to the v0.6 board item:
actual signing and installation, historical-anchor comparisons and reconciliation,
and actual disposition of the 83 candidate reports. These are no longer
archive prerequisites. The loss is evidence about the historical anchor and
real installation within this plan; cutting those steps follows the Maintainer's
sequencing rather than specifying them here.

C1–C3 still build the reusable machinery and functionally test its authentication,
bindings, refusal paths and ceremony commands using suitable scratch authority.
The tests and independent code and Security Reviews remain required; a scratch
anchor is optional as a means, not a real trust root. Historical bridge-specific
comparisons and authorizations are not required to archive. No actual signing,
ref installation or push is authorized by this amendment.
