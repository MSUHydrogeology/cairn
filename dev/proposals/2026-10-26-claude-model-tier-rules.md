# Use the lowest model tier that is safe, and say which one ran

**Author**: Claude (Strategy)
**Status**: awaiting-review
**Review**: usual
**Plan review**: required(Internal)
**Opened**: 2026-10-26
**In brief**: Every Cairn project gets a short rule to pick the cheapest model that can safely do the work, name it when it starts a helper agent, and move up one tier when a cheaper one fails.

**Authoring tier.** Doctrine sets proposal authoring at the high tier
(`doctrine/roles.md:167-172`). I wrote this at the medium tier because the
Maintainer directed it. The floor is lowered for this proposal only, and for
authoring only. The Maintainer's words:

> "I would also like to formalize a rule set for using lower-tier models where possible."

> "Go ahead and spawn the lowest-tier agents you can to design, review, and implement proposals toward 0.5"

## Context

This is a doctrine change, so it meets the rate-limit gate
(`doctrine/rationale.md:442-452`), which names recurrence, synthesis at a
routine boundary, or a Maintainer high-risk classification. The direction above
is none of those, so I ask the Maintainer to accept it as the evidence at the
Decision, which will record that. As doctrine the change is small (lane wording
and one sentence in `doctrine/roles.md`).

**What exists.** A floor by role (`doctrine/roles.md:149-197`): high for
Strategy, proposal review, Security Review and scribing; medium for non-trivial
implementation, plan review and code review; low for trivial chunks. The
`model-selection` module holds the role table
(`templates/modules/team-gated/model-selection.md:45-59`), a fan-out table
(`:94-109`) and a mapping schema (`:170-191`); Cairn's mapping is
`dev/.cairn/model-selection-mapping.yml:19-36`. The only check
(`scripts/check_model_selection.py:5-10`) fails on a `FILL ME` stub.

**Seven gaps, each checked. Gap 5 is narrower than it first looked.**

1. **Reach.** Only `collaborative-team` and `high-rigor-legacy` install the
   module (`bootstrap/_scaffold/config.py:1363-1391`); `solo-greenfield` installs
   none (`:1354-1361`). `AGENTS.md` has no tier text (searched "model", "tier").
2. **No trigger.** The module says tools let a sub-agent inherit the
   orchestrator's tier silently (`:91-92`). Nothing makes anyone name the model,
   and no tool sees which one a harness picked. Cairn has no CI (`AGENTS.md:408`),
   so the only triggers are a reader and a text check.
3. **"Risk" is undefined.** The floors rest on each adopter's complexity-axis
   placement (`doctrine/roles.md:191-197`); "trivial chunks" (module `:56`) has no
   definition. The lanes (`doctrine/lifecycle.md:40-78`) are a closed procedure
   every adopter already runs.
4. **No escalation for roster roles.** Fan-out has one
   (`doctrine/roles.md:224-225`; module `:134-135`); an author or reviewer has none.
5. **Nothing measures whether lower-tier work holds up** (the mapping binds
   tiers "by name, not by measurement", `dev/.cairn/model-selection-mapping.yml:11-12`).
   20 of 21 proposal-review headings from 2026-10-17 to 2026-10-26 name a model
   in the reviewer's name, by habit; the proposal template has no Model line,
   while plan and code review forms ask for one (`doctrine/plans.md:724`, `:929`).
   The author's model is not recorded: 11 of 12 proposals in that window read
   `**Author**: Claude (Strategy)`. I did not count plan or code reviews.
6. **The standing preference is private.** "Pass a cheaper model on new agent
   calls" is in an agent's memory directory, not the repository, though durable
   state belongs in the committed tree (`CLAUDE.md:17-34`).
7. **The cost rule's check needs a different maker.** A cheaper author may write
   below its floor only if a stronger tier of a different model architecture
   checks it (`doctrine/roles.md:227-234`; module `:126-131`, `:140-147`; pinned at
   `bootstrap/tests/test_review_stance_in_shipped_files.py:943-955` and
   `:1148-1157`). A one-vendor team cannot meet it. It is a permission, so it
   breaks no rule that a tier may not require a different agent type, but it
   closes below-floor writing for most adopters (Question 1).

## Proposal

Five rules. No new header field, parser, file, tool, gate, status or config key.

**R1. The lane sets the lowest tier to write at.** Trivial lane, off every
high-risk surface the project names: low. Standard lane: medium. Deliberate lane:
the role's floor. Security Review, proposal authoring and review,
premise-checking, novel design and any work on a high-risk surface stay high; a
defect repair that takes the trivial lane by the carve-out
(`doctrine/lifecycle.md:52-56`) on a named surface keeps that surface's floor.
Plan review and code review stay medium. An adopter may raise a floor (for
instance from its complexity placement); it never lowers one below the lane's.

