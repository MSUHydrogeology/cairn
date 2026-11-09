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

## C2 complete file census and next batches -- GPT-6.1 Terra Medium (Implementation) -- 2026-11-08

At `7cfb8625`, the file census is **138 classified, zero unclassified at file level**: 3 fenced, 13 mixed prose/behavior, 63 security or protected-surface screening, and 59 other behavior files (24 tools, 15 install/onboarding, 7 session, 11 upgrade/profile and 2 additional security). These are routing categories, not decisions to delete or retain every node. In particular, the 63 are not a blanket KEEP: their exact candidate removals require the C2 security gates. A mixed file may contain separately owned pins and live install/behavior checks. The exact tracked membership is below, relative to `bootstrap/tests/`; no new test ledger is required.

**Meter/claims fence (3):** `integration/test_claim_check_allow_config.py`, `integration/test_meter.py`, `test_claim_check_module.py`.

**Mixed prose and behavior (13):** `contract/test_certifying_run_rule.py`, `contract/test_comprehension_floor.py`, `contract/test_model_tier_rule_ships.py`, `contract/test_review_and_verification_rules_ship.py`, `contract/test_scientific_check_guidance_ships.py`, `contract/test_stewardship_rules_ship.py`, `contract/test_verification_boundaries.py`, `contract/test_writing_rules_ship.py`, `test_doc_governance.py`, `test_review_stance_in_shipped_files.py`, `test_review_sweep_ships.py`, `test_scope_reduction_trap.py`, `test_session_start_drain_rules.py`.

**Security or protected-surface screening (63):** `contract/test_release_members_contract.py`, `contract/test_test_tiers.py`, `security/test_check_release_publication.py`, `security/test_code_map.py`, `security/test_git_interpreter_binding_portable.py`, `security/test_git_read.py`, `test_api_access_security.py`, `test_ast_attest.py`, `test_broad_run_guard.py`, `test_ceremony_review_report.py`, `test_check_cairn_content.py`, `test_config_module.py`, `test_content_scan.py`, `test_default_security_stance.py`, `test_engine_copy_fallback_contained.py`, `test_facade_loader_cleanup.py`, `test_gate_manifest.py`, `test_gate_preflight.py`, `test_gate_reanchor.py`, `test_gate_transition.py`, `test_hardening.py`, `test_install_module.py`, `test_loader_identity.py`, `test_lockfile_module.py`, `test_manifest.py`, `test_oracle.py`, `test_oracle_activation.py`, `test_oracle_trust.py`, `test_portable_security_sweeps.py`, `test_python_floor.py`, `test_reanchor.py`, `test_reanchor_driver_disclosures.py`, `test_repin.py`, `test_repin_ceremony.py`, `test_scaffold.py`, `test_scaffold_substrate.py`, `test_security_capability_install.py`, `test_security_check.py`, `test_security_finding_confidentiality.py`, `test_security_leaf.py`, `test_security_lint.py`, `test_security_marker.py`, `test_security_net.py`, `test_security_stack.py`, `test_security_verification.py`, `test_session_binding_gate_and_printing_hold.py`, `test_session_binding_untracked.py`, `test_session_failsafe.py`, `test_session_kernel.py`, `test_session_writes_contained.py`, `test_skills_security.py`, `test_slotmerge_leaf.py`, `test_upgrade.py`, `test_upgrade_edit_check_runs_no_project_programs.py`, `test_upgrade_lockfile_path_containment.py`, `test_upgrade_module.py`, `test_upgrade_module_additions.py`, `test_upgrade_refuses_hostile_project_data.py`, `test_upgrade_removes_retired_files.py`, `test_verify_integrity.py`, `test_verify_ref.py`, `unit/test_cli_module.py`, `unit/test_merge_module.py`.

**Tools, advisory and documentation behavior (24):** `contract/test_cairn_prefix_links.py`, `integration/test_check_cairn_counts.py`, `integration/test_deleted_tracked_markdown.py`, `integration/test_evolution_infer.py`, `integration/test_gauge.py`, `integration/test_link_check_exclusions.py`, `integration/test_prune_tools.py`, `integration/test_quality_gate_redundancy.py`, `integration/test_verify_stems.py`, `test_doc_drift_tools.py`, `test_documentation_plan_module.py`, `test_fork_advisory.py`, `test_issue_capture_bootstrap.py`, `test_loop_fidelity_gate.py`, `test_module_roster.py`, `test_next_session_local_note.py`, `test_practice_modules.py`, `test_quality_gate_cli.py`, `test_quality_gate_neutrality.py`, `test_quality_gate_order_independence.py`, `test_reference_scripts.py`, `test_replacement_tools.py`, `test_test_coupling.py`, `test_verify_counts.py`.

**Install, output and onboarding (15):** `test_agreement_retired.py`, `test_coordination_broad_intent.py`, `test_core_dev_folders.py`, `test_first_session_report.py`, `test_incident_trackers_module.py`, `test_install_report_slots.py`, `test_install_time_onboarding.py`, `test_model_selection_stub.py`, `test_notice_install.py`, `test_onboarding_seed_roster.py`, `test_onboarding_slot_substitution.py`, `test_quickstart_sequence.py`, `test_skills_install.py`, `test_skills_matrix.py`, `test_skills_onboarding.py`.

