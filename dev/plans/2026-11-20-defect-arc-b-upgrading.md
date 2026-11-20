# Plan: Defect arc B, upgrading

**Source proposal**: dev/proposals/archive/2026-11-20-claude-v09-defect-arc.md
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-20
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/certifying-runs.md, dev/rules/working-agreements.md, dev/rules/conventions.md, dev/rules/development-environment.md
**In brief**: Fix the defects adopters met when upgrading to 0.8: a Windows clone fails with the wrong error, the security check stops working after the layout move, and a deleted wrapper file cannot be retired.

## Build summary

After this plan, an upgrade from 0.7.0 or 0.8.0 tells the truth when it stops: a Windows clone with changed line endings and a shallow clone each get their own message. The layout move no longer leaves lock keys that disable the security verification, and one new command, `upgrade --heal-layout`, repairs trees that already have them and fixes the `claim_check_command` setting. One new command, `upgrade --retire-wrapper`, retires the record of a vendor wrapper (such as `CLAUDE.md`) that the adopter deleted on purpose. The installer says what to do when the harness folder is missing. Cairn's own repository gains a root `.gitattributes`. The change is in the installer engine; five chunks.

## Source proposal

The Maintainer accepted the defect arc at the heavy tier ("Go ahead on the defect arc.", chat, 2026-11-20). Plan B is its upgrading part: #95, #99.1, #99.3, #99.4, #100, #102, #98.3, and the engine-file comments of #99.5. This plan executes it and reopens nothing. It takes a usual review and a Security Review, at plan stage and again at code stage.

## Scope

**Result.** An upgrade from 0.7.0 or 0.8.0 runs to the end on a test tree, and `run_security_verification.py local` is not left unable to run by it.

Proposed paths:
- `.gitattributes`
- `tests/test_retire_wrapper.py`

| Item | Chunk | Entry point |
|---|---|---|
| #95 parts 1 and 2 (clone error, `.gitattributes`); #98.3 | C1 | `scaffold.py upgrade`, `scaffold.py install` |
| #99.1 lock keys | C2 | `upgrade --stage/--apply`, `--heal-layout` |
| #99.3 shallow; #99.4 stale hash; engine comments; `test_command` | C3 | `upgrade --plan --to` |
| #100 token | C4 | `upgrade --heal-layout` |
| #102 wrapper; #95 part 3 note; notes, changelog, own lock | C5 | `upgrade --retire-wrapper`, `verify_integrity` |

