<!-- cairn-internal-ref-allow: doctrine/dual-review.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- Author tip: if your plan cites count claims (numbers
     adjacent to `lines` / `proposals` / `plans` / `tests` /
     `commits` / `files` -- common in chunk tables like
     "ships in 2-3 commits"), claim_check will soft-flag them.
     Four clearance paths -- see "Count claims" section below for
     details:
       1. Rephrase to a delta
       2. Cite the command that computed the count
       3. Add an inline `<!-- claim-check-allow-count: N noun -->`
          directive next to the claim (the common case for plans)
       4. Consciously accept in the implementing commit body
     -->

# Plan template

> **This is the plan template.** A non-trivial accepted proposal
> opens a plan: copy the section template below the rule into
> `dev/plans/<short-slug>.md`. The doctrine above the rule is
> reference.

## The plan lifecycle

```
open -> [awaiting-plan-review] -> executing -> review -> archived
```

* **open** — the plan-open commit creates the plan and archives
  the source proposal.
* **awaiting-plan-review** — *(only for a review-required plan; see the
  plan-review precondition below)* the plan is open but implementation has
  not started, waiting for its plan-review section to land. A plan marked
  `Plan review: not required` skips this status and goes straight to
  `executing`.
* **executing** — implementation commits land.
* **review** — a code-review pass examines the implementation.
* **archived** — after review, lasting truth migrates to durable
  homes and the plan moves to `dev/plans/archive/`.

