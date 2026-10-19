# Cairn as a core with two profiles: Develop for code, Lab for research

**Author**: Claude (Strategy, for the Maintainer)
**Model**: claude-fable-5-1
**Date**: 2026-10-19
**Status**: draft
**Type**: design-exploration
**Surfaces this would feed**: a Cairn proposal to refactor the proposal and plan templates into slot-filled profiles, after the Cairn Lab toy has run 20 to 30 cycles; the `cairn-lab` adopter repository (MSUHydrogeology/cairn-lab, not yet created); the LHM proposal `agent-run-contract` (in LHM's tree, opened 2026-10-16); `dimensions/README.md` if a research axis is added

## The question / felt gap

The Maintainer is building a second kind of Cairn adopter. LHM adopts Cairn to change *software* under review. Cairn Lab adopts it to run a community of persistent AI research labs that change *what is known* under review: labs write short papers with executable evidence, a journal agent re-runs and reviews them, accepted claims enter a shared record, and labs build on the record. The two share the deliberation discipline and almost nothing else: one ships files a person reads, the other is a runtime that executes models nightly.

The question is whether Cairn should become a core plus two profiles, Cairn Develop and Cairn Lab, and if so what is actually in each. A secondary question, raised by the Maintainer: which ideas from existing agent-research tools (crux and its relatives) Cairn Lab should reuse rather than reinvent.

This note answers both from the repository as it stands. It does not propose the split. It records what the split would move, what it would not, and what has to be learned from the toy first.

## Method

* Read the Cairn tree at `f9e1d572`: `doctrine/` (14 files), `dimensions/` (6 axes), `templates/core/` (18 files), `templates/modules/default-on` and `templates/modules/team-gated` (8 and 18 modules), `bootstrap/`, `tools/`, `scripts/`, `examples/`, and the slot markers in `templates/core/dev/proposals/_template.md` and `templates/core/dev/plans/_template.md`.
* Read LHM's `AGENTS.md`, `RULES.md`, `dev/README.md`, and its proposal template as the installed instance of the Develop shape (LHM's tree, 2026-10-16).
* Read the Cairn Lab concept document (Maintainer's OneDrive, revision of 2026-10-18) and the three external reviews folded into it, two by Codex and one by a Claude session in this repository.
* Read the crux README (github.com/mehdiforoozandeh/crux) and the published descriptions of AgentRxiv, Sakana's AI Scientist, the Virtual Lab, Google's Co-Scientist, and FutureHouse's Robin, as surveyed in the concept document's precedent section.
* Counts below are point-in-time at `f9e1d572`; `python scripts/verify_counts.py` is the discipline for keeping them honest.

What would falsify the recommendation: a toy run in which the Lab's fidelity manifest records no deviations from core templates (then no Lab profile is needed, only modules), or one in which the deviations touch doctrine rather than templates (then the split is deeper than slots and this note underestimates it).

## Findings

### 1. Cairn is already core plus adaptation; the split is a sort, not a rewrite

The `dimensions/README.md` states the design: a small invariant core, with structure added only as a project warrants. In practice the tree already separates three kinds of content:

| Kind | Where | Software-specific? |
| --- | --- | --- |
| Invariant doctrine | `doctrine/` | No. None of the 14 files names a language, a test suite, or a build. `doctrine/proposals.md` and `doctrine/plans.md` describe deliberation artifacts; both profiles use them |
| Adaptation axes | `dimensions/` | Half. Age, size, complexity, and language describe a codebase. Human-team and agent-team describe a team and apply to any adopter |
| Templates | `templates/core/` | Mixed. `AGENTS.md`, `VENDOR.md`, and the `dev/` tree skeleton are general. The proposal and plan templates interleave the lifecycle with software verification |
| Modules | `templates/modules/` | Mixed, roughly half and half (table below) |
| Bootstrap and tools | `bootstrap/`, `tools/`, `scripts/` | Mostly general; a few scripts are code-only |

### 2. Where each piece lands

| | Cairn (core) | Cairn Develop | Cairn Lab |
| --- | --- | --- | --- |
| Doctrine | All 14 files unchanged | A profile README: what a proposal, plan, and review mean when the artifact is a code change | A profile README: what a paper, review, and reproduction mean when the artifact is a claim about the world |
| Dimensions | human-team, agent-team | age, size, complexity, language | New: evidence kind (model run, observation, both), persistence depth, lab count |
| Templates | `AGENTS.md`, `VENDOR.md`, the `dev/` tree, and the proposal and plan templates with their software sections turned into slots | Fills the slots: verification boundaries A, B, C; tests tier; examples and smoke checks; security preflight; assurance-path triggers; install-contract triggers; the codebase-readiness report; greenfield and legacy project profiles | Fills the same slots: the paper template with contribution type and pre-registered next test; the claims record; reproduce versus baseline regression; the lab scope file; the operating specification |
| Modules, default-on | claim-check, documentation-plan, incident-trackers, reflections, onboarding | security-verification | lab-persistence, journal |
| Modules, team-gated | content-security, issue-capture, intent (work-intent claims), coordination-tiers, dual-review, model-selection, doc-drift-prevention | legacy-agent, domain-agents, architecture-review, testing-discipline, dual-language-tests, examples-gallery, security-review, python-security, api-access-security, web-hosting-security, portable-security-sweeps | replicator, claims-store, seeded-tests, audit-budget, conferences, harness-adapter |
| Bootstrap | scaffold, verify_integrity, upgrade and reanchor runbooks, container, profile selection | The three current profiles (solo-greenfield, collaborative-team, high-rigor-legacy) | New profiles: toy-lab, multi-lab |
| Tools and scripts | session, board, intent, the prune tools, gauge, audit_report, evolution_infer, claim_check, content_scan, link_check, token_budget, the label bootstraps | quality_gate, the legacy-pass generators, security_check, sync_doc_snippets, check_model_selection (arguable: model selection is general, its mapping is code-shaped) | a controller, a claims query, the board writers |
| Examples | none | minimal, scientific-minimal | the Cedar Creek ecosystem |

By file count the core is roughly three-fifths of the tree. Everything LHM and Cairn Lab both reuse unchanged is in that three-fifths.

### 3. The real work is in two files

The proposal and plan templates are the only places where core and profile are interleaved in one document. They already carry `cairn:slot` regions (`triage-extra-triggers`, `documentation-tier-home`, `tests-tier-home`, `examples-smoke-home`, `assurance-path-triggers` in the proposal; `documentation-tier-home`, `acceptance-doc-tooling`, `verification-commands` in the plan). The split extends that mechanism: the security preflight, the verification-boundary doctrine, and the assurance-path definitions become slots too, and a *profile* is a named set of slot fills plus a module list plus a dimension position. No file moves between repositories to achieve this. Whether the profiles then live as directories in this repository or as sibling repositories is a packaging choice the proposal can make late.

### 4. Security straddles the boundary

`security-verification` is default-on and most of its body is about code. The honest division: the core keeps the obligation (a high-risk surface takes a security review, declared in the header, satisfied only by a matching pass); Develop keeps what counts as a high-risk surface in software (deserialization, subprocess, parsing, credentials); Lab defines its own (the controller's protected authority, the held-out evaluation data, the seeded-test answers, the trust boundary between an agent-written adapter and a trusted one). The five preflight questions S1 to S5 are general and stay in the core.

### 5. What Cairn Lab should take from existing tools rather than build

The concept document's precedent survey found no system that combines persistent multi-lab research with independently re-run experiments in a physical-science domain. It did find components worth reusing. Each maps to a Cairn concept, which is the test of whether it belongs.

| Tool or practice | What it does | Cairn concept it maps to | Reuse decision |
| --- | --- | --- | --- |
| **crux** (github.com/mehdiforoozandeh/crux) | A plain-Markdown lab notebook an agent drives: a tree of questions and falsifiable hypotheses; each hypothesis carries pass/fail "verifiables" written before the run; findings and reports attach; a stdlib-only engine rolls evidence up, derives supported, partial, refuted, or inconclusive from checkboxes a human set, and keeps a human review gate; a read-only browser cockpit; a curated literature wiki; installs as agent skills | The lab's durable state (the `dev/` tree for a lab); pre-registration as the Lab analogue of a plan's acceptance criteria; the human Decision as the Lab's sign-off gate; `NEXT_SESSION.md` as a working summary over an inspectable record | **Adopt** as each lab's notebook, as a Develop-maintained fork (four stars; pinned release, enumerated patches, an exit for each). Its question tree is the persistence representation the third review asked for; its verifiables are the pre-registered next test; its refusal to read run logs keeps the verdict human. The Maintainer decided this on 2026-10-18 |
| **Registered reports** (Stage-1 and Stage-2 review) | Methods reviewed before data; outcome reviewed after | Cairn's own README frames a proposal as the Stage-1 registered report. The Lab paper is the Stage-2 report; the lab's pre-registered test is its Stage-1 | **Already in Cairn**; the Lab profile names both stages |
| **Architecture decision records** | Append-only, one decision per file, superseded rather than edited | The proposal lifecycle's append-only rule | **Already in Cairn** |
| **Experiment trackers** (MLflow, Weights and Biases) | Run IDs, parameters, metrics, artifacts per run | The run certificate the controller writes; the `requires` relation from a claim to its runs | **Reuse the idea, not the tool**: a run certificate in the record, written by the controller, is enough for the toy; crux's README says it sits beside such trackers, which is the right boundary |
| **Data version control** (DVC, git-annex) | Content-addressed data versions referenced from git | Input hashes in the run certificate; `depends_on` to a dataset version | **Reuse the idea**: hash and name every input the harness reads; adopt a tool only if inputs outgrow the repository |
| **Containers and lockfiles** | A reproducible environment | The replicator's clean container; Cairn's own `bootstrap/container` | **Already in Cairn** |
| **AgentRxiv** (Schmidgall and Moor, 2025) | A shared preprint server that lets agent labs build on each other's work; three labs beat one on a benchmark; the authors verified every reported number by hand because agents wrote placeholder code and mismatched results | The shared record; the replication gate | **Adopt the structure, not the trust model**: the shared record is the preprint server, with the journal's reproduction as the step AgentRxiv did by hand |
| **Sakana AI Scientist** (Nature, 2026) | An automated reviewer that aggregates several independent reviews and tracks human decisions on OpenReview data; an agent that tried to extend its own timeout | The journal's reviewer tier; the controller's protected authority | **Adopt the reviewer aggregation**; the timeout incident is the reason the controller's live configuration is outside agent reach |
| **Virtual Lab** (Swanson, Zou, Pak, Nature 2025) | A PI agent plus a Scientific Critic plus specialists, with about one percent human input, produced designs validated in a wet lab | A critic as the Internal review floor; the human who sets the question | **Already in Cairn** as the Internal and External tiers; the Lab profile's journal is the critic made independent |
| **Google Co-Scientist** (2025) | A reflection agent and tournament ranking with Elo ratings over hypotheses; self-ratings tracked expert judgment | Ranking the question queue; prioritizing audits by consequence | **Reuse for the audit budget**: a cheap tournament over open questions orders what the Maintainer reads, which the third review's attention-budget finding requires |
| **FutureHouse Robin** (2025) | Multi-agent drug repurposing; the analysis agent was weak on statistics | Harness does the arithmetic; the agent configures and interprets | **Design rule, no tool** |
| **OpenReview** | Public reviews with reviewer identity and scores | Attributed, self-committed reviews | **Already in Cairn** |

Two lessons cut across the table. First, every precedent that reported honestly found that re-execution catches less than it seems: placeholder code, impossible plans written up as success, numbers that did not match. Cairn Lab's claim statuses, held-out scoring, and seeded tests exist because of that, and they are Lab-profile content with no Develop analogue. Second, the tools that survive are the ones that keep the human verdict out of the machine's hands: crux does not read run logs; Cairn's Decision is quoted verbatim. That is a core property, and the Lab profile must not weaken it in the name of autonomy.

### 6. What a toy will tell us that this note cannot

The Cairn Lab toy (two labs, one journal, one basin, 20 to 30 nightly cycles) runs as an ordinary Cairn adopter with a fidelity manifest. The manifest will list every core template or module the Lab bent and why. That list is the Lab profile's first draft, derived from evidence rather than from this table. Until it exists, the sort above is a hypothesis about where the boundary falls.

## Options

1. **Do nothing to Cairn.** Cairn Lab stays an adopter indefinitely, carrying its deviations in its own manifest and modules. Costs: every Lab-specific template section is a local override that drifts from core on each consume; a second Lab adopter would copy them by hand; the science-discipline family stays an issue on the tracker rather than a shipped thing.
2. **Profiles by slots, one repository.** Extend the slot mechanism in the two templates, define a profile as slot fills plus modules plus a dimension position, ship Develop and Lab as directories under a new templates/profiles tree (a proposed path; it does not exist today). Costs: a template refactor through the deliberate lane; the three existing bootstrap profiles become Develop sub-profiles. Benefits: no repo surgery, one consume path, and Develop is simply the name for what the current profiles already are.
3. **Profiles by slots, three repositories.** As option 2, then split Develop and Lab into sibling repositories that depend on core. Costs: three release trains and a cross-repository consume. Benefits: separate maintainers become possible; the Lab runtime (a program) does not sit inside a methodology repository.
4. **Fold Lab into modules only, no profile concept.** Treat journal, replicator, claims-store, and the rest as team-gated modules of the existing kind. Costs: the paper template and the reproduce gate cannot be expressed as modules, because they replace the proposal template's software sections rather than add to them.

## Recommendation

Option 2, after the toy. Specifically:

* **Now**: create MSUHydrogeology/cairn-lab as a Cairn adopter with the standard bootstrap and a fidelity manifest. Fork crux under Develop's fork rules. Run the toy. Change nothing in this repository.
* **After 20 to 30 cycles**: open a Cairn proposal titled something like `profiles-by-slots`, with the Lab's fidelity manifest as its Context. The proposal turns the software sections of the proposal and plan templates into slots, defines the profile mechanism, and ships two profiles: Develop (the current profiles, renamed and grouped) and Lab (the manifest's deviations, generalized). The security straddle (finding 4) is a named chunk of that proposal.
* **Defer** the three-repository question (option 3) until a second Lab adopter or a second maintainer exists. Nothing in option 2 forecloses it.

Residual risk: the toy may show that the Lab's deviations reach doctrine rather than templates, for instance if the lifecycle's `awaiting-decision` state cannot survive a nightly loop with no human present. That would make the split a doctrine change, which is heavier and would need its own External review. The toy's manifest will show this within the first ten cycles, because it is the first thing a nightly loop hits.

## Open questions

* Does `awaiting-decision` have a Lab analogue, or does the journal's accept stand in for it with the Maintainer's sampled audit as the Decision? The concept document assumes the latter; doctrine does not yet say.
* Which of the six existing dimensions apply to a Lab adopter as written, and which need a research reading (complexity in particular: review weight scaled by what?).
* Whether `tools/intent.py` work-intent claims extend to labs claiming a question, which would make the controller's concurrency guard a core tool rather than Lab code.
* Whether the crux fork should expose its engine as a Cairn module (a notebook for any adopter) or stay Lab-only. A Develop adopter might want a question tree for a research-software roadmap; it is not obvious it would.
* The naming: "Cairn Develop" for the software profile reads better than "Cairn Coding" and says what it is; the Maintainer has used both. Settle it in the proposal.

## Fold-up note

This note is itself the fold-back: the scientific-software dimension raised on Cairn's tracker from LHM's strategy note is what the Lab profile would become. When the `profiles-by-slots` proposal opens, the tracker issue should cite it and close on promotion.
