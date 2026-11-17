# Classify Pulse's guarded XML scanner finding

**Author**: Terra Medium, proposal author; security design assessed by Sol High
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy — changes an existing security-check exception
**Plan review**: required(Internal + Internal Security Review), unless the Maintainer grants the explicit limited exception requested below
**Opened**: 2026-11-17
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/working-agreements.md
**In brief**: Keep scanning Pulse's report reader, but classify its already-guarded XML call as an accepted scanner finding.

## Decision summary

The security scanner blocks release checks because Pulse uses a standard XML
reader. It identifies the reader's name without considering Pulse's existing
checks that reject document definitions and entities, which can make XML unsafe.
Proposed: add one explained exception in the existing scanner settings and fix
file-name matching so the same exceptions work on Windows. Extend one existing
check; no parser, tool or installed file changes.

The exception covers this scanner rule throughout one file, including a future
call added there. That is the tradeoff requiring your acceptance. The scanner
continues reporting it, and the gate rejects an exception whose finding disappears.
For this one settings entry, I also request permission to use this proposal's
exact implementation instructions and the ongoing code reviews instead of
adding a separate plan and plan reviews. Required code reviews and checks stay.

## Context

At `fbb53ebb`, the release-test implementer reports Bandit's B314 finding at
`templates/skills/_lib/pulse.py:166`, failing the security-lint check and the
connected public release-record fixture. Sol's read-only comparison found the
bounded reader and parser identical to their pre-extraction implementation in
`8cec9b83^:tools/gauge.py`; shipping Pulse brought that call into the scanner.
This assessment covers document-definition and entity expansion, not all XML
resource-exhaustion risks.
The first Security Review also identified a Windows defect: `_rel` returns
backslash-separated relative paths there, while exception keys use forward
slashes. Without correcting that, the exception would not match on Windows.

## Proposal

For v0.8, add only the existing `bootstrap/security_check.py` allowlist key
`("templates/skills/_lib/pulse.py", "B314")`, with this rationale:

> `_parse_pulse_report` parses only bounded UTF-8 text after rejecting NUL,
> non-UTF-8 declarations, DOCTYPE and ENTITY; the input checks precede its
> sole ElementTree call. Reassess this path/rule allowance if that changes.

Update the adjacent comment describing the entries so it also names guarded
XML parsing. Leave scanner targets, blocking severity, other findings,
exception liveness, and Pulse's guards unchanged. Keep the expected frozen-file
change with the existing release-cut baseline wait; it does not block archive.

In `_rel`, replace only
`str(Path(filename).resolve().relative_to(CAIRN_ROOT))` with
`Path(filename).resolve().relative_to(CAIRN_ROOT).as_posix()`. Preserve resolution,
repository containment and the outside-repository fallback. This uses the same
forward-slash keys on every host; no new finding is allowed beyond those keys.
Extend `test_a_live_allowlist_entry_passes` to exercise its public `run_bandit`
route with both ordinary and Windows-style relative path representations. The
Windows case must fail with the old conversion. This models path rendering;
it does not claim a native Windows scanner run or full release record.

The coordinator owns this post-archive repair. The ordinary and Security code
reviews of the release-test changes must explicitly cover this correction too;
neither the archived Pulse plan nor its completed reviews are reopened.
If the Maintainer does not explicitly grant the limited plan exception, open
a plan with both required plan reviews before implementation. No current plan
is claimed to have already approved this allowance.

## Rationale

Classifying the reported finding retains the scanner and the existing parser
protections without rewriting working code merely to evade a scanner pattern.

## Alternatives considered

Keep the finding blocking: no policy change, but the connected release checks
remain broken. Replacing the XML parser adds implementation burden unrelated
to the demonstrated scanner limitation. Inline suppression hides the finding
from the existing live-exception check.

## Documentation / doctrine surface

One rationale and adjacent comment in the existing security command; this
proposal records the decision. No methodology or shipped guidance changes.

## Evidence / verification plan

### Tests required

Use the existing public checks, with canonical Python 3.13:

- `bootstrap/tests/test_security_lint.py::test_no_blocking_security_findings`;
- `bootstrap/tests/test_security_check.py::test_run_bandit_clean_with_bandit_present`;
- `bootstrap/tests/test_security_check.py::test_a_live_allowlist_entry_passes`,
  extended as specified above, plus the existing stale-entry and unallowlisted
  finding controls;
- `bootstrap/tests/integration/test_gauge.py::test_invalid_xml_and_impossible_counts_fail_without_echoing_input`;
- `bootstrap/tests/integration/test_gauge.py::test_utf16_and_nul_are_rejected_before_xml_parsing`.

After the correction commits, retry only the blocked
`bootstrap/tests/test_security_check.py::test_committed_fixture_connects_real_record_and_join_entrypoints`.
No new permanent tests or broad suite. Retain failures as failures until these pass.

### Examples / smoke checks

Claim and link checks on this proposal; the real scanner checks above establish
that the exception is live rather than relying on an invented finding.

#### Security preflight

- **S1:** The gate reads its committed allowance and Bandit's report; the report
  being classified does not set the allowance.
- **S2:** Existing hostile XML and UTF-16/NUL public cases must still reject.
  Existing scanner tests exercise unallowlisted findings and stale allowances.
- **S3:** The security-lint test and release command run Bandit over its existing
  targets, including shipped Pulse. No target is removed.