**Board, session and skill behavior (7):** `test_board_json_contract.py`, `test_intents_tool.py`, `test_session_routines.py`, `test_skill_contract.py`, `test_skills_fanout.py`, `test_skills_self_heal.py`, `test_status_vocabulary_advisory.py`.

**Upgrade, merge and profile behavior (11):** `test_drift_surfacing.py`, `test_finalize_retired_living_state.py`, `test_lockfile_provenance.py`, `test_module_merge.py`, `test_module_merge_lockfile.py`, `test_presets.py`, `test_profile_grammar.py`, `test_profiles_smoke.py`, `test_skills_upgrade.py`, `test_upgrade_added_slots.py`, `test_upgrade_side_door_parity.py`.

**Additional security behavior (2):** `test_generated_output_scan.py`, `test_web_hosting_security.py`.

**Witness and ownership map.** The first fence holds meter/claims behavior for their own Decisions; the gauge file is mixed because it also tests JUnit pulse behavior (`test_testsuites_and_testsuite_counts_keep_phase_and_session_time_distinct`) and its meter assertions remain fenced. The prose group routes literal wording to functional prose, while retaining installed outputs, real scaffold and parity checks; the drain pin remains the Maintainer's explicit keep. For the protected group, the earlier tables name each security family and the four new exact candidates; additional protected surfaces include interpreter binding (`test_a_binding_written_on_this_machine_is_still_used`), install containment (`test_a_linked_folder_above_the_link_to_make_is_refused_before_the_link_is_made`), release selection (`test_actual_security_omission_fails_after_pytest_passes`), and loader identity (`test_load_engine_is_idempotent_one_object_per_file`). Public witnesses do not by themselves clear other assertions or defensive sites.

The other behavior groups have concrete public witnesses: installed incident analysis `TestRegistration::test_tool_installed_verbatim` and `TestGateEval::test_main_suggests_and_json`; core folder creation `TestScaffoldCompleteness::test_upstream_dir_and_files_created`; install omission `TestInstallPath::test_omission_path` in incident trackers; upgrade no-clobber `TestUpgradeNoClobber::test_diverged_upstream_readme_not_clobbered`; board status `TestTheBoardFlagsStatusesOutsideTheVocabulary::test_retired_and_unknown_statuses_are_named_and_still_listed`; and generated-output checks `test_minimal_profile_generates_clean` and installed web scanner `test_a_fully_conformant_local_target_is_clean`. These describe representative family promises, not complete coverage of every file. Security, link, hostile-state, native, parity, manifest, real-install and timing assertions within any group retain their individual protection.

**Ordinary Low batch:** in `integration/test_quality_gate_redundancy.py`, prepare a real `scripts/quality_gate.py --root <fixture> --sub redundancy --report` witness for `TestR1Shingles::test_high_overlap_pair_surfaces` using the same two files and asserting an R1 overlap in public output. Keep low-overlap, threshold and shingle-size cases and preserve the semantics of their tunable flags. Record baseline/candidate collection and clean runtimes; use an independent old/new behavior mutant removing overlap detection before proposing retirement. Treat the candidate as protected if the exact target is found to guard a named trust surface; no removal is authorized here. Separately, `integration/test_evolution_infer.py::TestGateEval::test_two_occurred_in_window_suggests` is a candidate for public `main --json` coverage, but the existing main test does not also demonstrate the outside-window and prevented rows; add those to the public fixture and compare corresponding mutants first. Keep fail-closed and no-write cases. Count new tests as well as removed cases.

**Grouped High handoff:** include the previously named default-security, module-additions, integrity, scaffold, gate-preflight and security-leaf nodes, plus `test_core_dev_folders.py::TestScaffoldCompleteness::test_all_core_folder_files_in_core_mappings`: its three real install checks cover the listed destinations, subject to an independently derived missing-mapping mutant for each destination and confirmation that the mapping assertion has no further public contract. The install witnesses, link and overwrite checks stay. Submit one grouped review with a separate per-family and per-node verdict, complete independent defensive-site accepting mutants, old/new results, and manifest/native dispositions. The independent reviewer, not private-reach counts, determines if public coverage preserves each fault. Gate/leaf remain held pending the prior specified evidence.

**Limits and next evidence:** file routing is complete; this census does not claim that all individual assertions, defensive sites, runtime baselines or removals have been mapped or approved. Each family still needs its own C2 promise list, exact before/after nodes and counts, independent behavior mutations, and applicable High/native evidence before its conversion lands. Six advisory paths outside this 138-file tree include examples, historical material and tool sources, not additional members of this census; their actual test ownership must be handled when changing those components. No tests, mutation, deletion, security review or suite ran for this inventory. Net combined test volume remains to be measured.

**Elapsed:** approximately 15 minutes. **Tokens:** unknown.

## Independent ordinary C2 comparison -- GPT-6.1 Terra Medium (Reviewer) -- 2026-11-08

