# Plan: Install a project-owned rules starter

**Source proposal**: dev/proposals/2026-11-12-terra-rules-router-stub.md
**Status**: awaiting-plan-review
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

Use existing public workflows in `bootstrap/tests/test_scaffold.py`,
`bootstrap/tests/test_upgrade.py` and
`bootstrap/tests/test_upgrade_module_additions.py`. Replace obsolete RULES
absence checks; extend current preservation and parameterized refusal checks
instead of cloning a changelog test family. Keep permanent tests of promises,
not private helpers or wording. Temporary development probes are removed.

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
