# Plan: Release without the development tree

**Source proposal**: `dev/proposals/archive/2026-11-17-codex-release-without-dev.md`
**Status**: revising-plan
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-18
**Rules that apply**: `dev/rules/conventions.md`, `dev/rules/working-agreements.md`, `dev/rules/protected-surfaces.md`
**In brief**: Help projects leave development records out of releases while preserving their own work and finding dangling development references.

## Build summary

Give adopters development-folder guidance, ignored scratch space and an advisory boundary report. Preserve their release content and existing entry-file duties, and support project tests in either location. The report helps a Maintainer inspect a proposed release; it does not assemble or approve one.

## Source proposal

The accepted heavy proposal follows the settled repository layout and assigns the release-boundary report, folder guidance, optional test location and release-facing instructions to v0.8. It leaves the keep list and release cut script to the separate v0.9 module.

## Scope

Update the installed collaboration guide and its Cairn counterpart, entry and plan/proposal/contributing guidance, Cairn’s `README.md` and `docs/getting-started.md` as the kept README and first user-guide chapter, folder READMEs, module documentation and descriptive install inventory. Preserve all `AGENTS.md` development pointers as development-checkout-only, including the Operator stop when required development material is absent. An opted-in root `RULES.md` ships whole, has no run-rule dependency on `dev/`, and its development-only pointer is removed by an adopter using this release convention. Do not automatically rewrite adopter citations or move tests.

Inventory actual installed `dev/` folders from the installer destinations and directories it creates, plus tracked project folders, rather than treating the present catalog as exhaustive. Give each mapped or explicitly created installed folder a short README stating purpose, suitable contents and required Maintainer permission; describe generated cache descendants in their owning README. List permitted top-level folders in `dev/README.md`. Project-added folders follow the same rule; a list or README records permission and does not grant it. New `dev/` folders and committed briefs or reports used to evade length limits need permission. Add tracked `dev/scratch/README.md` and `dev/scratch/.gitignore`, ignore its other contents, and explain that ignore is not secrecy; private evidence stays out of commits and releases. Durable conclusions go to their proper records and no file outside `dev/` points to scratch.

Describe release-side content as project source, tests, examples, user and theory docs, changelog and metadata; references to deliberation use date and topic rather than paths into `dev/`. Development guides may cite records. Add concise agent entry sentences to the kept README and first user-guide chapter pointing to `AGENTS.md` and then the guide without requiring `RULES.md`. Describe test configuration for `dev/tests/` and existing locations, root-relative fixtures and qualified `dev.tools` / `dev.tests` imports. Provide no automatic relocation.

Extend the installed link checker with `python dev/tools/link_check.py --release-boundary dev/scratch/release-scope.json`, optionally `--root`; reject normal scanner options and file arguments in this mode. The UTF-8 JSON object has exactly `kept` and `development` arrays of repository-relative POSIX exact file paths or directory prefixes ending `/`; reject globs, absolute, drive, UNC and `..` paths. The reviewed scope may be scratch or committed and controls only this report. `dev/` is implicitly development; root `AGENTS.md` must be kept. All other classifications belong to the project.

Use the pinned Git reader and exact Git top-level check to inventory all tracked working-tree paths, without ordinary Markdown filters or a walk fallback. Unmatched selectors, unclassified paths outside `dev/`, overlapping classes, unavailable inventory or unsafe inputs are incomplete. Read working-tree bytes only for kept files, scope and `dev/README.md`, refusing linked/reparse components, nonregular, missing, unreadable, out-of-tree, non-UTF-8 or NUL-containing files; no external probes or target reads. Reuse raw Markdown link/reference patterns independent of allowances; resolve local Markdown targets relative to their source (`/` means root), decode URL escapes once and strip query/fragment. Also identify literal root-relative `dev/` tokens, including backticks and Windows separators. Report lexical references whether targets exist; identify root `AGENTS.md` pointers as exempt. Document these literal limits and that untracked files and indirect dependencies are outside coverage.

Derive every `dev/` folder ancestor from tracked names. Preserve index modes and stages from the pinned Git inventory; `_tracked_index_paths` discards them. A folder README qualifies only with a regular stage-zero index entry. Use the `dev/README.md` table only when it qualifies and its contained working-tree read succeeds; otherwise report incomplete alongside known missing-guide findings. Find missing indexed regular READMEs, top-level folders absent from first-column backticked `name/` rows under `## The tree`, and indexed scratch names other than its README and ignore file, even when missing on disk. Generated cache descendants remain in this inventory; document them at the owning `.cairn` README without writing into the raw-template cache. Print deterministic findings, incomplete reasons and `WITH FINDINGS`, `INCOMPLETE` or `CLEAN`; findings alone exit 0, incomplete exits 2 even with findings. The mode is advisory, not a gate.

**Reuse.** `templates/modules/team-gated/link_check.py` already installs as `dev/tools/link_check.py` and supplies local parsing and the pinned Git reader; `install/_scaffold/config.py` owns installed destinations. Searches of those paths and `templates/core/dev/` found existing installation and folder guidance, not a release-boundary report. Extend those homes rather than add a second packager or report runner. No published methodology change.

Proposed paths:
- `dev/scratch/README.md`
- `dev/scratch/.gitignore`
- `dev/tests/`

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Specify and implement the advisory report | Reviewed plan | Installed link-checker mode and public checks |
| C2 | Add folder and scratch guidance and installer ownership | C1 | Guides, scratch seed and upgrade preservation |
| C3 | Update release-facing guidance and test-location support | C2 | Entry guidance, templates and test examples |
| C4 | Verify public install, upgrade and release scenarios | C3 | Focused evidence and dispositions |

