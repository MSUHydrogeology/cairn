# Plan: Align the quickstart lifecycle

**Source proposal**: dev/proposals/archive/2026-11-02-codex-quickstart-lifecycle-alignment.md
**Status**: archived
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-02
**In brief**: Correct the quickstart and its sequence test so the example records its final check before archive.

## Source proposal

The Maintainer accepted a light teaching example and a correction to its protected sequence test, with heavy assurance for the test change. The actual one-line tagline normally takes the trivial lane.

## Scope

Revise `docs/quickstart.md` and `bootstrap/tests/test_quickstart_sequence.py`. Preserve the review, Decision, tagline, changelog and clean history checks. No governing rule, gate, baseline or release requirement changes. Stop for reassessment if another protected surface or conflicting requirement proves necessary.

**Reuse.** The existing Step 5 and Step 6 tests construct the disposable lifecycle; searches for `Step 5`, `Step 6`, `archive` and `verification` in those files found the prose and assertions to revise. Extend those checks rather than add a checker.

### Documentation / doctrine surface

The quickstart describes existing practice; no doctrine surface changes. The plan and proposal hold deliberation.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Correct the recipe and existing sequence checks. | Both required plan reviews and author response | Updated example and disposable workflow assertions. |
| C2 | Independent ordinary and Security code reviews, response and final verification. | C1 committed | Review records and wide Boundary B evidence. |

## Acceptance criteria

**C1.** The opening, proposal prompt and Maintainer Decision identify the deliberate example as light and retain the ordinary trivial-lane explanation. The recipe commits implementation, runs the applicable bounded final integration check on that clean commit, records results and omissions in the accepted proposal, then archives in a later commit. Prompts, expected history and explanation agree; no full suite or separate ceremony is introduced. Step 5 and Step 6 exercise this order and retain existing content and lifecycle assertions. A missing or misplaced verification record is rejected by an assertion on constructed history.

**C2.** Independent ordinary and Security code reviews precede passing wide Boundary B. The finished recipe is read cold against installed guidance; its commands and history match the exercised sequence. The surrogate does not claim to execute an adopter's agent.

## Scope delta

**Scope delta**: preserved.

## Verification

Before implementation, map readers and byte pins for both changed files with `python tools/test_tiers.py for docs/quickstart.md bootstrap/tests/test_quickstart_sequence.py` and search, validating negative searches against a known positive. Run the mapped iteration checks, including Step 5 and Step 6, through the real disposable-repository workflow. Demonstrate that omitting or misplacing the verification record fails an assertion on the constructed history; report the mutation and result. This is the proposal's S2/S3 control; it cannot prove the record is truthful or that an adopter ran the recipe.

Run applicable claim, link, snippet and neutrality gates and `python scripts/check_cairn.py`. After independent ordinary and Security code reviews and fixes, run wide Boundary B on a clean unchanged final commit under canonical Python 3.13: mapped iteration and integration/workflow checks, owning families, known public paths and standing gates. Record SHA and range, interpreter, clean pre/post state, commands and counts, elapsed time, non-pass dispositions and omissions. Full certification and baseline work remain separate; do not run a full suite for implementation.

## Plan review -- Codex gpt-6.1-sol -- 2026-11-02

Reviewed commit: 5fca7a821552db1eeb8f63ec7eed54d42a64ba17  
Target: protected sequence assertions, verification order and scope boundary  
Prior findings: none  
Assurance path: high-assurance

**Obligation**: Internal Security Review  
**Tier**: Internal Security Review  
**Findings**: none

**Foundations**

1. **Should this happen as framed?** Yes. The two-file plan delivers the accepted light teaching route while retaining heavy assurance for the protected test. Implementation, checked clean commit, recorded evidence and later archive remain ordered. -- Source proposal, Decision and S1–S5; plan C1/C2; shipped AGENTS.md, Boundary B.
2. **Best alternative.** Extend the existing Step 5/6 disposable workflows, as planned. A prose-only fix leaves assertions endorsing the old order; an additional checker or heavy tagline exercise adds burden without improving this lesson. -- Existing test Step 5/6; proposal Alternatives; plan Reuse.
3. **What would show it wrong?** A missing/misplaced record passing the history assertion, malformed evidence counted as complete, or a recipe requiring full certification. The mutation and cold read target these failures; structural evidence cannot prove truthful adopter execution. -- Plan Verification and C1/C2; proposal S2–S5; test lifecycle-shape sentinel.

