# Code review at agent scale

**Author**: Codex / Strategy
**Model**: Codex (exact runtime model identifier unavailable)
**Date**: 2026-10-28
**Status**: draft
**Type**: design-exploration
**Surfaces this would feed**: v0.7 adopter support for agent change review and visual human review of codebase evolution. Scheduling is tentative; this note authorizes no implementation or policy change.

## The question / felt gap

Agent teams can produce changes faster than scientists can read them. Cairn needs two complementary capabilities: **agents review individual changes; people review the evolving system**. Humans need not inspect every patch. They should be able to understand what the software can now do, how its structure is changing, and whether complexity is earning its keep.

The proposed human interface is a visual, evidence-linked **codebase review**, comparing a chosen release or commit with the current system. It answers: what did we build, how does it fit together, and what should we consolidate? It is not another approval gate, a wall of agent comments, or an automatic bloat verdict.

## Method

Surveyed research through 2026-10-28 using [Consensus](https://consensus.app/search/we-are-designing-a-stage-0-strategy-for-a-vendor-n/_nAR66dJQ26RyG3grawJlA/), arXiv and primary engineering accounts. Opened the sources below; this was a targeted survey, not a systematic review. Consensus supplied discovery leads, not independent verification.

Read Cairn's [review doctrine](../../doctrine/dual-review.md), [review sweep](../agent_collaboration.md#the-review-sweep), shipped architecture/testing modules and adjacent strategies.

External-repo paths: inspected LHM's `tools/scope_map.py`, `tools/scope_map.html` and `tests/test_scope_map.py` at LHM commit `8d0460e8` (those paths were clean). This was a source/documentation inspection, not an execution audit, benchmark or adopter trial.

## Evidence and its limits

| Source | Design implication; limit |
|---|---|
| [Bacchelli & Bird, ICSE 2013](https://www.microsoft.com/en-us/research/publication/expectations-outcomes-and-challenges-of-modern-code-review/); [Sadowski et al., ICSE SEIP 2018](https://research.google/pubs/modern-code-review-a-case-study-at-google/) | Understanding, knowledge transfer and small review cycles matter alongside defect finding. Industrial practices do not establish a scientist's ideal workload. |
| [Alami & Ernst, CHASE 2025](https://arxiv.org/abs/2501.02092); [Zhong et al., March 2026 preprint](https://arxiv.org/html/2603.15911v1) | Excess feedback can burden reviewers; people contribute contextual and testing judgments. Suggestion adoption is not correctness or causal productivity. |
| [c-CRAB, March 2026 v1](https://arxiv.org/html/2603.23448v1); [CRBugBench, October v1](https://arxiv.org/html/2610.13668v1); [SecPRBench, October 24 v1](https://arxiv.org/abs/2610.33509) | Evaluate review with independently grounded faults and behavioral evidence. Context, repair agents and model judges limit comparisons. More agents need not improve detection. These benchmarks do not validate scientific conclusions or architectural judgment. |
| [Anthropic engineering account, October 15](https://claude.dev/blog/solving-code-review-at-anthropic/); [StrongDM software factory](https://factory.strongdm.ai/) | Explore fresh-context review, author verification, risk-directed effort and scenarios independent of implementation. These practitioner accounts do not prove a universal workflow or justify removing human scientific judgment. |

The visual system-review design below is a hypothesis, not an intervention these studies have validated.

## Existing foundation: LHM Unpushed Scope

LHM already has a useful first view: a Sankey diagram connecting **workstream -> area -> folder**, with commits/files behind each selection and a shared-files panel. Its generator reads git history and changes no repository content; it writes a report. The page includes data but loads visualization libraries from CDNs, so it is not fully offline.

Reuse that interaction and attribution work before building a rival. Generalization needs explicit repository/base/head selection, project-owned area rules and aliases, and visible attribution reasons. Prefer reliable lifecycle metadata where available; retain an honest unmatched/ambiguous bucket rather than inventing assignments.

Keep two measurements separate: accumulated editing activity across commits, and actual differences between endpoint trees. Repeated edits, reversals, renames and merge resolutions make them different. Neither is delivered capability. Attributing shared-file endpoint growth to individual workstreams needs an explicit method and may remain ambiguous. The existing collector excludes merge commits; an endpoint comparison must still account for their resulting content. Display actual generation time separately from the head commit's time, and label working-tree material separately from committed evidence.

## What the human review looks like

One local report, four linked views, with a shared baseline/current selector and evidence inspector:

![Illustrative codebase-review interface; all names and figures are examples, not repository measurements.](assets/2026-10-28-codebase-review-concept.png)

| View | Graphic and question | What selection reveals |
|---|---|---|
| **Workstreams** | LHM-style flow: which efforts changed which areas? Width selects activity, endpoint growth or file touches, with explicit units. | Attribution, commits, affected files, overlaps and unmatched work. Overlap suggests an integration question, not a demonstrated conflict. |
| **System shape** | Stable-layout component/dependency map, with added, removed and changed parts overlaid. What responsibilities and connections are accumulating? | Entry points, callers, dependency evidence, changed boundaries and relevant independent findings. Distinguish imports, observed runtime links and agent-inferred relationships. |
| **Capabilities** | Workflow map or matrix showing new, changed, removed and uncertain user/scientific capabilities. What can we actually do now? | A concrete workflow, responsible components, examples and existing tests or demonstrations. Claims inferred from plans or names remain unverified until grounded in behavior. |
| **Growth and consolidation** | Baseline/current size bars plus duplication and change-together links. Where should we investigate maintenance cost? | Exact files, measurement method, competing implementations, reasons to retain them, and an agent's evidence-backed consolidation candidate. |

For example: a scientist notices three workstreams converging on one coordinator, selects it, sees repeated orchestration and two new workflows, then asks whether those workflows justify the added responsibility. The next action is a focused investigation, not reading hundreds of commits.

Keep layouts stable across snapshots; offer grouping, labels and non-graphical equivalents rather than an unreadable whole-repository graph. Separate production code, tests, generated material, dependencies, documentation and deliberation. No composite health score, deletion quota or equation of growth with waste. Static unreachability cannot establish that a public, dynamic or externally used interface is unused. Extra code may preserve compatibility, reproducibility or scientific clarity.

## Tools to learn from

Documentation inspected, not audited or installed:

| Building block | Reuse candidate |
|---|---|
| [CodeCharta](https://github.com/MaibornWolff/codecharta) | Existing metric maps, dependency views and version comparison. Trial its useful views before commissioning visualization infrastructure; 3D is optional, not the goal. |
| [Code Maat](https://github.com/adamtornhill/code-maat) | Mine files changing together; distinguish this history signal from actual code dependencies. |
| [pydeps](https://github.com/thebjorn/pydeps); [jscpd](https://github.com/kucherenko/jscpd) | Language-specific import graphs and duplication evidence. Preserve each tool's coverage limits; neither proves bloat. |
| [nbdime](https://nbdime.readthedocs.io/en/latest/); [reviewdog](https://github.com/reviewdog/reviewdog) | Notebook-aware comparison and diagnostic exchange, not scientific-validity certificates. |
| [PR-Agent](https://github.com/The-PR-Agent/pr-agent); [OpenQodex](https://github.com/openqodex/openqodex); [revmux](https://github.com/umputun/revmux); [Review Council](https://github.com/deployhq/review-council) | Change-review commands, finder/verifier separation, supervised runs and preserved dissent. Investigate integration rather than rebuilding an agent orchestrator. |

External analyzers remain optional; Cairn's shipped core stays standard-library-only. Pin and assess licenses, maintenance, execution behavior and data transmission before adoption.

## Recommendation and pilot

Start with LHM's scope view plus a thin system-review companion to Cairn's existing [architecture review](../../templates/modules/team-gated/architecture_review_template.md). Reuse its five lenses rather than inventing another framework. Compare this with unchanged practice and an existing visualization product before selecting a build. Defer hosted orchestration, not any of the four review outcomes.

Routine agent review still needs coherent changes, author verification, independent reconstruction, actionable findings and revision closure. Preserve dissent and unresolved scientific questions; reuse valid evidence rather than multiply broad test runs. The human view summarizes this work but never converts missing review or failed checks into a green graphic.

Pilot on milestone-sized histories containing justified growth and independently prepared duplication, architectural drift and capability overclaims. Compare scientists' accuracy and time explaining the system and identifying useful consolidation, plus false alarms, missed problems, refresh time and token cost. Evaluate routine defect detection separately. Reject attractive graphics that improve neither understanding nor decisions.

Generate on request or at project-chosen milestones, not for every commit. Show stale/missing evidence. Default to local read-only inspection: no implicit candidate execution, code upload or publication. Escape repository-controlled display data and make external resources explicit. Human choices initiate normal reviewed work; no automatic deletion.

Compose with [engineering practices](2026-10-27-codex-adopter-engineering-practices.md), [scientific testing](2026-10-27-antigravity-judicious-testing-and-simulation-verification.md), [team measurement](2026-10-27-antigravity-lightweight-team-measurement.md) and [scoped verification](../plans/scoped-change-verification.md). Before promotion, settle pilot projects, capability evidence, language coverage, privacy constraints and report maintenance. The eventual guidance should serve shipped adopter projects, not just Cairn itself.

## Review

**Temporary**: author to fold accepted comments into the note and remove this section.
**Reviewer**: Antigravity (Gemini 4 Argon)
**Role**: Strategy reviewer
**Date**: 2026-10-28
**Reviewed commit**: 9bd6eb5fb3efadecf6fb0d234f58562277a6c643

**Foundations**

1. **Should it happen as framed?** Yes: separating patch-level agent review from
   system-level human review addresses the core bottleneck of high-throughput
   agent teams, and anchoring the human view in LHM's Sankey scope map plus
   Cairn's five-lens
   [architecture rubric](../../templates/modules/team-gated/architecture_review_template.md)
   avoids inventing a second review framework —
   `dev/strategy/2026-10-28-codex-review-at-agent-scale.md:12-15, 35-42, 76`.
2. **Best alternative**: Stage the design into two explicit tiers rather than
   one monolithic four-view build: ship the deterministic, language-agnostic
   **Workstreams + Endpoint Growth** views (`git log`/`git diff` + Cairn
   lifecycle metadata, sharing collection with
   [`tools/gauge.py`](../../tools/gauge.py)) first, and ground **System shape**
   and **Capabilities** in curated
   [architecture rubric](../../templates/modules/team-gated/architecture_review_template.md)
   and
   [testing-discipline](../../templates/modules/team-gated/testing-discipline.md)
   declarations rather than language-specific static analyzers —
   `dev/strategy/2026-10-28-codex-review-at-agent-scale.md:45-58`,
   `dev/strategy/2026-10-27-antigravity-lightweight-team-measurement.md:114-123`.
3. **What would show it wrong**: If scientists piloting the visual report on a
   real milestone cannot explain what changed, where responsibilities
   accumulated, and what to consolidate faster or more accurately than from
   [`tools/board.py`](../../tools/board.py),
   [`tools/gauge.py`](../../tools/gauge.py), and
   [`architecture_review_template.md`](../../templates/modules/team-gated/architecture_review_template.md)
   alone, or if populating `System shape` and `Capabilities` requires brittle
   per-language AST parsers or unverified agent guesses —
   `dev/strategy/2026-10-28-codex-review-at-agent-scale.md:51-55, 80-81`.

**Blocking before promotion**

* **B1. Separate deterministic git/lifecycle views from views requiring
  language-specific analysis or curated manifests.** `Workstreams` (`:51`) and
  `Growth` (`:54`) can be computed deterministically using only Python's
  standard library from `git log`, `git diff`, and Cairn `dev/proposals/` +
  `dev/plans/` links across any scientific language (Python, Fortran, R, C++,
  Julia). By contrast, `System shape` (imports, callers, runtime links, `:52`)
  and `Capabilities` (behavior-grounded workflow matrices, `:53`) require either
  language-specific static/dynamic analyzers (`pydeps` is Python-only, `:68`) or
  structured declarations. *Satisfier*: Stage the recommendation into (a) a
  deterministic, language-agnostic core (`Workstreams` + `Endpoint Growth`) and
  (b) rubric-linked `System shape` and `Capabilities` views populated from
  explicit
  [`architecture_review_template.md`](../../templates/modules/team-gated/architecture_review_template.md)
  (`## Current architectural shape`) and
  [`testing-discipline.md`](../../templates/modules/team-gated/testing-discipline.md)
  workflow mappings, with language-specific analyzers kept strictly optional.
* **B2. Define the concrete attribution precedence for Cairn workstreams and
  shared-file endpoint deltas.** Lines 39–41 note that LHM's collector needs
  explicit attribution reasons and that shared-file endpoint growth is ambiguous
  across workstreams. *Satisfier*: Name the attribution order for Cairn adopters
  — (1) explicit plan/proposal linkage from commit trailers, branch, or touched
  lifecycle artifacts, (2) project path/area rules shared with
  [`tools/gauge.py`](../../tools/gauge.py), and (3) an explicit
  `unattributed / maintenance` bucket — and state that net endpoint delta
  (`git diff base..head`) on a shared file (`run_coordinator.py`, `:56`) is
  reported per file alongside its contributing workstreams rather than splitting
  net line delta across overlapping edits.
* **B3. Reconcile data collection with `tools/gauge.py` to avoid two competing
  git-history collectors.** The note cites
  [team measurement](2026-10-27-antigravity-lightweight-team-measurement.md)
  (`:84`), which already assigns `product` / `dev` / `machinery` path
  classification and commit-range churn measurement to
  [`tools/gauge.py`](../../tools/gauge.py). *Satisfier*: Specify that the visual
  report shares path bucketing and git-range data extraction with `tools/gauge.py`
  rather than building a parallel collector.

**Non-blocking**

* **N1. Make self-contained, zero-CDN inline SVG the default HTML output.** Line
  37 notes that LHM's `scope_map.html` loads visualization libraries from CDNs
  (preventing offline use), and line 82 says to make external resources
  explicit. Because Sankey flows and growth bars can be rendered as
  self-contained inline SVG directly from Python's standard library, make
  zero-CDN, fully offline HTML the default target so air-gapped or
  privacy-sensitive research teams never trigger external network requests when
  opening a local report.

**Coverage**: covered claim verification (`#1`: checked internal citations
against `doctrine/dual-review.md`, `dev/agent_collaboration.md`,
`templates/modules/team-gated/architecture_review_template.md`,
`dev/plans/scoped-change-verification.md`, and the three linked strategy notes
at `:20, 76, 84`), fail-closed/privacy posture (`#3`: CDN and local read-only
bounds at `:37, 82`), design completeness and scientific scope (`#4`:
multi-language scientific adopter support vs. Python-only static tools at
`:51-55, 68`), cross-document consistency and placement (`#5-7`: composition
with `architecture-review`, `testing-discipline`, and `tools/gauge.py` at
`:76, 84`), and scope/satisfiers (`#8-9`: B1–B3, N1). Not covered: external LHM
repository paths (`8d0460e8` is outside this workspace), full-text
re-verification of external URLs/preprints beyond the limits already stated in
`:26-31`, or test-suite execution.
