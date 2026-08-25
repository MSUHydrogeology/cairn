# Plan: adopting a module into an existing tree

**Source proposal**: `dev/proposals/2026-08-20-claude-adopt-into-existing-tree.md`
(accepted Revision 2, 2026-08-20)
**Status**: awaiting-plan-review
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
1. resolve the candidate token map (profile ∪ lockfile, lockfile wins)
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
`upgrade.py:1146-1148` is **not** in `_resolve_lock_profile_fields` — so "reuse
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

**This is a deviation from an accepted term and needs the Maintainer's
allowance.** Recorded here rather than taken: the plan-review reviewer should
say whether the reasoning holds, and the Decision on this plan's disposition
grants or refuses it. If refused, option 1 is the fallback and costs one line of
sweep work later.

## Verification

**Boundary A (iteration, scoped).** `bootstrap/tests/test_upgrade_module.py`,
`bootstrap/tests/test_module_merge_lockfile.py`,
`bootstrap/tests/test_profile_grammar.py`. `--adopt-module` is exercised through
its **real CLI entry point**, and the secret-token refusal through the CLI, not
by a direct helper call.

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
