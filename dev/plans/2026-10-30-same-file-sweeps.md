# Plan: Detect and record same-file sweeps

**Source proposal**: dev/proposals/archive/2026-10-29-codex-same-file-sweeps.md
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Assurance path**: high-assurance
**Opened**: 2026-10-30
**In brief**: Help shared-tree authors avoid misattributed commits and count confirmed sweeps honestly.

## Source proposal

The accepted revision extends existing commit inspection with agreed serialization, defines a confirmed sweep and one countable event per commit, and makes the advisory gate's incomplete reporting explicit. Its Security preflight and residual limitations remain part of the contract.

## Scope

Update `AGENTS.md`, `doctrine/coordination.md`, `dev/modules/coordination-tiers.md`, `templates/modules/team-gated/coordination-tiers.md`, tracker guidance in `templates/modules/default-on/incident-trackers.md` and `templates/modules/default-on/incident_log_template.md`, and advisory output in `tools/evolution_infer.py` and `templates/modules/default-on/evolution_infer.py`. Search for other installed owners and consumers and keep corresponding copies aligned. Reconcile the local `dev/measurement/collision_log.md` without overwriting it; do not invent confirmation. No attribution detector or claim-release change.

**Reuse.** `rg -n 'collision_log|same.file|evolution_infer|coordination.md' tools bootstrap/tests doctrine/coordination.md AGENTS.md` found the existing gate, tracker and tests; extend them rather than build a detector. The two gate scripts are intentional installed counterparts.

### Documentation / doctrine surface

Coordination prescription belongs in governing doctrine and installed coordination guidance; tracker and output describe reporting. Apply `docs/DOCUMENTATION_PLAN.md`. Before doctrine edits establish the trigger under `doctrine/rationale.md` > How the doctrine evolves under evidence; if not established, stop for Maintainer resolution. The shipped gate and its tests are listed in `bootstrap/tests/fixtures/protected_test_roster.json`; record the applicable gate-manifest ceremony and do not self-authorize re-anchoring.

**Maintainer resolution, 2026-10-30:** After being shown that recurrence and synthesis evidence was not established, the Maintainer authorized proceeding past this doctrine gate:

> Go ahead

This allowance does not assert that recurrence or synthesis occurred.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Update guidance, gate output, focused checks and local incident reconciliation | Both plan reviews; doctrine trigger before doctrine edits | Aligned guidance and gate copies, tests, local report if evidence permits |
| C2 | Verify and hand to code review | C1 complete | Change verification and review handoff |

## Acceptance criteria

### C1

Agree serialization before inspecting shared paths through commit; claims alone are not agreement. Inspect tracked candidates against HEAD, including staged and unstaged bytes, and new files directly; reinspect changed bytes. Stop on foreign or uncertain content and coordinate; use separate worktrees when agreement cannot hold. State that noncooperating writers can defeat this procedure.

A confirmed sweep requires author confirmation or recorded provenance, not a claim or diff alone. Record one `occurred` row per commit with paths together, occurrence and discovery dates, and a minimal confirmation reference; check for an existing row. Put occurrence date in the existing `Date` column and discovery date in a separate field. Keep uncertain reports outside the Incidents table until confirmed; never mark them `occurred`. Prevented cases remain separate. Reconcile `5094a977` only if confirmed, preserving the local tracker. Keep evidence local; screen committed summaries for sensitivity and exclude private conversations, secrets and unrelated uncommitted text.

The real gate suggests two in-window confirmed commits, including one with two paths, but not one commit or a prevented case; late discovery uses occurrence date. Human and JSON output identify incomplete reporting and remain advisory. Demonstrate staged foreign content, changed bytes requiring reinspection, and legitimate separately authored integration without inventing attribution.

S2: change one of two occurred impacts to prevented and show the threshold finding disappears, with an unmutated control. S3: the human runs the mapped tests and gates below; inspection and confirmation remain human judgments.

### C2

Record the clean tested SHA and range, interpreter, pre/post state, commands, outcomes, timing, non-pass dispositions, omissions and ceremony obligation; hand to independent code review.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A runs the mapping below during iteration; Boundary B repeats it on the final clean commit in **wide** mode for governing and installed contracts, under canonical Python 3.13.x, with `Certified by: pending`. No full certification is implied.

