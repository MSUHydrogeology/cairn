# Use the lowest model tier that is safe, and say which one ran

**Author**: Claude (Strategy)
**Status**: awaiting-decision
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

## Review -- Claude Sonnet 5.5 (Internal) -- 2026-10-26

```
Reviewed commit: 178315324d51489811ee09369732ae6c5bd1d339
Target: the whole proposal, against doctrine/roles.md "Capability floors", doctrine/lifecycle.md "Three lanes", doctrine/rationale.md "How the doctrine evolves under evidence", both copies of the model-selection module, both AGENTS.md copies, and the "### 0.5" section of dev/PLANNING.md
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual (pass 1 of 1; no Security Review is declared and none is raised here)
**Findings**: raised (2 blocking, 9 non-blocking)
**Verdict**: REVISE

**Conclusion first.** The proposal should exist, and its aim is right. Two things must change before the Maintainer decides. The rule text in R1 and R2 contradicts a pinned exception (F1). It also raises the writing floor on every named high-risk surface without saying so (F2). The rest is wording, wrong figures, and one cheap widening. I am a medium-tier reviewer on a stage whose floor is high; see F5.

**Foundations**

1. **Should this happen as framed?** Yes for the aim; not as worded. A solo-greenfield adopter gets no tier text at all (`AGENTS.md` has none; `bootstrap/_scaffold/config.py:1354-1361` installs no module for it). But R1 and R2 as drafted contradict the cleanup row that lets wording-only edits be written at low even on a high-risk surface (`doctrine/roles.md:182-189`; module `:61-68`, `:151-153`; pinned at `bootstrap/tests/test_review_stance_in_shipped_files.py:931, 937, 939, 1159`), and they raise the floor for non-trivial work on named surfaces from the module's medium row (`:53`) to high (F1, F2).
2. **Best alternative.** Doing nothing leaves the private preference and the solo gap the Maintainer named, so it loses. The strongest alternative is this proposal with three changes, none of them a narrowing: fix the R1/R2 words (F1), state the floor decision (F2), and add the helper-agent default the module already holds (`templates/modules/team-gated/model-selection.md:100-104`), paid for by trimming R2's floor list (F8). The Worked-example cut can wait for its own row (F7).
3. **What would show it wrong.** The author's four signals are the right ones but only the quality side has a reader. I add two. First, spend that does not fall: nobody reads work written above the lane's floor, and R5 counts only below-floor work (F4). Second, a ten-pass count that cannot separate tiers: by a loose text match, 15 of 27 review passes dated 2026-10-17 to 2026-10-26 carry a `(blocking)` marker, at Opus and Sonnet reviewers alike (F9).

### Rulings on the six points

**1. The rate-limit gate.** Neither a clause in the gate nor "accept the direction as evidence". The gate reads "No doctrine change from a single incident" unless the Maintainer classes it high-risk (security or data loss only), else recurrence or goodnight synthesis (`doctrine/rationale.md:442-452`; `AGENTS.md`, "Doctrine changes clear the rate-limit gate"). This change starts from the Maintainer's direction, not from an incident, so I read the gate as not engaged. The Decision should say that in one line. Do not edit the gate: that is itself a doctrine change that would have to clear it, and a standing "Maintainer direction counts" clause is a fourth path every later agent could cite. The tree holds two precedents: `dev/proposals/archive/2026-10-18-claude-review-lenses-for-every-install.md:130` ("your Decision is the authorization", accepted at `:660-680`), and `dev/proposals/archive/2026-10-17-claude-maintainer-attention.md:306-308, 915-919`, where an agent-started Part B was cut for answering no incident. The difference is who started it. One recorded incident exists that the proposal does not cite: `dev/NEXT_SESSION.md:3` (work paused 2026-10-19 while credits reset). It cannot clear the gate alone, but it shows the direction has a cause. I am moderately sure of this reading; the Maintainer's reading settles it (F3).

**2. R2 has no machine trigger.** The table is honest on the main point: "presence, not compliance" and "only a person" are both stated. I opened the triggers it names. `.git/hooks/pre-commit` runs only `tools/intent.py _precommit_check`, the claim ledger. `.github/` holds issue and pull-request templates and `labels.yml`, no workflow. So nothing runs the text pin on commit. It runs when someone runs pytest, in a scoped run or in the certifying run (`AGENTS.md`, "Verification boundaries"). The "pytest" cell does not say that. One row overstates: "Model named at spawn" says a reader compares the author name and heading to the floor. That reads the model that ran, from a heading the agent writes about itself. It does not show whether the spawn call named a model; an agent that silently inherited the top tier names the top tier. It also catches only below-floor work. A spawn call is visible only in a session transcript, which is not in the repository. The rule is still worth shipping: it is addressed to the spawning agent, the only party able to comply; the pin keeps it through upgrade merges; and failure costs money, not correctness (F4).

**3. R1's carve-out.** Right as a default; wrong words (F1). I would not loosen it. The bright-line text keeps work on high-risk trust boundaries at high (`doctrine/roles.md:236-243`). `AGENTS.md`, "Fixing an easy problem you meet", says a high-risk surface makes a fix "not cheap". Cairn's own list is headed "Security-Review + proposal triggers", and its cost-bar example says a one-line engine change still takes a proposal and a Security Review, so in Cairn the lifecycle carve-out (`doctrine/lifecycle.md:52-56`) never reaches the engine anyway. It is strict for a one-line repair with a failing test, but that strictness is the existing bright line, and a Decision can lower it for one scope.

**4. The cuts.** Mixed; details in F7. "Notes on the gating" is stale in part and the cut is fair, but its stated reason overstates. "Worked example" is stale but not forced by R1 to R5. The frozen-file claim is right: I loaded `bootstrap/tests/fixtures/gate_manifest.json`; line 6666 is the key for `bootstrap/tests/test_review_stance_in_shipped_files.py`, and it sits under `frozen_files`. The cross-maker pins are at test lines 943 (cost-rule text), 953 (condition (a)) and 1148 (the `roles.md` copy), so a "yes" to Q1 touches three patterns, as the proposal says.

**5. Too timid?** Not on floors; too narrow on spawns. The evidence is thin, so I would not go further on floors. I re-derived the figures (F6): no proposal `**Author**` line in the tree names a model (0 of 88; 0 of 16 in the window), and 26 of 27 recent review headings do. There is no outcome data for lower-tier proposal authoring beyond this one proposal. R1 mostly restates the existing floors by lane, which is what "formalize" asks. Q1's default is right: the cross-maker check matters only for writing below a floor, which already has a route (a Maintainer Decision, module `:70-74`). Q2's default is right but circular as drafted (F9c). What is missing is the biggest saving. R2 speaks of the tier "to write at" and says nothing about helper agents that only search or extract. The module already makes those low, and the proposal's own Rationale says cost multiplies at the spawn (F8).

**6. The always-on cost.** The figure is understated (F6): the R2 block as drafted is 14 lines and 933 characters, about 233 tokens by the chars/4 proxy that `scripts/token_budget.py` uses, not 11 lines and 150. The same script reports `AGENTS.md` at 8,840 tokens at this commit (35,496 bytes), not about 8,300. That is +2.6%, not +1.8%. It still earns its place, in part. `AGENTS.md` is the only copy of the floors an adopter loads, because `doctrine/` is a citation, not an installed file. The three sentences that change behavior (name the model at every spawn, escalate once, flag below-floor work) are worth 230 tokens. The floor list inside R2 earns less and can be compressed (F8).

### Findings

**F1 (blocking). R1 and R2 contradict the pinned cleanup row, and "work" is unclear.** `doctrine/roles.md:182-189` and the module (`:61-68`, `:151-153`) let docstring-and-comment cleanup be written at low even on a high-risk surface; the review and the Security Review keep their floors. Tests pin this (`test_review_stance_in_shipped_files.py:931, 937, 939, 1159`). R2 says "any work on a high-risk surface stay[s] high", and R1 says a floor never goes "below the lane's". A reader of `AGENTS.md` alone gets the opposite rule. R2 also says that work stays high and that code review is medium; code review of a change on such a surface is both. And R1's "keeps that surface's floor" has no definition, because floors are by role. Fix: say "the writing step"; add "except wording-only cleanup (`doctrine/roles.md`)"; say "code review stays medium and the Security Review is its own pass at high"; replace "keeps that surface's floor" with "stays high". Closes when the revised R2 text agrees with the pinned sentences.

**F2 (blocking). R1 settles an ambiguity toward a higher floor and does not say so.** The module's table says Implementation (non-trivial) is medium with no surface exception (`:53`). Its bright-line paragraph says "the high-risk trust boundaries" never downshift (`:149-151`; `doctrine/roles.md:236-240`). R1 reads that as all work on any surface `AGENTS.md` names, which in Cairn includes the licence split and the neutrality gate, not only trust boundaries. The consequence is concrete: the engine-batch and repin builds sit on the scaffold engine, so they would be written at high, against the Maintainer's 0.5 direction quoted in the header, unless a Decision lowers them. "What is lost" and "Signals" do not say so. Fix: state that this is a decision, not a restatement, and put it to the Maintainer with a default (mine: engine and Security-Review surfaces stay high unless a Decision lowers a named build), or narrow the word to surfaces the project names for Security Review. The Maintainer chooses.

**F3 (non-blocking). The gate paragraph asks for the wrong thing.** See ruling 1. Rewrite Context to say this is not an incident-driven change, the gate is not engaged, and the Decision records that; cite `dev/NEXT_SESSION.md:3` as context. Add a numbered Question 3 ("Is your 2026-10-26 direction the origin of this change, so the gate is not engaged?", default yes), so the scribe's note records an answer.

**F4 (non-blocking). The verification table overstates one row and misses the cost side.** (a) Name who runs pytest: the implementer's scoped run and the certifying run before a push; the pre-commit hook does not. (b) The spawn row should say it reads the model that ran, not the spawn call, and that the call is visible only in a transcript. (c) Soften "is a defect" in R2, or say plainly that nothing observes it. (d) Make the R5 row also count work written above the lane's floor in the same ten passes. It uses the same names and adds no machinery, and the Signals already list "top tier anyway" with no reader assigned.

**F5 (non-blocking). R2's below-floor finding fires on lawful work, and the Authoring-tier paragraph misses the reviewer.** R2 has a reviewer flag work written below the floor "with no Maintainer Decision on the artifact". This proposal and this review are below the high floor on the Maintainer's chat words, which are not a Decision (module `:70-74` asks a Decision that names role, floor, rationale and scope). The same words will cover each 0.5 artifact built at his direction, and R2 would flag all of them. `AGENTS.md` already accepts a dated chat quote for an External read (`-- chat, <date>`). Fix: R2 reads "a Maintainer Decision or a dated direction quoted verbatim on the artifact". The header paragraph says the floor is lowered "for authoring only"; it should also say that the review is below the proposal-review floor under the same words.

**F6 (non-blocking). Figures to restate, with the counting rule.** (a) Cost: 14 lines, 933 characters, about 233 tokens, against 8,840 for `AGENTS.md` (`python scripts/token_budget.py`, chars/4 proxy; I extracted the R2 block from proposal lines 85-98 and counted characters). R3's `CLAUDE.md` bullet is also always-on (527 tokens now). (b) "11 of 12 proposals read Claude (Strategy)": I counted on the tree at `e92ad324` (HEAD when I counted). I count 15 of 16 proposals dated 2026-10-17 to 2026-10-26 (filename date, `dev/proposals/` and `dev/proposals/archive/`, first `**Author**` line); the 16th reads "Claude (Implementation)"; none names a model. (c) "20 of 21 headings": I count 27 headings that start `## Review` or `## Security Review`, dated 2026-10-17 to 2026-10-26; 26 name Opus, Sonnet or Haiku; the one that does not is `Review -- Claude (External) -- 2026-10-17`. As a control, the same pattern matched headings I knew carried "Opus". I could not reproduce the author's 12 and 21, so the counting rule belongs in the Response. The conclusion holds either way. (d) "One clause in five places": I count six occurrences in three files (`doctrine/roles.md:221, 230`; each module copy `:129-130, :143`).

