# Security Review — engine copy fallback (`cf707e2a`) — Claude Opus 5.5 — 2026-10-19

**Obligation**: the Security Review of the repair for SW-SR-2
(`dev/plans/archive/2026-10-18-security-review-session-writes.md`, at `598aa6be`).
The repair changes the scaffold engine (`bootstrap/_scaffold/`), a named
high-risk surface in `AGENTS.md`. It has no proposal or plan.
**Reviewed commit**: `cf707e2a` ("Installer fan-out: no copy, quarantine or
probe write goes through a link or leaves the project"):
`bootstrap/_scaffold/install.py` (`_symlinks_available`,
`_emit_skill_copy_fallback`), `bootstrap/_scaffold/SECURITY_MUTATIONS.md`, and
the new `bootstrap/tests/test_engine_copy_fallback_contained.py`. The "before"
engine is its parent `2e1c9b3b`.
**Distance**: a fresh session, not the implementing one. The commit credits a
different model size of the same agent type, so the distance is a fresh
context, not a different type. This is a security pass only; a separate code
review does the ordinary falsification.
**Interpreter**: Python 3.13.13 at `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
`PYTHONDONTWRITEBYTECODE=1`. Platform darwin, APFS (case-insensitive), git 2.53.0.
**Where things ran**: a detached worktree of `cf707e2a` and one of its parent,
each in a fresh, uniquely named folder under the session scratchpad; four
`git archive` extractions of `cf707e2a` for the mutants; throwaway probe
folders beside them. All removed when done. The only writes to the shared tree
are the intent claim and this record.

**Verdict**: **SW-SR-2 CLEARED.** 0 findings block it. 5 findings: 2 low,
3 informational.

## In brief

**The hole is closed.** On the old engine, a committed folder at the old
probe name made the installer copy instead of link, on macOS, and a link at a
copy name then let the project create or change files outside itself. I
measured all of it again through the real installer, including with
repositories committed and cloned with git: a new `.zshenv` outside holding
the project's line, a file moved into an outside folder, an outside file
rewritten in place. On the new engine, the folder no longer changes anything,
and when copying is genuinely needed (no links possible), every one of those
shapes is refused before the installer writes a single copy, and nothing
outside changes.

**Upgrade too.** The implementer had not tested `upgrade --apply` end to end.
I did: an apply that adds the skills over the same hostile data. The old
engine wrote outside in all three ways. The new one finished the upgrade,
refused the fan-out with a one-line warning, and left both the outside folder
and the harness folder untouched.

**The remaining gap is the accepted one.** A folder on the way to a copy can
still be swapped for a link between the check and the write. That needs a
program already running on the machine. I forced it, and in a real race I won
it once in 3,000 runs (a stray temporary file outside). This is the window
`bootstrap/SAFETY.md` already accepts, and the commit names it honestly.

**Two small things to fix.** (1) The warning printed when a copy had been
edited prints the project's own file names raw, so a crafted name can put
terminal control codes on the screen (CF-SR-1). The fix is one function the
commit already has. (2) The commit's claim that dropping either of two safety
flags is harmless is half wrong: one flag carries the protection and the other
adds nothing. The code is right; the tests would not notice the important flag
being removed (CF-SR-2).

## Findings at a glance

| id | what | severity | blocks SW-SR-2? |
|---|---|---|---|
| CF-SR-1 | the copy-divergence warning prints project file names (and the absolute harness path) raw: a committed file name put ESC/BEL sequences on the terminal | low | no |
| CF-SR-2 | `O_EXCL` and `O_NOFOLLOW` are not an equivalent pair: dropping `O_EXCL` passes every shipped test, and then a hard link at the temporary name has the copy written into an outside file | low (test gap; the code is correct) | no |
| CF-SR-3 | a second last-name gap, not named: a racing program that swaps the temporary file for a link gets its link renamed into the copy name (5 of 3,000 runs). Nothing is written outside | informational | no |
| CF-SR-4 | on the `upgrade --apply` route the refusal says "then re-run", but re-running the upgrade does not redo the fan-out | informational | no |
| CF-SR-5 | `[skip]` lines and others print the absolute target path raw; the project cannot choose those names, only the person typing the target can | informational (not on this path) | no |

## Q1 — Is SW-SR-2 closed?

### Every write on the fan-out path, listed from the tree

Found by an AST walk of the five fan-out functions in
`bootstrap/_scaffold/install.py` for every call that writes, moves, removes,
links, opens, guards or prints. The walk's instrument was confirmed: it lists
the `os.symlink` calls known to be there. Then I read each hit in place and
traced the two callers, `main` (`bootstrap/_scaffold/cli.py:539`) and
`_apply_upgrade` (`bootstrap/_scaffold/upgrade.py:2231`). Line numbers are at
`cf707e2a`.

| # | write | where | guard | disposition |
|---|---|---|---|---|
| F1 | probe: `os.symlink(".", probe)`, then `probe.unlink()` | `install.py:499`, `:506` | a random name each call, directly under the resolved target | **safe.** Creating a link never follows one and fails on a taken name. A folder at the old name no longer forces copying (measured through the CLI, Q1); the shipped test pins the prefix variants. Side benefit: the old probe **deleted** a committed file at its fixed name (measured); the new one leaves it alone. |
| F2 | link mode: `dst.unlink()` (only when `dst` is a link), `dst.parent.mkdir`, `os.symlink(rel, dst)` | `:519`, `:527`, `:528` | `_assert_fanout_contained` at `:719` (link ancestors refused; `dst` itself may be the link it replaces) | **safe, unchanged.** Removes and makes only a link, inside the project. A planted `.claude/skills` link to an outside folder is replaced by the right link; nothing outside changes (L1). |
| F3 | quarantine: `os.replace(out, bak)` | `:637` | `check(bak)` → `_assert_safe_write` (`:587`), plain-file test, all before the first write | **closed.** A rename replaces a link at `bak`; it never moves into the folder a link names (E4, R1b). A hard link at `bak` is replaced; the outside file's bytes and time are unchanged, only its link count drops because the project's name for it is gone (H3, identical on the old engine). |
| F4 | `out.parent.mkdir(parents=True, exist_ok=True)` | `:639` | every folder on the way checked for links (`_assert_safe_write`) and for "file where a folder must go" first | **closed** for data present at the check. Follows a folder swapped in later: the accepted window (Q2). |
| F5 | copy: `os.open(tmp, O_CREAT\|O_EXCL\|O_NOFOLLOW)`, write through the descriptor, `os.replace(tmp, out)`, `os.unlink(tmp)` on failure | `:641`–`:648` | `check(out)` for the whole set first; exclusive create; rename | **closed.** No mode change by name (the kernel's SW-SR-3 has no twin here). A link at `out` is replaced, not followed (E3, E5, E6, R1). A hard link at `out` is renamed aside or left alone; never written into (H1, H2). The temporary-name gap is CF-SR-3. |
| F6 | `seed_gitignore(target, (".claude/skills/",))` in copy mode, and `seed_gitignore(target, _SKILLS_GITIGNORE)` after an upgrade fan-out | `:728`; `upgrade.py:2234` | `_assert_safe_write` (`install.py:235`) | **unchanged.** A linked `.gitignore` is refused (the earlier repair). A hard-linked one is still written through (GS-SR-4, known, git cannot carry one). |
| F7 | the terminal | `:521`, `:653`, `:731`; `cli.py:541`; `upgrade.py:2233` | refusals: `shown()` (project-relative, `ascii()`-escaped) | refusals clean; **the divergence warning at `:653` is not** (CF-SR-1). |

### Probes through the real installer

Every case is a fresh project with a harness folder (`.claude/`), a folder
outside it holding a sentinel, and a profile outside it. The real
`bootstrap/scaffold.py` ran as a subprocess. "Links impossible" runs the same
command through a three-line wrapper that makes every `os.symlink` call fail
the way it does on Windows without Developer Mode, so the engine's own probe
decides. The outside folder is snapshotted with no link followed (bytes,
modification time, link count, link targets), before and after.

**Shapes** (each plants the old forcing folder `.cairn-symlink-probe/keep`
unless noted):

* E3 copy name a dangling link to an outside path; E4 a divergent copy and its
  quarantine name a link to an outside folder; E4b the same to a missing
  outside file; E5 copy name a link to an outside file holding the canonical
  bytes; E6 the project's own skill set to `touch ZSHENV_MARKER` and its copy
  name a dangling link to `outside/.zshenv`;
* H1 copy name a hard link to an outside file; H2 the same with the canonical
  bytes; H3 quarantine name a hard link to an outside file;
* L1 `.claude/skills` a link outside; L2 a skill folder a link outside; L3
  `.claude` a link outside; L4 a skill folder a link to `dev/` inside; L5
  `.claude/skills` a link to the canonical folder (the normal link-mode state);
* P1 a FIFO at a copy name; P2 a FIFO at a quarantine name; P3 a file where a
  copy folder must go;
* X1 a canonical file and a differing copy, both named
  `ESC]0;RETITLED BEL ESC[2J.md`;
* control (nothing planted) and a committed **file** at the old probe name.

19 shapes, run as a plain install and as `--force` (17), so 36 runs per mode
and engine.

| engine | mode | copy path chosen | outside changed | refused before any write |
|---|---|---|---|---|
| old `2e1c9b3b` | native | **forced in all 34**: 20 finished copying; L1, L2, L4, L5 refused and P1, P3 crashed inside the copy code; L3 was refused just before it | **E3, E4, E5, E6, H2** (and H3's link count); `--force`: **E3, E4, E6** | L1–L5 (exit 2); P1, P3 crash with a traceback (exit 1) |
| new `cf707e2a` | native | **0 of 36** | none | L3 (the pre-existing `.claude` link refusal) |
| old | links impossible | all | **E3, E4, E5, E6, H2**; `--force`: **E3, E4, E6** | L1–L5; P1, P3 traceback |
| new | links impossible | all | none (H3's link count only, as on the old engine) | E3, E4, E4b, E5, E6, L1, L2, L4, L5 "refusing to write skill copies through a link or outside the project: `<name>`"; L3 the fan-out guard; P1, P2, P3 "not a plain file" / "a file is where a folder must go" (exit 2, no traceback) |

What the old engine did outside, measured: E3 created `created-by-install`
holding the skill; E4 moved `SKILL.md` into the outside folder; E5 and H2
rewrote the outside file in place (bytes equal, new modification time; H2
through a hard link); E6 created `outside/.zshenv` holding
`touch ZSHENV_MARKER`. On the new engine H1 and H2 leave the outside file
exactly as it was, H2 included (the "already current" skip).

**Committed and cloned with git.** E3, E4, E5, E6 and X1, each built in a
source repository, committed, and cloned with `git clone`; the installer ran
on the clone.

| engine | mode | result |
|---|---|---|
| old | native | copy path 5 of 5; outside changed in E3, E4, E5, E6 (`.zshenv` created holding `touch ZSHENV_MARKER`) |
| new | native | copy path 0 of 5; outside unchanged 5 of 5 |
| new | links impossible | E3–E6 refused, exit 2, outside unchanged; X1 exit 0 with raw ESC on stderr (CF-SR-1) |

**`upgrade --apply` adding the skills.** Install; turn the tree into a
pre-skills adopter (the skills dropped from the lockfile and deleted, as
`bootstrap/tests/test_skills_upgrade.py` does); plant the forcing folder, a
project skill `.agents/skills/evil/SKILL.md` holding `touch ZSHENV_MARKER`
with its copy name a dangling link to `outside/.zshenv`, a divergent
`session-end` copy whose quarantine name links to an outside folder, and a
`session-start` copy name linked to an outside file holding the canonical
bytes. Then `upgrade --stage` and `upgrade --apply` through the CLI.

| engine | mode | stage / apply | skills recorded | outside changed |
|---|---|---|---|---|
| old | native | 0 / 0 | yes | **`.zshenv` created, `bakdir/SKILL.md` moved in, `keep.txt` rewritten** |
| old | links impossible | 0 / 0 | yes | **the same three** |
| new | native | 0 / 0 | yes | none; `.claude/skills exists as a non-symlink; leaving it untouched` |
| new | links impossible | 0 / 0 | yes | none; `[warn] skills fan-out skipped: refusing to write skill copies through a link or outside the project: .claude/skills/evil/SKILL.md` and the harness folder untouched |

So no fan-out write leaves the project, follows a link present at the check,
or changes an outside file, on any route I could reach. The one sense in which
an outside file "changes" is H3's link count: removing a project's name for a
file is not a write to it.

The commit's own 33 tests pass on `cf707e2a` (33 passed, 1.98 s). With
`test_skills_fanout.py` and `test_security_leaf.py`, 47 pass in the worktree;
adding `test_skills_install.py`, 52 pass on an archive copy of the commit. One note for the code reviewer, not a finding: the commit's Boundary
B ran on base `1e4f1e96`, not on the parent `2e1c9b3b`. The engine bytes are
identical between the two; `templates/skills/` (the canonical skills the
fan-out copies) changed in `08c946a6` and `a95b9b31`.

## Q2 — The check-to-write gap

The commit says the one remaining gap is a parent folder swapped for a link
between the check and the write, which needs a program already running on
the machine, and that a link appearing at a copy or quarantine name after the
check is replaced, not followed. Both hold. Measured against the engine in
copy mode, 3,000 runs each:

| probe | result |
|---|---|
| R1: a racing thread keeps putting a link to an outside file at the copy name | 108 clean, 2,892 refused at the check, **0 files outside** |
| R1b: a racing thread keeps putting a link to an outside folder at the quarantine name | 1,247 runs quarantined, 1,753 refused, **0 entries outside** |
| R2: a racing thread swaps every `.cairn-write-*` temporary file for a link (24,902 swaps) | 3,000 clean, **0 files outside**; but the copy name **ended as the racer's link in 5** (CF-SR-3) |
| R3f: forced, the skill folder swapped for a link to an outside folder right after the last check | the copy is written **outside** |
| R3q: the same, on a run that quarantines | an outside `SKILL.md` is **renamed** to `SKILL.md.diverged.bak` and replaced |
| R3r: a real race, a thread swapping the skill folder for an outside link and back | 2,998 clean, 2 `OSError`, **1 stray `.cairn-write-…` file left outside** |

So the parent-folder window is real, I won it for real once, and within it the
engine can create, rename or replace files outside. That is exactly the class
`bootstrap/SAFETY.md` accepts as residual (1), "a small TOCTOU window between
the scaffold engine's `_assert_safe_write` containment check and the write"
(`bootstrap/SAFETY.md:243`), under its stated model of no concurrent
filesystem attacker. A program that can win it could write those files
itself, so it gains nothing. The bound is honest. Two refinements, neither
owed: because the whole set is checked before the first write, the window for
the last file spans the writes of all the earlier ones (milliseconds, not a
different class); and a stray temporary file can be left outside, because its
cleanup removes it by name through the restored folder.

## Q3 — Is `O_EXCL` / `O_NOFOLLOW` an equivalent pair?

**No. Only one half is equivalent.** POSIX makes `O_CREAT|O_EXCL` fail on any
existing name, a link included, so with `O_EXCL` present `O_NOFOLLOW` adds
nothing at the last name. The reverse does not hold: `O_NOFOLLOW` only refuses
a *symbolic* link. A hard link or a plain file at the name opens normally, and
without `O_TRUNC` the write overwrites the start of whatever is there.

Measured on four `git archive` copies of `cf707e2a` (one unmutated control,
three mutants), with the temporary name made guessable as the shipped test
does, and three things planted at it:

| copy | symbolic link to outside | hard link to an outside file | longer plain file inside | shipped tests (4 files) |
|---|---|---|---|---|
| control | refused (`FileExistsError`) | refused | refused | 52 passed |
| no `O_EXCL` | refused (`ELOOP`) | **outside file overwritten**; the copy name becomes a hard link to it | **copy holds non-canonical bytes** | **52 passed: survived** |
| no `O_NOFOLLOW` | refused | refused | refused | 52 passed: equivalent, measured |
| neither | **outside written** | **outside written** | non-canonical | 1 failed: killed |

The shipped test kills only "neither", because it plants only a symbolic link.
On Windows, the platform copy mode exists for, `O_NOFOLLOW` is absent
(`getattr(os, "O_NOFOLLOW", 0)`), so `O_EXCL` is the only defence there. This
is CF-SR-2. The code itself is correct.

## Q4 — Messages

* **Refusals are clean.** Fixed words, the project-relative name through
  `ascii()`, and a remedy. The shipped test plants ESC and BEL in a name and
  checks the refusal; I saw the same through the CLI. Where a link points is
  not printed.
* **The divergence warning is not.** `install.py:653` prints `{dst}` (the
  absolute harness path) and `', '.join(quarantined)` (each `str(rel)`, a name
  from the project's own `.agents/skills/`). With X1, committed and cloned with
  git and run with links impossible, stderr carried
  `session-start/^[]0;RETITLED^G^[[2J.md`: 2 ESC bytes and 1 BEL, a title
  change and a screen clear. This is CF-SR-1.
* **Reach is narrow**, and the repair itself narrowed it: project data can no
  longer force copy mode, so the warning prints only where links truly fail.
  Windows forbids bytes 1–31 in file names, so there the reachable cases are
  C1 controls and bidirectional-override characters, which `ascii()` also
  escapes.
* **The `[skip]` lines** (`install.py:315` and the onboarding ones) print
  `target / <a destination Cairn chose>`. No project file name reaches them;
  only the target path the person typed. With a target folder named
  `proj<ESC>[31mRED`, a re-run put a raw ESC on 34 lines, on "Scaffolding Cairn
  into", "Target repository" and every `[skip]`. That is CLI-wide and not on
  this path (CF-SR-5).
* The other fan-out prints are fixed text or Cairn's own vendor paths.

## Q5 — AST

Derived as the runbook says (`bootstrap/AST_BASELINE_RUNBOOK.md`, step 1), on
the parent and on the commit, against the committed baseline:

| tree | CHANGED | MISSING | DUPLICATE | NEW |
|---|---|---|---|---|
| parent `2e1c9b3b` | 5 (`_cmd_adopt_module`, `cmd_upgrade`, `create_dev_tree`, `main`, `seed_gitignore`) | 0 | 0 | 86 |
| `cf707e2a` | 7: the same five plus `_emit_skill_copy_fallback` and `_symlinks_available` | 0 | 0 | 86 |

Comparing every one of the 259 top-level symbols across all
`bootstrap/_scaffold/*.py`, parent against commit, exactly two digests moved:
`_emit_skill_copy_fallback` `28134f3136c51838` → `29ef25b1a8aba93d` and
`_symlinks_available` `eee811ebda2020c8` → `28f5d712e82d2dd7`, matching the
commit body. The five earlier CHANGED symbols keep their digests. No symbol
appeared or left. `_ast_attest.py verify --known-new` reports only those 7
CHANGED and no rekeyed known-new symbol. The commit touches no fixture under
`bootstrap/tests/fixtures/`. `test_ast_attest.py`: 2 failed (the two the
commit names), 28 passed.

## Findings

### CF-SR-1 — low: the copy-divergence warning prints project file names raw

**Plain:** when a generated copy had been edited, the installer moves it aside
and says so. That message lists the files by name, straight from the project,
so a file name with terminal control codes in it can retitle the window or
clear the screen.

* `bootstrap/_scaffold/install.py:653`: `{dst}` (absolute) and each `str(rel)`
  of the quarantined files, unescaped.
* **Measured**, committed and cloned with git, links impossible: 2 ESC and 1
  BEL on stderr. The same on the old engine.
* Reach: only where links truly fail (the repair removed the forcing). It is
  not a containment break.

**Recommended fix** (cheap, on-path, same function): print
`', '.join(shown(dst / r) for r in quarantined)` and `shown(dst)` instead of
the raw names, using the `shown()` the commit added. That is project-relative,
`ascii()`-escaped, and matches the refusal text. Pin it with the X1 shape in
copy mode, as `test_a_refusal_puts_no_raw_control_bytes_on_the_terminal`
already does for refusals.

### CF-SR-2 — low: `O_EXCL` is load-bearing; the "equivalent pair" was measured with a probe that could not tell them apart

**Plain:** the copy is written to a new temporary file that must not already
exist. One flag (`O_EXCL`) enforces "must not exist". The other (`O_NOFOLLOW`)
only refuses a symbolic link. The commit reports that dropping either one alone
is harmless. Dropping `O_NOFOLLOW` is. Dropping `O_EXCL` is not, and no
shipped test would notice.

* Measured (Q3): without `O_EXCL`, a hard link at the temporary name made the
  installer overwrite an outside file and leave the copy name hard-linked to
  it. A longer plain file there left non-canonical bytes in the copy. The
  shipped tests: 52 passed.
* On Windows `O_NOFOLLOW` does not exist, so `O_EXCL` is the whole defence.
* Reaching it needs the random 64-bit temporary name guessed, or a program
  racing on the machine, so the exposure is low. The code is correct.

**Recommended fix:** add a test that plants a **hard link** (and a longer
plain file) at the guessed temporary name, beside
`test_a_link_at_the_temporary_name_is_not_written_through`
(`bootstrap/tests/test_engine_copy_fallback_contained.py:492`). It kills the
`O_EXCL` mutant. Record the ledger as: `O_NOFOLLOW` alone equivalent (measured);
`O_EXCL` alone a survivor, now killed by that test.

### CF-SR-3 — informational: the temporary-name swap installs a link at the copy name

**Plain:** a program racing on the machine can replace the just-written
temporary file with a link. The rename then puts that link at the copy's name.
Nothing is written outside, and the next install refuses the link loudly. But
until then the harness reads through it.

* Measured (R2): 5 of 3,000 runs, 0 writes outside.
* The docstring and the `SECURITY_MUTATIONS.md` row name only the parent-folder
  swap as the remaining gap. The kernel review recorded the same pattern
  (SW-SR-3: a second gap of the same kind, not named).

**Recommended (optional):** name it beside the parent-folder window in the
docstring and the inventory row. To narrow it, compare `os.fstat(fd)` with
`os.lstat(out)` after the rename and refuse on a mismatch. Under the stated
threat model, naming it is enough.

### CF-SR-4 — informational: on the upgrade route, "then re-run" does not redo the fan-out

**Plain:** after an upgrade, the refusal tells the person to remove the link
"then re-run". Re-running the upgrade does nothing for the skills, because
they are already recorded. The harness simply has no copies until something
else fans out.

* Measured: after removing the planted links, `upgrade --stage` and `--apply`
  (exit 0, "Applied 0 file(s)") left `.claude/skills/` without the copies.
* It fails safe. The session kernel's self-heal at `session-start`, or a
  re-install, does the fan-out.

**Recommended (optional):** in `_apply_upgrade`'s warning
(`upgrade.py:2233`), say what to re-run: `session-start`, or the installer.

### CF-SR-5 — informational, not on this path: the absolute target path reaches the terminal raw

The `[skip]` lines (`install.py:315` and the onboarding ones), "Scaffolding
Cairn into", "Target repository" and others print the absolute target path
unescaped. A target folder whose name carries ESC put it on 34 lines of a
re-run. The project cannot choose those names. Only the person typing the
target can, for example a folder unpacked from an archive. The engine has no
single terminal encoder. The kernel's `encode_display` is the model, if the
CLI ever takes one. No change is owed by this repair.

## What I did not cover

* **Windows.** Not available. `O_EXCL` as `CREATE_NEW` against a reparse
  point, `os.replace` over a link, NTFS junctions (which `is_symlink()` does
  not report; check (3)'s `resolve()` is the backstop there), and the real
  no-links behaviour were argued, not run. The "links impossible" runs are a
  stand-in that fails `os.symlink`. I also did not check whether `CREATE_NEW`
  follows a dangling symbolic link on Windows. If it does, Windows has no
  last-name defence against a link at the temporary name. That needs a guessed
  name or a racing program, and creating links there needs Developer Mode,
  which would select link mode anyway.
* **Linux and case-sensitive filesystems.** Everything ran on case-insensitive
  APFS.
* **A real no-symlink filesystem** (exFAT, some network mounts). Those also
  forbid control bytes in names, which limits CF-SR-1 there.
* **The session kernel's twin** (`_heal_skill_copy` in `tools/session.py`),
  reviewed in `598aa6be` and unchanged here.
* **The full suite and the commit's own mutation ledger.** Not rerun. I ran the
  four owning files (52 passed) and the AST test, measured the open-flag mutants
  myself, and left ordinary falsification to the code review.
* **Reads.** The copy path still reads through links inside `.agents/skills/`
  (SW-SR-8, informational, unchanged).

## Verification of the answer -- Claude Opus 5.5 -- 2026-10-19

**Reads**: `80c54552` ("Answer the engine copy-fallback reviews"), against its
parent `6c436a9f`. A detached worktree of `80c54552` in a fresh, uniquely named
scratchpad folder; `git archive` copies of `80c54552` for the mutants and one of
the parent for controls; all removed when done. Python 3.13.13. Scoped runs
only, no full suite (doctrine `12be58d9`).

**Verdict**: **CF-SR-1 to CF-SR-4 are closed.** CF-SR-5 needed no change and
none was made. The new `format_forked_facade_warning` encoding is complete for
every lockfile field it prints and idempotent. A crafted lockfile can no longer
forge a line through `upgrade --plan` (10 fields probed). One new
informational finding (CF-SR-6), not blocking.

**Scoped tests at `80c54552`**: `test_engine_copy_fallback_contained.py` 42
passed, `test_fork_advisory.py` 37, `test_lockfile_module.py` 7,
`test_lockfile_provenance.py` 13, `test_module_merge_lockfile.py` 13,
`test_upgrade_lockfile_path_containment.py` 71: **183 passed, 0 failed**.

### The four findings

| finding | evidence at `80c54552` | status |
|---|---|---|
| CF-SR-1 divergence warning raw | Through the CLI, links impossible, a canonical file and a differing copy both named `ESC]0;RETITLED BEL ESC[2J.md`: exit 0, **0 ESC and 0 BEL on stderr**. The line reads `copy-fallback divergence under .claude/skills: session-start/\x1b]0;RETITLED\x07\x1b[2J.md`. It is project-relative and escaped. Mutants: names back to `str(rel)`, killed; folder back to absolute `{dst}`, killed (both by `test_the_divergence_warning_names_files_escaped_and_relative_to_the_project`). | **closed** |
| CF-SR-2 `O_EXCL` load-bearing | Mutants on the two owning files (79 tests; control 79 passed): **no `O_EXCL`: killed** (2 failed, `test_anything_at_the_temporary_name_is_refused_not_written_into[hard-link]` and `[regular-file]`); no `O_NOFOLLOW`: 79 passed, the equivalent one, as the answer now records; neither: killed (3 failed). | **closed** |
| CF-SR-3 second window unnamed | The docstring and the `SECURITY_MUTATIONS.md` row now name both windows: the temporary file swapped for a link lands that link at the copy name, nothing is written outside, and the next install refuses it. Matches R2. | **closed** |
| CF-SR-4 "then re-run" | The upgrade route now prints "...then run `python tools/session.py session-start` (or install again) to copy the skills." I followed it: a pre-skills tree, `upgrade --stage` / `--apply` with links impossible over a dangling link at `.claude/skills/session-start/SKILL.md` (exit 0, nothing outside, the warning above). Then I removed the link and ran `session-start`, links impossible: exit 0, and the three copies appeared. | **closed** |

A note on my own earlier upgrade probe, not a finding. It removed only the
three skill records from the lockfile, as `test_skills_upgrade.py`'s helper
does, so `.agents/skills/_data/vendor_targets.yml` was never restored. Without
that table, `session-start` reports "no symlink-tier harness in use" and copies
nothing. The remedy check above removes every skills record, as a real
pre-skills tree would have none. My Q1 results stand: that probe still reached
the fan-out.

### The forked-facade advisory encoding (`bootstrap/_scaffold/lockfile.py`)

**Every field it prints**, traced to its source in `forked_facade_findings`:

| field | source | printed as |
|---|---|---|
| `dst` | the lockfile record | `!r`: escaped |
| `engine` | derived from `dst` (`<dir>/_<stem>`) | `!r`: escaped |
| `reason` | fixed text, plus `_guarded_read`'s reason (a record path, a guard or `OSError` message) | `plain()`: encoded (new) |
| `skew` | the lockfile's `cairn_version` and the checkout's version | `plain()`: encoded (new) |
| `upstream` ("Compared against …") | the resolved `--cairn-root` templates path and `_cairn_version` of that checkout's `CITATION.cff` | raw. It is not lockfile text, so the lockfile cannot reach it. `--to` sets it to none. |
| `src_relabelled` | a boolean; the text is fixed | fixed |

So the encoding is complete for lockfile text.

**Idempotent, as claimed.** `plain()` returns printable ASCII unchanged and
anything else through `ascii()`, whose output is printable ASCII, so a second
pass changes nothing. I fuzzed 20,000 random pairs (`skew`, `reason`) over an
alphabet of line breaks, CR, tab, ESC, BEL, DEL, NEL, U+2028, U+202E, C1 CSI,
backslashes and quotes:

* the engine's output is identical when its fields are pre-encoded (0 differ);
* `verify_integrity._plain`'s escape passes through unaltered (0 altered), so it
  is not doubled;
* no control byte and no extra line reached the text on either route (0).

The same fuzz on the parent engine leaks in 27,824 checks, which confirms the
instrument.

**Can a crafted lockfile forge a line through `upgrade --plan`?** No. Each case
installs, adds a forked facade so the advisory fires, then writes
`\nFORGED: OK -- run …\x1b[2J` into one lockfile field and runs the real
`upgrade --plan`. The parent engine was the control.

| field crafted | parent `6c436a9f` | `80c54552` |
|---|---|---|
| `cairn_version` | **1 forged line, 1 raw ESC** | 0, 0 |
| `cairn_commit`, `cairn_source`, `profile.preset`, `tokens.project_name`, an unknown key | 0, 0 | 0, 0 |
| facade `src`, another record's `dst`, a `base_cache` | refused, exit 2, name escaped | refused, exit 2, name escaped |
| a facade `dst` carrying the text, with its engine folder present so the advisory names it | 0, 0 (`!r`), then refused, exit 2 | 0, 0, then refused, exit 2 |

Neither `stdout` nor `stderr` held a line starting with the forged text, and
`verify_integrity` over the crafted-dst tree printed none either.

### New finding

**CF-SR-6 — informational: the two encoders differ on a backslash.**
`verify_integrity._plain` sends any text with a backslash through `ascii()`, so
a real line break (`\n`) and the two typed characters `\n` print differently.
The engine's `plain()` leaves printable ASCII alone, backslashes included. That
is what makes it idempotent over `verify_integrity`'s output. But on the
`upgrade` route a `cairn_version` holding the typed characters `\n` prints the
same as one holding a real line break (measured: identical text). No line is
forged and no control byte reaches the terminal; a reader just cannot tell the
two apart in the upgrade advisory. **Optional:** if that distinction matters
here too, let the engine apply `_plain`'s backslash rule, and have
`verify_integrity` pass the finding's `skew` and `reason` raw so they are
encoded once.

### What I did not cover

* Windows, Linux, and the full suite, as before. Boundary B for `80c54552` is
  the implementer's, reported to the coordinator.
* The answers to the code review's findings (CF-CR1 to CF-CR7). I checked only
  where they overlap mine; the `UPGRADE.md` wording and the reworked
  `needs_links` test markers I did not review.
* The AST change set, briefly: across all 263 engine symbols, parent against
  `80c54552`, exactly `_emit_skill_copy_fallback` (`29ef25b1a8aba93d` →
  `fa4da6192cf48ae2`) and `format_forked_facade_warning` (`a508f3c7ba8d7232` →
  `297f1daa42a82205`) moved, as the commit says. CHANGED goes from 10 to 11, and
  no fixture is touched. The re-anchor stays the Maintainer's.
