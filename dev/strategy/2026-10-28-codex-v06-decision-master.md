# v0.6 decision master — editing burden and nimbleness first

**Author**: Codex (Coordination)
**Model**: GPT-6; coordination switched to Terra by Maintainer on 2026-10-28
**Date**: 2026-10-28
**Status**: living
**Type**: living-reference
**Surfaces this would feed**: Maintainer decisions and actions on v0.6 plans and the roadmap.

## Purpose and authority

This is the consolidated decision packet for the nimbleness-first v0.6 batch.
The Maintainer authorized continuous reviews and handoffs without check-ins.
The [roadmap](../PLANNING.md) remains the scope inventory; each linked plan owns
its contract and status. This briefing grants no approval and replaces no
Decision. Pushing, publishing, repository settings changes and issue closure
remain unauthorized.

v0.6 makes existing capabilities work; v0.7 adds capabilities and adopter
research. This five-plan batch does not complete v0.6.

## Delivered work and current holds

| Plan | Result |
|---|---|
| [Model floors](../plans/archive/2026-10-28-model-floor-alignment.md) | Implemented, reviewed and archived; shipped generic task floors align with vendor assignments. Certification/re-anchor remain on the roadmap. |
| [Scoped verification](../plans/archive/2026-10-28-scoped-change-verification.md) | Implemented; 2,700 nodes reconciled, five guard cases and required local-capability security cases passed. Independent examples and ordinary/Security reviews complete; both hold archive for the frozen-file ceremony. Naming examples later corrected (656 passes, Python 3.13.13). |
| [Governing text](../plans/archive/2026-10-28-governing-text-single-source.md) | Archived after inventory and consolidation; forward-baseline installation remains separate v0.6 work. |
| [Test trust boundary](../plans/archive/2026-10-28-test-trust-boundary.md) | Roster and dormant setting approved; the dormant candidate is committed. Final verification and reviews wait on the reusable verifier workflow below; existing protection remains active. |
| [Ordinary test maintenance](../plans/archive/2026-10-28-ordinary-test-maintenance.md) | Reviewed plan; implementation waits because the chosen board file contains security defenses and remains protected. |
| [Release evidence environment](../plans/archive/2026-10-29-release-evidence-environment.md) | C1's exact cache-only pytest exception was implemented at `0c07eb37`, wide-verified and accepted by Internal and Security code reviews (`Certified by: pending`). Plan archived at `81072be0` after Maintainer-authorized deferral of C2 packet/reader and C3 prior-verifier, pinning and signing to the forward-baseline board item. C3's Maintainer-only fence remains; no ceremony or full-suite certification ran. |

The source Decisions are `63e315fa`, `f110d263`, `cca436a9`, `cea1299d` and
`439c7b34`. All five plans were authorized; their later explicit fences remain.
Use `python tools/board.py --maintainer` for declared next moves.

## Ceremony-command plan

The [ceremony-command proposal](../proposals/archive/2026-10-29-codex-ceremony-commands.md)
addresses the existing v0.6 two-command item, builds on v0.5 `repin`, and
originally included a full prior-anchor verifier. The Maintainer approved it
in `02a81d33`; the [plan](../plans/archive/2026-10-29-ceremony-commands.md)
completed its reviewed command machinery and scratch verification. Actual
installation remains separate v0.6 baseline work. No signing, re-anchor or push
is authorized by this briefing.

## Remaining decisions and actions

### 1. Governing-text routing and two conflicting prescriptions

**Chosen:** route public methodology to `docs/methodology/`, keep operating
duties in installed files and project rules in `dev/rules/` (`aa9fc08b`). The
Maintainer also chose the coordination default (`7013de1d`): claim intent,
block provable live-session conflicts, warn on stale/tokenless claims, and keep
warn/confirm modes and hooks. Explicit literal path declarations may recur with
exact matching and provenance (`560a178c`); checker logic is unchanged.

Proposed path: `docs/methodology/` (not yet created).

Retain all 21 partial-reach obligation groups until installed homes and usable
pointers are shown. No accepted duty is lost by consolidation. C3 must show an
actual simpler edit against both baselines; frozen tests await trust-boundary
work.

### 2. Approved initial test-protection roster

**Approved:** the [refreshed roster](../plans/archive/2026-10-28-test-trust-boundary/c1b-roster-6cc95fa7.json)
at `884e6d53`; [evidence](../plans/archive/2026-10-28-test-trust-boundary/c1b-evidence-6cc95fa7.json)
records its classification. It covers 78 test files and 12 controls, leaving
51 ordinary tests; installation is not established. Approval at `3e9f8fc2`
does not waive ceremony. Ordinary tests retain byte and node/marker HOLD
protection; ordinary Python can still influence protected execution.

### 3. Allow a preparatory extraction for the maintenance pilot

**Recommend:** separately authorize extracting the two named ordinary methods
to `bootstrap/tests/test_board_json_values.py`, preserving names and updating
the pilot path. Security helpers and cases stay protected. This is new scope
despite roster approval and requires independent reads and a protected-node
transition. Otherwise leave the pilot waiting or explicitly lose its protected-
lane outcome. Keep the testing-module update; simulation guidance stays v0.7.

