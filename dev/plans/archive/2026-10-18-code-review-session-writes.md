# Code review (Internal) — the session kernel's writes (`7e6a14e5`) — Claude Sonnet 5.5 — 2026-10-18

**Obligation**: code review (falsification) of a defect repair that has no plan,
the repair of GS-SR-1 in `dev/plans/archive/2026-10-18-security-review-gitignore-seed-guard.md`
and GS-CR1 in `dev/plans/archive/2026-10-18-code-review-gitignore-seed-guard.md`.
Fresh session, not the implementing session. The implementer is the same agent
type, so the distance here is a fresh context, not a different type. This is an
Internal pass; I do not claim External standing. A separate Security Review of the
same commit ran in parallel and is not read or relied on here.
**Reviewed commit**: `7e6a14e5` ("Session kernel: no write goes through a link or
leaves the project"), parent `c14ec9c5`. It changes four files: `tools/session.py`,
its byte-identical twin `templates/skills/_lib/session.py`, the new
`bootstrap/tests/test_session_writes_contained.py` (86 tests), and one hash line in
`dev/.cairn/cairn-lock.yml`. The repository's HEAD moved while I worked (now
`3c50940d`); I checked that the two kernel files and the new test file are
byte-identical at HEAD to `7e6a14e5`, so every line number below holds at both.
**Interpreter**: Python 3.13.13 at `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
`PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider`. Platform: darwin. Every write,
mutation, probe and test ran in a detached `git worktree` of `7e6a14e5` (or of its
parent, or of the base `20f145ed`), each in a fresh folder under a uniquely named
scratch directory, removed afterwards. The shared checkout was only read. Every
process I started has exited; I killed none.

**Verdict**: NO BLOCKING FINDINGS — 0 blocking, 8 non-blocking.

**In plain terms.** The repair does what it says. A checkout that is only data (a
link, a folder, a row in the vendor table) can no longer make `session-start`,
`session-end` or the handoff lock write through a link or outside the project. I
checked this three ways. First, I listed every place the kernel writes from the
code itself (not from the commit's table) and broke each guard, one at a time and
in layers, in copies of the commit with both twin files edited the same way: 67
deliberate breaks, and the tests catch 56. Second, I built hostile clones from
committed data only and ran the real command in each. The unmutated code leaves
every outside file alone in all 14 cases, and 14 of the breaks that the tests catch
also leak in the real command, so the guards they remove are doing real work. Third, I ran the 86 new tests against the
parent commit: 82 fail there, 4 pass as the commit says. For a normal adopter the
repair changes almost nothing: on a fresh `solo-greenfield` install, `session-start`
(link mode and simulated copy mode), `session-end`, `session-end --handoff` with
and without the marker, and a second run all print the same text as the parent.
The differences I found are improvements (a Windows-style `.gitignore` keeps its
line endings; a non-UTF-8 one is refused softly instead of crashing) and one
behaviour change I would not have chosen (a read-only `.gitignore` is now replaced,
SW-CR4).

The recorded test figure reproduces exactly: 3590 passed, 2 failed (the two AST
tests that already fail on the parent). On the commit's own bytes I get 3618
passed, 2 failed.

What is left is not in the defect the commit set out to close. The biggest item
(SW-CR1) is a rule the commit adds but makes too narrow: a vendor-table row can
still point the fan-out at the user's own untracked folder or link, for example a
virtual environment's `python` link, and replace it. The parent does exactly the
same, so it is not a regression, and a one-line rule closes it (tested). The other
seven are a second pruner that shares the defect, adopter-facing behaviour and
wording, and gaps in what the tests pin (11 of my 67 breaks pass every owning test).

## What I verified

| # | Check | Result |
|---|---|---|
| 1 | **Twins and lockfile** | `tools/session.py` and `templates/skills/_lib/session.py` are byte-identical at `7e6a14e5` and at HEAD (`cmp`). Both hash to `4f08c74e…0379`. The one lockfile line the commit changes (the `hash` of the `tools/session.py` entry in `dev/.cairn/cairn-lock.yml`) equals that sha256 exactly, at the commit and in the committed lockfile at HEAD; `base_hash` is unchanged, as in earlier commits of this file. No other file in the tree pins the old hash (searched). |
| 2 | **Boundary B record, reproduced** | A detached worktree of `20f145ed` with exactly the commit's four files copied over it: `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` gave **3590 passed, 2 failed** in 611 s (the body says 601 s), Python 3.13.13. The two failures are `test_ast_attest.py::test_ast_gate_passes_over_the_full_scaffold_module_set` and `test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package`. No skip, xfail or xpass was reported (`-rfEsxX`). |
| 3 | **The same run on the commit's own bytes** | The record was measured on `20f145ed` plus four files, not on `7e6a14e5`, which sits on 21 later commits (it says so: "fresh detached worktree of 20f145ed holding only these four files"). So I also ran the pair on a clean worktree of `7e6a14e5`: **3618 passed, 2 failed** (the same two), 613 s, tree clean before and after. The 28 extra passes are tests added by the intervening commits. `scripts/quality_gate.py --sub neutrality --sub redundancy` exits 0: neutrality fail=0, redundancy fail=0. The two AST failures also fail on the parent (`2 failed, 28 passed` for that file), as the body says, so they are not this commit's. |
| 4 | **The new tests can fail** | I copied the new test file onto a worktree of the parent `c14ec9c5` and ran all 86: **82 failed, 4 passed**, matching the body. The four that pass on the parent are pins, not repairs: the permission-bit test, the link-in-the-middle-of-a-copy-path test, the link-to-a-folder-inside-the-project test and the inventory test. The failures are 32 "did not raise", 27 "fan-out returned a row where `[]` was expected", and the rest a missing helper or a changed write. |
| 5 | **Trust-root code is untouched** | By AST comparison against the parent: `_resolve_interpreter`, `_probe_interpreter`, `_has_symlink_component`, `encode_display`, `_resolve_agent` and `_resolve_session` are identical. The changed functions are `_skill_symlinks_available`, `_assert_fanout_contained`, `_seed_skill_gitignore`, `_heal_skill_copy`, `_heal_skills_fanout`, `HandoffLock` (`__init__`, `acquire`, `heartbeat`), `_prune_reflections` and `_do_reflection`; five functions are new. `import stat` shadows nothing. |
| 6 | **The set of writes, from the tree** | Table below. It matches the module docstring's list and the commit's "six guard call sites". |
| 7 | **Falsification ledger** | 67 breaks plus a control; table below. |
| 8 | **Hostile clones through the real entry** | 14 scenarios, table below. |
| 9 | **Normal-adopter regression** | Fresh `solo-greenfield` install with the parent's kernel and with this commit's kernel; outputs compared. Section below. |
| 10 | **Durable-artifact hygiene** | No finding id, chunk letter or review coordinate in the new docstrings, comments or test names (searched both files). Test names say the property they pin. |
| 11 | **The end-to-end clone test** | `test_session_start_in_a_hostile_clone_writes_through_no_link` stays green under every one of my 66 narrower breaks, because on this platform the probe fix keeps it in link mode and the `.gitignore` is never reached. It is a whole-chain tripwire, and it is one: with the probe name, the guard, the read and the write all reverted together (ALLGI) it fails along with 14 other tests. The individual layers are pinned by the unit tests. That is a fair design; I note it so nobody reads that test as the proof of the guard. |

### The writes the kernel makes, listed from the tree

I listed every write-capable call in `tools/session.py` with an AST walk (`os.open`,
`os.write`, `os.ftruncate`, `os.replace`, `os.symlink`, `os.chmod`, `unlink`,
`mkdir`, `write_*`, `subprocess`) and grouped them by what stands in front of
them. The "breaks" column names the ledger rows that remove or weaken that
protection.

| Write | Where | What stands in front of it | Breaks |
|---|---|---|---|
| Symlink probe: create then remove a link in the project root | `_skill_symlinks_available`, `tools/session.py:843` | a fresh random name each call | H10 |
| Fan-out link: replace or create `.claude/skills` as a link | `_heal_skill_symlink`, `:972` | `_assert_fanout_contained` (`:898`, unchanged) and the vendor-path rule | F1, F2, V8 |
| `.gitignore` seed | `_seed_skill_gitignore`, `:929` | entry rule; `_assert_not_linked` (`:953`); a read that refuses links; a write by temp file and rename | G1, G1m, H1, H7, V9, GH1, G1H7, G1H1H7, ALLGI |
| Copy-mode files and quarantine | `_heal_skill_copy`, `:996` | `_assert_not_linked` on each destination (`:1015`) and each quarantine name (`:1027`); a "not a plain file" refusal; the check-everything-first plan; `os.replace` | G2, G3, H12 to H16, GH3, GH3b |
| Handoff lock: create, reclaim, release | `HandoffLock.acquire` `:1249` (guard `:1251`), `_reclaim_or_refuse`, `release` | the guard, then `O_EXCL`; reclaim and release only remove the name | G4, G4m |
| Lock heartbeat | `HandoffLock.heartbeat`, `:1301` | writes the descriptor opened with `O_EXCL` | H9, H9b, H9c |
| Reflection prune: delete dated files | `_prune_reflections`, `:1330` (guard `:1340`) | the guard (also on the dry run) | G5, G5m, G5x6x |
| Reflection scaffold: make the folder, create the file | `_do_reflection`, `:1496` (guard `:1505`) | the guard, then `O_EXCL` | G6, G6m, H6, H6b |
| Child processes: `intent.py prune`, `intent.py list`, `evolution_infer.py`, `git` | `_prune_intents`, `_surface_intents`, `_run_evolution_infer`, `_git` | nothing in `session.py`; they are the project's own tools | not covered (see the last section) |

Eight of the nine rows have a protection I broke. No write the kernel makes itself sits
outside the table.

### Hostile clones, through the real command

Each scenario commits only data (links, folders, vendor rows) to a repository,
clones it, and runs `python tools/session.py …` in the clone. "Copy mode" is
simulated by making only the kernel's own probe link fail, which is what a machine
without link rights does. A leak is any change under the outside folder, to
`.git/config`, or to `.git/hooks`.

| # | Scenario | Unmutated result |
|---|---|---|
| C1 | `.gitignore` is a link to a file outside the clone (copy mode) | refused, nothing written |
| C2 | `.gitignore` is a link to `.git/config`, plus a vendor row whose folder name carries a config stanza (copy mode) | refused, `.git/config` unchanged |
| C3 | `.claude/skills` is a link to an outside folder (copy mode) | refused |
| C4 | `.claude/skills/session-start` is a link to an outside folder (copy mode) | refused |
| C5 | the quarantine name is a link to an outside folder, with a divergent file beside it (copy mode) | refused |
| C6 | a dangling link where the second copy would go (copy mode) | refused before any file is copied |
| C7 | `dev/reflections` is a link to an outside folder, `session-end` | exit 1, refused, nothing created outside |
| C8 | the same, `session-end --handoff` with the marker | exit 1, the old outside diary entry is intact |
| C9 | `dev/.cairn` is a link to an outside folder, `session-end --handoff`, with the process killed before release | exit 1, no lock file outside |
| C10 | `.claude` is a link to an outside folder (link mode) | refused by the older fan-out check |
| C11 | vendor row `.git/hooks` (copy mode) | skipped as unsafe, hooks folder unchanged |
| C12 | vendor row `dev/.cairn` (copy mode) | skipped as unsafe |
| C13 | vendor row `.git/hooks/pre-commit` (link mode) | skipped as unsafe |
| C14 | `.gitignore` is a link outside, link mode | not touched (nothing to seed) |

All 14 are clean on `7e6a14e5`. In the ledger below, the "real-entry leak" column
names which of these a break turns into a leak.

### Normal adopters: parent kernel against this commit's kernel

I installed `solo-greenfield` twice with the real installer (once from the parent's
tree, once from `7e6a14e5`), added a `.claude/` folder (a Claude Code user has one;
without it the fan-out correctly does nothing), committed, and ran the same sequence
with each kernel: `session-start` twice, `session-end` twice, `session-end
--handoff --dry-run`, `--handoff` without the marker, `--handoff` with it, then
`session-start` in simulated copy mode twice, once with a diverged copy, and then
copy mode over ten `.gitignore` shapes at two permission settings. I compared exit
codes, stdout, stderr, `git status` and the resulting bytes. The installed kernel
equals the template byte for byte in both. The heartbeat leaves a valid lock file
(139 bytes before and after two refreshes, valid JSON each time), the lock is gone
after the handoff, and no `.cairn-write-*` or probe file is left behind.

**Identical** in every flow except the four differences below. In particular:
`session-end --handoff` on a normal tree prints the same manifest and the same
steps; the heartbeat through a descriptor changes no output.

| Difference | Parent | This commit | Judgment |
|---|---|---|---|
| `.gitignore` with Windows line endings | whole file rewritten with LF | bytes and CRLF kept; appended lines use CRLF | an improvement |
| `.gitignore` that is not UTF-8 | traceback, exit 1 | soft refusal ("not a readable regular UTF-8 text file"), exit 0 | an improvement |
| `.gitignore` whose last byte is a lone carriage return | CR rewritten to LF | entry appended directly after the CR | see "seen, not raised" |
| `.gitignore` is read-only (mode 0444) | `PermissionError` traceback, file untouched | file replaced, mode 0444 kept, entry added | SW-CR4 |

The new vendor-name rule changes nothing for the shipped table: its only
link-tier row is `.claude/skills`, which passes. A custom row with a space or a
character outside letters, digits, dot, dash and underscore is now skipped with a
warning where the parent used it.

## Falsification ledger

Method. For each row, a fresh detached worktree of `7e6a14e5`; the same text edit
applied to **both** twins (editing only one trips the twin-comparison test and
hides the result); then (a) the six test files that read or import the kernel
(190 tests: `test_session_kernel`, `test_session_routines`, `test_session_failsafe`,
`test_session_writes_contained`, `test_skills_self_heal`, `test_skills_security`)
and (b) the 14 hostile-clone scenarios above. "Owning tests" is the number that
fail. "Real-entry leak" is which scenarios changed something they must not.
A break is **killed** if some owning test fails. It is **survived** if none does.
I call a survivor **equivalent** only after measuring that it changes no behaviour,
and I measured none to be: every survivor below has a measured difference or an
unmeasured case, so all eleven are reported as survivors.

Unmutated control: 190 passed, 0 failed; all 14 scenarios clean.
Totals: 67 breaks, **56 killed, 11 survived**. 14 breaks leak in the real command
(G2, G4, G4m, G6, G6m, G5x6x, V3, V8, V89, V389, F1, GH3b, G1H1H7, ALLGI). The
proposed fix (FIXLAST) is not a break.

| Id | Break | Owning tests | Real-entry leak | Verdict |
|---|---|---|---|---|
| CONTROL | unmutated | 0 failed | none | control |
| G1 | delete the guard in _seed_skill_gitignore | 7 failed | none | killed |
| G2 | delete the guard on each copy destination | 4 failed | C3,C4 | killed |
| G3 | delete the guard on each quarantine name | 1 failed | none | killed |
| G4 | delete the guard in HandoffLock.acquire | 1 failed | C9 | killed |
| G5 | delete the guard in _prune_reflections | 2 failed | none | killed |
| G6 | delete the guard in _do_reflection | 1 failed | C7,C8 | killed |
| G1m | gitignore guard moved below the write | 7 failed | none | killed |
| G4m | lock guard moved below the first write | 1 failed | C9 | killed |
| G5m | prune guard moved below the deletions | 1 failed | none | killed |
| G6m | reflection guard moved below the write | 1 failed | C7,C8 | killed |
| G5x6x | delete both the prune guard and the reflection guard | 3 failed | C7,C8 | killed |
| A1 | guard ignores a link on the way (folder loop) | 1 failed | none | killed |
| A2 | guard ignores a link at the destination | 11 failed | none | killed |
| A3 | guard skips the stays-inside-the-project check | 1 failed | none | killed |
| A4 | guard lets a destination outside root through | 1 failed | none | killed |
| H1 | _write_replacing opens dst itself | 5 failed | none | killed |
| H2 | _write_replacing temp file without O_EXCL | 1 failed | none | killed |
| H3 | _write_replacing fixed temp name | 0 failed | none | SURVIVED |
| H4 | _write_replacing drops the kept permission bits | 1 failed | none | killed |
| H5 | _write_replacing leaves its temp file on failure | 1 failed | none | killed |
| H6 | _create_text_exclusive without O_EXCL (O_NOFOLLOW stays) | 1 failed | none | killed |
| H6b | _create_text_exclusive in its unsafe form (no O_EXCL, no O_NOFOLLOW) | 1 failed | none | killed |
| H7 | _read_regular_bytes follows a link | 1 failed | none | killed |
| H8 | _read_regular_bytes accepts a non-regular file | 0 failed | none | SURVIVED |
| H9 | heartbeat writes through the path | 1 failed | none | killed |
| H9b | heartbeat does not rewind | 0 failed | none | SURVIVED |
| H9c | heartbeat does not truncate | 0 failed | none | SURVIVED |
| H10 | symlink probe has a fixed name again | 1 failed | none | killed |
| H11 | copy before the gitignore seed | 7 failed | none | killed |
| H12 | quarantine by shutil.move | 1 failed | none | killed |
| H13 | copy writes by out.write_bytes | 1 failed | none | killed |
| H14 | copy checks and writes file by file | 2 failed | none | killed |
| H15 | no refusal when the quarantine name is a folder | 1 failed | none | killed |
| H16 | no refusal when a copy destination is a folder | 1 failed | none | killed |
| V1 | vendor path may be one name | 5 failed | none | killed |
| V2 | vendor path names are not restricted to the safe set | 28 failed | none | killed |
| V2c | vendor name matched by prefix, not whole | 16 failed | none | killed |
| V3 | .git allowed in a vendor path | 4 failed | C11,C13 | killed |
| V4 | dev/.cairn allowed in a vendor path | 3 failed | none | killed |
| V5 | .git compared case-sensitively | 2 failed | none | killed |
| V6 | .git compared with its trailing dots | 1 failed | none | killed |
| V7 | .git refused only as the first name | 3 failed | none | killed |
| V8 | fan-out does not check the vendor path | 29 failed | C13 | killed |
| V9 | gitignore writer does not check the entry | 20 failed | none | killed |
| V89 | neither the fan-out nor the writer checks the vendor path | 49 failed | C11,C13 | killed |
| V389 | no vendor path check anywhere (.git allowed, fan-out and writer unchecked) | 49 failed | C11,C13 | killed |
| S1 | seed always appends LF | 1 failed | none | killed |
| S2 | seed adds no line break after a lone CR check | 0 failed | none | SURVIVED |
| S3 | seed never sees the entry as present | 2 failed | none | killed |
| F1 | fan-out containment check removed from _heal_skills_fanout | 1 failed | C10 | killed |
| F2 | fan-out containment ignores a symlinked parent | 2 failed | none | killed |
| E1 | guard message shows the relative name raw | 1 failed | none | killed |
| E2 | guard 'outside' message raw | 0 failed | none | SURVIVED |
| E3 | fan-out 'symlinked parent' message raw | 1 failed | none | killed |
| E4 | fan-out 'outside the repo' message raw | 1 failed | none | killed |
| E5 | 'not a plain file' (copy destination) raw | 0 failed | none | SURVIVED |
| E6 | 'not a plain file' (quarantine name) raw | 0 failed | none | SURVIVED |
| E7 | divergence warning shows the folder raw | 0 failed | none | SURVIVED |
| E8 | divergence warning shows the file names raw | 1 failed | none | killed |
| E9 | unsafe-vendor-path warning raw | 0 failed | none | SURVIVED |
| E10 | unsafe-entry refusal raw | 0 failed | none | SURVIVED |
| GH1 | gitignore guard deleted AND the write goes through the path | 12 failed | none | killed |
| GH3 | quarantine guard deleted AND quarantine by shutil.move | 2 failed | none | killed |
| GH3b | quarantine guard deleted, 'not a plain file' check deleted, quarantine by shutil.move | 3 failed | C5 | killed |
| G1H7 | gitignore guard deleted AND the read follows a link | 7 failed | none | killed |
| G1H1H7 | gitignore guard deleted, read follows a link, write through the path | 12 failed | C1,C2 | killed |
| ALLGI | the whole pre-repair chain: probe fixed name, no guard, read follows a link, write through the path | 15 failed | C1,C2 | killed |
| FIXLAST | PROPOSED FIX (not a mutant): a vendor path must end in the name 'skills' | 0 failed | none | proposed fix (not a mutant) |

Reading it:

* **The guard call sites** (G1 to G6, and each moved below its write) are all
  killed by a test written for them. G2, G4 and G6 (and their moved forms, G4m and
  G6m) leak in the real command, so those guards are load-bearing. G1, G3 and G5
  do not leak when broken alone, and that is because a second layer catches the
  same input: the `.gitignore` read refuses a link; the "not a plain file" check
  sits in front of the rename; and `_do_reflection`'s guard stands in front of the
  prune. I did not argue that, I broke the second layer too. GH1, G1H7 and G1H1H7
  show the `.gitignore` chain has three layers and the last of them leaks only when
  all three are gone. GH3 and GH3b do the same for the quarantine (three layers,
  leak at C5). G5x6x shows the prune deletes the outside diary entry once both
  reflection guards are gone. Each layer on its own is killed by an owning test.
* **The older check for link mode** (`_assert_fanout_contained`, F1 and F2) is
  load-bearing: without it C10 writes a link into the outside folder. The commit
  leaves `_heal_skill_symlink` unchanged on the grounds that this check covers it;
  I confirm that for links through a parent. It does not cover what the vendor row
  chooses to name (SW-CR1).
* **The vendor-path rules** (V1 to V9) are all killed, and removing either the
  `.git` rule (V3) or the fan-out's check (V8) leaks into `.git/hooks`.
* **The eleven survivors** are measured next.

### The eleven survivors, measured

Each was run against an unmutated control. All of them are in the "unpinned" class:
the code is right today and a test would not notice if it changed.

| Id | What I measured | Consequence |
|---|---|---|
| H3 (fixed temp name) | With the temp name fixed, a file committed at that name makes the copy-mode fan-out end in `FileExistsError` (control: no error). | Availability only; random names are what prevents squatting. SW-CR7. |
| H8 (no regular-file check) | `.gitignore` as a folder: refused identically with and without the check. `.gitignore` as a named pipe: **hangs for the control too** (the open blocks before the check can run). | The check is unreachable for anything git can carry. SW-CR8. |
| H9b (heartbeat does not rewind), H9c (does not truncate) | After two heartbeats the control file is valid JSON. Without rewinding: 447 bytes, 313 of them NUL, invalid JSON. Without truncating: trailing bytes after the JSON, invalid. | A lock file the next handoff cannot read: it sees an unknown holder and refuses. Fails closed. SW-CR6. |
| S2 (lone CR) | `b'*.log\r'` becomes `b'*.log\r.claude/skills/\n'` in the control, and git then does **not** ignore `.claude/skills/x`; with the break it becomes `b'*.log\r\n.claude/skills/\n'` and git does. | Only for classic-Mac line endings. Listed under "seen, not raised". |
| E2, E5, E6, E7, E9, E10 (message text printed raw) | With the break, the message carries a raw escape byte (`\x1b`) in each case; the control carries none. | The "no raw control bytes in refusal text" property is pinned at 4 of 10 sites. SW-CR5. |

## Findings

### [SW-CR1] non-blocking (medium) — the vendor-path rule is a two-name list, so a vendor row can still replace or fill the user's own links and folders

**What.** `_vendor_path_parts` (`tools/session.py:870`) accepts any relative path of
two or more names made of letters, digits, dot, dash and underscore, except one that
passes through `.git` or `dev/.cairn`. The commit's reason for the exclusions is
that copy mode "puts every canonical file under the row's folder", so a row must not
name "places the project's own files must not fill". The same reason covers every
other untracked place that holds things the user runs, and the rule does not.

**Evidence** (scratch repositories; the table is read from the checkout, so a row
is data a clone can carry; **the parent kernel gives the same result in all three**,
so none of this is new):

1. **Link mode, every platform.** A clone whose vendor table has a link-tier row
   with path `.venv/bin/python`, in a project where the user has made a virtual
   environment (so `.venv/bin/python` is a link to the interpreter). `session-start`
   removes that link and puts a link to the skills folder in its place. Before:
   `.venv/bin/python` -> the Python 3.13 interpreter. After: `.venv/bin/python` ->
   `../../.agents/skills`, a folder, so the environment no longer runs. The same
   with a row `dev/reflections` replaces a user's link there. This is what
   `_heal_skill_symlink` (`:972`) does by design to any link the row names, and
   `_assert_fanout_contained` only checks where the link sits, not whether it is
   ours to replace.
2. **Copy mode** (a machine without link rights). A row `.venv/bin` and a file
   `python` in `.agents/skills/` of the clone: after `session-start`, the user's
   `.venv/bin/python` holds the clone's bytes, the original is kept as
   `python.diverged.bak`, and `.gitignore` gains `.venv/bin/`. That is an
   attacker-chosen file in the folder the user's shell runs from.

Neither writes through a link or leaves the project, so neither breaks the commit's
stated rule, and neither is a regression. I raise it because the commit adds this
rule to close this class and stops two names short.

**Fix** (tested). Require the last name of the path to be `skills`, which is what a
harness read-path is: in `_vendor_path_parts`, `if len(parts) < 2 or parts[-1] !=
"skills": return None`. In a scratch copy: all 190 owning tests pass, all 14
hostile-clone scenarios stay clean, and the three results above flip to "link kept,
file kept, row skipped with the existing unsafe-path warning". A test beside the
existing path tests: rows `.venv/bin`, `.venv/bin/python` and `dev/reflections` are
skipped in both modes.

### [SW-CR2] non-blocking (low) — the same defect class remains in the second reflection pruner

`tools/prune_reflections.py` (shipped with the default-on reflections module, with a
byte-identical twin at `templates/modules/default-on/prune_reflections.py`) lists
`dev/reflections` with `directory.iterdir()` (`tools/prune_reflections.py:71`) and
skips links among the *files* (`:72`) but never checks the folder. I made
`dev/reflections` a link to an outside folder holding two dated files and ran
`python tools/prune_reflections.py --keep 1`: the older outside file was deleted and
the exit code was 0. Its deletion filter is strict (the pinned
`<date>-<HHMMSS>-<agent>-<role>.md` grammar), so the reach is narrow, and it only
runs when someone invokes it. It is outside what the commit set out to change, and
the commit body's "Reflection prune: guarded" is true of the kernel's own
`_prune_reflections`. But the commit title and the module header read as "no write
goes through a link", and anyone who takes that to cover the repository will be
wrong by this one.

**Fix.** The same refusal at the top of `prune_reflections()` (a link at the folder
or any parent, refuse), edited in both copies, with a test next to the kernel's
`test_pruning_never_deletes_through_a_linked_reflections_folder`. Or record it as the
next follow-up; the call is the Maintainer's.

### [SW-CR3] non-blocking (low) — adopter-facing changes are undocumented and one refusal does not say which part is the link

Nothing in the commit touches a document, and `bootstrap/UPGRADE.md` describes only
the installer's `.gitignore` and `dev/` refusals. Four behaviours are new for an
adopter and appear nowhere they would look:

1. `session-end` now ends with exit 1 and no reflection when `dev`,
   `dev/reflections` or the file's folder is a link (C7). A user who links
   `dev/reflections` to a shared folder across worktrees, which is plausible, loses
   the reflection scaffold until they undo it.
2. The handoff is refused when `dev` or `dev/.cairn` is a link (C9).
3. The message in both cases is `refusing to write through a link or outside the
   project: dev/reflections/2026-10-18-<agent>-<session>.md`. It names the file it
   was going to create, not the link, and it gives no remedy. The reader has to
   work out which folder is the link. (The installer's `.gitignore` refusal names
   the remedy, after the earlier review asked for it.)
4. In copy mode, a refusal while copying leaves the `.gitignore` entry already
   seeded (C3 shows a modified `.gitignore` after the refusal), because the seed
   now runs first. The body says a refusal "leaves nothing copied", which is true;
   the converse is not. And `session-start` prints "no symlink-tier harness in use
   here (nothing to fan out)" right after the refusal warning (`:1123` to `:1127`),
   which reads as though nothing was wrong.

**Fix.** One paragraph in `bootstrap/UPGRADE.md` beside the existing `.gitignore`
paragraph; make `_assert_not_linked` name the first link it finds ("`dev/reflections`
is a link; replace it with a real folder") instead of the destination; in
`cmd_session_start` skip the "nothing to fan out" line when a refusal was just
printed. The first two are wording only.

### [SW-CR4] non-blocking (low) — a read-only `.gitignore` is now replaced instead of respected

The write is a temp file and a rename in the project folder, and a rename needs
write permission on the folder, not on the file. So a `.gitignore` the owner made
read-only (mode 0444) is replaced, with the 0444 mode copied over. On the parent
this ended in a `PermissionError` traceback and the file stayed as it was. Measured:
parent exit 1, bytes `*.log\n`; this commit exit 0, bytes `*.log\n.claude/skills/\n`,
mode 0444. A read-only mark is an owner's way to say "not by a tool", and the
old failure honoured it, ungracefully.

**Fix.** In `_seed_skill_gitignore`, before writing, refuse (as `LifecycleError`,
fail soft) when the file exists and `os.access(path, os.W_OK)` is false, using the
same "not a writable regular file" family of message; one test with a 0444 file.

### [SW-CR5] non-blocking (low) — the "no raw control bytes in a refusal" property is pinned at 4 of 10 message sites

The body says each message's encoding was checked. I removed `encode_display` at
each of the ten sites: four tests notice (E1, E3, E4, E8); six do not (E2, E5, E6,
E7, E9, E10, measured above). Three of the six take their text from the checkout:
E5 and E6 (the "not a plain file" refusals; the name comes from the canonical
skills and the destination, both data) and E9 (the unsafe-vendor-path warning; the
name and path come from the table). The code is right today; a later edit could
drop one of these and nothing would say so. This is the same shape as GS-CR7.

**Fix.** One parametrized test that drives each of the ten messages with an
escape-bearing name and asserts no `\x1b` or `\x07` in the output. The existing
`test_a_refusal_names_the_path_without_putting_control_bytes_on_the_terminal`
shows the pattern.

### [SW-CR6] non-blocking (low) — nothing checks what the heartbeat writes

`HandoffLock.heartbeat` (`:1301`) now rewinds, truncates and writes by descriptor.
Dropping the rewind (H9b) or the truncate (H9c) leaves a lock file that is not valid
JSON (NUL padding or leftover bytes, measured), and all 190 owning tests still
pass. The only heartbeat test asserts the outside file is untouched. The next
handoff reads such a file as an unknown holder and refuses, so it fails closed, but
the contract "the file holds a valid, current payload" is unpinned.

**Fix.** In `test_the_handoff_heartbeat_writes_the_file_it_holds_open`, after the
heartbeat, read the lock file, parse it and compare `heartbeat_at` to the one
before; add a second heartbeat with a shorter agent name to cover the truncate.

### [SW-CR7] non-blocking (low) — nothing pins that the temporary file name is random

`_write_replacing` (`:581`) names its temp file `.cairn-write-` plus 16 random hex
digits. With the name fixed (H3) every test still passes, yet a file committed at
that name then makes the copy-mode fan-out end in an uncaught `FileExistsError`
(measured: control no error). Randomness is what stops a clone from squatting the
name, and the existing test patches the random function to a constant to test
something else (that an existing name is not opened).

**Fix.** A test that calls `_write_replacing` twice and asserts the two temp names
differ (record the names through a patched `os.open`), or one that commits a file at
the name the *old* constant would give and checks the fan-out still works.

### [SW-CR8] non-blocking (low) — the "regular file" check in the read cannot run before a named pipe blocks it

`_read_regular_bytes` (`:617`) opens the path and then checks the opened descriptor
is a regular file. Opening a named pipe for reading blocks until a writer appears,
so a pipe at `.gitignore` hangs `session-start` forever, with or without the check
(measured, 6-second timeout, both). Git cannot store a pipe, so a checkout cannot
cause this; a local process could. The helper's docstring promises a refusal.

**Fix.** Add `os.O_NONBLOCK` to the open flags for the read; the open then returns
at once and the check refuses. Pin it with a pipe in a test that has a timeout.

## Seen, not raised

* **The Boundary B record's tree.** It was measured on `20f145ed` plus four files,
  and the body says so. It reproduces exactly (row 2), and the commit's own tree
  gives the same two failures (row 3), so no further run is owed.
* **The new tests are outside the gate manifest's pinned collection.** The 86 nodes
  in `test_session_writes_contained.py` are not in `bootstrap/tests/fixtures/gate_manifest.json`.
  No frozen file changed (the commit says so, and `tools/session.py` is not frozen), so
  nothing goes stale. It is the bookkeeping the earlier review asked to be named at
  the next serialization point.
* **A lone carriage return as the last byte of `.gitignore`.** The kept-bytes rule
  appends right after it, so git reads the new entry as part of the previous line
  and ignores nothing, and the next run sees the entry as already present (it splits
  lines on a bare CR). Classic-Mac line endings only. A break that stops treating a
  bare CR as a line end (S2) makes the result correct; the "lone CR" clause is the
  odd one. No one is likely to hit it.
* **Reads follow links.** `_heal_skill_copy` copies the bytes of a canonical file
  that is itself a link, so a linked canonical file puts outside bytes into the
  generated copy. That is a read of an outside file into the project, not a write;
  the alias-tier harnesses read `.agents/skills` directly in the same way.
* **A plain file where the harness folder should be.** A file named `.claude` makes
  `session-start` end in an uncaught `FileExistsError` (exit 1) on both the parent
  and this commit (measured), because the fan-out creates the folder's parent without
  a `LifecycleError`. A clone can cause it; the cost is a traceback, not a write.
  Same for a vendor-row name over 255 characters, by reading.
* **A hard link** at `.gitignore` is replaced, not written into (a test pins it);
  git cannot carry one.
* **Time between check and write.** The commit says so in the module header and
  closes it for the files (exclusive temp file and rename); a swap of a *parent*
  folder for a link between the check and the `mkdir` is the one gap left, and needs
  another process on the machine.
* **The engine's copy fallback** has the same leaf write; the body says it is not
  fixed here.

## What I did not cover

* Windows: junctions, reparse points, `core.symlinks=false` checkouts, the
  `O_BINARY` flag. All my runs were on macOS. Copy mode was simulated by failing the
  kernel's own probe link, not on a machine without link rights.
* Case-insensitive aliases of `.gitignore` or `.git` beyond what the new tests pin;
  I did not run on a case-insensitive volume other than the default one.
* The child tools the kernel runs: `tools/intent.py` (list, prune), `tools/evolution_infer.py`,
  `tools/prune_intents.py` and `tools/board.py`. Their own writes (the intent ledger
  in particular) are not behind `_assert_not_linked`; the handoff runs the project's own
  copy of `intent.py` with the resolved interpreter, which is the trust model the
  kernel already documents. I checked only that `session-end --handoff` reaches them
  the same way as on the parent.
* `HandoffLock._reclaim_or_refuse` and `release` as separate mutation targets. They
  only remove a name, after `acquire`'s guard; I did not break them individually.
* A real shell startup file as a link target. I used a stand-in file, and
  `.git/config` only inside a throwaway clone with a harmless marker.
* Bandit and the release ceremony beyond what the full suite runs
  (`test_security_lint` passed in both full runs with no skip).
* The interpreter binding (`_resolve_interpreter` and its helpers): AST-identical to
  the parent, so I did not re-test it. The Security Review owns that surface.

**Disposition.** Accept as a defect repair; no finding blocks it. SW-CR1 is the one I
would fix in this repair, since it is one line, it is tested, and it finishes what
the new rule starts. SW-CR2 is a second route to the same class and wants a decision
(fix now or record). SW-CR3 to SW-CR8 can ride one follow-up commit. Nothing about
this review changes a file the commit touched.

## Falsification run (summary of what ran)

* Full suite, base plus the four files: 2 failed, 3590 passed, 611 s. Full suite,
  `7e6a14e5`: 2 failed, 3618 passed, 613 s. Gates exit 0.
* 86 new tests on the parent: 82 failed, 4 passed.
* 190 owning tests as the control, then 67 breaks each with the 190 and the 14 clone
  scenarios, one fresh worktree each, both twins edited together; the proposed fix
  for SW-CR1 run the same way (190 passed, 14 clean).
* Fresh `solo-greenfield` install with both kernels, 10 flows and 20 `.gitignore`
  variant runs (plus a read-only file) compared byte for byte.
* Vendor-row probes (`.venv/bin`, `.venv/bin/python`, `dev/reflections`) on both
  kernels and on the proposed fix; the second pruner against a linked folder; the
  survivor measurements.


## Verification of the answer -- Claude Sonnet 5.5 -- 2026-10-19

**Scope**: a Boundary C check of the answer, commit `83b144f9` (SW-CR1 to SW-CR8,
with the Security Review's low items), and a check of `a95b9b31` (the fix for a
committed interpreter binding) for ordinary defects and regressions only. Its
security depth belongs to the Security Reviewer and I did not test it. This is not a
fresh review. Fresh session; the same agent type as the author, so the distance is a
fresh context. Internal; I do not claim External standing.
**Bytes**: the kernel twins, the pruner twins and both test files are byte-identical
at HEAD (`d2730303`) to `83b144f9`. The twins are identical to each other in both
pairs, and the two lockfile hash lines (`tools/session.py`, `tools/prune_reflections.py`)
equal the files' sha256.
**Interpreter**: Python 3.13.13 at `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
`PYTHONDONTWRITEBYTECODE=1`, darwin. Every run was in a detached worktree of the
commit under test, in a uniquely named scratch folder, removed afterwards. The three
full runs were nearly done and the 54-break sweep had just finished when the
shared-lock rule arrived; I let them finish and ran nothing heavy after it. Load on
the machine was above 20 during the runs, so the times are long (about 1100 s against
726 s recorded).

