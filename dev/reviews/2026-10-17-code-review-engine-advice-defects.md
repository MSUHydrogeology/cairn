# Code review (External) — the engine advice defects (`6894ed0c`) — Claude Opus 5.5 — 2026-10-17

**Obligation**: External code review (falsification), the one code review the
trivial lane's defect-repair carve-out requires (`doctrine/lifecycle.md` >
"Three lanes"). Fresh session, not the implementing session. The implementer
is the same agent type, so the distance here is a fresh context, not a
different type.
**Reviewed range**: 6894ed0c (parent `6894ed0c^` used as the "before" engine).
**Interpreter**: Python 3.13.13 at `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
`PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider`. Platform: darwin. Every
install, stage and mutation ran in `git archive` extractions of `6894ed0c` and
`6894ed0c^` under the session scratchpad, against throwaway target trees. One
read-only test node ran in the live checkout, to confirm a failure was caused
by the environment; `git status --short` was unchanged before and after.

**Verdict**: ACCEPT-WITH-FOLLOWUPS — 0 blocking, 5 non-blocking.

Both repairs do what the commit says. An install over a tree that already has
a lockfile no longer sends the adopter round in a circle. The review copies
(`.theirs`) no longer show filled-in placeholders as changes. On an untouched
migrated tree, differing review pairs fell from 10 to 2, and both remaining
differences sit inside slot bodies, as the commit's comment says. Nothing that
`--apply`, the lockfile or the published `scaffold.py --manifest` depends on
moved. One small remnant of the same defect remains (EA1): when the profile
has no axes, a review copy keeps two marker lines the install strips. That is
a one-line fix in `_write_stage`. It should land before the Maintainer
re-anchors the AST baseline, so the baseline moves once and not twice.

## Falsification ledger

| # | Check | If the change were wrong, this would show | Result |
|---|---|---|---|
| 1 | Install over a migrated tree with one edited file (`AGENTS.md`), then follow the printed advice | the warning still names `--init-lock`, the lockfile changes, or `upgrade --plan` fails | **Holds.** Warning names `upgrade --target <repo> --plan`; lockfile sha unchanged; `--plan` exits 0 and names `--stage` next. The parent engine names `--init-lock`, and following it answers "already exists; nothing to migrate" (exit 0). The loop is reproduced, and the fix closes it. |
| 2 | Same, on a tree with **no** lockfile | the `--init-lock` advice is lost | **Holds.** The warning still names `upgrade --init-lock`. |
| 3 | `--stage` an unedited migrated tree, parent engine against reviewed engine | install-filled placeholders still in `.theirs` | **Holds.** Parent: 10 of 27 pairs differ; the `.theirs` files carry 16 `{{project_name}}` and 6 `{{claim_check_command}}`. Reviewed: 2 of 27 differ (`AGENTS.md`, `dev/PLANNING.md`), and with every `cairn:slot` body blanked, 27 of 27 are byte-equal. The only placeholders left are `{{author}}` and `{{reviewer}}`, on both sides. |
| 4 | Can a verbatim file reach the new rendering? | a script's `{{...}}` text rewritten | **No, by construction.** The verbatim branch of `_compute_upgrade` returns before any review-only plan is made (`bootstrap/_scaffold/upgrade.py:361`). Measured: 23 verbatim records, 27 review-only, overlap empty. |
| 5 | Can literal `{{...}}` text in a mergeable file be corrupted? | text the install leaves alone gets substituted | **No.** `substitute_tokens` replaces only keys in its map. The map is the lockfile's tokens plus the reference-script default: the same `KNOWN_TOKENS`-filtered set the install applies. A literal `{{author}}` survives on both sides. |
| 6 | Rendering against the install's expected bytes (`write_install_lockfile`'s `would`) and the mergeable path | a token, axis or ordering mismatch | **One mismatch → EA1.** Order (substitute, then strip) matches `_install_one` and the `would`. The token setdefault matches the CLI (`bootstrap/_scaffold/cli.py:418`); for a fresh-install lockfile those defaults are already in `tokens`, so it is a no-op there. Axes come from the same `_embedded_axes`. The mismatch: an empty axes map skips the strip, which the install still applies. |
| 7 | `new_profile=None` fallback | wrong or no sizing | **Holds.** A direct `_write_stage` call without the argument sizes by the lockfile profile, byte-identical to a same-profile stage. |
| 8 | Profile changed since install (`human_team: solo` → `small-multi` in `profile.yml`) | sizing ignores the change, or leaves markers | **Sensible.** `.theirs` gains the "Human contributors" section with its markers stripped; `.ours` lacks it. The stage metadata records the new profile. This matches `_compute_upgrade`, which sizes `theirs` under the current profile. With `profile.yml` absent, the stage falls back to the lockfile profile, byte-identical. |
| 9 | The two new tests on the parent engine | a test that cannot fail | **Both red** (2 failed, 6 passed in `TestInitLock`). Green on 6894ed0c (8 passed). |
| 10 | Mutation of each leg of the change | a leg no test pins | **Four survivors → EA2.** |
| 11 | Contract: what `--apply` reads, the lockfile, `scaffold.py --manifest` | a machine consumer of `.theirs`, or a changed contract byte | **Unchanged.** Nothing reads a review-only `.theirs` (only messages name the directory). The stage-metadata dict is untouched by the diff, and `stage-metadata.json` is identical between engines. `scaffold.py --manifest` is byte-identical between parent and reviewed (7,662 bytes). The install returns before any lockfile write in both branches. |
| 12 | Safety | a new path, containment, YAML, or subprocess surface | **None.** The `.theirs` write path is unchanged and already guarded: every plan destination passes `_assert_safe_write` before any write (`bootstrap/_scaffold/upgrade.py:825`). Bandit 1.9.4 `-ll -r bootstrap/_scaffold`: no findings. `bootstrap/tests/test_security_lint.py`: 11 passed, no skip. **No Security Review trigger applies**: the change alters the content of one already-contained write and one message, and nothing in parsing, path handling, or what is authorized. |
| 13 | AST runbook Step 1 | an undeclared CHANGED, MISSING or DUPLICATE | **Exactly as declared.** CHANGED 2: `FunctionDef:_write_stage` 2def9e4453394dae → 52f1cff8340692dc and `FunctionDef:write_install_lockfile` 63e897b5d01e8deb → c7076e7d963ad9e6. MISSING 0, DUPLICATE 0, NEW 86 (the parent shows CHANGED 0, NEW 86). One NEW key swapped, `Import:8d5fb3a9a20f` → `Import:58ab263fdd4b`, from the added `reference_script_token_defaults` import. Import keys are exempt from the known-new pin by design, and `_ast_attest.py verify --known-new` reports only the two CHANGED. Neither symbol is in `_UPDATE_ALLOWLIST`, so the repair is the Maintainer's direct correction, as the commit says. |
| 14 | Engine family | a regression elsewhere | **None.** 11 files (`test_upgrade`, `test_skills_upgrade`, `test_upgrade_module`, `test_upgrade_module_additions`, `test_upgrade_side_door_parity`, `test_scaffold`, `test_module_merge_lockfile`, `test_lockfile_module`, `test_lockfile_provenance`, `test_install_module`, `test_skills_install`): 285 passed, 1 failed. The failure is environmental (see Seen, not raised). |

## Findings

### [EA1] non-blocking — with no axes in the profile, `.theirs` keeps marker lines the install strips

**What.** `_write_stage` strips only `if review_axes:`
(`bootstrap/_scaffold/upgrade.py:898`). The install strips whenever it has an
axes map, even an empty one. `_install_one` tests `if axes is not None`
(`bootstrap/_scaffold/install.py:289`). The lockfile's expected-bytes
computation strips with `profile.get("axes") or {}` every time
(`bootstrap/_scaffold/install.py:1764`). With an empty map,
`strip_conditional_regions` keeps the content but removes the two marker
lines. So for a profile with no axes, `.theirs` carries a `cairn:if` /
`cairn:endif` pair the installed file never had. That reads as a change the
adopter never made, which is the defect class this commit repairs.

**Reachable.** The Appendix B example profile in `bootstrap/BOOTSTRAP.md` (a
literal `modules:` list, with no preset and no axes) installs with lockfile
`profile: {"axes": {}, "preset": null}`. Review-only pairs arise in such a tree
when a base cache is missing or a tracked file is missing on disk. A migrated
lockfile cannot reach this state, because `--init-lock` requires all six axes.

**Evidence.** I installed with only `project_name` and `test_command`. The
lockfile axes were `{}`, and the installed `AGENTS.md` had 0 `cairn:if` lines.
I then deleted that tree's base-cache copy of `AGENTS.md` and ran `--stage`.
The `AGENTS.md` pair differs by the expected slot body plus
`< <!-- cairn:if human_team in small-multi,large-multi -->` and
`< <!-- cairn:endif -->`.

**Fix.** Drop the guard and call the strip unconditionally. It is the identity
on marker-free text (rule 5 of its own docstring). I checked this in a scratch
copy: the axes-less pair becomes equal outside slot bodies, and `TestInitLock`
passes (8). The guard was copied from `_compute_upgrade`
(`bootstrap/_scaffold/upgrade.py:406` and its new-file adds), which has the
same gap against the install. That is older than this commit and outside its
scope. I mention it so whoever fixes this can decide whether to align both.

**Why non-blocking.** The defect is two HTML comment lines, in one file, in an
uncommon state, and the change is strictly better than its parent, which also
carried every placeholder. **Timing:** the fix touches `_write_stage`, so it
should land before the AST re-anchor.

### [EA2] non-blocking — the tests pin only the token leg; four behaviours survive mutation

I applied each mutation alone to a scratch copy and ran it against
`TestInitLock` and the 11-file engine family from ledger row 14:

| Mutation | Outcome |
|---|---|
| remove the `strip_conditional_regions` call | survives. `AGENTS.md.theirs` gains a 13-line "Human contributors" section, plus its markers, that a solo install never had |
| size by `lock["profile"]` and ignore `new_profile` | survives. A profile change since install stops showing in `.theirs` |
| `setdefault` → plain assignment | survives. It would override a profile-supplied `claim_check_command` |
| print the `--plan` remedy for every tree | survives. A tree with no lockfile would be told its lockfile "is kept unchanged" |

Controls: restoring the parent's remedy, the raw `.theirs` write, or deleting
the setdefault loop each turns the matching new test red. The last names
`{{claim_check_command}}` in `dev/modules/claim-check.md`, as the commit says.

The placeholder test compares the token *names* left in each file. That catches
the raw-template defect, but it cannot see sizing or values. A stronger
property, measured: on an unedited migrated tree, each pair is byte-equal
once every `cairn:slot` body is blanked. It holds on 6894ed0c (27 of 27). It
fails on the parent (10 files) and on the strip-removed mutation
(`AGENTS.md`). It is also the direct test of the comment's claim that only
slot bodies differ. **Recommend** adding it, plus one assertion that a tree
with no lockfile still gets `--init-lock`. Given an axes-less fixture, the same
property would have caught EA1.

### [EA3] non-blocking — the gate-manifest collection change is recorded nowhere

`bootstrap/tests/test_upgrade.py` is a frozen file in
`bootstrap/tests/fixtures/gate_manifest.json`. Its hash was already out of
date before this commit, and the file is already named in the queued re-anchor
row ("Re-anchor the gate manifest — 10 frozen files, then nine more",
`dev/PLANNING.md:156`). That row says to derive the frozen set from the
manifest's own keys at ceremony time, so the hash is covered. The *collection*
is not. The row lists the test-node changes the ceremony should expect,
including two added to `test_upgrade.py::TestInitLock` by `f3c839a7` and
`b61983bb` (`dev/PLANNING.md:183`). This commit adds two more. The manifest
pins 4 `TestInitLock` nodes, and the tree now has 8 (4 + 2 + 2). The commit's
"Owed" paragraph names only the AST baseline. A changed frozen file does not
redden the suite (`AGENTS.md` > Operational pitfalls), so nothing will surface
this before the ceremony meets two unexplained nodes. **Fix:** name the two
node IDs in that row at its next serialization point, or in the AST re-anchor
commit's body. I did not edit the board, because it is a shared file.

### [EA4] non-blocking — the install's "lockfile exists" check is not the check `--init-lock` refuses on

The install checks `(target / _LOCKFILE_REL).exists()`
(`bootstrap/_scaffold/install.py:1816`). `--init-lock` refuses only when
`read_lockfile(target) is not None` (`bootstrap/_scaffold/upgrade.py:1187`),
and `read_lockfile` returns `None` for a file that does not parse. I
reproduced this with a lockfile that does not parse. The install says the
lockfile "is kept unchanged" and points at `--plan`. `--plan` answers "no
dev/.cairn/cairn-lock.yml in the target. Run `upgrade --init-lock`", and
`--init-lock` then succeeds. That is two hops, not a loop. But the new
comment's premise ("--init-lock refuses once a lockfile exists") holds only for
a lockfile that parses. **Fix:** one line, testing `read_lockfile(target) is
not None`, which lives in the `.lockfile` module that `install.py` already
imports from. `write_install_lockfile` is the other CHANGED symbol, so the same
timing note as EA1 applies.

### [EA5] non-blocking — the caller's comment still describes only the old advice

`bootstrap/_scaffold/cli.py:733` to `:735` says the install, on divergence,
"points the user at `upgrade --init-lock`". That is now true only when no
lockfile exists. The fix is comment-only, with no AST effect.

## Seen, not raised

* **The blocked-addition `.theirs` files are still raw**
  (`bootstrap/_scaffold/upgrade.py:928` to `:931`). Leaving them raw is right.
  The `--adopt-collisions` authorization digest is minted from those exact
  bytes (`:941` to `:946`), and rendering them would break that binding. The
  two loops never write the same adoptable path: an adoptable collision is
  never lockfile-tracked, and every review-only file is.
* **A malformed `cairn:if` in an upstream template now stops `--stage`** with an
  uncaught `ValueError` on a review-only file, where the parent staged it raw.
  Verified. The same template already stops the install (verified) and the
  3-way merge path. The input is Cairn's own template, so this is parity, not
  a regression an adopter can cause.
* **`.theirs` uses the lockfile's tokens, not the current `profile.yml`'s.** A
  token value changed since install therefore shows in neither `.theirs` nor
  the 3-way merge (`merge_file(..., tokens)`, `bootstrap/_scaffold/upgrade.py:409`).
  That is consistent across the engine and not a defect of this change.
* **`_write_stage`'s `new_profile=None` default** sizes by the lockfile while
  `_compute_upgrade` sizes by the current profile, so a direct caller that
  omits it gets the two under different profiles (verified with a direct call).
  The only caller (`bootstrap/_scaffold/upgrade.py:2490`) passes it.
* **"run … `--plan` to bring this tree up to date".** `--plan` is read-only, but
  it prints `--stage` as the next step, so the chain holds.
* **The board row's sentence** that the AST baseline "is separate and already
  current" (`dev/PLANNING.md:186`) is false from 6894ed0c until the re-anchor.
  The brief says to expect that.
* **`bootstrap/security_check.py` was not run.** It is the release ceremony (a
  clean-tree preflight, then the whole suite in release mode), and even
  `--help` fails closed. I ran Bandit directly instead (ledger row 12).
* **The one engine-family failure is environmental.**
  `test_upgrade_module_additions.py::test_module_additions_under_explicit_to_are_hard_blocked`
  needs a git checkout as the Cairn root. It fails the same way on the
  parent's archive copy and passes in the live checkout.

**Disposition**: accept. EA1 and EA4 are one-line fixes in the two CHANGED
symbols; land them, with EA2's stronger test, before the AST re-anchor so the
baseline moves once. EA3 and EA5 can ride any later commit.
