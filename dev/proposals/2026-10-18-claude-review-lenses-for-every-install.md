# Every install gets the review lenses and the scope-reduction trap

**Author**: Claude (Strategy)
**Status**: awaiting-decision
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

## Response -- Claude (author) -- 2026-10-18

Answers the Internal review at `b16f4607` (REVISE; RL1 blocking, RL2 to RL7 non-blocking). I accept every
recommendation, so no finding is dispositioned *reject*, and nothing here narrows the opened scope. I did not
repeat the review's simulation (a word-for-word move in detached worktrees: manifest identical, 22 test files
green, +86 lines, the LHM staging). I did re-open the citations the findings lean on, and they hold: the stance
proposal at `:422-424`, `:1035`, `:1068`, `:1277`; `doctrine/plans.md:918-930`; module lines `136-144`;
`templates/core/AGENTS.md:272`; `scripts/check_cairn.py:532`; the two precedent plans, which do drain three and
two accepted proposals into one plan.

* **RL1, accept.** The review-stance proposal was **accepted at `58f30d6c`**, not "awaiting Decision". My
  "Sequencing" sentence was stale and its "if rejected" branch is withdrawn. I agree one plan is the better
  order, for three reasons: the wording is written once instead of rewritten in the module and then moved; the
  stance plan's new test is written against the final homes, so my "no frozen file edited" stays true
  instead of resting on a test not yet written; and there is one plan review and one code review. The cost is
  real and goes in front of you as **Question 5**: that plan cannot open until this proposal is decided, and the
  combined plan is bigger. The fall-back order stays written for a "no". The `AGENTS.md` pointer is rebased to
  the accepted stance text (the lenses are where the evidence for the three answers comes from).
