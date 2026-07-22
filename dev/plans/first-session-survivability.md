<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/lifecycle.md doctrine/session-routines.md doctrine/onboarding.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: bootstrap/tests/test_first_session_report.py, bootstrap/tests/test_onboarding_seed_roster.py -->
<!-- The two paths above are forward-reference files this plan creates; they materialize as the chunks land. -->

# Plan: first-session survivability (F1, F3, F4)

**Source proposal**: `dev/proposals/archive/2026-07-11-claude-first-session-survivability.md`
**Status**: executing
**Plan review**: required(Internal) — ratified at Decision; F1/F3 touch the
scaffold engine (a new install-set signature + preset-template conditional
markers) and this plan pins the exact wording/markers the proposal left to
plan stage. F2 (the interpreter trust-root degrade) is explicitly out of
scope — carved out at Decision to its own Security-Reviewed proposal.
**Last update**: 2026-07-22
**Opened**: 2026-07-22

## Source proposal

The accepted proposal fixes three of four verified day-one adoption
breakers: a phantom `/good-morning` command plus a silently-dropped skills
skip (F1); onboarding seeds that command tools/docs the resolved module
roster never staffed (F3); and `session-start`'s self-description
overclaiming "read-only" when it performs one idempotent self-heal write
(F4). F2 (graceful degrade on a moved interpreter, the security trust-root
finding) was split out at Decision to its own Security-Reviewed proposal —
already open and independently in progress as
`dev/proposals/2026-07-22-claude-interpreter-trust-root-fallback.md` — and
is untouched by this plan. The proposal cleared a 3-lens Internal panel (12
findings, all accepted) and a Gemini External SHIP; the Decision ratified
F1/F3/F4 and required a supervised AST re-anchor for F1 (`cli.py`) + F3
(`install.py`, `config.py`-adjacent) since they touch the scaffold engine.

## Proposed paths

Proposed paths:
- `bootstrap/tests/test_first_session_report.py` — the F1 behavioral test; lands with the F1 implementation commit.
- `bootstrap/tests/test_onboarding_seed_roster.py` — the F3 drift guard; lands with the F3 implementation commit.

## Scope

Implements F1, F3, F4 as revised (the proposal's `## Revised proposal`
section is authoritative — it corrects the original's `high-rigor-legacy.md`
factual error, the wrong test citations, and the axes-dict inconsistency).

**Scope fence (what this does NOT do):** F2 (the `_resolve_interpreter`
absent-vs-tamper carve in `templates/skills/_lib/lifecycle.py`) is not
touched — it has its own proposal and Security Review already in progress
independently. This plan's F4 edits are in the *same file* as F2 but at
different, non-overlapping locations (docstring/parser text only); no
functional interaction.

