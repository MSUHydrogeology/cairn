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

## Code review -- Codex (gpt-6.1-sol) -- 2026-11-01

**Reviewed:** `bae1d930`; **Verdict:** blocking check remains open.

**Foundations**

1. **Should it happen as framed?** Yes. The template puts waits first, retains both slot placeholders and the archive and removal preconditions, and gives each release table the accepted three columns (`templates/core/dev/PLANNING.md`; implementation diff).
2. **Best alternative.** Retain the old board; that avoids rewriting but leaves the requested decision-first layout undelivered. The existing reader already supports the standalone marker, so a parser change adds no necessary capability (`tools/board.py`, `_roadmap_waits`).
3. **What would show it wrong?** A missed wait, changed seed or loss of a customized board. The implementation record reports reader checks and slot mutation, but the upgrade check below remains incomplete.

**Blocking finding:** C1 requires a real upgrade preserving a customized board's content and layout. The implementation record says the upgrade was staged with a conflict and the resolved apply was not exercised. Staging and unchanged live bytes do not establish the outcome after applying the upgrade. Close by completing the real upgrade, resolving the conflict as needed, and recording the resulting content and layout against the original, including permitted onboarding reconciliation.

**Elapsed:** approximately 3 minutes; **Tokens:** unknown.

**Coverage:** Read committed proposal, plan, implementation diff and full rewritten board, including onboarding, marker guidance and removal duties; inspected the author's recorded checks. No tests or upgrade were rerun. Did not independently establish seed behavior, inspect rendered installs, or test malformed inputs. Security Review and final Boundary B remain separate.

## Code Security Review -- Codex (gpt-6.1-sol) -- 2026-11-01

Reviewed commit: `bae1d93076f7833b4628fcb4975f9869b0ea3d47`.
Target: shipped board rewrite. Prior findings: none.
**Obligation:** Internal Security Review

**Foundations**

1. **Should it happen as framed?** Yes. The layout retains authority: the complete Archive preconditions block is byte-identical to the parent, and the three removal prerequisites remain (`templates/core/dev/PLANNING.md`, committed comparison).
2. **Best alternative.** The single-template rewrite using existing installer and reader is the smallest adequate build. Both slot blocks compare byte-for-byte with the parent; no onboarding contract change is needed (same comparison; `bootstrap/_scaffold/install.py`, slot substitution).
3. **What would show it wrong?** A lost duty, false or hidden wait, or overwritten customization. In a separate snapshot of the reviewed commit, the actual `python tools/board.py --maintainer` returned zero waits for the shipped sample, then exactly one standalone bullet while ignoring a table-cell marker. These targeted probes passed under Python 3.12.9; the apply path remains unmeasured.

**Verdict:** No security defect found; the ordinary review's blocking upgrade check remains open. I concur with its evidence and satisfier: staged conflict preservation cannot establish preservation after applying an upgrade. This is the same finding, not an additional obligation.

**Bounding:** WIDER RUN REQUIRED for the named customized-board upgrade apply path. Final Boundary B remains due.

**Elapsed:** approximately 6 minutes; **Tokens:** unknown.

**Coverage:** Read committed proposal, plan, original and rewritten guardrails, slots and reader; compared slot and archive-block bytes and exercised the actual board CLI in an isolated copy. Did not execute installs or upgrades, inspect rendered installed boards, exercise every fallback or malformed input, or run final wide integration.

## Implementation verification -- Codex (Implementation, gpt-6.1-sol) -- 2026-11-01 (follow-up)

In an isolated copy, installed the pre-rewrite source at `7f9a0710` into a
fresh `solo-greenfield` adopter, committed a custom release row and an appended
`Adopter notes` section, then staged and applied the upgrade from `cc784445`.
`upgrade --plan` and `upgrade --stage` showed the expected `dev/PLANNING.md`
conflict. I resolved it with the new release-table layout, carried the local
board wording forward, placed the custom row in the current-release table, and
kept the appended local note. `upgrade --apply` succeeded, applied 17 files,
and advanced the lock and base cache to `cc784445`.