- **S4:** Scanner errors, unrelated findings and stale allowances still fail;
  this one matching path/rule is permitted. Separator conversion happens only
  after the existing resolved-repository-relative operation succeeds; outside
  paths retain their existing unmatched fallback.
- **S5:** A future unsafe B314 call in this file would share the allowance;
  source review must reassess it. No general XML-safety claim is made.

### Independent scientific check

N/A: no scientific assumption or result changes.

## Signals the change is wrong

A forbidden XML input is accepted, another finding stops blocking, or the
scanner no longer reports the allowed finding while the gate passes.

## Scope delta

**Scope delta**: preserved; expanded before Decision to correct Windows path
matching identified by the first Security Review. No original outcome is lost.

## Assurance path

**Assurance path**: high-assurance. This proposes a security-policy change;
no source modification or exception is authorized before the Maintainer decides.

**Elapsed**: approximately 5 minutes including triage. **Tokens**: unknown.

## Ordinary proposal review -- Terra (Reviewer, Medium) -- 2026-11-17

**Steelman.** Unblock the release scanner by classifying one guarded XML finding, while preserving the scanner and making the path-wide tradeoff visible to the Maintainer.

1. **Should this happen as framed?** Revise the routing before a Decision. **Blocking:** `AGENTS.md` requires a plan for a non-trivial heavy proposal; the release plan's Scope and C1–C5 specify the shipped-only selection, not this allowance. Shared reviews are allowed, but the proposal's “Plan review: not required” does not identify a reviewed plan covering this work. Close by specifying a plan route consistent with that requirement, including the applicable plan review, without reopening completed Pulse reviews. The proposal otherwise makes the future same-file B314 exposure legible; `finding_key` and `observed` in `bootstrap/security_check.py` confirm path/rule matching and liveness, not call-site isolation.
2. **Best alternative?** The existing allowlist is the smallest identified mechanism: `pulse.py` rejects NUL, non-UTF-8 declarations, DOCTYPE and ENTITY before `ET.fromstring`, and the release failure is recorded in commit `fbb53ebb`. Keeping the block leaves that failure; changing parsers adds work. This is static evidence, not a new security assessment.
3. **What would show it wrong?** The named public scanner and hostile-input checks failing after implementation would contradict the proposed behavior; a later unsafe B314 call could also share the allowance while the original remains live. Review that risk whenever the file changes.

**Audience and rule loss:** The Decision summary states the choice and tradeoff without translation; this proposal changes no installed authoritative instruction. **Coverage:** Read the proposal, current plan routing, reader guards and scanner filter/liveness. Did not run tests, assess all XML risks, or repeat the separate Security Review, which remains required. Elapsed: approximately 5 minutes; tokens: unknown.

## Security proposal review -- Sol (Security Reviewer, High) -- 2026-11-17

```
Reviewed commit: 679927e46ffa4006146367f4267f961eea56d4f4
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: ACCEPT

**Elapsed**: approximately 2 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes, subject to the Maintainer accepting the file-wide B314 exception and disposing of plan routing. The only parser call receives at most 8 MiB per report and follows NUL, UTF-8, declaration, DOCTYPE and ENTITY checks. The byte bound leaves XML processing costs outside this review's assurance. `templates/skills/_lib/pulse.py:24`, `:148`, `:682`.
2. **Best alternative.** A call-specific matcher would narrow future exposure at the cost of changing shared scanner policy. The proposed entry reuses the existing matcher: any blocking result with that path and rule keeps it live, including a future result at a different call. `bootstrap/security_check.py:1356`, `:1497`.
3. **What would show it wrong?** A forbidden input passing, or any named scanner or connected fixture check failing, would leave the repair incomplete. The public XML controls drive `tools/pulse.py`, whose committed blob matches the shipped copy. `bootstrap/tests/integration/test_gauge.py:621`, `bootstrap/tests/test_security_check.py:960`, `:1857`.

**Non-blocking finding.** Native Windows paths render with backslashes while `_rel` applies no separator conversion. Slash-key matching on Windows remains unverified. Limit the claimed repair to the checks that pass on their actual host. `bootstrap/security_check.py:1335`.

**Coverage.** Read committed parser, filter, liveness and test entry points. `fbb53ebb` records the lint failure and `45fe2fc2` the fixture failure. Checked Windows path rendering with `PureWindowsPath`. No runtime scanner, fixture or native Windows run, and no general XML resource-exhaustion assessment.

## Targeted ordinary review -- Terra (Reviewer, Medium) -- 2026-11-17

**Steelman and verdict:** The widened proposal makes existing exception keys work on Windows while keeping containment and the fallback; accept subject to the Maintainer's explicit plan-routing Decision and the separate Security pass.

1. **Should it happen?** Yes. `_rel` currently converts the resolved relative `Path` with `str` and returns the original filename on `ValueError`; the specified replacement changes only the successful conversion. The revised header requires both plan reviews unless the Maintainer expressly grants the requested exception, resolving my routing finding as a Decision choice.
2. **Best alternative?** Reusing `as_posix()` and the existing public live-entry test avoids a new matcher. **Non-blocking:** the summary says “no ... tool ... changes,” although `bootstrap/security_check.py` changes; clarify that no installed Pulse tool changes.
3. **What would show it wrong?** The extended public test must fail under the old conversion and pass under the new one; existing stale and unallowlisted controls must still pass.

**Coverage:** Reviewed the widened diff, `_rel`, and test location; no tests, native Windows execution or renewed security assessment. No installed instruction is removed. Elapsed: approximately 2 minutes; tokens: unknown.
