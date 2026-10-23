# Case study: LHM, an 18-year-old hydrology model

> Written 2026-10-23 from LHM's own decision record. LHM and Cairn have the
> same maintainer, so this is an account of use, not independent evidence that
> Cairn works. The reviews described below ran under earlier versions of the
> method, which sometimes used several review rounds and a second AI tool as
> the reviewer; Cairn now asks for one round by a fresh reviewer, with more
> distance only when the Maintainer asks.

## The project

LHM (the Landscape Hydrology Model) is an integrated surface-water and
groundwater model from the MSU Hydrogeology Lab. It simulates snow, evapotranspiration,
runoff, routing and lakes, and couples them to a MODFLOW groundwater model. Its
history starts in 2008, imported from an older version-control system.

It is a hard place to bring AI agents into:

* **Old and largely untested.** The scientific core is about 89,000 lines of
  MATLAB, much of it written before automated tests were usual in the lab.
* **Two languages.** About 177,000 lines of Python wrap the core: data
  preparation, model setup, output products and a user interface. Part of the
  MATLAB is being ported to Python, and part will stay MATLAB.
* **Results people act on.** Research papers and partner projects use its
  water budgets, recharge and streamflow, so a wrong number that runs cleanly
  is the failure that matters most.

LHM has used Cairn since May 2026. Its record holds 58 proposals and 56 plans.

## How Cairn is set up there

LHM uses the heaviest configuration of any Cairn project, because each of its
difficulties has a module that answers it:

| LHM's difficulty | What Cairn adds |
| --- | --- |
| Three distinct parts of the code (inputs, the model core, outputs) | **Domain agents**: an agent role for each part, which proposes, plans and builds within it |
| A large core with few tests | A **legacy agent** role that writes tests pinning what the old code does today, and keeps a map of which parts are safe to change |
| MATLAB and Python side by side | **Two-language testing**, so a ported function is checked against the MATLAB it replaces |
| Several agents in the repository at once | **Work intents**: an agent claims the files it is about to edit, so two agents do not collide |

One human, the Maintainer, makes every decision. Reviews are written by an
agent session that did not write the work. Everything else in this page
happened inside that arrangement.

## What the record shows

### Lakes that froze in January and never thawed

**The problem.** On the Cedar Creek test basin, the model's lakes froze on
3 January and never melted. Because the model believed the lakes were iced
over all summer, warm humid air condensed onto them, and the model invented
about 250 mm of water a year: 28% of the basin's precipitation. The water
budget closed perfectly. In the proposal's words:

> "The model's water-balance check cannot see this, because the invented
> water is booked correctly"

**What review caught.** The proposal's first fix changed one line. The
reviewer did not take it on trust: it ran the changed code on a small test
case and showed that ice sitting at exactly 0 °C still produced no melt, hour
after hour. It also found that condensation below freezing was charged the
heat of forming ice but then stored as liquid water. It pointed out that a test of the
water balance could never catch that, because the error is in the energy
budget, so the plan added tests that check the energy budget too.

**At code review**, a second reviewer found that one new tolerance could not
fail in summer. In August it allowed more than the month's entire runoff. The
Maintainer weighed the options and decided, in writing: *"Go with (c),
revisit after the warm start"*. The tolerance shipped, with an issue filed
to revisit it.

**Where it is:** `dev/proposals/archive/2026-10-15-claude-lake-ice-melt.md`
and the plan of the same name, in the LHM repository.

### A "bug" that was holding the flow network together

**The problem.** A proposal set out to fix what looked like a defect: a step
in the flow-routing code that turns missing values into zeros.

**What review caught.** The reviewer measured what the fix would do before
anyone wrote it. On a small test grid, the current code gave all 85 valid
cells a flow direction. The proposed fix left only 41. The "bug" was what
connected flow around the edge of the domain and every lake margin. The
Maintainer confirmed it in one line: *"The NaN→0 collapse is intentional for
exactly the reason you specify."*

**The Maintainer's call.** A later reviewer pushed to convert all 8-bit
rasters to floating point when they are read, to make missing values
explicit. The Maintainer refused on domain grounds, and that is now on the
record:

> "We should not promote, definitively so. Every user of an 8-bit raster
> knows that there is a number that codes for NaNs."

**Where it is:** `dev/proposals/archive/2026-07-29-claude-d8-flow-direction-dtype.md`.

### A storage product off by a factor of 1,000

**The problem.** A proposal promised a total-water-storage product in
kilograms per square metre, the unit used by satellite gravity missions, so
model storage could be compared with them. The model works in metres of
water, and the proposal never converted.

**What review caught.** A reviewer from a second AI tool spotted it:

> "Merely assigning `units = "kg m-2"` would make every component and the
> total wrong by 1000 for the normal metre case."

It also noticed that MODFLOW can be run in feet. The revised design converts
every component through one shared step and refuses to run on a length unit
it does not recognise, with tests that feed in exactly 1 m and 1 mm.

**Where it is:** `dev/proposals/archive/2026-08-03-claude-storage-netcdf-product.md`.

## What it cost

The record is honest about the overhead, and so is this page.

* **The storage proposal took six rounds of outside review** before the
  Maintainer decided. Some of that was earned (the factor of 1,000), and some
  was not: an earlier review made two claims the author later showed were
  wrong, and the author admitted adding sections without first reading a
  blocking finding. Episodes like this are why Cairn now asks for **one**
  round of review, with a second only when a revision adds something new.
* **The apparatus is large.** Domain agents, a legacy agent, two-language
  testing and work intents are a lot to run. LHM carries them because its
  code is old, large and in two languages; a younger or smaller project
  should not.

## What to take from it

* **A closed water balance is not a correct model.** Two of the three
  stories are errors a conservation check could not see. Cairn's rule that a
  scientific change names one check whose expected answer comes from outside
  the code exists because of failures like these.
* **Ask the reviewer to measure, not only to read.** The most useful reviews
  here ran the code on a small case (melting ice at 0 °C, an 85-cell grid)
  and reported numbers.
* **The Maintainer's domain knowledge is part of the method.** Twice the
  deciding word was the scientist's, and it is now written down where the
  next agent will find it.

## Sources

Every path above is in the LHM repository, not in Cairn.

External-repo paths: `dev/proposals/archive/2026-10-15-claude-lake-ice-melt.md` `dev/proposals/archive/2026-07-29-claude-d8-flow-direction-dtype.md` `dev/proposals/archive/2026-08-03-claude-storage-netcdf-product.md`
