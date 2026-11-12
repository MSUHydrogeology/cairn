# Plan: Install a project-owned rules starter

**Source proposal**: dev/proposals/archive/2026-11-12-terra-rules-router-stub.md
**Status**: revising-plan
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-12
**In brief**: Give adopters a small rules starter while preserving the rules they already own.

## Build summary

Add one short template to the existing core install set. Keep project rules
editable without integrity re-attestation, preserve existing files and deliberate
deletion, and explain the existing collision-recovery workflow. No new command,
configuration format or release ceremony is added.

## Source proposal

The Maintainer accepted the clarified heavy proposal at `5ba9ad64` with
“Accept and prepare the plan.” Both proposal reviews accepted it. This plan
delivers its complete agent-owned outcome; release signing remains separate.

## Scope

Add `templates/core/RULES.md` through `core/RULES.md` in `_CORE_MAPPINGS` in
`bootstrap/_scaffold/config.py` and `RULES.md` to the authoritative
`_LIVING_STATE_DSTS` in `bootstrap/_scaffold/lockfile.py`. Keep it a normal
mergeable core record with the existing raw-template ancestor and source
attestation; a lockfile's own flag never grants an exemption.

The starter tells teams to keep concise project rules and routes there. It
adds no project-specific policy. Normal install preserves an existing file;
explicit `--force` retains its documented overwrite behavior. Upgrade uses
the existing new-core collision staging and digest-bound adoption flow to keep
an untracked regular rules file as a fork. Unsafe destinations retain existing
refusals. A tracked deleted rules file stays tracked and absent; use the existing
missing-file review path, not a newly synthesized addition or automatic restore.
Do not introduce a new deletion state or general preservation framework.

**Reuse.** Source inspection found the changelog's core mapping, living-state
allowlist, normal-install preservation, collision adoption and cached merge
ancestor machinery. Reuse those paths rather than adding another installer.
Existing missing mergeable files receive `review-only` plans with no applied
bytes; public repeated-upgrade checks must establish deletion preservation.

### Documentation / doctrine surface

Update `bootstrap/UPGRADE.md` and
`docs/methodology/doc-governance.md`, including its no-template/no-tracking
description and ownership table. Describe project ownership, force, collisions,
edits and deletion accurately. Preserve agent duties in their installed homes.
Update affected fidelity/install descriptions and extend the relevant changelog
entry. Do not replace Cairn's own root `RULES.md`.

Proposed paths:
- `templates/core/RULES.md` -- the only new shipped file.

## Sequence

Authority and existing install machinery are available. Ordinary and Security
plan reviews precede implementation. Estimate one agent workday including
reviews and checks; uncertainty is whether an existing preservation path needs
a small repair, not permission to omit its outcome.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Seed and track the project-owned starter | Required plan reviews | Template, core mapping and authoritative integrity exemption |
| C2 | Exercise preservation, collision and deletion workflows; correct guidance | C1 | Public promise checks and accurate ownership/recovery guidance |
| C3 | Review and finish | C1–C2, ordinary and Security code reviews, wide Boundary B | Fixed findings, release records and archived plan/proposal |

Luna executes reviewed C1–C2. A new trust-boundary design or a failure of the
specified reuse returns to the author and High reviewer; it is not left to
the Low implementer to redesign.

## Acceptance criteria

**C1.** Public installs in the existing small and full profile workflows seed
RULES and record its canonical source, cached ancestor and living-state status.
The shipped starter plus installed AGENTS and wrapper fit the 1,500-word cap;
measure the result without pinning its sentences. Normal install preserves an
existing regular file byte-for-byte, and explicit force behaves as documented.
Editing RULES does not fail integrity verification; editing an apparatus file
and falsely marking it living state still fails.

**C2.** Public upgrade plan/stage/adopt/apply preserves an old untracked regular
RULES as a fork under the displayed digest authorization. Changed staged bytes,
links, directories and another source's ownership retain safe refusal/manual
recovery. Subsequent upgrades preserve project edits and never restore a tracked
deleted RULES. Source and merge-ancestor tampering still refuse. Guidance explains
the adopter's actual choices and contains no obsolete never-shipped assertion.

**C3.** Accepted outcomes, required reviews and applicable checks pass. Fix cheap
findings; leave no implementation evidence folders or undocumented deferments.
Update the board/changelog at completion, close any issue actually implemented,
and archive the plan and proposal by file move with links repaired. No currently
named issue is exclusively owned by this proposal.

## Scope delta

Preserved: all accepted install, ownership, collision, deletion and integrity
outcomes remain required.

## Verification

Extend or replace the existing nodes below through `scaffold.main` install, `upgrade --plan`,
`--stage`, `--adopt-collisions`, `--apply`, and `verify_integrity.verify` on
temporary projects. Replace obsolete absence nodes with the stated promises;
use public entry points and extend existing checks rather than cloning families.

| Owner | Nodes to replace or extend | Promise / inputs |
|---|---|---|
| `bootstrap/tests/test_scaffold.py` | `TestRulesMdNeverTemplated::test_full_install_writes_no_rules_md`; `TestInstallCore::test_normal_install_preserves_existing_changelog_bytes` | Small/full seed and word budget; existing RULES bytes and explicit force |
| `bootstrap/tests/test_upgrade.py` | `TestRulesMdAbsentFromUpgradePlan::test_upgrade_plan_never_lists_rules_md` | Replace with edited/deleted tracked RULES, two stage/apply cycles, retained absence and lock record |
| Same upgrade owner | `TestLivingStatePartition::test_install_flags_living_state_records`; `TestLivingStatePartition::test_editing_living_state_does_not_fail_integrity`; `TestLivingStatePartition::test_living_state_flag_rejected_outside_authoritative_set` | RULES exemption versus apparatus tampering/forged exemption |
| `bootstrap/tests/test_upgrade_module_additions.py` | `test_new_core_changelog_collision_can_be_kept_as_a_fork`; `test_adapted_changelog_is_restaged_before_collision_adoption`; `test_new_core_changelog_link_collision_cannot_be_adopted` | Extend the existing collision class to RULES; preserve digest-bound adoption, restaging and unsafe-destination refusal |

