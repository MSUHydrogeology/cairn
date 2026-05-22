# Case study — `modflow_tools`

**Project**: `modflow_tools` — a research-grade Python toolkit for
building and calibrating MODFLOW groundwater models, intended to
help graduate-level hydrogeologists assemble world-class regional
models with FloPy and PEST++/pyEMU.

**Dimension profile**: legacy · medium · complex · single ·
solo · concurrent-multi-type.

**Module selection**: kernel + all default-on + two of the
team-gated modules (`dual-review`, `coordination-tiers`).

**Reference manifest**: see
[`modflow_tools-fidelity-manifest.yml`](modflow_tools-fidelity-manifest.yml)
for the machine-readable fidelity record at Cairn reference commit
`d152cbb`.

This case study walks through the matrix application — what the
project looks like on each axis, what the score implies, and which
parts of the apparatus run as a result. It is the smaller of the
two reference walkthroughs; the larger is
[`lhm.md`](lhm.md).

---

## What the project is

`modflow_tools` is a Python package that wraps and orchestrates
MODFLOW 6 (and the legacy MODFLOW-2005 / MODFLOW-NWT versions used
by partners) plus the PEST++ / pyEMU calibration stack. Its
deliverables: a unified `Model` class for build + load + translate;
canonical-state classes (`GridInfo`, `GridValues`,
`TimeDiscretization`) that pair with typed BC and array specs; a
single-dispatch family for MODFLOW-version-agnostic build paths;
calibration ergonomics around per-package `external:` knobs; and a
`CalibrationResults` API with FOSM screening and ensemble-fallback
uncertainty.

It is **the methodology's reference instance** — the codebase the
Cairn doctrine was extracted *from* while being applied *to*. The
two grew together. That is the load-bearing context for the age
classification below.

## Scoring the six axes

### Age — legacy

A counter-intuitive call for a roughly two-year-old codebase, and
worth justifying.

**Why legacy.** The Cairn methodology was authored alongside this
codebase, not before it. Early commits predate the proposal /
plan lifecycle, the role roster, the structural-independence
floors. Some early architectural decisions were made before the
review system existed; the methodology was bolted on once enough
practice had accumulated to encode it. By the age axis's strict
test — "is the methodology being retrofitted onto code that
predates it?" — `modflow_tools` qualifies as legacy.

**What does *not* follow from legacy.** No Legacy Agent role is
installed; no surface-readiness map exists; no
characterization-testing discipline runs as a standing apparatus.
The retrofit apparatus the legacy classification *can* trigger is
not installed here because:

* The early-commit period was short (months, not years).
* The maintainer is the same person who authored the methodology;
  there is no "the original authors are unavailable" failure mode
  the Legacy Agent is meant to absorb.
* The pre-lifecycle code was actively rewritten under the
  lifecycle as the methodology matured; almost no surface remains
  that the proposal / review apparatus has not touched.

**Lesson for adopters.** The age axis sets *eligibility* for the
retrofit modules; it does not by itself *demand* them. A project
whose legacy surfaces are small, recent, and actively
modernized can elect the lighter configuration — but the case for
omission has to be made, and it has to be visible.

### Size — medium

`modflow_tools` is roughly mid-five-figures of Python LOC across
preparation, build, load, postprocess, calibration, and the CLI;
the test suite collects ~2k tests across contract / integration
/ workflow / unit / notebook / benchmark tiers. Medium on the
rubric: too
large for a one-file utility, well below the partition-by-domain
threshold a `domain-agents` module is meant to address.

**What follows.** The `domain-agents` team-gated module is
**not** installed. There is one Implementation Agent role, not
several scoped to subsystems. As the codebase grows past the
clear-partition threshold (separate scientific concerns that
benefit from agent specialization), `domain-agents` becomes the
right next module to add.

### Complexity — complex

