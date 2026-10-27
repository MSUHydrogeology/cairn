# Getting started — a change moving through Cairn

The [on-ramp](../on-ramp/README.md) describes *how much* of Cairn to
adopt (read the doctrine, or install it with a profile). This page is
the complement: a narrated trace of **one change moving
through the lifecycle**, so you see the apparatus *in motion* rather
than only described.

If you want to read the artifacts of a real (tiny) instance alongside
this narrative, open [`examples/minimal/`](../examples/minimal/) —
it carries the actual proposal, code, and test for the change traced
below. ([`examples/scientific-minimal/`](../examples/scientific-minimal/)
shows the same shape on a tiny science workflow — a mass-balance
invariant — if you want a domain-flavored example.)

> **Honest framing.** The five steps below add friction *before*
> code: you write the decision down first, review it, accept it,
> *then* implement. That is the design. The payback is fewer
> forgotten assumptions, fewer collisions, less rework — but only
> on changes big enough to warrant a proposal. Smaller changes take
> a lighter lane (see the figure below).

## The five steps

Not every change needs all five. A change is sorted into one of three lanes
first, and the steps below are the deliberate lane, the heaviest one:

![Three lanes: most changes take a light path. A typo or one-line fix is the change with its test and needs no review. A change whose shape is settled gets a short change note and a review first. Only a new feature, a contract change or a high-risk surface gets a proposal, a review, the Maintainer's decision and a plan. When unsure, take the heavier lane; every step is a commit.](assets/three-lanes-of-change.svg)

A substantive change moves through
[propose → review → decide → implement → record](../doctrine/lifecycle.md).
Walk a concrete one: *add an optional name argument to a `greet` CLI.*
That adds a capability, so it belongs in the deliberate lane.

### 1. Propose

You write a proposal as a committed Markdown file under
`dev/proposals/` — context, the change, and the alternatives you
considered. The act of writing it is the point: it forces the
reasoning into the open *before* code is written, where it can be
reviewed cheaply.

A proposal is **append-only**: reviews and the decision are *added*
to it, never edited over. The file is the audit trail.

### 2. Review

A reviewer who did not write it — a fresh session of an agent counts, and the
file names who they were (see [Dual-Review](../doctrine/dual-review.md)) —
appends a `## Review` section. They check the reasoning, not just the
code-to-be: should this exist as framed, is the change backward-compatible,
is anything under-specified? One fresh reviewer is enough. If the
Maintainer wants more distance on a particular change, they can ask for
another model or a person.

### 3. Decide

The **Maintainer** appends the `## Decision` section: accept, reject,
or supersede. This is the human authority gate — agents propose and
review, but the Maintainer (or their explicit instruction) records the
decision. An accepted proposal stays in `dev/proposals/` until the work
starts: it moves to `dev/proposals/archive/` in the commit that opens its plan,
or, for a small change, in the commit that implements it.

A small accepted proposal can be implemented and archived in one commit.
A larger one opens a **plan** under `dev/plans/` first, which sequences
the implementation and gets its own review before the work archives.
The `greet` change is small enough for the one-commit path.

### 4. Implement — absorbing tests, docs, examples

The change lands *with* its test and any doc or example update in the
same commit. A change absorbs its tests; they are not an afterthought.
Cairn does not run those tests. Your test runner does (see
[`workflow-role.md`](workflow-role.md) for the boundary). Cairn's job
is to make sure the test is required and that it gets reviewed.

### 5. Record

The decision and its rationale already live in the archived proposal
(and plan, if any). A one-line `CHANGELOG` entry records the
user-visible change. Together the git history + the archived
deliberation are the durable record: a future reader can reconstruct
*what* changed and *why* it was agreed.

## What to do next

* **Just exploring?** Read [`doctrine/`](../doctrine/) as a handbook
  and let it inform how your team already works.
* **Ready to adopt?** Install it with the scaffold and a profile — see the
  [on-ramp](../on-ramp/README.md) for how to choose one, and
  [`quickstart.md`](quickstart.md) to try the smallest install on a
  throwaway repository first.
* **Need to learn the craft Cairn assumes** (testing, reproducibility,
  working with AI agents)? See [`further-reading.md`](further-reading.md);
  Cairn points you to those resources rather than re-teaching them.
