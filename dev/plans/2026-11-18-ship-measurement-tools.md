# Plan: Ship measurement tools

**Source proposal**: `dev/proposals/archive/2026-11-18-terra-ship-measurement-tools.md`
**Status**: awaiting-plan-review
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

The registry is an object keyed by whole `[\w-]+` names. Each value is exactly either `{"kind":"snapshot","value":<nonnegative integer>,"as_of":"YYYY-MM-DD"}` or `{"kind":"invariant","fn":<operation>,"target":<string>,"root":<project-relative directory>}`; root may be omitted for the project root. Operations are `count_lines`, `count_files`, `count_defs`, and `git_commits_in_range`. Reject duplicate keys at every object level, unknown fields, wrong types (including booleans as integers), invalid dates and unsupported operations. No executable definitions. Annotation parsing treats every HTML comment starting with optional whitespace and `verify:` as an attempted marker, rejecting malformed or unclosed markers and missing preceding same-line numbers. Snapshot dates must appear on the line.

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

**C1.** Installed `token_budget.py` works from outside the project for detected and explicit files, labels its approximation in text and JSON, warns by default and fails strict caps. Installed `verify_counts.py` reads only the fixed JSON registry and verifies snapshots and all four operations. It refuses malformed or unclosed markers, a dotted key in either input, invalid definitions, unknown keys, escapes and changed helper bytes; reports zero, drift and skips with the specified statuses. Git accepts a valid range and fails a missing range even when a same-named file exists. Existing internal entry points and definitions remain usable.

**C2.** Public install places each file under its named module. Upgrade preserves an edited registry and verifies it as mergeable data, while changed shipped Python fails integrity. Existing collision/customization protection remains. The guides show registry syntax, key-only markers, zero checks, malformed markers, skips, reviewed definitions, approximate estimates, caps and Git requirements. Inventory and release records match the delivered paths.

**C3.** Public installed commands, installer, upgrade and integrity checks demonstrate C1 and C2 with both positive and negative controls, including root containment before skip, direct and child-link escape, exact Git worktree root and revision-only behavior. Run both commands from outside a disposable install. Add permanent checks only for public promises; remove developmental probes before archive. Record coverage and omissions.

## Scope delta

**Scope delta**: preserved.

## Verification

Before implementation run `python tests/tier_inventory.py for <changed paths>` and run only mapped tests, plus applicable prose gates. Map the installed command cases into `tests/test_verify_counts.py`, install and integrity cases into `tests/test_manifest.py`, and preservation into `tests/test_upgrade_module_additions.py`; use the public entry points. For security negative controls, mutate a count, use an unknown key and escaping targets, and alter the pinned helper; pair each refusal with a valid control. Check that registry edits pass integrity while support edits fail. Run claim, link, snippet and neutrality gates for prose and applicable release gates. Use `/Users/kendal30/conda_envs/lhm/bin/python3.13` and record results and limits. Independent scientific check: N/A, as accepted. Independent ordinary and Security code reviews remain required. Record benefit versus cost and any separate human operation's unpassed evidence before archive.