A research-grade scientific tool: groundwater flow physics, model
calibration mathematics, multi-version MODFLOW dispatch,
heterogeneous spatial data sources, the FloPy and PEST++ external
contracts. A change here can be technically correct *and*
scientifically wrong — wrong sign convention, wrong units, wrong
ensemble interpretation — without any test catching it.

**What follows.** Review weight is high. The `dual-review`
team-gated module is installed: every change that touches a
contract, an abstraction, or a scientific assumption is eligible
for an External review (structural-independence floor: different
agent type). The Code review section in the plan template
requires a different agent than the implementing one. Security
review is on the role roster as a focused application of External
Review.

### Language — single

Python only. The runtime calls FloPy (Python), shells out to
MODFLOW executables (Fortran) and to PEST++ (C++), but the
codebase the team contributes to is Python end-to-end.

**What follows.** The `dual-language-tests` team-gated module is
**not** installed; one test architecture suffices. Cross-language
seams exist (FloPy round-trips, MODFLOW output parsing) but live
inside Python test code.

### Human team — solo

One human maintainer (Anthony Kendall, MSU). External
contributors interact via issues and the eventual public release,
but the core write surface is one person.

**What follows.** Decision authority is unambiguous — the
Maintainer holds it without committee. The
`dev/collaboration_agreement.md` team-roster slot lists one
human plus AI collaborators. The proposal-Decision step has no
voting; the Maintainer scribes (or instructs a scribe).

### Agent team — concurrent-multi-type

The repository runs Claude Code (Sonnet and Opus, in different
sessions and roles), Codex (GPT-5), and Antigravity in
overlapping working trees. Concurrent multi-agent work happens
intermittently — two agents may be in the same working tree at
once, especially during goodnight scrubs and review handoffs.

**What follows.** This is the axis position that gates the most
apparatus.

* The `dual-review` module is installed (concurrent agent types
  enable the structural-independence floor for External review
  by *agent-type* rather than only by fresh session).
* The `coordination-tiers` team-gated module is installed at the
  **work-intent tier**. The substrate is a single append-only
  JSON-lines claim/release log (`dev/intents.jsonl`, gitignored),
  accessed through one CLI (`python -m tools.intent
  {claim,release,list,install-hook}`) with atomic small-record
  appends; it replaced the original per-agent untracked-YAML-file
  form. A post-commit hook auto-releases the committing session's
  claims whose paths intersect the commit. The real-time
  typed-event tier is not installed; team size does not warrant
  it.
