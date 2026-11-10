# The oversight dashboard: purpose, tabs and widgets

**Author**: Claude Sonnet 5.5 (Strategy)
**Model**: Claude Sonnet 5.5 (`claude-sonnet-5-5`)
**Date**: 2026-11-10
**Status**: draft
**Type**: design-exploration
**Surfaces this would feed**: the v0.8 oversight-website proposal (the "One local oversight website with tabs" row in [`dev/PLANNING.md`](../PLANNING.md), with the [website note](2026-11-10-claude-local-oversight-website.md)); [`tools/gauge.py`](../../tools/gauge.py); the v0.9 meter comparisons

## Summary

The oversight website is a **dashboard for the person running the project**. At a glance it shows how things are and how they are changing, so that person can monitor the project's growth. It has five tabs: Development, Sankey diagrams, Complexity, Growth over time and Security. Every widget shows a number, its direction over time and a status, and is marked ready, partial or placeholder, so the design can be complete before all the data exists. The first version should ship small and grow. This note authorizes no implementation; the next step is the v0.8 proposal.

## The question

Maintainer, 2026-11-10, in chat:

- *"it's a dashboard, informing the user at a glance how things are and how they are changing. This is a tool so that a person can monitor the growth of their project."* Sign-off is not the use case, except perhaps on the security tab.
- The tabs: development status (plans, implementations, proposals, for this or future versions); Sankey-style diagrams of where development is occurring, "modeled after the LHM one"; complexity parameters; growth over time. Plus *"a security tab, including one that shows me what has changed from a security-relevant standpoint so that I can do a better job of signing off on releases"*.
- *"I don't think claims are worth me looking at"* and *"This is for a person, not an agent"*.
- *"We can design it with widgets that don't quite work yet, and/or plan to make them work in v0.8."* And: *"We will inevitably add/change/delete with time. But the key is to get it going so it can become useful."*

## Method

I measured with `git` and small scripts, not committed: Python code length by `tokenize` and `ast` at v0.6.0 and `05da1e04`; security-relevant change from the v0.6.1 baseline (`977b5250`, 2026-11-03) to `a850f1a8`, by path patterns and text matches; and the `Tokens` and `Elapsed` lines in every plan and proposal. I read the docstrings of `tools/gauge.py`, `tools/meter.py` and `scripts/token_budget.py`, the protected-surface list and the release process. Not checked: a weekly series, other languages, pytest-collected counts, whether the meter can supply tokens per period, and whether `prose_diff.py` has landed. The risky-call counts are crude text matches that include comments and strings, and my gate-file pattern may undercount.

## Findings

- **Effort data is thin.** 168 of 214 recorded `Tokens` lines (79%) say unknown; 150 of 613 `Elapsed` lines (24%). Meter collection is off, and its comparisons are in v0.9. [`AGENTS.md`](../../AGENTS.md) cites a 188-run test timing log, but I found no machine-readable series.
- **A definition trap.** The layout proposal moves installed tools into `dev/`, so "files outside `dev/`" would drop with nothing real changing. Series must be defined by role, not folder.
- **Volume.** 1,452 commits landed between the v0.6.1 baseline and `a850f1a8`, far more than anyone can read. That is the reason for glance views.

## The design

**Rules for every widget:**

1. A number, its direction over time and a status; about six widgets a tab; detail one click down.
2. Compare to the last release and to a fixed baseline (v0.6.0), so growth shows.
3. Plain labels, with a one-sentence "what this means."
4. Define series by role, apply the same map to old commits, and mark the layout commit.
5. Derive history from git at sampled commits (weekly and at tags) into a generated cache, never hand-edited.
6. Show unknown with its coverage ("46 of 214 records"), never as zero; label figures observed, estimated or span.
7. Trends, not scores. Reference lines only for budgets that exist, such as the 10-minute certifying run.
8. Keep "since I last looked" and a print view. Leave out claims and any agent-facing control.

**The tabs, each with one question:** Development: what is in motion, and what waits on me? Sankey: where is the work landing? Complexity: how big and tangled is it now? Growth: how fast is it changing, and what does it cost? Security: how is the security-relevant surface changing?

