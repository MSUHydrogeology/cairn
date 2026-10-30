# Plan: Protect upgrade bases and install output

**Source proposal**: dev/proposals/archive/2026-10-29-codex-upgrade-install-integrity.md
**Status**: revising-code
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Check upgrade ancestors before merging and make supplied names recognizable in paths and output.

## Source proposal

The Maintainer accepted the revised proposal: check saved merge ancestors and bind staged results to the evidence checked, refuse specified invisible path characters, and escape supplied names in output. Preserve work and provide recovery; the digest is consistency evidence, not authentication.

## Scope

Change `bootstrap/_scaffold/upgrade.py`, `install.py`, and `cli.py`, shared helpers where appropriate, their tests, `bootstrap/UPGRADE.md` and relevant descriptive install/lockfile guidance. No doctrine surface. The existing Maintainer-run AST re-anchor remains required; this plan does not authorize baseline installation or old-anchor reconciliation.

**Stage and apply.** Stage records each automatic result’s source, destination and cache identity, expected digest and digest of the exact checked bytes. Apply compares the current record and bytes to that snapshot, then revalidates immediately before each automatic destination write; a changed or unreadable record or cache stops that write and lockfile advancement. Earlier unaffected writes may already have occurred: report them, retain staged data and original bad cache, and allow a safe restage and retry without overwriting adopter edits. This bounds changes observable at the checks, not arbitrary concurrent writes between a check and write; tell operators to stop concurrent writers. Recovery stores the preserved bad cache separately and establishes the new upstream ancestor at a distinct safe cache path before advancing provenance; failures leave the old evidence and adopter content recoverable. 

**Reuse.** Searching `bootstrap/_scaffold` for `base_hash`, `_contained_lockfile_path`, `print_report`, and `fidelity_warnings` found existing digest production, shared path admission, report rendering and merge output. Extend the review-only and stage/apply mechanisms, and existing display escaping, rather than duplicate them. Search test consumers with `rg` for those symbols and command flags before implementation; update the mapping below if further consumers are found.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Verify ancestors, bind stage to checked evidence, and implement recovery | Both plan reviews | Upgrade behavior, recovery and public-command tests |
| C2 | Enforce character policy and escape supplied names at all output routes | C1 and both plan reviews | Admission, display, tests and descriptive guidance |
| C3 | Record stable verification and hand off for independent code and Security reviews | C1–C2 complete | Boundary B evidence and review handoff; AST ceremony remains Maintainer-run |

## Acceptance criteria

### C1

Hash raw saved bytes against a well-formed `sha256` base digest before decoding; merge that same read. Missing, malformed, mismatched, unreadable or invalid UTF-8 evidence, including legacy records without a valid base digest, produces review-only, preserving the adopter file and original bad cache. Public plan, stage and apply tests cover matching control and a crafted loss case. Recovery tests reconcile the affected file, acknowledge review-only, advance unaffected files, preserve the bad cache as evidence, and complete a subsequent upgrade with a valid new ancestor derived from the applicable upstream template, never silently from the adopter file. Document exact operator steps and digest limitations.

### C2

Retain existing containment and path-shape restrictions. At shared admission reject Unicode categories Cc and Cf, U+034F and variation selectors in source, destination and cache paths; escape rejected values in diagnostics. Permit decomposed accents and visible non-Latin names; test zero-width, bidi, terminal controls, contextual joiners and selectors. Explain the compatibility cost and a supported recovery for existing refused names without hand-editing tool-owned provenance. Escape supplied module and slot names for display, preserving ASCII readability and distinguishing literal backslashes from escapes; lookup uses unchanged names. Public commands cover unknown modules, unpaired-marker warnings, normal and absent-module slot reports, and merge and fidelity output. No claim of complete protection against visual deception.

### C3

