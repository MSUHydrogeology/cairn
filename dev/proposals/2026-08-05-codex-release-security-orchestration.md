<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/lifecycle.md doctrine/rationale.md doctrine/proposals.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# One honest release-security command

**Author**: Codex (Strategy)
**Model**: GPT-5 (Codex)
**Date opened**: 2026-08-05
**Status**: proposed
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
