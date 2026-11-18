# Plan: Ship measurement tools

**Source proposal**: `dev/proposals/archive/2026-11-18-terra-ship-measurement-tools.md`
**Status**: ready-to-archive
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-18
**Rules that apply**: `dev/rules/conventions.md`, `dev/rules/working-agreements.md`, `dev/rules/protected-surfaces.md`
**In brief**: Install two existing measurement commands so adopters can estimate instruction size and check documented counts.

## Build summary

Ship a standard-library token estimator and a count checker with an empty, editable JSON registry. Preserve Cairn's internal commands and make installed definitions survive upgrades while keeping executable support under integrity checks. Document both commands and verify the public install, upgrade and command paths.

## Source proposal

The accepted heavy proposal assigns the estimator to documentation-plan and the checker, support and empty registry to claim-check. It fixes the trust boundary, supported measurements, containment, Git invocation, status reporting and required checks; this plan executes that decision for v0.8.

## Scope

Adapt `tests/token_budget.py`, `tests/verify_counts.py` and `tests/measurements.py` into the four source and installed paths named in the proposal. Update `install/_scaffold/config.py`, lock/integrity handling, relevant manifest and release records, the two module guides and published inventory/tool descriptions. Preserve internal definitions, preset counting, sibling checkouts and audit behavior. No new governing doctrine; guide instructions live in the installed module guides, descriptions in `docs/` and deliberation here. Use the existing unconditional `dev/tools/git_read.py` owner and verified-buffer binding without fallback.

The registry is an object keyed by whole `[\w-]+` names. Each value is exactly either `{"kind":"snapshot","value":<nonnegative integer>,"as_of":"YYYY-MM-DD"}` or `{"kind":"invariant","fn":<operation>,"target":<string>,"root":<project-relative directory>}`; root may be omitted for the project root. Operations are `count_lines`, `count_files`, `count_defs`, and `git_commits_in_range`. Reject duplicate keys at every object level, unknown fields, wrong types (including booleans as integers), invalid dates and unsupported operations. Before reading the fixed registry, resolve it and refuse a link outside the project; missing, unreadable or malformed registry fails even when no annotations exist. No executable definitions. Annotation parsing treats every HTML comment starting with optional whitespace and `verify:` as an attempted marker, rejecting malformed or unclosed markers and missing preceding same-line numbers. Snapshot dates must appear on the line.

Resolve roots against the project above `dev/tools/`; enforce project containment before an absent root can skip. Resolve file targets and every counted child within the selected root; refuse escapes. For history, require Git 2.45+, exact resolved worktree-root equality, a non-option-shaped validated range and `git log --oneline <range> --` through the bounded pinned helper. A failure takes exit 1; otherwise a skip takes 3; no markers reports zero checks and exits 0. The estimator uses characters divided by four, labelled approximate in text and JSON, detects common always-loaded files or accepts explicit files, warns by default and makes caps strict only on request.

**Reuse.** `tests/measurements.py` supplies the fixed counters and verified Git reader; `tests/verify_counts.py` supplies annotation and result handling; `tests/token_budget.py` supplies detection and caps. Search of `install/_scaffold/config.py`, `release/` and the named tests found existing module mappings and install/upgrade checks; reuse them rather than introduce a second installer or registry engine.


## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Adapt estimator and count support, parser and registry | Reviewed plan | Four standard-library source files |
| C2 | Wire module ownership, upgrades and integrity; document commands and inventory | C1 | Installer, guides and release records |
| C3 | Exercise installed contracts and record results | C2 | Focused public-promise checks and evidence |

Expected work window: several focused sessions; installer integrity interactions may take longer. The parent owns the joined Group 4 integration after connected work. Human trust, release and signing operations are separate board waits, with evidence and owner, not plan completion gates.

## Acceptance criteria

**C1.** Installed `token_budget.py` works from outside the project for detected and explicit files, labels its approximation in text and JSON, warns by default and fails strict caps. Installed `verify_counts.py` reads only the fixed JSON registry and verifies snapshots and all four operations. It refuses an escaping registry link before reading, and a missing, unreadable or malformed registry even without annotations. It refuses malformed or unclosed markers, a dotted key in either input, invalid definitions, unknown keys, escapes and changed helper bytes; reports zero, drift and skips with the specified statuses. Git accepts a valid range and fails a missing range even when a same-named file exists. Existing internal entry points and definitions remain usable.

**C2.** Public install places each file under its named module. Upgrade preserves an edited registry and verifies it as mergeable data, while changed shipped Python fails integrity. Existing collision/customization protection remains. The guides show registry syntax, key-only markers, zero checks, malformed markers, skips, reviewed definitions, approximate estimates, caps and Git requirements. Inventory and release records match the delivered paths.

