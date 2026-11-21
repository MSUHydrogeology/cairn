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
| Plan A, stale text | code review | Medium | 130,979 | 3 | accept, 4 notes |
| Plan D1, gate narrowings | author | Medium | 240,961 | 10 | opened, 2,059 words plus a companion |
| | usual review | Medium | 174,542 | 6 | revise, 1 blocking |
| | Security Review | High | 151,767 | 7 | revise, 2 blocking |
| | fold of both reviews, by a fresh agent | Medium | 82,907 | 1 | ready to implement |
| Plan B, upgrading | helper: a scratch upgrade check as a script, run twice | Medium | 98,840 | 6 | defect shown from 0.7.0 |
| | implementation, chunks C1 and C2 | Low | 190,900 | 23 | done |
| Plan C, first session and tools | implementation, chunks C1 and C2 | Low | 170,999 | 27 | C1 done; C2 written and tested, left uncommitted |
| Plan D1, gate narrowings | implementation, four chunks | Low | 192,331 | 19 | done |
| | usual code review | Medium | 102,189 | 2 | accept, 3 notes |
| | Security Review of the code | High | 126,389 | 4 | accept, 4 notes |
| Plan B, upgrading | usual code review at the review point after C2 | Medium | 158,151 | 7 | revise, 1 blocking |
| | Security Review at the same point | High | 136,088 | 4 | revise, the same finding |
| Plan C, first session and tools | implementation, chunks C3 to C5 | Low | 172,477 | 9 | done |
| Code layout proposal | author, from a complete design brief | Medium | 111,537 | 2 | drafted, 1,497 words |
| | usual review | Medium | 101,155 | 2 | revise, 4 blocking |
| | Security Review | High | 92,938 | 2 | revise, 4 blocking |
| Consumer proposal | author, from a complete design brief | Medium | 128,380 | 4 | drafted, 1,700 words |
| | usual review | Medium | 79,482 | 1 | revise, 3 blocking |
| | Security Review | High | 94,489 | 2 | revise, 4 blocking |
| Plan B, upgrading | implementation, chunks C3 and C4 | Low | 232,591 | 24 | done |
| | implementation, chunk C5 | Low | 243,761 | 13 | done |
| Plan C, first session and tools | usual code review | Medium | 157,867 | 5 | accept, 5 notes |
| | Security Review of the code | High | 144,982 | 6 | accept, 5 notes |
| Layout-page trial plan | author, from a complete design brief | Medium | 156,038 | 6 | opened, 1,235 words |
| | usual review | Medium | 105,392 | 2 | revise, 5 blocking |
| Layout trial, step 1 | draft of the page, from a code-only copy | High | 133,527 | 7 | done, 871 words |
| | three tasks and their key | Medium | 114,176 | 4 | done |
| Layout trial, step 2 | counts against the hand-kept account | Medium | 68,119 | 0.3 | done |
| Plan B, upgrading | usual final code review | Medium | 160,248 | 8 | revise, 1 blocking |
| | Security Review of the final code | High | 195,473 | 10 | revise, 2 blocking (1 shared) |
| Plan E, the documentation plan moves | author | Medium | 322,825 | 13 | opened, 2,052 words plus a companion |
| | usual review | Medium | 218,598 | 7 | revise, 3 blocking |
| | Security Review | High | 145,619 | 5 | revise, 1 blocking |

