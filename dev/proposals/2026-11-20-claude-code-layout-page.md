# A layout page for each project's code

**Author**: Claude (Strategy), drafted by Claude Sonnet 5.5 (`claude-sonnet-5-5`)
**Status**: revising
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

## Review -- Claude Sonnet 5.5 (`claude-sonnet-5-5`) -- 2026-11-20

```
Reviewed commit: 947d3d3cc97ce7d675275eab758ab2d3829e1ffb
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes for A, B and F, which are text and a trial; C and E are not yet specified well enough to build -- findings 1 to 3 below; `dev/tools/code_map.py` (1,210 lines, similarity-based, no page reader), `docs/code-map.md`.
2. **Best alternative.** A hand-edited page with plan lines and the trial, and no check until the trial shows the page is useful; doing nothing leaves the account by hand -- the `git`/`_git` search below (seven non-test homes).
3. **What would show it wrong.** Forward test: an agent given the page and one without it each write the same small task, and the first still adds a new copy of a central tool -- no such test is in F.

The proposal tries to give the scientist one page he can correct as a description of the project, and to make agents call central tools instead of writing copies. The trial-first order is sound.

**Findings**

1. **Blocking.** The check has no one who runs it. S3 says the implementer runs `code_map.py` "as one of the plan's verification commands", but no outcome puts it there, and the Context says none of 25 recent plans cites the code map. The module is also team-gated. Closing words below, block 1.
2. **Blocking.** E relies on "the check confirms each function is otherwise unchanged", a tool feature that C's four warnings do not list. E is set to Internal plan review only, though it would be a new claim adopters rely on. Closing words, block 2.
3. **Blocking.** The trial has no stop result: "Signals" names an hour of correcting, but nothing says that stops C and E. F also cannot show agents stop writing one-offs, the thing the Maintainer wants. Closing words, block 3.
4. **Blocking (weakens a rule).** Taking over "Critical Helper Homes" would drop its "Limits and preserving checks" column and its warnings that verbatim shipped copies are intentional and readers must not merge on name similarity (`dev/architecture_review.md`). Closing words, block 4.
5. Non-blocking. A "word for word" copy warning will fire on every intended twin (`session.py`, `code_map.py`, `prose_diff.py` each ship a byte-identical copy); add to C: "a copy in a file the page lists as an intended twin draws no warning."
6. Non-blocking. The doctrine list omits `tests/security/test_code_map.py` (names the install copy and the owner-home guard), `tests/security_manifest.py`, `tests/fixtures/gate_manifest.json`, `dev/.cairn/cairn-lock.yml`, and says nothing of how installed projects already holding an edited rubric get the page (`tests/test_upgrade.py` treats it as adopter-owned). Security Review should take this.
7. Non-blocking. Commit `52cc8095` is a repeated clock workaround inside one test file; a page of folders, state and central tools would not have caught it. The seven `git` copies are the better example.
8. Non-blocking. The v0.9 row for the code-map comparison pilot overlaps C and is not named.
9. Non-blocking, the Decision summary. He would ask what "promise", "promise test", "fold" and choice 2(c) ("if its language can be described by hand") mean; E's timing is in no choice. Length: about 1,750 words against 1,000; cut first the Context bullets (the note holds them), then "Why heavy", which repeats the header.

**Checked myself**: seven `git`/`_git` functions in seven non-test files (match); `meter.py` 7,322 lines (match); `dev/tools` holds 23 `.py` files, not 22; README presence for six folders (consistent with 2 of 12). `HandoffLock` also stores its root. Not checked: the 70 classes, 12-to-22 copy groups, the 195 failures, all outside studies, and tier correctness beyond heavy being defensible for A and C.

**Not covered**: security answers S1 to S5 (for the Security pass), no test run.

### Closing words for the blocking findings (review of 2026-11-20)

1. Add to B: "When the project has a layout page, the plan's verification field lists `code_map.py --changed <files>` as a required command, and the code reviewer quotes its report in the review." Replace S3 with: "The plan lists it; the implementer runs it; the code reviewer quotes it."
2. Add to C: "In E's plans, a move check reports each function whose body differs after a move." Change the Plan review line to: "required(Internal + Internal Security Review) for the plans that build A, C and E's move check; required(Internal) for B, F and the rest of E."
3. Add to F: "Stop rule: if the Maintainer cannot correct the page without reading code, or correcting it takes over an hour, C and E are not built and the proposal returns to him. The trial also gives one agent the same small task with the page and one without, and counts new copies of a central tool in each."
4. Add to A: "`dev/architecture_review.md` keeps its Critical Helper Homes table and the notes on intended copies until the page's central-tool entries each carry a limits-and-preserving-checks field covering every row."

## Review -- Claude Opus 5.5 (`claude-opus-5-5`) -- 2026-11-20

```
Reviewed commit: 6eb2adafc3edf46f877ae6dabb004788a1c34f4f
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE

**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes, once the page reader, the page-change review and the move check are bounded; the existing reader already refuses links and runs isolated -- `dev/tools/code_map.py` lines 1-17 and `_changed_paths`.
2. **Best alternative.** Keep the page as text agents read, with no tool reading it, until the trial passes; that removes the new input path -- `install/_scaffold/config.py` "architecture-review" entry.
3. **What would show it wrong.** Forward test: a planted page naming `..\x`, `\\host\share` and a link draws "rejected" for each and opens nothing -- no such case is named under C.

The proposal makes the page a checked description, not a rule, and keeps the check advisory. That is the right risk posture.

I agree with usual findings 1, 3 and 4. On finding 2 I agree on the review tier; my wording of the claim governs. My finding 4 governs over usual finding 6.

**Findings**

1. **Blocking (S4).** "Follows no link out of the project" is weaker than the code map today, which follows no link at all. Paths named in the page are not bounded; on Windows a `\\host\share` path can make the machine contact another host.
2. **Blocking (S2).** A one-off can still be blessed unseen: a page edit made during implementation, a new "long on purpose" file, a new intended twin, or a removed central tool each silence a warning, and nothing shows them to the Maintainer.
3. **Blocking (E).** "Otherwise unchanged" is false when a moved body is the same text but its names resolve to different things in the new home, its decorators or defaults change, the old copy stays, or a caller now reaches a different function of the same name.
4. **Blocking (install).** The page changes the install table, the layout catalog, lockfile entries and the published manifest, and nothing says how existing installs get it or that an adopter's file at that path survives.
5. Non-blocking. Agents read the page as data; a central-tool entry never makes an agent run a command named in it.

**Not covered**: the trial's design, Decision-summary wording, numbers in Context, and whether upgrade adds new files to an already-adopted module (I read `tests/test_upgrade.py` 2425-2460 only). No test run.

### Closing words for the Security Review findings (2026-11-20)

1. Replace S4's last sentence with: "The page is opened only through the code map's existing root-relative, no-follow reader, under its existing size limit (`MAX_SOURCE`) and time limits; a link, or a page over the limit, is reported as unreadable. Each path or folder pattern in the page must pass the rule `--changed` paths pass (root-relative, no `..`, no backslash) and also contain no colon, so no drive letter, or is reported as rejected and never opened; patterns are matched against the files already collected, never expanded on disk. The report prints names and paths only, ASCII-escaped and cut to 200 characters, never page prose. A missing page is reported once as missing, never as a clean result."
2. Add to S2: "The code reviewer lists every line of `dev/code-layout.md` added, removed or changed in the reviewed range. Each must match a page change in the plan the Maintainer accepted. Any other page change, including a new long-on-purpose file, a new intended twin or a removed central tool, goes to the Maintainer as a question of kind D before archive." Add to S5: "a page change listed but not questioned."
3. In E, replace "the check confirms each function is otherwise unchanged" with: "the move check reports, for each moved function, whether its text is the same apart from its file; it does not claim the same behaviour. It reports as changed any difference in decorators, default values, signature or class; any name the body uses that is bound differently in the new home; an old copy left in place; and any caller that now reaches a different function under the same name. For a model, the reference run, not this check, shows the numbers are unchanged. The test helper's layout map changes only in the move's own commit and is shown in its review."
4. Add to "Why heavy": "Adding `dev/code-layout.md` changes the architecture-review entry in `install/_scaffold/config.py`, `install/_scaffold/layout_catalog.py`, lockfile entries and the published install manifest. The plan for A states that the page installs as an adopter-owned, substituted file; that an existing file at that path is never overwritten and draws the existing differs advisory; how a project that already has the module receives the page on upgrade; and the test case for each in `tests/security/test_code_map.py` and `tests/test_upgrade.py`."
