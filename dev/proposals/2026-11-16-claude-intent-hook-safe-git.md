# The intent hook installer finds Git the safe way

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: light — a small, reversible defect repair that narrows an existing trust gap; the Maintainer sets the tier.
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-11-16
**In brief**: The opt-in command that installs Cairn's Git hooks should find Git the same careful way Cairn's other tools do, so a planted fake `git` cannot run; a related small fix makes two checks fail cleanly instead of with a traceback.

## Decision summary

Cairn's other tools find Git through a safe reader that picks one real Git program and ignores a repository's own files. One function in the hook installer does not: `_git_hooks_path` runs plain `git` found through `PATH`, so a fake `git` in the repository can run when someone installs the hook. Only people who run `install-hook`, `install-precommit` or their uninstall forms are exposed. I recommend fixing it: pick Git with the safe reader's `select_git`, run it ourselves with a cleaned environment, and still honor `core.hooksPath`. Cost (my estimate): about 25 changed lines in two byte-identical files and a few new test cases. I also recommend fixing the second finding here: two Markdown checks should print their refusal and exit 2, not crash with a traceback.

## Context

- `_git_hooks_path` in `tools/_intent/hooks.py` (line 310; the twin `templates/modules/team-gated/_intent/hooks.py` is byte-identical, checked with `diff`) runs `["git", "rev-parse", "--git-path", "hooks"]` with `cwd=toplevel`. `_cmd_install_hook` (line 138) and `_resolve_hooks_dir` (line 300) call it.
- The safe reader (`tools/git_read.py`, `select_git`, line 460) takes the first absolute `PATH` entry that holds Git and skips relative entries. Plain `git` has no such rule: with `.` or an empty entry on `PATH`, the child looks in the repository root first. The board row (`dev/PLANNING.md`, item 30) says a job reproduced this with `.` first on `PATH`. I did not reproduce it; I read the code and the row.
- The function's docstring calls the plain call an exception, because the safe reader's `run_git` cannot answer this question. Read from `tools/git_read.py` lines 568 and 488, not run: every call it makes forces `core.hooksPath` to the null device and blanks the global and system config, so `--git-path hooks` would return the null device instead of the real folder.
- The archived safe-Git plan (`dev/plans/archive/2026-11-06-safe-git-reads.md`, lines 33 and 1297) says "hooks-path installation" stays outside the ordinary-reader change. So the plan carved this call out; it did not promise to route it later. Whether any review examined the plain `PATH` lookup itself I did not check.
- The test file added in `3184f6c7` (`bootstrap/tests/security/test_git_read_routes.py`, lines 400-430) covers `install-hook` only when the safe reader refuses at the earlier `--show-toplevel` step. It does not cover a planted relative `git` while the safe reader succeeds.
- Second finding: `_tracked_index_paths` raises `RuntimeError` in `scripts/link_check.py` (line 807) and `scripts/sync_doc_snippets.py` (line 363). Their `main` functions call `tracked_markdown` with no handler (`link_check.py` line 985, `sync_doc_snippets.py` line 426), so a refused read ends in a traceback and exit 1, the same code as ordinary findings. `scripts/check_cairn.py` (line 675) already catches it. Both files have byte-identical twins under `templates/modules/team-gated/`.

## Proposal

**A. Hook installer.** In both copies of `hooks.py`, `_git_hooks_path` asks the pinned helper (`_git_read()`, already loaded and hash-checked by `conflict.py`) for `select_git(toplevel)`. If it returns nothing, the function returns `None`, which the callers already report as "could not resolve the git hooks directory". Otherwise it runs that absolute program with `-C toplevel`, a minimal environment (empty `PATH`, no inherited `GIT_*` variables, `stdin` closed, the existing 10-second timeout) and the same `--git-path hooks` question. The user's global Git config stays visible, so `core.hooksPath` is honored as Git itself would honor it at commit time. `tools/git_read.py` is not changed: it is hash-pinned, and a new helper form would be a much larger heavy change.

