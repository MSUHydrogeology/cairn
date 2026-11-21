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

## Plan review -- Reviewer (Sonnet 5.5) -- 2026-11-21

```
Reviewed commit: 984fcaf7190d3f7a4265a972e20169607aa3a599
```

**Obligation**: usual plan review (Internal)
**Tier**: Internal
**Findings**: raised

**Verdict**: REVISE. Two blocking findings; the design is sound.

**Foundations**

1. **Should this happen as framed?** Yes. The owner and access-list test lives only in `check_acl` (`dev/tools/meter.py` 626-678); the plan's five project sites are every project caller, and the log, consent and private-record callers keep their roles (744-775, 2176, 4056-4369, 5168-5352).
2. **Best alternative.** The early return in `check_acl` is the simplest path; no simpler one found (`meter.py` 626).
3. **What would show it wrong.** One missed `"ancestor"` site: the real refresh on the `F:` machine would still refuse. That is Strategy's check; no test shows the five sites pass `"project"`.

**What still holds without the test (read in code):** (a) no-follow opens and reparse refusal, 415 and 456; identity re-checks, 1713-1721 and 5752-5791. (b) Windows: private candidate, `"export"` owner and protected-ACL checks, rename by handle, 5731 and 5739-5831; Mac and Linux: owner, mode 0o600, one link, 5598-5635. (c) 5927 and 5932 (the bytes run are the bytes hashed). (d) `_project_for_folder` compares text only, 6370.

**Blocking**

1. The test stand-in has no access entry: its list is `struct.pack("<BBHH", 2, 0, 8, 0)`, count 0 (`tests/integration/test_meter.py` 8886), so the "entry giving another account full control" case cannot be added as written. `"project"` returns before reading anything. Replace the criterion's test text with: add to `cases` at 8907 `("project", 2, True), ("project", 5, True), ("ancestor", 2, False)`.
2. A sentence that states the old rule is not listed: `dev/rules/development-environment.md` 135-137, "The meter's project `.git/config` read (... role `ancestor`) refuses a project under such a folder, so a real meter read there reports `project_remote_unavailable`." The search skipped `dev/rules/`. Replace it with: "Before the v0.8.1 change, the meter's project `.git/config` read refused a project under such a folder (`check_acl`, role `ancestor`, `project_remote_unavailable`). A project's folders are no longer tested; the refusal still applies to log folders." Add the file to the stale list.

**Non-blocking**

- Say plainly that `"project"` also drops the test for the drive root and every folder above the project, and in `_git_helper_source` for every folder above the meter's own file (`source_path.parent`), which need not be in a project. The SHA-256 test (5927) is what protects the helper's bytes.
- Give the nine direct lines: 2480, 2487, 5722, 5723, 5760, 5770, 5784, 6098, 6111, not "28 lines".
- Give the shim: `def open_source_root(api_instance, root, user_sid, role="ancestor"):` and both returns `original_open_root(api_instance, root, user_sid, role)`.
- Give the Mac and Linux test lines, after 5455: `for folder in (alpha, alpha / "dev", alpha / "dev" / "measurement"): folder.chmod(0o777)`.
- Add: "The build does not attempt Strategy's check."
- No Windows test plants a link at a project; the shared `_windows_open_root` refusal is shown by the native log-folder case. Accepted.

**Not covered:** no test run; no Security Review questions (group-write on Mac and Linux, the receipt wording); fixtures `promise_security_leaf_*` not read.

Elapsed time: unknown. Tokens: unknown.
