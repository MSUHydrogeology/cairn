# Security Review — upgrade lockfile paths (`d299f37c..2f07f2e7`) — Claude Opus 5.5 — 2026-10-19

**Obligation**: the Security Review of the repair for the out-of-scope finding
raised in the Security Review of
`dev/proposals/2026-10-19-claude-remove-collaboration-agreement.md`: `upgrade`
read upstream text from a path taken from the lockfile's `src` with no
containment check. The repair changes the scaffold engine
(`bootstrap/_scaffold/`), a high-risk surface in `AGENTS.md`. It has no
proposal or plan.
**Reviewed commits**: `d299f37c` (red tests), `6c436a9f` (the fix, in
`bootstrap/_scaffold/upgrade.py` and `bootstrap/_scaffold/SECURITY_MUTATIONS.md`),
`2f07f2e7` (two tests that kill mutation survivors). Test file:
`bootstrap/tests/test_upgrade_lockfile_path_containment.py`. The "before"
engine is `90715acb`, the parent of `d299f37c`.
**Distance**: a fresh session, not the implementing one. The commits credit a
different model size of the same agent type, so the distance is a fresh
context, not a different type. Security pass only.
**Single pass**: by the Maintainer's instruction, relayed by the coordinator,
there is no second Security Review round. Each finding below therefore carries
the exact fix and the test that shows it closed; the code review checks the
answer against them.
**Interpreter**: Python 3.13.13 at `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
`PYTHONDONTWRITEBYTECODE=1`, scripts run with `-I`. Darwin, APFS
(case-insensitive: a `DOCS/LINKDIR` name resolved through a `docs/linkdir`
link), git 2.53.0.
**Where things ran**: detached worktrees of `2f07f2e7` and of `90715acb`, a
`git archive` extraction of `2f07f2e7` for one experiment, and probe projects,
all in one uniquely named folder under the session scratchpad. Every "outside"
file was a marker file in that folder. All removed when done. The only writes
to the shared tree are the intent claim and this record. No full suite was run.

**Verdict**: **CLEARED.** The hole is closed. 8 findings: 1 high, 1 medium,
4 low, 2 informational. None of them is in the repaired code path; the high
one is an older, separate hole in the same command (see *Clearing*).

## In brief

**The hole is closed.** On the old engine I reproduced it through the real
command line: a lockfile record whose `src` climbs out of Cairn's `templates/`
folder made `--plan`, `--stage` and `--apply` all exit 0, and the outside
file's text ended up in a tracked project file. On the repaired engine I tried
31 shapes of bad `src`, `dst` and `base_cache` against all five actions, 155
runs: `..`, absolute names, `//`, `./`, `~`, `file://`, `x:` prefixes,
backslashes, links to files and folders, a dangling link, a link inside
Cairn's own `templates/`, case tricks through a link, and nine look-alike or
encoded separators and dots. Every real escape was refused with exit 2, the
record number, the escaped name and a remedy, and nothing was written. The
look-alikes are just odd characters in a file name, not separators, so they
name a template that does not exist: nothing was read, and the marker
appeared nowhere. The review area check refuses a planted link, and the AST
change set is exactly what the commit says.

**But the same command has an older hole that is worse.** If a repository
carries `dev/.cairn/profile.yml` as a link to a file that does not exist yet,
`upgrade --apply` creates that file outside the project, and the lockfile
chooses some of its lines. I delivered the link through `git clone` and it
worked with one command and no staged upgrade (LP-SR-1). The old engine does
the same, so the repair did not cause it, but it is the most serious thing I
found.

**Three smaller routes of the same kind.** A lockfile that is itself a link
gets written back through the link (LP-SR-2). The lockfile's `cairn_commit` is
handed to git as an option, and `--plan` created a file outside (LP-SR-3).
Module names, and names in a staged upgrade the repository carries, still
reach the terminal raw (LP-SR-4), the same kind of fault the repair fixed for
`dst`.

**On the questions you asked.** The advisory-before-check order costs a
yes/no glimpse outside the project. That is acceptable, but the new inventory
text overstates it, and it can be avoided without touching the frozen test: I
measured that (LP-SR-5). The legitimate adopter whose folder is a link now
gets refused at `--plan`. That is the right result, but the remedy wrongly
tells them to restore the lockfile (LP-SR-6).

## Clearing

