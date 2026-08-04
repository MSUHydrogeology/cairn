<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/lifecycle.md doctrine/plans.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- Author tip: numeric claims follow the three-kind precision /
     `as_of` discipline -- approximate a decision-irrelevant count
     (`~4900 lines`), date a snapshot (`N, as_of YYYY-MM-DD`, never
     re-measured), register a live invariant; never quote one from
     memory.  Chunk-size estimates ("ships in 2-3 commits") are
     decision-irrelevant -- approximate them.  See `doctrine/plans.md` >
     "Count claims".  (The old `claim_check` count soft-flag +
     `claim-check-allow-count` directive were retired 2026-06-05 --
     claim_check no longer flags counts.) -->

# Plan template

> **This is the plan template.** A non-trivial accepted proposal
> opens a plan: copy the section template below the rule into
> `dev/plans/<short-slug>.md`. The lifecycle, archive-precondition,
> plan-review-precondition, triage, mutability, planning-handshake,
> forward-reference-path, count-claim, and plan-review/code-review
> doctrine above the rule live in `doctrine/plans.md` — read it once,
> then work from the sections below.

## The plan lifecycle

See `doctrine/plans.md` > "The plan lifecycle" for the full lifecycle
diagram, the plan-archive precondition (a plan never archives until
a code review has occurred), the plan-review precondition (a
review-required plan does not start implementation until its plan-review
section has landed), the release-gated parked-state note, and the
fast-multi-stage sub-pattern.

```
open -> [awaiting-plan-review] -> executing -> review -> archived
```

A plan is an *execution* artifact: status, progress markers, and commit
hashes are updated in place. Review findings and the archive record are
**append-only**. See `doctrine/plans.md` > "Mutability rule" for the
full mutable-in-place vs. append-only split.

**The plan is Stage 2 of the Registered Report** (see
`doctrine/lifecycle.md` > "The lifecycle as a Registered Report"):
the plan and its code review check the implementation and the evidence
it produced against the locked proposal (Stage 1).

## Plan triage rule

See `doctrine/plans.md` > "Plan triage rule" for the full rule.

Open a plan when an accepted proposal's implementation: (a) lands
across multiple commits, (b) touches multiple files / areas, (c) has
multi-stage sequencing, or (d) carries deferred follow-ups. Skip the
plan when the implementation is a single commit, single-file / single-area,
with no follow-ups needing a durable home.

## Forward-reference paths — `Proposed paths:` marker doctrine

See `doctrine/plans.md` > "Forward-reference paths" for the full
marker mechanism, placement rules, and the two other marker keywords
(`Untracked paths:`, `External-repo paths:`).

Place `Proposed paths:` lines near the top of the plan (after this section,
before `## Scope`), each listing a batch of related tokens. The marker
exempts tokens on its own line and any contiguous structured block
immediately beneath it.

## Count claims — the three-kind precision / `as_of` discipline

See `doctrine/plans.md` > "Count claims" for the three-kind discipline
(decision-irrelevant / dated snapshot / live invariant) and the retired
`claim-check-allow-count` directive.

---

# Plan: {{short title}}

