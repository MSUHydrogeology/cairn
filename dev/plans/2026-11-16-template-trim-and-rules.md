# Plan: Trim the authoring templates, testing module and collaboration guide; list the rules that apply

**Source proposal**: dev/proposals/archive/2026-11-16-claude-template-trim-and-rules.md
**Author**: Claude Sonnet 5.5 (`claude-sonnet-5-5`, Medium), plan author
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-16
**Rules that apply**: dev/rules/working-agreements.md, dev/rules/protected-surfaces.md, dev/rules/conventions.md
**In brief**: Agents will read about 3,300 fewer words in five shipped files with every rule kept, each plan and proposal will name the rule files that apply, and a plan cannot archive with leftovers that have no home.

## Build summary

After this plan an agent starting a task loads less text: the accepted targets hold, with operative duties retained. Both templates gain a `**Rules that apply**:` line; the closeout record names a Home for each remaining item and the board warns when one is missing. The testing module gains the accepted testing rules. Background removed from shipped text lands in an on-demand shipped explanation; Cairn-only background stays in Cairn's documentation. The exact replacement rows leave no prose design to Low execution.

The opening exceeds the template's word target because the exact replacements are the implementation design, including the review-required cuts and their survivors.

## Source proposal

The heavy-tier proposal (`dev/proposals/archive/2026-11-16-claude-template-trim-and-rules.md`, accepted 2026-11-16: "Let's accept all five as revised") sets a word target per file, moves explanation to documentation, adds the rules line, folds Dispositions into the closeout record with an advisory `board.py` warning, and adds five testing sentences and an appendix rule. It keeps #74, #76 and #79 in a held follow-on and keeps the test-cut rule in the shipped `testing-discipline` module. No operative rule may leave loaded text without the Maintainer's quoted word.

Proposed paths:
- `bootstrap/tests/contract/test_board_closeout_warning.py`
- `templates/core/dev/method-background.md`
- `dev/method-background.md`

## Scope

**Result.** The targets are 3,900 shipped plan-template words, 3,400 proposal-template words, 1,400 testing-module words, 4,800 words in each guide, and 170 wrapper words. Both module copies remain byte-equal. `AGENTS.md` and `RULES.md` are not edited; the three Plain Language copies remain equal. A scratch replay of C3–C7, including the earlier heavy-tier edits and C7 carry, measured with `wc -w`: both byte-equal module copies 1,392; shipped / Cairn guides 4,787 / 4,755; shipped / Cairn plan templates 3,769 / 3,757; shipped / Cairn proposal templates 3,360 / 3,807. Both guide Plain Language sections remained byte-identical to their sources. These are scratch results, not future implementation results: C4, C6 and C7 must measure the actual files, including any template-scan wording change.

**Branch.** Every chunk runs on `0.8-dev` (`dev/PLANNING.md` > "Working rules"). It does not exist at `1fa1d898`; no chunk starts before the coordinator creates it. This plan is a document and may be committed on `master`.

**Protected engine mapping.** C2 adds one `_CORE_MAPPINGS` entry in `bootstrap/_scaffold/config.py` to deliver the explanation. The resulting expected `_CORE_MAPPINGS` AST mismatch against `bootstrap/tests/fixtures/scaffold_ast_baseline.json` stays unpassed until the existing grouped Human re-anchor operation. Verify it is exactly the reviewed mapping change; unexpected drift remains implementation work. The separate human operation is not a plan-archive condition. No frozen test is edited; C1 stops on a newly found frozen wording pin.

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

Governing text: both templates, the module, the guide, `VENDOR.md`, both rules READMEs and the protected engine mapping. Deliberation: `dev/rules/protected-surfaces.md`. The shipped, on-demand `dev/method-background.md` holds the shipped explanatory M spans; it is not an operative rule source. Cairn-only explanatory spans and the Cairn-only roster go in `docs/methodology/coordination.md`, not the shipped file. The three security caveats in the proposal template and shared-test-setup duty in the module remain in their loaded homes. The outstanding ordinary and Security reviews must cover this mapping and the replacement rows.

## Sequence

