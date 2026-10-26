# A short tour of `dev/` -- the deliberation tree

The `dev/` folder is where your project writes down what it decided
and why. Every change goes into one of three lanes, chosen before any
file is written. Most changes take a light lane; only a few take the
full one. This tour says what each part of `dev/` holds, then shows the
light lane on a typo and points to the full lane in Cairn's README.
Best read after *doctrine/lifecycle.md*, which carries the *why*; this
is the *where*.

## What lives in `dev/`

### `dev/proposals/` -- the written case for a big change

A proposal explains a substantial change before anyone builds it: the
problem, the change, the alternatives, and what would show it wrong.
One proposal per file; the filename is its handle. Its status always
says who moves next:

`awaiting-review` → `revising` → `awaiting-decision` → `accepted`,
`rejected` or `superseded`.

A fresh reviewer who did not write the proposal appends a `## Review`.
The author appends a `## Response` and a revised proposal. The
Maintainer appends a `## Decision`. Proposals are append-only: nothing
already written is edited, so the file shows what was believed at each
point. A rejected or superseded proposal moves to
`dev/proposals/archive/` with its Decision; an accepted one moves when
its plan opens or its change ships. `dev/proposals/_template.md` is the
starting point.

### `dev/plans/` -- how an accepted proposal gets built

A plan splits accepted work into chunks, each with its own acceptance
criteria and how it will be checked. A fresh reviewer reads the plan
once, then you implement, and a code review checks the result. The plan
moves to `dev/plans/archive/` when the work is done. Commits cite the
plan by filename. The short change note used by the standard lane
follows the same plan template. See `dev/plans/_template.md`.

### `dev/strategy/` -- thinking before a proposal

A strategy note is long-form framing: a comparison of tools, an audit
of a worry, a direction sketch. It is not yet a commitment. Unlike a
proposal, a strategy note is **revised in place**: when a review
arrives, the author folds in what they accept and deletes the review,
so the note stays clean. The history lives in `git log`. A note
archives once accepted proposals and doctrine have absorbed it.

### `dev/reflections/` -- session logs

A reflection is one agent's session log: what it tried, what worked,
what the next session should pick up. The folder is gitignored by
default, because the per-session content is short-lived. Anything
that matters moves into a proposal, a strategy note or the roadmap.

### The rest of `dev/`

| Path | What it holds |
|------|---------------|
| `README.md` | Entry point to the tree. |
| `agent_collaboration.md` | The roles and the review loop. |
| `PLANNING.md` | The roadmap board: queued and active work. |
| `NEXT_SESSION.md` | The handoff: what to start next. |
| `modules/` | One file per installed optional module. |
| `upstream/` | Drafts of bug reports for outside tools your project depends on. |
| `rules/` | Detail for your project's own agent rules, routed from `RULES.md`. |

### `dev/.cairn/` -- install state, not for editing by hand

This folder holds what the installer needs to update your copy of
Cairn later: the lockfile, base copies of installed files, your
profile, and local settings. It is not a log of ideas.

If you find an improvement that would help other teams too, file it as
an issue on Cairn's own tracker. The template is
`.github/ISSUE_TEMPLATE/foldback.md` in the Cairn repository.

## The three lanes

1. **Trivial** -- a typo or one-line fix. Make the change and its test
   in one commit. No proposal and no code review.
2. **Standard** -- the shape is settled, but the change is not trivial.
   Write one short change note (why, what, approach, verification,
   risk), have it reviewed, then make the change and its test, then a
   code review.
3. **Deliberate** -- a new feature, a contract change, or a
   high-risk surface. Proposal, review, the Maintainer's decision,
   plan, plan review, change and test, code review, archive.

When you are unsure, take the heavier lane. Every step is its own
commit.

## Worked example -- a typo, in the trivial lane

Suppose your README says "scientifc" where it means "scientific".

Edit the word and commit it with a message that says what changed. A
README typo has no behavior to test, so the edit is the whole change.

That is all: no proposal, no plan, no review, no archive. A typo fix
that touches a contract or a high-risk surface is not trivial, so take a
heavier lane. If you want another model or a person to look at a
trivial change anyway, that is your call as Maintainer. Running this
change through a proposal would cost more attention than the typo is
worth.

For the full lane from start to finish, see the toy example in Cairn's
README ("A toy example: asking for a new feature"). It follows one
feature request through proposal, review, decision, plan, build and
code review.

## Where to next

* Try the typo fix above on a real change in your tree.
* When you coordinate two or more agents, read *doctrine/coordination.md*;
  it covers the work-intent mechanism that prevents collisions.
* When you have an improvement for Cairn itself, the template
  `.github/ISSUE_TEMPLATE/foldback.md` in the Cairn repository walks
  you through filing it.
