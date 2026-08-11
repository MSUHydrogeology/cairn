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
