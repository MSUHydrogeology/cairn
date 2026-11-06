# Human-useful ceremony output and return on attention

**Author**: Codex (Strategy / proposal author, gpt-6.1-sol, High)
**Status**: awaiting-review
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
  sentence adds a small recurring writing/read cost. No numerical savings
  estimate exists.
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

Map affected checks with `tools/test_tiers.py for` after selecting concrete
paths. Extend existing ceremony/forward/baseline tests for misleading approval
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
