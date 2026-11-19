# Re-anchor preparation record, 2026-11-13

**Role:** Reviewer/Implementation (Medium), read-only except this file.
**Model:** Claude Sonnet 5.5. **Elapsed:** about 45 minutes (estimate).
**Tokens:** unknown. **Read at:** `0.7-dev` tip `f4aff580`. **Authority:**
Maintainer chat, 2026-11-13: "Okay, I want these items powered through. LFG!"
and "Don't do extra testing. Just tight, only what was edited". This record
runs no tests, collection, signing, repin or ceremony command and moves no ref.

## Conclusion

1. **Three protected test files were deleted, not six.** They are
   `test_loader_identity.py` (8 test IDs), `test_lockfile_module.py` (7) and
   `test_slotmerge_leaf.py` (6): 21 IDs. Roadmap item 12 check (d) and the
   promise-testing plan's closeout say six; I could not reproduce six against
   the signed manifest. Every one of the 78 protected test files differs from
   the signed manifest: 75 edited, 3 deleted.
2. **2,466 of the 5,913 test IDs in the signed manifest no longer exist.**
   1,087 of them are in protected files. 1,966 IDs are new. The current total
   is about 5,413. This comes from the 2026-11-12 certification run's report,
   not from a fresh collection (see "What this did not check").
3. **The forward packet is stale in the mechanical sense and unchanged in
   content.** It is bound to `91e17bf1`; `HEAD` is 44 commits later, and the
   review and guide commands refuse unless `HEAD` equals the packet's
   candidate. None of the 32 files changed since touches the AST inputs, so a
   fresh packet at the final candidate should reproduce the same 21 symbol
   changes and 25 known-new changes. It needs fresh packet preparation and two
   fresh bound reviews, once, at the final candidate.
4. **The manifest has no field for a deletion.** A deleted file shows up only
   as absence from `frozen_files` and from the new collection. The roster file
   is byte-pinned (hard-coded digest), so the three deleted names stay in it
   unless the Maintainer decides on a new approved roster. The durable record
   of the deletions is this file plus the independent reader's record.
5. **Nothing here blocks the Maintainer's steps by itself,** but three
   decisions come first (section 4, steps 1 to 3).

## 1. What the re-anchor must record

The last re-anchor is `977b5250` ("Cairn forward trust baseline", signed,
2026-11-03 13:53). It signed candidate `56b9db59` and added only the manifest.
`refs/cairn/gate-anchor` in this clone points at it. The anchored manifest and
roster at `HEAD` are byte-identical to that commit's.

### Protected test files (90 roster paths: 78 test files, 12 control modules)

| State against the signed manifest | Files |
|---|---|
| Deleted | 3 (named above) |
| Renamed | 0 |
| Edited, test files | 75 |
| Edited, control modules | 3: `_oracle.py`, `conftest.py`, `security_manifest.py` |
| Unchanged, control modules | 9 |

Deleting commits: `26cf203b` (2026-11-11, batch B10) removed
`test_loader_identity.py` and `test_lockfile_module.py`; `64f4e973`
(2026-11-11) removed `test_slotmerge_leaf.py`. The roster fixture still lists
all three. The other frozen files: 22 non-test frozen files edited (scripts,
shipped modules, `bootstrap/security_check.py`), plus
`scripts/run_windows_interpreter_binding.py` and one fixture
(`fixtures/skills/README.md`). Against the signed manifest that is 102 edited
frozen files and 3 missing.

Not protected, but moved or deleted (24 paths; names in Appendix A): 14 deleted
(7 of them reappear under the same name in `contract/` or `integration/`) and
10 moved into `contract/`, `integration/`, `security/` or `unit/`.

### Test IDs ("node IDs") in protected files

The signed manifest pins 5,913 IDs, 4,213 of them in protected files.

| Protected-file IDs | Count |
|---|---|
| No longer exist, file deleted | 21 |
| No longer exist, file still present | 1,066 (64 files) |
| of which: function gone (660 plain, 389 parametrized) | 1,049 |
| of which: function still defined, ID changed (parametrization or class) | 17 |
| New IDs in protected files | 982 |

