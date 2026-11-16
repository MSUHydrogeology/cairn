# Plan: Trim the authoring templates, testing module and collaboration guide; list the rules that apply

**Source proposal**: dev/proposals/archive/2026-11-16-claude-template-trim-and-rules.md
**Author**: Claude Sonnet 5.5 (`claude-sonnet-5-5`, Medium), plan author
**Status**: revising-plan
**Waiting on Maintainer**: allow or refuse the Scope delta
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-16
**Rules that apply**: dev/rules/working-agreements.md, dev/rules/protected-surfaces.md, dev/rules/conventions.md
**In brief**: Agents will read about 3,300 fewer words in five shipped files with every rule kept, each plan and proposal will name the rule files that apply, and a plan cannot archive with leftovers that have no home.

## Build summary

After this plan an agent starting a task loads less text. The plan template, proposal template and vendor wrapper reach the accepted word targets. The testing module and the collaboration guide shrink by 515 and 609 words but stop 219 and 707 words short of their targets, because every sentence left in them states a rule, a limit or an example; the Scope delta asks the Maintainer to allow that. Duplicated text is deleted where the rule survives elsewhere and explanation moves to the published docs. Every chunk applies exact rows or exact text, so a Low-tier agent decides nothing. Both templates gain a `**Rules that apply**:` line. The plan's Dispositions section becomes an Implementation closeout record in which every "not run, not covered or remaining" item names a Home, and `tools/board.py` warns on stderr when a plan at `ready-to-archive` has an item with no Home. The testing module gains the accepted test-cut rule and its exemption, a time owner, a clean-checkout run and the part-by-part principle.

**Length.** This opening is about 8,100 words against the 1,000-word target. About 4,700 of them are the exact rows and new texts of C2 to C8, which are the design; leaving them out would hand rule rewriting to the implementer, which the proposal forbids, and the Internal review returned C4 and C6 for exactly that.

## Source proposal

The heavy-tier proposal (`dev/proposals/archive/2026-11-16-claude-template-trim-and-rules.md`, accepted 2026-11-16: "Let's accept all five as revised") sets a word target per file, moves explanation to documentation, adds the rules line, folds Dispositions into the closeout record with an advisory `board.py` warning, and adds five testing sentences and an appendix rule. It keeps #74, #76 and #79 in a held follow-on and keeps the test-cut rule in the shipped `testing-discipline` module. No operative rule may leave loaded text without the Maintainer's quoted word.

Proposed paths:
- `bootstrap/tests/contract/test_board_closeout_warning.py`

## Scope

**Result.** Measured with `wc -w` at `1fa1d898` (the paths are clean there). "After rows" is the author's replay by script of every row and text of C2 to C7 (the Internal review's replay of C3, C5 and C7 matched). The module and guide miss their targets by 219 and 707 words; the Scope delta (U1, U2) asks the Maintainer to allow it.