**The re-anchor gate, corrected (per the adopter-licensing-compliance
plan's finding, carried forward here).** The Decision's "supervised AST
re-anchor per `bootstrap/REANCHOR_RUNBOOK.md`" citation is the same error
found and corrected in that sibling plan: `REANCHOR_RUNBOOK.md`'s Phase 0/4
ceremony does not govern `bootstrap/tests/fixtures/scaffold_ast_baseline.json`
(`bootstrap/tests/_gate_manifest.py`'s `CASCADE_MUTABLE` dict explicitly
excludes it). The real mechanism is `bootstrap/tests/_ast_attest.py
update-symbol`. **Good news carried from the sibling plan's Chunk D
close-out:** the previously-blocking pre-existing drift
(`FunctionDef:print_report`) is **already resolved** (commit `e1eec63`,
independently re-confirmed by this plan's own plan-review: `test_ast_attest.py`
is clean, 26 passed, under the canonical `lhm` interpreter *before* this
plan's edits land) — so every CHANGED symbol after Chunks A/B lands will be
this plan's own, not inherited noise.

**Three symbols, not one, after the PR1 fix (B1b).** `FunctionDef:main`
(`cli.py`, Chunk A) and `FunctionDef:install_onboarding` (`install.py`,
Chunk B1) were the two originally expected; `install_onboarding` alone is
allowlisted (`_UPDATE_ALLOWLIST`: `_MODULE_MAPPINGS`/`_SKILLS_MAPPINGS`/
`_CORE_MAPPINGS`/`install_onboarding`). B1b's fix to
`write_install_lockfile` (also `install.py`) adds a **third** CHANGED
symbol, `FunctionDef:write_install_lockfile` — not allowlisted either. All
three still need the same Maintainer-run, dry-run-verified script pattern
used for the licensing plan's Chunk D (load the committed baseline, verify
the live CHANGED set is *exactly* the expected keys, surgically update only
those digests+spans, everything else byte-for-byte untouched) — just
targeting three keys instead of one. The new shared helper
`_rendered_onboarding_overlay` (B1) will show as a tolerated **NEW** symbol
(informational only, per `verify()`'s "new top-level symbols are allowed...
but reported" behavior) — not a blocker.

### Documentation / doctrine surface

Scaffold engine (`bootstrap/_scaffold/cli.py`, `install.py`) + adopter
preset templates (`templates/onboarding/collaborative-team.md`,
`high-rigor-legacy.md`) + a shipped tool's self-description
(`templates/skills/_lib/lifecycle.py`, text-only). No doctrine change —
F1/F3 are engine/template fixes; F4 aligns shipped text to *already-accepted*
doctrine (`doctrine/session-routines.md:66-67`). Per plan-review R6 in the
source proposal, `doctrine/onboarding.md` is the doctrine describing the
roster-dependent-seed mechanism F3 modifies — named here as the relevant
citation surface, not edited.

<!-- cairn:slot documentation-tier-home -->
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
plan's *Scope* must name the doctrine-surface touched (or an explicit
"no doctrine surface").
<!-- cairn:end documentation-tier-home -->

## Sequence

```
A. F1 -- honest fan-out report + real invitation (cli.py)         [commit pending]
B. F3 -- gate onboarding seeds by the resolved roster              [commit pending]
C. F4 -- correct session-start's self-description (lifecycle.py)   [commit pending]
D. Supervised AST correction (Maintainer-gated; not this agent's act) [parked]
```

### Chunk A — F1 (honest fan-out report + real invitation)

| # | File | Change |
|---|------|--------|
| A1 | `bootstrap/_scaffold/cli.py` | Drop the phantom `(/good-morning)` parenthetical from the skills-install closing line (currently ``Try `session-start` (/good-morning).``) — leave only the real invocation, ``Try `python tools/lifecycle.py session-start`.`` |
| A2 | `bootstrap/_scaffold/cli.py` | Replace the fan-out report's silent drop of `skipped-vendor-absent` (`if status not in ("noop", "skipped-vendor-absent"): print(...)`) with an always-printed, calm, no-action line for that status specifically — per the Revised proposal's R11 correction: *"Skills link automatically the first time you launch your harness — no action needed."* — naming the harness from the row, matching the existing copy/symlink rows' format. `noop` stays silently filtered (genuinely nothing happened, not a "will happen later" state). |
| A3 | `bootstrap/tests/test_first_session_report.py` (new) | (i) the closing line contains no `/good-morning` and does contain the real `python tools/lifecycle.py session-start` invocation; (ii) a fresh scaffold into a target with no `.claude/` directory prints the calm advisory line for the `claude-code` row, and that line contains neither "skipped" nor "error" (R11's exact requirement). |

### Chunk B — F3 (gate onboarding seeds by the resolved roster)

| # | File | Change |
|---|------|--------|
| B1 | `bootstrap/_scaffold/install.py` | **New shared helper** `_rendered_onboarding_overlay(preset_name, preset_text, axes) -> str`: `strip_conditional_regions(preset_text, axes or {})` → `_extract_seed_tasks(...)` → `_render_onboarding_slot(preset_name, seed_blocks)`, returning the final slot content in one call. Add `axes: dict | None = None` as a **keyword-only** parameter to `install_onboarding` (backward-compatible with the three existing positional 3-arg call sites in `test_upgrade_side_door_parity.py`, verified this session) and switch its write-C computation to call the new helper instead of the raw `_extract_seed_tasks`/`_render_onboarding_slot` pair. The verbatim preset-source copy (write D) is untouched — it stays the full authoritative reference the goodnight helper reads for deferred tasks. |
| B1b | `bootstrap/_scaffold/install.py` | **Critical fix, per plan-review PR1.** `write_install_lockfile`'s separate `onboarding_overlay` precompute (`:1499-1511`) calls the *raw*, unstripped `_extract_seed_tasks`/`_render_onboarding_slot` pair — a second, independent call site B1 alone does not touch. Left as-is, the very first real (non-`--dry-run`) install of `collaborative-team` + an axes override that strips a seed would fail closed: `install_onboarding`'s actual on-disk `PLANNING.md` (stripped) would diverge from `write_install_lockfile`'s `would` value (unstripped), tripping the fail-closed divergence guard (`:1547-48`) and refusing to write `dev/.cairn/cairn-lock.yml` — reintroducing, via F3's own fix, exactly the "don't lie about state" defect class F3 exists to close. Switch this call site to the **same** `_rendered_onboarding_overlay` helper (B1), passing `profile.get("axes") or {}` — the identical axes source the adjacent general-file strip loop two lines below already uses (`:1524-1533`). One shared helper, both call sites: they cannot drift apart again. |
| B2 | `bootstrap/_scaffold/cli.py` | Pass `axes=embedded_axes` at the `install_onboarding` call site (the same `embedded_axes` dict `install_core` already strips with, per R8 — **not** `resolved_axes`, so every strip site keys off one axes map and the `install.py` would-strip invariant at the lockfile-divergence check holds). |
| B2b | `bootstrap/tests/` (new, in `test_onboarding_seed_roster.py` or a live-install extension of `test_upgrade_side_door_parity.py`) | **The PR1 regression test.** A real (non-dry-run) scaffold install of `collaborative-team` + `agent_team: single` (and `+ agent_team: concurrent-single-type`) asserts `dev/.cairn/cairn-lock.yml` is written cleanly — not refused, no diverged-files message — proving B1b actually closes the gap. The `--dry-run` smoke check in Acceptance criteria exits before `write_install_lockfile` is ever reached (`cli.py:449`) and cannot substitute for this. |
| B3 | `templates/onboarding/collaborative-team.md` | Wrap `install-work-intent-hooks` (seed) and `read-coordination-doctrine` (seed) in `<!-- cairn:if agent_team in concurrent-multi-type,concurrent-single-type -->` / `<!-- cairn:endif -->` (mirrors `_TEAM_STAFFING_GATES["coordination-tiers"]` exactly). Wrap `read-dual-review-module` (seed) in `<!-- cairn:if agent_team in concurrent-multi-type -->` (mirrors `_TEAM_STAFFING_GATES["dual-review"]`). Wrap `agent-team-onboarding` (seed, R6 tour-seed extension) in `<!-- cairn:if agent_team in concurrent-multi-type -->` — it onboards a **second agent type**, which only `concurrent-multi-type` staffs; same gate as dual-review, not coordination-tiers. `sign-collab-agreement-day-one` is **left ungated** (see Author-accounting — it's about the human/agent roster generally, not agent-concurrency shape). |
| B4 | `templates/onboarding/high-rigor-legacy.md` | Wrap **only** `install-work-intent-hooks` in the same coordination-tiers gate (`concurrent-multi-type,concurrent-single-type`) — this preset carries no `read-coordination-doctrine`/`read-dual-review-module` seeds at all (R2's correction; verified this session, unchanged). Wrap `agent-team-onboarding-legacy` in the `concurrent-multi-type`-only gate (same reasoning as B3's `agent-team-onboarding`). `confirm-maintainer-authority` is left ungated (same reasoning as `sign-collab-agreement-day-one`). |
| B5 | `bootstrap/tests/test_onboarding_seed_roster.py` (new) | The broadened drift guard (R6), **two distinct assertion sets per plan-review PR2** (not one flat list — `concurrent-single-type` keeps `coordination-tiers`, only `dual-review` drops):<br>**(a)** `collaborative-team` × `agent_team: single` (unstaffs both `coordination-tiers` and `dual-review`) — assert the rendered slot references **none** of: `tools/intent.py`, the `doctrine/coordination.md` seed, the `dev/modules/dual-review.md` seed, the `agent-team-onboarding.md` seed.<br>**(b)** `collaborative-team` × `agent_team: concurrent-single-type` (unstaffs only `dual-review`) — assert **absence** of the `dev/modules/dual-review.md` and `agent-team-onboarding.md` seeds **and explicit presence** of `tools/intent.py` and the `doctrine/coordination.md` seed — proving the narrower gate doesn't over-strip coordination-tiers content it must keep.<br>**(c)** the **unconditional** case (no override) still renders all seeds — proving the gate is a real filter, not a silent no-op. |

**Author-accounting note on the two left-ungated seeds (`sign-collab-agreement-day-one`,
`confirm-maintainer-authority`).** Both are about *who is on the team*
(the `team-roster` slot in `dev/collaboration_agreement.md`), which matters
for any human team regardless of `agent_team`'s resolved value — a
`concurrent-single-type` or even `single` team still benefits from an
explicit roster (it's what makes even a same-vendor fresh-session Internal
review reproducible, per `doctrine/dual-review.md`). Gating them on
`agent_team` would incorrectly imply the roster only matters for multi-type
concurrency. This is this plan's own judgment call (the proposal deferred
the exact gate to plan stage); flagged for plan-review to confirm or
challenge.

**Confirmed by plan-review, with a residual noted (PR3).** The always-on
`team-roster` slot means leaving these two ungated never produces a
dangling file/tool reference — the drift guard's actual invariant holds.
But `sign-collab-agreement-day-one`'s own prose ("...the roster is what
makes Dual-Review's External tier structurally meaningful... which the
collaborative-team profile is sized past") stays literally accurate only
when `dual-review` is staffed — under this plan's own `agent_team: single`
reproduction it isn't, yet the seed still asserts the team is "sized past"
same-vendor review. This is a conceptual-accuracy residual (not a dangling
surface reference), so B5's drift guard correctly does not catch it, and
this plan does not attempt a prose fix for it — recorded here as a known,
accepted gap for a future pass, not silently left unrecorded.

### Chunk C — F4 (correct `session-start`'s self-description)

| # | File | Change |
|---|------|--------|
| C1 | `templates/skills/_lib/lifecycle.py` | Module docstring: reword "Every side-effecting subcommand honors `--dry-run`: it prints the planned writes and exits writing nothing." to scope the claim to `session-end` only, and state `session-start`'s one exception plainly: it performs one idempotent write (the skills fan-out self-heal) regardless of any flag, matching `doctrine/session-routines.md:66-67`'s existing framing ("The only write the routine itself makes is the tool's idempotent skills self-heal, not the agent's"). |
| C2 | `templates/skills/_lib/lifecycle.py` | Parser `description=`: reword "Read-only orientation and reflection-only goodnight; no network." to "Orientation gather (plus one idempotent skills-fan-out self-heal write) and reflection-only goodnight; no network." |
| C3 | `templates/skills/_lib/lifecycle.py` | `session-start` subparser `help=`: reword "Read-only orientation gather (commits, tree state, threads, intents)." to name the one write, matching C2's phrasing. **Note:** `cmd_session_start`'s own function docstring is *already* accurate (confirmed this session — it already reads "Orientation gather (read-only) + idempotent skills fan-out self-heal") and needs no edit; only the module docstring and the two parser-level strings overclaim. |
| C4 | `bootstrap/tests/test_lifecycle_cli.py` (extend) | Text-assertion test: the built parser's top-level `description` and the `session-start` subparser's `help` text each mention the skills-fan-out self-heal write and neither claims "read-only" unqualified; the module docstring's `--dry-run` claim is scoped to `session-end`. **Also** (plan-review PR4, optional, same file already open): this test file's own module docstring carries the identical "read-only" overclaim about `session-start` it now asserts against the shipped tool — reword it in the same commit, in the spirit of the theme, though it's test-internal prose, not adopter-facing, and outside F4's stated scope. |

**Twin-parity note (B1-C3, same principle as the sibling licensing plan's P2).**
`templates/skills/_lib/lifecycle.py` self-hosts as `tools/lifecycle.py`
(byte-identical twin, per `install.py`'s divergence/base-hash check). Every
edit in Chunk C lands in the `templates/` source; the same edit is applied
identically to `tools/lifecycle.py` in the same commit so the pair stays
byte-identical, verified by direct `diff`.

## Acceptance criteria

* **Tests that must pass** — `bootstrap/tests/test_first_session_report.py`
  (new, F1); `bootstrap/tests/test_onboarding_seed_roster.py` (new, F3);
  the extended `bootstrap/tests/test_lifecycle_cli.py` (F4); the existing
  `install_onboarding` callers (`test_install_module.py`,
  `test_security_leaf.py`, `test_upgrade_side_door_parity.py`) stay green
  unmodified (the new `axes` parameter is keyword-only with a `None`
  default, verified backward-compatible with all three positional call
  sites this session). The full `python -m pytest bootstrap/tests` suite
  green **modulo**: the two `test_ast_attest.py` symbols this plan's own
  Chunk A/B introduce (until Chunk D lands) and the separately-tracked
  clock-expired `test_evolution_infer.py` case — run under the canonical
  `lhm`/Python 3.13 interpreter, since the sandbox default (3.12) produces
  spurious digest mismatches unrelated to real drift (confirmed
  empirically on the sibling licensing plan).
* **Doc updates that must land** — the two onboarding preset templates
  (B3, B4); no other doc changes (F4 is code/parser text, not a doc file).
* **Examples / smoke checks required** — `python bootstrap/scaffold.py
  --dry-run --config <collaborative-team + agent_team:single>` shows the
  roster-gated seed with no `tools/intent.py`/coordination-doc reference;
  a scratch install into a target with no `.claude/` prints the calm
  advisory line; `python scripts/check_cairn.py` clean over the two edited
  templates; `python scripts/claim_check.py` clean over this plan and the
  two new test files.
* Inbound path-link updates: none required (`PLANNING.md` / `NEXT_SESSION.md`
  refer to plans by filename stem).

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.** (i) The install report names no command that is not
  installable, and never silently drops a `skipped-vendor-absent` row —
  *enforced by* `test_first_session_report.py`. (ii) A rendered onboarding
  seed references no tool/doc surface the resolved roster did not install —
  *enforced by* `test_onboarding_seed_roster.py`. (iii) `session-start`'s
  self-description matches `doctrine/session-routines.md:66-67` —
  *enforced by* the extended `test_lifecycle_cli.py`. (iv) The
  `templates/skills/_lib/lifecycle.py` ↔ `tools/lifecycle.py` twin stays
  byte-identical — *enforced by* a direct `diff` check in Chunk C's
  verification (matching the licensing plan's parity-check precedent).
* **Failure modes.** F1/F4 are report/text accuracy — a regression is
  visible, not silent. F3's drift guard is fail-closed (a re-drifted
  condition turns the suite red). The AST-baseline drift Chunks A/B
  introduce (three symbols: `main`, `install_onboarding`,
  `write_install_lockfile` — see the Scope section's re-anchor note) is
  entirely this plan's own, expected drift — no inherited noise, since the
  sibling plan's Chunk D already cleared the one pre-existing blocker.
* **Edge cases.** F3: a preset with no roster-dependent seed
  (`solo-greenfield`) is a no-op (it carries none of the gated seed IDs);
  an axis absent from `axes` keeps the content (conservative
  keep-on-missing-axis default, unchanged); `concurrent-single-type`
  keeps the coordination seeds but drops the dual-review seed and the
  tour seed (the two gates differ, verified). F1: `.claude/` present →
  fan-out proceeds unchanged, no advisory line printed (only the
  `skipped-vendor-absent` status triggers it).
* **Public-path → test mapping.** `cli` install-report path →
  `bootstrap/tests/test_first_session_report.py`; `install_onboarding`
  roster gating → `bootstrap/tests/test_onboarding_seed_roster.py`;
  `session-start` self-description → `bootstrap/tests/test_lifecycle_cli.py`.
* **Known omissions.** F2 (interpreter degrade) is fully out of scope —
  own proposal, in progress. No `--dry-run` added to `session-start`
  (the proposal's own deferred feature, unrelated to F4's text-only fix).

## Verification

```
python -m pytest bootstrap/tests
python -m pytest bootstrap/tests/test_first_session_report.py bootstrap/tests/test_onboarding_seed_roster.py bootstrap/tests/test_lifecycle_cli.py -v
/Users/kendal30/conda_envs/lhm/bin/python3 -m pytest bootstrap/tests/test_ast_attest.py -q   # canonical interpreter; see Scope note
python scripts/check_cairn.py
python scripts/claim_check.py <each changed/new file>
python scripts/quality_gate.py --sub neutrality
diff templates/skills/_lib/lifecycle.py tools/lifecycle.py   # twin parity
```

## Plan review -- Claude (Internal, fresh-context) -- 2026-07-22

**Attribution / committer note.** Fresh-context subagent read of this plan (Internal floor: same agent type, fresh session, no access to the plan-authoring session). The subagent cannot commit; per the accepted deviation model used throughout this repo's lifecycle (`dev/plans/archive/review-record-integrity.md`), whoever invokes this review commits it as a disclosed scribe.

**Model**: Claude Sonnet 5 (fresh session; read the plan, the full accepted proposal record including the Revised proposal / Gemini External review / Decision, and independently re-derived every concrete claim this review names against the live tree as of 2026-07-22).

**Steelman.** This plan is a faithful, disciplined translation of the *Revised* proposal, not the original — every place the original had a factual error (the `high-rigor-legacy.md` seed-count claim, the wrong `install_onboarding`-caller test citations, the `resolved_axes`-vs-`embedded_axes` inconsistency) is correctly carried forward in its *corrected* form, and nothing from the Revised proposal or the Decision's ratified scope (F1+F3+F4, F2 carved out) is silently dropped. Every concrete specific I independently re-derived reproduced exactly: `collaborative-team.md` really carries all three named coordination/dual-review seeds plus the tour and roster seeds (read live), `high-rigor-legacy.md` really carries only `install-work-intent-hooks` among those (read live, zero `read-coordination-doctrine`/`read-dual-review-module` hits) — the plan's B3/B4 gate assignments match `_TEAM_STAFFING_GATES` (`config.py:874-879`) exactly, including the well-reasoned extension of the dual-review gate (`concurrent-multi-type` only) to the two tour seeds on "second agent *type*" grounds, which the axis-comment at `config.py:867-873` independently corroborates. The phantom `/good-morning` line and the `skipped-vendor-absent` filter are exactly where and as described (`cli.py:487`, `:502-504`). `install_onboarding`'s current signature (`install.py:924-931`) has no `axes` param, and all three real call sites in `test_upgrade_side_door_parity.py` (`:335,346,430`) are 3-positional-or-fewer, confirming the keyword-only-with-default design is genuinely backward compatible; `test_install_module.py`/`test_security_leaf.py` reference `install_onboarding` only as a bare string in guard/identity sets, never as a direct call, exactly as claimed. `cmd_session_start`'s own docstring (`lifecycle.py:633`) is already byte-for-byte the corrected text the plan says it is — a claim I verified rather than trusted, and it holds. The `templates/skills/_lib/lifecycle.py` ↔ `tools/lifecycle.py` twin is confirmed byte-identical today (`diff`, zero output). The AST re-anchor framing is the most impressively re-verified part of the plan: I ran `bootstrap/tests/test_ast_attest.py` under the canonical `lhm` interpreter and it is clean (26 passed) — the sibling licensing plan's Chunk D close-out claim holds, so this plan's own Chunk A/B symbols (`main` in `cli.py`, `install_onboarding` in `install.py`) really will be the *only* drift, and the `_UPDATE_ALLOWLIST` (`_ast_attest.py:141-146`) really does contain exactly `_MODULE_MAPPINGS`/`_SKILLS_MAPPINGS`/`_CORE_MAPPINGS`/`install_onboarding`, confirming `install_onboarding`'s Chunk-B edit is surgically covered while `main`'s Chunk-A edit correctly needs the parked Chunk D. A full `bootstrap/tests` run under the canonical interpreter shows exactly one failure — the separately-tracked clock-expired `test_evolution_infer.py` case — matching the plan's "green modulo" claim precisely.

**Critiques** (descending severity):

* **[PR1] (blocking)** Chunk B leaves a second, independent `_extract_seed_tasks` call site unpatched, and it will regress the install lockfile the instant Chunk B ships — invisible to the plan's own designated smoke check. `_extract_seed_tasks`/`_render_onboarding_slot` are called from exactly two places in `install.py`: `install_onboarding` (`:1054-1055`, the one Chunk B1 patches) and `write_install_lockfile` (`:1508,1511-1512`, computing the `onboarding_overlay` used to build the lockfile's expected-clean-install `would` value for `dev/PLANNING.md`). The second call site reads `preset_src.read_text(...)` **raw** — it never calls `strip_conditional_regions`, unlike the general per-file loop two lines below it which explicitly does (`:1531-1533`, keyed off `profile.get("axes")`). Once Chunk B1 makes `install_onboarding` strip the preset text by axes before extracting seeds, the *actual* on-disk `dev/PLANNING.md` for an axes override that unstaffs a module will be correctly stripped, but `write_install_lockfile`'s `would` for that same file will still be computed from the **unstripped** seed list — a mismatch. `write_install_lockfile` is fail-closed by design (`:1453-1454` docstring; `:1547-1548` `if on_disk is None or on_disk != would: diverged.append(...)`; `:1572-1577` prints "`cairn-lock.yml` NOT written: N installed file(s) differ from a clean install" and returns `None`). Concretely: for `collaborative-team` + `agent_team: single` — the plan's own reproduction scenario and the Acceptance criteria's designated smoke check — a real (non-`--dry-run`) install will, post-Chunk-B, silently fail to write the upgrade-ancestor lockfile on every such install, with a confusing "differs from a clean install" message on what is actually a pristine, correctly-customized install. This is exactly the "don't lie about state" defect class F3 exists to close, reintroduced by F3's own fix. It is invisible to the plan's verification because the `--dry-run` early return in `cli.py` (`:449`, `return 0`) exits *before* `write_install_lockfile` is ever reached (`cli.py:671`, well after); and no existing test exercises this combination — I grepped `write_install_lockfile` call sites (only `cli.py:671`) and confirmed none of `test_upgrade_side_door_parity.py`, `test_install_module.py`, or `test_security_leaf.py` calls it with a selected preset *and* an axes override that strips a seed.
  *Grounding:* `bootstrap/_scaffold/install.py:1054-1055` (patched site) vs. `:1499-1513` (unpatched site, `onboarding_overlay` computed from raw `preset_src.read_text(...)`, no strip call) vs. `:1524-1533` (the *adjacent* general-file loop that *does* strip, same function); `:1547-1548`, `:1572-1577` (fail-closed divergence guard); `bootstrap/_scaffold/cli.py:449` (dry-run early return) vs. `:669-676` (`lock_profile["axes"] = embedded_axes`; `write_install_lockfile(..., onboarding_preset=preset_name)` call, live-path only); grep of `write_install_lockfile(` — one call site; grep of `_extract_seed_tasks` — exactly two call sites total, confirmed project-wide.
  *Fix:* Add a Chunk B item patching `write_install_lockfile`'s onboarding-overlay precompute to apply the identical `strip_conditional_regions(preset_text, profile.get("axes") or {})` before its own `_extract_seed_tasks` call — ideally by factoring "strip → extract → render" into one small shared helper both `install_onboarding` and `write_install_lockfile` call, so the two computations cannot silently drift apart again in the future. Add a **live** (non-dry-run) install test asserting `dev/.cairn/cairn-lock.yml` is written cleanly (not `None`, no diverged files) for `collaborative-team` + `agent_team: single` and `+ agent_team: concurrent-single-type` — the `--dry-run` smoke check in Acceptance criteria cannot substitute for this.

* **[PR2] (substantive)** B5's drift-guard row does not clearly separate the two override scenarios' distinct assertion sets, risking an implementer over-asserting absence for the `concurrent-single-type` case. The row lists "no `tools/intent.py`, no `doctrine/coordination.md` seed, no `dev/modules/dual-review.md` seed, no `agent-team-onboarding.md` seed" as one flat list following *both* scenario descriptions, with only the earlier parenthetical "(unstaffs only dual-review)" signaling that `concurrent-single-type` must *keep* `tools/intent.py` and the `doctrine/coordination.md` seed (coordination-tiers stays staffed) — verified: `concurrent-single-type` ∈ `_TEAM_STAFFING_GATES["coordination-tiers"]` but ∉ `_TEAM_STAFFING_GATES["dual-review"]` (`config.py:875-879`). As written, a literal reading of the bullet list risks a test that asserts absence of all four surfaces for both cases, which would be *wrong* for `concurrent-single-type` and would either fail against a correct implementation or (worse) get "fixed" by over-stripping coordination-tiers content it shouldn't touch.
  *Grounding:* plan `dev/plans/first-session-survivability.md` B5 row; `bootstrap/_scaffold/config.py:874-879` (`_TEAM_STAFFING_GATES`).
  *Fix:* Split B5 into two explicit assertion blocks: `agent_team: single` → assert absence of all four surfaces; `agent_team: concurrent-single-type` → assert absence of only `dev/modules/dual-review.md` + `agent-team-onboarding.md`, **and** explicit presence of `tools/intent.py` + the `doctrine/coordination.md` seed reference, so the test also proves coordination-tiers content survives the narrower gate.

* **[PR3] (minor)** The plan's judgment call to leave `sign-collab-agreement-day-one` ungated is defensible on the invariant it's actually tested against — `dev/collaboration_agreement.md`'s `team-roster` slot is always-on core (`templates/core/dev/collaboration_agreement.md:14-19`, unconditional across every axis/module), so leaving it ungated never produces a dangling file/tool reference. But the seed's own prose ("...the roster is what makes Dual-Review's External tier structurally meaningful; teams without an explicit roster fall back to fresh-session same-vendor review, which the collaborative-team profile is sized past" — `collaborative-team.md:76-82`) stays literally accurate only when `dual-review` is actually staffed; under the plan's own reproduction override it isn't, yet the seed still asserts the team is "sized past" same-vendor review. This sits just below the line the plan's drift-guard tests for (a conceptual mismatch, not a dangling surface reference), so no planned test would catch it, but it's the same underlying defect class F3 exists to close.
  *Grounding:* `templates/onboarding/collaborative-team.md:76-82` (live); `templates/core/dev/collaboration_agreement.md:15-19` (live, always-on).
  *Fix:* Optional — either have the plan's Author-accounting note explicitly flag this as a documented residual rather than implying full resolution, or soften the seed prose to be axis-neutral (e.g., "the roster is what any review discipline needs explicit, whether or not dual-review is staffed").

* **[PR4] (very minor, optional)** `bootstrap/tests/test_lifecycle_cli.py`'s own module docstring ("session-start: read-only gather of commits / tree-state / in-flight threads...") carries the identical "read-only" overclaim F4 is fixing in the shipped tool, in the very file Chunk C4 extends. Not part of F4's stated scope (it targets only `templates/skills/_lib/lifecycle.py`), and low-stakes since it's test-internal prose, not adopter-facing — but worth a one-line touch-up while the file is open for the C4 edit, in the spirit of the "don't lie about state" theme.
  *Grounding:* `bootstrap/tests/test_lifecycle_cli.py:6-8` (live).
  *Fix:* Optional; a one-clause reword alongside C4, not blocking.

**Coverage.** Independently re-verified this session against the live tree (2026-07-22, 11 days after the proposal's `as_of` snapshot): `cli.py:485-504` (phantom-command line + fan-out filter, both unchanged from the proposal's citations); `install.py:924-931` (`install_onboarding` signature, no `axes` today); `install.py:1040-1100` (Chunk B1's target — write C slot substitution vs. write D verbatim copy, confirming the plan's "not write D" scoping is correct); `install.py:1439-1600` (`write_install_lockfile` in full, surfacing PR1); `cli.py:464-476,620-686` (`embedded_axes` construction, `install_core`/`install_onboarding`/`write_install_lockfile` call sites, the dry-run early return at `:449`); `config.py:847-879` (`_AXES`, `_TEAM_STAFFING_GATES`, confirming both gate value-sets and the axis-semantics comment backing the tour-seed gate reasoning); `templates/onboarding/collaborative-team.md` and `high-rigor-legacy.md` in full (both live files, confirming B3/B4's per-seed gate assignments exactly); `templates/skills/_lib/lifecycle.py` (module docstring at `:5-41`, `cmd_session_start` docstring at `:632-643`, parser `description=`/`help=` at `:1205-1220`, all matching the plan's before/after claims verbatim) and byte-diff against `tools/lifecycle.py` (identical); `doctrine/session-routines.md:66-67` (verbatim match); `bootstrap/tests/test_upgrade_side_door_parity.py:330-436`, `test_install_module.py:1-80`, `test_security_leaf.py:1-45` (call-site/reference audit for R8's backward-compatibility claim); `bootstrap/tests/_ast_attest.py:127-146` (`_UPDATE_ALLOWLIST`) and a live `/Users/kendal30/conda_envs/lhm/bin/python3 -m pytest bootstrap/tests/test_ast_attest.py -q` run (26 passed, clean baseline, confirming the sibling plan's close-out); a full `bootstrap/tests` run under the canonical interpreter (1 failed — the tracked `test_evolution_infer.py` clock case — 1423 passed, ~111s); `python3 scripts/claim_check.py dev/plans/first-session-survivability.md` (clean). **Not verified** (no implementation exists yet to run against): the exact printed wording/formatting Chunk A2's calm advisory line will take beyond the proposal's pinned sentence; whether `test_onboarding_seed_roster.py`'s eventual code correctly implements the B5 distinction as written (PR2 is about the plan's specification, not a run of nonexistent code); PR1's regression was derived from static code-reading of the two independent call sites plus the fail-closed divergence logic, not from executing Chunk B (which doesn't exist yet) — I'm confident in the reasoning but flag that a live repro after Chunk B lands would be the final confirmation.

### Sharpening -- Claude (author) -- 2026-07-22

All four findings accepted; none dropped.

* **[PR1] accept — independently re-verified before accepting.** I read
  `install.py:1499-1533` myself and confirmed the finding exactly:
  `write_install_lockfile`'s `onboarding_overlay` precompute calls the raw
  `_extract_seed_tasks`/`_render_onboarding_slot` pair with no
  `strip_conditional_regions`, while the adjacent per-file loop two lines
  below it does strip. This is a real, confirmed regression this plan
  would have shipped. Fixed above: Chunk B1 now factors a shared
  `_rendered_onboarding_overlay` helper both call sites use (so they
  cannot drift apart again), a new B1b row patches the second call site,
  and a new B2b row adds the live-install regression test the reviewer
  correctly identified as missing (the `--dry-run` smoke check cannot
  substitute for it). The re-anchor section is updated: this doubles the
  non-allowlisted CHANGED-symbol count from one (`main`) to two (`main` +
  `write_install_lockfile`), alongside the one allowlisted symbol
  (`install_onboarding`) — three total, still one reviewed
  Maintainer-run pass, same pattern as the licensing plan's Chunk D.
* **[PR2] accept.** B5 now specifies two distinct assertion sets (plus the
  unconditional no-override case as a third), explicitly requiring
  *presence* of `tools/intent.py` + the coordination-doctrine seed under
  `concurrent-single-type` — not just absence elsewhere — so the test
  cannot pass by over-stripping.
* **[PR3] accept.** Added an explicit "confirmed, with a residual noted"
  paragraph to the Author-accounting section recording the
  `sign-collab-agreement-day-one` prose's conceptual-accuracy gap under
  `agent_team: single` as a known, accepted, not-silently-dropped residual
  — no test can catch it and this plan does not attempt a prose fix.
* **[PR4] accept.** C4's row now includes the optional
  `test_lifecycle_cli.py` module-docstring touch-up alongside the planned
  edit, same file, same commit.

**Status: awaiting-plan-review → executing.** All findings disposed;
implementation begins next (Chunk A, then Chunk B with the PR1 fix
folded in from the start, then Chunk C).

## Code review

*Filled in after implementation commits land (Chunks A-C; Chunk D is
Maintainer-gated and reviewed separately once it runs).*

## Lasting-truth migration

*Filled in at archive time — gated on Chunk D (the Maintainer's supervised
AST correction), not solely on code review. See "The re-anchor gate" above.*

Per the [Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home outside
the plan.

This section is append-only once written.
