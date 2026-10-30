# v0.6 decision master — editing burden and nimbleness first

**Author**: Codex (Coordination)
**Model**: GPT-6; coordination switched to Terra by Maintainer on 2026-10-28
**Date**: 2026-10-28
**Status**: living
**Type**: living-reference
**Surfaces this would feed**: Maintainer decisions and actions on v0.6 plans and the roadmap.

## Purpose and authority

This packet coordinates v0.6 decisions. The [roadmap](../PLANNING.md) owns
scope and plans own contracts; this file grants no approval. Push, publication,
settings changes and issue closure remain unauthorized. v0.6 repairs existing
capabilities; v0.7 adds capabilities and adopter research.

## Delivered work and current holds

| Plan | Result |
|---|---|
| [Model floors](../plans/archive/2026-10-28-model-floor-alignment.md) | Implemented, reviewed and archived; shipped generic task floors align with vendor assignments. Certification/re-anchor remain on the roadmap. |
| [Scoped verification](../plans/archive/2026-10-28-scoped-change-verification.md) | Implemented and scoped-verified; frozen-file ceremony remains. |
| [Governing text](../plans/archive/2026-10-28-governing-text-single-source.md) | Archived after inventory and consolidation; forward-baseline installation remains separate v0.6 work. |
| [Test trust boundary](../plans/archive/2026-10-28-test-trust-boundary.md) | Roster and dormant setting approved; active protection and certification remain. |
| [Ordinary test maintenance](../plans/archive/2026-10-28-ordinary-test-maintenance.md) | Reviewed plan; implementation waits because the chosen board file contains security defenses and remains protected. |
| [Release evidence environment](../plans/archive/2026-10-29-release-evidence-environment.md) | C1 implemented and reviewed; deferred packet, verifier, pinning and signing belong to the forward-baseline item. |

The source Decisions are `63e315fa`, `f110d263`, `cca436a9`, `cea1299d` and
`439c7b34`. All five plans were authorized; their later explicit fences remain.
Use `python tools/board.py --maintainer` for declared next moves.

## Ceremony-command plan

The Maintainer approved the [ceremony-command proposal](../proposals/archive/2026-10-29-codex-ceremony-commands.md)
in `02a81d33`; its [archived plan](../plans/archive/2026-10-29-ceremony-commands.md)
delivered the reviewed v0.5 `repin` command machinery and scratch verification,
including a prior-anchor verifier. Installation, signing, re-anchor and push
remain separate, unauthorized baseline work.

## Remaining decisions and actions

### 1. Governing-text routing and two conflicting prescriptions

**Chosen:** public methodology at `docs/methodology/`, installed duties and
project rules in `dev/rules/` (`aa9fc08b`). Coordination claims intent, blocks
provable live conflicts, warns on stale/tokenless cases and retains warn/confirm
(`7013de1d`). Literal paths recur only by declared provenance; checker logic is
unchanged (`560a178c`).

Proposed path: `docs/methodology/` (not yet created).

Retain all 21 partial-reach groups until installed homes and pointers exist.
C3 must show simpler edits against both baselines; frozen tests still wait.

### 2. Approved initial test-protection roster

**Approved:** [roster](../plans/archive/2026-10-28-test-trust-boundary/c1b-roster-6cc95fa7.json)
`884e6d53`; [evidence](../plans/archive/2026-10-28-test-trust-boundary/c1b-evidence-6cc95fa7.json)
classifies 78 test files and 12 controls, leaving 51 ordinary. Installation is
not established; approval `3e9f8fc2` waives no ceremony. Ordinary tests retain
byte and node/marker HOLD protection; ordinary Python can influence protected
execution.

### 3. Allow a preparatory extraction for the maintenance pilot

**Recommend:** separately authorize moving two named ordinary methods to
`bootstrap/tests/test_board_json_values.py`; keep security helpers protected.
This new scope needs independent reviews and a protected-node transition.
Otherwise wait or explicitly lose the pilot; keep the testing-module update,
while simulation guidance stays v0.7.

Proposed path: `bootstrap/tests/test_board_json_values.py` (not yet created).

### 4. Establish a forward-trust baseline at v0.6

The Maintainer directed v0.6 re-anchoring without old-anchor drift checks. The
[exploration](2026-10-29-sol-forward-baseline.md) proposes a reviewed, signed
baseline with the approved roster; earlier history is not certified. Prior
HOLDs are not prerequisites. Candidate, package, signer and push need separate
authorization. Bridge `6e3197f6` is approved, not installed or certified;
frozen checker wording remains.

