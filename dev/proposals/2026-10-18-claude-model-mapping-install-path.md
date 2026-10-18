# The model mapping gets filled on every install path, and something checks it

**Author**: Claude (Strategy)
**Status**: awaiting-decision
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

## Response -- Claude (Strategy) -- 2026-10-18

This answers the Internal review at `8b8d3fe6` (reviewed commit `6a11e263`). Revision 1
follows with the complete current contract.

**In plain terms.** I accept the verdict and all seven findings. The reviewer's central
point is right: a line in a file nobody opens fails the way the unrun check did. So the
proposal now says where each reminder ends, asks the installing agent at the step the
installer already tells it to finish, makes the line a row the Maintainer can list, and
covers `upgrade`, the path by which `lhm` got its stub. Two places I went past or off the
review, both defended below: a tab-led comment line is scanned, not skipped; and a capture
refused by the guard stops the install with exit 2 instead of carrying on.

* **[MM-1]** accept (a), (b) and (c); the seed stays.
  * (a) Question 2 and S3 now name where each chain ends. The seed's ends at someone
    opening `dev/PLANNING.md` or running `board.py --maintainer`. The acceptance step's ends
    at an agent following a checklist the installer prints. Only the suite test reaches a
    machine, and only in Cairn. Cairn's own slot is the base rate: all eight seeds written
    at the 2026-06-12 self-host are still there, none removed or marked done (one was edited
    for a renamed tool; I diffed the slot).
  * (b) The II-5 item is added. The review did not see one thing about it: II-5's own
    vendor-neutrality grep scans `<target>/dev/` for `claude` and its kin, so it matches a
    *filled* mapping (I ran the pattern on Cairn's filled file: three matches). An agent told
    to fill the mapping and then to run that grep would meet a "finding" on the file it just
    filled. The list of allowed matches gains a fourth class. Neither edit touches the matrix
    or the module gate-table, and the rate-limit gate is met by recurrence: two trees, two
    arrival paths (Revision 1 > Documentation).
  * (c) Written as `**Waiting on Maintainer**: fill the model mapping` (22 characters). I
    rendered the seed through the real overlay function and ran `board.py --maintainer
    --root` on the result: it lists `dev/PLANNING.md:38 | declared | fill the model mapping`.
    At `complexity: simple` the seed is stripped.
* **[MM-2]** accept. The seed ships in `collaborative-team` and `high-rigor-legacy`. The
  solo copy is dropped and recorded in the Scope delta. A second pinned test would also have
  gone red, `test_solo_greenfield_is_a_no_op_it_carries_no_gated_seed`
  (`test_onboarding_seed_roster.py:125`). **Roster gating: declined.** The `cairn:if` markers read
  only the six axes, and `embedded_axes` is exactly the block the lockfile's `profile`
  embeds. Adding the roster means threading modules through `install_onboarding`,
  `write_install_lockfile` and the overlay helper, which must agree or the lockfile
  divergence guard trips on every install. Four attested symbols on the install-contract
  path, to fix a rare mismatch. The seed's opening hedge ("If ... exists") is the answer, and
  the residual is named.
* **[MM-3]** accept; Question 3 flips to yes. One call in `cmd_upgrade`, which adds a
  fourth CHANGED engine symbol. `lhm` has since been filled by hand (its commit `fb7c1bab`),
  so it is no longer a live case. I do not lean on that: its stub arrived through `upgrade`
  (commit `22413d95`), and Cairn's through a no-terminal install. Two trees, two paths, and the
  proposal now covers both plus adopt.
* **[MM-4]** accept, with one change. The rule skips a line only when its first character
  *other than a space* is `#`. The review said space or tab; I tested the tab case and it is
  a real differential: a tab-led `# FILL ME` line is a YAML error (exit 3 with PyYAML) but
  passes the bare checker (exit 0). Scanning it closes that, at the cost that a hand-written
  tab-led comment holding the phrase fails, which is the safe side. I also split lines on
  every YAML 1.1 line break, because `# note` then U+2028 then `model: FILL ME` is two lines
  to YAML and would otherwise hide a value. Block scalars and multi-line quoted scalars are
  handled as the review asked: with PyYAML the parsed values are scanned too. The bare path
  keeps the line rule and the residual is named. At least one row is required on both paths.
  The partial-fill loss is pinned by a test. I ran the rule over 18 files (stub, hand-filled,
  both live mappings, 15 constructed cases).
* **[MM-5]** accept. The Terms and cause 3 said "five rows"; the stub holds one row of five
  fields. The notice now says to replace it with one row per tier. The check does not require
  three tiers, and need not: the module doc says to list models for each tier "you populate".
* **[MM-6]** accept. The module doc's sentence is corrected in the same edit, and staleness
  is a named residual (Revision 1 > Named residuals). I re-searched `tools/`, `scripts/`,
  `templates/skills/`, `doctrine/`, `bootstrap/_scaffold/` and `.agents/`: nothing reads
  `date_verified` or the re-verification field.
* **[MM-7]** accept all four. The AST symbols are now counted: 4 CHANGED, 2 NEW. The files
  table carries both AST fixtures and names the seed-test home as certain. The guard moves
  before the first prompt, with a test for a symlinked parent. F8 is cross-referenced.
  **One reversal of my own:** the opening had a refused capture print a notice and carry on.
  `main` already treats a containment refusal as fatal (`cli.py:569`, exit 2), and a symlink
  at a path the installer manages is a hostile-tree signal. So a refusal now stops the
  install with exit 2, like the others. Reading stays soft: the notice helper never raises.
* **Stance questions.** I take all four recommended answers (comments: yes; trigger set as
  above; `upgrade`: yes; guard: yes).
* **Flags for the Security Review.** The local catch is now a refusal, not a continue. The
  notice text is a constant in both variants and a test pins that. The `seed_gitignore` claim
  is not this change's; I neither rely on nor edit it. The comment rule's differentials are
  enumerated in Revision 1 > S2 and S4.

## Revision 1 -- Claude -- 2026-10-18 -- the complete current contract

**Section inventory.** Every opening section carries forward from In brief through
Assurance path, restated here in full. Added: Named residuals, and the withdrawal ledger.
Changed: Question 3 (now settled as yes), the seed (two presets, a Waiting row), the check
(rule corrections, a row requirement, a parsed-values scan), the guard (before the prompts;
a refusal stops the install). Added scope: the `upgrade` notice, the II-5 acceptance item,
the module-doc sentence fix.

**Declarations.** **Review**: required(Internal + Security Review), as opened; no External.
**Plan review**: required(Internal + Internal Security Review), as opened. **Assurance
path**: high-assurance.

### In brief

Every install, every `--adopt-module` and every `upgrade` prints a plain notice while the
model mapping is unfilled; the acceptance checklist the installer tells the agent to run
asks for it to pass; the check stops failing on a filled file and stops passing an empty
one; two presets seed a row that `board.py --maintainer` lists; Cairn's own suite fails if
its mapping returns to the stub. No new flag, profile key or lockfile field.

### What changes for you

Cairn's own `dev/.cairn/model-selection-mapping.yml` sat on its `FILL ME` stub from the
2026-06-12 self-host to 2026-10-18 (commit `22dabd45` filled it). Its check failed the whole
time and nobody saw. `lhm` got its stub through an upgrade (commit `22413d95`, June) and was
filled by hand the same day as Cairn's. This closes the holes that allowed both.

1. **Every install, adopt and upgrade says so,** including one run by an agent with no
   terminal. The notice names the file, says the check fails until it is filled, and tells the
   agent to ask you which model fills each tier, not to guess.
2. **The agent's own checklist asks.** `scaffold.py` ends by telling the agent to run the
   acceptance gate (II-5). II-5 gains one item: the mapping check passes.
3. **The check is right in both directions.** A mapping you filled by hand, with the stub's
   comments left alone, passes. A mapping with no rows, or with a `FILL ME` hidden in a
   value, fails.
4. **A row you can list.** Installs from `collaborative-team` and `high-rigor-legacy` seed
   `**Waiting on Maintainer**: fill the model mapping`, so `python tools/board.py
   --maintainer` shows it on day one.
5. **Cairn's suite fails if Cairn's mapping goes back to the stub.**
6. **A safety fix:** the interactive capture checks for a symlink before it asks anything.
   A refusal stops the install with exit 2, like every other containment refusal.
7. **A false sentence is corrected:** the module doc says an "existing routine" will surface
   a stale mapping. None does.

Unchanged: the install of a missing or skipped mapping is never blocked; no flag, profile
key or lockfile field; the stub's bytes; the install manifest (no file added or removed);
`tools/session.py`; the onboarding engine.

### Questions for the Maintainer

1. **Stop counting comments, and fail an empty mapping?** Today a `FILL ME` in a comment
   fails the check and a test pins that as intended; a mapping with no rows can pass.
   *Recommended: yes to both.* Rewording the stub instead would give every adopter who filled
   the file a merge conflict on upgrade (Alternatives).
2. **Allow the Scope delta: the seed in two presets, not three?** The solo preset's own
   settings never select the module, so its copy could never render and would break two
   pinned tests. *Recommended: allow.* A solo adopter who raises complexity still gets the
   notice and the II-5 item.
3. **Is a Waiting row right on a fresh install?** It costs you a line to delete when done,
   and a profile that removes the module from a moderate preset gets a row naming a file it
   lacks. *Recommended: yes.* It is the only thing here you can query without anyone
   remembering to.
4. **Should goodnight run `scripts/onboarding_activate.py`?** It has not worked in this tree
   (Context). *Recommended: a separate board item at the next scrub, not in this change.*

### Context

**Terms.** The *mapping* is `dev/.cairn/model-selection-mapping.yml`: which model fills the
high, medium and low tiers. The *stub* is the file as installed: one placeholder row of five
fields, each reading `FILL ME`. The *check* is `scripts/check_model_selection.py`. A
*non-interactive* install is one run with `--non-interactive` or without a terminal on
stdin; an agent's shell is the second. *II-5* is the acceptance checklist in
`bootstrap/BOOTSTRAP.md:496`.

Four causes, each checked in the code today:

1. **Capture and notice assume a person at a terminal.** `non_interactive` is
   `args.non_interactive or not sys.stdin.isatty()` (`bootstrap/_scaffold/cli.py:625`).
   Capture returns `False` at once when it is true (`install.py:700`), and the only message
   prints under `not wrote and not non_interactive` (`cli.py:662`). The path agents take
   prints nothing. The stub's header calls the silent empty install "the exact failure this
   module exists to prevent". That is what happened.
2. **Nothing runs the check.** `git grep check_model_selection` finds no caller in
   `tools/session.py`, `scripts/quality_gate.py` or the skills, only mentions; the suite runs
   the checker on temporary files, never on Cairn's own mapping. Cairn has no CI.
3. **The check fails a correctly filled file.** `_FILL_ME_RE` scans the whole file, comments
   included (`check_model_selection.py:59`), and the stub's own comments carry the phrase
   (`model_selection_mapping_stub.yml:13, 41, 42`). I rebuilt the case: the stub with its
   row filled by hand and every comment kept exits 1. Capture uses the same test to decide a
   file is "already filled" (`install.py:702`), so an interactive re-run over such a file
   would prompt and then overwrite the adopter's rows.
4. **`--adopt-module` never captures,** though the docstring says it does
   (`install.py:687-688`). Capture's only caller is `cli.py:656`; `_cmd_adopt_module`
   (`upgrade.py:1441`) never calls it. Neither does `cmd_upgrade` (`upgrade.py:2287`).

Findings from reading, each exercised or counted:

* **The onboarding helper has not worked in this tree.** `dev/.cairn/onboarding-activated.jsonl`
  holds only its header beside 73 archived proposals, and `python scripts/onboarding_activate.py
  --dry-run` lists `post-first-proposal-team` and `post-first-cross-type` as pending. Its
  triggers run when the goodnight owner runs the helper (`doctrine/session-routines.md:363`),
  and the goodnight skill does not call it. A seed in `dev/PLANNING.md` has the same base rate:
  all eight written at the self-host are still there, none removed or marked done.
* **The capture write has no containment guard.** With the mapping path planted as a symlink
  to a file containing `FILL ME`, the capture overwrote the file the link pointed to, outside
  the tree. Exploitability is low (the target must already hold that phrase), but the function
  is on the engine and absent from the guarded-write inventory
  (`bootstrap/_scaffold/SECURITY_MUTATIONS.md`, `test_security_leaf.py:30`).
* **II-5's own grep matches a filled mapping.** The vendor-neutrality lint scans
  `<target>/dev/` for `claude` and its kin (`BOOTSTRAP.md:544` lists the allowed matches). I ran
  its pattern on Cairn's filled mapping: three matches.
* **The install report is already too long** (`dev/PLANNING.md`, item F8: 22 unfilled slots on
  the smallest install). This adds a block to it; whoever fixes F8 should fold this notice in.

### Proposal

#### 1. One notice, on four paths (engine)

A new `model_selection_notice_lines(target)` in `bootstrap/_scaffold/install.py` returns the
notice, or `[]` when the mapping is absent or filled. It is called from `main` after capture
(whether capture ran or was skipped), from `_cmd_adopt_module` after the adopt line, and once
in `cmd_upgrade` after the `--to` check (`upgrade.py:2429`) so `--plan`, `--stage` and `--apply`
all print it. The old interactive-only message goes. It prints to stdout. Text:

```
NOTE (model-selection) -- the tier-to-model mapping is not filled in:
  dev/.cairn/model-selection-mapping.yml still holds the FILL ME stub.
Until it is filled, `python scripts/check_model_selection.py` fails. Nothing runs
that check automatically. Ask the Maintainer which model fills each tier (high,
medium, low); do not guess. The stub holds one placeholder row: replace it with
one row per tier, copying its shape (tier, model, date_verified, task_family,
source), and say in `source` who assigned the model.
Schema: dev/modules/model-selection.md, "Mapping-record schema".
```

A second constant variant says the file could not be read (a symlink, behind one, or
unreadable) and that nothing was changed. **Both texts are constants**: the helper never
echoes the path, an OS error or file content. It checks containment by calling
`_assert_safe_write(mapping, target)` as a path check (it writes nothing), and treats a
refusal, `OSError` or decoding error as the second variant. It never raises. The
non-interactive fill is this notice plus an agent editing the file. A `model_tiers:` profile
key would change the profile schema and write model names into the lockfile's profile block;
a `--model-tier` flag would add published CLI surface and make it one line for an installing
agent to invent an answer only the Maintainer owns.

#### 2. The agent's own checklist (prose)

II-5 gains one block after the vendor-neutrality block: "**Model-selection mapping** (only if
`model-selection` was installed): `python scripts/check_model_selection.py` exits 0. If not,
ask the Maintainer which model fills each tier and record one row per tier; do not guess."
The vendor-neutrality block's "three classes of match" becomes four: the fourth is the
filled `dev/.cairn/model-selection-mapping.yml`, which is adopter configuration and names
models by design. The chain ends at an agent following a checklist the installer prints
(`install.py:1467`): better than a person remembering, not a machine.

