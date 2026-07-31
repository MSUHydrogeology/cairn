<!-- cairn-internal-ref-allow: doctrine/coordination.md doctrine/lifecycle.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
# Cairn — development roadmap

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
**Released at v0.3.0 (2026-06-12).** Phases 1–4 are complete: doctrine
extraction, the forkable templates, the bootstrap procedure + scaffold +
the engine test suite, and two case studies (modflow_tools — the
reference instance — and LHM). The methodology is in active use in those
two real projects. **Phase 5 — launch and governance — is in progress;**
the R-H third-party correctness probe (plan chunk 5.3) is still
outstanding, awaiting a consenting third-party scientific repository that
did not contribute to the doctrine.

**Cairn now self-hosts (adopted 2026-06-12).** Development was previously
tracked in the modflow_tools repository's `dev/plans/` lifecycle; this
`dev/` tree is Cairn running its own methodology on itself, so future
development — and Issues filed via GitHub — happens here. The accepted
adoption profile is recorded at `dev/.cairn/profile.yml`
(`collaborative-team` preset, human-team overridden to solo; the
deliberation is at `dev/strategy/2026-07-11-claude-cairn-adoption-record.md`,
a 2026-07-11 reconstruction, not contemporaneous).

**Where it is headed.** The immediate next phase is a broad strategy +
roadmap pass: take a wide look at the project, tighten what has
accumulated across phases 1–4, and lay out a forward roadmap. Those
deliberations open as `dev/strategy/` notes and `dev/proposals/`.

*(Refreshed at each goodnight scrub.)*
<!-- cairn:end project-status -->

## Onboarding

Progressive onboarding tasks live here. The bootstrap fills this
section from the chosen profile preset (`solo-greenfield`,
`collaborative-team`, or `high-rigor-legacy`) with the preset's
day-one seed tasks plus a preset-metadata comment that the
goodnight activation helper reads to discover the preset's
deferred tasks (held in `dev/modules/onboarding/`'s installed
preset file until their named trigger fires). The progressive-
onboarding doctrine is the source of the mechanism; this section
is its surface in PLANNING.

<!-- cairn:slot onboarding-tasks -->
<!-- preset: collaborative-team -->

* [seed; id: try-session-start-skill]
  Try the `session-start` skill (`/session-start`): run
  `python tools/lifecycle.py session-start` to orient at the top of a
  session. The lifecycle routines are now invokable skills installed under
  `.agents/skills/`; the canonical doctrine is `doctrine/session-routines.md`.
* [seed; id: read-lifecycle-doctrine]
  Read `doctrine/lifecycle.md` together as a team -- the
  proposal -> review -> decision -> archive shape is the load-
  bearing convention every later coordination behavior assumes.
* [seed; id: read-coordination-doctrine]
  Read `doctrine/coordination.md`. The work-intent mechanism is
  what prevents collision between concurrent agents in the same
  tree; multi-agent teams need this from day one, not as a
  later upgrade.
* [seed; id: install-work-intent-hooks]
  Install the work-intent git hooks, or record that you are skipping
  them. This preset is concurrent, so the scaffold *recommended* the
  hooks at install time but does **not** install them for you (it
  never mutates `.git/hooks`). Run `python tools/intent.py
  install-hook` + `install-precommit`, then `hooks-status` to confirm.
  Without them, `dev/intents.jsonl` stays empty and the coordination
  signal never fires. To opt out (now or later), re-run either command
  with `--uninstall`; note the choice here so the team's preference is
  on the record.
* [seed; id: read-dual-review-module]
  Read `dev/modules/dual-review.md`. The collaborative-team
  preset installs the dual-review module by default; the
  External-tier review now has structural independence from
  the start.
* [seed; id: walk-dev-tour]
  Walk the `dev/`-tree tour at `dev/modules/onboarding/dev-tour.md`
  together. It carries one paragraph per `dev/` subdirectory plus a
  worked example showing one change through the full lifecycle.
* [seed; id: agent-team-onboarding]
  Walk `dev/modules/onboarding/agent-team-onboarding.md` to align on capability
  tiers + the `Co-Authored-By:` trailer convention for each
  agent in the roster. Multi-agent is this preset's defining
  shape; the agent-team-onboarding doc carries the
  baseline configuration the team uses.
