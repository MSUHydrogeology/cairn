<!-- cairn-internal-ref-allow: doctrine/dual-review.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Plan: re-pin the stale AST known-new manifest (Parts 1-2)

**Source proposal**: `dev/proposals/archive/2026-07-22-claude-ast-known-new-repin.md`
**Status**: review
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
  those symbols' digests **and multiplicities** into the regenerated
  manifest (plan-review PR5 — the Decision's exact wording) and does not
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
| B1 | `bootstrap/tests/_ast_attest.py` | Define one shared helper, `_is_per_module_necessity(key)`, returning `key.startswith("Import:") or key.startswith("ImportFrom:") or key.split("#", 1)[0] == "Docstring"` — the Docstring check matching `_classify()`'s own `key.split("#", 1)[0] == "Docstring"` exactly (plan-review PR3; not `startswith("Docstring#")`, which misses a bare `"Docstring"` key `_classify()` would exempt). Apply it in **both** places `update_symbol()` needs it (plan-review PR2, closing an asymmetry the original design missed): (1) the NEW-symbol loop (`:299-307`) — skip a key `k` from `new_problems` entirely when `_is_per_module_necessity(k)`; (2) the `MISSING-KNOWN-NEW` loop (`:311-315`, `for k in sorted(set(allowed_new) - set(new))`) — same skip, so a pinned `Import:`/`Docstring#`-prefixed key that later vanishes from the live set can never trip this loop either, making the exemption correct-by-construction regardless of what the manifest happens to contain (not merely a consequence of Chunk A dropping all `Import:` pins today). Named symbols (`FunctionDef`/`ClassDef`/`Assign`) are completely unaffected in both loops — the existing pinned/mismatch/deleted-key checks apply to them exactly as before. |
| B2 | `bootstrap/tests/_ast_attest.py` | Module docstring (`:24-30` area, the `update_symbol` workflow description): short addition explaining the Import-exemption rationale, mirroring the existing per-module-necessity comment `_classify()` already carries (`:148-156`) — imports recurring across split modules are a per-module necessity, not injected/altered top-level logic, so pinning them by content hash buys no real security margin and is why the manifest went stale on ordinary commits. Notes explicitly (plan-review PR4) that `ast.Import` and `ast.ImportFrom` nodes share one `"Import:"` key prefix in this file's key-generation scheme (`_node_key`) — there is no separate `"ImportFrom:"` prefix in practice, so a reader shouldn't infer a distinction the key strings don't carry. |
| B3 | `bootstrap/tests/test_ast_attest.py` (extend) | Regression coverage per the proposal's own Evidence plan: (a) a synthetic fixture module with a fresh, unpinned `Import:*`-shaped NEW entry passes `update_symbol` cleanly (no `known_new` pin required) when it is the only NEW entry and no CHANGED/MISSING/DUPLICATE exists; (b) a synthetic fixture module with a fresh, unpinned `FunctionDef`/`ClassDef`/`Assign` NEW entry still refuses exactly as today (`REFUSED — ... new-symbol violation(s)`) — so the exemption cannot silently widen to cover named symbols later without this test catching it. |

## Acceptance criteria

* **Tests that must pass** — the extended `bootstrap/tests/test_ast_attest.py`
  (Chunk B3, both new cases). **Corrected per plan-review PR1:** the
  originally-planned `update-symbol install_onboarding --expect-old
  cec6f103797053c5 ... --dry-run` worked example (the exact call the
  sibling `first-session-survivability` plan's Chunk D needed) is
  **not usable as an acceptance check** — that pre-image digest was
  already resolved via direct-edit in that plan's own Chunk D, and
  `install_onboarding` currently shows **no** CHANGED state against
  the live baseline (`_classify()` confirms it), so the call refuses
  with "nothing to update" (exit 4) regardless of how well this plan's
  chunks are implemented. **Use a scratch demonstration instead:** copy
  `scaffold_ast_baseline.json` to a scratch path, hand-edit
  `install_onboarding`'s digest to a synthetic stale value (any
  differing 16-hex-char string), then run `update-symbol
  install_onboarding --baseline <scratch> --expect-old <the synthetic
  stale value> --known-new bootstrap/tests/fixtures/scaffold_ast_known_new.json
  bootstrap/_scaffold/*.py --dry-run` against the *real* module tree —
  this must succeed cleanly (exit 0, "DRY-RUN — no write"), proving
  Part 1 + Part 2 together actually restore the guarded path's
  usability against genuine drift, without depending on a live symbol
  that happens to currently show real drift (none currently does).
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

* **The scratch synthetic-drift `update-symbol` call above still
  refuses** after both chunks land → Part 1 or Part 2 has a real gap
  this plan's own preparation missed; do not proceed to declare
  success, re-derive from the actual refusal message. (Corrected per
  plan-review PR1: a refusal on the *real*, undrifted baseline against
  `install_onboarding` specifically is expected, not a signal — that
  symbol currently has nothing to update regardless of this plan.)
* **A future commit's ordinary import-line change trips `update_symbol`
  again** despite Part 2 → the predicate match is narrower than
  `_classify()`'s in some edge case (e.g. a key format mismatch) —
  re-diff the two predicates literally, don't assume equivalence.
* **The regenerated manifest's dropped `Import:*` keys turn out to be
  read by something else** (not just `update_symbol`) → re-grep for
  `scaffold_ast_known_new` across the whole tree before finalizing
  Chunk A, not just `_ast_attest.py`.

## Review

**Attribution / committer note.** Fresh-context subagent plan-review;
the subagent cannot commit, so the author-session commits this section
as a disclosed scribe, the accepted deviation model used throughout
this repo's lifecycle.

## Plan review -- Claude (Internal, fresh-context) -- 2026-07-31

**Model**: Claude Sonnet 5

**Steelman.** This is a well-scoped, well-fenced plan translating an already-litigated proposal into two concrete chunks. The Context section correctly reproduces both of the Decision's corrections, the scope fence is honored throughout (no edit to `scaffold_ast_baseline.json` anywhere in the plan; the one mention of that filename is a read-only `--baseline` argument to a `--dry-run` invocation), and the currency re-check and digest-transcription arithmetic — the two claims most likely to have silently rotted in nine days — both check out **exactly**, digit for digit, when independently reproduced. The core two-part design (drop `Import:*` pins, exempt them structurally) is not just plausible on paper; the reviewer built scratch copies of both chunks and confirmed by direct execution that the mechanism genuinely restores the guarded `update-symbol` path in a scenario with real drift, and that neither chunk alone is sufficient.

**Findings** (most significant first):

* **[PR1] The Acceptance Criteria's specific dry-run command cannot succeed, and will misdiagnose a healthy implementation as broken.** `install_onboarding`'s baseline digest is no longer `cec6f103797053c5` (that was the pre-image from `first-session-survivability`'s Chunk D handoff, already resolved via direct-edit) — it's now `382bfff5b2ace579`, and the *live* digest matches it exactly. `_classify()` reports `install_onboarding` as **not CHANGED**. The plan's literal command refuses with an `expect-old` mismatch (exit 3); corrected to the real digest, it still refuses because there's nothing to update (exit 4). None of the four allowlisted symbols currently show CHANGED state — the criterion is unsatisfiable against live repo state, no matter how well Chunks A/B are implemented, and the plan's own "Signals the change is wrong" would misdiagnose this refusal as a Part 1/2 gap.
  *Grounding:* `bootstrap/tests/fixtures/scaffold_ast_baseline.json` (`install_onboarding.digest` = `382bfff5b2ace579`); live `digest_module()` over `install.py` returns the identical digest; direct execution of the plan's literal command (exit 3) and the digest-corrected version (exit 4); `dev/plans/archive/first-session-survivability.md:225` (origin of the stale pre-image).
  *Suggested fix:* Replace the specific `install_onboarding` worked-example criterion with a scratch/synthetic-drift demonstration (inject a synthetic stale pre-image into a scratch baseline copy, confirm the dry-run then succeeds cleanly) — proving the mechanism works without depending on a live symbol that happens to currently show real drift. Amend "Signals the change is wrong" so a refusal on the *real* baseline isn't read as a gap.

* **[PR2] The `MISSING-KNOWN-NEW` loop has no Import/Docstring exemption — Part 2's "cannot drift apart again" claim currently holds only by convention, not by code.** Chunk B1 as written only patches the NEW-unpinned loop (`_ast_attest.py:299-308`). A second, separate loop (`:311-315`, `for k in sorted(set(allowed_new) - set(new))`) flags any *pinned* `known_new` key that's vanished from the live set, with **no exemption predicate at all**. Proven live: running the patched first-loop-only fix against the *current, unregenerated* 43-key manifest (still carrying 30 `Import:*` pins) in a synthetic-drift scenario produces four unguarded `MISSING-KNOWN-NEW Import:...` refusals. Chunk A's design (drop all 30 `Import:*` keys) sidesteps this immediately after implementation — with zero `Import:*` keys ever pinned, the second loop has nothing to flag — but that's a consequence of Chunk A's data choice, not a code guarantee; if anyone ever re-pins an `Import:`/`Docstring#`-prefixed key into the manifest in the future, the asymmetry resurfaces.
  *Grounding:* `_ast_attest.py:299-315` (both loops); direct execution showing 4 unguarded `MISSING-KNOWN-NEW Import:` refusals against the current manifest with only the first loop patched.
  *Suggested fix:* Apply the identical predicate inside the second loop too, so the exemption is symmetric and correct-by-construction regardless of what the manifest happens to contain, not dependent on Chunk A's data choice holding forever.

* **[PR3] The Docstring exemption predicate isn't literally identical to `_classify()`'s — currently unreachable, but the "exact literal predicate" framing overstates it.** `_classify()` exempts via `key.split("#", 1)[0] == "Docstring"`, matching both a bare `"Docstring"` key and any `"Docstring#N"`. The plan's proposed predicate, `k.startswith("Docstring#")`, does not match a bare `"Docstring"` key. Unreachable today (the baseline carries exactly one bare `"Docstring"` key, always already baselined, and the scope fence forbids touching the baseline) — but not literally the same predicate.
  *Grounding:* `_ast_attest.py:164` vs. the plan's B1 text; the baseline's one bare `"Docstring"` key, confirmed present.
  *Suggested fix:* Use `k.split("#", 1)[0] == "Docstring"` for true fidelity to the "exact literal predicate" claim, low priority given unreachability.

* **[PR4] The `"ImportFrom:"` branch of the proposed predicate is dead code (cosmetic).** `_node_key()` keys both `ast.Import` and `ast.ImportFrom` nodes under the same `"Import:"` prefix — there is no `"ImportFrom:"`-prefixed key anywhere in this codebase's key scheme, confirmed by enumerating all Import/ImportFrom nodes across `bootstrap/_scaffold/*.py` (57 `ImportFrom` + 16 `Import`, all keyed `"Import:"`). Harmless, but implies a distinction that doesn't exist in this file's key-generation scheme.
  *Suggested fix:* Optional one-line docstring note in B2 clarifying the key-string scheme collapses both AST types under one prefix.

* **[PR5] Minor: "carried forward verbatim" drops "and multiplicities."** The plan's ratified-condition bullet says "...copies those symbols' digests into the regenerated manifest," while the Decision's actual text says "...digests **and multiplicities**..." Immaterial to the outcome (the manifest format already stores multiplicity as a list per key), but worth exact quotation given this repo's own discipline around it.

**Coverage.** Independently verified: the full NEW-entry list (not just counts) against the proposal's table (zero drift, exact match); the manifest's key classification and digest values (30/13 split, 13/13 digest matches); both loops of `update_symbol()`'s NEW-handling logic by constructing and executing scratch copies of both chunks against the real live module set; the specific acceptance-criterion command, both as literally written and digest-corrected, against real current repo state; a synthetic-drift scenario proving the underlying design works when there's real drift to fix; that Chunk A alone and Chunk B alone are each individually insufficient. Not covered: re-deriving each of the 28 symbols' origin-commit attributions (already settled at the proposal's own Decision); the full `bootstrap/tests` suite (ran only `test_ast_attest.py`, 26/26 under canonical `lhm`, as a pre-implementation sanity baseline); B3's regression tests (don't exist yet — simulated via scratch scripts only).