Existing `TestUpgradeModes::test_bad_ancestor_uses_review_recovery_and_preserves_evidence`
and `TestUpgradeModes::test_apply_rejects_changed_ancestor_since_stage` in the
upgrade owner remain ancestor consumers. Core mapping/manifest consumers and
source attestation are included by the changed-path selection. Keep permanent
promise checks; remove temporary development probes before archive.

Before implementation, map changed paths with `tools/test_tiers.py for`;
for governing text pass the reviewed range. Run scoped prose gates for changed
guidance. Security preflight answers remain those of the accepted proposal;
C2 owns destination, changed-stage, unauthorized-exemption and ancestor
falsifiers through existing public commands. No scientific check applies.

After independent code reviews, run one clean-commit **wide Boundary B** covering
mapped producers, consumers and public install/upgrade/integrity workflows with
canonical Python 3.13.13. Share an unchanged final selection with overlapping
plans where valid; fix failures and retry affected checks. Full certification,
repin, re-anchor and publication remain separate release work, not plan gates.

## Plan review -- GPT-6.1 Terra (Reviewer) -- 2026-11-12

Reviewed commit: 71b03633

**Obligation**: Internal
**Findings**: blocking
**Verdict**: REVISE
**Elapsed**: approximately five minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: the plan retains the accepted install, collision, deletion and integrity outcomes, but its verification mapping needs completion before execution -- accepted proposal at `5ba9ad64`; plan Scope and Verification.
2. **Best alternative.** Reuse the existing mergeable-file and collision paths as proposed; a new deletion state would add machinery without an identified need -- `bootstrap/_scaffold/upgrade.py:905` and `bootstrap/tests/test_upgrade_module_additions.py:1021`.
3. **What would show it wrong?** A repeated public upgrade that restores deleted rules, changes a fork, or accepts tampered evidence would falsify it -- plan C2; `bootstrap/_scaffold/upgrade.py:1398`.

**Blocking:** The accepted proposal requires the plan to map exact behavioral test nodes and affected consumers. Verification names three test files, but defers path mapping until implementation and identifies no nodes or public command inputs. Map the existing nodes and affected consumers, including the repeated deletion and integrity controls, before Low execution; identify any uncovered promise to extend. Evidence: proposal Tests required; plan Verification.

**Audience:** Ownership and recovery are adopter choices; the plan preserves agent duties in installed homes and removes no rule. **Coverage:** Read the accepted proposal, plan, current templates and relevant source and test homes. Missing mergeable files are review-only with no applied file bytes; repeated RULES upgrades remain prospective. Did not run tests or conduct Security Review.

## Plan review response -- GPT-6.1 Terra (Author) -- 2026-11-12

Specified the actual public commands, existing nodes to replace or extend,
their inputs and promises, and integrity/ancestor/mapping consumers in
Verification. This closes the review's missing-mapping finding; no accepted
outcome or required check is removed. The added table is required by that
finding, not a new evidence ledger. Implementation remains unstarted pending
the required Security plan review. The accepted source proposal also moves to
the archive, as the plan-opening template requires.

**Elapsed:** approximately four minutes. **Tokens:** unknown.

## Plan review -- GPT-6.1 Sol (Security Review, High) -- 2026-11-12

Reviewed commit: 5da65af84f916d8c36b4024debfe6a5bc03cd862

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: blocking
**Verdict**: REVISE
**Elapsed**: approximately six minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: the mapping, authoritative exemption and retained review-only deletion path preserve the accepted outcomes without new write authority; one required consumer mapping remains unsatisfied -- accepted proposal at `5ba9ad64`; plan Scope and Verification.
2. **Best alternative.** Keep the existing collision and mergeable-file machinery: digest-bound adoption retains exact project bytes, and missing tracked files never enter the applied set -- `bootstrap/tests/test_upgrade_module_additions.py:1021`; `bootstrap/_scaffold/upgrade.py:1398`.
3. **What would show it wrong?** Repeated stage/apply restoring deleted RULES, adoption accepting changed bytes, or an apparatus record obtaining the exemption would falsify delivery -- plan C2 and mapped public refusal controls.

**Blocking:** Verification says manifest consumers are included by changed-path selection. The actual canonical command `tools/test_tiers.py for bootstrap/_scaffold/config.py bootstrap/_scaffold/lockfile.py` selects 59 files, including the known upgrade consumer, but omits `bootstrap/tests/test_manifest.py`. The accepted proposal explicitly requires manifest checks; relying on that selection therefore leaves a required check unassigned. Close by explicitly mapping `TestInstallManifest::test_manifest_matches_actual_install` and `TestInstallManifest::test_manifest_cli_needs_no_config` in that existing file (or a named executing equivalent), including them in the required run, and correcting the selection claim.

**Does any rule weaken or disappear?** No planned rule loss: ownership, force and recovery guidance retain installed duties.

**Coverage:** Compared the accepted scope, revised plan, current templates, mapping/allowlist, ancestor validation, collision tests and stage/apply ordering. Confirmed cited nodes exist and ran only mapping selection; did not execute implementation tests, RULES workflows or mutations. Future RULES bytes and runtime outcomes remain unmeasured.
