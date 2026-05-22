# Case study — LHM (Landscape Hydrology Model)

**Project**: LHM — an 18-year-old coupled surface-hydrology /
groundwater research model. Surface processes (snow, ET, runoff)
in MATLAB; a MODFLOW groundwater coupling; a Python frontend that
wraps and orchestrates the MATLAB core; an in-flight MATLAB →
Python port.

**Dimension profile**: legacy · large · complex · multi · solo ·
concurrent-multi-type.

**Module selection**: kernel + all default-on + **all five
team-gated modules**.

This case study is the larger of the two reference walkthroughs:
the **full-apparatus** configuration of Cairn, where every
team-gated module finds a use. The smaller sibling is
[`modflow_tools.md`](modflow_tools.md). The pair illustrates the
matrix's range without requiring an adopter to imagine
intermediate cases.

The walkthrough draws on the LHM proposal
`2026-05-17-claude-dev-collaboration-model` (accepted), which
established LHM's Cairn-equivalent adoption. The proposal lives
in the LHM repository; this case study summarizes its
dimension-profile reasoning and module selection without
duplicating the project's working content.

---

## What the project is

LHM (Landscape Hydrology Model) is a coupled surface-water /
groundwater model used in MSU hydrogeology research and external
collaborations. Its architecture has three clean activity
domains:

* **Inputs** — climate and forcing ingestion, feature data
  preparation, model-grid mapping (`frontend/preparation/`,
  `frontend/import/`, `lhm/input/`).
* **Model** — the simulation core: snow physics, ET, runoff,
  routing, and MODFLOW groundwater coupling (`lhm/groundwater/`,
  `lhm/surface/`, the controllers).
* **Outputs** — UI, postprocessing, output controllers
  (`frontend/ui/`, `output_controller.m`).

A `frontend/helper/` directory holds cross-cutting infrastructure
(datastore, feature, GIS, HDF5 I/O) that straddles all three
domains.

The model core is the legacy. The Python frontend (added ~2024)
wraps it without changing the science; an in-flight MATLAB →
Python port is migrating modules to Python under a
characterization-testing discipline.

## Scoring the six axes

### Age — legacy (deeply)

* **History**: ~18 years of accumulated development, originally
  imported from SVN in 2008. ~2,800 commits.
* **Test coverage**: zero automated tests on the MATLAB core
  before the Cairn-equivalent adoption began.
* **Documentation trust**: the theory documentation and developer
  guide are partial and known to have drifted from current
  behavior in several modules.
* **Modernization debt**: substantial. Behaviorally load-bearing
  MATLAB whose semantics live only in the running code, not in
  any spec.

LHM is the canonical legacy case the age axis is designed for —
where modflow_tools is "legacy by origin, greenfield in
practice," LHM is **legacy throughout**, with all the retrofit
apparatus the axis names.

**What follows.** The `legacy-agent` team-gated module is
installed. It carries:

* A **Legacy Agent** role with a clear scope: characterization
  testing of the MATLAB core, documentation retrofill from the
  historical design notes (`dev/old_docs/`), and the
  surface-readiness map.
* A **surface-readiness map** classifying every legacy surface as
  *Ready* (safe to change), *Transitional* (changes only under
  characterization tests), or *Frozen* (no behavior changes —
  port-then-replace).
* A **characterization-testing** discipline: pin current behavior
  with tests before changing it, even if the behavior is odd, so
  the change is provable as behavior-preserving.
* MATLAB → Python **port stewardship** as an owned transition,
  not a side activity.

### Size — large

* **File count**: ~505 source files (376 MATLAB + 129 Python),
  roughly four times modflow_tools.
* **Subsystem partition**: clean three-domain split — Inputs,
  Model, Outputs — each with non-trivial internal structure and
  domain-specific expertise required.

**What follows.** The `domain-agents` team-gated module is
installed. Three Domain Agents are added to the role roster:

* **Inputs Domain Agent** — climate ingestion, feature
  preparation, grid mapping. Python-dominant; the most
  agent-ready domain.
