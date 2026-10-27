# Nimbleness recovery — keeping Cairn light enough to use

**Author**: Claude (Strategy), Antigravity (Strategy)
**Model**: Claude Fable 5, Gemini 3.1 Pro
**Date**: 2026-08-21; updated around `0.5-dev` 2026-10-27
**Status**: living
**Type**: product-strategy
**Surfaces this feeds**: [`AGENTS.md`](../../AGENTS.md); [`dev/agent_collaboration.md`](../agent_collaboration.md); [`dev/proposals/_template.md`](../proposals/_template.md); [`dev/plans/_template.md`](../plans/_template.md); [`dev/PLANNING.md`](../PLANNING.md)

## Summary

Cairn began as *"Yes, we can do that — let's take a moment to make it good."* Without a counterforce, AI agents turn any process into *"We can't do that without 1,000 lines of deliberation and process adherence."*

The August 2026 subtraction sweep ([`dev/plans/archive/subtraction-sweep.md`](../plans/archive/subtraction-sweep.md)) and the `0.4.0` / `0.5-dev` releases removed ~55,000 lines of deliberation tooling, retired delayed onboarding triggers, capped reviews at one round by default, introduced **Cairn Plain Language 1.0**, added `/session-start --drain` and `tools/board.py --maintainer`, and allowed 1-commit bounded changes to skip plans and code review.

However, **process mass regrows automatically unless the ratchets that produce it are countered.** On `0.5-dev` today (`2026-10-27`), plans have shrunk to **277–364 lines** (down from a 1,906-line median in August), but proposals still average **600–1,000 lines** with reviews appended, and Cairn's four core governing files (`AGENTS.md`, `dev/agent_collaboration.md`, and the two `_template.md` files) have grown back to **1,842 lines** total. This note states the permanent anti-bloat principles and the **five remaining structural items** needed to finish the recovery.

---

## The irreducible core (what Cairn must never drop)

What actually solves sloppy "vibe-coded" output is four things:

1. **Write intent before code.** A short committed record stating what changes and why.
2. **Independent review before it lands**, centered on **at least one falsification attempt** — run the code or check, try to break it, and record what happened.
3. **Record the Maintainer's Decision.** One committed block quoting who decided and what was authorized.
4. **Empirical verification.** Scoped tests for code, a real invocation for tools, and `claim_check.py` / `link_check.py` for prose.

Everything beyond those four is elaboration, and every elaboration must pay rent in saved Maintainer attention or prevented defects.

---

## Five ratchets that make process grow back

Cutting lines once does not stop regrowth if these five mechanisms stay active:

1. **Every incident becomes a rule, and no rule ever leaves.** Adding a rule to `AGENTS.md` or a template feels prudent after a bug; if nothing flushes rules whose hazard is now prevented by code, governing prose accretes without bound.
2. **Pinned prose-regex tests freeze verbosity in place.** On `0.4.0` and `0.5-dev`, several plans added new instruction paragraphs to `AGENTS.md` and the `_template.md` files and pinned their wording with regex tests under `bootstrap/tests/`. Because `bootstrap/tests/**/*.py` is gate-frozen, shortening a paragraph breaks a frozen test and requires a Maintainer gate-manifest re-anchor.
3. **Agents have an asymmetric loss function.** No agent is penalized for writing an 800-line proposal, while any perceived omission draws a review finding. Without explicit size expectations, agents write defensive armor.
4. **Multi-file deliberation for routine multi-step work.** Even after `no-plan-changes-end-to-end` freed 1-commit changes, any change that takes two commits or touches a broad test scope still writes *both* a proposal (`dev/proposals/`) and a separate plan (`dev/plans/`), doubling review cycles and file volume.
5. **Self-hosting maximum ceremony.** Cairn runs every high-assurance gate on itself (including freezing all 195 test files in `bootstrap/tests/`), so routine maintenance on Cairn pays a much higher ceremony tax than an adopter project does.

---

## Standing principles (now in force)

These principles from the original recovery note are settled doctrine and govern all future work:

* **Process weight scales with irreversibility, not habit.** Trivial defect fixes with a failing test and 1-commit bounded changes skip plans and code reviews (`AGENTS.md`). Full proposals, plans, and Security Reviews are reserved for new capabilities, contract changes, and high-risk surfaces.
* **One review round by default; the author resolves.** A review moves an artifact to `revising`; the author's response and revision carry it directly to `awaiting-decision` (proposals) or `ready-to-implement` (plans). Plan review never has a second round, and code/proposal review gets a second round only for widened scope, new defects, or an open Security Review.
* **Route questions by expertise.** Science and domain assumptions always go to the Maintainer in plain domain terms. Structural choices arrive with a clear `(Recommended)` default. Implementation details belong to the author and are not escalated.
* **Advisory tools warn; only safety and trust boundaries block.** Coordination and hygiene tools (`board.py`, `intent.py`, `audit_report.py`, `claim_check.py` on archives) inform rather than block. Fail-closed refusal is reserved for scaffold path/symlink containment (`_assert_safe_write`, `_contained_lockfile_path`) and release trust gates (`security_check.py`, `repin.py`).
* **Comprehension is the currency of Maintainer attention.** Under **Cairn Plain Language 1.0** ([`docs/plain-language.md`](../../docs/plain-language.md)), every artifact leads with the conclusion in plain language so the Maintainer can decide from the opening section without translating systems jargon.
* **Running code and failing tests beat essays.** In review, a reproduced failing test or probe outranks speculative argument, and a reviewer's suggested patch is an offer the author may decline if a simpler fix works.

---

## Five uncompleted items to finish the recovery