Run the mapped checks and scratch install/upgrade, including the recovery sequence; record results and omissions against the exact clean implementation commit. In separate scratch copies, remove the digest check and display escaping respectively: relevant behavior tests must fail, with controls passing. Record each mutation and outcome. Security preflight S2 is exercised here; S3 is the public commands and gates below. Unmet checks keep the work open. The existing AST ceremony is not performed by this plan's implementation agent.


## Scope delta

**Scope delta**: preserved.

## Verification

The reviewed command, input, test and wording mapping is `dev/plans/2026-10-30-upgrade-install-integrity/public-paths.md`.

Boundary A uses the canonical Python 3.13 interpreter and scoped tests. For ancestor and recovery behavior run `python -m pytest bootstrap/tests/test_upgrade.py bootstrap/tests/test_upgrade_lockfile_path_containment.py bootstrap/tests/test_upgrade_side_door_parity.py`; for module addition and provenance consumers run `python -m pytest bootstrap/tests/test_upgrade_module_additions.py bootstrap/tests/test_lockfile_provenance.py`; for display and install paths run `python -m pytest bootstrap/tests/test_install_report_slots.py bootstrap/tests/test_install_module.py bootstrap/tests/test_module_merge.py bootstrap/tests/test_scaffold.py`. Add public-command tests in the owning files and include their files in these commands. Split selections within the broad-run guard's file limit and reconcile the union; do not override the guard. Search actual readers and extend this mapping if affected consumers are missing.

Exercise `python bootstrap/scaffold.py upgrade --target <repo>` with `--plan`, `--stage`, `--apply` and `--apply --ack-review-only` in a scratch project, and `bootstrap/scaffold.py` install with normal, absent and unknown module cases. The new behavior tests must cover all C1/C2 cases, not just the smoke. Run `python scripts/claim_check.py` on changed documentation, `python scripts/check_cairn.py`, `python scripts/link_check.py`, `python scripts/sync_doc_snippets.py` where synced snippets change, and `python scripts/quality_gate.py --sub neutrality` for prose. Run `python -m pytest bootstrap/tests/test_security_lint.py` for the engine Bandit gate, treating a skip as an unmet check; do not run the full suite here.

Boundary B is **wide** for the engine contract and security boundary: repeat the mapped owning families, public paths, mutation and standing gates on a clean, unchanged final implementation commit under the canonical interpreter. Record tested SHA and reviewed range, interpreter, clean pre/post state, commands, outcomes, timing, non-pass dispositions, omissions, and **Certified by**: pending. Certification is separate. Boundary C is independent targeted falsification by the code reviewer, including the set of output routes and staged-evidence changes; the reviewer records bounding and any missing check. An AST re-anchor follows its existing Maintainer-run ceremony, separately authorized.


## Plan review -- Codex GPT-6 -- 2026-10-30