At baseline `c6283b46` and candidate `2db4b622`, the implementation sources were identical; the installed and template evolution sources were byte-identical. Before reading either test body, I derived 15 behavior mutants from the candidate module promises and owning sources. The temporary description script's SHA-256 was `62c27fc36c04165b983fba99fc6f3f24a069ac082f0d8ca188269f8983af6879`; its sealed list was `ef2d35aae3c87f4d17b912eae9da8acc10a69d3d56bafebb2f1ba71c5eb48c03`. The evolution probes were applied to the byte-identical template actually loaded by the tests. Using separate copies and `/Users/kendal30/conda_envs/lhm/bin/python3.13`, healthy controls passed for both versions: redundancy 12/12 and evolution 22/22. Both versions caught all 15 mutants with target-test assertions, not setup failures; none was caught by old and missed by candidate.

A post-seal probe omitted R1 from public report aggregation: old survived and candidate caught it, confirming the added public witness reaches that path. A separate callback-specific whitelist removal survived both versions: the existing fixture references its callback, so it does not isolate the exemption. Ordinary cross-file calls and CLI threshold and shingle-size wiring also lack public witnesses. These are unchanged-family coverage gaps, not evidence of a regression in the added witnesses. This comparison covers additions while old nodes remain; it does not approve removals or complete C2, code review or Security Review. The temporary mutation mechanism is not retained in canonical tests or scripts and remains work for implementation. Elapsed time and token use: unknown.

## Targeted ordinary C2 follow-up -- GPT-6.1 Terra Medium (Reviewer) -- 2026-11-08

At `d0a63111`, four new public redundancy witnesses each passed on healthy source and failed on its targeted behavior mutant in separate copies under Python 3.13.13: CLI threshold and shingle-size arguments forced to defaults, omission of the `_cmd_claim` whitelist exemption, and replacement of cross-file reference accumulation. All four failures were the intended assertions. The callback uses `globals()[name]`, with no static callback-name reference; the exemption mutant triggers the new report assertion. These close the three specific witness gaps recorded above, subject to the remaining work below. No earlier mutant matrix was rerun.

The canonical fixture's 15 `(id, source, old, new)` tuples exactly match the sealed temporary descriptions; both description and list SHA-256 values match the preceding record. The replay utility still needs repair before its results can be relied on: `target` and `family` are outside the tuple digest, target paths are not confined to their checkout or checked against links, and text-mode restoration can change line endings. Its `finally` restores after ordinary exceptions but not abrupt termination. It also treats any nonzero mutant exit as caught, including setup failures. These observations do not constitute Security Review or a full plan review. Elapsed time and token use: unknown.

## Implementation verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-08

At `08755689`, the replay child traces only the exact `scripts/quality_gate.py` subprocess launched during an active test call. Its fresh, exclusive evidence file binds nonce, absolute target and source digest; validated CLI line hits join only the owning node. Unmatched commands remain unwrapped. Missing or malformed evidence, `check=True` failures and timeouts make classification inconclusive while preserving the original argv and raised exception. The fixed-target control confirmed direct-script argv, `sys.path[0]`, `__main__`, `__file__`, stdout, stderr and exit 7; another control confirmed that a line reached in a passing node cannot explain a separate failing node.

The previous actual `r1_public_omit` result remains visible: the old checkout survived and the candidate was inconclusive because subprocess target lines were not traced. After this repair, one new run used fresh clean detached copies at old `c6283b46` and candidate `08755689`, under `/Users/kendal30/conda_envs/lhm/bin/python3.13`. Old survived (baseline 6.468 s, mutant 6.494 s); new was caught by its own call assertion after line 701 ran (baseline 9.301 s, mutant 10.196 s). Both collected the same 12 ordinary nodes as their baselines. Both clones were clean afterward; the target bytes matched each checkout's committed source and mode remained 0644. Results and logs: `/private/tmp/c2-replay-results-08755689/`. No 15-probe matrix was rerun.

Changed-file check: `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q bootstrap/tests/test_replay_ordinary_c2_mutants.py --tb=short` passed 33 tests in 22.98 s. An earlier targeted iteration exposed four test-control failures, then one malformed-evidence control failure; each was corrected and the final targeted selection passed 5 tests. No full suite, old matrix, Security Review, independent code review, Boundary B, baseline or re-anchor was run. This repair does not complete C2 or the plan. Elapsed time: approximately 25 minutes; token use: unknown.

## Default-security public witness -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

At candidate `66ab4df7`, the existing module docstring now carries the
accepted three `Promises:` bullets, and a new public `expand_preset` witness
uses the exact placeholder and three-space parameter values. Each case checks
that `python-security` is absent and that a healthy `mypkg` roster still selects
it. The old private-helper cases and import remain untouched pending fresh High
node-by-node agreement and the independent old/new mutation comparison; no
removal is authorized. The two old node IDs are absent from
`security_manifest.NATIVE_ONLY_NODE_IDS` on these bytes.

Separate committed archives under canonical Python 3.13.13 measured the family
before and after: baseline `99a1d591` collected 16 cases and passed 16 in 1.82
s; candidate `66ab4df7` collected 18 cases and passed 18 in 1.84 s. This adds
one test definition and two collected cases before any removal; it does not yet
deliver a net volume reduction. The public witness and healthy case are the
only changed behavior. No mutation comparison, other test family, full suite,
native run, review, or removal was performed. This candidate closes no High
gate and is not a family-removal approval. **Elapsed:** approximately 7
minutes; **tokens:** unknown.

