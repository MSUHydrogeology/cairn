# A layout page for each project's code

**Author**: Claude (Strategy), drafted by Claude Sonnet 5.5 (`claude-sonnet-5-5`)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — outcome A adds an installed file through the installer's table of module files, and outcome C gives a shipped tool a new project file to read.
**Plan review**: required(Internal + Internal Security Review) — for the plans that build outcomes A and C; the plans for B, E and F are text and a trial and take required(Internal).
**Opened**: 2026-11-20
**Rules that apply**: dev/rules/conventions.md, dev/rules/working-agreements.md, dev/rules/protected-surfaces.md
**In brief**: Each project gets one plain page saying what each code folder holds, which classes hold state and which central tools the rest relies on, so the scientist can follow the code and agents stop writing one-off copies.

Proposed paths:
- `dev/code-layout.md`

## Decision summary

**The problem you notice.** Cairn tells an agent where a document, a rule and a test go. It does not say where code goes. So you keep the account of the code by hand, and agents write one-offs: a private copy of a job the project already does somewhere. You said agents "like one-off solutions that are really customized, rather than central rock-solid capabilities with some additional function arguments." By "architecture" you mean "what is in this folder in the code?" and "what different classes exist that hold states?"

**The change.** Each project keeps one page, `dev/code-layout.md`, with three lists and nothing else. Folders: what belongs in each. State: each class that holds state (what a program stores while it runs, such as the water in each cell), what it stores, and what may change it. Central tools: each one function or file that does a common job for the whole project, its one-sentence promise, its home and its tests. An agent drafts the page from the code. You correct it as a description of the project. Plans then say where new code goes and which central tool it calls. A check reports what the page misses. Old code is restructured by approving a page.

**What is added.** One page per project. Two lines in each plan. One new report from the existing code map tool. Guidance for restructuring old code. No always-loaded rule text changes.

**What it costs.** Someone must keep the page true; the check makes that cheap. Each plan carries two more lines. The check misses copies written in different words.

**Choices for you** (my pick first):

1. *When to build.* (a) Decide now, run a trial in the v0.9 window, build first thing in v0.10. (b) Build the page and the plan lines inside v0.9, the rest in v0.10. (c) Decide in v0.10. I recommend (a): v0.9 is your tightening release with no notable new feature, and the trial ships nothing.
2. *Which project gets the first trial page.* (a) modflow_tools: it is Python, it is yours, and you have done this work there by hand. (b) Cairn itself. (c) LHM, the largest, if its language can be described by hand; the page is plain words. I recommend (a).
3. *Which languages matter after Python.* The check starts with Python. Which others should it learn? I make no recommendation; please name them.

## Context

All numbers were measured by the strategy note on this subject, on Cairn's code at v0.8.0.

- Of 12 code folders, 2 carry a README. `dev/tools`, with 22 files, has none.
- No record lists the 70 classes in 25 files, nor what they store.
- Seven functions named `git` or `_git` sit in seven files with seven different bodies, though one central Git reader exists. Exact copies of functions across files grew from 12 groups to 22 in three weeks.
- None of 25 recent plans cites the code map.
- The 0.8 layout move had a 9,692-word plan. The first full test run then failed 195 tests and hit 18 errors in 46 files; about 29 commits repaired them.

A one-off from today (commit `52cc8095`): a helper in one test file worked around a clock problem. A fixture elsewhere in the same file did not, and its tests failed every time on Linux.

Outside studies mostly agree; one found no rise in such problems (see the note). Only Cairn's own code was measured; no other project's was.

## Proposal

Six outcomes, each its own plan or part of one. Later ones wait on the board until their condition is met.

- **A. The layout page.** `dev/code-layout.md`, as above. A high-tier agent drafts it from the code. The architecture-review module installs it, and its "Fill:" prompt is replaced by a pointer to the page. In Cairn's own tree it takes over the sections "Current Shape" and "Critical Helper Homes" of `dev/architecture_review.md`. It is plain words, the same for any language.
- **B. The plan chooses where code goes.** Beside **Reuse**, the plan template gains two short lines: where each chunk's new code goes, by the page's folders, and which central tools it calls. Where a tool nearly fits, the plan adds an argument to it in an early chunk and lists its file. The plan's author decides, not the implementer. A plan that adds a folder, a state-holding class or a central tool also edits the page; that page change is what you are shown.
- **C. A check keeps the page true.** At each change `code_map.py` reports what the page does not cover: a new folder, a new class that holds state, a function that copies a central tool word for word, and a file longer than the page's limit (default 2,000 lines; the page may list files long on purpose, each with its reason). It warns and never blocks. It will miss copies written in different words. Python first.
- **D. Two questions reach you**, and no lists of functions. A change to the page: "Routing would now change the snow class's stored depth. Is that right in the model?" A difference between two copies: "One reader skips dry cells and the other returns zero. Which is right?" D is part of A and B.
- **E. Restructuring old code by page.** You said: "Restructuring old code is the biggest deal." An agent drafts two pages: the layout today and the one proposed. You approve the second. Agents then plan two kinds of step, never mixed. A **move** changes where code lives and nothing else; the check confirms each function is otherwise unchanged. A **fold** replaces several one-offs with one central tool: the tool's promise test comes first, then each one-off becomes a call. For a model, a reference run gives the same numbers before and after. Tests reach code through one helper that knows the layout, so a move does not break them. Restructuring runs early in a release window. The guidance goes in the legacy-agent module. A sister proposal covers removal after each release.
- **F. A trial before the tool is built.** An agent drafts the page for one real project and you correct it. The trial ships nothing. It records your correction time and entries changed. It tests whether the page speaks of the right things. C and E are built only after it.

