# Plan: Trim the authoring templates, testing module and collaboration guide; list the rules that apply

**Source proposal**: dev/proposals/archive/2026-11-16-claude-template-trim-and-rules.md
**Author**: Claude Sonnet 5.5 (`claude-sonnet-5-5`, Medium), plan author
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-16
**Rules that apply**: dev/rules/working-agreements.md, dev/rules/protected-surfaces.md, dev/rules/conventions.md
**In brief**: Agents will read about 4,000 fewer words in five shipped files with every rule kept, each plan and proposal will name the rule files that apply, and a plan cannot archive with leftovers that have no home.

## Build summary

After this plan an agent starting a task loads far less text. The plan template, proposal template, testing module, collaboration guide and vendor wrapper shrink to the accepted word targets. Duplicated text is deleted where the rule survives elsewhere, explanation moves to the published docs, and two Medium-tier chunks rewrite the rest shorter. Both templates gain a `**Rules that apply**:` line. The plan's Dispositions section becomes an Implementation closeout record in which every "not run, not covered or remaining" item names a Home, and `tools/board.py` warns on stderr when a plan at `ready-to-archive` has an item with no Home. The testing module gains the accepted test-cut rule and its exemption, a time owner, a clean-checkout run and the part-by-part principle.

**Length.** This opening is about 5,600 words against the 1,000-word target. About 2,700 of them are the exact rows and new texts of C2, C3, C5, C7 and C8, which are the design; leaving them out would hand rule rewriting to the implementer, which the proposal forbids.

## Source proposal

The heavy-tier proposal (`dev/proposals/archive/2026-11-16-claude-template-trim-and-rules.md`, accepted 2026-11-16: "Let's accept all five as revised") sets a word target per file, moves explanation to documentation, adds the rules line, folds Dispositions into the closeout record with an advisory `board.py` warning, and adds five testing sentences and an appendix rule. It keeps #74, #76 and #79 in a held follow-on and keeps the test-cut rule in the shipped `testing-discipline` module. No operative rule may leave loaded text without the Maintainer's quoted word.

Proposed paths:
- `dev/proposals/archive/2026-11-16-claude-template-trim-and-rules.md`
- `bootstrap/tests/contract/test_board_closeout_warning.py`

## Scope

**Result.** Measured with `wc -w` at `1fa1d898` (the paths are clean there). "After rows" is the measured count once the exact rows below are applied; C4 and C6 close the rest.

