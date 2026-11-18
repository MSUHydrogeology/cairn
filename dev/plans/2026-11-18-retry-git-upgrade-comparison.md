# Plan: Retry the isolated Git upgrade comparison

**Source proposal**: dev/proposals/archive/2026-11-18-terra-retry-git-upgrade-comparison.md
**Status**: ready-to-implement
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-18
**Rules that apply**: dev/rules/conventions.md, dev/rules/protected-surfaces.md, dev/rules/working-agreements.md, dev/rules/development-environment.md
**In brief**: Compare a Git merge with Cairn's upgrade on matched synthetic projects inside a verified guest boundary.

## Build summary

Use the existing Linux guest for one controlled comparison, after a reviewed guest setup and nonvacuous confinement controls. Reconstruct the prior install faithfully, run both paths against three identical variants, and record the outcomes and limits. A failed control stops the comparison; no result authorizes an engine replacement.

## Source proposal

The Maintainer accepted the revised heavy proposal and temporary guest administrator setup under a reviewed plan. The earlier Mac trial stopped before comparison; the Linux isolation candidate is untested. Approval includes neither a broader fallback nor release of existing protections.

## Scope

Use the shared `linux-dev` guest described in `dev/rules/development-environment.md`; do not alter other projects or global policy, add packages or create a VM. Create an owned temporary workspace with no host shares. Pin the v0.5.0 source `3bb27388fccaf51ae490e80ca4b4ab94aa5e2206`, a clean candidate commit, guest Python and Git, profile, driver and corpus hashes. The recorded Mac interpreter is `/Users/kendal30/conda_envs/lhm/bin/python3.13`; record the guest runtime actually used. Synthetic inputs only; no production engine, installed contract, trust record or real adopter data changes. No doctrine surface changes. Estimated work window: 2 to 4 hours across C1–C3; main uncertainty is tuning the Linux unshare/pidfd/subreaper lifetime and AppArmor canary controls on ARM64 Linux 6.8 and achieving byte-exact v0.5.0 predecessor reconstruction.

The reviewed setup must make a private filesystem, network, PID and IPC view and install a unique deny-default AppArmor trial profile. Pinned sources and driver are read-only; only the synthetic writable island W and `/dev/null` are writable. Allow exact Python and Git applications to execute, with loader and libraries read or mapped but not directly executable. Drop setup privilege before trial, deny network, remove the temporary profile and owned workspace afterward, and verify cleanup. No comparison writes precede startup and all C0 controls; no unsafe fallback.

### Guest setup and launch

High-tier design input (not a demonstrated C0 pass): the guest was observed as
ARM64 Linux 6.8, UID/GID 1001, Python `/usr/bin/python3.12`, Git
`/home/cairn/opt/git-2.56.1/bin/git`, util-linux 2.39.3 and AppArmor 4.0.1.
Verify those facts, sudo availability, AppArmor and required syscalls again;
stop if missing. No profile load, mount or privileged setup occurs before both
plan reviews. Run a reviewed fixed Python supervisor using `sudo -n
/usr/bin/python3.12 -I -B -` on script stdin; never evaluate trial data as shell.
Create a root-owned `mkdtemp` under `/tmp`, record its device/inode and use a
128-bit random token for unique profile `cairn-upgrade-<32hex>`. Write root-only (`0600`)
`fsync`ed recovery metadata (host boot ID, profile name, owned `mkdtemp` path,
device/inode, and monitor/PID1 PID plus start time as acquired) in a sibling
root-only metadata file before loading policy or launching children so abrupt
supervisor loss leaves verifiable cleanup identifiers. Stage only
hash-checked regular committed inputs and reviewed scripts using descriptor-
relative `O_NOFOLLOW` traversal, without hardlinks; stage backing `canary` as
mode `0600` owned by UID `1001` inside a guard staging directory. Record the existing loaded
profiles. Refuse an existing name; load only the new profile with
`apparmor_parser -a -K PROFILE` and verify `NAME (enforce)` in
`/sys/kernel/security/apparmor/profiles`. Never replace another profile.

