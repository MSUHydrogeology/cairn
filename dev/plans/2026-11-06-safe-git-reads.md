# Plan: One safe boundary for Git reads

**Source proposal**: dev/proposals/archive/2026-11-04-codex-safe-git-reads.md
**Author**: Codex GPT-6.1 Terra (Medium)
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-06
**In brief**: Give ordinary repository reads one verified safety boundary so untrusted projects cannot run programs or turn failed checks into clean results.

## Source proposal

The delegated Sol Decision `05ea5d90` accepted the complete heavy proposal,
including N1–N3 and its delivery fence. The scheduling Decision `67e2c63b`
authorizes this prerequisite plan while architecture work continues. Dependent
Git views wait for this plan's verified boundary; this plan does not wait for
architecture, release or a human trust operation.

## Scope

Implementation paths:
- `templates/skills/_lib/git_read.py`
- `tools/git_read.py`

Deliver the accepted small standard-library helper, byte-identical at
`templates/skills/_lib/git_read.py` and `tools/git_read.py`, through the
existing unconditional skill mapping and install/upgrade contracts. Route all
ordinary readers named in the source proposal: upgrade, install and lockfile;
session; intent conflict and both generated hooks; content runner and audit
preflight; portable sweeps and its shim; link, snippet and self-checkers;
measurements, gauge, tier selector and legacy report. Preserve each caller's
parsing, capability and failure policy, and retire duplicated launch loops.
The accepted proposal's delivery/binding and caller-policy tables are normative
for every member. Keep hooks-path installation, merge-file, privileged gate,
release, signing, re-anchor and publication runners separate as specified.

Bind trusted helper bytes before execution in source and installed layouts,
including dispatcher, audit before injection, direct content/sweep, other first
importers and shim; pin reviewed bytes in trusted caller source, enforce required
lock records and execute the verified buffer. Never use target-selected code,
CWD, cached unverified modules or candidate-adjacent digests as authority.
Keep anchor-session extraction self-contained. Preserve fixed diagnostic policy,
caller-specific empty/absent/failure translations and the pre-confirmation
no-Git exception. A High-tier owner must resolve and document the remaining in-contract
mechanisms for verified-buffer loading, enclosing-worktree exclusion before
probing, and Windows process/descendant cleanup before Low-tier execution.
New boundary questions also require High-tier judgment; no outcome is waived.

**Reuse.** Search of `_run_git_sterile`, session `_git`, intent `_git_path`,
and `additional_immutable_paths` found existing upgrade, session, intent and
dispatcher seams. Reuse guarded installation, sweep executable revalidation and
adapter shim, and existing caller test homes rather than a registry or framework.

### Documentation / doctrine surface

Update `docs/tool-usage.md`, `bootstrap/UPGRADE.md` and domain-local
`bootstrap/SAFETY.md` as behavior changes; retain governing AGENTS obligations
and mirror any necessary operative clarification in the shipped template.
No lifecycle change is authorized.

## Sequence