## C2 default-security removal-set Security Review -- GPT-6.1 Sol (High) -- 2026-11-09

**Foundations**

1. **Should this happen as framed?** The two replacements preserve their faults, but the family lacks required coverage of summary exactness and upgrade opt-in restrictions. -- Independent probes and findings below; plan C2.
2. **Best alternative.** Extend the existing summary and upgrade public checks with the missing assertions, retaining the old nodes until the family gate closes. -- `test_the_profile_summary_names_the_token_gated_addition`; `test_a_new_default_on_module_stays_opt_in_for_an_existing_adopter`.
3. **What would show it wrong?** A repaired candidate surviving S1/S2/U1/U2, or any old-caught/new-missed behavior, keeps removal stopped. -- Sealed comparison below.

**Reviewed commit:** `66ab4df731f26223013d8046da18397170a39960`; old `99a1d59118dba77fababed987c45aaadcabefee9`.
**Obligation:** C2 first protected-family removal-set Security Review and independent behavior comparison; not final code review.
**Verdict:** node-local AGREE for both `test_an_unfilled_python_package_token_does_not_select[{{python_package}}]` and `test_an_unfilled_python_package_token_does_not_select[   ]`; family HOLD until findings 1–2 close. No canonical removal occurred.
**Elapsed:** approximately 22 minutes. **Tokens:** unknown.

Before reading test bodies, I sealed 14 source-derived probes: D1 default content; D2/D3 exact install default/token widening; T1/T2/T3 accepting absent/blank/placeholder tokens; T4 disabling filled selection; R1 ignoring removal; S1/S2 exact-summary default/token widening; S3/S4 omitted summary roster/token label; U1/U2 treating unadopted content-security as unconditional/adopted. Defensive sites include all three token conjuncts, install/summary exact-list branches, final removal and both upgrade write-set restrictions. General parser/path guards and selected-module required-token validation are distinct contracts outside this selection family.

Sealed fixture SHA-256: `380d2e78e177736f9430793647332fe7e78db9c48b5345132800a72f7b7ec4b4`. Replay and public witnesses: `/private/tmp/default-security-probes.py`, `/private/tmp/default-security-public-witness.py`; logs/data: `/private/tmp/default-security-comparison-sol-r1/`. Low should retain the finite data in the existing fixture home and reuse a small family replay script, without adding 14 permanent tests.