**R2. Every profile gets a short rule in `AGENTS.md`**, under Roles, in
`AGENTS.md` and `templates/core/AGENTS.md`. It stands alone, so a profile with no
module is covered:

> * **Model tier.** Use the lowest-capability model that can do the task
>   safely. The lane sets the lowest tier to write at: low for a trivial-lane
>   change off every high-risk surface, medium for the standard lane, and for the
>   deliberate lane the role's floor (`doctrine/roles.md`, "Capability floors").
>   Proposal authoring and review, Security Review, premise-checking, novel
>   design and any work on a high-risk surface stay high; plan and code review
>   are medium. **Name the model at every spawn**: a sub-agent that inherits
>   yours because no one set it is a defect. If a lowered agent's output fails
>   its check, or a review blocks on a defect it should have caught, re-run once
>   one tier up, never again at the same tier. Author and reviewer names carry
>   the model, and a reviewer who sees work written below its floor, with no
>   Maintainer Decision on the artifact lowering it, says so as a finding.

**R3. Setting the model is a tool habit, so it goes in the vendor wrapper.**
Cairn's `CLAUDE.md` addendum gets one bullet: pass the model on every new agent
call; resuming keeps the old model, so start a fresh lower-tier agent for new
work. `templates/core/VENDOR.md` is unchanged. **R4.** The escalation sentence in
R2 also goes in `doctrine/roles.md`, generalizing fan-out condition (d).

**R5. Measure from names already written.** Authors name their model in the
existing `**Author**` field, as reviewers do in the review heading. One row goes
in the deferred-follow-ups table of `dev/PLANNING.md`, beside "Watch the new
review header" (`:266`): after ten review passes on work written below the high
tier, the goodnight scrub owner counts the passes that returned REVISE with a
blocking finding, reads each to judge whether a higher tier would likely have
avoided it, and puts the counts to the Maintainer. I have no base rate, so the
same ten passes also count work written at the floor in the same window. This
proposal, written below its floor, is the first case.

The cross-maker condition is left as it is (Question 1).

**Edits and cuts.** Both `AGENTS.md` copies: R2, about 11 lines each.
`doctrine/roles.md`: Implementation bullets name lanes (`:173-180`); `:191-197`
becomes "the lane is the measure of risk; an adopter may raise a floor"; the R4
sentence; `:210-213` sends model names to the mapping file, not a case study.
The module (shipped file and byte-identical `dev/modules/` copy): Implementation
rows name lanes (`:53`, `:56`); "Notes on the gating" (`:193-215`) shrinks from 23
lines to about 6, since it says solo teams get nothing, which R2 makes false;
"Worked example" (`:76-83`) goes, since it points to a case study while
`:182-191` points to the mapping file. Also: the mapping's low row names the
trivial lane; `CLAUDE.md` (R3); `dev/PLANNING.md` (R5); one `CHANGELOG.md` line;
and two entries in the existing table of sentences both `AGENTS.md` copies must
carry (`bootstrap/tests/test_review_stance_in_shipped_files.py`).

Net: the always-on `AGENTS.md` grows 11 lines (about 150 tokens of about 8,300,
by `python scripts/token_budget.py`); the module shrinks about 26 lines per copy.

## Rationale

The floors already say "lowest tier by role". Missing is a way to apply them in
every profile: a shared risk measure (the lane), a rule in the file every agent
loads, and a visible choice at spawn, where cost multiplies (module `:87-92`).

## Alternatives considered

* **Do nothing.** A fan-out keeps inheriting the top tier by default;
  `solo-greenfield` gets no guidance; the instruction stays in private memory;
  nothing shows whether lower-tier work holds up.
* **Rejected as new machinery:** a hook that refuses a spawn with no model set
  (harness-specific, so not for vendor-neutral `AGENTS.md`); a `**Model tier**`
  header field with a parser; a check in `check_cairn.py` or `tools/board.py`
  comparing a review's model to the floors (headings are free text and the mapping
  is per adopter, so it needs a model-name resolver); a per-session log of model
  use; extending `check_model_selection.py` to read floors or `date_verified`; a
  "tier-cleared" status.
* **Install the module in `solo-greenfield`.** Rejected: the stub fails its own
  check until filled (`bootstrap/tests/test_model_selection_stub.py:141`), and a
  one-model adopter has nothing to map.
* **Relax the cross-maker condition now.** Not the default; Question 1.

## What is lost

