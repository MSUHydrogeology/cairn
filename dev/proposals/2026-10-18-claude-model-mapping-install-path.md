# The model mapping gets filled on every install path, and something checks it

**Author**: Claude (Strategy)
**Status**: revising
**Review**: required(Internal + Security Review) — the scaffold engine's write path is touched; the Maintainer asked for this change, so "should it exist" is settled
**Plan review**: required(Internal + Internal Security Review) — the plan edits `bootstrap/_scaffold/` and a script adopters run (see the preflight)
**Opened**: 2026-10-18
**In brief**: every install and every `--adopt-module` prints a plain notice while the model mapping is unfilled; the check stops failing on a file that is filled; a PLANNING.md task and a test in Cairn's own suite keep it from being forgotten; no new flag, profile key or lockfile field.

## What changes for you

Cairn's own `dev/.cairn/model-selection-mapping.yml` sat on its `FILL ME` stub from the
2026-06-12 self-host to 2026-10-18 (commit `22dabd45` filled it). Its check failed the
whole time and nobody saw. This closes the four holes that allowed that.

1. **Every install says so.** An install run by an agent (no terminal) prints the notice
   an interactive install prints: the file, that the check fails until it is filled, and
   how to fill it. It tells the agent to ask you which model fills each tier, not to guess.
2. **`--adopt-module model-selection` says so too.** The docstring claiming it prompts for
   the mapping is corrected; it never did.
3. **The check stops failing on a correct file.** A mapping you filled by hand, leaving the
   stub's explanatory comments alone, fails today. After this only a `FILL ME` in a value counts.
4. **The install leaves a durable line.** A notice scrolls away; a task in `dev/PLANNING.md`
   does not. Installs from a preset get one.
5. **Cairn's suite fails if Cairn's mapping returns to the stub,** which puts the one tree
   where this happened on a machine trigger.
6. **A small safety fix** found on the way: the interactive capture writes the mapping
   without the symlink check every other install write has.

Unchanged: the install is never blocked; no new flag, profile key or lockfile field; the
stub's bytes; the install manifest (no file added or removed); `tools/session.py`.

## Questions for the Maintainer

1. **Stop counting comments?** Today a `FILL ME` in a comment fails the check, and a test
   (`test_fill_me_in_comment_fails`) pins that as intended. I would reverse it.
   *Recommended: yes, ignore full-line comments, change the checker only.* Rewording the stub
   looks cleaner but would give every adopter who filled the file a merge conflict on their
   next upgrade (see Alternatives).
2. **Which "trigger"?** *Recommended: the PLANNING.md task plus the suite test; not an
   onboarding trigger now.* That trigger fires only when someone runs
   `scripts/onboarding_activate.py` at goodnight. Nobody has in this tree: its log is empty and
   a dry run today lists two tasks that fired long ago. It would sit unseen as the check did.
   Whether goodnight should run that helper is a separate question, flagged here, not folded in.
3. **Print the notice on `upgrade` as well?** It would reach adopters already on the stub.
   *Recommended: not in this change.* I have not read the upgrade command's output paths closely
   enough to name a safe call site; say yes and a revision adds it.
4. **Fold in the symlink guard on the capture write?** *Recommended: yes.* Same function,
   on the engine; a Security Review would find it anyway.

## Context

**Terms.** The *mapping* is `dev/.cairn/model-selection-mapping.yml`: which model fills the
high, medium and low tiers. The *stub* is the file as installed, five rows reading `FILL ME`.
The *check* is `scripts/check_model_selection.py`. A *non-interactive* install is one run with
`--non-interactive` or without a terminal on stdin; an agent's shell is the second.

Four causes, each checked in the code today:

1. **Capture and notice assume a person at a terminal.** `non_interactive` is
   `args.non_interactive or not sys.stdin.isatty()` (`bootstrap/_scaffold/cli.py:625`). Capture
   returns `False` at once when it is true (`install.py:700`), and the only message prints under
   `not wrote and not non_interactive` (`cli.py:662`). The path agents take prints nothing. The
   stub's header calls the silent empty install "the exact failure this module exists to
   prevent". That is what happened.
