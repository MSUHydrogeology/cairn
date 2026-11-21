# Certify each release on the Mac, Linux and Windows

**Author**: Claude Fable 5.2 (Strategy)
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: light
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-11-21
**Rules that apply**: dev/rules/certifying-runs.md, dev/rules/development-environment.md, dev/rules/working-agreements.md
**In brief**: A release of Cairn is certified when its whole test suite has passed once on a Mac, once on Linux and once on Windows, and the three results are written in the release note.

## Decision summary

**What you noticed.** Cairn 0.8.0 was certified by one full test run on the Mac. The records that the release steps ask of the Mac and of Windows, and the check that joins them, were waived at the cut, and Linux has never been tested as a whole. You wrote on 2026-11-21 that "excluding Windows and Linux certification was a defect", and that v0.8.1 is to be certified on all three platforms.

**The change, in its simple form.** Before a release is cut, the whole suite is run once on each of the three platforms, at the release commit, under Python 3.13. Each result is written in the release note: the platform, the commit, the counts, and every test skipped on that platform with its reason. A release is certified when all three have passed. No code is added.

**What changes.**
- Two documents: the rule on certifying runs and the release steps.
- The Linux machine gets Python 3.13.
- A test that cannot pass on a platform is marked to skip there, with its reason written in the test.
- The record and join commands of the release check, which were waived at 0.8, are not used for v0.8.1. Whether to keep, extend or remove them is left to the tightening.

**What it costs.** One full run on each platform at every release. It took 61 minutes on the Mac at 0.8 (measured); Linux and Windows have never been timed. Before v0.8.1 the suite must first be made to pass on Linux and on Windows, and nobody can size that until each has run once.

**This is the narrowed form.** The proposal first asked for a stricter check in code: three machine-written records and a join that refuses a missing host. Both reviews below are of that form. Asked to choose between the two, you wrote: "Yes, the simple way". What was dropped is listed under Scope delta.

## Context

- **Today's rule.** The certifying run is the full suite on a clean tree under Python 3.13 (`dev/rules/certifying-runs.md`). The release steps then ask for a machine-written record from the Mac, one from Windows, and a join of the two (`release/RELEASE_PROCESS.md`).
- **0.8.0.** The Mac full run gave 1 failed, 5,894 passed and 66 skipped in 60:41 (`dev/measurement/certification-run-2026-11-19.md`). The two records, the join and both secrets scans were waived (`dev/PLANNING.md`, "Checks waived at the 0.8 cut").
- **Linux.** The shared virtual machine runs Ubuntu 24.04 with Python 3.12.3, 2 cores and 3 GiB of memory (`dev/rules/development-environment.md`). No full Linux run exists, so the number of tests that fail there is not known.
- **Windows.** The last counted run on the Windows virtual machine gave 15 failed, 305 passed and 27 skipped (2026-11-16). The six measurements that plan D2 of the defect arc waits for have not been taken.

## Proposal

**A. The rule.** `dev/rules/certifying-runs.md` says that a release is certified by one full run on each of the three platforms, at the release commit, under Python 3.13, and that the three results go in the release note. A platform whose run did not pass is not certified. Only the Maintainer can cut without it, in words quoted in the release note.

**B. The release steps.** `release/RELEASE_PROCESS.md` names the three runs and their order, and says that the record and join commands are not part of the v0.8.1 cut.

**C. Linux.** Python 3.13 is added to the shared Linux virtual machine in its user's own folder, built from the official python.org source and checked against its published checksum, as Git was on that machine. `dev/rules/development-environment.md` records where it came from. It is a download on the Maintainer's machine, so it waits for his word in the Mac session.

**D. Making the suite pass.** The suite is run once on Linux and once on the Windows virtual machine, to see what fails. Each failure is fixed, or the test is marked to skip on that platform with its reason. On Windows this is the work that plan D2 of the defect arc was waiting for. Each fix is an ordinary change, checked by the fewest tests that show it is right.

**E. The secrets scans** that were also waived at 0.8 are not changed here; they are due at the v0.8.1 cut.

There is no plan. The two documents are edited under this proposal. C and D happen in the Mac session, which reaches both virtual machines.

## Rationale

The simplest thing that shows a release works on a platform is to run its tests there once. The stricter check adds code to a file the Maintainer signs and runs the suite twice on each host, and at 0.8 that same machinery was waived and never run.

## Alternatives considered

- **The stricter check in code,** this proposal's first form. Dropped by the Maintainer's choice; whether it returns is the tightening's question.
- **Do nothing.** v0.8.1 is certified on the Mac alone again.

