# Plan: Remove the collaboration agreement

**Source proposal**: `dev/proposals/archive/2026-10-19-claude-remove-collaboration-agreement.md`
**Status**: archived
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-19
**In brief**: Cairn will stop installing its collaboration agreement while keeping each project's copy and the team guidance that still matters.
**Assurance path**: high-assurance

## Source proposal

Revision 1 and the Decision in the source proposal are the contract. The
Maintainer accepted four answers: an upgrade reports `removed-upstream` and
keeps a project's copy; the roster and second-agent prompt survive while the
signing prompt retires; Cairn alone keeps its finite decision list while the
shipped roles document keeps the agreement's two existing sentences; and this
plan opens now but implementation waits for `review-stance-and-lenses` to
archive. The Security and Internal reviews found the unsafe deletion advice,
the opposite rules for uncertain agents, and tests that would pass vacuously;
Revision 1 accounts for each. The engine and install contract are high-risk
surfaces under `AGENTS.md`, so this plan needs both the usual Internal plan
review and a separate Internal Security Review.

## Scope

* Retire `templates/core/dev/collaboration_agreement.md` and Cairn's
  `dev/collaboration_agreement.md`. Remove their install row from
  `bootstrap/_scaffold/config.py`. Keep the old destination in
  `_LIVING_STATE_DSTS` in `bootstrap/_scaffold/lockfile.py` for existing
  projects, with a comment saying it must not become a shipped file again.
  Leave Cairn's existing `dev/.cairn/cairn-lock.yml` record in place; do not
  hand-edit a tool-owned lockfile. Existing projects keep their file, lock
  record and cached base. The installer, upgrade planner and lockfile schema
  get no new behavior.
* Put the roster in a separate **The team** section in both copies of
  `dev/agent_collaboration.md`. The shipped copy receives the same
  `team-roster` markers and default text as the shipped agreement. Cairn's
  copy carries its current roster in plain text, with the two now-inaccurate
  sentences reworded. Move Cairn's finite-list paragraph, word for word, to
  the start of its **Surfacing judgment calls to the Maintainer** section and
  conform the paragraph after it. In the shipped roles document, preserve
  these two sentences from the shipped agreement, word for word:

  > Agents propose, review, implement, and advise; they do not decide.

  > Acceptance, rejection, and supersession are the Maintainer's call. An agent unsure whether something is a decision surfaces it rather than assuming.

  Do not ship Cairn's finite-list rule. Leave `doctrine/lifecycle.md` alone;
  its different escalation guidance has a deferred board home.
* Retire `collab-agreement-signing` from the registry and trigger evaluator
  in `scripts/_onboarding/{prompts,triggers}.py` and their byte-identical
  `templates/modules/default-on/_onboarding/` twins. Keep
  `second-agent-type`, pointing its contained roster read at the moved slot.
  Remove the signing prompt and its solo seed task from all three
  `templates/onboarding/` presets. Retarget the collaborative and legacy seed
  tasks. Update the installed collaborative preset in
  `dev/modules/onboarding/` and the team tour in both
  `docs/agent-team-onboarding.md` and its installed copy. Keep the trigger's
  `log_records` argument for existing callers.
* Remove live pointers to the retired path and ritual in the `AGENTS.md`
  pair, four proposal/plan template copies, `doctrine/dual-review.md`,
  `doctrine/onboarding.md`, the `dev/README.md` pair,
  `docs/DOCUMENTATION_PLAN.md` and its installed template,
  `templates/optional/CONTRIBUTING.md`, `bootstrap/BOOTSTRAP.md`,
  `bootstrap/fidelity-check.md`, both `dev/measurement/README.md` copies,
  and `dev/measurement/queued-issue-drafts.md`. Write the adopter advice in
  `bootstrap/UPGRADE.md`: empty a no-longer-needed project copy rather than
  delete it; explain the repeating report line, the old README pointer, the
  moved roster, the integrity warning and scoped finalize. Add a changelog
  entry. Remove the template-specific entry from
  `dev/.cairn/claim-check-allow.json`, retaining exemptions for history.
* Update owning tests, including the review-stance test that pins the old
  roster sentence. Add `bootstrap/tests/test_agreement_retired.py` for fresh installs,
  upgrade preservation, finalize behavior, roster attestation and the
  surviving second-agent prompt. Historical proposals, case studies and old
  changelog entries remain historical. Removing an orphan lock record or
  changing `upgrade --finalize` is outside this Decision.

Proposed paths:
* `bootstrap/tests/test_agreement_retired.py` — focused install and upgrade contract tests.

### Search and current-tree accounting

At parent `6c8b8effa5085690225276d32696398b89e59390`, I searched the tracked tree with `git grep -IlEi` for
`collaboration[_ -]agreement|collab[_-]agreement|sign-collab|team-roster|External Review Norms`
(68 files, including historical records), then used `rg -n` for
`_CORE_MAPPINGS`, `collab-agreement-signing`, both `sign-collab-agreement`
seed ids, `signature log`, `signed agreement`, `working agreement`, `review
compact`, and the whole word `agreement` to catch wrapped names and
paraphrases. I checked the known positive controls in the template, the
installer mapping and the trigger before treating an absence as evidence.
I searched `bootstrap/tests/` for the paths, trigger and seed ids,
`_CORE_MAPPINGS`, `removed-upstream`, `_LIVING_STATE_DSTS` and the preset
names, and opened the readers rather than relying on filename matches. The
current public manifest has 97 data rows plus its header; its agreement row
must be the sole removal. `review-stance-and-lenses` is now
`awaiting-code-review`, `model-mapping-install-path` is
`ready-to-implement`, and `board-as-basis` is implementing; re-read their
shared files just before each edit. The source proposal's old 0.3 search
counts, AST figures and claim-check baseline are measurements at earlier
commits, not acceptance pins. Its opening's six roster-sentence copies were
superseded by seven in Revision 1. Its initial full-per-change Boundary B
recipe was superseded by `AGENTS.md`'s certifying-run rule.

### Documentation / doctrine surface

