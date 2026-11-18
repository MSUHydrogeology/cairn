# Plan: Retry the isolated Git upgrade comparison

**Source proposal**: dev/proposals/archive/2026-11-18-terra-retry-git-upgrade-comparison.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-18
**Rules that apply**: dev/rules/conventions.md, dev/rules/protected-surfaces.md, dev/rules/working-agreements.md, dev/rules/development-environment.md
**In brief**: Compare a Git merge with Cairn's upgrade on matched synthetic projects inside a verified guest boundary.

## Build summary

Use the existing Linux guest for one controlled comparison, after a reviewed guest setup and nonvacuous confinement controls. Reconstruct the prior install faithfully, run both paths against three identical variants, and record the outcomes and limits. A failed control stops the comparison; no result authorizes an engine replacement.

## Source proposal

The Maintainer accepted the revised heavy proposal and temporary guest administrator setup under a reviewed plan. The earlier Mac trial stopped before comparison; the Linux isolation candidate is untested. Approval includes neither a broader fallback nor release of existing protections.

## Scope

Use the shared `linux-dev` guest described in `dev/rules/development-environment.md`; do not alter other projects or global policy, add packages or create a VM. Create an owned temporary workspace with no host shares. Pin the v0.5.0 source `3bb27388fccaf51ae490e80ca4b4ab94aa5e2206`, a clean candidate commit, guest Python and Git, profile, driver and corpus hashes. The recorded Mac interpreter is `/Users/kendal30/conda_envs/lhm/bin/python3.13`; record the guest runtime actually used. Synthetic inputs only; no production engine, installed contract, trust record or real adopter data changes. No doctrine surface changes.

The reviewed setup must make a private filesystem, network and PID view and install a unique deny-default AppArmor trial profile. Pinned sources and driver are read-only; only the synthetic writable island W and `/dev/null` are writable. Allow exact Python and Git applications to execute, with loader and libraries read or mapped but not directly executable. Drop setup privilege before trial, deny network, remove the temporary profile and owned workspace afterward, and verify cleanup. No comparison writes precede startup and all C0 controls; no unsafe fallback.

### Guest setup and launch

High-tier design input (not a demonstrated C0 pass): the guest was observed as
ARM64 Linux 6.8, UID/GID 1001, Python `/usr/bin/python3.12`, Git
`/home/cairn/opt/git-2.56.1/bin/git`, util-linux 2.39.3 and AppArmor 4.0.1.
Verify those facts, sudo availability, AppArmor and required syscalls again;
stop if missing. No profile load, mount or privileged setup occurs before both
plan reviews. Run a reviewed fixed Python supervisor using `sudo -n
/usr/bin/python3.12 -I -B -` on script stdin; never evaluate trial data as shell.
Create a root-owned `mkdtemp` under `/tmp`, record its device/inode and use a
128-bit random token for unique profile `cairn-upgrade-<32hex>`. Stage only
hash-checked regular committed inputs and reviewed scripts using descriptor-
relative `O_NOFOLLOW` traversal, without hardlinks. Record the existing loaded
profiles. Refuse an existing name; load only the new profile with
`apparmor_parser -a -K PROFILE` and verify `NAME (enforce)` in
`/sys/kernel/security/apparmor/profiles`. Never replace another profile.

For each launch, use `Popen` with `start_new_session=True`, fresh environment,
DEVNULL stdin, anonymous output pipes and only the supervisor lifeline read FD:
`/usr/bin/unshare --mount --net --pid --fork --kill-child=SIGKILL --propagation
private /usr/bin/python3.12 -I -B ROOT/ns-init.py`. PID1 mounts a
`nosuid,nodev` tmpfs root, populates the pinned copy manifest and binds only W
at `/w` (nonrecursive, `rw,nosuid,nodev,noexec`), protected canary at `/guard`
(nonrecursive, `ro,nosuid,nodev,noexec`), and verified character device
`/dev/null` (major 1, minor 3; `rw,nosuid,noexec`, without `nodev`). Inputs in
`/inputs` are root-owned read-only. Pivot with ARM64 `pivot_root` syscall 41,
chdir to `/`, detach and remove `/.old`, then remount root `ro,nosuid,nodev`.
Mount no proc, sysfs, home, host cwd or shares; keep private loopback down.

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
AppArmor ID 104). Hold the owned child on `/guard/go`; the supervisor checks
its scoped proc ancestry, IDs, capability sets and NoNewPrivs, then creates the
gate. Clear it between launches. Missing proof never opens the gate. Check
loader direct execution is denied and exact Git starts under the same profile.
PID1 polls the lifeline and reaps all children; EOF or trial exit kills any remaining namespace processes.

Cap each captured stream at 1 MiB, each command at 60 seconds and driver at
15 minutes. On failure or timeout kill the owned namespace-init pidfd with
SIGKILL and reap it; `--kill-child` and the lifeline cover supervisor loss.
Before cleanup verify private mount IDs are gone and the parent mount list has
no owned paths. In `finally`, remove only the exact loaded profile with
`apparmor_parser -R -K` on the same bytes; verify its absence and the unrelated
profile listing. Check the owned root's owner/device/inode and remove by
FD-safe traversal without following links or mounts. If reaping, profile or
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

**C1.** Under the same final restrictive profile, the pinned Python `-I -B -c` constant print succeeds after privilege drop. The known-absent marker remains absent. A write to a protected outside canary is denied and its parent-observed digest unchanged; deliberately alter W's outside sentinel, detect it and restore it. A controlled guest-side unsandboxed loopback reaches its listener; the confined child cannot connect and is not observed. The verified read helper returns the exact synthetic root and refuses `push --all` without launch. Record exact commands, profile and hashes, outputs and limits. Failure stops comparison writes and remains incomplete; earlier broad-read probes do not satisfy C0.

**C2.** Reconstruct each recorded predecessor destination from verified base hashes, conditional sizing and tokens, with the actual security-module merge for `AGENTS.md` and onboarding overlay for `dev/PLANNING.md`. Compare bytes against an independently saved clean install; classify unrecorded install outputs. A mismatch stops the Git leg. From identical customizations run benign, committed leaf-link and committed linked-parent variants through both Git merge and public `upgrade --plan`, `--stage`, `--apply` (six cells). Record conflicts, marker preservation, sentinel and outside changes, operator steps, modules exercised, migration result, timings, platform, versions, hashes, exclusions and limits. Classify all 37 pinned hostile functions and parameter classes applicable, inapplicable or untested, with reason and remaining mechanism; this is not a security-equivalence claim.

**C3.** On success or failure, remove only the owned profile and scratch root without following planted links; verify absence and unchanged unrelated policy and projects. Failure to establish cleanup stays open. No routine human action is a final chunk.

## Scope delta

**Scope delta**: preserved

## Verification

Before implementation, map changed paths with `tests/tier_inventory.py`; use applicable claim, link, snippet, neutrality and `tests/check_cairn.py` prose gates and known-positive controls for negative searches. C1 uses the specified guest setup, read dependencies, privilege and cleanup proofs; startup alone does not satisfy its controls. C2 uses the old snapshot's `bootstrap/scaffold.py`, candidate `install/scaffold.py` and trusted Git. Retain the archived C1 controlled Git environment, empty hooks/templates, configuration checks, isolated home/temp, timeout/process-group handling and no execution of target-installed code. The driver uses temporary artifacts only; no permanent promise test is required solely for observations. Record elapsed time, tokens and all failures. Independent ordinary and Security code reviews follow; the arc owner runs one joined integration at the arc end.
