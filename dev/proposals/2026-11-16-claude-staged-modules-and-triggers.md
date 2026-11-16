# Offer a module when the project reaches the need: a first trigger, guidance only

**Author**: Claude Sonnet 5.5 (`claude-sonnet-5-5`)
**Status**: awaiting-review
**Waiting on Maintainer**: release draft for review
**Review**: usual
**Proposed tier**: standard — it adds a mechanism and edits two shipped files, but no installer code; the Maintainer sets the tier
**Plan review**: required(Internal)
**Opened**: 2026-11-16
**In brief**: When a project's rules folder has grown past a stated size, the session-start routine tells the person what a guidance module does and costs and asks, and remembers the answer in a committed file.

## Decision summary

Cairn guides a project through starting and says little once it has grown. The Maintainer agreed on 2026-11-16: "Yeah we need to have triggers that offer new modules to the adopter". This proposal is the smallest version, with no code change: one trigger, one offer, one record of answers. The trigger is a `dev/rules/` folder over 5,000 words. The offer is a short guidance section on organizing a grown rules folder; the agent explains what it does and costs, and asks. An answer is written to a committed file and not repeated.

Cost: about 90 words added to the session-start skill, about 300 to the shipped `dev/rules/README.md` (read on demand, not every session), and one small adopter file created only when someone answers. No new shipped file, no installer change. A tool that reads triggers, and offers that install real module files, wait for a later heavy proposal.

## Context

- Each module states "Selected when", a condition on the profile given at install (`templates/modules/README.md`). Nothing looks again. `upgrade --plan` prints one line, "new modules available (opt-in)", with no description (`new_modules` in `bootstrap/_scaffold/upgrade.py`).
- LHM's rules folder grew from 2,327 words in 3 files to 10,523 in 13 in three days (strategy note, measured by its author). Cairn's own `dev/rules/` holds 2,651 words in 7 files (`wc -w`, today).
- An unselected module has no file in the adopter's repository, and every shipped file is a row in an install table in `bootstrap/_scaffold/config.py`, a protected surface. So a trigger written in an unselected module cannot be read, and any new shipped file is an engine change. That sets the tier.
- The `session-start` skill is manual only (`disable-model-invocation: true`) and ends with judgment steps for the agent.

## Proposal

1. **Declaration.** One line, `Offered when:`, at the top of the guidance section in `dev/rules/README.md`. A trigger is a count or existence test over named paths: words or files in a folder, a file present or absent. No network, no Git history, standard tools only. Judgment ("the rules feel big") is not a trigger.
2. **Who checks.** The agent, in a new bullet in the skill's step 3: find `Offered when:` lines, evaluate each by a count (not by reading files), skip any offer the record answers, make at most one offer per run. It speaks only when someone runs session-start. Cost: one folder listing and one word count; not timed.
3. **The offer.** Plain language: what the guidance covers, what it costs (about 300 words on disk, no tool, no change to always-loaded files), the measured figure, and that either answer is fine. Nothing is applied without a yes.
4. **The record.** `dev/modules/offers.md`, created on the first answer and committed by the agent that records it, so every vendor's tool reads one file. One line per answer: `2026-11-16 | rules-folder-growth | declined | Maintainer | measured 5,412 words`. Only an answer the person gave is recorded. Reopen by deleting the line (Git keeps it) or by asking.
5. **First trigger and module.** Trigger: `dev/rules/` (README excluded) over 5,000 words. Evidence: LHM at 10,523 words asked for guidance; Cairn at 2,651 works without it. 5,000 lies between them and is a judgment, not a fit. Guidance: entry shape, an "Applies when" line, a size budget per entry, run rules apart from development rules, how a rule enters and leaves (the strategy note's list of what LHM converged on); the text is drafted in the plan.
6. **Later.** A table printed by `session.py session-start`, offers that install module files via `--adopt-module`, and descriptions in `upgrade --plan`. Each needs an installed offers table, so it touches the engine: tier heavy with Security Review, after the repository layout (`dev/proposals/2026-11-09-claude-repository-layout.md`, accepted). The record's path moves with `dev/modules/` if the layout moves it (not checked).

**The upgrade row.** Keep "Offer new and unselected modules at upgrade" separate: it concerns `upgrade --plan` and the engine, and would share the record file. Its open question stays the Maintainer's: does "not automatically" also cover core and skills files that upgrade adds automatically today (`bootstrap/UPGRADE.md`)? Recommended default: no, keep them automatic; they are the unconditional tier. This proposal's two edits arrive that way, so a "yes" would change how they ship. The strategy note's question 5 (the wrapper file) is not part of this proposal.

## Rationale

The risk in triggers is human: a wrong or noisy offer costs trust. Guidance only tests that cheaply, in editable files, before a tool is built on an unproven threshold. This is the go-ahead request the standing direction asks for; the later tool needs its own.

**Measured:** offers made, accepted and declined, counted from the record in each adopter. **Wrong if:** an offer repeats after an answer; fires below its threshold; or an adopter calls one noise or already covered. Any one withdraws the trigger. Limit: both adopters are past the threshold and have their own answer, so early offers will likely be declined. That tests silence and memory, not usefulness, which needs a third adopter.

## Alternatives considered

- **Do nothing.** Each adopter invents its own structure, as LHM did.
- **Installer now.** Delivers module files and descriptions, but is an engine change that waits for the layout and fixes a threshold built on two points.
- **Word count printed by `session.py`.** More reliable than agent counting, but edits the file holding the interpreter-binding reader. Defer until the first offers show the threshold is right.

## Documentation / doctrine surface

`templates/skills/session-start/SKILL.md` (1,756 words, +90) and `templates/core/dev/rules/README.md` (359, +300), both shipped by existing install rows. `AGENTS.md`, `RULES.md` and install tables are unchanged. Adopter burden: two edited files arrive on upgrade; one record file appears after an answer. Cairn's burden: keep one trigger line and one section accurate.

Proposed paths:
- `dev/modules/offers.md`

## Evidence / verification plan

Falsifiers: the trigger fires on Cairn's own folder, fails on a padded copy, or a second run repeats an answered offer.

### Tests required

No code changes, so no new test. Run the tests that name the two edited files (`python tools/test_tiers.py for <paths>`); delete one that pins old wording. Not run yet.

### Examples / smoke checks

Scratch trial by the plan's implementer: no offer for Cairn's `dev/rules/`; one offer in a copy padded past 5,000 words; silence on a second run after an answer. Also `python scripts/check_cairn.py` and `python scripts/claim_check.py`.

#### Security preflight

N/A: no trust boundary added or widened. `templates` are on the protected-surfaces list, so the Maintainer may still call for Security Review.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Assurance path

Usual review, then a standard plan reviewed internally. After offers reach an adopter, the Maintainer reads `dev/modules/offers.md` against the signal above before any tool is proposed.
