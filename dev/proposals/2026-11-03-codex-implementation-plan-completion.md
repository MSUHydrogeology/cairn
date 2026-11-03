# Complete implementation plans without human-run operations

**Author**: Codex (inherited runtime; exact model identifier unavailable)
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-03
**In brief**: Finish implementation plans on agent-owned delivery and track human-run trust and release work separately, without relaxing its safeguards.

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
an operational row merely to close a plan. A pending trust-installation
result stays explicitly unpassed and continues to block the relevant
operation; it is not an automatic exception for arbitrary test failures.

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