2. **Nothing runs the check.** `git grep check_model_selection` finds no caller in
   `tools/session.py`, `scripts/quality_gate.py` or the skills, only mentions; the suite runs the
   checker on temporary files, never on Cairn's own mapping. Cairn has no CI. Its only trigger is
   a person remembering.
3. **The check fails a correctly filled file.** `_FILL_ME_RE` scans the whole file, comments
   included (`check_model_selection.py:59`), and the stub's own comments carry the phrase
   (`model_selection_mapping_stub.yml:13, 41, 42`). I rebuilt the case: the stub with its five
   rows filled by hand and every comment kept exits 1. Capture uses the same test to decide a
   file is "already filled" (`install.py:702`), so an interactive re-run over such a file would
   prompt and then overwrite the adopter's rows.
4. **`--adopt-module` never captures,** though the docstring says it does
   (`install.py:687-688`). Capture's only caller is `cli.py:656`; `_cmd_adopt_module`
   (`upgrade.py:1441`) never calls it.

Two things found while reading, both exercised:

* **The onboarding helper has not worked in this tree.** `dev/.cairn/onboarding-activated.jsonl`
  holds only its header beside 73 archived proposals, and `python scripts/onboarding_activate.py
  --dry-run` lists `post-first-proposal-team` and `post-first-cross-type` as pending. These
  triggers do not run at session start; they run when the goodnight owner runs the helper
  (`doctrine/session-routines.md:363`), and the goodnight skill does not call it.
* **The capture write has no containment guard.** With the mapping path planted as a symlink to
  a file containing `FILL ME`, the capture overwrote the file the link pointed to, outside the
  tree. Exploitability is low (the target must already hold that phrase), but the function is
  on the engine and absent from the guarded-write inventory
  (`bootstrap/_scaffold/SECURITY_MUTATIONS.md`, `test_security_leaf.py:30`).

## Proposal

### 1. One notice, on every path (engine)

A new `model_selection_notice_lines(target)` in `bootstrap/_scaffold/install.py` returns the
notice, or `[]` when the mapping is absent or filled. `main` calls it after capture (whether
capture ran, was skipped or was refused), and `_cmd_adopt_module` after the adopt line. It
replaces the old interactive-only message and prints to stdout like the other module NOTE
blocks. Proposed text, for reviewers to disagree with:

```
NOTE (model-selection) -- the tier-to-model mapping is not filled in:
  dev/.cairn/model-selection-mapping.yml still holds the FILL ME stub.
Until it is filled, `python scripts/check_model_selection.py` fails, and nothing
else runs that check for you. Ask the Maintainer which model fills each tier
(high, medium, low); do not guess. Replace each FILL ME row with tier, model,
date_verified (YYYY-MM-DD), task_family, and source (say who assigned it).
Schema: dev/modules/model-selection.md, "Mapping-record schema".
```

A symlinked or unreadable path yields a notice saying so, never silence. The text names no
model or vendor. **The non-interactive fill is this notice plus an agent editing the file.** A
`model_tiers:` profile key would change the profile schema and write model names into the
lockfile's profile block; a `--model-tier` flag would add published CLI surface and make it one
line for an installing agent to invent an answer only the Maintainer owns.

### 2. The check ignores full-line comments (checker, verbatim)

A line whose first non-blank character is `#` is skipped before the scan. Trailing comments on a
value line still count; the shipped stub has none containing the phrase. The engine's
"already filled" test uses the same rule, and a test runs both predicates over one corpus. The
checker's docstring and its "whole-file scan" comment are rewritten to match; exit codes keep
their meanings.

### 3. The capture write is guarded and its claim corrected (engine)

`capture_model_selection_mapping` calls `_assert_safe_write(mapping, target)` before writing and
joins `_GUARDED_WRITE_FUNCS` and the SECURITY_MUTATIONS table. The call site catches
`ScaffoldSecurityError`, says it declined to write, and continues to the notice, since this step
has always been "never blocks the install". The docstring says "at install time" and names
`--adopt-module` as notice-only.

