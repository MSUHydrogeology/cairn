# Plan: Retire the doctrine folder

**Source proposal**: dev/proposals/archive/2026-10-28-codex-governing-text-single-source.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Move public methodology to its chosen home and remove the old folder while preserving installed duties and working checks.

## Source proposal

The accepted proposal requires an inventory and Maintainer routing choice before moving rules, with complete duties in installed homes and checks of actual installed reach. The archived plan's C2 records the choice of `docs/methodology/` for public methodology, usable installed homes for complete duties, and `dev/rules/` for project-specific rules; it made no relocation. The Maintainer reaffirmed in chat on 2026-11-01 the intent to remove `doctrine/` entirely. The archived plan completed its separate simplification and comparison; this plan executes the remaining relocation, not that work again.

## Scope

Move useful current methodology, preserve installed duties and their usable pointers, update live references and path-dependent behavior, then remove `doctrine/`. Preserve historical records as history; ensure their treatment does not mask broken live claims or make standing checks fail. Update active governing text, templates, documentation plan and its shipped counterpart where routing changes; preserve deliberate adopter differences. Coordinate with `dev/proposals/2026-11-01-codex-plain-language-docs.md`: carry forward completed improvements and leave its full reading review to that work, including material at all final homes. No redirects, permanent ledger, evidence folder, generator or new general-purpose tool.

**Reuse.** Search `doctrine/`, `docs/`, `templates/`, `bootstrap/`, `scripts/` and `tools/` for old paths and readers; existing `scripts/check_cairn.py`, shipped claim/link checks, installer and tests already perform the relevant jobs. Adapt them rather than add a parallel checker. Refresh the existing inventory against the implementation base; it is not a complete current consumer map.

### Documentation / doctrine surface

Public methodology lands in `docs/methodology/`, cross-cutting prescription in governing and installed files, Cairn-specific rules in `dev/rules/`, and deliberation remains in `dev/`. A published explanation is not an installed duty. The documentation plan and its forkable template must agree on their structural routing while retaining their intended differences.

Proposed paths:
- `docs/methodology/`

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Refresh content and consumer mapping; identify exact installed homes, live paths, pins, tests and any unresolved duty | Plan reviews; coordinate affected writers | Concise mapping in implementation record before edits |
| C2 | Move material and migrate active references and consumers, including affected tests and protected copies; remove old folder | C1 establishes homes and checks; unresolved home or new trust boundary stops work for reassessment | Destination guidance and working consumers |
| C3 | Independent code and Security Reviews, then final wide integration | C2 iteration checks and reviews; fixes receive required targeted look | Verification and review records |

## Acceptance criteria

### C1

Reconcile every current doctrine file with the existing section inventory, source changes since it, its final home and installed reach. Search tracked live references, readers, path classification, config/install mappings, generated output and byte pins; validate negative searches with a known positive. Identify historical references separately, and map each changed duty and consumer to tests and real entry points before editing. Unresolved meaning, installed home or mandatory pointer blocks the affected move.

### C2

Useful explanation and complete duties remain accessible with the same meaning; no obligation is replaced by a published citation. Current live links, claims and installed pointers resolve as intended. Historical records retain their meaning without weakening live-path detection. The folder is gone, path classifiers still detect non-installed dependencies, and required identical session helpers remain byte-identical. Updated guards pass intact real installs and fail on removed or inverted operative clauses; preserve distinct semantics. No unresolved required check or known broken consumer is treated as complete.

### C3

Ordinary and Security Reviews inspect committed implementation and iteration evidence. Final wide Boundary B covers the reviewed range and review fixes on a clean final commit. Record omissions and non-passes; unresolved criteria and checks block archive.

## Scope delta

**Scope delta**: preserved. The source plan's completed simplification and comparisons remain in its archived record; this plan does not claim to redo them or remove accepted outcomes.

## Verification

**Boundary A:** Before edits, run `python tools/test_tiers.py for <changed paths>` and run its selected tests during iteration, plus applicable claim, link, snippet and neutrality gates. Map and exercise actual readers and installed output. Starting points, to extend from C1:

- `scripts/check_cairn.py` internal-only prefix and loop-fidelity behavior: `bootstrap/tests/test_loop_fidelity_gate.py` and `test_check_cairn_content.py`; verify an intact installed pointer and a deliberately introduced non-installed dependency through the real check, including historical-path handling.
- `bootstrap/_scaffold/config.py` mappings and actual `bootstrap/scaffold.py` installs: inspect small `solo-greenfield` and fuller `high-rigor-legacy` output and affected pointers; use mapped scaffold and install tests. `test_review_sweep_ships.py` exercises installed review guidance, whereas `test_review_and_verification_rules_ship.py` also checks source copies; do not substitute source-only checks for installed reach.
- `test_scope_reduction_trap.py` and `test_doc_governance.py` read specific current doctrine paths and protect distinct semantics; update their actual targets and test meaningful deletion/inversion in installed output when replacing a duty guard. The session helpers in `tools/session.py` and `templates/skills/_lib/session.py` must remain identical; use their mapped session/skill tests and real entry points.
- `scripts/claim_check.py`, `scripts/link_check.py`, `scripts/check_cairn.py`, `scripts/sync_doc_snippets.py` and `scripts/quality_gate.py --sub neutrality` provide applicable prose checks. Confirm each trigger and input set; use existing snippet check mode where applicable, not an unreviewed rewrite of source examples.

**Boundary C:** A reviewer other than the implementer independently falsifies the committed result with tight targeted checks, not a suite. The separate Security Review remains required. A review fix beyond a failing test returns for the required targeted look.

**Boundary B:** After reviews, run the mapped iteration and integration/workflow selections plus relevant standing gates in wide mode on an unchanged clean commit under canonical Python 3.13. Record full SHA and range, interpreter, clean pre/post state, commands, counts, time, token use or `unknown`, non-pass dispositions and omissions; retain timing diagnostics and slow-test reporting. Certification is separate and is not authorized by this plan. Do not re-anchor per plan; the deferred v0.6 cut ceremony retains its existing authority and checks.