Separate clean disposable commits `4a8fbac0` (old) and `862d9e41` (candidate minus exactly those two cases/import) each passed 16/16 healthy controls on canonical `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13), 2.469/2.373 s including instrumentation. Sources matched and trees remained clean. Each caught ten mutants by call assertions; S1/S2/U1/U2 survived both; zero old-caught/new-missed. T2/T3 failed the exact old cases and corresponding public replacements. No setup failure counted. Initial instrumentation failed before collection on a plugin argument name; its log remains in `/private/tmp/default-security-comparison-sol/`. Corrected execution took 66.592 s for 28 probes. D1 deletion was demonstrated by missing public roster/files, rather than an executable changed line.

**Finding 1 -- Blocking coverage gap:** Exact summaries are unexercised. Direct public witnesses show S1/S2 falsely adding content-security/python-security while installation remains claim-check. Close by asserting the summary roster is exactly claim-check, with no token-addition label, for an explicit list plus filled token.

**Finding 2 -- Blocking coverage gap:** Upgrade planning survives U1/U2 while wrongly scheduling six unadopted content-security files. Both sites executed. Close by requiring its existing public plan output to omit the content-security module and scanner file paths, then falsify with both mutants.

Record checks: claim, link and snippet checks passed on this plan; neutrality reported fail=0, info=43.

**Coverage:** AST inspection confirmed both exact IDs absent from `NATIVE_ONLY_NODE_IDS`, with a listed native ID as positive control. Covered only this family, owning selection/reporting/upgrade sites and fixed commits; no other family, native execution, suite, private collection, baseline or re-anchor. Over target to retain independence, exact verdicts, inherited gaps and failed-instrumentation evidence.

## Default-security hold repair -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

At `afede0b5`, the existing summary test now uses a filled token with an exact
`claim-check` module list and requires the public summary roster to equal that
list with no token-gated label. The existing adopter upgrade-plan test now
requires both `dev/modules/content-security.md` and
`scripts/content_scan.py` to be absent from the plan output. The old private
helper cases remain in the committed tree.

The original 14 sealed patches are retained byte-for-byte in
`bootstrap/tests/fixtures/default_security_stance_promise_mutants.json`;
SHA-256 remains `380d2e78e177736f9430793647332fe7e78db9c48b5345132800a72f7b7ec4b4`.
The family-specific replay script creates disposable copies from its committed
candidate, removes the two old cases only in each disposable copy, and accepts
only reached call-assertion failures after healthy calls and successful setup
and teardown.

On a clean archive of `afede0b5`, canonical Python 3.13.13 collected and passed
the healthy family once: 18 passed in 1.96 s. The four new probes each passed
their healthy call then failed in the intended assertion after the mutated
line ran: S1 line 250, S2 line 255, U1 lines 966–967 and U2 line 1036. Each
mutant used its own fresh candidate copy and its tracked source was restored
before that copy was discarded. The prior ten caught results from High's
sealed comparison were reused; they were not rerun. No old test was removed
from the branch. The candidate still has 18 collected cases, so the required
net volume reduction remains outstanding.

This closes the two named witness findings for the requested targeted High
follow-up; it is not the review itself or authority to remove either old node.
No other family, full suite, native run, re-anchor or baseline was checked.
**Elapsed:** approximately 8 minutes; **tokens:** unknown.

## Default-security replay classifier repair -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

At the follow-up to `0a70b690`, the family replay runner now accepts the old
private-pair removal only when both the function and helper import are already
absent, rejects inconsistent or duplicate states, and classifies a catch only
when the owning call report records an `AssertionError` in addition to the
existing phase and changed-line requirements. The previous four-probe evidence
at `afede0b5` still demonstrates those real faults, but its runner did not
machine-check the exception class. This correction has not been rerun; the
targeted High follow-up must verify the updated filter and classifier against
the four public workflows. Both old nodes remain in the primary tree.
**Elapsed:** approximately 3 minutes; **tokens:** unknown.

## C2 default-security targeted Security Review -- GPT-6.1 Sol (High) -- 2026-11-09

**Foundations**

1. **Should this happen as framed?** Yes: the repaired existing public checks now catch all four faults behind findings 1–2 without the old helper cases. -- Fixed `233d492f`; four canonical replay workflows below.
2. **Best alternative.** Remove only the two agreed cases and unused import; the retained public parameters and filled-token control preserve their demonstrated protection without duplicate helper checks. -- Prior T2/T3 comparison; current test diff.
3. **What would show it wrong?** An exact-summary widening or unadopted-module plan surviving its repaired assertion would keep the family held; all four now fail their owning calls as intended. -- S1/S2/U1/U2 evidence below.

**Reviewed commit:** `233d492f267f0730531b8ba680d6bfcd1ffd2a3e`.
**Obligation:** second, targeted C2 removal-set Security Review addressing findings 1–2 and the changed replay classifier; not final code review.
**Verdict:** findings 1–2 CLOSED; AGREE to this family's exact removal set: `test_an_unfilled_python_package_token_does_not_select[{{python_package}}]` and `test_an_unfilled_python_package_token_does_not_select[   ]`. Both remain absent from `NATIVE_ONLY_NODE_IDS`, checked against a listed positive control. No manifest-member removal is needed.
**Elapsed:** approximately 8 minutes. **Tokens:** unknown.

I prepared committed disposable `05c20bf1f1355a7748b7e0d77a887d9ba5ad1a66` with the old function/import already absent. Running `scripts/replay_default_security_stance_mutants.py` there under canonical `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13) exercised the idempotent absence branch and all four fixed workflows once, exit 0 in 11.216 s. Each healthy owning call passed; each mutant raised `AssertionError` during that call with successful setup/teardown and reached changed lines: S1 250; S2 255; U1 966–967; U2 1036. Copies were restored; the outer checkout remained clean. Log: `/private/tmp/default-security-pass2-sol-233d492f.log`. The sealed fixture digest is unchanged.

The prior ten caught comparisons and healthy 16-case baselines are reused. Their selection/reporting predicates and retained witnesses are unchanged; current adjacent differences add content-security install mappings and tighten a separate upgrade edit-check guard. Initial copy preparation rejected an ignored historical tracked reflection; adding the explicit extracted tracked paths with force corrected preparation before any probe ran.

Record checks: claim, link and snippet checks passed; neutrality reported fail=0, info=43.

**Coverage:** Read only the committed repairs, fixed runner/data and affected selection paths; ran four targeted workflows, no earlier matrix, other family, native execution or suite. Low may now remove exactly the old function/import and record the final 16-case family check. Final code review, Boundary B, combined volume accounting and release holds remain due; no canonical test was removed here. Over target to retain exact agreement, evidence reuse and preparation limits.

## Default-security agreed removal -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

At `fef3218c`, I removed only the High-agreed function
`test_an_unfilled_python_package_token_does_not_select` with its exact
placeholder and three-space cases, and the now-unused `token_gated_modules`
import. The public parameterized roster witness, filled `mypkg` positive case,
exact-summary assertions, and both existing-adopter plan exclusions remain.
No implementation source or native-manifest row changed; High confirmed these
IDs absent from `NATIVE_ONLY_NODE_IDS` with a positive control at `fca398e2`.

A clean committed archive under canonical Python 3.13.13 passed the remaining
family once: **16 passed in 1.82 s**. The collected count is reduced from 18 to
16: one test definition and two parameter-expanded cases removed. No old/new
mutation matrix, other family, full suite, native run, final code review,
Boundary B, or re-anchor was performed. This executes only the exact removal
authorized by High; family-level plan work and combined volume accounting
remain open. **Elapsed:** approximately 4 minutes; **tokens:** unknown.

## C2 prose-control reduction -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

