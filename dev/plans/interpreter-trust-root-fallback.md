<!-- claim-check-allow: dev/reviews/2026-07-22-interpreter-trust-root-security-review.md -->
<!-- The path above is a forward reference: the raw Security Review's committer
     note in the source proposal cites this artifact path; it is not this
     plan's own concern and may or may not exist -- carried only because the
     plan's Context section quotes proposal text that mentions it. -->

# Plan: interpreter trust root -- absent degrades, present-but-wrong refuses

**Source proposal**: `dev/proposals/archive/2026-07-22-claude-interpreter-trust-root-fallback.md`
**Status**: awaiting-plan-review
**Plan review**: required(**External**) -- the proposal's own header field,
carried unamended into the Decision ("Accepted, as reviewed and
conditioned"): "the floor is a fresh-context Internal read, and an External
(different-agent-type or human) read... this proposal *relaxes* a fail-closed
control on an executable trust root; it should not land on a same-type
read." Read as governing the *plan's* implementation gate (the proposal's own
Internal/External/Security-Review rounds are already complete and are not
what this line requires) -- consistent with how `lockfile-provenance-fields`
uses the identical header field. **This plan cannot proceed to implementation
on an Internal pass alone.**

## Context

The Decision (2026-07-22, Anthony Kendall) accepted the Revised C1-C4 design
"as reviewed and conditioned." Full detail:
`dev/proposals/archive/2026-07-22-claude-interpreter-trust-root-fallback.md`
-- its `## Revised proposal`, `## Security Review`, `## Response`, and
`## Decision` sections are authoritative. This is the most heavily reviewed
change in this session's queue: a 3-lens Internal panel (12 findings, 3
blocking) forced a full Response + Revised round; a cross-type External read
(Gemini) returned SHIP; a **dedicated Security Review** (Codex, a third agent
type, Maintainer-ordered) adjudicated the two risk-acceptance questions
neither prior tier was entitled to close, found one blocking record
correction (S1: the resolver is a *shape validator, not an authenticator*)
and one pre-existing non-blocking residual (S2: a symlink-walk check/use
race). The Decision accepted the design **subject to five binding
conspicuousness conditions** and **one required (not preferred) ordering
rule** -- both reproduced verbatim in Acceptance criteria below, since they
are not this plan's judgment calls to soften.

**Findings from this plan's own preparation, disclosed up front:**

1. **Every `lifecycle.py` line citation in the proposal has drifted by
   roughly five lines**, re-verified this session against the live tree (an
   unrelated edit landed between 2026-07-22 and now -- the accepted
   `first-session-survivability` F4 fix, which the proposal itself flagged as
   sharing the same file). Current, re-read locations used throughout this
   plan: `_warn` `:107`; `_intent_whoami` `:187-213` (swallow at `:198-200`);
   `_resolve_agent`/`_resolve_session` `:218-287`; `_sibling_tool`
   `:288-292`; `_has_symlink_component` `:320-333`; `_resolve_interpreter`
   `:336-395`; `cmd_session_start` `:634` (resolver call `:703`);
   `_do_full_handoff` `:1130` (resolver call `:1160`); `main` `:1270-1281`
   (catches only `LifecycleError`, unchanged). `bootstrap/tests/
   test_lifecycle_failsafe.py`'s own citations, by contrast, are **exact** --
   re-verified line-for-line (`_make_exe` `:255-260`, the parametrize
   `:240-245`, `test_space_in_interpreter_path_accepted` `:263-275`,
   `test_extra_key_in_local_env_refused` `:278-287`, the monkeypatch pattern
   `:297-300` -- no drift there at all).
2. **The self-hosted copy is still byte-identical, re-verified.** `shasum -a
   256` on both `templates/skills/_lib/lifecycle.py` and `tools/lifecycle.py`
   → `6f6333ee3a5c0d53f8278601ccfdd0867f749452ac02d63faba6ccb32e46d852`,
   matching both the `hash` and `base_hash` recorded at `dev/.cairn/
   cairn-lock.yml:546-549` exactly. No unrelated drift to reconcile before
   this plan's own edit lands.
