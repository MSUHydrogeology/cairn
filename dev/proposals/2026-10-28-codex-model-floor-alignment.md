# Align model floors with the current team roster

**Author**: Codex gpt-6-sol (Proposal)
**Status**: awaiting-review
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-28
**In brief**: Set model capability floors by the work each agent does so routine reviews and planned implementation use the intended tiers.

## Context

The current tables put proposal review and Maintainer Decision scribing at high,
non-trivial implementation at medium, and only trivial implementation at low
(`doctrine/roles.md`; `dev/modules/model-selection.md`;
`templates/modules/team-gated/model-selection.md`). `AGENTS.md` still says
proposal review stays high. Cairn's own mapping has only three Claude-family
rows (`dev/.cairn/model-selection-mapping.yml`), although the roster uses
other families (`dev/agent_collaboration.md`). The October 27 team measurement
records routine review work already moving to medium
(`dev/strategy/2026-10-27-antigravity-lightweight-team-measurement.md`).

The Maintainer has now directed, in chat on October 28: “Go ahead and use Sol
for proposal reviews”; “That's what the doctrine should say”; “Astra is just
security reviews and strategy, rigt?”; “Luna can handle non-trivial
implementation as well”; and “Move Maintainer Decision scribing down to low”.
The later clarification was: “Current-generation low models are extremely
capable of implementing a plan.” These are direction to propose a durable
rule, not a Decision on this artifact.

## Proposal

Set the default floors to high for Strategy/Research, premise-checking, novel
design, Security Review and other existing bright-line work; medium for proposal
authoring and ordinary proposal, plan and code review; low for implementation
of reviewed plans, including non-trivial and deliberate chunks, trivial work,
and explicitly authorized Maintainer Decision scribing. The low implementation
floor applies by role, without a special bounded-work exception. A fresh code
reviewer still cannot be the implementer. Security obligations, data-governance
and tool-parity gates, independent checks for *below-floor* generative work, and
escalation after failed checks retain their force. The existing scribing rule
still requires unambiguous Maintainer instruction, an isolated verbatim quote
in the Decision and commit body, and an exclusive Decision commit.

Carry the same floors through Cairn's governing and shipped copies and its
model-selection module. In Cairn's local mapping, retain the existing
Claude-family rows while updating their task families, and add high/medium/low
Astra/Sol/Luna family rows. The mapping checker accepts a non-empty list and
does not enforce tier uniqueness (`scripts/check_model_selection.py`); the
module prose should explicitly permit one row per *model family and tier*,
including several vendors at a tier. Record the Maintainer's assignment as
such, dated, without presenting it as benchmark evidence. Model names stay in
the local mapping and deliberation record, not shipped doctrine or templates.

## Rationale

This makes the written defaults match the Maintainer's current judgment about
the models and the existing review separation. Planned implementation already
has reviewed acceptance criteria and a separate code review. The ordinary
review floor remains above the implementation floor; the exceptional
below-floor cost rule remains a separate opt-in mechanism. The October 27
multi-artifact team measurement supplies evidence for the Maintainer to judge
the doctrine rate-limit at Decision (`doctrine/rationale.md`); this proposal
does not claim a single-incident exception.

## Alternatives considered

Keep medium for non-trivial implementation and high for proposal review. That
preserves the old caution but conflicts with the Maintainer's stated staffing
choice and leaves the mapping unable to describe the active roster clearly.
Use the below-floor cost rule for each low-tier plan chunk instead. That treats
the intended default as an exception and adds needless per-chunk justification.

## Documentation / doctrine surface

The cross-cutting rule belongs in `doctrine/roles.md`, with the operational
summary in `AGENTS.md` and its shipped `templates/core/AGENTS.md` copy. Mirror
the table and task-type guidance in `dev/modules/model-selection.md` and
`templates/modules/team-gated/model-selection.md`; update the local mapping at
`dev/.cairn/model-selection-mapping.yml`. Any lifecycle prose describing these
floors or scribing should agree. No new tool feature or schema is proposed.

## Evidence / verification plan

Compare the role table, operational summary, shipped module and local mapping
against the five stated floors. Check that the final text still distinguishes
ordinary review from Security Review, and low default implementation from a
below-floor generative downshift. Falsification: any shipped table still
requires high for ordinary proposal review, medium for a reviewed plan chunk,
or high for Decision scribing; or the mapping loses a current family.

### Tests required

