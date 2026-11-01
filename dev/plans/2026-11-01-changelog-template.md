# Plan: Ship a changelog template

**Source proposal**: dev/proposals/archive/2026-11-01-codex-changelog-template.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Give adopters a usable changelog while preserving their existing history during installation and upgrades.

## Source proposal

The Maintainer accepted the heavy proposal at `7f8e3a14`: install a root changelog for every profile, explain its format and existing-history choices, and preserve existing collision and overwrite safeguards.

## Scope

Add `templates/core/CHANGELOG.md` and its core mapping in `bootstrap/_scaffold/config.py`; update the shipped `templates/core/AGENTS.md` reference, `bootstrap/UPGRADE.md` and any install descriptions needed for accuracy. The published install manifest must include the mapping. Add focused tests in existing bootstrap test homes. This touches adopter-facing governing guidance and the install contract; no new doctrine is proposed.

**Reuse.** Searched `_CORE_MAPPINGS`, `bootstrap/tests/test_scaffold.py` and `bootstrap/tests/test_upgrade_module_additions.py`: core mappings already deliver across profiles, while existing install skip, collision staging and adoption handle history. Extend their behavior tests rather than introduce a second workflow or new machinery.

Proposed paths:
- `templates/core/CHANGELOG.md`

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
