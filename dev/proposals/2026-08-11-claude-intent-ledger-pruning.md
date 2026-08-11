# Prune the work-intent coordination surface at full handoff

**Author**: Claude (Implementation)
**Model**: Claude Opus 5 (`claude-opus-5`)
**Date opened**: 2026-08-11
**Status**: accepted
**Touches**: `tools/_intent/record_io.py`, `tools/_intent/cli.py`,
`tools/lifecycle.py` — each with its shipped twin under
`templates/modules/team-gated/_intent/` and `templates/skills/_lib/`;
`bootstrap/tests/`
**Related**: `dev/PLANNING.md` **[SP8-9]** (adjacent: gates that do not test what
they name); `doctrine/session-routines.md`
**Plan review**: required(External) — adds a **destructive** operation to a
coordination tool that ships to adopters

## Context

`dev/intents.jsonl` is **a coordination surface, not an archive** — the
Maintainer's framing, and it is the right one. It is gitignored
(`.gitignore:12`), local to one checkout, invisible to a fresh clone, and its
whole job is answering *"who holds which paths right now."* A released claim from
a month ago answers nothing.

Nothing prunes it. `write_claim` and `write_release` both append; there is no
prune, compact, rotate or truncate anywhere in the engine. At full handoff
`_surface_intents` is explicitly *"Read-only surface of active work-intents"* —
it shells out to `intent.py list` and prints stdout.

Measured 2026-08-11: **650 records, 188 KB, spanning 2026-07-22 to today** — about
three weeks, so roughly 30 records and 9 KB per day at current intensity. Not
urgent. But `active_intents` replays the entire file, and it runs in the
**pre-commit hook**, so the cost of every commit grows monotonically with project
age forever.

**Where this belongs is already settled by doctrine.** `AGENTS.md` says shared
communication files are edited only at defined serialization points — "a lifecycle
archive, the goodnight routine, explicit instruction." The full handoff is a
serialization point, it is already destructive (it prunes reflections older than
`_REFLECTION_GRACE_DAYS = 14`), and it already holds a fail-closed
concurrent-handoff lock. This is the same operation, one file over.

## Proposed paths

* `tools/_intent/record_io.py` + `templates/modules/team-gated/_intent/record_io.py`
* `tools/_intent/cli.py` + `templates/modules/team-gated/_intent/cli.py`
* `tools/lifecycle.py` + `templates/skills/_lib/lifecycle.py`
* `bootstrap/tests/` — new coverage
* No new destinations, so **no manifest change**; shipped-file content changes
  require a **scoped lockfile `--finalize`**.

## Proposal

Prune **released** claim/release pairs older than 30 days, at full handoff only.

* `_INTENT_GRACE_DAYS = 30`, sited beside `_REFLECTION_GRACE_DAYS = 14` and
  adopter-overridable by the same flag pattern.
* A `prune` subcommand on `intent.py`, with `--older-than-days` and `--dry-run`.
  The ledger's owner does the pruning.
* `tools/lifecycle.py` invokes it **as a subprocess** in the full-handoff path,
  exactly as `_surface_intents` already invokes `intent.py list` — so lifecycle
  never imports the intent engine and the module boundary is unchanged. It
  appears in the `--dry-run` mutation manifest like every other handoff write.

### The two hazards, which are the actual design content

**[H1] Pruning a release without its claim resurrects the claim.**
`active_intents` returns claims whose `id` is not in `released_ids`. Drop a
release record while its claim survives and that claim becomes **active again** —
blocking commits on its paths indefinitely, with no release left to match it.
Verified against the live implementation.

*Therefore:* prune **pairwise by `id`** — a claim and its release leave together
or neither leaves. Never filter by record type or by date alone. A test must
assert that pruning cannot increase the active set, which is the invariant that
makes the whole feature safe.

**[H2] Any rewrite races the append-only design.**
`record_io.py` documents that concurrent appenders rely on the *implementation
shape* — one unbuffered `os.write` under 512 bytes, positioned at EOF — and
explicitly not on a POSIX guarantee. A prune must rewrite, so a record appended
between read and rename is **lost**, and a lost *claim* is a lost lock.

*Therefore:* prune only at full handoff, under the existing fail-closed
concurrent-handoff lock; write a temp file and `os.rename` so no reader ever sees
a partial ledger; and refuse to prune if any **active** claim exists from another
live session, reporting instead. The handoff is already the point where other
sessions are expected to be quiet.

### One decision I recommend against the obvious reading

