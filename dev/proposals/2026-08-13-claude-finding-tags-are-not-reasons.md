# A finding tag is not a reason

**Author**: Claude (Strategy)
**Model**: Claude Opus 5 (`claude-opus-5`)
**Date opened**: 2026-08-13
**Status**: proposed
**Touches**: `AGENTS.md` and `templates/core/AGENTS.md` (the comprehension-floor
paragraph in `## Review`); a read-and-revise pass over the ~40 comments and
docstrings where a tag is load-bearing, sequenced per file owner
**Related**: `2026-08-13-claude-test-names-outlive-their-plans` (the same
failure in test names); `dev/PLANNING.md` > "Opaque finding-IDs in code comments
and docstrings", which this proposal drains
**Plan review**: not required(no plan — one paragraph plus a bounded,
judgement-led revision pass; no sequencing beyond file ownership)

## Context

`dev/PLANNING.md` carries this item, raised by the Maintainer on 2026-08-13:

> *"They don't inform anyone anything. I don't know what FUR5 is."*

Comments and docstrings across the codebase carry bare review-finding tags —
`[FUR5]`, `[M2-1]`, `[S1]`, `[C1]`, `[E1]`, `[D2]`. The board already classifies
this as a **comprehension-floor** failure (`AGENTS.md` > Review): the tag was
written for the reviewer who had just read the finding, and is inert for
everyone after.

**Measured, `as_of 2026-08-13`:** 262 occurrences of 37 distinct tags in `.py`
files. (The thousands more in `.md` are deliberation artifacts, where a review
section citing its own findings is correct and out of scope here.) They
concentrate in `bootstrap/tests/test_gate_preflight.py` (54),
`bootstrap/tests/_gate_preflight.py` (40), and the `lifecycle_planner` twins
(21 each).

### Not all tags are the same, and that is the whole proposal

The board's note says *"the rationale is usually present and worth keeping —
what fails is the bare identifier standing in for it."* Reading the corpus bears
that out, and sharpens it into three distinguishable cases.

**1. Annotation — the tag sits beside stated reasoning. Fine.**

```python
# Security review [S1]. `gpg.ssh.defaultKeyCommand` names a program Git runs
```

Strip the tag and the comment still teaches. The tag is a footnote.

**2. Gloss — the tag is immediately defined. Fine, and arguably the target
form.**

```python
# FUR5 -- the recorded anchored invocation, actually executed
```

The reader learns what `FUR5` means from the line itself.

**3. Referent — the sentence's meaning depends on knowing the tag. Broken.**

```python
recorded one stayed broken, which is FUR5 exactly
It is the [M2-1] shape once more: built, unit-tested, and dead to
`[E3]`'s property survives, because it was about a *neighbouring round's*
Since FUR5 the executed bytes come from **the anchor**
"""The premise the FUR5 shape
```

Here the tag is the **subject**, not a footnote. There is no reading of these
that recovers the meaning without the originating plan open. `Since FUR5` is a
date the reader cannot date; `the [M2-1] shape` is a shape only the plan
describes.

**Only case 3 is a defect.** A sweep that strips tags indiscriminately would
delete the footnotes in cases 1 and 2 while leaving case 3 exactly as unreadable
— strictly worse than doing nothing.

## Proposed paths

* `AGENTS.md` and `templates/core/AGENTS.md` — the comprehension-floor paragraph
* the ~40 case-3 sites, revised in place

## Proposal

### 1. The rule

Add to the comprehension-floor paragraph in both `AGENTS.md` copies:

> **A finding tag is a footnote, never a referent.** `[S1]`, `[M2-1]`, `FUR5`
> and their kin identify nothing to a reader without the originating plan open,
> and that plan archives. Cite one *beside* a reason — never *as* one. If a
> sentence stops making sense when the tag is deleted, the sentence is missing
> its reason: state the thing the tag stands for. This is the comprehension
> floor applied to code, and it binds the author, who had the finding in front
> of them, not the reader who never will.

### 2. The revision pass

Roughly 40 case-3 sites, revised **by reading, one at a time**. `[M2-1]` becomes
what `[M2-1]` *was*:

```python
# It is the [M2-1] shape once more: built, unit-tested, and dead to
+ # Built, unit-tested, and never reached in production -- the same shape as
+ # the earlier attestation bug ([M2-1]).
```

