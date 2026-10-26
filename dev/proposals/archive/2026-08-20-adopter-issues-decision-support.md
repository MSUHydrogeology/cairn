<!-- This document is DECISION SUPPORT for the Human Maintainer. It is NOT a review, creates no lifecycle obligations, carries no formal findings, and is disposable once the Decisions on the three proposals land. -->

# Decision Support: Adopter Issues #4–#7 Proposals

**Date**: 2026-08-20  
**Evaluator**: Antigravity (Gemini 3.7 Flash)  
**Target Proposals**:
1. [`dev/proposals/2026-08-20-claude-adopt-into-existing-tree.md`](2026-08-20-claude-adopt-into-existing-tree.md) (Operative: **Revision 2**) — Issues #5 (gaps 1–2), #7
2. [`dev/proposals/2026-08-20-claude-portable-sweeps-cannot-run.md`](2026-08-20-claude-portable-sweeps-cannot-run.md) (Operative: **Revision 4**) — Issue #4
3. [`dev/proposals/2026-08-20-claude-scanner-claim-scope.md`](2026-08-20-claude-scanner-claim-scope.md) (Operative: **Revision 4**) — Issues #5 (gap 3), #6

---

## 1. What Is Actually Being Decided

### Proposal 1: `adopt-into-existing-tree` (Revision 2)
* **Problem**: Adopter installing into an existing repo with a committed `profile.yml` faced silent token drops (causing placeholder persistence in `cairn-lock.yml`), silent overwriting/skipping of existing files, and an obsolete `--include-archives` recommendation in `UPGRADE.md`.
* **Changes in Code & Docs**:
  * **D1 (`bootstrap/_scaffold/upgrade.py`)**: `_cmd_adopt_module` seeds missing tokens from `profile.yml` into `cairn-lock.yml` (existing lockfile tokens always win). Applies strict placeholder detection (`{{...}}` AND `<...>`). Executes `_refuse_secret_tokens` **before** the spec loop writes any files. Emits a loud warning on an incomplete/invalid profile rather than silent fallback.
  * **D2 (`bootstrap/_scaffold/upgrade.py`)**: When an adopted module destination already exists, compares on-disk bytes against what *would* install (after token substitution). Covers both the `else` (differing) and `continue` (already tracked in lockfile) branches. Emits a non-blocking advisory note if bytes differ; does not overwrite or abort.
  * **D3 (`bootstrap/UPGRADE.md`)**: Replaces `python tools/lifecycle_planner.py scan --include-archives` with `python tools/lifecycle_planner.py scan`.
* **Contractual Invariants**: Tokens are validated and secrets refused *before* any disk writes occur; lockfile schema remains unchanged; advisory note never blocks adoption.

### Proposal 2: `portable-sweeps-cannot-run` (Revision 4)
* **Problem**: `portable-security-sweeps` failed to run any scan legs under Gitleaks 8.30.1 due to probe/parser mismatches, over-strict git config screening, syntax incompatibilities in timeout flags, and an overloaded exit code.
* **Changes in Code & Docs**:
  * **D1 (`scripts/run_portable_security_sweeps.py` and template twin)**: Inserts an explicit extractor between `probe_version` and `parse_version` that recognizes both `gitleaks version X.Y.Z` and bare `X.Y.Z`. Flips `fake_tool` default in tests to emit realistic output.
  * **D2 (`scripts/run_portable_security_sweeps.py` and template twin)**: Adds `remote.<name>.glab-resolved` and `branch.<name>.vscode-merge-base` to inert git config allowlist; accumulates all non-inert keys into a single refusal message (capped at 20).
  * **D3 (`templates/modules/team-gated/portable-security-sweeps.md`)**: Documents that the admission ceremony from evidence to admitted entry is unautomated and must be performed manually by the Maintainer in 4 steps.
  * **D4 (`scripts/run_portable_security_sweeps.py` and template twin)**: Formats `--timeout` as integer seconds across all three subcommands, matching Gitleaks flag tables.
  * **D5 Part A (`scripts/run_portable_security_sweeps.py` and template twin)**: Disambiguates Gitleaks exit `1` by passing `--exit-code 42` for findings (exit `0` = clean, `42` = findings, `1` = usage error/invalid argv).
  * **D5 Part B (`scripts/run_portable_security_sweeps.py` and template twin)**: Completely removes adapter `stdout` and `stderr` from `LegOutcome.reason` across all exit codes and signals; replaces them with runner-owned messages naming numeric exits only, preventing secret leakage into summary JSON or reports.
* **Contractual Invariants**: No adapter-controlled bytes reach `LegOutcome.reason` or durable report sinks; finding exit is distinguishable from usage error.

