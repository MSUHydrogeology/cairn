# Plan: Public contract repairs

**Source proposal**: [Public contract repairs](../proposals/archive/2026-11-12-codex-public-contract-repairs.md)
**Status**: revising-plan
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-12
**In brief**: Refuse damaged project data cleanly and repair the comparison and test promises exposed by public testing.

## Build summary

Repair install and upgrade refusals and the oracle's provenance allowance, remove unused
sweep code, and finish the affected public-test conversions. Update shipped copies,
guard references, and the existing worklist and changelog. The result keeps existing
interfaces and security boundaries.

## Source proposal

The accepted heavy proposal assigns all five board item 24 defects, stale guard
references and affected held tests to one plan. Its preflight treats project and Git
administration data as untrusted; it requires clean pre-write refusal, narrowly bounded
comparison, ordinary and Security Review. Independent scientific check: N/A.

## Scope

In `bootstrap/_scaffold/install.py` translate expected binding-path `lstat` access
failures to the existing security refusal. In `upgrade.py`, validate the required
`files` record shape and needed `src`/`dst` before consumers, preserving containment and
source-identity checks; translate invalid tracked UTF-8 at its read boundary to a useful
refusal before writes. Do not catch arbitrary programmer `KeyError`. Preserve valid
workflows.

In `bootstrap/tests/_oracle.py`, use the security design supplied by
proposal_security_sol: `_normalize` returns bytes or an invalid sentinel; `_compare`
reports existing `bytes_differ` if either lock is invalid, including identical malformed
bytes. Only `_LOCKFILE_REL` is decoded as strict UTF-8. Skip ASCII whitespace and whole
leading `#` comment lines, then require one JSON object and trailing JSON whitespace
only. Reject BOM, internal comments and non-JSON constants. A strict `JSONDecoder`
rejects duplicate decoded keys at every depth and constants; `raw_decode` walks root
key/colon/value/comma/close grammar, tracking decoded root keys and raw value spans.
Require exactly one string each for `cairn_version` and `cairn_commit`; validate the
whole document, then replace only their value spans right-to-left with the fixed JSON
string `"<pinned>"` and encode strictly. Preserve all other bytes. Catch only Unicode,
JSON, value and recursion failures as invalid. Remove the YAML regex; YAML-shaped input
is invalid. Keep helpers private in the existing file.

Remove `_git_subcommand` and `ACCOUNTED_GIT_SUBCOMMANDS` from the sweep and twin,
retaining active accounting, admission and host evidence. Correct stale test names in
`tools/session.py`, `scripts/content_scan.py`, `bootstrap/_scaffold/config.py` and
shipped twins; update normal source pins and twin records, without re-anchoring. No
doctrine surface changes.

**Reuse:** Searches for `_git_subcommand` and its set found definitions, twins and
private tests, not production consumers; `_check_lockfile_paths` already validates
present fields, and
`test_oracle.py::test_oracle_reports_a_target_engine_that_only_rewrites_existing_files`
exercises engine rewriting through `run_oracle`. Reuse these surfaces, not a new API or
parser module.

## Sequence

One coherent chunk, estimated one to two working days including reviews and
verification; the cost of public conversions and security edge cases is uncertain. No
release ceremony or future plan is a prerequisite.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Repair refusals and comparison, remove dead code, reconcile held tests and references | Plan review, including Security Review | Code, shipped twins, public promise checks, worklist and changelog |

Before Low-tier execution, map each `WAIT-FOR-ITEM-24` row in
`dev/measurement/promise-testing-worklist-2026-11-11.csv` to a retained or extended
public node and consumer, then record the disposition there. Use these existing homes
and entry points: profile whitespace rows →
`test_profile_grammar.py::TestUnknownKeysRefuseBeforeAnyWrite::test_a_real_install_refuses_with_nothing_written`
(install); lazy fetch →
`test_reanchor.py::TestLazyFetchCannotRunAnUnlistedTransportHelper::test_the_checker_binds_it_too`
(checker command); pulse →
`test_replacement_tools.py::test_public_pulse_attaches_multiple_explicit_sidefiles_and_leaves_ambiguous_orphans`
(pulse command); helper pin →
`test_security_stack.py::test_member_command_refuses_a_wrong_pin_or_helper_layout_before_the_helper_runs`
(member command); interpreter path rows →
`test_session_binding_untracked.py::test_a_binding_written_on_this_machine_is_still_used`
(session command); session write rows →
`test_session_writes_contained.py::test_session_start_in_copy_mode_refuses_a_link_file_or_folder_in_the_copy_path`
and `::test_the_pruner_command_exits_with_a_plain_refusal_for_a_linked_folder`
(session/pruner commands); edit guard rows →
`test_upgrade_edit_check_runs_no_project_programs.py::test_apply_goes_on_with_no_git_and_stops_when_git_does_not_answer`
(upgrade apply); lock shape →
`test_upgrade_lockfile_path_containment.py::test_a_dst_that_leaves_the_project_is_refused_on_every_action`
(upgrade). Extend or replace those homes when needed to actually exercise each stated
promise, not merely cite them; retain release-roster guards. Run individual nodes with
`python -m pytest bootstrap/tests/<file>::<node>`.

