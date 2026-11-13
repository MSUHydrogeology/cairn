# Plan: Bound upgrade growth and trial Git merge

**Source proposal**: dev/proposals/archive/2026-11-05-codex-upgrade-growth.md
**Author**: gpt-6.1-terra (Medium), plan author
**Status**: awaiting-code-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-12
**In brief**: Require an evidenced threat for new upgrade refusals and compare the existing upgrade with an isolated Git merge.

## Build summary

Add the accepted review rule without weakening existing protections, then measure one finite comparison on synthetic projects. A failed or incomplete comparison is a result; it authorizes no engine replacement. The temporary trial uses an operating-system write boundary, not production machinery or a new shipped framework.

## Source proposal

Decision `15264bf4` accepted both outcomes and no scope reduction. The source Proposal 1–3 and its security preflight govern the rule, controls, comparisons and reporting. The High-tier trial design was supplied by gpt-6.1-sol on 2026-11-12; it is design input, not a Security Review or a waiver.

## Scope

Add the rule to `AGENTS.md` review guidance: every proposed new upgrade refusal identifies attacker, controlled input, harmful action, threat-model connection and distinguishing evidence or test. Outside-model risk needs the Maintainer's explicit disposition; unexplained threats and unmet protection stay open. Existing refusals and checks remain. This is governing doctrine; explanatory methodology belongs in `docs/methodology/` only if needed. Record trial evidence here; do not change the engine or installed contract.

Reuse: searches of `bootstrap/_scaffold/{upgrade,merge,security,lockfile}.py`, `bootstrap/container/recipe.md` and `bootstrap/tests/test_upgrade_refuses_hostile_project_data.py` found the real CLI, merge, containment, recorded bases, existing containment pattern and hostile cases. Use those, the verified `tools/git_read.py`, system Git and macOS `sandbox-exec`; no new shipped launcher or harness. Scratch drivers and profiles are developmental and removed after evidence is recorded.

## Sequence

Estimate two focused windows plus review and verification; uncertainty is whether the untried sandbox profile and recorded-base reconstruction work on the host. C0 establishes the available read boundary and safe trial island locally; C1 ships rule and bounded trial evidence. Neither depends on a future plan review or archive.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C0 | Pin sources and establish read and confinement controls below. | Plan reviews | Recorded controls or incomplete trial |
| C1 | Rule and matched comparison below. | C0 controls pass for writes | Governing rule and observations, including negative/incomplete outcomes |

### C0: source and isolation

Use canonical `/Users/kendal30/conda_envs/lhm/bin/python3.13` on macOS; freeze candidate `326f9474eeae060c655e4a5ed051d9639187c0c7` (or explicitly pin a later clean commit and compare relevant bytes) and v0.5.0 `3bb27388fccaf51ae490e80ca4b4ab94aa5e2206`. Verify `tools/git_read.py` and its template twin match SHA256 `a1c54924ef70e15d583ed265aba1fbaa3195554f7e29e36fdd726cb7cc322cec` and trusted caller. In the synthetic repo, its public `run_git` must return the exact canonical root for `rev-parse --show-toplevel`, and `('push','--all')` must return failed/`unsupported-read-form` without launch. This uses existing reviewed and cap-accepted 3.13 mechanism plus local controls, not a claim that Safe Git's final wide Boundary B passed. That separate obligation remains open.

Create a canonical temporary root outside the project, with frozen committed source exports, driver, profile and protected canary outside writable island W; W holds synthetic copies, home, temp, empty hooks/templates, logs and outside sentinel. Resolve and hash trusted Python and Git outside W; recheck before each spawn. Run fixed driver with `/usr/bin/sandbox-exec -f PROFILE PYTHON -I -B DRIVER` and a fresh environment, no credentials or agent/socket, `PYTHONDONTWRITEBYTECODE=1`, PATH limited to trusted Git's parent. Deny by default, allow needed reads, mappings, process and interpreter facilities; allow exec only those exact Python and Git paths, writes only W and `/dev/null`, and no network. Never execute target-installed code. Do not broaden to allow-default or an unisolated fallback if it fails.