```
Reviewed commit: 353fb15cde122dcd4489dea77075269e96acb48b
Target: operative plan, accepted proposal and named production paths
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** The recovery and character-policy criteria carry the accepted outcomes, but the entry-point mapping is incomplete before implementation -- `dev/plans/2026-10-30-upgrade-install-integrity.md`, Verification.
2. **Best alternative.** Keep the existing review-only recovery and shared admission path, and complete the route-to-test mapping in the plan rather than adding another recovery mechanism -- `bootstrap/_scaffold/upgrade.py`, `_apply_upgrade`; `bootstrap/_scaffold/install.py`, `print_report`.
3. **What would show it wrong.** A supported recovery cannot preserve the bad ancestor and reach a later upgrade, or a named output route lacks a public test that checks the displayed value -- `dev/proposals/archive/2026-10-29-codex-upgrade-install-integrity.md`, Current contract.

**PR1: Complete the reviewed entry-point and wording mapping before implementation.** The accepted security preflight requires the plan to enumerate entry points and reconcile the exact adopter-facing wording with the selected tests before implementation. The plan instead says to check help and entry points and search for consumers before implementation, and groups output paths under broad test families. For example, `install.py` emits unpaired-marker warnings while `cli.py` emits merge and fidelity results; their distinct routes are not mapped to commands and tests. This leaves the author to decide coverage after the one plan review. Enumerate each public entry point and selected input, map each named output and recovery route to its owning test file or node, and reconcile the planned adopter-facing wording with those assertions in the operative cells. Retain all accepted routes and the scoped guard-respecting runs.

**Coverage:** Compared accepted current contract, recovery, character policy, stage binding, public paths and verification with the plan; inspected the named production output routes and template requirements. No implementation, command execution, timing or Windows rendering was tested. This pass clears only the ordinary Internal obligation.


## Plan review -- Codex GPT-6 Security reviewer -- 2026-10-30

```
Reviewed commit: a40d1e88f1ae19feb317aed8468ea37275727e92
Target: operative plan, accepted proposal, ordinary review and engine boundaries
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** The plan preserves the accepted raw-byte check, stage binding, recovery and display policy, but leaves the promised race handling undefined -- `dev/plans/2026-10-30-upgrade-install-integrity.md`, C1; `dev/proposals/archive/2026-10-29-codex-upgrade-install-integrity.md`, Current contract.
2. **Best alternative.** Extend the existing stage metadata and pre-write apply gates with an explicit evidence snapshot and revalidation contract; no new authentication or general transaction system is needed -- `bootstrap/_scaffold/upgrade.py`, `_write_stage` and `_apply_upgrade`.
3. **What would show it wrong.** A cache or digest change after an initial apply check still permits an automatic write, or failed recovery replaces the original bad cache -- `bootstrap/_scaffold/upgrade.py`, `_apply_upgrade`, file swap and new-base refresh.

**SRP1: Define the race and preservation contract before implementation.** C1 requires invalidation “including race/error paths,” but does not say when evidence is revalidated, what snapshot is compared, or what state survives a late failure. The accepted contract explicitly requires the plan to define races. Existing apply reads the lockfile before entering `_apply_upgrade`, performs several gates, writes staged destinations, then overwrites new-base cache paths and finally replaces the lockfile. Simply comparing cache/digest agreement once at entry would leave a later change unaddressed; comparing only current agreement would also admit jointly changed evidence unrelated to the stage.

In the operative cells, name the stage-bound evidence (including expected digest and identity of the ancestor record), its apply comparison and revalidation point relative to writes, and the supported concurrency boundary. State what happens when evidence changes or becomes unreadable during that interval, including whether any earlier writes can have occurred and how retry preserves adopter content and the original bad cache. Define where recovery stores a new valid ancestor without replacing that preserved evidence. This need not promise protection against arbitrary concurrent project write access, which the accepted proposal excludes. Map deterministic changed-after-check and read/write-failure cases, with a matching control, to the public apply/recovery tests. These criteria specify accepted race handling and preservation; they remove no outcome.

The character policy correctly separates admission from display and retains decomposed accents and visible non-Latin names. Keep existing containment and path-shape restrictions when extending admission; do not substitute a smaller forbidden-character set for them. The named display routes and compatibility recovery still need the command/input/assertion mapping requested by ordinary PR1; this pass does not duplicate that finding.

**Coverage:** claims, completeness and fail-closed behavior: C1 and `_compute_upgrade`/`_apply_upgrade`; production paths and drift: `_write_stage`, install `print_report`, CLI merge/fidelity output and ordinary PR1; reuse and consistency: searches for `base_hash`, `_contained_lockfile_path`, `print_report` and `fidelity_warnings`; lifecycle: declared obligations and Maintainer-only AST ceremony; domain/scope: consistency rather than authentication, no scientific result; satisfier: explicit operative contract and mapped race/failure tests above. **Not covered / low confidence:** no implementation, mutation, runtime, command execution or platform rendering tests; no suite run. This is the Security plan pass, not implementation assurance.

## Response to plan review -- Codex GPT-6 -- 2026-10-30

