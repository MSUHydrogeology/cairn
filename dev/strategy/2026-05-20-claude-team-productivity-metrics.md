<!-- Origin: authored 2026-05-20 in modflow_tools' dev/strategy/ (Cairn's
     development home before self-hosting) and migrated 2026-06-12; see
     dev/strategy/MIGRATION.md. Vantage adaptation completed 2026-08-11 --
     this note now speaks from Cairn's own tree and measures Cairn's own
     corpus. modflow_tools appears only where it is genuinely the subject:
     as the named reference deployment. No claim-check exemption remains. -->

# Strategy: team productivity metrics for the human + AI development team

**Author**: Claude (Strategy)
**Date**: 2026-05-20 (substantively revised 2026-05-28; currency pass + External review folded 2026-08-11)
**Status**: living
**Type**: living-reference
**Audience**: maintainer + collaborating AI agents; secondary audience is a scientist (or scientist-team) adopting a structured human + AI development methodology and wanting to know what to measure -- and how the measurement infrastructure itself earns the adopter's trust

## Purpose

**The measurement question is a trust question.**  A human+AI team's data on its own efficacy is the most sensitive material the team produces: it tells the world how the methodology worked, where it failed, who routed what to whom.  Shipping infrastructure that collects that data **requires more adopter trust than not shipping it**.  Trust architecture comes first; the data primitive comes second.  Never the reverse.  See "The trust paradox of empirical-data infrastructure" below + the master guide-star doc's **Anchor 10** (Lin et al. 2020, *The TRUST Principles for digital repositories*, *Scientific Data* 7:144) for the broader framework Cairn's design has been implicitly following.

Cairn ships a lifecycle-metrics layer (`tools/lifecycle_metrics.py`) that turns its own proposal and plan corpora into structured rows -- author, status, finding counts, stage timings, review-yield dispositions, cross-agent-type review rates.  The layer originated in **modflow_tools**, the reference deployment, and folded up to Cairn; it now runs on Cairn's own tree, and the figures in this note are Cairn's unless a sentence says otherwise.

**Cairn's own corpus, measured 2026-08-11** (`python tools/lifecycle_metrics.py proposals` / `plans`): **49 proposals** -- 45 accepted, **4 superseded, 0 rejected** -- carrying **246 findings**, a mean of **7.5 findings** on each of the 33 proposals that drew any, **76% reviewed cross-agent-type**, **63% revised**, and a **median time-to-decision of 0 days** (mean 1.0).  On the plan side: **38 plans**, 36 archived.

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
* **The metrics layer must be forkable, not merely usable where it was built.**  It ships to adopters as a module, so portability is itself a measurement question -- and Cairn is now one of the deployments being measured, not an outside observer of one.

**A third move drives the 2026-05-28 rewrite that follows:**

* **The measurement work IS itself a Cairn portability question -- specifically, the question "how does a Cairn deployment empirically demonstrate trustworthiness?"**  TRUST principles (Anchor 10 of the master guide-star) give the answer; Cairn 0.3 Goal 7 gives the concrete primitive; the trust paradox (below) gives the discipline that prevents over-collection.  Cairn portability is no longer the doc's fourth layer -- it is the doc's spine.

