# External is the Maintainer's call: one review stance, with the questions changing by stage

**Author**: Claude (Strategy)
**Status**: awaiting-review
**Review**: required(Internal)
**Plan review**: required(Internal)
**Opened**: 2026-10-18

*Length: about 500 lines, well over the 250-300 aim. The Maintainer's second direction
widened this from removing a choice to saying, once and in every place, what a review
must ask. About 175 lines are lists the brief required (the Questions, the Origin
quotes, the migration, the file list, the tests and the exclusions); the argument is
the rest. Read "In plain terms" and "Questions for the Maintainer" first: they are
enough to decide.*

## In plain terms

**What changes for you.**

* **No agent ever picks a kind of review.** There is no `required(External)`, no
  "External floor" on proposals, and no "External code review is an escalation".
  There is one review, at every stage.
* **Every review asks the foundational questions of its stage**, answers each in
  writing with evidence, and says what it did not cover. It is on the work's side
  and wants it better. It does not hunt for holes for their own sake, and it does
  not polish something that should not exist.
* **"External" becomes a word that means one thing: you asked for it.** You may ask
  for more distance on anything, at any time: a different agent type, a person, or a
  deliberate attempt to kill a big decision. You ask outside the usual procedure, and
  the record quotes your words.
* **Security Review is unchanged.** It stays a separate obligation on high-risk
  surfaces. It is about *what* is examined, not who examines.

| Stage | What the reviewer asks of the foundation |
|---|---|
| Proposal | Should this exist as framed? Is there a better design, doing nothing included? |
| Plan | The Decision settled the premise. Does this plan deliver it? Is there a simpler path? |
| Code | Does it really do what it claims? Try to break it, in order to fix it. |

**Every review owes three written answers**: should the work happen as framed (for
code: does it do what it claims), the best alternative, and what would show it wrong.
**Improve means recommend.** The reviewer proposes the better version; "don't do
this" and "do it differently" count. The author decides, and any narrowing still
reaches you as a scope change. **There is no quota of findings.** A review that finds
no defects is allowed when it shows its work.

**Two things in this change you should know about before you decide.** It edits a
framework anchor (the Dual-Review statement in `doctrine/rationale.md`), so the
Decision accepts that knowingly. And it changes what the README and its figure say
about review.

## Questions for the Maintainer

Each has my recommended default. An unanswered question takes its default.

1. **Capability floors, re-keyed to the stages.** The model-selection table now names
   "External Review" (high) and "Internal Review" (medium). I propose proposal
   review **high**, plan review **medium**, code review **medium**, Security Review
   **high**. Proposal review is high because the premise is still movable there and
   a wrong one is cheapest to catch there. *Default: these four.*
2. **The name "Dual-Review".** With one stance it no longer means two tiers. I would
   keep the name and the module id `dual-review` (the id is part of the install
   contract) and say what "dual" now means: an independent reviewer beside the
   author at every stage, with your Decision after. *Default: keep the name; a rename
   is a separate proposal.*
3. **Who gets the lens roster.** The `dual-review` module (the nine lenses, the
   scope-reduction trap) installs only for teams with two agent types. Under one
   stance a solo team gets none of it. Changing who gets the module edits the engine
   and the install set, so it is not in this change. *Default: leave the gate; open a
   proposal if you want it everywhere.*
4. **The migration.** Nothing is rewritten. A legacy `(External)` label on a pass
   nobody called is read as the standard review. For the one open case,
   `2026-10-18-claude-board-as-basis`, the Decision reads its External-labeled pass
   as the standard review unless you tell it you called for it. *Default: ratify.*

## Origin

The Maintainer, 2026-10-18, quoted verbatim:

> "Make it a proposal, yes. We need to completely do-away with agents selecting External review. We can, of course, decide to do such a thing. But that has to be something that the maintainer decides to do outside of the usual procedure. So "External" is a stance, not an agent type."

Earlier the same day, for code review (applied in `b712020d`; the commit body says it
was relayed to that session by the coordinating session):

> "No external by default. That can't be the case as we've discussed in other sessions extensively."

On the idea of one stance whose foundations vary by stage, relayed to this session by
the coordinating session:

> "I actually like your foundations at each stage. That's a really nice, succinct way of putting it."

