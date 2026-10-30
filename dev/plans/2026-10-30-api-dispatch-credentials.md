# Plan: API dispatch credentials

**Source proposal**: dev/proposals/archive/2026-10-30-codex-api-dispatch-credentials.md
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Pass only the local API policy's credentials to its dispatched check so configured checks can run.

## Source proposal

The accepted heavy proposal authorizes the local API leg to receive only present credentials derived from its validated local policy, while preserving binding, isolation and fail-closed behavior.

## Scope

Change the shipped dispatcher and its tests; update the API module description if needed. No doctrine surface. Reuse `_bind_runner` and the existing policy `load_policy` and `Policy.credential_names("local")`; searches of the dispatcher, API facade and `_security_net/policy.py` found these existing binding and derivation paths. No second parser or credential registry.

The parent first binds the facade and every engine member it will execute, using the existing immutable lockfile checks, including containment and no symlinks. Only then load that bound sibling package, verify engine completeness, import its policy module, and validate the bound local policy before deriving names. Load only the bound source bytes or use an equivalent cache exclusion; reject pre-existing module substitution. Do not import the facade or execute unbound package initialization. A binding, engine or policy failure fails closed without reading credential values. Preserve the runner's own verification-before-credential ordering. If this path cannot preserve the existing binding and isolation guarantees, stop for reassessment. Account for Windows paths and subprocess behavior without introducing platform-specific shell commands.

### Documentation / doctrine surface

The shipped module describes the handoff if its current wording needs correction; no governing doctrine changes.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Bind and load the existing policy engine safely, pass the selected local credentials, and cover installed dispatch | Both plan reviews and their dispositions | Dispatcher, tests and any necessary module description |

## Acceptance criteria

**C1.** Only present names from validated local principals reach the API local child; deployed-only, unrelated and malformed names do not. Other legs receive none, and reports reveal neither names nor values. Invalid or unreadable policy and missing credentials refuse or remain incomplete without broadening the environment. Existing runner, policy, engine binding and isolation checks remain effective; tampering with engine initialization or a policy member is refused before parent execution or credential lookup, and unbound cached executable bytes and pre-existing module substitution cannot execute. The installed actual dispatcher and runner with a two-principal loopback fixture match direct execution. Omitting a local credential and admitting a deployed-only credential each make their respective tests fail. The implementation records those mutations and the applicable checks below.

## Scope delta

**Scope delta**: preserved

## Verification

Boundary A: run `python tools/test_tiers.py for <changed paths>` and its selected tests, plus applicable prose claim, link, snippet, neutrality and `python scripts/check_cairn.py` gates. Inspect actual readers and byte pins. Include the configured installed-dispatcher and isolation nodes added to `bootstrap/tests/test_security_verification.py`, alongside existing `TestRealFacadesDrivenByTheRealDispatcher` and `test_child_env_is_minimal_and_strips_proxies_and_credentials`; use the loopback fixture in `bootstrap/tests/test_api_access_security.py` where practical. Exercise negative engine and cached-byte tampering, module substitution, and both handoff mutations in separate copies. Map exact added nodes and any additional callers in the implementation record.

Boundary C: independent ordinary code and Security Reviews read the committed implementation and its iteration evidence, and run only targeted falsification checks. Boundary B follows review once on a clean unchanged final commit under canonical Python 3.13.x: **wide**, because this changes a credential trust boundary. Run the iteration selection for the entire reviewed range plus mapped integration/workflow tests, the API and dispatcher owning test families and applicable standing gates. Record the tested SHA and reviewed range, interpreter, clean pre/post state, commands, counts, times, token use, non-pass dispositions and omissions; `Certified by: pending`. Full-tree certification and re-anchor are separate ceremonies, not part of this change.

## Plan Review -- Codex GPT-6 -- 2026-10-30

**Reviewed commit**: 38b19294
**Obligation**: Internal (plan)
**Verdict**: PROCEED
**Elapsed**: approximately 2 minutes
**Tokens**: unknown

