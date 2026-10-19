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

## Review — Codex — 2026-10-19

**Foundations**

1. **Should this happen as framed?** The shared-method direction and adopter-first toy are worthwhile; the claim that the eventual split is chiefly two template edits is not established, because the current doctrine fixes software stages and a human Decision — `doctrine/plans.md:25`, `doctrine/lifecycle.md:168`, and this note's Findings 1–3.
2. **Best alternative.** Keep one repository and distinguish the runtime's Develop workflow from its labs' research workflow; share principles, borrow crux's notebook concepts without committing to its workflow, and extract only the common contracts the toy actually demonstrates — `bootstrap/_scaffold/slotmerge.py:247`, `bootstrap/_scaffold/config.py:1288`, and this note's Options 1, 2, and 4 and crux reuse row.
3. **What would show this wrong?** If a bounded paper cannot proceed through journal acceptance and into the next investigation without a human signature, while instrument changes remain reserved to their owning project's process, the proposed unchanged-core boundary does not deliver the intended autonomy — this note's lines 84, 101–109 and the Lab concept's operative Boundary, Journal, and Audit rows.

**Reviewed commit:** `87607d284f127a22db1d6953094da52045db7969`.
**Attribution and scope:** Codex, Reviewer; not the author of this strategy, but a participant in the preceding Lab concept discussion. This is the usual requested review, not a claimed fresh-context or Security Review. Anthony's clarification is material: “Keep in mind--only I am a Cairn adopter!” The relevant costs are his deployments, attention, and maintenance, not hypothetical outside customers. The review is temporary: the author folds accepted points into the note and removes this section. I have not changed its draft status or any operative recommendation.

Anthony also explicitly reopened crux adoption during this review:

> Go ahead and re-open that decision! That is more of a hypothetical idea. We can build from the concept without adoption.

The strongest version of the idea is one method with two concrete applications, not two products to maintain. Cairn-Develop governs changes to instruments; Cairn-Lab lets persistent labs investigate physical mechanisms and exchange reviewed papers. That could give the existing methodology a useful common purpose. I support the experiment and the one-repository preference. I would revise the proposed boundary before treating Option 2 as the expected result of the toy, and borrow crux's concepts before committing to a fork. No finding here calls for abandoning papers, weakening persistence, or atomizing the scientific process.

### 1. Two workflows must coexist, not replace one another's slots

**Non-blocking strategy finding; resolve in the boundary definition before promotion.** The table treats Develop and Lab as alternative fills of the proposal/plan templates. But the same Cairn-Lab runtime needs both processes. A paper proposing a better physical explanation can be accepted by the journal; a patch changing the controller's permissions must follow the runtime's software-development process. Replacing its software template with a paper template would not supply that second process. Conversely, leaving the installed development templates unchanged says little about how research is governed inside the runtime.

**Evidence:** the source note's lines 12, 48, 59, and 88; the Lab concept's operative *Boundary: developing vs using* row explicitly separates instrument changes from ordinary experiments. The Nov 2 plan repeats the distinction under *What governs the toy*. This is already part of the intended architecture, not new scope from the review.

**Recommendation / satisfier:** distinguish a repository's development configuration from the research protocol it executes. Show where each of four events goes: an ordinary experiment, a submitted paper, a trusted-adapter change, and a controller-permission change. Make their artifact, deciding authority, and durable record explicit. Both workflows may share doctrine and infrastructure without being interchangeable versions of one file. A small mapping is enough at strategy stage; no second installer is implied.

This also changes the proposed falsifier at line 26: zero changes to installed core templates might simply mean the runtime used ordinary Cairn correctly while its research protocol lived elsewhere. A template-difference manifest alone cannot decide whether a common research profile is useful. Record semantic differences in artifact and authority contracts as well as file customizations.

### 2. The current “core” is not already domain-neutral; security overlaps rather than dividing cleanly

**Non-blocking strategy finding; the scope estimate needs correction.** “All 14 files unchanged,” “none ... names a language, a test suite, or a build,” and “the real work is in two files” are stronger than the tree supports. Examples: the runtime contract explicitly declares Python requirements; plans prescribe implementation commits, code-review states, and code review before archive; documentation governance routes rules about building software. The shipped governing file also carries verification-boundary doctrine outside the two artifact templates.