## Acceptance criteria

**C1.** Public install and upgrade reject invalid UTF-8, malformed `files`/missing `src`
or `dst`, and denied binding access nonzero, with useful bounded diagnostics, no
traceback and no writes; valid control succeeds. The public oracle workflow equates only
provenance value changes and reports changed hash, nested field, unrelated bytes and
malformed or ambiguous lock, including identical malformed input. Exercise escaped keys,
duplicates, comments, invalid encoding and trailing data as meaningful falsifiers.
Sweep's public unknown-command refusal and valid accounting persist. Each of the 15 held
rows has a public promise check or evidenced existing coverage, without removing release
guards. Twin checks and corrected references agree; temporary debugging tests are
removed.

## Verification

Use `/Users/kendal30/conda_envs/lhm/bin/python3.13`. Before fixes, demonstrate named
public checks catch their faults; the saved `f8b02eea` reproduction and logs at
`/private/tmp/cairn-board24-public-repro-20261112/` are evidence for the three CLI
failures and valid control. Extend the existing install and upgrade public refusal
fixtures; use the oracle engine-rewrite workflow above and
`test_portable_security_sweeps.py::test_verify_version_support_refuses_a_candidate_that_invokes_an_unaccounted_git_subcommand`
for admission. Run `python tools/test_tiers.py for <changed paths>` and its named
iteration checks, prose claim/link/snippet/neutrality gates and applicable
twin/source-pin checks. Plan and code reviews include Security Review; code review
falsifies targeted cases. Boundary B is wide: on the clean reviewed final commit run
mapped owning families, known public and integration paths and standing gates, recording
commands, results, elapsed time, tokens and omissions. Full certification remains at its
established boundary.

## Plan review -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-12

**Reviewed commit:** `15c8d355`.
**Obligation:** Internal. **Verdict:** ACCEPT; no findings.

**Foundations**

1. **Should this happen?** Yes. The plan retains all accepted repairs and the
   15 held public-test conversions rather than treating parser deletion as
   completion. Its outcomes match the accepted source and the worklist's
   profile, transport, sidefile, binding, containment and upgrade promises.
2. **Best alternative.** Repair the existing entry points and reuse the
   existing test owners. A new parser module, diagnostic command or private
   test interface would add maintenance without delivering another user need.
   The specified standard JSON decoder and existing refusal machinery avoid
   those additions.
3. **What would show it wrong?** A malformed-state refusal that writes or
   succeeds, or an oracle comparison hiding an unrelated byte/hash change,
   falsifies the outcome. The plan requires these public falsifiers, a valid
   control and identical-malformed-input rejection before completion.

The High-supplied token-span algorithm specifies validation, duplicate handling,
precise replacement and failure behavior before Low execution. The plan names
public conversion homes and retains required release guards. Error handling is
restricted to expected input/access failures; arbitrary programmer errors are
not masked. No scientific result or governing duty changes.

**Coverage:** Read the committed plan, accepted proposal, all 15 waiting rows,
oracle comparison/writer and engine-rewrite test, relevant upgrade dispatch and
earlier public reproductions. **Not covered:** Implementation, every runtime
edge, Security plan review, platform execution or final integration. No tests
were rerun; existing evidence was read, not remeasured.
**Elapsed:** approximately six minutes. **Tokens:** unknown.

## Plan review -- GPT-6.1 Sol (Security Review, High) -- 2026-11-12

Reviewed commit: 0409bfa7

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: blocking
**Verdict**: REVISE
**Elapsed**: approximately eight minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: narrow input refusals, provenance-only comparison and retained public promises match the accepted contract; install ordering needs specification before Low execution -- source Decision at `9b37bdde`; plan C1.
2. **Best alternative.** Reuse the existing binding validator in a no-write preflight, preserving its final write-time guard; catching its error after installation cannot meet the accepted no-write outcome -- `bootstrap/_scaffold/cli.py:502`; `bootstrap/_scaffold/install.py:507`.
3. **What would show it wrong?** A denied binding access changing a fresh/partial target, or an oracle accepting identical malformed locks or hiding unrelated bytes, falsifies delivery -- plan C1 and public engine-rewrite workflow.

**Blocking:** The plan specifies translating binding `lstat` failures but not moving validation before writes. Current CLI creates directories and installs core/skills before `write_local_env`; catching the later exception still leaves a partial installation -- `bootstrap/_scaffold/cli.py:502` and `bootstrap/_scaffold/cli.py:538`. The saved reproduction installs first and then retries, so its unchanged target does not establish this ordering. Specify a no-write binding preflight before `create_dev_tree`, retain the final guard, and require the public denial check to snapshot a fresh/partial target as well as a valid control.

**Evidence:** Strict whole-document JSON validation, decoded duplicate rejection, two required string values, reverse span replacement and invalid-sentinel propagation preserve unrelated bytes. All 15 waiting rows map to existing public homes; sweep removal retains active shim admission and release guards. Shape validation is explicitly required before consumers, including the existing early advisory.

**Coverage:** Read committed plan/source, worklist, refusal dispatch, binding writer, oracle and sweep admission. No implementation tests, reproductions, mutations or suites rerun; runtime outcomes remain prospective. No governing rule changes.
