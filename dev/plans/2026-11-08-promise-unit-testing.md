# Plan: Promise-unit testing

**Source proposal**: dev/proposals/archive/2026-11-08-claude-promise-unit-testing.md
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-08
**In brief**: Test component promises through their public entry points and give adopters the same practical guidance.

## Build summary

Pilot promise-based tests on upgrade, independently check the protection they retain, then apply the method to the eligible families and ship the guidance and advisory report. Security-sensitive removals receive an additional review before they land. The work produces evidence for a separate release re-anchor, not the re-anchor itself.

## Source proposal

The Maintainer accepted the heavy proposal at `0e1f9ae2`, including the widened adopter capabilities. The accepted change gives up tests catching only internal-only mutants; it does not waive protection of caller-visible behavior, including hostile input and timing.

## Scope

Change Cairn's governing `AGENTS.md` Verification rule and the corresponding shipped rule, testing-discipline module, core plan template, install specification and capability row. Add the standard-library advisory tool at its team-gated source and installed `scripts/` path. Convert the protected `bootstrap/tests/test_upgrade.py` pilot and then the eligible families, including `test_gate_preflight.py`, `test_reanchor.py`, `test_repin_ceremony.py`, `test_upgrade_removes_retired_files.py`, and security families. Promise lists live in test-file docstrings. Text-pin retirement belongs to the functional-prose plan; meter and claims-tool families remain on the board pending their respective Decisions. Hostile-state injection tests remain as declared exceptions.

Reuse: `rg` for mutation and upgrade tests found existing fixtures and public upgrade tests in `bootstrap/tests/test_upgrade.py`, and mutation examples in `bootstrap/tests/test_review_sweep_ships.py`; reuse suitable fixtures and entry points rather than build a parallel harness. The existing testing-discipline paragraph and install patterns are the homes for guidance and the tool. The proposal specifies path-only AST resolution and its failure behavior; use those contracts, without importing inspected modules. A new security or trust design beyond them needs high-tier design before execution.

## Sequence

One coherent outcome has three dependent internal chunks. Estimate 3–6 focused workdays, with substantial uncertainty from family inventory, defensive-site probes and review; this is not a deadline. The installed interpreter, existing tests and source are available. The implementation coordinator arranges the available Windows VM window and stages disposable committed source copies; fresh agents provide the independent probes and required reviews.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Inventory eligible families and pilot upgrade promises, retained checks and removal candidates; collect baseline counts and runtime. Convert the pilot and independently probe it. | Fresh high-tier Security Review agrees to the protected pilot removal set before removals land; independent old/new behavior-mutant check passes before C2 or C3. | Pilot tests, promise list and recorded evidence. |
| C2 | Apply the same method to each eligible family, ordered by private reach and runtime; independently inspect defensive sites for security families. | Fresh high-tier Security Review agrees to each security/high-risk removal set before it lands, and to every listed native-only node individually. | Reviewed removals and grouped evidence for the release owner. |
| C3 | After C1 passes, replace the rule, extend shipped guidance and plan prompt, and install the advisory tool. | Contract and forward tests pass. | Cairn and adopter capabilities. |

A reviewed expected AST mismatch from planned engine changes remains unpassed until the separate Maintainer-owned release baseline operation; unexpected drift and unexplained integrity failures remain implementation work. Record the human re-anchor and baseline operation as a separate named board wait with evidence, not as a plan completion condition. Archive requires all agent-owned work, reviews and checks; it grants no release authority.

## Acceptance criteria

**C1.** List upgrade's caller-visible promises, including refusals, and cover each through `scaffold.py --upgrade` or its public function. Record before/after collection, every removed node, counts and runtime. A fresh agent, without reading the tests, derives at least one behavior-changing mutant per promise and an accepting mutant per refusal from the list and `bootstrap/_scaffold/`. It runs each once against the old file from the commit before first removal and once against the new file. Any mutant caught by old and missed by new fails the pilot; restore or strengthen coverage and record the result. The retired-files test belongs to C2.

**C2.** For each eligible family, list promises, retain public-entry coverage, record counts, runtime and every removed node, and pass the same independent old/new mutant comparison. For security families the independent agent additionally derives an accepting mutant for each defensive check found in code, even if absent from the list. Treat every file guarding a security property or named high-risk surface as protected, whether or not the gate holds it. Before removal, obtain the family Security Review; require its node-by-node agreement for `NATIVE_ONLY_NODE_IDS` members and preserve a reason for each affected manifest member. Group protected removed nodes by promise with the retained check and mutant result; a node missing either is `stop` and stays. Ordinary drops are gate notes; protected drops are holds pending re-anchor. Do not remove a family that has not completed its checks.

**C3.** Both rules express the accepted promise, refactor, scaffolding, surviving-mutant, refusal and justified internal-test provisions, including hostile-state exceptions. Extend the existing testing paragraph, map each removed caller-visible fault to a retained check using behavior mutants, and include a pin-style before and the existing scientific-minimal test as after. The plan prompt asks which promise changes and which entry point checks it. A promise list is a module docstring line `Promises:` followed by at least one `- ` line. Resolve project imports by paths inside the project root outside tests, without imports; count `from m import _x` and `alias._x` for bound project modules. The advisory tool installs verbatim with its module and reports private reach and missing `Promises:` lists worst first, states that refusal and hostile-state injection tests stay, names its Python-only gap, and exits zero unless strict mode is requested. Its CLI tests cover project-module aliases and private imports, exclusions for local helpers, fixtures and dunders, missing lists, strict/non-strict exits, parse, recursion and decoding failures, escaped output, no import machinery, and out-of-root links reported without following. The scientific-minimal forward test has no private reach; five sampled upgrade tests agree with a hand count. The install test and `python bootstrap/scaffold.py --dry-run` demonstrate installation.

## Scope delta

**Scope delta**: preserved. The accepted internal-only mutant loss is explicit above; no broader fault criterion is waived. The source assigns text pins to the functional-prose work and fences meter and claims on their own Decisions.

## Verification

Boundary A: before implementation use `python tools/test_tiers.py for <paths>` and run the deduplicated tests naming changed files, with the complete reviewed range for governing text. Map changed behavior, callers and consumers to existing test homes; run standing claim, link, snippet and neutrality gates for prose. The independent mutant agent uses isolated copies of the old and new committed files, one probe per mutant per file; retain repeatable probes in tests or scripts and summarize outcomes and omissions. Do not replay broad tests for each mutation.

For C2 native-only evidence, the implementation coordinator uses the available `cairn-windows` SSH host (Windows 11 ARM64, `C:\ProgramData\miniconda3\python.exe` 3.13.17). Transfer disposable exact committed old and new source copies and verify their commits and source hashes. In the activated Miniconda environment, run `scripts/run_windows_interpreter_binding.py` for its binding family: its DLL path, Git, pytest and symlink privilege prerequisites must hold. Also run the exact applicable Windows `NATIVE_ONLY_NODE_IDS` for eligible code-map and interpreter-binding families, and each independent old/new mutant through its actual public entry point on Windows. Retain commands, node IDs, interpreter, hashes, old/new results and skips in the plan evidence; use existing runners and canonical test homes for reproducible probes. A host skip, missing prerequisite, unmatched native probe or absent evidence is unpassed and stops that family’s removals. An equivalent probe must exercise the actual public behavior. No human trial or broad Windows suite is a prerequisite.

Boundary B: **wide**, on a clean final reviewed commit under `/Users/kendal30/conda_envs/lhm/bin/python3.13`, after code review and fixes. Run the deduplicated iteration list for the whole reviewed range plus tier-map integration/workflow tests naming those files, the acceptance commands above and applicable security and trust-ceremony checks. Record SHA and range, interpreter, pre/post state, commands, counts, elapsed time, omissions and non-passes; record timing misses and the over-10-second files on the consolidation list. Boundary C is independent code-review falsification, including targeted checks and explicit coverage gaps. The Security Review for each removal set is in addition to ordinary review. The release certification and re-anchor are separate; neither substitutes for a failed change check.

## Plan review -- GPT-6.1 Terra (Reviewer) -- 2026-11-08

Reviewed commit: 864b5a783c7efd7d6116d3cac0f6c61f7206fe83

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: APPROVE
**Elapsed**: approximately 3 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: C1 tests upgrade promises and refusals against the old file, C2 carries the comparison and independent defensive-site probes into later families, and C3 ships the accepted adopter capabilities after the pilot; protected removals receive the separate reviews and evidence the Decision requires. -- Plan Scope, Sequence and C1–C3; accepted proposal Outcomes 2–4 and Decision.
2. **Best alternative.** Keep inventory as C1's internal step and reuse the existing tests and guidance: a pilot-only delivery would lose the accepted later-family work and adopter tool, while a separate inventory plan would add a dependency without delivering the outcome. -- Plan Sequence and Reuse; `test_upgrade.py` and `testing-discipline.md` at the reviewed commit.
3. **What would show it wrong?** A pilot mutant caught by the old file but missed by the new one, or a tool false positive on the scientific example or sampled upgrade tests, would fail its stated gate and require repair. -- Plan C1 and C3.