### 4. Where it persists

* **A seed task in each preset** (`templates/onboarding/{solo-greenfield,collaborative-team,high-rigor-legacy}.md`)
  under `<!-- cairn:if complexity in moderate,complex -->`, the axis that selects the module:
  "If `dev/.cairn/model-selection-mapping.yml` exists, fill it (ask the Maintainer which model
  fills each tier), then run `python scripts/check_model_selection.py`." It follows the
  `install-work-intent-hooks` precedent: a printed notice plus a task that stays.
* **A suite test** that Cairn's own mapping passes its own check, so the full suite, run at each
  integration check, goes red if it returns to the stub.
* **A "Filling the mapping" paragraph** in the module doc, which today never mentions the file or
  the check. It says what runs the check: the suite in Cairn, a person elsewhere.

### 5. Files touched

| File | Change | Frozen? | AST-attested? |
|---|---|---|---|
| `bootstrap/_scaffold/install.py` | `capture_model_selection_mapping` (docstring, rule, guard); new `_mapping_is_unfilled`, `model_selection_notice_lines` | no | **yes**: 1 changed, 2 new |
| `bootstrap/_scaffold/cli.py` | `main`: call site; import list | no | **yes**: `main` |
| `bootstrap/_scaffold/upgrade.py` | `_cmd_adopt_module`: notice; import list | no | **yes**: 1 changed |
| `templates/modules/team-gated/check_model_selection.py` | comment rule; docstring | **yes** | no |
| `scripts/check_model_selection.py` | byte-identical copy of the above | **yes** | no |
| `bootstrap/tests/test_model_selection_stub.py` | new tests; one reversed | **yes** | no |
| `bootstrap/tests/test_security_leaf.py` | `_GUARDED_WRITE_FUNCS` gains the capture | **yes** | no |
| `bootstrap/_scaffold/SECURITY_MUTATIONS.md` | one table row | no | no |
| `templates/onboarding/*.md` (3) | one conditional seed each | no | no |
| `templates/modules/team-gated/model-selection.md`, `dev/modules/model-selection.md` | one paragraph, byte-identical pair | no | no |

The frozen set is `bootstrap/tests/fixtures/gate_manifest.json` > `frozen_files`. Four are
certain; `test_presets.py` and `test_onboarding_seed_roster.py` are also frozen and join if they
pin seed lists. All join the standing re-anchor on the `dev/PLANNING.md` board, the Maintainer's.
The AST figures are my reading, not the instrument's: the ceremony derives them against the
committed baseline (`bootstrap/AST_BASELINE_RUNBOOK.md`), and no touched symbol is in
`_UPDATE_ALLOWLIST`, so it is a Maintainer-run correction. Cairn's lockfile hashes the checker, so
the plan also owns `upgrade --finalize scripts/check_model_selection.py`.

Not touched: the stub, `config.py`, `lockfile.py`, `scripts/_onboarding/`, `tools/session.py`,
`templates/skills/_lib/session.py`, the profile schema, `scaffold.py --manifest`.

## Rationale

One design assumption, a person at a terminal, met a world where agents do most installs. The
cheapest honest fix speaks on the path agents take, makes the check trustworthy so the notice
is not crying wolf, and leaves a record that outlives the terminal. None of it changes the
install contract.

## Alternatives considered

* **Reword the stub's comments instead.** Rejected, and tested: I ran the real `merge_file` with
  the old stub as base, a reworded stub as theirs, and as ours both (a) the capture's output and
  (b) a hand-filled file. Both returned `conflict`. Adopters' old checkers would also keep failing
  until upgraded. The checker is verbatim, so unforked adopters take it as a clean update.
* **Profile keys or a CLI flag for the non-interactive fill.** Rejected in section 1.
* **An onboarding action trigger** reading the file. Right in kind (it reads state) and the only
  candidate that also reaches adopters already on the stub. Not the primary because its root is
  the goodnight helper, which has not run here (Q2). Cheap to add later: one evaluator, one entry
  per preset, no kernel change.