Total for the day so far: 9,872,104 tokens across 65 subagent runs (rows from plan A's code review on were added in the evening). Plan A's
implementer stopped three times; the harness reported 88,695, 94,365 and
135,367 tokens at those stops, and whether those figures add up or include
each other is not known. The table uses the last.

**Test runs (machine time on a Windows Server host, no tokens).** A selection of
23 test files for a rule-text change: 16 to 17 minutes a run, three runs. Plan
A's groups: 15 files, 11 minutes a run; 40 files, 57 minutes for one run. Seven
files of signing tests in the Linux subsystem: 10 to 21 minutes a run. Plan
A's ten files that name the upgrade notes: 27 to 29 minutes a run, three runs.
Plan A in all: about 3.6 hours of machine time for tests, against 0.81 million
subagent tokens in five runs.

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
- **Plan D1 cost 650,177 tokens to plan** (author, two reviews, fold), for four
  small chunks. Both reviews said revise; the Security Review again raised
  blocking findings the usual review had not.
- **Plan D1 from opening to merge: 1,071,086 tokens in seven runs, and 1 hour
  54 minutes by commit times**, for four small chunks (about 100 changed lines
  of code and tests). Planning and its two reviews took 61 percent of the
  tokens, building 18 percent, the two code reviews 21 percent.
- **Building cost less than planning.** Three low-tier implementers used
  171,000 to 192,000 tokens each for two to four chunks; the plans they built
  from cost 241,000 to 309,000 each to write.
- **Where a test runs decides what it can show.** One 17-file group fails 103
  of 1,151 tests on the Windows Server machine before any change, and 1 of
  1,151 in its Linux subsystem. On Linux a real failure stands out; on
  Windows it has to be found by comparing two long lists.
- **A complete brief roughly halved the cost of a proposal.** The two
  proposals written in the evening went from brief to awaiting-decision for
  305,630 and 302,351 tokens (author, usual review, Security Review). The
  two written in the morning cost 557,593 and 555,078. Two things differed:
  Strategy put every design decision in the brief, so the author did no
  design, and Strategy folded the reviews itself, so no agent was resumed or
  spawned for that. Two against two is a small sample.
- **Thirty-four review passes so far, and still no return visit.**
- **Plan E was the dearest plan to write: 322,825 tokens.** Its author had to
  settle a design question from code on an unmerged branch. Both reviews then
  pointed to a lighter design; had Strategy settled that question in the
  brief, part of the plan and of both reviews would not have been needed.
- **The final code review of plan B earned its cost.** Two passes, 355,721
  tokens and 18 minutes, found two defects that four test groups on two hosts
  and the end-to-end checks had not: a restored wrapper that was never picked
  up again, and a setting name printed raw from the lock. Each came with the
  code that fixes it and a test that fails without it.
- **Drafting a layout page for a 111,000-line project cost 133,527 tokens.** A
  high-tier agent read a code-only copy by searching and counting, not by
  reading every file, and wrote 871 words in 7 minutes. The trial's first two
  steps cost 315,822 tokens in three runs.
- **Plan B is the exception to "building cost less than planning".** Its five
  chunks took three low-tier implementers and 667,252 tokens (190,900,
  232,591 and 243,761), against 308,764 to write the plan. The last chunk
  alone, one new installer command with its tests, cost 243,761.
- **An agent's own "elapsed" figure is not data.** Four agents wrote an elapsed
  time into their records this evening, and the harness timed the same runs:
  40 minutes written against 3 measured, 30 against 6, 25 against 7, and 10
  against 1. All four were too long, by 3.5 to 14 times. The coordinating
  session did no better: it took plan A for an eight-hour job, and the commits
  show three hours from opening to merge.

My reading, not measured:

- The floor of about 80,000 tokens for a review is the cost of a fresh agent
  reading the rules, the brief and the document. Shorter rules would lower
  every row at once.
- The one-round rule sends added scope back to the first reviewer. Today that
  cost more than a fresh reviewer with a short brief would have.
- Plans grow past their target because reviewers, rightly, ask for every
  condition and message to be written out for a low-tier implementer.
- The rule that every review records its elapsed time gets a guess unless the
  harness supplies the number. A candidate for the tightening: take time from
  the harness or from commit times, or write `unknown`.

## Keeping it

Add a dated section for each working day. Take tokens and minutes from the
harness's own report for each run, and write `unknown` where it gives none.
Never estimate a token figure. The row at the end of v0.9 on recounting review
passes (`dev/PLANNING.md`, section 2) reads this file.