Enable `PR_SET_CHILD_SUBREAPER` in the supervisor so if the `unshare` monitor dies
before guest `PID1`, `PID1` reparents directly to the supervisor rather than init.
For each launch, keep the supervisor as the sole writer to the lifeline pipe
(checking EOF and write readiness before fork and during reaping), and use
`Popen` with `start_new_session=True`, fresh environment, DEVNULL stdin,
anonymous output pipes and only the lifeline read FD:
`/usr/bin/unshare --mount --net --pid --ipc --fork --kill-child=SIGKILL --propagation
private /usr/bin/python3.12 -I -B ROOT/ns-init.py` (do not rely on `--kill-child`
after privilege drop, since `setuid` clears `PR_SET_PDEATHSIG`). Identify `PID1` as the
sole live owned child of the `unshare` monitor by verifying `PPid`, `NSpid`, `UID`,
start time and `/proc/<pid>/fdinfo` showing the inherited lifeline read-end FD, and
hold separate `os.pidfd_open` handles for both the `unshare` monitor and `PID1` before
opening `/guard/go`. `PID1` mounts a
`nosuid,nodev` tmpfs root, populates the pinned copy manifest and binds only W
at `/w` (nonrecursive, `rw,nosuid,nodev,noexec`), protected canary at `/guard`
(nonrecursive, `ro,nosuid,nodev,noexec`), and verified character device
`/dev/null` (major 1, minor 3; `rw,nosuid,noexec`, without `nodev`). Inputs in
`/inputs` are root-owned read-only. Pivot with ARM64 `pivot_root` syscall 41,
chdir to `/`, detach and remove `/.old`, then remount root `ro,nosuid,nodev`.
Mount no proc, sysfs, shm, mqueue, home, host cwd or shares; keep private loopback down.

Copy Python to `/usr/bin/python3.12`, Git to `/opt/cairn-trial/bin/git`, and regular files from `dpkg-query -L`
for `libpython3.12-minimal` and `libpython3.12-stdlib` under
`/usr/lib/python3.12`, excluding site/dist-packages, links and pyc. Copy the
loader to `/usr/lib/aarch64-linux-gnu/ld-linux-aarch64.so.1` with `/lib ->
usr/lib`, plus the pinned dependency closure: `libc.so.6`, `libm.so.6`, `libz.so.1`,
`libexpat.so.1`, `libbz2.so.1.0`, `libcrypt.so.1`, `libcrypto.so.3`,
`libdb-5.3.so`, `libffi.so.8`, `liblzma.so.5`, `libncursesw.so.6`,
`libpanelw.so.6`, `libreadline.so.8`, `libsqlite3.so.0`, `libssl.so.3` and
`libtinfo.so.6`. Record exact files, aliases and hashes; no system ld cache, NSS or configuration. Use only
synthetic pinned passwd/group files if needed. Refuse an unsupported closure.

The named profile uses `flags=(chroot_relative,mediate_deleted)`, no
abstractions, the exact copied Python and Git paths `mrix`, and loader, named libraries and packaged
extensions `mr` without execute. Permit read of `/usr/lib/python3.12/{,**}`,
`/inputs/{,**}` and `/guard/{canary,go}`; permit `/w/{,**} rwk`,
`link subset /w/** -> /w/**`, and `/dev/null rw`. Allow signal send/receive to
the same profile and receive from `unconfined`; deny network, unix, capability,
userns, ptrace, mount, umount and pivot_root. Profile rules are comma-ended.

Drop groups with `setgroups([])`, bounding capabilities 0–40 via
`PR_CAPBSET_DROP`, clear ambient capabilities, set all real/effective/saved
GID and UID to 1001, and zero both capability words using ABI v3
`0x20080522`. Set `PR_SET_NO_NEW_PRIVS=1` and `PR_SET_DUMPABLE=0`. Fork trial
PID2; PID1 remains an unprivileged trusted reaper, calls
`waitpid(-1,WNOHANG)` and polls only the supervisor lifeline until exit or
failure. PID2 sets stdin to private `/dev/null`, closes FD 3 and above with
`close_range(3,UINT_MAX,0)`, and installs preloaded libseccomp rules denying `socket`,
`socketpair`, `io_uring_setup`, `io_uring_register`, `io_uring_enter` and
`pidfd_getfd`. Enter AppArmor via ARM64 `lsm_set_self_attr` syscall 460:
attribute 101, flags 0, context `struct.pack('=QQQQ',104,0,32+len(payload),
len(payload))+payload`, payload `b'exec '+NAME.encode()+b'\0'`. Require zero,
then exec exact Python with `-I -B`, fixed constant or trusted `/inputs` driver,
fresh C environment and PATH containing only the Git parent; HOME and temp are
under W. No target-installed code executes.

