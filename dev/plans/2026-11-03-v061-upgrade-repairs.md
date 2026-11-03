# Plan: v0.6.1 adopter upgrade repairs

**Source proposal**: dev/proposals/archive/2026-11-03-codex-v061-upgrade-repairs.md
**Author**: Codex (inherited runtime model; identifier unavailable)
**Status**: awaiting-code-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-03
**In brief**: Repair changelog ownership, Windows upgrades and stale citations, then prepare v0.6.1 without performing the Maintainer's trust or publication steps.

## Source proposal

Decision `184dd877` accepts the complete grouped repair contract and review
clarifications. Changelog content becomes project-owned living state while
apparatus integrity, collision review and path refusals remain. No new command,
service or recurring operator step is introduced.

## Scope

Change the existing lockfile policy and upgrade engine, owning tests, shipped
sources with stale governing references and their self-hosted copies. Prepare
`CITATION.cff`, README version text and a separate patch changelog section.
No engine redesign, new dependency, global encoding switch or trust-record edits.

**Reuse:** searches for `_LIVING_STATE_DSTS`, `_record_fork_entry`,
`relative_to`, `_display_name` and citation readers found existing policy,
record builders, report display and documentation-test homes. Extend those;
do not introduce another registry, parser framework or release runner.

### Documentation / doctrine surface

Describe ownership/migration in `bootstrap/UPGRADE.md` and the changelog
template. Repair stale section citations in shipped sources, self-hosted
copies and directly corresponding methodology; do not resurrect removed rules.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Changelog living-state policy and record migration | Both plan reviews folded | Existing policy/record paths plus regressions |
| C2 | Windows filesystem comparisons and report display | Same review gate; separate hostile-name controls | POSIX-rendered filesystem keys, encoding-safe reports, tests |
| C3 | Governing-reference repair and regression inventory | Same review gate | Current citations, aligned twins and falsifiable doc test |
| C4 | Prior-release rehearsal and patch preparation | C1-C3 implemented; code and Security Reviews precede final Boundary B | Version/notes, migration evidence, outstanding-platform report |
| C5 | Native Windows evidence and trust/release completion | MAINTAINER-ONLY for host access, baseline/anchor correction, signing, tagging and publication | Applicable Windows result, prescribed trust correction and release evidence |

C1-C3 may share one implementation commit and fixture preparation. No extra
review between chunks. C5 is not authorized by the Decision; stop at its fence.

## Acceptance criteria

**C1.** Only root `CHANGELOG.md` joins the authoritative exemption set. Fresh
install, unchanged carried records, added records and collision adoption emit
the flag; scoped finalize migrates old records too. Independently constructed
unflagged fixtures become editable without recurring finalize. Existing history,
merge ancestors and repeat upgrade survive. Script edits and forged exemptions
still fail integrity. No change to verification policy for any other path.

**C2.** Genuine nested Windows filesystem paths compare to canonical manifest
keys, including discovery outputs. Backslash/traversal metadata, POSIX
literal-backslash stage names, missing/extra files and link escapes still
refuse. CP1252 label and filename-display cases succeed independently of UTF-8
content round-tripping; display escaping never changes actual file names.
Native Windows stage/apply remains required before declaring #44 closed.

**C3.** Inventory shipped sources from the install mappings and check explicit
governing-section citations against actual emitted sections. Include the
session, stem, plan and rules references; fix corresponding live twins.
A broken-heading mutation goes red through the same test. Keep genuine
slot-target metadata distinct from section references. Existing link/content
checks pass; no scanner opt-out or recreated doctrine.

**C4.** A disposable project installed from actual `v0.6.0` upgrades through
the patch CLI, retaining committed custom history and other local edits;
another changelog edit passes integrity while script mutation fails. Repeat
upgrade is safe. Version is 0.6.1 with preparation date, not a claim of release.
The patch notes contain only patch outcomes; released v0.6.0 history is
unchanged and v0.7 deliberation stays Unreleased. Reviews and wide Boundary B
record all non-passes without waivers.