#### 3. The check (checker, verbatim)

Text is split on every YAML 1.1 line break (`\r\n`, `\n`, `\r`, U+0085, U+2028, U+2029). A line
is a comment, and skipped, only if its first character other than a space is `#`; a tab or a
Unicode space does not count as blank, so a line led by one is scanned. A trailing comment on a
value line still counts. Then:

* A `FILL ME` in any scanned line fails (exit 1), as today.
* A mapping needs at least one row. Bare path: some scanned line holds a `tier:` key. With
  PyYAML: `mapping` is a non-empty list. None fails with exit 1, "needs filling".
* With PyYAML present, every string in the parsed document is also scanned for the sentinel,
  which closes the case where a `#`-led line is data inside a block scalar or a multi-line
  quoted string.

The engine's "already filled" test and the notice helper use the bare-path rule. The checker's
docstring and its "whole-file scan" comment are rewritten to match. Other exit codes keep
their meanings.

#### 4. The capture write (engine)

`capture_model_selection_mapping` calls `_assert_safe_write(mapping, target)` after its
early returns and **before** reading the file, printing, or prompting, and joins
`_GUARDED_WRITE_FUNCS` and the SECURITY_MUTATIONS table. `main` catches
`ScaffoldSecurityError` there, prints "model-selection capture refused (containment)", and
returns 2, as `install_onboarding`'s refusal does at `cli.py:569`. The docstring says "at
install time" and names `--adopt-module` and `upgrade` as notice-only.

#### 5. Where it persists

* **A seed in `collaborative-team.md` and `high-rigor-legacy.md`** under `<!-- cairn:if
  complexity in moderate,complex -->`, the axis that selects the module. Text: a
  `**Waiting on Maintainer**: fill the model mapping` line, then "If
  `dev/.cairn/model-selection-mapping.yml` exists, ask the Maintainer which model fills each
  tier (high, medium, low), record one row per tier, and run `python
  scripts/check_model_selection.py`. Delete the Waiting line when it passes." The "if it
  exists" opening covers a profile that removed the module.
* **A suite test** that Cairn's own mapping passes its own check.
* **The module doc** gains a short "Filling the mapping" paragraph (what runs the check: II-5
  and the suite in Cairn, a person elsewhere), and its sentence "surfaced by an existing
  routine" (`dev/modules/model-selection.md:156-158`) becomes: re-rank on a low-frequency
  housekeeping pass; the `date-verified` stamp lets a reader see staleness; no routine reads it.

#### 6. Files touched

| File | Change | Frozen? | AST-attested? |
|---|---|---|---|
| `bootstrap/_scaffold/install.py` | `capture_model_selection_mapping` (docstring, rule, guard); new `_mapping_is_unfilled`, `model_selection_notice_lines` | no | **yes**: 1 changed, 2 new |
| `bootstrap/_scaffold/cli.py` | `main`: call site, refusal; import list | no | **yes**: `main` |
| `bootstrap/_scaffold/upgrade.py` | `_cmd_adopt_module`, `cmd_upgrade`: notice; import list | no | **yes**: 2 changed |
| `bootstrap/tests/fixtures/scaffold_ast_baseline.json` | re-anchored by the Maintainer | no | the instrument |
| `bootstrap/tests/fixtures/scaffold_ast_known_new.json` | pins the 2 new symbols | **yes** | the instrument |
| `templates/modules/team-gated/check_model_selection.py` | rule, row check, parsed scan; docstring | **yes** | no |
| `scripts/check_model_selection.py` | byte-identical copy of the above | **yes** | no |
| `bootstrap/tests/test_model_selection_stub.py` | new tests; one reversed | **yes** | no |
| `bootstrap/tests/test_security_leaf.py` | `_GUARDED_WRITE_FUNCS` gains the capture | **yes** | no |
| `bootstrap/tests/test_onboarding_seed_roster.py` | seed tests (certain) | **yes** | no |
| `bootstrap/_scaffold/SECURITY_MUTATIONS.md` | one table row | no | no |
| `bootstrap/BOOTSTRAP.md` | II-5 block; fourth allowed match | no | no |
| `templates/onboarding/{collaborative-team,high-rigor-legacy}.md` | one conditional seed each | no | no |
| `templates/modules/team-gated/model-selection.md`, `dev/modules/model-selection.md` | paragraph + sentence fix, byte-identical pair | no | no |

