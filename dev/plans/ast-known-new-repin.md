<!-- cairn-internal-ref-allow: doctrine/dual-review.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Plan: re-pin the stale AST known-new manifest (Parts 1-2)

**Source proposal**: `dev/proposals/archive/2026-07-22-claude-ast-known-new-repin.md`
**Status**: open
**Plan review**: required(Internal) — per the Decision's ratified plan
conditions (the proposal's own External-tier read already cleared the
design; the plan's job is translation + the currency re-check below,
which a fresh-context Internal read is the right tier for).

## Context

The Decision (2026-07-22, Anthony Kendall) accepted the Revised
proposal's Parts 1 + 2 in full, with two corrections to the record
(the proposal's own review was mislabeled Internal when it was
structurally External per cross-vendor authorship; and the review's
own audit table, I1, had 13 of 28 citations wrong despite a correct
bottom-line conclusion — the **author's** corrected table is ratified
as the audit of record). Full detail:
`dev/proposals/archive/2026-07-22-claude-ast-known-new-repin.md` — its
`## Revised proposal` section (28-symbol table) and
`## Decision > Ratified plan conditions` are authoritative.

**Ratified plan conditions, carried forward verbatim:**

* **Part 1's implementation work is transcription, not audit.** The
  audit is complete in the Revised proposal's table; this plan copies
  those symbols' digests into the regenerated manifest and does not
  re-derive provenance.
* **Part 2 uses `_classify()`'s literal predicate**, so the two halves
  of `_ast_attest.py` cannot drift apart again on this point.
* **Scope fence (binding):** no loosening of CHANGED/MISSING/DUPLICATE
  enforcement, no widening of `_UPDATE_ALLOWLIST`, no touching
  `scaffold_ast_baseline.json`. The supervised baseline re-anchor
  (`bootstrap/REANCHOR_RUNBOOK.md`, Maintainer-only) remains separate
  and still outstanding — unaffected by this plan.

**Currency re-check, this session (2026-07-31, 9 days after the
proposal was authored) — the whole point of this manifest is that it
goes stale fast, so this had to be re-verified, not assumed:**
`bootstrap/tests/_ast_attest.py verify` under the canonical `lhm`
interpreter reports the **same 60 NEW entries** (32 `Import:*` + 28
named symbols) as the proposal's table — **zero drift** since
2026-07-22. The audit table is still fully current; transcription can
proceed without any re-audit.

**A design detail the Decision didn't spell out, resolved here:**
of the existing 43 pinned `known_new` keys, 30 are `Import:`-type and
13 are named-symbol keys. All 13 named keys are still live and are an
exact subset of the 28-symbol audit table (digests independently
re-verified this session — 13/13 match the currently-pinned values
exactly, zero mismatches). Once Part 2 lands, `Import:*` keys are
categorically exempted from ever needing a `known_new` pin — so the
30 existing `Import:` entries become dead weight, not merely
redundant. **Chunk A's regenerated manifest contains only the 28
named-symbol keys** (13 already-pinned + 15 newly pinned), dropping
all 30 `Import:` entries — matching the proposal's own framing
("`Import:*` entries are handled by Part 2, not individually
re-pinned") to its logical conclusion rather than leaving stale
hash-keyed entries nobody will ever clean up otherwise.

### Documentation / doctrine surface

Both parts touch `bootstrap/tests/` engine-adjacent surfaces only — a
test fixture (Part 1) and a narrow internal-tool guard (Part 2), plus
the module docstring's own explanation of the mechanism (per the
proposal's Documentation / doctrine surface section). No `doctrine/`
or `AGENTS.md` change. No engine change to
`bootstrap/_scaffold/*.py` — `scaffold_ast_baseline.json` is
explicitly untouched (scope fence above), so no AST re-anchor applies
to *this* plan's own work (the irony of a plan about AST re-anchoring
not itself needing one is intentional: it edits the tooling and its
test fixtures, not the attested package).

## Sequence

```
A. Part 1 -- regenerate scaffold_ast_known_new.json (28 named symbols)  [commit pending]
B. Part 2 -- exempt Import:/ImportFrom:/Docstring# from the NEW check  [commit pending]
```

### Chunk A — Part 1 (regenerate the known-new manifest)

