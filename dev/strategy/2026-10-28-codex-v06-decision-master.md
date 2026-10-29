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
research. This five-plan batch does not complete v0.6.

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

**Chosen:** public methodology at `docs/methodology/`, duties in installed
files and project rules in `dev/rules/` (`aa9fc08b`). Coordination claims intent,
blocks provable live conflicts, warns on stale/tokenless cases and retains
warn/confirm modes (`7013de1d`). Literal paths can recur only by exact declared
provenance; checker logic is unchanged (`560a178c`).

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

**Recommend:** separately authorize moving two named ordinary methods to
`bootstrap/tests/test_board_json_values.py`; security helpers stay protected.
New scope despite roster approval, it requires independent reviews and a
protected-node transition. Otherwise wait or explicitly lose the pilot outcome.
Keep the testing-module update; simulation guidance stays v0.7.

Proposed path: `bootstrap/tests/test_board_json_values.py` (not yet created).

### 4. Establish a forward-trust baseline at v0.6

The Maintainer directed re-anchoring at v0.6 without checking intervening
changes against the old anchor. The [exploration](2026-10-29-sol-forward-baseline.md)
proposes one reviewed, signed baseline with the approved roster. This gives up
P443-to-release drift checks and certifies no earlier history; prior HOLDs are
not prerequisites. Align the plans. Candidate, package and signer need
Maintainer authorization; pushing is separate. Dormant bridge `6e3197f6` is
approved but uninstalled and not certified. Account for frozen checker wording.

### 5. Queued convention choice: session handoff marker

A scratch history reproduced `Goodnight` missing `Handoff:`. **Recommend:** use
`--handoff-marker` in Cairn; settle a convention before changing adopters' default.
This remains queued, not a prerequisite to the open decisions.

### 6. Upgrade base and install-output integrity

**Awaiting the Maintainer's Decision.** The [proposal](../proposals/2026-10-29-codex-upgrade-install-integrity.md)
checks saved ancestor bytes before merging; invalid evidence routes to manual
review while preserving adopter files and cache. It rejects Cc/Cf, U+034F and
variation selectors in paths, retains ordinary combining marks and visible
non-Latin names, and escapes supplied output names. Reviews accepted. The digest
is not authentication when cache and lockfile are jointly controlled. No
implementation; Internal/Security plan reviews and AST ceremony remain. No
baseline installation or old-anchor reconciliation is authorized.

### 7. Directories occupying tracked upgrade paths

**Awaiting the Maintainer's Decision.** The [proposal](../proposals/2026-10-29-codex-upgrade-directory-collisions.md)
hard-blocks a tracked destination occupied by a directory, preserving contents
until resolution and a fresh stage. It retains unaffected-file reporting but
allows no partial apply, adoption or review pair. Both reviews accepted; the
response covers stage/apply observation points and containment. Arbitrary races
after checks remain possible. Implementation, plan reviews and AST ceremony
remain pending.

### 8. Nested Git paths during upgrade

**Awaiting the Maintainer's Decision.** The [proposal](../proposals/2026-10-29-codex-nested-git-upgrade.md)
refuses `.git` components in supplied and resolved project paths, including
lockfile destinations, caches and staged names. This closes the demonstrated
nested-hook write and stable symlink read while retaining ordinary contained
links and lookalikes. Trailing-dot/space compatibility costs remain; hard links
under other names and post-check races are not covered. Resolved-target reviews
accepted; implementation, Internal/Security plan reviews and AST ceremony
remain pending.

### 9. Prepare the handoff before pruning

**Awaiting the Maintainer's Decision.** The [proposal](../proposals/2026-10-29-codex-handoff-prune.md),
handed off at `c6c6bbea`, adds non-pruning preparation with capture prompts and
preview, preserving `--handoff` as the guarded user-run deletion. Both reviews
accepted. Preparation cannot prove sessions are quiet; the user must establish
quiet when pruning. Plan reviews and the doctrine-evolution gate remain.

### 10. Bind the interpreter in Git's per-worktree administration

**Awaiting the Maintainer's Decision.** The [proposal](../proposals/2026-10-29-codex-git-interpreter-binding.md),
handed off at `74b5917f`, stores the binding in verified per-worktree Git
administration and requires exact-root discovery. Non-repository installs can
proceed without it and rebind later; the legacy file is never read or migrated.
Revised ordinary findings were answered and Security accepted. Copied `.git`
administration or a delivered pointer can still supply the binding, a residual
for Maintainer judgment. Native Windows discovery and junction/reparse evidence
remain required; Internal/Security plan reviews remain.

### 11. Detect and report same-file sweeps

**Awaiting the Maintainer's Decision.** The [proposal](../proposals/2026-10-29-codex-same-file-sweeps.md)
clears its Security obligation at `7211bca4`. It counts only confirmed
misattributed commits (another author's uncommitted work committed without
attribution), one row each with grouped paths and occurrence separate from
discovery date; uncertainty is excluded without author confirmation or
provenance. Require writer agreement through commit, inspect staged/unstaged and
new files, recheck changed bytes, or use separate worktrees. Claims are not
consent; stop on foreign/uncertain content. Keep minimal local references and
screen summaries; never copy private chats, secrets or unrelated text. The
advisory gate is incomplete; noncooperation, omissions and dishonest reports
remain possible. Plan/code Security reviews remain owed.

### 12. Correct work-intent guidance and identity help

**Awaiting the Maintainer's Decision.** The [proposal](../proposals/2026-10-29-codex-intent-guidance.md),
handed off at `f2a5b459`, reconciles guidance and parent CLI help without changing
enforcement. The opt-in hook blocks fresh overlaps only with a token and
different resolved labels; stale/unclaimed paths warn. Use one session label for
claim, commit and inherited auto-release; prefer harness identity, avoid global
overrides and shared sibling labels. Manual release uses claim ID, not label
authentication. Labels/logs are cooperative, not authentication. Security
accepted after ordinary findings were answered; Internal/Security plan reviews
remain owed.

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