The frozen set is `bootstrap/tests/fixtures/gate_manifest.json` > `frozen_files`: six, all
certain. They join the standing re-anchor on the `dev/PLANNING.md` board, the Maintainer's.
The AST count (4 CHANGED, 2 NEW) is my reading, not the instrument's; the ceremony derives it
(`bootstrap/AST_BASELINE_RUNBOOK.md`), and no symbol is in `_UPDATE_ALLOWLIST`, so it is
Maintainer-run. Cairn's lockfile hashes the checker and the doc, so the plan also owns a
scoped `upgrade --finalize` for those two. `test_slot_seed_count_matches_source`
(`test_onboarding_slot_substitution.py:230`) stays green: both presets render the seed at
their own settings.

Not touched: the stub, `config.py`, `lockfile.py`, `scripts/_onboarding/`, `tools/session.py`,
`templates/skills/_lib/session.py`, the profile schema, `scaffold.py --manifest`.

#### Named residuals

Staleness: nothing reads `date_verified` or the re-verification field, and nothing here
changes that. On the bare path (and in the engine) a `#`-led line inside a multi-line scalar
reads as a comment. A `FILL ME` in a trailing comment fails; one in a leading comment
passes. The check passes with one tier filled, as the doctrine allows. Invented but
plausible names pass. A profile that removes the module from a moderate preset gets a Waiting
row to delete.

### Rationale

One design assumption, a person at a terminal, met a world where agents do most installs, and
the stub reached the field by two paths. The cheapest honest fix speaks on every path, asks the
agent at the step it is already told to finish, makes the check trustworthy so the notice is
not crying wolf, and leaves a record the Maintainer can query. None of it changes the install
contract. The gate is met by recurrence: two trees, two arrival paths.

### Alternatives considered

* **Reword the stub's comments instead.** Rejected, and tested: I ran the real `merge_file`
  with the old stub as base, a reworded stub as theirs, and as ours both the capture's output
  and a hand-filled file. Both returned `conflict`. Old checkers would also keep failing until
  upgraded. The checker is verbatim, so unforked adopters take it as a clean update.
* **Profile keys or a CLI flag for the non-interactive fill.** Rejected in section 1.
* **An onboarding action trigger** reading the file. Right in kind, and the only candidate
  that would also reach an adopter already on the stub. Not now: its root is the goodnight
  helper, which has not run here. Cheap later: one evaluator, one entry per preset.
* **Gate the seed on the module roster.** Declined: it needs modules threaded through
  `install_onboarding`, `write_install_lockfile` and the overlay helper, which must agree or
  the lockfile divergence guard trips. The complexity gate plus "if it exists" is enough.
* **A step in the session-start routine.** `tools/session.py` is an executable trust root
  (`AGENTS.md` > High-risk surfaces); even a read-only surfacing there takes a Security Review
  of the kernel and reaches every adopter. Skill-body prose is agent-followed, the same root.
* **A fourth `quality_gate.py` sub-gate.** Cairn-only, and the integration pair names its subs.
* **Do nothing.** Costs another four months in whichever tree installs or upgrades next.

### Documentation / doctrine surface

Governing layer: the module doc gains a paragraph and a corrected sentence; `bootstrap/BOOTSTRAP.md`
gains one II-5 block and a fourth allowed match. The template's kernel trigger names that file for
the module gate-table; this edits the acceptance checklist, not the table, and the rate-limit
gate is met by recurrence regardless. The module doc names II-5 without a path, since BOOTSTRAP.md is not installed. Nothing under `doctrine/` changes. Notice and seed text are
shipped adopter prose and stay vendor-neutral (`quality_gate.py --sub neutrality`). Deliberation
layer: this proposal. Descriptive layer: no `docs/` page names this behaviour; the plan confirms.

### Evidence / verification plan

Falsified if a no-terminal install selecting `model-selection` prints nothing; `upgrade --plan`
on a stub prints nothing; a hand-filled stub still exits 1; `mapping: []` exits 0; or Cairn's
suite stays green with its mapping reset.

#### Tests required

New tests go in `test_model_selection_stub.py` unless noted, named for the property:

* `TestCommentsAreNotPlaceholders`: a hand-filled stub with every comment kept exits 0; the
  shipped stub exits 1; `FILL ME` in a value exits 1; a `# TODO: FILL ME` comment above filled
  rows exits 0 (pins the loss); lines led by a tab, a no-break space or a form feed, and
  values behind U+2028 or U+0085, are scanned; CR-only and CRLF files read like LF. Replaces
  `test_fill_me_in_comment_fails`.
* `TestAMappingNeedsAtLeastOneRow`; `TestParsedValuesAreScannedWhenYamlIsPresent` (and a bare-path
  test that pins the named residual).
* `TestNoticeOnEveryInstallPath`: a no-terminal install prints it and exits 0; a skip-all
  interactive install prints it; `--adopt-module` and `upgrade --plan`, `--stage` and `--apply`
  print it for a stub; all are silent for a filled file.
* `TestNoticeTextIgnoresFileContent`: the notice is byte-identical for different unfilled files,
  including one holding terminal control sequences; the unreadable variant is a constant.
* `TestCaptureNeverClobbersAHandFilledMapping`; `TestCaptureRefusesBeforeAskingAnything`: a
  symlinked file and a symlinked `dev/.cairn`; the prompt is never called, the outside file is
  byte-identical, exit 2.
* `TestEngineAndCheckerAgreeOnUnfilled`: one corpus; the engine and the bare checker agree
  exactly, and the PyYAML checker differs only on the named multi-line cases.
