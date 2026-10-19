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
