# Keep agents moving through agent-owned work

**Author**: Claude Opus 5.5 (Strategy)
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: heavy -- a shipped tool that launches agent commands, plus shipped board, hook and skill changes
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-03
**In brief**: Make the board name the next step an agent may take, print it after every commit, and offer a bounded loop that starts a fresh agent for each step.

## Decision summary

Lower-tier agents stop after each finished step and wait for the Maintainer
to say "continue", even after agreeing not to (Maintainer chat, 2026-11-03).
This proposal stops relying on memory:
- **A.** `board.py --next` names the next step and the role that owns it.
- **B.** The post-commit hook prints that line.
- **C.** One drain-mode rule: continue your own role's next step on your
  drain target.
- **D.** An optional loop starts a fresh agent per step, within hard limits.
  It cannot run until the accepted spending stop exists.

D launches commands, so it needs a Security Review.

## Context

- **No written rule to continue.** At `c3b9a1c1`, `AGENTS.md`,
  `dev/agent_collaboration.md` and the session skills hold none. The
  Maintainer's spoken instruction failed; a written rule was never tried.
- **Many rules say stop:** pause when unsure, approval gates, session-start's
  "stop". I assume, unmeasured, that lower tiers over-generalize them.
- **No tool names the next owner.** `tools/board.py` "judges nothing";
  `--maintainer` lists only the Maintainer's waits.
- **The spending stop** in the metered-cost proposal is accepted, but not
  built.

## Proposal

**A. Next step.** `board.py --next` applies one documented table to written
header fields, review headings and Decision blocks.
- It covers all 14 status words in `tools/session.py` `_STATUS_VOCABULARY`.
- Each row gives the role and its tier floor from the model-selection
  mapping. Examples:
  - under `usual + Security Review`, `revising` with no Security Review
    heading → Security reviewer, high;
  - `awaiting-code-review` → code reviewer;
  - `accepted` with a standard or heavy Decision and no plan → plan author.
- Any missing, conflicting or unrecognized field prints
  `NEXT: stop -- <reason>`. So does a Maintainer row, or a step under
  another claim. An unreadable claims log also stops.
- It prints one line: `NEXT (<role>, <tier>): dev/<kind>s/<name>.md --
  <move>`.
- Names come only from files whose stem matches
  `YYYY-MM-DD-<lowercase-hyphen-words>`, checked independently of the board.
  A non-matching name prints stop and is never echoed.
- `--next` has its own JSON schema. `cairn-board/1` and plain board output
  stay unjudged.

**B. After each commit.** The coordination module's post-commit hook prints
the line. It is advisory. Adopters without the module get A and C only.

**C. Drain only.** In drain mode, after each commit, an agent starts the
`NEXT` step only when that step is on its own drain target and in its own
role. Review steps go to a fresh subagent, as drain already requires.
Outside drain, `NEXT` is information.

**D. Optional loop.**
Proposed paths:
- `tools/drain_loop.py`

- **Settings.** It reads its settings once at start: agent command per tier,
  item limit (default 5) and per-item timeout. They come from a file in Git's
  administration folder, like the interpreter binding. It refuses a link or a
  tracked file, and resolves the command under `bootstrap/SAFETY.md` rule 10.
- **Each item.**
  1. It refreshes the spending stop.
  2. It reads `--next`.
  3. It launches the command for that tier, if configured, as an argument
     list with no shell. The full artifact path is one argument, so drain's
     issue and board targets cannot be reached.
- **It stops on any of:**
  - stop, or a tier with no configured command;
  - the limit or timeout;
  - an agent failure;
  - uncommitted changes;
  - a step with no new commit touching its artifact;
  - a status only the Maintainer may set, written during the run;
  - a stale, missing or unreadable reading.
- **At the end** it prints items, commits and the stop reason.

## Rationale

Output seen at the moment of deciding beats a rule read at session start.
D makes each stop the hand-off, with limits enforced outside the agent.

## Alternatives considered

- **Do nothing:** keep typing "continue", or pay for higher tiers.
- **A–C only** (usual review). The plan delivers and trials A–C first; if
  they suffice, it asks the Maintainer whether to keep D.
