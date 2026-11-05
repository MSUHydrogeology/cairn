# Complete implementation plans without human-run operations

**Author**: Codex (inherited runtime; exact model identifier unavailable)
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-03
**In brief**: Finish implementation plans on agent-owned delivery and track human-run trust and release work separately, without relaxing its safeguards.
**Implementation plan**: `dev/plans/archive/2026-11-04-implementation-plan-completion.md`

## Decision summary

An implementation plan should finish when its implementation, review and
change verification are complete. Do not give it a final chunk that only the
Maintainer can execute, such as signing, re-anchoring or publishing. Put those
operations in named `dev/PLANNING.md` rows with their evidence requirements
and links back to the implementation. Archiving code work is not permission
to activate or release it.

The Maintainer requested this policy and its shipment to adopters. This
codification uses existing board markers and records; no new tool, status,
register or routine is proposed.

## Context

Target release: **v0.7**, as directed by the Maintainer on 2026-11-03.
This does not gate or widen the v0.6.1 implementation.

Cross-checkout evidence: the repair plan cited below lives on `0.61-dev` at
`10d98e18`, not in this checkout. Read its committed Git object; the imported
review's citation is retained unchanged.
External-repo paths: `dev/plans/2026-11-03-v061-upgrade-repairs.md`

The repair plan's C5 required a Maintainer ceremony after both code reads had
accepted the source. Its code could not finish its lifecycle without a human
operation. `dev/plans/2026-11-03-v061-upgrade-repairs.md` records the problem
and the Maintainer's explicit transfer to the release board.

This recurs, rather than deriving doctrine from one incident. Within
2026-10-28 through 2026-11-03, two committed records show occurred impact:
`dev/plans/archive/2026-10-28-scoped-change-verification.md` records clean code
held for a frozen-file ceremony and the Maintainer's eventual scope amendment;
the current repair plan repeats the hold. These are the recurrence basis for
the doctrine-evolution rule, not a claimed high-risk bypass.

Current instructions actively teach the coupling: the plan templates'
Sequence sections prescribe Maintainer-only chunks; their Waiting-line and
code-review instructions reinforce it. `templates/core/dev/PLANNING.md`
already supports separate human-operation waits. `tools/board.py::_roadmap_waits`
reads standalone markers, not markers hidden in table cells.

## Rationale

Separate two outcomes: delivering reviewed code and authorizing its use.
One human operation can cover several completed implementations without
keeping every implementation plan open. The board retains the outstanding
work, its owner, source and required evidence.

Direction and permission are not execution. Proposal Decisions, scope
concessions and unexpected-boundary stops remain the Maintainer's. A plan
must still pause if the agent lacks authority or understanding. The rule
forbids designing a routine human operation into plan completion; it does
not promise that agents never consult people.

**Documentation / doctrine surface:** update live and shipped `AGENTS.md`,
both plan templates, the shipped roadmap template and corresponding
methodology (`docs/methodology/plans.md`, `docs/methodology/lifecycle.md`).
Update proposal guidance only where needed to stop assigning human
operations as implementation acceptance criteria. Preserve scientific,
functional and security verification requirements.

## Alternatives considered

Keep the current fence inside every plan: no editing cost, but recurring
human waits obscure finished code and repeat the handoff. A separate release
plan still needs a human to finish and recreates this problem. Existing board
rows are enough; another workflow engine would add unnecessary burden.

The proposed split costs a small amount of board upkeep and careful wording.
Its main risk is using a handoff to hide unfinished implementation. Retain
the accepted scope floor and all agent-owned checks. No unresolved code
defect, missing functional/scientific evidence or required review becomes
an operational row merely to close a plan. Classify by the actual pending
human operation and its evidence, not the word "trust". Reviewed source
awaiting human baseline installation stays explicitly unpassed under that
named operation; an unexplained integrity failure stays implementation work.
The handoff never makes an arbitrary failed check transferable or green.

## Evidence / verification plan

Extend an existing shipped-doctrine test home, not a new checker. Exercise
fresh installation through `bootstrap/scaffold.py` and inspect emitted
doctrine, plan and roadmap instructions. A deletion or contrary-instruction
mutation must fail for each required surface. Existing scope-floor,
verification-boundary and release-gate controls must still pass.

Run `tools/test_tiers.py for` changed paths with the reviewed range; use
scoped claim/link/content, snippet and neutrality gates. Final change
verification uses one clean committed copy after code review. No certifying
suite or ceremony is added. Current repair work retains its own verification.

### Security preflight

**S1:** The Maintainer supplies policy authority in chat; authors supply
plans/board text and reviewers assess committed evidence. Board text is not
authentication, execution authority or proof that an operation passed.

