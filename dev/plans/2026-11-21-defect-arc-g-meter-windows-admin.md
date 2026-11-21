# Plan: Defect arc G, the meter runs for a Windows administrator

**Source proposal**: dev/proposals/archive/2026-11-20-claude-v09-defect-arc.md
**Status**: ready-to-implement
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

**The consent folder and file on the Maintainer's machine** (measured by Strategy with `Get-Acl`, 2026-11-21): both are owned by his own account, so the roles `cairn` and `config` do not refuse there, and this plan does not widen them. A user who made the consent folder or file from an administrator shell may find them owned by the Administrators group and still get `unavailable`; `dev/measurement/README.md` gains one sentence for that user. If the real machine shows a second refusal of another kind, it goes back to Strategy; the build does not widen the access-list test.

**Other places** (searched `"profile"`, `check_acl(` and `owner` in `meter.py`; read, not run). The profile folder's owner is tested in one place, the line above. The role `profile` is set once, in `read_config`; the ledger and export writers re-check the folders it held with those same roles, so they gain the rule with no edit. The source-root walk, the project-claims walk and the writers' own directory checks use the role `ancestor`, which already accepts SYSTEM and Administrators as owner. None needs a different rule.

**Reuse.** `_privileged_sid`, found by searching `meter.py`; the `ancestor` test uses it the same way.

### Documentation / doctrine surface

No doctrine surface. `dev/measurement/README.md` states no owner rule today. It gains one sentence, right after the sentence that begins "Keep the config and private ledger": "On Windows the Meter runs only when `.cairn` and `meter.json` are owned by your own account; if you made them from an administrator shell, make your account their owner."

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Owner test, one test, shipped copy, changelog, lock | plan review | v0.8.1 |

Code review once after C1.

## Acceptance criteria

**C1.** (a) The condition above is in `check_acl`. (b) One permanent test in `tests/integration/test_meter.py`: the function `test_windows_profile_owner_may_be_system_or_administrators`, appended exactly as the Security Review gives it below under "The test, as code". It runs the real `_privileged_sid`, so a wrong list of accounts fails it. Seven cases: the profile folder owned by the user, by the system or by Administrators is accepted; owned by another account or by TrustedInstaller it is refused; the consent folder or the consent file owned by Administrators is refused. The system and Administrators cases fail before the change. (c) `cmp dev/tools/meter.py templates/skills/_lib/meter.py` prints nothing.

**Strategy's check, not the build's.** On the Windows Server machine the meter stops answering `unavailable`. The build agent must not attempt it or run the meter.

## Scope delta

**Scope delta**: preserved

## Verification

Run once, on Windows, the one new test: `C:\ProgramData\Anaconda3\python.exe -m pytest tests/integration/test_meter.py -q -k test_windows_profile_owner_may_be_system_or_administrators`. Nothing else: that file fails many of its other tests on this machine by itself, and they do not touch this change.

**What goes stale, and who refreshes it.** The build agent refreshes the first three; the Maintainer does the fourth.
- Shipped copy: `cp dev/tools/meter.py templates/skills/_lib/meter.py`, then `cmp` prints nothing.
- Cairn's own lock: `C:\ProgramData\Anaconda3\python.exe install/scaffold.py upgrade --target . --finalize dev/tools/meter.py dev/measurement/README.md`, in a commit holding only the lock (leave the README out of the command if the lock does not record it).
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

## Plan review -- Security Review -- 2026-11-21

Reviewed commit: fc060059

**Obligation**: the Security Review at the plan stage
**Tier**: Internal Security Review
**Findings**: raised

**Foundations**:

1. **What the owner test guards.** An owner can always rewrite a folder's access list. Requiring the user as owner stops another ordinary account from doing that and planting `.cairn`. SYSTEM and Administrators already pass the access-list loop, so letting them own the profile adds nothing -- `dev/tools/meter.py` lines 629, 660-661.
2. **The consent file stays the user's.** `.cairn` and `meter.json` still need the user as owner, and the meter does not create them on Windows -- `meter.py` lines 755, 763; `grep -n '"\.cairn"' dev/tools/meter.py`.
3. **The pair is exact.** `ancestor=False` gives only `S-1-5-18` and `S-1-5-32-544`. It compares the owner's identity, not group membership, so a domain group such as Domain Admins stays refused -- `meter.py` lines 386-400.

