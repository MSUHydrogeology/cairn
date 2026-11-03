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

## Plan review -- Codex ordinary Reviewer (inherited runtime) -- 2026-11-03

```
Reviewed commit: 6641e0f5612e35940c08b24c934e2d18091db816
Target: operative plan against the accepted forward-trust-baseline contract
Prior findings: none
Assurance path: required(Internal + Internal Security Review); Boundary B wide
```

**Model**: inherited Codex runtime; exact model identifier unavailable.

**Foundations**

1. **Should this happen as framed?** Yes. The accepted contract requires signed-prior membership for later comparisons; the installed narrowed manifest meets a dormant-mode refusal. C1 restores that outcome without replacing authority. -- `dev/proposals/archive/2026-10-29-codex-forward-trust-baseline.md`, Current contract and Decision; anchor `67cdb805`, `bootstrap/tests/fixtures/gate_manifest.json:8754`; `bootstrap/tests/_gate_preflight.py:61`, `bootstrap/tests/_gate_preflight.py:2060`.
2. **Best alternative.** The proposed mode correction, explicit legacy fixture and default-mode regression are the smallest adequate repair. Reuse the resolver; a broad-policy fallback would lose signed membership. -- `bootstrap/tests/_gate_preflight.py:1980`; `bootstrap/tests/test_gate_preflight.py:814`, `bootstrap/tests/test_gate_preflight.py:1034`.
3. **What would show it wrong.** A regression that survives mode-only reversion, malformed or unreviewed changed membership passing, or legacy compatibility failing would contradict C1. Its mutation criterion and retained transition checks address those outcomes. -- Acceptance criteria C1; `bootstrap/tests/test_gate_preflight.py:66`, `bootstrap/tests/test_gate_preflight.py:1702`, `bootstrap/tests/test_gate_preflight.py:5995`.

**Verdict**: ACCEPT.
**Obligation**: Internal
**Tier**: Internal
**Findings**: none.

The selector reproduced the ten named test files in a disposable committed-tree
copy; no tests were run. C2 preserves fresh ceremony inputs and separate
Maintainer operations, consistent with `dev/PLANNING.md:49`.

**Elapsed**: about 3 minutes; **Tokens**: unknown.

**Covered**: source alignment, resolver callers, fixture mismatch, regression
design, mapped checks and ceremony separation. **Not covered**: implementation,
runtime or mutation outcomes, reported certification counts, signature
authentication, or Security Review; no suite or trust operations performed.

## Plan review -- Codex (inherited runtime), Security reviewer -- 2026-11-03

```
Reviewed commit: 29c32d521410267f36964afe6143addca5aeb1cc
Target: operative plan and accepted forward-baseline contract
Prior findings: none
Assurance path: ordinary/Security reviews; wide verification
```

**Model**: inherited Codex runtime; exact identifier unavailable.
**Obligation**: Internal Security Review
**Tier**: Internal Security Review

**Foundations**

1. **Should this happen as framed?** Repair is authorized, but candidate activation cannot restore the existing transition. Forward comparisons remain accepted scope. -- source proposal, Current contract/Decision; plan C1.
2. **Best alternative.** Preserve signed-prior comparisons, or seek explicit Maintainer authorization for the existing forward-baseline replacement, losing predecessor E7 comparison. Fix authorization supplies no such disposition. -- source proposal, Scope delta/Decision; plan authorization.
3. **What would show it wrong?** A narrowed/dormant predecessor refusing before stage 1, or a regression inheriting forced activation, defeats the proposed repair. -- `bootstrap/reanchor-launcher.template.sh:704`; `bootstrap/tests/test_gate_preflight.py:1036`.

**Verdict**: REVISE. **Findings**: raised.

**S1 -- Blocking: predecessor scanner still refuses.** The launcher extracts
P's checker; `range_scan` reaches the dormant-policy refusal. Raw `67cdb805`
has narrowed membership plus dormant code; candidate activation leaves it
unchanged. The coordinator reports exact C34/P67 reproduction: exit 2 (chat,
2026-11-03). `scripts/repin.py:2476` stops before signing. Close with a scratch
public-transition check preserving P authentication, exact roster and E7
comparison, or a named Maintainer disposition authorizing the existing
replacement baseline and explicitly accepting that comparison loss. Neither
route is authorized by this review.

**S2 -- Required-check gap.**
`bootstrap/tests/test_repin_ceremony.py:2251` requires dormant source copied
at line 170. Activation breaks this mapped check. Include its minimal
adjustment, retaining a genuine authority delta and an override-free default
regression.

**Elapsed**: about 4 minutes active review/append preparation; **Tokens**: unknown.

**Covered:** authorization, roster/legacy refusals, fixture masking and
transition sources. **Not covered:** execution, mutations, signature
authentication, suites or signing; reported reproduction and 22-pass probe
were not rerun.
