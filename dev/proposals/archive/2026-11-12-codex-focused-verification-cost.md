# Focus verification on delivered promises and integrate at arc end

**Author**: Codex GPT-6.1 Sol (Strategy, High)
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: heavy — governing methodology and shipped templates change
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-12
**In brief**: Check the outcomes people rely on as each plan finishes, then join related work in one integration run at the end of the development arc.

## Decision summary

Deliver this guidance in v0.7, before the release cut. For each plan, test changed public promises, dispose of findings and archive. Run integration at the end of the connected arc, or at a named critical boundary. Reviewers may use committed code and existing evidence when sufficient, reserving a fresh probe for a specific uncertainty. This replaces per-plan integration and exhaustive mutation instructions in the eight existing governing, shipped and public text files. A cross-plan interaction may first appear at the joined run; a failed promise still holds its plan open.

## Context

The Maintainer's 2026-11-12 focused loop is in `dev/PLANNING.md`; on 2026-11-13 they asked to consider v0.7 delivery and compare its cost with v0.8. Current doctrine favors public entry points and Pareto selection yet requires integration after every implementation and a fresh probe for every review claim. `docs/methodology/dual-review.md` requires per-member mutations for universal claims. Templates repeat these demands. The archived testing strategy (`dev/strategy/archive/2026-10-27-antigravity-judicious-testing-and-simulation-verification.md`) records test growth from 5,913 at v0.6.1 to 7,165 on 2026-11-10 and repeated burden across two workstreams; it supplies recurrence for doctrine review, not measured savings from this proposal. Issue #61 describes another project, not a Cairn benchmark.

## Proposal

**Selection during a plan.** In existing plan Verification, name changed caller-visible promises, their public entry points and outputs, and the smallest checks that could catch plausible faults. Group equivalent paths. Reuse a result when its tested bytes, platform, input and obligation still apply; cite its source and limit. A changed boundary, failed check, uncovered fault or explicit requirement expands selection. A claim about *every* member inventories the set and checks each applicable path, without a separate mutant for each. Temporary development probes leave before archive; permanent tests guard external promises. An import, help display or private-helper result cannot replace an output check. A plan template example will show one changed output, reused control and joined run.

**Review and evidence.** Reviewers still try to falsify the change. Evidence may be committed bytes, an existing result, static calculation or focused run, chosen for the uncertainty. Forward behavior needs executable evidence before completion; forward structure can be checked on committed structure. An unestablished required outcome stays open. Remove the blanket scratch-attempt and per-member mutation instructions. Mutation remains optional unless accepted security, scientific or component requirements call for it. Security preflight S2 should accept a valid existing negative control; a new security check needs a demonstrated failing case. Work touching a scientific assumption or a result the project publishes or acts on retains its independent error and positive controls, even when intended output is unchanged.

**Integration point.** Replace per-plan Boundary B with one selected run after connected plans' reviews and dispositions, under the applicable canonical runtime and standing gates. An earlier run needs a named critical shared boundary. The arc owner records revision, selected producers and consumers, results and omissions in the existing verification record. At arc close, the joined evidence must cover the clean final combined revision before arc completion or release. Run affected interactions on that state; carry forward prior results whose tested behavior and inputs remain unchanged, rather than replaying the whole selection solely for a new commit ID. After a repair, rerun only affected integration checks. If integration finds a defect in an archived plan's work, the arc owner coordinates its repair under existing defect and review rules, records the resolution in the existing verification record, and leaves the archived plan closed. Known failed promises, required security checks and accepted criteria remain plan work before archive. Release certification and human trust operations keep their triggers.

**Release recommendation.** Apply the eight-file consistency repair before the v0.7 cut if accepted. Existing v0.7 coordination already covers handoffs, parallel owners, dispositions and finishing records; no new coordination rule is proposed.

## Rationale

The current file selector and public-promise rule do not resolve conflicting probe and integration instructions. One joined run tests interactions after dependent work exists. Once-per-commit baselines, test budgets and a cost ledger would add ceremony without demonstrated benefit. Existing timing, token and defect records can reveal savings or late repair cost. Related selected nodes may share a runner session when isolated results remain clear; timing targets stay diagnostic.

**Cost of timing, estimates:** now **4.5–8 agent-hours, 2–5 elapsed hours**; later **4–9 agent-hours, 2–5 elapsed hours once started**. The ranges overlap. Assumptions and release-packet cost appear in the scheduling revision below; token and dollar costs are unknown.

## Alternatives considered

Simply enforce Pareto selection: leaves conflicting integration and mutation demands. Run a suite after every plan: repeats unchanged checks before dependent work exists. Add a test budget or stop-and-ask gate: rewards omissions and moves routine selection to the Maintainer.

## Documentation / doctrine surface