* **The obligation is cleared as committed.** The repair does what it claims,
  and no finding below sits in the code it changed.
* **LP-SR-4 to LP-SR-8, answered as specified, need nothing more** than the
  code review checking the answer against the fix and test named in each.
* **LP-SR-1 is the one I would not wave through on a description.** It is a
  write outside the project, with lines an attacker chooses, delivered by an
  ordinary clone. It is not part of this obligation, so it does not hold the
  clearance. But its fix must not count as closed until someone runs the named
  test against the fixed bytes. The code review doing that is enough; it needs
  no second Security Review. The Maintainer should decide whether it rides
  this answer or gets its own repair, before the next release either way.
  LP-SR-2 has the same shape at lower severity, and the same fix family; it
  can ride with LP-SR-1.

## Findings at a glance

| id | what | severity | blocks this obligation? |
|---|---|---|---|
| LP-SR-1 | `upgrade --apply` creates a file outside the project through a linked `dev/.cairn/profile.yml`, with lockfile-chosen lines; delivered by `git clone`; pre-existing | high | no (separate hole; fix must be measured) |
| LP-SR-2 | a lockfile that is itself a link is read through it and written back through it by `--apply` and `--finalize`; an outside JSON file was rewritten | medium | no |
| LP-SR-3 | the lockfile's `cairn_commit` reaches `git rev-list` as an option: `--output=` made `--plan` create a file outside | low | no |
| LP-SR-4 | raw control characters still reach the terminal: lockfile `modules` (report) and a carried review area's names (`--apply` messages) | low | no |
| LP-SR-5 | the advisory runs before the check and stats and globs a folder outside the project; the new inventory text says it reads only through its contained reader | low | no |
| LP-SR-6 | the "leads outside" refusal tells an adopter with a linked folder to restore the lockfile | low | no |
| LP-SR-7 | a linked renamed vendor wrapper: `--finalize` records a digest of the outside file in the lockfile; the inventory's "Not covered" note says its content reaches a write only through `_write_stage` | informational | no |
| LP-SR-8 | "inside the project" includes `.git/` and ignored files: a crafted record overwrote `.git/description` with template text | informational | no |

## Q1 — Is it closed?

### The defect, measured on the old engine

New record `{"src": "<relative path from templates/ to the outside marker>",
"dst": "docs/notes.md", "verbatim": true}` with hashes matching the committed
`docs/notes.md`. On `90715acb`:

```
[before-src-dotdot]
  plan      rc=0
  stage     rc=0 MARKER-IN-PROJECT:dev/.cairn-upgrade/files/docs/notes.md
  apply     rc=0 MARKER-IN-PROJECT:docs/notes.md
  docs/notes.md NOW: 'OUTSIDE-fafea89a2119\nsecond line OUTSIDE-fafea89a2119\n'
```

### The repaired engine, every lockfile path shape, every action

Each case is a fresh copy of one real install (`scaffold.py` with the
`solo-greenfield` preset), a fresh outside folder holding the marker file, and
the real `scaffold.py upgrade` run as a subprocess for `--plan`, `--stage`,
`--apply`, `--finalize --force` and `--adopt-collisions`. After each run I
checked: exit code, the marker or a raw control character in anything printed,
the marker anywhere in the project (the review area included), and a
byte-and-link snapshot of the outside folder.

| field | shapes | result, all five actions |
|---|---|---|
| `src` | `..` to the marker; absolute; `./..`; `//abs`; `core/../..`; `../TEMPLATES/..`; `~/..`; `file://`; `x:..`; backslashes; zero-width space between the dots | exit 2, `'src' is not a plain relative file name inside the Cairn source tree`, nothing written |
| `src` | `templates/core/evil` a link to the outside folder (in a separate copy of the Cairn tree), `src: core/evil/secret.md` | exit 2, `'src' leads outside the Cairn source tree` |
| `src` | `/` replaced by U+2215, U+FF0F, U+2044, U+29F8; `..` replaced by fullwidth dots, U+2025, `%2e%2e`, `.` + U+0307 + `.`; `/` as `%2f` | not refused, correctly: plan/stage/apply/finalize exit 0, adopt exit 1 (no adoptable set). The name is one odd file name under `templates/`, absent, so the record reads "removed upstream". Marker nowhere, outside unchanged |
| `dst` | `..`; absolute | exit 2, `is not a plain relative file name inside the project` |
| `dst` | the file is a link out; a tracked mergeable file (`NOTICE.md`) replaced by a link out; a dangling link out; `DOCS/LINKDIR/secret.md` through a lowercase `docs/linkdir` link out | exit 2, `'dst' leads outside the project`; the refusal never printed the link's target |
| `base_cache` | `..`; absolute; the cache file a link out; the cache folder a link out, reached by an uppercase name | exit 2, `'base_cache' ...` |