The plan explicitly preserves hostile-state and caller-visible fault coverage while recording the Maintainer's narrower acceptance of internal-only mutant loss. It assigns text pins to functional prose, leaves meter and claims behind their Decisions, and keeps the human release baseline operation outside archive while retaining failed checks as implementation work. -- Plan Scope, Scope delta and Verification; accepted proposal Outcome 3.

**Coverage:** Compared the committed plan with the accepted proposal, its widening and Decision, and inspected the named reuse homes and plan template. Did not execute implementation checks, enumerate future removal families, or perform the separately required Security Review; no suite was run.

## Plan review -- GPT-6.1 Sol (Security Review) -- 2026-11-08

Reviewed commit: 864b5a783c7efd7d6116d3cac0f6c61f7206fe83

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: approximately 8 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes, with the native execution prerequisite repaired: C1/C2 preserve caller-visible refusals through independent old/new probes, defensive-site enumeration and removal-set Security Review; the accepted loss concerns internal-only mutants. -- Plan C1/C2; source Outcomes 2/3 and Decision.
2. **Best alternative.** Reuse the existing native probe route within C2 rather than add another approval or defer an eligible family; keep node-level reviewer agreement and the existing human release ceremony. -- Plan Sequence/C2; source Outcome 3; finding 1.
3. **What would show it wrong?** An accepting mutant for a Windows reparse refusal caught by the old file but missed by the replacement would falsify retained protection; a skipped native probe establishes neither result. -- Plan C2; `bootstrap/tests/security/test_git_interpreter_binding_portable.py:397`.

**Finding 1 -- Blocking: specify the native evidence route.** C2 promises completed independent old/new probes for every eligible family, but Verification names only the local canonical interpreter. The committed code-map tests at lines 492, 516, 527 and 584 require native Windows; the interpreter-binding reparse test at line 397 does too. These non-meter security families are eligible, and local skips cannot prove their refusal coverage. Close by naming the available native execution route, its prerequisite/owner and how committed old/new probe evidence is retained; an equivalent probe must exercise the actual public behavior. Keep unmatched checks unpassed and their removals stopped. This requests execution detail for accepted checks, not a new human gate.

C3's path-only resolution, no imports, escaped output and reported parse/link failures bound the advisory tool without executing inspected projects. Source/shipped rules, module, template and install coverage are named. Expected reviewed AST mismatch remains separate from actual failed checks; release authority is preserved.

**Coverage:** Read the committed plan, accepted source and reviews/Decision, plan template, security manifest and native test guards, safety/runbook provisions. Did not enumerate every defensive site, validate future removals or run tests; those remain implementation and removal-review evidence. No suite run. Over target to explain the native dependency and its closure without adding a gate.

## Plan review response -- GPT-6.1 Terra (Implementation) -- 2026-11-08

**Elapsed**: approximately 5 minutes. **Tokens**: unknown.

- Ordinary review: no findings.
- Security finding 1, accepted: Sequence assigns the VM window and committed source staging; Verification names the Windows interpreter, existing binding runner and prerequisites, applicable native nodes, public-entry mutant probes, evidence and stop conditions. Skips do not establish coverage.

## C1 promise inventory -- GPT-6 Luna (LowImplementation) -- 2026-11-08

**Elapsed**: approximately 45 minutes. **Tokens**: unknown.

The module docstring in `bootstrap/tests/test_upgrade.py` now lists its
caller-visible installation, profile, upgrade, refusal, migration, finalizing,
manifest-citation and module-adoption promises. Public checks include
`TestLockfile::test_install_refuses_secret_shaped_profile_values` through
`scaffold.py` for the nine refusal inputs;
`TestUpgradeModes::test_plan_reports_clean_untouched_after_upstream_advance`
through `s.main --plan`;
`TestManifestHomeAndSelfHeal::test_plan_reports_citation_status_through_public_command`
through its warning; `::test_apply_self_heal_preserves_present_profile_or_skips_stub`
through `s.main --apply`; and
`TestTrackedDirectoryCollisions::test_finalize_prefers_custom_wrapper_file_to_known_name_directory`
through `s.main --finalize`. Existing public checks cover the other promise
groups below.

**Retained public-entry coverage by promise:** installation/lock records:
`TestLockfile::test_round_trip`, `::test_base_cache_is_raw_mergeable_only`,
`::test_fail_closed_on_divergence`; profile selection/content:
`TestProfileSizedAssembly::test_solo_strips_region_lockfile_and_verify_clean`,
`::test_multi_keeps_region_lockfile_and_verify_clean`,
`::test_profile_change_solo_to_multi_reincludes_region`, and the four
`TestTemplateGatingSafety` checks; merge and plan behavior:
`TestUpgradeModes::test_plan_writes_nothing`, `::test_stage_then_apply`,
`::test_plan_summary_shows_distinct_labels`,
`::test_plan_reports_clean_untouched_after_upstream_advance`, plus public
`parse_slots`/`merge_file` checks in `TestSlotParser` and `TestMerge`; refusal
and recovery: `TestUpgradeModes::test_apply_rejects_stale_stage`,
`::test_apply_rejects_changed_ancestor_since_stage`,
`::test_apply_rejects_changed_digest_since_stage`,
`::test_apply_rejects_conflict_markers`, `::test_apply_rejects_corrupt_stage`,
`::test_apply_keeps_path_and_exact_set_refusals`, and `TestReviewOnlyMerge`;
migration: public `s.main` cases in `TestInitLock` and
`TestInitLockFullProfile`; manifest citation: the public `--plan` case above
and init-lock source recovery; profile self-heal: `::test_self_heal_through_apply_not_stage` and `::test_apply_self_heal_preserves_present_profile_or_skips_stub`;
module adoption: public `s.main` cases in `TestAdoptModule`; wrapper/finalize/
tracked state: `TestUpgradeModes::test_renamed_wrapper_apply_advances_to_resolved_dst`,
`TestFinalizeDirtyTreeGuard`, the new custom-wrapper finalize node, and public
stage/apply checks in `TestDirtyTreeGuard` and `TestTrackedDirectoryCollisions`.
Hostile-state injection remains in place. Literal-pathspec and terminal-output
encoding remain as seam-specific checks; the Windows discovery test runs the
public command with simulated native path spelling.

**Proposed protected removal set (one grouped Security Review; no removals in
this commit):**

| Promise group | Candidate nodes | Retained public fault check |
|---|---|---|
| Secret-shaped install values refuse | `TestLockfile::test_secret_token_guard` | `TestLockfile::test_install_refuses_secret_shaped_profile_values` checks all nine inputs through `scaffold.py`; ordinary install nodes cover benign values. The allow-list parameter is internal-only. |
| Local-merge and untouched plan labels | `TestUpgradeModes::test_locally_modified_merged_clean_classified_distinctly`; `::test_clean_untouched_when_ours_equals_base` | `TestUpgradeModes::test_plan_summary_shows_distinct_labels` and `::test_plan_reports_clean_untouched_after_upstream_advance` check both labels through `s.main --plan`; `::test_stage_then_apply` covers the merge transition. |
| Renamed wrapper resolves through upgrade | `TestUpgradeModes::test_renamed_vendor_wrapper_resolves_on_standard_upgrade` | `TestUpgradeModes::test_renamed_wrapper_apply_advances_to_resolved_dst`; `TestFinalizeDirtyTreeGuard::test_scoped_finalize_renamed_wrapper_by_recorded_name`. |
| Review-only files never advance | `TestReviewOnlyMerge::test_review_only_never_in_advancing_set` | `TestReviewOnlyMerge::test_stage_review_only_file_missing_only_theirs`, `::test_apply_fail_closes_on_review_only`, and `::test_apply_ack_review_only_overrides_and_cleans` check staging, refusal and unchanged lock hash through `s.main`. |
| Fidelity citation warning/home precedence | `TestManifestHomeAndSelfHeal::test_r10_finds_manifest_in_cairn_home`; `::test_r10_legacy_strategy_fallback`; `::test_r10_prefers_cairn_over_legacy` | `TestManifestHomeAndSelfHeal::test_plan_reports_citation_status_through_public_command` checks current, stale, legacy fallback and canonical-home precedence via `s.main --plan`; init-lock recovery is public too. |
| Self-heal only from a complete profile | `TestManifestHomeAndSelfHeal::test_self_heal_materializes_when_absent`; `::test_self_heal_noop_when_present`; `::test_self_heal_noop_on_empty_lockfile_profile` | `TestManifestHomeAndSelfHeal::test_self_heal_through_apply_not_stage` checks creation only on apply; `::test_apply_self_heal_preserves_present_profile_or_skips_stub` checks non-clobber and no fabrication from an empty embedded profile. |
| Custom wrapper file precedes known-name directory | `TestTrackedDirectoryCollisions::test_custom_wrapper_file_precedes_known_wrapper_directory` | `TestTrackedDirectoryCollisions::test_finalize_prefers_custom_wrapper_file_to_known_name_directory` checks the destination and hash via `s.main --finalize`. |

