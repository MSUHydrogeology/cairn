# Plan: Ship a changelog template

**Source proposal**: dev/proposals/archive/2026-11-01-codex-changelog-template.md
**Status**: implementing
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
This is iteration evidence only; ordinary code review and Security Review remain
owed before Boundary B.

## Author response -- Codex GPT-6 -- 2026-11-01

Both the ordinary plan review and Security Review recommend proceeding with no findings. The accepted scope and verification remain unchanged.

Elapsed: approximately 1 minute; tokens: unknown.
