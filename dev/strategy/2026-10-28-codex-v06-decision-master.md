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
| [Scoped verification](../plans/archive/2026-10-28-scoped-change-verification.md) | Implemented; scoped checks passed and independent reviews hold archive for the frozen-file ceremony. Naming examples later corrected (656 passes, Python 3.13.13). |
| [Governing text](../plans/archive/2026-10-28-governing-text-single-source.md) | Archived after inventory and consolidation; forward-baseline installation remains separate v0.6 work. |
| [Test trust boundary](../plans/archive/2026-10-28-test-trust-boundary.md) | Roster and dormant setting approved; active protection remains. Final verification and reviews await the reusable verifier. |
| [Ordinary test maintenance](../plans/archive/2026-10-28-ordinary-test-maintenance.md) | Reviewed plan; implementation waits because the chosen board file contains security defenses and remains protected. |
| [Release evidence environment](../plans/archive/2026-10-29-release-evidence-environment.md) | C1 implemented at `0c07eb37`, wide-verified and code-reviewed (`Certified by: pending`). Archived at `81072be0` after authorized deferral of C2 packet/reader and C3 verifier, pinning and signing to the forward-baseline item; its Maintainer-only fence remains. No ceremony or full certification ran. |

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
`ready-to-implement`. Refuse `.git` components in supplied and resolved project
paths, including lockfile destinations, caches and staged names. Keep ordinary
contained links and lookalikes. Trailing-dot/space compatibility costs remain;
hard links under other names and post-check races are not covered. Implementation
verification and the separate Maintainer-run AST ceremony remain.

### 9. Prepare the handoff before pruning — accepted

The [archived proposal](../proposals/archive/2026-10-29-codex-handoff-prune.md)
and [plan](../plans/2026-10-30-handoff-preparation.md) are accepted; the plan
is `ready-to-implement`. Add non-pruning preparation with capture prompts and
preview; retain `--handoff` as guarded user-run deletion. Preparation cannot
prove sessions are quiet; the user establishes quiet before pruning. Implementation
verification and the doctrine-evolution gate before doctrine edits remain.

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
and [plan](../plans/2026-10-30-same-file-sweeps.md) are accepted;
`ready-to-implement`. Count confirmed misattributed commits only, one row each;
separate occurrence from discovery, excluding uncertainty without confirmation
or provenance. Agree with writers, inspect staged/unstaged/new files, reinspect
changed bytes or use separate worktrees. Claims are not consent: stop on foreign
or uncertain content. Keep minimal local references; screen summaries and never
copy private chats, secrets or unrelated text. Advisory gate limits remain:
omissions, noncooperation and dishonest reports are possible. Verify mapped
behavior and complete the applicable frozen-file ceremony.

### 12. Correct work-intent guidance and identity help — accepted

The [archived proposal](../proposals/archive/2026-10-29-codex-intent-guidance.md)
and [archived plan](../plans/archive/2026-10-30-intent-guidance.md) delivered
the guidance and parent CLI help correction without changing enforcement.
The ordinary and Security code reviews accepted the implementation; the
recorded gate-manifest ceremony remains separate v0.6 baseline work.

### 13. Repair certification test failures — awaiting Decision

The [proposal](../proposals/2026-10-30-codex-certification-test-repairs.md),
responded at `bfb996f8`, awaits Decision. The uncertified `8b51bb2e` run had
5,622 passes and six failures. Five are test infrastructure: malformed lockfile
fixtures, a stale plan path and module identity contamination; the sixth is
unrelated upgrade behavior. Reproduce test ordering before choosing isolation;
preserve leak, evidence-refusal and re-anchor assertions. Four affected files
remain frozen by the installed manifest; the proposed ordinary classification
is not installed and waives no ceremony.

### 14. Render generated inventory in upgrade review copies — awaiting Decision

The [proposal](../proposals/2026-10-30-codex-review-inventory-rendering.md),
responded at `315f8506`, awaits Decision. Render upstream `.theirs` from the
recorded lock roster with the existing renderer; keep `.ours` as adopter bytes
so edits remain visible. Preserve the raw ancestor, installed inventory, apply
and reconciliation behavior. The plan must handle historical `--to` and
missing/malformed markers without presenting invalid comparisons as valid.

### 15. Reduce repeated setup in review-sweep tests — awaiting Decision

The [speed proposal](../proposals/2026-10-29-codex-certification-cost-audit.md),
concretized at `a3f7e15b`, awaits Decision. Change `installs` from module to
session scope, retaining every node and one install per profile. See [full-run
durations](../proposals/2026-10-29-codex-certification-cost-audit/certification-durations.txt),
[module-scope](../proposals/2026-10-29-codex-certification-cost-audit/scoped-baseline.txt)
and [session-scope](../proposals/2026-10-29-codex-certification-cost-audit/scoped-session.txt)
reports: both scoped runs passed 391 tests (18.55 and 0.65 seconds). These single
measurements establish neither timing stability nor full-suite speedup. File
is ordinary in the approved roster but frozen in the installed manifest; its
ceremony remains owed. No extra suite, protection change or baseline installation
is authorized. A plan must test shuffled shared-tree isolation, repeat timings
and fault controls; stop if the gain is unstable or controls fail.

## Issue triage, staffing and close-out

Read-only issue triage found #31 and #32 already implemented and reviewed;
closure remains the Maintainer's action. #33 is addressed by scoped verification,
with its ceremony hold still open. #19 is new scientific-governance capability
outside this batch and remains deferred/v0.7.

Staffing follows the Maintainer: **Terra coordinates and handles ordinary reviews;
Luna implements reviewed plans; Sol handles strategy, premise/novel-design and
Security judgment.** Cairn-local high/medium/low assignments are Sol/Terra/Luna,
Opus/Sonnet/Haiku and Argon/Pro/Flash. Shipped tiers remain vendor-neutral.
Decision scribing requires unambiguous disposition and commit authorization.

Completed strategy explorations archive with their owned evidence once their
purpose is discharged. This master stays current until its coordinating role is
retired; active v0.7 explorations remain live. Plans and their records own the
engineering evidence. Prose gates validate this briefing, not certification or
suite-wide performance. No full suite, certification or push was performed for
this update.
