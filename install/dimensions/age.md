# Age — greenfield ↔ legacy

A codebase's **age** is whether it was built with this methodology
from the start (greenfield) or predates it and is being
retrofitted (legacy). Age drives the single largest block of
optional apparatus: a legacy codebase needs a *retrofit* layer a
greenfield one does not.

## Scoring rubric

Place the codebase by these observable signals:

* **History.** How long has the codebase existed, and how much of
  its history predates any AI-team or recorded-deliberation
  practice?
* **Test coverage of existing surfaces.** Greenfield code is
  tested as it is written; legacy code often has large untested
  regions.
* **Documentation trust.** Are the existing docs and docstrings
  known to be accurate, or known to have drifted from the code?
* **Modernization debt.** Are there surfaces nobody wants to touch
  — code whose behavior is load-bearing but not understood?

A codebase need not be uniformly one or the other. A **mixed**
codebase has greenfield and legacy *surfaces*; score the surfaces,
not only the repository.

## Positions

### Greenfield (AI-team-first)

The codebase is built under the methodology. No retrofit
apparatus:

* No Legacy Agent role.
* Tests, documentation, and examples are **absorbed into every
  proposal** as required, omission-is-a-finding template prompts —
  a change ships with its tests because the proposal template will
  not let it ship without them.
* No surface-readiness map and no attic; there is no legacy
  material to quarantine.

### Legacy (retrofit)

The codebase predates the methodology. A standing retrofit layer:

* A **Legacy Agent** role — a standing frame responsible for the
  untrusted surfaces.
* A **surface-readiness map** — every surface classified Ready /
  Transitional / Frozen, so a contributor knows whether a surface
  may be changed freely, changed with care, or not at all.
* A **characterization-testing** discipline — before changing
  legacy behavior, pin the *current* behavior with tests, so the
  change is visible against a known baseline.
* An **attic** for relocated legacy material, and a codebase-wide
  docstring-modernization sweep.

### Mixed

The Legacy Agent role and the readiness map are scoped to the
legacy *surfaces* only; greenfield surfaces follow the
absorbed-test path. This is the common real case — most retrofits
grow greenfield regions over time.
