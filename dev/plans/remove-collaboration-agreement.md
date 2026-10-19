# Plan: Remove the collaboration agreement

**Source proposal**: `dev/proposals/2026-10-19-claude-remove-collaboration-agreement.md`
**Status**: awaiting-plan-review
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