**Verdict:** Proceed with the fixes above folded in. PR1 and PR2 are substantive and should be resolved before implementation — PR1 because the Acceptance Criteria as written cannot pass and would misdiagnose a correct implementation as broken; PR2 because Part 2's "cannot drift apart again" claim currently depends on an unenforced convention (never re-pinning an Import:/Docstring#-prefixed key) rather than code. Chunk A's transcription work and Chunk B's core design are independently confirmed sound — not a "start over" finding.

### Sharpening -- Claude (author) -- 2026-07-31

All five findings independently re-verified before disposing: re-ran
the exact `install_onboarding` digest comparison (confirmed
`382bfff5b2ace579` == live, not CHANGED); re-read both loops in
`update_symbol()` and confirmed the second loop's missing guard by
direct code read; re-confirmed the baseline's one bare `"Docstring"`
key and the `Import`/`ImportFrom` key-collapse via direct inspection.

* **[PR1] accept.** The Acceptance Criteria's worked-example command
  is replaced below with a scratch/synthetic-drift demonstration
  (inject a synthetic stale pre-image into a scratch copy of the
  baseline, confirm the dry-run then succeeds cleanly) — proving the
  mechanism without depending on a live symbol currently showing real
  drift. "Signals the change is wrong" corrected to not read a refusal
  against the *real*, undrifted baseline as a gap.
