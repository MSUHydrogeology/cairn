# The model mapping gets filled on every install path, and something checks it

**Author**: Claude (Strategy)
**Status**: awaiting-review
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
