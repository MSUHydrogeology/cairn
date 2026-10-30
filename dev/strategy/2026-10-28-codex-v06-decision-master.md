# v0.6 decision master — editing burden and nimbleness first

**Author**: Codex (Coordination)
**Model**: GPT-6; coordination switched to Terra by Maintainer on 2026-10-28
**Date**: 2026-10-28
**Status**: living
**Type**: living-reference
**Surfaces this would feed**: Maintainer decisions and actions on v0.6 plans and the roadmap.

## Purpose and authority

This living packet coordinates v0.6 decisions. The Maintainer authorized
continuous reviews and handoffs; the [roadmap](../PLANNING.md) holds scope and
linked plans their contracts and status. It grants no approval and replaces no
Decision. Push, publication, settings changes and issue closure remain
unauthorized.

v0.6 makes existing capabilities work; v0.7 adds capabilities and adopter
research. The five-plan batch does not complete v0.6.

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

Retain all 21 partial-reach groups until installed homes and usable pointers
are shown; consolidation loses no accepted duty. C3 must show a simpler edit
against both baselines; frozen tests await trust-boundary work.

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

The Maintainer directed v0.6 re-anchoring without checking intervening changes
against the old anchor. The [exploration](2026-10-29-sol-forward-baseline.md)
proposes one reviewed, signed baseline with the approved roster. It gives up
P443-to-release drift checks and certifies no earlier history; prior HOLDs are
not prerequisites. Align plans. Candidate, package and signer need Maintainer
authorization; pushing is separate. Bridge `6e3197f6` is approved but not
installed or certified. Account for frozen checker wording.

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

The [archived proposal](../proposals/archive/2026-10-29-codex-upgrade-directory-collisions.md)
and [plan](../plans/2026-10-30-upgrade-directory-collisions.md) are accepted;
the plan is `ready-to-implement`. Hard-block a tracked destination occupied by
a directory, preserving contents until resolution and a fresh stage. Keep
unaffected-file reporting, but allow no partial apply, adoption or review pair.
Arbitrary races after checks remain possible. Implementation verification and
the separate Maintainer-run AST ceremony remain.

### 8. Nested Git paths during upgrade — accepted

The [archived proposal](../proposals/archive/2026-10-29-codex-nested-git-upgrade.md)
and [plan](../plans/2026-10-30-nested-git-upgrade.md) are accepted; the plan is
`implementing`. Refuse `.git` components in supplied and resolved project
paths, including lockfile destinations, caches and staged names. Keep ordinary
contained links and lookalikes. Trailing-dot/space compatibility costs remain;
hard links under other names and post-check races are not covered. Implementation
verification and the separate Maintainer-run AST ceremony remain.

### 9. Prepare the handoff before pruning — accepted

The [archived proposal](../proposals/archive/2026-10-29-codex-handoff-prune.md)
and [archived plan](../plans/archive/2026-10-30-handoff-preparation.md) are
accepted; implementation is complete. It adds non-pruning preparation with
capture prompts and preview, retaining `--handoff` as guarded user-run
deletion. Preparation cannot prove sessions are quiet; the user establishes
quiet before pruning. The
implementation verification and reviews are complete. The doctrine-evolution
trigger was not established; the Maintainer allowed the approved scope to
proceed, as recorded in the plan.

### 10. Bind the interpreter in Git's per-worktree administration — accepted

The [archived proposal](../proposals/archive/2026-10-29-codex-git-interpreter-binding.md)
and [plan](../plans/2026-10-30-git-interpreter-binding.md) are accepted;
`ready-to-implement`. Store the binding in verified per-worktree Git
administration and require exact-root discovery. Non-repository installs can
proceed without it and rebind later; never read or migrate the legacy file.
Copied `.git` administration or a delivered pointer can still supply the
binding. Native Windows and junction/reparse evidence remain required during
implementation.

### 11. Detect and report same-file sweeps — accepted

The [archived proposal](../proposals/archive/2026-10-29-codex-same-file-sweeps.md)
and [plan](../plans/archive/2026-10-30-same-file-sweeps.md) are accepted and
implemented. Count confirmed misattributed commits only, one row each;
separate occurrence from discovery, excluding uncertainty without confirmation
or provenance. Agree with writers, inspect staged/unstaged/new files, reinspect
changed bytes or use separate worktrees. Claims are not consent: stop on foreign
or uncertain content. Keep minimal local references; screen summaries and never
copy private chats, secrets or unrelated text. Advisory gate limits remain:
omissions, noncooperation and dishonest reports are possible. Mapped checks
and both independent code reviews are recorded; certification remains pending.

### 12. Correct work-intent guidance and identity help — accepted

The [archived proposal](../proposals/archive/2026-10-29-codex-intent-guidance.md)
and [archived plan](../plans/archive/2026-10-30-intent-guidance.md) delivered
the guidance and parent CLI help correction without changing enforcement.
The ordinary and Security code reviews accepted the implementation; the
recorded gate-manifest ceremony remains separate v0.6 baseline work.

### 13. Repair certification test failures — awaiting Decision

The [proposal](../proposals/2026-10-30-codex-certification-test-repairs.md),
awaits Decision. The uncertified `8b51bb2e` run had 5,622 passes and six
failures: five in test infrastructure, one in unrelated upgrade behavior.
Reproduce ordering before choosing isolation; retain the safety assertions.
Four affected files remain frozen, with ceremony owed.

### 14. Render generated inventory in upgrade review copies — awaiting Decision

The [proposal](../proposals/2026-10-30-codex-review-inventory-rendering.md),
awaits Decision. Render upstream `.theirs` from the recorded roster; keep
`.ours` as adopter bytes. Preserve ancestor and apply behavior; handle
historical `--to` and invalid markers without a false comparison.

### 15. Reduce repeated setup in review-sweep tests — awaiting Decision

The [speed proposal](../proposals/2026-10-29-codex-certification-cost-audit.md),
awaits Decision. Change `installs` from module to session scope, retaining
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

### 17. Refuse linked files during lockfile migration — awaiting Decision

The [proposal](../proposals/2026-10-30-codex-init-lock-linked-files.md),
responded at `e6c69148`, cleared Security Review at `52a7feb3` and awaits
Decision. `--init-lock` currently hashes a linked installed file's target,
even outside the project. Reuse its link guard before mapped-file reads in a
stable tree. Legitimate linked installs must replace the linked file or folder
with an ordinary copy before migration. A separate fidelity-manifest reader
can still follow a link; this scope discloses but does not fix that gap.

## Issue triage, staffing and close-out

Issues #31 and #32 await Maintainer closure; #33's scoped verification retains
its ceremony hold; #19 remains deferred to v0.7.

Staffing follows the Maintainer: **Terra coordinates and handles ordinary reviews;
Luna implements reviewed plans; Sol handles strategy, premise/novel-design and
Security judgment.** Cairn-local high/medium/low assignments are Sol/Terra/Luna,
Opus/Sonnet/Haiku and Argon/Pro/Flash. Shipped tiers remain vendor-neutral.
Decision scribing requires unambiguous disposition and commit authorization.

This master stays current until its coordinating role retires. Plans own
engineering evidence; this briefing certifies no implementation or release.