* **[PR2] accept.** Chunk B1 revised: the identical
  `Import:`/`ImportFrom:`/`Docstring#` predicate now applies inside
  **both** loops (the NEW-unpinned loop and the `MISSING-KNOWN-NEW`
  loop), so the exemption is correct-by-construction regardless of
  what the manifest contains, not dependent on Chunk A's "drop all
  Import: keys" choice holding forever.
* **[PR3] accept.** Chunk B1's Docstring check corrected to
  `k.split("#", 1)[0] == "Docstring"`, matching `_classify()` exactly
  rather than `k.startswith("Docstring#")`.
* **[PR4] accept, folded into B2.** The docstring addition now notes
  the `Import`/`ImportFrom` key-collapse explicitly.
* **[PR5] accept.** Ratified-condition bullet corrected to "digests
  and multiplicities."

**Status: open → executing.** All findings disposed; implementation
begins next (Chunks A-B).

## Code review

**Attribution / committer note.** Fresh-context subagent review of the
two implementation commits; the subagent cannot commit, so the
author-session commits this section as a disclosed scribe, the
accepted deviation model used throughout this repo's lifecycle.

## Code review -- Claude (sub-agent, fresh context, not the implementer) -- 2026-07-31

**Verdict: Accept**, applying to the two commits `a5d52af` (Chunk A)
and `e039f33` (Chunk B).

