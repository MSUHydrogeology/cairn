<!-- claim-check-allow: dev/architecture_review.md -->
<!-- ^ Illustrative adopter-tree path: this module's output surface, created on first use; the cite travels with the template to adopters. -->

# Module: architecture-review

**Selected when:** the codebase's architecture **accreted rather than
was deliberately designed** — inherited legacy, merged prototypes, or
vibe-coded growth where structure emerged from accumulation rather than
intent. This is widespread in the AI-assisted-coding era, where working
code routinely outruns deliberate design. The gate is **not** team
shape: a solo maintainer with an inherited legacy codebase is a valid
adopter. A deliberately-architected greenfield project may never need
it.
**Adds to:** a new `dev/architecture_review.md` (a forkable rubric
frame, installed alongside this doctrine).

This module is a **triggered remediation / on-ramp tool**, not a
standing routine. The invariant kernel reviews *changes* (code review)
and, where the `security-review` module is installed, *trust boundaries*;
the long-range north star is the vision. Nothing in the kernel examines
**whole-system architecture coherence and extensibility** — the altitude
*between* a per-change review and the vision. This module fills that gap
*when an adopter needs it*.

## What it ships

* **`dev/architecture_review.md`** — a forkable rubric frame carrying
  five review lenses (Workflow Coherence, Data Contracts, Correctness /
  Provenance Trust, Extensibility, Operational Maturity), a "Biases to
  Challenge" meta-section, and program governance. The adopter fills the
  lenses with their own system's seams and failure signals; the frame
  ships the *questions*, not the answers.

## How it composes

* With **`codebase-readiness-report`** (the diagnostic companion): the
  readiness report tells you *whether* you carry architectural debt;
  this frame is *how* you examine it. Fill the report first to decide
  whether you need the frame.
* The frame is a **rubric**, not a verdict. It is cited by proposals and
  plans; a *review program* (a proposal + an optional plan) applies the
  lenses to produce assessment artifacts carrying evidence markers
  (`[inference]` / `[hypothesis]` / `[unverified]`). Carrying the frame
  and running a program are separate steps — installing this module does
  the first, not the second.

## The deliberation rule

Updating the lenses or the biases is **itself a deliberation** worth a
proposal — don't drift the rubric quietly. The rubric stays stable
across successive review programs so their findings stay comparable; the
artifacts a program produces are not part of the rubric.

Without this module a project still has code review (and, when selected,
a security review and a vision); the module adds the
**architecture-coherence altitude** for an adopter whose structure
accreted rather than was designed.
