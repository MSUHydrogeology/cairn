<!-- Author tip: a strategy doc is INLINE-REVISED, not append-only (the
     opposite of a proposal). Fold reviews in and remove them; keep the doc a
     clean artifact. The deliberation lives in git log + transient review
     sections, never as blow-by-blow residue in the body. See README.md. -->

# Strategy-note template

> **This is the `dev/strategy/` template.** To open a strategy note, copy
> the section template below the rule into
> `dev/strategy/<YYYY-MM-DD>-<author>-<short-slug>.md`, fill it, and commit.
> The doctrine above the rule is reference — read it once, then work from the
> sections below. The single source of truth for the folder's *kinds*,
> *lifecycle*, and *status × type validity* is [`README.md`](README.md); this
> template only carries the shape.

## What a strategy note is (and the one rule that defines it)

`dev/strategy/` is the project's **Stage-0 "explore before you commit"**
space: comparative research, tool analysis, product strategy, and long-horizon
design context that is *not yet a commitment*. A proposal is the **Stage-1
registered report** (the commitment); a strategy note is what you write
*before* you are ready to propose.

**The defining discipline — inline-revised, not append-only.** This is the
load-bearing contrast with proposals, and the easy mistake to avoid:

* A **proposal** is *append-only*: reviews and responses are appended and
  **retained**; reading top-to-bottom replays the deliberation.
* A **strategy note** is *inline-revised*: a review is folded **in and
  removed**, leaving a clean artifact. No blow-by-blow, no finding-tags, no
  "the earlier draft said…" residue. The deliberation lives in `git log` and
  in the transient review section while it is open — not in the doc body.

> **Cross-lifecycle word note (the same words, the opposite handling).** A
> strategy note's `reviewed` / `revised` statuses mean *a review was folded in
> and removed* (inline-revise). A **proposal's** identical `reviewed` /
> `revised` mean *reviews appended and retained* (append-only). Same word,
> opposite record discipline — don't carry append-only habits onto a strategy
> note.

### The review mechanic (the three steps)

A review on a strategy note is **transient by design** — the principle above
("fold in and remove") works only if the steps are explicit:

1. **Reviewer appends** a `## Review` section and flags it as temporary.
2. **Author revises the doc inline**, folding in what they accept — no
   finding-tags, no "the draft said…" residue.
3. **Author deletes the review section.** The arc survives in `git log`, not
   the doc.

The reviewer does not retain or re-append; the **author owns the delete**. (A
proposal is the mirror image — append and keep.)

## Status vocabulary

One vocabulary, replacing the ad-hoc forms the folder accreted:

```
draft → reviewed → revised → settled → promoted (→ <proposal/plan>) / archived
```

plus **`living`** for durable references that never promote or archive (kept
current as the project evolves).

Three definitions worth pinning (the rest are self-evident):

* **`settled`** — exploration complete / conclusions stable, *whether or not a
  review happened*. Review is **optional** for a strategy note; an unreviewed
  but stable note is `settled`, not `draft`.
* **`living`** — kept current / a durable companion. Assigned by **role**, not
  by the literal last-edit word (a note "revised twice" that is now a durable
  companion is `living`, not `revised`).
* **`promoted (→ <proposal/plan>)`** — its direction was carried into a
  proposal **or** fed a plan. "Fed a plan" counts as promotion, not only
  "became a proposal".

## `Type:` tag

A light tag naming the kind, so the multi-kind folder stays legible:

| `Type:` | What it is | Promotes? |
|---|---|---|
| `design-exploration` | explores a design before it is a commitment | → a proposal |
| `comparative-research` | weighs options / surveys the field | → a proposal/plan, or informs |
| `tool-analysis` | external-tool / dependency evaluation | informs, or → a proposal |
| `product-strategy` | direction / scope / roadmap thinking | informs, or → a proposal |
| `living-reference` | a durable companion kept current | **never** — stays `living` |

**Status × Type validity** (see README for the full rule): a `living-reference`
is always `Status: living` (never `promoted`); a `design-exploration` may reach
`promoted`. The two fields must not contradict.

---

# {{strategy note title}}

**Author**: {{name / role}}
**Model**: {{your actual running model — query and state it}}
**Date**: {{YYYY-MM-DD}}
**Status**: draft
**Type**: {{design-exploration | comparative-research | tool-analysis | product-strategy | living-reference}}
**Surfaces this would feed**: {{the proposal(s) / plan(s) / docs / roadmap items this could promote to or inform — or "TBD"}}

## The question / felt gap

What are we exploring, and what triggered it? The honest open question, not a
foregone conclusion.

## Method *(grounded, falsifiable — verify-before-asserting)*

How the findings were established: the files read, the commands run, the
sources surveyed, the things tried-to-break. A strategy note's authority comes
from grounding, not assertion — name what would falsify the conclusion.

## Findings

What the exploration actually turned up.

## Options

The paths on the table (include "do nothing"). Naming them matters more than
picking — it forces the reader to push back at the right level.

## Recommendation

The direction, with its rationale and the residual risk.

## Open questions

What is unresolved and would need settling before (or at) promotion.

## Fold-up note *(when methodology-bound)*

If the convention/finding is methodology-general rather than project-specific,
name it here as a fold-back candidate for the project's upstream methodology
record (if using Cairn: `dev/.cairn/cairn_foldback.md`).

---

*The header (through **Surfaces this would feed**) is required; the sections
below it are the **suggested** shape — the looser kinds
(`comparative-research`, `tool-analysis`) may drop or merge sections that don't
fit, as the proposal/plan templates allow. Keep the doc clean and
inline-revised either way.*