**Foundations**:

1. **Should it happen as framed?** Yes. The accepted proposal requires exact local-policy credentials through the actual dispatcher. At 38b19294, `_evaluate_capability` binds the runner and policy before `_run_child`, whose `_build_child_env` currently excludes those credentials. C1 preserves that binding and requires the configured installed path, not just a helper test.
2. **Best alternative.** Running the API runner directly avoids the new handoff but loses dispatcher execution. Reusing the bound policy engine and its existing credential-name derivation is the smallest path that retains the accepted isolation; a prefix allowlist would admit unrelated credentials.
3. **What would show it wrong?** A direct and dispatched configured run disagree, either required handoff mutation survives, or engine tampering executes before refusal. C1 and its verification require these checks; their results are not yet measured.

**Findings**: None. The plan maps the accepted delivery, refusal, isolation and tamper outcomes to one implementation chunk and requires exact test nodes in the implementation record.

**Coverage**: Read the committed plan, accepted proposal and dispatcher binding and child launch paths, and inspected the runner's policy and credential ordering. Did not execute implementation tests, audit every policy validation edge, or assess the boundary in depth; the separate Security Review remains owed.


## Plan review -- Codex GPT-6.1 Sol -- 2026-10-30

**Foundations**:

1. **Should it happen as framed?** Yes. C1 preserves the accepted exact-local handoff and binds every engine member before parent execution. Existing `_bind_runner` checks each additional immutable path; `_security_net/__init__.py` imports policy, net and report during completeness verification, so binding all members first is necessary.
2. **Best alternative.** Keep loading confined to the bound sibling engine and reuse `Policy.credential_names("local")`. Direct execution loses the accepted dispatcher path; a new parser duplicates validation. The plan's stop-for-reassessment rule prevents a convenience fallback from widening authority.
3. **What would show it wrong?** Tampered initialization or policy executes in the parent, invalid policy broadens delivery, or either handoff mutation survives. C1 requires negative tamper checks and installed two-principal execution; implementation outcomes remain unmeasured.

**Reviewed commit**: 38b19294
**Obligation**: Internal Security Review (plan)
**Verdict**: PROCEED
**Elapsed**: approximately 4 minutes
**Tokens**: unknown

**Non-blocking advice**: Make the verified loading path exclude unbound cached executable bytes and pre-existing module substitution. The current facade's `_load_engine` uses `spec_from_file_location`; binding source files alone does not establish which cached bytes a standard loader executes. Close this advice with source-only loading or equivalent cache exclusion, plus a negative cache-tamper test. This implements the existing no-unchecked-code criterion without widening scope.

**Coverage**: Read committed plan and accepted proposal, dispatcher binding/environment paths, facade loader and verification ordering, and engine completeness imports. Did not execute implementation checks, audit every policy schema case, or measure Windows subprocess behavior; no implementation reviewed.

## Response to plan review -- Codex GPT-6 -- 2026-10-30

**Elapsed**: unknown
**Tokens**: unknown

Ordinary review found no findings. Accepted Security Review advice: Scope and C1 now exclude unbound cached code and module substitution; Verification requires negative checks. These clarify the accepted no-unchecked-code criterion.

## Code review -- Codex GPT-6 -- 2026-10-30

**Reviewed commit**: 4d96b627
**Verdict**: CHANGES REQUIRED
**Elapsed**: approximately 3 minutes
**Tokens**: unknown

**Foundations**:

1. **Should it happen as framed?** Yes. The dispatcher binds the facade and selected engine members before validating policy; only names returned by `credential_names("local")` are added to its child environment.
2. **Best alternative.** Reuse the bound policy engine, as implemented. A broad credential prefix would admit names outside the local policy, while direct execution would lose dispatcher coverage.
3. **What would show it wrong?** A deployed-only credential reaching the child, a local credential omitted, or unbound engine bytes executing would falsify the design. The configured and tampering checks passed, but the required mutations are not recorded.

