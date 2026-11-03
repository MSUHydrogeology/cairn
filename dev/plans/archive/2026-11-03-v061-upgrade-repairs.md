# Plan: v0.6.1 adopter upgrade repairs

**Source proposal**: dev/proposals/archive/2026-11-03-codex-v061-upgrade-repairs.md
**Author**: Codex (inherited runtime model; identifier unavailable)
**Status**: archived
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

## Code review -- Codex (inherited runtime; exact model identifier unavailable) -- 2026-11-03

**Foundations**

1. **Should this happen as framed?** Yes: exact-root ownership, migration and byte preservation deliver C1-C4's source outcomes without relaxing guards -- `bootstrap/_scaffold/lockfile.py::_LIVING_STATE_DSTS`, `bootstrap/_scaffold/upgrade.py::_apply_upgrade`, `bootstrap/_scaffold/install.py::_install_one`.
2. **Best alternative.** Keep the existing policy, record builders and display helper; no additional mechanism is needed -- `bootstrap/_scaffold/upgrade.py::_record_fork_entry`, `bootstrap/_scaffold/install.py::_display_name`.
3. **What would show it wrong?** Lost history, converted verbatim bytes, corrupt stages or vacuous citation extraction. Independent probes challenged these; committed controls include `bootstrap/tests/test_install_module.py::test_install_one_verbatim_not_stripped` and `bootstrap/tests/test_documentation_plan_module.py::test_agents_citation_inventory_controls`.