A plan is an *execution* artifact: its status, progress markers,
and commit hashes are updated in place. Review findings and the
archive record are append-only. *(One bounded exception to those
append-only sections: inserting a `claim_check` marker line —
`Proposed/Untracked/External-repo paths:` — adjacent to a path token is
**mechanical maintenance, not authoring a review** (additive-only, its own
labeled `claim-marker maintenance:` commit, typo-guarded). A task-checkbox
/ status update is ordinary mutable workflow, not this carve-out. See the
[Mutability rule](#mutability-rule) below and the lifecycle doctrine.)*

**The plan is the Stage 2 of the Registered Report.** Where the
proposal pre-registered the design and the verification plan
(Stage 1; see `../proposals/_template.md`), the plan and its code
review check the implementation and the evidence it produced
against that locked plan. This is the defense against metric
p-hacking the proposal's Stage 1 named: judged against a prior
commitment, not chosen after the fact.

A non-trivial accepted proposal typically spans **5-10 commits**
across the full lifecycle (`accepted` Decision, plan-open,
implementation commits, code-review, sharpening, plan-archive); the
**minimum is 4** (plan-open + first implementation combine, and code
review records inline with the sharpening commit). Trivial accepts
collapse implementation + proposal-archive into a single commit —
they have no plan, so the plan preconditions do not apply.

<!-- claim-check-allow-count: 5 commits, 10 commits, 4 commits -->

### Release-gated plans (an expected parked state)

A plan may be explicitly **release-gated** — a phase that cannot fire
until a release boundary has elapsed (e.g. a removal step that waits
on a deprecation clock). Such a plan may remain `executing` in
`dev/plans/` **indefinitely**, parked between its pre-release and
post-release phases. This is the plan's *designed* lifecycle state —
not clutter, not a hygiene problem; do not "clear" it.

## The plan-archive precondition

**A plan never archives until a code review has occurred.** This is
the bright-line rule that makes the review system work end-to-end on
the implementation side — parallel to the proposal-review pass that
makes it work on the deliberation side. Without this rule, fast
implementations escape independent review because the archive commit
closes the loop before any independent eye sees the code.

Concretely, an accepted non-trivial proposal flows through:

```
plan-open (+ optional first implementation)   <- can be ONE commit
implementation (one or more commits)
code-review pass (findings appended in plan; sharpening fixes if needed)
plan-archive (lasting-truth migration; this is what closes the loop)
```

The plan-open and first-implementation commits MAY combine when the
work is tractable in one commit — but only for a plan marked
`Plan review: not required` (see the plan-review precondition below).
The **plan-archive commit, however, is always distinct** from the
implementing commit(s); it is the artifact of "review happened and
the loop is closed." Bundling plan-archive into the implementing
commit hides whether code review actually occurred.

Code review's reviewer is **not the implementing agent**. Trivial
accepts skip the plan entirely (per the triage rule below) and
therefore do not encounter this precondition.

## The plan-review precondition

Symmetric to the plan-archive precondition, at the *entry* boundary:
**a review-required plan does not start implementation until its
plan-review section has landed.** The plan-archive gate guards
*review-before-close*; this gate guards *review-before-implement*.

The gate is **explicit, not remembered**: the `**Plan review**` metadata
line above is mandatory — `required(<tier>)` or `not required(<rationale>)`,
with **no silent default**. The author states it; the Maintainer ratifies.
When `required`, the plan opens in **`awaiting-plan-review`** and reaches
`executing` only after a dated `## Plan review` section lands: the review
**and**, when it raised findings, a dated `### Sharpening` subsection
dispositioning them. Its plan-open and first-implementation commits stay
**distinct** (implementation cannot front-run the review). When
`not required`, the rationale is on the record and the plan may combine
plan-open with first implementation.

```
open --> awaiting-plan-review --> executing --> review --> archived   (review required)
open ------------------------->   executing --> review --> archived   (review not required)
```

Like the plan-archive precondition, this converts a *remembered* norm
into a *structural* one: the gate is a status the plan **carries**, not
an agent's memory (the recurring plan-review-skip failure mode). The
plan header's `Plan review:` line makes the gate legible to a cold
reader; a static plan-review lint is the mechanical backstop (a
`required` plan past `open` must carry a dated review subsection). The
review *tier* follows the structural-independence framing in
`dual-review.md`. See the lifecycle doctrine for the full statement.

## Plan triage rule

**Open a plan when an accepted proposal's implementation:**

* Will land across multiple commits.
* Touches multiple files / areas (code + tests + docs).
* Has multi-stage sequencing (e.g., infrastructure first, then
  per-target rollouts).
* Carries deferred follow-ups that need durable homes before
  archiving.

**Skip the plan when:**

* The implementation is a single commit.
* The change is single-file or single-area.
* No follow-ups need a durable home (the proposal's "what's next" is
  fully captured in the implementing commit message).

When in doubt, open the plan. The cost is low (one file in
`dev/plans/`); the benefit is durable execution context for any agent
who picks up the work mid-flight.

### Fast multi-stage (a sub-pattern of non-trivial)

The triage bullets above are OR-conditions: a plan is warranted when
ANY of the four hold. The common sub-pattern where the first bullet
is FALSE (the implementation itself fits in one commit) but at least
one of the others holds (touches multiple files / areas, has
multi-stage sequencing, or carries deferred follow-ups) is called
**fast multi-stage**.

Fast multi-stage compresses the implementation phase into a single
commit but does **not** collapse the lifecycle. Plan-open + first
implementation may combine in one commit (per the
[plan-archive precondition](#the-plan-archive-precondition) above);
plan-archive remains distinct. The minimum lifecycle is **three
commits past the implementing combined commit**:

```
commit N:    plan-open + implementation       (status: review)
commit N+1:  code review + sharpening
commit N+2:  plan-archive + lasting truth
```

Ordinary multi-commit plans are not fast multi-stage, but they use
the same review-before-archive guardrail.

## Mutability rule

Plans are **execution artifacts**, not deliberation artifacts; they
need ordinary status tracking as work proceeds without the
bright-line append-only contract that proposals carry. Two classes
of edit:

**Mutable in place** (status updates as work proceeds):

* `Status` field (`open` / `executing` / `review` / `archived`) plus
  the "last update" date.
* Checkboxes / progress indicators in the Sequence section.
* Commit hashes filled in as commits land.
* Verification notes (test counts, runtime, tooling output).
* Link targets when referenced files move.
* **Chunk-table cell text — pre-implementation only** (plan status
  `open`; no commits in flight against the chunks being edited).
  Inline edits driven by accepted plan-review findings land here,
  with the Sharpening subsection (see [Plan review](#plan-review))
  naming which cells changed and why. Once status flips to
  `executing`, chunk-table edits follow the append-only rule below.

**Append-only** (history of decisions):

* Scope changes (add a new sub-section if scope materially shifts;
  don't rewrite the original Scope paragraph).
* Material sequence changes (add a "Sequence revision" note; don't
  edit prior Sequence entries that are already in flight).
* Review findings — both `## Plan review` and `## Code review`
  sections are append-only once a reviewer has added findings;
  Sharpening subsections under either are also append-only. Mirrors
  the proposal Review section's append-only contract.
* Archive decisions (Lasting-truth migration entries are append-only
  once written).

**Distinct from discovery-driven inline revisions.** When the
implementing agent (or the plan author) revises the plan mid-flight
in response to *implementation discovery* — not in response to a
review pass — inline chunk-table edits are also permitted while
status is `open`, but no `## Plan review` section is required. The
audit trail lives in the revision commit's message + the git diff.
Add a `## Plan review` section only when an actual review pass
occurred.

Once the plan archives to `dev/plans/archive/`, the file is
**closed** — only link maintenance permitted (parallel rule to
archived proposals).

## The planning handshake

Before heavy implementation, the team converges on a short set of
questions — a lightweight handshake for plan-shaped work below the
full-proposal bar (a proposal answers these at greater depth; a plan
draining an accepted proposal inherits most of them):

* What workflow or capability are we improving?
* What is the current pain or risk?
* What contract or module boundary is involved?
* What would success look like?
* What tests, docs, or examples prove the change?
* **What must explicitly *not* change in this pass** — the scope fence?

The `## Scope` section below is where these land: it names what the
plan executes *and* what it deliberately leaves alone. The scope fence
is the load-bearing one — an unstated "not this pass" is how a bounded
plan quietly grows.

## Forward-reference paths — `Proposed paths:` marker doctrine

A plan typically cites paths it *plans to create* during chunk
execution (new modules, new test files, new docs). At plan-open time
those paths do not resolve, so `claim_check` hard-flags them. The
escape hatch is `claim_check`'s marker-line mechanism: a line that
begins with `Proposed paths:` (case-insensitive; optional list-item
prefix) exempts the backticked path tokens **on that same line** from
the hard path check.

Use the marker when:

* The plan opens with paths it plans to create at chunk commits.
* The plan cites future test files, fixture files, or documentation
  files in chunk tables.
* The plan moves a file — the future archive path is forward-reference
  until the move happens.

Marker shape (preferred): one or more `Proposed paths:` lines near the
top of the plan (after `## Plan triage rule`, before `## Scope`), each
listing a batch of related tokens. Multiple tokens per line are fine;
a marker line also exempts any **contiguous structured block
immediately beneath it** (table rows, list rows, or bare backticked
path-list rows) until the next blank line, heading, or ordinary prose
line.

Example:

```
Proposed paths: `path/to/new_tool.py`, `path/to/new_dir/`,
`path/to/new_doc.md`.

Proposed paths: `path/to/tests/test_new_thing.py`,
`path/to/tests/test_new_contract.py`.
```

**The marker is line- and block-scoped**: it does NOT exempt a path
where the same token recurs in ordinary prose (a chunk description, an
acceptance-criterion sentence). Such an occurrence still hard-flags.
Two clean ways to handle it, in preference order:

* **Cite the existing parent directory + the bare new filename.**
  `claim_check` treats a backticked token as a repo-path claim only
  when its first segment is a real top-level directory; a bare
  filename (no `/`) is not a claim. Write a new file as a bare name
  beside its directory — e.g. `new_tool.py` next to the existing
  `path/to/dir/` — so the directory token resolves, the bare name is
  ignored, and the full slashed path stays declared once in the
  marker. No flag, no residue.
* **Conscious-accept**, documented in the plan-open commit body — the
  fallback when the full slashed path must appear in prose; it clears
  at the implementing chunk commit where the path is created.

**Two other marker keywords** parallel `Proposed paths:`:

* `Untracked paths:` — for git-ignored paths a fresh checkout will not
  carry.
* `External-repo paths:` — for paths that resolve in a sibling
  repository this project depends on, or an upstream framework
  checkout, rather than in this tree.

All three markers exempt only the tokens on the marker line itself;
count claims still soft-flag. See `claim_check`'s module docstring
(the "Marker lines" subsection) for the full mechanism documentation.

**Applies to a plan's append-only finding sections too.** Under the
`AGENTS.md` claim-marker-maintenance exception, inserting a marker line
to clear a forward-reference / sibling-repo path flag is permitted even
inside an append-only `## Plan review` / `## Code review` section (and a
reviewer's findings) — additive marker line only, in its own
`claim-marker maintenance:` commit, with no change to the finding's
text. A plan's **task checkboxes / status** are ordinary mutable
workflow, distinct from these append-only finding sections. Before
marking, confirm the flagged path is not a typo of a real local path.
**Placement safety**: an inline marker is *block-scoped* (it exempts
contiguous rows beneath it until a blank line / heading) — place it
immediately adjacent to the target token and leave a blank line after
the target row so it does not over-exempt later rows; for many
sibling-repo paths, prefer the file-level
`<!-- claim-check-allow: <glob> -->` directive (narrow globs only).

## Count claims -- soft-flag clearance

`claim_check` soft-flags any **count claim** -- a number directly
adjacent to one of six tree-nouns: `lines`, `proposals`, `plans`,
`tests`, `commits`, `files`.  Example soft-flag triggers:

* "5-10 files at scale" (forward-looking range estimate)
* "281 tests" (live-computed from `pytest --collect-only`)
* "Plan ships across approximately 7 commits" (plan-shape estimate)
* "12,847 nodes" (-- **not** a tree-noun, doesn't flag)

<!-- claim-check-allow-count: 10 files, 281 tests, 7 commits -->
<!-- ^ This template's own teaching examples are self-exempted
     here.  The inline directive form is mechanism (3) below;
     this section thus demonstrates its own recommended pattern. -->

The flag's job is to catch **memory-quoted absolute counts** that
should be deltas or live-computed; the scanner can't tell legitimate
counts from misremembered ones.  Four clearance mechanisms exist;
pick one per claim:

1. **Rephrase to a delta** -- "+5 files vs current N" rather than
   an absolute number.  Best when the claim is structurally a
   change-size.
2. **Cite the command that computed the count** -- "281 tests (per
   `pytest --collect-only`)."  Best for live-from-probe claims; the
   adjacent command names the cheap defense the reader can re-run.
3. **Inline `<!-- claim-check-allow-count: N noun, ... -->`
   directive** -- exempts specific count tokens on adjacent prose.
   Best for forward-looking range estimates ("plan ships across
   ~7 commits") where rephrasing would lose information.  **Reserved
   for prescriptive rules (e.g., doctrine wording like "5-10 commits")
   or historical quotes; never for live / mutable counts where
   mechanisms (1) delta or (2) cited command would be cleaner.**
   Multiple nouns per line; multiple directives per document.
   Example:

       The plan will ship across approximately 7 commits.

       <!-- claim-check-allow-count: 7 commits -->

4. **Consciously accept in the implementing commit body** -- name
   the count, name why the soft flag is acceptable (forward-looking
   estimate, live-probe, etc.), and the commit body becomes the
   audit trail.  Use sparingly -- (3) is usually cleaner; (4) is
   the fallback when inline-exempt would clutter the prose.

**Plan-specific note**: chunk tables (`Chunk A -- <name>`) commonly
cite per-chunk commit counts ("ships in 2-3 commits").  These are
forward-looking range estimates -- option (3) is the natural
clearance mechanism.

**Avoid the discipline antipattern**: do **not** rephrase by
substituting non-tree-nouns purely to avoid the flag (e.g., "five
test cases" instead of "5 tests").  The discipline targets quoted
absolute counts; substituting nouns hides the count rather than
grounding it.

<!-- claim-check-allow-count: 5 files, 3 commits, 5 tests -->
<!-- ^ The "+5 files" delta-example in mechanism (1), the "2-3
     commits" plan-specific-note example, and the "5 tests"
     antipattern example are self-exempted here. -->

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
they don't drift back into this pass by accident. See "The planning
handshake" above for the convergence questions this section answers.

### Documentation / doctrine surface

What documentation, doctrine, or contract surface does this plan
touch? If none, say so explicitly — silent omission is a code-review
finding (the plan must name what doc state is mutated, not surface
it at review time).

<!-- cairn:slot documentation-tier-home -->
(Filled from the `documentation-plan` default-on module when installed
— paste content from `dev/modules/documentation-plan.md` > "Merged
into" > Block 3: dev/plans/_template.md. The merged content names
the per-layer routing rule for doc + doctrine changes, pointing at
`docs/DOCUMENTATION_PLAN.md`. If documentation-plan is not installed,
replace with `N/A: documentation-plan not installed`. An unfilled
slot is a review finding.)
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
  (Adopter-specific doc-generation tooling — the exact schema source +
  render command, the snippet-sync command, the CLI / notebook smoke
  surfaces the project uses. Fill with the project's commands, or
  replace with `N/A: no generated or snippet-synced docs`.)
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
(Adopter-specific verification commands — the test-runner invocation +
expected scope, the doc-link / schema-render / snippet-drift gates, the
security-lint budget, and any plan-specific gate. Fill with the
project's commands, or replace with `N/A`.)
<!-- cairn:end verification-commands -->

**Note on doc gates**: drift gates (broken references, stale renders,
snippets that diverged from their source) catch **drift**, not
**absence** of new doc updates. Confirm each doc named in Acceptance
was actually updated; the gates don't enforce that.

## Plan review

*Optional; pre-implementation.* An Internal review pass on the plan
itself, before implementation commits land. Mirrors the proposal
Review/Response cycle but adapted to the plan's execution-artifact
nature: **findings are append-only; chunk-table cell edits that
accepted findings motivate are inline, with a documenting Sharpening
subsection.** See the [Mutability rule](#mutability-rule) for the full
inline-vs-append split.

### When to use it

* **Maintainer-requested** ("I'd like a review or two before this moves
  forward").
* **Plan revised mid-flight** — when a discovery-driven revision
  materially expands scope or adds chunks, an Internal review pass on
  the revised plan is worth running before chunks land.
* **Scope is large or load-bearing** — many chunks, multiple modules,
  scientific / architectural risk that the proposal review didn't fully
  resolve.
* **Plan author wants a second eye** — always defensible; the cost is
  low and the failure mode it prevents (implementing against a flawed
  spec) is expensive.

Skip plan review when the plan is small, derived directly from a
proposal that itself went through Internal review, and the implementing
chunks are straightforward. Trivial accepts that skip the plan entirely
(per the [Plan triage rule](#plan-triage-rule)) also skip plan review.

### Reviewer identity

**Internal-review floor** — same-agent-fresh-session is sufficient. The
plan is a deliberation artifact (parallel to the proposal Review
section's tier), not implementing code. The stricter cross-agent-type
floor in [Code review](#code-review) below applies to *implementation*
review, not here.

Escalate to the External-review tier (different agent type or human)
when the plan carries scientific or architectural risk not fully
resolved during proposal review.

### Format

Each review pass gets its own dated subsection:

```
### Plan review -- <reviewer> -- YYYY-MM-DD

**Model**: <model or tier when known; "unknown" if not>

<one-paragraph orientation: who asked, what triggered the pass>

**Structural-independence stance.**  Author / revision-author /
reviewer identities; tier choice (Internal-review floor
sufficient because <reason>).

**Verification done before drafting:**

* <bullet -- file:line reads, empirical reproducers, grep counts>
* <bullet>

**Steelman:**

* <bullet -- what the plan got right; what should not be
  contested unless the reviewer can show otherwise>
* <bullet>

**Findings:**

* **[N1] (LOAD-BEARING) -- <one-line title>.**  <body with
  file:line citations + empirical evidence where applicable>
  - **(a)** <alternative one>
  - **(b)** <alternative two>
  **Lean: (a)**.  <rationale>
* **[N2] (important) -- <title>.**  <body>
* **[N3] (nit) -- <title>.**  <body>

**Suggested sharpening before implementation:**

1. <action>
2. <action>

**Coverage + second-round recommendation** (see `doctrine/dual-review.md` >
"Recommend-and-decide"):

* **Covered** -- <review-sweep lenses swept, each with a falsifiable citation>
* **Not covered / low confidence** -- <the negative space>

Recommendation: <recommended / not recommended a second cross-type pass, with
reasons grounded in the negative space>. (A declared-`required` tier runs
regardless.)
```

Priority labels:

* `(LOAD-BEARING)` — plan-as-written will not achieve its acceptance
  criteria; blocker for implementation.
* `(important)` — design / scope concern; deserves resolution but not
  strictly a blocker.
* `(nit)` — clarity / polish; defer-OK.

### Sharpening (response to findings)

When findings are addressed, append a Sharpening subsection under the
same `## Plan review` heading:

```
### Sharpening -- <author> -- YYYY-MM-DD

Dispositions on the review's findings, per maintainer
directive ("<quoted directive>"):

* **[N1] accept (rewrote chunk 1.1 in place)** -- <what changed
  inline; what guidance the new cell text gives>
* **[N2] accept (added chunk 1.7)** -- <what was added>
* **[N3] defer (will land at archive time)** -- <why>
* **[N4] wontfix** -- <rationale>

Verification post-sharpening:

* <doc-link gate> -- clean.
* Plan re-reads coherently end-to-end.
```

**Chunk-table cells are edited inline** when sharpening accepts a
finding; the Sharpening subsection NAMES which cells changed and why.
This combines audit-trail integrity (append-only Sharpening doc) with
execution-spec correctness (the implementer reads the corrected chunk,
not the obsolete one). Permitted only while plan status is `open`;
once status flips to `executing`, follow the append-only
Sequence-revision rule (see [Mutability rule](#mutability-rule)).

### Multi-round review

Each subsequent review pass gets its own dated subsection with a round
suffix:

```
### Plan review -- <reviewer> -- YYYY-MM-DD (round 2)
...
### Sharpening -- <author> -- YYYY-MM-DD (round 2)
...
```

Finding numbering restarts per round (`N1`, `N2`, ... in each round);
cross-round disposition citations reference the round explicitly
(`N1.r2 accept`).

### Distinct from discovery-driven plan revision

Inline plan revisions driven by *implementation discovery* — e.g., the
implementing agent realizes the original plan's chunk shape was
incomplete — do NOT require a `## Plan review` section. No review
happened; the audit trail lives in the revision commit's message + the
git diff. Use this section only when an actual Internal review pass
occurred.

## Code review

*Filled in after implementation commits land.* Begin with
`**Model**: <model or tier when known; "unknown" if not. Do not copy-paste old model labels from past templates or archives; query and state your actual running model identity.>`
immediately below the section header (or below a `### Code review --
<reviewer> -- YYYY-MM-DD` sub-heading if used). The reviewer is
typically NOT the implementing agent (Internal Reviewer or External
Reviewer norms apply, same as the proposal Review section). Findings as
a numbered list with `accept (commit <sha>)` / `defer` / `wontfix`
dispositions. Sharpening fixes land as follow-up commits before the
plan archives.

**A clean code review carries a falsification ledger.** Per
`dev/agent_collaboration.md` > "Review Expectations", a **final
pre-archive** code review with **no P1/P2 findings** clears the
plan-archive precondition only with a falsification ledger **or** a
confirming second different-agent-type pass. Minimal ledger shape:

* **Surfaces probed** — what was actively examined / tried-to-break.
* **Negative / edge-case attempt** — at least one, when applicable.
* **Verification** — the checks run (or consciously not run, with why).
* **Residual risk** — what remains unverified.

**End with the coverage line + recommendation** (`doctrine/dual-review.md` >
"Recommend-and-decide"): **Covered** (the review-sweep lenses swept, with
citations) / **Not covered / low confidence** (the negative space), then a
recommendation on whether a further independent pass is warranted. For a clean
final pre-archive review this composes with the falsification ledger above —
the ledger *is* the "Covered" evidence, and the negative space is what a
second pass would target.

**Reviewer identity** (per the structural-independence tier rule, see
`dev/collaboration_agreement.md` > "External Review Norms" and
`dev/agent_collaboration.md` > "Stage-to-role matrix"): the "not the
implementing agent" default is the FLOOR for code review — stricter
than the Internal-review tier's same-agent-fresh-session allowance.
Rationale: proposal review surfaces intellectual flaws in ideas; code
review surfaces implementation regression risk where the implementer's
just-written code is harder to spot mistakes in cold by someone with
the same underlying reasoning patterns. Escalate to the External-review
tier (different agent type or human) when the implementation carries
scientific or architectural risk not fully resolved during proposal
review.

This section is append-only once a reviewer has added findings.

## Lasting-truth migration

*Filled in at archive time.* Per the
[Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home
outside the plan. Acceptable homes:

* `dev/PLANNING.md` — a tier item, a follow-up backlog, or a new
  dedicated subsection.
* A topic doc's "Future work" section.
* `CHANGELOG.md > Unreleased` — the user-visible release-facing
  summary.
* Its own queued follow-up proposal at
  `dev/proposals/<date>-<author>-<short-title>.md`.

`dev/NEXT_SESSION.md` is not an archive-time home — it is edited only
at the goodnight routine and on explicit user instruction. A small,
pickable-cold follow-up goes to `dev/PLANNING.md` here; the goodnight
scrub then surfaces it into `NEXT_SESSION.md`.

The archive commit body must name where each item went, in the form:

```
Follow-ups migrated to:
* <item> -> dev/PLANNING.md > <section>
* <item> -> CHANGELOG.md > Unreleased > Added
* <item> -> docs/<topic>.md > Future work
```

This makes the migration auditable from `git log` alone.

The archive-time migration note must also include an **evidence
ledger**:

* **Evidence shipped** — tests, docs, examples, or workflow checks that
  actually landed in the implementation / sharpening commits.
* **Evidence deferred** — planned checks or workflow smokes that did
  not land in this plan.
* **Deferred evidence home** — where each deferred item is now tracked
  (`dev/PLANNING.md`, a topic doc's "Future work" section, or a queued
  follow-up proposal).

This prevents the archive commit from accidentally turning "deferred"
evidence into "shipped" evidence by implication.

This section is append-only once written.
