# Plan: Align the checker with the installed baseline

**Source proposal**: dev/proposals/archive/2026-10-29-codex-forward-trust-baseline.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-03
**In brief**: Restore forward checking of the protected-test policy already installed in Cairn's signed baseline.

## Source proposal

The accepted forward-baseline contract promises usable signed-prior checks
after installation. This follow-through repairs that promise; it introduces no
new policy or roster. The Maintainer authorized proceeding with a fix in chat
on 2026-11-03:

> You have my authorization to proceed when you have a fix

## Scope

Change the committed mode in `bootstrap/tests/_gate_preflight.py` to consume
the already installed protected roster. Correct the synthetic legacy manifest
in `bootstrap/tests/test_gate_preflight.py`; it currently copies a narrowed
manifest while promising a broad-policy fixture. Add a regression that uses
the committed default rather than the fixture's forced active mode.

**Reuse.** Keep `resolve_protected_roster`, signed-prior authentication,
reviewed authority transitions and the existing ceremony. No new executable,
switch, file format or policy membership. Searches for `_PROTECTED_ROSTER_MODE`
and `_evidence_repo` locate the existing owners.

### Documentation / doctrine surface

No doctrine change. Correct the mode's obsolete bridge comment. The existing
v0.6.1 board row retains real re-anchoring, signing and publication separately;
none is required to finish this implementation plan.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Align the mode and synthetic fixture; add regression | Both plan reviews | Existing forward checks become usable |
| C2 | Verify and independently review | C1 | Ordinary and Security code reviews; final wide verification |

## Acceptance criteria

**C1.** The committed checker resolves an installed narrowed roster without a
mode override, retaining exact signed roster identity and reviewed-change
requirements. The synthetic legacy fixture explicitly lacks
`protected_roster`. All twenty certification failures are covered by passing
checks. A default-mode regression fails when only that mode is reverted.
Legacy compatibility and malformed/changed roster refusals remain enforced.

**C2.** Mapped checks and independent ordinary/Security reviews complete.
Record any non-pass and limitations. No real trust record, signer, roster
membership or ref is changed by this implementation. Fresh ceremony inputs
are required later because this changes authority code.

Security preflight: S1/S5 retain the accepted local-host and uncontained
collection limits. S2 changes only which existing checker branch runs. S3 is
the default-mode behavior regression plus signed-prior and transition tests.
S4 is demonstrated by reverting the mode in a disposable copy. None of these
tests substitutes for the Maintainer's trust operation.

## Scope delta

**Scope delta**: preserved. This restores the accepted forward-checking
outcome. The quoted authorization covers this protected-file repair; it
waives no security, certification or release requirement.

## Verification

Canonical Python: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13).
Boundary A runs the ten files selected by `tools/test_tiers.py for` the two
code paths: gate-preflight, gate-reanchor, ceremony-review-report,
oracle-activation, reanchor, reanchor-driver-disclosures, repin,
repin-ceremony, review-stance-in-shipped-files and security-marker. These
cover roster resolution, signed-prior/public ceremony paths and consumers.
Use disposable repositories and keys only. Mutation testing changes only a
separate copy, never the signed anchor.

Boundary C is separate ordinary and Security code review. Boundary B is wide,
on a clean final commit after review: the same mapped families and public
paths, plus claim/prose/link/snippet and neutrality/redundancy gates. An
authorized release certification may supply this final evidence once, rather
than repeat those tests separately; its complete non-pass result remains
visible. No ordinary full-suite run is authorized by this plan.

## Release diagnosis -- Codex -- 2026-11-03

**Model**: inherited Codex runtime; exact model identifier unavailable.
**Elapsed**: about 35 minutes including certification; **Tokens**: unknown.

At clean commit `c34eef17fb89683c8bac35478c391d8f9db10e00`, authorized
seed-0 certification returned 5,884 passed, 20 failed and eight native-Windows
skips in 1,521.30 s. The required neutrality/redundancy pair and prose gate
passed; external links were not probed. This is not clean certification.
The real `check` CLI refuses because signed anchor
`67cdb805704425132de3122dacf384830734f5fa` has a narrowed manifest but a
dormant checker. The released v0.6.0 checker produces the same refusal.
All twenty failures are in the gate-preflight family. A disposable mode and
legacy-fixture correction passed 22 focused checks in 5.52 s; that probe is
feasibility evidence, not committed implementation or independent review.