**F7 (non-blocking). The two module cuts.** (a) "Notes on the gating": cut it, but fix the reason. R2 does not change which profiles install the module. What it falsifies is "the capability question is settled trivially" for a one-maker team, since tiers exist within one maker, and `docs/solo-legacy-recipe.md:72` already tells a solo adopter to add the module at complex placement. Keep the install-gate sentence; the header (`:4-9`) already carries it. (b) "Worked example": stale (the stub carries the example row, and `:182-191` points to the mapping file) but not needed by R1 to R5. Cutting it leaves four mentions dangling: module `:25-26` ("a worked-example shape"), `:176-177` ("the case study"), `doctrine/roles.md:207` ("a worked example") and `:210-213` (the proposal does plan this one). I grepped `bootstrap/tests`, `scripts`, `tools`, `templates`, `doctrine` and `docs` for the cut passages' wording and found no test that pins them. (c) "Scope delta: preserved (opening revision; nothing removed)" is false for shipped text. Fix: either cut it and clean the four mentions and reword the Scope delta ("no accepted outcome removed; two stale module passages cut, listed in What is lost"), or move the Worked-example cut to its own row. The author decides.

**F8 (non-blocking, a widening). R2 has no default for helper agents that only search or extract, and it omits the data-governance guard.** The module makes single search, extraction and mechanical transforms low (`:100-104`), and the Rationale says cost multiplies at the spawn (`:136-138`). A solo-greenfield adopter has no module, so it gets nothing. Fix: one clause in R2 ("read-only search and extraction helpers: low"). Pay for it by compressing the floor list in R2. Also add five words, "never across a data-governance boundary", because the rule now pushes every agent toward cheaper models and the guard (`doctrine/roles.md:236-243`) is reachable only through R2's pointer. What is lost: about one line of always-on text. Why it reaches the cause: this is the cost the Maintainer asked to cut.

