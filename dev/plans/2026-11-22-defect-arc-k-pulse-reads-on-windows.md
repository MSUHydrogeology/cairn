# Plan: Defect arc K, the pulse reads a report on Windows

**Source proposal**: dev/proposals/archive/2026-11-20-claude-v09-defect-arc.md
**Status**: awaiting-code-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-22
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/working-agreements.md, dev/rules/conventions.md, dev/rules/development-environment.md
**In brief**: The pulse will stop refusing a report it has just written on Windows, by comparing the file's change time only between its two readings by handle, not with the reading by name, where Windows reports another time.

## Build summary

On Windows the pulse refuses most reports it has just written, so `tests/integration/test_gauge.py` fails 24 to 27 of 77 tests, differently each run. This plan stops comparing that one field against the reading by name.

## Source proposal

The defect arc fixes 0.8 faults; this is roadmap items (j) and (p).

## Scope

`_read_pulse_report` in `dev/tools/pulse.py` requires three readings of the file to agree: by handle at open, by handle after the read, and by name after the read. Each is `(st_dev, st_ino, st_size, st_mtime_ns, st_ctime_ns, st_nlink)`.

Measured (Strategy, 2026-11-22; Python 3.13.5, Windows Server 2022, 300 rounds, two drives): the handle and name readings differ in `st_ctime_ns`, and no other field, in 299 or 300 of 300 rounds. By handle it is the last change time; by name, the creation time. They match only within one clock tick, so failures vary by run. Read, not run: on Mac and Linux both come from one field.

**The change.** Take `st_ctime_ns` out of the tuple, and compare it only between the two readings by handle:

```python
identity = lambda st: (st.st_dev, st.st_ino, st.st_size,
                       st.st_mtime_ns, st.st_nlink)
if (identity(opened) != identity(after)
        or opened.st_ctime_ns != after.st_ctime_ns
        or identity(after) != identity(name_after)):
    raise _PulseInputError
```

Everything else stays.

**One plain code path, no Windows-only step.** `exact_replace.py`, `git_read.py` and `session.py` swap in the creation time on Windows first. The pulse will not, and it is still one plain code path: the change time is still compared where both readings come from the open file. The Maintainer's 2026-11-21 direction for the meter was one plain code path, with checks matched to what they protect ("That is way too much for a log that doesn't actually do anything."). It was about the meter; applying it here is Strategy's reading, and a reviewer may disagree.

**For the Security Review.** The change time is kept between the two readings by handle and dropped only from the reading by name, where Windows reports another time. Kept: the bytes still come from one file (same device and file id by handle and by name), whose size, last write time and count of names did not change during the read, reached through no link.

**Reuse.** N/A: no code added. No doctrine surface; no non-archived document says the pulse compares change time (searched `.md` files for `ctime`, `change time` and `pulse`), so no correction.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Narrow the change-time test; shipped copy; lock; changelog | Plan J merged first (it also edits `pulse.py`) | `pulse.py` and its copy |

## Acceptance criteria

C1: the direct check below refuses at least one round before and none after. `tests/integration/test_gauge.py` runs once, whole, after the change: each remaining failure is named with its cause; a cause other than this fault is reported, not chased. `cmp` of the two copies prints nothing; `verify_integrity.py` reports OK; `CHANGELOG.md` gains one `Fixed` line under Minor changes, citing this plan.

## Verification

Direct check, once before and once after, from the work folder, run in Git Bash:

```
C:\ProgramData\Anaconda3\python.exe -c '
import importlib.util as u, pathlib as p
s = u.spec_from_file_location("pulse", "dev/tools/pulse.py")
m = u.module_from_spec(s); s.loader.exec_module(m)
f = p.Path("dev/scratch/k_probe.txt")
def refused():
    f.unlink(missing_ok=True); f.write_text("x")
    try: m._read_pulse_report(f, 1000); return 0
    except Exception: return 1
print(sum(refused() for _ in range(300)), "of 300 refused"); f.unlink()'
```

Expected: at least one refused before (the count may be well below 300), 0 after. Then `cp dev/tools/pulse.py templates/skills/_lib/pulse.py`; then, alone in its commit, `install/scaffold.py upgrade --target . --finalize dev/tools/pulse.py`, then `install/verify_integrity.py --target .`.

Not run: a second host, the rest of the suite.

## Plan review -- Reviewer (Claude Sonnet 5.5) -- 2026-11-22

Reviewed commit: 2e95613b8cb9416e9a2a93f6e867a72c7265e1e3

**Obligation**: usual plan review (Internal)
**Tier**: Internal
**Findings**: raised (none blocking)

**Foundations**:

1. **Should this happen as framed?** Yes. `_read_pulse_report` compares `opened`, `after` (by handle) with `name_after` (by name) on a tuple holding `st_ctime_ns`; Strategy's measurement says Windows reports that field differently by handle and by name, so the refusal follows -- `dev/tools/pulse.py` 100-106.
2. **Best alternative.** One plain path is right: the bytes stay tied to one file by device and file id, size, write time and name count, so a creation-time swap adds code for a change no byte of the report shows. Both identity tests (line 90 and the tuple) use only `st_dev`/`st_ino` besides the removed field -- `dev/tools/pulse.py` 87-106.
3. **What would show it wrong.** A refusal after the change in the direct check, or a failing `st_mtime_ns` or `st_ino` comparison in `test_gauge.py`; I did not run either.