At `c8326634`, I removed the seven wording-only definitions (14 expanded
cases) cleared by Medium `b8d4f07b` and the thirteen obsolete controls cleared
by Medium `96f6fbc7` from the three named test owners. Install parity,
correspondence, slots, schema, mapping, SVG, drain and live public behavior
checks remain. No support runner or fixture was added; only now-unused local
helpers/constants were removed. The combined volume on these owners fell from
98 definitions / 404 collected cases at parent `4631fb61` to 78 / 370 at
`c8326634` (20 definitions / 34 cases fewer).

On separate clean archives under canonical Python 3.13.13, collect-only over
the three changed owners found 404 cases before and 370 after. The focused
retained checks passed: all of `test_writing_rules_ship.py`, plus review-sweep
body/installed-loop/pointer and review-stance roster nodes, **25 passed in
1.53 s**. Collection took 0.12 s before and 0.11 s after. No full suite,
five-file mapped batch, mutation comparison, other family, native run, or
release check was performed. C2 and combined test-volume work remain open.
**Elapsed:** approximately 14 minutes; **tokens:** unknown.

## C2 security-leaf public witness preparation -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

Frozen baseline commit `96c9898375c43cd45f12b0ee138b9f37f66a6c79` passed the
entire leaf owner once in a clean Python 3.13.13 copy: 16 passed in 0.21
seconds. Candidate `82d29a89c73c644303965de780fccfe70d10d293` adds one public
`seed_gitignore` refusal witness and the test module's public `Promises:` list;
the same clean-owner selection passed once: 17 passed in 0.22 seconds.

The new witness catches the facade-exported `ScaffoldSecurityError` and checks
that an outside file's bytes and the target's `.gitignore` symlink remain
unchanged. The promise list covers refusal before outside changes, the exported
facade exception, and cleanup limited to still-owned temporary files. No
product source, definition-count pin, defense, or native-only identity changed.
The three existing native IDs remain in place.

This prepares only the candidate for the planned fresh High review and
independent old/new defensive-site comparison. It does not authorize removing
`test_scaffold_security_error_defined_exactly_once_in_the_leaf`; that pin stays
until both gates agree. No other family, full suite, native replay, removal,
code review, or Security Review ran. **Elapsed:** unknown; **tokens:** unknown.

## C2 security-leaf family Security Review -- GPT-6.1 Sol -- 2026-11-09

**Obligation:** Internal Security Review (family gate only)
**Candidate:** `82d29a89c73c644303965de780fccfe70d10d293`
**Baseline:** `96c9898375c43cd45f12b0ee138b9f37f66a6c79`
**Verdict:** HOLD -- defensive-site evidence incomplete.
**Elapsed:** approximately 15 minutes. **Tokens:** unknown.

**Foundations**

1. **Should this happen as framed?** The proposed
   `test_scaffold_security_error_defined_exactly_once_in_the_leaf` removal loses
   unused-class counting, an accepted internal-only loss. Retained identity
   tests and the public seed witness protect exported catchability and outside
   bytes. The node stays until C2 completes.
2. **Best alternative.** Keep this pin while resolving the outstanding sites;
   retain guard-routing, hostile-state and all three native-only nodes. The
   definition count itself adds no independent caller-visible guarantee.
3. **What would show it wrong?** An old-caught/new-missed behavioral mutant
   blocks removal. None occurred; a surviving accepting mutant at an unresolved
   site still needs an owning witness or specific redundancy explanation.

**Evidence.** Before reading tests, sealed 66 cases in
`bootstrap/tests/fixtures/promise_security_leaf_independent_mutants.json`
(SHA-256 `f06c1445c03a7384cdda7b06cacdfb24f8eb1ac8d52a4f96ef03807e7eab6090`).
A fresh source-only GPT-6.1 Sol sealed 20 omitted-site cases in
`bootstrap/tests/fixtures/promise_security_leaf_gap_mutants.json`
(`2b2348e301e1a5b1e1ede3034588bb6ddfa77aafabd78589782ac530d3380fa3`).
Python 3.13.13 leaf baselines: old 16 passed/0.21 s; new 16 passed/0.16 s,
only the proposed pin deselected; public witness executed. Exact removal,
hardening, fanout and seed owners: 41 passed each/0.41 and 0.40 s.
Across 86 old/new comparisons, 44 were detected by both, zero lost detections;
the nonblocking-flag mutant timed out at 12 s on both. Sessions
23140/95523/81957 exited zero; commands, stdout/exits and results remain under
`/private/tmp/cairn-leaf-sol-review`.

**Blocking finding.** Twenty-nine component survivors lack complete behavioral
or redundancy dispositions, including staging-failure owned-temp cleanup,
staged-name races, fanout final containment and descriptor-error handling.
Close with independently specified probes and explicit per-site dispositions;
this pass grants no removal authority.

**Coverage:** Committed source, exact node, public witness, manifest reason
“Smallest shipped security surface” and owning hostile tests. Thirteen
unchanged launcher cases belong to separate loader infrastructure. No whole-plan
review, native removal approval, certification or release operation; ordinary
and whole-plan Security Reviews remain owed.

### Same-pass author handoff -- GPT-6.1 Sol -- 2026-11-09

The 29 survivors above are evidence cases, **not 29 required tests**. This
clarifies the first pass at `61850b89`; it is no additional review or clearance.
References below name sealed fixture source lines or supplement IDs.