The governing layer is the `AGENTS.md` pair, roles-document pair, four
authoring templates and one sentence in `doctrine/dual-review.md`. The
onboarding doctrine describes the surviving prompt. The adopter description
is the README, onboarding, bootstrap and upgrade guidance above. The plan,
board and changelog are deliberation or release records. This follows the
placement rule in `docs/DOCUMENTATION_PLAN.md`. No new doctrine rule is
introduced; `doctrine/lifecycle.md` is deliberately deferred.

### Frozen files and engine symbols handed to the 0.4 ceremony

I intersected the planned changes with the actual `frozen_files` keys in
`bootstrap/tests/fixtures/gate_manifest.json`. These **nine existing frozen
files** change; none is deleted:

* `templates/modules/default-on/_onboarding/prompts.py`
* `templates/modules/default-on/_onboarding/triggers.py`
* `bootstrap/tests/test_active_surfacing_mechanism.py`
* `bootstrap/tests/test_active_surfacing_render.py`
* `bootstrap/tests/test_core_dev_folders.py`
* `bootstrap/tests/test_notice_install.py`
* `bootstrap/tests/test_onboarding_seed_roster.py`
* `bootstrap/tests/test_quickstart_sequence.py`
* `bootstrap/tests/test_trigger_evaluation_action.py`

`bootstrap/tests/test_review_stance_in_shipped_files.py` is edited but is not
an existing `frozen_files` key; the new retirement test will be newly
collected at the ceremony. The engine edit changes the top-level assignment
`_CORE_MAPPINGS` only. **Top-level `bootstrap/_scaffold/` functions expected
to change: none.** The `lockfile.py` edit is comment-only. The implementer
records its own diff for each of the nine frozen files and `config.py`; an
overlapping pre-existing `FROZEN-MODIFIED` line cannot identify these bytes.
The gate manifest and AST baseline are Maintainer-only and re-anchored once
at the 0.4 cut. This plan has no re-anchor chunk, and no agent updates either
fixture or pre-fills its digests. The prior review-stance blob record for
`test_review_stance_in_shipped_files.py` will be superseded by that file's
final blob at code review; the ceremony derives the actual set then.

## Sequence

**Start fence — MAINTAINER-GATED by the accepted Decision:** no implementation
chunk starts until `dev/plans/review-stance-and-lenses.md` has Status
`archived`. The Decision supplies the authorization; the status is the
condition, not a request for fresh approval. This plan must land before
`dev/plans/model-mapping-install-path.md` starts C2. If that ordering is lost,
stop and resolve the collision before editing shared files. Plan review may
proceed while the archive is pending.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Preserve the rules and move the roster into **The team**. Reword the seven roster pointers and the stance-test pin. | Both plan-review obligations clear; start fence; re-read the roles documents, templates and stance test. | One explicit-path commit; old agreement still present. |
| C2 | Retire the signing prompt and task; move the roster reader and onboarding guidance. Keep the two helper twins and the tour twins equal. Repair the prompt, trigger and seed tests in the same commit. | C1; re-read the presets and any `board-as-basis` or model-mapping edits. | One explicit-path commit; old agreement still present. |
| C3 | Delete the template and Cairn copy, remove the install row, close remaining live citations, write upgrade guidance and changelog, change tests and claim allowance. | C2; the row and template leave in the same commit. | One explicit-path commit with the new retirement test; installer and docs agree. |
| C4 | Run the mapped checks and contract smokes on the committed result; append the evidence and move Status to `awaiting-code-review`. | C3; no new implementation bytes after the measured commit. | One explicit-path plan commit; `**Certified by**: pending`. |

No chunk performs the AST or gate-manifest re-anchor. At archive, close the
old queued removal row and the duplicated onboarding seed on the board at
its prescribed serialization point.

## Acceptance criteria

* **C1:** Cairn's finite list appears in its roles document, ahead of the
  recommendation paragraph, with the original rule's words intact. The
  shipped roles document contains both quoted sentences above exactly and
  none of Cairn's finite-list text. Both have a distinct **The team** section;
  the shipped slot retains its marker names and default text. The current
  stance test fails if the roster sentence still names the retired path or if
  the shipped section is counted as extra team roles.
* **C2:** Both shipped helper files remain byte-identical to their `scripts/`
  twins, and the two tour files remain byte-identical. A filled two-agent
  roster fires `second-agent-type`; an unfilled, missing or doubled-opening
  roster does not. No prompt row or task still invokes
  `collab-agreement-signing`, and the activation registry is nonempty. The
  idempotency test first proves the surviving prompt fires, then proves it
  does not fire again; removing the already-emitted check must make its
  `activate()` test fail. The cap test has more than three candidates before
  asserting a cap of three; the distinct-body test has two rows, one a
  stand-in, and can fail on a duplicated body. The three presets retain
  distinct second-agent text.
* **C3:** Compared with the C2 commit, `scaffold.py --manifest` loses exactly
  the agreement row and no other row. A fresh install of each preset has no
  agreement file or lock record, retains `dev/agent_collaboration.md`, and
  passes integrity verification. A project with an old agreement reports
  exactly one `removed-upstream` line; plan, stage and apply leave its file,
  record and cached base bytes unchanged. The path remains literally in
  `_LIVING_STATE_DSTS` but in no install mapping. Deleting an old copy makes
  bare finalize refuse; emptying it lets bare finalize pass. Filling the
  moved roster first raises the expected integrity warning, then scoped
  finalize clears it and the second-agent prompt can fire. An injected
  retired-path citation into a scanned install surface must make the citation
  test fail. `check_cairn.py` has no new live-reference flags relative to C2.
* **C4:** The record names the tested commit, interpreter, clean pre/post
  state, commands, outcomes, elapsed time, non-pass disposition and omissions.
  It lists the diff for each frozen file, the engine assignment and any
  collection changes for the Maintainer's 0.4 ceremony. No full-suite result
  is claimed from this change's scoped run.

The accepted proposal's scientific-check answer is N/A: no scientific
assumption or result changes. Chunking changes the security preflight's S2
and S3 triggers: the named tests, contract smokes and controlled breaks above
run by the implementer on the clean result; the full suite runs only at the
next certifying point. S1 (project-supplied roster and lock record), S4
(missing roster suppresses a prompt; dropped exemption alarms), and S5 (the
retired path remains an enumerated integrity blind spot) remain as answered
in Revision 1. The Internal Security Review must challenge the contained
roster read, `removed-upstream` preservation and literal no-reuse pin.