The Maintainer also asked "Never a review with no findings?" (relayed). Section 2
answers it: never a review with no *answers*.

## Context

**The rule is contradicted today, in text adopters receive.**

* `doctrine/dual-review.md` says in "Structural independence" that no tier requires a
  different agent type, and in "Plan review is Internal, always" that "External
  independence lives at the proposal" and keeps an "External floor on deliberate-lane
  proposal review". `AGENTS.md` says External is "an escalation" for code.
* `templates/modules/team-gated/dual-review.md`, which a two-agent-type team installs,
  says the External reviewer's floor is "a different agent type ... or a human", that
  "a human fills the External tier", and that a clean code review is "confirmed by a
  second independent different-agent-type pass". `docs/glossary.md` says the External
  floor is "a different agent type, or a human".
* `templates/onboarding/*.md` tell adopters the External tier or floor is "filled by
  the human Maintainer's read" or by the second agent type.
* Cairn's own `dev/modules/dual-review.md` is a stale copy: it still says "an explicit
  second-round recommendation", which the doctrine forbids.
* `dev/proposals/_template.md` and its shipped twin offer `required(External)` as a
  header value an author may write.

**The label became an agent's choice.** 78 review sections in `dev/proposals/` are
headed External (`grep -rhE '^## (Review|Re-review|Round[^-]*review).*[Ee]xternal'
dev/proposals`). 73 name a different vendor from the proposal's author. The other 5
name the same vendor, and all five are proposals opened 2026-10-17 or 2026-10-18, after
`d98b4c19` (2026-09-01) stopped requiring a different type. So the floor survived, the
type requirement went, and what remained was an agent deciding, on every deliberate
proposal, to run a pass called External.

**Two agents disagreed on the floor inside one proposal.** `2026-10-18-claude-board-as-basis`
declared `required(Internal)`, citing earlier waivers, "for your Decision to ratify or
override". Its reviewer then ran an External pass anyway, and the Response withdrew
the author's sentence. Neither was wrong under the text. The text let both choose.

**No tool validates these fields.** The lifecycle planner was removed in `bfe6bbfd`.
I searched `tools/`, `scripts/`, `templates/skills/` and `bootstrap/_scaffold/` for
`**Tier**` and `required(`. `tools/board.py` prints the `Review` field as written,
`tools/audit_report.py` checks that a risk field is present, and
`scripts/gen_legacy_passes.py` (a one-off generator) reads plan `Plan review` values.
The onboarding trigger reads review headings for a different *vendor* name, not for
the word External. So the grammar change costs no parser change, and equally nothing
enforces it: the trigger is a reviewer reading a reviewer, and you at the Decision.

## Proposal

### 1. One stance, three stages

Every review, at every stage, has one stance: **the reviewer is on the work's side and
makes it better by questioning its foundations.** No agent chooses a different stance
and there is no tier to select. The stage sets which foundation is questioned (the
table above). Two limits keep this honest:

* **The questions are required answers, not a mood.** Without that, "wants it better"
  drifts into polishing something that should not exist.
* **Improve means recommend, not rewrite or cut.** A recommendation may be "don't do
  this" or "do it differently". The author answers it in the Response and decides.
  A narrowing is a scope change under the existing outcome test, and only you concede
  it (`doctrine/dual-review.md` > "Review expectations — the scope-reduction trap").
  This adds nothing to that rule; it restates it where reviewers will meet it first.

Code review keeps its floor, unchanged: **not the implementing agent**. A code review
never reopens the Decision; its "should it exist" question is "does it do what it
claims". Plan review is a fresh-context pass and has one round, unchanged.

### 2. What every review must show

Each pass opens with a `**Foundations**` block of three lines, each ending in the file,
test, line or command that backs it:

| | Answer 1 | Answer 2 | Answer 3 |
|---|---|---|---|
| Proposal | Should this happen as framed? yes / yes but differently / no | The best alternative, doing nothing included | The observation that would make the author withdraw |
| Plan | Does it deliver what the Decision settled? | A simpler path to the same outcomes | The result that would show it cannot deliver |
| Code | Does it do what it claims? | A simpler or safer build, if there is one | The input, test or run that breaks it, and what was tried |

