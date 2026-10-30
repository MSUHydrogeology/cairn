# Plan: Bind the interpreter in per-worktree Git administration

**Source proposal**: dev/proposals/archive/2026-10-29-codex-git-interpreter-binding.md
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Assurance path**: high-assurance
**Opened**: 2026-10-30
**In brief**: Store each worktree's interpreter choice in its Git administration instead of project content.

## Source proposal

The accepted contract relocates the executable selection from checkout content
into trusted per-worktree Git administration, without migrating the old file.
It preserves explicit rebinding, records copied administration as a residual
trust assumption, and requires native Windows evidence.

## Scope

Change the installer, session resolver and shipped copies, their consumers and
owning tests; retain the legacy ignore rule. The reviewed reader, writer and
shipped-copy inventory is in `dev/plans/2026-10-30-git-interpreter-binding/coverage.md`. Update `AGENTS.md`, its shipped equivalent,
`bootstrap/UPGRADE.md` and `bootstrap/SAFETY.md`, including rebinding and the
copied-administration and delivered-pointer residual. Same-user races and
executable provenance remain outside the boundary. No scientific check applies.

**Reuse.** Searching `tools/session.py` and `bootstrap/_scaffold/install.py`
for `local-env`, `local_env` and `interpreter` found `_resolve_interpreter`,
`write_local_env`, existing path and tracked-executable checks; reuse or adapt
them and the existing scrubbed Git invocation where applicable. The inventory records the search and maps its hits to checks.

### Documentation / doctrine surface

`AGENTS.md` and its shipped equivalent carry governing instructions; safety and
upgrade guides describe operation. Route changes under
`docs/DOCUMENTATION_PLAN.md`. Do not change other doctrine without establishing
its evolution trigger and recording the evidence.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Relocate discovery, reading and writing; update guidance and tests | Both plan reviews | Installer and session paths, shipped copies, docs and portable tests |
| C2 | Verify final implementation and hand to code review | C1 complete; native Windows evidence | Wide change-specific record and review handoff |

## Acceptance criteria

### C1

Discovery uses a scrubbed Git environment and requires the supplied root to be
the exact worktree root. Normal, linked, separate-directory and submodule
repositories work independently. Non-repository and nested targets install
without a binding, report this and give Git initialization and rerun guidance;
session falls back with guidance. Discovery errors and unsafe state refuse.
Never read or migrate the legacy file. Only true absence falls back; dangling
links, reparse points, wrong types and unreadable state refuse before launch.
Preserve schema, executable-shape, tracked in-project executable and warned
stale-executable behavior. Writes stay inside verified per-worktree
administration through a dedicated guard; unsafe destinations cannot be
clobbered even with force. Existing safe bindings survive unless forced. Do
not relax the target-tree guard. Guidance explains that copied administration
or a delivered pointer can supply a binding and must be trusted or rebound.

S2: a marker test through the real entry point detects deliberate redirection
to the legacy file; record control and mutant outcomes. S3: mapped tests and
gates below exercise the revised guidance and implementation.

### C2

Record clean tested commit, range, canonical interpreter, pre/post state,
commands, counts, timing, non-pass dispositions and omissions. Native Windows
must demonstrate discovery and junction/reparse handling before acceptance;
name any unsupported link case and leave a required unchecked case open. Hand
implementation and evidence to independent usual and Security code reviews.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A runs the mapping while iterating; Boundary B repeats it on the final
clean committed tree under canonical Python 3.13 in **wide** mode for the
trust boundary, with `Certified by: pending`. Split selections within the
pytest guard's file limit and reconcile their union. No full certification run
is authorized by this plan.

* Add and run `python -m pytest bootstrap/tests/test_git_interpreter_binding_portable.py`
  (proposed), including the control and deliberate legacy-redirection mutant.
  The inventory maps the entry points, layout, link, refusal, force and
  containment cases and the same native Windows command and required cases.
* Run owning families `bootstrap/tests/test_session_binding_untracked.py`,
  `bootstrap/tests/test_session_binding_gate_and_printing_hold.py`,
  `bootstrap/tests/test_session_kernel.py`, `bootstrap/tests/test_session_failsafe.py`,
  `bootstrap/tests/test_session_writes_contained.py`,
  `bootstrap/tests/test_install_module.py`, `bootstrap/tests/test_skills_install.py`,
  `bootstrap/tests/test_skills_security.py`, `bootstrap/tests/test_security_leaf.py`
  and `bootstrap/tests/test_security_stack.py`, plus
  `bootstrap/tests/test_claim_check_module.py` for the exclusion consumer.
