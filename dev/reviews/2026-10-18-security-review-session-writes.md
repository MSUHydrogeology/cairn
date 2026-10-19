# Security Review — session kernel writes (`7e6a14e5`) — Claude Opus 5.5 — 2026-10-18

**Obligation**: the Security Review that clears GS-SR-1
(`dev/reviews/2026-10-18-security-review-gitignore-seed-guard.md`, at
`c00e6ddc`) and GS-CR1
(`dev/reviews/2026-10-18-code-review-gitignore-seed-guard.md`), both
answered by the defect repair in `7e6a14e5`. That repair has no proposal or
plan; it changes the local interpreter binding's module, a named high-risk
surface in `AGENTS.md`.
**Reviewed commit**: `7e6a14e5` ("Session kernel: no write goes through a link
or leaves the project"): `tools/session.py`, its twin
`templates/skills/_lib/session.py`, the new
`bootstrap/tests/test_session_writes_contained.py`, and one lockfile hash
line. The "before" kernel is its parent `c14ec9c5`; its `session.py` is
byte-identical to the implementer's stated base `20f145ed`.
**Distance**: a fresh session, not the implementing one. The commit credits a
different model size of the same agent type, so the distance is a fresh
context, not a different type. This is a security pass only.
**Interpreter**: Python 3.13.13 at `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
`PYTHONDONTWRITEBYTECODE=1`. Platform darwin, APFS (case-insensitive), git 2.53.0.
**Where things ran**: one detached worktree of `7e6a14e5` in a fresh, uniquely
named folder under the session scratchpad, plus throwaway probe folders beside
it; all removed when done. Every hostile repository was built, committed and
then **cloned with git**, and the clone's real `tools/session.py` was run as a
subprocess. The only writes to the shared tree are the intent claim and this
record. Two adopter repositories (LHM, modflow_tools) were only read; the
kernel ran against `git archive` snapshots of their skills data, never the
repositories.

Untracked paths: `dev/.cairn/handoff.lock`, `dev/.cairn/handoff-owner`, `dev/.cairn/x`, `dev/.cairn.` (machine-local state names, and hostile vendor-row values used in the probes; no checkout carries them)

**Verdict**: **GS-SR-1 and GS-CR1 CLEARED.** 0 findings block them. 9 findings
in all: 2 high that are not caused by this commit and live in other code
(SW-SR-1, SW-SR-2), 4 low, 3 informational.

## In brief

**The hole is closed.** Both reported attacks work on the old kernel and fail
on the new one, through a real `git clone`. On the old kernel, a committed
folder forced the copy path, a committed `.gitignore` link sent the appended
lines to a shell startup file, and with `.gitignore` linked to `.git/config`
git ran the planted command during the routine's own later git calls. On the
new kernel, the folder no longer forces anything (the probe name is random),
a linked `.gitignore` is refused with a plain one-line note, and a vendor row
carrying a config stanza is skipped.

**The wider set the implementer named is closed too.** I listed every write in
the module from the tree myself (below) and attacked each one: 25 hostile
vendor rows (`.git` and `dev/.cairn` in many spellings, plus shell, glob and
newline characters), folder links to `.git` and
`dev`, links at a copy destination, at a skill folder, at the copy root and at
the harness folder, a quarantine name linked to an outside folder, linked
`dev/`, `dev/reflections` and `dev/.cairn` under `session-end` and
`session-end --handoff`, a hard link, a folder and a non-UTF-8 `.gitignore`.
Across all my probes, 14 runs of the old kernel wrote outside the project or
into `.git/` or `dev/.cairn/`, and in three of them git then ran a planted
command. On the new kernel none did.

**The interpreter binding is untouched.** `_resolve_interpreter`,
`_probe_interpreter`, `_has_symlink_component`, `_warn_stale_once`,
`encode_display` and `_safe_field` are AST-identical to the parent, and so is
the encoder's range table. The twins are byte-identical (`cmp`), and the
lockfile's new hash matches the file.

**But two serious holes remain elsewhere, and this commit did not create
either.** (1) A project can simply *commit* `dev/.cairn/local-env.json`. Git
checks it out like any other file, and `session-start` then runs whatever
program it names. With `/usr/bin/make` and a committed `Makefile`, the
unmodified kernel ran the Makefile's command at session start and again at
the plain reflection-only `session-end` (SW-SR-1). (2) The installer's copy
fallback has the defect the kernel just lost, as the implementer reported. I
confirmed it: a committed folder forces copy mode, and a committed dangling
link made the install create a file outside the project with the project's
own chosen bytes (SW-SR-2).

**The one remaining gap the module names is real and acceptable**: a parent
folder swapped for a link between the check and the write. That needs a
process already running on the machine. I forced it and it wins. There is a
second gap of the same kind that the module does not name: the temporary
file's permission change follows a link (SW-SR-3, low).

## Findings at a glance

| id | what | severity | blocks GS-SR-1 / GS-CR1? |
|---|---|---|---|
| SW-SR-1 | a committed `dev/.cairn/local-env.json` is trusted: `session-start` runs the program it names (measured: `make` ran a committed `Makefile`) | **high** (pre-existing, interpreter trust root) | no; owed its own repair and Security Review |
| SW-SR-2 | engine twin: the installer's copy fallback writes through links and its fixed probe name lets a folder force copy mode (measured: project bytes into a new file outside) | **high** (pre-existing, engine) | no; different program, reported by the implementer |
| SW-SR-3 | `_write_replacing` changes the temp file's mode by name; a swapped-in link carries the change to an outside file | low | no |
| SW-SR-4 | where `O_NOFOLLOW` is missing, the `.gitignore` read follows a link swapped in after the check and copies outside bytes into the project's `.gitignore` | low | no |
| SW-SR-5 | copy mode crashes with a traceback when a file sits where a copy folder must go; the ignore seed and earlier copies have already been written | low | no |
| SW-SR-6 | raw terminal control bytes from checkout data still reach the terminal on two `session-end` routes this commit did not touch | low (pre-existing) | no |
| SW-SR-7 | a `.gitignore` that is a named pipe hangs `session-start` in copy mode | informational | no |
| SW-SR-8 | copy mode reads through links inside `.agents/skills/` and copies the outside bytes into `.claude/skills/` | informational | no |
| SW-SR-9 | the fan-out guard's messages print absolute paths, and its "outside" branch prints the resolved path | informational | no |

## Q1 — Is it closed?

### Every write in `session.py`, listed from the tree

Found by a search of the file for every call that creates, writes, moves,
removes, links, changes the mode of, or runs something
(`write`, `open`, `replace`, `rename`, `unlink`, `mkdir`, `symlink`, `chmod`,
`ftruncate`, `subprocess.run`), then each hit read in place. Line numbers are
at `7e6a14e5`; the twin has the same lines.

| # | write | where | guard | disposition |
|---|---|---|---|---|
| W1 | symlink probe: `os.symlink(".", probe)`, then `probe.unlink()` | `tools/session.py:852`, `:859` | random name each call | **safe.** Creating a link never follows one; the unlink removes only the link. A committed folder at the old name (or the new prefix) no longer forces copy mode (A12). |
| W2 | `_write_replacing`: exclusive temp create, write through the descriptor, `os.chmod(tmp)`, `os.replace(tmp, dst)`, unlink temp on failure | `:599`, `:602`, `:605`, `:608`, `:611` | caller checks first; `O_EXCL` + `O_NOFOLLOW` on create | **safe except `:605`**: `os.chmod` by name follows a link (SW-SR-3). The rename replaces a link instead of following it (race R1: 0 of 3,000). |
| W3 | `_create_text_exclusive` | `:630`, `:632` | caller checks; `O_EXCL` + `O_NOFOLLOW` | **safe** on POSIX. |
| W4 | `.gitignore` seed, `_seed_skill_gitignore` → W2 | `:969` | entry name rule `:948`; `_assert_not_linked` `:953`; read with `O_NOFOLLOW` `:955` | **closed** (A1–A4, A9). |
| W5 | `_heal_skill_symlink`: `dst.unlink()` (a link), `dst.parent.mkdir`, `os.symlink(rel, dst)` | `:981`–`:983`, `:991`–`:992` | `_assert_fanout_contained` `:1086` (link ancestors refused; `dst` itself may be the link it replaces) | **safe**: removes and makes only a link, inside the project (A6n, A7cn). git returns a resolved project root, so the ancestor walk runs (checked through a linked folder). |
| W6 | `_heal_skill_copy`: `os.replace(out, bak)`, `out.parent.mkdir`, `_write_replacing(out)` | `:1039`, `:1041`, `:1042` | `_assert_not_linked` on every copy and quarantine name before the first move, `:1015`, `:1027`; plain-file checks | **closed** (A5–A8). Crash on a file where a folder must go (SW-SR-5). |
| W7 | handoff lock: `mkdir`, exclusive create, write; reclaim `unlink` + recreate; heartbeat through the descriptor; release `unlink` | `:1252`, `:1254`, `:1259`, `:1286`, `:1289`, `:1307`–`:1309`, `:1318` | `_assert_not_linked` `:1251` | **closed** for a link present at the check (B2). Release and reclaim remove by name: the parent-swap gap class. |
| W8 | reflection prune: `path.unlink()` | `:1356` | `_assert_not_linked` on the folder `:1340`, dry runs included | **closed** (B1). A dated entry that is itself a link has only the link removed (B8). |
| W9 | reflection scaffold: `refl_dir.mkdir`, `_create_text_exclusive` | `:1521`, `:1525` | `_assert_not_linked` `:1505` | **closed** (B1a, B3, B4). |
| W10 | child processes: `git` (`:349`, `:390`), `intent.py whoami/list/prune` (`:429`, `:1393`, `:1423`), `evolution_infer.py` (`:1457`) | run under the resolved interpreter | — | git may refresh its own index. The intent prune's writes are `intent.py`'s, not reviewed here. **What runs is chosen by the binding: SW-SR-1.** |
| W11 | the terminal (stdout, stderr) | throughout | `encode_display` | Q4. |

### Probes (hostile clones, real `session-start` / `session-end`)

Each case: a source repository built with the hostile data, committed, then
cloned with `git clone`; the clone's own `tools/session.py` (the shipped bytes
of the version under test) run as a subprocess. Snapshots compare a folder
outside the clone, the clone's `.git/` (index and logs aside) and its
`dev/.cairn/`. "Forced copy" loads the clone's file and sets the symlink probe
to "unavailable" before calling `main`: a stand-in for a platform where links
cannot be made. That is the copy path's real home, and on POSIX a checkout can
no longer reach it (A12). For the A cases, "before" is `c14ec9c5` and "after" is
`7e6a14e5`. In some forced-copy rows the wrapper itself left a
`tools/__pycache__` (it runs with `-I`); the kernel did not write it.

| case | before | after |
|---|---|---|
| A1 GS-SR-1: `.gitignore` → outside startup file, folder at the old probe name | exit 0, **outside appended**, copies made | exit 0, symlink made, outside unchanged |
| A2 + row `$(touch GSR_MARKER_RAN)/skills` | **outside appended** with the command line | row skipped (encoded note), outside unchanged |
| A3 GS-CR1: `.gitignore` → `.git/config`, row carries `[core] fsmonitor = touch FSMON_MARKER` | **`.git/config` changed, `FSMON_MARKER` created by git** | row skipped, `.git/` unchanged, no marker |
| A4a–c the same three, forced copy | **outside appended**; **`.git/config` changed, marker created** | refused: "refusing to write through a link or outside the project: .gitignore"; or row skipped. Nothing outside, nothing in `.git/` |
| A5 25 hostile rows (`.git`, `.git/hooks`, `.GIT/hooks`, `.Git/x`, `.git./hooks`, `.git../hooks`, `.git /hooks`, `dev/.cairn`, `DEV/.Cairn`, `dev/.cairn.`, `dev./.cairn`, `dev/.cairn/x`, `./dev/.cairn`, `dev//.cairn`, `dev/.cairn/`, `.claude`, `/abs/x`, `a/../.git`, names with a space, `!`, `#`, a newline, `*`, `git~1/hooks`, `.git::$INDEX_ALLOCATION/x`) + the real row, canonical skills holding a `config` and a `local-env.json`, a real binding planted after the clone; forced copy | **`.git/config` replaced (git ran the planted fsmonitor: `CFG_MARKER`), the binding `dev/.cairn/local-env.json` replaced**, 19 new paths in `.git/`, 13 in `dev/.cairn/` | all 25 hostile rows skipped, one encoded note each; `.git/` and `dev/.cairn/` unchanged; the real row copied |
| A5n the same, symlink mode | links made at `.git/x`, `dev/.cairn/x` | all skipped, `.git/` and `dev/.cairn/` unchanged |
| A6 committed `g → .git`, `d → dev`; rows `g/hooks`, `d/.cairn`; both modes | refused (symlinked parent) | refused (symlinked parent) |
| A7a copy destination `SKILL.md` → outside file | link quarantined, outside unchanged | refused before any copy |
| A7b skill folder → outside folder | refused (old guard) | refused |
| A7c `.claude/skills` → outside folder (copy) | refused | refused (`.gitignore` already seeded, inside) |
| A7cn the same, symlink mode | relinked inside | relinked inside, outside unchanged |
| A7d `.claude` → outside folder | refused | refused |
| A8 quarantine name `SKILL.md.diverged.bak` → outside folder | **divergent file moved into the outside folder** | refused before anything moved |
| A9a `.gitignore` hard-linked to an outside file (local; git cannot carry one) | **outside appended** | outside bytes unchanged; the project's name now has its own file |
| A9b `.gitignore` is a named pipe (local) | hangs | hangs (SW-SR-7) |
| A9c `.gitignore` is a folder (committed) | traceback, exit 1 | one-line note, exit 0 |
| A9d `.gitignore` is not UTF-8 (committed) | traceback, exit 1 | one-line note, exit 0 |
| A10 a file where a copy folder must go | traceback, exit 1 | traceback, exit 1 (SW-SR-5) |
| A12 folders at `.cairn-skill-symlink-probe`, `…-00000000`, `…-` | copy mode forced | symlink mode |

`session-end`, both versions, real subprocess:

| case | before | after |
|---|---|---|
| B1a `dev/reflections` → outside folder; `session-end` | **reflection written outside** | exit 1, refused, nothing written |
| B1b the same, `--handoff`, owner marker set | **outside `2020-01-01-old.md` deleted**, reflection written outside | exit 1, refused before the prune |
| B1c the same, `--handoff --dry-run` | listed | exit 1, refused |
| B2 `dev/.cairn` → outside folder (made read-only to catch the attempt), `--handoff` | traceback: tried to create `dev/.cairn/handoff.lock` in the outside folder | refused: "… dev/.cairn/handoff.lock" |
| B3 `dev` → outside folder | **`reflections/` and a reflection created outside** | refused |
| B4 dangling link at the reflection's exact name (operator set `CAIRN_AGENT`/`CAIRN_SESSION` so the name is predictable) | **outside file created** | refused |
| B8 a dated reflection that is a link to an outside file, `--handoff` | the link removed, outside unchanged | the same |

**Answer.** On the new kernel, no probe wrote outside the project, followed a
link, or touched `.git/` or `dev/.cairn/`. The remaining routes are races
that need a process on the machine (Q3), and the binding route (SW-SR-1),
which is not a write by this module.

## Q2 — The interpreter binding is untouched

* AST comparison, `c14ec9c5` against `7e6a14e5`, both files:
  `_resolve_interpreter`, `_probe_interpreter`, `_has_symlink_component`,
  `_warn_stale_once`, `encode_display`, `_safe_field` are **identical**. So are
  `_escape_code_point`, `_display_unsafe_code_point`, `_safe_stream`,
  `_git_env`, `_state_dir`, `_assert_within`, `_sibling_tool`,
  `_intent_whoami`, `_surface_intents`, `_prune_intents`,
  `_run_evolution_infer`, `_DISPLAY_UNSAFE_RANGES`, `_DISPLAY_SYNTAX_CHARS`,
  `_CAIRN_STATE_DIR` and `_REBIND_REMEDY`. The changed or new definitions are
  exactly the write-path set (`_assert_not_linked`, `_write_replacing`,
  `_read_regular_bytes`, `_create_text_exclusive`, `_vendor_path_parts`,
  `_skill_symlinks_available`, `_assert_fanout_contained`,
  `_seed_skill_gitignore`, `_heal_skill_copy`, `_heal_skills_fanout`,
  `HandoffLock`, `_prune_reflections`, `_do_reflection`) and three new
  constants.
* `cmp tools/session.py templates/skills/_lib/session.py`: identical at
  `7e6a14e5`, and at its parent.
* `dev/.cairn/cairn-lock.yml`: the new `tools/session.py` hash
  (`sha256:4f08c74e…`) equals the file's SHA-256.
* The owning test files (`test_session_writes_contained.py`,
  `test_skills_self_heal.py`, `test_session_kernel.py`) in the worktree: 115
  passed.

## Q3 — Gaps and fallbacks

**Closed where claimed: a link swapped in at the last name.** A separate
thread flipped `.gitignore` between a regular file and a link to an outside
file while the kernel seeded 3,000 different entries (R1). The writes
completed 986 times, 2,014 calls were refused, and the outside file never
changed. None of the bytes the seed wrote contained the outside file's
content. The rename and `O_NOFOLLOW` do what the docstring says. The
implementer's tests for a link swapped in at a copy destination and at the
quarantine name pass.

**The named gap: a parent folder swapped for a link.** I forced the win (R2):
swapping `.claude/skills/s` for a link to an outside folder just before the
write put `SKILL.md` in the outside folder. The same swap of
`dev/reflections` between its check and the exclusive create put the
reflection outside. Real racing attempts did not win in 3,000 calls each (a
racing thread, which Python's interpreter lock slows, and a separate-process
flipper that jammed), so I have no measured real-race win rate. That is not
evidence the race cannot be won: the window from the last check to the first
write is 61.5 µs at the median and 415 µs at the 99th percentile. The prune's
window spans its whole listing loop. **Honest and acceptable**: it needs a
process already on the machine with write access to the project, which is
the "no concurrent filesystem attacker" model `bootstrap/SAFETY.md` already
accepts for the engine. Two notes: the module's "the one gap left" undercounts
(SW-SR-3, and SW-SR-4 where `O_NOFOLLOW` is missing), and `bootstrap/SAFETY.md`'s
residuals list names only the engine's and the onboarding helper's windows,
not the kernel's.

**Platforms without `O_NOFOLLOW`** (Windows). `_OPEN_NO_LINK` falls back to
`O_BINARY` alone, silently. I simulated that by setting the flag to 0 and
rerunning R1. Writes stay safe: 1,151 writes, and the outside file never
changed, because the rename and `O_EXCL` carry the write side. The read does
not stay safe: 223 of the 1,151 writes carried the outside file's bytes into
the project's `.gitignore` (SW-SR-4). On Windows, making a link needs the same
privilege that would also make the probe succeed, so copy mode and links
rarely coexist there. I could not test Windows itself (see "What I did not
cover").

## Q4 — Messages

The new refusals are fixed text plus a project-relative name through
`encode_display`: `_LINK_REFUSAL`, the unsafe-entry and unsafe-row notes, the
not-a-plain-file refusal, `_GITIGNORE_UNREADABLE`. Probes with
`ESC ] 0 ; PWNED BEL ESC [2J` in a canonical file name and in a link target (M1–M4,
forced copy) put no raw ESC or BEL on stdout or stderr. A link's target never
appeared: M4's link pointed at a name carrying the escape, and the message
named only `.claude/skills/_data/vendor_targets.yml`. The crash in M3 is a
Python traceback, whose `repr` escapes the name. The row note in A3 shows the
stanza as `zz\x0a[core]\x0a\x09fsmonitor…`. The fan-out guard's two messages
are encoded but print absolute paths, not project-relative ones (SW-SR-9).
Older messages elsewhere in the module still print checkout data raw
(SW-SR-6).

## Q5 — Legitimate adopters

* **LHM** and **modflow_tools** (read only): each table has the stock seven
  rows. The only symlink-tier row is `.claude/skills`, which passes the rule.
  The alias rows are skipped before the rule runs. `.gitignore`, `dev/`,
  `dev/reflections` and `dev/.cairn` are plain in both; `.claude/skills` is
  the expected link.
* Running the new kernel on `git archive` snapshots of each project's
  `.agents/`, `.gitignore` and `dev/reflections`: symlink mode gives
  `claude-code: symlink -> linked`. Forced copy gives `copied`, then
  `already current` on the rerun. `.gitignore` is untouched, since both
  already ignore `.claude/skills`, and `git status` is clean.
* Plausible future rows pass: `.github/skills`, `.cursor/skills`,
  `.gemini/skills`, `.kiro/skills`, `.opencode/skill`,
  `.github/copilot/skills`, `.config/harness/skills`. A single name
  (`skills`), a space, `+`, `@` or a backslash is warned and skipped.
  **Acceptable**: the skip is loud and names the row, and no shipped or
  adopter row is affected.
* Behaviour changes a deliberate setup would feel: a linked
  `dev/reflections`, `dev/` or `dev/.cairn` (a synced folder, say) now makes
  `session-end` exit 1 rather than write through. A linked `.gitignore` stops
  the copy-mode fan-out, with a note. Both fail closed with plain text. I
  found no adopter doing either.

## Q6 — The engine twin (confirmed; not fixed)

Measured with the real installer (`bootstrap/scaffold.py`, from the reviewed
worktree; the engine is unchanged by `7e6a14e5`) into a fresh target already
holding the data:

| case | result |
|---|---|
| E1 control: `.claude/` only | exit 0, `.claude/skills` is a link |
| E2 + a folder at `.cairn-symlink-probe` | exit 0, **copy mode** ("symlinks unavailable (Windows without Developer Mode?)" on macOS) |
| E3 E2 + `.claude/skills/session-start/SKILL.md` a dangling link to an outside path | exit 0, **file created outside** |
| E4 E2 + divergent `session-end/SKILL.md` and its `.diverged.bak` a link to an outside folder | exit 0, **the divergent file moved into the outside folder** |
| E5 E2 + the copy name a link to an outside file holding the canonical bytes | exit 0, **outside file rewritten in place** (mtime changed, bytes equal) |
| E6 E2 + the project's own `.agents/skills/session-start/SKILL.md` set to a shell line, its copy name a dangling link to `outside/.zshenv` | exit 0, **`outside/.zshenv` created holding the project's bytes** (`touch ZSHENV_MARKER …`); the install kept the project's canonical file and only warned that the lockfile was not written |

The causes are the ones reported. `_symlinks_available`
(`bootstrap/_scaffold/install.py:485`) uses the fixed name
`.cairn-symlink-probe` (`:490`), and its cleanup fails on a non-empty folder.
`_emit_skill_copy_fallback` (`:523`) checks each name with the engine's
`_assert_fanout_contained` (`:550`, `:555`; `bootstrap/_scaffold/security.py:79`),
which permits the name itself to be a link. It then writes with
`shutil.copyfile` (`:559`), which opens the destination and so follows a
link, and quarantines with `shutil.move` (`:556`), which moves *into* a
folder that a link names. The project's own skills folder supplies the bytes,
because the install does not clobber it. This is SW-SR-2.

## Findings

### SW-SR-1 — high, pre-existing, not blocking: a committed interpreter binding is trusted, so a checkout chooses what `session-start` runs

**Plain:** the file that tells the session helper which Python to run is
meant to be private to each machine and never committed. Nothing checks that.
A project can commit one, git hands it to whoever clones or checks out the
branch, and the helper then runs the program it names, with arguments it
fixes.

* `_resolve_interpreter` (`tools/session.py:678`) reads
  `dev/.cairn/local-env.json` and accepts any absolute, present, non-linked,
  executable file. It is the documented "shape validator, not an
  authenticator". Its premise, "untracked, gitignored", is not enforced:
  being ignored does not stop git checking out a *tracked* file.
* **Measured** through `git clone`, unmodified kernel, before and after
  `7e6a14e5` alike: a committed binding `{"interpreter": "/usr/bin/make"}`
  plus a committed `Makefile` with a `list whoami:` rule. `session-start` ran
  `make tools/intent.py list` in the project and the rule created
  `MAKE_MARKER`. The plain `session-end` ran `make … whoami` and did the same:
  this is the reflection-only path the module says can at worst leave "a
  stray reflection file". The binding line "interpreter: /usr/bin/make (from
  local-env.json)" is printed only after the program has run.
* **Not only fresh clones.** Git treats an ignored file as expendable.
  Checking out a branch that tracks `dev/.cairn/local-env.json` overwrote an
  existing ignored binding without a word, and switching back deleted it
  (measured).
* Reach: the runs happen where `tools/intent.py` (session start, reflection)
  or `tools/evolution_infer.py` (full handoff) sits beside the kernel, which
  is every adopter of the coordination module and Cairn itself.
* Relation to this commit: none in the code. But the commit's rule refusing a
  `dev/.cairn` vendor row "would write the interpreter binding" defends a
  door the checkout can open directly. That part of the rule adds little
  until this is fixed. The `.git` part of the rule is not affected: git
  itself never checks files out into `.git/`.

**Recommended fix** (a change to the binding's reader and validation order,
so it takes its own Security Review):
1. **Required:** refuse a binding that git tracks, before reading it. For
   example `git ls-files --error-unmatch -- dev/.cairn/local-env.json`
   succeeding → `LifecycleError` with the rebind remedy. Optionally also
   refuse one that is not ignored (`git check-ignore`).
2. Have the installer's binding writer refuse to keep a tracked binding, and
   have the session report say when one is found.
3. Recommended: print the resolved interpreter *before* the first child
   process, not after.

### SW-SR-2 — high, pre-existing, not blocking: the installer's copy fallback writes through links (the engine twin)

**Plain:** the installer has the same copy code the session helper just
lost. A project can force the copy path with one folder on any operating
system. A link at a copy name then lets it create a file anywhere the user
can write, holding bytes the project chose.

* Evidence: Q6, E2–E6.
* Exposure: running the installer into a repository that already holds
  hostile data, the normal "adopt Cairn into an existing project" path, and
  `--force` re-installs. `upgrade --apply` reaches the fan-out only when a
  new skill is added. Creating a file needs one that does not exist yet (a
  missing `~/.zshenv`, a launch-agent file). Overwriting an existing file
  changes nothing visible, because a differing file is moved aside and only
  an equal one is rewritten.

**Recommended fix** (an engine change: new AST symbols, a Maintainer-run
re-anchor and a Security Review): port the kernel's helpers. A random probe
name; `_assert_safe_write` (which refuses the name itself being a link) on
every copy and quarantine name, for the whole set before the first move; the
write by exclusive temp file and rename; the quarantine by `os.replace`.

### SW-SR-3 — low: the temp file's mode is changed by name, and that follows a link

**Plain:** the safe-write helper makes a new temporary file, then sets its
permission bits by name. A program racing on the same machine can swap that
name for a link in the gap, and the permission change lands on a file outside
the project.

* `os.chmod(tmp, kept_mode)` (`tools/session.py:605`) follows a link.
* **Forced win**: an outside file at mode 0600 became 0644. Its bytes were
  unchanged, and `.gitignore` was left as a link to it, so the next session
  refuses loudly.
* **Real race**: a thread listing the folder and swapping any
  `.cairn-write-*` name for a link changed the outside file's mode in **22 of
  3,000** calls.
* This is a link-follow at the last name, not the parent-folder gap the
  docstring names as "the one gap left".

**Recommended fix:** set the mode on the open descriptor before closing it
(`os.fchmod(fd, mode)`; skip it where the platform lacks it). Then list the
kernel's remaining window in `bootstrap/SAFETY.md`'s residuals beside the
engine's.

### SW-SR-4 — low: where `O_NOFOLLOW` is missing, the `.gitignore` read follows a swapped-in link

**Plain:** on a platform without the "don't follow a link" open flag, a link
swapped in after the check is still never written through. But the read
follows it, and the outside file's text is copied into the project's
`.gitignore`, which is usually committed.

* Simulated with the flag set to 0 (R1 rerun): 223 of 1,151 seeds wrote the
  outside file's bytes into the project file. With the flag: 0.
* Needs a process on the machine, and a platform with links but no
  `O_NOFOLLOW`.

**Recommended:** after opening, compare `os.fstat(fd)` with an `os.lstat`
taken at the check (device and inode). That works without `O_NOFOLLOW`. Or
refuse to read where the flag is absent and a link is possible.

### SW-SR-5 — low: copy mode crashes when a file sits where a folder must go, after it has already written

**Plain:** if, say, `.claude/skills/session-start` is a file, the copy step
stops with a Python traceback and `session-start` exits 1 instead of warning
and carrying on. By then the `.gitignore` seed and the earlier copies have
already been written.

* `_heal_skill_copy` plans every name, but `Path.exists()` returns False
  under a file parent, so the plan passes. `out.parent.mkdir` (`:1041`) then
  raises `FileExistsError`, which `cmd_session_start` (`:1121`–`:1125`) does
  not catch; it catches only `LifecycleError`. Measured on A10 (before and
  after alike) and M3.
* This contradicts "a refusal leaves nothing half-done" for this one route,
  and the module's "fail-soft" self-heal. It is not a containment break.

**Recommended:** in the planning loop, refuse with `LifecycleError` when any
existing folder between `dst` and the copy name is not a folder. Or turn
`OSError` from the self-heal into the same warning.

### SW-SR-6 — low, pre-existing: raw control bytes from checkout data still reach the terminal on `session-end`

**Plain:** two older messages in this module print text taken from the
project without the module's own safety encoder. A project can therefore put
terminal control sequences on the operator's screen.

* The full-handoff manifest prints reflection file names raw
  (`tools/session.py:1588`–`:1590`). A committed
  `dev/reflections/2020-01-01-<ESC]0;PWNED BEL ESC[2J>.md` put raw ESC/BEL on
  stdout under `session-end --handoff --dry-run`, which needs no marker (B5).
* The handoff-lock refusal prints the lock's `agent` and `host` raw
  (`:1294`–`:1299`). A committed `dev/.cairn/handoff.lock`, plus a committed
  `dev/.cairn/handoff-owner`, which satisfies the designation gate as
  documented, put raw ESC/BEL on stderr under `session-end --handoff` (B6).
  The reclaim warning (`:1281`) and the prune warning (`:1358`) have the same
  shape.
* Identical before and after this commit, which did not touch these lines.

**Recommended:** route those fields through `_safe_field`.

### SW-SR-7 — informational: a named-pipe `.gitignore` hangs copy mode

`_read_regular_bytes` (`:620`) opens before it checks the file type, and
opening a named pipe for reading waits for a writer forever (A9b: timed out
at 10 s; the old kernel hung too). Git cannot carry a named pipe, so this
needs someone on the machine. **Recommended:** add `O_NONBLOCK` to the open
(the `fstat` regular-file check that follows stays).

### SW-SR-8 — informational: copy mode reads through links inside the canonical skills folder

A committed `.agents/skills/session-start/notes.md` linking to an outside
file was copied, as a plain file holding the outside bytes, into the ignored
`.claude/skills/` (forced copy). This is a read, not a write. In symlink mode
the harness reads through the same link itself. Noted so that "every write
is contained" is not read as "nothing is read from outside". No change
required.

### SW-SR-9 — informational: the fan-out guard's messages are absolute and can name the resolved path

`_assert_fanout_contained` (`:898`) now encodes its messages but prints the
absolute ancestor, and in its "outside the repo" branch it prints
`dst.parent.resolve()`, that is, where a link leads. With git's resolved root
that branch did not fire in any probe (link ancestors are refused first), and
the text is encoded, so there is no terminal risk. **Optional:** make it
project-relative, like `_assert_not_linked`.

## What I did not cover

* **Windows.** Not available. `O_EXCL` and `os.replace` against a link, the
  `O_BINARY`-only path, and NTFS junctions (which `is_symlink()` does not
  report) were argued, not run. Only the missing `O_NOFOLLOW` was simulated.
* **Linux and case-sensitive filesystems.** Everything ran on case-insensitive
  APFS; the case and trailing-dot rules were exercised there only.
* **A real win of the parent-folder race.** Forced wins only; my two racing
  attempts did not win, which does not show the race cannot be won.
* **The full suite and a mutation ledger.** Not rerun. I ran the three owning
  test files (115 passed) and relied on the commit's Boundary B record for
  the rest. The ordinary code review owns falsification.
* **What `intent.py` and `evolution_infer.py` write**, and the no-network
  property.
* Reads that do not write: a committed `dev/proposals/*.md` linking to a
  device file that never ends would stall the in-flight survey.
  Not measured.
* The `.claude/skills` symlink that `session-start` makes shows as untracked
  in a project that does not ignore it (seen in the C1 clone). That is
  ordinary behaviour, not reviewed.

## Security verification of the answer -- Claude Opus 5.5 -- 2026-10-19

**Obligation**: SW-SR-1 (above), answered by `a95b9b31`, `83b144f9` and
`7832d057`; plus confirmation that SW-SR-3 to SW-SR-7 are closed.
**Reviewed commit**: `7832d057`. `tools/session.py` is byte-identical to its
twin `templates/skills/_lib/session.py` (`cmp`), and unchanged from
`7832d057` to today's `master`.
**Distance**: a fresh session, not the implementing one. Same agent type,
different model size, so the distance is a fresh context. Security pass only.
**Single pass**: by the Maintainer's instruction there is no second round
("Let's just not iterate back and forth on the Security Review"). So each
finding below carries the exact fix and the test that shows it closed, and
the verdict says which answers a code review can sign off.
**Method**: reading, the two owning test files, and resolver-level cases in a
scratch file. Every scratch case asserts on what `_resolve_interpreter` or
`_binding_untrusted` returns; nothing a binding names was run. No full suite,
`CAIRN_FULL_SUITE` unset.
**Interpreter**: Python 3.13.13, `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
`PYTHONDONTWRITEBYTECODE=1`. Darwin, APFS (case-insensitive), git 2.53.0.
**Where things ran**: one detached worktree of `7832d057` and two more for
mutants, each in a fresh, uniquely named folder under the session
scratchpad, plus throwaway probe folders; all removed. The only writes to the
shared tree are the intent claim and this record.

**Verdict: SW-SR-1 CLEARED on the route it named.** A binding that came with a
`git clone` or a branch checkout is no longer run, under any spelling this
Mac's disk treats as the same file, through a link, inside a submodule, in a
linked worktree, or when git fails, hangs or prints something odd. I found no
path that returns a binding git's index lists. Six new findings, none
caused by a defect in the fix's own logic: 1 medium, measured (SW-SR-10); 1
medium, argued (SW-SR-12); 1 low (SW-SR-11); 3 informational.

**What a code review can close, and what it cannot.**
* SW-SR-11 to SW-SR-15: answered exactly as written below, they close without
  another Security Review; the code review checks each answer against its
  test. Until SW-SR-12 is answered, the clearance holds on APFS only, not on
  Windows or on Mac OS Extended (HFS+) drives.
* **SW-SR-10 I would not clear on a code review.** Its real fix moves the
  binding to a place no download or patch can carry, which changes the
  install contract and needs its own proposal and Security Review. The
  alternative is to accept the gap in writing, which is a risk decision.
  Either way it is the Maintainer's call. My recommended default is in the
  finding.

### In brief

**The hole SW-SR-1 named is closed.** The fix asks git one question, "list
everything you track", and checks the answer itself. That means it does not
depend on how git matches names. The questions I was asked about it come out
clean. Stripping the caller's git settings works. Putting back the two
settings the module chooses itself (no pager, no password prompt) cannot
point git anywhere else. Every failure, including a timeout, counts as "not
safe".

**But the fix works on a proxy.** It asks "does git track this file *now*?"
That stands in for the real question: "was this file written on this
machine?" A binding that comes with the project another way passes the check
and is run. I measured three such ways: a downloaded copy of the repository
followed by `git init`, a contributed patch applied with `git apply`, and the
common "undo last commit" (`git reset HEAD~`) (SW-SR-10). Separately, an
honest binding can name a Python *inside* the project folder, and checking
out a branch can replace that program (SW-SR-11).

**The name rule fits this Mac exactly.** I tried every character in every
letter position of the binding's three names, and slipped every character
into three places. The only foreign spelling this disk opens as the binding
is U+017F (long s) for the "s" of "json", and the rule catches it. But other
disks compare names differently: older Mac drives ignore some invisible
characters, and Windows has its own rules and short "8.3" names. There a
tracked look-alike would get through (SW-SR-12, argued, not measured). The
fix is to ask the disk, not model it: compare the file's identity.

**Fall back, don't stop.** When the binding is not trusted, the kernel uses
the Python already running it. That Python is already running the kernel
itself, so falling back gives the project nothing new. Stopping would protect
nothing more, and it would block every collaborator whenever someone
commits a binding by mistake.

### Findings at a glance

| id | what | severity | answer closes it on code review? |
|---|---|---|---|
| SW-SR-10 | the gate sees only git's index; a binding that arrives by a downloaded archive + `git init`, `git apply`, or `git reset HEAD~` is trusted and run (measured, resolver level) | **medium** | **no**: Maintainer decision (design change or accepted residual) |
| SW-SR-11 | an honest binding may name an interpreter inside the project; a branch checkout replaces that ignored file and the kernel runs the branch's program (measured, resolver level) | low (argued medium on Windows, where a venv's `python.exe` is a real file in the project) | yes |
| SW-SR-12 | the name fold models APFS; on HFS+ (ignored invisible characters) and NTFS (dotless i, 8.3 short names) a tracked look-alike is the same file but not the same folded name | **medium** (argued, not measured) | yes; the mechanism test runs on any disk |
| SW-SR-13 | the two "equivalent" encoder mutants on exception text are survivors: a printable-invisible character tells them apart (measured, 2 of 2) | informational | yes |
| SW-SR-14 | a non-UTF-8 binding and a binding holding a lone surrogate end in a Python traceback, not a refusal; a tracked binding reaches both, since the gate runs last | informational | yes |
| SW-SR-15 | the project folder's path still reaches the terminal raw in three messages, plus `sys.executable` in the stale message and the interpreter path in three run-failure messages | informational | yes |

### Q1 -- Does SW-SR-1 clear? Reading the gate

`_resolve_interpreter` runs its shape checks (all read-only: one JSON read,
`lstat`/`stat`, `os.access`), then `_binding_untrusted`, then returns. Every
process start in the module is accounted for. Two git calls run before it
(`_repo_root`, `_git`) and one inside it. The three that run the interpreter
(`_intent_whoami`, `_surface_intents`, `_prune_intents`/`_run_evolution_infer`)
all take it from `_resolve_interpreter`. No other shipped reader of the
binding exists: `git grep local-env` outside the deliberation record finds
only the kernel, the engine's writer `write_local_env`, and a path list in
`claim_check.py`.

* **Links.** `_assert_not_linked(cfg, root)` runs before git is asked. It
  refuses a link at any folder between the project and the file, or at the
  file. A tracked `dev/.cairn` link is caught (tested).
* **Index reading and parsing.** One argument list,
  `git ls-files -z --cached --stage`, with no pathspec, so pathspec magic and
  `GIT_LITERAL_PATHSPECS` no longer matter. With `-z` git never quotes, and
  each record is `mode object stage TAB path`. The code splits at the first
  tab, which is right because the head can hold no tab. A record with no tab
  or no head means "could not ask". Names that are not UTF-8 are decoded with
  replacement characters and cannot fold onto an ASCII name. Index states
  checked: assume-unchanged and skip-worktree (tested); conflict stages
  (listed once per stage, by reading); **a sparse index** (measured:
  `ls-files` without `--sparse` expands a `dev/` sparse-directory entry, so
  the binding is still listed).
* **Submodules.** A `160000` entry whose folded path is a whole-folder prefix
  of the binding gives its own reason. A gitlink at exactly the binding's
  path gives "tracked". `de` does not count as `dev`, and a plain file called
  `dev` is not a submodule (both tested).
* **Worktrees and the `.git` file form.** Git finds the repository from the
  folder alone, so a linked worktree and a project that is itself a
  submodule both read their own index (tested, tracked and untracked).
  A checkout cannot create a `.git` file or folder, since git refuses that
  name at any depth.
* **The environment.** `_binding_git_env` drops every `GIT_*` name (compared
  upper-cased) and puts back `GIT_PAGER=cat` and `GIT_TERMINAL_PROMPT=0`.
  Those two are the module's own constants, not the caller's values. Neither
  one can choose a repository, an index or a matching rule. `ls-files` writes
  to a pipe, so no pager starts, and it never asks for credentials. **Putting
  them back does not matter.** What remains outside `GIT_*` is the operator's
  own: `HOME`/`XDG_CONFIG_HOME` choose their global config, and `PATH`
  chooses which `git` runs. That is the same `git` that `_repo_root` has
  already run, so a project-controlled `PATH` entry would own the session
  before the gate. `_repo_root` still honours a caller's `GIT_DIR` and
  `GIT_WORK_TREE`. The gate then asks about that folder by discovery, which
  either agrees or fails, and failing falls back.
* **Failures fail closed.** Git missing, an `OSError`, a timeout (`run` kills
  the child), a non-zero exit, or output it does not understand all give
  `_BINDING_UNVERIFIED` and the fallback. A silent success means "nothing
  tracked", correctly (all tested).

**Tests.** `test_session_binding_untracked.py` and
`test_session_writes_contained.py` at `7832d057`: **196 passed (48 + 148), 0
skipped, 0 failed, 13.9 s**. I checked that each variant test exercises what
its name says:
* The resolver-level variants assert on the return value: the source is
  `fallback-untrusted` and the interpreter is `sys.executable`.
* The case and long-s tests take their asserting branch here. I measured that
  this disk opens both spellings as the binding.
* Two variants are weaker than their names. `GIT_CEILING_DIRECTORIES` set to
  the project's parent cannot redirect discovery from the project folder, so
  it pins the strip without showing a harm. `GIT_LITERAL_PATHSPECS` is moot
  now that there is no pathspec; it was red only against the old form. The
  submodule tests assert the fallback but not which reason. None of these is
  a gap in what the gate does.
* The encoding tests use a C1 control and a bidi override. Python's `repr()`
  already escapes both, which is why two mutants survived (SW-SR-13).

**Resolver-level scratch cases** (12, all passing on `7832d057`; each asserts
a return value). Three show the SW-SR-10 routes trusted. One shows the
SW-SR-11 replacement trusted. Two pin the exception-text encoding. Two
document the spellings the fold does not equate. One shows an ASCII case
variant gives the "tracked" reason. One is the sparse index. Two are the
SW-SR-14 tracebacks.

**Mutation ledger** (separate fresh worktree per mutant, both twins mutated;
control: unmutated, 48 + 12 passed):

| mutant | `test_session_binding_untracked.py` | scratch case | result |
|---|---|---|---|
| M1: drop `encode_display` on the read-error exception text | 48 passed | `test_read_error_text_is_encoded` failed | survived the shipped tests; killed by the scratch case |
| M2: drop `encode_display` on the could-not-inspect exception text | 48 passed | `test_inspect_error_text_is_encoded` failed | survived the shipped tests; killed by the scratch case |

**The disk measurement.** On this APFS volume, with `dev/.cairn/local-env.json`
present, I opened every candidate spelling and compared device and inode.
Candidates: each letter of `dev`, `.cairn` and `local-env.json` replaced by
every non-ASCII code point; every code point inserted into `local-env.json`
at two places and into `.cairn` at one. One hit: U+017F for the `s` of
`json`. No insertion matched, so APFS ignores no invisible character. The
fold is exact for this disk and only over-folds, which fails closed.

### Q2 -- Fall back or refuse

**Can project data influence `sys.executable`?** Only through how the
operator starts the kernel. The skill says `python tools/session.py
session-start`, and `python` comes from the operator's `PATH`. A project can
steer that only through the operator's own tools. Examples: a `.python-version`
file for pyenv, which picks among installed versions (older pyenv also
allowed a path, CVE-2022-35861); an editor that activates a project `.venv`
on its own; `uv run`; `direnv` or `mise` once trusted. In every such case the
same interpreter is already running the kernel's own code before any check.
The kernel cannot be safer than the program running it, and falling back
hands the sub-tools nothing that program did not already have.

**Recommendation: keep fall-back with the warning.** Reasons:
1. The property the gate exists for, that project data does not choose a
   second program, holds fully under fall-back. `fallback-untrusted` runs
   exactly what a fresh clone with no binding runs.
2. The honest failure is common: someone runs `git add -f`, or commits before
   the ignore line existed. Refusing would stop every collaborator's session
   in that project until history is fixed. A warning keeps them working and
   names the fix.
3. Cairn's own rule is that tools warn and refuse only for a genuine safety
   property. Here the fallback already secures that property.

Optional, not a finding: the reason goes to stderr. Stdout carries only
`(from fallback-untrusted)`. An agent that relays stdout alone would drop the
"why", and repeating the reason under "resolved project interpreter" would
fix that. SW-SR-1's two *recommended* (not required) items were not done and
are not needed to clear it. The installer still keeps an existing binding
silently (`write_local_env` → `skipped-exists`), which matters for SW-SR-10.
The interpreter line still prints after `_surface_intents` has run.

### Q3 -- Messages

**Confirmed for every value that can come from a binding git has not
vouched for:**
* the binding file's path (`shown_cfg`, encoded: the project folder's name
  may come from a clone URL);
* the interpreter text (`shown_interp`), in the vanished, parent-traversal,
  could-not-inspect and not-executable messages;
* the exception text in the read and inspect refusals;
* the `session-start` interpreter line;
* `_intent_whoami`, which repeats the refusal already encoded where it was
  made.

The three `_BINDING_*` reasons are fixed words.

**The fixer's equivalence claim is half right.** It holds for the JSON
error, whose text is fixed words plus a position. It also holds for control
and bidi characters, which `repr()` escapes inside `OSError` text. It fails
for the printable-invisible characters (U+3164 Hangul filler, U+034F, the
variation selectors). `repr()` leaves these raw, and the encoder's range
table exists for exactly them. Measured: both mutants are killed by a
U+3164 in the project folder or the interpreter path (SW-SR-13). The code is
right; the pin is missing.

**The raw `sys.executable` in the stale message is acceptable.** It is the
operator's own path. Project text reaches it only when the operator starts
the kernel from an interpreter inside a folder someone else named. Encoding
it is one call, so I list it under SW-SR-15. The interpreter path also
appears unencoded inside the `OSError` text of three run-failure warnings
(`could not run intent.py list`, `intent prune failed to run`,
`could not run evolution_infer.py`). Those need a binding that passed the
gate, and `repr()` covers control characters there. They are in SW-SR-15
for the same reason.

### Q4 -- The fold

**Canonical caseless matching is the right rule for APFS** (measured above).
Folding more than the disk does is the right way to be wrong. My concerns:
1. It is a model of one disk. Other disks compare names differently
   (SW-SR-12). The robust rule asks the disk: compare device and inode.
2. On a case-sensitive disk (Linux), a tracked `DEV/.cairn/local-env.json` is
   a *different* file. The honest binding is still set aside, and the
   remedy says `git rm dev/.cairn/local-env.json`, a path git does not track
   there (scratch case: the reason is "tracked" and the remedy names the
   plain spelling). A hostile project can use this to switch off every Linux
   user's binding. The result is the current interpreter, which is what a
   fresh clone gets anyway, so the cost is a wrong remedy, not a hole. The
   fix in SW-SR-12 names the entry git actually tracks.

The fixer's choice to fail closed is right. I have no other concern.

### Q5 -- SW-SR-3 to SW-SR-7, by reading

* **SW-SR-3 closed.** `_write_replacing` sets the kept mode with
  `os.fchmod` on the open descriptor after a flush, skipped where the
  platform lacks it. A name swapped for a link can no longer carry the change.
* **SW-SR-4 closed, and the recheck is sound.** `_read_regular_bytes` takes
  `lstat` (no link followed), refuses a non-regular file, opens, and
  requires `fstat` to show a regular file with the same device and inode.
  A link swapped in leads to a different file, which has its own inode.
  The only way to match is the same file under another name (a hard link),
  and then its bytes were already the project file's own. Inode reuse gains
  nothing: a reused inode holds bytes the racer just wrote, never an existing
  outside file's. One residue, no finding: where `O_NOFOLLOW` is missing, a
  swapped-in device file is *opened* before the check refuses it.
  `O_NONBLOCK` keeps that from hanging, and the platform that lacks the flag
  (Windows) has no named pipes on disk.
* **SW-SR-5 closed.** `_heal_skill_copy`'s planning loop refuses a non-folder
  where a folder must go with a `LifecycleError`, which `cmd_session_start`
  turns into a warning. No copy is written first. The `.gitignore` seed still
  lands before the copy plan refuses, by design ("the ignore entry first").
  It is the idempotent line the module wants anyway.
* **SW-SR-6 closed.** The full-handoff manifest names, the lock refusal's
  agent, pid and host, the reclaim warning's agent and the prune warning go
  through `encode_display`. The reclaim warning's pid is printed raw but is
  checked to be an `int` on that branch. The lock refusal's `self.path` is
  still raw (SW-SR-15).
* **SW-SR-7 closed.** The type is checked by `lstat` before the open, and the
  open adds `O_NONBLOCK`.

### Findings

#### SW-SR-10 -- medium: the gate sees only git's index, so a binding that arrives another way is trusted

**Plain:** the check asks git "do you track this file now?" A binding can
come with a project without being in git's index. Then it passes, and the
kernel runs the program it names, which is SW-SR-1's consequence by another
road.

* **Measured** (resolver level, returns `(program, "local-env.json")`):
  `git archive` of a repository that tracks a binding, unpacked, then
  `git init` (what "Download ZIP" plus a new repository gives);
  `git apply` of a patch that creates the binding (no `--index`, so the
  index is untouched); and `git reset HEAD~` after the commit that added it.
  The shipped test `test_an_untracked_binding_resolves_and_a_tracked_one_falls_back`
  already shows `git rm --cached` does the same. The tracked-binding remedy
  rightly says plain `git rm`, but `git rm --cached` is the widely taught
  "untrack, keep locally" idiom.
* The installer keeps such a binding without a word
  (`write_local_env`: `skipped-exists`).
* No check based on the index can see these routes. The signal itself is the
  limit.

**Fix (the Maintainer chooses):**
* **(a) Full fix, recommended for later.** Its own proposal and Security
  Review, because it changes the install contract. Move the binding into
  git's own folder (`git rev-parse --git-common-dir` + `/cairn/local-env.json`).
  No checkout, archive, patch or ZIP can carry a file there. The old path is
  then read only to say "not used; re-run the install". A repository that
  arrives with its own `.git` folder is already hostile to every git call,
  so it is out of scope.
* **(b) Interim, recommended now as the default.** Accept the residual in
  writing. In the `_resolve_interpreter` docstring and `bootstrap/SAFETY.md`'s
  residuals, add one sentence saying the gate proves only "git's index does
  not list the file now". Name the routes: a downloaded archive followed by
  `git init`, `git apply`, `git reset`, `git rm --cached`.
* **Test for (a):** the three scratch cases above, plus `git rm --cached`,
  each ending at `fallback` or `fallback-untrusted`.
* **For (b):** a claim-checked prose change, no test.

#### SW-SR-11 -- low (argued medium on Windows): an in-project interpreter can be replaced by a checkout

**Plain:** an honest binding may name a Python inside the project folder (an
ignored `env/` or `.venv/`). Git treats ignored files as expendable. Checking
out a branch that tracks that path overwrites the program, and the gate does
not look at it.

* **Measured** (resolver level): the binding names `env/bin/python3`, an
  ignored regular file. Checking out a branch that tracks that path rewrote
  the file, and `_resolve_interpreter` still returned it with source
  `local-env.json`.
* **Reach.** The installer writes `Path(sys.executable).resolve()`, so a
  symlinked venv on macOS or Linux points outside the project. The case needs
  a conda prefix inside the project (`conda create -p ./env`) or
  `venv --copies`. On Windows, a venv's `Scripts\python.exe` is a real file
  inside the project, so this is the normal case there (argued; no Windows
  run).

**Fix:** in `_binding_untrusted`, give it the interpreter. When it lies under
`root` (`Path(value).relative_to(root.resolve())` succeeds; `_probe_interpreter`
has already refused links), compare its project-relative path against the
**same** listing, with the same fold and the same `160000` prefix rule.
Return a new fixed-text reason, `_INTERPRETER_TRACKED`: the interpreter is
inside the project and tracked by git, so it was not used.

**Test:** add the scratch case
`test_a_checkout_can_replace_an_in_tree_interpreter_the_binding_names` to
`test_session_binding_untracked.py`, with its last assertion changed to
`(sys.executable, "fallback-untrusted")`. Keep its middle assertion as the
control: before the checkout, the untracked in-project interpreter still
resolves.

#### SW-SR-12 -- medium, argued not measured: the name fold models APFS, not every disk

**Plain:** the fix decides "same file" by comparing folded names. That
matches this Mac exactly. Other disks treat other spellings as the same
name, and there a tracked look-alike is opened as the binding while its
folded name differs.

* **HFS+ (Mac OS Extended, still common on external drives)** ignores
  U+200C to U+200F, U+202A to U+202E, U+206A to U+206F and U+FEFF in names.
  Git's own guard for `.git` skips exactly these. A tracked
  `dev/.cai<U+200C>rn/local-env.json` is the binding there; the fold leaves
  U+200C in place (scratch case: `_binding_untrusted` returns `None` for
  that listing).
* **NTFS** compares upper-cased names. U+0131 (dotless i) upper-cases to `I`,
  but case folding leaves it alone (scratch case, same result for
  `dev/.ca<U+0131>rn/...`). With 8.3 names on, a folder `.cairn` also has a
  short name. Git writes through a short name for any folder but `.git`. A
  tracked `dev/<short name>/local-env.json` then lands in `dev/.cairn`, and
  no name fold can see it.
* **Argued, not measured.** There is no HFS+ volume or Windows machine here,
  and the binding tests skip on Windows entirely (`pytestmark`), so the gate
  has never run there.

**Fix:** keep the fold. Also compare identity: take `os.stat(cfg)` once.
* For every index entry whose path has exactly three parts, `os.lstat(root
  / entry)`, ignoring `OSError`. Equal `(st_dev, st_ino)` means tracked.
* For every `160000` entry with one or two parts, compare its identity with
  `root / "dev"` or `root / "dev" / ".cairn"`. Equal means in a submodule.
* When the match came from the fold or from identity rather than the exact
  name, the message adds "git tracks it as <entry>", with the entry through
  `encode_display`, so the `git rm` remedy works (Q4 point 2).

**Test (runs on any disk):**
* In the test's temporary project, make a file `alias.json` beside the
  binding (same folder) as a hard link to it. Stub the listing to that one
  entry. `_binding_untrusted` returns the tracked reason, and the message
  names that entry.
* Control: a separate file of the same name, not a link, gives `None`.

A Windows run is still owed before anyone claims the gate on Windows.

#### SW-SR-13 -- informational: two encoder calls on exception text are unpinned

The fixer's ledger recorded the encoder calls on the read-error and
could-not-inspect exception text as equivalent mutants. They are survivors.
A U+3164 (Hangul filler) in the project folder or interpreter path reaches
the message raw when either call is removed (measured, 2 of 2 killed by the
scratch cases).

**Fix:** no code change. Add the scratch cases `test_read_error_text_is_encoded`
(binding at mode 000 in a folder named `p<U+3164>`) and
`test_inspect_error_text_is_encoded` (interpreter
`/tmp/` + 300 × `a` + U+3164 + `/python`) to `test_session_binding_untracked.py`.

**Test:** each must fail with its call removed and pass without the removal.

#### SW-SR-14 -- informational: two binding shapes end in a traceback, not a refusal

* A binding holding the byte `0xff` raises `UnicodeDecodeError` from the
  read. The handler catches only `OSError` and `JSONDecodeError`.
* `{"interpreter": "/x\ud800y"}` (a lone surrogate) raises
  `UnicodeEncodeError` from `stat()` in `_probe_interpreter`, since
  `is_symlink()` swallows it first and the caller catches only `OSError`.
* Nothing runs in either case. But session-start dies with a Python
  traceback, and because the gate runs last, a tracked binding chooses this.
  Measured, resolver level.

**Fix:**
* Catch `(OSError, ValueError)` on the read, which covers
  `UnicodeDecodeError` and `JSONDecodeError`, with the same "not readable
  JSON" refusal.
* Catch `(OSError, ValueError)` around `_probe_interpreter`, with the same
  "could not be inspected" refusal.
* Optional, the fixer's call: run `_binding_untrusted` before the read, so a
  tracked binding's content is never read or printed. That changes two
  pinned behaviours
  (`test_a_malformed_binding_still_refuses_even_when_tracked`,
  `test_a_tracked_binding_to_a_vanished_interpreter_keeps_the_stale_message`).

**Test:** add the scratch cases `test_a_non_utf8_binding_is_a_traceback_not_a_refusal`
and `test_a_lone_surrogate_interpreter_is_a_traceback_not_a_refusal`, with
both changed to expect `LifecycleError`.

#### SW-SR-15 -- informational: a few paths still reach the terminal raw

The fix encodes the binding file's path because "a folder name may be
someone else's choice". The same folder name is still printed raw in:
* `_assert_within` (`base`, `path`);
* `_heal_skill_symlink` ("exists as a non-symlink", `dst`);
* `HandoffLock._reclaim_or_refuse` (`self.path` in the refusal).

`sys.executable` is raw in the stale message (Q3). The exception text is
raw in `_surface_intents`, `_prune_intents` and `_run_evolution_infer`'s
run-failure warnings.

**Fix:** wrap each of these values in `encode_display` (`str(...)` first).

**Test:** one parametrized test over the seven sites. Use a project folder
named `p` + U+009B + U+202E for the three path sites, a monkeypatched
`sys.executable` holding the same two characters for the stale message, and
a monkeypatched `subprocess.run` raising `OSError(8, "Exec format error",
<that path>)` for the three run sites. Assert with the existing
`_assert_inert`. Add a U+3164 case so `repr()` cannot hide a missing call
(SW-SR-13).

### What I did not cover

* **Windows and HFS+.** Neither is available here, and the binding tests skip
  on Windows. SW-SR-11's Windows reach and all of SW-SR-12 are argued from
  documented disk behaviour and git's own guards, not run.
* **Linux and case-sensitive disks**, and the optional case-folding folders
  some Linux file systems offer. Q4 point 2 was shown with a stubbed
  listing, not on such a disk.
* **Other git versions.** Only 2.53.0. In particular, I did not check how
  older versions expand a sparse index in `ls-files`.
* **Hostile end-to-end runs.** Excluded by the brief. Every case here is
  resolver-level, and nothing a binding names was executed.
* **Races** on the binding between its read and the gate. These need a
  process already on the machine.
* **The full suite.** Excluded by today's rule. I ran the two owning files
  (196) and my 12 scratch cases.
* **What `intent.py` and `evolution_infer.py` do** under the interpreter
  they are given.
