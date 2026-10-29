# Plan: Ordinary test maintenance

**Source proposal**: dev/proposals/archive/2026-10-28-codex-ordinary-test-maintenance.md
**Status**: ready-to-archive
**Plan review**: required(Internal)
**Opened**: 2026-10-28
**In brief**: Simplify one board test cluster without losing fault detection and share the resulting test-maintenance practice.

## Source proposal

The Maintainer accepted the two-node pilot staged after test-trust-boundary implementation and directed that it refer to the test-practice strategy and update the testing module (`cea1299d`).

## Scope

Inventory and, if useful, simplify the named JSON-output cluster in `bootstrap/tests/test_board_json_contract.py`; update `templates/modules/team-gated/testing-discipline.md` and its self-hosted copy `dev/modules/testing-discipline.md`. The strategy `dev/strategy/2026-10-27-antigravity-judicious-testing-and-simulation-verification.md` informs concise test-maintenance practice: inventory behaviors and plausible faults, preserve detection, use public entry points, reuse setup with fresh mutable repositories, and distinguish test scope from runtime. This does not adopt its ratio target, new simulation guidance, parallel pytest, or dependencies. The broader suite work remains open.

**Reuse.** `rg -n '_build_golden_main_tree|board.main|tmp_path' bootstrap/tests/test_board_json_contract.py` locates existing builders and public entry points; assess whether they fit before extracting a fresh builder. Do not change protected cases or controlling helpers, the fixture, product code, schema or gates.

### Documentation / doctrine surface

The testing module is adopter-facing practice, with a self-hosted mirror; route it under `docs/DOCUMENTATION_PLAN.md`. No cross-cutting governing rule changes. Vendor-neutrality applies to the module; this does not alter the neutrality rule or other named high-risk controls.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Inventory and fault map | Reviewed plan; Maintainer pilot-file allowance below | Cluster properties, fault ledger and retained assertions |
| C2 | Simplify cluster | C1 establishes a useful consolidation in the original file | Fresh setup reuse and preserved assertions |
| C3 | Update testing module | Reviewed plan and C1 evidence | Concise practice in shipped and self-hosted copies |

The Maintainer's pilot-file allowance below permits the named work in `bootstrap/tests/test_board_json_contract.py` without the trust-inventory eligibility, protected-file review or baseline prerequisites. Keep the two named test methods in their original file; do not extract or substitute them. Preserve their behavior and fault detection, run the mapped functional checks, and obtain the ordinary plan and code reviews. Do not change shared controlling helpers, product code, schema or gates.

## Acceptance criteria

### C1 — inventory and fault map

Inventory both `TestRecordFactsComeFromWhereTheFileSits::test_all_record_values_and_absent_vs_blank_and_headerless_files` and `TestOutputIsDeterministic::test_archives_unique_path_key_and_deterministic_ascii_json`: setup, public behavior and plausible faults. Map each property and fault to retained assertions and probes; retain it without a convincing replacement. No pre-edit test-family run, timing baseline or installed-roster eligibility check is required by the Maintainer's amendment.

### C2 — preserve behavior

Reuse immutable descriptions or builders creating fresh paths and mutable repositories per call. Preserve absent versus blank, header boundaries, headerless plain-view omission, distinct archive paths, ordering, ASCII bytes and reproducibility across roots. Keep both named nodes and the existing real CLI/subprocess failure and exit checks. Report changed setup and assertion counts without a before/after runtime claim. Only a certifying run supports whole-suite timing.

### C3 — module practice

Both module copies carry consistent concise guidance for behavior and fault inventory, preserving fault detection when consolidating, public entry points, reusable setup with fresh mutable repositories, and separating scope from runtime. Reconcile both copies’ claims that a tier alone conveys cost and scope and that the module does not teach test craft with the limited maintenance guidance. Preserve location-based tiers, negative guard tests and the existing module promises. Verify the actual installed wording through the mapped owners. Do not add simulation guidance or a numerical test-volume quota.

## Scope delta

**Scope delta**: degraded with the Maintainer's explicit allowance below. The module update remains accepted scope. The named methods stay in their original file; the trust-inventory classification, installed-roster eligibility check, protected-file review/baseline work, extraction and matched timing baseline do not gate this pilot. Functional verification and ordinary reviews remain required.