* **Model Domain Agent** — the simulation core. ~100% MATLAB;
  mostly readiness-gated and co-located with the Legacy Agent
  until modules graduate from the readiness map's *Transitional*
  to *Ready* status.
* **Outputs Domain Agent** — postprocessing and UI;
  Python-majority.

A Domain Agent is a **combined Planning + Implementation Agent**
for one domain: it writes the proposal, opens the plan, and ships
the code for its domain — the full arc stays with one agent.
This minimizes handoffs (the multi-agent-systems literature cites
handoff / coordination breakdowns as 35–57% of failures) and
keeps deep domain context (snow physics, MODFLOW coupling,
climate ingestion) inside one agent across the lifecycle.

`frontend/helper/` is **cross-cutting** — no single Domain Agent
owns it. Changes there are Strategy-framed or co-authored by the
affected Domain Agents, and they require cross-domain review.

### Complexity — complex

A scientific simulation tool with research-grade calibration
expectations. The model couples surface and subsurface
hydrology — snow accumulation and melt; potential and actual
evapotranspiration; runoff routing; the MODFLOW groundwater
solution; mass balance across the coupling. Sign conventions,
units, time-step discipline, and ensemble interpretation all
carry scientific consequence.

**What follows.** Review weight is high — the `dual-review`
team-gated module is installed (see Agent team below). External
review is invited routinely for changes that touch the model
science, the coupling, or the calibration interface.

### Language — multi

* **MATLAB**: 75% of source files (376 `.m`). The model core is
  100% MATLAB.
* **Python**: 25% of source files (129 `.py`). The frontend; the
  in-flight port destination.

**What follows.** The `dual-language-tests` team-gated module is
installed. It carries:

* Two test architectures — pytest (Python) and a MATLAB
  test-harness (under characterization-testing discipline as
  modules acquire test coverage).
* A **cross-language-seam doctrine**: every MATLAB ↔ Python
  boundary is named, contract-tested (when Python-side), and
  documented in the developer guide.
* **Port-pairing test discipline**: a module being ported keeps
  both implementations running until the test suite
  bit-for-bit (or numerically-equivalent) agrees.

### Human team — solo

One human maintainer (Anthony Kendall, MSU). External
collaborators consume the model and exchange model artifacts via
file handoffs; the active write surface is one person plus the
AI team.

**What follows.** Same as modflow_tools — decision authority is
unambiguous and lives with the Maintainer. The Domain Agent
roles do not introduce multi-human governance; the proposals,
plans, and implementations all converge on the Maintainer's
Decision.

### Agent team — concurrent-multi-type

The repository runs Claude and Codex in overlapping working
trees. With three Domain Agents added to the roster (Inputs,
Model, Outputs) plus the Legacy Agent and Strategy, concurrent
work across domains becomes routine — multiple agent sessions
can be active in different subtrees simultaneously.

**What follows.** Both the `dual-review` and `coordination-tiers`
team-gated modules are installed.

* `dual-review`: External review uses a different agent type
  (Codex reviewing Claude-authored work, or vice versa) for
  load-bearing changes — contract changes, abstractions, the
  port stewardship, the readiness-map updates.
* `coordination-tiers`: the **work-intent tier** is installed
  (per-agent untracked YAML files declaring path scope before
  edits). The **real-time typed-event tier** is selected as a
  forward option, motivated by the high-concurrency / domain-
  agent team shape; whether it is installed at adoption time or
  added once concurrency intensity warrants it is a project-side
  call.

## Module selection (derived)

