# Test names outlive the plans that produced them

**Author**: Claude (Strategy)
**Model**: Claude Opus 5 (`claude-opus-5`)
**Date opened**: 2026-08-13
**Status**: proposed
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
> lifecycle tells them not to re-read. **Provenance belongs in the docstring** —
> the finding id, the date, and *why the obligation exists* — where it is read
> when deciding whether a test still earns its place, rather than every time it
> fails.

The second sentence is the load-bearing one. This is not "delete the
provenance"; it is "put it where it is useful and out of where it is not."

### 2. The rename

~30 classes, mechanically: `TestP2AmendmentBScopeReduction` →
`TestADeclaredReductionNeedsItsAllowance`, and so on. **Bodies untouched, no
test logic changed**, with the coordinate moved into the class docstring if it
is not already there.

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
* **Ban coordinates from docstrings too.** Rejected — that is where provenance
  belongs. This proposal moves the coordinate, it does not delete it.
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