3. **The Security Review's governance-registration follow-up is already
   done -- landed independently, outside this plan's lifecycle.** `AGENTS.md`
   now carries "**The local interpreter binding**" as a fifth high-risk
   surface (`:296-303`, `git blame` → commit `91c96b4`, "AGENTS.md: register
   the interpreter trust boundary as a high-risk surface," committed directly
   by the Maintainer today, 2026-07-31, citing this exact proposal's Security
   Review). **This plan's own follow-up-homing work is therefore only for
   S2** (the check/use race), not governance registration -- that box is
   already checked.
4. **The full suite baseline under the canonical `lhm` interpreter (Python
   3.13.13) is 0 failed / 1446 passed / 0 skipped**, re-verified this
   session, consistent with the same canonical figure independently
   re-derived for the sibling `lockfile-provenance-fields` plan today. The
   proposal's own honest baseline (3 failed / 1408 passed / 3 skipped) was
   measured on the non-canonical Python 3.12.9 sandbox and is stale on two
   counts: the two `test_ast_attest.py` artifacts are canonical-clean, and
   the `test_evolution_infer.py` clock-dependent failure was independently
   fixed earlier this session (commit `0bfba10`).
5. **The gate manifest's pinned `collection.node_count` (1404) has drifted
   further from the live tree (now 1446 collected, up from the proposal's
   own already-stale 1414) -- reconfirming, not merely repeating, the
   proposal's own conclusion that no gate-manifest-anchored batch is
   currently live.** This does not change the operative consequence: `
   bootstrap/tests/test_lifecycle_failsafe.py` is in the pinned 147-entry
   `frozen_files` set regardless (`bootstrap/tests/fixtures/
   gate_manifest.json`, re-verified this session), and `_gate_manifest.py`
   HOLDs on *any* edit to a frozen file independent of whether a batch is
   live -- so Chunk F's test rewrite routes through the supervised re-anchor
   path unconditionally, exactly as the proposal's R5/S5 exchange concluded.
6. **`bootstrap/tests/_gate_reanchor.py` exists and is a structurally
   different, heavier mechanism than the AST-baseline direct-edit pattern
   used on every prior sibling plan this session.** It is a cryptographically
   anchored **two-stage** ceremony: Stage A (`gather_evidence`) executes
   candidate code in an isolated, credential-scrubbed temp tree and emits a
   non-authoritative evidence bundle; Stage B (`promote_data_only`) re-derives
   everything from trusted git objects at the immutable anchor, executes
   **no candidate code**, and atomically advances one designated trusted ref
   via an expected-old compare-and-swap -- "the Maintainer's supervised act,"
   per the tool's own module docstring. Chunk G below is scoped to `prepare`
   only; `promote` is explicitly not this plan's or any implementing agent's
   act.

**Everything else in the Revised proposal + Security Review + Decision is
taken as settled** -- the C1-C4 code design, the S1 record correction's
exact language, the required probe ordering, the five binding conspicuousness
conditions, the test list, and the two named follow-ups (S2, governance --
the latter now closed per Finding 3 above). This plan does not re-litigate
any of it.

### Documentation / doctrine surface

Per the proposal: shipped-tool docstrings only (the resolver's contract
paragraph, the stale `:370-374`-region comment, the module docstring of the
test file). No `doctrine/` change, no further `AGENTS.md` change (the one
follow-up that would have touched it is already landed, Finding 3). A
`CHANGELOG.md` entry is deferred to the next goodnight-routine scrub per
`AGENTS.md`'s shared-communication-file rule, not a chunk of this plan.

## Sequence

```
A. C1(revised)+C1a -- _probe_interpreter classifier, _REBIND_REMEDY, R6 guard   [commit pending]
B. C2(revised) -- _warn_stale_once, docstring source-value update              [commit pending]
C. C3 -- _intent_whoami surfaces the swallowed refusal                        [commit pending]
D. C4 -- _REBIND_REMEDY appended to the fatal messages                        [commit pending]
E. The S1 record correction -- resolver docstring rewritten verbatim to spec  [commit pending]
F. Tests -- bootstrap/tests/test_lifecycle_failsafe.py (FROZEN, rewritten)    [commit pending]
G. Supervised gate-manifest re-anchor: prepare (Maintainer promotes)          [parked]
H. Self-host sync: tools/lifecycle.py + cairn-lock.yml hash refresh          [commit pending]
```

