# Give the shipped board the current board's layout

**Author**: Codex (gpt-6.1-sol)
**Status**: awaiting-decision
**Review**: usual + Security Review
**Proposed tier**: heavy — a shipped methodology template is a protected surface.
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Give new projects a board that puts Maintainer decisions first and makes each release's next steps easy to scan.

## Decision summary

Adopters start with a board organized by queued and active work, while Cairn's current board puts decisions for the Maintainer first and presents release work in a three-column table. Give the shipped board that shape while keeping its existing duties and installation behavior. The tradeoff is a rewrite of protected guidance, requiring careful comparison and review; existing projects' boards remain theirs.

## Context

`dev/PLANNING.md` has “Waiting on you,” release tables, terms and agent working rules. `templates/core/dev/PLANNING.md` instead leads with project status, onboarding, queued and active sections and carries detailed archive and removal duties. Its onboarding slot is filled by `bootstrap/_scaffold/install.py`; `tools/board.py` recognizes a Maintainer wait only on its own suitably formatted line, not inside a table cell. `bootstrap/tests/test_scope_reduction_trap.py` protects scope-reduction wording.

## Proposal

Rewrite the shipped board around “Waiting on you” first, release sections with Work, Next step and Record columns, a short terms list, and working rules clearly marked for agents. Include guidance and an example that put each Maintainer wait on a standalone bulleted marker line outside any table, so the existing board reader finds it. Keep project-status and onboarding slots and their install-time behavior, including preset metadata and seed tasks; retain the existing archive, disposition, scope, date, coordination and removal duties. Preserve the scope wording guarded by the named test. Do not add a tool or process. Preserve user-owned boards during upgrades; do not replace or restructure them automatically.

Coordinate the rewrite with `dev/plans/2026-11-01-plain-language-docs.md` so that plan's owner reads the final board and the template is rewritten once. The accepted documentation audit remains responsible for its full reading and marker requirements.

## Rationale

A shared layout helps a Maintainer see decisions and next actions immediately. Keeping marker lines outside tables respects the existing parser; preserving slots and duties avoids making presentation changes alter installation or governance.

## Alternatives considered

Leave the template as it is: this avoids a rewrite but leaves new adopters with a less actionable layout than the current board. Changing the parser to accept table cells adds software and a second contract when a standalone line already works.

## Documentation / doctrine surface

The shipped board is installed guidance and deliberation in `templates/core/dev/PLANNING.md`; this proposal is deliberation in `dev/`. No governing policy or software behavior is intended to change.

## Evidence / verification plan

### Tests required

Map actual readers, byte pins, slot and upgrade consumers before editing using `python tools/test_tiers.py for templates/core/dev/PLANNING.md` and searches with a known-positive control. Exercise the real install with and without a profile, including seeded onboarding and both slot markers; exercise an upgrade with a customized existing board and verify its user-owned content and layout survive, allowing existing onboarding-slot reconciliation. Exercise `tools/board.py --maintainer` with a standalone bullet and a table-cell marker, confirming only the former is reported. Run the mapped tests including `bootstrap/tests/test_scope_reduction_trap.py`, onboarding and board-reader consumers. A lost duty, changed seeded behavior, missed wait or overwritten board falsifies the change. Record exact nodes and any missing coverage in the plan.

### Examples / smoke checks

Inspect rendered installed boards and run applicable claim, link, snippet and neutrality gates. The implementation plan must map each named check to its trigger and runner, and use wide final integration for this protected surface. No full-tree certification is authorized by this proposal.

### Security preflight

