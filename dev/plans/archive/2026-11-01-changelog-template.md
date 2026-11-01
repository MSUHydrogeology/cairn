# Plan: Ship a changelog template

**Source proposal**: dev/proposals/archive/2026-11-01-codex-changelog-template.md
**Status**: archived
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Give adopters a usable changelog while preserving their existing history during installation and upgrades.

## Source proposal

The Maintainer accepted the heavy proposal at `7f8e3a14`: install a root changelog for every profile, explain its format and existing-history choices, and preserve existing collision and overwrite safeguards.

## Scope

Add `templates/core/CHANGELOG.md` and its core mapping in `bootstrap/_scaffold/config.py`; update the shipped `templates/core/AGENTS.md` reference, `bootstrap/UPGRADE.md` and any install descriptions needed for accuracy. The published install manifest must include the mapping. Add focused tests in existing bootstrap test homes. This touches adopter-facing governing guidance and the install contract; no new doctrine is proposed.

**Reuse.** Searched `_CORE_MAPPINGS`, `bootstrap/tests/test_scaffold.py` and `bootstrap/tests/test_upgrade_module_additions.py`: core mappings already deliver across profiles, while existing install skip, collision staging and adoption handle history. Extend their behavior tests rather than introduce a second workflow or new machinery.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Add template, mapping, guidance and focused behavior tests | Plan reviews and response | Template and existing-workflow coverage |
| C2 | Review implementation, resolve findings, then run final integration | Ordinary code review and separate Security Review | Reviewed change and verification record |

## Acceptance criteria

**C1.** Every profile installs the root template on an empty target and the published manifest lists its mapping. Its linked Plain Language marker, Unreleased/Major/Minor headings, ordered entry types and concise use instructions match the Decision. Shipped AGENTS points to those instructions. Normal install preserves existing history byte-for-byte; force retains its explicit overwrite meaning.

Actual upgrade entry points block an unlocked new-core collision and preserve its bytes; staged copies and the displayed command permit adoption from the target tree without `--to`, recording the correct fork and base. Guidance in the template and upgrade guide explains keeping history unchanged, optionally adapting and re-staging it, or saving it separately before removing the destination and installing fresh. A different-source ownership conflict and unsafe or non-regular paths require manual resolution or refusal. Tests check bytes and relevant lock/base records and exercise keep and fresh-start paths.

**C2.** Ordinary and Security code reviews address the implementation. Collision-bypass and replacement mutations make focused behavior tests fail; report outcomes and omissions. The final wide integration selection passes or every non-pass is dispositioned before closure.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A: run `python tools/test_tiers.py for <changed paths>` and its selected tests, plus claim, link, snippet and neutrality gates for prose. Search changed files for readers and byte pins. Extend existing entry-point tests, including `test_scaffold.py` install skip/force cases and `test_upgrade_module_additions.py::test_adopt_collisions_records_fork_and_unblocks`, `::test_duplicate_destination_ownership_is_refused`, and `::test_adopt_collisions_refuses_to_ref`, with specific changelog scenarios where coverage is missing. Check template content, profile and published manifest membership, staged guidance and the actual command. Test collision-bypass and replacement mutations in separate copies against independent history bytes.

Boundary C: an independent reviewer reads the committed implementation and iteration evidence and runs targeted falsification checks, not a suite; a separate Security Review is also required. Return substantive review fixes to the same reviewer for a targeted look.

Boundary B: after reviews, use a clean unchanged final commit under canonical Python 3.13.x. Run the mapped iteration list for the reviewed range, named integration/workflow tests, standing prose gates, and plan-specific behavior and mutation checks. Use **wide** for the install contract, covering its owning test families, public install and upgrade paths and their consumers. Record SHA and range, interpreter, clean pre/post state, commands, counts, elapsed time, tokens or unknown, non-pass dispositions and omissions in the required dated implementation verification section. Record timing misses and list test files over 10 seconds as required. Neither full-tree certification nor re-anchor is authorized here.

