# Test names outlive the plans that produced them

**Author**: Claude (Strategy)
**Model**: Claude Opus 5 (`claude-opus-5`)
**Date opened**: 2026-08-13
**Status**: reviewed
**Touches**: `AGENTS.md` and `templates/core/AGENTS.md` (the `**Naming.**`
paragraph); a bounded, mechanical rename of ~30 test classes in
`bootstrap/tests/`, sequenced after their owning plan archives
**Related**: `doctrine/doc-governance.md` (routing); the archived
`scope-reduction-trap`, whose review rounds surfaced this
**Plan review**: not required(no plan — one convention paragraph plus a
mechanical rename, no sequencing, no deferred follow-ups)

## Context

A test name is read at **failure time**, usually months later, usually by
someone who was not there. It has one job: say what broke.

**217 of 3546** test names in `bootstrap/tests/` (`as_of 2026-08-13`) instead
carry a *lifecycle coordinate* — the plan chunk or review finding that produced
them:

```
class TestP2AmendmentBScopeReduction
class TestP2AmendmentDMalformedNeverMeansReady
class TestCF1AssurancePathOnTheEvent
class TestP1AuthoringTemplates
```

`P2` is a chunk in a plan. `Amendment B` is a revision made on a particular
afternoon. `CF1` is a carried-forward finding. None of that is in the failing
test's file, and none of it is knowledge a future maintainer has.

**Cairn has a sharper version of this than most repositories.** These
coordinates point into plan artifacts, and Cairn's own glossary says an archived
artifact is history: *"read it for context, do not edit it, and never mine it
for metrics."* So the name refers a reader to a document the methodology tells
them not to go rummaging in — and which, once archived, is not maintained.

### The damage is narrower than the names suggest

The **leaf** names are almost all correct:

```
test_a_declared_reduction_with_no_allowance_refuses
test_every_emphasis_spelling_of_the_declaration_triggers
test_the_declaration_is_read_from_the_header_only
```

Behaviour, no coordinate. So a failure today reads:

```
TestP2AmendmentBScopeReduction::test_a_declared_reduction_with_no_allowance_refuses[degraded]
```

The half that tells you what broke is already durable. The coordinate is in the
**container**. That is why this is a small change rather than a rewrite.

### What I checked and did *not* find

I expected to find coordinates already colliding across plans — two `P2`s
meaning different things. **They do not.** Every `P2` reference outside
`review-efficient-lifecycle` is prose citing that plan's chunk, not a second
definition. The argument here rests on **legibility over time**, not on a
collision that exists today, and it should not be strengthened past that.

## Proposed paths

* `AGENTS.md` and `templates/core/AGENTS.md` — the `**Naming.**` paragraph,
  which today covers file names and says nothing about tests
* `bootstrap/tests/` — the bounded rename

## Proposal

### 1. The convention

Add to the `**Naming.**` paragraph in both `AGENTS.md` copies:

> **Tests are named for the property they pin, never for the plan chunk or
> review finding that produced them.** A test name is read at failure time by
> someone who was not there: `test_a_declared_reduction_with_no_allowance_refuses`
> tells them what broke; `TestP2AmendmentB` sends them to an archived plan the
> lifecycle tells them not to re-read. **The docstring carries the reason** —
> *why the obligation exists*, in plain terms — not the finding id, which
> identifies nothing to a reader without that plan open. Provenance already
> lives in `git blame` → the commit body → the plan.

This is not "delete the history"; it is "write the history into the sentence
rather than a label pointing at it." The sibling proposal
`2026-08-13-claude-finding-tags-are-not-reasons` states that rule for comments
and docstrings generally; this one applies it to names.

### 2. The rename

~30 classes, mechanically: `TestP2AmendmentBScopeReduction` →
`TestADeclaredReductionNeedsItsAllowance`, and so on. **Bodies untouched, no
test logic changed**, with the class docstring stating *why the obligation
exists* where it does not already.

**Sequenced after the owning plan archives.** Most affected classes belong to
`review-efficient-lifecycle`, which is executing. Renaming another plan's tests
mid-flight is a collision hazard this repository has paid for twice in the last
two days, and the rename is worth nothing if it costs a merge conflict.

### Documentation / doctrine surface

The governing layer only (`AGENTS.md` and its shipped twin), per
`docs/DOCUMENTATION_PLAN.md`: this is cross-cutting prescription an agent must
follow, not deliberation and not description. No `doctrine/` file currently
mentions test naming and none needs to — the rule is operational, and a doctrine
page would be a second home for a one-paragraph convention.

### Doctrine-change rate-limit

**Not a doctrine change.** `AGENTS.md`'s `**Naming.**` paragraph is operational
convention, not the invariant kernel, so the rate-limit gate does not apply.
Flagged explicitly because the adjacent triage trigger — "anything under
`doctrine/`" — does not fire here and a reviewer should not have to work that
out.

## Rationale

The cost of this convention is one sentence. The cost of not having it grows
with the corpus: every plan adds tests, and coordinate names decay at exactly
the rate the deliberation record archives. Fixing it at 217 names is cheap;
fixing it at 2000 is a project.

