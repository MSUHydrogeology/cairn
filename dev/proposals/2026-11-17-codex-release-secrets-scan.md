# Proposal: release secrets scanning on Mac and Windows

**Author**: Codex
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-17
**Rules that apply**: `dev/rules/protected-surfaces.md`, `dev/rules/conventions.md`
**In brief**: Make a full secrets scan of Cairn's release candidate and its history a recorded release check on both Mac and Windows.

## Decision summary

Add a repeatable release check for exposed credentials in current files and Git history. Make the existing offline scanner capable of a fully verified run on Windows, approve a scanner build for each release platform through the existing reviewed admission process, and record each result with the release evidence. A release passes this check only when both scans report CLEAN; missing support or evidence stays incomplete. This requires security design, tests and two host build approvals; a clean scan is a tripwire, not proof that no secret exists.

## Context

The v0.8 row in `dev/PLANNING.md` requests this work and equal Windows support. `docs/release-process.md` does not name a secrets scan in its mechanical checks; `bootstrap/security_check.py` does not run the portable sweep. `scripts/run_portable_security_sweeps.py` has an empty admitted-build list, so no build can currently reach CLEAN. Its Windows admission matrix refuses to run, and its full-mode path refuses before the scan legs because full Git mediation is unavailable. The Windows limitation is established by source inspection, not a native run. The module describes the existing two legs, trust boundaries and release admission cadence in `dev/modules/portable-security-sweeps.md`.

The module also documents a real Gitleaks 8.30.1 finding whose redaction shape produces DEGRADED rather than FINDINGS. Neither that result nor a reduced-mode INCOMPLETE is a clean release result. No Cairn history scan or native Windows trial has been run for this proposal.

## Proposal

Deliver a release procedure and its supporting capability for v0.8:

1. Run the existing two-leg offline sweep against the final release candidate on each native platform. Make it an automatic part of the release checking route, with an explicit checklist command and visible per-platform result. Bind the evidence to the candidate, platform, architecture, scanner version and admitted digest; do not silently reuse evidence for changed candidate or scanner inputs. Use the final paths established by the repository-layout work when implementing.
2. A pass requires both legs to complete CLEAN in full mode on both Mac and Windows. FINDINGS, INCOMPLETE, DEGRADED, a missing result or an unapproved build leaves this check unpassed. A finding requires private triage; if a credential was committed, stop and tell the Maintainer to revoke it. Record only safe summaries and dispositions with the existing cut evidence, never secrets or raw reports. Preserve the distinction between a finding and an untrustworthy or incomplete scan; do not change an incomplete result into a pass while the admission list is empty.
3. Preserve the existing checksum-verified, matrix-tested, security-reviewed, manually entered admission process and release cadence. Provide equivalent native Windows admission and full-sweep capability with protections at least as strong as the current trusted-checkout contract, including Git mediation and safe output handling. The implementation plan must design and review those protections before code; do not bypass the existing refusal merely to obtain CLEAN. Keep the shipped code standard-library-only and preserve the byte-identical shipped runner. The Maintainer approves the Mac and Windows builds as separately owned release operations; a matrix report alone does not admit a build. Missing approval remains a release wait, not a completed check.
4. Resolve the documented real-finding redaction incompatibility sufficiently for safe triage without exposing credential material or weakening refusal on untrustworthy output. Retain reviewed fingerprint suppression rules and do not automatically suppress findings.

The plan may finish once the capability and its required checks are reviewed and verified; the human build approvals and actual release scans remain named release waits with their owner and evidence. They are not represented as passed before they happen. This changes the release check, not the authority to cut a release.

## Rationale

Using the existing runner keeps one cross-language, offline procedure and its established trust model. Native results on both platforms exercise the environments the release record already expects. Treating incomplete as a pass would conceal the empty admission list and defeat the check.

## Alternatives considered

Keep the current manual, reduced-mode sweep: it can surface findings but cannot establish a complete clean run, and has no required release record. Running a different scanner or downloading one as part of a release would introduce another executable trust chain; neither is needed for this outcome.

## Documentation / doctrine surface

`docs/release-process.md` owns the release checklist and evidence instructions. `dev/modules/portable-security-sweeps.md` describes the runner's actual contract and admission procedure; the runner and its shipped twin own executable behavior. Update the existing release route and relevant tests at their final layout paths. No new governing doctrine is proposed.

## Evidence / verification plan

### Tests required

The reviewed plan must map public entry points and affected existing nodes in `bootstrap/tests/test_portable_security_sweeps.py` and the release-runner tests. Exercise actual release entry points and both legs using synthetic repositories and credentials: clean, known finding, incomplete, degraded, unapproved and mismatched builds must yield distinct, non-passing outcomes as applicable. Test that a failed or absent leg cannot pass, evidence is candidate-bound, redaction never publishes secret bytes, and scanner or Git configuration cannot evade the retained trust controls. Native Mac and Windows tests must establish the actual admission matrix and full-sweep paths; simulate a known secret and show detection, then show refusal of a broken mediation or redaction control. No real credential or private history is needed in fixtures. An inability to achieve equivalent protection or native coverage falsifies the Windows design and stays open.

