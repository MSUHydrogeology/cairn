# Remove the collaboration agreement

**Author**: Claude (Strategy)
**Status**: awaiting-review
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-19

## In brief

You decided on 2026-06-12 that Cairn no longer needs a collaboration agreement, and on 2026-10-19 that the removal ships in 0.4, after the review-stance plan. This proposal is that removal. I read the tree instead of trusting the board row, and the row is out of date in both directions.

**The row overstates the work in three places.** The `AGENTS.md` required-reading link and the `agent_collaboration.md` pointer are already gone. The "External Review Norms" the row says to re-home were never in Cairn's agreement or in the shipped template (they are in modflow_tools' own copy), so there is nothing to carry across. The review-stance plan removes the last dangling citations of them.

**It understates the work in four.**

1. The agreement is wired into the onboarding helper that adopters run. One of that helper's two goodnight prompts, and one of its triggers, exist only for this file; the other trigger reads the file's team-roster slot.
2. Removing the install row is an engine edit (one list in `bootstrap/_scaffold/config.py`), and the published install manifest loses a row. Both are contract surfaces.
3. The review-stance plan, being built now, added the file's path to six more places and to its tests. This change has to follow it.
4. Cairn's own copy holds one rule that nothing else says: the Maintainer decides a short, fixed list, and escalating anything else is a defect. Deleting the file would lose it.

**What I recommend.**

* Stop shipping and installing the file, and delete Cairn's own copy.
* **Upgrade leaves a project's copy alone and says so.** LHM's copy is 77 lines and modflow_tools' is 229, both customised; deleting them would destroy governance text you wrote. Cairn's engine already does exactly this for any file it stops shipping: it prints one `removed-upstream` line and touches nothing. I measured it on a scratch install and on local clones of both projects. It needs no new upgrade logic.
* Do not touch the integrity check's list of exempt files. Taking this file off it makes every upgraded project fail the check with a "tamper" message (measured).
* Move the "short fixed list" rule into *Surfacing judgment calls to the Maintainer* in both copies of `dev/agent_collaboration.md`, word for word.
* Move the team-roster slot there too, and retire only the "sign the agreement" prompt, its seed task and its trigger. The "add a second agent type" prompt stays.

**What it costs.** A Security Review and the high-assurance path. Nine frozen files change (two helper scripts and seven tests), and one engine symbol, `_CORE_MAPPINGS`, changes in the AST baseline. The re-anchor you already plan at the cut covers all of it, provided this change finishes first. You run nothing now except the answers below.

**What I could not show.** I ran `upgrade --plan` on clones of LHM and modflow_tools but did not apply an upgrade to them: their trees carry unrelated 0.3 drift that blocks an apply. I rehearsed the apply on a scratch install shaped like them. I also cannot say whether anyone values the signing prompt: no fire is recorded for it in Cairn, LHM or modflow_tools.

## Questions for the Maintainer

Each has my default. An unanswered question takes it.

1. **What happens to a project's existing copy when it upgrades?** *Default:* it stays exactly as is, and `upgrade --plan` prints one informational line, `removed-upstream 1: dev/collaboration_agreement.md`, which `bootstrap/UPGRADE.md` will explain. The cost is that the line repeats on every plan for as long as that project's lockfile lists the file, because only new engine code (or hand-editing a file marked do-not-edit) could release it. *Alternatives:* delete the copy on upgrade (it destroys the 77 and 229 lines of project-owned text, and an upgrade should not do that), or teach the upgrade to stop tracking it (new engine logic and a second Security Review, which I would queue after 0.4 if the repeating line bothers anyone).
2. **Keep the team roster and the "add a second agent type" prompt?** The roster is the list of who works the project, today a slot in the agreement. A helper reads it to suggest the second-agent checklist. *Default:* keep both. The slot moves, with the same name and text, to `dev/agent_collaboration.md` under *Team roles*, and the helper reads it there. Only the "sign the agreement" prompt, its seed task and its trigger retire. *Alternative:* drop the roster and both prompts. The helper's prompt list would then be empty, and the repo has a test that refuses an empty list, so the whole prompt feature would go too (a 161-line helper module, its call sites in the activation command, and two test files of about 430 lines between them). Neither prompt has a recorded fire in any of the three projects, so that is a fair option. I rejected it for 0.4 only because it grows the shipped-code change in the release window. I would queue it as a follow-up.
3. **Where does the "short fixed list" rule live, and does it ship?** It says you decide acceptance, rejection, supersession, new scopes, overruling a reviewer, ceremonies where an agent must not bless its own verifier, pushing, and direction; everything else is the agent's call and escalating it is a defect. Only Cairn's copy of the agreement has it; adopters got the older one-sided version. *Default:* move it, word for word, into *Surfacing judgment calls to the Maintainer* in both copies of `dev/agent_collaboration.md`, so adopters receive it. *Alternative:* Cairn's copy only, which leaves the two copies different.
4. **If the review-stance plan slips past the cut, what gives?** This change cannot start until that plan archives. *Default:* 0.4 ships with the file still in it, and the removal goes into the next release. Nothing breaks, because the file still exists and the pointers to it still resolve. *Alternative:* hold the cut for it.