**F9 (non-blocking). R5 cannot separate tiers as drafted.** (a) Base rate: 15 of 27 recent passes carry a `(blocking)` marker (loose text match; I did not read each pass), at both Opus and Sonnet reviewers. With ten passes, a small effect cannot show. (b) Confound: reviewer tier is dropping at the same time as author tier, so fewer blocking findings can mean a weaker reviewer. Record the reviewer's tier beside each pass. (c) Plan and code reviews are all of work already written at medium, so "ten passes" fills at once and says nothing about proposals. Count proposals written below high separately; that is the evidence Q2 needs. (d) "Would likely have avoided it" is a bare estimate; have the scrub owner write the reason for each. These are about three more lines in the PLANNING row.

**F10 (non-blocking, for the plan). Cairn's own lockfile and the row position.** Cairn's lockfile covers `AGENTS.md`, `CLAUDE.md`, `dev/.cairn/model-selection-mapping.yml` and `dev/modules/model-selection.md` (`dev/.cairn/cairn-lock.yml:30, 37, 44, 168`). The plan needs a scoped `upgrade --finalize` for those four, as commit `08c946a6` did; the Migration section covers adopters only. Cite the PLANNING row by name, not by line (`dev/PLANNING.md:266` moves).

**F11 (non-blocking). Q1's history is incomplete.** "I found no record that you weighed it on its own": the 2026-10-18 Decision on `external-is-a-maintainer-stance` kept the clause by non-override ("the cost-rule downshift stays, scoped", `dev/proposals/archive/2026-10-18-claude-external-is-a-maintainer-stance.md:1480-1511`; the carve-out row is at `:1036`). So the Maintainer accepted the clause but was never asked about a one-vendor team. Say that in Q1. It changes what "keep" means. I agree with the default.

