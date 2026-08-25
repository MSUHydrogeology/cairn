# Plan: adopting a module into an existing tree

**Source proposal**: `dev/proposals/archive/2026-08-20-claude-adopt-into-existing-tree.md`
(accepted Revision 2, 2026-08-20)
**Status**: ready-to-implement
**Plan review**: required(**Internal**) — as the accepted Revision 2 declares.
No `Plan readiness` inheritance is claimed; the External pass withheld it, and
under the rule that landed 2026-08-24 no External plan tier exists to claim.
**Security Review**: **REQUIRED**, surface-based (`AGENTS.md` > High-risk
surfaces, the scaffold / merge engine). D1 adds profile parsing and YAML loading
inside `bootstrap/_scaffold/`, where the parsed result gates a fail-closed
refusal and then a lockfile write. The trigger is the surface; whether a
boundary moved is a different question and does not discharge it.

**It attaches to the implementation, not to this plan's design review** — the
accepted Revision 2 declares the two separately, and its Decision says
*"Implementation carries a Security Review REQUIRED trigger."* An earlier draft
of this header also claimed
`required(Internal + Internal Security Review)`, which would have been a
**plan-review** obligation blocking the design read on a security pass the
change had not yet produced. That is the identical overclaim a plan reviewer
blocked on `convergent-lifecycle` Chunk E a day earlier — a plan-review token
carrying a code-stage obligation — and it is corrected here rather than
rediscovered. The obligation is real and unchanged; only its stage is.
**Last update**: 2026-08-25
**Opened**: 2026-08-25

## Why

