External-repo paths: `docs/methodology/coordination.md`, `docs/methodology/lifecycle.md`, `docs/methodology/session-routines.md`
# {{project_name}} — development roadmap
Written in Cairn Plain Language 1.0

## Waiting on you

List decisions, approvals and other next steps only the Maintainer can take.
Use one bullet for each wait. Keep the marker at the start of that bullet so
`python tools/board.py --maintainer` can find it. Remove the bullet when the
Maintainer responds.

When a wait belongs to work in a release table, put its marker on a separate
bullet outside the table. For example, a row might read `| Prepare release |
Run release checks | release plan |`; the sample wait below belongs to that
work:

> - **Waiting on Maintainer**: approve release

The quoted sample is guidance, not a live wait. On this board, write the bullet
without the quote marker. Do not put the marker in a table cell; the board
reader does not find it there.

*(Empty at adoption.)*

## Where the project stands

<!-- cairn:slot project-status -->
(A few paragraphs — kept short — on where {{project_name}} is and
where it is headed, so a human or agent can come up to speed
quickly. The bootstrap seeds this from the Project Profile; it is
refreshed at the goodnight scrub.)
<!-- cairn:end project-status -->

## Onboarding

The install seeds this section once from the selected profile preset and
module roster. Tasks are guidance, not module-selection or execution
authority. Once written, they belong to the project: later installs do not
restore, reconcile or backfill them. First adoption of a manually copied module
appends its task at the end of this board; repeat adoption leaves the board
unchanged.

<!-- cairn:slot onboarding-tasks -->
(Empty at adoption unless the bootstrap fills it from a profile
preset.)
<!-- cairn:end onboarding-tasks -->

## Current release

Put accepted work for the release in this table. Each row names the work, its
next step and the record with its evidence or history. Link a proposal or plan
by its filename stem so archiving it does not require a board edit.

| Work | Next step | Record |
|---|---|---|
| *(Empty at adoption.)* |  |  |

## Later releases

Keep accepted or anticipated work for a later release in a separate table.
When it starts, move it to the current release and update its next step.

| Work | Next step | Record |
|---|---|---|
| *(Empty at adoption.)* |  |  |

## Terms

- **Queued** — accepted or anticipated work that has not started.
- **Active** — work in flight, such as an open plan or executing sub-track.
- **Blocked** — work waiting on an outside dependency or a Decision. Name the
  blocker so someone can act on it.
- **Deferred** — work deliberately parked, with conditions for bringing it
  back to the current release.
- **Completed** — a short-lived state between finishing work and the next
  goodnight scrub. Then remove the item from the board.

Mark each item, or its release section, with `(Mon YYYY)` for when it was added
or last reaffirmed, such as `(May 2026)`. Refresh the date when reaffirming it
at a goodnight scrub. This makes the staleness check possible by reading the
board.

## Working rules (for agents)

- Treat this board as a current view of queued and active work, not a history.
  Remove completed items after their lasting truth has moved to durable records
  such as archived proposals and plans, commits and the changelog.