**S2:** Proposed test mutations remove the split, delete preserved-check
wording, or reinstall a human-only completion criterion. They have not run
yet; implementation must record their failures before claiming coverage.
Text tests cannot establish honest agent behavior by themselves.

**S3:** The existing affected-test selector supplies the iteration input set;
the installed-tree checks exercise the scaffold's real output. Intended
adopter sentence: "Human-run trust and release operations belong on the
planning board, not in an implementation plan's completion criteria."

**S4:** No parser, fallback or execution authority changes. A missing handoff
or unmet applicable code check keeps implementation incomplete. A pending
trust/release obligation keeps that operation blocked, never silently green.

**S5:** This assumes a cooperative team. A dishonest agent can still falsify
a board entry; this documentation is not containment or automated release
enforcement. Existing ceremony and release controls remain authoritative.

**Independent scientific check:** N/A; no scientific assumption or result changes.

## Signals the change is wrong

Plans still end in human-only chores; adopters receive contradictory advice;
or an agent treats archive as authority to skip a check, sign or publish.

## Scope delta

Preserved: all implementation outcomes and existing human authority. This
changes the home and completion dependency of operational work, not whether
it is owed. No global retroactive rewrite of archived records.

## Assurance path

**Assurance path**: high-assurance. Governing and shipped doctrine are named
protected surfaces; ordinary and Security Reviews remain separate.

**Elapsed**: approximately 8 minutes. **Tokens**: unknown.

## Review -- Codex-usual-completion (inherited runtime; exact identifier unavailable) -- 2026-11-03

**Foundations**

1. **Should this happen as framed?** Yes. Separating delivered implementation from permission to activate it addresses two recorded ceremony holds, not unfinished code -- `dev/plans/archive/2026-10-28-scoped-change-verification.md`, Response to code review and Scope amendment; `dev/plans/2026-11-03-v061-upgrade-repairs.md`, Maintainer scope amendment at `10d98e18`.
2. **Best alternative.** Keep case-by-case scope amendments: no doctrine-edit cost, but both incidents required another human handoff. Existing board rows avoid a new release-plan lifecycle -- `templates/core/dev/PLANNING.md`, Waiting on you and Working rules; `tools/board.py::_roadmap_waits`.
3. **What would show it wrong.** Moving a missing scientific result, broken code or required implementation review onto the board would defeat completion. The proposal expressly forbids all three and retains scope-change authority -- Alternatives considered; `AGENTS.md`, Working tree and commits.

```
Reviewed commit: 13bd71e51467b429262fca85c2d8ab6e81d85cbb
Target: opening proposal; recurrence, lifecycle, scope and adopter reach
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: none
**Verdict**: ACCEPT

The split preserves every code goal and applicable check. An unpassed trust
result remains unpassed; archive grants no release authority. Live doctrine
and adopter templates are both in scope, with contrary-instruction mutations
owed during implementation.

**Elapsed**: approximately 4 minutes. **Tokens**: unknown.

**Coverage**: Read committed recurrence records, both plan templates and
methodology. On an isolated copy, Python 3.13.13 passed one targeted board
contract test; the real board command displayed the standalone wait, while a
table-cell mutation hid it. Repeatable probe:
`/private/tmp/cairn-usual-completion-board-probe.py`.
**Not covered / low confidence**: Security Review, future implementation,
installed-output mutations, scientific execution and release ceremonies;
no full suite run.

## Review -- Codex Security Reviewer (inherited runtime; exact model identifier unavailable) -- 2026-11-03

**Foundations**

1. **Should this happen as framed?** Yes. Separating reviewed implementation from human activation addresses two recorded holds without transferring authority -- scoped-change-verification archive, Scope amendment; v061 repair plan, Maintainer scope amendment at `10d98e18`.
2. **Best alternative.** Retain existing board rows and standalone wait markers. Keeping ceremonies inside implementation plans preserves the hold; another operational workflow adds machinery -- `tools/board.py::_roadmap_waits`; shipped roadmap template, Waiting on you.
3. **What would show it wrong?** Transferred functional/scientific failures, missing reviews, or archive treated as signing/publication permission -- Alternatives considered; S4; `bootstrap/REANCHOR_RUNBOOK.md:3`.

```text
Reviewed commit: 13bd71e51467b429262fca85c2d8ab6e81d85cbb
Target: operative proposal, S1-S5, recurrence and trust boundaries
Prior findings: none
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: none
**Verdict**: ACCEPT -- proposal only.

The split preserves permission, checks and outstanding obligations.

