# Getting started — a change moving through Cairn

The [on-ramp](../on-ramp/README.md) describes the adoption *levels*
(read the doctrine / hand-copy the kernel / run the bootstrap). This
page is the complement: a narrated trace of **one change moving
through the lifecycle**, so you see the apparatus *in motion* rather
than only described.

If you want to read the artifacts of a real (tiny) instance alongside
this narrative, open [`../examples/minimal/`](../examples/minimal/) —
it carries the actual proposal, code, and test for the change traced
below.

> **Honest framing.** The five steps below add friction *before*
> code: you write the decision down first, review it, accept it,
> *then* implement. That is the design. The payback is fewer
> forgotten assumptions, fewer collisions, less rework — but only
> on changes substantive enough to warrant a proposal. The
> [quickstart](quickstart.md)'s "trivial accept" path collapses
> three of these steps into a single implement-and-archive commit
> for the smallest end of that scale.

## The five steps

A substantive change moves through
[propose → review → decide → implement → record](../doctrine/lifecycle.md).
Walk a concrete one: *add an optional name argument to a `greet` CLI.*

### 1. Propose

You write a proposal as a committed Markdown file under
`dev/proposals/` — context, the change, and the alternatives you
considered. The act of writing it is the point: it forces the
reasoning into the open *before* code is written, where it can be
reviewed cheaply.

A proposal is **append-only**: reviews and the decision are *added*
to it, never edited over. The file is the audit trail.

### 2. Review

A reviewer — **structurally independent** of the author (a different
person, or a different agent type; see
[Dual-Review](../doctrine/dual-review.md)) — appends a `## Review`
section. They check the reasoning, not just the code-to-be: is the
change backward-compatible, is a test absorbed, is anything
under-specified? On a small change one review suffices; higher-stakes
changes get the second tier.

### 3. Decide

The **Maintainer** appends the `## Decision` section: accept, reject,
or supersede. This is the human authority gate — agents propose and
review, but the Maintainer (or their explicit instruction) records the
decision. An accepted proposal then moves to `dev/proposals/archive/`.

A small change is a **trivial accept** (implement-and-archive in one
step). A larger one opens a **plan** under `dev/plans/` first, which
sequences the implementation and gets its own review before the work
archives.

### 4. Implement — absorbing tests, docs, examples

The change lands *with* its test and any doc/example update in the same
movement — "a change absorbs its tests" is core doctrine, not an
afterthought. Cairn does not run those tests; your test framework does,
and your CI gates them (see [`workflow-role.md`](workflow-role.md) for
the boundary). Cairn's job was to decide the test is required and to
have it reviewed.

### 5. Record

The decision and its rationale already live in the archived proposal
(and plan, if any). A one-line `CHANGELOG` entry records the
user-visible change. Together the git history + the archived
deliberation are the durable record: a future reader can reconstruct
*what* changed and *why* it was agreed.

## What to do next

* **Just exploring?** Read [`../doctrine/`](../doctrine/) as a handbook
  (on-ramp Level 0) and let it inform how your team already works.
* **Ready to adopt?** Hand-copy [`../templates/core/`](../templates/core/)
  (Level 1) or run the bootstrap (Level 2) — see the
  [on-ramp](../on-ramp/README.md).
* **Need to learn the craft Cairn assumes** (testing, reproducibility,
  working with AI agents)? See [`further-reading.md`](further-reading.md);
  Cairn points you to those resources rather than re-teaching them.