Under the same profile prove a mode-0600 outside canary write is denied and its parent-observed digest unchanged; deliberately alter W's outside sentinel and detect its changed digest, then restore it. An unsandboxed loopback connection must reach a controlled listener; the sandboxed child connection must be denied and not observed. Failure of any control or runtime stops writes and records incomplete. Use DEVNULL stdin, bounded captured output, 60-second command and 15-minute driver limits; on timeout kill the owned process group before bounded reap. Snapshot and cleanup never follow planted links; remove only the owned canonical temporary root after recording evidence. Profile and commands are temporary evidence, not shipped code.

### C1: comparison

Use trusted Git directly for writes, not the read-only helper. Initialize scratch repositories with empty templates; synthetic author, committer and fixed dates; `HOME`, `XDG_CONFIG_HOME`, `TMPDIR` in W; `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_ATTR_NOSYSTEM=1`, `GIT_TERMINAL_PROMPT=0`, `GIT_NO_LAZY_FETCH=1`, `LC_ALL=C`. Prefix every Git call with `-c core.hooksPath=EMPTY -c core.fsmonitor=false -c core.attributesFile=/dev/null -c core.pager= -c core.editor=/dev/null -c sequence.editor=/dev/null -c commit.gpgSign=false -c tag.gpgSign=false -c protocol.allow=never -c protocol.file.allow=never -c gc.auto=0 -c maintenance.auto=false -c submodule.recurse=false`. Check known local config before each call: no includes, aliases, external filters or drivers, remotes or submodules. Copy full synthetic `.git` without alternates, hardlinks or gitfiles; do not use clone protocol. The exec restriction is a backstop. Existing `merge.py` uses the frozen Git via PATH unchanged.

Profile: `project_name: UpgradeTrial`, `test_command: pytest`, `preset: solo-greenfield`. Install old source with `python bootstrap/scaffold.py --config PROFILE --target A --cairn-root OLD --allow-dev --non-interactive`; render candidate into B with the same command and profile. In A fill a project-conventions slot with `TRIAL_SLOT_KEEP`, append `TRIAL_ORDINARY_KEEP` to `dev/README.md`, and commit. Copy identical snapshots for each path and three variants: benign; committed `dev/proposals/_template.md` symlink to an outside sentinel file; committed `dev/proposals` symlink to an outside directory with `_template.md` sentinel. Before each path record sorted lstat types, modes, targets and regular-file hashes, marker bytes and outside inventory/digests.

Build template baseline T0 from A's recorded ancestors: check cached raw bytes against each `base_hash`, apply existing `strip_conditional_regions` and `substitute_tokens` using the old profile; for verbatim records require pristine old-install bytes match. Compare reconstructed destinations to clean A; a mismatch is a negative migration result and stops that prototype leg, never substitute a guessed baseline. Exclude Git and runtime/lock/base/profile bookkeeping, name exclusions and report stale inert metadata; include other supported installed destinations. Build T0 and candidate T1 with Git `hash-object -w`, temporary `GIT_INDEX_FILE`, `read-tree --empty`, `update-index --index-info`, `write-tree`, `commit-tree` and `update-ref refs/heads/cairn/template`; T1's parent is T0. The adopter commit has T0 as parent and the entire same customized snapshot, including metadata and link. Run `git merge --no-ff --no-commit --no-edit --no-stat cairn/template`; record exit, unmerged stages and bytes, no auto-resolution. In the matched copy run candidate `scaffold.py upgrade --target TARGET --cairn-root NEW --plan`, then `--stage`, then `--apply`; a refusal or conflict is a result, never bypassed.

## Acceptance criteria

### C0

The pinned read controls and three nonvacuous isolation controls above pass before comparison writes. A denied write leaves the protected digest unchanged; the positive sentinel and loopback controls prove observation. Record profile, commands, results and limits. Any missing control stops writes and is an incomplete trial, not a safety conclusion.

### C1

The rule retains existing protections and assigns out-of-model risk only to the Maintainer. For each path and variant record conflicts/count, marker preservation or loss, sentinel and outside changes, operator steps, engine modules exercised, migration result, elapsed time, platform, Python/Git versions, source/config/profile/corpus hashes and limitations. Inventory all 37 hostile-test functions and their parameter classes from the pinned source; label each applicable, inapplicable or untested with reason and remaining mechanism. Only three variants run; no security equivalence or replacement readiness is claimed. More conflicts, lost edits, sentinel writes or unaccounted cases falsify readiness. A blocked or unfavorable trial remains an honest result; future replacement requires a separate proposal.

