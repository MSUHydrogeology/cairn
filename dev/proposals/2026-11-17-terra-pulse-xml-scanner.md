# Classify Pulse's guarded XML scanner finding

**Author**: Terra Medium, proposal author; security design assessed by Sol High
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — changes an existing security-check exception
**Plan review**: not required(no separate plan: connected Group 2 repair; the coordinator assigns explicit shared ordinary and Security code-review coverage with the release-test changes)
**Opened**: 2026-11-17
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/working-agreements.md
**In brief**: Keep scanning Pulse's report reader, but classify its already-guarded XML call as an accepted scanner finding.

## Decision summary

The security scanner blocks release checks because Pulse uses a standard XML
reader. It identifies the reader's name without considering Pulse's existing
checks that reject document definitions and entities, which can make XML unsafe.
Proposed: add one explained exception in the existing scanner settings. No
parser, tool, test or installed file changes.

The exception covers this scanner rule throughout one file, including a future
call added there. That is the tradeoff requiring your acceptance. The scanner
continues reporting it, and the gate rejects an exception whose finding disappears.

## Context

At `fbb53ebb`, the release-test implementer reports Bandit's B314 finding at
`templates/skills/_lib/pulse.py:166`, failing the security-lint check and the
connected public release-record fixture. Sol's read-only comparison found the
bounded reader and parser identical to their pre-extraction implementation in
`8cec9b83^:tools/gauge.py`; shipping Pulse brought that call into the scanner.
This assessment covers document-definition and entity expansion, not all XML
resource-exhaustion risks.

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

The coordinator owns this post-archive repair. The ordinary and Security code
reviews of the release-test changes must explicitly cover this correction too;
neither the archived Pulse plan nor its completed reviews are reopened.

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
  this one matching path/rule is permitted.
- **S5:** A future unsafe B314 call in this file would share the allowance;
  source review must reassess it. No general XML-safety claim is made.

### Independent scientific check

N/A: no scientific assumption or result changes.

## Signals the change is wrong

A forbidden XML input is accepted, another finding stops blocking, or the
scanner no longer reports the allowed finding while the gate passes.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance. This proposes a security-policy change;
no source modification or exception is authorized before the Maintainer decides.

**Elapsed**: approximately 5 minutes including triage. **Tokens**: unknown.