`dev/PLANNING.md`'s deferred row for S2 (the check/use race) lands **now, at
plan-open** -- see below, committed in the same commit as this plan.

### Chunk A -- C1(revised) + C1a (the classifier, the remedy constant, R6)

| # | File | Change |
|---|------|--------|
| A1 | `templates/skills/_lib/lifecycle.py` | New `_probe_interpreter(interp: Path) -> str` helper (returns `"symlinked"` / `"absent"` / `"present"`), placed immediately above `_resolve_interpreter`. Wraps the **whole** classification -- the symlink walk *and* the `stat()` probe -- so the caller's `except OSError` is reachable for both; wrapping only the probe was disproven by execution at the Internal panel's R2(a) (an EACCES parent raises inside the symlink walk, before the probe is ever reached). |
| A2 | `templates/skills/_lib/lifecycle.py` | New module-level constant `_REBIND_REMEDY`, exact text from the Revised proposal's C1a block -- delete-then-reinstall, explicit **never** `--force`, explicit that a bare delete alone leaves the fallback in place. Single source so C1's warning and both C4 fatals cannot drift apart. |
| A3 | `templates/skills/_lib/lifecycle.py` | Insert the R6 relative-segment guard (`any(part in ("..", ".") for part in interp.parts)`) **before** the classifier call, so `..`/`.` segments raise `LifecycleError` rather than reach `_probe_interpreter` at all -- makes the docstring's "no relative segments" clause true rather than leaving it aspirational. |
| A4 | `templates/skills/_lib/lifecycle.py` | Replace the current tail of `_resolve_interpreter` (`:380-395` in the live tree, i.e. from the `is_absolute()` check through the return) with the Revised proposal's dispatch on `_probe_interpreter`'s three outcomes: `symlinked` → fatal (symlink message + `_REBIND_REMEDY`); `absent` → `_warn_stale_once(...)` then `return sys.executable, "fallback-stale"`; `present` → the existing `is_file()`/`os.access(X_OK)` check, fatal message now carrying `_REBIND_REMEDY`. `except OSError` around the classifier call raises `LifecycleError` with `_REBIND_REMEDY` appended (the R2(a) EACCES fix). `LifecycleError` subclasses `RuntimeError` (`:107` region), not `OSError` -- verify this by inspection before relying on it, since the `except OSError` block must not swallow a symlink refusal raised through the same call. |

### Chunk B -- C2(revised) (once-per-process warning)

