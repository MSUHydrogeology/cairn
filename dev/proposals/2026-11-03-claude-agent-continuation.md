# Keep agents moving through agent-owned work

**Author**: Claude Opus 5.5 (Strategy)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy -- a shipped tool that launches agent commands, plus shipped board, hook and skill changes
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-03
**In brief**: Make the board name the next step an agent may take, print it after every commit, and offer a bounded loop that starts a fresh agent for each step.

## Decision summary

Lower-tier agents stop after each finished step and wait for the Maintainer
to say "continue", even after agreeing not to. The Maintainer reported this in
chat on 2026-11-03. This proposal stops relying on the agent to remember to
continue:

1. **`board.py --next`** reads each artifact's status and prints the first
   step an agent may take, or says that nothing is agent-owned.
2. **The post-commit hook prints that line** after every commit, where the
   agent sees it at the moment it decides whether to stop.
3. **An optional dispatcher loop** starts a fresh agent on each agent-owned
   step in turn, within an item limit and the accepted spending stop, and ends
   with one summary.

The cost is a small change to the board tool and hook, one new shipped
script, and a Security Review, because the script launches commands.

## Context

- **Nothing tells an agent to continue.** On `0.7-dev` at `c3b9a1c1`,
  `AGENTS.md`, `dev/agent_collaboration.md` and the session skills have no
  rule to start the next owned step. A search for continue, next-item and
  end-the-turn wording found none.
- **Many rules say stop:** pause when unsure, approval gates, session-start's
  "stop". I assume, unmeasured, that lower tiers over-generalize them.
- **No tool names the next owner.** `tools/board.py` "judges nothing";
  `--maintainer` lists only what waits on the Maintainer. The proposal
  template says "each status names who holds it next", but no tool reads it.
- **Drain mode** (`templates/skills/session-start/SKILL.md`, step 4) says "go
  to the next", but inside one session that can still stop.
- **A spending stop is accepted** in the metered-cost proposal, checked
  "before each drain item". It has no plan yet.

## Proposal

**A. Next owned step.**
- `board.py --next` maps each status to who holds it, using one documented
  table. For example:
  - `awaiting-review` and `awaiting-plan-review`: a reviewer agent;
  - `revising` and `revising-code`: the author;
  - `awaiting-decision` and any declared fence or wait: the Maintainer;
  - an accepted standard or heavy proposal with no plan: the plan author.
- It prints exactly one line:
  - `NEXT (agent): <artifact> -- <move>`, or
  - `NEXT: none agent-owned; stop and report`.
- It skips artifacts under another session's active claim.
- `--json` carries the same field. The table reads written statuses only; it
  infers nothing else.

**B. Printed after each commit.** The existing post-commit hook in
`tools/_intent/cli.py` and its shipped copy appends the `NEXT` line. It is
advisory and never blocks a commit.

**C. One continuation rule.** One sentence in `AGENTS.md` and the drain step:
after each commit, read the `NEXT` line and start that step in the same turn,
unless it names the Maintainer, a stop condition in drain mode applies, or
the step is under another claim.

**D. Optional dispatcher**, shipped with the coordination module.
Proposed paths:
- `tools/drain_loop.py`

It loops:
1. Read `board.py --next --json`.
2. Stop if nothing is agent-owned, the next step is the Maintainer's, the
   item limit is reached (default 5), the same step comes back unchanged, or
   the accepted spending stop says no.
3. Otherwise run the Maintainer's locally configured agent command once,
   with that artifact as the drain target, in a fresh session.

At the end it prints one summary: items run, commits, stop reason. The agent
command comes only from an uncommitted local setting, so the file names no
vendor.

## Rationale

Tool output read at the moment of deciding is followed more reliably than a
rule read at session start. D makes each stop the hand-off, with a fresh
context per item.

## Alternatives considered

- **Do nothing:** the Maintainer keeps typing "continue" or pays for higher
  tiers.
- **A rule alone (C only):** its spoken form has already failed.
- **A harness stop hook** that refuses an agent's end of turn and hands back
  the next step. It works in one vendor's tool only and prolongs one context;
  revisit it as a vendor-wrapper option once A exists. Its interface was not
  tested here.

## Documentation / doctrine surface

- **Prescription:** the one continuation sentence in `AGENTS.md`, with its
  shipped template and the drain step.
- **Description:** the status-owner table and dispatcher usage go in
  `docs/build-a-board-view.md` and the coordination module.
- **Doctrine:** the `AGENTS.md` sentence takes the rate-limit gate.

## Evidence / verification plan

- **Tests.**
  - Board tests cover every status's owner, claim skipping, and the `none`
    line. The plan maps the exact files.
  - Hook tests check that the line prints and never blocks.
  - Dispatcher tests use a fake agent command and cover each stop reason,
    the limit, the no-progress stop and the summary.
- **Trial.** One lower-tier agent works a three-item practice board without
  B and C, with them, and through D; count each "continue" a person typed.
- **Security preflight.**
  - S1: the command comes only from local configuration; the artifact name
    must match a board listing under `dev/`.
  - S2: removing the name match must fail a test.
  - S3: `tools/drain_loop.py` runs only when invoked.
  - S4: any unreadable state stops the loop.
  - S5: a hostile artifact can still instruct the agent it starts. That is
    unchanged from drain mode, which already treats artifact text as data.
- **Independent scientific check:** N/A, no scientific assumption touched.

## Signals the change is wrong

Agents still stop with a `NEXT (agent)` line in view; the loop repeats a
step; `NEXT` names a Maintainer step; or unattended work must be unwound.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance -- the dispatcher launches commands an
adopter configures, and the change touches shipped templates.
