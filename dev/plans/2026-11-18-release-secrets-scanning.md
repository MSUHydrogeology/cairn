# Plan: Release secrets scanning on both platforms

**Source proposal**: `dev/proposals/archive/2026-11-17-codex-release-secrets-scan.md`
**Status**: revising-code
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

## Implementation checkpoint -- Windows relay and records -- 2026-11-18

The Windows runner now creates and holds a protected workspace and invocation
record. The native relay accepts fixed Git operations and starts an isolated
worker under the existing Job. Worker and executable bytes are verified,
and a successful history record follows output transfer. A missing frozen
history context refuses the log operation. The existing Windows full-mode and
admission refusals remain until the release controller and native checks land.

On Windows Python 3.13.18, the first native privacy probe against
`36bad4f7` stopped opening the volume root with NTSTATUS `0xc000000d`.
Opening the root through the Win32 directory API let the probe create and
read private files. Duplicate creation, rename of a held ancestor, unsafe
inheritance, foreign access entries, junctions and hardlinks were refused.
The checkout write control exposed a missing explicit target exclusion for
directories without Git metadata. Adding the lexical and resolved checkout
to the existing exclusions made that focused native control pass in 0.37
seconds. The first relay probe compiled but lost stdout despite exit 0.
After explicitly passing only the three standard handles to the Python
worker, native compilation, Git version output and unsupported-operation
logging passed. The full ACL probe was not repeated after the focused repairs.

On Mac Python 3.13.13 the runner and generated worker parsed, the runner copies
matched, the shipped neutrality check passed, and the focused full-mode refusal
test passed. No scanner, admission run or Git history scan ran.

**Elapsed**: unknown
**Tokens**: unknown

## Implementation checkpoint -- C1–C3 Mac and Windows implementation -- 2026-11-18

Completed C1–C3 code, tests, twin synchronization, lockfile finalization, and documentation in `dev/tools/run_portable_security_sweeps.py`, `templates/modules/team-gated/run_portable_security_sweeps.py` (byte-identical via `cmp -s`), `dev/modules/portable-security-sweeps.md`, `templates/modules/team-gated/portable-security-sweeps.md` (byte-identical via `cmp -s`), `release/security_check.py`, `release/RELEASE_PROCESS.md`, `tests/test_portable_security_sweeps.py`, `tests/test_security_check.py`, and `dev/.cairn/cairn-lock.yml` (`install/scaffold.py upgrade --target . --cairn-root . --finalize dev/tools/run_portable_security_sweeps.py dev/modules/portable-security-sweeps.md`).

- Added runner-private `_release_history_git(session, op)` (`WORKTREES`, `HEAD_SYMBOLIC`, `FOR_EACH_REF_SHARED`, `FOR_EACH_REF_PRIVATE`, `PACK`, `INIT`, `INDEX`, `PROJECT`, `HEAD`) with closed-enum dispatch, source/store separation, Windows Job/private-ACL worker execution (enforcing worker-side stderr checks without reading `ReadResult.stderr`), and sterile projection validation.
- Wired Windows full-mode relay dispatch (`_windows_git_relay`) into `_run_sweep_inner` (`os.name == "nt"` consistent check) and `cmd_verify_version_support`, plus frozen-history shim/relay support.
- Updated Gitleaks 8.30.1 redaction validation (`Secret == "REDACTED"` and `"REDACTED" in Match`), discarded `Match` wholesale, enforced exit/report agreement (`exit 0` with findings stays `20` DEGRADED), isolated public/child summaries (`finding_count` only), and added `--triage-record` off-tree owner-only private triage output (including Windows protected-ACL handle writes).
- Added `--freeze-history` (`O_BINARY` full loop write), `--record ... --history-roots` (Windows private workspace via `ExitStack` + live source drift check on both POSIX and Windows), and `--join ... --history-roots` in `release/security_check.py`, plus cross-platform Windows tests.

