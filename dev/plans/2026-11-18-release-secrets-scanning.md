# Plan: Release secrets scanning on both platforms

**Source proposal**: `dev/proposals/archive/2026-11-17-codex-release-secrets-scan.md`
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-18
**Rules that apply**: `dev/rules/conventions.md`, `dev/rules/working-agreements.md`, `dev/rules/protected-surfaces.md`, `dev/rules/development-environment.md`
**In brief**: Make the existing offline secrets scanner check the same complete release history and current files on Mac and Windows.

## Build summary

Extend the existing scanner and release evidence route so a full two-leg scan can be verified on both native platforms. Each host must check the same frozen complete history and candidate, using a separately admitted build. Keep findings private for triage and make missing or untrustworthy evidence unpassed.

## Source proposal

The accepted heavy proposal makes both native scans a required release check, resolves Windows mediation and safe finding triage, and preserves the existing reviewed build-admission process. The capability plan finishes independently of the Maintainer's build approvals and actual release scans.

## Scope

Change the byte-identical `dev/tools/run_portable_security_sweeps.py` and `templates/modules/team-gated/run_portable_security_sweeps.py`, their module guidance and existing policy contract; update `release/security_check.py`, `release/RELEASE_PROCESS.md` and focused public tests. Preserve standard-library-only shipped code, offline operation, pinned executable and Git mediation, candidate-configuration and ignore-file refusals, reviewed fingerprint suppressions, and all existing unadmitted-build and failure distinctions. No governing doctrine change: the module documents the scanner and the release procedure owns the checklist and evidence.

**Native mediation.** Keep the fixed-operation Python Git shim, its pinned reader, configuration screen and invocation ledger. On Windows build an off-tree `git.exe` relay from embedded reviewed C# with the revalidated absolute inbox .NET Framework `csc.exe`, the existing bounded Git-reader Job worker, `/noconfig` and explicit standard framework references; no shell, NuGet or download. Compiler/CLR absence is incomplete. Revalidate interpreter, relay and Git identities and digests; reject on-target or reparse paths; use an off-tree current-user/trusted-admin ACL, neutral cwd, relay-only PATH, `PATHEXT=.EXE` and disabled implicit cwd search. The relay accepts only source-owned version, `ls-remote --quiet --get-url` and log forms, invokes the selected interpreter with fixed `-I -S -B` arguments and an operation enum, and logs/refuses all others. The worker binds the original verified Git-reader bytes, sanitizes the environment, verifies real Git and owns the exact argument vector; ledger success follows bounded output transfer. Retain POSIX mediation, Job process-tree cleanup, include-expanded effective worktree config and all existing hostile-input refusals; no weaker fallback.

**Freeze and attest.** Add `release/security_check.py --freeze-history <new off-tree JSON>`; use `--record <local> --history-roots <frozen>` and `--join <mac> <win> --history-roots <frozen>` with the existing detached-checkout, nonce and strict join. Freeze the full candidate commit, object format, byte-sorted complete ref names and raw OIDs (including packed refs), and count/digest of sorted reachable raw object IDs. Keep the full manifest private in existing cut evidence; public records carry digest and count only. Resolve actual common/worktree directories, reject shallow repositories, grafts, missing, malformed or unavailable objects and failed/budget-truncated reads, and retain no-replace/no-lazy-fetch/protocol controls. Before and after each leg compare local refs, candidate, object count/digest and scope digest to the frozen snapshot. Use bounded `rev-list --objects --no-object-names --missing=print` over raw roots with final `--`; reject missing rows and roots that do not peel to commits. Pass only validated full OIDs within fixed host argument budgets. The shim substitutes explicit peeled OIDs and final `--` in `git log --full-history --root --diff-merges=first-parent --text --no-textconv --no-ext-diff`; this changes diff format, not traversal. Bind candidate and policy/runner/admission identities; both full legs must be CLEAN on each host before join.