There is also a self-consistency argument. Cairn's whole premise is that the
deliberation record is a **by-product** of a good process rather than the point
of it. A test named after a chunk inverts that: it makes the executable artifact
depend on the record for its meaning.

## Alternatives considered

* **Do nothing.** Defensible: the leaf names already carry the behaviour, so a
  failure is legible even now. Rejected because the container is what groups a
  suite for a reader browsing it cold, and because the cost of the rule is one
  sentence.
* **Rename everything now.** Rejected on collision risk, not on merit. The
  affected classes are in an executing plan's files.
* **Keep the coordinate in the docstring.** This was the earlier draft.
  Rejected on the Maintainer's correction (2026-08-13): a finding id identifies
  nothing to a reader without the plan open, and `git blame` is the maintained
  path to it. The docstring carries the *reason*, not the label. See the sibling
  proposal for the general rule.
* **Add a naming lint.** Rejected *for now*, and the reasoning is worth
  recording because the criterion in `doctrine/dual-review.md` does not cleanly
  decide it. That criterion says mechanize when the failure is silent, the check
  is substantive rather than formal, and the consequence is expensive. Naming is
  the unusual case where the check *is* formal and that is fine — a pattern
  match fully decides the property, with no gap between what the tool sees and
  what we care about. So the criterion does not forbid a lint; it simply does
  not argue for one. The deciding factor is volume: one paragraph plus a rename
  is cheaper than a gate every contributor meets forever. **Revival condition:**
  if coordinate names reappear after the rename, the lint becomes warranted —
  recurrence is what a formal check is for.

## Evidence / verification plan

* **The count is measured**, not estimated: 217 of 3546 (`as_of 2026-08-13`),
  by matching coordinate patterns against collected test and class names.
* **The leaf/container split is measured** — the sample above is drawn from
  classes matching the coordinate pattern, and their methods do not.
* **The collision claim is explicitly *not* made** — see Context.

**Tests required**: none new. The rename must leave the suite's node count and
pass/fail set **unchanged** — that is the acceptance criterion, and it is
checkable by diffing `--collect-only` output across the rename commit.

**Docs**: `AGENTS.md` ×2. No `CHANGELOG.md` entry — this changes no adopter-
facing behaviour; the shipped `AGENTS.md` paragraph is the delivery.

## Signals the change is wrong

* Renamed classes drift back toward coordinates because authors find behaviour
  names hard to invent under time pressure. That would mean the convention needs
  examples, or a lint after all.
* A reader reports that provenance became *harder* to find once it moved to
  docstrings — which would mean the docstrings are not being written, and the
  convention has traded a bad pointer for no pointer.
* The rename produces a merge conflict with an executing plan despite the
  sequencing, which would mean the sequencing rule was too weak and the whole
  thing should wait longer.

## Review -- Antigravity (External) -- 2026-08-13

**Model**: Antigravity (Gemini 3.1 Pro)
**Tier**: External, different agent type from the author (Claude Opus 5)
**Reviewed commit**: `42322f3a653ac359f378bce36f586d7a73ac0993`
**Reviewed proposal blob**: `035053183fd1290340adc2c1e2f164f4cc7d3860`
**Assurance path**: high-assurance
**Findings**: 3 raised (1 header contradiction, 1 execution tracking gap, 1 docstring formatting gap)
**Verdict: REVISE.** The core problem and proposed convention are sound, but the proposal carries a direct contradiction in its header justification regarding sequencing, lacks an explicit tracking mechanism for the post-archive rename task, and should provide a standardized docstring example in `AGENTS.md`.

### Findings

1. **[E1 -- Header Justification Contradiction]**:
   - Line 12 asserts: `**Plan review**: not required(no plan — one convention paragraph plus a mechanical rename, no sequencing, no deferred follow-ups)`.
   - However, lines 9 and 99–102 explicitly state that the rename is **`sequenced after their owning plan archives`** (specifically `review-efficient-lifecycle`).
   - *Required satisfier*: Correct the header justification to `not required(no plan — single concept, operational convention change, mechanical rename)` rather than claiming "no sequencing".

2. **[E2 -- Execution Handoff & Tracking for Deferred Rename]**:
   - Because `review-efficient-lifecycle` is currently executing, renaming its test classes now would cause merge conflicts. However, once `review-efficient-lifecycle` eventually archives in a future session, a future agent will have no automated way of knowing this mechanical rename is pending.
   - *Required satisfier*: Specify that upon acceptance, the mechanical rename is recorded as a queued item in `dev/PLANNING.md` under an explicit revival condition: *"When `review-efficient-lifecycle` archives, execute the test container rename from `2026-08-13-claude-test-names-outlive-their-plans`."*

3. **[E3 -- Standardized Docstring Provenance Example]**:
   - The proposed `AGENTS.md` text states: `Provenance belongs in the docstring — the finding id, the date, and why the obligation exists`. Without a concrete example, future test authors will format provenance docstrings inconsistently.
   - *Required satisfier*: Include a concise 1–2 line docstring template example directly inside the proposed `AGENTS.md` text (e.g. `"""Pinned behavior for finding CF1 (2026-08-11). Asserts that..."""`).

### Summary Verdict
**Verdict**: **REVISE** (3 minor/substantive findings). Address E1–E3 in a short Response and Revised proposal.


