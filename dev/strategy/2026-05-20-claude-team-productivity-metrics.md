<!-- Migrated 2026-06-12 from modflow_tools dev/strategy/ (Cairn's development home before self-hosting). Authored from modflow_tools' vantage; some path cites and "current state" reflect that origin and are being adapted to Cairn. Preserved as Cairn's living deliberation record -- see dev/strategy/MIGRATION.md. -->
<!-- claim-check-allow: dev/proposals/archive/2026-05-21-claude-lifecycle-metrics-layer-v2.md -->
# Strategy: team productivity metrics for the human + AI development team

**Author**: Claude (Strategy)
**Date**: 2026-05-20 (substantively revised 2026-05-28)
**Status**: living
**Type**: living-reference
**Audience**: maintainer + collaborating AI agents; secondary audience is a scientist (or scientist-team) adopting a structured human + AI development methodology and wanting to know what to measure -- and how the measurement infrastructure itself earns the adopter's trust

## Purpose

**The measurement question is a trust question.**  A human+AI team's data on its own efficacy is the most sensitive material the team produces: it tells the world how the methodology worked, where it failed, who routed what to whom.  Shipping infrastructure that collects that data **requires more adopter trust than not shipping it**.  Trust architecture comes first; the data primitive comes second.  Never the reverse.  See "The trust paradox of empirical-data infrastructure" below + the master guide-star doc's **Anchor 10** (Lin et al. 2020, *The TRUST Principles for digital repositories*, *Scientific Data* 7:144) for the broader framework Cairn's design has been implicitly following.

The modflow_tools project ships **v2A** of a lifecycle-metrics extraction layer (`tools/lifecycle_metrics.py`; v2A landed via the accepted `2026-05-21-claude-lifecycle-metrics-layer-v2` proposal) that turns proposals + plans into structured rows -- author, status, finding counts, time-to-decision, cross-agent-type review rates.  A 2026-05-19 baseline run (via `python -m tools.lifecycle_metrics proposals`, commit `0c30b5e`) quantified the v1 corpus: 51 proposals (49 accepted), mean 7.7 findings per reviewed proposal, 80% cross-agent-type, median time-to-decision 0 days.  Those numbers are historical-baseline values from the v1 era; the corpus has grown substantially since (the 2026-05-28 session alone added a meaningful batch of accepted proposals); a fresh `lifecycle_metrics` run regenerates the current state.

The maintainer raised a follow-on concern at 2026-05-20 chat ~13:34 ET:

> "I think we need more and better metrics for productivity, relative
> per-agent, start/end times, etc.  Things that we can use to track
> changes over time and with practices."

Four distinct asks compressed into one sentence:

1. **Per-agent productivity** (relative comparison; Claude vs. Codex vs. Antigravity vs. maintainer).
2. **Time-of-stage granularity** (start/end times, lifecycle CDF, not just `days_to_decision`).
3. **Time-series tracking** (metrics change over time; historical comparison).
4. **Practice-correlation** (when a doctrine landed, did metrics improve?).

This note positions the four asks against the established literature on software-development productivity measurement -- DORA, SPACE, AI-assisted-coding empirical studies, multi-agent LLM-SE evaluation, open-source community health, the interrupted-time-series methodology, and research-software-engineering practice -- so the subsequent v2 proposal lands at the right scope and avoids two well-documented failure modes: measuring what's easy instead of what matters, and confusing activity with productivity.

Two structural moves drove the original (pre-review) revision:

* **The metrics layer must measure the methodology's effect on *scientific software outcomes*, not just the health of the proposal/plan machinery.**  Lifecycle metrics are necessary instrumentation, but they are not the product.  An outcome layer (workflow capabilities shipped, runnable examples, reproducibility artifacts, defect/rework rate) joins the original four-asks-driven layer as a peer.
* **The metrics layer must be designed forkably for Cairn (the Open Science methodology repository being constructed in parallel), not just usable in modflow_tools.**  Cairn portability becomes its own measurement layer.

**A third move drives the 2026-05-28 rewrite that follows:**

* **The measurement work IS itself a Cairn portability question -- specifically, the question "how does a Cairn deployment empirically demonstrate trustworthiness?"**  TRUST principles (Anchor 10 of the master guide-star) give the answer; Cairn 0.3 Goal 7 gives the concrete primitive; the trust paradox (below) gives the discipline that prevents over-collection.  Cairn portability is no longer the doc's fourth layer -- it is the doc's spine.

This is a strategy artifact, not a proposal.  Strategy notes (per `AGENTS.md > dev/`) are comparative research and long-horizon design context, not commitments.  Per the original framing, the doc seeded a subsequent `lifecycle-metrics-layer-v2` proposal -- **that proposal has shipped** (accepted; v2A's `tools/lifecycle_metrics.py` + the Measurement Compact codified in `AGENTS.md` + the v2A contract test gating per-agent / per-tier external publication).  This doc's residual job is **strategy companion to Cairn 0.3 Goal 7** -- the per-project efficacy-data primitive Cairn ships before public launch.

## The 2026-05-28 reframe -- what shipped + what changed

The session-of-2026-05-28 layered substantial Cairn-side material on top of this doc.  Catalog of what's new:

1. **Lifecycle-metrics v2A shipped** (accepted; per-agent / per-tier dashboards + Measurement Compact contract test + the unconditional local wording ban that bites per-agent / per-tier tokens in `CHANGELOG.md > Unreleased` and adopter-facing docs).  The Measurement Compact's five commitments are now `AGENTS.md` doctrine, not draft text in a strategy note.
2. **Anchor 10 -- Lin et al. 2020 TRUST principles** added to the master guide-star doc.  Five dimensions of trustworthy infrastructure operation (Transparency, Responsibility, User focus, Sustainability, Technology) generalize cleanly from data repositories to research-software-methodology frameworks like Cairn.  Names the surface this doc was implicitly oriented around.
3. **"Trust as design center" section** added to the master guide-star doc.  Maps the five TRUST dimensions onto Cairn's existing doctrine + names the trust paradox of empirical-data infrastructure (below).
4. **Cairn 0.3 Goal 7** added to `dev/PLANNING.md` -- the concrete per-project efficacy-data infrastructure (pre-0.4 / 0.5) the doc's Layer 4 anticipated.  Frames Cairn's first empirical-research paper as a longitudinal study with consenting deployments.
5. **Cross-links from Goal 1 (self-host) and Goal 4 (doctrine introspection)** -- Goal 1 creates Cairn's own instrumentation surfaces; Goal 4 reads the same signals for read-to-update-doctrine purposes (Goal 7 reads them for read-to-archive-for-research).
6. **Cairn-deployment count moved from N=0 to N=2** (modflow_tools + LHM in-flight today).  The "Cairn has zero adopters" framing in the original Cairn-portability section is superseded.

## Trust as the measurement design center

A human+AI team's data on its own efficacy is **load-bearing trust material**.  Releasing it exposes routing decisions, failure modes, agent-comparison framing, decision velocity -- all of which an adopter has a legitimate stake in controlling.  Any framework that ships measurement infrastructure must clear the trust bar BEFORE the data primitive ships.  Cairn's Anchor 10 names the five TRUST dimensions; mapping them onto measurement specifically:

* **Transparency** -- the measurement schema, the collection logic, and the audit trail of "what was collected when, by whom" are public, append-only, and adopter-inspectable.  Cairn-side: lifecycle-metrics output schema is documented; the v2A contract test scans for compact violations; the consent flow doctrine is public.
* **Responsibility** -- the measurement infrastructure is dogfooded before it ships.  Each metric is exercised on the reference deployment(s) under real conditions; no metric ships untested.  Cairn-side: v2A landed on modflow_tools, the reference deployment, with N=2 dimension-corpora (proposals + plans).
* **User focus** -- the adopter chooses what to collect, when to collect, what to share.  No metric is mandatory; default mode is **collection-only-where-consented** with the lifecycle-metrics module's per-deployment opt-in.  Cairn-side: the on-ramp's graduated levels mean an L1 (hand-copy-kernel) adopter doesn't get the same measurement surface as an L2 (full bootstrap) one.
* **Sustainability** -- measurement infrastructure must not silently lock the adopter into Cairn.  Data leaves with the adopter when they exit; collection produces a portable artifact (the on-disk metric tables); no central server, no Cairn-side persisted state.
* **Technology** -- no-network-by-default composition; the export-safety scrub on any outbound artifact; the `content-security` module protects against accidental exfiltration; verify-integrity gates protect against silently-corrupted data.

**Reference**: the master guide-star doc's "Trust as design center" section names the same five dimensions and provides the analog mapping for Cairn's other apparatus.  This section narrows the lens to the measurement infrastructure specifically.

## The trust paradox of empirical-data infrastructure

**Adding a primitive that collects efficacy data requires more adopter trust than not adding it** -- even when the data stays local.  Three trust dimensions tighten when measurement infrastructure ships:

1. **Surveillance vector**: an adopter has to trust that the collection itself doesn't introduce a surveillance pathway.  A metric that captures "time-to-decision per agent" is an audit trail of who decided what when -- benign at the modflow_tools reference scale, sensitive at larger team scales where agent-comparison framing has political weight.
2. **Outreach surface**: the maintainer's future ability to contact participants for a research paper means the data persists with the intent of future research use.  Even if outreach is out-of-band + per-occurrence opt-in, the data's existence presupposes the outreach pathway.
3. **Evaluation drift**: the Measurement Compact's first commitment ("metrics are for system learning, not agent punishment") is **a doctrine commitment**, not a technical guarantee.  As the framework spreads to communities the maintainer cannot personally vouch for, an adopter must trust either (a) every future framework maintainer's good faith, or (b) the framework's structural impossibility of misuse.

**The paradox dissolves when the trust architecture lands before the data primitive itself.**  This is the load-bearing sequencing claim of Cairn 0.3 Goal 7 (below): consent-flow doctrine + data-collection audit trail + no-network-by-default composition + "what is collected + what is not" documentation must all be in place + dogfooded + Cairn-portable BEFORE the primitive ships.  Each Anchor 10 TRUST dimension must be demonstrably checked.

The Measurement Compact (above; now `AGENTS.md` doctrine) closes most of the paradox at the framework-level.  The remaining gap is the per-adopter-deployment surface: every Cairn deployment must be able to verify the trust architecture on its own tree, not just trust that Cairn's framework-level commitments hold.  That verification surface is what Goal 7's pre-shipping work creates.

## Cairn 0.3 Goal 7 -- the concrete realization of Layer 4

The original (2026-05-20) doc's Layer 4 framed Cairn-portability metrics as "design-only in modflow_tools; Cairn-side / v3 instrumentation."  The 2026-05-28 PLANNING.md edit promoted that anticipated work into the Cairn 0.3 milestone roadmap as **Goal 7 -- Per-project efficacy-data infrastructure (pre-0.4 / 0.5)**.

**What Goal 7 collects** (working list, per the PLANNING entry):

* The lifecycle-metrics module output (v2A's per-agent / per-tier rows, the Measurement Compact's bounded surface).
* The collision log (`dev/measurement/collision_log.md`).
* The intent log (`dev/intents.jsonl`).
* The fold-back ledger.
* Maturity-ladder transition timings (Cairn's on-ramp moves: read-doctrine -> hand-copy-kernel -> full-bootstrap).
* Saugatuck-style pilot metrics from the methods.md generation arc -- time-to-first-draft, edit fraction, citation accuracy, drift rate.  See Cairn's master Tier 5 (methods.md as build artifact) for the full per-metric provenance.

**What Goal 7 does NOT collect**: anything outside the deployment's already-instrumented surfaces; no source code; no scientific content; no commit messages; no personal identifiers.  Data **stays local** -- no telemetry, no auto-upload, no central server, no implicit consent.

**Out-of-band research outreach**: the maintainer reaches out to participants when a research paper warrants; participation is per-occurrence opt-in; co-authorship is offered.  See PLANNING.md > Cairn 0.3 Goal 7 for the full sequencing.

**Goal 7's sequencing within the Cairn 0.3 milestone list**:

* **Depends on Goal 1 (self-host `cairn/dev/`)** -- Goal 1 creates the surfaces the primitive reads from (Cairn's own `dev/intents.jsonl`, `dev/upstream/`, lifecycle-metrics output).  Cairn cannot collect efficacy data on its own apparatus until its own apparatus is self-hosted.
* **Shares signals with Goal 4 (doctrine introspection)** -- both read collision-log recurrence, lifecycle-metrics drift, repeated patterns.  Goal 4 reads to update doctrine; Goal 7 reads to archive for the longitudinal-study consent flow.  The two are complementary; they share the underlying instrumentation surface.
* **Independent of Goals 2, 3, 5** -- can land in parallel with the governance-models / PR-workflow / strategy-doc-fold-back work.

**Goal 7's verification gate**: each Anchor 10 TRUST dimension must be demonstrably checked on the data primitive before adopters are asked to commit to running it (per the trust paradox section above).  The dogfood happens on modflow_tools first; the LHM adoption is the second exercise; only then does the primitive ship as a default-on Cairn module.

## Framework anchors

Eight citable frameworks bound the gap analysis:

1. **DORA / Accelerate** -- Forsgren, N., Humble, J., & Kim, G. (2018). *Accelerate: The Science of Lean Software and DevOps.*  Four-key metrics for software delivery performance: Deployment Frequency, Lead Time for Changes, Change Failure Rate, Mean Time to Recovery.  In 2023 the recovery metric was redefined and renamed to *Failed Deployment Recovery Time*; in 2024 the framework added a fifth metric, *Deployment Rework Rate*.  The 2025 DORA Report (published at [dora.dev/research](https://dora.dev/research/); specific URL anchor depends on the report's stable form -- to be re-cited precisely at v2-proposal time) found that AI adoption improves throughput but increases delivery instability.  That is a directional finding from DORA's industry survey and merits the standard hedge that subsequent meta-analyses may revise the magnitude; the direction is the load-bearing claim, not the effect size.  Canonical metrics reference: [dora.dev/guides/dora-metrics-four-keys](https://dora.dev/guides/dora-metrics-four-keys/).

2. **SPACE framework** -- Forsgren, N., Storey, M.-A., Maddila, C., Zimmermann, T., Houck, B., & Butler, J. (2021). *The SPACE of Developer Productivity: There's more to it than you think.*  ACM Queue 19(1).  [queue.acm.org/detail.cfm?id=3454124](https://queue.acm.org/detail.cfm?id=3454124).  Five-dimension model premised on "no single metric can capture developer productivity accurately": **S**atisfaction & well-being, **P**erformance, **A**ctivity, **C**ommunication & collaboration, **E**fficiency & flow.  Lead author Forsgren's framing: productivity is multidimensional; one-number capture consistently produces decisions on incomplete information.

3. **AI-assisted coding empirical productivity** -- multiple recent studies anchored on GitHub Copilot:
   * Peng, S. et al. (2023). *The Impact of AI on Developer Productivity: Evidence from GitHub Copilot.*  Controlled study; ~55% productivity gain on a specific task (single study; subsequent meta-analyses show smaller effect sizes that vary sharply by task type).  [researchgate.net/publication/368473822](https://www.researchgate.net/publication/368473822_The_Impact_of_AI_on_Developer_Productivity_Evidence_from_GitHub_Copilot).
   * GitClear (2025). *AI Copilot Code Quality.*  Quality-side counterweight: AI-coauthored PRs show ~1.7× more issues than human-only PRs; ~4× growth in code clones.  [gitclear.com/ai_assistant_code_quality_2025_research](https://www.gitclear.com/ai_assistant_code_quality_2025_research).
   * Maintainability study -- Krasniqi, R., & Do, H. (2024). *Does Co-Development with AI Assistants Lead to More Maintainable Code? A Registered Report.*  [arXiv:2408.10758](https://arxiv.org/pdf/2408.10758).
   * Two findings recur across studies: (a) task-specific productivity varies sharply (boilerplate / tests = high gain; complex algorithms / security-critical work = modest gain); (b) ~11-week learning curve before measured gains stabilize -- most users abandon before they reach steady-state.

4. **Multi-agent LLM-SE evaluation** -- the closest-fit anchor for our specific team shape:
   * **A Catalogue of Evaluation Metrics for LLM-Based Multi-Agent Frameworks in Software Engineering** (AGENT 2026 workshop at [ICSE 2026](https://conf.researchr.org/details/icse-2026/agent-2026-papers/13/)).  37 metrics across four categories: **Outcome**, **Process**, **Product**, **Framework**.  Combines 26 existing metrics with 11 newly-proposed.  Names the inconsistency problem -- evaluation practices in this area remain fragmented; frameworks "rely on self-defined or inconsistent metrics."
   * Liu, J. et al. (2024).  *LLM-Based Multi-Agent Systems for Software Engineering: Literature Review, Vision, and the Road Ahead.*  ACM Transactions on Software Engineering and Methodology.  [doi:10.1145/3712003](https://dl.acm.org/doi/10.1145/3712003).

5. **CHAOSS -- Community Health Analytics in Open Source Software** -- a Linux Foundation project ([chaoss.community](https://chaoss.community/)) that ships implementation-agnostic metrics for OSS-project health.  Three relevant metric families: **Activity** (commits, issues, PRs over time), **Responsiveness** (time-to-first-response, time-to-resolution), and **Contributor sustainability** (active-contributor counts, retention).  Tooling (Augur, GrimoireLab) is operational, not just theoretical.  CHAOSS treats community / contributor data as first-class -- the closest established analog to our per-agent ask.

6. **Interrupted Time Series (ITS) analysis** -- the methodology anchor for "track changes with practices."  Established in policy / healthcare evaluation; software-eng applications growing.  ITS quantifies the impact of an intervention by comparing repeated observations before and after, separating *level change* (immediate effect) from *slope change* (sustained trend effect).  Software tools: Stata's `itsa` command; the Robust ITS (RITS) toolbox.  Foundational reference: [Wagner, A. K. et al. (2002)](https://pubmed.ncbi.nlm.nih.gov/12174032/) on segmented regression for ITS.  For our case: each doctrine commit is in principle an intervention -- with substantive coupling caveats addressed under "Methodological cautions" below.

7. **Research Software Engineering (RSE) / scientific-software practice** -- modflow_tools is scientific software, not general-purpose SaaS.  RSE-community guidance bears directly on what to measure:
   * The [FAIR4RS principles](https://www.rd-alliance.org/group/fair-research-software-fair4rs-wg) (Findable, Accessible, Interoperable, Reusable for Research Software).
   * The [Better Scientific Software project](https://bssw.io/).
   * Carver, J. et al. on scientific software development practices.
   * Anchor implication: "shipping verified science" is a different metric target from "shipping working software."  Numerical correctness, calibration validity, computational reproducibility, paper-grade verification are first-class outcomes that general-SE metrics underweight.

8. **Three Ways of DevOps + adaptive software methodologies** -- the anchor for the *closed-loop* concept (metrics drive doctrine + tool changes, not just describe state):
   * Kim, G., Behr, K., & Spafford, G. (2013). *The Phoenix Project*; Kim, G., Humble, J., Debois, P., Willis, J., & Allspaw, J. (2021). *The DevOps Handbook* (2nd ed.).  [The Three Ways](https://itrevolution.com/articles/the-three-ways-principles-underpinning-devops/): the **First Way** (systems flow), the **Second Way** (amplify feedback loops -- shorten cycles, embed knowledge where it's needed, learn from defects quickly), and the **Third Way** (continual experimentation, taking risks, learning from failure; allocate time for improvement of daily work).  The Second + Third Ways together name the concept the maintainer raised at 2026-05-20 chat ~16:18 ET: metrics on productivity should *dynamically turn into changes in AI team structure and tools*.
   * Highsmith, J. (1990s). *Adaptive Software Development (ASD)* -- the speculate / collaborate / learn cycle; methodology that adapts from each iteration's feedback.  [Overview](https://www.geeksforgeeks.org/software-engineering/adaptive-software-development-asd/).
   * Deming, W. E. *Plan-Do-Check-Act (PDCA)* cycle -- the foundational continuous-improvement primitive.  Adopted in software through Lean Software Development's "amplify learning" principle.
   * Anchor implication: a measurement layer that *only* measures is a missed opportunity.  The harder question is what triggers what change, with what guardrails against measurement-driven over-correction (the Goodhart amplification risk).  Cairn-specific framing: methodology-as-software, with versioning, adopter feedback, and explicit feedback-loop discipline rather than fixed doctrine that ages out.

These eight anchors -- DORA for delivery-level metrics, SPACE for multi-dimensional caution, AI-assisted-coding empirics for what's been quantified in adjacent settings, multi-agent LMA evaluation for our team's specific shape, CHAOSS for contributor / community metrics, ITS for practice-correlation methodology, RSE for scientific-software-specific outcomes, and Three Ways / ASD / PDCA for the adaptive-doctrine closed loop -- bound the design space for a lifecycle-metrics v2.

## Current state -- what v1 measures

`tools/lifecycle_metrics.py` (single-file extractor at baseline-snapshot scale; accepted via the `2026-05-18-claude-lifecycle-metrics-layer` proposal) emits two CSVs:

**Per-proposal** (16 columns): `stem`, `author`, `date_opened`, `status`, `decision_date`, `days_to_decision`, `review_rounds`, `reviewer_agents`, `cross_agent_type_review`, `human_review`, `external_tier_review`, `revised`, `total_findings`, `findings_p1/p2/p3`.

**Per-plan** (6 columns): `stem`, `status`, `plan_review_rounds`, `code_review_rounds`, `paired_proposal`, `paired_proposal_reliability`.

The 2026-05-19 baseline run (historical snapshot, not live count):

* 51 proposals (49 accepted / 0 rejected / 0 superseded)
* 50 of 51 reached a Revised-proposal stage
* Mean 7.7 findings per reviewed proposal
* 80% reviewed cross-agent-type
* Median `days_to_decision` = 0 days

V1 is read-only on the corpus, regenerates from in-file headers, parses prose-structured artifacts (not a separate schema database), and documents its reliability tiers (exact / good / best-effort).

## Mapping the maintainer's four asks against the anchors

### Ask 1 -- per-agent productivity (with decomposition)

"Per-agent" is doing more semantic work than it first appears.  Four axes hide under the single word:

* **Agent-as-identity**: Claude vs. Codex vs. Antigravity vs. the human maintainer.
* **Agent-as-model-tier**: Opus 4.7 vs. Sonnet 4.6 vs. Codex (GPT-5) vs. future tiers.  Today's role-based-model-selection doctrine routes tier by task complexity; tier comparisons that don't normalize by task complexity measure *routing policy* as much as model capability.
* **Agent-as-role**: Strategy author vs. External Reviewer vs. Implementation vs. Internal Reviewer vs. User Agent.  Codex frequently performs External Review; Claude drafts long arcs.  Finding counts, proposal counts, revision rates partly measure *assignment policy*, not agent performance.
* **Agent-as-session**: each conversation is its own session-state; the same model in two parallel sessions is structurally two agents for coordination purposes.

The right framing per SPACE and per the multi-agent LMA evaluation literature: per-agent measurement is a *system diagnostic*, not an *agent-ranking surface*.  Decomposed reporting:

* **Per-role workload distribution** -- comparable across agents in the same role.
* **Per-model-tier productivity** -- comparable if normalized by task complexity / role.
* **Per-actor distribution** -- the human maintainer vs. the AI collectivity is a different analytical surface (different role, different cost structure, different evaluation criteria).
* **Per-session activity** -- only meaningful when correlated with calendar time / concurrency context.

**Anchor coverage**: SPACE's *Activity* + *Communication & collaboration* are explicit; the AGENT 2026 catalogue's *Process* category includes per-agent contribution metrics; CHAOSS treats contributor-activity as first-class; AI-assisted-coding empirics validate that per-developer comparison is established practice (with the same warnings about confounding).

**V1 coverage**: partial.  `author` is captured per proposal; `reviewer_agents` per review.  The `**Model**:` header field added by today's role-based-model-selection doctrine is not yet extracted.  Aggregation into a per-agent summary is not emitted -- a user has to group_by manually.

**What v2 should add**: see "Recommended v2 scope > Layer 2 -- Collaboration metrics" below.

### Ask 2 -- start/end times and lifecycle granularity

**Anchor coverage**: DORA's *Lead Time for Changes* is the canonical timing metric; SPACE's *Efficiency & flow* tracks interruption / handoff timing; AGENT 2026's *Process* category includes per-stage timing.

**V1 coverage**: `days_to_decision` only.  Section-header dates exist in source files (each Review / Response / Decision section has a `-- YYYY-MM-DD` header) but are not extracted as per-stage timestamps.

**What v2 should add**: see "Recommended v2 scope > Layer 1 -- Flow metrics" below.

**Sub-day granularity question**: section headers carry dates, not timestamps.  Sub-day timing would require either commit-timestamp cross-reference (git log -- already a v2 follow-up of v1) or an explicit timestamp convention in headers.  Lean: git log cross-check, no doctrine change.

### Ask 3 -- time-series tracking (changes over time)

**Anchor coverage**: DORA time-series IS the framework; SPACE is multi-temporal by design; CHAOSS tooling emits dated trend data; ITS requires time-series with marked interventions; GitClear's 2025 finding of *growing* code-clone rate is itself a time-series finding -- the harms compound.

**V1 coverage**: none.  The CSV regenerates from the current-state corpus.  The 2026-05-19 baseline is regenerable as a number but not as a *snapshot* -- the CSV at the baseline-run commit has the same content as a regeneration today only by coincidence; an intervening proposal accept changes everything.

**What v2 should add**: see "Recommended v2 scope > Layer 1 -- Flow metrics" (snapshots).  **Cadence note** (per Codex's review): event-triggered snapshots primary (after proposal-archive, after plan-archive, after goodnight, before/after named methodology interventions), calendar-cadence secondary.  This team works in bursts; calendar-only oversamples quiet periods and undersamples high-change days.

### Ask 4 -- practice-correlation (changes with doctrine)

**Anchor coverage**: ITS is the methodology, full stop.  Wagner et al. (2002)'s segmented regression for ITS is the canonical pattern.  DORA-style cross-team correlation is the broader research framing.

**V1 coverage**: none.  V1 has no intervention-annotation surface.

**What v2 should add**: see "Recommended v2 scope > Layer 1 / Layer 2" (annotation file + before/after deltas, with annotations framed as *small causal hypotheses* not date labels).

**Critical methodological caveat -- doctrine-churn coupling**: today's session landed 5+ doctrine commits within hours (`90cdd76` work-intent required-signal+read; `13f60c2` NEXT_SESSION rewrite-from-scratch; `2ef4864` PLANNING completed-sweep; `cf2f45e` + `3ac3f3b` role-based-model-selection; `5dfeecd` proposal-cycle-clarifications).  For ITS analysis these are **coupled interventions**, not independent point-events.  You cannot attribute any subsequent metric shift to any single doctrine without controlling for the others.  Three responses available -- the v2 proposal must pick:

* **Cluster the interventions**.  Treat clusters of doctrine commits within one session as a single intervention.  Loses resolution; preserves causal inference.
* **Spread the interventions deliberately**.  Doctrine-work pacing as a process discipline -- one doctrine change per calendar day, not five per session.  Aligns with small-N reality; makes ITS tractable.
* **Accept the limit**.  Report findings as *directional*, not causal.  Match the small-N framing already in this note.

## Beyond the four asks -- the science/product outcome layer

The four asks above cover *coordination mechanics* -- how the team's lifecycle machinery moves work through proposal -> review -> decision -> implementation.  The maintainer's larger goal is not measured by these alone: world-class MODFLOW workflows, faster scientific modeling, reproducible notebooks/configs, a Cairn methodology reusable across scientific codebases.

Lifecycle metrics are necessary instrumentation but not the product.  Without an outcome layer, the v2 dashboard could tell us the team reviews faster and collides less while missing whether modflow_tools is becoming more capable, more reliable, and more useful to scientists -- the exact activity-vs-productivity failure mode SPACE warns about.

**Outcome-layer candidate measures**:

* **Capability coverage**: shipped user-facing workflows by tier (build, review, calibration, delivery, particle tracking, visualization, teaching).  Each workflow has: runnable example, smoke test, docs, user-guide entry.
* **Runnable-artifact health**: notebooks that execute cleanly top-to-bottom; CLI examples that run as documented; configs that load without warnings.
* **Reproducibility-artifact production**: configs, delivery packages, benchmark baselines, generated schema docs, snapshot files.
* **Post-ship defect / rework rate**: per capability surface, follow-up amendments / sharpening commits / revert events within rolling windows.  Maps to DORA's *Deployment Rework Rate* (the 2024 fifth metric).
* **Time-from-proposal-to-working-workflow**: not just `days_to_decision`, but `days_to_documented_runnable_user_facing_workflow`.  A proposal accepted is not a workflow delivered.
* **Maintainer-reported friction reduction**: qualitative signal -- specifically, time saved or friction removed on real hydrogeology tasks the maintainer has been doing.  N=1 today; structurally available; matters more than most quantitative metrics for "is this serving the science."

The outcome layer joins coordination metrics as a *peer*, not a subordinate.  In v2's report shape: a coordination-metric improvement that doesn't move outcomes is a problem to investigate, not a win.

## Cairn portability -- the methodology's transfer test

Cairn (the Open Science methodology repository) is the natural home for *exportable* measurement methodology.  **As of 2026-05-28: Cairn v0.2.0 is cut; the two deployments are modflow_tools (reference instance) + LHM (adoption in-flight)**.  The "today, Cairn has zero adopters" framing in this section's original (2026-05-20) version is superseded -- portability is now measurable as N=2 with a third-party N=3 anticipated for 0.3.

Cairn portability is the doc's spine, not its fourth layer.  The concrete plan for measuring it is **Cairn 0.3 Goal 7** (above) -- the per-project efficacy-data infrastructure ships pre-0.4 / 0.5, before community adopters arrive.  Anchor 10's TRUST dimensions gate the primitive: each must be demonstrably checked before adopters are asked to commit to running it.

**Cairn-portability-layer candidate measures** -- each is a per-adopter measurement event; the modflow_tools N=1 baseline exists; LHM adoption produces N=2; the third-party N=3 baseline lands during 0.3's external correctness probe:

* **Bootstrap time**: how long does it take a cold-start single agent to bootstrap Cairn into a target repo with its assessment / proposal / plan / review-loop / goodnight surfaces?
* **Customization burden**: number of local customizations required to make Cairn fit the target repo.
* **Adoption coverage**: of Cairn's methodology modules, how many were adopted vs. skipped?  Which were skipped and why?
* **Friction reports**: doctrine edits and adopter friction observations after first use.  (The adopter-friction package, accepted 2026-05-28, ships static entry-surface artifacts that ARE the first attack on this metric.)
* **Time-to-first-reviewed-implementation**: from Cairn bootstrap to the first proposal-cycle-completed implementation in the target repo.
* **Saugatuck-style pilot metrics** (the methods.md generation arc's gate): time-to-first-draft, edit fraction, citation accuracy, drift rate.  See Tier 5.5 (Saugatuck first-pilot dogfood) for the per-metric provenance.

For each measurement choice, a **forkability test**: would another scientific-software team be able to run this measurement on their own corpus, against their own agents, with their own doctrine commits?  Tag each metric: *generic* (reusable across teams) or *modflow_tools-specific* (configuration / customization needed for adoption).  The v2A `lifecycle_metrics.py` ships the forkable contract surface; Goal 7 ships the consent + collection wrapper around it.

## Three data sources v1 doesn't ingest but should

Three new data sources landed today that v2 should treat as first-class inputs:

1. **`dev/measurement/collision_log.md`** -- accepted by the R2 staged-index-collision-assessment proposal (`2026-05-20-claude-r2-staged-index-collision-assessment`).  Records true-staged-index collisions, prevented overlaps, and parallel non-conflicts.  Direct measurement of coordination-failure / coordination-prevention rate.  Maps to AGENT 2026 *Framework* category and SPACE *Communication & collaboration*.

2. **`**Model**:` field on author / reviewer / responder section headers** -- introduced today by the role-based-model-selection doctrine (`cf2f45e`).  Enables per-tier comparative analysis with the decomposition framing above.  Maps to all seven anchors; most directly to AI-assisted-coding empirics.

3. **Goodnight-day reflection files in `dev/reflections/`** -- gitignored and ephemeral *by design*.  This is in tension with using them as a measurement source.  Two options for the eventual v3 or follow-on proposal:
   * **Migrate selected fields at goodnight** (lossy but preserves the channel's ephemeral character).
   * **Change the reflection doctrine** to structured frontmatter and tracked (durable but contradicts the original design intent of "things that don't need to survive context loss").

   The v2 proposal should leave reflections untouched.  A satisfaction-proxy is a v3 / separate-proposal direction.

## Recommended v2 scope -- four layers, staged into v2A / v2B / v3

Restructured into four layers (each addresses a different evaluation purpose).  The four-asks → four-layers numerical symmetry is convenient but is not a 1-to-1 mapping: Layers 1-2 are primarily ask-derived (Layer 1 covers asks 2 and 3; Layer 2 covers ask 1 with overlap into ask 4), Layer 3 absorbs the science/product outcome structural-move and parts of ask 4 (practice-correlation manifests partly here as rework-within-window), and Layer 4 absorbs the Cairn-forkability structural-move (no ask-derivation; it derives from the second structural move in the Purpose section).

**Staging discipline** (load-bearing).  The four-layer scope is the destination; it is not what v2 ships in one cut.  Trying to implement all four layers fully would produce a metrics platform before the team has learned which measurements actually change behavior -- the "build it all, learn from none" failure mode.  The v2 proposal must explicitly stage:

* **v2A -- operational minimum** (the first shippable slice).  Layer 1 (per-stage timestamps + conservative-cadence snapshots), Layer 2 (`**Model**:` extraction, per-role/per-tier summaries, collision-log ingestion, author × reviewer matrix), and the Metric Contract table across both.  Review-yield disposition shipping in v2A requires a proposal-template amendment for explicit disposition markers (see Layer 2 below); historical extraction is best-effort-only.
* **v2B -- quality / outcome layer** (the follow-on).  Layer 3 fully, gated on the workflow-outcomes registry (see Layer 3 below) as the source-of-truth.  Ships after v2A is in service and the team has confirmed which v2A metrics actually feed back into doctrine / tool changes.
* **Cairn-side / v3** (deferred outside modflow_tools).  Layer 4 (Cairn portability), versioned doctrine (mechanism 5 of the adaptive-doctrine surface), reflection-derived satisfaction proxies, A/B doctrine testing (mechanism 4), doctrine sunset surface (mechanism 7).  Modflow_tools v2 ships forkable metric *contracts* that Cairn can consume; the *Cairn-specific instrumentation* lands in Cairn once the first adopter exists.

The staging is not a hedge against ambition; it is the discipline that lets each slice teach the next one's design.  Codex's framing (round-2 External review, finding P1 #1): "build the smallest metrics layer that can tell us whether the process is improving scientific software outcomes, then let the adaptive loop learn from that."

### Layer 1 -- Flow metrics

What: stage timing, latency distributions, snapshot history.

* **Per-stage timestamps**: extract per-section dates (review / response / decision) from header conventions; emit per-stage deltas and lifecycle CDF (p25/p50/p75/p95) rather than just median `days_to_decision`.
* **Event-triggered committed snapshots** (with retention discipline).  Dated CSV snapshots in a new directory.  Event triggers must be tightened against churn -- the v2A default is conservative: snapshot after **plan-archive** and at **goodnight**, plus **before / after named doctrine-intervention events**.  Proposal-archive events do *not* trigger snapshots by default (proposal-archive frequency is too high; let plan-archives absorb the signal).  Same-day events coalesce into one `YYYY-MM-DD-N` snapshot rather than producing N separate commits.  High-frequency snapshots may be pruned or rolled up after release boundaries.  v2 proposal decides explicitly: do snapshots live as tracked artifacts in this repo, or as release/analysis artifacts outside the hot working tree?  Each snapshot records its commit hash for reproducibility.
* **Doctrine-intervention annotations** as small causal hypotheses.  A new tracked annotation surface (file *or* directory -- shape decided in v2 proposal) captures dated doctrine-change events.  Each annotation names: the eligible artifact types; the expected affected metric(s); the hypothesized direction of change; the minimum observation window; known confounders (e.g., unusually concurrent Cairn work, large implementation arc).  Without these fields, annotations become date labels rather than testable claims.
* **Annotation governance + collision discipline**.  The doctrine-committing agent writes the annotation in the *same commit as the doctrine change* (mirroring the CHANGELOG-with-its-change pattern).  Goodnight owner verifies coverage at scrub.  Append-only at the file level.  **Collision-doctrine choice for v2 proposal**: either (a) a single annotation file added to the shared-communication-file roster in `AGENTS.md > Shared communication files` with explicit cadence + signal-and-read rules, accepting that high-touch doctrine commits will compete for it; or (b) one annotation file per intervention under a new per-intervention directory, eliminating the single-file contention at the cost of more files to parse.  Strategy lean: option (b) -- per-intervention files compose better with the work-intent doctrine and the doctrine-churn coupling caveat below.
Proposed path: `dev/metrics_annotations/`.

*Anchors*: DORA Lead Time + 2024 fifth metric (Deployment Rework Rate, used in Layer 3); SPACE Efficiency & flow; AGENT 2026 Process; ITS methodology; CHAOSS time-series.

### Layer 2 -- Collaboration metrics

What: per-role / per-tier distributions, review matrix, collision log, review yield.

* **Per-role + per-tier summary view**: new derived report -- one row per (agent, role, model_tier) tuple.  Columns: workload by lifecycle stage (proposals authored, reviews performed, etc.), mean findings raised when reviewing, mean findings received when authoring, revision rate when authoring.  Surfaced as **system diagnostic** not agent ranking; the Measurement Compact below names the interpretation rules.
* **`**Model**:` field extraction**: parse the new header field added by today's role-based-model-selection doctrine.  Required to do the per-tier surface honestly.
* **Author × reviewer matrix**: which agent-pairs review each other's work.  Surfaces structural-independence patterns (frequently same-agent-type pairs are a coverage gap).
* **Review yield + disposition labels**: parse Response sections for per-finding dispositions (`accept (rewrote inline)`, `accept (merged at <sha>)`, `reject`, `defer`).  Emit: findings raised vs. accepted vs. rejected vs. deferred per reviewer, per review-tier, per agent.  Distinguishes "rigorous reviewer" from "false-positive-pressure reviewer" -- without disposition the finding count is ambiguous.  **Schema-change prerequisite**: the historical corpus uses varied language for dispositions (accepted, partially accepted, addressed, deferred, modified, not accepted, implicitly handled in implementation).  Reliable extraction requires an explicit disposition-marker grammar going forward.  v2A ships a small **proposal-template amendment** adding a finding-disposition marker convention (e.g., one of the four normalized verbs in a leading code-spanned token); historical Response-section extraction is best-effort-only.  Without the template amendment, this metric line is a slogan, not a signal.
* **Collision-log integration**: parse the just-accepted `dev/measurement/collision_log.md` and emit collision-rate metrics per rolling window.  Directly feeds the R2 14-day re-open trigger.

*Anchors*: SPACE Activity + Communication & collaboration; CHAOSS contributor-activity + responsiveness; AGENT 2026 Process + Framework; AI-assisted-coding empirics (per-developer measurement is established practice but confounding caveats apply).

### Layer 3 -- Quality and outcome metrics (gated on workflow-outcomes registry)

What: post-ship defect/rework signals + the science/product outcome layer.  **Ships in v2B, not v2A.**  Layer 3 has a hard prerequisite the other layers don't: a canonical *source of truth* for what counts as a "shipped user-facing workflow."  Without a tracked registry, every Layer 3 measure becomes a brittle inference contested at each release.

* **Workflow-outcomes registry (NEW v2B precondition)**: a small tracked file (proposed path declared at v2B-proposal time; lean: a single Markdown table or YAML list under `dev/`) with one row per user-facing workflow.
Proposed paths: `dev/workflow_outcomes.md`, `dev/workflow_outcomes.yml` (one of these; v2B proposal picks).  Columns: `workflow_id`, `tier`, `user-facing docs path`, `runnable example path`, `smoke test path`, `contract/integration test paths`, `first accepted proposal stem`, `first working commit hash`, `current status`.  The registry is the *authoritative source* for Layer 3's outcome metrics.  Without it, "shipped-workflow coverage" is guesswork.  Registry rows are added at workflow-acceptance time by the implementing agent; goodnight owner verifies coverage.
* **Rework-within-window**: did a follow-up proposal / sharpening commit on the same workflow row land within X days of acceptance?  Map to DORA's *Deployment Rework Rate*.  Tunable window; 14- and 30-day defaults.  Reads the registry, not the proposal corpus alone.
* **Shipped-workflow coverage**: count of registry rows where (runnable example AND smoke test AND docs entry) are all present.  Time-series.
* **Runnable-artifact health**: cleanly-executing notebooks, configs that load without warnings, CLI examples that run as documented.  Goodnight or release-prep cadence.  Registry rows whose runnable-example paths fail at runtime get a `health=failing` flag.
* **Reproducibility-artifact production**: configs, delivery packages, benchmark baselines, generated schema docs per period.  Counted independently of registry (reproducibility artifacts aren't always workflows).
* **Time-from-proposal-to-working-workflow**: registry's `first accepted proposal stem` -> `first working commit hash` delta.  A *workflow-delivery* lead time peer to the *decision* lead time.  Distinguishes "shipped a proposal" from "shipped a workflow."
* **Maintainer-reported friction**: explicitly qualitative; structured intake (could be a reflection-channel field migrated at goodnight per the data-source note above).  N=1 today; high information density.

*Anchors*: DORA Deployment Rework Rate (the 2024 fifth metric); RSE / scientific-software outcomes; AGENT 2026 Product + Outcome categories; GitClear's quality-counterweight findings.

### Layer 4 -- Cairn portability metrics -- now Cairn 0.3 Goal 7 (2026-05-28 update)

**Status superseded by Cairn 0.3 Goal 7** (per `dev/PLANNING.md` >
"Cairn 0.3 milestone goals" > Goal 7).  The original (2026-05-20)
"design-only in modflow_tools; Cairn-side / v3 instrumentation"
framing is now stale: Goal 7 is the concrete pre-0.4 / 0.5 plan that
ships the Cairn-side primitive.

The modflow_tools v2A contribution to Goal 7's primitive: the forkable
metric *contract* surface (`tools/lifecycle_metrics.py` shipped its
outputs in the Metric Contract table format) is in place, and the
generic-exporter hook is ready for the Goal 7 primitive to consume.
The Cairn-side wrapping (consent flow + collection + audit trail +
no-network-by-default composition) lands in Goal 7's implementation
plan, NOT in modflow_tools.

Candidate Cairn-side measures for Goal 7 (the list this section
originally anticipated; superseded by PLANNING.md > Goal 7's
working-list, which is the authoritative version):

* **Bootstrap time**: cold-start single agent to bootstrap Cairn into a target repo.
* **Customization burden**: count of local customizations required.
* **Adoption coverage**: methodology modules adopted vs. skipped, with reasons.
* **First reviewed implementation**: time from Cairn bootstrap to the target repo's first proposal-cycle-completed implementation.
* **Adopter friction reports**: doctrine edits and friction observations after first use.
* **Saugatuck-style pilot metrics** (round-5 / methods.md-arc additions): time-to-first-draft, edit fraction, citation accuracy, drift rate.

**The trust architecture lands FIRST** (per Goal 7's sequencing
precondition): consent-flow doctrine + data-collection audit trail +
no-network-by-default composition + the "what is collected + what is
not" documentation all in place + dogfooded + Cairn-portable BEFORE
the primitive ships.  Each Anchor 10 TRUST dimension must be
demonstrably checked.

*Anchors*: CHAOSS adoption-coverage; AGENT 2026 Framework category; the master guide-star doc's "Trust as design center" section (Anchor 10 + the trust paradox); the 2026-05-14 human-AI-team-development-framework note's "publishable repo-first" framing.

## The Measurement Compact (shipped 2026-05-21 via the v2A proposal; now AGENTS.md doctrine)

**This section's draft text is now the operative compact shipped in `AGENTS.md`.**  Per the accepted `2026-05-21-claude-lifecycle-metrics-layer-v2` proposal (v2A operational-minimum), the five commitments below are repo doctrine, the v2A contract test scans tracked externally-facing artifacts for the violation pattern Tier 1 prohibits (per-agent / per-tier metric tokens), and the two-tier enforcement (Tier 1 Maintainer-Decision-required for externally-published artifacts; Tier 2 normative-only for internal dashboards) is the bite.  The original (2026-05-20) "the v2 proposal should commit to..." framing is superseded -- the v2 proposal DID commit, and the compact landed.

The five doctrine commitments (operative; verbatim from `AGENTS.md > The Measurement Compact`):

* **Metrics are for system learning, not agent punishment.**  Per-agent and per-tier summaries exist to surface routing-policy mistakes and missing review-coverage patterns, not to rank agents.
* **No single score.**  Composite indices that collapse multiple dimensions into one number are not adopted.
* **No interpretation of role-confounded metrics as capability proof.**  Per-tier comparisons require normalization by task assignment; absent normalization, metrics are workload distribution, not capability evidence.
* **No cross-team generality claims from the modflow_tools corpus alone.**  Cross-team claims require Cairn-portability-layer data from N≥2 teams.
* **Internal-diagnostic posture, not external-marketing posture.**  Metrics surface what to investigate; they do not produce evaluations to be shown outside the team without context.

The compact is doctrine, not just norms.  Violations of the compact are findable in External review of the v2 proposal and its eventual implementation -- but those reviews catch *proposal-time* and *implementation-time* violations, not *operational-time* violations (e.g., someone publishing a per-agent ranking externally despite the compact; using per-tier surfaces to make a "model X is better than model Y" claim in chat; generating an external-marketing slide from the operational dashboard).  The v2 proposal must pick one of two enforcement framings for operational-time violations:

* **Maintainer Decision required** before any methodology-related external publication or sharing of compact-governed metrics.  Codifies the compact as a release-style gate, mirroring the existing push-approval discipline for git.  Adds friction but makes the compact bite.
* **Normative-only**: the compact lives in v2's doctrine; review surfaces catch implementation-time violations; operational-time violations rely on maintainer discretion and the compact's own visibility in the doctrine.  Lighter weight; assumes good-faith adherence.

Either is defensible.  Leaving it implicit makes the compact easier to forget in practice, especially as the team scales beyond the maintainer + two AI agents.  Strategy lean: **Maintainer-Decision-required** for any externally-published artifact derived from per-agent or per-tier surfaces; normative-only for internal-only dashboard reading.

## Metric contract -- design discipline

Before each metric ships in v2, define it in a tabular contract.  Match the care the repo already gives to config schema and workflow contracts.

| Field | Purpose |
|---|---|
| **Name** | The metric's name as it appears in reports. |
| **Numerator** | What is being counted / measured. |
| **Denominator** | What it is normalized against (if any). |
| **Data source** | Which file(s) / commit(s) / artifacts produce the data. |
| **Reliability tier** | Exact / Good / Best-effort (mirrors v1's tiering). |
| **Intended interpretation** | What a higher / lower value means. |
| **Explicit non-interpretation** | What it does *not* mean (preempts folk meanings). |

The contract table for v2's full metric set lives in the eventual proposal text and in a generated documentation surface.  Before any metric becomes visible in a snapshot, its row must exist.

## Methodological cautions

Five caveats matter for any analysis built on this v2:

1. **Small N.**  The 2026-05-19 baseline (51 proposals across ~3 months) is enough for descriptive case-study narrative; not enough for statistical inference in the DORA / ITS sense (typical ITS guidance is 12+ observation points per side of an intervention; we run thinner than that, even with subsequent days' accruals).  Right framing for any eventual paper: "one team's measured experience + re-runnable methodology," not "AI agents produce X% more findings (p < 0.05)."

2. **Survivorship bias.**  The proposals/plans corpus is what *got written*.  Work that should have been a proposal but was skipped is invisible.  Today's `d75df00a` revert is a concrete example -- implementation shipped without a proposal; only the maintainer's catch surfaced the gap.  Counter-signal candidates: revert events, proposal-cycle-clarifications doctrine activations, reflection-channel reports of skipped-proposal incidents.

3. **Doctrine-churn coupling.**  Per the Ask 4 caveat above: when multiple doctrine commits land in one session, they are coupled interventions; isolating any single doctrine's effect is structurally limited.  The v2 proposal must engage this (cluster / spread / accept-the-limit).

4. **Measurement-boundary discontinuity at `**Model**:` field introduction.**  The `**Model**:` header field that Layer 2's per-tier comparison depends on was introduced today by the role-based-model-selection doctrine (`cf2f45e`).  Pre-today proposals carry no `**Model**:` annotation and cannot be assigned a tier retroactively without forensic git-archaeology that v2 does not propose.  The retroactive-snapshot backfill (Sequence step 6) will therefore have NULL tier columns for all pre-`cf2f45e` proposals.  This is a *measurement-boundary* discontinuity distinct from the doctrine-effect discontinuities the ITS framing engages with: pre-`cf2f45e` per-tier metrics are not "tier X = 0" but "tier unknown."  V2 reports of per-tier surfaces must either restrict to the post-`cf2f45e` window or carry an explicit "tier-unknown" bucket for the pre-window slice.  This is the cleanest example of how a doctrine landing can also be a *measurement landing*.

5. **Goodhart's Law and AI-specific sensitivity.**  Per the Measurement Compact above: AI agents respond to evaluation criteria more literally than humans; the gameable-metric risk is larger here than in human-team SPACE applications.  Metric design must select for game-resistance (distributions over means; samples over counts; rolling-window aggregates over point-in-time) or accept the gameable-metric cost with complementary anti-gaming measures (sampling, cross-validation, human review).

## Operating vs publishing -- separate the dashboards

Per Codex's review point: the v2 metrics serve two purposes that should not be confused:

* **Operating the team day-to-day**: collision rate, stage latency, stale follow-ups, review yield, snapshot history.  Useful at goodnight, during proposal-review cycles, when triaging deferred follow-ups.  The dashboard's daily audience is the maintainer + active agents.
* **Publishing the methodology**: Cairn adoption, cross-team portability, the outcome ladder, the AI-team-native DORA equivalents.  Useful at paper-writing time / methodology-repo-bootstrap time.  The audience is the external Open Science readership.

V2 ships the *operational* layer with hooks for the *research* artifact.  Paper-oriented analysis lives in Cairn strategy unless it directly improves day-to-day repo operation.

## Adaptive doctrine -- closing the measurement → change loop

The seven anchors above plus the v2's four layers describe *what to measure*.  The Three Ways of DevOps (anchor 8) names what's missing: the closed feedback loop that turns measurements into structural and tool changes.  Metrics that don't drive change are pure observation; metrics that drive change without guardrails are Goodhart amplification.  The interesting design space is between.

This is especially load-bearing for **Cairn as a dynamic and adaptable framework**, not a fixed methodology.  A doctrine repo that doesn't update from its own measurement layer ages out -- the same fate as a metrics dashboard that nobody acts on.

### Today's session as the working example

The d75df00a → revert → proposal-cycle-clarifications-doctrine arc earlier today is the prototype of this loop, just executed informally:

1. **Failure mode surfaces in practice**: I (Implementation) shipped a substantive cross-cutting refactor without a proposal -- `d75df00a` Tier 5.8 visualization split.
2. **Maintainer catches**: chat surface flagged the lifecycle violation about 30 minutes after the commit landed.
3. **Revert**: `f309c17` undoes the implementation; the work is preserved in git history as an inspection artifact.
4. **Strategy authors a proposal**: `2026-05-20-claude-proposal-cycle-clarifications` (5 sharpenings) opens a doctrine change targeting the exact failure mode.
5. **External + Internal review** sharpen the proposal; revisions land.
6. **Maintainer Decision accepts** the doctrine.
7. **Doctrine sharpenings update**: `dev/proposals/_template.md > Triage rule`, `dev/agent_collaboration.md > Review Loop`, `AGENTS.md > Multi-agent collaboration`, `dev/agent_collaboration.md > Internal Reviewer > Post-review`.
8. **Next session sees the new doctrine** and the failure mode is structurally less likely.

That is the Second Way (amplify feedback loop) + Third Way (continual experimentation / learning from failure) in operation.  It happened *informally* -- ad hoc per-incident.  Several other today-arcs follow the same shape: the R2 staged-index collision incident → R2 assessment proposal → collision-log file + doctrine governance.  The work-intent doctrine sharpening (`90cdd76`) → required-bilateral signal+read for shared-comm files.  The NEXT_SESSION drift → rewrite-from-scratch doctrine (`13f60c2`).  Five+ doctrine-change arcs in one session, each one triggered by a measured-or-observed failure mode.

What's missing is the *explicit closure of the loop* -- formal mechanisms that turn the informal pattern into reliable doctrine, with guardrails against over-correction.

### Concrete mechanisms (candidate v2 / v3 surfaces)

Ordered by lightness; pick the lightest that closes the loop you need:

1. **Trigger-condition re-proposals** (already exists for R2; generalize the pattern).  Each substantive doctrine carries an explicit *re-open trigger*: "if metric X crosses threshold Y in window Z, re-open this doctrine."  The R2 collision-log + 14-day rolling-window trigger is the canonical example.  Lightweight, high-information; the maintainer + agents respond to triggers when they fire, not on a cadence.

2. **Reflection-driven doctrine proposals**.  The `dev/reflections/` channel already captures per-agent retrospectives at goodnight.  A structured "today's friction" or "recurring slip" field, migrated at goodnight per the existing doctrine, becomes intake for doctrine-proposal candidates.  Each goodnight produces ≤1 doctrine-proposal stub; the strategy + maintainer triage at the next session.  Pairs with reflections-as-Satisfaction-proxy (the v3 research direction).

3. **Periodic doctrine review** (calendar cadence -- monthly?  quarterly?).  Scheduled doctrine retrospectives where the team asks: "what doctrine has the metrics layer surfaced as ineffective or absent?"  Lighter weight than a trigger; misses things that fire between cycles but catches slow drifts.

4. **A/B doctrine testing** (when N≥2 -- e.g., Cairn adopters or branches).  Run two practices in parallel; compare per the lifecycle-metrics-layer; pick the winner.  Requires meaningful corpus per branch; not feasible at N=1, which is where modflow_tools is today.  Cairn-portability layer creates the conditions for this at adopter-N≥2.

5. **Versioned doctrine** (semver-like).  Doctrine commits carry version stamps.  Adopters pin to a version; upgrades are explicit.  Cross-adopter learning (Cairn) requires version discipline so adopters can attribute their measured outcomes to specific doctrine versions.  Today's modflow_tools doctrine is monotonically growing; no versioning.  Cairn's launch needs versioning from day 1.

6. **Failure-mode → doctrine pipeline** (formalize today's informal arc).  Each true-staged-index collision (collision-log), each verified-flag instance (claim-check), each proposal-cycle violation gets a structured intake → triage → doctrine-proposal pathway.  Codifies the pattern that ran ad hoc today.

7. **Doctrine sunset / deprecation surface**.  Adaptive systems prune too.  Doctrine that hasn't fired in N months may be safe to retire; doctrine that fires constantly may need to be restructured rather than just enforced.  Today's doctrine corpus has no sunset surface -- it's growing without explicit pruning.

### Cairn as adaptive framework

Cairn is the natural home for the explicit adaptive-doctrine machinery, because Cairn is methodology-as-software for general scientific-software teams.  Cairn must be designed *as a dynamic and adaptable framework* from launch, not retrofitted later:

* **Versioned doctrine releases** with semver semantics: major (breaking adopter contracts), minor (additive doctrine), patch (clarifications).  Today's modflow_tools doctrine has no version stamps; Cairn cannot launch the same way.
* **Adopter-feedback intake**: a structured channel for adopters to report friction, doctrine misfires, and doctrine gaps back upstream.  Closes the loop that today modflow_tools doesn't even have (modflow_tools IS the only "adopter" of its own doctrine).
* **Cross-adopter learning loop**: when N≥2 adopters exist, the Cairn-side measurement layer aggregates adopter signal and surfaces patterns that justify doctrine evolution.
* **Methodology-version compatibility matrix**: which Cairn version paired with which lifecycle-metrics version paired with which proposal-template version.  Adopters at older versions know what to upgrade for what benefit.
* **Doctrine-change governance** at Cairn: doctrine commits go through the same proposal cycle as the modflow_tools doctrine they're based on.  Cairn maintainer (initially the modflow_tools maintainer, plausibly delegated later) decides.

The Cairn portability layer (Layer 4 above) measures *whether* the framework transfers.  The adaptive-doctrine layer measures *whether the framework improves over time*.  Both are necessary for the Open Science methodology repository's claim to non-trivial value.

### Risks of an adaptive layer

Three risks deserve explicit framing in any v2 proposal that introduces feedback-driven doctrine changes:

* **Goodhart amplification at scale**.  Already discussed in the Measurement Compact.  When metrics drive doctrine changes automatically (or even semi-automatically), the gameable-metric risk compounds: agents optimize for the metric, doctrine adapts to reward the metric, the metric-and-doctrine pair drifts away from the underlying objective.  Mitigation: keep the loop *human-in-the-loop* at the maintainer's discretion; no automated doctrine commits.

* **Doctrine churn**.  Today landed 5+ doctrine commits in hours -- itself an instance of a measurement-induced loop running too fast.  Adopters of Cairn (today: zero; tomorrow: hopefully N≥1) cannot absorb high doctrine churn rates.  Mitigation: rate-limit doctrine changes; cluster related changes; respect the "marinate overnight" disposition (which the maintainer has used today; doctrine choices benefit from cool-off).

* **Loss of intentionality**.  An adaptive framework that responds too readily to local signals loses the deeper strategic frame that made it useful.  The 2026-05-14 human-AI-team-development-framework strategy note's six-anchor scaffolding is the kind of structural commitment that should *not* adapt away on a metric trend.  Mitigation: separate *operational* doctrine (which can adapt quickly) from *foundational* doctrine (which adapts only via deliberate Strategy-level reconsideration).

### Strategy lean -- a tiered adaptive surface, with rate-limit gates in the core

V2 ships mechanisms 1 (trigger-conditions, already exists for R2) and 6 (failure-mode → doctrine pipeline, formalize today's informal arc).  These are *operational* feedback loops -- they respond to measurable incidents.

V3 / Cairn launch ships mechanisms 2 (reflection-driven proposals) and 5 (versioned doctrine).  These add *structural* feedback discipline that survives the move from N=1 (modflow_tools) to N≥2 (Cairn adopters).

Mechanism 4 (A/B doctrine testing) and mechanism 7 (doctrine sunset) wait for evidence that the lighter mechanisms are insufficient.

**Rate-limit gate -- in the core mechanism, not just in the risks section.**  The mechanisms 1 + 6 v2 ships are exactly what can accelerate doctrine churn if every local slip becomes a doctrine proposal.  The risk needs an enforcement primitive *built into the mechanism*, not deferred to discretion.  Concrete rule for v2: **no doctrine change from a single incident** unless the maintainer explicitly classifies the incident as high-risk (e.g., a security or data-loss surface).  Otherwise, the trigger requires *recurrence* (collision-log threshold; ≥2 incidents of the same shape in a rolling window) *or* goodnight-time synthesis (the goodnight owner aggregates the day's reflection-channel signal into one doctrine-proposal stub, not per-incident).  This keeps the loop adaptive without turning every sharp edge into process; it forces the loop to learn from patterns, not from single events.

Throughout: keep the loop human-in-the-loop at the maintainer's discretion; no automated doctrine commits; the Measurement Compact's "internal-diagnostic posture, not external-marketing posture" extends to "internal-improvement posture, not autopilot posture."

## Open research directions

Items worth recording but not yet committed:

1. **Cross-team comparison via methodology re-use** -- if the lifecycle-metrics-layer + `**Model**:` annotation + collision log pattern is *forkable*, other small teams could run the same instrumentation on their own corpora.  Cross-team data without cross-team data-sharing, since each team owns its own artifacts.  Cairn portability layer makes this measurable.

2. **Reflections as a SPACE Satisfaction proxy** -- the only structurally accessible signal we have for the Satisfaction dimension is the per-agent reflection channel.  But reflections are gitignored and pruned by design; using them as a measurement source is in tension with that choice.  Defer to v3 + a dedicated proposal that explicitly takes a position on the doctrine tension.

3. **AI-team-native DORA equivalents** -- the 2025 DORA report measures AI's effect on *classical* DORA metrics; it does not propose AI-team-native metrics.  Several measures we already have are AI-team-native by accident -- they don't have classical-team analogs: revision rate, finding count per review tier, cross-agent-type review percentage, role-routing escalation rate (from today's role-based-model-selection doctrine), staged-index collision rate per shared-comm file.  Worth surfacing in the Cairn methodology repo's empirical section as "what classical DORA misses about AI-team work."

4. **Re-learning curves at model upgrades** -- the 11-week learning curve found in Copilot studies may have a model-upgrade analog: when models are upgraded (Opus 4.7 → 5; Sonnet 4.6 → 4.7), does the team experience a measurable re-learning period?  Conjectural; would require N >> our current.

## Recommended sequence

1. **Maintainer reads this revised strategy note.**  Decides on v2 scope (the four-layer recommendation above, or a different cut).
2. **Strategy opens a `lifecycle-metrics-layer-v2` proposal** at the agreed scope.  Per today's proposal-cycle clarifications doctrine, chat input is cited as drafting preference, not Decision.
3. **External review by Codex** (different agent type per the role-based-model-selection independence floor).
4. **Response + Decision + plan-open** per normal lifecycle.
5. **Implementation** -- additive to `tools/lifecycle_metrics.py`; new files for snapshots + annotations + the metric contract table; no breaking changes to v1.
6. **Backfill snapshot retroactively** at first run -- generate one snapshot per past goodnight-commit date so the time-series starts before v2 lands, not at v2 launch.  V1 IS read-only and regenerable; running it at past commits gives historical CSVs.

Total span from this strategy note to v2 shipping: probably 1-2 weeks of calendar time once initiated (today's atypical session-density is not the steady-state cadence).  The most valuable use of the time is not the implementation but the design decisions surfaced here -- which is what a strategy note is for.

## References

* **DORA**: Forsgren, Humble, Kim (2018), [dora.dev](https://dora.dev/); 2024 fifth metric (Deployment Rework Rate); [2023 metric rename](https://dora.dev/) (Failed Deployment Recovery Time).
* **SPACE**: Forsgren, Storey, Maddila, Zimmermann, Houck, Butler (2021), [ACM Queue](https://queue.acm.org/detail.cfm?id=3454124).
* **AI-assisted coding productivity**: Peng et al. 2023 ([researchgate](https://www.researchgate.net/publication/368473822_The_Impact_of_AI_on_Developer_Productivity_Evidence_from_GitHub_Copilot)); GitClear 2025 ([gitclear.com](https://www.gitclear.com/ai_assistant_code_quality_2025_research)); Krasniqi & Do 2024 ([arXiv:2408.10758](https://arxiv.org/pdf/2408.10758)).
* **Multi-agent LMA evaluation**: AGENT 2026 workshop / ICSE 2026 ([conf.researchr.org](https://conf.researchr.org/details/icse-2026/agent-2026-papers/13/)); Liu et al. 2024 ([doi:10.1145/3712003](https://dl.acm.org/doi/10.1145/3712003)).
* **CHAOSS**: [chaoss.community](https://chaoss.community/); [CHAOSS metrics repo](https://github.com/chaoss/metrics).
* **Interrupted Time Series**: [Wagner, Soumerai, Zhang, Ross-Degnan (2002)](https://pubmed.ncbi.nlm.nih.gov/12174032/) on segmented regression for ITS; software tools: Stata's `itsa`; the [RITS toolbox](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8265076/).
* **RSE / scientific software**: [Better Scientific Software](https://bssw.io/); FAIR4RS principles; Carver et al. on scientific software development practices.
* **Adjacent project context**: the [2026-05-14 human-AI-team-development-framework strategy note](2026-05-14-claude-human-ai-team-development-framework.md) for the broader six-anchor framework that this metrics note nests inside.

This note is the seed for the subsequent `lifecycle-metrics-layer-v2` proposal.  It is not itself a commitment.

---

## Review -- Claude (External Reviewer-functioning, broad feedback) -- 2026-05-28

<!-- claim-check-allow-count: 513 lines, 51 proposals, 49 accepted, 11-week, 7.7 findings, 4 asks -->

**Model**: Opus 4.7 (1M context).  Frontier-tier.  Invited by the maintainer to provide External-Reviewer-style broad feedback on the 2026-05-28-rewritten state of this strategy doc.

**Structural-independence disclosure (load-bearing)**: I am Claude; the author (also Claude per the header) is the same vendor.  Per `agent_collaboration.md > Stage-to-role matrix`, External review requires a **different agent type or a human** -- same-vendor-different-session is *explicitly insufficient* for the External-tier floor.  This review therefore does **not** meet that floor.  Treat as **decision-support / pre-Codex/Antigravity stress-testing**, not a satisfying External-tier checkpoint.  For a strategy doc, the floor is looser than for a proposal (strategy is design-space exploration, not commitment), and the doc has already had one Codex External round per the header -- so this pass is *third-round same-vendor* primarily catching post-rewrite drift + operationalization gaps.

**Pre-review verifications** (cheap factual checks before drafting):

* `tools/lifecycle_metrics.py` exists -- v2A genuinely shipped. ✓
* `dev/proposals/archive/2026-05-21-claude-lifecycle-metrics-layer-v2.md` is archived -- v2A accepted + archived. ✓
* `~/Code/lhm/dev/` exists with `agent_collaboration.md` + the Cairn-methodology adoption per `~/Code/lhm/AGENTS.md` line 5 -- N=2 deployment claim is real, not aspirational. ✓
* `dev/PLANNING.md` references Goal 7 (lines 1188 / 1235 / 1237) -- the per-project efficacy-data infrastructure goal is captured. ✓
* `tests/integration/test_intent_jsonl_atomic_appends.py` exists locally -- confirms the intent-system precedent the doc cites. ✓

### Steelman

The 2026-05-28 rewrite materially improves the doc: trust-architecture-first framing is the right design center (the Lin TRUST anchor + the trust paradox section together make the case that measurement infrastructure earns its keep only after the trust architecture lands).  The four-layer factoring (Flow / Collaboration / Quality+Outcome / Cairn-portability) cleanly separates evaluation purposes.  The staging discipline (v2A / v2B / v3) explicitly addresses "build it all, learn from none."  The Measurement Compact's five commitments are operationally codified in `AGENTS.md` doctrine with a contract test backing the most obvious violation surface.  Eight framework anchors carry real citations + URLs; the AI-assisted-coding empirics are honest about effect-size variance and learning-curve realities.  Five methodological cautions are explicit and non-defensive.  The working example (today's `d75df00a` → revert → proposal-cycle-clarifications arc) gives the adaptive-doctrine loop a concrete illustration.

### Findings

**A. Currency / drift (the older bottom half lags the 2026-05-28 rewrite):**

1. **The "Recommended sequence" section (lines 491-499) is fully stale.**  It recommends "Strategy opens a `lifecycle-metrics-layer-v2` proposal at the agreed scope" -- but the doc's preamble explicitly says that proposal has shipped (v2A accepted, archived).  Steps 1-6 describe work that already happened.  *Close by*: either delete the section + replace with a one-paragraph "what shipped" recap pointing at the archive, or rewrite as a forward-looking "Recommended next sequence" describing v2B and Cairn-side / Goal 7 work.

2. **The adaptive-doctrine "Strategy lean" section (lines 466-476) frames the rate-limit gate as "to add."**  But the rate-limit gate IS now `AGENTS.md` doctrine (`AGENTS.md > Adaptive-doctrine rate-limit gate`, landed via the v2A arc per the doc's own preamble note about the Measurement Compact + the same arc).  Mechanism 1 (trigger-condition re-proposals) is also operational via the collision-log's R2 14-day rolling-window trigger (and now the handoff-hazard-log's parallel trigger that landed earlier today).  *Close by*: convert "v2 ships mechanisms 1 + 6" / "Rate-limit gate -- in the core mechanism, not just in the risks section" framing to a "what's now operational" recap + a "what's still aspirational" forward look.

3. **Layer 4 supersession leaves a redundant candidate list.**  Lines 325-334 carry the original Layer-4 candidate measures with a note that "PLANNING.md > Goal 7's working-list, which is the authoritative version" supersedes them.  Strategy docs aren't append-only.  *Close by*: delete the redundant list + leave only the pointer to PLANNING > Goal 7, OR keep it explicitly as "historical record of what the doc originally anticipated" framed as such.

4. **Date-anchor drift in narrative voice.**  The doc says "today's session landed 5+ doctrine commits within hours" (Ask 4 caveat) and "Today landed 5+ doctrine commits in hours" (Risks of an adaptive layer) -- where "today" was 2026-05-20.  Reads as present-tense to a 2026-05-28+ reader.  Same with "this team works in bursts" framing.  *Close by*: replace "today" with explicit dates (`2026-05-20`) so the temporal anchors are stable.

**B. TRUST framing strain (the analogy stretches in places):**

5. **The TRUST principles (Lin et al. 2020) → measurement-infrastructure mapping is more metaphorical than literal in places.**  Lin et al. designed TRUST for digital data repositories (preservation infrastructure); the doc maps the five labels onto a research-software-methodology framework.  The labels fit, but the conceptual content shifts.  Most strained: **Sustainability** -- Lin et al.'s "sustainability" is long-term data preservation (the repository can fund and operate over decades); the doc maps it to "measurement infrastructure must not silently lock the adopter into Cairn / data leaves with the adopter."  That's a portability / no-vendor-lock-in claim, not a sustainability-in-the-Lin-sense claim.  *Close by*: either tighten by naming the analogical strain (e.g., "TRUST labels carry analogically; the conceptual content for methodology-framework Sustainability is portability + no-lock-in, which differs from Lin et al.'s data-preservation Sustainability"), OR adopt a different label that fits more literally.  Not a blocker -- the mapping is *useful* as a structural framing -- but honest framing would acknowledge the metaphor.

**C. Operationalization gaps (concepts that need mechanism):**

6. **"Each Anchor 10 TRUST dimension must be demonstrably checked" -- but how, and by whom?**  The doc treats this as the load-bearing precondition for Goal 7's primitive shipping ("dogfooded + Cairn-portable BEFORE the primitive ships"), but doesn't name a verification artifact, attestation surface, or check protocol.  Is it a checklist?  A code-level test?  A doctrine-doc attestation?  A maintainer Decision?  *Close by*: name the verification artifact explicitly, OR explicitly defer to Goal 7's implementation plan with "the verification protocol is decided at Goal 7 plan-open."  Either is fine; leaving it implicit makes the precondition slogan rather than gate.

7. **The Measurement Compact's contract test is a token-pattern scanner.**  The doc honestly acknowledges (under "Operating vs publishing" + adjacent) that "the contract test catches the most obvious violations; broader violation patterns (e.g., per-agent metrics inferred from non-token language) fall outside the test's bite and rely on the doctrine itself."  Fine -- but the doc could be more honest about the gap structure: the Compact's five commitments are mostly enforced by agent discipline + maintainer judgment, with the token scanner covering only the most-mechanical-of-the-most-egregious external violations.  This isn't a defect (mechanical enforcement of all five commitments would be over-engineered), but the doc should name the architecture rather than implying the scanner is broader than it is.  *Close by*: a paragraph explicitly mapping each of the five commitments to its enforcement surface (token-scanner / agent-discipline / Maintainer-Decision / norm-only) so the bite-architecture is transparent.

**D. Missing data / under-exploited surfaces:**

8. **The N=2 deployment claim doesn't surface what LHM specifically demonstrates.**  The doc cites N=2 (modflow_tools + LHM) but doesn't analyze what LHM's adoption process has revealed about Cairn-portability so far -- which is *exactly* the kind of empirical data Goal 7's eventual research artifact would draw on.  Today's adopter-friction-package proposal Decision explicitly noted the willing-volunteer-target is "almost certainly an existing project" -- so LHM (existing scientific codebase, getting Cairn-bootstrapped today) is the canonical first data point.  *Close by*: a paragraph naming what LHM's adoption has demonstrated to date -- bootstrap time, customization burden, doctrine that fit cleanly vs. needed adaptation, friction reports -- even if N=1 on the non-reference-deployment side and the data is qualitative.  This is the load-bearing real-world data the doc otherwise gestures at without surfacing.

9. **Sub-day timing surfaces already exist + the doc doesn't note them.**  Layer 1's "sub-day granularity question" answer is "git log cross-check, no doctrine change" -- but the doc misses that `dev/intents.jsonl` already carries microsecond-precision ISO-8601 timestamps (per the schema doctrine), and `dev/reflections/<date>-<HHMMSS>-*` filenames carry HHMMSS-precision timestamps.  Some per-stage sub-day signal is already available without git-log cross-reference.  *Close by*: a paragraph naming the three existing timing surfaces (intents JSONL / reflection filenames / git log) + their precision + the cross-reference workflow for Layer 1's flow metrics.

10. **Methodological caution #5 (Goodhart + AI-specific sensitivity) is uncited.**  "AI agents respond to evaluation criteria more literally than humans; the gameable-metric risk is larger here than in human-team SPACE applications."  Plausible but empirically thin in the public literature.  *Close by*: cite a specific study (a Goodhart-in-LLM or reward-hacking paper would work) OR weaken to "plausible from first principles; specific empirical magnitude not in public literature" so the claim's status is honest.

### Recommendation

**The 2026-05-28 rewrite's spine (trust-architecture-first + Goal 7 as concrete realization) is strong and lands the doc in a good place as a strategy companion to Goal 7.**  Findings cluster as:

* **A (currency/drift)**: four light edits would close the post-shipping lag in the older bottom half.  Highest ratio of impact-per-effort.
* **B (TRUST framing)**: one paragraph naming the analogical strain on Sustainability.
* **C (operationalization)**: two paragraphs naming the verification artifact (Goal 7 implementation plan?) + the Compact's enforcement-surface architecture.  Most-load-bearing of the four themes.
* **D (under-exploited)**: three small additions surfacing LHM's adoption data, the existing sub-day timing surfaces, and the citation for the Goodhart-AI claim.

None block.  If the maintainer wants a tighter doc, A's currency-drift fixes are the cheapest with the highest readability payoff; C's operationalization gaps are the most consequential if Goal 7 ramps up under capability-pull.

The **structural-independence floor for strategy-doc External review remains insufficient with same-vendor**.  A Codex or Antigravity pass would carry the floor my review structurally cannot -- worth invoking if the doc graduates from "strategy companion to Goal 7" into a public-facing methodology artifact (per the doc's own "Operating vs publishing" framing).