- Edit this shared file only at a defined serialization point: lifecycle
  archive, goodnight routine, or explicit Maintainer instruction. Use filename
  stems for proposals and plans, not links to paths that move when archived.
  Follow the required-signal-read discipline for shared communication files
  (Cairn's published coordination method, "Required signal+read").
- When multi-step standard or heavy work starts, open a plan under `plans/` and
  replace the queued entry with the plan's filename stem. Light work keeps its
  no-plan route, even when it has multiple steps.
- Human-run trust and release operations stay in separate standalone waits,
  with an owner, evidence requirement and link to the completed implementation. They
  are not final plan chunks or a reason to open a release plan. Plans finish
  after agent-owned scope, reviews and applicable checks, including change
  verification, are complete; archive is not permission to activate or release.
  A reviewed baseline awaiting a named human operation remains unpassed, while
  an unexplained integrity failure remains implementation work. Other
  outstanding operations remain blocked or unpassed until their evidence and
  authority exist.
- Give each item one status: `queued`, `active`, `blocked`, `deferred`, or
  `completed`. A deferred item needs revival conditions. Remove completed work
  at the next goodnight scrub; the board keeps no completion history.
- If the next step belongs to the Maintainer alone, add a separate bullet
  outside any table. Begin it with `**Waiting on Maintainer**: `, followed by
  a description under 48 characters. The reader accepts one optional `* ` or
  `- ` before the marker. Delete the bullet when the Maintainer responds.
- Before deleting a completed item, confirm all three removal preconditions
  below. If any is unmet, finish the migration first.

## Archive preconditions (proposals and plans)

Before a proposal or plan moves to `archive/`, every
**explicitly-deferred follow-up** it carries must carry a **recorded
disposition**. A disposition is not the same thing as a durable home:
the precondition exists so nothing is dropped *silently*, not so
everything is kept *forever*. Requiring a home for every deferral
makes this board the only sanctioned outcome, which turns it into a
one-way accumulator.

The vocabulary, restated here so the board can be read on its own. **This
copy is not the source — cite the governing statement instead**:
`dev/plans/_template.md` > *Dispositions* (and *Scope delta*, for the
scope-reduction rule in the `accept` entry), with the *why* in
Cairn's published lifecycle method > "Archive precondition".

* `accept` — fixed in scope. Includes writing the doc, and narrowing
  the artifact's own claim so the finding no longer applies (a
  *scope-cut*). **A scope-cut removes no work** — it corrects a claim
  to match what the artifact always did. Removing previously proposed
  or accepted work is a **scope reduction**, which is not an `accept`.
  Judge it against the baseline artifact's own commitments — the scope
  as *opened* before a Decision, as *accepted* after it: if every
  baseline outcome is still delivered the narrowing owes nothing, and
  otherwise it takes a `**Scope delta**` declaration, one grouped
  scope-remainder record per source artifact, and the Maintainer's
  explicit allowance. Neither author nor reviewer may concede a
  baseline outcome.
* `guard (<path>::<node>)` — homed in something that **executes** —
  a test node, an assertion, a runtime guard — and **names the node**.
  A comment is *not* eligible: comments do not fire, and a comment is
  a board row relocated somewhere fewer people read.
* `wontfix` — explicit non-action, **with a rationale**.
* `defer` — deposited on this board or appended to the receiving open plan.
  **Requires the Maintainer's authorization, quoted verbatim**, including
  the added scope in the receiving plan.

A deferral names one of the three reasons in the governing plan template's
*Dispositions*; a priority label is not a reason. This mirror adds no rule.

**No required order** — the record says why the chosen disposition is
right. Two eligibility rules bound it: a follow-up that **reaches an
adopter, blocks a release, or needs a Decision** cannot be `wontfix`;
and one **named by a closed artifact's disposition block** cannot be
`wontfix` without the Maintainer, because an archived record is
append-only and cannot be corrected in place.

Record each disposition in a durable, auditable location the team's
workflow preserves (the archive commit body, the PR description, or
the plan's closing metadata) as a `Dispositions: …` block, so the
outcome is reconstructible from the durable record alone. The older
`Follow-ups migrated to: …` spelling stays valid and is still
recognized. **Archive-preparation is the serialization point**, and
`defer` requests are presented there as **one batch** — that batching
is what keeps the Maintainer gate affordable.

On a **solo profile**, where author and Maintainer are the same
person, the `defer` gate collapses to a written justification to
oneself: weaker, but not vacuous — it is on the record at a
serialization point.

This precondition is **documentary, not mechanical**: a reviewer
opening the artifact at archive-preparation is the enforcer.

## Removal preconditions

A `completed` item is **removed**, not crossed off — but removal has gates.
Before deleting a board entry, confirm all three:

1. the accepted proposal / plan is archived;
2. its lasting truth has migrated to durable homes (doctrine, topic
   docs, the changelog);
3. the cold-start "what was tried, and why?" is answerable from the
   archives + commit log **without** this board entry.

If a gate is unmet, finish that migration first, then delete. See Cairn's
published lifecycle method > "Removal preconditions for a roadmap item".