The governing changes belong in `dev/agent_collaboration.md` and its shipped `templates/core/dev/agent_collaboration.md`; the published explanation belongs in `docs/methodology/plans.md` and `docs/methodology/dual-review.md`. The operative examples and security-preflight wording belong in `dev/plans/_template.md`, `templates/core/dev/plans/_template.md`, `dev/proposals/_template.md` and `templates/core/dev/proposals/_template.md`. `AGENTS.md` keeps its short routing rule. No software behavior, test runner or coordination instruction is proposed.

## Evidence / verification plan

### Tests required

No product behavior or test changes. Identify readers and pins, then select changed-guidance checks and prose gates; the mapper's owner list is not a replay requirement. A retained per-plan integration or universal mutation rule, or permission to skip an accepted check, would falsify the change. No full suite solely for prose scheduling; failed required checks remain open.

### Examples / smoke checks

Run claim, link, snippet and neutrality prose gates. Check the example against an accepted outcome and compare shipped with self-hosted copies. For v0.7, refresh the packet's exact-candidate binding and affected reads; preserve Maintainer baseline and release steps. Compare later arcs using existing time, token and defect records, reporting gaps as unknown.

#### Security preflight — five questions, answered in writing

S1: This proposal changes evidence-selection instructions, not a software admission decision; inputs are accepted plan obligations, committed code and existing results. S2: A weakened safety check would be exposed by comparing each edited instruction with its existing required trigger and a known failing control; no new executable check is proposed. S3: Existing plan review, code review, file-specific verification and joined integration fire at their named lifecycle points; the plan must trace their actual commands and selected paths. S4: Missing or failed required evidence leaves implementation open, never silently passes it. S5: A contributor could still misstate a result; independent review and the existing evidence record remain the control, not a new attestation mechanism.

### Independent scientific check

N/A: this proposal touches no scientific assumption or result. Future work touching an assumption or a published or acted-on result still owes its independent check and positive control, even if the intended result is unchanged.

## Signals the change is wrong

Reviewers cannot tell which changed promise was checked; previously required refusals or scientific controls disappear; the joined run regularly finds defects that a named earlier public check would have caught; or elapsed/token records show no savings while late repair burden grows.

## Scope delta

**Scope delta**: preserved. This proposal changes verification timing and evidence granularity; it removes no accepted outcome, public promise, independent review, security check, scientific check or release operation.

## Assurance path

**Assurance path**: high-assurance. Governing methodology and shipped authoring templates require ordinary and Security proposal review, a reviewed plan, affected prose checks and the existing protected-surface procedure.

## Security Review -- Codex GPT-6 Sol -- 2026-11-12

**Tier**: Security Review
**Reviewed commit**: `02f051cd`
**Verdict**: REVISE

The proposal's strongest case is that plan-specific public-output checks can finish each plan, while one later run tests the combined arc. It keeps named security, scientific and release obligations; I found two gaps in how those obligations reach completion.

**Foundations — Should this happen as framed?** Yes, with the final-revision and scientific-trigger fixes below; the proposal's Selection and Integration point retain changed promises and required checks, while `dev/PLANNING.md`'s v0.8 focused-checks row authorizes arc-end integration.
**Foundations — Best alternative?** Keep the proposed loop and add two sentences at its existing integration and scientific rules, rather than restoring per-plan integration; `dev/agent_collaboration.md` > Verification and `dev/proposals/_template.md` > Independent scientific check establish those obligations.
**Foundations — What would show it wrong?** In a later arc, compare the joined run's tested revision with the final combined revision and trace every changed scientific assumption or result to its independent error and positive controls; an untested final revision or missing control falsifies the design (`dev/proposals/_template.md` > Independent scientific check; proposal > Signals the change is wrong).

**Blocking finding 1 — Final integrated state.** “Later changes need focused correction checks and eventual inclusion” permits archive or release before the final combined revision receives the joined run. The current Boundary B runs after code-review fixes on a clean final commit (`dev/agent_collaboration.md` > Verification). Require the arc's joined selection to cover the final combined revision before arc completion or release, with affected integration checks repeated after later changes. Say where a failure discovered after a source plan's archive is owned and fixed; it cannot retroactively hold an archived plan open. This closes the gap without a new record or stage.

**Blocking finding 2 — Scientific trigger.** “Changed scientific assumptions or results” is narrower than the current trigger for a change that *touches* an assumption or a published/acted-on result, even if the intended output is identical (`dev/proposals/_template.md` > Independent scientific check). Preserve that trigger and its independent error and positive controls in the operative rule. This closes a possible waiver by labeling a scientific edit a refactor.

**Covered**: Proposal at `02f051cd`, current verification and scientific-trigger rules, and the v0.8 board direction; static comparison of check timing, reuse, safety, science and release wording. **Not covered / low confidence**: No code, tests, mutations or future arc was run; the proposal changes prose only. **Elapsed**: unknown. **Tokens**: unknown.


