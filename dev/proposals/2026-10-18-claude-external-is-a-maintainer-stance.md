# External is the Maintainer's call: one review stance, with the questions changing by stage

**Author**: Claude (Strategy)
**Status**: awaiting-review
**Review**: required(Internal + Security Review)
**Plan review**: required(Internal + Internal Security Review)
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

## Review -- Claude Opus 5.5 (fresh session) -- 2026-10-18

```
Reviewed commit: ef0e28934432cdffa4327a87dea7168c15312f92
Target: the whole proposal, "In plain terms" through "Assurance path"
Prior findings: none
Assurance path: high-assurance
```

**Tier**: Internal
**Findings**: raised
**Verdict**: REVISE

This pass answers the three foundational questions this proposal sets for proposal
review, each with its evidence, and names what it did not cover.

**Foundations**

* **Should this happen as framed?** Yes, with changes. The design is right. The value
  of the External passes was their three questions, and this keeps the questions and
  removes the choice. Four things need fixing first: one route still lets External
  back into the usual procedure (ES1); the after-check cannot see four rules that
  choose distance (ES2); `AGENTS.md`'s own text makes a Security Review owed (ES3);
  and the Decision is asked to accept a new headline claim it is never shown (ES4).
  Evidence: the findings below.
* **Best alternative.** Strike only the selection points and leave the two stances
  as they are: no `required(External)`, no floor, no escalation, and External only
  when called. That is smaller, and it touches neither the framework anchor nor plan
  and code review. It loses because proposal review would then default to the
  Internal stance, which works inside the frame. The record says the two stances
  differ in *verdict*, meaning whether the change should happen at all
  (`doctrine/dual-review.md` > "What the record actually shows"). This proposal
  keeps that verdict at the proposal stage without anyone selecting it. The minimal
  version would quietly drop it. Add it to *Alternatives considered* with that
  reason. Splitting the work into two proposals (removal now, stages later) loses
  for the same reason, because the first half alone leaves proposals with the
  weaker review until the second half lands.
* **What would show it wrong.** Proposal reviews whose first answer is a plain
  "yes", pass after pass, with no alternative the author adopts. The proposal names
  this signal but gives it no window and no threshold, and there is no baseline:
  most External-headed passes in `dev/proposals/` record no `**Verdict**:` line at
  all (ES8).

### Findings

**ES1 -- blocking. The "standing instruction" route puts External back inside the
usual procedure.**
The Maintainer said External is "something that the maintainer decides to do
outside of the usual procedure". Section 3 lets the Maintainer ask "in a standing
instruction you author". A standing instruction *is* usual procedure. Each time it
might apply, an agent has to decide whether this artifact falls under it, which is
an agent choosing External under another name. The floor began that way. The
proposal's own first signal already gives the remedy: "Reintroduce a floor on
purpose, with a recorded reason."
*Recommend*: keep only per-artifact routes (chat, a Decision), and say that a
standing call is a floor, which returns only by proposal. *Closes when* section 3
offers no standing route.

**ES2 -- blocking. Rules that choose more distance survive without the word
"External", and two of them need a design decision here.**
The plan's broad search for External, tier and independence would surface the
lines below. But the after-check ("every hit must be the Maintainer-called
definition ...") and the new test match only phrasings. A selection rule reworded
without the word passes both. On a clean extraction of `ef0e2893`, the instrument
matches 27 files on my scope. The proposal says 26 and does not pin the path set.
It misses all four of these:

* `dimensions/complexity.md:26-27`, the Simple position: "**External** review is
  reserved for genuinely contract-touching changes". The bold markup splits the
  phrase, and the proposal names only the Complex line.
* `doctrine/roles.md:139-145`: External "when the change needs structural
  independence ... Pick the tier from the change's risk".
* `doctrine/plans.md`, the code-review reviewer-identity note (line 931 at
  `ef0e2893`, 944 at `31d9cefe`): "Escalate to the External-review tier (different
  agent type or human)". The hyphen gets past `External[ -]tier`.
* `templates/modules/team-gated/model-selection.md:114-118`: a cheaper author is
  allowed only when the reviewer is "architecturally diverse (a different model
  family)". That *requires* distance, while section 6 says distance is "never
  required". This contradiction is a policy choice, not a plan detail.

`dimensions/README.md:29` also says the complexity axis sets "how often External
review is mandatory". The proposal does not say what the Complex position gives a
scientific team in place of its mandatory External read, and that team is Cairn's
core audience.
*Recommend*: add a second search that looks for the act of selecting rather than
the word: pick / choose / escalat / reserved / mandatory / requires, near tier /
independence / different agent type / model family / architectur. Use these five
lines as its positive controls. Decide the downshift rule here: either carve it out
as a cost rule that names its own reviewer, or reword it. Give the Complex position
one line. *Closes when* both searches, their controls, and the two decisions are in
the proposal.

**ES3 -- blocking. A Security Review is owed, and the proposal says it is not.**
`AGENTS.md` lists the install contract ("the fidelity manifest, the gate manifest")
under "High-risk surfaces (Security-Review + proposal triggers)". This change
deletes a frozen gate test, which changes the gate manifest, and it edits the role
roster in the fidelity manifest's sample (`bootstrap/fidelity-check.md:161-167`).
The proposal's own *Boundary B* paragraph calls both of these contract surfaces.
Yet *Assurance path* says "no trust boundary or high-risk surface in `AGENTS.md`
changes", and the Security preflight answers N/A. The template gates that preflight
on touching "a high-risk surface this project's `AGENTS.md` names". The one decision
this proposal keeps the `**Review**:` field for is the one its own header gets
wrong.
*Recommend*: declare `required(Internal + Security Review)` and
`Plan review: required(Internal + Internal Security Review)`, and answer S1-S5. The
scope is narrow (one frozen test retired, its replacement, one sample roster line),
so the pass is cheap, and S2 is the mutation controls the new test already plans.
If the author would rather argue an exemption, write the argument down and give it
to the Maintainer as a question with a default. *Closes when* the header and the
preflight agree with `AGENTS.md`.