**No additional witness justified by these mutations:** security.py lines 73
(remaining inode check rejects last-name swaps; accepted parent-race boundary
unchanged), 141/171 (walking above the resolved target still stops at
`relative_to`), 23 (exception base changes, exported identity remains), stage
line 59's `O_NOFOLLOW` (`O_CREAT|O_EXCL` already refuses an existing name), read
line 231/folder line 281's `O_CLOEXEC` (Python's opened descriptors are
non-inheritable), and gap12's `O_DIRECTORY` (a nonfolder descriptor cannot
resolve the remaining child). These eight textual mutations do not establish
lost public protection.

**Concrete missing-witness groups:**

- Lines 81/82: public seeding with an injected staging write/mode failure must
  preserve the destination and remove its owned temporary; current coverage
  injects replacement failure, later in the operation.
- Lines 75/95/97: swap the staged name to a hardlink during staging, then in a
  separate case swap after the replacement helper snapshots the staged inode,
  before its final guard/recheck. Refuse changed identity/final destination
  links; preserve outside bytes/mode and unowned names. The
  existing symlink swap is earlier and intercepted by another guard.
- Line 147/gap02: exercise an in-tree linked parent and an escaping fanout
  destination respectively. Existing selected parent tests use an escaping
  link, leaving in-tree refusal and the fanout final check unexercised.
- Removal read line 231's `O_NONBLOCK`: a FIFO needs a bounded child witness;
  without the flag the removal reader can block before its regular-file check.
- Gap04/06/07/08/10: inject read/stat and the named open failures; seed/removal
  must use the exported security exception. Existing selected tests do not
  reach these error-conversion branches.
- Gap16/18: inject a non-absence stat error after unlink and in confirmation-only
  mode; return false/keep the record, rather than claim confirmed absence.

**Effects still unestablished:** line 226's malformed-parts flip crashes rather
than accepts; gap05's lexical alias has no identified public caller; line 237
needs a special file plus matching expected bytes; removal `O_NOFOLLOW` retains
an opened-versus-name identity check; both `O_NOCTTY` cases require a native
controlling-terminal counterexample. These are probe questions, not automatic
new-test requirements or waived controls. Source defenses and the held pin stay.

**Coverage:** Static classification and existing-owner gap mapping only; no
matrix rerun or new behavioral measurement. Extra text makes the original
finding actionable rather than prescribing one test per textual flip.
**Elapsed:** approximately 5 minutes; **tokens:** unknown.

## Implementation verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

Commits `a741be46` and `bd5057de` add witnesses in the existing seed,
hardening, fan-out and retired-file owners. The leaf's exact-definition pin,
all prior defenses, product source, and its three native-only nodes remain
unchanged. The tests exercise public seed read/open/fstat errors and staging
write/mode failures; during-stage and post-snapshot hardlink swaps; an in-tree
linked parent; the public fan-out final containment guard; removal open/fstat
errors in both branches, target-folder open refusal, and bounded FIFO refusal.

On committed copies, Python 3.13.13: seed witnesses 6 passed, then the one
late-swap timing correction passed on retry; hardening 2 passed; fan-out 1
passed. Retirement witnesses had 8 passed and 3 failed. The two by-path
confirmation cases returned `removed` on injected EACCES where they must keep
the record. The public step case left the file present but cleared its retired
record. These are current source defects, not test skips or waivers; the
security-leaf pin/removal remains blocked pending a separately reviewed fix.
The earlier 3.12.9 retirement setup error was rerun under 3.13.13. The first
late-swap failure was a fixture hook firing before staging; the corrected hook
was verified after the staged inode snapshot.

New POSIX-only witnesses awaiting High source-policy classification:
`test_public_seed_gitignore_rejects_hardlink_swap_during_staging_without_deleting_unowned_name`,
`test_public_seed_gitignore_rejects_hardlink_swap_after_staged_identity_snapshot`,
and `test_retired_fifo_is_refused_in_a_bounded_owned_child`. No policy count
changed. The earlier 16/17 leaf baselines, mutation matrix, full suite, and
native runs were not repeated. **Elapsed:** unknown; **tokens:** unknown.

### Interpreter attribution correction -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

The initial seed, hardening and fan-out runs above used system Python 3.12.9;
those figures are not canonical verification. Corrected runs used
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13) in the clean
`bd5057de` copy: seed 7 passed in 0.05 s, hardening 2 passed in 0.02 s, and
fan-out 1 passed in 0.05 s. Raw outputs are
`/private/tmp/cairn-security-leaf-seed-313.log`,
`/private/tmp/cairn-security-leaf-hardening-313.log`, and
`/private/tmp/cairn-security-leaf-fanout-313.log`. The canonical retirement
result remains 8 passed/3 failed and was not repeated. The earlier 3.12.9
retirement setup error is retained as a noncanonical attempt. **Elapsed:**
0.12 seconds total test time; **tokens:** unknown.


## Security-leaf platform source classification -- GPT-6.1 Sol (High) -- 2026-11-09

**Foundations**

