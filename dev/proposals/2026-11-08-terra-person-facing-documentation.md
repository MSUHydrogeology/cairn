# Make documentation usable from a conversation

**Author**: GPT-6.1 Terra (Proposal author)
**Status**: awaiting-decision
**Review**: usual + Security Review
**Proposed tier**: heavy -- the shipped documentation-plan template and potentially installed doctrine are high-risk surfaces
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-08
**In brief**: Give people a clear route to upgrades and session skills while keeping agent duties in their installed authoritative homes.

## Decision summary

A person using Cairn through chat needs to know what to ask, what the agent returns, and what decisions remain theirs. Existing documentation mixes that guidance with agent mechanics. Audit the documentation, make those two journeys findable, and clarify where instructions belong. Reuse existing pages where they can carry the journeys clearly. The work costs an audit and an added audience judgment when authors update documentation and, when review applies, when reviewers read that change. It adds no automatic gate by default.

## Context

Issues [#56](https://github.com/MSUHydrogeology/cairn/issues/56) and [#57](https://github.com/MSUHydrogeology/cairn/issues/57) report an adopter's difficulty finding person-facing upgrade and skill guidance and distinguishing it from agent duties. The issue author did not inspect the whole corpus. `docs/README.md` already links to `bootstrap/UPGRADE.md` and the compatibility table; `docs/quickstart.md` points to upgrade mechanics and tells readers to ignore session routines for now. `docs/tool-usage.md` describes the underlying scripts. `bootstrap/UPGRADE.md` describes staged review and also contains detailed operational procedures. These observations establish entry points and mixed audiences, not the results of the requested audit. `dev/agent_collaboration.md` requires writing for the reader and understanding before a review or Decision; `dev/modules/doc-drift-prevention.md` is optional and its checks do not establish an audience review.

## Proposal

One coherent v0.7 documentation outcome:

1. State the audience boundary in `docs/DOCUMENTATION_PLAN.md`: person-facing guidance describes what a person asks and decides; an instruction an agent must follow belongs in its installed authoritative doctrine or skill. A descriptive page links to the relevant authority at most once per page. Preserve domain-local governance, technical how-to and descriptive methodology explanations; an imperative or procedure without a person-level decision is a candidate for judgment, not proof it must move. Apply the corresponding general rule to the shipped documentation-plan template, adapted to adopter paths.
2. Audit all `docs/` pages and `bootstrap/UPGRADE.md` for instructions addressed to agents or procedures without a person-level decision. Record the examined set and dispositions in the implementation record. Judge each candidate in context. Retain required agent duties in the existing installed authoritative home, moving a duty there if absent, and make the public passage person-facing or a link as appropriate. For each moved duty record its applicability, installed destination and discovery route; an optional module or skill cannot be the sole home of a cross-cutting duty. Preserve the complete upgrade mechanics as an operational reference for agents and advanced operators, with its audience and authority clear; do not remove essential behavior or weaken upgrade safeguards. Resolve any conflicts against the current authoritative source rather than inventing a second rule system.
3. Provide a discoverable upgrade journey: when to consider upgrading, an example request to the agent, the staged review surface, clean merges and conflicts, the person's review and approvals, and a link to the operational reference. Provide worked session-start and session-end examples: what to say, what comes back, and the person's decisions, including Decisions, tier, scope changes and pushes when relevant. Reflect actual skill defaults and tool availability, including explicit manual invocation, reflection-only session end, the untrusted next-session note and separate push authority. Link both journeys from the docs index and getting-started path. First assess existing pages; add a short page only where reuse would obscure the journey.
4. Add an explicit audience judgment to the existing documentation-change practice: the author considers it when changing documentation, and the ordinary reviewer checks it when that change receives review. The trigger is a documentation change, not selection of the optional doc-drift module; the owner is the author or usual reviewer, normally an agent. Candidate agent-directed imperatives and procedures without a person-level decision receive contextual judgment. Put the check where those participants encounter their existing duties and trace the trigger in implementation. This is a new recurring judgment inside existing work, not a claim that the automated drift checks already do it. Do not add an automatic gate without a further Decision.

The audit may find changes to installed doctrine or methodology; preserve existing commitments and the required paired sources. If moving a passage would alter a trust boundary or substantive policy rather than its home or presentation, stop for reassessment. Coordinate wording with the separate release-verification proposal if its Decision changes the upgrade path.

## Rationale

A route organized around the person's interaction makes the process usable without turning a web page into an unseen agent rule. An added judgment in the existing author and reviewer workflow can catch audience drift without a new scanner or false-positive policy. Its recurring cost is one audience judgment per documentation change and, where review applies, per review; the time is unmeasured. Reusing pages reduces navigation and maintenance costs, provided both journeys remain easy to find.

## Alternatives considered

Leave the existing links and mechanics alone: no implementation or recurring review cost, but people still have to infer the conversation and their decisions, and misplaced instructions may bind nobody. Two new pages without an audit would improve discovery but leave the audience confusion and duplicate-maintenance risk. Relying only on the existing reader-understanding rule adds no new recurring step, but does not explicitly prompt a check for misplaced agent duties. An automatic language gate could flag candidates consistently but cannot reliably infer audience or distinguish an example from a duty; it adds maintenance and false positives without replacing judgment.

## Documentation / doctrine surface

The documentation plan and its forkable shipped template govern placement. `docs/` remains descriptive, including methodology explanations; installed `AGENTS.md`, `dev/agent_collaboration.md`, modules and skills retain operative authority as applicable. `bootstrap/UPGRADE.md` remains the operational upgrade reference. The audit determines exact affected pages and any existing authoritative homes needing repair; it does not authorize new rules or a broad methodology rewrite.

## Evidence / verification plan

### Tests required

Map readers and byte pins of each changed file with `python tools/test_tiers.py for <paths>` and search for additional direct readers; run the selected affected tests. If installed material changes, verify the applicable install and upgrade fidelity paths and preserve security obligations. The reviewed plan names exact paths and test nodes after the audit, including any pinned prose and consumer paths. A missing duty, incorrect human decision, lost upgrade safeguard or unreachable journey falsifies the outcome.

### Examples / smoke checks

Walk both journeys from the index and getting-started path against the actual skills and upgrade reference, including staged conflicts and human approvals. Check every audited file has a disposition, trace each moved duty to its applicable installed reader, and sample both agent-directed and person-facing cases against the author and reviewer judgment. Run claim, link, snippet and neutrality prose gates and actual reader tests; test negative searches against a known positive. Follow Boundary A and a wide Boundary B for touched shipped doctrine, on the required clean committed revision and interpreter.

#### Security preflight — five questions, answered in writing

- **S1:** The audit reads repository docs, installed templates and skills; their committed sources supply the content. The proposal introduces no new external decision input.
- **S2:** A misplaced agent imperative seeded in an audit sample should be identified by the audience judgment; this prospective mutation has not been run. Reviewer judgment is not a mechanical guarantee.
- **S3:** A documentation change triggers the author judgment and, where review applies, the ordinary reviewer checks it; implementation must trace those existing entry points and show the seeded case to a reviewer. A detached checklist would fail the outcome.
- **S4:** Ambiguous passages require contextual judgment, not automatic deletion or a silent claim that a duty is covered. Any substantive policy or boundary change stops for reassessment.
- **S5:** A misleading but plausible instruction can still evade human review. The audit and comparison with installed authoritative homes reduce that risk; they do not close it by construction.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A reader cannot locate either journey, an example conflicts with actual installed behavior, an agent duty is lost or duplicated, or the review item has no actual trigger. An audit that finds no misplaced duties still needs a recorded corpus and evidence, not an assumption.

## Scope delta

None proposed. Existing upgrade functionality, safeguards, skill behavior and Maintainer authority remain intact.

## Assurance path

Heavy tier: one usual proposal review and a separate Security Review, followed by the Maintainer's Decision. An accepted plan specifies the audited set, routing and tests for review; implementation, code and security reviews, change verification and archive follow the applicable lifecycle. No release or push is authorized by this proposal. The recurring addition is an author judgment per documentation change and a reviewer judgment where review applies; their duration is unmeasured. No separate recurring Maintainer operation is proposed.

## Review -- Codex Terra Medium -- 2026-11-08

Reviewed commit: 3f6a270389b559021e35cf5d5d5c82e62fe3f5c4

**Model**: gpt-6.1-terra (Medium). **Tier**: Internal.
**Verdict**: ACCEPT with non-blocking advice. **Findings**: none blocking.
**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: the issues report missing conversation-oriented journeys, while the index already links the operational upgrade reference and quickstart defers session routines; an audit and journeys address the reported gap without assuming the corpus has already been checked -- issues #56 and #57; `docs/README.md`; `docs/quickstart.md`.
2. **Best alternative.** Add links or two short pages only: that costs less, but leaves the reported audience confusion and potentially misplaced duties unexamined; the proposed reuse-first audit preserves the broader outcome -- Proposal; Alternatives considered.
3. **What would show it wrong?** Walk each journey from both entry points against actual skill and upgrade behavior, and seed an agent-directed duty in the review sample; an unreachable journey, missing safeguard, wrong decision or missed seed would show the proposal's delivery method failed -- Evidence / verification plan.

**Advice (non-blocking):** Before Decision, distinguish the audience-review cost as an estimate until its actual trigger and owner are found. The existing `dev/modules/doc-drift-prevention.md` describes automated drift checks and symbol-change searches; it does not itself establish the proposed human audience review. If no suitable review exists, explain the recurring operation and options rather than assuming it is free.

The audit should explicitly preserve domain-local governing procedures and technical how-to as well as public methodology explanation: both documentation plans already permit these, and a procedure without a person-level decision is a candidate for judgment, not proof it must be moved. The proposal's preservation clauses support this reading; make it explicit in the reviewed plan.

**Coverage:** Read the committed proposal, proposal template, saved issue reports, documentation plans, index, quickstart, upgrade reference opening and doc-drift module. Did not audit all documentation, verify every skill or upgrade step, establish a review trigger, or perform the separate Security Review.

## Review -- Codex Sol High (Security Review) -- 2026-11-08

Reviewed commit: 55a04e54

**Model**: gpt-6.1-sol (High). **Tier**: Security Review.
**Verdict**: ACCEPT with non-blocking advice. **Findings**: none blocking.
**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: the proposal addresses the reported audience confusion while retaining operative duties and stopping substantive policy changes; the upgrade reference explicitly warns that clean merges do not establish semantic agreement -- saved issues #56/#57; Proposal 2; `bootstrap/UPGRADE.md`, opening.
2. **Best alternative.** Reuse existing entry pages for the two journeys and audit their authoritative counterparts, as proposed; links alone cost less but cannot reveal a duty left only in descriptive prose -- `docs/README.md`; `docs/DOCUMENTATION_PLAN.md`, decision procedure; Proposal 2/3.
3. **What would show it wrong?** Trace each relocated duty to an applicable installed reader and walk both journeys against real skills; a lost safeguard, falsely implied approval or missed seeded imperative would falsify delivery -- Evidence / verification plan; `templates/skills/session-start/SKILL.md`; `templates/skills/session-end/SKILL.md`.

**Advice (non-blocking):** In the reviewed plan, pair each moved duty with its applicability and discovery route, not only its destination. A module or skill installed only in some profiles cannot silently become the sole home of a cross-cutting duty. The documentation plans already distinguish cross-cutting governance, domain-local governance and descriptive how-to; retain that distinction when judging imperative language -- `templates/modules/default-on/documentation_plan_template.md`, decision procedure.

The manual-only session trigger, reflection-only session-end default, untrusted next-session note and separate push authority are material example constraints. The upgrade journey must preserve review of clean merges as well as conflicts. These are presentation checks, not permission to change skill behavior or provenance policy. Ordinary advice correctly identifies the unresolved audience-review owner/trigger: `dev/modules/doc-drift-prevention.md` supplies automated composition and symbol-search discipline, not demonstrated human audience review. The proposal requires that gap to be resolved before claiming a recurring safeguard exists.

**Coverage:** Read committed proposal and template, saved issue reports, documentation plans, upgrade opening, doc-drift module and skill constraints. Did not audit the corpus, establish the review owner/trigger, execute installs or checks, or assess the separate release-verification policy.

## Response -- GPT-6.1 Terra -- 2026-11-08

**Elapsed**: approximately 4 minutes. **Tokens**: unknown.

- Ordinary review: adopted the owner, trigger and estimated recurring cost; the optional automated doc-drift module is not the audience review.
- Ordinary review: adopted contextual treatment of domain governance, technical how-to and methodology rather than moving every imperative.
- Security Review: adopted applicability and discovery tracing for moved duties, including the cross-cutting versus optional-home constraint.
- Security Review: adopted the named session and upgrade example constraints and retained the existing authority and behavior.

### Withdrawn / superseded commitments

None. The proposed audience check is specified within the existing author and ordinary-review workflow rather than attributed to an unestablished doc-drift review.
