# One local oversight website: the release board and the code-change views

**Author**: Claude (coordinating session, recording findings at the Maintainer's request)
**Model**: Sonnet 5.5 (`claude-sonnet-5-5`)
**Date**: 2026-11-10
**Status**: draft
**Type**: design-exploration
**Surfaces this would feed**: a v0.8 proposal (the "One local oversight website with tabs" row in `dev/PLANNING.md`); the postponed chunk C3 of `dev/plans/2026-11-05-architecture-and-reuse.md`; `docs/build-a-board-view.md`.

*Tier note.* The Maintainer asked for this record ("Make sure all of your insights are recorded appropriately, in the strategy doc perhaps?"). It lists findings and options and decides nothing. Strategy work has a High floor and this was written at Sonnet; a High-tier agent should check the options before a proposal relies on them.

## Summary

The Maintainer wants one local website with tabs that helps a person oversee the work. One tab behaves like the chat work tracker, for the release board. Another carries the four-view pilot of code changes, which was postponed from the architecture plan (C3). It can be a single self-contained HTML file written by one command, as LHM's scope map already is. One gap must close: LHM's page loads its drawing library and fonts from the internet. A static file shows a snapshot, is read-only and cannot run tools. That fits the earlier rule that derived rows are never hand-edited. C3's full criteria stay in the architecture plan, which remains in the repository when it archives.

## The question / felt gap

Maintainer, 2026-11-09: "I'm really finding myself needing a better visual tool to use to see where we are on development toward a version release. I want something that works the same across agents. This is a pain point." On 2026-11-10: "This four-view pilot and the visual release board and siblings--both mean to be graphical tools to enhance human oversight capabilities." And: "I want a single local website with tabs that mimicks the behavior of your artifact tracker tool here for the release board, and the example I passed for the four-view pilot of code changes." The example named was "LHM's scope-map interaction". The Maintainer also asked: "Can we have a single .html interface with board.py and other tools in a way that allows that tool to be self-contained?"

## Method

Read on 2026-11-10, none of it run except where noted: the source of the chat work tracker page; `docs/build-a-board-view.md`; `tools/board.py`, `tools/gauge.py`, `tools/code_map.py` and `tools/_intent/cli.py` (searched for JSON options); LHM's `scope_map.py` (docstring) and `scope_map.html` (searched for external references and for how data enters the page). The gap in finding 2 comes from reading the page's `<script src>` and `<link>` lines. I did not open the page offline, which would falsify it.

## Findings

1. **A single-file precedent exists.** LHM's `scope_map.py` (10 KB) runs read-only `git log`, `git diff` and `git ls-files`. It assigns each commit to a workstream (the proposal or plan it belongs to) and each file to an area and folder. It writes the result into `scope_map.html` (23 KB) by replacing one placeholder, `const D = __DATA__;`, with JSON, escaping `</`. Its docstring calls the result "one self-contained HTML file". It draws workstream, then area, then folder as a Sankey diagram (a flow diagram) and lists commits and files.
2. **The gap.** That page loads Google Fonts, D3 7.8.5 (cdnjs) and d3-sankey 0.12.3 (jsdelivr) from the internet. Offline it cannot draw, and viewing it contacts third-party servers. C3 requires the report to work with the network disabled.
3. **Cairn has a board precedent.** `docs/build-a-board-view.md` has a worked example that regenerates an HTML board page from `board.py --json`. It flattens and escapes every string with `html.escape` and scans for odd Unicode. The JSON schema `cairn-board/1` only gains keys within a version.
4. **Data sources.** `board.py` and `gauge.py` have `--json`. The claims list has a versioned JSON format in the intent engine. I found no JSON option on `code_map.py`. Git, and optionally `gh`, supply history and issues.
5. **What the chat tracker does that a local page should copy.** It groups rows by who acts next. It uses five status labels (needs you, running, queued, blocked, done) with counts and filter buttons. Each row shows stage, owner, reference and last-updated date. It has a "last change" footer, light and dark themes, and a phone layout. **What a static file cannot do:** change a status or add an item from the page, which the tracker does by writing to a shared database.
6. **A static file is a snapshot.** It must print when and from which commit it was made. Refreshing means re-running the command. A small local server would refresh live, but it is no longer one file.
7. **Hand-written content has no home in a derived view.** `dev/strategy/2026-10-26-claude-work-tracker-and-the-board.md` recommends derived rows that are never hand-edited, with hand-written rows only for facts that have no repository home. A local site needs a small committed notes file for those.
8. **The four views in C3** are workstreams, system shape, capabilities and growth.
9. **Dependencies.** The code-change tab needs Git history through the safe-Git helper (board item 2d), which also owes Python 3.12 on macOS and a "clean" scan on Windows (v0.7 items 21 and 22). Windows is an equal partner, so the generator and page must work there. Cairn ships standard-library-only Python.

## Options

- **A. Do nothing.** Keep the chat tracker. Cheapest; leaves the "works the same across agents" pain.
- **B. One generator command, one HTML file.** Data embedded, JavaScript and CSS inline, system fonts, the diagram drawn in plain SVG. Fully offline and no third-party licence; the most drawing code to write.
- **C. As B, with D3 and d3-sankey embedded.** Less drawing code; adds vendored third-party code that needs a licence and provenance check. I did not check Cairn's rule on vendored JavaScript.
- **D. B or C plus an optional local server** (standard library) for live refresh. One more process to run.
- **E. Tables or bars instead of a Sankey.** Smallest; may not answer C3's visual question.

## Recommendation

Start with B, plus a size cap, a freshness stamp, escaping of every string, and a non-graphical equivalent for each view (C3 already requires the last three). Leave the server for later. If plain SVG proves too costly, move to C. The residual risk is drawing effort, which I have not estimated.

## Open questions

Which tabs come first, or both? Does it ship to adopters? The guide is adopter-facing; the tracker is Cairn-only. Where do hand-written notes live? Does the generator live in `board.py` or a new tool? Commit messages and file lists embed in the page, so the file must stay local and never be published. How does the page separate observed from inferred progress? Do C3's comparators (CodeCharta, manual practice) still apply to a tab? I did not check LHM's scope map for licence or ownership limits, and assume the Maintainer's own project may be reused.

## Where C3's text lives

C3's full criteria are in `dev/plans/2026-11-05-architecture-and-reuse.md`: the Sequence row for C3 and the "Acceptance criteria" paragraph C3. They cover the comparators, the fresh-reviewer baseline, what to record, and the rule to reject the visual approach if it helps neither understanding nor decisions. The plan moves to `dev/plans/archive/` when it closes, and the archive step repairs links. The accepted pilot outcome is also in `dev/proposals/archive/2026-11-02-codex-architecture-and-reuse.md`.
