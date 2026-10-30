# Meter agent cost from the tools' own logs

**Author**: Claude Opus 5.5 (Strategy)
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy — the meter reads files outside the repository, a new trust boundary
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Count agents' real token and time use from logs their tools already keep, show it to the Maintainer beside Cairn's existing measures, and stop unattended runs at a spending ceiling, without asking agents to report anything.

## Context

The Maintainer wants data to begin a Cairn budgeting capability (chat,
2026-10-30). Self-report has failed: since the Tokens fields landed
(`3cceb2c0`), every filled entry reads `unknown`, about 55 entries and no
numbers. Agents cannot see their own counts.

The tools already log every model call. Measured on this machine,
2026-10-30:

- Claude Code keeps one log folder per project. This project's holds 1,752
  files (1.27 GB) and 77,190 distinct model calls; one full pass reading only
  usage fields took 5.4 seconds.
- Codex opens each session file with the working folder, git remote, branch
  and commit, and logs a running total and a per-turn count of tokens.
- Three traps: records repeat (7,085 records, 3,118 calls in one session);
  98.3% of tokens are cache re-reads, priced at about a tenth of fresh input;
  subagents log separately (341 files for one session).
- The join to work already exists. A claim's id is the tool name plus the
  first 8 hex characters of SHA-256 of the tool's session id
  (`tools/_intent/identity.py:45-75`); this session's log id reproduces its
  claim prefix, `0ae5e069`.

Cairn already measures size, not spend: `tools/gauge.py` (lines by kind),
`scripts/token_budget.py` (4,281 tokens per session load today) and
`tools/audit_report.py`, all warn-only. The board row "Lightweight team
measurement" (`dev/PLANNING.md:100`) asks for a proposal first;
`doctrine/rationale.md:584-588` says the cost side is not mechanized.

## Proposal

**1. The meter.** One standard-library script, one small reader per tool.
- **Content-blind:** reads usage numbers, timestamps, ids, folder and git
  remote; never message text.
- **Counting rules:** remove repeated records by message id; keep fresh
  input, cache write, cache read and output separate; fold subagent logs into
  their parent session; take a session's last running total, never a sum of
  running totals; confirm whether a tool's cached input sits inside its input
  figure before adding.
- **Project:** chosen by git remote, so one run covers every project.
- **Work:** the claim digest links tokens to files and their artifact;
  anything outside a claim is shown as unattributed.
- **Test waiting:** command timestamps give time spent in test runs and how
  often each is repeated.
- **Output:** a gitignored ledger plus a reader, the slot
  `dev/measurement/README.md` already reserves; each run reads only new log
  lines. Missing logs are `unknown`, never zero.
- **Units:** raw kinds, a weighted figure from a small price-ratio table, and
  plan percentage where the tool reports it.

**2. A pulse report.** `tools/gauge.py --pulse` prints, by week and
project: metered tokens and time per artifact, test-wait time, review passes,
model-tier mix, and always-loaded cost from `token_budget.py`. This delivers
the board row's first item; its other two (review side-file attribution, a
`dev/measurement/` archive folder) come as the strategy note specifies.

**3. A spending ceiling for unattended runs.** Before each drain item, read
the plan percentage, or else the meter's weekly figure, against a ceiling the
Maintainer sets in local configuration. At the ceiling, stop and leave a
note. If the figure cannot be read, unattended work stops. Attended sessions
are never stopped.

**4. Numbers for the Maintainer, not targets.** No per-artifact budgets or
scores; agents are not asked to read or act on the figures. Budgets come
later, set by the Maintainer from the data, in their own proposal.

**5. Q1 for the Decision.** Once the meter passes its checks, retire the
self-reported Tokens and Elapsed fields in both templates (recommended), or
keep them. This changes a choice the Maintainer made on the apparatus
proposal's Q1, so it is theirs.

Proposed paths:
- tools/meter.py
- bootstrap/tests/test_meter.py

## Rationale

Counts come from the source, cost agents nothing, cover past work and every
project, and stay out of the agents' loop, so they inform judgment without
becoming the thing agents optimize.

## Alternatives considered

A local proxy sees every prompt and credential, and gateways can move
billing off the plan. Built-in telemetry suits a live ceiling later.
Self-report yields `unknown`. Per-artifact budgets invite gaming.

## Documentation / doctrine surface

`tools/gauge.py`; `dev/measurement/README.md`; `.gitignore`; the drain step
of the session-start skill and its shipped copy; both templates (Q1); the
`incident-trackers` module for the shipped copy; `doctrine/rationale.md:584-588`.
Per-tool readers carry `vendor-ok`; shipped prose names no vendor.

## Evidence / verification plan

### Tests required

The meter test module (proposed above), tiny fixtures, under one second: a
fixture secret never reaches output; repeated records count once; running
totals are not summed; a subagent rolls up to its parent; the digest joins a
claim; a malformed line yields `unknown`; the ceiling stops at its limit and
when unreadable.

### Examples / smoke checks

Over one week, the meter's weighted total moves with the plan percentage;
one session matches the tool's own report.

#### Security preflight

S1: the tools write the logs, and a measured agent could alter its own; the
figures inform, they do not authorize. S2: the content-blind test fails if
any text field reaches output. S3: a person runs the meter; the ceiling runs
before each unattended item. S4: a parse error yields `unknown`; an
unreadable ceiling stops unattended work only. S5: an agent editing logs or
working outside claims still understates cost.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

The meter and the plan percentage disagree; agents start citing the figures
to justify cuts; the suite slows; nobody reads the pulse.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance — new trust boundary and an
unattended-run control.

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