**Every chunk.**
1. `git branch --show-current` prints `0.8-dev`. Claim the paths (`python tools/intent.py claim --files <paths> --action "<what>" --stem trim<N>`), commit by explicit path, never push, never edit `CHANGELOG.md`.
2. Re-measure with `wc -w` and find each span by grepping its first words. Counts differ if an earlier plan landed. An anchor matching 0 or 2 times: stop, return to the plan author.
3. A span runs from its first anchor word to its last, line breaks ignored. A `> ` at the start of a line counts as a line break, not text, and no anchor includes it. **D** deletes the span and one adjacent blank line (a bare `>` line counts as blank, and a span that starts or ends a block-quoted line takes that line's `> `). **M** is **D** plus appending the deleted text verbatim under a source-named heading in the explanation file: use the shipped source once for identical shipped/Cairn spans; append Cairn-only spans to `docs/methodology/coordination.md`. Preserve source order and distinguish background from operative rules. Do not append the same span twice. **S** replaces the span by the given text; where the row says M, the replaced words are appended too. **I** inserts the given text after the span, preceded by one space. **N** inserts the given text as its own line or paragraph directly after the line or paragraph the anchor ends. Retype, rewrap or reorder nothing else (`scripts/exact_replace.py` or an exact Edit).
4. Before a D row, read its survivor (the home named) and confirm the rule is there. A survivor is never lost; the exact GT rows may combine it without weakening its meaning. Home codes in the tables: PR = guide "Plans and records", RR = guide "Review rules", RL = guide "The review loop", VF = guide "Verification", PA = plan template "Plan amendments", WL = plan template "The Waiting line", AG = `AGENTS.md` "Lifecycle and records". A deleted sentence with a condition the survivor lacks: stop, return to the author; the carried text this plan lists is the only exception.
5. Apply every row to the Cairn copy too; a row whose anchor is absent there is skipped and named in the commit body. Afterward `diff <shipped> <cairn>` shows only the pre-existing differences plus the explicit Cairn-only roster move and README pointers.
6. No-weakening check, every prose chunk. A throwaway script lists, from `git show <base>:<path>`, each sentence containing `must`, `never`, `only`, `required`, `requires`, `cannot`, `may not`, `do not`, `does not`, `refus`, `always`, `owes`, `unless`, `stop`, `no agent`, `waive`, `exempt`, `hostile`, `negative`, `guard`, `fence` or `Maintainer`, with its best match in the new file. At `1fa1d898` the shorter list gave 94 sentences in the plan template, 64 in the proposal template, 131 in the guide, 24 in the module and 4 in the wrapper; the added words raise them, and the implementer's script sets the figures. Each is verbatim, deleted or shortened by a row of this plan whose survivor holds it, or the chunk stops. A shortened sentence that can be read two ways keeps its original: stop and return to the author. The row tables are the ledger; append nothing.
7. The commit body gives words before and after, the rows applied, each rule removed or changed with its home, and the tests run.

| # | Chunk | Tier | Gate | Ships |
|---|---|---|---|---|
| C1 | Pin scan | Low | `0.8-dev` exists | scan result |
| C2 | Add the shipped explanation mapping and file; trim wrapper and add rules README sentence | Low | C1 | mapping, explanation, wrapper and rules READMEs |
| C3 | Testing module: exact rows, new rules | Low | C2 | module copies, protected-surfaces, explanation |
| C4 | Testing module: exact cut rows | Low | C3 | module copies and explanation |
| C5 | Guide: exact rows and carried sentences | Low | C4 | both guides, explanation |
| C6 | Guide: exact cut rows and Cairn-only roster move | Low | C5 | both guides and explanations |
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

First create `templates/core/dev/method-background.md` with the heading `# Cairn method background`, followed by the sentence `Loaded rules remain authoritative.` Add a pointer in `templates/core/dev/README.md` to `dev/method-background.md` and in `dev/README.md` to the tracked source `templates/core/dev/method-background.md`; Cairn uses that source directly and has no local installed copy. Add `("core/dev/method-background.md", "dev/method-background.md")` to `_CORE_MAPPINGS` in `bootstrap/_scaffold/config.py`, beside the other `core/dev` mappings. In C2–C7 append each shipped M span, once in source order under a heading naming its source, to that source file. Add exactly `[Cairn method background](method-background.md)` to the shipped README and `[Cairn method background](../templates/core/dev/method-background.md)` to Cairn's README, as a paragraph after its `Written in` line in the shipped README and after `# dev/ — the development coordination space` in Cairn's README. Append Cairn-only M spans to `docs/methodology/coordination.md`; do not ship Cairn's roster. Check the public installer manifest, a fresh install and an upgrade fixture for the source/destination and delivered content, run selected tests and security checks, and record only the expected `_CORE_MAPPINGS` AST mismatch for the existing grouped Human re-anchor wait.

Replace `templates/core/VENDOR.md` with this text (310 to 154 words). In Cairn's `CLAUDE.md` delete `> **Thin vendor wrapper.** … not here.` (M, Cairn-only) and replace the `**Drift guard.**` paragraph by the last paragraph of that text. In both `dev/rules/README.md` files insert, after ``this folder or `docs/` can hold it.``: `A Maintainer's rule goes in the rule file with the Maintainer's approved wording, never only in an agent's memory.`

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

Also append to `dev/rules/protected-surfaces.md` (Cairn-only): ``Tests exempt from the promise-only cut. Cut only through a Security Review: tests of the surfaces above; the security-family files and native-only IDs in `bootstrap/tests/security_manifest.py`; tests that a release document, `bootstrap/SAFETY.md`, `bootstrap/_scaffold/SECURITY_MUTATIONS.md` or a shipped file names as a guard; and refusal, hostile-state and negative-guard tests. The generic rule is in the testing-discipline module.`` M spans follow the explanation routing in Sequence. No rule is deleted.

### C4 Testing module: exact cut rows

After C3 apply the existing rows below, then MT1–MT9. Apply them to both module copies identically. Measure actual `wc -w`; each copy must be at most 1,400. The scratch replay measured 1,392 words by `wc -w`; the actual result must be measured, not inferred. All C3 duties, refusal and negative-guard protections, independent mutation expectations and the three simulation timescales retain their meaning. MT rows combine wording; they do not cut the TM7 Security Review exemption or the scientific rules. For MT6 and MT7, append the original parenthesized regime examples beginning `valid and malformed`, boundary examples beginning `zero, empty`, and property examples beginning `conservation, symmetry` verbatim to the shipped background under the module heading.

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

M spans follow Sequence. Then apply these exact replacements to both copies. Each end anchor is excluded; preserve blockquote prefixes and wrap normally.

**MT1.** Start: ``**Developmental tests``. End: ``**A surviving mutant``. Replace up to, but not including, the end anchor:

```text
**Developmental tests are scratch work; permanent tests guard promises.** Run debugging tests in scratch, record results and delete them before merge or archive. Keep a test only for a listed external promise through a public entry point; run each new test once on a clean checkout. Before adding an input variation, confirm production branches differently; one uniform guard or passthrough needs one test. Never add a test file per plan, bug or review finding.
```

**MT2.** Start: ``**Choose change checks``. End: ``**Simulation models``. Replace up to, but not including, the end anchor:

```text
**Choose change checks from affected behavior.** Trace changes through owners, existing test homes, callers, imports, configuration, data readers and public entries; map checks to affected components and consumers. Local changes use affected checks; shared contracts, infrastructure, language seams, solver or physics changes and uncertain dependencies widen to owners and consumers. Add tests only for plausible uncovered faults. If dependencies cannot be bounded, state the uncertainty and smallest useful remedy. Test each part of a large project where it lives. Current results may verify a change; a release never replaces its own whole-suite and security-family run, and may reuse results only under a reviewed rule.
```

**MT3.** Start: ``**A surviving mutant``. End: ``**Refusals are promises``. Replace up to, but not including, the end anchor:

```text
**A surviving mutant is a question.** If it changes promised behavior, strengthen the promise test; if unobservable, ask whether the code is needed. Never pin the mutated line.
```

**MT4.** Start: ``Investigate surviving mutations``. End: ``Do not weaken assertions``. Replace up to, but not including, the end anchor:

```text
Investigate surviving mutations against independent expectations, not candidate output; no per-function or set-wide quota applies. Humans confirm reported faults, not every discarded candidate or ordinary change.
```

**MT5.** Start: ``**Test tiers are a single``. End: ``**The tier is``. Replace up to, but not including, the end anchor:

```text
**Test tiers are a single coherent scheme.** Use named unit (pure logic, synthetic inputs), contract (stable boundary), integration (multi-component dataflow), workflow (end-to-end small fixture) and project-specific tiers.
```

**MT6.** Start: ``**Choose tests by regime``. End: ``**Prefer properties``. Replace up to, but not including, the end anchor:

```text
**Choose tests by regime and boundary.** Test each input regime and its transitions once. This heuristic is not a guarantee; keep extra cases where a regime is poorly understood.
```

**MT7.** Start: ``**Prefer properties``. End: ``**Test promises``. Replace up to, but not including, the end anchor:

```text
**Prefer properties to snapshots.** Assert invariants such as conservation or round trips. Input exploration is optional; no generator or dependency is required.
```

**MT8.** Start: ``**Test promises``. End: ``**Developmental tests``. Replace up to, but not including, the end anchor:

```text
**Test promises, not wording or internals.** A caller-visible promise covers behavior, refusals and formats. Test it through the public entry point, in-process where practical. Put a `Promises:` line and one or more `- ` lines in the test file's module docstring. A behavior-preserving refactor should change no test; failure despite unchanged behavior is a pin. Protect instructional prose by exact edits and review, not tests freezing wording or key terms.
```

**MT9.** Start: ``**Advisory report``. End: ``**Use public entry``. Replace up to, but not including, the end anchor:

```text
**Advisory report.** `python scripts/test_coupling.py` reports private reach and missing promise lists worst first. It names its Python-only gap, keeps refusal and hostile-state tests, and is a review prompt, not a deletion list. `--strict` exits nonzero for a gap or scan failure; default is advisory and exits zero.
```

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

M spans follow Sequence. Shipped guide after rows: 5,681 (the bare `>` line beside G0 goes with it).

### C6 Guide: exact cut rows

After C5 apply the existing rows below, then GT1–GT15, in order, to both guides. The exact replacements merge repeated obligations; they retain the meaning of the C5–C7 survivors and carried text, all Boundary and floor duties, refusals, fences and Maintainer-only actions. Measure actual `wc -w`: each guide must be at most 4,800, including prior group 2 additions. Scratch `wc -w` after the roster move, the heavy-tier plan's 169 / 170 word additions and the C7 carry measured 4,787 shipped and 4,755 Cairn. Re-measure the actual files. For GT1 append the original parenthesized claim examples beginning `exists / works` and edge-case examples beginning `empty / None` verbatim to the shipped background. Do not edit Plain Language, slots or role bullets.

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

M spans follow Sequence. Apply these replacements in order, to both guides; each end anchor is included. Wrap normally, retaining list structure in GT1. A row whose start and end anchors are identical replaces that exact span once.

**GT1.** Start: ``1. **Claims**``. End: ``only the Maintainer may concede (below).``. Replace through the end anchor:

```text
1. **Claims** — Check load-bearing claims against the current tree with committed evidence or adequate reasoning; cite evidence and limits. Forward behavior needs executable evidence; inventory and check every applicable member for a set-wide claim.
2. **Production path** — Test the failing path through the public entry point, not a helper or stub.
3. **Design completeness** — State preconditions, invariants, edge cases and failure modes.
4. **Fail-closed** — Guards fail loudly, not by degrading or returning empty, across configurations and stages; make fail-open paths intentional.
5. **Consistency** — Check docs, roadmap, code, tests and doctrine for stale references and reusable tools. Repeat the plan's reuse search and one of your own, testing each against a known positive; an accidental near-copy is a finding satisfied by reuse or generalization.
6. **Drift** — Match docs, examples, changelog and commit claims to shipped behavior.
7. **Placement** — For process changes, identify who acts, when, and in which ceremony or serialization point.
8. **Scientific validity and scope** — Ground and document methods, prevent quiet scope expansion, and justify new abstractions.
9. **Satisfier** — Every finding names a closing test, guard, doc, scope-cut or explicit `wontfix`; without one it is an observation. At archive, test or guard maps to `guard`, doc or scope-cut to `accept`, and wontfix to `wontfix`. Other real work is `defer`, the Maintainer's call. A scope-cut corrects a claim; only the Maintainer may concede removal of accepted work.
```

**GT2.** Start: ``**The clean pass has a mirror:``. End: ``scope-reduction trap").``. Replace through the end anchor:

```text
An honest, evidence-backed failure to falsify clears the review; unsupported assertion does not. **The scope-reduction trap.** Scrutinize narrowing as carefully as a clean pass. Reviewers state what is lost and why the narrower change reaches the cause. An author removing underspecified work says why specification was rejected. Compare outcomes with the artifact as opened before Decision and as accepted afterward, never a later summary. A lighter mechanism delivering every outcome is no reduction. Lost outcomes require a `**Scope delta**`, one grouped scope-remainder record per source artifact, and the Maintainer's explicit allowance. Declining an outcome proposed only during review is not a reduction.
```

**GT3.** Start: ``Set a useful plan goal first.``. End: ``another plan's future review, archive or release may not be required to finish this plan.``. Replace through the end anchor:

```text
Set a useful goal, scope and observable criteria; estimate the work window and uncertainty, not a deadline or waiver. Open only outcomes with authority and resources; queue unavailable approval or passive calendar waits with source, owner and restart condition. Approved scientific observation remains implementation across days; missing evidence stays unverified. A plan may group dependent chunks that deliver one independently finishable outcome; the coordinator decides connected-arc grouping. A commit, work item or contract label alone never forces another artifact. Shared reviews name changes and cover every obligation; grouping waives no Decisions, fences, scope, checks, floors or trust and release operations. Uncovered promises, new boundaries, failed checks and changed scope follow existing stop rules. Name each outcome's prerequisites and release; queue the rest without losing accepted scope. A shipped capability may be a prerequisite; another plan's future review, archive or release may not be required to finish this plan.
```

**GT4.** Start: ``Only the Maintainer calls an External read``. End: ``Detail: Cairn's published dual-review procedure.``. Replace through the end anchor:

```text
Only the Maintainer calls an External read on one existing artifact; a standing call needs a proposal. A roster adds or upgrades no read. The reviewer answers three questions and states distance. Record the Maintainer's verbatim words set apart and commit them with their source: `Called by: Maintainer -- Decision at <commit>` or `-- chat, <date>`, adding `, relayed by <who>` where relayed. Without that line the pass is ordinary; `**Tier**: External` needs it. The call adds focus, replaces no review or owed answer, clears Security Review only as one, and grants no Decision or fence authority. Waivers or scope changes take effect only in a Decision or plan fence. Agents never request or declare one, say a change needs one, recommend more distance, head a pass External or start one without the Maintainer's words; they may name risk and gaps. The next reviewer and Maintainer, not a tool, check the quote. High-risk work retains separate ordinary and Security passes; Internal cannot clear Security. A plan's Internal Security Review needs the matching `Obligation` line. Plan review is fresh-context; code review is by another agent, never reopens the Decision or reruns implementation checks. Detail: Cairn's published dual-review procedure.
```

**GT5.** Start: ``Plans finish after their accepted scope``. End: ``Do not replay the whole selection solely to stamp a new commit ID.``. Replace through the end anchor:

```text
Plans finish as in “Plans and records”; they do not wait for later integration. The arc owner runs one joined integration selection under the canonical runtime after connected plans finish, or earlier at a critical shared boundary. Before arc completion or release, record final combined coverage, evidence producers and consumers, results and omissions. Reuse applicable results only for unchanged behavior and inputs; after corrections rerun affected interactions. The arc owner records and repairs post-archive defects without reopening the plan. Missing evidence, failed promises and required checks remain plan work. Routine human trust and release operations remain separate. Cover the clean final combined revision; do not replay the whole selection solely to stamp a new commit ID.
```

**GT6.** Start: ``Search before building``. End: ``no `restore`, `checkout`, `stash`, `reset` or `clean` there.``. Replace through the end anchor:

```text
Search and reuse before building. Coordinate shared-tree overlaps and claim exact files before editing where claims are used. Commit explicit paths, never bare `git commit`; add and commit a new file in one invocation, unstaging it if that fails. Serialize commits with other writers. Inspect staged and unstaged candidate changes against `HEAD` with `git status --short` and `git diff <paths>`, never the shared cached index; stop if another writer's work appears. Without that agreement use a fresh worktree for writing checks. A shared-tree reviewer claims, writes and commits only their own review by explicit path; no `restore`, `checkout`, `stash`, `reset` or `clean` there.
```

**GT7.** Start: ``At goodnight, leave``. End: ``The smoke does not replace them or any required certification.``. Replace through the end anchor:

```text
At goodnight commit a handoff and reflection, and leave an uncommitted next-session note; refuse it if its path, `dev/reflections` or `dev` is a link. Goodnight never authorizes a push. The full-handoff owner runs configured fast smoke if present, recording command, result and coverage limits; absence is unavailable, not passed, and failure is failed. Reflection-only participants owe no test. Slow tests remain due at release and when an accepted plan, safety/security requirement or Maintainer requires them. Change checks and joined Boundary B remain due on their schedules; smoke replaces neither them nor required certification.
```

**GT8.** Start: ``**End with a two-part coverage line**``. End: ``the Maintainer reads the negative space and may ask any reader for anything.``. Replace through the end anchor:

```text
Cite a file, test, line or command; report coverage, low confidence, risks and gaps, not a recommendation for more review. The Maintainer may ask any reader.
```

**GT9.** Start: ``For a proposal, read its title``. End: ``prepares the reader for the proposal.``. Replace through the end anchor:

```text
Before body or code read the proposal's title, one-line summary and Decision summary; state the gist in one or two sentences. If the top needs the body for understanding, make a finding. After every revision the author rereads and revises the top as a whole when needed.
```

**GT10.** Start: ``A reviewer may identify avoidable burden``. End: ``a global optimum is required.``. Replace through the end anchor:

```text
A reviewer may name a simpler adequate alternative with lower total build, run, understanding and maintenance cost. The author decides; no per-addition accounting or global optimum proof is required.
```

**GT11.** Start: ``The lenses can inform proposal, plan and code review. A trivial change with no review owes no review record.``. End: ``The lenses can inform proposal, plan and code review. A trivial change with no review owes no review record.``. Replace through the end anchor:

```text
Unreviewed trivial changes owe no review record.
```

**GT12.** Start: ``A reviewer who tests claims against applicable evidence or reasoning``. End: ``An unsupported assertion alone does not clear it.``. Replace through the end anchor:

```text

```

**GT13.** Start: ``**Falsifiable evidence, not "checked."**``. End: ``not a pass.``. Replace through the end anchor:

```text

```

**GT14.** Start: ``When asking the Maintainer to choose,``. End: ``a routine Decision with no such addition needs no extra sentence or inventory.``. Replace through the end anchor:

```text
When asking the Maintainer to choose, show each material option's changes and build, run, understanding and maintenance costs, with estimates or uncertainty. Include the least involved credible option, including doing nothing when viable, and losses including safeguards. Separate recommendation and reason from options. Waive no required check, accepted scope or model floor. Name changed or added material human operations, estimated counts (zero when informative), and recurring additions; omit routine agent work. The Decision names material new recurring additions; none needs no extra sentence or inventory.
```

**GT15.** Start: ``Apply the **Pareto testing principle**``. End: ``the Maintainer sets high-level project needs and material exceptions.``. Replace through the end anchor:

```text
Apply the **Pareto testing principle**: aim for 80% fault coverage in 20% of runtime and maintenance. Permanent tests guard external promises through public entries: primary workflows, scientific or data invariants, and one parameterized check per security or refusal class. Run developmental tests during coding and delete them before archive. Do not keep private-helper tests, change-specific pins or wording tests; do not add separate input variations on the same code branch. Pruning non-promise, private-helper or over-budget tests needs no per-member mutation proof unless specifically required. Simulations use real equations on small domains and analytical or convergence benchmarks. Local effects use affected checks; shared contracts, common infrastructure and solver behavior widen to owning families and consumers. Agents select routinely, reviewers challenge, and the Maintainer sets high-level needs and material exceptions.
```

**GT16, Cairn only.** Move the span from `Cairn is built by the **Human Maintainer**` through `Refreshed when the team changes.` verbatim to `docs/methodology/coordination.md` under `## Cairn team roster`. Replace it in `dev/agent_collaboration.md` with the following text; it keeps the refresh duty and does not ship Cairn's people or project details:

```text
Cairn's Maintainer directs work; agents advise and do not decide. The current roster is in `docs/methodology/coordination.md`. Refresh it when the team changes.
```


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

Not rows, by the Security Review: the three proposal-template sentences that say what the checks do not prove (`Structural questions about where material … a reviewer can falsify.`, `**What they do not reach.** A … finds it.`, `These are author declarations, not inferences: … it was right.`) stay where they are. They are caveats against reading the security questions and the path checker as proof, and Cairn's `docs/` does not ship. They total 73 words; the updated proposal-template counts are in Scope.

M spans follow Sequence. Apply the following former reserve: the earlier heavy-tier edits add 109 shipped proposal words, so the reviewed 3,398 result no longer fits. Then apply QT16–QT22 below: for the proposal template, cut the slot sentences `Trace changed behavior through callers … plausible uncovered faults.` (51 words, shipped copy only), and in the guide's "Verification" (both guides) replace `shared contracts, common infrastructure and solver behavior widen` by `shared contracts, common infrastructure, language seams, solver behavior and uncertain dependencies widen` (+5 words). Still over after these rows: stop and return to the author; no other cut. None for the plan template.

**QT16.** In both proposal templates, replace the span `For every implementation change,` through `existing promise test.` with: `For each implementation change, name its caller-visible promise and public entry point. Identify a plausible uncovered fault or extend an existing promise test; do not propose a test merely because a change exists.`

**QT17.** In the shipped proposal template only, replace the span `(Adopter-specific test taxonomy` through `entry points.` with: `(Name the project's test homes, affected behavioral nodes and public paths exercised through their real entry points.`

**QT18.** In the shipped proposal template only, replace the span `Record speed or environment tiers` through `Broader certification is separate and does not replace a missing check.` with:

```text
Record speed or environment tiers, but speed alone does not establish affected coverage. The reviewed plan maps changed behavior, not a permanent fast set: `bounded` covers affected behavior and consumers; `wide` covers owning families, known integration, public paths and standing gates where dependencies are uncertain. Name uncertainty; never claim unknown dependencies covered, and keep known unmet checks or criteria open. Certification cannot replace a missing check.
```

**QT19.** In the shipped proposal template only, delete `Routine selection belongs` through `material exceptions.`; its survivor is the guide's Verification paragraph (GT15), which retains agent selection, reviewer challenge and Maintainer authority.

**QT20.** After QT6a and QT6b, in both proposal templates replace `In a few ordinary-language sentences,` through `proposal text.` with:

```text
Briefly name in plain language the issue people notice, proposed change, material outputs added, changed or removed, and meaningful costs or tradeoffs. Define technical terms at first use; give a concrete example when it clarifies an abstraction. Supporting evidence and technical detail go below. This reading aid is not another scope contract; correct mismatches to the operative proposal text.
```

**QT21.** In both proposal templates, replace `What is true today,` through `show it failing.` with `Describe current state and problem with evidence; demonstrate claimed failures.`

**QT22.** In both proposal templates, replace `What documentation, doctrine, or contract surface` through `where does the change to it land?` with `Name affected documentation, doctrine and contract surfaces and their destinations.`

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

Run Verification. For each changed lock-tracked file (`dev/plans/_template.md`, `dev/proposals/_template.md`, `dev/agent_collaboration.md`, `dev/modules/testing-discipline.md`, `dev/rules/README.md`, `CLAUDE.md`, `tools/board.py`, `dev/README.md`) run `python bootstrap/scaffold.py upgrade --target . --finalize <path>`, commit `dev/.cairn/cairn-lock.yml` alone, then run `python bootstrap/verify_integrity.py --target .` and compare affected-path results with the pre-C1 baseline. Record existing failures as unpassed and stop on unexpected new failures; do not claim a clean whole tree. Run `grep -n "> \*\?Dispositions" templates/core/dev/PLANNING.md`: it prints nothing (the coordinator's `dev/PLANNING.md` line 288 is checked the same way once it lands). Put the counts table in the commit body and end this plan with its closeout record in the new form, carrying the upgrade note as an item whose Home is the coordinator's changelog entry.

## Acceptance criteria

**C1.** Capture `python bootstrap/verify_integrity.py --target .` output as the pre-change baseline without claiming it clean. The scan names its inputs and four test folders; its result is in the C2 commit body. No frozen test is edited; `python scripts/repin.py status` lists the same frozen-modified files before and after the plan.

**C2.** The public manifest, a fresh install and an upgrade fixture include `templates/core/dev/method-background.md` at `dev/method-background.md`, with the reviewed background content and no Cairn-only roster. In a disposable fresh install, confirm the source is delivered at that destination; use `bootstrap/tests/test_upgrade_module_additions.py`’s `_prepare_new_core_upgrade(target, "dev/method-background.md")` in a disposable probe to model an older adopter, then call the public `upgrade --stage` and `--apply` against that disposable target and confirm the destination and lock record return with source `core/dev/method-background.md`. The source has no local installed copy in Cairn, and the lock attests none; both READMEs point to the appropriate available file. The `_CORE_MAPPINGS` change is the only expected AST delta; applicable selected checks and Security Review cover it. `templates/core/VENDOR.md` is 154 words, line 1 `# Vendor wrapper — {{project_name}}`, `@AGENTS.md` on line 4. Shipped `AGENTS.md`, `VENDOR.md` and `RULES.md` total at most 1,500 words (planned 1,339); Cairn's three at most 2,000 (planned 1,414). Both READMEs carry the new sentence once. The wrapper-rename nodes of `test_upgrade.py` pass.

**C3.** All seven rows are applied to both module copies, which stay byte-equal; line 1 is gone; the #77, #86, #88 and #81 sentences each appear once; the file is 1,900 words. The protected-surfaces paragraph exists. Shipped M spans appear in the installed background, except the shared-setup sentence of TM1, which stays in the module.

**C4.** Both module copies are byte-equal and at most 1,400 words by `wc -w`. Every existing C4 row and MT1–MT9 applies; C3 duties, the Security Review exemption, refusal and negative-guard duties, independent mutation expectations and the three simulation timescales retain their meaning. `claim_check` is clean on both copies; moved examples are in the shipped background.

**C5.** Every row is applied to the shipped guide and, where its anchor exists, to Cairn's; the shipped guide is 5,681 words. The 14 headings and Plain Language are unchanged. Each D row's survivor was read first. Each carried text is present once. M spans are in their shipped or Cairn-only background homes as specified.

**C6.** Both guides are at most 4,800 words by `wc -w`, including earlier group 2 additions. The Plain Language section diffs empty; headings, role bullets and slots remain. GT rows preserve the meaning of survivors and carried duties, including every Boundary, floor, refusal, fence and Maintainer-only action. The Cairn roster is kept in its Cairn-only home, with its refresh duty and pointer in the guide. Each D row's survivor was read first.

**C7.** Shipped plan template at most 3,900 words (scratch 3,769), shipped proposal template at most 3,400 (scratch 3,360); Cairn copies measured 3,757 and 3,807, including their slots. Both carry the rules line and paragraph. `## Dispositions` is gone; `## Implementation closeout` carries the Home rule, the deferral rule, the `wontfix` limits and the executing-`guard` rule. The three caveat sentences on what the security questions and the path checker do not prove are still in the proposal template. The shipped `PLANNING.md` says `Implementation closeout` in both places. The C1 structure list holds, shipped bytes install unchanged, and Cairn's copies differ from shipped only as before.

**C8.** The eight tests pass once on a clean checkout, `python tools/test_tiers.py check` passes, the board files are byte-equal, and `test_board_json_contract.py` passes for both copies. The warning prints only a file name and number. S2 (it can fail): tests 1, 5 and 8 fail without the code. S3 (what fires it): `python tools/test_tiers.py for tools/board.py` lists the new file and the contract file.

**C9.** The commit body has the counts table and each chunk's shared-file re-read. The lock records the changed installed paths including `dev/README.md`; Cairn has no local `dev/method-background.md` and the lock attests no such copy. Report integrity results and existing mismatches without claiming a clean whole tree. The expected reviewed `_CORE_MAPPINGS` AST mismatch remains unpassed until the separate grouped Human re-anchor. `git diff --name-only` since C1 names no `frozen_files` entry. The grep for `Dispositions` pointers prints nothing. The closeout lists each item not run or not covered with its Home, including the upgrade note.

## Scope delta

**Scope delta**: preserved. The Maintainer refused waiving the targets; the cuts above retain the accepted outcomes and route adopter background to a shipped home. The extra core mapping delivers that accepted home and is covered by this heavy plan's required reviews. Its expected AST mismatch remains a separate grouped Human re-anchor wait, not a completed baseline.

## Verification

**Maintainer verification direction** (chat, 2026-11-17): “Please re-write the plans to use focused checks and joined integration.” “Just do focused replacements”. Preserve the eight board tests and named failure controls, installer manifest and fresh-install/upgrade contract, byte parity and word caps. Template-scan wording remains future work and the old full mapped list is not claimed as run. Use `python tools/test_tiers.py for <changed paths>` to identify candidate owning families, then select the smallest checks for changed public promises; it does not require running every listed case. Reuse evidence only for unchanged behavior and inputs, and run the prose gates for prose. The arc owner runs one joined Group 2 integration selection after connected plans finish, or earlier at a named critical shared boundary; record the combined revision, checks, results and omissions. Required code reviews remain.

Changed promises and entry points: the public install manifest and fresh install deliver the background file; the expected `_CORE_MAPPINGS` AST mismatch is checked against `bootstrap/tests/fixtures/scaffold_ast_baseline.json` and recorded in the existing grouped Human re-anchor wait. The warning (`python tools/board.py`), both templates through install, module copy equality, the wrapper's rename detection, the 1,500 and 2,000 caps. Use `python tools/test_tiers.py for <changed paths>` to identify candidate families; select focused checks for changed public promises, not every listed file. By reading, that is `test_board_json_contract.py` (read-only, templates and both board copies), `test_review_sweep_ships.py`, `test_writing_rules_ship.py`, `test_review_stance_in_shipped_files.py`, `test_scientific_check_guidance_ships.py`, `test_scope_reduction_trap.py`, `test_install_report_slots.py`, `test_verification_boundaries.py`, `test_practice_modules.py`; for `VENDOR.md`, `test_upgrade.py -k "vendor or VENDOR or wrapper"` and the one node `test_scaffold.py -k test_full_install_seeds_rules_md_within_word_budget`. Interpreter: `/Users/kendal30/conda_envs/lhm/bin/python3.13`.

Prose gates on each changed prose file: `python scripts/claim_check.py`, `python scripts/link_check.py`, `python scripts/sync_doc_snippets.py --check`, `python scripts/quality_gate.py --sub neutrality`; counts by `wc -w`. Code reviews: R1 (Internal) over C1 to C7 and C9, with the reading question answered row by row from C3 to C7; R2 (Internal Security Review) covers the C2 engine mapping and shipped explanation, all security-bearing C3–C7 changes, and C8. Both plan-review obligations cover the revised mapping and rows before implementation.

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

## Response to plan review -- Terra Medium -- 2026-11-17

**Elapsed**: unknown
**Tokens**: unknown

The Maintainer, 2026-11-16, refused the target waiver: “I think that those three modules need to be trimmed, not waived. We need some principles for combining rules.” C4 and C6 now specify compact replacements, retain the operative duties and require both actual copies to meet their targets. The explanation home is a core shipped file: adding its existing installer mapping delivers the accepted requirement, rather than the previous author's proposed Cairn-only destination. The expected engine AST mismatch is recorded for the existing separate Human re-anchor wait. Scratch C3–C7 replays, word counts and their limits are in Scope; no product files, runtime tests, or release operations were run. C7 retains its previously reviewed rows; its reserve and all required reviews remain due.

## Plan review -- Terra Medium -- 2026-11-17

Reviewed commit: be02b1f05f57e2e3ba1cb31715c2f0700b8a59a7

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** The exact cuts and shipped explanation support the accepted trim, but GT3 changes the grouping rule (finding 1). -- proposal item 1; plan C2, C6
2. **Best alternative.** Keep the same compact rows and retain independence of the outcome, not of each dependent chunk. -- `dev/agent_collaboration.md`, Plans and records
3. **What would show it wrong?** A plan with dependent chunks that together deliver one finishable outcome would be incorrectly excluded by GT3's wording. -- plan GT3; `dev/agent_collaboration.md`, Plans and records

1. **Blocking -- preserve the grouping rule.** GT3 changes “dependent chunks that deliver one independently finishable outcome” to “dependent, independently finishable chunks.” The latter puts independence on each chunk and can narrow when one plan may hold dependent work. Restore the original relationship in the compact replacement, then remeasure both guides against 4,800 words. -- plan GT3; `dev/agent_collaboration.md`, Plans and records
2. **Non-blocking -- stale estimate.** C7 still says the proposal template is planned at 3,398 words, while Scope reports the newer scratch replay at 3,360 shipped and 3,807 Cairn. Label the shipped target and update the estimate so Low can distinguish the target from Cairn's added slots. -- plan Scope and C7; accepted proposal target table

**Audience / rule loss:** GT3 narrows an operative planning permission; Plain Language is explicitly preserved. The explanation mapping gives adopters the moved background, and the expected AST mismatch remains a separate Human wait.

**Coverage:** Compared revised C2–C7 rows, targets, dependency and review responses with the accepted proposal and current source, sampling replacement duties and survivors. Template-scan wording remains future work and actual counts must be remeasured. Did not replay all rows, run tests, inspect private inputs or perform Security Review.

## Response to plan review -- Terra Medium -- 2026-11-17

**Elapsed**: unknown
**Tokens**: unknown

Accepted both findings. GT3 now permits dependent chunks that together deliver one independently finishable outcome. Replaying that exact replacement on the earlier guide scratch results measured 4,787 shipped and 4,755 Cairn words, including the heavy-tier changes and C7 carry; C7 now labels the shipped targets and current template counts. Template-scan wording remains unimplemented and actual files must be remeasured. No product tests or release operations ran.

## Plan review -- Sol High, targeted Security pass 2 -- 2026-11-17

Reviewed commit: 5c8659cdb7fb8c9d7611abb47c2d5362dcf699f5

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none remaining
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: compact safeguards preserve their duties, and the final GT3 correction restores independence of the outcome rather than each chunk. -- GT3; correction `5c8659cd`
2. **Best alternative.** Exact compact rows and one existing core mapping meet the accepted targets without deleting duties or adding an installer mechanism. -- C2, C4 and C6
3. **What would show it wrong?** An omitted security duty or missing installed background would falsify preservation; the row inventory and install/upgrade checks must expose it. -- Sequence steps 4–6; C2 and C6 criteria

MT/GT rows retain refusal and negative-guard tests, independent expectations, public-entry evidence, External-read authority, separate Security obligations, scope-loss allowance and fence duties. The ordinary GT3 finding was also observed in this still-open pass and is closed by the exact correction; no further blocker remains.

C2 ships background through one core mapping; Cairn points to the canonical source without a duplicate file or false lock attestation. Expected mapping AST drift stays unpassed at the separate grouped Human operation. Scratch counts include heavy-tier additions; template-scan wording remains future work, so actual measurement and preservation checks remain due.

**Coverage:** Changed rows at `be02b1f0`, the exact correction at the reviewed commit, and relevant current source; reused the first pass's unchanged-row coverage. Exactly one earlier plan Security pass exists; this is pass 2, not a reset. No row replay, runtime tests, private inputs, installer execution or complete resulting-prose read. No operative rule loss is authorized.

## Targeted plan reread -- Terra Medium -- 2026-11-17

Reviewed commit: 5c8659cdb7fb8c9d7611abb47c2d5362dcf699f5

**Obligation**: Internal
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

Both findings are closed: GT3 restores dependent chunks delivering one independently finishable outcome; C7 labels shipped targets and updates both copies' scratch estimates. Scope and C6 record the revised guide estimates and require actual measurement. Read the committed correction and affected rows; did not repeat the full review, replay counts or run tests.

## Author disposition -- Terra Medium -- 2026-11-17

**Disposition**: ready-to-implement. Ordinary and Security reviews accept the corrected plan. Implementation waits for `0.8-dev` and must remeasure after the dependent template-scan wording lands. The expected engine AST mismatch remains unpassed until the existing separate grouped Human re-anchor. Elapsed: unknown. Tokens: unknown.