These 12 nodes are proposed for the required fresh high-tier Security Review
to accept or reject as one grouped removal set; no protected check was removed
or replaced before that review. The independent old/new behavior-mutant check
remains required and has not run. Literal-pathspec, terminal-encoding and
fork-detection checks stay outside this set because the mapped public checks
do not yet cover those faults or the tests inject seam-specific conditions.

**Collection and timing evidence:** at base `5ced3b3efc7d02eca81c62a4443c7de9005e493a`,
the file SHA-256 was
`cfc7f1db0d0d74de504e9df187048adc1370765947ad30c2dd0531643cf79c2b`;
AST inspection found 131 test-function definitions and collection found 159
parameter-expanded items under Python 3.12.9 before the additions. The AST
inventory found 64 functions with direct private-module reach/imports (61 with
`s._...`/`verify_integrity._...` attributes, four private imports, one overlap).
Five public test functions add 14 collected items; removals have not occurred.
They are `TestLockfile::test_install_refuses_secret_shaped_profile_values`
(nine inputs), `TestUpgradeModes::test_plan_reports_clean_untouched_after_upstream_advance`,
`TestManifestHomeAndSelfHeal::test_plan_reports_citation_status_through_public_command`,
`::test_apply_self_heal_preserves_present_profile_or_skips_stub` (two profile
states), and
`TestTrackedDirectoryCollisions::test_finalize_prefers_custom_wrapper_file_to_known_name_directory`.
The resulting file has 136 function definitions and 173 collected items under
canonical Python 3.13.13 (`pytest --collect-only -qq`). Thus the 14 added items
are distinct from the original 159-item planning count; the original count was
collected under Python 3.12.9 and is not the canonical baseline. If all 12
proposed nodes are later approved and removed, the projection is 124 functions
and 161 items; actual post-removal counts remain due. The targeted selection
ran 20 items: 20 passed in 5.57 s total. The five added public functions
account for about 3.0 s summed call time; the nine secret-input cases each took
under 0.005 s. The plan's prior `ecd787e6` timing is 89.068 seconds of summed
case time under Python 3.13.13, planning data only. `claim_check` and
`link_check` each passed on the plan, snippet sync passed on the plan, and the
neutrality gate reported fail=0, info=43. No broad file baseline was run here;
the coordinator is running a separate clean baseline on the old, unmodified
file at `28f79683`, to be joined to this record when available. The expected
AST fixture was not applied or re-anchored.

**Coverage:** read the accepted proposal and Decision, both plan reviews and
response, the current plan template, `test_upgrade.py`, and mapped public paths
and retention checks. Ran canonical collection and targeted checks for the
new public tests and proposed retained nodes; did not remove tests, run the
broad file baseline, mutate source, perform Security Review or run independent
mutant probes. The linked-worktree `session-start` helper reported “not inside
a git repository”; ordinary Git inspection works with fsmonitor disabled and
the coordinator confirmed the helper limitation. The first probe fixture
used a VENDOR wrapper without a usable merge base; the second omitted the
changed `base_hash`. The affected test now
uses mergeable `NOTICE.md`, updates its base hash, and passes on Python 3.13.13.

## C1 removal-set Security Review -- GPT-6.1 Sol (High) -- 2026-11-08

**Foundations**

1. **Should this happen as framed?** Ten removals have retained public checks; two lack equivalent caller-visible coverage, so the proposed twelve-node set must change before it lands. -- C1 inventory; findings 1–2 below.
2. **Best alternative.** Land the ten agreed removals and retain the two held nodes until their public replacements cover the named gaps; this preserves the accepted outcome without another mechanism. -- Node verdicts below; `write_install_lockfile` and upgrade classification callers.
3. **What would show it wrong?** A directory-first resolver mutant already fails the old node but passes its proposed finalize replacement; the independent blind old/new behavior-mutant comparison must still test every promise and refusal before C2/C3. -- Finding 2; plan C1.

**Reviewed commit**: `5dabd13ffe1df6e96db0d859d30c8c9639811b12`.
**Obligation**: C1 protected removal-set Security Review, not final code review.
**Verdict**: AGREE to the ten named nodes; HOLD the other two.
**Elapsed**: approximately 10 minutes. **Tokens**: unknown.

**Finding 1 -- Blocking for the secret node.** The new nine-input CLI check refuses unknown profile keys in `config.py::load_config`, before `cli.py` filters tokens through `KNOWN_TOKENS`. A direct `api_token` config probe confirmed `ProfileGrammarError`. This does not cover public `scaffold.write_install_lockfile`, exported at `bootstrap/_scaffold/__init__.py:200`: it accepts a supplied token mapping and calls the secret guard before writing (`install.py:2134`). Its `allow_secret_tokens` parameter is public too; the inventory's internal-only claim is unsupported. Close with writer-entry refusal/non-mutation checks for the nine spellings and its explicit allowance, or retain the node. The retained adoption check arranges only `api_secret_key`.

**Finding 2 -- Blocking for the custom-wrapper node.** Finalize calls `_resolve_vendor_wrapper` with its default false mode; the old node uses `include_directories=True`, as real plan/stage classification and apply observation do (`upgrade.py:823,3428`). In a separate archive of the reviewed commit, moving known-directory resolution before custom-file resolution only in that mode made the old node fail (0.58 s) while the new finalize node passed (0.34 s), Python 3.13.13. Close with a public plan/stage check that a custom wrapper file wins over a known-name directory, or retain the node. This targeted falsification is not the blind comparison.

**Exact node verdicts** (all in `bootstrap/tests/test_upgrade.py`):

| Node | Verdict |
|---|---|
| `TestLockfile::test_secret_token_guard` | HOLD, finding 1 |
| `TestUpgradeModes::test_locally_modified_merged_clean_classified_distinctly` | AGREE |
| `TestUpgradeModes::test_clean_untouched_when_ours_equals_base` | AGREE |
| `TestUpgradeModes::test_renamed_vendor_wrapper_resolves_on_standard_upgrade` | AGREE |
| `TestReviewOnlyMerge::test_review_only_never_in_advancing_set` | AGREE |
| `TestManifestHomeAndSelfHeal::test_r10_finds_manifest_in_cairn_home` | AGREE |
| `TestManifestHomeAndSelfHeal::test_r10_legacy_strategy_fallback` | AGREE |
| `TestManifestHomeAndSelfHeal::test_r10_prefers_cairn_over_legacy` | AGREE |
| `TestManifestHomeAndSelfHeal::test_self_heal_materializes_when_absent` | AGREE |
| `TestManifestHomeAndSelfHeal::test_self_heal_noop_when_present` | AGREE |
| `TestManifestHomeAndSelfHeal::test_self_heal_noop_on_empty_lockfile_profile` | AGREE |
| `TestTrackedDirectoryCollisions::test_custom_wrapper_file_precedes_known_wrapper_directory` | HOLD, finding 2 |

**Coverage:** Compared committed candidate/old nodes and retained checks with accepted source, plan/template and engine entry paths, including self-heal before apply's stage validation. Ran only the tight config and two-node resolver falsification above, in disposable copies; the repeatable probe is at `/private/tmp/cairn-promise-removal-sol-probe.py`. Did not run a suite, repeat the twenty implementation cases, perform the independent blind comparison, validate C2/C3 or discharge final ordinary/Security code review, Boundary B, baseline or re-anchor holds. Over target to retain exact node verdicts and explain both public-route gaps.

## C1 Security Review response -- GPT-6 Luna (LowImplementation) -- 2026-11-08

**Finding 1:** Replaced the nine-case CLI profile test, which stopped at unknown
key validation, with `TestLockfile::test_public_writer_refuses_secret_tokens_without_writing_state`.
It calls the public `scaffold.write_install_lockfile` on one valid installed
tree for all nine spellings, checks the lock and base cache stay byte-identical
after each refusal, and verifies the public `allow_secret_tokens` argument
accepts a harmless fake `apiKey` value. The earlier claim that the allowance
was internal-only is withdrawn. The retained private guard node remains in
place pending targeted High agreement.

**Finding 2:** Added
`TestTrackedDirectoryCollisions::test_plan_prefers_custom_wrapper_file_to_known_name_directory`.
It uses public `s.main upgrade --plan` with `CUSTOM.md` importing `@AGENTS.md`
and a `CLAUDE.md` directory, then checks the plan resolves the custom file and
does not classify the known-name directory as the wrapper. The finalize check
is supplemental only; the original helper node remains pending targeted High
agreement.

