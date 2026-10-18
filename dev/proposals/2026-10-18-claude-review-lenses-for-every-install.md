# Every install gets the review lenses and the scope-reduction trap

**Author**: Claude (Strategy)
**Status**: revising
**Review**: required(Internal) — the recommended option touches no engine file, install-contract surface or trust root; options (a) and (c) below would make it `required(Internal + Security Review)`
**Plan review**: required(Internal)
**Opened**: 2026-10-18

## In plain terms

You said every team should get the nine review lenses and the scope-reduction trap, whatever
its shape. One correction first: **half of this is already done.** I installed the solo preset
into a scratch folder. The trap is there (in `dev/agent_collaboration.md`, `AGENTS.md`, both
templates and the planning board), and a test pins it on 16 surfaces. What a solo install
lacks is the other half:

* the **nine lenses**, the fixed list of categories every reviewer works through (claims,
  tests, completeness, silent failure and so on);
* the rule that each lens **cites what backs it** (a file, test, line or command), so
  "checked" alone counts as an incomplete review;
* the **coverage line** that ends a review: what was covered, and what was not.

Cairn's own doctrine already tells every plan review and code review to end with that coverage
line, and a solo install is never shown it. A solo team is asked for something it was never given.

**The change.** Put the lenses, the citation rule, the coverage line and (Question 1) the
ledger in the review-loop document every install already receives, next to the trap, with a
six-line pointer in `AGENTS.md`. No new module, no change to who gets which module, and no
change to the engine, the install list or the published manifest.

**For LHM and modflow_tools.** Both have the `dual-review` module, yet neither has the lens list
where an agent reads it: it sits in `dev/modules/`, and nobody pasted it into `AGENTS.md` or
`dev/agent_collaboration.md`. They get the change through the ordinary `upgrade`. LHM's
`dev/agent_collaboration.md` already conflicts with Cairn today, so it is a by-hand merge for
LHM whether or not this lands. **Order:** this waits for the review-stance proposal's plan,
because both rewrite the same paragraphs.

## Questions for the Maintainer

Each has my default. An unanswered question takes it.

1. **Put the falsification ledger in the same move?** It is the four-part record (edge cases
   probed, failures tested, what was run or consciously not, what stays unverified) a clean code
   review must show. `templates/core/AGENTS.md:256` already uses the term and the review-stance
   proposal's code-review answer points at it, but only the module defines it. About 12 lines.
   *Default: yes.* Say no and it stays in the module, undefined for solo teams.
2. **Where does the full text live?** The review-loop document, with a six-line pointer in
   `AGENTS.md`, which you asked to keep lean. *Default: that.*
3. **Add a coverage-line stanza to the proposal and plan review scaffolds?** The review-stance
   plan already rewrites those authoring templates' review blocks. *Default: not here; this change
   defines the line, that plan can use it.*
4. **Run the real upgrade on LHM and modflow_tools?** *Default: no.* The plan rehearses on scratch
   copies and reports what conflicts; the upgrades stay yours to run.

## Origin

The Maintainer, answering Question 4 of the review-stance proposal (relayed by the coordinating
session), quoted verbatim:

> "Everyone should get them"

That question said a solo team "gets neither". For the trap that is not so, as shown below.

## Context

**What a solo install holds today** (`solo-greenfield` into an empty folder, at `58f30d6c`):

| Piece | Solo install | Evidence |
|---|---|---|
| Scope-reduction trap | **yes** | grep `scope-reduction trap`: `dev/agent_collaboration.md`; `Scope delta`: `AGENTS.md`, `dev/PLANNING.md`, both templates. `bootstrap/tests/test_scope_reduction_trap.py` pins it on 16 surfaces |
| Nine lenses | no | grep `Name the satisfier`, `Silent failure`, `Cross-document consistency`: no file |
| Citation rule, coverage line | no | grep `Falsifiable coverage`, `coverage line`: no file |
| Falsification ledger | no | `falsification ledger` appears in `AGENTS.md` only, undefined |

The control: the same patterns all match `templates/modules/team-gated/dual-review.md`, so the
empty results are absences, not a dead search.

**The shipped text points at what it never defines.**

