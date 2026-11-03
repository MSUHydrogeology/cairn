# Plan: Align the checker with the installed baseline

**Source proposal**: dev/proposals/archive/2026-10-29-codex-forward-trust-baseline.md
**Status**: awaiting-code-review
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
the committed default rather than the fixture's forced active mode. Adjust
the existing authority-transition test in
`bootstrap/tests/test_repin_ceremony.py` to make a genuine closure-byte
change without assuming the committed checker is dormant.

**Reuse.** Keep `resolve_protected_roster`, signed-prior authentication,
reviewed authority transitions and the existing ceremony. No new executable,
switch, file format or policy membership. Searches for `_PROTECTED_ROSTER_MODE`
and `_evidence_repo` locate the existing owners.

### Documentation / doctrine surface

No doctrine change. Correct the mode's obsolete bridge comment. Real
re-anchoring, signing and publication stay separate from plan completion.
At the Maintainer's request, finish those operations in the release handoff,
without another v0.6.1 board row.

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
are required later because this changes authority code. Demonstrate ordinary
and authority-transition operation after a compatible active baseline in
disposable repositories. The actual narrowed/dormant predecessor remains
blocked: use the existing replacement-baseline route under the Maintainer
disposition below, not a new adapter or an automatic fallback.

Security preflight: S1/S5 retain the accepted local-host and uncontained
collection limits. S2 changes only which existing checker branch runs. S3 is
the default-mode behavior regression plus signed-prior and transition tests.
S4 is demonstrated by reverting the mode in a disposable copy. None of these
tests substitutes for the Maintainer's trust operation.

## Scope delta

**Scope delta**: degraded only for the one-time predecessor E7 comparison,
under the Maintainer disposition below. Future protected checks, exact
membership and signed-prior operation remain required. No other security,
certification or release requirement is waived except the separately named
v0.6.1 strict-runner exception.

## Verification

Canonical Python: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13).
Boundary A runs the files selected by `tools/test_tiers.py for` the three
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

## Maintainer dispositions -- 2026-11-03

**Elapsed**: unknown; **Tokens**: unknown. Scribed by Codex.

**Existing replacement-baseline path.** Codex asked in chat:

> May we use the existing fresh-baseline procedure for v0.6.1 after the checker fix and independent review? I recommend it to avoid adding compatibility machinery. We would preserve the signer and exact protected-test list, review the changes from the old baseline, and run the required verification, but explicitly forgo the broken old scanner's automatic comparison for this transition. You would still approve and sign the exact final package. The alternatives are to build and review a compatibility bridge, or hold the release without changing trust.

After Codex reiterated that this route requires the one-time comparison loss,
the Maintainer authorized proceeding:

> Yes please, I need to move on to other things and want this release completed

Use the existing independently reviewed replacement-baseline procedure for
this repair, not a new compatibility adapter. The old scanner's automatic E7
comparison is not preserved for this transition. Retain the current signed
anchor as evidence, review its difference from the final candidate, preserve
the approved roster and signer, and prepare exact independently reviewed
inputs. This is no automatic fallback. The Maintainer alone approves the
final package and signs; no agent may install the real baseline or move refs.

**Strict release runner: v0.6.1-only exception.** Codex asked to carry forward
the v0.6.0 exception while still completing corrected full certification,
focused security scanning and native Windows checks; the strict runner would
remain explicitly unpassed and its repair would be required for v0.7. The
Maintainer answered:

> Authorize the v0.6.1-only exception

The exception does not waive the checker repair, required independent
reviews, corrected certification or actual trust/release approvals. It does
not renew for v0.7. The strict runner's duplicate-suite and platform-outcome
repair is on `0.7-dev` at `136dac9f` as a required pre-release outcome.

## Response to plan reviews -- Codex -- 2026-11-03

**Elapsed**: about 3 minutes; **Tokens**: unknown.

Ordinary review accepted the repair. Security S1 is accepted: the actual
predecessor's `scan-digest` also refuses (exit 2, C34/P67), so candidate
activation cannot make the old transition usable. The Maintainer disposition
at `b4d87555` chooses the existing replacement-baseline path and names that
one-time loss; Scope delta and C2 now say so. No compatibility code or
fallback is added. Actual installation remains a separately approved human
operation, not this plan's completion condition.

S2 is accepted: Scope names the existing transition test's adjustment and C2
retains genuine authority drift plus post-baseline public-path verification.
The override-free regression remains separate. Both plan-review obligations
are recorded; fold complete, with no clearing review.

## Iteration evidence -- Codex -- 2026-11-03

**Model**: inherited runtime; exact identifier unavailable.
**Tested commit**: `9f0bd13ed010cc1f933fa391ef0e9f6163111b90`.
**Range**: `3c6238ec..9f0bd13e`.
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, 3.13.13.
**Elapsed**: 979.44 s for pytest; **Tokens**: unknown.

A clean, branch-attached disposable checkout ran the exact ten-file selector
union with `python -m pytest -q`, `--tb=short` and an external JUnit output:
`test_ceremony_review_report.py`, `test_gate_preflight.py`,
`test_gate_reanchor.py`, `test_oracle_activation.py`, `test_reanchor.py`,
`test_reanchor_driver_disclosures.py`, `test_repin.py`,
`test_repin_ceremony.py`, `test_review_stance_in_shipped_files.py` and
`test_security_marker.py`, all under `bootstrap/tests/`.
**1,476 passed; zero failed, skipped or omitted.** Pre/post tracked and
untracked status was clean and HEAD unchanged. No broad-run or release token
was set. This includes the formerly failing evidence/CLI cases, default-mode
regression and disposable signed ordinary/transition ceremonies.