**C5.** Native Windows public stage/apply and encoding evidence is recorded.
Maintainer performs any prescribed trust corrections and release checks on
reviewed bytes. Do not close issues, archive this plan, sign, tag, push or
publish before applicable evidence and authority exist.

Security preflight S1/S4/S5 are unchanged from the proposal. S2 mutations occur
in owning tests: script/exemption, stage corruption and stale-heading controls.
S3 public paths are `bootstrap/scaffold.py` install and upgrade
`--stage`, `--apply`, `--adopt-collisions` and scoped `--finalize CHANGELOG.md`,
followed by `bootstrap/verify_integrity.py --target` on each disposable target.
The plan record binds filled-in arguments and input trees to results.
No scientific assumption or result is touched.

## Scope delta

Preserved: all accepted outcomes, including native Windows and release/trust
evidence. Outstanding fences are not deferrals or authority to waive checks.

## Verification

Canonical Python: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13).
Boundary A uses `tools/test_tiers.py for` on the actual changed paths; retain
the selected union in batches of at most 40 files, with no broad-run override.
The initial source mapping selects 86 test files; re-derive after edits.
Principal homes: upgrade, module-addition, integrity, lockfile,
documentation-plan, session and stem tests. Run the union once after grouped
edits, not per chunk. Run scoped claim/link/content checks and
`scripts/quality_gate.py --sub neutrality --sub redundancy` for prose.

Boundary C is independent usual code review plus separate Security Review,
using tight falsification probes, not suites. Then wide Boundary B on a clean
committed copy covers the selected union, mapped integrations, twin fidelity,
real prior-tag rehearsal and relevant trust checks. Record SHA/range, clean
states, interpreter, commands, counts, elapsed time, token uncertainty and
omissions. Unmet trust/platform checks keep the plan open at C5; no baseline
or frozen-file alteration by the implementer. Full certification stays at its
existing release/re-anchor trigger, not during iteration or review.

Before execution, C1 binds fixtures to existing CLI arguments: fresh install
uses `_install`; carried unflagged records run `upgrade --stage` then
`--apply`; an absent changelog record/file runs that same add path; occupied
history runs `--stage`, displayed `--adopt-collisions TRIPLE`, then stage/apply;
unflagged finalize uses `--finalize CHANGELOG.md`. Each command supplies
`--target TARGET --cairn-root ROOT`. Each ends with a history edit and integrity
check, then a script-edit refusal. C2 retains changed-lock, ancestor and
discovery-input refusals with unchanged destination/lock bytes. C3 asserts
nonempty extraction for each named family; deleting one mapped source or
disabling its extractor must fail the executing inventory test.

**Elapsed**: approximately 6 minutes. **Tokens**: unknown.

## Plan review -- Codex (inherited runtime; exact model identifier unavailable) -- 2026-11-03

**Foundations**

1. **Should this happen as framed?** Yes: C1-C5 retain migration, Windows, citation and patch outcomes, including outstanding platform/trust evidence -- Decision `184dd877`, plan Acceptance criteria.
2. **Best alternative.** Extend the existing exact-path policy, record builders and display helper; no additional mechanism is needed -- `bootstrap/_scaffold/lockfile.py:83`, `bootstrap/_scaffold/upgrade.py:1880`, `bootstrap/_scaffold/install.py:41`.
3. **What would show it wrong?** An unflagged carried record, accepted hostile stage or undetected stale citation would defeat C1-C3; the named owning tests provide extension points -- `bootstrap/tests/test_upgrade.py:1090`, `bootstrap/tests/test_upgrade_module_additions.py:792`, `bootstrap/tests/test_documentation_plan_module.py:135`.

```
Reviewed commit: 4001192bac05c507a1fbd8c360c7eab6fd212d69
Target: whole plan against accepted Decision 184dd877
Prior findings: none
Assurance path: high-assurance (accepted source)
```

**Tier**: Internal
**Obligation**: usual plan review
**Findings**: raised, non-blocking
**Verdict**: ACCEPT