The tag survives in parentheses; the sentence no longer leans on it.

**Explicitly not a mechanical find-and-replace.** The board's note warns of this
and it is right: some tags sit next to genuinely load-bearing history, and a
regex sweep loses the reason along with the label.

**Sequenced by file owner, not in one commit.** The two `_gate_preflight` files
hold 94 of the 262 and belong to a security plan closing now — the board routes
those as a *closure change* and this proposal does not pre-empt that. Everything
else is an ordinary change against whichever plan next touches the file.

### Documentation / doctrine surface

Governing layer only, per `docs/DOCUMENTATION_PLAN.md`. It extends the existing
comprehension-floor rule rather than adding a home: that paragraph already says
*"define a specialist term the first time it carries weight"* — a finding tag is
a specialist term that never gets defined, so this is the same rule reaching a
surface it did not name.

### Doctrine-change rate-limit

**Not a doctrine change.** The rule lands in `AGENTS.md`, and
`doctrine/rationale.md`'s comprehension floor is unchanged — this is its
operational reach, not a new principle. Flagged because the adjacent trigger
("anything under `doctrine/`") does not fire.

## Rationale

The comprehension floor already says a decision surface the reader cannot follow
is not decidable. A comment is a decision surface for the next person changing
that code, and 262 tags is 262 places where the author's context was assumed
rather than supplied.

The economics also favour acting now. Tags accrue per review round, and this
repository ran nine review rounds on one plan this week. The cost of the rule is
a paragraph; the cost of the backlog grows monotonically and its readability
decays as plans archive.

## Alternatives considered

* **Do nothing.** The strongest version: most tags are case 1, the reasoning is
  usually there, and a reader who hits one can survive not knowing. Rejected
  because case 3 is not survivable — the sentence is simply unreadable — and
  because the Maintainer reports hitting exactly that.
* **Strip every tag mechanically.** Rejected, per the board's own warning and
  the three-case split: it would destroy the footnotes and leave the defects.
* **Ban tags from code entirely.** Rejected. In case 2 the tag plus its gloss is
  genuinely useful — it lets a reader who *does* want the history find it.
* **Add a lint for bracketed tags.** Rejected. A regex cannot tell case 1 from
  case 3; that distinction is exactly the judgement the note says a sweep must
  not skip. A lint here would flag 262 sites of which ~85% are fine — noise that
  trains people to ignore it.
* **Fold this into the test-naming proposal.** Tempting, since both are "an
  identifier that pointed into a plan." Rejected: that one is a mechanical
  rename with a checkable acceptance criterion, this one is a read-and-judge
  pass with no mechanical check. Bundling would put a judgement pass behind a
  rename's verification story.

## Evidence / verification plan

* **Counts are measured**: 262 occurrences, 37 distinct tags in `.py`,
  `as_of 2026-08-13`; concentrations by file as listed.
* **The three cases are drawn from the corpus**, quoted verbatim above, not
  constructed.
* **The ~40 figure for case 3 is approximate and stated as such.** A pattern
  matching tags used as grammatical subjects returns 248 candidate lines, but
  that over-counts heavily — it catches every `the [C2]` that is really an
  annotation. The real number needs reading, which is the point of the pass. **A
  reviewer should not treat 40 as measured.**

**Tests required**: **none, and that is a deliberate limit.** No test can
distinguish a tag that carries its reason from one that does not; the property
is semantic. The verification is that a reader who has never opened the source
plan can follow each revised comment — which is review, not a gate. Stating this
rather than inventing a proxy check, per `doctrine/dual-review.md`'s
mechanize-criterion.

**Docs**: `AGENTS.md` ×2. No `CHANGELOG.md` entry — no adopter-facing behaviour
changes; the shipped `AGENTS.md` paragraph is the delivery.

## Signals the change is wrong

* Authors stop citing findings in code at all, losing the traceability cases 1
  and 2 provide. That would mean the rule read as "tags are bad" rather than
  "tags are footnotes", and needs the case-2 example promoted into the rule
  itself.
* The revision pass produces comments that are longer but no clearer — reasons
  restated at length because the author could not recall what the finding
  actually established. That would suggest the affected sites should carry a
  short gloss and a plan citation instead of a reconstructed rationale.
* A reviewer finds the three-case split does not hold on a sample I did not
  read — in which case the taxonomy, not just the sites, needs revising.