**C3.** Public installed commands, installer, upgrade and integrity checks demonstrate C1 and C2 with both positive and negative controls, including an escaping registry link against a valid in-project registry, missing and invalid registries without annotations, root containment before skip, direct and child-link escape, exact Git worktree root and revision-only behavior. Run both commands from outside a disposable install. Add permanent checks only for public promises; remove developmental probes before archive. Record coverage and omissions.

## Scope delta

**Scope delta**: preserved.

## Verification

Before implementation run `python tests/tier_inventory.py for <changed paths>` and run only mapped tests, plus applicable prose gates. Map the installed command cases into `tests/test_verify_counts.py`, install and integrity cases into `tests/test_manifest.py`, and preservation into `tests/test_upgrade_module_additions.py`; use the public entry points. For security negative controls, refuse an escaping registry link and missing, unreadable or malformed registries even without markers, with a valid in-project registry as control; mutate a count, use an unknown key and escaping targets, and alter the pinned helper; pair each refusal with a valid control. Check that registry edits pass integrity while support edits fail. Run claim, link, snippet and neutrality gates for prose and applicable release gates. Use `/Users/kendal30/conda_envs/lhm/bin/python3.13` and record results and limits. Independent scientific check: N/A, as accepted. Independent ordinary and Security code reviews remain required. Record benefit versus cost and any separate human operation's unpassed evidence before archive.

## Plan review -- Terra (Reviewer, Medium) -- 2026-11-18

**Reviewed commit**: 91a3f77bbdad3373bc64fb452f44dda42c8ab638
**Obligation**: Internal
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: the plan preserves the accepted tools, data boundary, upgrade protection, documented use and public checks while keeping human release operations separate. -- Source proposal, Scope, Acceptance criteria
2. **Best alternative.** Reusing the existing counters, parser, installer and pinned Git reader is simpler than maintaining a second measurement and installation system. -- Scope, Reuse, `tests/measurements.py`, `install/_scaffold/config.py`
3. **What would show it wrong?** A disposable public install or upgrade that loses an edited registry, accepts an escaping count or changed helper, or cannot run either command would falsify delivery. -- C1–C3, Verification

The criteria focus permanent checks on public promises; developmental probes are removed. The module guides are the installed homes for the new procedures, and no governing rule is removed. Parent-owned joined integration is named in Sequence. Coverage: compared the committed plan with the accepted proposal, template and review rules; did not run commands, tests or upgrades, inspect implementation, or assess the security boundary. Security Review remains a separate obligation.

## Plan review -- Codex Sol (Security Review, High) -- 2026-11-18

Reviewed commit: 91a3f77bbdad3373bc64fb452f44dda42c8ab638

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Steelman.** Adopters can edit count definitions while installed Python remains covered by integrity checks.

**Foundations**

1. **Should this happen as framed?** The schema, key-only markers, fixed operations and upgrade ownership deliver the Decision once the registry load itself is contained (Scope, C1–C3, accepted Proposal).
2. **Best alternative.** Use the existing unconditional helper and verified-buffer binding for Git. An exact worktree root and trailing `--` keep the bounded call revision-only (`install/_scaffold/config.py:916`, `tests/measurements.py:53-157`, Scope).
3. **What would show it wrong?** An installed check accepting a registry link outside the project, changed helper bytes or an invalid revision range matching a filename, or an upgrade losing an edited registry (C1–C3, Verification).

**Blocking — contain the registry before reading it.** The accepted Proposal explicitly refuses an escaping link at the fixed JSON registry path. Scope contains measurement roots and targets. A fixed registry pathname can still follow a link outside the project. In C1, require containment before loading the registry and failure for an absent or invalid registry, as in Security preflight S4. In C3, verify refusal of an escaping registry link through the installed command, alongside a valid in-project registry.

**Coverage.** Compared the committed plan with the accepted proposal and final Security response, helper ownership, and current binding. No implementation, install, upgrade, command probe or suite ran.

## Response -- Terra (Implementation) -- 2026-11-18

**Disposition**: ready-to-implement
**Elapsed**: unknown
**Tokens**: unknown

Accepted the registry-load finding. Scope now requires containment before reading and failure for a missing, unreadable or malformed registry even without annotations; C1 and C3 make the refusal and valid in-project control observable. This restores the accepted proposal’s S4 boundary without changing it.

## Implementation evidence -- Terra (Implementation) -- 2026-11-18

The implementation and public checks are in `32037a03`; the direct-link, unreadable-registry and release-scan corrections are in the following commit. The four focused installed command, manifest, upgrade and integrity tests passed under Python 3.13.13. The two installed-command tests passed again after the added controls. Three release-scan checks passed, including the corrected current-path assertion. Claim checks, snippet sync and neutrality passed. Link checking reported unrelated stale historical paths; external links were not probed. No full suite, native Windows, signing or baseline operation ran. The parent owns joined Group 4 integration and separate human trust/release operations.