| Layer | Module | Installed? | Reason |
|-------|--------|-----------|--------|
| Kernel | (always) | yes | The lifecycle (proposals + plans), the Maintainer authority, append-only deliberation, the `dev/` tree, the baseline coordination tier, the session routines. |
| Default-on | `lifecycle-metrics` | yes | Same v1 reference as `modflow_tools`, adapted to LHM's proposal corpus. |
| Default-on | `reflections` | yes | Cross-agent goodnight handoff; critical here because Domain Agents work in different subtrees and need a daily integrating surface. |
| Default-on | `claim-check` | yes | Hard-flags broken repo paths; especially valuable in a multi-language tree where path drift is silent across MATLAB / Python / docs. |
| Team-gated | `dual-review` | yes | Concurrent-multi-type agent team can staff the structural-independence floor; complexity warrants the review weight. |
| Team-gated | `domain-agents` | yes | Three clean domain partitions; domain expertise is not interchangeable across them. |
| Team-gated | `legacy-agent` | yes | 18-year MATLAB core with zero tests; the canonical retrofit case. |
| Team-gated | `dual-language-tests` | yes | MATLAB + Python; the port discipline needs both. |
| Team-gated | `coordination-tiers` | yes (work-intent; real-time as forward option) | High-concurrency domain-agent team; pre-edit signals are needed beyond commit-time discipline. |

LHM installs **every team-gated module**. That is not a
recommendation to install everything by default — it is the
configuration this project's profile produces. A different
legacy project (small, single-language, no clear domain split)
would install `legacy-agent` and skip the others.

## Role roster

Seven distinct roles plus the focused-mode Security Review (eight
counting it separately). Per the LHM `dev-collaboration-model`
proposal:

* **Human Maintainer** — direction, Decisions, commit/push approval.
* **Strategy and Research Agent** — `dev/strategy/`, vision,
  cross-cutting architecture; *does not write code-edit
  proposals* (that's the Domain Agents' work).
* **Legacy Agent** — characterization tests, documentation
  retrofill, the surface-readiness map, port stewardship.
* **Inputs Domain Agent** — `frontend/preparation/`,
  `frontend/import/`, input-data proposals + plans +
  implementation.
* **Model Domain Agent** — `lhm/` core, the controllers; in the
  near term mostly co-located with the Legacy Agent.
* **Outputs Domain Agent** — `frontend/ui/`, postprocessing,
  `output_controller.m`.
* **Internal / External Reviewer** — review *tiers*, not
  headcount; any agent can fill either tier.
* **User Agent** — interactive pairing; gap capture to GitLab
  issues (LHM already uses `glab`).
* **Security Review (focused mode)** — periodic focused pass on
  trust boundaries (HDF5 I/O, MATLAB engine, subprocess).

The Domain Agent design — combined Planning + Implementation per
domain — is the structural answer to the multi-agent handoff
failure mode. The full arc (proposal → plan → implementation)
stays with one agent per domain, which preserves the deep
context (snow physics, MODFLOW coupling) across the lifecycle.

The 2026-05-20 capability-tier amendment that landed in
modflow_tools (the role-based model-selection doctrine) applies
here too once LHM adopts it: Strategy and Security Review at the
`frontier` tier; Domain Agents and Legacy Agent at `standard`
with the escalation triggers; Internal Reviewer at
`standard`-default with the four escalation triggers. Cairn
doctrine inheritance of the capability-tier rule is queued for
Cairn Phase 4+.

## Customization narrative

The five customization block slots were filled as follows.

* `project-overview` in `AGENTS.md` — the model name, the
  coupling architecture (surface hydrology + MODFLOW
  groundwater), and the user audience (research-grade hydrologic
  modeling at MSU and collaborators). Authored by the Maintainer
  + Strategy agent.

* `project-conventions` in `AGENTS.md` — the multi-language
  development environment, the MATLAB engine call boundary, the
  HDF5 I/O conventions, the snake_case-Python / camelCase-MATLAB
  naming split, the in-progress port and the
  characterization-testing precondition for legacy edits.
  Updated as failure modes are observed.

* `role-roster-additions` in `dev/agent_collaboration.md` —
  filled with substantial content: the three Domain Agent roles
  (Inputs, Model, Outputs), the Legacy Agent role, and the
  Strategy and Research Agent's LHM-specific scope. This slot
  carries the **largest customization** of any case study — the
  domain partition is the LHM-specific architecture, and its
  expression in the role roster is the load-bearing adaptation.