* [seed; id: sign-collab-agreement-day-one]
  Convene the team + agents in your first session and fill the
  `team-roster` slot in `dev/collaboration_agreement.md`. The
  roster is what makes Dual-Review's External tier
  structurally meaningful; teams without an explicit roster
  fall back to fresh-session same-vendor review, which the
  collaborative-team profile is sized past.
<!-- cairn:end onboarding-tasks -->

## Queued

The forward-looking board: substantive work that is accepted or
anticipated but not yet in flight. When a queued item grows into
multi-step work, open a plan under `plans/` and replace the entry
with the plan's filename stem.

* **Adopter-entry doc-refresh follow-ups** *(deferred, Jun 2026)* — the
  doc-refresh + prose↔runtime drift-gate shipped (plan
  `adopter-entry-doc-refresh`, archived; from the 2026-06-12
  adopter-friction audit). Two deferred follow-ups: (a) a context-aware
  scaffold **`--quickstart` mode** (richer than the "Next steps for a real
  adoption" reframe — let the scaffold print a trimmed next-step for the
  trivial path); (b) extend the `verify:` count guard to **other
  adopter-facing counts** beyond the quickstart's two. Each → its own
  proposal when revived.
* **Transition-lint** *(queued, accepted 2026-07-22)* — an **advisory**
  check that a commit's message claim is supported by its diff: a subject
  claiming a review / response / decision transition whose diff adds no such
  section, and a proposal-*open* commit whose file already carries reviews.
  Guards the failure that opened the tighten-up (Cairn's own showcase arc
  carried both shapes). Accepted at proposal stem
  `2026-07-22-claude-transition-lint`, which pinned the heuristics this entry's
  earlier deferral was waiting on — an independent reimplementation scored **0
  false positives across 538 commit subjects**, surfacing exactly the 3 real
  incidents. The sibling reader-fix (stem
  `2026-07-22-claude-stage-commit-patterns`) confirmed it is *not* made
  redundant: that reader classifies messages and never opens a diff.
  **Queued, not next** — maintainer-facing apparatus, and the standing priority
  is postdoc-first; it does not displace adopter-path work. Plan conditions
  (rename-awareness, narrowed trigger, carve-in-bounded exceptions, advisory
  exit 0, no silent-clean) are ratified in the Decision. → plan-open when it
  reaches the top.
* **Self-host lockfile reconciliation** *(deferred, Jul 2026)* —
  `python bootstrap/scaffold.py upgrade --target . --cairn-root . --plan`
  currently reports **38** files as "no recoverable base (review-only
  diff)" against the base cache, each needing a by-hand `--stage`/`--apply`
  merge or a reviewed `--finalize` once its actual customization state is
  confirmed. Surfaced (not caused) by the `solo-legacy-adopter-path` plan
  (archived; Part 3 touched one of the 38, `dev/proposals/_template.md`,
  and deliberately left its lockfile hash un-finalized rather than
  hand-patching one file in isolation — see that plan's Lasting-truth
  migration for the full account). No proposal yet; revive by running
  `--plan` fresh, confirming the current file list, and scoping the
  reconciliation pass (likely several small, reviewed `--finalize` batches
  rather than one large `--apply`).

*(Otherwise empty at adoption — native proposals populate this board. The
Cairn roadmap migrated 2026-06-12 from modflow_tools — queued items,
deferred follow-ups, and the release path — lives at the **bottom** of this
file under "Migrated Cairn roadmap (2026-06-12)".)*

## Active

Substantive work currently in flight: open plans, executing
sub-tracks, in-progress proposals between Decision and
plan-open. When an entry completes, it is **removed** from this
section at the next goodnight scrub — the truth migrates to the
archived plan / proposal, the implementing commits, and the
changelog. There is no "completed recently" section on this
board by design.


---

## Status taxonomy

A board item carries one status. These are the inline reference
for any agent editing the board (the full *why* is in
`doctrine/lifecycle.md`):

* `queued` — accepted or anticipated, not yet in flight.
* `active` — in flight: an open plan, an executing sub-track.
* `blocked` — in flight but waiting on an external dependency or a
  Decision; name the blocker so it is actionable cold.
* `deferred` — consciously parked, **with revival conditions** (what
  must become true for it to return to `queued`).
