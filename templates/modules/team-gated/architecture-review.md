<!-- ^ Illustrative adopter-tree path: this module's output surface, created on first use; the cite travels with the template to adopters. -->

# Module: architecture-review

**Selected when:** a project needs to examine how its code fits together or
how that structure is changing. This can be inherited code, a new design or
a mixture of old and new components. A small, coherent project may need no
architecture change; the rubric must allow that result. Selection is not
determined by team size.
**Adds to:** a new `dev/architecture_review.md` (a forkable rubric
frame, installed alongside this doctrine).

This module provides a review when an adopter needs one; it does not add a
standing routine. Cairn's core process reviews individual changes. When the
`security-review` module is installed, it also reviews trust boundaries. The
project vision sets the long-term direction. Those parts do not examine how
well the whole system's architecture fits together or can grow. This module
provides that system-wide review when an adopter needs it.

## What it ships

* **`dev/architecture_review.md`** — a forkable rubric frame carrying
  five review lenses (Workflow Coherence, Data Contracts, Correctness /
  Provenance Trust, Extensibility, Operational Maturity), a "Biases to
  Challenge" meta-section, and program governance. The adopter fills the
  lenses with their own system's seams and failure signals; the frame
  ships the *questions*, not the answers.
* **`tools/code_map.py`** -- a bounded, read-only filesystem map and advisory
  function neighbors. With a trusted Python runtime and installed copy, run
  `python -I tools/code_map.py --root PATH`; add `--changed src/file.py` for
  changed-function neighbors or `--release` for whole-scope comparisons.
  JSON output names omissions and incomplete analysis. Similarity is a lead,
  not evidence of equivalent behavior or permission to delete. Unsupported
  operating-system traversal remains incomplete, never a clean scan.

## Applying the frame

Record the current homes of safety-sensitive helpers in the existing rubric:
regular-file reading, write containment, terminal encoding and Git execution.
Look there before adding another implementation. Keep justified standalone
scripts, stronger specialized readers and wrappers; compare their actual
contracts rather than matching names alone. For a demonstrated dangerous
fork, add a narrow check in its existing test home with a failing example and
an allowed-copy or wrapper control. This is not a universal duplicate-code ban.

At releases using this module, update the assessment in the same record with
the map and its omissions, neighbor dispositions, endpoint growth and ranked
consolidation candidates with preserving tests. Missing evidence stays unknown;
lines repeatedly edited are not net growth. This adds no approval stage or
deletion quota. Use the selected [testing-discipline module](testing-discipline.md)
for test selection and execution cost; do not duplicate its rules here.

## How it composes

* With **`codebase-readiness-report`** (the diagnostic companion): the
  readiness report helps identify architectural debt; this frame helps
  examine it. Fill out the report first to decide whether to use the frame.
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