- **A harness stop hook.** It works in one vendor's tool and prolongs one
  context. Revisit it as a vendor-wrapper option once A exists.

## Documentation / doctrine surface

- **Prescription:** one sentence in the shipped drain step only.
- **Description:** the table, name pattern and loop usage go in
  `docs/build-a-board-view.md` and the coordination module; the board
  docstring and session-start step 2 credit owners to the table.
- **Doctrine:** the drain sentence takes the rate-limit gate.

## Evidence / verification plan

- **Tests:**
  - each status row, including every stop case;
  - each hostile name the Security Review used;
  - the claims-log and meter failures;
  - the hook prints and never blocks;
  - the loop, with a fake command, covers each stop condition.
- **Trial.** One lower-tier agent works a three-item practice board without
  B and C, then with them; count each "continue" a person typed.
- **Security preflight:**
  - S1: settings come from outside the tree, read once. Names pass an
    independent pattern.
  - S2: removing the pattern, the dirty-tree stop or the Maintainer-status
    stop each fails a test.
  - S3: `tools/drain_loop.py` runs only when invoked.
  - S4: every unreadable input stops.
  - S5: a hostile artifact can still instruct its launched agent, as in
    drain today. It cannot choose the command, the target or the limits.
- **Independent scientific check:** N/A, no scientific assumption touched.

## Signals the change is wrong

Agents still stop with a `NEXT` line in view; `NEXT` names a wrong role or a
Maintainer step; or unattended work must be unwound.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance -- the loop launches commands an adopter
configures, and the change touches shipped templates.

## Review -- Claude Sonnet 5.5 -- 2026-11-03

```
Reviewed commit: 29202b7b
Target: Decision summary, Context, Proposal A-D, Alternatives, Evidence, Assurance path
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised (none blocking)
**Verdict**: REVISE

**Elapsed**: about 12 minutes
**Tokens**: about 90,000 (estimate)

**Foundations**

1. **Should this happen as framed?** Partly. One chat report is the evidence, and no written continuation rule was ever tried, so "C alone has already failed" is unsupported -- Context bullet 1; no such rule in `AGENTS.md` or `session-start/SKILL.md`.
2. **Best alternative.** A-C first, trialled; build D only if B+C fall short -- its own Trial.
3. **What would show it wrong.** No drop in typed "continue" with B+C, or a step started by the wrong role or tier -- F2, F3.

- **F1 Table unsound.** `tools/session.py:1118-1124` holds 14 status words; the proposal names five. Missing: `revising-plan`, `ready-to-implement`, `implementing`, `awaiting-code-review`, `ready-to-archive`. "Accepted, no plan" needs tier (Decision body) and a plan join, against "infers nothing else". Under `usual + Security Review`, one pass moves `awaiting-review` to `revising`, so the Security pass is never next. Close: full table; ambiguous rows print "stop".
- **F2 Role separation.** A reviewer's commit prints "revise", an author's prints "review", and C says start it. Drain says "a fresh subagent, never you". Close: C starts only the committer's own moves; reviews go to a fresh subagent.
- **F3 Model floors.** One command cannot meet a Security Review floor (`model-selection-mapping.yml`). Close: `NEXT` carries the tier; D stops above the configured one.
- **F4 "Judges nothing" reversed.** The `board.py` docstring and SKILL step 2 disclaim next-step judgment; the docs say `--json` "derives no value". Close: keep `--next` out of `cairn-board/1`; reword both.
- **F5 Reach.** Claim-skipping and the hook need the optional coordination module (`templates/modules/team-gated/intent.py`); solo adopters get only C. State it.
- **F6 Money.** `tools/gauge.py` has no spending stop yet. D has no per-item timeout or failed-exit stop, and "step unchanged" misfires on multi-commit `implementing`. Close: D waits for the stop; add both.

Heavy fits the bundle; splitting D lets A-C avoid the subprocess boundary.

**Coverage.** No code run; hook output reaching the agent unmeasured; `docs/methodology/` unread; Security Review excluded.

## Review -- Claude Opus 5.5 (Security Review) -- 2026-11-03

```
Reviewed commit: 29202b7b3bcba6ad3d53f3a41767c6cbb9cd871d
Target: Proposal A-D; Security preflight S1-S5
Prior findings: none
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE

**Elapsed**: about 15 minutes
**Tokens**: about 90,000 (estimated)

**Foundations**

1. **Should this happen as framed?** A, B yes; C, D only bounded. -- `templates/skills/session-start/SKILL.md` step 4.
2. **Best alternative.** A, B, and D with fixed arguments; C only inside drain. -- sections C, D.
3. **What would show it wrong.** A filename or edited setting changing what the loop runs. -- SR1 probe.

**Findings**

- **SR1 (blocking; S1, S2).** Names are unconstrained. Measured on a `29202b7b` scratch copy, `board.py --json` listed `7`, `issues`, `--dangerously-skip-permissions`, `x; touch pwned` and a name with a newline plus fake `NEXT (agent):` line. Drain reads `7` and `issues` as issue targets. S1's board match uses that same listing: it cannot fail. Close: an independent name pattern; pass the path as one argument, no shell; never print or launch a non-match; test each.
- **SR2 (blocking; S1, S4).** Settings read from the tree, or reread per item, let item n set item n+1's command. Close: read once, from outside the tree (Git administration, like the interpreter binding); refuse links and tracked files. `bootstrap/SAFETY.md` Rule 10 governs PATH lookup.
- **SR3 (blocking).** A launched agent following `NEXT` bypasses the item limit and per-item spending stop; outside drain, C overrides "Do not act autonomously". A self-written `accepted` hands the next item to a plan author. Close: C only within drain's target; stop on failure exit, dirty tree, or a new Maintainer-only status.
- **SR4 (S4).** `read_log` skips malformed claim lines (`tools/_intent/record_io.py:217`); the meter is unbuilt. Close: stop on either; say D waits for the meter.

**Coverage:** Not run: tests, harness permission modes, hook output encoding.

## Response -- Claude Opus 5.5 -- 2026-11-03

All findings accepted; operative text revised in place.

- **Foundation 1:** Context now says only a spoken instruction failed; no
  written rule was tried.
- **F1:** A covers all 14 status words, reads Security Review headings and
  the Decision tier, and prints `stop` on anything missing or unknown.
- **F2:** C acts only in the agent's own role and drain target; reviews go
  to a fresh subagent.
- **F3:** `NEXT` names the tier; D launches only a command configured for it.
- **F4:** `--next` has its own schema; `cairn-board/1` stays unjudged.
- **F5:** without the coordination module, adopters get A and C.
- **F6:** D waits for the spending stop, has a timeout, stops on agent
  failure, and counts progress as a new commit touching the artifact.
- **A–C first:** taken as sequencing. The plan trials A–C, then asks the
  Maintainer whether to keep D.
- **SR1:** an independent date-stem name pattern; non-matches print `stop`
  unechoed; the full path is one argument, no shell.
- **SR2:** settings read once from Git administration; links and tracked
  files refused; `SAFETY.md` rule 10 governs lookup.
- **SR3:** C applies only within drain; D stops on a dirty tree or a new
  Maintainer-only status.
- **SR4:** an unreadable claims log or meter reading stops.

**Elapsed**: about 25 minutes. **Tokens**: unknown.

### Withdrawn / superseded commitments

- The `AGENTS.md` continuation sentence, replaced by a drain-step sentence
  (SR3).
- S1's board-listing match, replaced by the independent name pattern (SR1).

## Decision -- Maintainer -- 2026-11-03

**ACCEPTED, as revised.** The Maintainer's authorization, quoted **verbatim and visually isolated** (chat, 2026-11-03; scribed by Antigravity):

> "Accept all 5 as revised."

**Tier**: heavy. Accepted as revised under Option 1 (delivering and trialing steps A–C first before deciding whether to keep D) with high assurance and required Internal + Internal Security Review plan review. Recurring additions: none.