The nine lenses in `doctrine/dual-review.md` stay as the generic roster, but they
become **where the evidence for these answers comes from**, not a second checklist.
A lens cited only to be ticked, with no answer resting on it, is the "checked" failure
the doctrine already names. The closing coverage line keeps its two halves, and its
first half is now the evidence behind the three answers; its second half, what the pass
did not cover, is unchanged. The coverage line still does not end in a recommendation
for more review. A reviewer reports the risk and the gap; you read the negative space
and decide whether to ask for more.

**On "never a review with no findings".** The clean-pass trap stays, restated: a
review that reports no defects is allowed when its three answers are evidenced and its
negative space is named. The thin clean pass is what deserves skepticism. **There is no
quota of findings.** A quota invites manufactured nits, and it feeds the narrowing bias
that `doctrine/dual-review.md` already warns about. A clean code review still carries a
falsification ledger; "or a confirming second different-agent-type pass" is struck.

### 3. External is the Maintainer's call

An **External read** is a review the Maintainer called for, outside the usual procedure.
The Maintainer sets the distance (a different agent type, a person) or the brief (try to
kill a large decision). The word means that and nothing else.

* **How you ask**: in chat, in a Decision, or in a standing instruction you author. An
  agent never creates a standing call by inference.
* **How it is recorded**: the pass carries a line `**Called by**: Maintainer`, followed
  by your words, verbatim and visually isolated, and the same quote in the commit body,
  as for a scribed Decision. A relayed instruction names the relayer. `**Tier**: External`
  is valid only with that line. A pass headed External without it is read as the
  standard review; the label was wrong and the content still counts.
* **What an agent never does**: write `required(External)` or an equivalent in a header;
  say a change "needs" or "floor-requires" one; escalate a code review to one; head a
  pass External on its own; start one without your quoted words.
* **The staffing agent follows your brief.** It answers the same three questions from
  the distance and with the brief you set, and its pass says so.

### 4. Header and record grammar

* `**Review**:` stays, with two values: `required(Internal)` and
  `required(Internal + Security Review)`. It no longer names a tier. It carries the one
  decision it still forces: whether a Security Review is owed. The token `Internal`
  stays because plan headers, `AGENTS.md` and 68 proposals and plans use it; read it as
  "the usual review". `required(External)` is removed from the template's menu.
* `**Plan review**:` is unchanged: `required(Internal)` or
  `required(Internal + Internal Security Review)`.
* The pass record keeps `**Tier**:` (a name used by every existing record), with the
  values `Internal | Security Review`, plus `External` only with `**Called by**`.
* **Security Review** keeps its own obligation line, protocol and trust-boundary
  checklist. It uses the same stance; it differs in what is examined.

### 5. Harmonizing every statement of what a review asks or shows

The rule is stated once per layer and conformed everywhere else (file list below). In
`doctrine/dual-review.md`: "Two tiers, two purposes" becomes "One stance, three stages";
"Structural independence" keeps distance as recorded, not required; "Plan review is
Internal, always" loses the External floor and the type-scoped-removal paragraph; "Code
review — the implementation side" loses the External escalation; the clean-pass trap,
the coverage line and "Briefs to reviewers" are re-pointed as in section 2. A brief to a
reviewer may state the stage's three questions: they are the same for every artifact at
that stage, so they do not telegraph a lens. The heading "Review expectations — the
clean-pass trap" and its place before the scope-reduction trap stay, because
`bootstrap/tests/test_scope_reduction_trap.py` pins them.

### 6. Capability floors keyed to the stages

`templates/modules/team-gated/model-selection.md` and `doctrine/roles.md` > "Capability
floors" replace the "External Review" and "Internal Review" rows with the four stage
rows (Question 1). The bright-line phrase "adversarial premise-checking" becomes
"premise-checking", which is proposal review's question. "Diversity within tier" stays
as a recommendation: a different model architecture is useful distance, never required.
The tier-to-model mapping file and `scripts/check_model_selection.py` key on capability
tier (high / medium / low), not on role, so neither changes.

### 7. Migration

Five artifacts from 2026-10-17 and 2026-10-18 are in play, as `python tools/board.py`
and its `--archive` view show them. Four proposals opened 2026-10-17 declare
`required(External)`: two are accepted and still in `dev/proposals/`, and two are
archived as the sources of the two plans on the board. The fifth, `board-as-basis`
(2026-10-18), declares Internal but received an External-labeled pass.

