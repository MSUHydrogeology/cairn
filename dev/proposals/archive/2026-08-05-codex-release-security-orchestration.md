<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/lifecycle.md doctrine/rationale.md doctrine/proposals.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# One honest release-security command

**Author**: Codex (Strategy)
**Model**: GPT-5 (Codex)
**Date opened**: 2026-08-05
**Status**: accepted
**Touches**: `bootstrap/security_check.py`, its tests and release-only pytest
policy; `SECURITY.md` and the release-cut description in
`bootstrap/PROVENANCE.md`; the live false-CI and floor-gate wording in
`dev/plans/_template.md`, `bootstrap/requirements-dev.txt`,
`doctrine/runtime-contract.md`, `bootstrap/tests/test_security_lint.py`,
`bootstrap/tests/test_python_floor.py`, and
`bootstrap/tests/fixtures/skills/README.md`; one `CHANGELOG.md` line and board
retirement at their serialization points
**Related**: `gate-claims-vs-enforcement`, `profile-parse-fail-open`,
`scan-coverage`, `default-security-stance`, `release-security-bar`,
`board-drain-guards`; `dev/PLANNING.md` > **Security apparatus**, **Scan
coverage**, and **Archive-time follow-ups**
**Plan review**: required(External + External Security Review) -- this changes
the command Cairn names as its fail-closed release security gate, including
what it runs and what outcomes it refuses.

## Context

The security board is carrying several individually small rows whose common
cause is now visible: Cairn has useful checks, but no single command expresses
the complete local release bar honestly.

`bootstrap/security_check.py` is documented as the release command. Today it
runs Bandit and `scripts/check_cairn.py`. `SECURITY.md` separately asks the
Maintainer to remember the full test suite, while `scripts/quality_gate.py` is
not in that checklist at all. The suite may exit zero after skipping a security
test, because ordinary contributor runs deliberately permit missing dev tools.
Several comments still claim CI supplies the missing trigger even though Cairn
has no CI.

The gaps reproduce by execution rather than inference:

* On 2026-08-05, under the canonical Python 3.13.13 interpreter,
  `bootstrap/security_check.py` returned exit 0 and printed its final `PASS`
  while the checkout contained both tracked modifications and untracked files.
  Its output showed only `check_cairn` and Bandit; it did not run pytest or the
  quality gate.
* Bandit 1.9.4, run directly over
  `templates/modules/team-gated/link_check.py`, reported five LOW findings and
  **no `B310` finding**. The only entry in `security_check.ALLOWLIST` is the
  absent `(link_check.py, B310)` pair. It is stale now, not merely vulnerable to
  becoming stale later.
* `bootstrap/tests/conftest.py` contains only the order-shuffle hook. There is no
  release mode and no session outcome check; pytest's normal zero exit after a
  skip is therefore the behavior Cairn receives.

These are not six unrelated projects. They are one missing boundary: the
Maintainer needs one local command that says exactly what it ran, refuses
incomplete evidence, and is described as Maintainer-run rather than CI-run.

## Proposed paths

Proposed paths:
- `bootstrap/tests/fixtures/release_gate/outcomes.py` -- explicitly selected pass/skip/xfail/xpass fixture nodes for subprocess tests; it is not collected by the ordinary suite.

## Proposal

### 1. Keep the existing public command, and make it complete

`python bootstrap/security_check.py` remains the one release-security command.
Do not add a second wrapper whose only job is to remember the first one.

The command runs four named phases and reports one result per phase:

1. repository-state preflight;
2. Bandit over `scan_targets()` plus `scripts/check_cairn.py`;
3. the complete `bootstrap/tests` suite in release mode; and
4. `scripts/quality_gate.py` with all of its sub-gates.

The repository-state preflight runs first and stops the command if the checkout
is not a release candidate. Once it passes, the other three phases are all
attempted so the Maintainer gets a complete repair list from one run. The
repository state is checked again afterward: `HEAD` must be unchanged and the
tree must still be clean. The final exit is non-zero if any phase failed,
errored, was unavailable, changed the candidate, or produced incomplete
evidence. `PASS` is printed only after both state checks and all three checking
phases return clean.