Two adopter-filed issues, [#5](https://github.com/MSUHydrogeology/cairn-scientist-ai-teams/issues/5)
and [#7](https://github.com/MSUHydrogeology/cairn-scientist-ai-teams/issues/7).
`--adopt-module` can refuse on a token the adopter has already filled in, and
can silently keep a differing destination file without saying so.

**This plan is deliberately first, and deliberately small.** The strategy note
that authorizes the concurrent subtraction sweep also says a bug fix with a
failing-test reproduction is *"code + test + one code review, full stop"*, and
that adopter-filed bugs are **"fixed and shipped within two sessions."** Folding
this into the sweep would put an adopter's bug behind the largest change in this
repository's history. It shares no file with the sweep and is blocked by
nothing.

## What

Three changes, exactly as Revision 2 accepted them.

| id | change | surface |
|---|---|---|
| **D1** | Profile as seed, lockfile as authority. `_cmd_adopt_module` resolves required tokens from profile ∪ lockfile (lockfile wins), applies a strict placeholder predicate and `_refuse_secret_tokens` **before** the spec loop writes anything, and persists newly-resolved values in the existing atomic `_commit_lock_and_caches`. | `bootstrap/_scaffold/upgrade.py` |
| **D2** | Advisory on both quiet branches, comparing on-disk bytes against **what this spec would install** — `theirs_b` verbatim, substituted for mergeable. Reports kept-and-differing (`else`) and skipped-and-untracked (`continue`), reconciles the `recorded N file(s)` count. Advisory only: never blocks, never overwrites. | `bootstrap/_scaffold/upgrade.py` |
| **D3** | Drop the obsolete `--include-archive` recommendation. **See "The D3 collision" below — this one cannot be implemented as written.** | `bootstrap/UPGRADE.md` |

## Approach

**The order of operations in D1 is the change**, not a detail:

```
1. resolve **the currently-adopting module's required tokens** (profile ∪
   lockfile, lockfile wins) — not the whole profile map, and **merged into**
   the existing lockfile token map, never assigned over it
2. strict placeholder predicate            -> refuse
3. _refuse_secret_tokens(candidate map)    -> refuse
4. ONLY THEN the spec loop (which writes destination files)
5. _commit_lock_and_caches
```

Steps 2 and 3 sit **before** step 4. A guard at step 5 refuses after the loop has
already written files, violating invariant (i). Revision 1 said the write "routes
through" the guard and never fixed its position; that was the gap the External
review found.

**The strict predicate lives in the adopt path, not in a reused helper.** A
required token is unfilled when absent, blank, `{{...}}` (`_UNFILLED_TOKEN_VALUE`,
`config.py:1284`), **or** `<...>`. The angle-bracket form is what the profile
template `_cmd_init_lock` writes actually contains, and its guard at
`upgrade.py:1158-1160` is **not** in `_resolve_lock_profile_fields` — so "reuse
the helper" would hand this plan the narrower predicate by construction and
reintroduce the bug for the exact shape the adopter hit.

**Three fallback dispositions, one of which changes.** Absent profile → silent
(an absent optional file is not an anomaly). Unparseable → warn, unchanged.
**Incomplete or invalid → warn, then fall back** — a behaviour change, because
silence hides from the adopter that their committed edit had no effect.

### The D3 collision — and why it is a design question, not a typo

Revision 2 says `bootstrap/UPGRADE.md:255` becomes
`python tools/lifecycle_planner.py scan`.

**That tool is on the subtraction sweep's removal list** — build table order 5,
*"Lifecycle CLI + planner (+ twins, tests) | remove"*. And the sweep's
constitution rewrite carries the falsifier **"no governing document references a
tool this sweep removes."** Implementing D3 as accepted would write, into a
governing document, a reference the very next accepted proposal must delete.

Three options, and none is free:

1. **As accepted** — write `lifecycle_planner.py scan`, and the sweep changes the
   same line again. Honest, cheap, and leaves a known-dead reference in an
   adopter-facing document for however long the sweep takes.
2. **Point at the replacement** — the sweep's order-3 rows create a ~100-line
   standalone board view. It does not exist yet, so this would document a command
   an adopter cannot run today. Worse than option 1.
3. **Drop the recommendation without replacing it** — delete the obsolete flag and
   the sentence recommending the command, leaving the surrounding prose intact.

**Recommended: option 3**, and it is the one consistent with the philosophy the
Maintainer asked for. D3's accepted purpose is *"drop the obsolete
`--include-archives` recommendation"* — the subtraction is the change. Naming a
successor command was Revision 2's way of not leaving a gap; the sweep is about
to prove the gap was never load-bearing. Option 3 removes a line instead of
rewriting it twice.

**The replacement text, written out — because "leave the surrounding prose
intact" does not hold here.** The passage is a two-item numbered list under the
lead-in *"Two consequences:"*. Deleting item 1 makes that lead-in false, orphans
the *"It is read-only"* sentence whose antecedent is the command being removed,
and leaves a one-item list. The fold is to flowing prose.
`bootstrap/UPGRADE.md:251-267` becomes, in full:

> **What that means for your tree.** Cairn's manifest enumerates *Cairn's* old
> records, not yours, so **every** review-required plan in your tree is judged
> by the full schema from the moment you upgrade. The consequence: a plan
> already past `open` whose review predates the schema will be reported.
> Append-only forbids editing that landed review, so the repair is a **new**
> conforming pass appended to the plan (a re-read, by whoever performs it, with
> the two attestation lines) — not a rewrite of the old one. If instead you want
> your own pre-existing records enumerated the way Cairn's are, that is a code
> change to a committed constant in your installed checker, and it shows up as a
> code diff in review; it is deliberately not something a plan file can ask for.

Nothing but the command recommendation is lost: the numbered list, the "Two
consequences" lead-in and the orphaned sentence all go, and item 2's substance
survives verbatim as the body. Confirmed no other line in the tree anchors to
this passage by name.

**This is a deviation from an accepted term and needs the Maintainer's
allowance.** Recorded here rather than taken: the plan-review reviewer should
say whether the reasoning holds, and the Decision on this plan's disposition
grants or refuses it. If refused, option 1 is the fallback and costs one line of
sweep work later.

## Verification

**Boundary A (iteration, scoped).** `bootstrap/tests/test_upgrade.py`,
`bootstrap/tests/test_upgrade_module.py`,
`bootstrap/tests/test_module_merge_lockfile.py`,
`bootstrap/tests/test_profile_grammar.py`. `--adopt-module` is exercised through
its **real CLI entry point**, and the secret-token refusal through the CLI, not
by a direct helper call.

**`test_upgrade.py` is the load-bearing one and is named first on purpose.**
`class TestAdoptModule` (`test_upgrade.py:1133-1203`) is the only pre-existing
CLI-level regression suite for the command this plan changes — four tests
driven through `s.main([..., "--adopt-module", ...])`, including
`test_adopt_records_on_disk_content_not_template`, which is precisely D2's
already-on-disk-and-customized scenario. New CLI-level tests belong here.
They do **not** belong in `test_upgrade_module.py`, whose stated contract is
Stage-7 import layering and single-identity-across-facades, and which has no
behavioural adopt-module coverage at all; `test_module_merge_lockfile.py`
covers an unrelated `install_core` defect and is retained only as a
neighbouring-surface check.

**Boundary B mode: `full`.** Not a choice — `bootstrap/_scaffold/upgrade.py` is
the scaffold/merge engine, a named high-risk surface, and the change touches the
install contract's `--adopt-module` write path. `AGENTS.md` refuses bounded mode
on either condition.

**The five S2 mutations, each required red:**

| mutation | must redden |
|---|---|
| delete the persist call | "token lands in the lockfile" |
| make the placeholder predicate curly-brace-only | the `<my package>` regression |
| move `_refuse_secret_tokens` back to just before `_commit_lock_and_caches` | the no-destination-written assertion |
| make the byte comparison always-equal | the advisory-fires test |
| make the byte comparison always-unequal | the paired advisory-absent test on identical bytes |

The last two are a **pair on purpose**: without both, the check cannot
distinguish a correct comparison from one that always fires. And the
secret-token test **arranges its own known required token** rather than deriving
an expectation from the live `KNOWN_TOKENS` — a test that reads its expectation
from the thing it checks cannot fail, which this repository shipped eight times
in one file yesterday before a Security Review measured it.

**Edge cases, each its own case**: no `profile.yml`; token absent; token present
but an unfilled placeholder **in either form**; token in both sources disagreeing
(lockfile wins); destination missing; destination byte-identical after
substitution; destination differing; destination skipped at `continue`; a path
that is both a spec destination and a declared superseded surface
(the architecture-review document is both, per its `config.py` spec and
`_superseded_surface_note` must not both fire about it in one run); module
already in the roster.

**Confirm the instrument before trusting an absence.** D2's comparison is
against `substitute_tokens(theirs_b...)`, not raw `theirs_b` — comparing against
raw would fire on every mergeable spec carrying a token, and `claim-check.md`,
`lifecycle-metrics.md` and `architecture_review_template.md` all do. The
motivating example cannot settle this: `run_security_audit.py` is
`verbatim=True`, so raw and installed are identical for it.

## Risk

**C0 answer: yes.** This writes into an adopter's tree through the install
contract, and a wrong guard either refuses a legitimate adopt or lets a
placeholder into a lockfile. Both reach someone who is not in this conversation.

That is why the Security Review is declared and why Boundary B is `full`. It is
also why the guard **moves earlier** rather than gaining a second guard later:
the subtraction philosophy applies to safety machinery too — one check in the
right place beats two in the wrong one.

**Additions kept minimal, deliberately.** The Maintainer's constraint was that
any addition be consistent with the removal philosophy. What this plan adds is
one predicate, one reordering, and one advisory — no new module, no new
registry row, no new tool, no new lifecycle vocabulary, and nothing the
subtraction sweep would then have to remove. D3 is where that constraint bites,
and the recommendation above resolves it by removing a line rather than adding a
command.

**Known dependency.** None. This plan shares no file with the subtraction sweep
and is blocked by nothing.


## Maintainer allowance -- D3 drops the recommendation -- 2026-08-25

**Option 3 is allowed.** Authorization, quoted verbatim and visually isolated:

> "Drop the recommendation"

**What this permits.** D3 removes the obsolete `--include-archive`
recommendation from `bootstrap/UPGRADE.md` **without naming a successor
command**, leaving the surrounding prose intact. The accepted Revision 2 text
had that line become `python tools/lifecycle_planner.py scan`.

**Why it is a deviation, stated plainly.** Revision 2 is an accepted contract
and it names a specific replacement string. Removing rather than replacing is a
different outcome, however small, and accepted scope is a floor. The allowance
is what makes it legitimate; the reasoning is what makes it right.

**The reasoning.** `tools/lifecycle_planner.py` is on the subtraction sweep's
removal list (build table order 5, basis `570fedb`), and that sweep's
constitution rewrite carries the falsifier *"no governing document references a
tool this sweep removes."* Implementing D3 as written would put a reference into
an adopter-facing document that the next accepted proposal must delete —
rewriting one line twice, and shipping a dead command in between.

**Scope delta: preserved.** D3's accepted purpose is to *drop the obsolete
recommendation*; the subtraction is the change. Naming a successor was
Revision 2 avoiding a gap, and the sweep is about to demonstrate the gap was
never load-bearing. Nothing the accepted contract set out to achieve is lost.

**What the plan reviewer should check anyway**: that the surrounding prose still
reads correctly with the sentence gone, and that no other line in
`bootstrap/UPGRADE.md` depends on the removed one. A removal that leaves a
dangling "as described above" is worse than the flag it deleted.

## Plan review -- Claude Sonnet 5 (Internal, fresh context) -- 2026-08-25

Reviewed commit: 86e49a34d2c2646d094620d5f5448ab7bbd48491
Target: the complete plan -- Why, What (D1-D3), Approach (including "The D3
collision" subsection), Verification (Boundary A/B, the five S2 mutations,
edge cases), Risk, and the "Maintainer allowance -- D3 drops the
recommendation" section
Prior findings: none
Assurance path: high-assurance (the source proposal's declared path; D1/D2
write into the install contract, D1 is a scaffold/merge-engine surface)

**Tier**: Internal
**Model**: Claude Sonnet 5
**Findings**: raised -- 4 notes, all non-blocking
**Verdict**: No blocking findings. Every load-bearing design claim I
re-measured against the real code held: the D1 step-ordering fix, the
strict-predicate/helper-scope claim, D2's substituted-bytes comparison
target, the three-row fallback-disposition table, and the D3 collision's
factual basis (the `570fedb` build-table row, the subtraction sweep's own
quoted falsifier) all confirmed exactly as stated. The four notes below are
citation drift and prose-precision issues, each cheap to close and each
backstopped by Boundary B's mandatory full run before anything ships --
none of them let a wrong implementation pass silently.

### Steelman

* **D1's step ordering is real and matches the code it changes.**
  `_cmd_adopt_module` (`upgrade.py:1358-1452`) today reads tokens from the
  lockfile only (`:1387`), preflights `missing_required_tokens` before the
  spec loop (`:1393-1402`, already correctly ordered), then the loop
  (`:1408-1440`) writes destination files via `dst_abs.write_text` at `:1427`
  before `_commit_lock_and_caches` at `:1444`. `_refuse_secret_tokens` is
  **not called anywhere in `upgrade.py` today** (confirmed by
  `grep -rn _refuse_secret_tokens bootstrap/_scaffold/` -- its one production
  caller is `install.py:1667`), so the plan's step 3 is a new call site being
  wired in, not a call being repositioned -- and the plan's diagram places it
  correctly, before step 4's loop.
* **The strict-predicate placement claim is correct on both halves I was
  asked to check.** `_resolve_lock_profile_fields` (`upgrade.py:1064-1084`)
  builds its token map with `if isinstance(k, str) and k in KNOWN_TOKENS and
  v` -- no angle-bracket test anywhere in the function. `_cmd_init_lock`'s
  actual guard is `placeholder_tokens = sorted(k for k, v in tokens.items()
  if v.strip().startswith("<") and v.strip().endswith(">"))`, and the profile
  template it writes (`_INIT_LOCK_TOKEN_PLACEHOLDERS` /
  `_AXIS_PLACEHOLDERS`, `upgrade.py:1054-1061`) genuinely contains values
  like `"<your project name>"` and `"<small|medium|large>"`. So "the helper
  would hand the plan the narrower predicate by construction" is true, and
  "the strict check lives in the adopt path itself" is the right call --
  reused, the helper really would silently readmit the `<my package>`
  regression. (The plan's specific line pin for this guard is off; see
  Note 1.)
* **D2's substitution claim is not asserted, it is measured.**
  `claim-check.md`, `lifecycle-metrics.md` and `architecture_review_template.md`
  are declared without `verbatim=True` in `_MODULE_MAPPINGS`
  (`config.py:739-785`, `:1144-1145`; `InstallSpec.verbatim` defaults to
  `False` at `config.py:664`), and each raw template genuinely carries a
  `{{...}}` token (`{{claim_check_command}}`, `{{metrics_command}}`,
  `{{project_name}}` -- confirmed by direct grep of the shipped templates).
  `run_security_audit.py` is confirmed `verbatim=True`
  (`config.py:1043-1044`), so the motivating example really can't
  distinguish raw-vs-substituted comparison, exactly as the plan says.
  Comparing against raw `theirs_b` would genuinely fire on every one of
  those three mergeable specs on a clean install.
* **The fallback-disposition table matches `_resolve_current_profile` as it
  reads today.** Absent profile (`upgrade.py:235-236`) returns silently;
  the parse-exception branch (`:237-253`) warns; the incomplete/invalid
  branch (`missing or invalid or not axes`, `:255-259`) returns
  **silently** today -- so the plan's "chosen: warn, then fall back" for
  that row is correctly identified as the one behaviour change, not a
  restatement of existing behaviour.
* **The D3 collision's factual basis is real, not asserted.** `570fedb`
  resolves to a real commit (`Build table complete: the three open calls
  decided (Maintainer, 2026-08-25)`); its build table does carry `Lifecycle
  CLI + planner (+ twins, tests) | remove` at
  `dev/strategy/2026-08-21-claude-nimbleness-recovery.md:853`; and the
  quoted falsifier `"no governing document references a tool this sweep
  removes"` appears verbatim in `dev/proposals/2026-08-25-claude-
  subtraction-sweep.md:56` and `:309`. The Maintainer allowance quotes
  `"Drop the recommendation"` standalone and visually isolated, as the rule
  requires.
* **The five S2 mutations are sound and none is satisfiable by a circular
  test.** Walking each: (1) delete-the-persist and (2) curly-brace-only
  both have fixture-determined expectations independent of the code under
  test. (3) is the exact shape of the External reviewer's own [A2] finding
  (guard-not-really-wired-before-writes), reproduced correctly. (4)/(5),
  the always-equal/always-unequal pair, is the minimum needed to pin a
  boolean comparison -- one alone cannot distinguish "correct" from
  "trivially satisfies this one test." And `KNOWN_TOKENS`
  (`config.py:63-73`: `project_name`, `test_command`,
  `claim_check_command`, `metrics_command`, `python_package`) genuinely
  contains no name matching `_SECRET_TOKEN_RE`
  (`password|passwd|secret|credential|token|key`), so the plan's "the
  secret-token test must **arrange** its own known required token" is not
  optional caution -- there is no real required token today that would
  exercise that refusal branch, and `_MODULE_REQUIRED_TOKENS`
  (`config.py:1268`) is a plain module-level dict a test can patch to
  arrange one.

### Findings

**Note 1 -- the D1 predicate's line citation points at the wrong lines,
though the claim it supports is correct.** The plan (and Revision 2 before
it) cites `upgrade.py:1146-1148` for `_cmd_init_lock`'s angle-bracket guard.
Those lines are actually `if not profile_path.is_file(): return
_write_init_lock_profile_template(target)` / `try:` -- the "no committed
profile" branch, not the placeholder check. The real guard is
`placeholder_tokens = sorted(...)` at `upgrade.py:1158-1160`. The
`:1058-1061` citation for the placeholder template is correct as given. Not
blocking: I independently re-derived the same conclusion (helper lacks the
guard; template does write `<...>`) straight from the code, so the design
is right even though this particular pointer is stale -- but it is
inherited into a plan an implementer will read literally, and a 12-line
drift is enough to send someone looking at the wrong branch. Worth a
one-line fix before implementation.

**Note 2 -- "leaving the surrounding prose intact" (D3, option 3) is not
literally true against the actual `UPGRADE.md` text, and the plan does not
yet say what the corrected paragraph reads.** The live text
(`bootstrap/UPGRADE.md:251-267`) is:

> **What that means for your tree.** ... **every** review-required plan in
> your tree is judged by the full schema from the moment you upgrade. Two
> consequences:
>
> 1. Run `python tools/lifecycle_planner.py scan --include-archive`
>    **before** you rely on the upgraded gate. It is read-only; it reports
>    each non-conforming record, and when the problem is a heading that did
>    not count as a pass it quotes that heading back to you rather than
>    leaving you to guess which of the near-miss shapes you hit.
> 2. A plan already past `open` whose review predates the schema will be
>    reported. ...

Deleting item 1's recommending sentence leaves "Two consequences:" false --
there is now one -- and the numbered list needs renumbering either way.
If item 1's *second* sentence ("It is read-only; it reports each
non-conforming record...") survives the cut, "It" loses its antecedent,
since the sentence naming the command is what "It" refers back to. I ran
this exact check the allowance section itself asks for ("does the
surrounding prose ... still read correctly with that sentence gone") and
the literal answer is no -- not without also rewriting the lead-in
("Two consequences:" -> "One consequence:" or folding to flowing prose)
and either dropping or re-anchoring the "It is read-only" sentence. I found
no other file or line depending on this passage (`grep -rn "Two
consequences|consequences" bootstrap/UPGRADE.md` finds only this one
occurrence; nothing anchors to it by name elsewhere in the tree). Not
blocking under the C0 test -- this is a doc-legibility defect in Cairn's
own `UPGRADE.md`, trivially correctable in the same commit, not damage
reaching an adopter's tree -- but per the plan's own words, "worse than the
flag it deleted" is exactly what shipping the naive deletion would produce,
so the plan should carry the actual replacement text (or an explicit
instruction to fold to prose) rather than "delete X, leave the rest," which
this passage's shape does not support as written.

**Note 3 -- the Boundary A / "Public paths -> tests" file list (inherited
from Revision 2) misidentifies where `--adopt-module`'s real-CLI-entry-point
tests live.** I read all three cited files:

* `bootstrap/tests/test_upgrade_module.py` -- its own docstring says
  "Stage 7 -- the extracted upgrade subsystem," and its four tests check
  import direction, single-identity-across-facades, and that CLI entry
  points stay out of the module. `_cmd_adopt_module` appears once, inside a
  tuple of names checked for object identity (`:70`) -- there is no
  behavioral or CLI-level adopt-module coverage in this file today.
* `bootstrap/tests/test_module_merge_lockfile.py` -- its docstring is about
  a different defect entirely (`run_module_merge_pass` /
  `write_install_lockfile` divergence during `install_core`). `grep -c
  "adopt"` returns 0 real hits (the only "adopt" substrings are inside the
  word "adopter").
* The actual CLI-level `--adopt-module` regression suite --
  `class TestAdoptModule`, four tests exercised through the real
  `s.main([..., "--adopt-module", ...])` entry point, including
  `test_adopt_records_on_disk_content_not_template` (the exact
  already-on-disk-and-customized scenario D2 is about) -- lives in
  `bootstrap/tests/test_upgrade.py:1133-1203`, which appears in **none** of
  the plan's Boundary A command or its "Public paths -> tests" mapping.
  `test_profile_grammar.py`'s citation, by contrast, is accurate: it
  already contains `TestResolveCurrentProfileIsAudible`
  (`:79-155`), pinning exactly the fallback-disposition behavior the plan
  changes.

Not blocking: Boundary B is already pinned `full` (not a choice, per the
plan's own Risk section), so `python -m pytest bootstrap/tests` runs
`test_upgrade.py` regardless of this citation, and nothing here lets a
regression ship silently. But as written, an implementer following
Boundary A's scoped command literally would iterate without ever running
the four pre-existing tests for the exact command being changed, and new
CLI-level tests risk landing in a file whose own stated contract
(Stage-7 layering) doesn't fit them. Worth naming `test_upgrade.py`
(`TestAdoptModule`) explicitly in both the Boundary A command and the
public-paths mapping before implementation starts.

**Note 4 -- the Approach section's step 1 is looser than the "What" table's
scoping, and a careless read could widen it.** The "What" table (D1 row)
says "resolves required tokens from profile ∪ lockfile ... persists
newly-resolved values" -- correctly scoped to the adopting module's
required tokens, and to values that are new. The Approach diagram's step 1
just says "resolve the candidate token map (profile ∪ lockfile, lockfile
wins)," with no scoping word. `_resolve_lock_profile_fields` returns
**every** `KNOWN_TOKENS` entry present in `profile.yml`, not just the
tokens the module being adopted requires -- so a literal read of the
Approach diagram alone could lead an implementer to merge the *entire*
profile token map into `lock["tokens"]`, and to do it by assignment
(`lock["tokens"] = candidate_map`) rather than update, which would also
silently drop any previously-tracked token not present in this profile
read. Both would still likely be caught by adjacent tests (existing specs'
token substitution depends on tokens like `project_name` surviving), so
this is not blocking, but the two sections should say the same thing in
the same words -- "the currently-adopting module's required tokens,
merged into the existing lockfile token map" -- rather than leaving the
tighter scope to be inferred from a different section.

<!-- claim-check-allow: dev/architecture_review.md -->

### Coverage

**Exercised** -- direct reads of `_cmd_adopt_module`
(`upgrade.py:1358-1452`), `_resolve_lock_profile_fields` (`:1064-1084`),
`_cmd_init_lock` (`:1128-1170`), `_resolve_current_profile` (`:216-260`),
`_commit_lock_and_caches` (`:1275-1334`), `_superseded_surface_note`
(`:1337-1355`); `_refuse_secret_tokens` / `_SECRET_TOKEN_RE`
(`lockfile.py:121-259`) and its one production caller
(`install.py:1667`); `KNOWN_TOKENS` / `_MODULE_REQUIRED_TOKENS` /
`missing_required_tokens` / `_UNFILLED_TOKEN_VALUE`
(`config.py:63-73`, `:1268`, `:1282-1327`) -- confirmed
`missing_required_tokens` also lacks an angle-bracket test, a third
location (besides `_resolve_lock_profile_fields`) with the narrower
predicate; `_MODULE_MAPPINGS` entries and raw template bytes for
`claim-check`, `lifecycle-metrics`, `architecture-review` and
`python-security` (`config.py:737-1146`, plus the four template files
directly); confirmed `dev/architecture_review.md` is simultaneously a spec
destination (`config.py:1144-1145`) and a declared superseded surface for
the same module name (`config.py:1209`), matching the plan's named edge
case. Read Revision 2 in full (the operative contract) plus the Internal
and External review rounds and both Responses that produced it, to confirm
the plan's inherited claims (fallback table, D2 branch coverage, S1-S5)
against their own history rather than against the plan's restatement
alone. Read `bootstrap/UPGRADE.md:200-290` around the D3 line. Ran
`CAIRN_SUITE_LEDGER=0 PYTHONDONTWRITEBYTECODE=1
/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest
bootstrap/tests/test_upgrade_module.py
bootstrap/tests/test_module_merge_lockfile.py
bootstrap/tests/test_profile_grammar.py -q -p no:cacheprovider` --
**67 passed**, exit 0, full output inspected (2 lines total, not just the
tail) for a hidden `INTERNALERROR` -- none found. Confirmed the instrument
before trusting it: all three files import their targets from
`bootstrap._scaffold` directly (`from bootstrap._scaffold import upgrade as
UP`, etc.), not from the `templates/skills/_lib` twin, so a mutation to the
real engine would actually redden these tests rather than being masked by
a stale copy. Ran `python scripts/claim_check.py
dev/plans/adopt-into-existing-tree.md` -- clean (confirms the checker is a
path/line-bounds tool only; it does not and cannot catch the semantic
citation drift in Note 1 or Note 3, which is why this pass exists). Ran
`tools/lifecycle_planner.py next` against the plan to confirm current
state (`awaiting-plan-review`, structurally sound) before drafting this
pass.

**Not exercised** -- no code changes exist yet, so there is nothing to
mutation-test; the five S2 mutations and the D2/edge-case fixtures are
Boundary C's job once implementation lands. I did not attempt to reproduce
the original adopter's tree or hand-edited lockfile. I did not check
Windows filesystem semantics. I did not verify the sibling proposal
(`2026-08-20-claude-scanner-claim-scope`)'s own status for the issue-#5
closure dependency -- out of scope for a plan review of this proposal
alone. I did not run the full suite (not requested, and a bare
`python -m pytest bootstrap/tests` is refused by design) or touch
`bootstrap/tests/_gate_manifest.py` or any fixture under
`bootstrap/tests/fixtures/`.


## Response to plan review -- Claude (Author) -- 2026-08-25

Reviewer: Claude Sonnet 5 (Internal, fresh context), reviewing `86e49a3`.
Verdict was **no blocking findings**; all four notes are folded into the
operative cells below, per this lane's rule that a plan answers plan review
in its cells rather than in a contract revision.

| # | Finding | Disposition | Where it landed |
|---|---|---|---|
| 1 | `upgrade.py:1146-1148` cited for `_cmd_init_lock`'s angle-bracket guard; those lines are the "no committed profile" branch | -> accept | "The strict predicate lives in the adopt path" — citation corrected to `upgrade.py:1158-1160` |
| 2 | D3's "leaving the surrounding prose intact" is false against the live text; the plan carried no replacement paragraph | -> accept | "The D3 collision" — new subsection carries the full replacement text for `bootstrap/UPGRADE.md:251-267` |
| 3 | Boundary A named no file containing real `--adopt-module` CLI coverage; the actual suite is `test_upgrade.py:1133-1203` | -> accept | Verification / Boundary A — `test_upgrade.py` added and named first, with where new CLI tests belong and why not the other two |
| 4 | Approach step 1's token-map scoping looser than the "What" table's; a literal read permits a whole-profile merge by assignment | -> accept | Approach step 1 — rewritten to "the currently-adopting module's required tokens", merged into the existing map, never assigned over it |

**All four verified independently before folding, not taken on the reviewer's
word.** `upgrade.py:1146-1148` reads `if not profile_path.is_file(): return
_write_init_lock_profile_template(target)` / `try:`; the `placeholder_tokens`
guard begins at `:1158`. `class TestAdoptModule` is at
`bootstrap/tests/test_upgrade.py:1133`. `bootstrap/UPGRADE.md` does carry
"Two consequences:" above a two-item list whose item 1 is the recommendation
D3 removes, and whose "It is read-only" sentence refers back to the command
named in the sentence being deleted.

**Nothing was narrowed.** Every accepted outcome D1-D3 committed to is still
delivered; the four edits sharpen pointers, prose and scoping. The D3
allowance recorded above is unchanged and still the only deviation.

**One correction the reviewer flagged and I am not making.** Note 2 suggests
the plan "should carry the actual replacement text (or an explicit instruction
to fold to prose)". It now carries the text itself rather than the
instruction, because an instruction to "fold to prose" re-opens at
implementation time exactly the judgement the review just closed.


## Implementation verification -- Claude Sonnet 5 -- 2026-08-25

**Tested SHA**: `cc6c6c7` (the second of two implementation commits --
`bec2cca` D1+D2, `cc6c6c7` D3 -- both direct ancestors of the current
`master` tip; two unrelated `subtraction-sweep` commits landed on top from a
concurrent session during this verification and are not part of this
plan's diff). **Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(3.13.13, the canonical interpreter). **Pre-state**: `git status --short --
bootstrap/ dev/plans/adopt-into-existing-tree.md` empty (clean) immediately
before the Boundary B run. **Post-state**: clean again after (`git diff
cc6c6c7 -- bootstrap/_scaffold/upgrade.py` empty).

**Boundary B mode**: full. Not a choice -- `bootstrap/_scaffold/upgrade.py`
is the scaffold/merge engine (a named high-risk surface) and this touches
the install contract's `--adopt-module` write path, per the plan's own Risk
section.

### Boundary A (iteration, scoped) -- run before landing D1/D2

* `CAIRN_SUITE_LEDGER=1 python -m pytest bootstrap/tests/test_upgrade.py -k TestAdoptModule -q` -- **13 passed** (4 pre-existing + 9 new).
* `python -m pytest bootstrap/tests/test_upgrade.py -q` (full file) -- **96 passed**.
* `python -m pytest bootstrap/tests/test_profile_grammar.py -q` -- **45 passed** (41 pre-existing + 4 new/extended).
* `python -m pytest bootstrap/tests/test_upgrade_module.py bootstrap/tests/test_module_merge_lockfile.py -q` -- **23 passed**, unaffected by the `_superseded_surface_note` signature extension (its 2 callers there pass only 2 positional args; `exclude` defaults to empty).

Full output inspected for every run (not just the tail); no `INTERNALERROR`
found in any of them.

**The five S2 mutations, self-verified before the Boundary B run** (each
applied to a saved-original copy of `bootstrap/_scaffold/upgrade.py`, the
named test run, then the file restored and the restoration confirmed
byte-identical by sha256 -- `b8c5867349f4d9d89f50252051fbe8f30327c388efde1c1aaf646383136c04ed`
before the first mutation and after every restore):

| mutation | test that must redden | result |
|---|---|---|
| delete the persist call (`lock["tokens"] = tokens`) | `test_adopt_required_token_seeded_from_profile` | **reddened** (assertion on the persisted token value failed) |
| make the placeholder predicate curly-brace-only | `test_adopt_required_token_angle_placeholder_refuses_closed` | **reddened** (`<my package>` no longer refused) |
| move `_refuse_secret_tokens` back to just before `_commit_lock_and_caches` | `test_adopt_secret_shaped_required_token_refuses_closed` | **reddened** (the no-destination-written assertion failed -- the file was written before the guard fired) |
| make the byte comparison always-equal | `test_adopt_advisory_fires_when_kept_file_differs` | **reddened** (the advisory never printed) |
| make the byte comparison always-unequal | `test_adopt_advisory_silent_when_kept_file_matches` | **reddened** (the advisory printed on a byte-identical kept file) |

### Boundary B (integration, full)

```
CAIRN_FULL_SUITE=1 PYTHONDONTWRITEBYTECODE=1 \
  /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests \
  --quality-gate-shuffle-seed=0
```

**4596 passed, 3 failed, in 797.00s (13m17s).** Full output (4728 lines)
inspected, not just the tail; no `INTERNALERROR`. Non-pass disposition, all
three:

1. **`test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package`**
   and **`test_ast_attest.py::test_ast_gate_passes_over_the_full_scaffold_module_set`**
   -- **Fence 1, expected.** `python bootstrap/tests/_ast_attest.py verify
   bootstrap/tests/fixtures/scaffold_ast_baseline.json bootstrap/_scaffold/*.py`
   reports exactly **4 CHANGED** baselined symbols, **0 MISSING, 0
   DUPLICATE** -- the derived CHANGED set, precisely:

   | symbol | baseline digest | live digest |
   |---|---|---|
   | `FunctionDef:_cmd_adopt_module` | `81a91762d82268ba` | `e94a89ec4083cd40` |
   | `FunctionDef:_compute_upgrade` | `d8c2e51016e736c8` | `a98e65843a1c67be` |
   | `FunctionDef:_superseded_surface_note` | `183df5ea0106c0c1` | `f68dc613d601aa1f` |
   | `FunctionDef:cmd_upgrade` | `3a1480d796d59488` | `d98eff085ea46b43` |

   This is **not** the two-symbol set the briefing anticipated
   (`_cmd_adopt_module` + `_resolve_lock_profile_fields`) -- empirically,
   `_resolve_lock_profile_fields` is untouched (D1's strict predicate lives
   in the new `_adopt_token_unfilled`, deliberately not in that helper, per
   the plan's own instruction). The actual fourth-and-fifth deltas are a
   consequence not called out in the plan: `_resolve_current_profile`
   (itself **not** baseline-pinned) gained a third return value (`tokens`,
   for D1's profile-seeding), and its two upgrade-materialization call
   sites -- inside the baseline-pinned `_compute_upgrade` and `cmd_upgrade`
   -- each needed a one-token unpacking-arity edit (`_new_profile, new_axes,
   _new_tokens = ...`) to keep receiving it; that edit changes *their*
   digest even though neither function's own logic moved. `_superseded_surface_note`
   changed because D2's "must not both fire" edge case
   (architecture-review's destination is also its own declared superseded
   surface) needed an `exclude` parameter -- confirmed via
   `bootstrap/tests/test_upgrade.py::TestAdoptModule::test_adopt_advisory_fires_when_kept_file_differs`,
   which asserts both that D2's advisory fires AND that `"reconcile or
   retire"` does not appear in the same run's stderr.

   Per the fences in this brief: **not fixed, not routed around.** The
   baseline file was not edited; no `_ast_attest.py update-symbol` command
   was run (and none of the 4 symbols is in `_UPDATE_ALLOWLIST` regardless).
   Re-anchoring this baseline over the reviewed tree is a Maintainer-run,
   dry-run-verified direct correction per `bootstrap/AST_BASELINE_RUNBOOK.md`.

2. **`test_lifecycle_contract.py::test_the_live_corpus_is_sound_under_the_p1_contract`**
   -- **pre-existing, confirmed unrelated to this plan.** Fails on
   `dev/proposals/2026-08-20-claude-portable-sweeps-cannot-run.md`'s `##
   Review` (line 395) reading as authored by the proposal author rather
   than an independent reviewer -- a file this plan never touches, in a
   family (`dev/proposals/`) this plan's diff does not reach. Verified the
   same node fails **identically** (same file, same message) at the
   pre-implementation commit `7dc66a1` (this plan's D1/D2 commit's parent),
   checked out into an isolated `git worktree` (no destructive operation on
   the working tree) and run in isolation
   (`CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests/test_lifecycle_contract.py -k test_the_live_corpus_is_sound_under_the_p1_contract`)
   -- same failure, same corpus finding. The worktree was removed
   (`git worktree remove --force`) after the check; nothing else touched.

`python scripts/quality_gate.py --sub neutrality --sub redundancy`:
`[neutrality] fail=86 info=21`, `[redundancy] fail=0 info=2` -- **every**
flagged path is outside this plan's diff (`docs/`, `doctrine/`,
`templates/`, `bootstrap/tests/fixtures/skills/README.md`,
`templates/modules/default-on/_lifecycle_metrics/subsystems.py`); **zero**
flags in any of `bootstrap/UPGRADE.md`, `bootstrap/_scaffold/upgrade.py`,
`bootstrap/tests/test_upgrade.py`, or `bootstrap/tests/test_profile_grammar.py`.
Matches the tracked pre-existing gate-findings state; this plan introduces
no new neutrality or redundancy flag.

### Fence 2 -- the gate manifest, derived precisely (not run, not touched)

`bootstrap/tests/test_upgrade.py` and `bootstrap/tests/test_profile_grammar.py`
are both in `bootstrap/tests/fixtures/gate_manifest.json`'s 209-entry
`frozen_files` (confirmed by direct lookup, not assumed); no other file this
plan touches (`bootstrap/_scaffold/upgrade.py`, `bootstrap/UPGRADE.md`) is in
that set. Their live sha256 now differs from the committed manifest's
recorded value for each:

| file | recorded sha256 | live sha256 |
|---|---|---|
| `bootstrap/tests/test_upgrade.py` | `a85513e156e61d35d17690442583ba70acebf9d295cc3a0736f8c6bb576103d9` | `fdf758022386aab86e6cd403048d7803bb52a66b72e40b5af17734866a292791` |
| `bootstrap/tests/test_profile_grammar.py` | `9d6b777bfe48a1012bdfbbb92bdb5e43b2c25bfe0c9e364c46c39b93b4ccc89d` | `86cf4755fb60d66c6800397f3b9e4cd8e842a8488aefddcbd0ac0ef291d350b1` |

`bootstrap/tests/test_gate_manifest.py`'s own suite does **not** exercise
this drift (its `produced()` fixture calls `_gate_manifest.produce(_REPO)`
fresh at test time and verifies self-consistently -- it never diffs against
the committed `fixtures/gate_manifest.json`), so this did not and could not
show up as a Boundary B pytest failure; it is a property of the
differential-oracle gate ceremony
(`python bootstrap/tests/_gate_manifest.py verify --anchor-ref <SHA>`),
which was **not run**. Per the fences in this brief: the committed manifest
was not edited, and no re-anchor command was run; re-anchoring is
`bootstrap/REANCHOR_RUNBOOK.md`, a Maintainer ceremony.

### Known omissions

Windows filesystem semantics not checked (matches the plan's own plan-review
omission list). The sibling proposal `2026-08-20-claude-scanner-claim-scope`'s
status for the issue-#5 closure dependency was not re-checked (out of scope
for implementation). No attempt to reproduce the original adopter's tree or a
hand-edited lockfile beyond the fixtures constructed in
`bootstrap/tests/test_upgrade.py`.