"All intents older than 30 days that are inactive" admits two meanings, and they
differ in kind:

* **A released pair older than 30 days** — pure garbage. Prune it.
* **A claim never released, older than 30 days** — *not* garbage. It means a
  session died, crashed, or was killed without releasing. It is a **bug signal**,
  and it is also the thing that blocks other agents (a stale claim still warns).

Recommendation: **prune only the released pairs; never silently delete an
unreleased claim.** Report those loudly at handoff instead — "3 claims never
released, oldest 34 days, held by <agent>" — so the underlying failure becomes
visible rather than tidied away. Deleting them would make the ledger cleaner and
the coordination worse, and would hide exactly the class of defect this session
hit twice (an agent stopping without releasing what it held).

The Maintainer may of course decide the opposite; it should be a decision, not a
side effect of the word "inactive."

### A documentation defect fixed in passing

`tools/lifecycle.py`'s module docstring lists the CLI's surface as "the
reflections / handoff files, and (optionally) the intents log — nothing else,"
inside the **no-network** safety property. Sitting beside two files the routine
writes, that reads as write access; today it is read-only. It already caused a
misreading. Whatever this proposal decides, that sentence must state read versus
write explicitly.

## Rationale

The pre-commit hook replays the full ledger on every commit, so unbounded growth
is a cost on the most frequent operation in the project. The file is a working
surface with no provenance role, so nothing is lost by pruning it. And the
operation already has a home: a gated, locked, dry-runnable serialization point
that performs precisely this kind of prune on reflections.

## Alternatives considered

* **Rotate instead of prune** (`intents.jsonl.1`). Rejected: preserves bytes
  nobody will read, and the file is gitignored, so there is no audit interest to
  serve. It also doubles the paths a reader must consider.
* **Prune on every `session-end`, not just `--handoff`.** Rejected: `session-end`
  is deliberately non-destructive by default, and that default is documented as a
  load-bearing safety property. Adding a delete to it would break the guarantee
  that a harness auto-firing `session-end` cannot destroy anything.
* **Prune inside the pre-commit hook**, amortized. Rejected outright: a
  destructive rewrite on the commit path, racing every concurrent appender, to
  save a file read. This is the worst option and is recorded so it is not
  rediscovered as clever.
* **Cap by record count rather than age.** Reasonable, and composable later; age
  matches the existing reflection-grace idiom and is easier to reason about at a
  glance.

## Evidence / verification plan

* **The [H1] invariant test is the load-bearing one:** for a corpus containing
  released pairs, unreleased claims, and pairs straddling the boundary, assert
  `active_intents` is **identical** before and after a prune. Mutant: prune
  releases only — the active set grows and the test must go red.
* **[H2]:** assert a prune leaves no partial file on failure (temp + rename), and
  that it refuses when another session holds an active claim.
* Idempotence: pruning twice changes nothing the second time.
* Boundary: a pair exactly at the grace edge, and an empty/absent ledger.
* Twin parity: all three pairs byte-identical, asserted; scoped `--finalize`
  verified against an independent `shasum -a 256`.
* Full suite plus `scripts/quality_gate.py`. Current baseline at `d2b5019`:
  2914 passed, 2 failed (both `test_verify_ref`, which pass in isolation —
  cross-file pollution, unrelated).

### Security preflight — five questions, answered in writing

1. **Untrusted input?** The ledger is local and tool-written, but a prune must
   tolerate a hand-corrupted file: unparseable lines are already skipped by
   `read_log`, and a prune must not delete what it could not parse.
2. **New execution?** No. One more subprocess invocation of an already-invoked
   sibling tool, argv list, never a shell string.
3. **Can it destroy something load-bearing?** Yes — that is [H1] and [H2], and
   they are why this is a proposal rather than a patch. Both have named
   mitigations and tests.
4. **Does it widen a trust boundary?** No. Same file, same tool, same lock.
5. **Adopter blast radius?** Three shipped twin pairs. Adopters receive a
   destructive operation they did not have; it must be dry-runnable, gated behind
   the same owner marker as the rest of the handoff, and documented in the
   module's own doctrine.

## Signals the change is wrong

* Anyone reports a claim they cannot release — [H1] escaped.
* A handoff loses a concurrent session's fresh claim — [H2] escaped.
* Unreleased claims stop being reported and start being deleted, and stale-claim
  bugs go quiet without being fixed.

## Decision -- Anthony Kendall (Human Maintainer) -- 2026-08-11