The repository-state preflight requires the checkout root, a clean tracked and
untracked worktree, and a resolvable full `HEAD` object ID. It prints that full
ID in the final summary so the release notes can bind the recorded run to the
commit being tagged. Git runs with the steering environment stripped and the
execution-bearing configuration used by Cairn's existing trust-root tools
disabled; the implementation reuses their narrow pattern rather than inventing
an ambient `git status` call.

This is a **local, Maintainer-run release ceremony**, not CI. It does not add a
forge workflow, a hook, or an always-on contributor gate.

### 2. Add an explicit release-only pytest disposition

`bootstrap/security_check.py` marks every pytest subprocess it owns with one
private environment token. `bootstrap/tests/conftest.py` recognizes that token
and changes only release-mode session disposition:

* any actual `skipped`, `xfailed`, or `xpassed` outcome makes the session
  non-zero;
* an already failing or interrupted session stays non-zero; and
* without the token, current contributor behavior is unchanged.

The token is inherited by the order-independence subprocesses spawned by
`scripts/quality_gate.py`, so a shuffled run cannot silently skip what the
ordinary release suite would refuse. This is an outcome rule, not a marker
census: an inactive `skipif` marker does not fail a release merely for existing.
The gate manifest continues to own its separate "new skip/xfail marker" check.

This resolves the tension that produced the board row. A scientist developing
without every optional dev tool can still run the suite and see a documented
skip; a Maintainer cutting a release cannot call that incomplete run green.

### 3. Make the Bandit allowlist self-retiring

Delete the stale `B310` entry. In `run_bandit()`, derive the set of observed
`(repo-relative path, test_id)` pairs from Bandit's successfully parsed report
and fail closed if any configured `ALLOWLIST` key is absent.

This makes an allowlist entry a live exception to a live finding. If a file
moves, a rule is retired, or code is remediated, the next release check stops
and asks for deletion of the obsolete exception. Rationale remains mandatory;
liveness is an additional condition, not a replacement.

### 4. Correct the live trigger vocabulary

Make the already-ledgered wording corrections in the same scope:

* `dev/plans/_template.md` says "the standing gates Cairn runs before a change
  lands", with no claim that CI enforces them. Existing proposal/plan sections
  remain append-only historical records; only the source template changes
  prospectively.
* `bootstrap/tests/test_security_lint.py` describes its CI branch as dormant
  provisioning for a future CI, and names the release command as today's
  fail-closed trigger.
* `bootstrap/tests/fixtures/skills/README.md` says "suite-proven" and names a
  recorded native-harness transcript where the suite cannot run the harness.
* `bootstrap/tests/test_python_floor.py` and
  `bootstrap/requirements-dev.txt` say "floor check", not "CI floor check".
* `doctrine/runtime-contract.md` calls
  `bootstrap/container/floor-gate.sh` the **Maintainer-run contained floor
  check**, and says an unresolvable `vermin` fails *that command*. It does not
  imply that the main release-security command dispatches a host-specific
  container check.

The doctrine edit is a correction of trigger strength, not a new contributor
obligation. It clears the doctrine rate-limit as a high-risk security/release
classification: the current text overstates enforcement on the release path.

### 5. Name the human root instead of pretending to remove it

Nothing inside a repository can prove that a Maintainer ran a repository-local
command before using raw `git tag`. Cairn will not build a tag-creation wrapper,
CI workflow, signed gate receipt, or mandatory hook in this proposal.

Instead, `SECURITY.md` names one command and requires its output, including the
full clean `HEAD`, in the release notes. `bootstrap/PROVENANCE.md` states the
ordering: run the command against the clean commit, then sign a release tag that
names that same commit. The Maintainer's act is the operational root.

This **dispositions** the board's "nothing invokes `security_check.py`" row; it
does not mechanize it. The accepted residual is explicit:

* a Maintainer can omit the command or record false output;
* the command does not authenticate its own process or bytes; and
* the repository does not cryptographically bind the output to the tag.

The disposition expires if Cairn gains a second release Maintainer, accepts
untrusted contributions, adds forge automation, or misses a release check in
practice. Any of those makes an authenticated receipt or release-cut wrapper a
new decision with evidence behind it rather than machinery built in advance.

### Documentation / doctrine surface