* **A step in the session-start routine.** `tools/session.py` is an executable trust root
  (`AGENTS.md` > High-risk surfaces); even a read-only surfacing there takes a Security Review of
  the kernel and reaches every adopter. Skill-body prose is agent-followed, the same root.
* **A fourth `quality_gate.py` sub-gate.** Cairn-only, and the integration pair names its subs.
* **Do nothing.** Costs another four months in whichever tree installs next.

## Documentation / doctrine surface

Governing layer: the module doc gains one paragraph; nothing under `doctrine/` changes, so the
doctrine rate-limit gate is not engaged. The notice and seed text are shipped adopter prose and
stay vendor-neutral (`quality_gate.py --sub neutrality`). Deliberation layer: this proposal.
Descriptive layer: no `docs/` page names this behaviour; the plan confirms by search.

## Evidence / verification plan

Falsified if a non-interactive install selecting `model-selection` prints nothing, the
hand-filled stub still exits 1, or Cairn's suite stays green with its mapping reset.

### Tests required

New tests go in `test_model_selection_stub.py`, named for the property:

* `TestCommentsAreNotPlaceholders`: a hand-filled stub with every comment kept exits 0; the
  shipped stub exits 1; `FILL ME` in a value line exits 1. Replaces `test_fill_me_in_comment_fails`.
* `TestNoticeOnEveryInstallPath`: a no-terminal install prints the notice and exits 0; an
  interactive install that skips every tier prints it; a filled file is silent;
  `--adopt-module model-selection` prints it for the stub and is silent for a filled file.
* `TestCaptureNeverClobbersAHandFilledMapping`; `TestCaptureRefusesToWriteThroughASymlink` (the
  outside file is byte-identical afterward, the install still exits 0).
* `TestEngineAndCheckerAgreeOnUnfilled`; `TestThisRepositorysMappingIsFilled`.
* Seeds present at moderate and complex, absent at simple, in the preset test home.

Boundary B mode is **full**: the engine, a verbatim adopter script and the install overlay are
touched, and uncertainty resolves to full.

### Examples / smoke checks

`scaffold.py --config <profile> --target <tmp> --non-interactive` prints the notice;
`scaffold.py --manifest` is byte-identical before and after; the checker returns 1, 0 and 0 on the
stub, a hand-filled stub and Cairn's file; the claim, link and neutrality gates on the prose.

#### Security preflight — five questions, answered in writing

* **S1 — Who supplied it?** The notice and "already filled" decisions read one adopter-tree file,
  writable by anyone who can write the tree, and that file supplies the input it is judged by.
  The notice carries no authority; the overwrite decision does, and is guarded in S4. The path
  also comes from the tree, hence the symlink check.
* **S2 — Can it fail?** Mutations, each owed to the plan with its result: drop the comment skip
  (hand-filled test fails); make the helper return `[]` (install test fails); remove the guard
  (symlink test and `test_security_leaf` fail). A parity test over identical source text could
  not fail, so it compares behaviour on a corpus. Premises I ran now: the hand-filled stub exits 1
  on today's checker; the symlink write-through happened.
* **S3 — What fires it, over what?** The notice: `scaffold.py` install and `upgrade
  --adopt-module`, over the one mapping path. The check: a person or agent running
  `python scripts/check_model_selection.py`, plus the suite in Cairn only. The notice says
  "nothing else runs that check for you", true in adopter trees; the module paragraph says the
  suite runs it in Cairn.
* **S4 — Which way does it break?** Helper on an unreadable or symlinked file: prints a notice,
  the louder side. Capture on a refused guard: writes nothing and says so. Comment skip: a
  `FILL ME` left only in a comment passes. That is less strict, accepted because the check
  attests shape, not truth, and a false failure teaches people to route around it.
* **S5 — Who still wins?** Assumed: someone who can write the tree. They can still enter
  plausible model names or edit the tree-local checker; the check cannot tell. The symlink write
  is closed by the shared guard, which is closure by enumeration (the pinned inventory), not by
  construction.

## Signals the change is wrong

The notice becomes noise people stop reading. Agents fill all three tiers with their own model to
silence it (look for `source` lines reading "recorded at install"). The comment rule lets an
unfilled row through. A seed task outlives its purpose and nobody deletes it.