The existing installer, sweeps, source callers and test homes are available.
Estimate 5–10 workdays including reviews and verification; full migration,
per-member controls, native Windows and real old-Git availability are material
uncertainties. The recorded native Windows VM is available, but old-Git
availability and x64 compatibility on ARM64 remain unproven. First acquire
[MinGit 2.44.0 for Windows](https://github.com/git-for-windows/git/releases/tag/v2.44.0.windows.1)
into a disposable local VM directory, without system installation or PATH
changes. Verify `MinGit-2.44.0-64-bit.zip` SHA-256
`ed4e74e171c59c9c9d418743c7109aa595e0cc0d1c80cac574d69ed5e571ae59`,
then run its actual `--version` and establish compatibility below 2.45 before
claiming that capability. If this route fails, a High-tier owner selects a
credible alternative; real old-Git evidence remains required. Coordinate shared
session/caller edits with active owners; no unfinished plan is a prerequisite.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C0 | Resolve and document the three remaining boundary mechanisms; establish old-Git capability or a credible alternative | Usual and Security plan reviews; High-tier owner before Low execution | Concrete in-contract design choices and evidence route |
| C1 | Implement and deliver bounded helper and pre-import bindings | C0 | Mirrored helper, fixed-source pins and installed-layout controls |
| C2 | Migrate every inventoried ordinary reader and repair N1–N3 | C1 | Preserved capabilities, caller-specific failure handling and real-entry regressions |
| C3 | Complete iteration, adversarial and platform evidence, then code reviews and final verification | C1–C2; code reviews read iteration evidence; Boundary B follows review and fixes | Per-member mutation evidence, both reviews and final wide Boundary B |

## Acceptance criteria

**C0.** Before Low execution, a High-tier owner records concrete choices for
verified-buffer loading, enclosing-worktree exclusion before any probe and
Windows descendant cleanup, within the accepted contract. Establish the named
old-Git capability or a High-selected credible alternative; a mock or skipped
check is not evidence.

**C1.** Each trusted importer resolves only its fixed delivery root, rejects
missing, linked/reparse, nonregular, oversized or mismatched helper bytes and
executes the once-read verified buffer before any probe. Dispatcher binds all
six apparatus records; audit binds before injection; direct self-audit checks
the fixed record; external target and target CWD cannot supply helper authority.
Verified copies, pins, install/upgrade records and shim agree. Positive-control
execution markers prove missing records, tamper, links, cache substitution,
pin removal and audit-order mutations are detected. Jointly rewritten trusted
local code/records, malicious host Git and same-user races remain stated limits.

**C2.** The full source inventory uses validated off-tree host Git with
per-launch revalidation, closed environment and standard input (`DEVNULL`),
bounded noninteractive offline read forms and cleanup, including version/config,
filter-safe status and sweep
screen/shim; reduced sweep mode remains Git-free. Revision and supplied paths
are safe data. Markdown discovery enumerates and filters rather than treating
`*.md` as a literal selection; real link, snippet and delegated self-checks
find planted defects with and without the literal-wildcard decoy and refuse an
empty selection. Failure cannot appear clean or as measured zero: every source
policy row distinguishes completed empty from failed/absent/incomplete, with
fixed reasons and only labeled bounded non-secret data. N1 post-confirmation
startup failures, including later groups, refuse apply/finalize without byte
changes and advise stage; the intentional pre-confirmation no-Git case remains.
N2 linked-worktree and N3 version-only hang controls detect their mutations.

**C3.** Each inventoried real entry point and routing member has a separately
mutated control with a demonstrated positive tripwire. Exercise executable and
PATH/symlink substitution, inherited environment, hooks, filters, fsmonitor,
signatures, missing objects/remote helpers, options/paths, timeout, overflow,
descendant, closed-standard-input and cleanup cases through real entry points.
Complete these and affected iteration checks before code review; review fixes
precede final Boundary B. Record real native Windows and real old-Git
results; object reads retain the 2.45.0 floor and older discovery is permitted
only with demonstrated prevention. Both reviews and all mapped checks pass;
unknown, failed or missing required evidence keeps implementation open.

## Scope delta

**Scope delta**: preserved. No reader, check or accepted outcome is transferred
to architecture or deferred.

## Verification

Boundary A: before edits map imports, consumers and `python tools/test_tiers.py
for <changed paths>`; run its selected tests and standing prose gates. Extend
existing upgrade edit-check, session, interpreter binding, intent, security
stack, portable sweep, security verification, doc-drift, self-check, count and
reference parity homes, plus nearest existing gauge/report/tier owners. Use
actual shipped layouts and entry points; retain the source proposal's detailed
F1/F2, SR1–SR3 and N1–N3 controls. Run each routing mutation in an isolated
copy and summarize reproducible evidence, not a new ledger. Check synthetic
forged advice, controls and secrets at real output sinks. S2 mutations run in
C1–C3; S3 is triggered by these existing real-entry tests and adopter commands.

Complete mapped iteration and adversarial/platform evidence before code review,
so reviewers can read it; address review fixes before Boundary B.
Boundary C: independent code review falsifies the committed implementation;
separate Security Review is required. Boundary B: after reviews, run wide on a
clean unchanged final commit under canonical Python 3.13.x: all mapped
iteration and integration/workflow tests, installed public paths, required
security controls and standing claim, link, snippet and neutrality gates.
Record SHA/range, interpreter, pre/post state, commands and counts, elapsed,
non-pass dispositions, omissions and an evidence-qualified benefit-versus-effort
sentence. An expected reviewed engine AST mismatch remains unpassed pending a
separate Maintainer baseline operation; unexpected drift and integrity failures
remain implementation work. No certification, signing, ref movement or release
is authorized by this plan.

## Plan review -- Codex GPT-6.1 Terra (Medium) -- 2026-11-06

Reviewed commit: d55fe688659839bc49c4af060d216aff22aecf46

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised
**Verdict**: Revise before implementation.

**Foundations**

1. **Should this happen as framed?** The scope preserves the accepted migration, binding, N1–N3 and required evidence, but two sequencing prerequisites need resolution before its independent finish is credible -- plan Scope, Sequence and C3; source Decision `05ea5d90`.
2. **Best alternative.** Keep one helper and existing caller test homes, but identify the real evidence environments and place adversarial iteration before code review; this keeps the same outcomes without another framework -- plan Reuse and Verification; source proposal's delivery and test tables.
3. **What would show it wrong.** A real entry point surviving its separate routing mutation, a failed read reported clean, or inability to demonstrate the required real-platform controls would disprove delivery -- plan C2–C3 and source proposal Tests required.

**F1 -- blocking: real old-Git prerequisite is not established.** C3 requires real old-Git results, but Sequence lists only uncertainty; the source explicitly says those checks were not run and identifies no available installation or acquisition route. A prior native Windows VM is evidenced in `dev/plans/2026-11-05-architecture-and-reuse.md` under C1 native Windows capability; that is not old-Git evidence. Identify an available real old-Git environment or a credible, authorized way to obtain one, including constraints and uncertainty; keep missing evidence open. Do not substitute a mock or waive the Decision.

**F2 -- blocking: review precedes its evidence in the chunk gate.** C3 makes both code reviews a gate for completing adversarial and platform evidence, while Verification says code review falsifies the implementation and the governing rules require it to read iteration evidence. Arrange implementation and required iteration/adversarial evidence before code review, then review fixes and final Boundary B afterwards; preserve all controls.

**Advice:** Make closed standard input explicit for every read launch and test it at a real entry point. Existing upgrade `_run_git_sterile` uses `DEVNULL`; a noninteractive prompt setting alone does not establish that inherited input is unavailable.

**Coverage:** Read the committed plan, template, full operative source and Decisions, existing upgrade launcher, recorded Windows capability and reuse seams. The source tables remain normative for budgets, binding and caller policies. Did not run implementation tests, mutate members, establish old-Git availability, execute Windows, or assess the separate Security obligation. Over target to distinguish the two prerequisites and evidence. **Elapsed:** unknown; **tokens:** unknown.

## Plan review -- Codex GPT-6.1 Sol (High) -- 2026-11-06

Reviewed commit: a589416435e7f2d66b2e1e503a54c3bdc1a8a164

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: Revise before implementation.

**Foundations**

1. **Should this happen as framed?** Yes, retaining complete migration, pre-import binding, failure translations and separate anchored authority; sequencing and the remaining design owner need correction -- plan C1–C3; source Decision `05ea5d90`, delivery/binding and caller-policy tables.
2. **Best alternative.** Keep the small helper, existing delivery and test homes, resolving remaining security design within C1 before mechanical migration; this delivers the same outcomes without another framework -- plan Reuse; source Alternatives considered.
3. **What would show it wrong.** Run each member's real-entry mutation: any executed marker, surviving descendant, false-clean failure or lost capability disproves delivery; native Windows and below-floor Git must demonstrate their controls -- source Tests required; plan C3.

**SRP1 -- blocking: assign unfinished boundary design to High.** Scope requires High judgment only for questions “beyond the accepted contract.” The contract also leaves mechanism choices for verified-buffer loading, enclosing-worktree exclusion before probing, and bounded process/descendant cleanup on Windows. Accepting their outcomes does not settle those novel security choices. Name a High owner/gate to resolve them before Low execution, retaining the existing contract and required reviews. Medium planning of the accepted contract is not itself a floor violation. Close in Scope/Sequence; do not invent authority or remove outcomes.

Concur with ordinary F1/F2 and closed-stdin advice. The [official 2.44 release](https://github.com/git-for-windows/git/releases/tag/v2.44.0.windows.1) identifies `MinGit-2.44.0-64-bit.zip` and its SHA-256. Acquisition into a disposable VM directory, publisher-checksum verification and actual version/compatibility checks form a credible acquisition-first gate. Nothing was downloaded or executed; Windows ARM64 compatibility and actual old-Git controls remain unproven. Missing evidence keeps implementation open.

**Coverage:** Read the committed plan, template, full source/response/Decisions, upgrade launch and sweep validation seams, and recorded Windows capability; opened the official release. No implementation tests, mutations, package execution, native Windows, private data or trust operations. Claim check covered this isolated review candidate only. **Elapsed:** unknown; **tokens:** unknown.

## Plan review response -- Codex GPT-6.1 Terra (Medium) -- 2026-11-06

- **F1 accepted:** Sequence and C0 name an acquisition-first official MinGit
  route, checksum, actual version/compatibility check and High-owned fallback;
  no old-Git capability has yet been measured.
- **F2 accepted:** C3 and Verification place iteration and adversarial/platform
  evidence before code review and final Boundary B after review fixes.
- **Closed-input advice accepted:** C2 and C3 require `DEVNULL` and a real-entry
  control.
- **SRP1 accepted:** Scope, C0 and its criterion assign the three remaining
  in-contract security mechanisms to High before Low execution.

No accepted scope, evidence or review obligation is removed. **Elapsed**:
approximately 2 minutes. **Tokens**: unknown.

## C0 boundary design -- gpt-6.1-sol (High) -- 2026-11-06

**Role**: Strategy / in-contract mechanism design, not another plan review or
Security clearance. **Basis**: reviewed plan and response through `0e410866`,
accepted source `05ea5d90`; implementation started in `a83bc227`.
**Elapsed**: unknown. **Tokens**: unknown.

**C0 result**: the three reserved mechanisms are specified below, and real
old-Git execution is available. C1 may proceed after the coordinator's short
clone-freeze window for unrelated reviewed work; it does not wait for that
work's tests or completion. No source implementation occurred in C0. No
accepted reader, N1–N3 control or required check is removed.

### Verified source, fixed layouts and records

Keep one helper and its installed twin, not a package, registry or general
execution framework. Every first importer supplies a literal SHA-256 expected
value from reviewed canonical bytes. Source engine callers use their known
source root plus `templates/skills/_lib/git_read.py`; source template scripts
use that same fixed source-layout root; installed/self-hosted callers use
`tools/git_read.py` under their known delivery root. The session twins use
their fixed sibling. Layout is determined by the trusted caller's packaged
location, never target/CWD metadata, existence-based fallback or lockfile `src`.
Delegated consumers receive the bound helper, not a root that chooses code.

Use a small loader gate in those trusted first importers. Before opening,
`lstat` every absolute path component: reject links/reparse points, missing or
nondirectory parents and nonregular leaves. Bound the helper at 256 KiB. Open
once, with no-follow/nonblocking/binary flags where supplied by the platform;
compare descriptor identity with the checked leaf, read at most cap plus one,
and compare identity, mode, size, modification/change metadata before/after.
Do not compare access time. Recheck the component metadata and reject observed
changes. SHA-256 must equal the caller's literal pin. Execute only that buffer
with `compile(..., dont_inherit=True)` in a fresh module; never reopen its
source, load bytecode or reuse a `sys.modules` entry. A same-user replacement
race is not containment, but cannot substitute executed bytes for the verified
buffer. Reject errors with fixed caller-owned reasons, not exception payloads.

Bind the fixed installed helper record before direct content/sweep self-audit;
use the existing bounded JSON-encoded lockfile format, reject duplicate records,
and require its exact destination/hash rather than trusting adjacent digests.
Add the helper to the dispatcher's existing content apparatus (six members)
and audit's content apparatus before injection. Required records come only
from the trusted delivery root; missing/tampered/unbound records refuse or
degrade. They detect drift, not authenticity against a joint caller/helper/
lockfile rewrite. Do not invent another policy writer or lockfile schema.

Session's helper loading is lazy at ordinary Git entry points. Merely importing
its terminal encoder must remain self-contained when repin extracts the anchor's
single session file (`scripts/repin.py::load_encoder`). Privileged Git runners
continue using their own authority; they never import candidate helper/session
code. First-importer pin/parity tests must enumerate the actual complete set
from the implemented tree, not assume this design paragraph is that set.

**Falsifiers**: each first importer independently rejects missing record,
wrong pin, changed bytes, linked parent/leaf, oversized leaf and cached-module
substitution before an observable execution marker. Replace the path after
verification: the verified buffer alone executes. Launch from a distinct target
CWD containing matching-looking helpers/digests: none supplies authority.

### Exclusion before the first probe, executable identity and forms

Discover exclusion roots using filesystem metadata before executing even
`--version`. Include the supplied target's absolute lexical and resolved paths;
walk both ancestry chains, bounded at 512 components. Any `.git` entry counts
as a worktree marker without opening/following it, including a gitfile, link or
special file. Also conservatively recognize a bare-repository shape by its
HEAD/config/objects/refs metadata. Exclude each enclosing marker directory and
both its lexical/resolved spellings. Metadata errors, cycles or limits fail,
not a guess that the starting subfolder is the whole worktree. This preliminary
screen only denies execution locations; Git later supplies authoritative
worktree/common-directory information under the sterile launch contract.

Resolve operator PATH explicitly, without Windows implicit current-directory
search or accepting a selected empty/relative PATH entry. Select an absolute
regular executable; on Windows require a native executable, never a batch/shell
wrapper. Neither its lexical nor resolved location may enter any exclusion
root. Reuse sweep digest/revalidation semantics: bounded 512 MiB hash, identity
and path/content revalidation immediately before every launch. Cache a version
only against that validated executable identity; revalidate on cache hits.
Recompute exclusions for each target and reject newly observed location drift.
This authenticates no host binary, interpreter, DLL or trusted distribution.

Use source-owned read constructors, not arbitrary target-supplied argv. The
existing population needs version; config/root/git-admin discovery; index
listing; status; log/rev-list/describe; tree/blob/show; and diff/diff-index/
diff-tree forms. The implementation enumerates their actual fixed option sets
at the named callers. Unknown forms stop for High; no permissive passthrough.
Resolve supplied revisions with an option terminator to full object IDs before
composing ranges/blob expressions. Paths use literal pathspecs and `--` where
applicable. Markdown discovery specifically enumerates bounded `ls-files -z --`
and applies the fixed `.md` filter, retaining exclusions/present-file handling;
never turn the trusted wildcard into a literal selection. Preserve metacharacter
and option-looking filenames as data.

Before 2.45, only the measured version, metadata/config discovery and index-only
forms may run. Object-consuming forms require 2.45.0 and
`GIT_NO_LAZY_FETCH=1`; unknown versions fail them. Actual 2.44 controls must
prove the admitted old forms stay offline and that rejected object forms never
reach the hostile remote-helper control. Do not infer that from a mock.

**Falsifiers**: a fake Git in the enclosing repository above a nested start
must not run even for version; test gitfile/linked-worktree and bare controls,
relative/empty PATH, lexical/resolved links and executable swaps. Per-member
routing mutations must restore the unsafe route and trigger their planted
program, lost-capability or false-clean controls, including the wildcard decoy.

### Environment, filters, failures and the upgrade guard

Construct a closed host-minimum child environment; inherit no `GIT_*`, Python
import steering, pager/prompt, proxy or shell-startup settings. Supply the
existing noninteractive/offline settings, null global/system configuration,
no replacements/optional locks/lazy fetch, inert hooks/fsmonitor/signature
presentation, and no external diff/textconv. Set source-owned `GIT_ALLOW_PROTOCOL` to the empty string and
`GIT_PROTOCOL_FROM_USER=0`, alongside the protocol deny settings; the real old
and current Git controls must show even an explicit per-protocol allow cannot
launch a remote helper. Deny every transport, including remote helpers. Use an off-target neutral working
directory and explicit `-C`, not target CWD for interpreter/program startup.
Any workspace must be owned/off-target in lexical and resolved form; unavailable
safe workspace is failure. Do not add a host search or target-written shim.

For status, first obtain bounded include-expanded configuration as data.
Enumerate every clean/process/smudge/required filter-driver name and override
all those drivers to empty commands/`required=false` at command precedence
before status. Parse errors, oversized config or inability to neutralize a
name refuse; never pass unparsed config text as options. Retain sweep's stronger
existing include/origin/key screen, not just counted overrides. Conservative
dirty results after disabling filters remain dirty, with fixed explanation.

Return a small result distinguishing absent, failed/incomplete and completed
commands, including their exit code and requested output bytes. A selected
invalid/disappeared executable is failed, not absent. Failure output and Git
stderr never become result banners/remedies; omit them by default. Any retained
diagnostic field must be specifically allowlisted, non-secret, bounded, escaped
and labeled untrusted Git data. Requested successful data still follows its
consumer's established parsing/display policy; it is not diagnostic authority.
Apply the source proposal's entire caller-policy table, not one universal
exception or a successful empty/zero fallback.

For upgrade, keep worktree confirmation explicit. No repository or genuinely
absent Git before confirmation retains the intentional no-guard route. Once a
completed query confirms the worktree, every subsequent startup/config/HEAD/
index/diff/group failure raises `_EditCheckCannotTell`; never translate it to
`None` or discard earlier collisions. Apply and bare finalize preserve bytes;
stage advises, and existing explicit force remains caller-owned. Version-only
no-answer is failure, not absence. Preserve N2's real gitfile control and N3's
version-only hang with working later queries.

### Process bounds and Windows cleanup

Use the existing bounded subprocess/worker shapes rather than add a native
launcher dependency. Actual Git always has `DEVNULL` stdin. Drain stdout and
stderr concurrently into separately capped buffers; stop on timeout, cap,
decode/protocol failure or cancellation. Defaults: 10 seconds for ordinary
reads, caller-specific existing bounds where stricter; version 256 bytes,
config 256 KiB, roots 64 KiB, ordinary requested data 8 MiB, history at most
64 MiB, stderr 64 KiB. Existing larger legitimate requests need an explicit
bounded source-owned form, never silent truncation. Cleanup has a separate
2-second budget; no cleanup uncertainty reports completed success. Tests must
make output-reader and child/descendant cleanup observable.

On POSIX start a fresh session/process group, hold the leader unreaped until
group cleanup, then kill the owned group and wait/reap the leader before
returning, including normal completion. Use `waitid` with `WNOWAIT` to observe
exit without releasing the PID before `killpg`; do not poll/reap and then signal
a potentially reused group ID. The canonical host exposes those APIs. If a
platform lacks them, fail closed rather than introduce an unexamined fallback.
Reap only owned children; malicious host processes deliberately escaping the
owned group remain outside the trusted-host assumption.

On Windows reuse the `tools/code_map.py::_WindowsAPI.install_worker_job`
pattern, including its checked 64-bit layouts and system-DLL binding, in a
small private helper implementation. Do not import that large module at runtime.
A trusted isolated Python worker installs its own kill-on-close Job before
spawning Git; setup failure means no Git launch. Never put the main caller or
user desktop process in this Job. The parent supervises the worker and kills/
waits it on timeout, overflow, protocol failure or cancellation; closing the
worker's sole noninherited Job handle causes its ordinary descendants to die.
Keep the Job handle alive until worker exit. Do not permit breakaway, taskkill,
PID-name sweeps or a second unmanaged Git path.

The worker bootstrap receives only a bounded, parent-written request and the
already verified helper buffer, with the caller's literal expected pin carried
from the verified loader binding. It verifies the pin again before executing
that buffer in a fresh module. Use fixed `-I -S -B -c` bootstrap code and a
validated off-target `sys.executable`; no target imports, source reopen,
user-facing worker option or dynamic function selection. This request pipe is
not inherited input; close it after the bounded payload. The nested Git child
still gets `DEVNULL`. Bound/close all worker pipes and join their reader/writer
threads on every exit; no surviving reader is reported as a clean result.
The [Windows Job documentation](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
explains descendant inheritance and kill-on-last-close; the probe below tests
that pattern on the actual VM. The extra Windows Python startup cost is unmeasured. A direct creation-time
Job/handle launcher could remove it but adds a larger native process layer;
the existing worker substrate is the lower continuing-burden choice.

**Falsifiers**: positive EOF control for Git stdin; independent stdout/stderr
floods and version/config hangs; a live descendant retaining a pipe; cancellation
and forced worker-setup failure before Git execution; surviving child, open
pipe/thread/workspace or lost failure classification. Run native Windows
controls, not only simulated `os.name`. Hostile host code can escape via other
OS facilities; this is cleanup of the permitted process tree, not a sandbox.

### Sweeps and the Windows full-mode interpretation

The POSIX off-tree `git` shim must mediate each admitted adapter Git invocation
through these same forms and process bounds. Give it verified helper bytes and
fixed, validated Python/Git identities; expose only the shim directory on PATH,
never the original Git directory. Recheck the materialized shim and interpreter
before adapter execution. Unknown adapter forms/remote-capable calls refuse;
retain the existing admission/screen/reduced-mode controls. The existing
shebang route requires a kernel-usable fixed interpreter spelling; if unavailable,
report unsupported execution rather than add a shell or launcher dependency.
The admission controls must exercise this exact route, not a logging bypass.

**Delegated interpretation -- gpt-6.1-sol (High).** Preserve the established
Windows reduced route and native ordinary-reader migration; do not manufacture
Windows full-mode admission or use an unsafe batch shim. This preserves scope:
the module promises full mode only for the exact admitted triple, says prior
triples stay supported, and expressly limits established cross-platform
behavior to admission records (`dev/modules/portable-security-sweeps.md`, modes,
version cadence and Residuals). The current roster has no entries, and the
existing admission shim is POSIX-only. A callable matrix command promises an
honest evidence record/refusal, not that every platform can pass it. Thus no
currently established Windows full route or prior admitted artifact is removed.
This conclusion uses that explicit platform contract, not the empty roster alone.

Keep unsupported Windows full invocation/matrix fail-closed, without an admission
or a clean claim; reduced adapter execution remains Git-free and incomplete.
Ordinary runner discovery/screen reads still use the native helper; no Windows
reader is excused from C1–C3. A future proposed Windows full admission must first
supply a safe measured mediation mechanism and its existing required review;
this plan adds no admission, executable dependency or standing approval. Revisit
this interpretation if evidence identifies an already-established Windows full
route. Do not silently reclassify such a route as unsupported.

The alternatives are an unsafe shell shim (rejected), a new native launcher/
host dependency (material build, provenance and maintenance cost outside this
small helper, rejected), or retaining unmediated Git (violates the accepted
boundary, rejected). The chosen current-capability preservation adds zero new
human operations or recurring service/ledger. It does not concede an accepted
reader/check or waive native Windows evidence.

Temporary authority, Maintainer chat 2026-11-06, relayed by the coordinator:

> "I specifically authorize you to use a Sol agent to make decisions in my stead until I return (excepting anything that cannot be undone easily). Keep track of these decisions for review. Let the other agent know to ask you if they need it, and you will spawn the Sol review and track its outcome."

### Measured capability and Low handoff

On an isolated copy of `a83bc227`, the disposable Python 3.13.13 primitive
probe passed ten checks: verified-buffer/cache/post-read replacement controls,
tamper/link/oversize refusal, and enclosing-root discovery for directory,
gitfile, linked marker and bare shapes. This is limited POSIX primitive
evidence, not implementation/migration assurance. Probe:
`/private/tmp/cairn-safe-git-c0-probe.py`.

Native Python 3.13.17 ARM64 successfully ran the existing Windows worker Job
pattern: install before child, hold a handle proving the child alive, kill only
the disposable worker, then observe that child's handle signal within three
seconds. No file or private-profile access was needed. This supports the chosen
substrate, not every future cleanup path. Probe/log:
`/private/tmp/cairn-safe-git-c0-job-probe-launch.py` and
`/private/tmp/cairn-safe-git-c0-job-probe.log`.

Actual old Git is now available in the VM. The [official MinGit release](https://github.com/git-for-windows/git/releases/tag/v2.44.0.windows.1)
ZIP matched the plan's SHA-256; bounded extraction produced 342 entries/111,753,413 bytes from
45,462,622 compressed bytes. Its actual command reported
`git version 2.44.0.windows.1` under ARM64 Python 3.13.17. Retained executable:
`C:\cairn-git-c0-6d55e5e1dfe54ac4b881e98b296f4c15\mingit\cmd\git.exe`, SHA-256
`bd1bf0469426e2e67a27300176303b5e43e1dda81babc1c24c9c2ce627b97960`.
The owned temporary root passed local-NTFS/owner/ACL metadata guards; no host
installation, persistent PATH setting or real profile/config/source/ledger
read occurred. Acquisition/probe log:
`/private/tmp/cairn-safe-git-c0-oldgit.log`. Revalidate retained bytes before use.
Version/compatibility is measured; old-Git hostile-object controls remain owed.
If the workspace disappears or cannot be reused, repeat the pinned acquisition
in a fresh owned workspace; acquisition failure returns to High, not a mock.

Implementation handoff: first implement the cohesive buffer-bound helper and
its POSIX/Windows process paths, using those available binaries for focused
controls. Then wire the fixed source/installed bindings and six-member security
apparatus before migrating the complete normative inventory. Preserve each
caller's policies and N1–N3, then execute each member's real-entry and separate
mutation controls. Use existing owners, not new test files solely for routing.
Complete required iteration/adversarial/native/old-Git evidence before code
review; both reviews and final wide Boundary B remain due. Do not start source
edits until the coordinator confirms its clone snapshot is frozen; this is only
shared-tree serialization, not another plan prerequisite.

C0 ran no suite, caller migration, real ceremony, signing/ref operation, private
collection or release check. Future Windows/parser/shim/cleanup failures remain
implementation work and return to High when mechanism judgment is required.
A runtime or usability benefit is not measured; whether the complete change
justifies its remaining burden is unknown.

## Strategy mechanism Decision -- GPT-6.1 Sol (High) -- 2026-11-06 -- Darwin cleanup

**Conclusion:** replace the proposed bare Darwin `leader_exited + EPERM`
exception with a tiny owned-group membership proof. Preserve all accepted
cleanup/PID/timeout criteria; no scope is conceded. This is an author-side
mechanism Decision under temporary delegation, not Security Review or clearance.
Source authority is committed helper/tests `c8f96054`, not Low's unmirrored WIP.
The initial six-pass/four-fail record remains; no implementation suite ran here.

**Delegated authority:** Maintainer chat, 2026-11-06:

> I specifically authorize you to use a Sol agent to make decisions in my stead until I return (excepting anything that cannot be undone easily). Keep track of these decisions for review. Let the other agent know to ask you if they need it, and you will spawn the Sol review and track its outcome.

**Evidence and inference:** Apple XNU
[`kern_sig.c`](https://github.com/apple-oss-distributions/xnu/blob/f6217f891ac0bb64f3d375211650a4c1ff8ca1ea/bsd/kern/kern_sig.c),
`killpg1`, filters zombies and returns EPERM when it found no permitted live
recipient. `cansignal` also applies MAC policy before ordinary UID permission.
A same-session, same-credential child normally remains signalable, but exit of
its leader does not prove either emptiness or permission; MAC denial or changed
credentials can give the same error. `getpgid` on the zombie is not a descendant
absence test. The public source commit is not asserted to match this host's
kernel build. This explains Low's reported one-off observation without treating
that unsaved probe as repeatable evidence.

The selected fallback uses the system
[`proc_listpids`](https://github.com/apple-oss-distributions/xnu/blob/f6217f891ac0bb64f3d375211650a4c1ff8ca1ea/libsyscall/wrappers/libproc/libproc.c)
wrapper and its [kernel implementation](https://github.com/apple-oss-distributions/xnu/blob/f6217f891ac0bb64f3d375211650a4c1ff8ca1ea/bsd/kern/proc_info.c).
The group filter returns that PGID's live and zombie PIDs; policy failure returns
an error, not an authenticated empty list. The wrapper maps failure to zero, so
checking errno is mandatory. No process names, argv, credentials or unrelated
process list is needed.

**Concrete choice:** keep the fresh session/group and exact unreaped leader
reservation from C0. Only on Darwin, after `waitid(P_PID, owned_pid, WEXITED |
WNOHANG | WNOWAIT)` has positively identified that same exited leader, may a
SIGKILL `EPERM` enter this fallback. Bind the fixed system
`/usr/lib/libproc.dylib` through standard-library ctypes, with checked 4-byte
`c_int` and explicit `proc_listpids(uint32, uint32, void*, int) -> int` signature.
Query only `PROC_PGRP_ONLY=2` and the owned PGID into a fixed **two-PID** zeroed
buffer. Never use a host-wide selector or null-buffer sizing query. Clear errno
first. Accept only errno zero, returned bytes 0 or 4, and every returned PID
exactly equal to the retained exited leader. Reject negative/misaligned/other
sizes, an 8-byte saturated buffer, another PID, invalid data, unavailable symbol/
library or any error. Zero without a clean errno is failure. There is no fallback
to assuming permission from matching labels or UIDs.

No other member at that kernel snapshot means no remaining group member can
fork. An outside process cannot join the fresh session; the unreaped leader
reserves the identifier until all signalling/querying ends. Thus the empty-group
case needs no destructive signal and can proceed to bounded EOF draining and
leader reap. Other members, even zombies, keep the fallback conservative. Do not
reap/poll/wait before this check, signal a reused identifier, enumerate arbitrary
host groups or substitute direct leader kill for group cleanup. EPERM while
leader exit is unproved, on another platform, or with uncertain membership
remains failed cleanup. Existing successful SIGKILL and ESRCH handling remains;
other signal errors still fail. Keep the existing two-second cleanup budget and
make a missing/reaped child observation fail, never completed success.

**Cost and best alternative:** the bare EPERM exception is a few lines cheaper
but loses the accepted refusal on unexplained cleanup failure. Leaving the code
unchanged keeps ordinary Darwin reads unusable and the plan incomplete. A live
supervisor/sentinel could retain a signalable group member, but adds a process,
startup/IPC protocol and cleanup obligations to every read. The selected fixed
native query adds one small Darwin-only binding on the exceptional path, no
executable/dependency/framework or human operation, and checks the required fact
directly. It retains the existing malicious-host/escaping-process residual;
this is owned-group cleanup, not hostile-OS containment or a new sandbox.

**Measured capability:** saved probe
`/private/tmp/cairn-sg-darwin-owned-probe.py` and its `.log` used canonical Python
3.13.13 on Darwin 27.0.0, only two newly owned synthetic sessions/groups. With
only the WNOWAIT-held dead leader, the filtered query returned 4 bytes containing
that leader, errno zero; signal-zero and SIGKILL each returned EPERM. With an
exited leader plus a live same-group child, it returned 8 bytes (fallback refused)
and both signals succeeded. Both controls reached pipe EOF and reaped their
leaders only after signal/query handling. No unrelated host group was queried
or signalled. These are primitive controls, not proof of the integrated helper.

**Low execution and required falsifiers:** replace the held WIP with this guard,
mirror the actual helper pair, and extend the existing helper owner. Exercise
normal version/config/read completion on real Darwin; leader exit with a live
child holding a pipe and with a child closing pipes; timeout and each output
cap; and cancellation/BaseException cleanup. Inject EPERM after leader exit
while a real child remains and prove it does not become completed success.
Inject live-leader/non-Darwin EPERM, query errno failure (including zero return),
saturation, wrong PID, malformed size and missing API; preserve failed output.
Assert the leader remains unreaped through the last group signal/query. Kill and
reap only owned fixtures during test cleanup, including negative controls.

The committed capture's `finally` currently closes selector/pipes without
ensuring group cleanup on BaseException. This accepted cancellation obligation
remains implementation work in the same capture function; the narrow EPERM fix
must not hide it. Cleanup must occur before propagating cancellation, under the
existing bounds, and no uncertainty yields success. Run only affected iteration
controls before the owed independent reviews and final wide Boundary B. No
formal extra review pass, check waiver, private/trust operation or host setting
change is authorized. **Elapsed:** approximately 6 minutes through investigation
and native probe; finalization additional/unknown. **Tokens:** unknown.

Precommit claim check first flagged the two now-materialized helper paths still
marked proposed. Changing only that marker to “Implementation paths” cleared
the check; the path list, accepted scope and lifecycle status are unchanged.