## Plan review -- Codex GPT-6 -- 2026-11-01

Reviewed commit: `844cd4e1`; target: whole plan; prior findings: none.
Tier: Internal; Obligation: ordinary plan review; verdict: **PROCEED**; findings: none.
Elapsed: approximately 3 minutes; tokens: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. The accepted proposal requires an installed template and preservation of existing history; C1 covers install, upgrade collision, eligible adoption and the three practical choices. It also requires the linked marker, headings and entry-type order from the Decision. The plan reuses existing workflows rather than adding a ledger.
2. **Best alternative.** A separate example avoids a root collision but loses the requested ready-to-use root file and adds a copying step; the proposal's collision workflow preserves the existing upgrade contract.
3. **What would show it wrong?** An entry-point test showing lost history, unusable staged adoption, incorrect fork/base records, a missing profile or misleading guidance. C1 and Boundary A require those cases and independent-byte mutations; the named upgrade tests already exercise adoption, ownership and the `--to` refusal.

**Coverage:** Read the committed plan and accepted proposal, current changelog format, upgrade guidance and named test locations. Did not execute tests or mutations, inspect every upgrade branch or assess security in depth; a separate Security Review remains required.

## Plan review -- Codex GPT-6 Security Review -- 2026-11-01

Reviewed commit: `ba63765b`; target: whole plan; prior Security findings: none.
Tier: Internal Security Review; Obligation: Internal Security Review; verdict: **PROCEED**; findings: none.
Elapsed: approximately 3 minutes; tokens: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. C1 preserves normal-install bytes, distinguishes eligible collisions from another source's ownership, and requires correct fork/base records. This delivers the accepted heavy proposal without widening overwrite authority. The committed upgrade new-core loop blocks occupied destinations; collision adoption revalidates eligibility and both authorized hashes before recording a fork (`bootstrap/_scaffold/upgrade.py`).
2. **Best alternative.** Reuse those controls and add focused changelog cases, as Boundary A proposes. A separate example avoids collision but loses the accepted root file. New adoption machinery adds burden without improving this outcome; existing tests already exercise preservation, ownership refusal and adoption without `--to` (`bootstrap/tests/test_upgrade_module_additions.py`).
3. **What would show it wrong?** Actual entry-point tests permitting silent replacement, adoption of another source's destination, unsafe writes, incorrect ancestry or unusable staged commands. C1 and Boundary A require these behaviors, independent history bytes and collision-bypass/replacement mutations; C2 retains separate implementation Security Review. Wide mapped integration covers the install contract while explicitly excluding certification and re-anchor.

**Coverage:** Read the committed plan and accepted proposal, current install skip/force interface, new-core collision classification, adoption authorization/preflight, named preservation and ownership tests, and protected-surface guidance. No new process or ledger is proposed. Did not run tests or mutations, inspect every apply branch, or establish race resistance; implementation evidence and separate code Security Review remain owed.

## Implementation iteration -- Codex GPT-6 -- 2026-11-01

