# Plan: Refresh release roster and held guards

**Author**: gpt-6.1-terra (Implementation, Medium)
**Source proposal**: dev/proposals/archive/2026-11-18-terra-release-roster-and-guards.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-18
**Rules that apply**: dev/rules/conventions.md, dev/rules/protected-surfaces.md, dev/rules/working-agreements.md, dev/rules/development-environment.md
**In brief**: Refresh native release-test classifications and retire only guards whose protections remain demonstrably covered.

## Build summary

Reconcile the release roster with current native Mac and Windows behavior, repair the identified skip cases, and resolve the 28 held guards without losing their public protections. Assess eligible redundancy in the named claims-tool test file. Record the evidence and complete the required reviews before the separate release operations.

## Source proposal

The accepted heavy proposal selects Option B: retire only eligible held guards alongside the roster refresh, keeping any whose protection is not established. The Maintainer authorized one further focused Security Review of the old capped code in commit `8ac332b4`, for the precise question and scope below.

## Scope

Change `tests/security_manifest.py`, affected tests and fixtures, and existing shipped-source, parity or release-procedure references only as needed to carry out the accepted dispositions. The prepared `prep/windows-roster-refresh` commits are historical inputs, not current truth. Reconcile current collection and native outcomes, including deleted IDs, 20 now-Windows-capable Git route nodes, 15 previously missed Windows-only nodes, `test_rules_folder_offer.py::test_count_command_and_offer_text`, the illegal-filename call-phase skip in `contract/test_board_closeout_warning.py::test_warning_escapes_untrusted_name_and_never_shows_closeout`, four fixture skips in `test_upgrade_removes_retired_files.py`, and in-body symlink-privilege and POSIX skips. Only genuine opposite-platform setup skips belong in the roster. Account for Gitleaks, Bandit and Vermin availability; missing tools, unexpected skips, xfail and xpass cannot become a strict pass.

Recover the historical 28 rows from Git before `546959c1` and reconcile each to its current owner and named duties. A High-tier assessment identifies each public promise, distinct protection and retained public witness before any removal; keep an unproven guard. Resolve roster, shipped-source, parity and procedure references with each eligible retirement. Assess private-helper and same-branch redundancy only in `tests/test_intents_tool.py`, preserving public warn-default, explicit-block and distinct refusal classes. The claims Decision lifts that file's fence alone; it does not authorize other claims-family cuts.

**Reuse.** Inspect `tests/security_manifest.py`, `release/security_check.py` and existing tests and fixture owners for classifications, public witnesses and the outcome validator. Reuse those entries and `tests/tier_inventory.py`; no new permanent tool or mutation ledger. No doctrine surface changes. Documentation changes, if needed, stay in their existing shipped or release homes.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Reconcile current native roster and repair named skip behavior | Reviewed plan; current native evidence | Roster and focused test/fixture repairs |
| C2 | Assess 28 holds and eligible claims tests; retire proven redundancy and resolve references | C1; High-tier protection assessment | Retained public witnesses, eligible removals and references |
| C3 | Run focused native checks, independent reviews and joined integration | C2 | Evidence and review dispositions |

The Maintainer's exact authorization was: “Accept both as revised, choosing Option B and authorizing the one scoped Security Review pass on #1, implemented in the plan.” The question is: “would removing the identified held guards leave a public path to unsafe writes, bypassed containment or a false release-gate pass without a retained check?” Scope: proposed guard removals, their retained public witnesses, and affected roster/reference changes. The one authorized code pass may also cover applicable new roster changes once; it does not reset the old cap or authorize an informal preliminary old-code review. Any further capped-code pass requires new explicit Maintainer authorization and a specific unresolved security question. Independent ordinary and Security plan reviews remain required.

## Acceptance criteria

**C1.** Current native outcomes and collection identity support each roster classification. Each named case is resolved by actual behavior; unsupported setup, call-phase and in-body skips cannot be disguised as opposite-platform setup skips. Required nodes are not silently omitted; missing tools and unexpected skip, xfail or xpass outcomes leave the strict release record unpassed. The existing release outcome validator is the public gate.

**C2.** Each historical hold has a current disposition and named public promise; removals have an existing or focused public-entry witness for each distinct protection and correctly resolved named duties. Otherwise the guard stays. Claims pruning preserves default warning, explicit blocking and distinct public refusal classes. No unrelated claims fence is lifted.

**C3.** Native Mac and Windows evidence names candidate, commands, interpreters, tool availability, outcomes and gaps. Focused public checks demonstrate passing behavior and one representative negative per changed refusal class. Independent ordinary code review and the authorized focused Security code review resolve findings; the arc owner runs one integration after connected work. A failed or missing check remains unpassed.

## Scope delta

**Scope delta**: preserved.

## Verification

Before implementation use `python tests/tier_inventory.py for <changed paths>` to select tests naming changed files and focused public-entry nodes. Use current source inventory and known-positive controls for negative searches. Run the applicable checks on native Mac with `/Users/kendal30/conda_envs/lhm/bin/python3.13` and native Windows in the existing local UTM environment, including previously skipped paths; record exact commands, versions and results. Use existing scripts and readers, not a new ledger or one test per helper. For changed prose run claim, link, snippet, neutrality and prose-integrity gates, and inspect readers and byte pins. Independent scientific check: N/A, as accepted.

The Maintainer's re-anchor and actual certifying records are separate named board waits with their owner, required evidence and link to this implementation; they remain unpassed until their evidence exists. This plan neither performs nor signs a baseline, and routine release operations do not gate its final chunk. Elapsed: unknown; tokens: unknown.
