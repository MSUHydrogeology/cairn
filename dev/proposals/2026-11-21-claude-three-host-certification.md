# Certify each release on the Mac, Linux and Windows

**Author**: Claude Fable 5.2 (Strategy)
**Status**: awaiting-decision
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-21
**Rules that apply**: dev/rules/certifying-runs.md, dev/rules/protected-surfaces.md, dev/rules/development-environment.md, dev/rules/working-agreements.md, dev/rules/conventions.md
**In brief**: A release of Cairn is certified only when its tests have passed on a Mac, on Linux and on Windows, each host leaving its own record, so that no host you use is left out.

## Decision summary

**What you noticed.** Cairn 0.8.0 was certified by one full test run on the Mac. The records that the release steps ask of the Mac and of Windows, and the check that joins them, were waived at the cut. Linux has never had a record, and the release check cannot accept one. You wrote on 2026-11-21 that "excluding Windows and Linux certification was a defect", and on 2026-11-19: "for future releases, I want Linux and Windows verification alongside Mac."

**The change.** A release needs three records, one from each host. I read your words as starting with v0.8.1; that is choice 4. A record is nearly the whole test set (all but 16 files that only the Mac's own full run covers), run on that host twice, in two orders, under Python 3.13. One check, the join, reads the three records. It refuses the release if a host is missing, if the records are from different commits, or if a test that belongs to a host did not pass there.

**What is added, changed or removed.**
- The release check, an existing script, learns a third host, and its two-host join is removed. No new script and no new option.
- The release steps and the rule on certifying runs name three hosts.
- The Linux machine gets Python 3.13.
- If the Linux run finds tests that can pass only on a Mac, each is listed by name with its reason, and each release states how many there are.
- Plan D2 of the defect arc, the Windows checks, becomes this work's Windows plan.

**What it costs.** Machine time at every release: three hosts, two orders each. One order took 61 minutes on the Mac at 0.8 (measured). No full run has been timed on Linux or Windows, so the total is not known; expect several hours, unattended. Before the first such release the Linux and Windows runs must also be made to pass, and nobody can size that until each has run once.

**Your choices.**
1. *The Linux machine.* (a) The shared Linux virtual machine, with Python 3.13 added in its user's own folder: built from the official python.org source and checked against its published checksum, as Git was on that machine. Recommended. (b) Another machine you name.
2. *Waivers.* (a) The join always refuses a missing record and has no waiver option. A waiver is your own words, quoted in the release notes. Recommended. (b) No waiver at all; a machine that is down then stops the release.
3. *Tests that pass only on a Mac.* (a) List each by name with its reason. Recommended. (b) Make each one portable before the first three-host release; the size is unknown until Linux has run.
4. *The first release cut this way.* (a) v0.8.1, as I read your words of 2026-11-21: Linux and Windows must pass before it is cut. (b) The release after, so that v0.8.1 is not held.

## Context

- **Today's rule.** The certifying run is the full suite on a clean tree under Python 3.13 (`dev/rules/certifying-runs.md`). The release steps then ask for a record from the Mac, a record from Windows, and a join (`release/RELEASE_PROCESS.md`).
- **A record** is what `release/security_check.py --record` writes on one host: every tracked test file except the 16 the release excludes, run in the default order and in one fixed shuffled order.
- **The join** (`--join`) accepts exactly one Mac record and one Windows record (`_join_local_records`). No other host can produce a record: `_supported_native_host` knows only `darwin` and `win32`.
- **Native tests.** 425 tests are marked as belonging to a host family: 63 to Windows and 362 to POSIX, the family that holds both the Mac and Linux (`tests/security_manifest.py`, counted 2026-11-21). The join requires each to pass on its host.
- **0.8.0.** The Mac full run gave 1 failed, 5,894 passed and 66 skipped in 60:41 (`dev/measurement/certification-run-2026-11-19.md`). The two records, the join and both secrets scans were waived (`dev/PLANNING.md`, "Checks waived at the 0.8 cut").
- **Linux.** The shared virtual machine runs Ubuntu 24.04 with Python 3.12.3, 2 cores and 3 GiB of memory (`dev/rules/development-environment.md`). A record needs Python 3.13. No full Linux run exists, so the number of tests that fail there is not known.
- **Windows.** The last counted run on the Windows virtual machine gave 15 failed, 305 passed and 27 skipped (2026-11-16). The six measurements plan D2 waits for have not been taken.

## Proposal

**A. Three records, one join.** `--record` accepts a Linux host. `--join` takes three records and requires exactly one each from the Mac, Linux and Windows, at the same commit, with the same test policy and the same excluded list, each having collected the same test files. Any other host, and any missing or repeated host, is refused, as today. The two-host join is removed, not kept beside this one. The Linux record is taken with the same `--history-roots` manifest as the others, the file that tells a record which history to scan for secrets. The join requires that scan in all three records, with equal policy and runner hashes, and every other comparison between records covers all three as well. Plan C confirms that the scan tool runs on the Linux machine.

**B. A Mac-only class, built only if Linux needs it.** A POSIX test must pass on the Mac and on Linux. If the Linux run finds a test that can pass only on a Mac, it moves to a third class, with a one-line reason beside it. A Mac-only test must pass on the Mac and be skipped, never absent and never passed, on Linux and Windows; the Mac's record carries both the POSIX and the Mac-only duties. Moving a test into the class is a cut of a native test: it takes a Security Review and your re-signing of the gate manifest. The release's record states how many tests each class holds.

**C. The Linux record.** Python 3.13 is added to the Linux machine from a checked source (choice 1), and `dev/rules/development-environment.md` records where it came from. The record is run there once, to measure. Each failure is then fixed, or moved to the Mac-only class with its reason (choice 3).

**D. The Windows record.** The record is run on the Windows virtual machine. What fails there is the list plan D2 was waiting for. D2 is written from it and makes the record pass. Two of D2's six measurements are not part of any record and stay with D2 as they are: the published tag through both install routes in Git Bash, and the signing tests' missing temporary-folder variable.

**E. Rules and steps.** `dev/rules/certifying-runs.md` and `release/RELEASE_PROCESS.md` name the three hosts and the order. The Mac's full run, with the 16 excluded files, stays the certifying run. A waiver is yours alone (choice 2). Records are kept where they are kept today, and the short committed note that 0.8 had states the three results. The two secrets scans that were also waived at 0.8 are not changed here; they are due at the v0.8.1 cut.

**Plans.** One on the Windows Server machine for A, B and E, tested with records written by hand. One for C and one for D, each run from the Mac, which reaches both virtual machines. The three real records and the join at the cut are your operation, not a plan's task. Which release is cut this way first is choice 4.

## Rationale

The join is where "certified" is decided, so it is where a host must be required. Written steps cannot refuse a missing record, and at 0.8 they did not. This is exact work, the kind the roadmap's tooling rule keeps in a script, and it grows one existing script.

## Alternatives considered

- **Record Linux but do not require it.** A record nobody must produce is what was waived at 0.8.
- **Certify Linux in the Linux subsystem of the Windows Server machine.** It is at hand, but it runs Python 3.14 and is not a host you named.
- **Run only the native tests on Linux and Windows.** Minutes, not hours. But a test fails on a new host for reasons nobody listed, and only the whole set finds those. Worth another look if machine time proves too high.
- **Do nothing.** v0.8.1 is certified on the Mac alone again.

## Documentation / doctrine surface

`dev/rules/certifying-runs.md` and `release/RELEASE_PROCESS.md` (the governing and release layers); `dev/rules/development-environment.md` (the Linux machine's Python); the roadmap's section 2 row and its entry "Checks waived at the 0.8 cut". No shipped template changes.

## Evidence / verification plan

It worked when a join over three real records at one commit passes, and a join without the Linux record is refused.

### Tests required

Promise: no join passes without all three hosts. Entry points: `security_check.py --join` and `--record`. Extend the existing join tests in `tests/test_security_check.py` with records written by hand. Three good records pass. Each of these is refused: no Linux record; two Linux records; a Linux record at another commit, with another policy, or with another excluded list; a Linux record whose scan policy or runner hash differs; a POSIX test that failed on Linux; a Mac-only test that failed or was skipped on the Mac; a Mac-only test that passed on Linux. A Mac-only test must pass on the Mac and be skipped, never absent and never passed, on Linux and Windows. Bounded: the release check and its tests.

### Examples / smoke checks

`python tests/check_cairn.py` on each changed document. The three real records and their join at the cut.

#### Security preflight

- **S1.** The join decides. Its inputs are three record files that the Maintainer names, the commit of the checkout, and the test policy in the checkout. Each record is written by the host it speaks for, as today. The join compares it with the checkout's own list of tests, not with what the record claims.
- **S2.** Each refusal above is a test that fails if the refusal is removed. Moving a test into the Mac-only class is a cut of a native test: it needs a Security Review and the Maintainer's re-signing of the gate manifest, and the release's record states the class counts.
- **S3.** The Maintainer runs `--record` on each host and `--join` on the Mac, over every tracked test file but the 16 excluded. The release steps will say three hosts.
- **S4.** An unknown host, a missing record and a file that does not parse are each refused. That is less authority, not more.
- **S5.** Someone who can edit a record file before the join can forge a pass. That is true today for two hosts and stays true for three. The Linux record is also written on a virtual machine that other projects share, and is carried to the Mac, which adds one writer and one transfer. The class is closed neither by construction nor by enumeration.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

More than 50 of the 362 POSIX tests end up Mac-only, so the Linux record says little. A release's three records take more than a working day of machine time. The virtual machines fail tests for their own reasons, such as 3 GiB of memory, more often than Cairn does. The first Linux record fails in files nobody had measured.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance

## Review -- Claude Sonnet 5.5 -- 2026-11-21

```
Reviewed commit: 2e7c920bebb9735c826f3a48815b79fefa11585f
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Elapsed**: unknown
**Tokens**: unknown

**Foundations**:

1. **Should this happen as framed?** Yes: the join is the one place a missing host can be refused, and a three-host join is the smallest code that does it. The framing leaves two things to guess (findings 1 and 2). -- `release/security_check.py` `_join_local_records` (line 732: exactly two records) and `_supported_native_host` (line 324).
2. **Best alternative.** Whole set on each host beats native-only: the join already demands every non-excluded test pass in both orders (`_validate_raw_suite_report`, `pytest_exit == 0`), so a native-only record would be new code, not less. Doing nothing repeats the 0.8 waiver. -- `release/security_check.py` lines 395-413, 464-474.
3. **What would show it wrong.** The proposal's own signals hold (over 50 Mac-only, over a working day). Add: the first Linux record fails in files it never measured. -- Signals section; `dev/PLANNING.md` Windows entry.

**Does any rule weaken or disappear?** No, if finding 4 is added. Checked: facts 63/362 (`validated_native_only_nodes`, line 689), 16 excluded rows (`RELEASE_EXCLUDED_TESTS`), 60:41 run (certification record), Linux VM facts (`development-environment.md` lines 163-167). Not checked: the 15/305/27 Windows figures of 2026-11-16 (taken from the roadmap and proposal, not re-counted) and the 61-minute timing beyond the record's own line.

The proposal's strongest form: no host you use is left out, and the join, not prose, enforces it. Sound.

**Findings**

1. **Blocking. "A Mac-only test absent from the Linux record is accepted" contradicts the code and weakens it.** Today `_validate_outcome_rows` (lines 374-376) and `_validate_local_record` (584-586) refuse a record that omits any fixed native ID. Accepting absence loosens both, for every host, and lets a test vanish from Linux unseen. Replace the sentence with the exact words below.
2. **Blocking. The secrets-scan part of the record is unstated.** With `--history-roots`, every record must carry a history sweep and the join compares two records' policy and runner hashes (`_run_join`). Three records change that; Linux would need the same scan tool. State whether the Linux record uses it. Words below.
3. **Blocking. "Waiver" has no mechanism.** The join refuses; it prints no waiver. Say a waiver is the Maintainer's quoted words in the release notes, with no script option. Also say choice 2(b) means a down machine stops a release. Words below.
4. **Blocking, premise, for the Maintainer: which release.** "Excluding Windows and Linux certification was a defect" ends his reply about Claude and Antigravity; the roadmap calls the v0.8.1 reading Strategy's, and another roadmap entry says the waived checks fall due at 0.9. Add a fourth choice. The Decision summary now states v0.8.1 as settled.
5. Non-blocking. The Mac full run (with the 16 excluded files) must stay named in the certifying rule; add one clause to E.
6. Non-blocking. The 120-of-895 signing failures belong to files the record excludes; they do not predict the Mac-only count. Drop or label them.
7. Non-blocking. Build the Mac-only class in plan C only if Linux needs it, per "no new tooling unless it's needed". The join for three is needed.
8. Non-blocking. Plan D2: measurements (d) the published-tag check in Git Bash and (e) the ceremony tests are not in a record (the ceremony files are excluded). Say they stay with D2 or move to the roadmap.
9. Non-blocking. Name where Python 3.13 comes from and how it is checked; it runs the certifying record.
10. Non-blocking. The proposal is 1,669 words against 1,000; Context's native-test and Windows lines repeat the roadmap.

**Not covered**: no test run; Windows record and the plan archive read only for D2's six items; code of the record's child run (`_run_local_record` body) skimmed, not traced.

### Exact words

- **1.** In "Tests required", replace "A Mac-only test absent from the Linux record is accepted." with "A Mac-only test must appear in the Linux and Windows records as skipped, never absent, and must pass on the Mac; a Mac-only test that passed on Linux is also accepted."
- **2.** Add to A: "The Linux record is taken with the same `--history-roots` manifest as the others, and the join requires the history sweep in all three and equal policy and runner hashes across them. Plan C confirms the sweep tool runs on the Linux machine."
- **3.** Add to choice 2(a): "A waiver is the Maintainer's own words, quoted in the release notes; the join has no waiver option and still refuses." Add to 2(b): "A machine that is down then stops the release."
- **4.** Add "4. *First release.* (a) v0.8.1, as you wrote on 2026-11-21; Linux and Windows must pass first. (b) The release after, so v0.8.1 is not held." and, in the summary, "I read your words as v0.8.1."
- **5.** Add to E: "The Mac's full run, with the 16 excluded files, stays the certifying run."

## Review -- Claude Opus 5.5 -- 2026-11-21

```
Reviewed commit: 49e1315b06b16164f4f1b1018631072057ed3796
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE

**Elapsed**: unknown
**Tokens**: unknown

**Foundations**:

1. **Should this happen as framed?** Yes: the join is the only place that can refuse a missing host, and every record outcome is already checked strictly. -- `release/security_check.py` lines 332-383, 732-773.
2. **Best alternative.** Whole set over native-only, as the usual review says. Doing nothing leaves the 0.8 waiver as the precedent. -- same file, lines 464-474.
3. **What would show it wrong.** A Mac record relabelled as Linux passes the join. Today only the Mac-only outcomes could tell the two apart. -- lines 324-329 (Mac and Linux share the tag `posix`).

The strongest form: no host goes unchecked, and code, not prose, refuses. I agree with usual findings 2, 3, 4 and 8. My words govern finding 1 (B1 below) and raise finding 9 to blocking (B5).

**Findings**

- **B1. Blocking. A Mac-only test could skip on every host.** A record names its host family (`posix` or `nt`), not the machine. A Mac-only test is skipped wherever its tag differs from the host's, and the Mac's tag is `posix`. So without new words the Mac could skip it too. Also, a Mac-only test that passes on Linux is not Mac-only.
- **B2. Blocking. S2 overstates the guard.** The policy id is a hash pinned in the same file, so whoever moves a test recomputes it (`tests/security_manifest.py` lines 656, 687). The real guards are the gate signing, which covers that file (`tests/fixtures/gate_manifest.json` line 7674), and the protected-surfaces rule (line 43). That rule does not clearly say that moving a test between classes is a cut.
- **B3. Blocking. A two-way check is easy to leave in place.** The sweep check compares `loaded[0]` with `loaded[1]` only (lines 2626-2630). A third record would go unchecked.
- **B4. Blocking. A two-record join must not survive as a fallback.** If it did, the script itself would be the waiver.
- **B5. Blocking. Where Python 3.13 comes from.** That interpreter writes the evidence the join trusts. On this VM, Git came from checksum-verified upstream source (`dev/rules/development-environment.md` line 169). Choice 1(a) names no source.
- N1. Non-blocking. S5 is incomplete. The Linux record is written on a VM that other projects share and is carried to the Mac, so the steps add a writer and a transfer. Its file mode is 0600 (line 668).

S1, S3 and S4 hold (lines 748-761, 2591-2593, 329).

**Not covered**: no tests run; the join tests in `tests/test_security_check.py`, the Windows record and the plan for the Windows checks were not read; the PLANNING quotes were taken from the usual review.

### Exact words (Security Review)

- **B1.** Replace the usual review's sentence for finding 1 with: "A Mac-only test must pass on the Mac and be skipped, never absent and never passed, on Linux and Windows. The Mac's record carries both the POSIX and the Mac-only duties." Add to Tests required: "a Mac-only test skipped on the Mac; a Mac-only test that passed on Linux."
- **B2.** Replace S2's second sentence with: "Moving a test into the Mac-only class is a cut of a native-only ID: it needs a Security Review and the Maintainer's re-signing of the gate manifest, and the release's record states the class counts."
- **B3.** Add to A: "Every comparison between records, including the history-sweep policy and runner hashes, covers all three." Add to Tests required: "a Linux record whose sweep policy or runner hash differs."
- **B4.** Add to choice 2(a): "The two-record join is removed, not kept beside the three-record one."
- **B5.** Add to choice 1(a): "built from the official python.org source, checked against its published checksum, as Git was."

## Response -- Claude Fable 5.2 (Strategy) -- 2026-11-21

Both reviews are folded once, in place. Status is now `awaiting-decision`.

Usual review:
1. Blocking 1 (an absent test was accepted): closed with the Security Review's stricter words, its B1.
2. Blocking 2 (the secrets scan in a record): taken, in A.
3. Blocking 3 (a waiver had no mechanism): taken, in choice 2 and E.
4. Blocking 4 (which release): taken as choice 4. The summary now says v0.8.1 is my reading. Also asked of the Maintainer in chat on 2026-11-21.
5. Finding 5 (the Mac's full run stays): taken, in E.
6. Finding 6 (the 120 of 895 signing failures): dropped from Context.
7. Finding 7 (build the class only if Linux needs it): taken, in B and the summary.
8. Finding 8 (two of D2's measurements are in no record): taken, in D.
9. Finding 9 (where Python 3.13 comes from): taken with the Security Review's B5, in choice 1 and C.
10. Finding 10 (length): one Context sentence is cut. The fold adds more than it cuts, because nine blocking findings each needed words; the Decision summary is not shortened.

Security Review:
1. B1 (a Mac-only test could skip on every host): taken with its exact words, in B and Tests required. Its question, skipped only or pass or skip: skipped only.
2. B2 (S2 overstated the guard): taken, in S2 and B.
3. B3 (the scan check compared two records): taken, in A and Tests required.
4. B4 (no two-record join as a fallback): taken, in A, choice 2 and the summary.
5. B5 (the source of Python 3.13): taken, in choice 1 and C.
6. N1 (S5 was incomplete): taken, in S5.

### Withdrawn / superseded commitments

- "A Mac-only test absent from the Linux record is accepted." Withdrawn: it must be skipped, never absent and never passed.
- S2's claim that the pinned policy id keeps a class move from going unseen. Withdrawn: the guards are the Security Review and the re-signing.
- "From v0.8.1", stated as settled. It is now the Maintainer's choice 4.

**Elapsed**: unknown. **Tokens**: unknown.