On a separate clean copy of `1273e3f7`, Python 3.13.13 `repin.py status`
reproduced 11 changed baseline symbols, two known-new rekeys, six frozen
modifications and 0/12 changed authority files. Source diff, AST test bodies
and AST runbook support pending trust accounting, not a generic exception
for failing code checks. Results remain unpassed; final agent-owned Boundary B
remains owed.

S1/S4/S5 preserve board-as-data, Maintainer authority and unexpected-boundary
stops. S2/S3 are prospective: installed-output coverage and per-surface
mutations remain implementation obligations.

Latest Maintainer direction assigns policy implementation to v0.7. This
review does not gate v0.6.1 or replace its directly authorized scope amendment.

**Elapsed**: unknown. **Tokens**: unknown.

**Coverage:** committed doctrine, templates, recurrence, source/status evidence
and scratch board command. **Not covered:** implementation-test reruns, future
mutations, full suite, native reruns, cryptographic authentication or
ceremonies; no operational authority granted.

## Review -- Codex gpt-6.1-terra (Maintainer-called Reviewer) -- 2026-11-03

**Foundations**

1. **Should this happen as framed?** Yes: separate finished agent-owned work from human trust/release operations while keeping their permissions and evidence. Two actual scope amendments show the hold; neither grants release authority -- scoped-change-verification plan, Scope amendment; v061 repair plan at `10d98e18`, Maintainer scope amendment.
2. **Best alternative.** Continue case-by-case Maintainer amendments and board rows: no doctrine migration, but repeated intervention and no general guidance. The neighboring continuation proposal addresses selecting agent-owned work, not this completion boundary; neither needs to absorb the other -- Alternatives considered; continuation proposal at `29202b7b`, Proposal A-D.
3. **What would show it wrong?** A required functional failure or review moved to the board, or archive treated as permission to sign or publish, defeats the split -- Alternatives considered and Security preflight S4; v061 amendment at `10d98e18`.

```text
Reviewed commit: 3f3f33f286dcef9d83ca63ebb1e71442ab00779d
Target: operative proposal, recurrence, authority and overlap
Prior findings: none
Assurance path: high-assurance
```

**Tier**: External
**Called by**: Maintainer -- chat, 2026-11-03

> Go ahead and send that new proposal to a Terra reviewer in the 0.7-dev branch.

**Findings**: one non-blocking recommendation
**Verdict**: ACCEPT

Clarify in implementation guidance that a failed check is not transferable merely because it concerns trust: identify the pending human operation and its evidence, retain the failure as unpassed, and keep independently agent-owned checks and defects open. The v061 amendment distinguishes two stale-baseline failures from final wide Boundary B; S4 and Alternatives intend that distinction but do not spell out the classification. An explicit example would close this ambiguity.

**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Coverage**: committed proposal, imported reviews, cited amendments and neighboring proposal. Distance: Terra model in Codex; no claim of a different agent type. Not covered: implementation, independent Security Review, tests, release operations or full suite; this read grants no authority.

## Response -- Codex -- 2026-11-03

The usual and separate Security passes accepted without findings. Terra's
non-blocking recommendation is accepted: Alternatives now classifies by the
actual pending human operation, keeps its result unpassed, and contrasts
reviewed source awaiting baseline installation with an unexplained integrity
failure that remains implementation work. No agent-owned check or defect
can be transferred merely because it concerns trust.

Implementation is for v0.7, not the v0.6.1 patch. The neighboring continuation
proposal selects next work; this proposal defines completion, so neither
absorbs or widens the other.

### Withdrawn / superseded commitments

None. The Maintainer assigned the release timing; all proposed outcomes remain.

**Elapsed**: approximately 2 minutes. **Tokens**: unknown.

## Decision -- Maintainer -- 2026-11-03

**Tier**: heavy

**ACCEPTED for v0.7.** Scribed by Codex under the Maintainer's explicit chat
authorization after the usual, separate Security and named Terra reviews:

> Yes, record the Decision and implement after review

> We need to codify this in our templates and doctrine.

> And that shipped to adopters.

The subsequent release assignment and priority are binding:

> I think this proposal should be in v0.7

> Let's get v0.6.1 out

Accept the complete current contract, including live and shipped doctrine,
templates, corresponding methodology and falsifiable installed-output checks.
Human-run operations remain blocked until their own evidence and authority
exist; agent-owned checks, defects and accepted scope cannot be handed off
merely to finish a plan. Decision and permission stops remain unchanged.

Queue implementation for v0.7 after the patch; no policy implementation or
new plan is opened as a v0.6.1 release prerequisite. The heavy-tier plan,
independent reviews and final change verification remain required when that
work starts. Recurring addition: existing board handoff upkeep only; no new
tool, routine or lifecycle stage.

**Elapsed**: less than 1 minute. **Tokens**: unknown.
