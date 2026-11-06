# Human-useful ceremony output and return on attention

**Author**: Codex (Strategy / proposal author, gpt-6.1-sol, High)
**Status**: awaiting-decision
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-06
**In brief**: Explain what each trust approval does and whether the delivered benefit justified its human effort, using existing records and safeguards.

## Decision summary

Make the maintained ceremony guide explain the behavior being approved, why it
matters, its risk, its evidence and exactly what the next approval permits.
Keep every required comparison visible where the person must make it. Reuse
existing Decision and closing records to describe human follow-ups and judge
whether the result repaid their attention. This adds presentation maintenance
and one short closing judgment, with no new approval, ledger or ceremony.

## Context

Board item 11 combines the Maintainer's request for human-useful ceremony
output with [nimbleness recovery, item 4](../strategy/2026-08-21-claude-nimbleness-recovery.md#4-add-lightweight-return-on-attention-accounting-to-proposals).
The current [driver](../../scripts/repin.py), `run_ceremony`, verifies the
launcher, packet, reader record, signer and package, then relays the report
under “Summary 2” and asks whether it describes the intended signature. The
[runbook](../../bootstrap/REANCHOR_RUNBOOK.md) explains the comparisons and
limits. The output has useful disclosures; it is not an empty hash display.
It nevertheless mixes raw evidence with the approval story, leaving the
person to connect what changed to what their next yes authorizes.

Attention accounting is partly delivered already. [AGENTS.md](../../AGENTS.md)
requires meaningful build/run/understanding/maintenance costs for material
choices and new recurring additions in the Decision. The [archive rules](../../docs/methodology/lifecycle.md#archive-precondition--every-deferred-follow-up-carries-a-disposition)
and [plan template](../plans/_template.md#dispositions) require explicit
follow-up dispositions, live homes and batched deferral requests. These are
real safeguards, not missing machinery. They do not explicitly ask whether
the delivered benefit repaid the effort, or consistently name the number and
kind of human operations in the Decision's existing cost sentence. No human
usability or saved-time measurement is claimed here.

## Proposal

Deliver both outcomes together for v0.7, before final ceremony preparation,
in one independently finishable plan:

1. **Explain existing approvals at their real entry points.** Revise the
   maintained `repin` presentation and runbook for ordinary/transition
   ceremonies, verifier HOLD dispositions and explicit forward/baseline
   approval paths. At each existing approval, say what changes, its purpose,
   remaining risk, the evidence source, and the exact authorized action.
   Distinguish preparation, independent review, applying or committing pins,
   signing/ref movement and publication. Describe a HOLD as unresolved even
   after a bounded proceed disposition. Derive factual labels from already
   checked state; never invent a semantic safety verdict from a digest.
2. **Finish attention accounting in existing records.** Clarify the existing
   Decision cost sentence to name material human operations and follow-up
   homes/counts, including zero when useful, without a new field or exhaustive
   inventory of routine agent work. At implementation closeout, add one
   sentence to the existing verification/disposition record judging benefit
   against observed effort and remaining burden; say unknown when evidence
   cannot support a judgment. Light work uses its proposal record. Reconcile
   this with existing archive completeness judgment; add no second archive
   gate, score, timesheet or Maintainer response.

Automated exact-byte, fingerprint, packet/reader binding, security checks,
refusal behavior, prompt order and approval boundaries remain unchanged.
Full hashes and structural differences remain in technical evidence. A digest
that must be pasted/compared and an independently sourced signer fingerprint
remain visible at that comparison; “technical detail” is not permission to
hide them. No extra manual comparison, command or confirmation is introduced.

## Rationale

A short explanation beside the existing approval can make its purpose clear
without weakening the mechanism that binds it to exact bytes. Reusing the
Decision and closeout record also preserves both attention outcomes without
another reporting system. Reduced human effort is a hypothesis, not a result.

## Alternatives considered

- **Keep current tools and rules.** No build or maintenance cost. Existing
  comparisons and cost/disposition rules survive, but approval translation
  and the explicit retrospective judgment remain incomplete.
- **Presentation and existing-record clarification.** The proposed scope
  requires a bounded cross-surface edit, targeted tests and both reviews;
  future prompt changes must maintain their explanations. The closing
  sentence adds a modest recurring agent writing and reader-attention cost
  at each closeout. It requires no extra Maintainer response. No numerical
  savings estimate exists.
- **New report generator or attention ledger.** Could aggregate histories,
  but adds a format, readers, maintenance and recurring collection, with no
  current evidence it improves this decision. Defer that expansion.

**Recommendation:** take the presentation and existing-record clarification;
it delivers both requested outcomes with the least additional mechanism.

## Documentation / doctrine surface

Software guidance lands in the driver and runbook. Cross-cutting prescription
belongs in local/shipped AGENTS and existing proposal/plan templates, with
rationale in lifecycle documentation. Follow [documentation routing](../../docs/DOCUMENTATION_PLAN.md);
coordinate shared template edits with other accepted work. Do not alter
machine evidence schemas or introduce a new artifact type.

## Evidence / verification plan

### Tests required

Before editing, map ordinary, transition, verifier, forward and baseline
prompt-text consumers, including protected manifests naming parameterized test
nodes. Map affected checks with `tools/test_tiers.py for` after selecting
concrete paths; retain the real comparison/authority checks and account for
any required protected-test review or baseline handling. Extend existing
ceremony/forward/baseline tests for misleading approval
text, missing required comparison values and changed refusal/authorization
behavior; do not replace byte/security assertions with wording assertions.
Use synthetic fixtures only. Final Boundary B is wide because this is a trust
ceremony and doctrine surface. Existing certification triggers stay unchanged.

### Examples / smoke checks

A fresh reader must explain each affected approval's effect and limits from a
saved synthetic transcript plus its evidence, including a refusal/HOLD case.
Compare before/after manual prompts and prescribed operations: additions fail
the no-extra-step criterion. This supplies comprehension evidence, not measured
Maintainer usability. Run claim, link, snippet and neutrality prose gates.

#### Security preflight — five questions, answered in writing

- **S1 — Who supplied it?** Candidate bytes, packets, reader records, values
  and reports retain their existing channels and checks; candidate-supplied
  report claims remain identified. This change adds no decision input.
- **S2 — Can it fail?** Existing `test_repin_ceremony.py` disclosure controls
  remove each required line and detect its absence. Implementation must also
  demonstrate failure when an approval loses its required comparison or
  misstates the authorized action. No mutation was run for this draft.
- **S3 — What fires it, over what?** Maintainers invoke the runbook's existing
  commands; plan-mapped tests exercise their synthetic paths. Preserve its
  instruction: “Agents prepare the packet and read the change”; the
  Maintainer inspects comparisons, decides and signs. New explanations cover
  those actions, not an unexecuted substitute guide.
- **S4 — Which way does it break?** No parser, fallback or default changes.
  Missing evidence still refuses; a clearer summary cannot turn unknown or
  HOLD into permission.
- **S5 — Who still wins?** Code already running as the Maintainer can still
  subvert the host. Presentation does not contain candidate code or establish
  external authority; disclose that limitation at the relevant approval.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A reader cannot identify the next action or its residual risk; a required
comparison value disappears; an approval or refusal changes; manual work
increases; or closing judgments become unsupported claims of time saved.

## Scope delta

**Scope delta**: preserved — both board outcomes remain; existing accounting
is reused rather than claimed absent.

## Assurance path

**Assurance path**: high-assurance

Trust-ceremony presentation and governing templates require separate usual and
Security Reviews at applicable stages. This proposal authorizes no operation,
signing, baseline installation, private collection, host change or push.

**Authoring record**: elapsed unknown; tokens unknown. Source inspection only;
no ceremony, test suite or implementation check run for this opening draft.

## Proposal review -- Codex GPT-6.1 Terra (Medium) -- 2026-11-06

**Reviewed commit**: `d20e24fb`. **Verdict**: PROCEED; no blocking findings. **Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**:

1. **Should it happen as framed?** Yes. `run_ceremony` displays the signer and package digest before Summary 2, while the runbook separately explains the independent reader, key and comparison limits. Connecting those facts to each existing authorization can reduce translation work; a closeout judgment adds an explicit retrospective that current Decision cost and follow-up disposition rules do not require. Benefit remains unmeasured.
2. **Best alternative.** Keep the current checks and records, adding concise explanations and one evidence-qualified sentence as proposed. Doing nothing costs nothing and preserves safeguards, but leaves the retrospective and approval context implicit. A new ledger adds recurring collection and maintenance; the proposed wording and tests still cost implementation and future prompt maintenance.
3. **What would show it wrong?** A synthetic transcript that misstates the action, obscures a required digest or independent fingerprint, changes a refusal, adds a human step, or leaves a reader unable to explain a HOLD would falsify the outcome. An unsupported claim of saved effort would falsify the closeout outcome.

**Advice**: Map prompt-text consumers before editing: `test_repin_ceremony.py` drives and slices output using Summary 2 and question text, and protected manifests name parameterized nodes. Preserve these contracts or explicitly account for their required review and baseline handling.

**Coverage**: Read the proposal, template and cost/disposition rules, ordinary, verifier, forward and baseline entry points and runbook comparisons, plus stdout test consumers. Did not execute ceremonies, tests, private sources or provider actions; did not exhaustively audit all consumers. Separate Security Review remains due.

## Security proposal review -- Codex GPT-6.1 Sol (High) -- 2026-11-06

**Reviewed commit**: `b7a0b987`
**Obligation**: Internal Security Review
**Tier**: Security Review
**Verdict**: PROCEED; no blocking findings.
**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**:

1. **Should it happen as framed?** Yes: explain each existing authorization without replacing its evidence. `run_ceremony` compares the pasted launcher digest, authenticates the prior signer, displays the package/fingerprint and rechecks package bytes after approval. The proposal explicitly retains these comparisons and independent reader authority. -- `repin.py`, `run_ceremony`; runbook verifier and ceremony sections.
2. **Best alternative.** Keep the existing driver and add explanations at its prompts plus the single evidence-qualified closeout sentence. Runbook-only edits cost less but leave the actual approval context implicit; a new attention ledger adds unnecessary collection and maintenance. Current cost/disposition rules already provide the record homes. -- Proposal alternatives; AGENTS Decision cost rule; plan template Dispositions.
3. **What would show it wrong?** Remove a required digest/fingerprint, substitute a candidate claim for authenticated evidence, or describe a dispositioned HOLD as cleared: synthetic transcript and refusal checks must fail. A fresh reader must still identify the exact next authorization and limits, with no additional manual operation. -- Proposal checks; `test_repin_ceremony.py` Summary 2 disclosure and prompt-driving consumers; runbook HOLD contract.

**Advice**: Inventory the ordinary, transition, verifier, forward and baseline prompt consumers before editing. Preserve comparison values at their existing decision point, including the independently sourced fingerprint; retain machine schemas and exact-byte checks. Keep retrospective judgments evidence-qualified, including unknown, rather than turning them into a new response or archive gate. The proposed synthetic comprehension check supplements rather than removes any existing human comparison.

**Coverage**: Read committed proposal/template, driver approval and watched-byte paths, forward/baseline boundaries, runbook risks/HOLD handling, prompt tests and current cost/disposition rules. No tests, ceremonies, signing, baseline operations or host/private data access; complete consumer mapping and comprehension remain implementation evidence.

## Response -- Codex GPT-6.1 Sol (High) -- 2026-11-06

Both reviews recommend proceeding without blockers.

- **Usual advice accepted:** The verification plan now explicitly maps prompt
  consumers and protected parameterized nodes before editing, preserving real
  comparisons and accounting for required protected-test review/baseline
  handling. This specifies the existing assurance outcome, without new scope.
- **Security advice accepted:** The same mapping covers every named entry
  point. Existing operative text retains independent fingerprints at their
  comparison, exact-byte/schema/authority checks and evidence-qualified payoff
  judgments, including unknown. No new ledger, human step, response or archive
  gate is introduced. The option comparison now explicitly states the modest
  recurring agent prose and reader-attention cost.

Opening prose gates passed on a separate copy of `d20e24fb` under Python
3.12.9: claim, link, content, snippet and neutrality (zero failures). Named
reader selection returned zero tests; the exact-stem search found none and
the AGENTS reader search provided a positive control. These are not canonical
Python 3.13 evidence. Final canonical committed-copy verification is recorded
below after the status transition.

**Elapsed**: approximately 4 minutes. **Tokens**: unknown.

### Withdrawn / superseded commitments

None.

## Author verification -- Codex GPT-6.1 Sol (High) -- 2026-11-06

On a separate archive of committed `534f4ee7`, Python 3.13.13 passed
`claim_check.py`, `link_check.py`, `check_cairn.py` and
`sync_doc_snippets.py --check`, each naming this proposal, plus
`quality_gate.py --sub neutrality` (zero failures, 43 informational entries).
The tools ran against that copy's root; no implementation bytes were checked.
`tools/test_tiers.py for` selected zero tests for the exact proposal path.
The exact proposal-stem reader search in `bootstrap/tests` found none; an
AGENTS filename search found existing readers as its positive control.
No test suite, ceremony, private input or host change was performed.

Both review records remain verbatim; response `4df902fb` specifies their
advice without widening scope. Status transition `534f4ee7` leaves the
proposal awaiting the Maintainer's Decision. No required proposal check
remains open; future implementation evidence remains conditional on approval.

**Elapsed**: approximately 1 minute. **Tokens**: unknown.
