# Plan: Detect and record same-file sweeps

**Source proposal**: dev/proposals/archive/2026-10-29-codex-same-file-sweeps.md
**Status**: archived
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

## Inspection note -- Codex GPT-6 -- 2026-10-30

At `566acce0`, scaffolded a disposable project with `coordination-tiers` and `incident-trackers` and inspected the installed `dev/modules/coordination-tiers.md`: it states agreement before inspection, staged and unstaged comparison, reinspection, stopping on uncertain content, separate worktrees if agreement fails, and the noncooperation limit. The controlled reader search in Verification also finds onboarding references, legacy and security doctrine citations, the roadmap template, both session copies, schema checker, manifest and roster. Inspection shows onboarding and templates point readers to existing guidance; `scripts/check_cairn.py` checks canonical tracker columns; both session copies run the advisory tool and forward its output. The manifest and roster name the changed frozen tool and test; the Maintainer-run ceremony remains outstanding.

The local tracker has no `same-file-sweep` event-class row and no incident description naming `5094a977`. References to the plan filename are prevented claim conflicts, not sweep confirmations. Its descriptions contain local project paths and agent identifiers, so they remain local and are not reproduced here. No historical row was added: authorship remains unconfirmed. This inspection does not prove the tracker contains no sensitive data of every possible kind.

These inspections complete the remaining agent-executable manual checks identified above. S3 specifies human-run mapped checks and gates; those remain pending, as does the Maintainer-run ceremony. This note does not claim Boundary B, completion or review handoff.

## Sequencing amendment -- Codex GPT-6 -- 2026-10-30

The Maintainer clarified in chat, relayed by the coordinating agent:

> We only repin and reanchor at version cuts or as I ask

> The plan should not require that

Accordingly, earlier statements in this plan that require repinning or
re-anchoring are superseded as plan requirements. Neither ceremony is a
prerequisite for completing or archiving this plan. The new baseline is a
v0.6 board item; repinning and re-anchoring occur at a version cut or when
the Maintainer asks. This amendment does not authorize a ceremony or waive
other checks, reviews, or acceptance criteria. Earlier evidence remains a
record of what was known and done at the time.

## S3 authorization amendment -- Codex GPT-6 -- 2026-10-30

The Maintainer clarified in chat, relayed by the coordinating agent:

> And all of those types of tests are EXACTLY the thing that I am not qualified to do.

S3's requirement that the human run the mapped tests and gates and perform
technical inspection is superseded: capable agents run and interpret those
checks and perform the technical inspections. The same tests, gates and
inspection properties remain required; this changes who performs them, not
what they must establish. Maintainer decisions remain with the Maintainer.
The earlier partial evidence records agent-run checks and inspections; final
Boundary B and independent review remain required.

## Implementation verification -- Codex GPT-6 -- 2026-10-30

**Boundary B mode**: wide. Governing and installed coordination and tracker guidance, both advisory tool copies, their tests, session consumers and onboarding paths are covered by the reviewed mapping; a narrower bound would not cover the cross-surface contract. **Certified by**: pending.

**Tested commit**: `76b5dbccbd3231b992c5daddb403f87e8b6b3d0d`. **Reviewed range**: `86223682d76ca180fed40831ead8f9505d6376f5..76b5dbccbd3231b992c5daddb403f87e8b6b3d0d`; the implementation commits are `1631e59d`, `566acce0`, and `76b5dbcc` within that range, which also includes unrelated work. **Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13. A fresh detached worktree at the tested commit was clean before and after. Prior manual probes and installed-output inspection at `566acce0` remain applicable: the later implementation commit adds only the doctrine assertion.

| Command (Python 3.13.13) | Result | Test-reported time |
|---|---|---|
| `python -m pytest -q bootstrap/tests/test_evolution_infer.py bootstrap/tests/test_session_binding_gate_and_printing_hold.py` | 65 passed | 2.34s |
| `python -m pytest -q bootstrap/tests/test_incident_trackers_module.py bootstrap/tests/test_coordination_broad_intent.py bootstrap/tests/test_intents_tool.py` | 147 passed | 10.25s |
| `python -m pytest -q bootstrap/tests/test_default_security_stance.py bootstrap/tests/test_onboarding_seed_roster.py bootstrap/tests/test_review_and_verification_rules_ship.py bootstrap/tests/test_stewardship_rules_ship.py` | 120 passed | 2.03s |
| `python scripts/claim_check.py <file>` for each of the seven changed guidance Markdown files named in the partial note | all passed | under 1s combined |
| `python scripts/check_cairn.py`; `python scripts/link_check.py`; `python scripts/sync_doc_snippets.py --check`; `python scripts/quality_gate.py --sub neutrality --sub redundancy` | all passed; neutrality and redundancy each had zero failures | timing not captured |

