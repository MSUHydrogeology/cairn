# Run rules apart from development rules, an Operator role, a project-wide entry file

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: awaiting-review
**Waiting on Maintainer**: release draft for review
**Review**: usual + Security Review (until the accepted template-scan change lands; then usual only)
**Proposed tier**: standard — prose edits only, no installer or code change; it does edit `docs/methodology/roles.md` and an always-loaded file, so the Maintainer may raise it to heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-16
**In brief**: Let a project whose agents both run and change its software keep the rules for running it in a short file that can ship in a release, and give the agent that runs the software its own role name.

## Decision summary

Issues #74, #76 and #79 come from one adopter whose agents both run its software and change it. Its entry file carried the full development process, so an agent that only runs the software read about 720 words of it every turn, and the adopter could not remove them, because upgrades merge Cairn's text back. Recommended: (1) the split is opt-in, so a project with no "run" job pays nothing; (2) a new optional role, **Operator**, names the agent that runs the project's software, and "User Agent" is narrowed to its Cairn meaning; (3) `AGENTS.md` keeps every heading and slot a tool reads but moves most development rule text behind pointers. Cost: adopters who edited those paragraphs meet merge conflicts at upgrade. The Maintainer asked for this follow-on early (chat, 2026-11-16: "Go ahead and build the follow-on proposals now--unless doing so requires a completion of an earlier step."). It does need earlier steps; see item 5.

## Context

Measured at commit `e8703b2c` with `wc -w`. Shipped `AGENTS.md` 1,125, `VENDOR.md` 310, `RULES.md` 60: 1,495 of the 1,500 cap held by `bootstrap/tests/test_scaffold.py`. Added words need room first.

Shipped `AGENTS.md`, my classification: development process 723 words (Lifecycle and records 187, Review 102, Roles 158, Working tree and commits 96, Verification 157, Functional prose 23); project-wide 402.

A tool or test reads: five slots (`project-overview`, `claim-check`, `security-verification`, `documentation-discipline`, `project-conventions`; `bootstrap/tests/test_install_report_slots.py`); the headings Review, Roles and Lifecycle and records (`bootstrap/tests/test_documentation_plan_module.py`); and "Lifecycle and records" in `tools/session.py` messages. Not checked: any other test that quotes a heading.

Cairn's role texts disagree: `docs/methodology/roles.md` says the User Agent "runs the software"; the shipped `dev/agent_collaboration.md` says it "exercises Cairn from an adopter's position". "Operator" appears in neither. `dev/rules/README.md` says its files are "entirely the adopter's own", which rules out #79's `dev/rules/` as a place for Cairn-written text.

One adopter's practice (read, not run): its root `RULES.md` (1,166 words) holds run rules and names nothing under `dev/`. It kept all of Cairn's `AGENTS.md` and put its router in its own overview slot. Holding that layout cost it two guard tests (537 lines): line ceilings, section-name and slot-order checks, and a check that run rules cite no `dev/` path.

## Proposal

**1. Who gets it: opt-in, default off.** No shipped file gains a second rule path. One section of `dev/rules/README.md` (about 150 words, read on demand) says: the root `RULES.md` holds rules for an agent that runs the software, cites nothing under `dev/`, and ships whole; development rules live in `dev/rules/` and may cite run rules, never the reverse; essentials both jobs need (temporary files, never delete, never push unasked) live once, in `RULES.md`. The `RULES.md` template points to it in one line. A project opts in by writing those rules. There is no installer question (a profile field is an engine change). The staged-modules draft offers rules-folder guidance by size; "agents also run the software" is a fact about the project, so its trigger fits poorly. If decided, it may offer this section too.

**2. Operator.** Add to the roster in `dev/agent_collaboration.md` and `roles.md`: **Operator**, runs the project's software under its run rules and files software defects in the project's tracker. Narrow **User Agent** to exercising Cairn from an adopter's position and filing what it hits to Cairn. Both are optional. A project with an Operator adds a line to the `role-roster-additions` slot; one with neither writes nothing. `AGENTS.md` > Roles gains the word "Operator" (+2 words).

**3. Shape of `AGENTS.md`.**

| Option | What it is | At upgrade |
|---|---|---|
| (a) Router only | About 50 words at the top: running, read `RULES.md`; developing, read on | No conflict, but the 723 words still load for a run-only agent, so #79 is unsolved |
| (b) Full split (#79) | Development text becomes new files | Largest conflict; new install rows are an engine change (heavy, Security Review) |
| **(c) Middle** | Every parsed heading and slot stays. Each development section keeps its first rule sentence and a pointer; the rest moves under a new heading in `dev/agent_collaboration.md`, a file adopters already receive | Edits inside a moved paragraph conflict: the 2026-11-11 trial (`dev/strategy/2026-11-10-claude-agents-md-diet.md`) found one word changed in a removed paragraph made 93 of 206 lines conflict, and `--apply` refuses until resolved. A rule appended at the end merged clean |

Recommend (c): it solves #79 with no engine change. The plan reruns the trial and writes the upgrade note.

**4. What the release rule needs.** In a project that opts in, `RULES.md` ships whole (no per-section rule, so no parser). `AGENTS.md` ships, and its pointers into `dev/` are the one allowed exception to "nothing a release keeps cites `dev/`" (#69, #75). This proposal states the exception in the `RULES.md` template. It does not design the release module (v0.9) or the citation check (board row "A project can leave Cairn out of a release").

**5. Dependencies.**
- *Trim draft* (`2026-11-16-claude-template-trim-and-rules.md`) lands first: same files, 5 words of cap room, and its item 8 asks for this as a follow-on. If its Decision folds #74, #76 and #79 into the trim, item 3 merges into its rewrite; items 1, 2 and 4 are small and ride along.
- *Repository layout* (accepted 2026-11-12) fixes final paths and the fate of `VENDOR.md`.
- *Staged-modules draft*: both edit `dev/rules/README.md`; land one at a time. If it is rejected, item 1 stands alone.
- *Leave-out row* consumes item 4 and need not wait.

## Rationale

Opt-in keeps shipped weight flat; moving text to a file adopters already receive avoids an engine change.

## Alternatives considered

Do nothing: adopters merge by hand each upgrade. Options (a), (b): tabled. Split for every project: each pays for a job it may lack.

## Documentation / doctrine surface

`templates/core/AGENTS.md`, `RULES.md`, `dev/rules/README.md`, `dev/agent_collaboration.md`, `docs/methodology/roles.md`; Cairn's own `AGENTS.md` follows its shipped copy. **Does any rule weaken or disappear?** None is deleted. One weakens: development rules past each section's first sentence leave always-loaded text and load only when the agent follows a pointer, which it can skip (the risk the 2026-11-10 trim note named). Ask-before-push, commit-explicit-paths, plain-language and model-tier rules stay in `AGENTS.md`.

## Evidence / verification plan

Evidence is one adopter. I ran no tests, installs or upgrades. A second project must show it also needed run rules apart, and that a run-only agent missed nothing. **Wrong if:** an opted-in adopter still hand-edits `AGENTS.md`; a review finds an agent broke a moved rule; or a second project defines a different third role. Checks: `wc -w` against the cap, the upgrade trial, tests naming changed files. Not run yet.

**Security preflight**: N/A: no trust boundary added; prose only.
**Independent scientific check**: N/A: no scientific result touched.

## Assurance path

**Assurance path**: high-assurance — it edits governing doctrine (`docs/methodology/roles.md`) and named always-loaded templates.