The governing security workflow remains in `SECURITY.md`; source/tag ordering
remains in `bootstrap/PROVENANCE.md`; the floor-check description remains in
`doctrine/runtime-contract.md`. The plan template and frozen comments receive
accuracy corrections only. One `CHANGELOG.md > Unreleased > Changed` line will
say that Cairn's Maintainer-run release command now covers the complete local
bar and refuses dirty or incomplete runs.

No adopter doctrine or installed module behavior changes. The release command
is Cairn's own development apparatus.

## Scope and interaction with current plans

This proposal deliberately joins the existing security cluster instead of
claiming its work:

* `default-security-stance`, `portable-security-sweeps`,
  `security-verification-activation`, and `api-web-security-modules` continue to
  own module selection, runners, policies, and registry bindings. Their new
  shipped Python enters `scan_targets()` automatically; this proposal does not
  re-enumerate or baseline it.
* `content-scan-detectors` and `separator-detection` continue to own the content
  scanner. The release command reaches their result through `check_cairn`; it
  does not duplicate detector logic.
* `dependency-advisory-coverage` keeps its accepted no-baseline v1. This command
  does not run adopter-facing dependency modules against Cairn's development
  environment.
* `release-security-bar` remains the v0.4.0 register and decider owner. This
  proposal supplies a better local machine-checkable decider command; it does
  not absorb the register's manual checks, the host-specific contained floor
  check, examples, or release-authenticity ceremony, alter B1-B6, or declare the
  release ready.
* `board-drain-guards` lands its factual corrections first. Its corrected SC5
  and G6 rows then retire when this proposal implements, rather than receiving
  the guards that plan correctly rejected.

Implementation should be the last code scope admitted before the already
scheduled shared supervised re-anchor. It touches frozen tests and fixtures;
joining the batch avoids paying a second ceremony. Every count, frozen-file
delta, and suite figure is re-derived at plan/implementation time after the
other security plans land. No number in an earlier plan is an input here.

### Board effect

On implementation and the required serialization point, this proposal closes
or dispositions these existing rows:

| Board row | Disposition |
|---|---|
| Scan coverage SC5, stale Bandit allowlist | fixed by deletion plus runtime liveness refusal |
| Profile parse G6, zero skips unenforced | fixed for the release path; ordinary development skips remain intentional |
| Gate claims A5/A6/A8, frozen CI wording | corrected during the shared re-pin batch |
| Gate claims, false CI text in `dev/plans/_template.md` | corrected prospectively at the template source |
| Gate claims B3, "release floor gate" vocabulary | corrected to the actual Maintainer-run contained check |
| Gate claims, nothing invokes `security_check.py` | explicit human-root disposition plus one complete command; not represented as automation |

It does **not** close the install-integrity trust anchor, conda advisory
coverage, the unfinished axis-2/axis-3 claim audit, gate-manifest skip-marker
over-reporting, or the release checker's own integrity preflight.

## Rationale

The Maintainer is a solo scientist, and ceremony complexity is itself a
security cost. One complete command is easier to run, easier to record, and
harder to misunderstand than a checklist of partially overlapping commands.
Release-only strictness preserves contributor ergonomics while making the
security claim true at the point where it matters.

The proposal also gives the board a stopping rule. Rows that are one symptom of
the same missing release boundary leave together; genuinely different trust
questions stay separate. That is how the backlog shrinks without weakening the
review record or building speculative infrastructure.

## Alternatives considered

### Add hosted CI

Rejected for this proposal. Cairn currently has no CI, active gate-manifest
work deliberately creates supervised red windows, and a forge runner changes
the untrusted-contribution and credential threat model. CI may be right later;
using it to repair inaccurate prose today would turn a bounded release fix into
an operations program.

### Add a new `release_check.py` wrapper

Rejected. `security_check.py` is already the documented public command and the
single source of the Bandit scan surface. A second entry point would leave two
names to remember and create another place for phase lists to drift.

### Make every pytest invocation fail on skips

Rejected. Optional dev tools intentionally remain optional for ordinary
contributors. The security property is not "no developer ever skips"; it is
"a release cannot use a skipped check as clean evidence."

### Create a signed release-check receipt or a tag-cut command

