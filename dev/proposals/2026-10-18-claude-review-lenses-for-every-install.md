# Every install gets the review lenses and the scope-reduction trap

**Author**: Claude (Strategy)
**Status**: awaiting-review
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