**Finding privacy.** Keep `--redact=100` and bounded strict raw JSON only in private ephemeral workspace. For Gitleaks 8.30.1 require `Secret == "REDACTED"` and a string `Match` containing that exact marker, strict row types and exit/report agreement. Treat Match as tainted and discard it wholesale; surrounding text is not proven safe. Only a narrowly typed alternative demonstrated by the native matrix may be admitted. Never excuse live secrets, malformed or missing output. Write only validated, sanitized bounded path/line/commit/rule/fingerprint to an explicit off-tree owner-only private triage record. Public and child summaries contain statuses, counts, trusted binding IDs and reviewed reason codes only, never raw diagnostics or candidate metadata. Nonempty diagnostic failure, truncation or contradictory output cannot become CLEAN.

The release route records validated safe summaries bound to candidate, platform, architecture, scanner version and admitted digest. Findings require private triage; a committed credential requires stopping and telling the Maintainer to revoke it. Correct the documented redaction-shape incompatibility only when secret-bearing fields can be safely validated without relaying their context; malformed or untrustworthy output stays DEGRADED. Preserve the distinct FINDINGS, INCOMPLETE and DEGRADED results and their precedence. Both legs and both native hosts must be CLEAN for the release check to pass.

The checksum-verified matrix runs explicitly on an unadmitted candidate, followed by Security Review and manual source admission; it admits nothing itself. Retain prior triples and cadence. Land admissions before final scans; changed candidate or scanner inputs invalidate evidence. Human Mac and Windows approvals and real scans are separate unpassed release waits.

**Reuse.** The runner supplies the two-leg adapter, pinned Git reader, matrix and output validator; its shipped twin is identical. `release/security_check.py` records and joins native results; `release/RELEASE_PROCESS.md` owns instructions. Searches of these files and `tests/test_portable_security_sweeps.py` found existing configuration, redaction, Git, history, admission and twin controls; extend them.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Implement complete frozen-history binding and native Windows mediation and admission capability | Reviewed plan | Runner twins and focused controls |
| C2 | Fix safe finding validation and candidate-bound release evidence | C1 | Private triage boundary and release route |
| C3 | Verify native synthetic scenarios and document operation | C2 | Focused tests, release and module guidance |

Expect several focused sessions, including native Mac and Windows checks; binary behavior and cross-host history are the main uncertainties. No real credential, private history, human admission or release cut is needed for capability verification. Human build approvals, real scans, signing and re-anchor remain separately owned release operations.

## Acceptance criteria

**C1.** Installed full mode and the admission matrix run on native Mac and Windows with equivalent mediated Git controls. Through the release freeze, record and join entries, matching complete frozen roots pass; different refs, a finding in a non-candidate root, missing objects, root drift, shallow and linked worktrees, absent compiler, broken mediation or unsupported calls never pass. Matrix output alone admits no build. Native controls include a merge or non-candidate-ref secret and broken mediation; public release evidence identifies the same candidate and frozen history on both hosts.

**C2.** Through the installed runner and `release/security_check.py` record/join entries, clean, known finding, incomplete, degraded, absent or failed leg, unapproved or mismatched build and stale candidate remain distinct and cannot yield a false release PASS. A real-shaped redacted finding is triageable without emitting secret bytes, paths or fingerprints in public evidence; broken redaction remains degraded. Existing fingerprint suppressions require review and are never added automatically.

**C3.** On each native host, run the real checksum-verified candidate through `--verify-version-support <absolute-path> --confirm-executing-an-unadmitted-binary` on synthetic matrix data; it admits nothing. Separately, patch a disposable sealed runner/package copy with only that host/version/architecture's measured digest and invoke the ordinary full release/sweep path on synthetic roots; mismatch and empty-table controls refuse. No test branch, environment override or fixture admission enters shipped code. Detect a planted credential in each leg and refuse broken mediation and redaction controls. Both runs use synthetic repositories and credentials only. Module and release instructions identify the exact public command, output and limits, reviewed admission sequence and separate unpassed human waits. The two runner copies remain byte-identical.