## Scope delta

**Scope delta**: preserved. This is the opening text.

## Assurance path

**Assurance path**: high-assurance — the scaffold engine, a verbatim script adopters execute, and
the onboarding overlay written into every preset adopter's `dev/PLANNING.md`.

## Review -- Claude Sonnet 5.5 (Internal) -- 2026-10-18

**Model**: Claude Sonnet 5.5, a fresh session with no shared context, of the same agent family as the author; no cross-type distance. An Internal pass: it strengthens the change inside its structure, and, as asked, also answers the four stance questions below. The Security Review follows separately; items for it are flagged at the end, not probed.

```
Reviewed commit: 6a11e26366fb8072d1746c43b709c337835895c8
Target: the whole proposal, In brief through Assurance path; every cited fact checked against the working tree at d88a14f9479f7350f40853d9bbb7739e78aa7cae on 2026-10-18
Prior findings: none
Assurance path: high-assurance
```

**Tier**: Internal
**Findings**: raised (3 blocking, 4 non-blocking)
**Verdict**: REVISE

### Verdict in brief

**The change should happen, and its core is sound:** the notice on every install path, the checker fix, the symlink guard. I reproduced or confirmed by reading all four causes and both side-findings. Three things in the framing need answers before a Decision:

* The "durable line" (section 4) is not a trigger in the sense `AGENTS.md` uses the word, and the reason the proposal gives for rejecting the onboarding trigger applies to it equally (MM-1).
* One of its three seed copies can never render and would turn a pinned test red (MM-2).
* The only live instance of this failure that I could find, the unfilled mapping in `lhm`, is out of reach of everything proposed. Question 3 should flip to yes (MM-3).

**The strongest alternative the proposal did not weigh** is to put the question inside the agent's own install checklist (BOOTSTRAP.md II-5), which the installer already tells the agent to run last. It adds one line of prose and no engine symbol.

### Steelman

One assumption, a person at a terminal, met a world where agents run installs, and the one tree where it mattered went four months with a failing check nobody ran. The proposal speaks on the path agents take, stops the check failing on a correctly filled file so the notice is not crying wolf, refuses to invent a non-interactive way to answer a question only the Maintainer owns (no flag, no profile key), and leaves the install contract alone. That restraint is right, and most of what follows asks for corrections, not additions.

### Findings

#### MM-1 -- BLOCKING: the seed task is not a trigger, and the proposal's own objection to the onboarding trigger applies to it

**Plain:** a line in a file that nothing tells anyone to open fails the same way the unrun check failed. The proposal says "a notice scrolls away; a task in `dev/PLANNING.md` does not" and rejects the onboarding trigger because it "would sit unseen". Both depend on someone reading the file.

* Cairn's own `dev/PLANNING.md` onboarding slot still holds all eight seeds the self-host commit `7519c5da` wrote on 2026-06-12. None is removed or marked, though the board's rule is that finished items are removed. One of them (`agent-team-onboarding`, about capability tiers) is the closest relative of this task. A seed has no done-mark, so the list cannot tell outstanding from finished.
* Nothing in the routines reads that slot. `tools/session.py` has no reference to `PLANNING.md` or onboarding (searched). The `session-start` skill runs `session.py` and `tools/board.py`; the board reads proposal and plan headers, and under `--maintainer` only rows carrying the Waiting marker.
* No mechanism carries a new seed into an existing tree. The seed text lives in `templates/onboarding/*.md`, not in `PLANNING.md`'s own template, and the upgrade code notes that onboarding slot bodies are not reproduced, because they sit inside slots on the adopter's side of a merge (`bootstrap/_scaffold/upgrade.py:880-884`). I read that; I did not run an upgrade.
* So, under "check what it checks, and open it", the seed's chain ends at "someone opens PLANNING.md": a person remembering, like the check. That is acceptable if written down, and it is not.