1. **Should this happen as framed?** Classify by the operation required, not
   the current skip: two new nodes require POSIX behavior, while the third's
   source does not establish that restriction -- `bootstrap/tests/security_manifest.py`,
   `NATIVE_ONLY_NODE_IDS`; the exact nodes below at `bd5057de`.
2. **Best alternative.** Transfer only the two justified POSIX identities and
   repair the post-snapshot node's unnecessary skip rather than permit an
   unsupported release omission -- `_stage_exclusive` closes its descriptor
   before `_write_by_replacing` invokes that node's guard hook in
   `bootstrap/_scaffold/security.py`.
3. **What would show it wrong?** A concrete platform dependency in the
   post-snapshot path would justify revising its classification; otherwise
   portable collection must retain it and native Windows execution should
   exercise its identity assertion -- the post-snapshot node below.

**Reviewed source:** `a741be46` and timing correction `bd5057de`; the two test
files are unchanged between `bd5057de` and `c1cabed4`. **Verdict:** two POSIX
classifications eligible; one native-policy transfer held. No policy changed.

- `bootstrap/tests/test_security_leaf.py::test_public_seed_gitignore_rejects_hardlink_swap_during_staging_without_deleting_unowned_name`
  -- POSIX: the injected swap unlinks a staged file while its descriptor is
  open, and asserts exact 0600 permissions on the outside inode.
- `bootstrap/tests/test_upgrade_removes_retired_files.py::test_retired_fifo_is_refused_in_a_bounded_owned_child`
  -- POSIX: creates an `os.mkfifo` filesystem FIFO and tests its nonblocking
  read/refusal in a bounded child; this is not a Windows named-pipe test.
- `bootstrap/tests/test_security_leaf.py::test_public_seed_gitignore_rejects_hardlink_swap_after_staged_identity_snapshot`
  -- HOLD: the descriptor is already closed; `os.link`, unlink and identity
  comparison do not establish a POSIX requirement. Its existing skip reason
  alone cannot authorize omitting it on Windows. Close by removing the
  unnecessary platform skip with affected verification, or showing a concrete
  source dependency before transferring this ID.

Python's [os documentation](https://docs.python.org/3.13/library/os.html)
confirms Windows hardlink support, Unix-only `mkfifo`, and different open-file
unlink behavior; `fchmod` gained Windows support in 3.13, so its name alone is
not sufficient evidence.

**Coverage:** Source classification only; no tests, mutation matrix, native
run, policy identity/count edit or security-leaf pin removal. The existing
three native leaf IDs remain unchanged. **Elapsed:** about 10 minutes.
**Tokens:** unknown.

## Accepted amendment -- confirm retired-file absence -- GPT-6.1 Terra -- 2026-11-09

**Amendment review:** awaiting the usual and Security plan reviews of this
bounded addition; do not execute the addition before those reviews and response.
The existing plan remains implementing for its other accepted work.

**Source:** [accepted absence correction](../proposals/archive/2026-11-09-terra-confirm-retired-file-absence.md),
Maintainer Decision `e1a6556e`. This amendment delivers the public refusal
promise exposed by C2's retirement tests within the same independently
finishable outcome. No other plan, private permission or future observation is
needed; the source, failing regressions and host/Windows interpreters exist.

**Scope and build summary:** In `bootstrap/_scaffold/security.py`, replace the
two fallback `lexists` confirmations with explicit `lstat`: only
`FileNotFoundError` confirms absence; a present name or other `OSError` keeps
the record. Preserve all path validation, identity checks, handle-branch
behavior and existing race limits. Adapt the three existing denial regressions
in `bootstrap/tests/test_upgrade_removes_retired_files.py` to inject denial at
the actual confirmation, after earlier safety and identity checks. Preserve
their branch-hit assertions and public surviving-file/retained-record witness.
No new helper, API, schema or additional tool is needed.

**Sequence and estimate:** After these amendment reviews, Low implements the
two checks and test-seam correction, runs affected iteration checks and commits.
Independent ordinary and Security code review cover the fix before the final
wide Boundary B; coordinate it with this plan's still-open leaf removal review
without replaying the old mutation matrix. Estimate one focused work window
for correction and targeted checks, plus reviewer/native availability; unexpected
failures are uncertainty, not authority to omit accepted checks.

**Acceptance:** Both confirmation branches distinguish missing from denied
names. The three adapted regressions pass, including the real upgrade step
where a failed unlink leaves the file and its tracking record. Existing normal
removal, kept-file and containment/race behavior passes. Reintroducing the
error-to-absence mistake fails the adapted regression. Native Windows exercises
the applicable fallback witness; skips do not establish that result.

**Verification:** Map the changed engine/test paths with `tools/test_tiers.py`
and run that affected selection under canonical Python 3.13.x; preserve earlier
8-pass/3-fail evidence. Reviewers use committed source and tight independent
falsification, not another author suite. Final wide Boundary B after fixes
covers this addition and the plan's affected consumers; required checks remain
open until measured. A reviewed expected AST mismatch alone belongs to the
separate release operation, as already prescribed; unexpected drift remains
implementation work. No documentation or scientific result is changed.

**Scope delta:** addition explicitly authorized by the named accepted proposal;
no previously accepted outcome is removed. **Elapsed:** about five minutes.
**Tokens:** unknown.
