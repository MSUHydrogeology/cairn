# Restore Python 3.12 support without weakening process cleanup

**Author**: GPT-6.1 Sol (Strategy, High)
**Status**: awaiting-decision
**Review**: usual + Security Review
**Proposed tier**: heavy — process supervision and verified helper delivery
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-12
**In brief**: Make shipped tools work on Python 3.12 while preserving bounded, contained Git reads on macOS, Linux and Windows.
**Elapsed**: approximately seven minutes. **Tokens**: unknown.

## Decision summary

Python 3.12 on macOS cannot currently run Cairn's safe Git reader, so session
startup incorrectly says the project is not a Git repository. Supply the missing
Python wrapper through a small binding to macOS's existing system function.
Keep the current process supervisor and check actual Python 3.12 workflows for
the shipped tools. This adds a maintained native binding, but no dependency,
command, setting or Maintainer ceremony. One plan delivers board item 21.

## Context

At `5ba9ad64`, `tools/git_read.py:756` refuses POSIX interpreters lacking
`os.waitid`. Installed Python 3.12.9 at
`/Users/kendal30/conda_envs/miniforge3/bin/python3.12` lacks it; canonical 3.13
has it. SafeGit's C0 deliberately refused an unexamined fallback. Its accepted,
capped Security fixes remain accepted; this is new compatibility scope.

The temporary primitive probe `/private/tmp/cairn-python312-observer-probe.py`
ran on 3.12.9: native `waitid` reported a live child as PID zero, then the exact
exited PID twice without reaping it; ordinary `wait` subsequently returned zero.
Late `kqueue` registration instead returned `EV_ERROR/ESRCH`, so exit flags alone
are insufficient. Group cleanup, timeouts and other shipped workflows were not
measured by this probe.

## Proposal

Add one private owned-child exit observer to the existing helper and its
byte-identical shipped twin. Select its backend before launching a child:
prefer the complete existing `os.waitid` API; otherwise use the following
Darwin-only native binding. Other unsupported POSIX hosts continue to refuse;
Linux retains `os.waitid` and Windows retains its existing isolated Job worker.

