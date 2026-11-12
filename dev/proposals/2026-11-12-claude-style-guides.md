# A style guide for Cairn, a short agent version, and an onboarding task that starts one

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: awaiting-decision
**Review**: usual + Security Review
**Proposed tier**: heavy — shipped modules, presets and the rules README are currently high-risk surfaces. The pending template-scan proposal grants no exemption or grandfathering; retain required Security Review and plan review.
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-12
**In brief**: Cairn would get a human-first style guide and a much shorter agent version in its rules, and every new install would put "write a style guide" on its board with guidance on how.

## Decision summary

Cairn has a writing style guide (Cairn Plain Language) but no code style guide, and tells adopters almost nothing about writing one. This proposal adds a human-first `docs/style_guide.md`, a short agent extract in `dev/rules/conventions.md`, installed adopter guidance, and a task in every preset to create both. A note is the whole sync mechanism: no pin, test or generator. Optional style preferences may drift; binding security, dependency and license duties remain operative in their routed homes. This adds prose and onboarding text, not tooling. Target: v0.8, after the repository layout fixes final paths.

## Context

Measured 2026-11-12. Cairn has no style guide for code. Its only guidance for adopters is about 40 lines in `docs/methodology/doc-governance.md` on where one can live, a directory adopters do not receive. `dev/rules/README.md` line 31 lists "naming/style" as not belonging in the rules folder. `dev/rules/conventions.md` holds 117 words. LHM and modflow_tools open the same way (a why-paragraph, a quick-reference table) and keep a short extract in `RULES.md` or `AGENTS.md`. Cairn's own habits (SPDX header, standard library only, `from __future__ import annotations`, injectable `out` and `err`) were seen in one file, `tools/test_tiers.py`, not surveyed. Onboarding tasks come from `templates/onboarding/*.md`, are seeded once at install, and are not backfilled.

Maintainer, 2026-11-12:

> "I think actually that we need a separate style guide for agents (Which probably does belong in rules) that is way shorter. The docs one should be for humans primarily, but kept in sync (not with a pin, but a note in the style guide)."

> "Let's make this a v0.8 proposal right now. And at the top of the style guide, just include a note about making sure to keep them in sync with the relevant conventions. If they diverge it's not a big deal. Pinning things is though."

## Proposal