**Verdict**: **All eight findings are closed. The answer introduces no blocking
defect, and I found none in `a95b9b31`.** Three new low findings (SW-CR9 to SW-CR11),
none blocking.

**In plain terms.** I re-ran every route I had used to break the first commit, on the
answer. A vendor row can no longer replace the user's `.venv/bin/python` link or fill
their `.venv/bin` folder; the second pruner refuses a linked reflections folder and
deletes nothing; a read-only `.gitignore` is refused with the line to add, and one that
already holds the entry is left alone; the ten message sites, the heartbeat, the temp
name and the named pipe are all pinned now. All 14 hostile-clone cases are still clean,
and a fresh `solo-greenfield` install prints the same text as before except the
read-only case, which changed on purpose. Both recorded test figures reproduce. The
three new items are small: a legitimate-looking vendor row with another last name is
called "unsafe" without a reason, the pruner can still be steered by an operator's own
`--dir ...`, and the read-only refusal's remedy words are not pinned.

### One line per finding

| Finding | State | Evidence |
|---|---|---|
| SW-CR1 (vendor last name) | **closed** | `.venv/bin/python` row, link mode: the user's link is unchanged (still points at the interpreter). `.venv/bin` row, copy mode: `python` keeps the user's bytes, no `.diverged.bak`, no `.venv/bin/` line in `.gitignore`. `dev/reflections` row: the user's link is unchanged. All three print the existing "unsafe vendor path ... skipped" warning, exit 0. With the rule removed (LAST) 17 tests fail. Rows that must keep working still do: `.opencode/skills`, `.github/copilot/skills`, `.claude/skills/`. |
| SW-CR2 (second pruner) | **closed** | The outside-deletion probe now exits 2 with nothing deleted, on a real run and on `--dry-run`; the same for a link at `dev` and a link back into the project, and with the script run through a link above the project. Ordinary use is unchanged (default folder, relative `--dir`, absolute `--dir` from another folder); a folder the operator names outside the project is pruned as before. Breaks: call deleted (P1), link on the way unseen (P3), innermost-first boundary (P4), skipped on dry run (P5), exit 1 instead of 2 (P6) all killed. One residue is SW-CR10. |
| SW-CR3 (docs, wording) | **closed** | Each refusal now names the first link and the fix ("`dev/reflections` is a link; replace it with a real folder inside the project"; checked in C3 to C9). "Nothing to fan out" no longer follows a refusal (MSG2 killed). `bootstrap/UPGRADE.md` has two new bullets and `bootstrap/SAFETY.md` one sentence; each matches what I measured. A copy-side refusal still leaves the `.gitignore` entry already seeded (the fix list did not ask for that to change). |
| SW-CR4 (read-only `.gitignore`) | **closed** | Read-only, entry absent: exit 0, a warning that gives the exact line to add, file and mode untouched, nothing copied. Read-only, entry present with or without the slash: no refusal, copy proceeds. Absent file, empty read-only file, and a writable file behave as before; link mode never reaches it. Removing the check (RO1) fails a test; checking when the file is absent (RO2) fails 16; checking when the entry is already there (RO3) fails one. The wording of the remedy is not pinned (SW-CR11). |
| SW-CR5 (message encoding) | **closed** | I replaced each of the 21 `encode_display(` calls in the kernel by `str(`, one at a time: 21 of 21 killed (the first pass left six message sites unpinned). Measured with an escape byte in the name at each former survivor (outside-project, copy destination, quarantine name, divergence warning, unsafe vendor path, unsafe entry) and at the new lock-refusal and reclaim lines: no raw escape reaches the terminal. |
| SW-CR6 (heartbeat) | **closed** | Dropping the rewind (H9b) or the truncate (H9c) now fails `test_the_heartbeat_leaves_a_whole_current_payload_each_time`. Measured: after a long agent name then a short one, the lock file is valid JSON (137 bytes). |
| SW-CR7 (random temp name) | **closed** | A fixed name (H3) fails `test_each_write_gets_its_own_random_temporary_name`. Measured: two writes used `.cairn-write-766fc733…` and `.cairn-write-a3147237…` (16 hex digits each), and a file at the old fixed name no longer disturbs the copy-mode fan-out. |
| SW-CR8 (named pipe) | **closed** | A pipe at `.gitignore` is refused in 0.07 s (it hung before). Dropping the non-blocking open (H8nb) fails a test; dropping both regular-file checks (H8ab) fails a test; dropping the device and inode comparison (H8ino) fails two. Each of the two checks alone (H8a, H8b) passes the suite because the other recovers the case; the pair is what is killed, which is the measurement. |

