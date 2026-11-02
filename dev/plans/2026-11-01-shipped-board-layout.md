# Plan: Shipped board layout

**Source proposal**: dev/proposals/archive/2026-11-01-codex-shipped-board-layout.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Give new projects a clearer board while preserving their existing duties and installation behavior.

## Source proposal

The Maintainer accepted the heavy proposal at `01acbdb8`: reorganize the shipped board, preserve its duties and installation behavior, and leave existing project boards under their owners' control.

## Scope

Rewrite `templates/core/dev/PLANNING.md` once in coordination with the owner of `dev/plans/2026-11-01-plain-language-docs.md`, who reads the final board and retains that plan's full audit and marker duties. Preserve installed guidance; no governing policy, parser, installer, new process, or automatic restructuring of existing boards is intended. The doctrine surface is the shipped board's installed guidance. Update existing tests only where needed to verify the accepted behavior.

**Reuse:** N/A: no code added. Reuse the existing installer, upgrade and `tools/board.py` entry points and their tests.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Coordinate the single rewrite, map readers and preserve duties while changing layout; verify installation, upgrade and wait visibility. | Both plan reviews cleared; coordinate with the documentation plan owner before editing. | Shipped board and necessary behavior tests. |

## Acceptance criteria

**C1.** The board starts with Waiting on you, has release tables with Work, Next step and Record, short terms and agent working rules. Guidance and an example put each Maintainer wait on a standalone bullet outside tables; the real board reader reports it and does not report a table-cell marker. Preserve project-status and onboarding slots, preset metadata and seeds, and all existing archive, disposition, scope, date, coordination and removal duties, including eligibility, quoted authorization, serialization and all three removal prerequisites. Compare against the pre-rewrite template, not only a test derived from the new template. Real installs with and without a profile preserve slot and seed behavior. A real upgrade preserves a customized board's user content and layout, allowing existing onboarding-slot reconciliation. Installer and parser fallbacks and malformed-input behavior remain unchanged. The documentation audit owner reads the final board; no second rewrite is planned.

## Scope delta

**Scope delta**: preserved.

## Verification

**Boundary A:** Before editing, run `python tools/test_tiers.py for templates/core/dev/PLANNING.md` and search for readers, byte pins, slot and upgrade consumers; validate negative searches with a known-positive case. Trace each selected test and prose gate from trigger to runner and inputs, record exact nodes and missing coverage. Run mapped tests, including `bootstrap/tests/test_scope_reduction_trap.py`, onboarding and board-reader consumers. Exercise real installs with and without a profile, both slot markers and seeds; a customized-board upgrade; and `python tools/board.py --maintainer` with standalone and table-cell markers. Inspect rendered boards. Run applicable claim, link, snippet and neutrality gates.

In separate copies, remove a slot, invert a guarded scope condition, and move a wait into a table; record which real-entry checks fail and any surviving mutation. Compare all duties against the original and inspect actual installed behavior; a template-derived expectation alone is not independent evidence. The slot is read by `bootstrap/_scaffold/install.py` during onboarding and upgrade reconciliation by `bootstrap/_scaffold/upgrade.py`; `tools/board.py` reads standalone board waits; `bootstrap/tests/test_scope_reduction_trap.py` checks guarded wording. Follow each check to its actual runner and inputs before relying on it.

**Boundary C:** Independent code reviewer falsifies the committed implementation with the tightest targeted checks, reports missing tests and coverage gaps; separate Security code review remains owed.

**Boundary B:** After code review and any targeted re-review, run wide integration on a clean, unchanged final commit under canonical Python 3.13.x: mapped iteration and integration/workflow selections for the reviewed range, affected public paths, standing gates and plan-specific checks. Record the full SHA and range, interpreter, clean pre/post state, commands and counts, elapsed time, tokens or `unknown`, non-pass dispositions, omissions, timing misses and slow-test reporting. A missing check remains open. No full-tree certification or re-anchor is authorized here.
