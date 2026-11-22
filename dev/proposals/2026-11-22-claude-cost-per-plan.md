# Cost per plan, from the usage meter

**Author**: Claude Fable 5.2 (Strategy)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — it changes three shipped tools (the usage meter, the work-claim tool and the pulse) and adds one working rule
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-22
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/working-agreements.md, dev/rules/conventions.md, dev/rules/custom_session_routines.md, dev/rules/development-environment.md
**In brief**: The usage meter will report what each plan and each of its steps cost, by counting the usage of the agent run that did the step, so the token figure every step record asks for stops being "unknown".

## Decision summary

Every review and record in a plan ends with a token figure, and it almost always says "unknown": an agent cannot see its own usage. The usage meter can see it, in the assistant's own logs, but today it ties no usage to a plan.

This proposal makes the meter count by **run**: one agent's stretch of work, which the log already marks. A one-line **stage declaration** in the project's own record says which plan and step a run is doing. The end-of-session report then prints the cost of each plan and step, and a plan's closeout carries its table.

The cost is one short command each time an agent is started or resumed. Three choices are the Maintainer's; they end the Proposal section.

## Context

- **The field is empty.** In the 35 plans and proposals of 20 to 22 November, 158 of 163 token figures say "unknown" (counted by search). The Maintainer wrote on 2026-11-22: "This was always the intent of the tokens field in the plan".
- **The meter's present tie does not work.** It ties a reply to a file only while one work claim (the short notice an agent files before editing) is open around it. Measured in the meter's own record on 2026-11-22: 298 claims, and 0 of 295 replies tied. Claims last a median of 22 seconds, sub-agents share one tag so their claims collide, and 109 claims never released block every later tie.
- **The logs do mark runs.** Each reply of a Claude sub-agent carries that agent's run id, and it equals the id the tool gives the session that started the agent: 11 of 11 on 2026-11-22. Summed by hand that day, plan J's agents cost 6.37 dollars at public prices and plan K's 2.39, against 47.73 for the coordinating session (`dev/measurement/agent-step-costs.md`, "Cost by plan, priced").
- **A sub-agent cannot name itself.** Its environment holds the same names and the same session tag as the session that started it (probed 2026-11-22). So its starter must declare it.

## Proposal

One outcome, in one plan: **the report gives the cost of each plan and step.**

1. **Runs.** With each reply it counts, the meter records which run made it: a session's own thread, or a sub-agent's run id kept as a digest (a one-way fingerprint). For Codex a run is a thread. Antigravity follows when its reader exists.
2. **Stage declarations.** A new command of the work-claim tool writes one line to the project's own claim record: the run, the plan or proposal, a short step name and the time. An agent declares its own thread. Whoever starts or resumes a sub-agent declares it, with the id the tool returned.
3. **The tie.** A reply counts toward the latest declaration of its run at or before its time. A reply of a run with no declaration is reported as not tied, with its cost, so gaps show.
4. **The report.** The summary and the pulse give, for each plan and step: model, replies, tokens by kind, the weighted total, first and last time. Then each plan's total, then what is not tied.
5. **The record.** A plan's closeout carries its table from the meter. Step records keep their own field and may still say "unknown".
6. **A ledger survives the change.** A ledger from before it loads and is brought forward, not refused.
7. **The old tie goes.** The claim-window tie to files is removed, with its rule that an unreleased claim blocks later ties.

Kept: the meter reads only what the consent file lists, and takes from a log only counts, times, model names and run fingerprints. Plan and step names come from the project's own record, checked for form and length.

**Choices for the Decision.**

1. **Release.** v0.9, although the defect arc's Decision kept v0.9 free of notable new features; or v0.10. Recommended: v0.9. The tightening needs this measurement, and it completes a field Cairn already has.
2. **The old tie.** Remove it (recommended), or keep it beside the new one.
3. **Tier.** Heavy, as proposed.

## Rationale

The run is the one unit the logs mark exactly, with no reading of what was said. The declaration is the least a project can add: who is doing which step. The rest is arithmetic the meter already does.

## Alternatives considered

- **Hold a work claim for a whole step.** Sub-agents share one tag, so parallel steps still collide, and the claim warns other agents off the file all that time.
- **Read the plan from the log**, from the label a starter gives its sub-agent. That breaks the promise that only counts leave a log.
- **Keep the hand-kept record.** Its figure is the harness's, near the size of a run's last request: 18.9 million tokens against 725 million real ones on 2026-11-22.
- **Let each agent declare itself.** A sub-agent cannot learn its run id. Kept only for a session's own thread.

