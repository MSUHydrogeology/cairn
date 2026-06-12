# `dev/strategy/` — the Stage-0 "explore before you commit" space

This directory holds **strategy notes**: comparative research, tool analysis,
product strategy, and long-horizon design context that is **not yet a
commitment**. It is the project's *think-before-you-propose* space.

This `README.md` is the **single source of truth** for the folder's kinds,
lifecycle, and status vocabulary. The [`_template.md`](_template.md) carries
the shape. New notes start from the template.

## Stage-0 vs Stage-1: the relationship to proposals

A **strategy note is Stage-0 exploration** — no commitment, written before you
are ready to propose. A **proposal is the Stage-1 registered report** — the
commitment, design-and-evidence locked for review (see
[`../proposals/_template.md`](../proposals/_template.md)). The exit from a
strategy note is **promotion** (it becomes / feeds a proposal or plan); the
closed end is [`archive/`](archive/).

## The defining discipline — inline-revised, not append-only

The load-bearing distinction, and the easy mistake:

* A **strategy note is inline-revised**: a review is folded **in and removed**,
  leaving a clean artifact. No blow-by-blow, no finding-tags, no
  "earlier-draft-said" residue. The deliberation lives in `git log` and in the
  transient review section while open — not in the body.
* A **proposal is append-only**: reviews/responses are appended and retained.

**Cross-lifecycle word note:** a strategy note's `reviewed` / `revised` mean
*folded-and-removed* reviews; a proposal's identical words mean
*appended-and-retained*. Same word, opposite handling.

## Kinds (`Type:`)

| `Type:` | What it is |
|---|---|
| `design-exploration` | explores a design before it is a commitment (promotes to a proposal) |
| `comparative-research` | weighs options / surveys the field |
| `tool-analysis` | external-tool / dependency evaluation |
| `product-strategy` | direction / scope / roadmap thinking |
| `living-reference` | a durable companion kept current (never promotes) |

## Status vocabulary + lifecycle

```
draft → reviewed → revised → settled → promoted (→ <proposal/plan>) / archived
                                                          living
```

* **`draft`** — in progress.
* **`reviewed` / `revised`** — a review happened and was folded in (optional;
  see the inline-revise rule). Review is *not required* for a strategy note.
* **`settled`** — exploration complete / conclusions stable, **whether or not a
  review happened**. An unreviewed-but-stable note is `settled`, not `draft`.
* **`promoted (→ <proposal/plan>)`** — its direction was carried into a
  proposal **or fed a plan** ("fed a plan" counts as promotion).
* **`living`** — kept current / a durable companion; assigned by **role**, not
  by the literal last-edit word. Never promotes or archives.
* **`archived`** — moved to [`archive/`](archive/) (adopted / superseded /
  retired). A note in `archive/` is `archived` by its location.

### Status × Type validity

The two fields must not contradict:

* `living-reference` ⟺ `Status: living` — never `promoted` / `settled` /
  `archived` (a living reference is, by definition, kept current).
* `design-exploration` may reach `promoted`; it does not end `living`.
* `comparative-research` / `tool-analysis` / `product-strategy` typically end
  `settled` (point-in-time) or `promoted` (fed a proposal/plan); they become
  `living` only by an explicit role change to `living-reference`.

## Archive trigger

A note moves to [`archive/`](archive/) when its direction has been **adopted**
into a proposal/plan, **superseded** by a later note, or **retired**. Read an
archived note for historical context; do **not** treat it as current direction
unless a live proposal, plan, `dev/PLANNING.md` item, or doc cites it.

See [`../README.md`](../README.md) for the full `dev/` subdirectory map.