Expected work: several focused sessions; installer migration and platform coverage may extend it. The parent owns one joined Group 4 integration after connected work. Human signing, trust and release operations are separate board waits, not completion gates.

## Acceptance criteria

**C1.** Through the installed report, a kept file's reference to an existing `dev/` target is a finding despite an allowance; a classified development guide and retained `AGENTS.md` pointer are distinguished. Missing or unlisted folders and forced-tracked scratch are findings; an untracked root list or a nonregular indexed root guide replaced by a regular working-tree table cannot satisfy membership and reports incomplete; a fully classified clean fixture is clean. Unclassified, out-of-tree, unreadable, skipped or unavailable inventory is incomplete. Findings alone exit 0; incomplete exits 2. No project content executes, external links are probed or files change.

**C2.** Fresh install and upgrade preserve project-owned content and collision protections; each mapped or explicitly created development folder has a purpose-specific README, generated cache descendants are described at their owner, top-level folders are listed, and the two tracked scratch files survive while other scratch content is ignored. Folder guidance records, but never grants, permission. Git ignore is not described as confidentiality.

**C3.** Release-facing guidance preserves the entry-file exception and Operator stop, separates kept content from development records and does not impose optional `RULES.md`. An adopter can configure tests in both supported locations and use root-relative fixtures and qualified imports without moving existing tests. A fixture with colliding bare names selects the intended qualified modules.

**C4.** A disposable installed project demonstrates the report's required positive and clean controls, preservation on upgrade and its retained tests after `dev/` is omitted; missing prerequisites are reported rather than passed. Inspect installed lock destinations and named root exceptions. Record the actual output and limitations; do not treat this fixture as a real release.

## Scope delta

**Scope delta**: preserved.

## Verification

Before implementation select changed-file checks with `python tests/tier_inventory.py for <paths>` and run only applicable public-promise tests, plus claim, link, snippet and neutrality gates for prose. Use `/Users/kendal30/conda_envs/lhm/bin/python3.13`. Map report cases to `tests/test_doc_drift_tools.py` through the installed link-checker entry, installation and upgrade to their existing public entry tests, and both test locations to the public test-selection entry. Include a known-positive forbidden reference despite an ordinary allowance, and a clean classified control. Preserve applicable protected-surface checks, independent ordinary and Security code reviews and negative install/upgrade controls. Independent scientific check: N/A, as accepted. Record benefit versus cost and separate human operations' unpassed evidence before archive.

## Plan review -- Terra (Reviewer, Medium) -- 2026-11-18

**Reviewed commit**: 9080b56be3924e018358bddb032da00af4fc6d10
**Obligation**: Internal
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: the plan retains the advisory report, project-owned content, entry-file exception, optional test locations and scratch guidance without adding a release gate. -- Scope, C1–C4, accepted Proposal
2. **Best alternative.** Extend the installed link checker and existing installer rather than add a packager or second report runner; the separate release module retains its later work. -- Scope, Reuse, Source proposal
3. **What would show it wrong?** An installed report missing a known forbidden reference despite an allowance, or reporting unreadable or unclassified input as clean, would falsify the boundary. -- C1, Verification

The specified scope, inventory and result rules make the report actionable for implementation; raw-cache descendants remain inventoried and may produce honest advisory findings. The longer opening earns its detail by defining that boundary and failure behavior. The Operator stop and existing entry duties remain; folder listings record permission rather than grant it. Public checks and negative controls target outcomes rather than prose pins; parent integration and human release operations are separate. Coverage: compared the committed plan with its accepted proposal and review rules; did not run a report, installer, upgrade or tests, or assess the security boundary. Security Review remains separate.

## Plan review -- Codex Sol (Security Review, High) -- 2026-11-18

Reviewed commit: 9080b56be3924e018358bddb032da00af4fc6d10

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown. **Tokens**: unknown.

An offline report can help an adopter spot dangling references while leaving
release decisions and project files in the adopter's hands.

**Foundations**

1. **Should this happen as framed?** Yes, once folder evidence has an explicit index rule. The plan confines reads to the project and makes unavailable Git or incomplete classification visible. — Scope, C1, accepted proposal item 4 and S1–S5.
2. **Best alternative.** Use the pinned Git reader and raw link patterns for the advisory mode, and inventory installed folders from destinations and directory creation. — C1–C2, `templates/modules/team-gated/link_check.py`, `install/_scaffold/config.py`, `install/_scaffold/install.py` (`_DEV_DIRS`).
3. **What would show it wrong?** An installed-command case where a plausible untracked or nonregular indexed root guide satisfies the folder listing would break tracked-only coverage. — Scope, C1, `templates/modules/team-gated/link_check.py` (`_tracked_index_paths`).

**Blocking.** Define the index evidence in Scope and C1. The path-only helper
drops mode and stage. Require a regular stage-zero index entry for a folder's
README. Use the root `dev/README.md` membership table only when that entry
also passes the contained working-tree read. If the table is unavailable,
report incomplete alongside any known missing guide findings. Include the
public control in Foundation 3.

**Rule retention.** The plan retains the `AGENTS.md` exception and Operator
stop, optional root rules, scratch privacy and cache-byte preservation.

**Coverage.** Compared the accepted proposal and committed plan with the
scanner, installation destinations and directory creation. Runtime probes,
native-platform checks and installer runs were outside this pass.

## Response -- Terra (Implementation) -- 2026-11-18

**Disposition**: ready-to-implement
**Elapsed**: unknown
**Tokens**: unknown

Accepted the index-evidence finding. Scope now retains index mode and stage, requires a regular stage-zero README and a contained readable root table, and reports incomplete when that table is unavailable. C1 adds installed-command controls for untracked and nonregular indexed root guides. This restores the accepted tracked-folder report without changing its boundary.