| Finding | Disposition |
|---|---|
| PR1 | Accepted. The public paths mapping records each selected input, test home and operator-facing assertion; verification retains scoped runs. |
| SRP1 | Accepted. C1 defines stage snapshot, pre-write comparison, observable concurrency boundary, partial-write and retry handling, and distinct recovery evidence; the mapping records deterministic race and failure tests. C2 retains existing path restrictions. |

Both plan-review obligations are complete. Scope remains preserved; implementation remains subject to the Maintainer-run AST ceremony already applicable.

## Implementation verification -- Codex GPT-6 -- 2026-10-30

**Boundary B mode**: wide. The scaffold upgrade engine is a contract and security boundary. This clean detached checkout exercised the mapped ancestor/recovery and path-admission family, install/module and lockfile consumers, scaffold and merge integration, public command paths, engine security lint, and prose/link/neutrality gates. The plan's reviewed tests cover plan, stage, apply, review-only acknowledgment/recovery, normal and absent module reporting, unknown module and slot display, merge/fidelity output, and added-module paths.

**Certified by**: pending

**Tested commit**: `38e3a2758d39f6a9920713cdf9fcdb87703f3e95`

**Reviewed range**: `85a9b6d2baa8a1167ee2c05a45519d59905f92e6`..`38e3a2758d39f6a9920713cdf9fcdb87703f3e95`

**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13, pytest 9.0.3

**Pre-run state**: clean detached worktree at the tested commit.

**Post-run state**: clean detached worktree at the same tested commit.

| Command | Exit | Outcomes | Elapsed |
|---|---:|---|---:|
| `python -m pytest bootstrap/tests/test_upgrade.py bootstrap/tests/test_upgrade_lockfile_path_containment.py bootstrap/tests/test_upgrade_side_door_parity.py` | 1 | 204 passed, 1 failed | 24.25s |
| `python -m pytest bootstrap/tests/test_upgrade_module_additions.py bootstrap/tests/test_lockfile_provenance.py bootstrap/tests/test_install_report_slots.py bootstrap/tests/test_install_module.py` | 0 | 84 passed | 21.14s |
| `python -m pytest bootstrap/tests/test_scaffold.py bootstrap/tests/test_module_merge.py bootstrap/tests/test_skills_upgrade.py bootstrap/tests/test_upgrade_added_slots.py bootstrap/tests/test_upgrade_edit_check_runs_no_project_programs.py` | 0 | 209 passed | 34.40s |
| `python -m pytest bootstrap/tests/test_security_lint.py` | 0 | 11 passed | 1.90s |
| `python scripts/claim_check.py bootstrap/UPGRADE.md` and `python scripts/claim_check.py dev/plans/2026-10-30-upgrade-install-integrity.md` | 0 | both OK | <1s |
| `python scripts/check_cairn.py` | 0 | 198 Markdown files scanned; no issues | <1s |
| `python scripts/link_check.py` | 0 | 198 Markdown files scanned; no issues | <1s |
| `python scripts/quality_gate.py --sub neutrality` | 0 | fail=0, info=43 | <1s |
| Digest mutation: bypass `checked_base_hash != expected_base`; `pytest bootstrap/tests/test_upgrade.py -k 'bad_ancestor_uses_review_recovery_and_preserves_evidence and altered-cache'` in a fresh mutation copy | 1 | expected behavior assertion failed: altered ancestor was merged instead of staged review-only | <1s |
| Unmutated control: same selected ancestor test on the clean tested commit | 0 | 1 passed | 0.51s |
| Display mutation: bypass `_display_name` ASCII escaping; `pytest bootstrap/tests/test_install_report_slots.py -k 'report_escapes_supplied_slot_names_and_distinguishes_backslashes'` in a separate fresh mutation copy | 1 | expected display assertion failed on bidi character | <1s |
| Unmutated control: same selected display test on the clean tested commit | 0 | 1 passed | 0.03s |