This is a strategy artifact, not a proposal.  Strategy notes (per `AGENTS.md > dev/`) are comparative research and long-horizon design context, not commitments.  Per the original framing, the doc seeded a subsequent `lifecycle-metrics-layer-v2` proposal -- **that proposal has shipped** (accepted; v2A's `tools/lifecycle_metrics.py` + the Measurement Compact -- whose Cairn home is the `lifecycle-metrics` module doc, not `AGENTS.md`; see that section -- and the v2A contract test gating per-agent / per-tier external publication).  This doc's residual job is twofold: **strategy companion to the per-project efficacy-data horizon item** (now 0.5+, not pre-0.4), and **the home of Cairn's measure-forward discipline** (see *Measuring forward*).

## The 2026-05-28 reframe -- what shipped + what changed

The session-of-2026-05-28 layered substantial Cairn-side material on top of this doc.  Catalog of what's new:

1. **Lifecycle-metrics v2A shipped** (accepted; per-agent / per-tier dashboards + Measurement Compact contract test + the unconditional local wording ban that bites per-agent / per-tier tokens in `CHANGELOG.md > Unreleased` and adopter-facing docs).  The Measurement Compact's five commitments are now `AGENTS.md` doctrine, not draft text in a strategy note.
2. **Anchor 10 -- Lin et al. 2020 TRUST principles** added to the master guide-star doc.  Five dimensions of trustworthy infrastructure operation (Transparency, Responsibility, User focus, Sustainability, Technology) generalize cleanly from data repositories to research-software-methodology frameworks like Cairn.  Names the surface this doc was implicitly oriented around.
3. **"Trust as design center" section** added to the master guide-star doc.  Maps the five TRUST dimensions onto Cairn's existing doctrine + names the trust paradox of empirical-data infrastructure (below).
4. **Cairn 0.3 Goal 7** added to `dev/PLANNING.md` -- the concrete per-project efficacy-data infrastructure (pre-0.4 / 0.5) the doc's Layer 4 anticipated.  Frames Cairn's first empirical-research paper as a longitudinal study with consenting deployments.
5. **Cross-links from Goal 1 (self-host) and Goal 4 (doctrine introspection)** -- Goal 1 creates Cairn's own instrumentation surfaces; Goal 4 reads the same signals for read-to-update-doctrine purposes (Goal 7 reads them for read-to-archive-for-research).
6. **Deployment count moved from N=0 to N=3** -- modflow_tools (reference), LHM (legacy retrofit), and Cairn itself, which self-hosted on 2026-06-12 and has since produced the 49-proposal corpus above.  Cairn measuring its own apparatus is the strongest available portability evidence, because it is the case where the methodology and the subject are the same tree.

## Trust as the measurement design center

A human+AI team's data on its own efficacy is **load-bearing trust material**.  Releasing it exposes routing decisions, failure modes, agent-comparison framing, decision velocity -- all of which an adopter has a legitimate stake in controlling.  Any framework that ships measurement infrastructure must clear the trust bar BEFORE the data primitive ships.  Cairn's Anchor 10 names the five TRUST dimensions; mapping them onto measurement specifically:

* **Transparency** -- the measurement schema, the collection logic, and the audit trail of "what was collected when, by whom" are public, append-only, and adopter-inspectable.  Cairn-side: lifecycle-metrics output schema is documented; the v2A contract test scans for compact violations; the consent flow doctrine is public.
* **Responsibility** -- the measurement infrastructure is dogfooded before it ships.  Each metric is exercised on the reference deployment(s) under real conditions; no metric ships untested.  The layer was exercised on the reference deployment before folding up, and now runs against Cairn's own two corpora (proposals + plans) every time this note is re-measured.
* **User focus** -- the adopter chooses what to collect, when to collect, what to share.  No metric is mandatory; default mode is **collection-only-where-consented** with the lifecycle-metrics module's per-deployment opt-in.  Cairn-side: the on-ramp's graduated levels mean an L1 (hand-copy-kernel) adopter doesn't get the same measurement surface as an L2 (full bootstrap) one.
* **Sustainability** -- measurement infrastructure must not silently lock the adopter into Cairn.  Data leaves with the adopter when they exit; collection produces a portable artifact (the on-disk metric tables); no central server, no Cairn-side persisted state.  *(Naming the analogical strain honestly: Lin et al.'s Sustainability is long-term **preservation** -- can the repository fund and operate for decades. What is claimed here is **portability and no-lock-in**, which is a different property wearing the same label. The five TRUST labels carry over as a useful structural frame; their conceptual content shifts when moved from a data repository to a methodology framework, and this dimension shifts most.)*
* **Technology** -- no-network-by-default composition; the export-safety scrub on any outbound artifact; the `content-security` module protects against accidental exfiltration; verify-integrity gates protect against silently-corrupted data.

**Reference**: the master guide-star doc's "Trust as design center" section names the same five dimensions and provides the analog mapping for Cairn's other apparatus.  This section narrows the lens to the measurement infrastructure specifically.

## The trust paradox of empirical-data infrastructure

**Adding a primitive that collects efficacy data requires more adopter trust than not adding it** -- even when the data stays local.  Three trust dimensions tighten when measurement infrastructure ships:

1. **Surveillance vector**: an adopter has to trust that the collection itself doesn't introduce a surveillance pathway.  A metric that captures "time-to-decision per agent" is an audit trail of who decided what when -- benign at Cairn's current scale (one maintainer, a small agent roster), sensitive at larger team scales where member-comparison framing carries political weight.
2. **Outreach surface**: the maintainer's future ability to contact participants for a research paper means the data persists with the intent of future research use.  Even if outreach is out-of-band + per-occurrence opt-in, the data's existence presupposes the outreach pathway.
3. **Evaluation drift**: the Measurement Compact's first commitment ("metrics are for system learning, not agent punishment") is **a doctrine commitment**, not a technical guarantee.  As the framework spreads to communities the maintainer cannot personally vouch for, an adopter must trust either (a) every future framework maintainer's good faith, or (b) the framework's structural impossibility of misuse.

**The paradox dissolves when the trust architecture lands before the data primitive itself.**  This is the load-bearing sequencing claim of Cairn 0.3 Goal 7 (below): consent-flow doctrine + data-collection audit trail + no-network-by-default composition + "what is collected + what is not" documentation must all be in place + dogfooded + Cairn-portable BEFORE the primitive ships.  Each Anchor 10 TRUST dimension must be demonstrably checked.

The Measurement Compact (above; now `AGENTS.md` doctrine) closes most of the paradox at the framework-level.  The remaining gap is the per-adopter-deployment surface: every Cairn deployment must be able to verify the trust architecture on its own tree, not just trust that Cairn's framework-level commitments hold.  That verification surface is what Goal 7's pre-shipping work creates.

## Per-project efficacy-data infrastructure -- the realization of Layer 4

**Roadmap home re-checked 2026-08-11.** This work was once tracked as "Cairn
0.3 Goal 7." That numbering no longer exists: `dev/PLANNING.md` now carries it
as a horizon line -- *"0.5+ -- per-project efficacy-data infrastructure and
beyond."* Cite it by description, not by a goal number, and read every "Goal 7"
below as naming that horizon item. **It has also moved further out** (0.5+
rather than pre-0.4/0.5), which changes its sequencing relative to everything
else here: the trust-architecture work it is gated on is no longer near-term.

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

**Goal 7's verification gate**: each Anchor 10 TRUST dimension must be demonstrably checked on the data primitive before adopters are asked to commit to running it (per the trust paradox section above).  Cairn dogfoods it on its own tree first; the reference and legacy deployments are the second and third exercises; only then does the primitive ship as a default-on module.

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

7. **Research Software Engineering (RSE) / scientific-software practice** -- Cairn's adopters build scientific software, not general-purpose SaaS, and Cairn is itself research-software methodology rather than a product.  RSE-community guidance bears directly on what to measure:
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

## Current state -- what the layer measures *(re-measured 2026-08-11)*

`tools/lifecycle_metrics.py` is no longer a single-file extractor: it is a
69-line facade over a nine-module `_lifecycle_metrics/` package (`extract`,
`parse`, `snapshot`, `subsystems`, `gitmeta`, `config`, `report`, `cli`).
**Substantially more of the recommended scope below has shipped than the
recommendation text implies** -- read the layer sections as a mix of *landed*
and *outstanding*, not as a forward plan.

**Per-proposal: 30 columns**, verified by running the tool. Beyond the
original sixteen, the live schema now carries:

* **Per-stage timestamps and deltas** -- `reviewed_date`, `revised_date`,
  `days_open_to_reviewed`, `days_reviewed_to_revised`,
  `days_revised_to_decision`, plus **hour-resolution** counterparts
  (`hours_*`) and a `stage_timestamp_reliability` tier. This is Layer 1's
  stage-granularity ask, delivered -- including the sub-day resolution the
  original text treated as an open question.
* **Review-yield dispositions** -- `review_yield_accept_count`,
  `review_yield_accept_with_modification_count`, `review_yield_reject_count`,
  `review_yield_defer_count`. This is Layer 2's disposition grammar, which the
  original text called "a slogan, not a signal" without the template
  amendment. The amendment happened; the signal exists.
* **`response_models`** -- the `**Model**:` extraction Layer 2 required for
  honest per-tier comparison.
* **`proposal_annotation_count`** -- the doctrine-intervention annotation hook.

One column named in the original sixteen, `human_review`, is **not** in the
live schema; `external_tier_review` remains. Treat any analysis written
against the old column list as needing a re-check.

**A live reliability question on the plan side.** Of 38 plans, `code_review_rounds`
reports **0 for 28 of them**, while 36 are archived -- and Cairn's plan-archive
precondition holds that a plan cannot archive until a code review has occurred.
Every archived plan does carry a heading matching *code review*. So either the
extractor counts rounds by a marker convention most plans predate, or the
precondition is satisfied in a form the metric cannot see. This is checkable and
unresolved; until it is resolved, `code_review_rounds` should not be read as
evidence about review coverage. It is exactly the failure mode the metric
contract's *reliability tier* field exists to record.

**Per-plan: still 6 columns** -- `stem`, `status`, `plan_review_rounds`,
`code_review_rounds`, `paired_proposal`, `paired_proposal_reliability`.

**That asymmetry is the single most important fact in this section.** The
proposal side has rich per-finding data; the plan side has **round counts
only** -- no code-review finding counts, and no file attribution. So the layer
can say a great deal about how *proposals* are deliberated and almost nothing
about what *implementing* a given code surface costs. Any study of the form
"does this part of the codebase cost more review effort" runs straight into
that gap (see *Measuring forward* below).

**Snapshots and events have shipped too.** The CLI carries `--snapshot`,
`--event {plan-archive,goodnight,doctrine-intervention,manual,backfill}`,
`--backfill-from`, `--manifest`, and `--format {csv,md}` -- the
event-triggered cadence Layer 1 specified, with the conservative trigger set
it recommended.

**But the time series is not in the record.** `dev/measurement/snapshots/`
holds real snapshots (2026-07-31, 2026-08-04, 2026-08-05) and is **untracked
-- not gitignored, simply uncommitted**; `dev/measurement/collision_log.md` is
in the same state. `dev/intents.jsonl` *is* deliberately gitignored
(`.gitignore:12`), so the contrast is not a blanket policy. Layer 1 asked
explicitly whether snapshots should be tracked artifacts or live outside the
hot working tree; that question was never answered, and the current state is
the worst of both -- a time series that exists on one machine and is absent
from the durable record. **This is the highest-value cheap fix in the note:
decide, and either commit them or gitignore them deliberately.**

The 2026-05-19 baseline run (historical snapshot, not live count):

* 51 proposals (49 accepted / 0 rejected / 0 superseded)
* 50 of 51 reached a Revised-proposal stage
* Mean 7.7 findings per reviewed proposal
* 80% reviewed cross-agent-type
* Median `days_to_decision` = 0 days

**Gating-function caveat (2026-07-22 addendum).** Three things worth
stating plainly where these numbers are presented, not just implied:

1. The headline figures are now **Cairn's own corpus** (measured 2026-08-11),
   not an inherited reference-deployment baseline.
2. The numbers are strong evidence for review's **improvement**
   function (mean 7.7 findings per reviewed proposal) — they are **not**
   evidence for its **gating** function. A ~96% same-day acceptance
   rate (0 rejected / 0 superseded, median 0 days to decision) reads,
   on its own, like an accept-ceremony. One candidate honest
   explanation: bad ideas die during chat-stage shaping, before a
   proposal is ever written. `doctrine/lifecycle.md:285-296`
   establishes that a pre-proposal shaping stage exists (chat
   preferences are input folded into a draft, not a Decision) — it
   does **not** itself claim that losing ideas are filtered out there,
   so treat this as an unverified candidate explanation, not a
   doctrine-backed fact.
3. **Material update since the baseline:** Cairn's own tree has since
   produced its first **superseded** proposal
   (`2026-07-08-claude-automated-review-committer`, superseded
   2026-07-09). Review's blocking Internal finding led the author to
   *supersede* the proposal in favor of an existing-doctrine practice
   plus a recurrence-gated follow-up — the adversarial read materially
   blocked the change **as written**, and the author reshaped it. This
   is not a rejection: the hard-rejection count stays **0**, and
   supersession is a distinct, non-rejection gating signal — the first
   recorded instance of the adversarial read actually biting, not just
   improving.

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

**Critical methodological caveat -- doctrine-churn coupling**: the 2026-05-20 session landed 5+ doctrine commits within hours (`90cdd76` work-intent required-signal+read; `13f60c2` NEXT_SESSION rewrite-from-scratch; `2ef4864` PLANNING completed-sweep; `cf2f45e` + `3ac3f3b` role-based-model-selection; `5dfeecd` proposal-cycle-clarifications).  For ITS analysis these are **coupled interventions**, not independent point-events.  You cannot attribute any subsequent metric shift to any single doctrine without controlling for the others.  Three responses available -- the v2 proposal must pick:

* **Cluster the interventions**.  Treat clusters of doctrine commits within one session as a single intervention.  Loses resolution; preserves causal inference.
* **Spread the interventions deliberately**.  Doctrine-work pacing as a process discipline -- one doctrine change per calendar day, not five per session.  Aligns with small-N reality; makes ITS tractable.
* **Accept the limit**.  Report findings as *directional*, not causal.  Match the small-N framing already in this note.

## Beyond the four asks -- the science/product outcome layer

The four asks above cover *coordination mechanics* -- how the team's lifecycle machinery moves work through proposal -> review -> decision -> implementation.  The maintainer's larger goal is not measured by these alone: world-class MODFLOW workflows, faster scientific modeling, reproducible notebooks/configs, a Cairn methodology reusable across scientific codebases.

Lifecycle metrics are necessary instrumentation but not the product.  Without an outcome layer, the dashboard could report that the team reviews faster and collides less while missing whether the software itself is becoming more capable, more reliable, and more useful to scientists -- the exact activity-vs-productivity failure mode SPACE warns about.

**Outcome-layer candidate measures**:

* **Capability coverage**: shipped user-facing workflows by tier (build, review, calibration, delivery, particle tracking, visualization, teaching).  Each workflow has: runnable example, smoke test, docs, user-guide entry.
* **Runnable-artifact health**: notebooks that execute cleanly top-to-bottom; CLI examples that run as documented; configs that load without warnings.
* **Reproducibility-artifact production**: configs, delivery packages, benchmark baselines, generated schema docs, snapshot files.
* **Post-ship defect / rework rate**: per capability surface, follow-up amendments / sharpening commits / revert events within rolling windows.  Maps to DORA's *Deployment Rework Rate* (the 2024 fifth metric).
* **Time-from-proposal-to-working-workflow**: not just `days_to_decision`, but `days_to_documented_runnable_user_facing_workflow`.  A proposal accepted is not a workflow delivered.
* **Maintainer-reported friction reduction**: qualitative signal -- specifically, time saved or friction removed on real hydrogeology tasks the maintainer has been doing.  N=1 today; structurally available; matters more than most quantitative metrics for "is this serving the science."

The outcome layer joins coordination metrics as a *peer*, not a subordinate.  In v2's report shape: a coordination-metric improvement that doesn't move outcomes is a problem to investigate, not a win.

## Cairn portability -- the methodology's transfer test

Cairn is the home for *exportable* measurement methodology, and -- since self-hosting on 2026-06-12 -- one of the deployments being measured.  **Three measured deployments today**: Cairn itself (the 49-proposal corpus above), modflow_tools (the reference instance the layer came from), and LHM (a legacy retrofit).  A genuinely third-party deployment, by a team that did not contribute to the doctrine, remains the open portability test; none of the three is independent of the maintainer.

Cairn portability is the doc's spine, not its fourth layer.  The concrete plan for measuring it is **Cairn 0.3 Goal 7** (above) -- the per-project efficacy-data infrastructure ships pre-0.4 / 0.5, before community adopters arrive.  Anchor 10's TRUST dimensions gate the primitive: each must be demonstrably checked before adopters are asked to commit to running it.

**Portability candidate measures** -- each is a per-adopter measurement event, and Cairn's own adoption of its apparatus is the first datum rather than an exception to the series:

* **Bootstrap time**: how long does it take a cold-start single agent to bootstrap Cairn into a target repo with its assessment / proposal / plan / review-loop / goodnight surfaces?
* **Customization burden**: number of local customizations required to make Cairn fit the target repo.
* **Adoption coverage**: of Cairn's methodology modules, how many were adopted vs. skipped?  Which were skipped and why?
* **Friction reports**: doctrine edits and adopter friction observations after first use.  (The adopter-friction package, accepted 2026-05-28, ships static entry-surface artifacts that ARE the first attack on this metric.)
* **Time-to-first-reviewed-implementation**: from Cairn bootstrap to the first proposal-cycle-completed implementation in the target repo.
* **Saugatuck-style pilot metrics** (the methods.md generation arc's gate): time-to-first-draft, edit fraction, citation accuracy, drift rate.  See Tier 5.5 (Saugatuck first-pilot dogfood) for the per-metric provenance.

For each measurement choice, a **forkability test**: would another scientific-software team be able to run this measurement on their own corpus, against their own agents, with their own doctrine commits?  Tag each metric: *generic* (reusable across teams) or *deployment-specific* (configuration or customization needed before it transfers).  `lifecycle_metrics.py` ships the forkable contract surface; the efficacy-data horizon item ships the consent + collection wrapper around it.

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
* **Still open.**  Layer 4 (portability), versioned doctrine (mechanism 5), reflection-derived satisfaction proxies, A/B doctrine testing (mechanism 4), and the doctrine sunset surface (mechanism 7).  The forkable metric *contracts* exist; the consent-and-collection wrapper around them does not.

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
"design-only at the reference deployment; instrumentation later"
framing is now stale: Goal 7 is the concrete pre-0.4 / 0.5 plan that
ships the Cairn-side primitive.

The reference deployment's contribution to that primitive: the forkable
metric *contract* surface (`tools/lifecycle_metrics.py` shipped its
outputs in the Metric Contract table format) is in place, and the
generic-exporter hook is ready for the Goal 7 primitive to consume.
The Cairn-side wrapping (consent flow + collection + audit trail +
no-network-by-default composition) lands in Goal 7's implementation
plan, not in the deployment the layer came from.

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

## The Measurement Compact (operative; home re-checked 2026-08-11)

The compact landed. **Its home in Cairn is not `AGENTS.md`** -- that was true
of the reference deployment this note was written in, and carrying the claim
forward would send a reader to the wrong file. In Cairn the five commitments
live in `templates/modules/default-on/lifecycle-metrics.md`, the module doc
shipped to every adopter that selects the metrics layer, and the
adaptive-doctrine **rate-limit gate** is separately operative in Cairn's own
`AGENTS.md` citing `doctrine/rationale.md`.

That placement difference is not pedantry: it means the compact governs
adopters **only if they install the module**, whereas an `AGENTS.md` rule
would bind every adopter unconditionally. Whether that is the right scope is a
real question and is left open here rather than assumed.

The five commitments (operative):

1. **Metrics serve system learning, not member punishment.**  Per-member and per-tier surfaces exist to find where the *collaboration apparatus* drifts, not to rank contributors.
2. **No single composite score.**  A composite hides the diagnostic value of per-dimension signals and invites ranking-style reading.
3. **No role- or tier-confounded metric is read as capability proof.**  Per-tier and per-role surfaces are confounded by task assignment and escalation rules.
4. **No cross-team generality from a single corpus.**  One team is N=1 in the methodology-export sense; a cross-team claim needs independent teams, not a deeper read of one.
5. **Internal-diagnostic posture, not external-marketing posture.**  Any externally-published artifact derived from them is a separate, gated act.

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

5. **Goodhart's Law and AI-specific sensitivity.**  Per the Measurement Compact above: the gameable-metric risk plausibly runs larger with AI agents than in human-team SPACE applications, because agents optimize against a stated criterion more literally.  **Evidence status, stated rather than implied: this is reasoning from first principles and from the reward-hacking literature's general shape -- no measurement of the specific magnitude in a human+AI development team exists in the public literature, and none is offered here.**  Treat it as a design posture, not a finding.  Metric design should still select for game-resistance (distributions over means; samples over counts; rolling-window aggregates over point-in-time) or accept the cost with complementary measures (sampling, cross-validation, human review) -- the posture is cheap and the downside of being wrong about it is small.

## Operating vs publishing -- separate the dashboards

Per Codex's review point: the v2 metrics serve two purposes that should not be confused:

* **Operating the team day-to-day**: collision rate, stage latency, stale follow-ups, review yield, snapshot history.  Useful at goodnight, during proposal-review cycles, when triaging deferred follow-ups.  The dashboard's daily audience is the maintainer + active agents.
* **Publishing the methodology**: Cairn adoption, cross-team portability, the outcome ladder, the AI-team-native DORA equivalents.  Useful at paper-writing time / methodology-repo-bootstrap time.  The audience is the external Open Science readership.

V2 ships the *operational* layer with hooks for the *research* artifact.  Paper-oriented analysis lives in Cairn strategy unless it directly improves day-to-day repo operation.

## Adaptive doctrine -- closing the measurement → change loop

The seven anchors above plus the v2's four layers describe *what to measure*.  The Three Ways of DevOps (anchor 8) names what's missing: the closed feedback loop that turns measurements into structural and tool changes.  Metrics that don't drive change are pure observation; metrics that drive change without guardrails are Goodhart amplification.  The interesting design space is between.

This is especially load-bearing for **Cairn as a dynamic and adaptable framework**, not a fixed methodology.  A doctrine repo that doesn't update from its own measurement layer ages out -- the same fate as a metrics dashboard that nobody acts on.

### Today's session as the working example

The d75df00a → revert → proposal-cycle-clarifications-doctrine arc of 2026-05-20 is the prototype of this loop, just executed informally:

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

4. **A/B doctrine testing** (when N≥2 -- e.g., Cairn adopters or branches).  Run two practices in parallel; compare per the lifecycle-metrics-layer; pick the winner.  Requires a meaningful corpus per branch.  Cairn's own 49 proposals are a single stream, not two arms, so this stays infeasible here; the portability layer creates the conditions once independent adopters exist.

5. **Versioned doctrine** (semver-like).  Doctrine commits carry version stamps.  Adopters pin to a version; upgrades are explicit.  Cross-adopter learning (Cairn) requires version discipline so adopters can attribute their measured outcomes to specific doctrine versions.  Cairn's own doctrine grows monotonically with no version stamps on individual rules -- releases are versioned, doctrine changes within them are not.  A cross-adopter learning loop needs the finer grain.

6. **Failure-mode → doctrine pipeline** (formalize today's informal arc).  Each true-staged-index collision (collision-log), each verified-flag instance (claim-check), each proposal-cycle violation gets a structured intake → triage → doctrine-proposal pathway.  Codifies the pattern that ran ad hoc today.

7. **Doctrine sunset / deprecation surface**.  Adaptive systems prune too.  Doctrine that hasn't fired in N months may be safe to retire; doctrine that fires constantly may need to be restructured rather than just enforced.  Today's doctrine corpus has no sunset surface -- it's growing without explicit pruning.

### Cairn as adaptive framework

Cairn is the natural home for the explicit adaptive-doctrine machinery, because Cairn is methodology-as-software for general scientific-software teams.  Cairn must be designed *as a dynamic and adaptable framework* from launch, not retrofitted later:

* **Versioned doctrine releases** with semver semantics: major (breaking adopter contracts), minor (additive doctrine), patch (clarifications).  Cairn's own doctrine rules carry no individual version stamps -- releases are versioned, the rules inside them are not -- and a cross-adopter learning loop needs the finer grain.
* **Adopter-feedback intake**: a structured channel for adopters to report friction, doctrine misfires, and doctrine gaps back upstream.  Cairn has the fold-back ledger as the mechanism; what it does not yet have is an adopter population independent of the maintainer to feed it.
* **Cross-adopter learning loop**: when N≥2 adopters exist, the Cairn-side measurement layer aggregates adopter signal and surfaces patterns that justify doctrine evolution.
* **Methodology-version compatibility matrix**: which Cairn version paired with which lifecycle-metrics version paired with which proposal-template version.  Adopters at older versions know what to upgrade for what benefit.
* **Doctrine-change governance**: doctrine commits go through the same proposal cycle as everything else, and clear the adaptive-doctrine rate-limit gate.  The Human Maintainer decides, plausibly delegated as the contributor pool grows.

The Cairn portability layer (Layer 4 above) measures *whether* the framework transfers.  The adaptive-doctrine layer measures *whether the framework improves over time*.  Both are necessary for the Open Science methodology repository's claim to non-trivial value.

### Risks of an adaptive layer

Three risks deserve explicit framing in any v2 proposal that introduces feedback-driven doctrine changes:

* **Goodhart amplification at scale**.  Already discussed in the Measurement Compact.  When metrics drive doctrine changes automatically (or even semi-automatically), the gameable-metric risk compounds: agents optimize for the metric, doctrine adapts to reward the metric, the metric-and-doctrine pair drifts away from the underlying objective.  Mitigation: keep the loop *human-in-the-loop* at the maintainer's discretion; no automated doctrine commits.

* **Doctrine churn**.  2026-05-20 landed 5+ doctrine commits in hours -- itself an instance of a measurement-induced loop running too fast.  Adopters of Cairn (zero at the time of writing; N≥2 today) cannot absorb high doctrine churn rates.  Mitigation: rate-limit doctrine changes; cluster related changes; respect the "marinate overnight" disposition (which the maintainer used that day; doctrine choices benefit from cool-off).

* **Loss of intentionality**.  An adaptive framework that responds too readily to local signals loses the deeper strategic frame that made it useful.  The 2026-05-14 human-AI-team-development-framework strategy note's six-anchor scaffolding is the kind of structural commitment that should *not* adapt away on a metric trend.  Mitigation: separate *operational* doctrine (which can adapt quickly) from *foundational* doctrine (which adapts only via deliberate Strategy-level reconsideration).

### Strategy lean -- a tiered adaptive surface, with rate-limit gates in the core

V2 ships mechanisms 1 (trigger-conditions, already exists for R2) and 6 (failure-mode → doctrine pipeline, formalize today's informal arc).  These are *operational* feedback loops -- they respond to measurable incidents.

V3 / Cairn launch ships mechanisms 2 (reflection-driven proposals) and 5 (versioned doctrine).  These add *structural* feedback discipline that survives the move from a maintainer-adjacent deployment set to genuinely independent adopters.

Mechanism 4 (A/B doctrine testing) and mechanism 7 (doctrine sunset) wait for evidence that the lighter mechanisms are insufficient.

**Rate-limit gate -- in the core mechanism, not just in the risks section.**  The mechanisms 1 + 6 v2 ships are exactly what can accelerate doctrine churn if every local slip becomes a doctrine proposal.  The risk needs an enforcement primitive *built into the mechanism*, not deferred to discretion.  Concrete rule for v2: **no doctrine change from a single incident** unless the maintainer explicitly classifies the incident as high-risk (e.g., a security or data-loss surface).  Otherwise, the trigger requires *recurrence* (collision-log threshold; ≥2 incidents of the same shape in a rolling window) *or* goodnight-time synthesis (the goodnight owner aggregates the day's reflection-channel signal into one doctrine-proposal stub, not per-incident).  This keeps the loop adaptive without turning every sharp edge into process; it forces the loop to learn from patterns, not from single events.

Throughout: keep the loop human-in-the-loop at the maintainer's discretion; no automated doctrine commits; the Measurement Compact's "internal-diagnostic posture, not external-marketing posture" extends to "internal-improvement posture, not autopilot posture."

## Open research directions

Items worth recording but not yet committed:

1. **Cross-team comparison via methodology re-use** -- if the lifecycle-metrics-layer + `**Model**:` annotation + collision log pattern is *forkable*, other small teams could run the same instrumentation on their own corpora.  Cross-team data without cross-team data-sharing, since each team owns its own artifacts.  Cairn portability layer makes this measurable.

2. **Reflections as a SPACE Satisfaction proxy** -- the only structurally accessible signal we have for the Satisfaction dimension is the per-agent reflection channel.  But reflections are gitignored and pruned by design; using them as a measurement source is in tension with that choice.  Defer to v3 + a dedicated proposal that explicitly takes a position on the doctrine tension.

3. **AI-team-native DORA equivalents** -- the 2025 DORA report measures AI's effect on *classical* DORA metrics; it does not propose AI-team-native metrics.  Several measures we already have are AI-team-native by accident -- they don't have classical-team analogs: revision rate, finding count per review tier, cross-agent-type review percentage, role-routing escalation rate (from today's role-based-model-selection doctrine), staged-index collision rate per shared-comm file.  Worth surfacing in the Cairn methodology repo's empirical section as "what classical DORA misses about AI-team work."

4. **Re-learning curves at model upgrades** -- the 11-week learning curve found in Copilot studies may have a model-upgrade analog: when models are upgraded (Opus 4.7 → 5; Sonnet 4.6 → 4.7), does the team experience a measurable re-learning period?  Conjectural; would require N >> our current.

## Measuring forward -- the discipline this layer still owes

The v2 sequence this section once carried is spent: the proposal shipped, the
layer was built, and the schema above is what it produces. What remains is not
another build. It is a discipline question that surfaced from an unrelated
attempt to *use* the layer as evidence, and it belongs here because it
constrains every future measurement Cairn adds.

**The attempt.** A 2026-08 complexity study needed to answer "does a
higher-complexity code surface cost more review effort?" and reached for this
layer. It could not get there, for two reasons already visible above: the
per-plan schema carries **round counts, not code-review findings**, and it
carries **no file attribution**; and the per-proposal finding counts describe
deliberation *before* implementation, so attributing them to files a later
plan touched would not measure what the question asks.

**The temptation, and the rule.** The obvious repair is to reconstruct the
missing attribution from the archive -- read closed plans and decide which
file each historical finding concerned. **That is prohibited, and the reason
is methodological rather than procedural.** A plan is append-only once
implementation starts and closed once archived; the plan-archive precondition
(a plan cannot archive until a code review occurred) is what makes an archived
plan usable as evidence at all. Deciding *now, with a hypothesis in hand*
which file a past finding blamed is fitting evidence to a conclusion, done by
the party who wants a particular answer. **The archive's entire evidentiary
value is that it was written before anyone asked the question.**

Measured coverage, so the sparsity is a stated limit rather than a repair
target: of 34 archived plans, 20 touch a substantial code artifact, 13 carry
tagged code-review findings, and 32 of 57 such findings (56%) name a file.

**So: instrument the next cycle instead of litigating the last one.** The
generalizable rule, and the one this note should carry as measurement
doctrine:

> **If you want a question answerable later, add the field that answers it
> before you need it, where the person who knows the answer is already
> writing.** When an existing record is too sparse to test a hypothesis, the
> legitimate moves are to report the sparsity and to instrument forward --
> never to annotate the old record.

Three design constraints follow, and they are what keep forward instrumentation
from becoming ceremony:

* **Lightweight -- a field, not a workflow.** Reviewers already name a file in
  prose 56% of the time. Structuring that extends the plan template's existing
  finding-disposition vocabulary rather than adding a mechanism.
* **Transparent by construction.** The data lives where the finding lives --
  in the committed plan, human-readable, reviewable by the person it concerns.
  No separate database, no side channel, no telemetry, nothing collected that
  was not already being written down. This is the compact's posture made
  concrete rather than asserted.
* **Analysis registered before the data exists.** Outcome, covariates,
  retention of zero-finding cases, and an explicit **INCONCLUSIVE** branch
  declared up front -- which is *easier* prospectively than retrospectively,
  because no results exist yet to fit to. Cairn's proposal template is already
  registered-report-shaped; this inherits that discipline rather than inventing
  it (cf. Chambers 2013, *Registered Reports*, Cortex 49(3):609-610).

**The honest cost:** forward instrumentation answers in months, not weeks, and
whatever prompted the question stays unvalidated meanwhile. That is the price
of not manufacturing the evidence, and it is the right price.

**One compact application worth deciding before collection starts.** A
file-attributed finding links *a file* to *a problem* to *whoever found it* --
finer-grained than anything this layer currently keeps. Under the first
commitment ("system learning, not agent punishment") the answer is to say so
explicitly in advance and to keep per-reviewer aggregation out of the declared
analysis entirely. Retrofitting that constraint after the data exists is the
harder direction.

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