The marker never appeared in any output, any project file or the review area,
and the outside folder never changed. Also measured: `--plan --to HEAD` is
refused the same way; `--adopt-module` and `--init-lock`, which run before the
check, read no record path over a crafted lockfile (exit 0, marker nowhere); a
self-loop link and a link that leaves the project and comes back are judged by
where they end and are not refused at `--plan` (the write guard still refuses
`--stage`). With `base_cache` pointed at an ignored in-project `.env`, under
both the default and the `diff3` conflict style, the `.env` text did not reach
the review area.

### The review area

The new tests' four planted links (staged file, new-base file, staged folder,
the metadata file), the whole review area as a link, and a hand-built review
area naming an outside saved ancestor all pass at `2f07f2e7` (72 passed,
9.0 s). I read `_assert_stage_has_no_links`: it runs first in `_apply_upgrade`,
before the metadata is read, and walks without following links.

### Routes beside the three fields

All four are written up as findings: LP-SR-1 to LP-SR-4. Two more were checked
and are clean. A linked `dev/.cairn/profile.yml` pointing at an existing
outside file is read, and the grammar error names only the line number, not
the text. Lockfile `cairn_version`, `tokens` and `profile.preset` carrying ESC
and a line break printed nothing raw on any action.

## Q2 — The ordering cost

`cmd_upgrade` runs the forked-facade advisory (`upgrade.py:2552`) before
`_check_lockfile_paths` (`upgrade.py:2563`). The frozen
`bootstrap/tests/test_fork_advisory.py` requires that: its node 16 sets
`"src": "../../../../etc/hostname"` (line 1138) and expects the advisory to
still print at `cmd_upgrade`.

**What it costs, measured.** The advisory's candidate gate joins
`target_root / engine_rel` unchecked (`lockfile.py:510`) and calls `is_dir()`
and `glob("*.py")` (`lockfile.py:512`). With a record
`dst: ../outside/probe.py` (verbatim, `hash != base_hash`):

```
outside/_probe/x.py present: plan rc=2 refused; NOTE printed: True
  upgrade: NOTE -- facade '../outside/probe.py' differs from its install-time baseline ...
  but its engine package '../outside/_probe' is installed
outside/_probe/x.py absent:  plan rc=2 refused; NOTE printed: False
```

So one line on the operator's own terminal answers yes or no: does a folder
named `_<name>` holding a `.py` file exist at a path the lockfile chose? No
byte is read, nothing is written, and the answer goes nowhere the lockfile's
author can see unless the operator shares the output.