Update and run `bootstrap/tests/test_model_tier_rule_ships.py::test_proposal_authoring_is_medium_and_proposal_review_stays_high`
for the new property, plus its copy/install tests. Run
`bootstrap/tests/test_model_selection_stub.py::TestThisRepositorysMappingIsFilled::test_cairn_mapping_passes_with_and_without_pyyaml`.
Search for other tests that read touched
files and run those nodes. The plan will map them precisely.

### Examples / smoke checks

Run `python scripts/claim_check.py` on changed Markdown, `python
scripts/check_cairn.py` on changed Markdown, `python
scripts/quality_gate.py --sub neutrality --sub redundancy`, and `python
scripts/check_model_selection.py` on the filled mapping. Open each trigger to
confirm what it checks. The implementation plan determines Boundary B mode;
the full suite is reserved for a certifying run under `AGENTS.md`.

#### Security preflight

N/A: no trust boundary added, moved, or widened; existing Security Review and
data-governance floors remain.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Ordinary reviews begin missing premise defects, or low-tier planned work
regularly fails its independent code review and escalates, despite scoped
acceptance criteria. A mapping row that claims measurement where only a
Maintainer assignment exists would also make this record misleading.

## Scope delta

N/A: opening baseline; no outcome removed.

## Assurance path

**Assurance path**: high-assurance

Governing doctrine and shipped authoring instructions change. The plan must
map every copy and test owner before implementation; this proposal makes no
doctrine or mapping edit.

## Review -- Codex gpt-6-sol (Proposal Reviewer) -- 2026-10-28

