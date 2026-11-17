# Plan: Repository layout and self-adoption

**Source proposal**: dev/proposals/archive/2026-11-09-claude-repository-layout.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-17
**Rules that apply**: dev/rules/conventions.md, dev/rules/protected-surfaces.md, dev/rules/working-agreements.md, dev/rules/development-environment.md
**In brief**: Put Cairn's installation, tests, release work and installed tools in clear homes while preserving adopters' changes.

## Build summary

Move Cairn's source and installed tools to the accepted homes, using its own upgrade for the installed copies. Preserve local work and the existing chain of trust during the move. The result includes the layout checks, updated guidance, and a reviewed candidate for the Maintainer's separate re-anchor; it does not claim that operation has passed.

## Source proposal

The accepted repository-layout proposal specifies twelve outcomes, destination migration and self-lock reconciliation, historical-source compatibility, and a verified old-to-new trust transition. Its Decision amendment removes the need for a Claude Code wrapper while retaining a fallback and root skills.

## Scope

Apply the proposal's items 1–12, including the root `.gitattributes` exception, root governing files and `.agents/skills/` and `.claude/skills/`. Preserve the installed method background from `templates/core/dev/method-background.md`, the scientific-testing module and the rules-folder offer. Keep `dev/architecture_review.md` and `dev/ceremony-record.md`: the proposal authorizes no move for either. Do not ship the separately queued `token_budget` and `verify_counts` additions here.

Move `bootstrap/tests/` to `tests/`, `bootstrap/` to `install/`, pre-install phase-0 and readiness inputs to `install/`, root `dimensions/` and `on-ramp/` to `install/`, onboarding guides into `templates/`, and `case-studies/` into `docs/case-studies/`. Move the two baseline and re-anchor runbooks, `reanchor.sh`, launcher and values templates from `bootstrap/`, and `repin.py`, `reanchor_ceremony.py`, `check_release_publication.py` and `check_release_test_members.py` from `scripts/` to `release/`. Place remaining Cairn-only scripts in `tests/`, keeping `audit_report.py` beside `gauge.py`; migrate the installed tools from `tools/` and `scripts/` to flat `dev/tools/` through upgrade. Move associated manifests and configuration alongside their readers. Machine-assisted path rewrites must be surgical: inspect each functional-prose patch, retain its duties and do not rewrap it.

**Reuse.** `bootstrap/_scaffold/{config,install,upgrade}.py` contains mappings, staging and historical reads; `scripts/repin.py` and the re-anchor runbook contain the existing authority chain. `rg 'parents\[|CAIRN_ROOT|_theirs_text|reanchor|VENDOR' bootstrap scripts tools templates` finds existing root, migration and wrapper mechanisms. Extend these rather than creating a parallel installer or verifier.

### Documentation / doctrine surface

Update both `AGENTS.md` files for commands, citations and `dev/` as records, state and tools; put folder roles in `docs/DOCUMENTATION_PLAN.md` and link from `README.md`. Update install guidance, module docs, skills, examples and path references in their current authoritative homes. Keep the vendor-neutrality exceptions limited to `docs/case-studies/`. Preserve the applicable rules in shipped instructions.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Discover roots and inventory source, destination and lock ownership | None | Shared test root helper; executable root fixes; reviewed mapping |
| C2 | Implement destination migration and reconcile self-lock | C1 | Upgrade transaction and provenance reconciliation |
| C3 | Relocate sources and update references | C1–C2 | New layout, compatibility entry and wrapper guidance |
| C4 | Run real self-upgrade and prepare trust transition | C2–C3 | Self-adopted tools and verified candidate chain |
| C5 | Verify promises and close records | C1–C4 | Focused evidence, reviews and issue closure |

## Acceptance criteria

**C1.** Tests use one repository-root helper based on a repository marker, not parent counts. Installed commands and configuration discover their intended project root, including `content_scan_runner.py`; test misleading nested roots through public entry points. Inventory all installer sources and destinations, selected modules, unlisted self-hosted copies, and source moves in the committed mapping. Mapping has one owner per destination and names every root exception: `AGENTS.md`, `RULES.md`, `VENDOR.md`, `.gitattributes`, `.agents/skills/`, Claude skills discovery, and project-facing `CHANGELOG.md`, `NOTICE.md` and selected optional templates. Inventory actual lock destinations, including every selected module. Record elapsed and tokens for each step, or `unknown`.