**When.** Decide now; run F in the v0.9 window; build A, B and C first in v0.10; build E after F and C.

**Why heavy.** Outcome A adds a file that the installer puts in a project, through the installer's own table of module files, which changes the install contract. Outcome C changes a tool adopters run and gives it a new project file to read. Each is a trigger for the heavy tier and a Security Review. Outcomes B, E and F are text and a trial; their plans take the usual review only.

## Rationale

The page gives you one place to check and agents one place to look. Your decisions stay about the science.

## Alternatives considered

- **Leave it.** You keep the account by hand; exact copies grew from 12 groups to 22 in three weeks.
- **Add more generated views.** The code map already lists every class, and none of 25 recent plans cited it.
- **Add rules against one-offs.** A study in the note found guidance lowered where decay started, not its rate.

## Documentation / doctrine surface

Affected: `templates/modules/team-gated/architecture_review_template.md` and `architecture-review.md`; `templates/modules/team-gated/legacy-agent.md`; the **Reuse** field of `dev/plans/_template.md`; `dev/tools/code_map.py` with its shipped twin and `docs/code-map.md`; Cairn's `dev/architecture_review.md`; and `install/_scaffold/config.py` with `install/_scaffold/layout_catalog.py`, which list the files each module installs. None of `AGENTS.md`, `RULES.md` or the counted files under `templates/core/` is touched.

## Evidence / verification plan

The trial (F) is the first evidence. For C, the check reports a planted new folder, state-holding class and copy of a central tool, and nothing on an unchanged tree. For E, count the tests that fail after the first move, against 195 failures and 18 errors after the 0.8 move.

### Tests required

C only: the code map's report on the planted cases and an unchanged tree. Prose uses the prose gates.

### Examples / smoke checks

An agent's uncorrected draft of the lists for `dev/tools`, unchecked by anyone who knows the project.

- Folders: `dev/tools/*.py`, the tools agents run.
- State: `HandoffLock` in `session.py` stores the lock file's path, the agent and an open file; only its own acquire and release change it. `CheckResult` in `claim_check.py` stores one file's findings; only the checker adds to it.
- Central tools: `git_read.py::run_git` reads Git data under fixed offline settings; `exact_replace.py` replaces exact text or refuses without writing; `session.py::encode_display` turns any text into printable ASCII.
- Not in this draft: where each central tool's tests are.

#### Security preflight

- **S1, who supplies the check's input.** The layout page and the project's source files, both from the project being checked. The check authorizes nothing: it only warns.
- **S2, can it fail.** Yes: a planted folder, state-holding class, copied function and over-long file each draw a warning, and an unchanged tree draws none. One limit, said plainly: the check compares the code with the page, so a page edited to match a one-off silences it. That is why a page change is what the scientist is shown.
- **S3, what runs it.** The implementer runs `code_map.py` as one of the plan's verification commands, and the code reviewer reads its report.
- **S4, which way it breaks.** It never blocks. A page it cannot read is reported as unreadable, never treated as a clean result. The page's reader takes one fixed form, has a size limit, follows no link out of the project and escapes every name it prints.
- **S5, what still gets through.** Copies written in different words, code in languages other than Python, and a page changed to bless a one-off that nobody questions.

N/A for the independent scientific check: no scientific assumption or result is touched.

## Signals the change is wrong

You cannot judge the trial page, or correcting it takes over an hour. The check's warnings go ignored for a release. Exact copies keep rising two releases after C. A restructuring by page breaks as many tests as the 0.8 move.

## Scope delta

**Scope delta**: preserved. Nothing existing is removed; the "Fill:" prompt is replaced, not dropped.

## Assurance path

**Assurance path**: high-assurance. Outcome A changes what the installer puts in a project, and outcome C changes a tool adopters run.
