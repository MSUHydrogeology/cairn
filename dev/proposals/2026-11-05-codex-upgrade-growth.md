# Bound Upgrade Growth and Trial a Git Merge

**Author**: Codex GPT-5 (Proposal author)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-05
**In brief**: Limit new upgrade refusals to justified threats and compare the existing upgrade with a small Git-based trial.

## Decision summary

Upgrade protects adopter files, but each additional refusal adds code and
maintenance. Adopt a review rule requiring a concrete in-model attack for
each new refusal, or an explicit Maintainer decision on the risk. Then compare
the present upgrade with a scratch Git merge on the same customized project.
The trial costs a session and cannot establish that Git is a safe replacement.

## Context

The [upgrade-growth strategy](../strategy/2026-10-30-claude-upgrade-growth.md)
records historical growth and proposes the comparison; those measurements are
from October 30, not current counts. Upgrade already uses containment checks,
a recorded base and Git's `merge-file`; see
[`security.py`](../../bootstrap/_scaffold/security.py),
[`upgrade.py`](../../bootstrap/_scaffold/upgrade.py) and
[`merge.py`](../../bootstrap/_scaffold/merge.py). A hostile project can plant
paths that redirect a privileged operator's writes, or corrupt upgrade state;
protecting the project and files outside it remains necessary.
[`SAFETY.md`](../../bootstrap/SAFETY.md) separately documents residuals under
its stated assumptions, including no concurrent filesystem attacker and no
untrusted code path. Those assumptions do not make all hostile project data
out of scope. Board [7d](../PLANNING.md) asks for both the rule and trial;
onboarding work does not replace the comparison.

## Proposal

1. In the governing review guidance, require each proposed new upgrade
   refusal to identify the attacker, controlled input, concrete harmful action
   and connection to the existing threat model, with evidence or a test able to
   distinguish it. If outside that model, identify the residual and seek the
   Maintainer's explicit risk disposition; an agent or reviewer cannot accept
   risk on the Maintainer's behalf. An unexplained threat or unmet protection
   remains open, not automatically accepted. Existing refusals and required
   checks remain intact; this is not permission to delete or weaken them.
2. After the verified Git-read boundary in
   [2d](2026-11-04-codex-safe-git-reads.md) is available, run one bounded
   session in isolated scratch repositories, with no real adopter data or
   trust-record edits. Pin the v0.5.0 source and candidate HEAD, environment,
   Git version and commands. Install the prior version, make representative
   slot and ordinary-file edits, and clone the same initial state for the
   existing upgrade and a prototype template-branch merge. Include a separate
   committed planted-link case and an outside sentinel; observe writes and
   conflicts without assuming Git prevents escape. Keep the prototype out of
   production. Do not bypass the 2d prerequisite if delayed; record the wait.
3. Record each path's conflicts, preserved or lost edits, operator steps,
   engine code exercised, and applicability of cases in
   [`test_upgrade_refuses_hostile_project_data.py`](../../bootstrap/tests/test_upgrade_refuses_hostile_project_data.py).
   List the cases and explain applicable, inapplicable and untested entries;
   do not claim a security equivalence from a single example. Record elapsed
   time, limitations, and whether migration from recorded bases preserves the
   sample customizations. A failed or incomplete trial is a result, not
   permission to ship a replacement.

The rule and trial are the v0.7 outcomes. A supported replacement, install
contract or migration change needs a separate accepted v0.8 proposal; no
replacement is promised here. Coordinate Git callers with 2d and the upgrade
walkthrough in [release verification](2026-11-05-codex-opt-in-release-verification.md).

## Rationale

The rule makes the cost of another refusal visible while retaining defenses
against the confused-deputy problem: project-controlled data causing a trusted
operator's tool to write somewhere unintended. A matched comparison can reveal
conflicts and migration losses before anyone commits to new machinery. Neither
the trial nor an out-of-model label proves a path safe.

## Alternatives considered

Do nothing adds no policy or trial work, but leaves future growth and the Git
alternative unmeasured. A table-driven path policy could simplify code but
keeps the same state and trust problem; building it now costs implementation
and review without comparison evidence. Replacing the engine now risks the
install contract and adopter edits before the migration and link behavior are
known.

## Documentation / doctrine surface

Route the review rule to the appropriate governing instruction in `AGENTS.md`,
with any explanatory methodology in `docs/methodology/`; keep trial evidence in
the plan under `dev/`. No engine or installed contract change is authorized.

## Evidence / verification plan

The plan must map changed prose readers and pins, run applicable claim, link,
snippet and neutrality gates, and record Boundary B on the final committed
change. Review the recorded trial against both paths and every listed hostile
case. More conflicts, lost edits, a write through the planted link, or an
unaccounted hostile case falsifies any claim that the prototype is ready to
replace the current path. Record observations even when the session ends
without a conclusion.

### Tests required

Map tests that read the eventual changed instruction using
`tools/test_tiers.py for`; include relevant pinned-prose tests. The trial uses
the real scaffold upgrade entry point and actual Git merge in isolated copies;
it does not substitute for the hostile-project test family or security review
of a future implementation. Exact nodes depend on the selected rule location.

### Examples / smoke checks

Run `python scripts/claim_check.py` on the proposal and applicable prose gates
for the eventual change. The trial's customized and planted-link controls must
show their initial state and resulting bytes, including the outside sentinel.

#### Security preflight -- five questions

**S1:** Project paths, lock/base data, Git objects and customizations can be
project-controlled; the operator selects trusted source versions and host Git.
The trial supplies synthetic data, not authority to change a real project.

**S2:** A planted link directed at an outside sentinel tests the write boundary;
an intentional edit in a customized slot tests whether preservation can be
observed. These controls have not been run yet and must be recorded in the trial.

**S3:** The future plan names exact commands and inputs for both real entry
points and checks their observed output against the rule's shipped wording;
there is no new automated admission check in this proposal.

**S4:** Missing prerequisite, ambiguous output or an incomplete control leaves
the trial inconclusive; it never grants permission to bypass existing refusals.
No fallback to unsafe Git reads is authorized.

**S5:** A project-data attacker can plant paths or corrupt state. Concurrent
filesystem races and untrusted executable code remain outside the cited model;
the trial does not establish protection against them or all Git behaviors.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

The rule obscures an in-model attack or delays a necessary fix; the trial cannot
make the comparison reproducible; or its results are treated as proof that
Git or a migration is safe. Reconsider the rule or design on that evidence.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance
