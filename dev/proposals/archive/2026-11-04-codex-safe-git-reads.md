# One Safe Boundary for Git Reads

**Author**: Codex (Sol, high) -- Strategy / proposal author
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-04
**In brief**: Give repository inspection one shared safety boundary so project settings cannot run programs and failed checks cannot masquerade as clean results.

## Decision summary

Replace the duplicated Git read launchers with one small standard-library file
using the existing unconditional delivery path. Migrate ordinary readers
together and repair the edit-check failure below. This costs coordinated caller/test edits,
executable-validation overhead, one installed file and pre-import byte bindings;
it adds no service, general Git framework, or recurring ledger.

This proposes board **2d**, not implementation authority. Maintainer chat,
2026-11-04: "Prepare board2d proposal early while2a/b/cfoundationworkruns";
also: "Do NOTforgeDecisionorassumeexistingusersequenceapprovalacceptsyournewdesign."
The [delivery sequence](../../strategy/2026-11-02-codex-v07-delivery-sequence.md)
likewise leaves child Decisions open.

## Context

The [security strategy](../../strategy/2026-08-05-codex-security-strategy.md#1-one-shared-sterile-git-runner-for-untrusted-repositories-bnd-3--tru-6)
calls for one sterile runner: a launcher whose environment and command choices
do not let the inspected repository select programs. Current protections differ.
Upgrade caps reads and disables lazy fetching; content scanning resolves Git
outside the target and closes its environment; sweeps additionally revalidate
executable bytes and mediate adapter configuration. None alone is the whole
replacement contract ([upgrade](../../../bootstrap/_scaffold/upgrade.py),
[scanner](../../../scripts/content_scan_runner.py),
[sweeps](../../../scripts/run_portable_security_sweeps.py),
[Safety Rules 5, 7 and 10](../../../bootstrap/SAFETY.md)).

**N1, current evidence supplied by the Maintainer:** on committed `46c8a55f`,
Python 3.13.13, `_writeset_dirty_collisions` normally finds edited `A.md`.
Returning `_GIT_NOT_STARTED` only at config, HEAD, ls-files or diff-index gives
`[]` in each case; second-group startup failure also discards a first-group edit.
This is a collision-helper reproduction, not a fresh measured `--apply`
overwrite. The [historical author review](../../plans/archive/upgrade-edit-check-no-repository-programs.md)
measured an actual overwrite with self-deleting host Git, not a
candidate-caused executable. Its N2 linked-worktree and N3 version-only-hang
test gaps are included here, not deferred again. Current source still contains
the relevant `None` returns; I did not rerun that reproduction.

## Proposal

### One Home, Complete Migration

Use `templates/skills/_lib/git_read.py` as one cohesive helper, separate from the
large, frequently edited session kernel (F2). Add its verbatim row beside
session/board in `_SKILLS_MAPPINGS`
in [config](../../../bootstrap/_scaffold/config.py); existing
[install](../../../bootstrap/_scaffold/install.py) machinery then covers its
manifest, lockfile digest, base cache and upgrade. Mirror only these two files:

Proposed paths:
- `templates/skills/_lib/git_read.py` -- canonical standard-library-only helper.
- `tools/git_read.py` -- byte-identical unconditional installed/self-hosted copy.

Retire duplicate process/env loops, retaining caller parsing/result policy.
No service, helper-discovery registry, universal Git API or `unsafe=True`.

The source search found this ordinary read population, including indirect and
generated callers; mirrored template/self-hosted copies follow their existing
packaging, not independent policies:

| Existing owner | Reads to route |
|---|---|
| [upgrade](../../../bootstrap/_scaffold/upgrade.py) | `_run_git_sterile` / `_git_in_project`, edit prelude/index/comparison, committed-copy check; source-checkout discovery and both ref-selected template/blob reads |
| [install](../../../bootstrap/_scaffold/install.py), [lockfile](../../../bootstrap/_scaffold/lockfile.py) | Target interpreter-admin discovery; source provenance/status, `_cairn_commit`, `_behind_by_n` |
| [session](../../../tools/session.py) | Root discovery, `_git` history/status, tracked-interpreter gate, `_git_binding_path` discovery |
| [intent conflict](../../../tools/_intent/conflict.py), [hooks](../../../tools/_intent/hooks.py) | Ordinary `_git_path` discovery, staged paths/rename map; generated pre/post-commit diff, diff-tree and HEAD reads, moved into the existing Python handlers |
| [content runner](../../../scripts/content_scan_runner.py) | Resolved-binary tracked-root query and its environment |
| [security audit](../../../templates/modules/team-gated/run_security_audit.py) | Pre-import binding of that runner's helper before the injection pass; no new Git command family |
| [portable sweeps](../../../scripts/run_portable_security_sweeps.py) | Git version, common-dir/config/reachability discovery and transitive adapter Git; retain screen, admission and reduced-mode controls |
| [link checker](../../../scripts/link_check.py), [snippet checker](../../../scripts/sync_doc_snippets.py), [self-check](../../../scripts/check_cairn.py) | Root/tracked Markdown discovery, including self-check's delegated shipped link checker |
| [measurements](../../../scripts/measurements.py), [gauge](../../../tools/gauge.py), [tier selector](../../../tools/test_tiers.py), [legacy report](../../../scripts/gen_legacy_code_review_passes.py) | Commit counts, history/numstat/date, changed-passage diff, committed artifact tree/blob reads |

**Different authority, not omitted ordinary readers:** hook install/uninstall
discovery deliberately honors `core.hooksPath` to place executable hooks; isolate
that trusted write-related query from ordinary `_git_path`, without weakening
the read helper. [merge-file](../../../bootstrap/_scaffold/merge.py) operates on
engine-created temporary inputs, not a target repository. The release
[security checker](../../../bootstrap/security_check.py),
[repin](../../../scripts/repin.py), [re-anchor Python driver](../../../scripts/reanchor_ceremony.py),
[shell driver](../../../bootstrap/reanchor.sh),
[anchored launcher](../../../bootstrap/reanchor-launcher.template.sh) and protected
gate readers must retain independently trusted extraction/signing/ref-transaction
runners, never import candidate authority. The [ref verifier](../../../bootstrap/container/verify-ref.sh)
and [publication check](../../../scripts/check_release_publication.py) deliberately
use separately authorized fetch/signature or remote-publication boundaries.
[Container acceptance](../../../bootstrap/container/acceptance.sh),
[floor gate](../../../bootstrap/container/floor-gate.sh), and the
[Windows evidence runner](../../../scripts/run_windows_interpreter_binding.py)
inspect their own trusted build/test checkout and create/run fixtures, not
arbitrary adopter targets. Test fixture Git setup is likewise not production
inspection. These runners are not merged into an offline read API.

### Delivery and Pre-import Binding

**SR1:** helper code comes from the caller's trusted delivery root, never CWD,
`--root`, the inspected target, its lockfile's `src`, or an import search path.
Source engine/template callers use the fixed source-layout path under
`templates/skills/_lib/`; self-hosted `scripts/`/`tools/` and installed callers
use their fixed delivery-root `tools/` path. Layout is determined from the
trusted caller's known packaged location, not by searching the target or
trying an existence-based fallback. Each first importer owns a small stdlib
load gate; delegated consumers pass the already-bound helper, not a target root
from which to find code. Repin's anchor-session extraction stays self-contained:
no top-level helper import and no change to its privileged Git runner.

The **expected bytes** are supplied by a literal SHA-256 pin embedded in that
trusted importing caller's reviewed source. Implementation takes the pin from
the reviewed canonical helper; existing parity/install tests check every such
pin and both delivered copies. Runtime never learns the expectation by hashing
the candidate helper, reading an adjacent digest, or accepting target metadata.
Before any helper import, reject missing files, linked/reparse components,
non-regular or oversized files and mismatched pins; read once and compile/execute
exactly those verified bytes. Do not reopen the path, use bytecode caches, or
reuse an unverified cached module. This pins the dependency to trusted caller
code; authenticity of that caller still comes from the existing trusted
distribution/checkout assumption, not from this helper.
Required install records below come from that delivery root's fixed lockfile;
an external target's records cannot choose code or supply the expected pin.

| Launch path | Binding before helper execution |
|---|---|
| Default dispatcher | Add `tools/git_read.py` to content-security's fixed `additional_immutable_paths`; parent binds all six apparatus records before child launch; child's trusted runner also enforces its embedded helper pin before import. |
| Python-security audit | Add helper to the content apparatus in `_MODULE_APPARATUS`; `integrity_preflight` checks its fixed record/path before `_load_runner`/injection. The runner's own pin gate still runs before helper execution; the later adopted-executable gate is not the protection. |
| Direct content/sweep self-audit | Trusted caller gate checks its embedded helper pin and the fixed helper's installed lock record before import; missing records, tamper or links refuse/degrade, not fall back to an unbound import. |
| Other ordinary source/installed readers and sweep shim | Their trusted first importer checks its embedded pin against its fixed delivery path; shim receives the verified helper bytes and fixed host interpreter/Git, not a target-selected helper path. Existing caller-specific lock checks remain. |

Direct self-audit remains **advisory on an operator-trusted code tree**. A
joint rewrite of installed caller, helper and lockfile can still pass; neither
the added record nor a pin inside that rewritten caller authenticates its own
mutable tree. External inspection instead runs the separately trusted caller and
helper delivery against a distinct target. No fallback imports a target's
`session.py`, `git_read.py`, or a substituted `candidate_session.py`.

### Read Contract

Resolve host Git to an absolute executable regular file; reject both lexical
and resolved locations inside the inspected worktree, including current-directory
and relative-PATH selection. Root discovery must exclude the enclosing worktree,
not merely its starting subfolder. Revalidate path/content immediately before
each launch, reusing the sweeps' treatment; bind cached version results to that
executable identity. This is containment, not host provenance.
The pre-import contract above applies before even a version probe.

Use source-owned read command forms and argv data, never shell commands or
repository-supplied command/options. Scrub every inherited `GIT_*` through a
closed host-minimum environment; own `GIT_CONFIG_NOSYSTEM`, null global/system
configuration, no prompt, optional locks, replacement objects or lazy fetch.
Disable hooks, fsmonitor, pagers, signature display, external diff and textconv;
deny every transport, including per-protocol overrides and remote helpers.
**F1/SR2:** distinguish caller-owned selection patterns from untrusted paths.
For both Markdown discovery pipelines, replace the trusted `*.md` Git pattern
with bounded `ls-files -z --` enumeration and the caller's fixed `.md` suffix
filter; retain present-file and existing source exclusions. Thus a tracked file
literally named `*.md` is data, not the entire selection. Apply literal
pathspecs and `--` to supplied paths (including metacharacter filenames), not
blindly to source-owned patterns; never let target text select pattern mode.
Validate revisions and use option terminators where supported. Object-consuming
operations retain the existing
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
permitted descendants on timeout/overflow. **SR3:** default reasons and remedies
are fixed caller-owned text. Git stderr never becomes `LifecycleError` or a
result banner verbatim; discard free-form diagnostics by default, including in
machine channels. Retained details must be allowlisted non-secret fields,
bounded, escaped and labeled **untrusted Git data**, never remedies or result
authority. Unknown or possibly secret payload is omitted, not trusted to a
generic redactor: escaping alone protects neither authority nor confidentiality. Neither config
overrides nor screening freeze the filesystem or contain a malicious host.

Return distinct absence, failed/incomplete, and completed-command outcomes.
Present-but-invalid executables are failure, not absence.
Never turn failure into a clean scan, empty measured history, or successful
edit check. Retain the intentional upgrade no-Git prelude: no repository or Git
unavailable before worktree confirmation means no guard. **After confirmation,
every later startup failure is `_EditCheckCannotTell`, including later groups.**
Apply and bare finalize refuse without changing bytes; stage advises. Existing
explicit `--force` behavior stays caller-owned, never a helper escape hatch.

**F2:** preserve translation at actual consumers, not in a universal exception:

| Caller | Empty success versus failure |
|---|---|
| Upgrade/install | Post-confirmation edit failure refuses/advises as above; committed-copy uncertainty keeps the file; binding discovery refuses unless the existing no-worktree/not-root exception is established; informational source provenance says unavailable rather than clean. |
| Session | Successful empty history is allowed; command/discovery/binding failure raises a fixed `LifecycleError`, never empty history/status. |
| Lockfile | `_cairn_commit` retains `unknown`; `_behind_by_n` retains unavailable; neither claims current/zero on failure. |
| Intent/hooks | Failed path/rename discovery is unknown with a warning under existing coordination enforcement policy, not a successful empty set. Do not auto-release claims on unknown committed paths; this does not add a new commit-blocking policy. |
| Checkers/measurements/reports | Enumeration failure is an error; no Markdown selection exits nonzero (currently 2), not clean. A completed empty log may mean zero commits; failed count/gauge/report/tier reads are unavailable/error, not measured zero or an empty successful test selection. |
| Security callers | Content scan keeps direct failure 2 / dispatcher DEGRADED; audit keeps DEGRADED on preflight/injection failure. Sweeps retain absent-tool INCOMPLETE, unsound execution DEGRADED, Git-free reduced mode and genuine not-applicable distinctions. |

## Rationale

The small file costs one delivery row, mirrored bytes and importer pins, but
keeps helper bindings stable during 2b/2c/8b session edits (F2). Reuse
[dispatcher](../../../templates/modules/default-on/run_security_verification.py)
and audit preflight bindings rather than invent another registry (SR1).
Preserve lockfile schema, manifest/parity contracts and anchored-reader isolation.
Helper changes require repinning trusted importers; unrelated session changes
do not. Runtime hashing/enumeration overhead still requires measurement.

## Alternatives considered

**Least involved credible repair:** fix N1 and add N2/N3 in the existing upgrade
test home. It is cheaper to build/run/review but leaves duplicated boundaries
and does not enable safe 7d/8a Git inspection. Doing nothing also leaves N1.
**Copy stronger settings into every caller:** avoids a shared dependency but
keeps repeated executable-resolution/cleanup fixes and their maintenance cost.
**Keep the helper inside session:** saves one file/delivery row but couples
every helper pin to unrelated session churn and imports its lifecycle surface.
**New package/universal wrapper:** adds install and trust machinery without a
needed capability. Recommendation: one cohesive file using the existing
delivery/pin seams, retaining the complete ordinary population.

## Documentation / doctrine surface

Governing layer: retain [AGENTS](../../../AGENTS.md) obligations and mirror any
necessary operative clarification in its shipped template; no lifecycle change.
Deliberation: this proposal and its eventual reviewed plan; parent owns board/
changelog. Descriptive layer: update [tool usage](../../../docs/tool-usage.md) and
[upgrade description](../../../bootstrap/UPGRADE.md), with domain-local safety
contract corrections in [SAFETY](../../../bootstrap/SAFETY.md), notably Windows bare
Git lookup and post-confirmation failure. Route these three levels under the
[documentation plan](../../../docs/DOCUMENTATION_PLAN.md), without duplicating policy.

## Evidence / verification plan

### Tests required

Use existing `bootstrap/tests/` owners, not another harness. In
[`test_upgrade_edit_check_runs_no_project_programs.py`](../../../bootstrap/tests/test_upgrade_edit_check_runs_no_project_programs.py),
extend `test_git_that_cannot_start_or_does_not_answer_at_any_step_is_no_guard_or_cannot_tell`
and `test_a_failure_in_a_later_group_is_cannot_tell`: N1 regression must fail on
current code, find an edit in the first group, and cover config/HEAD/index/diff
startup failures through collisions and real apply/finalize/stage entry points.
Retain no-Git success controls and byte-preservation assertions. N2 adds a real
linked-worktree `.git`-file edit control; changing `lexists` to `is_dir` must fail
it. N3 hangs **only** version, with later questions functional; ignoring the
version no-answer must fail it. Keep mutations repeatable in these tests.

F1/SR2's real controls belong in the existing doc-drift/self-check test homes:
run the actual link checker, snippet `--check`, and delegated `check_cairn`
without explicit file lists on a tracked broken-link document or drifted snippet,
first alone, then with a clean tracked literal `*.md` decoy. Require exit 1,
the planted finding, a nonempty selection and the expected one/two-file scan
set; a blanket-literal mutation must fail even when the decoy makes selection
nonempty. Also cover empty discovery's nonzero result, nested Markdown and
literal option/pathspec/metacharacter names. Security Review `c93d9dc4` measured
link-checker exits 1/2 without the decoy and 1/0 with it under normal/literal
mode; that probe is evidence, not a new-helper test run.

SR1 controls run real dispatcher, audit, direct content/sweep and ordinary
source/installed entry points: missing helper/required record, changed bytes,
linked parent/leaf and cached-module substitution must refuse before an
execution marker. A positive control first proves the marker is observable.
For commands accepting separate targets, plant helpers and adjacent matching
digests there and launch the trusted tool from target CWD: none may execute.
Mutating pin enforcement or moving audit verification after injection must fail
these controls. Bind the shim too; keep anchor-session extraction importable
without the new helper. F2 consumer checks exercise both completed-empty and
failed reads in every policy row. SR3 output-sink controls plant printable
forged status/bypass advice, control characters and a synthetic secret: only
fixed reasons and explicitly labeled safe data may appear, never raw secrets.

Extend existing owners:
[`test_session_kernel.py`](../../../bootstrap/tests/test_session_kernel.py),
[`test_git_interpreter_binding_portable.py`](../../../bootstrap/tests/security/test_git_interpreter_binding_portable.py),
[`test_intents_tool.py`](../../../bootstrap/tests/test_intents_tool.py),
[`test_security_stack.py`](../../../bootstrap/tests/test_security_stack.py)'s
`TestRunnerGitBoundary`,
[`test_portable_security_sweeps.py`](../../../bootstrap/tests/test_portable_security_sweeps.py),
[`test_security_verification.py`](../../../bootstrap/tests/test_security_verification.py)'s
apparatus-failure controls, [doc-drift tests](../../../bootstrap/tests/test_doc_drift_tools.py),
[count tests](../../../bootstrap/tests/test_verify_counts.py), and
[reference-script parity](../../../bootstrap/tests/test_reference_scripts.py).
[Self-check content tests](../../../bootstrap/tests/test_check_cairn_content.py)
and existing security-stack preflight tests own the new coverage above.
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
caller source supplies helper pins, delivery paths, commands and limits. Pins
are derived from reviewed helper bytes before delivery, never candidate data;
lockfile records add drift detection, not authenticity against joint rewriting.

**S2 -- falsifiability:** restore N1's `None`; ignore version no-answer; replace
`lexists` with `is_dir`; remove one environment/executable/command guard or one
pre-import pin/binding, or make every pattern literal: the corresponding
entry-point controls above must fail. These proposed mutations have **not** been
run; N1's supplied reproduction and historical
N2/N3 survivors are evidence of the present gap, not new-helper assurance.

**S3 -- trigger/set:** manual adopter commands above reach only their named
target read forms; mapped pytest selections exercise the complete inventory
and six-member content apparatus, including trusted enumeration selection and
literal supplied paths. Proposed adopter wording: "From trusted installed tool
code, repository reads use a pinned helper and validated host Git under bounded,
noninteractive, offline settings; an unanswered check is not a clean result."
Existing test/gate consumers were opened; no commit hook or CI is claimed to
enforce this design.

**S4 -- failure direction:** absent Git remains distinct from execution failure;
only upgrade's pre-confirmation no-guard path retains permission to proceed.
Malformed output, old unsupported Git, unsafe executable, missing helper pin or
record, empty Markdown selection, timeout and overflow take the caller-policy
row above, never authorize protected writes or claim measured cleanliness.

**S5 -- residual winner:** repository-controlled programs must not run, but
malicious host Git, compromised trusted source, or a same-user filesystem race
can still win, as can jointly rewritten local caller/helper/lockfile material
under the explicitly trusted-code advisory assumption. Git-admin interpreter
binding remains operationally trusted as Safety states. Command/config coverage
is reviewed enumeration, not a sandbox or proof against future Git execution features.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A migrated caller executes a planted program/remote helper, misses its positive
control, reports failure as clean, loses a listed read capability, or lets target
code supply expected helper bytes or imports. Such evidence keeps implementation
open; reject any routing that makes anchored ceremonies import candidate code.

## Scope delta

**Scope delta**: preserved -- all opening readers and N1-N3 remain. F1/F2 and
SR1-SR3 specify the original safety/capability contract and replace its helper
home, not its outcomes; no accepted scope is removed or Decision recorded.

## Assurance path

**Assurance path**: high-assurance

New execution boundary, scaffold, interpreter binding, portable sweeps,
dispatcher and install consumers require heavy treatment. Ordinary proposal
review plus separate Security Review precede a Maintainer Decision; an accepted
plan then needs Internal and Internal Security Review before implementation.
Coordinate caller/session edits with 2b/2c/8b; no reassignment of their work.

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

## Review -- Codex Terra -- 2026-11-04

Reviewed commit: c1be9fbb75c8865307fbff34ba1b6f5c38cab80a

**Model**: Codex Terra (medium)
**Tier**: usual
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes, with the wildcard contradiction resolved: a shared read boundary and the post-confirmation refusal address real gaps without granting ceremony authority. `bootstrap/_scaffold/upgrade.py` `_ask_git`, `_edit_check_prelude`, and `_writeset_dirty_collisions`.
2. **Best alternative.** Repair N1-N3 in upgrade alone: cheaper and preserves that guard, but leaves the other readers exposed and does not deliver the shared boundary; a new library adds installation and binding machinery, while the already-installed session home needs its cohesion tested. `bootstrap/_scaffold/config.py` `_SKILLS_MAPPINGS`; `templates/skills/_lib/session.py` `_git`.
3. **What would show it wrong?** Withdraw or redesign if a real entry-point negative control still executes a planted program, loses a required read, or reports an unanswered check as clean; mutate each routed caller separately. `scripts/link_check.py` `tracked_markdown`; `bootstrap/tests/test_upgrade_edit_check_runs_no_project_programs.py`.

**F1 -- Blocking: distinguish trusted patterns from literal paths.** The contract says to preserve literal pathspecs, but `scripts/link_check.py` and `scripts/sync_doc_snippets.py` use the source-owned pattern `*.md` in `git ls-files`. Applying literal pathspecs indiscriminately can return success with no files and a false clean result. Specify a fixed trusted pattern or enumerate and filter results, while treating supplied paths literally; require real checker entry-point controls with tracked Markdown, a planted finding, and a literal-wildcard mutation that fails.

**F2 -- Advice: make result translation and module cohesion explicit.** Session `_git` raises on a failed command but permits genuinely empty history; lockfile `_cairn_commit` deliberately reports `unknown`. Specify caller-owned translations that distinguish empty success, absence and failure, and test the actual consumers. Show that importing the large session module is self-contained in installed and source layouts and does not pull candidate code into anchored extraction; compare that ongoing coupling with a small separately installed library before settling the home. Preserve dispatcher digest binding and separate privileged write/ceremony runners.

**Coverage:** Read the committed proposal, current template, session reader and binding, upgrade prelude and grouped reads, install mapping, lockfile fallbacks, dispatcher binding, and searched production Git launch sites with known-positive matches. No tests or mutations were run; I did not fully trace every caller, native Windows or old Git, adapter cleanup, or independent Security Review. This pass exceeds the target to explain the false-clean mechanism and delivery tradeoff.

## Review -- Codex Sol (Security Review) -- 2026-11-04

Reviewed commit: c1be9fbb75c8865307fbff34ba1b6f5c38cab80a

**Model**: Codex Sol (high)
**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: approximately 10 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes, after SR1-SR2: centralize ordinary reads, not writer/ceremony authority; post-confirmation refusal repairs a real overwrite path. Evidence: `bootstrap/_scaffold/upgrade.py` `_ask_git`; archived `dev/plans/archive/upgrade-edit-check-no-repository-programs.md` code-review N1-N3.
2. **Best alternative.** Upgrade-only repair is cheaper but loses the shared protection; session avoids another installed module, not loader obligations. Evidence: `bootstrap/_scaffold/config.py` `_SKILLS_MAPPINGS`; SR1.
3. **What would show it wrong?** Mutate each routed real entry point: execution markers, lost documents or false cleanliness must fail controls, not merely helper mocks. Evidence: proposal S2 and SR2's measured checker probe.

**SR1 -- Blocking: bind before importing on every launch path.** Rationale names only the default dispatcher. Yet `templates/modules/team-gated/run_security_audit.py` `_MODULE_APPARATUS` excludes session, and `main` runs injection before `run_adopted_executable_gate`; that later detection cannot undo executing a substituted helper. Close by specifying pre-import verification for this orchestrator and direct content/sweep callers, with canonical trusted-source loaders in source and installed layouts, never target-root imports. Execute verified bytes, not unchecked cached code. Candidate-adjacent hashes are drift evidence, not authentication. Require real entry-point missing-record, tamper, link and substituted-helper controls that refuse before an execution marker; include separate external targets.

**SR2 -- Blocking: separate trusted patterns from literal paths (ordinary F1 independently assessed).** Python 3.13.13, isolated committed-source copy, actual `scripts/link_check.py --root` probe: tracked broken `A.md` exits 1; literal mode alone exits 2, not clean. Add a clean tracked file literally named `*.md`: normal mode still exits 1 over two files, but `GIT_LITERAL_PATHSPECS=1` exits 0 over only the decoy. Thus candidate-controlled filenames turn capability loss into false assurance. Close with fixed trusted-pattern handling or enumerate/filter, retaining literal untrusted paths; pin checker, snippet and delegated self-check entry-point controls.

**SR3 -- Advice: make default errors source-owned.** Session `_git` currently puts Git stderr into `LifecycleError`, printed by `main`. "Escape diagnostics" alone leaves printable candidate instructions looking authoritative. Prefer fixed default reasons; label bounded escaped details as untrusted data, never remedies or result authority. Close with forged-status/bypass-advice and control-character probes at actual output sinks.

**Coverage:** Independent non-author read; caller inventory, install homes and byte-identical session/sweep mirrors, N1-N3, configuration/environment/argv contracts, host revalidation, bounds/cleanup requirements and separate anchored authority. Probe above used synthetic data only. Claim/link/content checks cover this appended candidate in the isolated copy. No pytest, new-helper assurance, per-member routing mutations, native Windows/old-Git or descendant/race experiments; no network or certification. Host compromise and filesystem races remain named residuals. Over target to distinguish measured decoy exploitation from the inferred loader risk. Status remains revising; earlier records are unchanged.

## Response -- Codex (Sol, high) -- 2026-11-04

**Elapsed**: unknown
**Tokens**: unknown

Both full reviews (`6ed52df5`, `c93d9dc4`) are folded into operative text;
their records remain unchanged. All design findings are disposed below; status
is `awaiting-decision`, not accepted. These specify the original boundary and
preserve every reader/N1-N3, rather than widening its outcomes. No clearing
review or implementation is requested.

- **F1: accept.** Both discovery pipelines enumerate/filter tracked Markdown;
  untrusted supplied paths remain literal, never source-owned patterns.
- **F2: accept.** The caller-policy table separates empty success from failure,
  absence, unknown and incomplete. One small mirrored helper uses the existing
  delivery path; its extra row/pins cost less continuing churn than binding
  every reader to the session monolith. Privileged runners remain separate.
- **SR1: accept.** The delivery/binding table covers dispatcher, audit before
  injection, direct security callers, ordinary readers and shim. Expected
  helper bytes come from a literal pin in trusted caller source, not target or
  adjacent digest material; execute the verified buffer only. Existing lock
  bindings add pre-import drift checks, not authentication of a jointly
  rewritten local installation. Missing/tamper/link/substitution controls must
  observe refusal before markers, including external-target/CWD cases.
- **SR2: accept.** Require actual checker/snippet/self-check finding and scan-set
  controls both with and without the literal-wildcard decoy, plus empty-set
  refusal and literal metacharacter coverage. The measured probe is the
  reviewer's, not a new run or implementation assurance.
- **SR3: accept.** Fixed default errors, labeled bounded escaped non-secret data
  only, and forged-status/bypass/secret sink controls replace raw Git authority.

Python 3.13.13: claim, one-file link/content and snippet checks pass;
neutrality has zero failures/43 informational items (excludes this file).
Selector: zero test readers; known-positive search reaches content-runner tests.
No pytest, probe rerun, mutations, network or implementation. Windows/old-Git,
host compromise, paired tamper and races remain declared; no separate scope
concession is needed beyond deciding this proposal.

### Withdrawn / superseded commitments

- Session as helper home and its additional apparatus binding are replaced by
  the cohesive helper/mirror and pre-import pins (F2/SR1); no read is dropped.
- The opening "no new module" choice is superseded by one delivered file to
  reduce continuing coupling (F2), not a new framework or service.
- Unqualified literal-pathspec wording is replaced by trusted enumeration/filter
  versus literal supplied paths (F1/SR2). No capability is conceded.

## Decision -- gpt-6.1-sol (High), delegated decision-maker -- 2026-11-06

**Model**: gpt-6.1-sol (High).
**Authority**: temporary Maintainer delegation -- chat, 2026-11-06, relayed by the coordinating agent. This is the Sol agent's decision under that explicit exception, not a claim that the Maintainer selected this option personally.

> "I specifically authorize you to use a Sol agent to make decisions in my stead until I return (excepting anything that cannot be undone easily). Keep track of these decisions for review. Let the other agent know to ask you if they need it, and you will spawn the Sol review and track its outcome."

**Tier**: heavy.
**Elapsed**: unknown. **Tokens**: unknown.
**Source**: operative proposal, appended usual and Security Reviews, and author responses as committed at `831d0e3b`; the proposal bytes remained unchanged through `8380bc9b`.

**ACCEPTED.** Choose the small, byte-identical Git-read helper and complete ordinary-reader migration for v0.7, including N1-N3.

**Reason.** The supplied N1 failure and the Security Review's literal-wildcard
probe establish distinct false-clean paths. The revised contract closes those
paths and binds the helper before execution across the inventoried callers;
privileged ceremony runners keep their independent authority. The F1/F2 and
SR1-SR3 responses specify the opening outcomes without conceding readers.

**Options and costs.** Upgrade-only N1-N3 repair is the least involved credible
repair: less caller coordination and runtime work, but it leaves duplicated
boundaries and does not deliver safe shared inspection for dependent Git views.
Doing nothing also retains N1. Copying guards separately avoids the helper
binding but repeats future fixes. The selected cohesive file adds one delivery
row, mirrored bytes, importer pins, executable checks and bounded enumeration;
helper changes require repinning consumers. Runtime overhead and total build
cost remain unmeasured. It adds zero new human ceremonies and no service or
recurring ledger; existing release operations retain their current homes.

**Delivery fence.** Keep the full caller inventory, pre-import byte binding,
fixed diagnostic policy, failure translations, N1-N3 regressions, per-member
mutation controls and named native Windows/old-Git evidence. Dependent Git views
wait for the verified boundary; absence of that evidence is unfinished work,
not permission to use an unsafe fallback.

Accept the complete operative scope and its stated limitations; no outcome or
required check is waived. High-assurance treatment, both required plan reviews,
ordinary and separate Security code reviews, mapped checks and final wide
Boundary B remain due. Proposal controls described as unrun remain unrun.
This authorizes reversible local planning and implementation, not an actual
release, push, publication, signing, trust-ref movement, credentials/private-log
access or other hard-to-undo action. Those operations remain with the Maintainer.