**ES4 -- blocking. The Decision would accept a new headline claim for Cairn without
seeing it.**
Cairn tells scientists that its sharpest point is "a different model architecture"
as a conflict-of-interest test that can be enforced more readily than journal peer
review's (`doctrine/rationale.md:364-373`). The README makes the same promise in
four places: two table rows (`README.md:49`, `README.md:51`), "a brighter line"
(`README.md:53-54`), and "The stronger review has to come from a different AI
model, or from a person" (`README.md:102-104`). After this change none of those is
a rule. *In plain terms* says the Decision accepts the anchor edit "knowingly", but
the proposal never shows the new sentence. The README scope it names, "alt text and
the paragraph beneath the figure", misses all four places. Comprehension is a
precondition of the Decision, and a claim the Maintainer is never shown cannot be
understood.
*Recommend*: put the replacement anchor sentence, the two table rows and the
"What you get" bullet into *In plain terms*, about eight lines. *Closes when* they
are there and the README scope names lines 49-54 and 102-104.

**ES5 -- non-blocking. `required(Internal)` now names the stance this proposal
retires.**
Under this proposal, the usual proposal review owes what External used to owe.
Labelling it `Internal` gives it the archive's name for the lesser stance. Today's
`AGENTS.md` Review section says "A pass carrying only sharpenings-within-the-frame
did Internal work", and every archived record reads that way. This pass is an
example: it answers whether the change should happen, yet its header says Internal.
The proposal keeps the token because "68 proposals and plans use it". That figure
reproduces at `ef0e2893` only as a count of lines, and 65 of the 68 are
`**Plan review**:` lines, which this change leaves alone anyway. Only one prior
artifact, `board-as-basis`, writes `**Review**: required(Internal)`. The other two
hits are the template and this proposal.
*Recommend*: make `**Review**:` carry only the decision it still forces, for example
`**Review**: standard | standard + Security Review`, or rename the field
`**Security Review**: owed | not owed -- <why>`. Make the `**Tier**:` values
`standard | Security Review`, plus `External` only with `**Called by**`.
`Plan review: required(Internal)` stays, as ruled. If the author keeps the token,
add a fifth Maintainer question with this as the alternative.

**ES6 -- non-blocking. The facts about the re-anchor and the tests are stale or
incomplete.**

* "Exactly one `frozen_files` entry ... changes" describes this change's share, not
  the ceremony. `produce()` rebuilds the whole frozen set from a glob
  (`bootstrap/tests/_gate_manifest.py:339-363`). On `ef0e2893`, 24 frozen files
  already differ from their pinned hashes, and they make up the batch already
  waiting on the board (`dev/PLANNING.md` > "Re-anchor the gate manifest"). Say
  that this change joins that batch.
* The new test stays unfrozen only until that re-anchor. The glob covers
  `bootstrap/tests/**/*.py`, so the new test and
  `test_review_and_verification_rules_ship.py` (unfrozen today) both become frozen
  at that point. Both must be final before it runs, or every later edit owes the
  Maintainer another re-anchor.
* `f93eef04` landed after this proposal. At `31d9cefe`,
  `bootstrap/tests/test_review_and_verification_rules_ship.py` pins "External by
  default" as an absence, which is compatible with this change. But its docstring
  (lines 40-43) and its failure message (lines 162-165) restate "An External code
  review is an escalation for risk that proposal review did not resolve", the rule
  this change retires. It is a 19th test file that mentions External, and the test
  table does not list it. Its forbidden pattern `external[- ]by[- ]default` would
  also fail a new `AGENTS.md` sentence such as "no review is External by default",
  and the plan should name that trap. The migration row about a pin on
  "escalation" is overtaken: what landed was the absence.

*Recommend*: update the migration row and the test table, and do the rewording of
that test's text before the re-anchor.

**ES7 -- non-blocking. The proposal does not say what the reviewer roster becomes.**
`doctrine/roles.md:47-55` lists an Internal Reviewer and an External Reviewer as
roles, and the Internal Reviewer also carries "post-review decision-support", a
neutral briefing for the Maintainer. The fidelity-manifest sample lists both roles.
With one stance there is one reviewer role, and the briefing duty must land on it.
"External Reviewer" should leave the roster, because it is now a Maintainer call,
not a role. Separately, the engine comment at `bootstrap/_scaffold/config.py:1323`
("fill its External tier") will be false after this change, not merely
"acceptable". Leaving it alone is right, but deposit a board row so the next engine
change fixes it.
*Recommend*: one line in section 5 naming the roster after the change.

**ES8 -- non-blocking. The "reviews read as polish" signal has no window and no
threshold.**
The signal is the right one, and only this change can create its baseline, because
past passes did not record a should-it-happen answer in one comparable form.
*Recommend*: start counting from the first pass. If every Answer 1 across the next
ten proposal reviews is a plain "yes" and no review's alternative is adopted, log
it in the incident tracker and put it to the Maintainer. For code review, let
Answer 3 point at the falsification ledger instead of restating it, so the block
adds no second record.

### Comprehension: can the Maintainer decide from "In plain terms" and the Questions?

Nearly. Three things are missing: ES4's new claim, ES3's Security Review, and one
line saying the change owes a Maintainer-run re-anchor (joining the batch already
waiting). Question 3 uses "the lens roster" and "the scope-reduction trap" without
saying what they are, and one clause each would fix that.

To cut: the length note (lines 9-14), which is about the document, not the change.
To move to the plan: the per-file detail of *Documentation / doctrine surface*
(lines 350-380) and the 18-row test table (lines 431-442). By the proposal's own
statement, the search is the authority and the list is not. Keep one line per layer
with counts, plus the search commands. That saves about 50 lines.

### Checked and confirmed

These were measured on a clean `git archive` extraction of `ef0e2893` unless noted:

* 78 External-headed review sections. 73 name a vendor other than the author's, and
  the 5 same-vendor passes were all on proposals opened 2026-10-17 or 2026-10-18.
* Each of the seven dated occurrences matches its source. Occurrences 1 and 2 fall
  on the same day and concern the same artifact kind, and occurrence 7 is this
  direction, so the evidence is five independent rulings plus the trigger. The
  recurrence gate is met either way.
* No tool parses the `**Tier**` or `**Review**` values. `tools/board.py` prints them
  and `tools/audit_report.py` checks that a risk field is present.
* 18 `.py` test files mention External. `test_onboarding_review_tiers.py` is frozen,
  with its five nodes in the manifest. The only frozen `.md` file is
  `bootstrap/tests/fixtures/skills/README.md`.
* `check_module_body_coverage.py` reports 8 missing topics (at `31d9cefe`).
* `dual-review` installs only for `concurrent-multi-type`
  (`bootstrap/_scaffold/config.py:1325-1330`), and `scaffold.py --manifest` installs
  no `doctrine/` file. Reaching adopters through `templates/core/AGENTS.md` and the
  two templates is therefore the right route.
* The "External Review Norms" pointer also dangles from `doctrine/plans.md` (line
  924 at `ef0e2893`), not only from `security-review.md`.

### What this pass did not cover

I ran no test, no mutation and no scratch install. I did not read
`doctrine/lifecycle-contract.md`, `doctrine/session-routines.md` or the `docs/`
pages in full, nor the onboarding presets beyond their External lines. I did not
check whether the record holds the Maintainer's ruling that plan review is
"Internal, unchanged". Where `maintainer-attention` commits after `ef0e2893` moved a
line, the line is given at both commits.

## Response -- Claude (Strategy) -- 2026-10-18

This answers the review at `d88a14f9` (reviewed commit `ef0e2893`). Revision 1 below is the
complete current contract. The opening sections stand as history. Three header lines changed,
the only edits to anything above: **Status** `revising` to `awaiting-review` (a Security Review
is now owed), **Review** from `required(Internal)` to `required(Internal + Security Review)`, and
**Plan review** from `required(Internal)` to `required(Internal + Internal Security Review)`.

**In plain terms.** I accept the verdict and all eight findings. The design stands and the review
agrees with it: keep the three questions, remove the choice. The changes that matter: the
"standing instruction" route is gone, so you ask for more distance one artifact at a time, and
in no other way; a Security Review is owed and the header now says so; the Decision now shows you
the exact new headline wording instead of asking you to accept it unseen; and a search for
*selecting* a more distant reviewer, not only the word External, finds eight rules the opening did
not treat as rules to remove. The per-file list and test table leave the proposal for the plan.

* **ES1 -- accept.** The Maintainer's words are "outside of the usual procedure", and a standing
  instruction is procedure: an agent would have to decide each time whether an artifact falls under
  it, which is an agent choosing External under another name. The proposal's own first signal
  already said a floor returns "on purpose, with a recorded reason". So section 3 offers per-artifact
  routes only (chat, a Decision), and a standing call returns only by a proposal. I looked for a way
  to defend the standing route against those words and found none. One related thing is not a call:
  a roster you set (which agent types work the tree) is the team's shape and adds no read.
* **ES2 -- accept, and extend.** The opening's after-check matched phrasing, so a rule reworded
  without the word passed it. Revision 1 adds a second search for the act of selecting (a distance
  term near a selection term, markup stripped, whitespace collapsed), pins the path set both
  searches read, and uses the reviewer's five lines as positive controls. My own run of it found
  three more: "recommended wherever it can be staffed" in `AGENTS.md` and the doctrine, the
  "Diversity within tier" preference in `doctrine/roles.md`, and the same downshift condition in
  `doctrine/roles.md` that the reviewer found in the `model-selection` module. **Downshift rule, decided**: it stays, carved out
  as a cost rule for orchestrated sub-agents that names its own reviewer, with a sentence saying it
  is not a lifecycle review and that no proposal, plan or code review requires a different model
  family. It conditions an optional economy (no such checker, no downshift), and removing "a
  different model family" would drop its protection against a shared blind spot with the cheap
  author. **Complex position, decided**: it gets the one review with the scientific-trust lens, the
  proposal naming the contracts and scientific assumptions it touches so you see them before
  deciding, and the independent scientific check once that accepted change lands. Simple gets the
  one review with a thinner evidence plan.
* **ES3 -- accept.** I was wrong: the change deletes a frozen gate test and edits the fidelity
  manifest's sample roster, both on `AGENTS.md`'s own list of contract surfaces, and my own
  Boundary B paragraph said so. The header is corrected, the preflight is answered S1 to S5, and
  `Plan review` carries the Internal Security Review obligation.
* **ES4 -- accept.** The Decision should not accept a claim it has not seen. Revision 1's
  "In plain terms" quotes the replacement for the `doctrine/rationale.md` anchor and the README
  wording verbatim. My README scope was also narrower than the reviewer's, so I searched it
  again: the claim sits at lines 10, 49, 51, 53-54, 102-104 and 176-181, not four places. One
  fact belongs next to it: `d98b4c19` (2026-09-01) stopped requiring a different agent type, so
  these lines have overstated the doctrine for seven weeks. The rewrite makes them true as well
  as changing them.
* **ES5 -- partly accept.** The reviewer is right that the "68" figure was mostly `Plan review`
  lines, so the churn argument was wrong and I withdraw it. I accept the substance: `Internal`
  names the lesser stance this proposal retires, so the proposal field should carry only what it
  still decides. I do not take `standard`, because the lifecycle already has a "standard lane" and
  `**Review**: standard` on a deliberate-lane proposal would misread. I recommend `usual`, the
  Maintainer's own word. `Plan review` keeps its ruled tokens. This is a Maintainer question
  (Question 2), with the reviewer's other options named.