Deferred, with the expiry triggers stated above. It would narrow omission and
record-tamper risk, but introduces a second signing protocol and a ref-mutating
Maintainer tool. That cost is not justified under the current solo-maintainer,
trusted-contributor model.

### Fold in checker self-integrity or install-integrity anchoring

Rejected as a scope merge. A candidate script cannot establish trust in its own
bytes, and `verify_integrity.py` cannot distinguish a legitimate fork from a
coordinated target-plus-lockfile edit without an external trust source. Both
need trust-root designs; neither is repaired by running more checks from the
same checkout.

### Do nothing

Rejected. The current command can print release `PASS` over a dirty checkout,
the suite can skip security evidence while exiting zero, the sole allowlist
entry is already stale, and the docs still attribute enforcement to CI that
does not exist.

## Evidence / verification plan

### Author-accounting -- invariants, failure modes, edge cases

| Contract | Enforcer |
|---|---|
| Final `PASS` means all named phases completed cleanly | orchestration tests force each phase to fail, error, and disappear in turn; every mutation must make `main()` non-zero |
| Release evidence names the tree it tested | repository-state checks before and after the checking phases refuse dirty tracked/untracked state and require the same full `HEAD`; tests cover a clean temporary repo, tracked dirt, untracked dirt, changed `HEAD`, phase-created dirt, and git failure |
| Ordinary contributor skip behavior does not change | subprocess tests run the same fixture without the release token and observe pytest's normal disposition |
| Release pytest cannot pass with skipped/xfail/xpass outcomes | subprocess tests select each fixture node with the release token and require non-zero; the clean node requires zero |
| Quality-gate child pytest runs inherit release strictness | an orchestration test captures the child environment, plus one end-to-end quality-gate probe runs a selected skip fixture through the inherited token path |
| Every Bandit exception is live | `run_bandit()` refuses a parsed report missing any allowlist key; tests cover present, missing, moved-path, malformed-report, and scanner-error cases |
| No historical lifecycle section is rewritten | changed-file review permits only `dev/plans/_template.md`; existing plan/proposal instances remain untouched |

**Failure disposition.** Scanner absence/error, malformed scanner output,
unopened target, stale allowlist, dirty tree, unknown HEAD, missing pytest,
actual skip/xfail/xpass, failed suite, missing quality-gate script, and any
quality sub-gate failure all fail closed. Ordinary non-release pytest skips
remain intentionally open and visible.

**Known omissions.** Tests do not prove a human ran the command, authenticate
the command's bytes, bind stdout cryptographically to a tag, or contain code
executed by pytest. Those are outside the accepted local trusted-contributor
threat model and are stated in the release docs.

### Tests required

* Extend
  [`bootstrap/tests/test_security_check.py`](../../bootstrap/tests/test_security_check.py)
  for repository-state checks, complete phase orchestration, environment
  propagation, fail-closed subprocess errors, and final-summary binding.
* Extend
  [`bootstrap/tests/test_security_lint.py`](../../bootstrap/tests/test_security_lint.py)
  for live allowlist behavior. The decisive path remains `run_bandit()` itself;
  a test-only census is not the control.
* Add the explicitly selected outcome fixture named under **Proposed paths** and
  subprocess tests for clean, skip, xfail, and xpass release dispositions.
* Run the whole suite under the canonical Python 3.13.x interpreter. A release
  acceptance run must report zero failed, skipped, xfailed, and xpassed; the
  implementation re-measures the node count rather than inheriting one.

### Examples / smoke checks

1. In a clean disposable worktree, run the canonical interpreter against
   `bootstrap/security_check.py`; require all four named phase summaries, full
   `HEAD`, and final `PASS`.
2. Add one untracked file and rerun; require non-zero before the scanners run.
3. Restore cleanliness, inject a temporary stale allowlist key, and rerun;
   require a named stale-entry refusal.
4. Run the release-mode pytest fixture's skip node; require non-zero. Run the
   same node without release mode; require the ordinary pytest skip result.
5. Run `python scripts/check_cairn.py`, `python scripts/quality_gate.py`, and the
   proposal/plan claim checks separately so orchestration cannot hide a broken
   component command.

### Docs delivered

