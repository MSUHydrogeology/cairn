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

The archived plans for [model floors](../plans/archive/2026-10-28-model-floor-alignment.md),
[scoped verification](../plans/archive/2026-10-28-scoped-change-verification.md),
[governing text](../plans/archive/2026-10-28-governing-text-single-source.md),
[test trust](../plans/archive/2026-10-28-test-trust-boundary.md),
[ordinary test maintenance](../plans/archive/2026-10-28-ordinary-test-maintenance.md)
and [release evidence](../plans/archive/2026-10-29-release-evidence-environment.md)
record delivered work and outstanding fences. Certification, protection and
forward-baseline work remain separate. The ordinary-test pilot remains held
because its board file contains security defenses. The source Decisions are
`63e315fa`, `f110d263`, `cca436a9`, `cea1299d` and `439c7b34`.
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
[exploration](archive/2026-10-29-sol-forward-baseline.md) proposes a reviewed, signed
baseline with the approved roster; earlier history is not certified. Prior
HOLDs are not prerequisites. Candidate, package, signer and push need separate
authorization. Bridge `6e3197f6` is approved, not installed or certified;
frozen checker wording remains.

### 5. Session-start handoff marker — corrected

Commit `6f425b64` changed the session-start default from `Goodnight` to
`Handoff` in the CLI and shipped kernel, with the owning test updated. Its
bounded check passed (26 tests, Python 3.13.13); certification remains pending.

### 6. Upgrade base and install-output integrity — delivered

The [archived proposal](../proposals/archive/2026-10-29-codex-upgrade-install-integrity.md)
and [plan](../plans/archive/2026-10-30-upgrade-install-integrity.md) record the
implementation, 740 passing mapped tests and standing gates, and two killed
mutants. The digest does not authenticate jointly controlled cache and lockfile.
Certification and baseline remain separate.

### 7. Directories occupying tracked upgrade paths — accepted

The [proposal](../proposals/archive/2026-10-29-codex-upgrade-directory-collisions.md)
and [plan](../plans/2026-10-30-upgrade-directory-collisions.md) remain in
implementation. Fixes `a5940f31` and `3796e277` address the wrapper finding
and preserve precedence; final reviews and verification remain open.

**Recovery choice:** accepted text permits absence after moving a folder, but
`verify_integrity` rejects a missing tracked file. Should upgrade-only recovery
remain allowed with failed integrity, or should restoration be required? The
latter loses accepted scope and needs a Maintainer-approved Scope delta.

### 8. Nested Git paths during upgrade — delivered

The [archived proposal](../proposals/archive/2026-10-29-codex-nested-git-upgrade.md)
and [archived plan](../plans/archive/2026-10-30-nested-git-upgrade.md) record
the completed implementation, clean wide verification and both independent
reviews. Upgrade refuses `.git` components in supplied and resolved project
paths, including lockfile destinations, caches and staged names. Ordinary
contained links and lookalikes remain valid. The conservative trailing-dot/space
rule can refuse distinct POSIX names; hard links under other names and
post-check races remain outside the protection. Certification and any
Maintainer-run AST ceremony are separate from this plan.

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

### 16. Clean customized upgrade merges — rejected

The [proposal](../proposals/archive/2026-10-30-codex-upgrade-semantic-adoption.md) was
rejected as framed. The Maintainer retained #35 for a smaller, lower-burden
redesign; no engine implementation is authorized. A clean merge may still
retain conflicting policy, and the requested incorporation-or-disposition
outcome remains undelivered.

### 17. Refuse linked files during lockfile migration — delivered

The [proposal](../proposals/archive/2026-10-30-codex-init-lock-linked-files.md)
was accepted at `06af4aeb` after Security Review clearance at `52a7feb3`.
Implementation is complete in the [archived plan](../plans/archive/2026-10-30-init-lock-linked-files.md).
`--init-lock` refuses links at mapped installed paths before existence checks
or reads in a stable tree. Legitimate linked installs must replace the linked
file or folder with an ordinary copy before migration. The separate
fidelity-manifest reader and concurrent path replacement remain outside this
check, as the archived plan records.

### 18. Publish and check the GitHub Release — delivered

