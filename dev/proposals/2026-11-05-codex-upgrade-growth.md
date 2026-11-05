# Bound Upgrade Growth and Trial a Git Merge

**Author**: Codex GPT-5 (Proposal author)
**Status**: accepted
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
   For Git writes and the existing upgrade alike, the plan must specify an
   operating-system-enforced isolated environment with no network and no write
   access to real project, home or Git administration data. Put the sentinel
   outside the scratch project but inside the isolated writable area. Use a
   trusted host Git and controlled environment and configuration, disable
   hooks and external filters, and prevent repository-supplied commands from
   running. Git configuration alone is not an isolation boundary. Before the
   comparison, demonstrate that a write to a protected outside location is
   denied, and that a deliberate write to the sentinel is detectable; record
   the commands and results. If isolation or either control cannot be shown,
   stop the write trial and record it incomplete. These controls do not prove
   Git safe on an adopter's machine.
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

## Review -- Codex GPT-5 -- 2026-11-05

Reviewed commit: 07366b969a2c0cd90cfedb611a800c30cbe74ab2

**Tier**: usual
**Findings**: raised
**Verdict**: ACCEPT

**Elapsed**: approximately 4 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: it preserves existing protections and tests a possible simplification without authorizing replacement; both outcomes match board 7d. Evidence: `dev/PLANNING.md` 7d; Proposal 1-3.
2. **Best alternative.** Keep the current engine and add no rule or trial; it avoids recurring policy and trial costs but leaves the proposed comparison unmeasured. Evidence: Alternatives considered; `bootstrap/_scaffold/merge.py` `_three_way_merge`.
3. **What would show it wrong?** Withdraw or redesign the rule if a realistic in-model threat is obscured, or the trial if it cannot reproduce both paths and their resulting bytes. Evidence: Signals the change is wrong; `bootstrap/SAFETY.md` documented residual risks.

The proposal turns the strategy's growth concern into a bounded comparison while retaining the Maintainer's risk authority. Its distinction between hostile project data and the stated race and untrusted-code exclusions is important.

**F1 -- Advice:** Specify how the scratch Git *write* operations are isolated from hooks, configuration and outside paths, and what evidence establishes that isolation. The 2d prerequisite concerns Git reads, so its availability alone does not establish safe merge or commit execution. Close by naming the write-side controls and their limits in the trial plan. Evidence: `dev/proposals/2026-11-04-codex-safe-git-reads.md`, caller scope and separate write/ceremony runners; Proposal 2.

**Coverage:** Read the committed proposal, template, board 7d, cited strategy, safety assumptions, merge implementation and 2d scope. No trial, mutations, complete engine trace or independent Security Review was run; the separate Security Review remains owed.

## Response -- Codex GPT-5 -- 2026-11-05

**F1 -- Accept.** The trial now requires write-side isolation, controlled Git
execution, and denial and sentinel positive controls; the Git-read prerequisite
does not supply these. The separate Security Review remains owed.

**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

### Withdrawn / superseded commitments

None.

## Review -- Sol (gpt-6.1-sol, High-tier) -- 2026-11-05

Reviewed commit: b6a5e2467b4314f5db4a6c3bae32d07f6bd75a08

**Tier**: Security Review
**Findings**: none
**Verdict**: ACCEPT

**Elapsed**: approximately 6 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: the rule demands an evidenced threat without removing protection, and the comparison cannot authorize replacement. Hostile project data remains in scope despite the race and untrusted-code exclusions. Evidence: Proposal 1-3; `bootstrap/SAFETY.md`, documented Layer 4 residuals; `bootstrap/_scaffold/security.py`, `_assert_safe_write`.
2. **Best alternative.** Retain the current engine without the trial or new rule: this avoids isolation setup and recurring review wording, but leaves the Git alternative unmeasured. Git already supplies text merging, not the whole write boundary. Evidence: Alternatives considered; `bootstrap/_scaffold/merge.py`, `_three_way_merge`.
3. **What would show it wrong?** Try a committed dangling link and linked parent on both paths, under the same isolation policy used for the denial and sentinel controls; an escape, undetected sentinel change or skipped control must prevent a safety conclusion. Evidence: Proposal 2-3; `bootstrap/tests/test_upgrade_refuses_hostile_project_data.py`, `test_apply_never_creates_a_profile_through_a_link` and `test_init_lock_refuses_a_mapped_file_below_a_linked_parent`.

No security defect found in the proposed authorization. Project-controlled
paths, metadata and Git attributes could redirect writes or select programs;
the revision requires operating-system isolation, controlled execution and
prevention of repository-supplied commands, not merely Git configuration pins.
The protected-location denial and deliberate sentinel write test different
properties: confinement and observation. Neither establishes universal safety.
The separate 2d read prerequisite remains a wait, not permission for writes.

The refusal rule also closes the strategy's dangerous shortcut: an
out-of-model label does not accept risk. Unexplained threats remain open,
existing checks remain required, and only the Maintainer disposes of risk.

**Coverage:** Read the committed proposal, review template, strategy, board 7d,
2d boundary, safety residuals, containment/merge code and hostile-test cases.
No trial, isolation demonstration, mutations, engine tests or full suite run;
the plan must still establish executable isolation and case-by-case evidence.

## Review identity correction -- gpt-6.1-terra -- 2026-11-05

The coordinator assigned Sol for review `a1a76899`, but the actual runtime
model during that review was not confirmed. The Sol byline records the
assignment, not a verified runtime. The current resumed runtime is
gpt-6.1-terra; that does not establish the earlier runtime. The Security Review
obligation remains outstanding pending a reviewer verified at High tier.

**Elapsed**: approximately 1 minute. **Tokens**: unknown.

## Response -- Codex GPT-5 -- 2026-11-05

The ordinary review's F1 was accepted and addressed in the earlier response.
The Security Review at `a1a76899` raised no findings; no further operative
revision is needed on that review. Its proposed trial controls remain evidence
for the plan, not a claim that the trial has run.

The coordinator confirms in chat that the original reviewer was spawned with
the tool's `gpt-6.1-sol` model override, with no evidence it ran otherwise.
The subsequent identity note did not verify the original runtime either way.
The Maintainer clarified in chat on 2026-11-05:

> "Don't worry about the author line--that is often wrong. Just trust your own processes. You are the only person developing here now."

On that basis this response treats `a1a76899` as the Sol-assigned Security
Review and advances to the Maintainer's Decision; it does not claim an
independent runtime measurement. The original review and identity note remain
intact.

**Elapsed**: approximately 2 minutes. **Tokens**: unknown.

### Withdrawn / superseded commitments

None.

## Decision -- Anthony Kendall -- 2026-11-05

**Decision**: accepted as framed. The proposal retains both outcomes and its
heavy tier: the upgrade-refusal review rule and the bounded, isolated Git
comparison. The ordinary review's finding is addressed; the Security Review
raised no findings, and the response records the Maintainer's clarification
about the reviewer's assigned model. No scope is removed or deferred. The
required plan review remains Internal plus Internal Security Review.

**Material recurring additions**: the new review guidance applies to future
upgrade-refusal proposals, and the comparison requires one isolated session
with operating-system controls. This evidence will not authorize a production
Git replacement.

**Called by**: Maintainer -- chat, 2026-11-05

> “Oh, please scribe my acceptance on those proposals and mark them as ready to implement”

**Elapsed**: approximately 4 minutes. **Tokens**: unknown.
