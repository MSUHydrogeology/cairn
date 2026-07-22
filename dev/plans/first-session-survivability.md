<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/lifecycle.md doctrine/session-routines.md doctrine/onboarding.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: bootstrap/tests/test_first_session_report.py, bootstrap/tests/test_onboarding_seed_roster.py -->
<!-- The two paths above are forward-reference files this plan creates; they materialize as the chunks land. -->

# Plan: first-session survivability (F1, F3, F4)

**Source proposal**: `dev/proposals/archive/2026-07-11-claude-first-session-survivability.md`
**Status**: awaiting-plan-review
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
update-symbol`, allowlisted for exactly one of this plan's two touched
symbols (`_MODULE_MAPPINGS`/`_SKILLS_MAPPINGS`/`_CORE_MAPPINGS`/
`install_onboarding` — see Chunk B). **Good news carried from the sibling
plan's Chunk D close-out:** the previously-blocking pre-existing drift
(`FunctionDef:print_report`) is **already resolved** (commit `e1eec63`), so
`bootstrap/tests/test_ast_attest.py` is clean under the canonical `lhm`
interpreter *before* this plan's own edits land — this plan's Chunk A/B
symbols will be the *only* drift `update-symbol`/a Maintainer-run
correction needs to handle, with no unrelated noise in the way this time.

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
| B1 | `bootstrap/_scaffold/install.py` | Add `axes: dict | None = None` as a **keyword-only** parameter to `install_onboarding` (backward-compatible with the three existing positional 3-arg call sites in `test_upgrade_side_door_parity.py`, verified this session). Apply `strip_conditional_regions(preset_text, axes or {})` immediately before `_extract_seed_tasks(preset_text)` — stripping only the text that feeds the `PLANNING.md` slot substitution (write C), **not** the verbatim preset-source copy (write D), which stays the full authoritative reference the goodnight helper reads for deferred tasks. |
| B2 | `bootstrap/_scaffold/cli.py` | Pass `axes=embedded_axes` at the `install_onboarding` call site (the same `embedded_axes` dict `install_core` already strips with, per R8 — **not** `resolved_axes`, so every strip site keys off one axes map and the `install.py` would-strip invariant at the lockfile-divergence check holds). |
| B3 | `templates/onboarding/collaborative-team.md` | Wrap `install-work-intent-hooks` (seed) and `read-coordination-doctrine` (seed) in `<!-- cairn:if agent_team in concurrent-multi-type,concurrent-single-type -->` / `<!-- cairn:endif -->` (mirrors `_TEAM_STAFFING_GATES["coordination-tiers"]` exactly). Wrap `read-dual-review-module` (seed) in `<!-- cairn:if agent_team in concurrent-multi-type -->` (mirrors `_TEAM_STAFFING_GATES["dual-review"]`). Wrap `agent-team-onboarding` (seed, R6 tour-seed extension) in `<!-- cairn:if agent_team in concurrent-multi-type -->` — it onboards a **second agent type**, which only `concurrent-multi-type` staffs; same gate as dual-review, not coordination-tiers. `sign-collab-agreement-day-one` is **left ungated** (see Author-accounting — it's about the human/agent roster generally, not agent-concurrency shape). |
| B4 | `templates/onboarding/high-rigor-legacy.md` | Wrap **only** `install-work-intent-hooks` in the same coordination-tiers gate (`concurrent-multi-type,concurrent-single-type`) — this preset carries no `read-coordination-doctrine`/`read-dual-review-module` seeds at all (R2's correction; verified this session, unchanged). Wrap `agent-team-onboarding-legacy` in the `concurrent-multi-type`-only gate (same reasoning as B3's `agent-team-onboarding`). `confirm-maintainer-authority` is left ungated (same reasoning as `sign-collab-agreement-day-one`). |
| B5 | `bootstrap/tests/test_onboarding_seed_roster.py` (new) | The broadened drift guard (R6): for `collaborative-team` × an `agent_team: single` override (unstaffs both `coordination-tiers` and `dual-review`) and `collaborative-team` × `agent_team: concurrent-single-type` (unstaffs only `dual-review`), assert the rendered `PLANNING.md` seed slot references **no module-specific surface — tool *or* doc — the resolved roster did not install** (not just `tools/intent.py`): no `tools/intent.py`, no `doctrine/coordination.md` seed, no `dev/modules/dual-review.md` seed, no `agent-team-onboarding.md` seed, exactly as staffed. Also assert the **unconditional** case (no override) still renders all seeds — proving the gate is a real filter, not a silent no-op. |

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

### Chunk C — F4 (correct `session-start`'s self-description)

| # | File | Change |
|---|------|--------|
| C1 | `templates/skills/_lib/lifecycle.py` | Module docstring: reword "Every side-effecting subcommand honors `--dry-run`: it prints the planned writes and exits writing nothing." to scope the claim to `session-end` only, and state `session-start`'s one exception plainly: it performs one idempotent write (the skills fan-out self-heal) regardless of any flag, matching `doctrine/session-routines.md:66-67`'s existing framing ("The only write the routine itself makes is the tool's idempotent skills self-heal, not the agent's"). |
| C2 | `templates/skills/_lib/lifecycle.py` | Parser `description=`: reword "Read-only orientation and reflection-only goodnight; no network." to "Orientation gather (plus one idempotent skills-fan-out self-heal write) and reflection-only goodnight; no network." |
| C3 | `templates/skills/_lib/lifecycle.py` | `session-start` subparser `help=`: reword "Read-only orientation gather (commits, tree state, threads, intents)." to name the one write, matching C2's phrasing. **Note:** `cmd_session_start`'s own function docstring is *already* accurate (confirmed this session — it already reads "Orientation gather (read-only) + idempotent skills fan-out self-heal") and needs no edit; only the module docstring and the two parser-level strings overclaim. |
| C4 | `bootstrap/tests/test_lifecycle_cli.py` (extend) | Text-assertion test: the built parser's top-level `description` and the `session-start` subparser's `help` text each mention the skills-fan-out self-heal write and neither claims "read-only" unqualified; the module docstring's `--dry-run` claim is scoped to `session-end`. |

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
  condition turns the suite red). The AST-baseline drift F1/F3 introduce is
  the **expected, sole** post-Chunk-D-close-out drift (no unrelated noise
  this time, per the Scope section).
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

## Plan review

*Filled in below once the fresh-context Internal pass lands.*

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
