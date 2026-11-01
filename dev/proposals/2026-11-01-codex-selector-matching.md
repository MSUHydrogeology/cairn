# Reduce incidental test-selector matches

**Author**: Codex GPT-6.1
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: not required(no plan: light tier)
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
but retains a measured broad run and its repeated cost. Inspect current matches
and retain the selector unchanged if a reliable small rule is not found. Use
paths only: smaller, but misses legitimate imports and indirect command consumers. Manually curate a
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

**Assurance path**: high-assurance, proposed as a precaution because selection
can omit required checks. Neither review identified a named high-risk surface
or an added or widened trust boundary. Heavy remains the proposed tier until
the Maintainer decides; the Maintainer may choose light, retaining the same
consumer-preservation criteria and required checks. If implementation needs a
protected surface or a new boundary, stop for reassessment.

## Proposal review -- Codex GPT-6.1 -- 2026-11-01

**Verdict**: Revise the assurance rationale; the narrowing itself is worth pursuing.

1. **Should it happen as framed?** Yes: the selector treats every occurrence of a Python stem as a match, and the collision record shows 51 selected files without claiming all are incidental. The proposal preserves ambiguous consumers and stops if a small rule cannot distinguish them. That is a useful, testable limit, not a claim of complete dependency discovery.
2. **Best alternative.** Keep the existing selector and inspect its real selections before changing only matching. The actual upgrade tests include both `from bootstrap._scaffold import upgrade` and dotted imports, while the collision plan names public-command and hostile-data tests; these examples make a path-only rule inadequate. Avoid a permanent mapping or new reporting machinery.
3. **What would show it wrong?** A real import or identified public-command consumer disappears, a representative incidental match remains, or the rule needs enough exceptions to erase its savings. Compare the real entry point on the recorded inputs and preserve the named consumers with regressions.

**Finding, advisory -- tier**: The heavy rationale cites potential omission of security checks, but `tools/test_tiers.py` is not among the named high-risk surfaces in `AGENTS.md`, and the proposal says no new trust boundary is intended. Potential error alone does not establish a named high-risk surface or widened boundary. Recommend light, the default, with the same targeted consumer checks; identify a concrete trigger if one exists. The Maintainer sets the tier.

**Coverage**: Read the committed proposal, selector, governing verification and high-risk rules, selector test and representative upgrade import and public-command test references, and the collision plan's mapping and run record. Did not inspect every selected consumer, run tests, or perform Security Review. Elapsed: approximately 5 minutes; tokens: unknown.

## Security Review -- Codex GPT-6.1 -- 2026-11-01

Reviewed commit: 4fd95510b07d193f0616705b82643d4504964d41.
Target: consumer preservation. Prior findings: none. Assurance path: high-assurance.

**Tier**: Security Review
**Foundations**:

1. **Should this happen as framed?** Yes. The current selector adds bare Python stems and uses substring membership (`tools/test_tiers.py`, `tests_for_paths`); the proposal explicitly retains ambiguous consumers and requires reassessment when reliable exclusion fails.
2. **Best alternative.** Keep current matching until inspected examples support a smaller rule. Import/path-only matching is insufficient: `bootstrap/tests/test_upgrade.py` exercises the public `s.main` command, and `bootstrap/_scaffold/cli.py` dispatches the upgrade command to `cmd_upgrade`. This is a real indirect dependency, not incidental prose.
3. **What would show it wrong?** A known indirect command consumer disappears from real-entry-point selection, or import/path regressions fail. The proposed regressions and committed comparisons address this; counts alone cannot establish safety.

**Verdict**: ACCEPT; no blocking security finding.

**Finding S1, advisory -- tier rationale**: Potentially omitting checks is a credible failure mode, but alone does not demonstrate a mandatory heavy trigger. `AGENTS.md` names protected control machinery without expressly naming this selector; the proposed change adds no trust boundary or governing-rule change. Recommend light with the same consumer safeguards unless the Maintainer identifies a concrete protected-surface classification. This removes later review stages, preserving functional outcomes and checks. Close by explaining the classification or recording the Maintainer's tier choice; the author's heavy tier stands until Decision.

**Elapsed**: approximately 5 minutes. **Tokens**: unknown.

**Coverage**: Committed proposal, selector, governing tier rules, selector regressions and representative public-command dispatch. **Not covered**: exhaustive consumer inventory, implementation behavior or mutations; no tests run.

## Response -- Codex GPT-6.1 -- 2026-11-01

- Ordinary advisory, tier: accepted the distinction; no concrete mandatory
  heavy trigger was established. The proposal now states that heavy is a
  precaution and light is a Maintainer option with the same safeguards.
- Security S1, tier rationale: accepted for the same reason; the proposed
  tier remains heavy pending the Maintainer's Decision.

**Elapsed**: approximately 2 minutes. **Tokens**: unknown.

### Withdrawn / superseded commitments

None.

## Decision -- Maintainer -- 2026-11-01

Elapsed: unknown; tokens: unknown.

**Tier**: light

**ACCEPTED.** The Maintainer's authorization, quoted verbatim:

> "Accept light and implement"

## Code review -- Codex GPT-6.1 -- 2026-11-01

Reviewed commit: d714596d82d9da0c3ce933fb6bde21d3b3ff7c8b.

1. **Should it happen as framed?** Yes, provided imports remain selected: the accepted criteria require retaining genuine imports while reducing incidental stem matches.
2. **Best alternative.** Keep the previous conservative matcher until a small rule handles valid imports; the committed selection still retains `test_upgrade.py` and `test_upgrade_refuses_hostile_project_data.py`, and the added regression distinguishes incidental words.
3. **What would show it wrong?** A valid import omitted by the real entry point. A committed-copy probe containing `from bootstrap._scaffold import (\n    upgrade,\n)` was omitted when selecting `bootstrap/_scaffold/upgrade.py`; the expression limits imported names to the first line.

**Verdict: REVISE. Blocking:** The omitted multiline import violates the accepted import-preservation criterion and can leave required verification unrun. Handle valid multiline and multiple-name imports conservatively, and exercise them through the real selector. The committed selector regression only covers a single-line import.

**Coverage:** Read the implementation and selector regressions, including changed-test and AGENTS reviewed-range logic; checked the public upgrade consumers and probed the real command in a separate copy of the reviewed commit. An AST scan found no such currently omitted direct imports in the committed top-level test files. Did not exhaust indirect consumers, rerun implementation checks, or perform Security Review. Elapsed: approximately 4 minutes; tokens: unknown.

## Code review re-look -- Codex GPT-6.1 -- 2026-11-01

Reviewed commit: d3bc1e529b7c672d92b0a594ba838ba7920f84b0. **Finding closed.** The revised expression matches the stem inside the parentheses; a separate copy of the commit selected a probe containing a parenthesized multiline import with multiple names via `tools/test_tiers.py for bootstrap/_scaffold/upgrade.py`. The committed regression covers the reported form and a near-match exclusion. Covered the correction to the import finding only; did not rerun implementation checks or revisit other consumer coverage. Elapsed: approximately 2 minutes; tokens: unknown.
