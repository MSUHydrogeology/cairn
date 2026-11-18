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