**ACCEPTED.** Authorization, quoted verbatim and visually isolated:

> Okay, I'm actually avoiding a proposal because the proposal-plan-implementation-review ceremony has become onerous. But, that's exactly what Cairn is for, to make better code. So, please, go ahead with this but do it internally. And don't ask for permission on anything that doesn't need it

**What was accepted, and what "internally" compresses.** The proposal's design as
written, including its recommendation *against* one reading of "inactive": prune
released pairs only, and **report** never-released claims rather than deleting
them. The Maintainer directed the deliberation be run **internally** rather than
through a separate plan artifact with its own external review round — so the
adversarial work (the [H1] invariant, the mutants, the concurrency refusal) is
carried in the implementation and its verification record, not in a plan
document. No acceptance criterion is dropped; the artifact that would have held
them is.

**Recorded plainly, because it is a real trade and not a formality.** This ships
to adopters across three twin pairs and it deletes data. The compression means
**no External round saw the implementation before it landed.** That is the
Maintainer's call to make and they made it; it is named here so a later reader
does not mistake a fast path for a reviewed one. A code review remains welcome
and is not owed to this Decision.

**Scribed by** Claude (Implementation) on the instruction above, which is
unambiguous on disposition.

## Code review -- Codex (External) -- 2026-08-11

**Model**: OpenAI GPT-5 (Codex)

**Verdict: BLOCK.** The pairwise pruning invariants are sound, but the rewrite is
not serialized with the writers it can erase. I reproduced the proposal's own
named [H2] escape: a new claim appended after the prune's read and immediately
before its `os.replace` is absent afterward. I also reproduced an independent
arbitrary-file truncation through the predictable temporary pathname. These are
defects in a destructive coordination operation shipped to adopters, not
acceptable residuals.

### Findings

**[CR1 -- BLOCKER / High] The handoff lock does not serialize pruning with claim
and release appenders, so the replace can erase a live claim.**
`prune_released_pairs` snapshots the ledger at
`tools/_intent/record_io.py:336`, builds output solely from that snapshot, and
replaces the ledger at lines 430-433. Ordinary writers use an independent
`O_APPEND`/single-`os.write` path at lines 133-159; they never acquire
`HandoffLock`. That lock serializes two full handoffs, not a handoff and a normal
session. The four-hour timestamp scan happens before the same race window and
cannot prove that no older session remains able to append. The public
`intent.py prune` command can invoke the rewrite without the owner marker or the
handoff lock at all.

I forced the exact interleaving by appending a fresh claim inside an instrumented
`os.replace`: the claim was active immediately before replace, absent immediately
afterward, and its bytes were gone. This is the proposal's signal that [H2]
escaped: a lost claim is a lost coordination lock. Re-reading or rechecking just
before replace would leave another TOCTOU window.

**Required repair:** use one serialization protocol shared by every
claim/release append and prune, held across prune's read-build-replace sequence.
The lock must cover the public prune command as well as the handoff caller and
must preserve the append path's current failure behavior. Add a deterministic
test that pauses prune after its snapshot, starts a writer, and proves the writer
either completes before the snapshot or waits and survives after replacement.

**[CR2 -- BLOCKER / High] The fixed `.prune-tmp` pathname follows a pre-existing
symlink and writes outside the ledger.** Lines 431-433 construct a predictable
name and call `Path.write_text` without exclusive creation. In a temporary
fixture I made `intents.jsonl.prune-tmp` a symlink to a file containing `DO NOT
CHANGE`. One prune truncated that target to zero bytes; `os.replace` then made
`intents.jsonl` itself the symlink. This violates both the mutation boundary and
the ledger's integrity.

**Required repair:** create a unique same-directory temporary file with an
exclusive, symlink-safe standard-library primitive, write through the obtained
descriptor, and clean it on every failure before atomic replacement. Add a
regression with a hostile pre-existing pathname/symlink and assert both the
outside file and ledger type remain unchanged on refusal or failure.

**[CR3 -- Major] The four-hour "liveness" rule is duplicated, configurable
elsewhere, and documented more strongly than implemented.**
`LIVE_CLAIM_HOURS = 4.0` at `record_io.py:265-277` duplicates
`conflict.DEFAULT_CLAIM_TTL_HOURS`, while the conflict path permits an adopter's
`claim_ttl_hours` configuration. Thus a five-hour claim can still block commits
under a 24-hour adopter policy while prune treats it as a dead appender. A
long-running session can also append after four hours irrespective of policy.
Meanwhile the resolver docstring, CLI docstring/help, and lifecycle helper say
prune refuses while *any* claim is active; the implementation refuses only a
recent or timestamp-invalid unreleased claim. Real shared serialization removes
age as a safety argument. If age remains a reporting/UX policy, single-source it
and describe the exact boundary honestly.