Prove the post-exec profile via syscall 459 (`CURRENT=100`, `SINGLE=1`,
AppArmor ID 104). Hold the owned child on `/guard/go`; before creating the gate,
the supervisor verifies both `PID1` (monitor-child `PPid`, sole child, lifeline
`fdinfo`, private `mnt`/`net`/`pid`/`ipc` namespace IDs, no `/dev/shm` or
`/dev/mqueue` paths, and separate monitor/`PID1` `pidfd`s) and `PID2` (`NSpid`,
matching namespace IDs, zero capability sets, `NoNewPrivs=1`, `Dumpable=0`, and
`NAME (enforce)`), updates the root recovery metadata with `PID1` start time,
and then creates `/guard/go`. Clear it between launches. Missing proof never opens
the gate. Prove the canary positive control with an unconfined helper running as
the same UID `1001` that writes one byte to `canary` using only a preopened
host `guard-dirfd`; supervisor observes the changed digest and restores the
original content. In the confined guest, read `/guard/canary` first to confirm the
same inode and visibility, then attempt a non-truncating write (`O_WRONLY`/`O_RDWR`
without `O_CREAT`/`O_TRUNC`) and require `EACCES`, `EPERM` or `EROFS` with
unchanged parent digest (`ENOENT`/`ENOTDIR` fails C0). Check
loader direct execution is denied and exact Git starts under the same profile.
PID1 polls the lifeline and reaps all children; EOF or trial exit kills any remaining namespace processes.

Cap each captured stream at 1 MiB, each command at 60 seconds and driver at
15 minutes. Install handlers for catchable termination signals (`SIGTERM`,
`SIGINT`), and on exit, timeout, signal or monitor-first loss close the
supervisor lifeline write FD, track monitor state, send `SIGKILL` to the owned
`PID1` `pidfd` (and monitor `pidfd` if alive) and reap both `PID1` (via
`PR_SET_CHILD_SUBREAPER`) and the monitor while checking lifeline EOF. Abrupt
`SIGKILL` loss of the supervisor leaves only the boot-scoped root recovery
metadata, loaded profile name and root-owned `mkdtemp` path/device/inode for
verified post-mortem cleanup.
Before cleanup verify private mount IDs are gone and the parent mount list has
no owned paths. In `finally`, remove only the exact loaded profile with
`apparmor_parser -R -K` on the same bytes; verify its absence and the unrelated
profile listing. Check the owned root's owner/device/inode and remove by
FD-safe traversal without following links or mounts; remove the sibling root
recovery metadata file only after verified cleanup succeeds. If reaping, profile or
path verification is uncertain, stop and report the exact owned residual;
never blindly remove it. Record source-controlled reviewed supervisor input if
needed for reproducibility, not a separate evidence ledger.

**Reuse.** The archived `dev/plans/archive/2026-11-12-upgrade-growth.md` C0–C1 supplies the bounded driver, controls, Git isolation settings and corpus. Searched `install/_scaffold/install.py` and `install/_scaffold/upgrade.py`: installer assembly includes module-merge and onboarding overlays; raw-cache reconstruction deliberately excludes generated overlays. Reuse those version-appropriate routines and verified `dev/tools/git_read.py`; old scratch drivers are absent. Temporary drivers belong in scratch, with no retained tooling or evidence folder unless strictly needed.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Set up the private guest view, prove startup and C0 controls | Both plan reviews | Controlled trial island and recorded evidence |
| C2 | Reconstruct old baseline and compare six matched cells | C1 passes | Trial results and 37-case classification |
| C3 | Remove owned guest profile and workspace; record cleanup | C1 setup, including failures | Cleanup evidence and remaining limits |

## Acceptance criteria

