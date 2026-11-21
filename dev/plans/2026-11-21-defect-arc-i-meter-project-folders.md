# Plan: Defect arc I, the meter does not judge a project's folders

**Source proposal**: dev/proposals/archive/2026-11-20-claude-v09-defect-arc.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-21
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/working-agreements.md, dev/rules/conventions.md, dev/rules/development-environment.md
**In brief**: The usage meter will stop refusing a project because of who may change the project's folders, so it runs on a drive shared on purpose, while it still refuses a link or a redirected folder on the way to the project.

## Build summary

The meter refuses the Maintainer's Windows project because its drive is open to the Users group. After this plan it no longer asks who owns a project's folders or who else may change them. Ships in v0.8.1.

## Source proposal

The accepted defect arc takes in later defects. Asked whether to tighten the drive, the Maintainer wrote: "Leave it. F: permissions are exactly what I want them to be", then "Why would meter usage depend at all on the F: permissions?", and to the change: "Yes, change it".

## Scope

**Today.** On Windows `check_acl` with the role `"ancestor"` refuses a folder or file owned by another account (the user, SYSTEM, Administrators and TrustedInstaller excepted) or whose access list lets another account write. A project's tree meets it in four places: `_windows_project_config`, `_capture_windows_project_claims`, `_windows_atomic_write_project_export` and `_git_helper_source` (it reads `git_read.py` from inside the project). Measured on the Windows Server machine, in memory: skipping it in those four places gives a real refresh `ok`. On Mac and Linux only `_posix_project_directory_snapshot` judges folders, refusing one that another account owns or that group or others may write.

**Kept:** every check on the consent file, the log folders and the private record. On a project's tree: no link or redirected folder (each part opened without following, a reparse point refused); same volume or device; identities unchanged across the operation; `.git` a plain folder with a `config` of one name; the remote check; the summary private, owned by the user, with one name, written to a candidate and renamed. **Removed:** the owner and who-else-may-change test on a project's tree.

**Windows, as code.** A role `"project"` for which `check_acl` makes no owner or access-list test:

```python
# check_acl, first statement
if role == "project":
    return
# _windows_open_root: both check_acl calls use role
def _windows_open_root(api, root, user_sid, role="ancestor"):
# _WindowsApprovedLineStream
def __init__(self, root, relative, budget, api, user_sid, *, role="ancestor", **options):
    super().__init__(root, relative, budget, **options)
    self.api, self.user_sid, self.role = api, user_sid, role
# its _open_root passes self.role; its seven check_acl(..., "ancestor")
# calls (in __iter__ and _capture_windows_final) use self.role
# _git_helper_source
stream = _WindowsApprovedLineStream(..., api, user_sid, role="project")
# the three project functions: _windows_open_root(..., "project"), and each
# direct check_acl(..., "ancestor") on a project folder or file -> "project"
```

That is 28 lines. `"export"` calls and every other caller keep their roles.

**Mac and Linux, as code.** Two lines become one; the returned tuple is unchanged, so a change mid-write is still caught:

```python
if not stat.S_ISDIR(info.st_mode) or (device is not None and info.st_dev != device):
    raise Unavailable("project_export_unavailable")
```

**For the Security Review.** The removed test guarded against another account changing a folder the meter uses. A redirect is still stopped: each part is opened without following, handles stay held and identities are re-checked (a change gives `source_changed`). The summary stays private: owned by the user, one name, renamed into place. The helper runs only if its SHA-256 equals the meter's constant. Usage comes from the logs; a record counts only when the folder it names is inside the project. An account that may change the project can still make the remote check fail (usage goes unassigned), change the split of usage between plans by editing the claims file, or delete the summary; it can already do each to the project's own files. Nothing changes for the consent file, logs or private record.

Not in this plan: the log folders' access test, and the weights index.

**Reuse.** The existing role mechanism; no other project caller of `check_acl(` exists.

### Documentation / doctrine surface

No doctrine surface. A search of the measurement README, `dev/modules/`, `install/SAFETY.md`, `docs/` and `templates/` found no sentence stating the old rule. The measurement README gains, before "To refresh and render the complete pulse": "The Meter does not judge who else may change a project's folders. It refuses a link or a redirected folder on the way to them, and it makes its summary file private. On a project that others may change, the remote check and the work claims are only as sound as that folder."

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Tests, code, shipped copy, README, changelog, lock | plan review | v0.8.1 |

Code review once after C1.

## Acceptance criteria

**C1.** (a) The code above is in `dev/tools/meter.py`. (b) In `tests/integration/test_meter.py`, no new function: `test_windows_profile_owner_may_be_system_or_administrators` gains two cases (its stand-in carries one access entry): `"project"` accepts an owner that is another account and an entry giving another account full control; `"ancestor"` still refuses both. `test_public_refresh_repeat_and_rebuild_publish_distinct_project_exports` (Mac and Linux) makes the project, `dev` and `dev/measurement` group- and other-writable and still expects the summary written. The shim `open_source_root` (near line 1087) forwards the role. (c) `cmp` of the shipped copy prints nothing.

**Existing refusals.** A search of `tests/` for `project_export_unavailable`, `project_remote_unavailable` and writable or foreign-owned project folders found no test that holds the old refusal; `test_windows_project_export_rechecks_directory_acl_before_replace` injects its own and stays. A redirect at `dev/measurement` is still refused: `test_posix_project_export_refuses_missing_or_linked_parents` shows it on Mac and Linux. No Windows test plants one at a project; the refusal (`_WindowsConsentAPI.info`, unchanged) is shown for a log folder by the native `entry-and-parent-reparse` case.

**Strategy's check, not the build's.** On the Windows Server machine `meter.py refresh --json` answers `ok` and files usage under the project.


## Scope delta

**Scope delta**: preserved

## Verification

Change the tests first and run only the two above once (they fail); change the code and run them once more (they pass): the Windows one here, the other in the Linux subsystem. The shim edit waits for certification.

**What goes stale.** The shipped copy (`cp`, then `cmp`). Cairn's own lock, by `install/scaffold.py upgrade --target . --finalize <paths>`, alone in its commit. One `Fixed` line under `Unreleased` in `CHANGELOG.md`: the meter no longer refuses a project because of who owns or may change its folders. The `test_meter.py` hash in the gate manifest, a line at the Maintainer's signing. Run `dev/tools/claim_check.py` on the README and this plan.