* `templates/core/dev/agent_collaboration.md:74` opens "The clean pass has a mirror: the
  scope-reduction trap" and asks for "the same skepticism as a clean pass". A solo install never
  states the clean pass.
* `doctrine/plans.md:732` and `:932` require every plan review and code review to end with the
  coverage line, built from "review-sweep lenses swept". Nothing in `templates/core/` describes it.

**Installing the module does not deliver it.** `dual-review.md` has no merge directive
(`grep -c cairn:merge-target` returns 0); its "Merged into" block is a manual paste. LHM and
modflow_tools both lock `dual-review`, and in both the lens text is in `dev/modules/dual-review.md`
and nowhere in `AGENTS.md` or `dev/agent_collaboration.md` (grep: 5 hits, then 0 and 0).

**Rehearsal, read-only.** I copied each adopter's `dev/`, `AGENTS.md` and `CLAUDE.md` to a scratch
folder and ran `upgrade --plan` and `--stage` against Cairn at `58f30d6c`. The copies are partial, so
"file missing" noise is mine. For the three files that matter: LHM's `AGENTS.md` merges clean,
`dev/agent_collaboration.md` **conflicts**, the module is untouched; modflow_tools merges all three
clean. The LHM conflict is 118 lines of LHM's own text (clean-pass trap, falsification ledger, briefs,
restricted verification) against nothing upstream. The trees are 181 and 167 commits behind.
Separately, LHM lists `documentation-plan` and `security-verification` as "new modules available
(opt-in)"; both are default-on today. **A module made default-on later does not reach an installed
tree by itself.**

## Proposal

Proposed paths:
* `bootstrap/tests/test_review_sweep_ships.py` — the new test

1. **"The review sweep" joins the review-loop document** (`templates/core/dev/agent_collaboration.md`,
   about 60 lines, before the trap paragraph so "the mirror" has its referent): a one-paragraph clean-pass
   statement; the nine lenses as the generic, change-agnostic roster; the citation rule; the two-part
   coverage line, which does not end in a recommendation for more review; "a floor, never a downgrade of a
   declared tier"; and, per Question 1, the ledger. It carries the text **as the review-stance plan leaves
   it**, not today's. The document grows from 152 to about 212 lines.
2. **`AGENTS.md` gains a pointer** (`templates/core/AGENTS.md`, in "Review"; about 6 lines, 419 to about
   425). The wording this change would install:

   > **Every review reports what it swept.** It works the nine standing lenses in
   > `dev/agent_collaboration.md` > "The review sweep" and ends with a coverage line: the lenses
   > covered, each backed by the file, test, line or command that supports it (a bare "checked" is an
   > incomplete review), and what the pass did not cover. A reviewer who recommends narrowing the work
   > states what is lost and why the narrower change still reaches the cause; only the Maintainer
   > concedes a loss.
3. **The module keeps what is about multi-type teams.** `templates/modules/team-gated/dual-review.md`
   drops the roster, the citation rule and the ledger for a two-line pointer; it shrinks from 152 to about
   90 lines. Its trap and outcome-test paragraphs **stay byte-compatible** with `test_scope_reduction_trap.py`,
   a frozen file. That test's pattern for "scope-cut means claim correction" matches a clause that sits
   inside lens 9 today, so the plan keeps the clause beside the trap. Its id, gate and install path do not
   change.
4. **Cairn's own copies follow**: `AGENTS.md`, `dev/agent_collaboration.md`, `dev/modules/dual-review.md`.
5. **Two doctrine sentences.** `doctrine/dual-review.md` > "Adaptation" says "the review *apparatus* is
   team-gated"; the sweep and the trap no longer are. No rule changes, only where it ships, so I do not
   claim the recurrence the rate-limit gate asks of a new rule: your Decision is the authorization. The
   deep why (the staged evidence bar, the ritual-going signal, don't telegraph the lens, the outcome test
   in full) stays in the doctrine and does not move.
6. **One new test**, `bootstrap/tests/test_review_sweep_ships.py`: installs `solo-greenfield` through the
   real CLI into a temp folder and asserts the installed loop document carries all nine lens labels, the
   citation rule, both coverage-line halves and the ledger, and the installed `AGENTS.md` the pointer; the
   same obligations over the four source surfaces; and that the module does not restate the roster.