**Where the code differs from the defaults** (read, not run):
1. #99.1: the layout stage reads `layout_base_commit` and `layout_ancestry` from old-path records on its next stage (`_layout_plan`), so the keys must stay there. Only the final stage stops writing them, and the heal skips old-path records.
2. #100: the layout transaction can only create absent files and rewrite the lock and profile (`Transaction._publish`). It cannot re-render `dev/modules/claim-check.md`. The token and its files are fixed by the heal command, not by the move.
3. #102: removing the record is not enough. `_compute_upgrade` adds `VENDOR.md` as a new core file when no record has the source `core/VENDOR.md`. So the record stays, with a new optional key, `adopter_deleted` (additive; no schema bump, per `install/UPGRADE.md`, "Adding a lockfile field without bumping the schema").
4. `templates/skills/_lib/git_read.py` is pinned by hash and is not changed. Shallow detection uses a form it already allows.
5. Plan A left three things here. **Taken**: 14 comment lines in `install/_scaffold/config.py`, `lockfile.py` and `__init__.py` (C3); the stale `test_command` and header comment in `dev/.cairn/profile.yml` (C3); the re-read of the line-ending note in `install/UPGRADE.md` (C5, after plan A's C5). **Not taken**: the one comment in `install/check_module_body_coverage.py`. It is a frozen gate file (`tests/fixtures/gate_manifest.json`, under its pre-layout path), so a comment edit would add a HOLD at the signing. Home: `dev/PLANNING.md`, section 1, "Comments in protected files", where the choice is put to the Maintainer (plan D1 does not edit this file). Docstrings and strings that name old folders stay; editing them changes the AST baseline.
6. #99.4 may not reproduce. C3 says what happens in each case.

**Protected files and the reason the Maintainer will see at the signing.**
- `install/_scaffold/upgrade.py` (engine): the layout move stops writing keys the security verification refuses; new commands repair old trees and retire a deleted wrapper's record.
- `install/_scaffold/cli.py` (engine): the first-install message says what to do when the harness folder is absent.
- `install/_scaffold/config.py`, `lockfile.py`, `__init__.py`: comment text only.
- `install/verify_integrity.py` (frozen in the manifest under its pre-layout path): a missing file is accepted only for a vendor wrapper the adopter retired.
- `.gitattributes` (new, functional configuration): Windows checkouts keep the LF bytes that Cairn's pinned helper and the gate expect.
- `dev/.cairn/profile.yml`: Cairn's own test command names the real folder.
- `dev/.cairn/cairn-lock.yml`: refreshed by the repository's own tool, never by hand.
No dispatcher, `install/scaffold.py` or `git_read.py` change. `config.py` is cascade-mutable (no HOLD).

**Staleness (read, not run).** Four baselined symbols change: `cmd_upgrade`, `_compute_upgrade`, `_cmd_finalize_lockfile` and `main` in `install/_scaffold/cli.py`. The AST baseline then fails `test_ast_attest` until the Maintainer's baseline operation (`release/AST_BASELINE_RUNBOOK.md`; an agent does not perform it). New functions are allowed. After C5 run the runbook's Step 1 listing: any other CHANGED symbol is implementation work. The manifest and roster already name pre-layout paths. The install lock changes only through `--heal-layout` (C5).

**Reuse.** `_layout_render`, `_commit_lock_and_caches`, `_write_by_replacing`, `_writeset_dirty_collisions`, `_resolve_vendor_wrapper`. Searched `install/_scaffold/` for `shallow`, `adopter`, `retire` and `heal`: nothing does these jobs. `_cmd_remove_retired` is for files Cairn stopped shipping and stays unchanged.

**Length.** The plan is well over the word target, because each change carries its exact condition and text for a low-tier implementer. The code review checks them against the code, not against my reading.

### Documentation / doctrine surface

`install/UPGRADE.md` and `CHANGELOG.md`. No doctrine rule changes.

## Sequence

One review point before the end: after C2 (usual and Security), because C4 builds on the heal command and C2 adds a write route into the lock. Code review once more after C5. C1 to C3 need no earlier chunk. C4 needs C2. C5 needs plan A's C5 committed (it edits the same `install/UPGRADE.md`).

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Windows clone, first-launch text | plan review | `.gitattributes`, `_git_read_binding_refusal`, `cli.py` message (#95, #98.3) |
| C2 | Lock keys | C1 | prevention, `--heal-layout` (keys) (#99.1) |
| C3 | Blocks and leftovers | review point 1 | shallow text, stale-hash fix, 14 comments, `profile.yml` (#99.3, #99.4) |
| C4 | The token | C2 | heal rewrites `claim_check_command` and its files (#100) |
| C5 | Wrapper route and records | C3, C4, plan A C5 | `--retire-wrapper`, `verify_integrity`, notes, changelog, own lock (#102, #95 note) |

**Plan E depends on C2 and C3** (same function, `_layout_plan`) and must start after this plan's code review. C4 and C5 do not touch the move.

## Acceptance criteria

**C1.** Root `.gitattributes` is a byte copy of `templates/core/gitattributes.txt`. `git ls-files --eol` shows every tracked text file `i/lf` (measured: 1,106), so nothing is renormalized; `git check-attr eol -- templates/skills/_lib/git_read.py` prints `lf`. New `upgrade.py` function `_git_read_binding_refusal() -> str | None`: calls `_git_read_helper()`; returns `None` if it binds. On `RuntimeError` it reads the helper's own path, built by a new function `_git_read_helper_path()` exactly as `_git_read_helper` builds it (from the `lockfile` module's folder, not from `_cairn_root()`), only after `os.lstat` shows that no part of the path is a link and that the file is regular and at most `_GIT_READ_MAX_BYTES` bytes (import it from `.lockfile`); if any part is a link or the file is not regular or too large, it gives the second text without reading. It returns text only (never file bytes). If the bytes with CRLF folded to LF hash to `_GIT_READ_SHA256` (import it from `.lockfile`): "Cairn's copy of templates/skills/_lib/git_read.py has Windows line endings, so the installer cannot trust it. Git did this when it cloned Cairn with core.autocrlf=true. In the Cairn checkout run `git config core.autocrlf false`, delete that file, and run `git checkout -- templates/skills/_lib/git_read.py`. Then run this command again. A new clone made with `git clone -c core.autocrlf=false` also works." Any other cause: "Cairn's copy of templates/skills/_lib/git_read.py does not match the copy this installer is pinned to (it was edited, is a link, or is another version). Restore it from the Cairn release you are installing from, then run this command again." Used in two places: first statement inside `if not _cairn_is_git(cairn_root):` in `_layout_target` (raise `ScaffoldSecurityError`); and before the `--to <ref> needs a git-checkout` error in `cmd_upgrade` (print `error: <text>`, return 1). `_cairn_is_git` and the binding check itself stay unchanged. In `cli.py` `main`, the `skipped-vendor-absent` branch prints two lines: `  Skills fan-out [<tier>] <name>: not linked yet, because the folder <folder> does not exist.` and `    Create it (`mkdir <folder>`) or let your harness create it, then run `python dev/tools/session.py session-start`; that links the skills.` `<folder>` is the posix parent of the row's `path` from `load_vendor_targets` (import from `.install`), for example `.claude`. The first line holds neither "skipped" nor "error". **Permanent tests**, through `scaffold.main(["upgrade", ...])` in `tests/test_upgrade_layout_migration.py`: monkeypatch `upgrade._git_read_helper` to raise and `upgrade._git_read_helper_path` to a file holding a CRLF copy: exit 2 and the first text. Same with a changed byte: the second text. In `tests/test_first_session_report.py`, change `test_skipped_vendor_absent_is_a_calm_no_action_line` so each `Skills fan-out` line for `claude-code` holds `.claude` and neither "skipped" nor "error", and the whole output holds `session-start`. In `main`, find the row with `row["target"] == name`. **Developmental, on this Windows host, deleted before archive:** `git clone -c core.autocrlf=true` of the starting commit gives CRLF and the first text; a clone of the C1 commit gives LF bytes that hash to `_GIT_READ_SHA256`.

**C2.** In the final stage of `_layout_plan` (`comparison is None`), the record built for a moved file drops `layout_ancestry`, `layout_base_commit` and `layout_fork` (constant `_LAYOUT_LOCK_KEYS`). The reconcile branch keeps writing them, and `layout_keep` on the wrapper stays. New `_layout_heal_findings(lock)` returns the records whose `dst` is not an old path of `_LAYOUT_MOVES` and which carry one of the three keys. New `_cmd_heal_layout(target, lock, force)` and flag `--heal-layout`: removes those three keys from exactly those records, writes the lock with `_commit_lock_and_caches`, prints `Removed layout keys from N lock record(s). Commit dev/.cairn/cairn-lock.yml.` and exits 0; with nothing to do prints `Nothing to heal.` and exits 0. Before writing it asks `_writeset_dirty_collisions` about the lock: unsaved edits refuse with exit 1 unless `--force`; `_EditCheckCannotTell` uses `_cannot_tell_refusal("--heal-layout", reason)`. `--to` is refused as `--remove-retired` refuses it. Wiring: add the flag to the mutually exclusive `actions` list, to both `any(...)` tuples in `_layout_command` (`mutable` and the `return None` list; without them the flag runs a layout plan), and to the profile-link refusal tuple. Plain `--plan`, after the model-selection lines, prints when findings exist: `Run python install/scaffold.py upgrade --target <repo> --heal-layout to remove lock keys the security verification refuses.` Each new command catches `ScaffoldSecurityError` as `--remove-retired` does: `error: upgrade --heal-layout refused (containment): <reason>` (or `--retire-wrapper`), exit 2. **Permanent tests** in `tests/test_upgrade_layout_migration.py`: after stage and apply the moved records carry none of the three keys (update the existing `layout_fork` assertion to check the key is absent and `hash` differs from `base_hash`); a lock with the keys on moved records and on one old-path record is healed so only the moved records change, byte for byte elsewhere; a second run prints `Nothing to heal.`; a dirty lock is refused. The reconcile test (`layout_ancestry` on the old path) stays unchanged. **Developmental:** at the starting commit, a scratch 0.7.0 install taken through both layout stages makes `python dev/tools/run_security_verification.py local` report `unrecognized lockfile-record key(s)`; after C2 it does not.

**C3.** `_cairn_git_is_shallow(root)`: runs `rev-parse --path-format=absolute --git-common-dir` through `_git_read_helper().run_git` (an allowed form), true only if `<that folder>/shallow` is a file; any failure returns false. In `_layout_plan`, where `if not old_proved:` blocks, when `historical is None` and the root is shallow (computed once) the line is `<dst>: unproved ancestry; the Cairn checkout is shallow, so the release this copy came from is not in it`, and one last line is added once: `Fetch the full history in the Cairn checkout (git fetch --unshallow --tags), then run this again.` Otherwise the existing text. #99.4: the reproducing test is a `layout`-fixture variant whose first record has `hash` and `base_hash` set to the digest of the CRLF form of the original bytes while the file holds the original LF bytes: `upgrade --plan --to HEAD`. If it exits 2 with "unproved ancestry" (today's expected result), change `old_proved` to `old_proved = old is not None and rec is not None and ((rec.get("base_hash") or rec.get("hash")) == _layout_digest(old.raw) or (verbatim and live.raw == old.raw))`, and keep the test as permanent: exit 0, action `copy`. If it already exits 0, change no code, record the evidence, and delete the test. A file whose bytes differ from the release stays blocked. Comments: in the 14 `#` lines of `config.py` (41, 97, 967, 1050, 1158, 1245, 1272, 1321, 1346, 1347, 1353, 1354), `__init__.py` (255) and `lockfile.py` (42), replace the old test folder with `tests/`, the old installer folder with `install/`, and the old script folders with `dev/tools/`. Criterion: `ast.dump(ast.parse(...))` is equal before and after for all three files. `profile.yml`: `test_command: "python -m pytest tests"` and `install/scaffold.py` in the header comment. Its lock token keeps the old value (no template renders it; no command changes it). If a selected test that passed at the start fails on this edit, revert it and report. **Permanent tests**: the shallow text, driven by a shallow clone (`git clone --depth 1 file://<path>`; a plain path ignores `--depth`) as the Cairn root; and the stale-hash case.

**C4.** `_layout_heal_findings` also returns tokens: each `(name, value, new)` where `value == "python " + old` for a row of `_LAYOUT_MOVES`, the file `new` has a record, and no record has `old`. `--heal-layout` then sets the token to `"python " + new`. For each non-verbatim record whose saved ancestor (`base_cache`, digest equal to `base_hash`) contains `{{name}}`: it reads the ancestor as `_compute_upgrade` reads a merge ancestor (`_assert_safe_write`, `_read_regular_bytes`, raw digest against `base_hash` before decoding) and the project file with `_assert_safe_write` then `_read_regular_bytes`; on any failure it keeps the file and prints `kept <dst>: could not be read safely; correct it by hand`. Otherwise it renders that ancestor with `_layout_render` under the old and the new tokens, using the matching `LAYOUT_INSTALLS` row's new source. If the file on disk equals the old rendering (or already the new one), it is rewritten with `_write_by_replacing` and its `hash` set. Otherwise it is kept and named: `kept <dst>: you edited it, so it still names the old path; correct it by hand`. Files first, lock last, so a stop leaves a state that a second run finishes. If `dev/.cairn/profile.yml` also holds the old value, print a note to change it there. The final-stage apply message gains `A setting still names a pre-0.8 path; run upgrade --heal-layout.` when findings exist. **Permanent tests**: token and unedited file corrected, edited file kept and named, second run `Nothing to heal.`, a custom token value untouched.

**C5.** `upgrade --retire-wrapper NAME` (`_cmd_retire_wrapper`). Wire it as C2 wires `--heal-layout`: `p.add_argument("--retire-wrapper", default=None, metavar="NAME")`; append `--retire-wrapper` to `actions` when `args.retire_wrapper` is set, as `--adopt-module` is; add `args.retire_wrapper` to both `any(...)` tuples in `_layout_command` and to the profile-link refusal condition; refuse `--to` as `--remove-retired` does. Dispatch it right after the `--finalize` branch of `cmd_upgrade`, with the lock already read, and ask `_writeset_dirty_collisions` about the lock as C2 does. Refuses, exit 1, unless the lock has exactly one record with source `core/VENDOR.md`; exit 2 unless `NAME` is `VENDOR.md`, one of `_KNOWN_VENDOR_WRAPPERS`, or that record's own root-level `dst`; exit 1 if `NAME`, the record's `dst`, or any file `_resolve_vendor_wrapper` finds exists (`os.path.lexists`), or if a link lies above it (`_assert_safe_write`). Otherwise sets `adopter_deleted: true` on that record, writes the lock, and prints `Retired the record of <NAME>: Cairn treats its absence as intended. Commit dev/.cairn/cairn-lock.yml. To bring a wrapper back, restore the file and run upgrade --finalize <NAME>.` Repeating it is exit 0. One rule decides whether a record is a retired wrapper: `_wrapper_retired(rec, files, target)` in `upgrade.py`, repeated inline in `verify_integrity` (which imports only the lockfile reader). All must hold: `rec.get("adopter_deleted") is True`; `rec.get("src") == "core/VENDOR.md"`; `rec.get("verbatim")` is falsy; no other record in `files` has that `src`; `dst` is text with no `/` or `\`, ends in `.md`, and is not `AGENTS.md`, `CHANGELOG.md`, `RULES.md` or `NOTICE.md`; and `os.lstat(target / dst)` raises `FileNotFoundError`. For such a record `_compute_upgrade` returns `up-to-date` (`vendor wrapper deleted on purpose`) before the `layout_keep` check; `_cmd_finalize_lockfile` skips it, and removes the key when its file is present; `_layout_plan` skips its wrapper section; `verify_integrity` skips it after the `living_state` branch and adds `(1 vendor wrapper record retired by the adopter)` to its OK line. `--retire-wrapper` refuses, exit 1, a record failing any part but the `lstat` one. A record with the key that fails the rule is checked like any other. Only the wrapper record's `missing:` line adds `(deleted on purpose? upgrade --retire-wrapper <name>)`, the name through `_plain`. Other missing files still fail. The review-only text for a missing wrapper names the command. **Permanent tests** in `tests/test_retire_wrapper.py`: after retiring, `--plan`, `--finalize` and `verify_integrity` pass; a present modified wrapper still fails; `NAME` of a non-wrapper, a present file, or a lock with no wrapper is refused; a retired record whose file is later restored is checked again. Tampered-lock controls: remove the wrapper record, give a shipped `dev/tools/` script's record `src: core/VENDOR.md` and `adopter_deleted: true` without `verbatim`, delete the script: `verify_integrity` exits 1 naming it `missing:`, and `upgrade --plan` does not call it `up-to-date`. The same for `AGENTS.md`, and for two `core/VENDOR.md` records. `install/UPGRADE.md`: a subsection after the `RULES.md` one for the command; a `--heal-layout` step in plan A's layout section; the Cairn-checkout note replaced by the new message and the `.gitattributes`; one sentence on shallow clones. `CHANGELOG.md`: one Minor entry. Then `upgrade --heal-layout --target .` on Cairn's own tree, its lock committed alone.

**Security (re-answered).** S1: the checkout's helper bytes, the lock and the saved ancestors come from the thing judged; messages use fixed words and never echo them, and unreadable input is skipped and named. S2: negative controls are the C1 refusals, the C2 old-path record kept, the C4 edited file kept and the C5 refusals. S3: `upgrade --plan`, `--heal-layout`, `--finalize`, `verify_integrity` and `run_security_verification.py local` fire the checks. S4: two routes add authority and are adopter-run: the heal removes only three named keys and rewrites unedited files; the retire sets one key on the wrapper record, only when the file is absent. S5: someone who writes the lock can retire the record of a missing wrapper only when it passes `_wrapper_retired` (source `core/VENDOR.md`, unique, not verbatim, a root-level `.md` name other than `AGENTS.md`, `CHANGELOG.md`, `RULES.md` and `NOTICE.md`); that hides only a deleted vendor wrapper, and a record moved onto any other file is still reported missing.

## Scope delta

**Scope delta**: preserved. Every outcome the proposal assigns to plan B is delivered. The one comment in `install/check_module_body_coverage.py` was never plan B's item.

## Verification

**Selector.** `tests/conftest.py` refuses any one run over 40 test files, so the 102-file selection is not run here; the arc's joined run owns it. Each chunk makes one pytest call of at most 40 files: the tests it adds or edits plus `tests/tier_inventory.py for` the one engine file it changes. C1: `install/_scaffold/cli.py` (15 files) plus `tests/test_upgrade_layout_migration.py` and `tests/test_first_session_report.py`. C2, C3 and C4: `install/_scaffold/upgrade.py` (38 files). C5: `install/verify_integrity.py` (18 files) plus `tests/test_retire_wrapper.py`, `tests/test_upgrade_layout_migration.py` and `tests/test_upgrade_side_door_parity.py`. C3's comment edits run no selection (the AST-equality check covers them); for `profile.yml` run `tests/test_intents_tool.py`, `tests/test_security_verification.py` and `tests/test_session_writes_contained.py`, the three of its 65 selected files that build paths from the repository root (found by grep). Before C1, make each call at the starting commit with `-rf` and keep every failing test id with its first message line. After a chunk, a failure is a host failure only if the same id and the same message are on that list; any other is reported. Left to the joined run: the 102-file selection, the Python 3.13 run, and `tests/test_ast_attest.py` (red until the Maintainer's baseline step).

**Hosts.** This Windows machine: the selected tests, the C1 clone checks and the first-launch message (Windows behaviours). Its Linux subsystem (Python 3.14.4; development checks only): the layout, heal and retire tests once, for file modes and links. The one end-to-end check, on either host and not in the permanent tests: upgrade scratch installs from `v0.7.0` and `v0.8.0`, then `run_security_verification.py local` must report no DEGRADED for a lock key. Canonical runtime (`dev/rules/certifying-runs.md`): nothing here certifies. The Python 3.13 full run waits for the arc's joined run.

**Prose gates**, one file per call: `dev/tools/claim_check.py`, `dev/tools/link_check.py`, `tests/check_cairn.py`, and `git diff --check` on each changed `.md`. Then the Step 1 listing of `release/AST_BASELINE_RUNBOOK.md`.

**Issues, for the Maintainer.** Nobody closes or comments on any: #95 (all three parts after C5), #98 (part 3 only), #99 (parts 1, 3, 4 and the engine comments; part 2 is plan A's), #100, #102.

**Not checked.** No code or test was run for this plan. Not measured: Windows behaviour; `--path-format` on a Git older than 2.31; whether a selected test ties `profile.yml` to the lock; whether a release-membership test lists root files, which would need `.gitattributes` named. Other callers of `_git_read_helper` keep the old wording. **Does any rule weaken or disappear?** No: no rule text is edited.

## Plan review -- Claude Sonnet 5.5 (`claude-sonnet-5-5`, usual reviewer) -- 2026-11-20

```
Reviewed commit: 02f92d370067ce5ba2d9d1b5ad62d554abeaccda
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised
**Verdict**: REVISE

The plan turns five upgrade defects into small, tested engine changes. The design holds: the three layout keys are dropped where written, `adopter_deleted` is the smallest way to keep a retired wrapper from being re-added (`upgrade.py:1054`), and each added command earns its place. Four gaps would make a low-tier implementer invent or stall.

**Foundations**

1. **Should this happen as framed?** Yes. Every proposal item for plan B is carried; the two commands deliver "heal" and "documented route" -- appendix rows #99.1, #102; `upgrade.py:4395`.
2. **Best alternative.** Treating an absent wrapper like `RULES.md` (`upgrade.py:979`) is smaller but lets `verify_integrity` pass silently; the explicit key keeps a reviewable lock edit -- `verify_integrity.py:462`.
3. **What would show it wrong.** After C2, a 0.7.0 scratch install still prints `unrecognized lockfile-record key(s)`; or `--retire-wrapper` then `--stage` re-adds `VENDOR.md` -- the C2 and C5 permanent tests.

**Does any rule weaken or disappear?** No.

**Findings**

1. **Blocking.** The 102-file run cannot execute: `tests/conftest.py` refuses over 40 files. Words: block V below.
2. **Blocking.** C5 never says how `--retire-wrapper NAME` is wired, and C2's `--plan` line has no text. Words: block W.
3. **Blocking.** C1's test edit would fail. The test is in `tests/test_first_session_report.py`, and it reads only lines containing "Skills fan-out", so `session-start` on the second line is never seen. Words: block X.
4. **Blocking.** C3's `old_proved` clause crashes when `old` is `None`. Words: block Y.
5. Non-blocking. The shallow test needs `git clone --depth 1 file://<path>`; a plain path ignores `--depth`.
6. Non-blocking, for the Security pass. `verify_integrity` should skip a record only when its `dst` has no `/`; the binding check should use `_GIT_READ_MAX_BYTES`, not a literal.
7. Non-blocking. The `test_command` default (leave the lock token) is right: no code reads it, and changing it edits a protected lock. It is the plan's call, not the Maintainer's; the plan raises no question.
8. Non-blocking. Keep one plan. The review point after C2 is the right place and enough, since only C4 builds on C2.

**Not covered.** I ran no test, installer command or Windows check. I did not trace `_layout_render` returns of `None` in C4, whether a root `.gitattributes` trips a release-membership test, or `--path-format` on old Git. Over the 300-word target because of four blocking findings.

**Elapsed**: about 40 minutes. **Tokens**: unknown.

### Exact words for the plan review above

**V (replace the whole Selector paragraph).** "**Selector.** `tests/conftest.py` refuses any one run over 40 test files, so the 102-file selection is not run here; the arc's joined run owns it. Each chunk makes one pytest call of at most 40 files: the tests it adds or edits plus `tests/tier_inventory.py for` the one engine file it changes. C1: `install/_scaffold/cli.py` (15 files) plus `tests/test_upgrade_layout_migration.py` and `tests/test_first_session_report.py`. C2, C3 and C4: `install/_scaffold/upgrade.py` (38 files). C5: `install/verify_integrity.py` (18 files) plus `tests/test_retire_wrapper.py`, `tests/test_upgrade_layout_migration.py` and `tests/test_upgrade_side_door_parity.py`. C3's comment edits run no selection (the AST-equality check covers them); for `profile.yml` run `tests/test_intents_tool.py`, `tests/test_security_verification.py` and `tests/test_session_writes_contained.py`, the three of its 65 selected files that build paths from the repository root (found by grep). Before C1, make each call at the starting commit with `-rf` and keep every failing test id with its first message line. After a chunk, a failure is a host failure only if the same id and the same message are on that list; any other is reported. Left to the joined run: the 102-file selection, the Python 3.13 run, and `tests/test_ast_attest.py` (red until the Maintainer's baseline step)."

**W (add to C5, after its first sentence; and to C2 after "Plain `--plan`").** C5: "Wire it as C2 wires `--heal-layout`: `p.add_argument("--retire-wrapper", default=None, metavar="NAME")`; append `--retire-wrapper` to `actions` when `args.retire_wrapper` is set, as `--adopt-module` is; add `args.retire_wrapper` to both `any(...)` tuples in `_layout_command` and to the profile-link refusal condition; refuse `--to` as `--remove-retired` does. Dispatch it right after the `--finalize` branch of `cmd_upgrade`, with the lock already read, and ask `_writeset_dirty_collisions` about the lock as C2 does." C2: "Plain `--plan`, after the model-selection lines, prints when findings exist: `Run python install/scaffold.py upgrade --target <repo> --heal-layout to remove lock keys the security verification refuses.`"

**X (replace C1's test sentence).** "In `tests/test_first_session_report.py`, change `test_skipped_vendor_absent_is_a_calm_no_action_line` so each `Skills fan-out` line for `claude-code` holds `.claude` and neither "skipped" nor "error", and the whole output holds `session-start`. In `main`, find the row with `row["target"] == name`."

**Y (replace the `old_proved` change).** "`old_proved = old is not None and rec is not None and ((rec.get("base_hash") or rec.get("hash")) == _layout_digest(old.raw) or (verbatim and live.raw == old.raw))`."

## Plan review -- Claude Opus 5.5 (`claude-opus-5-5`, Security Review) -- 2026-11-20

```
Reviewed commit: d087d2fc9346aabc83561292ba7e80f5039ab3e0
```

**Obligation**: Internal Security Review (heavy tier, plan stage)
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE

The plan repairs upgrades without widening the dispatcher: its record-key list stays as it is (`run_security_verification.py:136`), so the heal removes keys and adds none. One opt-out trusts the lock it should judge.

**Foundations**

1. **Should this happen as framed?** Yes, once the wrapper opt-out is bound to the wrapper -- `run_security_verification.py:504`; appendix row #102.
2. **Best alternative.** The `RULES.md` exemption binds source, destination and `lstat` absence; copy that shape -- `upgrade.py:983`.
3. **What would show it wrong.** A lock that moves `adopter_deleted` onto a deleted script passes `verify_integrity` -- the Z2 test.

**Findings**

1. **Blocking.** C5 honors `adopter_deleted` on the lock's `src` alone. The lock is a tamper target (`verify_integrity.py:439`), so an edited record can hide any deleted file, a security runner included, from both the verifier and the upgrade. S5 is untrue until this closes. Words: Z1. Mine governs over finding 6 of the usual review: "no `/`" alone still lets `AGENTS.md` go.
2. **Blocking.** No negative control exercises a tampered lock; the C5 refusals test only the command, which a lock edit bypasses. Words: Z2.
3. **Blocking.** C4 reads a saved ancestor and a project file at paths the lock names, without saying through which reader; nor do the new commands say how a containment refusal exits. Words: Z3.
4. Non-blocking. C1's diagnosis reads `_cairn_root()`, which follows links; `_git_read_helper` refuses them (`lockfile.py:57`). Build the helper's own path and give the first text only when no part is a link. Use `_GIT_READ_MAX_BYTES`: agreed.
5. Non-blocking, checked. #99.4's equality proof uses a blob from Cairn's own history (`upgrade.py:4183`), stronger than the lock hash; the shallow text changes words only and blocks as before; dropping `layout_ancestry` loses nothing, since only `upgrade.py:4273` reads it, on records the heal skips.

I agree with V, W, X, Y and findings 7 and 8: keep one plan.

**Not covered.** No test, installer or Windows run; `_lock_record_identity` and staged-apply evidence with the new key; `_run_slot_note` on a retired record. Over target for three blocking findings.

**Elapsed**: about 35 minutes. **Tokens**: unknown.

### Exact words for the Security Review above

**Z1 (replace C5's sentence beginning "Honoring the key needs all of:" through "says so in its OK line.")** "One rule decides whether a record is a retired wrapper: `_wrapper_retired(rec, files, target)` in `upgrade.py`, repeated inline in `verify_integrity` (which imports only the lockfile reader). All must hold: `rec.get("adopter_deleted") is True`; `rec.get("src") == "core/VENDOR.md"`; `rec.get("verbatim")` is falsy; no other record in `files` has that `src`; `dst` is text with no `/` or `\`, ends in `.md`, and is not `AGENTS.md`, `CHANGELOG.md`, `RULES.md` or `NOTICE.md`; and `os.lstat(target / dst)` raises `FileNotFoundError`. For such a record `_compute_upgrade` returns `up-to-date` (`vendor wrapper deleted on purpose`) before the `layout_keep` check; `_cmd_finalize_lockfile` skips it, and removes the key when its file is present; `_layout_plan` skips its wrapper section; `verify_integrity` skips it after the `living_state` branch and adds `(1 vendor wrapper record retired by the adopter)` to its OK line. `--retire-wrapper` refuses, exit 1, a record failing any part but the `lstat` one. A record with the key that fails the rule is checked like any other. Only the wrapper record's `missing:` line adds `(deleted on purpose? upgrade --retire-wrapper <name>)`, the name through `_plain`."

**Z2 (add to C5's permanent tests).** "Tampered-lock controls: remove the wrapper record, give a shipped `dev/tools/` script's record `src: core/VENDOR.md` and `adopter_deleted: true` without `verbatim`, delete the script: `verify_integrity` exits 1 naming it `missing:`, and `upgrade --plan` does not call it `up-to-date`. The same for `AGENTS.md`, and for two `core/VENDOR.md` records."

**Z3 (add to C4 after "contains `{{name}}`"; and to W).** C4: "It reads the ancestor as `_compute_upgrade` reads a merge ancestor (`_assert_safe_write`, `_read_regular_bytes`, raw digest against `base_hash` before decoding) and the project file with `_assert_safe_write` then `_read_regular_bytes`; on any failure it keeps the file and prints `kept <dst>: could not be read safely; correct it by hand`." W: "Each new command catches `ScaffoldSecurityError` as `--remove-retired` does: `error: upgrade --heal-layout refused (containment): <reason>` (or `--retire-wrapper`), exit 2."

## Plan response -- Claude Sonnet 5.5 (`claude-sonnet-5-5`, for the author) -- 2026-11-20

Both reviews said REVISE. Every blocking finding is applied with its reviewer's exact words; where the two touch the same point, the Security Review governs. Status is now `ready-to-implement`.

**Usual review**

1. Blocking (V): accepted; the Selector paragraph in Verification is replaced.
2. Blocking (W): accepted; C5's wiring sentences follow its first sentence, and C2's `--plan` line replaces "Plain `--plan` ends with one line...".
3. Blocking (X): accepted; replaces C1's test sentence.
4. Blocking (Y): accepted; the `old_proved` expression is in C3.
5. Non-blocking, shallow test: applied (`file://<path>`, C3).
6. Non-blocking: the "no `/`" test gives way to Z1; `_GIT_READ_MAX_BYTES` is in C1.
7 and 8: no change asked.

**Security Review**

1. Blocking (Z1): accepted; it replaces C5's "Honoring the key..." sentences.
2. Blocking (Z2): accepted; added at the end of C5's permanent tests.
3. Blocking (Z3): accepted; in C4 after "contains `{{name}}`", and in C2 after the `--plan` line (it covers both commands).
4. Non-blocking: applied in C1 (helper's own path, no link in any part).
5. Informational, no change.

**Consistency changes**

- C1 test sentence: the patch point `upgrade._cairn_root` became `upgrade._git_read_helper_path`, because the diagnosis no longer reads `_cairn_root()`. The function name is mine; the reviewer gave no name.
- C4: "contains `{{name}}`, it renders" became a colon plus Z3's words plus "Otherwise it renders".
- C5: "and `verify_integrity`'s `missing:` line name the command" shortened, because Z1 now words that line.
- S5 rewritten; the Security Review calls the old sentence untrue.
- Table and Build summary unchanged (command count is the same).

**Left for the code review**: nothing. Could not apply exactly: nothing.

Not checked: no code or test run; the new function's name and the `_wrapper_retired` details against the code.

**Elapsed**: about 15 minutes. **Tokens**: unknown.
