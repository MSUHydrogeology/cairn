# Meter agent cost from the tools' own logs

**Author**: Claude Opus 5.5 (Strategy)
**Status**: awaiting-decision
**Review**: usual + Security Review
**Proposed tier**: heavy — the meter reads files outside the repository, a new trust boundary
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Count agents' real token and time use from logs their tools already keep, show it to the Maintainer, and stop unattended runs at a spending limit, without asking agents to report anything.

## Context

The Maintainer wants data to begin a Cairn budgeting capability (chat,
2026-10-30). Self-report has failed: since `3cceb2c0`, all of about 55
filled Tokens entries read `unknown`.

The tools already log every model call. Measured on this machine,
2026-10-30:

- Claude Code keeps one log folder per project; this project's holds 1,752
  files (1.27 GB) and 77,190 distinct model calls, read in 5.4 seconds.
- Codex opens each session file with folder, git remote, branch and commit,
  and logs running and per-turn token totals.
- Three traps: records repeat (7,085 records, 3,118 calls in one session);
  98.3% of tokens are cache re-reads; subagents log separately.
- A claim's id carries the first 8 hex characters of SHA-256 of the tool's
  session id (`tools/_intent/identity.py:45-75`), so logs join to claims.

Cairn measures size, not spend (`tools/gauge.py`, `scripts/token_budget.py`);
`doctrine/rationale.md:584-588` says the cost side is not mechanized.

## Proposal

**1. The meter.** One standard-library script, one small reader per tool.
- **Opted in, private:** reads only log roots and projects the Maintainer
  lists in local configuration. The cross-project ledger lives in a private
  per-user folder, never a repository; each project gets only its own
  aggregates, in its gitignored `dev/measurement/` slot.
- **No message content kept or shown:** parsing may read whole lines, but
  only usage numbers, timestamps and ids are kept. Git remotes are stored
  with credentials removed; errors name a file and line, never its text;
  displayed names pass through `encode_display` (`tools/session.py`).
- **Bounded inputs:** regular files only, no links, a per-line size cap,
  finite non-negative numbers (`NaN` is invalid), reusing
  `_read_regular_bytes` (`tools/session.py:657`). Ledger writes are atomic
  and refuse links.
- **Counting rules:** drop repeated records by message id; keep the four
  token kinds separate; fold subagents into their parent; use a session's
  last running total, never a sum; confirm whether cached input sits inside
  a tool's input figure.