**C2.** Upgrade uses explicit revision-aware old/new source and destination mappings, not lock claims as authority. For unchanged tracked files move verified bytes; preserve executable modifications as marked forks and merge modified prose only against a verified base. Keep installed hashes distinct from upstream base hashes and migrate cache references. Unprovable ancestry remains unknown, bytes stay untouched, and the report names reconciliation; verify actual source commits/blobs or caches with rendering inputs before recovering bases, including unlisted copies. Stage bytes, provenance and lock/cache updates together; recheck inputs before apply, retain old bytes until verified destination and recoverable transaction state are durable. Occupied, conflicting, linked or non-file paths refuse without overwrite or traversal. Interrupted retry recognizes completed bytes, refuses changed inputs and never deletes the only copy. Retained old paths are reported and prevent migration-complete claims. Existing onboarding copies survive Write E separately; historical reads resolve the path appropriate to their revision.

**C3.** Every installed template source is under `templates/`, and every file there is read by the installer; every `dev/tools/` file is an install destination, with no Cairn root `scripts/` or `tools/`. Check every lock destination lies under `dev/` or a named root exception. Build a test release archive with `dev/` omitted and inspect its remaining Cairn footprint, including `AGENTS.md`; do not claim the exceptions disappear. Mutate each layout rule to confirm its check fails. Release-policy work stays with the later release items. `cairn/…` citations mean Cairn's source, bare `bootstrap/` citations are repaired, and a test install passes link checking. The legacy `bootstrap/scaffold.py` only reports the new command until v1.0. Hooks, imports, configuration, hashes and manifest paths follow moved files; preserve byte-identical shipped twins and existing module behavior. Keep `VENDOR.md` for other tools but stop directing Claude Code users to create a wrapper. Put Claude habits in `AGENTS.md`, document the local uncommitted `CLAUDE.md` fallback containing `@AGENTS.md`, and leave existing adopter wrappers untouched. An agent checks a fresh desktop session for an observable instruction unique to `AGENTS.md` with the wrapper absent in a disposable copy; remove Cairn’s wrapper only if that check succeeds. If the desktop session cannot be tested or the check fails, retain the wrapper and record the limit; no human action gates archive.

**C4.** The real self-upgrade uses C2 and completes without overwriting adaptations or leaving competing commands. Preserve the old anchor's verifier and interpreter binding while preparing the new layout: verify candidate bytes, paths and import roster before any candidate import, using the old trusted verifier and independently trusted signer. Update the existing ceremony's exact path and module roster as a reviewed transition, not a candidate-authorized loader. Substituted helpers, unauthorized candidate code and wrong interpreters refuse before import. If the chain cannot establish authority, stop for the named Maintainer risk decision. The Maintainer's exact authorization and re-anchor are a separate board wait with linked evidence; the anchor stays unpassed until performed and does not gate plan archive or permit activation or release.

**C5.** Run the checks below on the final relevant bytes; remedy failures before code review and archive. Close #67 when the destination inventory and root exceptions establish its promise. Close #90 only if its full issue scope is satisfied; the broader helper standard remains queued. Close a satisfied issue at its fixing commit, not release. Record limitations, review dispositions, changed-file burden and benefit versus cost.

## Scope delta

**Scope delta**: preserved

Proposed paths:
- `dev/tools/`
- `docs/case-studies/`

## Verification

Use the canonical Python recorded in the environment. Before implementation run `python tools/test_tiers.py for <changed paths>`; run mapped checks and prose gates for changed prose, including claim, link, snippet and neutrality checks, and pass the reviewed range for governing text. Follow changed public promises through scaffold fresh install, v0.7 migration and Cairn's real self-upgrade: unchanged, forked, unprovable, occupied/linked and interrupted/retry cases check bytes, ownership, locks, caches and stale commands. Check historical reads, misleading roots, layout mutants and ceremony refusals through public entries. The layout check joins certification; migration and ceremony checks run in plan verification. Test a negative search with a known positive. Retain only external-promise tests and protected guards; remove developmental probes.

Run scaffold summary and dry-run, both example self-tests, prose gates at their new paths, and test-install link checking. In the separate authorized certification operation compare clean before/after pass, skip and node counts; counts alone establish neither behavior nor authority. Keep those results unpassed until the Maintainer runs it. The arc owner runs one joined integration selection at arc end, not a suite per chunk. Record covered bytes, inputs, platform, omissions and results. Scientific independent check: N/A, as in the proposal. Obtain fresh ordinary and Security code reviews; a review names what it did not cover. Unexpected drift, missing evidence or failed checks remain implementation work.