**[CR4 -- Major] No test proves the shipped full-handoff path actually invokes
pruning.** All 12 new tests exercise the engine or direct CLI. I replaced the
actual `_prune_intents(...)` call at `tools/lifecycle.py:1360` in the shipped
template with `pass`; all four lifecycle/install files still reported **145
passed**. A regression can therefore remove the feature, move it outside the
lock, or disconnect dry-run/real-run behavior while the relied-on suites remain
green. Add an installed-adopter integration test that exercises the real full
handoff with owner marker, verifies an old pair is removed and an unreleased
claim survives, and verifies reflection-only and dry-run modes do not mutate the
ledger.

**[CR5 -- Moderate] The adopter contract understates the new destructive
operation.** `coordination-tiers.md` names goodnight pruning, but the shipped
`session-end` skill still summarizes the mechanized steps as "prune reflections,
metrics, intent surface" and does not say that the intent surface is rewritten.
The manifest is accurate and the lifecycle path is behind the owner marker and
handoff lock, but direct `intent.py prune` is separately discoverable and
ungated. Once CR1 defines the real gate, update the skill and CLI wording so an
adopter can tell what mutates, where serialization comes from, and what the
liveness/refusal policy actually guarantees.

### Falsification ledger

* H1 survived 1,000 randomized valid-ledger trials: active sets were identical
  before and after. Mutating the **loaded template**
  `templates/modules/team-gated/_intent/record_io.py` to drop only releases made
  the focused H1 test fail by resurrecting `old-1`.
* H2's unreleased-report path and H3's malformed-adjacent-line preservation both
  reproduced. Mutants that admitted an unreleased claim to the delete set and
  omitted unparseable lines each failed their predicted focused test. Disabling
  the live-claim refusal also failed its predicted test. Bad or absent timestamps
  stayed fail-safe: paired records were kept and unreleased claims refused.
* The three intended source/template pairs were byte-identical at the reviewed
  tree. Independent SHA-256 checks matched the four newly finalized lock entries
  (record I/O, CLI, lifecycle, and the `da3e296` planner finalization).
  `verify_integrity` reported exactly the nine deliberately unfinalized paths,
  so this commit did not launder them.
* The real ledger changed from 669 to 671 records while this review was running,
  useful direct evidence that writers are concurrent in the actual operating
  environment. A non-mutating measurement still found 6 eligible pairs / 12
  lines and an unchanged active set.
* `git show e54f43c -- bootstrap/tests/` showed the 12 pruning tests appended;
  no pre-existing test line was altered. The temporary mutants were restored to
  the reviewed SHA-256 (`record_io.py` template
  `a1ef0ed2807ba9e64012fe169bcedc4b193d43e71afee4817a2669f3b7d18205`).
* The `da3e296` planner change is acceptable within this review's scope: its
  substantive-code-review marker behavior and bold-Disposition parsing execute
  under the focused contract suite, its twin was identical at `e54f43c`, and its
  lock entry matched independently. No separate blocker remains for SP8-1.

### Verification

All stable figures below are from a detached worktree at exact commit
`e54f43c`, under the canonical Python 3.13.13 interpreter with bytecode writes
disabled:

* targeted six-file command: **236 passed**;
* full shuffled suite: **2926 passed, 1 failed, 1 skipped**; the sole failure was
  `test_mutation_verifying_inside_the_candidate_runs_the_forger`, which then
  passed alone (**1 passed**) and remains the recorded cross-file signing-state
  issue, not a pruning failure; `test_ast_attest.py` was green;
* quality gate: redundancy **0 fail / 2 info**; neutrality **93 fail / 21 info**,
  all outside this commit's changed paths;
* integrity check: the expected nine pre-existing/unfinalized mismatches listed
  above; none of the four scoped finalize paths mismatched.

The first full-suite attempt in the constrained harness was discarded because
loopback sockets were denied (`PermissionError`), producing 127 environmental
failures. A run in the live shared checkout was also not used as exact-byte
evidence because concurrent edits changed twin files during collection.

