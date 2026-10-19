# Project Profile — legacy code-state assessment

> Fill this for a **legacy** codebase — one that predates the
> methodology. A bootstrapping agent completes it by inspecting
> the repository and interviewing the Maintainer; the result is
> presented for acceptance before Act II.
>
> **Fast path:** the `high-rigor-legacy` preset pre-fills the six-axis
> point for a large, complex legacy codebase — start there and adjust
> the axes below to the project's real scores. See
> `README.md > Governance presets`.

**Project:** {{project_name}}
**Assessed:** {{YYYY-MM-DD}} by {{assessor}}

## Architecture map

<!-- cairn:slot architecture-map -->
(The major modules / packages, what each does, and how they depend
on each other — the shape of the codebase as it is.)
<!-- cairn:end architecture-map -->

## Scientific-surface map

<!-- cairn:slot scientific-surface-map -->
(Where the code encodes domain / scientific assumptions — numerical
methods, units, models — the surfaces a reviewer must know the
science to check.)
<!-- cairn:end scientific-surface-map -->

## Test / readiness map

<!-- cairn:slot readiness-map -->
(Test coverage by surface, and each surface classified Ready /
Transitional / Frozen — see the legacy-agent module.)
<!-- cairn:end readiness-map -->

## Documentation-trust map

<!-- cairn:slot documentation-trust-map -->
(Which docs and docstrings are known accurate, and which have
drifted from the code and cannot be trusted.)
<!-- cairn:end documentation-trust-map -->

## Risk register

<!-- cairn:slot risk-register -->
(The surfaces where a change is most likely to break something
quietly — the highest-consequence, least-understood code.)
<!-- cairn:end risk-register -->

## Data / executable-dependency inventory

<!-- cairn:slot dependency-inventory -->
(External data, executables, and services the project depends on
to build, run, or test.)
<!-- cairn:end dependency-inventory -->

## Modernization-opportunity list

<!-- cairn:slot modernization-opportunities -->
(Where a retrofit would most repay the effort — and where it would
not.)
<!-- cairn:end modernization-opportunities -->

## Human-baseline practice — the Cognitive Adapter

In a retrofit, the **codebase** is not the only thing that has to
change. The contributors' development habits — built up over the
life of the project — are usually a stronger source of drift than
the code itself. Naming those habits explicitly here is a
*cognitive adapter*: it lets the team see the friction the new
discipline will create *before* it creates it, so the adoption
plans for it rather than discovers it.

<!-- cairn:slot human-baseline-practice -->
(Evaluate:
* How much of today's work is ad-hoc, un-staged, or untracked
  editing? Are commits regular and named, or rare and "wip"?
* What tracking surfaces does the team already use — issues,
  pull-request review, code review, none?
* How is design currently discussed — in chat, in a doc, in
  someone's head, in commit messages?
* How ready is the team to adopt **peer-review gates** — a fresh
  reviewer at every stage, the proposal-first lifecycle? What
  about that will feel slow, and what will feel like protection?
* Which surfaces sit closest to human muscle memory — the parts
  of the workflow contributors do automatically — and where will
  Cairn's discipline most disturb them?)
<!-- cairn:end human-baseline-practice -->

## Dimensional placement

The codebase axes, scored from the above (see `dimensions/` for the
rubrics):

* **Age:** legacy — {{age_note}}
* **Size:** {{size_position}} — {{size_reason}}
* **Complexity:** {{complexity_position}} — {{complexity_reason}}
* **Language:** {{language_position}} — {{language_reason}}

### Module-selection signals

Beyond the axes, two conditions select team-gated modules:

* **Trust boundary?** Does untrusted input meet the system
  (deserialization, subprocess invocation, file / network I/O,
  path handling)? If so, select the `security-review` module —
  the gate is trust-boundary-first; complexity tunes the review
  cadence and depth (see `modules/team-gated/security-review.md`).
* **Issue tracker?** Does the team use an issue tracker for gap /
  friction capture? If so, select the `issue-capture` module
  (see `modules/team-gated/issue-capture.md`).
