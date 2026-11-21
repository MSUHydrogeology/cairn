# Plan: Defect arc G, the meter runs for a Windows administrator

**Source proposal**: dev/proposals/archive/2026-11-20-claude-v09-defect-arc.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-21
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/working-agreements.md, dev/rules/conventions.md, dev/rules/development-environment.md
**In brief**: The usage meter will accept a Windows profile folder owned by the Administrators group or the system, which is what Windows makes for an administrator's account, so it stops answering `unavailable` on such machines.

## Build summary

On a Windows Server machine every meter command answers `unavailable`: the profile folder is owned by the Administrators group and the meter wants the user's own account. After this plan the meter also accepts the system or the Administrators group as owner of the profile folder only. One condition in `dev/tools/meter.py` changes, with its shipped copy, one test and one changelog line, for v0.8.1.

## Source proposal

The accepted defect arc takes in defects found since. Asked whether to fix the meter or change the folder's owner, the Maintainer wrote: "Fix the meter". The usage-counting plan (branch `usage-impl`) changes the same file and merges first; this plan is built on the merged tree, and the build agent re-reads the lines named here.

## Scope

**The change.** In `check_acl` (`dev/tools/meter.py`), the owner test becomes:

```python
if role == "profile":
    if owner_bytes != user_sid and not self._privileged_sid(owner_bytes, ancestor=False):
        raise Unavailable
elif role in {"cairn", "config", *private_roles} and owner_bytes != user_sid:
    raise Unavailable
```

`_privileged_sid(..., ancestor=False)` matches only SYSTEM (`S-1-5-18`) and Administrators (`S-1-5-32-544`), the two accounts the meter already trusts in an access list. Any other owner is refused.

**Why it is safe.** Those two accounts may already hold full control of the profile folder under today's rule, and an administrator can take ownership of any folder, so this gives no account a power it lacks.

**What stays.** The `.cairn` folder, the consent file and every private file the meter makes must still be owned by the user. The profile folder's access-list test is untouched. The POSIX check is untouched. No new tooling.

**Other places** (searched `"profile"`, `check_acl(` and `owner` in `meter.py`; read, not run). The profile folder's owner is tested in one place, the line above. The role `profile` is set once, in `read_config`; the ledger and export writers re-check the folders it held with those same roles, so they gain the rule with no edit. The source-root walk, the project-claims walk and the writers' own directory checks use the role `ancestor`, which already accepts SYSTEM and Administrators as owner. None needs a different rule.

**Reuse.** `_privileged_sid`, found by searching `meter.py`; the `ancestor` test uses it the same way.

### Documentation / doctrine surface

No doctrine surface. `dev/measurement/README.md` states no owner rule, so no sentence there changes.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Owner test, one test, shipped copy, changelog, lock | plan review | v0.8.1 |

Code review once after C1.

## Acceptance criteria

**C1.** (a) The condition above is in `check_acl`. (b) One permanent test in `tests/integration/test_meter.py`, the file whose tests drive the Windows consent check with stand-ins (all replace `check_acl`). It builds `object.__new__(meter._WindowsConsentAPI)` with a stand-in `advapi` whose `GetSecurityInfo` returns a chosen owner and an empty access list, and stand-ins for `_sid_bytes` and `_privileged_sid` (true for `b"admins"` only, recording `ancestor=False`). Case 1: role `profile`, owner `b"admins"`, user `b"user"`: returns. Case 2: role `profile`, owner `b"other"`: raises `Unavailable`; role `cairn`, owner `b"admins"`: raises `Unavailable`. Case 1 fails before the change. (c) `cmp dev/tools/meter.py templates/skills/_lib/meter.py` prints nothing.

**Strategy's check, not the build's.** On the Windows Server machine the meter stops answering `unavailable`. The build agent must not attempt it or run the meter.

## Scope delta

**Scope delta**: preserved

## Verification

Run once, on Windows: `C:\ProgramData\Anaconda3\python.exe -m pytest tests/integration/test_meter.py -q`. Nothing else.

**What goes stale, and who refreshes it.** The build agent refreshes the first three; the Maintainer does the fourth.
- Shipped copy: `cp dev/tools/meter.py templates/skills/_lib/meter.py`, then `cmp` prints nothing.
- Cairn's own lock: `C:\ProgramData\Anaconda3\python.exe install/scaffold.py upgrade --target . --finalize dev/tools/meter.py`, in a commit holding only the lock.
- Changelog: one `Fixed` line under `Unreleased` in `CHANGELOG.md`.
- Gate manifest: `tests/fixtures/gate_manifest.json` holds a hash of `test_meter.py`; the edit leaves one HOLD, a line added to the Maintainer's next signing.

Run `dev/tools/claim_check.py` on prose changed.

## Plan review -- Reviewer (usual) -- 2026-11-21

Reviewed commit: 328325bb665c671f7057f0f088b99de19e989b38

**Obligation**: the usual plan review
**Tier**: Internal
**Findings**: raised

**Foundations**:

1. **Should this happen as framed?** Yes: the design is sound. Under today's rule the access-list loop already skips SYSTEM and Administrators, so they may hold full control of the profile folder; owning it adds no power an administrator cannot take -- `dev/tools/meter.py` lines 629-666.
2. **Best alternative.** None simpler: the Maintainer chose "Fix the meter"; one condition at the one place the role `profile` is set -- `meter.py` line 741, `dev/PLANNING.md` section 1 entry.
3. **What would show it wrong.** On the real machine another refusal appears, such as an extra access-list entry that holds write rights on the profile folder -- Strategy's check, after the build.

**Findings**

1. **Blocking: the test is not given as code.** A low-tier builder must invent the stand-in: `check_acl` writes owner, access list and descriptor through `C.byref`, calls `C.string_at` on the access list, and uses `kernel.LocalFree`. Replace Acceptance (b)'s description with the test as code: `api = object.__new__(meter._WindowsConsentAPI)`; set `api.C = ctypes`, `api.W = ctypes.wintypes`, `api.kernel` with a no-op `LocalFree`, and `api.advapi.GetSecurityInfo` setting `owner._obj.value`, `dacl._obj.value` (the address of a buffer holding the 8 bytes `02 00 08 00 00 00 00 00`) and `sd._obj.value` to non-zero, returning 0; `api._sid_bytes = lambda p: owners[0]`. Then the three cases with `user_sid=b"user"`. The author must confirm that code against `check_acl` lines 619-671.
2. Non-blocking: add case "role `profile`, owner `b"user"`: returns", so "too strict" is also caught.
3. Non-blocking: "all replace `check_acl`" is not exact; the fault harness near test line 964 wraps the real one. Say "most".
4. Non-blocking: state that a second refusal on the machine goes back to Strategy; the build does not widen the access-list test.

Checked and right: `check_acl` has 45 call sites (`grep -c "check_acl(" dev/tools/meter.py` gives 46 with the definition); roles `meter`, `ledger`, `lock`, `candidate`, `export`, `cairn`, `config` stay user-owned; every walk and writer passes `ancestor`. Stale records are complete: shipped copy, `dev/.cairn/cairn-lock.yml`, the manifest hash of the test file (`tests/fixtures/gate_manifest.json` line 8457), changelog. The Strategy-only check is stated.

**Verdict**: REVISE

Not covered: the Security Review questions, any run, and the real machine's access lists. Elapsed time: unknown. Tokens: unknown.
