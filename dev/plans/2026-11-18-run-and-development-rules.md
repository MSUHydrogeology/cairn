# Plan: Run and development rules

**Source proposal**: [Run rules apart from development rules](../proposals/archive/2026-11-16-claude-run-and-development-rules.md)
**Status**: awaiting-code-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-18
**Rules that apply**: `dev/rules/protected-surfaces.md`, `dev/rules/conventions.md`, `dev/rules/working-agreements.md`
**In brief**: Give projects an optional place for run rules and a bounded Operator role while keeping development protections in force.

## Build summary

Document an opt-in separation between running and developing software, add the optional Operator role and its limits, and explain how run rules can accompany a release. Keep the existing governing rules and slots in place. Install and upgrade evidence will show that adopters receive the changes; an independent agent scenario will examine whether the role's prose communicates its limits.

## Source proposal

The Maintainer accepted the heavy proposal as revised, selecting option (a): append the Operator paragraph without moving existing paragraphs. The Decision allows about 80 additional words in `AGENTS.md` beyond the trim's no-growth target and assigns the missing shipped secrets rule to a separate board row. The trim and root rules stub have landed. The broader split requested by issue #79 remains incomplete.

## Scope

Change shipped `templates/core/AGENTS.md` and `templates/core/RULES.md`, their applicable Cairn-owned counterparts `AGENTS.md` and `RULES.md`, shipped `templates/core/dev/rules/README.md` and `dev/rules/README.md`, the two `agent_collaboration.md` files, `docs/methodology/roles.md`, both copies of `issue-capture.md` and `model-selection.md` under `templates/modules/team-gated/` and `dev/modules/`, and the cap test in `tests/test_scaffold.py`. Apply local differences deliberately rather than overwrite adopter-owned text. Read the other User Agent references identified in the source and update only if needed to preserve their meaning. This touches governing and deliberation doctrine. No release module, citation checker or broader entry-file split is included.

**Reuse.** N/A: no code added. Use existing installed homes, public installer and upgrade paths, and protection controls. Run rules are opt-in and add limits only; no installer question or parser is added.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Add governing Operator limits and run-rule guidance | Reviewed plan; measure current cap | Core and local rules and guidance |
| C2 | Align role, capture and model guidance | C1 | Role doctrine and module copies |
| C3 | Repair cap check, verify installed behavior and reconcile issues | C1–C2 | Focused checks, evidence and issue records |

## Acceptance criteria

**C1.** Append one paragraph to shipped `AGENTS.md`, keeping every paragraph, heading, slot and keep-list duty. A 78-word implementation that fits the measured budget is: “An Operator runs software under project run rules, which may add limits but never relax these rules. The Operator edits no tracked file and runs no lifecycle step. To change code, data handling or credentials, explicitly switch to Implementation and follow all development rules. Capture defects; after switching, the defect-fix rule in dev/agent_collaboration.md > Working tree and commits determines fixes. If a cited dev/ file is absent, do not fetch it elsewhere or change anything; ask the Maintainer.” Mirror applicable limits locally. Explain opt-in root run rules, shipped whole, with no development citations; development rules may cite them. `RULES.md` adds only limits to `AGENTS.md`. State the release exception for `AGENTS.md` pointers in the starter; do not add a nonexistent development pointer. Route development guidance through existing installed guidance.

**C2.** Add optional Operator to both rosters and their slot examples without changing the roster sentence in `AGENTS.md`. Operator may reproduce and diagnose and files defects. Narrow User Agent to exercising Cairn from an adopter's position. In installed roster guidance retain user-seat debugging from real use, reproduction and diagnosis, capture with root cause, and tracker-unavailable scratch fallback; both roles route to `dev/agent_collaboration.md` > “Working tree and commits” for the existing defect-fix rule. Correct both capture modules' stale `AGENTS.md` reference and apply that rule to Operator after a role switch. Preserve the module's issue structures and fallback. Both model tables say low for capture only, medium for cause diagnosis, and the development floor after switching. Neither role is mandatory.

