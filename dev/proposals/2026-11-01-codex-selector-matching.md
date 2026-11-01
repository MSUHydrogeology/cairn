# Reduce incidental test-selector matches

**Author**: Codex GPT-6.1
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Make the test selector distinguish file references from incidental words so scoped verification runs fewer unrelated tests.

## Context

`tools/test_tiers.py` selects a test when its source contains any candidate
needle; for Python files one needle is the bare stem. Thus `upgrade.py` matches
unrelated uses of “upgrade” as a substring. The collision plan's Boundary B
record reports 51 selected files, 3,130 passing tests and 344.62 seconds across
five test commands on Python 3.13.13; its seven explicitly mapped files account
for 517 tests and 85.80 seconds. Those seven are not an exhaustive consumer
inventory. The broad remainder includes incidental prose and fixtures, but its
cost cannot all be attributed to false matches without inspecting it.

## Proposal

Correct `for` matching so incidental stem substrings do not select a test, while
retaining genuine imports, file-name and path citations, and known indirect
command-line consumers. Preserve the governing rule's scope: a test names a
file when it imports it or cites its path or file name. Search the actual
selected tests and callers before choosing the matching rules; retain any
ambiguous real consumer unless its exclusion is justified. Keep changed-test
selection, the `AGENTS.md` reviewed-range and omission behavior, and required
security and integration checks intact. Do not introduce a new diagnostic tool,
per-probe evidence ledger, or changes to the full-suite authorization.

The change succeeds only if it removes demonstrated incidental matches and
preserves the identified real consumers. If that cannot be done reliably with
a small, reviewable rule, stop for reassessment rather than silently dropping
coverage. This proposal does not claim complete dependency discovery.

## Rationale

A narrower interpretation of a Python stem can reduce repeated testing while
keeping references that explain why a test belongs in scope. Real CLI consumers
may refer indirectly to the implementation, so a simple path-only filter can
lose coverage. Exact matching rules must follow the inspected examples rather
than an assumption that every bare word is either a dependency or irrelevant.

## Alternatives considered

Keep the current selector: safest against this class of missed lexical match,
but retains a measured broad run and its repeated cost. Use paths only: smaller,
but misses legitimate imports and indirect command consumers. Manually curate a
permanent fast set: it can drift and changes the existing file-based rule.

## Documentation / doctrine surface

No governing rule or shipped template change is proposed. Describe any actual
selector behavior change in its existing tool documentation if needed; the
proposal and its decision belong in `dev/`. Any necessary change to governing
prescription or a protected surface requires reassessment before proceeding.

## Evidence / verification plan

### Tests required

Use `bootstrap/tests/test_test_tiers.py` and the real `tools/test_tiers.py for`
entry point to test imports, dotted modules, file-name and path references,
changed tests, incidental prose and substring collisions, plus identified real
indirect CLI consumers. Retain the reviewed-range and omission regressions.
Inspect selector results for the collision plan's changed files, documenting
which representative exclusions are incidental and which real consumers remain;
do not claim all omitted files are irrelevant without evidence. Search for
callers, readers and pins and run the mapped checks. A lost known consumer, a
changed security obligation, or no demonstrated reduction falsifies the change.

### Examples / smoke checks

Compare selection on the collision plan's recorded input paths before and after
on committed bytes. Record file counts, representative differences and the
limits of the comparison; counts alone do not prove coverage. No full suite is
authorized by this proposal.

#### Security preflight — five questions, answered in writing

S1: The operator supplies changed paths and optionally a reviewed range; test
source supplies the references being classified. The classified tests thus
supply their own lexical evidence. S2: A test with a real import or identified
CLI consumer removed from selection should fail its regression; this mutation
has not been run and must be checked in implementation. S3: The `for` command
selects files for the scoped run; the governing rule says a test names a file
when it “imports it or cites its path or file name.” Verify the selected cases
against that rule and the actual invocation. S4: An ambiguous reference should
remain selected; a failure to establish a safe exclusion stops the change, since
omission reduces verification. S5: A consumer with no recognized reference
can still be missed; lexical matching is not complete dependency analysis.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Withdraw or revise if a known consumer is omitted, a required security check
is weakened, incidental matches cannot be distinguished reliably, or the
maintenance cost exceeds the demonstrated savings.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance. This changes the selection of required
verification and could omit checks, including security checks; the heavy lane
provides separate Security Review. No new trust boundary is intended.
