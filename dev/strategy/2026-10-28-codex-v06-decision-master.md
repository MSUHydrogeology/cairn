# v0.6 decision master — editing burden and nimbleness first

**Author**: Codex (Coordination)
**Model**: GPT-6; coordination switched to Terra by Maintainer on 2026-10-28
**Date**: 2026-10-28
**Status**: living
**Type**: living-reference
**Surfaces this would feed**: Maintainer decisions and actions on the five accepted v0.6 plans and the roadmap.

## Purpose and authority

This is the consolidated decision packet for the nimbleness-first v0.6 batch.
The Maintainer authorized continuous reviews and handoffs without check-ins.
The [roadmap](../PLANNING.md) remains the scope inventory; each linked plan owns
its contract and status. This briefing grants no approval and replaces no
Decision. Pushing, publishing, repository settings changes and issue closure
remain unauthorized.

Keep the release boundary: v0.6 makes existing capabilities work; v0.7 adds
capabilities and adopter research. This five-plan batch does not finish v0.6.

## Delivered work and current holds

| Plan | Result |
|---|---|
| [Model floors](../plans/archive/2026-10-28-model-floor-alignment.md) | Implemented, independently reviewed and archived. Local vendor assignments and shipped generic task floors align; 574 mapped passes under Python 3.13.13. Certification/re-anchor debt remains live in the roadmap. |
| [Scoped verification](../plans/2026-10-28-scoped-change-verification.md) | Implemented; 2,700 collected/executed nodes reconciled, five guard cases passed, environment-denied security cases passed with required local capability. Independent example adjudication and ordinary/Security reviews completed. Both reviews hold completion for the prescribed frozen-file ceremony. Later naming examples corrected with 656 mapped passes under Python 3.13.13. |
| [Governing text](../plans/2026-10-28-governing-text-single-source.md) | Routing chosen at `aa9fc08b`, coordination default at `7013de1d`, and document-wide path declarations at `560a178c`. Path instructions updated and the focused review finding addressed at `860481db`; remaining consolidation and ceremony gates stay open. |
| [Test trust boundary](../plans/2026-10-28-test-trust-boundary.md) | Exact roster approved at `3e9f8fc2`; implementation is blocked on approval review of the dormant bridge candidate. Existing protection remains active. |
| [Ordinary test maintenance](../plans/2026-10-28-ordinary-test-maintenance.md) | Reviewed plan; implementation cannot start because the chosen board file contains security defenses and remains protected. |

The source Decisions are `63e315fa`, `f110d263`, `cca436a9`, `cea1299d` and
`439c7b34`. All five plans were authorized; their later explicit fences remain.
Use `python tools/board.py --maintainer` for declared next moves.

## Remaining decisions and actions

### 1. Governing-text routing and two conflicting prescriptions

**Chosen:** move public explanation/reference to the proposed methodology
home under docs; keep complete operating duties in usable installed files and
project-specific rules in `dev/rules/`. The Maintainer chose this routing in
`aa9fc08b`; both rule choices below are also recorded. A separate published methodology has a
purpose, but the inventory found no delivery requirement for the distinct
`doctrine/` location. Moving costs the familiar landmark and citation migration;
a rename alone saves no editing.

Proposed path: `docs/methodology/` (not yet created).

The [inventory and recommendation](2026-10-28-codex-governing-text-inventory.md)
map 190 document headings plus five fenced examples, 55 obligation groups and
21 editing measurements. Fresh installs wrote 69/101 files, without doctrine.
They revealed two conflicts requiring separate choices, rather than an
implied wording cleanup:

| Conflict | Recommended choice and conceded prescription |
|---|---|
| Coordination defaults | **Chosen (`7013de1d`):** block provable live-session conflicts; agents claim intent before editing. Warn for stale/tokenless cases; retain warn/confirm modes and opt-in hooks. Update the different published default. |
| Path declarations | **Chosen (`560a178c`):** an explicitly declared literal path may recur document-wide, with exact matching and provenance. Instructions updated; siblings, descendants, look-alikes and malformed declarations stay unexempted. Checker logic is unchanged. |