**C1.** Under the same final restrictive profile, the pinned Python `-I -B -c` constant print succeeds after privilege drop. Verify private `mnt`, `net`, `pid` and `ipc` namespace IDs differ from parent and zero `/dev/shm` or `/dev/mqueue` paths exist in guest mounts or policy; prove subreaper, separate monitor/PID1 `pidfd`s, lifeline EOF and root recovery metadata behavior without relying on `--kill-child` after `setuid`. The known-absent marker remains absent. Prove the canary positive control with an unconfined UID-`1001` write of one byte via only a preopened `guard-dirfd` (parent observes change and restores), then inside confinement read the mode-`0600` `/guard/canary` (proving the exact same inode) and require `EACCES`/`EPERM`/`EROFS` on a non-truncating write with parent-observed digest unchanged (`ENOENT`/`ENOTDIR` fails C0); deliberately alter W's outside sentinel, detect it and restore it. A controlled guest-side unsandboxed loopback reaches its listener; the confined child cannot connect and is not observed. The verified read helper returns the exact synthetic root and refuses `push --all` without launch. Record exact commands, profile and hashes, outputs and limits. Failure stops comparison writes and remains incomplete; earlier broad-read probes do not satisfy C0.

**C2.** Reconstruct each recorded predecessor destination from verified base hashes, conditional sizing and tokens, with the actual security-module merge for `AGENTS.md` and onboarding overlay for `dev/PLANNING.md`. Compare bytes against an independently saved clean install; classify unrecorded install outputs. A mismatch stops the Git leg. Verify Git ancestry before running the cells: the reconstructed predecessor commit `T0` must be the sole direct parent (`parents == [T0]`) of both candidate template commit `T1` and each synthetic adopter base commit, confirmed with `git merge-base`. From identical customizations run benign, committed leaf-link and committed linked-parent variants through both Git merge and public `upgrade --plan`, `--stage`, `--apply` (six cells). Record conflicts, marker preservation, sentinel and outside changes, operator steps, modules exercised, migration result, timings, platform, versions, hashes, exclusions and limits. Classify all 37 pinned hostile functions and parameter classes applicable, inapplicable or untested, with reason and remaining mechanism; this is not a security-equivalence claim.

**C3.** On success or failure, remove only the owned profile and scratch root without following planted links; verify absence and unchanged unrelated policy and projects. Failure to establish cleanup stays open. No routine human action is a final chunk.

## Scope delta

**Scope delta**: preserved

## Verification

Before implementation, map changed paths with `tests/tier_inventory.py`; use applicable claim, link, snippet, neutrality and `tests/check_cairn.py` prose gates and known-positive controls for negative searches. C1 uses the specified guest setup, read dependencies, privilege and cleanup proofs; startup alone does not satisfy its controls. C2 uses the old snapshot's `bootstrap/scaffold.py`, candidate `install/scaffold.py` and trusted Git. Retain the archived C1 controlled Git environment, empty hooks/templates, configuration checks, isolated home/temp, timeout/process-group handling and no execution of target-installed code. The driver uses temporary artifacts only; no permanent promise test is required solely for observations. Record elapsed time, tokens and all failures. Independent ordinary and Security code reviews follow; the arc owner runs one joined integration at the arc end.

## Plan review -- gpt-6.1-terra, Reviewer -- 2026-11-18

Reviewed commit: a1522c0fed2c3054d618a10a4ca252020e0c75e5

**Obligation**: Internal plan review
**Tier**: Internal
**Findings**: raised

The plan aims to make the accepted comparison observable without treating a failed isolation control as a successful trial.

1. **Should this happen as framed?** Yes: C1 gates C2 on both reviews and confinement controls, and C2 retains the six matched cells, baseline comparison and 37-case classification -- accepted proposal, Proposal and Evidence; plan Sequence and Acceptance criteria.
2. **Best alternative.** The temporary driver and existing installer routines avoid a maintained trial framework while retaining the accepted outcomes -- plan Scope and Reuse; archived upgrade-growth plan C0–C1.
3. **What would show it wrong?** A failed control, mismatched reconstructed destination, or an unobserved cell must stop the affected work or leave it incomplete -- plan C1–C3 and Verification.

**Non-blocking finding:** The plan gives command and driver time limits but no estimated work window or uncertainty, as required by `dev/agent_collaboration.md` under Plans and records. Add an approximate window and its main uncertainty; it is an estimate, not a deadline or waiver.

**Coverage:** Compared the committed plan with the accepted proposal, current template, archived C0–C1 and installer reuse points. The plan adds no doctrine and leaves installed duties in their existing homes. No guest setup, controls, comparison, tests, Security Review or integration was run; feasibility and confinement remain unproven. Elapsed: unknown. Tokens: unknown.

## Plan review -- gpt-6.2-sol (Security Review, High) -- 2026-11-18

