# Phase 0 — Understand

Phase 0 is **Act I** of the bootstrap: *understand the project
before installing any process.* It runs before a single template
is copied, and it produces two durable artifacts the rest of the
bootstrap reads — the **Project Profile** and the **Team Profile**.
Both are presented to the Maintainer for acceptance before Act II
(Install) begins.

## The two profiles

* **Project Profile** — positions the codebase on the codebase
  axes (Age, Size, Complexity, Language; see `dimensions/`). It
  has two branches:
  * *Legacy* — a full code-state assessment:
    `project-profile-legacy.md`.
  * *Greenfield* — a light project-design checklist:
    `project-profile-greenfield.md`.
* **Team Profile** — positions the team on the team axes (Human
  team, Agent team) and records a current-practice baseline:
  `team-profile.md`.

## Why both, and why first

The Project Profile decides *what apparatus the codebase warrants*;
the Team Profile decides *what apparatus the team can staff*. The
dimensional matrix needs both — a 5,000-line repo with five
contributors and a 200,000-line solo repo select very differently.

The Team Profile's **current-practice baseline** — how the team
works today, and what hurts — is what Act III's measurement is
later read against; without it, "improvement" is unmeasurable.

These templates carry `{{placeholder}}` tokens and block slots; a
bootstrapping agent fills them by inspecting the repository and
interviewing the Maintainer.

## Governance presets — the fast path

Filling both profiles and hand-deriving the module roster from the
six axes is the principled path. The **fast path** is a *governance
preset*: a named point in the six-axis space that pre-fills a sensible
profile, which the adopter then adjusts. Three are shipped:

* **`solo-greenfield`** — a solo maintainer on a new, small, simple
  codebase: the default-on disciplines, no coordination machinery.
* **`collaborative-team`** — a small concurrent multi-agent team on a
  moderate codebase: + coordination-tiers, dual-review, and the
  practice modules the moderate-complexity gate selects.
* **`high-rigor-legacy`** — a large, complex, multi-language legacy
  codebase with a full team: the broad set (legacy-agent,
  security-review, dual-language-tests, the practice modules, +
  coordination).

A preset is **composable, not rigid**: it sets the baseline; the
adopter overrides any individual axis (the real team axes always win on
staffability) and adds/removes any individual module on top
(`modules_add:` / `modules_remove:`). Start from the preset whose
canonical point is closest to the project, then tune the axes in the
profile templates below to the project's real scores. The per-preset
rosters, the six-axis points, and the config shape are in
`../../bootstrap/BOOTSTRAP.md` (Act I-5 "Fast path — governance presets"
and Appendix B); preview a resolved profile with
`python bootstrap/scaffold.py --summary --config <profile>`.
