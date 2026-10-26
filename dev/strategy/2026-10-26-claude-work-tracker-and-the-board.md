# The work tracker and the official board: what to automate, what to keep by hand

**Author**: Claude (Strategy)
**Model**: Sonnet 5.5 (`claude-sonnet-5-5`)
**Date**: 2026-10-26
**Status**: draft
**Type**: design-exploration
**Surfaces this would feed**: a small, optional proposal to add fields to the board's `--json` output (schema `cairn-board/1`); a one-time reconciliation of the tracker against `dev/PLANNING.md`; a script that generates the tracker's repo-derived rows; the declared-wait convention in `dev/PLANNING.md`; the worked example in `docs/build-a-board-view.md`.

## In brief

The Maintainer keeps a **work tracker**: a hosted page whose rows the coordinating agent writes by hand. Cairn also ships an **official board** (`tools/board.py`) that reads the repository and prints what it finds. The two overlap, and the tracker has already drifted from the repository three times. Cairn's own board guide says a view should be "built, never hand-kept".

**Recommendation.** Split the tracker into two kinds of row. **Derived rows** (proposal and plan status, who acts next, last commit, issue state, unpushed commits) are regenerated from the board's `--json` output plus `git` and `gh`, and never edited by hand. **Hand-written rows** hold only what has no home in the repository: decisions made in chat, and the plain-language gloss. Before any tooling, do a one-time check that every tracker row waiting on the Maintainer has a declared row in `dev/PLANNING.md`. Change the board itself only if the generator shows a gap it cannot fill; the likeliest gap is "which review passes have happened".

**Not decided.** Which tracker features the Maintainer relies on most. That answer decides how much of the hand-written half survives. See *Open questions*.

## The question / felt gap

The Maintainer asked (2026-10-26, in chat) whether the official board leaves anything undone that the work tracker does, and whether it should be automated. The trigger was a concrete one: the board lists one decision waiting on the Maintainer, and the tracker lists others.

## Method

Everything below was measured on 2026-10-26 on branch `0.5-dev`, unless marked otherwise.

* Ran `python tools/board.py --help`, `--maintainer` and `--json`; listed the JSON's keys and the keys of one artifact record.
* Read `docs/build-a-board-view.md`: its opening rule, its list of what will not change, and its recipe titles.
* Read the tracker's rows (60 as of this date) and compared the ones the Maintainer owns with `dev/PLANNING.md` by searching for each row's subject.
* Re-checked the claim that two sets of review findings were unfixed, by searching the test files for the closing tests the reviews name (3 names, 0 hits each), against a control name that is known to exist (2 hits).
* **Not measured:** how the Maintainer uses the tracker. The tracker records no views and no clicks. See *What I did not check*.

What would falsify the conclusion: if most tracker rows turn out to have a repository home and no row ever lacks one, the "no home" gap is smaller than this note says. If regenerated rows disagree with the repository often, the board's header lines are not reliable enough to derive from.

## Findings

### The board, as it is

* **Read-only, and it derives little on purpose.** It reads each proposal's and plan's header lines and the waits declared in `dev/PLANNING.md`. Its own help says `--json` "derives no value".
* **What `--json` carries.** Top level: `artifacts`, `includes_archive`, `roadmap_read`, `roadmap_waits` (a line number and text), `schema`, `skipped_symlinks`. Per artifact: `archived`, `id`, `in_brief`, `kind`, `opened`, `path`, `plan_review`, `review`, `source_proposal`, `status`, `title`, `waiting_on_maintainer`.
* **What it says it leaves out.** Its own output ends with "not listed -- pushes (git status shows them) and anything no artifact or row declares". It carries no timestamp, no commit hash and no "whose move is it" field; the guide has a view apply `doctrine/lifecycle.md` for that.
* **It was built to be built on.** The guide has a worked example (a regenerated HTML page), recipes for "what waits on the Maintainer", "plans finished by date" and "joining active work-intent claims (a hint only)", and a "Keeping a page honest" section. It promises additive-only change within `cairn-board/1`: new keys may appear, none is removed or retyped.

### The tracker, as it is

A hosted page. Its rows live in a small database written by the coordinating agent. Each row has an id, title, section, status (queued, running, blocked, done, or "you"), owner, a reference (usually a commit), a stage line, a plain-language detail, an order and an updated date. It had 60 rows on 2026-10-26. Sections: Decisions waiting on you, Plans and implementation, Issues and follow-ups, Reviews and agents, Proposals, Later.

### Three times hand-keeping went wrong

1. **Rows went stale.** The v0.4 rows stayed as they were on 2026-10-19 while v0.4.0 was released on 2026-10-20, and were corrected on 2026-10-26. Part of that was a work pause. But nothing would have corrected them without someone remembering.
2. **An unsound claim.** The tracker said two sets of Security Review findings were unfixed because six function names the fixers planned were missing from the code. Five of the six names exist as other functions, so the check proved nothing. The sound check is the closing tests the reviews name: none exists in any test file. The planning session caught the error; a derived row would not have made it.
3. **A row with no home in the repository.** "Older installs fail the integrity check after an upgrade" has been marked "you" since 2026-10-17. `dev/PLANNING.md` never mentions it (0 matches). The board cannot see it. I have not established whether the defect still exists.

A counter-example worth keeping: the Maintainer's chat decision of 2026-10-26 to put the unfixed security findings on the 0.5 list got a row in `dev/PLANNING.md` the same day, because the planning session wrote it. Routing a chat decision into the repository works when someone does it. Nothing makes them.

### What only the tracker shows today