**Recommend:**
(a) Say so in Question 2 and the S3 answer.
(b) Add the trigger that sits on the agent's path. `scaffold.py` ends its output with "5. Run the R-F acceptance gate (II-5)" (I ran an install; it is line 136 of 169). II-5 (`bootstrap/BOOTSTRAP.md`, "All items below must pass before declaring the installation complete") already checks unfilled tokens and slots and says nothing of the mapping. One item: "if `model-selection` was installed, `python scripts/check_model_selection.py` exits 0; ask the Maintainer which model fills each tier, do not guess." That puts the question inside a step the installing agent is told to finish. It is prose in a file that is not frozen and is not the fidelity manifest (`bootstrap/fidelity-check.md`); the only test reading BOOTSTRAP.md reads the Appendix B and preset example blocks (`test_profile_grammar.py:1001-1131`), and the plan should confirm it does not pin II-5.
(c) If the seed stays, write it as a marked row (`**Waiting on Maintainer**: fill the model mapping`, under 48 characters), so `python tools/board.py --maintainer` lists it. That marker exists for "a question only they answer" (`templates/core/dev/PLANNING.md:97`) and ships to adopters.

Do not cut the seed to make this tidy: the durable line is a baseline outcome (In brief, item 4), so removal would be a Scope delta only the Maintainer can allow. (a)-(c) preserve it.

#### MM-2 -- BLOCKING: the solo-greenfield seed never renders at that preset's own settings, and it turns a pinned test red

**Plain:** one of the three seed copies is dead text, and adding it breaks the test that guards the seed lists.

* solo-greenfield's complexity is `simple` (`bootstrap/_scaffold/config.py:1356`), so `cairn:if complexity in moderate,complex` strips the seed. I ran `strip_conditional_regions` with each preset's axes on a two-seed sample: 1 of 2 kept for solo-greenfield, 2 of 2 for the other two.
* `test_onboarding_slot_substitution.py::TestInstallPath::test_slot_seed_count_matches_source[solo-greenfield]` counts `* [seed;` in the rendered slot against the source file and demands equality. The source gains one, the slot does not: red. That file is frozen, so it would be another re-anchor entry. (From reading the test and the strip run; I did not edit a template to watch it fail.)
* The gate is keyed on `complexity`, but the module also follows `modules_add` and `modules_remove`. A moderate-complexity install with `model-selection` removed renders a seed naming `scripts/check_model_selection.py`, a surface the roster did not install, which `test_onboarding_seed_roster.py` exists to prevent. The seed's "If `...mapping.yml` exists" opening hedges it; say that this is why it is there.

**Recommend:** ship the seed in the two presets that install the module at their own settings (collaborative-team, high-rigor-legacy). Because "installs from a preset get one" is baseline wording, record the solo copy in the Scope delta as dropped-for-cause (it has no behaviour) for the Maintainer's allowance, or keep it and amend the count test.

#### MM-3 -- BLOCKING: leaving `upgrade` out leaves the one live case unreached, and the recommendation to leave it out rests on code that was not read

**Plain:** the unfilled mapping that exists today is in your science repository `lhm`, and nothing in the proposal tells anyone about it.

* Read-only, in the sister repository `lhm` (outside this tree; I changed nothing): its `dev/.cairn/model-selection-mapping.yml` is the stub (8 lines carrying `FILL ME`) and the checker exits 1. The only commit that ever touched that file is its 2026-06-10 upgrade commit `22413d95`. So the stub reached it through `upgrade`, a third arrival path that "every install and every `--adopt-module`" omits. (`modflow_tools` filled its file by hand and exits 0.)
* Nothing proposed can reach it: the seed is not delivered by upgrade (MM-1), the suite test covers only Cairn, and the notice fires at install and adopt. Cairn's own case is fixed (`22dabd45`); `lhm`'s is not, and its next upgrade will say nothing.
* The call sites exist. In `cmd_upgrade` (`upgrade.py:2287`) `lock` and `target` are in scope at all three exits: `--apply` (2471), `--stage` (ends 2522), and the default plan (ends 2534). The helper needs only the target; gate it on `"model-selection"` in `lock["modules"]`. One call before the dispatch also works, at the cost of printing above a long report. Price: `cmd_upgrade` is a baselined symbol, so the Maintainer-run ceremony gains a fourth CHANGED entry.