**Blocking finding**: C1 and Boundary A require separate local-omission and deployed-only-admission mutations and their results. Neither the plan at 4d96b627 nor that commit's message records these outcomes; the commit also reports an initial scoped run with a failure followed by focused checks, rather than a passing final scoped selection. Close by recording the required mutation outcomes and a passing applicable scoped selection, or the disposition of each non-pass, on the implementation's committed bytes.

**Evidence and coverage**: Read the committed plan, dispatcher diff and added tests. In a separate archive of 4d96b627, Python 3.12.9 ran the configured, engine-tamper, invalid-policy and missing-credential nodes: 5 passed in 1.40 seconds. Did not audit all policy schema cases or Windows behavior; the separate Security Review and final Boundary B remain owed.

## Implementation verification -- Codex GPT-6.1 Luna -- 2026-10-30

**Boundary A**: `python tools/test_tiers.py for templates/modules/default-on/run_security_verification.py bootstrap/tests/test_security_verification.py` selected the nine files named below. On a clean Git clone of implementation commit `4d96b627`, Python 3.12.9 ran that selection: 519 passed, 2 skipped in 100.32 seconds. The iteration target is 30 seconds; this run exceeded it. Per-file durations were not collected, so no individual file is assigned to the >10-second list here.

**Tested commit**: `4d96b627b35a99d52f59e67ad02a1c9c1c9ac54a`

**Reviewed range**: `ea16abda64ba54c25eb1a43251225f8708576761..4d96b627b35a99d52f59e67ad02a1c9c1c9ac54a`

**Interpreter/runtime**: `/Users/kendal30/conda_envs/miniforge3/bin/python`, Python 3.12.9.

**Pre-run state**: clean clone at `4d96b627`; no staged or unstaged changes.

**Post-run state**: clean clone at the same commit; no staged or unstaged changes.

**Scoped selection**: `bootstrap/tests/test_default_security_stance.py`, `test_module_merge_lockfile.py`, `test_notice_install.py`, `test_security_finding_confidentiality.py`, `test_security_lint.py`, `test_security_marker.py`, `test_security_stack.py`, `test_security_verification.py`, and `test_upgrade.py`. The two skips were the local Bandit-dependent checks: the standalone security-lint gate and the real-Bandit shadow-isolation check. Bandit was unavailable locally; those checks are not evidence for this credential handoff. The Security Review and post-review Boundary B remain owed.

**Required mutations**: Starting from separate clean archives of `4d96b627`, the configured installed-dispatcher test `TestRealFacadesDrivenByTheRealDispatcher::test_configured_api_dispatch_hands_only_validated_local_credentials` was run once per mutant under Python 3.12.9. In the first copy, the dispatcher dropped one derived local credential; the test failed as required because dispatch returned exit 20 instead of the direct run's CLEAN exit 0 (1 failed in 0.98 seconds). In the second copy, the loader admitted `CAIRN_API_P3_CREDENTIAL`; the test failed as required at the exact local-name/environment assertion (1 failed in 0.76 seconds). Each mutant was killed; the unmutated control passed in the scoped selection.

**Non-pass disposition**: An initial source archive without `.git` made four unrelated historical-upgrade tests fail because those tests require a Git checkout for `--to HEAD`. That archive was not a valid checkout. The required nine-file selection was rerun from a clean Git clone of the same implementation commit and passed as recorded above.

| Command | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---|
| `python -m pytest -q bootstrap/tests/test_default_security_stance.py bootstrap/tests/test_module_merge_lockfile.py bootstrap/tests/test_notice_install.py bootstrap/tests/test_security_finding_confidentiality.py bootstrap/tests/test_security_lint.py bootstrap/tests/test_security_marker.py bootstrap/tests/test_security_stack.py bootstrap/tests/test_security_verification.py bootstrap/tests/test_upgrade.py --tb=short` | 0 | 519 passed, 2 skipped (Bandit unavailable) | 100.32 s | unknown |
| Configured dispatch test in local-omission mutation copy | 1 | Mutant killed: dispatched result became exit 20 instead of CLEAN exit 0 | 0.98 s | unknown |
| Configured dispatch test in deployed-admission mutation copy | 1 | Mutant killed: exact local credential-name assertion rejected added P3 | 0.76 s | unknown |