**Commit checked:** `d45ea20ee6f32a541af618e0701a41762236da51`, in a clean copy.
**Interpreter:** `/Users/kendal30/conda_envs/miniforge3/bin/python`, Python 3.12.9.
**Targeted command:** six changelog install and upgrade nodes in
`test_scaffold.py` and `test_upgrade_module_additions.py`; **6 passed** in
2.44 seconds. This covers template and manifest membership, normal install
byte preservation, explicit `--force`, staged `.ours`/`.theirs` review, the
printed adoption digest, fork and base records, fresh start with saved history,
another-source ownership, and linked-path refusal.
**Prose gates:** `claim_check.py` passed for the template, shipped AGENTS and
upgrade guide; `link_check.py` passed on those three files; `sync_doc_snippets.py
--check` reported no drift; `quality_gate.py --sub neutrality` reported
`fail=0`, `info=43`.
**Mapped selection:** `test_tiers.py for` selected 40 test files and omitted
45 AGENTS readers under its guard. An initial run yielded after partial
progress and has no final result; no pass is claimed. Per Maintainer direction,
the complete mapped selection is deferred to final Boundary B on Python 3.13.x.
**Earlier targeted disposition:** the first six-node run had four passes and
two assertion failures in the new tests. The test wording and conflict selection
were corrected in `d45ea20e`; the six-node rerun above passed. Tokens: unknown.
**Mutation checks:** separate clean copies of `d45ea20e` were mutated and
tested through the real entry points. Making `_install_one` bypass the existing-
file skip made `test_normal_install_preserves_existing_changelog_bytes` fail as
expected (0.58 seconds). Removing the unlocked-destination clause from the
new-core classifier made `test_new_core_changelog_collision_can_be_kept_as_a_fork`
fail as expected (0.70 seconds). Both controls passed on unmutated bytes in the
six-node run; both mutants were killed. Tokens: unknown.
This is iteration evidence only; ordinary code review and Security Review remain
owed before Boundary B.

## Implementation recheck -- Codex GPT-6 -- 2026-11-01

**Review fix:** ordinary code review `7a2de064` found that adapting history
must be followed by a fresh stage because the adoption digest is bound to the
bytes staged earlier. Both guides now state the order. The new entry-point
test proves that the earlier authorization is refused after editing, a new
stage exposes the changed bytes, and the newly printed authorization adopts
them.
**Commit checked:** `89e390341e24e5d5770e538a720ca68da9958657`, clean copy.
**Interpreter:** `/Users/kendal30/conda_envs/miniforge3/bin/python`, Python 3.12.9.
**Targeted tests:** seven changelog install/upgrade nodes passed in 3.78 seconds,
including the new edit, re-stage and adopt sequence. The first run on the
corrected code passed all seven.
**Prose gates:** `claim_check.py` passed on the template, shipped AGENTS and
upgrade guide; `link_check.py` scanned all three without issues;
`sync_doc_snippets.py --check` found no drift; `quality_gate.py --sub neutrality`
reported `fail=0`, `info=75`.
**Mutation checks:** in separate clean copies of this commit, bypassing the
normal-install skip made `test_normal_install_preserves_existing_changelog_bytes`
fail (0.47 seconds), and bypassing new-core collision detection made
`test_new_core_changelog_collision_can_be_kept_as_a_fork` fail (0.76 seconds).
Both mutants were killed; the unmutated seven-node controls passed. Tokens:
unknown. The initial mapped selection still has no final result; complete mapped
tests remain for wide Boundary B. A targeted ordinary review re-look and
Security Review remain owed before Boundary B.

## Author response -- Codex GPT-6 -- 2026-11-01

Both the ordinary plan review and Security Review recommend proceeding with no findings. The accepted scope and verification remain unchanged.

Elapsed: approximately 1 minute; tokens: unknown.

## Code review -- Codex GPT-6 -- 2026-11-01

Reviewed: implementation `d45ea20e` and evidence `eaf4144a`; Tier: Internal; verdict: **REVISE**. Elapsed: approximately 5 minutes; tokens: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. The core mapping supplies the template, while existing install and collision mechanisms preserve history; the two targeted keep and fresh-start entry-point tests passed on a separate committed copy (Python 3.12.9, 2 passed in 1.49 seconds).
2. **Best alternative.** Reuse the existing collision workflow, as implemented. A separate example avoids a collision but loses the accepted ready-to-use root file.
3. **What would show it wrong?** A user losing history, a displayed command refusing reviewed adapted bytes, incorrect fork ancestry, or a missing profile or manifest entry. The implementation tests cover several of these; the guidance gap below leaves the adapted path unclear.