* **Per-session coordination identity.** Holder identity is
  derived per-session from the harness session ID, not a static
  per-tool name — the fix for the same-tool-concurrency collapse
  (multiple parallel Claude sessions would otherwise share one
  "Claude" identity and cross-release each other's claims). The
  resolution ladder: explicit `MODFLOW_TOOLS_AGENT` override
  (escape hatch) → harness session ID → `~/.modflow_tools/agent.yml`
  → none. Harness session-ID env vars, supplied by each harness's
  own reviewer: `CLAUDE_CODE_SESSION_ID` (Claude Code),
  `CODEX_THREAD_ID` (Codex), `ANTIGRAVITY_TRAJECTORY_ID`
  (Antigravity). The ID is hashed in full (sha256, 8-hex) — never
  prefix-sliced — because `CODEX_THREAD_ID` is UUIDv7-shaped
  (time-ordered leading bytes), so a prefix would collapse
  near-simultaneous sessions. `_auto_release` warns when a global
  `MODFLOW_TOOLS_AGENT` export shadows a present session ID.
* The Maintainer ratified the work-intent system through its own
  proposal lifecycle (Codex-authored, accepted), then refined it
  through two follow-on proposals — the JSONL substrate +
  goodnight prune, and the per-session identity model (Codex +
  Antigravity reviewed, each supplying its own harness's session
  var) — the coordination apparatus is dogfooded.

## Module selection (derived)

| Layer | Module | Installed? | Reason |
|-------|--------|-----------|--------|
| Kernel | (always) | yes | The lifecycle (proposals + plans), the Maintainer authority, append-only deliberation, the `dev/` tree, the baseline coordination tier, the session routines. |
| Default-on | `lifecycle-metrics` | yes | Implemented as `tools/lifecycle_metrics.py`; the v1 reference instance of the layer. Its CSV output feeds the project's own evidence section and informed the Cairn metric-layer module. |
| Default-on | `reflections` | yes | The cross-agent goodnight handoff channel. Implemented in `dev/reflections/` (untracked); read by the agent running the day's goodnight scrub. |
| Default-on | `claim-check` | yes | Implemented as `scripts/claim_check.py`; the v1 reference instance of the discipline. Hard-flags broken repo paths and out-of-bounds line citations; soft-flags count claims. Invoked at write-time and during goodnight. |
| Team-gated | `dual-review` | yes | Concurrent-multi-type agent team can staff the structural-independence floor for External review. The complexity axis warrants the extra review pressure. |
| Team-gated | `coordination-tiers` | yes (work-intent tier only) | Concurrent agent team needs a pre-edit signal beyond the kernel's commit-time discipline. Real-time typed-event tier deferred until team size warrants it. |
| Team-gated | `domain-agents` | no | Size is medium; no clear partition. Right next module when partitioning becomes clear. |
| Team-gated | `legacy-agent` | no | Age is legacy by origin but no retrofit apparatus is needed in practice (see Age discussion above). |
| Team-gated | `dual-language-tests` | no | Language is single (Python). |

The minimal honest configuration (kernel + default-on) would still
function; the two installed team-gated modules add structural-
independence review (dual-review) and pre-edit coordination
(coordination-tiers), both of which earn their keep in observed
practice.

## Role roster

Derived from the dimension profile and recorded in
`dev/agent_collaboration.md`:

* **Human Maintainer** (the dimension profile's `human_team: solo`).
* **Strategy and Research Agent** (proposal authorship, doctrine).
* **Implementation Agent** (scoped code changes, plan execution).
* **Internal Reviewer** (same-agent fresh-session review tier).
* **External Reviewer** (different-agent-type review tier — the
  `dual-review` team-gated module's standing role).
* **User Agent** (concrete-mode interactive work; debugging,
  notebook running; the upstream-of-proposal capture surface for
  GitLab issues).
* **Security Review** (focused application of External Reviewer
  with a security threat-model lens — see
  `dev/security_review_protocols.md` in the target).

The `User Agent` role was added after the role-confirmation
discipline matured; the `Security Review` focused-mode was
formalized once a periodic security-audit cadence was needed.
Both belong to the canonical Cairn roster (`doctrine/roles.md`).

The 2026-05-20 amendment added a per-role **capability-tier
floor**; the floor was ported into Cairn doctrine in the
2026-05-19 → 2026-05-21 doctrine sync (see the F9 evidence
ledger below). The adopter-local tier-to-model mapping (per
`templates/modules/team-gated/model-selection.md`) is in §
"Tier-to-model mapping" further down this case study.

## Customization narrative

The five customization block slots (Cairn `BOOTSTRAP.md > Appendix
A`) were filled as follows.

* `project-overview` in `AGENTS.md` — a short statement of what the
  package does and the audience (graduate-student hydrogeologists
  building MODFLOW models). Authored by the Maintainer + Strategy
  agent together.

* `project-conventions` in `AGENTS.md` — naming conventions,
  development-environment (conda env `lhm`), high-risk surfaces
  (MF2005 write-side parity, FloPy round-trip), and a numbered
  operational-pitfalls list that grows with practice. Filled by
  the Maintainer + Strategy agent; the pitfalls list is updated as
  failure modes are observed.

* `role-roster-additions` in `dev/agent_collaboration.md` —
  filled with the `User Agent` and `Security Review` role
  descriptions. The content was sourced from the canonical Cairn
  role roster (`doctrine/roles.md`) and adapted to project-local
  conventions (the GitLab-issue capture surface; the focused-mode
  security review protocol).

* `coordination-additions` in `dev/agent_collaboration.md` —
  filled from the `coordination-tiers.md` module template (the
  `Merged into:` block describing the work-intent tier). Adapted
  with project-local conventions: an untracked `dev/intents/`
  directory; an empty-intent-directory false-clear rule; a
  schema for the per-intent YAML.

* `team-roster` in `dev/collaboration_agreement.md` — one human
  (Anthony Kendall, Maintainer) plus AI collaborators (Claude,
  Codex) with their signature dates. The amendment ladder is
  recorded in the file's Revision History.

## What shipped (evidence)

The Cairn methodology was not the *first* thing on this codebase,
so the evidence is the corpus the lifecycle has produced. At the
Cairn reference commit `d152cbb`:

* **Proposal lifecycle**: dozens of accepted proposals across
  `dev/proposals/archive/`, each with an Internal review record;
  many with an additional External review; every Decision
  scribed.
* **Plan lifecycle**: archived plans for non-trivial work, each
  with chunk-by-chunk sequencing, a Code review section, and
  Lasting-truth migration notes.
* **Strategy work**: longer-horizon notes in `dev/strategy/`,
  including the "human-AI-team-development-framework" doc that
  catalyzed the Cairn methodology itself.
* **Verify-before-asserting discipline**: the `claim_check.py`
  reference implementation; the typology proposal cataloguing
  observed verify-before-asserting failures.
* **Lifecycle metrics**: a v1 extractor producing per-proposal
  CSVs of review rounds, revision counts, time-to-decision; the
  empirical baseline that informs Cairn's evidence section.
* **Test corpus**: a tiered suite (contract / integration /
  workflow / unit / notebook / benchmark) where testing is
  absorbed into every proposal as required acceptance criteria
  rather than delegated to a Test-Agent role.

## Doctrine-sync 2026-05-19 → 2026-05-21 (F9 evidence ledger)

The modflow_tools project ran a discovery window between
2026-05-19 and 2026-05-21 that surfaced nine doctrine landings,
all of which ported into Cairn proper through the
`cairn-doctrine-sync-may-19-21` plan. This section is the
evidence ledger the plan's F9 requirement names: the link from
each Cairn-doctrine surface to the modflow_tools incident, file,
and commit that grounds it.

| Cairn doctrine surface | Adopter incident / file (modflow_tools) | Source commit |
|------------------------|------------------------------------------|---------------|
| `doctrine/coordination.md` > "Required signal+read for coordination-surface files" | Staged-index collision on `dev/PLANNING.md` (cf2f45e) -- two agents silently edited different sections; one commit absorbed the other's unstaged work. Promoted the required-signal-read protocol on shared-comm files: `dev/PLANNING.md`, `dev/agent_collaboration.md`, `dev/NEXT_SESSION.md`, `CHANGELOG.md`. | `90cdd76` ("Sharpen work-intent doctrine: required signal+read for shared communication files") |
| `templates/modules/team-gated/coordination-tiers.md` > "Tracked collision log" | `dev/collision_log.md` (markdown table at the repo root) — three event kinds (`true-staged-index`, `prevented-overlap`, `parallel-non-conflict`); 14-day rolling window; goodnight migration from reflections. | `be58d78` ("R2 staged-index assessment: implement + archive") + `ca16ffd` (lifecycle-metrics-layer-v2 Chunk A4 — collision-log parser + rolling-14d snapshot column) |
| `templates/modules/team-gated/coordination-tiers.md` > "Goodnight intent-hygiene" | `dev/intents/` (untracked YAML) accreted "done" intents over weeks; prune-intents + migrate-collisions goodnight steps codified. | `ea30649` ("prune-intents goodnight step: implement + archive") |
| `doctrine/session-routines.md` > "The next-session starting plan: written from scratch each goodnight" | `dev/NEXT_SESSION.md` accreted across ~10 sessions; readers acted on stale "pickup-next" entries that had already shipped. Rewrite-from-scratch discipline promoted. | `13f60c2` ("Doctrine: NEXT_SESSION.md is rewritten from scratch each goodnight") |
| `doctrine/dual-review.md` > "Decision-support Round-2 review" | Two 2026-05-20 proposals had External-reviewer findings appended after the author's Response and Revised proposal; both ran into the "another revision cycle?" trap before the structural-property naming landed. | `c41962b` ("agent_collaboration: document Round-2 decision-support review + procedural-gap Decision-resolution") |
| `doctrine/lifecycle.md` > "Procedural-gap inline Decisions" | tier-1.1 particle-tracking plan hit a procedural gap mid-implementation (a missing enumeration of a sub-package retrofit); Maintainer scribed an inline Decision-clarification on the live plan rather than open a new proposal. Three-criterion gate codified. | `c41962b` (same commit as Round-2; both patterns surfaced together) |
| `doctrine/lifecycle.md` > "Deferred-follow-up revival" | Multiple accepted proposals carried explicitly deferred follow-up items; the revival-as-implementable failure mode was observed before the rule was named. | (cumulative across the window; codified incrementally) |
| `doctrine/lifecycle.md` > "The roadmap is a current-state index, not a historical log" | `dev/PLANNING.md` had grown a "Completed recently" section that gradually became the primary where-did-this-happen surface, shadowing the archived plans and the changelog. No-history posture promoted. | `5e30ea4` ("Doctrine: PLANNING.md is not a historical record") |
| `doctrine/roles.md` > "Capability floors -- model selection by role and risk" + `templates/modules/team-gated/model-selection.md` | The project runs Claude Opus 4.7, Claude Sonnet 4.6, Codex (GPT-5), and Antigravity (Gemini 2.5 Pro) in different roles; the per-role capability-floor doctrine was authored on `modflow_tools` and is the first adopter mapping. | `cf2f45e` ("implement role-based model selection doctrine") + `3ac3f3b` (sharpening of code-review findings) |

The ledger is the load-bearing link from Cairn's abstract
doctrine to the concrete adopter incidents that surfaced the
patterns. Future Cairn doctrine syncs from other adopters will
add their own ledger rows.

## Governance-doctrine sync 2026-05-22 (fidelity-gaps: gaps 1–2)

A second sync — the `cairn-fidelity-gaps` plan — ported two
governance landings that the project accepted on 2026-05-21 (the
`lifecycle-metrics-layer-v2` proposal) into Cairn proper. These are
the two rows whose *source* is modflow_tools; gaps 3–11 of the same
plan came from the LHM adopter (see `lhm.md`).

| Cairn doctrine surface | Adopter incident / file (modflow_tools) | Source |
|------------------------|------------------------------------------|--------|
| `templates/modules/default-on/lifecycle-metrics.md` > "The Measurement Compact" | The project's per-agent / per-tier lifecycle-metrics surfaces risked being read as agent ranking. modflow_tools adopted the five commitments + two-tier enforcement, and an **unconditional wording-ban contract test** (`tests/contract/test_measurement_compact_no_external_per_agent_metrics.py`) that scans externally-facing files for per-agent/per-tier tokens. Cairn ports the doctrine and the *idea* of the gate; the contract test is named here as **one** implementation, shaped by this project's file layout — not the canonical form. The Cairn example gate parameterizes its banned-token list rather than hardcoding identities (vendor-neutrality). | modflow_tools `AGENTS.md` > "The Measurement Compact"; `2026-05-21-claude-lifecycle-metrics-layer-v2` proposal (Chunk B1b contract test) |
| `doctrine/rationale.md` > "How the doctrine evolves under evidence" + `doctrine/session-routines.md` > "Goodnight-time synthesis" | The project churned doctrine faster than it could be internalized until the rate-limit gate landed: no doctrine change from a single incident unless the Maintainer classifies it high-risk (security / data-loss); else recurrence or goodnight synthesis. The concrete recurrence instance is the **14-day rolling window** on `dev/collision_log.md` (one specific window length); Cairn states the gate generally and leaves the window length to the adopter. | modflow_tools `AGENTS.md` > "Adaptive-doctrine rate-limit gate"; the 2026-05-20 five-sharpenings-at-once worked example |

## Tier-to-model mapping (per `model-selection` module)

Per Cairn's `templates/modules/team-gated/model-selection.md`,
each adopter that installs the model-selection module publishes
its concrete tier-to-model mapping in its case study (Cairn
doctrine names the invariant; the case study identifies the
models). `modflow_tools` runs the following mapping; model
names are pinned to their 2026-05-20 versions and will be
updated as the lineup evolves.

| Tier | Vendor A (Anthropic) | Vendor B (OpenAI / Codex) | Vendor C (Google / Antigravity) |
|------|----------------------|---------------------------|---------------------------------|
| **high-capability** | Claude Opus 4.7 (1M context) | GPT-5 (high reasoning) | Gemini 2.5 Pro (Antigravity) |
| **medium-capability** | Claude Sonnet 4.6 | Codex (GPT-5 standard) | — |
| **low-capability** | Claude Haiku 4 | — | — |

Vendor diversity is populated at the high-capability tier (the
External Review and Maintainer-scribing roles get the strongest
*structural-independence* benefit from cross-vendor reviewer
selection). The medium-capability tier has two vendors
available; the low-capability tier currently has only Vendor A
populated, which is acceptable because no high-stakes role
defaults to low-capability.

Default tier-by-role assignment (matching the module's default
template):

* **High-capability tier**: Strategy / Research, External
  Review, Security Review, Maintainer scribing.
* **Medium-capability tier**: Implementation (non-trivial),
  Internal Review, Code Review.
* **Low-capability tier**: Implementation (trivial chunks),
  User Agent (routine workflow exercise), non-substantive doc
  tweaks.

The Maintainer has not lowered a high-stakes floor for any
session or sub-domain in this project. The mapping is reviewed
at each goodnight in the context of the day's substantive work.

## What might surprise an adopter

* **Legacy by origin, greenfield in practice.** A project can
  score `legacy` on the age axis without installing the Legacy
  Agent or surface-readiness map. The classification is
  descriptive of *how the project arrived at the methodology*;
  the module selection is about *what apparatus the team
  actively needs*.

* **The reflections channel is intermittent, not nightly.** The
  goodnight routine fires when a substantive multi-agent session
  ends; many sessions are short or single-agent and skip the
  reflection step. The channel is durable when it fires, not
  performatively daily.

* **Work intents are courtesy signals, not locks.** An empty
  `dev/intents/` directory means "nobody declared," never
  "nobody is working." `git status` and recent `git log` remain
  the source of truth for what is actually being touched.

* **The capability-tier floor (role-based model selection)
  layers on top of the structural-independence floor.** The
  two axes — agent-type independence (kernel) and model-tier
  capability (per-role) — stack rather than substitute. A
  same-agent-fresh-session Internal review on a `standard`-tier
  model is an Internal review; a different-agent-type
  `frontier`-tier review of the same artifact is a stronger
  signal in both axes.

## How to read this case study

The reference manifest
([`modflow_tools-fidelity-manifest.yml`](modflow_tools-fidelity-manifest.yml))
records the *what*: which modules are installed, which slots are
filled, which Cairn commit informed the install. This narrative
records the *why*: the reasoning that justifies each axis score
and module decision, the project-local adaptations of the merged
module content, and the practical experience of running the
configuration.

The [`lhm.md`](lhm.md) case study is the larger sibling — a
legacy, multi-language, large codebase running the full
team-gated apparatus. The pair illustrates the matrix's range
without requiring an adopter to imagine intermediate cases.