## Scope delta

**Scope delta**: degraded, one accepted unit. The Decision authorizes
Cairn-only retention of the finite list and defers shipping it to adopters;
the shipped agreement's older two sentences are preserved instead. This is
the Decision's Q3, not a new cut by this plan. **Disposition**: defer; any
future adoption of Cairn's different unsure-case rule needs its own proposal.
The separate `doctrine/lifecycle.md` wording is also left for the registered
deferred row. No other accepted outcome is dropped.

## Verification

**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(confirm its 3.13.x version in the implementation record).
**Boundary B mode**: full is required because the install contract and scaffold
engine change, but the full suite belongs only to the next certifying run.
**Boundary B execution**: scoped to the reviewed mapping below, on a clean
unchanged final commit.
**Certified by**: pending

**Boundary A (iteration, scoped).** Run the owning tests for each chunk. The
reader search above produced this mapping; re-search at implementation time
for tests added meanwhile:

| Changed surface | Owning tests and checks |
|---|---|
| Rules, roster, authoring templates, shipped docs | `test_review_stance_in_shipped_files.py`, `test_scope_reduction_trap.py`, `test_review_and_verification_rules_ship.py`, `test_review_sweep_ships.py`, `test_core_dev_folders.py`; `scripts/check_cairn.py`, `scripts/link_check.py`, `scripts/claim_check.py` for each authored document, and `scripts/sync_doc_snippets.py --check` for edited Markdown. |
| Prompt registry, roster reader and activation | `test_trigger_evaluation_action.py`, `test_active_surfacing_mechanism.py`, `test_active_surfacing_render.py`, `test_onboarding_seed_roster.py`, `test_onboarding_slot_substitution.py`, `test_skills_onboarding.py`, `test_presets.py`, `test_profiles_smoke.py`; compare each exact helper twin. |
| Install mapping, manifest and fresh installs | `test_notice_install.py`, `test_quickstart_sequence.py`, `test_manifest.py`, `test_config_module.py`, `test_scaffold.py`, `test_lockfile_module.py`, `test_verify_integrity.py`, `test_security_capability_install.py`, and the new `test_agreement_retired.py`. |
| Old projects and upgrade guidance | `test_upgrade.py`, `test_upgrade_module_additions.py`, `test_claim_check_allow_config.py`, and the new `test_agreement_retired.py`; check the upgrade note against the tested finalize behavior. |

**Boundary B (integration).** On the final committed tree, run the mapped
test files above with the canonical interpreter, then
`python scripts/quality_gate.py --sub neutrality --sub redundancy`. Run
`python scripts/check_cairn.py` and the document checks on the edited
documents; use explicit paths where its default search excludes one. Compare
the manifest to the C2 commit, and run scratch installs and an upgrade of a
scratch old project through plan, stage, apply and integrity verification.
Run the controlled breaks in separate scratch copies beside an unmodified
control: remove the already-emitted guard; remove the living-state exemption;
make apply delete the old file; restore the install mapping; inject a retired
citation. Record each as killed, survived or equivalent. The implementer
records `**Certified by**: pending` until a later clean-tree certifying run
covers this commit. The implementer never sets the full-suite switch for
this change.

Append `## Implementation verification -- <agent> -- YYYY-MM-DD` only after
the scoped stable run: tested SHA and reviewed range, canonical interpreter,
clean pre/post state, commands and counts, timing, non-pass disposition,
known omissions, the mutation ledger, and the frozen-file/engine-symbol
handoff. The AST and gate-manifest fixtures are not changed here.

**Boundary C (falsification)** belongs to a fresh code reviewer. The
reviewer checks the record against the implementation range and attacks
the highest-risk claims independently, including an upgrade that keeps a
project's old copy and the copied roster's integrity transition. A finding
that changes implementation or tests invalidates the scoped record and
requires another scoped Boundary B after the repair. The full suite still
waits for a certifying point.

## Dispositions

At archive preparation, record a `Dispositions:` line for every follow-up
and check its live board home. The Q3 adopter-rule deferral and the distinct
`doctrine/lifecycle.md` wording have homes in `dev/PLANNING.md`; neither is
silently treated as implemented. The existing project's repeating
`removed-upstream` line is accepted behavior under Q1. Archive only after
code review and the board/changelog serialization, without performing a
re-anchor in this plan.

## Plan review -- Codex (Internal, fresh session) -- 2026-10-19