| # | File | Change |
|---|------|--------|
| B1 | `templates/skills/_lib/lifecycle.py` | `_warn_stale_once(message)`: a module-level sentinel (e.g. `_STALE_WARNED: bool`) guarding a single `_warn` call, since the resolver is reached up to four times in one `session-end --handoff` (R4's measured chain: `_intent_whoami` `:198`, `cmd_session_start` `:703`, `_do_reflection`→`_resolve_agent`/`_resolve_session`, `_do_full_handoff` `:1160`). Return type of `_resolve_interpreter` stays `Tuple[str, str]` (preserves `test_space_in_interpreter_path_accepted`); source token stays `"fallback-stale"`. |
| B2 | `templates/skills/_lib/lifecycle.py` | Docstring's "Returns... source is `"local-env.json"` or `"fallback"`" gains the third value, `"fallback-stale"`. |

### Chunk C -- C3 (`_intent_whoami` stops swallowing silently)

| # | File | Change |
|---|------|--------|
| C1t | `templates/skills/_lib/lifecycle.py` | The `except LifecycleError` swallow at `:199-200` gains a `_warn` naming the caught refusal's message *before* falling back to `sys.executable` -- per the Security Review's "pre-existing fail-open ruling": non-fatal fallback stays acceptable (optional tool, repo-controlled script, same interpreter already running), **conditioned on** surfacing the original refusal reason first. |
| C2t | `templates/skills/_lib/lifecycle.py` | Resolver docstring's "Any violation refuses before running anything" corrected to name this one non-fatal exception explicitly, rather than asserting a universal guarantee the code does not have. |

### Chunk D -- C4 (recovery guidance on messages that stay fatal)

| # | File | Change |
|---|------|--------|
| D1 | `templates/skills/_lib/lifecycle.py` | `_REBIND_REMEDY` appended to: the symlink-refusal message, the not-an-executable-file message, the new relative-segment message (A3), and the new EACCES/uninspectable-path message (A4's `except OSError` branch). No disposition changes anywhere in this chunk -- guidance only. |

### Chunk E -- the S1 record correction (Decision-mandated, verbatim in substance)

| # | File | Change |
|---|------|--------|
| E1 | `templates/skills/_lib/lifecycle.py` | `_resolve_interpreter`'s docstring trust-root paragraph rewritten to the Decision's on-the-record correction: `dev/.cairn/local-env.json` is an **operationally trusted executable binding**, untracked/gitignored/not lockfile-covered, and `_resolve_interpreter` is a strict **shape validator, not an authenticator** -- it checks neither Python identity nor binary provenance, and accepts any absolute, present, non-symlinked, executable regular file. This is not optional prose-polish: it is the specific correction the Security Review made blocking, and the Decision quotes it as "on the record." Land it in substance, not as a paraphrase that could soften it. |
| E2 | `templates/skills/_lib/lifecycle.py` | The stale comment near the old `is_file()` check (the one claiming an appended-argument string "is caught by the `is_file()` check below") corrected -- under the revised classifier such a string is an absent *path* and degrades, per R2/R6's discussion. |
| E3 | `templates/skills/_lib/lifecycle.py` | Threat-model-adjacent note (R7): the docstring's stdlib-only safety rationale is scoped to *this tool*, not the sub-tools the resolved interpreter runs -- one sentence, not a new section (the full threat-model argument lives in the proposal's record, not duplicated into shipped-tool prose). |

### Chunk F -- tests (`bootstrap/tests/test_lifecycle_failsafe.py`, FROZEN, rewritten)

| # | Change |
|---|--------|
| F1 | `test_tampered_local_env_refuses` (`:240-252` live): relocate the two absent-path values (`/usr/bin/python --foo`, `/no/such/python`) out; replace with a present-non-executable regular file and a present directory, materialized in the test body via a non-id-representable sentinel (module-level parametrize values cannot use the `repo` fixture, and `_make_exe` at `:255` is defined *below* the decorator). Pin `ids=["bad0","bad1","bad2","bad3"]` explicitly on the decorator -- R5's empirically-verified fix (an all-dict-except-one-string list silently drops a node from collection; the explicit `ids=` avoids depending on parametrize-value shape). |
| F2 | New `test_stale_interpreter_path_degrades_with_guidance`, parametrized over the two relocated values: `rc == 0`, `(from fallback-stale)` on stdout, `_REBIND_REMEDY`'s text on stderr. |
| F3 | New `test_stale_warning_fires_once_per_process` (R4's count fix, not presence): a full `session-end --handoff` with an `intent.py` sibling present (monkeypatch `_sibling_tool`, per F6) and `CAIRN_AGENT`/`CAIRN_SESSION` **unset** (the real multi-call shape the `repo` fixture's `CAIRN_AGENT=owner` would otherwise mask) asserts **exactly one** occurrence of the remedy string in captured stderr, not merely its presence. |
| F4 | New `test_stale_binding_is_not_rewritten`: `local-env.json` bytes identical before/after a degraded run (R11's note: the resolver contains no write path today, so this is a forward regression guard against the explicitly-rejected auto-rebind alternative, not a guard against a present mechanism -- label it as such in the test docstring). |
| F5 | New `test_uninspectable_interpreter_path_refuses`: an unreadable-parent (mode-000) path raises `LifecycleError` via the classifier's `except OSError`, root/non-POSIX skip-guarded. Valid against the *revised* guard only (R2(a)'s falsification was against the naive single-probe version). |
| F6 | New `test_symlinked_parent_with_absent_leaf_still_refuses` and `test_symlinked_leaf_refuses` (R3): a real dir, a symlink to it, binding pointed at `<symlink>/python` where `python` does not exist → `LifecycleError`; and a symlinked leaf directly → `LifecycleError`. Pins the required probe ordering (symlink walk before absence classification) as an actual enforced test, not an asserted-but-untested invariant. |
| F7 | New `test_tampered_binding_warns_in_intent_whoami` (C3): a present-but-wrong binding produces a warning on stderr instead of silence; `_intent_whoami` still returns non-fatally (`None`). Requires monkeypatching `_sibling_tool` per the existing pattern at `:297-300` (R4c) -- `_intent_whoami` returns early at `:193`-ish without it. |
| F8 | New resolver source-scan test in the spirit of `bootstrap/tests/test_lifecycle_contract.py:139-148` (which scans the *planner*, `lifecycle_planner.py` -- a pattern to copy, not an existing guard covering this module, per R11's precision correction): assert the resolver's source contains no write primitive against the state directory. |
| F9 | Module docstring (`:16-19`) reworded from "a tampered config refuses before running anything" to the two-branch posture. |
| F10 | Must stay green, byte-unchanged in assertion shape: `test_interpreter_resolved_from_local_env_and_reported`, `test_absent_local_env_uses_fallback_with_guidance`, `test_space_in_interpreter_path_accepted`, `test_extra_key_in_local_env_refused`. |

### Chunk G -- supervised gate-manifest re-anchor (Maintainer-gated; `prepare` only)

**Not the AST-baseline direct-edit pattern** used on every other plan this
session -- `test_lifecycle_failsafe.py` is a `bootstrap/tests/` FROZEN file
under `bootstrap/tests/_gate_manifest.py`'s `frozen_files` set, a
structurally different control from `scaffold_ast_baseline.json`'s symbol
digests (which this proposal never touches -- no `bootstrap/_scaffold/` edit
means no AST re-anchor at all, confirmed by the proposal and re-confirmed
this session). The applicable mechanism is `bootstrap/tests/
_gate_reanchor.py`'s two-stage contract: `gather_evidence` (Stage A,
executable, non-authoritative, isolated temp tree) then `promote_data_only`
(Stage B, data-only, authoritative, git-plumbing CAS ref advance). This
implementing agent runs **`prepare`** only -- Stage A+B through data-only
validation, no ref advance -- once Chunks A-F land and their real diff is
known. **`promote`** (the ref-advance CAS) is explicitly the Maintainer's
supervised act per the tool's own module docstring; this plan does not
attempt it.

### Chunk H -- self-host sync

| # | Change |
|---|--------|
| H1 | Copy the edited `templates/skills/_lib/lifecycle.py` to `tools/lifecycle.py` verbatim (the `config.py:211` `verbatim: true` mapping). |
| H2 | Refresh `dev/.cairn/cairn-lock.yml:546-549`'s `hash` and `base_hash` for the `tools/lifecycle.py` entry to the new sha256 -- a **hash refresh for one changed file**, not a lockfile-schema change (R9). Named explicitly, per R9: hand-edit the two lines (matching the precedent this session already used for hash-only corrections), not `scaffold.py upgrade --target .` -- the latter is a full upgrade-stage/apply cycle with its own stage-metadata and backfill semantics that this single-entry refresh does not need and would pull in unrelated machinery for. Flagged for the required External reviewer to confirm this choice, since R9 asked the plan to justify it, not merely state it. |
| H3 | `python bootstrap/verify_integrity.py --target .` run **before** H1/H2 (must already be clean) and **after** (must still be clean) -- promoted from a smoke check to a required plan step, per R9. |
| H4 | One-line byte-identity assertion (`shasum -a 256` on both copies, equal) added to the plan's own verification block below, since no automated test ties `tools/lifecycle.py` to the template. |

## Acceptance criteria

**Binding conspicuousness conditions** (from the Security Review's sign-off,
quoted in the Decision as acceptance conditions, not design preferences --
each maps to a specific Chunk F test):
* Exactly one stderr warning per process (F3).
* The stale recorded value **and** the substituted interpreter both named in
  that warning (F2's stdout/stderr assertions).
* The source reported as `fallback-stale` (F2).
* Actionable, non-`--force` recovery guidance (F2, via `_REBIND_REMEDY`'s
  fixed text).
* No automatic rewrite of the binding (F4).

**Required probe ordering** (not preferred -- the symlink walk runs first,
then absence classification, both inside one `except OSError`): enforced by
F6, and by Chunk A's `_probe_interpreter` structure itself.

**Other criteria:**
* **Tests that must pass** -- `bootstrap/tests/test_lifecycle_failsafe.py`
  in full (Chunk F, all nodes, old and new). Full `python -m pytest
  bootstrap/tests`, canonical `lhm` interpreter, at **0 failed / (1446 + new
  node count) passed / 0 skipped** -- today's re-verified baseline (Finding
  4 above); re-derive fresh at implementation time, don't copy.
* **3.11 / 3.13 disposition parity (R2b's plan-execution prerequisite)** --
  the Security Review already executed the full classifier matrix on
  3.11.15, 3.12.9, and 3.13.13 and confirmed agreement on every disposition
  (absent, `ENOTDIR`, symlinked-parent, unreadable-parent, delete/recreate,
  present-then-delete); this plan's own implementation re-confirms on
  whatever interpreters are available on the implementing host and records
  which were and were not re-run, rather than re-asserting the Security
  Review's figures as this session's own.
* **S1 record correction present** -- Chunk E1's docstring text is checked
  against the Decision's verbatim correction, not merely "some correction
  landed."
* **Gate-manifest re-anchor** -- Chunk G's `prepare` step succeeds through
  data-only validation (no HOLD); `promote` is explicitly deferred to the
  Maintainer.
* **Self-host verification** -- H3's before/after `verify_integrity.py`
  runs, both clean; H4's byte-identity assertion holds.
* **Bandit / security lint** -- `python -m pytest
  bootstrap/tests/test_security_lint.py` green; the new code adds no
  subprocess/eval/deserialization surface.
* **Docs** -- `python scripts/check_cairn.py` and `python
  scripts/claim_check.py` clean over this plan and every touched/new file.
* **Smoke** -- the two-line manual repro from the proposal's Evidence
  section: point `local-env.json` at a deleted path, run `python
  tools/lifecycle.py session-start`, confirm warn + remedy + exit 0; point it
  at a present non-executable file, confirm refuse + exit 1.

## Signals the change is wrong

Carried forward from the proposal's own list, unchanged: an adopter running
for weeks on `fallback-stale` without noticing (recovery: escalate
surfacing, or fall back to guidance-only per the proposal's Alternative 2);
a Security-Review-unmodeled shape where absence itself is attacker-
influenced (recovery: Alternative 2, deleting only Chunks A/B/D); the
relocated test cases turning out to still need to refuse regardless of
existence (recovery: a targeted raw-string check, re-litigating
`test_space_in_interpreter_path_accepted`); C3's warning firing noisily on
a normal reflection-only `session-end` (recovery: one line, trivially
reverted); the self-host sync causing unanticipated lockfile churn
(recovery: revert the `tools/lifecycle.py` sync, land the template change
alone, documented divergence until the next full upgrade pass). Add one
from this plan's own preparation: **`_gate_reanchor.py prepare` reports a
diff wider than the test file's own intended rewrite** -- the plan's own
edits touched something unintended; do not hand off `promote` until the
Stage A evidence bundle's diff matches exactly what Chunks A-F actually
changed.

## Review

*Filled in after the fresh-context Internal plan-review subagent pass, and
separately after the required External read this plan's own declared tier
mandates before implementation.*

## Code review

*Filled in after implementation commits land (Chunks A-H).*

## Lasting-truth migration

*Filled in at archive time. Per the [Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home outside
the plan -- S2 (the check/use race) is homed at this plan's own open, at its
`dev/PLANNING.md` Queued row (see below); the governance-registration
follow-up needs no home here, since it already landed independently
(Finding 3, this plan's Context).*

This section is append-only once written.