**Benefit versus cost**: unknown -- adopter commands and maintained registry delivered; cost and remaining burden unknown; revisit after usage and joined integration.

**Elapsed**: unknown
**Tokens**: unknown

## Code review -- Codex Sol (Security Review, High) -- 2026-11-18

Reviewed commit: a6fa653aaec59628a0dd45f7eb031a9732d057e0
Reviewed measurement source range: fc880f8ea6bd336c85aa96d68f7711bcee2f86ab..089c678f6bb711780fe55aaf6813d54f7e85227a

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Steelman.** A fixed JSON registry lets adopters customize counts while shipped Python remains integrity-checked.

**Foundations**

1. **Should this happen as framed?** Yes once attempted markers cannot vanish across a line break. The checker validates the contained registry before reading annotations and dispatches four fixed operations (`templates/modules/default-on/measurements.py:249-304`, `templates/modules/default-on/verify_counts.py:173-189`).
2. **Best alternative.** Preserve the existing module and integrity paths, the caller-pinned bounded helper, and the exact-root check with a revision-only Git invocation (`install/_scaffold/lockfile.py:215`, `templates/modules/default-on/measurements.py:27-125`, `templates/modules/default-on/measurements.py:224-246`).
3. **What would show it wrong?** A local edit lost on upgrade, a changed helper accepted, or a malformed attempt reported as zero checks (`tests/test_upgrade_module_additions.py`, `tests/test_verify_counts.py`, C1–C3).

**Blocking — recognize a marker opener across whitespace.** Scope covers every HTML comment beginning with optional whitespace and `verify:`. The scanner splits the document first, so an opener `<!--` followed by a newline and `verify: key -->` never reaches the malformed-marker branch. It can exit 0 with zero checks. Recognize attempted openers across whitespace and reject cross-line attempts under the same-line rule. Add this case to the existing installed malformed-marker checks (`templates/modules/default-on/verify_counts.py:60-75`, `tests/test_verify_counts.py`).

**Coverage.** Read committed code, module ownership and existing install, integrity, upgrade and refusal evidence. Guide additions retain the existing duties. No checks were rerun. Native Windows, signing and joined integration were outside this pass.

## Response -- Terra (Implementation) -- 2026-11-18

**Disposition**: awaiting-code-review
**Elapsed**: unknown
**Tokens**: unknown

Accepted the cross-line opener finding. The parser now finds attempts across the whole document and rejects any that span lines. The existing installed malformed-marker check includes the reported case; `test_installed_measurement_commands` passed under Python 3.13.13. No other checks were rerun. Ordinary code review remains outstanding.

## Code review -- Terra (Reviewer, Medium) -- 2026-11-18

**Reviewed commit**: 4c296221817b11d18f4771096d28c4a306887f02
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: the installed estimator labels its approximation, and the count checker uses the fixed registry and operations with visible drift, skips and failures. -- `templates/modules/default-on/token_budget.py`, `templates/modules/default-on/verify_counts.py`, `templates/modules/default-on/measurements.py`
2. **Best alternative.** Reusing existing counters, module installation and verified Git support avoids a parallel installer or executable adopter registry. -- Scope, `install/_scaffold/config.py`, `templates/modules/default-on/measurements.py`
3. **What would show it wrong?** An installed upgrade losing a local definition, or a malformed marker reporting zero checks, would falsify delivery. -- `tests/test_upgrade_module_additions.py::test_measurement_registry_survives_upgrade_and_support_is_checked`, `tests/test_verify_counts.py::test_installed_measurement_commands`

The public tests cover the four operations, containment, Git range behavior, integrity and upgrade preservation; the recorded correction rejects a cross-line attempted marker through the installed command. Guides and inventory describe the delivered tools without changing governing doctrine. Coverage: read the committed implementation, correction and recorded results; did not repeat tests, run native Windows, assess the security boundary, or perform signing and joined integration. The earlier Security finding is addressed in the author response.

## Completion -- Codex (Implementation) -- 2026-11-18

The Security finding is closed by `04490e6f`, its passing affected installed
test and the independent ordinary review `129111d7`. No finding remains open.
Earlier passing public checks remain applicable; no clearing review or test
replay is needed. Native Windows, joined integration, certification and trust
operations are not claimed by this record. No implementation follow-up remains.

**Benefit versus cost**: worth it -- adopters receive count verification and
approximate token estimates with editable definitions. This adds four installed
files and one deliberate data exclusion, no external dependency or always-loaded
words. The shared measurement/report implementation range `19406866..4c296221`
changed 30 source, test and guidance files (1,047 insertions, 158 deletions),
excluding deliberation records, board, changelog and installed lock metadata;
those are combined costs, not this feature alone. Runtime and aggregate agent
cost are unknown. Revisit if actual usage does not justify maintaining the tools.