## Documentation / doctrine surface

Governing layer: one sentence in `AGENTS.md` beside the rule on recording token use, and the plan template's closeout text. Deliberation layer: the session routines gain the declaration. Descriptive layer: both measurement READMEs and the changelog.

## Evidence / verification plan

Strategy checks the first plan built after the change, on a real machine: the meter's cost for each step equals an independent count of the same logs by run id, as was done by hand on 2026-11-22. A mismatch falsifies it. So does a reply filed under the wrong plan while two agents ran at once.

### Tests required

Two, each through a refresh. (a) A session thread and two sub-agent runs working at once on two plans, with one run resumed for a second step and one run undeclared: exact totals for each step, and the untied row. (b) A ledger written before the change loads and keeps its counts.

### Examples / smoke checks

`python tests/check_cairn.py` on each changed document.

#### Security preflight — five questions, answered in writing

- **S1.** The meter decides which plan a reply counts toward, from the run id and time on the log record and the declaration in the project's own claim record. A log cannot name its own plan. Whoever can write the project can write a declaration, and already owns the report.
- **S2.** A declaration that names another run, or is dated after the reply, ties nothing. Test (a) plants both.
- **S3.** `meter.py refresh` runs the tie over the consented sources and the listed projects. The README will say: "a reply counts toward a plan only when the project's own record declares the run that made it."
- **S4.** A malformed declaration is skipped and its replies stay untied. Less is tied, and nothing more is read.
- **S5.** Someone who can write the project's record can misfile costs in a report they can already edit, and no more. For log content the class is closed by construction: only counts, times, model names and fingerprints cross.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Declarations get forgotten, and the untied row stays large. Per-step totals disagree with an independent count. Agents spend more on declaring than the figures are worth.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance

## Review -- Claude Sonnet 5.5 (Reviewer) -- 2026-11-22

**Reviewed commit**: 93c030a3. **Verdict**: REVISE.

**Foundations.**
1. *Should this happen as framed?* Yes in aim; the design needs two repairs. The meter has a sub-agent record (`agent_runs`) but does not attach a run to a reply: Claude replies use the session as their thread (`meter.py` line 4063), so the run fingerprint is new data on every reply, which the text does not say.
2. *Best alternative.* The four rejected options are fairly put. None beats a per-run declaration; "declare once per agent" is the right unit.
3. *What would show it wrong.* Foreground agents' early replies untied, and one hostile line stopping the meter (findings 1 and 2).

**Problem shown.** The three reasons hold in code: the 22-second windows, the shared tag (`overlap`, `collisions`), and an open claim blocking later ties (`open_claim`). A fourth is real: a claim naming more than one file never ties. My recount of token figures gave 131 "unknown" of 136 with a narrower search than yours; name your search.

**Findings.**
1. **Blocking: the declaration format, and S4 is false today.** `_claim_snapshot` raises `Unavailable` on any event that is not `claim` or `release`, and on any malformed line. So a new line kind stops the meter for the whole project, and a hostile line does too. It is "skipped" only if the proposal changes this. The record-writing and conflict code (`_intent/record_io.py`, `conflict.py`) also know only the two kinds.
2. **Blocking: replies before the first declaration.** A starter learns a sub-agent's id after it starts, so its first replies precede the declaration and stay untied under rule 3.
3. **Blocking: "A ledger survives" is not checkable, and "brought forward" is new.** Older schemas are refused today (`ledger_old_schema`). Old replies have no run fingerprint.
4. Non-blocking: removing the old tie also removes the artifact column of today's report (`meter.py` lines 2290-2392); say what replaces it. Say a declaration's step name uses the same safe-name check as claim targets.

**Not covered**: logs, the Security Review questions, running anything.

**Exact words.**
- Proposal item 2, add: "The declaration is a new event kind in the claim record. The meter's reader skips any line of a kind or shape it does not know, and the writer and conflict code ignore it; a malformed line never makes the project unavailable. Test (a) plants one."
- Rule 3, add: "A run's replies before its first declaration count toward that declaration; a run never declared stays untied."
- Item 6, replace with: "The ledger schema is raised and a version-6 ledger is migrated, not refused. After a refresh the event count and each day's token sums equal their values before; replies counted earlier are reported once as 'before run tracking', not as untied. Test (b) checks this."

**Time and tokens**: unknown; unknown.
