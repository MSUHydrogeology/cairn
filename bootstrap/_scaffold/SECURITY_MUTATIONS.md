<!-- claim-check-allow: bootstrap/_scaffold/, bootstrap/_scaffold/security.py, bootstrap/_scaffold/__init__.py -->

# SR6 — adopter-tree mutation inventory (scaffold-split Stage 1)

Every write/removal the scaffold engine performs **into an adopter's target
tree** must route its destination through a containment guard before touching
disk. The guards are the Stage-1 leaf `bootstrap/_scaffold/security.py`:

- **`_assert_safe_write(dst, target)`** — ordinary writes; refuses a symlinked
  destination, a symlinked parent, or a path resolving outside `target`.
- **`_assert_fanout_contained(dst, target)`** — the skills fan-out; like the
  above but permits `dst` itself to be the (re)created symlink.

Both raise the single **`ScaffoldSecurityError`** identity, caught once at the
CLI top level (exit 2).

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
| `install_onboarding` | `_assert_safe_write` | the always-on launcher + `_onboarding/` engine (installed FROM `_ALWAYS_ON_MAPPINGS`, the SSOT `install_manifest`/`scan_targets` also consume), activation log, PLANNING slot, preset source, onboarding docs. **Fail-closed before any write** on an incomplete launcher+engine completeness group (`assert_always_on_complete`, R4) |
| `write_install_lockfile` | `_assert_safe_write` | base-template cache, `cairn-lock.yml`. **Refuses (returns `None`)** before any write on an incomplete always-on completeness group (R4 — a partial group must not yield a lockfile tracking only the present members) |
| `_emit_skill_copy_fallback` | `_assert_fanout_contained` | regenerated canonical skill copy, diverged-copy quarantine |
| `fan_out_skills` | `_assert_fanout_contained` | vendor fan-out destination |
| `_cmd_adopt_module` | `_assert_safe_write` | a single added module's files (missing-dst install); the base-cache + lockfile writes route through `_commit_lock_and_caches` |
| `_cmd_adopt_collisions` | `_assert_safe_write` | the adopted collision's destination (containment re-check; never written); the base-cache + lockfile writes route through `_commit_lock_and_caches`. Resolves the adoptable occupied-destination collisions in **either** tier — module-internal (`new-module-blocked`) **and** core/always-on (`new-core-blocked`, side-door parity R5) — via the shared `_record_fork_entry` (`base_hash = upstream`, R2) |
| `_commit_lock_and_caches` | `_assert_safe_write` | the base-template caches **and** `cairn-lock.yml` itself — preflighted for ALL writes, then temp-staged + atomically replaced, lockfile last (adopt-as-fork R4: the lockfile authority write was previously unguarded in `_cmd_adopt_module`) |
| `_apply_upgrade` | `_assert_safe_write` | the swapped-in upgraded files (incl. `new-core` / `new-module` additions, which share the swap loop) |
| `merge_module_into_slot` | `_assert_safe_write` | a module-merge slot write + its conflict side-file (final Security Review P1 #1) |
| `_write_stage` | `_assert_safe_write` | every staged-file / new-base / review-only destination, validated up-front for ALL plans (External Security review F1) |

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
  immediately unlinks; fail-soft, no caller-controlled path.
- **`seed_gitignore`**: read-then-append on the fixed `target/.gitignore`.

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