## Context

**Terms.** A *frozen file* is one whose hash is pinned in `bootstrap/tests/fixtures/gate_manifest.json`; changing it needs your *re-anchor* (the supervised ceremony in `bootstrap/REANCHOR_RUNBOOK.md`). The *AST baseline* is the committed fingerprint of the engine's top-level definitions (`bootstrap/tests/fixtures/scaffold_ast_baseline.json`). The *lockfile* (`dev/.cairn/cairn-lock.yml`) records, per installed file, where it came from and its hash. A *living-state* file is a project-owned file that `verify_integrity` skips. `removed-upstream` is the upgrade's word for a tracked file Cairn no longer ships.

**The decision.** `dev/PLANNING.md` row "Remove the collaboration agreement" records "Maintainer decision (2026-06-12): Cairn no longer needs a collaboration agreement", gated "before 0.4", and says it needs its own proposal. The release path's "Revised 2026-10-19" block (commit `26653324`) records your answer to "Include that removal in this release?": "Yes, before the cut (Recommended)". It sequences the removal "after `review-stance-and-lenses`, which edits the same review norms".

**What the file is.** A short file every install receives at `dev/collaboration_agreement.md`: 68 lines in the template, 94 in Cairn's copy, at the base commit named under *What I measured*. It holds a `team-roster` slot, six norms and an optional signature-log ritual. Each norm exists in more authoritative form elsewhere:

| The agreement's norm | Where it lives now |
|---|---|
| Substantive change is deliberated | `AGENTS.md` > "The lifecycle" and the proposal template's triage |
| Review is honest | `AGENTS.md` > "Review" (no quota of findings; a clean pass needs evidenced answers) |
| The record is durable and append-only | `AGENTS.md`, the "Append-only" bright line |
| The Maintainer decides | `AGENTS.md` > "Roles" and "Git and commit workflow" (the four things approval attaches to) |
| Roles are named | `AGENTS.md` > "Roles" ("name your role before substantive work") |
| Coordination is through artifacts | `dev/agent_collaboration.md` > "Coordination" ("sessions coordinate through the record, not through shared memory") |
| Amending is a proposal; the signature log | no counterpart. The signature log is opt-in, and only modflow_tools' own copy carries one |
| **Cairn's copy only:** the Maintainer's short fixed list, and "escalating it is a defect" | **nowhere** (this is the loss the proposal prevents) |

The last row is the only unique content. It came from the accepted proposal `2026-08-04-claude-decision-rights-floor`, which amended only Cairn's own copy ("No code, no doctrine, no templates"). The nearest text elsewhere, *Surfacing judgment calls to the Maintainer*, says "Most calls are the agent's to make" but carries neither the list nor the "defect, not caution" sentence nor the "decide, act, and record" instruction.

**The two real projects.** LHM's copy has its own roster. modflow_tools' copy is 229 lines with its own norms, a revision history and a signature log, and it holds the "External Review Norms" heading that `doctrine/plans.md` cites. A search with a control shows the heading never lived in Cairn's agreement or the template: `git log --all -S"External Review Norms"` over those two paths returns no commit, while the same command for a phrase known to be in the template ("Optional: a signature log") returns one. In both projects the lockfile marks the file `living_state: true`, with the same `base_hash` as the template at the base commit (the review-stance plan's C3 has since edited the template).

### The surfaces, found by search

**The instrument.** Case-insensitive `git grep -I` over every tracked file at the base commit, pattern `collaboration[_ -]agreement|collab[_-]agreement|sign-collab|team-roster|External Review Norms`. Control: the template, `scripts/_onboarding/triggers.py` and `bootstrap/_scaffold/config.py` all match, and the three files that cite the old heading (`doctrine/plans.md` and the two `security-review` copies) match. Because prose wraps, a separate whole-word pass for `agreement` alone catches a name split across two lines; it found three names split across lines (a comment in `bootstrap/_scaffold/lockfile.py`, the board row, and `case-studies/lhm.md`) and three "signed agreement" paraphrases (that lockfile comment again, `bootstrap/verify_integrity.py`, and a docstring in `bootstrap/tests/test_upgrade.py`), all in files already listed or placed in group 8. A second pass for the paraphrases `signature log`, `signed agreement`, `working agreement`, `review compact` and every other `collab` spelling found one more live mention (the `dev/` README table row, already counted) and one ambiguous one: `templates/core/dev/measurement/README.md` lists "the signature log" among incident ledgers, which reads as an unrelated ledger; a reviewer should confirm.