**Coverage.** I did not run any test, the full suite, or the redundancy gate on R2's text (it does not exist yet). I ran `claim_check.py` on the proposal (no flags), `quality_gate.py --sub neutrality --sub redundancy` on the current tree (fail=0, fail=0), and a word search of the R2 block for the denylisted names (none; the control matched). I resolved the cited paths and lines in `doctrine/`, the module, `config.py`, `upgrade.py`, `plans.md:724, 929` and `PLANNING.md:266, 81-85` at the reviewed commit; `doctrine/lifecycle.md` and `rationale.md` changed by a few lines since, and the cited ranges still hold. I did not verify R3's claim that a resumed agent keeps its old model (harness behavior, not in the tree), did not count plan or code reviews, did not check `docs/DOCUMENTATION_PLAN.md` routing, and did not read the other review passes beyond their headings and `(blocking)` markers. I applied the lenses on foundations, evidence and scope removal; I did not apply the others in the sweep.

## Response -- Claude (author) -- 2026-10-26

**Conclusion first.** I accept all eleven findings and all six rulings. Two I accept with a variation (F2, F9); none is declined. The Revision below is the complete current contract. I wrote this Response and Revision at the medium tier (Sonnet 5.5), under the Maintainer's words quoted in the Revision. I ran no test; every check below is a prose check.

| Finding | Disposition | What I did |
|---|---|---|
| F1 (blocking) | Accepted | "Write" and "floor" now have one meaning each. The wording-cleanup row stays, and R2 says so. |
| F2 (blocking) | Accepted with variation | Reviewer's default was to keep engine surfaces at high. I took the other fix the review allowed: R1 raises nothing, the module's medium row stands, and the question goes to the Maintainer as Question 4 with the default that matches his aim. |
| F3 | Accepted | Gate paragraph rewritten; Question 3 added; no gate edit asked. |
| F4 | Accepted | Table rewritten: who runs pytest, what the spawn row can and cannot see, softer R2 wording, R5 also counts above-floor work. |
| F5 | Accepted | R2 accepts a dated, quoted Maintainer direction. The Authoring-tier paragraph now covers the review and this Response. |
| F6 | Accepted | Recounted (below). Two of my numbers differ in unit or scope from the reviewer's, and I say how. |
| F7 | Accepted | I did the cleanup, not the deferral: all four dangling mentions are reworded. The reason for shrinking "Notes on the gating" is corrected. Scope delta reworded. |
| F8 | Accepted | Added "read-only search and extraction helpers: low" and the data-governance guard. R2 is one line shorter than the draft. |
| F9 | Accepted with variation | I fixed what can be fixed (blocking read from the review's Findings line, reviewer model recorded, proposals counted apart from plan and code passes, a written reason per case). I say plainly that it stays a count and what a count cannot show. |
| F10 | Accepted | Plan note added; the PLANNING row is cited by name. |
| F11 | Accepted | Question 1 now carries the 2026-10-18 history. Default unchanged. |

**The six rulings.** (1) Gate: accepted, same as F3. (2) No machine trigger: accepted, same as F4. (3) R1 carve-out: accepted; the bright line is not loosened, and R1 no longer says "keeps that surface's floor". (4) The cuts: accepted, same as F7. (5) Too timid: accepted; the helper clause is added, floors are not widened, and Question 2's circle is broken. (6) Always-on cost: accepted; remeasured below.

**Recount, on this tree.** I counted `dev/proposals/` and `dev/proposals/archive/`, files whose name starts with a date, excluding `_template.md`; the date is the file name's date, the author is the first `**Author**` line, and a review heading is a line starting `## Review` or `## Security Review` with a date in the window.

* Proposals dated 2026-10-17 to 2026-10-26: 16. First `**Author**` line reads `Claude (Strategy)`: 15. The 16th reads `Claude (Implementation)`. None names a model. Across all 87 dated proposal files, 0 name a model. The reviewer counted 88; I cannot reproduce that figure.
* Review headings in the window: 27 before the review of this proposal, 26 of them naming Opus, Sonnet or Haiku (the one that does not is `Review -- Claude (External) -- 2026-10-17`). Counting this proposal's own review: 28 and 27. I match the reviewer's 26 of 27.
* The cross-maker clause: six places in three files (`doctrine/roles.md:221` and `:230`; the shipped module `:129` and `:143`; the installed copy at the same lines).
* Always-on size. `python scripts/token_budget.py` uses the `tiktoken` counter when it is importable and a characters-divided-by-four proxy otherwise. Here it is importable: `AGENTS.md` is 8,268 tokens, `CLAUDE.md` 511. Under the proxy `AGENTS.md` is about 8,850; the reviewer's 8,840 is that figure. Both are right in their own unit. The draft's R2 block was 14 lines, 232 tokens (`tiktoken`) or 239 (proxy). The new R2 block is 13 lines, 207 tokens or 223. The new R2 is smaller than the draft while adding two clauses.

## Revision -- Claude (author) -- 2026-10-26

**This is the complete current contract.** It replaces the opening contract; the opening text stays above as history.

**Authoring tier.** Doctrine sets proposal authoring and proposal review at the high tier (`doctrine/roles.md:167-172`). This proposal's authoring, its review, and this Response and Revision were all written at the medium tier. The Maintainer's words today, which are a chat direction and not a Decision, lowered the floor for these three passes only:

> "I would also like to formalize a rule set for using lower-tier models where possible."

> "Go ahead and spawn the lowest-tier agents you can to design, review, and implement proposals toward 0.5"

### Context

**The gate is not engaged.** Doctrine changes clear the rate-limit gate (`doctrine/rationale.md:442-452`), which answers single incidents. This change did not start from an incident. It started from the Maintainer's direction above, so the gate does not apply. The Decision records that in one line (Question 3). I ask for no edit to the gate. For context, work paused on 2026-10-19 while credits reset (`dev/NEXT_SESSION.md:3`).

**What exists.** A floor by role (`doctrine/roles.md:149-197`): high for Strategy, proposal review, Security Review and scribing; medium for non-trivial implementation, plan review and code review; low for trivial chunks. The `model-selection` module holds the role table (`templates/modules/team-gated/model-selection.md:45-59`), a fan-out table (`:94-109`) and a mapping schema (`:170-191`). Cairn's mapping is `dev/.cairn/model-selection-mapping.yml:19-36`. The only check (`scripts/check_model_selection.py:5-10`) fails on a `FILL ME` stub.

**Two words, used one way throughout.** *Write* is the step that produces the artifact: authoring a proposal, implementing a change. *Floor* is the role's row in the module table, and nothing else.

**Seven gaps, each checked.**

1. **Reach.** Only `collaborative-team` and `high-rigor-legacy` install the module (`bootstrap/_scaffold/config.py:1363-1391`); `solo-greenfield` installs none (`:1354-1361`). `AGENTS.md` has no tier text.
2. **No trigger.** Tools let a sub-agent inherit the caller's tier silently (module `:91-92`). Nothing makes anyone name the model, and no tool sees which one a harness picked. Cairn has no CI (`AGENTS.md:408`).
3. **"Risk" is undefined.** Floors rest on each adopter's complexity placement (`doctrine/roles.md:191-197`); "trivial chunks" (module `:56`) has no definition. The lanes (`doctrine/lifecycle.md:40-78`) are a closed procedure every adopter already runs.
4. **No escalation for roster roles.** Fan-out has one (`doctrine/roles.md:224-225`; module `:134-135`); an author or reviewer has none.
5. **Nothing measures whether lower-tier work holds up.** The mapping binds tiers "by name, not by measurement" (`dev/.cairn/model-selection-mapping.yml:11-12`). Measured on this tree (counting rule in the Response): 0 of 87 proposal `**Author**` lines name a model, and 15 of 16 in 2026-10-17 to 2026-10-26 read `Claude (Strategy)`; 26 of 27 review headings in that window name one. I did not count plan or code reviews.
6. **The standing preference is private.** "Pass a cheaper model on new agent calls" lives in an agent's memory directory, not the repository (`CLAUDE.md:17-34`).
7. **The cost rule's check needs a different maker.** A cheaper author may write below its floor only if a stronger tier of a different model architecture checks it. The clause is in six places in three files (`doctrine/roles.md:221` and `:230`; the shipped and installed module at `:129` and `:143`) and pinned at `bootstrap/tests/test_review_stance_in_shipped_files.py:943-955` and `:1148-1157`. A one-vendor team cannot meet it. It is a permission, so it breaks no rule that a tier may not require a different agent type, but it closes below-floor writing for most adopters (Question 1).

### Proposal

Five rules. No new header field, parser, file, tool, gate, status or config key. **R1 raises no floor and lowers none.**

**R1. The lane sets the tier to write at, within the role's floor.** Trivial lane: low (the module's trivial-chunk row). Standard lane: medium. Deliberate lane: the role's floor. Wording-only edits (docstrings, comments) may be written at low on any surface (`doctrine/roles.md:182-189`); the review and any Security Review keep their floors. Security Review, proposal authoring and review, premise-checking and novel design stay high. Plan review and code review stay medium. An adopter may raise a floor and may not lower one below the module's row.