**Not in this proposal**: the engine; any profile or preset; `bootstrap/BOOTSTRAP.md`; the proposal and plan
templates (Question 3); `README.md` and `docs/`; retiring the module's duplicate trap paragraphs and their
pins (the plan deposits one board row at its archive).

## Sequencing and upgrade

**After the review-stance plan.** `dev/proposals/2026-10-18-claude-external-is-a-maintainer-stance.md`
(Revision 1, awaiting Decision) makes the lenses "where the evidence comes from", strikes "or a confirming
second different-agent-type pass" from the ledger, and rewrites the module and the loop document. Moving
text that is about to be rewritten means writing it twice. This proposal can be reviewed and decided now;
its plan opens when that plan has archived and rebases on what it leaves. If that proposal is rejected,
this one moves today's text and its outcome is unchanged.

**Reaching installed trees.** Both core files travel on `upgrade --stage` then `--apply`, a three-way merge
against the copy of the template the install kept (`bootstrap/UPGRADE.md`). The sweep is body text, not a
slot, and that matters: a slot body is the adopter's and is never updated on upgrade, so delivery through a
slot would freeze the roster at its first paste. Expect a hand merge in LHM's `dev/agent_collaboration.md`,
where its own clean-pass and ledger subsections sit beside the new one: keep theirs, fold in the roster, or
adopt the core text. A tree with no lockfile gets a by-hand diff (`--init-lock`). A tree that never runs
`upgrade` gets nothing.

## Rationale

The outcome is "an agent in any install reads the lenses when it reviews". Agents are sent to `AGENTS.md`
and the review-loop document, and the adopter evidence above shows nobody carries a module's text there. So
the content goes where the reading happens, and the only question is the cheapest carrier. *AST baseline*
below is the committed fingerprint of the engine's top-level definitions; changing one outside the four
allowlisted symbols needs a Maintainer-run correction.