* `bootstrap/tests/test_evolution_infer.py::TestGateEval` and new real `main` fixture tests cover one multipath commit, two distinct commits, prevented impact, uncertain reports outside the table, occurrence versus discovery dates, human and JSON warnings, and the S2 mutation. `TestRegistration::test_tool_installed_verbatim` covers the installed gate; `bootstrap/tests/test_session_binding_gate_and_printing_hold.py` covers the session consumer.
* `bootstrap/tests/test_incident_trackers_module.py::TestSchemaContract` covers tracker schema and impact values; extend it for the human reporting contract. `bootstrap/tests/test_coordination_broad_intent.py::TestBroadIntentBoundary` covers installed coordination. Add focused guidance assertions for all changed governing and installed copies and run `bootstrap/tests/test_intents_tool.py` for existing conflict behavior. Inspect the actual installed module output for the new wording.
* In a disposable repository, document a human inspection of staged foreign bytes against HEAD, an intervening write and reinspection, and a legitimate separately authored integration. Verify uncertain evidence stays outside countable rows, and inspect the local reconciliation for duplication and sensitive content without publishing it.
* Controlled reader search: `rg -l -F -e 'evolution_infer.py' -e 'incident-trackers.md' -e 'incident_log_template.md' -e 'coordination-tiers.md' -e 'doctrine/coordination.md' bootstrap/tests scripts tools templates` found the above tests, `bootstrap/tests/test_default_security_stance.py`, `bootstrap/tests/test_onboarding_seed_roster.py`, `scripts/check_cairn.py`, `tools/session.py`, and installed session and onboarding references. The positive `evolution_infer.py` hit validates the search. Run the two additional test files; inspect the remaining references for affected behavior. Search `AGENTS.md` readers separately: `bootstrap/tests/test_review_and_verification_rules_ship.py` and `bootstrap/tests/test_stewardship_rules_ship.py` read its workflow rules; run them and add any relevant reader found when implementing. The manifest and protected roster also match; inspect their ceremony requirements.
* Run `python scripts/claim_check.py` on changed documents, `python scripts/check_cairn.py`, `python scripts/link_check.py`, `python scripts/sync_doc_snippets.py --check` and `python scripts/quality_gate.py --sub neutrality --sub redundancy`. A `snippet:` search found none in the named Markdown surfaces; the checker source contains a positive example, so the whole-tree check remains the standing control. Split pytest selections within the guard limit and reconcile their union.
* Record frozen-file changes for the Maintainer-run ceremony in `bootstrap/REANCHOR_RUNBOOK.md`. Boundary C is independent targeted falsification by the code reviewer.

## Plan review -- Codex gpt-6.1-sol -- 2026-10-30

```
Reviewed commit: 4a8b89056f5d8bbba0db6c0b0e8a1266a51846c2
Target: complete opening plan and accepted proposal
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: ordinary plan review
**Tier**: Internal
**Findings**: raised

**Foundations**:

1. **Should this happen as framed?** The plan carries the accepted human confirmation, serialization, privacy and one-commit counting contract, but its verification mapping still delegates discovery to implementation -- Acceptance criteria C1 and Verification.
2. **Best alternative.** Keep the existing tracker and gate, and finish the reader search and map its results before implementation rather than add an attribution detector -- Scope and `tools/evolution_infer.py::evaluate_tracker`.
3. **What would show it wrong.** A required installed reader or public path omitted from the checks, or one commit producing a threshold finding, would show the plan cannot establish the accepted outcome -- Verification and `templates/modules/default-on/incident_log_template.md` > Incidents.

**P1 -- Blocking: complete the verification mapping before implementation.**
The plan says to search changed paths in tests and manifests and add readers
found, but does not record that search or its results. It also lists test
families without mapping each changed invariant and public path to the actual
checks, and leaves the applicable snippet command unspecified. The template
requires that mapping before implementation so review can assess whether the
checks cover the change. Satisfier: perform the controlled search now, name
readers and installed/public paths found, map each affected behavior to exact
test files or nodes and standing gates, and identify the applicable snippet
command or explain why none applies. Include how occurrence date reaches the
gate's `Date` column, and how the single-commit and two-commit cases are
exercised through the real entry point.

Covered: accepted scope and its failure signals (proposal revised Proposal and
Signals); privacy and human confirmation (C1); serialization and staged bytes
(C1); recurrence and trigger (`tools/evolution_infer.py::parse_incidents` and
`evaluate_tracker`); lifecycle and verification mapping (plan template >
Verification). Not covered: execution of scenarios, independent authorship
confirmation, Security Review, or test runs.

## Plan review -- Codex GPT-6 Security reviewer -- 2026-10-30

```
Reviewed commit: 35515e8c208f35d0dadac418a07c436ef9c461af
Target: complete plan and accepted proposal's revised contract
Prior findings: ordinary P1 considered, not closed
Assurance path: high-assurance
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised

**Foundations**:

1. **Should this happen as framed?** The plan preserves the accepted confirmation, serialization, privacy and event-counting boundaries, but its security checks need the completed mapping requested in ordinary P1 -- Acceptance criteria C1 and Verification.
2. **Best alternative.** Retain human confirmation and the existing advisory gate, completing the check map before implementation; neither claims nor a new detector can establish line authorship -- accepted proposal, revised Proposal and Security preflight; `tools/evolution_infer.py::evaluate_tracker`.
3. **What would show it wrong.** A legitimate integration counted as a sweep, staged foreign content missed, changed bytes signed without reinspection, or one multipath commit meeting recurrence would falsify the intended protection -- C1; `tools/evolution_infer.py::parse_incidents` and `evaluate_tracker`.

**S1 -- Blocking: concur with ordinary P1's incomplete verification map.**
The security contract is explicit, but Verification still postpones discovery
of installed readers and public paths and leaves the snippet check unresolved.
Before implementation, map the confirmation/uncertainty controls, inspection
interval scenarios, grouped event and occurrence-date cases, and both advisory
output formats to exact tests or documented human probes. In particular, name
how uncertain reports stay outside the gate's `occurred` rows and how occurrence
date populates its `Date` column: the current parser consumes those fields,
not confirmation references or discovery dates. Complete ordinary P1's
controlled reader search and standing-gate mapping, including applicable
protected-file ceremony obligations. This is the same missing evidence, not a
request for a second mechanism or reduced scope. The Security obligation stays
open until the author supplies that mapping.

The substantive boundaries are sound. C1 requires author confirmation or
recorded provenance rather than inferred identity; the historical event remains
conditional. Agreement starts before inspection and continues through commit;
claims alone do not suffice, changed bytes are reinspected, and failed agreement
routes work to separate worktrees. Noncooperation remains an explicit limitation.
One row groups all paths per commit, existing rows are checked, occurrence and
discovery dates differ, and uncertain or prevented cases do not count. Minimal
confirmation references stay local; committed summaries exclude sensitive or
unrelated working content. These controls preserve the accepted outcome without
pretending the advisory gate authenticates testimony.

Covered: claims, design and failure limits (C1, accepted preflight S1–S5);
production readers and reuse (commit-pinned search for `evolution_infer` in
`tools`, `templates/modules/default-on` and `bootstrap/tests`, including
`tools/session.py::_run_evolution_infer`); consistency and drift (Scope and
installed gate counterpart); lifecycle and scope (Sequence, doctrine-trigger
fence, Scope delta); satisfier (S1). Not covered / low confidence: no tests,
mutation, concurrency experiment, historical authorship confirmation or local
tracker privacy audit; no scientific result is involved. This is a plan read,
not implementation verification or certification.

## Response to plan reviews -- Codex gpt-6.1-sol -- 2026-10-30

| Finding | Disposition |
|---|---|
| P1 | Accepted. Verification maps the real gate, installed readers, human probes and standing gates; C1 places occurrence date in `Date`. |
| S1 | Accepted. C1 keeps uncertain reports outside countable rows; Verification maps confirmation, inspection and mutation controls. Security obligation remains open for its reviewer. |

## Plan review -- Codex GPT-6 Security reviewer -- 2026-10-30 -- obligation closure