**Verdict**: Accept as framed; no blocking findings. Preserve S4's malformed-evidence rejection through the existing content/history assertions rather than adding apparatus. The stop-on-discovery boundary keeps gate manifests, baseline and release requirements outside this implementation's authority.

**Elapsed**: approximately 5 minutes. **Tokens**: unknown.

Coverage: read committed plan, accepted proposal, current plan template, governing verification/archive rules, target prose and tests, protected roster and gate-manifest entries. Did not map all readers/pins, run mutations, exercise installation, compare an anchor or run suites.

## Plan review -- Codex GPT-6 (Reviewer) -- 2026-11-02

Reviewed commit: 4dee6507
Target: scope, sequence, criteria and verification against the accepted proposal
Prior findings: none
Assurance path: high-assurance

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: ACCEPT; the plan delivers the accepted scope. **Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. The plan retains the light example, trivial-lane explanation, verification before archive, existing content checks and independent reviews. -- Accepted proposal, Proposal and Tests required; plan C1–C2.
2. **Best alternative.** Updating only the prose would leave the existing Step 5 and 6 tests endorsing the old order; extending those tests avoids adding a separate checker. -- Proposal Alternatives; committed sequence tests and plan Reuse.
3. **What would show it wrong?** A recipe that archives before verification or a constructed-history assertion that accepts an omitted or misplaced record would defeat the lesson. The plan requires a mutation and cold comparison with installed guidance. -- Plan C1 and Verification; proposal S2–S5.

Coverage: read the committed plan, accepted proposal, Security plan review, template, and relevant quickstart and sequence-test passages. Did not map all readers or pins, run the mutation or tests, or exercise the recipe; those checks remain implementation obligations.

## Response to plan reviews -- Codex GPT-6 -- 2026-11-02

Both reviews accept the plan without blocking findings. The Security review’s advice is accepted: reject malformed evidence through the existing content and history assertions. Reader and pin mapping, mutations, independent code reviews and wide final verification remain implementation obligations.

**Elapsed**: approximately 2 minutes. **Tokens**: unknown.

## Implementation iteration -- Codex gpt-6.1-sol -- 2026-11-02