| File (Cairn's copy in brackets) | Now | After rows | Target |
|---|---|---|---|
| `templates/core/dev/plans/_template.md` (4,859) | 4,871 | 3,769 (3,757) | 3,900 |
| `templates/core/dev/proposals/_template.md` (4,599) | 4,275 | 3,321 (3,645) | 3,400 |
| `templates/modules/team-gated/testing-discipline.md` (equal copy) | 2,134 | 1,900 | 1,400 |
| `templates/core/dev/agent_collaboration.md` (6,190) | 6,116 | 5,682 (5,757) | 4,800 |
| `templates/core/VENDOR.md` (Cairn `CLAUDE.md` 362) | 310 | 154 (288) | 170 |

Shipped `AGENTS.md`, `VENDOR.md` and `RULES.md` then total 1,339 (now 1,495; cap 1,500, held by `bootstrap/tests/test_scaffold.py`); Cairn's three total 1,414 (now 1,488; written cap 2,000). `AGENTS.md`, `RULES.md` and the `## Cairn Plain Language` section are not edited (three copies must stay equal).

**Branch.** Every chunk runs on `0.8-dev` (`dev/PLANNING.md` > "Working rules"). It does not exist at `1fa1d898`; no chunk starts before the coordinator creates it. This plan is a document and may be committed on `master`.

**Frozen files.** None edited. Measured: no planned path is in `frozen_files` or `protected_roster` of `bootstrap/tests/fixtures/gate_manifest.json` (exact-string search; `tools/board.py` appears only inside test node IDs). The one risk is C1 finding a frozen test that pins wording; C1 then stops for the Maintainer, so any frozen edit is grouped in C1 and one re-anchor covers it. Otherwise no ceremony is owed. C9 is the last chunk.

**Shared files** (order of group 2: heavy-tier trigger, template scan, release tests, this plan, staged modules, scientific run evidence). Each chunk starts with `git status --short <paths>` and `git log -5 --oneline -- <paths>` and stops on another session's uncommitted edit; a sentence an earlier plan added is kept verbatim.
- Both proposal templates and both guides: the heavy-tier trigger and template scan edit trigger lines first; no row below touches those lines.
- `dev/rules/protected-surfaces.md`: both edit it first; C3 appends one paragraph.
- Both `dev/rules/README.md` files: staged modules adds about 300 words after; C2 adds one sentence first.
- Both testing-module copies: scientific run evidence adds about 170 words after; C4 keeps the three numbered items of "Simulation models verify at three timescales".
- `tools/test_tiers.json`: staged modules adds a pattern; each adds its own line.

**Plans written against today's template** (adopter-defects, meter) keep their shape. A plan still open when C7 lands may close with the old Dispositions section; nothing reads it and the new warning ignores it.

**Non-work**, with reasons:
- #74, #76, #79: the held follow-on, by the Decision. Rules-folder guidance beyond one sentence: the staged-modules plan.
- `CHANGELOG.md`, `dev/PLANNING.md`, moving the proposal: the coordinator at closeout, not implementers.
- `docs/methodology` text on the `Dispositions:` block: it already says "closing metadata", which the closeout record is.
- A test-record tool (#81): principle only, by the proposal. An upgrade-merge trial on an adopter tree: not requested.

**Upgrade note** (for the coordinator's changelog): "Before upgrading, move any rule lines you added to Cairn's authoring templates or collaboration guide into `RULES.md` or `dev/rules/`. Taking Cairn's new text in a merge conflict loses a line you added."

**Reuse.** The warning reuses `_artifacts`, `_header_fields` and `_encode` in `tools/board.py`. Searched `grep -n "^def _" tools/board.py`: `_waiting` and `_roadmap_waits` read plan text for other markers but share no grammar. The count and cut checks are throwaway scripts.

### Documentation / doctrine surface

Governing text: both templates, the module, the guide, `VENDOR.md`, both rules READMEs. Deliberation: `dev/rules/protected-surfaces.md`. Descriptive: moved explanation is appended verbatim under `## Moved from the <file> in the v0.8 trim` in `docs/methodology/plans.md`, `proposals.md`, `dual-review.md` and `docs/further-reading.md`. No doctrine-evolution gate is claimed: the Maintainer's direction is the authority and the appended text adds no rule.

## Sequence

**Every chunk.**
1. `git branch --show-current` prints `0.8-dev`. Claim the paths (`python tools/intent.py claim --files <paths> --action "<what>" --stem trim<N>`), commit by explicit path, never push, never edit `CHANGELOG.md`.
2. Re-measure with `wc -w` and find each span by grepping its first words. Counts differ if an earlier plan landed. An anchor matching 0 or 2 times: stop, return to the plan author.
3. A span runs from its first anchor word to its last, line breaks ignored. **D** deletes it and one adjacent blank line. **M** deletes it and appends it verbatim to the named docs file. **S** replaces it by the given text. **I** inserts the given text after it, preceded by one space. Retype, rewrap or reorder nothing else (`scripts/exact_replace.py` or an exact Edit).
4. Before a D row, read its survivor (the home named) and confirm the rule is there. A survivor is never cut. Home codes in the tables: PR = guide "Plans and records", RR = guide "Review rules", RL = guide "The review loop", VF = guide "Verification", PA = plan template "Plan amendments", WL = plan template "The Waiting line", AG = `AGENTS.md` "Lifecycle and records". A deleted sentence with a condition the survivor lacks: stop, return to the author; the carried text this plan lists is the only exception.
5. Apply every row to the Cairn copy too; a row whose anchor is absent there is skipped and named in the commit body. Afterward `diff <shipped> <cairn>` shows only the hunks it showed before.
6. No-weakening check, every prose chunk. A throwaway script lists, from `git show <base>:<path>`, each sentence containing `must`, `never`, `only`, `required`, `requires`, `cannot`, `may not`, `do not`, `does not`, `refuse`, `always`, `owes`, `unless`, `stop`, `no agent`, `waive` or `exempt`, with its best match in the new file. Measured at `1fa1d898`: plan template 94 sentences, proposal template 64, guide 131, module 24, wrapper 4. Each is verbatim, deleted by a table row whose survivor holds it, or rewritten; any other stops the chunk. In C4 and C6 each rewritten one gets a ledger row.
7. The commit body gives words before and after, the rows applied, each rule removed or changed with its home, and the tests run.

| # | Chunk | Tier | Gate | Ships |
|---|---|---|---|---|
| C1 | Pin scan | Low | `0.8-dev` exists | scan result |
| C2 | Vendor wrapper, rules README sentence | Low | C1 | 3 files, 2 copies |
| C3 | Testing module: exact rows, new rules | Low | C1 | module copies, protected-surfaces, further-reading |
| C4 | Testing module to 1,400 | Medium | C3 | module copies, ledger |
| C5 | Guide: exact rows, carried sentences | Low | C1 | both guides, dual-review |
| C6 | Guide to 4,800 | Medium | C5 | both guides, ledger |
| C7 | Plan and proposal templates | Low | C6 | 4 templates, plans, proposals |
| C8 | Board warning, appendix skip, test | Low | C7 | 2 board copies, 1 test, tier map |
| C9 | Sweep and lock | Low | C8 | lock record; last chunk |

Assumed, not measured: 8 to 10 agent-hours and two code reviews. The two Medium chunks are authoring, not mechanical edits. The rewrite starts with the testing text (C3, C4); Boundary A, B and C sentences stay verbatim, checked first in C5.

### C1 Pin scan

Throwaway script: lowercase, strip quotes and `*_#>`, collapse spaces, take every six-word run of the five shipped files and their Cairn copies, search every `test_*.py` under `bootstrap/tests`, `scripts`, `tools` and `templates/modules/team-gated` (`dev/rules/working-agreements.md` > Tests). Measured 2026-11-16: none pins prose. Hits: one placeholder line in `test_board_json_contract.py`, an unrelated phrase in `test_reanchor.py`, a slot placeholder in `test_agreement_retired.py`, a docstring in `tools/test_tiers.py`. The scan finds copied runs, not paraphrase. Structure that tests read, which no row may break:
- Both templates: one `**In brief**:` line below the first `---` with its placeholder; `**The summary line.**` above it; plan only: `**Waiting on Maintainer**:` above the rule and not in the header block, one `acceptance-doc-tooling` slot; every slot and its end marker; no one-word `{{x}}`; shipped bytes install unchanged.
- Guide: all 14 `##` headings (ten are cited by `AGENTS.md`), the role bullets, every slot, no `cairn:` marker inside "The review sweep", Plain Language unchanged.
- Module: `dev/modules/testing-discipline.md` byte-equal to shipped.
- `VENDOR.md`: line 1 `# Vendor wrapper — {{project_name}}`, `@AGENTS.md` within the first five lines (rename detection in `bootstrap/_scaffold/upgrade.py`), slot `vendor-addendum`.

A new wording pin that is not frozen: delete the test and name it. A frozen one: stop.

### C2 Vendor wrapper and README sentence

Replace `templates/core/VENDOR.md` with this text (310 to 154 words). In Cairn's `CLAUDE.md` delete `> **Thin vendor wrapper.** … not here.` (M, to `docs/methodology/dual-review.md`) and replace the `**Drift guard.**` paragraph by the last paragraph of that text. In both `dev/rules/README.md` files insert, after ``this folder or `docs/` can hold it.``: `A Maintainer's rule goes in the rule file with the Maintainer's approved wording, never only in an agent's memory.`

```text
# Vendor wrapper — {{project_name}}
Written in [Cairn Plain Language 1.0](dev/agent_collaboration.md).

@AGENTS.md

Rename this file to your AI tool's auto-loaded file (`CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`), and keep it thin: only habits specific to that one tool. The import line above gives the tool the shared `AGENTS.md`; adjust that one line if the tool imports another way.

## Tool-specific habits

<!-- cairn:slot vendor-addendum -->
(Harness-specific habits only: this tool's session and context model, scratch directory, command quirks, and how a context compaction or resume should trigger re-orientation. Do not restate the test command, required reading, routines or conventions; they live in `AGENTS.md`. An empty slot is valid.)
<!-- cairn:end vendor-addendum -->

---

**Drift guard.** Anything an agent of a different tool would also need belongs in `AGENTS.md`, not here. A wrapper that duplicates the test command, git rules, routines or required reading has drifted: fold that content back to its single source and leave the pointer.
```

Deleted, as explanation (the rename instruction and the adjust note are kept in the new text): the "This is the thin vendor-wrapper template" note, the HTML comment about the import line, and the `CONTRIBUTING.md` pointer (adopters get none). `bootstrap/BOOTSTRAP.md` II-2 also gives the rename step.

### C3 Testing module: exact rows

Both copies, identically.

| ID | Span | Kind and home |
|---|---|---|
| TM1 | `Cairn requires a change to **absorb … a complete testing curriculum.` | S; the rationale and Cairn's own-tests narrative are M |
| TM2 | ``> **Worked contrast: a pin and … private reach in `scripts/test_coupling.py`.`` | M |
| TM3 | `> **Worked useful/vacuous/broken contrast.** … not the expected value.` | S; the two examples are M |
| TM5 | ``A permanent test enters `tests/` only … a public entry point.`` | I (#88) |
| TM6 | `> **The suite has a time … measures it.` | S (#86) |
| TM7 | `equivalence proof is required. A size … quota.` | I (#77) |
| TM8 | `remedy; optional architecture review is available, not required for every change.` | S (#81); the deleted clause is M |

Texts:
- TM1: `This module gives the suite a shape, a way to choose tests, and a budget. The guidance below is a practical summary, not a complete testing curriculum.`
- TM3: `> **Observe the failure first.** Observe a new check fail before fixing behavior; fix the behavior, not the expected value.`
- TM5: `Run each new test once on a clean checkout before keeping it, so it does not depend on state only your machine has.`
- TM6: `> **The suite has a time budget and an owner.** The project names who owns the ordinary run's time, sets how long it may take, and measures it. Review the slowest test files on a stated schedule, such as each release.`
- TM7: ``A test that is not clearly a public promise is not kept; a higher-tier agent decides each judgment call. These are exempt and are cut only through a Security Review: tests of the surfaces your project's `AGENTS.md` names as high-risk, tests your project's release or security records name as guards, and refusal, hostile-state and negative-guard tests.``
- TM8: `remedy. A large project is not one piece: test each part where it lives. A change may be verified from current results in place of a whole-suite run; a release's own whole-suite and security-family run is never replaced by earlier results, and a release may reuse results only where a reviewed rule allows it.`

Also append to `dev/rules/protected-surfaces.md` (Cairn-only): ``Tests exempt from the promise-only cut. Cut only through a Security Review: tests of the surfaces above; the security-family files and native-only IDs in `bootstrap/tests/security_manifest.py`; tests that a release document, `bootstrap/SAFETY.md`, `bootstrap/_scaffold/SECURITY_MUTATIONS.md` or a shipped file names as a guard; and refusal, hostile-state and negative-guard tests. The generic rule is in the testing-discipline module.`` M spans go to `docs/further-reading.md`. No rule is deleted.

### C4 Testing module to 1,400 (Medium)

After C3 the file is 1,900 words, of which about 230 are the new C3 texts (verbatim, with the exemption sentence). Rewrite every other paragraph, in place and in order, to at most 68 percent of its words, rounded down; the file total must be at most 1,400 and both copies stay byte-equal. Keep the `Simulation models verify at three timescales` numbered items. Each keyword sentence (step 6) is kept, or shortened without dropping a condition or exception, and has a ledger row if changed. Append `## Trim ledger -- testing-discipline module` to this plan: one row per changed or missing sentence (first eight words; kept, shortened, moved or deleted; where the rule now lives; shipped or Cairn-only), only a count for verbatim ones. "Deleted" needs a reason: a duplicate (name the survivor) or explanation. If the target cannot be met without removing a ruled sentence, stop and report the shortfall.

### C5 Guide: exact rows and carried sentences

Both guides (Cairn's G6 end anchor reads `need no extra sentence or inventory.`).

| ID | Span | Kind and home |
|---|---|---|
| G0 | `> **The deliberation and decision process.** … shape they do.` | M |
| G1 | `**The AI surface is bimodal.** … than it should.` | M |
| G2 | `Plan reviews use the same three … repair an underspecified plan.` | D, RR plan-review paragraph |
| G4 | `Use the smallest checks that test … behavior need executable evidence.` | D, plan template "Verification" |
| G5 | `Narrowing is the path of least … version is never built.` | M |
| G6 | `When presenting a choice, show what … extra sentence or inventory.` | D, the next choice paragraph, with G6b |
| G7 | `Findings state their evidence and what … no criterion or check.` | D, RL finding paragraph |
| G7b | `Aim for 300 words of reviewer-written … in the coverage line.` | D, RL |
| G8 | ``Each appended `Plan change` entry uses … distinct and unchanged.`` | D, PA |
| G10 | `That is what makes the method … changing anything.` | D, "Durable state" paragraph; explanation M |
| G6b, G9, G11, G11b, G12, G13, G14, G15 | see below | I or S, carried text |

Carried text holds conditions that the templates' deleted copies had and the guide lacked:
- G6b, I after `do not inventory routine agent work.`: `The existing Decision briefly names material new recurring additions; a routine Decision with no such addition needs no extra sentence or inventory.`
- G9, S for `Full selection and evidence guidance is in the plan template.`: `Cover the clean final combined revision. Do not replay the whole selection solely to stamp a new commit ID.`
- G11, I after ``without `Called by` it is an ordinary pass.``: ``A roster the Maintainer sets (which agent types work the tree) is the team's shape, not a call: it adds no read and upgrades none. Where the call was relayed, add `, relayed by <who>`; the Maintainer's words follow, verbatim and set apart, and go in the commit message as for a scribed Decision. `**Tier**: External` is valid only with the `Called by` line. Its brief removes no owed answer; a pass clears a Security Review only by being one. Any other authority in the quoted words, such as a waiver or a change of scope, takes effect only where Maintainer authorizations already live, a Decision block or a plan's fence, never from a `Called by` line. Nothing checks the quote mechanically; the next reviewer and the Maintainer at the Decision are the check.``
- G11b, S for `Agents never request one or declare it required, but they may name a risk and a coverage gap.`: `Agents never request one, declare it required, say a change needs one, recommend more distance, head a pass External on their own, or start one without the Maintainer's words, but they may name a risk and a coverage gap.`
- G12, I after `names the unresolved question`: `or newly changed material`.
- G13, S for `owner and evidence, and create no release plan.`: `owner, evidence and a link to the implementation, and create no release plan; keep its result unpassed until its evidence exists.`
- G14, I after `Do not split work by default or lose accepted scope.`: `A shipped capability may be a prerequisite; another plan's future review, archive or release may not be required to finish this plan.`
- G15, I after `Failed required checks stay implementation work.` (cheap-follow-up paragraph): `This is not the narrower cheap defect fix in "Working tree and commits".`

M spans go to `docs/methodology/dual-review.md`. Shipped guide after rows: 5,682.

### C6 Guide to 4,800 (Medium)

Rewrite each section shorter to its budget (words after C5, then budget): header 36, 36; Team roles 264, 225; The team 45, 45; Collaboration stance 62, 55; The review loop 328, 270; The review sweep 976, 720; Cairn Plain Language 886, 886 (untouched); Surfacing 264, 215; Review rules 759, 590; Agent execution retries 130, 105; Plans and records 534, 410; Working tree and commits 414, 335; Verification 585, 460; Coordination 155, 130; Session reflections 244, 195. The budgets sum to 4,677 and leave about 120 for earlier plans' additions; the file total binds.

Kept verbatim: every survivor named in a D row of C5 or C7, all C5 carried text, any sentence an earlier group 2 plan added (`git log -p`), and any sentence naming Boundary A, B or C, `Bounding`, a model capability floor, a refusal or a Maintainer-only step. Then C4's rules apply: the step 6 inventory, no Security-Review-bearing sentence "deleted", `## Trim ledger -- collaboration guide`, the stop rule. Cairn's copy ends at most 74 words above the shipped one (today's difference), and its Cairn-only paragraphs lose no rule.

### C7 Plan and proposal templates

Both copies of each, after C6 so every survivor is final.

Rules line, below the rule after `**Opened**` and before `**In brief**` (I): `**Rules that apply**: {{rule file paths from the RULES.md routing table | bright lines only}}`. Paragraph above the rule, after `**Write for the reader.**` (I, both templates): ``**Rules that apply.** List the rule file paths from the `RULES.md` routing table that apply, never rule text, or write `bright lines only`. A rule that applies but is not listed is still followed; add it to the line. The line never narrows a review, a Security Review trigger or a protected-surface obligation. Reviewers compare it with Scope.`` Together 78 words per template; the proposal said about 20, and the required never-narrows sentence outgrows it. The trim pays for it.

| ID | Span | Kind and home |
|---|---|---|
| PL1 | `For related authorized work in a … usual plan and reviews.` | D, PR |
| PL2 | `Show that the goal is achievable … to finish this plan.` | D, PR with G14 |
| PL3 | `If work already opened encounters unexpected … when the Maintainer answers.` | D, WL |
| PL4 | `Cheap follow-ups mean a few person-steps … remains implementation work.` | D, RR with G15 |
| PL5 | `A fence is for a Decision … not at release.` | S, PR with G13 |
| PL6 | `Optional prompts for a criterion: condition, … or required checks.` | M |
| PL7 | `Record scientific evidence with the work … waiver or rescheduling.` | D, VF |
| PL8 | `**A reviewer cannot create that authority … only the Maintainer can.` | D, "Deviating from an accepted plan" paragraph |
| PL9 | `**Example.** A plan changes the public … final combined revision.` | M |
| PL10 | `The arc owner joins connected work … plan work before archive.` | D, VF with G9 |
| PL11 | `**More distance is the Maintainer's call, … Decision are the check.` | S, RR with G11, G11b; a sentence is M |
| PL12 | `Code review's job is falsification, and … "The review sweep").` | S |
| PL13 | ``` `python tools/board.py --json` prints … read by the board.``` | M |
| PL14 | `One plan may include dependent internal chunks … outcome unassigned.` | D, PR |
| PL15 | `This paragraph sits above the rule, … new plan as waiting.` | M |
| PL16 | `**Improve means recommend**: the reviewer proposes … no quota of findings.**` | D, RR |
| PL19a | `## Dispositions *Appended at archive-preparation` | S, heading below |
| PL19b | `doctrine").* Record one` | S, text below |
| PL20 | ``do not copy template instructions or … `## Dispositions`,`` | S |
| QT1a | `A second pass applies only to widened … ordinary cap stands.` | D, AG with G12 |
| QT1b | `At the cap, only … without a clearing review.` | D, AG |
| QT2a | `**Improve means recommend**: the reviewer proposes … no quota of findings.**` | D, RR |
| QT2b | `Target 300 words of reviewer-written text … required checks.` | D, RL |
| QT3 | as PL11 | S, as PL11 |
| QT4, QT5 | `Wrap prose normally; putting a … saves zero tokens.`; QT5 as PL13 | M |
| QT6a | `Name only useful output categories; … invent a tool.` | M |
| QT6b | `Keep this short; a short proposal may … fill sections.` | S: `Keep this short.`; M |
| QT7 | `Open each implementation plan only when … duration in the estimate.` | D, PR |
| QT8 | as PL1 | D |
| QT9 | `Select the smallest checks that could … keep their existing triggers.` | D, plan template "Verification" |
| QT11 | `one, which is the point: the reviewer checks … over four rounds.` | S: `one.`; M |
| QT11b | `Structural questions about where material … a reviewer can falsify.` | M |
| QT11c | `**Prospective only.** This accounting applies … retro-fitted with it.` | D, the earlier "Prospective only" sentence |
| QT12 | `For example, an analysis that reports … distance and schedule.` | M |
| QT13 | `When work joins a connected … reopening the archived plan.` | D, VF |
| QT14 | `**What they do not reach.** A … finds it.` | M |
| QT15 | `These are author declarations, not inferences: … it was right.` | M |
| QA1 | ``Readers list them with `grep -n … the job needs.`` | I, appendix bullet below (#73) |

Texts (PL rows apply to the plan template, QT and QA rows to the proposal template):
- PL5: `A fence is for a Decision or permission needed to carry out accepted scope, not a routine human-run trust or release operation.`
- PL11 and QT3: ``**More distance is the Maintainer's call, and only theirs.** See `dev/agent_collaboration.md` > "Review rules".``
- PL12: `Code review's floor is not the implementing agent, and it never reopens the Decision.`
- PL19a: `## Implementation closeout -- <agent> -- <YYYY-MM-DD>` then a blank line then `*Appended at archive-preparation`.
- PL19b: ``doctrine").* Say in a few lines whether each acceptance criterion held. Write each check not run, area not covered or work remaining as its own item: `Not run: <what>`, `Not covered: <what>` or `Remaining: <what>`, ending `Home: <roadmap row, issue, proposal or the Maintainer's quoted word>`. An empty Home means the plan is not ready to archive. A deferral of accepted scope or of a required check has the Maintainer's quoted word as its Home; a Home an agent creates alone (an issue or a roadmap row) covers only a follow-up that defers neither. Then record one``. The rest of the old section stays: the `Dispositions:` line, `accept`, `guard`, `wontfix` with its limits, `defer`, the batch and Waiting-line rule.
- PL20: ``do not copy template instructions or the `## Implementation closeout`,``
- QA1: after the span, a new bullet: ``* **Appendix.** Default none. Allowed only for a table or arithmetic a reviewer must check that no cited record can hold: one separate file, `<proposal-stem>--appendix.md`, beside the proposal (the board does not list it), never inline. The 1,000-word budget applies to the text at the Decision, so cut or move review additions before it.``

M spans go to `docs/methodology/plans.md` (PL) and `proposals.md` (QT, QA). Reserve, only if a count is over target and in this order: none for the plan template; for the proposal template, cut the slot sentences `Trace changed behavior through callers … plausible uncovered faults.` (51 words, shipped copy only), after carrying "language seams" and "uncertain dependencies" into the guide's "Verification".

### C8 Board warning, appendix skip, test

Edit `templates/skills/_lib/board.py` (the source), then copy it byte for byte to `tools/board.py`. Behavior (the criterion; the implementer writes the code):
- Plain view only (not `--json`, `--next`, `--maintainer`), active plans whose `Status` starts with `ready-to-archive`. A closeout item starts at a line that, after indentation and one `- ` or `* `, begins `Not run:`, `Not covered:` or `Remaining:`, inside a section headed `## Implementation closeout` and outside code fences; it runs to the next blank line, labeled line or heading. It has a Home if its text contains `Home:` followed by non-space text.
- Each item with no Home prints one line to stderr: `board: warning -- <file>:<line> has no Home`, the file name through `_encode` (escaped, elided at 48), the line a number. At most 5 lines, then `board: warning -- <k> more not shown`. Exit status stays 0. Plans are read only through `_artifacts`.
- `_artifacts` skips names ending `--appendix.md`. The module docstring gains one sentence. `--json` output and exit codes are unchanged.

New `bootstrap/tests/contract/test_board_closeout_warning.py`, through `board.main`: (1) a Home-less item warns, the output holding the plan's file name and the line number (not the message wording), and the stdout table is unchanged; (2) the same plan with a Home is silent; (3) an `implementing` plan and an archived plan are silent; (4) `--json` on the Home-less tree is valid `cairn-board/1` with empty stderr; (5) a 120-character plan name with an ESC character, and closeout text carrying escapes, print no raw ESC and none of the closeout text (the ESC name skipped where the filesystem refuses it); (6) 12 items print at most 6 lines; (7) the two board files are byte-equal; (8) an `--appendix.md` beside a proposal is not listed in plain or `--json`. Add `test_board_closeout_warning` to the `contract` tier in `tools/test_tiers.json`.

### C9 Sweep and lock

Run Verification. For each changed lock-tracked file (`dev/plans/_template.md`, `dev/proposals/_template.md`, `dev/agent_collaboration.md`, `dev/modules/testing-discipline.md`, `dev/rules/README.md`, `CLAUDE.md`, `tools/board.py`) run `python bootstrap/scaffold.py upgrade --target . --finalize <path>`, commit `dev/.cairn/cairn-lock.yml` alone, then `python bootstrap/verify_integrity.py --target .`. Put the counts table in the commit body and end this plan with its closeout record in the new form.

## Acceptance criteria

**C1.** The scan names its inputs and four test folders; its result is in the C2 commit body. No frozen test is edited; `python scripts/repin.py status` lists the same frozen-modified files before and after the plan.

**C2.** `templates/core/VENDOR.md` is 154 words, line 1 `# Vendor wrapper — {{project_name}}`, `@AGENTS.md` on line 4. Shipped `AGENTS.md`, `VENDOR.md` and `RULES.md` total at most 1,500 words (planned 1,339); Cairn's three at most 2,000 (planned 1,414). Both READMEs carry the new sentence once. The wrapper-rename nodes of `test_upgrade.py` pass.

**C3.** All seven rows are applied to both module copies, which stay byte-equal; the #77, #86, #88 and #81 sentences each appear once; the file is 1,900 words. The protected-surfaces paragraph exists. Removed spans appear verbatim in `docs/further-reading.md`.

**C4.** Both module copies are at most 1,400 words and byte-equal. Every keyword sentence of the pre-edit file is verbatim, shortened with all conditions kept, or in the ledger. The C3 texts are verbatim. A reviewer can answer "Does any rule weaken or disappear?" from the ledger row by row.

**C5.** Every row is applied to the shipped guide and, where its anchor exists, to Cairn's; the shipped guide is 5,682 words. The 14 headings and Plain Language are unchanged. Each D row's survivor was read first. Each carried text is present once. M spans are in `dual-review.md`.

**C6.** The shipped guide is at most 4,800 words and Cairn's at most 74 more. The Plain Language section diffs empty; headings, role bullets and slots remain. Survivors, carried text, Boundary and floor sentences are verbatim. The ledger covers every changed keyword sentence, with its home and shipped or Cairn-only. A stop with a stated shortfall is an acceptable result.

**C7.** Plan template at most 3,900 words (planned 3,769), proposal template at most 3,400 (planned 3,321). Both carry the rules line and paragraph. `## Dispositions` is gone; `## Implementation closeout` carries the Home rule, the deferral rule, the `wontfix` limits and the executing-`guard` rule. The C1 structure list holds, shipped bytes install unchanged, and Cairn's copies differ from shipped only as before.

**C8.** The eight tests pass once on a clean checkout, `python tools/test_tiers.py check` passes, the board files are byte-equal, and `test_board_json_contract.py` passes for both copies. The warning prints only a file name and number. S2 (it can fail): tests 1 and 5 fail without the code. S3 (what fires it): `python tools/test_tiers.py for tools/board.py` lists the new file and the contract file.

**C9.** The commit body has the counts table and each chunk's shared-file re-read. The lock records the seven paths and `verify_integrity` passes. `git diff --name-only` since C1 names no `frozen_files` entry. The closeout lists each item not run or not covered with its Home.

## Scope delta

**Scope delta**: preserved. Every outcome of the proposal is assigned: the five targets, the rules line, the closeout fold with the board warning, the five testing sentences, the appendix rule, the README sentence and the exempt-test list. C4 and C6 carry the risk: if a target cannot be met without removing a ruled sentence, the implementer stops and the shortfall goes to the Maintainer for a quoted allowance. A rule is never weakened to meet a number.

## Verification

Changed promises and entry points: the warning (`python tools/board.py`), both templates through install, module copy equality, the wrapper's rename detection, the 1,500 and 2,000 caps. Per chunk run `python tools/test_tiers.py for <changed paths>` and only the files it lists; never the whole suite. By reading, that is `test_board_json_contract.py` (read-only, templates and both board copies), `test_review_sweep_ships.py`, `test_writing_rules_ship.py`, `test_review_stance_in_shipped_files.py`, `test_scientific_check_guidance_ships.py`, `test_scope_reduction_trap.py`, `test_install_report_slots.py`, `test_verification_boundaries.py`, `test_practice_modules.py`; for `VENDOR.md`, `test_upgrade.py -k "vendor or VENDOR or wrapper"` and the one node `test_scaffold.py -k test_full_install_seeds_rules_md_within_word_budget`. Interpreter: `/Users/kendal30/conda_envs/lhm/bin/python3.13`.

Prose gates on each changed prose file: `python scripts/claim_check.py`, `python scripts/link_check.py`, `python scripts/sync_doc_snippets.py --check`, `python scripts/quality_gate.py --sub neutrality`; counts by `wc -w`. Code reviews: R1 (Internal) over C1 to C7 and C9, with the reading question against the ledgers; R2 (Internal Security Review) over C8, and over "Review rules" in C6 if the template-scan change has not landed.

Not run, to be homed at closeout: the whole suite and security family, Windows, an upgrade-merge trial on an adopter tree, any desktop-app behavior of `AGENTS.md`, a capability check of the Medium chunks' output.

## Plan review -- Claude Sonnet 5.5 (Plan Reviewer, Medium) -- 2026-11-16

```
Reviewed commit: 6986fafe15edfa9da764c6d0df9d178385c2a749
```

**Obligation**: Clear that a Low-tier implementer can run every chunk with no design left to them; that the plan delivers every outcome the 2026-11-16 Decision adopted; that no rule weakens or disappears except as the Decision accepts; and that the order, ownership and ceremony statements are true.
**Tier**: Internal
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: about 13 minutes (16:07 to 16:20, measured with `date`)
**Tokens**: unknown

Conclusion: not cleared; two blocking findings (C4 and C6, then C8) and four non-blocking. Steelman: C2, C3, C5 and C7 give exact old and new text, and my replay of their rows matched the plan's counts (module 1,902 against 1,900; guide about 5,680 against 5,682), so those chunks are close to mechanical.

**Foundations**

1. **Should this happen as framed?** Yes, and every accepted outcome has an owner, but the exact rows reach only three of the five word targets (templates 3,769 and 3,321, wrapper 154); the module stays at 1,902 against 1,400 and the guide at 5,682 against 4,800 -- `wc -w` on the shipped files and my row replay.
2. **Best alternative.** Fewer chunks and looser gates: C1 commits nothing (its result goes in C2's body), C8 needs only the branch, and C7 waits on C6 though C6 keeps every survivor verbatim, so one C6 stop stalls the rules line, the closeout fold and the board warning -- plan lines 85-86, 188, 263.
3. **What would show it wrong.** C4 or C6 ending in a stop, or the C8 warning never firing on the template's own heading; the plan excludes neither -- plan lines 152, 188, 251, 255, 273.

**Findings**

1. **Blocking, C4 and C6 (missing design; needs the Maintainer if it stands).** The plan gives only budgets (68 percent per paragraph; 410, 460, 590 and so on per section) for about 500 and 880 further words. Missing decisions: which sentences go, what replaces them, and when a target "cannot be met" (the implementer's own skill decides that, so the stop rule is a design choice; "ruled sentence" is defined only by step 6's keyword list, which misses rules such as "Choose tests by regime and boundary"). C6's "A stop with a stated shortfall is an acceptable result" pre-accepts a shortfall. The Decision adopted the table's targets, so a stop is a degraded Scope delta that only the Maintainer can allow. They would be allowing: module 1,900 against 1,400 (500 words, 36 percent over; adopters who select the team-gated module read 500 more words than adopted, 234 fewer than today) and guide 5,682 against 4,800 (882 words, 18 percent over; every adopter's guide, 434 fewer than today). By my crude keyword count, 2,557 of 5,181 guide words outside Plain Language sit in sentences with rule words, so the budgets are unproven. Closes: exact D/M/S rows for the rest, as C3, C5 and C7 have (both chunks then run Low); or the Maintainer's quoted allowance with the label `degraded`, and C6's acceptance line changed to "stops and reports".
2. **Blocking, C8 (small).** The output and the advisory-only rule are exact (stderr, exit 0, plain view, cap of 5, `_encode`). The input is not: "a section headed `## Implementation closeout`" is an equality or a prefix, and the template's heading is `## Implementation closeout -- <agent> -- <date>` (equality never fires); "labeled line", the fence marker, the line-number base and whether `Home: <placeholder>` counts are undefined. Test 1 builds its own plan, so it cannot catch a heading mismatch. Closes: say "heading starts with", define the other four, and have test 1 use the template's heading verbatim.
3. **Non-blocking, C7 and C8: stale pointer, appendix.** (a) Shipped `templates/core/dev/PLANNING.md` lines 127 and 152-153 and `dev/PLANNING.md` line 287 cite `dev/plans/_template.md` > *Dispositions* as the governing text; C7 removes that heading and no chunk edits them. Closes: two exact S rows, one coordinator line, and a C9 grep that prints nothing. (b) The `_artifacts` skip is needed and not enough: on a scratch tree `tools/session.py` `_in_flight()` printed `proposals/2026-01-01-x--appendix.md -- (no status line)`, so session start lists the appendix as an open proposal; `session.py` is named in `dev/rules/protected-surfaces.md`. Closes: the author either extends the skip (Security Review) or has QA1 say the board does not list it and session start does.
4. **Non-blocking, row mechanics.** About 15 anchors break across lines (G4, PL3, QT13 and others). In the module a block quote puts `\n> ` inside a span, so TM8's whole first anchor greps 0 times and can fire the stop rule; say a `> ` prefix counts as a line break. The rules line "below the rule after `**Opened**`" names no such rule (it is a new line between `**Opened**` and `**In brief**`), and "I ... preceded by one space" would join it to the line above. The rules text counts 73 words, not 78.
5. **Non-blocking, order and ownership.** Gate C7 on C5 and C8 on C1, and fold C1 into C2 (eight chunks; seven if finding 1 closes by rows). The upgrade note has an owner (the coordinator) but no acceptance line.
6. **Non-blocking, the plan's own gate.** `python scripts/claim_check.py` on this plan prints one hard flag, at line 22 (not in this review): the `Proposed paths:` declaration of the proposal's archive path is stale because the path now exists (the proposal moved in `6986fafe`). Closes: the author deletes that one declaration line and keeps the new test's path.

Author-reported gaps, verified: rules text 73 words against the proposal's "about 20" stays inside the Decision (both template targets still hold); no closeout section existed (`grep -n closeout` finds only `docs/methodology/lifecycle.md` line 92), so the heading is the plan's and stays inside the Decision; the two targets are finding 1; the appendix skip is finding 3b. Frozen: no plan path is an exact entry in `frozen_files` (167) or `protected_roster`; `dev/plans/_template.md` and `tools/board.py` appear only in test node IDs; `repin.py status` lists 24 FROZEN-MODIFIED, none of these paths. Order and shared files are true: the heavy-tier plan (line 47) lists the same group 2 order, staged modules gates its C1 on this plan's README edit, release tests names none of these files, and Scope line 43 has each chunk re-read `git status` and `git log -5` (C9 checks it). No wording-pin test is added: the new test asserts the file name and line number, and a search of the tests for 26 phrases from deleted rows found none that pin them.

**Does any rule weaken or disappear?** No security rule I checked. I read the M spans of C5 and C7 for rule words (explanation, or the rule lives in the guide: PL11's seven sentences land in G11 and G11b) and the survivors of 14 D rows (PL1 to PL5, PL7, PL8, PL10, PL14, PL16, QT1a, QT1b, QT7, QT13). Three small conditions soften: PL3 "stop that action", PL4 "non-cheap advice keeps its existing disposition", QT1b "by name"; none carries a Security Review. C4 and C6 cannot be answered until their rows exist.

**Security question (one line, the Security Review owns it):** R2 covers only C8 and part of C6; whether the security-bearing sentences moved in C3 to C7 need a Security pass while templates stay high-risk is for the Security Review.

**Coverage**: Replayed every row's anchors by script (each first anchor matches once) and the module and guide counts; HEAD moved to `c94eec50` during the pass, and the plan file is unchanged since `a36f7513`. Not covered: survivors of G2, G4, G6 to G8b, G10, QT2b and QT9; `claim_check` on an appendix; running any test or edit; Windows; C4 and C6 output. Over target (about 950 words against 300) because two findings are blocking and each needs its numbers.
