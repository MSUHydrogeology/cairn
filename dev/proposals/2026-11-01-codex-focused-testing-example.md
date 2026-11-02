# Align the documentation plan's testing example

**Author**: Codex GPT-6.1 Sol (Strategy)
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy — the installed, vendor-neutral methodology template is a named high-risk surface.
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Update a shipped example so it reminds adopters to use focused testing rather than run the whole suite after every substantive change.

## Decision summary

Replace the testing example in the documentation plan template with a focused-testing reminder. The example currently suggests running the test suite after every substantive change, which conflicts with Cairn's focused-testing guidance. Preserve the example's purpose: an operational reminder can pair with a rationale in the collaboration doctrine. The cost is the review and verification owed for changing a shipped template.

## Context

Issue #42 identifies the example in `templates/modules/default-on/documentation_plan_template.md`, under the paired-update rule. The same paragraph points to testing-discipline rationale; `AGENTS.md` instead directs implementation to tests that name changed files and restricts full-tree certification to named occasions. An adopter copying the example could infer a broader routine than intended.

## Proposal

Replace only the quoted testing example with a concise reminder to run focused tests for changed files. Retain the surrounding explanation and its example of paired testing rationale. Do not change testing policy, the paired-update rule, or install behavior.

## Rationale

A current example illustrates the same pairing without recommending unnecessary full-suite runs. This is a wording correction, not evidence that adopters actually followed the old example.

## Alternatives considered

Leave the example unchanged: it avoids an edit but continues to present a conflicting testing practice. Remove the example: that removes the conflict but loses a concrete illustration of the pairing.

## Documentation / doctrine surface

The change lands in the shipped documentation-plan template, a domain-local governing example. Deliberation stays in this proposal; no cross-cutting rule or descriptive documentation changes are proposed.

## Evidence / verification plan

### Tests required

At implementation, search for direct readers and byte pins of the template, run the file-specific selection from `python tools/test_tiers.py for templates/modules/default-on/documentation_plan_template.md`, and record omissions. A plan must map any affected install or integration paths before implementation. A reader or pin that still requires the old wording would falsify the change's completeness.

### Examples / smoke checks

Run applicable claim, link, snippet and neutrality prose gates. Check the resulting paragraph against the focused-testing guidance and confirm that the paired rationale remains intelligible. Complete wide Boundary B on the final reviewed commit because the shipped template is a high-risk surface.

#### Security preflight — five questions, answered in writing

S1: The proposed change makes no authentication or admission decision; its input is maintained template prose. S2: No new security check is proposed; the reader and pin search must be checked against a known-positive result, with outcomes recorded during implementation. S3: Existing prose and file-specific checks are selected as described above; their actual triggers and coverage must be opened and recorded in the plan, rather than assumed. S4: No default, parser, fallback or error path changes. S5: An actor able to alter shipped prose could still insert misleading guidance; this wording change does not prevent that capability.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

The replacement implies a full suite is always required, omits tests that should be selected under current guidance, or obscures the reason operational guidance pairs with a rationale.

## Scope delta

**Scope delta**: preserved; the proposed change addresses the identified example only.

## Assurance path

**Assurance path**: heavy, with ordinary and Security Reviews and a reviewed plan, because the change touches a shipped vendor-neutral methodology template. No new trust boundary is proposed.

## Ordinary proposal review -- Codex GPT-6.1 Sol -- 2026-11-01

**Verdict:** Support as framed; no blocking findings.

**Foundations.** Should it happen? Yes: the committed template's paired-update example says to run the suite after any substantive change, while `AGENTS.md` limits iteration to tests naming changed files and separately requires a final integration selection. The example can mislead even though it is illustrative. Best alternative: delete the example; this removes the misleading wording but loses the concrete operational-rule/rationale pairing. A short focused-testing example preserves that purpose with no new process. What would show this wrong? A replacement that suggests changed-file tests are the only required verification, or an unchanged reader that still prescribes the old wording, would leave a misleading account.

**Advice:** Keep the replacement illustrative and concise; avoid introducing a new selection rule or verification apparatus. Check that it does not imply the final integration selection is optional. The proposal's existing reader search and prescribed checks can establish the relevant evidence without creating a new process.

**Coverage:** Read proposal and the template at `bc2c211e`, and checked the iteration and integration rules in `AGENTS.md` and the installed testing module. Did not inspect every downstream copy or run implementation checks; those remain for implementation. Elapsed: approximately 2 minutes; tokens: unknown.

## Security proposal review -- Codex GPT-6.1 Sol -- 2026-11-01

**Verdict:** Support as framed; no blocking findings.

**Foundations.** Should it happen? Yes. At `7dd331a0`, the shipped documentation-plan template's paired-update example says “Run the test suite after any substantive change”; `AGENTS.md` Verification instead separates changed-file iteration, final integration and named certification occasions. Correcting this example removes a competing instruction without changing executable checks or admission decisions. Best alternative: remove the testing example. That avoids prescribing test selection but loses the concrete reminder/rationale pairing; a short focused-testing example preserves that teaching purpose. What would show this wrong? Wording that permits skipping required integration or security checks, or implementation that changes the surrounding paired-update rule, would defeat the proposal's explicit policy-preservation boundary.

**Advice:** Keep the example subordinate to the project's required verification. “Focused tests” must not imply that changed-file tests exhaust assurance. No additional mechanism is needed: the proposal already retains heavy review, reader/pin discovery and wide final integration verification.

**Coverage:** Read the proposal, the shipped paired-update paragraph, `AGENTS.md` Verification and `templates/modules/team-gated/testing-discipline.md` at `7dd331a0`; examined whether the scope could weaken required checks or introduce a trust boundary. Did not evaluate replacement bytes, downstream installation behavior or implementation checks, because no implementation exists yet; ran no suite. Elapsed: approximately 3 minutes; tokens: unknown.