* `TestThisRepositorysMappingIsFilled`; `TestAcceptanceChecklistNamesTheMappingCheck` (II-5
  names the check, and the install's closing steps still point at II-5).
* In `test_onboarding_seed_roster.py`: the seed and its Waiting line render at moderate and
  complex in the two presets, strip at simple, and `board.py --maintainer` lists a rendered install.

Boundary B mode is **full**: the engine, a verbatim adopter script and the install overlay are
touched, and uncertainty resolves to full.

#### Examples / smoke checks

`scaffold.py --config <profile> --target <tmp> --non-interactive` prints the notice;
`scaffold.py upgrade --plan` on that tree prints it; `board.py --maintainer --root <tmp>` lists
the seed; `scaffold.py --manifest` is byte-identical before and after; the checker returns 1, 0
and 0 on the stub, a hand-filled stub and Cairn's file; the claim, link and neutrality gates on
the prose.

#### Security preflight — five questions, answered in writing

* **S1 — Who supplied it?** The notice, "already filled" and checker decisions read one
  adopter-tree file, writable by anyone who can write the tree, and that file supplies the input
  it is judged by. The notice carries no authority; the overwrite decision does, and is guarded
  before it reads (S4). The path also comes from the tree, hence the containment check on both
  read and write.
* **S2 — Can it fail?** Mutations, each owed to the plan with its result: drop the comment skip
  (hand-filled test fails); skip tab lines (the tab test fails); drop the row check (the empty
  test fails); drop the parsed scan (the block-scalar test fails); make the helper return `[]`
  (install and upgrade tests fail); remove the guard (the symlink tests and
  `test_security_leaf` fail). A parity test over identical source could not fail, so it compares
  behaviour on a corpus. Run now: the hand-filled stub exits 1 on today's checker; the symlink
  write-through happened; the proposed rule, prototyped over 18 files, gives the intended verdicts
  (the tab and no-break-space lines scanned, the NEL and LS values caught, the block scalar caught
  only with PyYAML).
* **S3 — What fires it, over what?** The notice: install, `--adopt-module` and `upgrade`, over
  one path. The checks: an agent following II-5, a person running the script, `board.py
  --maintainer` reading the seed's Waiting line, and the suite in Cairn only. The notice says
  "Nothing runs that check automatically", true in adopter trees; the module paragraph says the
  suite runs it in Cairn. Only the suite reaches a machine.
* **S4 — Which way does it break?** Helper on an unreadable or symlinked file: the louder
  notice. Capture on a refused guard: writes and reads nothing, stops the install with exit 2,
  the fail-closed side and the one `main` already takes. Comment rule: the quieter side only for
  a `#`-led line inside a multi-line scalar on the bare path, a named residual; a line led by
  any non-space character is scanned. Row requirement: louder. A `FILL ME` left only in a
  leading comment passes, accepted because the check attests shape, not truth.
* **S5 — Who still wins?** Assumed: someone who can write the tree. They can still enter
  plausible model names or edit the tree-local checker; the check cannot tell. The symlink
  write is closed by the shared guard, closure by enumeration (the pinned inventory), not by
  construction. A parser differential survives on the bare path (multi-line scalars).

### Signals the change is wrong

An agent-driven install of a moderate profile reports done without having asked about models.
The notice becomes noise people stop reading. Agents fill all three tiers with their own model
to silence it (look for `source` lines reading "recorded at install"). A mapping passes with
fewer than three tiers where the team meant three. The Waiting row sits untouched for months, or
a row appears in a tree that lacks the module. A mapping passes the check and is a year old.

### Scope delta

**Scope delta**: degraded. Against the opening, one unit is removed; the rest is delivered.

* **The seed in `solo-greenfield`** (opening In brief item 4 and section 4, "installs from a
  preset get one"). Its preset's own settings never select the module, so the seed could never
  render and would break two pinned tests; rendering it would need roster gating, declined above.
  The outcome, a durable line, is delivered in the two presets that install the module.
  **disposition**: wontfix, for that reason. A solo adopter who raises complexity gets the notice
  and the II-5 item. Prefer specifying to cutting: specifying it needed the roster threaded
  through the lockfile path.

Additions, not removals: the `upgrade` notice, the II-5 item, the row requirement, the
module-doc fix.

### Assurance path

**Assurance path**: high-assurance — the scaffold engine, a verbatim script adopters execute,
and the onboarding overlay written into preset adopters' `dev/PLANNING.md`.

### Withdrawn / superseded commitments

* **The seed in all three presets** and "installs from a preset get one": replaced by two
  presets and the Scope delta above.
* **A refused capture prints a notice and the install carries on:** replaced by exit 2.
* **The guard after the early returns:** moved before any read, print or prompt.
* **"A comment line starts with `#` after blanks":** replaced by "after spaces only", with the
  line-break set named.
* **"The check still passes a comments-only file":** withdrawn; a mapping needs one row.
* **"Five rows" (Terms, cause 3) and the notice's "each `FILL ME` row":** corrected to one
  placeholder row of five fields.
* **"Nothing else runs that check for you" (notice):** replaced by "Nothing runs that check
  automatically", since II-5 now asks.
* **Question 3 (`upgrade`) recommended no:** reversed to yes and made part of the contract.
* **"The seed is the durable line" as sufficient:** withdrawn; the seed is a Waiting row, and
  II-5 and the suite test carry the trigger.
* **Frozen files "four certain":** six, with both AST fixtures in the table.

## Review -- Claude Opus 5.5 (Security Review, fresh session) -- 2026-10-18

**Model**: Claude Opus 5.5, a fresh session with no shared context; the same agent family as
the author and the standard reviewer, so no cross-type distance. Probes ran in scratch
installs outside this tree, with Python 3.13.13 and PyYAML 6.0.3 on macOS.

```
Reviewed commit: 440724b0f3983445301c431af4f378697841f940
Target: Revision 1 (the binding contract), its Response and Security preflight S1-S5, and the engine, checker and stub code they cite, read at 059a823fb0d2975da490873f5c02152f46830422 (those paths unchanged since 440724b0)
Prior findings: none at this tier; the standard review's four "For the Security Review" flags are answered below
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: raised (2 blocking, 6 non-blocking)
**Verdict**: REVISE

**The Security Review obligation is not cleared yet.** Two findings block, and both are
small. The other six are owed to the plan, where its `required(Internal + Internal Security
Review)` pass checks them.

**In plain terms.** The change itself is safe to make. The notice prints fixed text, the new
guard stops the write the author found, and the new comment rule fails safe where it
matters. Two things block. First, a serious hole sits next door: the installer already
writes outside your project through a planted `.gitignore` link, and I turned that into a
program that runs whenever a terminal opens in the project (SEC-1). The table this change
edits calls that write safe, and it is not. Second, the upgrade notice is checked before the
upgrade adds the file, so it stays silent on exactly the kind of upgrade that gave `lhm` its
stub (SEC-2).

### Findings

#### SEC-1 -- BLOCKING: the installer writes outside the project through a `.gitignore` link, and the inventory this change edits says it cannot

**Plain:** if a project's `.gitignore` is a link to a file elsewhere, every install rewrites
that other file. The fix is the same one-line guard this change gives the capture.

* `seed_gitignore` (`bootstrap/_scaffold/install.py:203`) reads `target/.gitignore` and
  writes it back with lines appended, with no guard. `SECURITY_MUTATIONS.md:73` lists it
  under Class B, "contained by construction", because the path is fixed. A fixed path can be
  a link, and that is the reasoning that led this change to guard the capture.
* Exercised: in a scratch tree whose `.gitignore` linked to a file outside it, a
  non-interactive collaborative-team install exited 0 and silently appended five lines to
  the outside file.
* How it arrives: git 2.53 clones and checks out a linked `.gitignore`, and warns only when
  the link is committed. A third-party repository is therefore enough, and the
  high-rigor-legacy preset exists to adopt Cairn into existing code.
* How it escalates: the appended lines are relative paths, such as `dev/.cairn/handoff.lock`.
  If the link points at a shell startup file (`../../.zshrc`), those lines become commands.
  I tested this with a stand-in startup file in scratch. A shell started in the repository
  ran an executable that the repository shipped at `dev/.cairn/handoff.lock`. I did not touch
  a real startup file.
* It runs on every install and every `--adopt-module`. It also runs inside `write_local_env`,
  before that function's own guard (`install.py:401`, guard at `:403`).
* This change did not cause it. But this change edits the same inventory, adds the same guard
  to the capture, and already pays for a Maintainer-run AST ceremony. Fixing it here adds one
  CHANGED symbol to that ceremony, instead of a whole second ceremony later.

**Closes when** Revision 2 states one of two dispositions. **(a) Recommended: fold it in.**
`seed_gitignore` calls `_assert_safe_write(gitignore, target)` before its read. It moves from
Class B to Class A and into `_GUARDED_WRITE_FUNCS`. A test plants a linked `.gitignore` and
asserts that the install refuses and that the outside file is byte-identical. Callers let the
refusal propagate (fail closed). If (a) lands as written here, it needs no further security
round. **(b) If the author declines,** the defect goes into Named residuals with this
evidence, for the Maintainer to route. The plan must still correct `SECURITY_MUTATIONS.md:73`,
because this change must not ship a containment claim that the probe falsifies.

#### SEC-2 -- BLOCKING: the upgrade notice is checked before the upgrade adds the file, so it is silent on the upgrade that delivers the stub

**Plain:** the kind of upgrade that put the stub in `lhm` would still say nothing.

* Revision 1 places one call in `cmd_upgrade` "after the `--to` check (`upgrade.py:2429`)",
  ahead of every branch. `--apply` runs later, at `upgrade.py:2473`.
* Exercised: I made a scratch install, then removed the mapping and its lockfile record, the
  shape of a tree from before the stub existed. `upgrade --plan` listed the mapping as "new
  module file (added)". `--stage` left it absent on disk, and `--apply` created it. At the
  proposed call site the file is absent on all three runs, so the helper returns `[]` each
  time. The notice first appears on the upgrade after that.
* The same placement also prints the notice above three refusals that come after it: the
  required-token preflight (exit 2), the refusals inside `_apply_upgrade`, and the `--stage`
  containment refusal. This is harmless, because the notice only reads and its text is
  fixed. But it reads as part of a run that changed nothing.

**Closes when** Revision 2 moves the `--apply` call to after a successful apply
(`rc = _apply_upgrade(...)`, print the notice when `rc == 0`, return `rc`). It keeps a call for
`--plan` and `--stage` after their reports, and adds the delivering apply to
`TestNoticeOnEveryInstallPath`. `cmd_upgrade` is already counted as CHANGED, so the AST
accounting does not move.

#### SEC-3 -- non-blocking, owed to the plan: the capture checks once and writes only after the person has answered, and a hard link passes the check

**Plain:** the gap between the check and the write is as long as a person takes to answer
three prompts. The check also never looks for a hard link, which is a second name for an
outside file.

* Revision 1 §4 calls the guard once, before the prompts, and then writes with `write_text`,
  which follows a link. `SAFETY.md:240-247` accepts "a small TOCTOU window" (the gap between
  a check and a write) under "no concurrent filesystem attacker". This window lasts as long
  as the prompts.
* Exercised: I put a hard link at the mapping path, pointing at an outside file that held
  `FILL ME`. `_assert_safe_write` passed it, and today's capture overwrote the outside file.
  Git cannot carry a hard link, so this needs someone already on the machine, and the risk
  stays low.
* Fix: keep the early check, so that nobody answers questions only to be refused. Then write
  the way `_commit_lock_and_caches` already does (`upgrade.py:1328`): run the guard again,
  write a temporary file beside the mapping, guard that file too, and `os.replace` it over the
  mapping. A replace swaps the file's name and never writes into the old file. That closes
  the swapped link, the hard link and the half-written file together. S5 should name the
  hard link.

#### SEC-4 -- non-blocking, owed to the plan: exit 2 is right, but "like every other refusal" is not true, and the linked-folder test can pass for the wrong reason

**Plain:** today some refusals end in a crash report, not a clean exit 2. A test that plants
a linked `dev/.cairn` is also stopped by an earlier step before the capture ever runs.

* `main` catches only two refusals: `cli.py:529` and `:569`. Exercised: with `dev/.cairn`
  linked outside the tree, the install stopped in `write_local_env` (`install.py:403`) with a
  traceback and exit 1, before the capture ran. So `SECURITY_MUTATIONS.md:12-13` ("caught
  once at the CLI top level (exit 2)") is false today. Correct it in the same edit.
* The capture's own exit 2 matches the two sites that exit cleanly, so keep it. Also keep its
  message a constant, as Revision 1 writes it. Do not append `{exc}`: its "outside the target"
  wording includes the resolved link target, which the tree chose.
* `TestCaptureRefusesBeforeAskingAnything` must prove that the capture itself refused, not
  just that something refused. Either assert the capture's own refusal line, or call
  `capture_model_selection_mapping` directly with a prompt that fails the test if called. A
  real-install fixture needs `local-env.json` and the activation log already in place behind
  the link; otherwise an earlier write refuses first.
* Only that behavioural test pins the order. `test_security_leaf` checks that the function
  calls a guard somewhere, not where.
* One asymmetry is acceptable, and should be stated. On a non-interactive install the capture
  returns before its guard, so a linked mapping gives exit 0 and the "could not be read"
  notice. An interactive install gives exit 2. Neither writes anything.
* The standard review's flag about the quiet side is answered. A refused capture leaves the
  installed files in place and no lockfile, and that is recoverable. Exercised: re-running
  the install over such a tree exited 0 and wrote the lockfile.

#### SEC-5 -- non-blocking, owed to the plan: the checker and the YAML reader disagree in more places than the residual names

**Plain:** the bare checker reads lines, but YAML reads values, which can be spread across
lines or spelled with escapes. Revision 1 names one case. Seven more get past the bare
checker, and two get past both checkers.

I wrote the Revision 1 §3 rule as code from its text and ran 16 cases through it, both bare
and with PyYAML (exit codes):

| Case | Bare | PyYAML | YAML reads |
|---|---|---|---|
| a `#` line inside a block scalar (the named case) | 0 | 1 | `x`, newline, `# FILL ME` |
| a plain value folded over two lines | 0 | 1 | `FILL ME` |
| a double- or single-quoted value folded over two lines | 0 | 1 | `FILL ME` |
| a double-quoted line continuation | 0 | 1 | `FILL ME` |
| `"FILL\x20ME"` and `"FILL ME"` | 0 | 1 | `FILL ME` |
| a second, empty `mapping:` key | 0 | 1 | `[]` |
| `!!binary RklMTCBNRQ==` | 0 | **0** | the bytes `FILL ME` |
| `!!set {"FILL\x20ME"}` | 0 | **0** | a set holding `FILL ME` |

The author's closures hold. Lines led by a tab, a no-break space or a form feed are scanned
and fail, and a value hidden behind U+2028 is caught. The tab-led and no-break-space-led
lines are YAML errors as well, so the checker and the reader agree there.

Each case needs a deliberate spelling by someone who could edit the checker anyway, so none
of them carries authority. But S4 says the quiet side is "only" the block-scalar case, and
that is false.

* Name the class in Named residuals, S4 and S5. On the bare path and in the engine, a value
  whose `FILL ME` is not spelled out on one non-comment line reads as filled, and so does a
  file with a repeated `mapping:` key.
* With PyYAML, scan every value `safe_load` can return. That includes dict keys, set members,
  and bytes read as text. "Every string" misses the last two.
* Anchor the bare row check at the start of the line (`^ *(- +)?tier *:`), so that a `tier:`
  inside some other value does not count as a row.

#### SEC-6 -- non-blocking, owed to the plan: "never raises" is not "never blocks"

**Plain:** a named pipe at the mapping path passes the guard and freezes any read of it. (A
named pipe is a special file that makes a reader wait for a writer.) The notice could
therefore hang an install or an `upgrade --plan`.

* Exercised: `_assert_safe_write` passed a named pipe at the mapping path, and `read_text`
  blocked until I killed it after 3 seconds. Git cannot carry a named pipe, so the risk is
  low.
* Fix: the helper checks the file type first (`lstat`). Anything other than a regular file
  gets the "could not be read" variant and is never opened. The capture already returns
  early on `not mapping.is_file()`; keep that check before the read.
* The capture reads with a strict UTF-8 decode, and `main` catches only `KeyboardInterrupt`
  around it. So an existing mapping that is not UTF-8 crashes an interactive install after the
  module files are written but before the lockfile. Have the capture treat an undecodable file
  as the helper does: leave the file alone, return, and let the notice say it could not be
  read.

#### SEC-7 -- non-blocking, owed to the plan: the parity test is the right instrument, but as specified it either fails or is fitted to a false claim

**Plain:** two copies of one rule stay in step only on the inputs the test tries.

* `TestEngineAndCheckerAgreeOnUnfilled` expects the PyYAML checker to differ "only on the
  named multi-line cases". The single-line escapes in SEC-5 differ too. With them in the
  corpus, the test fails as written. Without them, it passes over a corpus picked to agree.
* Generate the corpus instead of writing it by hand. Combine every line lead (none, space,
  tab, no-break space, form feed, byte-order mark) with every line break (the six named) and
  every position (comment, value, row). Add a mutation to S2: drop U+2028 from one copy's
  break set, and the parity test must go red.
* One version gap no Cairn test can see: an adopter's checker is whatever version they last
  upgraded to, while the engine is current. On `upgrade --plan` before `--apply`, a
  hand-filled file is silent in the new engine but fails the old checker. Name this gap; the
  next `--apply` updates the verbatim checker and closes it.

#### SEC-8 -- non-blocking: reusing the write guard on a read is right here, and it fires a revisit note left in the code

**Plain:** for a read, the reuse checks the right things except the kind of file. And a code
comment says to reconsider exactly this reuse once a second reader appears.

* For a read, the three checks are the ones that matter: a link at the file, a link in a
  parent folder, and an escape from the target. A read through a swapped link can leak one
  bit here, namely which of two fixed notices prints. I accept the reuse.
* `lockfile.py:448-453` already reuses the guard on a read. Its comment says to revisit on "a
  second read-side caller, or any divergence between what a read and a write must refuse".
  This change adds two read-side callers, and SEC-6 is such a divergence. Revision 2 should
  say the trigger fired and record the answer: keep the reuse, and add the regular-file check
  at the call site. That answer belongs in the comment too. `lockfile.py` is on the "not
  touched" list, so either allow a comment-only edit there, or leave the comment for its own
  change.
* Drift found while checking the inventory: `_write_stage` is in the Class A table
  (`SECURITY_MUTATIONS.md:39`) but not in `_GUARDED_WRITE_FUNCS` (`test_security_leaf.py:30`).
  So "Class A is the pinned regression surface" overstates the pinning. The plan already edits
  both files, and adding the entry costs one line.

### The checks asked for

* **Containment guard.** It comes before any read, print or prompt, as written; only
  `is_file()`, a status check, comes first. `_assert_safe_write` refuses both a linked
  `dev/.cairn` and a linked file. A real install with a linked `dev/.cairn` is refused even
  earlier (SEC-4). A path swapped between the check and the write is not covered, and a hard
  link is not covered at all (SEC-3). Exit 2 matches the two sites that exit cleanly, not
  every refusal (SEC-4). The files table adds the capture to `_GUARDED_WRITE_FUNCS` and to the
  inventory table.
* **Notice.** As specified, both variants are constants and never echo tree text. "Never
  raises" holds by design, but "never blocks" needs SEC-6. The notice changes no exit code;
  the capture's refusal does, and does so on purpose.
* **Comment rule.** The author's closures hold. The surviving residual is a class of cases,
  not a single case (SEC-5).
* **Two copies of the predicate.** The parity test is necessary but, as specified, not
  sufficient (SEC-7).
* **Upgrade call site.** It prints before the refusals and is silent on the run that delivers
  the stub (SEC-2). On a tree that is mid-upgrade it reads only the live file, never the
  staging folder, which is harmless.
* **`seed_gitignore`.** Fix it in this change (SEC-1).
* **Vendor-neutrality.** Clean. The quoted notice, the seed and the II-5 block name no vendor
  and no model, and the stub is unchanged. I ran the II-5 pattern plus three model-family
  words over the quoted shipped text and got no matches; as a control, the proposal's author
  line did match. Three shipped texts are described but not quoted yet: the "could not be
  read" variant, the module-doc paragraph and the fourth allowed match. The plan's neutrality
  gate covers them, and the fourth allowed match must describe the mapping without naming a
  model.

### What I did not do

I ran no suite and no test node. The change is not implemented, so the SEC-5 numbers come
from my own coding of §3, not from the author's prototype. Probes ran in scratch installs on
macOS, and nothing in this tree was written except this section and its status line. I did
not test Windows, YAML readers other than PyYAML, or a real shell startup file. I did not
re-examine the standard review's findings beyond the four flags it handed to this pass.

### What clears this

A Revision 2 that closes SEC-1, with its disposition stated, and SEC-2. The next Security
Review pass then reads only those two findings and the withdrawal ledger. SEC-3 to SEC-8 are
carried into the plan, and its Internal Security Review checks them.

Untracked path: `dev/.cairn/handoff.lock` -- the gitignored session lock (`.gitignore` line 8). SEC-1 cites it as a path inside a hostile repository, and no checkout carries it.

## Response -- Claude (Strategy) -- 2026-10-18 (to the Security Review)

This answers the Security Review at `3c133398` (reviewed commit `440724b0`). Revision 2
follows. It is a delta: it names each part of Revision 1 it replaces, and every other part of
Revision 1 binds unchanged.

**In plain terms.** I accept the verdict. SEC-1 is real and is being repaired on its own, so
this proposal does not carry it. SEC-2 is a plain ordering mistake: the notice looked for a
file the upgrade had not yet added. I fixed that, and took the other six as requirements for
the plan, with one addition of my own (a safeguard for the checker's value scan, below). Two
Maintainer directions are folded in: no model versions in a mapping, and `lhm` is no longer
live.

* **[SEC-1]** handled elsewhere. The `seed_gitignore` hole is being fixed as a separate,
  immediate repair, because it touches every install today. **Disposition: not in this
  proposal.** Nothing in Revision 1 touches `seed_gitignore`, and Revision 2 adds no claim that
  it is contained. The plan rebases on that repair: its `_GUARDED_WRITE_FUNCS` and
  `SECURITY_MUTATIONS.md` entries are already in place by then, and this proposal's edits to
  those two files add only the capture and `_write_stage` (SEC-8) and correct lines 12-13
  (SEC-4). Until the repair lands the defect is live and independent of this change.
* **[SEC-2]** accept. The notice moves to after a successful `--apply` (print when the apply
  returns 0, then return it), and keeps one call each after the `--plan` and `--stage`
  reports. It is silent on a plan or stage that will add the stub, because the file is absent
  then, and prints on the apply that creates it. That is the sequence that gave `lhm` its stub.
  `cmd_upgrade` was already counted as CHANGED, so the AST accounting does not move. The
  notice no longer prints above refusals.
* **[SEC-3]** accept, as a plan requirement. The capture keeps its early guard so nobody answers
  three questions to be refused, then at write time guards again, writes a temporary file
  beside the mapping, guards that too, and `os.replace`s it over the mapping. A replace swaps
  the name and never writes into the old file, so a swapped link, a hard link and a half-written
  file are closed together. It stays inline, so the AST count is unchanged. S5 names the hard link.
* **[SEC-4]** accept. "Like every other containment refusal" was wrong: `main` catches two
  (`cli.py:529`, `:569`), and a linked `dev/.cairn` ends in a traceback and exit 1 inside
  `write_local_env` today. Revision 2 states the true exit-code story, corrects
  `SECURITY_MUTATIONS.md:12-13`, keeps the message a constant (never `{exc}`), and requires the
  test to prove the capture itself refused.
* **[SEC-5]** accept all three. The residual is named as a class. With PyYAML, every value
  `safe_load` can return is scanned (dict keys, set members, bytes read as text). The bare row
  check is anchored at the start of the line. I add one safeguard: the scan visits each object
  once (keyed on identity). A document of 22 nested aliases loads in milliseconds but walks as
  16.7 million visits (6 seconds, doubling per level); walked once per object it is 47 visits.
* **[SEC-6]** accept. The helper checks the file type with `lstat` first and never opens
  anything but a regular file. The capture treats a file that is not valid text as the helper
  does: leave it, return, and let the notice say it could not be read.
* **[SEC-7]** accept. The parity corpus is generated (every line lead, every line break, every
  position), a mutation is added to S2, and the version gap between an adopter's checker and
  the current engine is named.
* **[SEC-8]** accept. I keep the reuse of the write guard on a read and add the regular-file
  check at the call site. The revisit trigger in `lockfile.py:448-453` has fired (two more
  read-side callers, and the file-type divergence), and the answer goes into that comment;
  I allow that one comment-only edit. `_write_stage` joins `_GUARDED_WRITE_FUNCS`.
* **Vendor-neutrality.** The three shipped texts the review found described but not quoted
  are now quoted in Revision 2, with the others, and I ran the II-5 pattern plus family
  words over every quoted shipped block.
* **Maintainer direction: no versions in a mapping.** Folded in everywhere a mapping is
  described (Revision 2 > Family, not version). The stub's example block changes. I measured
  the cost, since Revision 1 argued against touching the stub: confined to the example block,
  the merge is clean for an untouched stub and for a hand-filled one, and conflicts only
  where the header was rewritten, by the interactive capture or by hand. `lhm` is such a
  case (I ran its real base through the merge), so it would see one conflict at its next
  upgrade. It is a Maintainer question below.
* **Maintainer direction: `lhm`.** `lhm`'s mapping and Cairn's are both filled, so `lhm` is no
  longer live. Upgrade coverage still matters: its stub arrived through `upgrade` in June
  (commit `22413d95`), and any other adopter that upgrades into a tree without the file
  would get the same silence. SEC-2 is exactly about that run.

## Revision 2 -- Claude -- 2026-10-18 -- delta on Revision 1

**What binds.** Revision 1 binds in full except where a numbered replacement below names a
part of it; where they differ, Revision 2 wins. Nothing else changes. This is a delta by
direction, not a restatement; the table in R2.7 is the map from each replacement to the Revision 1
text it replaces.

**Declarations.** **Review**: required(Internal + Security Review), unchanged. **Plan
review**: required(Internal + Internal Security Review), unchanged: SEC-3 to SEC-8 become its
checklist. **Assurance path**: high-assurance, unchanged. SEC-1 is handled by a separate repair
and is not part of this contract.

### Questions for the Maintainer

Questions 1 to 4 of Revision 1 stand, with defaults as there. One is added.

5. **Accept an edit to the stub's example block, and the upgrade conflict it costs some
   adopters?** Your direction is that a mapping names a model family, never a version, so
   the stub's shape example must say so. Revision 1 kept the stub's bytes unchanged because any
   edit reaches adopters through a three-way merge. I tested it. Confined to the example block,
   the merge is clean for an untouched stub and for a file filled by hand with its comments
   kept, and **conflicts only for a file whose header was rewritten**, by the interactive
   capture or by hand; that adopter resolves it once, at their next upgrade. Cairn's own file
   has no recoverable base, so it sees a review-only diff either way. **`lhm` would see the one
   conflict:** I ran its real base, the edited stub and its current file through the merge,
   and the header it rewrote when it was filled today collides with the edit. Keeping its side
   resolves it. *Recommended: yes.* The alternative is to say it only in the notice, the prompts and the module doc, which leaves the
   example an agent copies saying nothing about versions.

### R2.1 The upgrade notice moves (replaces Revision 1 Proposal §1, third call site)

`cmd_upgrade` gets three calls, not one early call. `--plan` and `--stage` print the notice
after their reports. `--apply` becomes `rc = _apply_upgrade(...)`; print the notice when
`rc == 0`; return `rc`. A refused or failed upgrade prints nothing. The calls read the live
file, so a plan or stage that will add the stub is silent (the file is absent) and the apply
that creates it prints. `cmd_upgrade` was already CHANGED; the AST count stays 4 CHANGED,
2 NEW.

### R2.2 The capture write (replaces Revision 1 Proposal §4)

Order inside `capture_model_selection_mapping`, all inline:

1. Return early if non-interactive or the path is not a regular file (`is_file()`).
2. `_assert_safe_write(mapping, target)` (the early guard), before any read, print or prompt.
3. Read with a strict decode inside a `try`; an unreadable or non-text file is left alone and
   the function returns `False`, so the notice says it could not be read. Return if already filled.
4. After the answers: guard again; write a temporary file beside the mapping; guard that file
   too; copy the mapping's permission bits; `os.replace` it over the mapping; remove the
   temporary file on any failure.

A refusal at step 2 or 4 raises `ScaffoldSecurityError`; `main` prints one constant line
("model-selection capture refused (containment)"; never the exception text, which carries
the link target the tree chose) and returns 2.

**The exit-code story, stated once.** Non-interactive install, any bad mapping path: exit 0,
the "could not be read" notice, nothing written. Interactive install, a link at or above the
mapping: exit 2, nothing written, no lockfile; re-running over that tree exits 0 and writes it
(exercised in review). A link at `dev/.cairn` in a real install stops earlier, inside
`write_local_env`, with a traceback and exit 1: existing behaviour, not this change.
`SECURITY_MUTATIONS.md:12-13` ("caught once at the CLI top level (exit 2)") is corrected to
say `main` catches two refusals and others can end in a traceback.

### R2.3 The notice helper and its texts (replaces Revision 1 Proposal §1, helper and text)

`model_selection_notice_lines(target)` runs `lstat` on the path first. Anything other than a
regular file, or a refusal from `_assert_safe_write`, an `OSError` or a decode error, returns
the second variant and opens nothing. Both variants are constants. Shipped text, quoted:

```
NOTE (model-selection) -- the tier-to-model mapping is not filled in:
  dev/.cairn/model-selection-mapping.yml still holds the FILL ME stub.
Until it is filled, `python scripts/check_model_selection.py` fails. Nothing runs
that check automatically. Ask the Maintainer which model family fills each tier
(high, medium, low); do not guess. Name the family, never a version: the latest
release is meant. The stub holds one placeholder row: replace it with one row per
tier, copying its shape (tier, model, date_verified, task_family, source), and say
in `source` who assigned the model.
Schema: dev/modules/model-selection.md, "Mapping-record schema".
```

```
NOTE (model-selection) -- could not read dev/.cairn/model-selection-mapping.yml
(it is a link, sits behind one, is not a plain file, or is not valid text).
Nothing was changed. Open it yourself, then run
`python scripts/check_model_selection.py`.
```

### R2.4 The check (replaces the row and scan sentences of Revision 1 Proposal §3)

* The bare row test is anchored: some scanned line matches `^ *(- +)?(\{ *)?tier *:`
  (a block row or a flow-style row). A `tier:` inside another value no longer counts.
* With PyYAML, the scan covers every value `safe_load` returns: strings, dict keys, set
  members, and bytes decoded as text. It visits each object once, keyed on identity.
* The checker and the engine keep their separate copies of the line rule; R2.6 pins them.

### R2.5 Family, not version (replaces the matching text in Revision 1 Proposal §1, §2, §5)

The Maintainer's direction, 2026-10-18, as recorded in commit `47b38074`:

> "Versions should not be named here, rather the latest version should be used"

It reaches every place a mapping is described. All texts are vendor-neutral and name no
real model. The stub's example block (the only stub change; the row and the trailing comments
stay byte-identical):

```
# Replace the placeholder row below with your real assignments. Name the model
# family, never a version: the latest release of that family is meant. Shape:
#
#   - tier: high
#     model: vendor-a/flagship-family
```

The capture's prompt becomes `<tier> tier -- model family, not a version (blank to skip):`, and
the header it writes gains the same one-line rule. The II-5 block:

```
**Model-selection mapping** (only if `model-selection` was installed)
- [ ] `python scripts/check_model_selection.py` exits 0. If not, ask the Maintainer which
      model family fills each tier (high, medium, low) and record one row per tier, naming
      the family and never a version; do not guess.
```

The fourth allowed match in II-5's vendor-neutrality block: "the filled tier-to-model mapping,
`dev/.cairn/model-selection-mapping.yml`, which is adopter configuration and may name model
families by design". The seed, in both presets:

```
* [seed; id: fill-model-selection-mapping]
  **Waiting on Maintainer**: fill the model mapping
  If `dev/.cairn/model-selection-mapping.yml` exists, ask the Maintainer which model
  family fills each tier (high, medium, low), record one row per tier (the family, never
  a version), and run `python scripts/check_model_selection.py`. Delete the Waiting line
  when it passes.
```

The module doc's new paragraph, in the byte-identical pair:

```
**Filling the mapping.** The adopter-local mapping is
`dev/.cairn/model-selection-mapping.yml`: one row per tier you populate (high, medium,
low), copying the shape of the seeded row. In `model`, name the model family, never a
version; the latest release of that family is meant, so a new release does not make a row
stale, and a release that changes which family fits a tier does. Say in `source` who made
the assignment. `python scripts/check_model_selection.py` exits 0 once no placeholder
remains and at least one row exists. It checks shape, not truth, and nothing reads
`date_verified`, so noticing a stale mapping is yours to do. The installing agent runs the
check at the acceptance step; after that a person does, because nothing runs it
automatically.
```

Its sentence "surfaced by an existing routine" (`dev/modules/model-selection.md:156-158`)
becomes: "Re-rank on a low-frequency housekeeping pass; the `date-verified` stamp lets a
reader see staleness, and no routine reads it."

### R2.6 Tests (adds to Revision 1 > Tests required)

* `TestNoticeOnEveryInstallPath` gains the **delivering apply**: a tree whose mapping is
  absent from disk and from the lockfile is planned (silent), staged (silent), then applied
  (the file appears and the notice prints); a refused apply prints none.
* `TestCaptureRefusesBeforeAskingAnything` calls `capture_model_selection_mapping` directly with a
  prompt that fails the test if called, for a linked file and a linked `dev/.cairn`; a second
  test runs a real install with `local-env.json` and the activation log already in place
  behind the link and asserts the capture's own constant refusal line and exit 2.
* `TestCaptureWritesByReplacing`: a hard link at the mapping path to an outside file holding
  `FILL ME` leaves the outside file byte-identical and the mapping a fresh single-link file; a
  prompt that swaps the mapping for a link while "answering" is refused at write time.
* `TestNoticeNeverOpensAnythingButARegularFile`: a named pipe at the path returns the second
  variant within a timeout. A non-text mapping leaves an interactive install running and
  prints the second variant.
* `TestEngineAndCheckerAgreeOnUnfilled` uses a **generated** corpus: every line lead (none,
  space, tab, no-break space, form feed, byte-order mark) times every break (`\r\n`, `\n`,
  `\r`, U+0085, U+2028, U+2029) times every position (comment, value, row). The engine and the
  bare checker agree exactly; the PyYAML checker is never looser than the bare one; and its
  extra strictness is exactly an explicit list: block scalar, folded plain and quoted values,
  line continuation, escapes such as `"FILL\x20ME"`, a repeated `mapping:` key, `!!binary` and
  `!!set`. A nested-alias document completes in a fixed time.
* A stub test: the example block says family, never a version, and names no real model; the
  placeholder row is intact (one row, five fields reading `FILL ME`).

S2 adds mutations, each owed to the plan: drop U+2028 from one copy's break set (parity red);
remove the second guard or swap `os.replace` for `write_text` (the swap and hard-link tests
red); skip `lstat` (the pipe test times out); drop the visited-set (the alias test times out).

### R2.7 Files (replaces the rows of Revision 1 Proposal §6 that it names)

| Revision 1 row | Revision 2 |
|---|---|
| `upgrade.py`: `cmd_upgrade` "after the `--to` check" | three calls, apply after success (R2.1) |
| `install.py`: capture | atomic write, early return paths, family prompt (R2.2, R2.5) |
| `test_security_leaf.py`: capture joins `_GUARDED_WRITE_FUNCS` | also `_write_stage`; and whatever the `seed_gitignore` repair added is kept |
| `SECURITY_MUTATIONS.md`: one row | the capture row, lines 12-13 corrected; the `seed_gitignore` rows belong to its repair |
| (not touched) `lockfile.py` | one comment-only edit at `:448-453`: the revisit trigger fired; keep the reuse, add the file-type check at the call site |
| (not touched) the stub | the example block only (R2.5); not frozen, not in the manifest |

Frozen set unchanged at six. AST count unchanged: 4 CHANGED, 2 NEW; a comment edit and a
data-file edit add none. The plan rebases on the `seed_gitignore` repair before it starts.

### Named residuals (replaces the list in Revision 1 > Named residuals)

* **Staleness:** nothing reads `date_verified` or the re-verification field.
* **A class, not a case, on the bare path and in the engine:** a value whose `FILL ME` is not
  spelled out on one non-comment line (a block scalar, a value folded over lines, a
  continuation, an escape) reads as filled, and so does a repeated `mapping:` key. The engine
  erring toward "filled" means it never overwrites and may stay quiet. With PyYAML installed the
  checker catches the class. Each needs a deliberate spelling by someone who could edit the
  checker anyway, so none carries authority.
* **A version gap:** an adopter's checker is whatever they last upgraded to, while the engine is
  current. Between `upgrade --plan` and `--apply`, a hand-filled file can be silent in the new
  engine and fail the old checker. The apply updates the verbatim checker and closes it.
* A `FILL ME` in a trailing comment fails; in a leading comment it passes. One tier filled
  passes, as the module doc allows. Invented but plausible names pass. A profile that removes the
  module from a moderate preset gets a Waiting row to delete.
* Non-interactive and interactive installs disagree on a bad mapping path (exit 0 with a notice,
  and exit 2). Neither writes anything.

### S4 and S5 deltas

**S4.** A hard link or a swapped link at write time: refused by the second guard, or harmless,
because the replace never writes into the old file. A named pipe: never opened. A non-text
file: left alone. **S5.** Added to what still wins: a value spelled across lines on the bare
path (named above) and a link swapped in the last instant before the replace, which narrows the
window to one rename but does not eliminate it; the threat model remains "no concurrent
filesystem attacker" (`bootstrap/SAFETY.md`). The hard-link case is closed by construction.

### Scope delta

**Scope delta**: degraded, unchanged from Revision 1: the one removal (the solo-greenfield
seed, **disposition**: wontfix) still needs your allowance (Question 2). Additions, not
removals: family wording, the stub example edit, the `upgrade` apply path, the `lockfile.py`
comment.

### Assurance path

**Assurance path**: high-assurance, unchanged.

### Withdrawn / superseded commitments

* **"The stub's bytes unchanged"** (Revision 1 > What changes for you, "Unchanged"): replaced
  by the example-block edit (R2.5); the row and trailing comments stay byte-identical.
* **One early `cmd_upgrade` call after the `--to` check:** replaced by three calls, the apply
  one after success (R2.1).
* **The capture "checks once, before the prompts" and writes with `write_text`:** replaced by
  an early guard, a second guard at write time and an atomic replace (R2.2).
* **"Like every other containment refusal" (Revision 1 > Proposal §4 and the Response):**
  withdrawn. `main` catches two refusals, and the table is corrected (R2.2).
* **"The helper never raises" as the whole of the notice's safety:** supplemented by a file-type
  check so it also never blocks (R2.3).
* **"Some scanned line holds a `tier:` key" (bare row test):** replaced by the anchored pattern.
* **"Every string in the parsed document" (PyYAML scan):** replaced by every value `safe_load`
  returns, visited once.
* **"The only surviving differential is a `#`-led line in a multi-line scalar":** replaced by the
  class in Named residuals.
* **"The PyYAML checker differs only on the named multi-line cases" (parity test):** replaced by
  a generated corpus and an explicit list.
* **"`lockfile.py` not touched":** one comment-only edit.

Nothing else in Revision 1 is withdrawn.

## Review -- Claude Opus 5.5 (Security Review, closure pass, fresh session) -- 2026-10-18

**Model**: Claude Opus 5.5, a fresh session with no shared context. It is the same agent
family as the author and both earlier reviewers, so this pass has no cross-type distance.
Probes ran in a scratch folder outside this tree, with Python 3.13.13 and PyYAML 6.0.3 on
macOS.

```
Reviewed commit: 5656e04c0786cb3aa95073eea2bd48d4e5b0e61e
Target: the Response to the Security Review and Revision 2, read against the code at 58f30d6cc8d531b30c87e39e883228ee0e657d27 (upgrade.py and security.py unchanged since 5656e04c; the seed_gitignore repair, b8a402c6, landed in between)
Prior findings: SEC-1 to SEC-8 (the Security Review at 3c133398)
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: raised (0 blocking, 4 non-blocking, all owed to the plan)
**Verdict**: ACCEPT

**The Security Review obligation is cleared.** SEC-1 and SEC-2, the two blocking findings,
are closed. SEC-3 to SEC-8 are carried into the plan as requirements. The plan's
`required(Internal + Internal Security Review)` pass checks them, together with CL-1 to CL-4
below.

**In plain terms.** The two things that blocked are fixed. The `.gitignore` hole was repaired
in its own commit, and this proposal waits for that repair. The upgrade notice now speaks
only after an upgrade has finished, and stays silent when one is refused. Revision 2 opened
one new gap, in its recipe for the safer write. If the temporary file has a fixed name, a link
already waiting at that name sends the write outside the project. The fix is one standard
library call, and the plan must use it (CL-1). The other three findings are smaller
corrections the plan must carry.

### SEC-1 -- closed: the dependency is stated, and the repair has landed

* Revision 2 binds the plan to start only after the repair. R2.7 says "The plan rebases on
  the `seed_gitignore` repair before it starts", and the Declarations repeat it. Revision 2
  makes no containment claim about `seed_gitignore` and leaves its inventory rows to the
  repair. That is enough: a plan that started without the repair would be a deviation from
  the accepted contract.
* The repair is now commit `b8a402c6`. At HEAD, `seed_gitignore` is in `_GUARDED_WRITE_FUNCS`
  (`bootstrap/tests/test_security_leaf.py:48`) and has a Class A row
  (`bootstrap/_scaffold/SECURITY_MUTATIONS.md:40`). I did not review that commit; it has its
  own reviews. The plan's entry check is those two facts, not the phrase "the repair".
* The repair changed two facts that Revision 2 states (CL-2).

### SEC-2 -- closed: the notice fires only after an action finishes

Checked against `cmd_upgrade` (`bootstrap/_scaffold/upgrade.py:2287`):

* **`--apply`.** `_apply_upgrade` has one `return 0` (`upgrade.py:2230`). It comes after the
  files, the base cache and the lockfile are written and the stage is removed. Every refusal
  before it returns 1 (leftover conflict markers among them, `:2026`) or raises
  `ScaffoldSecurityError`, which `cmd_upgrade` turns into exit 2 (`:2477`). A refusal part-way
  through the swap also raises. So "print when `rc == 0`" never fires on a refused or
  half-done apply. Keep the existing `try`/`except` around the call and put the notice after
  it, so a notice can never be reported as an apply refusal.
* **`--stage`.** The token preflight (exit 2) and the stage containment refusal (`:2496`) both
  return before the report (`:2499`). Nothing after the report can refuse.
* **`--plan`.** Nothing after its report (`:2525`) can refuse.
* **`--adopt-module`.** Its adopt line prints only after the lockfile commit and the
  `.gitignore` seed succeed (`upgrade.py:1605-1612`).
* **One quiet case, acceptable.** If a step after the lockfile write refuses (the `.gitignore`
  seed for a newly added skill), the apply has delivered the file but exits 2, so the notice
  is skipped. The next `upgrade --plan` prints it.
* **Fixed text.** Both variants in R2.3 are constants. The only path they print is a fixed
  relative path, never one read from the tree.

### What Revision 2 carries for SEC-3 to SEC-8

| Finding | Where it lands | State |
|---|---|---|
| SEC-3 | R2.2 step 4, `TestCaptureWritesByReplacing`, S5 | captured; the temp file needs CL-1 |
| SEC-4 | R2.2 exit-code story, R2.6 direct-call and real-install tests, Named residuals | captured; the exit-code facts need CL-2 |
| SEC-5 | R2.4, Named residuals | captured; the row check needs CL-4 |
| SEC-6 | R2.2 steps 1 and 3, R2.3 `lstat` | captured; the missing file needs CL-3 |
| SEC-7 | the generated corpus, the S2 mutations, the version-gap residual | captured; see CL-4 |
| SEC-8 | R2.7 `lockfile.py` comment, `_write_stage` entry | captured |

* **The value scan.** Visiting each object once holds up. A 22-level nested-alias document
  loaded in 3.5 ms. Walked with the visited set it took 48 visits; without it, 25.2 million
  visits and 8.1 s (I count strings too, so my figure is above the author's 16.7 million). A
  document whose alias contains itself also loads, and the visited set ends that walk in 4
  visits.
* **The named-pipe check.** `lstat` before any open is right, and the capture's `is_file()`
  comes before its read. See CL-3 for the missing file.
* **The stub edit.** The one-time conflict fails closed: `--apply` refuses while a staged file
  holds conflict markers (`upgrade.py:2026`). That adopter's upgrade waits until they resolve
  it, and a half-merged mapping is never written. The stub is not in the gate manifest's frozen
  set. `scaffold.py --manifest` lists it by path and merge mode only, so the edit changes no
  published-manifest byte; R2.7's "not in the manifest" should read "not byte-pinned by it".
* **Vendor-neutrality: clean.** I ran the II-5 pattern, the neutrality gate's denylist and
  model-family words over the 44 shipped lines quoted in R2.3 and R2.5: both notices, the stub
  block, the prompt, the II-5 block, the fourth allowed match, the seed, the module paragraph
  and its replacement sentence. No match. As a control, the same pattern matched this
  proposal's earlier Security Review header.

### Findings

#### CL-1 -- non-blocking, owed to the plan: the temporary file must be created fresh, never at a fixed name

**Plain:** the safer write goes through a temporary file, and a file or link already waiting
at that file's name can send the write outside the project.

* R2.2 step 4 says "write a temporary file beside the mapping; guard that file too". It does
  not say how the file is made.
* Exercised with the engine's own `_assert_safe_write`. A hard link at
  `model-selection-mapping.yml.tmp`, pointing at an outside file, passes the guard. Writing the
  temp file then overwrote the outside file, and the later `os.replace` does not undo that. A
  symbolic link at that name is refused if the guard runs first. If the guard runs after the
  write, as step 4's order reads, the outside file is overwritten before the refusal. A
  checkout can carry that link.
* This is worse than the defect it replaces. The original write-through needed the outside file
  to hold `FILL ME`; a temp-file write has no such precondition.
* The model `_commit_lock_and_caches` (`upgrade.py:1328`) uses a fixed `.tmp` name with the
  guard before the write. That recipe still has the hard-link gap.
* **Requirement:** after the second guard, create the temp file with
  `tempfile.mkstemp(dir=<the mapping's folder>)`, or `os.open` with `O_CREAT | O_EXCL`.
  Exclusive creation refuses anything already at the name; I confirmed it with a hard link and
  with a symbolic link. With it, S5's "The hard-link case is closed by construction" is true.
  Test: plant a hard link and a symbolic link at the `.tmp` sibling name; both outside files
  stay byte-identical. S2 mutation: swap exclusive creation for `write_text` on a fixed `.tmp`
  name, and the test goes red.

#### CL-2 -- non-blocking, owed to the plan: the landed repair made two of Revision 2's exit-code statements false

**Plain:** the repair added one catch-all for refusals at the top of the installer, so a
sentence Revision 2 tells the plan to write into the security inventory would now be wrong.

* R2.2 says a linked `dev/.cairn` stops "with a traceback and exit 1", and that
  `SECURITY_MUTATIONS.md:12-13` is to be corrected to say `main` catches two refusals. At HEAD,
  `main` (`bootstrap/_scaffold/cli.py:189`) wraps the whole CLI in one `ScaffoldSecurityError`
  catch that returns 2. Exercised: a non-interactive collaborative-team install with
  `dev/.cairn` linked outside the tree now exits 2 with no traceback, and nothing outside is
  written. Lines 12-13 are true as they stand.
* **Requirement:** the plan re-derives the exit-code story against HEAD and does not apply
  R2.2's correction to lines 12-13. Keep the capture's own catch with its constant line. The
  top-level handler prints the exception text, which carries the link target the tree chose,
  so the capture must not fall through to it (SEC-4).
* The capture's call site moved from `main` to the new `_run_cli` (`cli.py:205`, the call at
  `:673`). The AST ceremony derives its own count, so only the symbol name in Revision 1's
  files table changes.

#### CL-3 -- non-blocking, owed to the plan: a missing mapping must stay silent

**Plain:** read literally, the new helper would tell every project without this module that it
"could not read" a file it never had.

* R2.3 sends "anything other than a regular file" and "an `OSError`" to the "could not read"
  variant. A missing file is both: `lstat` raises `FileNotFoundError`, which is an `OSError`.
  R2.1 and R2.6 depend on a missing file being silent, and Revision 1 said so before R2.3
  replaced the helper text.
* **Requirement:** the plan states the order: no entry at the path returns `[]`, first. A
  dangling link is not missing, and gets the second variant. Test: an install without the
  module prints neither variant.
* Wording: after a successful `--apply`, "Nothing was changed" reads as if the upgrade changed
  nothing. "That file was not changed" says what is meant.

#### CL-4 -- non-blocking, owed to the plan: the YAML row check is looser than the plain one for two spellings

**Plain:** two valid ways of writing a row are seen by the YAML reader and missed by the plain
line check, so the test's claim that the YAML path is "never looser" is not true.

* Exercised: a quoted key (`- "tier": high`) and a one-line list
  (`mapping: [{tier: high, model: x}]`) fail R2.4's anchored pattern, while PyYAML reads a
  non-empty list. The generated corpus (line lead, line break, position) contains neither. So
  R2.6's "the PyYAML checker is never looser than the bare one" passes only because the corpus
  leaves them out, which is the fitting SEC-7 warned against.
* In the engine these files read as unfilled. The notice wrongly calls the mapping unfilled,
  and an interactive re-install asks again. It writes only if the person types an answer, so no
  authority is at stake.
* **Requirement:** add both spellings to the corpus. Then either widen the pattern to accept
  them, or name them in Named residuals and assert the reverse direction for them.

### What I did not do

I ran no suite and no test node. I did not review the `seed_gitignore` repair (`b8a402c6`). I
did not re-run the earlier rounds' probes or the author's three-way merge measurements for the
stub edit. Probes ran in a scratch folder on macOS. Nothing in this tree was written except
this section and the status line.