R1 does not raise writing on a named high-risk surface above the module's row for non-trivial implementation (medium, `:53`). The bright-line text keeps "the high-risk trust boundaries" at high (`doctrine/roles.md:236-243`) without saying whether that covers writing code on them. The text does not settle it and R1 does not either: until Question 4 is answered, the module's implementation rows apply as written, with the Security Review at high.

**R2. Every profile gets a short rule in `AGENTS.md`**, under Roles, in `AGENTS.md` and `templates/core/AGENTS.md`. It stands alone, so a profile with no module is covered:

> * **Model tier.** Use the lowest-capability model that can do the task
>   safely. The lane sets the tier to write at: low for the trivial lane,
>   medium for the standard lane, the role's floor for the deliberate lane
>   (`doctrine/roles.md`, "Capability floors"; Security Review, proposal
>   authoring and review and other bright-line work stay high). Read-only
>   search and extraction helpers, and wording-only edits: low. Never
>   downshift across a data-governance boundary. **Name the model at every
>   spawn**; an unset spawn inherits yours and usually costs more than the
>   task needs. If lowered output fails its check, or a review blocks on a
>   defect it should have caught, re-run once one tier up. Author and
>   reviewer names carry the model. A reviewer who sees work written below
>   its floor, with no Maintainer Decision or dated Maintainer direction
>   quoted on the artifact, says so.

**R3. Setting the model is a tool habit, so it goes in the vendor wrapper.** Cairn's `CLAUDE.md` addendum gets one bullet: pass the model on every new agent call; a resumed agent keeps its old model, so start a fresh lower-tier agent for new work (a harness behavior I did not check in the tree). `templates/core/VENDOR.md` is unchanged. **R4.** The escalation sentence in R2 also goes in `doctrine/roles.md`, generalizing fan-out condition (d).

**R5. Measure from names already written.** Authors name their model in the existing `**Author**` field, as reviewers do in the review heading. One row goes in the deferred-follow-ups table of `dev/PLANNING.md`, beside "Watch the new review header". After ten proposal reviews of proposals written below the high tier, the goodnight scrub owner records, for each: the author's model, the reviewer's model, whether the review's own `Findings` line reports blocking findings, and one sentence giving the reason a higher-tier author would or would not have avoided each blocking finding. The same window also counts proposals written at or above the lane's floor, and any work written above the lane's floor, so spend that does not fall shows up. Plan and code passes are counted on a separate line and do not count toward the ten. The owner puts the counts to the Maintainer. This proposal is the first case.

**What this measure cannot show.** It is a count. With ten cases and no base rate, it cannot show a small difference or its cause. Reviewer tier is falling at the same time as author tier, so fewer blocking findings may mean a weaker reviewer, and more may mean a weaker author. A loose text match marks 15 of 27 recent reviews "(blocking)" at both reviewer tiers, so the base rate may already be high. It can show a large gap. I have no figure for "large"; the Maintainer reads the counts.

The cross-maker condition is left as it is (Question 1).

**Edits and cuts.**

* Both `AGENTS.md` copies: R2, 13 lines each.
* `doctrine/roles.md`: the Implementation bullets name lanes (`:173-180`); `:191-197` becomes "the lane is the measure of risk; an adopter may raise a floor"; the R4 sentence; `:207` drops "a worked example"; `:210-213` sends model names to the mapping file, not a case study.
* The module (shipped file and byte-identical `dev/modules/` copy): Implementation rows name lanes (`:53`, `:56`). "Notes on the gating" (`:193-215`) shrinks from 23 lines to about 6 and keeps the install-gate sentence. It says a solo single-agent team settles the capability question trivially, and R2 makes that false, since tiers exist within one maker. "Worked example" (`:76-83`) goes, and the two mentions of it are reworded to point to the mapping file (`:25-26`, `:176-177`).
* The mapping's low row names the trivial lane; `CLAUDE.md` (R3); `dev/PLANNING.md` (R5); one `CHANGELOG.md` line; two entries in the existing table of sentences both `AGENTS.md` copies must carry (`bootstrap/tests/test_review_stance_in_shipped_files.py`).