| Shown on the tracker | On the board? | Where it could come from | Verdict |
|---|---|---|---|
| Status, opened date, review headers, source proposal, declared waits | Yes, in `--json` | `board.py --json` | Regenerate. |
| Whose move it is | No; the guide has a view compute it | `doctrine/lifecycle.md` lookup | Derive in the view. |
| A short plain summary | Partly: `in_brief` | The artifact's own "In brief" | Derive; hand-write only where it is missing or wrong. |
| Last commit and date | No, by design (no hashes or times) | `git log` on the path | Derive in the view, not in `board.py`. |
| Which review passes happened and what they ruled | No; headers say what is required, not what has happened | Headings and verdict lines of appended review sections | Needs a new board field, or a parser in the view. See *Options*. |
| Roadmap work that is not a wait (the 0.5 table, queued and deferred rows) | No; only declared waits | Tables and prose in `dev/PLANNING.md`, whose shapes vary | Hard. Keep by hand for now. |
| Issue state and links | No | `gh issue list` | Derive in the view. |
| Commits not yet pushed | No (the board says so) | `git rev-list --count` | Derive in the view. |
| Who is working right now | No | `tools/intent.py list` is a local hint only; the coordinator also knows which agents it started | Hand-written; claims as a hint. |
| Decisions made in chat and not yet recorded | No, by design | Nowhere | Needs the declared-wait convention. Hand-written until recorded. |

## Options

1. **Do nothing.** Keep hand-keeping. Cost: the drift above, and the coordinator's attention. Benefit: no new work; the plain-language gloss stays.
2. **Split the tracker into derived and hand-written rows** (recommended; below).
3. **Make the tracker the official board.** Rejected. It lives outside the repository, so adopters cannot have it, and Cairn keeps durable state in the repository.
4. **Put git, issue and claim data into `board.py`.** Rejected for now. The board is deliberately read-only and file-only. Adding subprocess calls widens a surface that a read-only, file-only tool does not carry today, and it ships to every adopter.
5. **Drop the tracker and use only the guide's generated HTML page.** Loses the hand-written half: chat decisions, the running-agent view, and the plain-language gloss.

## Recommendation

Option 2, in this order. Each step stands on its own; stop whenever the next is not worth it.

1. **Reconcile once (small).** List every tracker row owned by the Maintainer, marked "you", or blocked. For each, find its home in `dev/PLANNING.md` or in a proposal or plan. A row without a home either gets a declared row there or is closed. For the integrity-check row, first find out whether the defect still exists.
2. **State the declared-wait convention.** One sentence in the roadmap's header: anything waiting on the Maintainer has a declared row, because `board.py --maintainer` lists only declared waits. Optionally extend the board's existing advisory ("plans that mention a fence but declare no wait") to roadmap rows that name the Maintainer without a declared wait. That is a small change to a shipped tool and would go through a proposal.
3. **Generate the derived rows (medium).** A script prints rows as JSON from `board.py --json`, `git`, `gh` and `tools/intent.py list`. The coordinating agent writes them to the tracker. Each row carries a `source` of `derived` or `hand`; a derived row is never edited by hand; the page shows the source. The script prints data only, so it stays tool-neutral; writing to the hosted page is the session's job. It changes no shipped tool. Where it lives (Cairn's `scripts/` as a documented example extending the guide, or outside the repository) is a question below.
4. **Only if step 3 proves the need:** add an optional `passes` field to the board's `--json` (heading text, model, date and verdict line for each appended review section). It is additive, so it stays inside `cairn-board/1`. It touches the shipped board tool and its twin, and the frozen `--json` contract test and baseline fixture, so it would likely owe a gate-manifest re-anchor at the next cut. It is a proposal, not a build.

Residual risk: derived rows are only as accurate as the header lines they read. If a proposal's `Status` is stale, the tracker repeats the error with confidence. The guide's answer is the right one: fix the header, regenerate.

## What would show this wrong

* The Maintainer stops opening the derived half, or says the page was better hand-written. Then drop step 3.
* Regenerated rows often disagree with the Maintainer's picture of the repository. Then the headers are the problem, and the work moves to them.
* The hand-written half keeps growing. Then the declared-wait convention is not being followed, and step 2 is the weak step.
* A refresh takes more of the coordinator's time than hand-keeping did. Measure one refresh both ways before building more.

## Open questions

For the Maintainer. Each has a recommended default.

1. **Which tracker features do you lean on most?** (Sections by who acts next, the plain-language detail, the status chips, the "waiting on you" section first, something else.) *Default:* keep all four, and build the derived half around the first and last.
2. **Is the tracker a working surface or something Cairn ships?** *Default:* a working surface. The board guide's worked example is the shipped, adopter-facing part.
3. **Should every chat decision also be recorded in `dev/PLANNING.md`?** *Default:* yes, by the planning session, as it did for the security findings. The tracker row is then a pointer.
4. **When does the tracker refresh?** *Default:* on request, and as a step in the end-of-session routine.
5. **Is step 4 (the `passes` field) worth a proposal now?** *Default:* not until step 3 has run for a few weeks and shows the pain.

## What I did not check

* How the Maintainer uses the tracker: it records no views, so every claim about use is the coordinator's impression.
* The source of `tools/board.py` beyond its `--help` and `--json` output.
* Whether the review-section headings are regular enough across the whole history for a parser; the template's headings are, but older records are unmeasured.
* Whether the integrity-check row's defect still exists.
* Whether the work-intent log can be trusted to show running agents. A recorded defect says one agent's commit releases every sibling's claims, so I treat it as a hint only.

## Fold-up note

Nothing here is specific to this project. The methodology-general part is the declared-wait convention and the "derived or hand-written, never mixed" rule for a view. If the Maintainer agrees, they could become an issue on Cairn's tracker once step 1 has run and shown whether the gap is real.