**Non-pass disposition**: no test failures, skips, xfails or xpasses reported. Quality gates reported informational items only. **Plan-specific acceptance commands**: the real gate's control and S2 prevented-impact mutation run in `test_evolution_infer.py`; the installed tool and coordination module, human inspection scenarios, tracker and reader checks are recorded in the preceding notes. **Known omissions**: the proposed historical incident lacks confirmation and was not recorded as occurred; external links were not probed. No full certification was run. `Implementation verified at 76b5dbccbd3231b992c5daddb403f87e8b6b3d0d`; handed to independent code review.

## Code review -- Codex gpt-6.1-sol -- 2026-10-30

```
Reviewed commit: 76b5dbccbd3231b992c5daddb403f87e8b6b3d0d
Target: implementation commits 1631e59d, 566acce0 and 76b5dbcc, and verification record 43391ddb
Prior findings: none
```

**Obligation**: ordinary code review. **Findings**: none. This pass does not clear a separate Security Review obligation.

**Foundations**:

1. **Should this happen as framed?** Yes. The committed rules require serialization and inspection of staged and unstaged candidate bytes; the gate reports its limits. Independent real-entry probes produced the expected one-commit, two-commit, prevented and late-discovery results -- `AGENTS.md` > Shared-file commit inspection; `doctrine/coordination.md`; `tools/evolution_infer.py::main`; falsification ledger below.
2. **Best alternative.** Keep one row per confirmed commit as the human reporting contract and the gate as an advisory row counter; automatic authorship or duplicate detection would add a claim the existing evidence cannot support -- accepted proposal > Proposal; `templates/modules/default-on/incident_log_template.md` > Commit; `tools/evolution_infer.py::evaluate_tracker`.
3. **What would show it wrong.** One multipath row reaching recurrence, an uncertain or prevented report entering the count, a late discovery changing the window, or a missing output limitation would falsify the claim -- falsification ledger below.

**Bounding**: ACCEPTED. The independent probe challenged the gate's real entry point and both reporting formats; its behavior matches the reviewed human reporting contract and the Boundary B record. The duplicate-row case remains a reporter error the gate does not authenticate.

**Falsification ledger**:

* **Surfaces and edge cases.** In an isolated `git archive` of `76b5dbcc`, invoked `tools/evolution_infer.py --root <archive> --trackers dev/measurement/collision_log.md --json` on a synthetic tracker. One confirmed row with two paths plus an `occurred` row outside `## Incidents` gave no finding and one counted row; two distinct confirmed commits gave a count of two; changing the second to `prevented` or dating its occurrence 20 days earlier gave no finding and one counted row. JSON reported `complete: false` in each case. The two-commit case is the positive control for the absent findings.
* **Known boundary.** Two identical `occurred` rows naming one commit gave a count of two. This confirms the gate counts rows, not distinct commit values. The accepted contract assigns duplicate prevention to the reporter and explicitly disclaims automatic confirmation; `incident_log_template.md` says to check for an existing commit row before adding one.
* **Output-path mutations.** Listed both copies from the tree: `tools/evolution_infer.py` and `templates/modules/default-on/evolution_infer.py`. In four fresh archives, changed each copy's human `REPORTING LIMIT` label or JSON `complete` value separately. Direct CLI checks killed all four mutants; the unmutated control above passed. These checks target output visibility, not all parser behavior.
* **Verification and residual risk.** Read the Boundary B mapping and its 65 + 147 + 120 passing-test record at `43391ddb`; did not repeat those suites. Authorship of `5094a977` remains unconfirmed, and a noncooperating writer can change shared bytes after inspection. No full certification, external-link probe, or Security Review was performed here.

