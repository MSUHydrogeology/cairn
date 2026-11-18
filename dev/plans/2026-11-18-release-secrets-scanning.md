# Plan: Release secrets scanning on both platforms

**Source proposal**: `dev/proposals/archive/2026-11-17-codex-release-secrets-scan.md`
**Status**: implementing
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

**Freeze and attest.** Freeze from the clean trusted release checkout, ordinary or linked, at candidate HEAD. Pin its top level, absolute Git admin and common directories. Enumerate the main and every registered linked worktree with bounded `worktree list --porcelain -z`; verify each context and common directory. Enumerate shared refs once, excluding `refs/bisect`, `refs/worktree` and `refs/rewritten`; enumerate those private prefixes and HEAD in each worktree context. Record a valid unborn symbolic HEAD explicitly. Label rows `shared`, `main` or exact `worktrees/<admin-id>`, with original ref-name bytes and raw OIDs; store registration and HEAD separately from machine paths. Inaccessible/prunable or malformed worktrees, broken-ref warnings and unavailable inventory are incomplete. Pseudorefs and reflogs are outside the existing `--all` domain. Compare two full live inventories around object collection; never add the scan's detached checkout to this authority.

Use bounded `rev-list --objects --no-object-names --missing=print` over validated raw roots and a final `--`; reject missing objects, failed or truncated reads and roots that cannot peel to commits. Reject shallow, grafted or alternate storage and retain no-replace/no-lazy-fetch/protocol controls. Stream the sorted reachable raw OIDs to sterile `pack-objects --stdout` without `--revs` or `--thin`, under fixed size/time limits. The private manifest binds the non-thin pack SHA-256, original ref/HEAD inventory, candidate, object format and object count/digest; recheck the pinned live inventory after packing. Transfer manifest and pack by the existing private cut channel. The Maintainer runs `python release/security_check.py --freeze-history /abs/private/cut-history.json` on the authority; it exclusively creates the deterministic sibling `cut-history.pack`, then publishes the manifest last. `--record <local> --history-roots /abs/private/cut-history.json` and `--join <mac> <win> --history-roots /abs/private/cut-history.json` derive that sibling, never a manifest-selected path. The manifest binds pack size/hash and private source checkout/admin identities. Mac freeze and record recheck the live source; join runs on that pinned Mac source and rechecks it automatically. Windows remains offline and checks the shared frozen projection and closure around each leg.

Both hosts verify the same manifest and pack, import via `index-pack --strict --stdin` into a new sterile off-tree bare repository using source-owned Git commands, project each non-unborn row into deterministic `refs/cairn-frozen/<zero-padded-row-index>` and set its HEAD to the candidate. Compare exact projected refs/HEAD and reachable object count/digest before and after each leg; any mismatch or missing evidence is unpassed. Create the byte-verified detached candidate checkout from the sterile bare repository on each host; only that mirror acquires the command-owned registration. Compare every mirror shared ref, bare HEAD and exactly one owned detached registration (candidate HEAD, no private refs); extra refs, registrations or drift fail. The detached checkout supplies current files and tests; mediated history reads only the pinned sterile repository and explicit validated peeled commit OIDs, never mutable local refs. The shim uses final `--` with `git log --full-history --root --diff-merges=first-parent --text --no-textconv --no-ext-diff`; this changes diff format, not traversal. Join binds the signed-off source manifest digest, both projection/closure attestations, candidate and policy/runner/admission identities; two full CLEAN legs per host are required.

**History Git owner.** The release controller calls runner-private `_release_history_git(session, op)`, a closed enum with controller-created context, separate from the scanner-facing version/url/log shim. Keep the pinned generic Git reader and its read allowlist unchanged. Fixed read forms are `WORKTREES` (`worktree list --porcelain -z`), `HEAD_SYMBOLIC` (`symbolic-ref -q HEAD`), and shared/private `for-each-ref` inventories with zero stderr; their authority is the pinned source or a verified registered admin view. A detached HEAD's exit 1 is accepted only with empty output, a separate valid commit read and matching metadata. A separate store-context `WORKTREES` read checks the mirror registration. Other ordinary reads use the pinned reader.

`PACK` streams sorted validated full OIDs to `pack-objects --stdout` without `--revs` or `--thin`; the controller exclusively writes capped output to the private sibling. `INIT`, `INDEX`, `PROJECT` and `HEAD` are fixed `init --bare`, `index-pack --strict --stdin`, generated `update-ref --stdin` transaction and `update-ref --no-deref HEAD` forms, restricted to an exclusive off-tree sterile store with private ACL and no link/reparse ancestors. Recheck its identity, initial emptiness, and resulting bare/admin/common identity; never use source paths for write operations or user ref names as destinations. Import verified pack bytes only.

Revalidate the same off-target Git and interpreter identities before launch; use fixed `--no-pager -C` argv, verified base environment and neutral cwd, no shell, prompts, inherited config, replacement or fetch. POSIX uses bounded capture with stdin and cleanup. Windows uses an isolated verified runner-owned dispatch worker under the existing Job, reading bounded identity/digest-checked owned inputs and passing them to its inherited-Job child; never tunnel binary input through generic origin-config. Fixed per-operation caps and deadlines refuse nonzero or incomplete transfers. The scanner shim cannot invoke these operations.