Eleven lines more in the file every agent reads each turn. A one-vendor adopter
still cannot write below a floor without a Maintainer Decision (today's
behavior, now stated). A person, not a tool, reads the model names. The module's
solo-team note and case-study example, both stale.

## Migration for existing installs

`templates/core/AGENTS.md` changes, so installs receive R2 through the upgrade
merge (a token- and slot-aware 3-way merge, `bootstrap/_scaffold/upgrade.py:1-5`);
an adopter who edited Roles sees a merge result, not an overwrite; module edits
arrive the same way. The lockfile hash advances with `upgrade --finalize`
(`bootstrap/fidelity-check.md:28`).

## Documentation / doctrine surface

Prescription goes to the governing layer (both `AGENTS.md` copies,
`doctrine/roles.md`), per `docs/DOCUMENTATION_PLAN.md`; the rubric stays in the
module; the standing preference moves to the vendor-wrapper slot; the measure goes
on the board. R2 names tiers, never models or vendors.

## Evidence / verification plan

Every touched surface is prose or a text pin. Bold marks a person as the only trigger.

| Surface | Check | What triggers it |
|---|---|---|
| All edited Markdown | `python scripts/check_cairn.py`; `python scripts/claim_check.py <file>` | a person or agent, before commit (no CI) |
| `AGENTS.md` copies, module copies, `doctrine/roles.md` | `python scripts/quality_gate.py --sub neutrality --sub redundancy` | a person; the certifying run before a push includes it |
| R2 in both `AGENTS.md` copies | two new entries in `test_review_stance_in_shipped_files.py` | `pytest`; shows the sentence is present, not that anyone follows it |
| Module install, mapping shape | `test_model_selection_stub.py`; `python scripts/check_model_selection.py` | `pytest`, scoped; a person for the script |
| Model named at spawn (R2) | a reader compares the author name and review heading to the floor | **only a person or reviewing agent**; no command sees a spawn |
| Lowered work holds up (R5) | the PLANNING row's counts after ten passes | **only the goodnight scrub owner**, by reading |

I found the tests that read these files by searching their names in
`bootstrap/tests/`, `scripts/` and `tools/`. That test file is frozen
(`bootstrap/tests/fixtures/gate_manifest.json:6666`), so the edit owes the
gate-manifest re-anchor, which the 0.5 cut already folds in (`dev/PLANNING.md:81-85`).
A frozen gate file is a contract surface, so the plan's Boundary B mode is `full`,
recorded `Certified by: pending` until the next certifying run. Nobody sets
`CAIRN_FULL_SUITE=1` for this change.

### Tests required

Scoped: `test_review_stance_in_shipped_files.py`, `test_model_selection_stub.py`,
`test_writing_rules_ship.py`, `test_certifying_run_rule.py`. Mutant: delete the R2
sentence from one `AGENTS.md` copy; the new entry must fail, beside a passing
control. Smoke: `python bootstrap/scaffold.py --dry-run --config bootstrap/profiles/solo-greenfield.yml`.

#### Security preflight

N/A: no trust boundary added, moved, or widened. The data-governance gate
(`doctrine/roles.md:236-243`) and the bright-line list are unchanged. A "yes" to
Question 1 would widen who may check below-floor work, and this line would be redone.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

* Later sessions spawn agents with no model named, and review headings show the
  top tier anyway: R2 did not change behavior.
* After ten passes, REVISE with a blocking finding is clearly more common on
  lowered-tier work than on floor-tier work. I have no figure for "clearly"; the
  Maintainer reads the counts.
* A lowered agent edits a high-risk surface and a reviewer catches it.
* `AGENTS.md` must grow again to explain R2.

## Questions for the Maintainer

1. **Keep the "different maker" check?** Today a cheaper agent may write below its
   floor only if a stronger model from a different company checks it, so a
   one-vendor team never can. Should a stronger model from the same company
   count, if the other three conditions hold? **Default: no, keep it.** The lane
   table already puts most writing at the lowest tier, so this decides only
   writing below a floor, the riskier case. The clause dates from 2026-06-04
   (`d8ef569c`) and its wording from 2026-10-19 (`08c946a6`, `e4b4dbb5`); I found
   no record that you weighed it on its own. You can already lower one floor for
   one scope (module `:70-74`), and there is no measure yet. "Yes" costs one
   clause in five places and three patterns in the frozen test.
2. **Lower the default floor for proposal authoring from high to medium?**
   **Default: no; keep high** until the R5 row has its ten passes, with this
   proposal's review as the first data point.

## Scope delta

**Scope delta**: preserved (opening revision; nothing removed).

## Assurance path

**Assurance path**: high-assurance (governing doctrine, the shipped `AGENTS.md`
and a frozen gate test are in the template's trigger list).