**PR1 -- non-blocking.** Bind commands to cases before execution, not only
afterward in the results record. The accepted source Response promises exact
commands/input sets before execution; plan S3 currently lists operation names
and postpones filled arguments. Close by naming each independent old-record
fixture and its stage/apply, adoption or scoped-finalize command, followed by
the history-edit/integrity and script-tamper controls. Existing test fixtures
can supply these bindings; no new runner is needed.

**Elapsed**: approximately 6 minutes. **Tokens**: unknown.

**Covered:** committed migration branches, filesystem-versus-metadata
normalization, mapped citation sources, verification scope and C5 fences;
scratch manifest/selector probes and scoped prose checks passed under Python
3.13.13. The plan retains wide Boundary B after both implementation reviews.
**Not covered:** implementation, native Windows, prior-tag rehearsal, mutations,
full suite, trust ceremonies or the separate Security Review obligation.

## Plan review -- Codex Security Reviewer (inherited runtime; exact model identifier unavailable) -- 2026-11-03

**Foundations**

1. **Should this happen as framed?** Yes: C1-C5 preserve exact-path authority, migration branches, encoding/data separation and Maintainer fences -- `dev/plans/2026-11-03-v061-upgrade-repairs.md:52`.
2. **Best alternative.** Extend existing record builders and filesystem comparisons; no additional registry or normalization of untrusted metadata is needed -- `bootstrap/_scaffold/upgrade.py:1880`.
3. **What would show it wrong?** Apparatus exemptions, accepted hostile stages or missed citations defeat delivery -- `dev/proposals/archive/2026-11-03-codex-v061-upgrade-repairs.md`, Signals the change is wrong.