* Run `python scripts/claim_check.py` on changed documents,
  `python scripts/check_cairn.py`, `python scripts/link_check.py`,
  `python scripts/quality_gate.py --sub neutrality --sub redundancy`, and
  `python -m pytest bootstrap/tests/test_security_lint.py` for the engine
  security lint; a skip does not satisfy it. Run snippet sync if a synced source
  changes. Preserve applicable frozen-file and AST re-anchor ceremonies; do not
  compare against a historical anchor as change verification.

Boundary C independently falsifies the reviewed change and verification record;
its reviewer records bounding and a targeted ledger, without running the full
suite.


## Plan review -- Codex gpt-6.1-sol -- 2026-10-30

```
Reviewed commit: 49e6a59123b88bf954d1b5ee4e7a6a6ba2b0fc05
Target: opening plan and accepted proposal contract
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** The outcomes follow the Decision, but the test and consumer mapping must be finished before implementation so this review can assess its coverage -- plan Scope and Verification; `dev/plans/_template.md` > Verification.
2. **Best alternative.** Keep the two chunks, but complete the reference inventory and map affected consumers to checks now; this preserves all accepted outcomes without another implementation chunk -- plan Sequence and Verification.
3. **What would show it wrong.** A no-repository install changes an ancestor binding, an unsafe path launches or escapes containment, or a required native Windows case cannot be demonstrated -- plan Acceptance criteria C1–C2.

**P1 -- blocking: finish the reviewed verification mapping.** Scope defers the reference inventory until implementation, and Verification adds unspecified “readers found by inventory.” The template requires the mapping before implementation, and the accepted proposal requires readers, writers and consumers mapped in the plan. The named families and behavioral list do not establish which existing consumers or shipped copies are covered, nor the commands that exercise the new entry-point and mutation checks. **Satisfier:** run the stated inventory against the committed tree, account for affected readers and shipped copies, and name their test files or nodes and executable commands (including the control and mutant check); identify any uncovered surface and its required check. This retains the accepted scope and lets the author respond without another plan review.

**Coverage:** accepted contract and Decision, repository-less and nested targets, supported Git layouts, refusal and native Windows acceptance: plan C1–C2 and proposal Current contract; verification and lifecycle: plan Verification and `dev/plans/_template.md`. **Not covered:** no implementation or native Windows evidence exists; no tests were run. The separate Internal Security Review remains open.


## Plan review -- Codex gpt-6.1-sol Security -- 2026-10-30

```
Reviewed commit: 0399dc783d47fa1ee8c372c16da66f15a40e6684
Target: operative plan and accepted Current contract
Prior findings: none for this obligation
Assurance path: high-assurance
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** The plan preserves the accepted authority boundary and Windows acceptance fence, but its security cases need a reviewed executable mapping before implementation -- plan C1–C2 and Verification; source proposal Current contract.
2. **Best alternative.** Retain the two chunks and dedicated administration guard; finish the security mapping rather than weaken the existing target-tree guard or omit supported layouts -- plan Sequence and C1; `bootstrap/_scaffold/install.py::write_local_env`.
3. **What would show it wrong.** An ordinary Git pointer is rejected, a filesystem link redirects binding access, an unsafe forced write escapes administration, or an untested required Windows case is accepted -- source proposal Current contract; plan C1–C2.

The strongest feature is separation of delivered content from a local executable
choice without silently migrating the old authority. The plan correctly keeps
copied administration and delivered Git pointers as explicit trust assumptions;
this relocation does not authenticate either administration or the executable.

**S1 -- blocking: map the security boundary to discriminating checks.** The
Verification list names broad families and “unsafe destinations,” but does not
map the accepted distinction between a regular Git pointer and a filesystem
link or reparse point in that pointer or its binding path. A final-file-only
check would miss an unsafe ancestor; a blanket external-path refusal would
break linked, separate-directory and submodule support. The accepted Current
contract explicitly requires both sides. Existing security helpers are not
proof of the future path: `tools/session.py::_binding_git_env` scrubs overrides,
while `bootstrap/_scaffold/install.py::write_local_env` currently writes under
the checkout guard. **Satisfier:** extend P1's reviewed mapping with exact test
files/nodes and commands through both real entry points, distinguishing valid
regular pointers from linked/reparse pointer and binding-path components,
true absence from dangling/unreadable/wrong-type state, and hostile discovery
from non-repository/nested targets. Map force and non-force containment and
no-launch assertions, independent worktree bindings, and the legacy marker
control/mutant command. Name the native Windows command and required
junction/reparse cases; an unavailable required case stays open as C2 already
requires. Proposed tests may be identified as such. This specifies the accepted
checks and removes no outcome.