**Findings**

1. Non-blocking. The direct check deletes and recreates one name each round. Windows can hand a recreated name its old creation time (file tunneling), so the by-name field may match less often than in a fresh-name test; the change time by handle still moves, so "most refused before" should hold, but the plan should say the count may be below 299.
2. Non-blocking. The check is written with single quotes around inner double quotes: it works in Git Bash, not in PowerShell. Say "run it in Git Bash".
3. Non-blocking. The changelog line should cite this plan, as the neighbouring lines do.

Gate on plan J, the shipped copy, the lock alone in its own commit and the changelog line are in order.

Not covered: the measurement itself (not repeated), the Security Review questions, any test run.

Elapsed: about 6 minutes. Tokens: unknown.

**Verdict**: ACCEPT

## Plan review -- Security Reviewer (Claude Opus 5.5) -- 2026-11-22

Reviewed commit: 6486febc8fd3044468d1a3ebad191dcbcf72be33

**Obligation**: Internal Security Review (plan)
**Tier**: Internal Security Review
**Findings**: raised (two blocking)

I agree with the usual review on the cause, the gate and the records. On the check's count and on the change itself, my wording governs.

**Foundations**:

1. **Should this happen as framed?** Yes, but drop the change time only from the by-name comparison: the plan says no byte can change unseen, yet the writer of a file can rewrite it at the same size and put the write time back (`os.utime`); on Mac and Linux only the change time shows that -- reasoning; `dev/tools/pulse.py` 102-106.
2. **Best alternative.** Keep the change time between the two by-handle readings, in one plain code path: on Windows they never differed (0 of 300 rounds) -- my scratch probe, Python 3.13.5, deleted after.
3. **What would show it wrong.** A refusal in the direct check after the change -- not run.

**Findings**

1. Blocking. Replace the code block under "The change" with:
   ```python
   identity = lambda st: (st.st_dev, st.st_ino, st.st_size,
                          st.st_mtime_ns, st.st_nlink)
   if (identity(opened) != identity(after)
           or opened.st_ctime_ns != after.st_ctime_ns
           or identity(after) != identity(name_after)):
       raise _PulseInputError
   ```
   and in "For the Security Review" replace "The removed field guarded notice of a change to the file's record alone (permissions or owner) during the read; no byte the pulse reads changes." with "The change time is kept between the two readings by handle and dropped only from the reading by name, where Windows reports another time."
2. Blocking. My probe, which deletes and recreates one name like the direct check, saw the by-name time differ in 47 of 300 rounds, not most. In Acceptance criteria replace "refuses most rounds before and none after" with "refuses at least one round before and none after"; in Verification replace "most refused before" with "at least one refused before".

Kept, as the plan says: no link on the path, a regular file with one name, the same device and file id by handle and by name, and size and write time unchanged. Nothing new is read or printed. An attacker who can write the report gains no new output: reports are parsed as untrusted (`dev/tools/pulse.py` 695-765).

Not covered: Mac and Linux behaviour (read, not run), the tests.

Elapsed: about 12 minutes. Tokens: unknown.

**Verdict**: REVISE

## Plan response -- Claude Sonnet 5.5 (Implementation, for the plan's owner) -- 2026-11-22

- Security 1 (blocking): took the exact code and the replacement sentence; the In brief line, Build summary, "The change" lead-in and one-code-path paragraph now agree.
- Security 2 (blocking): "most refused" became "at least one refused" in Acceptance criteria and Verification.
- Usual 1: settled by Security 2; Verification also says the count may be well below 300.
- Usual 2: Verification says the check is run in Git Bash.
- Usual 3: Acceptance criteria say the changelog line cites this plan.

Disposition: ready-to-implement. Not run for this response: any test. Elapsed: unknown. Tokens: unknown.

## Implementation record -- Claude Sonnet 5.5 -- 2026-11-22

The change works: the direct check refused 61 of 300 rounds before and 0 of 300 after (measured, Git Bash, Windows Server 2022, Python 3.13).

- **Commits**: `0c2af525` status to implementing; `ca3afa72` the change in `dev/tools/pulse.py`, the shipped copy and the changelog line; `d1dbd1a6` Cairn's lock alone.
- **Code**: exactly as the revised plan gives it. `cmp` of the two copies printed nothing.
- **Test file**: `tests/integration/test_gauge.py`, whole, once: 68 passed, 1 failed, 8 skipped. The failure is `TestGaugePhysicalBinding::test_real_cli_refuses_each_binding_mutation[cached-module]`. Read from its output, not rerun: a test helper writes a Windows temp path into a Python `-c` string without escaping, so Python stops on `\U` in `\Users` with a SyntaxError. That is a test-side Windows path fault, not this one; reported, not chased.
- **Integrity**: `verify_integrity.py --target .` OK (70 files); `tests/check_cairn.py` with no argument OK (224 files).
- **Not run**: any second host, any other test file, a rerun of the failing test.
- **Difference from the plan**: none.

Elapsed: unknown. Tokens: unknown.
