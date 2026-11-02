# Plan: Shipped board layout

**Source proposal**: dev/proposals/archive/2026-11-01-codex-shipped-board-layout.md
**Status**: ready-to-implement
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

## Plan review -- Codex (gpt-6.1-sol) -- 2026-11-01

**Obligation:** Internal

**Verdict:** Support as framed; no blocking findings.

**Foundations**

1. **Should it happen as framed?** Yes. C1 carries the accepted layout and preserves the slots, installed duties and existing boards. The documentation plan's coordination record at `260231cd` assigns this plan the single rewrite and retains its final-board audit.
2. **Best alternative.** Keep the existing template: it avoids a rewrite but leaves the requested decision-first layout undelivered. Reusing the installer and reader avoids another behavior contract.
3. **What would show it wrong?** A lost duty, changed seed, overwritten custom board or invisible wait. C1 and verification require comparison with the original, real installations and upgrade, and mutations. `_roadmap_waits` in `tools/board.py` recognizes a marker at the beginning of a line after an optional bullet, not inside a table cell; the standalone example and real-entry check address that constraint.

**Elapsed:** approximately 3 minutes; **Tokens:** unknown.

**Coverage:** Read plan at `2662ddf9`, accepted proposal, original template, board reader and documentation coordination commit. Did not run installs, upgrades, tests or mutations, inventory all consumers, or assess future rewritten wording. Separate Security Review remains owed.

## Plan review -- Codex (gpt-6.1-sol), Security Review -- 2026-11-01

Reviewed commit: `2662ddf9` (operative plan); ordinary review: `90e2ac3c`.
Target: C1, safeguards and verification. Prior findings: none.
Assurance path: high-assurance, inherited from the accepted proposal.

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none

**Foundations**

1. **Should it happen as framed?** Yes. C1 preserves authority as well as layout: disposition eligibility, quoted authorization, serialization and all three removal prerequisites remain explicit. Comparing with the original prevents a rewritten test from silently redefining those duties (`templates/core/dev/PLANNING.md`, Archive and Removal preconditions; plan C1).
2. **Best alternative.** A single template rewrite using existing entry points is the smallest path delivering the Decision. Changing the parser or installer adds a contract without improving the accepted outcome. C1 and Scope retain the existing slots, onboarding metadata and seeds, user-owned content and documentation-owner coordination (`bootstrap/_scaffold/install.py`, `_substitute_slot`; `bootstrap/_scaffold/upgrade.py`, `_prepare_module_discovery`).
3. **What would show it wrong?** A hidden wait, weakened duty, changed seed or overwritten customization. Boundary A requires real installs and upgrade, standalone-versus-table marker checks and separate mutations; `_roadmap_waits` accepts only the marker at a line's beginning after an optional bullet (`tools/board.py`). Independent Security code review and wide final integration remain owed (Boundaries C and B).

**Verdict:** Support as framed; no blocking findings. The existing comparison and real-entry checks are necessary evidence, not reasons to add another process or artifact.

**Elapsed:** approximately 5 minutes; **Tokens:** unknown.

**Coverage:** Read committed plan, accepted proposal, original board duties, reader and slot/upgrade handling, and ordinary review. Did not execute installs, upgrades, tests or mutations, inventory every consumer, or establish equivalence of future wording.

## Plan review response -- Codex (plan author) -- 2026-11-01

**Elapsed:** approximately 1 minute; **Tokens:** unknown.

Both required reviews support the plan without findings. The documentation audit owner confirmed the single rewrite and final-board reading in `260231cd`; the existing scope and checks remain in force.

## Implementation verification -- Codex (Implementation, gpt-6.1-sol) -- 2026-11-01

Changed only the shipped board template. It now opens with Waiting on you,
has current and later release tables with Work, Next step and Record, a short
terms list, and agent working rules. The shared-file signal-read rule,
serialization points, date convention, dispositions and all removal gates
remain. Both install slots and their placeholder bytes match the original;
the template marker is directly below the title.

Before editing, `python tools/test_tiers.py for templates/core/dev/PLANNING.md`
selected 20 files. Searches found install substitution in
`bootstrap/_scaffold/install.py`, upgrade discovery reconciliation in
`bootstrap/_scaffold/upgrade.py`, board waits in `tools/board.py`, and the
scope wording guard in `bootstrap/tests/test_scope_reduction_trap.py`. The
known-positive searches included the existing slot markers, onboarding tests,
and the parser's marker constant. `README.md` describes the installed tools;
the shipped dev README describes PLANNING as queued and active work.

Under Python 3.12.9, the mapped 20-file selection passed: 1,024 tests in
139.54 seconds. This exceeded the 30-second iteration target; the run did not
report per-file durations. Five focused scope, install, seed, slot and reader
files passed 229 tests in 9.40 seconds; `test_upgrade_module_additions.py`
passed 60 in 28.60 seconds. Claim, link, snippet and neutrality gates passed.
The first install-test attempt after editing found changed slot-placeholder
bytes; I restored both original placeholders, then the focused and mapped runs
passed. No installer, parser or malformed-input behavior was changed.

Real-entry checks: the CLI ignored the quoted sample and a table-cell marker,
then reported a standalone bullet. Separate-copy mutations removing the
onboarding slot and inverting the test-pinned scope-cut rule each failed their
mapped install or scope test. An old-template install with a customized board
was staged for upgrade against the new template; the stage exposed a conflict,
kept the custom row and section in the staged file, and left the live board
bytes unchanged. The non-conflicting resolved apply was not exercised.

No tests or implementation files changed. Checks not run: a completed apply
after resolving the customized-board conflict, installer/parser fallback and
malformed-input mutations, and independent code or Security Review. Boundary B
is still due after review on a clean commit under canonical Python 3.13.x.
Elapsed: approximately 7 minutes; tokens: unknown.
