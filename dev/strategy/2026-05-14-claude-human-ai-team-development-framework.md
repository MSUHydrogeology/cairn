<!-- Migrated 2026-06-12 from modflow_tools dev/strategy/ (Cairn's development home before self-hosting). Authored from modflow_tools' vantage; some path cites and "current state" reflect that origin and are being adapted to Cairn. Preserved as Cairn's living deliberation record -- see dev/strategy/MIGRATION.md. -->
# Cairn -- the guide star: rationale, current state, and direction

**Author**: Claude (Strategy)
**Date**: 2026-05-14
**Status**: living (last major revision 2026-10-01: field-currency pass against the 2026 literature, folding a fresh External assessment; Anchor 22. Anchor 16 updated 2026-10-26 for Cairn Plain Language 1.0)
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

## The promise, and what the evidence supports

*(Settled 2026-10-01, folding a fresh External assessment.)* Stated as sharply
as it can honestly be put, Cairn's promise is: **delegate the coding without
losing control of the scientific assumptions, the evidence, and the
decisions.** Four things carry it, and they are the parts worth defending —
the portable decision record, explanations the scientist can follow,
independent challenge, and restraint. Everything else in this document is a
possibility that waits on evidence.

**Evidence status: plausible, exercised here, awaiting comparative evidence.**
Two cases under one Maintainer demonstrate *use*; they are not independent
evidence that Cairn reduces errors or total human effort. The literature
anchors explain why each mechanism might help; they do not show that this
bundle helps enough to pay for itself. Faster agents make that distinction
more urgent, not less: elaborate process can consume the benefit they offer.

**The serious alternative is not careless prompting.** It is a scientist using
a current coding agent, ordinary version control and tests, a small local
instruction file, and short records for important decisions. That already buys
much of Cairn's portability and reviewability at lower adoption cost. Cairn
earns its place only where its science-specific assurance and decision
discipline make a difference that lighter practice does not.

**What would settle it.** Before any further expansion: one small outside
adoption on real scientific changes, alongside comparable work under the
lighter baseline, with the improvement worth the extra effort declared
beforehand. Record total scientist attention (setup, reading, review,
correction, later resumption); check scientific outcomes against a separately
justified basis; ask whether another person can later reproduce the result and
understand its assumptions; note model and tool versions. Existing artifacts
and a short retrospective, not a new measurement system. The promise is
falsified if the lighter baseline delivers the same scientific reliability and
later comprehension with less attention, or if an outside scientist cannot use
Cairn without sustained help from its author. It is supported by independently
detected scientific mistakes, successful handoffs, and attention saved beyond
setup. Progress in AI should renew this comparison periodically, not add or
remove ceremony on its own.

## Framework anchors

Citable frameworks ground the rationale. The numbering is **canonical and
append-only**: a new anchor takes the next integer and a new row in the index
below, so "Anchor 10" stays unambiguous as the set grows.
As of 2026-10-01, the index contains **22 anchors**.

**Every anchor is introduced where it bites**, with its full citation at that
point. There is no privileged tier. The first six were once set apart because
each carried its own gap-analysis section; those sections have been folded
down (see *What the anchors bound*), and the anchors now sit on equal footing.
That change matters for how this document ages: a living reference should let
new anchors arrive without asking whether they are first-class.

The six that opened the analysis, kept here because later sections cite them
by number:

1. **Interaction taxonomy** -- Treude, C., & Gerosa, M. A. (2025). *How Developers Interact with AI: A Taxonomy of Human-AI Collaboration in Software Engineering.*  Proceedings of the 2nd ACM International Conference on AI Foundation Models and Software Engineering (FORGE 2025).  [arXiv:2501.08774](https://arxiv.org/abs/2501.08774).  Eleven distinct interaction types across the SDLC.
2. **Multi-agent SDLC role design** -- Liu, J. et al. (2025). *LLM-Based Multi-Agent Systems for Software Engineering: Literature Review, Vision, and the Road Ahead.*  ACM Transactions on Software Engineering and Methodology.  [doi:10.1145/3712003](https://dl.acm.org/doi/10.1145/3712003).  Systematic review of LMA applications across SDLC stages.
3. **Trust + governance maturity** -- Steinmetz, S. T. et al. (2025). *The Trust Calibration Maturity Model for Characterizing and Communicating AI Trustworthiness.*  Sandia report SAND2025-00999O.  [arXiv:2503.15511](https://arxiv.org/abs/2503.15511).  Five-dimension maturity model: Performance Characterization, Bias & Robustness Quantification, Transparency, Safety & Security, Usability.
4. **Scientific-software rigor** -- Bridgeford, E. W., Campbell, I., Chen, Z., Lin, Z., Ritz, H., Vandekerckhove, J., & Poldrack, R. A. (2025). *Ten Simple Rules for AI-Assisted Coding in Science.*  [arXiv:2510.22254](https://arxiv.org/abs/2510.22254).  Four-theme framework: problem preparation & understanding; managing context & interaction; testing & validation; code quality assurance & iterative improvement.  Paired with the risk-side anchor: Nature Computational Science (2025), *Threats to scientific software from over-reliance on AI code assistants.*  [doi:10.1038/s43588-025-00845-2](https://www.nature.com/articles/s43588-025-00845-2).
5. **Inter-agent communication patterns** -- two literatures provide complementary lenses:
   * **Cognitive stigmergy / artifact-mediated coordination** -- Ricci, A., Omicini, A., Viroli, M., Gardelli, L., & Oliva, E. (2007). *Cognitive Stigmergy: Towards a Framework Based on Agents and Artifacts.*  In *Environments for Multi-Agent Systems III* (LNAI 4389), Springer.  Crowston, K. *The under-appreciated role of stigmergic coordination in software development.*  Agents coordinate via persistent artifacts in a shared environment; FLOSS / git / issue trackers are canonical software-engineering examples.
   * **Direct agent communication protocols** -- Ehtesham, A. et al. (2025). *A Survey of Agent Interoperability Protocols: Model Context Protocol (MCP), Agent Communication Protocol (ACP), Agent-to-Agent Protocol (A2A), and Agent Network Protocol (ANP).*  [arXiv:2505.02279](https://arxiv.org/abs/2505.02279).  Real-time message-passing protocols dominant in 2025 multi-agent LLM systems; since then ACP merged into A2A (2025-08), MCP and A2A moved under the Linux Foundation's Agentic AI Foundation (2025-12), and every major coding harness shipped native agent-to-agent messaging in early 2026.
   * **Multi-agent debate as a coordination pattern** -- Du, Y., Li, S., Torralba, A., Tenenbaum, J. B., & Mordatch, I. (2024). *Improving Factuality and Reasoning in Language Models through Multiagent Debate.*  Proceedings of the 41st International Conference on Machine Learning (ICML 2024).  [arXiv:2305.14325](https://arxiv.org/abs/2305.14325).  Foundational paper for agents-debate-to-consensus patterns; typically synchronous in implementations.
6. **Scientific peer review as a process model** -- the project's review system has its closest real-world analog not in the multi-agent-debate literature (Anchor 5) but in scientific peer review itself.  Anchored on the peer-review process as codified by editorial-standards bodies (the [ICMJE *Recommendations*](https://www.icmje.org/recommendations/) and the [Council of Science Editors](https://www.councilscienceeditors.org/)), which fix the author / editor / reviewer division of labor, and on the open-peer-review taxonomy -- Ross-Hellauer, T. (2017). *What is open peer review? A systematic review.*  *F1000Research* 6:588.  [f1000research.com/articles/6-588](https://f1000research.com/articles/6-588) -- which classifies review systems by seven openness traits.

Each anchor provides one axis of gap analysis below.  None of the six maps perfectly onto the modflow_tools structure; the mismatches are the interesting part.

### Anchor index (clustered)

All anchors are introduced where they bite, with the full citation at the point
of use. This index fixes the numbering so
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
| **I · AI & multi-agent collaboration** | 1 | Interaction taxonomy (Treude & Gerosa 2025) | "Framework anchors" |
| | 2 | Multi-agent SDLC role design (Liu et al. 2025) | "Framework anchors" |
| | 5 | Inter-agent communication patterns (Ricci 2007; Ehtesham 2025; Du 2024) | "What the anchors bound" > "What the analysis produced" |
| | 11 | AI-productivity value curve (METR 2025; Boehm 1981 / 2001) | "Cairn as a publishable artifact" > "The honest value curve" |
| | 12 | Agentic context efficiency / "context rot" (EMNLP 2025; Liu et al. 2024) | "Where Cairn is headed" > Horizon 3 |
| | 18 | Agent deliberation pathologies (Cemri 2025; overthinking, round-noise, verbosity-bias literatures) | "Restraint as design center" > "The 2026-08 refocus" |
| **II · Trust, governance & coordination** | 3 | Trust + governance maturity (TCMM; Steinmetz et al. 2025) | "Framework anchors" |
| | 10 | Trustworthy operation (TRUST principles; Lin et al. 2020) | Horizon 1 + "Trust as design center" |
| | 14 | Scientific-software governance exemplars (USGS FSP; NEP/APE; LIGO/CESM/CMIP) | "Where Cairn is headed" > "Reframing the governance axis for scientific software" |
| | 16 | Recipient-calibrated communication + the comprehension floor (Miller 2019; Kalyuga 2007; Clark & Brennan 1991; Rozenblit & Keil 2002; appropriate-reliance literature; uncertainty-communication literature; Cairn Plain Language 1.0) | "Trust as design center" > "Recipient-calibrated communication and the comprehension floor" |
| | 19 | The oversight bottleneck and the theory of the firm (Coase 1937; oversight-in-practice + the 2026 OSS maintainer crisis) | "Restraint as design center" > "The 2026-08 refocus" |
| | 20 | The operator's own allocation (Ferster & Skinner 1957; Alter 2017) | "Restraint as design center" > "The human side of restraint" |
| | 22 | The agent supply-chain incident record (Thompson 1984; s1ngularity 2025; Clinejection 2026; "Comment and Control" 2026) | "Restraint as design center" > "Not all weight is waste" |
| **III · Scientific-software rigor & validation** | 4 | Scientific-software rigor (Bridgeford et al. 2025; Nature CS 2025) | "Framework anchors" |
| | 6 | Scientific peer review as a process model | "What the anchors bound" > peer review, not agent debate |
| | 15 | Research-software character taxonomy + V&V / reproducibility canon (Hasselbring 2024; Oberkampf & Roy 2010; Roache 2002; PROV-DM; Sandve 2013; Eisty & Carver 2022) | "Where Cairn is headed" > "The scientific-character dimension" |
| | 21 | Measurement discipline — the retired instruments' inheritance (Rahman & Devanbu 2013; Nagappan & Ball 2005; Kruchten, Nord & Ozkaya 2012; Chambers 2013; Forsgren et al. 2021) | "Restraint as design center" > "What the retired instruments leave behind" |
| **IV · Open-source sustainability & community** | 7 | Maintenance-burden thesis + project typology (Eghbal 2020) | "Where Cairn is headed" > Horizon 1 |
| | 8 | External reuse contract (FAIR4RS; Barker et al. 2022) | Horizon 1 |
| | 9 | Open-development playbook for scientific software (Prlić & Procter 2012) | Horizon 1 |
| | 17 | Waste, and how much process a project should carry (Poppendieck & Poppendieck 2003; Boehm & Turner 2003; Saltzer & Schroeder 1975) | "Restraint as design center" |

## Current structure

This document does not restate the operating structure; it would go stale by
construction, and did. The roles are in `doctrine/roles.md` and
`dev/agent_collaboration.md`; the two lifecycles and the review floors are in
`AGENTS.md`; the review tiers, the one-round rule, and the stance distinction
are in `doctrine/dual-review.md`. Where this document and those disagree,
those are right.

## What the anchors bound, and what came out of it

*Folded down 2026-08-11.* The first six anchors each used to carry a full
gap-analysis section — roughly 240 lines of working-out — and that working was
then summarised again in a per-anchor table. Both are gone.

**The rule that replaced them**, and it applies to every strategy note here,
not just this one:

> **Ground the anchor where it bites. State the gap it exposes once. Maintain
> the gap list, never the mapping.**

A central "here is where Cairn sits against each anchor" table has to track
every introduction scattered through the document. It goes stale by
construction — the same failure as a module catalogue or doctrine index that
silently omits newer entries. Gap analysis produces **durable output** (the
contributions, the open gaps) from
**disposable working** (the per-anchor mapping). Keep the output current;
delete the working once it has yielded it.

So what survives below is the analogy that does the most explanatory work, the
contributions, and — the one list that must stay complete — what is still open.

### Peer review, not agent debate

The closest real-world match for Cairn's review system is not the multi-agent
debate literature. It is scientific peer review, which is also the frame a
scientist already understands.

| Scientific peer review | Cairn |
|---|---|
| Manuscript → editor → referees → decision | Proposal → maintainer → review tiers → Decision |
| Pre-submission collegial read | **Internal review** (strengthens the change within its own frame; a fresh session) |
| Independent journal referees | **External review** (makes it prove it should land; a different agent type or a human is the strongest distance and is recommended, never required) |
| Report → rebuttal → revised manuscript | Review → Response → Revised sections, one round |
| Conflict-of-interest rules; open review | Attributed, self-committed reviews; the whole arc in git |

Three differences are the interesting part. Independence is a **stance first
and a staffing choice second**: Internal strengthens within the structure
proposed, External evaluates that structure from outside and owes a verdict on
whether the change should happen at all. A different model architecture is the
strongest distance available, and the first controlled study of the question
says the direction of the pairing matters — Xiang et al. (2026), *Cross-Model
LLM Code Review: Should you use Claude to review Codex or vice versa?*,
[arXiv:2607.21656](https://arxiv.org/abs/2607.21656): on 116 tasks, one
cross-model direction raised pass rate 71.6% → 89.7%, the reverse direction
*lowered* it 91.4% → 82.8%, and self-review ranged from +13 points to no
effect. That is why cross-type is recommended and not required: a blanket rule
can make a change worse. The record is **radically open**: the whole arc
replays from `git log`. And the proposal's up-front verification plan gives it
a **registered-report flavour**, committing to what would falsify the change
before the work starts.

**One round.** A review and the author's revision close the loop, and the
revision carries the artifact to the Decision; a second round exists only for
material the first could not have read (a revision that widened scope; a code
revision that introduced new defects; an open Security Review). The reviewer
has already said what satisfies each blocking finding, and the field measured
what further rounds buy — modest recall at a precision-destroying
false-positive rate (Anchor 18). The differentiator's truer name is
**recorded, replayable deliberation**; append-only is one mechanism for it,
kept on the deliberate lane, while `git log` carries the property everywhere.

Two costs and one limit come with it. Reviewer diversity is bounded by the
number of model families available, so the External tier reduces correlated
blind spots without eliminating them. The maintainer is editor, domain expert,
and reviewer at once — efficient at this scale, and a real single point of
judgment. And **agreement between agents establishes consistency, not
correctness**: two reviewers can agree with a wrong specification, and a green
test can encode the same mistake as the implementation (a water-balance
calculation and its expected-value test that both reverse the sign of an
outflow term agree perfectly and conserve nothing). For a consequential
scientific change, independence has to include a basis *outside* the proposed
implementation — an analytical solution, a separately justified conservation
constraint, a trusted observation, or a domain expert's judgment — as one
well-chosen acceptance check, not another standing round. This is the
`deliverable` axis's concrete mechanism (below), and it is why the earlier
claim that Cairn is "more rigorous" than scientific peer review is withdrawn:
the apparatus is more *open* and its independence more *checkable*; whether it
is more rigorous is what the comparative evidence above has to show.

### What the analysis produced

Four things Cairn does that the surveyed literature does not describe, or
describes only in passing:

* **The Dual-Review model.** Two *stances* — one that helps a change land, one
  that makes it prove it should — executed asynchronously, mediated by commits,
  on a record that replays. AI code review itself is now default tooling and
  cross-model review a studied practice (Anchor 6), so the uncommon part is
  not "two AI reviewers"; it is the stance distinction and the recorded,
  attributable, replayable deliberation. That is Cairn's most legible
  contribution to a scientific audience, and one of its two differentiators.
* **The record is file-mediated; the channel is whatever the harness
  provides.** Nothing load-bearing exists until it is in the tree: a decision,
  a review, a plan, a hold. Agents may coordinate over harness messaging —
  every major harness ships it as of early 2026, and Cairn's own sessions use
  it for holds and relays — but the durable state lives in version-controlled
  artifacts, never in a session or a tool's memory. No server, no
  session-spanning agent identity, and any model family can join by reading and
  writing files. That is where vendor-neutrality actually comes from.
* **Test and documentation absorbed into every proposal**, rather than split
  into specialist agents. The distinction between built-AI-team-first and
  retrofit-onto-legacy work is itself worth naming; Cairn has a case on each
  side.
* **The User Agent** — a user-side role, where the literature covers agent-side
  roles acting on a project.

### Still open

**The one list in this section that must stay complete.** Each item names the
anchor it comes from, so a new anchor arrives with its gap rather than needing
a table row.

* **Measurement has a trend but no comparison** (3, 21). The git-derived
  time series exists (the takeover table); nothing compares Cairn against the
  lighter baseline named under *The promise*. Coordination-failure rates and
  reviewer-diversity blind spots are unmeasured.
* **No external-facing transparency artifact** (3, 8). The in-repo record is
  complete and hard to read from outside. An outside reader should not have to
  walk `git log` to reconstruct a decision.
* **No scientific acceptance check grounded outside the implementation** (4,
  6). Scientific correctness routes entirely through the human, and nothing in
  the apparatus asks for a basis independent of the proposed code and its
  tests. The `deliverable` axis is the proposed way to move part of it into
  the apparatus; the one-check form above is the cheap first step. That form
  landed as template guidance on 2026-10-19 (`independent-scientific-check`).
  The gap stays named: the `deliverable` axis, its disciplines, the governance
  reframe and the doctrine statement of the rule remain open (issue #19).
* **Reviewer diversity is bounded by the model families available** (6). The
  External tier reduces correlated blind spots; it cannot manufacture
  independence past the number of distinct families in use.
* **Stack-neutrality of the tooling is aspirational** (13). The methodology
  sits at the waist and is stack-independent; the Python tooling sits above it
  and has no second implementation.
* **The governance-regime and `deliverable` axes are unbuilt** (14, 15). Both
  are argued and neither is a dimension yet.
* **The context budget is unmeasured** (12). Leanness is argued as a
  correctness property with no measurement of the always-loaded surface.
* **The default routes to ceremony** (17). Triage separates trivial from
  substantive, but in practice the heavy path is the default and the maintainer
  has to intervene to get the cheap one.
* **The writing standard has been tried once** (16). Cairn Plain Language 1.0
  was tried on three real passages before it landed; nothing evaluates it with
  readers over time, as ISO 24495-1 asks, and its reasoning rules rest on the
  literature rather than a Cairn incident. The check is the Maintainer's own
  read about three months after landing (late January 2027): are the "I don't
  understand this" pauses rarer, and are reviews free of style policing?

Five early gaps are closed and now live in the doctrine: the bimodal AI surface
is documented, test and documentation requirements sit in the proposal
template, the verify-before-asserting failure typology is structured, the
write-time claim checker moved agent-output validation from reactive to
proactive, and the comprehension floor (16) is in the file every adopter
receives — `AGENTS.md` states that comprehension is a precondition of the
Decision. Since 2026-10-26 that floor has a method as well as a goal: Cairn
Plain Language 1.0, in the same shipped files.

## What Cairn is today

Cairn is at **v0.3.0** -- the realized methodology repository this doc's
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
"What the analysis produced" above):

* the **append-only, git-committed deliberation lifecycle** -- every decision's
  full arc reconstructible from `git log`; and
* the **Dual-Review model** -- two review stances (Internal helps a change
  land; External makes it prove it should) executed asynchronously and
  commit-mediated, with the strongest independence available recommended; a
  faithful instantiation of scientific peer review that is more *open* and
  whose independence is more *checkable* (Anchor 6).

**The apparatus an adoptable methodology demands.**  Beyond doctrine and
templates, Cairn ships what a *forkable, living* standard needs and a static
prose framework does not: a four-layer **security model** (scaffold safety,
lockfile integrity, content scanning, vendor-neutrality checks); an **upgrade
capability** (3-way module merge with a lockfile and base-cache, so a deployment
folds in new Cairn doctrine while keeping local optimizations); a **fold-back
channel** (`dev/upstream/`, a ledger and template by which deployments propose
improvements upstream; its tooling was retired in the 2026-08 sweep); and the
**work-intent tool** (an executable collision-avoidance primitive realizing the
stigmergic coordination of Anchor 5).

**The value curve, honestly.**  Cairn *adds friction before code* and is meant
to pay it back later -- in less rework, fewer forgotten decisions, fewer agent
collisions, and fewer unreviewed scientific changes.  That payback is the bet,
and as *The promise* says, it is plausible and exercised, not yet shown
(**Anchor 11**):

* *The bottleneck has moved from writing code to verifying it.*  METR's
  early-2025 randomized trial -- METR (2025), *Measuring the Impact of
  Early-2025 AI on Experienced Open-Source Developer Productivity*,
  [arXiv:2507.09089](https://arxiv.org/abs/2507.09089) -- found experienced
  developers on their own mature repositories **19% slower** with AI while
  believing themselves ~20% *faster*.  METR's own February 2026 update retired
  the slowdown as a current picture: the same developers re-measured at −18%
  with an interval spanning zero, newly recruited ones at −4%, and selection
  effects (developers unwilling to work without AI; 30–50% withholding the
  tasks they expected AI to help most) obscure a speedup METR now calls
  likely ([study-design update](https://metr.org/blog/2026-02-24-uplift-update/)).
  A tens-of-thousands-of-engineers rollout at Microsoft measured ~24% more
  merged pull requests over four months, with the authors' caveat that a
  merged PR is not value ([arXiv:2607.01418](https://arxiv.org/abs/2607.01418)).
  What survives all of it: the **perception gap** is real, the uplift is real
  and instrument-dependent, and the cost has moved to review.  Neither study
  compares a Cairn-shaped process with a lighter one; the 19% result does not
  establish that Cairn's front-loaded friction pays back.
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
doctrine exercised in use, and -- carrying a DOI via a release plus a
`CITATION.cff`, dual-licensed (CC BY for prose / templates, a permissive license
for scripts) -- it is itself a citable Open Science artifact independent of any
paper.

**The two-case comparison is the spine -- of the description, not yet of the
efficacy claim.**  modflow_tools (AI-team-first) and LHM (a long-lived,
majority-MATLAB, majority-untested landscape-hydrology model retrofitted under
the same maintainer) are a before/after on each side, not "apparatus vs.
none": LHM's baseline is its pre-adoption ad-hoc state, and its treatment is
the modflow_tools apparatus *deliberately adapted* for a large, old,
multi-language legacy codebase.  Both are one Maintainer's; they show what
generalizes and what does not, and they are not independent evidence that the
apparatus reduces errors or effort.  What the pair shows:

* **What generalizes vs. what is project-specific accretion.**  Generalizes
  near-verbatim: the proposal/plan lifecycle, append-only deliberation, the
  Internal/External review tiers and structural-independence floors, stigmergic
  artifact coordination, the shared-communication-file discipline.
  Context-driven additions with no greenfield equivalent: the Legacy Agent,
  domain-specialized agents, the surface-readiness ledger, the MATLAB-first
  dual-language test architecture, bounded port stewardship.
* **The retrofit role the framework predicts, instantiated.**  modflow_tools,
  AI-team-first, deliberately has no Test/Doc agent; LHM, retrofit-on-legacy,
  needs a standing Legacy Agent -- the built-from-scratch-versus-retrofit
  distinction, with a concrete case on each side under one maintainer.
* **Role-design and independence variants.**  LHM splits agents by *domain*
  (Inputs / Model / Postprocess) where modflow_tools splits by *lifecycle stage*
  (Strategy / Implementation); LHM's domain agents cross-review one another, so
  structural independence comes from domain-rotation, not only agent-type
  difference (extending the role-design and structural-independence findings
  above).
* **The surface-readiness ledger** -- a Ready / Transitional / Frozen tiering of
  every code surface: both a safety interlock and a *measurable* human-only ->
  human+AI transition metric.

**Positioning.**  The audience is **scientists building scientific-computing
software** -- not software-engineering generalists or agentic-framework builders
-- who care about rigor, reproducibility, and review discipline; the methodology
was developed by a scientist on scientific software, an authentic and
underserved niche.  Cairn does not pitch `AGENTS.md` (a Linux Foundation
standard since 2025-12 under the Agentic AI Foundation, read natively by every
major harness -- Claude Code since v2.1.277, 2026-09-18, wherever no
`CLAUDE.md` exists) or spec-driven-development tooling (crowded); it leads with the two
differentiators above, and The Turing Way is its model for adoptability (a
template repository, a quickstart, a piecemeal-adoption path).  **If a paper is
ever written** it is optional amplification -- a short arXiv preprint (cs.SE)
pointing at the DOI'd repository; JOSS does not fit (it reviews research
*software*, not a methodology) -- and its skeleton already exists here: the
framework anchors as related work, the two case descriptions, the
contributions under "What the analysis produced", and the forward directions as future work.

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
* **When this fails, the human over-relies** -- the appropriate-reliance literature (e.g. *Knowing About Knowing: An Illusion of Human Competence Can Hinder Appropriate Reliance on AI Systems*, arXiv:2301.11333; *In Search of Verifiability: Explanations Rarely Enable Complementary Performance in AI-Advised Decision Making*, arXiv:2305.07722): fluent explanations can *increase* over-reliance and manufacture an *illusion of understanding*; genuine complementary performance needs **verifiability**, not a plausible-sounding story.  This is the empirical shape of the rubber-stamp.  The agent-research community reached the same place in 2026: a thirteen-author position paper argues the bottleneck has shifted from task-solving to how users communicate with, supervise, and trust agents -- verifiability and steerability first (*Humans are Missing from AI Coding Agent Research*, [arXiv:2608.12355](https://arxiv.org/abs/2608.12355)); and a Microsoft study of agent-trace interfaces found a redesign that cut error-detection time while raising user confidence *without* raising accuracy (*Overseeing Agents Without Constant Oversight*, [arXiv:2602.16844](https://arxiv.org/abs/2602.16844)) -- the illusion, measured.

**Leg 2 -- plain explanation is also a test of the explainer's own understanding.**  The discipline cuts both ways.  For humans this is well established: the **illusion of explanatory depth** (Rozenblit & Keil 2002, *The misunderstood limits of folk science: an illusion of explanatory depth*, Cognitive Science 26:521--562) -- people are confident they understand a bicycle or a zipper until asked to explain it step by step, at which point the understanding collapses.  Explaining plainly *tests* understanding; it does not merely deliver it.  **The same is plausibly true of AI** -- stated honestly as a well-motivated extension, not a settled result: a model can produce fluent, confident jargon that pattern-matches expertise without a correct, grounded claim beneath it, and the jargon then *shields* that claim from scrutiny -- the human's and the model's own.  This makes the plain-language requirement a **correctness check on the explainer**, not only a service to the reader, and ties it to Cairn's existing `verify-before-asserting` discipline (Anchor 3's Bias & Robustness leg): jargon can hide an unverified assertion; plain words expose it to challenge.

**Leg 3 -- an agent must say how sure it is, in a form the reader can use.**  Added 2026-10-26, from the literature search behind Cairn Plain Language; this leg rests on published studies, not on a Cairn incident.  Language models rarely state uncertainty unprompted, and when asked to they are overconfident: on average 47% of their confident answers were wrong (Zhou et al. 2024, *Relying on the unreliable*, arXiv:2401.06730).  Readers overestimate the accuracy of model answers, and longer explanations raise their confidence without raising accuracy (Steyvers et al. 2025, *What large language models know and what people think they know*, Nature Machine Intelligence 7:221--231).  First-person uncertainty helps, but only partly: when a model said "I'm not sure, but...", people relied less on its wrong answers, though over-reliance did not disappear (Kim et al. 2024, ACM FAccT); Zhou et al. found users relied on model output whether or not it was marked.  How uncertainty is stated matters too.  Probability words alone are read very differently by different readers; pairing them with numeric ranges raised agreement with the intended meaning only from 27% to 40% across 25 samples in 24 countries (Budescu et al. 2014, Nature Climate Change 4:508--512), and words added to numbers do no better than numbers alone (Mandel & Irwin 2020; Dhami & Mandel 2022).  So the floor needs more than plain words: it needs the agent to separate what it measured from what it assumed, to state uncertainty as a number with its source, and to say which checks it did not make.  This also gives Leg 2 a mechanism: a first-person account of what was checked is what lets the Maintainer audit the work, even when fluent prose would otherwise carry their trust.

**Worked example (the origin case).**  This anchor surfaced from a real comprehension failure during the six-proposal superplan.  The package-splitting work leaned on "AST source-motion attestation" -- opaque enough that the Maintainer had to look the term up separately, then reverse-engineer the implementing agent's function names and outputs to follow it.  In plain terms the claim was simply: *"we used Python's own structured representation of the code (its abstract syntax tree) to prove every function moved exactly once when the oversized package was split -- nothing lost, nothing altered."*  The plain version is not less precise -- it is more reviewable.  And the jargon's cost was not merely slower reading: it left the Maintainer unable to *review* the work, because the opaque surface was the only window onto it.  The thesis, in miniature.

**The Cairn contribution / divergence.**  The XAI and reliance literatures study AI-to-human explanation largely in *decision-support* settings (a model advises; a human accepts or overrides).  Cairn's setting differs: a **recorded-deliberation lifecycle** in which the human must understand in order to *legitimately decide and sign*, on a durable, reviewable record.  So Cairn does what the source literatures do not -- it makes the **comprehension floor a reviewable property of the lifecycle**, the same move that turned reviewer independence into a structural, checkable tier.  "Did the human actually understand what they decided?" becomes a first-class question, not an afterthought.  Stated reflexively: this anchor was itself produced by the failure mode it names -- a jargon-dense stretch that degraded the Maintainer's review -- which is exactly the incident-grounded evidence the doctrine-evolution gate asks for.

**Surfaced direction -- communication calibration -- a universal standard now, a dimension on the evidence.**  Anchor 3's *Usability* dimension remains part of the open measurement gap; this is where it gets watched -- two parts, deliberately at different maturity.

* **Settled -- the universal standard: Cairn Plain Language 1.0.**  Lead plain, keep precision beneath, and treat *"I don't understand this yet"* as a **mandatory pause**: a decision surface the Maintainer cannot follow is not decidable.  Until 2026-10-26 that rule named a goal and no method, and the same failure recurred three times (the origin case above; three proposals of 2026-08-13 fixing comments, docstrings and test names; the 2026-10-23 rewrite of the reader-facing docs and case studies).  The method is now **Cairn Plain Language 1.0**: 17 numbered rules in the shipped `dev/agent_collaboration.md`, with one pointer sentence in `AGENTS.md` (proposal `dev/proposals/archive/2026-10-26-claude-writing-for-the-reader.md`, accepted 2026-10-26).  Three choices in it answer this anchor directly.  It **limits structure, not vocabulary**, so domain terms stay and get defined, which serves both ends of Kalyuga's expertise range.  Its **reasoning rules (13 to 17)** carry Leg 3: measured, assumed and expected kept apart; numbers with units and sources; uncertainty as a number, or an explicit "I have no basis for a number"; and the agent's own account of what it checked.  It is **checked by reading, never scored**, which is Anchor 21's discipline applied to prose.  The standard is versioned, CC BY 4.0, and free of Cairn-only terms in its rules, so other projects can adopt it unchanged.  Every adopter, always.
* **Observed -- heading toward a dimension.**  Treat communication calibration as its own Cairn axis (distinct from the *programming-language* axis), tuned to the reader's register -- *domain* proximity and *software* proximity.  This is **not imagined enrichment**: it is an **origin-deployment design note from real maintainer usage**, evidence-status *observed-here, not yet externally replicated* -- the same footing the project's `deliverable` / product axis arose on.  *Revised 2026-10-26:* the earlier text here proposed adopting an existing controlled-language grammar such as ASD-STE100 or Attempto Controlled English.  The Cairn Plain Language proposal weighed that and rejected it: a controlled vocabulary suits maintenance procedures and strips the hedges and domain terms that scientific argument is made of.  If the axis is built, its language classes start from the standard's rules (undefined terms and acronyms, stacked nouns, coined names, bare probability words), not from a word list.

Two guards answer the real risks: the calibration is a **dynamic starting register, not a fixed label** -- grounding (Clark & Brennan) adjusts it turn-by-turn, so it neither ossifies nor profiles; and its evidence ledger is **score-free** -- language-*classes*, never the person.  One invariant holds throughout: **guarantee a plain layer, never strip precision** -- the record stays exact, the plain layer sits on top.  Building the axis (its grades and rubric) is the follow-on, gated on the next bet (a third-party adopter); the fixed standard is the cheaper first step, and using it will show whether a per-reader setting is needed at all.

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

This also sharpens the 2026-06-05 stack-neutrality assessment, since folded
into this section: the *methodology* sits at the
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

## Restraint as design center

Cairn's two differentiators are the deliberation record and Dual-Review. The way
Cairn dies is not that they fail. It is that they get expensive enough that
people work around them. Restraint therefore sits beside trust as a design
center, not as a nice-to-have.

**The dominant failure is bloat, and it takes two forms.** Bloat in code is
visible and gets audited. Bloat in deliberation is invisible, because it looks
like diligence: every artifact is defensible on its own, and together they
crowd out the work.

**The recursive form is the dangerous one — apparatus built to prevent bloat
that itself bloats.** Two instances from this repository on 2026-08-11:

* A complexity instrument, built to find code bloat, accumulated two external
  review rounds, a twelve-anchor literature grounding, a declared corpus, and a
  preregistered validation design. That exceeded the refactoring it existed to
  justify, and no refactor followed.
* A metrics note, built to measure the apparatus, reached 724 lines specifying a
  measurement platform. It was cut to 161.

That day the repository produced **41 commits, 4 of which touched shipped
code**. A proposal named `review-efficient-lifecycle` has consumed **32
commits** of lifecycle ceremony.

**17. Waste, and how much process a project should carry.** Poppendieck, M., &
Poppendieck, T. (2003). *Lean Software Development: An Agile Toolkit.*
Addison-Wesley. Lean's first principle is **eliminate waste**, translating
Ohno's seven wastes into software; **extra processes** and **extra features**
are named waste categories, waste being anything that does not produce value for
the user. With Boehm, B., & Turner, R. (2003). *Balancing Agility and
Discipline: A Guide for the Perplexed.* Addison-Wesley, which makes "how much
process" an explicit judgment across five factors — **personnel, criticality,
size, culture, dynamism** — where too much ceremony and too little are both
failures. The security-side companion is Saltzer, J. H., & Schroeder, M. D.
(1975). *The Protection of Information in Computer Systems.* Proceedings of the
IEEE 63(9): 1278-1308, whose **first** design principle is **economy of
mechanism**: *"Keep the design as simple and small as possible… design and
implementation errors that result in unwanted access paths will not be noticed
during normal use."* Over-building a protection mechanism is a security failure,
not only a cost.

### What the retired instruments leave behind (Anchor 21)

The two instruments named above did not die because their science was wrong;
they died because their *maintenance* exceeded their return. Their epistemics
are the inheritance, preserved here so retiring the machinery does not retire
the discipline (Maintainer direction, 2026-08-26).

**21. Measurement discipline.** Rahman, F., & Devanbu, P. (2013). *How, and
Why, Process Metrics Are Better.* ICSE 2013 — history-derived metrics (churn,
change patterns) outperform code-derived metrics and generalize better; with
Nagappan, N., & Ball, T. (2005). *Use of Relative Code Churn Measures to
Predict System Defect Density.* ICSE 2005 — churn normalized by size predicts,
absolute churn does not. Kruchten, P., Nord, R. L., & Ozkaya, I. (2012).
*Technical Debt: From Metaphor to Theory and Practice.* IEEE Software 29(6) —
the debt metaphor is useful only when principal and interest are concrete; a
ledger without a cost model has no stopping rule. Chambers, C. D. (2013).
*Registered Reports: A New Publishing Initiative at Cortex.* Cortex 49(3) —
declare hypothesis, population, and analysis before the results exist; with
Kerr, N. L. (1998). *HARKing: Hypothesizing After the Results Are Known.*
Personality and Social Psychology Review 2(3): 196–217 — presenting a post-hoc
hypothesis as a priori is the named malpractice rule 4 guards against.
Forsgren, N., et al. (2021). *The SPACE of Developer Productivity.* ACM Queue
19(1) — productivity is multidimensional; no single number captures it; with
Campbell, D. T. (1979). *Assessing the Impact of Planned Social Change.*
Evaluation and Program Planning 2(1): 67–90 — the more a quantitative
indicator is used for decision-making, the more it corrupts and distorts the
process it monitors; and Austin, R. D. (1996). *Measuring and Managing
Performance in Organizations.* Dorset House — the book-length treatment of
measurement dysfunction, grounded in software organizations: people respond
to being measured with unanticipated sophistication, and dysfunction follows
a recognizable pattern.

*Evidence status, in the discipline's own spirit.* Rule 2 rests on **direct
measured comparisons** (Rahman & Devanbu; Nagappan & Ball) — though measured
for defect prediction, and extrapolation beyond that is argued, not measured.
Rules 1, 3, 4, and 5 rest on **established methodological literature**
(Campbell's law, registered reports, HARKing, measurement dysfunction, SPACE)
applied to the human + AI setting by argument; no one has measured them in a
setting like Cairn's. One mechanistic datum is native to the agent context:
the verbosity-bias literature under Anchor 18 shows judges rewarding length,
which is rule 1's failure mode observed at the model level. And this
repository supplied its own instance: an instrument that paid for findings
was rebuilt twice in one week before the rule against it was written down.

Five rules, distilled from the two retired programs
(`archive/2026-06-05-claude-cairn-complexity-debt-audit.md` and
`archive/2026-05-20-claude-team-productivity-metrics.md`, both closed and
archived 2026-08-26) and binding on all of Cairn's measurement — today that
means the gauge classifier, the takeover table, and the mission metrics:

1. **Measure structural events; never measure prose.** A metric scraped from
   written text makes the text the optimization target — any metric that
   rewards writing more is a defect to remove, not a signal to tune.
2. **Prefer history to shape.** Git-derived process measures are the
   better-supported instrument class; a static metric owes decorrelation from
   raw size before it earns a place.
3. **Declare the population and the analysis before the results exist**, state
   limits before findings, and give INCONCLUSIVE a defined branch — a ranking
   without a declared corpus is not reproducible, and partial exclusions
   reshape conclusions silently.
4. **Measure forward; never annotate the archive with the hypothesis in
   hand.** A closed record is evidence precisely because it predates the
   question. If a question should be answerable later, add the field that
   answers it before it is needed, where the person who knows is already
   writing.
5. **No composite scores, no per-person totals, ever.** Metrics serve system
   learning, not member ranking — the instrument that pays for *findings*
   rather than outcomes recreates the disease it was built to watch.

Rule 5 carries the **Measurement Compact** (its live home as of 2026-08-26,
hoisted from the archived metrics note), whose remaining commitments bind
alongside it: no role- or tier-confounded metric is read as capability proof;
no cross-team generality is claimed from a single corpus; the posture is
internal-diagnostic, never external-marketing — any externally published
artifact derived from these measurements is a separate act gated on an
explicit Maintainer decision.

### Not all weight is waste

Boehm & Turner's **criticality** factor is not discounted by how many adopters
exist. It measures what happens if the thing is wrong, not how often it is
exercised. Cairn installs executable code into other people's repositories and
gives agents write authority there. That is a supply-chain position, and it is
exactly where a default-trust posture has failed worst — the point Thompson, K.
(1984), *Reflections on Trusting Trust*, Communications of the ACM 27(8):
761-763, made in the first place: you cannot trust code you did not create
entirely yourself.

So the line runs between two things that are easy to confuse:

* **Security properties on trust boundaries are worth keeping even when they
  look premature.** Fail-closed defaults, trust roots that measure rather than
  assume, revalidation immediately before use. These are cheap to hold and
  expensive to retrofit, because once a boundary is assumed trustworthy that
  assumption spreads everywhere. Economy of mechanism keeps them small, not
  absent.
* **Security deliberation bloats like anything else.** Six review rounds on a
  proposal about review efficiency is ceremony wearing a security jacket.

The test is not "is this security?" It is **does the deliberation cost track
the blast radius, or how interesting the question is?**

22. **The agent supply-chain incident record.** The posture above was argued
    from Thompson in 2026-08; by 2026-10 the field had supplied the incidents.
    *s1ngularity* (2025-08-26): malicious releases of the Nx build system
    weaponized developers' own Claude, Gemini and Q command-line agents, with
    permission-bypass flags, to enumerate and exfiltrate 2,349 credentials
    from 1,079 machines. *Clinejection* (2026-02-17): a prompt injection
    carried in a GitHub *issue title* reached a Claude Code CI workflow holding
    shell and write permissions, stole an npm publish token, and shipped a
    rogue agent to ~4,000 developer machines in eight hours
    ([CSA research note](https://labs.cloudsecurityalliance.org/research/csa-research-note-clinejection-prompt-injection-cicd-cache-p/)).
    *Comment and Control* (2026-06): Claude Code, Gemini CLI and Copilot
    agent integrations all treated pull-request titles, issue bodies and HTML
    comments as instructions, yielding live API keys and write-scoped tokens
    ([CSA research note](https://labs.cloudsecurityalliance.org/research/csa-research-note-claude-code-github-action-prompt-injection/));
    OWASP's 2026 reporting puts prompt injection behind most agentic security
    failures in production. The live attack class is **an agent reading
    untrusted repository content as instructions while holding credentials**.
    Cairn's answers are structural rather than clever: no CI agent, no egress
    path, humans alone push, the instruction-source boundary in every agent's
    standing rules, and trust roots that are measured before use. Those are
    cheap to hold and were not premature.

### The default is currently backwards

Cairn's triage separates trivial from substantive work, but in practice
everything routes to the heavy path unless the maintainer intervenes. On
2026-08-11 the maintainer twice had to ask "why not just do it?" — once about a
two-character fix, once about cutting a document. For a method that claims
nimbleness, **ceremony should be opt-in on demonstrated blast radius, not
opt-out on maintainer override.**

**The standing test:** shipped change versus deliberation about change, over a
working period. It is crude and gameable in principle, but it counts structural
events rather than prose, and a method that never passes it is not earning its
overhead. *The session that produced this section fails it.*

This section is where three existing threads belong, and they should point here
rather than restate: Anchor 12's argument that leanness is a **correctness**
property and not only a cost one; the adoption promise (*keep the apparatus only
as heavy as your codebase and team earn*); and the Horizon 2 maturity ladder,
which this supplies with its actual justification.

### The 2026-08 refocus — restraint wins the argument

This section predicted the failure; in August 2026 the Maintainer called it:
*"instead of a capable AI agent development team I feel like we have a bunch
of process-zombies."* The full diagnosis, measurements, counterforce design,
and subtraction plan live in `2026-08-21-claude-nimbleness-recovery` (a
strategy note co-revised with the Maintainer through four correction rounds);
two derived proposals are in flight. What belongs *here* is the durable frame
and its grounding.

**The measured fact**: since July 2026, ~5% of all lines written across Cairn
and modflow_tools were functional product; the rest was deliberation and
process machinery. The standing test this section defined ("shipped change
versus deliberation about change") was finally run as a weekly time series,
and the method failed its own test for two months straight.

**The causal frame**: every prior methodology was implicitly disciplined by
the scarcity of human attention — payroll and boredom bounded bureaucracy.
Agents removed that scarcity, and review is ideal work for a
compliance-shaped optimizer: findings are legible wins, their cost diffuse,
and a finding can never be shown not-worth-raising because the lighter path
never runs. A system whose only legible currency argues for more
deliberation converges on what Cairn became. This is not unique to Cairn:

18. **Agent deliberation pathologies.** Cemri, M. et al. (2025). *Why Do
    Multi-Agent LLM Systems Fail?* (MAST, the multi-agent failure taxonomy;
    NeurIPS 2025). [arXiv:2503.13657](https://arxiv.org/abs/2503.13657) —
    across 1,600+ traces, specification and coordination failures dominate,
    and surviving production systems share Cairn's skeleton: phase gates,
    shared artifacts, a final supervisor. The deliberation-over-action bias
    is measured at the model level: *The Danger of Overthinking: the
    Reasoning-Action Dilemma in Agentic Tasks*
    ([arXiv:2502.08235](https://arxiv.org/abs/2502.08235)) and the TMLR 2025
    survey *Stop Overthinking*
    ([arXiv:2503.16419](https://arxiv.org/abs/2503.16419)) — selecting
    low-overthinking trajectories improves outcomes ~30% while cutting
    compute; deliberation past a point degrades results, not just budgets.
    Review-round inflation is measured too: *More Rounds, More Noise*
    ([arXiv:2603.16244](https://arxiv.org/pdf/2603.16244)) finds added review
    rounds buy modest recall at precision-destroying false-positive rates
    (a second round raised findings per artifact 9.3 → 15.2, true positives
    only 2.64 → 3.03) — the empirical footing under the one-round rule the
    doctrine adopted 2026-10-01. And verbosity
    bias in preference data and judges
    ([arXiv:2310.10076](https://arxiv.org/pdf/2310.10076)) is the mechanism
    by which agent prose armor gets rewarded at the foundations.
19. **The oversight bottleneck, and the theory of the firm.** Coase, R.
    (1937). *The Nature of the Firm.* Economica 4(16): 386–405 — where price
    coordination is too costly, the efficient structure is hierarchy; an
    internal "market" for agent effort is a category error, and the refocus's
    mechanisms are management technology, requiring a manager irreducibly.
    The field converged on the same scarce resource in 2026: human attention
    as the budgeted bottleneck of agentic development (e.g. *Human Oversight
    of Agentic Systems in Practice*,
    [arXiv:2606.05391](https://arxiv.org/pdf/2606.05391); practitioner
    accounts of review as the new bottleneck), independently reproducing the
    refocus's specific mechanisms — reversibility-sorted escalation, batched
    review windows, risk-tiered oversight. At internet scale the same
    economics is the 2026 open-source crisis: AI-generated contributions
    cheap to create and expensive to review flooding maintainers. curl ended
    its six-year bug bounty on 2026-01-21 after the valid-report rate fell
    from ~15% to under 5% (the first three weeks of 2026: twenty reports,
    none valid); Jazzband sunset its 84 projects in 2026-03 naming the flood;
    tldraw auto-closes every external pull request; Ghostty bans AI-written
    code; GitHub publicly weighed a pull-request kill switch. Rationed there
    by refusal, where Cairn's answer is pricing and routing.

**The counterforce, settled with the Maintainer** (details in the refocus
note): the four-part core is untouchable — intent before code, independent
verification before landing, recorded decisions, measurements over
assertions. Around it: three lanes triaged by blast radius; review answers
*"does this work"* evidence-first; loops terminate agent-side with an
irreversibility tripwire to the Maintainer; every artifact carries a
net-zero attention balance (attention asked, outcome that repays, archive
verdict — additions and removals both cost, only outcomes earn); decisions
route by expertise; Maintainer-facing prose leads plain. The firm is staffed
so agents prepare judgments the Maintainer merely makes, and the genuinely
self-regulating forces are the boundary markets: adopters, agent types
competing for role seats, and the Maintainer's own continued investment.

**The build honors economy of mechanism** (Anchor 17's Saltzer principle,
now applied to the apparatus itself): ~30 required new lines of code against
a measured ~61k-line subtraction — because for an agent, a sentence of
doctrine does most of what bookkeeping code did: agents re-read the
constitution each session and largely comply, so enforcement code guarded a
reader who rarely needed it. *Largely*, not reliably: a mining study of 7,310
agent-rule entries across 83 projects found compliance rising from 49% to 72%
after corrective rules landed, with 78% of edits adding negative constraints
after an AI error ([arXiv:2606.12231](https://arxiv.org/abs/2606.12231)), and
Epoch AI / METR's MirrorCode report records an agent choosing eager over lazy
evaluation against a specification that repeatedly said otherwise,
recognizing the mismatch, and patching around it
([MirrorCode](https://epoch.ai/publications/mirrorcode-preliminary-results)).
So a sentence replaces a ledger; it does not replace a boundary. Code keeps
what text cannot do: compute, execute, and physically protect — and the
scientific checks and required human decisions are placed *at the point of
action*, in a short handoff naming the applicable constraints, evidence, and
open decisions, rather than in a history the agent is trusted to have read.
Reversibility is judged beyond the repository too: git can roll back a
commit, not a published conclusion or overwritten unversioned data. The
standing razor: *could this be a sentence instead of a script?* — answered
for bookkeeping, never for a trust boundary.

### The human side of restraint — the operator's own allocation

The refocus's causal frame has a second application the 2026-08 record
surfaced last, in the Maintainer's own words: agent-based development is
*addictive for the human*, and it genuinely displaced paid work — affecting
interactions and overall output *"despite building some amazing stuff."*
The mechanism is the same missing scarcity, one level up. Working with
agents is compulsion-shaped by accident: each prompt is a cheap pull with a
variable payout — the most habit-forming reinforcement schedule known —

20. **The operator's own allocation.** Ferster, C. B., & Skinner, B. F.
    (1957). *Schedules of Reinforcement.* Appleton-Century-Crofts — the
    variable-ratio schedule produces the highest, most extinction-resistant
    response rates; with Alter, A. (2017). *Irresistible: The Rise of
    Addictive Technology.* Penguin — modern behavioral design assembles
    exactly these ingredients (variable reward, no stopping cues, frictionless
    re-engagement). Agentic development assembles them *unintentionally*, and
    adds two amplifiers no consumer product has: extraordinary real leverage
    per pull, and an infinitely patient, responsive, appreciative
    collaborator — which removes the social stopping cues human collaboration
    provides. The surveyed oversight literature prices the human's *burden*;
    operator *compulsion* — the human volunteering the attention the system
    no longer even has to demand — is, as far as this framework has found,
    undescribed. It is the missing-scarcity thesis applied to the operator.

and there is no natural end: no tiredness on the other side, no one to
disappoint by continuing, always one more visible improvement — with
**meta-work as the strongest attractor**, because process work always yields
legible motion. A methodology for scientists must say this plainly, because
its adopter is a person whose paid work is the science and whose calendar is
the same unpriced commons the process once was. The guidance mirrors the
firm design, applied to the operator:

* **Async over synchronous.** The interface contract (digest, batched
  decisions, the goodnight window) bounds the *human's presence*, not only
  the system's demands. The compulsive modality is the rapid back-and-forth
  loop; variable-ratio reinforcement dies at long intervals. Scope, fire,
  close the laptop, read at the window.
* **A calendar appetite for methodology work**, set outside the pull — the
  operator's own objective function: is this session worth more than what it
  costs, denominated in paid work and people.
* **A personal staff gauge**: hours in agent sessions against real output,
  glanced at, not ledgered — the takeover table for the calendar.
* **Say it to a colleague.** Named compulsions lose power; a team that knows
  is a natural boundary. Persistent displacement after structure is in place
  is a reasonable thing to bring to a professional.
* **Agent-side norms carry part of it**: clean closes without dangling
  next-step hooks; no treatment of late-night presence as an opportunity to
  extend work; energy steered toward the science over the meta-work.

## Where Cairn is headed

These are **possibilities, not a queue** -- the anti-scope at the end binds,
each would go through the normal proposal cycle, and *(settled 2026-10-01)*
every one of them now sits behind the comparative evidence named under *The
promise*: an outside adoption on real scientific changes, measured against
the lighter baseline. None of them follows automatically from more capable
agents. A cheaper move than any new axis is a **worked example**: one
hydrology change, specified, independently checked against a basis outside
its implementation, reproduced, and explained to its scientist. A second
domain would show what generalizes before any general configuration is built.

**The open empirical work** *(revised 2026-10-01)*.  The time series exists
— derived from git alone, no instrument layer: the weekly
deliberation/machinery/product accounting in
`2026-08-21-claude-nimbleness-recovery` (the "takeover table," product share
~5% of lines written since July 2026). The lifecycle-metrics layer that once
carried this was retired in the subtraction sweep; the program continues on
**git-derivable staff gauges** read at the goodnight routine. A small share
of functional lines is a warning about *allocation*, not a measure of value
— one scientific correction can matter more than thousands of product lines
— which is why the comparison above, not the share, is the test.  Two
measurement gaps ride on it: **reviewer-pool diversity** (does the current
small agent corpus systematically miss particular finding-classes?) and a
**coordination-failure taxonomy** (industry reporting attributes a large share
of multi-agent failures to coordination/orchestration; Cairn has
countermeasures but no measurement of them).

**The agents the apparatus was sized for are gone.** METR's time-horizon
series doubles roughly every four months as of early 2026, and a frontier
model crossed a full working day of autonomous task length in 2026-02; the
MirrorCode report describes a ~16,000-line bioinformatics toolkit
reimplemented end to end, under the explicit conditions of an executable
oracle and extensive tests, with the authors warning against generalizing
beyond them. Two consequences for this document. The maturity ladder (Horizon
2) runs *down* as agents strengthen — much of the 2026-08 bloat was process
built for weaker agents and never re-sized. And what the agent cannot supply
is unchanged by its horizon: deciding what *correct* means for the science,
and supplying the feedback that says so. Better agents make protecting
scientific judgment more important; they do not make a larger methodology
more valuable.

Two horizons follow.


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
  has the *capture* surfaces (issue-tracker doctrine, the User Agent role)
  but not the *graduation* mechanics.
* **Distributed, asynchronous review with an external reviewer pool.**  The
  **Dual-Review model** already assumes structural independence; community
  mode generalizes the External Reviewer from "the strongest distance one
  team can staff" to "a rotating pool of external human + AI reviewers."  This directly attacks
  the open reviewer-diversity gap -- a community is *how* the reviewer
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
  This is uncharted in the surveyed anchors and is the clearest candidate for a
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
agent-side scientific-error check the open-gap list calls missing (the move is to make part
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
genuinely scientific content is thin -- Anchor 4 (borrowed) and the open
scientific-correctness gap.
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
dimension). It also feeds the trust model: the finding that *scientific
validity routes wholly through the human maintainer* is the verification-owner
bottleneck, and the PV/NT/PROV disciplines -- with USGS's domain review as the
proof-of-concept -- are how some of it moves into the apparatus.

**The 2026 field evidence lands exactly here.** OpenAI's field report on
agents in scientific computing (2026-08; eight projects, mostly genomics;
Codex and Claude Code) reports speedups to 60× alongside agents that were
"eloquent, convincing, and confidently wrong in ways that are easy to miss" —
one package shipped inverted control parameters whose plausible output passed
initial validation and was caught only by calibration against synthetic data
— and concludes that the bottleneck has moved "toward validation, scientific
review, and clear responsibility for maintenance." Two benchmarks say the same
from opposite sides: SWE-bench Science's September revision puts the best
agent below 50% on 119 repository tasks, with failures of scientific
abstraction ([arXiv:2608.19799](https://arxiv.org/abs/2608.19799)), while
SciCode-Verified's authors report main-problem accuracy rising from 9–27% to
69–92% once domain experts repaired faulty specifications and grading
([arXiv:2608.04975](https://arxiv.org/abs/2608.04975)) — good coding scores
do not establish scientific reliability, and a failed scientific test does
not establish incompetence, because the correctness of the *test* is in
question too. The closest prior art to this axis is Bhave et al. (Idaho
National Laboratory, 2026), AI-assisted verification and validation inside a
nuclear quality-assurance regime — disclosure and review standards, auditable
artifacts, human accountability, demonstrated on a fusion code with
known-solution validation cases
([arXiv:2605.17675](https://arxiv.org/abs/2605.17675)); the 2026
scientific-computing-ecosystems workshop report names trust, validation and
traceability a strategic theme ([arXiv:2608.26519](https://arxiv.org/abs/2608.26519)).
The disciplines this axis names are the apparatus-side form of what all of
them ask for, and the one-check rule under Anchor 6 is their cheapest first
instance.

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

Cairn v0.3 ships the **static half**: the `on-ramp/` defines three graduated
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
into a self-instrumenting one** -- Cairn ships heuristics that observe a
live deployment (the git-derived gauges, collision log, intent log, commit
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
depth yet* — and, the refocus's addition, *you no longer need the depth you
have*: the ladder runs down as well as up, and the 2026-08 refocus is Cairn
itself taking the down rung.

The novel step is narrow: methodology frameworks (the Turing Way, the *Ten Simple
Rules* papers, FAIR4RS) are *static prose* -- none watches your repository and
tells you when you have outgrown your setup; even TCMM (Anchor 3) scores an AI
system's trustworthiness, not a deployment's depth. This turns the `dimensions/`
model from *statically-profiled* axes into *continuously re-observed* ones, and
is the natural consumer of the still-open **empirical time-series** work -- the
triggers need a *trend*, not a snapshot.

### Candidate moves

None is queued. One gates most of the rest; each would go through the normal
proposal cycle when its gate or its time comes:

* **The outside adoption with a pre-declared threshold** (*The promise*) --
  the one move that can turn the horizons from possibilities into work.
* **The worked example** -- one hydrology change carried through
  specification, an independent scientific check, reproduction, and plain
  explanation; cheaper than any axis and the first `deliverable` discipline
  in practice.
* **The LHM operating case** -- carry LHM from adopted to *operating*; the
  second domain that shows what generalizes.
* **Publishing Cairn Plain Language as a standalone standard** -- its own page
  on the project site, a block to paste into any agent's instruction file,
  worked before-and-after examples, its own DOI. Not behind the adoption gate,
  but timed: the 2026-10-26 Decision waits for about three months of use in
  Cairn, LHM and modflow_tools, so the examples come from real use.
* **Governance-regime axis**, **self-instrumenting maturity layer**, and the
  **governed AI-community-contributor scope** -- behind the gate; community
  governance should answer actual contributors' needs, and a public release
  alone does not create them.

Retired from this list 2026-10-01: the pre-0.3 friction package (shipped in
0.3.0) and the per-project efficacy-data primitive, which Anchor 21's
measurement discipline and the retired metrics program argue against building
-- a short retrospective on existing artifacts is the instrument, not a new
collection layer.

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
    moves into Cairn.)*  **Three 2026 results cut against the simplest
    reading.**  A study of 10,664 agent trajectories across nine models finds
    that **step count, not context length, drives long-horizon degradation,
    and that constraining context *accelerates* decay** (Mittal, *How Fast Do
    Agents Rot?*, [arXiv:2609.01660](https://arxiv.org/abs/2609.01660)).
    *Evaluating AGENTS.md* (Gloaguen et al., final version 2026-09-29,
    [arXiv:2602.11988](https://arxiv.org/abs/2602.11988)) finds repository
    context files do **not** generally improve task success, cost over 20%
    more inference on average, and help only where they specify non-standard
    practices — agents followed the instructions; the repository overviews
    model providers recommend were simply not useful.  And the rule-file
    mining study under Anchor 17 (arXiv:2606.12231) finds such files are
    mostly low-level workflow and formatting, updated mainly as corrective
    negative constraints after an error.

Three things follow -- two of them the **framework's own contribution**, where
it leads the literature rather than borrows from it (as with the AI-team-first
lifecycle, User Agent, and stigmergic-coordination contributions):

* **Lean is a cost, a routing-reliability, and a *currency* property; whether
  it is also a correctness property is contested.**  The length effect is real
  (EMNLP 2025) and the inference from it -- that a fat always-loaded prefix
  degrades accuracy -- is now contradicted by the step-count result, so this
  document no longer leans on it.  What is not contested: an instruction file
  earns its tokens only where it states what the agent would not otherwise
  know, and a stale or generic one is pure cost.  That is the backbone under
  the **adoption promise** ("keep the apparatus only as heavy as your codebase
  and team earn") and under the `RULES.md`-as-router design: a small
  always-loaded bright-line set + a routing table to on-demand docs *is*
  progressive disclosure, and the maturity ladder (Horizon 2) is its
  **profile-sizing** control.  Keep the instructions whose useful effect is
  demonstrated; no universal token threshold is justified.
* **A governed, measured always-loaded token budget is a Cairn lead.**  The
  literature supplies the measurement primitives (≈100 tokens per skill;
  the finite-attention-budget framing) and, as of 2026, the nearest
  neighbours (the AGENTS.md evaluation; the rule-file taxonomy), but **no
  surveyed source describes a governed, measured always-loaded budget as a
  standing engineering control**.  That is the framework's to define, applied
  to the apparatus's own context weight -- and the budget is as much about
  rule *quality and currency* as about size.
* **The `sessions × agents × adopters` fan-out is a Cairn lead.**  All
  verified work is single-agent / single-session.  The shared-context
  economics of *one* always-loaded doctrine file read by *many* agents
  across *many* adopters -- the multiplier that makes a heavy Cairn prefix
  expensive at scale -- is unmodeled in the surveyed literature.  Like the
  stigmergic-coordination contribution, it is a distinctive position worth
  holding onto as such.

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
* Making the repository public, or any other public-surface action -- those
  are maintainer-performed.

Cairn's current structure is organically derived and load-bearing; the horizons
extend it, they do not replace it.  Concrete moves go through the normal Cairn
PR-flow / proposal cycle.  The guide star remains the scientist's work, not
Cairn's growth.

## Review -- Antigravity (Gemini 4 Argon, Reviewer) -- 2026-10-26

*(Temporary review section per `dev/strategy/_template.md:45-55` — to be folded in inline and deleted by the author.)*

```
Reviewed commit: 747d56c9f1cc6d7a2cbab0e9f26020140a61de0d (file last modified at 68268b4b3c7501a38c7d3efc7d6f77c4314156d7)
Target: full strategy note (`dev/strategy/2026-05-14-claude-human-ai-team-development-framework.md`)
```

**Foundations**:
1. **Should this exist as framed?** Yes; the guide star's core thesis — delegating coding without losing control of scientific assumptions, evidence, and decisions, with all future horizons gated on comparative outside-adoption evidence — is sound, though four sections have drifted behind `0.5-dev` doctrine or contradict other parts of the same note. -- `dev/strategy/2026-05-14-claude-human-ai-team-development-framework.md:42-79`, `doctrine/dual-review.md:6-84`, `doctrine/rationale.md:189-317`
2. **Best alternative.** Replacing the 1,444-line living note entirely with `doctrine/rationale.md` would lose the unharvested anchors (11, 12, 14, 15, 18–22), the open-gap list, and the gated horizon analysis; however, shrinking the guide star by pointing harvested anchors (1–10, 13, 16, 17) to `doctrine/rationale.md` rather than maintaining two full copies of their prose is a cleaner medium-term path. -- `doctrine/rationale.md:1-572`, `dev/strategy/2026-05-14-claude-human-ai-team-development-framework.md:110-147`
3. **What would show it wrong.** An outside adoption against the lighter baseline showing no gain in scientific reliability or later comprehension for the added attention (the falsifier already stated in the note), or internal drift severe enough that a collaborator reading the guide star applies retired review rules. -- `dev/strategy/2026-05-14-claude-human-ai-team-development-framework.md:66-79`, `dev/strategy/2026-05-14-claude-human-ai-team-development-framework.md:186-205`

### Summary judgment

The October 2026 revisions (*The promise*, the 2026-08 refocus under *Restraint as design center*, Anchor 20 on operator allocation, Anchor 22 on agent supply-chain incidents, and the Anchor 16 update for Cairn Plain Language 1.0) give this document rare honesty for a methodology project. Downgrading the efficacy claim from "proven" to *"plausible, exercised here, awaiting comparative evidence"* and gating the three horizons behind one outside adoption or worked example protect Cairn from building speculative process.

I found four concrete places where the text has drifted behind current `0.5-dev` files or contradicts itself, plus one structural recommendation to reduce maintenance weight.

### Findings and recommendations

1. **R-1 (Doctrine drift): Four passages still teach the retired two-stance (`Internal` vs. `External`) review model instead of `0.5-dev`'s single stance.**
   * *Where*: Lines 189–197 (the peer-review table and paragraph), lines 243–249 (*What the analysis produced*), lines 345–349 (*What Cairn is today*), and lines 422–423 (*Cairn as a publishable artifact*) define Dual-Review as two stances: `Internal` ("strengthens the change within its own frame") and `External` ("makes it prove it should land; a different agent type or a human is the strongest distance and is recommended, never required").
   * *Why it matters*: Current `0.5-dev` doctrine (`AGENTS.md:12, 59-117`, `doctrine/dual-review.md:6-84`, and `doctrine/rationale.md:398-409`) unified review into **one stance at every stage** ("on the work's side, making it better by questioning its foundations", answering three stage-specific questions in a `**Foundations**` block) and made an **External read** a Maintainer-only, per-artifact commissioned pass (`**Called by**: Maintainer ...`) that agents never select or recommend. Line 154 says operating doctrine wins when they disagree, but leaving the retired definition in four summary sections misleads readers.
   * *Recommendation*: Revise lines 186–205, 243–249, 345–349, and 422–423 inline to state the one-stance, three-question model and the Maintainer-called External read, matching `doctrine/rationale.md:398-409`.

2. **R-2 (Internal contradiction): Lines 548–568 announce a per-project efficacy-data collection move that line 1331 retired.**
   * *Where*: `### The trust paradox of empirical-data infrastructure` (lines 548–568) opens with *"An upcoming near-term move (below) ships per-project efficacy-data collection: every Cairn deployment gathers its own data on framework efficacy locally..."* Meanwhile, `### Candidate moves` (lines 1330–1334) states: *"Retired from this list 2026-10-01: ... the per-project efficacy-data primitive, which Anchor 21's measurement discipline and the retired metrics program argue against building -- a short retrospective on existing artifacts is the instrument, not a new collection layer."*
   * *Recommendation*: Remove lines 548–568, or replace them with a two-sentence note that any future comparative study under *The promise* (lines 66–73) uses existing repo artifacts and explicit per-occurrence consent rather than an installed collection layer.

3. **R-3 (Missing half of Anchor 16 + copy defect): Anchor 16 omits the temporal comprehension floor (Naur 1985) that `doctrine/rationale.md` and `docs/plain-language.md` rely on.**
   * *Where*: Lines 522–546 (`### Recipient-calibrated communication and the comprehension floor (Anchor 16)`).
   * *Why it matters*:
     1. Line 524 still says *"The anchor has two legs"* immediately before listing **Leg 1**, **Leg 2**, and **Leg 3** (added in `dc70249d`).
     2. In `doctrine/rationale.md:223-278`, Anchor 16 includes Naur (1985), *Programming as Theory Building*, and the **temporal half of the comprehension floor**: *"a durable artifact must stand without the deliberation that produced it"* (forbidding dead deliberation coordinates such as `F5`, `CR1`, or plan-chunk test names in durable code and tests, bounded by Anchor 17 against over-narration). `docs/plain-language.md:12-13` names that exact failure as one of the three incidents behind Cairn Plain Language 1.0, but the guide star's Anchor 16 section never mentions Naur (1985) or the temporal half.
   * *Recommendation*: Fix *"two legs"* on line 524 and add a short paragraph on Naur (1985) and the temporal half (pointing to `doctrine/rationale.md:223-278`) so both files agree on Anchor 16's scope.

4. **R-4 (Stale version and inventory): Version numbers, the `doctrine/` file list, and "pre-public-flip" phrasing lag the repository.**
   * *Where*:
     1. Line 317 (`"Cairn is at v0.3.0"`) and line 1271 (`"Cairn v0.3 ships the static half"`): `CHANGELOG.md:124` and `CITATION.cff:22` are at **v0.4.0** (released 2026-10-20), with `0.5-dev` active.
     2. Lines 320–322 list `doctrine/` contents as *"collaboration-stance, coordination, doc-governance, dual-review, lifecycle, rationale, roles, session-routines, and the fold-back mechanism."* No fold-back file exists in `doctrine/`, while six current files (`consolidation-review.md`, `lifecycle-contract.md`, `onboarding.md`, `plans.md`, `proposals.md`, `runtime-contract.md`) are missing from that list.
     3. Lines 510 and 1140 refer to Cairn as *"pre-public-flip"*, whereas `CITATION.cff:24-25` already points to a public GitHub repository and Zenodo DOI (`10.5281/zenodo.23500751`).
   * *Recommendation*: Update `v0.3.0` to `v0.4.0` (or cite `CITATION.cff` so the version does not rot on release cuts), replace the enumerated `doctrine/` file list on lines 320–322 with a pointer to `doctrine/README.md` (following line 166's own rule: *maintain the gap list, never the mapping*), and rephrase "pre-public-flip" as "pre-external-adopter".

5. **R-5 (Non-blocking structural suggestion): Point harvested anchors to `doctrine/rationale.md` instead of maintaining two full expositions.**
   * *Where*: At 1,444 lines (~106 KB), the guide star duplicates much of the prose for the harvested anchors (1–10, 13, 16, 17) that now live in `doctrine/rationale.md` (572 lines). That creates two places to update whenever an anchor evolves (as happened with Anchor 16 today).
   * *Recommendation*: On the next major pass, keep each harvested anchor's row in the Anchor Index (lines 123–146) and a one-paragraph summary in the guide star pointing to `doctrine/rationale.md`, reserving full exposition in this file for the unharvested anchors (11, 12, 14, 15, 18–22), *The promise*, *Still open*, and the gated *Horizons*.

**Coverage**:
* **Covered**: Read all 1,444 lines of `dev/strategy/2026-05-14-claude-human-ai-team-development-framework.md` at commit `747d56c9` (last modified at `68268b4b`) and checked its claims against `AGENTS.md`, `doctrine/dual-review.md`, `doctrine/rationale.md`, `doctrine/README.md`, `docs/plain-language.md`, `dev/agent_collaboration.md`, `dev/strategy/README.md`, `dev/strategy/_template.md`, `CHANGELOG.md`, and `CITATION.cff` (Lenses #1 claims, #3 completeness, #5 cross-document consistency, #6 doc drift, #7 lifecycle, #8 domain/restraint, #9 actionable recommendations).
* **Not covered / low confidence**: I did not re-verify external URLs or re-derive the git commit-accounting time series from raw history; prose-only review, no test suite run.