```
Reviewed commit: 4001192bac05c507a1fbd8c360c7eab6fd212d69
Target: whole plan; accepted source, AGENTS.md and current plan template
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Verdict**: ACCEPT
**Findings**: two non-blocking recommendations

**SPR1 -- Citation nonvacuity.** C3 requires a broken-heading mutation but does
not explicitly guard empty or incomplete extraction. Assert each named citation
family contributes references; demonstrate that omitting one mapped source or
disabling its extractor fails the same executing test. This prevents a green
result from checking nothing.

**SPR2 -- Stale-stage controls.** C2 names hostile metadata and exact-set
failures, but not stale-input refusals. Explicitly retain changed-lock,
ancestor and discovery-input controls alongside Windows-rendering success.
Close by mapping existing stale-stage tests and recording unchanged
destination/lock bytes after refusal, without converting saved metadata keys.

**Elapsed**: approximately 4 minutes active work. **Tokens**: unknown.

**Covered:** committed policy/migration paths, stage validation, encoding
boundaries, citation-test design, separate implementation Security Review,
wide Boundary B and AST/anchor/release fences.
**Not covered:** implementation, runtime probes, native Windows, prior-tag
rehearsal, suites, broad sweeps or release ceremonies.

## Implementation progress -- Codex -- 2026-11-03

C1-C4 changes are prepared but not committed. On a separate copy of
`37952558` plus the candidate tests, nine selected regression cases failed
against the unchanged source. On a fresh copy plus the complete candidate,
21 focused cases passed, 55 deselected, in 4.52 seconds under Python 3.13.13.
Individual Markdown claim checks, scoped prose checks and the existing
neutrality/redundancy gates passed. Released v0.6.0 and earlier changelog bytes
remain unchanged; session and stem twins match. No full suite ran.

The actual changed-path selector lists 90 test files. The committed-candidate
iteration run, prior-tag rehearsal, code/Security Reviews and Boundary B have
not run. A disposable actual-v0.6.0 checkout is prepared for the rehearsal.
Native Windows and trust/release completion remain owed.

### Frozen-file wording clarification requested

Verification's generic "no baseline or frozen-file alteration by the
implementer" conflicts with C1-C3's explicit tests and shipped-source edits.
The frozen-set intersection is exactly the two upgrade test files plus
`scripts/verify_stems.py` and its shipped twin. None is a trust record being
rewritten. The Maintainer is asked to allow these already-scoped edits while
keeping trust records and re-anchoring Maintainer-only. Until answered, none
of the implementation changes is committed. Proposed clarification removes
no accepted repair, test, review or ceremony safeguard.

**Elapsed**: approximately 12 minutes of implementation preparation.
**Tokens**: unknown.

## Maintainer clarification -- 2026-11-03

The Maintainer answered the chat question about the generic frozen-file
restriction conflicting with C1-C3's named source and test edits:

> Allow the already-scoped source/test edits; keep trust corrections Maintainer-only

This permits the accepted edits to the two upgrade test files and the
self-hosted/shipped stem-checker twins. Verification's generic prohibition
therefore applies to trust-record/control corrections, not those expressly
scoped source/test edits. No repair, check or review is removed. Baseline and
anchor correction, signing, tagging and publication remain Maintainer-only.

**Elapsed**: less than 1 minute. **Tokens**: unknown.

## Native Windows follow-through -- Codex -- 2026-11-03

The Maintainer authorized the native part of C5 in chat:

> Go ahead and validate using windows. UTM is open and I think the SSH is set to start up automatically

The existing Windows ARM64 Miniconda reports Python 3.13.17 and pytest 9.2.0,
with default CP1252 and UTF-8 mode off. A verified archive of `1fde38d3`
ran 47 selected cases: 29 passed, 18 failed in 16.92 seconds. This is not a
passing Windows result. The initial archive/setup hypothesis was wrong.

Fresh installation changed a verbatim tool from 96,614 bytes with no CRLFs to
98,835 bytes with 2,221 CRLFs; changing only those endings back recovered the
source exactly. The strict clean-install guard therefore refused the lockfile.
This exposes a pre-existing byte-fidelity defect that prevents C2/C4's native
install/upgrade outcomes; relaxing the hash comparison would be wrong.

Restore the existing byte contract in the current install, onboarding,
module-merge, three-way-merge and upgrade writers: generated text uses UTF-8/LF;
verbatim installation keeps the validated source bytes, including original
CRLFs. Guards, collision consent, metadata validation and strict comparisons
stay unchanged. Extend the existing install tests with LF/CRLF byte controls.
This is C2/C4 correctness follow-through, not a new mechanism or trust boundary.
One separate legacy-binding fixture also failed; its result remains open for
diagnosis. Rerun native evidence before claiming Windows completion.

**Elapsed**: approximately 5 minutes. **Tokens**: unknown.

## Plan response -- Codex (inherited runtime; identifier unavailable) -- 2026-11-03

Both required plan passes ACCEPT. PR1 is incorporated as fixture-to-command
bindings before execution in Verification. SPR1 adds named-family nonempty
controls and omitted-source/disabled-extractor failure checks there. SPR2
retains stale lock, ancestor and discovery-input refusals with unchanged-byte
assertions. These sharpen existing criteria without dropping an outcome or
adding a mechanism. The plan is ready to implement; C5 remains fenced.

**Elapsed**: approximately 2 minutes. **Tokens**: unknown.

## Implementation start -- Codex -- 2026-11-03

C1-C4 begin from the reviewed plan. C5 remains fenced. Runtime: canonical
Python 3.13.13. Group source changes before the selected iteration run; do not
alter pinned trust records to make an expected trust refusal disappear.

**Elapsed**: less than 1 minute. **Tokens**: unknown.

## Implementation log -- Codex -- 2026-11-03

**Source range:** `37952558..1273e3f777b7bd43f5c81bb8d73e2beddcce7fe9`.
C1-C4's code is implemented; native C5 access was delegated above. Trust and
release completion are still fenced. No new production command, function,
class or dependency was added. The environment reference requested in chat is
`dev/rules/development-environment.md`, committed in `b2994e5e`.

### Iteration evidence

All macOS figures below use `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
Python 3.13.13, in separate committed-source copies. The initial 26 changed
paths selected 90 files; sorted output was split 40/40/10. Commands were
`python -m pytest <selected files>`, without a full-suite override.