```
Reviewed commit: 013ae14893e87b42769279533944e03d59085705
Target: the complete plan against the accepted proposal's Revision 1 and Decision, and the committed implementation/document/test surfaces
Prior findings: none; read CA1-CA6, CA-SR1-CA-SR7 and the author's Response as source requirements, not findings being cleared by this pass
Assurance path: high-assurance
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised
**Verdict**: REVISE

**Foundations**:

1. **Should this happen as framed?** The design delivers all four Decision answers: report and preserve the old copy, retain roster and second-agent prompt, preserve the two adopter sentences while keeping Cairn's list local, and wait for the review-stance archive before landing ahead of model-mapping C2. Correct the lifecycle omission before implementation -- source proposal, Decision Q1-Q4; this plan, Scope and Sequence; `dev/plans/_template.md:18`.
2. **Best alternative.** Keep the three implementation chunks and existing report-only upgrade mechanism; add the missing verification and explicit archive handoff rather than new deletion or lock-release behavior -- `bootstrap/_scaffold/upgrade.py`, `_ADVANCING_KINDS`, `_compute_upgrade` and `_apply_upgrade`; this plan, C1-C4.
3. **What would show it wrong.** Losing an old project's file, reversing adopters' unsure-case rule, or allowing the ceremony to freeze a test without the promised replacement blob would contradict the accepted contract -- source proposal, Revision 1 steps 3-5 and "What the cut will show"; `dev/PLANNING.md`, agreement-removal Joined paragraph.

The strongest part of this plan is its restraint: remove a delivery row while
preserving project-owned governance, and move the unique words before deleting
their home. The two-sentence adopter rule and Cairn-only list are deliberately
different, as the Decision requires. The anti-vacuity criteria for idempotency,
the task cap and rendered bodies answer the proposal reviews concretely.

### CA-PR1 -- Medium, blocking -- Archive the accepted source proposal

The opening commit changes only this plan and `dev/PLANNING.md` (`git show
--stat 013ae148`). Its source remains at the active proposal path with Status
`accepted`; the plan also points there. The template requires opening a plan
to archive its source in the same commit (`dev/plans/_template.md:18`). The
missed transition leaves two active lifecycle records for the same work and
is not an authorized exception to that rule.

**Satisfier:** correct the source-proposal archive in a separate lifecycle
correction commit before implementation, preserving its prior sections and
updating live references, including this plan's Source proposal line. Record
that it repairs the missed opening transition; do not rewrite the opening
commit or change the Decision. This review itself appends only to the plan.

### CA-PR2 -- Low, non-blocking -- Make the replacement-blob handoff executable as an archive task

The plan says the old blob record "will be superseded" at code review, and
C4 asks for frozen-file diffs and collection changes, but its archive
instruction only closes the removal row and onboarding seed. Revision 1's
"The blob-id record" specifically requires the re-anchor board paragraph to
carry the new blob id and say it replaces the earlier one. The existing
Joined paragraph on `dev/PLANNING.md` promises replacement but contains no
final blob. The predecessor's M row likewise asks the ceremony to confirm
exact bytes (`dev/plans/review-stance-and-lenses.md:431`). The source contract
still binds; make its final action explicit so it is not lost at archive.

**Satisfier:** add an archive criterion to obtain the test's blob with
`git ls-tree <code-reviewed-commit> -- bootstrap/tests/test_review_stance_in_shipped_files.py`,
put that id and commit in the existing Joined paragraph, and state that it
replaces the predecessor's record for this file only. This records evidence;
it does not perform either re-anchor.

### CA-PR3 -- Low, non-blocking -- Put the final changelog entry at archive

C3 currently writes the changelog, while Dispositions refers generally to
board/changelog serialization. `AGENTS.md` limits shared communication edits
to serialization points, and `dev/plans/_template.md`, Dispositions, says the
archive commit writes its own changelog entry. Revision 1 requires an entry
but does not require it in C3.

**Satisfier:** keep the upgrade guide in C3 and assign the final changelog
entry explicitly to the archive commit, beside the board cleanup and blob
handoff. No accepted output is removed.

### CA-PR4 -- Medium, blocking -- Complete the document-reader mapping

The scoped run in Verification is narrower than the actual readers of the
changed governing documents. For example, the committed
`bootstrap/tests/test_documentation_plan_module.py` reads both the shipped
documentation-plan template and `docs/DOCUMENTATION_PLAN.md`, while
`bootstrap/tests/test_comprehension_floor.py` and
`bootstrap/tests/test_verification_boundaries.py` read the `AGENTS.md` pair.
`bootstrap/tests/test_scientific_check_guidance_ships.py` reads all four
authoring templates. None appears in this plan's mapping, although the
source proposal's Revision 1 measurement N7 already names all four.
Passing them on an earlier prototype does not verify the final bytes.

**Satisfier:** add those owning test files or the exact nodes that read the
touched surfaces to Boundary A and the scoped stable run. Re-run the reader
search over the full touched-file list before the fold, distinguishing real
repository readers from tests that only construct similarly named scratch
fixtures. Keep the certifying run pending; this finding asks for the missing
scoped owners, not a full suite.

**Coverage -- Covered:** claims and drift (#1, #6): the committed search
`git grep -n -i -E 'collaboration[_ -]agreement|collab[_-]agreement|sign-collab|team-roster|External Review Norms' 013ae148`
finds the mapping, template and trigger as positive controls, then the live
surfaces listed in Scope; no additional live retirement surface was found
in that search. Production-path coverage and completeness (#2, #3):
`bootstrap/tests/test_manifest.py::TestInstallManifest::test_manifest_matches_actual_install`,
`bootstrap/tests/test_trigger_evaluation_action.py::TestSecondAgentTypeTrigger`,
and C2-C3's proposed controls. Fail-closed (#4): the separate Security Review
below examines the reader and verifier. Cross-document consistency and
lifecycle (#5, #7): Decision Q1-Q4, the plan template's source-archive rule,
the predecessor's M row, and the model-mapping plan's C2 write set. Scope and
domain (#8): the two decision-rights deferrals have a live home in
`dev/PLANNING.md`, "Decision-rights questions left by the agreement removal";
scientific validity is N/A because no result or method changes. Satisfiers
(#9): each finding above names its closing artifact/action.
**Not covered / low confidence:** no implementation exists to execute; no
suite, mutation, install, real-project upgrade, or ceremony was run for this
plan review. The earlier proposal prototypes remain their authors' evidence.
Later commits through `4f08957d` add review records and board-as-basis evidence;
`git diff 013ae148 HEAD -- dev/plans/remove-collaboration-agreement.md` was empty
before this append. Other sessions' work was left alone.

## Plan review -- Codex (Internal Security Review, fresh session) -- 2026-10-19

```
Reviewed commit: 013ae14893e87b42769279533944e03d59085705
Target: the contained roster read, retired-path integrity policy, report-only upgrade preservation, adopter authority wording, and security verification mapping
Prior findings: none; CA-SR1-CA-SR7 are accepted source requirements, not a second proposal-review round
Assurance path: high-assurance
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE

**Foundations**:

1. **Should this happen as framed?** The trust boundaries are sound as planned: retain the literal retired exemption without granting the roles document one, keep removals report-only, and preserve adopters' unsure-case sentence. The mapped checks do not yet cover the changed reader's containment call or the standing scan -- `bootstrap/_scaffold/lockfile.py`, `_LIVING_STATE_DSTS`; `bootstrap/verify_integrity.py`, living-state branch; this plan, Verification.
2. **Best alternative.** Preserve the existing containment primitive and add direct reader refusals plus the existing static gate to the scoped mapping; no new parser, exemption or upgrade operation is needed -- `scripts/_onboarding/triggers.py:134`; `scripts/_onboarding/security.py:117`; `bootstrap/tests/test_security_lint.py::test_no_blocking_security_findings`.
3. **What would show it wrong.** A symlinked roster being consumed, a restored mapping inheriting the retired exemption, or an apply modifying the old file would break the stated security boundaries; map the first alongside the already-planned literal no-reuse and destructive-apply controls -- this plan, C3 acceptance and Boundary B controlled breaks; `bootstrap/tests/test_onboarding_activation_helper.py::TestContainmentGuards`.