**Blocking finding — adaptation must be re-staged before adoption.** C1 requires guidance for optionally adapting and re-staging history. Both `templates/core/CHANGELOG.md` and `bootstrap/UPGRADE.md` say to review changed bytes before adopting but do not say to run `upgrade --stage` again after editing and before using the new displayed command. The printed authorization binds the staged bytes (`bootstrap/_scaffold/upgrade.py` `_print_adopt_command` and `_cmd_adopt_collisions`), so a command obtained before editing refuses the changed file. Close by making the order explicit in both guides and exercising adaptation, re-staging, and adoption through the entry point.

**Coverage:** Read the committed diff, accepted plan and iteration evidence, mapping, template, upgrade guidance, tests and adoption authorization code; ran the two named focused tests above. Did not run the mapped selection, mutation checks or security review; separate Security Review and final wide integration remain owed.

## Targeted code review re-look -- Codex GPT-6 -- 2026-11-01

Reviewed fix `89e39034` and evidence `7a6897f8`; Tier: Internal; verdict: **finding closed**. Elapsed: approximately 2 minutes; tokens: unknown.

Both guides now direct the adopter to re-stage after editing, review the new copies, and use the new command. The new entry-point test verifies that the old authorization refuses edited bytes and that the new one adopts the reviewed bytes. I ran that test on a separate copy of `89e39034`: Python 3.12.9, **1 passed in 1.28 seconds**.

**Coverage:** Checked the ordinary review finding and its correction, including the test and implementation evidence. Did not repeat the broader review, mutation checks or Security Review; final wide integration remains owed.

## Security code review -- Codex GPT-6 Security Review -- 2026-11-01

Reviewed implementation: `89e39034`; evidence: `7a6897f8`; ordinary re-look: `7cf2c51d`.
Tier: Internal Security Review; Obligation: Internal Security Review;
verdict: **PROCEED**; findings: none.
Elapsed: approximately 15 minutes including serialization waits; tokens: unknown.

**Foundations**

1. **Should this ship as framed?** Yes. The sole production-code change adds
   `core/CHANGELOG.md` to `_CORE_MAPPINGS`. Existing `_install_one` skip/force
   behavior and upgrade provenance, containment and authorization guards remain
   intact. Corrected guidance requires fresh staging after edits and excludes
   other-source ownership, links and folders from collision adoption.
2. **Best alternative.** Reuse those guards, as implemented. A separate example
   loses the accepted ready-to-use root file; another adoption mechanism adds
   maintenance without improving preservation. The staged command binds both
   observed history and upstream bytes; adoption writes cache/lock records,
   never the history destination.
3. **What would show it wrong?** Silent collision application, stale-byte
   authorization succeeding, altered history or incorrect merge ancestry.
   An independent entry-point probe on a separate `89e39034` archive refused
   collision apply, preserved history, refused changed-byte authorization with
   an unchanged lockfile, then adopted restored bytes with the exact upstream
   `base_hash` and cache bytes. Python 3.12.9; 1.18 seconds. The implementation
   record reports seven passing focused cases and killed install-replacement
   and collision-bypass mutants; these were read, not rerun.

**Coverage:** Read committed changes, accepted criteria, install write guard,
new-core classification, adoption preflight/commit and corrected guidance;
independently probed preservation, authorization and base integrity. No new
machinery or trust boundary found. Did not establish race resistance, exhaust
all filesystem types, rerun implementation checks or run a suite. Final wide
Boundary B under Python 3.13.x remains owed before closure.

## Implementation verification -- Codex GPT-6 -- 2026-11-01

**Boundary B:** wide. Reviewed implementation range `f3b31530..89e39034`;
clean final reviewed commit `75e6091b` (ordinary and Security review records
included). Checks ran in a separate Git clone of that commit; clean before and
after. Interpreter: `/Users/kendal30/conda_envs/lhm/bin/python`, Python
3.13.13. Elapsed: 8 minutes 25 seconds for the interrupted mapped selection;
remaining gate and focused checks completed in about 10 seconds; total about
8 minutes 35 seconds. Tokens: unknown.