* `coordination-additions` in `dev/agent_collaboration.md` —
  filled from the `coordination-tiers.md` module template, with
  the work-intent tier carrying the agent-scope-declaration
  contract. The real-time typed-event tier is named as a
  forward option — selected on the dimensions but installed
  later as concurrency intensifies.

* `team-roster` in `dev/collaboration_agreement.md` — one human
  (Anthony Kendall, Maintainer) plus AI collaborators (Claude,
  Codex) with signature dates. Same shape as modflow_tools at
  the human level; the role-axis richness lives in
  `agent_collaboration.md`.

## What might surprise an adopter

* **Domain Agents are not just "Implementation Agents with a
  scope label."** A Domain Agent owns the full arc — proposal,
  plan, implementation — for its domain. The "Strategy author
  ≠ Plan author ≠ Implementer" handoff pattern is collapsed *per
  domain* into one agent because the multi-agent literature shows
  the handoff itself is where coordination breakdowns happen. The
  Strategy Agent still authors cross-cutting work; the Domain
  Agents author within-domain work.

* **The Legacy Agent is not "another Domain Agent."** Its scope
  is *retrofit* (characterization tests, documentation
  backfill, the readiness map, the port stewardship), not a
  domain. It works *with* the Domain Agents — co-located on
  Model-domain work in particular — but its deliverables are
  retrofit artifacts, not domain code.

* **The surface-readiness map is the interlock that makes the
  full apparatus tractable.** Without it, every change to legacy
  code is a question ("is this safe to touch?") the Domain
  Agents can't answer alone. The Legacy Agent's continuous
  classification of surfaces as Ready / Transitional / Frozen
  turns "is this safe to touch?" into a lookup, and that lookup
  is what unblocks normal Domain-Agent work on the legacy core.

* **Port stewardship is its own role, not a side task.** The
  MATLAB → Python port is a multi-year transition. Owning it as
  a named Legacy-Agent responsibility — with port-pairing test
  discipline and module-graduation criteria — is what keeps the
  port from becoming an ambient "we'll get to it" backlog.

* **LHM reuses, rather than duplicates, prior LHM doctrine.**
  LHM already had `vision.rst`, `review_protocol.rst`,
  `style_guide.rst`, and `contributing_guidelines.rst` under
  LHM's own docs/developer-guide/ tree (an LHM-repo path, not a
  Cairn one). The Cairn adoption extended these
  in place — review tiers extending `review_protocol.rst`;
  Strategy Agent maintaining `vision.rst` — rather than creating
  `dev/` copies. Only genuinely new doctrine (the collaboration
  agreement, the role roster, the lifecycle templates) landed in
  `dev/`. The minimum-viable-overlap principle.

## The matched pair: modflow_tools vs LHM

The two case studies are designed as a **matched pair** for
illustrating Cairn's range:

| Axis | `modflow_tools` | LHM |
|------|----------------|-----|
| Age | legacy (by origin) | legacy (deeply) |
| Size | medium | large |
| Complexity | complex | complex |
| Language | single | multi |
| Human team | solo | solo |
| Agent team | concurrent-multi-type | concurrent-multi-type |

They share the team axes (solo human, multi-type agents) and the
complexity axis. They diverge on size, language, and age-in-
practice — and the divergences are what drive the module-set
difference.

| Module | `modflow_tools` | LHM |
|--------|----------------|-----|
| `lifecycle-metrics` | installed | installed |
| `reflections` | installed | installed |
| `claim-check` | installed | installed |
| `dual-review` | installed | installed |
| `domain-agents` | omitted (no partition) | **installed** (3 domains) |
| `legacy-agent` | omitted (origin-only) | **installed** (deep) |
| `dual-language-tests` | omitted (single lang) | **installed** (MATLAB + Python) |
| `coordination-tiers` | installed (work-intent) | installed (work-intent; real-time forward) |

LHM installs every team-gated module; modflow_tools installs
two. The pair shows the matrix doing work — the dimensions
produce different module sets, the module sets produce different
role rosters and review weights, and the resulting
configurations are different shapes of the same doctrine.

