# What each step cost: agent tokens and minutes, as the harness reported them

This is a running record, kept by hand until the usage meter can fill it. Each
row is one agent doing one step of Cairn's own work. It exists so the project
can see which practices keep costs down. The Maintainer asked for it on
2026-11-20: "We need this data so we can actually see what works to keep costs
down."

**How to read it.** A token is the unit a model provider bills by. "Tokens" is
the total the harness reported for one subagent run. Minutes are the wall time
the harness reported. Tiers follow the model mapping (`dev/.cairn/model-selection-mapping.yml`): High for
Strategy and Security Review, Medium for authoring and ordinary reviews, Low for
carrying out a reviewed plan.

**What the numbers leave out.** The coordinating Strategy session (High tier)
cannot see its own use, so it is not here; it is likely the largest single
cost. The harness does not say how much of a total was reused from cache. Test
runs cost machine time, not tokens, and are listed separately.

## 2026-11-20

| Work | Step | Tier | Tokens | Minutes | Result |
|---|---|---|---|---|---|
| One-round review proposal | author | Medium | 180,063 | unknown | opened |
| | author's revision, by resuming the same agent | Medium | 215,893 | unknown | revised |
| | usual review | Medium | 82,249 | unknown | revise |
| | Security Review | High | 79,388 | unknown | revise |
| One-round review plan | author | Medium | 238,417 | 19 | opened |
| | plan review | Medium | 112,010 | 4 | accept, 3 notes |
| | implementation, 20 files of rule text | Low | 143,458 | 24 | done |
| | code review | Medium | 85,442 | unknown | 1 open check |
| Defect arc proposal | defect inventory | Medium | 150,879 | 7 | 28 entries |
| | author | Medium | 230,522 | 10 | opened |
| | usual review | Medium | 81,979 | 1 | accept, 3 notes |
| | Security Review | High | 91,698 | 2 | revise, 2 blocking |
| Re-anchor proposal | usual review | Medium | 84,954 | 1 | revise, 1 blocking |
| | Security Review | High | 110,363 | 3 | revise, 2 blocking |
| Re-anchor plan | author | Medium | 168,952 | 8 | opened, 1,397 words |
| | usual review | Medium | 145,722 | 4 | revise, 4 blocking |
| | Security Review | High | 111,329 | 2 | revise, 3 blocking |
| Plan A, stale text | author | Medium | 210,989 | 9 | opened, 1,337 words plus an edit list |
| | usual review | Medium | 159,834 | 6 | revise, 3 blocking |
| | implementation, 55 text replacements | Low | 135,367 | 13 | done; stopped twice, correctly |
| | limited review of added scope, by resuming the first reviewer | Medium | 169,380 | 0.5 | accept |
| Plan B, upgrading | author | Medium | 308,764 | 13 | opened, 2,927 words |
| | usual review | Medium | 211,498 | 9 | revise, 4 blocking |
| | Security Review | High | 146,314 | 6 | revise, 3 blocking |
| | fold of both reviews, by a fresh agent | Medium | 92,293 | 2 | ready to implement |
| Plan C, first session and tools | author | Medium | 299,083 | 13 | opened, 2,207 words plus a companion |
| | usual review | Medium | 193,893 | 9 | revise, 3 blocking |
| | Security Review | High | 128,460 | 5 | revise, 3 blocking |
| | fold of both reviews, by a fresh agent | Medium | 98,415 | 2 | ready to implement |
| Testing assessment | reader of LHM | Medium | 153,729 | 2 | inventory |
| | reader of modflow_tools | Medium | 114,050 | 2 | inventory |

Total for the day: 4,735,387 tokens across 31 subagent runs. Plan A's
implementer stopped three times; the harness reported 88,695, 94,365 and
135,367 tokens at those stops, and whether those figures add up or include
each other is not known. The table uses the last.

**Test runs (machine time on a Windows Server host, no tokens).** A selection of
23 test files for a rule-text change: 16 to 17 minutes a run, three runs. Plan
A's groups: 15 files, 11 minutes a run; 40 files, 57 minutes for one run. Seven
files of signing tests in the Linux subsystem: 10 to 21 minutes a run.

## What the day's numbers show

Measured:

- **A review pass cost 79,000 to 211,000 tokens.** The size of the thing
  reviewed moved that less than a factor of three.
- **Writing a plan cost 169,000 to 309,000 tokens.** Plans B and C ran two to
  three times the 1,000-word target; the others ran 1.3 to 1.6 times.
- **Sixteen review passes, no return visit.** Thirteen said revise; each
  blocking finding came with the exact words that closed it.
- **Six Security Reviews, and all six said revise.** In the five whose findings
  are in today's records, each raised at least one blocking finding the usual
  review of the same document had not.
- **Resuming an agent is dear.** A half-minute check by a resumed reviewer cost
  169,380 tokens. A fresh agent folded two whole reviews for 92,293.
- **Writing and reviewing four plans cost about 2.3 million tokens before any
  of their code was written.** With plan A's implementation and its limited
  review the four come to about 2.6 million.

My reading, not measured:

- The floor of about 80,000 tokens for a review is the cost of a fresh agent
  reading the rules, the brief and the document. Shorter rules would lower
  every row at once.
- The one-round rule sends added scope back to the first reviewer. Today that
  cost more than a fresh reviewer with a short brief would have.
- Plans grow past their target because reviewers, rightly, ask for every
  condition and message to be written out for a low-tier implementer.

## Keeping it

Add a dated section for each working day. Take tokens and minutes from the
harness's own report for each run, and write `unknown` where it gives none.
Never estimate a token figure. The row at the end of v0.9 on recounting review
passes (`dev/PLANNING.md`, section 2) reads this file.