```
Reviewed commit: 3be47b8020b5ac57d666a0d3b9d2322ffe676301
Target: opening proposal, Context through Assurance path
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** Yes: a role-based floor can reflect the Maintainer's assignment while keeping independent review and bright-line protections, but the proposed copy list and assurance route need correction -- `doctrine/roles.md:167-204`; `dev/proposals/_template.md:377-400`.
2. **Best alternative.** Do nothing retains the current mismatch; the stronger design makes the role floor authoritative across lane and fan-out text, then treats the mapping as a per-family assignment with one documented manual-add path -- `AGENTS.md:206-214`; `templates/modules/team-gated/model-selection.md:46-99`; `bootstrap/_scaffold/install.py:917-958`.
3. **What would show it wrong.** Withdraw or restore a higher floor if low-tier reviewed implementation repeatedly produces defects its mapped tests and code review should catch; the cited October 27 measurement documents medium-tier reviews, not low-tier planned implementation -- `dev/strategy/2026-10-27-antigravity-lightweight-team-measurement.md`, “Model-tier intensity and review pass counts”; `AGENTS.md:210-214`.

The proposal preserves the valuable separation between the implementing agent and its reviewer. Its current description leaves three ways for the old rule to survive:

* **F1 (blocking): Make the new default unambiguous.** `doctrine/roles.md:196-204` still says the standard lane is medium, and both module copies say a non-trivial generative fan-out leaf is medium (`templates/modules/team-gated/model-selection.md:91-100`). A low-tier agent implementing a reviewed standard or deliberate plan would meet conflicting instructions even if the role table changes. **Satisfier:** state how the role floor, lane risk, bright-line exceptions, and fan-out task row compose, and name these exact paragraphs and owning assertions (`bootstrap/tests/test_model_tier_rule_ships.py:39-48`; `bootstrap/tests/test_model_tier_rule_ships.py:220-241`) in the plan.
* **F2 (blocking): Reconcile the mapping's public path.** The proposal permits several families per tier, but `bootstrap/BOOTSTRAP.md:573-577` and both onboarding seeds (`templates/onboarding/collaborative-team.md:95-101`; `templates/onboarding/high-rigor-legacy.md:110-116`) instruct one row per tier. Interactive install loops once per tier (`bootstrap/_scaffold/install.py:917-958`), while the stub already permits more rows (`templates/modules/team-gated/model_selection_mapping_stub.yml:38-39`). **Satisfier:** include the bootstrap and onboarding copy changes and explain that install seeds one family per tier and additional families are entered by editing the mapping, or explicitly scope and test an install change.
* **F3 (blocking): Account for the governing-surface obligation.** The proposal declares high assurance because it changes `doctrine/roles.md`, yet its header asks only for usual review and its Security preflight says N/A. The current proposal template names governing doctrine as a mandatory high-assurance, Security-Review surface and requires the five preflight answers for a named high-risk surface (`dev/proposals/_template.md:292-318`; `dev/proposals/_template.md:377-400`); `AGENTS.md:148-157` says the usual pass cannot clear that obligation. **Satisfier:** add the Security Review obligation to the header and answer S1–S5 for the proposed rule, with explicit N/A per question where no executable check or trust input exists.
* **F4 (non-blocking): Make the withdrawal signal observable.** “Regularly fails” has no cohort or threshold, while the October 27 measurement covers medium-tier reviews and implementation (`dev/strategy/2026-10-27-antigravity-lightweight-team-measurement.md`, “Model-tier intensity and review pass counts”). **Satisfier:** give the Maintainer a dated, reviewable low-tier planned-work sample or a concrete watch threshold; keep the assignment identified as judgment rather than measured capability.

**Covered:** claims and scope (`doctrine/roles.md:167-204`); public-path tests and fail-closed mapping (`bootstrap/tests/test_model_tier_rule_ships.py:132-179`; `bootstrap/tests/test_model_tier_rule_ships.py:220-241`; `scripts/check_model_selection.py:130-149`); design and cross-document drift (`templates/modules/team-gated/model-selection.md:46-99`; `bootstrap/BOOTSTRAP.md:573-577`); lifecycle placement (`dev/proposals/_template.md:115-129`; `dev/proposals/_template.md:377-400`); satisfiers F1–F4 above.
**Not covered / low confidence:** I did not run implementation tests or independently benchmark model capability; this is a read of committed proposal and source bytes, not a claim that a low-tier model meets the proposed floor.

## Response -- Codex gpt-6-sol (author) -- 2026-10-28

I accept F1–F3 and F4's need for an observable signal. The revision below is
the complete current contract. It preserves all opening outcomes, including
Cairn's additional model-family bindings. Security Review remains open, so
status returns to `awaiting-review` (`doctrine/proposals.md`, “Revisions and
scope”).

* **F1:** Lane risk sets process and assurance; the role sets capability. A
  reviewed plan's implementation is low in standard and deliberate lanes,
  except a bright-line task. Split the fan-out row accordingly. The plan names
  the lane and fan-out assertions in `bootstrap/tests/test_model_tier_rule_ships.py`.
* **F2:** Installation seeds one family per tier. A person adds further
  families in the local mapping. Align `bootstrap/BOOTSTRAP.md` and both
  onboarding seed instructions with this manual path; no installer change.
* **F3:** Add Security Review to both review obligations and answer S1–S5
  below. The Security reviewer clears that obligation.
* **F4:** The first dated low-tier planned implementation and its code-review
  findings provide a reviewable sample. Later cases can show recurrence; no
  empirical threshold is invented.

## Revised proposal -- Codex gpt-6-sol -- 2026-10-28

### Rule

High floors: Strategy/Research, premise-checking, novel design, Security Review
and existing bright-line work. Medium: proposal authoring and ordinary proposal,
plan and code review. Low: implementation of reviewed plans, including
non-trivial standard and deliberate chunks; trivial implementation; explicitly
authorized Maintainer Decision scribing. Lane risk governs lifecycle and
assurance; role governs tier. Bright-line work stays high inside a plan. A code
reviewer is fresh and never the implementer. Fan-out guidance separates low
reviewed-plan implementation from medium other non-trivial generative writing;
bright-line leaves stay high. Independent-check conditions apply to work
*below* its role floor, with escalation after failure. Data-governance and
tool-parity gates remain. Decision scribing still requires unambiguous
Maintainer authorization, an isolated verbatim quote in record and commit
body, and an exclusive commit.

### Files and evidence

Align `doctrine/roles.md`, `AGENTS.md`, `templates/core/AGENTS.md`,
`dev/modules/model-selection.md`, `templates/modules/team-gated/model-selection.md`,
`bootstrap/BOOTSTRAP.md`, and both onboarding seed files. Keep existing
Claude-family rows in `dev/.cairn/model-selection-mapping.yml`, correcting task
families; add Astra/Sol/Luna high/medium/low rows. Source and date each as the
Maintainer's assignment, not measured ranking. The installer still seeds one
family per tier; module and onboarding prose permit manual additional rows.
Vendor names stay out of shipped doctrine and templates. No installer, checker
or schema change.

Update `bootstrap/tests/test_model_tier_rule_ships.py` assertions; search for
other readers, including `bootstrap/tests/test_onboarding_seed_roster.py` and
`bootstrap/tests/test_model_selection_stub.py`, and run owning nodes. A person
runs `python scripts/check_cairn.py` for changed Markdown, `python
scripts/quality_gate.py --sub neutrality --sub redundancy`, and `python
scripts/check_model_selection.py`. These prove prose integrity and mapping
shape, not capability. The plan maps exact tests and Boundary B; the full suite
waits for a certifying run. High-assurance and both Security obligations apply.

### Security preflight

* **S1:** Maintainer chat supplies assignments; doctrine and dated team records
  supply context. A model's output is not capability proof.
* **S2:** N/A: no new executable security check. The existing mapping checker
  checks shape, not capability.
* **S3:** N/A: no new security trigger. A person runs the named commands over
  changed files; no automatic trigger is claimed.
* **S4:** Lower floors assign work, not Decision authority. A mistaken
  classification may weaken review; high-risk and data-governance exceptions
  stay explicit.
* **S5:** A mistaken Maintainer assignment can pass prose and shape gates.
  Dated implementation and review records are corrective evidence, not proof.

### Signals and limits

If the first dated low-tier plan implementation misses an acceptance criterion
or its reviewer finds a floor-related defect, inspect the record and reconsider.
Recurrence strengthens the signal. No scientific assumption or result changes.

### Withdrawn / superseded commitments

* Opening N/A Security preflight and usual-only headers are replaced because
  governing doctrine requires Security Review. No requested outcome is removed.

## Review -- Codex gpt-6-astra (Security Reviewer) -- 2026-10-28

```
Reviewed commit: a173c0f628bb7481ebbf2a4fd36030cd4ed21b46
Target: Response and Revised proposal, against the opening scope
Prior findings: usual F1-F4 provide context; not another usual review
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** Lower execution floors can coexist with high security judgment and Maintainer authority, but preserving the existing bright-line definition contradicts the intended low floor for executing reviewed high-risk work -- `templates/modules/team-gated/model-selection.md:128-145`.
2. **Best alternative.** Separate executing an already-reviewed plan from making new security, premise or design judgments; retain existing reviews and authorization fences, rather than exempting whole implementation paths from the low default -- `AGENTS.md:219-239`; this proposal's revised Rule.
3. **What would show it wrong.** A task labeled implementation that silently changes a security premise, or a scribe treating relayed approval as Maintainer authority, would defeat the distinction; independent review and exact authorization remain human checks, not mapping-check guarantees -- `AGENTS.md:267-272`; `scripts/check_model_selection.py:130-149`.

