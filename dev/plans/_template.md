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
with no follow-up needing a `defer` home (a follow-up headed for
`accept`, `guard` or `wontfix` does not by itself require a plan).

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

**The fence bounds this pass; it does not bound the accepted proposal.**
Accepted scope is a **floor** — a plan that drains less than the proposal
it executes has deviated from approved scope, not chosen a tidy fence,
and no reviewer can create that authority by calling the remainder "out
of scope". If this fence leaves an accepted outcome undelivered, say so
here and get the Maintainer's explicit disposition; see the `Scope delta`
prompt in the plan-review section below.

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
criteria, to the test that exercises it through its public path. A
security-touching plan re-answers the five security-preflight questions only
where its chunking changes an answer — most often S2 (which chunk runs the
mutation) and S3 (which gate command fires the check). Cite tests as
relative markdown links so the link checker verifies they exist. Include a
known-omissions line. Reviewed as evidence — the reviewer challenges a row
or names the one they sampled, never "table present." Prospective only: an
archived plan is never retro-fitted. See `doctrine/dual-review.md` > "Review
expectations — the clean-pass trap". -->

## Verification

The concrete commands the implementation must pass.

<!-- cairn:slot verification-commands -->
Before implementation, make Boundary A a **reviewed mapping**: for each changed
invariant and public path, name the exact affected test node/file and every
standing non-pytest gate for the touched surface. Run that scope while
iterating. There is no permanent fast tier; if a substantive code surface has
no reviewed mapping or cannot be bounded confidently, run the full suite.

After the final implementation commit, Boundary B runs once against a clean,
unchanged commit under the canonical interpreter. The default is the **full
suite**; a plan whose reviewed mapping **bounds the change's effects
confidently** may instead run that mapping plus every standing gate for every
touched surface. Bounded mode **refuses** — run full — when the change touches a
**contract surface** (install contract, fidelity or gate manifest, lockfile
schema, published `scaffold.py --manifest`) or a **trust-ceremony surface**
(any high-risk surface `AGENTS.md` names, or release/security ceremony work).
**Uncertainty resolves to `full`.** The commands:

* **Engine + seed-0 order coverage** — `python -m pytest bootstrap/tests
  --quality-gate-shuffle-seed=0`.
* **Static quality legs** — `python scripts/quality_gate.py --sub neutrality
  --sub redundancy` (does not dispatch pytest again).
* **Prose integrity** — `python scripts/check_cairn.py`.
* **Write-time claim check** — `python scripts/claim_check.py <file>` once for
  each authored proposal, plan, or doc.
* **Plan-specific acceptance commands** — the mapped tests, security budgets,
  doc-drift gates, public-path smokes, and other commands named above.

Only after that stable run, append a dated section named
`Implementation verification -- <agent> -- YYYY-MM-DD` at H2. Do not place an
empty heading in a new plan. The record uses these exact fields:

* **Boundary B mode** — `full` | `bounded`. On `bounded`, also name the touched
  surfaces, the reviewed mapping and standing gates run, why the effects are
  bounded, and the explicit absence of any contract or trust-ceremony surface.
* **Tested commit** — full SHA.
* **Reviewed range** — base and tested endpoint.
* **Interpreter/runtime** — canonical path and version.
* **Pre-run state** and **Post-run state** — clean tree and identical tested
  `HEAD`.
* A command table with **Command**, **Exit**, **Outcomes**, and **Elapsed**
  columns, including pass/fail/skip/xfail/xpass counts where applicable.
* **Non-pass disposition**, **Plan-specific acceptance commands**, and
  **Known omissions**.
<!-- cairn:end verification-commands -->

**Note on doc gates**: drift gates (broken references, stale renders,
snippets that diverged from their source) catch **drift**, not
**absence** of new doc updates. Confirm each doc named in Acceptance
was actually updated; the gates don't enforce that.

**Inherited plan readiness -- the two-field declaration.** When the source
proposal's **External** review recorded `Plan readiness: READY`, this plan takes
a fresh-context **Internal** plan review instead of a second
different-agent-type round, and it says so in *two* header fields, not one:

    **Plan review**: required(Internal)
    **Inherited proposal basis**: review=<full External-review commit>;
                                    proposal=<full accepted commit>

`proposal=` is the proposal commit the Decision binds -- the same commit the
readiness review recorded as its `Reviewed commit`. Both ids are full 40-character
lowercase hex; an abbreviation can collide, and a colliding binding names two
commits. Omit the field entirely when this plan does not inherit: a partial or
misspelled declaration **refuses** and never reads as `READY`.

**Inheritance reallocates the plan review; it never removes it.** Pairing an
inherited basis with `not required(...)` would leave the plan no independent read
at all, and refuses.

**Seven things invalidate it, in both directions.** A new scope item, invariant,
public path, failure disposition, trust boundary or ceremony -- declared as

    **Contract expansion**: none | <dimension>[; <dimension>]

-- and, equally, a **scope reduction** relative to the accepted proposal, declared
through the `Scope delta` prompt below. Either one means this plan takes
`required(<tier>)` and a distinct plan review before implementation continues; a
reduction is admitted only by the Maintainer's recorded allowance. Both are
**author declarations**: the checker binds the record, and whether the translation
is faithful stays the reviewer's judgement.