Implemented C1 in `39b2c9bd400bd24acfd9c30efc7322331e54eb51`, after the
plan transition `69be5fdd`. Interpreter: `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(Python 3.13.13). The tested source was the working tree at those bytes;
unrelated files were concurrently changing, so no clean-tree claim is made.
Elapsed: approximately 7 minutes. Tokens: unknown.

**Reader and pin map.** `test_quickstart_sequence.py` reads the quickstart
and exercises the lifecycle; `test_review_stance_in_shipped_files.py` reads
it for stance wording. `scripts/measurements.py`, the solo-greenfield profile
comment and the installer point readers to the quickstart. `test_tiers.py`
selected the two tests above. The changed test is listed in
`bootstrap/tests/fixtures/gate_manifest.json::frozen_files`: expected SHA
`24902eae743e6a486f8160c72158a73151cf6231a89eab152159759734119e05`, current
SHA `f3a5cdb307f6de3029dd83411c9795cfdf81c8e59ec94a8500dbc738f800a2f4`.
This mismatch is recorded as separate baseline/re-anchor work; no pin or gate
was changed, and no re-anchor was run.

| Command | Result | Elapsed |
|---|---|---:|
| `python tools/test_tiers.py for docs/quickstart.md bootstrap/tests/test_quickstart_sequence.py` | selected the two tests listed below | <1 s |
| `python3.13 -m pytest bootstrap/tests/test_quickstart_sequence.py bootstrap/tests/test_review_stance_in_shipped_files.py -q` | 490 passed | 3.41 s |
| `python3.13 scripts/check_cairn.py docs/quickstart.md` | pass | <1 s |
| `python3.13 scripts/sync_doc_snippets.py --check docs/quickstart.md` | pass | <1 s |
| `python3.13 scripts/quality_gate.py --sub neutrality` | fail=0, info=43 | <1 s |
| `python3.13 scripts/claim_check.py dev/plans/2026-11-02-quickstart-lifecycle-alignment.md` | pass | <1 s |
| `python3.13 scripts/check_cairn.py` | 2 unrelated broken links; quickstart-scoped run passed | 1.2 s |

A separate disposable-repository mutation removed the verification section
while retaining its empty commit; `_assert_verification_order` rejected the
history because the record was absent. `claim_check.py` accepted the plan
before this appended record. The full-tree prose failure is in unchanged
`dev/strategy/archive/2026-10-28-codex-v06-decision-master.md:26` and `:28`, whose
links target `../proposals/2026-11-02-codex-release-test-corrections.md`
and `../proposals/2026-11-02-codex-quickstart-lifecycle-alignment.md`, now
under the archive. The same source and missing targets were present at `HEAD`.

No full suite or wide Boundary B run was performed. Boundary B remains after
independent ordinary and Security code review. The full-tree prose failure
and stale frozen-file hash remain explicit non-pass/omission dispositions for
that review and the Maintainer's separate baseline work.

## Code review -- Codex GPT-6 (Reviewer) -- 2026-11-02

Reviewed commit: 39b2c9bd400bd24acfd9c30efc7322331e54eb51
Target: quickstart and sequence-test changes in 69be5fdd..39b2c9bd; iteration evidence at 1aec801b1418909d149863026df9963c5c41c257
Prior findings: none

**Foundations**

1. **Should this happen as framed?** Yes. The recipe now commits implementation, records the bounded check and archives later; the test inspects proposal contents at both implementation and verification commits. -- `docs/quickstart.md` Step 5; `_assert_verification_order`.
2. **Best alternative.** Reusing the existing disposable lifecycle avoids a separate checker; prose alone would leave its old ordering unchallenged. -- Step 5/6 tests; accepted proposal Alternatives.
3. **What would show it wrong?** Missing or early evidence passing the history assertion, or instructions conflicting with the test, would defeat the lesson. The author's missing-record mutation was rejected; both Step 5/6 nodes passed on a separate copy of the reviewed commit under Python 3.13.13 (2 passed, 1.36 s). -- Implementation iteration; `_assert_verification_order`.

**Bounding**: ACCEPTED for the mapped behavior; final wide Boundary B remains required.
**Findings**: The required full `scripts/check_cairn.py` failed on two stale proposal links, as recorded in iteration evidence. This unmet check keeps work open until corrected and rerun. Nonblocking: Step 5 and Step 6 test docstrings still describe a combined implementation/archive commit and six commits, contradicting the revised test; update those descriptions in the existing test file.
**Verdict**: Changes need the required prose check to pass before completion. **Elapsed**: approximately 4 minutes. **Tokens**: unknown.

Coverage: reviewed committed diff, accepted plan and iteration evidence, recipe and history assertions; ran only the two targeted nodes. Did not independently rerun the mutation, exercise an adopter's agent, compare a historical anchor, or run a suite. The surrogate cannot establish the truth of a verification record.

## Code-review fix evidence -- Codex gpt-6.1-sol -- 2026-11-02

Corrected only the Step 5 and Step 6 test docstrings in
`bootstrap/tests/test_quickstart_sequence.py` at `07c10c3d`. No assertions
or executable behavior changed. Elapsed: approximately 3 minutes. Tokens:
unknown.

Checked a clean local clone at `07c10c3dc872485d9635505168fe7d7f35b2b408`;
`3d5d2af9` is an ancestor. The clone's pre-run and post-run worktrees were
clean.

| Command | Result | Elapsed |
|---|---|---:|
| `python3.13 -m pytest bootstrap/tests/test_quickstart_sequence.py::TestLayerBLifecycleShapeOnly::test_step5_decision_then_implement_and_archive bootstrap/tests/test_quickstart_sequence.py::TestLayerBLifecycleShapeOnly::test_step6_git_log_has_lifecycle_boundaries -q` | 2 passed | 1.31 s |
| `python3.13 scripts/check_cairn.py` | exit 1; one unresolved link, detailed below | 1.4 s |

The repaired decision-master links no longer appear. The one remaining finding
is in concurrent, out-of-scope proposal
`dev/proposals/2026-11-02-codex-security-review-pass-limit.md:17`: unresolved
anchor `../../docs/methodology/dual-review.md#caps-and-closure`. The plan stays
`revising-code` until the required full prose check has no findings. This
single full check was run once as requested; no second run was made. No wider
tests or suite were run.