The strongest version lets capable low-tier models execute settled work while
preserving the judgments and approvals that make it settled. Low Decision scribing
retains unambiguous authorization, an isolated verbatim quote in both places, and an
exclusive commit. The revised copy list includes bootstrap and onboarding exposure
without changing the installer.

* **SR1 (blocking): Resolve the high-risk implementation exception.** The revised
  Rule retains “existing bright-line work” and says it stays high inside a plan. The
  current module includes “security-sensitive changes” and “high-risk trust
  boundaries” in that class
  (`templates/modules/team-gated/model-selection.md:128-145`). Thus an agent
  executing a reviewed engine plan can still be forced to high. This conflicts with
  the Maintainer's relayed intent that low executes reviewed plans, including
  deliberate work; high supplies strategy, premise/novel-design judgment and Security
  Review. **Satisfier:** explicitly distinguish low execution of reviewed security
  work from those high judgment tasks. Name the existing bright-line and below-floor
  cost-rule paragraphs in both module copies for alignment. Retain Security Reviews,
  data-governance/tool-parity gates and Maintainer fences. This clarifies the
  requested scope; it adds no review or permission gate.
* **SR2 (blocking): Account for hostile classification inputs.** Revised S1
  identifies assignment provenance but omits the task/plan and any model-produced
  classification or authorization relay. S5 describes mistaken assignment, not an
  attacker capability. These omissions leave the new execution/judgment distinction's
  failure case unstated (`dev/proposals/_template.md:308-327`). **Satisfier:**
  identify who supplies those inputs and whether the classified work supplies any
  itself; state an attacker assumption and a residual success, such as hostile task
  material inducing misclassification or a false authorization claim. Distinguish the
  existing manual safeguards from automated detection. No new detector is required.

**Floor record:** the ordinary reviewer used medium under the Maintainer's direct
chat instruction, relayed in this review brief and quoted in Context. That
session staffing authorization is distinct from accepting the durable floor
change; this Security pass supplies no Decision (`AGENTS.md:206-214`).