## Scope delta

**Scope delta**: preserved.

## Verification

Before implementation, run `python tests/tier_inventory.py for <changed paths>` and select focused public-promise checks, not a whole family or suite by judgment. Extend `tests/test_portable_security_sweeps.py` and `tests/test_security_check.py` at the installed runner and release record/join entry points. Pair the retained configuration, ignore-file, executable-binding, redaction, output and admission refusals with passing controls; add one focused failing mutation for each new mediation, evidence and history boundary. Run the required native synthetic checks on both platforms and record interpreter, revision, results and gaps; do not scan real credentials or private history. Use `/Users/kendal30/conda_envs/lhm/bin/python3.13` on Mac and the documented `cairn-windows` Python on Windows. Run applicable prose and release checks and preserve independent ordinary and Security code reviews. Independent scientific check: N/A, as accepted. Record benefit versus cost and separate human-operation evidence before archive.

## Plan review -- Terra -- 2026-11-18

Reviewed commit: 6ae1dba4d84957b63718a6256b8205fc236616d9

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes, once the release waits are made actionable: the plan delivers the accepted two-host capability independently of the actual cut. -- Plan Scope and Sequence; source proposal Proposal 1–4.
2. **Best alternative.** Reuse the existing scanner, admission matrix and release record rather than create a second scanning route; reduced mode cannot establish the accepted full check. -- Plan Reuse; source proposal Alternatives considered.
3. **What would show it wrong.** A synthetic secret in a non-candidate root missed on either host, or a join passing with drifted roots, would disprove the coverage claim. -- Plan C1 and C3.

**Blocking:** The plan names separate human approvals and real scans as unpassed release waits but does not provide for named standalone board waits with an owner, required evidence and a link to the implementation. Add those provisions for Mac and Windows approvals and actual scans, keeping each unpassed until its evidence exists. -- Source proposal Proposal 3–4; `dev/agent_collaboration.md` > Plans and records.

**Rule loss and audience:** No applicable duty is deliberately removed; the missing wait records above must preserve the release operator's next action and evidence. Existing module and release homes remain named.

**Coverage:** Read the committed plan, accepted proposal, plan template, review and verification rules and existing release and module entry points. No tests, probes, native runs, real scans or detailed security-design review; the separate Security Review remains due.

## Plan review -- Sol -- 2026-11-18

Reviewed commit: 6ae1dba4d84957b63718a6256b8205fc236616d9

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Model basis**: GPT-6.2-sol High
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** The fixed-operation Windows relay, bounded Git reader, private triage and reviewed admission preserve the trusted-checkout contract. The root inventory needs a correction below. -- Scope; source proposal Proposal 1–4 and S5.
2. **Best alternative.** Reuse the pinned reader and detached release record, using the same release repository view to inventory refs at freeze and around each leg. -- `release/security_check.py:1268`; Scope.
3. **What would show it wrong?** A secret reachable only through a worktree-local ref disappears between freeze and scan, or an otherwise complete linked checkout cannot pass. -- C1; [Git worktree ref rules](https://git-scm.com/docs/git-worktree#_refs).

**Blocking:** C1 says linked worktrees never pass, yet the normal record path creates one. Freeze and scan can also see different refs because Git keeps `refs/bisect`, `refs/worktree` and `refs/rewritten` per worktree. Specify and use one pinned release-repository ref inventory for freeze and before/after comparisons, including how worktree-local refs enter it. Bind detached candidate and object traversal to that inventory. Require a clean complete linked control and shallow or drifted linked refusals through record/join. -- `release/security_check.py:1268`; accepted Proposal 1.

**Rule loss:** The design retains mediated Git, fail-closed admission and separate human release authority. The linked-worktree criterion would prevent the accepted normal release workflow.

**Coverage:** Read the committed plan, accepted proposal, runner and release paths, module contract and relevant Git and Gitleaks source documentation. No tests, executable probes, native runs, admissions or real scans.