Each widget is a card marked **ready** (inputs exist), **partial** (inputs exist with gaps) or **placeholder** (inputs do not exist yet; the card shows what it needs). None is built. "Now" figures are demos, v0.6.0 to `05da1e04` unless stated.

| Tab | Widget | Now | Status | To go live |
|---|---|---|---|---|
| Development | Status by stage and who acts next; waiting on you | `board.py --json`, `--maintainer` | ready | none |
| Development | Days at each stage | | partial | stage times from commits |
| Sankey | Workstreams and system shape from git history | | partial | drawing code, offline; reads through the safe-Git helper, which lands in v0.7; detail in the website note |
| Complexity | Test functions | 3,637 → 4,093 | ready | collected count for the latest commit only |
| Complexity | Files and folders by role | 427 → 463 files, 68 → 73 folders outside `dev/` | partial | role map; layout marker |
| Complexity | Non-comment Python | tests 65,165 → 82,440; other 34,604 → 62,406 | ready | other languages later |
| Complexity | Always-loaded words | `AGENTS.md` 3,058 → 3,925 | ready | add `RULES.md` and wrapper |
| Complexity | Largest files; shipped footprint | | ready; partial | layout homes for footprint |
| Growth | Complexity series as trends | from v0.6.0 | ready | none |
| Growth | Process volume | | partial | gauge buckets lines, not commits |
| Growth | Review load | | ready | baseline 6.9, target 3.5 |
| Growth | Elapsed per proposal or plan | 24% unknown | partial | label commit span as span |
| Growth | Tokens per artifact | 79% unknown | placeholder | v0.9 meter comparisons |
| Growth | Full-suite run time; release procedure time | | placeholder; partial | a recorded run series (own decision); tag dates |
| Security | High-risk surface churn | since v0.6.1: engine +470/−235; sweeps +2,210/−335; interpreter readers +652/−180 | ready | none |
| Security | Risky calls added to shipped code | 41 subprocess, 12 eval/exec, 11 delete/chmod, 1 network | ready (crude) | none |
| Security | Agent-directed rule size | `AGENTS.md` 3,058 → 3,925; shipped 3,139 → 4,343 | ready | sentence-level changes via `prose_diff.py` |
| Security | Open residuals; time since last re-anchor | | partial | parse the register; read the signed anchor's date |
| Security | Since-last-release drill-down: per surface, scans, gates | | placeholder | results recorded in readable form |

## Options

- **A. A first slice early (recommended).** One command writes one self-contained file: the Development tab from the board, the ready widgets, and cards for the rest. Value comes soon; the layout move later relocates it, and the role map keeps series stable.
- **B. All five tabs after the layout lands.** Cleaner paths; a later start.
- **C. Add the numbers to `tools/gauge.py --pulse` only.** Least involved. Loses trends and tabs.

## Recommendation

Option A. Every widget that reads git history goes through the safe-Git helper, a v0.7 deliverable that will have landed before v0.8 starts, so nothing waits on it. Residual risks: a metric on screen invites reading as a target, which rule 7 guards, and embedded commit messages must be escaped, as the website note requires. The proposal's tier is not decided here.

## Open questions

- Order within v0.8: start the first slice before the layout lands and move it with the layout, or start after, so it installs once? Undecided; the Maintainer, 2026-11-10: *"To some extent it depends on what happens with the rest of v0.7."* Decide when v0.8 opens. The factors are whether the layout proposal has been accepted by then (if so, building after it costs little; if it is undecided or late, an early start avoids stalling); how long v0.7 runs (a longer v0.7 makes a monitoring dashboard worth more, which favors an early start); and the layout's size, a heavy change with a Security Review and a re-anchor, against the smaller first slice.
- Do adopters get the Complexity, Growth and Security tabs? "Outside `dev/`" and the high-risk list are Cairn's own.
- Where does the generated history cache live, and who regenerates it?
- Should the dashboard show Maintainer time? Nothing records it today.