**Finding privacy.** Keep `--redact=100` and bounded strict raw JSON only in private ephemeral workspace. For Gitleaks 8.30.1 require `Secret == "REDACTED"` and a string `Match` containing that exact marker, strict row types and exit/report agreement. Treat Match as tainted and discard it wholesale; surrounding text is not proven safe. Only a narrowly typed alternative demonstrated by the native matrix may be admitted. Never excuse live secrets, malformed or missing output. Write only validated, sanitized bounded path/line/commit/rule/fingerprint to an explicit off-tree owner-only private triage record. Public and child summaries contain statuses, counts, trusted binding IDs and reviewed reason codes only, never raw diagnostics or candidate metadata. Nonempty diagnostic failure, truncation or contradictory output cannot become CLEAN.

The release route records validated safe summaries bound to candidate, platform, architecture, scanner version and admitted digest. Findings require private triage; a committed credential requires stopping and telling the Maintainer to revoke it. Correct the documented redaction-shape incompatibility only when secret-bearing fields can be safely validated without relaying their context; malformed or untrustworthy output stays DEGRADED. Preserve the distinct FINDINGS, INCOMPLETE and DEGRADED results and their precedence. Both legs and both native hosts must be CLEAN for the release check to pass.

The checksum-verified matrix runs explicitly on an unadmitted candidate, followed by Security Review and manual source admission; it admits nothing itself. Retain prior triples and cadence. Land admissions before final scans; changed candidate or scanner inputs invalidate evidence. Create four standalone board waits, each linked to this plan: Mac build admission and Windows build admission owned by the Maintainer, each requiring its checksum, native matrix record, Security Review and reviewed digest entry; Mac candidate scan and Windows candidate scan owned by the release operator, each requiring its native CLEAN two-leg candidate-bound record and matching frozen history. Keep each unpassed until its own evidence exists.

**Reuse.** The runner supplies the two-leg adapter, pinned Git reader, matrix and output validator; its shipped twin is identical. `release/security_check.py` records and joins native results; `release/RELEASE_PROCESS.md` owns instructions. Searches of these files and `tests/test_portable_security_sweeps.py` found existing configuration, redaction, Git, history, admission and twin controls; extend them.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Implement complete frozen-history binding and native Windows mediation and admission capability | Reviewed plan | Runner twins and focused controls |
| C2 | Fix safe finding validation and candidate-bound release evidence | C1 | Private triage boundary and release route |
| C3 | Verify native synthetic scenarios and document operation | C2 | Focused tests, release and module guidance |

Expect several focused sessions, including native Mac and Windows checks; binary behavior and cross-host history are the main uncertainties. No real credential, private history, human admission or release cut is needed for capability verification. Human build approvals, real scans, signing and re-anchor remain separately owned release operations.

## Acceptance criteria

**C1.** Installed full mode and the admission matrix run on native Mac and Windows with equivalent mediated Git controls. Through the release freeze, record and join entries, matching complete frozen roots pass; different refs, a finding in a non-candidate root, missing objects, root drift, shallow linked worktrees, absent compiler, broken mediation or unsupported calls never pass. A complete clean linked worktree passes the same coverage checks; a shallow or drifted linked worktree refuses through record/join. Matrix output alone admits no build. Native controls include a merge or non-candidate-ref secret and broken mediation; public release evidence identifies the same candidate and frozen history on both hosts.

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

## Response -- Terra (Implementation) -- 2026-11-18

**Disposition**: ready-to-implement
**Elapsed**: unknown
**Tokens**: unknown

Accepted both findings. Scope now assigns four separate unpassed admission and scan board waits with owners, evidence and this plan link. The frozen authority inventories shared and each registered worktree's local refs and HEAD; a private non-thin pack and deterministic sterile projections bind both native scans without treating the detached scan checkout as a source ref. C1 now accepts a complete linked worktree and tests shallow/drifted linked refusals. The exact freeze, record and join commands, source-host rechecks and offline Windows projection are specified in Scope.

## Implementation clarification -- Terra (Implementation) -- 2026-11-18

The pinned generic reader excludes worktree and sterile write operations. The History Git owner paragraph names the reviewed private, closed-operation dispatch and separates source reads from sterile-store writes; it changes no accepted outcome, protection or fence. The generic reader and its pins remain unchanged.

**Elapsed**: unknown
**Tokens**: unknown

## Implementation clarification -- Windows private boundary -- 2026-11-18

The runner twins own the Windows private creation and verification helpers. They adapt the smallest applicable Meter token, security descriptor and ACL routines without importing Meter or Pulse: reject impersonation; create exclusively with a protected current-user, SYSTEM and Administrators DACL before writing; hold and validate the local non-reparse ancestor chain; and verify file identity, type, link count, owner, protected DACL and permitted ACEs by handle. Child outputs may inherit the protected root but receive the same SID and handle checks. API, ACL, identity or inheritance failures remain incomplete or refused; there is no chmod fallback. This specifies the reviewed boundary without adding an outcome or fence.

**Elapsed**: unknown
**Tokens**: unknown

## Implementation checkpoint -- Codex Sol (Implementation, High) -- 2026-11-18

Implemented private Windows creation and handle checks in the two portable
runner copies. Exclusive creation applies the protected access list before a
file can receive bytes. Parent-relative handles refuse aliases and stay open
without delete sharing while the caller uses the path. Inherited outputs
require a verified protected root and checked intermediate directories.

Both copies parsed under Python 3.13.13 and compared byte-identical. The
local Windows VM reported Python 3.13.18. Automatic approval review refused
the source and synthetic-fixture transfer, including after verification of
the local VM network, so no native privacy check ran. The helper is an
unverified checkpoint. Integration, native positive and refusal checks,
and independent reviews remain open. No scanner or Git history ran.

**Elapsed**: unknown
**Tokens**: unknown