**The four-field review basis is mandatory in every plan-review pass.** Its
first four lines name the bounded target that pass actually read:

    Reviewed commit: <full commit id>
    Target: <the operative plan sections this pass reviewed>
    Prior findings: <ids being closed, or none>
    Assurance path: <standard | high-assurance>

They sit above the pass's first `###` heading -- a field parked below an H3 does
not count -- and the emphasis is optional, because the field name is the
contract. `Assurance path` restates the source proposal's declaration rather
than re-deciding it. The basis is a default navigation target, not permission to
ignore relevant history: a reviewer reads any earlier section a current claim
depends on, and a correctness, security, scientific-validity, or scope defect is
blocking whenever it is found.

<!-- Each review pass is its own dated H2 section, appended below this
     comment as:

       ## Plan review -- <reviewer> -- YYYY-MM-DD

       Reviewed commit: <full commit id>
       Target: <the operative plan sections this pass reviewed>
       Prior findings: <ids being closed, or none>
       Assurance path: <standard | high-assurance>
       **Tier**: <Internal|External>
       **Findings**: <none|raised>

     with its `### Sharpening` at H3 inside the pass body. There is no
     `## Plan review` container heading: an empty container reads as a
     landed review, and a review is what the `**Plan review**:` metadata
     line makes *mandatory* -- `doctrine/plans.md` requires that line with
     "no silent default", so this section is not optional. Whether a *pass*
     is required is what `required(<tier>)` vs `none` on that line decides.
     See `doctrine/plans.md` > "Plan review" for reviewer identity, format,
     sharpening, multi-round review, and the distinction from
     discovery-driven plan revision.

     SCOPE DELTA -- accepted scope is a FLOOR, and the Sharpening is where
     that most often bites, because a reviewer's narrowing recommendation and
     the author's acceptance of it land in the same section.  Sequencing is
     free: moving work between chunks, re-ordering them, or splitting one
     across commits changes no outcome and owes nothing.  REMOVING an accepted
     outcome is a deviation from approved scope under `AGENTS.md`, not a scope
     fence the plan may draw for itself -- and a plan reviewer cannot create
     that authority by calling the remainder "out of scope".

     So when a Sharpening disposition narrows what this plan will deliver,
     judge it against the scope AS ACCEPTED and declare the result inside the
     Sharpening:

       **Scope delta**: preserved | degraded | lost

       **Removed scope**
       * <unit> -- source section; reason; revival/closure condition.

       **Disposition/home**: <where the grouped remainder lives>

     State `preserved` if you want the record to show you checked; only
     `degraded` and `lost` require the block above -- a lighter mechanism that still delivers is what
     restraint asks for, and a declaration on every revision would be ritual
     within a month.  `degraded` and `lost` both additionally need the
     Maintainer's explicit disposition under the deviation gate; partial
     changes what residual is recorded, never who may concede it.  Full rule:
     `doctrine/dual-review.md` > "Review expectations -- the scope-reduction
     trap". -->

## Code review

*Filled in after implementation commits land.* See `doctrine/plans.md` >
"Code review" for the full doctrine: falsification ledger, coverage
line, reviewer identity (not the implementing agent), and the
append-only rule.

Each pass is its own dated H2 section, `## Code review -- <reviewer> --
YYYY-MM-DD[ (round N)]`, and opens with the mandatory review basis on its own
lines above the pass's first `###` heading:

    Reviewed commit: <full commit id>
    Target: <the code range this pass reviewed>
    Prior findings: <ids being closed, or none>
    Assurance path: <standard | high-assurance>

Then the reviewer identity line, the verdict, and the findings declaration. A
field parked below an H3 does not count toward the basis.

Before reusing Boundary B, verify its Tested commit, Reviewed range, path
validity, pre/post clean state, command results, and non-pass disposition.
Then run an independent targeted falsification ledger; copying Boundary B's
broad command is not independent review. Require a fresh full-suite run when:

1. no valid Boundary B record exists;
2. review discovers an unrecorded cross-surface dependency;
3. a skip, xfail, or xpass lacks an adequate disposition;
4. review sharpening changes implementation, tests, executable templates, or
   fixtures in the reviewed range;
5. the accepted plan governs a trust ceremony that explicitly requires
   independent full execution; or
6. the reviewer has a concrete reason to distrust or falsify the broad result.

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

**The archive gate now checks substance, not the label.** An attestation is
required **every time**: either at least one entry naming `accept`, `guard`,
`wontfix` or `defer`, or the explicit form `Dispositions: none` on its own
line when there are genuinely no follow-ups. This supersedes the earlier rule that
allowed the block to be *omitted* in the zero-follow-up case — omission and an
empty label are now indistinguishable to a reader, and both refuse.

The loop-fidelity sign-off must sit **inside this section** and name at least
one implementing commit id plus the governing accepted/Revised section.
Promising that it is owed does not satisfy it.

See also `doctrine/lifecycle.md` > "Loop-fidelity verification" for
the Decision→implementation fidelity sign-off checkpoint.

Per the [Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up carries a recorded
disposition — `accept`, `guard`, `wontfix`, or (with the Maintainer's
quoted authorization) `defer`. Only `defer` needs a durable home
outside the plan; the other dispositions *are* the home.

This section is append-only once written.