This is a separate security pass by the same fresh reviewer. The repository
requires separate passes with matching Obligation lines; it does not require
different people or agent sessions for the two lenses (`AGENTS.md`, Review;
`dev/agent_collaboration.md`, Team roles). Neither pass is attributed to the
plan author or treated as a Maintainer-called External read.

### CA-PS1 -- Medium, blocking -- Test containment through the moved roster reader

The reader currently checks `_assert_safe_read` immediately before reading
the roster (`scripts/_onboarding/triggers.py:140`). Its guard rejects both a
symlinked leaf and a symlinked parent (`scripts/_onboarding/security.py:127`).
The plan moves that read and promises containment, but C2 only specifies
ordinary, missing, unfilled and doubled-marker rosters. Its mapping omits
`bootstrap/tests/test_onboarding_activation_helper.py`; that file's existing
`TestContainmentGuards` tests call the guard directly, so even adding those
tests would not catch a reader that forgot to call it. The mapped
`TestSecondAgentTypeTrigger` fixtures write ordinary files. This is a
verification gap, not evidence of an implemented vulnerability.

**Satisfier:** in the already-edited trigger test file, add cases through
`evaluate_action_triggers` for a symlinked `dev/agent_collaboration.md` and
for a symlinked `dev/`, with a real two-agent roster as the ordinary-file
control. Require `OnboardingSecurityError` before roster content is read,
rather than accepting an empty trigger set. Map these cases and the existing
guard tests into C2 and Boundary B. A targeted removal of this reader's guard
call should fail the new cases; run that controlled break in a separate copy,
beside its control. This preserves the current guard rather than enlarging
the implementation.

### CA-PS2 -- Medium, blocking -- Include the standing Bandit gate

The plan edits the scaffold package and both shipped onboarding helpers,
but its mapping and Boundary B command list contain only the neutrality and
redundancy static legs. Neither dispatches Bandit (`scripts/quality_gate.py`,
`_SUB_GATES` and `run_gates`). The existing owner is
`bootstrap/tests/test_security_lint.py::test_no_blocking_security_findings`;
its `_run_bandit` scans the targets from `bootstrap/security_check.py::scan_targets`,
which explicitly includes the whole scaffold package and the always-on
onboarding engine. `AGENTS.md`, Verification boundaries A, requires standing
gates for every touched surface. Deferring the full certifying suite does
not defer this applicable scoped gate.

**Satisfier:** add that exact pytest node (or an equivalent direct scan with
the same target, severity and allowlist semantics) to the reviewed mapping
and scoped stable run under the canonical interpreter. Record any missing
Bandit skip as a non-pass with its disposition. Do not run the release
orchestrator or set the full-suite switch to satisfy this finding.

