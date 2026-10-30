# Plan: Align work-intent guidance with behavior

**Source proposal**: dev/proposals/archive/2026-10-29-codex-intent-guidance.md
**Status**: awaiting-plan-review
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

Explain opt-in hooks, default block only for fresh overlapping claims with a session token and differing resolved label, warnings for unclaimed and stale paths, tokenless withholding of cross-claim blocking, and existing warn and confirm modes. Use the same session-specific label for claim, commit and inherited auto-release; manual release uses claim ID and does not authenticate ownership. Prefer harness identity and compare `whoami` in relevant environments for diagnosis. A synthetic example sets a distinct override separately in each fresh shell that needs it, including the commit; an override alone supplies no token. Warn that shared labels can hide conflicts and that labels and logs are cooperative, not authentication. Keep copies aligned and change no hook or identity behavior.

S2: assert corrected parent help in both copies under Python 3.13.x; in disposable copies restore `warn-by-default` independently in each and show the assertion fails, with unmutated controls. S3: the mapped tests and gates below are human-run during C1 and C2. No automatic prose-accuracy control is claimed.

### C2

Record the clean tested SHA and range, interpreter, pre/post state, commands, counts, timings, non-pass dispositions, omissions and ceremony obligation. Hand the implementation and evidence to independent code review.

## Scope delta

**Scope delta**: preserved

## Verification

Boundary A runs the mapped checks during iteration; Boundary B repeats them on the final clean commit in **wide** mode because this changes governing and installed contracts. Use canonical Python 3.13.x and record `Certified by: pending`. No full certification is implied.

* `bootstrap/tests/test_intents_tool.py`: real `whoami`, claim, pre-commit and post-commit paths, default modes, no-token, same-label, stale and unclaimed cases; add real parent-help assertions for both copies and the reverse mutation above. Exercise manual release by ID separately. Check source/twin parity and the installed entry point.
* `bootstrap/tests/test_coordination_broad_intent.py`, `bootstrap/tests/test_upgrade_module_additions.py`, `bootstrap/tests/test_review_sweep_ships.py`, and `bootstrap/tests/test_review_stance_in_shipped_files.py`: installed module and collaboration readers. Search all changed paths in tests and manifests again, with a known match as control, and add actual owners and public paths found. Split pytest selections within the guard limit and reconcile the union.
* Run `python scripts/claim_check.py` on changed documents, `python scripts/check_cairn.py`, `python scripts/link_check.py`, `python scripts/sync_doc_snippets.py` in check mode if supported, and `python scripts/quality_gate.py --sub neutrality --sub redundancy`; establish the snippet command's actual mode before running it. Record any omissions and resolve missing required coverage before handoff.
* Record frozen-file changes for the existing Maintainer-run gate-manifest re-anchor ceremony under `bootstrap/REANCHOR_RUNBOOK.md`; do not treat a green suite as re-anchoring. Boundary C belongs to the independent code reviewer, who challenges the verification record and runs targeted falsification.