**Source proposal**: {{link to dev/proposals/archive/...}}
**Status**: open
**Plan review**: {{required(<tier>) | not required(<rationale>)}}
**Last update**: {{YYYY-MM-DD}}
**Opened**: {{YYYY-MM-DD alongside the proposal's Decision-and-archive commit}}

## Source proposal

A one-paragraph summary of what the proposal decided. The plan
executes the decision; it does not re-litigate it.

## Proposed paths

*(Optional. Populate as forward-reference paths accrue — relocation
targets, suggested filenames, future module homes — so they don't
trigger `claim_check` while the plan is being authored. Each entry is
the path **and** a one-line note on what it is / when it materializes.
Remove the section if empty. Once a path resolves on disk, drop its
line.*

*Three structural rules for the marker to work: (a) the literal
`Proposed paths:` line below is the marker `claim_check` matches —
don't drop it while bullets remain; (b) **no blank line between
the marker line and the first bullet** — `claim_check`'s
continuation check uses original line numbers, so a gap breaks
adjacency; (c) **keep each bullet on a single physical line** —
wrapped/indented bullet continuations close the marker block and
re-expose subsequent paths to hard-check.)*

Proposed paths:
- `path/to/proposed/file.md` — what it is; when it lands.

## Scope

What this plan executes — and, explicitly, what it does *not* (the
**scope fence**: work the proposal deferred to a follow-up, and
anything deliberately left untouched this pass). Cite the proposal's
"v1 scope" (or equivalent) as authoritative; if the proposal deferred
work to a later phase or proposal, name the deferrals explicitly so
they don't drift back into this pass by accident. See
`doctrine/plans.md` > "The planning handshake" for the convergence
questions this section answers.

### Documentation / doctrine surface

What documentation, doctrine, or contract surface does this plan
touch? If none, say so explicitly — silent omission is a code-review
finding (the plan must name what doc state is mutated, not surface
it at review time).

<!-- cairn:slot documentation-tier-home -->
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
plan's *Scope* must name the doctrine-surface touched (or an explicit
"no doctrine surface").
<!-- cairn:end documentation-tier-home -->

## Sequence

Rough commit-by-commit execution order. Allowed to evolve as work
proceeds; revisions are append-only (don't edit prior Sequence entries
that are already in flight — add a "Sequence revision YYYY-MM-DD"
sub-section if the plan materially changes).

```
1. <chunk A> -- <one-line description>      [commit <sha or "pending">]
2. <chunk B> -- <one-line description>      [commit <sha or "pending">]
3. <chunk C> -- <one-line description>      [commit <sha or "pending">]
```

For larger plans, break each chunk into its own subsection with a file
table:

### Chunk A -- <descriptive name>

| # | File | Change |
|---|------|--------|
| A1 | `path/to/file` | <code change> |
| A2 | `path/to/tests/test_<thing>` | <test that pins the contract> |
| A3 | `docs/<topic>` *(if user-facing or developer-facing docs change)* | <topic-doc update> |
| A4 | `CHANGELOG.md > Unreleased > Added/Fixed/Changed` *(if release-facing behavior changes)* | <release-note line> |

For multi-chunk plans where doc updates cut across implementation
chunks, **prefer a dedicated documentation chunk** to repeated
"no change" rows in every chunk:

### Chunk D -- documentation

| # | File | Change |
|---|------|--------|
| D1 | `docs/<topic>` | <topic-doc update covering all impl chunks> |
| D2 | `CHANGELOG.md > Unreleased > Added` | <release-note line> |

Authors choose between per-chunk conditional rows (small / single-area
plans) and a dedicated documentation chunk (large / cross-cutting
plans).

## Acceptance criteria

The concrete deliverables that define "done". The first three — tests,
docs, examples — mirror the proposal template's evidence treatment;
name each, or give an explicit "**N/A**: <reason>".

* **Tests that must pass**, named by tier (or "**N/A**: <reason>" —
  e.g. a pure-doc plan).
* **Doc updates that must land** (or "**N/A**: <reason>"). Doc updates
  come in three shapes; route each correctly:
  - **Hand-authored** — narrative docs you edit directly.
  - **Generated** — docs rendered from a source by a script: update
    the source, run the generator, never hand-edit the rendered file.
  - **Snippet-synced** — doc fenced blocks pulled from example sources
    via directives: update the source, then run the sync.
  - `CHANGELOG.md > Unreleased > Added/Fixed/Changed` — one-line
    release note.

  <!-- cairn:slot acceptance-doc-tooling -->
  Cairn's doc surface is mostly hand-authored Markdown read on GitHub;
  the doc tooling is drift-prevention, not generation:
  - **Snippet-sync** — `python scripts/sync_doc_snippets.py` pulls
    fenced blocks from runnable example sources into docs; update the
    source, then run the sync (never hand-edit a synced block).
  - **Prose-integrity gate** — `python scripts/check_cairn.py` resolves
    every internal Markdown link / anchor and every claim-path; it is
    the doc smoke for any Markdown change.
  - **Link check** — `python scripts/link_check.py` for the broader
    cross-reference sweep.
  There is no schema-render generator; a plan that introduces one names
  its source + render command here.
  <!-- cairn:end acceptance-doc-tooling -->
* **Examples / smoke checks required** — name the artifact and, if it
  is not a runnable command, the gate that verifies it (snippet-sync,
  doc-link, etc.). Or "**N/A**: <reason>".
* Inbound path-link updates in `dev/` docs that link the moved file.
  `PLANNING.md` and `NEXT_SESSION.md` refer to plans by filename stem,
  not path link (per `AGENTS.md > Shared communication files`), so they
  need no update on an archive-move.

### Author-accounting — invariants, failure modes, edge cases

<!-- Triage-gated (high-stakes changes only; a one-line "N/A: no new
contract / invariant / public path" for routine) — same discipline as the
proposal template's author-accounting. At PLAN stage the satisfier is
*sequencing*: each invariant has an enforcing test sequenced into a chunk,
and each public entry point this plan touches is mapped, in its acceptance
criteria, to the test that exercises it through its public path. Cite tests
as relative markdown links so the link checker verifies they exist. Include a
known-omissions line. Reviewed as evidence — the reviewer challenges a row or
names the one they sampled, never "table present." Prospective only: an
archived plan is never retro-fitted. See `doctrine/dual-review.md` >
"Review expectations — the clean-pass trap". -->

## Verification

The concrete commands the implementation must pass.

<!-- cairn:slot verification-commands -->
The standing gates Cairn runs before a change lands (the same ones CI
enforces):

* **Engine suite** — `python -m pytest bootstrap/tests` (the whole
  suite; scope to `bootstrap/tests/test_<surface>.py` while iterating,
  but the full suite gates the cut).
* **Prose integrity** — `python scripts/check_cairn.py` (internal link
  / anchor resolution + claim-path check over the Markdown tree).
* **Quality gate** — `python scripts/quality_gate.py` (order-
  independence + vendor-neutrality + redundancy; `--sub neutrality`
  alone for a doctrine / template wording change).
* **Write-time claim check** — `python scripts/claim_check.py <file>` over
  each proposal / plan / doc the change authored. **One file per
  invocation** — the checker takes a single path and exits 2 (usage) on
  more, so loop rather than passing a list.

Plan-specific gates (a security-lint budget, a doc-drift gate, the
model-selection mapping check `python scripts/check_model_selection.py`)
are added per plan when the change touches that surface.
<!-- cairn:end verification-commands -->

**Note on doc gates**: drift gates (broken references, stale renders,
snippets that diverged from their source) catch **drift**, not
**absence** of new doc updates. Confirm each doc named in Acceptance
was actually updated; the gates don't enforce that.

## Plan review

*Optional; pre-implementation.* See `doctrine/plans.md` > "Plan review"
for the full doctrine: when to use it, reviewer identity, format,
sharpening, multi-round review, and the distinction from
discovery-driven plan revision.

## Code review

*Filled in after implementation commits land.* See `doctrine/plans.md` >
"Code review" for the full doctrine: falsification ledger, coverage
line, reviewer identity (not the implementing agent), and the
append-only rule.

Begin with `**Model**: <model or tier when known; "unknown" if not. Do not
copy-paste old model labels from past templates or archives; query and
state your actual running model identity.>` immediately below the
section header (or below a `### Code review -- <reviewer> -- YYYY-MM-DD`
sub-heading if used).

## Lasting-truth migration

*Filled in at archive time.* See `doctrine/plans.md` > "Lasting-truth
migration doctrine" for the full rule: the disposition vocabulary, the
`Dispositions:` commit-body form, the evidence ledger, and the
loop-fidelity sign-off.

See also `doctrine/lifecycle.md` > "Loop-fidelity verification" for
the Decision→implementation fidelity sign-off checkpoint.

Per the [Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up carries a recorded
disposition — `accept`, `guard`, `wontfix`, or (with the Maintainer's
quoted authorization) `defer`. Only `defer` needs a durable home
outside the plan; the other dispositions *are* the home.

This section is append-only once written.