The focused `bootstrap.security_check.run_bandit` phase passed over 74
Python files, with zero live suppressions. Prose (192 Markdown files), link,
snippet (536 docs), neutrality and redundancy gates passed; external links
were not probed. This is not the strict release command, which remains
unpassed under the named patch-only exception.

Timing targets were exceeded. Per-file JUnit totals over 10 s: repin-ceremony
540.11, gate-preflight 159.12, repin 146.13, reanchor 63.22, security-marker
24.52, ceremony-review-report 19.28, gate-reanchor 18.10. Retain these names
on the existing v0.7 consolidation list.

Production bytes are unchanged by later board cleanup `124b4e85`. Independent
code/Security reviews, final wide verification, certification and the human
baseline/release operations remain owed. No real key or ref was used.

## Code review -- Codex ordinary Reviewer (inherited runtime) -- 2026-11-03

```
Reviewed commit: 9f0bd13ed010cc1f933fa391ef0e9f6163111b90
Target: 3c6238ec..9f0bd13e; iteration evidence at 6d0c1675
Prior findings: none (first code review)
```

**Model**: inherited Codex runtime; exact model identifier unavailable.

**Foundations**

1. **Should this happen as framed?** Yes. The active default consumes installed membership without changing identity/refusal logic; the legacy stub now omits the policy-selecting field. -- `bootstrap/tests/_gate_preflight.py:61`, `bootstrap/tests/_gate_preflight.py:1980`; `bootstrap/tests/test_gate_preflight.py:824`.
2. **Best alternative.** Keep this three-file repair and existing resolver, not new compatibility machinery. The transition test still changes authority bytes; the authorized one-time predecessor comparison loss remains explicit. -- `bootstrap/tests/test_repin_ceremony.py:2251`; Maintainer dispositions at `b4d87555`.
3. **What would show it wrong.** Masked activation or a false legacy fixture would survive reversion. Instead, mode-only reversion fails the new default regression (0.39 s); retaining the roster field fails the evidence round-trip (0.50 s), with passing controls. -- `bootstrap/tests/test_gate_preflight.py:835`, `bootstrap/tests/test_gate_preflight.py:852`.

**Verdict**: ACCEPT. **Findings**: none.
**Obligation**: Internal
**Tier**: Internal
**Bounding**: ACCEPTED -- resolver, evidence collection and signed ceremony
consumers are covered by the mapped families and targeted probes.

Python 3.13.13, separate exact-commit copies: three targeted checks passed.
The changed signed transition/ordinary workflow passed in 25.73 s outside the
restricted runner after an initial throwaway-key passphrase failure there.
The author's committed iteration record reports 1,476 passes, zero non-passes
or omissions, and passing focused security/prose gates; not rerun.
No Maintainer fence became due in the reviewed range.

**Elapsed**: about 5 minutes active review/append preparation; **Tokens**: unknown.

**Covered**: committed diff, refusal logic, fixture/default mutations, public
transition workflow and iteration evidence. **Not covered**: independent
Security Review, final Boundary B, certification, external links or real
baseline/release operations; no suite run or authority granted for them.

## Code review -- Codex (inherited runtime), Security reviewer -- 2026-11-03

```
Reviewed commit: 9f0bd13ed010cc1f933fa391ef0e9f6163111b90
Target: 3c6238ec..9f0bd13e; iteration record at 6d0c1675
Prior findings: plan S1 disposed at b4d87555; S2 implemented
```

**Model**: inherited runtime; exact identifier unavailable.
**Obligation**: Security code review
**Tier**: Security

**Foundations**

1. **Should this happen as framed?** Yes: only the default changes; the signed-roster resolver and trust inputs remain unchanged. The replacement baseline follows the named disposition, not a claim that old P works. -- `bootstrap/tests/_gate_preflight.py:61`; `b4d87555`.
2. **Best alternative.** Retain this resolver and explicit legacy fixture; no adapter or fallback is added. The transition test uses genuine closure-byte drift independently of the default. -- `bootstrap/tests/test_gate_preflight.py:824`; `bootstrap/tests/test_repin_ceremony.py:2252`.
3. **What would show it wrong?** Substitution passing, malformed metadata becoming legacy, or the regression surviving mode-only reversion. Independent probes challenged these; reversion caused the dormant refusal and restoration passed. -- evidence below.

**Verdict**: ACCEPT. **Findings**: none.
**Bounding**: ACCEPTED for the recorded wide mapping; final Boundary B remains owed.

A separate exact-9f copy under Python 3.13.13 passed ten unsigned probe groups
covering trusted raw identity, byte/membership substitution and review binding,
missing/mismatched rosters, six malformed metadata cases,
legacy/compatibility/first-admission behavior and closure-byte admission. One
harness field-name error was corrected. Two targeted nodes passed (0.38s);
mode-only reversion failed the default regression (0.38s), restored code
passed (0.31s). Tracked source bytes were restored exactly.

Read `6d0c1675`'s clean unchanged-commit evidence: all ten mapped files, 1,476
passed, zero failures/skips/omissions, 979.44s; focused Bandit and prose gates
passed. These implementation checks were not repeated.

**Elapsed**: about 4 minutes active work; **Tokens**: unknown.

**Covered:** changed source, mapped consumers, roster refusals, legacy behavior
and mutation sensitivity. **Not covered:** independent signing/ceremony
execution, signature authentication, final Boundary B, certification or real
installation. No suite or real trust operation performed; old P remains
unusable.