I agree with the usual review's Foundations and findings 2-4. For its finding 1, the code below governs.

**Findings**

1. **Blocking: a second refusal is likely.** An administrator whose new files are owned by Administrators probably created `.cairn` and `meter.json` the same way, and roles `cairn` and `config` still require the user. Add to Scope: "Before the build, Strategy asks the Maintainer to run `(Get-Acl $HOME\.cairn).Owner` and `(Get-Acl $HOME\.cairn\meter.json).Owner`. If either names Administrators, the build waits for his Decision: change those owners to his account, or widen this plan to the roles `cairn` and `config`."
2. **Blocking: the stand-in hides the SID list.** The plan replaces `_privileged_sid`, so a wrong SID list or `ancestor=True` would still pass. Use the test below, which runs the real `_privileged_sid`.
3. Non-blocking: TrustedInstaller stays out of the profile rule. No profile is owned by it.

Not covered: the real machine, any run, the POSIX path. Elapsed time: unknown. Tokens: unknown.

**Verdict**: REVISE

### The test, as code (for Acceptance (b))

Append to `tests/integration/test_meter.py`; it needs no new import.

```python
def test_windows_profile_owner_may_be_system_or_administrators():
    acl = ctypes.create_string_buffer(struct.pack("<BBHH", 2, 0, 8, 0), 8)
    sids = {1: b"user", 2: b"other", 3: b"system", 4: b"admins", 5: b"trusted"}
    names = {"S-1-5-18": 3, "S-1-5-32-544": 4,
             "S-1-5-80-956008885-3418522649-1831038044-1853292631-2271478464": 5}
    state = {}

    class Advapi:
        def GetSecurityInfo(self, _handle, _kind, _info, owner, _group, dacl, _sacl, sd):
            owner._obj.value = state["owner"]
            dacl._obj.value = ctypes.addressof(acl)
            sd._obj.value = 99
            return 0

        def ConvertStringSidToSidW(self, text, out):
            out._obj.value = names[text]
            return 1

    api = object.__new__(meter._WindowsConsentAPI)
    api.C, api.W = ctypes, SimpleNamespace()
    api.advapi, api.kernel = Advapi(), SimpleNamespace(LocalFree=lambda _p: None)
    api._sid_bytes = lambda sid: sids[sid.value]
    cases = [("profile", 1, True), ("profile", 3, True), ("profile", 4, True),
             ("profile", 2, False), ("profile", 5, False),
             ("cairn", 4, False), ("config", 4, False)]
    for role, owner, allowed in cases:
        state["owner"] = owner
        if allowed:
            api.check_acl(7, b"user", role)
        else:
            with pytest.raises(meter.Unavailable):
                api.check_acl(7, b"user", role)
```

Before the change, the profile cases with SYSTEM and Administrators raise, so the test fails. If the rule is too loose, the cases for another account or TrustedInstaller fail.

## Plan response -- Claude Fable 5.2 (Strategy, for the author) -- 2026-11-21

Both reviews are folded once; status is now `ready-to-implement`.

Usual review:
1. Blocking 1 (the test is not given as code): closed with the Security Review's test, which governs; criterion (b) now names it.
2. Non-blocking 2 (a case for the user as owner): it is in that test.
3. Non-blocking 3 ("all replace `check_acl`"): the sentence is gone with the old criterion.
4. Non-blocking 4 (a second refusal goes back to Strategy): taken, in Scope.

Security Review:
1. Blocking 1 (a second refusal is likely for the consent folder and file): answered by measurement. Strategy read both owners with `Get-Acl` on 2026-11-21 before this plan was written: both are the Maintainer's own account. So the plan is not widened, and no Decision is needed for his machine. For a user whose consent files are owned by Administrators, the README gains one sentence.
2. Blocking 2 (the stand-in hid the list of accounts): closed with the reviewer's test, which runs the real `_privileged_sid`.
3. Non-blocking 3 (TrustedInstaller stays out): the test has that case.

Also changed, by the Maintainer's standing direction on testing of 2026-11-21 ("run the fewest tests possible to make sure it was right"): the build runs the one new test, not the whole file.

Edited directly by Strategy, by exact replacement. Not run: any test.

**Elapsed**: unknown. **Tokens**: unknown.