## Full prose-check follow-up -- Codex gpt-6.1-sol -- 2026-11-02

The finding from review `644363d9` is closed: after the proposal-link
correction at `0b26b13e`, the required full prose check passed. Checked a
clean local clone at `0b26b13ebf0e03b9b26c99469d342a2a305366ac`, which
includes the correction. Pre-run and post-run trees were clean, and `HEAD`
was unchanged. Interpreter: `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(Python 3.13.13). Elapsed: approximately 2 minutes. Tokens: unknown.

| Command | Result | Elapsed |
|---|---|---:|
| `python3.13 scripts/check_cairn.py` | exit 0; 189 Markdown files scanned, 0 issues; 102 external links not probed | 1.2 s |

No test suite or wide Boundary B was run. Independent Security code review
and the plan's final wide Boundary B remain outstanding.

## Code review -- Codex gpt-6.1-sol, Security Review -- 2026-11-02

Reviewed commits: 39b2c9bd400bd24acfd9c30efc7322331e54eb51 and 07c10c3dc872485d9635505168fe7d7f35b2b408  
Target: quickstart implementation and docstring follow-up; evidence through 3a8488bc  
Prior findings: ordinary prose-check finding closed by recorded passing check

**Tier**: Security Review  
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** Yes, but the surrogate Decision still contradicts its revised execution. The recipe correctly selects light and separates implementation, verification and archive; content-at-commit assertions strengthen ordering. -- Quickstart Step 5; `_implement_verify_archive`; `_assert_verification_order`; `_DECISION_TEXT`.
2. **Best alternative.** Align the existing fixture and assertions; no new checker is needed. Preserve the surrogate limitation and lifecycle assertions. -- Accepted C1/C2; test lifecycle-shape sentinel.
3. **What would show it wrong?** A test accepting authority inconsistent with its constructed history. In a clean clone at `07c10c3d`, both Step 5/6 nodes passed under Python 3.13.13 (2 passed, 1.14 seconds) while `_DECISION_TEXT` still ordered implementation/archive in one commit. The clone remained clean. -- Those two nodes and fixture literal.

**S1 — Blocking, accepted C2 consistency.** The fixture quotes “Add the tagline and archive the proposal in one commit,” but the helper creates separate implementation, evidence and archive commits. C2 requires the recipe's commands/history to match the exercised sequence. Align the fixture Decision with the revised light-example authorization and assert its operative content in the existing workflow; rerun the two nodes. This closes the mismatch without widening scope.

**Verdict**: Revise the named inconsistency. **Bounding**: WIDER RUN REQUIRED — existing nodes miss the Decision-content disagreement; extend their assertion before final wide Boundary B. Author-reported missing-record mutation failed as intended; not independently repeated.

**Elapsed**: approximately 4 minutes. **Tokens**: unknown.

Coverage: committed edits, criteria, shipped guidance, iteration/mutation evidence and prose-check follow-up; targeted disposable Git workflow. Did not run suites, verify adopter-agent execution or record truthfulness, compare historical anchors or alter baselines. No reached fence or deviation request in this implementation range.


## Security finding fix evidence -- Codex gpt-6.1-sol -- 2026-11-02

Closed the fixture/content mismatch from Security Review `68df1f21` in
`67bc241555da42bb469fc274eb7a4fbd0ea92aa1`. The surrogate Decision now
states the light tier, permits a separate implementation check and record,
and directs archive in a later commit. The existing Step 5 test asserts that
full operative quotation in the archived proposal. No new checker or
executable behavior was added. Elapsed: approximately 2 minutes. Tokens:
unknown.

Checked a clean local clone at
`67bc241555da42bb469fc274eb7a4fbd0ea92aa1`; it includes link correction
`0b26b13e`. Pre-run and post-run trees were clean; `HEAD` was unchanged.
Interpreter: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python
3.13.13).

| Command | Result | Elapsed |
|---|---|---:|
| `python3.13 -m pytest bootstrap/tests/test_quickstart_sequence.py::TestLayerBLifecycleShapeOnly::test_step5_decision_then_implement_and_archive bootstrap/tests/test_quickstart_sequence.py::TestLayerBLifecycleShapeOnly::test_step6_git_log_has_lifecycle_boundaries -q` | 2 passed | 1.15 s |

No broad tests or wide Boundary B were run. The plan is back at
`awaiting-code-review` for the targeted Security follow-up and final wide
Boundary B.

## Targeted Security follow-up -- Codex gpt-6.1-sol -- 2026-11-02

Reviewed fix: `67bc241555da42bb469fc274eb7a4fbd0ea92aa1`; evidence: `c67e3952a57d3626ba86c10ac1f3d8e011a52758`.

**S1 closed.** The fixture now authorizes the light example's check, recorded evidence and later archive; the existing Step 5 workflow asserts the full operative quotation. This matches the recipe. In a separate copy of the fix commit, restoring only the old Decision fixture failed Step 5 at that new assertion: 1 failed as intended, Python 3.13.13, 0.75 seconds. The author records both unmodified nodes passing on a clean committed copy.

**Verdict**: No new defects found in the targeted fix. **Bounding**: ACCEPTED for this corrected consistency check; final wide Boundary B remains owed. No additional clearing review is needed.

**Elapsed**: approximately 2 minutes. **Tokens**: unknown.

Coverage: fix diff, committed evidence and targeted regression mutation. Did not rerun iteration, suites, broader recipe behavior or historical-anchor checks; the prior Security review's other limits remain.

## Implementation verification -- Codex gpt-6.1-sol -- 2026-11-02

**Boundary B mode**: wide. The quickstart is the front door and its
sequence test owns the disposable end-to-end workflow; C2 requires a cold
read against installed guidance and a wide final check. Ordinary review
`644363d9` and Security review/follow-up `68df1f21` / `9febad81` are closed.
The cold read compared Step 5 and its accepted Decision with installed
`AGENTS.md` lifecycle and Boundary B rules. The helper and Step 6 assertions
match the recipe's separate implementation, verification-record and archive
commits.

- **Tested commit**: `9febad81bdbf2ff810044da3479b166e6cb31c41`
- **Reviewed range**: `69be5fdd3079680d1bb741b58a8e0175364b188e` .. `9febad81bdbf2ff810044da3479b166e6cb31c41`
- **Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` — Python 3.13.13
- **Pre-run state**: clean detached local clone at the tested commit.
- **Post-run state**: clean; `HEAD` unchanged at the tested commit.
- **Elapsed**: approximately 4 minutes for clone, checks and cold read. **Tokens**: unknown.