- **Project:** chosen by git remote, so one run covers every project.
- **Gathering (Maintainer's contract, relayed in review):** per-item
  attribution when reliable, otherwise daily totals; refreshed at
  `session-end --handoff`. Because claims are pruned
  (`tools/_intent/record_io.py:288`), the meter keeps its own
  session-to-claim mapping when it first sees a claim. Ambiguous coverage
  is shown, not guessed.
- **Test waiting:** command timestamps give time in test runs and repeats.
- **Incremental:** each run reads only new lines and must equal a full
  rebuild. Missing logs are `unknown`, never zero.
- **Units:** raw kinds, a weighted figure from a price-ratio table, and plan
  percentage where reported.

**2. A pulse report.** `tools/gauge.py --pulse` prints, by week and
project: metered tokens and time per artifact, test-wait time, review passes,
model-tier mix and always-loaded cost, completing the board row.

**3. A cooperative spending stop for unattended runs.** The Maintainer's
local policy names the source and account, one unit (plan percent for a
named window, or weighted tokens per day), the limit and the maximum age of
a reading. Before each drain item the meter refreshes; the item starts only
on a fresh, finite reading in that unit below the limit. Stale, missing,
invalid or mismatched readings stop unattended work. Attended work is never
stopped. This is a between-item stop, not a spending guarantee: one item or
concurrent sessions can overshoot.

**4. Numbers for the Maintainer, not targets.** Agents get no per-artifact
budgets or scores. Budgets come later, from the data, in their own proposal.

**5. Q1 for the Decision.** Retire the self-reported Tokens field once the
meter passes its checks (recommended); keep Elapsed until metered time is
shown equivalent. This changes the Maintainer's apparatus Q1 choice.

Proposed paths:
- tools/meter.py
- bootstrap/tests/test_meter.py

## Rationale

Counts come from the source, cost agents nothing, and stay out of the
agents' loop, so they inform judgment without becoming a target.

## Alternatives considered

A proxy sees every prompt and credential. Built-in telemetry suits a live
stop later. Self-report yields `unknown`. Budgets per artifact invite gaming.
The `ccusage` reader breaks the standard-library rule but is an
independent count to compare against.

## Documentation / doctrine surface

`tools/gauge.py`; `dev/measurement/README.md`; the drain step and its shipped
copy; both templates (Q1); `doctrine/rationale.md:584-588`. Per-tool readers
carry `vendor-ok`.

## Evidence / verification plan

### Tests required

The meter test module, tiny fixtures, under one second: secrets in message
text and in a remote URL never reach output or errors; links, non-regular
files and oversized lines are refused; repeated records count once; running
totals are not summed, including inherited ones; subagents roll up;
incremental equals rebuild across rotation; `NaN`, stale, wrong-unit and
over-limit readings each stop the drain.

### Examples / smoke checks

Over one week, the meter's weighted total moves with the plan percentage,
and its counts match `ccusage` on the same logs.

#### Security preflight

S1: the tools write the logs and a measured agent could alter them; the
readings do authorize another unattended item, so only a fresh valid reading
under the Maintainer's policy does. S2: the secret fixtures fail if text
reaches output. S3: a person or `--handoff` runs the meter; the drain runs
it before each item. S4: every invalid input stops unattended work; attended
work is untouched. S5, declared residuals: log tampering and overshoot by
one item or concurrent sessions; this is cooperative control, not
authenticated enforcement.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

The meter disagrees with the plan percentage or `ccusage`; agents cite the
figures to justify cuts; the suite slows; nobody reads the pulse.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance — new trust boundary; unattended-run control.

## Review -- Codex -- 2026-10-30

**Model**: Codex (runtime identifier unavailable)

```
Reviewed commit: e741f1dbdec2a6ac2d3fec81b24649b1965fe933
Target: proposal and Maintainer's item/daily/handoff clarification
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Premise:** Yes: automate observation, not bookkeeping; observation and permission
   to continue differ. -- sections 1, 3.
2. **Alternative:** Keep stdlib runtime; study [ccusage](https://ccusage.com/guide/)
   readers/fixtures before duplicating their accounting. -- Alternatives.
3. **Falsifier:** Credential-bearing metadata exposed, inherited usage counted twice, or
   stale usage permitting another item. -- sections 1, 3; proposed fixtures.

Strongest case: make expenditure visible without another agent reporting task.

### Findings

1. **MC1 -- Blocking: content-blind is not secret-free.** Section 1 retains
   remotes/folders across projects; credentials can occur in remotes, not just message
   bodies. Specify opted-in source/project scope, credential removal, private ledger
   placement and safe diagnostics; test secrets in metadata too. A message-only secret
   fixture is insufficient.

2. **MC2 -- Blocking: define the ceiling's units and authority.** Section 3 switches
   between percentage and weighted tokens without unit-specific limits; S1 incorrectly
   says figures never authorize. Bind source/account, unit, reset window and freshness
   to the configured limit; stale/unknown stops. Describe a cooperative between-item
   stop, not a hard spending guarantee: one item or concurrent sessions can overshoot.

3. **MC3 -- Gathering contract.** The Maintainer requests per-item attribution when
   reliable; otherwise daily totals and refresh at `--handoff`. Advice: session digests
   cannot select claim intervals, and claims are pruned
   (`tools/_intent/record_io.py:288`). Preserve mappings, expose ambiguous coverage, and
   test incremental/rebuild equality, inherited counters and rotation. Retain
   verification timing until equivalence is demonstrated.

**Elapsed**: 6m35s (18:52:23-18:58:58 UTC; finalization excluded)
**Tokens**: unknown

**Coverage:** Read identity, claim retention, drain/handoff and existing measurement
tools. No private transcript scan, provider-count reproduction or implementation
execution; separate Security Review remains open.

## Review -- Codex (Security Review) -- 2026-10-30

**Model**: Codex (runtime identifier unavailable)

```
Reviewed commit: 742c3cc98ef06efbf58dd90ce142871f32e8b45b
Target: log ingestion, ledger, reporting and unattended admission
Prior findings: MC1-MC3 remain open; separate obligation
Assurance path: high-assurance
```

**Tier**: Security Review
**Obligation**: local usage-log ingestion and unattended-run control
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Premise:** Support local observation, not an authenticated quota guarantee. --
   sections 1, 3.
2. **Alternative:** Constrained ingestion and cooperative stopping, reusing existing
   file-safety patterns. -- `tools/session.py:657`.
3. **Falsifier:** Invalid usage permits continuation, or ledger output follows a link
   outside its destination. -- proposed fixtures; Python 3.13.13 primitive probe below.

Strongest case: measure expenditure without collecting prompts or imposing agent
bookkeeping.

### Security adjudication

1. **MS1 -- Blocking; S1/S4.** MC2 remains open: measurements authorize another drain
   item. Require Maintainer-controlled policy, matched account/unit/window, freshness
   and finite nonnegative values. Primitive probe: Python JSON accepts `NaN`, yet `NaN
   >= 100` is false; this is not an observed meter exploit. Stale, incomplete or invalid
   data must stop unattended admission, never invalidate attended work.

2. **MS2 -- Blocking; S2/S3.** MC1 remains open. Specify opted-in source roots, private
   cross-project storage, redacted/escaped metadata and content-free errors. Bound reads
   and prevent symlink escapes/non-regular inputs and redirected ledger writes; reuse
   existing patterns rather than new machinery. Add fixtures for these boundaries.
   Refresh before drain admission; daily/`--handoff` reporting cannot establish
   freshness alone. "Content-blind" should prohibit body retention/disclosure, not
   falsely promise JSON parsing never reads body bytes.

3. **S5 ruling:** Mutable-log tampering and in-flight/concurrent overshoot are
   acceptable only as explicitly declared cooperative-control residuals, not
   authenticated spending enforcement.

**Elapsed**: 3m13s (19:01:15-19:04:28 UTC; finalization excluded)
**Tokens**: unknown

**Coverage:** Read committed contract, drain and file-safety helpers; executed only the
JSON/comparison primitive. No private-log scan, meter implementation, platform matrix or
end-to-end security test. Obligation remains open.

## Response -- Claude Opus 5.5 -- 2026-10-30

Answers Codex's usual review (`742c3cc9`, MC1 to MC3) and Security Review
(`b70fdbdf`, MS1, MS2, S5). The operative sections are revised in place;
both reviews are unchanged. Status moves to `awaiting-decision`.

- **MC1 and MS2, accept.** Sources and projects are opted in by the
  Maintainer; the cross-project ledger is private and per-user; remotes lose
  credentials; errors carry no text. Inputs are regular files only, linkless,
  size-capped and finite, reusing `_read_regular_bytes`; ledger writes are
  atomic and refuse links. "Content-blind" now promises no content kept or
  shown, not that bytes are never read. Fixtures cover each boundary.
- **MC2 and MS1, accept.** The stop binds source, account, unit, window,
  limit and freshness in Maintainer policy, refreshes before each item, and
  stops on anything stale, missing, invalid or mismatched. S1 now says the
  readings authorize continuation. It is declared a cooperative between-item
  stop.
- **MC3, accept.** The Maintainer's per-item-else-daily contract, refreshed
  at `--handoff`, is adopted as relayed in the review; the meter keeps its
  own claim mapping against pruning; incremental-equals-rebuild, inherited
  totals and rotation are tested. Elapsed stays until metered time is shown
  equivalent; Q1 now retires only Tokens.
- **`ccusage`, accept as a control:** its counts are compared, its code is
  not adopted.
- **S5, accept** as declared residuals.

### Withdrawn / superseded commitments

- "Content-blind: never message text": replaced by no content kept or shown.
- "Retire Tokens and Elapsed": Elapsed is retained.
- "The figures inform, they do not authorize": withdrawn as untrue.