1. **`docs/style_guide.md`** (name set by the Maintainer): a why-paragraph, an authority line, a quick-reference table, then short topical sections. Link Cairn Plain Language, not copy it. First survey `tools/`, `scripts/` and `bootstrap/` read-only: describe existing practice; add a rule only for a real inconsistency.
2. **Agent version** in `dev/rules/conventions.md`: about ten concise, actionable entries, with guide links for explanation, not as substitutes for duties. Preserve dependency-budget, standard-library, placement, naming, canonical-home, license and retry duties. Add "write or change code" to its `RULES.md` routing row. Cairn's own three-file cap is 2,000 words (`RULES.md`); the shipped set retains 1,500 (Maintainer record f20de75d). Remeasure both at implementation; the earlier 1,474 figure is not current evidence.
3. **The sync note**, first in the guide: keep both versions aligned; optional preference drift is acceptable; no synchronization pin or check. The guide explains preferences; routed agent conventions govern coding decisions, subject to binding higher-level rules. Neither guide nor drift tolerance grants a security, dependency or license exception. Report discrepancies and propose a correction; do not silently replace a binding rule with descriptive guidance.
4. **Guidance for adopters**: under 300 words in the default-on `documentation-plan` module, installed at `dev/modules/documentation-plan.md`, heading "Style guide": when, where and how to write both versions, the sync note and authority distinction. Use the adopter's installed `docs/DOCUMENTATION_PLAN.md` for placement, not Cairn-only `docs/methodology/` links. Keep duties usable in installed authoritative files; source-doc citations supply context only.
5. **`dev/rules/README.md`** (Cairn's and shipped): allow a short operative agent extract while leaving descriptive explanations in the guide. Retain `RULES.md` indexing and all other exclusions.
6. **Onboarding seed** `write-style-guide` in all three presets: greenfield sets conventions with first code; legacy records existing practice without invention; team agrees and records. Each produces both files and points to the installed "Style guide" section in item 4, using a path relative to the installed board. Existing projects are not backfilled. If the module is explicitly deselected, retain the task with self-contained guidance rather than an unavailable link.

Order: after the repository layout (final paths) and roadmap item 23, the `RULES.md` stub. Until the stub ships, the task tells a project with no `RULES.md` to put the short list under `AGENTS.md`'s project-conventions section.

## Rationale

Agents pay for every line they load; humans need the reasons. Two lengths serve both: actionable agent duties stay short, with links for explanation. Seeding a task puts the work where each project already looks.

## Alternatives considered

- **Host the guidance in `architecture-review`.** Rejected: that module is team-gated and selected only when a codebase's design accreted; almost every code project needs a style guide.
- **One guide.** A long one costs agent attention on every use; a short one loses the reasons humans need.
- **Pin or generate the pair.** The Maintainer rejected pins; a generator needs a machine-readable source and prose has none.
- **A new module.** More shipped weight than five small edits.
- **Do nothing.** Each adopter writes a 1,600 to 2,000 line guide from scratch, or none.

## Documentation / doctrine surface

Project-owned governing detail: `dev/rules/conventions.md`, `dev/rules/README.md` and its shipped copy, one `RULES.md` row; shared `AGENTS.md` is unchanged. Descriptive layer: the new guide. Shipped: the `documentation-plan` module and three onboarding presets.

Rate-limit gate: not one incident. Two adopters and Cairn's own gap are the same need recurring.

Proposed paths:
- `docs/style_guide.md`

## Evidence / verification plan

Falsifiers: a fresh install of a preset lacks the task; the guide's first lines lack the note; any test or check names the guide and the agent version together.

### Tests required

Promise: each fresh preset install seeds the task once; reinstall preserves project-owned board text. Extend `bootstrap/tests/test_onboarding_slot_substitution.py` through the public scaffold entry, parameterized across all three presets, to follow the board reference to the installed guidance section; cover module opt-out without a dangling reference. Retain reinstall coverage in `bootstrap/tests/test_onboarding_seed_roster.py`. No test pins guide wording or synchronization. Review checks retained duties, authority and README exclusions.

### Security preflight

Required because shipped templates are high-risk, even without a new parser or writer.

- **S1 -- Inputs:** Maintainer-reviewed module and preset prose enters existing seed extraction, roster filtering and rendering in `bootstrap/_scaffold/install.py`; profile selections and target files are project-controlled. Task text does not authorize code execution or exceptions to governing rules.
- **S2 -- Failure evidence:** At implementation, remove a seed, break its installed reference, and enable board reseeding separately; record each affected public-install check failing. Expectations come from promised task presence, installed section existence and preserved project text, not copied seed bytes. These mutations have not been run in this proposal-only revision.
- **S3 -- Trigger and coverage:** At implementation run `python -m pytest bootstrap/tests/test_onboarding_slot_substitution.py bootstrap/tests/test_onboarding_seed_roster.py` for all three presets, opt-out and reinstall. Adopter-facing promise: "Create a human guide and short agent conventions using the installed Style guide section; existing boards are not backfilled." Installation checks verify delivery, not semantic agreement between guides.
- **S4 -- Failure direction:** Preserve existing roster filtering, seed syntax, safe-write/path checks, dry-run and project-owned-board protection. Malformed/missing seed content can omit guidance, not confer authority; fail delivery verification rather than claim success. Module opt-out uses self-contained task guidance; no fallback loads inaccessible source docs or relaxes binding duties.
- **S5 -- Residual attacker:** A project writer can alter board or guide prose and inject semantically hostile instructions. This change does not detect that class: review and installed authority rules remain necessary. Existing containment/divergence protections remain; advisory synchronization is no security control.

Independent scientific check: N/A: no scientific assumption or result touched.

## Signals the change is wrong

- Two releases on, new projects' boards still carry the task unchecked: drop the seed.
- The agent version passes about twenty bullets: it has become the long guide; cut it.
- An agent follows a stale short rule to a wrong result: revisit the sync by asking the Maintainer, not by adding a pin.

## Scope delta

**Scope delta**: preserved. Both guides, advisory sync, adopter guidance, all-preset onboarding and the v0.8 layout prerequisite remain; authority and delivery are clarified.

## Assurance path

**Assurance path**: high-assurance

## Review -- Terra Medium -- 2026-11-12

Reviewed commit: be015399831b62898f10696191cd60b1b325a6c1

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

The strongest case is to give people the reasoning behind local code conventions, give agents a concise working reference, and make creating both a visible onboarding task without adding a synchronization pin.

**Foundations**

1. **Should this happen as framed?** The outcome is useful, but the guidance destination and conflicting-authority behavior need clarification before acceptance. -- `bootstrap/_scaffold/config.py` documentation-plan mapping; proposal items 1-6
2. **Best alternative.** Keep a concise agent-owned rules list and an explanatory guide, with an explicit resolution for disagreement and an installed reference to the guidance; no pin is needed. -- `dev/rules/README.md` lines 10-22; proposal item 3
3. **What would show it wrong?** In fresh installs of all three presets, follow the seeded task from the board to the guidance and produce both files; a missing or inaccessible destination falsifies the onboarding outcome. -- `templates/onboarding/solo-greenfield.md`; `bootstrap/_scaffold/config.py` documentation-plan mapping

1. **Non-blocking.** Item 4 places guidance in the module, while the installer separately installs that module as `dev/modules/documentation-plan.md` and the forkable plan as `docs/DOCUMENTATION_PLAN.md`. Item 6 must identify the installed section, not merely its source; specify the adopter-facing path and test the board reference on each fresh install. -- `bootstrap/_scaffold/config.py` documentation-plan mapping
2. **Non-blocking.** The guide is called the source of truth, yet drift is acceptable and the short rules are the agent's routed instructions. A disagreement has no stated operational resolution. Specify which governs a coding decision and how to handle a discrepancy without requiring a pin. -- proposal items 2-5; `dev/rules/README.md` lines 10-22
3. **Non-blocking.** The summary cites a 1,500-word cap, but the reviewed `RULES.md` sets 2,000. Correct the figure and remeasure the three files at implementation; do not treat the old figure as a current rule. -- `RULES.md` Bright lines; proposal item 2

**Audience / rule loss:** Replacing the README exclusion is intentional; preserve its distinction between descriptive docs and routed agent duties, including the existing requirement to index project rules from `RULES.md`.

**Coverage:** Read the committed proposal, module mapping, README and a preset; did not run installs or verify the sibling-project line counts. The template-scan proposal may change the review process for this shipped prose, not this proposal's promised outcomes. Security Review is separate.

## Review -- Sol High -- 2026-11-12

```
Reviewed commit: be015399831b62898f10696191cd60b1b325a6c1
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown
**Model basis**: coordinator's explicit Sol High assignment.

The strongest case gives humans explanations and agents compact operational
guidance, seeding both through existing onboarding without synchronization
machinery.

**Foundations**

1. **Should this happen as framed?** The split is useful, but authority needs
   clarification. -- `docs/DOCUMENTATION_PLAN.md`, installed-authority rule
2. **Best alternative.** Keep both documents and advisory synchronization,
   distinguishing style preferences from binding development constraints. --
   `dev/rules/conventions.md`, dependency, licensing and placement duties
3. **What would show it wrong.** A missing seed or reinstall changing
   project-owned board text falsifies delivery. --
   `bootstrap/tests/test_onboarding_slot_substitution.py`,
   `TestInstallPath::test_preset_install_inlines_seeds_only`;
   `bootstrap/tests/test_onboarding_seed_roster.py`,
   `test_reinstall_never_reconciles_board_and_updates_inventory`

1. **Blocking: preflight incorrectly N/A.** Current protected-surface rules
   include shipped templates; the pending exemption grants nothing. Close with
   S1-S5 covering seed parsing/rendering, installed guidance and retained
   installer protections. -- `dev/rules/protected-surfaces.md`;
   `dev/proposals/_template.md`, Security preflight
2. **Non-blocking: bound acceptable drift.** Items 2-5 could make descriptive
   guidance appear to override operative conventions. Close by stating that
   drift tolerance concerns style preferences, preserves existing binding
   duties and grants no security or dependency exception. --
   `dev/rules/conventions.md`; proposal items 2-5

**Audience / rule loss:** A short agent extract is reasonable. Keep actionable
duties in conventions, not solely behind human-guide links; preserve the
README's remaining exclusions.

**Coverage:** I traced preset extraction and onboarding delivery, confirmed
default-on module registration, the 117-word conventions figure and sibling
guides' 2,080/1,616 lines from committed files. Not covered: proposed wording,
future layout, install execution or sibling revision provenance. This records
the initial pass after ordinary-review serialization, not another pass.

## Response -- Sol High -- 2026-11-12

**Role**: revising author (security/authority clarification), requested Sol High tier.
**Elapsed**: unknown
**Tokens**: unknown

1. Ordinary 1: adopted. Items 4/6 name the installed module section and placement authority; public-install verification follows the board reference for every preset, including module opt-out behavior.
2. Ordinary 2: adopted. Items 2/3/5 distinguish explanatory preferences from operative conventions, resolve coding authority and preserve routing and exclusions without a synchronization pin.
3. Ordinary 3: adopted. Item 2 distinguishes Cairn's current 2,000-word cap from the retained shipped 1,500-word limit and requires remeasurement.
4. Security 1 (blocking): adopted. Replaced N/A with explicit S1-S5 covering inputs, falsification, triggers, failure direction and residual attackers. Heavy assurance remains; no future template-scan exemption is assumed. Mutation/install evidence belongs to implementation and is not claimed here.
5. Security 2: adopted. Drift tolerance is limited to optional preferences. Existing dependency, placement, naming, license and retry duties remain actionable in conventions; no descriptive guide overrides binding security or dependency rules.

Additions answer these findings; no baseline outcome is removed. Top reread: summary now prepares the reader for both guide lengths, installed guidance, advisory sync and binding authority. No remaining design choice beyond the Maintainer's acceptance/tier Decision; final paths await the retained layout prerequisite. No new review pass is requested.

### Withdrawn / superseded commitments

- Unqualified guide-as-source-of-truth and drift permission: replaced with explanatory-guide/operative-conventions authority and preference-only drift.
- Preflight N/A: replaced with S1-S5 because shipped prose is currently high-risk.
- The 1,474-of-1,500 current-Cairn claim: replaced with separate current and shipped caps and implementation remeasurement.
- Source-only task reference: replaced with installed guidance and module-opt-out fallback; delivery scope preserved.