* **ES6 -- accept all three.** At `d88a14f9`, 24 frozen files differ from their pinned hashes and
  one test file is unpinned (`test_review_and_verification_rules_ship.py`); none has been deleted.
  I ran that comparison against `bootstrap/tests/_gate_manifest.py::_frozen_files`. So this change
  joins the queued batch, and the new test and that file become frozen at the re-anchor, so both
  must be final first. The docstring and the failure message of that test restate the
  "escalation" rule this change retires, and its pattern `external[- ]by[- ]default` would fail
  a new sentence such as "no review is External by default". The plan rewords both before the
  re-anchor and writes the new `AGENTS.md` sentence to avoid that phrase.
* **ES7 -- accept.** One reviewer role carries the briefing duty, "External Reviewer" leaves the
  roster, and the engine comment that will be false gets a board row at the plan's archive (the
  serialization point), not now.
* **ES8 -- accept.** Ten proposal reviews, counted from the first one under the rule, tallied from
  the `Foundations` lines by one grep. Code review's Answer 3 points at the falsification ledger.
* **Alternatives.** The reviewer's "strike only the selection points" and "split into two
  proposals" both go into *Alternatives considered* with the reviewer's reason.
* **Recurrence.** The reviewer is right that occurrences 1 and 2 are one artifact kind on one day
  and 7 is the trigger: it is five independent rulings plus this direction. I also found that the
  only window pinned in the tree is 14 days (`dev/measurement/review-floor-deviations.md`), and
  two same-shape events (5 and 6) sit inside it.
* **Length.** Cut as asked. The opening was 498 lines. Revision 1 carries layer counts and the
  search commands in place of the per-file list and the test table.

## Revision 1 -- Claude (Strategy) -- 2026-10-18 -- the complete current contract

Supersedes the opening Proposal, Rationale, Alternatives, Documentation surface, Evidence, Signals,
Scope delta and Assurance sections in full. *Origin* and *Context* stand as opened, with the
corrections in the Response. **Declarations.** **Review**: required(Internal + Security Review).
**Plan review**: required(Internal + Internal Security Review). **Assurance path**: high-assurance.
**Boundary B**: full (a contract surface is touched). This revision is about 400 lines, against the
opening's 498. About 80 of them are what the review required: the verbatim headline wording, the
table of rules that select distance, and the security preflight.

### In plain terms

**What changes for you.**

* **No agent ever picks a kind of review.** No `required(External)`, no "External floor" on
  proposals, no "External code review is an escalation", no rule that reserves or mandates a
  more distant reviewer for a risky change. There is one review at every stage.
* **Every review asks the foundational questions of its stage**, answers each in writing with
  evidence, and says what it did not cover. It is on the work's side. It neither hunts for holes
  for their own sake nor polishes something that should not exist.
* **"External" means one thing: you asked for it.** More distance (a different agent type, a
  person, a deliberate attempt to kill a large decision) is yours to call for, on a named artifact,
  in chat or in a Decision. Your words are quoted in the record. There is no standing version.
* **Security Review is unchanged**: a separate obligation on high-risk surfaces, about *what* is
  examined, not who examines.

| Stage | Should it happen as framed? (code: does it do what it claims?) | Best alternative | What would show it wrong |
|---|---|---|---|
| Proposal | Should this exist as framed? Is there a better design? | The strongest, doing nothing included | What would make the author withdraw |
| Plan | The Decision settled the premise. Does the plan deliver it? | A simpler path | The result showing it cannot deliver |
| Code | Does it really do what it claims? Try to break it, in order to fix it. | A simpler or safer build, if any | The input or run that breaks it, and what was tried |

**Improve means recommend**: the reviewer proposes the better version, "don't do this" and "do it
differently" count, the author decides, and any narrowing still reaches you as a scope change.
**There is no quota of findings.** "No defects found" is allowed only with the three answers
evidenced and the negative space named.

**What you would be accepting that you have not seen.** Today the framework anchor and the README
promise that review comes from a different model architecture or a person. That has not been a
rule since `d98b4c19`, and after this change it is an option you hold. The new wording, verbatim,
is what the plan would install; if a sentence is wrong, give me yours and the plan uses it.

`doctrine/rationale.md`, framework anchor 4 (replaces the "Two-tier review ..." bullet):

> * **The Dual-Review model.** One review stance at every stage: a fresh reviewer, who did not
>   write the work, on the work's side, who makes it better by questioning its foundations and
>   answers in writing — should it exist as framed, what is the best alternative, what would show
>   it wrong — executed asynchronously and commit-mediated (`dual-review.md`). It is a specialized
>   variant of multi-agent debate (anchor 5) and a faithful instantiation of scientific peer review
>   (anchor 6). Its sharpest point: independence is *recorded, not claimed* — every review names its
>   reviewer, so how far that reviewer stood from the author is visible, and a different model
>   architecture or a person is available whenever the Maintainer asks for more distance.

`README.md` (each replaces the text at the cited lines):

> Line 10: "read by someone who did not write it — a fresh AI session by default, a different model
> or a person whenever you ask —"
>
> | Independent referees who don't know you | A review by someone who did not write the work; a **different** AI model, or a person, whenever the maintainer asks |
> | Conflict-of-interest rules | Every review names its reviewer, so how far they stood from the author is on the record |
>
> Lines 53-54: "Distance is easier to record — the file names the reviewer, and "a different model
> architecture" is a brighter line than "no recent co-authorship," when you want that line."
>
> Lines 102-104: "- **The reviewer is not the author, and you can see who they were.** Every review is by a
> fresh reviewer, who must answer in writing whether the work should exist as framed and what would
> show it wrong. A different AI model, or a person, reads it too whenever you ask. Who reviewed what
> is written down in your repository, not claimed."
>
> Lines 176-181, figure text: "One review at every stage: a reviewer who did not write the work
> questions its foundations and answers in writing. A different model, or a person, adds more
> distance whenever the maintainer asks." Paragraph: "**This works with one agent.** If you have a
> single AI tool, a fresh session of it is your reviewer at every stage. A second model, or a second
> person, is there whenever you want more distance. You do not need a team to start."