| Option | Engine and AST baseline | Install set, manifest, lockfile | Reaches an installed tree? |
|---|---|---|---|
| **(b) core text** (recommended) | none | none; `--manifest` byte-identical; fidelity manifest and lockfile schema unchanged | yes, a three-way merge of two core files |
| (a1) `dual-review` default-on, in place | `_DEFAULT_ON_MODULES`, `_TEAM_STAFFING_GATES`, `_TEAM_STAFFING_GATED` (`bootstrap/_scaffold/config.py:82`, `:1325`, `:1334`) are in the baseline and **not** in `_UPDATE_ALLOWLIST` (`bootstrap/tests/_ast_attest.py:143`): Maintainer-run. `bootstrap/_scaffold/upgrade.py:1087` reads "module installed" as a multi-type team, so `init-lock` would infer one for every tree | +1 file for every install without two agent types; roster +1; frozen `test_presets.py` and `test_onboarding_seed_roster.py` assert such a team does *not* get the module | no: opt-in via `--adopt-module`, and the module is a manual paste |
| (a2) move the file to `default-on/` | as (a1), plus `_MODULE_MAPPINGS` | as (a1), plus the `--manifest` source column changes; both adopters' locks name `modules/team-gated/dual-review.md`, which would vanish upstream | no |
| (c) split out a new default-on module | `_MODULE_MAPPINGS` (allowlisted) and `_DEFAULT_ON_MODULES` (not): Maintainer-run | new module id, new `--manifest` rows, new roster entry | no: opt-in; a slot-fed version never updates |
| (b') one new core file | `_CORE_MAPPINGS` (allowlisted, self-service) | +1 `--manifest` row, installed everywhere | yes, auto-added with no merge |

**Why (b).** It delivers the outcome in the files agents read, reaches adopters by the path core text already
travels, and leaves the install contract alone. (a) and (c) put the text where the evidence shows it goes
unread, edit the engine, and need a deliberate step per adopter. (b') is the runner-up: it spares LHM a
merge. But LHM's file conflicts today after 181 commits of drift, so the saving is small, and the cost is a
published-manifest row plus splitting one subject (the clean pass, its lenses, its mirror) across two files.
The module stays: its id is install-contract and the review-stance proposal keeps it; thinning it further is
a follow-on.

## Alternatives considered

* **(a1), (a2), (c), (b')** — above.
* **Point solo teams at the doctrine.** Rejected: `doctrine/` is not installed; a reference there is a
  citation, not a file the adopter has.
* **Full text in `AGENTS.md`.** Rejected: about 60 lines in the file you asked to keep lean, for text needed
  at review time rather than at every session start.
* **Do nothing.** A solo team keeps being asked for a coverage line it was never shown, and the stance
  proposal's "improve by questioning" has no standing list of what to question.

## Documentation / doctrine surface

Routed by `docs/DOCUMENTATION_PLAN.md`: prescription goes to the governing layer. **Edited**:
`templates/core/AGENTS.md`, `AGENTS.md`, `templates/core/dev/agent_collaboration.md`,
`dev/agent_collaboration.md`, `templates/modules/team-gated/dual-review.md`, `dev/modules/dual-review.md`,
and `doctrine/dual-review.md` > "Adaptation". **New**: the test above. **Untouched**: every
`bootstrap/_scaffold/` file (**no AST impact**), `bootstrap/tests/fixtures/gate_manifest.json`,
`scaffold_ast_baseline.json`, the profiles, the proposal and plan templates, `README.md`, `docs/`.
**Frozen files** (pinned by hash in `gate_manifest.json` > `frozen_files`): none edited. Seven that exercise
these surfaces or the module roster must stay green unedited: `test_scope_reduction_trap.py`,
`test_presets.py`, `test_onboarding_seed_roster.py`, `test_scaffold.py`, `test_profiles_smoke.py`,
`test_loop_fidelity_gate.py`, `test_verification_boundaries.py`. No re-anchor is owed; the new test joins
your next batch and must be final before it.

## Evidence / verification plan

Falsifiers: a fresh `solo-greenfield` install lacking any of the nine lens labels, the citation rule, either
coverage-line half, or the `AGENTS.md` pointer; or `scaffold.py --manifest` differing before and after.

### Tests required

* **New**: `test_review_sweep_ships.py`, through the real install path (`scaffold.py --config
  bootstrap/profiles/solo-greenfield.yml`), not a helper. Its patterns are literals, not derived from the
  files they check.
* **Mapped, unedited**: `test_scope_reduction_trap.py` (16 surfaces, both module copies among them);
  `test_verification_boundaries.py` (reads both `AGENTS.md` copies and forbids Cairn-only tokens in the
  adopter file, so the pointer names no `bootstrap/tests` path); `test_review_and_verification_rules_ship.py`;
  `test_loop_fidelity_gate.py` (`doctrine/` citations in shipped files carry the allow marker);
  `test_scaffold.py`, `test_profiles_smoke.py`, `test_presets.py`, `test_onboarding_seed_roster.py` (the
  gate is unchanged, so these should not move).
* **Mutations, beside an unmutated control**: delete lens 4 from a template copy; delete the "Not covered"
  half; restore a second roster in the module copy. Each must turn the new test red.

### Examples / smoke checks

`claim_check.py` and `check_cairn.py` over every changed file; `quality_gate.py --sub neutrality`;
`scaffold.py --manifest` diffed before and after; `check_module_body_coverage.py --target . --cairn-root .`
(8 missing topics today, one of them "The coverage line"; it must not exceed 8); the control grep above
rerun on a fresh solo install; and the Question 4 rehearsal on scratch copies of both adopters, recording the
kind of each of the three files and checking the staged merge for a duplicated roster. **Boundary B**:
expected `bounded`, since no contract surface is touched; uncertainty resolves to `full`, interpreter named.

#### Security preflight

N/A: no trust boundary added, moved, or widened. Prose, and one test that reads tracked files.

## Signals the change is wrong

* A staged merge for either adopter holds two rosters, or a file that merges clean today conflicts outside
  the review-loop region.
* The plan's added text passes about 80 lines: the doctrine must stay the deep why.
* Coverage lines converge on "all lenses swept, clean" across trivial and complex changes (the ritual signal
  in `doctrine/dual-review.md`). Log it in the incident tracker.
* A solo team skips the sweep because it reads as heavy. It binds non-trivial changes only; a trivial change
  is made and says so in the commit.

## Scope delta

**Scope delta**: preserved. The baseline is your two items. The trap already reaches every install and stays
pinned; the lenses, citation rule and coverage line reach every install through this change. The ledger
(Question 1) and the doctrine sentences are additions, so declining either is not a reduction.

## Assurance path

**Assurance path**: high-assurance. The trigger is governing text: this edits `doctrine/` and the `AGENTS.md`
every adopter receives. It is **not** the engine, the install contract, a trust root or anything an adopter
executes. A Security Review is not declared, because none of `AGENTS.md`'s high-risk surfaces is touched; if
you choose (a) or (c) the engine is, and the header becomes `required(Internal + Security Review)` in a
revision.

## Review -- Claude Opus 5.5 (Internal) -- 2026-10-18

**Model**: Claude Opus 5.5, a fresh session with no shared context, of the same agent family as the author; no cross-type distance. An Internal pass, taking the stance the Maintainer's accepted review-stance Decision sets for proposal review: should this exist, and is there a better design.

```
Reviewed commit: 2e7f41dfd054f93449cff0afa719c04f491e68e6
Target: the whole proposal, In plain terms through Assurance path; every figure measured in detached worktrees of that commit; LHM and modflow_tools read only
Prior findings: none
Assurance path: high-assurance
```

**Tier**: Internal
**Findings**: raised (1 blocking, 6 non-blocking)
**Verdict**: REVISE

### Verdict in brief

**This should exist, and option (b) is the right carrier.** I tested the "no contract effect" claim by applying a word-for-word version of the change to a scratch copy. The published install manifest came out byte-identical, no frozen file changed, and the 22 test files that read these files stayed green. The trap does already ship to a solo install; the lenses, the citation rule and the coverage line do not. modflow_tools takes the change with no hand-merge. LHM's conflict is the one it has today.

One thing needs an answer before a Decision (RL1): **the order of work.** The review-stance plan, which this one waits for, adds a test that reads the `dual-review` module and is frozen at the next re-anchor. If that test pins any wording this proposal moves out of the module, "no frozen file edited" is false and you owe a re-anchor. The strongest design the proposal did not weigh avoids that and saves a whole plan cycle: **implement both accepted proposals in one plan**, writing the lens text once, in its final home. Cairn has done this twice before.

RL2 to RL7 sharpen the text the plan will write: one ledger shape, not two; a realistic size; LHM's hand-merge advice; two test gaps; one checker side effect.

### Steelman

Cairn's doctrine requires every plan review and code review to end in a coverage line built from "review-sweep lenses swept", and the shipped review-loop document refers to a clean pass it never states. A solo team is held to a rule it was never shown. The proposal puts the missing text in the one document every install has and reviewers already use, adds six lines to `AGENTS.md` to send them there, and leaves the engine, the install list and the published manifest alone. It found the one trap in its own move (the `scope-cut` clause the module test pins), and it rejects slots for the right reason: a slot body belongs to the adopter and never updates. The adopter evidence (in both science repositories the lens text sits unread in `dev/modules/`) shows why the module could not be the carrier.

### Foundations

* **Should this exist? Yes.** You asked for it ("Everyone should get them", recorded in the Decision at `58f30d6c`). The shipped text already points at what it never defines: `templates/core/dev/agent_collaboration.md:74` (the clean pass) and `templates/core/AGENTS.md:256` (the falsification ledger), against `doctrine/plans.md:732` and `:932`. A fresh `solo-greenfield` install at `2e7f41df` contains none of `Name the satisfier`, `Silent failure`, `Cross-document consistency`, `Falsifiable coverage` or `coverage line`; the same patterns all match the module (the control). The payoff today is LHM and modflow_tools, whose agents never read the module file; future installs get it from day one.
* **Is there a better design? For the carrier, no; for the order of work, yes.** (b) is the least contract change that reaches installed trees. I checked the engine citations in the options table (`bootstrap/_scaffold/config.py:82`, `:1325`, `:1334`; `bootstrap/tests/_ast_attest.py:143`; `bootstrap/_scaffold/upgrade.py:1087`) and found no cheaper carrier the author missed. The better order is RL1: one plan for both proposals.

### Findings

#### RL1 -- BLOCKING: waiting for the review-stance plan carries a frozen-file risk, and one plan is the cheaper order

**Plain:** the plan this one waits for will add a test that reads the module this one thins, and that test will be frozen before this plan runs. Doing both changes in one plan avoids the clash and writes the lens text once.

* The stance proposal's accepted text adds a test, `test_review_stance_in_shipped_files`, that "reads both `AGENTS.md` copies, the two templates, the `dual-review` module and the onboarding presets" (`dev/proposals/2026-10-18-claude-external-is-a-maintainer-stance.md:422-424`). Its gate-manifest row says the re-anchor re-globs the tests, so that test becomes frozen (`:1068`). The same proposal says "the module keeps the lenses, the trap, the ledger" (`:1035`). A test written to that sentence can pin module wording that item 3 here deletes. Item 3 would then edit a frozen file and owe a Maintainer-only re-anchor. The claim "Frozen files: none edited" is true today (measured below), but it is stated unconditionally about a test not yet written.
* This order does not avoid writing the text twice. The stance plan rewrites the module's lens and ledger paragraphs, then this plan moves them. Either order writes twice; one plan writes once.
* Precedent: `dev/plans/archive/comprehension-outlives-the-artifact.md` drains three accepted proposals into one plan "by Maintainer direction"; `dev/plans/archive/convergent-lifecycle.md` drains two.
* Stale text: "Sequencing and upgrade" calls the stance proposal "Revision 1, awaiting Decision" and plans for its rejection. It was accepted at `58f30d6c`, the commit this proposal's own Context installs from.
* The `AGENTS.md` pointer is quoted as final ("It works the nine standing lenses"), but the accepted stance text makes the lenses "where the evidence comes from, not a second checklist" (`:953-955`). The pointer needs the same rebase as the rest.

**Recommend:** add **Question 5: implement this through the review-stance plan, one plan with two source proposals? Default: yes.** The lens, citation, coverage-line and ledger text is then written once, in the core review-loop document, in the stance plan's wording; the stance test pins it there rather than in the module; and there is one plan review and one code review instead of two. If the answer is no, keep this order but write the contingency into "Documentation / doctrine surface": if the stance test pins module text that item 3 moves, this plan edits that test and adds one entry to the re-anchor batch. Either way, fix the stale sentence and mark the pointer wording as rebased.

#### RL2 -- non-blocking: Cairn defines the ledger twice, and the proposal would ship the older shape

**Plain:** "falsification ledger" has two definitions in Cairn with different items. The one that would ship lacks the mutation line that every installed `AGENTS.md` already asks for.

* The module's shape, which item 1 moves: probed edge cases, failure modes tested, verification run, residual risks (`templates/modules/team-gated/dual-review.md:136-144`).
* The doctrine's shape: surfaces probed, a negative or edge-case attempt, verification, residual risk, and **mutation** when a claim names a set (`doctrine/plans.md:923-930`). The mutation-ledger rule already ships in `templates/core/AGENTS.md:272`.
* `doctrine/plans.md:918` points readers at `dev/agent_collaboration.md` > "Review Expectations", a heading in neither copy of that file. This change creates the heading that pointer needs.

**Recommend:** ship one shape: the doctrine's, or the module's four items plus the mutation line. Have the new test pin its labels. Retarget `doctrine/plans.md:918` to "The review sweep" in the same edit; that adds one doctrine file, as a pointer fix, not a rule change.

#### RL3 -- non-blocking: "about 60 lines" measures at about 85, and the proposal's own signal fires at about 80

* I moved the module text word for word into a scratch copy (lenses, the `scope-cut` clause, the citation rule, a three-line coverage line, the floor sentence, the ledger). `templates/core/dev/agent_collaboration.md` went from 152 to 238 lines (+86); the module went from 152 to 84.
* Getting to 60 means compressing, and compressed text is new wording that should be reviewed as new, not as a move. A line count is also a weak proxy for what the signal guards: the doctrine's deeper reasoning leaking into installed text.

**Recommend:** say 75 to 90 lines, and recast the signal as "the added text restates the staged evidence bar, the ritual signal, or don't-telegraph-the-lens".

#### RL4 -- non-blocking: for LHM, the suggested hand merge leaves two ledgers and two clean-pass statements

**Plain:** in LHM the new text merges in automatically above the conflict, so keeping LHM's side of the conflict keeps a duplicate.

* Read-only rehearsal on a scratch copy of LHM's tracked `dev/`, `AGENTS.md` and `CLAUDE.md`, with the simulated change: `upgrade --stage` places the sweep (lenses, citation rule, ledger) with no conflict at lines 163-248 of the staged review-loop file. The conflict is lines 272-391: LHM's own clean-pass list (five standing checks), its ledger, briefs and restricted-verification text, against nothing upstream. That is the 118-line conflict the proposal reports.
* Keeping LHM's side (the first option the proposal offers) leaves two ledger definitions and two clean-pass statements. The signal the proposal names, "two rosters", does not fire, because LHM's five checks are not the nine lenses.

**Recommend:** reword the advice: the core sweep and ledger arrive above the conflict; keep LHM's domain probes (units and coordinate systems, HDF5 quantization, the MATLAB and MODFLOW boundaries) and drop its duplicate ledger. Widen the signal to "two definitions of the roster, the ledger or the clean pass". Add one sentence to the sweep inviting project-specific probes after the nine, so a list like LHM's has a home. Keep it body text, not a slot: a new slot adds an unfilled-slot finding to every install.

#### RL5 -- non-blocking: a signal relies on a sentence the shipped text does not carry

* "Signals" says a solo team will not find the sweep heavy because "it binds non-trivial changes only; a trivial change is made and says so in the commit". None of the six pieces item 1 lists says so, and the module text it moves reads "a fixed, change-agnostic roster every reviewer works through", with no scope.

**Recommend:** put the scope sentence in the sweep (it applies to the reviews the lifecycle calls for; a trivial change with no review owes none) and have the new test pin it.

#### RL6 -- non-blocking: the new test stops the roster returning to the module, not the citation rule or the ledger

* Item 6 asserts "the module does not restate the roster". The citation rule and the ledger move too, and nothing else would catch them drifting back: `scripts/quality_gate.py --sub redundancy` compares only `doctrine/`, `dimensions/`, `on-ramp/` and `docs/` (`scripts/quality_gate.py:498`), so it cannot see one template repeating another.
* The body-coverage criterion "must not exceed 8" stays at 8 under a word-for-word move (measured before and after). It works as a regression check; it is not evidence the text arrived.

**Recommend:** extend the negative assertion to the citation rule and the ledger labels, and add the mutant "restore the ledger in the module copy" to the three listed.

#### RL7 -- non-blocking: thinning the module breaks two line citations in the stance proposal

* Measured: with the module thinned, `python scripts/check_cairn.py` goes from clean to 2 issues, both line-bounds citations in the stance proposal's Security Review (`dev/proposals/2026-10-18-claude-external-is-a-maintainer-stance.md:1277`, citing lines 132-133 and 131-132 of the two module copies, which would be 84 and 83 lines long). That record is append-only.
* `check_cairn.py` skips archived records unless asked (`scripts/check_cairn.py:532`), so under the proposal's order the flags never appear. That is a second, unstated reason for the order.

**Recommend:** name this effect in "Sequencing and upgrade". Under RL1's one plan, thin the module in the last chunk and record the two flags as expected until the stance proposal archives.

### Measured: the contract claims

* **Frozen files.** None of the six edited prose files, nor `doctrine/dual-review.md`, is in `bootstrap/tests/fixtures/gate_manifest.json` > `frozen_files`; the same search finds `bootstrap/tests/test_scope_reduction_trap.py` (control). Static `python bootstrap/tests/_gate_manifest.py verify --no-collect` on the simulated change reports 50 holds: 25 frozen files already drifted and queued for the re-anchor, none of them touched here.
* **Collection.** No pinned test ID is built from these files' contents. A dropped ID would hold and an added one is allowed (`bootstrap/tests/_gate_manifest.py:672-686`).
* **`scaffold.py --manifest`**: byte-identical before and after. It lists destination, source and mode, no content hash.
* **AST baseline**: engine symbols only; no template path or text appears in `scaffold_ast_baseline.json` or `scaffold_ast_known_new.json`.
* **Fidelity manifest** (`bootstrap/fidelity-check.md`): names `dev/agent_collaboration.md` as a kernel file and `dual-review` as a module; nothing pins their text.
* **Tests that read these files**, found by searching `bootstrap/tests`, `scripts`, `tools` and the engine for each path, then run on the simulated change under Python 3.13: 22 files (the proposal's eight mapped files and `test_comprehension_floor.py`, `test_documentation_plan_module.py`, `test_quickstart_sequence.py`, `test_cairn_prefix_links.py`, `test_check_cairn_content.py`, `test_quality_gate_neutrality.py`, `test_onboarding_review_tiers.py`, `test_manifest.py`, `test_module_roster.py`, `test_module_merge.py`, `test_merge_module.py`, `test_upgrade.py`, `test_lockfile_module.py`, `test_verify_integrity.py`), 625 passed. Unmutated control for the first 14 files: 395 passed before, 395 after. One mutant: deleting the `scope-cut` clause from the thinned module fails exactly that node of `test_scope_reduction_trap.py` (killed), so the proposal's note to keep the clause is load-bearing.
* **Gates.** Neutrality: the same pre-existing failures before and after (all under `templates/skills/`), none new. Redundancy: clean both ways, and blind to templates (RL6). `check_cairn.py`: RL7.
* **The trap ships (check 2).** In the solo install, `scope-reduction trap` is in `dev/agent_collaboration.md`; `Scope delta` is in `AGENTS.md`, `dev/agent_collaboration.md`, `dev/PLANNING.md` and both templates. Confirmed.
* **Upgrade (check 3).** The two lock commits are 181 and 167 behind `58f30d6c`, as stated. modflow_tools, today and with the simulated change: `AGENTS.md` and `dev/agent_collaboration.md` merge clean, the module is "clean (untouched)", and the staged files carry the sweep, the pointer and the thinned module with no conflict marker. LHM: as in RL4; `documentation-plan` and `security-verification` are listed opt-in, as stated.

### Answers to the proposal's four questions

1. **The ledger in the same move:** yes, in one shape (RL2).
2. **Where the full text lives:** the review-loop document, with the pointer. Measured cost to the shipped `AGENTS.md`: 7 lines, about 120 tokens on 6,150.
3. **A coverage-line stanza in the review scaffolds:** agree, not in this change. Under RL1's one plan it lands naturally, since that plan rewrites those blocks.
4. **Real upgrades on LHM and modflow_tools:** agree, no. LHM's own `AGENTS.md` makes its `AGENTS.md`, review-loop document and `dev/modules/*` Maintainer-gated ("Doctrine surfaces stay Maintainer-gated regardless", its line 198), so an agent should not run it there anyway. The scratch rehearsal is enough; I ran it with the change applied and recorded the result above.

### Coverage

* **Covered** -- claims: the contract list, measured on a simulated change with controls (above). Production path: a real `solo-greenfield` install through `bootstrap/scaffold.py`, and real `upgrade --plan` and `--stage` runs. Cross-document consistency: RL1, RL2, RL7 (the stance proposal, `doctrine/plans.md`, `check_cairn.py`). Drift: RL3 (size), RL5 (signals). Lifecycle placement: RL1 (order), Question 4 against LHM's own gate. Test-plan completeness: RL6 and one mutant.
* **Not covered / low confidence** -- below.

### What I did not cover

* I did not run the full suite, or `_gate_manifest.py verify` with collection; Boundary B is the implementation's.
* My simulation moved today's module text word for word. The plan will carry the stance-rebased, possibly compressed text, which does not exist yet. RL1's frozen-file risk is a forecast from the stance proposal's description of its test, not a measurement.
* The adopter rehearsals copied only tracked `dev/`, `AGENTS.md` and `CLAUDE.md`, so their "file missing" noise is mine. I ran `--plan` and `--stage` on the copies, never `--apply`, and changed nothing in either repository.
* I did not draft or judge the `doctrine/dual-review.md` > "Adaptation" sentences, and did not test other interpreters.
