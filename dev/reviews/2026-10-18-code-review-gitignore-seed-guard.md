# Code review (Internal) — the `.gitignore` seed guard (`b8a402c6`, `fde3054c`, `8335e9f4`, `3ba6f230`) — Claude Sonnet 5.5 — 2026-10-18

**Obligation**: code review (falsification) of a defect repair that has no plan.
Fresh session, not the implementing session. The implementer is the same agent
type, so the distance here is a fresh context, not a different type. This is an
Internal pass; I do not claim External standing.
**Reviewed range**: `b8a402c6` through `3ba6f230` (four commits), and the engine
files as they stand at `3ba6f230`. `9832c411` (the parent of `b8a402c6`) is the
"unfixed" engine below. Other sessions' commits sit between these four and are not
reviewed.
**Interpreter**: Python 3.13.13 at `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
`PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider`. Platform: darwin. Every
write, mutation, probe and test ran in a detached `git worktree` of `3ba6f230`
(or of `9832c411`), each in a fresh empty folder under the session scratchpad,
and was removed afterwards. The shared checkout was only read.

**Verdict**: REVISE — 1 blocking, 5 non-blocking.

**In plain terms.** The four commits do what they say. A project whose `.gitignore`
is a link to a file somewhere else is now refused before anything is written, by
every Cairn entry point I could list from the code: install, install dry run,
`upgrade --stage`, `--apply` and `--adopt-module`. On the unfixed engine six of my
runs (install, install with copy-mode fan-out, stage, apply, apply with copy-mode
fan-out, adopt) all wrote through the link. On the repaired one they exit 2 and
create nothing, not even a folder. The new tests fail on the unfixed engine and
pass on the repaired one. Of 26 single deliberate breaks of the repair, the tests
catch 15, 10 are harmless (I measured that, not argued it), and 1 gets through
the owning tests (GS-CR3). The full suite at `3ba6f230` gives 3401 passed and 2
failed, the two AST tests the commits already expect.

The defect is not closed, though. Cairn ships a second, separate piece of code
that appends to `.gitignore`: the `session-start` routine, in its "copy" mode. It
has no check, and the repair, its tests and its inventory never saw it, because it
does not go through `seed_gitignore`. A repository can force that mode with an extra
folder, so it does not depend on a Windows machine. In a throwaway clone I got the
unmodified `tools/session.py session-start` to write attacker-chosen lines into
`.git/config`, and git then ran the command those lines named (GS-CR1). The fix is
small, and I tested it. The other five findings are about evidence and wording.

## What I verified

| # | Check | Result |
|---|---|---|
| 1 | The four diffs, and the engine at `3ba6f230`: `seed_gitignore` (`bootstrap/_scaffold/install.py:203`), the three preflights (`bootstrap/_scaffold/cli.py:457`, `bootstrap/_scaffold/upgrade.py:1533`, `bootstrap/_scaffold/upgrade.py:2481`) | Match the commit bodies. The guard runs before the read, on dry runs too. No general `except` was added: a dangling `AGENTS.md` link at install still exits 1 with a traceback naming `ScaffoldSecurityError`, which the commit body says the differential oracle pins (those tests are green at `3ba6f230`). |
| 2 | **Boundary B record** | The figure quoted in the brief **reproduces** but is **not in the commit bodies** (GS-CR2). I ran the pair myself on a clean worktree of `3ba6f230`: `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` gave **2 failed, 3401 passed** in 1049 s (17 min 29 s), Python 3.13.13, tree clean before and after. The two failures are `test_ast_attest.py::test_ast_gate_passes_over_the_full_scaffold_module_set` and `test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package` (the four CHANGED symbols of row 8); no skip, xfail or xpass was reported. Gates: `redundancy` 0 findings; `neutrality` red for reasons outside this repair (row 9). |
| 3 | The call-site set, listed from the tree | 13 sites in 4 files (one of them has a byte-identical self-hosted copy); table below. An AST call graph over `bootstrap/_scaffold/` and `bootstrap/scaffold.py` gives the callers of `seed_gitignore`: `main`, `cmd_upgrade` (through `_write_stage`, `_apply_upgrade`, `_cmd_adopt_module`), `fan_out_skills`, `write_local_env`. `--plan`, `--init-lock`, `--finalize`, `--adopt-collisions`, `--manifest` and `--summary` do not reach it. A search of the whole tree for `gitignore` finds exactly two places that write the file: `bootstrap/_scaffold/install.py:237` and `templates/skills/_lib/session.py:797`. The second is GS-CR1. |
| 4 | Entry-point probes, unfixed (`9832c411`) against repaired (`3ba6f230`) | Table below. |
| 5 | Variants of the `.gitignore` object | Table below. |
| 6 | The new tests can fail | On `9832c411`, with the three changed test files copied in from `3ba6f230`, I ran 24 nodes (the new class, all of `test_skills_upgrade.py`, all of `test_security_leaf.py`): **11 failed**, 13 passed. The 11 are the 8 nodes of `TestGitignoreSeedingRefusesLinks`, the stage and apply tests, and `test_guarded_write_functions_still_call_a_containment_guard`. The `--plan` test passes on both, as it should: it is a negative control. |
| 7 | `SECURITY_MUTATIONS.md` against the code | The rows for `_cmd_adopt_module`, `_apply_upgrade`, `_write_stage` and `seed_gitignore` are accurate (probes: exit 2, 0 paths written, `--plan` unaffected). The opening sentence at line 12 is not (GS-CR4). The inventory's scope is the engine package, so it is silent on the session helper (GS-CR1). |
| 8 | AST attestation, by the runbook's Step 1 | CHANGED 4 (`_cmd_adopt_module`, `cmd_upgrade`, `main`, `seed_gitignore`), MISSING 0, DUPLICATE 0, NEW 86. The parent shows CHANGED 0, NEW 86, so the repair adds no new symbol. None of the four is in `_UPDATE_ALLOWLIST`: a Maintainer-run correction, as the commits say. The two red AST tests in the record are these. |
| 9 | Quality gates at `3ba6f230` | `redundancy`: 0 findings. `neutrality`: fail=81, against 74 at the parent. The difference is seven new hits in `templates/modules/team-gated/api-access-security.md`, `templates/modules/team-gated/web-hosting-security.md` and `templates/skills/_data/vendor_targets.yml`, which come from other sessions' commits between the two (for example the scanner
widening in `1fb06ea6`). None is in a file this repair touched. |

### Call sites, listed from the tree

| Site | Reached by | Mutation ids below |
|---|---|---|
| `bootstrap/_scaffold/install.py:227` the guard in `seed_gitignore` | everything below | A1–A4 |
| `bootstrap/_scaffold/cli.py:457` preflight | install, dry run | B1, B2, B3, B3b |
| `bootstrap/_scaffold/cli.py:486` dry-run listing | install `--dry-run` | C1 |
| `bootstrap/_scaffold/cli.py:687` skills entries | install | C2 |
| `bootstrap/_scaffold/cli.py:698` module entries | install | C3 |
| `bootstrap/_scaffold/install.py:408` in `write_local_env` | install | C4 |
| `bootstrap/_scaffold/install.py:628` in `fan_out_skills`, copy mode | install, `--apply` | C5 |
| `bootstrap/_scaffold/upgrade.py:784` `_seed_staging_gitignore` (called at `:998`) | `--stage` | C6 |
| `bootstrap/_scaffold/upgrade.py:1533` preflight | `--adopt-module` | B4, B5, B5b |
| `bootstrap/_scaffold/upgrade.py:1617` final seed | `--adopt-module` | C7 |
| `bootstrap/_scaffold/upgrade.py:2233` skills seed | `--apply` | C8 |
| `bootstrap/_scaffold/upgrade.py:2481` preflight | `--stage`, `--apply` | B6–B12 |
| `templates/skills/_lib/session.py:894` (byte-identical at `tools/session.py:894`) | `session-start`, copy mode | not routed through `seed_gitignore` — GS-CR1, F1 |

### Entry-point probes (a link to a file outside the tree)

Each row: exit code / did the outside file change / paths created or changed under
the target (files and folders). Unfixed is `9832c411`; repaired is `3ba6f230`.

| Entry point | Unfixed | Repaired |
|---|---|---|
| install | 0 / **yes** / 101 | 2 / no / 0 |
| install `--dry-run` | 0 / no / 0 | 2 / no / 0 |
| install, copy-mode fan-out | 0 / **yes** / 108 | 2 / no / 0 |
| `upgrade --stage` | 0 / **yes** / 18 | 2 / no / 0 |
| `upgrade --apply` | 0 / **yes** / 33 | 2 / no / 0 |
| `upgrade --apply`, copy-mode fan-out | 0 / **yes** / 37 | 2 / no / 0 |
| `upgrade --adopt-module reflections` | 0 / **yes** / 7 | 2 / no / 0 |
| `upgrade --plan` | 0 / no / 0 | 0 / no / 0 |
| `tools/session.py session-start`, copy mode | 1 / **yes** / 7 | 1 / **yes** / 7 |

The last row is GS-CR1. Its exit code 1 comes later, from `git log` in a scratch
repository with no commits. The write has already happened.

### Variants of the `.gitignore` object (repaired engine, `seed_gitignore` called directly)

| Object | Preflight (no entries) | Real seed | Outside file |
|---|---|---|---|
| regular file, or absent | ok | ok | unchanged |
| link to an outside file | refused | refused | unchanged |
| dangling link | refused | refused | unchanged |
| link to a directory | refused | refused | unchanged |
| chain of two links | refused | refused | unchanged |
| relative link to a file inside the tree | refused | refused | unchanged |
| **hard link** to an outside file | ok | ok | **changed** — knowingly out of scope (SEC-3, owed to the model-mapping plan) |
| `.gitignore` is a directory | `IsADirectoryError` | same | unchanged |
| non-UTF-8 file | `UnicodeDecodeError` | same | unchanged |

The last two end in a traceback, as they did before. They now do so before the
install has written anything, because the preflight reads the file.

## Falsification ledger

Method: each row is one deliberate break, applied alone to a fresh worktree of
`3ba6f230`. "Suite" is the 10 test files that import or read the touched code
(353 tests; the control passes 353). "Probe" is the table above, rerun on the
mutant: a leak is the outside file changing. The AGENTS.md rule for equivalence is
applied literally: a break is **equivalent** only if a behaviour test through the
real entry point passes under it *and* breaking the site said to recover the
value fails a test. Where a site is masked by another, a second run breaks both,
to show the first site writes when unmasked.

Unmutated control (G0): 353 passed; the seven probes over a link (install, dry run,
install in copy mode, stage, apply, apply in copy mode, adopt) all exit 2 and write
0 paths; `--plan` exits 0.

| Id | Break | Suite | Probe | Verdict |
|---|---|---|---|---|
| A1 | delete the guard in `seed_gitignore` | 11 failed | six entry points leak | killed |
| A2 | guard skipped on dry runs | 8 failed | install ends in a traceback after 42 paths | killed |
| A3 | guard only when a write will happen | 8 failed | same as A2 | killed |
| A4 | guard moved below the read | 0 failed | identical to control | **equivalent** — the guard still precedes every write; probes identical |
| B1 | delete `main`'s preflight | 3 failed | install: traceback, 42 paths written | killed |
| B2 | `main`'s preflight after the dry-run branch | 1 failed | dry run: traceback | killed |
| B3 | `main`'s preflight after `create_dev_tree` (also for dry runs) | 1 failed | install: 13 folders made, then exit 2 | killed, but only through the dry-run test — see B3b |
| **B3b** | dry runs keep the early check; a real install refuses only after `create_dev_tree` | **0 failed** | install: **13 folders created, then exit 2** | **survived** the whole suite too (2 failed, 3401 passed: the control's two AST failures, nothing else) — GS-CR3 |
| B4 | delete `--adopt-module`'s preflight | 1 failed | adopt: traceback, 7 paths, lockfile rewritten | killed |
| B5 | `--adopt-module` preflight after the spec loop | 1 failed | adopt: exit 2 after 4 paths | killed |
| B5b | `--adopt-module` preflight after the lockfile commit | 1 failed | adopt: exit 2 after 7 paths | killed |
| B6 | delete `cmd_upgrade`'s preflight | 2 failed | stage 18, apply 15, apply (copy) 19 paths written before exit 2 | killed |
| B7 | `cmd_upgrade` preflight for `--stage` only | 1 failed | apply unguarded | killed |
| B8 | `cmd_upgrade` preflight for `--apply` only | 1 failed | stage unguarded | killed |
| B9 | `cmd_upgrade` preflight after the profile self-heal | 1 failed | identical (my fixture already has a profile file, so the self-heal writes nothing; the test builds the missing-config case) | killed |
| B10 | `--stage`'s preflight moved to just before `_write_stage` | 0 failed | identical to control (0 paths) | **equivalent** — `_compute_upgrade` and `_resolve_current_profile` write nothing; probes identical |
| B11 | `cmd_upgrade` preflight widened to `--plan` | 1 failed | plan exits 2 | killed |
| B12 | `cmd_upgrade` preflight below the `--apply` branch | 1 failed | apply: 15 paths before exit 2 | killed |
| C1 | bypass the guard at `cli.py:486` (dry-run listing) | 0 failed | identical to control | **equivalent** — `dry_run=True` cannot write; with B1 as well (C1x) no leak, but the dry run then promises a seed the real run refuses |
| C2 | bypass at `cli.py:687` | 0 failed | identical | **equivalent** — masked by B1 and by C4's earlier guarded seed; C2x: no leak |
| C3 | bypass at `cli.py:698` | 0 failed | identical | **equivalent** — same; C3x: no leak |
| C4 | bypass at `install.py:408` (`write_local_env`) | 0 failed | identical | **equivalent while B1 stands** — B1 fails 3 tests; C4x (both): **leaks** in install (66 paths) and copy-mode install (50) |
| C5 | bypass at `install.py:628` | 0 failed | identical | **equivalent** — masked by B1 and C4's guard; C5x: no leak |
| C6 | bypass at `upgrade.py:784` (`--stage`) | 0 failed | identical | **equivalent while B6 stands** — B6 fails 2 tests; C6x: **leaks** (stage, 18 paths) |
| C7 | bypass at `upgrade.py:1617` | 0 failed | identical | **equivalent while B4 stands** — B4 fails 1 test; C7x: **leaks** (adopt, 7 paths) |
| C8 | bypass at `upgrade.py:2233` | 0 failed | identical | **equivalent while B6 stands** — C8x: **leaks** (apply 33, apply copy-mode 37 paths) |
| F1 | **proposed fix** for GS-CR1 (not a mutant) | 0 failed | session-start copy mode: outside unchanged, 0 paths | the fix closes the route and breaks no owning test |

Reading it: the guard and each of the three preflights are pinned, and the
position of the `--adopt-module` and `--apply` preflights is pinned tightly (a
move of one statement fails a test). The seven call sites C2–C8 each survive the
suite alone, and that is safe today only because a preflight stands in front of
each. The one gap in what the tests pin is B3b.

## Findings

### [GS-CR1] blocking (high) — `session-start` in copy mode appends to a linked `.gitignore`; the defect is not closed

**What.** `_seed_skill_gitignore` (`templates/skills/_lib/session.py:781`; the
self-hosted `tools/session.py:781` is byte-identical) reads `<root>/.gitignore`
and appends to it with no containment check. Its one caller,
`_heal_skills_fanout` (`templates/skills/_lib/session.py:862`), reaches it in copy
mode (`:893` and `:894`), after the copies have already been written. This is a
second writer of the file the repair guards. It does not go through
`seed_gitignore`, so the guard, the three preflights, the new tests and
`SECURITY_MUTATIONS.md` do not see it. Adopters run this code whenever an agent
starts a session.

**It does not need a Windows machine.** Copy mode runs when
`_skill_symlinks_available` (`templates/skills/_lib/session.py:738`) returns False.
It returns False whenever its probe path cannot be unlinked. A non-empty directory
checked in at that path makes both unlink attempts raise `OSError`, which the
function catches and reads as "no symlinks here". A checkout can therefore force
copy mode. It also needs `.agents/skills/` (it has one in any Cairn project) and a
harness folder such as `.claude/` (a checked-in file under it is enough).

**What lands is not fixed text.** The lines come from the `path` field of
`.agents/skills/_data/vendor_targets.yml`, read from the repository
(`templates/skills/_lib/session.py:722`). With the shipped table the line is
`.claude/skills/`. With an edited table it is any text without a leading `/` or a
`..` part, and a folder name may hold newlines.

**Evidence** (all in throwaway trees; nothing real was touched):

1. Installed tree, `.gitignore` linked to an outside file, harness folder present.
   Control, probe path free: the outside file is unchanged and `.claude/skills`
   becomes a link. With a checked-in folder at the probe path: the outside file
   gains `.claude/skills/` and `.claude/skills` is a copy.
2. A committed repository, cloned: `.gitignore` is a link to `.git/config` (git
   cloned it as mode 120000), plus the probe folder, `.claude/keep`, and a table row
   whose path carries a config stanza. The unmodified `tools/session.py
   session-start` appended `zz`, `[core]`, `fsmonitor = touch PWNED-MARKER` and a
   comment line to `.git/config`. `git config --get core.fsmonitor` returned the
   command, and the marker file appeared in the clone, so git ran the command
   during the routine's own later git calls. The payload was a harmless `touch`.

The attacker needs the victim to run `session-start` in the clone. The script is
the shipped, unmodified one, so a reviewer who diffs `session.py` sees nothing: what
changes is a link, a table row and an extra folder. That is the SEC-1 threat model
exactly.

**Why blocking.** The last commit's body opens "Last instance of the defect class".
The class is "a Cairn route appends to a linked `.gitignore`", and this
route is shipped, reachable from a checkout alone, and measured to reach a
command-running file.

**Fix** (variant tested as F1 in the ledger):
1. In `_heal_skills_fanout`, before `_heal_skill_copy` in the copy branch, refuse
   when `root/.gitignore` is a symlink: `raise LifecycleError("refusing to write
   through a symlinked .gitignore: ...")`. `cmd_session_start` already turns that
   into a warning and carries on, so session-start stays fail-soft, and nothing is
   written first. Put the same check in `_seed_skill_gitignore` itself, as the
   repair did for `seed_gitignore`.
2. Edit both copies identically (`templates/skills/_lib/session.py` and
   `tools/session.py`); adopters take it through the normal verbatim upgrade.
3. A test beside `test_copy_fallback_when_symlinks_unavailable`
   (`bootstrap/tests/test_skills_self_heal.py`): link the file, force copy mode,
   assert the outside bytes and the target tree are unchanged. Also one test with
   the probe folder and no monkeypatch, since that is the route a checkout uses.
   I drafted both in a scratch copy: they fail on `3ba6f230` (2 failed) and pass
   with the F1 edit (13 passed, the 11 existing self-heal tests included).
4. A test that fails when any shipped Python file writes a path named
   `.gitignore` outside `seed_gitignore` and this helper. That is what would have
   shown the second writer; nothing in the suite can see a new one today.
5. Say in `SECURITY_MUTATIONS.md` that the session helper is outside its scope and
   where its writes are inventoried.
6. Because this is a new containment decision in a shipped executable file, I
   would route the fix through an Internal Security Review. That is the
   Maintainer's call.

### [GS-CR2] non-blocking (low, process) — the Boundary B record is not in the commit bodies

The four bodies record scoped runs: `b8a402c6` "298 passed, 2 failed", `fde3054c`
"12 passed" (the new class only), `8335e9f4` "446 passed, 2 failed", `3ba6f230`
"449 passed, 2 failed" (each headed "Scoped ... set"). None carries a
`Boundary B mode` line, none says full, and "3401" occurs in no commit message and
not in the intent log (searched with `git log --grep` and `grep`). The scaffold
engine is a named high-risk surface, so bounded mode is refused and a full-mode
record was required in the body of the last implementation commit.

The figure the brief quotes (full mode, 3401 passed, 2 failed, Python 3.13.13)
does reproduce: row 2 above. So the evidence is sound; it just does not live where
the next reader will look for it. Under Boundary C a missing record would have
meant a fresh full run, which is why I ran one.

**Fix.** Carry the full-mode record (mode, interpreter, counts, the two expected
failures) into the body of the next commit that touches this area, for instance
the AST re-anchor commit, or into a Response to this review.

### [GS-CR3] non-blocking (low) — nothing pins "refuse before the install's first write" except the absence of one file

B3b: with the early check kept for dry runs and the real install's check moved to
just after `create_dev_tree`, the install leaves 13 empty folders in the target
before it refuses. The 353 owning tests all pass, and so does the whole suite (2 failed, 3401 passed,
the control's two AST failures). The two install tests
assert only that `AGENTS.md` does not exist
(`bootstrap/tests/test_intents_tool.py`, `test_install_through_a_link_to_an_outside_file_exits_2`
and `test_install_through_a_link_to_a_file_inside_the_target_exits_2`). The
claim "nothing written" holds today (probe: 0 paths), so this is a gap in the
pin, not in the code.

**Fix.** In those two tests, list the target before and after (files and folders)
and assert the lists are equal. The stage, apply and adopt tests already compare
the lockfile and the stage folder, so they need nothing.

### [GS-CR4] non-blocking (low) — `SECURITY_MUTATIONS.md` line 12 is false

"Both raise the single `ScaffoldSecurityError` identity, caught once at the CLI top
level (exit 2)." Measured at `3ba6f230`: an install over a dangling `AGENTS.md`
link exits 1 with a traceback naming `ScaffoldSecurityError`. The only containment
refusals that exit 2 with a plain line are the three `.gitignore` preflights
(`main`, `--adopt-module`, `--stage`/`--apply`). The repair chose that, because (per the
commit body of `fde3054c`) the differential oracle pins the traceback, and it edited four rows of this file, but
not the sentence.

**Fix.** Say what is true: the error is raised by the guard; a command turns it into
exit 2 only where it asks first (the `.gitignore` preflights, the fan-out and
onboarding calls, `--apply` and `--stage` around their own writes); elsewhere it
propagates as a traceback with exit 1, which the oracle pins.

### [GS-CR5] non-blocking (low) — the gate-manifest row does not know about this repair

Two frozen files changed: `bootstrap/tests/test_security_leaf.py` and
`bootstrap/tests/test_skills_upgrade.py` (the manifest still holds their
pre-repair blob ids, `726781fa` and `29087bd2`). The pinned collection also lacks
11 new nodes: 8 in `TestGitignoreSeedingRefusesLinks` and 3 in
`test_skills_upgrade.py`. The four commit bodies name only the AST re-anchor. A
changed frozen file does not redden the suite, so nothing will say this before the
ceremony. Same pattern as EA3 in the 2026-10-17 review.

**Fix.** Name the two files and the 11 node ids in the board row at its next
serialization point, or in the AST re-anchor commit's body. I did not edit the
board.

### [GS-CR6] non-blocking (low) — the refusal names no remedy, and it also refuses when nothing would be written

The line is `error: .gitignore seed refused (containment): refusing to write
through a symlinked destination: <path>`. Replacing the link with a real file is
the remedy, and it is stated only in a test docstring. It is printed from three
places (`bootstrap/_scaffold/cli.py:459`, `bootstrap/_scaffold/upgrade.py:1535`,
`bootstrap/_scaffold/upgrade.py:2483`).

A behaviour change worth a sentence: with a link to an in-tree file that already
lists every entry, the unfixed `seed_gitignore` returned `[]` and wrote nothing;
the repaired one refuses. An adopter who keeps a shared `.gitignore` by link can no
longer install, stage, apply or adopt, where before the install was a no-op for
that file. The tests pin this on purpose, and it follows from "a link is refused
wherever it points", so I do not ask for a change of rule. `bootstrap/UPGRADE.md`
and `bootstrap/SAFETY.md` do not mention it.

**Fix.** Add the remedy to the message (change all three places together) and one
sentence to `bootstrap/UPGRADE.md`.

## Seen, not raised

* **Hard links (SEC-3)** pass the guard and the outside file changes (variants
  table). Knowingly out of scope; owed to the model-mapping plan.
* **Time of check to time of use.** A link planted between the preflight and the
  seed would defeat it. That needs another process running as the same user inside
  the tree, outside the threat the repair addresses.
* **Class C writers** in `SECURITY_MUTATIONS.md` (`cmd_update_profile`,
  `cmd_init_lock` and others) write fixed paths without the guard. They do not
  touch `.gitignore`, are listed as owned follow-up work, and are not this repair's.
* **`_apply_upgrade` swallows a copy-mode refusal.** `fan_out_skills` is wrapped in
  `except Exception` and warns (`bootstrap/_scaffold/upgrade.py:2230`); the later
  skills seed would raise. Unreachable while the `--apply` preflight stands (C5, C8).
* **The refusal exits 2 where its neighbours exit 1.** A deliberate result of the
  oracle pin (commit `fde3054c`); noted in GS-CR4.
* **The neutrality gate is red at this commit** (81 hits) for reasons outside this
  repair (row 9 above).
* **`session-start` exits 1** in my scratch repositories because they have no commits.
  That is after the write and unrelated to it.

## What I did not cover

* Windows: reparse points, junctions, `core.symlinks=false` checkouts. All my runs
  were on macOS.
* A case-insensitive alias of `.gitignore` (for example `.Gitignore` on a
  case-insensitive disk). `is_symlink` resolves the name the OS resolves, but I did
  not test it.
* A real shell startup file as the link target. I used a stand-in file; the
  `.git/config` chain in GS-CR1 ran only in a throwaway clone and only with a
  harmless payload.
* `bootstrap/security_check.py` (the release ceremony) and a separate Bandit run.
  The full suite's `test_security_lint` (Bandit over the engine) passed with no skip
  reported; I ran no other static check.
* The seven mutants named in the body of `3ba6f230`: I reran six of those shapes
  (B6, B7, B8, B9, B11, B12) and not the seventh (the stage-only check placed
  after the stage write).
* The `scripts/` self-hosted copies, harnesses other than the Claude one in the fan-out
  table, and the other sessions' commits interleaved with these four.

**Disposition**: revise. GS-CR1 is the only thing between this repair and "the
defect is closed"; its fix is a few lines in one file, tested in a scratch copy.
GS-CR2 to GS-CR6 can ride that follow-up. The four commits themselves need no
change.