Corrected mapping for the proposed grouped removal set: the secret refusal row
maps to the public writer test above plus retained benign install coverage; the
custom-wrapper row maps to the public plan test above. The other ten previously
agreed nodes and their mappings are unchanged. This response removes or
replaces no protected test. The original 159 collected items remain; canonical
Python 3.13.13 collection is now 166 items (137 test functions), a net seven
additions after replacing nine CLI cases with one writer case and adding one
plan case. The two new public tests pass: 2 passed in 0.88 s, with call times
0.38 s (writer) and 0.47 s (plan). Tokens: unknown. Elapsed time:
approximately 12 minutes. No broad upgrade run, removals, Security Review, or
blind behavior-mutant comparison was performed in this response. Targeted High
follow-up remains required before removing either held node.

## C1 removal-set Security Review follow-up -- GPT-6.1 Sol (High) -- 2026-11-08

**Foundations**

1. **Should this happen as framed?** Yes: both repaired replacements reach the previously missing public paths, closing findings 1–2 without conceding caller-visible protection. -- `test_upgrade.py::TestLockfile::test_public_writer_refuses_secret_tokens_without_writing_state` and `::TestTrackedDirectoryCollisions::test_plan_prefers_custom_wrapper_file_to_known_name_directory`.
2. **Best alternative.** Use these public replacements and the ten earlier agreed mappings; retaining the two helper checks would duplicate the newly demonstrated fault detection. -- Reviewed diff from `aa3b0acd` to `b8520f25`; targeted mutations below.
3. **What would show it wrong?** The required blind old/new comparison could still reveal a lost behavior or refusal; these two targeted mutants establish only the repaired routes, not the full pilot. -- Plan C1; follow-up probe results below.

**Reviewed commit**: `b8520f253f5f7036d84f9c58a21ce29b859242c8`.
**Obligation**: targeted second removal-set Security Review for newly changed material addressing findings 1–2.
**Verdict**: both findings CLOSED; AGREE to removing `TestLockfile::test_secret_token_guard` and `TestTrackedDirectoryCollisions::test_custom_wrapper_file_precedes_known_wrapper_directory`. The earlier ten agreements stand; all twelve proposed nodes now have removal-set agreement.
**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

Finding 1's replacement calls the public writer with all nine names, checks each refusal leaves lock/cache bytes unchanged, and demonstrates successful explicit allowance on the same valid install. Finding 2's replacement invokes real `upgrade --plan`, reaching directory-aware classification and requiring the custom wrapper in its report.

In separate archives of the reviewed commit, disabling the secret guard made the writer replacement fail at its expected exception (0.70 s); the earlier directory-first mutant made the plan replacement fail at its custom-wrapper assertion (0.86 s), canonical Python 3.13.13. Both targeted mutants were caught. Repeatable probe: `/private/tmp/cairn-promise-removal-sol-followup-probe.py`.

**Coverage:** Read only the committed two-finding repair, response and relevant engine paths; ran the two targeted falsifications in separate disposable copies. Did not replay passing implementation checks or run a suite. This pass does not discharge the independent blind comparison, final ordinary/Security code review, Boundary B, baseline or re-anchor holds; no removals occurred during review. Over target to preserve both route closures and probe limits.

## C1 agreed pilot removals -- GPT-6 Luna (LowImplementation) -- 2026-11-08

Removed exactly the twelve nodes agreed in the grouped Security Review at
`65a8ef7f`:

- `TestLockfile::test_secret_token_guard`
- `TestUpgradeModes::test_locally_modified_merged_clean_classified_distinctly`
- `TestUpgradeModes::test_clean_untouched_when_ours_equals_base`
- `TestUpgradeModes::test_renamed_vendor_wrapper_resolves_on_standard_upgrade`
- `TestReviewOnlyMerge::test_review_only_never_in_advancing_set`
- `TestManifestHomeAndSelfHeal::test_r10_finds_manifest_in_cairn_home`
- `TestManifestHomeAndSelfHeal::test_r10_legacy_strategy_fallback`
- `TestManifestHomeAndSelfHeal::test_r10_prefers_cairn_over_legacy`
- `TestManifestHomeAndSelfHeal::test_self_heal_materializes_when_absent`
- `TestManifestHomeAndSelfHeal::test_self_heal_noop_when_present`
- `TestManifestHomeAndSelfHeal::test_self_heal_noop_on_empty_lockfile_profile`
- `TestTrackedDirectoryCollisions::test_custom_wrapper_file_precedes_known_wrapper_directory`

The module promise now describes refusal by secret-shaped token **names** and
names the public writer's explicit `allow_secret_tokens` list. No other test
node was removed; retained public checks, including the writer, plan and
finalize replacements, remain.

Canonical Python 3.13.13 collection changed from 166 items / 137 test
functions to 154 / 125. The coordinator's clean pre-removal run on
`28f79683` (source file SHA-256
`cfc7f1db0d0d74de504e9df187048adc1370765947ad30c2dd0531643cf79c2b`) collected
and passed 159 items with no skips or failures; summed case time was 93.204 s,
not file wall time. These 12 one-item nodes reduce the 166-item candidate by
12; prior additions account for the difference from the old baseline.

Focused retained/new public checks: 16 passed, no skips, in 7.94 s under
Python 3.13.13. This covered the writer refusal/allow-list, public plan labels
and untouched state, stage/apply merge, renamed wrapper apply/finalize,
review-only stage/apply/refusal, citation reporting, profile self-heal, wrapper
plan/finalize and module-adoption secret-name refusal. Tokens: unknown.
Elapsed: approximately 10 minutes. The new-file baseline and independent blind
old/new behavior-mutant comparison remain pending with the coordinator; no
whole-file or mapped-family run was performed here. These results do not
complete C1 or authorize C2/C3.

## Maintainer Decision amendment notice -- Claude Opus 5.5 (Strategy) -- 2026-11-08

Relayed at the Maintainer's request; they cannot reach this plan's agent
directly. This is a notice, not an edit to operative cells: the Scope delta
and its placement remain the plan author's.

Commit `0d2fc71f` on `0.7-dev` appends a Decision amendment to both archived
source proposals. The Maintainer's authorization, verbatim:

> "Move the testing rule out of AGENTS.md into the templates and testing module; keep the editing rule to one sentence"

