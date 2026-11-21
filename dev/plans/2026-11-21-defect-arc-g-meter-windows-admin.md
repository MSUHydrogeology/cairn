# Plan: Defect arc G, the meter runs for a Windows administrator

**Source proposal**: dev/proposals/archive/2026-11-20-claude-v09-defect-arc.md
**Status**: ready-to-archive
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

## Implementation record -- Implementation (Claude Sonnet 5.5) -- 2026-11-21

Worktree `.claude/worktrees/arc-g`, branch `arc-g-impl`, cut from `0.9-dev` at f7c4498a (usage-counting work already merged; lines re-read before the edit).

**Commits.** 5141720c status implementing; 14cde571 code, test, README sentence, changelog line, shipped copy; 4a40b602 lock only.

**Condition as built**, in `check_acl` (`dev/tools/meter.py`), exactly as the Scope gives it:

```python
if role == "profile":
    if owner_bytes != user_sid and not self._privileged_sid(owner_bytes, ancestor=False):
        raise Unavailable
elif role in {"cairn", "config", *private_roles} and owner_bytes != user_sid:
    raise Unavailable
```

**Test.** `test_windows_profile_owner_may_be_system_or_administrators`, appended as the Security Review gives it; it needed no new import. With the change, on Windows: `1 passed, 554 deselected in 3.16s`.

**Fails without the change.** I stashed only `dev/tools/meter.py` (the old condition), ran the same command once, then restored it: `1 failed, 554 deselected in 3.65s`, with `Unavailable` raised at the old owner line, on the first SYSTEM-owned profile case.

**Checks.** `cmp dev/tools/meter.py templates/skills/_lib/meter.py` printed nothing. `verify_integrity.py --target .` reported OK (70 recorded files match). The lock was refreshed with the plan's `--finalize` command for `meter.py` and the README (both are recorded); its commit holds only the lock.

