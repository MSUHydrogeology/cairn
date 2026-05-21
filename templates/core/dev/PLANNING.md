# {{project_name}} — development roadmap

`PLANNING.md` is the **roadmap board**: a current-state index of
what is queued and in flight. It is **not** a historical log —
completed items are *removed* from the board, not crossed off or
struck through, once their lasting truth has migrated to the
durable record (archived proposals and plans, implementing
commits, the changelog). See `doctrine/lifecycle.md` > "The
roadmap is a current-state index, not a historical log" for the
load-bearing reasoning.

`PLANNING.md` is a **shared communication file**: edited only at
defined serialization points — a lifecycle archive, the goodnight
routine, or explicit maintainer instruction — and referring to
proposals and plans by **filename stem**, not path link, so an
archive-move needs no edit here. The required-signal-read
discipline on shared communication files applies
(`doctrine/coordination.md` > "Required signal+read for
coordination-surface files").

## Where the project stands

<!-- cairn:slot project-status -->
(A few paragraphs — kept short — on where {{project_name}} is and
where it is headed, so a human or agent can come up to speed
quickly. The bootstrap seeds this from the Project Profile; it is
refreshed at the goodnight scrub.)
<!-- cairn:end project-status -->

## Queued

The forward-looking board: substantive work that is accepted or
anticipated but not yet in flight. When a queued item grows into
multi-step work, open a plan under `plans/` and replace the entry
with the plan's filename stem.

*(Empty at adoption — the first accepted proposals populate it.)*

## Active

Substantive work currently in flight: open plans, executing
sub-tracks, in-progress proposals between Decision and
plan-open. When an entry completes, it is **removed** from this
section at the next goodnight scrub — the truth migrates to the
archived plan / proposal, the implementing commits, and the
changelog. There is no "completed recently" section on this
board by design.

*(Empty at adoption.)*