Whole manifest: 2,466 gone (1,087 protected, 1,379 ordinary), 1,966 new.
Against the signed manifest, the verifier would list each of the 1,087 as a
protected HOLD (`COLLECTION-DROPPED`); ordinary drops are notes only.

Which commit removed them (name level; 1,070 of 1,087 attributed, the 17 above
are not):

| Nodes | Commit |
|---|---|
| 162 | `64f4e973` Cut 167 tests; remove `test_slotmerge_leaf.py` |
| 117 | `e15b596e` J5: nine public promise tests replace 31 private tests |
| 98 / 89 | `71eee3ac` batch B12 / `d5f03fef` batch B13 (security stack, preflight) |
| 85 | `57f4ecaf` batch B14; remove `test_upgrade_module.py` |
| 69 / 59 / 16 / 26 / 19 | `d98ea3af` J2 / `55154dfc` J3 / `299a824e` J4 / `09e1d45d` J6 / `de414f9e` J1 |
| 68 / 54 / 39 | `26cf203b` B10 / `f24527b8` B11 / `d97d0800` B9 |
| 53 | `a2776c37` Cut 50 tests the open questions decided against |
| 15 / 13 / 13 / 12 | `aaaf4ab3` B6 / `4d892749` S1 / `5f1b7545` B4 / `ce55e4f4` upgrade removals |
| 63 | 26 smaller commits (8 or fewer each) |

All are 2026-11-05 to 2026-11-12. The per-file drop counts are in Appendix A.

## 2. The forward packet

Two packet folders exist, both under `/private/tmp` (local, not in Git):

| Folder | Candidate | Transaction SHA-256 (start) | Reviews |
|---|---|---|---|
| `cairn-v07-forward-20261113` | `d9708a0d` | `6f297c8a` | none; superseded |
| `cairn-v07-forward-final-20261113` | `91e17bf1` (2026-11-12 22:37) | `4cdae097` | ordinary ACCEPT, Security ACCEPT |

The final packet SHA-256 is `ca409bc7...`. Both reviews name that packet and
transaction. Content: 21 baseline symbol changes (config 4, lockfile 3, upgrade
8, install 5, cli 1), baseline membership unchanged at 169 keys, 10 known-new
additions and 15 rekeys, no drops, no lockfile output, outputs limited to the
two AST fixtures. Only 4 of the 21 symbols are in the self-service allowlist
(`_CORE_MAPPINGS`, `_MODULE_MAPPINGS`, `_SKILLS_MAPPINGS`, `install_onboarding`);
the other 17 are Maintainer-run corrections under
`bootstrap/AST_BASELINE_RUNBOOK.md` > "Who may perform it".

**Stale?** Mechanically yes: `forward_review` and `forward_guide` in
`scripts/repin.py` refuse when `HEAD` is not the packet's candidate ("prepare
fresh evidence"), and the packet carries the candidate's tree digest. The item
26 commits (archive `3ff9dbfa`) are not what makes it stale; any later commit
does, including the closing commits of items 27 to 29. Substantively no: between
`91e17bf1` and `HEAD`, `git diff` shows no change to `bootstrap/_scaffold/`,
both AST fixtures, `scripts/repin.py` or `bootstrap/tests/_ast_attest.py`
(the 12 tool-hash inputs). The 32 changed files are guidance, templates, the
lockfile, the board and archived records. The roadmap already says to refresh
once at the final candidate and reuse the unchanged body analysis.

## 3. What the independent readers must check

1. **Fresh packet equals the old one.** After `forward-prepare` at the final
   candidate, everything except the candidate id, tree digest and transaction
   head should match `91e17bf1`: the 21 `changed_symbols` (bodies, spans,
   digests), `known_new_delta`, the 46 summary lines, `fixture_hashes`, the 12
   `tool_hashes`, and each output's preimage and new SHA-256. Any difference
   means an engine or fixture commit landed; then re-read those symbols.
2. **Each of the 46 changes traces to a landed, reviewed plan.** The engine
   changed in 36 commits since the anchor (`9547bf74` code map through
   `3e0b39c3` denied binding parents); the runbook's step 1 asks for the trace.
   I did not trace symbol by symbol.
