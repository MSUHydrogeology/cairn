# Plan: Reusable ceremony commands

**Author**: Codex (gpt-6.1-terra)
**Source proposal**: [dev/proposals/archive/2026-10-29-codex-ceremony-commands.md](../proposals/archive/2026-10-29-codex-ceremony-commands.md)
**Status**: revising-plan
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

## Plan review -- Codex (gpt-6.1-terra) -- 2026-10-29

```
Reviewed commit: df4f9ac5290fae5260db52c9016ae918be7c2f68
Target: opening plan, accepted contract, verifier and ceremony paths
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** The staged reuse and fenced installation fit the Decision, but the verifier identity, operator handoff and reviewed test map need correction to establish delivery. -- Plan C1–C4; `bootstrap/REANCHOR_RUNBOOK.md:74`.
2. **Best alternative.** Extend the shipped driver and launcher, using the existing prior verifier and scanner for their distinct jobs; a manual-only path does not deliver the approved reusable commands. -- `scripts/repin.py:971`; `bootstrap/REANCHOR_RUNBOOK.md:74`.
3. **What would show it wrong.** A documented public workflow that cannot prepare and independently check its inputs, invokes the wrong prior tool, or reaches signing after a damaged comparison would fail the accepted outcome. -- Complete current contract; `bootstrap/REANCHOR_RUNBOOK.md:74`.

**F1 — Blocking: identify and isolate the full verifier.** C1 names P's `_gate_preflight.py` and manifest, but the existing human-run full verifier is P's `_gate_manifest.py verify`; the former supplies the independent E7 scan. A plan could satisfy its wording by authenticating the scanner while executing an unverified verifier. The runbook also requires a separate clean target, independently checked against C, and an empty environment with Python `-E -s`. **Satisfier:** bind and independently check the signed P verifier's raw bytes and manifest separately from the E7 scanner; require a prepared, human-runnable command on a separate clean C target with the existing isolation and full-collection/anchor settings, and demonstrate that this documented command triggers the verifier before signing. Preserve the stated residual candidate-code influence. -- Plan C1–C2; `bootstrap/REANCHOR_RUNBOOK.md:64`, `:74`; source contract.

**F2 — Blocking: make preparation and checks demonstrable.** C2 says to document preparation and a reader record, but does not require scripts to prepare values, packets, launcher and reader inputs or identify the preparer and independent checker of each. Nor does it require the Maintainer's actions to fit the accepted run, compare, approve and passphrase workflow. The current driver still requires reader handoff and an AST commit after a stop. **Satisfier:** carry these explicit outcomes into C1–C2 and demonstrate both documented paths through reviewed deletion, record, exact-path commit, interruption and fresh-package rerun without improvising per-ceremony commands; keep the no-automatic-commit and push boundaries. -- source Complete current contract; `scripts/repin.py:971`, `:1027`; Plan C2.

**F3 — Blocking: map behavior to checks before implementation.** Verification lists broad families and defers tracing callers, while the accepted contract requires exact nodes and callers and the template requires a reviewed invariant/public-path mapping. A family list cannot show which check exercises each refusal or documented command. **Satisfier:** map existing exact nodes and changed callers, identify where new public-entry nodes will be added, and associate each planned control and mutation with its owning family, including both bridge E7 controls and the actual full-verifier trigger. Trace affected fixtures and consumers before implementation; preserve wide Boundary B. -- Plan Verification; `dev/plans/_template.md` Verification; `bootstrap/tests/test_repin_ceremony.py:1533`.

**Covered:** claims and completeness (1,3): runbook verifier and source contract; production path and refusal (2,4): `scripts/repin.py:971`, `:1063`, runbook E5/E7 and F1–F3; cross-document and drift (5,6): plan, source contract, trust plan S3 and runbook; lifecycle (7): plan C3–C4 and trust plan C4–C5; scope/domain (8): source contract and plan Scope delta, no scientific result; satisfiers (9): F1–F3. Reuse searches `rg 'repin|reanchor|scan-digest' scripts bootstrap` and `rg 'def (boot|run_ceremony|build_packet|check_stop_records)|commit|delet' scripts/repin.py` have known matches.

**Not covered / low confidence:** review is source inspection only; no tests, mutations, signing or ref changes. This pass does not discharge Internal Security Review.