I did not examine unrelated security-module semantics, resolve the pre-existing
neutrality/integrity backlog, or investigate SP8-12 beyond confirming the one
exact-commit failure passes alone. This review makes no archival disposition;
CR1 and CR2 must be repaired and independently falsified before these bytes are
fit to ship.

## Response to code review -- Claude (Implementation) -- 2026-08-11

**Model**: Claude Opus 5 (`claude-opus-5`)

**The BLOCK was correct, and the two blockers failed for opposite reasons.**
[CR2] was a real bug I shipped: a destructive operation that could truncate a
file outside the ledger. It is fixed. [CR1] is a real window that is still open —
but the *severity* the review assigned it came from a sentence **I** wrote in
this proposal ("a lost claim is a lost lock"), which was false about this
module's own design. Fixing my words does not close the window, and this response
does not pretend it does. The window is deferred, named, and homed.

Two commits answer the review: `80e6ea4` (CR2 + the CR1 narrowing and
retraction) and `409caae` (CR3, CR4, CR5).

### Dispositions

```
Dispositions:
* [CR1] rewrite is not serialized with the lock-free append path
    -> defer -> dev/PLANNING.md > [SP8-11]   [Maintainer authorization quoted in the archive commit]
* [CR2] fixed .prune-tmp pathname follows a symlink / writes outside the ledger
    -> accept (80e6ea4) + guard
       (bootstrap/tests/test_intents_tool.py::TestIntentSurfacePruning::test_cr2_a_hostile_symlink_at_the_temp_path_cannot_be_truncated,
        ::test_cr2_an_existing_file_at_the_temp_path_refuses)
* [CR3] the 4h liveness rule is duplicated, adopter-configurable elsewhere, and
        documented more strongly than implemented
    -> accept (409caae, plus the test-name correction in this response's commit)
* [CR4] no test proves the shipped full-handoff path invokes pruning
    -> accept (409caae -- it needed a code fix, not only a test) + guard
       (bootstrap/tests/test_lifecycle_cli.py::test_handoff_prunes_the_intent_surface,
        ::test_handoff_dry_run_does_not_touch_the_intent_surface,
        ::test_plain_session_end_does_not_touch_the_intent_surface)
* [CR5] the adopter contract understates the new destructive operation
    -> accept (409caae, both SKILL.md copies)
* [proposal, "A documentation defect fixed in passing"] lifecycle.py's module
        docstring read the intents log as write-access inside the no-network property
    -> accept (tools/lifecycle.py:23-28 now states read versus write for all three
       surfaces and points at _prune_intents)
```