**Result: 69 tracked files hit.** 22 are records (17 archived proposals and plans, one review JSON, the changelog, two strategy notes, one measurement draft) and 47 are live. Re-run at `08c946a6`, after the review-stance plan's C3 landed: 67 files. The two `security-review` copies dropped out, as that plan promised, and its own test grew from 3 hits to 6, because it now pins more of the agreement pair. The live ones, grouped by what happens to them:

| # | Group | Files | What happens |
|---|---|---|---|
| 1 | The file and its install wiring | `templates/core/dev/collaboration_agreement.md`; `bootstrap/_scaffold/config.py` (`_CORE_MAPPINGS`); `bootstrap/_scaffold/lockfile.py` (`_LIVING_STATE_DSTS` and its comment); `dev/collaboration_agreement.md`; `dev/.cairn/cairn-lock.yml`; `dev/.cairn/claim-check-allow.json` | Template deleted. One row deleted from `_CORE_MAPPINGS`, the only engine symbol that changes. `_LIVING_STATE_DSTS` keeps the path (measured below); only its comment is reworded, which does not move the AST fingerprint (measured). Cairn's copy deleted after its rule moves. Cairn's lock keeps an orphan record, as adopters' will (tool-owned, never hand-edited). The allow-config loses the template-keyed entry and `CHANGELOG.md` gains the two retired paths, or its two history lines flag (measured). |
| 2 | Pointers in text adopters receive | `AGENTS.md` and `templates/core/AGENTS.md`; the proposal and plan templates, each with Cairn's copy (four files); `dev/README.md` and `templates/core/dev/README.md`; `docs/DOCUMENTATION_PLAN.md` and `templates/modules/default-on/documentation_plan_template.md`; `templates/optional/CONTRIBUTING.md`; `bootstrap/BOOTSTRAP.md`; `bootstrap/fidelity-check.md` | The review-stance plan's sentence about a roster loses "in `dev/collaboration_agreement.md`" and keeps its meaning (six files). A table row, a list entry and a bullet are deleted. `BOOTSTRAP.md` loses the file from its verify checklist and its token table, and re-points the roster slot in its slot list and slot table. The fidelity manifest sample loses the file in two places; its schema does not change. |
| 3 | The onboarding package | `templates/modules/default-on/_onboarding/triggers.py` and `prompts.py` with their byte-identical twins in `scripts/_onboarding/`; `templates/onboarding/solo-greenfield.md`, `collaborative-team.md`, `high-rigor-legacy.md` and the installed copy `dev/modules/onboarding/collaborative-team.md`; `docs/agent-team-onboarding.md` and its installed copy; `doctrine/onboarding.md`; `dev/PLANNING.md` | `collab-agreement-signing` goes from the trigger code and from the prompt registry. The roster reader points at the moved slot. Each preset loses its Row 1 prompt section; the solo preset loses its `sign-collab-agreement` task; the collaborative preset's day-one seed is retargeted at the roster slot and the legacy preset's `confirm-maintainer-authority` seed at `AGENTS.md`. The tour's roster step is re-pointed. Cairn's own board loses its copy of the seed task at the archive commit. |
| 4 | Where moved content lands | `templates/core/dev/agent_collaboration.md`, `dev/agent_collaboration.md` | Each gains the verbatim rule and the `team-roster` slot. |
| 5 | Tests | seven frozen tests edited (five tied to the onboarding change, two that go red when the file leaves); one more frozen test fixed by a config edit instead; the review-stance plan's new test, not yet frozen; one new test file | See *Tests required*. |
| 6 | Words for upgraders | `bootstrap/UPGRADE.md`, `CHANGELOG.md` | A short section on a file Cairn stopped shipping (`removed-upstream` appears nowhere in adopter-facing text today), and a changelog entry. |
| 7 | **Owned by the review-stance plan; not edited here** | `doctrine/plans.md` (the "External Review Norms" and "Stage-to-role matrix" cite); both `security-review` copies (already clean at `08c946a6`) | Its C4 removes the `doctrine/plans.md` cite. This change re-searches after it lands and expects zero. |
| 8 | Left alone, as history | `CHANGELOG.md`'s four old lines, `case-studies/lhm.md`, `case-studies/modflow_tools.md` and its fidelity-manifest example (accounts of those projects' own trees), two strategy notes (`dev/strategy/2026-05-14-claude-human-ai-team-development-framework.md` and an archived one), 17 archived records, `dev/measurement/queued-issue-drafts.md` (see below), a docstring in the frozen `bootstrap/tests/test_upgrade.py` that says where the living-state set came from, the two active plans that quote the path as a recipe | A record shows what was true when it was written. |