* **RL2, accept, and I pick the doctrine's shape.** One ledger ships: surfaces probed; a negative or edge-case
  attempt; verification; residual risk; and mutation when a claim names a set. Why that one and not the
  module's four items: the doctrine is the canonical source and the module is the derived subset; the
  mutation rule already ships in every `AGENTS.md` (`:272`), so a ledger without it would be a third
  definition; and the module's "failure modes tested" is covered by the negative-attempt item. The module's
  one good sentence stays (a reviewer who tried to break it and could not has cleared the gate; one who only
  read it has not). `doctrine/plans.md:918` points at a heading, "Review Expectations", that exists in neither
  copy of `dev/agent_collaboration.md`; the plan retargets it to "The review sweep". **Plan work only: this
  commit edits no doctrine.** That paragraph is already struck by the stance plan ("or a confirming second
  different-agent-type pass"), so it is one edit in one place.
* **RL3, accept.** I said 60 lines; the review measured +86 word for word. Corrected to 85 to 95, and the
  signal is recast on what it guards, doctrine reasoning leaking into installed text.
* **RL4, accept.** My advice would have left LHM with two ledgers and two clean-pass statements. Reworded
  below; the signal now counts duplicate definitions; the sweep gains one sentence inviting project-specific
  probes after the nine. Body text, not a slot: a new slot adds an unfilled-slot finding to every install.
* **RL5, accept.** The "binds non-trivial changes only" sentence was in my signals and in none of the shipped
  text. It moves into the sweep and the new test pins it.
* **RL6, accept.** The negative assertion now covers the roster, the citation rule and the ledger labels, and
  the mutant "restore the ledger in the module copy" is added. The body-coverage count stays 8 under a move; I
  now call it a regression check, not evidence of arrival.
* **RL7, accept.** Thinning the module breaks two line-bound citations in the stance proposal's Security
  Review (`:1277`). That record is append-only, so the plan treats the two `check_cairn.py` flags as expected
  until that proposal archives (the checker skips archives), and thins the module in its last chunk.

**Does the revision widen scope?** No second round is owed. Revision 1 adds a single-shape ledger, a scope
sentence, a project-probes sentence, one doctrine pointer fix and test assertions. Each is a reviewer
recommendation the review read, none is an outcome the review could not have seen, and nothing in the opening
is dropped. So **Status goes to `awaiting-decision`.** If a reader sees a widening, the fix is a second pass.

## Revision 1 -- Claude (author) -- 2026-10-18

The complete current contract. It supersedes the opening *Proposal*, *Sequencing and upgrade*, *Rationale*,
*Alternatives*, *Documentation / doctrine surface*, *Evidence*, *Signals*, *Scope delta* and *Assurance path* in
full. *Origin* and *Context* stand as opened. **Declarations**: **Review**: required(Internal), done at
`b16f4607`. **Plan review**: required(Internal + Internal Security Review) for the combined plan (the stance
proposal's declaration binds it; this work adds no security surface and is covered by the stronger one); if
Question 5 is "no", required(Internal). **Assurance path**: high-assurance. **Boundary B**: `full` in the combined
plan, since the stance plan touches contract surfaces; `bounded` is expected only if this runs alone.

### In plain terms

Half of what you asked for is already done: a solo install carries the scope-reduction trap, pinned by a test on
16 surfaces. What it lacks is the nine lenses (the fixed list of categories a reviewer works through), the rule
that each lens **cites what backs it** (a bare "checked" is an incomplete review), the **coverage line** that
ends a review (what was covered, what was not), and the ledger a clean code review must show. Cairn's doctrine
already tells every plan and code review to end with that coverage line, so a solo team is asked for something it
was never given. The fix is text in the review-loop document every install receives, beside the trap, plus a
seven-line pointer in `AGENTS.md`. No new module, no change to who gets which module, no engine, install-list or
published-manifest change.

**What the review changed.** Build this in one plan with the review-stance change (Question 5). Ship one ledger,
not two. The added text is about 90 lines, not 60. LHM keeps its domain probes and drops its duplicate ledger.

### Questions for the Maintainer

Each has my default. An unanswered question takes it.

1. **Put the falsification ledger in the same move, as one definition?** It is the checklist a clean code review
   must show: surfaces probed, a negative or edge-case attempt, verification, residual risk, and mutation when a
   claim names a set. `AGENTS.md` already uses the term; only the module defines it, and Cairn has two versions.
   About 14 lines. *Default: yes, using the doctrine's version.*
2. **Where does the full text live?** The review-loop document, with a seven-line pointer in `AGENTS.md`, which you
   asked to keep lean. *Default: that.*
3. **Add a coverage-line stanza to the proposal and plan review scaffolds?** *Default: no.* The line is defined
   once in the review-loop document; the scaffolds can cite it later.
4. **Run the real upgrade on LHM and modflow_tools?** *Default: no.* The plan rehearses on scratch copies. LHM's own
   `AGENTS.md` makes its review-loop document Maintainer-gated, so the merge there is yours.
5. **Build this and the review-stance change in one plan?** That change was accepted today and has no plan yet.
   One plan means the lens wording is written once, in its final place, and reviewed once, and a new test cannot be
   written against wording this change then moves (which would mean editing a pinned test file and a re-anchor).
   The costs: that plan cannot open until you decide this proposal, and it gets bigger. *Default: yes.* Say no and
   the review-stance plan goes first; this one follows.

### Proposal

Proposed paths:
* `bootstrap/tests/test_review_sweep_ships.py` — the new test

1. **"The review sweep" joins `templates/core/dev/agent_collaboration.md`**, before the trap paragraph so "the
   mirror" has its referent. Body text, not a slot. Contents: the clean-pass statement; the nine lenses as the
   generic, change-agnostic roster, written as **where the evidence for a review's three answers comes from**
   (the accepted stance wording), not a second checklist; the **scope sentence** (the sweep applies to the reviews
   the lifecycle calls for; a trivial change with no review owes none); the citation rule; the two-part coverage
   line, which does not end in a recommendation for more review; "a floor, never a downgrade of a declared tier";
   one sentence inviting project-specific probes after the nine; and the ledger in the doctrine's shape. About 85
   to 95 lines (the review measured +86 word for word); the document goes from 152 to about 240.
2. **`AGENTS.md` gains a pointer** in "Review", about 7 lines. Draft wording, to be fitted to the stance's
   "Review" text in the same plan; the test pins the obligations, not the sentences:

   > **Every review shows its evidence.** The three answers a review owes rest on the nine standing lenses in
   > `dev/agent_collaboration.md` > "The review sweep". A lens a review cites names the file, test, line or
   > command that backs it (a bare "checked" is an incomplete review), and the coverage line that ends the
   > review says what the pass did not cover. A reviewer who recommends narrowing the work states what is
   > lost and why the narrower change still reaches the cause; only the Maintainer concedes a loss.
3. **The module keeps what is about multi-type teams.** `templates/modules/team-gated/dual-review.md` drops the
   roster, the citation rule and the ledger for a two-line pointer (152 to about 84 lines). Its trap and
   outcome-test paragraphs **and the "scope-cut means claim correction" clause** stay: the frozen
   `test_scope_reduction_trap.py` pins that clause, and the review's mutant (delete it) fails exactly that node.
   Id, gate and install path do not change. The plan thins the module in its **last chunk**.
4. **Cairn's own copies follow**: `AGENTS.md`, `dev/agent_collaboration.md`, `dev/modules/dual-review.md`.
5. **Doctrine, as plan work.** `doctrine/dual-review.md` > "Adaptation" gets two sentences (the sweep and the trap
   are no longer team-gated). `doctrine/plans.md:918` is retargeted from "Review Expectations" to "The review
   sweep". No rule changes, only where it ships and a pointer that now resolves. `doctrine/plans.md` is already in
   the stance plan's doctrine list, so the combined plan gains no file.
6. **One new test**, `test_review_sweep_ships.py`. *Positive*: install `solo-greenfield` through the real CLI and
   assert the installed loop document carries all nine lens labels, the scope sentence, the citation rule, both
   coverage-line halves and the ledger's five labels, and the installed `AGENTS.md` the pointer; the same over the
   four source surfaces. *Negative*: the module carries none of the lens labels, the citation rule or the ledger
   labels.

**Not in this proposal**: the engine; profiles and presets; `bootstrap/BOOTSTRAP.md`; the proposal and plan
templates (Question 3); `README.md` and `docs/`; retiring the module's duplicate trap paragraphs and their pins
(the plan deposits one board row at its archive).

### Order of work and upgrade

**One plan, two source proposals** (Question 5, default yes). The plan opens when this proposal is decided,
keeping the rebase conditions the stance proposal already names. **If "no"**: the stance plan runs first and this
one follows on its text. Then, if the stance test pins module wording that item 3 moves, and the Maintainer's
re-anchor has already frozen that test, editing it adds one entry to the next re-anchor batch. The plan states
which case it is in.

**Expected checker flags.** Thinning the module breaks two line-bound citations in the stance proposal's Security
Review (`dev/proposals/2026-10-18-claude-external-is-a-maintainer-stance.md:1277`, citing module lines 132-133 and
131-132). `check_cairn.py` will report both until that proposal archives, since it skips archives. They are
expected; the plan records them and does not edit the append-only record.

**Reaching installed trees** is the three-way merge on `upgrade --stage` then `--apply` (`bootstrap/UPGRADE.md`).
modflow_tools merges clean. For LHM the review's rehearsal shows the sweep and ledger arriving **above** the
existing conflict with no markers of their own; the conflict is LHM's own clean-pass list, ledger, briefs and
restricted-verification text against nothing upstream. So the advice is: take the core sweep, **keep LHM's domain
probes** (units and coordinate systems, HDF5 quantization, the MATLAB and MODFLOW boundaries), which now have a home
in the project-probes sentence, and **drop LHM's duplicate ledger and clean-pass statement**. A tree with no
lockfile gets a by-hand diff (`--init-lock`). A tree that never runs `upgrade` gets nothing. A slot would freeze
the roster at its first paste, which is why this is body text.

### Rationale

The outcome is that an agent in any install reads the lenses when it reviews. Agents are sent to `AGENTS.md` and
the review-loop document; the adopter evidence (5 hits in the module, 0 in each of the other two, in both trees)
shows nobody carries a module's text there. So the question is only the cheapest carrier. The *AST baseline* is the
committed fingerprint of the engine's top-level definitions; a symbol outside the four allowlisted ones needs a
Maintainer-run correction.

| Option | Engine and AST baseline | Install set, manifest, lockfile | Reaches an installed tree? |
|---|---|---|---|
| **(b) core text** (recommended) | none | none; `--manifest` byte-identical (measured by the review) | yes, three-way merge |
| (a1) `dual-review` default-on, in place | `_DEFAULT_ON_MODULES`, `_TEAM_STAFFING_GATES`, `_TEAM_STAFFING_GATED` (`bootstrap/_scaffold/config.py:82`, `:1325`, `:1334`) outside `_UPDATE_ALLOWLIST` (`bootstrap/tests/_ast_attest.py:143`); `bootstrap/_scaffold/upgrade.py:1087` would make `init-lock` infer a multi-type team everywhere | +1 file per install; frozen `test_presets.py` and `test_onboarding_seed_roster.py` assert a team without two agent types gets none | no: opt-in, and a manual paste |
| (a2) file moved to `default-on/` | as (a1), plus `_MODULE_MAPPINGS` | as (a1), plus the manifest source column; both adopters' locks name the old path | no |
| (c) new default-on module | `_MODULE_MAPPINGS` (allowlisted), `_DEFAULT_ON_MODULES` (not) | new id, new manifest rows | no: opt-in; a slot never updates |
| (b') one new core file | `_CORE_MAPPINGS` (allowlisted) | +1 manifest row | yes, auto-added |

**Why (b).** It delivers the outcome in the files agents read, travels by the path core text already takes, and
leaves the install contract alone; the review checked the engine citations and found no cheaper carrier. (b') only
spares LHM a merge it already has, and costs a published-manifest row and splits one subject across two files. The
module stays: its id is install contract, and thinning it further is a follow-on.

### Alternatives considered

* **(a1), (a2), (c), (b')**: above.
* **Do the stance plan first, then this one** (my opening order). Lost to RL1: it writes the same text twice and
  risks editing a pinned test; it is the fall-back for Question 5.
* **Keep the module's four-item ledger.** Lost: it is the older shape and lacks the mutation line `AGENTS.md`
  already requires.
* **Point solo teams at the doctrine, or put the full text in `AGENTS.md`.** Lost: `doctrine/` is not installed;
  about 90 lines do not belong in the file you asked to keep lean.
* **Do nothing.** A solo team keeps being asked for a coverage line it was never shown.

### Documentation / doctrine surface

Routed by `docs/DOCUMENTATION_PLAN.md`: prescription goes to the governing layer. **Edited**: the six prose files
of item 1 to 4 (`templates/core/AGENTS.md`, `AGENTS.md`, `templates/core/dev/agent_collaboration.md`,
`dev/agent_collaboration.md`, `templates/modules/team-gated/dual-review.md`, `dev/modules/dual-review.md`) and, as
plan work, `doctrine/dual-review.md` and `doctrine/plans.md`. **New**: the test. **Untouched**: every
`bootstrap/_scaffold/` file (**no AST impact**), `bootstrap/tests/fixtures/gate_manifest.json`,
`scaffold_ast_baseline.json`, the profiles, the proposal and plan templates, `README.md`, `docs/`. **Frozen files**
(pinned by hash in `gate_manifest.json` > `frozen_files`): this work edits none, **in the one-plan order**, because
the stance test is written against the final homes. In the fall-back order that holds only if the stance test pins no
module wording this moves (Order of work). Seven frozen files exercise these surfaces and must stay green unedited:
`test_scope_reduction_trap.py`, `test_presets.py`, `test_onboarding_seed_roster.py`, `test_scaffold.py`,
`test_profiles_smoke.py`, `test_loop_fidelity_gate.py`, `test_verification_boundaries.py`. The new test joins your next
re-anchor batch and must be final before it.

### Evidence / verification plan

Falsifiers: a fresh `solo-greenfield` install lacking a lens label, the scope sentence, the citation rule, either
coverage-line half, a ledger label or the `AGENTS.md` pointer; the module carrying any of them; or
`scaffold.py --manifest` differing before and after.

#### Tests required

* **New**: `test_review_sweep_ships.py` (above), through the real install path, with literal patterns that are not
  derived from the files they check.
* **Mapped, unedited**: the review found 22 test files that read these files and ran them on a simulated change
  (625 passed): the plan maps those, led by `test_scope_reduction_trap.py`, `test_verification_boundaries.py`
  (forbids Cairn-only tokens in the adopter `AGENTS.md`, so the pointer names no `bootstrap/tests` path),
  `test_review_and_verification_rules_ship.py`, `test_loop_fidelity_gate.py`, `test_scaffold.py`,
  `test_profiles_smoke.py`, `test_presets.py` and `test_onboarding_seed_roster.py`.
* **Mutations, each beside an unmutated control**, each of which must turn the new test red: delete lens 4; delete
  the "Not covered" half; delete the scope sentence; restore the roster, then the citation rule, then the ledger,
  in the module copy.

#### Examples / smoke checks

`claim_check.py` and `check_cairn.py` over every changed file (two expected flags, above);
`quality_gate.py --sub neutrality` (pre-existing failures under `templates/skills/` before and after, none new);
`scaffold.py --manifest` diffed before and after; the control grep rerun on a fresh solo install; and the
Question 4 rehearsal on scratch copies of both adopters, checking each staged merge for a duplicate roster, ledger or
clean-pass statement. `check_module_body_coverage.py` stays at 8 missing topics under a move: a regression check, not
evidence the text arrived; the new test and the install grep are the evidence.

##### Security preflight

N/A: no trust boundary added, moved, or widened. Prose, and one test that reads tracked files.

### Signals the change is wrong

* A staged merge for either adopter holds **two definitions of the roster, the ledger or the clean pass**, or a file
  that merges clean today conflicts outside the review-loop region.
* The added text restates the staged evidence bar, the ritual signal or don't-telegraph-the-lens: the doctrine's
  reasoning is leaking into installed text.
* Coverage lines converge on "all lenses swept, clean" across trivial and complex changes (the ritual signal in
  `doctrine/dual-review.md`). Log it in the incident tracker.
* A solo team runs the sweep on trivial changes: the scope sentence is not doing its job.

### Scope delta

**Scope delta**: preserved. The baseline is your two items. The trap already reaches every install and stays
pinned; the lenses, citation rule and coverage line reach every install through this change. The ledger, the scope
and project-probes sentences, the doctrine pointer fix and the extra test assertions are additions, so declining any
is not a reduction.

### Assurance path

**Assurance path**: high-assurance, unchanged. The trigger is governing text: this edits `doctrine/` and the
`AGENTS.md` every adopter receives. It is **not** the engine, the install contract, a trust root or anything an adopter
executes. In the combined plan the stance proposal's Security Review obligations apply to the whole plan. If you
choose (a) or (c), the engine is touched and a revision makes this `required(Internal + Security Review)`.

### Withdrawn / superseded commitments

* "Waits for the review-stance plan; its plan opens when that plan has archived": superseded by one plan (Question 5),
  kept as the fall-back.
* "Revision 1, awaiting Decision" for the stance proposal, and "if that proposal is rejected, this one moves today's
  text": withdrawn; it was accepted at `58f30d6c`.
* "Frozen files: none edited" stated unconditionally: made conditional on the order (Documentation surface).
* The module's four-item ledger as the shape to ship: superseded by the doctrine's five items.
* "About 60 lines; 152 to about 212": superseded by 85 to 95 lines, 152 to about 240.
* The signal "the plan's added text passes about 80 lines": recast on doctrine reasoning leaking into installed text.
* The signal "two rosters": widened to two definitions of the roster, the ledger or the clean pass.
* "Keep theirs, fold in the roster, or adopt the core text" (LHM): superseded by keep LHM's domain probes, drop its
  duplicate ledger and clean-pass statement.
* The claim that a solo team "binds non-trivial changes only" as a signal: now a sentence in the shipped sweep.
* `**Plan review**: required(Internal)` and "Boundary B expected `bounded`": superseded by the combined plan's
  declarations; both stand only if Question 5 is "no".
* The `AGENTS.md` pointer "It works the nine standing lenses": rebased to the accepted stance wording.
