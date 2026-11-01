# Plan: Remove the pending certification marker

**Source proposal**: dev/proposals/archive/2026-11-01-codex-certification-label.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Remove the per-change pending marker while keeping checks and one record of each actual tree-certification run.

## Source proposal

The Maintainer accepted the heavy proposal at `8d1c6bde`: remove the mandatory marker,
retain checks and triggers, and record each actual run once in a discoverable existing
shared record. Do not backfill archived plans or create a ledger.

## Scope

Change `AGENTS.md`, `templates/core/AGENTS.md`, both plan templates,
`doctrine/plans.md`, `doctrine/dual-review.md`, `docs/glossary.md`, the refusal message
in `bootstrap/tests/conftest.py`, and affected rule tests and shipped copies. Search for
further live readers and pins before editing. Retain the guard condition, certification
pair, failure and bisect rules, and all Boundary B evidence except the pending field.
Historical records remain intact.

**Reuse.** N/A: no code added. Search for `Certified by`, `certifying run`, and the
refusal message found the above live rules and
`bootstrap/tests/test_certifying_run_rule.py` and
`bootstrap/tests/test_verification_boundaries.py`; the gate manifest pins `conftest.py`
and the former test. Existing guard and rule tests are reused.

### Documentation / doctrine surface

Governing and shipped rules hold the prescription; plan templates and doctrine explain
the record; the glossary describes the distinction. No new document or process is
introduced.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Align rules, templates, refusal message and existing tests | Both plan reviews and author response | The accepted outcome and scoped iteration evidence |

## Acceptance criteria

C1 removes the mandatory per-change field across current surfaces, without weakening any
required change check, certification trigger, guard refusal, failed-run handling or
bisect rule. Tests exercise those retained obligations and the actual refusal, and
reject a restored mandatory marker. Shipped rules remain appropriate to adopters. Each
actual run has one shared record: use the existing release or re-anchor evidence record
for those runs; for a required push or Maintainer-requested run outside those
ceremonies, use the commit message recording the run, headed `Tree certification --
<tested SHA>`. It records tested SHA, commands, results and existing required evidence,
including failures; `git log --all --grep='Tree certification --'` finds it. Readers are
told where to find each kind; no per-plan backfill or new ledger. Absence of a marker
does not prove that a run passed. Security preflight S2/S3: C1 tests the changed
obligations and real guard through the existing tests and scoped checks.

## Scope delta

**Scope delta**: preserved.

## Verification

Before editing, search live references, readers and byte pins, check known-positive
search cases, and run `python tools/test_tiers.py for <paths>` for the actual changed
files. Follow protected-file procedures; no re-anchor is authorized. Boundary A runs the
selected tests and applicable claim, link, snippet and neutrality gates. Verify the
guard still refuses the same broad invocation and test rule mutations against a passing
control. Inspect release and re-anchor evidence homes and demonstrate lookup of each
record type with representative existing evidence; record any gap rather than claim a
nonexistent example.

After independent code and Security Reviews, Boundary B is **wide** for governing and protected surfaces. On one clean unchanged final commit under canonical Python 3.13.x, run the reviewed-range iteration selection plus mapped integration/workflow tests, owning families, installed public paths and standing gates; record SHA/range, clean pre/post state, interpreter, commands, counts, timing, non-pass dispositions and omissions. Boundary C independently falsifies the implementation and mapping. No full certification or re-anchor is authorized by this plan.
