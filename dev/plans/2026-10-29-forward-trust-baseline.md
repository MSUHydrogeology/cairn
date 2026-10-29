# Plan: Forward trust baseline machinery

**Source proposal**: dev/proposals/archive/2026-10-29-codex-forward-trust-baseline.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Build and test a reusable way to establish a reviewed starting point for future trust checks.

## Source proposal

The Maintainer accepted the revised forward-baseline contract and its grouped historical scope loss. Build the machinery and independently review it before the separate v0.6 installation. The old protections remain active until installation.

## Scope

Implement an explicit no-signed-predecessor preparation and installation path in the existing ceremony machinery, its tests and operator documentation. The approved roster is `dev/plans/archive/2026-10-28-test-trust-boundary/c1b-proposed-roster.json`: 78 test files and 12 controlling Python modules, plus its approved protected scripts, modules and fixtures. Do not reclassify it. Preserve ordinary signed-prior authentication and future comparisons. The existing board item in `dev/PLANNING.md` carries real installation; affected plans have already archived under their amended fences. No real ref move, signing, push or historical comparison is authorized here.

**Reuse.** Search `scripts/repin.py` for `extract`, `build_packet`, `build_transaction`, `apply_reviewed_pin`, `check_record`, and `run_ceremony`; `bootstrap/tests/_gate_preflight.py` for `rederive_static_manifest`; and `bootstrap/tests/_gate_reanchor.py` for authority and ref checks. Extend those paths where their guarantees fit rather than duplicating them. Trace changed imports and callers before implementation.

### Documentation / doctrine surface

Update descriptive operator instructions in `bootstrap/REANCHOR_RUNBOOK.md` and governing text only if the reviewed mechanism requires it; route any prescription under `docs/DOCUMENTATION_PLAN.md`. The separate board item must retain certification before real re-anchor and `python bootstrap/security_check.py` at the eventual clean release commit with required tools and no skip, xfail or xpass; update it at the archive serialization point if needed.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Define and implement candidate preparation and package | Plan reviews | Extraction, independent roster/static derivation, preparation and reader binding |
| C2 | Implement installation and forward verification | C1 | Refusal checks, signed commit and atomic ref transaction; scratch demonstrations |
| C3 | Document and verify | C2 | Operator instructions, scoped evidence, independent code and Security Reviews |
| C4 | Actual baseline installation | MAINTAINER-ONLY: separate exact candidate, package and signer authorization | Separate v0.6 board item, not a prerequisite for this plan's archive |

## Acceptance criteria

**C1.** Extract the clean committed candidate from Git objects; check containment and membership; collect without signing credentials. Bind the independently supplied approved roster, candidate, manifest, collection, interpreter, tool hashes and reader record. Determine required AST/lockfile preparation using existing transaction checks: an implementer prepares and commits any required changes, an independent reviewer reviews them before final candidate/package review, and missing preparation refuses. Independently derive static fields; candidate-controlled expectations cannot authorize its roster.

**C2.** Bind the reviewed launcher, installer and its complete imported execution closure to the reader record and approval; compare executing bytes before signing or ref updates. Expected signer fingerprint is supplied independently of candidate signers. Installation rechecks candidate and package, runs no candidate tests, signs once, verifies candidate parent and manifest-only change, records old anchor ID without comparison, and atomically updates both refs against observed values. Scratch public-path controls demonstrate refusal of roster substitution, missing preparation, changed executing code, wrong signer, stale reader/package and either stale ref, with neither ref moved on refusal. A disposable anchor demonstrates subsequent protected byte/node loss and new-marker HOLDs; ordinary changes yield notes, unrostered tests notice, and full collection and release outcome refusal remain intact. New protected tests require reviewed admission.

**C3.** Document actual human-invoked commands and their checks, limitations and independent approval inputs. Record passing controls, mutations and omissions. Ordinary and Security code reviews challenge current controls and the new public paths. Machinery archive does not claim the boundary is installed.

**C4.** The Maintainer independently authorizes and performs installation for the exact candidate, package and signer after canonical certification. The separate release security run remains required at the eventual clean release commit. This plan does not execute C4.

## Scope delta

**Scope delta**: preserved. The source Decision permits the grouped historical losses; the separate board item carries real installation and its release dependency.

## Verification

Boundary A and B use the canonical Python 3.13 interpreter. Map changed callers and exact nodes before implementation, adding tests to these owning families: `bootstrap/tests/test_gate_manifest.py` (roster, collection, protected and ordinary outcomes); `bootstrap/tests/test_gate_preflight.py` and `bootstrap/tests/test_gate_transition.py` (closure, static derivation and substitution); `bootstrap/tests/test_gate_reanchor.py` (installation and signed-prior checks); `bootstrap/tests/test_reanchor.py`, `bootstrap/tests/test_reanchor_driver_disclosures.py`, `bootstrap/tests/test_repin.py` and `bootstrap/tests/test_repin_ceremony.py` (public ceremony paths); `bootstrap/tests/test_security_check.py` and `bootstrap/tests/test_security_marker.py` (release outcomes). Include newly identified callers and fixtures. Run scoped families in guard-compliant batches, reconcile their union, and record counts and non-passes. Exercise real preparation and installation in disposable repositories with unmutated controls and each C2 refusal; record each result. Run claim, link, snippet, neutrality and prose-integrity gates as applicable to changed documentation.

Boundary B is **wide** for this trust ceremony: on the final clean committed implementation run the mapped families, public paths and standing gates, record SHA, range, interpreter, clean pre/post state, timings, outcomes and omissions, and `Certified by: pending`. A missing required check keeps the work open. No full certification is authorized by this plan; the separate installation item retains it. Boundary C belongs to independent reviewers, who falsify the claims and assess the mapping without running the full suite.