**Non-pass disposition**: `bootstrap/tests/test_upgrade.py::TestInitLock::test_review_pairs_leave_no_placeholder_the_install_filled` fails because the generated module inventory differs outside slots between the upstream review copy and the adopter copy. This is the pre-existing discrepancy identified during Boundary A and is unrelated to the accepted upgrade-integrity changes. The other 204 tests in that mapped group passed. No skip, xfail or xpass occurred.

**Plan-specific acceptance commands**: the mapped public-command tests above exercise `upgrade --plan`, `--stage`, `--apply`, `--apply --ack-review-only`, recovery followed by a later stage, install with normal/absent/unknown modules, and the listed output paths. The two scoped mutations were each made in a fresh detached copy; each relevant behavior test failed under mutation and passed on the unchanged commit.

**Known omissions**: no full-suite certification was run; it remains pending at the authorized integration point. The Maintainer-run AST re-anchor was not performed. No Windows terminal rendering run was performed. The checks cover the named behavior and public paths, not arbitrary concurrent writes between revalidation and replacement, which the plan expressly bounds out.


## Code review -- Codex GPT-6 -- 2026-10-30

**Reviewed commit**: `38e3a2758d39f6a9920713cdf9fcdb87703f3e95`; verification record `9aac9c15`.
**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** The raw-byte check and stage binding address the accepted design, but recovery cannot repeat and a mapped check failed -- `bootstrap/_scaffold/upgrade.py`, `_recovered_base_cache_path`; Implementation verification above.
2. **Best alternative.** Keep the recovery mechanism but allocate a distinct safe cache for each recovery, preserving previous evidence and supporting retry -- `bootstrap/_scaffold/upgrade.py`, `_apply_upgrade`.
3. **What would show it wrong.** A second corrupted ancestor that cannot be reconciled, or a required mapped check that fails -- see falsification ledger below.

**CR1: Repeated recovery cannot complete.** After a successful recovery, corrupt its new ancestor and repeat stage, manual reconciliation and acknowledged apply. The destination-derived recovered path is identical to the corrupt current cache, so apply refuses its different contents. The operator cannot complete recovery while preserving that evidence. Allocate a distinct safe path for the next ancestor, preserve the old cache, and test two successive recoveries through the public command.

**CR2: The mapped Boundary B check did not pass.** `TestInitLock::test_review_pairs_leave_no_placeholder_the_install_filled` failed in the recorded run. Its characterization as pre-existing does not satisfy the plan's mapped command or C3's explicit rule that unmet checks keep work open. Resolve or otherwise obtain the Maintainer's authorization for a change to the accepted verification contract, then record valid evidence against the final implementation commit.

**Falsification ledger** (Python 3.13.13, separate archive of reviewed commit):

- Unmodified `pytest bootstrap/tests/test_upgrade.py -k 'bad_ancestor_uses_review_recovery_and_preserves_evidence or stage_ancestor' -q`: 7 passed; matching and invalid ancestor controls exercised.
- Extended the existing altered-cache public test in that copy to corrupt the newly recovered cache and repeat reconciliation and acknowledged apply: 1 failed; apply refused the already occupied recovery cache. No production bytes were changed.
- Inspected the recorded mapped failure and C3: the required command exited 1; no passing replacement is recorded.
- Waiting-line history: no fenced chunk or deviation request was reached in this reviewed range; no waiting line was owed.

**Bounding**: WIDER RUN REQUIRED -- the repeated-recovery public path and the failed mapped test need passing coverage and a new final-commit verification record.

**Coverage:** Reviewed ancestor checks, stage/apply and recovery logic, verification record and plan criteria; challenged the public recovery path and mapped non-pass. Did not independently run the full mapped families, exercise every display route or assess terminal rendering; Security Review remains separate. No full suite was run.

## Code review -- Codex GPT-6 Security reviewer -- 2026-10-30