### `.opencode/skill` (singular) is now skipped: is that acceptable?

**Yes, today; with one cost that SW-CR9 asks to soften.** Measured on the answer: a
row `.opencode/skill` is skipped with "unsafe vendor path for 'x': '.opencode/skill';
skipped." in link mode and in copy mode, exit 0, nothing made, while `.opencode/skills`
(plural) and `.github/copilot/skills` work. The shipped table has one link-tier row
(`.claude/skills`), so no shipped or adopter row is affected, and the skip is loud and
names the row. The rule is also written down for adopters in `bootstrap/UPGRADE.md`. What it
costs is the table's own promise: the table says a vendor refresh is a row edit and
never a redesign, but a harness whose folder is not called `skills` now needs a kernel
change, in two files plus a lockfile line. That is the right trade for a rule that
closes SW-CR1 in one line, as long as the person adding such a row is told. They are
not (SW-CR9).

### Boundary B records, against the committed bytes

| Record | Tree I built | Mine | Their figure |
|---|---|---|---|
| `a95b9b31` (binding) | detached worktree of `f949e342` with the commit's four files, committed as a private snapshot so the frozen-file self-checks see a clean tree | 4448 passed, 3 failed; the third, `test_security_stack.py::test_a_t4_output_is_bounded`, is a load failure (its own comment says the 5 s grace can run out on a loaded machine; the status read "truncated+cleanup-failed"). It passes alone in 0.2 s twice, which makes **4449 passed, 2 failed**. The two are `test_ast_attest.py::test_ast_gate_passes_over_the_full_scaffold_module_set` and `test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package`. | 4449 passed, 2 failed, 829 s |
| `83b144f9` (answer) | detached worktree of `a95b9b31` with the commit's eight files, committed as a private snapshot | **4508 passed, 2 failed** (the same AST pair), 1080 s, no skip, xfail or xpass | 4508 passed, 2 failed, 726 s |
| `83b144f9` itself | detached worktree of the commit | **5832 passed, 2 failed** (the same AST pair), 1092 s, tree clean; the larger count is the commits between the two bases | not recorded |

