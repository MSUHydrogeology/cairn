<!-- claim-check-allow: dev/reviews/2026-07-22-interpreter-trust-root-security-review.md -->
<!-- The path above is a forward reference: the raw Security Review's committer
     note in the source proposal cites this artifact path; it is not this
     plan's own concern and may or may not exist -- carried only because the
     plan's Context section quotes proposal text that mentions it. -->
<!-- claim-marker maintenance 2026-07-31: this file's own Response section cites
     `dev/plans/lockfile-provenance-fields.md` -- ACCURATE when written (that
     sibling plan's own pre-archive path). Archiving that plan (git mv to
     dev/plans/archive/, a separate commit) breaks the citation here. Retained
     unedited (append-only, response prose); path marked so the checker clears. -->
<!-- claim-check-allow: dev/plans/lockfile-provenance-fields.md* -->

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
   plan: `_warn` `:107`; `_intent_whoami` `:187-213` (swallow `try`/`except`
   at `:199-202`); `_resolve_agent`/`_resolve_session` `:218-287`;
   `_sibling_tool` `:288-297`; `_has_symlink_component` `:320-333`;
   `_resolve_interpreter` `:336-396` (its `is_absolute()` guard at `:385`,
   the appended-argument comment at `:375-379`); `cmd_session_start` `:634`
   (resolver call `:703`); `_do_full_handoff` `:1130` (resolver call
   `:1160`); `main` `:1270-1281` (catches only `LifecycleError`, unchanged).
   **Corrected at plan-review (PR3/PR4/PR5/PR8/PR9, Internal, substantive
   and minor):** this plan's own first draft applied the ~5-line drift
   inconsistently — some spans re-derived correctly, others still carried a
   pre-drift or otherwise wrong number (the classifier-dispatch tail
   `:380-395`→`:385-396`; the `_intent_whoami` swallow `:198-200`→`:199-202`;
   `_sibling_tool` `:288-292`→`:288-297`; the appended-argument comment
   `:370-374`→`:375-379`) — corrected above and at every chunk citing them,
   listed by chunk below. `bootstrap/tests/test_lifecycle_failsafe.py`'s own
   citations, by contrast, are **exact** — re-verified line-for-line
   (`_make_exe` `:255-260`, the parametrize `:240-245`,
   `test_space_in_interpreter_path_accepted` `:263-275`,
   `test_extra_key_in_local_env_refused` `:278-287`, the monkeypatch pattern
   `:297-300` -- no drift there at all).
2. **The self-hosted copy is byte-identical, re-verified — but the
   lockfile record is not the clean match this finding originally claimed.**
   `shasum -a 256` on both `templates/skills/_lib/lifecycle.py` and
   `tools/lifecycle.py` → `6f6333ee3a5c0d53f8278601ccfdd0867f749452ac02d63faba6ccb32e46d852`,
   matching the entry's `hash` field exactly. **Corrected at plan-review
   (PR2, Internal, blocking):** the entry's `base_hash`
   (`dev/.cairn/cairn-lock.yml:545`, corrected range from `:546-549`) does
   **not** match — it is still `sha256:296ef88b...`, the *pre-drift*,
   *pre-`first-session-survivability`* value. Per `lockfile.py`'s own
   fork-detection semantics (`hash != base_hash` → "forked from upstream,"
   `:258-280`), this record currently reads as a silent fork even though
   the two files are verified byte-identical right now. This inconsistency
   **predates this plan** (it was introduced when `first-session-
   survivability`'s F4 edit resynced `hash` without anyone refreshing
   `base_hash` to match) and is not this plan's to have caused — but Chunk
   H2's refresh (below) corrects it as a side effect, and that should be
   named explicitly rather than left implicit in "a hash refresh for one
   changed file."
3. **The Security Review's governance-registration follow-up is already
   done -- landed independently, outside this plan's lifecycle.** `AGENTS.md`
   now carries "**The local interpreter binding**" as a fifth high-risk
   surface (heading `:304`, bullet `:319-327` — **corrected at plan-review,
   PR5, Internal, substantive, from this finding's original `:296-303`**,
   which matched neither the source proposal's own unrelated pre-session
   citation nor the file's state after either of two same-day edits;
   `git blame` → commit `91c96b4`, "AGENTS.md: register the interpreter
   trust boundary as a high-risk surface," committed directly by the
   Maintainer today, 2026-07-31, citing this exact proposal's Security
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
   per the tool's own module docstring. **Corrected at plan-review (ETR1,
   External/Codex, blocking process; sequencing and delta mechanics
   corrected again at ETR1-R2):** Chunk G below splits into a **G0**
   pre-Chunk-A Maintainer prerequisite (resolve the inherited gate-anchor
   drift, establish a concrete `P`) and a **G1** post-Chunk-H Maintainer
   handoff (identify the actual final commit `C` and the correct
   whole-candidate `P`→`N` delta). Neither `prepare` nor `promote` is this
   plan's or any implementing agent's act at either step;
   `refs/cairn/gate-authorization` does not exist today, and `prepare`
   itself (not only `promote`) requires it, per direct execution this
   session.

**Everything else in the Revised proposal + Security Review + Decision is
taken as settled** -- the C1-C4 code design, the S1 record correction's
exact language, the required probe ordering, the five binding conspicuousness
conditions, the test list, and the two named follow-ups (S2, governance --
the latter now closed per Finding 3 above). This plan does not re-litigate
any of it.

### Documentation / doctrine surface

Per the proposal: shipped-tool docstrings only (the resolver's contract
paragraph, the `:375-379`-region comment — **corrected at plan-review, PR8,
Internal, substantive, from this section's original `:370-374`**, the module
docstring of the test file). No `doctrine/` change, no further `AGENTS.md`
change (the one follow-up that would have touched it is already landed,
Finding 3). A `CHANGELOG.md` entry is deferred to the next goodnight-routine
scrub per `AGENTS.md`'s shared-communication-file rule, not a chunk of this
plan.

**S3 carried forward, per plan-review (PR7, Internal, substantive).** The
Decision's third named follow-up — "native Windows execute semantics remain
unverified... the present-but-non-executable leg is not claimed as a
cross-platform verified guarantee" — was absent from this plan's first
draft (S2 got its `dev/PLANNING.md` row; governance was marked already done;
S3 was simply never mentioned). It carries forward unchanged as an explicit
residual: this plan touches no Windows-specific code path, `os.access(...,
os.X_OK)` is unmodified by any chunk here, and no chunk adds a Windows test
— so no action in this plan closes it, and none is owed. Recorded here
rather than left to be inferred.

## Sequence