**Reviewed commit**: `38e3a2758d39f6a9920713cdf9fcdb87703f3e95`; plan and ordinary review through `9ea6f2bc`.
**Target**: implementation range `85a9b6d2`..`38e3a275`, ancestor consistency, recovery, containment and supplied-name output.
**Prior findings**: none closed; ordinary CR1 independently reproduced.
**Obligation**: Security Review of the scaffold / merge engine
**Tier**: Internal Security Review
**Findings**: raised; existing CR1 also blocks this obligation.

**Foundations**

1. **Should this happen as framed?** Hashing precedes decoding and the merge consumes the checked read; recovery preserves evidence on a failed write, but a second corruption cannot complete recovery -- `bootstrap/_scaffold/upgrade.py`, `_compute_upgrade`, `_recovered_base_cache_path`, `_apply_upgrade`; ledger below.
2. **Best alternative.** Retain the checked-read and stage-bound identity design; allocate a fresh safe recovery ancestor without replacing earlier evidence, as CR1 requests -- `bootstrap/_scaffold/upgrade.py`, recovery-cache collision check.
3. **What would show it wrong.** Substituted bytes reach the merge, failed recovery destroys evidence, or repeated corruption prevents supported recovery -- falsification ledger below.

**Security disposition.** CR1 is confirmed independently: the first recovery works, but corrupting its recovered ancestor makes the second acknowledged apply refuse because the destination-derived cache path is already occupied by that corruption. Keeping evidence is correct; reusing its name for the next ancestor prevents the promised recovery. The satisfier remains a distinct safe allocation, two successive public-command recoveries preserving both bad ancestors, and final-commit change verification. This pass does not clear the Security obligation. CR2's failed mapped check also remains unresolved; this pass does not waive it.

**Falsification ledger** (fresh detached checkout of the reviewed commit; Python 3.13.13):

- Checked-read substitution: wrap `_read_regular_bytes` to replace the AGENTS ancestor immediately after returning its original bytes. `_compute_upgrade` reads that cache once and merges the checked bytes, retaining the adopter slot; substituted content does not enter the result. Passed.
- Recovery storage failure: through public stage and acknowledged apply, inject `OSError` at `_write_by_replacing` for the recovered cache. Apply refuses; original bad cache, lockfile, reconciled adopter file and stage survive. Remove the fault and retry the same apply: succeeds, preserving the original bad cache. Passed.
- Repeated corruption: public stage, manual reconciliation and acknowledged apply succeeds once; corrupt the newly recorded cache and repeat. Second apply returns 1, preserving the corrupt cache, lockfile and stage. Reproduces CR1.
- Scratch-only probe selection: `python -m pytest bootstrap/tests/test_security_upgrade_probe.py -q` (reviewer-created probe file in the detached copy): 3 passed, 1.28s. An initial probe expected `clean` rather than the correct `clean-locally-modified`; corrected the probe expectation, with no production changes.

**Bounding**: WIDER RUN REQUIRED -- repeated-recovery behavior needs passing public coverage and a new final-commit verification record; the mapped failure in CR2 also remains open.

**Coverage:** claims, production paths, completeness and fail-closed behavior: probes above and stage/apply identity checks; reuse and consistency: existing path admission, replacing writer and display helper; drift: C1/C2 and public-path mapping against the changed engine and output calls; lifecycle/scope: separate Security obligation, pending certification and Maintainer-run AST ceremony. Waiting-line history reaches no fence or deviation. No new scope proposed. Did not mutate every output route, rerun Boundary B, test arbitrary concurrent writes, platform rendering or the historical anchor. No full suite or re-anchor run.

## Response to code reviews -- Codex GPT-6.1 Sol -- 2026-10-30

| Finding | Disposition |
|---|---|
| CR1 | Accepted. Commit `3fd8dab3` allocates a fresh stage-bound recovery cache and refuses an occupied path. The public-entry regression now repeats recovery after corrupting the first recovered ancestor and checks both corrupt caches survive. Targeted evidence follows; final change verification remains outstanding. |
| CR2 | Open. The mapped test failed in the prior verification; a separate proposal addresses the generated inventory discrepancy and awaits the Maintainer's Decision. No verification requirement is waived or removed. |
| Security Review | Open. The pass independently confirmed CR1 and requires final-commit verification; this response does not clear that obligation. |