**Evidence at the reviewed commit:** `doctrine/runtime-contract.md:3` and `doctrine/runtime-contract.md:11`; `doctrine/plans.md:25` and `doctrine/plans.md:106`; `doctrine/doc-governance.md:49`; `templates/core/AGENTS.md:206`. These are counterexamples to the classification, not a demand to generalize every paragraph. Python requirements for a shared installer may properly stay shared even though they name a language.

The same issue affects security. `templates/modules/team-gated/security-review.md:4` selects by trust boundary, and its checklist at line 36 covers deserialization, subprocesses, parsing, paths, network I/O, and credentials. Lab controllers and adapters encounter those same classes. Likewise, `templates/modules/default-on/security-verification.md:17` supplies a general evidence-dispatch route, not just a code scanner. Classifying these as Develop-only while Lab redefines security risks gives one maintainer two partially duplicated safety taxonomies. Lab-specific protected evaluation data adds to the common concerns; it does not replace them.

**Recommendation / satisfier:** reclassify by responsibility: shared methodological principle, Develop artifact/stage rule, Lab artifact/stage rule, or common tooling policy. Keep shared trust-boundary rules with profile-specific instances and checks. Extend the scope inventory beyond two templates where the existing text actually binds behavior. The scientific-check section at `templates/core/dev/proposals/_template.md:178` also shows that independent expectations and positive controls already have a Develop analogue; those principles need not be reinvented as uniquely Lab content. This preserves the intended outcomes while correcting where the work lives.

### 3. Borrow crux's notebook concepts first; its workflow is not a demonstrated fit

**Non-blocking strategy finding; revise the “Adopt” and “Now” recommendations.** With adoption reopened, I recommend taking the plain-Markdown question tree, explicit hypotheses and prospective checks, evidence links, and recoverable working summaries as design ideas—not adopting the engine and its agent instructions as the toy's foundation by default. The note establishes a conceptual resemblance, not a lower-cost integration. Its human-approval model conflicts with the Lab's intended delegated work. That is not merely a packaging question to observe after thirty cycles.