**Acceptable? Yes, as a residual.** **Documented? Only half.** The frozen test
says it plainly (node 13: "it stats and globs an engine directory outside the
target", `test_fork_advisory.py:859`), and `lockfile.py` marks candidate
selection as lock-derived (`lockfile.py:495`). But the new Class D row says
the advisory "reads names only through its own contained reader", which is not
the whole story. The commit message does not mention it either. LP-SR-5.

**Avoidable without touching a frozen file, measured.** In a `git archive`
copy of `2f07f2e7` I ran the `dst`/`base_cache` half of the check before the
advisory and kept `src` after it. `test_fork_advisory.py`: 37 of 37 passed.
The new file: 71 passed, and 1 failed, only its "checked in exactly one place"
pin. The probe above then printed no NOTE.

## Q3 — The legitimate adopter with a linked folder

`dev/modules` moved beside the project and replaced by a link to it:

```
before (90715acb):  plan rc=0;  stage rc=2 "refusing to write through a symlinked parent: <absolute path>"
after  (2f07f2e7):  plan rc=2;  stage rc=2
  error: upgrade refused (containment): record 13: the lockfile's 'dst' leads outside the project: 'dev/modules/claim-check.md'
    The lockfile is project data. Look at that record in dev/.cairn/cairn-lock.yml (`git log -p` on it shows who changed it), restore it from a copy you trust, then re-run.
```

**Right behaviour, wrong words.** That adopter could never finish an upgrade
anyway, because `--stage` refused. Refusing at the read-only `--plan` is
consistent, and it stops `--plan` reading their files from outside the
project, which the engine cannot tell apart from a hostile link. But the
remedy points at the lockfile, which is fine. Restoring it changes nothing, so
the adopter is sent the wrong way. LP-SR-6.

## Q4 — AST

I computed per-symbol digests with `digest_module` from
`bootstrap/tests/_ast_attest.py` at each commit boundary:

```
6c436a9f^ -> 6c436a9f   CHANGED _apply_upgrade, _theirs_bytes, _theirs_text, cmd_upgrade
                        NEW     _assert_stage_has_no_links, _check_lockfile_paths,
                                _contained_lockfile_path, _lockfile_refusal
80c54552^ -> 80c54552   CHANGED _emit_skill_copy_fallback, format_forked_facade_warning
90715acb  -> 2f07f2e7   exactly the union of the two lines above
6c436a9f -> 80c54552^, 80c54552 -> 2f07f2e7: nothing
```

**Confirmed.** Against the committed baseline, `test_ast_attest.py` at
`2f07f2e7` reports 11 CHANGED and these 4 NEW (2 failed, 28 passed). That
includes `_cmd_adopt_module`, `_symlinks_available`, `create_dev_tree`, `main`
and `seed_gitignore`. Those five were already CHANGED at `90715acb`, from
earlier repairs, and so was `cmd_upgrade`, which this repair re-digests.
Nothing else moved because of this repair. The re-anchor is still owed
(`bootstrap/AST_BASELINE_RUNBOOK.md`). The fixes below add to it:
`_self_heal_profile_config` (LP-SR-1), `_cmd_finalize_lockfile` (LP-SR-2),
`_behind_by_n` (LP-SR-3), `_print_upgrade_report` (LP-SR-4), and
`_resolve_vendor_wrapper` if LP-SR-7 takes the code fix.

## Findings

### LP-SR-1 — `upgrade --apply` creates a file outside the project through a linked profile — high

**Evidence.** `_self_heal_profile_config` (`upgrade.py:2385`) checks
`profile_path.exists()`, which is False for a dangling link, then calls
`write_text` (`upgrade.py:2425`), which follows the link. `cmd_upgrade` calls
it on every `--apply`, before `_apply_upgrade` and before any staged upgrade is
looked for. The install I probed carries no `dev/.cairn/profile.yml`, so the
self-heal fires on a normal tree.

* Link to a missing outside file, then `upgrade --apply` alone, no stage:
  it prints `[self-heal] materialized dev/.cairn/profile.yml ...`, then
  `error: no staged upgrade found`, exit 1. The outside file now exists
  (592 bytes).
* Same on `90715acb`: pre-existing.
* Delivered by a repository: a relative link
  `../../../outside/from-clone.yml`, committed, then `git clone`; the clone
  carries the link; `--apply` created the outside file; `git status` in the
  clone is clean.
* With lockfile `profile.preset` set to `"solo-greenfield\nINJECTED_LINE: 1"`,
  the created file holds `INJECTED_LINE: 1` on a line of its own. `preset`, the
  axis values and the module names are written unquoted.

So a repository can make one command create a new file at a path it guesses,
such as a shell start-up file that does not exist yet, holding a line it
chose. An existing file is not overwritten, because then `exists()` is true.

**Fix.**
1. First statement of `_self_heal_profile_config`:
   `_assert_safe_write(profile_path, target)`. It refuses a dangling link, a
   linked file and a linked parent; I checked the dangling case on the guard.
2. In `cmd_upgrade`, wrap the `--apply` self-heal call in
   `try/except ScaffoldSecurityError`, print
   `error: profile self-heal refused (containment): {exc}` plus
   `  replace the link with a regular file, then re-run.`, and return 2. This
   mirrors the `.gitignore` preflight just above it.
3. Before writing anything, return False (no self-heal) unless every value it
   would write (`preset`, each axis value, each module name, each token) is a
   `str` with `isprintable()`. Quote `preset`, the axis values and the module
   names with `_yaml_sq`, as the tokens already are.
4. Add a `_self_heal_profile_config` row to Class A of
   `bootstrap/_scaffold/SECURITY_MUTATIONS.md`.

**Test that shows it closed** (in the new, non-frozen test file, driving the
real command line):
`test_apply_never_creates_a_profile_through_a_link`, parametrized over:
* a dangling absolute link;
* a dangling relative link committed and delivered by `git clone`;
* a link to an existing outside file;
* `dev/.cairn` itself a link out, with its lockfile copied there.

Each runs `--apply` with no stage. Assert: exit 2, `refus` in stderr, no
Traceback, nothing created or changed in the outside folder (snapshot), and
the link still a link.

Plus `test_self_heal_writes_no_line_break_from_the_lockfile`: preset carrying
`\nINJECTED_LINE: 1`, no profile file. Assert that `--apply` either writes no
`dev/.cairn/profile.yml` or writes one with no line starting `INJECTED_LINE`.

### LP-SR-2 — a lockfile that is a link is written back through the link — medium

**Evidence.** `read_lockfile` reads `dev/.cairn/cairn-lock.yml` through
whatever it is. Two writes then follow the link unguarded: `_apply_upgrade`
(`upgrade.py:2355`) and `_cmd_finalize_lockfile` (`upgrade.py:2033`).
`_commit_lock_and_caches` guards the same name, so the adopt paths are safe.

* Lockfile → an outside copy whose `cairn_version` was changed to
  `0.0.1-outside`. `--stage` exit 0, then `--apply` exit 0: the outside file
  now says `0.3.0`, and the project's lockfile is still a link.
* Lockfile → an outside JSON object that is not a lockfile
  (`{"auths": {...}}`). `--finalize --force` exit 0: the outside file was
  rewritten with Cairn's comment header in front, so a strict JSON reader can
  no longer parse it.
* Lockfile → outside plain text: exit 1, "no lockfile", and nothing printed
  from the file.

Reasoned, not measured: the outside file's `tokens`, if it has any, are
substituted into staged files. The target must be an existing JSON object
file at a path the repository guesses.

**Fix.**
1. In `cmd_upgrade`, before `read_lockfile` and before the `--adopt-module`
   branch: `_assert_safe_write(target / _LOCKFILE_REL, target)`. On
   `ScaffoldSecurityError`, print
   `error: upgrade refused (containment): the lockfile is a link, or sits behind one`
   plus a remedy line (`replace it with a regular file, then re-run.`), and
   return 2.
2. Immediately before each of the two raw lockfile writes, call
   `_assert_safe_write(target / _LOCKFILE_REL, target)`. The reader-side check
   does not cover a link swapped in mid-run.
3. Add the two writes to the `_apply_upgrade` row of Class A, and add a
   `_cmd_finalize_lockfile` row.

**Test that shows it closed.**
`test_a_lockfile_that_is_a_link_is_refused_and_never_written`, parametrized
over:
* an outside valid lockfile, with a different `cairn_version`;
* an outside JSON object;
* a dangling link.

Run all of `--plan`, `--stage`, `--apply`, `--finalize --force`,
`--adopt-collisions <dummy>` and `--adopt-module dual-review`. Assert: exit 2
(the dangling case may keep its existing "no lockfile" exit 1), no Traceback,
and the outside snapshot unchanged.

### LP-SR-3 — `cairn_commit` reaches `git rev-list` as an option — low

**Evidence.** `_behind_by_n` builds `f"{lock_commit}..{new_commit}"`
(`lockfile.py:230`) from the lockfile's `cairn_commit`, unchecked. With
`cairn_commit = "--output=<outside>/created-by-git"`, `upgrade --plan` (the
read-only action) exited 0 and created an empty
`<outside>/created-by-git..2f07f2e7`. The old engine does the same: an empty
`created-by-git..90715acb`.

The name always ends `..<running commit>`, so the damage is empty junk files
in any writable folder, or truncating a file of that odd name. `_check_lockfile_paths`
does not look at this field.

**Fix.** At the top of `_behind_by_n`, if `lock_commit` is not a `str`
matching `re.fullmatch(r"[0-9a-f]{7,40}", lock_commit)`, return the existing
`"adoption drift: behind-by-N check unavailable (refs not comparable)"`
without running git. The lockfile writer only ever records a short hex commit
or `unknown`. Do not validate `new_commit` that way, because `--to <tag>` is
legitimate.

**Test that shows it closed.**
* Unit: `_behind_by_n(CAIRN_ROOT, f"--output={tmp_path / 'x'}", "HEAD")`
  returns the "unavailable" text, and `tmp_path` stays empty.
* Command line: the lockfile `cairn_commit` set as above; `--plan` exits 0;
  the outside folder is unchanged; stdout has `check unavailable`.

### LP-SR-4 — raw control characters still reach the terminal — low

**Evidence.**
* A lockfile `modules` entry `"x\x1b[2J\x1b[31mFORGED\nforged: line"`:
  `--plan` and `--stage` printed the ESC raw, through
  `modules removed upstream (flagged)` (`upgrade.py:840`).
* A review area the repository carries, with the same kind of value: `--apply`
  printed it raw in `review_only` (exit 1), in `module_blocked` (exit 1), and
  in `new_commit` on success (exit 0), through `upgrade.py:2178`,
  `upgrade.py:2196` and `upgrade.py:2373`.
* The conflict-marker, changed-on-disk and expected-absent messages print
  staged names the same way (read, not measured).

The repair established that the review area is project data, and fixed this
fault for `dst`. These are the same fault, so they belong with it.

**Fix.** Refuse rather than escape, matching the repair's pattern.
1. In `_check_lockfile_paths`: if `lock.get("modules")` is present, it must be
   a list of non-empty `str` with `isprintable()`, else `_lockfile_refusal`.
2. In `_apply_upgrade`, right after the metadata is parsed: every name in
   `staged_files`, `review_only`, `module_blocked` and `expected_absent`, and
   every key of `kinds` and `new_entries`, must pass
   `_contained_lockfile_path(target, name, "staged name", "the project")`.
   `new_commit` and `new_version` must be `str` with `isprintable()`. Any
   failure raises the stage refusal; it is already turned into exit 2.

**Test that shows it closed.**
* Lockfile `modules` gets an ESC and line-break entry: all five actions exit
  2, with no `\x1b` and no line starting `forged` in the output.
* A planted review area with the same value in `review_only`,
  `module_blocked` and `new_commit` in turn: `--apply` exits 2, no `\x1b` is
  printed, and no project file changes.

### LP-SR-5 — the advisory's glimpse outside, and the text that understates it — low

**Evidence.** Q2 above.

**Fix.**
1. Give `_check_lockfile_paths` a `fields` parameter, defaulting to
   `("src", "dst", "base_cache")`.
2. In `cmd_upgrade`, call it with `fields=("dst", "base_cache")` before
   `trusted_upstream` / `forked_facade_findings`, and with `fields=("src",)`
   where it is now. Both refusals keep the same exit-2 handling.
3. Correct the Class D row and the `cmd_upgrade` comment. Say that the
   advisory reads file bytes only through its contained reader, but its
   candidate gate stats and globs `<dst folder>/_<name>/` unchecked. Say that
   the residual left after the split is an in-project engine folder that is
   itself a link out.

If the fixer keeps the single call instead, step 3 alone is the minimum
answer, and it must name the yes/no glimpse.

**Test that shows it closed.**
* The probe above as a test: `dst: ../outside/probe.py` with
  `outside/_probe/x.py` present; `--plan` exits 2 and `NOTE` is not in stderr.
* Replace the "exactly one place" pin: the project-side check's line comes
  before the `forked_facade_findings` call; the `src` check comes after it and
  before every step the pin lists.
* `test_fork_advisory.py` unchanged and green (measured: 37 passed).

### LP-SR-6 — the "leads outside" refusal sends an adopter to the wrong fix — low

**Evidence.** Q3 above. `_lockfile_refusal` has one remedy for both causes.

**Fix.** Give `_lockfile_refusal` a remedy argument. The shape branch keeps
today's text. The containment branch ("leads outside") says:

> A folder or file on the way is a link that leads out of {tree}; upgrade
> does not read or write through it. Replace the link with a real folder or
> file inside the project. If the record itself was changed, restore
> dev/.cairn/cairn-lock.yml from a copy you trust. Then re-run.

**Test that shows it closed.** `dev/modules` a link to a folder beside the
project; `--plan` exits 2, and stderr holds `is a link that leads out` and
`Replace the link`. The existing tests that assert
`dev/.cairn/cairn-lock.yml` is in stderr still pass.

### LP-SR-7 — a linked vendor wrapper, and a "Not covered" note that is not quite true — informational

**Evidence.** `VENDOR.md` removed, `CLAUDE.md` a link to the outside marker.
* `--plan` exit 0: the outside file is read as the project's copy; nothing is
  printed from it.
* `--stage` exit 2: the write guard refuses.
* `--finalize --force` exit 0: the lockfile now holds the outside file's
  SHA-256, and the `VENDOR.md` record now names `CLAUDE.md`.

The Class D note says the wrapper's content reaches a write only through
`_write_stage`. A digest of it reaches the tracked lockfile through
`--finalize`. `_resolve_vendor_wrapper` accepts any `is_file()`
(`upgrade.py:1153`), and that follows links.

**Fix.** In both tiers of `_resolve_vendor_wrapper`, accept a candidate only
if `is_file() and not is_symlink()`, and test that before tier 2 reads its
first lines. The minimum answer instead: correct the note to name the digest
route.

**Test that shows it closed** (code fix): the setup above; after
`--finalize --force`, the outside file's hex digest is not in the lockfile and
the record still names `VENDOR.md`. The run is expected to exit 1 with "missing
on disk", which fails closed.

### LP-SR-8 — "inside the project" includes `.git/` and ignored files — informational

**Evidence.** After `git init`, a record with `dst: .git/description`,
verbatim, and hashes equal to the bytes a fresh `git init` writes there. The
`--plan` / `--stage` / `--apply` runs (the apply was given `--force`, which
this untracked file did not need) exited 0, and `.git/description` was
replaced by the `NOTICE.md` template text.

The text is always Cairn's own template, and the attack needs the file's
exact current bytes. So this is integrity damage only. But `.git/` is not
project data in the sense the repair means.

**Fix.** In `_contained_lockfile_path`, for the project root only (`dst`,
`base_cache`), refuse a name whose first part is `.git` in any letter case.
The minimum answer instead: one sentence in Class D saying that "the project"
means the whole project folder, `.git/` and ignored files included.

**Test that shows it closed** (code fix): the guard's shape table gains
`.git/config` and `.GIT/hooks/pre-commit` for `dst` and `base_cache`, and the
command-line probe above exits 2 with `.git/description` unchanged.

## Verification run on `2f07f2e7`

Scoped only. The full suite was not run and `CAIRN_FULL_SUITE` was not set.

| what | result |
|---|---|
| `test_upgrade_lockfile_path_containment.py` | 72 passed, 9.0 s |
| `test_fork_advisory.py` (37), `test_security_leaf.py` (5), `test_oracle.py` (18), `test_upgrade.py` (106), `test_upgrade_side_door_parity.py` (15) | 181 passed, 45.2 s; gate anchor present; no skips |
| `test_ast_attest.py` | 28 passed, 2 failed (the re-anchor that is owed, Q4) |
| split-order experiment (`git archive` copy, patched) | `test_fork_advisory.py` + the new file: 108 passed, 1 failed (the one-call pin) |
| command-line probes | 31 path shapes × 5 actions on the repaired engine, the baseline case on the old engine, and the route, ordering, adopter, lockfile-link, loop and `.git` probes above |

## What I did not cover

* **No mutation ledger.** The implementer's 31-mutant ledger is the code
  review's to check. I mutated nothing in the engine except the one
  split-order experiment.
* **Races.** A local process swapping a name between the check and the read,
  or between `_assert_stage_has_no_links` and the read of the staged copies, is
  the model `bootstrap/SAFETY.md` accepts. Hard links in a review area were
  not tried: git cannot carry one, and only a local process can make one
  that points at an existing outside file.
* **Other readers of the lockfile.** `bootstrap/verify_integrity.py`, the
  session tools and `cmd_drift` / `cmd_verify` (Class C) were not probed.
  `verify_integrity` has its own containment check, which I did not test.
* **Other platforms.** macOS only. Windows drive and UNC forms are covered by
  the shape table in the tests, not by a run. Case-sensitive file systems
  were not tried.
* **Network side effects of the glimpse.** On a system that automounts paths
  such as `/net/<host>`, the advisory's unchecked `is_dir()` could trigger a
  mount. This machine's `/etc/auto_master` has no `/net` entry, so this is
  reasoned, not measured. The LP-SR-5 split removes it for `..` and absolute
  names.
* **The fixes.** None was written or run. The tests named above are a
  specification, not measured passes.
