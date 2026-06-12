<!-- Migrated 2026-06-12 from modflow_tools dev/strategy/ (Cairn's development home before self-hosting). Authored from modflow_tools' vantage; some path cites and "current state" reflect that origin and are being adapted to Cairn. Preserved as Cairn's living deliberation record -- see dev/strategy/MIGRATION.md. -->
<!-- claim-check-allow: dev/security_review_protocols.md -->
# Cairn -- the guide star: rationale, current state, and direction

**Author**: Claude (Strategy)
**Date**: 2026-05-14
**Status**: living
**Type**: living-reference
**Audience**: maintainer + collaborating AI agents; secondary audience is a scientist implementing a human + AI development methodology on their own scientific-computing project (Cairn's reader); a future paper reader is tertiary

## Purpose

**Cairn** is an Open Science methodology repository -- explanatory doctrine plus
reusable, forkable templates -- for **scientists building their own
scientific-computing software** who want a disciplined human + AI development
methodology.  Its structure was not designed top-down: it was extracted and
generalized from a working team (one human maintainer, the AI collaborators
Claude and Codex), where each piece had been added in response to a concrete
failure mode -- silent agent drift, deliberation arcs lost across sessions,
cross-agent review masking shared blind spots.

This document is Cairn's **guide star**.  It does three things, and only these:

* **Rationale** -- *why* Cairn's load-bearing pieces exist, positioned against
  the framework anchors below (the human-AI software-engineering, multi-agent
  coordination, scientific-software, and peer-review literatures) and the
  research-software-community literature.  This is the grounding: every
  mechanism is tied to the failure mode it answers and the literature it
  extends.
* **Current state** -- what Cairn *is* today: its shipped surfaces, its
  differentiators, and its two worked case studies (modflow_tools, built
  AI-team-first; LHM, a legacy-rooted retrofit under the same maintainer -- the
  pair that distinguishes "what generalizes" from "what is project-specific
  accretion").
* **Direction** -- where Cairn is headed, as grounded horizons, not commitments
  (the anti-scope at the end binds: each move goes through the normal Cairn
  PR-flow / proposal cycle before shipping).

Cairn is **repo-first**: a forkable, DOI-bearing repository gets *adopted* where
a paper gets *cited*.  A short paper or preprint is optional later amplification,
not the primary artifact -- see "Cairn as a publishable artifact" below.

## Framework anchors

Citable frameworks ground the rationale.  They fall in two groups, and the
numbering is **canonical and append-only** -- a new anchor takes the next
integer and a new row in the Anchor index below, so a cross-reference like
"Anchor 10" stays unambiguous as the set grows.

* **Anchors 1-6 -- the gap-analysis frame.**  They bound the apparatus *as it
  stands*; each has its own `## Gap analysis -- Anchor N` section below.
* **Anchors 7-13 -- introduced where they bite.**  Defined at their point of
  use rather than front-loaded: the research-software-community trio (7-9) and
  the trustworthy-operation principles (10) ground the forward direction; the
  AI-productivity value curve (11) grounds Cairn's "faster" claim; agentic
  context efficiency (12) grounds the apparatus's own context-budget rationale;
  the durable neutral coordination layer (13) grounds vendor- and
  stack-neutrality as a single principle.
  All are indexed after the first six (under "What Cairn is today" and "Where
  Cairn is headed").

The first six:

1. **Interaction taxonomy** -- Treude, C., & Gerosa, M. A. (2025). *How Developers Interact with AI: A Taxonomy of Human-AI Collaboration in Software Engineering.*  Proceedings of the 2nd ACM International Conference on AI Foundation Models and Software Engineering (FORGE 2025).  [arXiv:2501.08774](https://arxiv.org/abs/2501.08774).  Eleven distinct interaction types across the SDLC.
2. **Multi-agent SDLC role design** -- Liu, J. et al. (2025). *LLM-Based Multi-Agent Systems for Software Engineering: Literature Review, Vision, and the Road Ahead.*  ACM Transactions on Software Engineering and Methodology.  [doi:10.1145/3712003](https://dl.acm.org/doi/10.1145/3712003).  Systematic review of LMA applications across SDLC stages.
3. **Trust + governance maturity** -- Steinmetz, S. T. et al. (2025). *The Trust Calibration Maturity Model for Characterizing and Communicating AI Trustworthiness.*  Sandia report SAND2025-00999O.  [arXiv:2503.15511](https://arxiv.org/abs/2503.15511).  Five-dimension maturity model: Performance Characterization, Bias & Robustness Quantification, Transparency, Safety & Security, Usability.
4. **Scientific-software rigor** -- Bridgeford, E. W., Campbell, I., Chen, Z., Lin, Z., Ritz, H., Vandekerckhove, J., & Poldrack, R. A. (2025). *Ten Simple Rules for AI-Assisted Coding in Science.*  [arXiv:2510.22254](https://arxiv.org/abs/2510.22254).  Four-theme framework: problem preparation & understanding; managing context & interaction; testing & validation; code quality assurance & iterative improvement.  Paired with the risk-side anchor: Nature Computational Science (2025), *Threats to scientific software from over-reliance on AI code assistants.*  [doi:10.1038/s43588-025-00845-2](https://www.nature.com/articles/s43588-025-00845-2).
5. **Inter-agent communication patterns** -- two literatures provide complementary lenses:
   * **Cognitive stigmergy / artifact-mediated coordination** -- Ricci, A., Omicini, A., Viroli, M., Gardelli, L., & Oliva, E. (2007). *Cognitive Stigmergy: Towards a Framework Based on Agents and Artifacts.*  In *Environments for Multi-Agent Systems III* (LNAI 4389), Springer.  Crowston, K. *The under-appreciated role of stigmergic coordination in software development.*  Agents coordinate via persistent artifacts in a shared environment; FLOSS / git / issue trackers are canonical software-engineering examples.
   * **Direct agent communication protocols** -- Ehtesham, A. et al. (2025). *A Survey of Agent Interoperability Protocols: Model Context Protocol (MCP), Agent Communication Protocol (ACP), Agent-to-Agent Protocol (A2A), and Agent Network Protocol (ANP).*  [arXiv:2505.02279](https://arxiv.org/abs/2505.02279).  Real-time message-passing protocols dominant in 2025 multi-agent LLM systems.
   * **Multi-agent debate as a coordination pattern** -- Du, Y., Li, S., Torralba, A., Tenenbaum, J. B., & Mordatch, I. (2024). *Improving Factuality and Reasoning in Language Models through Multiagent Debate.*  Proceedings of the 41st International Conference on Machine Learning (ICML 2024).  [arXiv:2305.14325](https://arxiv.org/abs/2305.14325).  Foundational paper for agents-debate-to-consensus patterns; typically synchronous in implementations.
6. **Scientific peer review as a process model** -- the project's review system has its closest real-world analog not in the multi-agent-debate literature (Anchor 5) but in scientific peer review itself.  Anchored on the peer-review process as codified by editorial-standards bodies (the [ICMJE *Recommendations*](https://www.icmje.org/recommendations/) and the [Council of Science Editors](https://www.councilscienceeditors.org/)), which fix the author / editor / reviewer division of labor, and on the open-peer-review taxonomy -- Ross-Hellauer, T. (2017). *What is open peer review? A systematic review.*  *F1000Research* 6:588.  [f1000research.com/articles/6-588](https://f1000research.com/articles/6-588) -- which classifies review systems by seven openness traits.

Each anchor provides one axis of gap analysis below.  None of the six maps perfectly onto the modflow_tools structure; the mismatches are the interesting part.

### Anchor index (clustered, 1-16)

All sixteen anchors are introduced where they bite (the full citation lives at the
point of use): anchors **1-6** each carry a full *Gap analysis* section; anchors
**7-16** are the lighter, inline ones. This index fixes the numbering so
cross-references stay stable and now groups the anchors into a cross-cutting
**Foundation** plus **four thematic clusters** for navigation. The Foundation
(the narrow-waist coordination layer) is the **open-science substrate the four
clusters all rest on** — the same thin-stable-interface principle whether the
interface is a data format, a science protocol, or Cairn's `dev/` tree — so it is
not a peer cluster but the layer beneath them. **Adding an anchor**: take the next
integer, file it under the right cluster (or the Foundation, if it is genuinely
cross-cutting), and define the citation at its point of introduction.

| Cluster | # | Theme | Introduced under |
|---|---|-------|------------------|
| **0 · Foundation (cross-cutting)** | 13 | Durable neutral coordination layer (hourglass / narrow-waist; Beck 2019; Akhshabi & Dovrolis 2011) — the open-science substrate: underpins vendor-neutrality (I), stack-neutrality + protocol-conformance (III/IV), and the trust layer (II) | "Trust as design center" > "The durable neutral coordination layer" |
| **I · AI & multi-agent collaboration** | 1 | Interaction taxonomy (Treude & Gerosa 2025) | "Gap analysis — Anchor 1" |
| | 2 | Multi-agent SDLC role design (Liu et al. 2025) | "Gap analysis — Anchor 2" |
| | 5 | Inter-agent communication patterns (Ricci 2007; Ehtesham 2025; Du 2024) | "Gap analysis — Anchor 5" |
| | 11 | AI-productivity value curve (METR 2025; Boehm 1981 / 2001) | "Cairn as a publishable artifact" > "The honest value curve" |
| | 12 | Agentic context efficiency / "context rot" (EMNLP 2025; Liu et al. 2024) | "Where Cairn is headed" > Horizon 3 |
| **II · Trust, governance & coordination** | 3 | Trust + governance maturity (TCMM; Steinmetz et al. 2025) | "Gap analysis — Anchor 3" |
| | 10 | Trustworthy operation (TRUST principles; Lin et al. 2020) | Horizon 1 + "Trust as design center" |
| | 14 | Scientific-software governance exemplars (USGS FSP; NEP/APE; LIGO/CESM/CMIP) | "Where Cairn is headed" > "Reframing the governance axis for scientific software" |
| | 16 | Recipient-calibrated communication + the comprehension floor (Miller 2019; Kalyuga 2007; Clark & Brennan 1991; Rozenblit & Keil 2002; appropriate-reliance literature) | "Trust as design center" > "Recipient-calibrated communication and the comprehension floor" |
| **III · Scientific-software rigor & validation** | 4 | Scientific-software rigor (Bridgeford et al. 2025; Nature CS 2025) | "Gap analysis — Anchor 4" |
| | 6 | Scientific peer review as a process model | "Gap analysis — Anchor 6" |
| | 15 | Research-software character taxonomy + V&V / reproducibility canon (Hasselbring 2024; Oberkampf & Roy 2010; Roache 2002; PROV-DM; Sandve 2013; Eisty & Carver 2022) | "Where Cairn is headed" > "The scientific-character dimension" |
| **IV · Open-source sustainability & community** | 7 | Maintenance-burden thesis + project typology (Eghbal 2020) | "Where Cairn is headed" > Horizon 1 |
| | 8 | External reuse contract (FAIR4RS; Barker et al. 2022) | Horizon 1 |
| | 9 | Open-development playbook for scientific software (Prlić & Procter 2012) | Horizon 1 |

## Current structure (compact reference)

Before the gap analysis, a one-page sketch of what currently exists:

* **People**: 1 human maintainer (Anthony Kendall, hydrogeologist) + 2 AI collaborators (Claude, Codex).  Co-authorship recorded in commit trailers; signed instrument in `dev/collaboration_agreement.md`.
* **AI surface is bimodal** -- documented in `dev/agent_collaboration.md` > "The AI surface is bimodal":
  - *Agent-side*: Claude + Codex operating under the role roster below; structural work (proposals, plans, implementation, review).
  - *Inline-side*: GitHub Copilot used by the maintainer during hand-edits.  Named in the doctrine as inline-tier editing tooling -- not a team role -- so the distinction between "AI the team coordinates with" and "AI the maintainer uses while editing" is explicit.
* **Roles** (named in `dev/agent_collaboration.md > Team Roles`):
  - Human Maintainer -- product direction, scientific priorities, final judgment.
  - Strategy and Research Agent -- frames proposals, writes plans.
  - Implementation Agent -- ships code against plans.
  - Internal Reviewer -- collaborative-skeptical review pass; also synthesizes a decision-support recommendation for the maintainer and scribes the maintainer's Decision (the maintainer retains the call).
  - External Reviewer -- harder-to-please stress-test (structural-independence floor: different agent type or human).
  - User Agent -- pairs interactively with the maintainer; captures gaps to GitLab Issues.
  - Security Review (focused mode) -- specialized application of Internal/External review.
* **Lifecycles**:
  - Proposal: `proposed -> reviewed -> revised -> accepted/rejected/superseded` with append-only bright-line and one commit per transition.
  - Plan: `open -> executing -> review -> archived` with mutability rule (chunk cells editable pre-impl, append-only post-impl) and load-bearing plan-archive precondition (archive ALWAYS distinct from implementing commits, ALWAYS after code review).
* **Capture surfaces**:
  - `dev/proposals/` (deliberation, append-only).
  - `dev/plans/` (execution, mutable per template).
  - `dev/strategy/` (assessment / horizon-setting).
  - `dev/PLANNING.md` (roadmap status -- mutable).
  - `dev/NEXT_SESSION.md` (cold-pickup context; written at the goodnight routine or on explicit instruction).
  - `dev/reflections/` (per-agent end-of-session retrospectives, read forward by the agent running the goodnight routine; gitignored and pruned).
  - GitLab Issues (in-the-moment friction capture; User Agent's surface).
* **Doctrine**:
  - `AGENTS.md` (cross-agent operational).
  - `CLAUDE.md` + memory files (Claude-specific).
  - `STYLE_GUIDE.md` (design + code style).
* **Review discipline**:
  - Internal Review Norms: steelman first, numbered findings, accept/reject/defer.
  - External Review Norms: make confidence prove itself; closed by fix or explicit wontfix; reviewer prefers different agent type (Codex if Claude authored; Claude if Codex authored).
  - Structural-independence tiers (per `dev/collaboration_agreement.md`): Internal-review tier accepts same-agent-fresh-session; External-review tier requires different agent type or human; code-review tier floors at "not the implementing agent."

## Gap analysis -- Anchor 1: Interaction taxonomy (Treude & Gerosa 2025)

Treude & Gerosa identify eleven interaction types covering the SDLC.  The modflow_tools structure exercises a subset of these heavily and others not at all.

**Heavy usage**:

* **Conversational assistance** -- the Strategy-mode and Review-mode planning sessions.  Probably the most-exercised type in this project.
* **Command-driven actions** -- the Implementation Agent's plan-driven execution; Claude Code's harness shape encourages this.
* **Agentic operations on multi-step tasks** -- the review cycle is an agentic operation that spans multiple turns / sessions.

**Inline tier present but not team-doctrine-named as a role**:

* **Inline auto-complete / suggestion** -- the maintainer uses GitHub Copilot during hand-edits.  It is in use and now named in the doctrine as inline-tier editing tooling, distinct from the agent-side roles (see G1).

**Light or absent usage**:

* **Conversational explanation / Q&A** -- happens implicitly (in User Agent sessions); not a named role / mechanism.
* **Documentation generation** -- happens implicitly inside Implementation work; no dedicated agent or mechanism, but every proposal's acceptance criteria typically include doc updates.

**Gap**:

The project's full AI surface is **bimodal** -- agent-side AI under formal roles, inline-side AI under maintainer-controlled tooling.  This is underdescribed in the LMA literature surveyed (Anchor 2), which treats agent-side AI as the entire AI surface.  The bimodal real-world picture affects how the team's mechanism design should balance handoff burden (where agent-side work picks up) vs. real-time-edit burden (where inline-side work happens within the maintainer's editing session).

**Future-development directions surfaced**:

* **G1 -- Document the bimodal AI surface.**  *Resolved.*  `dev/agent_collaboration.md` > "The AI surface is bimodal" names Copilot's role as inline-tier AI tooling, distinguishing "AI the team coordinates with" (Claude / Codex, named roles) from "AI the maintainer uses while editing" (Copilot, tooling).
* **G1-B -- Semantic drift at the bimodal boundary.**  Inline completions (e.g., Copilot) operate in microscopic contexts optimized for raw speed/convenience, whereas agent-side operations (e.g., Claude/Codex) rely on macroscopic architectural consistency.  Edits made via the inline tier can introduce subtle style, type, or contract drift that pollutes the agent's context window.  This requires the team's pre-commit claim-checking mechanisms to act as a **boundary filter** that gates both human-made inline edits and agent-made implementations before staging.
* **G2 -- Test + documentation as proposal-template requirements, not new roles.**  *Resolved.*  Rather than add Test Agent and Documentation Agent roles (the LMA-literature path), testing, documentation, and examples are formalized as **required, omission-is-a-finding prompts in the proposal template**.  Reasoning: agent roles like Test Agent and Doc Agent are *retrofitting* tools -- they exist because legacy code has untested surfaces and undocumented behavior.  When a codebase is built AI-team-first (modflow_tools is), every proposal already produces its own tests + docs as acceptance criteria; making this explicit in the template requires only a small amendment, not a new role.  Concrete shape: the **documentation** prompt is the `## Proposal > Documentation / doctrine surface` subsection; the **tests** and **examples / smoke checks** prompts are subsections of `## Evidence / verification plan`.  Silent omission of any of the three is a review finding; explicit `N/A: <reason>` is the way out.  Itself a paper-worthy distinction: **"AI-team-built from the ground up" workflows have different requirements than "retrofit AI assistance onto legacy code" workflows**, and the literature is heavily weighted toward the latter.

## Gap analysis -- Anchor 2: Multi-agent SDLC role design (Liu et al. 2025)

Liu et al.'s systematic review maps LMA agents to SDLC stages.  Common LMA roles in the literature:

* Requirements / product-management agent.
* Architecture / design agent.
* Code-generation / programmer agent.
* Code-review agent.
* Test-generation / tester agent.
* Debugging agent.
* Documentation agent.
* Project-management / orchestration agent.

**Mapping the current modflow_tools roster against this**:

| LMA role (literature) | modflow_tools role |
|---|---|
| Requirements / product-management | Strategy and Research Agent (combined with architecture; maintainer holds final product-direction authority) |
| Architecture / design | Strategy and Research Agent |
| Code-generation / programmer | Implementation Agent |
| Code-review | Internal Reviewer + External Reviewer (two-tier) |
| Test-generation | (absorbed into every proposal's acceptance criteria; not a distinct role -- see G2 / G3 for why this is structural, not accidental) |
| Debugging | (partially the User Agent role, but it's user-side not agent-side) |
| Documentation | (absorbed into every proposal's acceptance criteria; not a distinct role -- same reasoning as Test-generation) |
| Project-management / orchestration | Strategy + the proposal lifecycle artifacts themselves |
| (no LMA equivalent) | **User Agent** (user-side, interactive, gap-capture) |
| (no LMA equivalent) | **External Reviewer** (named harder-to-please stance, distinct from the Internal review) |

**Gaps and novel directions**:

* **G3 (novel contribution) -- AI-team-first lifecycle absorbs test + doc work into every proposal rather than separating it into specialist roles.**  The LMA literature's Test-Agent and Documentation-Agent roles are retrofitting tools -- they exist because legacy code arrives at the AI team with untested surfaces and undocumented behavior; someone has to go fill those in.  modflow_tools was built AI-team-first, so every proposal that ships already produces its own tests + docs as part of its acceptance criteria.  Adding Test/Doc roles would be a structural redundancy; the better move is to *formalize* the implicit requirement (see G2).  **This distinction -- AI-team-built-from-scratch workflows vs. retrofit-AI-assistance workflows -- is itself paper-worthy** because the literature is heavily weighted toward the retrofit case.  The accepted LHM `dev/`-collaboration-model proposal instantiates the retrofit case directly -- its Legacy Agent is the standing retrofit role this distinction predicts, justified for LHM's ~18-year legacy exactly where it is unjustified for greenfield modflow_tools.  The built-from-scratch / retrofit pair now has a concrete case on each side; see "Bridge to the publishable artifact" below.
* **G3-B (novel contribution) -- Retrofit roles as a Human Cognitive Adapter.**  In legacy codebases, the biggest hurdle is not merely code rot, but the human developer's entrenched, un-automated coding habits.  The introduction of the Legacy Agent and the Surface-Readiness Ledger serves a social-cognitive purpose: they act as a **cognitive adapter** that forces the human to transition from ad-hoc, untracked modifications to structured, staged git hygiene.
* **G4 (novel contribution) -- The User Agent role.**  LMA literature focuses on agent-side roles (agents acting on the project); modflow_tools introduced a user-side role (agent helping the user act on the project).  Different mode of presence.  Worth surfacing as a contribution to the role-design literature.
* **G5 (novel contribution) -- The External Reviewer as a distinct role.**  Most LMA papers treat "code review" as a single role; modflow_tools' two-tier split (Internal review for landing, External review for proving) with explicit structural-independence requirements (different agent type for the External review) is more disciplined than typical descriptions.  Pair with G6 below.
* **G6 (novel contribution) -- Structural-independence tiers.**  The codified tier rule (Internal review OK with same-agent-fresh-session; External review requires different agent type; code-review floor "not the implementing agent") gives the review system its empirical bite.  Not a standard part of LMA-system descriptions in the literature surveyed.

## Gap analysis -- Anchor 3: Trust + governance maturity (TCMM, Steinmetz et al. 2025)

The Trust Calibration Maturity Model evaluates five dimensions.  Mapping the current structure:

**Performance Characterization**:

The lifecycle-metrics measurement layer (`tools/lifecycle_metrics.py`) walks `dev/proposals/`, `dev/plans/`, and `git log` and emits per-proposal lifecycle metrics (review rounds, revision counts, time-to-decision, finding severities).  The infrastructure and a baseline snapshot exist; what is still missing is a *time series* -- a single snapshot is not yet a trend, so the longitudinal empirical record Cairn's evidence section needs is not yet produced (see "Where Cairn is headed").

**Bias & Robustness Quantification**:

The `verify-before-asserting` operational pitfall (`AGENTS.md > Operational pitfalls > #5`) is now structured as a **4+1 failure-mode typology** (see G9) backed by a date-ordered instance table of agent-side hallucinations caught during review.  This is a deliberate defect taxonomy, but it is not yet wired into the measurement layer for quantitative trend analysis.

**Transparency**:

Within the project: high.  The proposal lifecycle's append-only commit-per-transition structure means every deliberation arc is reconstructible from `git log`.  Externally (to a third-party reader): no formal artifacts beyond the repo itself.

**Safety & Security**:

Covered.  `dev/security_review_protocols.md` carries the threat model, audit surfaces, and severity-tier reporting.  Contract-tier security gate enforced in `tests/contract/test_security_lint.py`.

**Usability**:

The maintainer's interaction surface is well-documented (`AGENTS.md > Session start`; goodnight routine; handoff templates).  No measurement of maintainer-time efficiency or cognitive load.

**Gaps**:

* **G7 -- Measurement layer.**  *Partially addressed.*  The lifecycle-metrics script ships the Performance-Characterization infrastructure with a baseline snapshot; the remaining work is to (a) build a time series across commits rather than the single snapshot, and (b) extend coverage to the Bias & Robustness and Usability dimensions, which remain unmeasured.  The metrics also seed Cairn's empirical section.
* **G8 -- External-facing transparency artifact.**  For the publishable artifact, the in-repo deliberation arc needs an external-readable synthesis.  Not a redesign of the in-repo structure; an additional artifact (perhaps a *docs/methods/* tier) that points outside collaborators at the deliberation record without making them read `git log`.
* **G9 -- Failure-mode typology.**  *Resolved.*  `AGENTS.md` Operational pitfall #5 is structured as a **4+1 typology** -- four subject categories (code-object shape, file existence, tree & history, count claims), each with one 30-second verification check, plus a cross-cutting self-contradiction check -- backed by a single date-ordered instance table.  The flat list became structured data; the next step (G7) is to wire the instance table into the measurement layer.

## Gap analysis -- Anchor 4: Scientific-software rigor (Bridgeford et al. 2025; Nature CS 2025)

Bridgeford et al.'s four themes:

**Problem preparation and understanding**:

Strongly served by the existing structure.  Strategy Agent + proposals + PLANNING.md are essentially infrastructure for problem preparation.  The "Frame" step in the collaboration agreement's Working Rhythm names this explicitly.

**Managing context and interaction**:

Strongly served.  AGENTS.md + CLAUDE.md + good-morning routine + handoff template + the GitLab Issues capture surface form a context-management substrate.  The role-confirmation step in the Working Rhythm tightens this further.

**Testing and validation**:

Mixed.  The test tier roster (`tests/contract/`, `tests/unit/`, `tests/integration/`, `tests/workflow/{smoke,regression}/`, `tests/notebook/`, `tests/benchmarks/`) is unusually disciplined for a scientific-software project.  But:

* Testing isn't role-distinguished (no Test Agent); tests are absorbed into every proposal's acceptance criteria instead -- see G2 / G3 for the structural reasoning.
* Validation of **agent output** specifically -- distinct from validation of code correctness -- is still partly informal (the verify-before-asserting pitfall catches it, with the typology making the catch more systematic; a write-time check would make it proactive -- see G10 / Cluster D).

**Code quality assurance and iterative improvement**:

Strongly served.  The review system + plan-archive precondition (code review must precede archive) + sharpening cycles institutionalize iterative improvement.

**Nature Computational Science risk anchor**:

The Nature paper warns against over-reliance leading to undetected errors in scientific code.  The modflow_tools structure has explicit countermeasures:

* Decision rights preserve human agency (the maintainer is the final arbiter).
* Internal + External review are designed to catch silent errors.
* The verify-before-asserting pitfall is exactly the over-reliance failure mode the Nature paper warns about; it has been caught and documented repeatedly and is now organized as a typology.

**Gaps**:

* **G10 -- Agent-output validation infrastructure.**  *Resolved.*  Distinct from code-correctness tests (which are well-covered).  The write-time claim checker (`scripts/claim_check.py`) flags load-bearing assertions about tree state and forces a verification round before commit -- moving agent-output validation from reactive (caught in review) to proactive.
* **G11 -- Scientific-discipline interlock.**  *Answered in direction.*  The team has hydrogeology-aware vocabulary in memory + AGENTS.md, but discipline-domain expertise is held by the human maintainer, so when the maintainer is out of the loop (e.g., an overnight External review) there is no agent-side mechanism for catching scientific (vs. structural) errors.  The 2026-06-05 LHM fold-back review resolves the long-deferred "gap or feature" question: it is a **gap, and fillable** -- by the **`deliverable` axis's** science-disciplines (physical-validity, numerical-tolerance, provenance; see "Where Cairn is headed" > "The scientific-character dimension").  USGS's *Fundamental Science Practices* domain review is the proof-of-concept that such an apparatus-/agent-run gate is real and separable from the structural review -- proven LHM-first, then folded up.

## Gap analysis -- Anchor 5: Inter-agent communication patterns (Ricci et al. 2007; Ehtesham et al. 2025; Du et al. 2024)

The literature on how agents talk to each other splits into two paradigms, and the choice between them is consequential.  Mapping the current structure against both:

**Paradigm 1 -- Cognitive stigmergy / artifact-mediated coordination (Ricci et al. 2007; Crowston on software development)**:

Agents coordinate via persistent artifacts in a shared environment that subsequent agents read and update.  The original definition (Ricci et al.): *artifacts are environment abstractions that mediate agent interaction and enable emergent coordination*.  Software-engineering precedent (Crowston): FLOSS projects coordinate via git, CVS, issue trackers, mailing-list archives -- all artifacts the next contributor reads to update their mental model.

The modflow_tools structure is **textbook cognitive stigmergy**.  Concrete examples in the current artifact roster:

* **Proposal files** -- the deliberation channel.  Append-only because the artifact-as-channel relies on history being intact.  Status field (`proposed -> reviewed -> revised -> accepted`) IS the coordination signal.  File location (`dev/proposals/` vs. `dev/proposals/archive/`) IS the lifecycle-stage signal.
* **Plan files** -- the execution channel.  Chunk tables are coordination state visible to any agent reading them.  Status field + commit references inside the plan signal what's in flight.
* **PLANNING.md** -- the roadmap-coordination artifact.  Status-tagged entries with cross-links coordinate which agent picks up which item next.
* **NEXT_SESSION.md** -- explicit handoff artifact for cold-pickup contexts.
* **`dev/reflections/`** -- per-agent end-of-session retrospectives; a stigmergic handoff channel read forward by the agent running the goodnight routine.
* **Signature log** (in `dev/collaboration_agreement.md`) -- a coordination artifact for "who has agreed to what version of the working norms."
* **Commit history** -- one-commit-per-lifecycle-transition makes the coordination state machine auditable from `git log` alone.

The pattern fits Ricci et al.'s "engineered artifacts populating the agent working environment" exactly.  

**The Model-Agnostic Resilience Vector**: A vital advantage of filesystem-based stigmergy over real-time communication protocols (Paradigm 2) is **infrastructure-independence**.  By offloading all system coordination state to the version-controlled directory structure, the team eliminates the need for persistent server orchestration.  Crucially, this makes the methodology **completely model-agnostic**: any LLM family (whether a proprietary API or a locally hosted open-weights model like Llama) can seamlessly participate in the team simply by reading and writing files.

**Paradigm 2 -- Direct agent communication protocols (Ehtesham et al. 2025 survey)**:

Dominant in 2025 multi-agent LLM systems.  Real-time message-passing; agents discover each other, exchange task specifications via structured capability cards, stream status events.  The four major protocols:

* **MCP (Model Context Protocol)** -- standardizes how an LLM accesses external tools and contextual data.
* **A2A (Agent-to-Agent)** -- standardizes how autonomous agents discover and communicate; capability cards + artifact exchanges.
* **ACP (Agent Communication Protocol)** -- April 2025; asynchronous REST-based task exchanges.
* **ANP (Agent Network Protocol)** -- broader network-of-agents focus.

The modflow_tools structure uses **none** of these protocols directly.  Agents (Claude in a session, Codex in a session) don't send each other messages; they leave traces in the shared artifact environment that other agents read.  The choice is structural, not incidental -- A2A-style real-time message-passing would require persistent inter-session agent identity and orchestration infrastructure neither agent currently has.

**Paradigm 3 (debate as a special case) -- Multi-agent debate (Du et al. 2024)**:

The foundational paper introduces multi-agent debate for improving factuality and reasoning: multiple language-model instances propose and debate responses over multiple rounds to arrive at a common final answer.  Most implementations are **synchronous** (turn-by-turn within one session, possibly with role-specialized agents like Verifier / Solver).

The modflow_tools Internal + External review structure IS multi-agent debate, but **asynchronous**:

* Proposal author drafts; Internal Reviewer appends Review section in a separate commit; author appends Response section in another commit.
* Each round is a commit-mediated turn, not a synchronous exchange.
* Structural-independence tiers govern who can be on which side (different agent type for the External review, etc.) -- a richer governance layer than typical debate frameworks describe.

This is asynchronous multi-agent debate with codified structural independence -- a variant the literature has not centrally addressed.

**Coordination-failure context**:

Recent industry reporting on multi-agent LLM systems cites striking failure-rate statistics:

* UC Berkeley research finds **coordination breakdowns account for ~35% of all multi-agent failures**.
* Anthropic's enterprise analysis attributes **~57% of multi-agent failures to orchestration-design issues**.

(These figures appear in 2025 survey articles; the primary-source citations would warrant verification for the publishable artifact.)  The modflow_tools structure has explicit countermeasures -- handoff-template discipline, append-only deliberation, role-confirmation at session start, the Stage-to-role matrix -- but no quantitative measurement of how those countermeasures perform.

**Gaps and novel directions**:

* **G12 (novel contribution) -- Stigmergic coordination as a deliberate design choice.**  The modflow_tools structure sits in the cognitive-stigmergy lineage (Ricci et al. 2007; Crowston on software development), NOT in the dominant 2025 agent-protocol lineage (MCP / A2A / ACP).  The literature treats these as alternatives suiting different operational contexts; the choice has consequences for what the team can and can't do (e.g., real-time orchestration is harder under stigmergy; long-arc deliberation across sessions is easier).  Worth naming as a deliberate position rather than an accident, especially because pairing artifact-mediated coordination with multi-agent debate (G5 / G6 / G13) is a coherent design philosophy the publishable artifact articulates as a contribution.
* **G13 (novel contribution) -- Asynchronous, structurally-tiered multi-agent debate.**  Du et al. (2024) and follow-on work (Adaptive Heterogeneous Multi-Agent Debate; Tool-MAD) describe synchronous debate within a session.  modflow_tools' Internal + External review structure is *asynchronous* (commit-mediated turn-taking across sessions) with *structural-independence tiers* (different floors at different stages, including the External-review-tier different-agent-type requirement).  Refines / extends G5 (two-tier review) and G6 (structural-independence tiers) by naming the debate-literature connection explicitly.
* **G14 -- Coordination-failure taxonomy.**  Industry reporting attributes 35-57% of multi-agent failures to coordination / orchestration issues.  modflow_tools has explicit countermeasures but no measurement of how they perform.  Cluster A's measurement layer (G7) could extend to track coordination-class failures specifically -- handoff drift, lifecycle-stage skips, missed cross-references -- and the verify-before-asserting instance table (G9) becomes a starting point for a broader failure-mode taxonomy.

## Gap analysis -- Anchor 6: Scientific peer review as a process model

The closest real-world analog to the modflow_tools review system is not the
multi-agent-debate literature (Anchor 5) -- it is **scientific peer review**, a
fitting and more legible frame for a *scientific* software project.

**The two-stage parallel.**  A careful author runs review in two stages: a
*pre-submission* collegial read that helps the draft *land*, then independent
*journal peer review* that decides whether it is *sound*.  modflow_tools
formalizes exactly this -- the doctrine's own gloss (the Internal Reviewer helps
a proposal *land*; the External makes it *prove* it should) is precisely that
distinction:

| Scientific peer review | modflow_tools |
|---|---|
| Manuscript → editor → referees → decision | Proposal → maintainer → review tiers → Decision |
| Pre-submission collegial read | **Internal Review** (same-agent-fresh-session floor) |
| Independent journal referees | **External Review** (different-agent-type / human floor) |
| Report → rebuttal → revised manuscript | Review → Response → Revised sections |
| COI rules; open peer review (disclosed identities, published reports) | Structural-independence tiers; append-only attributed file in `git` |

G5, G6, and G13 -- previously anchored only on the debate literature -- are more
aptly framed here: the project runs a faithful instantiation of peer review, the
discipline's own gold-standard quality control.

**Where it differs -- the interesting part:**

* **Independence is structural, not institutional.**  Journal independence rests
  on fuzzy social facts (different institution, no recent co-authorship);
  modflow_tools derives it from a brighter, externally checkable one -- a
  different model architecture (Codex reviewing Claude-authored work).
* **Radically open.**  The proposal file is fully attributed and the whole arc
  (manuscript → reports → rebuttal → decision) is reconstructible from `git log`
  -- the maximally-open end of Ross-Hellauer's taxonomy, which the open-science
  movement advocates but few journals adopt.
* **Fast and asynchronous**, with on-call reviewers -- removing peer review's
  worst failure mode (delay) but introducing a different one (G15).
* **Role conflation.**  The maintainer is editor + domain expert + reviewer at
  once (efficient at this scale, but the concern G11 raises); the Internal
  Reviewer's decision-support + Decision-scribing partly mitigates by delegating
  the *drafting* while the maintainer keeps the *call*.
* **A Registered-Reports flavor.**  The proposal's up-front "Evidence /
  verification plan" -- committing to what would falsify the change *before*
  implementation -- is a countermeasure against agentic metric p-hacking: Stage 1
  (design + test plan) is locked before Stage 2 (execution evidence) proceeds.

**Gaps surfaced:** **G15 -- reviewer-pool diversity is structurally bounded**
(two agent families + the maintainer; the External tier mitigates *correlated*
blind spots but cannot manufacture diversity past two model families -- feeds
Cluster A's measurement layer).  **G16 -- structural independence as a
contribution to the peer-review COI literature** (a more enforceable independence
criterion than the institutional one journals rely on; sharpens G6, feeds
Cluster C).

## Cross-cutting synthesis

Pulling the 17 named items together, they cluster into four directions:

### Cluster A -- Measurement layer (G7, G8, G9, G14, G15, G17)

The structure was mechanism-rich and metric-poor.  The lightweight measurement infrastructure (`tools/lifecycle_metrics.py`) is now in place; running it would:

* Seed the publishable artifact's empirical section.
* Make the team's claims about its own discipline (e.g., "External review catches structural problems the author can't see") falsifiable / quantifiable.
* Surface drift: agents whose acceptance rates change over model versions; rounds where revision counts spike.

This is the highest-leverage direction.  The infrastructure cost was low (a script + a PLANNING entry); the remaining cost is even lower (run it, read the output).  G14 specifically extends the layer to coordination-class failures, which the inter-agent-communication literature flags as a major source of multi-agent system failures (35-57% per the 2025 industry reporting).  G15 extends it again -- to reviewer-pool-diversity blind spots: whether particular finding-classes are systematically missed, not only how many findings land.  G17 extends it once more -- to the **comprehension surface** (Anchor 16): keep visible whether the human actually understood a change before deciding on it, so a collapse of review into rubber-stamping is caught rather than silently logged as assent.

### Cluster B -- Documenting deliberate design choices (G1, G2)

Two pieces of the current structure are *intentional* but were *unnamed*; both are now documented:

* The **bimodal AI surface** -- the team's role roster covers agent-side AI (Claude, Codex) exhaustively; `dev/agent_collaboration.md` > "The AI surface is bimodal" now also names the inline tier (GitHub Copilot, used during maintainer hand-edits), distinguishing "AI the team coordinates with" from "AI the maintainer uses while editing."
* The **test + doc absorption into proposals** -- rather than adopting Test Agent and Doc Agent roles (the LMA-literature path, which is a retrofit pattern), testing, documentation, and examples are required, omission-is-a-finding prompts in the proposal template -- **documentation** under `## Proposal > Documentation / doctrine surface`, **tests** and **examples / smoke checks** under `## Evidence / verification plan`.

Both were cheap to ship (small doctrine amendments via the normal proposal lifecycle) and resolve "is this intentional or oversight?" ambiguities for any future reader of the project's structure.

### Cluster C -- Novel contributions to surface (G3, G4, G5, G6, G12, G13, G16)

Seven pieces of the current structure either don't appear in the literature surveyed, or sit in named-but-uncommon corners of it.  They are surfaced as such in `dev/agent_collaboration.md` > "Comparison with the multi-agent-systems literature":

* **AI-team-first lifecycle** (G3) -- the choice to absorb test + doc work into every proposal rather than spinning up Test/Doc agents.  Reflects the underlying distinction between AI-team-built-from-scratch and retrofit-AI-on-legacy workflows.
* **User Agent role** (G4) -- user-side interactive collaboration mode.
* **Two-tier review** (G5) -- Internal review for landing; External review for proving.  Specialized variant of multi-agent debate (Du et al. 2024) with role-asymmetric debate stances.
* **Structural-independence tiers** (G6) -- different floors for review at different stages.  No direct analog in the surveyed debate literature.  The peer-review frame (Anchor 6) sharpens this as **G16**: structural independence -- a different model architecture -- is a more enforceable conflict-of-interest criterion than the institutional independence journal peer review relies on.
* **Stigmergic coordination as deliberate design choice** (G12) -- the project's coordination paradigm sits in the cognitive-stigmergy lineage (Ricci et al. 2007; Crowston) rather than the dominant 2025 agent-protocol lineage (MCP / A2A / ACP).  Worth naming because the literature treats these as alternatives suiting different operational contexts; modflow_tools' choice is structural and load-bearing.
* **Asynchronous, structurally-tiered multi-agent debate** (G13) -- commit-mediated turn-taking across sessions with codified role-asymmetry.  Refines G5 + G6 by naming the debate-literature connection.

**The Dual-Review model.**  G5, G6, G13, and G16 are facets of one nameable contribution -- the **Dual-Review model**: two-tier review (an *Internal* pass that helps a change land; an *External* pass that makes it prove it should land) executed across **structural independence** (a different model architecture reviews -- Codex on Claude-authored work; in LHM, domain-rotation), asynchronously and commit-mediated.  It is a faithful instantiation of scientific peer review (Anchor 6) and, on the openness and independence axes, a *more rigorous* one -- which makes it the project's most legible contribution to a scientific-computing audience.  Alongside the append-only git-committed deliberation lifecycle, it is one of the two differentiators Cairn leads with.

The combination of stigmergy + asynchronous structurally-tiered debate is the coherent design philosophy the team enacts; naming it as such gives Cairn -- and any later paper -- a clean contribution shape.

### Cluster D -- Output-validation surface (G10, G11)

Agent-output validation moved from reactive (caught in review) to proactive: the write-time claim checker (`scripts/claim_check.py`) flags load-bearing assertions about tree state and forces a verification round before commit -- it gates this very doc.  It is tied to the scientific-discipline-interlock question (G11), where the discipline-domain judgment is deliberately routed through the human maintainer.

## What Cairn is today

Cairn is at **v0.2.0** -- the realized methodology repository this doc's
rationale grounds.  Its surfaces:

* **`doctrine/`** -- the generalized doctrine: collaboration-stance,
  coordination, doc-governance, dual-review, lifecycle, rationale, roles,
  session-routines, and the fold-back mechanism.
* **`templates/core/` + `templates/modules/`** -- the installable invariant
  kernel (`AGENTS.md`, `VENDOR.md`, the `dev/` tree) plus default-on and
  team-gated modules.
* **`dimensions/`** -- six adaptive axes (age, size, complexity, language,
  human-team, agent-team) with bootstrap presets, so the apparatus is fitted to
  the project rather than one-size-fits-all.
* **`bootstrap/`** -- the scaffold installer plus its safety, integrity, and
  upgrade machinery.
* **`on-ramp/`** -- three graduated adoption levels (read-the-doctrine /
  hand-copy-the-kernel / run-the-bootstrap), with a level recommended from the
  dimensional profile and an explicit "a project can move up" path.
* **`case-studies/`** -- modflow_tools (built AI-team-first) and LHM
  (legacy-rooted retrofit), with a fidelity manifest.
* **`docs/`, `examples/`, `SECURITY.md`, `CITATION.cff`** -- the adopter-facing
  entry surface, a runnable example, the security/trust posture, and citable
  metadata.

**The two differentiators Cairn leads with** (both genuinely uncommon; see the
Cluster C synthesis above):

* the **append-only, git-committed deliberation lifecycle** -- every decision's
  full arc reconstructible from `git log`; and
* the **Dual-Review model** -- two-tier review (Internal helps a change land;
  External makes it prove it should) executed across structural independence,
  asynchronously and commit-mediated; a faithful, and on the openness and
  independence axes more rigorous, instantiation of scientific peer review
  (Anchor 6).

**The apparatus an adoptable methodology demands.**  Beyond doctrine and
templates, Cairn ships what a *forkable, living* standard needs and a static
prose framework does not: a four-layer **security model** (scaffold safety,
lockfile integrity, content scanning, vendor-neutrality checks); an **upgrade
capability** (3-way module merge with a lockfile and base-cache, so a deployment
folds in new Cairn doctrine while keeping local optimizations); the
**fold-back-ledger mechanism** (a standing channel by which deployments improve
Cairn upstream); and the **work-intent tool** (an executable collision-avoidance
primitive realizing the stigmergic coordination of Anchor 5).

**The honest value curve, grounded.**  Cairn *adds friction before code* and pays
it back later -- in less rework, fewer forgotten decisions, fewer agent
collisions, and fewer unreviewed scientific changes.  This is an evidence-based
bet, not an aspiration (**Anchor 11**):

* *Raw AI speed is partly illusory.*  METR's randomized controlled trial -- METR
  (2025), *Measuring the Impact of Early-2025 AI on Experienced Open-Source
  Developer Productivity*, [arXiv:2507.09089](https://arxiv.org/abs/2507.09089)
  -- found experienced developers working on their own mature repositories were
  **19% slower** with early-2025 AI tools, while believing they were ~20%
  *faster*.  Closing that perception-vs-reality gap with a recorded, reviewed
  process is exactly the friction Cairn front-loads.
* *The expensive errors are the late ones.*  The cost-of-change literature --
  Boehm, B. (1981), *Software Engineering Economics*, Prentice Hall; Boehm, B. &
  Basili, V. (2001), *Software Defect Reduction Top 10 List*, IEEE Computer --
  holds that defects cost more the later they are caught.  The magnitude is
  contested (Bossavit, L., *The Leprechauns of Software Engineering*, argues the
  classic 100:1 multiplier is weakly evidenced and nearer 5:1 for small,
  noncritical systems), so Cairn leans on the *direction* -- catch it in review,
  not in production -- not on a multiplier.

Stated as the product promise (Codex's adopter-friction audit,
`dev/strategy/archive/2026-05-27-codex-cairn-adopter-friction-audit.md`): *"Keep the
apparatus only as heavy as your codebase and team earn."*  This candor is
load-bearing, not a caveat -- it is what lets a lone scientist + one agent start
at the kernel and deepen only as the project earns it, and it is the premise of
the maturity-ladder direction below.

## Cairn as a publishable artifact

Cairn is **repo-first**: a forkable, DOI-bearing repository gets *adopted* where
a paper gets *cited*.  It is largely an *extraction and generalization* of
doctrine proven in use, and -- carrying a DOI via a release plus a
`CITATION.cff`, dual-licensed (CC BY for prose / templates, a permissive license
for scripts) -- it is itself a citable Open Science artifact independent of any
paper.

**The two-case comparison is the evidence spine.**  modflow_tools (AI-team-first)
and LHM (a long-lived, majority-MATLAB, majority-untested landscape-hydrology
model retrofitted under the same maintainer) are a before/after on each side, not
"apparatus vs. none": LHM's baseline is its pre-adoption ad-hoc state, and its
treatment is the modflow_tools apparatus *deliberately adapted* for a large, old,
multi-language legacy codebase.  What the pair shows:

* **What generalizes vs. what is project-specific accretion.**  Generalizes
  near-verbatim: the proposal/plan lifecycle, append-only deliberation, the
  Internal/External review tiers and structural-independence floors, stigmergic
  artifact coordination, the shared-communication-file discipline.
  Context-driven additions with no greenfield equivalent: the Legacy Agent,
  domain-specialized agents, the surface-readiness ledger, the MATLAB-first
  dual-language test architecture, bounded port stewardship.
* **The retrofit role the framework predicts, instantiated.**  modflow_tools,
  AI-team-first, deliberately has no Test/Doc agent; LHM, retrofit-on-legacy,
  needs a standing Legacy Agent -- G3's built-from-scratch-vs-retrofit
  distinction, with a concrete case on each side under one maintainer.
* **Role-design and independence variants.**  LHM splits agents by *domain*
  (Inputs / Model / Postprocess) where modflow_tools splits by *lifecycle stage*
  (Strategy / Implementation); LHM's domain agents cross-review one another, so
  structural independence comes from domain-rotation, not only agent-type
  difference (extending G6 / G16).
* **The surface-readiness ledger** -- a Ready / Transitional / Frozen tiering of
  every code surface: both a safety interlock and a *measurable* human-only ->
  human+AI transition metric.

**Positioning.**  The audience is **scientists building scientific-computing
software** -- not software-engineering generalists or agentic-framework builders
-- who care about rigor, reproducibility, and review discipline; the methodology
was developed by a scientist on scientific software, an authentic and
underserved niche.  Cairn does not pitch `AGENTS.md` (now a cross-vendor
standard) or spec-driven-development tooling (crowded); it leads with the two
differentiators above, and The Turing Way is its model for adoptability (a
template repository, a quickstart, a piecemeal-adoption path).  **If a paper is
ever written** it is optional amplification -- a short arXiv preprint (cs.SE)
pointing at the DOI'd repository; JOSS does not fit (it reviews research
*software*, not a methodology) -- and its skeleton already exists here: the
framework anchors as related work, the two case descriptions, the Cluster C
contributions, and the forward directions as future work.

## Trust as design center

The closer Cairn comes to recruiting outside adopters, the more
unusual the trust ask becomes: not just "use this tool" but **"commit
this load-bearing apparatus to your git history, give AI agents
read/write authority on the repository that holds your science, and
let the apparatus shape how your team deliberates."**  The adoption
decision is therefore a *trust decision* -- larger than adopting a
library, smaller than joining a religion.  Cairn earns or loses
that trust by structural choices, not by marketing.

**Anchor 10's TRUST principles** (Lin et al. 2020) name five
dimensions of trustworthy infrastructure operation.  All five map
onto Cairn's existing doctrine:

* **Transparency** -- every decision lives in a public,
  append-only deliberation record (`dev/proposals/archive/` +
  `dev/plans/archive/`).  Every load-bearing claim cites where it
  came from (the verify-before-asserting discipline, the
  claim-check infrastructure).  Anti-scope is explicit (this
  doc's final section names what Cairn deliberately does not do).
* **Responsibility** -- two dogfooded case studies (modflow_tools
  + LHM) carry the apparatus through real work.  A pre-release
  sweep gates every cut.  The `verify_integrity.py` fail-closed
  guarantees catch the failure modes the doctrine warns about.
  Cairn does not ship doctrine it has not exercised.
* **User focus** -- the on-ramp's three graduated adoption
  levels + the adopter-friction package + the progressive-
  onboarding architecture + the heterogeneous-workflow design
  (the maintainer is one user among many; multi-user is the
  design center).  The adopter chooses their depth; the apparatus
  only as heavy as the project earns.
* **Sustainability** -- dual CC BY 4.0 + MIT license + no vendor
  lock-in + no-telemetry default + the community-mode horizon.
  Adoption is reversible; nothing about adopting Cairn commits
  the team to anything they can't exit.
* **Technology** -- no-network-by-default composition, the
  export-safety scrub, the `content-security` module, the
  trust-boundary doctrine (own runs trusted; colleague-supplied
  artifacts user-controlled).  The infrastructure does not
  silently exfiltrate.

**Where the existing architecture is strong**: public deliberation;
vendor-neutrality (Anchor 13); the security four-layer model + verify_integrity;
the explicit Anti-scope.  Anchor 3 (Steinmetz TCMM) covers the
AI-system-trustworthiness side; Anchor 4 (Bridgeford / Nature CS)
covers the risk-side of AI-assisted science; Anchor 6 (peer
review) covers institutional trust; Anchor 8 (FAIR4RS) covers the
external-reuse contract.  Anchor 10 (TRUST) is the surface that
names what those five existing anchors add up to from the
infrastructure-operation lens.

**Where it still has work to do**: Cairn pre-public-flip has only
N=2 case studies (modflow_tools + LHM); Anchor 10's Responsibility
dimension is lightly evidenced until a third-party adoption lands.
The Software Sustainability Institute's "Trusted by design"
framing (Sirmpilatze, FOSDEM 2026) names the
social-foundations-of-trust gap directly: mission/scope clarity,
reasonable first release + consistency, radically open
communication.  Cairn's case studies + the public deliberation
record cover the first two; the third (open communication outside
the modflow_tools / LHM authorship pair) is what the public flip +
community-mode horizon directly address.

### Recipient-calibrated communication and the comprehension floor (Anchor 16)

**Review is Cairn's whole engine, and opaque language quietly switches it off: you cannot review what you cannot penetrate, so "review and decide" collapses into "approve."**  Comprehension is therefore not a courtesy the agent extends to the human -- it is a **precondition of the human's authority**.  A Maintainer who does not understand a change cannot legitimately decide on it; they can only rubber-stamp it.  Calibrating communication to the recipient, and confirming it landed, is thus load-bearing for the lifecycle, on the same footing as structural independence.  The anchor has two legs.

**Leg 1 -- calibrate to the recipient, and check that it landed.**  Four converging literatures:

* **Recipient-designed explanation** -- Miller (2019), *Explanation in artificial intelligence: insights from the social sciences* (Artificial Intelligence 267:1--38; doi:10.1016/j.artint.2018.07.007): human explanation is selective and tailored to the listener (contrastive, social), not exhaustive.  An agent that dumps everything it knows is transcribing, not explaining.
* **The right level depends on expertise, and must move with it** -- Kalyuga (2007), *Expertise Reversal Effect and Its Implications for Learner-Tailored Instruction* (Educational Psychology Review 19:509--539): instructional support that helps a novice actively *harms* an expert (redundant detail becomes cognitive-load cost), and the reverse.  There is no one-size explanation.  Cairn adopters span no-software-background to senior engineer, and a single Maintainer's level varies by subsystem -- so the agent calibrates per person and per topic, and recalibrates as understanding grows.
* **Comprehension is built and verified, not assumed** -- Clark & Brennan (1991), *Grounding in communication* (in *Perspectives on Socially Shared Cognition*, 127--149): mutual understanding is *grounded* turn by turn, the listener signalling understanding and the speaker confirming.  The agent owns the grounding -- it checks the human is still with it, rather than reading the silence after a wall of jargon as assent.
* **When this fails, the human over-relies** -- the appropriate-reliance literature (e.g. *Knowing About Knowing: An Illusion of Human Competence Can Hinder Appropriate Reliance on AI Systems*, arXiv:2301.11333; *In Search of Verifiability: Explanations Rarely Enable Complementary Performance in AI-Advised Decision Making*, arXiv:2305.07722): fluent explanations can *increase* over-reliance and manufacture an *illusion of understanding*; genuine complementary performance needs **verifiability**, not a plausible-sounding story.  This is the empirical shape of the rubber-stamp.

**Leg 2 -- plain explanation is also a test of the explainer's own understanding.**  The discipline cuts both ways.  For humans this is well established: the **illusion of explanatory depth** (Rozenblit & Keil 2002, *The misunderstood limits of folk science: an illusion of explanatory depth*, Cognitive Science 26:521--562) -- people are confident they understand a bicycle or a zipper until asked to explain it step by step, at which point the understanding collapses.  Explaining plainly *tests* understanding; it does not merely deliver it.  **The same is plausibly true of AI** -- stated honestly as a well-motivated extension, not a settled result: a model can produce fluent, confident jargon that pattern-matches expertise without a correct, grounded claim beneath it, and the jargon then *shields* that claim from scrutiny -- the human's and the model's own.  This makes the plain-language requirement a **correctness check on the explainer**, not only a service to the reader, and ties it to Cairn's existing `verify-before-asserting` discipline (Anchor 3's Bias & Robustness leg): jargon can hide an unverified assertion; plain words expose it to challenge.

**Worked example (the origin case).**  This anchor surfaced from a real comprehension failure during the six-proposal superplan.  The package-splitting work leaned on "AST source-motion attestation" -- opaque enough that the Maintainer had to look the term up separately, then reverse-engineer the implementing agent's function names and outputs to follow it.  In plain terms the claim was simply: *"we used Python's own structured representation of the code (its abstract syntax tree) to prove every function moved exactly once when the oversized package was split -- nothing lost, nothing altered."*  The plain version is not less precise -- it is more reviewable.  And the jargon's cost was not merely slower reading: it left the Maintainer unable to *review* the work, because the opaque surface was the only window onto it.  The thesis, in miniature.

**The Cairn contribution / divergence.**  The XAI and reliance literatures study AI-to-human explanation largely in *decision-support* settings (a model advises; a human accepts or overrides).  Cairn's setting differs: a **recorded-deliberation lifecycle** in which the human must understand in order to *legitimately decide and sign*, on a durable, reviewable record.  So Cairn does what the source literatures do not -- it makes the **comprehension floor a reviewable property of the lifecycle**, the same move that turned reviewer independence into a structural, checkable tier (G16).  "Did the human actually understand what they decided?" becomes a first-class question, not an afterthought.  Stated reflexively: this anchor was itself produced by the failure mode it names -- a jargon-dense stretch that degraded the Maintainer's review -- which is exactly the incident-grounded evidence the doctrine-evolution gate asks for.

**Surfaced direction -- G17: communication calibration -- a universal norm now, a dimension on the evidence.**  Anchor 3's *Usability* dimension was flagged unmeasured (G7); this is where it gets watched -- two parts, deliberately at different maturity.

* **Settled -- the universal norm.**  Lead plain, keep precision beneath, and treat *"I don't understand this yet"* as a **mandatory pause**: a decision surface the Maintainer cannot follow is not decidable.  Every adopter, always.
* **Observed -- heading toward a dimension.**  Treat communication calibration as its own Cairn axis (distinct from the *programming-language* axis), tuned to the reader's register -- *domain* proximity and *software* proximity.  This is **not imagined enrichment**: it is an **origin-deployment design note from real maintainer usage** (it surfaced this very session), evidence-status *observed-here, not yet externally replicated* -- the same footing the project's `deliverable` / product axis arose on.  Adopt an **existing** controlled-language grammar rather than invent one -- *Simplified Technical English* (ASD-STE100), *Attempto Controlled English*, the *Federal Plain Language Guidelines* -- so calibration is by language-*class* (undefined acronyms, nominalizations, dense embedding, abstraction-without-instance), not ad-hoc word-banning.

Two guards answer the real risks: the calibration is a **dynamic starting register, not a fixed label** -- grounding (Clark & Brennan) adjusts it turn-by-turn, so it neither ossifies nor profiles; and its evidence ledger is **score-free** -- language-*classes*, never the person.  One invariant holds throughout: **guarantee a plain layer, never strip precision** -- the record stays exact, the plain layer sits on top.  Building it (the axis's grades, the rubric, the chosen grammar) is the follow-on, gated on the next bet (a third-party adopter); the bearing -- and its origin in real use -- is fixed here.

### The trust paradox of empirical-data infrastructure

An upcoming near-term move (below) ships **per-project efficacy-
data collection**: every Cairn deployment gathers its own data on
framework efficacy locally, with no telemetry, no auto-upload, no
central server.  *Adding this infrastructure requires more trust
than not adding it*: even with data staying local, an adopter has
to trust that the collection itself doesn't introduce a
surveillance vector, that the eventual out-of-band outreach for a
research paper respects consent, that participation is per-occurrence
opt-in (not inferred from data existence), and that the data
won't be used to evaluate or embarrass the adopter project.

**Trust architecture comes first** -- consent flow + data
audit-trail + no-network composition by default + clear "what is
collected + what is not" doctrine -- before the data primitive
itself.  Never the reverse.  The five TRUST dimensions are the
checklist: every Anchor-10 box must be demonstrably checked
before the primitive ships.  The paradox dissolves when the
infrastructure proves its trustworthiness in five dimensions
before adopters are asked to commit to it.

### The durable neutral coordination layer (Anchor 13)

Cairn's "no vendor lock-in" and "vendor-neutrality" (above) are usually
stated as *features*.  They are better understood as one **architectural
principle** with a real literature -- and that same principle grounds a
second neutrality the framework had not named: **stack-neutrality**, the
commitment that the methodology binds the adopter to a programming-language
stack no more than it binds them to an AI vendor.

**Anchor 13 -- the hourglass / narrow-waist model.** *Beck, M. (2019). "On
the Hourglass Model." Communications of the ACM 62(7): 48-57.
[doi:10.1145/3274770](https://dl.acm.org/doi/10.1145/3274770).  With Akhshabi,
S., & Dovrolis, C. (2011). "The Evolution of Layered Protocol Stacks Leads to
an Hourglass-Shaped Architecture." Proc. ACM SIGCOMM 2011, 206-217.
[doi:10.1145/2018436.2018460](https://dl.acm.org/doi/10.1145/2018436.2018460);
the end-to-end principle (Saltzer, Reed & Clark 1984) as the companion.*

The model is most recognizable from a system every modeler already relies on.
MODFLOW's input/output file formats are a deliberately **simple, stable
interface** -- a "waist" -- between two layers that change at very different
rates.  *Below* the waist the solver evolves (MODFLOW-2005 -> MODFLOW 6 ->
parallel backends); *above* it the pre- and post-processing ecosystem evolves
(FloPy, ModelMuse, custom analysis).  Because the file-format waist stays
narrow and stable, the two layers **evolve independently** -- you can replace
the solver without rewriting FloPy, and write a new visualizer without
touching the solver.  Beck's contribution is the design rule behind this: a
waist works *because* it is kept **minimal and weak** -- only what is strictly
necessary -- which is exactly what lets it be implemented on, and
re-implemented for, almost any substrate.  He names the payoff **deployment
scalability**: a thin waist lowers the cost of adoption for everyone above and
below it.  Akhshabi & Dovrolis supply the other half empirically: a successful
waist **ossifies and survives** for decades (IP and TCP on the Internet; the
long-lived scientific data formats in our world) *precisely because* so much
comes to depend on it.  The waist is the durable layer; the diversity lives
above and below.

**Cairn's coordination layer is that waist.**  The deliberation substrate --
plain markdown in a git history -- is about the weakest, most universal
interface available: text under version control.  The model maps directly:

* **Below the waist** -- the adopter's project stack (Fortran, R, Rust, JS,
  Python).  The substrate asks nothing of it.  -> **stack-neutrality.**
* **Above the waist** -- the AI tooling that acts on the deliberation record
  (Claude, Codex, Cursor; the discipline-aid scripts).  The substrate asks
  nothing of it either.  -> **vendor-neutrality.**
* **The waist itself** -- markdown + git -- is the durable asset, kept
  deliberately minimal so neither the tool layer above nor the language layer
  below can capture it.  *That minimalism is the single source of both
  neutralities*; they are not two features but one principle seen from two
  sides.

This also sharpens the companion stack-neutrality assessment
(`2026-06-05-claude-cairn-stack-neutrality`): the *methodology* sits at the
waist and is already stack-independent, while the *Python tooling* sits
**above** the waist -- which is exactly why it can be made replaceable without
disturbing the substrate.  The hourglass predicts that the layer above the
waist is *where* independent evolution is supposed to happen.

**Three honest qualifications.** (1) This is the *principle* applied by analogy,
not a claim that Cairn is a network protocol -- the same analogical move the
peer-review anchor (Anchor 6) makes.  (2) Ossification cuts both ways: a waist
that succeeds becomes *hard to change*.  For Cairn that is mostly the point --
a stable coordination substrate is what you want -- but it is a deliberate
trade, not a free lunch: once a community's deliberation lives in markdown +
git, the substrate is as committed as a model is to its file formats.  The
*replaceable* part is the tooling above; the waist is the part you choose to
ossify.  (3) Vendor- and stack-neutrality are *siblings in principle, not in
maturity*: vendor-neutrality is enforced **today** -- free (markdown
discipline), lint-gated -- while stack-neutrality of the *tooling* is still
aspirational and costly (a Python reference implementation plus
run-it-in-Python docs today; a different-language implementation only if an
adopter builds one from the project's inherent specs).  The shared waist is the
principle; the distance each has travelled is not the same.

## Where Cairn is headed

These are **grounded horizons, not commitments** -- the anti-scope at the end
binds, and each goes through the normal Cairn PR-flow / proposal cycle before
shipping.

**The open empirical work.**  The highest-leverage near-term move is to build the
**lifecycle-metrics time series** across commits -- the tooling and a baseline
snapshot exist, but the trend does not -- so the team's claims about its own
discipline ("External review catches what the author can't"; "revision counts
fall as doctrine matures") become *measurements* rather than assertions.  Two
measurement gaps ride on it: **reviewer-pool diversity** (does the current small
agent corpus systematically miss particular finding-classes?) and a
**coordination-failure taxonomy** (industry reporting attributes a large share of
multi-agent failures to coordination/orchestration; Cairn has countermeasures but
no measurement of them).  A separate live operational question -- whether
modflow_tools' own contended tree warrants **sharded PLANNING** -- sits in the
same measurement bucket; the work-intent tool already mitigates the staged-index
hazard that raised it.

Two horizons follow.

<!-- claim-check-allow: templates/core/, templates/modules/, dev/cairn-lock.yml -->

### Horizon 1 -- community-maintained scientific software

Anchors 1-6 and the `dimensions/` model all assume a **small, co-located
team under one maintainer**: both worked cases (modflow_tools, LHM) are
single-maintainer projects, and the `human-team` dimension tops out well
short of a distributed contributor community.  Community-maintained
scientific software is a *distinct governance regime* the framework does
not yet cover.  Three verified anchors bound it (all confirmed via search
2026-05-27, not cited from memory):

7. **The maintenance-burden thesis + a project typology** -- Eghbal, N.
   (Asparouhova, N.) (2020). *Working in Public: The Making and Maintenance
   of Open Source Software.*  Stripe Press.  ISBN 978-0-578-67586-2.  Two
   load-bearing ideas: (a) the dominant cost of modern open source is
   *maintenance*, borne by a few (often solo) maintainers, not the initial
   build; and (b) a typology of projects by the ratio of **user growth to
   contributor growth** -- *toys* (low/low), *clubs* (high contributors /
   low users), *stadiums* (high users / few contributors), *federations*
   (high/high; e.g. Linux, Rust, Node.js).  This typology is the natural
   axis for "Cairn modes": the apparatus a project needs is a function of
   *where it sits* in this space, and the failure mode of a *stadium*
   (millions of users, a handful of overloaded maintainers) is exactly the
   one AI-agent collaborators are positioned to absorb.
8. **The external reuse contract** -- Barker, M., Chue Hong, N. P.,
   Katz, D. S., et al. (2022). *Introducing the FAIR Principles for
   research software.*  *Scientific Data* 9:622.
   [doi:10.1038/s41597-022-01710-x](https://www.nature.com/articles/s41597-022-01710-x).
   The FAIR4RS principles adapt Findable / Accessible / Interoperable /
   Reusable to software as a first-class digital object (executable,
   composite, continuously versioned).  Where Eghbal describes the
   *internal* sustainability problem, FAIR4RS fixes the *external* contract
   a community-maintained scientific project owes its drive-by contributors
   and downstream reusers -- citation, versioning, dependency declaration,
   archival.  A Cairn community mode should aim to leave a project
   FAIR4RS-conformant *by construction* (Cairn already ships `CITATION.cff`
   + a release cadence; the move is to generalize that into the community
   contract).
9. **The scientific-software-specific open-development playbook** --
   Prlić, A., & Procter, J. B. (2012). *Ten Simple Rules for the Open
   Development of Scientific Software.*  *PLOS Computational Biology*
   8(12):e1002802.
   [doi:10.1371/journal.pcbi.1002802](https://doi.org/10.1371/journal.pcbi.1002802).
   The closest prior art to what a Cairn community mode must encode:
   develop in the open from day one, lower the barrier to contribution,
   automate tests, document for contributors not just users, and establish
   light governance early.  It is the scientific-domain bridge between
   Eghbal's general-OSS lens and this framework's scientist-maintainer
   audience.
10. **Trustworthy operation, complementary to FAIR** -- Lin, D.,
    Crabtree, J., Dillo, I., et al. (2020). *The TRUST Principles for
    digital repositories.*  *Scientific Data* 7:144.
    [doi:10.1038/s41597-020-0486-7](https://www.nature.com/articles/s41597-020-0486-7).
    Five guiding dimensions for the trustworthiness of data
    infrastructure: **T**ransparency, **R**esponsibility, **U**ser
    focus, **S**ustainability, **T**echnology.  Explicitly
    complementary to FAIR (Anchor 8) and published in the same
    journal (Nature Scientific Data): where FAIR governs the
    external-reuse contract for the artifact, TRUST governs the
    operational trustworthiness of the infrastructure that holds it.
    The five dimensions generalize cleanly from data repositories
    to research-software-methodology frameworks like Cairn -- naming
    the trust surface an adopter weighs when deciding whether to
    commit a methodology framework to their repository, give AI
    agents read/write authority on it, and let it shape how their
    team deliberates.  Anchor 10 is the framework Cairn's design
    has been implicitly following; the "Trust as design center"
    section below names it.

### The concept -- Cairn modes for community-maintained scientific software

The proposal is a **new adaptive axis** for Cairn's `dimensions/` model:
**governance regime**, running *solo-maintainer -> small team ->
community / federation*.  As a project moves rightward on Eghbal's
typology, the apparatus changes shape -- and most of Cairn's existing
doctrine already has a community-mode analog waiting to be drawn out:

* **Contributor onboarding + the contributor->maintainer pipeline.**  A
  solo project needs none; a community project needs `CONTRIBUTING.md`,
  drive-by-PR triage, a labeled good-first-issue surface, and an explicit
  path by which a repeat contributor earns commit / review standing.  Cairn
  has the *capture* surfaces (GitLab-issue doctrine, the User Agent role)
  but not the *graduation* mechanics.
* **Distributed, asynchronous review with an external reviewer pool.**  The
  **Dual-Review model** already assumes structural independence; community
  mode generalizes the External Reviewer from "a different agent type" to
  "a rotating pool of external human + AI reviewers."  This directly attacks
  the open G15 reviewer-diversity gap -- a community is *how* the reviewer
  pool grows past N=2.
* **Maintainer sustainability as the design center.**  Eghbal's thesis is
  that the binding constraint is *maintainer attention*, not contributor
  supply.  The Cairn-native move -- and the genuinely novel contribution --
  is **AI agents as maintenance-load absorbers**: triage, first-pass review,
  doc-drift repair, dependency hygiene, and the fold-back channel all run as
  standing agent work so the human maintainer's scarce attention is spent on
  judgment, not throughput.  A *stadium* project (Eghbal) staffed by a solo
  maintainer + a disciplined agent team is the case Cairn is uniquely shaped
  to serve.
* **AI agents as first-class community contributors -- governed.**  The
  hardest and most original sub-problem: a community-maintained scientific
  project where *some contributors are AI agents* operating under the
  doctrine.  How are agent-authored PRs attributed, reviewed, and trusted
  when the contributor pool is open?  How does the work-intent /
  staged-index discipline extend past a single working tree to many forks?
  This is uncharted in all nine anchors and is the clearest candidate for a
  Cairn-native research contribution.
* **The FAIR4RS external contract, by construction.**  Community mode folds
  the FAIR4RS obligations (citation, semantic versioning, dependency
  declaration, archival DOI) into the installable templates so a Cairn
  deployment is reuse-ready and citable from its first public release.

**Why this motivates Cairn's future directly.**  Cairn is *itself* becoming
an Open Science repository -- the moment it is pushed public it stops being
a solo-maintainer artifact and becomes a community-maintained project, the
exact regime this axis describes.  So Cairn must **dogfood its own community
mode**: its reference deployment shifts from the solo modflow_tools case to
*Cairn governing its own contributor community*.  That is both the strongest
possible worked example and a forcing function -- Cairn cannot credibly ship
a community mode it does not run on itself.

### Reframing the governance axis for scientific software

(Folded 2026-06-05 from an LHM-deployment fold-back review.) The axis above keys
on Eghbal's *user/contributor-growth* typology -- a sound general-OSS lens, but
the wrong *primary* for science, whose governance reality is dominated by three
properties it does not see. **Keep Eghbal as one input and supplement it:**

* **Stewardship / succession (the primary reframing)** -- will the software
  outlive its authors? Most scientific software is succession-fragile (the solo
  grad-student artifact; the PI-lab with 2-5 yr student turnover), and Cairn's
  deliberation record + readiness map are *exactly* succession infrastructure --
  a stronger latent value than contributor-onboarding mechanics. The governance
  question for science is less "how many contributors" than "how does knowledge
  survive personnel turnover."
* **Criticality** -- exploratory <-> mission-critical, which drives rigor
  *independently of team size*: a one-person LIGO-class pipeline (a bug = a false
  detection) needs heavier apparatus than a fifty-person exploratory project.
* **Coordination locus** -- shared-codebase <-> artifact/protocol-handoff. Cairn's
  stigmergy already lives on the artifact-handoff side, so it is *natively* shaped
  for the protocol-conformance regime (CMIP: dozens of independent modeling centers
  conforming to a shared experiment protocol + output format, no shared codebase)
  -- an under-claimed strength.

Two exemplars are gifts to existing theses. **USGS / MODFLOW** releases software
under *Fundamental Science Practices* mandating **two reviews -- a code review and
a domain review** -- plus center-director sign-off: the **Dual-Review model already
operating in agency-stewarded science**, whose *domain review* is exactly the
agent-side scientific-error check **G11** calls missing (the move is to make part
of it apparatus-run, not to invent it). That the ecosystem modflow_tools wraps is
governed this way puts the whole modflow_tools/LHM stack *downstream of an
agency-steward governance model*. And **NumPy NEP / Astropy APE** are
commit-mediated decision lifecycles -- Cairn's proposal lifecycle at federation
scale -- while **LIGO / CESM** are the upper-rigor anchors the Horizon-2 maturity
ladder needs to argue "deepen as you earn it" [Anchor 14].

**Anchor 14** (governance exemplars, verified 2026-06-05): USGS *Fundamental
Science Practices* + IM OSQI 2019-01 (two-review software release); NumFOCUS
sponsorship + NumPy NEP / Astropy APE / Python PEP 13 governance; CESM
Scientific-Steering-Committee governance; LIGO blind / hardware-injection
validation (arXiv:1612.07864); CMIP/CMOR protocol coordination (Eyring et al.
2016, *Geosci. Model Dev.* 9:1937-1958, doi:10.5194/gmd-9-1937-2016).

### The scientific-character dimension -- the `deliverable` axis

The axis above asks *how a project is governed*; this orthogonal one asks *what
science it is on the hook for*, and it answers the standing **audience/apparatus
gap**: Cairn claims an audience of "scientists building scientific-computing
software," yet nearly everything it ships is *science-agnostic* SE rigor. The
genuinely scientific content is thin -- Anchor 4 (borrowed) and the open **G11**.
(Raised 2026-06-05 by an LHM fold-back review; the axis is on **LHM's Cairn
fold-back ledger** and prototypes LHM-first.)

The fix is Cairn's **first domain-flavored dimension** (the existing six are
generic): **`deliverable`** -- *"what is the project epistemically on the hook
for?"* (chosen over `epistemic-role` for legibility; the epistemic question, not
a PM milestone). It is **character-valued**: scientific software has recurring
characters -- *process-simulation model* · *tooling / wrapper* · *numerical
library* · *data-reduction pipeline* · *analysis / last-mile* · *inverse /
calibration / UQ* · *coupled / multiphysics* · *instrument / viz* (refining the
research-software-category literature [Anchor 15]) -- each mapping to a **preset
of science-disciplines**: physical/domain-validity (PV), numerical-tolerance
(NT), provenance (PROV), coupling-contracts (COUP), exactly as the six dimensions
map to module presets.

The worked **N=2** is the body's retrofit pair. **modflow_tools** is mostly
`tooling` but genuinely *multi-character* -- also a visualization / model-review
code, and wraps PEST++/pyEMU (`inverse`) -- which is the point: a real project
spans characters. **LHM** is `model` + `coupled`, the first adopter whose
correctness includes science *the code itself produces*. That asymmetry is why
the disciplines prototype LHM-first and only the proven core folds up
(prove-then-fold -- the Anchor-13 maturity-asymmetry caveat, applied to a
dimension). It also feeds the trust model: G11's finding that *scientific
validity routes wholly through the human maintainer* is the verification-owner
bottleneck, and the PV/NT/PROV disciplines -- with USGS's domain review as the
proof-of-concept -- are how some of it moves into the apparatus.

**Anchor 15** (the science-disciplines' canon, verified 2026-06-05): Hasselbring
et al. (2024), *Toward Research Software Categories*, arXiv:2404.14364, with Eisty
& Carver (2022), *Testing research software: a survey*, *Empirical Software
Engineering*, doi:10.1007/s10664-022-10184-9 (the taxonomy + testing basis);
Oberkampf & Roy (2010), *Verification and Validation in Scientific Computing*,
Cambridge UP, ISBN 9780521113601, with Roache (2002), *Code Verification by the
Method of Manufactured Solutions*, *J. Fluids Eng.* 124(1):4-10,
doi:10.1115/1.1436090 (the verification-vs-validation distinction + MMS, under the
validation-regime idea); W3C **PROV-DM** (2013) + Sandve et al. (2013), *Ten
Simple Rules for Reproducible Computational Research*, PLOS Comp. Biol.
9(10):e1003285, doi:10.1371/journal.pcbi.1003285 (the PROV discipline).

### Horizon 2 -- a self-instrumenting maturity ladder

Orthogonal to the governance-regime axis but sharing its root insight: **Cairn
should guide an adopter to *deepen* its apparatus as project complexity rises,
rather than asking it to guess the right depth up front.**

Cairn v0.2 ships the **static half**: the `on-ramp/` defines three graduated
levels (read-the-doctrine → hand-copy the kernel → full bootstrap), recommends a
starting level from the dimensional profile, and states that a project can move
up. What is missing is the **dynamic half** -- the recommendation is made *once,
at install, from a static snapshot*, and nothing then watches the *live*
deployment to signal *when* a project has outgrown its level. The failure mode
cuts both ways: a Level-1 project that grows into a multi-agent, safety-critical
system silently re-accretes every failure the deeper apparatus prevents (drift,
lost deliberation, shared-blind-spot review, staged-index collisions); an
over-installed project carries ceremony it never needed.

The proposal: **extend the on-ramp from a static install-time recommendation
into a self-instrumenting one** -- Cairn ships metrics + heuristics that observe a
live deployment (the lifecycle-metrics layer, collision log, intent log, commit
cadence, contributor count -- data it already produces) and *recommend* when to
move up a level or promote a module. Several such triggers already run here as
one-off internal rules (the R2 collision window; rising review/revision counts;
concurrent-agent count; a project acquiring a safety/data-loss surface;
contributor growth past the solo regime); the move is to package them as
portable, adopter-facing guidance delivered through Cairn's lockfile-aware
**upgrade** path -- *recommend, not impose*, the same posture as the
adaptive-doctrine rate-limit gate. Its honest framing (Codex's adopter-friction
audit): *"keep the apparatus only as heavy as your codebase and team earn"* -- a
methodology that signals *when* to deepen can also say *you do not need this
depth yet*.

The novel step is narrow: methodology frameworks (the Turing Way, the *Ten Simple
Rules* papers, FAIR4RS) are *static prose* -- none watches your repository and
tells you when you have outgrown your setup; even TCMM (Anchor 3) scores an AI
system's trustworthiness, not a deployment's depth. This turns the `dimensions/`
model from *statically-profiled* axes into *continuously re-observed* ones, and
is the natural consumer of the still-open **empirical time-series** work (R1 /
G7) -- the triggers need a *trend*, not a snapshot.

### Near-term moves

Each goes through the normal proposal cycle before shipping; the detail lives in
each proposal, not here:

* **Governance-regime axis** (Horizon 1) and **self-instrumenting maturity layer**
  (Horizon 2) -- each a Cairn proposal adding a new `dimensions/` axis / the
  trend-driven on-ramp extension over the lifecycle-metrics / collision / intent
  data.
* **Governed AI-community-contributor scope** -- the agent-authored-PR /
  cross-fork work-intent sub-problem Horizon 1 opens (the candidate Cairn-native
  contribution none of the anchors describe).
* **Cairn as its own community-mode case study** -- dogfooding Horizon 1; gated on
  the public-flip decision.
* **The LHM operating case** -- carry LHM from adopted to *operating*, then a
  measurement pass across both projects.
* **Adopter first-use friction** -- the pre-0.3 friction package (Codex's audit);
  tracked in `dev/PLANNING.md`.
* **Per-project efficacy-data infrastructure** (pre-0.4/0.5) -- a
  privacy-by-design, stays-local primitive (no telemetry / no auto-upload /
  per-occurrence opt-in) for deployments to collect their own efficacy data,
  **gated on the consent / audit-trail / no-network-by-default trust architecture
  landing first** (each Anchor-10 TRUST dimension checked before it ships). Detail
  in its own proposal.

### Horizon 3 -- the apparatus's context budget (token efficiency)

Cairn's apparatus *is* an always-loaded context surface: `AGENTS.md` +
`RULES.md` + the vendor wrapper are read into **every** agent's context on
**every** session.  That surface has a cost the framework has so far argued
only loosely (cheaper / faster).  Anchor 12 grounds it on a stronger
footing -- correctness, not only cost.

12. **Agentic context efficiency / "context rot"** -- *Context Length Alone
    Hurts LLM Performance Despite Perfect Retrieval* (EMNLP 2025).
    [arXiv:2510.05381](https://arxiv.org/abs/2510.05381).  Accuracy degrades
    as input length grows **even at 100% exact-match retrieval** -- so a fat
    always-loaded prefix makes an agent *less accurate*, independent of
    cost.  Foundational corroboration: Liu, N. F., et al. (2024), *Lost in
    the Middle: How Language Models Use Long Contexts*, *Transactions of the
    ACL* 12, [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
    (position-dependent degradation).  The practitioner discipline that
    operationalizes the response is **"context engineering"** (Anthropic,
    2025): curate the optimal always-loaded token set at every inference
    step; treat context as a finite *attention budget* every token depletes;
    disclose **progressively** -- load the router / names always, the bodies
    on demand.  An industrial replication across 18 frontier models corroborates
    the length effect (Chroma, *Context Rot*, 2025 -- a vector-DB vendor, so
    weigh the result against that interest; it is offset by the independent
    academic work above).  Two further facts the argument below leans on, each
    multi-vendor or independently sourced: prompt-cache reads are cheap while
    cache *writes* carry a premium (≈1.25-2× base) and a stable-prefix-first
    load order preserves cache hits (documented in both Anthropic and OpenAI
    caching docs); and on-demand retrieval is not free reliability -- one
    independent test across 4,027 tools measured deferred-retrieval accuracy at
    only ~55-64% (Arcade).  *(Synthesized June 2026 via a deep-research pass
    over ≈25 sources with adversarial claim-verification; the primary sources
    are cited inline above, so this anchor stands on its own when this doc
    moves into Cairn.)*

Three things follow -- two of them the **framework's own contribution**, where
it leads the literature rather than borrows from it (as at G3 / G4 / G12):

* **Lean is a *correctness* property, not only a cost one.**  The earlier
  "faster / cheaper" framing undersold the case: an over-stuffed
  always-loaded doctrine surface does not merely cost cache-write tokens, it
  *degrades the agent's accuracy*.  This is the empirical backbone under the
  **adoption promise** ("keep the apparatus only as heavy as your codebase
  and team earn") and under the `RULES.md`-as-router design now landing in
  the modflow_tools Cairn adoption: a small always-loaded bright-line set + a
  routing table to on-demand docs *is* progressive disclosure, and the
  maturity ladder (Horizon 2) is its **profile-sizing** control.
* **A governed, measured always-loaded token budget is a Cairn lead.**  The
  literature supplies the measurement primitives (≈100 tokens per skill;
  the finite-attention-budget framing) but **no surveyed source describes a
  governed, measured always-loaded budget as a standing engineering
  control**.  That is the framework's to define -- the same move the
  lifecycle-metrics layer makes for the review process, applied to the
  apparatus's own context weight.
* **The `sessions × agents × adopters` fan-out is a Cairn lead.**  All
  verified work is single-agent / single-session.  The shared-context
  economics of *one* always-loaded doctrine file read by *many* agents
  across *many* adopters -- the multiplier that makes a heavy Cairn prefix
  expensive at scale -- is unmodeled in the surveyed literature.  Like G12
  (stigmergy), it is a distinctive position worth holding onto as such.

**The caveat -- do not over-minimize (a reliability floor).**  Leanness has a
floor: independent testing measured on-demand / deferred retrieval accuracy
at only ~55-64% in one 4,027-tool study, so an over-stripped router *fails
to trigger the right doc or skill*.  "Minimize the always-loaded surface"
therefore carries a measured floor -- the router must keep enough signal to
route reliably.  This is exactly the tension the `RULES.md` router and the
Cairn module / `dual-review` slots must size as modflow_tools adopts Cairn;
it pairs with the maturity ladder's empirical triggers rather than a fixed
minimum.

## Anti-scope

This guide star is **the agenda, not the authorization**.  Everything under
"Where Cairn is headed" is a candidate direction that needs its own proposal,
review, and Decision before it ships.  In particular, this doc does not by
itself authorize:

* Adding the governance-regime axis or any other new `dimensions/` axis.
* Building the self-instrumenting maturity layer.
* Changing Cairn's role roster, lifecycle, or structural-independence tiers.
* Amending a signed collaboration agreement (which requires a formal amendment).
* Flipping the v0.2.0 tag public, or any other public-surface action -- those
  are maintainer-performed.

Cairn's current structure is organically derived and load-bearing; the horizons
extend it, they do not replace it.  Concrete moves go through the normal Cairn
PR-flow / proposal cycle.
