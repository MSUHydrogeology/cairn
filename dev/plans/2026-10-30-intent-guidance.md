# Plan: Align work-intent guidance with behavior

**Source proposal**: dev/proposals/archive/2026-10-29-codex-intent-guidance.md
**Status**: awaiting-code-review
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

## Implementation note -- Codex (GPT-6) -- 2026-10-30

The C1 acceptance text names `CAIRN_ALLOW_UNCLAIMED`; the implemented public
variable is `CAIRN_INTENT_ALLOW_UNCLAIMED` (`tools/_intent/conflict.py`,
`ALLOW_UNCLAIMED_ENV_VAR` and `_precommit_check_impl`). Guidance and checks use
the actual name. This is a factual identifier correction only; enforcement and
accepted scope are unchanged.

The doctrine-edit gate is met as a correction to the recorded Maintainer
choice, not a rule inferred from the incident. The C2 coordination choice in
`dev/plans/archive/2026-10-28-governing-text-single-source.md` records the
Maintainer's words: “Blocking for live-session conflicts, yes. Agents should
claim intent prior to editing.” That choice predates the incident, and the
accepted proposal identifies this correction as implementing it.

## Implementation verification -- Codex (GPT-6) -- 2026-10-30

**Boundary B mode**: wide
**Certified by**: pending
**Tested commit**: be41b61ed62168c5a0a034827c1d43457caf6cff
**Reviewed range**: 82b08e8eb2ba215e846e1275436336691cf62a7d .. be41b61ed62168c5a0a034827c1d43457caf6cff
**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` -- Python 3.13.13
**Pre-run state**: clean at tested commit
**Post-run state**: clean; same tested commit

| Command | Exit | Outcomes | Elapsed |
|---|---:|---|---:|
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest` on the five mapped files below, `-q` | 0 | 860 passed | 28.80 s |
| `scripts/claim_check.py` on the five changed Markdown files (five invocations) | 0 | All five clean | <0.01 s each |
| `scripts/link_check.py` on the five changed Markdown files | 0 | No issues | <0.01 s |
| `scripts/sync_doc_snippets.py --check` on the five changed Markdown files | 0 | No drift | <0.01 s |
| `scripts/check_cairn.py` | 0 | 198 Markdown files clean; 83 external links not probed | 2.15 s |
| `scripts/quality_gate.py --sub neutrality --sub redundancy` | 0 | 0 failures; 43 neutrality info, 1 redundancy info | 1.07 s |
| Disposable parent-help controls and reverse mutations, source and shipped copies | 0 | Both controls passed; both restored `warn-by-default` mutants killed | 0.30 s |
| Controlled `rg` searches for related descriptions and test/manifest readers | 0 | Positive controls matched; no further direct contradictions | 0.10 s |

The pytest selection was `bootstrap/tests/test_intents_tool.py`,
`bootstrap/tests/test_coordination_broad_intent.py`,
`bootstrap/tests/test_upgrade_module_additions.py`,
`bootstrap/tests/test_review_sweep_ships.py`, and
`bootstrap/tests/test_review_stance_in_shipped_files.py`. It covers the real
identity, claim, hook, mode, exemption, stale-claim, release-by-ID, installed
module, and collaboration-reader paths. No full-suite certification was run
for this commit.

**Plan-specific acceptance commands and comparison.** `cmp -s` passed for the
development/shipped coordination-tier pair and for the source/shipped CLI pair.
The help search used `tools/_intent/cli.py` as its positive control before
searching `doctrine`, `dev/modules`, `templates/modules`, and `tools`; the test
search used `test_intents_tool.py` as its positive control before scanning the
test tree and both gate fixtures. The protected roster lists
`bootstrap/tests/test_intents_tool.py` and
`templates/modules/team-gated/_intent/cli.py`; the existing Maintainer-run
gate-manifest re-anchor ceremony remains owed under `bootstrap/REANCHOR_RUNBOOK.md`.

The final wording was compared with `tools/_intent/identity.py` identity and
token resolution; `tools/_intent/conflict.py` mode, freshness, overlap, and
exemption decisions; `tools/_intent/hooks.py` inherited commit environment;
and `tools/_intent/cli.py` claim, manual release, and auto-release paths. The
comparison confirms that the per-session token gates blocking, resolved labels
are compared only when a token exists, both exemptions retain overlap warnings,
manual release is by claim ID, and post-commit release follows the committing
session's resolved label. The searches caught the former warn-only/default
claims, the missing opt-in condition, and the legacy-only config wording; these
were corrected in the source and shipped guidance. The plan's bypass variable
typo is recorded in the implementation note above. Remaining incident-tracker
references describe impact logging, not alternate enforcement behavior.

**Non-pass disposition**: An earlier `check_cairn.py` at provisional commit
3b3738c4 reported a missing suite-log path in an unrelated strategy note. The
reference was repaired in 85a9b6d2; the final clean run above passed. An
initial Python 3.12.9 test attempt was interrupted and is excluded as evidence.

**Known omissions**: The 83 external links are not fetched by the doc checker.
No certifying full-suite run or gate-manifest re-anchor was performed; the
certificate remains pending and the Maintainer owns the ceremony.

## Code review -- Codex (GPT-6) -- 2026-10-30

Reviewed commit: 394aaf3c24b8bd7b8a3f409cc2af35e3341b68a7
Implementation: 82b08e8e..be41b61e; verification: 394aaf3c
**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Bounding**: ACCEPTED

**Foundations**