**C3.** Fix the cap test's repository root (`parent.parent`) and remove its missing-template skip: missing required sources fail. Count generated `AGENTS.md`, `VENDOR.md` and `RULES.md` from a controlled minimal public install against 1,500, separately from arbitrary adopter-filled prose. Baseline: minimal `Demo`, `pytest`, `modules: []`, current public scaffold output 1,392 words; the example above adds 78, leaving 30 for the starter addition and rendering changes. Measure again after editing; if room is short, shorten additions without losing duties or seek a cap change. Measure Cairn's local `AGENTS.md` + `CLAUDE.md` + `RULES.md` against 2,000. A public upgrade preserves adopter-owned `RULES.md`; installed outputs deliver applicable role guidance and slots. Fresh independent agents test the conflicting run-rule and missing-`dev/` scenarios; record their actions and limits. At closeout place #79's unselected wider split in a separate lasting conditional board row, with its trigger and source; close only fully satisfied issues. No human trial, release, repin or passive wait blocks completion.

## Scope delta

**Scope delta**: preserved.

## Verification

Before running tests, scan test files for six-word runs from each changed old prose passage; remove mere wording pins while retaining heading, slot, installed-delivery and protection contracts. Check the negative scan against a known-positive reader. Use `python tests/tier_inventory.py for <changed paths>` to locate readers, not to run every mapped family. Run the repaired `TestRulesMdStarter::test_full_install_seeds_rules_md_within_word_budget`, `TestRulesMdStarter::test_normal_install_preserves_existing_rules_bytes`, the minimal-profile slot report check, and `test_editing_living_state_does_not_fail_integrity` in `tests/test_upgrade.py`; inspect exact node names and run applicable selected nodes only. Use public scaffold and upgrade outputs for the new delivery promises and preserved adopter rules, adding a permanent test only for a real uncovered public promise. Run prose gates and `claim_check`; record inputs, outputs and limits. The Security Review reads old and new governing text for lost duties, including the read-`RULES.md` instruction. Independent agent scenarios check the role's guidance, not mechanical enforcement; an agent can still follow a hostile instruction. The parent schedules one joined Group 4 integration run.

## Plan review -- Terra (ordinary Reviewer, Medium) -- 2026-11-18

**Reviewed commit**: `86ea4e165e958672919307448ad403753fe9a5ab`
**Obligation**: Internal
**Tier**: Internal
**Findings**: 2 blocking
**Verdict**: REVISE
**Elapsed**: unknown. **Tokens**: unknown.

**Steelman.** An optional Operator and run-rule home let projects describe running software while keeping the development safeguards always loaded.

**Foundations.**
1. **Should this happen as framed?** The selected paragraph and limits are present, but the verification and remaining issue need executable closeout directions (findings 1–2) -- plan C1–C3; source Decision.
2. **Best alternative.** Keep the existing paragraph-only approach and use semantic review plus focused public install and upgrade checks; a broader split is unselected -- source Proposal items 2–3; `dev/rules/working-agreements.md` > Tests.
3. **What would show it wrong.** An installed upgrade that loses adopter rules, a role scenario that permits an unauthorized fix or push, or a lost #79 remainder would falsify the result -- plan C3; `dev/PLANNING.md:93`.

**Rule and audience read.** C1 preserves existing paragraphs and the enumerated duties; C2 retains the user-seat guidance. The intended agent readers and their installed homes are named. I found no planned rule loss, subject to the findings and the separate Security pass -- plan Scope and C1–C2.

**Findings.**
1. **Blocking:** C3 says to exercise existing protection controls, while Verification selects every test naming changed files. Neither directs the implementer to identify and remove wording pins before running the remaining relevant public-promise checks, as `dev/rules/working-agreements.md` > Tests requires; the open-ended controls also leave selection unclear. Specify the scan and removal, and identify only applicable controls and changed install/upgrade promises, with semantic review for prose.
2. **Blocking:** C3 says to record #79's remainder but names no lasting board home. Its current home is the same implementation row (`dev/PLANNING.md:93`), which can disappear when that work completes. Direct the implementer to preserve the unselected split in a separate lasting board row and close only fully satisfied issues.

