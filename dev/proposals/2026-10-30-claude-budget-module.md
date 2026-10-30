# Budget module: price work in the artifacts that create it

**Author**: Claude Opus 5.5 (Strategy)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — the meter reads files outside the repository, a new trust boundary
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Give every proposal and plan a budget of agent spend, Maintainer interactions and lasting complexity, measured mechanically, so adding things costs something and removing them earns something.

## Context

Cost rules keep getting swallowed, each one more sentence to remember
(Maintainer, chat, 2026-10-30). Agents fill the shape they are given.

Agents' incentives point one way. A reviewer flags what is missing far more
often than what is excess, so adding is safe and omitting is punished. Later
costs fall on someone else. Agents meet a numeric limit well and judge "worth it" poorly.

The data already exists, measured 2026-10-30: this session's transcript holds
7,066 per-call usage records; Codex keeps 763 session files with token-count
events. Intent claims already name the session, files and time of each piece
of work (`dev/intents.jsonl`).

## Proposal

A default-on module that makes cost a scarce number inside the artifact.

**1. The budget card.** Every proposal and plan opens its Proposal section
with three ledgers. The author estimates three numbers. Scarcity works on
estimates alone; measurement checks them and builds history. Measure only
what is cheap and reliable; branch count and public names are shown, never
budgeted, because complexity proxies predict comprehension poorly.

| Ledger | Measured | Author estimates |
|---|---|---|
| Spend | agent tokens; elapsed time, Maintainer waiting split out | tokens |
| Attention | Maintainer interactions: Decisions, questions, waits | count |
| Carry | always-loaded words; files; public names; branch count; tests and suite seconds | the one expected to grow most |

One line follows: **Buys:** the outcome. No single score; each ledger shows
beside its reference class (point 4).

Attention is the scarcest ledger. A light proposal budgets one interaction,
its Decision; each further ask spends from it, visibly.

**2. Context rent.** Text every session loads (`AGENTS.md`, vendor wrapper,
templates) is paid on every load. The card prices it as words × loads per
week, in tokens per week. `AGENTS.md` is 2,487 words (measured), about 3,300
tokens per load at an assumed 1.33 tokens per word. Rules growth becomes a
recurring cost in the same unit as everything else.

**3. Priced findings and deletion credit.** A review remedy states its price
on the card's ledgers; adopting it spends the budget. When a ledger is spent,
the author drops something or asks the Maintainer to raise it (one
interaction). Removal earns its carry back: deleting always-loaded words,
files or tests funds new work. Cut 5 of the accepted apparatus proposal
becomes priced.

**4. Reference-class forecast.** Beside each estimate the card prints what
past artifacts of the same kind and tier actually cost (median and 80th
percentile). After the United Kingdom mandated this for major projects,
average cost overrun fell from 38% to 5% (Park 2021,
doi:10.18757/ejtir.2021.21.2.5504; contested by Themsen 2019,
doi:10.1111/faam.12210). Until twenty artifacts exist, it prints
"uncalibrated".

**5. The meter.** A standard-library reader per harness, content-blind: it
reads usage numbers, timestamps and session ids, never message text. It joins
usage to intent claims by session and time, so tokens land on the files being
worked. Output is a gitignored local ledger; at archive, actuals fill the
card's second column. Carry is computed from git and `ast` (files, public
names, branches), the timing record (suite seconds) and word counts.
Unknown stays unknown, never zero.

**6. Fuel gauge.** An unattended loop reads plan usage before each item and
stops at a Maintainer-set ceiling, leaving a note. Attended sessions only see
the figure.

**7. Portfolio view.** The board footer shows this week's spend, projected
burn, queued Maintainer interactions and total context rent. That view is the
first project budget.

**This proposal's card:** Spend estimated 2M tokens; Attention 2 (this
Decision and the plan's); Carry: about 120 always-loaded words, roughly 4 new
files and 1 test module. Uncalibrated. Buys: Cairn's budgeting capability.

Proposed paths:
- templates/modules/default-on/budget.md
- templates/modules/default-on/budget_meter.py
- tools/budget.py
- bootstrap/tests/test_budget_meter.py

## Rationale

A scarce number changes what agents do; a sentence does not. Pricing
findings makes review ask what is worth its cost. Deletion credit is Cairn's
first reward for simplifying.

## Alternatives considered

Self-reported cost lines: swallowed. One composite score: gamed at once, and productivity
research rejects single metrics (SPACE). Doing nothing: costs stay invisible
to the agents who create them.

## Documentation / doctrine surface

Both templates (card, with equal words removed elsewhere); the session-start
and drain skills (gauge); `tools/board.py` (footer); a module file with an
adopter guide. Shipped text names no vendor; per-harness adapters carry
`vendor-ok`. Rate-limit gate: the Maintainer's instruction and the recurrence
recorded in the accepted apparatus proposal.

## Evidence / verification plan

### Tests required

The meter test module (proposed above): a fixture secret never appears in
output; malformed lines count as unknown; usage joins
to the right claim; the gauge stops at its ceiling and when it cannot read.

### Examples / smoke checks

Meter last week here; the session total matches the harness report within 5%.

#### Security preflight

S1: the harness writes the logs and the measured agent could alter them;
actuals are an estimate of record, not an audit. S2: the content-blind test
fails if any text field is emitted. S3: a person runs the meter at archive;
the gauge runs before each unattended item. S4: a parse error yields unknown,
never zero; an unreadable gauge stops unattended work. S5: an agent splitting
sessions or editing logs still understates cost.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Boilerplate cards; estimates never converge; the card costs more than it
saves; one ledger gets gamed.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance — new trust boundary (meter) and
unattended-run control (gauge).