**Coverage:** claims/design/fail-closed behavior: C1 and S1; production paths
and reuse: the two reader/writer helpers cited above and the plan's named
entry points; consistency/drift: source proposal Current contract against plan
Scope and C1–C2; lifecycle: separate Security obligation and C2's Windows fence;
scope/scientific validity: accepted residuals preserved, no scientific surface;
satisfier: S1. **Not covered:** no implementation exists, and no tests or native
Windows probes were run during active certification. Same-user races and
executable provenance remain outside the accepted boundary. Existing P1 also
remains for the author's response; this pass does not clear it.


## Response to plan review -- Codex gpt-6.1-sol -- 2026-10-30

| Finding | Disposition |
|---|---|
| P1 | Accepted. Scope and Verification point to the completed inventory and executable mapping in `dev/plans/2026-10-30-git-interpreter-binding/coverage.md`, including shipped copies, uncovered portable tests and control/mutant command. |
| S1 | Accepted. The inventory specifies pointer versus filesystem-link cases, absence and refusal, hostile discovery, force containment and no-launch checks, worktree isolation and native Windows junction/reparse evidence. |

## Implementation verification -- Codex GPT-6 -- 2026-10-30

**Boundary B mode**: wide. This changes a trust boundary and user-facing
installer/resolver paths. The clean run covered the portable real-entry-point
control/mutant, Git layouts and worktree isolation, refusal and containment,
binding consumers, tracked-executable checks, installed copies, security
families, claim-check exclusions, and required prose gates.

**Certified by**: pending

**Tested commit**: `dadb4e404559f12bb74bb2031d70737d5d908d46`

**Reviewed range**: `49e6a59123b88bf954d1b5ee4e7a6a6ba2b0fc05`..`dadb4e404559f12bb74bb2031d70737d5d908d46`

**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13, pytest 9.0.3

**Pre-run state**: clean detached worktree at the tested commit.

**Post-run state**: clean detached worktree at the tested commit; only ignored test cache may have been created.

| Command | Exit | Outcomes | Elapsed |
|---|---:|---|---:|
| `python -m pytest bootstrap/tests/test_git_interpreter_binding_portable.py bootstrap/tests/test_install_module.py bootstrap/tests/test_session_binding_untracked.py bootstrap/tests/test_session_binding_gate_and_printing_hold.py bootstrap/tests/test_session_failsafe.py bootstrap/tests/test_session_kernel.py bootstrap/tests/test_skills_install.py bootstrap/tests/test_session_writes_contained.py bootstrap/tests/test_skills_security.py bootstrap/tests/test_security_leaf.py bootstrap/tests/test_security_stack.py bootstrap/tests/test_claim_check_module.py bootstrap/tests/test_security_lint.py` | 0 | 565 passed | 34.98s |
| `python scripts/check_cairn.py` | 0 | 198 Markdown files; no issues | 1.10s |
| `python scripts/link_check.py` | 0 | 198 Markdown files; no issues | 0.07s |
| `python scripts/quality_gate.py --sub neutrality --sub redundancy` | 0 | both fail=0; 43 neutrality and 1 redundancy informational notices | 1.03s |
| `python scripts/claim_check.py <each changed document>` | 0 | all five documents OK; existing allowlisted paths reported | <1s |

**Legacy assertion mapping**: tests that proved `dev/.cairn/local-env.json`
could not be replaced or reinterpreted through Git tracking, spelling aliases,
hard links, inode identity, or index flags enforced authority of the old
checkout file. That authority is the accepted changed behavior: the file is
never read or migrated. `test_legacy_checkout_file_is_never_read` and the
real-entry-point control/mutant now prove that boundary. Binding path links,
wrong types, dangling state, unreadable state, discovery failures and timeout
refusal are exercised against Git administration. The distinct promise that a
selected in-project executable tracked by Git is refused remains exercised by
the retained tracked-executable and submodule-executable tests. Existing
malformed/stale binding, terminal encoding, child framing, containment,
scrubbed Git invocation and warning behavior tests remain in the mapped run.

**Non-pass disposition**: none in the mapped run. The control passes without
launching the legacy marker; its deliberate redirection mutant launches the
marker and is detected by the same assertion.

**Known omissions and open criterion**: native Windows was not available.
Discovery and junction/reparse handling were therefore not demonstrated on
Windows; a POSIX skip is not accepted as evidence. C2 and the required Windows
acceptance criterion remain open, so this record does not assert
`Implementation verified at` and the plan remains `implementing`. No full-suite
certification, code review, or push occurred.

## Interim code review -- Codex GPT-6 -- 2026-10-30

**Reviewed commit**: `dadb4e404559f12bb74bb2031d70737d5d908d46`  
**Obligation**: Internal (interim)  
**Findings**: raised  
**Bounding**: WIDER RUN REQUIRED -- exercise malformed Git administration through the real resolver and demonstrate refusal before any sub-tool launch.