**Model**: Claude Sonnet 5, fresh session, no access to the
implementing session.

### Falsification ledger

**Chunk A.** `scaffold_ast_known_new.json` has exactly 28 keys, all
named-symbol type, zero `Import:`/`ImportFrom:` keys. Independently
recomputed the live digest for **all 28** symbols (not a sample) via
`_merge_current()` under the canonical `lhm` interpreter: 0 mismatches.
Diffed the pre-Chunk-A 43-key manifest against the new one: the 13
carried-forward named keys are byte-identical, 15 are genuinely new,
all 30 `Import:` keys dropped — exact match to the commit message.
`verify()` structurally cannot be affected by this change (it doesn't
accept a `known_new` argument at all) — confirmed by reading its
signature, then confirmed empirically: still 60 NEW entries as
informational notes.

**Chunk B — the most important part, and the most scrutinized.** The
Docstring predicate is `key.split("#", 1)[0] == "Docstring"`, a
literal character-for-character match to `_classify()`'s own predicate
(plan-review PR3, confirmed actually landed). The exemption guard is
present in **both** loops — the unpinned-NEW loop and the separate
`MISSING-KNOWN-NEW` loop (plan-review PR2's asymmetry, confirmed
genuinely closed in the shipped code by direct reading of both call
sites, not just the commit message's claim). Named symbols confirmed
unaffected by direct code reading and by test evidence.
**Non-vacuity proven by mutation, independently repeated by the
reviewer** (not just re-trusting the implementing session's own
mutation test): removing both guards reproduces exactly the two
predicted test failures with the exact refusal messages, the
named-symbol boundary test stays green; reverted, confirmed
byte-identical to HEAD via both `git diff` (0 lines) and
`git hash-object` matching `git rev-parse HEAD:...` exactly.

**Acceptance-criterion demonstration** reproduced independently
end-to-end under `lhm`: synthetic stale `install_onboarding` digest,
`update-symbol --dry-run` → exit 0, all 28 named symbols pinned and
matched, all 32 `Import:` entries exempted and unpinned — direct proof
Parts 1+2 together restore the guarded path.

**Scope fence** confirmed via `git diff-tree`: neither commit touches
`scaffold_ast_baseline.json` or `_UPDATE_ALLOWLIST`'s dict body.

**Gate sweep at HEAD**, all independently reproduced: full suite 1441
passed / 3 skipped / 2 failed (both failures independently confirmed
**pre-existing** — reproduced identically at the pre-Chunk-A commit,
`879176a`, before either chunk landed); canonical `lhm`
`test_ast_attest.py` 29/29; `check_cairn` OK (164 files); `claim_check`
clean on all four touched files; `quality_gate --sub neutrality`
unchanged at 99 FAILs.

### Coverage

Independently verified: full 28-name/28-digest cross-check (not a
sample) against the proposal's audit table; the `verify()`/
`update_symbol()` structural separation; both loops' guards by direct
code read plus live mutation testing (independently repeated, not
re-trusted); all three new tests' bodies and non-vacuity; the
acceptance demonstration end-to-end; the scope fence; the full gate
sweep including re-deriving that the 2 full-suite failures pre-date
this plan. Not re-covered: re-deriving the 28 symbols' origin-commit
provenance (already settled at the proposal's Decision, not reopened).

### Required follow-ups

None. Both substantive gaps the plan's own review caught in the
original design (PR2's loop asymmetry, PR3's Docstring predicate) are
genuinely present in the shipped code, proven by direct reading and
independent mutation testing, not merely asserted by commit messages.
Every numeric claim in both commit messages independently reproduced
exactly.

**Status: executing → review.** Code review clean, no follow-ups. No
Maintainer-gated closeout remains (`scaffold_ast_baseline.json`
untouched throughout — the scope fence held). Archive next.

## Lasting-truth migration

*Filled in at archive time. Per the [Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home
outside the plan — the supervised `scaffold_ast_baseline.json`
re-anchor stays the Maintainer-only, separately-tracked outstanding
act this proposal's scope fence explicitly excludes.*

This section is append-only once written.