Reviewed commit: c76e760454972011ff37eed18a31a9f4cae9de64

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE

1. **Should this happen as framed?** The accepted retry can run after the shared guest boundary and controls are complete. See the Decision and C1.
2. **Best alternative.** Keep the temporary launcher and adopt archived C1's matched snapshots and template ancestry explicitly. Both the adopter and candidate template commits descend directly from the verified reconstructed predecessor. See Reuse and archived C1.
3. **What would show it wrong?** A surviving trial process, a false pass on the outside-write control or a baseline mismatch invalidates the affected result. See C1–C3 and archived C0–C1.

**Blocking — process lifetime.** The supervisor starts the `unshare` monitor, which forks and reaps PID1. The credential drop clears the monitor-death signal. Specify how the supervisor identifies and holds a process handle for PID1 before opening the gate, handles monitor loss, closes the lifeline and confirms exit, and reaps its own monitor before removing the profile. Define how catchable termination reaches cleanup and which owned identifiers survive abrupt supervisor loss. [util-linux source](https://github.com/util-linux/util-linux/blob/v2.39.3/sys-utils/unshare.c#L896-L982), [Linux parent-death signal](https://man7.org/linux/man-pages/man2/PR_SET_PDEATHSIG.2const.html).

**Blocking — shared guest IPC.** The launcher leaves UID 1001 in the guest's interprocess communication namespace. Its listed restrictions do not isolate System V shared memory, semaphores or queues. Use and verify a private IPC namespace in the existing launcher. [Linux IPC namespaces](https://man7.org/linux/man-pages/man7/ipc_namespaces.7.html), [AppArmor kernel hooks](https://github.com/torvalds/linux/blob/v6.8/security/apparmor/lsm.c#L1341-L1432).

**Blocking — canary false pass.** Specify a mode-0600 canary writable by the trial UID before confinement, prove the confined probe can read that same file, and require a permission or read-only denial at the attempted write with the parent digest unchanged. Missing-path errors fail C0. See Guest setup and launch, C1 and archived C0.

**Coverage:** Read the Decision, both plans, template and verifier source. No guest setup, controls, baseline reconstruction, comparisons or tests ran. Elapsed: unknown. Tokens: unknown.

## Author Response -- Orchestrator (Argon, High) -- 2026-11-18

**Disposition**: ready-to-implement

All plan review findings are accepted and folded into the operative plan text per the prepared High security corrections:

- **Estimated work window (`gpt-6.1-terra`, non-blocking)**: Added a 2–4 hour work window across C1–C3 and its primary technical uncertainty under `## Scope`.
- **Process lifetime (`gpt-6.2-sol`, blocking)**: Replaced post-`setuid` reliance on `--kill-child` (`PR_SET_PDEATHSIG` clears across credential drop) with supervisor `PR_SET_CHILD_SUBREAPER`, sole-writer lifeline pipe, `PPid`/`NSpid`/`UID`/start-time/`fdinfo` identification of guest `PID1` as the monitor's sole live child before opening `/guard/go`, separate `os.pidfd_open` handles for monitor and `PID1`, catchable signal handlers (`SIGTERM`/`SIGINT`), lifeline EOF checks on reap, and boot-scoped root-only (`0600`) `fsync`ed recovery metadata for abrupt supervisor loss.
- **Shared guest IPC (`gpt-6.2-sol`, blocking)**: Added `--ipc` to `unshare`, required verifying `mnt`/`net`/`pid`/`ipc` namespace ID isolation on both `PID1` and `PID2`, and prohibited `/dev/shm` and `/dev/mqueue` mounts or AppArmor paths.
- **Canary false pass & `T0` ancestry (`gpt-6.2-sol`, blocking)**: Specified staging `/guard/canary` as mode `0600` owned by UID `1001` under a read-only `/guard` bind, proving positive writability via an unconfined UID-`1001` write using only a preopened host `guard-dirfd` (observed and restored by parent), then proving the confined child reads that exact same inode before receiving `EACCES`/`EPERM`/`EROFS` on a non-truncating write with unchanged digest (`ENOENT`/`ENOTDIR` fails C0). Added explicit `C2` check that reconstructed predecessor `T0` is the sole direct parent of candidate template `T1` and each synthetic adopter base commit via `git merge-base`.

Elapsed: unknown. Tokens: unknown.
