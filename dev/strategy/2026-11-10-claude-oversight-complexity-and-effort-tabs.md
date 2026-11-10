# Complexity and effort tabs for the oversight website

**Author**: Claude Sonnet 5.5 (Strategy)
**Model**: Claude Sonnet 5.5 (`claude-sonnet-5-5`)
**Date**: 2026-11-10
**Status**: draft
**Type**: design-exploration
**Surfaces this would feed**: the v0.8 oversight-website proposal (the "One local oversight website with tabs" row in [`dev/PLANNING.md`](../PLANNING.md)); [`tools/gauge.py`](../../tools/gauge.py); the v0.9 meter comparisons

## Summary

Add two tabs to the oversight website: **Complexity** (how big and tangled the project is, and how that changes over time) and **Effort** (what building it costs in time and tokens). Design every widget now, including ones whose data does not exist yet, and mark each as ready, partial or placeholder. Build the ready ones in v0.8; tokens stay placeholder until the v0.9 meter work. This note authorizes no implementation.

## The question

Maintainer, 2026-11-10: *"In our oversight board, I think we also need a panel that shows project complexity parameters, and changes over time. Numbers of tests, numbers of folders, numbers of non-dev files, length of non-comment code, (and any other suggestions you have)."* Then: *"Another tab should show project effort: time to run tests, release procedures, tokens consumed in development, wall clock time in development, etc."* And: *"We can design it with widgets that don't quite work yet, and/or plan to make them work in v0.8."*

## Method

I measured the Maintainer's four numbers at v0.6.0 and at `05da1e04` from `git archive` of each commit, counting Python code with `tokenize` and `ast` (blank lines, comment lines and docstrings excluded). I counted `Tokens` and `Elapsed` lines in every plan and proposal under `dev/`, archive included, on 2026-11-10. I read the docstrings of `tools/gauge.py`, `tools/meter.py` and `scripts/token_budget.py`. The probe script lives in a scratchpad and is not committed; two commits, Python only. Not checked: a weekly series, other languages, pytest-collected counts, or whether the meter can supply tokens per period.

## Findings

| Measure | v0.6.0 | `05da1e04` |
|---|---|---|
| Test functions (`def test_`) | 3,637 | 4,093 |
| Files outside `dev/` | 427 | 463 |
| Folders outside `dev/` | 68 | 73 |
| Non-comment code, tests | 65,165 | 82,440 |
| Non-comment code, everything else | 34,604 | 62,406 |

Effort data is thin. Of 214 recorded `Tokens` lines, 168 (79%) say unknown; of 613 `Elapsed` lines, 150 (24%) do. The meter exists but real collection is off, and its comparisons are in v0.9. [`AGENTS.md`](../../AGENTS.md) cites a 188-run test timing log, but I found no machine-readable series. The [weight review](2026-11-06-claude-v07-weight-review.md) measured `AGENTS.md` growing from 3,058 to 3,806 words and 70% of commits touching only `dev/`.

**A definition trap.** The layout proposal moves installed tools into `dev/`, so "files outside `dev/`" would drop with nothing real changing. Folder-based series break the same way.

## The design: widgets with a status

Each widget is a card showing its name, one-line definition, value and trend, coverage, and a status chip: **ready** (inputs exist), **partial** (inputs exist with known gaps) or **placeholder** (inputs do not exist yet; the card shows what it needs). None is built.

| Tab | Widget | Inputs | Status | To go live |
|---|---|---|---|---|
| Complexity | Test functions over time | `def test_` per sampled commit | ready | pytest-collected count for the latest commit only |
| Complexity | Files and folders by role | git tree, role map | partial | role map; marker at the layout commit |
| Complexity | Non-comment code length | tokenize, ast | ready (Python) | other languages later |
| Complexity | Always-loaded words | `scripts/token_budget.py` | ready | none |
| Complexity | Largest files | git tree | ready | none |
| Complexity | Shipped footprint | install list, file sizes | partial | layout homes |
| Complexity | Trust-machinery size | high-risk list, gate manifest | partial | list kept as data |
| Complexity | Process volume | git log, `tools/gauge.py` classes | partial | gauge buckets lines, not commits |
| Effort | Elapsed per proposal or plan | `Elapsed` lines | partial | show coverage, 24% unknown |
| Effort | Tokens per artifact | `Tokens` lines, later the meter | placeholder | v0.9 meter comparisons |
| Effort | Wall-clock span | commit timestamps | ready | label it span, not work time |
| Effort | Full-suite run time | none recorded | placeholder | a small append-only record per certifying run |
| Effort | Release procedure | tag dates, human-operation count | partial | strict-check duration not recorded |
| Effort | Review load | review commits per archived artifact | ready | baseline 6.9, target 3.5 (board, measure 2026-11-30) |
| Effort | Wait for a Decision | status-transition commits | ready | none |

**Rules for every widget:**

1. Define series by role, not folder, apply the same role map to old commits, and mark the layout commit.
2. Derive history from git at sampled commits (weekly and at tags) into a generated cache, never hand-edited. Any past commit can be re-measured, so series can start at v0.6.0.
3. Show unknown with coverage ("46 of 214 records"), never as zero.
4. Label each figure observed, estimated or span.
5. Show trends, not scores. Reference lines only for budgets that already exist, such as the 10-minute certifying run. The gauge's own docstring says commit share measures cost and cannot show worth.

## Options

- **A. Both tabs, placeholders included (recommended).** The design is complete before the data is, and each placeholder says what it needs.
- **B. Complexity tab in v0.8, Effort in v0.9.** Smaller first release; delays the effort view you asked for.
- **C. Extend `tools/gauge.py --pulse` with the numbers.** Least involved; a testing note already recommended test-growth figures there. Loses the trends view and all effort data.

## Recommendation

Option A, after the repository layout lands, so the role map is defined once. v0.8 builds the ready widgets and the placeholder cards; partial widgets fill as their inputs do. Tokens stay placeholder until the v0.9 meter comparisons. Two new inputs need their own decisions: a suite-run time record, and the high-risk list as data. Residual risk: a metric on a screen invites reading as a target; rule 5 is the guard.

## Open questions

- Do adopters get these tabs? "Outside `dev/`" is Cairn's own definition; a generic version needs different roles.
- Where does the generated series live, and who regenerates it?
- Should the Effort tab show Maintainer time? Nothing records it today.
- Is a Decision-wait widget wanted, given it times the Maintainer's own responses?
