# Plan: Make release verification an explicit choice

**Source proposal**: dev/proposals/archive/2026-11-05-codex-opt-in-release-verification.md
**Author**: gpt-6.1-terra (Medium), plan author
**Status**: implementing
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


## Plan review -- GPT-6.1 Sol (Security Review, High) -- 2026-11-12

Reviewed commit: `326f9474`.

**Obligation**: Internal Security Review
**Tier**: Internal
**Findings**: none
**Verdict**: APPROVE
**Elapsed**: approximately 12 minutes, shared across both plans.
**Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: the ordinary route explicitly accepts distribution-channel trust while requiring fixed official selection and an exact clean checkout before execution; the stronger route retains independent fingerprints and verified-object binding -- C1 and source Proposal 1–4.
2. **Best alternative.** Keep the manual four-value record in the same adopter commit and reuse current install, integrity and verifier entry points; a new flag, field or automatic verifier would add a contract without improving the accepted procedural outcome -- Scope and C1.
3. **What would show it wrong?** A redirected or stale selection, verification-to-checkout swap, altered apparatus or wrong/missing record must fail the documented criterion; exercise every source negative with independent expectations -- C1 and source Tests required.

The source specifies: trusted acquisition tools, isolated Git configuration, selected tag/version/full SHA, fetched annotated object, checkout identity and same-commit read-back. Signature failure cannot silently select ordinary mode; existing stricter adopter policies still bind. The contained verifier's exit 3 remains an unsigned integrity pin, and 1/2 stop. I traced that exit contract in `bootstrap/container/verify-ref.sh`; its candidate-local status remains explicit, so it cannot establish initial trust.

No rule weakens beyond the expressly accepted ordinary-route assurance change. Developer signing, install/integrity checks and publication duties remain. Real-adopter operation/publication is a separate Maintainer wait, not an archive prerequisite or an authorization granted here.

**Coverage:** I compared the committed plan, accepted source/Decision, current template and verifier/public-test homes. I did not execute either recipe, negative controls, signatures, installs, upgrades, publication or tests/suites. A coherent compromised distribution remains a stated residual; manual recording is auditable, not machine-enforced. Boundary B remains unpassed.


## Plan review -- GPT-6.1 Terra (ordinary reviewer, Medium) -- 2026-11-12

Reviewed commit: `326f9474eeae060c655e4a5ed051d9639187c0c7`.

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: approximately 10 minutes across both queued plans.
**Tokens**: unknown.

The plan removes signing-key setup from ordinary adopter selection while preserving an explicitly stronger route and an honest record of the selected bytes.

1. **Should this happen as framed?** Yes. C1 carries the accepted fixed-source, exact-checkout and same-commit record requirements into an agent-executable local exercise. Actual adopter use and publication remain separate Human operations -- delegated Decision `f2bbc04d`; Scope and C1.
2. **Best alternative.** Reuse current install, integrity and signature entry points and a manual target-commit line. A new verifier or lock field would add machinery beyond the accepted procedural solution -- source Proposal 1–4; plan Reuse.
3. **What would show it wrong?** An ordinary cold reader requiring a key, a changed checkout being executed, or a missing/mismatched selection record being called complete falsifies the result -- C1 and source Tests required.

Source requirements specify the detailed endpoint and checkout controls, so the executor need not invent trust policy. Unsigned verifier exit 3 is distinguished from authenticated success, stronger-policy refusal cannot downgrade, and publisher checks remain. The prose is adopter-facing procedure; agent duties must remain discoverable in their installed guidance. No required check weakens or disappears.

**Coverage:** Compared accepted source and current template, followed the named public verifier/integrity tests, and confirmed publication tests at `bootstrap/tests/security/test_check_release_publication.py` (the plan's shortened `security/` citation is relative to the test root). No recipes, signatures, live endpoints, mutations, source-specific negatives or tests ran. Full local delivery and final integration remain required; this is no publication permission.


## Review disposition -- GPT-6.1 Terra (Implementation coordinator, Medium) -- 2026-11-12

Both required plan obligations are accepted: ordinary `af447c28` and Security `2a4580c3`. Neither pass raised a finding. The operative plan is unchanged and ready for Low-tier execution; all trial controls, scope fences, code reviews and final verification remain due. No runtime result or publication permission is inferred. Elapsed: approximately one minute; Tokens: unknown.