1. **Does it do what it claims?** The guidance describes the conditional block, exemptions, identity and release paths implemented by `tools/_intent/conflict.py::_precommit_check_impl`, `other_session_overlaps`, and `tools/_intent/cli.py::_cmd_release` and `_cmd_auto_release`; the two CLI and module copies match at the tested commit.
2. **Best alternative.** Retain the human comparison and real-entry-point help assertion: a prose checker would not establish the behavioral statements, while the help assertion checks both published entry points (`bootstrap/tests/test_intents_tool.py::TestIntentParentHelp`).
3. **What would show it wrong?** A mode, exemption, identity or shipped-help counterexample would break the claim; the falsification ledger below records the challenges made.

**Falsification ledger.** In a fresh detached local clone at 394aaf3c, Python 3.13.13 ran targeted real-entry-point identity, release, exemption, stale-claim, auto-release and parent-help cases: 9 passed, 125 deselected. The unmutated parent-help case passed in that control. Replacing the corrected parent-help phrase with `warn-by-default` in `tools/_intent/cli.py` killed the source mutant (1 assertion failure); independently replacing it in `templates/modules/team-gated/_intent/cli.py` killed the shipped mutant (1 assertion failure). Each mutant was reset before the other. The tests and mutations ran only in the disposable copy. I compared the verification record with the range, the identity and conflict branches, and the manual and automatic release commands; the record names its interpreter, tested commit, coverage, omissions and pending ceremony.

**Coverage:** Examined the changed guidance and help, acceptance criteria, implementation branches and verification record. Targeted checks did not exercise every enforce mode or independently reproduce the full mapped selection; the implementation record supplies those results. No full suite or re-anchor was run. This ordinary pass does not discharge the separate Security Review.

## Code review -- Codex (GPT-6), Security -- 2026-10-30

Reviewed commit: 0b7aeedf
Target: intent-guidance implementation 82b08e8e..be41b61e and verification at 394aaf3c; unrelated interleaved changes excluded
Prior findings: none
Assurance path: high-assurance
**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none
**Bounding**: ACCEPTED

**Foundations**

1. **Does it do what it claims?** The guidance makes enforcement conditional, names both exemptions and warns that labels are cooperative; these match the actual token gate, label comparison and exemption branches -- `tools/_intent/conflict.py::_precommit_check_impl`, `other_session_overlaps`; `tools/_intent/identity.py::resolve_session_token`.
2. **Best alternative.** Preserve the narrow guidance correction and explicit limitations; adding authentication would change the accepted contract, while the existing manual-release command intentionally accepts a claim ID without owner authentication -- `tools/_intent/cli.py::_cmd_release`, `_cmd_auto_release`.
3. **What would show it wrong?** A token-bearing solo commit that blocks, a suppressed cross-label warning under bypass, or a shared label still being distinguished would contradict the guidance -- see the falsification ledger below.

**Falsification ledger.** All execution used a fresh detached local clone of 0b7aeedf under `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13). A detached worktree could not be created because Git administration writes were denied; the local clone supplied an independent checkout instead. The shared checkout was not used for probes.

* **Surfaces and edge attempts:** An independent real-CLI matrix created five fresh temporary Git repositories, claimed the same path under one token/label, then staged it under a different token. The unmodified control refused with exit 1 and an overlap warning. Canonical `solo_mode: true` returned 0 and retained that warning. A nonempty `CAIRN_INTENT_ALLOW_UNCLAIMED=0` also returned 0 and retained the warning: this is presence-based, not a Boolean parser. Reusing the claimant's label with the different token returned 0 and suppressed the overlap warning, demonstrating the documented identity limitation. Headless `confirm` refused with exit 1 and retained the warning. Each result was asserted through `tools/intent.py _precommit_check` on the staged path; no engine mutation was needed.
* **Verification:** Targeted pytest selection in `bootstrap/tests/test_intents_tool.py` covering `TestEnforceModeAndN1`, `test_solo_mode_suppresses_self_not_other`, `TestManualRelease`, `test_no_token_collision_records_no_incident`, and `test_confirm_ack_records_occurred`: 10 passed, 124 deselected, 1.63 s. Byte comparisons passed for source/shipped CLI and development/shipped coordination guidance. The independent matrix passed all five cases in 0.62 s.
* **Record and trust boundary:** The implementation record identifies the committed bytes, wide mapping, interpreter, outcomes, omissions and pending certificate. The guidance accurately separates label override from token availability, manual release from authentication, and hook opt-in from installation. The source and shipped CLI changes affect help, not enforcement. The frozen-file ceremony remains owed; this pass does not authorize re-anchoring.
* **Residual risk:** Cooperative identity can be spoofed or shared and the hook intentionally fails open on internal error. These are stated limits, not new safeguards supplied by this change. No full-suite certification, re-anchor, historical-incident reconstruction, exhaustive test rerun or new help mutation was performed; the ordinary review records independent mutations of both help copies.

**Coverage -- covered:** Claims, failure/exemption modes and public paths through the five-case real-CLI matrix and targeted tests above; identity and release boundaries through `tools/_intent/identity.py`, `tools/_intent/cli.py` and `tools/_intent/hooks.py`; consistency and drift through the committed doctrine/module/collaboration wording and byte comparisons; lifecycle and scope through the plan's accepted contract, verification and pending ceremony. **Not covered / low confidence:** adversarial log tampering, all malformed-config combinations, unrelated interleaved implementation, external links, and Maintainer-run trust ceremonies.