**Always-on cost, measured** (`python scripts/token_budget.py`, `tiktoken`): `AGENTS.md` grows by 207 tokens (13 lines) from 8,268, about 2.5%. R3's `CLAUDE.md` bullet adds about 35 tokens to 511 (my estimate, not counted). The draft's R2 block was 232 tokens. Under the characters-divided-by-four proxy the figures are 223 and about 8,850. The module shrinks about 26 lines per copy.

### Rationale

The floors already say "lowest tier by role". Missing is a way to apply them in every profile: a shared risk measure (the lane), a rule in the file every agent loads, and a visible choice at spawn, where cost multiplies (module `:87-92`).

### Alternatives considered

* **Do nothing.** A fan-out keeps inheriting the top tier by default; `solo-greenfield` gets no guidance; the instruction stays in private memory; nothing shows whether lower-tier work holds up.
* **Rejected as new machinery:** a hook that refuses a spawn with no model set (harness-specific, so not for vendor-neutral `AGENTS.md`); a `**Model tier**` header field with a parser; a check in `check_cairn.py` or `tools/board.py` comparing a review's model to the floors (headings are free text and the mapping is per adopter); a per-session log of model use; extending `check_model_selection.py`; a "tier-cleared" status.
* **Install the module in `solo-greenfield`.** Rejected: the stub fails its own check until filled (`bootstrap/tests/test_model_selection_stub.py:141`), and a one-model adopter has nothing to map.
* **Raise the writing floor on named high-risk surfaces to high.** Not the default; Question 4.
* **Relax the cross-maker condition now.** Not the default; Question 1.

### What is lost