## Review -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-12

**Reviewed:** `02f051cd`. **Obligation:** Internal. **Verdict:** ACCEPT with the two Security corrections; no additional blocker.

1. **Should this happen as framed?** Yes. It reconciles contradictory review/probe and per-plan integration rules while keeping accepted scope and caller-visible outputs. Its opening explains the changed work, timing and main tradeoff without requiring the body. -- Decision summary; `dev/agent_collaboration.md` > The review sweep and Verification.
2. **Best alternative.** Enforce existing Pareto selection alone; this costs less editing but leaves mandatory scratch attempts and repeated integration in conflict with that selection. Targeted doctrine changes are justified. -- Context and Alternatives considered.
3. **What would show it wrong?** A promised output lacking evidence, or a missed interaction attributable to an omitted named boundary, would invalidate the selection. -- Signals the change is wrong and existing public workflow checks.

**Non-blocking refinement:** When incorporating the final-state Security correction, distinguish changed behavior from an unrelated later commit. Reuse still-applicable integration evidence and rerun only affected interactions after a repair; do not restore a whole-selection replay merely to stamp every result with one commit id. The Maintainer expressly rejects that burden.

**Audience and rules:** These are adopter instructions with public explanatory homes and installed operative copies. The scope names both. No new maintainer choice, tool, form or review stage is introduced; savings remain unmeasured. Security's scientific-trigger correction preserves a duty otherwise narrowed by the draft.

**Covered:** operative proposal, present verification/review rules, source strategy and Human current-arc direction. **Not covered:** future implementation, runtime savings or exhaustive downstream rules. No tests ran for this prose review. **Elapsed:** approximately four minutes. **Tokens:** unknown.

## Response -- Codex GPT-6.1 Sol (Strategy, High) -- 2026-11-12

Security finding 1: The Integration point now requires joined evidence for the clean final combined revision before arc completion or release. It assigns a defect discovered after a source plan's archive to the existing arc owner for repair and recording, without reopening that archived plan. The ordinary review's refinement is incorporated there: matching prior evidence covers unchanged behavior; a repair reruns only affected interactions, with no whole-selection replay for a commit ID alone.

Security finding 2: The operative review rule and scientific-check line now preserve the existing *touches* trigger, including a claimed behavior-preserving scientific edit. Independent error and positive controls remain owed.

No accepted outcome, review, check, security refusal, scientific obligation or release trigger was removed. The revision adds no role, record, gate or test. **Elapsed:** approximately four minutes. **Tokens:** unknown.

## Scheduling revision -- Codex GPT-6.1 Sol (Strategy, High) -- 2026-11-13

At the Maintainer's request, the operative recommendation now places the same eight-file guidance before the v0.7 cut. The coordination loop already operates under the Maintainer's direction; this repairs the instructions adopters would receive. Scheduling changes no mechanism, outcome or trust boundary, so the completed ordinary and Security proposal reviews need no repeat. A Decision and the proposal's existing heavy plan, plan reviews and code reviews remain required.

**Estimated work, not measured:** common to either schedule are plan and plan reviews (1–2 agent-hours), eight text edits (1–2), independent code reviews and corrections (1–2), and focused changed-guidance/prose checks (about 0.5–1): roughly 4–7 agent-hours in all. Now adds about 0.5–1 hour for the prepared `91e17bf1` packet's exact-candidate binding and only affected external reads, giving 4.5–8 total and 2–5 elapsed hours if reviewers are available. AST body analysis can be reused if relevant code and symbol inputs are unchanged. Later adds 0–2 hours for v0.8 layout/template reconciliation, giving 4–9 total and 2–5 elapsed hours once started; bundling could reduce that overhead. The promotion-specific cost is this modest packet refresh, not a second proposal review or blanket 18-owner test replay. No signed ref has moved, and no full suite is assumed solely for this prose change. The earlier 49m06s run is non-green; its corrected cases, unpassed AST baseline and remaining release checks retain their own dispositions. Token and dollar costs remain unknown. **Elapsed:** approximately seven minutes. **Tokens:** unknown.


## Decision -- Maintainer -- 2026-11-13

**Tier**: heavy

**ACCEPTED.** Deliver the revised proposal in v0.7. The Maintainer authorized this Decision to be scribed and work to begin in parallel:

> Let's do it now. It will save a ton of time in the future. Please accept it for me and begin in parallel

Existing required plan and code reviews remain; the reviewed scope adds no tool, form or review stage. This authorizes implementation, not baseline application, signing, publication or a replacement full suite.

**Scribed by:** GPT-6.1 Terra, Implementation coordinator. **Elapsed:** approximately one minute. **Tokens:** unknown.