1. **Inputs:** The installer reads the shipped template and profile preset; the board reader reads board text. The project supplies its own board and profile. This proposal adds no input or decision mechanism.
2. **Failure:** During implementation, remove a slot, invert a guarded scope condition, and move a wait into a table in separate copies; record which real-entry checks fail. These mutations have not yet been run. A check deriving its expected content from the same altered template cannot independently establish preservation.
3. **Trigger and set:** The implementation plan must trace each selected test and prose gate to its runner and inputs, and compare installed guidance with observed behavior. The proposed instruction is to place waits on standalone bullets; the existing reader must report them.
4. **Failure direction:** The rewrite must preserve installer and parser fallbacks and malformed-input handling; no authority or fallback changes are proposed. Verify actual behavior rather than assuming it.
5. **Residual risk:** A project author can edit their board or write misleading instructions; layout and lexical checks cannot prevent that. Semantic preservation depends on review and comparison as well as tests.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Adopters cannot find a next action, a Maintainer wait disappears from the reader, an onboarding seed changes, an existing board is overwritten, or an existing duty is weakened or lost.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance — shipped methodology template and installed guidance; ordinary and Security Reviews remain separate.

## Proposal review -- Codex (gpt-6.1-sol) -- 2026-11-01

**Verdict:** Support as framed; no blocking findings.

**Foundations**

1. **Should it happen as framed?** Yes. The v0.6 board requests decisions first, release tables, short terms and agent rules; the proposal carries each, preserves both installer slots and existing duties, and coordinates the accepted Plain Language audit.
2. **Best alternative.** Retain the present board: it avoids rewriting protected guidance but leaves new adopters with its queued/active layout. The proposed layout addresses the requested usability problem without changing the parser or adding a process.
3. **What would show it wrong?** A lost duty, altered onboarding seed, overwritten customized board or missed wait would defeat the proposal. Its verification plan calls for real installs and upgrade, parser exercises, reader mapping and comparison; `tools/board.py` confirms that a marker in a table cell is not a standalone wait.

**Coverage:** Read the proposal at 75b4bb0b against the v0.6 board item, shipped board, board reader and accepted Plain Language plan. Did not run installs, tests or mutations, inventory all readers, or assess future wording. Separate Security Review remains due.

**Elapsed:** approximately 2 minutes; **Tokens:** unknown.

## Proposal Security Review -- Codex (gpt-6.1-sol) -- 2026-11-01

**Tier**: Security Review

**Foundations**

1. **Should it happen as framed?** Yes. Presentation can change without transferring authority: the proposal preserves archive, disposition, scope, coordination and removal duties, whose existing installed wording distinguishes the governing source and reserves scope concessions to the Maintainer (`templates/core/dev/PLANNING.md`, Archive preconditions and Removal preconditions).
2. **Best alternative.** Keep the current template. This avoids semantic drift but retains the usability problem. Standalone waits and existing slots achieve the requested layout without expanding parser behavior or introducing another mechanism (`tools/board.py`, `_roadmap_waits`; `bootstrap/_scaffold/install.py`, `install_onboarding`).
3. **What would show it wrong?** Lost authority conditions, invisible waits, changed seeds or overwritten customized content. The proposal requires independent comparison, real installs, an upgrade and separate mutations; these target the relevant failure paths rather than treating a template-derived expectation as proof (Evidence / verification plan; Security preflight).

**Verdict:** Support as framed; no blocking findings. Preserve the complete duties, including disposition eligibility, quoted authorization, serialization points and all three removal prerequisites; passing the scope wording test alone cannot establish that preservation. The proposal already requires this broader comparison. Module adoption can reconcile generated onboarding blocks, so preserve existing slot behavior while preventing automatic board restructuring (`bootstrap/_scaffold/upgrade.py`, `_prepare_module_discovery_updates`).

**Elapsed:** approximately 4 minutes; **Tokens:** unknown.

**Coverage:** Read committed `02563167`, the ordinary review, installed board duties, installer slot handling, upgrade discovery handling, scope-test obligations and accepted audit coordination. Did not execute installs, upgrade, parser checks or mutations, inventory every consumer, or establish equivalence of future wording.

## Proposal review response -- Codex (gpt-6.1-sol) -- 2026-11-01

**Elapsed**: approximately 2 minutes; **Tokens**: unknown.

Both reviews support the proposal without blockers. Security advice accepted: compare all duties, including eligibility, quoted authorization, serialization and all three removal prerequisites, rather than relying on the scope test alone; the proposal already requires retaining those duties. Clarified upgrade verification to allow existing onboarding-slot reconciliation while preserving user-owned content and layout. The Plain Language audit coordination and single rewrite remain in scope.