## Verification

Boundary A: run the two named nodes and owning `bootstrap/tests/test_board_json_contract.py` family, including real `tools/board.py` paths. Search imports and readers of touched tests and helpers before edits; add any owners found. For the module run `bootstrap/tests/test_practice_modules.py`, `bootstrap/tests/test_doc_governance.py`, `bootstrap/tests/test_presets.py` and `bootstrap/tests/test_profiles_smoke.py`; search again for readers, mirrors and manifest pins at implementation and include those found. Check copies and installation content. Run applicable claim, link, snippet, prose-integrity and neutrality gates; inspect each trigger. Run timed control and final family with identical `pytest --durations` settings and environment.

Boundary B is full if a contract or trust-ceremony surface is touched, an effect cannot be bounded, or a required mapping is missing; otherwise record bounded mode with surfaces, tests, gates, counts, rationale and explicit absence of those surfaces. After the final implementation commit, run the scoped mapping and standing gates on a clean unchanged tree under `/Users/kendal30/conda_envs/lhm/bin/python3.13`. Record tested SHA and range, interpreter, pre/post state, commands, outcomes and counts, timing, non-pass dispositions and omissions. Set **Certified by**: pending until the next authorized certifying run. The independent code reviewer challenges the evidence and fault preservation without running the full suite.

## Plan review -- Codex (Terra), Internal plan reviewer -- 2026-10-28

