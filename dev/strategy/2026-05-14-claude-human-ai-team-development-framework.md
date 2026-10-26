# Cairn — the guide star

**Author**: Claude (Strategy), Antigravity (Strategy)
**Date**: 2026-05-14 (rewritten 2026-10-26 around current state)
**Status**: living
**Type**: living-reference
**Audience**: Maintainer and collaborating AI agents; secondary audience is a scientist evaluating or adopting Cairn

## What Cairn is, and what its evidence supports

**Cairn is an Open Science methodology repository for scientists and research-software teams working with AI coding agents.** Its promise is simple: **delegate the coding without losing control of the scientific assumptions, the evidence, and the decisions.**

Four practices carry that promise today:

1. **A git-committed deliberation record.** Proposals, plans, reviews, and decisions live as plain Markdown files in `dev/`. Any model family or human collaborator can read and write the record without a server, a shared session memory, or vendor lock-in.
2. **One review stance at every stage.** Every proposal, plan, and implementation is read by a fresh reviewer who did not write the work. The reviewer is on the work's side and makes it better by questioning its foundations in writing — answering whether it should happen as framed, what the strongest alternative is, and what would show it wrong (`AGENTS.md`, [`doctrine/dual-review.md`](../../doctrine/dual-review.md)). When the Maintainer wants review from a different model family or a human on a specific artifact, the Maintainer commissions an **External read** (`**Called by**: Maintainer ...`). No agent selects or recommends a review tier on its own.
3. **The comprehension floor and Cairn Plain Language 1.0.** A Maintainer cannot legitimately decide on a change they cannot follow; opaque prose turns "review and decide" into a rubber stamp. Cairn enforces a 17-rule writing and reasoning standard ([`dev/agent_collaboration.md`](../agent_collaboration.md), [`docs/plain-language.md`](../../docs/plain-language.md)), treats *"I don't understand this yet"* as a mandatory pause, and requires durable code, tests, and comments to stand on their own without dead pointers into archived deliberation ([`doctrine/rationale.md`](../../doctrine/rationale.md)).
4. **Restraint and proportional verification.** Work is triaged by blast radius: trivial changes and bounded defect repairs land in a single commit with scoped test evidence in the commit body, while non-trivial changes take the proposal and plan lifecycle. Standard review is one round. The full test suite runs only at certifying integration points (before push, release, or re-anchor), never per chunk or per review pass. Security controls stay fail-closed on real trust boundaries, while bookkeeping ceremony is cut.

### Evidence status

* **Measured:** Cairn governs its own repository and two documented case studies under one Maintainer — `modflow_tools` (built AI-team-first; [`case-studies/modflow_tools.md`](../../case-studies/modflow_tools.md)) and `LHM` (a legacy MATLAB and Python landscape-hydrology model retrofitted with Cairn; [`case-studies/lhm.md`](../../case-studies/lhm.md)).
* **Assumed from literature:** Each mechanism rests on published research in software engineering, cognitive science, and scientific peer review (the 22 anchors below). Literature grounding explains why a mechanism is plausible; it does not prove that the bundle pays for its overhead.
* **Unmeasured (what would falsify or confirm it):** Deployments under a single Maintainer show use, not comparative efficacy. The serious alternative is not careless prompting; it is a scientist using a current coding agent, ordinary Git and tests, a short instruction file, and brief notes for major decisions. Cairn earns its keep only if its science-specific assurance and decision record beat that lighter baseline. Settling that question requires an outside adoption on real scientific changes alongside comparable work under the lighter baseline, with the threshold declared beforehand: recording total scientist attention, checking scientific outcomes against a basis independent of the code, and testing whether another person can later reproduce the result and state its assumptions.

---

## What Cairn ships today

Cairn is a citable, DOI-bearing repository ([`CITATION.cff`](../../CITATION.cff), [`CHANGELOG.md`](../../CHANGELOG.md)), dual-licensed under CC BY 4.0 for prose and templates ([`LICENSE-CC-BY.md`](../../LICENSE-CC-BY.md)) and MIT for code and scripts ([`LICENSE-MIT.md`](../../LICENSE-MIT.md)). Its shipped surfaces are:

* **[`doctrine/`](../../doctrine/README.md)** — the methodology reference: the lifecycle, single-stance Dual-Review, roles, session routines, coordination, documentation governance, onboarding, consolidation review, and the research rationale.
* **[`templates/core/`](../../templates/core/) and [`templates/modules/`](../../templates/modules/README.md)** — the invariant kernel (`AGENTS.md`, `VENDOR.md`, `NOTICE.md`, and the `dev/` templates) plus default-on and team-gated modules.
* **[`dimensions/`](../../dimensions/README.md)** — six project axes (`age`, `size`, `complexity`, `language`, `human-team`, `agent-team`) that size a deployment's module profile.
* **[`bootstrap/`](../../bootstrap/BOOTSTRAP.md)** — the installer, 3-way lockfile-backed upgrade engine, integrity verifier (`verify_integrity.py`), and re-anchor runbook ([`bootstrap/REANCHOR_RUNBOOK.md`](../../bootstrap/REANCHOR_RUNBOOK.md)).
* **[`on-ramp/`](../../on-ramp/README.md)** — three adoption depths: read the doctrine, copy the kernel by hand, or run the bootstrap installer.
* **[`tools/`](../../tools/) and [`scripts/`](../../scripts/)** — operational utilities (`session.py`, `intent.py`, `board.py`) and prose/integrity gates (`claim_check.py`, `link_check.py`, `content_scan.py`, `quality_gate.py`, `repin.py`).
* **[`docs/`](../../docs/README.md) and [`case-studies/`](../../case-studies/README.md)** — adopter-facing guides, [`docs/plain-language.md`](../../docs/plain-language.md), [`docs/glossary.md`](../../docs/glossary.md), and the `modflow_tools` and `LHM` case studies.

### What the case-study pair shows

Comparing `modflow_tools` (greenfield, Python) and `LHM` (legacy-rooted, MATLAB + Python) under the same Maintainer separates what generalizes across scientific projects from what adapts to legacy model code:

* **Generalizes unchanged:** the proposal and plan lifecycle, append-only proposals, single-stance review with `**Foundations**` blocks, stigmergic coordination through `dev/` files, explicit-path commits, and Cairn Plain Language.
* **Adapts to legacy scientific models (`LHM`):** splitting agent roles by scientific domain (Inputs / Model / Postprocess) rather than only by lifecycle stage; a standing Legacy Agent role; a surface-readiness ledger (`Ready` / `Transitional` / `Frozen`) that gates where agents may edit; and an explicit **independent scientific check** in proposals and plans that compares model output against an analytical solution, conservation law, or reference dataset outside the implementation.

---

## Framework anchors

Cairn's design rests on **22 numbered literature anchors**. Anchor numbers are canonical and never change: [`doctrine/rationale.md`](../../doctrine/rationale.md) carries the full exposition for the harvested core anchors (1–10, 13, 16, 17), while this guide star maintains the complete 22-anchor index and the full grounding for the remaining anchors (11, 12, 14, 15, 18–22).

### Anchor index

