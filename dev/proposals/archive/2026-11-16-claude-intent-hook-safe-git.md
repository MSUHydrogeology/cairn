# The intent hook installer finds Git the safe way

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: light — a small, reversible defect repair that narrows an existing trust gap; the Maintainer sets the tier.
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-11-16
**In brief**: The opt-in command that installs Cairn's Git hooks should find Git the same careful way Cairn's other tools do, so a planted fake `git` cannot run; a related small fix makes two checks fail cleanly instead of with a traceback.

## Decision summary

Cairn's other tools find Git through a safe reader that picks one real Git program and ignores a repository's own files. One function in the hook installer does not: `_git_hooks_path` runs plain `git` found through `PATH`, so a fake `git` in the repository can run when someone installs the hook. Only people who run `install-hook`, `install-precommit` or their uninstall forms are exposed. I recommend fixing it: pick Git with the safe reader's `select_git`, run it ourselves with a cleaned environment, and still honor `core.hooksPath`. Cost (my estimate): about 25 changed lines in two byte-identical files and a few new test cases. Five files frozen in the gate manifest change (the shipped copy of `hooks.py`, and both Markdown checkers with their shipped copies; `tools/_intent/hooks.py` itself is not frozen), and new cases in the hash-pinned `test_git_read_routes.py` change the manifest's recorded test IDs, so the Maintainer's gate re-anchor follows. I also recommend fixing the second finding here: two Markdown checks should print their refusal and exit 2, not crash with a traceback.

## Context

- `_git_hooks_path` in `tools/_intent/hooks.py` (line 310; the twin `templates/modules/team-gated/_intent/hooks.py` is byte-identical, checked with `diff`) runs `["git", "rev-parse", "--git-path", "hooks"]` with `cwd=toplevel`. `_cmd_install_hook` (line 138) and `_resolve_hooks_dir` (line 300) call it.
- The safe reader (`tools/git_read.py`, `select_git`, line 460) takes the first absolute `PATH` entry that holds Git and skips relative entries. Plain `git` has no such rule: with `.` or an empty entry on `PATH`, the child looks in the repository root first. The board row (`dev/PLANNING.md`, item 30) says a job reproduced this with `.` first on `PATH`. I did not reproduce it; I read the code and the row.
- The function's docstring calls the plain call an exception, because the safe reader's `run_git` cannot answer this question. Read from `tools/git_read.py` lines 568 and 488, not run: every call it makes forces `core.hooksPath` to the null device and blanks the global and system config, so `--git-path hooks` would return the null device instead of the real folder.
- The archived safe-Git plan (`dev/plans/archive/2026-11-06-safe-git-reads.md`, lines 33 and 1297) says "hooks-path installation" stays outside the ordinary-reader change. So the plan carved this call out; it did not promise to route it later. Whether any review examined the plain `PATH` lookup itself I did not check.
- The test file added in `3184f6c7` (`bootstrap/tests/security/test_git_read_routes.py`, lines 400-430) covers `install-hook` only when the safe reader refuses at the earlier `--show-toplevel` step. It does not cover a planted relative `git` while the safe reader succeeds.
- Second finding: `_tracked_index_paths` raises `RuntimeError` in `scripts/link_check.py` (line 807) and `scripts/sync_doc_snippets.py` (line 363). Their `main` functions call `tracked_markdown` with no handler (`link_check.py` line 985, `sync_doc_snippets.py` line 426), so a refused read ends in a traceback and exit 1, the same code as ordinary findings. `scripts/check_cairn.py` (line 675) already catches it. Both files have byte-identical twins under `templates/modules/team-gated/`.

## Proposal