```text
Reviewed commit: 1273e3f777b7bd43f5c81bb8d73e2beddcce7fe9
Target: 37952558..1273e3f7; implementation evidence ca2b6e0dca84070e8f3d65ffc286b36d92a3003b
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: usual code review
**Tier**: Internal
**Findings**: none
**Verdict**: ACCEPT -- code only.
**Bounding**: ACCEPTED -- challenged stage/cache bytes and citation nonvacuity;
the 96-file union covers mapped consumers, not completed final verification.

Independent Python 3.13.13 checks: nine latest-byte probes, two install
controls and the real merge control passed. Isolated verbatim, cache/apply,
fixture-read and merge-decoding mutations failed as intended; the latter uses
`bootstrap/tests/test_merge_module.py::test_three_way_merge_roundtrip_clean_and_needs_value`.
Earlier probes covered seven migration paths and hostile-name refusals.
A scratch import collected 34 unintended existing cases; corrected before
explicit selections. All passed; no certifying override was used.

The committed log records 3,795 passes across the final 62-file batches,
two unmet AST checks, eight macOS skips, native 55-pass evidence and the
prior-release rehearsal; none is relabeled final Boundary B.

**Elapsed**: unknown. **Tokens**: unknown.

**Covered**: committed source, preserved history/checks, fixture changes and
iteration evidence. **Not covered**: independent native/prior-tag reruns or
the separate Security Review. C5 trust correction, both AST checks, final
wide Boundary B and strict release certification/signing/publication remain
unmet; this pass grants no completion or waiver.

## Code review -- Codex Security Reviewer (inherited runtime; exact model identifier unavailable) -- 2026-11-03

**Foundations**

1. **Should this happen as framed?** Yes: history ownership stays exact-path; apparatus exemptions remain forbidden -- `bootstrap/_scaffold/lockfile.py::_LIVING_STATE_DSTS`, `bootstrap/verify_integrity.py::verify`.
2. **Best alternative.** Existing record builders and explicit byte/text serialization suffice without another mechanism -- `bootstrap/_scaffold/upgrade.py::_record_fork_entry`, `bootstrap/_scaffold/install.py::_install_one`.
3. **What would show it wrong?** Accepted hostile stages, converted bytes or vacuous citations; independent probes challenged these -- `bootstrap/tests/test_documentation_plan_module.py::test_agents_citation_inventory_controls`.

```text
Reviewed commit: 1273e3f777b7bd43f5c81bb8d73e2beddcce7fe9
Target: 37952558..1273e3f7; evidence ca2b6e0d; usual review 96f26e1d
Prior findings: draft UTF-8 merge-decoding finding, closed at 1273e3f7
Assurance path: high-assurance
```

**Obligation**: Security Review
**Tier**: Internal Security Review
**Findings**: no unresolved code defects
**Verdict**: ACCEPT -- code only.
**Bounding**: ACCEPTED -- challenged writer, metadata and exemption boundaries;
not final verification.

Separate-copy Python 3.13.13 probes: 29 passed in 3.83 seconds; two committed
controls passed in 0.06 seconds. Exact verbatim bytes, Unicode Git merge and
stage/apply survived; invalid UTF-8, link/traversal escapes, hostile metadata,
script exemptions and newline-only consent changes refused. Restored exact
collision bytes remained adoptable.

Two isolated mutations failed as intended: removing explicit decoding failed
`bootstrap/tests/test_merge_module.py::test_three_way_merge_roundtrip_clean_and_needs_value`;
normalizing verbatim reads failed
`bootstrap/tests/test_install_module.py::test_install_one_verbatim_not_stripped`.
Initial helper-class overcollection passed 51 cases; excluded from the
31-case scoped figure.

The implementation log records 55 native passes, not an independent rerun.

**Elapsed**: unknown. **Tokens**: unknown.

**Covered**: committed migration, filesystem/display separation, citation
controls, native writer fixes, fixture changes and implementation evidence.
**Not covered**: independent native/prior-tag reruns or certification. The log's
two AST failures remain unmet. Trust correction remains owed for the log's 11
baseline changes, two known-new rekeys and six frozen edits; 0/12 authority
records differ. C5 trust/release work and final wide Boundary B remain owed;
no waiver or release readiness is granted.

## Code review response -- Codex -- 2026-11-03

The usual pass `96f26e1d` and separate Security pass `58f3f563` both ACCEPT
the code and mapped scope, with no unresolved code finding. Their independent
byte, encoding, migration and hostile-input probes support the repairs.
No further clearing read is owed on unchanged source.

The plan remains implementing because C5 is unfinished, not because code
review is missing. The existing signed trust record is intact but does not
yet attest the patch. The Maintainer performs the prescribed AST/known-new
correction and gate re-anchor; final wide Boundary B and applicable release
certification still have to pass. Native Windows validation is complete;
archive, issue closure, signing, tagging and publication remain unperformed.
No accepted outcome or safeguard is removed.

**Elapsed**: approximately 2 minutes. **Tokens**: unknown.

## Documentation verification -- Codex -- 2026-11-03

On clean `7e3da296d76b96e83e0a19471704166344657c8c`, canonical Python
3.13.13 ran the 20-file selection from `tools/test_tiers.py for
dev/PLANNING.md dev/plans/2026-11-03-v061-upgrade-repairs.md`:
`python -m pytest -q --tb=short <selection>` -- **1,034 passed in 105.21 s**.
The copy stayed clean at the same commit. Claim/content/link checks passed;
external URLs were not probed. The three files over ten seconds are already
on the consolidation list. No full-suite override was used.

This is documentation iteration, not final wide Boundary B. Source bytes
remain those reviewed at `1273e3f7`. The no-clearing-round statement above
concerns code review; the existing ceremony's independent packet read and
reader-record commit remain required within C5.

**Elapsed**: 105.21 seconds test time. **Tokens**: unknown.

## Maintainer scope amendment -- 2026-11-03

The Maintainer directed in chat:

> Plans should not have Maintainer's trust/release step in them. That should be created as a separate PLANNING.md board item.

> A plan should not require Maintainer's intervention to complete.

**Scope delta:** trust/release completion moves out of this plan into the
separate v0.6.1 trust-and-release row in `dev/PLANNING.md`.
**Disposition:** defer that operational work to the named row, not abandon it.
C5's native Windows evidence is already delivered and remains evidence here.
The row owns AST/known-new correction, the independent ceremony packet read,
gate verification/re-anchor, certification, signing, publication and issue
closure. Those operations keep their existing authority and checks.

This supersedes C4/C5 and later records only where they make those operations
a prerequisite for completing this implementation plan. The loss is an
installed-trust/release claim in this plan; that claim must instead wait for
the separate operation's evidence. The two stale-baseline failures remain
failures, bound to the reviewed source and tracked with that obligation.
No failing code behavior, missing functional check, review or accepted repair
outcome is transferred. Final agent-owned wide Boundary B remains owed here.
Finishing this plan will not authorize release or claim a clean trust record.

**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

## Implementation verification -- Codex -- 2026-11-03

**Boundary B mode**: wide. Owning upgrade/install/merge, integrity, session,
shipped-doctrine, manifest/AST and re-anchor families include real CLI and
integration consumers; narrower bounds would miss shared install contracts.
**Tested commit**: `66f61097bbe809a20b76e28f772fbdc07a611647`.
**Reviewed range**: `37952558..66f61097`.
**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
Python 3.13.13, macOS.
**Pre-run state** and **Post-run state**: clean copies, unchanged tested SHA.
Only deliberation records changed afterward; implementation, templates,
descriptive documentation and environment-note bytes remain identical.

`tools/test_tiers.py for` every changed path in the range selected 97 files.
Sorted rows were partitioned by index modulo three into 33/32/32 files.
Each copy ran `python -m pytest -q --tb=short --junitxml=<batch.xml>
<selection>`, without a broad-run override. Nothing was deselected.

| Command / selection | Exit | Outcomes | Elapsed | Tokens |
|---|---|---|---|---|
| Pytest rows 1/4/7/... | 0 | 2,132 passed | 731.72 s | unknown |
| Pytest rows 2/5/8/... | 1 | 1,035 passed, 2 failed | 146.22 s | unknown |
| Pytest rows 3/6/9/...; corrected attached-copy setup | 0 | 1,605 passed, 8 skipped | 288.82 s | unknown |
| Actual v0.6.0 CLI upgrade rehearsal | 0 | history/overview, later notes, script refusal and repeat upgrade passed | 1.42 s | unknown |
| `scripts/check_cairn.py` | 0 | 193 Markdown files; no issues | unknown | unknown |
| `scripts/sync_doc_snippets.py --check` | 0 | 536 documents; no drift | unknown | unknown |
| `scripts/quality_gate.py --sub neutrality --sub redundancy` | 0 | no failures; existing informational notices | unknown | unknown |

The selected final runs therefore record **4,772 passed, two failed and eight
skipped**, not a clean whole-tree certification. An initial third batch had
1,604 passes, one failure and eight skips in 288.02 s: its release fixture
clones the test source and requires an attached branch. My detached copy
violated that setup assumption. Attaching the same clean commit fixed the
single case (one passed in 31.53 s), then the complete third batch passed as
shown. No source/test assertion changed and the earlier failure is retained.

**Non-pass disposition:** both failures are the two real-tree AST checks named
in the implementation log. The Maintainer's amendment `10d98e18` assigns their
pending baseline installation to the separate trust/release operation; they
remain failed, and release remains blocked. They are not a generic exception
for agent-owned checks. All eight skips are native Windows junction cases;
the recorded 55-pass Windows run exercised those eight successfully under
Python 3.13.17. No code defect or applicable functional check is outstanding.

**Plan-specific acceptance commands:** the real `v0.6.0` tree `ecce3465`
installed and finalized custom history/overview, then the tested patch ran
stage/apply, integrity after ordinary changelog edits, script-tamper refusal,
and repeat stage/apply/integrity. Historical UTF-8 bytes survived exactly;
only the intended upstream guidance merged. The existing iteration record
supplies the independent old-record, hostile-stage and citation mutations;
both code reviews accepted them. No scientific check applies.

**Known omissions:** full certification, strict release security, live gate
verification/re-anchor, actual trust correction, signing and publication were
not performed. External URLs were not probed. The separate board operation
retains these obligations and the existing release dispositions; archiving
this implementation attests none of them. The v0.7 policy proposal was moved
off this branch without implementing its general doctrine/template changes.

The iteration/integration timing diagnostics were exceeded. The existing
consolidation row records slow files; the additional wide-run file over ten
seconds is `test_ceremony_review_report.py` (22.61 s, summed JUnit times).
**Elapsed**: approximately 17 minutes including setup diagnosis/retry.
**Tokens**: unknown.

## Dispositions -- Codex -- 2026-11-03

Dispositions: accept -- C1-C4 repair outcomes, native Windows evidence and
both independent code reviews are complete; lasting behavior is in the
existing engine, upgrade guidance, changelog template, citation sources and
their tests. No new policy implementation is claimed.

Dispositions: defer -- only the human-run trust/release operation, at the
Maintainer's verbatim direction recorded in `10d98e18`, to the separately
named v0.6.1 board row. The reason is ownership outside implementation, not
test cost or unfinished code. Preserve both failed AST results and required
operational checks there. Issues #43-#45 stay open until release.

## Archive -- Codex -- 2026-11-03

Implementation, both independent code reviews, native Windows evidence and
final agent-owned wide verification are complete under the Maintainer's
scope amendment `10d98e18`. Lasting behavior and guidance live in the engine,
owning tests, upgrade documentation and shipped citation sources. The local
environment reference is in `dev/rules/development-environment.md`.

The separate v0.6.1 trust/release board item retains the two failed AST
results, prescribed corrections and ceremony, certification, publication and
issue closure. This archive claims neither clean installed trust nor a
released patch. No human operation is a remaining completion step here.

**Elapsed**: approximately 1 minute. **Tokens**: unknown.
