# Plan: Align work-intent guidance with behavior

**Source proposal**: dev/proposals/archive/2026-10-29-codex-intent-guidance.md
**Status**: ready-to-implement
**Plan review**: required(Internal + Internal Security Review)
**Assurance path**: high-assurance
**Opened**: 2026-10-30
**In brief**: Make work-intent guidance match the existing conflict check and identity handling.

## Source proposal

The accepted revised contract corrects guidance and parent CLI help without changing enforcement or identity behavior. Its prior C2 coordination choice predates the incident; the Maintainer judges its bearing on the doctrine-evolution gate.

## Scope

Correct `doctrine/coordination.md`, `dev/agent_collaboration.md`, `dev/modules/coordination-tiers.md`, `templates/modules/team-gated/coordination-tiers.md`, and help in both `tools/_intent/cli.py` and `templates/modules/team-gated/_intent/cli.py`. Search related current descriptions and correct directly relevant contradictions, including shipped counterparts where applicable. Preserve behavior. Search tests and manifests for every changed surface, with a known hit as control; record owners and omissions.

**Reuse.** `rg -n 'intent|coordination-tiers' bootstrap/tests` finds `bootstrap/tests/test_intents_tool.py` and installed-module tests. Extend existing real-entry-point tests and use existing identity, conflict and hook implementations; the source and shipped CLI are intentional twins.

### Documentation / doctrine surface

The coordination doctrine and module prescribe cooperation; collaboration guidance describes the team workflow. Route changes by `docs/DOCUMENTATION_PLAN.md`. Before editing doctrine, establish and record the applicable trigger under `doctrine/rationale.md` > How the doctrine evolves under evidence. If not established, stop for Maintainer resolution. The shipped CLI is listed in `bootstrap/tests/fixtures/protected_test_roster.json`; determine the applicable frozen boundary and record the owed gate-manifest ceremony, without self-authorizing a re-anchor.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Correct guidance and help; add targeted evidence | Both plan reviews; doctrine gate before doctrine edit | Guidance, shipped copies, help and tests |
| C2 | Verify committed implementation and hand to code review | C1 complete | Change-verification record and review handoff |

## Acceptance criteria

### C1

Explain opt-in hooks, default block only for fresh overlapping claims with a session token and differing resolved label, warnings for unclaimed and stale paths, tokenless withholding of cross-claim blocking, and existing warn and confirm modes. `CAIRN_ALLOW_UNCLAIMED` and `solo_mode` also prevent blocking while retaining the other-session warning. Use the same session-specific label for claim, commit and inherited auto-release; manual release uses claim ID and does not authenticate ownership. Prefer harness identity and compare `whoami` in relevant environments for diagnosis. A synthetic example sets a distinct override separately in each fresh shell that needs it, including the commit; an override alone supplies no token. Warn that shared labels can hide conflicts and that labels and logs are cooperative, not authentication. Keep copies aligned and change no hook or identity behavior.

S2: assert corrected parent help in both copies under Python 3.13.x; in disposable copies restore `warn-by-default` independently in each and show the assertion fails, with unmutated controls. S3: the mapped tests and gates below are human-run during C1 and C2. No automatic prose-accuracy control is claimed.

### C2

Record the clean tested SHA and range, interpreter, pre/post state, commands, counts, timings, non-pass dispositions, omissions and ceremony obligation. Hand the implementation and evidence to independent code review.

## Scope delta

**Scope delta**: preserved

## Verification

Boundary A runs the mapped checks during iteration; Boundary B repeats them on the final clean commit in **wide** mode because this changes governing and installed contracts. Use canonical Python 3.13.x and record `Certified by: pending`. No full certification is implied.

* `bootstrap/tests/test_intents_tool.py`: real `whoami`, claim, pre-commit and post-commit paths, default modes, no-token, same-label, stale and unclaimed cases, and `CAIRN_ALLOW_UNCLAIMED` and `solo_mode` warning-without-block exemptions; add real parent-help assertions for both copies and the reverse mutation above. Exercise manual release by ID separately. Check source/twin parity and the installed entry point.
* `bootstrap/tests/test_coordination_broad_intent.py`, `bootstrap/tests/test_upgrade_module_additions.py`, `bootstrap/tests/test_review_sweep_ships.py`, and `bootstrap/tests/test_review_stance_in_shipped_files.py`: installed module and collaboration readers. Search all changed paths in tests and manifests again, with a known match as control, and add actual owners and public paths found. Split pytest selections within the guard limit and reconcile the union.
* Compare final guidance by hand with `tools/_intent/identity.py`, `tools/_intent/conflict.py`, `tools/_intent/hooks.py` and release commands in `tools/_intent/cli.py`, including both exemptions and inherited environments; record each comparison and discrepancies corrected. Search current related descriptions with `rg -n -i 'warn.by.default|block.by.default|work.intent|CAIRN_ALLOW_UNCLAIMED|solo_mode' doctrine dev/modules templates/modules tools`, first confirming a known match in `tools/_intent/cli.py`; inspect matches and record corrections and omissions.
* Run `python scripts/claim_check.py` on changed documents, `python scripts/check_cairn.py`, `python scripts/link_check.py`, `python scripts/sync_doc_snippets.py` in check mode if supported, and `python scripts/quality_gate.py --sub neutrality --sub redundancy`; establish the snippet command's actual mode before running it. Record any omissions and resolve missing required coverage before handoff.
* Record frozen-file changes for the existing Maintainer-run gate-manifest re-anchor ceremony under `bootstrap/REANCHOR_RUNBOOK.md`; do not treat a green suite as re-anchoring. Boundary C belongs to the independent code reviewer, who challenges the verification record and runs targeted falsification.


