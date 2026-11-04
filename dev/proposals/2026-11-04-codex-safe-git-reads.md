# One Safe Boundary for Git Reads

**Author**: Codex (Sol, high) -- Strategy / proposal author
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-04
**In brief**: Give repository inspection one shared safety boundary so project settings cannot run programs and failed checks cannot masquerade as clean results.

## Decision summary

Replace the duplicated Git read launchers with one standard-library helper in
an existing, always-installed file. Migrate ordinary readers together and
repair the edit-check failure below. This costs coordinated caller/test edits,
some executable-validation overhead, and one additional dispatcher digest
binding; it adds no package, general Git framework, or recurring ledger.

This proposes board **2d**, not implementation authority. Maintainer chat,
2026-11-04: "Prepare board2d proposal early while2a/b/cfoundationworkruns";
also: "Do NOTforgeDecisionorassumeexistingusersequenceapprovalacceptsyournewdesign."
The [delivery sequence](../strategy/2026-11-02-codex-v07-delivery-sequence.md)
likewise leaves child Decisions open.

## Context

The [security strategy](../strategy/2026-08-05-codex-security-strategy.md#1-one-shared-sterile-git-runner-for-untrusted-repositories-bnd-3--tru-6)
calls for one sterile runner: a launcher whose environment and command choices
do not let the inspected repository select programs. Current protections differ.
Upgrade caps reads and disables lazy fetching; content scanning resolves Git
outside the target and closes its environment; sweeps additionally revalidate
executable bytes and mediate adapter configuration. None alone is the whole
replacement contract ([upgrade](../../bootstrap/_scaffold/upgrade.py),
[scanner](../../scripts/content_scan_runner.py),
[sweeps](../../scripts/run_portable_security_sweeps.py),
[Safety Rules 5, 7 and 10](../../bootstrap/SAFETY.md)).

**N1, current evidence supplied by the Maintainer:** on committed `46c8a55f`,
Python 3.13.13, `_writeset_dirty_collisions` normally finds edited `A.md`.
Returning `_GIT_NOT_STARTED` only at config, HEAD, ls-files or diff-index gives
`[]` in each case; second-group startup failure also discards a first-group edit.
This is a collision-helper reproduction, not a fresh measured `--apply`
overwrite. The [historical author review](../plans/archive/upgrade-edit-check-no-repository-programs.md)
measured an actual overwrite with self-deleting host Git, not a
candidate-caused executable. Its N2 linked-worktree and N3 version-only-hang
test gaps are included here, not deferred again. Current source still contains
the relevant `None` returns; I did not rerun that reproduction.

## Proposal

### One Home, Complete Migration

Put the low-level read helper in
[`templates/skills/_lib/session.py`](../../templates/skills/_lib/session.py),
mirrored byte-for-byte to [`tools/session.py`](../../tools/session.py).
`_SKILLS_MAPPINGS` in [config](../../bootstrap/_scaffold/config.py) already
installs it unconditionally and verbatim; [install](../../bootstrap/_scaffold/install.py)
already records its digest. Retire duplicate process/env loops, retaining only
caller-specific parsing and result translation. No new module or `unsafe=True`.

The source search found this ordinary read population, including indirect and
generated callers; mirrored template/self-hosted copies follow their existing
packaging, not independent policies:

| Existing owner | Reads to route |
|---|---|
| [upgrade](../../bootstrap/_scaffold/upgrade.py) | `_run_git_sterile` / `_git_in_project`, edit prelude/index/comparison, committed-copy check; source-checkout discovery and both ref-selected template/blob reads |
| [install](../../bootstrap/_scaffold/install.py), [lockfile](../../bootstrap/_scaffold/lockfile.py) | Target interpreter-admin discovery; source provenance/status, `_cairn_commit`, `_behind_by_n` |
| [session](../../tools/session.py) | Root discovery, `_git` history/status, tracked-interpreter gate, `_git_binding_path` discovery |
| [intent conflict](../../tools/_intent/conflict.py), [hooks](../../tools/_intent/hooks.py) | Ordinary `_git_path` discovery, staged paths/rename map; generated pre/post-commit diff, diff-tree and HEAD reads, moved into the existing Python handlers |
| [content runner](../../scripts/content_scan_runner.py) | Resolved-binary tracked-root query and its environment |
| [portable sweeps](../../scripts/run_portable_security_sweeps.py) | Git version, common-dir/config/reachability discovery and transitive adapter Git; retain screen, admission and reduced-mode controls |
| [link checker](../../scripts/link_check.py), [snippet checker](../../scripts/sync_doc_snippets.py), [self-check](../../scripts/check_cairn.py) | Root/tracked Markdown discovery, including self-check's delegated shipped link checker |
| [measurements](../../scripts/measurements.py), [gauge](../../tools/gauge.py), [tier selector](../../tools/test_tiers.py), [legacy report](../../scripts/gen_legacy_code_review_passes.py) | Commit counts, history/numstat/date, changed-passage diff, committed artifact tree/blob reads |

**Different authority, not omitted ordinary readers:** hook install/uninstall
discovery deliberately honors `core.hooksPath` to place executable hooks; isolate
that trusted write-related query from ordinary `_git_path`, without weakening
the read helper. [merge-file](../../bootstrap/_scaffold/merge.py) operates on
engine-created temporary inputs, not a target repository. The release
[security checker](../../bootstrap/security_check.py),
[repin](../../scripts/repin.py), [re-anchor Python driver](../../scripts/reanchor_ceremony.py),
[shell driver](../../bootstrap/reanchor.sh),
[anchored launcher](../../bootstrap/reanchor-launcher.template.sh) and protected
gate readers must retain independently trusted extraction/signing/ref-transaction
runners, never import candidate authority. The [ref verifier](../../bootstrap/container/verify-ref.sh)
and [publication check](../../scripts/check_release_publication.py) deliberately
use separately authorized fetch/signature or remote-publication boundaries.
[Container acceptance](../../bootstrap/container/acceptance.sh),
[floor gate](../../bootstrap/container/floor-gate.sh), and the
[Windows evidence runner](../../scripts/run_windows_interpreter_binding.py)
inspect their own trusted build/test checkout and create/run fixtures, not
arbitrary adopter targets. Test fixture Git setup is likewise not production
inspection. These runners are not merged into an offline read API.

### Read Contract

Resolve host Git to an absolute executable regular file; reject both lexical
and resolved locations inside the inspected worktree, including current-directory
and relative-PATH selection. Root discovery must exclude the enclosing worktree,
not merely its starting subfolder. Revalidate path/content immediately before
each launch, reusing the sweeps' treatment; bind cached version results to that
executable identity. This is containment, not host provenance.
Load the helper only from fixed, checked paths relative to the trusted running
Cairn tools/source, never from the target's tool directory when inspecting it
externally. Keep import-time behavior standard-library-only and self-contained
so repin's extracted anchor-session encoder acquires no candidate dependency.

Use source-owned read command forms and argv data, never shell commands or
repository-supplied command/options. Scrub every inherited `GIT_*` through a
closed host-minimum environment; own `GIT_CONFIG_NOSYSTEM`, null global/system
configuration, no prompt, optional locks, replacement objects or lazy fetch.
Disable hooks, fsmonitor, pagers, signature display, external diff and textconv;
deny every transport, including per-protocol overrides and remote helpers.
Preserve literal pathspecs and `--` for paths; validate revisions and use option
terminators where supported. Object-consuming operations retain the existing
2.45.0 lazy-fetch prevention floor; discovery/index-only old-Git cases remain
available only where prevention is demonstrated, not guessed.

Status cannot simply inherit the old call: first read bounded configuration
without executing it and neutralize every configured clean/process filter driver
(including required-driver behavior) before status. Preserve staged/untracked
reporting; document conservative dirty reports where removing a filter changes
comparison semantics. Keep sweeps' stronger include/origin/key screen, not just
its counted overrides. Reuse its existing off-tree Git shim mechanism for
adapter reads through this same helper, with fixed trusted interpreter/helper/
real-Git paths and bounded approved read forms; do not expose the original
Git directory as a bypass. Keep reduced mode Git-free.

Bound time and stdout/stderr bytes while reading, including version/config
probes; kill/reap the child and clean pipes, readers, temporary shims and any
permitted descendants on timeout/overflow. Escape diagnostics. Neither config
overrides nor screening freeze the filesystem or contain a malicious host.

Return distinct absence, failed/incomplete, and completed-command outcomes.
Present-but-invalid executables are failure, not absence.
Never turn failure into a clean scan, empty measured history, or successful
edit check. Retain the intentional upgrade no-Git prelude: no repository or Git
unavailable before worktree confirmation means no guard. **After confirmation,
every later startup failure is `_EditCheckCannotTell`, including later groups.**
Apply and bare finalize refuse without changing bytes; stage advises. Existing
explicit `--force` behavior stays caller-owned, never a helper escape hatch.

## Rationale

An always-installed home avoids another module/install group. The necessary
consumer change is adding `tools/session.py` to content-security's existing
`additional_immutable_paths` in the
[dispatcher](../../templates/modules/default-on/run_security_verification.py),
so all six apparatus members bind before launch. Preserve lockfile schema,
manifest/parity contracts and anchored-reader isolation. Recurring cost is
maintaining that binding, mirrored bytes and affected controls, not a new audit
routine. Runtime overhead requires measurement; no estimate is yet available.

## Alternatives considered

**Least involved credible repair:** fix N1 and add N2/N3 in the existing upgrade
test home. It is cheaper to build/run/review but leaves duplicated boundaries
and does not enable safe 7d/8a Git inspection. Doing nothing also leaves N1.
**Copy stronger settings into every caller:** avoids a shared dependency but
keeps repeated executable-resolution/cleanup fixes and their maintenance cost.
**New Git package/universal wrapper:** simplifies import routing but adds install
and trust machinery without a needed capability. Recommendation: reuse session's
existing delivery seam and migrate the complete ordinary population.

## Documentation / doctrine surface

Governing layer: retain [AGENTS](../../AGENTS.md) obligations and mirror any
necessary operative clarification in its shipped template; no lifecycle change.
Deliberation: this proposal and its eventual reviewed plan; parent owns board/
changelog. Descriptive layer: update [tool usage](../../docs/tool-usage.md) and
[upgrade description](../../bootstrap/UPGRADE.md), with domain-local safety
contract corrections in [SAFETY](../../bootstrap/SAFETY.md), notably Windows bare
Git lookup and post-confirmation failure. Route these three levels under the
[documentation plan](../../docs/DOCUMENTATION_PLAN.md), without duplicating policy.

## Evidence / verification plan

### Tests required

Use existing `bootstrap/tests/` owners, not another harness. In
[`test_upgrade_edit_check_runs_no_project_programs.py`](../../bootstrap/tests/test_upgrade_edit_check_runs_no_project_programs.py),
extend `test_git_that_cannot_start_or_does_not_answer_at_any_step_is_no_guard_or_cannot_tell`
and `test_a_failure_in_a_later_group_is_cannot_tell`: N1 regression must fail on
current code, find an edit in the first group, and cover config/HEAD/index/diff
startup failures through collisions and real apply/finalize/stage entry points.
Retain no-Git success controls and byte-preservation assertions. N2 adds a real
linked-worktree `.git`-file edit control; changing `lexists` to `is_dir` must fail
it. N3 hangs **only** version, with later questions functional; ignoring the
version no-answer must fail it. Keep mutations repeatable in these tests.

Extend existing owners:
[`test_session_kernel.py`](../../bootstrap/tests/test_session_kernel.py),
[`test_git_interpreter_binding_portable.py`](../../bootstrap/tests/test_git_interpreter_binding_portable.py),
[`test_intents_tool.py`](../../bootstrap/tests/test_intents_tool.py),
[`test_security_stack.py`](../../bootstrap/tests/test_security_stack.py)'s
`TestRunnerGitBoundary`,
[`test_portable_security_sweeps.py`](../../bootstrap/tests/test_portable_security_sweeps.py),
[`test_security_verification.py`](../../bootstrap/tests/test_security_verification.py)'s
apparatus-failure controls, [doc-drift tests](../../bootstrap/tests/test_doc_drift_tools.py),
[count tests](../../bootstrap/tests/test_verify_counts.py), and
[reference-script parity](../../bootstrap/tests/test_reference_scripts.py).
Cover each inventoried entry point, installing actual shipped layouts; extend
the nearest existing owner for presently uncovered gauge/report/tier readers.
Add no test file merely to centralize routing. Include target-local executable,
PATH/symlink swap, inherited-env redirection, hooks/filter/fsmonitor/signature,
missing-object/remote-helper, option/path injection, version-only hang,
overflow and cleanup controls. Prove each tripwire can observe its planted
effect before trusting absence; mutate each routing member separately in
isolated copies. Native Windows and real old-Git evidence must be named, not
inferred from stand-ins.

### Examples / smoke checks

The accepted-if-decided scope includes installation/upgrade, session discovery,
both intent hooks, direct/dispatcher content scan and sweep discovery/history.
Plan maps changed-file readers using `tools/test_tiers.py for`; after ordinary
and Security code review, run **wide Boundary B** on a clean final commit with
canonical Python 3.13.x. No whole-tree certification for proposal authoring.
Prose gates are claim, `scripts/check_cairn.py` (links/content), snippet check and
neutrality, invoked by the author, not blocking CI. Git-backed board 7d trial
and 8a views wait for this verified boundary in the approved sequence;
filesystem views proceed. No unsafe fallback or indefinite pilot deferral.

#### Security preflight -- S1-S5

**S1 -- supplier:** target files, config/includes, refs/objects, paths, pointer
administration and scan roots are target-controlled, including by reference.
Host PATH/environment and executable bytes come from the operator; trusted
running source owns commands, limits, helper location and dispatcher bindings.
Target lockfile digests detect drift, not authenticity against joint rewriting.

**S2 -- falsifiability:** restore N1's `None`; ignore version no-answer; replace
`lexists` with `is_dir`; remove one environment/executable/command guard or one
dispatcher binding: the corresponding controls above must fail. These proposed
mutations have **not** been run; N1's supplied reproduction and historical
N2/N3 survivors are evidence of the present gap, not new-helper assurance.

**S3 -- trigger/set:** manual adopter commands above reach only their named
target read forms; mapped pytest selections exercise the complete inventory
and six-member content apparatus. Proposed adopter wording: "Repository reads
run only the validated host Git under bounded, noninteractive, offline
settings; an unanswered check is not a clean result." Existing test/gate
consumers were opened; no commit hook or CI is claimed to enforce this design.

**S4 -- failure direction:** absent Git remains distinct from execution failure;
only upgrade's pre-confirmation no-guard path retains permission to proceed.
Malformed output, old unsupported Git, unsafe executable, missing binding,
timeout and overflow refuse/degrade/advisably report inability according to the
caller, never authorize protected writes or claim measured cleanliness.

**S5 -- residual winner:** repository-controlled programs must not run, but
malicious host Git, compromised trusted source, or a same-user filesystem race
can still win. Git-admin interpreter binding remains operationally trusted as
Safety states. Command/config coverage is reviewed enumeration, not a sandbox
or proof against future Git execution features.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A migrated caller executes a planted program/remote helper, misses its positive
control, reports failure as clean, loses a listed read capability, or lets target
code supply the helper. Such evidence keeps implementation open; if session's
home requires candidate imports in an anchored ceremony, reject that routing.

## Scope delta

**Scope delta**: preserved -- opening scope, including N1-N3; no accepted scope
is removed and no Decision is recorded.

## Assurance path

**Assurance path**: high-assurance

New execution boundary, scaffold, interpreter binding, portable sweeps,
dispatcher and install consumers require heavy treatment. Ordinary proposal
review plus separate Security Review precede a Maintainer Decision; an accepted
plan then needs Internal and Internal Security Review before implementation.
Coordinate the session edit with 2b/2c/8b; no reassignment of their work.

Authoring record: elapsed unknown; tokens unknown. Opening exceeds the soft
target to retain the caller/authority inventory and load-bearing security
contract. Python 3.13.13 author checks: `scripts/claim_check.py` and
`scripts/check_cairn.py` on this file passed (one Markdown file, no issues);
`scripts/sync_doc_snippets.py --check` passed (one document, no drift);
`scripts/quality_gate.py --sub neutrality` passed (zero failures, 43 informational
items; its standing scan excludes this deliberation file). The tier selector
selected zero test files. Exact new-path/stem searches found no direct test
reader or byte pin; the same search reached the known-positive content-runner
test references. No pytest, mutations, native Windows/old-Git checks, network,
implementation, re-anchor or release certification was run. Those implementation
proofs remain owed if this design is accepted.