**Concrete path:** a lab chooses a hypothesis, prepares a test, runs it, records the outcome, and closes a question. The [upstream crux skill](https://raw.githubusercontent.com/mehdiforoozandeh/crux/main/skills/crux/SKILL.md), in its approval instructions and verb table, requires PI approval for research direction, running experiments, conclusions, and synthesis sign-off. Its [CLI](https://raw.githubusercontent.com/mehdiforoozandeh/crux/main/skills/crux/scaffold/crux.py) exposes distinct approval/answer verbs. These are observed upstream documentation and entry-point definitions, not a tested assertion about an as-yet-unselected fork version. The note names no upstream revision to bind the integration claim.

Keeping every documented approval step human risks stopping each nightly investigation; silently letting the journal call human-signature operations misstates who decided. The notebook's refusal to infer a verdict from logs does not resolve either problem. The current Cairn doctrine similarly assigns proposal acceptance to the Human Maintainer (`doctrine/lifecycle.md:168`). crux does offer real implementation value—IDs, a deterministic evidence roll-up, a notebook structure, and a read-only view—but preserving those benefits while changing the approval semantics still requires a designed integration. A question tree alone also does not demonstrate recovery of a lab's failed approaches, working expertise, and unfinished investigations.

**Recommendation / satisfier:** make a small Lab-owned persistence layer the baseline: durable questions and hypotheses linked to runs and papers, recoverable working state, and explicit actors and authority. Do not recreate the whole crux cockpit or task system to achieve that. Define which actions an approved scope delegates to a lab, which belong to the journal, and which remain Anthony's. Demonstrate one complete question → experiment → paper → journal decision → next-question path without an unplanned human stop, plus a protected boundary-changing action and the Lab concept's interruption/retraction recovery cases. These are proposed acceptance examples, not tests I have run or a waiver of existing approval.

Keep engine reuse as a genuine alternative: a thin adapter around a pinned crux version might save more work than this baseline, and if the Lab-owned layer starts recreating its IDs, validators, and roll-ups, that is reason to reconsider. Choose it on demonstrated fit and avoided maintenance, not on the existence of a matching vocabulary. The cost of the baseline is owning the small state-handling code; the cost avoided is an upstream fork whose central approval behavior must be changed. Neither cost was benchmarked here. Reusing ideas preserves persistence and the paper record; it does not concede those outcomes.

### 4. Existing modules can fill extracted slots; the note has not distinguished that from a new profile mechanism

**Non-blocking strategy finding.** Option 4 is dismissed because modules allegedly cannot replace the templates' software sections. Existing modules cannot overwrite arbitrary populated sections, but neither does Option 2 achieve that merely by calling its fills profiles. Both require extracting the mixed prose into suitable boundaries. After that extraction, module-into-empty-slot composition already exists.

**Probe on the reviewed commit's code, Python 3.13.13:** evaluated the pure `resolve_slot_merge` function and its direct helpers from `bootstrap/_scaffold/slotmerge.py` in memory. An empty named slot plus proposed Lab text returned `inserted`; a populated slot with differing text returned `conflict`; a missing slot returned `missing-slot`. Positive and negative controls therefore distinguish composition from arbitrary replacement. This was not an install or upgrade test. Source: `bootstrap/_scaffold/slotmerge.py:247`.

Meanwhile, the current configuration recognizer has a closed six-axis schema and structural-key vocabulary (`bootstrap/_scaffold/config.py:1274` and `bootstrap/_scaffold/config.py:1288`). Evidence-kind or persistence axes, arbitrary profile fill sets, and profile identity are new configuration decisions, not already delivered by naming directories. A persistence-depth setting must also respect the Lab concept's non-negotiable continuity requirement; it cannot make an ephemeral lab a valid configuration by accident.

**Recommendation / satisfier:** distinguish two choices: extracting shared rules and naming Develop/Lab, versus adding a new install-time composition/schema mechanism. Compare a named preset/module bundle using the existing machinery with the proposed richer profile representation, and name the concrete behavior that requires the latter. For Anthony's own deployments there is no need to solve outside-customer migration or a public profile ecosystem first. If existing composition suffices, the names and shared methodology still survive; what is forgone is additional configuration machinery, not the Lab's scientific capability. Keep both options live until that behavior is identified.

### 5. The cited count checker checks none of this note's numbers

**Non-blocking evidence correction.** Line 24 names `verify_counts.py` as the discipline behind the inventory. That checker processes registered `verify` annotations, not unmarked numbers or general prose. The note has no such annotations. At the reviewed commit there are 15 Markdown files under doctrine including its README; if 14 means the substantive files excluding that index, state the inclusion rule. No denominator or classification measurement backs the three-fifths estimate.

**Probe, Python 3.13.13:** loaded the reviewed commit's `parse_annotations` function and regex definitions from `scripts/verify_counts.py` in memory; the complete committed strategy produced `[]`. A known-positive line containing 14 and a valid-shaped verification annotation produced one parsed entry. `git ls-tree --name-only 87607d28:doctrine` counted 15 Markdown paths. The scanner's behavior is visible at `scripts/verify_counts.py:104` and `scripts/verify_counts.py:215`: no annotation means no measurement. I did not run a broad suite or treat zero checked entries as verification.

**Recommendation / satisfier:** either attach the appropriate registered measurements or give dated snapshot commands with explicit inclusion rules. Correct the inventory and drop the three-fifths figure unless it helps a decision and has a reproducible denominator. This is a small evidence repair, not a reason to hold up the research toy.

### Recommendation and coverage

Retain the Lab toy and the one-repository direction; replace presumed crux adoption with concept reuse and a fit-dependent engine choice. Name Cairn-Develop and Cairn-Lab now if that improves Anthony's mental model; neither naming nor personal usefulness requires a second adopter. Revise the strategy around shared principles plus two coexisting protocols, and let the toy reveal the smallest composition machinery needed. Thirty completed cycles are an opportunity to make that judgment, not an automatic instruction to ship a predetermined profile design. The recommendation retains persistent labs, papers, and scientific exploration; it changes the notebook implementation recommendation under Anthony's express reopening, rather than silently conceding an accepted outcome. The author and Maintainer decide the disposition.

**Covered:** claims and drift—committed doctrine/template counterexamples and the count-parser probe above; design completeness and lifecycle placement—the four-event authority mapping and crux approval path; silent-failure risk—the zero-annotation control and explicit empty/occupied/missing-slot results; cross-document consistency—the Lab concept's operative table and Nov 2 plan; scientific scope—the distinction between developing instruments and judging papers, retaining end-to-end persistent labs and reviewed papers; satisfiers—each finding names its closing clarification, corrected measurement, or integration example. Local Lab context was read outside git: *Cairn Lab - Concept and Scope.md*, SHA-256 `2dcbaa1e257ff78691ea935c31fb2062752ee05abd21bfcdc1a7c74e1204b03e`, and *Cairn Lab - Nov 2 Plan.md*, SHA-256 `4668841c111705b46bce6fed6803fdd4cebb8a1c49b5b9ed34047483a310cf0f`.

**Not covered / low confidence:** no production Lab runtime, selected crux fork, install/upgrade composition, or LHM execution was exercised; no code-review clearance or Security Review is claimed. The remaining research precedent survey, LHM sibling proposal, detailed resource estimates, and exhaustive file-by-file sorting were not audited. Upstream crux was inspected as unpinned documentation/source accessed on 2026-10-19, not evidence about a selected release. No full suite ran for this prose-only review. No test reader of this artifact was identified by committed-tree searches for its name, strategy paths, or Markdown glob loops (positive control: the search finds known runtime-contract references); the inspected general globs concern shipped or generated templates, not this strategy note. Document-scoped claim, local-link, and snippet checks passed with Python 3.13.13; the two new external sources were opened separately. The neutrality scanner excludes the deliberation tree. Other sessions' working changes were not reviewed or edited.

## Review — Antigravity — 2026-10-19

**Foundations**

1. **Should this happen as framed?** No: forcing the synthetic research ecosystem into Cairn as a slot-merged template profile (Option 2) would churn a mature, slow-moving software methodology (`AGENTS.md:9`, `dimensions/README.md:23`, `tools/board.py:102`) to house an executable nightly research runtime that shares Cairn's epistemic principles but almost none of its mechanical state machine.
2. **Best alternative.** Keep Cairn untouched (Option 1) as the software methodology, build the research ecosystem as a separate project (`assai`) whose labs and journal use Cairn's session and review disciplines internally, and adopt `crux`'s stdlib engine (`ENGINE_VERSION = "3.5"`) as each lab's notebook with its signature verbs bound to the Journal/Controller — `AGENTS.md:9`, `templates/core/dev/proposals/_template.md:178`, and upstream `skills/crux/scaffold/engine.py`.
3. **What would show this wrong?** If an `assai` ecosystem needed `bootstrap/scaffold.py` to slot-merge research papers into `templates/core/dev/proposals/_template.md`, or if `crux`'s CLI blocked unattended runs even when its approval verbs are invoked by the Journal/Controller rather than a human in chat — this note's lines 58–60, 71, and 92–105.

**Reviewed commit:** `b69a988743dc15f155111c4c66f05868d84c8bad`.
**Attribution and scope:** Antigravity (Gemini), Reviewer; a third agent type reading the strategy note, Codex's review, the local `AI_Lab_Ecosystem` documents, and upstream `crux` source (`README.md`, `SKILL.md`, `crux.py`, and `engine.py`). Per `dev/strategy/_template.md:43-53`, this review section is temporary: the author folds accepted points into the note and deletes the review section.

### 1. Keep Cairn untouched and build `assai` as a separate project — the shared core is epistemic, not mechanical

**Strategy finding; recommends Option 1 (separate `assai` project) over Option 2 (slot-merged profiles).** Cairn is already mature across `LHM`, `modflow_tools`, and `cairn` itself, and will change slowly. Its identity is stated at `AGENTS.md:9` (*"Cairn is a methodology, not software"*), and its mechanical surfaces — `tools/board.py:102` walking `dev/proposals` and `dev/plans`, `dimensions/README.md:23` scoring codebase axes (`age`, `size`, `complexity`, `language`), and `templates/core/AGENTS.md:206` defining software verification boundaries A, B, and C — are built for human-reviewed code changes.

By contrast, the research ecosystem (`assai`) is **software**: an unattended nightly runtime with a controller, container sandboxes, held-out observation scoring, planted-error schedules, a structured `claims.json` graph, a replicator (`reproduce(bundle)`), and model harnesses (`LHM-MODFLOW`). Pretending a research paper (`question → method → result → claims.json → pre-registered next test`) is a slot-filled variant of `templates/core/dev/proposals/_template.md` (lines 48, 58–60) forces artificial template surgery on Cairn and conflates two peer worlds that are actually connected by a clean handoff bridge:

* **How `assai` uses Cairn internally:**
  1. *Developing the `assai` runtime:* `assai` (the Python repository) is a standard Cairn adopter, which automatically installs `claim_check.py`, `content_scan.py`, `link_check.py`, `intent.py`, and `session.py` for developing its controller and harnesses.
  2. *Inside each `assai` lab and the journal:* labs use Cairn's `session-start` / `goodnight` continuity discipline, pre-registration principles (`templates/core/dev/proposals/_template.md:178`), and citation checks; the journal and peer reviewers use Cairn's append-only review cycle and three-question `Foundations` review stance, with the replicator supplying Boundary C falsification (`reproduce(bundle)`).
* **How `assai` hands findings back to software repos (`LHM` / `modflow_tools`):** when an `assai` lab diagnoses a model defect (such as the Cedar Creek lake-ice condensation bug) or validates a missing process in a methods paper, that paper crosses over to `LHM` as the `Context` of a Cairn software proposal. Once `LHM` ships the change under Cairn, `assai` adopts the new model version via `APPROVALS.md`.

**Recommendation / satisfier:** reframe the strategy around keeping Cairn as Cairn (no "Cairn Develop" rename required across existing repos, and no `profiles-by-slots` refactor of `proposals/_template.md` or `plans/_template.md`) and naming the synthetic research ecosystem **`assai`** (`MSUHydrogeology/assai`). What the two projects share is the Cairn epistemic architecture — append-only git provenance, independent review by a separate agent/vendor, falsification with positive controls (`S1–S5` and `Independent scientific check`), and human authority at the boundary — without forcing them into one template tree.

### 2. Adopt `crux`'s engine (`engine.py` v3.5) for the `assai` labs — it already enforces pre-registration hashing and positive controls

**Strategy finding; supports the author's `crux` adoption recommendation against Review 1's Finding 3, with concrete evidence from `engine.py`.** Direct inspection of upstream [`crux.py`](https://raw.githubusercontent.com/mehdiforoozandeh/crux/main/skills/crux/scaffold/crux.py) and [`engine.py`](https://raw.githubusercontent.com/mehdiforoozandeh/crux/main/skills/crux/scaffold/engine.py) (`ENGINE_VERSION = "3.5"`, `CRUX_VERSION = "0.9.0"`, 2,667 lines of third-party-free stdlib Python) shows that `crux` already implements mechanical safeguards that a newly written "small Lab-owned persistence layer" would otherwise have to reinvent before Nov 2:

* **Content-hashed pre-registration lock (`lock_material`, `lock_hash`, `lock_drift`, `take_lock` in `engine.py`):** without a pre-run lock, a lab agent running unattended at 2 a.m. can quietly edit its notebook's pass/fail bar after seeing the model output, and `reproduce(bundle)` will still pass. In `crux` v1.9+, transitioning a hypothesis to `running` (`crux test <hid> --to running`) content-hashes the verifiables, their kinds, and the combination rule into the node's frontmatter; any later edit is permanently flagged by `lock_drift()`. (As an additional belt-and-suspenders check, the `assai` controller can record that node hash inside its protected run certificate when `run(scenario, out_dir)` starts.)
* **Mandatory outcome-neutral positive controls (`verifiable_kind`, `neutral_gap`, `derive_verdict_15` in `engine.py`):** every verifiable is typed `[hypothesis]` or `[outcome-neutral]` (`-n` / `--neutral` in `crux.py`). At least one outcome-neutral positive control is required before `test --to running`, and if the control fails, the engine derives **`invalid-run`** rather than **`refuted`** (*"without a passing control, 'the claim is false' and 'the apparatus is broken' are the same picture"*).
* **Null confounds and discriminating checks (`null_problem`, `scenario_gap`, `--null`, `--fails-if`, `--discriminates`):** before a run launches, the hypothesis must state a `--null` confound, each check must state `--fails-if` (exposing redundant checks), and at least one check must carry `--discriminates` against the null.
* **Deterministic verdict arithmetic (`--rule all | any | m-of-n`), sibling attempt lineage (`builds_on:` avoiding deep tree nesting on repeated attempts), bounded context assembly (`crux brief --mode=situate` for cold-start interruption recovery), and OpenAlex literature ingestion (`cmd_ingest`, `.sources.tsv` with SHA-256 digests).**

**Why `crux`'s approval gates (`◆`) are an asset, not a blocker:** Review 1's Finding 3 objected that `crux` requires human PI sign-off on `approve-null`, `task accept`, `approve`, and `answer`. In `crux`'s architecture, `crux.py` is a stateless CLI where every verb supports `--json`; the prohibition against self-approval lives in `SKILL.md` (the agent instructions), while `engine.py` simply enforces that the state transition occurred. In a multi-agent `assai` ecosystem, you do not strip those gates out — you **bind `crux`'s `◆` verbs to `assai`'s independent roles**:

1. **Lab agent:** permitted to run `ask`, `hypothesize`, `synthesize`, `task add`, `brief`, and `status`; barred by the controller from invoking `approve-null`, `task accept`, `approve`, or `answer`.
2. **Stage-1 gate (`approve-null`):** a lightweight Critic / Journal Stage-1 check inspects the lab's `--null`, `--neutral` control, and `--discriminates` check, then runs `crux approve-null <hid>` so `crux test <hid> --to running` can lock and launch.
3. **Stage-2 gate (`task accept` / `approve` / `answer`):** when a completed experiment or synthesis is submitted as a paper, the Journal + Replicator runs `reproduce(bundle)` and Cairn review, then invokes `crux task accept` / `crux approve` (with Maintainer audits governing high-level question closure or retraction).

**Recommendation / satisfier:** keep the `crux` fork decision (pinned to a specific commit/release of `engine.py` v3.5 under Develop's fork rules), update line 71's table row to name `engine.py`'s hash-locking (`take_lock`/`lock_drift`), `[outcome-neutral]` positive controls (`invalid-run`), and `--null`/`--discriminates` checks, and specify the Lab-vs.-Journal role binding for `crux`'s approval verbs.

### 3. Resolve Open Question 1 (`awaiting-decision`) by separating Nightly Editorial Publication from Human Promotion

**Strategy clarification on lines 105 and 109.** In Cairn's software lifecycle (`doctrine/lifecycle.md:168`, `tools/board.py:55`), `awaiting-decision` blocks on the Human Maintainer. In `assai`, requiring a human signature every night halts the loop, while calling the Journal's acceptance a Maintainer `Decision` blurs Cairn's human-verdict rule (line 84).

The clean mapping separates **working publication** from **epistemic or instrument promotion**:

* **Journal Acceptance is Boundary B/C Verification, not a Maintainer Decision:** when the Journal and Replicator accept a paper, its claims enter the store as `reproduced` (or `exploratory`). Other labs can build on `reproduced` claims immediately on the next night's cycle because uncertainty propagates mechanically along `requires` edges in `claims.json`.
* **The Human Maintainer's `Decision` sits at three promotion/retraction gates:**
  1. *Instrument and reference-set adoption* (`APPROVALS.md`), after the controller scores a frozen candidate once on held-out observations;
  2. *Weekly sampled and high-fan-out audits*, which either validate a claim chain or trigger a cascading retraction across `requires` (plus regenerating lab working summaries);
  3. *Lab-to-code escalation*, deciding that an `assai` lead brief warrants opening a Cairn proposal in `LHM` or `modflow_tools`.

### Coverage

**Covered:** `dev/strategy/2026-10-19-claude-core-and-two-profiles.md` and its appended Codex review; `AGENTS.md:9`, `doctrine/lifecycle.md:168`, `dimensions/README.md:23`, `templates/core/dev/proposals/_template.md:178`, `tools/board.py:55` and `tools/board.py:102`; the local `AI_Lab_Ecosystem` files (*Cairn Lab - Concept and Scope.md*, *Cairn Lab - Nov 2 Plan.md*, *Cairn Develop - Lobby Board v1.html*, and *Cairn Lab - Lobby Display v1.html*); and upstream `crux` (`README.md`, `skills/crux/SKILL.md`, `skills/crux/scaffold/crux.py`, and `skills/crux/scaffold/engine.py` at `ENGINE_VERSION = "3.5"` / `CRUX_VERSION = "0.9.0"`).

**Not covered:** no `assai` runtime or `LHM` harness code was executed, and upstream `crux`'s `selftest.py` / `cockpit` were not run locally. This is a prose-only strategy review; `python scripts/claim_check.py dev/strategy/2026-10-19-claude-core-and-two-profiles.md` was run to verify local path and line citations.