* `completed` — **transient**: held only between finishing the work
  and the next goodnight scrub, then *removed*. The board keeps no
  completion history — a finished item's permanent home is the
  archived proposal / plan, the implementing commits, and the
  changelog.

**Date-marker convention.** Each item — or its parent section —
carries a `(Mon YYYY)` marker recording when it was added or last
reaffirmed (e.g. `(May 2026)`). The marker makes the staleness sweep
(below) performable by **reading the file**, not by `git blame` or
memory. Refresh the marker whenever the item is reaffirmed at a
goodnight scrub.

## Archive preconditions (proposals and plans)

Before a proposal or plan moves to `archive/`, every
**explicitly-deferred follow-up** it carries must have a durable home
*outside* the file — a board item here, a topic doc's "Future work"
section, or its own queued follow-up proposal. Record where each went
in a durable, auditable location the team's workflow preserves (the
archive commit body, the PR description, or the plan's closing
metadata) as a `Follow-ups migrated to: …` block, so the migration is
reconstructible from the durable record alone. See
`doctrine/lifecycle.md` > "Archive precondition — every deferred
follow-up has a durable home".

## Removal preconditions

A `completed` item is **removed**, not crossed off — but removal has
gates. Before deleting a board entry, confirm all three:

1. the accepted proposal / plan is archived;
2. its lasting truth has migrated to durable homes (doctrine, topic
   docs, the changelog);
3. the cold-start "what was tried, and why?" is answerable from the
   archives + commit log **without** this board entry.

If a gate is unmet, finish that migration first, then delete. See
`doctrine/lifecycle.md` > "Removal preconditions for a roadmap item".

---

## Migrated Cairn roadmap (2026-06-12)

Imported from the modflow_tools-side Cairn roadmap when Cairn self-hosted —
live items only, re-expressed for Cairn's vantage (shipped history stays in
the archives); see [`strategy/MIGRATION.md`](strategy/MIGRATION.md). As
native proposals pick these up, they move into the Queued / Active board
near the top of this file.

### Queued

* **Broad-look + roadmap pass** *(queued, Jun 2026)* — the strategy /
  tighten-up pass: take a wide read of the project now that it self-hosts,
  consolidate what accreted across phases 1–4, and shape the forward
  roadmap. The first `dev/strategy/` notes + proposals of the self-hosted
  era.
* **0.3 external correctness test (R-H third-party probe)** *(blocked,
  Jun 2026)* — the launch gate: a consenting third-party scientific repo
  (one that did not contribute to the doctrine) runs the bootstrap
  end-to-end. **Blocks the 0.4 public release.** Blocked on enrolling a
  third party.
* **Remove the collaboration agreement** *(queued, gate: before 0.4)* —
  Maintainer decision (2026-06-12): Cairn no longer needs a collaboration
  agreement. Retire `templates/core/dev/collaboration_agreement.md` and
  re-home/drop every surface that references it (the `AGENTS.md`
  required-reading link, the `agent_collaboration.md` / `dev/README.md`
  pointers, the onboarding tour step, the `doctrine/plans.md` External
  Review Norms cite — re-home those norms, the scaffold's expected-folder
  wiring, the bootstrap tests). Cross-cutting doctrine + template +
  scaffold + test change → its own proposal (the guide star treats the
  agreement as load-bearing, so the proposal carries the deliberation).
* **0.4 launch-surface polish** *(queued for 0.4, not launch-blocking)* —
  graphics/figures in the adopter-facing docs + quickstart (lower the
  "doctrine-heavy at first contact" friction); a comment-cleanup pass
  (strip blow-by-blow comments; keep the *why*) before public adopters
  fork the code; and the shipped-executable-authority unification (one
  `shipped_executables()` traversal for install / manifest / security
  scan / upgrade).

### Deferred follow-ups (durable home)

The permanent, tracked home for Cairn work parked with revival conditions
— each becomes its own proposal when picked up (re-expressed generalizably,
no adopter specifics). Imported from the modflow_tools-side batch ledgers;
none blocking.

**Lifecycle apparatus**
* **Lifecycle mutation/commit arm** — the typed-mutation ops (decision /
  review / open / archive) + commit the read-only planner deferred; gated on
  the dogfood study *and* its own Security Review (commit is a separate
  privilege; print-the-command in v1).