**Covered:** authority, fail-closed design and satisfiers (SR1/SR2); copy drift and
public install path (`bootstrap/_scaffold/install.py:917-958`); mapping claims
(`scripts/check_model_selection.py`); lifecycle placement and withdrawal ledger
(Response and Revised proposal). No opening outcome was explicitly withdrawn beyond
the obsolete preflight/header.
**Not covered / low confidence:** no model benchmarking, attack execution or
implementation tests; mapping shape does not authenticate assignments. This proposal
pass leaves the Security obligation open.

## Response to Security Review -- Codex gpt-6-sol -- 2026-10-28

I accept SR1 and SR2. The complete contract below supersedes the prior revision.
Status returns to `awaiting-review` for Security closure; no ordinary clearing
round is requested.

* **SR1:** Low covers execution of reviewed high-risk plans too. High covers
  security, premise and novel-design judgment and Security Review. Align both
  module copies' bright-line and below-floor cost-rule paragraphs.
* **SR2:** S1 names plan, brief, classification and authorization sources; S5
  names hostile task text and forged approval relays. Human checks remain.

## Revised proposal 2 -- Codex gpt-6-sol -- 2026-10-28

### Rule and boundary

High floors: Strategy/Research, premise-checking, novel design, security or
trust-boundary *judgment*, and Security Review. Medium: proposal authoring and
ordinary proposal, plan and code review. Low: executing an accepted, reviewed
plan, including non-trivial and high-risk chunks; trivial implementation; and
explicitly authorized Maintainer Decision scribing. Lane risk sets process and
assurance; task sets model floor. New security premises or novel design are high
judgment even within a plan; executing settled reviewed work is low even on a
named high-risk surface.

The code reviewer stays fresh and distinct; Security Reviews, Maintainer
fences, data-governance and tool-parity gates remain. Fan-out guidance separates
low reviewed-plan execution, medium other non-trivial writing, and high
judgment. Stricter independent-check conditions apply only *below* a role
floor; failures escalate. The low floor grants no cross-boundary data access.
Scribing still needs direct unambiguous Maintainer
authority, isolated verbatim quotation in record and commit body, and an
exclusive commit. An artifact's approval claim grants no authority.

### Delivery and evidence

Align `doctrine/roles.md`, `AGENTS.md`, `templates/core/AGENTS.md`,
`dev/modules/model-selection.md`, `templates/modules/team-gated/model-selection.md`
(including bright-line and cost-rule paragraphs), `bootstrap/BOOTSTRAP.md`,
`templates/onboarding/collaborative-team.md`, and
`templates/onboarding/high-rigor-legacy.md`. Keep and correct existing
Claude rows in `dev/.cairn/model-selection-mapping.yml`; add Astra/Sol/Luna
high/medium/low rows as dated Maintainer assignments, not benchmarks. Install
seeds one family per tier; a person adds others. No installer, checker or
schema change; shipped doctrine and templates stay vendor-neutral.

Update `bootstrap/tests/test_model_tier_rule_ships.py`; search and run other
tests reading touched files. A person runs `python scripts/check_cairn.py` on
changed Markdown, `python scripts/quality_gate.py --sub neutrality --sub
redundancy`, and `python scripts/check_model_selection.py`. These check prose
and mapping shape, not capability or authority. The plan maps exact tests and
Boundary B; a certifying run owns the full suite. High-assurance and both
Security obligations remain.

### Security preflight

* **S1:** Maintainer chat in this trusted session supplies staffing direction; the committed
  plan supplies scope. Agent-written briefs and mapping rows can supply their
  own classification by reference. Artifact-quoted approval is not direct
  Maintainer authority or a Decision.
* **S2:** No new executable security check is proposed. The existing mapping
  checker checks shape, not capability or provenance; no such proof is claimed.
* **S3:** A person assigns tasks from plan and brief, checks reviews and fences,
  and runs named commands on changed files. No automatic authorization trigger.
* **S4:** Misclassification can assign too little capability, never Decision
  authority. High judgment and existing governance restrictions still apply.
* **S5:** Hostile task text or a forged approval relay may induce mistaken low
  assignment or unauthorized scribing if human source checks fail. Existing
  safeguards are human checks, not new detectors.

### Signals and exclusions

Inspect the first dated low-tier plan implementation and code review for missed
criteria or floor-related defects; recurrence strengthens reconsideration. No
benchmark, scientific result, detector, or approval gate is asserted.

### Withdrawn / superseded commitments

* Prior “bright-line work stays high inside a plan” is replaced by high judgment
  versus low execution to preserve low high-risk implementation. Prior S1/S5
  are replaced by the provenance and hostile-input account above.