**A. Hook installer.** In both copies of `hooks.py`, `_git_hooks_path` asks the pinned helper (`_git_read()`, already loaded and hash-checked by `conflict.py`) for `select_git(toplevel)`. If it returns nothing, or raises its refusal for an unsafe Git (a `RuntimeError`, which today's handler does not catch), the function returns `None`, which the callers already report as "could not resolve the git hooks directory". Otherwise it runs that absolute program with `-C toplevel`, the same `--git-path hooks` question and a named minimal environment (`stdin` closed, the existing 10-second timeout). Passed through: `HOME` and `XDG_CONFIG_HOME`, and on Windows `USERPROFILE`, `HOMEDRIVE`, `HOMEPATH` and `SystemRoot`. Stripped: `PATH` and every `GIT_*` variable, including `GIT_DIR`, `GIT_EXEC_PATH` and `GIT_CONFIG_*`. `GIT_CONFIG_NOSYSTEM` is not set, so a system-wide `core.hooksPath` still counts. The reviewer measured that with no `HOME` a global `core.hooksPath` is silently ignored, which is why the list is explicit; the Windows variables are not checked. The user's global Git config stays visible, so `core.hooksPath` is honored as Git itself would honor it at commit time. `tools/git_read.py` is not changed: it is hash-pinned, and a new helper form would be a much larger heavy change.

**B. Markdown checks.** In the four `main` functions (two copies each of `link_check.py` and `sync_doc_snippets.py`), catch `RuntimeError` around file discovery, print `<tool>: <message>` to stderr and return 2, the code those tools already use for "cannot run". Their docstrings define exit 2 as "usage error" (`link_check.py` line 53); the same edit widens that wording.

**C. Refuse a linked hook file.** Before it writes, the installer refuses if the hook file is a symbolic link, with a message. Today the write follows the link, so a hooks folder chosen by a repository's own config can send the write outside the repository (the Security Review reproduced this with today's code). Cost: a project that deliberately links its hook file to a tracked script is refused and must install by hand. A refused read stays a failure and never reads as clean.

**Not changed.** `_git_path` and the other safe-reader calls; `core.hooksPath` pointing outside the repository (see Residual risk).

## Rationale