### 1. Compress the four governing files and unfreeze prose-wording tests
* **Current state (measured `2026-10-27` on `0.5-dev`):**
  * [`AGENTS.md`](../../AGENTS.md): **579 lines**
  * [`dev/agent_collaboration.md`](../agent_collaboration.md): **356 lines**
  * [`dev/proposals/_template.md`](../proposals/_template.md): **452 lines**
  * [`dev/plans/_template.md`](../plans/_template.md): **455 lines**
  * **Total:** **1,842 lines** (plus identical copies in `templates/core/`).
* **Why it matters:** Agents mirror the length of the templates and instructions they read. A 452-line proposal template with extensive inline commentary produces 600–1,000-line proposals even with a "Keep the proposal short" banner at the top.
* **What to do:**
  1. Strip the tutorial commentary out of `dev/proposals/_template.md` and `dev/plans/_template.md` into `doctrine/proposals.md` and `doctrine/plans.md`, leaving the templates themselves as **~80–120 line** skeletons.
  2. Run a **rule-flush pass** across `AGENTS.md` and `dev/agent_collaboration.md` to merge overlapping sections added during `0.4` and `0.5`.
  3. Relax the regex tests (`test_scope_reduction_trap.py`, `test_review_and_verification_rules_ship.py`, `test_writing_rules_ship.py`, `test_model_tier_rule_ships.py`) so they check for the presence of the core rule concept rather than pinning multi-paragraph prose nearly word-for-word.

### 2. Merge proposal + plan into a single compact artifact for standard multi-step work
* **Current state:** `no-plan-changes-end-to-end` (`0.5-dev`) lets 1-commit bounded changes skip the plan entirely. However, a standard 2–3 chunk feature or bug fix still requires opening a proposal in `dev/proposals/`, running a proposal review + response + Decision, and then opening a second file in `dev/plans/` with its own plan review + response before writing code.
* **What to do:** Allow standard-lane multi-chunk work to carry its compact chunk/test plan directly inside the proposal (one file, one pre-code review, one Maintainer Decision -> `ready-to-implement`), reserving a separate `dev/plans/` artifact for large architectural or multi-session builds.

### 3. Narrow `bootstrap/tests/` gate-manifest freezing to security and trust-root tests
* **Current state:** `_frozen_files` in `bootstrap/tests/_gate_manifest.py` freezes **all 195 `.py` files** matching `bootstrap/tests/**/*.py`. As a result, updating a golden CLI line in `test_board_json_contract.py` or a prose test in `test_quickstart_sequence.py` triggers a `FROZEN-MODIFIED` gate failure and accumulates re-anchor debt on [`dev/PLANNING.md`](../PLANNING.md).
* **What to do:** Even with `scripts/repin.py` making re-pins much faster in `0.5`, freezing non-security unit tests conflates ordinary test maintenance with trust-root changes. Name the actual security and trust-apparatus test files explicitly in `_frozen_files` (as also recommended in [`2026-08-05-codex-security-strategy.md`](2026-08-05-codex-security-strategy.md) `[TRU-4]`) so ordinary feature and doc tests can evolve without a trust ceremony.

### 4. Add lightweight Return-on-Attention accounting to proposals
* **Current state:** `board-as-basis` (`0.4.0`) added the one-sentence `**In brief**:` summary header and `**Waiting on Maintainer**:` marker. However, proposals still do not state up front how many follow-up board rows or Maintainer ceremonies they create, nor do archived plans record whether the outcome was worth the attention spent.
* **What to do:** Add two lines to the deliberate-lane lifecycle:
  1. At Decision time: state **Maintainer steps & follow-ups spawned** (e.g., whether the change owes a re-anchor or defers new rows to `dev/PLANNING.md`).
  2. At archive time: record one sentence on whether the delivered outcome repaid the review and ceremony cost.

### 5. Finish the two remaining cleanup items from the August sweep
1. **Move `link-check-allow` and `cairn-internal-ref-allow` out of inline HTML comments:** The August sweep moved `claim-check-allow` exemptions out of Markdown file headers into a config file, but `link-check-allow` and `cairn-internal-ref-allow` remain inline HTML comments at the tops of Markdown files.
2. **Fix `tools/gauge.py` bucketing for Cairn's own product files:** Running `python3 tools/gauge.py --since 2026-08-25` on `2026-10-27` reports `dev/` at ~15,000 lines/week and `other-machinery` at ~13,000–15,000 lines/week (product share `3%–14%`), in part because `gauge.py` buckets `bootstrap/_scaffold/` (Cairn's installer/upgrader product) under `other-machinery` rather than `product`. Updating `gauge.py` to distinguish shipped adopter capabilities (`bootstrap/_scaffold/`, `templates/`) from internal process tooling will make the monthly product-vs-process check accurate.

---

## How to judge whether Cairn is staying nimble

Use these four practical health checks (no new ledger required):
* **Adopter defect turnaround:** Reported bug → committed fix with test in **1–2 sessions**.
* **Artifact readable at a glance (measured in words, not lines):** Proposals and plans open in **≤ 1,000 words (~6 KB)** before appended reviews; `Acceptance criteria` stays **≤ 150 words per chunk**; each appended review pass or response stays **≤ 600 words (~4 KB)**; and strategy notes stay **≤ 1,500 words (~10 KB)**.
* **Maintainer time spent on substance:** The Maintainer decides direction, science, and security boundaries from the opening plain-language summary, rather than refereeing multi-round wording disputes or running manual scratch scripts.
* **Deliberation vs. product balance:** On adopter repositories (`modflow_tools`, `LHM`, `Assai`) and Cairn alike, shipped code, science, and reader-facing documentation outpace `dev/` deliberation volume.
