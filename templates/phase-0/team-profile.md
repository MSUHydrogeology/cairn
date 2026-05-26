# Team Profile

> Fill this for **every** adoption — greenfield or legacy. It
> positions the team on the team axes and records the
> current-practice baseline.
>
> **Fast path:** a governance preset pre-fills the team axes, but the
> **real team axes always win on staffability** — a preset never
> installs coordination apparatus a solo / single-agent team can't run.
> Record the team's actual axes here. See `README.md > Governance
> presets`.

**Project:** {{project_name}}
**Assessed:** {{YYYY-MM-DD}}

## The humans

<!-- cairn:slot human-team -->
(Count and roles — the PI, the contributors, the students — and
the one designated Decision-authority Maintainer.)
<!-- cairn:end human-team -->

## The agents

<!-- cairn:slot agent-team -->
(Count and types of AI agents on the team — the same type, or
different types.)
<!-- cairn:end agent-team -->

## Current-practice baseline

<!-- cairn:slot current-practice -->
(How the team works *today*: solo, or with pull-request review?
Continuous integration? Session handoffs? What hurts? This is the
baseline Act III's measurement is read against — without it,
"improvement" is unmeasurable.)
<!-- cairn:end current-practice -->

## Dimensional placement

The team axes, scored from the above (see `dimensions/` for the
rubrics):

* **Human team:** {{human_position}} — {{human_reason}}
* **Agent team:** {{agent_position}} — {{agent_reason}}

### Module-selection signal

* **Issue tracker?** If the current-practice baseline above shows
  the team uses an issue tracker for gap / friction capture, select
  the `issue-capture` module — the standing capture surface for the
  User Agent role (see `modules/team-gated/issue-capture.md`).