The implementation updates the three documentation homes named above, the
prospective plan template, the frozen wording fixtures/comments, and one
release-note line. At archive, `dev/PLANNING.md` removes only the rows listed in
**Board effect** and leaves every excluded item in place.

## Expected outcome

Cairn has one accurately named, Maintainer-run release-security command. It
binds its output to a clean commit, runs the complete local bar, refuses
skipped evidence and stale exceptions, and says plainly what remains human.
Six board rows leave without pretending that CI, self-attestation, or
cryptographic release receipts were built.


## External review -- Antigravity (External, security lens) -- 2026-08-05

**Steelman.** Proposal `2026-08-05-codex-release-security-orchestration.md` addresses a fundamental boundary gap in Cairn's release workflow: today, `bootstrap/security_check.py` is documented as the release gate but runs only Bandit and `scripts/check_cairn.py`, leaving `bootstrap/tests` and `scripts/quality_gate.py` uncoordinated, permitting dirty worktrees, ignoring stale allowlist entries, and relying on inaccurate prose claiming CI enforcement. The proposal consolidates all local pre-release checks into one fail-closed command (`python bootstrap/security_check.py`) executing four sequential phases: (1) repository-state preflight/postflight, (2) Bandit + `check_cairn.py`, (3) `bootstrap/tests` in release mode (refusing skipped/xfail/xpass outcomes via a private environment token in `conftest.py`), and (4) `scripts/quality_gate.py` across all sub-gates. It also enforces allowlist liveness in `run_bandit()`, deletes the stale `B310` allowlist entry, updates trigger documentation across five files, and binds the clean `HEAD` SHA to release notes in `SECURITY.md`.

### Critical Security Audit & Analysis

1. **Fail-Closed Release Pytest Disposition (`conftest.py` & Token Inheritance)**:
   - **Mechanism**: `security_check.py` sets a private environment variable (`CAIRN_RELEASE_GATE_ACTIVE=1`) before executing subprocesses. `bootstrap/tests/conftest.py` checks this token during `pytest_sessionfinish(session)` and forces a non-zero exit if `skipped`, `xfailed`, or `xpassed` test outcomes are present.
   - **Subprocess Propagation**: `quality_gate.py:164` calls `subprocess.run(cmd, cwd=str(repo_root), capture_output=True, text=True)`. Because `env` is not overridden in `quality_gate.py`, `os.environ` is inherited automatically, ensuring order-independence shuffled test runs enforce the same strict release disposition.
   - **Security Edge Case**: In `conftest.py`, the token check must be strict (e.g. checking exact token value) so normal contributor runs without the token permit standard pytest skip behavior. Conversely, if a test script constructs a custom `env` dict for a `pytest` child process, it must forward `os.environ` or explicitly propagate `CAIRN_RELEASE_GATE_ACTIVE` so sub-invocations cannot bypass strictness.

