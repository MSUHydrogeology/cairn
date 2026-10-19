# A short tour of `dev/` -- the deliberation tree

The `dev/` tree is where Cairn writes things down. **Substantive
change is deliberated**: a proposal, then a review, then a
decision, then a plan, then implementing commits, then an archive.
This tour walks the five subdirectories with one paragraph each,
then runs a single trivial change through the full lifecycle as a
worked example. Best read after *doctrine/lifecycle.md* (which
carries the *why*; this is the *where*).

## The five subdirectories

### `dev/proposals/` -- the deliberation channel

A proposal is the unit of change. One open proposal per file;
filename is the stable handle the rest of the tree refers to.
Lifecycle: **open** (status `proposed`) → **reviewed** (a
reviewer appends a `## Review` section) → **responded** (the
author appends a `## Response`, often with body revisions) →
**decided** (the Maintainer appends a `## Decision` accepting or
rejecting) → **archived** (the accepted proposal `git mv`'s to
`dev/proposals/archive/`). Once archived, the proposal is the
canonical reasoning record -- everything downstream references
it. `dev/proposals/_template.md` is the structural baseline; new
proposals start by copying it.

### `dev/plans/` -- the implementation channel

A plan operationalizes an accepted proposal into reviewable
chunks. Each plan is its own file: header (touches + plan-review
line + related artifacts), context, chunk decomposition with
per-chunk acceptance criteria, verification, coordination, an
appended Review section + Response section, lasting-truth
migration. The plan archives at completion (`git mv` to
`dev/plans/archive/`). Plans are the *map* implementing commits
follow; commits themselves cross-reference the plan by filename.
`dev/plans/_template.md` carries the structural baseline.

### `dev/strategy/` -- the long-horizon framing channel

A strategy doc is a long-form framing -- a problem space
characterization, an audit of an emerging concern, a multi-year
direction sketch. Not yet a proposal; ground that proposals
later draw from. Strategies are append-only (revised by appended
sections, never overwritten) and they archive when their
substance has been fully absorbed into accepted proposals +
doctrine + the changelog. The shape of a strategy doc is more
fluid than a proposal's; the convention is "long-horizon honest
thinking that needs to be deliberated alongside the day-to-day
work."

### `dev/reflections/` -- the daily handoff channel

A reflection is one agent's session log -- what they tried, what
worked, what didn't, what the next session should pick up. The
directory is gitignored by default (the per-session content is
ephemeral); the tracked `README.md` is the directory guide.
Substantive observations migrate out (to proposals, to the
strategy/, to PLANNING). The reflection channel exists because
multi-agent and across-session-handoff coordination is friction
that compounds without the channel.

### `dev/.cairn/` -- the fold-back channel

A methodology improvement is filed as an issue on Cairn's own tracker.
A deployment captures Cairn-portable doctrine improvements here
-- changes that would help any differently-shaped team, not
just yours -- and the goodnight foldback-capture step keeps the
ledger populated. The ledger's job is to bridge the gap between
"noticed something generalizable" and "filed a Cairn upstream
issue or PR"; the fold-back issue template
(*.github/ISSUE_TEMPLATE/foldback.md*) walks you through
the filing when a candidate is ready.

## Worked example -- one trivial change end-to-end

The shortest illustration of the full lifecycle. Suppose your
project's README has a one-line typo: "scientifc" instead of
"scientific". A trivial fix; the lifecycle is still worth running
once to feel the shape.

**Step 1 -- open the proposal.** Copy `dev/proposals/_template.md`
to `dev/proposals/2026-MM-DD-<your-name>-readme-typo-fix.md`.
Fill in the header (author, model if AI, date opened, status
`proposed`). Write a one-line Context ("a typo in README; trivial
fix"), a one-line Proposal ("change `scientifc` to
`scientific`"), and a Rationale ("typo; no behavior change").
Commit: `git add dev/proposals/2026-MM-DD-... && git commit -m
"open proposal: readme-typo-fix"`. Status `proposed`.

**Step 2 -- review.** A reviewer (a different agent type if
you have one staffed; otherwise a fresh session of your agent,
or the Maintainer) appends a `## Review` section with a one-line
finding ("approve; trivial fix"). Status moves to `reviewed`. The
review commit carries the trailer naming the reviewer.

**Step 3 -- decide.** The Maintainer appends a `## Decision`
("Accepted -- the fix is correct; merge."). Status moves to
`accepted`. For trivial changes the proposal can also be its own
plan (no implementing chunks worth tracking separately); the
Decision section names this explicitly.

**Step 4 -- implement.** Make the actual README edit (fix the
typo). Commit references the proposal: `git commit -m "Fix typo
in README per accepted-proposal 2026-MM-DD-..."`. Implementing
commits cite the accepted proposal by filename stem.

**Step 5 -- archive.** `git mv
dev/proposals/2026-MM-DD-<...>.md dev/proposals/archive/` and
commit. The proposal moves to its permanent home; the deliberation
trail is now archival history. Status `archived`. The README typo
fix is a complete lifecycle artifact.

That five-step shape -- open / review / decide / implement /
archive -- holds for trivial changes (where every step is
one-line) up through multi-week proposals (where each step has
multiple commits + Review/Response rounds). The discipline
scales; the artifact tree is the same shape.

## Where to next

* Try the worked example above on a real change in your tree. A
  one-line README typo fix is a fine first run.
* When you're ready to coordinate across two or more agents, read
  *doctrine/coordination.md* -- it carries the work-intent
  mechanism that prevents collision.
* When your deployment's fold-back ledger has its first open
  candidate, the fold-back issue template
  (*.github/ISSUE_TEMPLATE/foldback.md*) is the natural
  next read.