Exposure and attacker need. Only a person who runs `install-hook`, `install-precommit` or an uninstall command is exposed. The attacker needs three things: an executable named `git` in the repository root, a victim who works in that repository, and a `PATH` that lets the child find it (`.` or an empty entry on POSIX, which is unusual; on Windows the search also begins in the parent's current folder, per the row). Victim and planted file together describe a cloned hostile repository, which is what the safe reader exists for.

Why fix, not document. The safe reader's promise is that Cairn never runs a repository-supplied `git`; this call is the one known place it does. Fixing adds no new trust; documenting leaves a known hole in a command that writes executable hooks.

Residual risk, stated plainly. (1) A hostile repository's own `.git/config` can still set `core.hooksPath`, so install can write a hook where the attacker chose; this existed before and is not a `PATH` issue. Writes there follow links today; item C refuses a linked hook file. The folder choice itself is left alone: a containment check would break a legitimate hooks folder outside the repository, such as a global `~/.githooks`. (2) If the user's own `PATH` or environment is already hostile, nothing here defends it. (3) Global Git config is trusted because it is the user's.

Tier and review. `dev/agent_collaboration.md` line 371 sends named high-risk surfaces and widened boundaries to heavy. `hooks.py` is not on the named list in `dev/rules/protected-surfaces.md` and this change narrows a boundary, so light is defensible. It starts a program and is an installed-engine file the row says joins the pending AST re-anchor, so I keep `usual + Security Review` as the row asks, as one Security pass.

## Alternatives considered

1. **Document the exception.** Cheapest now, but it leaves the row's reproduced attack open; lost.
2. **Call `run_git` as is.** Rejected: it would return the null device (see Context), silently dropping `core.hooksPath`.
3. **Add a hooks-path form to `git_read.py`.** Most uniform, but it changes a hash-pinned helper and its copy; lost on cost.
4. **Leave B for later.** A traceback is not unsafe, but later means a second lockfile pass for four small edits.

## Documentation / doctrine surface

No doctrine or `docs/` change. The `hooks.py` docstring is rewritten to say the call now uses the safe executable choice. It keeps the sentence that this call is "not used for repository inspection or hook execution", and names the residual: the repository's local config is still read. The archived safe-Git plan is immutable and is not touched.

## Evidence / verification plan

### Tests required

- Promise: with `.` first on `PATH` and a planted `git` at the repository root, `install-hook` and `install-precommit` run no repository program and still install. Public entry: `intent.py install-hook` in `test_git_read_routes.py` (new case beside lines 400-430), failing when plain `git` is restored.
- Promise: `core.hooksPath` still decides the folder. One case sets it in local config and checks the hook lands there.
- Promise: a global `core.hooksPath` set under a temporary `HOME` still decides the folder.
- Promise: a hook file that is a link is refused and nothing is written.
- When `select_git` finds nothing or refuses, install reports and writes nothing. This cannot be reached through the command, because an earlier check refuses first, so it is tested at the function, marked as an internal case.
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

## Review -- Claude Sonnet 5.5 (ordinary Reviewer, Medium) -- 2026-11-16

```
Reviewed commit: dae317c8e839ce14cf97b36b7039c68ea314ac79
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Elapsed**: about 5 minutes (11:54:15 to 11:59:03, `date`)
**Tokens**: unknown

The strongest case: Cairn promises that no repository-supplied program runs, this is the one known place that breaks it, and the draft closes it without touching the hash-pinned helper.

**Foundations**

1. **Should this happen as framed?** Yes, as a small repair, not a contract change. The defect is real (I reproduced it: with `.` first on `PATH`, a `git` at a scratch repo's root ran during `intent.py install-hook`). The helper cannot answer the question: `run_git(repo, ("rev-parse","--git-path","hooks"))` returned `/dev/null` with a local `core.hooksPath` set, while plain Git returned the real folder. `select_git` is public and already used by `bootstrap/_scaffold/lockfile.py` line 163. -- `tools/git_read.py` lines 460, 488, 568; `dev/proposals/archive/2026-11-04-codex-safe-git-reads.md` line 84 (the accepted text set this query apart)
2. **Best alternative.** The draft's own pick; documenting loses because the attack reproduces, and a new helper form (alternative 3) is a contract change. -- Alternatives 1-3
3. **What would show it wrong.** A global `core.hooksPath` under a temporary `HOME` landing the hook in the wrong folder; finding 1 shows this happens as the environment is described. -- measured below

1. **Blocking.** The "minimal environment" can silently drop the global `core.hooksPath` the draft promises to honor. Measured, Git 2.53.0, `env -i PATH=`: a global `.gitconfig` value was ignored (`.git/hooks` returned) until `HOME` was passed; `XDG_CONFIG_HOME` also works. Windows profile variables not checked. The test list sets `core.hooksPath` in local config only. Closes it: name the variables passed through, and add a global-config case under a temporary `HOME`.
2. **Non-blocking.** `select_git` returns `None` for no Git but raises `GitReadError` (a `RuntimeError`) for an unsafe one (`test_git_read.py` line 190); `_git_hooks_path` catches only `OSError`, `UnicodeError` and `SubprocessError`, so that case ends in a traceback. Catch `RuntimeError` and return `None`. The "finds nothing" test cannot be reached through the public entry (`_git_path` refuses first); mark it a seam case or drop it.
3. **Non-blocking.** Bundling B is justified (traceback reproduced; `check_cairn.py` line 675 already returns 2), but the cost is understated. Five frozen paths change (`gate_manifest.json` `frozen_files`: the `hooks.py` twin and both checkers with twins; `tools/_intent/hooks.py` is not frozen), and `test_git_read_routes.py` is a sha-pinned test file whose node IDs enter `collection`. Say so in the Decision summary. Both checkers' docstrings define exit `2` as "usage error" (`link_check.py` line 53); widen them in the same edit.

Light is defensible: the file is not on the named list in `dev/rules/protected-surfaces.md`. A second hand-rolled Git launch with repository config visible is for Security Review to judge, not this pass.

**Audience / rule loss:** The rewritten `hooks.py` docstring must keep "not used for repository inspection or hook execution" and name the trusted local-config residual; no other rule weakens.

**Coverage:** I did not run the gate or tier tests, test Windows, or read the helper's process-capture code. Over target (about 465 words) because each finding carries its measurement. Security Review is separate and this pass does not clear it.

## Security Review -- Claude Opus (Security Reviewer, High) -- 2026-11-16

```
Reviewed commit: 04921fc918bfe27535c8d2aecb1c6e6f39645ae0
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: ACCEPT

**Elapsed**: about 6 minutes (about 11:58 to 12:04, `date`)
**Tokens**: unknown

Obligation: does finding the hooks folder through `select_git` remove the "plain `git` from `PATH`" exposure without opening a new one?

Steelman: one verified absolute Git, run with no `PATH`, closes the only known place Cairn runs a repository-supplied program, and adds no new trust.

**Foundations**

1. **Should this happen as framed?** Yes. `select_git` skips relative and empty `PATH` entries and refuses a Git inside the repository (`git-inside-inspected-repository`), so neither a planted root `git` nor an absolute entry into the repository is run; an absolute program path is not searched for in the current folder on Windows either. -- `templates/skills/_lib/git_read.py` lines 444-462, 337-348
2. **Best alternative.** None safer at this cost; a folder-containment check would break a legitimate global `core.hooksPath` such as `~/.githooks`, which lives outside the repository by design. -- finding 1
3. **What would show it wrong.** A hostile local config making the hooks query itself run a program. Measured, Git 2.53.0, scratch repository: with `core.fsmonitor` set to a marker script, `rev-parse --git-path hooks` and `--show-toplevel` did not run it; `git status` did (positive control). -- scratch run, `env -i HOME=... git -C repo ...`

1. **Non-blocking (existing, not opened here).** Attacker: whoever delivers a whole repository folder including `.git/config` (a clone never copies it). Input: `core.hooksPath=../outside` plus a `post-commit` link in that folder. Harm, reproduced in scratch with today's `intent.py install-hook`: it appended the Cairn block to an executable script outside the repository, through the link. That attacker already gets code run by Git on the next `git status` (fsmonitor, above), so the added harm is small. Closes it: refuse when the hook file is a link (`lstat`), and say in Residual risk (1) that writes follow links.
2. **Non-blocking (adds to the ordinary finding 1).** Name the environment: pass `HOME`, `XDG_CONFIG_HOME` (Windows: `USERPROFILE`, `HOMEDRIVE`, `HOMEPATH`, `SystemRoot`); strip `PATH` and every `GIT_*`, including `GIT_DIR`, `GIT_EXEC_PATH` and `GIT_CONFIG_*`; do not set `GIT_CONFIG_NOSYSTEM`, so a system `core.hooksPath` still counts. Run the snapshot's verified path from the helper's neutral working folder.
3. A `GitReadError` traceback happens before any write, so it already fails closed; the ordinary finding 2 (refuse with a message, exit 1) is enough.

**Coverage:** Not covered: Windows (not run), the Markdown-check part B, the route-test harness (`lab.arm`), and other config keys beyond fsmonitor and hooksPath. No tests run.

## Response -- Claude Fable 5.2 (coordinator, for the Sonnet author) -- 2026-11-16

**Elapsed**: about 12 minutes. **Tokens**: unknown.

Both reviews are answered here. I checked the frozen-file and exit-code claims against the tree; the measurements (the reproduced `PATH` attack, the ignored global config, the write through a link) are the reviewers' and I did not repeat them. The operative text above is revised in place.

Ordinary review (REVISE):

1. **Accepted (blocking).** Item A now names the variables passed through and stripped, and the tests add a global-config case under a temporary `HOME`.
2. **Accepted (non-blocking).** The function also catches the helper's refusal and returns `None`. The "finds nothing" case is marked as an internal case, since the command cannot reach it.
3. **Accepted (non-blocking).** The Decision summary states the five frozen files and the re-anchor (checked in `gate_manifest.json`). Item B widens the checkers' exit-code wording.

Security Review (ACCEPT):

1. **Accepted (non-blocking).** New item C refuses a linked hook file, and Residual risk (1) says writes follow links today. This is the one addition to scope. It closes an exposure that exists in today's code, in the same function this proposal already edits.
2. **Accepted (non-blocking).** Folded into item A with the ordinary finding 1. "Run from the helper's neutral working folder" is left for the implementer to confirm against `-C toplevel`; I did not check how the helper sets it.
3. **Noted.** No change needed beyond ordinary finding 2.

The docstring keeps the sentence the ordinary reviewer named. The tier stays as proposed: light, with the Security Review now held. Unrun by anyone: Windows.

**For the Maintainer.** (1) Fix the lookup, not document the exception. Default: fix. (2) Refuse a linked hook file (item C), at the cost named there? Default: yes.

## Decision -- Maintainer (scribed by Antigravity Gemini 4 Hydrogen) -- 2026-11-16

**Tier**: light

**ACCEPTED.**

> "I accept #1 - #4 with your recommendations. #5 I accept requiring the checks to be working on windows"

This accepts the proposal as revised (`light` tier, with the completed Security Review held; no plan), fixing `_git_hooks_path` via `select_git` with the minimal environment (item A), exiting 2 cleanly on `RuntimeError` in `link_check.py` and `sync_doc_snippets.py` (item B), and refusing linked hook files before writing (item C). Joins the v0.8 gate re-anchor for the five frozen files and `test_git_read_routes.py` node IDs. New recurring human operations: zero.

**Elapsed:** under 1 minute. **Tokens:** unknown.

## Implementation verification -- Claude Sonnet 5.5 (Implementer, Medium) -- 2026-11-16

**Commit**: `114ef31c` (code and tests together). Items A, B and C as accepted. Choices the text left open: item C also covers `--uninstall` (it writes too) and refuses symbolic links only, exit 4 like the other refusals; the query runs from the helper's neutral folder via its private `_neutral_cwd` (as `lockfile.py` already calls `_version_probe`); no re-check of the Git file between selection and run.

**Before and after (measured).** Scratch script outside the repository, macOS, 19 checks: before 12 failed (planted root `git` ran with `.` or an empty entry first; `GIT_DIR` broke the query; writes followed live and dangling links; both checkers gave a traceback and exit 1); after all 19 pass, global and local `core.hooksPath` pass both ways. New route cases (13 selected, including the tightened `== 2` case): against pre-change code 11 failed and 2 passed (the local-config cases, which old code already honored), on macOS and on Windows; after, 13 passed on both.

**Whole route file.** macOS 29 passed (45.9 s; one earlier run had an exact-replacer failure under heavy disk load that did not recur in four reruns, cause not isolated). Windows VM, new folder, x64 Python 3.13.18, test-file hash matched: 29 passed (99.75 s), none skipped, so the link cases ran.

**Other tests.** Files naming the changed code: 376 passed, 1 skipped; the rest of the `test_tiers.py` list including `test_gate_manifest.py`: 640 passed, 2 skipped (Windows-only). `test_ast_attest.py`: 1 red, `install.py` `print_report` (another change, not these files). `_gate_manifest.py verify` HOLD names my five frozen files and 9 new node IDs, for the Maintainer's re-anchor.

**Not run.** Whole suite; native ARM64 Python; an older Git; `XDG_CONFIG_HOME` pass-through; Windows without `USERPROFILE`.

**Benefit versus cost**: worth it -- the known planted-`git` hole in the hook installer and two tracebacks are closed, and a hostile linked hook file is refused, with Windows checks; cost: 339 added lines in 7 files, +15 s macOS and +27 s Windows per route-file run, about 50 minutes from first claim (12:23) to this record (13:11, `date`; tokens unknown); remaining burden: the Maintainer's re-anchor, a project that links its hook file installs by hand, reliance on one private helper name.

## Implementation closeout -- Codex Terra, coordinator -- 2026-11-17

Complete on the recorded focused results, reusing evidence for unchanged
behavior. The combined revision includes the reviewed Windows receipt/ledger
repairs (`63d0704a`, `7c77da3d`; reviews `f8d171fd`, `aa1aeeba`). No suite
is repeated for this Boundary B record. Existing skips and omissions remain
unpassed; the grouped re-anchor stays a separate Maintainer wait on
`dev/PLANNING.md`, not an archive prerequisite.

Elapsed: approximately ten minutes for the grouped closeout; tokens unknown.
