# Proposals and plans list the rule files that apply

**Author**: Claude Fable 5.2 (Strategy)
**Model**: Claude Fable 5.2 (`claude-fable-5-2`)
**Date**: 2026-11-12
**Status**: draft
**Type**: design-exploration
**Surfaces this would feed**: the v0.8 template-trim proposal (the "Trim bulk from the Cairn templates" row in [`dev/PLANNING.md`](../PLANNING.md)); the proposal and plan templates; [`RULES.md`](../../RULES.md) and its shipped starter

## Summary

Each proposal and plan should name, in one header line, the rule files that apply to its work. The author picks them from the routing table in `RULES.md`. The agent that carries out the work then reads the plan and those files, and does not need every project rule in context. This adds to the `RULES.md` router; it does not replace it. The Maintainer agreed the direction on 2026-11-12 ("I like all of this"). It is not a Decision; the change would go through the v0.8 template-trim proposal.

## The question

The Maintainer, 2026-11-12: local rules can get very long, and agents should not carry all of them in context all the time. Could proposal and plan templates list the rules that apply, so an agent reads only those?

## Method

Word counts are `wc -w` at commit `6e687b14`. I read `RULES.md`, the `dev/rules/` README, both Cairn templates' headings, and the v0.8 rows of the roadmap. I did not read any adopter project's rules, and I did not measure how often an agent misses a routed rule today.

## Findings

**What is read, and when (measured).**

| Text | Words | When it is read |
|---|---|---|
| `AGENTS.md`, `CLAUDE.md` and `RULES.md` | 1,474 | every session |
| Seven files in `dev/rules/` | 1,872 | on demand, by the router's "When you…" table |
| `dev/agent_collaboration.md` | 5,535 | on demand, by section |
| Cairn's plan and proposal templates | 9,170 | whenever one is written |

The shipped set is `AGENTS.md` 1,111, `VENDOR.md` 310 and the `RULES.md` starter 60, which is 1,481 words.

**The every-session cap moved.** The cap on the three always-loaded files was 1,500 words (Maintainer, 2026-11-10). On 2026-11-12 the Maintainer raised it: "I don't think we can really keep the cap on every session to 1,500. Let's up that to 2,000." `RULES.md` now says 2,000.

**The router depends on the acting agent noticing.** `RULES.md` routes by trigger: "When you edit an engine… read `dev/rules/protected-surfaces.md`". Each agent must recognize, at the moment it acts, that a row applies. Nothing records which rows applied to a piece of work, so a reviewer cannot check it.

**A plan already names what it touches.** The plan template's Scope section asks for the surfaces touched. The rules are keyed to surfaces and actions. So the author can choose the rule files once, when the plan is written.

**The executor has the least context.** Cairn sends execution of an accepted plan to the lowest model tier. That agent gains most from a short, exact reading list.

**Assumed, not measured:** that adopter rule folders grow faster than Cairn's own. Cairn's seven files are small today; the concern is about growth.

## Options

- **A. Do nothing.** The router alone. No template change. Missed rules stay invisible to review.
- **B. One header line of rule file paths in both templates.** The author fills it from the router table; reviewers check it. About 20 template words.
- **C. Copy the applicable rule text into each plan.** Rejected: copies drift from the rule files, and plans get longer while the living-plans draft is trying to shorten them.
- **D. A tool suggests rule files from the plan's paths.** Possible if each router row carried path patterns. It is a new tool and a new format to maintain.

## Recommendation

Option B, written into the template-trim proposal so the templates get one heavy review, not two.

1. **The line.** Both templates gain one header field: `**Rules that apply**:` followed by rule file paths, or `bright lines only`. Example: `dev/rules/protected-surfaces.md; dev/rules/conventions.md`.
2. **Paths, never rule text.** The rule file is read fresh each time, so the list cannot go stale in wording.
3. **`RULES.md` stays.** Its bright lines apply to all work, listed or not. Trivial fixes, session routines and strategy conversations have no plan to carry a list, so the router still serves them. The router table is also the menu the author picks from.
4. **Not listed does not mean does not apply.** An agent that meets an unlisted rule that applies follows it and adds the file to the line.
5. **Both templates.** A light proposal has no plan; the proposal is its implementation record.
6. **Review.** Proposal and plan reviewers ask whether a rule file is missing, by comparing the line with the Scope section. This is a clause in the existing review questions, not a new pass.
7. **Briefs.** A brief to an implementer or reviewer copies the line as its reading list.
8. **No growth.** The trim row says the templates must not grow. The 20 words come out of the trim's savings, and no test pins the wording.
9. **Option D waits.** Revisit it if hand-written lines are missed in practice.

Residual risk: an author who does not know a rule cannot list it. The router has the same weakness today. This change moves it to one place that a reviewer reads.

For adopters, the v0.7 `RULES.md` starter (roadmap item 23) gives every install a router, so the line always has a table to draw from.

## Open questions

1. **Shipped cap.** A test in the item 23 candidate (`bootstrap/tests/test_scaffold.py`, "installed guidance uses … words") holds the shipped three files to 1,500 words. Does the 2,000 cap apply to what Cairn ships too? Default: leave the shipped limit at 1,500, because a tighter limit on shipped text is safe and the test belongs to a plan in implementation.
2. **Collaboration-guide sections.** The same line could cite sections of `dev/agent_collaboration.md`, which is where the larger reading saving is (5,535 words). Not sized.
3. **Living plans.** If the living-plans draft is accepted, the line is revised in place when Scope changes. Confirm the two proposals agree when both are written.