## Scope delta

**Scope delta**: preserved.

## Verification

Before implementation use `/Users/kendal30/conda_envs/lhm/bin/python3.13 tools/test_tiers.py for <changed paths>`; for `AGENTS.md` pass the reviewed range. Run its mapped readers and pinned-prose checks, plus claim, link/content, snippet and neutrality gates. The real install and upgrade CLI and Git merge are the trial entry points; no permanent tests are required solely for scratch observations. Boundary C is targeted ordinary and Security code review. Boundary B is wide for governing and trust surfaces, after review on a clean unchanged commit: mapped readers, owning and public paths, standing prose gates and the trial controls and evidence. Record commands, outcomes, tested SHA, interpreter, pre/post state, elapsed time, non-passes and omissions. Certification is separate.


## Plan review -- GPT-6.1 Sol (Security Review, High) -- 2026-11-12

Reviewed commit: `abd8efdb`.

**Obligation**: Internal Security Review
**Tier**: Internal
**Findings**: none
**Verdict**: APPROVE
**Elapsed**: approximately 12 minutes, shared across both plans.
**Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: the review rule preserves existing protections, and the synthetic comparison requires frozen trusted code, operating-system write confinement, exact executable restrictions and no network before writes -- Scope, C0 and source Proposal 1–3.
2. **Best alternative.** Retain the three matched variants and applicability inventory instead of building a shipped harness or replaying the full hostile matrix; this measures the accepted question with less continuing burden -- C1 and Acceptance criteria.
3. **What would show it wrong?** A successful protected write, undetected sentinel change or observed sandboxed loopback connection stops the trial; missing controls must be incomplete rather than safety evidence -- C0 controls and C1 reporting.

I found no new boundary design left to the executor: C0 fixes write and executable authority, source hashes, environment, command/process limits, cleanup and refusal behavior; runtime-specific profile syntax must satisfy those fixed constraints or stop. Safe Git's reviewed component is distinguished from its unpassed final Boundary B. Trusted direct Git writes are distinct from the read-only helper. Recorded-base reconstruction must match the old install; mismatches cannot be repaired by guessing. No rule weakens, no engine replacement is authorized, and temporary developmental probes need no permanent test contract.

**Coverage:** I compared the committed plan, accepted source, current template and Safe Git/merge entry-point source; the 37 hostile-test functions need classification, not full runtime replay. I did not run profiles, controls, Git writes, comparisons, tests or suites. Only the previously reported availability probe exists; executable provenance and actual confinement remain implementation evidence. This pass grants neither Safe Git archive clearance nor trial success.


## Plan review -- GPT-6.1 Terra (ordinary reviewer, Medium) -- 2026-11-12

Reviewed commit: `abd8efdb35cf0480fed488bebd88360336cd6609`.

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: approximately 10 minutes across both queued plans.
**Tokens**: unknown.

The plan measures whether a simpler upgrade approach merits further work while retaining today's protections.

1. **Should this happen as framed?** Yes. C0 and C1 deliver both accepted outcomes without making an engine replacement or another plan's archive a prerequisite. The source permits an honestly incomplete trial; C0's stop conditions preserve that distinction -- source Proposal 1–3; plan Sequence and Acceptance criteria.
2. **Best alternative.** Keep the fixed three variants and classify the existing hostile cases instead of building a reusable trial framework or replaying every case. This meets the comparison objective with temporary machinery -- C1; the current hostile-test file contains 37 test functions.
3. **What would show it wrong?** Failure to reconstruct the recorded baseline, observe the sentinel, or preserve a customization must appear as a negative result, not a guessed baseline or replacement recommendation -- C0 controls and C1 reconstruction/reporting.

The assigned executor has source identities, environment, command limits, write authority, controls and comparison inputs. Platform profile syntax remains implementation detail constrained by a stop, not permission to redesign isolation. The source's prerequisite remains a locally verified reviewed Git boundary; its unrun final integration is explicitly not claimed passed. The governing rule belongs in installed instructions; trial observations belong here. No existing protection weakens or disappears.

**Coverage:** Compared accepted scope, current template, helper/merge/config entry points and the hostile-test inventory; verified the named token renderer also exists in `slotmerge.py`. No sandbox, command-control or comparison execution, runtime tests, Security clearance or final integration was performed. Those outcomes remain unmeasured.