```
Reviewed commit: b4cae7c239c3aabf8d5952a71b5e2c9b27446991
Target: Source proposal through Verification
Prior findings: none
Assurance path: required(Internal)
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** The staged pilot and matched scoped timing deliver the accepted two-node contract, but the module criterion leaves an existing contradiction in place. -- `dev/proposals/archive/2026-10-28-codex-ordinary-test-maintenance.md` > Complete current contract; `templates/modules/team-gated/testing-discipline.md` > Template content.
2. **Best alternative.** Keep the staged pilot and reconcile the module's existing tier explanation while adding the requested maintenance practice; an appended paragraph alone cannot settle both claims. -- `dev/strategy/2026-10-27-antigravity-judicious-testing-and-simulation-verification.md` > Review; `templates/modules/team-gated/testing-discipline.md` > Template content.
3. **What would show it wrong.** An installed protected roster covering the file, no useful fresh builder, or a fault without a retained probe stops the pilot; incompatible tier guidance would also leave the module update incomplete. -- plan C1–C3; `bootstrap/tests/test_board_json_contract.py` > `TestOutputIsDeterministic`.

**F1 — Blocking: reconcile existing module claims with the new practice.** C3 asks to separate scope from runtime while retaining tier guidance, but the existing module says a tier alone tells readers a test's cost and scope, and says it does not teach test craft. Adding the requested maintenance guidance without changing these claims can leave adopters with contradictory instructions. Specify that C3 revises those claims in both copies while preserving location-based tiers and negative tests, and verifies the installed wording. This carries the requested practice rather than discarding the existing scheme. -- `templates/modules/team-gated/testing-discipline.md` > introduction and Template content; `dev/modules/testing-discipline.md`; plan C3.

**Covered**: accepted scope and staging (proposal Complete current contract and Decision; plan C1); public path and fault coverage (`bootstrap/tests/test_board_json_contract.py` > `TestRecordFactsComeFromWhereTheFileSits` and `TestOutputIsDeterministic`; plan C1–C2); reuse (plan search and `rg -n 'def _build|def _run_json' bootstrap/tests/test_board_json_contract.py`); fail-closed eligibility (plan Sequence); module consistency and installation (`bootstrap/_scaffold/config.py` > testing-discipline; `bootstrap/tests/test_practice_modules.py` > `TestInstallPath`; F1); scientific scope (plan Scope). **Not covered**: future roster eligibility, implementation timing or mutations, and an adopter trial. No tests run in this plan review.

## Response to plan review -- Codex (Terra), Plan author -- 2026-10-28

| Finding | Disposition |
|---|---|
| F1 | Accepted; C3 reconciles the conflicting claims in both copies, preserves the existing scheme and guard testing, and verifies installed wording. |


## Filename maintenance -- Codex (Coordination) -- 2026-10-28

Maintainer naming instruction, verbatim:

> "Your plan docs aren't following the right naming convention. See the archive. Can you check if the template specifies this? If not, please modify it and the other templates (And shipped copies) to specify the date as part of the naming."

The filename now uses its original Opened date. Its document-owned evidence
folder, where present, uses the same dated stem and archives with the plan.
This is a path migration, not a scope or lifecycle change. Historical review
and evidence citations retain the paths valid at their named commits; current
link destinations and operative targets use the dated paths.

## Pending scope request -- Codex (Coordination, Terra) -- 2026-10-28

The refreshed classification at `fd1c820e` retains protection for
`bootstrap/tests/test_board_json_contract.py`. The plan's protected-file refusal
therefore prevents implementing the pilot as written; the narrower trust
boundary itself is still uninstalled.

**Requested scope delta, not authorized:** separately review relocation of only
`TestRecordFactsComeFromWhereTheFileSits::test_all_record_values_and_absent_vs_blank_and_headerless_files`
and `TestOutputIsDeterministic::test_archives_unique_path_key_and_deterministic_ascii_json`,
keeping their class/method names, to the proposed ordinary file below; then allow
this pilot to use that path after all eligibility and transition gates are met.
Keep existing protected helpers and security cases in the original file.

Proposed path: `bootstrap/tests/test_board_json_values.py`.

The exact witnesses, retained helpers, alternatives and assurance costs are in
`dev/plans/2026-10-28-test-trust-boundary/c1b-refresh-classification-evidence.json`.
This adds preparatory extraction, dependency/fault evidence, ordinary and Security
reads, and the applicable protected-node transition and Maintainer ceremony.
It removes no accepted pilot property or testing-module update. Alternatively,
keep the pilot waiting; a protected-lane pilot would require explicit acceptance
of the changed maintenance outcome. No extraction, substitution or waiver is
made here. The consolidated choice is in
`dev/strategy/2026-10-28-codex-v06-decision-master.md`.

## Maintainer pilot-file allowance -- Codex (Implementation, Luna) -- 2026-10-29

Maintainer clarification in chat, relayed by Codex:

> “Again, no need to treat a file as protected in that sense.”

This authorizes proceeding with the original two-node pilot in
`bootstrap/tests/test_board_json_contract.py` without the trust-inventory
protected-file eligibility, additional review, or baseline checks. It
supersedes the pending extraction/path request above and the pilot-blocking
eligibility sentence in the test-trust-boundary plan. Keep both methods in
this file, preserve their behavior and fault detection, run the functional
checks in Verification, and obtain normal plan and code reviews. No pre-edit
family run or matched timing baseline is required. This allowance is limited
to this pilot and changes no other trust-boundary work.

## C1 inventory -- Codex (Implementation, Luna) -- 2026-10-29

**Source snapshot**: `fb7e8751` (Maintainer pilot allowance committed).

The first named test builds complete, blank-field and headerless artifacts
through `_write`, invokes the real `board.main` JSON entry point through
`_run_json`, compares the complete schema-1 record, distinguishes absent from
blank values, and confirms that plain output omits headerless artifacts. Its
failure witnesses include forged or late fields, title/in-brief substitution,
blank-to-absent coercion, dropped JSON records and accidental plain-board rows.

The second named test builds equal live/archive stems under two fresh roots and
checks archive inclusion, distinct path keys, same-root repeatability,
cross-root byte equality, ASCII-only sorted-key serialization, and the empty
root schema. Its failure witnesses include path collision, unstable ordering or
serialization, non-ASCII bytes, root-dependent output and omitted empty schema.

Both test nodes and all listed assertions remain. The only candidate cleanup is
the repeated public-entry invocation and capture sequence inside the second
test; a local helper can shorten that sequence without hiding fixture data or
changing shared helpers. No pre-edit test-family run or timing baseline was
made, as authorized above. No test property is proposed for removal.

## Implementation verification -- Codex (Implementation, Luna) -- 2026-10-29

**Boundary B mode**: wide
**Certified by**: pending
**Implementation verified at**: `70db63fd10cfa115a7053f4d1d5726968bed59d1`
**Tested commit**: `70db63fd10cfa115a7053f4d1d5726968bed59d1`
**Reviewed range**: `8b851656..70db63fd`
**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` -- Python 3.13.13
**Pre-run state**: clean detached worktree at the tested commit.
**Post-run state**: same commit; clean worktree.