## Targeted repair evidence -- Codex GPT-6.1 Sol -- 2026-10-30

The repair was tested in an isolated archive of the then-current committed tree with only the two repair files overlaid. Their tested bytes were subsequently compared with commit `3fd8dab395eb0cbb46953dada9297bdfbb9daf75` and matched. With `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13), `python -m pytest bootstrap/tests/test_upgrade.py -k 'bad_ancestor_uses_review_recovery_and_preserves_evidence or stage_ancestor' -q` exited 0: 7 passed, 109 deselected, in 3.80 seconds. The altered-cache case exercises two stage, manual reconciliation and acknowledged apply cycles and checks both corrupt ancestors survive.

This is targeted iteration evidence, not a new Boundary B record. The required mapped failure in CR2, final-commit wide verification, Security Review clearance, certification and the Maintainer-run AST ceremony remain outstanding. The plan stays `revising-code`; no full suite was run.

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

## Implementation verification follow-up -- Codex GPT-6 -- 2026-10-30

**Boundary B mode:** wide, on clean detached Git clones at
`22c49ec2bb588d1d237db14f44650caea77f4b33`. The recovery repair is
`3fd8dab395eb0cbb46953dada9297bdfbb9daf75`; the reviewed implementation
range remains `85a9b6d2`..`3fd8dab3`. Later integrated changes are included in
the tested commit. **Certified by:** pending. Interpreter:
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13).
Both verification clones were clean before and after their commands; temporary
logs were moved outside one clone before its final `git status --short`.

| Command, with the absolute interpreter above | Result | Wall time |
|---|---|---:|
| `-m pytest -q --tb=short bootstrap/tests/test_upgrade.py bootstrap/tests/test_upgrade_lockfile_path_containment.py bootstrap/tests/test_upgrade_side_door_parity.py` | 219 passed, 6 failed | 49.09s |
| `-m pytest -q --tb=short bootstrap/tests/test_upgrade_refuses_hostile_project_data.py bootstrap/tests/test_upgrade_module_additions.py bootstrap/tests/test_lockfile_provenance.py` | 254 passed | 48.01s |
| `-m pytest -q --tb=short bootstrap/tests/test_install_report_slots.py bootstrap/tests/test_install_module.py bootstrap/tests/test_module_merge.py` | 36 passed | 1.42s |
| `-m pytest -q --tb=short bootstrap/tests/test_scaffold.py bootstrap/tests/test_skills_upgrade.py bootstrap/tests/test_upgrade_added_slots.py bootstrap/tests/test_upgrade_edit_check_runs_no_project_programs.py` | 193 passed | 47.60s |
| `-m pytest -q --tb=short bootstrap/tests/test_security_lint.py` | 11 passed; no Bandit skip | 3.92s |
| `scripts/claim_check.py bootstrap/UPGRADE.md` and `scripts/claim_check.py dev/plans/2026-10-30-upgrade-install-integrity.md` | both OK | 0.05s each |
| `scripts/check_cairn.py`; `scripts/link_check.py`; `scripts/quality_gate.py --sub neutrality` | both link/prose checks OK on 195 Markdown files; neutrality fail=0, info=43 | 1.44s; 0.20s; 0.95s |

**Non-pass disposition:** The six failures in the first group are open, not
waived. `TestInitLock::test_review_pairs_leave_no_placeholder_the_install_filled`
is the generated inventory mismatch addressed by the separate proposal awaiting
Decision. Three `TestTemplateGatingSafety` nodes (`test_only_the_human_team_axis_is_gated`,
`test_solo_keeps_all_brightlines_drops_human_contributors`,
`test_multi_keeps_human_contributors`) and
`TestInitLock::test_review_copy_is_sized_to_the_current_profile` assert a
`human_team` gate, `## Human contributors`, or old headings removed by the
accepted apparatus reduction at `3cceb2c0`. The removed section was
informational; `templates/optional/CONTRIBUTING.md` still supplies the human
entry point and links to shared rules. The sizing node needs a current
profile-dependent assertion. The containment node
`test_a_hand_built_review_area_cannot_make_apply_record_a_path_outside_the_project`
builds a stage without the directory observations now required by
`a6703b49`; apply correctly refuses it. Its fixture must supply valid
observations before testing path containment. These causes identify stale
test inputs or assertions, but the mapped command remains failed.

