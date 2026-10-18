# Security Review — the `.gitignore` seed guard (`b8a402c6..3ba6f230`) — Claude Opus 5.5 — 2026-10-18

**Obligation**: the Security Review that clears SEC-1, raised by the
model-mapping proposal's Security Review (`3c133398`, in
`dev/proposals/2026-10-18-claude-model-mapping-install-path.md`).
**Reviewed commits**: `b8a402c6`, `fde3054c`, `8335e9f4`, `3ba6f230`; the
engine read as it stands at `3ba6f230`. The "before" engine is their parent,
`9832c411`.
**Distance**: a fresh session, not the implementing one. The implementing
commits credit a different model size of the same agent type, so the distance
is a fresh context, not a different type. A separate code reviewer is doing the
ordinary falsification in parallel; this pass is security only.
**Interpreter**: Python 3.13.13 at `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
`PYTHONDONTWRITEBYTECODE=1`. Platform darwin, APFS (case-insensitive), git 2.53.0.
**Where things ran**: three detached worktrees under the session scratchpad,
each in a fresh empty folder: `3ba6f230` (probes), `9832c411` (the "before"
engine) and a second `3ba6f230` copy for mutations, removed when done. Every
target tree was a throwaway folder. The only writes to the shared tree are the
intent claim and this record.

**Verdict**: **SEC-1 CLEARED** — 0 blocking findings, 6 findings in all
(1 high that belongs to a different program, 3 low, 2 informational).

## In brief

**The hole SEC-1 named is closed in the installer.** I ran every way the
installer can be started (a normal install, a dry run, a re-install with
`--force`, all three presets, adding a module, staging and applying an
upgrade, and the commands that do not touch `.gitignore`) over a project
whose `.gitignore` is a link to a file outside it. Before the repair, 12 of
those 20 runs wrote outside the project. After it, none did: every run that
would have written stopped with a plain message and exit code 2 before writing
anything, and the outside file was left byte for byte as it was. Links that
point inside the project, chains of links, broken links, links to a folder, and
an upper-case `.GITIGNORE` are all refused the same way.

**The second check, at the moment of writing, holds at every place the
installer writes `.gitignore`.** I swapped a link in after the early check had
passed, just before each of the seven places in the code that write it. Every
one refused, and nothing outside changed. What remains is the tiny gap inside
the writing function itself, about a tenth of a millisecond. A program racing it from the
same machine can win it; I measured that, and it is the risk Cairn already
accepts in `bootstrap/SAFETY.md` (GS-SR-3).

**The repair changed nothing else that refuses.** The pre-repair and
post-repair engines give the same exit code and message on eight other planted
links. The only difference shows up when a project has two traps at once: the
`.gitignore` one is now reported first.

**But the same hole is open in a second program Cairn ships** (GS-SR-1, high).
The session-start helper, `tools/session.py`, which every adoption gets and
every agent runs at the start of a session, appends to `.gitignore` with no
check at all. A project can steer it onto that path with one committed folder.
I reproduced it end to end through `git clone`. With one extra line of
project data, the appended text becomes a command that runs the next time a
shell reads the outside file. SEC-1 named the installer, and the installer is
fixed, so this does not hold up clearing SEC-1. But "no Cairn program writes
through a linked `.gitignore`" is not yet true, and it needs its own repair
and its own Security Review.

**The code fingerprint changed on exactly the four functions named**: `main`,
`seed_gitignore`, `_cmd_adopt_module` and `cmd_upgrade`. Nothing else in
`bootstrap/_scaffold/` changed.

## Findings at a glance

| id | what | severity | blocks SEC-1? |
|---|---|---|---|
| GS-SR-1 | `tools/session.py` appends to a linked `.gitignore`; a project can force that path and choose the appended text | **high** | no — different program; owed its own repair |
| GS-SR-2 | `create_dev_tree` makes folders through a linked `dev/`, outside the project, before any guard refuses | low | no — pre-existing, unchanged |
| GS-SR-3 | the gap inside `seed_gitignore` between its check and its write: a won race overwrites the outside file | low (accepted residual) | no |
| GS-SR-4 | a hard-linked `.gitignore` is still written through, as before (SEC-3 class) | low | no |
| GS-SR-5 | the early check reads the file, so a non-UTF-8 or folder `.gitignore` now blocks `--apply` with a traceback | informational | no |
| GS-SR-6 | the refusal line prints the project path unencoded; the link's own text never reaches the terminal | informational | no |

## Q1 — Is SEC-1 closed?

**Yes, for the installer.** Probe A ran each entry point as a real
subprocess, against the "before" engine and the reviewed engine, with
`.gitignore` a link to a stand-in startup file outside the project.

| case | before (`9832c411`) | after (`3ba6f230`) |
|---|---|---|
| A1 install, absolute link | exit 0, **outside appended** | exit 2, nothing written |
| A2 install `--dry-run` | exit 0, nothing written | exit 2 |
| A3 re-install `--force` | exit 0, **outside appended** | exit 2, nothing written |
| A4 relative link `../elsewhere/startup-file` | exit 0, **outside appended** | exit 2 |
| A5 chain: `.gitignore` → a link inside the throwaway project → outside | exit 0, **outside appended** | exit 2 |
| A6 broken link to a path that does not exist yet | exit 0, **outside file created** | exit 2, not created |
| A7 link to an outside folder | exit 1, traceback, `AGENTS.md` already written | exit 2, nothing written |
| A8 `.GITIGNORE` link (case-insensitive volume) | exit 0, **outside appended** | exit 2 |
| A9 presets `solo-greenfield`, `collaborative-team`, `high-rigor-legacy` | exit 0, **outside appended** (all 3) | exit 2 (all 3) |
| A10 `upgrade --adopt-module` `coordination-tiers` / `reflections` / `architecture-review` | exit 0; **outside appended** for the two with ignore entries; lockfile rewritten | exit 2; lockfile byte-identical |
| A11 `upgrade --stage` | exit 0, **outside appended**, stage written | exit 2, no stage folder |
| A12 `upgrade --apply` (link planted after `--stage`) | exit 0 | exit 2 |
| A13 `upgrade --plan` | exit 0 | exit 0 (writes nothing, not asked) |
| A14 `upgrade --finalize --force` | exit 0 | exit 0 |
| A15 `upgrade --init-lock` | exit 2, its own template refusal | same |
| A16 `upgrade --adopt-collisions` (bogus triple) | exit 1, its own refusal | same |

Totals: before, 12 of 20 runs wrote outside the project (11 appended to the
stand-in, A6 created a new file). After, 0 of 20. A13–A16 do not seed
`.gitignore` at all; the tree confirms it: the only `.gitignore` writer in the
engine is `seed_gitignore` (`bootstrap/_scaffold/install.py:237`), and its
callers are the seven sites listed under Q2, none in `--plan`, `--finalize`,
`--init-lock` or `--adopt-collisions`.

**Linked parent folder.** The only folder between the project root and
`.gitignore` is the root itself. Every entry point resolves `--target` before
use, so a root reached through a link is the real root, which is where the
operator pointed. `_assert_safe_write`'s ancestor walk has nothing to check for
this path, and its third check can never fire here (see Q2).

**Profile and module choice** change only which lines are appended, never the
path. The copy-fallback fan-out appends a path from Cairn's own vendor table
(`load_vendor_targets(templates_root)`), not the project's. Its seed goes
through the same guard (probe B1).

**The same hole outside the installer:** GS-SR-1.

**Mutation ledger** (separate worktree, one break at a time, against the 16
tests that own the change and the probe-A matrix; control: 16 passed, 0 of 20
wrote outside):

| mutant | tests | matrix: wrote outside | matrix: refusals not exit 2 |
|---|---|---|---|
| M1 guard in `seed_gitignore` deleted | **killed** (11 failed) | **11 of 20** | 16 |
| M2 guard skipped on dry runs | **killed** (8 failed) | 0 | 15 |
| M3 `main`'s early check deleted | **killed** (3 failed) | 0 | 11 (install cases) |
| M4 `--adopt-module`'s early check deleted | **killed** (1 failed) | 0 | 3 (A10) |
| M5 `--stage`/`--apply` early check deleted | **killed** (2 failed) | 0 | 1 (A12) |

So the security property (nothing written outside) rests on the one guard
inside `seed_gitignore`, and the tests pin it. The three early checks (in
`main`, `_cmd_adopt_module` and `cmd_upgrade`) add the clean exit 2 and the
"nothing half-done" property, and the tests pin each one.

## Q2 — The gap between check and write

**What `_assert_safe_write` does at write time.** It is the same function the
early checks call, run again inside `seed_gitignore` immediately before the
read and the write. It makes three checks: the file itself is not a symbolic
link (`is_symlink`, which does not follow the link); no folder strictly between
the root and the file is a link; and the resolved folder plus the file name is
inside the root. For `.gitignore` only the first can fire: there is no folder
in between, and the resolved folder *is* the root. It does not look at
hard-link counts (GS-SR-4), and it does not keep the file open; the write
reopens the file by name.

**A link swapped in after the early check (probe B1).** The engine calls
`seed_gitignore` to write from seven lines, listed from the tree rather than
the diff: `cli.py:687` and `:698`, `install.py:408` and `:628`, and
`upgrade.py:784`, `:1617` and `:2233`. For each one, a wrapper swapped
`.gitignore` for a link immediately before that call (`install.py:628` was
reached twice, from install and from `--apply`):

| write site | before | after: outcome | after: outside |
|---|---|---|---|
| `write_local_env` (install) | **outside written** | `ScaffoldSecurityError` escapes `main` (traceback, exit 1); files installed, no lockfile | unchanged |
| `main`, skills entries (install) | **outside written** | same | unchanged |
| `main`, module entries (install) | **outside written** | same | unchanged |
| `fan_out_skills`, copy mode (install) | **outside written** | exit 2 "skills fan-out refused" | unchanged |
| `_seed_staging_gitignore` (`--stage`) | **outside written** | exit 2 "upgrade --stage refused"; stage left | unchanged |
| `_cmd_adopt_module` | **outside written** | traceback, exit 1; lockfile already records the module | unchanged |
| `_apply_upgrade`, symlink fan-out (`--apply`) | **outside written** | exit 2 "upgrade --apply refused"; skills applied, lockfile advanced | unchanged |
| `fan_out_skills` inside `--apply`, copy mode | **outside written** | exit 2 (the fan-out's own refusal is caught and warned; the next seed refuses) | unchanged |

Every site fails closed. What a link planted mid-run leaves behind *inside* the
project is a half-finished run: the half-done state the early checks exist to
avoid. That needs someone changing files on the machine during the run, which
is outside the threat model `bootstrap/SAFETY.md` states.

**The gap inside `seed_gitignore` (probe B2).** Measured on `3ba6f230`:

* The span from the end of the guard to the write: median 94.4 µs, 99th
  percentile 633.3 µs (2,000 calls).
* A racing thread flipping `.gitignore` between a file and a link, 3,000
  calls: the guard refused 2,553; **99 calls' lines reached the outside file.**
* What a win does: the write is a truncate-and-rewrite of what was read. A
  forced win (the swap made on the read) left the outside file holding
  `*.log\ndev/.cairn/handoff.lock\n`: **its own content was destroyed**, not
  appended to. The reverse win (the read follows a link, the write does not)
  copied the outside file's bytes into the project's own `.gitignore`.
* The same race against a variant that opens both the read and the write with
  `O_NOFOLLOW`: **0 of 3,000** reached the outside file (185 opens refused by
  the OS instead).

This is GS-SR-3.

## Q3 — Terminal control sequences in the refusal message

Probe C, the real CLI as a subprocess, raw bytes captured:

| case | ESC / BEL / CR in output? |
|---|---|
| C1 the link's *target* text carries `ESC ] 0 ; … BEL ESC [2K CR …` | **no**, on stdout and stderr |
| C3 the same link, through `--adopt-module` and `--stage` | **no** |
| C2 the project *folder name* carries the same sequence: the refusal line | **yes** |
| C2 the same folder, a normal `.gitignore`, an ordinary `--dry-run` | **yes**: `[dry-run] Would install to:` already prints it raw |

The message names only `<target>/.gitignore`. Whatever the link points at
never reaches it, because the third check, the only one that names a resolved
path, cannot fire for this file. The folder name is the operator's own
`--target`, and the engine already prints it raw on its ordinary path
(`bootstrap/_scaffold/cli.py:464`, `:492`). So the new line opens no new route.
The engine has no terminal encoder; `encode_display` lives in the shipped
session kernel (`tools/session.py:169`). The message does not need encoding for
this repair (GS-SR-6).

## Q4 — Did narrowing the fix change any other refusal?

**The differential oracle across the whole range.** I ran
`bootstrap/tests/_oracle.py run --baseline-ref 9832c411 --trusted-ref 3ba6f230`
from the reviewed worktree: 3 fresh-install fixtures (84, 110, 116 files) and
3 privileged workflows (upgrade stage + apply, the containment refusal, the
dirty-tree refusal) all **MATCH**. The containment refusal is exit 1 with
`ScaffoldSecurityError: refusing to write through a symlinked destination:
<path>` on both engines.

**What the suite's oracle tests can and cannot show.** They use
`baseline_ref="HEAD"`. Run on an uncommitted change, as Boundary B prescribes, that
compares the change against its parent, which is a real differential, one step
at a time. Run on a committed tree it compares a commit with itself. The run
above is the one that spans all four commits.

**Scope.** The oracle pins one containment refusal (a linked `AGENTS.md` at
install). Probe D covered eight, before and after, each with a normal
`.gitignore` and again with `.gitignore` also linked:

| other refusal | normal `.gitignore`: before = after? | `.gitignore` also linked: after |
|---|---|---|
| install, `AGENTS.md` a link | identical (exit 1, traceback) | exit 2, `.gitignore` line |
| install, `dev/` a link | identical (exit 1) — see GS-SR-2 | exit 2 |
| install, `dev/.cairn` a link | identical (exit 1) | exit 2 (before: exit 1 **and the outside file appended first**) |
| install, `.claude/` a link | identical (exit 2, fan-out refusal) | exit 2 (before: **outside appended first**) |
| install, `tools/` a link | identical (exit 1) | exit 2 |
| `--stage`, `dev/.cairn-upgrade` a link | identical (exit 2) | exit 2 |
| `--adopt-module`, a module file a link | identical (exit 1) | exit 2 |
| `--apply --force`, a staged file a link | identical (exit 2) | exit 2 |

With a normal `.gitignore`, all eight are identical: same exit code, same
final line or error block, same folders created outside. With two traps the
`.gitignore` refusal is now reported first. That is the intended order (it
runs before the first write) and never hides a write. The commits' "every
other refusal keeps its current output and exit code" holds for a project with
one trap.

Five of the eight still end in a traceback with exit 1. The opening of
`bootstrap/_scaffold/SECURITY_MUTATIONS.md:12` ("caught once at the CLI top
level (exit 2)") is therefore still false; SEC-4 already assigns that
correction to the model-mapping plan, and this repair rightly did not take it.

## Q5 — Hard links (SEC-3)

Probe E, `.gitignore` hard-linked to an outside file on the same volume:

| case | before | after |
|---|---|---|
| install | exit 0, **outside appended** | identical |
| install `--dry-run` | nothing written | identical |
| `upgrade --stage` | exit 0, **outside appended** | identical |
| `upgrade --adopt-module reflections` | exit 0, **outside appended** | identical |

The repair does not make hard links worse: the early checks only read, and the
write is the same in-place rewrite as before. Today a hard-linked `.gitignore`
is written through on every seeding path. Git cannot carry a hard link, so
this needs someone already on the machine (GS-SR-4).

## Q6 — The AST CHANGED set

Runbook Step 1, derived against the committed baseline, not carried forward:

* `9832c411`: CHANGED 0, MISSING 0, DUPLICATE 0, NEW 86;
  `_ast_attest.py verify … --known-new …` exit 0, 173 baselined symbols
  accounted for.
* `3ba6f230`: **CHANGED 4**, MISSING 0, DUPLICATE 0, NEW 86. `verify
  --known-new` reports exactly these four and no rekeyed known-new symbol:
  * `FunctionDef:main` (`cli.py`) `5c197afe8ee049d4` → `6d93025d3b610dc3`, from `b8a402c6`, then `fde3054c`
  * `FunctionDef:seed_gitignore` (`install.py`) `55a95c62ab693619` → `12ca0b5cd49ed2d7`, from `b8a402c6`
  * `FunctionDef:_cmd_adopt_module` (`upgrade.py`) `92290a6b95389cc2` → `4679fad04dde6386`, from `8335e9f4`
  * `FunctionDef:cmd_upgrade` (`upgrade.py`) `d98eff085ea46b43` → `69badaf010d60a77`, from `3ba6f230`
* A per-symbol digest comparison of all 259 symbols between the two worktrees:
  the four above differ, and nothing else. The NEW set is the same 86 keys with
  the same digests.
* Files: `git diff 9832c411 3ba6f230 -- bootstrap/_scaffold/` touches only
  `cli.py`, `install.py`, `upgrade.py` and `SECURITY_MUTATIONS.md`. No
  `bootstrap/_scaffold/` commit has landed since `3ba6f230` (checked to
  `e9ea8c61`).
* None of the four is in `_UPDATE_ALLOWLIST`, so this is the Maintainer's
  direct correction, as the commits say. If GS-SR-5's optional change is
  taken, it moves `seed_gitignore` again; land it before the re-anchor so the
  baseline moves once.
* Bandit over `bootstrap/_scaffold/`: 22 low-severity results before and after,
  the same four test ids; nothing new.

## Findings

### GS-SR-1 — high, not blocking SEC-1: the session kernel appends to a linked `.gitignore`, and a project can steer it there and choose the text

**Plain:** the session-start helper that every adoption gets, and that agents
run at the start of every session, has the same defect SEC-1 found in the
installer, with no guard at all. A project can push it onto the code path
that writes, and can choose what it writes.

* `_seed_skill_gitignore` (`tools/session.py:781`) reads and rewrites
  `<root>/.gitignore` with `write_text` (`:797`), following any link. It runs
  from `_heal_skills_fanout` (`:894`), which `session-start` calls first
  (`:924`), whenever the copy fallback is chosen.
* The copy fallback is chosen when the symlink probe fails. The probe deletes
  and recreates a fixed name, `.cairn-skill-symlink-probe` (`:741`). A
  committed *folder* at that name makes the delete fail, and the probe then
  reports "no symlinks" on any operating system.
* The appended entry is the vendor row's `path` plus `/`. Rows come from the
  project's own copy of `.agents/skills/_data/vendor_targets.yml` (`:225`,
  read at `:722`). The only checks are no leading `/` and no `..` part; the
  parent folder must exist, which a project supplies.
* **Exercised.** A clean install by the reviewed engine; `tools/session.py`
  byte-identical to Cairn's shipped `templates/skills/_lib/session.py`. Then
  data only: `.gitignore` linked to a stand-in startup file, the probe folder,
  and `.claude/`. `session-start` exited 0 and appended `.claude/skills/` to
  the stand-in (F1). Adding one row whose path is `$(touch GSR_MARKER_RAN)/skills`
  (and that folder) appended `$(touch GSR_MARKER_RAN)/skills/`; `/bin/sh`
  sourcing the stand-in from a scratch folder **created `GSR_MARKER_RAN`** (F2).
* **Through git.** I committed that data (the link, the probe folder, the
  crafted folder and row) to a scratch repository, cloned it with git 2.53.0,
  and ran `session-start` in the clone: the stand-in gained both lines. Git
  carried all of it. The clone was silent; `git status` in the clone printed
  one warning, that it could not read `.gitignore`.
* **Why it is not just "running a hostile repo's code".** The code here is
  Cairn's, unchanged. The hostile part is data a reviewer reads as harmless: a
  link, a folder, a table row. A pull request that touches no script is enough
  for whoever checks it out and starts a session.
* **Why it does not block SEC-1.** SEC-1 named the installer; its closing
  condition is met. This is a sibling in another program, untouched and not
  worsened by this repair.

**Recommended fix** (its own change; `tools/session.py` is a named high-risk
surface, kept byte-identical with `templates/skills/_lib/session.py`, so the
change takes a Security Review):
1. **Required:** refuse a linked `.gitignore` in `_seed_skill_gitignore` before
   the read, using the kernel's own containment error. The self-heal already
   turns that error into a warning and carries on.
2. **Recommended:** validate a vendor row's `path` against a conservative
   character set before it is used as a path or written as an ignore line.
3. **Recommended:** make the symlink probe a name the project cannot occupy
   (create a fresh unique name), or treat "probe name occupied" as "cannot
   tell" rather than "no symlinks".

### GS-SR-2 — low, pre-existing, not SEC-1: `create_dev_tree` makes folders through a linked `dev/`

**Plain:** if a project's `dev/` folder is a link to somewhere else, the
install creates its empty `dev/` subfolders over there before a later check
stops it.

* `create_dev_tree` (`bootstrap/_scaffold/install.py:188`) calls `mkdir` with
  `parents=True` (`:198`) without a guard. Probe D, `dev/` linked to an
  outside folder: before and after alike, 12 folders created there (`plans`,
  `proposals`, `.cairn`, `modules/onboarding`, …), 0 files; then the first
  guarded write refuses (exit 1, traceback).
* Empty folders with fixed names only, so low. But it is a write into the
  adopter tree that the inventory in `SECURITY_MUTATIONS.md` does not list.
  The new early check stops it only when `.gitignore` is also linked.

**Recommended fix:** guard each folder with `_assert_safe_write(d, target)`
before `mkdir` (an engine change with its own AST symbol), or list
`create_dev_tree` in the inventory's Class C and hand it to the RR6/SR6
follow-on that `fork-advisory-semantics` owns.

### GS-SR-3 — low (accepted residual, measured): the gap inside `seed_gitignore`

**Plain:** between the check and the write there is about a tenth of a
millisecond. A program racing it on the same machine can win, and when it
wins, the outside file is overwritten, not just added to.

* Evidence in Q2: 99 of 3,000 calls lost to a racing thread; a won race
  replaced the outside file's content; a reverse win copied the outside file
  into the project's `.gitignore`; `O_NOFOLLOW` on both opens brought losses to
  0 of 3,000.
* `bootstrap/SAFETY.md:243` accepts "a small TOCTOU window" with no concurrent
  attacker on the filesystem. This is that window. The repair did not create
  it; before the repair, there was no check to race.

**Recommended:** none required for SEC-1. When the model-mapping plan builds
CL-1's write helper (exclusive-create a temp file, then `os.replace`), route
`seed_gitignore`'s write through it and read with `O_NOFOLLOW`. That closes
this race and GS-SR-4 together. Separately, the SAFETY.md residual could say
what a won race does (overwrite), since "small" alone undersells it.

### GS-SR-4 — low (SEC-3 class, unchanged): a hard-linked `.gitignore` is still written through

**Plain:** a hard link is a second name for the same file. The check cannot
see it, so the seed still lands in the shared file, as it did before.

* Evidence in Q5: identical before and after on install, `--stage` and
  `--adopt-module`; a dry run writes nothing.
* Git cannot carry a hard link, so this needs someone already on the machine.

**Recommended:** the same CL-1 helper (a replace never writes into the old
file), or refuse a `.gitignore` whose link count is above 1. If the plan's
helper is not extended to `seed_gitignore`, name this as a residual there.

### GS-SR-5 — informational (robustness, not security): the early check reads the file

**Plain:** the early check runs the whole seeding function with nothing to
add, so it also reads the file. A `.gitignore` that is not UTF-8, or a folder
named `.gitignore` (git can carry `.gitignore/x`), now stops install,
`--stage` *and* `--apply` with a traceback (exit 1) before anything is written.

* Probe G. Before: install and `--stage` failed the same way but *after*
  writing (a half install; a stage left behind), and `--apply` then succeeded
  from that stage. After: nothing is written, and `--apply` is blocked even
  when it would add no ignore line.
* Fail-earlier is the safer behaviour, and no outside write is involved. The
  commits do not mention it.

**Optional:** in `seed_gitignore`, return right after the guard when there are
no entries. The early checks need only the guard. If taken, land it before
the re-anchor (Q6).

### GS-SR-6 — informational: the refusal line prints the project path unencoded

Evidence in Q3. The link's own text never reaches the terminal. The folder
name does, exactly as it already does on the ordinary path. No action is needed
for this repair. If the engine ever encodes terminal output, it should do it
for every printed path at once. Importing the session kernel's encoder into the
engine would be a new dependency, so that is a separate change.

## The inventory row, checked against measurement

The new `seed_gitignore` row in `bootstrap/_scaffold/SECURITY_MUTATIONS.md`
holds as written. The guard runs before the read and on dry runs (M2). A link
is refused wherever it points (A5, the in-tree tests). Install, dry run,
adoption, stage and apply stop with exit 2 and nothing written (A1, A2, A10,
A11, A12, B1). `--plan` is not asked (A13). Moving the row out of Class B
corrected the false "contained by construction" claim SEC-1 flagged.

## What I did not cover

* **Other operating systems.** Only macOS (APFS, case-insensitive) was
  measured. Windows (junctions, `core.symlinks=false`, the symlink privilege)
  and Linux were not run.
* **The full suite and ordinary falsification.** These belong to the parallel
  code review. I ran the 16 tests that own the change, plus my probes.
* **A complete same-class sweep of the engine.** GS-SR-2 turned up in passing.
  I did not inventory every other `mkdir` or write in the engine, including the
  Class C commands.
* **GS-SR-1's fix.** The three recommendations are untested sketches. I did
  not check whether `verify_integrity` would flag the edited vendor table (it
  is lockfile-tracked; `session-start` does not consult it).
* **No real shell startup file was touched.** Execution was shown by `/bin/sh`
  sourcing a stand-in from a scratch folder.
* **Bandit:** compared result counts and ids only, not each result.
