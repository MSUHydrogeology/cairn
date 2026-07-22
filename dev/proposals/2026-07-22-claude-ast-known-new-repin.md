# Re-pin the stale AST known-new manifest (and stop it recurring)

**Author**: Claude (Strategy)
**Model**: Claude Sonnet 5
**Date opened**: 2026-07-22
**Status**: proposed
**Touches**: `bootstrap/tests/fixtures/scaffold_ast_known_new.json` (the manifest); `bootstrap/tests/_ast_attest.py` (`update_symbol`'s NEW-symbol strictness check — possibly narrowed, not the CHANGED/MISSING/DUPLICATE enforcement, which is unaffected); `bootstrap/tests/test_ast_attest.py` (new coverage for whatever the narrowed check becomes).
**Related**: found while preparing the Chunk D handoff for the accepted `dev/plans/first-session-survivability.md` (commit `4dfc98d`'s "Chunk D — supervised baseline re-pin" section documents the finding in place); the same guarded-`update-symbol` mechanism and its `_UPDATE_ALLOWLIST` are the ones the sibling `dev/plans/archive/adopter-licensing-compliance.md`'s Chunk D (commit `e1eec63`) also drove, for a different symbol.
**Plan review**: required(Internal) — narrows a verification-gate's strictness check (the NEW-symbol enforcement inside `update_symbol`), which a fresh-context reader should independently re-derive is safe (the CHANGED/MISSING/DUPLICATE enforcement that actually catches altered logic is untouched) rather than take on the author's word. Not a Security-Review trigger by the letter of `AGENTS.md`'s protected-contracts list (this doesn't touch `bootstrap/SAFETY.md`, `security_check.py`, or the content scanner, and `scaffold_ast_baseline.json`/`config.py`'s gate-manifest exclusion applies here too, per `_gate_manifest.py`'s `CASCADE_MUTABLE`) — but the audit component (confirming 25 untraced named symbols are legitimate) is exactly the kind of claim an Internal read should sample-check, not accept wholesale. External read welcome but not required by this proposal. Ratified at Decision.

## Context

Preparing first-session-survivability's Chunk D handoff script, I tried
routing its one allowlisted symbol (`install_onboarding`) through the
guarded `bootstrap/tests/_ast_attest.py update-symbol` path — the
narrow, self-service mechanism `_UPDATE_ALLOWLIST` exists for. It
refused:

```
[update-symbol] REFUSED — 60 new-symbol violation(s) alongside the
mapping change; a surgical re-baseline must NOT bless injected or
altered top-level logic. HOLD ...
```

`update_symbol()`'s design (`_ast_attest.py:209-296`) requires every
live top-level symbol absent from the committed baseline ("NEW") to
match a pinned `known_new` manifest by digest **and** multiplicity, or
it refuses outright ("strict: any new symbol refuses"). The committed
`bootstrap/tests/fixtures/scaffold_ast_known_new.json` pins 43 keys,
last touched 2026-06-08. The live `bootstrap/_scaffold/*.py` package
now carries **60** NEW top-level entries against it — none of them
this plan's own doing.

**Confirmed pre-existing, not caused by first-session-survivability.**
A disposable `git worktree` at `0864b16~1` (the commit immediately
before that plan's own Chunk A landed) shows the identical situation:
`verify()` reports the same NEW set as informational notes (it doesn't
enforce `known_new` — only `update_symbol()` does), and is otherwise
clean (174/174 baselined symbols accounted for). So this is
accumulated drift between 2026-06-08 and `0864b16~1`, entirely
unrelated to the three chunks first-session-survivability shipped.

**Breaking down the 60 (this session, `bootstrap/tests/_ast_attest.py
verify` at current HEAD):**

* **32 are `Import:*` hash-keyed entries** — content-addressed by
  `ast.dump` digest, so *any* new import line anywhere in the package
  mints a permanently-new key. `known_new` has no mechanism for these
  to stay current short of re-pinning after every commit that adds an
  import — which is most commits.
* **28 are named symbols** (`FunctionDef`/`ClassDef`/`Assign`) spread
  across `upgrade.py` (12), `_guard.py` (6), `config.py` (6),
  `install.py` (4). A representative trace (this session, `git log
  --diff-filter=A -S"<def>"`) finds three of them —
  `EngineFinder`, `ScaffoldLoaderError`, `_reject_polluted_children`
  (all `_guard.py`) — landing together in `a9e281b` ("scaffold-split:
  substrate Security re-review fixups R1 + R2"), i.e. already through
  a Security-Review-flavored commit, not orphaned or unreviewed. The
  remaining 25 were not individually traced this session (see Scope
  below).

**Why this matters beyond first-session-survivability.** Every future
single-symbol registry-mapping update — `_MODULE_MAPPINGS`,
`_SKILLS_MAPPINGS`, `_CORE_MAPPINGS`, or `install_onboarding`'s own
body, the exact class of change `_UPDATE_ALLOWLIST` was built for —
will hit this same refusal today, forcing the heavier, less-guarded
direct-edit path (baseline digest+span replacement outside the
`--expect-old`/one-symbol-delta/known-new guards) every single time,
even for genuinely narrow, legitimate changes. That defeats the point
of having a guarded self-service path at all.

## Proposal

Two parts — a data fix and a design fix, so the data fix doesn't just
go stale again on the next commit that touches an import line:

**1. Audit and regenerate `scaffold_ast_known_new.json`.** For each of
the 28 named-symbol NEW entries, trace it to its introducing commit
(`git log --diff-filter=A -S"<name>"` or equivalent), confirm it
shipped through this repo's normal review discipline (not an orphaned
or unreviewed addition), and record its current digest + multiplicity
in the regenerated manifest. `Import:*` entries are handled by Part 2,
not individually re-pinned.

**2. Narrow `update_symbol`'s NEW-symbol check to exempt `Import:*`
entries**, mirroring the exemption `_classify()` already applies to
the CHANGED/MISSING/DUPLICATE enforcement for imports and module
docstrings (`_ast_attest.py:148-156`, "per-module necessities, not
single-source moved symbols"). An import statement recurring across
split modules is not "injected or altered top-level logic" — the
threat `known_new`'s strict check exists to catch — so requiring it to
be individually pinned by content hash buys no real security margin
and is the entire reason this manifest goes stale on ordinary commits.
Named symbols (`FunctionDef`/`ClassDef`/`Assign`) keep full strict
enforcement, unchanged.

**Explicitly not proposed:** removing or loosening the CHANGED /
MISSING / DUPLICATE checks, widening `_UPDATE_ALLOWLIST`, or touching
`scaffold_ast_baseline.json` (this proposal's only baseline-adjacent
file is the known-new manifest).

### Documentation / doctrine surface

`bootstrap/tests/_ast_attest.py`'s own module docstring documents the
`update_symbol` workflow and the `known_new` mechanism's intent
(`:24-30`, `:209-249`) — the Import-exemption rationale gets a short
addition there, mirroring the existing per-module-necessity comment on
the `verify`-side exemption. No `doctrine/` or `AGENTS.md` change —
this is a scaffold-engine test-fixture correction plus a narrow
internal-tool guard adjustment, not a process or contract change.

## Rationale

* **Which workflow does it improve?** Restores the guarded
  `update-symbol` self-service path for the narrow case it was built
  for — the registry-mapping cascade (`_MODULE_MAPPINGS`/
  `_SKILLS_MAPPINGS`/`_CORE_MAPPINGS`/`install_onboarding`) that
  recurs on every module/skill/core install addition. Without this,
  every such change needs the heavier, un-guarded direct-edit path
  (Maintainer hand-verifies digest+span with no `--expect-old`/
  one-symbol-delta/known-new safety net) — worse, not better,
  security posture for routine changes.
* **What does it preserve?** The actual security property —
  CHANGED/MISSING/DUPLICATE enforcement on every named symbol, full
  strictness on any new `FunctionDef`/`ClassDef`/`Assign` — is
  untouched. Only the churn-generating, non-load-bearing `Import:*`
  hash-pinning requirement is narrowed.
* **Why now?** Found in original context while preparing a Chunk D
  handoff that depends on the exact mechanism this proposal repairs;
  the audit trail (which commit introduced which symbol) is easiest
  to reconstruct close to when it was noticed, and the maintainer
  asked that issues found in original context be handled there rather
  than deferred to an unscoped future backlog item.

## Alternatives considered

* **Do nothing; keep using the direct-edit path indefinitely.** Works
  (both plans in this session did exactly that), but means the
  guarded path — the one with real safety rails — is permanently
  unusable, and every future registry-mapping change repeats this
  same discovery.
* **Blind bulk re-pin (dump today's NEW set into `known_new.json`
  without auditing).** Rejected — defeats `known_new`'s purpose. The
  tool's own design (strict-by-default, one-symbol-delta, `--expect-
  old`) exists specifically so a re-pin can't silently bless
  unreviewed logic; an unaudited dump does exactly that.
* **Re-pin only, no Import exemption.** Fixes today's 60 but recurs on
  the next commit that adds any import anywhere in `_scaffold/` —
  observably imminent given how often that happens in this package.
* **Chosen: audit + regenerate, plus the Import exemption** — fixes
  the immediate blocker and removes its main recurrence source,
  without touching the enforcement that actually matters.

## Evidence / verification plan

* **Tests required**: extend `bootstrap/tests/test_ast_attest.py` with
  a case asserting a fresh `Import:*` NEW entry (synthetic module
  fixture, mirroring the existing `test_module_docstrings_do_not_trip_
  single_source`-style fixture tests) does **not** require a
  `known_new` pin, while a fresh unpinned `FunctionDef`/`ClassDef`/
  `Assign` still refuses exactly as today (a regression guard so the
  exemption can't silently widen further). [test_ast_attest.py — file
  exists](../../bootstrap/tests/test_ast_attest.py).
* **Examples / smoke checks**: after regeneration, `update-symbol
  install_onboarding --expect-old <digest>` (the exact call first-
  session-survivability's Chunk D needed) succeeds against the live
  module set without the direct-edit fallback.
* **Docs**: the `_ast_attest.py` module-docstring addition (see
  Documentation / doctrine surface above).

### Author-accounting — invariants, failure modes, edge cases

* **Invariant**: every baselined symbol's CHANGED/MISSING/DUPLICATE
  enforcement is bit-for-bit unchanged by this proposal — enforced by
  the existing `test_ast_gate_passes_over_the_full_scaffold_module_
  set` and the new regression test above.
* **Failure mode**: a malicious or mistaken commit that renames a new
  helper's import to smuggle altered logic behind an `Import:` key —
  closed: imports are structurally digested (`ast.dump`) same as
  everything else; the exemption only removes the *pinning
  requirement*, not the digest computation, and a changed import's
  digest still shows as a fresh, still-unenforced `Import:` NEW entry
  no differently than today (imports were never subject to CHANGED
  enforcement either, per the pre-existing `_classify()` skip) — this
  proposal changes nothing about that risk surface, it only stops
  `update_symbol` refusing over it.
* **Edge case**: an `Import:*` key that collides in hash with an
  unrelated import elsewhere (astronomically unlikely, same digest
  space `ast.dump`+`hashlib` already use throughout this file) — out
  of scope, pre-existing to the whole mechanism.
* **Known omission**: only 3 of the 28 named NEW symbols were traced
  to an origin commit this session (a representative sample, chosen to
  confirm none are orphaned/unreviewed); the full 28-symbol audit is
  this proposal's own implementation work, not yet done.

## Signals the change is wrong

If the regenerated `known_new.json` or the Import exemption lets
`update-symbol` accept a change it should have refused — e.g. a
future PR's altered-logic-behind-an-import slips through where the
direct-edit path would have surfaced it in review — that is the
signal to revert the exemption and fall back to full manifest pinning
including imports, accepting the churn cost as the price of the wider
safety margin.