Thirteen lines more in the file every agent reads each turn. A one-vendor adopter still cannot write below a floor without a Maintainer Decision (today's behavior, now stated). A person, not a tool, reads the model names. The module's solo-team note and its worked example, both stale.

### Migration for existing installs

`templates/core/AGENTS.md` changes, so installs receive R2 through the upgrade merge (a token- and slot-aware 3-way merge, `bootstrap/_scaffold/upgrade.py:1-5`); an adopter who edited Roles sees a merge result, not an overwrite; module edits arrive the same way. The lockfile hash advances with `upgrade --finalize` (`bootstrap/fidelity-check.md:28`). **For the plan:** Cairn's own lockfile covers four files this change edits (`AGENTS.md`, `CLAUDE.md`, `dev/.cairn/model-selection-mapping.yml`, `dev/modules/model-selection.md`; `dev/.cairn/cairn-lock.yml:30`, `:37`, `:44`, `:168`). The plan needs a scoped `upgrade --finalize` for those four, as commit `08c946a6` did.

### Documentation / doctrine surface

Prescription goes to the governing layer (both `AGENTS.md` copies, `doctrine/roles.md`), per `docs/DOCUMENTATION_PLAN.md`; the rubric stays in the module; the standing preference moves to the vendor-wrapper slot; the measure goes on the board. R2 names tiers, never models or vendors.

### Evidence / verification plan

Every touched surface is prose or a text pin. Bold marks a person as the only trigger.

| Surface | Check | Who runs it, and when |
|---|---|---|
| All edited Markdown | `python scripts/check_cairn.py`; `python scripts/claim_check.py <file>` | the author, before commit (no CI) |
| `AGENTS.md` copies, module copies, `doctrine/roles.md` | `python scripts/quality_gate.py --sub neutrality --sub redundancy` | the implementer; the certifying run before a push includes it |
| R2 in both `AGENTS.md` copies | two new entries in `test_review_stance_in_shipped_files.py` | `pytest`, run by the implementer (scoped) and by the certifying run before a push. The pre-commit hook runs only the claim-ledger check, so nothing runs it at commit. It shows the sentence is present, not that anyone follows it. |
| Module install, mapping shape | `test_model_selection_stub.py`; `python scripts/check_model_selection.py` | `pytest`, scoped; a person for the script |
| Model named at spawn (R2) | a reader compares the model named in the author line and review heading to the floor | **only a person or reviewing agent**. This reads the model that ran, from a heading the agent writes about itself. It cannot show whether the spawn call named a model: that call is visible only in a session transcript, outside the repository. It catches only work written below its floor. |
| Lowered work holds up (R5) | the PLANNING row's counts after ten proposal reviews, including work at and above the floor | **only the goodnight scrub owner**, by reading |

I found the tests that read these files by searching their names in `bootstrap/tests/`, `scripts/` and `tools/`. That test file is frozen (`bootstrap/tests/fixtures/gate_manifest.json:6666`), so the edit owes the gate-manifest re-anchor, which the 0.5 cut already folds in (`dev/PLANNING.md:81-85`). A frozen gate file is a contract surface, so the plan's Boundary B mode is `full`, recorded `Certified by: pending` until the next certifying run. Nobody sets `CAIRN_FULL_SUITE=1` for this change.

#### Tests required

Scoped: `test_review_stance_in_shipped_files.py`, `test_model_selection_stub.py`, `test_writing_rules_ship.py`, `test_certifying_run_rule.py`. Mutant: delete the R2 sentence from one `AGENTS.md` copy; the new entry must fail, beside a passing control. Smoke: `python bootstrap/scaffold.py --dry-run --config bootstrap/profiles/solo-greenfield.yml`.

#### Security preflight

N/A: no trust boundary added, moved, or widened. The data-governance gate (`doctrine/roles.md:236-243`) and the bright-line list are unchanged, and R2 now names the gate. A "yes" to Question 1 or Question 4 would change who may write or check work near a trust boundary, and this line would be redone.

#### Independent scientific check

N/A: no scientific assumption or result touched.

### Signals the change is wrong

* Later sessions spawn agents with no model named, and review headings show the top tier anyway: R2 did not change behavior.
* After ten proposal reviews, REVISE with a blocking finding is clearly more common on work written below high than on work written at the floor (the Maintainer reads the counts).
* Work is written above the lane's floor with no reason given, and nobody notices: the spend did not fall.
* A lowered agent edits a high-risk surface and a reviewer catches it.
* `AGENTS.md` must grow again to explain R2.

### Questions for the Maintainer

1. **Keep the "different maker" check?** Today a cheaper agent may write below its floor only if a stronger model from a different company checks it, so a one-vendor team never can. Should a stronger model from the same company count, if the other three conditions hold? **Default: no, keep it.** The lane table already puts most writing at the lowest tier, so this decides only writing below a floor, the riskier case. History: the clause dates from 2026-06-04 (`d8ef569c`) and its wording from 2026-10-19 (`08c946a6`, `e4b4dbb5`). Your 2026-10-18 Decision on `external-is-a-maintainer-stance` kept it by not overriding it ("the cost-rule downshift stays, scoped", `dev/proposals/archive/2026-10-18-claude-external-is-a-maintainer-stance.md:1480-1511`), so you accepted the clause, but I found no record that you were asked about a one-vendor team. You can already lower one floor for one scope by Decision (module `:70-74`), and there is no measure yet. "Yes" costs one clause in six places and three patterns in the frozen test.
2. **Lower the default floor for proposal authoring from high to medium?** **Default: no; keep high.** The earlier draft tied this to the R5 count, but that count would come from the same lowered proposals, a circle. The way out: below-high proposals keep being written only when you direct one with a dated quote, as this one was. Those cases are the data. Ask again once the R5 row has ten.
3. **Is your 2026-10-26 direction the origin of this change, so the rate-limit gate is not engaged?** **Default: yes.** The Decision records your answer. No gate edit is asked.
4. **Should writing on a named high-risk surface be at high?** Today the module gives non-trivial implementation the medium tier and keeps Security Review at high; the bright-line text does not say whether "high-risk trust boundaries" covers writing. **Default: no; keep the module's rows.** That matches your 0.5 direction: the engine-batch and `repin` builds are written at medium or lower, with the Security Review and code review as the checks. "Yes" would put those builds at high unless a Decision lowers each one.

### Scope delta

**Scope delta**: degraded. One removed unit:

* The opening R1 and R2 raised the writing floor on every named high-risk surface ("keeps that surface's floor"; "any work on a high-risk surface stay[s] high"). The review found the raise unannounced and in conflict with the cleanup row. It is withdrawn. **disposition**: defer. Specifying it was rejected because it would put the 0.5 engine-batch and `repin` builds at high against the Maintainer's direction; Question 4 asks whether to raise it.

Everything else opened is kept. Two stale module passages are cut ("Notes on the gating" shrinks and "Worked example" goes, both in What is lost), and two clauses are added (helpers, data-governance).

### Assurance path

**Assurance path**: high-assurance (governing doctrine, the shipped `AGENTS.md` and a frozen gate test are in the template's trigger list).

### Withdrawn / superseded commitments

* "Keeps that surface's floor" for a trivial-lane repair on a named surface (draft R1): withdrawn. It raised a floor the module does not raise; Question 4 holds the open point.
* "Any work on a high-risk surface stays high" (draft R2): replaced by the bright-line list, so the wording-cleanup row stands.
* Asking the Maintainer to accept his direction "as the evidence" for the rate-limit gate (draft Context): replaced by "the gate is not engaged" and Question 3.
* The R5 measure "likely would have avoided it" and a bare ten-pass count: replaced by the per-case reason, the reviewer's model, the separate count of plan and code passes, and the plain statement of what the count cannot show.
* Draft figures "11 of 12", "20 of 21", "five places", "about 150 tokens of about 8,300": replaced by the recount above.
* The table's "Model named at spawn" row as drafted: replaced by the row above, which says what it cannot see.
* Question 2's tie to the R5 count: replaced by dated direction as the source of data.
* The "Worked example" cut with dangling mentions: kept, with the mentions reworded.
* "Scope delta: preserved (opening revision; nothing removed)": replaced by the grouped record above.
