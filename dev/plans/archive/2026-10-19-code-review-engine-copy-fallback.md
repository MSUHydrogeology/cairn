# Code review (Internal) — the installer's copy fallback (`cf707e2a`) — Claude Sonnet 5.5 — 2026-10-19

**Obligation**: code review (falsification) of a defect repair that has no plan,
the repair of SW-SR-2 in
`dev/reviews/2026-10-18-security-review-session-writes.md`. Fresh session, not the
implementing session. The implementer is the same agent type, so the distance here
is a fresh context, not a different type. This is an Internal pass; I do not claim
External standing. A separate Security Review of the same commit ran in parallel;
its commit landed while I worked and I did not read it or rely on it.
**Reviewed commit**: `cf707e2a` ("Installer fan-out: no copy, quarantine or probe
write goes through a link or leaves the project"), parent `2e1c9b3b`. It changes
three files: `bootstrap/_scaffold/install.py`, `bootstrap/_scaffold/SECURITY_MUTATIONS.md`
and the new `bootstrap/tests/test_engine_copy_fallback_contained.py` (33 tests). The
repository's HEAD moved while I worked; the two engine files and the new test file
are byte-identical at HEAD to `cf707e2a` (an empty `git diff`), so every line number
below holds at both. The implementer measured on `1e4f1e96` plus the change, eight
commits before the parent this landed on; that matters for Q1.
**Interpreter**: Python 3.13.13 at `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
`PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider`. Platform: darwin. Every write,
mutation, probe and test ran in a detached `git worktree` of `cf707e2a` (or of its
parent `2e1c9b3b`, or of `1e4f1e96`), each in a folder under one uniquely named
scratch directory, removed afterwards. The shared checkout was only read; my only
writes to it are the work-intent claim (`dev/intents.jsonl`, ignored by git) and this
file. I started every process I ran, and every one has exited. I killed two, each by
its process id: two runs of a helper of my own (one per engine) that blocked reading a
named pipe one of my test cases planted. Both ran against throwaway worktrees.

**Verdict**: NO BLOCKING FINDINGS — 0 blocking, 7 non-blocking.

**In plain terms.** The repair does what it says. A project that is only data (a
link, a folder, an odd file) can no longer make the installer's copy fallback write
through a link or outside the project. I checked this five ways.

1. I ran the real installer on hostile projects built from committed data alone.
   On the parent engine, with nothing patched, a committed folder at the old probe
   name forced copy mode, and then all four reported cases reproduced: copy mode
   forced, a file created outside the project, a divergent file moved into a folder
   outside, and an outside file rewritten in place (a hard link was rewritten in place
   too). On `cf707e2a` all of them leave the outside folder exactly as it was, byte for
   byte and in modification time.
2. I raced a thread against the copy, 400 times, swapping links in and out of the
   copy and quarantine names. The parent wrote through a link 248 times and moved a
   file into a linked folder 180 times. The repaired engine did neither, in any of the
   400.
3. I broke the repair 33 ways, one at a time. The tests catch 30. The 3 that get
   through are one harmless (a flag the other flag already covers), one that is not
   harmless but needs an attacker to guess a 64-bit random name (CF-CR2), and one
   unpinned handler (CF-CR3).
4. I ran a normal adopter's install, re-install, forced re-install, dry run and
   `upgrade --apply` that adds a skill, in link mode and in copy mode. The result
   matches the parent file for file, except that a current copy is no longer
   rewritten, which is the intent.
5. The full suite on the committed bytes gives **2 failed, 5655 passed**. The two are
   the AST tests the commit says are red until the combined re-anchor. The figure in
   the commit body (4465 passed) is right for the tree it was measured on but is not
   the figure for the tree it landed on (CF-CR4).

What I found is small. The one place a hostile project can still reach the terminal
is a warning the repair left as it was: it prints project file names raw (CF-CR1).
Two tests are missing that would pin the two non-harmless survivors (CF-CR2, CF-CR3).
The rest is record accuracy and documentation. None needs the commit reverted.

## Findings at a glance

| id | what | severity | blocks? |
|---|---|---|---|
| CF-CR1 | the divergence warning prints project file names raw: escape and bell bytes reach the terminal (measured); it also prints the absolute folder | low | no |
| CF-CR2 | the "equivalent pair" in the ledger is not a pair: without `O_EXCL`, a hard link or file planted at the temporary name is written into (measured); no test pins it | low | no |
| CF-CR3 | the `upgrade --apply` handler that turns a refusal into a warning is pinned by no test; removing it changes behaviour (measured: exit 2, stage folder left) | low | no |
| CF-CR4 | the Boundary B record was measured on a base eight commits older than the parent; its pass count does not reproduce on the committed bytes (4465 vs 5655) | low (process) | no |
| CF-CR5 | the red-run figure in the body (22 failed, 5 passed) does not match the committed file (23 failed, 10 passed, of 33) | informational (process) | no |
| CF-CR6 | an autouse fixture skips the whole test file where links cannot be made, including the tests that need no link; that is the platform where copy mode is normal | informational | no |
| CF-CR7 | `bootstrap/UPGRADE.md` still says a changed copy is "warned, not clobbered" and says nothing about the new refusal | informational | no |

Both open items the implementer named are dispositioned below ("Open items"): the
absolute paths are acceptable and the file names in the same warning are CF-CR1;
`seed_gitignore`'s `write_text` is the accepted window and is left alone.

## Q1 — Boundary B: does the record hold on the committed bytes?

Rule: AGENTS.md Boundary C, "no valid Boundary B record exists" means a fresh full run.
The record names a copy of `1e4f1e96` plus the change; the commit landed on `2e1c9b3b`.
Between them are eight commits, among them `a95b9b31` (the session kernel) and the
review-stance work that added `test_review_stance_in_shipped_files.py` (1746 test
nodes) and `test_session_binding_untracked.py` (17). So I ran the pair on the
committed bytes, in a clean detached worktree (0 changed paths before and after).

| check | commit body | measured on `cf707e2a` |
|---|---|---|
| `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` | 4465 passed, 2 failed, 0 skip/xfail/xpass, 886.5 s | **5655 passed, 2 failed**, 3 warnings, 0 skip/xfail/xpass (run with `-rfEsxX`, none listed), 1005.81 s |
| the 2 failures | the AST tests | `test_ast_gate_passes_over_the_full_scaffold_module_set`, `test_committed_baseline_accounted_for_across_the_engine_package` |
| `scripts/quality_gate.py --sub neutrality --sub redundancy` | fail=0, fail=0 | exit 0; neutrality fail=0 (info=56), redundancy fail=0 |
| collection on `1e4f1e96` plus the three files | — | 4467 nodes = 4465 + 2: the body's figure reproduces on its own base |
| collection on `cf707e2a` | — | 5657 nodes = 5655 + 2 |
| AST: CHANGED 5 → 7, NEW 86 | the two added digests `29ef25b1a8aba93d`, `28f5d712e82d2dd7` | derived by the runbook's Step 1: parent CHANGED 5 NEW 86; `cf707e2a` CHANGED 7 NEW 86; the two new digests match the body, and the five earlier ones are unchanged |
| "No frozen file changed" | stated | none of the three files is among the 183 `frozen_files` in `bootstrap/tests/fixtures/gate_manifest.json` |

The dispositions agree (the same two failures; no skip, xfail or xpass; both gates at
0). Only the pass count differs, by 1190 nodes. I did not account for the 1190 node by
node: the two new test files add 1763, so about 570 nodes must have gone elsewhere
(tests parametrized over files that the eight commits changed); I did not trace which.
This is CF-CR4. The 154 tests of the six files I used as the owning set (below) pass at
`cf707e2a`. The body's "wider 6 files, 157 passed" does not name its six; my natural six
(the four owning files, `test_skills_self_heal.py`, `test_session_writes_contained.py`)
give 154. I did not chase the 3.

## Q2 — The set claim: every guard call site, mutated

**The set, listed from the tree** (not from the diff). In the three functions the
install's fan-out reaches (`_symlinks_available`, `_emit_skill_copy_fallback`,
`fan_out_skills`) and the two callers that turn a refusal into an exit:

| # | site | where (at `cf707e2a`) |
|---|---|---|
| S1 | `check(out)` → `_assert_safe_write` | `install.py:600` |
| S2 | `check(bak)` | `install.py:620` |
| S3 | the `_assert_safe_write` inside `check` | `install.py:587` |
| S4 | `_assert_fanout_contained(dst, target)` | `install.py:719` |
| S5 | `_assert_safe_write(gitignore, target)` inside `seed_gitignore`, reached from `fan_out_skills` in copy mode | `install.py:235`, called at `:728` |
| S6 | refusal: a file where a folder must go | `install.py:604` |
| S7 | refusal: a non-plain file at the copy name | `install.py:612` |
| S8 | refusal: a non-plain file at the quarantine name | `install.py:621` |
| S9 | skip a copy that is already current | `install.py:617` |
| W1–W7 | the writes: probe `os.symlink` and `unlink` (`:497` on), `os.replace(out, bak)` (`:637`), `mkdir` (`:639`), the exclusive temp open (flags `:628`–`:631`, open `:641`), `os.replace(tmp, out)` (`:645`), the temp cleanup (`:646`–`:651`) | `install.py` |
| K1 | the `ScaffoldSecurityError` handler around `fan_out_skills` | `cli.py:539` |
| K2 | the best-effort handler around `fan_out_skills` on `upgrade --apply` | `upgrade.py:2231` |
| — | `_emit_skill_symlink` (unchanged; its guard is S4, so S4's row covers it) | `install.py:511` |

The body names four guard sites (S1, S2, S3, S4). S5 sits on the same route (copy mode
calls `seed_gitignore` after each copy), S6 to S9 are guards of a kind, and K1 and K2
are where a refusal becomes behaviour. I mutated all of them (the ledger's Id column
maps to this list: G for S1 to S5 and S6 to S9, W for the writes, K for the callers).

**Method.** Each break is applied alone, by an edit that fails unless it matches
exactly once, to a scratch worktree of `cf707e2a` that is restored from the
pristine file before the next break (never in the shared tree). "Owning six" is the six test
files that import or read the touched code: `test_security_leaf.py`,
`test_skills_self_heal.py`, `test_engine_copy_fallback_contained.py`,
`test_session_writes_contained.py`, `test_install_module.py`, `test_skills_fanout.py`
(154 tests). "Probe" is my own run of the real installer on seven hostile projects
(copy mode, by failing only the symlink probe): a dangling link at a copy name, a
quarantine name linked to an outside folder, to a missing file, a copy name linked to
an equal outside file, a hard link to an equal outside file, a linked skill folder, a
linked `.claude/skills`; a leak is any change outside the project. "Race" is the
thread race (200 iterations). The AGENTS.md rule for equivalence is applied literally.

**Unmutated control (G0): 154 passed; the seven probes leak nothing; the race: 0 leaks
in 200 iterations.**

| Id | Break | Owning six | Probe / race | Verdict |
|---|---|---|---|---|
| G1-del | delete `check(out)` | 7 failed | probe leaks through a linked skill folder and a linked `.claude/skills` | killed |
| G2-del | delete `check(bak)` | 1 failed | probe: no leak (the rename and the plain-file refusal also stop it) | killed |
| G3-del | the guard inside `check` becomes `pass` | 10 failed | probe leaks the same two | killed |
| G3-old | the guard inside `check` is the old `_assert_fanout_contained` (permits a link at the name) | 6 failed | probe: no leak (the rename write also stops it) | killed |
| G4-del | delete `_assert_fanout_contained` in `fan_out_skills` | 6 failed | probe: no leak in copy mode | killed |
| G9 | delete the guard in `seed_gitignore` | 1 failed (the guard-presence test) | not probed; the earlier repair's tests also kill it | killed |
| G1-late | `check(out)` moved after its write | 7 failed | probe leaks the same two; race 0 | killed |
| G2-late | `check(bak)` moved after its write | 1 failed | probe none; race 0 | killed |
| G1-partial | `check(out)` only inside the write loop, not for the whole set first | 4 failed | — | killed |
| G2-partial | `check(bak)` only inside the write loop | 2 failed | — | killed |
| G5-del | delete the file-where-a-folder-must-go refusal | 1 failed | probe: none | killed |
| G6-del | delete the non-plain-file refusal at the copy name | 1 failed | probe: none | killed |
| G7-del | delete the non-plain-file refusal at the quarantine name | 1 failed | probe: none | killed |
| G8-del | an already-current copy is rewritten | 1 failed | — | killed |
| O-inline | write each file as soon as it is checked (no whole-set check first) | 9 failed | probe: none | killed |
| W1-move | quarantine by `shutil.move` | 1 failed (the late-swap test only) | **race: 4 of 200 moved into a linked folder** | killed |
| W2-noexcl | temp open without `O_EXCL` | 0 failed | race 0; **a planted hard link at the temp name is written into** (below) | **survived, not equivalent** (CF-CR2) |
| W3-nonofollow | temp open without `O_NOFOLLOW` | 0 failed | race 0; a symlink, hard link and file planted at the temp name all refused | **survived, equivalent** (below) |
| W4-neither | neither flag | 1 failed | a planted symlink is written through | killed |
| W5-fixedtmp | fixed temp name | 1 failed (incidentally: the test plants at a mocked name) | — | killed |
| W6-direct | write straight to the copy name | 3 failed | **race: 11 of 200 wrote through a link** | killed |
| W7-copyfile | finish with `shutil.copyfile(tmp, out)` | 2 failed | **race: 7 of 200 wrote through a link** | killed |
| W8-nocleanup | no temp cleanup on failure | 1 failed | — | killed |
| W9-probe-fixed | probe name fixed again | 9 failed | — | killed |
| W10-probe-leak | probe link not removed | 1 failed | — | killed |
| W11-probe-oldclean | old cleanup-first on a fixed name | 9 failed | — | killed |
| W12-nomkdir | no `mkdir` of the copy folder | 8 failed | — | killed |
| S1-raw | refusal shows the name unescaped | 1 failed | — | killed |
| S2-abs | refusal shows the absolute path | 1 failed | — | killed |
| S3-noremedy | refusal drops the remedy line | 4 failed | — | killed |
| S4-leak | refusal carries the guard's own text (where a link points) | 2 failed | — | killed |
| K1 | `cli.py`: the refusal handler removed | 13 failed | — | killed |
| K2 | `upgrade.py`: the apply-time handler removed | 0 failed (and 0 of 179 in the five upgrade test files) | **`upgrade --apply` over a refused copy name exits 2 and leaves the stage folder** | **survived, not equivalent** (CF-CR3) |

**33 breaks: 30 killed, 3 survived.** The implementer's 28 and 26 are a subset of this
set with the same shape: the four named guard sites and the writes all die. Reading
the probe column: removing the guard that looks at ancestors (G1, G3) opens a write
through a linked folder at the real entry point; the other guard breaks do not leak
because another layer still stops them (the rename-based write for a link at the last
name, the plain-file refusals, the check for the other name). That is defence in depth.
The tests kill those breaks by asserting the refusal, not a leak, so I do not call them
equivalent: the refusal is a stated property. W1, W6 and W7 leak only under a race, and
the late-swap tests are what kill them.

### The "equivalent pair" is not a pair

The body says `O_EXCL` alone and `O_NOFOLLOW` alone survive as one measured equivalent
pair, and that dropping both is killed. The last half is right (W4). The first half is
only half right. I planted three objects at a guessed temporary name (the test's trick
of fixing `secrets.token_hex`) and called `fan_out_skills`:

| planted at the temp name | control | no `O_EXCL` (W2) | no `O_NOFOLLOW` (W3) | neither (W4) |
|---|---|---|---|---|
| symlink to an outside file | refused, outside unchanged | refused, unchanged | refused, unchanged | **written through** |
| hard link to an outside file | refused, unchanged | **completed; outside file overwritten** | refused, unchanged | **written through** |
| a regular file | refused | completed (planted file overwritten) | refused | completed |

`O_NOFOLLOW` alone does not stop a hard link or a file at that name; `O_EXCL` does.
So W3 is equivalent on a platform that has `O_NOFOLLOW` (the symlink case is covered by
`O_EXCL`, and breaking the recovering site, W4, fails), but W2 is not. Where
`O_NOFOLLOW` is missing (`getattr(os, "O_NOFOLLOW", 0)` is 0 on Windows), W2 is the same
as W4. The name is 64 random bits, so this is not reachable by a project today; the
issue is that a stated "equivalence" was not measured, and that one flag's real job is
unpinned. CF-CR2.

## Q3 — The tests against the parent

The body says 22 failed and 5 passed against the unchanged engine. I copied the
committed test file into a clean worktree of `2e1c9b3b` (the parent; its engine is the
unfixed one, `git diff cf707e2a^ cf707e2a -- bootstrap/_scaffold` is the repair) and ran
all 33: **23 failed, 10 passed.** (22 + 5 is 27, not 33; CF-CR5.) At `cf707e2a`: 33
passed.

The 10 that pass on the parent, and whether each can be red there:

| passes on the parent | why | can it be red there? |
|---|---|---|
| `data-alone[quarantine-name-linked-to-a-missing-file]` | the parent quarantines by rename, and a rename replaces a dangling link | no, the parent is safe for this shape |
| `data-alone[harness-folder-linked]` | the parent already refuses a linked harness folder | no |
| `copy-mode[harness-skills-folder-linked]`, `copy-mode[harness-folder-linked]` | already refused by the parent's guard | no |
| `linked-folder-above[harness-folder]`, `[skills-folder]` | already refused by `_assert_fanout_contained` at the parent | no |
| `a_divergent_copy_is_still_quarantined_and_regenerated` | ordinary behaviour, unchanged | no |
| `a_hard_link_to_an_outside_file_is_replaced_not_written_into` | the parent's quarantine renames; the test uses differing bytes | no (with equal bytes the parent rewrote the outside file; that shape is the probe's `hardlink_equal`, not this test) |
| `the_probe_reports_no_links_where_none_can_be_made_and_leaves_nothing` | fail-soft pin | no |
| `a_link_swapped_in_at_the_quarantine_name_after_its_check_is_replaced_not_followed` | its swap arms only for names under `session-end`, which the parent's file-by-file loop reaches after `_data` is done | no as written. It is not vacuous: it is the only test that kills `shutil.move` (W1), and the real race shows W1 leaks (4 of 200). |

So the body's "5" is 10 in the committed file, and each of the 10 is accounted for.
None can be made red against the parent without changing the test, and none is a
placebo on the repaired code, except as noted for the last one, which earns its place
by killing W1. The instrument was confirmed to detect: the 23 reds are the same
property checks, run on the parent.

## Q4 — Hostile projects, parent against repaired, through the real installer

Built from committed data alone and run as a subprocess (`bootstrap/scaffold.py`).
"Copy mode" fails only the symlink probe (links still work), so the engine is not
told which path to take. "Outside" is a snapshot of a folder beside the project, with
bytes, modification time and inode.

| project data | parent `2e1c9b3b` | repaired `cf707e2a` |
|---|---|---|
| **data alone, link mode**: a committed folder at the old probe name, then | | |
| … a dangling link at a copy name | copy mode forced, **`outside/.zshenv` created** | outside unchanged |
| … a quarantine name linked to an outside folder | **divergent file moved into the outside folder** | unchanged |
| … a copy name linked to an equal outside file | **outside file rewritten** | unchanged |
| … a hard link at a copy name to an equal outside file | **outside file rewritten in place** | unchanged |
| … a plain install with only the folder | copy mode forced (`.claude/skills` is not a link) | link mode, `.claude/skills` is a link |
| **copy mode**: dangling link at a copy name | outside created | refused, exit 2, outside unchanged |
| quarantine name linked to an outside folder | file moved in | refused, exit 2 |
| quarantine name linked to a missing file | unchanged (rename replaces it) | refused, exit 2 |
| copy name linked to an equal file | rewritten | refused, exit 2 |
| hard link, equal bytes | rewritten in place | exit 0, **not rewritten** |
| hard link, differing bytes | unchanged | exit 0, unchanged |
| skill folder linked, `.claude/skills` linked, harness folder linked | refused, exit 2 | refused, exit 2 |
| a folder at the copy name | traceback, exit 1 | plain refusal, exit 2 |
| a file where a folder must go | traceback, exit 1 | plain refusal, exit 2 |
| a named pipe at the copy name | traceback, exit 1 (`SpecialFileError`) | plain refusal, exit 2, no hang |
| `.gitignore` linked | refused, exit 2 (the earlier repair) | refused, exit 2 |

A refused install exits 2 after the earlier steps of the install have run (40 to 44
paths made), the same shape as the parent's own refusal for a linked harness folder.
I removed the link in one case and re-ran: exit 0, and the copy is written. The
refusal text carries the remedy line ("remove that link ... then re-run").

**The race** (400 iterations, a thread swapping links in and out of the copy and
quarantine names while the fan-out runs): parent, 248 files created through a link and
180 files moved into a linked folder; repaired, 0 and 0 (370 stopped at the check, 30
completed with the link replaced). This is the property the rename-based write was
built for, and it holds in a real race, not only in the tests' hooks.

**The accepted window, forced.** The commit says a parent folder swapped for a link
between the check and the write is the accepted engine window. I forced it with a hook
and it wins: the temp file and the copy land in the outside folder. The same holds
for the `.gitignore` seed (open items, below). Both need a process on the machine,
which is the stated threat model.

## Q5 — Normal adopters

All on `cf707e2a`, against the parent, with the same profile.

| check | result |
|---|---|
| fresh install, link mode | 104 paths; `.claude/skills` is a link; byte-identical to the parent except the lockfile's commit id; no stray probe or temp name |
| fresh install, copy mode (probe-only failure) | 110 paths; same advisory line as the parent; `.gitignore` gains `.claude/skills/`; byte-identical (content and mode) except the commit id |
| re-run of the install | repaired: **21** files rewritten, none under `.claude/skills/`. Parent: 24 (the same 21 plus `_data/vendor_targets.yml`, `session-end/SKILL.md`, `session-start/SKILL.md`). The 21 are the base-cache copies the installer rewrites in link mode too, not this commit's |
| `--force` re-install | exit 0 in both modes; in copy mode an edited copy is quarantined to `SKILL.md.diverged.bak` (holding the edit) and regenerated, as on the parent |
| `--dry-run` | exit 0, creates nothing, leaves no probe link (both) |
| divergent copy, plain install in copy mode | quarantined and regenerated, warning printed; same as the parent |
| `upgrade --stage` then `--apply` on a pre-skills adopter | exit 0 in link and copy mode; the three skill files are recorded in the lockfile; the stage folder is removed; the final tree matches the parent except the commit id; a divergent copy is quarantined (`SKILL.md.diverged.bak` holds the edit) |
| the same, with a dangling link at a copy name | parent: **wrote `outside`**. Repaired: `[warn] skills fan-out skipped: refusing to write skill copies through a link ...: .claude/skills/session-start/SKILL.md`, exit 0, lockfile updated, outside empty |

I found no behaviour change a normal adopter would feel. The visible ones are all
improvements: a current copy keeps its timestamp, an odd object at a copy name is a
plain refusal with a remedy instead of a traceback, and the refusal never prints where
a link points.

## Open items the implementer named

**1. Unescaped absolute paths in warnings — acceptable in part; the file names in the
same warning are CF-CR1.** The absolute paths in these messages are the user's own
`--target` plus a vendor folder from Cairn's own table (`load_vendor_targets` reads
`templates/skills/_data/vendor_targets.yml` from the Cairn root, not from the project),
so a checkout does not control them. No change needed for those. The same warning also
prints the file names it quarantined, and those are project data (CF-CR1).

**2. `seed_gitignore` still uses `write_text` — leave it; it is the accepted window.**
Forced: a swap of `.gitignore` for a link to an outside file between the guard and the
`write_text` appends `.claude/skills/` to the outside file. That is the TOCTOU window
`bootstrap/SAFETY.md` already accepts ("a small TOCTOU window between the scaffold
engine's `_assert_safe_write` containment check and the write", no concurrent
filesystem attacker). A project cannot win it with data alone. It is the earlier
repair's function, not this commit's, and the model-mapping plan may consolidate the
write helpers. I recommend one sentence in the `seed_gitignore` row of
`SECURITY_MUTATIONS.md` naming it as a last-name window, so the two postures in the
engine (copies close it, the `.gitignore` seed does not) are stated rather than
discoverable. No code change.

## Findings

### [CF-CR1] low, non-blocking — the divergence warning prints project file names raw

**What.** `_emit_skill_copy_fallback` prints, when it quarantines a copy,
`copy-fallback divergence under {dst}: {', '.join(quarantined)} differed ...`
(`install.py:654`–`:655`). `quarantined` holds `str(rel)` (`:638`), the path of a file
under the project's `.agents/skills/`: project data. The repair escapes the refusal's
name (`shown`, `:575`) but not this line, and the test that guards it
(`test_a_refusal_puts_no_raw_control_bytes_on_the_terminal`) covers the refusal only.

**Evidence.** A canonical skill file named `x<ESC>]0;PWNED<BEL>.md` with a divergent
copy of the same name, installed in copy mode: stderr carries the raw bytes
(`session-start/x^[]0;PWNED^G.md` in `cat -v`). The same bytes are printed by the parent,
so the repair did not introduce it, but it touched the function and its docstring says
project names are escaped. The only other output in the fan-out route that can carry
project text is this one.

**Why low.** The reader has to run the installer in a hostile repository (the adoption
path, so in scope) and the repository has to commit a copy under `.claude/skills/`
that differs. The cost is a terminal title or other escape sequence on stderr, not a
write.

**Fix** (tested in a scratch copy: with the test below it fails on `cf707e2a` and
passes with the edit; the six owning files plus `test_skills_upgrade.py` and
`test_security_lint.py`, 176 tests, stay green):
`quarantined.append(shown(dst / rel))` at `:638`, and `shown(dst)` in place of `{dst}` at
`:654`, which also makes the line project-relative like the refusal. Add a test beside
the existing control-byte one: a canonical file with an escape in its name, a
divergent copy, copy mode, assert no `\x1b` or `\x07` on stderr and `\\x1b` present.
This changes `_emit_skill_copy_fallback` again, which is already in the CHANGED set
(no new AST symbol), so the pending re-anchor takes the new digest.

### [CF-CR2] low, non-blocking — the ledger's "equivalent pair" is half wrong, and `O_EXCL`'s own job is unpinned

**What.** See Q2. Removing `O_EXCL` lets a hard link or a regular file at the
temporary name be opened and written into; `O_NOFOLLOW` alone refuses only a symlink.
The body's claim that both survive as an equivalent pair is not what the AGENTS.md rule
calls equivalent (a break that changes no behaviour). `test_a_link_at_the_temporary_name_is_not_written_through`
plants only a symlink, so it cannot tell the flags apart.

**Evidence.** The table in Q2: under W2 a planted hard link ends with the outside file
overwritten and the call completes; under W3 it is refused. The name is
`secrets.token_hex(8)`, so a project cannot plant it today. On a platform without
`O_NOFOLLOW`, `O_EXCL` is the only flag in force.

**Fix.** Parametrize that test over a symlink, a hard link and a regular file at the
guessed name; assert `OSError` and that the outside file's bytes are unchanged (and
that the planted regular file is untouched). Drafted in a scratch copy: it passes on
`cf707e2a` and fails on W2 for both new variants. Then say in the Response that W3 is
equivalent on a platform with `O_NOFOLLOW` and W2 is not.

### [CF-CR3] low, non-blocking — nothing pins the apply-time handler

**What.** `upgrade --apply` calls `fan_out_skills` inside `except Exception ... warn`
(`upgrade.py:2231`), so a refusal during an apply that adds a skill warns and lets the
already-applied upgrade finish. The repair makes refusals more frequent in copy mode.
No test exercises that handler: replacing it with `except KeyError` (K2) passes the
owning six and all 179 tests of `test_upgrade*.py` and `test_skills_upgrade.py`.

**Evidence.** Behaviour under K2, measured through the real command: `upgrade --apply`
over a dangling link at a copy name prints `error: upgrade --apply refused (containment)
...`, **exits 2, and leaves `dev/.cairn-upgrade/` behind**, after the lockfile has
already advanced. Under the unmutated code it warns, exits 0, removes the stage folder
and records the skills. So K2 is a real behaviour change, not an equivalent break.

**Fix.** One test in `test_skills_upgrade.py`'s pre-skills pattern: install in copy mode
(patch `_symlinks_available` to False), make the pre-skills state, plant a dangling
link at `.claude/skills/session-start/SKILL.md`, `--stage`, `--apply`; assert exit 0,
`skills fan-out skipped` and `remove that link` in stderr, the outside folder empty,
the three skill files in the lockfile, and no stage folder. Drafted in a scratch copy:
passes on `cf707e2a`, fails on K2. That file is frozen (it is in `frozen_files`), so the
test belongs in the new file instead.

### [CF-CR4] low (process), non-blocking — the Boundary B record is for a different base

**What.** The record is correct for what it measured and cannot be compared with the
tree it landed on. It was taken on `1e4f1e96` plus the change; the parent is `2e1c9b3b`,
eight commits later, and the full suite on the committed bytes has 1190 more passing
tests (Q1). AGENTS.md asks for the run "on exactly the bytes being committed: a tree
clean apart from the change, or a separate copy holding only it", which a later parent
turns into a copy of a stale base.

**Evidence.** Q1, with the collection counts: 4467 nodes on the implementer's base
(reproducing 4465 + 2), 5657 on `cf707e2a` (matching my 5655 + 2).

**Fix.** Nothing to redo: I have the run on the committed bytes. Carry my figures
(2 failed, 5655 passed, 1005.81 s, Python 3.13.13, gates at 0) into the Response, or
into the AST re-anchor commit's body, and state the base the figure belongs to. Next
time build the scratch copy on the actual parent (`git worktree add <parent>` and apply
the patch) so the counts match what lands.

### [CF-CR5] informational (process), non-blocking — the red-run figure does not match the committed file

**What.** The body says "22 failed, 5 passed" against the unchanged engine and names
33 tests; those add to 27. Measured against the parent: 23 failed, 10 passed, of 33
(Q3). The ten are all explained, so this is a record error, not a gap in the tests.

**Fix.** State 23/10 in the Response.

### [CF-CR6] informational, non-blocking — the autouse link fixture skips every test where links cannot be made

**What.** `_links_must_work` (`test_engine_copy_fallback_contained.py:61`) is `autouse`,
so on a machine that cannot make links (Windows without Developer Mode, the platform
where the copy path is the normal one) all 33 tests skip. Nine of them need no symlink:
the three non-plain-file refusals (a folder at the copy name or at the quarantine name,
a file where a folder must go), the divergent-copy pin, the current-copy pin, the
failed-rename cleanup, the hard-link pin, and the two probe pins that use no real link
(its name is new each call; it reports no links where none can be made). Only the tests
that plant a symlink need the skip.

**Fix.** Move the skip from the autouse fixture into the fixtures or tests that plant
a link. Cairn has no CI, so nothing runs these on Windows today; I could not either
("What I did not cover").

### [CF-CR7] informational, non-blocking — `bootstrap/UPGRADE.md` is stale on the fan-out copies

**What.** `bootstrap/UPGRADE.md` (line 211 at `cf707e2a`) says the regenerated vendor
copies come "with a divergence guard that warns rather than clobbers a copy you edited
in place". The code quarantines the edit to `.diverged.bak` and then regenerates (that
sentence predates this commit and was already inexact). It also says nothing about the
refusals this commit adds: an install or an apply that meets a link, a folder or a file
in the wrong place at a copy name now stops (install, exit 2) or skips the fan-out with
a warning (apply), and the message carries the remedy. The earlier `.gitignore` repair
added such a paragraph for its own refusal (GS-CR6).

**Fix.** One sentence in that section: what is quarantined, and that a link or an
unexpected object at a copy name is refused, with the fix. Note that the shared tree has
uncommitted edits to `bootstrap/UPGRADE.md` from another session, so serialise this with
that session's commit.

## Seen, not raised

* **Copy mode still reads through links under `.agents/skills/`** (SW-SR-8 in the
  session-writes Security Review). A canonical `SKILL.md` that is a link to an outside
  file has that file's bytes copied into `.claude/skills/...` (measured: `TOP SECRET`
  from an outside file). This commit changes the write side only, and the inventory row
  says "a copy never follows a link" about writes; the read side is unchanged and
  tracked. The fix is a `src_file.is_symlink()` check in the plan loop (`:596`).
* **Hard links to an outside file** (SEC-3, owed to the model-mapping plan) pass the
  guard by design. The repair no longer writes into them, because a copy is a rename:
  a test pins it for differing bytes and my probe for equal bytes (the outside file was
  rewritten in place on the parent and is untouched now).
* **`_emit_skill_symlink`** is unchanged and unreviewed by this commit; its guard is S4
  (G4-del is killed by 6 tests).
* **A stale `.cairn-symlink-probe-*` link** from a process killed between making the
  link and removing it would now stay (the old code cleaned the fixed name). The window is
  a few lines wide and a link to `.` is harmless; not worth a change.
* **A caller that passes an unresolved `target`** to `_assert_safe_write` makes its
  ancestor walk a no-op (the function says the caller resolves it). Both engine callers
  (`cli.py`, `upgrade.py`) resolve. Not reachable from the commands.
* **The commit body is 46 lines** against AGENTS.md's target of 15 to 30.
* **`ascii()` as the escape** is not ambiguous: it also escapes a literal backslash, so
  `\x1b` typed in a name and a real escape byte look different.

## What I did not cover

* **Windows**: reparse points, junctions, `core.symlinks=false` checkouts, how `os.replace`
  behaves when the destination is open, and the `O_BINARY` branch. All my runs were on
  macOS, where `O_NOFOLLOW` exists.
* A **real shell startup file** as a link target. I used stand-in files.
* **`_emit_skill_symlink`** beyond its guard; **`seed_gitignore`'s** guard beyond the one
  break G9 and the forced swap; the other callers of the earlier repair.
* **Bandit** separately: the full suite's `test_security_lint` passed with no skip
  reported; I ran no other static check.
* The **1190-node difference** between the two bases, node by node (Q1).
* The Security Review of this commit (not read, by design), and the rest of the
  repository's interleaved commits.
* **The Boundary B timing** (886.5 s on the body, 1005.81 s here): other sessions were
  running pytest on the same machine, so I treat both as indicative only.

**Disposition**: accept. No finding blocks and the commit needs no revert. CF-CR1 is the
only one with a code change, two lines in the function the commit already changed, and
CF-CR2 and CF-CR3 are two missing tests; CF-CR4 to CF-CR7 are the record and the docs.
They can ride one follow-up commit with the AST re-anchor.
