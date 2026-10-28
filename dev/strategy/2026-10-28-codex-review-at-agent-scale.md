# Code review at agent scale

**Author**: Codex / Strategy
**Model**: GPT-6 (exact runtime variant unavailable)
**Date**: 2026-10-28
**Status**: draft
**Type**: design-exploration
**Surfaces this would feed**: a v0.7 proposal for adopter code-review support; review guidance, an agent skill and optional tool integrations. Scheduling is tentative; this note authorizes no implementation or policy change.

## The question / felt gap

How can scientists get good code review when agent teams produce changes faster than people can read them? Cairn should help teams find consequential defects, understand scientific effects and finish reviews at a sustainable cost. Increasing comment volume or making the scientist approve every detail would miss the goal.

The capability should serve human reviewers, agent reviewers and mixed teams. Its distinctive contribution would be a usable review workflow grounded in research, with scientific context and portable evidence. The interface should follow that workflow.

## Method

Surveyed research through 2026-10-28 using [Consensus](https://consensus.app/search/we-are-designing-a-stage-0-strategy-for-a-vendor-n/_nAR66dJQ26RyG3grawJlA/), arXiv and primary engineering accounts; opened the sources below directly. This is a targeted survey, not a systematic review. Consensus supplied discovery leads; its generated synthesis is not an independent verification of a paper.

Read Cairn's [review doctrine](../../doctrine/dual-review.md), [review sweep](../agent_collaboration.md#the-review-sweep), shipped architecture/testing modules and v0.7 roadmap during orientation at `bd582403`. Examined adjacent strategy, active verification work and the GitHub documentation below. This was no code audit, installation, benchmark or adopter trial.

## Findings: evidence and its limits

| Source and kind | What it supports; what it does not establish |
|---|---|
| [Bacchelli & Bird, ICSE 2013](https://www.microsoft.com/en-us/research/publication/expectations-outcomes-and-challenges-of-modern-code-review/); [Sadowski et al., ICSE SEIP 2018](https://research.google/pubs/modern-code-review-a-case-study-at-google/). Industrial empirical studies. | Change understanding, knowledge transfer and small, quick review cycles matter alongside defect finding. Large-company practices do not establish the right workload for a science team. |
| [Alami & Ernst, CHASE 2025](https://arxiv.org/abs/2501.02092), 20 interviews; [Zhong et al., March 2026 preprint](https://arxiv.org/html/2603.15911v1), observational review conversations. | Excessive AI feedback can increase cognitive load; humans contribute understanding and testing feedback. Suggestion adoption measures neither correctness nor causal productivity by itself. |
| [AACR-Bench, January 2026 v1](https://arxiv.org/html/2601.19494v1); [c-CRAB, March v1](https://arxiv.org/html/2603.23448v1); [CRBugBench, October v1](https://arxiv.org/html/2610.13668v1). Benchmark preprints. | Context and evaluation design matter. CRBugBench reports misleading-author-claim failures and tested multi-agent configurations with extra cost but no consistent gain. These evaluate particular defects; c-CRAB also depends on a repair agent. Scores are not interchangeable measures of overall review quality. |
| [SecPRBench, October 24, 2026 v1](https://arxiv.org/abs/2610.33509). New security benchmark preprint. | Uses validated bug-introducing changes and examines mistaken diagnoses. Its recent results, model-judged findings and security focus warrant validation before transfer to scientific work. |
| [Anthropic engineering account, October 15, 2026](https://claude.dev/blog/solving-code-review-at-anthropic/). Practitioner report. | Describes author-side verification, fresh-context review, short project instructions, effort matched to risk, revision-focused reads and incident feedback. Reported operational improvements are not a controlled demonstration that this whole package caused them. |
| [StrongDM software factory, February 2026](https://factory.strongdm.ai/). Practitioner design account. | Offers a stronger alternative: agents converge against scenarios held outside the implementation. This makes independent behavioral checks worth exploring; its position against human code review is not evidence that scientific judgment can be removed. |

These sources motivate the practices below. Their combination is a Cairn design hypothesis, not a validated recipe. Scientific validity remains a separate evaluation target: software bug benchmarks do not establish correct units, numerical assumptions or research conclusions.

## Practices to make usable

1. **Prepare reviewable changes.** Authors supply purpose, expected behavior, affected callers, scientific assumptions and existing verification evidence. Group changes by coherent behavior and distinguish mechanical edits. Preserve a view of the integrated change: splitting a large patch must not hide interactions.
2. **Spend machine effort before reviewer attention.** Reuse tests, linters and security scanners for their actual properties. Tie evidence to code, environment and command; show failed, skipped and untested work. Carry valid evidence forward and refresh affected checks after revisions. More reviewers must not multiply broad suite runs.
3. **Let reviewers form their own account.** A fresh agent reconstructs behavior from code, contracts and relevant callers, treating the author's explanation as a claim. Record uncertainties before reading other reviewers' conclusions where practical. Test delayed reveal of agent findings for human reviewers as a bias-reduction hypothesis, rather than assuming it works.
4. **Manage agent output as a queue.** Assign review effort by consequence, uncertainty and available expertise. Add parallel specialist reads for concrete questions; give one reviewer responsibility for interactions across their boundaries. Consolidate duplicate findings with attribution and dissent intact. Slow new implementation when unresolved review accumulates; adding agents alone is not a capacity plan.
5. **Make findings actionable.** Show impact, mechanism, location, evidence and what would resolve the concern. Separate demonstrated defects, reasoned concerns, questions and optional improvements. Reveal supporting detail on demand. Agreement among models is not proof, and a clean pass creates no quota of comments.
6. **Close revisions deliberately.** Compare iterations, reopen affected dependencies and verify the remedy. Show which conclusions became stale and why. Finish when owed questions and checks are settled; continue for new defects or unresolved obligations under Cairn's current rules. Route scientific assumptions and consequential tradeoffs to the appropriate person, with a brief they can understand.

For example, a horizontal-well calculation needs the reviewer to inspect geometry, units, boundary conditions and independently justified reference behavior. A green Python suite or an attractive plot cannot answer all four.

## GitHub projects and tools to learn from

Documentation inspected 2026-10-28; these are design examples, not audited dependencies or a ranking.

| Project / building block | Lesson for Cairn; adoption question |
|---|---|
| Git diff, immutable commits, worktrees and [range-diff](https://git-scm.com/docs/git-range-diff) | Identify reviewed bytes, isolate probes and compare patch iterations. |
| [nbdime](https://nbdime.readthedocs.io/en/latest/) | Notebook-aware source/output comparison; rendered output still needs reproducibility checks. |
| [reviewdog](https://github.com/reviewdog/reviewdog) | Reuse local/forge diagnostics and SARIF exchange. Changed-line filtering can hide relevant findings elsewhere. |
| [PR-Agent](https://github.com/The-PR-Agent/pr-agent) | Learn configurable review commands and provider adapters. Compare forge integration and deployment costs before writing equivalents. |
| [OpenQodex](https://github.com/openqodex/openqodex) | Study scanner -> finder -> verifier flow, checked evidence quotes and HTML/Markdown/JSON/SARIF reports. Changed-line assignment is not proof of behavioral coverage; its hooks/downloads need scrutiny. |
| [revmux](https://github.com/umputun/revmux) | Learn supervised subprocesses, timeouts, run archives and separate human/agent output. Test synthesis and inherited-round anchoring before adopting its review panel. |
| [Review Council](https://github.com/deployhq/review-council) | Study isolated refutation, inconclusive findings and preserved dissent. Cross-model confirmation remains model evidence; its default panel and retained suppressions need evaluation. |
| [Kodus](https://github.com/kodustech/kodus-ai) | Learn repository/path rules, issue tracking and cost visibility from a self-hostable review platform. Check its license split, services, telemetry and model egress before adoption. |
| Research benchmarks above | Borrow fault categories and evaluation methods; supplement with unseen scientific cases rather than using a leaderboard to select a universal reviewer. |

External tools stay optional integrations. Check maintenance, licenses and security at a pinned version before a trial. Cairn's shipped core remains standard-library-only and vendor-neutral.

## Options and recommendation

**Guidance and a review skill** offer the cheapest baseline. **A portable review workspace** could add a concise human view and structured agent input/output. **A hosted orchestrator** could manage queues and forge events but adds service, credential and maintenance costs. Keeping current practice is the control option.

Explore the workspace through a guidance-first pilot, trying existing projects before building orchestration. Its candidate flow is **change brief -> independent examination -> evidence-backed findings -> disposition**. A scientist sees scientific effects, unresolved risks and decisions needed; an agent sees the same record with locations and evidence links. Reuse Cairn's review record. Choose browser, terminal or forge presentation after observing use.

Repository text and findings are untrusted inputs. Separate inspection from executing candidate code, and local processing from transmitting research data. Any prototype must expose those choices, avoid implicit execution/uploads and preserve review attribution. This note changes no review floor or approval authority.

## Pilot and open questions

Compare current Cairn review, guidance/skill support and a minimal workspace on matched ordinary and scientific changes. Include correct changes, historical defects and independently prepared hidden faults in units, numerical behavior, provenance, notebooks and cross-file interactions. Counterbalance assignment to reduce learning effects; use domain adjudication and behavioral checks, not agent consensus, as the reference.

Measure consequential faults missed, false findings, adjudication and repair time, queue age, token/tool cost and regressions introduced by fixes. Ask scientists to explain a change's effect, rather than merely rate the summary. Follow escaped defects during use; a small pilot cannot establish safety from their absence. Set success margins before collecting results. Reject the workspace if it saves no attention or sacrifices consequential detection relative to the lighter option.

Compose with [architecture support](2026-10-27-codex-adopter-engineering-practices.md), [scientific testing](2026-10-27-antigravity-judicious-testing-and-simulation-verification.md), [team measurement](2026-10-27-antigravity-lightweight-team-measurement.md) and [scoped verification](../plans/scoped-change-verification.md). Those retain their own scopes. Before promotion, settle pilot participants, scientific reference cases, private-data constraints, integration costs and ownership of dated literature/tool evaluations. The methodology-general outcome should reach shipped adopter guidance as well as Cairn's own practice.