**Recommend:** flip the recommended answer to yes, name the call site, and add `cmd_upgrade` to the accounting in section 5.

#### MM-4 -- non-blocking: the comment rule is right for the defect that was observed, but has two holes and one lost feature

**Plain:** ignoring comment lines cures the false failure, but a `FILL ME` can still sit where the rule thinks it sees a comment, and the rule removes a check someone wrote on purpose. I ran the rule patched into scratch copies of the checker.

* **Spec detail.** "First non-blank character is `#`" must mean space or tab only. `str.lstrip()` strips Unicode whitespace: a line `U+00A0# FILL ME` after a valid row exits 3 with PyYAML (parse error) and **0 without it**. With `lstrip(" \t")` it exits 1 either way.
* **Block scalars.** A `#`-led line inside `model: |` is data, not a comment. That file exits 0 under the rule, PyYAML present. Where PyYAML exists the structural step already parses the file; have it also fail on any string value containing the sentinel. The dependency-bare path keeps the line rule, and the S4 answer should name this residual, which it does not (it mentions only comments). The engine erring toward "filled" here is the safe direction (it never clobbers).
* **Lost feature.** `test_fill_me_in_comment_fails` pins a deliberate behaviour, with its own example `# TODO: FILL ME -- add medium-tier model here`. Partial-fill markers now pass; the replacement test should pin that loss explicitly rather than only delete the old one. And `mapping: []` plus the header comments now passes (today it exits 1 only by accident of the stub's comments; under the rule, 0), and the notice goes silent with it, because the engine uses the same rule. Decide and record: either accept it under S4 ("attests shape, not truth"), or have `_structural_validate` require at least one row. I would tighten that one line.

#### MM-5 -- non-blocking: the notice tells an agent to fill "each FILL ME row", and the stub has one row

**Plain:** an agent following the notice literally fills the one row it sees with one model, and the check passes with one tier of three.

* The stub's `mapping:` holds a single list item whose five fields all read `FILL ME` (`model_selection_mapping_stub.yml:35-39`). The Terms ("five rows") and the notice ("each FILL ME row") both misdescribe it. The check never requires three tiers.
* Reword the notice: "The stub holds one placeholder row; replace it with one row per tier (high, medium, low), copying its shape." This sentence decides whether the agent-path result is right, so it is worth the care.

#### MM-6 -- non-blocking: nothing will say when the mapping goes stale, and the module doc says something will

**Plain:** the filled mapping is dated 2026-10-18 and names a re-verification trigger, and no routine reads either.

* `dev/modules/model-selection.md:156-157` (byte-identical to the template; the proposal edits both) says staleness is "surfaced by an existing routine". I searched `tools/`, `scripts/`, the skills and the doctrine for any reader of `date_verified` or the re-verification field and found none; only the capture writes them.
* The proposed suite test asserts "not the stub, parses", not "current".
* Add no mechanism (the standing direction is to fix defects and build nothing new). Correct that sentence in the same edit, so the new paragraph does not sit beside an unbacked claim, and record staleness in the proposal as a named residual that no part of this change addresses.

#### MM-7 -- non-blocking: the accounting is nearly right; four corrections

* **AST symbols, verified** against the committed baseline: `capture_model_selection_mapping`, `main` and `_cmd_adopt_module` are all baselined (3 CHANGED); `_mapping_is_unfilled` and `model_selection_notice_lines` would be 2 NEW, each needing a pin in `bootstrap/tests/fixtures/scaffold_ast_known_new.json`. Import-line edits cost nothing: the attestation skips imports. None is in `_UPDATE_ALLOWLIST`, so Maintainer-run is right. MM-3 adds `cmd_upgrade`.
* **The files table omits two ceremony files:** `scaffold_ast_known_new.json` (frozen) and `scaffold_ast_baseline.json` (not frozen). The seed test goes in `test_onboarding_seed_roster.py` or `test_presets.py`, both frozen, so that one is certain rather than "joins if they pin seed lists". The certain frozen set is the checker pair, `test_model_selection_stub.py`, `test_security_leaf.py`, `scaffold_ast_known_new.json` and the seed-test home; the count test joins if the solo copy stays.
* **The guard is right-sized** (one call, one inventory row, one test-set entry); answer Question 4 yes. Place it before the prompts, not after, so a person is not asked three tiers of questions and then told the write was declined. The guard makes three checks, so test a symlinked parent (`dev/.cairn` as a link) as well as a symlinked file.
* The install report is already on the board as too long (`dev/PLANNING.md`, F8: 22 unfilled slots on the smallest install). This adds a block to it. Cross-reference F8 in Context so whoever fixes the report folds this notice in.

### The four questions

**1. Should this happen as framed, and is there a better design?** Yes for sections 1-3. Section 4 needs MM-1 to MM-3. The better design is the same engine core (notice on install, adopt and upgrade; the checker rule with the MM-4 corrections; the guard) plus the II-5 line, the suite test, and the seed kept in two presets as a marked Waiting row. It adds one prose line and one call site, and removes one dead template copy.

**2. The strongest alternative.** The II-5 acceptance-gate line as the primary agent-path trigger (MM-1), absent from the Alternatives. Of those that are there: a session-start surfacing is the only candidate that would also catch staleness (MM-6); I do not press it, because the standing "build nothing new" direction is a fair reason to decline it. Rewording the stub is rejected on a conflict for "every adopter who filled the file"; today that is two repositories, both the Maintainer's (`dev/PLANNING.md` still lists the first external adopter as ahead), so its cost is smaller than stated. I still agree with the checker route, because it also repairs files already in the field.

**3. What would show it wrong.** (i) An agent-driven install of a moderate profile that reports done without having asked about models; the II-5 item would make that visible at the step where it happens. (ii) `lhm` still on the stub after its next upgrade. (iii) Seed lines untouched months on: Cairn's own slot is the base rate, 8 of 8 untouched since 2026-06-12. (iv) A mapping that passes with fewer than three tiers or with `mapping: []` (MM-4, MM-5); the proposal's own signal, `source` lines reading "recorded at install", also stands.

**4. What I did not cover.** I ran no pytest node and not the suite. I did not edit a template to watch the MM-2 count test fail; that rests on reading the test and the strip run. I did not re-run the author's `merge_file` conflict experiment. I read `_apply_upgrade` only at its call site, and did not run an upgrade to confirm MM-1's third bullet. I did not test non-3.13 interpreters or Windows line endings; the dependency-bare checker was simulated by blocking the `yaml` import. I read the sister repositories only for the mapping file and its history. Security probing was left to the Security Review.

### Recommended answers to the proposal's four questions

1. Stop counting comments: **yes**, with the MM-4 corrections.
2. Trigger: the notice, the II-5 line and the suite test; the seed in two presets as a marked Waiting row; no onboarding trigger now. I confirmed the premise for declining it: the activation log holds only its header beside 73 archived proposals, `onboarding_activate.py --dry-run` lists two long-fired tasks (it wrote nothing; the tree is unchanged), and the goodnight skill does not call the helper.
3. Notice on `upgrade`: **yes** (MM-3).
4. Symlink guard: **yes** (MM-7).

### For the Security Review (flagged, not probed)

* The capture call site catches `ScaffoldSecurityError` locally and continues. `SECURITY_MUTATIONS.md` says every refusal is caught once at the CLI top level (exit 2). The proposal's reason ("never blocks the install") is stated; confirm the quiet side is right, since files are already written and the lockfile is not.
* The notice helper reads a tree-controlled path and may follow a symlink. Keep the notice text fixed: never echo the path, an OS error message or file content (terminal control sequences; `encode_display` in `tools/session.py` is the one encoder).
* `seed_gitignore` is listed in `SECURITY_MUTATIONS.md` Class B as "contained by construction" on the strength of a fixed path, the same reasoning the capture write had until this proposal showed a fixed path can be a symlink. Not this change's to fix.
* MM-4 is a parser-differential class: the checker and the YAML loader disagree about what a comment is.