## Review disposition -- GPT-6.1 Terra (Implementation coordinator, Medium) -- 2026-11-12

Both required plan obligations are accepted: ordinary `83800e91` and Security `e59b8a1f`. Neither pass raised a finding. The operative plan is unchanged and ready for Low-tier execution; all trial controls, scope fences, code reviews and final verification remain due. No runtime result or publication permission is inferred. Elapsed: approximately one minute; Tokens: unknown.

## Implementation result -- GPT-6 Luna (Implementation, Low) -- 2026-11-12

C1 is incomplete. The final needed-read profile could not launch the trusted interpreter, so I stopped before the comparison. Earlier broad-read controls and synthetic setup are limited preflight evidence, not the accepted isolation result.

**C0 controls.** The pinned sources were old v0.5.0 commit 3bb27388fccaf51ae490e80ca4b4ab94aa5e2206 and candidate 326f9474eeae060c655e4a5ed051d9639187c0c7. Their Git archive SHA256 values were 2abde9ec20489d7e129b1b4e61059cb368b4b0f6b0e750ce88b039a2d194da2e and afb0c6d5c6b63438518be8c16c9557d2f700c27cbaedf4b37a149c57301e570c. Both Git-read helper copies at the candidate commit hash to a1c54924ef70e15d583ed265aba1fbaa3195554f7e29e36fdd726cb7cc322cec; the pinned exact_replace caller is c9150c7a024fb9cbb21209abb6a64be382477366982d779ab0277f7b53e28d40 and expects that helper hash. Under the broad-read preflight, the public run_git returned the exact synthetic repository root and push --all failed with unsupported-read-form.

The broad-read control run took 0.406 seconds. It denied a mode-0600 outside-canary write and the host-observed SHA256 stayed 55f51d0c65402916edf10ede368f4762397b3e79e147db4194ee9b66b90f5e6d. The W sentinel changed from 5a8030b6b19fc8d56e14b2bacf3836d95c6d7196c024efe2d669db1aa5781e15 to 0941ea6d968a96c2afb7286bb4b6b01aac97e532cf74e84861bfafb3f1fab41a, was detected, and was restored. A host connection reached the controlled loopback listener; the child was denied with PermissionError, and the listener accepted only the host connection.

Those controls used profile-broad-read.sb (SHA256 7bb5d1352975bd9f669cc5f3c3f44c36f34674f063c43d0034bd07393316e4de), whose file-read permission was broader than the plan's needed-read scope. The narrowed profile at /private/tmp/cairn-upgrade-c0-fnmwz2bd/profile.sb allowed reads only from W, frozen source exports, the fixed drivers, trusted Python and Git installations, and named OS paths; it kept writes in W and /dev/null, allowed only the exact Python and Git executables, and denied network access. Its SHA256 is 7cac96a2d4ab9761790397ce41d7337772693f9eaca429372c27dcb4e459e368. A harmless Python print under this profile exited 134 with no output; the trial driver exited -6 before output. The separate profile-parent-metadata.sb diagnostic (SHA256 31bf258419c99131815389098cedab2e231d4ab8d3fef62be8fdc83d679ef666) added only 13 literal ancestor metadata permissions and no content roots; its harmless Python launch also exited -6 with no output. No secret or credential file was read. Because the tightened profile did not pass the controls, C0 is incomplete; the broad-read run does not satisfy the acceptance gate.

**C1 setup and baseline.** The test profile was project_name UpgradeTrial, test_command pytest, preset solo-greenfield; its SHA256 is 6ebdb265a789f8d0c1e472e3eb4a3af933ab7aed198cefa2f27245825ede1f18. Python 3.13.13 at /Users/kendal30/conda_envs/lhm/bin/python3.13 hashes to a0e58d65114a537560a551b09d5a3c2d06f6c3a199d9ed819138080cd58ddf3e; trusted Git 2.53.0 at /opt/homebrew/Cellar/git/2.53.0/bin/git hashes to 5e5a622e407fb7deb74173cab9e47ff214952cc6bfcd036449cf9edbaa305537. The pinned hostile-test corpus bootstrap/tests/test_upgrade_refuses_hostile_project_data.py hashes to 39332906e7ab53fd144ad4707c0a69abc9233692586e628a3ca239a243d19871.

