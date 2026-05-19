# Project Profile — legacy code-state assessment

> Fill this for a **legacy** codebase — one that predates the
> methodology. A bootstrapping agent completes it by inspecting
> the repository and interviewing the Maintainer; the result is
> presented for acceptance before Act II.

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

## Dimensional placement

The codebase axes, scored from the above (see `dimensions/` for the
rubrics):

* **Age:** legacy — {{age_note}}
* **Size:** {{size_position}} — {{size_reason}}
* **Complexity:** {{complexity_position}} — {{complexity_reason}}
* **Language:** {{language_position}} — {{language_reason}}
