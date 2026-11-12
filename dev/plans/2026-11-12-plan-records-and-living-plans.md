# Plan: Living plans and concise records

**Source proposal**: dev/proposals/archive/2026-11-12-claude-plan-records-and-living-plans.md
**Author**: gpt-6.1-terra (Medium), plan author
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-12
**In brief**: Keep active plans current while preserving reviewed evidence and making costs visible at closeout.

## Build summary

Make the four operative plan cells editable throughout active work, with review bound to substantive changes. Preserve historical authority and every verification duty while shortening repeated instructions. Give final records a countable benefit judgment and add its advisory summary to Cairn's existing release report.

## Source proposal

Decision `5962633b` accepted the revised heavy v0.7 proposal, including its design-origin routing. Its Proposal A–C, security preflight and retained scope govern this plan; its historical measurements are not implementation evidence.

## Scope

Change Cairn's `AGENTS.md`, `dev/agent_collaboration.md`, plan and proposal templates and their `templates/core/` counterparts; reconcile `docs/methodology/plans.md`, `lifecycle.md` and `lifecycle-contract.md` with the installed rules. Change `tools/board.py` and its shipped `templates/skills/_lib/board.py` twin, Cairn-only `tools/audit_report.py`, and `docs/release-process.md`. Inventory other actual consumers of review headings and verification records before editing, including audit pulse; preserve their evidence semantics. Do not ship the audit reporter or change release authority.

Reuse: `tools/board.py`'s `--next` review/response reader and H2 section parser, its shipped twin, and `tools/audit_report.py`'s archive walk, `--root` and pulse paths already serve these jobs. `rg` for their headings and filenames found the board contract and replacement-tool tests; extend their public entry paths, not a new command, checker, collector or sidecar.

## Sequence

Estimate two focused implementation windows plus independent reviews and final verification. The main uncertainty is preserving advisory reader compatibility across legacy and amended records. Both chunks are agent-executable after the required plan reviews; C2 depends on C1's contract. Commit each lifecycle transition separately.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Reconcile active-plan lifecycle, record grammar and receipt guidance. | Plan reviews | Paired governing templates and methodology |
| C2 | Implement and verify existing readers and release invocation. | C1 | Board twins, advisory audit report, public-contract tests and release guidance |

C1: Scope, Sequence, Acceptance criteria and Verification remain mutable only while active. A change-log line identifies the revision commit (use `this commit` in that commit, resolvable from Git history), cells, change and reason; it cannot rewrite historical Reviews, responses, records, Decisions, quotations, accepted proposal scope or fences. Substantive changes stop affected and dependent work; return to `revising-plan`, commit the replacement, request a fresh non-author ordinary review and applicable Security Review, record author disposition, then use `ready-to-implement` before resuming. Preserve owed code-review returns, final verification, scope-reduction approval and Security Review caps. Wording/status changes that change no obligation need no amendment review; missing design returns to the existing operative cells.

For machine-readable amendment chains, document one change-log entry per revision with full prior reviewed commit and replacement commit (the latter may be `this commit` in its own commit), affected cells/dependencies and required obligations. Each `## Plan amendment review -- <reviewer> -- <date>` records `**Prior reviewed commit**`, `**Replacement commit**`, `**Affected cells and dependencies**`, one `**Obligation**` and `**Verdict**`; one unambiguous applicable ACCEPT per required obligation clears that revision. A later revision links to the preceding reviewed replacement. The committed records are authority; the board is advisory. No historical record is overwritten. Keep original full review distinct and existing full-review behavior compatible.

C1 also replaces the repeated Verification instructions in both plan templates toward 700 words each, mapping each removed passage to its retained duty: Boundary A selection and prose gates; Boundary B timing, clean unchanged final commit, mode/rationale and consumers, range, interpreter, command outcomes/counts/elapsed/Tokens, acceptance commands, non-pass disposition and omissions; Boundary C, timing diagnostics, conditional Tokens retirement, review fixes and final commit duties. Keep checks, not merely field names. Replace the old closing sentence in both plan and light-proposal templates and lifecycle guidance with `**Benefit versus cost**: <verdict> -- <benefit>; cost <measured>; remaining burden <measured>`. Verdict is `worth it`, `partly`, `not worth it`, or `unknown` with revisit condition. Use the declared implementation-to-tested range for Git counts and net burden; distinguish aggregate agent elapsed from wall time, report missing as `unknown`, and include available decision counts, shipped/always-loaded word changes, test count/runtime and installed-file deltas from existing records. No new collector or review stage.

C2: board `--next` recognizes the chain without counting amendment records as duplicate original reviews. A missing, conflicting, rejected or ambiguous link/obligation stops selection; a changed Verification or dependency cannot inherit an earlier ACCEPT. The audit command selects each archive's last H2 implementation-verification section only, ignores fenced and quoted examples, lists each plan then verdict totals, reports absent lines `no line` without a new warning, and malformed/duplicate/conflicting current lines `unknown` with advisory diagnostic. Keep historical archives unchanged; preserve existing audit and pulse evidence semantics. Document `python tools/audit_report.py` for the existing release-closeout owner; it is read-only, advisory and not a release gate.

## Acceptance criteria

### C1

The paired rules and published explanations agree on the revision, stop, review and resume conditions and retain accepted baseline, immutable history and all prior assurance duties. Compare each original Verification duty and receipt field to its new home; measure both sections and both always-loaded caps (Cairn 2,000; shipped 1,500). The 700-word target is not a cap or permission to omit evidence. Light and planned final records use the same countable line, including unknowns and range.

### C2

Extend `bootstrap/tests/test_board_json_contract.py` through `board.py --next --json` for both board copies using temporary artifacts: a complete ordinary/security chain continues; absent, conflicting and rejected links stop; Verification-only weakening and changed dependency cannot reuse old approval. Extend `bootstrap/tests/test_replacement_tools.py` through `python tools/audit_report.py --root <temporary-root>`: last versus earlier record, historical absence, duplicate/malformed current line, fenced/quoted example, and valid totals. Preserve existing public pulse and review-evidence behavior. Tests assert structured fields, verdicts and stop behavior, not prose wording; temporary developmental probes are removed. Security preflight S2/S3 uses these real entry points; no identity authentication or tamper-proof Git is claimed.

## Scope delta

**Scope delta**: preserved.

## Verification

Before implementation run `python tools/test_tiers.py for <changed paths>`; pass the reviewed range for governing text. Run mapped tests and applicable claim, link/content, snippet and neutrality prose gates; count negative searches against a known-positive case. Compare paired copies and receipt-duty mapping, measure word counts and exercise the named public commands. Boundary C is independent ordinary and Security code review with targeted falsification. After reviews, Boundary B is wide for governing and trust surfaces, on a clean unchanged final commit: mapped iteration and integration tests, owning/public paths, standing gates and plan-specific commands. Record mode and rationale, full tested SHA and reviewed range, interpreter, pre/post state, command table including outcomes, elapsed and Tokens, non-passes and omissions. Certification remains separate.