The old installer created A with 69 files and 39 lock records; its command exited 0 in 0.129 seconds. Candidate rendering produced B with 82 files and 49 lock records, but its individual exit and elapsed time were not retained in the truncated output. In A, the synthetic adopter commit 416b7c25508d998dbd2a93bc3f8da8bc1c695298 contains TRIAL_SLOT_KEEP in the project-conventions slot and TRIAL_ORDINARY_KEEP in dev/README.md. Its clean old-install parent is d0bf5889c1503ad6234093460555f8672f91fb1d.

I reconstructed all 39 recorded destinations from the old cached bases using the specified conditional-strip and token-substitution functions, checked their base hashes, and compared the result with that saved clean A parent, before the adopter markers. Thirty-seven destinations matched. AGENTS.md reconstructed to 33,006 bytes, SHA256 2d531b7f10f520faa15405e214baedf22d444617497dfdec41030d36c1fb0f2a; clean A has 33,518 bytes, SHA256 860eda6da3b14e98f148bbc91c5dd74d1f985e60c43a5b43e9b41a509605bdf9. dev/PLANNING.md reconstructed to 8,430 bytes, SHA256 3efa0a7b17c6ef8959233f50aecf045624a4f80045d281c5cc9cfaa6ab583169; clean A has 10,035 bytes, SHA256 26a2d619d32cdf3051dc564193ee1e84ee42e737f38c2fa4fcbbcdaf02968c71.

The differences are explained by the pinned installer: install.py writes the security-verification module merge into AGENTS.md and renders the selected onboarding overlay into dev/PLANNING.md. The plan's reconstruction recipe does not include those operations. I did not use them to guess a replacement T0. The mismatch is a negative migration result and stops the Git prototype leg. Clean A also had unrecorded install outputs .gitignore and two onboarding copies under dev/modules/onboarding, plus runtime dev/.cairn/local-env.json; no prototype tree was built, so I did not classify these as stale or add them to T0.

The six comparison cells below were not run. The strict C0 failure stopped further comparison writes; the Git prototype also lacks a reconstructable T0.

| Path | Benign | Leaf link | Linked parent |
|---|---|---|---|
| Git template merge | Not run | Not run | Not run |
| Existing upgrade engine | Not run | Not run | Not run |

No comparison conflicts, marker preservation/loss, planted-link sentinel changes, or operator steps were measured. The synthetic install and adopter commit are not comparison results. Only the old and candidate install commands ran; no upgrade --plan, --stage or --apply command and no Git merge command ran. No upgrade action, Git merge, or upgrade write path was run. The 37 hostile cases below remain unrun; their named functions and existing guards remain unchanged. No security equivalence or replacement-readiness conclusion follows.

**Untested hostile-test inventory.** All entries are untested because no comparison entry point ran. The named function in the pinned test file remains the mechanism for each case. Parameter classes are recorded as defined at candidate commit 326f9474; H means the file's hostile ESC-and-newline string.