**Coverage -- Covered:** claims and production paths (#1, #2):
`bootstrap/_scaffold/upgrade.py`, `_ADVANCING_KINDS` excludes removals,
`_compute_upgrade` emits `removed-upstream` for absent upstream sources, and
stage/apply select advancing kinds; the new contract test must pin file,
record and cached-base bytes. Completeness and fail-closed (#3, #4):
`scripts/_onboarding/triggers.py`, `_read_team_roster_body` and the guard in
`security.py`; `bootstrap/verify_integrity.py` skips only enumerated
living-state destinations; `_cmd_finalize_lockfile` checks missing files
before its living-state skip, supporting the keep-or-empty advice.
Consistency and drift (#5, #6): the shipped agreement's two sentences versus
Revision 1 steps 4-5 and C1; the upgrade note must retain the source's own-tree
search, README pointer loss and scoped-finalize guidance. Lifecycle and
scope (#7, #8): C1 waits for the predecessor archive, the whole change lands
before model-mapping C2, and fixtures remain Maintainer-only; no scientific
or credential behavior is added. Satisfiers (#9): CA-PS1 and CA-PS2 name the
precise checks that close them.
**Not covered / low confidence:** no future implementation or security
mutation was executed; no full suite, external project, AST baseline or
gate-manifest fixture was changed or re-anchored. The existing roster parser
is heuristic and reads the whole file; this plan does not claim to solve
those pre-existing limits. Both required plan-review passes are recorded;
their findings await the author's fold and response, without a second
plan-review round.

## Operative amendments after plan review -- Codex -- 2026-10-19

These amendments supersede only the named sentences in the earlier Scope,
Sequence, Acceptance criteria, Verification and Dispositions cells. The
earlier cells and both review passes remain intact as the record. No chunk
starts until the review-stance plan is `archived`, and this work still precedes
model-mapping C2.

* **Source and C3:** The source proposal was moved, unchanged, to the archive
  in correction commit `da6cc466`, repairing the missed opening transition.
  C3 still writes `bootstrap/UPGRADE.md` and its tests, but does **not** edit
  `CHANGELOG.md`. The final changelog entry belongs to the archive commit.
* **C2 containment:** Add tests to
  `bootstrap/tests/test_trigger_evaluation_action.py` that call the real
  `evaluate_action_triggers` with an ordinary filled two-agent roster as a
  control, a symlinked `dev/agent_collaboration.md` leaf, and a symlinked
  `dev/` parent. Each symlink case must raise `OnboardingSecurityError`
  before roster content is read; an empty fired set is not acceptance.
  Run the existing
  `test_onboarding_activation_helper.py::TestContainmentGuards` tests too.
  In a separate copy beside an unmodified control, remove this reader's
  `_assert_safe_read` call and show that the two new cases fail.
* **C4 document-reader map:** The first Verification row and Boundary B's
  reference to it additionally include the real-file readers
  `test_documentation_plan_module.py`, `test_comprehension_floor.py`,
  `test_verification_boundaries.py`,
  `test_scientific_check_guidance_ships.py`, `test_certifying_run_rule.py`,
  and `test_doc_governance.py`. They read, respectively, the edited
  documentation-plan pair and governing/template surfaces; the AGENTS pair;
  the AGENTS and authoring-template pairs; the authoring-template pair and
  bootstrap guide; the AGENTS and plan-template pair plus dual-review
  doctrine; and the shipped dev README. The earlier mapping already includes
  the real readers `test_review_stance_in_shipped_files.py`,
  `test_scope_reduction_trap.py`, `test_review_and_verification_rules_ship.py`,
  `test_review_sweep_ships.py` and `test_scaffold.py`. Re-search at
  implementation time for additions. Tests such as
  `test_claim_check_module.py` and `test_loop_fidelity_gate.py` that write
  similarly named scratch files, without reading the corresponding repo
  documents, are not document-reader owners; the claim checker itself still
  runs on every authored document.
* **C4 security gate:** The onboarding/engine Verification row and Boundary B
  additionally include
  `bootstrap/tests/test_security_lint.py::test_no_blocking_security_findings`.
  It runs Bandit over the scaffold and always-on onboarding targets through
  the repository's severity and allowlist policy; neutrality and redundancy
  do not run it. A missing-Bandit skip is a non-pass to record and resolve,
  not a clean gate result. Keep the full certifying suite pending and never
  set its override for this change.
* **Archive handoff:** At archive, after code review, obtain the final blob
  of `bootstrap/tests/test_review_stance_in_shipped_files.py` with
  `git ls-tree <code-reviewed-commit> -- bootstrap/tests/test_review_stance_in_shipped_files.py`.
  Put the blob and commit into the existing Joined paragraph under
  **Re-anchor the gate manifest** in `dev/PLANNING.md`, stating that they
  replace the review-stance predecessor's blob record for this file only.
  This is a board record, not an AST or gate-manifest re-anchor. The same
  archive serialization closes the removal and seed rows and writes the
  changelog entry.

## Response to plan review -- Codex -- 2026-10-19

| Finding | Disposition | Where answered |
|---|---|---|
| CA-PR1 | Accepted; source archived in `da6cc466`. | Header and operative amendment, Source and C3. |
| CA-PR2 | Accepted; final blob is an explicit archive task. | Operative amendment, Archive handoff. |
| CA-PR3 | Accepted; changelog moves from C3 to archive. | Operative amendment, Source and C3; Archive handoff. |
| CA-PR4 | Accepted; real document readers added to the scoped mapping. | Operative amendment, C4 document-reader map. |
| CA-PS1 | Accepted; call-path symlink refusals and a guard-removal break added. | Operative amendment, C2 containment. |
| CA-PS2 | Accepted; Bandit owner added, and a skip is non-pass. | Operative amendment, C4 security gate. |

Both plan-review obligations have been answered. There is no second plan
review. `ready-to-implement` does not lift the Decision's start fence:
implementation waits until `dev/plans/review-stance-and-lenses.md` is
`archived`.

## Implementation start -- Codex -- 2026-10-19

The start fence is satisfied: `review-stance-and-lenses` was archived at
`0974a4de`. The model-mapping plan has committed C1 but not C2. This plan
starts C1 now and keeps its before-C2 ordering. The concurrent model-mapping
engine edits are another session's work and are not part of this chunk.

## Implementation verification -- Codex -- 2026-10-20

**Boundary B mode**: full required for the install contract and scaffold
engine; the reviewed plan defers the full certifying suite and calls for this
scoped integration run. **Certified by**: pending. `CAIRN_FULL_SUITE` was never
set.

**Tested commit**: `bf84769c0beaac18594b0f7c45592f34cf72fc40`.
**Reviewed range**: `0afe97e21b5df9ce78b0e3edc013d40ec0b72432..bf84769c0beaac18594b0f7c45592f34cf72fc40`.
The removal's commits are `7f253b6b`, `a36005cb`, `69654f06`, `2cc6b260`
and `bf84769c`; intervening commits in the range belong to other work.
**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
Python 3.13.13.
**Pre-run state**: clean `git status --porcelain` in a detached worktree at
the tested SHA. **Post-run state**: the same clean status and unchanged SHA.

The mapped pytest commands used `python -m pytest -q` with these exact file
sets, split only to keep the run scoped:

* **G1 (12 files):** `test_review_stance_in_shipped_files.py`,
  `test_scope_reduction_trap.py`, `test_review_and_verification_rules_ship.py`,
  `test_review_sweep_ships.py`, `test_core_dev_folders.py`,
  `test_documentation_plan_module.py`, `test_comprehension_floor.py`,
  `test_verification_boundaries.py`, `test_scientific_check_guidance_ships.py`,
  `test_certifying_run_rule.py`, `test_doc_governance.py`,
  `test_claim_check_allow_config.py`, each under `bootstrap/tests/`.
* **G2 (10 files):** `test_trigger_evaluation_action.py`,
  `test_active_surfacing_mechanism.py`, `test_active_surfacing_render.py`,
  `test_onboarding_seed_roster.py`, `test_onboarding_slot_substitution.py`,
  `test_skills_onboarding.py`, `test_presets.py`, `test_profiles_smoke.py`,
  `test_onboarding_activation_helper.py`, `test_security_lint.py`, each under
  `bootstrap/tests/`. The security-lint test ran, not skipped.
* **G3 (11 files):** `test_notice_install.py`, `test_quickstart_sequence.py`,
  `test_manifest.py`, `test_config_module.py`, `test_scaffold.py`,
  `test_lockfile_module.py`, `test_verify_integrity.py`,
  `test_security_capability_install.py`, `test_agreement_retired.py`,
  `test_upgrade.py`, `test_upgrade_module_additions.py`, each under
  `bootstrap/tests/`.

| Command | Exit | Outcomes | Elapsed |
|---|---:|---|---:|
| `python -m pytest -q G1` | 1 | 932 passed, 1 failed; 0 skips/xfails/xpasses | 4.03 s |
| `python -m pytest -q G2` | 0 | 172 passed; 0 skips/xfails/xpasses | 6.78 s |
| `python -m pytest -q G3` | 0 | 469 passed; 0 skips/xfails/xpasses | 47.53 s |
| `python scripts/quality_gate.py --sub neutrality --sub redundancy` | 0 | neutrality 0 fails, 56 informational; redundancy 0 fails | under 2 s |
| `python scripts/check_cairn.py` | 1 | 5 flags across 185 files; 47 external links not probed | under 2 s |
| `python scripts/claim_check.py <file>` for each of 12 changed Markdown documents | 0 each | 12 clean, including declared historical-path exemptions in the upgrade guide | under 1 s total |
| `python scripts/link_check.py <the same 12 files>` | 0 | 12 files, no issues | under 1 s |
| `python scripts/sync_doc_snippets.py --check` | 0 | 356 documents, no drift | under 1 s |

**Non-pass disposition.** G1's sole failure is
`test_claim_check_allow_config.py::TestProseCarriesNoClaimCheckDirective`:
`dev/plans/archive/2026-10-19-security-review-upgrade-lockfile-paths.md:3` has an
inline directive. That line already exists at C3's parent `c177b8ca`; this
scope neither changed nor owns the other author's review. The other three
tests in that file passed. `check_cairn.py`'s five flags are two other
pre-existing records (`model-mapping-install-path.md`'s line citation and
`2026-10-18-security-review-session-writes.md`'s `tools/__pycache__` path)
plus three in this plan's original Scope/Proposed-paths paragraphs: two
retired paths and the new test after it materialized. Those paragraphs are
the append-only record of the planned change, not live adopter guidance;
they are not rewritten after implementation started. A direct live-surface
scan found the retired path only in `bootstrap/UPGRADE.md`, where it is
intentional advice to existing projects. The citation test's injected
retired-path control failed as intended. These non-passes are disclosed for
the code reviewer; no clean `check_cairn.py` or all-green mapped run is
claimed.

**Plan-specific acceptance.** Public `scaffold.py --manifest --allow-dev`
output at C3's parent `c177b8ca` and this tested SHA differs by exactly
one row, the retired agreement; the mapping was unchanged between C2 and
that parent. `test_agreement_retired.py` passed all eight cases: three fresh
presets, old-project plan/stage/apply preservation and the single
`removed-upstream` line, finalize refusal/empty-file recovery, roster
integrity and prompt activation, live-citation scan, and both shipped
decision sentences. Both onboarding helper pairs and the tour pair are
byte-identical. The clean old-project test exercises a synthetic prior
lock record and cached base through the public scaffold entry point.

**Controlled-break ledger.** Six fresh archive extractions of the tested SHA
each held one deliberate break; an unmodified control run of the same nodes
passed 5/5. Removing the roster read guard was **killed** by both leaf- and
parent-symlink cases (2 failures). Removing the already-emitted guard was
**killed** by the second-activation case (1 failure). Removing the retired
living-state exemption, restoring its install mapping, and injecting a
retired citation were each **killed** by the no-install-source contract
case (1 failure each). Making apply delete the old project file was
**killed** by the byte-preservation case (1 failure). The fresh-install
cases alone passed with the restored mapping because its source file is
absent; the explicit manifest-row assertion is what killed that mutant.
There were no survived or equivalent mutants.

**Ceremony handoff and known omissions.** The nine frozen-file changes,
as `+/-` line counts from the plan-start commit to C3, are:
`templates/modules/default-on/_onboarding/prompts.py` 1/2,
`templates/modules/default-on/_onboarding/triggers.py` 15/39,
`bootstrap/tests/test_active_surfacing_mechanism.py` 24/26,
`bootstrap/tests/test_active_surfacing_render.py` 29/24,
`bootstrap/tests/test_core_dev_folders.py` 1/1,
`bootstrap/tests/test_notice_install.py` 3/14,
`bootstrap/tests/test_onboarding_seed_roster.py` 1/1,
`bootstrap/tests/test_quickstart_sequence.py` 1/1, and
`bootstrap/tests/test_trigger_evaluation_action.py` 37/77. The new
`bootstrap/tests/test_agreement_retired.py` adds eight collected cases;
the roster test adds two parametrized symlink cases.
`bootstrap/tests/test_review_stance_in_shipped_files.py` also changes but
was not an existing frozen-file key. Our engine change is the one-row
`_CORE_MAPPINGS` assignment removal in `config.py`; our `lockfile.py`
change is comment-only. Top-level engine functions changed by this plan:
none. Neither AST baseline nor gate-manifest fixture was re-anchored. No
full suite, release ceremony, external-project upgrade, external-link
probe, or certifying run is claimed.

## Code review -- Antigravity (Gemini 3.8 Flash, fresh session) -- 2026-10-20

```
Reviewed commit: 5b7848c5cea68e7d5afc49c3f6781fb592cb8b6c
Target: C1-C4 (commits 7f253b6b, a36005cb, 69654f06, 2cc6b260, bf84769c, 5b7848c5)
Prior findings: none
```

**Foundations**:

1. **Should this happen as framed?** Yes; scaffold manifest loses exactly the agreement row, fresh installs omit the retired file while keeping roles, upgrades report `removed-upstream` once leaving existing files and lock records byte-for-byte untouched, and the moved roster is safely read from `dev/agent_collaboration.md` under containment guards with symlink refusal -- `bootstrap/_scaffold/config.py:547-553`; `bootstrap/_scaffold/lockfile.py:77-86`; `scripts/_onboarding/triggers.py:129-152`; `bootstrap/tests/test_agreement_retired.py::test_fresh_installs_have_roles_but_no_agreement`; `bootstrap/tests/test_trigger_evaluation_action.py::TestRosterReadBoundaries`.
2. **Best alternative.** The implemented design is minimal and safe: unshipping the file through `_CORE_MAPPINGS` removal rather than engine deletion commands, maintaining backward-compatible `_LIVING_STATE_DSTS` exemption for old projects, reusing the existing `_assert_safe_read` containment check for the moved roster slot, and adding an 8-case contract test rather than invasive scaffold alterations -- `bootstrap/_scaffold/config.py`; `bootstrap/_scaffold/lockfile.py`; `bootstrap/tests/test_agreement_retired.py`.
3. **What would show it wrong.** A symlinked roster being read, an upgrade silently deleting or modifying an old project's agreement file or lock cache, `removed-upstream` advancing machine state, or a fresh install leaking the retired file or trigger -- see the falsification ledger below.

**Bounding**: ACCEPTED

*Bounding rationale*: Challenged mapped tests and named surfaces across C1–C4:
* Ran mapped test files (`test_agreement_retired.py`, `test_trigger_evaluation_action.py`, `test_active_surfacing_mechanism.py`, `test_active_surfacing_render.py`, `test_security_lint.py`): all 55 tests passed cleanly with 0 skips/xfails.
* Verified byte-for-byte identity across all three twin pairs (`prompts.py`, `triggers.py`, and `agent-team-onboarding.md`).
* Evaluated disclosed non-passes: `test_claim_check_allow_config.py::TestProseCarriesNoClaimCheckDirective` failure is caused by an inline directive in `dev/plans/archive/2026-10-19-security-review-upgrade-lockfile-paths.md:3` created at `f0280ef0` by another author, outside this scope and unowned by this change; `check_cairn.py`'s five flags consist of two pre-existing files plus three historical citations in the plan's own append-only text from before implementation, while all 22 live markdown files touched by this plan pass `check_cairn.py` with 0 issues.
* Stated omissions: full-suite certifying run deferred per `AGENTS.md` and cited as `Certified by: pending`; AST and gate-manifest re-anchors deferred to Maintainer 0.4 ceremony.

**Waiting-line check.** The start fence was Maintainer-gated by the Decision conditional on `review-stance-and-lenses` being archived. Predecessor was archived at `0974a4de` prior to C1 start (`dev/plans/remove-collaboration-agreement.md:562-568`), so the fence condition was met before execution without requiring a pause or new approval. No deviation request was made in the implementation range.

### Falsification ledger

In an independent test worktree at `bf84769c`, six deliberate mutations were evaluated beside an unmutated control run (44/44 passed across `test_agreement_retired.py`, `test_trigger_evaluation_action.py`, `test_active_surfacing_mechanism.py`, `test_active_surfacing_render.py`):
1. **Mutant 1 (Roster read containment bypass)**: In `templates/modules/default-on/_onboarding/triggers.py`, removed `_assert_safe_read(roster_file, target)`. **KILLED** by `test_linked_roster_path_is_refused_before_read[leaf]` and `[parent]` in `test_trigger_evaluation_action.py` (2 failures: failed to raise `OnboardingSecurityError`).
2. **Mutant 2 (Living-state drop for old agreement)**: In `bootstrap/_scaffold/lockfile.py`, removed `"dev/collaboration_agreement.md"` from `_LIVING_STATE_DSTS`. **KILLED** by `test_old_agreement_is_reported_once_and_unchanged_by_upgrade`, `test_missing_old_file_refuses_bare_finalize_but_empty_file_survives`, and `test_no_install_source_cites_the_retired_path_or_trigger` in `test_agreement_retired.py` (3 failures: verify exits 1; not in living state).
3. **Mutant 3 (Accidental restoration of install mapping)**: In `bootstrap/_scaffold/config.py`, restored `("core/dev/collaboration_agreement.md", "dev/collaboration_agreement.md")` to `_CORE_MAPPINGS`. **KILLED** by `test_no_install_source_cites_the_retired_path_or_trigger` in `test_agreement_retired.py` (1 failure: manifest row assertion failed).
4. **Mutant 4 (Doubled opening marker suppression bypass)**: In `templates/modules/default-on/_onboarding/triggers.py`, suppressed the second `open_marker` check. **KILLED** by `test_doubled_opening_marker_does_not_fire` in `test_trigger_evaluation_action.py` (1 failure: unexpectedly fired `second-agent-type`).
5. **Mutant 5 (Preserved decision sentences drift)**: In `templates/core/dev/agent_collaboration.md`, replaced "they do not decide" with "they do not dictate". **KILLED** by `test_shipped_roles_retain_the_two_agreement_sentences_without_local_rule` in `test_agreement_retired.py` (1 failure: exact text match failed).
6. **Mutant 6 (Upgrade deletion on apply)**: In `bootstrap/_scaffold/upgrade.py`, unlinked "dev/collaboration_agreement.md" during `_apply_upgrade`. **KILLED** by `test_old_agreement_is_reported_once_and_unchanged_by_upgrade` in `test_agreement_retired.py` (1 failure: file missing on disk after apply).

There were no survived or equivalent mutants (6 of 6 killed).

**Coverage -- Covered:** claims #1-#9; old-project upgrade preservation through plan, stage, apply, and finalize; containment and symlink security boundaries on the moved roster slot; byte identity of onboarding and tour twin pairs; public manifest diff; 6-mutant ledger; analysis of disclosed non-passes. Not covered / low confidence: no full suite, AST re-anchor, or gate-manifest re-anchor was run (deferred to Maintainer certifying run and 0.4 ceremony per plan contract).

## Archive note -- Codex -- 2026-10-20

The independent code review at `764808e0` accepted the implementation with
no findings and a six-break falsification ledger. This archive is distinct
from the implementation and review commits. The adopter-visible result is
in the shipped roles document, onboarding helpers and `bootstrap/UPGRADE.md`;
the changelog now points to this record. Existing projects keep their copy
of the former agreement, lock record and base cache. The installer and
upgrader gained no file-deletion behavior.

The board's re-anchor register carries the reviewed final blob of
`bootstrap/tests/test_review_stance_in_shipped_files.py` at `5b7848c5`,
replacing the earlier review-stance receipt for that file only. The
Maintainer's 0.4 ceremony still derives the actual frozen-file, AST and
collection deltas; this archive performs none of those re-anchors. The
earlier Joined paragraph was condensed into the board's ceremony table by
`board-as-basis`; the new Joined paragraph beside that table is its durable
replacement. There is no open Waiting line.

The Decision's authorization for the two deferred decision-rights questions,
quoted verbatim:

> "Please scribe my acceptance as recommended."

**Dispositions:** `accept` — retire the installed agreement and signing
ritual while preserving old project copies, the roster and second-agent
prompt; `defer` — any future adopter-facing version of Cairn's finite
decision list needs its own proposal, homed in `dev/PLANNING.md`'s Decision
rights row; `defer` — revisit the distinct lifecycle-escalation wording on
a concrete conflict, in the same row; `defer` — the Maintainer-only AST and
gate-manifest re-anchors at the 0.4 cut, in the board's ceremony register.
