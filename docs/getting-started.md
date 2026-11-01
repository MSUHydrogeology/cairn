# Getting started — a change moving through Cairn

The [on-ramp](../on-ramp/README.md) helps you choose how much of Cairn to
adopt: read the guidance, or install it with a profile. This page follows
**one change through the lifecycle** so you can see what each step produces.

If you want to read the artifacts of a real (tiny) instance alongside
this narrative, open [`examples/minimal/`](../examples/minimal/) —
it carries the actual proposal, code, and test for the change traced
below. ([`examples/scientific-minimal/`](../examples/scientific-minimal/)
shows the same shape on a tiny science workflow — a mass-balance
invariant — if you want a domain-flavored example.)

Cairn supports Windows natively; the [quickstart](quickstart.md) includes
PowerShell steps.

> **What to expect.** The five steps below add work *before*
> code: you write the decision down first, review it, accept it,
> *then* implement. That is intentional. On changes large enough to
> warrant a proposal, this sequence can keep assumptions visible and
> reduce collisions and rework. Smaller changes take a lighter lane
> (see the figure below).

## The five steps

Not every change needs all five. A change is sorted into one of three lanes
first, and the steps below are the deliberate lane, the heaviest one:

![Three lanes: most changes take a light path. A typo or one-line fix is the change with its test and needs no review. A change whose shape is settled gets a short change note and a review first. Only a new feature, a contract change or a high-risk surface gets a proposal, a review, the Maintainer's decision and a plan. Ordinary ceremony uncertainty takes the lighter lane with a reason; stop on a newly discovered trust boundary. Every lifecycle step is a commit.](assets/three-lanes-of-change.svg)

A substantive change moves through
[propose → review → decide → implement → record](../doctrine/lifecycle.md).
Here is one example: add an optional name argument to a `greet` command-line
program. Because this adds a capability, it belongs in the deliberate lane.

### 1. Propose

You write a proposal as a committed Markdown file under
`dev/proposals/` — context, the change, and the alternatives you
considered. The act of writing it is the point: it forces the
reasoning into the open *before* code is written, where it can be
reviewed cheaply.

A proposal's operative text is revised in place while active; git preserves
earlier versions. Reviews, responses and decisions are appended and never
edited. The file and its history are the audit trail.

### 2. Review

A reviewer who did not write it — a fresh session of an agent counts, and the
file names who they were (see [Dual-Review](../doctrine/dual-review.md)) —
appends a `## Review` section. They check the reasoning, not just the proposed
code: should this happen as framed, what is the best alternative, and what
evidence would show the idea is wrong? One fresh reviewer is enough. If the
Maintainer wants more distance on a particular change, they can ask for
another model or a person.

### 3. Decide

The **Maintainer** appends the `## Decision` section: accept, reject,
or supersede. Agents can propose and review, but only the Maintainer decides
whether the change goes ahead. An accepted proposal stays in `dev/proposals/` until the work
starts: it moves to `dev/proposals/archive/` in the commit that opens its plan,
or, for a small change, in the commit that implements it.

So far, Cairn's own archive has no proposals with `rejected` status. That
describes this project's record, not a target for yours: many ideas end in
conversation before anyone opens a proposal, and a proposal can be rejected.

A small accepted proposal can be implemented and archived in one commit.
A larger one opens a **plan** under `dev/plans/` first, which sequences
the implementation and gets its own review before the work archives.
The `greet` change is small enough for the one-commit path.

### 4. Implement — include tests, docs and examples

Commit the change with its test and any needed doc or example update.
The test is part of the change, not an afterthought.
Cairn does not run those tests. Your test runner does (see
[`workflow-role.md`](workflow-role.md) for the boundary). Cairn's job
is to make sure the test is required and that it gets reviewed.

### 5. Record

The archived proposal (and plan, if there is one) records the decision and
its reason. A one-line `CHANGELOG` entry records what users will notice.
Together, these files and the commit history show what changed and why.

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
