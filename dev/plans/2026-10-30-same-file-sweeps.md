# Plan: Detect and record same-file sweeps

**Source proposal**: dev/proposals/archive/2026-10-29-codex-same-file-sweeps.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Assurance path**: high-assurance
**Opened**: 2026-10-30
**In brief**: Help shared-tree authors avoid misattributed commits and count confirmed sweeps honestly.

## Source proposal

The accepted revision extends existing commit inspection with agreed serialization, defines a confirmed sweep and one countable event per commit, and makes the advisory gate's incomplete reporting explicit. Its Security preflight and residual limitations remain part of the contract.

## Scope

Update `AGENTS.md`, `doctrine/coordination.md`, `dev/modules/coordination-tiers.md`, `templates/modules/team-gated/coordination-tiers.md`, tracker guidance in `templates/modules/default-on/incident-trackers.md` and `templates/modules/default-on/incident_log_template.md`, and advisory output in `tools/evolution_infer.py` and `templates/modules/default-on/evolution_infer.py`. Search for other installed owners and consumers and keep corresponding copies aligned. Reconcile the local `dev/measurement/collision_log.md` without overwriting it; do not invent confirmation. No attribution detector or claim-release change.

**Reuse.** `rg -n 'collision_log|same.file|evolution_infer|coordination.md' tools bootstrap/tests doctrine/coordination.md AGENTS.md` found the existing gate, tracker and tests; extend them rather than build a detector. The two gate scripts are intentional installed counterparts.

### Documentation / doctrine surface

Coordination prescription belongs in governing doctrine and installed coordination guidance; tracker and output describe reporting. Apply `docs/DOCUMENTATION_PLAN.md`. Before doctrine edits establish the trigger under `doctrine/rationale.md` > How the doctrine evolves under evidence; if not established, stop for Maintainer resolution. The shipped gate and its tests are listed in `bootstrap/tests/fixtures/protected_test_roster.json`; record the applicable gate-manifest ceremony and do not self-authorize re-anchoring.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Update guidance, gate output, focused checks and local incident reconciliation | Both plan reviews; doctrine trigger before doctrine edits | Aligned guidance and gate copies, tests, local report if evidence permits |
| C2 | Verify and hand to code review | C1 complete | Change verification and review handoff |

## Acceptance criteria

### C1

Agree serialization before inspecting shared paths through commit; claims alone are not agreement. Inspect tracked candidates against HEAD, including staged and unstaged bytes, and new files directly; reinspect changed bytes. Stop on foreign or uncertain content and coordinate; use separate worktrees when agreement cannot hold. State that noncooperating writers can defeat this procedure.

A confirmed sweep requires author confirmation or recorded provenance, not a claim or diff alone. Record one `occurred` row per commit with paths together, occurrence and discovery dates, and a minimal confirmation reference; check for an existing row. Unknown authorship or occurrence date remains uncertain and uncounted; prevented cases remain separate. Reconcile `5094a977` only if confirmed, preserving the local tracker. Keep evidence local; screen committed summaries for sensitivity and exclude private conversations, secrets and unrelated uncommitted text.

The real gate suggests two in-window confirmed commits, including one with two paths, but not one commit or a prevented case; late discovery uses occurrence date. Human and JSON output identify incomplete reporting and remain advisory. Demonstrate staged foreign content, changed bytes requiring reinspection, and legitimate separately authored integration without inventing attribution.

S2: change one of two occurred impacts to prevented and show the threshold finding disappears, with an unmutated control. S3: the human runs the mapped tests and gates below; inspection and confirmation remain human judgments.

### C2

Record the clean tested SHA and range, interpreter, pre/post state, commands, outcomes, timing, non-pass dispositions, omissions and ceremony obligation; hand to independent code review.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A runs the mapping below during iteration; Boundary B repeats it on the final clean commit in **wide** mode for governing and installed contracts, under canonical Python 3.13.x, with `Certified by: pending`. No full certification is implied.

* `bootstrap/tests/test_evolution_infer.py` exercises the real gate and installed counterpart, threshold, dates, output and mutation; extend focused entry-point tests for the accepted scenarios. Check source/copy parity and session consumer output in `bootstrap/tests/test_session_binding_gate_and_printing_hold.py`.
* `bootstrap/tests/test_incident_trackers_module.py`, `bootstrap/tests/test_coordination_broad_intent.py`, `bootstrap/tests/test_upgrade_module_additions.py` and `bootstrap/tests/test_review_sweep_ships.py` cover tracker and installed guidance. Search each changed path in tests and manifests with a known hit as control; add actual readers and public paths found. Split selections within the guard limit and reconcile their union.
* Exercise the prescribed inspection in a disposable repository with staged foreign content and an intervening change, and a legitimate separately authored integration; document observations and confirmation limits. Inspect local reconciliation for duplication and sensitive content without publishing it.
* Run `python scripts/claim_check.py` on changed documents, `python scripts/check_cairn.py`, `python scripts/link_check.py`, applicable snippet checks and `python scripts/quality_gate.py --sub neutrality --sub redundancy`. Establish snippet check mode before use. Resolve any missing required coverage before handoff.
* Record frozen-file changes for the Maintainer-run ceremony in `bootstrap/REANCHOR_RUNBOOK.md`. Boundary C is independent targeted falsification by the code reviewer.
