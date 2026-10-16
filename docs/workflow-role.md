# Cairn's role in the software-development workflow

Cairn is **methodology, not software**. The single most common
misread — "is this another CI tool / test framework / prompt
library?" — is worth answering head-on, because what Cairn *is* is
defined as much by what it deliberately leaves to other tools as by
what it owns.

## What Cairn owns

Cairn governs the **deliberation** around a change — the recorded,
reviewed decision-making *upstream* of the code:

* **The lifecycle.** Substantive changes move through
  propose → review → decide → implement → record, as append-only,
  git-committed artifacts (see [`../doctrine/lifecycle.md`](../doctrine/lifecycle.md)).
  Cairn decides *what gets proposed, reviewed, and shipped* — and
  keeps the trail.
* **Dual-Review.** Two-tier review across structural independence
  (see [`../doctrine/dual-review.md`](../doctrine/dual-review.md)):
  who must look at a change before it lands, and how independent
  they must be.
* **Coordination.** How a human maintainer and one or more AI agents
  share the tree without colliding (see
  [`../doctrine/coordination.md`](../doctrine/coordination.md)),
  the role roster ([`../doctrine/roles.md`](../doctrine/roles.md)),
  and the session routines
  ([`../doctrine/session-routines.md`](../doctrine/session-routines.md)).
* **Adaptation.** Which of the above scales up or down with the
  project's dimensions (see [`../dimensions/README.md`](../dimensions/README.md)).

## What Cairn deliberately does *not* do

Cairn sits **upstream** of the build/test/doc machinery and does not
replace it:

* **It does not run your tests.** Cairn's doctrine says a change
  *absorbs* tests; your test framework (pytest, JUnit, ...) runs
  them. Cairn decides that a test is required and reviewed; it does
  not execute it.
* **It is not CI/CD.** Cairn produces the reviewed decision and the
  recorded rationale; your CI system builds, gates, and deploys.
  Cairn is what tells CI *what* should be built and *why* it was
  agreed.
* **It is not a prompt library.** Cairn governs which work is worth
  prompting an agent for, and how the result is reviewed — not the
  wording of prompts. Bring your own.
* **It does not teach the craft.** Where an adopter needs to *learn*
  testing, reproducibility, or collaborative practice, Cairn points
  outward (see [`further-reading.md`](further-reading.md)); it does
  not re-teach what better resources already own.

## Where the seams meet

```
        Cairn (this repo)                     Your existing tooling
  ┌─────────────────────────────┐
  │ propose → review → decide    │
  │   (recorded deliberation)    │
  │            │                 │
  │            ▼                 │
  │ implement: change absorbs ───┼──▶  test framework runs the tests
  │   tests + docs + examples ───┼──▶  doc builder builds the docs
  │            │                 │
  │            ▼                 │
  │ record (CHANGELOG, archive) ─┼──▶  CI/CD builds, gates, deploys
  └─────────────────────────────┘
```

The boundary is a feature: Cairn stays small and durable because it
does not duplicate the tools that already run tests and ship code.
It is the layer that decides *what gets prompted, reviewed, and
shipped* — and leaves the running of tests and the shipping of code
to the tools built for those jobs.

## See also

* [`getting-started.md`](getting-started.md) — a worked trace of one
  change moving through the lifecycle.
* [`further-reading.md`](further-reading.md) — the craft resources
  Cairn relies on but does not re-teach.
* [`../on-ramp/README.md`](../on-ramp/README.md) — how to adopt:
  read the doctrine, or install it with a profile.
