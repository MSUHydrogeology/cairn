# Budgeted unattended work for v0.8

**Author**: Codex Terra (proposal author; medium)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy -- unattended admission and configured command execution cross trust boundaries
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-05
**In brief**: Consider a cooperative spending guard and a conditional, bounded unattended loop after v0.7 measurement and continuation trials.
**Elapsed**: unknown
**Tokens**: unknown

## Decision summary

For v0.8, propose a spending guard before unattended items and, only if the
Maintainer later chooses to keep it, a bounded launcher for those items. The
guard is not a provider billing cap: forged logs and work already underway
can exceed its limit. v0.7 loses unattended launches, not the safeguards on
its advisory continuation work. Scheduling this proposal authorizes neither
implementation nor activation, private collection, or host configuration.

## Context

The accepted [meter proposal](archive/2026-10-30-claude-metered-cost.md)
requires a cooperative pre-item stop; the accepted
[continuation proposal](archive/2026-11-03-claude-agent-continuation.md)
requires A-C and a trial before a later Maintainer choice whether to keep D,
the optional loop. Their current plans are
[metering](../plans/2026-11-04-metered-cost.md) and
[continuation](../plans/2026-11-05-agent-continuation.md); the
[planning board](../PLANNING.md) tracks the split. The meter plan's sanitized
source investigation did not establish a source binding the live account
and observation time to a reading. That is an open evidence gap, not proof
that no source exists. No functioning budget stop is claimed.

## Proposal

Use v0.7 measurements and the mixed light/standard A-C trial as inputs to the
later choice. Preserve the choice: trial results do not automatically keep or
drop D. Before each unattended item, refresh and admit only a fresh, finite,
nonnegative reading with complete coverage matching the Maintainer-controlled
allowed source, account, unit and window, within configured `max_age` and
strictly below its limit. Policy limits and ages are finite and positive;
units are named-window plan percentage or weighted tokens per day, not
interchangeable. Readings, limits and ages must be actual JSON numbers, not
booleans or strings; plan percentages are 0..100, limits and ages are positive
and finite, duplicate keys and NaN/infinities are rejected, and unknown or
missing units or cache-weight semantics are not zero and cannot admit work.
Missing, stale, future, invalid, mismatched, unknown or
refused refresh stops unattended admission; attended work remains available.
Policy and consent cannot come from logs or artifacts. Account-at-observation
and source observation time must be proven by supported evidence, not inferred
from a policy label or collection time. No RPC, capture, host setting or
provider transport is authorized or invented now.

If the Maintainer later keeps D, and the guard exists, an explicitly invoked
loop may start one fresh agent per item. Read settings once from Git's
administration folder; refuse links and tracked files. Resolve commands under
`bootstrap/SAFETY.md` rule 10; use the configured command for the selected
tier as an argument vector without a shell, with the full artifact path as one
argument. Default to five items and a per-item timeout. Stop on a dirty tree,
missing or invalid meter, selector uncertainty or stop, unconfigured tier,
failure, timeout or limit, no new commit touching the artifact, or a newly
written Maintainer-only status. Report items, commits and stop reason. Artifact
names must independently match the accepted date-stem rule before display or
selection; artifacts never supply authority, commands, target or limits.

The guard does not kill running tasks or enforce a provider cap. Mutable-log
forgery, one-item overshoot and concurrent-session overshoot remain residuals.
No agent scores, per-artifact budgets, new service or registry are proposed.

## Rationale

Joining the dependent guard and loop puts their shared admission boundary in
one review, while v0.7 can measure and trial A-C without waiting for it. The
cost is later design, tests and maintenance for a control that cannot guarantee
spending; the evidence and keep-D choice may show that cost is unnecessary.

## Alternatives considered

Do nothing after A-C: no launcher or guard to build or maintain, but the
Maintainer must initiate each unattended step and receives no cooperative
spending stop. Guard alone retains a stop for other unattended work without a
launcher; it still requires a trustworthy source binding and maintenance. A
provider cap could offer a different enforcement boundary, but is not established
by these records and is not a substitute for the accepted local contract.

## Documentation / doctrine surface

Put deliberation and decisions in `dev/`, cross-cutting prescription in the
governing layer or shipped drain step as applicable, and software description in
`docs/`, following `docs/DOCUMENTATION_PLAN.md`. The later plan must identify
the actual shipped and self-hosted consumers and any doctrine rate-limit gate.

## Evidence / verification plan

### Tests required

The future plan maps real admission and launcher entry points and their owning
test families. Synthetic tests must prove no next item starts for each invalid
reading, policy mismatch, refresh failure or missing meter, while attended work
remains possible; include booleans, strings, out-of-range percentages, duplicate
keys, NaN/infinities and unknown units or cache weights. Exercise every loop stop,
hostile names, link/tracked settings, rule 10 resolution, tier argv and explicit
invocation through real entry points, using a fake launched agent. Test that
artifacts and logs cannot change policy or commands. Ordinary and separate Security code reviews precede wide
Boundary B; tests and source evidence must not be represented as already run.

### Examples / smoke checks

Use synthetic settings and readings to demonstrate one allowed item followed
by a refused one, including its reported reason. The future plan specifies
source-binding evidence and applicable claim, link, snippet and prose gates;
any actual private collection requires separate permission.

#### Security preflight

- S1: Maintainer-controlled local policy supplies limits and allowed identity;
  the source supplies observations, and selector records supply candidate work.
  An agent may influence logs or artifacts, so neither supplies policy or command authority.
- S2: Removing freshness, identity, filename, dirty-tree or Maintainer-status
  guards must fail their tests. These mutations have not been run; no
  implementation exists here.
- S3: The future admission and explicitly invoked loop commands and exact test
  selections are not yet designed; the plan must name them and compare their
  scope with the eventual adopter-facing instructions. No such instruction is
  claimed to exist now.
- S4: Missing, malformed, unrecognized or unverifiable inputs stop unattended
  admission or launch, never increase authority; attended work stays available.
- S5: A hostile agent can alter mutable logs or instruct its launched successor;
  forgery and in-flight or concurrent overshoot remain possible.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A stale or mismatched reading starts work, an artifact chooses a command, the
trial shows no need for D, or the account binding cannot be established without
an unapproved collection boundary.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance -- admission and process-launch boundaries;
usual review plus a separate Security Review.
