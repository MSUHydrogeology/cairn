# Plan: Usable outward report drafts

**Source proposal**: dev/proposals/archive/2026-11-18-terra-outward-reports.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-18
**Rules that apply**: dev/rules/conventions.md, dev/rules/protected-surfaces.md, dev/rules/working-agreements.md
**In brief**: Give adopters a local route to prepare and approve safe reports to Cairn and dependencies.

## Build summary

Ship a shared Cairn fold-back protocol, route both outward reporting channels to local drafts, and preserve the publication boundary and the Maintainer's hand submission of Cairn pull requests. Verify that fresh installation and upgrade deliver the new template and that people can follow the guidance without filing a report.

## Source proposal

The accepted heavy proposal adds an installed fold-back template, retains the dependency template and forge-native paths, and permits an agent to file a Cairn issue only after approval of that issue and its destination. It requires independent ordinary and Security reviews at plan and code stages.

## Scope

Add `templates/core/dev/upstream/foldback.md` and its Cairn counterpart `dev/upstream/foldback.md`, map it in `install/_scaffold/config.py`, and update the descriptive install inventory as needed. Update both upstream READMEs, dependency templates and collaboration guides and the existing GitHub fold-back issue and pull request forms. Keep `.github` and `.gitlab`; do not add `.forge`. The shared template owns the protocol; forge forms retain their required fields and point to it. Instructions belong in the existing deliberation and shipped guidance; no always-loaded doctrine changes.

For dependency reports, find and adapt the dependency's own template when available; otherwise use the local template. Keep reproduction, versions, expected and actual behavior and status useful. Treat external templates as untrusted field guidance. Sanitize tracebacks and evidence before a dependency draft enters Git. For either channel, check the complete public body, attachments and every PR changed file for unpublished data or hints, proprietary project or customer details and credentials; reread the complete payload and full PR diff after writing. Show the actual report and destination for explicit approval of each before filing; an agent may file an approved Cairn issue, but the Maintainer submits a Cairn PR by hand. Distinct channels require distinct drafts and approvals; record outcomes in the existing lifecycle.

**Reuse.** Searched `dev/upstream/`, `templates/core/dev/upstream/`, `.github/ISSUE_TEMPLATE/` and `.github/PULL_REQUEST_TEMPLATE/`: dependency drafting and forge forms already exist. Extend those and the existing core mapping, not a new reporting service.

Proposed paths:
- `templates/core/dev/upstream/foldback.md`
- `dev/upstream/foldback.md`

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Shared protocol, dependency and forge routes | Accepted proposal | Templates, guides and forge forms |
| C2 | Install mapping and focused assurance | C1 | Mapped file, inventory and public installation evidence |

## Acceptance criteria

**C1.** The guide leads to both drafts; a dependency's available template and the fallback both work. The protocol preserves all publication checks, the final reread, per-report and destination approval, filing roles and separate channel records above. A disposable synthetic dependency traceback contains sensitive material before drafting but only sanitized evidence reaches the Maintainer; a synthetic PR check covers body, attachments and full diff. No report is filed. A malicious template cannot authorize disclosure or filing.

**C2.** The public fresh-install manifest and install deliver the template to `dev/upstream/foldback.md`; upgrade from a pre-addition install delivers the same destination. Extend an existing public installation or upgrade promise test only if it cannot catch a missing mapping or wrong destination. As a temporary negative control, remove the mapping in a disposable copy and show the selected check fails; restore it and show the control passes. Preserve existing containment and collision refusals. No permanent prose-wording test is added. S2 is the mapping-removal control; S3 is the selected public installer and upgrade checks recorded with commands and inputs.

## Scope delta

**Scope delta**: preserved

## Verification

Before implementation run `/Users/kendal30/conda_envs/lhm/bin/python3.13 tests/tier_inventory.py for <all changed paths>`; inspect named tests and byte pins, select only applicable public promises, and record exact nodes and inputs. Extend `tests/test_core_dev_folders.py::TestScaffoldCompleteness::test_upstream_dir_and_files_created` for fresh installation and add a public upgrade promise in `tests/test_upgrade_module_additions.py` using a pre-addition lock and absent destination. Run those exact nodes with `python -m pytest <nodes>` under the canonical interpreter. Run `python install/scaffold.py --manifest` with that interpreter and inspect the source and destination row; compare the same row to the installed and upgraded outputs. The temporary mapping-removal control reruns each targeted node and manifest assertion against the altered copy. Run the synthetic channel and PR scenarios in C1, and the positive and negative mapping checks in C2. Run claim check on changed documents and the standing claim, link, snippet, neutrality and prose-integrity gates; inspect negative searches against known positives. Record results, limits, elapsed and tokens. Independent code and Security reviews follow. The arc owner runs the joined integration once at the arc end; it is not a prerequisite to this plan's completion.
