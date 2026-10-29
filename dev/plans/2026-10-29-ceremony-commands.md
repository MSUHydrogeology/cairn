# Plan: Reusable ceremony commands

**Author**: Codex (gpt-6.1-terra)
**Source proposal**: [dev/proposals/archive/2026-10-29-codex-ceremony-commands.md](../proposals/archive/2026-10-29-codex-ceremony-commands.md)
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Give the Maintainer reusable commands for checking and carrying out trust ceremonies with human approval.

## Source proposal

The accepted proposal supplies reusable reanchor and repin commands and the trust plan's full verifier, preserving the staged ceremony, independent checks, explicit human decisions and separately authorized authority transitions.

## Scope

Extend `scripts/repin.py`, `scripts/reanchor_ceremony.py`, `bootstrap/reanchor.sh`, their launcher and tests; document inputs, preparer and independent checker in `bootstrap/REANCHOR_RUNBOOK.md`. A maintained human-runnable entry point prepares the details; it does not push or automatically commit AST changes without explicit Maintainer authorization. The verifier must work before the narrowed trust boundary is installed, because it is that plan's S3 prerequisite; the trust plan remains open through its own review and installation.

**Reuse.** Searching `rg 'repin|reanchor|scan-digest' scripts bootstrap` found the v0.5 driver, read-only preflight, staged launcher and prior-P scan. Extend those paths and preserve the ordinary boot refusal on changed authority; do not replace them with candidate-controlled authority.

### Documentation / doctrine surface

Operator description belongs in the runbook; deliberation here. No doctrine change is assumed; governing text changes require their own authority.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Preparation and verifier | Both plan reviews | Reusable preparation, authenticated P and raw C checks, full report and dispositions |
| C2 | Ceremony entry paths | C1 | Ordinary and separately reviewed transition paths, staged checks and scratch demonstrations |
| C3 | Verification and review | C2 | Wide Boundary B, independent code and Security Reviews |
| C4 | Actual installation | MAINTAINER-ONLY; separately authorized each transition | Human-run signing and root installation under the trust plan |

## Acceptance criteria

**C1.** With key away, authenticate immutable signed prior anchor P, its `bootstrap/tests/_gate_preflight.py` and `bootstrap/tests/fixtures/gate_manifest.json`; inspect clean committed C from raw objects and hashes. Require anchor and full collection. Display exact and grouped protected HOLDs and ordinary notes, including all candidate reports; require human dispositions bounded to displayed evidence, never automatic waivers. Missing or inconsistent inputs, collection errors and unresolved HOLDs refuse. An independent reader checks verifier provenance; document residual candidate-code influence. The 83 pending candidate reports require disposition on actual evidence, not an assumed waiver.

**C2.** Document and demonstrate preparation through reviewed AST deletions, reader record, write, exact-path commit, stop, interruption and fresh-package rerun for ordinary and changed-authority paths. Preserve Y1–Y5, stage 1, raw and expected E1–E6, H and K comparisons, human approval, stage 2 and signature verification with one passphrase. E5 independently checks launcher bytes. E7 runs authenticated old-P scanner and agrees with the report before signing. Dormant-roster and active-checker bridges each have their own candidate, packet, reader record, comparisons and explicit Maintainer authorization. Preserve prior scanner semantics; refuse an unsafe transition.

**C3.** Exercise documented public commands in scratch repositories with throwaway keys, honest controls and mutations of signature, checker, raw C hash, roster, collection, disposition and comparisons. In each bridge an altered candidate scan digest must fail E7 with a passing control. Verify one signing prompt, signature and no push. No real key or ref changes.

**C4.** No implementation agent performs actual signing or ref installation. Each bridge needs its own authorization and evidence; neither authorization implies the other, a HOLD waiver or a push.

## Scope delta

**Scope delta**: preserved; no accepted outcome is removed.

## Verification

Boundary A maps `bootstrap/tests/test_repin.py` (boot, AST and refusal), `bootstrap/tests/test_repin_ceremony.py` (public staged entry, signing and E7), `bootstrap/tests/test_reanchor.py` and `bootstrap/tests/test_reanchor_driver_disclosures.py` (launcher and disclosures), plus `bootstrap/tests/test_gate_manifest.py`, `bootstrap/tests/test_gate_transition.py`, `bootstrap/tests/test_gate_preflight.py`, `bootstrap/tests/test_gate_reanchor.py` and `bootstrap/tests/test_ceremony_review_report.py` (manifest, transition, prior checker and reports). Add public-entry cases to these owning families; trace changed callers and fixtures and add their owners before implementation verification. Run `python scripts/check_cairn.py`, `python scripts/claim_check.py`, `python scripts/link_check.py`, `python scripts/sync_doc_snippets.py --check`, and `python scripts/quality_gate.py --sub neutrality` for their respective prose, claim, link, snippet and neutrality properties; resolve any unsupported invocation before use.

Boundary B is **wide** for this trust ceremony: run the mapped families, documented scratch entry paths, mutation controls and standing gates on the clean final implementation SHA with canonical Python 3.13; record exact SHA, range, commands, timings, counts, omissions and non-passes, clean pre/post state, and **Certified by**: pending. No full-suite certification is implied. Fresh independent Terra plan review and Sol Internal Security Review precede implementation; independent code and Security Reviews falsify the final range. C4 stays fenced.