### 5. Session-start handoff marker — corrected

Commit `6f425b64` changed the session-start default from `Goodnight` to
`Handoff` in the CLI and shipped kernel, with the owning test updated. Its
bounded check passed (26 tests, Python 3.13.13); certification remains pending.

### 6. Upgrade base and install-output integrity — accepted

The [archived proposal](../proposals/archive/2026-10-29-codex-upgrade-install-integrity.md)
and [plan](../plans/2026-10-30-upgrade-install-integrity.md) are accepted;
`ready-to-implement`. Check saved ancestors before merge; invalid evidence routes
to manual review without overwriting adopter files/cache. Reject Cc/Cf, U+034F
and variation selectors in paths; retain ordinary combining marks and visible
non-Latin names; escape supplied output. A digest is not authentication when
cache and lockfile are jointly controlled. AST ceremony remains; no baseline
installation or old-anchor reconciliation is authorized.

### 7. Directories occupying tracked upgrade paths — accepted

The [proposal](../proposals/archive/2026-10-29-codex-upgrade-directory-collisions.md)
and [plan](../plans/2026-10-30-upgrade-directory-collisions.md) are accepted;
the plan is `implementing`. Six public controls passed at `4a76dc54`.
[Review `9b40d4d4`](../plans/2026-10-30-upgrade-directory-collisions.md)
found that a staged rename can omit `CLAUDE.md`; replacing it with a directory
then lets apply advance lock and cache. Refusing directories at known wrapper
names and root `*.md` paths may also block unrelated folders. A trusted name
map adds machinery. Post-check races remain.

**Recovery choice:** accepted text permits absence after moving a folder, but
`verify_integrity` rejects a missing tracked file. Keep upgrade-only recovery
with failed integrity, or require restoration, which loses accepted scope and
needs a Scope delta. Reviews and mapped verification remain open.

### 8. Nested Git paths during upgrade — accepted

The [archived proposal](../proposals/archive/2026-10-29-codex-nested-git-upgrade.md)
and [plan](../plans/2026-10-30-nested-git-upgrade.md) are accepted; the plan is
`implementing`. Refuse `.git` components in supplied and resolved project
paths, including lockfile destinations, caches and staged names. Keep ordinary
contained links and lookalikes. Trailing-dot/space compatibility costs remain;
hard links under other names and post-check races are not covered. Implementation
verification and the separate Maintainer-run AST ceremony remain.

### 9. Prepare the handoff before pruning — accepted

The [proposal](../proposals/archive/2026-10-29-codex-handoff-prune.md)
and [plan](../plans/archive/2026-10-30-handoff-preparation.md) are implemented
and reviewed. Preparation adds capture prompts and preview; `--handoff` remains
guarded user-run deletion. The user establishes quiet sessions before pruning.
The Maintainer allowed the approved scope despite an unestablished doctrine
trigger, as recorded in the plan.

### 10. Bind the interpreter in Git's per-worktree administration — accepted

The [proposal](../proposals/archive/2026-10-29-codex-git-interpreter-binding.md)
and [plan](../plans/archive/2026-10-30-git-interpreter-binding.md) are
implemented. Bind in verified per-worktree Git administration, discover the
exact root, and never migrate legacy files. Non-repository installs rebind
later. Copied `.git` administration remains a risk. Windows junction/reparse
work is a separate roadmap follow-up.

### 11. Detect and report same-file sweeps — accepted

The [proposal](../proposals/archive/2026-10-29-codex-same-file-sweeps.md)
and [plan](../plans/archive/2026-10-30-same-file-sweeps.md) are implemented.
Count only confirmed misattributed commits. Agree with writers, inspect all
candidate bytes and stop on foreign or uncertain content; claims are not
consent. Keep minimal screened records. The advisory gate can miss
noncooperation or dishonest reports. Mapped checks and both code reviews are
recorded; certification remains pending.

### 12. Correct work-intent guidance and identity help — accepted

The [archived proposal](../proposals/archive/2026-10-29-codex-intent-guidance.md)
and [archived plan](../plans/archive/2026-10-30-intent-guidance.md) delivered
the guidance and parent CLI help correction without changing enforcement.
The ordinary and Security code reviews accepted the implementation; the
recorded gate-manifest ceremony remains separate v0.6 baseline work.

### 13. Repair certification test failures — accepted