This is what "the methodology is the same; the configuration
differs" looks like in practice.

## Fidelity-gaps sync 2026-05-22 (gaps 3–11 evidence ledger)

The LHM bootstrap proposal (`2026-05-17-claude-dev-collaboration-
model`, accepted in the LHM repo) developed — across four review
rounds — nine generalizable mechanisms that the thin Cairn modules
did not yet carry. The `cairn-fidelity-gaps` plan ported them into
Cairn proper. This ledger links each Cairn surface to the LHM
review finding that grounds it; the LHM-specific instances (MATLAB,
the readiness ledger, the three domains) live here, not in the
doctrine.

| Cairn doctrine surface | LHM finding that grounds it |
|------------------------|------------------------------|
| `team-gated/legacy-agent` > "'Ready' means more than 'has a test'" + the readiness schema | Codex R5 + the Internal rounds: for legacy *scientific* code, the three-label tier set is a trap — "has a test" is not "safe to change." LHM's readiness records carry the full per-surface field set (verification command/owner, scientific assumptions, external-data deps, allowed agent actions). |
| `team-gated/legacy-agent` > "The readiness map is shared-state governance" | LHM Internal finding 1: the readiness map is the most collision-prone surface (every Domain Agent reads it; characterization work rewrites it). Single-writer tier column + dated tier-bump-request protocol. |
| `team-gated/legacy-agent` > "Single file vs. many" | The decentralized-registry alternative for highly concurrent teams (per-surface records / target-file frontmatter aggregated by a script) names the tradeoff LHM's three-domain concurrency exposed. |
| `doctrine/dual-review.md` > "Restricted verification surfaces" + `team-gated/dual-language-tests` | Codex R2: the reviewing agent cannot *execute* **MATLAB**; review of MATLAB code is weaker in practice than its tier. Generalized (Antigravity R2) to any asymmetrical execution environment; the verification-command/owner mechanism + the `verification owner = Maintainer` pre-framework fallback. MATLAB is the case-study instance of the general rule. |
| `team-gated/domain-agents` > "Cross-Domain Proposal" | Codex R4: LHM's Strategy-writes-no-code + shared-infra-is-Strategy-framed roster orphaned code-bearing cross-domain changes; the lead + co-author Domain Agent pattern closes the hole. |
| `team-gated/domain-agents` > "The ownership ledger" | Codex R3: LHM's deep shared helper / UI / config tree across three domains needed a seeded ownership ledger + partition-by-function, not prose ownership rules. |
| `team-gated/security-review` | LHM Implementation finding 5: the named Security Review role needed a protocol home (LHM's subprocess solver invocation + external-data file I/O are its trust boundaries). |
| `team-gated/issue-capture` | LHM Response M: the User Agent's "captures friction as issues" needed a capture surface (issue templates, label manifest, tracker-unavailable fallback). |
| `bootstrap/BOOTSTRAP.md` > "Plan-migration ledger" | Codex R6: LHM's pre-existing ad-hoc planning docs carried real state (shipped phases, blocked items, issue links) a mechanical move would erase. |
| `bootstrap/BOOTSTRAP.md` > "Two-phase de-risking" | Codex R1: LHM's bootstrap split Phase 1 (zero-risk apparatus) from Phase 2 (the RST↔MD documentation relocation touching the docs build). |

Cairn states each as a general invariant; the MATLAB / three-domain
/ RST-build specifics are LHM's, recorded here as the worked
instance. Future adopters add their own ledger rows.

## How to read this case study

Like `modflow_tools.md`, this is a walkthrough of *how the
matrix was applied*, not a project history. The
`dev-collaboration-model` proposal in the LHM repository carries
the operational detail (role responsibilities, the surface-
readiness map's status classes, the port-stewardship
discipline); this file summarizes the dimension-profile
reasoning that produced it.

The fidelity manifest for LHM is not committed to Cairn — LHM's
repository is the canonical home for the project's living
manifest record. Cairn's role is to document the doctrine and
the case-study walkthrough; the project keeps its own state.
