# Case study: modflow_tools, a groundwater-modelling toolkit

> Written 2026-10-23 from modflow_tools' own decision record. modflow_tools and
> Cairn have the same maintainer, and Cairn was first worked out on this
> project, so this is an account of use, not independent evidence that Cairn
> works. The reviews described below ran under earlier versions of the method,
> which sometimes used several review rounds and a second AI tool as the
> reviewer; Cairn now asks for one round by a fresh reviewer, with more distance
> only when the Maintainer asks.

## The project

modflow_tools builds, reviews and calibrates groundwater models. A modeller
describes a model in YAML files; the toolkit builds it for MODFLOW 6 through
FloPy, reviews existing MODFLOW-2005 and MODFLOW-NWT models, and runs
calibration and uncertainty analysis with PEST++ and pyEMU. It is meant to
help graduate-level hydrogeologists put together regional models they can
defend.

* **Built with AI agents from the start.** The first commit is from June
  2025, and the project now holds about 160,000 lines of Python.
* **Where Cairn came from.** The working method was worked out here, under
  pressure from real failures, and later pulled out into its own repository.
* **Correct code can still be wrong science.** A change can pass every test
  and still have a wrong sign convention, wrong units, or a misread statistic.

Its record holds 147 proposals and 107 plans, although many concern the
method itself rather than hydrology.

## How Cairn is set up there

modflow_tools runs one Maintainer and several agents, with a fresh agent
session reviewing what another wrote. Its install adds sixteen modules,
among them testing tiers, a check that the documentation still matches the
code, security and architecture review, and **work intents**, so that two
agents editing at the same time claim their files first and do not collide.

## What the record shows

### Calibration statistics that measured the wrong thing

**The proposal.** Add tables to the calibration results showing which
observations are most worth collecting, and how much each group of
parameters contributes to the uncertainty of a forecast.

**What review caught, before any code was written.** Two errors in the
mathematics, either of which would have produced tables that look right and
mean something else:

* The "data worth" table was framed as the increase in the model's misfit if
  an observation were removed. The pyEMU function it relied on returns
  something different: the forecast's uncertainty after removing it.
* The plan included a test that the parameter groups' contributions add up to
  100%. They do not, and should not: each is computed as if that group alone
  were known perfectly, so when parameters are correlated the shares overlap.

Both were redesigned in the proposal. The Maintainer's decision says why the
review was worth having:

> "would have shipped wrong contracts; worth the antagonistic round."

**The record paid off again.** The same proposal set aside two related tables
for later. Sixteen days later a new proposal picked them up, starting from
the written reasons rather than from memory.

**Where it is:** `dev/proposals/archive/2026-05-05-claude-tier-1.4-fosm-tables.md`
and `dev/proposals/archive/2026-05-21-claude-per-observation-data-worth.md`,
in the modflow_tools repository.

### A review report that would have told a client the wrong cell count

**The proposal.** Fix the toolkit's model-review report, which silently left
out evapotranspiration and drew no recharge or evapotranspiration on its maps.

**What review caught.** The reviewer did not stop at the proposal's list. It
ran the report against all three MODFLOW versions and found a defect the
author had walked past: the boundary-condition cell count counted every
stress-period record, not distinct cells. The same 12-cell model was reported
as 12 cells on one version and 24 on the others:

> "the deliverable report states **24 CHD cells for a 12-cell model** on two
> of three backends"

The fix counts distinct cells, and a test now checks that all three versions
agree.

**Where it is:** `dev/proposals/archive/2026-08-19-claude-review-report-areal-bc-parity.md`.

### The Maintainer overruling a safeguard

**The problem.** Quadtree meshes, which refine the grid around features like
rivers and wells, could not be built at all, and nothing in the test suite
exercised them.

**The disagreement.** The fix filled in missing layer elevations with a
placeholder (a top of 1 and a bottom of 0). The author worried this was
"silently wrong geometry" and wanted extra guards. The Maintainer disagreed,
from experience: a one-metre-thick model gives heads and a mass balance so
obviously absurd that no modeller would miss them.

> "Honestly I think that a sentinel like 1 is entirely fine. That is
> obviously not a real elevation"

The guards were dropped, and the plan instead required a test that the mesh is
actually refined, which "it builds" alone could not pass.

**Where it is:** `dev/plans/archive/disv_quadtree_base_elevations.md`.

## What it cost

* **The quadtree fix was small, and its plan grew to over 4,000 lines**, with
  four rounds of plan review and four of code review in a single day. The
  Maintainer ended it in one sentence: *"Archive, please, we don't need to get
  too caught up in the lifecycle_planner ceremony"*. Episodes like this are why
  Cairn now asks for one round of review, and why it no longer runs the tool
  named in that sentence.
* **Not every check earned its keep.** One check on numbers quoted in
  documents was retired after 17 logged uses had caught nothing.

## What to take from it

* **The most valuable reviews here were about meaning, not code.** A table
  that measures the wrong quantity, or a count that differs between MODFLOW
  versions, passes ordinary tests. A reviewer who asks "what does this number
  mean?" catches it.
* **Review before code is cheap.** The calibration errors were fixed by
  editing a proposal, not by rewriting a feature and its users' results.
* **The record outlives the session.** Work set aside on 5 May was picked up
  on 21 May from the written reasons, not from anyone's memory.
* **Watch the overhead.** The same record that caught these errors also shows
  ceremony outgrowing the work. A working method has to keep being trimmed.

## Sources

Every path above is in the modflow_tools repository, not in Cairn.

External-repo paths: `dev/proposals/archive/2026-05-05-claude-tier-1.4-fosm-tables.md` `dev/proposals/archive/2026-05-21-claude-per-observation-data-worth.md` `dev/proposals/archive/2026-08-19-claude-review-report-areal-bc-parity.md` `dev/plans/archive/disv_quadtree_base_elevations.md`