**Covered**: claims and production path (`tools/evolution_infer.py::main`, CLI probes); design and fail-closed boundaries (one/two/duplicate/prevented/late rows above); consistency and drift (`git diff 86223682..76b5dbcc` for governing, installed, tracker and gate copies; `git diff --check`); lifecycle and scope (plan C1/C2, accepted proposal > Proposal, Maintainer amendments); satisfier (none required). **Not covered / low confidence**: no live concurrent writers, private author confirmation, whole-tree certification, external links or independent security judgment; those limits do not convert the advisory gate into an attribution detector.

## Code review -- Codex GPT-6 Security reviewer -- 2026-10-30

```text
Reviewed commit: 76b5dbccbd3231b992c5daddb403f87e8b6b3d0d
Target: implementation commits 1631e59d, 566acce0 and 76b5dbcc; verification 43391ddb
Prior findings: none for this code pass
```

**Obligation**: Internal Security Review. **Tier**: Internal Security Review. **Findings**: none.

**Foundations**:

1. **Does it do what it claims?** The guidance requires agreed serialization and inspection, while the gate discloses that it counts reported rows without authenticating evidence; the independent section-boundary probe behaved as claimed -- `doctrine/coordination.md`, `tools/evolution_infer.py::parse_incidents`, and ledger below.
2. **Best alternative.** Retain human confirmation and a transparent advisory row counter; automatic attribution would claim evidence the gate does not have -- `templates/modules/default-on/incident_log_template.md` > Unconfirmed reports and `tools/evolution_infer.py::evaluate_tracker`.
3. **What would show it wrong?** An unconfirmed report counted across the section boundary, a prevented incident producing recurrence, or a hidden reporting limitation would contradict the contract -- falsification ledger below.

**Bounding**: ACCEPTED. The wide Boundary B record maps governing and installed copies, consumers, tests, and manual inspection; its results support the claimed change without asserting certification or provenance authentication.

**Falsification ledger**:

* In a fresh isolated clone checked out at `76b5dbcc`, Python 3.13.13 called `evaluate_tracker` on a synthetic tracker with an `occurred` row under Unconfirmed reports and one in Incidents. It returned no finding. Adding a second incident row produced a count of two; changing that second row to `prevented` removed the finding. The two-row run is the positive control for both negative results.
* `cmp tools/evolution_infer.py templates/modules/default-on/evolution_infer.py` succeeded at the reviewed commit. Read the two output paths and the ordinary review's independent CLI and output mutation ledger; their stated limitations cover unreported rows and unverified confirmation.
* Read the Boundary B record and the manual staged-byte, reinspection and integration evidence. These are human procedures: a noncooperating writer can still race inspection, and duplicate rows or false testimony can inflate counts. The tracker guidance requires checking for a prior row and confirmation; it does not promise machine enforcement.

**Covered**: security boundary and privacy guidance (`incident_log_template.md` > Confirmation Reference); section separation and impact filtering (ledger); copy consistency (`cmp`); review lifecycle and scoped verification (plan amendments and Boundary B). **Not covered / low confidence**: no live adversarial concurrent writer, private confirmation or local tracker contents were independently inspected; no full certification or external links were checked. The historical incident remains unconfirmed.

## Response to code reviews -- Codex GPT-6 -- 2026-10-30

The ordinary review at `9294dd82` and Internal Security Review at `82f441a5` both found no defects and accepted the verification bounding. Both obligations are clear; no revision or further review round is required. The gate counts reported rows rather than authenticating authorship or deduplicating them, and shared-tree serialization depends on cooperation. The historical occurrence remains unconfirmed.

## Dispositions

Dispositions: none. No deferred follow-up remains homed solely in this plan.

**Evidence shipped**: governing and installed guidance, tracker schema and advisory gate copies, scoped tests and the inspection probes recorded above. **Evidence deferred**: none. **Deferred evidence home**: not applicable. Whole-tree certification remains pending and is separate from this plan's known checks; baseline work is on the v0.6 board under the Maintainer's sequencing amendment.

**Fidelity sign-off**: implementation commits `1631e59d`, `566acce0` and `76b5dbcc` deliver the governing revised Proposal in the accepted `dev/proposals/archive/2026-10-29-codex-same-file-sweeps.md` Response, including conditional historical reconciliation, one row per confirmed commit, inspection and advisory reporting. The Maintainer's recorded plan amendments resolve the doctrine gate and technical-check ownership without asserting an unconfirmed incident.