* **Lifecycle mechanization dogfood study** — the multi-session,
  Maintainer-run measurement that earns (or declines) the mutation arm; rank
  by prevented-failure / preserved-assurance, not frequency.
* **Planner cross-checks** — `next` surfaces "review status undetermined" on
  an absent/malformed plan-review line (E-#1); assert the artifact resolves
  under `dev/` (E-#2).
* **`_agent_of` round-suffix regression test** — pin the `## Review (Round
  N)` header shape in the Cairn tree.

**Scaffold / engine**
* **Facade-loader symlink hardening (C-#3)** — refuse any engine submodule
  that is a symlink or resolves out-of-tree, across all three facades.
* **End-gate frozen-set decision (C-#4)** — whether the A/B/C engine
  packages fold into the gate manifest's `frozen_files`.
* **Facade residuals (B-#1/2)** — clean a partial `sys.modules` entry on a
  failed mid-load; reject a mismatched `<kind>:` prefix in `_ast_attest`.
* **Side-door non-executable surfaces** — disposition for the onboarding
  activation log, preset sources, and issue-capture forge starters.
* **Module destination renames / binary module files** — relocation
  classification when a module's destination changes; byte-preserving staging
  for non-text module files.

**Stack-neutrality**
* **Language-neutral conformance fixtures + golden vectors (Move 5)** — for
  the extrication seam (exit semantics, path containment, lockfile schema,
  slot parsing, 3-way merge, security refusals), generated from the Python
  reference. The seam architecture shipped; the executable fixtures are
  deferred.

**Coordination**
* **Refine the intent tool's necessity test** — gate on *shared-worktree*
  multi-agent, not just team size (worktree-per-agent doesn't need it).
* **Move `dev/intent-config.json` → `dev/.cairn/`** — machine-edited settings
  belong in the machine-state dir; transition reads both paths.

**Doctrine**
* **Count-claims doctrine dedup** — fold the three-kind concept into
  `doctrine/lifecycle.md` with a one-line pointer from `doctrine/proposals.md`
  + `doctrine/plans.md`.
* **Model-tier vocab single-source** *(low residual)* — the tier→model
  binding is canonical in `dev/.cairn/model-selection-mapping.yml`; revisit
  only if a project later adds its own metrics-config tier vocab.

**Adoption UX**
* **Constructive readiness** — when a Cairn tool finds a project below an
  expected bar, it should *offer and drive the path to readiness* (scaffold
  the missing pieces, guide the next action), not emit a bare "not ready"
  verdict. Generative about adoption, not only diagnostic.

**Lower-priority**
* **Container P3s** — acceptance credential-residue leg (note/drop); `--user`
  on a future Docker acceptance leg; pin the `git` apt version for image
  byte-reproducibility.
* **Differential-oracle two-stage `promote`** — future-use mechanism for a
  Cairn-engine refactor needing behavior-preservation promotion (trust root
  established, nothing pending; see `bootstrap/REANCHOR_RUNBOOK.md`).
* **Lifecycle-routine skill payloads (post-v1)** — additional episodic skills
  (proposal-open, review-append, decision-scribe, plan-archive); promote
  harness skill targets to native-tested as fixtures prove them.

### Release path

The version ladder is staged so the methodology stabilizes before going
public:

* **0.3.0** — current; private internal milestone (2026-06-12). Phases 1–4
  complete; Phase 5 (launch + governance) in progress.
* **0.3 external test** — the R-H third-party correctness probe (queued
  above); must clear before going public.
* **0.4 — earliest public release.** No earlier than 0.4, and only after the
  0.3 external test clears. The 0.4 candidates above are launch-surface
  polish, not blockers.
* **0.5+** — per-project efficacy-data infrastructure and beyond.

**Public-launch sequence** (deferred to 0.4+; Maintainer-gated, in order):
eyeball-check the private mirror renders cleanly → flip the repo to public +
set the template-repo flag (the actual "ship it" moment; explicit go-ahead
required) → enable Zenodo integration → tag `v0.4.0` and push (triggers
Zenodo deposition → DOI) → commit the issued DOI into `CITATION.cff` →
archive the `cairn_methodology_repo` construction plan via lasting-truth
migration.
