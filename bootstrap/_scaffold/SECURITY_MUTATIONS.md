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
and `--apply`, `--stage` and `--adopt-collisions` around their own writes.
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
| `_install_one` | `_assert_safe_write` | each installed template file |
| `write_local_env` | `_assert_safe_write` | `dev/.cairn/local-env.json` |
| `create_dev_tree` | `_assert_safe_write` | the empty `dev/` folder set. `mkdir(parents=True)` follows a link, so every destination is checked before the first `mkdir`: a linked `dev/`, or a linked folder below it, refuses with nothing created at either end |
| `install_onboarding` | `_assert_safe_write` | the always-on launcher + `_onboarding/` engine (installed FROM `_ALWAYS_ON_MAPPINGS`, the SSOT `install_manifest`/`scan_targets` also consume), activation log, PLANNING slot, preset source, onboarding docs. **Fail-closed before any write** on an incomplete launcher+engine completeness group (`assert_always_on_complete`, R4) |
| `write_install_lockfile` | `_assert_safe_write` | base-template cache, `cairn-lock.yml`. **Refuses (returns `None`)** before any write on an incomplete always-on completeness group (R4 — a partial group must not yield a lockfile tracking only the present members) |
| `_emit_skill_copy_fallback` | `_assert_safe_write` | regenerated canonical skill copy, diverged-copy quarantine. A copy name is not contained by construction: a checkout can plant a link at it (a dangling one creates a file outside the tree), a link at the quarantine name (`shutil.move` moves a file *into* the folder it names) or a link to a file that already holds the canonical bytes (the copy rewrites it in place). Every copy and quarantine name is guarded for the whole set, and anything but a free name or a plain file at a name, or a file where a folder must go, is refused, all before the first write, so a refusal leaves nothing half-done. Each copy is written to a new exclusive sibling and renamed into place, and the quarantine is `os.replace`, so a link that appears after the check is replaced, not followed. A refusal is fixed words, the escaped project-relative name and a remedy line (run `session-start` or install again, because an upgrade does not redo the fan-out when run again), never where a link points; the divergence warning names the quarantined files the same escaped, project-relative way. Two windows remain, each needing a process already running on the machine, which is the model `bootstrap/SAFETY.md` accepts: a parent folder swapped for a link between the check and the write (the copy or a temporary file can land outside), and the temporary file swapped for a link between its write and the rename (that link ends up at the copy's name; nothing is written outside, and the next install refuses it) |
| `fan_out_skills` | `_assert_fanout_contained` | vendor fan-out destination |
| `_cmd_adopt_module` | `_assert_safe_write` | a single added module's files (missing-dst install); the base-cache + lockfile writes route through `_commit_lock_and_caches`. A `seed_gitignore` dry run before the first write refuses a linked `.gitignore` (exit 2) ahead of the lockfile commit |
| `_cmd_adopt_collisions` | `_assert_safe_write` | the adopted collision's destination (containment re-check; never written); the base-cache + lockfile writes route through `_commit_lock_and_caches`. Resolves the adoptable occupied-destination collisions in **either** tier — module-internal (`new-module-blocked`) **and** core/always-on (`new-core-blocked`, side-door parity R5) — via the shared `_record_fork_entry` (`base_hash = upstream`, R2) |
| `_commit_lock_and_caches` | `_assert_safe_write` | the base-template caches **and** `cairn-lock.yml` itself — preflighted for ALL writes, then temp-staged + atomically replaced, lockfile last (adopt-as-fork R4: the lockfile authority write was previously unguarded in `_cmd_adopt_module`) |
| `_apply_upgrade` | `_assert_safe_write` | the swapped-in upgraded files (incl. `new-core` / `new-module` additions, which share the swap loop). `cmd_upgrade` refuses a linked `.gitignore` (a `seed_gitignore` dry run, exit 2) before this runs, since an apply that adds skills seeds `.gitignore` after the swap. It also reads the staged copies, and refuses a review area that holds or sits behind a link before reading any of them (`_assert_stage_has_no_links`, Class D) |
| `merge_module_into_slot` | `_assert_safe_write` | a module-merge slot write + its conflict side-file (final Security Review P1 #1) |
| `_write_stage` | `_assert_safe_write` | every staged-file / new-base / review-only destination, validated up-front for ALL plans (External Security review F1). `cmd_upgrade` refuses a linked `.gitignore` (a `seed_gitignore` dry run, exit 2) before this runs, since the stage seeds the review surface's ignore entry last |
| `seed_gitignore` | `_assert_safe_write` | the appended lines in `<target>/.gitignore`. A fixed path is **not** contained by construction: a checkout can make `.gitignore` a link to a file outside the tree, and the appended lines would land there. The guard runs before the read, and on `--dry-run` too, so a dry run never promises a seed the install refuses. A link is refused wherever it points, inside the tree or out: the stricter rule, "never write through a link", stays, because following an in-tree link would mean judging the final destination of a link chain in this one function. An adopter who keeps a shared `.gitignore` by link replaces the link with a regular file; every refusal says so. `main`, `upgrade --adopt-module`, `--stage` and `--apply` run the same check before their first write, so an install, dry run, adoption, stage or apply over a linked `.gitignore` stops with exit 2 and nothing written; `--plan` writes nothing and is not asked. The `--stage` and `--apply` check is unconditional, though an apply seeds only when it adds skills: a stage always seeds, so an adopter with a linked `.gitignore` cannot reach `--apply` through the normal flow anyway The write itself is `write_text` after the guard, which leaves a small check-to-write window at the last name: the same window `bootstrap/SAFETY.md` already accepts for engine writes (the skill copies, by contrast, are written by rename) |

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
| `_contained_lockfile_path` | itself the guard: a non-empty relative POSIX name (no `..`, no absolute or drive form, no backslash, nothing unprintable in it -- `str.isprintable()`), then the name with every link on the way followed must still lie under its root | returns the joined path; raises `ScaffoldSecurityError` in fixed words with the escaped, cut name and a remedy line, never where a link points |
| `_check_lockfile_paths` | `_contained_lockfile_path` for `src` (root: `templates/`), `dst` and `base_cache` (root: the project) of **every** record | called once, in `cmd_upgrade` right after the lockfile is read and the forked-facade advisory has run (the advisory reads names only through its own contained reader and prints them escaped, so a lockfile about to be refused cannot hide a forked facade), so the report, `--stage`, `--apply`, `--finalize` and `--adopt-collisions` never see a name they would have to trust. `cmd_upgrade` turns the refusal into a plain exit 2 and writes nothing. A field a record does not carry is not required |
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
wrapper (`CLAUDE.md` for `VENDOR.md`) -- is not in the lockfile and is read
through whatever the project made it; its content reaches a write only through
`_write_stage`, which refuses a linked destination. The name of the saved
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