Retain all 21 partial-reach obligation groups until a complete appropriate
installed home and usable pointer are demonstrated. Generic prompts or upstream
citations do not replace those duties. Alternatives are retaining the current
publication split, or settling routing while leaving conflicting/partial
obligations untouched. No accepted duty may be lost by consolidation. C3 must
show an actual simpler edit using the two recorded baselines before claiming
improvement; affected frozen tests still wait for the trust-boundary work.

### 2. Approved initial test-protection roster

**Approved:** the [refreshed roster](../plans/2026-10-28-test-trust-boundary/c1b-roster-6cc95fa7.json)
at commit `884e6d53`, raw SHA-256
`188fa76d82744be571bdc7ca91a43d605776b9df5ba0ac729e2cf22af66b8cc4`.
The [classification evidence](../plans/2026-10-28-test-trust-boundary/c1b-evidence-6cc95fa7.json)
contains every file's reason and preserved mechanisms.

It protects **78 test files plus 12 Python controls**, leaving **51 test files
ordinary**. The refreshed census has 5,490 nodes in 129 test files: 3,954 in
protected files and 1,536 in ordinary files. The approved classification
projected 147 frozen paths from the current 197. The implementation adds one
protected roster-data file, making the prospective total 148; that figure awaits
final verification. Approved test membership is unchanged. The boundary is not
yet installed, and no speedup has been measured.

The accepted trust Decision already concedes blanket ordinary-test byte and
node/marker HOLD protection. Ordinary Python can still influence protected
execution; narrower protection is not equivalent tamper resistance. Actual
release skip/xfail/xpass refusal stays. Roster approval authorizes neither
installation nor a waiver of existing ceremony/review obligations. The Maintainer approved the exact list in `3e9f8fc2`; implementation and
independent reviews precede installation.

### 3. Allow a preparatory extraction for the maintenance pilot

**Recommend:** separately authorize relocating only the two named ordinary
methods from the protected board-test file, preserving their class/method names,
and updating the pilot's path. Keep protected helpers and all security cases in
the original file. The exact methods, helpers and witnesses are in the
classification evidence above; the adjacent anti-forgery method stays protected.

Proposed path: `bootstrap/tests/test_board_json_values.py` (not yet created).

This adds extraction, dependency/fault evidence, independent ordinary/Security
reads and the applicable protected-node transition/ceremony. It is new scope,
not already authorized by approving the roster. Alternatives: leave the pilot
waiting, or explicitly accept the outcome loss of a protected-lane pilot. No
other test family is silently substituted. The existing testing-module update
remains required; new simulation guidance stays v0.7.

### 4. Complete the prescribed Maintainer ceremonies

The verification plan remains `revising-code`; ordinary review `f19f4f53`,
Security review `9d813013` and author response `e9928009` preserve the hold.
Its declared next move is the existing frozen-file ceremony: inspect
`python bootstrap/tests/_gate_manifest.py verify` within
`bootstrap/REANCHOR_RUNBOOK.md`, resolve and record discrepancies, then obtain
the applicable Maintainer disposition. This briefing authorizes no manifest
edit, signing, root change or waiver. Certification remains pending.

The path-instruction update also changed the frozen local and shipped checker
module descriptions; their applicable Maintainer ceremony remains owed under the
governing-text plan.

The old-anchor E7 comparison required the accepted two-transition bridge. The
active-mode candidate `bbe5ecb6` passed 1,085 scoped tests, but cannot itself
represent the required dormant first checkpoint. A one-line dormant setting in
`bootstrap/tests/_gate_preflight.py` is prepared and uncommitted. Automatic
approval review rejected its local commit, citing the security impact and
insufficient explicit authorization; it prohibited bypass. The Maintainer must
explicitly authorize that proposed local change before another attempt. The
preliminary code review also has three surviving mutations not yet shown
equivalent; neither independent review is complete.

The trust plan still requires independent code and Security Reviews, then its
Maintainer-only authority transitions/re-anchors and steady-state proof. The
prepared change does not install a boundary or authorize a ceremony.

### 5. Queued convention choice: session handoff marker

A scratch history reproduced the default `Goodnight` search missing a `Handoff:`
commit; the documented generic handoff obligation does not prescribe a subject.
**Recommend:** use the existing `--handoff-marker` option in Cairn now and settle
a canonical/compatible convention before changing adopters' default. No code
changed; this remains queued rather than blocking the four actions above.

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
