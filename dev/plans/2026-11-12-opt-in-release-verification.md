# Plan: Make release verification an explicit choice

**Source proposal**: dev/proposals/archive/2026-11-05-codex-opt-in-release-verification.md
**Author**: gpt-6.1-terra (Medium), plan author
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-12
**In brief**: Document an ordinary official-release installation and an optional stronger signature check while retaining the selected release record.

## Build summary

Give Git-backed adopters a documented path from an official stable release to a verified install or upgrade without key setup, and a separate optional signed path bound to the checkout executed. Record the complete selection in the target commit by hand. The ordinary route trusts the distribution channel and does not authenticate its operator. Local preparation is authorized; actual use on real adopter work and publication remain with the Maintainer.

## Source proposal

The accepted heavy proposal and delegated Decision `f2bbc04d` authorize reversible local preparation of both routes, the manual record and their checks, without waiving any outcome or publisher obligation. The source's Proposal and Tests required sections govern the full details and negative controls.

## Scope

Revise `bootstrap/PROVENANCE.md`, `bootstrap/BOOTSTRAP.md`, `bootstrap/UPGRADE.md` and `bootstrap/container/recipe.md` as needed, with related descriptive or governing cross-references found by the reader search. The doctrine surface is adopter provenance and install/upgrade guidance; retain developer signing, release testing and publication requirements in `docs/release-process.md`. Preserve existing prerelease and archive capabilities without claiming this route's assurance for them. No new CLI flag, lock field, verifier or automatic record enforcement.

Reuse: `bootstrap/scaffold.py` install and upgrade, `bootstrap/verify_integrity.py --target`, and `bootstrap/container/verify-ref.sh` already own these operations. Searches for those entry points in the four documents and for `test_` in `bootstrap/tests/test_verify_ref.py`, `test_lockfile_provenance.py`, `test_verify_integrity.py` and `security/test_check_release_publication.py` found the existing test homes. Extend only missing public-promise checks there; use disposable development probes for the procedural negatives and remove them afterward.

## Sequence

Estimate one to two focused work windows plus reviews and verification; uncertainty is the cost of independently exercising both recipes and their negative cases. The human release operation is a separate named board wait owned by the Maintainer, with its reviewed implementation and operation evidence; it is not a plan chunk or archive condition.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Write and exercise both documented routes and manual record; preserve existing checks and release duties. | Plan reviews and their responses | Reviewed local guidance and evidence; no real-adopter use or publication |

## Acceptance criteria

### C1

The source Proposal 1–4 holds: fixed official owner, page/API and fetch endpoints, preselected tag/version/full SHA, no redirects or stale refs, annotated tag and clean exact checkout before candidate execution. The ordinary path requires no signer or waiver. The stronger route verifies with independent fingerprint channels and roster, retains and peels the verified object, and executes its clean checkout; failure never downgrades. The contained recipe's `--unprovenanced` exit 3 means integrity pin only; exits 1/2 stop. Existing verifier default and release obligations remain unchanged.

A fresh install and prior-release `upgrade --plan`, `--stage`, `--apply` followed by `verify_integrity.py --target` succeed in disposable Git targets. The same target commit contains installed changes and lockfile plus the manually written official URL, tag, version and full SHA; compare and read it back with `git show -s --format=%B`, matching lock version and short SHA prefix. Missing history, lock change or mismatched tuple is incomplete. A cold reader reaches ordinary execution without key approval; an explicit stricter policy refuses signature failure. Exercise every source Tests required negative using independently fixed expectations; document observations and residual coherent distribution compromise. Retain existing public-entry promise tests; temporary probes do not become a new contract.

## Scope delta

**Scope delta**: preserved.

## Verification

Before implementation run `/Users/kendal30/conda_envs/lhm/bin/python3.13 tools/test_tiers.py for <changed paths>`; add only its mapped checks and the source's required acceptance controls, plus claim, link/content, snippet and neutrality gates for prose. Initial mapping of the four named documents selected 14 files, including `test_verify_ref.py` and `test_verify_integrity.py`; rerun on actual paths. Existing `test_documented_bootstrap_block_refuses_the_substitution`, `test_provenance_mode_requires_a_roster`, `test_unprovenanced_output_says_no_signature_was_checked`, `test_fresh_install_lockfile_carries_provenance`, `test_apply_backfills_provenance_from_new_stage`, `test_tampered_file_fails_closed`, and publication tests for redirects and annotated tags are relevant checks, not substitutes for the source's procedural controls. Compare `docs/release-process.md` before and after to ensure publisher duties remain.

Boundary C is targeted code review, including separate Security Review. Boundary B is wide on the clean reviewed final commit: mapped tests, owning families and public install, upgrade, signature and integrity paths, standing prose gates and all source-specific controls. Record command outcomes, tested SHA, interpreter, pre/post state, timing, non-passes and omissions in the implementation verification record. Certification is separate. A human release or real adopter operation remains unpassed until its own evidence exists.