| Command | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---|
| `python3.13 tools/test_tiers.py for docs/quickstart.md bootstrap/tests/test_quickstart_sequence.py` | 0 | Selected `test_quickstart_sequence.py` and `test_review_stance_in_shipped_files.py` | <1 s | unknown |
| `python3.13 -m pytest bootstrap/tests/test_quickstart_sequence.py bootstrap/tests/test_review_stance_in_shipped_files.py -q` | 0 | 490 passed | 3.70 s | unknown |
| `python3.13 scripts/check_cairn.py` | 0 | 189 Markdown files; 0 issues; includes claim and link checks | 1.4 s | unknown |
| `python3.13 scripts/sync_doc_snippets.py --check docs/quickstart.md` | 0 | 1 document; no drift | <1 s | unknown |
| `python3.13 scripts/quality_gate.py --sub neutrality` | 0 | fail=0, info=43 | 1.03 s | unknown |

**Non-pass disposition**: none. The 102 external links reported by
`check_cairn.py` were not probed. No full suite or tree certification was
run; both remain separate from this change's Boundary B. No tests from the
release-test-corrections plan were run. The test's stale frozen-file hash
remains separately assigned to the Maintainer's v0.6 baseline work; no
re-anchor or pin edit occurred here.

**Plan-specific acceptance checks**: Step 5/6 history and Decision-content
assertions passed in the mapped selection; missing-record mutation and stale
Decision mutation were each rejected as recorded above. No adopter agent was
simulated, and the evidence cannot prove a real agent ran or truthfully
reported its check.