The `test_board_json_contract.py` owning family passed **25 tests in 1.69 s**,
including both named pilot nodes and their real `tools/board.py` entry paths.
The mapped `test_practice_modules.py`, `test_doc_governance.py`,
`test_presets.py`, and `test_profiles_smoke.py` families passed **85 tests in
0.75 s**. No skips, xfails or xpasses were reported.

The actual CLI install of `bootstrap/profiles/high-rigor-legacy.yml` exited 0
and produced 101 files, including `dev/modules/testing-discipline.md`. That
installed file compared byte-identically with the changed shipped template and
contained the new behavior/fault, consolidation, fresh-state, and scope/runtime
guidance; the previous tier-alone and no-test-craft claims were absent. The
install target was fresh and outside the source worktree.

**Gates**: claim checks passed for both module copies and this plan; full
`link_check.py` passed across 189 Markdown files (84 external links were not
probed); `check_cairn.py` passed on the changed template and plan; neutrality
reported zero failures and 43 informational entries; redundancy reported zero
failures. A separate whole-tree `check_cairn.py` invocation found one
unrelated `imperative-override` finding at
`dev/proposals/2026-10-29-codex-dispatcher-content-scan.md:100`; it is outside
this reviewed range. No synced snippet block changed.

**Coverage / omissions**: the two properties and fault sets are mapped above;
all named tests and assertion behavior remain. No source schema, board command,
shared test helper, or product code changed. The only test change centralizes
the repeated command/output capture; all three return-code assertions still
run. No pre-edit family or matched timing baseline was run under the
Maintainer's allowance. No full suite, certifying run, mutation ledger or
adopter trial was run; no install timing was separately measured. Normal code
review remains due.

## Code review -- Codex (GPT-6), independent reviewer -- 2026-10-29

Reviewed commit: f44c287a31480435973b8b2a0e5c1c74186aa6c8
Target: 8b851656..70db63fd and verification at 930384b4
Prior findings: none

**Foundations**

1. **Does it do what it claims?** The local capture helper preserves the three entry-point calls and return checks, and the module copies match; the verification record is incomplete. -- `bootstrap/tests/test_board_json_contract.py`; `dev/modules/testing-discipline.md`; F1 below.
2. **Best alternative.** Retain the small helper and module wording, and supply the missing evidence rather than repeat unrelated checks. -- plan C2 and Verification.
3. **What would show it wrong.** A failed named behavior, changed capture semantics or incorrect installed content would undermine the claim. -- falsification ledger below.

**F1 — Blocking: complete the change-verification record.** The plan requires commands, outcomes, timing and changed setup and assertion counts. The record names families and summaries but does not give the actual commands or elapsed times for the install and gates, nor the changed setup and assertion counts. Add those facts from the run; where unavailable, repeat the affected checks on a clean final commit and record the results. -- plan C2, Verification and Implementation verification.

**Bounding**: WIDER RUN REQUIRED -- supply the missing change-specific evidence above; this does not require a full suite.

**Falsification ledger**

- Named board nodes: independent run under Python 3.13.13 in a fresh archive of f44c287a, `python -m pytest bootstrap/tests/test_board_json_contract.py -k 'all_record_values_and_absent_vs_blank_and_headerless_files or archives_unique_path_key_and_deterministic_ascii_json' -q`: 2 passed, 23 deselected.
- Capture helper: compared 70db63fd with its parent; each invocation still asserts the return code and immediately consumes captured output. No behavioral difference found by inspection.
- Installation: inspected `bootstrap/_scaffold/config.py` and mapped owners; the recorded install compares the installed module to the shipped template. The two committed module copies have identical changes.