2. **Repository-State Preflight & Postflight Dirt Control**:
   - **Verification**: `security_check.py` checks git worktree status before Phase 1 and after Phase 4. It requires a clean worktree (zero tracked modifications, zero untracked files) and a resolvable full 40-character `HEAD` SHA.
   - **Fail-Closed Hazard Analysis**: If any test in Phase 3 or Phase 4 leaves transient untracked artifacts (such as temporary cache files or un-ignored test outputs), the postflight check catches the dirt and fails closed. `security_check.py` itself must be strictly read-only and write zero untracked files.
   - **Environment Sanitization**: Git sub-commands executed during preflight/postflight must strip `GIT_*` steering variables (`GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, etc.) to prevent environment-injection attacks from overriding repository detection.

3. **Allowlist Liveness Enforcement**:
   - **Empirical Audit**: Executed `bandit -q -f json templates/modules/team-gated/link_check.py` under Python 3.13.13. Bandit 1.9.4 returned 5 LOW findings (B404, B607, B603) and **0 B310 findings**.
   - **Finding**: The sole entry in `ALLOWLIST`—`("templates/modules/team-gated/link_check.py", "B310")`—is indeed stale.
   - **Enforcement**: Under the proposed liveness rule, `run_bandit()` parses Bandit's JSON output, collects all observed `(file, test_id)` pairs, and compares them against `ALLOWLIST.keys()`. If any configured key is absent from the report, `run_bandit()` fails closed. Deleting `B310` alongside this change is required and prevents a baseline failure.

4. **Human-Root Grounding & Expiry Triggers**:
   - The proposal deliberately avoids building tag-creation CLI wrappers or forge CI infrastructure, placing the operational root on the Maintainer running `security_check.py` against a clean `HEAD` and embedding the full commit SHA in `SECURITY.md` release notes before signing the tag.
   - The explicit expiry triggers for this human-root posture (gaining a second maintainer, untrusted contributions, forge automation, or an un-checked release) provide clear governance boundaries for future architectural transitions.

### Covered

* **Empirical Script Execution**:
  - `bootstrap/security_check.py`: currently exits 0 with `PASS` over 76 files and 177 Markdown files, but misses pytest, quality gate, git state, and allowlist liveness.
  - `bandit`: confirmed `B310` is absent from `link_check.py` findings.
  - `scripts/claim_check.py`: clean output over `dev/proposals/2026-08-05-codex-release-security-orchestration.md`.
* **Path & Citation Audit**:
  - Verified all 11 paths in `Touches` exist and resolve accurately.

### Concerns

* **[E1] Pytest Subprocess Isolation in Custom Fixtures**:
  - The implementation plan must require any fixture or test runner that constructs a custom environment dictionary (`env={...}`) to explicitly preserve `CAIRN_RELEASE_GATE_ACTIVE`, preventing accidental token stripping during nested subprocess invocations.

### Recommendation

**ACCEPT / SHIP PROPOSAL.** The proposal is well-designed, security-hardened, empirically verified, and appropriately scoped. Proceed to plan creation.

## Response -- Codex (author, to the External Security Review) -- 2026-08-05

**Model**: GPT-5 (Codex)

**[E1] accepted and bound to the executable contract.** The review is right
that ambient inheritance alone is too easy to break later with an apparently
innocent `env={...}`. The required property is narrower than preserving the
token through every subprocess in the repository: every pytest subprocess
whose result contributes release evidence must receive the exact release token.

I audited the present nested-pytest paths. The only executable nested suite is
the order-independence runner in `scripts/quality_gate.py`; it currently passes
no `env` and therefore inherits the token. The other pytest subprocess in
`bootstrap/tests/_gate_manifest.py` is collection-only and constructs its
custom environment with `dict(os.environ, ...)`, which also preserves the
token. No present nested-pytest launcher replaces the environment from an empty
mapping.

### Binding amendment R1 -- release-token propagation

The implementation and its future plan must satisfy all of the following:

1. `bootstrap/security_check.py` constructs the child environment from a copy
   of the process environment, sets `CAIRN_RELEASE_GATE_ACTIVE` to the one
   recognized value, and passes that environment explicitly to both the
   complete-suite and quality-gate subprocesses.
2. Any nested pytest launcher reachable from either release phase inherits that
   environment. If it needs custom variables, it merges them into a copy of the
   inherited environment; it must not replace the environment with a partial
   mapping. An absent token or any value other than the one recognized value
   retains ordinary contributor behavior.
3. The release-orchestration tests capture both direct child environments and
   require the exact token. The quality-gate regression then selects a release
   outcome fixture through the real order-independence child path: a skipped,
   xfailed, or xpassed child must make the parent release phase non-zero, while
   the clean child passes. This is the decisive check against a future custom
   environment silently stripping the token.
4. A plan-time call-path audit re-enumerates nested pytest launchers. A
   collection-only launcher is recorded but is not represented as execution
   evidence; any newly discovered executable launcher joins the propagation
   test before implementation lands.

This amendment strengthens the proposal's existing token-inheritance test; it
does not make every unrelated test helper part of the release protocol. The
review returned SHIP, its sole concern is now part of the executable contract,
and the proposal is Decision-ready. Status remains `proposed` pending the
Maintainer's Decision.


## Decision -- 2026-08-05

**Maintainer authorization, quoted verbatim:**

> Please scribe my decisions as ACCEPT as revised.

Scribed by Antigravity on explicit Maintainer instruction. Proposal `2026-08-05-codex-release-security-orchestration.md` is **accepted as revised** (incorporating Author Response and Binding Amendment R1). Status changed from `proposed` to `accepted`.