### Examples / smoke checks

Run the prose gates and mapped changed-file checks. Demonstrate the documented release route on synthetic inputs on both platforms; record commands, results, omissions and platform details. Actual candidate scans and approvals are separate release evidence.

#### Security preflight

- **S1:** The host supplies Git and the scanner; candidate files, history and repository configuration are input to the scan. Reviewed source admits a digest, not a candidate-controlled policy or scan report. The release operator supplies the candidate and evidence location.
- **S2:** The plan must identify existing negative controls and add failing mutations for any new Windows mediation, redaction and evidence checks; these are required evidence, not yet demonstrated.
- **S3:** The release checklist will invoke the automatic route over the candidate's current tree and committed history on each native host; the exact command and adopter-facing wording must match the implemented entry point and selection. Existing runner entry: `python scripts/run_portable_security_sweeps.py --target . --policy scripts/portable_security_policy.json`.
- **S4:** Missing, mismatched, malformed or untrusted input and failed checks must refuse or remain incomplete, never gain release-pass authority. Findings take precedence over incompleteness where the runner can validate them.
- **S5:** This is a trusted-checkout self-audit, not containment for a hostile scanner or checkout. A malicious trusted executable or a secret outside the scanner's detection rules can still defeat the tripwire.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Windows needs weaker trust controls to reach CLEAN, real findings cannot be triaged safely, clean synthetic fixtures pass when a leg did not run, or recurring release effort outweighs useful detection without a remedy that preserves the outcome.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance

Elapsed: unknown. Tokens: unknown.

## Review -- Codex (Terra) -- 2026-11-17

Reviewed commit: f8fe39d8aa87379c0349106a6ac3aac52f8307f0

**Tier**: usual
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: requiring both native full scans makes the release check meaningful while preserving separate human approvals and real release evidence; a clean result remains a tripwire, not proof. Evidence: this proposal, Proposal 1–4 and Security preflight S5; `dev/PLANNING.md`, secrets-scanning row.
2. **Best alternative.** Keep the existing reduced-mode sweep and manual release process; it avoids the Windows implementation and two build approvals, but cannot deliver the requested full, recorded checks. Evidence: `dev/modules/portable-security-sweeps.md`, version-support cadence; this proposal, Alternatives considered.
3. **What would show it wrong?** Native synthetic tests that cannot detect a known secret or refuse broken mediation, or evidence that safe triage requires weaker controls, would falsify the design. Evidence: this proposal, Tests required and Signals the change is wrong.

The proposal's measurable outcome covers current files and history on both platforms, with incomplete or unapproved results unpassed. Its costs include implementation, security review, native tests and two host approvals; exact recurring effort is not yet measured. Agent-owned capability and checks can finish independently of the Maintainer-owned approvals and release scans.

Coverage: read the committed proposal, full planning row, review guidance, release procedure, and admission and protected-surface documentation. No implementation tests, native runs, real scans, or detailed security design review were performed; the separate Security Review remains owed. The intended release procedures preserve the existing admission contract; their detailed wording and installed homes remain for the plan and implementation.

## Review -- Sol -- 2026-11-17

Reviewed commit: f8fe39d8aa87379c0349106a6ac3aac52f8307f0

**Tier**: Security Review
**Model basis**: GPT-6.2 Sol, High
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: reading approximately one minute; recording and checks unknown.
**Tokens**: unknown.

Two native scans can add useful release evidence while retaining human admission and cut authority.

**Foundations**

1. **Should this happen as framed?** Yes, once both platforms' history coverage is bound to the release evidence. -- Proposal items 1–3 and `scripts/run_portable_security_sweeps.py:2320`.
2. **Best alternative.** Keep the existing two-leg scanner and admission matrix; bind its inputs at the existing native release-record step. Reduced mode cannot establish full results. -- `docs/release-process.md` and `dev/modules/portable-security-sweeps.md`.
3. **What would show it wrong?** Same candidate commit, different scanned history across hosts, and a reported pass. Test with a synthetic finding only in an expected history ref. -- `scripts/run_portable_security_sweeps.py:2320`, `bootstrap/security_check.py:1255`.

**Blocking:** `--all` scans refs beyond the candidate commit. A detached release worktree shares refs, and the runner checks `.git/shallow` as if `.git` were a directory. Define the trusted release history roots and require both records to bind that same complete history. Unavailable, truncated or changed history must prevent a pass, including in linked worktrees. -- `scripts/run_portable_security_sweeps.py:1163`, `bootstrap/security_check.py:1255`.

**Non-blocking:** Land reviewed admission entries before scanning the final candidate. Keep finding paths and fingerprints in private triage; reported metadata can carry candidate-controlled strings. -- `scripts/run_portable_security_sweeps.py:1146`, `:1920`.

**Rule loss:** The proposal retains the existing mediation, output and admission duties and separate cut authority. Rewritten procedures were unavailable.

**Coverage:** Read the board row, release procedure, runner, module and safety contract. No tests, binary admission, real scans or native execution.