## Plan review -- Codex (GPT-6) -- 2026-10-30

Reviewed commit: e5d6f6d5e31f35414842ca320f8eab932fe12b0a
Target: operative plan and accepted revised proposal
Prior findings: none
Assurance path: high-assurance

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** The plan carries the conditional default, parent help, shipped twins and release-by-ID, but its verification does not require the accepted comparison of final statements to the implementation -- `dev/proposals/archive/2026-10-29-codex-intent-guidance.md`, final current contract; `dev/plans/2026-10-30-intent-guidance.md`, Verification.
2. **Best alternative.** Keep the existing targeted tests and add a documented, human-run comparison and controlled search rather than constructing a prose checker -- `tools/_intent/identity.py`, `tools/_intent/conflict.py`, `tools/_intent/hooks.py`.
3. **What would show it wrong.** A final statement that passes the mapped tests while misstating a mode, an exemption, or an identity environment would show the mapping cannot establish the accepted outcome -- `bootstrap/tests/test_intents_tool.py`, enforce-mode and identity tests.

**IGP1 -- blocking: map the accepted prose comparison and reader search.** C1 specifies what the prose must say, and the test mapping exercises behavior, but neither requires comparing the resulting wording with the actual identity resolver, conflict decision and hook lifecycle. Existing behavioral tests can pass even when new prose misdescribes them; the parent-help assertion covers only that one help phrase. The accepted contract also requires searching current related descriptions using a known matching phrase as a positive control, whereas the plan specifies a controlled search only for tests and manifests. Add both human-run checks to the reviewed mapping, name the sources and positive control, and record their results and any contradictions corrected. This preserves the accepted scope and does not require an automated prose check.

**Coverage:** Read the committed plan, accepted proposal and review history, parser help declaration, and relevant existing test descriptions. No tests or mutations were run; this review did not independently inspect every installed reader or the Security Review obligation.


## Plan review -- Codex (GPT-6), Security -- 2026-10-30

Reviewed commit: b3276604c431de43f5f427214c8593ed64c9d1c8
Target: operative plan against accepted revised contract and existing security boundaries
Prior findings: IGP1 remains an author obligation
Assurance path: high-assurance

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** The plan preserves the accepted cooperative boundary and both shipped copies, but its explicit acceptance and verification mapping omit two existing exemptions from blocking -- `tools/_intent/conflict.py::_precommit_check_impl`.
2. **Best alternative.** Keep the narrow correction and record a human comparison of final guidance with the decision branches, including exemptions, rather than introduce authentication or a prose checker -- `tools/_intent/identity.py::resolve_session_token`; `tools/_intent/conflict.py::_precommit_check_impl`.
3. **What would show it wrong.** Guidance implying that a token and a fresh differently labelled claim necessarily cause refusal would be false when an exemption is set, even though the overlap warning remains -- `tools/_intent/conflict.py::classify_precommit_warnings`, `_precommit_check_impl`.

**IGPS1 -- blocking: explicitly map the existing enforcement exemptions.** C1 and the test mapping enumerate token, label, freshness and mode conditions, but not `CAIRN_ALLOW_UNCLAIMED` or `solo_mode`. The actual decision returns success for either exemption before enforcing a fresh cross-claim; it still emits the other-session warning. This matters because the first name sounds limited to unclaimed paths. Add these existing exemptions and their warning/block distinction to the required final-text comparison and affected test mapping. Preserve their present behavior and avoid an unconditional assurance that distinct fresh claims block. This is a concrete part of IGP1's missing comparison, not a request for a new control or wider enforcement design.

The remaining security treatment is adequate as planned: identity resolution keeps overrides separate from token availability, same-label suppression is acknowledged as cooperative, manual release is by ID, and auto-release inherits the committing environment. Evidence: `tools/_intent/identity.py::resolve_agent_identity`, `resolve_session_token`; `tools/_intent/conflict.py::other_session_overlaps`; `tools/_intent/cli.py::_cmd_release`, `_cmd_auto_release`; `tools/_intent/hooks.py::_build_hook_block`. C1 maps independent reverse help mutations in both intentional CLI twins; Verification retains installed paths and the owed frozen-file ceremony, matching `bootstrap/tests/fixtures/protected_test_roster.json`. The doctrine gate is a stop condition rather than assumed authority. IGP1 must also be folded: behavior tests alone cannot establish that final prose describes these paths accurately.

**Coverage:** Read committed plan, accepted revised proposal and Decision, current plan template and review rules, identity/conflict/release/hook paths, existing test descriptions and protected roster. Covered claims, public paths, failure/exemption behavior, drift, scope and lifecycle placement through those sources. No tests, mutations, hook installation, certification, original-incident reproduction or exhaustive reader search performed. Implementation evidence and final prose remain future author obligations; this pass supplies no re-anchor or doctrine authorization.

## Response to plan reviews -- Codex (GPT-6) -- 2026-10-30

| Finding | Disposition |
|---|---|
| IGP1 | Accepted; Verification maps the human comparison and controlled related-description search, including recorded corrections. |
| IGPS1 | Accepted; C1 and Verification name both exemptions and their warning-without-block behavior. |