Proposed path: `bootstrap/tests/test_board_json_values.py` (not yet created).

### 4. Establish a forward-trust baseline at v0.6

The Maintainer directed stopping checks of intervening changes against the old
anchor and re-anchoring at v0.6. The
[exploration](2026-10-29-sol-forward-baseline.md) proposes one reviewed, signed
baseline with the approved roster. This gives up P443-to-release drift checks
and certifies no earlier history; the 83 prior HOLDs are not a prerequisite.
Align trust, verification and ceremony plans. Candidate, package and signer
still need Maintainer authorization; pushing is separate. The dormant bridge at
`6e3197f6` is approved but not installed, and its runs are not certification.
Account for frozen checker wording in the release baseline.

### 5. Queued convention choice: session handoff marker

A scratch history reproduced `Goodnight` missing a `Handoff:` commit. **Recommend:**
use `--handoff-marker` in Cairn and settle a canonical convention before
changing adopters' default. No code changed; this is queued, not a prerequisite
for the open decisions.

### 6. Upgrade base and install-output integrity

**Awaiting the Maintainer's Decision.** The [proposal](../proposals/2026-10-29-codex-upgrade-install-integrity.md)
checks saved ancestor bytes before merging, sends invalid evidence to manual
review while preserving the adopter file and damaged cache, and escapes
untrusted module and slot names in output. It refuses control/format characters,
U+034F and variation selectors in project paths while retaining ordinary
combining marks and visible non-Latin names; existing refused names need a
documented recovery. Both proposal reviews accepted, with recovery, byte-binding
and compatibility guidance incorporated. A digest is not authentication when
the cache and lockfile are jointly controlled. No implementation was assessed;
the plan owes both Internal reviews and the existing AST ceremony. No old-anchor
reconciliation or baseline installation is authorized.

### 7. Directories occupying tracked upgrade paths

**Awaiting the Maintainer's Decision.** The [proposal](../proposals/2026-10-29-codex-upgrade-directory-collisions.md)
hard-blocks a directory at a tracked destination, preserving contents until
resolution and a fresh stage. The chosen path keeps unaffected-file information
but blocks the whole stage at apply; it permits no partial apply, adoption or
file review pair. Both reviews accepted without findings. The response added
observation-point, recovery and containment guidance. No implementation was
assessed; the plan owes both Internal reviews and the existing AST ceremony.
Arbitrary races after checks remain outside the claim.

### 8. Nested Git paths during upgrade

**Awaiting the Maintainer's Decision.** The [proposal](../proposals/2026-10-29-codex-nested-git-upgrade.md)
would refuse `.git` components in supplied project paths and their resolved
targets, including lockfile destinations, base caches and staged names. This
closes the demonstrated nested-hook write and stable symlink-to-Git read paths
while preserving ordinary contained read links and lookalike names. Both
resolved-target reviews accepted; the response retains a compatibility cost
for trailing-dot/space names and limits the claim: hard links under other names
and races after checks remain possible. The plan owes Internal and Internal
Security Review and the Maintainer-run AST ceremony; no implementation is
assessed.

### 9. Prepare the handoff before pruning

**Awaiting the Maintainer's Decision.** The [proposal](../proposals/2026-10-29-codex-handoff-prune.md),
handed off at `c6c6bbea`, adds non-destructive preparation that surfaces
capture prompts and a prune preview, while preserving `--handoff` as the
guarded user-run deletion command. The usual and Security Reviews accepted
without findings. Preparation cannot prove no session is appending; the user
must establish quiet when running the command. Implementation still owes both
plan reviews and the doctrine-evolution gate.

### 10. Bind the interpreter in Git's per-worktree administration

**Awaiting the Maintainer's Decision.** The [proposal](../proposals/2026-10-29-codex-git-interpreter-binding.md),
handed off at `74b5917f`, moves the binding from checkout content into verified
per-worktree Git administration. Linked worktrees, separate Git directories
and submodules qualify only when Git identifies the exact supplied root.
Non-repositories can install without a binding, then rebind after Git
initialization; the legacy file is never read or migrated, and unsafe state
refuses before launch. The revised usual findings were answered and Security
Review accepted. Copied `.git` administration or a delivered Git pointer can
still supply the binding; this residual is for Maintainer judgment. Native
Windows discovery and junction/reparse evidence remain required before
acceptance; plan review requires Internal and Internal Security Review.

### Certification cost — held for evidence, not a current Decision

The [proposal](../proposals/2026-10-29-codex-certification-cost-audit.md) remains
`revising`, held by its author until the next independently authorized clean
certification supplies family timings. It will then append a concrete candidate
and fault evidence for review before a Decision. The historical 24:55 run is
not a current measurement; no extra full suite is authorized. If no ordinary
family has a safe, useful improvement, record that and stop.

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
suite-wide performance. No full suite or push was performed for this handoff.