**B. Markdown checks.** In the four `main` functions (two copies each of `link_check.py` and `sync_doc_snippets.py`), catch `RuntimeError` around file discovery, print `<tool>: <message>` to stderr and return 2, the code those tools already use for "cannot run". A refused read stays a failure and never reads as clean.

**Not changed.** `_git_path` and the other safe-reader calls; `core.hooksPath` pointing outside the repository (see Residual risk).

## Rationale

Exposure and attacker need. Only a person who runs `install-hook`, `install-precommit` or an uninstall command is exposed. The attacker needs three things: an executable named `git` in the repository root, a victim who works in that repository, and a `PATH` that lets the child find it (`.` or an empty entry on POSIX, which is unusual; on Windows the search also begins in the parent's current folder, per the row). Victim and planted file together describe a cloned hostile repository, which is what the safe reader exists for.

Why fix, not document. The safe reader's promise is that Cairn never runs a repository-supplied `git`; this call is the one known place it does. Fixing adds no new trust; documenting leaves a known hole in a command that writes executable hooks.

Residual risk, stated plainly. (1) A hostile repository's own `.git/config` can still set `core.hooksPath`, so install can write a hook where the attacker chose; this existed before and is not a `PATH` issue. I propose to leave it, and ask below. (2) If the user's own `PATH` or environment is already hostile, nothing here defends it. (3) Global Git config is trusted because it is the user's.

Tier and review. `dev/agent_collaboration.md` line 371 sends named high-risk surfaces and widened boundaries to heavy. `hooks.py` is not on the named list in `dev/rules/protected-surfaces.md` and this change narrows a boundary, so light is defensible. It starts a program and is an installed-engine file the row says joins the pending AST re-anchor, so I keep `usual + Security Review` as the row asks, as one Security pass.

## Alternatives considered

1. **Document the exception.** Cheapest now, but it leaves the row's reproduced attack open; lost.
2. **Call `run_git` as is.** Rejected: it would return the null device (see Context), silently dropping `core.hooksPath`.
3. **Add a hooks-path form to `git_read.py`.** Most uniform, but it changes a hash-pinned helper and its copy; lost on cost.
4. **Leave B for later.** A traceback is not unsafe, but later means a second lockfile pass for four small edits.

## Documentation / doctrine surface

No doctrine or `docs/` change. The `hooks.py` docstring is rewritten to say the call now uses the safe executable choice. The archived safe-Git plan is immutable and is not touched.

## Evidence / verification plan

### Tests required

- Promise: with `.` first on `PATH` and a planted `git` at the repository root, `install-hook` and `install-precommit` run no repository program and still install. Public entry: `intent.py install-hook` in `test_git_read_routes.py` (new case beside lines 400-430), failing when plain `git` is restored.
- Promise: `core.hooksPath` still decides the folder. One case sets it in local config and checks the hook lands there.
- Promise: when `select_git` finds nothing, install refuses without writing.
- Promise: `link_check.py` and `sync_doc_snippets.py` exit 2 with no traceback on a refused read; the existing parametrized case (line 307) tightens from `!= 0` to `== 2`.
- Gates: `tools/test_tiers.py for <changed paths>` and `scripts/check_cairn.py`; no suite run. Windows is not covered: the file skips there (see the board row "Run the per-route safe-Git checks on Windows").

### Security preflight

- **S1**: Inputs are the `PATH` and the repository's files, both supplied by the thing being decided about; the fix drops both from Git selection.
- **S2**: The new case fails if plain `git` returns.
- **S3**: `install-hook`, `install-precommit` and uninstall; every path through `_git_hooks_path`.
- **S4**: Failure returns `None` and install refuses: less authority.
- **S5**: A hostile `.git/config` `core.hooksPath` still wins; closed by enumeration, not construction.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

`core.hooksPath` no longer honored; install failing for people whose Git sits only in a relative `PATH` entry; or any Windows report that `select_git` cannot find Git.

## Scope delta

**Scope delta**: preserved. Nothing from the board row is dropped.

## Assurance path

**Assurance path**: high-assurance — adopters execute the installed hook and tools.
