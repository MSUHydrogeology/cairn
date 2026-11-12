# A style guide for Cairn, a short agent version, and an onboarding task that starts one

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: awaiting-review
**Waiting on Maintainer**: release draft for review
**Review**: usual + Security Review
**Proposed tier**: heavy — it edits shipped modules, presets and the rules README, which are high-risk surfaces today; the pending template-scan proposal would change that.
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-12
**In brief**: Cairn would get a human-first style guide and a much shorter agent version in its rules, and every new install would put "write a style guide" on its board with guidance on how.

## Decision summary

Cairn has a writing style guide (Cairn Plain Language) but no code style guide, and tells adopters almost nothing about writing one. LHM and modflow_tools each wrote theirs by hand, at 2,080 and 1,616 lines. This proposal adds a human-first `docs/style_guide.md` for Cairn, a short agent version in `dev/rules/conventions.md`, a short "style guide" section in the `documentation-plan` module on how a project makes both, one relaxed line in the rules README, and one seeded onboarding task in each preset. A note at the top of the style guide is the whole sync mechanism: no test, check or generator pins the two guides together, and drift between them is acceptable. The cost is five small edits to shipped text and one new Cairn document; no tool is added. Target: v0.8, after the repository layout.

## Context

Measured 2026-11-12. Cairn has no style guide for code. Its only guidance for adopters is about 40 lines in `docs/methodology/doc-governance.md` on where one can live, a directory adopters do not receive. `dev/rules/README.md` line 31 lists "naming/style" as not belonging in the rules folder. `dev/rules/conventions.md` holds 117 words. LHM and modflow_tools open the same way (a why-paragraph, a quick-reference table) and keep a short extract in `RULES.md` or `AGENTS.md`. Cairn's own habits (SPDX header, standard library only, `from __future__ import annotations`, injectable `out` and `err`) were seen in one file, `tools/test_tiers.py`, not surveyed. Onboarding tasks come from `templates/onboarding/*.md`, are seeded once at install, and are not backfilled.

Maintainer, 2026-11-12:

> "I think actually that we need a separate style guide for agents (Which probably does belong in rules) that is way shorter. The docs one should be for humans primarily, but kept in sync (not with a pin, but a note in the style guide)."

> "Let's make this a v0.8 proposal right now. And at the top of the style guide, just include a note about making sure to keep them in sync with the relevant conventions. If they diverge it's not a big deal. Pinning things is though."

## Proposal

1. **`docs/style_guide.md`** (name set by the Maintainer): a why-paragraph, a source-of-truth line, a quick-reference table, then short topical sections. Cairn Plain Language is linked, not copied. A read-only survey of `tools/`, `scripts/` and `bootstrap/` comes first: describe what the code does, and add a rule only where the survey finds a real inconsistency.
2. **Agent version** in `dev/rules/conventions.md`: one-line rules, about ten, each pointing to the guide rather than shortening its paragraphs. Add "write or change code" to the existing `RULES.md` routing row for that file (about five words; the three capped files were 1,474 of 1,500 words on 2026-11-12).
3. **The sync note**, the first lines of the guide: keep this guide in sync with the agent conventions in `dev/rules/conventions.md`; if they drift that is acceptable; do not add a test or check that pins them.
4. **Guidance for adopters**: a section under 300 words in the `documentation-plan` module (default-on; it already mentions `STYLE_GUIDE.md`): when to write a guide, where it lives, the shape of both versions, the same sync note, no pins.
5. **`dev/rules/README.md`** (Cairn's and the shipped copy): replace the "naming/style" exclusion with a line allowing a short agent extract of a style guide, the guide being the source of truth.
6. **Onboarding seed** `write-style-guide` in each preset file. Greenfield: set conventions as you write the first code. Legacy: describe what the code already does and invent nothing. Team: agree and record. Each task produces both files and names the section in item 4. Existing projects are not backfilled.

Order: after the repository layout (final paths) and roadmap item 23, the `RULES.md` stub. Until the stub ships, the task tells a project with no `RULES.md` to put the short list under `AGENTS.md`'s project-conventions section.

## Rationale

Agents pay for every line they load; humans need the reasons. Two lengths serve both, and Cairn's documentation plan already pairs a short operational rule with a longer rationale, updated together. It also warns that a rule stated in full in both files drifts, which is why the agent version is one-liners that point to the guide. Seeding a task costs a few lines of board text and puts the work where each project already looks.

## Alternatives considered

- **Host the guidance in `architecture-review`.** Rejected: that module is team-gated and selected only when a codebase's design accreted; almost every code project needs a style guide.
- **One guide.** A long one costs agent attention on every use; a short one loses the reasons humans need.
- **Pin or generate the pair.** The Maintainer rejected pins; a generator needs a machine-readable source and prose has none.
- **A new module.** More shipped weight than five small edits.
- **Do nothing.** Each adopter writes a 1,600 to 2,000 line guide from scratch, or none.

## Documentation / doctrine surface

Governing layer: none; `AGENTS.md` is unchanged. Rules and deliberation: `dev/rules/conventions.md`, `dev/rules/README.md` and its shipped copy, one `RULES.md` row. Descriptive layer: the new guide. Shipped: the `documentation-plan` module and three onboarding presets.

Rate-limit gate: not one incident. Two adopters and Cairn's own gap are the same need recurring.

Proposed paths:
- `docs/style_guide.md`

## Evidence / verification plan

Falsifiers: a fresh install of a preset lacks the task; the guide's first lines lack the note; any test or check names the guide and the agent version together.

### Tests required

Promise: a fresh install of each preset seeds `write-style-guide` once into the onboarding slot, and a repeat install leaves the board unchanged. Public entry: the scaffold install, through the existing install-time onboarding tests, as one parameterized test over the three presets. No test pins the guide, the agent version or their sync. The reviewer answers "does any rule weaken or disappear?" for the README edit.

Security preflight: N/A: no trust boundary added or widened; the seed lines pass through the existing writer.

Independent scientific check: N/A: no scientific assumption or result touched.

## Signals the change is wrong

- Two releases on, new projects' boards still carry the task unchecked: drop the seed.
- The agent version passes about twenty bullets: it has become the long guide; cut it.
- An agent follows a stale short rule to a wrong result: revisit the sync by asking the Maintainer, not by adding a pin.

## Scope delta

**Scope delta**: preserved. This is the opening text; nothing has been dropped.

## Assurance path

**Assurance path**: high-assurance