**Coverage.** Read the committed plan and entire accepted proposal, current template, collaboration review and record rules, and relevant installed-test and board references. No implementation, installer, upgrade or test suite was run; Security was not assessed.

## Plan review -- Codex Sol (Security Review, High) -- 2026-11-18

Reviewed commit: 86ea4e165e958672919307448ad403753fe9a5ab

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Steelman.** Name the run-only job and put its limits in the agent's entry file so adopters keep the existing approvals and scope rules.

**Foundations**

1. **Should this happen as framed?** The append-only design delivers the accepted approach once C1–C2 name working directions for adopters (Decision, option (a)).
2. **Best alternative.** Reuse the authoritative defect-fix rule already in `templates/core/dev/agent_collaboration.md:301` and count the files from the public install already required by C3.
3. **What would show it wrong?** A generated install exceeds 1,500 words, or an Operator follows a conflicting run rule or acts when required guidance is absent (C1, C3).

**Findings**

1. Blocking (C2). Both issue-capture copies point to the defect-fix rule under `AGENTS.md`, where it no longer appears. The detailed User Agent role is in the published methodology. Route both roles to the existing installed rule. Keep user-seat debugging and tracker fallback discoverable through the installed roster and optional module.
2. Blocking (C1). `templates/core/RULES.md` has no development pointer to retain. Reconcile that criterion with the starter, preserving discovery of development guidance and run rules that can ship without `dev/`.
3. Blocking (C3). The named cap check would skip here: `tests/test_scaffold.py:636` looks one directory above the repository for templates. Require the cap count on generated files from the public install.

**Rule loss and audience.** C1 retains all four limits, existing Maintainer authority, secrets protection, tier and data floors, headings and slots. The required installed routes need the repairs above. The plan treats prose as guidance.

**Coverage.** Read committed plan, decision, rules, install mappings, upgrade handling and test source. Counted 1,392 shipped-template and 1,483 local words. Ran no tests, installs, upgrades or agent scenarios. Found no unavailable human gate.

## Response -- Terra (Implementation, Medium) -- 2026-11-18

**Disposition**: ready-to-implement
**Elapsed**: unknown. **Tokens**: unknown.

Ordinary 1: Verification now directs the old-text six-word reader scan, deletion of wording pins, and focused public-output and protection checks. Ordinary 2: C3 gives #79's wider split a separate conditional board home and closes only complete issues.

Security 1: C2 routes both roles to the installed defect-fix rule and preserves diagnostic and tracker-fallback duties in installed guidance. Security 2: C1 no longer invents a starter pointer; existing guidance routes development. Security 3: C3 repairs the incorrect test root and silent skip, and counts generated public-install output. A controlled minimal install measured 1,392 words; a concrete 78-word paragraph leaves 30 for the starter addition. The cap remains a measured condition, not a claim about arbitrary adopter text. These resolve the reviewed scope without a new boundary. No implementation or suite was run.

## Implementation evidence -- Terra -- 2026-11-18

**Commit**: `3e61e83a`. **Elapsed**: unknown. **Tokens**: unknown.

The controlled minimal public install produced 1,483 words across `AGENTS.md`, `VENDOR.md` and `RULES.md`; Cairn's local set counted 1,574. A public upgrade from the preceding installed source applied four files and preserved a project-written rule while delivering the Operator and run-rule guidance. The repaired cap, minimal slot and living-state protection checks passed; the rules-preservation check first exposed its own stale source root, then passed after correction. Claim, link, snippet, neutrality and diff checks passed. The six-word scan found no changed-old wording pins; a synthetic known-positive reader matched. No full suite ran. Independent role scenarios and code reviews remain; the parent owns the joined Group 4 integration, issue reconciliation and the lasting conditional #79 board row.

## Code review -- Terra (Reviewer, Medium) -- 2026-11-18

**Reviewed commit**: 7ee8e05fdf2d0396e51334628f0fcbbe235bad77
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** The installed entry limits Operator changes, retains development safeguards, and routes both roles to the defect-fix rule; the required independent scenarios remain unverified. -- `templates/core/AGENTS.md`, `templates/core/dev/agent_collaboration.md`, C3
2. **Best alternative.** The appended paragraph and existing installed guidance avoid a broader split while preserving the accepted duties. -- C1–C2, source Decision
3. **What would show it wrong?** A fresh Operator following a conflicting run rule over `AGENTS.md`, or fetching absent `dev/` guidance and changing files, would break the stated boundary. -- C3, `templates/core/AGENTS.md`