| What | Disposition |
|---|---|
| Archived records | Keep their `External` tokens and passes. Immutable, readable, as in the 2026-08-24 precedent. |
| `2026-10-17-claude-independent-scientific-check`, `...-neutrality-and-upgrade-slots` (accepted; header `required(External)` and `required(External + Security Review)`) | Headers stay as written. Their External and Security passes are the reviews they were. Nothing owes a further External. Neutrality's Security Review obligation was met in its record. |
| `maintainer-attention` and `verification-practice` plans | Headers say `required(Internal)`, so unaffected. Their archived source proposals declared `required(External)`, which stays. |
| `2026-10-18-claude-board-as-basis` (awaiting-decision; header Internal, External-labeled pass) | Header and pass stay. The Decision reads the pass as the standard review unless you called for it (Question 4). |
| Legacy `(External)` labels generally | Read, never rewritten, never warned: no tool reads them, so there is nothing to warn. |
| Tests pinning tier vocabulary | See *Tests required*. One frozen test file is retired and replaced. |
| Onboarding presets and their installed copies | Reworded so the External tier is not "staffed" by anyone. Three solo-greenfield passages are the pinned ones. |
| In-flight overlap | `verification-practice` (code review open) edits `AGENTS.md`, `doctrine/dual-review.md`, `doctrine/plans.md` and the plan template; `maintainer-attention` edits the plan template, `doctrine/plans.md` and `doctrine/lifecycle.md`, and adds five nodes to the frozen `test_replacement_tools.py`, which owes the same Maintainer re-anchor this change does, so one re-anchor can cover both if they are sequenced. This change's plan opens after both archive. If the code-review finding that proposes pinning "An External code review is an escalation" lands first, this change replaces that pin. |

### 8. Reaching adopters

Adopters receive `templates/core/AGENTS.md`, the templates and the installed modules,
never `doctrine/`. So the rule is written in `templates/core/AGENTS.md` and in the two
shipped templates first, and Cairn's own copies are conformed to match. The rule does
not live only in the `dual-review` module, because that module installs only for teams
with two agent types (Question 3). A solo team receives the stance, the three answers
and the Maintainer-called read through `AGENTS.md` and the proposal and plan templates.
The shipped sources, and Cairn's installed copies under `dev/`, are listed below.

### Not in this proposal

* **The engine's staffing gate.** `_TEAM_STAFFING_GATES` in
  `bootstrap/_scaffold/config.py` keeps `dual-review` to `concurrent-multi-type` teams.
  It remains coherent: that team can staff the Maintainer's "different agent type"
  option. Changing it is an install-contract change (Question 3). The comment above it,
  and the matching comment in `bootstrap/tests/test_presets.py`, still read acceptably
  and are left alone: editing them touches the engine package or a frozen test for no
  behavioural gain.
* **`bootstrap/REANCHOR_RUNBOOK.md`.** It requires "an External Security review" of the
  re-anchor launcher. The Maintainer runs that ceremony and chooses the reader, which is
  the Maintainer-called case by construction. Editing a trust-ceremony document would
  take its own Security Review.
* **Credit comments** such as "per External Review P2-3" in
  `scripts/_onboarding/triggers.py` and its twin. They record who found something, not a
  rule, and the files are frozen. The `first-cross-type-review` onboarding trigger
  matches a different *vendor* in a review heading, not the word External, so it is
  unaffected.
* **Stale planner text** in `doctrine/plans.md` (the record-schema section) and
  `bootstrap/UPGRADE.md` that describes the gate removed in `bfe6bbfd`. This change
  conforms only their External rows. A cleanup of the removed machinery is separate.

## Rationale

