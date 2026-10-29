# Find a safe test-family speed improvement

**Author**: Codex (GPT-6, proposal author)
**Status**: awaiting-review
**Review**: usual
**Plan review**: required(Internal)
**Opened**: 2026-10-29
**In brief**: Use timing from the next authorized certification to identify one test-family improvement without sacrificing fault detection.

## Context

A clean single-process certification at `7c910851` took 24 minutes 55 seconds
for 5,479 passes on Python 3.13.13, above the ten-minute budget recorded in
`dev/PLANNING.md`. This is historical, not a timing of the current tree.
`dev/strategy/2026-10-29-codex-certifying-run-cost.md` found no current
per-family timing and recommends using the next already-required certification.
The archived `dev/plans/archive/corpus-tier-cost.md` shows why a blanket cache
is unsafe: some tests assert real subprocess behavior, and other families had
little repeated work. Its measurements too are historical.

## Proposal

Conduct a bounded audit, not a suite rewrite. On the next independently
necessary, authorized clean certification, add `--durations=0 --durations-min=0` to the
existing fixed-seed suite command and retain its complete report, commit,
interpreter, command, and machine activity. Do not run an extra full suite for
this audit. Aggregate reported setup, call and teardown times by family, noting
reporting limits and missing phases. Rank the costly families; inspect at least
the leading ordinary candidate and its installed protection classification.

For one eligible candidate, inventory its behavioral properties and real entry
points, identify repeated work, and measure its scoped command on the same
committed bytes under stated conditions. Produce a concrete improvement proposal
only if the evidence supports a useful reduction while preserving those
properties. Specify targeted faults and how the existing and proposed tests
would detect each, including a control. If no candidate meets that bar, record
why and stop. The audit does not authorize changing tests, their protection,
the certification contract, or dependencies. Installation of the forward
baseline remains a separate Maintainer-authorized work item.

## Rationale

One observed family gives the next change a measurable target without assuming
that historical bottlenecks persist. Reusing a required run avoids paying for
another broad run. An audit may conclude that no safe worthwhile optimization
is visible; no suite-wide speedup is promised.

## Alternatives considered

Do nothing leaves the historical over-budget certification cost unexplained.
Parallel execution may be faster but introduces a dependency and ordering and
isolation questions without evidence that it is the best current lever. Reusing
a prior memo elsewhere assumes repetition and safety that have not been shown.

## Documentation / doctrine surface

The audit result belongs in the deliberation layer under `dev/`; any later
implementation and descriptive documentation require their own scoped
proposal. No doctrine or governing rule changes are proposed.

## Evidence / verification plan

The audit must show the source report and ranking, the selected family's
properties and entry points, protection classification, scoped baseline command
and phase timings, and a fault-detection matrix with controls. A missing duration
report, an ineligible candidate, or faults that surviving tests cannot detect
precludes an optimization recommendation. Timing is observational and must
not be presented as a controlled before/after improvement. Any later change
must measure the same scoped command before and after and demonstrate fault
protection before claiming a gain.

### Tests required

The audit changes no behavioral test; its eventual plan identifies the selected
`bootstrap/tests/` nodes and real entry points after the timing is available.
The existing certification remains governed by its authorization and fixed
shuffle seed. No added full run is required.

### Examples / smoke checks

Run `python scripts/claim_check.py` on the proposal and the applicable prose
integrity checks; verify the retained duration report actually includes setup,
call and teardown phases before treating absence as evidence.

#### Security preflight

N/A: no trust boundary added, moved, or widened.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

The timing report cannot support a family ranking, the eligible families are
not responsible for meaningful cost, the scoped measurements are unstable, or
the proposed fault controls expose lost protection. In those cases report the
limitation instead of claiming a speed improvement.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: standard