The mapped selector command included `--range f3b31530..89e39034` and the
changed files `bootstrap/UPGRADE.md`, `bootstrap/_scaffold/config.py`,
`bootstrap/tests/test_scaffold.py`,
`bootstrap/tests/test_upgrade_module_additions.py`, `templates/core/AGENTS.md`,
`templates/core/CHANGELOG.md`, and this plan. It selected 40 test files and
omitted 45 listed AGENTS.md readers under the selector guard. The corresponding
40-file `pytest -q` run was stopped after **1,028 passed and 8 skipped**; it
was executing `bootstrap/tests/test_repin.py:1001` at interruption. No failures
were reported before interruption. The test did not finish, so the mapped
selection is incomplete; whether that node was waiting externally or simply
slow was not established. No test was restarted. Per-file durations were not
captured; `test_repin.py` was the active file at the 8:25 stop.

Standing prose gates passed: `claim_check.py` on each changed guidance/template
file; `link_check.py` on the same three; `sync_doc_snippets.py --check`
(515 docs, no drift); and `quality_gate.py --sub neutrality` (`fail=0`,
`info=75`). Focused changelog entry-point checks passed: **4 passed in 2.28
seconds**, covering install preservation, manifest/template install, collision
fork adoption, and edit/re-stage/adoption authorization. Earlier implementation
evidence records the two independent mutation checks; they were not repeated
here. No full-tree certification or re-anchor was run.

**Disposition:** the wide mapped integration selection remains incomplete; this
record does not claim Boundary B passed. The Maintainer's plan-specific
disposition below waives the remaining broad selection for this plan.

## Maintainer disposition -- 2026-11-01

The 40-file mapped run on `75e6091b` was interrupted after 1,028 passed and 8
skipped; the skip reasons were not recorded. `test_repin.py` was active at
interruption, and the remaining selected tests were not run. The independent
Security Review, focused changelog entry-point checks, and prose gates passed as
recorded above. The Maintainer accepts those focused results for this plan and
waives the outstanding broad Boundary B selection before archiving. This
disposition does not clear or explain the eight skips, claim a full Boundary B
pass, or change the actual release check.

**Called by**: Maintainer -- chat, 2026-11-01

> "Accept focused results"

## Archive note -- Codex -- 2026-11-01

The accepted install and upgrade behavior is implemented and reviewed. The
Maintainer accepted the focused results and waived the unfinished wide mapped
selection for this plan in `f7f2d3ff`; the verification record remains explicit
that Boundary B did not pass. This archive commit removes the completed work
from the board and records the adopter-visible template in the changelog.

## Archive migration -- 2026-11-01

**Dispositions**: none outstanding. The incomplete broad selection was waived
for this plan by the Maintainer's disposition in `f7f2d3ff`; it is neither
claimed as passed nor left as a follow-up. The actual release check remains
under the existing release process.

**Evidence shipped**: install mapping, template and upgrade guidance in
`89e39034`; entry-point tests and restage guidance correction in `89e39034`;
ordinary review, Security Review and the targeted re-look in `7cf2c51d` and
`75e6091b`; implementation verification and Maintainer disposition in
`4f802e71` and `f7f2d3ff`.

**Evidence deferred**: none. The wide mapped selection remains incomplete as
recorded above and is waived for this plan only. The 1,028 passed, 8 unexplained
skips, active `test_repin.py`, unrun selected tests and 45 selector omissions
remain visible; no full Boundary B pass is claimed.

**Deferred evidence home**: none. The actual release check is governed by the
release process and is not a deferred follow-up from this plan.

**Fidelity sign-off**: `89e39034` delivers the accepted root template,
per-profile mapping, preservation and collision guidance, and focused entry-
point coverage. The shipped template offers unchanged history, optional
adaptation with re-staging, or a separately saved history before starting
fresh. The plan-specific assurance limit is the incomplete wide run recorded
above; the Maintainer's waiver does not change the preserved release check.