| File (Cairn's copy in brackets) | Now | After rows | Target |
|---|---|---|---|
| `templates/core/dev/plans/_template.md` (4,859) | 4,871 | 3,769 (3,757) | 3,900 |
| `templates/core/dev/proposals/_template.md` (4,599) | 4,275 | 3,398 (3,722) | 3,400 |
| `templates/modules/team-gated/testing-discipline.md` (equal copy) | 2,134 | 1,619 | 1,400 (219 over) |
| `templates/core/dev/agent_collaboration.md` (6,190) | 6,116 | 5,507 (5,586) | 4,800 (707 over) |
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
- `CHANGELOG.md`, `dev/PLANNING.md`, moving the proposal: the coordinator at closeout, not implementers. The `dev/PLANNING.md` change is one line: at "Archive preconditions" (line 288) `> Dispositions` becomes `> Implementation closeout`, because C7 removes that heading. The shipped `templates/core/dev/PLANNING.md` has the same two pointers; C7 rows PM1 and PM2 fix them.
- `tools/session.py`: a protected surface, and the Decision does not ask for it. Session start lists a proposal-folder file named `<stem>--appendix.md` as an open proposal with `(no status line)` (measured by the Internal review on a scratch tree); the appendix sentence of C7 says so.
- `docs/methodology` text on the `Dispositions:` block: it already says "closing metadata", which the closeout record is.
- A test-record tool (#81): principle only, by the proposal. An upgrade-merge trial on an adopter tree: not requested.

**Upgrade note** (for the coordinator's changelog): "Before upgrading, move any rule lines you added to Cairn's authoring templates or collaboration guide into `RULES.md` or `dev/rules/`. Taking Cairn's new text in a merge conflict loses a line you added."

**Reuse.** The warning reuses `_artifacts`, `_header_fields` and `_encode` in `tools/board.py`. Searched `grep -n "^def _" tools/board.py`: `_waiting` and `_roadmap_waits` read plan text for other markers but share no grammar. The count and cut checks are throwaway scripts.

### Documentation / doctrine surface

Governing text: both templates, the module, the guide, `VENDOR.md`, both rules READMEs. Deliberation: `dev/rules/protected-surfaces.md`. Descriptive: moved explanation is appended verbatim under `## Moved from the <file> in the v0.8 trim` in `docs/methodology/plans.md`, `proposals.md`, `dual-review.md` and `docs/further-reading.md`. No doctrine-evolution gate is claimed: the Maintainer's direction is the authority and the appended text adds no rule. Every moved span was read for a rule. Four rules were found and stay in shipped files: three sentences in the proposal template that say what the security questions and the path checker do not prove (C7 does not move them), and one sentence on shared test setup in the module (C4 row M9b). Cairn's `docs/` does not ship, and the Decision says moved text lands "for adopters, a shipped file, never Cairn's own `docs/`" while also sending explanation "to documentation"; the Scope delta (U3) asks the Maintainer to settle that for the explanation-only spans.

## Sequence

**Every chunk.**
1. `git branch --show-current` prints `0.8-dev`. Claim the paths (`python tools/intent.py claim --files <paths> --action "<what>" --stem trim<N>`), commit by explicit path, never push, never edit `CHANGELOG.md`.
2. Re-measure with `wc -w` and find each span by grepping its first words. Counts differ if an earlier plan landed. An anchor matching 0 or 2 times: stop, return to the plan author.
3. A span runs from its first anchor word to its last, line breaks ignored. A `> ` at the start of a line counts as a line break, not text, and no anchor includes it. **D** deletes the span and one adjacent blank line (a bare `>` line counts as blank, and a span that starts or ends a block-quoted line takes that line's `> `). **M** is **D** plus appending the deleted text verbatim to the named docs file. **S** replaces the span by the given text; where the row says M, the replaced words are appended too. **I** inserts the given text after the span, preceded by one space. **N** inserts the given text as its own line or paragraph directly after the line or paragraph the anchor ends. Retype, rewrap or reorder nothing else (`scripts/exact_replace.py` or an exact Edit).
4. Before a D row, read its survivor (the home named) and confirm the rule is there. A survivor is never cut. Home codes in the tables: PR = guide "Plans and records", RR = guide "Review rules", RL = guide "The review loop", VF = guide "Verification", PA = plan template "Plan amendments", WL = plan template "The Waiting line", AG = `AGENTS.md` "Lifecycle and records". A deleted sentence with a condition the survivor lacks: stop, return to the author; the carried text this plan lists is the only exception.
5. Apply every row to the Cairn copy too; a row whose anchor is absent there is skipped and named in the commit body. Afterward `diff <shipped> <cairn>` shows only the hunks it showed before.
6. No-weakening check, every prose chunk. A throwaway script lists, from `git show <base>:<path>`, each sentence containing `must`, `never`, `only`, `required`, `requires`, `cannot`, `may not`, `do not`, `does not`, `refus`, `always`, `owes`, `unless`, `stop`, `no agent`, `waive`, `exempt`, `hostile`, `negative`, `guard`, `fence` or `Maintainer`, with its best match in the new file. At `1fa1d898` the shorter list gave 94 sentences in the plan template, 64 in the proposal template, 131 in the guide, 24 in the module and 4 in the wrapper; the added words raise them, and the implementer's script sets the figures. Each is verbatim, deleted or shortened by a row of this plan whose survivor holds it, or the chunk stops. A shortened sentence that can be read two ways keeps its original: stop and return to the author. The row tables are the ledger; append nothing.
7. The commit body gives words before and after, the rows applied, each rule removed or changed with its home, and the tests run.

| # | Chunk | Tier | Gate | Ships |
|---|---|---|---|---|
| C1 | Pin scan | Low | `0.8-dev` exists | scan result |
| C2 | Vendor wrapper, rules README sentence | Low | C1 | 3 files, 2 copies |
| C3 | Testing module: exact rows, new rules | Low | C1 | module copies, protected-surfaces, further-reading |
| C4 | Testing module: exact cut rows | Low | C3 | module copies |
| C5 | Guide: exact rows, carried sentences | Low | C1 | both guides, dual-review |
| C6 | Guide: exact cut rows | Low | C5 | both guides |
| C7 | Plan and proposal templates, shipped `PLANNING.md` | Low | C6 | 5 templates, plans, proposals |
| C8 | Board warning, appendix skip, test | Low | C7 (test 1 reads C7's closeout heading) | 2 board copies, 1 test, tier map |
| C9 | Sweep and lock | Low | C8 | lock record; last chunk |

Assumed, not measured: 6 to 8 agent-hours and two code reviews. Every chunk applies given rows or text; none asks the implementer to write or choose prose. The testing text goes first (C3, C4); Boundary A, B and C sentences stay verbatim, checked first in C5.

### C1 Pin scan

Throwaway script: lowercase, strip quotes and `*_#>`, collapse spaces, take every six-word run of the five shipped files and their Cairn copies, search every `test_*.py` under `bootstrap/tests`, `scripts`, `tools` and `templates/modules/team-gated` (`dev/rules/working-agreements.md` > Tests). Measured 2026-11-16: none pins prose. Hits: one placeholder line in `test_board_json_contract.py`, an unrelated phrase in `test_reanchor.py`, a slot placeholder in `test_agreement_retired.py`, a docstring in `tools/test_tiers.py`. The scan finds copied runs, not paraphrase. Structure that tests read, which no row may break:
- Both templates: one `**In brief**:` line below the first `---` with its placeholder; `**The summary line.**` above it; plan only: `**Waiting on Maintainer**:` above the rule and not in the header block, one `acceptance-doc-tooling` slot; every slot and its end marker; no one-word `{{x}}`; shipped bytes install unchanged.
- Guide: all 14 `##` headings (ten are cited by `AGENTS.md`), the role bullets, every slot, no `cairn:` marker inside "The review sweep", Plain Language unchanged.
- Module: `dev/modules/testing-discipline.md` byte-equal to shipped.
- `VENDOR.md`: line 1 `# Vendor wrapper — {{project_name}}`, `@AGENTS.md` within the first five lines (rename detection in `bootstrap/_scaffold/upgrade.py`), slot `vendor-addendum`.

A new wording pin that is not frozen: delete the test and name it, unless it sits in a security-family file (`bootstrap/tests/security_manifest.py`) or guards a surface in `dev/rules/protected-surfaces.md`; then stop before deleting it and ask for a Security Review. A frozen one: stop.

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
| TM1 | `Cairn requires a change to **absorb … a complete testing curriculum.` | S; the rationale and Cairn's own-tests narrative are M, except the sentence `Shared immutable setup … stay per-test.`, a rule that C4 row M9b keeps in the module. Also delete line 1, `<!-- claim-check-allow: tools/test_tiers.json -->`, which nothing in the file needs after TM1 (`claim_check` is clean without it, measured on a scratch copy) |
| TM2 | ``**Worked contrast: a pin and … private reach in `scripts/test_coupling.py`.`` | M |
| TM3 | `**Worked useful/vacuous/broken contrast.** … not the expected value.` | S; the two examples are M |
| TM5 | ``A permanent test enters `tests/` only … a public entry point.`` | I (#88) |
| TM6 | `**The suite has a time … measures it.` | S (#86) |
| TM7 | `equivalence proof is required. A size … quota.` | I (#77) |
| TM8 | `remedy; optional architecture review is available, not required for every change.` | S (#81); the deleted clause is M |

Texts:
- TM1: `This module gives the suite a shape, a way to choose tests, and a budget. The guidance below is a practical summary, not a complete testing curriculum.`
- TM3: `**Observe the failure first.** Observe a new check fail before fixing behavior; fix the behavior, not the expected value.`
- TM5: `Run each new test once on a clean checkout before keeping it, so it does not depend on state only your machine has.`
- TM6: `**The suite has a time budget and an owner.** The project names who owns the ordinary run's time, sets how long it may take, and measures it. Review the slowest test files on a stated schedule, such as each release.`
- TM7: ``A test that is not clearly a public promise is not kept; a higher-tier agent decides each judgment call. These are exempt and are cut only through a Security Review: tests of the surfaces your project's `AGENTS.md` names as high-risk, tests your project's release or security records name as guards, and refusal, hostile-state and negative-guard tests.``
- TM8: `remedy. A large project is not one piece: test each part where it lives. A change may be verified from current results in place of a whole-suite run; a release's own whole-suite and security-family run is never replaced by earlier results, and a release may reuse results only where a reviewed rule allows it.`

Also append to `dev/rules/protected-surfaces.md` (Cairn-only): ``Tests exempt from the promise-only cut. Cut only through a Security Review: tests of the surfaces above; the security-family files and native-only IDs in `bootstrap/tests/security_manifest.py`; tests that a release document, `bootstrap/SAFETY.md`, `bootstrap/_scaffold/SECURITY_MUTATIONS.md` or a shipped file names as a guard; and refusal, hostile-state and negative-guard tests. The generic rule is in the testing-discipline module.`` M spans go to `docs/further-reading.md`. No rule is deleted.

### C4 Testing module: exact cut rows

After C3 the file is 1,900 words. Apply these rows to both copies, identically; the result is 1,619 words and the copies stay byte-equal. The target is 1,400. The 219 words between are the Scope delta's U1: every other sentence in the module states a rule, a limit or an example, and none is cut without the Maintainer's quoted word. If a count differs from 1,619 by more than the words an earlier group 2 plan added, stop and return to the author.

No row touches a sentence with `refus`, `hostile`, `negative` or `guard` (checked by script at design time), so these stay verbatim: the whole `Refusals are promises too` paragraph; the whole `Negative tests prove the guards` paragraph; `The report names its Python-only gap and says refusal and hostile-state tests stay. It is a review prompt, not a deletion list.`; `one parameterized check per refusal class`; `Never add a test that pins the mutated line.`; the `Do not weaken assertions …` paragraph; the `Investigate surviving mutations …` paragraph; and the TM7 sentence. The three numbered items of `Simulation models verify at three timescales` and every C3 text stay as C3 left them.

| ID | Span | Kind and home |
|---|---|---|
| M1 | `**test-tier scheme** rather than an undifferentiated … paying for it by default.` | S: `**test-tier scheme**.`; the cut (why the module is team-gated) is M |
| M2 | `A tier communicates broad scope; the test name … specific behavior.` | M |
| M3 | `A test's tier is determined by where … scheme cannot rot.` | S: text below; the cut clauses are M; the rule (tier from location, no hand tags, a check fails for a test with no tier) stays |
| M4 | `More examples inside a regime rarely … find new faults.` | M |
| M5 | `A golden output is a change detector: … result is right.` | M |
| M6 | `optional: sample or generate varied … No input generator` | S: `optional; no input generator`; the cut is M |
| M7 | `changes -- the change then has to be deliberate.` | S: `changes.`; the cut is M |
| M8 | `Scope and cost are separate: … on its own.` | M; TM6 already says the run's time is measured |
| M9 | `Exercise the public command or API when practical.` | D, "Test promises, not wording or internals" (`Test it through the public entry point, in-process where practical.`) |
| M9b | after `fresh paths and mutable repositories for each case.` | I: `Shared immutable setup may use session scope when shuffled tests interleave modules; mutable projects, refs, keys, paths, and monkeypatches stay per-test.` (TM1's rule, kept in the module) |
| M10 | `Unit checks cover local behavior, … the real entry point.` | D, the tier list in "Test tiers are a single coherent scheme" |
| M11 | `Agents map routine coverage and reviewers … material exceptions.` | D, guide "Verification" (`Agents make this routine selection and reviewers challenge it; the Maintainer sets high-level project needs and material exceptions.`; C6 keeps it) |
| M12 | `in, so the suite's shape stays … as it grows.` | S: `in.`; the cut is M |
| M13 | ``## Relationship to `dual-language-tests` … for the seams.`` | D, `templates/modules/team-gated/dual-language-tests.md` (it says it extends the base module and that a multi-language project selects both) |
| M14a | `The tier scheme and the selection rules above are Cairn's summary of established testing practice:` | S: `These rules summarize established practice:` |
| M14b | `"Software quality for scientists" for … re-teaching.` | S: `"Software quality for scientists".`; the cut is M |

M3 text: `A test's tier comes from where it lives (its directory, or a per-tier configuration that maps file names to tiers), not from hand-tagging, and a check fails when a test has no tier.`

M spans go to `docs/further-reading.md`. The rows are the ledger; append nothing. Measured: 1,900 minus 281 is 1,619.

### C5 Guide: exact rows and carried sentences

Both guides (Cairn's G6 end anchor reads `need no extra sentence or inventory.`).

| ID | Span | Kind and home |
|---|---|---|
| G0 | `**The deliberation and decision process.** … shape they do.` | M |
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

M spans go to `docs/methodology/dual-review.md`. Shipped guide after rows: 5,681 (the bare `>` line beside G0 goes with it).

### C6 Guide: exact cut rows

After C5 the shipped guide is 5,681 words. Apply these rows to both guides; the result is 5,507 shipped and 5,586 in Cairn's copy (79 above, against 74 today). The target is 4,800. The 707 words between are the Scope delta's U2: every sentence still in the guide, apart from the Plain Language section the plan may not edit, states a rule, a limit or an example, and none is cut without the Maintainer's quoted word. If a count differs by more than the words an earlier group 2 plan added, stop and return to the author.

Kept verbatim, so no row touches them: every survivor named in a D row of C5 to C7, all C5 carried text, any sentence an earlier group 2 plan added (`git log -p`), any sentence naming Boundary A, B or C, `Bounding`, a model capability floor, a refusal or a Maintainer-only step, and `Agents make this routine selection and reviewers challenge it; the Maintainer sets high-level project needs and material exceptions.` (the survivor of M11).

| ID | Span | Kind and home |
|---|---|---|
| G-a | `Full definitions, and what each review owes, in … dual-review method.` (Cairn's copy ends `` `docs/methodology/dual-review.md`. ``) | D, a pointer; "Review rules" ends with the same pointer |
| G-b | `except the first; name your role … if it is not explicit, ask.` | S: `except the first.`; survivor `AGENTS.md` > Roles (`Name your role before substantive work; ask if it is not clear.`) |
| G-c | `its author, who is typically the stronger party on the software.` | S: `its author.`; the cut is M |
| G-d | `It is asynchronous and commit-mediated: … leaves no record.` | M |
| G-e | `A structurally-independent read is only independent if … its committer.` | D, the two sentences before it and `AGENTS.md` > Review (`Append the review to the artifact; its author commits it.`) |
| G-f | `A review that opens with findings reads as a verdict, … defends rather than thinks.` | M |
| G-g | `not relief: a reviewer who reads to confirm that the change works will find that … it does.` | S: `not relief.`; the cut is M |
| G-h | `A covered-only line manufactures false comfort.` | M |
| G-i | `A menu of five options with no recommendation moves … than unblocking it.` | M |
| G-j | `A reviewer who proposes a narrower scope names what would be lost; … concedes a loss.` | D, the scope-reduction trap paragraphs in "The review sweep" (`states what is lost`; `neither author nor reviewer may concede a baseline outcome`) and `AGENTS.md` > "Working tree and commits" (`A reviewer cannot grant it.`) |
| G-k | `Lead plain, with precision beneath; if you do not understand … the work, pause.` | D, Plain Language rules 1 and 2, "Collaboration stance", `AGENTS.md` > Roles |
| G-m | `A tool's private memory is not shared with another agent type or … with a human reviewer.` | M |
| G-o | `before then; a lesson that stays only in a reflection is a lesson that expires.` | S: `before then.`; the cut is M |

M spans go to `docs/methodology/dual-review.md`. The rows are the ledger; append nothing. Measured: 5,681 minus 174 is 5,507.

### C7 Plan and proposal templates

Both copies of each, after C6 so every survivor is final.

Rules line (N, both templates): as its own line directly after the `**Opened**:` line, above the `**In brief**:` line: `**Rules that apply**: {{rule file paths from the RULES.md routing table | bright lines only}}`. Paragraph (N, both templates): as its own paragraph directly after the `**Write for the reader.**` paragraph, which is above the rule: ``**Rules that apply.** List the rule file paths from the `RULES.md` routing table that apply, never rule text, or write `bright lines only`. A rule that applies but is not listed is still followed; add it to the line. The line never narrows a review, a Security Review trigger or a protected-surface obligation. Reviewers compare it with Scope.`` Together 73 words per template (counted); the proposal said about 20, and the required never-narrows sentence outgrows it. The trim pays for it.

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
| PL11 | `**More distance is the Maintainer's call, … Decision are the check.` | S, RR with G11, G11b; the sentence `Distance is information, not a rule: … different knowledge.` is M |
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
| QT11c | `**Prospective only.** This accounting applies … retro-fitted with it.` | D, the earlier "Prospective only" sentence |
| QT12 | `For example, an analysis that reports … distance and schedule.` | M |
| QT13 | `When work joins a connected … reopening the archived plan.` | D, VF |
| QA1 | ``Readers list them with `grep -n … the job needs.`` | N, appendix bullet below (#73) |
| PM1 | in `templates/core/dev/PLANNING.md`: `> *Dispositions* (and *Scope delta*,` | S: `> *Implementation closeout* (and *Scope delta*,` |
| PM2 | in `templates/core/dev/PLANNING.md`: `*Dispositions*; a priority label is not a reason.` | S: `*Implementation closeout*; a priority label is not a reason.` |

Texts (PL rows apply to the plan template, QT and QA rows to the proposal template):
- PL5: `A fence is for a Decision or permission needed to carry out accepted scope, not a routine human-run trust or release operation.`
- PL11 and QT3: ``**More distance is the Maintainer's call, and only theirs.** See `dev/agent_collaboration.md` > "Review rules".``
- PL12: `Code review's floor is not the implementing agent, and it never reopens the Decision.`
- PL19a: `## Implementation closeout -- <agent> -- <YYYY-MM-DD>` then a blank line then `*Appended at archive-preparation`.
- PL19b: ``doctrine").* Say in a few lines whether each acceptance criterion held. Write each check not run, area not covered or work remaining as its own item: `Not run: <what>`, `Not covered: <what>` or `Remaining: <what>`, ending `Home: <roadmap row, issue, proposal or the Maintainer's quoted word>`. An empty Home means the plan is not ready to archive. A deferral of accepted scope or of a required check has the Maintainer's quoted word as its Home; a Home an agent creates alone (an issue or a roadmap row) covers only a follow-up that defers neither. Then record one``. The rest of the old section stays: the `Dispositions:` line, `accept`, `guard`, `wontfix` with its limits, `defer`, the batch and Waiting-line rule.
- PL20: ``do not copy template instructions or the `## Implementation closeout`,``
- QA1: as its own bullet directly after the `**Read by section.**` bullet: ``* **Appendix.** Default none. Allowed only for a table or arithmetic a reviewer must check that no cited record can hold: one separate file per proposal, `<proposal-stem>--appendix.md`, beside it, never inline. The board skips it; session start still lists it. The 1,000-word budget applies to the text at the Decision, so cut or move review additions before it.``

Not rows, by the Security Review: the three proposal-template sentences that say what the checks do not prove (`Structural questions about where material … a reviewer can falsify.`, `**What they do not reach.** A … finds it.`, `These are author declarations, not inferences: … it was right.`) stay where they are. They are caveats against reading the security questions and the path checker as proof, and Cairn's `docs/` does not ship. They are 73 words of the proposal template's 3,398.

M spans go to `docs/methodology/plans.md` (PL) and `proposals.md` (QT, QA). Reserve, only if a count is over target (an earlier group 2 plan adds words to the proposal templates, and 3,398 leaves 2): for the proposal template, cut the slot sentences `Trace changed behavior through callers … plausible uncovered faults.` (51 words, shipped copy only), and in the guide's "Verification" (both guides) replace `shared contracts, common infrastructure and solver behavior widen` by `shared contracts, common infrastructure, language seams, solver behavior and uncertain dependencies widen` (+5 words). Still over after the reserve: stop and return to the author; no other cut. None for the plan template.

### C8 Board warning, appendix skip, test

Edit `templates/skills/_lib/board.py` (the source), then copy it byte for byte to `tools/board.py`. The implementer writes the code from these criteria; each is exact.

**Warning.** Add `_closeout_warnings(root, encode)`, which returns a list of lines. `main` calls it in the plain view only (not `--json`, `--next` or `--maintainer`), after printing the table, and prints each returned line to stderr. Stdout and the exit status (0) are unchanged. It reads plans only through `_artifacts(root, False, [])`, kind `plan`, so archived files are never read.
- It reads a plan when `_header_fields(text)["Status"]` matches `^ready-to-archive(?![A-Za-z0-9_-])`.
- Lines are `text.splitlines()`, numbered from 1 at the first line of the file.
- A fence line is one whose stripped text starts with three backticks or `~~~`. Each fence line toggles a fence; fence lines and the lines between them are never read.
- A closeout section opens at a line that starts `## Implementation closeout` followed by the end of the line or a space (so the template's `## Implementation closeout -- <agent> -- <YYYY-MM-DD>` opens one and `## Implementation closeouts` does not). It ends before the next line that starts `## `.
- An item starts at a line inside a closeout section that, after leading spaces and at most one `- ` or `* `, begins `Not run:`, `Not covered:` or `Remaining:`. It runs through the following lines up to, not including, the next blank line, the next item-start line or the next line that starts `#`.
- An item has a Home when its joined text holds `Home:` followed by optional spaces and then a character that is neither a space nor `<`. An unfilled `Home: <roadmap row, …>` has none.
- Each item with no Home gives `board: warning -- <file>:<line> has no Home`: `<file>` is the plan's file name through `_encode()` (escaped, elided at 48) and `<line>` is the item's first line. Plans come in sorted file order and items in line order. At most 5 lines are returned, then `board: warning -- <k> more not shown`, k being the number not shown.

**Appendix skip.** In `_artifacts`, for kind `proposal` only (`dev/proposals` and its archive), skip a file named `<stem>--appendix.md` when `<stem>.md` is in the same folder and `_header_fields` of the file is empty. Every other file is listed as today, so an appendix that carries a `**Status**:` or `**Waiting on Maintainer**:` line is still seen by `--json` and `--maintainer`, and a `--appendix.md` file under `dev/plans` or with no sibling is still listed by `--json`. The module docstring gains two sentences, one for the warning (stderr only, never stdout or `--json`) and one for the skip. For a tree with no appendix file, `--json` output and exit codes are unchanged.

New `bootstrap/tests/contract/test_board_closeout_warning.py`, through `board.main` on a scratch tree it builds. The closeout heading in its plans is the line of `templates/core/dev/plans/_template.md` that starts `## Implementation closeout`, read at test time, so the board and the template cannot drift apart. Eight tests:
1. A Home-less item warns: stderr holds the plan's file name and the item's 1-based line number (not the message wording), and stdout equals stdout for the same tree with a Home.
2. The same item with `Home: roadmap row 7` is silent; with an unfilled `Home: <roadmap row>` it warns; an item inside a fence is silent.
3. An `implementing` plan, and a plan under `dev/plans/archive` (also with `--archive`), are silent.
4. `--json`, `--maintainer` and `--next` on the Home-less tree print nothing to stderr, and `--json` is valid `cairn-board/1`.
5. A 120-character plan name with an ESC character, and closeout text with ESC and control characters, print no raw ESC and none of the closeout text (the ESC name is skipped where the filesystem refuses it).
6. 12 Home-less items print exactly 6 lines, the last naming 7 more.
7. `tools/board.py` and `templates/skills/_lib/board.py` are byte-equal.
8. Appendix skip, four cases: a headerless `<stem>--appendix.md` beside its proposal is absent from the plain view and `--json`; the same file with `**Waiting on Maintainer**: x` is listed by `--maintainer` and `--json`; one with no sibling and one under `dev/plans` are listed by `--json`.
Also run, not rewritten: `bootstrap/tests/test_board_json_contract.py`, which covers both board copies.
Add `test_board_closeout_warning` to the `contract` tier in `tools/test_tiers.json`: after `"test_test_tiers"` add a comma and a new line `"test_board_closeout_warning"`.

### C9 Sweep and lock

Run Verification. For each changed lock-tracked file (`dev/plans/_template.md`, `dev/proposals/_template.md`, `dev/agent_collaboration.md`, `dev/modules/testing-discipline.md`, `dev/rules/README.md`, `CLAUDE.md`, `tools/board.py`) run `python bootstrap/scaffold.py upgrade --target . --finalize <path>`, commit `dev/.cairn/cairn-lock.yml` alone, then `python bootstrap/verify_integrity.py --target .`. Run `grep -n "> \*\?Dispositions" templates/core/dev/PLANNING.md`: it prints nothing (the coordinator's `dev/PLANNING.md` line 288 is checked the same way once it lands). Put the counts table in the commit body and end this plan with its closeout record in the new form, carrying the upgrade note as an item whose Home is the coordinator's changelog entry.

## Acceptance criteria

**C1.** The scan names its inputs and four test folders; its result is in the C2 commit body. No frozen test is edited; `python scripts/repin.py status` lists the same frozen-modified files before and after the plan.

**C2.** `templates/core/VENDOR.md` is 154 words, line 1 `# Vendor wrapper — {{project_name}}`, `@AGENTS.md` on line 4. Shipped `AGENTS.md`, `VENDOR.md` and `RULES.md` total at most 1,500 words (planned 1,339); Cairn's three at most 2,000 (planned 1,414). Both READMEs carry the new sentence once. The wrapper-rename nodes of `test_upgrade.py` pass.

**C3.** All seven rows are applied to both module copies, which stay byte-equal; line 1 is gone; the #77, #86, #88 and #81 sentences each appear once; the file is 1,900 words. The protected-surfaces paragraph exists. Removed spans appear verbatim in `docs/further-reading.md`, except the shared-setup sentence of TM1.

**C4.** Both module copies are 1,619 words and byte-equal. Every row M1 to M14b is applied once; the C3 texts and the verbatim list are untouched; `claim_check` is clean on both copies. The rows answer "Does any rule weaken or disappear?" one by one: none removes a rule, and M9b keeps the one rule found in a moved span. The 219 words over target are the Scope delta's U1.

**C5.** Every row is applied to the shipped guide and, where its anchor exists, to Cairn's; the shipped guide is 5,681 words. The 14 headings and Plain Language are unchanged. Each D row's survivor was read first. Each carried text is present once. M spans are in `dual-review.md`.

**C6.** The shipped guide is 5,507 words and Cairn's 5,586, each differing only by words an earlier group 2 plan added. The Plain Language section diffs empty; headings, role bullets and slots remain. Survivors, carried text, Boundary and floor sentences are verbatim, and each D row's survivor was read first. The 707 words over target are the Scope delta's U2; the commit body states them.

**C7.** Plan template at most 3,900 words (planned 3,769), proposal template at most 3,400 (planned 3,398). Both carry the rules line and paragraph. `## Dispositions` is gone; `## Implementation closeout` carries the Home rule, the deferral rule, the `wontfix` limits and the executing-`guard` rule. The three caveat sentences on what the security questions and the path checker do not prove are still in the proposal template. The shipped `PLANNING.md` says `Implementation closeout` in both places. The C1 structure list holds, shipped bytes install unchanged, and Cairn's copies differ from shipped only as before.

**C8.** The eight tests pass once on a clean checkout, `python tools/test_tiers.py check` passes, the board files are byte-equal, and `test_board_json_contract.py` passes for both copies. The warning prints only a file name and number. S2 (it can fail): tests 1, 5 and 8 fail without the code. S3 (what fires it): `python tools/test_tiers.py for tools/board.py` lists the new file and the contract file.

**C9.** The commit body has the counts table and each chunk's shared-file re-read. The lock records the seven paths and `verify_integrity` passes. `git diff --name-only` since C1 names no `frozen_files` entry. The grep for `Dispositions` pointers prints nothing. The closeout lists each item not run or not covered with its Home, including the upgrade note.

## Scope delta

**Scope delta**: degraded

**What the Maintainer is asked to allow, in plain words.** The Decision adopted five word targets and the rule that no rule may leave the files agents read "without the Maintainer's quoted word". Three targets are met: the plan template at 3,769 words (target 3,900), the proposal template at 3,398 (3,400) and the vendor wrapper at 154 (170). Two are not, because I found nothing more to cut without removing a rule. Counts are `wc -w` on a script replay of this plan's rows, not on the tree.

- **U1, testing module.** Lands at 1,619 words, not 1,400: 219 over (16 percent); today 2,134. C4 removes 281 words net (302 cut, 21 added by M9b), all explanation, duplicates and pointers. Every sentence left states a rule, a limit or an example. Reaching 1,400 would remove about 219 more words of rules. **disposition**: accept (owed: the Maintainer's quoted allowance; none yet).
- **U2, collaboration guide.** Lands at 5,507 words, not 4,800: 707 over (15 percent); today 6,116. C6 cuts 174 words of the same kinds. Reaching 4,800 would remove about 707 more words of rules; the External-read paragraph alone is 340. **disposition**: accept (owed: the Maintainer's quoted allowance; none yet).
- **U3, where explanation lands.** About 1,200 words of explanation (worked examples, reasons, notes on Cairn's own test suite) move to Cairn's `docs/`, which adopters do not receive. The Decision says moved text lands "for adopters, a shipped file, never Cairn's own `docs/`" and also that detail moves "to documentation". I read every moved span for a rule and kept the four that were rules in shipped files; the rest is explanation, and the Decision does not say outright that it may land in Cairn's `docs/`. **disposition**: accept (owed: the Maintainer's quoted allowance; none yet).

**Why the targets do not fit.** No rule is dropped to meet a number. The files shipped to adopters have no documentation folder, and a new shipped file needs an install-list change in `bootstrap/_scaffold/install.py` (a protected surface), which is a new proposal, not this plan.

**Cost to adopters if the Maintainer allows it.** Nothing they relied on is lost. Everyone who installs reads 707 more words in the guide than the target says, and those with the testing module read 219 more (against 609 and 515 fewer than today). If the explanation in U3 is wanted by adopters, they must open Cairn's published docs.

**Cost if the Maintainer refuses.** For U1 and U2 the Maintainer names, rule by rule, which rules to drop, each with a quoted word (the Decision's own condition); the plan then returns for new rows and a fresh review. For U3 the explanation is deleted instead of moved, or a new proposal adds a shipped home for it.

**Recommended default: allow U1, U2 and U3.** Every rule stays; the price is the extra words named above.

**Maintainer's allowance** (quote verbatim, with source):

## Verification

Changed promises and entry points: the warning (`python tools/board.py`), both templates through install, module copy equality, the wrapper's rename detection, the 1,500 and 2,000 caps. Per chunk run `python tools/test_tiers.py for <changed paths>` and only the files it lists; never the whole suite. By reading, that is `test_board_json_contract.py` (read-only, templates and both board copies), `test_review_sweep_ships.py`, `test_writing_rules_ship.py`, `test_review_stance_in_shipped_files.py`, `test_scientific_check_guidance_ships.py`, `test_scope_reduction_trap.py`, `test_install_report_slots.py`, `test_verification_boundaries.py`, `test_practice_modules.py`; for `VENDOR.md`, `test_upgrade.py -k "vendor or VENDOR or wrapper"` and the one node `test_scaffold.py -k test_full_install_seeds_rules_md_within_word_budget`. Interpreter: `/Users/kendal30/conda_envs/lhm/bin/python3.13`.

Prose gates on each changed prose file: `python scripts/claim_check.py`, `python scripts/link_check.py`, `python scripts/sync_doc_snippets.py --check`, `python scripts/quality_gate.py --sub neutrality`; counts by `wc -w`. Code reviews: R1 (Internal) over C1 to C7 and C9, with the reading question answered row by row from the C3 to C7 tables; R2 (Internal Security Review) over C8, and over "Review rules" in C6 if the template-scan change has not landed.

Not run, to be homed at closeout: the whole suite and security family, Windows, an upgrade-merge trial on an adopter tree, any desktop-app behavior of `AGENTS.md`, any application of the rows to the tree (the counts here come from a script replay).

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

## Plan review -- Claude Opus (Security Reviewer, High) -- 2026-11-16

```
Reviewed commit: 23c10ac7c7cc3879b7184742dd11a95977114886
```

**Obligation**: Internal Security Review: decide whether any cut or moved row weakens, removes or blurs a security, review, trust-boundary, protected-surface, fence, Maintainer-only or stop rule beyond what the 2026-11-16 Decision allows, and whether the C8 board change hides an artifact or stops being advisory.
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: about 5 minutes of my own pass (16:20 to 16:25 EST, measured with `date`)
**Tokens**: unknown

Steelman: every security-bearing D row I sampled has a survivor that holds its condition, the carried texts G11, G11b and G12 restore what the templates had and the guide lacked, and the board warning matches the proposal's advisory limits point for point.

**Foundations**

1. **Should this happen as framed?** Yes for the exact rows: the 14 sampled rows below keep their rule, and the Obligation-pass clearing rule stays verbatim in the plan template, touched by no row -- `templates/core/dev/plans/_template.md:176-180`; my span script over the shipped files at `23c10ac7`
2. **Best alternative.** None simpler for the board: the appendix skip is needed (Internal finding 3b) but can be narrower at no cost (finding 3) -- `tools/board.py:879-911`, where `_artifacts` also feeds `_waiting` (line 945) and `--next`
3. **What would show it wrong.** A C4 rewrite shortening a refusal or negative-guard sentence with no ledger row, because step 6's keyword list does not catch it -- plan line 74; `templates/modules/team-gated/testing-discipline.md:94-97`, `:117-120`

**Findings**

1. **Blocking, M rows QT11b, QT14, QT15.** These three sentences in the shipped proposal template's high-assurance block state what the checks do not prove: S1 to S5 "do not check whether an answer is *true*", a hostile valid instruction "carries no lexical signature", and the checker "attests that a path was declared, never that it was right". The plan moves them to Cairn's `docs/methodology/proposals.md`, which adopters do not receive. The Decision (proposal item 1) says moved text lands "for adopters, a shipped file, never Cairn's own `docs/`". Without them an adopter can read the security questions and the path checker as proof. Closes: keep the three in place (about 70 words; the template is planned at 3,321 against 3,400).
2. **Non-blocking for this lane; needs the plan author or the Maintainer.** The same Decision sentence covers every other M row out of a shipped file (G0, G1, G5, PL6, PL9, PL13, PL15, QT4 to QT6a, QT11, QT12, TM1 to TM3, TM8). I read them as explanation, not rules, but a Cairn-only destination departs from the accepted text. Closes: a shipped destination, or the Maintainer's quoted allowance.
3. **Non-blocking, C4 keep list and doubt rule (folds into Internal finding 1's fix).** C6 keeps verbatim any sentence naming a refusal or a Maintainer-only step; C4 has no such list, and step 6's keywords miss "Refusals are promises too" with its one-test-per-refusal-promise rule and "A guard with no negative test is an unproven guard". The TM7 exemption stays verbatim (C4 criterion), so refusal tests still cannot be cut without Security Review; what could go is the rule to write them. Closes: C4 keeps verbatim, or ledgers, each sentence containing `refus`, `hostile`, `negative`, `guard` or `Security Review`, and step 6 adds those words plus `fence` and `Maintainer`. The plan has no doubt rule; add one: a shortened sentence that can be read two ways keeps the original. (The existing "Uncertainty resolves to `high-assurance`" survives; QT15 starts after it.)
4. **Non-blocking, C8 appendix skip.** `_artifacts` feeds the table, `--json`, `--next` and `--maintainer`, so any `*--appendix.md` with a Status or Waiting line vanishes from all four, and the skip covers `dev/plans` though QA1 allows appendices only beside proposals. A leading `_` already hides a file the same way, so the consequence is small. Closes: skip only under `dev/proposals` and its archive, only when the sibling `<stem>.md` exists and the file has no `**Status**:` line; test 8 adds one listed case for each. The warning stays advisory exactly as proposed (stderr, exit 0, plain view, `_encode`, cap; tests 1, 4, 5, 6).
5. **Non-blocking, C1.** "A new wording pin that is not frozen: delete the test" also reaches the new exemption. The scan found none; add one clause: a pin in a security-family file or a `dev/rules/protected-surfaces.md` surface stops for Security Review.

Sampled rows (survivor, shipped file): G2 (guide :356); G4, QT9 (plan template :417-430 keeps reuse limits, "expands the selection", "Preserve required security checks and reviews"); G7, G7b, QT2b (guide :95-98, blocking meaning and no waiver); G8 (plan template :74, cap across replacements); PL4 with G15 (guide :358); PL5 with G13 (guide :411); PL8 (plan template :79-83); PL10 with G9 (guide :451); PL11, QT3 with G11, G11b (guide :360); QT1a, QT1b with G12 (`templates/core/AGENTS.md:32`); PL19b (keeps `defer` with the Maintainer's verbatim word, `wontfix` limits, executing `guard`; the Scope delta archive block at :406 is untouched; no `.py` file reads `## Dispositions`). Rules line: an unlisted rule still applies, it never narrows a Security Review trigger, reviewers check it against Scope; safe.

**Does any rule weaken or disappear?** No security rule in the exact rows; the Internal pass's three softenings carry no Security Review. Finding 1 removes three security caveats from adopters against the Decision's wording. C4 and C6 cannot be answered until their rows exist. The check for lost normative sentences is step 6's inventory plus the ledgers; finding 3 is its smallest repair. Frozen: no planned path in `gate_manifest.json` (exact-string search, 20 paths); `repin.py status` at 16:23 lists 25 FROZEN-MODIFIED, none planned. The new test pins no wording.

**Coverage**: Read the plan, the Internal pass, proposal items 1, 4, 5, 6 and both proposal Security Reviews, and 29 spans by script. Not covered: G0 (block-quote anchor not extracted), G6, G10, QT7, QT13, Cairn copies' extra paragraphs, C4 and C6 output, any test run, Windows. About 900 words against 450: a nine-chunk plan, and the sampled-row line is the evidence the obligation asks for.

## Response to plan review -- Claude Sonnet 5.5 (plan author, Medium) -- 2026-11-16

**Elapsed**: about 33 minutes (start 16:25, end measured with `date`)
**Tokens**: unknown
**Disposition**: awaiting the Maintainer's allowance of the Scope delta (U1, U2, U3); not `ready-to-implement`. Status becomes `revising-plan`. The plan moves to `ready-to-implement` only when the Maintainer's quoted allowance is in `## Scope delta`.

Conclusion: all three blocking findings are closed in the operative text, but the plan can no longer say `preserved`: the module lands at 1,619 words (target 1,400) and the guide at 5,507 (target 4,800), and nothing more can go without dropping a rule. The plan template (3,769), proposal template (3,398) and wrapper (154) meet theirs. I checked each finding against the tree first. I ran no test and applied no row to the tree; counts are from a script replay that matched the Internal review's 1,902 and 5,680 within 2 words.

| Finding | Disposition | Where answered |
|---|---|---|
| Internal 1, blocking | Accepted. Every cut is an exact row (Low tier) and none drops a rule; the stop rule is replaced by the `degraded` Scope delta (U1 219 words, U2 707). | C4, C6, Scope delta |
| Internal 2, blocking | Accepted, verified: the template heading has a `-- <agent> -- <date>` suffix. Heading prefix, fence, line base, item, `Home:` placeholder and output line are exact; test 1 reads the template's heading. | C8 |
| Internal 3a | Accepted, verified at `templates/core/dev/PLANNING.md` lines 127 and 152 and `dev/PLANNING.md` line 288. | C7 PM1, PM2; Non-work; C9 |
| Internal 3b | Accepted by recording: `tools/session.py` is protected and the Decision does not ask for it; QA1 says session start still lists an appendix. | Non-work; C7 |
| Internal 4 | Accepted: `> ` is a line break, kind N, rules text 73 words, exact placement. | Step 3; C7 |
| Internal 5 | Partly. Accepted: the upgrade note is a closeout item with a Home. Declined: gate changes (survivors must be final; test 1 reads C7's heading) and folding C1 into C2 (renumbering for no outcome). | C9; chunk table |
| Internal 6 | Accepted: stale `Proposed paths:` bullet deleted; both checks pass. | Source proposal |
| Security 1, blocking | Accepted, verified at proposal template lines 324, 349, 431: QT11b, QT14, QT15 are not rows; 73 words stay; 3,398 of 3,400. | C7 |
| Security 2 | Partly. Of all moved spans, those three and one sentence in TM1 (shared test setup; kept by M9b) were rules. The Decision points both ways on the rest, so U3 asks the Maintainer; default allow. | U3; M9b |
| Security 3 | Accepted: C4 lists what stays verbatim; step 6 adds the words and a doubt rule. | C4; step 6 |
| Security 4 | Accepted, narrower than proposed: only a headerless `<stem>--appendix.md` beside its proposal is skipped. | C8 |
| Security 5 | Accepted. | C1 |

Also: TM1 deletes line 1 (the `claim-check-allow` comment); anchors no longer carry `> `. No second Security pass is requested: nothing added widens a trust boundary.

**Coverage**: Replayed every C3 to C7 row on both copies by script; read each cut keyword sentence. Not covered: a tree edit, a test run, C8's code, Windows.
