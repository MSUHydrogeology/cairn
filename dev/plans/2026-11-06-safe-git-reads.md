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

## Strategy integration Decision -- GPT-6.1 Sol (High) -- 2026-11-06 -- held config data

**Conclusion:** Safe-Git owns one fixed in-memory origin-config parser operation.
Meter must use it, not retain its competing subprocess loop. This explicitly
narrows this plan's universal DEVNULL restriction; it does not pretend a data
pipe is DEVNULL. Every existing ordinary read and version probe keeps DEVNULL.
No accepted caller outcome, offline restriction, cleanup check or model floor
is removed. This reversible local design Decision supplies no private consent,
activation, code review or Security clearance.

**Delegated authority:** Maintainer chat, 2026-11-06:

> I specifically authorize you to use a Sol agent to make decisions in my stead until I return (excepting anything that cannot be undone easily). Keep track of these decisions for review. Let the other agent know to ask you if they need it, and you will spawn the Sol review and track its outcome.

**Scope delta:** degraded -- the literal all-invocations-DEVNULL assurance is
narrowed for one fixed data-parser form. Ordinary reads keep closed input; no
caller outcome or privacy scope is removed. C2 and C0's “actual Git always has
DEVNULL stdin” now have exactly one exception: `read_origin_from_config` invokes
only the fixed no-includes query below, with at most 256 KiB of already-approved,
once-read config bytes, then EOF. No generic
stdin parameter is added to `run_git`, the shim or other public forms. This
widens the helper's data-input channel for an operation already present in
Meter's accepted POSIX design. Heavy assurance and both plans' owed code reviews
remain; no source implementation may call it until this fixed operation exists.
The [official Git 2.44 config manual](https://git-scm.com/docs/git-config/2.44.0)
specifies the file/input, includes and NUL-output controls; actual platform and
old-Git execution of this new shared route remains required, not inferred.

**Options and cost:** a private off-target file retains literal DEVNULL, but
puts raw configuration, potentially including private paths and credentials,
on disk. It adds owner/DACL-at-create, no-follow identity, launch-time filename
binding, crash residue and deletion obligations on both platforms. A new Python
config parser avoids that persistence and the pipe, but duplicates Git's
quoting/continuation/section grammar or refuses valid accepted configs. Leaving
association unavailable does not deliver Meter. The selected fixed buffer
operation preserves the existing transient-memory boundary and Git's parser;
its material cost is bounded concurrent input writing and corresponding worker
protocol tests. It loses only the literal all-invocations-DEVNULL property,
replacing it for this form with finite verified data and mandatory EOF. No new
human operation, executable dependency, telemetry or continuing ledger is added.

**Owned API:** add only `read_origin_from_config(config_bytes, *, target,
excluded_roots=(), executable=None, path_value=None, timeout=5.0) -> ReadResult`
to the mirrored helper. `target` is a configured approved project and serves
exclusion/context selection, never Git's working directory or permission to read
a path. Meter supplies the union of all approved source/project roots; derive
lexical/resolved enclosing-worktree exclusions for every member before any
version probe. Revalidate a supplied executable snapshot against that entire
set. Reuse existing fixed-source/installed-buffer binding, host executable and
version cache identity, sterile environment, transport deny, timeout and
POSIX/Darwin/Windows Job cleanup. Use the verified off-target neutral cwd and no
`-C` into the project. The buffer operation opens no target/config path itself.
Its argv/key/mode are source constants, never selected by bytes or callers.
The sole form is `config --file - --no-includes --null --get-regexp` with the
constant pattern `^(remote[.]origin[.]url|include[.].*|includeif[.].*|extensions[.]worktreeconfig)$`.
Privately parse all bounded NUL records as Git key/newline/value output before
returning anything. Refuse any include/includeIf or worktreeConfig key, even an
inactive declaration; never follow it or expose its path/value. Refuse unknown
keys or malformed framing. Only exactly one origin record may return its value
plus NUL; do not return the selected config record stream to callers. This
closes a real gap in the old origin-only query, which ignored possible overriding
sources. Meter must also metadata-refuse `.git/commondir` and
`.git/config.worktree`, retaining direct `.git` directory admission. No alternate
config file or global account file is read. The result proves admitted direct
origin identity under the closed configuration context, not every ambient user
override or effective transport URL. Unsupported declarations remain unknown
rather than acquiring additional private-file authority.

Accept only bytes within the 256-KiB cap and reject embedded NUL before spawn.
Cap successful output at 16 KiB and stderr at 4 KiB, with the existing five-second
Meter parser bound and two-second cleanup bound. Return only the established
absent/failed/completed distinction and successful requested stdout; discard
stderr/input/exception contents. Meter still requires zero exit, no parser
uncertainty and exactly one nonempty NUL-terminated UTF-8 remote (at most 2048
characters), then strips credentials/query/fragment using its existing policy
and compares with private approved remote. Absent, malformed, multiple or
unsupported output is unavailable, never a guessed remote or zero usage.

**Process input mechanism:** ordinary execution uses no input data and DEVNULL.
Only the fixed operation selects a private internal config-input slot. On POSIX
reuse the selector loop, adding bounded nonblocking writes alongside both output
readers. Close stdin immediately after the exact buffer is written; timeout,
cap, write/pipe failure or cancellation closes it and enters the same owned-group
cleanup, retaining the leader through final signalling/query. Broken/short writes
or an incomplete writer fail even if a child prints a plausible remote. A
finished write proves delivery to the pipe, not authenticated consumption by a
malicious host executable; successful complete parsing relies on the existing
trusted-Git assumption. No inherited input or interactive wait is permitted.

On Windows, the fixed verified-buffer worker request identifies this operation
and carries capped base64 data; its closed validator reconstructs the constant
argv and rejects data for every ordinary form. Do not permit an arbitrary argv
plus arbitrary input combination. Keep Job installation before Git. Drain both
outputs and write the bounded buffer concurrently; supervise any writer thread
under the same deadline and require it to finish after input close/child cleanup.
Bound request transmission too: no blocking parent write outside its deadline.
Oversized/malformed request, broken/unfinished writer, reader or descendant
cleanup is failure and worker/Job termination, never success. This extends the
existing worker, not a second runner or another input protocol. Bytes stay only
in already-trusted process memory/pipes; do not copy them into argv, environment,
logs, manifests, diagnostics or a temporary file. No secure-erasure guarantee
beyond the existing trusted-host memory/swap assumption is claimed.

**Execution ownership:** Safe-Git Low implements this operation and its focused
controls in its helper pair/owner, after the current Darwin correction and under
a coordinated source-file window. Meter Low then calls it from the existing
held-config association seam, removes the duplicate Git launch loop, and keeps
its native/retention/handoff work in Meter. Coordinate the call signature and
fixed importer pins together; do not duplicate an unverified loader. The Meter
plan receives a separate matching Decision. This is one shared boundary with
two consumers' evidence homes, not a new plan/framework.

**Required falsifiers:** ordinary forms still see EOF and cannot request data;
only the constant config operation consumes the exact buffer then EOF. Exercise
zero/multiple remotes, valid Git quoting/continuation, embedded NUL/oversize,
include/conditional-include decoys and include-path secrets, hooks/filter/pager/
remote-helper markers, source/executable exclusion and replacement, early-exit/
no-read children, input backpressure with simultaneous stdout/stderr floods,
request transmission timeout, cancellation and live descendants. Failed results
must contain no supplied bytes or stderr. Run the fixed form on real POSIX,
native Windows and the measured old-Git binary, plus Meter's synthetic real
refresh/rebuild and failed-association/no-prune paths. No actual private read or
activation is required or authorized for these controls. No new probe or suite
ran for this judgment; current committed source and primary documentation were
read. **Elapsed:** approximately 4 minutes through comparison; finalization
additional/unknown. **Tokens:** unknown.

## Authorized scope addition -- C2-R repeated-release compatibility -- Codex GPT-6.1 Sol (High) -- 2026-11-06

**Authority**: proposal Decision `903aaefc` accepting
`dev/proposals/2026-11-06-codex-repeated-claim-releases.md` after both reviews
and its response. **Scope delta**: add C2-R; preserve all original safe-Git
outcomes, criteria and checks. Earlier operative cells/reviews remain intact.
**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Scope and owner.** Existing C2 ownership repairs `tools/board.py` and its
identical `templates/skills/_lib/board.py` copy, extending the installed-entry
owner `bootstrap/tests/test_intents_tool.py`. Trusted intent loading and the
protected test owner overlap this plan's binding integration. No writer,
schema, dependency, runtime capability or human operation is added.

**Sequence.** Coordinate board/protected-test windows with Safe-Git Low; its
helper/test source window remains separate. Map actual consumers before edits,
implement within C2, then carry evidence into C3. The reader delta is small;
verification cost remains uncertain until mapping. No external plan dependency.

**Additional acceptance criteria.**

- **R1.** Strictly validate every record before reduction. Valid repeated
  releases, including differing optional annotations, leave a known claim
  closed. Invalid second releases, orphan/pre-claim releases and duplicate
  claims even after release still stop.
- **R2.** Preserve mirrored bytes, trusted-reader binding, root/path checks,
  identity/resolver stops and existing own-claim behavior. Another agent's
  active overlap still stops alongside repeats for a different closed ID.
  Claims and annotations remain coordination data, not authenticated approval.
- **R3.** Through installed NEXT, demonstrate failure specifically at the old
  duplicate-release guard before the fix and success afterward; first-release
  control passes. Retain neighboring refusals and exercise R1–R2 controls.
- **R4.** Map both readers, protected owner and actual consumers into iteration,
  independent usual/Security code reviews and final wide Boundary B. Record
  exact commits/outcomes/omissions, parity and binding evidence. Keep protected
  hash/roster obligations. Update changelog at its defined serialization point.

After synthetic checks, read the actual advisory without changing its log;
another legitimate stop is allowed, but normal repeats must not be classified
invalid. No pruning, rewriting or regeneration of actual records is authorized.
The accepted proposal's full verification obligations remain normative.

**Assurance retained.** Both upcoming code reviews explicitly cover C2-R. No
clearing plan review is added and no separately owed obligation is waived;
earlier plan reviews did not assess this addition. New boundaries require
reassessment. No private-data, trust-ref, baseline, certification, release or
publication authority is granted.

## C1 implementation security triage -- GPT-6.1 Sol (High) -- 2026-11-06

**Conclusion:** the six reported B102 findings are the accepted verified-buffer
mechanism, not execution of target-supplied Python. Use the existing scoped
`bootstrap/security_check.py` ALLOWLIST with source-specific rationales; keep
the scanner, severity, scan set, liveness and fail-closed rules unchanged.
This is author-side implementation judgment, not the independent Code Security
Review or clearance. No accepted check, scope or trust boundary is removed.

**Evidence:** read isolated committed `66405422`, the accepted proposal's
Delivery and Pre-import Binding, and this plan's C0. One targeted Bandit 1.9.4
scan under Python 3.13.13 reproduced exactly six MEDIUM B102 findings over the
six files below, exit 1, zero scan errors; no other MEDIUM/HIGH was reported in
that selection. This does not reproduce or replace the coordinator's reported
493-pass/1-skip/1-fail iteration; its original output was not persisted.

| Finding / function | Executed input and authority |
|---|---|
| `bootstrap/_scaffold/lockfile.py:126`, `_git_read_helper` | Fixed source-layout helper; literal caller SHA-256, bounded single descriptor read, link/reparse refusal and identity/component rechecks precede compilation. Only the freshly verified module is cached. |
| `scripts/content_scan_runner.py:164`, `_load_verified_git_read` | Fixed delivery-root tools helper; same literal-pin, bounded no-follow and revalidation gate. Fresh module, no import-cache reuse. |
| `templates/modules/team-gated/content_scan_runner.py:164`, same function | Byte-identical runner mechanism; the trusted packaged location determines the delivery root, not inspected target/CWD data. |
| `templates/skills/_lib/git_read.py:256`, `load_verified_module` | Explicit caller pin compared with the bounded `_checked_bytes` buffer; no linked/reparse components, reopening, bytecode or `sys.modules` reuse. At this commit its only callers are helper tests; its API does not authenticate a caller-supplied pin. |
| `templates/skills/_lib/meter.py:4362`, `_verified_git_helper` | Fixed source/tools layout and literal SAFE_GIT_SOURCE_SHA256; POSIX descriptor-relative no-follow reader or Windows bounded NTFS handle/identity/ACL stream. Execute raw bytes only after pin match; cache only that module. |
| `templates/skills/_lib/session.py:438`, `_load_git_read_helper` | Fixed sibling helper and literal pin; bounded single read, no-follow/reparse and descriptor/component revalidation. Only the verified fresh module enters its private cache. |

The helper also contains an **unreported** exec inside the Windows bootstrap
string. Its source/pin arrive through a private pipe from the trusted parent,
which supplies its already-bound buffer. The child digest checks transmission
consistency, not independent authenticity. Fixed isolated interpreter launch,
bounded request/reply, executable revalidation, and Job-before-Git constraints
remain required. No target JSON/config/command output becomes Python source.
Trusted caller/distribution, malicious-host and same-user-race limits remain;
mutable Python globals are not an adversarial in-process security boundary.

**Minimal execution instructions:**

1. Coordinate existing owners. Add exactly the six `(path, B102)` keys above
   to the single ALLOWLIST, with each rationale naming its function, fixed
   source/pin and verified-buffer-only constraint. Do not add tools-mirror keys
   absent from this scan, inline scanner suppressions, scan exclusions or a new
   exception framework. This classifies intentional accepted execution; it
   does not bless unverified code or waive a dependency/trust requirement.
2. In `bootstrap/tests/test_security_check.py`, replace the obsolete empty-table
   pin `test_the_shipped_allowlist_is_empty_after_the_b310_retirement` with an
   exact six-key/rationale assertion. In that existing test home, bound each
   allowlisted file's direct exec to the single named function above using its
   parsed source; an extra exec in an already-allowlisted file must fail this
   control. Preserve the existing live/absent/LOW/partial-report/error tests.
   The path/test-id table alone cannot distinguish two B102 sites in one file.
3. Meter's compile call omits C0's `dont_inherit=True`; add it in both meter
   mirrors under Meter's owner. Extend its existing integration owner with a
   compile-call observer through `_verified_git_helper`, asserting the admitted
   raw buffer and that keyword, while retaining mismatch/no-execution controls.
   No helper-byte/pin change is needed for this Meter-only correction.
4. Select affected checks with `tools/test_tiers.py for` for the actual changed
   paths. Include the security-lint gate, existing release-runner Bandit test
   and its liveness/error controls; invoke `security_check.run_bandit()` only,
   never the release command's full main. Preserve the owed each-importer
   tamper/link/oversize/cache/replacement controls, helper tests and Meter owner
   checks. A green static scan cannot supply their behavioral evidence.

The remaining cost is six maintained rationales and a small existing-owner
guard, with zero new human operations or recurring service/ledger. Removing the
verified-buffer execution would contradict accepted C1 or require a larger
loader redesign; merely ignoring the failed gate leaves implementation open.
Both formal code reviews, platform controls, mapped checks and final wide
Boundary B remain due. No implementation, pytest, mutation, Windows execution,
full scan/suite or trust operation ran in this triage. Isolated record checks
under Python 3.13.13: claim, one-file link/content and snippet checks pass;
neutrality reports zero failures/43 informational items (does not scan dev
plans), and the selector names zero test readers. Eight external links were
not probed. **Elapsed:** approximately 15 minutes. **Tokens:** unknown.

## C2 hook-index mechanism Decision -- GPT-6.1 Sol (High) -- 2026-11-06

**Conclusion:** preserve Git's partial-commit index as bounded data through one
fixed helper operation. Do not inherit its environment. Cached comparisons,
rename detection and committed-path comparison retain the accepted Git 2.45
floor. Add exactly one newly evidenced B102 key for the intent loader.
This is Strategy / author-side design and scoped security triage, not either
formal code review or Security clearance. **Source:** committed `9d89c446` and
`0387c030`, accepted proposal Decision `05ea5d90`, C0 and triage `b41b6dda`.

**Authority:** the Sol agent's reversible local mechanism Decision under the
Maintainer's temporary delegation, relayed by the coordinator from chat,
2026-11-06; it is not a claim that the Maintainer selected these details:

> "I specifically authorize you to use a Sol agent to make decisions in my stead until I return (excepting anything that cannot be undone easily). Keep track of these decisions for review. Let the other agent know to ask you if they need it, and you will spawn the Sol review and track its outcome."

Renewed in the same day's chat:

> "I'm good with you just continuing and we can review those later"

**Guarantee clarification:** the helper still strips every inherited `GIT_*`
field. The one narrow input exception is that intent may capture the hook's
`GIT_INDEX_FILE` once as an untrusted data locator. The helper validates and
snapshots its bytes, then supplies its own different `GIT_INDEX_FILE` pointing
only to the owned snapshot. No inherited value reaches the child environment.
No other command or caller gains alternate-index authority. No ordinary reader,
accepted check or trust boundary is removed.

**Options and costs:** retaining the current code is least involved but reads
the wrong staged set on partial commits. Passing the inherited field directly
would avoid a copy but would permit arbitrary paths and mutable input. Moving
the reads back into generated shell hooks would duplicate the boundary and
undo accepted C2. The selected fixed operation adds one bounded copy and
temporary directory per staged read, two intent call-site changes, helper
repins and existing-owner tests. Runtime cost is unmeasured. Noncanonical or
external custom indexes report unknown instead of reading the main index;
this loses their prior unrestricted environment-driven selection, which the
accepted closed-environment contract already excludes. It adds zero human
operations, services or recurring ledgers. I choose the snapshot because it
preserves the actual ordinary/partial/linked hook capability without granting
environment or executable authority. Further design outside these bounds
returns to High.

### Fixed operation and data guards for Low

Add one helper entry point, `read_hook_index(target, args, *, index_file=None)`,
returning the existing `ReadResult`. Admit exactly the two tuples already in
intent: `("diff", "--cached", "--name-only", "-z")` and
`("diff", "--cached", "--name-status", "-M", "-z")`. Reject every other tuple
before launching. An absent locator delegates to the ordinary read; a present
empty, malformed, unavailable or rejected locator fails. Never retry against
the main index. Keep `run_git` free of arbitrary environment/alternate-index
options. Both forms retain all existing argv, executable, transport, process,
stdin, timeout, output and diagnostic controls, including the 2.45 floor.

1. Confirm the target and obtain `--show-toplevel` and `--absolute-git-dir`
   through the verified helper with its normal closed environment. Parse one
   bounded absolute directory from each successful result; failure is unknown.
   Bind the root and administration-directory component identities. Ordinary
   `.git` directories and real linked-worktree gitfiles are distinct positive
   controls. Require an ordinary directory to be exactly `<root>/.git`.
   For a gitfile, validate its single bounded `gitdir:` pointer against the
   returned directory. For linked worktrees additionally validate the bounded
   `commondir` pointer and reciprocal `gitdir` back-pointer to this checkout's
   `.git` file, requiring the established `<common>/worktrees/<single-name>`
   shape. Reuse the metadata-validation design in trusted `_intent/shared.py`,
   without importing target code. A separate-admin or submodule gitfile with
   no `commondir` still requires the confirmed pointer/directory identities;
   do not misclassify it as a linked checkout or search for another repository.
   For a linked worktree, use its own returned administration
   directory, such as `<main>/.git/worktrees/<name>`, never the common directory
   or another checkout's index. These queries establish repository identity,
   not authority to load code there. Do not read or honor inherited `GIT_DIR`,
   `GIT_COMMON_DIR` or `GIT_WORK_TREE`.
2. Bound the locator at 64 KiB, reject NUL, and resolve relative values against
   the captured hook CWD before any neutral-directory switch. Require its
   normalized parent to equal the confirmed administration directory, in both
   lexical and resolved form using platform path comparison. Admit only
   `index`, `index.lock`, or `next-index-<positive decimal PID>.lock`; the PID
   is a filename component, not process identity or permission. Reject
   traversal outside that directory, linked/reparse components, special files,
   Windows alternate streams/device/UNC spellings, cross-worktree paths and
   external custom indexes. Do not search for an index when validation fails.
3. Reuse the helper's bounded no-follow reader: one regular-file descriptor,
   pre/open/post `(device, inode, mode, size, mtime_ns, ctime_ns)` agreement,
   component rechecks, cap-plus-one read and exact size agreement. Cap selected
   index bytes at 64 MiB; require a complete `DIRC` header with version 2, 3
   or 4, leaving full index validation to Git. Reject observed identity/content
   drift, malformed headers and read errors with fixed local reasons. Keep a
   digest of the admitted buffer. Recheck the root/admin/source components
   before launch and after completion; observed drift discards the result.
4. Materialize only that buffer into a newly created private temporary
   directory. Canonicalize the chosen temporary parent first, validate its
   components, and require the new directory's lexical and resolved locations
   outside every target/enclosing-worktree exclusion. Use mode 0700 and an
   exclusive regular no-follow mode-0600 snapshot file; apply the native
   Windows private-directory semantics of canonical Python 3.13. Refuse an
   unavailable safe workspace. Verify snapshot identity, size and digest
   after writing and immediately before/after execution. Supply only the
   source-owned absolute snapshot path in the otherwise unchanged closed
   child environment. Do not set `GIT_DIR`, `GIT_COMMON_DIR` or object paths.
5. On Windows add only a fixed `hook-index` worker operation. Its bounded
   request identifies the approved tuple, snapshot path, identities and digest;
   it carries no Python or dynamic function selection. The verified worker
   revalidates that snapshot/workspace and reconstructs the one environment
   addition before Git, inside the existing Job. Keep index bytes out of the
   2-MiB worker request; the private file is the data channel. Ordinary Git
   still receives `DEVNULL` input. No unmanaged child or alternate launch path.
6. Delete only owned snapshot/lock files and the owned directory on success,
   refusal, overflow, timeout or cancellation, after existing child/reader
   cleanup. Never follow a replacement link or recursively traverse an
   unexpected entry. Cleanup uncertainty is failed/unknown, never completed.
   Do not unlink Git's original `index`, lock or partial index.

The snapshot freezes the selected index bytes, not repository refs/objects or
all concurrent state. Split-index backing files remain ordinary target data
under the confirmed Git administration directory; normal time/output/process
bounds apply, rather than a claim that every object file is size-bounded.
Do not invent another repository or copy the whole object database. Same-user
replacement races and malicious-host behavior retain C0's stated limits.

### Caller routing, fixtures and required falsifiers

Capture the optional locator once in the Python pre-commit handler and pass
it to both staged-path and rename reads; keep the shell free of Git commands.
Ordinary root discovery and post-commit HEAD/diff-tree reads use `run_git`,
without this context. Preserve unavailable versus completed-empty results;
bad context warns unknown under existing allow policy, never a successful
empty set, and post-commit unknown never releases claims.

Implement first in the canonical helper and its byte-identical tools twin.
Extend `bootstrap/tests/security/test_git_read.py` for the fixed API, guard failures,
closed child environment, snapshot-only input, drift and cleanup. Coordinate
all helper owners, recompute the literal helper digest, and update every
current first-importer pin plus its twin in the same source checkpoint; derive
the actual set from the tree, including Meter's separately owned importer.
Do not leave stale callers between helper and pin commits. Then route both
intent conflict twins, updating existing installed fixtures to copy the exact
helper bytes. Commit each completed source checkpoint by explicit paths before
running its selected checks on a clean copy. These commits are implementation
evidence, not reviewed clearance or release authority.

Extend existing `test_intents_tool.py` actual generated-hook controls: ordinary
commit, initial commit, partial commit with `a` and unrelated staged `b`, real
linked-worktree partial commit, source-claim rename detection and split-index
repositories. Assert partial commits report `a` only, preserve staged `b`, and
do not block solely on another session's claim to excluded `b`. Both staged
and rename queries must use the same captured selection. Include paths with
spaces/metacharacters, relative hook locators, wrong-worktree/outside locators,
links/reparse parents/leaves, oversize/malformed input and missing/raced files.
Plant inert execution markers in inherited Git settings and a positive marker
control; none runs. Exercise real source and installed entry points, timeout,
overflow/cancellation and Windows Job/snapshot cleanup. A mutation dropping
the synthesized context must fail the existing partial-commit assertion;
forwarding the raw locator or permitting a different command must fail the
bounded-input controls. Native Windows evidence remains owed.

### Older Git classification, without conceding discovery

The [Git diff manual](https://git-scm.com/docs/git-diff) defines cached diff
against HEAD by default; [diff-tree](https://git-scm.com/docs/git-diff-tree)
compares commit/tree objects. Name-only output does not make their input
index-only. Rename detection may additionally consume blobs. Therefore neither
cached tuple nor diff-tree joins the older-Git exception. Missing HEAD on an
initial commit does not relax the command's classification. Below 2.45 these
operations fail before launch and intent reports unknown; the accepted
object-reading floor, not a newly invented compatibility loss, governs them.

Replace the command-name-only `_OLD_GIT_COMMANDS` bypass with approved old
forms. Keep metadata queries `rev-parse --show-toplevel`,
`--absolute-git-dir`, `--is-inside-work-tree`, and
`--path-format=absolute --git-common-dir`; keep existing bounded config-data
forms and literal-path index enumeration (`ls-files -z -- <paths>`,
`ls-files -z --cached --stage`, `ls-files -z -s -- <paths>`). Match the actual
fixed config option tuples already used by callers, not arbitrary config
subcommands or target options. Require the object floor for other rev-parse
forms, including revision peeling/verification and abbreviated object names,
and for object-bearing for-each-ref formats. There is no current ordinary
for-each-ref caller in the searched Python production population. Unknown
forms return to High instead of gaining an old-version bypass. This preserves
the accepted older metadata/config/index-listing capability, not an assertion
that entire subcommands are object-free.

Use the retained official MinGit 2.44 VM executable and revalidation route in
C0; no host install or PATH changes. Actual old-Git controls must prove
metadata/config/index enumeration success, rejection before launch of both
cached tuples, diff-tree and object-peeling forms, and no hostile remote-helper
execution. Current Git controls prove the object-consuming forms still work.
A version-spoofing shim alone cannot supply this evidence. No old-Git or
native Windows run occurred in this Strategy turn.

### One additional scanned execution site

The actual `scan_targets()` set contains only the template intent conflict
file, not its tools twin. A targeted Bandit 1.9.4 scan under Python 3.13.13
reported exactly one MEDIUM B102 there, line 275, with zero errors and no
other MEDIUM/HIGH finding in that selection. Add exactly
`("templates/modules/team-gated/_intent/conflict.py", "B102")` to the existing
table. Its rationale must name `_git_read`, its fixed packaged source/tools
layout, literal `_GIT_READ_SHA256`, bounded single-descriptor no-follow read,
component/identity rechecks, and execution of only the verified buffer with
`dont_inherit=True`. The pin at the inspected commit matches canonical helper
SHA-256 `123c308982a65f4bd5f5e13452c7ee871d09565fc445f2aac6e6f99d2a11047a`.
Target/CWD data selects neither helper code nor expected bytes.

Expand the existing six-key rationale assertion and direct-exec owner census
in `bootstrap/tests/test_security_check.py` to exactly seven keys/owners; the
new owner is `_git_read`. Retain the legacy pinned test node name and all
liveness/error/severity controls. Add no tools key, inline suppression, scan
exclusion or advance approval for future importers. A further exec in any
allowlisted file must still fail the census. Re-run only mapped checks and
the existing Bandit-only gate, not release main or tree certification.

**Measured limits:** one synthetic actual Git 2.53 partial hook using the
current helper completed root/admin discovery and incorrectly returned `a,b`
from the main index. Its locator was the expected `next-index-PID.lock`.
A separate tiny snapshot prototype returned only `a` and its modification
status in ordinary, real linked-worktree and split-index partial commits.
These three controls test the snapshot mechanism, not the future guards or
implementation. Probe files are `/private/tmp/cairn-intent-design-probe.py`
and `/private/tmp/cairn-intent-index-snapshot-probe.py`. The coordinator's
normal-path unavailable warning did not reproduce; its cause remains open,
not evidence of an older Git. Diagnose fixed `ReadResult.reason` and loader
failure separately without exposing free-form Git diagnostics or changing
unknown into empty. No pytest, suite, private input, host installation, trust
operation, signing, push, publication or release ran. Both code reviews,
per-member controls, mapped/native/old-Git checks and final wide Boundary B
remain owed. **Elapsed:** approximately 20 minutes. **Tokens:** unknown.

Record verification under Python 3.13.13: claim check, one-file link/content
checks and snippet check pass; neutrality reports zero failures and 43
informational items, and does not scan dev plans. The selector names zero test
readers for this plan. Ten external links were not probed by the document
gates; the Git manuals/source cited for this design were opened separately.
No Boundary B implementation result is asserted by these prose checks.

## Portable sweep migration disposition -- gpt-6.1-sol (High) -- 2026-11-06

**Role:** Strategy / security design. **Committed basis:** `f54a7875`.
This is a bounded reversible delegated Decision, not a review or security
clearance. Maintainer authority, chat 2026-11-06, quoted verbatim:

> I specifically authorize you to use a Sol agent to make decisions in my stead until I return (excepting anything that cannot be undone easily). Keep track of these decisions for review. Let the other agent know to ask you if they need it, and you will spawn the Sol review and track its outcome.

Renewed in chat, quoted verbatim:

> I'm good with you just continuing and we can review those later

**Decision:** reuse the helper's existing executable-selection token and raw
bounded read result. Preserve the sweep's source-origin screen; do not use
`read_origin_from_config`, which deliberately returns only one selected URL.
No new generic launch API, environment escape or object-floor exception.
This record remains available for Maintainer review with the other delegated
Decisions. It authorizes no private input, signing, ref movement, push or release.

The least involved credible option is this small adapter over existing APIs:
it adds caller glue and tests, with no new human operation or recurring
service. A dedicated public executable-path API could avoid the comparison
below but adds another supported interface and its platform/error contracts.
Keeping direct subprocess reads would lose the accepted common process bounds
and cannot satisfy C2. Recommendation: the existing-token adapter, because it
preserves both boundaries with the least continuing interface burden.

### Low-ready executable identity and fixed forms

1. After the sweep resolves its Git `Resolved`, call bound helper
   `select_git(target, path_value=os.path.dirname(git.lexical))` once. This
   searches only that one absolute directory for the platform's fixed Git leaf,
   and performs the helper's enclosing-worktree exclusions and bounded digest
   checks without executing Git. Catch `GitReadError` with a fixed local
   degraded reason. Missing token, or inequality of normalized absolute lexical
   paths, normalized resolved paths, or SHA-256 digest against `Resolved`,
   degrades; never fall back to ambient PATH. Retain the returned token intact:
   do not instantiate its private type, synthesize its fields or use its
   resolved parent as a replacement search directory.
2. Pass that exact token as `executable=` to every helper read in the sweep.
   Retain sweep `revalidate(git, target)` where its contract requires it;
   helper per-launch snapshot revalidation supplies the stronger identity,
   metadata and digest continuity. A changed PATH cannot select another Git.
   Adapter/shim work must keep C0's fixed Python/Git identity and verified-buffer
   route; the shim receives the same pinned lexical/resolved/digest identity,
   reselects only its fixed lexical directory and compares before helper use.
   Never expose the host Git directory alongside the shim on adapter PATH.
3. Replace common-directory discovery with the exact tuple
   `("rev-parse", "--path-format=absolute", "--git-common-dir")`.
   Replace the screen launch with exact
   `("config", "--list", "--local", "--includes", "--show-origin", "-z")`.
   Both use helper `run_git`, its closed environment and DEVNULL input, the
   existing 60-second screen timeout, and output caps no greater than the
   existing screen cap and helper configuration cap. Require completed/zero
   before parsing. Reject invalid UTF-8, empty, multi-line or nonabsolute common
   directory output; keep existing resolved origin-containment and inert-key
   checks over every origin/key pair. Preserve include expansion, linked
   worktree handling and the pre-adapter-execution screen order.
4. Add only that exact config tuple to `_old_form_allowed` in both helper
   copies. It is configuration data, not an object read. The metadata tuple is
   already present. Real MinGit 2.44 must demonstrate both succeed and that an
   outside-origin include and non-inert key still refuse. Do not substitute a
   key-only listing or relax all config/rev-parse forms.
5. Commit discovery remains exact
   `("rev-parse", "--verify", "-q", "HEAD^{commit}")`, with the existing
   timeout/output bounds. Completed exit 0 means commit, completed exit 1 means
   absent commit; any other state/exit is degraded, never not-applicable.
   This tuple remains object-floor protected: Git 2.44 must refuse before its
   execution and report incomplete/degraded history rather than a clean or
   empty history. Current Git must preserve unborn and detached-HEAD behavior.
   No safe alternate ref-file heuristic exists within this Decision.
6. Do not forward the sweep's environment argument into the helper or restore
   raw stderr/exception diagnostics. Translate helper absence/failure using
   fixed local reasons and existing sweep outcome classes. Keep raw config
   values inside the bounded parser; expose only existing bounded escaped
   key/origin facts, never values. Reduced adapter mode remains structurally
   Git-free; its ordinary discovery/screen reads are distinct from adapter
   execution, as C0 already specifies.

Extend existing `test_portable_security_sweeps.py` and `test_git_read.py` homes:
positive current/linked config, outside include behind a non-inert key,
identity mismatch, lexical symlink/PATH substitution, config hang/overflow,
closed stdin, unsupported/common-dir output, completed-empty versus failed
history, and exact older-form allow/refuse controls. Separate per-member
routing mutations must cover both source and template entry points, each
screen/discovery read and mediated shim. Native Windows and real old-Git
controls remain owed; the C0 Windows full-mode interpretation is unchanged.
Helper edits require coordinated canonical/twin bytes and all current literal
pins in one checkpoint, including separately owned importers. No new scan
exception for a future sweep loader is granted here: inspect its implemented
owner and actual finding when it exists.

### Exact current execution-site census

On an isolated archive of `f54a7875`, importing `bootstrap/security_check.py`
and walking every member returned by its actual `scan_targets()` found 13
files with one direct AST `exec` each. Seven have existing B102 entries:
lockfile, source/template content runner, template intent conflict, and
canonical helper/meter/session. Six current files are pending; all six have
exactly one owner, `_load_verified_git_read`:

- `scripts/link_check.py`
- `templates/modules/team-gated/link_check.py`
- `scripts/sync_doc_snippets.py`
- `templates/modules/team-gated/sync_doc_snippets.py`
- `scripts/measurements.py`
- `scripts/gen_legacy_code_review_passes.py`

Inspection finds these owners use a fixed packaged tools helper path, literal
`_GIT_READ_SHA256`, bounded one-descriptor no-follow reading, component and
identity rechecks, and execution of only the verified buffer using
`dont_inherit=True`, followed by source binding. Target/CWD data selects neither
code nor expected digest. Their B102 disposition is the same narrow reviewed
buffer-loader rationale as the existing content loader: add only these six
exact path/B102 keys, each naming that owner and these safeguards. Extend the
existing rationale assertion and owner census from seven to exactly thirteen;
retain its legacy node name and all error/severity/liveness controls. Tools
twins are outside this scanned population and gain no keys. Embedded worker
source is not another direct AST exec site in this census. A further actual
exec in any listed file must fail its owner census.

This is a source/AST classification, not an observed Bandit result. Before
accepting the six entries, run the existing Bandit-only gate and show each is a
live MEDIUM B102 with no unrelated MEDIUM/HIGH finding or scan error; a stale
entry must still fail. No inline suppression, blanket filename exception,
future-owner approval, main release ceremony or full suite is authorized.

**Coverage and limits:** inspected the committed helper, sweep, six pending
loaders, selector and existing exact rationale/census test, plus the prior C0
shim and platform disposition. Measured the thirteen-owner AST census under
Python 3.12.9 in an isolated archive; no production code changed and no Git
platform, adapter, Bandit or pytest execution occurred. Existing accepted
reviews, iteration, per-member controls and final wide Boundary B remain owed.
**Elapsed:** unknown. **Tokens:** unknown.

Scoped record checks under Python 3.13.13: claim, one-file link/content and
snippet gates pass; ten external links were not probed. Neutrality reports zero
failures and 43 informational items; it does not scan dev plans. The tier
selector selects zero tests for this plan. Corrected the prior record's helper
test-path typo to its existing security test home so its claim resolves; no
prior conclusion changed. No implementation Boundary B result is asserted.

## Existing old-Git metadata forms -- gpt-6.1-sol (High) -- 2026-11-06

**Role:** Strategy / bounded execution Decision, not another review.
**Committed basis:** `95f64e6a`; reported failure at `5b2bc401` remains failed
until its fix and exact rerun. Maintainer delegated authority in chat,
2026-11-06, verbatim:

> I specifically authorize you to use a Sol agent to make decisions in my stead until I return (excepting anything that cannot be undone easily). Keep track of these decisions for review. Let the other agent know to ask you if they need it, and you will spawn the Sol review and track its outcome.

Renewal, verbatim:

> I'm good with you just continuing and we can review those later

**Decision:** complete the existing metadata exception with three exact tuples
already used by inventoried callers. Add these to `_old_form_allowed` in both
helper copies, not a subcommand-wide bypass:

- `("config", "-z", "--get-regexp", r"core\.filemode|core\.autocrlf|core\.eol|promisor|partialclone")`
- `("rev-parse", "--verify", "-q", "HEAD")`
- `("rev-parse", "--verify", "HEAD")`

The config tuple is upgrade `_edit_check_prelude`'s existing settings and
partial-clone discovery. The next tuple is that same prelude's HEAD reference
question. The third is source/template intent `_head_commit_via_git`'s existing
HEAD reference question. These fixed unpeeled HEAD forms resolve a reference
identifier; they do not establish that its object exists or has commit type.
Do not reinterpret their completed result as such proof or alter callers'
existing subsequent object-read failure policy. Arbitrary revisions, suffixes,
peeling, path expressions, abbreviation, other option combinations and generic
verification stay outside the exception.

This corrects the earlier design's overbroad treatment of every verification
form as object-consuming. In Git 2.44's [rev-parse source](https://github.com/git/git/blob/v2.44.0/builtin/rev-parse.c),
flags start at zero and the normal verification path prints the resolved OID.
The [object-name source](https://github.com/git/git/blob/v2.44.0/object-name.c)
resolves literal HEAD through `get_oid_basic` and `repo_dwim_ref`, without
peeling; its short-name fallback rejects HEAD's nonhex characters before object
disambiguation. Parent/typed expressions instead enter object-reading paths.
This is a source-based classification, not a new real Git 2.44 execution result.
`HEAD^{commit}`, cached diff, diff-tree, cat-file and all other object reads
retain the 2.45 floor. The sweep's exact origin-bearing local config form and
its outside-origin/inert-key screen remain unchanged; this upgrade query does
not replace or bypass that screen or the bounded origin-buffer parser.

**Batch inventory:** searched ordinary source and shipped Python readers for
config, rev-parse, ls-files and helper call sites. Existing metadata forms are
root/admin/worktree/common-dir discovery, the two full config listings and the
index-list tuples already in the helper. The three additions above are the
remaining actual fixed config/reference forms found. Install uses the existing
root/admin forms; lockfile uses abbreviated HEAD or typed revision resolution;
session uses root/admin and index listing; link/snippet/content/self-checks use
root/index discovery; measurements, gauge, tier selection and legacy reads
consume history/tree/blob/diff data. Those object paths gain no exception.
Meter's origin parsing uses the separately bounded config-buffer operation,
not arbitrary repository config execution. Privileged runners and intentional
hooks-path installation remain outside this ordinary-reader change. Unknown
future forms return to High.

The least involved credible option is the three-tuple completion plus existing
helper/caller tests. Keeping the current refusal loses promised older-Git
metadata discovery and leaves the observed check failed. Replacing caller HEAD
queries with another command would add parsing and migration work without
improving this fixed data-only boundary. Recommendation: exact tuple completion;
no human operation or new recurring component is added.

**Low execution:** extend the existing fixed-form helper test with these three
allowed tuples; replace its now-incorrect rejected literal HEAD case with
`HEAD^{commit}` and retain all other rejected object/unknown forms. Keep the
reported upgrade test's `(True, False, True)` assertion unchanged, and retain
partial-clone refusal before any later index/object query. Add near-miss regex,
HEAD suffix and option mutations to the existing test home. Recompute canonical
helper/twin bytes and every current importer pin together through existing
coordination. Rerun the exact failed upgrade node and affected mapped checks;
record each result without relabeling the earlier failure. Required real MinGit
2.44 evidence must additionally show these fixed config/ref forms succeed for
ordinary/unborn/detached cases, partial settings still refuse the upgrade
prelude, missing HEAD objects cannot cause fetch or a hostile marker, and
peeling/object forms refuse before execution. No simulated version alone closes
that requirement. Existing reviews and final Boundary B remain owed.

**Coverage:** read current committed helper, upgrade prelude and launcher,
intent HEAD caller, fixed-form test, inventoried source call sites and upstream
Git 2.44 implementations. No runtime implementation, adapter/platform execution,
pytest, certification, private inputs, refs or publication occurred.
**Elapsed:** unknown. **Tokens:** unknown.

Record checks under Python 3.13.13: claim/link/content/snippet pass; neutrality
zero failures and 43 informational items (dev plans outside its coverage);
selector zero test files. Twelve external links were not probed by prose gates;
the two upstream source files were opened separately. These are record checks,
not implementation verification.

## Implemented sweep loader classification -- gpt-6.1-sol (High) -- 2026-11-06

**Role:** Strategy / implementation-bound execution-site classification, not a
formal review pass. **Committed basis:** `78ed24df` (source `87f78e96`).
The existing C0 verified-buffer design and delegated authority govern this
classification; no new trust mechanism or process exception is introduced.

On a separate archive of that commit under Python 3.13.13, the actual
`scan_targets()` AST census has fifteen files with one direct exec each and
thirteen existing B102 keys. The two new files are byte-identical and each
has exactly one direct exec, line 140, owned by `_load_verified_git_read`:

- `("scripts/run_portable_security_sweeps.py", "B102")`
- `("templates/modules/team-gated/run_portable_security_sweeps.py", "B102")`

**Low-ready disposition:** add exactly those two keys. For each use this exact
rationale, also pinned by the existing rationale assertion:

> `_load_verified_git_read` executes only the bounded single-descriptor helper buffer from its fixed packaged source/tools root after literal `_GIT_READ_SHA256` comparison and component/identity rechecks; `dont_inherit=True` and source binding precede Git use, and target/CWD data selects neither code nor expected pin.

Both owners derive the delivery root from the caller's packaged location,
resolve only its `tools/git_read.py`, reject links/reparse components,
nonregular/oversized leaves and identity changes, read at most 256 KiB plus one
from one descriptor, compare size and metadata before/after, check the literal
digest, and execute only that buffer in a fresh module without reopening source
or consulting the module cache. Canonical helper digest measured on the archive:
`5e077f2e579f5f7febcda21148270bbcb1ae45a9262a5e76accbbee228f5214d`;
both new literal pins match it. The fixed trusted record must still be enforced
where the existing installed-layout contract requires it; loader classification
alone does not establish every routing/binding control.

Extend the exact rationale and owner tables from thirteen to fifteen; both new
owner values are `_load_verified_git_read`. Preserve the legacy node name,
severity threshold, missing-target/scan-error refusal and live-entry retirement
checks. A second direct exec, moved owner, changed rationale, extra key or stale
finding must fail. Retain positive marker controls for digest/pin/record tamper,
linked or substituted source and cache substitution in each real entry point;
this source inspection does not replace those accepted controls. The coordinator
reports an actual Bandit 1.9.4 run on clean `78ed24df`, Python 3.13.13, with
exactly these two unallowlisted MEDIUM B102 findings and no other finding/error;
that is reported evidence, not a run by this author. Rerun the existing
Bandit-only gate after the table change and affected mapped tests. No inline,
file-wide, prospective or other-owner allowance is granted.

### Intermittent executable digest refusal remains open

The reported combined run's `executable-changed-during-read` is separate from
the earlier sweep fixture count failure. Passing isolated retries do not
explain or close it. `_checked_digest` compares `_stat_key` for every ancestor,
including directory size/mtime/ctime, in addition to executable descriptor
metadata. A sibling creation can therefore refuse an unchanged executable.

A deterministic isolated Python 3.13.13 probe against archived `78ed24df`
wrapped its `os.read`: after the first executable read it created one unrelated
sibling in the fixture's parent, then called the original reader thereafter.
It returned exactly `executable-changed-during-read`; the executable's full
`_stat_key` remained unchanged and its SHA-256 stayed
`9b2ea417ea6adc0d6d81b786284236c6dfa5c977c6bacf91d5f83a986c0f4d9d`.
This proves that source condition can produce the reported diagnostic; it does
not prove that shared pytest ancestor activity caused the actual failed run.
The full-chain comparison is currently required by the recorded design, so no
runtime guard weakening or automatic retry is authorized by this finding.

Smallest next causal check: retain this sibling-mutation control in the
existing helper test home, with an unchanged-file positive control and a
file-replacement negative control. For the failing exact test, instrument only
the isolated test copy to capture before/after component stat tuples and name
which compared field changed when refusal occurs; keep diagnostics off product
sinks and use synthetic paths only. Run that test in the original combined
selection as well as its unique temporary directory. A captured ancestor-only
change explains that occurrence; unexplained file/identity/digest changes stay
implementation work. If eliminating benign ancestor-timestamp refusals is
needed, return the concrete identity-versus-directory-metadata distinction to
High for an in-contract design repair and its mutation controls before changing
guards. No conclusion that retries alone establish integrity is accepted.

**Coverage:** inspected both committed loaders, helper digest guard and exact
allowlist/owner test, measured actual scan population, twin parity and helper
pin equality, and ran only the synthetic sibling-change probe. No pytest,
Bandit, adapter/native run, private data, refs, signing or full suite ran here.
Ordinary and Security code reviews, required platform/per-member controls and
final Boundary B remain owed. **Elapsed:** unknown. **Tokens:** unknown.

Record gates under Python 3.13.13: claim/link/content/snippet pass; neutrality
zero failures and 43 informational items, with dev plans outside its coverage;
selector zero test files. Twelve external links were not probed. These record
gates do not close the implementation diagnostic or any C3 evidence.

## Executable directory comparison repair -- gpt-6.1-sol (High) -- 2026-11-06

**Role:** Strategy / reversible in-contract design Decision, not another formal
review. **Committed basis:** `62d08bb8` causal controls and current helper.
Maintainer delegation, chat 2026-11-06, verbatim:

> I specifically authorize you to use a Sol agent to make decisions in my stead until I return (excepting anything that cannot be undone easily). Keep track of these decisions for review. Let the other agent know to ask you if they need it, and you will spawn the Sol review and track its outcome.

Renewal, verbatim:

> I'm good with you just continuing and we can review those later

**Decision / grouped Scope delta:** allow ordinary directory entry churn during
host executable verification, while retaining sampled directory identity,
permissions/ownership/reparse metadata and the executable's full metadata and
content verification. This explicitly replaces C0's full size/time comparison
for real directory components only, in `_checked_digest` and
`_snapshot_executable`. It concedes one conservative signal: a transient
ancestor rename, permission/ownership change or reparse change that returns to
the same final sampled state may leave only ctime/mtime evidence, now ignored.
The source proposal S5 already declares same-user filesystem races outside
containment; this Decision accepts that specific lost signal within that
residual, rather than claiming identical detection. No accepted offline,
off-target, pinned-code, bounded-process, per-launch identity, object-floor or
failure-classification outcome is removed. No other file reader, importer,
index guard, signature function or trust ceremony gains this exception.

The least involved credible option is to keep conservative refusals and provide
a fixed explanation: no guard implementation changes, but normal sibling
activity in a common temporary/PATH ancestor can still make a valid read fail;
users must isolate activity or rerun, and recurring false unknowns remain.
The proposed executable-only signature repair adds one small private comparison
function and deterministic existing-home tests, removing those measured false
refusals at the cost of the transient-change signal above. Directory-descriptor
or native-handle traversal with broader race containment adds substantially more
platform implementation and review work and still needs a precisely stated race
model; it is unnecessary for the accepted host-trust boundary. None adds a
human ceremony or recurring service. Recommendation: the narrow signature
repair, because persistent identity/security changes still refuse and the
executable remains fully verified, while unrelated sibling churn stops breaking
ordinary reads. Required heavy reviews remain before activation; no release,
private access, signing, push or broader race-containment claim is authorized.

### Exact Low-ready change

Keep `_stat_key` and the `_Snapshot` fields and return contracts unchanged.
Add one private helper in the canonical helper and byte-identical tools twin:
`_executable_component_key(info: os.stat_result) -> tuple[int, ...]`.
Its security suffix, in this order, is integer `st_uid`, `st_gid`,
`st_file_attributes`, `st_reparse_tag`, using zero for platform-unavailable
attributes. For `stat.S_ISDIR(info.st_mode)` only, return
`(st_dev, st_ino, st_mode)` followed by that suffix. For every other component,
including lexical symlinks, return the full existing six-field `_stat_key(info)`
followed by that suffix. Do not follow a link to decide whether its own lstat
record is a directory. Directory type/mode, device/inode, owner/group and
Windows attribute/reparse changes therefore still compare unequal. This does
not assert ACL attestation; the existing reader does not capture ACLs.

Use the new key only for before/after chain tuple comparisons in
`_checked_digest` and `_snapshot_executable`. Keep their chain length/order,
`_lstat_chain` shape/link/reparse rules, lexical/resolved comparison and
containment unchanged. Keep the executable descriptor's full `_stat_key`
comparison, regular-file requirement, no-follow open, size/byte cap, exact byte
count and digest unchanged. The non-directory leaf chain key additionally
retains all old fields. Keep fresh snapshot/digest revalidation at every
launch, including version/config/shim launches; no cache, retry or fallback
hides a refusal. Do not globally replace `_stat_key`, change `_checked_bytes`,
hook-index component signatures, first-importer loaders or their trusted pin
rules. Update all current literal pins together after coordinated helper bytes.

### Causal and security controls

In the existing helper test home, revise the committed unrelated-sibling test
to require successful digest and executable selection, with full leaf metadata
and SHA equality despite changed directory size/timestamps. Use deterministic
mutation during the existing read seam; no timing sleeps. Retain unchanged and
file-replacement controls. Exercise both affected chain comparisons, so a fix
only to `_checked_digest` still fails the lexical snapshot control.

Add targeted persistent ancestor mode-change, directory-replacement and
lexical symlink-retarget controls that must refuse; restore test-owned fixtures
only after the assertion. Cover changed owner/group, Windows attributes and
reparse tag through constructed stat results in the private-key test where
native privileges cannot safely change them. Assert all security suffix fields
participate and that directory size/mtime/ctime alone do not; assert those same
fields still participate for non-directories. Retain actual native reparse and
per-launch executable/PATH substitution controls. An executable byte, identity,
mode or timestamp change must still refuse, even when directory churn occurs
at the same time. Do not claim transient-change-and-revert detection, which
this Decision explicitly concedes.

Run affected mapped checks and the existing combined selection that exposed
the diagnostic, plus the exact test in its unique temporary directory. Report
the original historical occurrence as unexplained unless captured evidence
identifies its changed component; the proven sibling mechanism is repaired,
not retroactively asserted as that event's cause. Independent ordinary and
Security code reviews assess the narrowed comparison and named lost signal;
required native/per-member evidence and final Boundary B remain owed.

**Evidence/limits:** inspected source proposal S5, C0's metadata contract,
current `_stat_key`, `_lstat_chain`, `_checked_digest`, `_snapshot_executable`
and committed causal controls. This turn changed no runtime source and ran no
pytest, adapter/native program, private input, full suite or trust operation.
**Elapsed:** unknown. **Tokens:** unknown.

Record gates under Python 3.13.13: claim/link/content/snippet pass; neutrality
zero failures and 43 informational items (dev plans outside coverage); selector
zero test files. Twelve external links were not probed. These prose checks
establish no implementation, platform or Boundary B result.

## Native Windows executable mode comparison -- gpt-6.1-sol (High) -- 2026-11-08

**Role:** Strategy / in-contract mechanism repair, not a formal review pass.
**Basis:** current helper SHA-256
`d53b4099ed8e31cc5bb5db9dd16d6f89d2982b81da58b445a6b2fcd0d03698c4`,
C0 and executable-directory Decision `34427405`.

**Native facts:** the coordinator's bounded diagnostic under Windows ARM64
Python 3.13.17 sampled retained MinGit 2.44 and synthetic `.exe` and `.bin`
files three times each. Every path/descriptor field matched except `.exe`
`st_mode`: path execute bits were 0111, descriptor execute bits zero, and all
remaining mode bits matched. Device/inode were nonzero and equal; size,
mtime/ctime, owner/group, Windows attributes/reparse tag, SHA and byte counts
matched. Path/path and descriptor/descriptor samples were stable. All `.bin`
fields matched. Both existing helper operations refused with
`executable-identity-changed`. This author read the retained JSON diagnostic;
the coordinator ran the VM. Direct MinGit version execution is established;
helper-mediated old-Git behavior checks remain **unpassed**.

CPython 3.13.17's [path stat implementation](https://github.com/python/cpython/blob/v3.13.17/Modules/posixmodule.c)
adds execute bits from executable filename extensions in
`update_st_mode_from_path`. Its [descriptor implementation](https://github.com/python/cpython/blob/v3.13.17/Python/fileutils.c)
uses handle attributes without that filename adjustment. These are synthetic
mode representations, not a measured file-identity change. The documentation's
zero-identity warning for cached `DirEntry.stat` does not describe these
`os.lstat`/`os.fstat` observations. No identity field may be dropped.

**Disposition:** repair only the executable's path-to-open-descriptor comparison
in `_checked_digest`, using one private
`_executable_open_matches(path_info, descriptor_info) -> bool` in both helper
copies. Obtain each full regular-file `_executable_component_key` (six stat
fields plus owner/group/Windows attributes/reparse tag). Require exact equality
normally. Only on `os.name == "nt"`, with both records regular, admit this exact
representation difference: descriptor execute bits are zero and path mode is
exactly `descriptor_mode | 0o111`. For that case alone compare every other key
field exactly, replacing only the path key's mode slot with descriptor mode.
Do not mask both modes generally, accept partial execute-bit differences,
normalize POSIX values, ignore device/inode or alter read/write/type bits.
Keep the existing fixed failure reason and all other refusal paths.

Use this comparator only in `_checked_digest`'s initial path/opened check.
Keep within-descriptor full `_stat_key` equality, within-path full component
keys, directory handling, no-follow/reparse/regular checks, bounds, byte counts,
digest and final path identity check unchanged. The cross-source comparator
also compares the existing security suffix rather than discarding it.
Do not globally change `_stat_key` or `_executable_component_key`, and do not
change `_checked_bytes`, importer gates, index signatures or the worker schema.

**Consumer audit:** `_checked_digest` continues returning the descriptor's
unmodified six-field key. `_snapshot_executable` therefore stores descriptor
mode in `_Snapshot.mode`; its final path comparison uses only device/inode,
which match natively. `_snapshot_still_matches` resnapshots through the same
descriptor route, so snapshot equality and `_version_key` remain exact.
The Windows request serializes that unchanged snapshot, and the worker uses
the same resnapshot check. The worker's own Python `.exe` selection also uses
this corrected path/open comparison. `_checked_bytes` callers read fixed `.py`
helper source, pointer/config data and extensionless index snapshots; their
cross-source checks have no observed executable-extension mismatch and gain no
exception. No current consumer requires a path-mode snapshot or global mode
normalization. A different native field mismatch returns to High.

The least involved alternative is continued refusal with a fixed unsupported
reason; that leaves required native helper functionality undelivered. A native
handle metadata layer adds code and platform contracts without improving this
already matching identity evidence. The single comparison adapter is the
recommended smallest repair: it preserves security-relevant equality and adds
no human operation or recurring component. It removes no accepted assurance
outcome or directory-race safeguard and needs no further Scope concession.

**Low checks:** add exact comparator cases in the existing helper test home:
native difference accepted; POSIX same difference rejected; exact ordinary
matches accepted; partial/reversed execute differences, type/read/write bits,
each identity/size/time/security-suffix difference rejected. Preserve actual
within-path and within-descriptor mode-mutation refusal and all replacement,
reparse, digest and per-launch controls. Run the native diagnostic again, then
actual helper version and retained MinGit behavior controls; worker resnapshot
and Python-executable startup must succeed without losing mutation detection.
Coordinate helper/twin and every current importer pin in the same checkpoint
(the coordinator inventories nineteen). Run mapped checks; no mock closes
native/old-Git evidence. Ordinary/Security reviews and final Boundary B remain
owed. No runtime implementation, VM execution, private input, signing, refs,
push or release occurred in this design turn. **Elapsed:** unknown.
**Tokens:** unknown.

Record gates under Python 3.13.13: claim/link/content/snippet pass; neutrality
zero failures and 43 informational items (dev plans outside coverage); selector
zero tests. Fourteen external links were not probed by prose gates; the two
CPython source files were opened separately. No implementation result is claimed.

### Permanent regression home for the Windows mode repair

Extend existing
`bootstrap/tests/security/test_git_read.py::test_executable_digest_accepts_an_unchanged_component_chain`
without renaming or parameterizing its node ID. Add owned regular `.exe` and
`.bin` data fixtures; do not execute them. On real Windows use native
`os.lstat`/`os.open`/`os.fstat` to assert the measured synthesized-execute-bit
relationship for `.exe` and exact equality for `.bin`, then assert
`_snapshot_executable` and `_snapshot_still_matches` succeed for both, preserving
descriptor mode and expected digest. On POSIX both fixtures retain exact
path/descriptor equality and successful snapshots. Close every descriptor.
For the existing `select_git` assertion use the platform's actual fixed leaf
(`git.exe` on Windows, `git` elsewhere); this test does not execute its synthetic
payload, so it needs no Windows shell or fake-Git launcher exception.

This keeps one existing cross-platform, unconditionally asserted node: there
is no added Windows-only node, new skip, or native-policy classification.
The full same-field inequality controls specified above stay in the existing
helper test home. Actual native execution of this node is required evidence;
mocked `os.name` alone cannot close it. Retained MinGit version/behavior controls
separately test real executable/process operation. This clarification adds no
runtime scope and was authored by gpt-6.1-sol (High), 2026-11-08.

Clarification gates under Python 3.13.13: claim/link/content/snippet pass;
fourteen external links not probed. The same-turn neutrality and zero-reader
selection above remain applicable; neither includes dev-plan implementation
coverage. **Elapsed:** unknown. **Tokens:** unknown.

## Confirmed Windows file-time semantics -- gpt-6.1-sol (High) -- 2026-11-08

**Role:** Strategy / in-contract mechanism repair, not a review pass.
**Basis:** `bc95b816`, exact helper `4fba189e` and the coordinator's native
Windows ARM64 Python 3.13.17 time diagnostic, read by this author.

**Measured cause:** three samples each of retained Git, Python, the pinned
helper and an owned `.py` before/after rewriting prove path `st_ctime_ns` is
native CreationTime, while descriptor `st_ctime_ns` is native ChangeTime.
Path/descriptor birth times both equal CreationTime exactly. Python, the helper
and rewritten fixture have different creation/change times. Git's happen to
coincide. The owned rewrite retained identity/creation/birth/path-ctime but
changed descriptor-ctime/native ChangeTime/LastWriteTime. Other sampled fields
and each within-source read were stable. This is not precision loss.

CPython 3.13.17's [path implementation](https://github.com/python/cpython/blob/v3.13.17/Modules/posixmodule.c)
copies birth time into ctime for compatibility; its descriptor conversion does
not make that copy. The [fileutils implementation](https://github.com/python/cpython/blob/v3.13.17/Python/fileutils.c)
assigns CreationTime to birthtime and ChangeTime to ctime.
[Microsoft FILE_BASIC_INFO](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_basic_info)
distinguishes metadata ChangeTime from data LastWriteTime. Thus comparing path
ctime to descriptor ctime asks unlike questions. This corrects the previous
claim that `.py` bindings have no cross-source mismatch; no global timestamp
relaxation or tolerance follows.

### Exact semantic adapter

Add private `_private_file_open_matches(path_info, descriptor_info, *, executable=False)`
in the mirrored helper. Both records must be regular. Start with the full
regular-file `_executable_component_key` for each (six original fields plus
owner/group/Windows attributes/reparse tag). On non-Windows require exact keys.
On Windows require integer `st_birthtime_ns` on both records, and require
`path_info.st_ctime_ns == path_info.st_birthtime_ns == descriptor_info.st_birthtime_ns`.
Missing fields or a failed equality refuse. For this cross-source comparison
only, put descriptor birthtime into a copy of the descriptor key's ctime slot
(index 5); never mutate the record or the retained descriptor key.

For `executable=True` only, additionally permit the already approved exact
execute-bit representation difference (descriptor execute bits zero and path
mode exactly descriptor mode OR 0111). No other mode difference is allowed.
Then compare every key field exactly. Retain `_private_executable_open_matches`
as a thin wrapper using `executable=True`, preserving its existing owner/tests;
`_checked_bytes` uses the new function with its default false. These are two
fixed source-owned call forms, not a target-selectable policy or general runner.

For the seventeen pre-import `.py` loaders below, helper code is not yet
available. Keep their small local gate, full `key` and verified-buffer design.
Add owner/group/file-attributes/reparse-tag fields to the existing local key
(using integer zero for platform-absent fields). Construct a separate initial
`opened_compare_key` from that key. Only on Windows, enforce the same exact
birth-field requirements/equalities above, and replace only its ctime slot with
descriptor birthtime. Compare this temporary key to `key(before)`. No execute
normalization is permitted in these `.py` loaders. Never change `key(opened)`,
`key(after)` or path component keys to use birthtime globally. A local expression
or local function may implement this fixed comparison; no unverified import,
new executable loader, module cache or source reopen is introduced.

### Complete affected-site inventory

The initial path/open-descriptor comparisons change at these seventeen actual
first-importer owners, plus `_checked_bytes` and the existing executable-open
comparison in each helper twin:

- `bootstrap/_scaffold/lockfile.py` -- `_git_read_helper`.
- `scripts/content_scan_runner.py`, `scripts/link_check.py`,
  `scripts/sync_doc_snippets.py`, `scripts/run_portable_security_sweeps.py`,
  `scripts/measurements.py`, `scripts/gen_legacy_code_review_passes.py`,
  `tools/gauge.py`, `tools/test_tiers.py` -- `_load_verified_git_read`.
- `templates/modules/team-gated/content_scan_runner.py`,
  `templates/modules/team-gated/link_check.py`,
  `templates/modules/team-gated/sync_doc_snippets.py`,
  `templates/modules/team-gated/run_portable_security_sweeps.py` --
  `_load_verified_git_read`.
- `tools/session.py`, `templates/skills/_lib/session.py` -- `_load_git_read_helper`.
- `tools/_intent/conflict.py`,
  `templates/modules/team-gated/_intent/conflict.py` -- `_git_read`.

Meter's `tools/meter.py` and `templates/skills/_lib/meter.py` are the remaining
two literal-pin owners: their Windows first binding uses the existing native
NT handle reader, not this path/fstat comparison. Repin them with the other
seventeen; do not alter their consent/native filesystem semantics here.
This is nineteen importer pins and two helper copies, with the existing parity
and fixture rules. Keep all direct exec owners/sites and the fifteen-key B102
census unchanged; correcting the pre-exec metadata comparison adds no B102
exception, weakens no liveness/severity rule and preserves each rationale.

### Retained checks and downstream contracts

Every descriptor-before/descriptor-after comparison retains actual ChangeTime
via full `st_ctime_ns`, plus mode, size and mtime; path-before/path-after and
component comparisons retain their full existing keys and reparse checks.
Descriptor identity, creation equality, ownership/attributes, no-follow opening,
bounds, exact byte count, digest/pin checks and failure policy remain enforced.
No rounding, time tolerance, ctime removal or fallback is authorized.

`_checked_digest` and `_checked_bytes` still return the descriptor's unchanged
six-field identity key; their returned path chains remain path signatures.
Executable `_Snapshot.ctime_ns` therefore remains actual descriptor ChangeTime
and is revalidated across every launch, cache lookup and worker serialization.
The interpreter follows that same route. `_pointer_value` ignores the descriptor
identity after its guarded read. `_index_locator_bytes` and
`_hook_index_source_matches` compare returned path chains to path chains and
content digests; do not compare those chains to descriptor times. Hook snapshot
materialization and `_hook_snapshot_matches` currently store/compare their
path-derived time fields to path fields, with separate descriptor identity and
content checks. Those are same-source comparisons: keep their schema, index
selection, lock/workspace cleanup and signatures unchanged. They gain no
ctime exemption. Pre-import gates likewise keep actual descriptor ChangeTime
through each read even though path compatibility ctime denotes creation.

The least involved credible option is the semantic adapter in the existing
readers; continued refusal cannot deliver required Windows binding/worker
functionality. A separate native metadata layer adds interfaces and platform
work to recover values Python already exposes exactly. Recommendation: compare
like timestamps only at crossing points, retaining stronger descriptor change
checks everywhere else. No human operation or recurring component is added,
no accepted outcome is conceded, and the previous directory-race Scope delta
is unchanged. A different Python timestamp contract fails closed and returns
to High rather than silently adopting this exception.

### Required regression and native evidence

Extend existing helper tests with a rewritten owned `.py` whose creation and
change times differ: native path ctime/birth and descriptor birth agree,
descriptor ctime differs, `_checked_bytes` and pinned `load_verified_module`
succeed. Retain actual descriptor ChangeTime mutation during reading as a
refusal, and each identity/type/creation/security-field mismatch as a refusal.
Host causal cases cover Windows semantic mapping and POSIX exact equality;
missing or unequal birth fields must fail. The executable test must additionally
exercise the real installed Python snapshot/resnapshot, not just fresh `.exe`
data. Keep the permanent existing cross-platform node IDs when extending these
controls; any genuinely new Windows-only node needs separate native-policy
classification before it can be skipped on other hosts.

Exercise each of the seventeen real first bindings with rewritten, correctly
pinned helper bytes in an isolated installed/source fixture under native
Windows. Pin mismatch and helper mutation during read must still prevent the
execution marker. Run actual worker-backed version and retained MinGit forms
only after coherent helper/pin commits; neither direct Git nor mock birthtimes
close those obligations. Use existing test homes, mapped checks and per-member
mutation controls; ordinary/Security reviews and final Boundary B remain owed.
This author ran no runtime implementation, VM command, pytest, private input,
ref operation, signing, push or release in this turn. **Elapsed:** unknown.
**Tokens:** unknown.

Record gates under Python 3.13.13: claim/link/content/snippet pass; neutrality
zero failures and 43 informational items (dev plans outside coverage); selector
zero tests. Seventeen external links were not probed by prose gates; cited
CPython and Microsoft source documentation was opened separately. These record
gates establish no native behavior or implementation verification result.

## Trusted caller aliases and two linked-parent controls -- gpt-6.1-sol (High) -- 2026-11-08

**Role:** Strategy / C0 interpretation and concrete fixture design, not another
formal review. **Committed evidence:** `2dd63aea` callers and controls.

**Conclusion:** an alias that relocates the selected trusted caller together
with its helper is permitted by the existing physical delivery-root meaning.
It is not a successful linked-helper refusal. The two skipped refusal controls
remain unpassed until repaired as specified below; no acceptance criterion or
per-member check is waived.

Source proposal “Delivery and Pre-import Binding”, SR1, fixes helper authority
to the trusted caller's “known packaged location”, forbids target/CWD/search
selection, and expressly says caller authenticity comes from the trusted
checkout/distribution assumption. C0 “Verified source, fixed layouts and
records” likewise determines layout from the trusted caller's packaged location,
not target metadata, and verifies every component of the resulting helper path.
Neither passage authenticates the spelling used to invoke that caller or pins
its checkout to an operator-supplied lexical prefix. The two committed tools
use `Path(__file__).resolve().parent.parent` before constructing the fixed tools
helper path. A complete caller/helper reached through a pre-existing tools
alias consequently belongs to the resolved physical delivery root. Its regular
helper still needs the caller's literal expected digest and all read guards.
Replacing caller/pin/checkout authority is outside this contract; an external
scan target remains unable to supply helper authority merely by choosing CWD
or providing matching-looking adjacent records.

The `2dd63aea` alias positives correctly include both caller and valid pinned
helper at that physical root. Their helper markers demonstrate alias acceptance,
not failure of a linked component in an already selected delivery root. The
previous fixture lacking the caller failed before binding and supplies no
refusal credit. Conversely, a link inserted into the helper path after the
trusted root has been captured must still refuse. The helper leaf-link control
also remains applicable independently of caller aliases.

**Smallest complete repair:** keep both alias positives. Replace only the
unresolved parent-link negative setup for `tools/test_tiers.py` and
`tools/gauge.py` with a deterministic post-root-capture mutation. Retain the
existing refusal node IDs and assertions; remove their unresolved skips only
when the corrected controls pass. Script-based readers retain their existing
independent linked-helper-parent setup.

Use the existing trusted Python test driver, leaving the copied caller source
unchanged except its existing synthetic helper pin. Before running the actual
CLI through its existing `runpy` entry, precompute the canonical absolute helper
leaf and save the real `os.lstat`. Wrap that call only in the test process:
on the first lstat of exactly that helper leaf, move the fixture's entire tools
directory into its owned outside directory and replace the original tools path
with a directory link. Then delegate to the saved real lstat; all later calls
also delegate unchanged. Resolve the expected path before installing the
wrapper, avoiding recursive realpath/lstat interception. Do not trigger on a
caller path or tools-directory lookup: those also occur during caller root
resolution and would reproduce the alias-positive setup instead.

That leaf lookup happens in the helper gate after root capture and initial
parent checks. The remaining component recheck must discover the substituted
parent and fail with `git-read-binding-failed` before helper execution. Record
a separate owned mutation-ran marker and assert it exists, as well as nonzero
exit, fixed binding refusal, absent helper execution/CWD/cache markers. A
missing caller, failed driver or untriggered mutation is a failed fixture, not
passing assurance. Restore the test wrapper in its driver cleanup; mutate and
clean only owned fixture paths. Retain the ordinary positive to prove the
helper execution marker is live, and run the two corrected negatives together
with both alias positives. This is one Medium-tier correction after High's
clarification, respecting the exhausted same-tier fixture retry budget.

Rejecting all aliases of the caller itself would add a new caller-spelling
restriction, affect ordinary alias-based invocation and require its own
mechanism/compatibility contract. It adds no helper-byte authentication beyond
the existing fixed caller pin. The least involved credible option is the
existing physical-root rule plus the stage-correct negatives above. Recommendation:
keep that meaning and complete the owed checks. No promised helper-link refusal,
security safeguard, human ceremony or recurring component is removed or added;
no Scope concession is needed. No runtime or test edits, pytest, native run,
private input, refs, signing, push or release occurred in this author turn.
**Elapsed:** unknown. **Tokens:** unknown.

Record gates under Python 3.13.13: claim/link/content/snippet pass; neutrality
zero failures and 43 informational items (dev plans outside coverage); selector
zero tests. Seventeen external links were not probed. These are prose checks,
not credit for either unresolved refusal node or implementation verification.


## Implementation evidence -- Codex coordinator -- 2026-11-08

On the frozen clean source `5ced3b3e`, the retained-conftest Windows selection
under Miniconda Python 3.13.17 reported **58 passed, one failed, no skips in
9.33 seconds**. All 52 first-importer nodes passed, including separate positive,
wrong-pin and same-bytes-during-read controls for each of the 17 inventoried
members. The three helper file-time/executable controls and three content-runner
checks also passed. The latter exercise clean output, sorted Git paths with
duplicate findings, and ambient Git-directory exclusion for issue #55. Meter's
synthetic refresh alone failed with `git_untrusted`; its native helper-source
boundary remains under diagnosis. This is not a whole-plan or whole-Windows pass.

The actual retained MinGit 2.44.0 Windows executable, hash verified against the
C0 acquisition record, passed the current `ec471c34` helper probe under the same
Python. Nine permitted metadata/config/index forms completed; unborn and
detached HEAD results retained their meanings, and literal wildcard roots were
exact. Five disallowed object/revision forms refused before launch. With a loose
HEAD object removed from a synthetic partial clone, the metadata lookup did not
restore it or invoke the local remote helper. The explicit-allow control first
proved that helper could create its marker. The first attempt failed that
control because its program was absent from the deliberately restricted PATH;
using its absolute system path corrected the fixture. No production relaxation
was made. This does not cover linked config, outside-origin includes, or the
remaining worker and caller matrix.

No full suite, private profile, persistent VM setting, trust operation or push
was used. Remaining per-member/platform evidence, mapped iteration, both code
reviews and final wide verification still keep this plan open. **Elapsed:**
approximately 15 minutes including preparation and diagnostics; native pytest
9.33 seconds above. **Tokens:** unknown.

## Implementation handoff -- Codex coordinator -- 2026-11-08

The mapped iteration on frozen `28f79683`, Python 3.13.13, selected 105 files
in three batches: 6,650 passed, 116 failed and 16 skipped. Targeted corrections
and environment-enabled retries resolved the 114 unexpected failures; the two
expected AST-baseline checks remain unpassed for the separate release operation.
This is qualified iteration evidence, not one green run or final Boundary B.
The final caller matrix, both code reviews and final verification remain due.

The native worker controls found a real cancellation defect: after a ready
worker received an injected `KeyboardInterrupt` in its supervising caller, the
worker was still alive when cancellation propagated. The test killed and waited
for its owned worker and joined its three pipe threads afterward. Ordinary EOF,
config-buffer, overflow, hang, early-exit, pipe-holding timeout and actual Job API
setup-refusal controls passed under Windows Python 3.13.17. Quiet-descendant
cleanup remains unmeasured: the direct fixture still holds its original stdout
pipe after parent exit, including after fixture correction `95e0f912`. This
fixture failure does not establish a production defect.

GPT-6.1 Sol's cancellation design assigns cleanup to one `try/finally` covering
everything after successful worker creation, including partial thread startup.
Use one monotonic cleanup deadline; kill and wait for the owned worker, then
join only started owned pipe threads within the remaining budget. Close pipes
only after their users finish. Preserve payload and overflow checks, report
ordinary incomplete cleanup as `worker-incomplete`, and re-raise cancellation
after cleanup. Do not add process-name killing, put the caller into the Job,
or treat cleanup uncertainty as success. The runtime correction and affected
native controls remain implementation work; no fix is claimed here.

The VM window is released. Cairn's broad host checks are held while the other
project runs its coordinated slow tests and benchmark; implementation and short
focused checks can continue. **Elapsed:** unknown. **Tokens:** unknown.

## Native worker policy and verification -- Codex GPT-6 Luna (Low) -- 2026-11-08

High Sol's source classification at `4f7be4f6` assigns exactly twelve
`test_git_read.py` native worker nodes to Windows-only policy: they require
Windows PE execution, kernel Job, handle or event behavior. This attribution is
an in-contract source classification, not a formal Security Review. The
manifest keeps every previous row, adds only those twelve exact IDs, and its
ordered digest and Windows count guard are updated together.

On Windows ARM64 with Python 3.13.17, the twelve exact native nodes passed.
On the canonical host with Python 3.13.13, the focused helper controls passed
11 tests with 38 deselected. The host run does not establish native worker
behavior. This is bounded policy and worker evidence, not a whole-plan or final
wide verification. **Elapsed:** unknown. **Tokens:** unknown.

## Affected iteration handoff -- Codex coordinator -- 2026-11-08

The clean `4f7be4f6` copy under Python 3.13.13 completed its mapped 69-file
selection in two batches: 5,488 passed, one failed, 28 skipped, no errors;
1,565.554 seconds total wall time, with clean pre/post state. Skips were seven
Windows token/NTFS cases, twelve native worker cases, eight junction cases and
one Windows drive-normalization case. These are opposite-host omissions, not
new native passes. This is affected iteration, not certification or Boundary B.

The sole failure was the portable sweep's stale self-hosted install hash after
the helper-pin update. Existing scoped finalize produced exactly one hash
change, committed as `f66306f9`; that exact failed node passed on its committed
bytes under Python 3.13.13 (one passed, 0.18 seconds). The 69 files were not
repeated. The two policy controls separately passed after the exact twelve-ID
classification at `807eb72a`. Remaining accepted routing evidence, code and
Security Reviews, and final wide verification remain due. Slow owners are on
the existing board consolidation list. **Elapsed:** about 26 minutes for the
mapped run; **tokens:** unknown.

## Coordinator record verification -- Codex coordinator -- 2026-11-08

The grouped board and two implementation-handoff updates at `58ef686e` passed
their mapped 21 reader files under Python 3.13.13: 1,650 passed, one Windows
drive-normalization skip, no failures or errors, 338.732 seconds. The bounded
selection ran once after the final prose-data commit in a separately bound
clone with clean pre/post state. Claim, link, content, snippet, neutrality and
board gates passed on identical candidate bytes. This covers those three
record files only, not the whole Git or Meter implementation; their code
reviews and wide final checks remain due. All other tests were omitted.
The three-minute integration diagnostic was missed, and the newly measured
install-time onboarding owner is on the existing consolidation list. This
append records that completed result; it changes no runtime, rule or accepted
criterion. **Elapsed:** approximately six minutes; **tokens:** unknown.

## C3 evidence mapping -- GPT-6.1 Terra Medium (Coordinator) -- 2026-11-08

The 52 native first-binding passes above cover each of the 17 named physical owners: lockfile; source and template content runners, link checkers, snippet checkers and sweeps; measurements, legacy report, gauge and tier selector; and both session and intent-conflict copies. They prove the tested pinned-buffer, wrong-pin and read-mutation behaviors, not a separate unsafe-Git routing mutation at each real consumer. The existing native worker and real MinGit results likewise do not close that caller matrix.

Real-entry binding positives and separate perturbations already have homes in `test_doc_drift_tools.py` (four link/snippet copies), `test_verify_counts.py`, `test_replacement_tools.py`, `integration/test_gauge.py`, `contract/test_test_tiers.py`, `test_session_kernel.py` and `test_intents_tool.py`. The installed audit in `test_security_stack.py::test_real_audit_binds_helper_before_injection` proves live helper/injection markers and separate record and binding refusals. These are useful binding evidence; a changed helper or wrong pin is not itself a mutation that routes Git around the boundary. Per-route unsafe-routing tripwires and their results have not been located for the full inventory. Use existing owners for lockfile and delegated upgrade/install; both content runners, dispatcher and audit; both sweeps and shim; four link/snippet copies and delegated self-check; measurements, legacy, gauge and tier; both sessions; and both intent-conflict copies and generated pre/post hooks. A distinct real route needs its own weakened-route positive tripwire and safe-route result; group only routes shown to share the same binding and launch path.

The existing edit-check post-confirmation and later-group controls, content failed-read control, intent unknown/no-release controls, measurement failed-count control and legacy failed-tree control provide partial caller-policy evidence. The accepted empty-success versus failed/absent/incomplete distinction still needs a complete evidence mapping across every policy row. The link and snippet literal-decoy tests call module `main` and plant a finding, but the accepted separate real CLI controls with and without the decoy and their literal-selection mutant are not established by those nodes alone. The existing slow-version fixture hangs all invocations; N3 still needs a version-only hang with functional later questions and an ignore-version mutant. N2 needs the real linked-worktree edit and `lexists`-to-`is_dir` mutant in the edit-check home; generic linked-worktree tests are not that evidence. The four additional functional-plan importers remain owned by that plan.

This is read-only evidence mapping, not a code or Security Review. No tests, mutation replays or platform runs were performed in this step. Missing functional evidence remains implementation work; both reviews and final wide Boundary B remain due. **Elapsed:** unknown. **Tokens:** unknown.

## C3 N2, N3 and discovery controls -- GPT-6 Luna (Implementation, Low) -- 2026-11-08

At `59289bc8`, three existing test homes add the requested public controls; no production reader changed. The upgrade test uses real linked-worktree `.git` files for apply, bare finalize and stage. Apply and finalize refuse the planted tracked edits without changing the protected bytes (including staged manifest contents); stage advises. In an isolated scaffold source copy, replacing the `.git` `lexists` check with `is_dir` made apply succeed and overwrite `AGENTS.md`.

The N3 stand-in hangs only when the command is `--version`; its logged metadata and index questions still return valid results through the same executable. The public apply path returns cannot-tell and preserves the edit and stage when the version probe times out. Mapping the no-answer sentinel to the absent-Git sentinel in the control makes apply overwrite `AGENTS.md`, proving the lost-guard tripwire. The version-only node passed after its final assertion changes; earlier harness attempts exposed expected-output mismatches, a test-only shell interpolation error, and a temporarily displaced existing timeout assertion. Those failures are retained in the step history; this node's correction exceeded the Low retry budget, so one-tier-up confirmation remains due.

Link, snippet and delegated self-check controls execute their real CLI entry points with no explicit Markdown paths. Without a decoy they flag the planted broken link or drift; with a clean tracked literal `*.md` decoy they still flag the planted file and report the one/two-file scan count. A disposable blanket-literal wildcard mutation selects only the decoy, misses the broken file and returns clean; each public finding assertion fails under that mutation. The literal filename control is explicitly POSIX-only because Windows forbids `*` in filenames; no Windows result is claimed.

Canonical Python 3.13.13 targeted evidence: upgrade N2/N3 plus the existing timeout node, 3 passed in 8.32 s; final N3-only rerun after its assertion adjustment, 1 passed in 2.41 s; real link/snippet CLI controls, 4 passed in 2.06 s; delegated self-check CLI controls, 2 passed in 1.14 s. The test-tier map selected these three files; broader file suites, full suite and 69-file replay were not run. This closes the named N2/N3 and three discovery controls only; the remaining per-route C3 matrix, usual and Security Reviews, final wide Boundary B, baseline and re-anchor remain open. **Elapsed:** approximately 16 minutes; **tokens:** unknown.

## N3 execution confirmation -- GPT-6.1 Terra (Medium) -- 2026-11-09

The one-tier-up execution confirmation after the Low retry cap passed the exact
`bootstrap/tests/test_upgrade_edit_check_runs_no_project_programs.py::test_version_only_timeout_keeps_edit_guard_and_no_answer_mutant_is_false_clean`
node once: **1 passed**, pytest 2.70 seconds, 3.59 seconds wall time. The
separately bound committed copy was clean before and after at
`34c5c3305c7743f3ef8928307f06c7aaa3132c37`, under
`/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13. Command:
`python3.13 -m pytest -q` followed by the exact node above. This confirms only
the N3 test execution; it is not another review, Security Review, or broader C3
coverage. Other tests and final verification were not run. **Elapsed:** 3.59
seconds for the test command; **tokens:** unknown.

## Owner routes and cached runner verification -- Codex GPT-6 Luna (Low) -- 2026-11-09

The route control at `b7a836af` passed its four physical Markdown owner routes
on a clean committed copy under Python 3.13.13: 4 passed in 2.83 seconds
(3.442 seconds wall time). The Medium execution corrected the common imported-
types anchor after the Low retry cap. Earlier link-gate passes and snippet
setup failures remain in their step history. This covers the four indexed
routes only, not the full caller matrix; evidence is recorded in
`/private/tmp/cairn-doc-routes-medium-b6u6ckfs/result.json`.

At `6623e1be`, audit-runner loading now verifies and executes the same source
buffer against the already verified lock digest, closing the timestamp-cache
substitution found by High. On a clean copy of that commit, the eight existing
wrong-caller-pin mutations and cached-helper control passed under canonical
Python 3.13.13: 9 passed in 8.92 seconds. No full route matrix, Windows replay,
10/69-file selection, or full suite was run. Code and Security Reviews, the
remaining caller evidence, and final wide verification remain due; this record
does not clear those obligations. **Elapsed:** unknown. **Tokens:** unknown.

## C3 owner route controls -- Codex GPT-6 Luna (Implementation, Low) -- 2026-11-09

Commit `3eaaae0115a4402269865a360cd639463fd67311` adds six real-route controls
in the existing measurement, gauge, test-tier and legacy test homes. Each
compares a clean-path public result, the unchanged caller refusing a hostile
Git executable inside its target repository, and a separate physical caller
copy with only the selected `run_git` callee changed to a PATH subprocess
adapter. Its trace confirms the pre-call marker precedes the hostile-wrapper
marker. The six routes are measurements `log`, gauge `--numstat` and snapshot
date, test-tier `diff`, and legacy `ls-tree` and `show`. Existing helper and
caller pins are unchanged. The POSIX wrapper does not establish Windows
behavior.

The exact six new nodes passed on a clean archive of that commit under
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13): **6 passed**
in 7.36 seconds. Earlier focused attempts exposed fixture mistakes: the first
six-node run had three failures, the next had one, and the single affected
measurement node then passed; after the final gauge/legacy assertions, those
four nodes passed and the final exact six passed. The failures and corrections
remain in the commit and run history. This is bounded caller-route evidence,
not final Boundary B. Other mapped tests and standing gates were not run.

The lockfile/install, session, intent, content, sweep, root-discovery and
delegated-upgrade routes remain open, as do the complete C3 caller matrix, code
and Security Reviews, and final wide verification. The prior four Markdown
index routes and nine cached-runner controls are recorded above and were not
rerun. No Windows replay, 10/69-file selection, or full suite was run. **Elapsed:**
unknown. **Tokens:** unknown. Six direct route tripwires provide useful
caller-specific evidence for modest fixture cost; the untested matrix and
required reviews remain the larger work.

## Cached runner loader protocol -- Codex GPT-6 Luna (Implementation, Low) -- 2026-11-09

Commit `92a52efff6ca2a96233619de46f24aa4f8a6f890` supplies the already
single-read, lock-hash-verified runner buffer through the `SourceFileLoader`
`get_code` protocol, then uses standard `exec_module`. The module spec,
metadata and `sys.modules` setup remain in place. The existing external-CWD
cached-helper control now traps any `SourceFileLoader.get_data` read of the
runner path, covering attempted source or bytecode reopening, while retaining
its poisoned-helper marker and real installed-audit path.

On a clean archive of that commit under canonical Python 3.13.13, the exact
eight wrong-caller-pin cases, cached-helper control, closed-allowlist control,
real Bandit liveness control and connected policy-finalize control passed:
**12 passed** in 10.67 seconds. An initial selector typo named the connected
test under the wrong class, so collection found no tests; the corrected exact
selection passed. No allowlist policy key, exception, test node or new fixture
was added, and the earlier reversed review proposal remains absent from the
diff. This alternative does not clear the usual code or Security Review.

The six owner-route controls recorded above were not rerun. The remaining C3
routes and final wide verification remain due. No Windows replay, 10/69-file
selection, full test family, or full suite was run. **Elapsed:** unknown.
**Tokens:** unknown. The loader trap adds focused assurance for the verified
buffer with one existing integration control and leaves the outstanding
caller matrix and review burden intact.

## Generated pre-commit hook routes -- Codex GPT-6 Luna (Implementation, Low) -- 2026-11-09

Commits `3471d7276f3738bc9be59414367a892798ce2e57` and
`fbee95e1589d1badc16909a378aa9eb387ebc745` add four POSIX route controls in
the existing intent-tool test. The cases cover both physical `conflict.py`
owners and the generated hook's staged-path and rename reads. Each fixture
uses the actual installed pre-commit hook and an absolute known-good Git for
repository setup. Healthy controls prove silent empty-index completion, the
unclaimed staged-file warning, and claim credit for a staged rename.

Each hostile case switches PATH immediately before its one selected hook-index
read. The unchanged caller reports unavailable coordination without running
the target-local Git wrapper. A separate physical caller copy changes only
that selected reader call to the PATH subprocess adapter; the same public hook
then runs the marker wrapper, falsifying the safe-refusal assertion. The route
trace verifies that the trigger preceded wrapper execution.

The first clean-copy run failed all four cases before the hook because the
restricted PATH could not resolve the generated `env bash` hook. The fixture
now keeps the known-good Git directory first and appends the ordinary safe
PATH; the hostile path is still set only at the selected read. On the clean
archive of `fbee95e1589d1badc16909a378aa9eb387ebc745`, canonical Python 3.13.13
passed all four exact parameter cases in 15.36 seconds. No product reader
changed, and no Windows, native, broad-family, 10/69-file or full-suite claim
is made.

This closes only the two physical pre-commit index routes. Remaining
pre-commit owners and post-commit, session, root-discovery and other C3 routes
remain open, along with code and Security Reviews and final wide verification.
**Elapsed:** unknown. **Tokens:** unknown. Four direct hook routes add focused
caller evidence at moderate fixture cost; the broader matrix and required
reviews remain the continuing burden.

## Scoped self-host lock coherence -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

At `fa462bbb`, the official scoped `upgrade --finalize` advanced only the
`hash` fields of the 15 preidentified verbatim records whose on-disk bytes
already matched their current template sources. Every other lock field and
record, the base hashes, and all source/template files remained unchanged. A
separate clone of `3396ddfa` produced the same exact 15-field delta through the
same official writer (`90836fb8`), before the canonical update.

On a clean committed copy of `fa462bbb`, `tools/intent.py --help` loaded and
ran successfully. A read-only audit found 35 tracked verbatim records: all 35
hashes match their on-disk bytes; 34 destinations equal current templates, and
`scripts/prose_roots.txt` retains its existing local roots beyond the template's
header. No private collection, full integrity/history ceremony, suite, or source
change was run. **Elapsed:** approximately 8 minutes; **tokens:** unknown.

## C3 native-policy source classification -- GPT-6.1 Sol (High) -- 2026-11-09

Source inspection supports 23 additional POSIX case identities within accepted
C3 platform coordination. This is implementation source classification, not a
Security Review pass or Maintainer Decision. Preserve all 664 existing policy
rows, tags and order; no B102 exception or trust relaxation is part of this work.

- Four physical Markdown owners and six ordinary-reader controls execute a
  target-local `#!/bin/sh` Git wrapper. Four generated pre-commit controls
  execute an extensionless Python-shebang Git wrapper through their selected
  physical hook read. Their unsafe-route positives require POSIX executable
  behavior; these 14 controls do not supply Windows native route evidence.
- Three CLI discovery controls and three earlier unit discovery controls
  physically create and stage `*.md`, distinguishing a literal filename from
  Git glob discovery. Windows cannot represent that filename. The separate
  no-decoy discovery controls remain portable.
- Three replay controls exercise the helper's explicitly POSIX-only
  `O_NOFOLLOW`, `O_DIRECTORY` and descriptor-relative open/stat contract.
  Missing required capabilities on a POSIX host remain unmet prerequisites.

The exact 23-row delta is `/private/tmp/cairn-native-source-sol-final23.json`.
Append its sorted additions without reordering existing rows: 61 NT plus
626 POSIX gives 687 identities. The actual ordered-row validator produces
`sha256:363e6b16a6473b139e9f5eb37f129f2b895542af8e8ac2457e394647245ea4c6`.
Update the manifest and connected-fixture count guards to 626 POSIX, policy
assertions to 687 identities, and synthetic raw outcomes to 688.

Portable fixture repairs remain separate and receive no native classification:
preserve the actual host-applied target mode while retaining the POSIX `0640`
assertion; retain LF path escaping on POSIX and use representable Unicode on
Windows for coupling output. Hardlink and symlink availability remain real
environment prerequisites, with no quiet strict-run skip allowance.

Evidence: inspected committed source `6f64ddf5..37f12b4a`, including the strict
collector, policy validator and physical fixture mechanisms. A clean committed
copy of `37f12b4a` collected 592 identities from the ten targeted test files in
0.68 seconds under Python 3.13.13; no test execution occurred in this step.
Earlier POSIX route passes remain their authors' recorded measurements, not
reruns here. Coverage excludes Windows execution, full-suite collection,
Boundary B and formal reviews. **Elapsed:** approximately 8 minutes across the
classification and clarification; **tokens:** unknown.

## Implementation verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

Commit `eaff9f82c13de47a7666eeee4eee8a10d57e8218` implements High's
23-row POSIX source classification from `bc790853` and
`/private/tmp/cairn-native-source-sol-final23.json`. It preserves the 664
previous rows in their prior order and appends only the sorted 23-row delta.
The checked policy has 687 unique identities (61 NT, 626 POSIX), 688 raw
synthetic outcomes, and the approved ordered-row ID
`sha256:363e6b16a6473b139e9f5eb37f129f2b895542af8e8ac2457e394647245ea4c6`.
The connected fixture and count guards use the updated totals. The same commit
repairs two portable controls: the mode test retains the actual host-applied
mode and still asserts POSIX `0640`; the coupling test retains its LF filename
on POSIX and uses U+2028 on Windows, checking the JSON-escaped path.

On an archive of the committed bytes under canonical Python 3.13.13, policy
uniqueness, raw-report positive control, and both portable fixture nodes passed
(4 passed in 0.94 seconds). The connected fixture failed there because its
implementation invokes `git archive HEAD` from `CAIRN_ROOT`, unavailable in an
archive without `.git`. I retained that attempt and retried only the connected
node from a detached clean clone of the same commit; it passed (1 passed in
16.72 seconds). The clone was clean before the check. The full set of five
specified nodes therefore passed across those focused runs; no wider selection
was run.

This source-based classification does not establish Windows equivalence for
the 23 POSIX cases. Windows execution, the other 10/69-file and 14/28-file
selections, full suite, final Boundary B, and usual code and Security Reviews
remain outstanding. No policy exception or runtime source change was made.
**Elapsed:** approximately 16 minutes; **tokens:** unknown.

## Implementation verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-09 -- local intent hook interpreter refresh

The installed worktree's old generated pre-commit and post-commit hooks invoked
`/Users/kendal30/conda_envs/miniforge3/bin/python3` (Python 3.12.9). A read-only
probe of the committed `tools/git_read.py` returned
`safe-process-supervision-unavailable` for both `read_hook_index` and `run_git`
under that interpreter; the same exact calls completed under canonical Python
3.13.13. This explained why recent commits emitted the existing advisory that
staged path discovery was unavailable.

Saved both existing hook files under
`/private/tmp/cairn-intent-hooks-before-refresh-20261109/`, then used only the
existing `tools/intent.py install-hook` and `install-precommit` commands with
`--python /Users/kendal30/conda_envs/lhm/bin/python3.13`. No hook source was
hand-edited. `hooks-status` reports both installed, and the generated bodies
invoke the canonical interpreter without raw shell Git discovery. The actual
`_precommit_check` returned 0 with an empty staged index. The next ordinary
commit, `2b067c347c3bbd2e24d6ab062f7a32eb64e485d1`, triggered the regenerated
post-commit hook and auto-released its owned claim. No binding was created.

This is local hook maintenance and interpreter diagnosis; it changes no tracked
product file and establishes no host-wide or native Windows behavior. The
backup copies remain available at the path above. **Elapsed:** approximately 5
minutes; **tokens:** unknown.