After apply, the custom row and note remained; the board had no conflict
markers. The profile and onboarding block retained `solo-greenfield`, all six
preset seed entries, and all six module-task entries. Both onboarding tour
documents remained installed. The upgrade materialized `dev/.cairn/profile.yml`
from the lockfile. Running `python tools/session.py session-start` from the
adopter root completed successfully and resolved the adopter's local Python
binding.

Python 3.12.9. Elapsed: approximately 4 minutes; tokens: unknown. This closes
the customized-board apply check only. No broad suite, fallback or malformed-
input checks, or final Boundary B integration run were performed; Boundary B
remains due under canonical Python 3.13.x.

## Targeted code review -- Codex (gpt-6.1-sol) -- 2026-11-01

**Reviewed:** `510c2085`; **Verdict:** prior upgrade-check finding closed.

**Foundations**

1. **Should it happen as framed?** Yes. The follow-up reports a completed real upgrade from the old board, including conflict resolution and apply; the custom row, note and onboarding entries remained.
2. **Best alternative.** Rely on the earlier staged conflict alone; it did not show the applied result, so it could not meet C1's upgrade check.
3. **What would show it wrong?** A post-apply loss of custom content or onboarding data would contradict the reported result. The record specifies the source revisions, customizations and observed post-apply state.

**Disposition:** The reported focused check closes my finding at `cc784445`. I relied on the implementer's record and did not rerun the upgrade or a suite. This disposition does not close the separately owed Boundary B checks.

**Elapsed:** approximately 1 minute; **Tokens:** unknown.

**Coverage:** Read the committed follow-up and prior finding. Did not inspect the isolated adopter or test other upgrade cases, fallback behavior or malformed input.

## Implementation verification -- Codex (Implementation, gpt-6.1-sol) -- 2026-11-01

**Boundary B mode:** wide. The changed surface is shipped board guidance. Its
consumers include install and upgrade slot handling, onboarding seeds and the
public board reader. The mapped selection includes all named integration and
workflow consumers; a narrower run would leave those consumers uncovered.

**Reviewed range:** `af8d1263e07ea64a64b77ebbecf6086a1a0b4f99` to
`bae1d93076f7833b4628fcb4975f9869b0ea3d47` (the one-file board rewrite);
final tested endpoint: `c575881d808c837308385bbf1c2ea387877441dc`. The code
review was recorded at `cc7844457f176bb506b32f30fcc78c10bd847f17`, Security
Review at `4be6b1ee17cda9264b6e6fc0a93ac5dcea69770c`, the completed upgrade
evidence at `510c20850399c15b08cb9c53b6cb92f449c6a2cf`, and its targeted review
disposition at the tested endpoint.

**Interpreter/runtime:** `/private/tmp/flopy312-trial/python313/bin/python`,
Python 3.13.18. No per-worktree interpreter binding was present; this is the
Python 3.13 runtime used for the required final run.

**Pre-run state:** clean clone at the tested endpoint above.
**Post-run state:** clean clone at the same endpoint; no tracked or untracked
changes. The command `python tools/test_tiers.py for
templates/core/dev/PLANNING.md` selected 20 test files. The plan file itself
selected zero files. The selected set included six integration files and five
workflow files; all 20 were run.

| Command | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---|
| `python tools/test_tiers.py for templates/core/dev/PLANNING.md` | 0 | 20 files selected; 6 integration and 5 workflow files | about 0.3 s | unknown |
| `python -m pytest -q` on the 20 mapped files listed by that command | 0 | 1,024 passed; no failures, skips, xfails or xpasses reported | 120.51 s | unknown |
| `python scripts/claim_check.py` on the plan and board | 0 | Both files clean on the tested snapshot | under 0.1 s | unknown |
| `python scripts/link_check.py` on the plan and board | 0 | 2 files scanned; no issues on the tested snapshot | under 0.1 s | unknown |
| `python scripts/claim_check.py dev/plans/2026-11-01-shipped-board-layout.md` after appending this record | 0 | Final plan bytes clean | under 0.1 s | unknown |
| `python scripts/link_check.py dev/plans/2026-11-01-shipped-board-layout.md` after appending this record | 0 | Final plan bytes clean | under 0.1 s | unknown |
| `python scripts/sync_doc_snippets.py --check` | 0 | 502 documents scanned; no drift | 0.065 s | unknown |
| `python scripts/quality_gate.py --sub neutrality` | 0 | 0 failures; 43 informational findings | 0.636 s | unknown |