| # | File | Change |
|---|------|--------|
| A1 | `bootstrap/tests/fixtures/scaffold_ast_known_new.json` | Regenerate wholesale from the Revised proposal's 28-symbol table (verified current this session, zero drift — see Context). Transcribe each symbol's live digest (single-element list per key; `_ast_attest.digest_module()` over `bootstrap/_scaffold/{upgrade,_guard,config,install}.py`, re-run at implementation time, not copied from this plan's own preparation numbers without re-verifying). **Drops all 30 existing `Import:*` keys** (dead weight after Part 2 lands) — the regenerated file contains exactly the 28 named-symbol keys, 13 of which keep their already-pinned digest unchanged (independently re-verified this session: 13/13 match) and 15 of which are newly added. |

### Chunk B — Part 2 (exempt imports/docstrings from the NEW-symbol check)

| # | File | Change |
|---|------|--------|
| B1 | `bootstrap/tests/_ast_attest.py` | In `update_symbol()`'s NEW-symbol loop (`:299-307`), skip a key `k` from `new_problems` entirely — never checked against `allowed_new`, never flagged unpinned — when `k.startswith("Import:") or k.startswith("ImportFrom:") or k.startswith("Docstring#")`. **The exact literal predicate `_classify()` already uses** (`:144`) for the CHANGED/MISSING/DUPLICATE side, so the two enforcement paths share one definition and cannot drift apart on this point again (plan-review PR1 in the sibling `first-session-survivability` plan flagged this exact drift risk for a different pair of functions; this design avoids it from the start by literal predicate reuse, not just parallel logic). Named symbols (`FunctionDef`/`ClassDef`/`Assign`) are completely unaffected — the loop's existing pinned/mismatch/deleted-key checks apply to them exactly as before. |
| B2 | `bootstrap/tests/_ast_attest.py` | Module docstring (`:24-30` area, the `update_symbol` workflow description): short addition explaining the Import-exemption rationale, mirroring the existing per-module-necessity comment `_classify()` already carries (`:148-156`) — imports recurring across split modules are a per-module necessity, not injected/altered top-level logic, so pinning them by content hash buys no real security margin and is why the manifest went stale on ordinary commits. |
| B3 | `bootstrap/tests/test_ast_attest.py` (extend) | Regression coverage per the proposal's own Evidence plan: (a) a synthetic fixture module with a fresh, unpinned `Import:*`-shaped NEW entry passes `update_symbol` cleanly (no `known_new` pin required) when it is the only NEW entry and no CHANGED/MISSING/DUPLICATE exists; (b) a synthetic fixture module with a fresh, unpinned `FunctionDef`/`ClassDef`/`Assign` NEW entry still refuses exactly as today (`REFUSED — ... new-symbol violation(s)`) — so the exemption cannot silently widen to cover named symbols later without this test catching it. |

## Acceptance criteria

* **Tests that must pass** — the extended `bootstrap/tests/test_ast_attest.py`
  (Chunk B3, both new cases). `bootstrap/tests/_ast_attest.py update-symbol
  install_onboarding --baseline bootstrap/tests/fixtures/scaffold_ast_baseline.json
  --expect-old cec6f103797053c5 --known-new bootstrap/tests/fixtures/scaffold_ast_known_new.json
  bootstrap/_scaffold/*.py --dry-run` (the exact call the sibling
  `first-session-survivability` plan's Chunk D needed and could not use)
  must now succeed cleanly against the regenerated manifest, dry-run
  only — proving Part 1 + Part 2 together actually restore the guarded
  path's usability, not just that each part is individually plausible.
  Full `python -m pytest bootstrap/tests` green modulo the two
  pre-existing `test_ast_attest.py` sandbox-interpreter artifacts every
  sibling plan this session has documented (canonical `lhm` interpreter
  must show these two tests passing, not failing — this plan touches
  `_ast_attest.py` and its fixtures directly, so this is the one plan
  this session where those two tests' *content*, not just their
  pass/fail count, actually matters).
* **Examples / smoke checks required** — `bootstrap/tests/_ast_attest.py verify`
  over the regenerated manifest's paired baseline must still report the
  identical 60 NEW entries as informational notes only (not a new
  MISSING/DUPLICATE) — confirming Part 1's manifest change is additive
  to `verify`'s own behavior, not a hidden behavior change to the
  gate `verify` enforces.
* **Docs**: `python scripts/check_cairn.py` and `python scripts/claim_check.py`
  clean over the plan and every touched file.

## Signals the change is wrong

* **The dry-run `update-symbol` call above still refuses** after both
  chunks land → Part 1 or Part 2 has a real gap this plan's own
  preparation missed; do not proceed to declare success, re-derive
  from the actual refusal message.
* **A future commit's ordinary import-line change trips `update_symbol`
  again** despite Part 2 → the predicate match is narrower than
  `_classify()`'s in some edge case (e.g. a key format mismatch) —
  re-diff the two predicates literally, don't assume equivalence.
* **The regenerated manifest's dropped `Import:*` keys turn out to be
  read by something else** (not just `update_symbol`) → re-grep for
  `scaffold_ast_known_new` across the whole tree before finalizing
  Chunk A, not just `_ast_attest.py`.

## Review

*Filled in after the fresh-context Internal plan-review subagent pass.*

## Code review

*Filled in after implementation commits land (Chunks A-B).*

## Lasting-truth migration

*Filled in at archive time. Per the [Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home
outside the plan — the supervised `scaffold_ast_baseline.json`
re-anchor stays the Maintainer-only, separately-tracked outstanding
act this proposal's scope fence explicitly excludes.*

This section is append-only once written.