The [proposal](../proposals/archive/2026-10-30-codex-certification-test-repairs.md)
was accepted at `322eafb5`. The uncertified `8b51bb2e` run had 5,622 passes and six
failures: five in test infrastructure, one in unrelated upgrade behavior.
Reproduce ordering before choosing isolation; retain the safety assertions.
Four affected files remain frozen, with ceremony owed.

### 14. Render generated inventory in upgrade review copies — delivered

The [proposal](../proposals/archive/2026-10-30-codex-review-inventory-rendering.md)
was accepted at `9db57ec6`. Implementation is complete in the
[archived plan](../plans/archive/2026-10-30-review-inventory-rendering.md).
Review copies render upstream `.theirs` from the recorded roster and keep
`.ours` as adopter bytes. Ancestors and apply behavior are preserved; historical
renderers must match before reuse, and invalid markers refuse staging.

### 15. Reduce repeated setup in review-sweep tests — accepted

The [speed proposal](../proposals/archive/2026-10-29-codex-certification-cost-audit.md)
was accepted at `3b675bb0`. Change `installs` from module to session scope, retaining
every node. One scoped run per variant passed 391 tests (18.55 versus 0.65
seconds); neither timing stability nor full-suite speedup is established.
The file remains frozen, so its ceremony is owed. A plan must test shuffled
isolation, repeat timing and fault controls. No extra suite or baseline is
authorized.

### 16. Clean customized upgrade merges — awaiting Decision

The [proposal](../proposals/2026-10-30-codex-upgrade-semantic-adoption.md),
responded at `4cc00bec`, awaits Decision. A clean text merge can retain
incompatible local and upstream policy. The author recommends rejecting the
proposed per-file enforcement: both reviews found it needs a true two-sided
trigger, durable decisions, byte binding and old profile context across partial
upgrades. This **loses** the board's required incorporation-or-disposition
outcome; only the Maintainer can allow that loss or keep #35 for redesign.

### 17. Refuse linked files during lockfile migration — delivered

The [proposal](../proposals/archive/2026-10-30-codex-init-lock-linked-files.md)
was accepted at `06af4aeb` after Security Review clearance at `52a7feb3`.
Implementation is complete in the [archived plan](../plans/archive/2026-10-30-init-lock-linked-files.md).
`--init-lock` refuses links at mapped installed paths before existence checks
or reads in a stable tree. Legitimate linked installs must replace the linked
file or folder with an ordinary copy before migration. The separate
fidelity-manifest reader and concurrent path replacement remain outside this
check, as the archived plan records.

### 18. Publish and check the GitHub Release — awaiting Decision

The [proposal](../proposals/2026-10-30-codex-tag-release-distinction.md)
responded at `a508dfcf`; both widened-scope reviews found no new issues and
Security Review closed its findings. The cut prepares notes and pushes a tag
without explicitly publishing the GitHub Release. The author recommends a
Maintainer create-or-edit step, manual notes/link read-back, and a read-only
script comparing the published Release and remote peeled tag with the
independently recorded gate commit. Correct the guide's retired unsigned-tag
alternative to match `bootstrap/PROVENANCE.md`. Links and remote tag identity
do not verify cached archive bytes. The Maintainer decides both additions;
Release and push remain unauthorized.

### 19. Refuse ambiguous module discovery markers — awaiting Decision

The [proposal](../proposals/2026-10-30-codex-module-marker-ambiguity.md)
responded to ordinary and Security Reviews at `0ac33887`. A public repeat
install returned success after a checked task's marker was edited, leaving
two `reflections` tasks. **Recommend accept as revised:** reuse the shared
reconciler to refuse malformed, nested or crossed generated markers before
planning, inventory or lock changes, including an empty module roster.
Inline, indented and blockquoted marker mentions remain ordinary prose.
The cost is manual reconciliation for edited markers; accepting loose syntax
risks duplicating or deleting adopter work. Heavy-tier plan and Security
Review remain required; no implementation or Decision is recorded.

## Issue triage, staffing and close-out

Issues #31 and #32 await Maintainer closure; #33's scoped verification retains
its ceremony hold; #19 remains deferred to v0.7.

Staffing: **Terra coordinates and reviews; Luna implements reviewed plans; Sol
handles strategy and Security judgment.** Model tiers remain vendor-neutral in
shipped text. Decision scribing needs explicit authorization.

This master stays current until its coordinating role retires. Plans own
engineering evidence; this briefing certifies no implementation or release.