`scripts/quality_gate.py --sub neutrality --sub redundancy` on `83b144f9`: exit 0,
neutrality fail=0, redundancy fail=0. All three trees were clean before and after. The
snapshot commits were made only in my private worktrees (they are unreferenced objects
once the worktrees go). One frozen file changed, `templates/modules/default-on/prune_reflections.py`
(the manifest still pins blob `bf4d5f75`, the file is `d0d397ed`); no test reddens, and
the commit says the Maintainer re-anchors, which is right.

### The sweep and the probes

* **Break ledger on the answer**: 54 breaks (33 named, plus the 21 encoder calls),
  each in a fresh worktree with both twins of the file edited together, against 280
  tests (the eight files that read or import the kernel or the pruner); control 280
  passed. **48 killed, 6 survived**: H8a and H8b (each alone equivalent, see SW-CR8;
  the pair is killed), P2 (pruner guard after the listing: probes identical to the
  control, since listing deletes nothing and the guard still precedes every deletion;
  equivalent), P7 (root taken unresolved: the root is already resolved when it is
  built, so equivalent; probes identical), S2 (a lone carriage return, unchanged,
  not a finding, see below) and RO4 (SW-CR11). The guard sites G1 to G6 are still
  each killed by a test written for them (7, 4, 1, 1, 2 and 2 failures).