### Proposal 3: `scanner-claim-scope` (Revision 4)
* **Problem**: `content_scan_runner.py` instructed operators to prune a shared security baseline based only on its own audited roots (exit 3), while `pip-audit` reported ambient environment vulnerabilities (299 distributions) without indicating whether they were reachable from the project's declared runtime dependencies (93 distributions).
* **Changes in Code & Docs**:
  * **D1 (`scripts/content_scan_runner.py` and template twin)**: Scopes the stale-baseline message on exit 3 to name the specific audited roots set; clarifies that unreferenced entries may be live in other consumers; frames exit 3 as a disagreement signal rather than an authoritative verdict to prune.
  * **D1b (`templates/modules/team-gated/content-security.md`)**: Syncs copy across docs and self-hosted twins.
  * **D2 (`templates/modules/team-gated/run_security_audit.py` and docs)**: Annotates `pip-audit` findings with reachability (`in-closure`, `out-of-closure`, `unknown`) based on standard-library `importlib.metadata` dependency walk. D2b adds a coverage-ceiling disclosure to `python-security.md`.
  * **Marker Tokenizer (`templates/modules/team-gated/run_security_audit.py`)**: Uses a quote- and whitespace-aware tokenizer in stdlib to handle `extra == "..."` in any operand order, ignores `extra` in quoted strings, and fails closed to `unknown` on other expressions (`extra !=`, `extra in`).
  * **Test Oracle (`bootstrap/tests/test_security_stack.py`)**: Asserts exact multiset equality over `(normalized_distribution, count, annotation)` triples in test fixtures.
* **Contractual Invariants**: The annotation changes no exit code, filters no findings, and drops no distributions; if closure cannot be determined, all findings annotate `unknown`.

---

## 2. Cross-Proposal Consistency

### Issue #5 Landing-Order Tiebreak
Issue #5 is partitioned across Proposal 1 (gaps 1 & 2: profile seeding and byte comparison) and Proposal 3 (gap 3: scoped stale-baseline message).
* **Proposal 1 (lines 1486–1495)**: *"Issue #5 closes only when this proposal and `2026-08-20-claude-scanner-claim-scope` have both landed — gaps 1–2 are here, gap 3 is there. Whichever lands second carries the close; the first posts a progress comment."*
* **Proposal 3 (lines 340–353)**: *"Gap 3 is D1 here; gaps 1 and 2 are in `2026-08-20-claude-adopt-into-existing-tree`. Issue #5 closes only when both proposals have landed... Whichever of the two lands second carries the close; whichever lands first posts a progress comment and leaves the issue open."*
* **Consistency Check**: **PERFECT MATCH.** Both proposals use identical logic, identical gap attributions, and an unambiguous tiebreak rule.

### Close Gates & Lifecycle Governance
* **Maintainer Gating**: All three proposals specify that the final plan chunk closing the respective GitHub issues is `MAINTAINER-GATED`.
* **Security Review Requirement**:
  * Proposals 1 and 2 declare **Security Review: REQUIRED** (Proposal 1 touches the scaffold/YAML loading/lockfile write surface; Proposal 2 touches the portable sweeps executable trust root).
  * Proposal 3 declares **Plan review: required(Internal)** and **No Security Review trigger** (it derives an advisory annotation without changing trust boundaries or filtering outputs).
* **Consistency Check**: **CONSISTENT.** The security review triggers align with the surface definitions in `AGENTS.md`.

---

## 3. What Accepting Obligates the Maintainer To Do

If the Maintainer accepts these proposals, the derived plans will require specific, non-delegable actions:

1. **Host-Specific Real-Adapter Verification (Proposal 2 / Issue #4)**:
   * Acceptance criterion 3 requires a real reduced-mode Gitleaks run against a fresh repository carrying at least one commit.
   * **Action required**: The Maintainer (or an adopter with Gitleaks 8.x installed) must execute the smoke command and provide the attestation. (Verified: Gitleaks 8.30.1 is present on this host).
2. **External Security Code Reviews (Proposals 1 & 2)**:
   * The implementation chunks for Proposals 1 and 2 must undergo an independent External Security code review before the issues can close.
3. **Public GitHub Issue Communication (All Proposals)**:
   * The Maintainer must authorize and post the public closing comments for Issues #4, #5, #6, and #7.
   * The comments must explicitly state what was **declined** (e.g., declining `--set-token` as primary in #5, declining option 2 / filtering in #6, declining automated admission in #4).
   * For Issue #6, the Maintainer must record the adopter's 299/93/212/144/27 conda measurement under `dev/measurement/`.

---

## 4. Where the Residual Risk Sits

| Proposal | Residual Risk | Manifestation | Reversibility |
|---|---|---|---|
| **1. `adopt-into-existing-tree`** | An adopter ignores the D2 advisory on differing bytes and proceeds with unverified files. | Target repository runs modified/stale scaffold files without realizing it. | **High**: D2 is non-destructive; files can be manually inspected or re-adopted. |
| **2. `portable-sweeps-cannot-run`** | Hostile candidate repository exploits an uncontained vulnerability in the Gitleaks binary itself (S5 residual). | Execution escape during developer scan. | **Medium**: Gitleaks execution is inherently uncontained; mitigated by `child_env` and config screening. |
| **3. `scanner-claim-scope`** | Complex PEP 508 environment markers or non-standard distribution packaging cause the tokenizer to misclassify a dependency as `out-of-closure`. | A vulnerable package is triaged last instead of first. | **High**: All findings are still printed; no findings or exit codes are suppressed. |

### The Security Review Asymmetry
* Proposals 1 and 2 require Security Review; Proposal 3 does not.
* **Legibility**: This asymmetry is fully justified and clear. Proposals 1 and 2 modify file-writing logic, secret-token refusal positioning, and executable trust-root parsing. Proposal 3 strictly modifies report formatting and advisory annotations without altering scanner exit codes or finding sets.

---

## 5. Convergence, Honestly Read

Across all three proposals, **~45 total findings** were raised and resolved over multiple review rounds:
* **Proposal 1 (2 rounds, 12 findings)**: Converged cleanly. Round 1 resolved 8 findings (including secret-refusal ordering and placeholder syntax); Round 2 resolved 4 findings (clarifying fallback loudness and S1 independence). The contract at Revision 2 is tight and stable.
* **Proposal 2 (4 rounds, 16 findings, 2 scope expansions)**: Required significant iteration. Round 4 caught a critical security issue (**Finding E1**): D5 Part A had inadvertently routed usage errors into a pre-existing unredacted stderr relay. Revision 4 resolved this by completely stripping adapter stderr from outcome reasons (Part B). The defect rate has converged to zero.
* **Proposal 3 (4 rounds, 17 findings)**: Required deep refinement of the parser and oracle. Round 4 caught **Finding Q1** (naive substring `extra ==` dropping valid packages) and **Finding Q2** (oracle projecting away the annotation). Revision 4 resolved both with a stdlib tokenizer and a triples multiset oracle.

**Verdict on Convergence**: All three proposals have **fully converged**. The high finding count in earlier rounds reflected rigorous adversarial testing (canary mutations, tokenizer stress-testing), and the operative revisions cleanly resolve the underlying defects.

---

## 6. The Strongest Case Against Accepting Each (Steelman)

### Against Proposal 1 (`adopt-into-existing-tree`)
* **The Argument**: Cairn’s design center is that `cairn-lock.yml` is the sole authority for installed modules. Introducing a fallback to `profile.yml` creates a dual-input hierarchy with complex fallback dispositions (silent, warn, warn). If an adopter needs custom tokens, they should explicitly provide them via `cairn init-lock` or `--set-token`, rather than having the adopt command inspect secondary files.

### Against Proposal 2 (`portable-sweeps-cannot-run`)
* **The Argument**: Gitleaks is an external third-party Go binary whose CLI flags and output formats change across versions. Adding custom output extractors, timeout flag formatters, and `--exit-code 42` workarounds into Cairn creates an ongoing maintenance burden. Cairn should remain un-opinionated and require adopters to provide a standard wrapper script if their local Gitleaks version differs from the upstream assumption.

### Against Proposal 3 (`scanner-claim-scope`)
* **The Argument**: Writing a custom standard-library PEP 508 marker tokenizer without `packaging` is notoriously brittle. Furthermore, reachability annotation adds heuristic complexity to what should be a simple, dumb security tripwire. If 71% of findings in a conda environment are out-of-closure, adopters should manage dependency scope using dedicated tools (`pip-compile`, `uv.lock`) rather than relying on Cairn’s scanner to annotate reachability.

---

## 7. Comprehension Verdict

* **Proposal 1**: **DECIDABLE.** The contract is compact, well-structured, and easy to follow. The order of operations in D1 and the fallback disposition table are unambiguous.
* **Proposal 2**: **DECIDABLE (with technical density).** D5 Part B and the exit-code mechanics are technically dense due to Gitleaks internals, but the operative contract in Revision 4 is self-contained and clear on what code will be written.
* **Proposal 3**: **DECIDABLE.** The marker tokenizer rules and the `(normalized_distribution, count, annotation)` triples oracle are precisely defined and mathematically testable.

**Overall Conclusion**: All three proposals are in a decidable state. The Maintainer has complete, self-contained, and cross-consistent contracts on which to render a Decision.