**The doctrine-evolution gate** (`doctrine/rationale.md` > "How the doctrine evolves
under evidence") bars a change from a single incident unless the Maintainer classifies
it high-risk, and otherwise needs recurrence. I do not claim high-risk. The evidence is
recurrence of one shape, which is that a rule treats External as something a tier or an
agent selects, the Maintainer overrules it for one kind of artifact, and it survives in
the next. Seven dated occurrences in eight weeks, six before this one:

1. 2026-08-24: External *plan* review retired. "It is not, and should not ever, be
   required." (`dev/proposals/archive/2026-08-24-claude-retire-external-plan-review.md`)
2. 2026-08-24: the `convergent-lifecycle` Decision waived the External plan floor.
3. 2026-09-01: `d98b4c19`, "We cannot require an External type review, ever", recorded
   "because the rulings kept being re-made".
4. 2026-10-01: the `adopter-path-consolidation` Decision, "External floor waived".
5. 2026-10-18: `b712020d`, "No external by default": `AGENTS.md` contradicted the
   doctrine on code review.
6. 2026-10-18: `board-as-basis` declared below the floor and its reviewer ran External
   anyway (Context).
7. 2026-10-18: this direction.

Each earlier fix removed External from one artifact kind: plan, then type, then code.
This one removes the last place (the proposal floor) and the label's selectability, which
is why it should be the last. It is also not a patch on the patch: it deletes a choice
and adds no tier, no escalation and no checker.

**Why keep the questions.** The External passes changed designs: the `board-as-basis`
pass answered "Should it land? Yes, in a narrower form", and the author took its
rejected alternative. The value was the foundational questions, not the label. Making
them a required answer at every stage, with evidence, keeps the value and removes the
selection. Extra distance then costs you one sentence when you want it, and the record
shows it was your choice.

## Alternatives considered

* **Keep External as a tier agents may choose when risk warrants.** Rejected: it is the
  current rule, and it produced the seven occurrences. "When risk warrants" is an agent's
  judgment about the Maintainer's attention.
* **Delete the External vocabulary entirely.** Rejected: you need a word to ask with,
  and the record needs one to mark that you did. The word survives with one meaning.
* **Rename `Internal` to `standard` in headers.** Rejected: 68 proposals and plans, the plan
  header grammar and `AGENTS.md` use `Internal`, and you ruled plan review "Internal,
  unchanged". It is churn for a label no tool reads.
* **Drop the `**Review**:` field.** Rejected: it is the one place an author must say
  whether a Security Review is owed. A missing decision there is worse than a constant
  value.
* **Make the foundational questions optional guidance.** Rejected: that is the mood
  version, and it is how "wants it better" becomes polishing.
* **Do nothing.** Costs a seventh and eighth ruling, and adopters keep receiving
  `required(External)` and "a human fills the External tier" with no one to fill it.

## Documentation / doctrine surface

Layers follow `docs/DOCUMENTATION_PLAN.md`: prescription in the governing layer,
description in the descriptive layer. The authoritative list is the plan's
case-insensitive search for External, tier and independence wording; this is the known
set, shipped source first and Cairn's installed or self-hosted copy beside it.

* **Governing and shipped**: `templates/core/AGENTS.md` and `AGENTS.md` (Review section,
  intro line); `templates/core/dev/proposals/_template.md` and
  `dev/proposals/_template.md`; `templates/core/dev/plans/_template.md` and
  `dev/plans/_template.md`; `templates/core/dev/agent_collaboration.md` and
  `dev/agent_collaboration.md`; `templates/core/dev/collaboration_agreement.md` and
  `dev/collaboration_agreement.md` (including Cairn's own roster slot, which says
  External is a different agent type); `templates/modules/team-gated/dual-review.md`
  and `dev/modules/dual-review.md`; `.../model-selection.md` and
  `dev/modules/model-selection.md`; `.../security-review.md` and
  `dev/modules/security-review.md` (a dangling "External Review Norms" pointer);
  `templates/onboarding/{solo-greenfield,collaborative-team,high-rigor-legacy}.md`
  with `dev/modules/onboarding/{collaborative-team,agent-team-onboarding}.md`;
  `templates/phase-0/project-profile-legacy.md`; `templates/skills/session-start/SKILL.md`
  and `.agents/skills/session-start/SKILL.md` (one phrase: "review tier, plan-review
  tier" describes the board's columns).
* **Doctrine**: `doctrine/dual-review.md`, `doctrine/plans.md`, `doctrine/proposals.md`,
  `doctrine/roles.md`, `doctrine/rationale.md` (the anchor), `doctrine/lifecycle.md`,
  `doctrine/lifecycle-contract.md`, `doctrine/session-routines.md` (the agent-dispatch
  line: dispatch follows what the Maintainer asked, else a same-type fresh session).
* **Dimensions**: `dimensions/README.md`, `agent-team.md`, `human-team.md`,
  `complexity.md` (its "External review is mandatory" for the complex position is a
  tier rule choosing External, so it goes).
* **Descriptive**: `README.md` (alt text and the paragraph beneath the figure),
  `docs/assets/dual-review-independence.svg` (redrawn), `docs/glossary.md`,
  `docs/vision.md`, `docs/agent-team-onboarding.md`, `docs/quickstart.md`,
  `docs/workflow-role.md`, `docs/getting-started.md`, `docs/dev-tour.md`,
  `docs/tool-usage.md` (the same "review tier" phrase).
* **Contract-adjacent prose**: `bootstrap/fidelity-check.md` (the sample roster line
  `External Reviewer`; the only test reading this file pins its `optional_templates:`
  block) and `bootstrap/UPGRADE.md` (External rows of the plan-pass schema).
* **Tests**: see below.

**Nothing under `bootstrap/_scaffold/` is touched, so there is no AST impact** and no
`_ast_attest` re-anchor. **Install contract**: `scaffold.py --manifest` lists
destinations and modes; no path is added or removed, only template contents change, so
adopters get them through the ordinary upgrade merge. The plan diffs the manifest before
and after. `CHANGELOG.md` is edited at archive, the serialization point.

**Gate manifest.** Exactly one `frozen_files` entry in
`bootstrap/tests/fixtures/gate_manifest.json` changes:
`bootstrap/tests/test_onboarding_review_tiers.py` is deleted, so its five nodes leave
the collection. Per `AGENTS.md`, a deleted frozen file reddens
`bootstrap/tests/test_gate_manifest.py` until the re-anchor runs. That re-anchor is
**MAINTAINER-ONLY** and is its own plan chunk; an implementing agent does not bless its
own verifier. Frozen files deliberately not edited: `bootstrap/tests/test_presets.py`,
`bootstrap/tests/test_scope_reduction_trap.py` (kept green by keeping its pinned
headings), and the `_onboarding` scripts. No markdown file in this list is frozen
(checked: the only frozen `.md` is `bootstrap/tests/fixtures/skills/README.md`).

## Evidence / verification plan

**Falsification instrument.** One case-insensitive search for agent-selected External,
over the governing and shipped paths. Before the change it matches 26 files
for the pattern `required\(External|External floor|External independence lives|declared-External|External code review is an escalation|different agent type, or a human|a human fills the External|different-agent-type pass|External[ -]tier|External Reviewer|External review is`
(as of 2026-10-18; positive control: it matches `AGENTS.md` and
`templates/core/AGENTS.md` today). After the change every hit must be the
Maintainer-called definition, a credit comment, or a marked history reference; the plan
classifies each. The pattern misses `doctrine/rationale.md`, `doctrine/lifecycle.md`
and the README, which phrase it differently, so the plan also reads every hit of
`external` and `independen` in those files; the list above is not the authority, the
search is.

**What would fail it**: a shipped template that still offers `required(External)`; a
shipped sentence that says a type or a human "fills" an External tier; any rule that
tells an agent to escalate to or declare External.

### Tests required

* **Retire** `bootstrap/tests/test_onboarding_review_tiers.py` (frozen). Its premise,
  that an External floor needs a different agent type or a human, is retired, and its
  positive check requires exactly three solo-greenfield paragraphs to name their
  staffing, which cannot survive the rewording. Its two forbidden wordings carry over.
* **Add** `bootstrap/tests/test_review_stance_in_shipped_files.py` (not frozen), modeled
  on `test_review_and_verification_rules_ship.py`. It reads both `AGENTS.md` copies,
  the two templates, the `dual-review` module and the onboarding presets, and pins:
  the obligations (one stance; three written answers; improve means recommend; no quota;
  External only when the Maintainer called it, with a verbatim `Called by`), and the
  forbidden phrasings above. Each obligation is an alternation over
  whitespace-collapsed text, with node IDs that are labels. **Controls**: each
  forbidden pattern is first shown to match its pre-change string, and each obligation
  is shown to fail on a copy with the sentence deleted.
* **Every test file the search `grep -rln External bootstrap/tests/` returns** (18),
  with what happens to it:

| File(s) | What "External" is there | Disposition |
|---|---|---|
| `test_onboarding_review_tiers.py` (frozen) | The pin itself | Retired, above |
| `test_scope_reduction_trap.py` (frozen) | A fixture heading; the test also pins the doctrine heading "the clean-pass trap" and the scope-reduction obligations in both module copies | Unchanged and must stay green: those headings and obligations are kept |
| `test_presets.py` (frozen) | A comment: dual-review needs a second type "to fill its External tier" | Left as written (Not in this proposal) |
| `test_reference_scripts.py`, `test_session_routines.py`, `test_trigger_evaluation_action.py` | Fixture headings such as `(External Reviewer)` and `(External)` used to exercise review-heading parsing and the vendor-match trigger | Unchanged: the parsers key on the vendor name, not the word |
| `_gate_manifest.py`, `_gate_preflight.py`, `_gate_transition.py`, `test_gate_preflight.py`, `test_reanchor.py`, `test_correct_pinned_digests.py` | "External Security Review" provenance strings and a note that three historical phase-mutable fixtures were governed by an "External-stance review" | Unchanged: history of how past ceremonies were reviewed, in frozen files |
| `test_content_scan.py`, `test_claim_check_module.py`, `test_link_check_exclusions.py`, `test_onboarding_activation_helper.py`, `test_onboarding_slot_substitution.py` | Authorship credits in comments and docstrings | Unchanged |
| `test_security_stack.py` | "External simulator", an unrelated trust-boundary term | Unchanged |

* **Readers of changed prose that do not say External**, so the search above misses
  them: `test_review_and_verification_rules_ship.py` and
  `test_verification_boundaries.py` (they read `AGENTS.md`; the paragraphs they pin are
  untouched), `test_scaffold.py`, `test_documentation_plan_module.py` and
  `test_onboarding_seed_roster.py`. The plan finds any others by searching what imports
  or reads each touched file, not by expectation.

### Examples / smoke checks

`python scripts/claim_check.py` and `python scripts/check_cairn.py` over every changed
file; `python scripts/quality_gate.py --sub neutrality` (shipped text must name no
vendor); `python bootstrap/check_module_body_coverage.py --target . --cairn-root .`
reports 8 missing topics today and must not report more (an advisory heading-name
probe: renamed doctrine headings must have their words in the module);
`python bootstrap/scaffold.py --manifest` diffed before and after. A scratch install
(`--dry-run` or a temp target) is grepped for the forbidden phrasings.

**Boundary B is `full`.** The change touches the gate manifest fixture and the fidelity
manifest prose, both contract surfaces, so bounded mode refuses.

#### Security preflight

N/A: no trust boundary added, moved, or widened. No code path changes except a test
deletion and a test addition; no parsing, subprocess, file-write or network behavior
moves. The re-anchor is a Maintainer-run ceremony this change does not alter.

## Signals the change is wrong

* **You find yourself asking for an External read on most proposals.** Then the option is
  carrying the load the floor used to. Reintroduce a floor on purpose, with a recorded
  reason, not by drift.
* **Reviews read as polish.** Pass after pass with `Should this happen as framed? yes`
  and no alternative of substance means the required answers have become a form. The
  signal is the answer's evidence being thin, not the count of findings.
* **A defect ships that a more distant read would plausibly have caught**, and no one
  had asked for one. Audit it against the actual finding, not the counterfactual.
* **An agent writes External in a header or an escalation sentence again.** The rule is
  leaking back; the shipped-file test should have caught it, so check the test too.

## Scope delta

**Scope delta**: preserved. Nothing the proposal opened with has been dropped. The
"Not in this proposal" list names exclusions as opened, with the reason each stays out.

## Assurance path

**Assurance path**: high-assurance

It edits governing doctrine and the authoring templates, a framework anchor, and the
prose of the fidelity manifest, and it retires a frozen gate test. No Security Review is
owed: no trust boundary or high-risk surface in `AGENTS.md` changes, and the engine
package is untouched.

Proposed paths:
* `bootstrap/tests/test_review_stance_in_shipped_files.py`
