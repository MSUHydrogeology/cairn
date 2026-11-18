# Plan: Run and development rules

**Source proposal**: [Run rules apart from development rules](../proposals/archive/2026-11-16-claude-run-and-development-rules.md)
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-18
**Rules that apply**: `dev/rules/protected-surfaces.md`, `dev/rules/conventions.md`, `dev/rules/working-agreements.md`
**In brief**: Give projects an optional place for run rules and a bounded Operator role while keeping development protections in force.

## Build summary

Document an opt-in separation between running and developing software, add the optional Operator role and its limits, and explain how run rules can accompany a release. Keep the existing governing rules and slots in place. Install and upgrade evidence will show that adopters receive the changes; an independent agent scenario will examine whether the role's prose communicates its limits.

## Source proposal

The Maintainer accepted the heavy proposal as revised, selecting option (a): append the Operator paragraph without moving existing paragraphs. The Decision allows about 80 additional words in `AGENTS.md` beyond the trim's no-growth target and assigns the missing shipped secrets rule to a separate board row. The trim and root rules stub have landed. The broader split requested by issue #79 remains incomplete.

## Scope

Change shipped `templates/core/AGENTS.md` and `templates/core/RULES.md`, their applicable Cairn-owned counterparts `AGENTS.md` and `RULES.md`, shipped `templates/core/dev/rules/README.md` and `dev/rules/README.md`, the two `agent_collaboration.md` files, `docs/methodology/roles.md`, and both copies of `issue-capture.md` and `model-selection.md` under `templates/modules/team-gated/` and `dev/modules/`. Apply local differences deliberately rather than overwrite adopter-owned text. Read the other User Agent references identified in the source and update only if needed to preserve their meaning. This touches governing and deliberation doctrine. No release module, citation checker or broader entry-file split is included.

**Reuse.** N/A: no code added. Use existing installed homes, public installer and upgrade paths, and protection controls. Run rules are opt-in and add limits only; no installer question or parser is added.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Add governing Operator limits and run-rule guidance | Reviewed plan; measure current cap | Core and local rules and guidance |
| C2 | Align role, capture and model guidance | C1 | Role doctrine and module copies |
| C3 | Verify installed behavior and reconcile issues | C1–C2 | Evidence, fixes and issue records |

## Acceptance criteria

**C1.** Append one Roles paragraph to shipped `AGENTS.md`: an Operator edits no tracked file or lifecycle step; switches explicitly to development and follows all development rules for changes to code, data handling or credentials; takes only added limits from `RULES.md`; captures defects and uses the capture-versus-fix rule after switching. If a cited `dev/` file is absent, change nothing, do not fetch it elsewhere, and ask. Preserve every existing paragraph, heading, slot and keep-list duty, including review caps, Maintainer authority, tier and governance floors, session-start and note safety, explicit-path commits, push and plan fences. Mirror the applicable limits locally without replacing local rules. Measure shipped `AGENTS.md` + `VENDOR.md` + `RULES.md` against 1,500 words and the local always-loaded set against its 2,000-word limit. If short of room, shorten other additions or seek a Maintainer cap change; never move keep-list duties. Guidance says opting in means writing root run rules, which ship whole, do not cite development rules and never relax `AGENTS.md`; development rules may cite them. The template retains its development pointer, explains its removal for a release without `dev/`, and states that shipped `AGENTS.md` pointers into `dev/` are the permitted release exception.

**C2.** Add optional Operator to both rosters and their roster-slot example without editing the roster sentence in `AGENTS.md`. Operator runs software under run rules, may reproduce and diagnose a defect and files it in the tracker. Narrow User Agent to exercising Cairn from an adopter's position; retain its user-seat debugging and capture-versus-fix guidance and have Operator refer to it. Both capture modules apply that same boundary to Operator. Both model tables specify low for capture only, medium for diagnosing a cause, and development's own floor after switching. Neither role becomes mandatory.

**C3.** A clean public install and a representative upgrade show the governing and module changes in their actual installed homes, including preservation of adopter-owned `RULES.md` and its opt-in nature. Exercise existing protection controls on the changed protected surfaces. A fresh independent agent receives only changed `AGENTS.md` and a filled `RULES.md`, including a conflicting instruction to fix, commit or push; give it a defect scenario and record whether it captures, switches or asks as required, including absent `dev/` guidance. This is evidence of comprehension, not a mechanical guarantee against an agent ignoring prose. Close issues whose entire accepted scope is implemented at their fixing commits; record remaining #79 scope honestly. No human trial, release, repin or passive wait blocks completion.

## Scope delta

**Scope delta**: preserved.

## Verification

Select tests with `python tests/tier_inventory.py for <changed paths>` and run only those naming changed files, plus prose gates and `claim_check` for documents. Do not add wording or pin tests for prose; automate only public install/upgrade output promises or existing protection controls where a real gap remains. The public entry points are the installer and upgrade commands, with installed files as outputs. Record inputs, results and limits; use a fresh independent agent for role behavior, which tooling cannot simulate. The existing Security Review reads old and new governing text for lost or weakened duties; deletion of the `RULES.md` reading instruction is a known failure that this read must detect. A malicious run rule can still persuade a noncompliant agent, so this boundary remains prose. The parent schedules one joined Group 4 integration run; record its relevant result without claiming other groups' checks as this plan's own.

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