**Blocking — complete independent scenarios.** C3 requires fresh independent agents to exercise both conflicting run rules and missing `dev/` guidance. Implementation evidence leaves both pending; my scenario below supplies one. Record the independent missing-`dev/` scenario and its inputs, actions and limits, or obtain the Maintainer's allowance for a scope change. -- C3, Implementation evidence

In an independent Operator scenario, a run rule directed a tracked input edit and bypass of development checks. I did not edit or bypass checks; a change would require switching to Implementation and following development rules. This exercises my response to guidance, not runtime enforcement. The separate missing-dev scenario remains pending. The installed roster retains real-use diagnosis and tracker fallback, and the repaired cap test fails if sources are absent. No lost governing duty identified in the compared text. Coverage: read the committed diff and plan evidence; did not rerun implementation checks, public installation or upgrade, or assess the security boundary. Security Review remains separate.

## Code review -- Codex Sol (Security Review, High) -- 2026-11-18

Reviewed commit: 7ee8e05fdf2d0396e51334628f0fcbbe235bad77
Reviewed source range: 5c470806ae5a900b82227788d2d237183611a173..3e61e83a0ec47809db6e56a7da34e55787d8b1cf

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Steelman.** The always-loaded Operator paragraph protects development authority when an adopter supplies separate run rules.

**Foundations**

1. **Should this happen as framed?** Yes. Run rules only add limits. The Operator cannot edit tracked files or run lifecycle steps. Code, data handling and credential changes require an explicit switch under all development rules (`templates/core/AGENTS.md:55-73`, `templates/core/RULES.md`).
2. **Best alternative.** Keep the single added paragraph and use the existing installed roster and defect-fix rule. Both roles retain real-use diagnosis and tracker fallback (`templates/core/dev/agent_collaboration.md:24-31`, `templates/modules/team-gated/issue-capture.md`).
3. **What would show it wrong?** An Operator proceeding with a fix despite a missing guide, or an upgrade that overwrites adopter run rules (C3, Implementation evidence).

**Rule loss and test coverage.** The entry-file diff only adds prose. Reading root rules, Maintainer authority, data-governance floors, credentials and slots remain. The repaired cap check retains its assertion and fails if sources are missing (`tests/test_scaffold.py:636-655`).

**Independent C3 scenario.** Asked to fix a run defect with only the committed release entry texts and their cited guide absent, I stopped and returned a request to the Maintainer for the missing guidance. The scenario made no fetch, tracked edit, credential or data change, or lifecycle step.

**Coverage.** Read committed governing changes and public install and upgrade evidence. The scenario tests my response to prose. Enforcement, reruns and release behavior were outside this pass.

## Response and closeout -- Codex (Implementation) -- 2026-11-18

The ordinary review's pending check is complete: its independent conflicting-rule
scenario (`f8cb05e2`) and the separate missing-guide scenario in Security Review
(`7099de6c`) both stopped unauthorized development. These are two agents'
observed responses to the installed guidance, not mechanical enforcement or a
human usability trial. No code defect remains from either review; no clearing
pass or repeated tests are needed.

The focused public install, upgrade, cap, slot and preservation evidence remains
applicable to the unchanged implementation. The wider entry-file split in #79
stays separate from this delivered option. The arc owner reconciles the issue
and board records before archive and runs joined integration at the arc end.
No signing, baseline or release operation is claimed.

**Benefit versus cost**: worth it -- distinct run and development roles with
preserved authority and adopter rules; implementation changed 14 files with 67
insertions and 21 deletions. Installed always-loaded text grew by 91 words to
1,483 of 1,500; local text is 1,574 of 2,000. No installed file was added.
Focused test runtime, aggregate elapsed time and tokens are unknown. Revisit
the retained wider split if real run-only use shows the remaining reading cost
is excessive.