| Cluster | # | Theme | Primary sources | Home |
|---|---|---|---|---|
| **0 · Foundation** | 13 | Durable neutral coordination layer (narrow waist) | Beck (2019); Akhshabi & Dovrolis (2011); Saltzer, Reed & Clark (1984) | [`doctrine/rationale.md`](../../doctrine/rationale.md) & below |
| **I · AI & multi-agent collaboration** | 1 | Developer–AI interaction taxonomy | Treude & Gerosa (2025), [arXiv:2501.08774](https://arxiv.org/abs/2501.08774) | [`doctrine/rationale.md`](../../doctrine/rationale.md) |
| | 2 | Multi-agent SDLC role design | Liu et al. (2025), [doi:10.1145/3712003](https://dl.acm.org/doi/10.1145/3712003) | [`doctrine/rationale.md`](../../doctrine/rationale.md) |
| | 5 | Stigmergic vs. message-passing coordination | Ricci et al. (2007); Ehtesham et al. (2025), [arXiv:2505.02279](https://arxiv.org/abs/2505.02279); Du et al. (2024), [arXiv:2305.14325](https://arxiv.org/abs/2305.14325) | [`doctrine/rationale.md`](../../doctrine/rationale.md) |
| | 11 | AI productivity value curve & verification bottleneck | METR (2025), [arXiv:2507.09089](https://arxiv.org/abs/2507.09089); METR (2026); Boehm (1981); Boehm & Basili (2001) | Below |
| | 12 | Context efficiency, length decay & instruction currency | Liu et al. (2024), [arXiv:2307.03172](https://arxiv.org/abs/2307.03172); EMNLP (2025), [arXiv:2510.05381](https://arxiv.org/abs/2510.05381); Mittal (2026), [arXiv:2609.01660](https://arxiv.org/abs/2609.01660); Gloaguen et al. (2026), [arXiv:2602.11988](https://arxiv.org/abs/2602.11988) | Below |
| | 18 | Agent deliberation pathologies & round noise | Cemri et al. (2025), [arXiv:2503.13657](https://arxiv.org/abs/2503.13657); *Stop Overthinking* (2025), [arXiv:2503.16419](https://arxiv.org/abs/2503.16419); *More Rounds, More Noise* (2026), [arXiv:2603.16244](https://arxiv.org/pdf/2603.16244) | Below |
| **II · Trust, governance & comprehension** | 3 | Trust calibration maturity model (TCMM) | Steinmetz et al. (2025), SAND2025-00999O, [arXiv:2503.15511](https://arxiv.org/abs/2503.15511) | [`doctrine/rationale.md`](../../doctrine/rationale.md) |
| | 10 | TRUST principles for digital repositories | Lin et al. (2020), [doi:10.1038/s41597-020-0486-7](https://www.nature.com/articles/s41597-020-0486-7) | [`doctrine/rationale.md`](../../doctrine/rationale.md) |
| | 14 | Scientific-software governance exemplars | USGS Fundamental Science Practices (IM OSQI 2019-01); NumPy NEP / Astropy APE; LIGO; CMIP (Eyring et al. 2016) | Below |
| | 16 | The comprehension floor & Cairn Plain Language 1.0 | Miller (2019); Kalyuga (2007); Clark & Brennan (1991); Rozenblit & Keil (2002); Naur (1985); Budescu et al. (2014); Mandel & Irwin (2020); Zhou et al. (2024); Steyvers et al. (2025); Kim et al. (2024) | [`doctrine/rationale.md`](../../doctrine/rationale.md) & below |
| | 19 | The oversight bottleneck & hierarchy | Coase (1937); *Human Oversight of Agentic Systems* (2026), [arXiv:2606.05391](https://arxiv.org/pdf/2606.05391) | Below |
| | 20 | The operator's own attention allocation | Ferster & Skinner (1957); Alter (2017) | Below |
| | 22 | Agent supply-chain & prompt-injection incidents | Thompson (1984); *s1ngularity* (2025); *Clinejection* (2026); *Comment and Control* (2026) | Below |
| **III · Scientific rigor & measurement** | 4 | AI-assisted coding rigor in science | Bridgeford et al. (2025), [arXiv:2510.22254](https://arxiv.org/abs/2510.22254); Nature CS (2025), [doi:10.1038/s43588-025-00845-2](https://www.nature.com/articles/s43588-025-00845-2) | [`doctrine/rationale.md`](../../doctrine/rationale.md) |
| | 6 | Scientific peer review as a process model | [ICMJE](https://www.icmje.org/recommendations/); [CSE](https://www.councilscienceeditors.org/); Ross-Hellauer (2017), [F1000Research 6:588](https://f1000research.com/articles/6-588); Xiang et al. (2026), [arXiv:2607.21656](https://arxiv.org/abs/2607.21656) | [`doctrine/rationale.md`](../../doctrine/rationale.md) & below |
| | 15 | Research-software V&V and reproducibility canon | Hasselbring et al. (2024); Eisty & Carver (2022); Oberkampf & Roy (2010); Roache (2002); W3C PROV-DM (2013); Sandve et al. (2013) | Below |
| | 21 | Measurement discipline & the Measurement Compact | Rahman & Devanbu (2013); Nagappan & Ball (2005); Kruchten et al. (2012); Chambers (2013); Kerr (1998); Forsgren et al. (2021); Campbell (1979); Austin (1996) | Below |
| **IV · Sustainability & restraint** | 7 | Maintenance burden & OSS typology | Eghbal (2020), *Working in Public* | [`doctrine/rationale.md`](../../doctrine/rationale.md) |
| | 8 | FAIR Principles for Research Software (FAIR4RS) | Barker et al. (2022), [doi:10.1038/s41597-022-01710-x](https://www.nature.com/articles/s41597-022-01710-x) | [`doctrine/rationale.md`](../../doctrine/rationale.md) |
| | 9 | Open development of scientific software | Prlić & Procter (2012), [doi:10.1371/journal.pcbi.1002802](https://doi.org/10.1371/journal.pcbi.1002802) | [`doctrine/rationale.md`](../../doctrine/rationale.md) |
| | 17 | Waste, proportional process & economy of mechanism | Poppendieck & Poppendieck (2003); Boehm & Turner (2003); Saltzer & Schroeder (1975) | [`doctrine/rationale.md`](../../doctrine/rationale.md) & below |

---

## Core design centers and anchor grounding

### 1. The narrow-waist coordination layer (Anchors 5, 13)

Cairn coordinates through plain Markdown files committed to Git ([`doctrine/rationale.md`](../../doctrine/rationale.md), Anchor 13; Beck 2019, [doi:10.1145/3274770](https://dl.acm.org/doi/10.1145/3274770); Akhshabi & Dovrolis 2011, [doi:10.1145/2018436.2018460](https://dl.acm.org/doi/10.1145/2018436.2018460)). Just as MODFLOW's plain-text input and output formats act as a narrow waist between solver engines below and analysis tools above, `dev/` Markdown in Git acts as a minimal waist between:

* **Below the waist:** the project's scientific stack (Python, Fortran, MATLAB, R, Rust).
* **Above the waist:** the AI coding harnesses (Claude Code, Codex, Gemini/Antigravity) and Cairn's Python helper scripts.

Agents may use native harness messaging for real-time holds or relays, but nothing has authority until it is committed to the repository (cognitive stigmergy, Anchor 5). Because the waist is plain text in Git, vendor-neutrality is enforced today. Tooling stack-neutrality remains partial: the methodology is language-independent, while the helper scripts (`bootstrap/`, `tools/`, `scripts/`) are written in Python.

### 2. Peer review and independent scientific checks (Anchors 4, 6, 14, 15)

Cairn models review on scientific peer review (Anchor 6) and agency-stewarded software release practices such as the USGS *Fundamental Science Practices* two-review requirement (code review plus domain review, **Anchor 14**: USGS IM OSQI 2019-01; NumPy NEP / Astropy APE; LIGO blind-injection validation, arXiv:1612.07864; CMIP protocol coordination, Eyring et al. 2016, doi:10.5194/gmd-9-1937-2016).

Three empirical findings shape how Cairn runs review today:

* **One stance, three stage-specific questions.** Every reviewer asks whether the work should happen as framed, what the strongest alternative is, and what would show it wrong, backed by citations to files, lines, or commands ([`doctrine/dual-review.md`](../../doctrine/dual-review.md)).
* **Cross-model distance is a Maintainer call, not a blanket rule.** Controlled evaluation of cross-model code review shows that direction matters: on 116 tasks, one cross-model direction raised pass rates from 71.6% to 89.7%, while the reverse direction lowered them from 91.4% to 82.8% (Xiang et al. 2026, [arXiv:2607.21656](https://arxiv.org/abs/2607.21656)). Cairn therefore records who reviewed every artifact and leaves cross-model **External reads** to the Maintainer's explicit call rather than mandating a blanket cross-model floor.
* **Agreement between agents proves consistency, not scientific correctness.** Two agents can agree on a wrong equation, and a green unit test can reverse the same sign as the code it tests. Field reports and benchmarks in 2026 confirm this gap: SWE-bench Science found top agents below 50% on 119 repository tasks ([arXiv:2608.19799](https://arxiv.org/abs/2608.19799)), SciCode-Verified showed accuracy jumping from 9–27% to 69–92% once domain experts fixed faulty specifications and test oracles ([arXiv:2608.04975](https://arxiv.org/abs/2608.04975)), and Bhave et al. (2026, [arXiv:2605.17675](https://arxiv.org/abs/2605.17675)) demonstrated AI-assisted verification anchored on known-solution validation cases (see also the 2026 scientific-computing ecosystems report, [arXiv:2608.26519](https://arxiv.org/abs/2608.26519)).

**Anchor 15 (Research-software V&V and reproducibility canon):** Hasselbring et al. (2024, arXiv:2404.14364); Eisty & Carver (2022, doi:10.1007/s10664-022-10184-9); Oberkampf & Roy (2010, *Verification and Validation in Scientific Computing*, Cambridge UP); Roache (2002, *Code Verification by the Method of Manufactured Solutions*, J. Fluids Eng. 124(1):4–10); W3C PROV-DM (2013); Sandve et al. (2013, doi:10.1371/journal.pcbi.1002802). In Cairn, every proposal or plan that touches scientific calculations, units, coordinate systems, or reference data must name an **independent scientific check** grounded outside the proposed implementation (an analytical solution, conservation constraint, or external dataset).

### 3. Trust, comprehension, and supply-chain safety (Anchors 3, 10, 16, 22)

Adopting Cairn gives AI agents write access to a scientific repository. Cairn bounds that risk through two mechanisms: the comprehension floor and structural supply-chain defenses.

**The comprehension floor and Cairn Plain Language 1.0 (Anchor 16).** Grounded in recipient-designed explanation (Miller 2019), the expertise-reversal effect (Kalyuga 2007), conversational grounding (Clark & Brennan 1991), the illusion of explanatory depth (Rozenblit & Keil 2002), appropriate reliance ([arXiv:2301.11333](https://arxiv.org/abs/2301.11333), [arXiv:2305.07722](https://arxiv.org/abs/2305.07722), [arXiv:2608.12355](https://arxiv.org/abs/2608.12355), [arXiv:2602.16844](https://arxiv.org/abs/2602.16844)), and Naur's (1985) *Programming as Theory Building* ([`doctrine/rationale.md`](../../doctrine/rationale.md)). It has three operational legs:

1. **Calibrate to the reader without stripping domain terms.** Keep the field's technical terms, define specialist terms where they first matter, and unpack stacked nouns.
2. **Stand without the deliberation record (the temporal half).** Durable code, tests, and comments must make sense to the next reader after the proposal and plan are archived; test names state the property they pin, never internal finding codes (`F5`, `CR1`).
3. **State epistemic confidence and uncertainty in usable form.** Because language models rarely express uncertainty unprompted and are overconfident when wrong (Zhou et al. 2024; Steyvers et al. 2025; Kim et al. 2024), and because bare probability words like "likely" fail across readers (Budescu et al. 2014; Mandel & Irwin 2020), Rules 13–17 of Cairn Plain Language require agents to separate *measured*, *assumed*, and *expected* claims, give numbers with units and sources, and state in the first person what they checked and did not check.

**The agent supply-chain incident record (Anchor 22).** Following Thompson (1984, *Reflections on Trusting Trust*), production incidents in 2025–2026 showed what happens when coding agents read untrusted text while holding credentials and network access:

* *s1ngularity* (2025-08-26): trojanized Nx build packages invoked developers' local CLI agents with permission-bypass flags to exfiltrate 2,349 credentials from 1,079 machines.
* *Clinejection* (2026-02-17): a prompt injection in a GitHub issue title compromised a CI agent holding shell and write permissions, stole an npm publish token, and pushed a compromised package to ~4,000 machines ([CSA research note](https://labs.cloudsecurityalliance.org/research/csa-research-note-clinejection-prompt-injection-cicd-cache-p/)).
* *Comment and Control* (2026-06): prompt injections in PR titles, issue bodies, and HTML comments extracted live API keys and write tokens across major agent integrations ([CSA research note](https://labs.cloudsecurityalliance.org/research/csa-research-note-claude-code-github-action-prompt-injection/)).

Cairn's defenses are structural: no autonomous CI agent, no network egress in verification tools, **humans alone push**, `content_scan.py` screens agent-loaded files for hidden instructions, and `verify_integrity.py` checks lockfile digests and refuses symlinked paths before use.

### 4. Restraint, context efficiency, and measurement discipline (Anchors 11, 12, 17, 18, 19, 20, 21)

The main threat to a review-centered methodology is not that review fails, but that process ceremony grows until it crowds out the science.

* **The verification bottleneck (Anchor 11).** METR's randomized trial of experienced open-source developers ([arXiv:2507.09089](https://arxiv.org/abs/2507.09089)) and its February 2026 follow-up ([study-design update](https://metr.org/blog/2026-02-24-uplift-update/)), alongside Microsoft's rollout study ([arXiv:2607.01418](https://arxiv.org/abs/2607.01418)) and Epoch AI / METR's [MirrorCode report](https://epoch.ai/publications/mirrorcode-preliminary-results), show that as code generation accelerates, human verification becomes the bottleneck. Catching defects in review rather than after publication follows Boehm (1981) and Boehm & Basili (2001), without relying on inflated cost multipliers.
* **Context efficiency and rule currency (Anchor 12).** Long contexts degrade retrieval and reasoning (Liu et al. 2024, [arXiv:2307.03172](https://arxiv.org/abs/2307.03172); EMNLP 2025, [arXiv:2510.05381](https://arxiv.org/abs/2510.05381)), while trajectory-level studies show step count driving agent decay (Mittal 2026, [arXiv:2609.01660](https://arxiv.org/abs/2609.01660)) and generic repository overview files adding >20% inference cost without improving task success unless they state non-standard project rules (Gloaguen et al. 2026, [arXiv:2602.11988](https://arxiv.org/abs/2602.11988); rule-file mining study, [arXiv:2606.12231](https://arxiv.org/abs/2606.12231)). Cairn keeps `AGENTS.md` focused on operational rules the agent would not otherwise know and loads module guidance on demand.
* **Agent deliberation pathologies and the one-round rule (Anchor 18).** Multi-agent failure taxonomies (Cemri et al. 2025, [arXiv:2503.13657](https://arxiv.org/abs/2503.13657)), overthinking studies ([arXiv:2502.08235](https://arxiv.org/abs/2502.08235); [arXiv:2503.16419](https://arxiv.org/abs/2503.16419)), and verbosity-bias research ([arXiv:2310.10076](https://arxiv.org/pdf/2310.10076)) show that unconstrained agent deliberation degrades outcomes. In code and proposal review, *More Rounds, More Noise* ([arXiv:2603.16244](https://arxiv.org/pdf/2603.16244)) measured a second review round raising total findings per artifact from 9.3 to 15.2 while true positives rose only from 2.64 to 3.03. Cairn therefore caps standard review at **one round**: the author's response and revision carry a proposal to `awaiting-decision`, with a second round allowed only if the revision widened scope, introduced new code defects, or left a Security Review open.
* **The oversight bottleneck and hierarchy (Anchor 19).** Following Coase (1937, *The Nature of the Firm*) and 2026 studies of human oversight ([arXiv:2606.05391](https://arxiv.org/pdf/2606.05391)), human attention is the scarce resource. Agents resolve routine sequencing, dispositioning, and archiving on their own; only a finite list of irreversible calls (accepting/rejecting a proposal, changing scope, pushing, and trust ceremonies) goes to the Maintainer, always accompanied by a concrete recommendation (`dev/agent_collaboration.md`).
* **The operator's own attention allocation (Anchor 20).** Prompting coding agents inadvertently creates a variable-ratio reinforcement schedule — cheap pulls with variable, high-leverage payouts and no natural social stopping cues (Ferster & Skinner 1957, *Schedules of Reinforcement*; Alter 2017, *Irresistible*). Because a scientist's primary work is the science, Cairn includes five operator norms:
  1. *Prefer asynchronous batches over rapid back-and-forth loops* (scope work, step away, review at defined windows).
  2. *Set a calendar budget for methodology and meta-work* outside the session.
  3. *Glance at hours spent in agent sessions against shipped scientific output.*
  4. *Name the pull to a colleague* so social boundaries remain active.
  5. *Close sessions cleanly* (`goodnight`) without dangling next-step hooks.
* **Measurement discipline and the Measurement Compact (Anchor 21).** Grounded in process-metric empirical studies (Rahman & Devanbu 2013; Nagappan & Ball 2005), technical-debt theory (Kruchten, Nord & Ozkaya 2012), Registered Reports and HARKing (Chambers 2013; Kerr 1998), multidimensional productivity (Forsgren et al. 2021, *SPACE*), and measurement dysfunction (Campbell 1979; Austin 1996). Five rules govern all measurement in Cairn:
  1. **Measure structural events; never measure prose.** Any metric scraped from text or readability scores makes the text the optimization target.
  2. **Prefer git history to static code shape.** Process measures derived from version history outperform static complexity metrics unless static metrics are decorrelated from size.
  3. **Declare the population and analysis before results exist**, state limits before findings, and define an explicit `INCONCLUSIVE` branch.
  4. **Measure forward; never back-annotate the archive with a hypothesis in hand.**
  5. **No composite scores and no per-agent or per-person rankings, ever.** Under the **Measurement Compact**, measurements are internal diagnostics rather than marketing claims, no role- or tier-confounded count is read as capability proof, and publishing any measurement externally requires an explicit Maintainer Decision.

---

## Still open

This list tracks the gaps that remain open in Cairn today, tagged by anchor number:

* **No comparative baseline study yet (3, 11, 21).** Cairn has git-derived activity records across its own repos, but no side-by-side comparison against the lighter baseline named under *What Cairn is*.
* **No external reader view of the decision archive (3, 8).** The `dev/` archive is complete in Git, and `tools/board.py` summarizes active work, but an outside reader still has to browse raw repository files to trace historical decisions.
* **Independent scientific check is template guidance, not yet a dimensional preset (4, 6, 15).** The proposal and plan templates require an independent scientific check (`independent-scientific-check`), while a full `deliverable` dimension mapping software character (simulation model, wrapper, inverse/calibration, data pipeline) to verification presets remains unbuilt (issue #19).
* **Reviewer diversity is bounded by available model families (6).** Cross-model review reduces correlated blind spots but cannot exceed the distinct model families available to the team.
* **Helper tooling is Python-only (13).** The Markdown + Git coordination waist is stack-neutral; `bootstrap/`, `tools/`, and `scripts/` require Python 3.11+.
* **Always-loaded context budget is unmeasured (12).** `AGENTS.md` and `dev/agent_collaboration.md` are kept lean by review, without an automated token-budget gauge.
* **Cairn Plain Language 1.0 awaits its three-month evaluation (16).** Adopted on 2026-10-26 after testing on three internal passages; its check is the Maintainer's review in late January 2027 (whether *"I don't understand this yet"* pauses are rarer and reviews stay free of style policing).

### Candidate future moves (not queued)

None of these moves is scheduled; except for the timed three-month check on Cairn Plain Language, all framework expansions wait on the outside-adoption comparison:

1. **One outside adoption compared against the lighter baseline** (*What Cairn is*).
2. **One end-to-end worked scientific example** — a hydrology change carried through specification, an independent analytical or conservation check, reproduction, and plain explanation.
3. **Three-month evaluation and standalone publication of Cairn Plain Language** (late January 2027) — a standalone page and paste-in block with its own DOI once tested in daily use across Cairn, `LHM`, and `modflow_tools`.
4. **Optional dimensional extensions** (a `deliverable` scientific-character axis, a community/succession governance axis, or dynamic maturity-level recommendations) — held behind comparative adoption evidence.

---

## Anti-scope

This guide star describes Cairn's rationale, current state, and open gaps; **it is not implementation authority**. Every change to Cairn's rules, templates, dimensions, or tooling requires its own proposal or plan and Maintainer Decision. In particular, this document does not authorize:

* Adding new `dimensions/` axes or automated maturity instrumentation.
* Changing Cairn's lifecycle, review rules, or role definitions.
* Running autonomous CI agents, adding telemetry, or pushing without explicit Maintainer approval.

The guide star remains the scientist's work, not Cairn's growth.