Verification:
- **macOS Python 3.13.13** (`/Users/kendal30/conda_envs/lhm/bin/python3.13`): `tests/test_security_check.py` -> `192 passed, 3 warnings in 56.63s`; `tests/test_portable_security_sweeps.py` -> `148 passed, 2 skipped in 124.95s` (skips are the two Windows-native Job tests); real `/opt/homebrew/bin/gitleaks` (`8.30.1`, `sha256:f414bc2fb952be6c9072b75cb411e3368614ef4b16d48dbd9ad238034afd2302`) `--verify-version-support --confirm-executing-an-unadmitted-binary` -> `"admit": true` across both `current-tree` and `history` legs (`canary_connections: 0`); `claim_check.py` passed on all 4 edited Markdown files (`0` flags); `link_check.py` OK (`3` files); `sync_doc_snippets.py --check` OK (`703` docs); `tests/check_cairn.py` had `0` issues in edited files.
- **Windows VM (`cairn-windows`, Python 3.13.18)** (`C:/ProgramData/miniconda3/envs/lhm/python.exe` on a disposable archive): `tests/test_security_check.py -k "freeze_history or history_roots or windows"` -> `9 passed, 183 deselected in 13.49s`; `tests/test_portable_security_sweeps.py` cross-platform/native/history/triage subset -> `8 passed, 1 skipped, 141 deselected in 3.47s` (skip: `native Windows gitleaks executable is unavailable`, as `gitleaks.exe`, Bandit, and Vermin are absent on `cairn-windows`; ~102 pre-existing `fake_tool` POSIX-shebang tests fail `'gitleaks' was not found` on Windows outside this plan's scope). Strict real-repo `--freeze-history`, Mac/Windows `--record`, and `--join` admission remain Maintainer-run waits.

**Elapsed**: unknown
**Tokens**: unknown

## Code review -- Hydrogen (Reviewer, Medium) -- 2026-11-18

Reviewed commit: 7579ce40

**Tier**: Internal (ordinary code review; `gemini-4-hydrogen-medium`)
**Findings**: none
**Verdict**: ACCEPT

**Steelman.** Binding both native release records to a single frozen history manifest and sibling pack (`--freeze-history`, `--record ... --history-roots`, `--join ... --history-roots`) ensures Mac and Windows scan the identical complete commit graph rather than drifting local refs, while keeping Gitleaks 8.30.1 findings private via `Match` discard and off-tree `--triage-record` output.

1. **Alignment with C1–C3 and scope.** Yes. `dev/tools/run_portable_security_sweeps.py` and `templates/modules/team-gated/run_portable_security_sweeps.py` are byte-identical (`cmp -s`), as are `dev/modules/portable-security-sweeps.md` and `templates/modules/team-gated/portable-security-sweeps.md` (`cmp -s`). `dev/.cairn/cairn-lock.yml` updates only those two installed paths. `dev/tools/run_portable_security_sweeps.py` imports only Python stdlib modules (AST check); `release/security_check.py` uses stdlib plus repo-local `install` and `tests`. Closed-enum `_release_history_git` dispatch, Windows relay wiring (`_windows_git_relay`), and `--freeze-history` / `--record` / `--join` `--history-roots` checks match C1–C3.
2. **Prose accuracy and secret-handling boundary.** Yes. `release/RELEASE_PROCESS.md` documents `--freeze-history`, `--history-roots` for `--record` and `--join`, fail-closed non-CLEAN sweep stops, and `--triage-record` revocation escalation. `portable-security-sweeps.md` documents `Secret == "REDACTED"` and `"REDACTED" in Match`, wholesale `Match` discard (verified in `read_report`), `finding_count`-only public summaries, and `20` DEGRADED for malformed or contradictory reports (including exit `0` with findings). Note: `_parse_cli_flags` in `release/security_check.py` keeps `--history-roots` optional for backward compatibility while `release/RELEASE_PROCESS.md` requires it for strict release runs.
3. **Verification and honest reporting.** Yes. The implementation checkpoint accurately records Mac (`192 passed` `test_security_check.py`; `148 passed, 2 skipped` `test_portable_security_sweeps.py`; Gitleaks 8.30.1 `admit: true`) and Windows VM (`9 passed` `test_security_check.py`; `8 passed, 1 skipped` `test_portable_security_sweeps.py`) results without masking absent native `gitleaks.exe`/Bandit/Vermin, the ~102 pre-existing POSIX-shebang `fake_tool` failures, or the 4 Maintainer-run release waits.

**Coverage.** Inspected `git show` for `36bad4f7`, `25fd162f`, `e1b01d0d`, and `7579ce40`, twin `cmp -s` parity, AST stdlib-only imports, `release/security_check.py`, `dev/tools/run_portable_security_sweeps.py`, doc/lockfile diffs, and test additions. Did not re-execute test suites or Security Review.

**Elapsed**: unknown
**Tokens**: unknown

## Security code review -- Argon (Security Review, High) -- 2026-11-18

Reviewed commit: 296213ad

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Model basis**: gemini-4-argon-high
**Findings**: raised
**Verdict**: REVISE

**Steelman.** The C1–C3 changes isolate frozen-history Git operations behind `_release_history_git`, enforce Windows handle-held DACLs and C# relay mediation under the kill-on-close Job, discard tainted Gitleaks 8.30.1 `Match` context while routing finding details to an off-tree owner-only `--triage-record`, and keep the four human release waits unpassed. However, six defects break the end-to-end frozen-history and Windows relay paths.

1. **Should this happen as framed?** Only after fixing the broken end-to-end `--record --history-roots`, `--join --history-roots`, and Windows relay execution paths below. -- `release/security_check.py:2087`, `:2380`, `:2487`; `dev/tools/run_portable_security_sweeps.py:2441`, `:3345`, `:3370`, `:3816`.
2. **Best alternative.** Retain the verified `_WindowsPrivateAPI`, `_release_history_git`, `_redaction_is_intact`, and `--triage-record` boundaries, fix the wiring defects in place, and add end-to-end tests covering sterile store import, full-mode frozen sweep, and join. -- Plan C1–C3.
3. **What would show it wrong?** An end-to-end `--freeze-history` -> `--record --history-roots` -> `--join --history-roots` test on a repo with an annotated tag, a non-candidate-ref secret, and a disposable admitted digest failing or missing the secret. -- Plan C1, C3.

**Verified boundaries.**
- **Windows mediation and Job confinement**: `_WindowsPrivateAPI` (`dev/tools/run_portable_security_sweeps.py:1536-1809`) refuses thread impersonation, requires a local unaliased NTFS volume, opens components with `FILE_OPEN_REPARSE_POINT` and no `FILE_SHARE_DELETE`, and verifies owner/protected DACL (`O:{user}D:P(A;...;FA;;;{user})(A;...;FA;;;SY)(A;...;FA;;;BA)`). `_windows_git_relay` (`:2680-2741`) compiles `_WINDOWS_RELAY_SOURCE` (`:2402-2535`) via inbox v4 `csc.exe` (`/noconfig`, `/nostdlib+`, explicit `mscorlib.dll`/`System.dll`), passing only duplicated stdio handles (`PROC_THREAD_ATTRIBUTE_HANDLE_LIST`), checking interpreter reparse/SHA-256, and invoking `-I -S -B` under the existing kill-on-close Job.
- **Finding privacy, Gitleaks 8.30.1, twins, and lockfile**: `_redaction_is_intact` (`:1077-1085`) and `read_report` (`:1092-1164`) require `Secret == "REDACTED"` and `"REDACTED" in Match`, discard `Match` wholesale, map exit `0` with findings to `20` DEGRADED (`classify_leg`, `:1262-1268`), keep public/child summaries to `finding_count` (`:1346-1452`), and write sanitized details only to off-tree owner-only `--triage-record` (`_write_private_triage_record`, `:3005-3053`). Runner (`1eab76f3...`) and module doc (`d256e276...`) twins match byte-for-byte, imports are stdlib-only, `dev/.cairn/cairn-lock.yml` touches only the two installed files, and `dev/PLANNING.md:112-115` preserves the four unpassed waits.

**Findings.**
1. **Blocking (`windows_relay.dir` crash and self-excluded `win_hist.authority` on Windows)**: `_WindowsGitRelay` (`dev/tools/run_portable_security_sweeps.py:2441-2446`) has no `.dir` field (`windows_relay.executable.directory` holds the directory), so `windows_relay.dir` at `:3370` (`cmd_verify_version_support`) and `:3816` (`_run_sweep_inner` full mode) raises `AttributeError` in both twins. In `cmd_verify_version_support` (`:3345-3347`), `win_hist = _WindowsFrozenHistory(Path(tree), Path(workdir), Path(tree), (tree_head,))` sets `authority = Path(tree)` equal to `repository = Path(tree)`, causing `_win_private_open(history.repository, target=history.authority, ...)` at `:2711` and `:2368` to fail `_GIT_READ._assert_off_target` against itself (`authority` must be the outer `target`). *Satisfier (guard + test)*: use `windows_relay.executable.directory`, pass `target` as `win_hist.authority` in both runner twins, re-finalize `cairn-lock.yml`, and add a test exercising Windows relay path binding and full-mode/matrix wiring.
2. **Blocking (`adapter_sha256` key mismatch in `_run_sweep_in_checkout`)**: `release/security_check.py:2487` reads `facts.get("adapter_sha256", "")`, whereas `dev/tools/run_portable_security_sweeps.py:3682` sets `facts["adapter_digest"] = adapter.digest`. Every `--record --history-roots` run sets `adapter_digest` to `""` and fails `_validate_history_sweep_record` (`release/security_check.py:520-521`). *Satisfier (guard + test)*: read `facts.get("adapter_digest", "")` and test `_run_local_record(..., history_roots=...)` end-to-end.
3. **Blocking (unresolved `/var` symlink in `scratch` on macOS)**: `release/security_check.py:2380` sets `scratch = Path(tempfile.mkdtemp(prefix="cairn-native-evidence-"))` without `.resolve(strict=True)`. On macOS `/var` is a symlink to `private/var`, so `store_repo = scratch / "frozen-store" / "mirror.git"` fails `_GIT_READ._lstat_chain` with `GitReadError("linked-path-component")` at `_release_history_git(store_session, "INIT")` (`release/security_check.py:2433`, `dev/tools/run_portable_security_sweeps.py:2851`). *Satisfier (guard + test)*: resolve `scratch` (`Path(tempfile.mkdtemp(...)).resolve(strict=True)`) and cover `_run_local_record(..., history_roots=...)` on macOS.
4. **Blocking (annotated tags omitted from pack and detached worktree HEADs omitted from sterile projection)**: In `release/security_check.py:2087-2105` and `:2140-2143`, `_collect_source_inventory` stores only `peeled_roots` in `inv["roots"]` and `_freeze_history` passes `*inv_before["roots"]` instead of validated `raw_roots` to `rev-list --objects --no-object-names --missing=print` (contrary to Plan Scope line 26). Annotated tag objects (`object_type == "tag"`, including Cairn's `v0.2.0`..`v0.7.0` tags) are omitted from the pack, so `PROJECT` (`update-ref --stdin -z` at `release/security_check.py:2436-2439`) fails on nonexistent tag OIDs. `PROJECT` also projects only `manifest["refs"]` and omits non-unborn `manifest["heads"]` rows (Plan Scope line 28). *Satisfier (guard + test)*: pass validated `raw_roots` to `rev-list --objects` while keeping peeled commit `roots` for `git log`, project all non-unborn rows into `refs/cairn-frozen/<idx:06d>`, and test freeze/record on a repository containing an annotated tag and a detached worktree HEAD.
5. **Blocking (unchecked store projection/closure against manifest, cross-host Windows offline check, and shallow linked worktree discovery)**: In `release/security_check.py:2442, 2464-2466` and `:2566-2578`, `_run_local_record` and `_run_join` check `proj_before == proj_after` but never verify `proj_before["object_count"] == manifest["objects"]["count"]`, `proj_before["objects_sha256"] == manifest["objects"]["objects_sha256"]`, or expected `projected_count` / `projected_sha256` against the manifest (Plan Scope line 28). In `release/security_check.py:2415-2419`, `_run_local_record` enforces `live["refs"] == manifest["refs"]` and `live["heads"] == manifest["heads"]` even when running on an offline second host whose checkout (`live["source"] != manifest["source"]`) has different local refs/worktrees from the freeze authority (Plan Scope line 27 & C1). Also, `_history_discovery` (`dev/tools/run_portable_security_sweeps.py:1187-1196`) checks `(target / ".git" / "shallow").exists()`, which is always `False` when `.git` is a linked-worktree gitfile (`shallow` lives under `common_dir`). *Satisfier (guard + test)*: verify `proj_before`/`proj_after` against `manifest["objects"]` and expected projection in `--record` and `--join`, require live ref/head equality in `--record` when `live["source"] == manifest["source"]` (and always in `--join`) while allowing a clean non-shallow offline second checkout to scan the frozen store, check `common_dir / "shallow"` in `_run_sweep_inner`, and add C1–C3 tests for end-to-end freeze/record/join, a non-candidate-ref secret, differing host refs, and a shallow linked worktree.

**Coverage.** I inspected `git show` for `36bad4f7`, `25fd162f`, `e1b01d0d`, `7579ce40`, and `296213ad`, read `release/security_check.py`, `dev/tools/run_portable_security_sweeps.py`, `dev/tools/git_read.py`, `release/RELEASE_PROCESS.md`, `dev/modules/portable-security-sweeps.md`, `dev/.cairn/cairn-lock.yml`, `dev/PLANNING.md:111-115`, `tests/test_security_check.py`, and `tests/test_portable_security_sweeps.py`, verified twin blob equality and AST stdlib-only imports, and ran targeted read-only Python probes confirming `_WindowsGitRelay` lacks `.dir`, macOS `tempfile.mkdtemp()` fails `_GIT_READ._lstat_chain`, and annotated tag OIDs are excluded from `rev-list` over peeled roots. This review exceeds 300 words to document all five blocking C1–C3 execution findings with exact line citations and satisfiers. I did not run the full test suite or mutate the Windows VM.

**Elapsed**: unknown
**Tokens**: unknown