**Mutation evidence:** On the unmodified commit, the public altered-ancestor
recovery test and supplied-slot display test each passed (one test each).
In separate copies, bypassing the ancestor digest comparison made the recovery
test fail because no review-only pair was staged; bypassing `_display_name`
escaping made the display test fail on U+202E. Total 2 mutants, both killed;
no survivors or measured equivalents. The recovery test also exercises two
successive corrupt ancestors and preserves both originals.

This follow-up took approximately 4 minutes of measured test and gate wall
time; token use is unknown. The mapped non-passes keep the plan in
`revising-code`. An independent Security Review follow-up on the recovery
repair and a passing final verification record remain outstanding. No full
suite, re-anchor, Windows terminal rendering, or arbitrary concurrent-writer
probe was run. Synced snippets were unchanged, so snippet synchronization was
not triggered.

## Code review follow-up -- Codex GPT-6 Security reviewer -- 2026-10-30

**Reviewed commit:** `3fd8dab395eb0cbb46953dada9297bdfbb9daf75`; verification follow-up through `872d1972`. **Obligation:** Security Review of the scaffold / merge engine. **Tier:** Internal Security Review. **Disposition:** interim; Security obligation remains open.

**Foundations**

1. **Should this happen as framed?** Yes: `upgrade.py` now stages a fresh random recovery path and refuses an occupied destination; the public regression preserves both corrupt ancestors and completes the second recovery.
2. **Best alternative:** Retain stage-bound allocation and refusal of occupied paths; `_contained_lockfile_path` and `_assert_safe_write` reuse existing containment checks.
3. **What would show it wrong?** A repeated recovery overwriting evidence, accepting a malformed or occupied recovery path, or failing a required mapped check; the latter remains evidenced below.

**CR1:** The repeated-recovery behavior is repaired on the reviewed bytes; final closure still requires passing required change verification. **CR2:** The wide verification follow-up records six failures, including the inventory discrepancy awaiting a separate Maintainer Decision. None is waived here. No final Security clearance is given.

**Falsification ledger:** In an isolated archive of `3fd8dab3`, Python 3.13.13, `python -m pytest bootstrap/tests/test_upgrade.py -k 'bad_ancestor_uses_review_recovery_and_preserves_evidence or stage_ancestor' -q` passed 7 tests, 109 deselected, 5.20s. Inspected the staged path's fixed destination digest and 32-hex nonce validation, old-path inequality, containment and occupied-path refusal in `_apply_upgrade`; the regression exercises two public recovery cycles. The recorded wide run at `22c49ec2` has 219 passes and 6 failures in its first mapped group; it is not a passing Boundary B. This follow-up took approximately 3 minutes; token use unknown.

**Bounding:** WIDER RUN REQUIRED: resolve the mapped non-passes and record passing final-commit verification.

**Coverage:** Claims and satisfier: C1 and the regression; production path and completeness: `_write_stage` and `_apply_upgrade`; fail-closed and reuse: path validation and containment; consistency and drift: recorded verification and plan C3; lifecycle and scope: unresolved CR2 and separate Decision. Did not rerun wide checks, mutate output routes, probe concurrent writers or assess platform rendering. No full suite or re-anchor was run.
