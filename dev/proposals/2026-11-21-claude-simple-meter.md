# A simple usage meter: read the logs, write the summary

**Author**: Claude Fable 5.2 (Strategy)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-21
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/working-agreements.md, dev/rules/custom_session_routines.md, dev/rules/development-environment.md
**In brief**: The usage meter keeps its two real promises, that it reads only the folders you list and that only counts leave a log, and loses the permission and anti-tamper checks that stopped it running on ordinary machines.

## Decision summary

**What you noticed.** The meter would not run on your Windows machine. In one day it refused five ordinary things in turn, each through one of its own checks, and none caught a real problem. You wrote on 2026-11-21: "The meter is literally just measuring a folder and writing a file inside of our measurement folder, right? There's no reason it needs elaborate permission checks, just read the right location for each agent". Asked whether to replace the narrow fix with the simple meter now, you wrote: "Yes, simplify now. That is way too much for a log that doesn't actually do anything."

**What the meter keeps.** Two promises, and neither is a permission check. It reads nothing unless your consent file lists the folder. And only counts leave a log: no text, no file names, no paths.

**The change.** The meter reads each listed log folder and writes its summary with ordinary file calls, the same ones on the Mac, Linux and Windows. Out come the tests of who owns a folder and who else may change it, the counting of a file's names, the re-checking of folders while it reads, the Windows-only layer, and the check of the project's Git settings.

**Two cheap habits stay.** It does not follow a link out of a log folder or write through one. It writes its summary and its own record beside their place and renames them in, so a crash cannot leave half a file.

**What it gives up.** An account on the same machine that can already write into your log folder or your project could skew your counts or delete the summary. It could not read your logs through the meter, before or after.

**What it costs.** It is the largest change in v0.8.1. By a rough count, up to half of the meter's code and a quarter or more of its tests go, 35 of them from the pinned list of Windows-only tests, which adds lines to your signing. Plan I is withdrawn. The owner rule of plan G and the folder-walk fixes of plan H go with the code they patched; plan H's fix to reply dates stays.

**Not in this proposal.** The Antigravity reader, which is built afterwards on the simple meter. The table of token weights, which has no entry for the newest model.

## Context

Measured on 2026-11-21 (`dev/PLANNING.md`, section 1, "The meter still does not run on the Windows Server machine", and "Waiting on you"). `dev/tools/meter.py` has 7,573 lines. By function name, 1,892 are in code named for Windows and 1,646 more in code named for access tests, links, held folders, guarded writes and the checked Git helper. The access test is called in 47 places, and 68 of the 260 meter tests are named for Windows. On the Windows Server machine the meter refused, in turn: a profile folder owned by the Administrators group; a log sub-folder, twice; a log with a second name; and a project on a drive the Maintainer shares on purpose. A sixth is known: an access entry on `AppData` would refuse any log kept there. With those checks relaxed in memory, the meter's token totals equalled an independent count of the same log over 77 replies.

## Proposal

**A. The two promises,** unchanged. Consent: the meter reads only the log folders and projects listed in `~/.cairn/meter.json`, and installing Cairn creates no such file. Counts only: nothing read from a log leaves it except counts, times, and names on the closed list the reader already keeps.

**B. Reading.** For each listed log folder the meter walks it with ordinary calls, skips any link or redirected folder, and reads each log from where it last stopped, up to the last whole line. A log it cannot open is left for the next run, and the reading is marked incomplete. It no longer tests owners, access lists or the number of names a file has, and no longer re-checks folders while it reads.

**C. Writing.** The summary goes to `dev/measurement/meter.json` in the project, and the meter's record stays under `~/.cairn/meter/`. Each is written to a new file beside its place and renamed in. Where the system has file modes, the record is made readable by the user alone. The meter refuses to write a summary when `dev` or `dev/measurement` is a link. One run writes at a time, by a plain lock file.

**D. Which project.** A record counts toward a project when the folder the record names is the project's folder or inside it. The project's remote is taken from the consent file, where the user wrote it. The project's Git settings are no longer opened, so the meter no longer uses the checked Git helper. Where a tool's own log names the repository a session ran in, as Codex's does, that name is still compared with the remote in the consent file.

**E. One code path.** The Windows-only layer and the descriptor walks used on the Mac and Linux are removed. The end-to-end tests that ran only on the Mac and Linux run on all three platforms.

**F. Tests.** Tests of the removed checks go, and their 35 rows leave the pinned list of Windows-only tests; the list's count and fingerprint, and the test that quotes them, follow. Tests of reading, counting and the two promises stay. Added, at most three: a full run on a made-up log folder that has a sub-folder, on every platform; a link out of a log folder is not followed; a summary is not written through a link.

One plan, at most five chunks. The consent file, the record and the summary keep their shapes.

## Rationale

Every check removed here guards against an account that can already write the user's own files. Against that account the checks protected a tally. Their price was a meter that refused ordinary machines, and a second code path for Windows that no test ran on a real log folder.

## Alternatives considered

- **Plan I now, the simple meter in v0.9.** The narrow fix lands sooner. It lost because its change would be removed weeks later, the Windows certification would be spent on tests of code that is to go, and the Antigravity reader would be built on the old meter.
- **Keep the checks and fix each refusal.** That took three plans in a day, with a sixth refusal already known.

## Documentation / doctrine surface

`dev/measurement/README.md`: the meter's section, rewritten shorter. `dev/rules/development-environment.md` and `dev/rules/custom_session_routines.md`, where they state a removed check; the rule on what may leave a provider log is untouched. `CHANGELOG.md`. The shipped copy of the meter and of each changed document.

## Evidence / verification plan

It worked when a real refresh on the Windows Server machine answers `ok` with the tracked meter, its totals equal an independent count of the same log, and nothing but counts is found in the summary and the record; and when the same holds on the Mac at the cut.

### Tests required

As in F: tests of removed checks are deleted, the rest are kept, and at most three are added.

### Examples / smoke checks

The two real-machine checks above, by Strategy, with probes that print counts only.

#### Security preflight

- **S1. What is protected.** The content of private logs. The reader, which emits counts only, and the consent file protect it. Neither changes.
- **S2. What is weakened.** The meter's numbers, and the place its summary lands, are no longer guarded against another account on the same machine.
- **S3. Who could use that.** Only an account that can already write the user's log folder, project or profile.
- **S4. If it goes wrong:** wrong counts, a missing summary, or a summary file in a folder the user can write. Never text from a log.
- **S5. What still gets through.** Usage planted in a log folder is counted. A log changed while it is read is read as found.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Any text from a log in the summary or the record. A summary found outside a project. Totals that differ from an independent count of the same log.

## Scope delta

**Scope delta**: lost

- The owner and access-list tests, the single-name test, the re-checks during a read, the private access list made for the meter's files on Windows, and the check of the project's Git settings. **disposition**: accept, by the Maintainer's words of 2026-11-21: "There's no reason it needs elaborate permission checks, just read the right location for each agent".

## Assurance path

**Assurance path**: high-assurance