Use standard-library `ctypes`, already used for Darwin cleanup, to load only
`/usr/lib/libSystem.B.dylib` with `use_errno=True`. Bind
`waitid(int, unsigned int, siginfo_t*, int) -> int`. Use Apple's documented
64-bit `siginfo_t` field layout, including its signal-value union and seven
reserved unsigned longs; require 4-byte signed/unsigned ints, 8-byte
pointers/longs, 104-byte structure and PID offset 12. Reject unsupported layout,
library or symbol before launch. The ABI comes from Apple's
[signal header](https://raw.githubusercontent.com/apple-oss-distributions/xnu/main/bsd/sys/signal.h)
and [wait header](https://raw.githubusercontent.com/apple-oss-distributions/xnu/main/bsd/sys/wait.h),
also inspected in this host's SDK; no runtime compiler or SDK is required.

Every observation uses a fresh zeroed structure, the exact positive owned PID,
`P_PID=1` and `WEXITED|WNOHANG|WNOWAIT=0x25`. Zero PID means no exit observed.
Accept exit only for that PID, `SIGCHLD`, zero `si_errno` and an exited/killed/
dumped child code (1–3). System errors and unexpected results are failures;
interruption must not introduce an unbounded retry. Never derive the final exit
code from this structure: the existing bounded final `process.wait` supplies it.

Route all three observation sites, including exceptional cleanup, through this
observer. Retain the unreaped leader until every group signal and Darwin
membership proof finishes. Preserve fresh session/group ownership, concurrent
pipe limits, stdin policy, cancellation, deadlines, TERM grace, two-second
cleanup budget and failure classification. No poll/reap-before-signal fallback.

Update existing trusted pins and ordinary source/installed records using the
current delivery machinery. Audit shipped Python entry points for 3.12-only
failures and repair any found without new interfaces or relaxed checks. The
plan names those entry points and existing test homes before implementation;
new boundary design returns to High. Preserve all three platforms equally.

## Rationale

The native function provides exactly the non-reaping observation the supervisor
already requires. Reusing that supervisor avoids a second lifecycle, process or
event loop. Its small ABI binding is the additional maintenance cost.

## Alternatives considered

Keeping the refusal violates the Maintainer's 3.12 direction. `kqueue` alone
misses children exiting before registration, as measured. Polling reaps the
leader and risks signalling a reused group ID. A sentinel worker adds process,
startup and cleanup machinery to every read. Neither is needed for an existing
system `waitid` call.

## Documentation / doctrine surface

Correct README's 3.13-only guidance and affected runtime/safety descriptions,
without narrowing the existing runtime policy in
`docs/methodology/runtime-contract.md`. Keep certification on canonical 3.13.
Extend the existing release note; no new doctrine or ceremony.

## Evidence / verification plan

### Tests required

Use `bootstrap/tests/security/test_git_read.py` public `run_git` workflows for
ordinary completion, timeout, quiet descendant cleanup, overflow and cancellation
on actual macOS 3.12; retain unsafe-executable and failed-cleanup refusals. Add
only uncovered promise classes in existing parameterized homes, including
unavailable/malformed native observation. A native-binding failure must not
become success or leave an owned child alive.

Run equivalent affected public controls on actual Linux and Windows 3.12,
recording interpreter/platform separately. Reuse existing install/upgrade and
installed-tool workflow checks for the shipped-entry-point inventory; successful
imports or `--help` alone do not establish runtime compatibility. Keep current
pin/twin controls. Scratch primitive probes remain developmental evidence.

### Examples / smoke checks

Exercise real session startup in a disposable Git checkout on macOS 3.12.
Use changed-file selections and existing final wide integration on canonical
3.13; full release certification remains separate. No new compatibility runner.

#### Security preflight — five questions, answered in writing

1. Trusted helper bytes choose the fixed system library and observer; target
   files supply no executable path, ABI or PID authority.
2. The native primitive succeeded and the competing late-registration probe
   failed. Timeout/descendant and unavailable-binding falsifiers remain unrun.
3. Public `run_git`, scaffold and installed-tool commands fire the planned
   checks; the plan maps their inputs to existing documented contracts.
4. Missing APIs, malformed observations and incomplete cleanup refuse; they
   grant no additional execution, comparison or write authority.
5. A compromised host/library or process deliberately escaping the owned group
   remains outside the existing trusted-host cleanup contract.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Any surviving owned descendant, reused-group signal, false completed result,
3.12 workflow failure or Linux/Windows regression leaves the work unfinished.

## Scope delta

**Scope delta**: new compatibility scope; no accepted SafeGit outcome removed.

## Assurance path

**Assurance path**: high-assurance

## Review -- GPT-6.1 Terra (Reviewer) -- 2026-11-12

Reviewed commit: c2b9fbc8

**Tier**: usual
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: approximately five minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: restoring actual 3.12 workflows while retaining bounded process cleanup addresses the startup failure without relaxing the existing contract -- `tools/git_read.py:756`; proposal Tests required.
2. **Best alternative.** Keep the current refusal: it avoids a native binding but leaves the requested macOS 3.12 use broken; the proposed observer reuses the existing supervisor -- `tools/git_read.py:889` and proposal Rationale.
3. **What would show it wrong?** A 3.12 public workflow leaving an owned descendant or reporting success on malformed observation would falsify the proposal -- proposal Tests required and Signals.

**Audience:** Runtime guidance belongs in README and descriptive safety documents; the proposal retains the runtime contract and agent duties. **Coverage:** Read the proposal, the existing supervisor's refusal and three observation sites, public test home, README and the temporary primitive probe source. The recorded native results are author-reported, not independently rerun; the probe does not establish cleanup or full workflows. Did not verify the ABI independently, run native probes or tests, review all shipped entry points, perform Security Review, or make a Decision. High Security Review remains owed.

## Review -- GPT-6.1 Sol (Security Review, High) -- 2026-11-12

Reviewed commit: 6601ed7e

**Tier**: Security Review
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: approximately eight minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: restoring the missing non-reaping observation preserves the supervisor's ownership invariant while delivering the requested compatibility -- `tools/git_read.py:756`; proposal Proposal.
2. **Best alternative.** Keep one supervisor and bind the existing system primitive; polling loses the unreaped leader, while a sentinel adds another lifecycle -- `tools/git_read.py:975`; proposal Alternatives considered.
3. **What would show it wrong?** A malformed native observation accepted as completion, a signalled reused group, or a surviving owned descendant would falsify it; actual 3.12 public refusal/cleanup workflows remain required on every named platform -- proposal Tests required and Signals.

**Evidence:** Independently compared Apple's linked `signal.h`/`wait.h` and this host's SDK: field order, signal-value union, seven reserved longs, 32-bit PID/ID types, exit codes 1–3, `P_PID=1` and flags `0x25` agree. The stated 64-bit layout totals 104 bytes with PID at offset 12. Fixed-library loading, layout refusal before launch, exact owned PID, fresh zeroed storage and bounded error handling add no target-controlled authority. All three observation sites and final reap ordering are explicitly preserved. Existing `ctypes` use and the dependency budget require no runtime package exception. Linux observation and Windows Job isolation remain required outcomes, not waived checks.

**Coverage:** Read proposal, primitive-probe source, supervisor lifecycle, public test home, runtime contract and dependency budget. Did not rerun primitive probes, execute platform workflows, audit every shipped entry point or review implementation; the probe's reported success alone establishes none of those guarantees.

## Review response -- GPT-6.1 Terra (Coordination) -- 2026-11-12

Both independent reviews accept the proposal without findings. No operative
revision is needed. Actual Python 3.12 workflow checks, platform guarantees and
the shipped-entry-point audit remain required implementation outcomes, rather
than results inferred from the primitive probe. Ready for the Maintainer's
Decision; no implementation is authorized by this response.

**Elapsed:** approximately one minute. **Tokens:** unknown.
