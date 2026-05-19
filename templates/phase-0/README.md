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