The integration and workflow files selected were `test_intents_tool.py`,
`test_onboarding_seed_roster.py`, `test_onboarding_slot_substitution.py`,
`test_replacement_tools.py`, `test_skills_onboarding.py`,
`test_verify_stems.py`, `test_finalize_retired_living_state.py`,
`test_install_time_onboarding.py`, `test_quickstart_sequence.py`,
`test_upgrade.py`, and `test_upgrade_module_additions.py`. The other nine
selected files were `test_board_json_contract.py`, `test_core_dev_folders.py`,
`test_hardening.py`, `test_scope_reduction_trap.py`,
`test_next_session_local_note.py`, `test_module_merge_lockfile.py`,
`test_verify_integrity.py`,
`test_upgrade_edit_check_runs_no_project_programs.py`, and
`test_upgrade_lockfile_path_containment.py`.

**Plan-specific acceptance commands:** The real customized-board upgrade
`--plan`, `--stage` and `--apply` check is recorded above under the follow-up
verification: apply succeeded for 17 files and preserved the custom row, local
section, profile and onboarding entries. The standalone-versus-table wait
reader check is recorded in the Security Review above. Those checks were not
repeated during this mapped run; the tested board bytes are unchanged from
those checks. The selected install tests inspect generated slot and seed
content and run the reader, but do not establish a full inspection of fresh
rendered boards with and without a profile. No separate full-board inspection
is recorded; that plan-specific check remains open.

**Non-pass disposition:** None. The neutrality gate's 43 informational results
were not failures.

**Known omissions:** No test was omitted from the mapped 20-file selection.
The final pytest run did not emit per-file durations. The earlier mapped run
recorded `test_upgrade_module_additions.py` at 28.60 seconds under Python
3.12.9; retain it on the test-consolidation list. The earlier 1,024-test run
took 139.54 seconds and exceeded the 30-second iteration target; this final
wide run took 120.51 seconds, within the three-minute integration target.
Installer/parser fallback and malformed-input mutations were not run. The
full-board inspection described above is not recorded. Full-tree certification
and re-anchor were not authorized by this plan.

The plan remains open until the fresh rendered-board inspection is recorded.

**Elapsed:** approximately 2 minutes for the mapped test run, plus under 1
second for the standing gates; **Tokens:** unknown.


## Rendered fresh-install inspection -- Codex (Implementation) -- 2026-11-01

Rendered three fresh targets from the isolated shipped source with Pandoc to
HTML and plain text: `solo-greenfield`; no preset with the explicit default-on
module list; and a minimal config with only `project_name` and `test_command`,
which the installer resolved to the default-on set. All targets started empty,
without an adopter-side profile file. A config file is required, so a literal
config-less install is unsupported and was not exercised.

All three renders contain two release tables with Work, Next step and Record.
The sample wait renders as a separate indented bullet outside the tables; the
installed board reader reports zero waits. Both slot markers remain in the
Markdown comments, and project-name substitution is visible. The preset case
renders six `[seed; id: ...]` tasks plus six module tasks. Both no-preset cases
render six module tasks and no preset seed IDs.

The rendered boards visibly show the external-path annotation above the title
and preset seed IDs as task text. Both were already present before the rewrite
(`bae1d930^`). The no-preset board says onboarding comes from a selected preset
although it receives module tasks; the same preset-only description was also
in the pre-rewrite board. Pandoc output was inspected; no browser screenshot
was captured because the browser blocked local `file:` URLs. No tests were run.

**Elapsed:** approximately 4 minutes; **Tokens:** unknown.
