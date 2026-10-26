<!-- The dev/ paths below refer to ADOPTER install destinations.
     From Cairn's own checkout some of them do not resolve (the source
     of truth for the task lists lives at templates/onboarding/<preset>.md).
     Exempted so the adopter-facing cite stays correct -- parallel to the
     fold-back.md pattern. -->

# Onboarding -- once, at install

Cairn onboards once, at install. While the scaffold runs, it writes the
profile's day-one tasks into `dev/PLANNING.md`, puts two tour pages in
`dev/modules/onboarding/`, and ends its report with one line that says
where the task list is. The project then holds everything onboarding
gave it. Nothing watches the project afterward, nothing adds a task
later, and no prompt appears at a later session. Nothing activates later.

## The two parts

### The day-one task list

`templates/core/dev/PLANNING.md` carries a
`<!-- cairn:slot onboarding-tasks -->` block between
`## Where the project stands` and `## Queued`. The scaffold fills it at
install from the profile you chose:

* `solo-greenfield` -- one human and one AI agent on a new codebase.
* `collaborative-team` -- 2-4 humans and 1-2 agent types on a
  greenfield or near-greenfield codebase.
* `high-rigor-legacy` -- 5+ humans, several agent types, a legacy
  codebase, several languages and security boundaries.

Each profile's task list lives at `templates/onboarding/<profile>.md`.
The scaffold inlines its seed tasks into the slot, with a
`<!-- preset: <name> -->` comment that names the profile. The list does
not grow after that: a profile seeds 6, 10 or 11 tasks, and every one is
a plain task an adopter can read, do and delete.

Every profile also seeds a day-one pointer to the lifecycle skills
(`session-start`, invoked as `/session-start`). The scaffold installs
those skills unconditionally and reports the count.

Three short pointers say where the list is: the last line of a
successful install, one sentence in `bootstrap/BOOTSTRAP.md` step II-6,
and one bullet in the `session-start` routine, which names the first
open task under Onboarding as a candidate for the operator.

### The tour pages

Two pages are installed to `dev/modules/onboarding/` for every profile:

* `dev-tour.md` -- the `dev/` subdirectory taxonomy and a worked
  example. Every profile's seed list points at it from day one.
* `agent-team-onboarding.md` -- the checklist for adding another agent
  type. The collaborative and legacy profiles reach it from the roster
  task; the solo profile reaches it through one sentence on its
  `skim-coordination-doctrine` task.

The upstream PR and issue walkthrough is a day-one seed task that hands
off to the fold-back issue template
(`.github/ISSUE_TEMPLATE/foldback.md`).

## Dispatching an agent session

The apparatus assumes you can hand a *fresh* agent session the context it
needs to act in the right frame. That hand-off is vendor-neutral doctrine:

* **Name the role first.** Open the session by stating its role (Strategy, a
  Domain, Legacy, the Reviewer -- see `doctrine/roles.md` > "When to
  dispatch which role"). The role determines the artifact; an unframed
  session defaults to whatever the prompt's verb implies, which is often the
  wrong frame.
* **Hand it the orientation, not the whole history.** Point the session at
  the `dev/` tree (the deliberation surfaces it will read and write) and at
  the one artifact this task turns on -- the proposal it implements, the plan
  it reviews, the issue it diagnoses -- rather than replaying the prior
  session. The durable record *is* the context; that is what it is for.
* **State the task and its boundary.** What this session should produce, and
  explicitly what it should *not* touch (the scope fence). A session given a
  clear "not this pass" stays bounded.

**Vendor boundary (load-bearing).** *How* you literally start a session -- the
command, the IDE action, the API call for a given agent harness -- is **not**
Cairn doctrine and is deliberately absent here: it is per-vendor and changes
faster than the methodology. Those mechanics live in your **vendor wrapper**
(the agent-specific file that imports the kernel `AGENTS.md` -- a
`CLAUDE.md`-style doc), which is where a harness-specific habit belongs. Cairn
stays vendor-neutral; the wrapper carries the spawn recipe.

## Cross-references

* `doctrine/lifecycle.md` -- the proposal-lifecycle the seed
  tasks introduce.
* `doctrine/roles.md` -- the role roster + the "When to dispatch which role"
  heuristics a fresh session is framed by.
* `doctrine/coordination.md` -- the work-intent mechanism the
  multi-agent presets exercise from day one.
* the retired fold-back doctrine -- the 6-step protocol the
  walk-foldback-protocol seed task invokes.
* `docs/tool-usage.md` -- worked invocations of the shipped tools
  (`claim_check`, `intent.py`, `lifecycle_metrics`, `link_check`).
* `on-ramp/README.md` -- the two ways to adopt Cairn: read the
  doctrine, or install it with the scaffold and a profile.