**Covered**: named behavior, capture ordering, installed module route, verification record and review range. **Not covered**: mutations, an adopter trial, or a full suite. A detached worktree could not be created because the repository metadata is read-only; the targeted run used an archive and did not mutate it.

## Response to code review -- Codex (Implementation, Luna) -- 2026-10-29

| Finding | Disposition |
|---|---|
| F1 | Accepted. The original run summary omitted literal commands and per-command elapsed times, and did not quantify setup/assertion changes. I repeated the mapped test families, install and gates in a clean checkout of the tested implementation commit; the addendum records those commands and results. |

## Implementation verification addendum -- Codex (Implementation, Luna) -- 2026-10-29

This addendum completes the evidence for implementation commit
`70db63fd10cfa115a7053f4d1d5726968bed59d1`. It was rechecked in a clean local
clone detached at that commit, with `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(Python 3.13.13). The checkout was clean before and after. All reported elapsed
times are `/usr/bin/time -p` real seconds. No skips, xfails or xpasses occurred.

| Command | Result | Real time |
|---|---|---:|
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_board_json_contract.py -q` | 25 passed | 1.61 s |
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_practice_modules.py bootstrap/tests/test_doc_governance.py bootstrap/tests/test_presets.py bootstrap/tests/test_profiles_smoke.py -q` | 85 passed | 0.91 s |
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 bootstrap/scaffold.py --config bootstrap/profiles/high-rigor-legacy.yml --target /private/tmp/cairn-install-target.D8T1e9` | exit 0; 101 files installed; installed testing module byte-identical to `templates/modules/team-gated/testing-discipline.md` | 0.28 s |
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 scripts/claim_check.py templates/modules/team-gated/testing-discipline.md` | passed | 0.04 s |
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 scripts/claim_check.py dev/modules/testing-discipline.md` | passed | 0.03 s |
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 scripts/claim_check.py dev/plans/2026-10-28-ordinary-test-maintenance.md` | passed | 0.03 s |
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 scripts/link_check.py` | passed; 189 Markdown files; 84 external links not probed | 0.21 s |
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py templates/modules/team-gated/testing-discipline.md dev/plans/2026-10-28-ordinary-test-maintenance.md` | passed; 2 files | 0.08 s |
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 scripts/quality_gate.py --sub neutrality` | 0 failures, 43 informational entries | 0.91 s |
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 scripts/quality_gate.py --sub redundancy` | 0 failures, 0 informational entries | 0.34 s |

The first install attempt,
`/Users/kendal30/conda_envs/lhm/bin/python3.13 bootstrap/scaffold.py --config bootstrap/profiles/high-rigor-legacy.yml --target /private/tmp/cairn-install-target.tdkZ7P`,
exited 2 because that temporary target path did not exist. Creating an empty
temporary directory and rerunning the listed command succeeded. The successful install contained the updated
behavior/fault, consolidation, fresh-state and scope/runtime guidance; the
installed wording matched the shipped template byte for byte.

For the two named methods, AST counts before -> after were: `_write` setup
calls **3 -> 3** in each method; `assert` statements **11 -> 11** in the
record-values method and **13 -> 11** in the deterministic-output method. The
two fewer assertion statements are the return-code checks moved into the local
helper; that helper runs three times, so all **3** return-code checks still
execute. The deterministic method's three `board.main` calls likewise remain
three helper invocations; no test data setup, fixture, named test, or behavior
assertion was removed. No pre-edit test-family timing baseline was run, as
authorized by the Maintainer's allowance, and no before/after runtime claim is
made. The mapped test families provide the named-node and module-owner counts
above; no full suite, certifying run, mutation ledger, or adopter trial was run.

The scoped evidence resolves F1. This addendum does not change the implementation
bytes or claim full-tree certification.

## Code-review resolution -- Codex (Implementation, Luna) -- 2026-10-29

Maintainer-relayed independent-review confirmation:

> “Independent reviewer confirms response 32375254 resolves F1, no implementation changes and lifecycle no clearing round.”

No implementation, test, executable-template or fixture bytes changed after the
reviewed implementation commit. The review's requested verification was added
in `32375254`; the independent reviewer confirmed F1 is resolved. No second
code-review pass is due. The plan is ready to archive.