| # | Test function and parameter classes |
|---|---|
| 1 | test_apply_never_creates_a_profile_through_a_link — how: dangling-absolute, dangling-relative-delivered-by-clone, existing-outside-file, cairn-folder-is-a-link |
| 2 | test_self_heal_writes_no_line_break_from_the_lockfile — where: preset, axis, token |
| 3 | test_self_heal_writes_nothing_when_a_profile_value_is_not_plain_text — value: integer, list, object, U+2028, ESC sequence |
| 4 | test_init_lock_never_creates_the_profile_template_through_a_link — no parameters |
| 5 | test_init_lock_refuses_a_profile_that_is_a_link — how: existing-outside-file, existing-inside-file, dangling |
| 6 | test_init_lock_refuses_a_cairn_folder_that_is_a_link — lockfile_behind_link: true, false |
| 7 | test_init_lock_with_no_profile_still_writes_the_template — no parameters |
| 8 | test_init_lock_with_a_complete_profile_still_writes_the_lockfile — no parameters |
| 9 | test_init_lock_refuses_a_mapped_file_that_is_a_link — how: existing-outside-file, existing-inside-file, dangling |
| 10 | test_init_lock_refuses_a_mapped_file_below_a_linked_parent — no parameters |
| 11 | test_init_lock_migrates_an_ordinary_mapped_file_with_its_digest — no parameters |
| 12 | test_init_lock_with_a_lockfile_already_there_still_changes_nothing — no parameters |
| 13 | test_plan_and_stage_refuse_a_profile_that_is_a_link — flag: --plan, --stage; how: dangling-absolute, existing-outside-file, existing-inside-file |
| 14 | test_plan_and_stage_still_run_over_a_regular_or_absent_profile — flag: --plan, --stage; profile: regular, absent |
| 15 | test_adoptions_refuse_a_profile_that_is_a_link — action: adopt-collisions, adopt-module; how: existing-outside-file, existing-inside-file, dangling |
| 16 | test_adoptions_still_run_over_a_regular_or_absent_profile — profile: regular, absent; action: adopt-collisions, adopt-module |
| 17 | test_finalize_is_not_stopped_by_a_profile_that_is_a_link — how: existing-outside-file, dangling |
| 18 | test_a_lockfile_that_is_a_link_is_refused_and_never_written — what: valid-lockfile-elsewhere, json-that-is-no-lockfile, dangling |
| 19 | test_a_lockfile_link_swapped_in_after_the_check_is_never_written_through — no parameters |
| 20 | test_a_saved_commit_name_that_is_an_option_creates_nothing_through_the_command — no parameters |
| 21 | test_a_module_name_that_is_not_plain_text_is_refused_on_every_action — value: H, empty string, integer, null, list, U+2028, U+202E, NUL, U+009B |
| 22 | test_a_module_list_that_is_not_a_list_is_refused — modules: string, object, integer |
| 23 | test_a_lockfile_with_ordinary_module_names_is_not_refused — no parameters |
| 24 | test_apply_refuses_a_review_area_that_names_an_unplain_file — field: review_only, module_blocked, directory_blocked, directory_observed, expected_absent, staged_files; name: H, ../escape.md, /etc/hosts, integer, .git/description, .GIT/hooks/post-merge, .gIt./description, docs/.git /description |
| 25 | test_apply_refuses_a_review_area_whose_keys_are_not_plain_names — field: kinds, new_entries, recovery_bases, ancestor_evidence |
| 26 | test_apply_refuses_nested_metadata_paths_into_git_data — field/member: recovery_bases/old_base_cache, recovery_bases/new_base_cache, ancestor_evidence/src, ancestor_evidence/dst, ancestor_evidence/record_dst, ancestor_evidence/base_cache |
| 27 | test_apply_refuses_a_review_area_whose_version_is_not_plain_text — field: new_commit, new_version; value: H, integer, list, null |
| 28 | test_apply_refuses_a_review_area_whose_bookkeeping_has_the_wrong_shape — field: staged_files, review_only, kinds |
| 29 | test_apply_refuses_a_review_area_whose_metadata_is_not_an_object — metadata: empty list, list, integer, string, null |
| 30 | test_apply_still_applies_a_review_area_of_plain_names — no parameters |
| 31 | test_a_linked_project_folder_is_told_to_replace_the_link_not_restore_the_lockfile — no parameters |
| 32 | test_a_name_of_the_wrong_shape_keeps_the_restore_the_lockfile_advice — no parameters |
| 33 | test_a_linked_vendor_wrapper_is_not_taken_for_the_wrapper_by_finalize — no parameters |
| 34 | test_finalize_over_a_linked_vendor_wrapper_names_the_link — no parameters |
| 35 | test_finalize_over_an_absent_vendor_wrapper_keeps_its_plain_message — no parameters |
| 36 | test_a_record_that_names_a_file_inside_git_is_refused_on_every_action — field: dst, base_cache |
| 37 | test_a_contained_alias_into_git_data_is_refused_without_changing_it — no parameters |

**Remaining checks.** The Internal ordinary code review and High-tier Internal Security Review are owed. Wide Boundary B is also owed after those reviews, on a clean unchanged commit: the complete reviewed-range test selection for AGENTS.md, mapped readers, standing prose gates, and the trial controls and evidence. This record is an incomplete trial result, not a scope waiver or replacement authorization.

**Elapsed**: C0 broad-read driver 0.406 seconds; strict-profile child attempt 0.010 seconds; old install 0.129 seconds; clean-baseline reconstruction approximately 0.2 seconds. Candidate-install and root diagnostic timings were not retained. **Tokens**: unknown.