* **Hostile clones** (C1 to C14 as in the first pass): all clean on `83b144f9`; the
  refusals now name the link. G2, G4 and G6 still leak in the real command when
  deleted, as before.
* **Normal adopters**: fresh `solo-greenfield` install with the installer and kernel of
  `7e6a14e5`, and again with those of `83b144f9`, then the same ten flows and the `.gitignore` variants. Output is
  identical, byte for byte, except the read-only `.gitignore` line (now a refusal with
  the remedy). The binding gate leaves a normal install alone: the binding is
  untracked, still reported "from local-env.json", and no untrusted-binding warning
  appears. It asks git once per `session-start` (one `git ls-files`); average
  `session-start` time rose from 0.15 s to 0.20 s on the loaded machine, which is noise-level.
* **`a95b9b31`, ordinary checks only**: `_resolve_interpreter`, `_binding_untrusted`,
  `_warn_untrusted_once`, `_probe_interpreter`, `encode_display` and the other helpers
  are AST-identical between `a95b9b31` and `83b144f9`, as the answer says. The
  17 new binding tests are in the 280 and pass in the control; they drive the real
  command from a fresh clone. The repository's own `dev/.cairn/local-env.json` is
  untracked and ignored, so the dogfooded tree is not affected. I found no ordinary defect.