```
G0. [Maintainer prerequisite, BEFORE Chunk A] Resolve inherited gate-anchor  [parked]
    drift (234 files), establish a concrete pre-implementation P
A.  C1(revised)+C1a -- _probe_interpreter classifier, _REBIND_REMEDY, R6 guard [commit pending]
B.  C2(revised) -- _warn_stale_once, docstring source-value update            [commit pending]
C.  C3 -- _intent_whoami surfaces the swallowed refusal                      [commit pending]
D.  C4 -- _REBIND_REMEDY appended to the fatal messages                      [commit pending]
E.  The S1 record correction -- resolver docstring rewritten verbatim to spec [commit pending]
F.  Tests -- bootstrap/tests/test_lifecycle_failsafe.py (FROZEN, rewritten)  [commit pending]
H.  Self-host sync: tools/lifecycle.py + cairn-lock.yml hash refresh         [commit pending]
G1. [Maintainer handoff, AFTER Chunk H] C = final commit, expected P->N      [parked]
    delta = all four code files + this plan document + generated
    gate_manifest.json (five files, not four -- ETR1-R3)
```
**Corrected at plan-review (ETR1-R2, External/Codex, blocking process;
file count corrected again at ETR1-R3):**
G0 now precedes Chunk A (a precondition, not parallel work) and G1 now
follows Chunk H (its candidate `C` cannot be "the final implementation
commit" while H is still pending) -- the prior draft placed the whole re-
anchor step between F and H, self-contradicting its own "final commit"
framing.

`dev/PLANNING.md`'s deferred row for S2 (the check/use race) lands **now, at
plan-open** -- see below, committed in the same commit as this plan.

### Chunk A -- C1(revised) + C1a (the classifier, the remedy constant, R6)

| # | File | Change |
|---|------|--------|
| A1 | `templates/skills/_lib/lifecycle.py` | New `_probe_interpreter(interp: Path) -> str` helper (returns `"symlinked"` / `"absent"` / `"present"`), placed immediately above `_resolve_interpreter`. Wraps the **whole** classification -- the symlink walk *and* the `stat()` probe -- so the caller's `except OSError` is reachable for both; wrapping only the probe was disproven by execution at the Internal panel's R2(a) (an EACCES parent raises inside the symlink walk, before the probe is ever reached). |
| A2 | `templates/skills/_lib/lifecycle.py` | New module-level constant `_REBIND_REMEDY`, exact text from the Revised proposal's C1a block -- delete-then-reinstall, explicit **never** `--force`, explicit that a bare delete alone leaves the fallback in place. Single source so C1's warning and both C4 fatals cannot drift apart. |
| A3 | `templates/skills/_lib/lifecycle.py` | Insert the R6 parent-traversal guard (`".." in interp.parts`) **before** the classifier call, so a `..` segment raises `LifecycleError` rather than reach `_probe_interpreter` at all. **Narrowed at plan-review (ETR4, External/Codex, substantive; response re-confirmed absent from the operative row at ETR4-R2 -- fixed here, this time verified landed by direct re-read after edit):** the original guard also checked for a bare `"."` component, but `Path(value).parts` already discards `.` at construction (executed on both 3.11.15 and 3.13.13 -- `Path("/a/./python").parts` never contains `"."`), so that half of the check is dead code. The guard's error message and the docstring's "no relative segments" claim are both narrowed to the security-relevant case, parent traversal (`..`), which *is* live and detected. F5b adds the direct resolver regression proving this. |
| A4 | `templates/skills/_lib/lifecycle.py` | Replace the current tail of `_resolve_interpreter` (`:385-396` in the live tree — **corrected at plan-review, PR3, Internal, substantive, from this row's original `:380-395`**; the `is_absolute()` check is at `:385`, the final `return` at `:396`, an off-by-five-and-zero mix rather than a consistent drift) with the Revised proposal's dispatch on `_probe_interpreter`'s three outcomes: `symlinked` → fatal (symlink message + `_REBIND_REMEDY`); `absent` → `_warn_stale_once(...)` then `return sys.executable, "fallback-stale"`; `present` → the existing `is_file()`/`os.access(X_OK)` check, fatal message now carrying `_REBIND_REMEDY`. `except OSError` around the classifier call raises `LifecycleError` with `_REBIND_REMEDY` appended (the R2(a) EACCES fix). `LifecycleError` subclasses `RuntimeError` (`:107` region), not `OSError` -- verify this by inspection before relying on it, since the `except OSError` block must not swallow a symlink refusal raised through the same call. |

### Chunk B -- C2(revised) (once-per-process warning)

| # | File | Change |
|---|------|--------|
| B1 | `templates/skills/_lib/lifecycle.py` | `_warn_stale_once(message)`: a module-level sentinel (e.g. `_STALE_WARNED: bool`) guarding a single `_warn` call, since the resolver is reached up to four times in one `session-end --handoff` (R4's measured chain: `_intent_whoami` `:200` — **corrected at plan-review, PR4, Internal, substantive, from this row's original `:198`, which is the unrelated early-return line** — `cmd_session_start` `:703`, `_do_reflection`→`_resolve_agent`/`_resolve_session`, `_do_full_handoff` `:1160`). Return type of `_resolve_interpreter` stays `Tuple[str, str]` (preserves `test_space_in_interpreter_path_accepted`); source token stays `"fallback-stale"`. |
| B2 | `templates/skills/_lib/lifecycle.py` | Docstring's "Returns... source is `"local-env.json"` or `"fallback"`" gains the third value, `"fallback-stale"`. |

### Chunk C -- C3 (`_intent_whoami` stops swallowing silently)

| # | File | Change |
|---|------|--------|
| C1t | `templates/skills/_lib/lifecycle.py` | The `except LifecycleError` swallow (`try:`/call/`except`/fallback at `:199-202` — **corrected at plan-review, PR4, Internal, substantive, from this row's original `:199-200`, which stopped short of the `except` clause and the fallback assignment it names**) gains a `_warn` naming the caught refusal's message *before* falling back to `sys.executable` -- per the Security Review's "pre-existing fail-open ruling": non-fatal fallback stays acceptable (optional tool, repo-controlled script, same interpreter already running), **conditioned on** surfacing the original refusal reason first. |
| C2t | `templates/skills/_lib/lifecycle.py` | Resolver docstring's "Any violation refuses before running anything" corrected to name this one non-fatal exception explicitly, rather than asserting a universal guarantee the code does not have. |

### Chunk D -- C4 (recovery guidance on messages that stay fatal)

| # | File | Change |
|---|------|--------|
| D1 | `templates/skills/_lib/lifecycle.py` | `_REBIND_REMEDY` appended to: the symlink-refusal message, the not-an-executable-file message, the new parent-traversal message (A3 -- **"relative-segment" corrected to "parent-traversal" at plan-review, ETR4-R2, External/Codex, matching A3's own narrowing**), and the new EACCES/uninspectable-path message (A4's `except OSError` branch). No disposition changes anywhere in this chunk -- guidance only. |

### Chunk E -- the S1 record correction (Decision-mandated, verbatim in substance)

| # | File | Change |
|---|------|--------|
| E1 | `templates/skills/_lib/lifecycle.py` | `_resolve_interpreter`'s docstring trust-root paragraph rewritten to the Decision's on-the-record correction: `dev/.cairn/local-env.json` is an **operationally trusted executable binding**, untracked, gitignored, **mutable**, and not lockfile-covered (**"mutable" restored at plan-review, PR10, Internal, minor — this row's original compression to "untracked/gitignored/not lockfile-covered" dropped one word of the Decision's verbatim four-adjective list; no other claim in this row was found softened**), and `_resolve_interpreter` is a strict **shape validator, not an authenticator** -- it checks neither Python identity nor binary provenance, and accepts any absolute, present, non-symlinked, executable regular file. This is not optional prose-polish: it is the specific correction the Security Review made blocking, and the Decision quotes it as "on the record." Land it in substance, not as a paraphrase that could soften it. |
| E2 | `templates/skills/_lib/lifecycle.py` | The stale comment near the old `is_file()` check (the one claiming an appended-argument string "is caught by the `is_file()` check below") corrected -- under the revised classifier such a string is an absent *path* and degrades, per R2/R6's discussion. |
| E3 | `templates/skills/_lib/lifecycle.py` | Threat-model-adjacent note (R7): the docstring's stdlib-only safety rationale is scoped to *this tool*, not the sub-tools the resolved interpreter runs -- one sentence, not a new section (the full threat-model argument lives in the proposal's record, not duplicated into shipped-tool prose). |

### Chunk F -- tests (`bootstrap/tests/test_lifecycle_failsafe.py`, FROZEN, rewritten)

| # | Change |
|---|--------|
| F1 | `test_tampered_local_env_refuses` (`:240-252` live): relocate the two absent-path values (`/usr/bin/python --foo`, `/no/such/python`) out; replace with a present-non-executable regular file and a present directory, materialized in the test body via a non-id-representable sentinel (module-level parametrize values cannot use the `repo` fixture, and `_make_exe` at `:255` is defined *below* the decorator). Pin `ids=["bad0","bad1","bad2","bad3"]` explicitly on the decorator -- R5's empirically-verified fix (an all-dict-except-one-string list silently drops a node from collection; the explicit `ids=` avoids depending on parametrize-value shape). **The present-non-executable-file parametrize case is POSIX-only** (per ETR5 below) until S3 (Windows `os.access(X_OK)`) closes -- skip-guard it on non-POSIX hosts; the present-directory case is a portable `Path.is_dir()`-shaped refusal and needs no such guard. |
| F2 | New `test_stale_interpreter_path_degrades_with_guidance`, parametrized over two values **materialized from the test's resolved `repo` path, not hardcoded POSIX literals** (**corrected at plan-review, ETR5, External/Codex, substantive portability**: the original literals `/usr/bin/python --foo` / `/no/such/python` are not absolute under `PureWindowsPath` -- executed directly, both report `is_absolute() == False` there -- so on Windows they would hit the "must be an absolute path" fatal branch instead of the accepted absent-path degrade, silently broadening the Windows gap beyond S3's own carried `X_OK` residual): a plain-absent value (`repo / "no" / "such" / "python"`, not created) and an appended-argument-shaped absent value (`f"{repo / 'python'} --foo"`, still absolute-prefixed by the OS-native resolved `repo` path, still never created). Both cases assert: `rc == 0`, `(from fallback-stale)` on stdout, `_REBIND_REMEDY`'s text on stderr, **and — added at plan-review, PR6, Internal, substantive, since this is one of the Decision's five binding conditions and its coverage must be named, not inferred — assert the recorded (stale) interpreter path string, and `sys.executable`, both appear in the captured stderr warning text** (the `_warn_stale_once` message the Revised proposal's C1 builds separately from `_REBIND_REMEDY`; `_REBIND_REMEDY` alone never names either value). Preserve explicit `ids=` on this parametrize too. |
| F3 | New `test_stale_warning_fires_once_per_process` (R4's count fix, not presence): a full `session-end --handoff` with an `intent.py` sibling present (monkeypatch `_sibling_tool`, per F6) and `CAIRN_AGENT`/`CAIRN_SESSION` **unset** (the real multi-call shape the `repo` fixture's `CAIRN_AGENT=owner` would otherwise mask) asserts **exactly one** occurrence of the remedy string in captured stderr, not merely its presence -- via multiple resolver-reaching calls made *within this one test node* (relies on F0's fixture below only to guarantee a clean sentinel on entry, not to isolate multiple calls from each other). |
| F0 | **New, per plan-review (ETR2, External/Codex, blocking):** an **autouse fixture resetting the module-level `_STALE_WARNED` sentinel before and after every test in this file.** The Revised proposal explicitly committed to this ("`_warn_stale_once` guards `_warn` with a module-level sentinel... The plan adds an autouse fixture clearing the sentinel between tests," archived proposal `:485-487`) but this plan's first draft omitted it. Without it, `test_lifecycle_failsafe.py` loads `lifecycle` once per test session (module-level `_load()`, `:52`), so the sentinel persists across test *nodes* — F2's parametrize cases, and F3/F4's own stale resolutions, would see the sentinel already tripped by an earlier node and silently observe zero warnings, either failing outright or (worse) tempting a weakened assertion to accommodate the leaked state. |
| F4 | New `test_stale_binding_is_not_rewritten`: `local-env.json` bytes identical before/after a degraded run (R11's note: the resolver contains no write path today, so this is a forward regression guard against the explicitly-rejected auto-rebind alternative, not a guard against a present mechanism -- label it as such in the test docstring). |
| F5 | New `test_uninspectable_interpreter_path_refuses`: an unreadable-parent (mode-000) path raises `LifecycleError` via the classifier's `except OSError`, root/non-POSIX skip-guarded. Valid against the *revised* guard only (R2(a)'s falsification was against the naive single-probe version). |
| F5b | **New, per plan-review (ETR4, External/Codex, substantive security contract):** `test_parent_traversal_segment_refuses` -- a binding containing a `..` component (e.g. `str(repo / "a" / ".." / "python")`) raises `LifecycleError` **before** reaching `_probe_interpreter`, the direct regression the narrowed A3 guard needs and Chunk F's first draft never named. |
| F6 | New `test_symlinked_parent_with_absent_leaf_still_refuses` and `test_symlinked_leaf_refuses` (R3): a real dir, a symlink to it, binding pointed at `<symlink>/python` where `python` does not exist → `LifecycleError`; and a symlinked leaf directly → `LifecycleError`. Pins the required probe ordering (symlink walk before absence classification) as an actual enforced test, not an asserted-but-untested invariant. **Capability-skip where the host cannot create symlinks** (per ETR5's portability note), rather than assume POSIX. |
| F7 | New `test_tampered_binding_warns_in_intent_whoami` (C3). **Corrected at plan-review (ETR3, External/Codex, substantive):** this plan's first draft asserted `_intent_whoami` returns `None` on a present-but-wrong binding -- **wrong**: executed live, with `_resolve_interpreter` forced to raise and a valid, working fake `intent.py` sibling present, the C3 fallback runs that sibling under `sys.executable` and returns its real output (a `codex-12345678`-shaped identity string in the reviewer's probe), not `None`. A `None` assertion can only pass by making the sibling itself fail or emit nothing -- which would not exercise the fail-open path the Security Review actually accepted. Corrected: use a valid fake `intent.py` (the existing `:297-300` monkeypatch pattern -- `_intent_whoami` returns early without it), assert the fallback's expected identity string is returned (not `None`), and assert stderr contains the original resolver refusal message (C3's actual job: surface the refusal, then still fall back successfully). Optionally keep a second, separate failing-sibling case asserting `None` if useful, but it is not the primary regression. |
| F8 | New resolver source-scan test in the spirit of `bootstrap/tests/test_lifecycle_contract.py:139-148` (which scans the *planner*, `lifecycle_planner.py` -- a pattern to copy, not an existing guard covering this module, per R11's precision correction): assert the resolver's source contains no write primitive against the state directory. |
| F9 | Module docstring (`:16-19`) reworded from "a tampered config refuses before running anything" to the two-branch posture. |
| F10 | Must stay green, byte-unchanged in assertion shape: `test_interpreter_resolved_from_local_env_and_reported`, `test_absent_local_env_uses_fallback_with_guidance`, `test_space_in_interpreter_path_accepted`, `test_extra_key_in_local_env_refused`. |

### Chunk G -- gate-manifest re-anchor (two Maintainer-only steps: a pre-Chunk-A prerequisite, and a post-Chunk-H handoff)

**Not the AST-baseline direct-edit pattern** used on every other plan this
session -- `test_lifecycle_failsafe.py` is a `bootstrap/tests/` FROZEN file
under `bootstrap/tests/_gate_manifest.py`'s `frozen_files` set, a
structurally different control from `scaffold_ast_baseline.json`'s symbol
digests (which this proposal never touches -- no `bootstrap/_scaffold/` edit
means no AST re-anchor at all, confirmed by the proposal and re-confirmed
this session). The applicable mechanism is `bootstrap/tests/
_gate_reanchor.py` + `bootstrap/REANCHOR_RUNBOOK.md`'s Phase 4 ceremony.

**Rewritten twice at plan-review.** First at ETR1 (External/Codex, blocking
process): the original "implementer runs `prepare`, Maintainer runs
`promote`" scoping is impossible (`refs/cairn/gate-authorization` does not
exist; `prepare` itself, not only `promote`, needs it) and unauthorized (a
234-file inherited drift against `refs/cairn/gate-anchor`, unrelated to this
plan). Then again at **ETR1-R2 (External/Codex, blocking process)**, because
the first rewrite still had two defects, both confirmed by execution this
session:

* **Wrong candidate/delta mechanics.** `_construct_anchor_commit`
  (`bootstrap/tests/_gate_reanchor.py:274-307`) builds `N = C`'s tree + the
  trusted manifest blob, committed **with `C` as `N`'s sole parent** — so
  `git diff P..N` is definitionally `git diff P..C` **plus** the manifest
  file, i.e. *every* file that changed between `P` and candidate `C`, not
  only whichever chunk the plan's prose singled out. The Round-1 rewrite
  called the expected `P`→`N` delta "exactly Chunk F's test-file changes" --
  wrong, confirmed by running the real `_construct_anchor_commit`/
  `_diff_name_only` helpers in an isolated temp repo with this plan's four
  implementation-touched files changed: `P..N` contained
  `templates/skills/_lib/lifecycle.py`, `tools/lifecycle.py`, `dev/.cairn/
  cairn-lock.yml`, and `bootstrap/tests/test_lifecycle_failsafe.py` (only
  `C..N` was manifest-only).
* **Wrong sequencing.** The Round-1 rewrite placed this chunk's handoff
  between F and H in the `## Sequence` block while calling its candidate `C`
  "this plan's final implementation commit" -- self-contradictory, since H
  (the self-host sync, which itself touches `tools/lifecycle.py` and
  `dev/.cairn/cairn-lock.yml`) had not landed yet at that point.

**Corrected design -- split into two Maintainer-only steps, neither an
implementing-agent act:**

**G0 -- pre-Chunk-A prerequisite.** Before Chunk A begins: the Maintainer
resolves the pre-existing 234-file / 54-changed-pinned-plus-14-newly-frozen
/ 1404→1446-collection drift against `refs/cairn/gate-anchor` (a
Maintainer-controlled gate-baseline transition, reviewed and recorded on its
own -- this plan does not decide how, only that a concrete, resolved `P`
must exist before implementation starts, so the eventual G1 handoff has a
known, reviewable starting point rather than an open-ended inherited scope).
This is a **precondition on Chunk A**, not parallel work -- the implementing
agent does not begin Chunk A until the Maintainer confirms a usable `P`.

**G1 -- post-Chunk-H handoff** (sequencing corrected -- this now runs
**after** Chunk H, not between F and H; see the `## Sequence` block below).
Once Chunks A-H all land: the implementing agent's job is limited to
identifying the actual final implementation commit as candidate `C`, and
stating the **reviewed expected `P`→`N` delta** correctly this time --
**all four** plan-touched files (`templates/skills/_lib/lifecycle.py`,
`tools/lifecycle.py`, `dev/.cairn/cairn-lock.yml`, `bootstrap/tests/
test_lifecycle_failsafe.py`) **plus this plan document itself**
(`dev/plans/interpreter-trust-root-fallback.md`) **plus** the generated
`gate_manifest.json` -- **five files, not four** (**corrected at
plan-review, ETR1-R3, External/Codex, blocking process**: a plan is a
mutable execution artifact per Cairn's own template, and each
implementation commit updates its Status field in place as chunks land --
the sibling `lockfile-provenance-fields` plan's own Chunk A commit
(`02f6ee1`) is the live proof, its diff naming the plan file alongside the
code for exactly this reason. G1's delta bounds the plan file's *allowed*
mutation to that normal execution-state progression (`Status:` transitions
and, if any landed, per-chunk `[commit pending]`-style Sequence notes) --
**not** a review or Sharpening/Response section, which stay append-only
throughout). Refusing (flagging to the Maintainer, not silently absorbing)
any unrelated intervening change, including an out-of-bound mutation to
the plan file itself. The Maintainer then authors the authorization anchor
`A` (Phase 4 step 1) against G0's established `P`, and runs **both**
`prepare` (step 2) and `promote` (step 3) themselves, recording the
resulting `P`/`A`/`C`/`N` in this plan's own eventual Lasting-truth
migration section. **The acceptance criterion is this Maintainer-recorded
result** -- not an implementing-agent `prepare` run, and not a delta claim
scoped to one chunk
when the mechanism itself always constructs the whole-candidate diff.

### Chunk H -- self-host sync

| # | Change |
|---|--------|
| H1 | Copy the edited `templates/skills/_lib/lifecycle.py` to `tools/lifecycle.py` verbatim (the `config.py:211` `verbatim: true` mapping). |
| H2 | Refresh `dev/.cairn/cairn-lock.yml:545-549`'s `hash` **and `base_hash`** for the `tools/lifecycle.py` entry to the new sha256 (**range corrected at plan-review, PR2, Internal, blocking, from `:546-549`, which excluded line `:545` — where `base_hash` actually is**) -- a **hash refresh for one changed file**, not a lockfile-schema change (R9). Named explicitly, per R9: hand-edit the two lines (matching the precedent this session already used for hash-only corrections), not `scaffold.py upgrade --target .` -- the latter is a full upgrade-stage/apply cycle with its own stage-metadata and backfill semantics that this single-entry refresh does not need and would pull in unrelated machinery for. Flagged for the required External reviewer to confirm this choice, since R9 asked the plan to justify it, not merely state it. **Also, per PR2:** this refresh corrects a **pre-existing** inconsistency, not only this plan's own edit — `base_hash` is already stale today (still the pre-`first-session-survivability` value, `hash != base_hash`), a silent-fork condition per `lockfile.py`'s own semantics, unrelated to and predating this plan (Context Finding 2). |
| H3 | `python bootstrap/verify_integrity.py --target .` output **scoped to the `tools/lifecycle.py` record specifically** — no `tools/lifecycle.py` line in its violations/notes, checked before H1/H2 and again after. **Corrected at plan-review (PR1, Internal, blocking):** the original "must already be clean" / "must still be clean" whole-tree framing is not satisfiable on the live tree as written — re-run this session, `verify_integrity.py --target .` reports **3 pre-existing hash-mismatch violations** (`AGENTS.md`, `dev/plans/_template.md`, `dev/proposals/_template.md`), a known, already-tracked, same-day condition (`dev/PLANNING.md`'s "Self-host lockfile reconciliation" entry, commit `d472c00`, 38 files with "no recoverable base," none of them `tools/lifecycle.py`). None of this plan's own disclosed findings mentioned it. The scoped before/after check (no `tools/lifecycle.py` line, specifically) is satisfiable today and is the check R9 actually needs; the whole-tree baseline is out of this plan's scope and separately tracked. |
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
* **Gate-manifest re-anchor** -- **corrected at plan-review (ETR1,
  External/Codex, blocking process; delta/sequencing corrected again at
  ETR1-R2, file count corrected again at ETR1-R3)**: **G0** (a precondition
  on Chunk A) is a Maintainer-resolved, concrete pre-implementation `P` —
  no current 234-file / 54+14-frozen-file drift against `refs/cairn/
  gate-anchor` left unaddressed. **G1** (after Chunk H) is the
  **Maintainer's own recorded `promote` result** (`P`/`A`/`C`/`N`), where
  `C` is the actual final implementation commit and the reviewed expected
  `P`→`N` delta is **five files, not four**: `lifecycle.py`,
  `tools/lifecycle.py`, `cairn-lock.yml`, `test_lifecycle_failsafe.py`,
  **and this plan document itself** (its Status field transitions in place
  as chunks land, exactly as the sibling `lockfile-provenance-fields`
  plan's own Chunk A commit demonstrates) — plus the generated
  `gate_manifest.json`. Not a single-chunk
  delta claim, since `_construct_anchor_commit` (`N = C` + the manifest blob,
  `C` as `N`'s sole parent) definitionally makes `P`→`N` equal `P`→`C` plus
  the manifest, i.e. every file the whole candidate changed. Not an
  implementing-agent `prepare` run at either step -- no current ref or code
  path supports that framing. This plan's own implementation stops at G1's
  candidate-`C`-and-delta identification.
* **Self-host verification** -- H3's before/after `verify_integrity.py`
  runs, both scoped to the `tools/lifecycle.py` record (no `tools/
  lifecycle.py` line in either run's output) -- **not** whole-tree-clean, per
  plan-review PR1; the tree carries 3 pre-existing, unrelated hash-mismatch
  violations today. H4's byte-identity assertion holds.
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
from this plan's own preparation, **corrected at plan-review (ETR1,
External/Codex, blocking process; corrected again at ETR1-R2 to match the
real `_construct_anchor_commit` mechanics; file count corrected again at
ETR1-R3)** to match Chunk G0/G1's rewritten handoff: **G1's `P`→`N` diff
contains anything beyond the five named files** (`lifecycle.py`,
`tools/lifecycle.py`, `cairn-lock.yml`, `test_lifecycle_failsafe.py`, and
this plan document itself, bounded to its normal execution-state
mutation) **plus the generated gate_manifest.json** -- since `P`→`N` is
definitionally `P`→`C` plus the manifest, an unexpected extra file in that
diff means either G0's established `P` was not actually current, or an
unrelated change slipped into candidate `C`; the Maintainer does not run
`promote` until the diff matches exactly those six items, nothing else.

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

## Plan review -- Claude (Internal, fresh-context) -- 2026-07-31

**Tier reminder.** This plan's header declares `Plan review: required(External)`.
Everything below is a same-agent-type, fresh-context **Internal** pass only. A
clean Internal pass, however thorough, does **not** satisfy that gate --
a genuinely different-agent-type or human read is still required before
implementation begins.

**Method.** Every `templates/skills/_lib/lifecycle.py` and
`bootstrap/tests/test_lifecycle_failsafe.py` line the plan cites was re-read
against the live tree independently (not copied from the plan's own
numbers), `shasum -a 256` was run on both `lifecycle.py` copies, `dev/.cairn/
cairn-lock.yml` and `AGENTS.md` were read directly, `git show 91c96b4` /
`git log` were run, `bootstrap/tests/_gate_reanchor.py` was read in full,
`python -m pytest bootstrap/tests --collect-only -q` and `bootstrap/tests/
fixtures/gate_manifest.json` were checked, and the full suite was executed
under the canonical interpreter (`/Users/kendal30/conda_envs/lhm/bin/
python3.13 -m pytest bootstrap/tests -q`, 242s).

**Summary: 2 BLOCKING, 6 SUBSTANTIVE, 2 MINOR.**

---

### BLOCKING

**PR1 -- Chunk H3's "must already be clean" precondition is not satisfiable
in the live tree right now, and the plan doesn't disclose why.**
`python bootstrap/verify_integrity.py --target .` was run this session and
does **not** report clean:

```
verify_integrity: 3 integrity violation(s) vs. dev/.cairn/cairn-lock.yml:
  modified (hash mismatch): AGENTS.md
  modified (hash mismatch): dev/plans/_template.md
  modified (hash mismatch): dev/proposals/_template.md
The on-disk tree no longer matches its recorded install. Do not trust the
shipped scripts until this is resolved.
```

plus two NOTE-level forked-facade warnings (`tools/intent.py`,
`tools/lifecycle_metrics.py` -- unrelated dormant-engine condition, not
`tools/lifecycle.py`). This is a known, already-tracked, same-day condition:
commit `d472c00` ("dev/PLANNING.md: queue the self-host lockfile
reconciliation gap", 2026-07-31 09:22, at the Maintainer's explicit
instruction) documents **38** files across the self-hosted tree with "no
recoverable base" against `dev/.cairn/cairn-lock.yml`, of which the three
`modified (hash mismatch)` files above are members (all `"verbatim": false,
"unrecoverable_base": true` in the lockfile). None of this plan's own six
disclosed findings mention it, and Chunk H3 as written ("run **before**
H1/H2 (must already be clean) and **after** (must still be clean)") gives
the implementer no way to reconcile the instruction with the actual tree:
run literally, the *before* check fails immediately, on a condition this
plan did not cause and cannot fix within its own scope.
*Suggested fix:* Cross-reference `dev/PLANNING.md`'s "Self-host lockfile
reconciliation" entry in Chunk H3, and scope the before/after clean-check to
**the `tools/lifecycle.py` record specifically** (e.g. `verify_integrity.py`
output contains no `tools/lifecycle.py` line, before and after), not to
zero-violations over the whole tree -- the whole-tree baseline is a
pre-existing, separately-tracked, out-of-scope condition.

**PR2 -- Context Finding 2's "matching both the `hash` and `base_hash`...
exactly" is false against the live lockfile; the same field is what Chunk H2
is about to rewrite.** Re-verified independently: `shasum -a 256` on both
copies gives `6f6333ee3a5c0d53f8278601ccfdd0867f749452ac02d63faba6ccb32e46d852`
(matches the plan's claim), and the live `dev/.cairn/cairn-lock.yml` entry
for `tools/lifecycle.py` (lines 545-549) reads:

```
545  "base_hash": "sha256:296ef88bda1e3e817734cc6cdb14e9571cd3a0ee0aada8d07dfa9e1f898839c9",
546  "dst": "tools/lifecycle.py",
547  "hash": "sha256:6f6333ee3a5c0d53f8278601ccfdd0867f749452ac02d63faba6ccb32e46d852",
548  "src": "skills/_lib/lifecycle.py",
549  "verbatim": true
```

`hash` matches the current byte-identical content (`6f6333ee...`); `base_hash`
does **not** -- it is still `296ef88b...`, which is exactly the *original*
2026-07-22 pre-drift proposal's cited hash, i.e. the value from **before**
the intervening `first-session-survivability` F4 edit resynced this file.
Per `bootstrap/_scaffold/lockfile.py`'s own fork-detection semantics
(`hash != base_hash` = "forked from upstream", `:262`, `:280`), this record
currently reads as a silent fork, even though the two files are verified
byte-identical right now. This is exactly the class of false "re-verified"
disclosed claim the task brief flags as highest-risk, on the one finding
this review was specifically asked to check by direct inspection. Chunk H2's
edit ("refresh ... `hash` and `base_hash` ... to the new sha256") happens to
fix this stale `base_hash` as a side effect, but the plan frames it purely
as "a hash refresh for one changed file" for *this plan's own edit* -- it
never states that `base_hash` is *already* wrong, for a reason unrelated to
this plan, before Chunk H even starts. Separately, the cited range
`dev/.cairn/cairn-lock.yml:546-549` excludes line 545, which is where
`base_hash` actually is -- the citation range does not even span the field
the claim is about.
*Suggested fix:* Correct Finding 2 in place is not possible (append-only),
so append a one-line correction to the Context section (or fold it into
Chunk H2's own row): "`base_hash` was already stale before this plan (still
the pre-F4-edit value); Chunk H2's refresh corrects a pre-existing
inconsistency, not only this plan's own edit." Fix the cited range to
`:545-549`.

---

### SUBSTANTIVE

**PR3 -- Chunk A4's citation for the single most load-bearing edit in the
plan (the classifier-dispatch tail replacement) is wrong on both ends.**
Chunk A4: "Replace the current tail of `_resolve_interpreter` (`:380-395` in
the live tree, i.e. from the `is_absolute()` check through the return)".
Read against the live file: `if not interp.is_absolute():` is at line
**385**, not 380 (line 380 is `if any(ord(ch) < 0x20 ...` -- the
control-character check, two guards earlier); the final `return str(interp),
"local-env.json"` is at line **396**, not 395. The correct span is
`:385-396`. This is the plan's own re-derivation, not a copy of the
proposal's pre-drift number (which was `:380-390`) -- the end shifted by
+5 (consistent with the claimed drift) but the start did not shift at all,
an inconsistent application of the same drift the plan says it corrected
throughout. Low risk of actually misleading an implementer (the surrounding
prose precisely describes the three-way dispatch), but on a security-
sensitive trust-root resolver this is exactly the citation that should be
exact.
*Suggested fix:* Correct to `:385-396` in Chunk A4.

**PR4 -- A cluster of citation errors around `_intent_whoami` / `_sibling_tool`
that the plan claims were carefully re-derived.** Read against the live file
(`templates/skills/_lib/lifecycle.py`):
* Context Finding 1: "`_intent_whoami` `:187-213` (swallow at `:198-200`)".
  The function does start at `:187` (exact), but the `try`/`except
  LifecycleError` swallow is at `:199-202` (`try:` `:199`, the resolver call
  `:200`, `except LifecycleError:` `:201`, the fallback assignment `:202`);
  line `:198` is `return None` (the unrelated `intent_tool is None` early
  return), not part of the swallow at all. The cited range also stops short
  of the except clause itself (`:201-202`).
* Chunk C1t (C3's own implementing instruction): "The `except LifecycleError`
  swallow at `:199-200` gains a `_warn`..." -- same gap: `:199-200` is
  `try:` plus the call being tried, not the `except` line or the fallback
  assignment.
* Chunk B1: "`_intent_whoami` `:198`" as the location of its resolver call --
  the actual call is at `:200`.
* Context Finding 1: "`_sibling_tool` `:288-292`" -- the function does start
  at `:288` (exact), but spans `:288-297`; `:288-292` stops mid-docstring
  and excludes the function's entire body (`candidate = ...` at `:296`,
  `return ...` at `:297`).
None of these point at nonexistent code, and an implementer reading the
surrounding prose would still find the right lines, but Chunk C is exactly
the chunk implementing the Security Review's "pre-existing fail-open ruling"
(surface the caught refusal before falling back) -- the citations naming
*where* to add the `_warn` should be exact.
*Suggested fix:* Correct to swallow `:199-202` (except clause `:201-202`),
`_intent_whoami` resolver call `:200`, `_sibling_tool` `:288-297`.

**PR5 -- Context Finding 3's `AGENTS.md` citation is off by a much larger,
differently-sourced margin (~15-23 lines) than the plan's own ~5-line
lifecycle.py-drift pattern.** Finding 3 cites `AGENTS.md` "`:296-303`" for
the "local interpreter binding" high-risk-surface bullet. Read against the
live file: the "**High-risk surfaces**" heading is at `:304`, and the bullet
itself spans `:319-327`. `git show 91c96b4 -- AGENTS.md` confirms the diff
inserted the bullet immediately after the "by-file license split" bullet
(`@@ -313,6 +313,15 @@`), so right after that commit landed the bullet sat
around `:316-324`; a second same-day commit (`3325a13`, "docs: pin the
canonical interpreter for the suite and the gates") also touched `AGENTS.md`
and pushed it down further to the current `:319-327`. `:296-303` matches
neither point in time -- it looks like a carry-forward of the *original*
proposal's own `AGENTS.md:301`/`:310` numbers (from R10(b), a pre-session
citation about an unrelated bullet) rather than a fresh re-derivation
against the file as it stands after *today's* two edits. The qualitative
claim (bullet exists, commit `91c96b4`, landed by the Maintainer today,
independent of this plan) is correct and independently confirmed via `git
show`/`git log`; only the line numbers are wrong.
*Suggested fix:* Correct to heading `:304`, bullet `:319-327`.

**PR6 -- F2's stated assertions don't clearly cover the binding condition
the Acceptance-criteria table credits it with.** The Acceptance criteria
section states: "The stale recorded value **and** the substituted
interpreter both named in that warning (F2's stdout/stderr assertions)."
But Chunk F's own description of F2 lists exactly three assertions: `rc ==
0`, `(from fallback-stale)` on stdout, and `_REBIND_REMEDY`'s text on
stderr. `_REBIND_REMEDY` (Chunk A2 / C1a) is a fixed generic string that
never contains the stale path or `sys.executable` -- those values are named
only in the `_warn_stale_once(...)` message the Revised proposal's C1 code
builds separately (`f'{cfg}: recorded interpreter "{interp}" no longer
exists ... Using the current interpreter ({sys.executable}) ...'`). As
written, an implementer following F2's three listed assertions literally
would not necessarily assert that either value appears in stderr; the
"(from fallback-stale)" stdout check happens to co-occur with the
interpreter path on the same `_emit` line at `cmd_session_start:709`, but
that is incidental, not something F2's description asks for. This is a
Decision-mandated, binding condition (not a preference), so its test
coverage should be named explicitly rather than inferred.
*Suggested fix:* Add to F2's description: "and assert the recorded (stale)
interpreter path string, and `sys.executable`, both appear in the captured
stderr warning text."

**PR7 -- S3 (the Windows caveat) is the one Decision follow-up this plan
never mentions.** The Decision lists three explicit follow-ups: S2 (its own
`dev/PLANNING.md` row, confirmed present and accurate -- see below),
governance registration (confirmed already landed, Finding 3), and S3
("native Windows execute semantics remain unverified and are carried as an
explicit residual; the present-but-non-executable leg is not claimed as a
cross-platform verified guarantee"). A full-text scan of this plan (Context,
all eight chunks, Acceptance criteria, Signals the change is wrong) turns up
no mention of "Windows" anywhere. S2 gets a durable home at plan-open;
governance is explicitly marked done; S3 is simply absent -- not carried
forward, not marked as needing no action, not cross-referenced to the
proposal's own residual-5 language. This is exactly the omission class the
task brief asked this review to check for.
*Suggested fix:* One sentence, e.g. in Chunk E's docstring rewrite or the
Acceptance criteria: "S3 (native Windows `os.access(X_OK)` semantics)
carries forward unchanged as an explicit residual per the Decision; this
plan touches no Windows-specific code path and adds no Windows test, so no
plan action closes it."

**PR8 -- The Documentation-surface section cites a lifecycle.py comment at
its pre-drift line number, contradicting the plan's own re-verification
claim.** "Per the proposal: shipped-tool docstrings only (the resolver's
contract paragraph, the stale `:370-374`-region comment, the module
docstring of the test file)." Read against the live file, the comment in
question ("An appended-argument string like ... is caught by the `is_file()`
check below") is at `:375-379` -- a clean +5 shift consistent with the
plan's own claimed drift, but the plan's text still carries the *old*,
un-adjusted number. This is a small thing on its own, but it is a concrete,
checkable instance of exactly the failure mode Finding 1 claims to have
eliminated ("Current, re-read locations used throughout this plan").
*Suggested fix:* `:375-379`.

---

### MINOR

**PR9 -- `_resolve_interpreter`'s own end-of-function citation is off by
one.** Context Finding 1 cites `_resolve_interpreter` as `:336-395`; the
function's def is at `:336` (exact) but its final `return str(interp),
"local-env.json"` is at `:396`, not `:395`. Same family as PR3.

**PR10 -- E1's compressed restatement of the S1 correction drops one word
from the Decision's verbatim text.** Comparing word-for-word per the task
brief: the Decision (and the Response's original correction) describes
`local-env.json` as "untracked, gitignored, **mutable**, and not
lockfile-covered"; the plan's Chunk E1 compresses this to
"untracked/gitignored/not lockfile-covered" -- dropping "mutable". The
substantive claims (operationally-trusted-binding, shape-validator-not-
authenticator, checks neither identity nor provenance, accepts any
absolute/present/non-symlinked/executable file) are all preserved
faithfully and I found no softening. Noted for completeness since the task
asked for a strict word-for-word check, not because it changes meaning.

---

### Independently confirmed as accurate (no issues found)

* All `bootstrap/tests/test_lifecycle_failsafe.py` citations in Context
  Finding 1 (`_make_exe` `:255-260`, the parametrize `:240-245`,
  `test_space_in_interpreter_path_accepted` `:263-275`,
  `test_extra_key_in_local_env_refused` `:278-287`, the monkeypatch pattern
  `:297-300`) -- exact, matching the plan's "no drift there at all" claim.
* `cmd_session_start` def `:634` and its resolver call `:703`; `_do_full_
  handoff` def `:1130` and its resolver call `:1160`; `main` `:1270-1281`;
  `_has_symlink_component` `:320-333` -- all exact.
* Finding 2's byte-identity claim: `shasum -a 256` on both `lifecycle.py`
  copies is `6f6333ee...`, confirmed equal (only `base_hash`, per PR2, is
  wrong).
* Finding 3's qualitative claim (bullet exists, commit `91c96b4`, Maintainer,
  today, independent of this plan) -- confirmed via `git show 91c96b4 --
  AGENTS.md` and `git log`; only the line numbers are wrong (PR5).
* Finding 4's suite baseline: `/Users/kendal30/conda_envs/lhm/bin/python3.13
  -m pytest bootstrap/tests -q` run fresh this review -- **0 failed, 1446
  passed, 0 skipped**, 242s. Exact match.
* Finding 5's two figures: `--collect-only -q` reports **1446 collected**;
  `bootstrap/tests/fixtures/gate_manifest.json`'s `collection.node_count` is
  **1404**. Both exact. `test_lifecycle_failsafe.py` confirmed present in
  the 147-entry `frozen_files` dict; `templates/skills/_lib/lifecycle.py`
  and `tools/lifecycle.py` confirmed absent from it.
* Finding 6's characterization of `bootstrap/tests/_gate_reanchor.py`:
  module docstring and the `prepare`/`promote` CLI subcommands (`main`,
  `:531-537`) confirm the Stage A (`gather_evidence`, executable,
  non-authoritative) / Stage B (`promote_data_only`, data-only,
  authoritative, CAS ref-advance) split exactly as described, and that
  `prepare` = "Stage A+B through data-only validation; NO ref advance" while
  `promote` is the ref-advance step. Chunk G's scoping to `prepare` only is
  accurate.
* Chunk A's `_probe_interpreter` design against the Revised proposal's C1
  (revised) code block: the unified `except OSError` wraps both
  `_has_symlink_component` and the `stat()` probe, matching R2(a)'s fix
  exactly (not the "wrap only the probe" shape R2(a) disproved).
* The required (not preferred) probe ordering -- symlink walk before
  absence classification, both under one `except OSError` -- is correctly
  preserved in both Chunk A's design and the Acceptance criteria's explicit
  labeling.
* The other four binding conspicuousness conditions map to concrete Chunk F
  tests as claimed: exactly-one-warning (F3), source token `fallback-stale`
  (F2), actionable non-`--force` guidance (F2 via `_REBIND_REMEDY`), and no
  automatic rewrite (F4, correctly re-labeled per R11 as a forward
  regression guard against the rejected auto-rebind alternative, not a
  guard against a present write path).
* The `dev/PLANNING.md` S2 row (`:304-316`, "Interpreter trust-root
  check/use race (S2)" under "Lifecycle apparatus") accurately restates the
  Security Review's disposition: pre-existing, not introduced by the
  absent-path degrade, attacker prerequisites generally permit replacing the
  interpreter directly, not accepted as closed by the Decision, revive as
  its own proposal. Already committed (`3982918`, plan-open), consistent
  with the plan's own "lands now, at plan-open" claim.
* Chunk H's justification for hand-editing the two lockfile hash lines
  instead of `scaffold.py upgrade --target .` is named and argued (not
  merely asserted), satisfying R9's requirement, independent of PR1/PR2's
  finding that the pre-existing lockfile state around it is not as clean as
  Finding 2 claims.
* F8's citation, `bootstrap/tests/test_lifecycle_contract.py:139-148`, is
  exact -- the cited lines are precisely the no-write-primitive source-scan
  pattern the plan proposes to copy.

Coverage note: this pass did not independently re-execute the disposition
matrix on 3.11/3.13, did not hand-run a real conda rebuild, and did not
attempt Chunk G's `_gate_reanchor.py prepare` itself -- all three are
implementation-time steps this plan correctly defers to the implementing
agent, not something a plan-review pass should pre-empt.

### Sharpening -- Claude (author) -- 2026-07-31

All ten findings independently re-verified before disposing, not taken on
the reviewer's word: ran `python bootstrap/verify_integrity.py --target .`
myself (identical 3 violations, identical file list); read `dev/.cairn/
cairn-lock.yml:544-550` directly and confirmed `base_hash` (`296ef88b...`)
does not equal `hash` (`6f6333ee...`); re-derived the classifier-tail span
by direct line count (`sed -n '375,397p'` against the live file) and
confirmed `is_absolute()` at `:385`, the appended-argument comment at
`:375-379`, and the final `return` at `:396`, all exactly as the reviewer
reported.

* **[PR1] accept — blocking, fixed.** Chunk H3 rewritten from an
  unsatisfiable whole-tree "must already be clean" / "must still be clean"
  pair to a check scoped to the `tools/lifecycle.py` record specifically,
  cross-referenced to `dev/PLANNING.md`'s already-tracked reconciliation
  gap. The Acceptance criteria's "Self-host verification" bullet corrected
  to match.
* **[PR2] accept — blocking, fixed.** Context Finding 2 corrected in place
  (mutable per doctrine — this is the plan's own Context, not the
  append-only review section) to state the `base_hash` staleness plainly,
  as a pre-existing condition Chunk H2's refresh incidentally fixes. H2's
  citation range corrected `:546-549` → `:545-549`, and H2's row now names
  the pre-existing-fix explicitly rather than leaving it implicit.
* **[PR3] accept — substantive, fixed.** Chunk A4's citation corrected
  `:380-395` → `:385-396`.
* **[PR4] accept — substantive, fixed.** Corrected throughout: Finding 1's
  summary line, Chunk B1 (`:198`→`:200`), Chunk C1t (`:199-200`→`:199-202`),
  and Finding 1's `_sibling_tool` citation (`:288-292`→`:288-297`).
* **[PR5] accept — substantive, fixed.** Finding 3's `AGENTS.md` citation
  corrected `:296-303` → heading `:304`, bullet `:319-327`.
* **[PR6] accept — substantive, fixed.** Chunk F2 gained the explicit
  stderr assertion (stale path and `sys.executable` both present) the
  Acceptance criteria already credited it with but the row itself never
  stated.
* **[PR7] accept — substantive, fixed.** S3 added to the Documentation /
  doctrine surface section as an explicit carried-forward residual,
  matching how S2 and governance are each accounted for.
* **[PR8] accept — substantive, fixed.** Documentation-surface section's
  comment citation corrected `:370-374` → `:375-379`.
* **[PR9] accept — minor, fixed.** Folded into Finding 1's `_resolve_
  interpreter` span, corrected `:336-395` → `:336-396`.
* **[PR10] accept — minor, fixed.** Chunk E1's compressed restatement
  restored to the Decision's full four-adjective list ("untracked,
  gitignored, mutable, and not lockfile-covered"), dropped word reinstated.

**Status: remains `awaiting-plan-review`.** This Internal pass and its
sharpening are the floor, not this plan's declared gate — the header's
`Plan review: required(External)` is not satisfied by an Internal read at
any thoroughness. Implementation on Chunk A does not begin until a
genuinely different-agent-type or human review lands as its own dated
`## Plan review` section.

This section is append-only once written.

## Plan review -- Codex (External, different-agent-type; Security Review) -- 2026-07-31

**Verdict: REVISE.** The plan faithfully carries the accepted security posture:
the absent-path detection downgrade remains acceptable, symlink inspection
correctly precedes absence classification, and all five conspicuousness
conditions are represented. It is not yet executable as written. One gate-
authority blocker, one test-isolation blocker, and three substantive test/
contract mismatches remain; Chunk A must not begin until a focused External
re-read closes them.

### Findings

* **[ETR1] BLOCKING PROCESS -- Chunk G assigns an impossible and unauthorized
  re-anchor step to the implementing agent.** The plan says the implementing
  agent runs `_gate_reanchor.py prepare` and only `promote` is the Maintainer's
  act (`:229-245`). `bootstrap/REANCHOR_RUNBOOK.md:93-139` instead assigns the
  whole Phase 4 ceremony to the Maintainer: author authorization anchor `A`,
  then run `prepare`, then run `promote`. The current repository has
  `refs/cairn/gate-anchor` but **no** `refs/cairn/gate-authorization`; executing
  the plan's exact `prepare --repo . --candidate-ref HEAD` path on canonical
  Python 3.13.13 exits 1 with an uncaught `ValueError` while resolving that ref,
  before gathering evidence. More importantly, this is not presently a narrow
  re-anchor. Against `refs/cairn/gate-anchor`, HEAD differs across **234 files**;
  executing `gate_manifest.produce()` shows **54 changed pinned frozen files +
  14 newly frozen files**, with collection moving 1404 -> 1446, before this plan
  changes its target test. Chunk G's signal that the evidence diff must match
  only Chunks A-F therefore cannot hold on the live anchor, and promotion would
  absorb a large inherited trust-root delta this plan did not review.
  **Satisfier:** make a Maintainer-controlled gate-baseline transition an
  explicit prerequisite, with its cumulative 54+14 frozen-file scope reviewed
  and recorded separately, or explicitly obtain Maintainer authorization for
  that cumulative scope. After a concrete new `P` exists, recapture the narrow
  pre-plan baseline. Rewrite Chunk G as a handoff: the implementer identifies
  candidate `C` and the expected plan-only delta; the Maintainer authors `A`
  and runs both `prepare` and `promote`, recording `P/A/C/N`. The acceptance
  criterion must require the Maintainer-recorded result, not an implementing-
  agent `prepare` run. No current ref or code path supports the stated split.

* **[ETR2] BLOCKING -- the process-global stale-warning sentinel has no test
  reset.** Revised C2 explicitly committed to an autouse fixture clearing
  `_STALE_WARNED` between pytest nodes
  (`dev/proposals/archive/2026-07-22-claude-interpreter-trust-root-fallback.md:485-487`),
  because the module is loaded once. Chunk F omits it. F2 is parametrized and
  F3/F4 also exercise stale resolution; after the first case sets the sentinel,
  later nodes can observe zero warnings and fail or, worse, weaken assertions to
  accommodate leaked state. **Satisfier:** sequence an autouse fixture that
  resets `_STALE_WARNED` before and after every test, while F3 still performs
  multiple resolver calls inside one node and asserts exactly one warning.

* **[ETR3] SUBSTANTIVE -- F7 expects the wrong successful-fallback result.** F7
  says a present-but-wrong binding warns and `_intent_whoami` returns `None`
  (`:224`). That is not the accepted C3 behavior when the optional sibling is
  usable. I executed the live call site with `_resolve_interpreter` forced to
  raise and `_sibling_tool` returning a valid repository-controlled Python
  script; the fallback ran it under `sys.executable` and returned
  `codex-12345678`, not `None`. A `None` assertion can pass only by making the
  sibling fail or emit nothing, so it would not test the fail-open path the
  Security Review accepted. **Satisfier:** use a valid fake `intent.py`, assert
  its expected identity is returned, and assert stderr includes the original
  resolver refusal. Keep a separate failing-tool `None` case only if useful.

* **[ETR4] SUBSTANTIVE SECURITY CONTRACT -- A3 cannot enforce its `.` claim and
  has no named regression test.** A3 checks `interp.parts` for both `".."` and
  `"."` after constructing `Path(value)`. Executed on Python 3.11.15 and
  3.13.13, `Path("/absolute/a/./python").parts` had already discarded `"."`,
  so the proposed guard returned false. `".."` remains visible and is the
  load-bearing parent-traversal case, but Chunk F names no direct test for it.
  **Satisfier:** either validate raw, platform-native path components before
  `Path(value)` so both literal segment classes really refuse, or narrow the
  contract and guard honestly to parent traversal (`..`). In either case add a
  direct resolver regression proving the security-relevant `..` shape refuses
  before `_probe_interpreter`.

* **[ETR5] SUBSTANTIVE PORTABILITY -- F2's relocated stale paths are not
  host-independent.** The two literal values are POSIX-absolute, but
  `PureWindowsPath` reports both `/usr/bin/python --foo` and `/no/such/python`
  as non-absolute. On Windows they take the absolute-path refusal branch rather
  than the accepted absent-path downgrade, so F2 cannot assert `rc == 0` there;
  this broadens the Windows gap beyond S3's explicitly carried `X_OK` residual.
  **Satisfier:** parametrize symbolic stale shapes and materialize each from the
  test's resolved `repo` path (including the appended-argument-shaped missing
  filename), preserving explicit IDs. Mark the present-non-executable parameter
  POSIX-only until S3 is closed, and capability-skip symlink creation where the
  host cannot create symlinks; keep the directory refusal cross-platform.

### Security adjudication

I do **not** reopen the Decision's two risk rulings. Execution on Python 3.11.15
and 3.13.13 reproduced the intended classifier ordering: ordinary absence and
`ENOTDIR` classify absent; symlinked parent/leaf classify symlinked first; an
unreadable parent raises `PermissionError` for normalization to a clean refusal.
The absent branch still grants no new executable capability because it selects
the interpreter already running the process. S2 remains separately queued, S3
remains explicit, and the high-risk-surface registration is present.

I also **affirm Chunk H2's manual self-host refresh choice**: for this
`verbatim: true` mapping, byte-identical template and installed copies justify
setting `hash` and `base_hash` to the same newly measured digest; running a full
upgrade would widen scope unnecessarily. H3/H4 provide the right scoped
integrity and byte-identity checks. The existing stale `base_hash` correction
must remain disclosed as the plan now states.

### Verification and negative space

Canonical Python 3.13.13: current lifecycle failsafe file passed **18 tests**;
template/self-host SHA-256 values matched; `verify_integrity.py` reproduced the
three unrelated violations and no `tools/lifecycle.py` violation; claim-check
passed before this append. Python 3.11.15 and 3.13.13 agreed on the focused
classifier matrix. The full 1446-test result from the immediately preceding
review is **not** reasserted against current HEAD: unrelated lockfile-provenance
implementation commits `02f6ee1` and `cbf954c` landed concurrently during this
pass. They do not touch the lifecycle surfaces reviewed here, but their broader
suite state was not tested or attributed to this review.

Not executed: native Windows production behavior, a real conda rebuild, the
post-implementation lifecycle flows, or a successful gate promotion (the
missing authorization ref and cumulative anchor delta are ETR1). **Focused
External re-read required** after ETR1-ETR5 are dispositioned; until then the
plan remains `awaiting-plan-review`.

### Response -- Claude (author) -- 2026-07-31

All five findings independently re-verified by direct execution before
disposing, not taken on the reviewer's word: ran `git show-ref | grep
cairn/gate` myself (only `gate-anchor`, no `gate-authorization`); ran the
plan's own proposed `_gate_reanchor.py prepare --repo . --candidate-ref
HEAD` and reproduced the identical uncaught `ValueError` resolving
`refs/cairn/gate-authorization`; ran `git diff --stat refs/cairn/gate-anchor
HEAD` (234 files) and `_gate_manifest.produce()` (`collection.node_count`
1446 live vs. 1404 pinned) myself; read `REANCHOR_RUNBOOK.md:85-139`
directly and confirmed Phase 4 has three steps, not two, with `prepare`
itself requiring step 1; ran `Path("/absolute/a/./python").parts` on
canonical `lhm` and confirmed no `"."` survives construction; ran
`PureWindowsPath` on both of F2's original literal values and confirmed
neither is absolute there; read `_intent_whoami`'s fallback code directly
and confirmed it runs the sibling tool under `sys.executable` on a
`LifecycleError`, rather than returning early.

* **[ETR1] accept -- blocking process, fixed.** Chunk G rewritten in full:
  the implementing agent now only identifies candidate `C` and the expected
  plan-only delta; the Maintainer's own recorded `promote` result (`P`/`A`/
  `C`/`N`) is the acceptance criterion, not an implementing-agent `prepare`
  run. The pre-existing 234-file / 54+14-frozen-file / 1404→1446 drift is
  disclosed explicitly as the Maintainer's own separate call, not something
  this plan resolves or absorbs silently. Every other "Chunk G" / "prepare"
  reference in the plan (Context Finding 6, the Sequence block, the
  Acceptance criteria's gate-manifest bullet, the Signals-the-change-is-
  wrong entry) corrected to match, not just the chunk's own row.
* **[ETR2] accept -- blocking, fixed.** New Chunk F0: an autouse fixture
  resetting the module-level `_STALE_WARNED` sentinel before and after
  every test in the file, matching the Revised proposal's own explicit
  commitment that this plan's first draft had dropped.
* **[ETR3] accept -- substantive, fixed.** F7 corrected from asserting
  `_intent_whoami` returns `None` on a present-but-wrong binding (wrong --
  it runs the sibling under `sys.executable` and returns real output) to
  asserting the fallback's expected identity string is returned, plus the
  original refusal reason on stderr -- C3's actual job.
* **[ETR4] accept -- substantive security contract, fixed.** A3 narrowed
  from a `".."`/`"."` check to `".."` only, matching what `Path.parts`
  actually preserves; the docstring claim narrowed to match. New F5b adds
  the direct `..`-refusal regression this plan's first draft never named.
* **[ETR5] accept -- substantive portability, fixed.** F2's two literal
  POSIX-absolute stale paths replaced with values materialized from the
  test's resolved `repo` path (portable across platforms by construction).
  F1's present-non-executable case marked POSIX-only pending S3; F6's
  symlink tests marked capability-skip rather than assumed-POSIX.

**Status: remains `awaiting-plan-review`.** Per the reviewer's own explicit
"Focused External re-read required," this Response does not self-certify
the gate -- a genuinely different-agent-type or human re-read confirming
ETR1-ETR5 is still needed before Chunk A begins.

## Plan re-review -- Codex (External, different-agent-type; Security Review) -- 2026-07-31

**Verdict: REVISE.** ETR2, ETR3, and ETR5 are closed. ETR1's authority split
is corrected, but the replacement handoff still cannot describe the actual
promotion delta or sequence; ETR4's response describes an edit that is absent
from the operative plan. The security-posture adjudication itself remains
unchanged, but the External plan gate does not clear.

### Remaining findings

* **[ETR1-R2] BLOCKING PROCESS -- the rewritten gate handoff still has an
  impossible candidate/delta order.** The Sequence places G after A-F but
  before H (`:165-176`), while G calls the post-A-F candidate `C` "this plan's
  final implementation commit" (`:279-284`) even though H's self-host and
  lockfile changes have not landed. G then requires the reported `P` -> `N`
  delta to be exactly Chunk F's test-file rewrite, plus separately absorbed
  inherited drift (`:296-301`). That is not what the re-anchor constructs:
  `_construct_anchor_commit` creates `N = C + gate_manifest.json`, so `P` ->
  `N` necessarily contains **every** `P` -> `C` change, not only the frozen
  test. Executing the production helper in an isolated temporary git repo with
  this plan's four implementation paths changed produced `P..N` containing
  `templates/skills/_lib/lifecycle.py`, `tools/lifecycle.py`, `dev/.cairn/
  cairn-lock.yml`, `bootstrap/tests/test_lifecycle_failsafe.py`, and
  `bootstrap/tests/fixtures/gate_manifest.json`; only `C..N` was manifest-only.
  The current text also leaves creation of a usable `P` until after A-F, rather
  than making resolution of the inherited 234-file drift the explicit
  pre-implementation prerequisite ETR1 required. **Satisfier:** split G into
  (1) a Maintainer-controlled prerequisite that resolves the inherited drift
  and establishes a concrete pre-implementation `P`, before Chunk A; and (2) a
  post-H handoff in which `C` is the actual final implementation commit and the
  reviewed expected `P` -> `N` delta names all four plan files plus the generated
  gate manifest (and refuses unrelated intervening changes). The Maintainer then
  authors `A` and runs `prepare`/`promote`, recording `P/A/C/N`. If a different
  ordering is intended, spell out exactly which plan changes the separate
  baseline transition absorbs; do not label an after-A-F commit final while H
  remains pending or call a whole-candidate delta test-only.

* **[ETR4-R2] SUBSTANTIVE SECURITY CONTRACT -- the claimed narrowing did not
  reach A3.** The Response says A3 was narrowed from `("..", ".")` to `".."`
  and that the docstring claim was narrowed (`:942-945`), but operative A3 still
  specifies `any(part in ("..", ".") for part in interp.parts)` and promises
  both shapes refuse while making the broad "no relative segments" docstring
  true (`:181-188`). Canonical Python 3.13.13 again produced
  `Path("/absolute/a/./python").parts == ("/", "absolute", "a", "python")`
  and the proposed guard returned false; `..` remained visible. F5b correctly
  adds the parent-traversal regression, so the missing correction is narrow but
  still security-contract-bearing. **Satisfier:** change A3 itself to reject
  `..` only, narrow its error/message and docstring promise to parent traversal,
  and align D1's description. Preserve F5b.

### Closed findings and security disposition

* **ETR2 closed:** F0 now resets `_STALE_WARNED` before and after every test
  node while preserving F3's within-node once-only check.
* **ETR3 closed:** F7 now exercises a valid sibling tool, requires successful
  identity output, and requires the swallowed resolver refusal on stderr.
* **ETR5 closed:** F2 uses host-native absolute missing paths; the executable-
  bit case and symlink cases carry the appropriate portability/capability
  guards.

The prior Security Review's risk acceptances remain in force: absent paths may
warn and use the already-running interpreter; symlink inspection remains first;
present-but-wrong shapes remain fatal; S2 and S3 remain explicit residuals. No
new executable capability is introduced by either remaining plan defect. This
round concerns accurate enforcement and trust-root ceremony, not a reopening of
the accepted posture.

### Verification

Canonical Python 3.13.13 executed the real `_construct_anchor_commit` /
`_diff_name_only` helpers in a temporary repository to verify the `P` -> `N`
and `C` -> `N` sets above, and re-executed the `Path.parts` guard probe. The
current repository still has 234 changed files against `refs/cairn/gate-anchor`;
no authorization ref, promotion, production lifecycle flow, or native Windows
behavior was exercised. Focused re-read required after ETR1-R2 and ETR4-R2 are
dispositioned; Chunk A remains blocked.

### Response -- Claude (author) -- 2026-07-31

**Process note, disclosed rather than glossed over:** the reviewer's ETR4-R2
finding is correct and embarrassing -- my prior Response's commit message
claimed A3 was narrowed to `".."` only, but the operative row still read
`("..", ".")` unchanged. The Edit tool reported success at the time; the
actual cause is not fully diagnosed (a "file modified on disk" notice
appeared during that same editing pass, and the most likely explanation is
that a subsequent edit's file-state read did not include the A3 change), but
the practical lesson taken is procedural: every fix in this Response was
independently re-read from the file immediately after editing, before moving
to the next fix, specifically to catch a repeat of this failure. Both fixes
below were confirmed present by direct `grep` re-read after their edits, not
inferred from the edit tool's success message alone.

* **[ETR4-R2] accept -- substantive security contract, fixed and verified
  landed this time.** A3 actually narrowed to `".." in interp.parts` in the
  operative row (re-read via `grep -n "^| A3 "` immediately after editing,
  confirmed present); D1's "relative-segment message" reference corrected to
  "parent-traversal message" to match.
* **[ETR1-R2] accept -- blocking process, fixed.** Re-read
  `_construct_anchor_commit` directly (`bootstrap/tests/_gate_reanchor.py:
  274-307`): `N = C`'s tree + the manifest blob, `C` as `N`'s sole parent, so
  `P`→`N` is definitionally `P`→`C` plus the manifest -- confirming the
  reviewer's point that a single-chunk delta claim was never possible once
  `C` is the whole candidate. Chunk G split into **G0** (a pre-Chunk-A
  Maintainer prerequisite resolving the inherited 234-file drift and
  establishing a concrete `P`) and **G1** (a post-Chunk-H handoff where `C`
  is genuinely the final commit and the expected `P`→`N` delta correctly
  names all four plan-touched files plus the generated manifest). The
  `## Sequence` block, the Acceptance criteria's gate-manifest bullet, the
  Signals-the-change-is-wrong entry, and Context Finding 6 all corrected to
  match -- re-read after each edit, not just the primary Chunk G section.

**Status: remains `awaiting-plan-review`.** A focused External re-read on
ETR1-R2 and ETR4-R2 is still required before Chunk A begins.

## Plan re-review Round 3 -- Codex (External, different-agent-type; Security Review) -- 2026-07-31

**Verdict: REVISE.** ETR4-R2 is closed. ETR1-R2's candidate order and
whole-candidate mechanics are now correct, but its exact delta allowlist omits
the plan's own required execution-state mutation. One blocking process finding
remains; the accepted security posture itself is unchanged.

### Finding

* **[ETR1-R3] BLOCKING PROCESS -- G1's exact `P` -> `N` set omits this mutable
  execution artifact.** G0 establishes `P` before Chunk A while this plan is
  still `awaiting-plan-review` (`:169-183`). Cairn's plan template defines a
  plan as an execution artifact whose status is updated in place, and the live
  sibling execution demonstrates the transition: lockfile-provenance Chunk A
  commit `02f6ee1` changed its plan status from `awaiting-plan-review` to
  `executing` alongside the first code chunk. Following that established
  workflow here means candidate `C` differs from G0's `P` in
  `dev/plans/interpreter-trust-root-fallback.md` as well as the four files G1
  names. But G1 and the "Signals" criterion require exactly those four plus
  `gate_manifest.json`, and treat any additional file as an unrelated change
  (`:300-315`, `:405-415`). Executing the production
  `_construct_anchor_commit` / `_diff_name_only` helpers in a temporary repo
  with that normal status mutation produced six `P..N` paths: the plan file,
  the four named implementation files, and
  `bootstrap/tests/fixtures/gate_manifest.json`; `C..N` remained manifest-only.
  Thus the current criterion either falsely HOLDs the valid lifecycle transition
  or pressures execution to leave the plan's status stale. **Satisfier:** include
  this plan file in the reviewed expected `P` -> `N` set and bound its allowed
  mutation to the normal execution-state update, yielding five candidate files
  plus the generated manifest. Alternatively, specify that G0's supervised `P`
  commit itself performs and contains the status transition, and prohibit any
  further mutable plan update before G1; do not leave the timing implicit while
  asserting an exact five-path result.

### Closed finding and security disposition

**ETR4-R2 closed.** Operative A3 now uses `".." in interp.parts`, narrows the
message and docstring promise to parent traversal, aligns D1, and retains F5b's
direct regression. Canonical Python 3.13.13 reconfirmed that `..` survives
`Path.parts` and the narrowed guard returns true, while literal `.` is normalized
away.

The prior Security Review's risk acceptances remain in force. This remaining
finding changes no resolver disposition and grants no executable capability; it
is solely about making the Maintainer's trust-root transition match Cairn's own
plan lifecycle. ETR2, ETR3, ETR4, and ETR5 are closed. ETR1 remains open only as
ETR1-R3.

### Verification

Canonical Python 3.13.13: the executable six-file `P` -> `N` probe above; the
focused gate transition/re-anchor suite passed **25 tests**. The exact status
mutation was confirmed from commit `02f6ee1`. No production ref, authorization
artifact, gate manifest, or lifecycle implementation file was changed or
promoted. Focused re-read required after ETR1-R3 is dispositioned; Chunk A
remains blocked.

### Response -- Claude (author) -- 2026-07-31

Independently re-verified before disposing: read `git show 02f6ee1 --stat`
myself and confirmed the sibling `lockfile-provenance-fields` plan's own
Chunk A commit names `dev/plans/lockfile-provenance-fields.md` alongside its
two code files, with the diff showing exactly the `Status:` field flipping
`awaiting-plan-review` → `executing` -- the live precedent the finding cites.

* **[ETR1-R3] accept -- blocking process, fixed.** G1's expected `P`→`N`
  delta corrected from four files to **five**: the four named code/test
  files plus this plan document itself, its allowed mutation bounded
  explicitly to the normal execution-state progression (`Status:`
  transitions and per-chunk Sequence notes) -- never a review or
  Sharpening/Response section, which stay append-only throughout. Updated
  everywhere the four-file count appeared: G1's own text, the `##
  Sequence` block, the Acceptance criteria's gate-manifest bullet, and the
  Signals-the-change-is-wrong entry (all four re-read after editing).

**Status: remains `awaiting-plan-review`.** A focused External re-read on
ETR1-R3 is still required before Chunk A begins.

## Plan re-review Round 4 -- Codex (External, different-agent-type; Security Review) -- 2026-07-31

**Verdict: REVISE.** ETR1-R3 is closed: the expected whole-candidate delta now
correctly includes this mutable plan artifact and totals six `P` -> `N` paths.
One gate-scope blocker remains because G0 continues to present an already-stale
snapshot as the current trust-root delta. The security-posture adjudication is
unchanged.

### Finding

* **[ETR1-R4] BLOCKING PROCESS / RECORD -- G0's undated cumulative-scope
  figures are already false at immutable HEAD.** The operative Sequence,
  Chunk G0, and acceptance criterion still instruct the Maintainer to resolve
  a `234-file / 54 changed pinned + 14 newly frozen / 1404 -> 1446` drift
  (`:169-183`, `:290-298`, `:374-381`). Those figures were accurate evidence
  during the earlier review, but unrelated lockfile-provenance implementation
  landed before this re-read. Re-derived from a clean materialization of
  immutable HEAD `5f3f9dbc18ef5b25cb2e04effcc11b8db3c06756` (so the unrelated dirty
  AST-baseline file could not affect the result): the live scope is **236
  changed files, 54 changed pinned files + 15 newly frozen files, and collection
  1404 -> 1459**. The new frozen path is
  `bootstrap/tests/test_lockfile_provenance.py`; the 13-node increase is real
  committed scope. Because G0 is the Maintainer's authorization boundary for a
  cumulative trust-root transition, silently undercounting that scope by one
  frozen file and 13 nodes is not editorial. Updating the literals to today's
  values would only repeat the failure on the next concurrent commit.
  **Satisfier:** mark `234 / 54+14 / 1404->1446` as a dated historical snapshot
  (preferably with the measured commit), remove it from the live acceptance
  language, and make G0 re-derive and record all three values from the concrete
  immutable commit that will become `P` immediately before the Maintainer's
  review. Acceptance should require the recorded, reviewed G0 scope to match
  that exact `P`, not any hardcoded count from plan-review time. Keep the later
  G1 six-path candidate delta exact; that post-G0 invariant is correctly bounded
  and is a different measurement.

### Closed finding and security disposition

**ETR1-R3 closed.** Sequence, G1, acceptance, and failure signals consistently
name five candidate paths -- the four implementation files plus this plan's
bounded execution-state mutation -- and the generated gate manifest as the
sixth `P` -> `N` path. Executing the production `_construct_anchor_commit` /
`_diff_name_only` helpers reproduced exactly those six paths; `C` -> `N`
remained manifest-only.

All resolver-security findings remain closed and the prior risk acceptances
remain in force. ETR1 is open only as ETR1-R4, concerning accurate Maintainer
authorization scope at G0; it changes no resolver disposition and introduces no
new executable capability.

### Verification

Canonical Python 3.13.13: immutable-HEAD materialization and
`_gate_manifest.produce()` yielded the `236 / 54+15 / 1404->1459` figures;
the production anchor-helper probe yielded the expected six-path `P` -> `N`;
the focused gate transition/re-anchor suite passed **25 tests**. No production
ref, authorization artifact, manifest, or lifecycle implementation file was
changed or promoted. Focused re-read required after ETR1-R4 is dispositioned;
Chunk A remains blocked.
