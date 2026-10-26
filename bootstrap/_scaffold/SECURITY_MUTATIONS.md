# SR6 — adopter-tree mutation inventory (scaffold-split Stage 1)

Every write/removal the scaffold engine performs **into an adopter's target
tree** must route its destination through a containment guard before touching
disk. The guards are the Stage-1 leaf `bootstrap/_scaffold/security.py`:

- **`_assert_safe_write(dst, target)`** — ordinary writes; refuses a symlinked
  destination, a symlinked parent, or a path resolving outside `target`.
- **`_assert_fanout_contained(dst, target)`** — the skills fan-out's vendor folder;
  like the above but permits `dst` itself to be the (re)created symlink. The files
  copied *under* that folder in copy mode do not use it: they use
  `_assert_safe_write`, which refuses a link at the name itself.

Both raise the single **`ScaffoldSecurityError`** identity. The guard raises it;
a command turns it into a plain exit 2 only where it asks first or wraps its own
writes: the three `.gitignore` preflights (`main`, `upgrade --adopt-module`,
`upgrade --stage` / `--apply`), the skills fan-out and onboarding calls in `main`,
the model-selection capture in `main` (a fixed refusal line), `--apply`,
`--stage` and `--adopt-collisions` around their own writes, and `upgrade`'s own
check of the lockfile's name, its check of the profile's name on `--plan`,
`--stage`, `--adopt-module` and `--adopt-collisions`, and its profile self-heal
on `--apply`.
Anywhere else it propagates as a traceback with exit 1, which the differential
oracle pins for an install over a planted link.

Reads are guarded too, where the name being read comes from project data: see
**Class D** below. Its refusals are a plain exit 2 from `upgrade` itself.

This inventory was taken **before** the Stage-1 motion and is **regression-pinned**
by the `bootstrap/tests/test_security_leaf.py` regression
`test_guarded_write_functions_still_call_a_containment_guard`, which AST-scans the
engine package and fails if any listed function stops calling a guard — so an
extraction stage cannot silently drop one.

## Class A — guarded adopter-tree writes (the pinned set)

Each function calls `_assert_safe_write` / `_assert_fanout_contained` on the
destination before any `mkdir` / `write_*` / `shutil` write:

| Function | Guard | Writes |
|---|---|---|
| `_stage_exclusive` | `_assert_safe_write` | a fresh, exclusive temporary sibling of a guarded destination, with permissions set through its descriptor |
| `_write_by_replacing` | `_stage_exclusive` plus a final-name check | replacement bytes staged beside the destination and renamed over it; `_cmd_init_lock` and `_cmd_finalize_lockfile` reach the guard through this helper |
| `capture_model_selection_mapping` | `_assert_safe_write` before reading or prompting, then `_write_by_replacing` | a filled mapping; a hard-linked old mapping is replaced, never written through |
| `_install_one` | `_assert_safe_write` | each installed template file |
| `write_local_env` | `_assert_safe_write` | `dev/.cairn/local-env.json` |
| `create_dev_tree` | `_assert_safe_write` | the empty `dev/` folder set. `mkdir(parents=True)` follows a link, so every destination is checked before the first `mkdir`: a linked `dev/`, or a linked folder below it, refuses with nothing created at either end |
| `install_onboarding` | `_assert_safe_write` | the always-on launcher + `_onboarding/` engine (installed FROM `_ALWAYS_ON_MAPPINGS`, the SSOT `install_manifest`/`scan_targets` also consume), activation log, PLANNING slot, preset source, onboarding docs. **Fail-closed before any write** on an incomplete launcher+engine completeness group (`assert_always_on_complete`, R4) |
| `write_install_lockfile` | `_assert_safe_write` | base-template cache, `cairn-lock.yml`. **Refuses (returns `None`)** before any write on an incomplete always-on completeness group (R4 — a partial group must not yield a lockfile tracking only the present members) |
| `_emit_skill_copy_fallback` | `_assert_safe_write` | regenerated canonical skill copy, diverged-copy quarantine. A copy name is not contained by construction: a checkout can plant a link at it (a dangling one creates a file outside the tree), a link at the quarantine name (`shutil.move` moves a file *into* the folder it names) or a link to a file that already holds the canonical bytes (the copy rewrites it in place). Every copy and quarantine name is guarded for the whole set, and anything but a free name or a plain file at a name, or a file where a folder must go, is refused, all before the first write, so a refusal leaves nothing half-done. Each copy is written to a new exclusive sibling and renamed into place, and the quarantine is `os.replace`, so a link that appears after the check is replaced, not followed. A refusal is fixed words, the escaped project-relative name and a remedy line (run `session-start` or install again, because an upgrade does not redo the fan-out when run again), never where a link points; the divergence warning names the quarantined files the same escaped, project-relative way. Two windows remain, each needing a process already running on the machine, which is the model `bootstrap/SAFETY.md` accepts: a parent folder swapped for a link between the check and the write (the copy or a temporary file can land outside), and the temporary file swapped for a link between its write and the rename (that link ends up at the copy's name; nothing is written outside, and the next install refuses it) |
| `fan_out_skills` | `_assert_fanout_contained` | vendor fan-out destination |
| `_cmd_adopt_module` | `_assert_safe_write` | a single added module's files (missing-dst install); the base-cache + lockfile writes route through `_commit_lock_and_caches`. A `seed_gitignore` dry run before the first write refuses a linked `.gitignore` (exit 2) ahead of the lockfile commit |
| `_cmd_adopt_collisions` | `_assert_safe_write` | the adopted collision's destination (containment re-check; never written); the base-cache + lockfile writes route through `_commit_lock_and_caches`. Resolves the adoptable occupied-destination collisions in **either** tier — module-internal (`new-module-blocked`) **and** core/always-on (`new-core-blocked`, side-door parity R5) — via the shared `_record_fork_entry` (`base_hash = upstream`, R2) |
| `_commit_lock_and_caches` | `_assert_safe_write` | the base-template caches **and** `cairn-lock.yml` itself — preflighted for ALL writes, then exclusively temp-staged with unpredictable names and atomically replaced, lockfile last (adopt-as-fork R4: the lockfile authority write was previously unguarded in `_cmd_adopt_module`) |
| `_self_heal_profile_config` | `_assert_safe_write` as its second statement (the first builds the path), before it looks at anything | `dev/.cairn/profile.yml`, written on `--apply` only when absent. `exists()` follows a link, so a link to a file not there yet read as absent and the write created that file wherever the link led, with lines the lockfile chose. A link at the name, or any link above it, is refused wherever it points -- an existing target and an in-project target included, the stricter rule -- and `cmd_upgrade` turns the refusal into a plain exit 2 before `_apply_upgrade` runs. The values written (preset, axis values, module names, the four tokens) must each be a non-empty printable string, else nothing is written. A line break in a value therefore cannot start a line of its own. Preset, axis values and module names are still written unquoted, as the differential oracle's frozen baseline writes them (the tokens are single-quoted), so a printable value holding `: ` or ` #` makes a profile the loader refuses to read, on that one line |
| `_write_init_lock_profile_template` | `_assert_safe_write` as its first statement after the path is built, before it looks at the project | `dev/.cairn/profile.yml`, written by `upgrade --init-lock` when no regular file is there. `is_file()` follows a link, so a link to a file not there yet read as "none" and the write created that file wherever the link led. A link at the name, or any link above it, is refused wherever it points. `_cmd_init_lock` makes that refusal first, at exit 2 (its row in Class D), so this guard backs up any other caller; called directly it raises `ScaffoldSecurityError`. Nothing is written outside the project. The text written is fixed (placeholders, axes read from the project's folders, module names from the engine's own registry); no lockfile chooses it |
| `_cmd_finalize_lockfile` | `_write_by_replacing`, which guards the lockfile's name immediately before the replace | the advanced `cairn-lock.yml`. A link at that name is refused at the write as well as by `cmd_upgrade`'s earlier check, which covers a link swapped in after it. A renamed vendor wrapper that is a link is never resolved, so no digest of a file outside the project is recorded. The failure message (exit 1, `VENDOR.md` missing on disk) also names a link at a known vendor file name such as `CLAUDE.md` and says to replace it with a regular file; a link under a custom name is not named, because telling it from any other link would mean reading it |
| `_apply_upgrade` | `_assert_safe_write` | the swapped-in upgraded files (incl. `new-core` / `new-module` additions, which share the swap loop). `cmd_upgrade` refuses a linked `.gitignore` (a `seed_gitignore` dry run, exit 2) before this runs, since an apply that adds skills seeds `.gitignore` after the swap. It also reads the staged copies, and refuses a review area that holds or sits behind a link before reading any of them (`_assert_stage_has_no_links`, Class D), and refuses a review area whose bookkeeping names a file that is not a plain relative name inside the project (Class D). The lockfile write goes through `_write_by_replacing`, so a link at the lockfile's name is refused at the write as well as at `cmd_upgrade`'s earlier check |
| `merge_module_into_slot` | `_assert_safe_write` | a module-merge slot write + its conflict side-file (final Security Review P1 #1) |
| `_write_stage` | `_assert_safe_write` | every staged-file / new-base / review-only destination, validated up-front for ALL plans (External Security review F1). `cmd_upgrade` refuses a linked `.gitignore` (a `seed_gitignore` dry run, exit 2) before this runs, since the stage seeds the review surface's ignore entry last |
| `seed_gitignore` | `_assert_safe_write` | the appended lines in `<target>/.gitignore`. A fixed path is **not** contained by construction: a checkout can make `.gitignore` a link to a file outside the tree, and the appended lines would land there. The guard runs before the read, and on `--dry-run` too, so a dry run never promises a seed the install refuses. A link is refused wherever it points, inside the tree or out: the stricter rule, "never write through a link", stays, because following an in-tree link would mean judging the final destination of a link chain in this one function. An adopter who keeps a shared `.gitignore` by link replaces the link with a regular file; every refusal says so. `main`, `upgrade --adopt-module`, `--stage` and `--apply` run the same check before their first write, so an install, dry run, adoption, stage or apply over a linked `.gitignore` stops with exit 2 and nothing written; `--plan` writes nothing and is not asked. The `--stage` and `--apply` check is unconditional, though an apply seeds only when it adds skills: a stage always seeds, so an adopter with a linked `.gitignore` cannot reach `--apply` through the normal flow anyway. The preflight checks kind and link count without reading; the append reads bytes through a regular-file descriptor and replaces through an exclusive temporary. A won parent-folder race remains under the Layer-4 threat model. |

### Fail-closed refusals added by the side-door-parity change (writes PREVENTED, not performed)

These do not write; they **refuse before a write** to close a data-loss /
facade-without-engine surface, and are listed so the inventory stays complete:

- **`assert_always_on_complete` / `missing_always_on_sources`** (R4): the
  onboarding launcher + `_onboarding/` engine are a **required completeness
  group**. Install (`install_onboarding`), lockfile write
  (`write_install_lockfile`), and upgrade advancement (`_compute_upgrade` →
  `new-core-incomplete-group`, an unconditional `--apply` block) each fail closed
  on a partial group — a present facade is never delivered/tracked/advanced over
  an absent engine member.
- **`new-core-blocked` / `new-core-lockconflict`** (R5): the new-core enumeration
  now mirrors the new-module occupied-destination split — a genuinely-new
  core/always-on add over an **occupied unlocked** destination (or one **owned by
  another lockfile source**) is a hard block, never a silent overwrite. This
  closes a data-loss surface that existed independently of onboarding (the prior
  new-core path never checked the destination).

## Class B — guarded-by-equivalent-invariant (no direct guard, contained by construction)

- **Upgrade staging** (`apply_adopter_merge`): writes go to the internal
  `dev/.cairn-upgrade/` staging subtree, an already-contained directory *inside*
  `target`; the apply swap into the live tree goes through the Class-A paths. The
  stage root is rmtree'd/recreated within `target`. (`_write_stage` itself now
  carries a **direct** Class-A guard — External Security review F1 — since a
  malformed/`..`-traversing `InstallSpec.dst` could otherwise escape the staging
  subtree and the adopter root during `--stage`, before the apply-time guard.)
- **`_emit_skill_symlink`**: its destination is guarded by
  `_assert_fanout_contained` at the `fan_out_skills` call site before it runs.
- **`_symlinks_available`**: writes/removes only a probe symlink it creates and
  immediately unlinks; fail-soft. The name is new on every call. A fixed name let a
  committed folder make the cleanup fail, which read as "no symlinks" and so chose
  the copy path above on any operating system. Creating a link never follows one and
  fails on any name already taken, so the probe can touch only the link it made. No
  guard is called: the name is fresh, directly under the install root.

## Class D — guarded reads of project data (the read side)

`upgrade` reads three paths out of every lockfile record, and the lockfile is
project data: a cloned repository can carry one somebody else wrote. A name that
leads out of its tree made `upgrade --stage` copy any file the user could read
into the review area, and `--apply` write that text into a tracked project file.
Each read is guarded **before** it happens; none of these functions writes, so
none is in the Class A write set. They are pinned by
`bootstrap/tests/test_upgrade_lockfile_path_containment.py` (call present, and
ahead of the function's first read), because the Class A set above lives in a
gate-frozen test and names write guards only.

| Function | Guard | Reads |
|---|---|---|
| `_contained_lockfile_path` | itself the guard: a non-empty relative POSIX name (no `..`, no absolute or drive form, no backslash, nothing unprintable in it -- `str.isprintable()`); for the project, a name whose first part is `.git` in any letter case is refused (Git's own folder is inside the project folder but holds no project file); then the name with every link on the way followed must still lie under its root | returns the joined path; raises `ScaffoldSecurityError` in fixed words with the escaped, cut name and a remedy line, never where a link points. The remedy fits the cause: a name that leads out through a link is told to replace the link, any other refusal to restore the record from a copy you trust |
| `_check_lockfile_paths` | `_contained_lockfile_path` for `src` (root: `templates/`), `dst` and `base_cache` (root: the project) of **every** record; and the lockfile's `modules`, which must be a list of non-empty printable strings (the report prints each) | called once, in `cmd_upgrade` right after the lockfile is read and the forked-facade advisory has run, so the report, `--stage`, `--apply`, `--finalize` and `--adopt-collisions` never see a name they would have to trust. The advisory runs first so that a lockfile about to be refused cannot hide a forked facade. It reads file bytes only through its own contained reader and prints names escaped, but it is not inert: its candidate gate stats and globs `<dst folder>/_<name>/` at a path the lockfile chose, unchecked, so a `dst` that leads outside the project lets one yes-or-no line on the operator's terminal say whether a folder of that name holding a `.py` file exists there. No byte is read and nothing is written. The frozen advisory tests pin that order; checking `dst` and `base_cache` ahead of the advisory is possible, and needs the "checked in exactly one place" pin in `test_upgrade_lockfile_path_containment.py` replaced. `cmd_upgrade` turns the refusal into a plain exit 2 and writes nothing. A field a record does not carry is not required |
| `cmd_upgrade` (the lockfile's own name) | `_refuse_if_linked`, which calls `_assert_safe_write`, on `dev/.cairn/cairn-lock.yml`, before the lockfile is read and before `--adopt-module` | the lockfile is read, and written back by `--apply` and `--finalize`, at one fixed name; a link at it (or a linked folder above it), dangling or not, is refused with exit 2 before anything is read through it. Two actions are left out: `--adopt-collisions` is skipped by it, and `--init-lock` returns before it and makes its own check (next row). Over a lockfile that is itself a link both are stopped by the lockfile reader's own refusal (`_read_regular_bytes`) instead -- a traceback and exit 1, with nothing read or written outside the project (a pinned test expects `--adopt-collisions` to propagate that refusal as an exception rather than an exit code) |
| `cmd_upgrade` (the profile's name, on `--plan`, `--stage`, `--adopt-module` and `--adopt-collisions`) | `_refuse_if_linked`, which calls `_assert_safe_write`, on `dev/.cairn/profile.yml`, in two places: ahead of the `--adopt-module` / `--adopt-collisions` branches, and, for the report and `--stage`, after the `--apply` branch has returned and before `_compute_upgrade` | the profile, read to size the upgrade under the profile the project has now (`_resolve_current_profile`, called by `_compute_upgrade`, again by `--stage`, and by `_cmd_adopt_module` for the module's tokens). A link at the name or above it, to a file that exists or to nothing, is refused with exit 2 and the remedy line `--init-lock` prints; nothing is read through it, `--stage` writes no review area, and `--adopt-module` records no token in the lockfile. Pinned by `test_plan_and_stage_refuse_a_profile_that_is_a_link` and `test_adoptions_refuse_a_profile_that_is_a_link` in `bootstrap/tests/test_upgrade_refuses_hostile_project_data.py`. Not covered, stated: `--finalize` never reads the profile, so a link there does not stop it |
| `_cmd_init_lock` | `_refuse_if_linked` on `dev/.cairn` before a lockfile is looked for, and on `dev/.cairn/profile.yml` before it is read or written | whether a lockfile exists, then the profile (the axes and tokens the new lockfile carries). A link at either name or above it, a link to a file that exists and a dangling one alike, is refused with the same exit 2 and remedy line `cmd_upgrade` prints, and nothing is read through it or changed. Pinned by the `test_init_lock_refuses_*` nodes of `bootstrap/tests/test_upgrade_refuses_hostile_project_data.py`. Not covered, stated: a link at the lockfile's own name is left to the reader's refusal (traceback, exit 1, as before); and each module file the new lockfile tracks is hashed where it stands, through a link if one stands there (measured: a linked `AGENTS.md` put the digest of the file behind it in the new lockfile, nothing written outside the project) -- only the renamed vendor wrapper is never resolved through a link |
| `_behind_by_n` | a full-match test: the saved commit must be 4 to 40 lowercase hex characters | the lockfile's `cairn_commit` goes into a `git rev-list` argument, where a leading `-` is an option (`--output=<path>` made the read-only report create a file); anything else returns the "refs not comparable" line and git is not run. The running tree's commit is not held to this, because `--to <tag>` is legitimate |
| `_apply_upgrade` (the review area's bookkeeping) | `_contained_lockfile_path` over every name in `staged_files`, `review_only`, `module_blocked`, `expected_absent` and every key of `kinds` and `new_entries`; `new_commit` and `new_version` must be printable strings | before any of it is printed or used. A review area is project data, and a repository can carry one whose names would reach the terminal raw or lead outside the project. The refusal prints none of what it found |
| `_theirs_text`, `_theirs_bytes` | `_contained_lockfile_path` as the first statement | the upstream template: `templates/<src>`, or `git show <ref>:templates/<src>`. The primitive is guarded as well as the command, so a caller that builds a `src` some other way cannot read outside `templates/` |
| `_assert_stage_has_no_links` | `_assert_safe_write` on the review area, then a walk that refuses any link inside it | `_apply_upgrade`: the staged copies and new-base copies. A repository can carry the (normally ignored) review area, and `--apply` read a staged copy through a planted link |

*Read versus write.* A read judges where the name **ends up**: a link that stays
inside the project is not refused. A write still refuses any link at the name or
above it (`_assert_safe_write`). The review area is the exception, because
nothing legitimate ever puts a link there.

*Terminal.* `dst` is printed in the upgrade report, so a control character in a
lockfile name would be typed at the operator's terminal. The shape check refuses
any unprintable character (both control ranges, line and paragraph separators,
format characters), and the refusal prints the name escaped and cut to 100
characters.

*Not covered, stated.* A name the engine builds itself -- the renamed vendor
wrapper (`CLAUDE.md` for `VENDOR.md`) -- is not in the lockfile. A link is never
taken for the wrapper (`_resolve_vendor_wrapper` tests `is_symlink()` in both
tiers before any read), because the wrapper's digest is recorded in the
lockfile by `--finalize`; a regular file is read as it is, and its content
reaches a write only through `_write_stage`, which refuses a linked destination.
"Inside the project" means the project folder: ignored and untracked files are
included, and only `.git/` at the root is set apart. The name of the saved
ancestor that `--apply` records for a newly added file is derived from the
destination (as `_compute_upgrade` derives it), not read back from the staged
record, so a hand-built review area cannot make the apply read or record a path
outside the project.

## Class C — documented follow-up gaps (the deferred single-write-capability redesign, RR6/SR6)

The `upgrade`-family CLI commands that write profile / lockfile / base-cache
files compute destinations from the lockfile and the resolved `target` but do
**not** currently call `_assert_safe_write`: `cmd_update_profile`,
`cmd_init_lock`, `cmd_rebase`, `cmd_verify`, `cmd_drift`, `cmd_complete_merge`.
These are operationally-trusted post-install maintenance paths (the adopter runs
them in their own tree); routing **all** adopter-tree writes through one audited
write capability is a **behavioral** change, deliberately scoped to a **separate
follow-on proposal** (RR6/SR6), not this pure-motion split. This split only
*inventories* them; it does not re-route them.

**Status of the follow-on, as of 2026-08-04 (residual R7 of
`fork-advisory-semantics`) — OWNED, and R7 discharged.** The RR6/SR6 follow-on
named above is **claimed by `fork-advisory-semantics` (scope 3)**, by
Maintainer ruling on 2026-08-04. It lands as additional chunks on that plan
after its current chunks commit; the plan's scope is not reopened to take it.

*How it got here, since the history is the point of this row.* The superseding
Decision carried Class C forward "as a candidate for scope 1 or scope 3, at the
drafting author's judgment", and **each of those two declined it, with a stated
reason**: `release-authenticity` (scope 1) and `fork-advisory-semantics` (scope
3). The other two `identity-not-name` successor scopes were never offered it
and recorded no decline. So it was, for a time, claimed by none of the four —
which is why R7 existed. Both drafting authors recommended ratifying it as its
own proposal; the Maintainer instead **ratified the departure and overruled
scope 3's decline**.

Three triggers discharged this residual, the first to occur: **(a)** the
Maintainer's ratification at the first successor Decision, which either opens
Class C as its own proposal or assigns it; **(b)** the next change that adds or
modifies an adopter-tree write in `upgrade.py` — the condition the closing line
below already names; **(c)** backstop, v0.4.0 release preparation, at which
point it is opened cold or explicitly closed as won't-fix with a reason.
**Trigger (a) fired**: the ruling assigns it. R7 is discharged and no longer
the only thing holding this item.

**This classification is the SR6 deliverable; Class A is the pinned regression
surface. Re-take the inventory if a future stage adds an adopter-tree write.**