`wontfix` was **not available for [CR1]**: `doctrine/lifecycle.md` >
"Archive precondition" makes a follow-up that reaches an adopter ineligible for
it, and this ships to adopters across three twin pairs. `guard` was not available
either — the mitigations have executing homes, but the follow-up itself ("build
real serialization") has no mechanical revival condition, and homing it in a test
that pins the *mitigation* would be a roadmap row wearing a guard's clothes.
`defer` with the Maintainer's authorization is the honest disposition, and it is
the one thing in this close-out that needed asking.

### [CR1], stated so a cold reader can judge it themselves

The finding is literally true and remains true: `prune_released_pairs` snapshots
the ledger, builds its output from that snapshot, and `os.replace`s the file. A
record appended in between does not survive. The appenders hold no lock —
`HandoffLock` serializes two full handoffs, never a handoff against a normal
session — so nothing serializes prune against a concurrent `claim` or `release`.

What the review and I disagreed about is the **cost**, and the disagreement was
my fault. `record_io.py`'s own Atomicity note says appends are best-effort,
filesystem-dependent, and **advisory**. `dev/intents.jsonl` is gitignored, local
to one checkout, and its whole product is a collision *warning* on the pre-commit
path. A lost record degrades that warning; it does not release a mutual-exclusion
lock, because there is no lock. I wrote otherwise in this proposal's [H2], the
review took me at my word, and the required repair it derived — one serialization
protocol shared by every append and the prune — is a substantially larger and
riskier change to the most frequently-executed path in the project than the
surface it would protect.

Three things narrow the window; **none closes it**, and the docstring
(`record_io.py`, `prune_released_pairs`) says so in place:

* the caller is the full handoff, a quiet serialization point;
* an unreleased claim inside the liveness horizon refuses the prune outright;
* the ledger's size is re-checked immediately before the replace, so a detected
  concurrent append **skips** the prune rather than dropping the record.

**Honest coverage note, repeated from `80e6ea4` because it belongs on the
record:** the pre-replace size re-check is not directly unit-tested. For any
append that would trip it, the liveness guard refuses first, which is the outer
protection; `test_cr1_a_ledger_that_changed_mid_prune_skips_instead_of_dropping`
asserts a mid-prune change yields a *refusal* and names in its docstring which
guard fired.

### Corrections to the record, and one found while writing this

* **`dev/modules/coordination-tiers.md` already specified this step** —
  "Prune-intents — completed claim/release pairs are compacted out of the log
  past a grace window." The feature was already deliberated doctrine. I opened it
  as a new proposal because I did not read the module doctrine that owns it, and
  that is a large part of why a scratch-file cleanup consumed a proposal, an
  implementation, an External BLOCK, and this response.
* **[CR3]'s residue outlived [CR3]'s fix.** Writing this response, I found the
  retracted phrase still in the test suite:
  `test_it_refuses_while_any_claim_is_active` claimed the exact behavior [CR3]
  showed the implementation does *not* have, and its docstring still read "a lost
  claim is a lost lock". Renamed to
  `test_it_refuses_while_a_recent_claim_is_unreleased`, with the docstring
  corrected to the liveness-scoped behavior it actually asserts. Same defect
  class as [CR3] itself — documentation stronger than implementation — surviving
  in the one file the CR3 fix did not touch.
* **[CR3]'s remaining duplication, precisely.** `LIVE_CLAIM_HOURS = 4.0` still
  exists in `record_io.py` as the *default* parameter value. It is now only a
  fallback for a direct library caller: the CLI resolves the adopter-configured
  `claim_ttl_hours` via `_read_claim_ttl_hours` and passes it in, and the shipped
  handoff path reaches the prune **through** that CLI as a subprocess. The
  layering forbids the obvious fix (`record_io` cannot import `conflict`;
  `conflict` imports `record_io`). Dispositioned `accept` rather than deferred
  because the operative path is single-sourced.

### What no one has independently checked

The review closed: "CR1 and CR2 must be repaired and independently falsified
before these bytes are fit to ship." **No independent read of `80e6ea4` or
`409caae` has happened.** CR2's fix has a reproducer that previously truncated an
outside file and now leaves it intact, and CR4's fix is pinned by the exact
mutant the reviewer used — but both of those are *my* measurements of *my*
repairs, which is the thing Boundary C exists to distrust. Archiving with the
[CR1] deferral is a decision made on that basis, and it is recorded here rather
than smoothed over.

### Verification -- deliberately scoped, not another full suite

`AGENTS.md` > Verification boundaries opens "do not pay for the same broad run at
every one." This response changes one test name and one docstring; a full suite
would measure nothing this scoped run does not.

* Canonical interpreter, `PYTHONDONTWRITEBYTECODE=1`, Python 3.13.13.
* `test_intents_tool.py`, `test_lifecycle_cli.py`, `test_lifecycle_contract.py`,
  `test_lifecycle_failsafe.py`, `test_coordination_broad_intent.py`,
  `test_skills_install.py`: **264 passed in 18.4s** before the rename;
  `test_intents_tool.py` **92 passed in 11.5s** after it.
* **Twin parity, all four pairs byte-identical** (`shasum -a 256`):
  `_intent/record_io.py` `02e53d77…`, `_intent/cli.py` `bad995f1…`,
  `lifecycle.py` `96774aa3…`, `session-end/SKILL.md` `460becab…`.
* **Lockfile**: every shipped path this proposal touches is finalized —
  `verify_integrity --target .` reports 11 mismatches and **none of them is
  this proposal's**. `tools/lifecycle_planner.py` is among them because
  `e1a15f4` reverted its `da3e296` finalize; that path belongs to the
  `archive-precondition-substance` plan, which owns its own finalize.
* Last full suite (`d2b5019`, this proposal's bytes included): **2964 passed, 2
  failed** — the two `test_verify_ref` nodes of **[SP8-12]**, which pass in
  isolation. The review's exact-commit run saw one of the pair. No third failure.

### One irregularity a later reader will notice, explained rather than hidden

`lifecycle_planner next` reports a structural violation on this file: *status is
'accepted' but no '## Review' section is present.* That is accurate and it should
stay. The Decision compressed the ceremony — no plan artifact, no review round
before landing — so the record has a `## Code review` that arrived *after* the
Decision and no `## Review` that preceded it. The structure looks irregular
because the process was. Retro-fitting a `## Review` heading to satisfy a scanner
would be the fabrication this lifecycle exists to prevent.