For this plan: neither `AGENTS.md` gains the promise rule. Its homes are a
short promise prompt in the core plan template's acceptance and
verification sections, the proposal template's "Tests required" slot (light
work has no plan), the code-review section ("does any new test pin
internals rather than a promise?"), and the full guidance in
`testing-discipline.md`. The templates carry the prompt themselves because
the `solo-greenfield` preset does not install the testing module. Strategy
recommends, beyond the amendment's words, moving the existing `AGENTS.md`
sentence "Add or extend a test only for a plausible uncovered fault" into
those prompts too. Record the Scope delta here.

**Elapsed**: under 5 minutes. **Tokens**: unknown.

## C1 independent behavior-mutant comparison -- GPT-6.1 Sol -- 2026-11-08

**Role:** independent falsification, High GPT-6.1 Sol; this is neither code
review nor removal-set Security Review. **Elapsed:** approximately 20 minutes;
**tokens:** unknown. **Result:** no old-caught/new-missed mutant found, but the
read-only plan promise remains unpassed and requires a stronger public check
before C2/C3.

Before reading tests, logs, reviews, mappings or removals, I read AGENTS, the
nine sealed promises (SHA-256
`665fddeff4313e97a33dc0240a1bedc412bf5af0d73294f129d417b5426a45fe`)
and engine source at `ce55e4f4`. I sealed 13 exact source replacements with
locations and public-behavior explanations. Their unchanged seal is
`bootstrap/tests/fixtures/upgrade_promise_mutants.json`, SHA-256
`0043a66b0356dbafe48c38a4d4cb0e45bb57a63af5073d3e98b199693c819ab0`.
It covers each promise and includes accepting mutants for refusal promises
4, 8 and 9. The seal was sent to the coordinator before test inspection.

Compared old `5ced3b3e` with new `ce55e4f4`. The old test file's SHA-256 is
`cfc7f1db0d0d74de504e9df187048adc1370765947ad30c2dd0531643cf79c2b`;
`git diff 5ced3b3e ce55e4f4 -- bootstrap/scaffold.py bootstrap/_scaffold`
was empty. Separate clean Git clones supplied each committed source version.
Using `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13), each of the 13
selected probes first passed unmutated, then ran once mutated in each clone:
26 healthy baselines and 26 initial mutation executions, 69.585 seconds total.
Every mutant reached its changed source line and a test call; none was counted
from import, setup or collection failure. Both clones were clean after patch
restoration. These are targeted probe figures, not family timing evidence.

| Sealed mutant | Old | New |
|---|---|---|
| P1-hash: wrong installed digest | caught | caught |
| P2-profile: ignore changed profile | caught | caught |
| P3-plan-write: write an extra project file | survived | survived |
| P4-valid-noop: claim successful apply without applying | caught | caught |
| P4-accept-conflict: allow unresolved marker bytes | caught | caught |
| P5-migration-tokens: discard recovered profile tokens | caught | caught |
| P6-citation: suppress stale citation | caught | caught |
| P6-precedence: prefer legacy manifest | caught | caught |
| P7-base: overwrite upstream fork baseline on finalize | caught | caught |
| P8-preserve: overwrite adopted custom content | caught* | caught* |
| P8-accept-unknown: record unknown module | caught | caught |
| P9-allow: ignore explicit secret-name allow-list | caught | caught |
| P9-accept-secret: allow secret-shaped token names | caught | caught |

*The first P8 selection, `test_adopt_records_on_disk_content_not_template`,
survived in both versions: recording the new on-disk hash does not prove the
original bytes survived. I preserved that result and ran the neighboring
public content/advisory witness once per version, each with a green baseline:
`TestAdoptModule::test_adopt_advisory_fires_when_kept_file_differs` caught the
mutation in both. That is probe-selection repair, not a coverage regression.

**Unclosed promise gap:** `TestUpgradeModes::test_plan_writes_nothing` only
asserts absence of the staging directory. P3 adds `cairn-plan-mutant-write`
elsewhere and survives both versions. A separate public CLI reproduction in
each clone installed normally, then ran the mutated `bootstrap/scaffold.py
upgrade --target <project> --plan --cairn-root <source>`: both returned zero
and created exactly that additional file containing `changed`. The existing
check cannot establish read-only behavior. Closure requires a public plan
check that compares all project entries and file bytes, then catches this
sealed mutant. Agreement between old and new does not waive the promise.

`scripts/replay_upgrade_promise_mutants.py` retains the exact node mapping and
bounded replay, including healthy baseline, changed-line reach, test-phase
checks, restored source and the P3 file side effect. It uses the stronger P8
witness. Run it with separate clean old/new checkouts and `--output` outside
the repository; `--only P3-plan-write` selects the remaining gap. A surviving
public-behavior mutant exits nonzero. Initial results, supplementary P8
results and CLI demonstrations were retained under
`/private/tmp/cairn-mutant-results-ce55`; replay does not require those logs.
The canonical helper's P3-only execution reproduced both surviving writes.

**Coverage and omissions:** all nine sealed promises received independently
derived mutants; accepting refusals cover conflict markers, unknown modules
and secret-shaped tokens. This is not an exhaustive defensive-site sweep;
other stale/corrupt/path/dirty/filesystem defenses were not independently
mutated in this C1 pass. No whole-file mutant replay, full suite, native
Windows run, release attestation, baseline change, re-anchor or push occurred.
The coordinator owns the separate new-family baseline and later reviews.

Replay-support checks: `tools/test_tiers.py for` the two support paths and this
plan selected zero test files; no test selection was widened. The helper's
P8-only replay passed with both mutations caught, while its P3-only replay
measured both writes. Claim, link and snippet/content checks on this plan
passed; the standing neutrality gate reported zero failures. These support
checks do not close P3 or replace the final reviewed-commit Boundary B run.

## Authorized C3 Scope delta -- GPT-6 Luna (LowImplementation) -- 2026-11-08

Maintainer Decision amendment `0d2fc71f` applies to this plan. The
authorization, quoted verbatim from the two archived source proposals:

> "Move the testing rule out of AGENTS.md into the templates and testing module; keep the editing rule to one sentence"

For C3, place promise-testing guidance in the proposal and plan templates and
the testing module; add no promise-testing paragraph to `AGENTS.md`. Preserve
the accepted outcomes and tier, and preserve verification rules already in
force. The editing rule remains one sentence. This authorized placement
clarifies the plan's existing doctrine/template/module work and adds no new
behavior. C3 implementation has not begun; this delta does not waive C1's P3
closure, the clean new-file baseline, the blind comparison, or later reviews.
Source: `dev/proposals/archive/2026-11-08-claude-promise-unit-testing.md`,
Decision amendment at commit `0d2fc71f`; relayed in plan notice at `7d4b4cd6`.
Tokens: unknown. Elapsed time: unknown.

## C1 P3 read-only-plan closure -- GPT-6 Luna (LowImplementation) -- 2026-11-08

`TestUpgradeModes::test_plan_writes_nothing` now snapshots the project root
and every descendant before and after the public `upgrade --plan` call. It
compares relative paths, entry kinds, permission modes, symlink targets and
regular-file bytes, while retaining the existing success and no-staging
assertions. The snapshot catches extra files outside the staging directory.
The test change is committed at `42c6e3aa`.

On a separate clean checkout of `42c6e3aa`, canonical Python 3.13.13 ran the
strengthened node: 1 passed in 0.98 s. The bounded P3 replay used
`scripts/replay_upgrade_promise_mutants.py --old
/private/tmp/cairn-mutant-old-ce55 --new
/private/tmp/cairn-mutant-new-42c6 --output
/private/tmp/cairn-p3-replay-42c6 --only P3-plan-write`. Both old/new healthy
baselines passed. The old mutant survived and wrote
`cairn-plan-mutant-write` with `changed`; the repaired new mutant was caught
when the tree snapshot found that entry. The helper restored both engine
copies and both checkouts are clean. No other sealed mutants were rerun.

Coordinator baselines, reported with their sources: the clean old-file run at
`28f79683`, with source SHA-256
`cfc7f1db0d0d74de504e9df187048adc1370765947ad30c2dd0531643cf79c2b`, passed
159 items with zero skips or failures and 93.204 s summed case time. The
one clean new-file run at `ce55e4f4`, source SHA-256
`73a78564ec8f02b19ad0b44520aad96e64dad33b801a44f0eb2d8f21173117ab`, passed
154 items with zero skips or failures; summed case time was 91.417 s and file
wall time 92.423 s. That full-file run predates the snapshot strengthening;
the final strengthened node has the separate focused result above. These
different-source timing totals do not establish a material speed change.

The public no-side-effects gap in the thirteen sealed probes is closed: twelve
were caught by both old and new tests, and P3 is caught by the repaired new
test (the old test still misses it). No other C1 behavioral gap was observed
in that sealed set. This does not claim an exhaustive defensive-site sweep or
discharge final code review, Boundary B, release baseline or re-anchor holds.
Tokens: unknown. Elapsed time: approximately 10 minutes.

## C2 initial inventory -- GPT-6.1 Terra (Implementation) -- 2026-11-08

**Basis and limits.** Inspected portions of the named family bodies, the accepted source and
`bootstrap/tests/security_manifest.py` at `f8adca2d`; this is a triage, not a
completed defensive-site enumeration or removal review. The source measured 98
private-module calls in gate preflight at `176d2caf`; it reported 97 retired-file
functions and 21 seconds there. Those are historical measurements, not current
collection or a clean runtime benchmark. Current per-family runtimes and exact
private-reach counts are unknown; the mapped repin timing included failures and
environment overhead and is not a clean benchmark. No test ran in this inventory.

**First family: `bootstrap/tests/test_gate_preflight.py`.** It is the largest
measured private-reach family in the source and an independently testable gate
component. Its ceremony fixtures are costly and some require native execution;
compare the actual clean old/new family time before claiming a saving. The
following is proposed docstring wording, to be refined against the remaining
bodies and source before Low edits the test file:

Promises:
- Evidence and preflight commands report their result and refuse malformed,
  untrusted or inconsistent inputs without treating them as authority.
- A reviewed anchor, roster, candidate, manifest, launcher and package remain
  bound to the exact authorized objects and bytes across both ceremony stages.
- Signing requires the confirmed package and the authorized key; a refusal or
  stale state does not move either protected ref, and successful publication
  advances the intended refs atomically.
- The stage that runs candidate code is separated from signing, uses the stated
  environment and reports the limits of its isolation.
- Git and filesystem reads resist redirected configuration, substitution and
  hostile paths, and release reports expose the relevant findings and limits.

Retain public CLI evidence/check and old-command refusal in `TestPublicPathCli`,
the full subprocess ceremony in `TestThreeCommandIntegration`, external package
confirmation and hostile package tests in `TestAuthorizationPackage`, the
launcher binding cases in `TestLoaderTrustBoundary`, and transaction and
publication checks. Private-call checks that inject changed paths, races, hostile
Git settings, malformed packages or signing state remain justified unless a
specific public witness and defensive-site probe establish equivalent coverage.
`TestPublicPathCli::test_the_single_stage_apply_and_its_boolean_are_gone_from_the_cli`
rejects the former single-stage command; the package and launcher tests check
external confirmation and binding. These are related evidence, not yet proof
that every self-authorizing bundle route is unreachable.

**Exact proposed removal set, not authorized:**
`TestApplyTakesNoArtifact::test_the_bundle_parser_is_gone`. It asserts only that
`P` has no attribute named `parse_bundle`; an unused function with that name
would fail it even if no public command accepts a self-authorizing bundle.
Before any removal, the independent High reviewer must decide whether the
existing public old-command refusal plus the package/launcher tests actually
protect the authority promise. If they do not, retain the node while Low adds a
public stage-2 test using a tampered, internally self-consistent artifact and an
independent confirmation for different reviewed bytes; assert refusal before
signing and unchanged refs. The test must reach that authority decision rather
than fail on an unrelated missing prerequisite. A fresh independent agent must
then compare the old and new files on behavior mutants and accepting mutants for
all defensive sites it finds in the gate code; a missed old-caught mutant or
missing retained witness stops removal. The package test above is an in-process
check, so it alone cannot close this public-route gap. This candidate is not a
native-only manifest ID; verify the committed manifest again before changing it.
There is no reviewer agreement, before/after count, mutant result or claimed
runtime improvement yet. If High does not agree, retain it and inventory the next
candidate; no deletion quota applies.

**Remaining named families and scope.** These dispositions are starting points,
not approvals or a claim that unlisted nodes are safe to remove:

| Family | Body evidence and next disposition |
|---|---|
| `test_reanchor.py` | Public launcher and report tests exercise stage input, signing and roster continuity; packet swaps, environment poisoning and refusal-before-execution cases protect trust boundaries. Retain those, and examine source-text/registry assertions separately for internal pins versus operator-visible contract; text-only prose checks go to functional-prose work. |
| `test_repin_ceremony.py` | Terminal-driven scratch ceremony covers confirmations, signatures, changed artifacts and key/agent isolation. Keep the hostile inputs and output needed for an informed operator; inspect exact source or prose assertions individually. Its elapsed time needs a clean baseline, not the failure-inclusive mapped figure. |
| `test_upgrade_removes_retired_files.py` | Real upgrade cases cover plan, removal, preservation, records and reruns; helper tests inject Git failures, path replacement and directory races. Keep the row-integrity oracle and its planted-defect check, and keep these defensive cases until an independent site sweep and public equivalent justify any exact removal. The once-per-process version test pins an internal cache but is a POSIX native-only ID and source documents that cache; do not remove it without its own High agreement and native old/new evidence. |
| `security/test_code_map.py`, `security/test_git_interpreter_binding_portable.py` | Public commands/install paths and hostile links, resource limits and reparse points are real promises. Four Windows code-map and eight Windows binding IDs require actual native old/new public-route evidence under Verification; POSIX native IDs also require exact individual agreement before removal. |
| `security/test_git_read.py`, `security/test_check_release_publication.py` | Verified-byte, process and path controls and public release/refusal cases guard security properties even outside the manifest family. Distinguish input-boundary tests from helper shape assertions; preserve fail-closed and hostile-state probes. |
| Gate/security families: `test_gate_reanchor.py`, `test_ast_attest.py`, `test_security_check.py`, `test_portable_security_sweeps.py`, `test_security_marker.py` | Anchor, attestation, release gate, host executable and security-family selection protect the gate or its trust roots. Check real entry points and injection witnesses before proposing specific internal pins; `test_security_marker.py` guards the manifest although it is not itself in `SECURITY_FAMILY`. |
| Manifest security families: `test_api_access_security.py`, `test_default_security_stance.py`, `test_security_capability_install.py`, `test_security_finding_confidentiality.py`, `test_security_leaf.py`, `test_security_lint.py`, `test_security_net.py`, `test_security_stack.py`, `test_security_verification.py`, `test_skills_security.py`, `test_web_hosting_security.py` | Inspect installed behavior, credential and disclosure boundaries, module composition, lint and path controls individually. Source-text-only cases belong to the functional-prose work when they are prose pins; do not classify behavior or installation checks as prose merely because they read files. |

The manifest is a floor, not the whole protected universe: inspect every other
eligible file guarding a security property or named high-risk surface, and the
remaining ordinary eligible families in source order by measured private reach
and credible runtime. List each family and exact candidates in subsequent plan
records; this initial triage does not close that inventory. Meter and claims
families remain fenced on their own Decisions; text-pin retirement belongs to
the functional-prose plan. Every family needs its own promises, baseline,
retained checks and independent old/new comparison; security families also need
the independent defensive-site accepting mutants and prior High removal-set
review. Native IDs need individual agreement and actual platform evidence.

**Elapsed:** approximately 12 minutes. **Tokens:** unknown. No removal, suite,
native run, security review, re-anchor, board edit or push was performed.

## C2 family dispositions and first conversion -- GPT-6.1 Terra (Implementation) -- 2026-11-08

This extends, and changes the first-family ordering in, the initial triage.
`test_gate_preflight.py` has the largest historical private-call count, but its
candidate needs an unresolved authority-boundary decision and its clean runtime
is unknown. `test_default_security_stance.py` is the simpler independent first
conversion: its existing public `expand_preset` reaches the selection helper,
and its install, summary and upgrade cases already cover the surrounding
caller-visible contract. This is a proposed conversion, not an approval or a
completed C2 family.

### Low-ready first family: default security stance

Proposed module docstring lines:

Promises:
- Shipped presets and the no-preset default select content security; an exact
  module list, empty list or explicit removal is respected.
- A filled Python package token selects Python security where permitted; an
  absent, blank or placeholder token does not, and explicit removal wins.
- The summary reports the selected roster and token additions consistently
  with installation; an existing adopter must opt in to a newly available module.

Keep `test_content_security_is_in_every_shipped_preset_roster`,
`test_content_security_reaches_the_no_key_default_shape`, both exact/empty-list
install tests, both filled/absent token install tests, the removal and opt-out
checks, `test_the_profile_summary_names_the_token_gated_addition`,
`test_a_declared_token_never_conscripts_a_module_into_an_exact_list`,
`test_a_new_default_on_module_stays_opt_in_for_an_existing_adopter`, and
`test_the_summary_and_the_install_agree_on_the_roster_for_a_no_preset_profile`.
These cover selection, actual installed files, reporting and existing-adopter
behavior; keep all parameters and refusal/opt-out cases. The public function
`expand_preset` is exported by `bootstrap.scaffold`; its implementation calls
`token_gated_modules` before applying explicit overrides.

**Exact proposed removal:** the two collected nodes of
`test_an_unfilled_python_package_token_does_not_select`: parameter IDs
`[{{python_package}}]` and `[   ]` (three spaces). They directly call the
selection helper with the two relevant values. Replace them with one public
`expand_preset` test parametrized over the same two strings, each with
`{"preset": "solo-greenfield", "python_package": value}`; assert
`python-security` is absent from the returned roster. In the same test or an
existing positive case, assert the roster contains `python-security` for
`mypkg`, so a mutation disabling token selection cannot make every case green.
Remove the now-unused helper import. The new node checks the same missing-token
behavior through the public roster, while existing installation tests check real
selection. Confirm the source/manifest and collect actual IDs before editing;
these two IDs were absent from `NATIVE_ONLY_NODE_IDS` at `c0211f74`. No native
ID removal is proposed. Parameter text must remain unchanged; do not substitute
a profile file parser that could reject a value before selection is reached.

Before deleting the old nodes, prepare the replacement without removing them,
run the scoped affected checks on committed copies and ask fresh High for
node-by-node family removal-set agreement. The independent agent then derives
mutants without reading the test mapping: at least one behavior mutant per
promise, accepting mutants for the refusal/opt-out promises, and one accepting
mutant for each defensive site found in the relevant code. Compare the old and
new committed test files (using a disposable candidate commit before removal
lands) against each mutant on isolated copies, after healthy
baselines; retain a reproducible probe and report reach, results and omissions.
If a caller-visible old-caught mutant is missed, or a required witness or site
probe is absent, the node stays and the family is unfinished. Record old/new
collection and a clean runtime, not the historical or failure-inclusive timing.
The protected removal is a release re-anchor hold. No test body or manifest is
changed by this inventory.

Canonical Python 3.13.13 collection at `c0211f74` listed 16 items in 0.03 s,
including those two exact IDs; this was collection in the feature worktree,
not a family execution or a clean runtime baseline. A direct public-function
probe returned absent, absent and present for placeholder, whitespace and
`mypkg`, respectively; this is a smoke observation, not mutation evidence.
`security_manifest.py`
marks the file as protecting the adopter default posture. The mutation and
High-review gates apply even if the change merely replaces two parameter cases.

### Additional protected candidates for one batched High handoff

- **Gate preflight:** the earlier exact candidate
  `TestApplyTakesNoArtifact::test_the_bundle_parser_is_gone` is a name-absence
  assertion. The old single-stage CLI refusal, confirmed package and launcher
  binding are related witnesses; equivalence to refusal of self-authorizing
  artifacts is not established. High must decide whether a public stage-2
  tampering witness is required and whether it proves the same authority
  boundary. Keep the candidate until that question and the independent
  defensive-site sweep are resolved.
- **Security leaf:** exact candidate
  `test_scaffold_security_error_defined_exactly_once_in_the_leaf` counts class
  definitions by source location; an unused extra definition would fail it
  without necessarily changing a caller's exception. Retain
  `test_single_scaffold_security_error_identity_across_consumers` and the
  guard-routing, symlink, hardlink, swap, mode and cleanup cases. Strengthen
  public evidence first: call exported `bootstrap.scaffold.seed_gitignore` on a
  target whose `.gitignore` links to an outside file, catch exported
  `bootstrap.scaffold.ScaffoldSecurityError`, and assert outside bytes remain
  unchanged. `test_intents_tool.py::TestGitignoreSeedingRefusesLinks::test_seed_refuses_a_linked_gitignore`
  already exercises the same public operation for inside/outside links and
  write/dry-run, but imports its error from the leaf; the new witness binds the
  exported exception specifically. High must assess whether removing the
  definition-count pin concedes any independent security guarantee, and the
  independent agent must probe all defensive sites. This candidate is absent
  from the native-only manifest; the three native-only leaf cases stay.

High may review both families in one pass but must give a separate verdict for
each named node and family. No set above has High agreement or a mutant result.
If a retained test is not an equivalent witness, the affected node stays.

### Remaining named-family disposition map

An empty candidate set below means no deletion is proposed by this inventory;
it does not prove the entire file has no possible future candidate. These are
specific starting witnesses and reasons, not blanket protection for private
calls. Text-only prose pins are assigned to functional-prose work, while actual
CLI output, install and safety contracts remain here.

| Family | Exact starting witnesses and disposition |
|---|---|
| `test_reanchor.py` | Keep `TestEveryPublicCommandIsExercised::test_the_dispatch_knows_exactly_these_commands`: it is source-shaped but flags a new public command absent from the expected list; `TestTheStepRegistry` cases preserve publicly reported order and candidate-code boundary. Keep packet rewrite, environment and signer refusals. No removal proposed until a public command-inventory witness and accepting mutants are shown. |
| `test_repin_ceremony.py` | Keep `test_a_full_ceremony_signs_once_with_the_typed_passphrase`, `test_a_package_rewritten_between_the_report_and_the_yes_refuses`, and `test_a_key_loaded_after_stage_one_refuses_before_stage_two`; they distinguish success, changed authorization and signing isolation. `test_the_page_is_at_most_eighty_lines_above_its_marker` and other runbook prose pins go to functional-prose. No ceremony-body removal proposed. |
| `test_upgrade_removes_retired_files.py` | Keep `test_no_retired_row_is_still_shipped_and_every_row_has_digests` with planted-oracle control `test_the_row_check_flags_a_shipped_row_and_a_renamed_template`; keep `test_plan_names_exactly_the_files_the_step_removes`, `test_a_folder_swapped_for_a_link_after_the_decision_leaves_the_outside_copy`, and `test_a_stop_before_the_lockfile_write_heals_on_rerun`. They protect list integrity, user-visible deletion, hostile timing and recovery. `test_git_version_is_read_once_per_process` is an internal cache pin but a POSIX native-only ID and source-documented behavior: no removal without individual High agreement and native old/new evidence. No other removal proposed. |
| `test_gate_reanchor.py` | Keep `test_candidate_mutation_during_stage_a_cannot_affect_stage_b`, `test_wrong_evidence_hash_refuses`, `test_rostered_stage_b_executes_only_preflight_bytes_pinned_by_p`, and `test_static_verify_failure_refuses_before_cas`: independent authority, binding and atomic movement controls. No proposed removal. |
| `test_ast_attest.py` | Keep `test_digest_detects_a_logic_change`, `test_pure_motion_across_modules_verifies`, `test_duplicate_symbol_fails`, `test_update_symbol_refuses_on_expect_old_mismatch` and `test_update_symbol_cli_path`: both healthy and rejecting attestation/update routes. No proposed removal. |
| `test_security_check.py` | Keep `test_release_mode_refuses_collection_time_skips`, `test_fixed_policy_skips_only_exact_opposite_platform_ids`, `test_liveness_never_derives_from_a_partially_scanned_report`, and `test_a_candidate_severity_downgrade_cannot_hide_corruption`. They protect release evidence, platform policy and scanner failures. No proposed removal. |
| `test_portable_security_sweeps.py` | Keep `test_policy_refusal_precedes_every_side_effect`, `test_path_drift_between_validation_and_invocation_is_degraded`, `test_a_hostile_path_string_cannot_forge_a_report_line`, and `test_the_runner_twin_is_byte_identical_to_its_template_source`; these cover refusal, executable revalidation, output safety and required shipped twin fidelity. No proposed removal. |
| `test_security_marker.py` | Keep `test_unmarking_a_member_is_detected`, `test_not_security_collects_no_member` and `test_the_release_entry_point_is_not_deselected`; source roster and selection checks prevent silently moving required security coverage. No proposed removal. |
| `test_api_access_security.py` | Keep `test_b2_a_fixture_that_authorizes_everything_is_not_clean`, `test_b3_local_never_reads_or_emits_a_deployed_credential`, and `test_b5_deployed_refuses_every_near_miss_before_any_request`: actual false-clean, credential and authorization boundaries. No proposed removal. |
| `test_security_capability_install.py` | Keep `test_modules_remove_wins_over_modules_add`, `test_hazard_a_renamed_engine_source_degrades_the_facade_at_runtime`, and `test_hazard_a_tampered_engine_member_fails_the_fresh_install`: selection, actual installed routing and integrity. No proposed removal. |
| `test_security_finding_confidentiality.py` | Keep `test_d1_no_planted_marker_reaches_any_sink`, its deletion-mutant control, `test_d6_control_sequences_and_a_forged_result_line_do_not_reach_stdout`, and `test_d7_absent_randomness_is_degraded_before_the_first_request`. These are observable disclosure and failure boundaries. No proposed removal. |
| `test_security_lint.py` | Keep `test_every_templates_py_on_disk_is_release_scanned`, `test_the_on_disk_oracle_goes_red_when_a_registry_stops_delivering`, and `test_a_templates_py_no_registry_delivers_is_reported_unscanned`; they prevent a scanner registry from defining away missing files. No proposed removal. |
| `test_security_net.py` | Keep `test_a1_public_at_validation_loopback_at_connect_is_refused`, `test_a4_the_engine_carries_nothing_to_a_redirect_target`, `test_a6_body_one_byte_over_the_cap_refuses`, and `test_a7_hostname_mismatch_refuses`; different live transport and refusal sites are not duplicates just because they share a helper. No proposed removal. |
| `test_security_stack.py` | Keep `test_b_t3_pip_audit_argv_is_fixed_and_environment_free`, `test_d_t2_one_unknown_gates_clean`, `test_a_failed_closure_drops_no_distribution`, and `test_physical_source_module_refuses_its_mismatched_pin`: execution boundary, fail-closed reporting and verified loader. No proposed removal. |
| `test_security_verification.py` | Keep `test_content_apparatus_member_failure_refuses_before_launch`, `test_child_env_is_minimal_and_strips_proxies_and_credentials`, `test_forged_terminal_controls_never_reach_the_terminal`, and `test_api_engine_member_tampering_refuses_before_child_or_credentials`; subprocess, disclosure and integrity boundaries. No proposed removal. |
| `test_skills_security.py` | Keep `test_session_start_opens_no_socket`, `test_hostile_artifact_name_cannot_forge_orientation_lines`, `test_crafted_agent_cannot_escape_reflections`, and `test_installed_artifacts_match_lockfile_hash`; no-egress, output, path containment and install integrity remain distinct. No proposed removal. |
| `test_web_hosting_security.py` | Keep `test_c1_deletion_mutant_removing_a_check_makes_its_row_go_green`, `test_c2_a_host_change_before_the_https_upgrade_is_a_finding`, and `test_deployed_refuses_every_near_miss`; positive/negative scan and target authorization cases. No proposed removal. |
| `security/test_git_read.py` | Keep `test_verified_module_executes_the_exact_pinned_buffer_without_cache_reuse`, `test_executable_digest_refuses_replacement_during_read`, and `test_timeout_kills_the_owned_process_group_and_returns_incomplete`: loader, race and bounded-process defenses. No proposed removal. |
| `security/test_git_interpreter_binding_portable.py` | Keep `test_linked_worktrees_get_distinct_bindings`, `test_binding_path_link_and_wrong_type_refuse`, and `test_windows_reparse_points_refuse_binding_access`. The eight parameterized Windows native-only IDs stay; actual Windows evidence is required for any later proposal affecting them. No proposed removal. |
| `security/test_code_map.py` | Keep `test_real_cli_does_not_execute_inspected_python_and_escapes_controls`, `test_race_substituting_a_file_for_a_link_is_refused`, and `test_windows_native_cli_refuses_reparse_entries_and_held_reparse_parent`. The four Windows and POSIX native-only IDs stay; native evidence and individual agreement remain required. No proposed removal. |
| `security/test_check_release_publication.py` | Keep `test_public_command_refuses_unpublished_or_wrong_release`, `test_public_command_refuses_mismatched_or_ambiguous_remote_refs`, and `test_public_command_ignores_hostile_git_configuration_and_proxy`: public release identity and hostile environment. No proposed removal. |

This maps every explicitly named C2 family, every `SECURITY_FAMILY` member and
the four `bootstrap/tests/security/` files, plus the security-marker guard.
It does not purport to enumerate or clear all other ordinary or security-relevant
files in `bootstrap/tests`; C2 still requires their component-by-component
inventory, using the accepted ordering and the same promise and mutant gates.
The eligible remainder is the tracked test tree less the pilot, the families
named above, the functional-prose text-pin work, and the separately fenced
meter and claims-tool families. Check actual file ownership and mixed-purpose
files before assigning individual nodes to a fence. The High review, independent
defensive-site enumeration and old/new comparisons remain work for every
protected family with a proposed removal; no later release run can replace them.

**Elapsed:** approximately 12 minutes. **Tokens:** unknown. Apart from the
collection described above, no tests, mutation replay, suite, removal, native
run, trust operation, board edit or push occurred.

## Implementation constraint -- GPT-6.1 Terra (Implementation support) -- 2026-11-08

The Maintainer directed: "Also, with today's testing plan, we absolutely must achieve a reduction in test volume". Measure a net reduction across the companion promise-testing and functional-prose work, including added tooling, loader and mutation-support tests. Report test definitions and collected parameter-expanded cases before and after, with support-code footprint for context. Preserve promised public behavior, refusals and hostile-state coverage; do not hide or rename discovery or merely pack assertions to manufacture a reduction.

Elapsed: under one minute; tokens: unknown.

## C2 broader family inventory and execution batches -- GPT-6.1 Terra Medium (Implementation) -- 2026-11-08

At `7cfb8625`, `git ls-tree -r --name-only 7cfb8625 bootstrap/tests` filtered to `test_*.py` yields 138 tracked test files. The advisory output `/private/tmp/cairn-promise-c2-coupling-7cfb8625.json` lists Python files by private reach, not removability; it includes six paths outside `bootstrap/tests`, and its current 82/77/38 for edit-check/module-additions/integrity are counts, not measured runtime or security rankings. The prior `99aa19d5` record covers the pilot and named/manifest families; the following adds concrete families and candidates. The test tree also contains mixed prose, behavior, and fenced material: classify individual nodes, not whole files, by ownership. No deletion is approved by this inventory.

| Family and public promise | Retained witnesses and candidate |
|---|---|
| `test_upgrade_module_additions.py` (77): stage/apply recognizes newly shipped module files, records canonical origins and preserves local data. | Keep `test_pre_split_apply_records_package_in_lockfile`, collision, changed-input, link and hardlink cases. Candidate `test_pre_split_compute_surfaces_package_as_new_module` checks private plan objects; the public stage/apply witness checks each destination, source and verbatim record. Before removal independently mutate discovery, source mapping and verbatim recording and compare old/new; missing plan-visible behavior needs an additional public witness. |
| `test_verify_integrity.py` (38): integrity returns failure on tampering and gives the finalize hint only for a customized slot. | Keep `test_tampered_file_fails_closed`, `test_a_filled_customized_slot_is_pointed_at_finalize`, and every refusal, resource bound, race and output-safety witness. Candidates `TestCustomizedSlotDetection::test_a_marker_inside_a_slot_counts` and `::test_a_marker_outside_every_slot_does_not`: the public `verify` witness checks both marker placements and finalization. Independently mutate inside/outside detection and compare old/new; other marker-shape and linear-time tests are not included. |
| `test_scaffold.py` (12): public token detection leaves document-author placeholders without unfilled warnings and identifies a real missing token. | Keep `TestFindUnfilledTokens::test_excludes_doc_author_placeholders`, which exercises all four names and a real missing token via exported `find_unfilled_tokens`. Candidate `::test_doc_author_tokens_constant` pins the private set. Check whether its template consistency claim adds a separate contract; independently mutate each of the four memberships and compare before proposing removal. Preserve install, slots and placeholder checks. |
| `test_upgrade_edit_check_runs_no_project_programs.py` (82): Git edit classification must not execute project-configured programs and must fail closed when it cannot determine state. | Keep the public stage/apply/finalize no-program test, every injected Git failure, link/FIFO case and Git-status parity case. Candidate for investigation only: `test_an_unchanged_file_does_not_differ_and_one_changed_byte_does`; the public parity test may cover its unchanged/changed/missing/folder distinctions, but inspect each branch and prove it with mutants before a removal set. Do not infer equivalence from the shared helper. |
| `test_upgrade_lockfile_path_containment.py` (23), `test_upgrade_refuses_hostile_project_data.py` (17): prevent source/destination, metadata and link escapes and hostile output across all upgrade actions. | Keep `test_a_dst_that_leaves_the_project_is_refused_on_every_action`, `test_apply_refuses_a_staged_upgrade_that_holds_a_link`, `test_apply_never_creates_a_profile_through_a_link` and the swapped-lockfile test. Direct guard tests and static guard-order assertions are candidates for inspection, not removals; enumerate all defensive sites and actual public action coverage first. |
| `test_upgrade_side_door_parity.py` (13), `test_skills_upgrade.py` (12): collision adoption preserves the authorized bytes and skill upgrades preserve merges and reject linked targets. | Keep fork-survival, keep-mine, upstream-restage, linked-gitignore and stage/apply/fanout cases. Inspect private compute classifications for publicly reported equivalents; no exact removal yet. |
| `test_profile_grammar.py` (8), `test_presets.py` (6): profile parsing refuses malformed/unknown input before writes; presets select, override, summarize and install the intended roster. | Keep parser-oracle disagreement controls, Unicode/line-ending/refusal cases, real-install refusal, exact-list install and summary CLI witnesses. Direct parser/public expansion cases may test a public API; inspect before proposing removal. |
| `test_engine_copy_fallback_contained.py`, `test_lockfile_module.py`, `test_finalize_retired_living_state.py`, `test_module_merge_lockfile.py`, `test_upgrade_module.py`: copy containment, lock provenance, finalize and module merge behavior. | Inventory entry points, baseline counts and hostile-state witnesses per file before selecting candidates; private reach 5–6 alone proves nothing. |
| `test_config_module.py`, `test_drift_surfacing.py`, `test_install_module.py`, `test_intents_tool.py`, `test_lockfile_provenance.py`, `test_onboarding_slot_substitution.py`, `test_profiles_smoke.py`, `test_scaffold_substrate.py`: config, installation, change/coordination, lock provenance and onboarding outcomes. | Read the real command/install consumers and distinguish schema, output and contained-write behavior from private-shape assertions; preserve hostile injections and per-file promise lists. Private reach is 4 each. |

**Low execution batches.** First prepare the existing default-security two-case replacement exactly as specified above, without deleting it. Next prepare the three exact candidates in the first three table rows in separate disposable candidate commits; leave all old nodes present until review. For each family record committed before/after collection and clean runtime under Python 3.13.13, promise list, exact retained nodes and exact proposed removals. Run only mapped checks; the independent agent derives behavior mutants without reading the mapping, and compares old/new once per mutant after healthy controls. A protected family additionally needs its complete independent defensive-site accepting-mutant sweep. A missed old-caught behavior, missing witness or failed check stops that family. Candidates are not permission to drop a test merely for using a private function.

**One grouped High handoff.** Present separate decisions for default-security's two parameter cases, module-additions' compute node, integrity's two marker nodes, scaffold's constant node, and the earlier gate-preflight and security-leaf holds, with the committed candidate, public witnesses, complete site sweep and old/new evidence per family. Gate helper absence remains held until the authority-boundary question is answered; leaf definition count remains held until exported exception identity and outside-byte safety are demonstrated. High must name each approved protected node and each affected manifest reason; native-only IDs require individual agreement and actual platform evidence. If evidence is missing, retain the affected node. Preserve hostile-state, refusal, timing and source/output parity protections.

**Remaining inventory, not completion:** the tracked set also includes zero-reach files and the remaining 1–2-reach rows in the report. They include installation/skills and onboarding, session and intent operations, manifest/gate/oracle/loader, quality and documentation tools, integration and unit contracts. Zero private reach does not remove them from C2; read their public promises and witnesses individually, distinguishing protected trust surfaces and new C3 tooling. Functional-prose owns its text pins; meter and claims tools remain behind their separate Decisions. The actual eligible set therefore remains to be resolved node by node, including mixed files and out-of-tree test owners; no complete family census, clean runtime or net reduction is claimed. Measure the combined before/after definitions and collected cases including six C3 coupling-tool definitions and all support tests. No test, mutation, suite, review, native run or removal was performed for this record.

**Elapsed:** approximately 12 minutes. **Tokens:** unknown.