## Documentation / doctrine surface

`dev/rules/certifying-runs.md` and `release/RELEASE_PROCESS.md` (the governing and release layers); `dev/rules/development-environment.md` (the Linux machine's Python); the roadmap's section 2 row and its entry "Checks waived at the 0.8 cut". No shipped template changes.

## Evidence / verification plan

It worked when the release note of v0.8.1 holds three passing full runs at one commit, one for each platform.

### Tests required

None is added. The suite is the evidence.

### Examples / smoke checks

`python tests/check_cairn.py` on each changed document.

#### Security preflight

N/A in this form: no code changes and no trust boundary is added or widened. One thing a reader should know: the three results are copied by hand from each run's output, so only the reader checks that they come from the same commit.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Dozens of tests end up skipped on Linux, so its run says little. A release's three runs take more than a working day of machine time. The virtual machines fail tests for their own reasons, such as 3 GiB of memory, more often than Cairn does. A result in a release note turns out to come from another commit.

## Scope delta

**Scope delta**: lost

- The three machine-written records and the join that requires all three, the first form's outcome A. **disposition**: accept, by the Maintainer's words of 2026-11-21: "Yes, the simple way". If it returns, its home is the tightening.
- The Mac-only class in the pinned list of native tests, outcome B. **disposition**: accept, same words. A test that cannot pass on a platform is skipped there with its reason.
- Two runs in two orders on each host. **disposition**: accept, same words: one run on each.

## Assurance path

**Assurance path**: standard

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

## Response to the Maintainer's choice -- Claude Fable 5.2 (Strategy) -- 2026-11-21

The operative text above is rewritten once, in place, for the simple form. Git keeps the form the two reviews read (`40a88e40`).

After both reviews were folded, the Maintainer set a standing direction on testing (chat, 2026-11-21): "Just do all of the changes we need. Then run the fewest tests possible to make sure it was right. Then we re-anchor, certify on all three platforms, and cut." Strategy then judged its own proposal too heavy: it added code to the release check and ran the suite twice on each host. Strategy offered him two ways: "(a) Certify v0.8.1 the simple way: the whole suite once on each of the three platforms, results written in the release note, no new code. I recommend this. (b) Build the stricter check now." He wrote: "Yes, the simple way".

What the rewrite does: it keeps the goal (three platforms) and the work that any form needs (Python 3.13 on Linux; making the suite pass on Linux and Windows), and drops the code. The proposed tier falls from heavy to light, because no high-risk surface changes: two rule and release documents are edited. His words also settle the first form's fourth choice: v0.8.1 itself is certified this way.

No new review pass: the Maintainer removed scope and added none.

### Withdrawn / superseded commitments

- The three-record join, the removal of the two-host join, and every test listed for them. Withdrawn; see Scope delta.
- The Mac-only class in the pinned list, and the rule that moving a test into it takes a Security Review and a re-signing. Withdrawn with the class.
- The requirement that all three records carry the history scan. Withdrawn with the records; the secrets scans stay due at the cut.
- Choices 2, 3 and 4 of the first form. Settled by the simple form: a waiver is the Maintainer's words in the release note; a test that cannot pass on a platform is skipped there with its reason; v0.8.1 is the first release certified this way.

**Elapsed**: unknown. **Tokens**: unknown.

## Decision -- Maintainer (scribed by Claude Fable 5.2) -- 2026-11-21

**Tier**: light

**ACCEPTED, in the simple form.** Strategy asked: "(a) Certify v0.8.1 the simple way: the whole suite once on each of the three platforms, results written in the release note, no new code. I recommend this. (b) Build the stricter check now." The Maintainer wrote (chat, 2026-11-21):

> "Yes, the simple way"

Earlier the same day he had written: "Then we re-anchor, certify on all three platforms, and cut."

What that settles:

- **The simple form is accepted,** as the operative text above states it: one full run on each of the three platforms, the results in the release note, no code.
- **v0.8.1 itself is certified this way.**
- **The stricter check is not built.** Whether the record and join commands are kept, extended or removed is left to the tightening.
- **Tier: light.** It was not put to him as a separate question. The revised proposal proposes light, because only two rule and release documents change, and by the template a proposed tier stands unless the Decision changes it.
- **Still his to say, in the Mac session:** adding Python 3.13 to the Linux machine, because it is a download on his machine.

**Elapsed**: unknown. **Tokens**: unknown.