3. **Four authority files changed since the anchor,** so this is a transition
   in the runbook's sense: `bootstrap/REANCHOR_RUNBOOK.md` (+30 lines),
   `bootstrap/tests/_oracle.py` (+99), `scripts/repin.py` (+40) and
   `tools/session.py` (+416). Their 20 commits (11-04 to 11-12) go into the
   reader's tool-hash review.
4. **The package manifest matches expectations.** About 5,413 collected IDs
   (or an explanation); the three deleted names absent from `frozen_files`;
   the roster file identical to the external copy with SHA-256 `188fa76d...`;
   interpreter 3.13.13 and the recorded Python hash; `old_anchor_id` equal to
   `977b5250` (context only).
5. **The 1,087 protected-ID removals were intended.** They follow the
   promise-testing plan's cuts and conversions (Maintainer, 2026-11-11 and
   2026-11-12; `dev/PLANNING.md` decisions 14, 15, 16 and 18); the reader samples the
   commits above rather than re-reviewing 1,087 IDs, and checks that the 3
   deleted files are covered by those decisions.
6. **Skip and xfail markers.** The verifier would also HOLD on any protected
   node that gained a marker (`SKIP-XFAIL-NEW`). I did not compute this.

## 4. Steps that remain the Maintainer's

| # | Step | Where |
|---|---|---|
| 1 | Decision naming the exact candidate bytes, and choice of route (forward baseline or the ordinary ceremony) | `bootstrap/REANCHOR_RUNBOOK.md` > "Preparing the forward baseline" (the paragraph "Do not run this flow ... until a separate Maintainer Decision"); `bootstrap/AST_BASELINE_RUNBOOK.md` > "Who may perform it". No such Decision is recorded yet |
| 2 | Roster question: keep the 3 stale names, or approve a new roster (needs a new hard-coded digest at `bootstrap/tests/_gate_manifest.py:80-81` and the runbook's digest) | runbook, same section ("The approved test roster ..."); `scripts/repin.py:304` |
| 3 | Correct "six" to three in `dev/PLANNING.md` item 12(d) and the plan's closeout, or tell me which six | `dev/PLANNING.md` item 12 |
| 4 | Fresh `forward-prepare`, then two fresh `forward-review` records bound to the final candidate (agents prepare and read) | runbook, "Preparing the forward baseline" |
| 5 | `forward-guide`: approve the write, then the exact-path commit of the two fixtures | same |
| 6 | `baseline-reader-inputs`, reader's reviewed record, `baseline-prepare`, then compare digests with the reader | same |
| 7 | `baseline-install`: key, passphrase, one signed commit, moves branch and anchor locally | same; `bootstrap/REANCHOR_RUNBOOK.md` "The steps the tools cite" (RA-18) |
| 8 | Import-list refresh. I found no runbook step by this name; nearest are the closed tool lists `LISTED` and `VERIFIER_SCANNER_PATHS` in `scripts/repin.py` (lines 68 to 82), bound as packet `member` digests | confirm what is meant |
| 9 | Push both refs atomically, then read back with `ls-remote` | `bootstrap/REANCHOR_RUNBOOK.md`, the section "Phase 5" (publish, in one atomic push) |
| 10 | Release join (Mac and Windows records, then the join) | `SECURITY.md` > "Release security checklist" |
| 11 | Publish the fingerprint, sign and push the tag (`git tag -s`), release | `bootstrap/PROVENANCE.md` > "Relationship to the release cut" |

If the ordinary ceremony is chosen instead, the verifier against the signed
anchor would list 102 `FROZEN-MODIFIED`, 3 `FROZEN-MISSING` and 1,087
`COLLECTION-DROPPED` HOLDs, each needing a recorded disposition.

## 5. What this did not check

- No collection or test run. The ID comparison reads the certification report
  at `072d82d2` (5,413 cases, all mapped). Only two test files changed after it
  (`test_git_read.py`, `test_fork_advisory.py`), and neither changed a test
  name or parametrization. A fresh collection by the verifier is the exact
  figure.
- Skip and xfail marker changes; the AST classification at `HEAD` (inferred
  from byte-identical inputs, not re-derived); the remote's anchor
  (`origin` was not queried); the signer fingerprint against an independent
  source; the 36 engine commits symbol by symbol; whether each protected
  removal was individually reviewed.
- Whether the "import-list refresh" step exists under another name.

## Appendix A: exact lists

**Protected test files edited (75):** test_api_access_security, test_ast_attest,
test_board_json_contract, test_broad_run_guard, test_ceremony_review_report,
test_check_cairn_content, test_config_module, test_content_scan,
test_default_security_stance, test_doc_drift_tools,
test_engine_copy_fallback_contained, test_facade_loader_cleanup,
test_finalize_retired_living_state, test_fork_advisory, test_gate_manifest,
test_gate_preflight, test_gate_reanchor, test_gate_transition,
test_generated_output_scan, test_hardening, test_install_module,
test_intents_tool, test_manifest, test_module_merge_lockfile,
test_next_session_local_note, test_notice_install, test_oracle,
test_oracle_activation, test_oracle_trust, test_portable_security_sweeps,
test_profile_grammar, test_quality_gate_cli, test_quality_gate_neutrality,
test_quality_gate_order_independence, test_reanchor,
test_reanchor_driver_disclosures, test_repin, test_repin_ceremony,
test_replacement_tools, test_scaffold, test_scaffold_substrate,
test_security_capability_install, test_security_check,
test_security_finding_confidentiality, test_security_leaf, test_security_lint,
test_security_marker, test_security_net, test_security_stack,
test_security_verification, test_session_binding_gate_and_printing_hold,
test_session_binding_untracked, test_session_failsafe, test_session_kernel,
test_session_routines, test_session_start_drain_rules,
test_session_writes_contained, test_skills_fanout, test_skills_install,
test_skills_security, test_skills_self_heal, test_skills_upgrade,
test_status_vocabulary_advisory, test_upgrade, test_upgrade_added_slots,
test_upgrade_edit_check_runs_no_project_programs,
test_upgrade_lockfile_path_containment, test_upgrade_module_additions,
test_upgrade_refuses_hostile_project_data, test_upgrade_removes_retired_files,
test_upgrade_side_door_parity, test_verify_counts, test_verify_integrity,
test_verify_ref, test_web_hosting_security (all under `bootstrap/tests/`, `.py`).

**Protected IDs gone, by file still present (count):**
test_session_writes_contained 103, test_portable_security_sweeps 92,
test_upgrade_lockfile_path_containment 63, test_security_verification 62,
test_quality_gate_neutrality 59, test_verify_integrity 55,
test_security_stack 50, test_upgrade_refuses_hostile_project_data 46,
test_gate_preflight 44, test_upgrade_module_additions 31,
test_profile_grammar 27, test_content_scan 25, test_fork_advisory 23,
test_reanchor 23, test_security_net 23, test_security_check 22,
test_intents_tool 18, test_upgrade 16, test_repin_ceremony 14,
test_scaffold 14, test_upgrade_removes_retired_files 12, test_security_leaf 11,
and 10 or fewer in the remaining 42 files (sum 1,066 over 64 files).
The per-ID list (ID and removing commit) was written to the scratchpad
`reanchor-prep-dropped-protected-nodes-2026-11-13.tsv` and is not in Git; the
verifier's own `COLLECTION-DROPPED` lines are the authoritative list.

**Not protected, deleted (14):** test_certifying_run_rule, test_cli_module,
test_comprehension_floor, test_doc_governance, test_link_check_exclusions+,
test_model_tier_rule_ships, test_quality_gate_redundancy+,
test_review_and_verification_rules_ship, test_scientific_check_guidance_ships+,
test_stewardship_rules_ship+, test_test_tiers+, test_upgrade_module,
test_verification_boundaries+, test_writing_rules_ship+. (+ = a file of the
same name now exists in a new folder.)

**Not protected, moved (10):** test_cairn_prefix_links to contract/;
test_check_cairn_counts, test_claim_check_allow_config,
test_deleted_tracked_markdown, test_evolution_infer, test_prune_tools,
test_verify_stems to integration/; test_check_release_publication,
test_git_interpreter_binding_portable to security/; test_merge_module to unit/.