`docs/vision.md`, `docs/glossary.md` and the other descriptive pages reuse these sentences. The
figure `docs/assets/dual-review-independence.svg` is redrawn to match.

**Calls I made near your line**; each stands unless you overrule it.

1. **Per artifact only.** A standing instruction would put External back in the procedure.
2. **The downshift rule stays, scoped.** An orchestrator may run a sub-agent's generative step on a
   cheaper model only if a stronger, different-family model checks the output. That is an optional
   economy, not a review of any proposal, plan or code, and the text now says so.
3. **Complex projects lose the mandatory External read.** They get the one review with the
   scientific-trust lens, a proposal that names the contracts and scientific assumptions it
   touches so you see them before deciding, and the accepted independent scientific check once
   that lands. Simple projects get the one review with a thinner evidence plan.

**What this change owes you.** A Security Review (it touches a frozen gate test and the fidelity
manifest's sample). And a Maintainer-run re-anchor of the gate manifest, which joins the batch
already waiting on the board: 24 frozen files differ from their pinned hashes today. This change
adds one deletion (five test nodes).

### Questions for the Maintainer

Each has my default. An unanswered question takes it.

1. **Capability floors, keyed to stages.** The model-selection table names "External Review"
   (high) and "Internal Review" (medium). Proposed: proposal review **high** (the premise is still
   movable, and a wrong one is cheapest to catch there), plan review **medium**, code review
   **medium**, Security Review **high**. *Default: these four.*
2. **Header words.** `**Review**:` now records only whether a Security Review is owed. Options:
   (a) `usual | usual + Security Review`, with `**Tier**: usual | Security Review`;
   (b) keep `required(Internal)` and `required(Internal + Security Review)`;
   (c) rename the field `**Security Review**: owed | not owed -- <why>`, which needs a board
   column added. `Plan review` keeps its ruled tokens in every option. *Default: (a).*
3. **The headline and the name.** Accept the rewritten anchor and README wording above, and keep
   the name "Dual-Review" and the module id `dual-review` (an install-contract identifier)? "Dual"
   would mean an independent reviewer beside the author at every stage. *Default: yes to both; a
   rename is a separate proposal.*
4. **Who gets the lens roster.** The `dual-review` module holds the nine checks every reviewer
   works through (claims, tests, completeness and so on) and the scope-reduction trap, the rule
   that narrowing a change in review needs your say. It installs only for two-agent-type teams,
   so a solo team gets neither. Changing that edits the engine and the install set. *Default:
   leave it; open a proposal if you want it everywhere.*
5. **The migration.** Nothing is rewritten. A legacy `(External)` label on a pass nobody called
   is read as the usual review, and the `board-as-basis` Decision reads its External-labeled pass
   that way unless you say you called for it. *Default: ratify.*

### 1. One stance, three stages

Every review has one stance: **on the work's side, making it better by questioning its
foundations.** No agent chooses a stance, and there is no tier to select. The table above sets the
stage's questions. **They are required answers, not a mood**; without that, "wants it better"
drifts into polishing something that should not exist. Code review keeps its floor, **not the
implementing agent**, and never reopens the Decision; plan review is a fresh-context pass with
one round. A narrowing recommended in review is a scope change under the existing outcome test
(`doctrine/dual-review.md` > "Review expectations — the scope-reduction trap"), and only you
concede it. This restates that rule where reviewers will meet it first; it adds nothing to it.

Each pass opens with a `**Foundations**` block of three lines, each ending in the file, test,
line or command that backs it. For code review, Answer 3 points at the falsification ledger
rather than restating it, so the block adds no second record. The nine lenses stay as the generic
roster but become **where the evidence comes from**, not a second checklist: a lens cited with no
answer resting on it is the "checked" failure the doctrine already names. The coverage line keeps
its two halves (what the answers rest on; what the pass did not cover) and still does not end in
a recommendation for more review. A reviewer reports the risk and the gap; you read the negative
space. The clean-pass trap stays, restated: the thin clean pass deserves skepticism, and a clean
pass with evidenced answers does not. A clean code review still carries a falsification ledger;
"or a confirming second different-agent-type pass" is struck. A brief to a reviewer may state the
stage's three questions: they are the same for every artifact at that stage, so they do not
telegraph a lens. The heading "Review expectations — the clean-pass trap" and its place before
the scope-reduction trap stay, because `bootstrap/tests/test_scope_reduction_trap.py` pins them.

### 2. External is the Maintainer's call, per artifact

An **External read** is a review you called for on a named artifact, outside the usual procedure.
You set the distance or the brief.

* **How you ask**: in chat, or inside a Decision ("also have X read this first"). The call names an
  artifact that exists now. A call that covers artifacts not yet written is a standing call, which
  is a floor; a floor returns only by proposal.
* **How it is recorded**: the pass carries `**Called by**: Maintainer`, followed by your words,
  verbatim and visually isolated, and the same quote in the commit body, as for a scribed
  Decision. A relayed instruction names the relayer. `**Tier**: External` is valid only with that
  line; without it the pass is read as the usual review, label wrong and content counted.
* **What an agent never does**: write `required(External)` or an equivalent in a header; say a
  change "needs" or "floor-requires" one; escalate a code review to one; head a pass External on
  its own; start one without your quoted words; recommend more distance. It may name a risk and
  a gap in the coverage line.
* **A roster you set** (which agent types work the tree, who staffs the one review) is the team's
  shape in `dev/collaboration_agreement.md`. It adds no read and upgrades none, so it is not a call.
* **What distance buys** is information for you, not a rule: a different agent type has different
  failure modes, a person has different knowledge, a try-to-kill brief narrows the pass to that.
  The staffing agent follows your brief, answers the same three questions from that distance, and
  says so.

### 3. Header and record grammar

`**Review**:` takes `usual` or `usual + Security Review` (Question 2, default (a)); it forces the
one decision it still carries. `**Plan review**:` is unchanged: `required(Internal)` or
`required(Internal + Internal Security Review)`. The pass record keeps `**Tier**:` with
`usual | Security Review`, plus `External` only with `**Called by**`. Legacy tokens are read, never
rewritten and never warned: no tool validates them (the lifecycle planner went in `bfe6bbfd`;
`tools/board.py` prints the field as written, `tools/audit_report.py` checks a risk field exists).
This proposal's own header uses the grammar in force today.

### 4. No rule selects more distance

**Two searches, one pinned path set.** Roots: `AGENTS.md`, `README.md`, `doctrine/`, `templates/`,
both `_template.md` files, `dev/agent_collaboration.md`, `dev/collaboration_agreement.md`,
`dev/modules/`, `docs/`, `dimensions/`, `bootstrap/{fidelity-check,UPGRADE,REANCHOR_RUNBOOK}.md`,
`on-ramp/`; `.md`, `.yml` and `.svg` files; archives excluded. Markup characters (`* _` backtick
`>`) are stripped and whitespace collapsed first, so bold and line wraps cannot split a phrase.

* **Search A, the phrasing**: `required(external` | `external[ -](floor|tier|review|reviewer|
  independence|stance|code review)` | `declared-external` | `a human fills` |
  `different-agent-type (pass|round)` | `escalate to the external` | `External Review Norms`,
  case-insensitive. At `d88a14f9`: **35 files, 102 matches**. Controls: both `AGENTS.md` copies match.
* **Search B, the act of selecting**, per paragraph, case-insensitive: a distance term
  `external | different (agent|model|vendor) | another (agent|model) type | second agent type |
  model famil* | architectur* +space+ diverse | diverse (a different | cross-(agent-)type |
  structural(ly) independen* | a human | human or | or a person`
  within 120 characters of a selection term
  `reserved | mandatory | require(d|s) | escalat* | pick | choose | need(s) | warrant(s) | only when |
  preferred | recommended | floor | wants | calls for`. At `d88a14f9`: **55 paragraph hits in 29
  files**. Controls, all of which it matches: `dimensions/complexity.md` (both positions),
  `dimensions/README.md` axis table, `doctrine/roles.md` "A Reviewer tier", `doctrine/plans.md`
  reviewer-identity note, `templates/modules/team-gated/model-selection.md` downshift condition.

Search B cannot decide meaning; the implementer classifies every hit of A and B, and the code
reviewer re-runs both on the reviewed commit. After the change no hit may select a more distant
reviewer: each is the Maintainer-called definition, a staffing fact, a credit comment, a marked
history reference, or noise (`External-repo`, external links).

| Rule that selects distance | Disposition |
|---|---|
| `dimensions/complexity.md`: Simple "reserved for genuinely contract-touching changes"; Complex "mandatory" | Struck. Simple and Complex get the lines in "In plain terms". |
| `dimensions/README.md` axis table: "how often External review is mandatory" | Reworded to review weight and verification depth. |
| `doctrine/roles.md` "A Reviewer tier": External "when the change needs structural independence ... pick the tier from the change's risk" | Struck. One reviewer role; the stage sets the questions. |
| `doctrine/plans.md` reviewer-identity note: "Escalate to the External-review tier"; "Tier ordering. External > Internal" | Struck. |
| Code-review "explicit escalation" in `AGENTS.md` (2), `doctrine/dual-review.md`, `doctrine/plans.md` | Struck. |
| "recommended wherever it can be staffed" (`AGENTS.md` ×2, `doctrine/dual-review.md`) | Struck from the procedure; the information moves to section 2. |
| "External floor on deliberate-lane proposal review"; "External independence lives at the proposal" | Struck. |
| `dual-review` module (shipped and installed copies): "gets an External review in addition" | Struck; the module keeps the lenses, the trap, the ledger and the Maintainer-called read. |
| `model-selection` module and `doctrine/roles.md`: downshift needs a "different model family" | **Carved out** as a cost rule for orchestrated sub-agents: names its own reviewer (the orchestrator's check), says it is not a lifecycle review, and no downshift if none is available. |
| `doctrine/roles.md` "Diversity within tier"; the module's "different architecture preferred" | Reworded: useful distance when you assign or ask; not a default an agent applies. |
| `doctrine/session-routines.md` dispatch: "a declared-External proposal review wants a cross-type dispatch" | Reworded: dispatch follows what you asked, else a same-type fresh session. |
| `doctrine/dual-review.md` "Domain rotation"; the minimal-team lines in `dimensions/` and `doctrine/roles.md` | Kept as staffing facts (who is available to be the one reviewer); reworded so none reads as independence earned or a read added. |
| `bootstrap/REANCHOR_RUNBOOK.md`: the launcher must be read by "an External Security review" | **Unchanged.** You run that ceremony and choose the reader, so no agent selects; editing it is a trust-ceremony change. Named for the Security Review. |

**The reviewer roster after the change**: Human Maintainer, Strategy, Implementation, **Reviewer**
(one role; it carries the post-review neutral briefing that the Internal Reviewer carried),
Security Review, User Agent. "External Reviewer" leaves the roster and the fidelity manifest's
sample, because it is now your call and not a role.

### 5. Capability floors keyed to the stages

`model-selection.md` (and its installed copy) and `doctrine/roles.md` > "Capability floors"
replace the "External Review" and "Internal Review" rows with four stage rows (Question 1).
"Adversarial premise-checking" in the bright-line list becomes "premise-checking", which is
proposal review's question. The mapping file and `scripts/check_model_selection.py` key on
capability tier, not role, so neither changes.

### 6. Migration

Four proposals opened 2026-10-17 declare `required(External)`: `independent-scientific-check` and
`neutrality-and-upgrade-slots` (accepted, in `dev/proposals/`) and the archived sources of the
`maintainer-attention` and `verification-practice` plans. The fifth, `board-as-basis`, declares
Internal but carries an External-labeled pass.

| What | Disposition |
|---|---|
| Archived records | Keep their `External` tokens and passes, as in the 2026-08-24 precedent. |
| The two accepted proposals | Headers stay. Their External and Security passes are the reviews they were. Nothing owes another. |
| The two plans | Headers say `required(Internal)`; unaffected. |
| `board-as-basis` | Header and pass stay; Question 5. |
| Gate manifest | **Joins the queued batch** (`dev/PLANNING.md` > "Re-anchor the gate manifest"), Maintainer-only. At `d88a14f9`, 24 frozen files differ from their pinned hashes and `test_review_and_verification_rules_ship.py` is unpinned. This change adds one deletion, `test_onboarding_review_tiers.py` (five nodes). The re-anchor re-globs `bootstrap/tests/**/*.py`, so the new test and that unpinned test become frozen at that point: both must be final first, or each later edit owes another re-anchor. |
| `test_review_and_verification_rules_ship.py` | Its pin is an absence (`external[- ]by[- ]default`), compatible with this change, but its docstring and failure message still say External code review "is an escalation". The plan rewords both before the re-anchor. The new `AGENTS.md` wording must avoid the phrase "External ... by default" in any form. |
| In-flight work | `maintainer-attention` (C2-C4 landed) touched the plan templates, `doctrine/plans.md`, `doctrine/lifecycle.md`; `2026-10-18-claude-model-mapping-install-path` touches `model-selection.md` and the checker. This change's plan opens after both and rebases on them. |
| Engine comment | `bootstrap/_scaffold/config.py` ("fill its External tier") and `bootstrap/tests/test_presets.py` will be false. Neither is touched here. The plan deposits one board row at its archive. |

### 7. Reaching adopters

Adopters receive `templates/core/AGENTS.md`, the templates and the installed modules, never
`doctrine/`. The rule is written first in `templates/core/AGENTS.md` and the shipped proposal and
plan templates; Cairn's own copies and the doctrine follow. The `dual-review` module installs only
for two-agent-type teams, so it is not the carrier (Question 4).

**What the plan carries** (the per-file list and the test table move there; the searches above are
the authority, not any list). Layers, with counts of prose files: shipped sources and Cairn's own
copies 24 (the `AGENTS.md` pair; two proposal and two plan templates; four collaboration files;
three modules with their installed copies; the three onboarding presets with two installed
copies and the phase-0 profile; the session-start skill pair); doctrine 8; dimensions 4;
descriptive docs and the figure 10; contract-adjacent prose 2 (`bootstrap/fidelity-check.md`,
`bootstrap/UPGRADE.md`). Tests: retire `test_onboarding_review_tiers.py` (its premise is gone and
its positive check needs exactly three solo-greenfield paragraphs to name their staffing); add
`bootstrap/tests/test_review_stance_in_shipped_files.py`, modelled on
`test_review_and_verification_rules_ship.py`, pinning the obligations and Search A's phrasings and
carrying the retired file's two forbidden wordings; reword the one test above; keep
`test_scope_reduction_trap.py` green unchanged. The plan lists every test file
`grep -rln External bootstrap/tests/` returns, with a disposition for each.

### Not in this proposal

* The engine's staffing gate and its comment (Question 4).
* `bootstrap/REANCHOR_RUNBOOK.md` and credit comments ("per External Review P2-3") in frozen
  scripts. The `first-cross-type-review` trigger matches a vendor name in a review heading, not the
  word External, so it is unaffected.
* Stale text about the removed lifecycle planner in `doctrine/plans.md` and `bootstrap/UPGRADE.md`:
  only their External rows are conformed.

### Rationale

**The doctrine-evolution gate** needs recurrence, or a high-risk classification I do not claim.
The recurrence is one shape: a rule makes External something a tier or an agent selects; you
overrule it for one kind of artifact; it survives in the next. **Five independent rulings** in
eight weeks, plus this direction: (1) 2026-08-24, External plan review retired ("It is not, and
should not ever, be required"), the same day `convergent-lifecycle`'s Decision waived the plan
floor; (2) 2026-09-01 `d98b4c19`, "We cannot require an External type review, ever", recorded
"because the rulings kept being re-made"; (3) 2026-10-01 `adopter-path-consolidation`, "External
floor waived"; (4) 2026-10-18 `b712020d`, "No external by default"; (5) 2026-10-18 `board-as-basis`
declared below the floor while its reviewer ran External anyway. No tracker holds the shape; the
only window pinned in the tree is 14 days (`dev/measurement/review-floor-deviations.md`), and (4)
and (5) both fall inside it. Each earlier fix removed External from one artifact kind: plan, then
type, then code. This removes the last place and the selectability, which is why it should be the
last. It adds no tier, escalation or checker.

**Why keep the questions.** The External passes changed designs: the `board-as-basis` pass
answered "Should it land? Yes, in a narrower form", and the author took its rejected alternative.
The value was the questions, not the label. As required answers at every stage they keep the value
and remove the choice, and extra distance costs you one sentence when you want it.

### Alternatives considered

* **Strike only the selection points and keep two stances.** Smaller; touches neither the anchor
  nor plan and code review. Rejected (the reviewer's alternative): proposal review would default to
  the stance that works inside the frame, and the record says the stances differ in *verdict*, whether
  the change should happen at all. The minimal version would quietly drop that verdict.
* **Split into two proposals (removal now, stages later).** Rejected for the same reason: the first
  half alone leaves proposals with the weaker review until the second lands.
* **Keep External as an agent-chosen tier "when risk warrants".** The current rule, and the source of
  the recurrence.
* **Allow standing Maintainer instructions.** Rejected: a standing call is procedure (Response, ES1).
* **Delete the External word.** Rejected: you need a word to ask with, and the record needs one to
  show you did.
* **`standard` as the header token.** Rejected: it collides with the lifecycle's "standard lane".
* **Make the questions optional guidance.** Rejected: that is the mood version.
* **Do nothing.** A sixth ruling, and adopters keep receiving `required(External)` and "a human
  fills the External tier" with no one to fill it.

### Evidence / verification plan

Searches A and B (section 4), with their controls. Falsifiers: a shipped template that offers
`required(External)`; a shipped sentence saying a type or a person "fills" an External tier; any
rule telling an agent to escalate to, declare or recommend External. Smoke checks:
`python scripts/claim_check.py` and `python scripts/check_cairn.py` over every changed file;
`python scripts/quality_gate.py --sub neutrality`; `python bootstrap/scaffold.py --manifest`
diffed before and after (no path added or removed); `python bootstrap/check_module_body_coverage.py
--target . --cairn-root .`, which reports 8 missing topics today and must not report more; a
scratch install grepped for the forbidden phrasings. **Boundary B is `full`**: the gate manifest
fixture and the fidelity manifest are contract surfaces, so bounded mode refuses.

#### Security preflight

* **S1 — Who supplied it?** Three decisions. *Is this pass External?* Its input is the
  `**Called by**` quote, written by the pass's own author, which is the thing being classified, and
  supplied by value. Nothing authenticates it. *Does shipped text conform?* The new test reads the
  repository's tracked files; a contributor can change a file and its test together. *Does the gate
  accept the dropped nodes?* That is the Maintainer's re-anchor, outside any agent.
* **S2 — Can it fail?** The new test: delete the Maintainer-called obligation from a copy, or add
  `required(External)` to a template copy, and it must go red. The implementing change runs both
  beside an unmutated control and records them; I have not, because the test does not exist yet. Its patterns are literals, not derived from the files they check.
  Retiring the old test is checked by reintroducing each of its two removed wordings into a preset
  copy and watching the new test fail. **The Called-by check cannot fail mechanically**: it is a
  reader reading a record, and I say so rather than imply a gate.
* **S3 — What fires it, over what?** `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests`, over
  the shipped sources the test lists. Adopters do not receive the test; in their tree the rule is
  one sentence in `AGENTS.md` and the check is a reader. The plan quotes the final adopter-facing
  sentence and shows it agrees with this paragraph.
* **S4 — Which way does it break?** A pass headed External with no quote is read as the usual
  review: less distance claimed, no authority gained. An unrecognized `Tier` value is read as the
  usual review. A missing obligation turns the test red, which is closed. After this change nothing
  conditions a transition, waiver or exemption on External, so no failure path grants more authority.
* **S5 — Who still wins?** Assumed: a contributor or agent with commit access to an artifact. One
  who forges a `Called by` quote, or a Maintainer relay, still succeeds: this change adds no
  signature. The class is closed by enumeration (a reader checking attribution, and you at the
  Decision), the same exposure as a scribed Decision's quoted authorization. The consequence is
  bounded: the label adds a read and waives none. Weakening shipped rule text in words the
  test's patterns do not match also still succeeds; that is closed by enumeration, not by construction.

### Signals the change is wrong

* **You ask for External reads on most proposals.** The option is carrying the load the floor
  carried. Reintroduce a floor on purpose, by proposal.
* **Reviews read as polish.** Counted from the first pass under the rule: across the next ten
  proposal reviews, if every Answer 1 is a plain "yes" and the author adopts no review's
  alternative, log it in the incident tracker (`dev/modules/incident-trackers.md`) and put it to
  you. The tally is one grep over the `Should this happen as framed?` lines.
* **A defect ships that a more distant read would plausibly have caught** and no one had asked for
  one. Audit it against the actual finding.
* **An agent writes External in a header or an escalation sentence again.** Search A and the new
  test should have caught it; check them too.

### Scope delta

**Scope delta**: preserved. Every opening outcome is delivered: no agent selects External; you
call it outside the usual procedure; the record shows it was your choice; Security Review,
plan review and the code-review floor are unchanged; migration, tests and the shipped copies are
covered. The standing-instruction route offered in the opening is an option within the second
outcome, withdrawn because it contradicts your quoted words (Response, ES1). Moving the per-file list and
test table to the plan removes no work, only its enumeration here.

### Assurance path

**Assurance path**: high-assurance. It edits governing doctrine, the authoring templates and a
framework anchor, retires a frozen gate test, and touches the fidelity manifest's prose. The
engine package is untouched, so there is no AST impact. A Security Review is owed on this revision.

### Withdrawn / superseded commitments

* The standing-instruction route (opening section 3): withdrawn; it contradicts "outside of the usual procedure".
* `**Review**: required(Internal)` and `**Plan review**: required(Internal)`: superseded by the Security Review declarations.
* "No Security Review is owed" and the preflight answer "N/A": withdrawn; the preflight is answered.
* "Keep the token `Internal` because 68 proposals and plans use it": withdrawn; the count was mostly `Plan review` lines.
* "Exactly one `frozen_files` entry changes": superseded by the batch statement.
* The README scope "alt text and the paragraph beneath the figure": superseded by the cited lines.
* The after-check defined by phrasing alone: superseded by Searches A and B.
* "`Diversity within tier` stays as a recommendation" and "recommended wherever it can be staffed": superseded by section 4.
* The migration row about a pin on "An External code review is an escalation": overtaken; what landed was the absence.
* The length note and the per-file document and test tables: moved to the plan.