## Dispositions

**Dispositions**: The stale frozen-file SHA for
`bootstrap/tests/test_quickstart_sequence.py` — defer to the v0.6 baseline
list in `dev/PLANNING.md` > “Waiting on you” / “What the v0.6 baseline
must include”. The Maintainer authorized this separate home; the wording
is recorded in `dev/PLANNING.md` > “What the v0.6 baseline must include”:
“They can each build the machinery, the new baseline does not need to be part of their plans. It can be a work board item for v0.6.” No pin refresh or re-anchor was run
for this plan; both remain with the Maintainer's v0.6 baseline ceremony.

## Archive verification -- Codex gpt-6.1-sol -- 2026-11-02

Checked the archive commit `dcf78dad39541dca3058791ee3ecf2c5b93a4625` in a
clean detached clone. Pre-run and post-run worktrees were clean; `HEAD` stayed
at the tested commit. Interpreter: `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(Python 3.13.13). Elapsed: approximately 5 minutes, including the mapped test
selection. Tokens: unknown.

`tools/test_tiers.py for dev/PLANNING.md CHANGELOG.md dev/plans/archive/2026-11-02-quickstart-lifecycle-alignment.md`
selected 22 files. The selection was:
`test_board_json_contract.py`, `test_core_dev_folders.py`,
`test_finalize_retired_living_state.py`, `test_hardening.py`,
`test_install_time_onboarding.py`, `test_intents_tool.py`,
`test_module_merge_lockfile.py`, `test_next_session_local_note.py`,
`test_onboarding_seed_roster.py`, `test_onboarding_slot_substitution.py`,
`test_quickstart_sequence.py`, `test_replacement_tools.py`,
`test_scaffold.py`, `test_scope_reduction_trap.py`,
`test_skills_onboarding.py`, `test_upgrade.py`,
`test_upgrade_edit_check_runs_no_project_programs.py`,
`test_upgrade_lockfile_path_containment.py`,
`test_upgrade_module_additions.py`, `test_verify_integrity.py`,
`test_verify_ref.py` and `test_verify_stems.py`.

| Command | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---|
| `python3.13 -m pytest <the 22 mapped files above> -q` | 0 | 1,167 passed | 154.39 s | unknown |
| `python3.13 scripts/check_cairn.py dev/PLANNING.md CHANGELOG.md dev/plans/archive/2026-11-02-quickstart-lifecycle-alignment.md` | 0 | 3 Markdown files; 0 issues; 8 external links not probed | <1 s | unknown |
| `python3.13 scripts/sync_doc_snippets.py --check dev/PLANNING.md CHANGELOG.md dev/plans/archive/2026-11-02-quickstart-lifecycle-alignment.md` | 0 | 3 documents; no drift | <1 s | unknown |
| `python3.13 scripts/quality_gate.py --sub neutrality` | 0 | fail=0, info=43 | 0.82 s | unknown |
| `python3.13 scripts/claim_check.py --include-archives dev/plans/archive/2026-11-02-quickstart-lifecycle-alignment.md` | 0 | no claim-check flags | <1 s | unknown |

**Non-pass disposition**: none. Per-file timings were not captured, so no
individual file can be named as exceeding the 10-second diagnostic target.
No full suite or tree certification was run. The 8 external links were not
probed. The stale frozen-file hash remains assigned to the v0.6 baseline;
no pin refresh or re-anchor occurred here.