**Not run.** The rest of `test_meter.py` and the suite (certification). The real machine and the meter itself (Strategy's check). The gate manifest hash of `test_meter.py` is left as the plan says: one HOLD for the Maintainer's next signing.

**Differences from the plan.** None.

**Elapsed**: unknown. **Tokens**: unknown.

## Code review -- Claude Sonnet 5.5 (usual reviewer) -- 2026-11-21

Reviewed commit: ea0a2a2f0144235fa44b32a08d63f419687284f6
Range: f7c4498af5073e604907e1e21a1e0cf865f759c1 (merge-base with `0.9-dev`) to ea0a2a2f0144235fa44b32a08d63f419687284f6

**Obligation**: the usual code review
**Tier**: Internal
**Findings**: none blocking

**Foundations**:

1. **Does it do what it claims?** Yes. The condition in `check_acl` matches the plan's Scope character for character. Role `profile` now accepts the user, SYSTEM or Administrators as owner. Roles `cairn`, `config` and the five private roles still accept only the user. Role `ancestor` is untouched and still accepts the user, SYSTEM, Administrators and TrustedInstaller -- `git diff` of `dev/tools/meter.py`, five lines, `check_acl`.
2. **Best alternative.** None simpler; the Maintainer chose "Fix the meter" -- the plan's Source proposal.
3. **What would show it wrong.** The test is the Security Review's block word for word. Too strict: the user, SYSTEM and Administrators cases would fail. Too loose: the other-account and TrustedInstaller cases would fail (`ancestor=True` would admit TrustedInstaller). I ran it once: `1 passed, 554 deselected in 2.92s`. That it fails without the change is the record's claim; I did not re-run it, but the old line raises for a SYSTEM owner on the first case -- `tests/integration/test_meter.py` last test.

**Findings**

1. Non-blocking: the README sentence was added inside an existing long line, so the paragraph is not rewrapped. It is true of what shipped (roles `cairn`, `config`) -- `dev/measurement/README.md`.

Also checked: the copies match (`cmp` printed nothing); the lock commit holds one file, the lock; `verify_integrity.py --target .` reports OK; the changelog line is true. No rule weakens beyond the plan; no frozen file changed. The gate-manifest HOLD and the real machine are left to Strategy, as the record says.

**Verdict**: ACCEPT

Not covered: the Security Review questions, the rest of `test_meter.py`, the real machine. Elapsed time: unknown. Tokens: unknown.

## Code review -- Claude Opus 5.5 (Security Review) -- 2026-11-21

Reviewed commit: ea0a2a2f0144235fa44b32a08d63f419687284f6
Range: f7c4498af5073e604907e1e21a1e0cf865f759c1 (merge-base with `0.9-dev`) to ea0a2a2f0144235fa44b32a08d63f419687284f6

**Obligation**: the Security Review at the code stage
**Tier**: Internal Security Review
**Findings**: none

**Foundations**:

1. **No account gains power over consent.** Owning a folder gives the right to rewrite its access list. Administrators and SYSTEM already pass the profile access-list loop with any rights, and an elevated administrator can take ownership anyway. An ordinary second user is neither, so stays refused; a second administrator gains nothing new -- `dev/tools/meter.py` `check_acl`, the loop's `_privileged_sid` skip.
2. **Identity, not membership.** The owner's SID bytes are compared with exactly `S-1-5-18` and `S-1-5-32-544`; group membership is never consulted, so Domain Admins or any other group stays refused -- `meter.py` `_privileged_sid`, `ancestor=False`.
3. **Every other role is as strict as before.** `cairn`, `config` and the five private roles still require the user; `ancestor` is untouched; the profile access-list mask (`profile_denied`) is unchanged, so no one but the user, SYSTEM and Administrators may hold write, delete-child or access-list rights there -- `git diff f7c4498a ea0a2a2f -- dev/tools/meter.py`, five lines.

I agree with the usual review's Foundations and its one finding; on the four security questions this review governs.

**Findings**

None. Checked: the test ran once, `1 passed, 554 deselected in 2.18s`; `cmp` printed nothing; `verify_integrity.py --target .` reports OK; the lock commit 4a40b602 holds only the lock.

**Verdict**: ACCEPT

Not covered: the real machine, the POSIX path, the rest of `test_meter.py`, a re-run without the change (the record shows it). Elapsed time: unknown. Tokens: unknown.

## Code-review response -- Claude Fable 5.2 (Strategy, for the author) -- 2026-11-21

Both code reviews accepted the change, and neither raised a blocking finding. Status is now `ready-to-archive`.

1. Usual review, finding 1 (non-blocking: the README sentence sits inside an existing long line): no change is asked and none is made. Functional prose is edited by exact replacement and never rewrapped, so the line stays as it is.
2. Security Review: no finding.

Not run for this response: any test.

**Elapsed**: unknown. **Tokens**: unknown.

## Strategy's check on the real machine -- Claude Fable 5.2 (Strategy) -- 2026-11-21

**Not met.** The refusal this plan fixes is gone, and the meter still does not run on the Windows Server machine. The plan stays at `ready-to-archive` and is not archived on this result.

Measured on the merged tree (`577e6a8e`), with probes that print sizes, counts, reason codes and code locations only; nothing read from a log was kept or shown.

- The consent read passes (`current_user_profile` and `read_config` both return). Before the change it stopped at the owner test in `check_acl`.
- `meter.py refresh --json` still answers `unavailable`, now with the reason `source_changed`, raised in the walk of the log folder (`_enumerate_windows_jsonl`).
- A diagnostic run relaxed each stopping comparison in memory only. The tracked file was not edited, and the ledger that run made was deleted. It found, in order: a sub-folder's size is read as a change; any sub-folder then fails a lookup; a log file with two names is refused, and the desktop app gives each background sub-agent's transcript a second name; and the project's own folders on the `F:` drive give other accounts rights the meter refuses.
- One finding touches every platform: a Claude reply written as several records with different times loses its date. With the meter's own reader over about five minutes of one session, 12 replies gave token totals equal to an independent count, and 9 of the 12 were marked `ambiguous_time`.

This is "a second refusal of another kind", which the Scope sends back to Strategy. Home: `dev/PLANNING.md`, section 1, "The meter still does not run on the Windows Server machine". Plan H carries the faults in the meter. The folders on the `F:` drive are the Maintainer's to settle and are asked of him under "Waiting on you".

Seen on the way: Cairn's own ignore file had no line for the meter's summary file, which every installed project gets. Fixed in `b6c26c71`.

Not checked: the export step on Windows, which the fourth finding stops before it runs; the Mac and Linux paths on a real log.

**Elapsed**: unknown. **Tokens**: unknown.