```
Reviewed commit: b934c1650899aed67dd77bc0c398e9ebc1458617
Target: amended C1, Verification and response, solely open Security S1
Prior findings: Security S1; related ordinary P1
Assurance path: high-assurance
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none remaining

**Foundations**:

1. **Should this happen as framed?** Yes. The revised map connects the security controls to real gate tests, installed consumers and documented human probes -- C1 and Verification.
2. **Best alternative.** Keep the existing parser and advisory output, using explicit reporting rules rather than a new authorship detector -- C1; `tools/evolution_infer.py::parse_incidents`.
3. **What would show it wrong.** Uncertain testimony counted as occurred, discovery replacing occurrence date, or a single multipath commit reaching recurrence would contradict named acceptance cases -- C1 and Verification, first and third bullets.

**S1 closed.** C1 now places occurrence date in the existing `Date` column,
records discovery separately, and keeps uncertain reports outside the Incidents
table and never `occurred`. These rules fit what the parser actually reads.
Verification assigns single/multiple commits, prevented and uncertain cases,
dates, both output formats and the controlled mutation to real `main` fixture
tests in `bootstrap/tests/test_evolution_infer.py`. It names the installed
verbatim test and session consumer family, tracker schema and installed
coordination classes, additional readers from a controlled search, and focused
guidance assertions. Staged foreign bytes, intervening changes, legitimate
integration, duplication and privacy remain documented human probes rather
than claims that testimony can be machine-authenticated.

The snippet command is now explicit, alongside claim, prose, link and
neutrality/redundancy gates. The frozen-file obligation remains with the
Maintainer-run ceremony in `bootstrap/REANCHOR_RUNBOOK.md`; this clearance
authorizes neither re-anchoring nor bypassing its HOLDs. The plan identifies
new tests as work to add, not checks already passed. Existing named classes
and the verbatim installed test resolve in the reviewed commit. This closes
the missing plan mapping without reducing scope or claiming implementation
verification. No other part of the plan is reopened.

Covered: S1's reporting semantics, entry-point mapping, installed consumers,
human confirmation/inspection probes and standing checks (C1, Verification;
commit-pinned reads of `bootstrap/tests/test_evolution_infer.py` and
`bootstrap/REANCHOR_RUNBOOK.md`). Not covered / low confidence: no tests or
mutation run, concurrency experiment, historical confirmation or local privacy
audit. Those are implementation evidence still owed; certification was not run.

## Response to Security clearance -- Codex gpt-6.1-sol -- 2026-10-30

S1 is closed. The reviewed plan is ready to implement; the mapped checks and Maintainer-run ceremony remain owed.

## Implementation note -- Codex GPT-6.1 -- 2026-10-30

The proposed historical occurrence is not confirmed by the cited commit in this checkout. `git show --format=fuller --name-status 5094a977` reports only `dev/plans/upgrade-edit-check-no-repository-programs.md` changed, with commit subject `Plan upgrade-edit-check-no-repository-programs: Internal plan review (revising-plan)`. The local `dev/measurement/collision_log.md` records `work-intent-claim-conflict` rows as prevented, and contains no confirmed `same-file-sweep` row. I did not modify that local file or infer authorship. This does not establish the doctrine trigger for editing `doctrine/coordination.md`; that edit is held for Maintainer resolution. The `5094a977` event remains uncertain and is not recorded as occurred. C1 remains open: this checkpoint has no Boundary B record or implementation-verification claim, and no code-review handoff.

## Partial verification note -- Codex GPT-6 -- 2026-10-30

After the Maintainer's fence resolution, doctrine guidance landed at `566acce0`. In a clean detached checkout of that commit, `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13) ran the mapped pytest groups: `TestGateEval`, `TestRegistration` and `test_session_binding_gate_and_printing_hold.py` (58 passed in 2.20s); `test_incident_trackers_module.py`, `test_coordination_broad_intent.py` and `test_intents_tool.py` (147 passed in 10.00s); `test_default_security_stance.py`, `test_onboarding_seed_roster.py`, `test_review_and_verification_rules_ship.py` and `test_stewardship_rules_ship.py` (119 passed in 1.90s). The entire `test_evolution_infer.py` also passed (22 in 0.14s, overlapping the first group). No skips or other non-passes were reported.

Claim checks passed for the seven changed guidance Markdown files. `scripts/check_cairn.py`, `scripts/link_check.py`, `scripts/sync_doc_snippets.py --check`, and `scripts/quality_gate.py --sub neutrality --sub redundancy` passed; external links were not probed. The installed-tool test exercised the scaffold and checked the installed tool's reporting-limit output. A disposable Git repository showed staged and unstaged content in a diff against HEAD, exposed an intervening edit on reinspection, and preserved a separate author's identity when integrating their commit. The checkout stayed clean after these checks. The local tracker remains uncommitted and was not reconciled: the historical occurrence is still unconfirmed. A failed commit attempt automatically added a prevented claim-conflict row, which was preserved.

This is partial evidence, not Boundary B or an implementation-verification claim. Still owed: manual inspection of installed coordination output and remaining reader references, the local tracker's duplication and privacy inspection, and the plan's S3 human-run checks. The frozen `bootstrap/tests/test_evolution_infer.py` and `templates/modules/default-on/evolution_infer.py` require the Maintainer-run gate-manifest ceremony in `bootstrap/REANCHOR_RUNBOOK.md`; no re-anchor is authorized by this note. C1 remains open and there is no code-review handoff.