Two items in group 8 need a word. `dev/measurement/queued-issue-drafts.md` is a draft of an issue to file, not an append-only record, and it cites the removal as undone; the plan marks that paragraph done. And `bootstrap/verify_integrity.py` carries the phrase "the signed agreement" in a comment that lists living-state examples. That file is a frozen trust root another repair is editing now, and the phrase stays true for any project that keeps its copy, so I leave it.

### What I measured

All at base commit `c504fca86a9ce17b2160bbdd30e71a4e81aba91e`, interpreter Python 3.13.13, in detached scratch worktrees with uniquely named directories, now removed. "Prototype" means the template deleted and its `_CORE_MAPPINGS` row deleted, nothing else (and, where stated, Cairn's own copy deleted too).

| # | Measurement | Result |
|---|---|---|
| M1 | `scaffold.py --manifest`, prototype against base | exactly one row removed (`dev/collaboration_agreement.md  core/dev/collaboration_agreement.md  substituted`); the other rows are byte-identical |
| M2 | Fresh install from the prototype (high-rigor-legacy profile) | exit 0; no agreement file; no lock record; `verify_integrity` OK; reported block slots 23 to 22 |
| M3 | Template deleted but the row left | install still exits 0 and prints `[warn] core template missing: core/dev/collaboration_agreement.md`; no file is written. So the row is not what removes the file, but leaving it puts a warning on every install |
| M4 | Scratch project shaped like LHM (filled roster, `living_state` record), `upgrade --plan`, `--stage`, `--apply` with the prototype | plan prints `removed-upstream 1: dev/collaboration_agreement.md`; apply exits 0 ("Applied 0 file(s)"); the file's bytes, its lock record and its base-cache copy are unchanged; `verify_integrity` OK; every later `--plan` repeats the line |
| M5 | M4, but the project deletes the file itself | same single line; `verify_integrity` OK (a living-state record is skipped before the missing-file check) |
| M6 | M4, but the path is also removed from `_LIVING_STATE_DSTS` | `verify_integrity` fails: `illegal living_state opt-out: dev/collaboration_agreement.md is not an authoritative living-state path ... (tamper / malformed lockfile)`, "Do not trust the shipped scripts". This is why the set stays |
| M7 | `upgrade --plan` on local clones of LHM and modflow_tools, base against prototype | in both, the only difference is the agreement moving from "locally-modified (merged clean)" to `removed-upstream 1`. Their other classes (conflicts and merges from 0.3 drift) are identical on both sides. The source repositories were read, never written |
| M8 | AST fingerprint, `bootstrap/tests/_ast_attest.py` classification | base: CHANGED 5 (other work). Prototype: CHANGED 6; the new member is `Assign:_CORE_MAPPINGS`. A comment-only edit to `lockfile.py` adds no CHANGED symbol |
| M9 | `bootstrap/_scaffold` knowledge of trigger names | none: `grep` for `second-agent-type`, `collab-agreement-signing` and `first-cross-type-review` finds nothing under `bootstrap/_scaffold`; trigger names are data in the presets |
| M10 | Full suite, `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` | base: 4432 passed, 2 failed (both AST-baseline tests, red at base for other work). Prototype: 4429 passed, 5 failed: the same two plus three that this change owes (see *Tests required*) |
| M11 | `scripts/check_cairn.py` | base: 1 flag (a pre-existing path in a review record). Both files deleted and nothing else done: 34, the 33 new ones being the live citations. The acceptance is a return to the base count |
| M12 | The retired triggers against the three projects' rosters (helper code read-only, trees untouched) | `collab-agreement-signing` fires for none (all rosters filled). `second-agent-type` counts 0 agent types for Cairn and LHM, because their rosters name no vendor, and 3 for modflow_tools, which has the helper installed. Activation logs: Cairn's and LHM's are empty; modflow_tools has none on disk (the file is git-ignored there), so no fire is recorded |
| M13 | `bootstrap/verify_integrity.py` on Cairn's own tree | 18 violations at base (other work) and 18 with both agreement files deleted: the orphan living-state record in Cairn's lock is skipped, as a project's would be |
| M14 | At `08c946a6` (after the review-stance plan's C3), both agreement files and the install row deleted, one-file run of `bootstrap/tests/test_review_stance_in_shipped_files.py` | 64 of its 1,017 nodes red, every one in its agreement groups (`shipped-agreement`, `own-agreement`); 953 pass. At the same commit unmodified: 1,017 pass. Without this change's sequencing, the two plans would collide in that file |
| M15 | Prototype that adds the `team-roster` slot to the roles document; scratch project with its own edit in that document; `upgrade --plan`, `--stage`, `--apply` | merges clean ("Applied 1 file(s)"); the project's edit survives; the new slot arrives holding Cairn's default text; `verify_integrity` OK and prints one slot note naming `dev/agent_collaboration.md` and offering "Write the content, or N/A: <reason>" or a `cairn:customized` marker. The old reader of the old file still sees the old slot |

M10 was run twice. The second prototype also deleted Cairn's own copy: the same five failures, 4429 passed. So deleting Cairn's copy breaks nothing more at the base commit. After the review-stance plan's C3 landed that is no longer true, which M14 measures.

## Proposal

**Order first, because it decides everything else.** This change's plan opens after `review-stance-and-lenses` (`dev/plans/review-stance-and-lenses.md`) archives, and its last byte change to a frozen file lands before the re-anchor at the cut. Reasons, each read from that plan: its C3 (landed at `08c946a6`) rewrote the agreement pair this change deletes; its C4 removes the `doctrine/plans.md` cite; its C6 and C7 rewrite the tour page and the presets this change then edits; and its new test pins the sentence this change rewords and has a group that reads both agreement files. Plans for `neutrality-and-upgrade-slots` and `independent-scientific-check` do not overlap on the agreement: neither's tests read it, and the slot note one of them adds reads living-state files generically. The first also edits `solo-greenfield.md` and `bootstrap/UPGRADE.md` in other places, which the plan's re-read at edit time handles. Inside the plan the order is *stop citing, then delete*, so `check_cairn.py` is at the base count at every commit and the suite is green at each.

**What changes.**

1. **Stop shipping.** Delete `templates/core/dev/collaboration_agreement.md` and its row in `_CORE_MAPPINGS`, in one commit (M3). Install writes no agreement; `--manifest` loses one row; new lockfiles carry no record for it. The frozen manifest-row-count pin and the quickstart's expected-path list move with the same commit.
2. **Delete Cairn's own copy** after step 4 lands.
3. **Upgrade: no new logic** (Question 1). The engine's existing `removed-upstream` kind is report-only by construction (`_ADVANCING_KINDS` omits it), which is what M4 and M5 observed. `_LIVING_STATE_DSTS` keeps the path (M6). Its comment is reworded to say the entry is kept for projects that installed before the retirement; the measurement shows the AST does not move.
4. **Re-home the one unique rule** (Question 3). The paragraph below, copied from Cairn's agreement, joins *Surfacing judgment calls to the Maintainer* in both `agent_collaboration.md` copies. I change none of its words:

   > **The Maintainer decides — and the list is finite.** Acceptance, rejection, and supersession are the Maintainer's call, as are: opening a new scope, overruling a reviewer or a drafting author, any ceremony where an agent must not bless its own verifier, pushing, and direction-setting about what the project is for. **Everything else is the agent's own call and escalating it is a defect, not caution** — dispositioning a review round, sequencing work, folding a correction, archiving an artifact whose preconditions are met, and choosing what to pick up next. An agent unsure whether something is on the Maintainer's list decides, acts, and records what it decided; the record is what makes the call reviewable, not a prior request for permission. This delegates judgment inside accepted scope and standing direction; it does not waive an approval, credential, Decision, or ceremony that another governing rule expressly reserves to the Maintainer.

5. **Move the roster slot** (Question 2). The `team-roster` slot, with its marker names and default text unchanged, moves into `dev/agent_collaboration.md` under *Team roles*; Cairn's own filled roster moves with it. The default text keeps the phrase the helper tests for ("the bootstrap records"). The helper's roster reader opens that file instead. A project that upgrades gets the slot through the ordinary merge, keeps its own edits, and sees one slot note asking it to fill the slot, mark it N/A or keep Cairn's text on purpose (M15). It copies its roster across by hand, and `UPGRADE.md` says so. Until it does, `second-agent-type` is quiet rather than wrong. Net slot count is unchanged, so the quickstart's "22 unfilled block slots" stays true.
6. **Retire the signing prompt.** `collab-agreement-signing` leaves the trigger code and the registry; each preset loses its Row 1 prompt section; the solo preset's `sign-collab-agreement` task goes; the collaborative preset's `sign-collab-agreement-day-one` seed becomes a plain roster-fill task under a new id; the legacy preset's seed points at `AGENTS.md`. The row name is an idempotency key in activation logs, so retiring (rather than renaming) it means nobody who dismissed it sees it again.
7. **Fix the pointers** in group 2, including the review-stance plan's sentence, which becomes: "A roster the Maintainer sets (which agent types work the tree) is the team's shape, not a call: it adds no read and upgrades none." That plan's test pins the old wording and is edited with it.
8. **Words for upgraders.** A section in `bootstrap/UPGRADE.md` titled for a file Cairn stopped shipping: what `removed-upstream` means, that the file is theirs now, that deleting it is safe, that the line repeats, and where the roster goes. A changelog entry.
9. **Tests**, as listed below.

**What does not change.** The engine apart from one row. The lockfile schema. The living-state set. The norms the review-stance plan retires stay retired: nothing is re-homed from "External Review Norms", because none were ever in these files. The signing ritual is not replaced. Archives, case studies and the changelog's old lines are untouched.

**Not in this proposal.** Releasing a lock record on upgrade (Question 1's second alternative). Removing the prompt feature (Question 2's alternative). Whatever the review-stance plan's C7 leaves in the preset text about the second-agent prompt; this change edits what it finds.

## Rationale

This follows your decision and spends the least engine. The shipped template, one table row and the pointers are prose. The engine edit is one list entry, and the upgrade path is code that already exists and already does the safe thing. The measurements say where cleverness would have hurt: removing the living-state entry, or deleting on upgrade, would each break or destroy something a project owns.

The cost is real. Two of the nine frozen files are executables adopters run, so this takes a Security Review and the high-assurance path, and it adds a repeating line to every affected project's `upgrade --plan`. It buys: the last file that asks every install to "sign" something is gone; one fewer place restates the review norms (the review-stance plan had to correct this file and add a sentence about it); and one fewer file for a new adopter to read and one fewer ritual to explain.

## Alternatives considered

* **Do nothing, or keep a slimmer file.** This contradicts a decision you made twice. It also keeps a surface that every review-norm change has to remember to correct, as the review-stance plan did.
* **Fold the removal into the review-stance plan.** That plan is already reviewed and being built, and you sequenced this after it. Folding would reopen its plan review for a change with a different risk (an engine edit and an adopter-run helper).
* **Delete the copy on upgrade.** Rejected on the files' sizes: it would erase LHM's roster and modflow_tools' norms, revision history and signatures. The upgrade is also designed never to apply a removal (`removed-upstream` is report-only), and making it do so is new, security-relevant engine behaviour.
* **Release the lock record on upgrade.** This would end the repeating line. It needs new logic in at least the upgrade planner and applier, a write to a tool-owned lockfile and a delete in the base cache, which is a containment question for a Security Review. It buys only the removal of one informational line. Deferred; Question 1.
* **Remove the template but leave the engine row.** M3: every install prints a "template missing" warning.
* **Drop the path from `_LIVING_STATE_DSTS`.** M6: every upgraded project fails its integrity check.
* **Leave `second-agent-type` reading the old path.** The smallest diff, and dead for every new install: a trigger no fresh tree can fire. I will not ship that.
* **Re-source `second-agent-type` from author and reviewer attributions** in proposals and plans. It needs no roster, but it is new parsing logic in a helper adopters run, and its sibling trigger `first-cross-type-review` already reads the same signal. Too much new code for the release window.
* **Retire both prompts and the roster.** Question 2's alternative. A test that exists to refuse an empty prompt list (`test_the_row_registry_is_not_empty`) would force deleting the prompt feature with them.

## Documentation / doctrine surface

Routed by `docs/DOCUMENTATION_PLAN.md`.

* **Governing** (prescription): the `AGENTS.md` pair (one sentence), the four authoring templates (the same sentence), and the `agent_collaboration.md` pair (the rule and the slot). All shipped, so the twins stay in step apart from tokens, slots and Cairn-only names.
* **Doctrine:** `doctrine/onboarding.md` describes the trigger list, the two named prompt rows and the priority order; it is rewritten to one row. This is a Maintainer decision conformed into text, not an incident, and it adds no rule, so I read the doctrine rate-limit gate as not triggered. A reviewer who reads it otherwise should say so, and the grounds are your two recorded decisions.
* **Deliberation:** this proposal, its plan, `dev/PLANNING.md` (the board row, its seed copy and a second *Joined* paragraph on the re-anchor row, all at serialization points) and `CHANGELOG.md`.
* **Descriptive:** `bootstrap/UPGRADE.md`, `bootstrap/BOOTSTRAP.md`, `bootstrap/fidelity-check.md`, `docs/agent-team-onboarding.md` and its installed copy, `docs/DOCUMENTATION_PLAN.md`, `templates/optional/CONTRIBUTING.md`, the two `dev/README.md` copies.

## Evidence / verification plan

The change works when four things hold on a clean tree. (1) A fresh install of each of the three presets writes no agreement, carries no lock record for it, passes `verify_integrity`, and no installed file cites the retired path. (2) `scaffold.py --manifest` differs from base by that one row and nothing else. (3) An upgrade of a project that has the file prints the single `removed-upstream` line, leaves the file, its record and its base copy byte-identical, and `verify_integrity` stays OK. (4) `check_cairn.py` is back at the base count. Boundary B runs `full` and records `**Boundary B mode**: full`: the change touches the install contract, the engine and an adopter-run executable, so bounded mode refuses.

What would falsify it: any of those four failing; or the re-anchor ceremony showing an AST symbol other than `_CORE_MAPPINGS` moved by this work.

### Tests required

**Test home:** `bootstrap/tests/`, run on the canonical interpreter. These are the affected nodes; the search for readers is by what imports or reads the touched files, and the plan's Boundary B is the full suite.

Red today when the file leaves (M10), and so edited in the same commit as the deletion:

* `bootstrap/tests/test_notice_install.py::test_notice_appears_in_manifest_data_row_count` pins the manifest row count at 97; it becomes 96. Frozen.
* `bootstrap/tests/test_quickstart_sequence.py::TestLayerAStepsOneThroughThree::test_step3_install_writes_expected_kernel_and_modules` lists the file among the expected installed paths and compares the slot count with `docs/quickstart.md`. The path comes off the list and a check that it is absent goes on; the slot count stays 22 because the slot moves. Frozen.
* `bootstrap/tests/test_claim_check_allow_config.py::TestTheConfigIsWhereExemptionsLive::test_a_configured_document_is_clean_and_is_not_clean_without_it` goes red through `CHANGELOG.md`, which cites the removed template. It is fixed by the allow-config edit, not by editing the test. Frozen, unedited.

Retire or rework with the onboarding change (all frozen; they build fixtures by hand, so they stay green until edited):

* `bootstrap/tests/test_trigger_evaluation_action.py`: the `TestCollabAgreementSigningTrigger` class (four nodes) retires; the `TestSecondAgentTypeTrigger` nodes and the shared roster-writing helper move to the new path; `TestMixedAction` loses one expectation.
* `bootstrap/tests/test_active_surfacing_mechanism.py`: the priority test needs two rows and one is leaving, so it injects stand-in rows. The idempotency and cap tests keep their meaning.
* `bootstrap/tests/test_active_surfacing_render.py`: the registry-derived row list loses a row, so the combination and distinctness tests shrink by themselves; the three per-preset Row 1 tests retire. `test_the_row_registry_is_not_empty` stays untouched; it is why Question 2's alternative is expensive.
* `bootstrap/tests/test_onboarding_seed_roster.py`: the seed-id list loses the old id and gains the new one.
* `bootstrap/tests/test_core_dev_folders.py`: a docstring that names the file as an example.

Read the preset or install and must stay green, unedited: `test_onboarding_slot_substitution.py`, `test_skills_onboarding.py`, `test_presets.py`, `test_profiles_smoke.py`, `test_scaffold.py`, `test_manifest.py`, `test_lockfile_module.py`, `test_scope_reduction_trap.py` (it reads both `agent_collaboration.md` copies by label), `test_verify_integrity.py` and `test_upgrade.py::TestLivingStatePartition` (the mutation partners for M6).

Not yet frozen, edited in place: `bootstrap/tests/test_review_stance_in_shipped_files.py` (the pinned roster sentence and its group over the agreement pair; 64 nodes red when the pair leaves, M14).

New, named for the property each pins and carrying no coordinate:

Proposed paths:
* `bootstrap/tests/test_agreement_retired.py` — the new test

The new file, `bootstrap/tests/test_agreement_retired.py`, pins three properties:

1. A fresh install of each shipped preset writes no agreement, carries no lock record and no manifest row for it, and still writes `dev/agent_collaboration.md` (the control that the test can see a file that should be there).
2. A project that still has the file and its living-state record, upgraded through plan, stage and apply, keeps the file's bytes, its record and its base copy, reports `removed-upstream`, and passes `verify_integrity`. Mutants, each beside an unmutated control: drop the path from `_LIVING_STATE_DSTS` (must fail the integrity half); make apply remove the file (must fail the bytes half).
3. No file in the install set (`templates/`, `dev/modules/`, both `AGENTS.md` copies, the shipped docs) cites the retired path or the retired trigger names. Control: inserting a citation into a scanned copy fires it. Any exemption table lists only files that do not ship.

### Examples / smoke checks

* `python bootstrap/scaffold.py --manifest` against the base output: one row.
* `--summary` and `--dry-run` for each of `solo-greenfield`, `collaborative-team` and `high-rigor-legacy`.
* Scratch installs from a detached worktree of the finished commit, then `verify_integrity` and a recursive search of the installed tree for the retired names (control: the same search on an install from the base tree finds the file and the lock record).
* The upgrade rehearsal on scratch clones of LHM and modflow_tools (as M7, extended through stage and apply where their drift allows) and on a scratch project shaped like them (as M4 to M6), in fresh directories under the scratchpad, never in either project.
* `python scripts/check_cairn.py` with the edited paths named (explicit paths bypass the default filter), `python scripts/claim_check.py` on each edited document, and `python scripts/quality_gate.py --sub neutrality` staying at its current count.
* `python bootstrap/tests/_ast_attest.py verify`, deriving the CHANGED set at the commit rather than carrying a figure: the work adds `Assign:_CORE_MAPPINGS` and nothing else.
* `python bootstrap/tests/_gate_manifest.py verify` in a scratch worktree, to list the `FROZEN-MODIFIED` and `COLLECTION-DROPPED` entries this change adds. The suite's own `test_gate_manifest.py` does not read the committed fixture, so a green suite does not show that a re-anchor is owed.

#### Security preflight — five questions, answered in writing

* **S1 — Who supplied it?** Three steps decide something. (a) The upgrade's `removed-upstream` verdict takes the lockfile record's `src`, supplied by the project's tool-owned lockfile, and a Cairn checkout named by the operator. The verdict is report-only: it is never staged and never applied, so a forged record can at most print a line. (b) `verify_integrity`'s living-state exemption takes the record's `living_state` flag and the verifier's own `_LIVING_STATE_DSTS`; it honours the flag only for paths in the verifier's set. This change adds nothing to the set and removes nothing, so it widens nothing. (c) The roster reader parses the text between two markers in a file the project supplies, through the helper's containment check, to decide whether to print a prompt. It decides no authority.
* **S2 — Can it fail?** The manifest comparison fails if the row is restored (M1, one-row difference). The row-count pin fails on either a leftover or a missing row (red in M10). `check_cairn.py` fails on a leftover citation (34 against 1 in M11). The integrity half of the upgrade test fails if the living-state entry is dropped (M6, run). The bytes half of that test and the citation scan in the new test fail only under the mutants named above, which the plan runs; I have not run them, so they are claims until then. The AST gate fails on any other changed symbol (M8). No check here derives its expectation from the object it checks: the manifest and the AST are compared against the committed base, not against the new tree.
* **S3 — What fires it, over what?** Cairn has no CI. A person or agent runs the commands in *Examples / smoke checks* and the Boundary B full suite, over the clean finished commit and its install set. The adopter-facing sentence is the new *UPGRADE.md* section's: it will say that the plan prints one `removed-upstream` line for the file, leaves it and its record, and that `verify_integrity` still passes. M4 and M5 show exactly that, and the plan quotes the sentence beside the measurement.
* **S4 — Which way does it break?** A missing template with the row left installs less, loudly (M3). A missing or unfilled roster reads as "unfilled" and fires no prompt: fewer prompts, no added authority. A retired trigger name in an old activation log is an inert string. Dropping the living-state path breaks toward more alarm for every project (M6), which is why the entry stays. Each lands on the side of less authority or more noise, never more access.
* **S5 — Who still wins?** The assumed attacker can edit a project's lockfile or its files. One still succeeds, as today: content changes to `dev/collaboration_agreement.md` pass `verify_integrity` because the path is in the verifier's set. After this change nothing Cairn ships reads that file in a fresh install, and the old helper that did, in a project that has not upgraded, only parses text between markers. The class is closed by enumeration (the verifier's set), not by construction, and it does not change.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

* After the change, `check_cairn.py` stays above the base count, or a fresh install's tree still names the file: a pointer was missed.
* An upgraded project's `verify_integrity` reports anything about the agreement: the living-state set or a record's shape moved.
* `upgrade --plan` on a clone of LHM or modflow_tools shows any class for the file other than `removed-upstream`, or any other line moving.
* A team that filled the moved roster slot sees no `second-agent-type` prompt, or the prompt fires from an unfilled slot: the reader's path or the default-text marker is wrong.
* The re-anchor ceremony lists an engine symbol other than `_CORE_MAPPINGS` as changed by this work, or a frozen file the plan did not list.
* An adopter or a reviewer says they relied on the signing prompt or on the roster for something this change drops. Nothing in the three logs suggests it, but nobody outside them has been asked.
* The `removed-upstream` line draws complaints from LHM or modflow_tools: Question 1's deferred alternative comes forward.

## Scope delta

**Scope delta**: preserved. The baseline is the board row's six surfaces, and each is accounted for with evidence in *Context*. Retired: the onboarding step and the expected-folder wiring. Re-pointed: the pointers and the bootstrap tests. Settled as moot, not dropped: the `AGENTS.md` required-reading link and the `agent_collaboration.md` pointer (already gone), and "re-home the External Review Norms" (the heading was never in these files; the review-stance plan retires the citations). The one unique rule the row did not name is added to the baseline, not traded for anything. Declining to re-home norms that do not exist is not a reduction.

## Assurance path

**Assurance path**: high-assurance

Mandatory here on four grounds, each named in `AGENTS.md` > "High-risk surfaces": the change touches the install contract (the published `scaffold.py --manifest` and the install set), the scaffold engine (one row of its install table), an executable adopters run (the onboarding helper), and the governing text and authoring templates every install receives. Uncertainty resolves upward and none remains. The same grounds set `**Review**: usual + Security Review` and `**Plan review**: required(Internal + Internal Security Review)` in the header. The Security Review has a concrete job: read the helper's roster reader after the change, confirm the upgrade path and the verifier's living-state set are untouched except for a comment, and try to break the new upgrade test with the two mutants named above.