**Foundations**

1. **Does it do what it claims?** Not yet: malformed `.git` administration falls back despite C1 requiring discovery errors and unsafe state to refuse -- `tools/session.py::_git_binding_path` and the ledger below.
2. **Best alternative.** Keep the per-worktree design, but distinguish an absent repository from a failed discovery when a `.git` entry exists, as the installer already does -- `bootstrap/_scaffold/install.py::write_local_env`.
3. **What would show it wrong?** A malformed administration directory causes fallback and permits the caller to proceed; see the falsification ledger below.

**CR1 -- blocking: failed discovery with an existing `.git` directory falls back.** In `_git_binding_path`, Git's “not a git repository” response returns `None` even when an existing directory named `.git` is invalid. `_resolve_interpreter` then selects the current interpreter. The installer checks whether `.git` exists before classifying the same error as absence. This violates C1's distinction between a non-repository and discovery errors or unsafe state, and can allow a sub-tool launch after damaged administration. **Satisfier:** refuse this state at the resolver and cover it through the real entry point with an assertion that no sub-tool launches; retain the true-absence and nested-target behavior.

**Falsification ledger** (Python 3.13.13, isolated archive of the reviewed commit):

* Created an empty `.git` directory in a temporary root and called `_resolve_interpreter(root)`: returned `(current interpreter, 'fallback')` and emitted missing-binding guidance; this reproduces CR1.
* Ran `python -m pytest bootstrap/tests/test_git_interpreter_binding_portable.py -q`: 13 passed in 1.43s. The existing portable checks do not catch that invalid-directory case.
* Read the committed installer and resolver path guards and legacy-marker test: installer checks the `.git` entry before no-repository fallback; pointer and binding components are checked for links; the legacy control and mutant are covered by the portable test. These observations do not establish Windows behavior.

**Coverage:** reviewed the recorded wide verification and the committed discovery, fallback, pointer, binding write and legacy paths, with the targeted probe above. **Not covered:** native Windows discovery and junction/reparse behavior, independent execution of every mapped family, same-user races, executable provenance, or the separate Security Review. C2 remains open; this interim pass does not accept or complete implementation.

## Interim code review follow-up -- Codex GPT-6 -- 2026-10-30

**Reviewed commit**: `a41787a766a395e19eb17f69272bc0b396bb5fe1`  
**Obligation**: Internal (interim follow-up to CR1)  
**Findings**: no new defects found in this revision  
**Bounding**: ACCEPTED for CR1's malformed-administration case; C2 and final Boundary B remain open.

**Foundations**

1. **Does it do what it claims?** The changed guard refuses failed discovery with a present `.git` entry, while true absence and a nested root still fall back -- `tools/session.py::_git_binding_path`; falsification ledger below.
2. **Best alternative.** The small condition matching the installer's existing classification is sufficient; no additional path or abstraction improves this fix -- `bootstrap/_scaffold/install.py::write_local_env` and `git show a41787a7 -- tools/session.py`.
3. **What would show it wrong?** A malformed `.git` directory or regular pointer reaching a sub-tool, or an absent/nested root refusing, would break this result -- falsification ledger below.

**Falsification ledger** (isolated detached worktree at the reviewed commit; `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13):

* Ran `python -m pytest bootstrap/tests/test_git_interpreter_binding_portable.py -q`: 14 passed in 1.40s, including the new handoff-entry test. This is a control run, not the independent challenge.
* Through `_resolve_interpreter`, an empty `.git` directory raised `LifecycleError("git could not resolve the worktree root")`; a regular pointer to a missing administration directory raised `LifecycleError(".git pointer target could not be inspected")`. Neither fell back. The new test drives `session-end --prepare-handoff --dry-run` and asserts `_surface_intents` was not reached.
* In the same probe, a directory with no repository returned `fallback`, and a nested directory inside an initialized repository returned `fallback`. These challenge the changed condition's other branch. The worktree's tracked files remained clean after the probes.

**Coverage:** claims, production path, edge cases and fail-closed behavior: the guard, new test and ledger above; consistency and reuse: the installer's analogous branch at `bootstrap/_scaffold/install.py::write_local_env` and the plan's C1 contract; drift and lifecycle: the commit's stated CR1 fix and the still-open C2 criterion; scope and satisfier: this revision changes only `tools/session.py` and its owning portable test, satisfying CR1 without reducing accepted work (`git show --stat a41787a7`). **Not covered:** native Windows discovery or junction/reparse behavior, full mapped Boundary B checks on the final commit, same-user races, executable provenance, or the separate Security Review. The plan stays `implementing`.