| Commit / check | Outcomes | Elapsed |
|---|---|---|
| `2b6411ff`, first 40 files | 1,114 passed, 15 failed, 8 skipped | 128.34 s |
| Same bytes, 14 local-socket failures retried with socket access | 14 passed | 6.51 s |
| `aa12762b`, corrected board assertion | 1 passed | 0.10 s |
| `aa12762b`, next 40 files | 2,833 passed, 1 stale citation assertion failed | 1,126.97 s |
| `aa12762b`, final 10 files | 693 passed | 117.13 s |
| `1fde38d3`, corrected citation and inventory controls | 4 passed | 0.55 s |

The two source-test corrections changed obsolete expected section names, not
asserted behavior. The eight skips require native Windows junctions.
These are successive checks, not a single clean run at one SHA.

Native follow-through changed install, merge and upgrade byte writers.
On clean `1273e3f7` copies, `tools/test_tiers.py for` those four source files
and `test_install_module.py`, `test_merge_module.py`, `test_upgrade.py` and
`test_git_interpreter_binding_portable.py` selected 62 files. Alternating
sorted rows formed two 31-file lists, run with `python -m pytest -q
--tb=short --junitxml=<batch.xml> <list>`:

| Batch | Outcomes | Elapsed |
|---|---|---|
| Odd rows | 1,788 passed | 389.85 s |
| Even rows | 2,007 passed, 2 failed, 8 skipped | 701.32 s |

Both copies remained clean at the same SHA. The two failures are
`test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package`
and `::test_ast_gate_passes_over_the_full_scaffold_module_set`: intentional
engine changes disagree with the unchanged trust baseline. They are unmet
checks, not passes or waivers. The complete range now selects 96 files; every
member occurred in the initial or follow-through mapping. This is Boundary A,
not the still-owed final wide Boundary B.

### Native and public-path evidence

Windows ARM64 used existing `C:\ProgramData\miniconda3\python.exe`, Python
3.13.17, pytest 9.2.0, Git 2.56.0.windows.4, CP1252 and UTF-8 mode off.
Both broad-run and release tokens were absent. The transferred `1273e3f7`
archive matched SHA-256
`f1104b5e42faacfc4cdf10b05a2ab7a04e96847b533b248887a678684e008a9a`.

`pytest` selected the living-state class; stage/apply, filesystem-key,
hostile-stage and console cases; five changelog-collision cases; two citation
controls; board and stewardship regressions; the entire portable binding and
merge-module files; and both exact install-byte controls: **55 passed in
45.39 s**. This includes the eight native junction cases skipped on macOS.
Earlier native results remain failures: `1fde38d3` had 29 passed/18 failed;
`43276e7b` had 44 passed/5 failed. The final run fixes rather than suppresses
those failures; no global encoding setting or new VM software was used.

The actual `v0.6.0` source `ecce3465` was rehearsed through the public CLI
against `1273e3f7` on macOS: install, committed history/overview edits, old
scoped finalize and integrity; new stage/apply with no review-only item;
later changelog edit/integrity; script mutation/refusal; repeat stage/apply
and integrity. All passed in 1.42 s. Exact historical UTF-8 bytes survived
alongside the new ownership paragraph. An initial fixture wrongly expected
the entire changelog, including upstream guidance, not to change; only that
fixture expectation was corrected. Native prior-tag installation was not run.

Individual claim checks and `check_cairn.py` passed for all 18 changed
Markdown files; ten external links were not probed. Neutrality/redundancy
passed. Session and stem pairs remain byte-identical. Released v0.6.0 history
is unchanged. No full-tree certification ran.

### Outstanding work and timing

`repin.py status` at `1273e3f7` reports 11 baseline symbols changed, two
known-new bodies rekeyed, six frozen files modified, none missing/new and
0/12 authority-closure files differing. The pre-existing NEW population is
not this patch's additions. No trust record was rewritten. C5 correction,
post-review wide Boundary B, certification, signing and publication remain
owed; issues stay open and the plan cannot archive yet.

Iteration exceeded the 30-second diagnostic. Per-file setup/call/teardown
totals over ten seconds are recorded on the existing suite-consolidation
board row, not treated as failures or omitted tests.
**Elapsed:** approximately 80 minutes including prior iteration, Windows
diagnosis and parallel independent reads. **Tokens:** unknown.