## New findings

### [SW-CR9] non-blocking (low) -- a vendor row with another last name is called "unsafe" and nothing says why, or where to change it

`_vendor_path_parts` (`tools/session.py:995`) now requires the last name to be
`skills`. The skip warning (`tools/session.py:1228`) still reads "unsafe vendor path
for 'x': '.opencode/skill'; skipped.", which calls a plausible row an attack and does
not name the rule. The table's own note (the `_doc` field of
`templates/skills/_data/vendor_targets.yml`) still says a vendor refresh is a row edit
and says nothing of the rule; it is written only in `bootstrap/UPGRADE.md`. And the
installer applies the older, looser test (`bootstrap/_scaffold/install.py:727`), so a
row like `.opencode/skill` would be installed as a link and then skipped by the kernel
at every `session-start`, never repaired, with a warning each time. Nothing shipped is
affected today.

**Fix.** Say the rule in the warning ("a vendor row must name a folder called 'skills'
inside another folder") and in one sentence of the `_doc` field; when a real harness
with another name is added, widen the rule to a named set in the same commit as the row.

### [SW-CR10] non-blocking (low, optional) -- the pruner's guard is blind to a `..` after a link in an operator's own `--dir`

`_refuse_linked_directory` (`tools/prune_reflections.py:70`) normalises the folder
lexically (`os.path.abspath`, `:78`) before it walks for links, so `--dir
dev/reflections/..` becomes `dev`, which is not a link, while the operating system
follows the link and then goes up one level. Measured with `dev/reflections` linked to a
folder inside an outside folder: the command exited 0 and deleted the older dated file
in the outside folder. Only an operator can cause this (no shipped skill or document
passes `--dir`; the default folder has no `..`), and the commit says a folder the
operator names is theirs; this is the one spelling that is inside the project and still
leaves it.

**Fix.** Refuse a `--dir` that contains a `..` part, or compare the real location of
the folder (`os.path.realpath`) with where the walk says it is and refuse when it is
outside the project but spelled inside it. One test.

### [SW-CR11] non-blocking (low) -- the remedy words of the read-only refusal are not pinned

`_GITIGNORE_READ_ONLY` (`tools/session.py:1055`) ends "make it writable, or add this
line yourself: ". With that phrase cut out (RO4) all 280 tests pass; the one test
(`bootstrap/tests/test_session_writes_contained.py:859`) matches only "read-only", so the
message could lose its remedy and nothing would say so. The behaviour is right today.

**Fix.** In that test, also assert the refusal text names the line to add (the entry) and
the words "writable".

## Seen, not raised

* **A lone carriage return as the last byte of `.gitignore`** (S2) still leaves the
  entry glued to the previous line for git. Unchanged, not asked for, exotic.
* **A copy-side refusal leaves the seeded `.gitignore` entry.** By design (the seed comes
  first so a refusal there copies nothing) and benign; I mention it because the first
  pass did.
* **`a95b9b31` costs a git call per `session-start`** and falls back, with a warning, in
  a folder where git cannot run. That is its stated design.

## What I did not cover (this pass)

* The security depth of `a95b9b31`: the link, tracked-name, case and git-failure
  routes. The Security Reviewer has them.
* Windows, and the `O_NOFOLLOW`-less path of `_read_regular_bytes` on a real Windows
  host; the tests simulate the missing flag. The answer says that platform has not been run.
* The first-pass breaks I did not repeat (the layered combinations, the symlink-probe
  and ordering breaks); the answer's own ledger covers them and the six guard sites were
  re-broken above.
* A fresh full run of everything at HEAD: the figures above are for the commit's bytes.