**Boundary B**: Pending the separate Security Review. Run once after both reviews on a clean, unchanged final commit under canonical Python 3.13.x; mode remains **wide** for this credential trust boundary. Full-tree certification and re-anchor were not run.

## Security code review -- Codex GPT-6.1 Sol -- 2026-10-30

**Reviewed commits**: implementation `4d96b627`, iteration/response `a061fa6d`.
**Obligation**: Internal Security Review (code)
**Verdict**: PROCEED; no blocking findings.
**Elapsed**: approximately 7 minutes. **Tokens**: unknown.

**Foundations**:

1. **Should it happen as framed?** Yes. `_evaluate_capability` binds the selected engine members and policy before parent execution; `_load_api_local_credential_names` compiles source directly and reuses validated local-principal derivation. `_build_child_env` receives those names only for the API leg. This delivers C1.
2. **Best alternative.** Retain this bound source-only loading. Ordinary import loaders can execute unchecked cached bytes; a prefix allowlist would admit unrelated credentials. 
3. **What would show it wrong?** Unbound code execution, module substitution, or an omitted/local or admitted/deployed credential surviving checks. In a separate archive of `a061fa6d`, Python 3.12.9 ran the configured, engine-tamper, invalid-policy, missing-credential and minimal-environment selection: **6 passed in 1.44 seconds**. A separate loader probe excluded an unchecked-hash poisoned cache and refused all four private package/member substitutions. Both required handoff mutations are recorded killed.

**Non-blocking advice**: Strengthen the committed cache-poison fixture with valid unchecked-hash bytecode. Its current timestamp cache comes from another source and may be rejected by an ordinary loader without testing cache exclusion. The stronger parent-loader probe passed.

**Coverage**: Examined credential derivation, binding/engine ordering, isolated child environment and confidentiality assertions. The two Bandit skips concern scanner availability and scanner shadow isolation; neither exercises this handoff. Did not run Bandit, Windows, full certification or Boundary B. A later modified loopback attempt hit socket permission denial before dispatch. Boundary B remains due after review.

**Author response**: Not adopted: the committed source-only loader already passed the Security Review's valid unchecked-hash bytecode probe, so a fixture-only change would duplicate this evidence without changing runtime behavior.

## Targeted Security code review -- Codex GPT-6.1 Sol -- 2026-10-30

**Reviewed commits**: loader replacement `2ccfc076`, metadata correction `1e849d4a`.
**Obligation**: Internal Security Review (code, changed loader only)
**Verdict**: PROCEED; no new findings.
**Elapsed**: approximately 2 minutes. **Tokens**: unknown.

**Foundations**:

1. **Should it happen as framed?** Yes. `_BoundSourceLoader.get_code` reads the named source and compiles it directly, bypassing bytecode lookup. Binding still precedes loading. The explicit `__file__` assignments restore the package's existing relative completeness checks.
2. **Best alternative.** Keep this source-loader override. A normal source loader could execute unchecked cached bytecode; weakening Bandit's rule would retain the reported lint failure rather than satisfying the accepted checks.
3. **What would show it wrong?** A valid poisoned cache executing, substituted modules being accepted, or completeness failing because module metadata changed. In a separate archive of `1e849d4a`, Python 3.12.9 ran the engine-tamper and invalid-policy selection: **3 passed in 0.46 seconds**. A targeted loader probe placed valid unchecked-hash poison caches beside all four engine sources: local-name derivation and completeness still succeeded. Four private module substitutions, wrong loader name/path, and namespace cleanup also behaved as required.

**Coverage**: Inspected the two loader diffs and falsified cache, substitution and metadata failure paths. Prior credential/environment review stands. Did not repeat the owning families, run Bandit, exercise Windows or conduct Boundary B; post-fix integration remains the author's obligation.