The [accepted proposal](../proposals/archive/2026-10-30-codex-tag-release-distinction.md)
and [archived plan](../plans/archive/2026-10-30-tag-release-distinction.md)
delivered a publication step, manual notes and link review, a read-only check
against the independently recorded gate commit, and signed-tag guidance.
The check does not verify cached archive bytes. Push and publication remain
separate Maintainer actions.

### 19. Refuse ambiguous module discovery markers — delivered

The [accepted proposal](../proposals/archive/2026-10-30-codex-module-marker-ambiguity.md)
and [archived plan](../plans/archive/2026-10-30-module-marker-ambiguity.md)
delivered refusal of malformed, nested or crossed generated markers before
planning, inventory or lock changes, including an empty roster. Inline, indented
and blockquoted mentions remain prose. Edited markers require reconciliation.

### 20. Pass local API credentials to the dispatcher — delivered

The [accepted proposal](../proposals/archive/2026-10-30-codex-api-dispatch-credentials.md)
and [plan](../plans/archive/2026-10-30-api-dispatch-credentials.md) record
delivery.

### 21. Plan evidence and sidecar rules — delivered

The [accepted proposal](../proposals/archive/2026-10-30-codex-plan-evidence.md)
and [plan](../plans/archive/2026-10-30-plan-evidence.md) record the
single-plan default and evidence rules.

### 22. VER-5 discovery behavior checks — delivered

The [accepted proposal](../proposals/archive/2026-10-30-codex-ver-5-coverage.md)
uses independently listed expected files for seven existing multi-script modules
to compare fresh installation, lock records, selected-module upgrade additions
and scan targets. The Maintainer accepted these checks as the v0.6 response;
they do not establish every future file or upgrade state, and no new traversal
was added. Review and focused verification passed.

### 23. Reduce template burden — delivered

The Maintainer accepted the [proposal](../proposals/archive/2026-10-30-codex-template-burden.md)
on 2026-11-01. The [plan](../plans/archive/2026-11-01-template-burden.md) trims four
existing templates and corrects a contradiction while preserving installed
guidance, obligations and machine consumers. Reviews and focused verification passed.

### 24. Narrow incidental test-selector matches — delivered

The [accepted proposal](../proposals/archive/2026-11-01-codex-selector-matching.md)
excludes demonstrated incidental matches while retaining identified real
consumers and required checks. On the collision plan's inputs, selection fell
from 51 files to 41; time saved has not been measured. Review and focused
verification passed.

### 25. Remove the pending certification marker — delivered

The Maintainer accepted the [proposal](../proposals/archive/2026-11-01-codex-certification-label.md)
at `8d1c6bde`. The [completed plan](../plans/archive/2026-11-01-certification-marker.md)
removed the marker while retaining the checks, triggers and actual-run evidence.

### 26. Make proposals easier to decide — delivered

The [reviewed proposal](../proposals/archive/2026-11-01-codex-proposal-decision-summary.md)
puts the problem, proposed change and meaningful tradeoffs together at the
start of a proposal, before implementation detail. The existing Plain Language
standard already calls for clear conclusions, definitions and examples, so no
new general rule or review stage is proposed. The Maintainer accepted it at
`c25427ce`; the [completed plan](../plans/archive/2026-11-01-proposal-decision-summary.md)
updated both proposal templates and passed review and focused verification.

### 27. Give the shipped board a clearer layout — accepted

The [proposal](../proposals/archive/2026-11-01-codex-shipped-board-layout.md)
was accepted at `01acbdb8`. Its [plan](../plans/2026-11-01-shipped-board-layout.md)
awaits ordinary and Security plan reviews; it coordinates one template rewrite
with the documentation audit and preserves existing project boards.

## Issue triage, staffing and close-out

Issue #33 asks that certification mean scoped checks. The accepted proposal
instead removes the misleading pending marker while retaining whole-tree
certification. Issue #35
remains for redesign. Issue #19 is
deferred to v0.7. The roadmap no longer lists a closure follow-up for #2 or #8;
this briefing does not assert current hosted issue status.

Staffing: **Terra coordinates and reviews; Luna implements reviewed plans; Sol
handles strategy and Security judgment.** Model tiers remain vendor-neutral in
shipped text. Decision scribing needs explicit authorization.

This master stays current until its coordinating role retires. Plans own
engineering evidence; this briefing certifies no implementation or release.
