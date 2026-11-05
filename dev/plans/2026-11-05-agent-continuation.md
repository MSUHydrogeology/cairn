# Plan: Continue agent-owned work

**Source proposal**: dev/proposals/archive/2026-11-03-claude-agent-continuation.md
**Author**: Codex Terra (ordinary plan author; medium)
**Status**: ready-to-implement
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-05
**In brief**: Show the next permitted owner and help agents continue their own drain work within existing limits.
**Elapsed**: unknown
**Tokens**: unknown

## Source proposal

The heavy Decision accepts A-C first and a trial before a Maintainer decision
whether to keep D. D also needs the accepted metered-cost spending stop. The
proposal's F1-F6 and SR1-SR4 responses bind this plan; neither opening nor
review grants the later decision.

## Scope

Deliver `--next`, advisory post-commit output and the drain-only sentence;
trial them before the conditional loop. Update `tools/board.py` and its shipped
`templates/skills/_lib/board.py` twin, the team-gated intent hook and shipped
copy, session-start skill, and `docs/build-a-board-view.md`. Preserve plain
board and `cairn-board/1`; `--next` has a separate JSON schema. Without the
coordination module, A and C remain available, not B or claim checking.

Proposed paths:
- `tools/drain_loop.py`

**Reuse.** Searches of `tools/board.py`, `tools/session.py`,
`tools/_intent/`, shipped twins and `bootstrap/tests/*board*` found board
enumeration/header parsing, lifecycle vocabulary, claim resolution and hook
builders, but no next-owner selector. Preserve existing best-effort callers;
add a strict option to the existing `record_io.read_log` for NEXT. When the
coordination module is present, malformed JSON, nonobjects, unknown events,
missing or ill-typed claim/release fields, and missing, unreadable or linked
ledgers stop. Reuse `shared._shared_intents_path` and its
`_INTENTS_LOG_FALLBACK`: any fallback reason stops NEXT; `None` is the normal
main-checkout success. Resolve identity through its existing owner; unknown
identity stops when claim checking is needed, another's conflicting claim
stops, and an own claim grants no role or Decision. Use only trusted installed
`_intent` helpers, never import code from a `--root` target; read ledger data
through the validated resolver. These are implementation requirements, not
claims that current guards exist. The ledger is neither authentication nor a
mutex. A foreign root without a verifiable resolver stops; never borrow a local
clear result. Inconsistent role or Decision evidence stops and a claim proves
neither. Without the module, explicitly report that claim checking is unavailable;
do not claim no conflicts. This is the parent High judgment for accepted SR4,
not a new registry.

### Documentation / doctrine surface

Describe the table, filename rule and conditional loop in the board guide and
coordination module; revise the board docstring and session-start step 2.
The sole new prescription is in drain step 4; apply the doctrine rate-limit
gate. No global autonomy change.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | A-C and trial | Reviewed plan; boundary design settled | Board selector, advisory hook, drain sentence, measured three-item trial |
| C2 | D decision | C1 trial; MAINTAINER-GATED | Present results and ask whether to keep D; no assumed answer |
| C3 | Conditional D | Explicit keep-D Decision and completed 2b spending stop | Bounded opt-in loop, tests and usage documentation |

If D is not kept, record the Maintainer's actual scope disposition; do not
claim D delivered. If D is kept but 2b is incomplete, C3 remains blocked.
At the fence use the template's Waiting line. The current 2b plan is
`revising-plan`; no consent to private data or D decision exists.

## Acceptance criteria

**C1.** Select an advisory owner and move from written fields, review headings
and Decision blocks; NEXT does not grant authority or establish completion.
Missing, duplicated, conflicting, unreadable or unrecognized authority stops.
Independent full-match `YYYY-MM-DD-<lowercase-hyphen-words>` precedes any
display or selection; hostile nonmatches stop without echo. One line names
role, tier, full artifact path and move, or `NEXT: stop -- <reason>`. Stop for
Maintainer work, another claim or an unreadable claims log. Preserve board
enumeration and unjudged existing outputs. Table, per artifact kind:

| Status | Next owner, floor, move |
|---|---|
| proposal `awaiting-review` | ordinary reviewer, medium; review, unless a required outstanding Security Review is next |
| proposal `revising` | Security reviewer, high, if required and missing; otherwise author, medium, respond/revise |
| proposal `awaiting-decision` | stop: Maintainer Decision |
| proposal `accepted` | light: implementer, low, complete accepted scope and applicable checks in the proposal; standard/heavy: plan author, medium, triage and open a plan when required, or follow the existing explicit trivial/no-plan contract |
| proposal `rejected` | stop: terminal |
| proposal `superseded` | stop: terminal |
| plan `awaiting-plan-review` | ordinary plan reviewer, medium; or required outstanding Security reviewer, high |
| plan `revising-plan` | Security reviewer, high, if required and missing; otherwise plan author, medium, revise/respond |
| plan `ready-to-implement` | implementer, low, start reviewed plan |
| plan `implementing` | implementer, low, continue accepted work |
| plan `awaiting-code-review` | ordinary code reviewer, medium, first; then separate Security reviewer, high, when owed and missing |
| plan `revising-code` | Security reviewer, high, if required and missing; otherwise implementer, low, fix/respond |
| plan `ready-to-archive` | implementer, low, complete required archive preparation |
| plan `archived` | stop: terminal |

For plan `revising-plan` and `revising-code`, an ordinary review that moved the
header does not displace an outstanding required Security Review. For code review, ordinary
precedes Security; neither substitutes for the other. Only select a review when the written record unambiguously establishes the
outstanding obligation and eligible next move; absent proof of Decision, plan
join, review disposition, fence or ownership stops. Never echo an invalid or
unknown name anywhere, including a stop reason. A waiting line or reached
fence stops. Never treat a status alone as authority. Role floors follow
`dev/.cairn/model-selection-mapping.yml` and `AGENTS.md`; design/security
judgment remains high even during low-tier execution. Hook failure cannot
block a commit; drain continues only its own role and target, with fresh
subagents for reviews. For accepted light work, the proposal holds Boundary B
after final integration, then archives; no plan opens. A Boundary B heading
alone proves neither completion nor archive readiness. If the written record
does not unambiguously justify archive, NEXT names the same implementer's move
to complete accepted scope and applicable checks; the owner reads the evidence
and checks all criteria before archive. See `docs/methodology/lifecycle.md`
and `docs/methodology/plans.md` on light verification and archive. Unknown
Decision tier, inconsistent evidence, a declared wait or reached fence stops;
never downshift a task's floor automatically.

Run one lower-tier three-item practice board without B and C, then with both,
recording typed continue counts and conditions. Include an accepted light item
through implementation, verification and archive, alongside standard work;
do not claim improvement without measurements.

**C3, only after both gates.** `tools/drain_loop.py` reads settings once from Git administration,
refusing links and tracked files; command resolution follows
`bootstrap/SAFETY.md` rule 10. Bind settings and the meter's actual delivery
and admission interface to the eventual accepted 2b implementation; do not
invent an onboarding or delivery mechanism. Each item refreshes the spending stop and reads
`--next`, then launches a configured tier command as argv, no shell, with the
full artifact path as one argument. Default limit is five with per-item timeout.
Stop on selector stop, missing command, limit/timeout, failed agent, dirty
tree, no new commit touching the artifact, newly written Maintainer-only
status, or stale/missing/unreadable input. Report items, commits and reason.
The loop runs only when explicitly invoked. An artifact can still instruct its
agent but cannot select command, target or limits.

## Scope delta

**Scope delta**: preserved. Conditional D remains accepted and unresolved;
only the Maintainer can authorize a reduction.

## Verification

Boundary A uses `python tools/test_tiers.py for <changed paths>` and prose
claim, link, snippet and neutrality gates. Extend existing homes:
`bootstrap/tests/test_board_json_contract.py` for both schemas and real board
entry point; `bootstrap/tests/test_intents_tool.py` for real ledger resolution,
malformation, identity and hook output/nonblocking behavior;
`bootstrap/tests/test_session_start_drain_rules.py` for drain scope and fresh
reviews; existing skill installation tests for shipped twins. Test every table
row, conflicting/missing authority, each SR1 hostile name, each stop and
actual consumers, including no coordination module. Use synthetic projects,
not fake success evidence. Exercise valid unfinished and completed light work,
missing or ambiguous Decision/review evidence, claims and fences through the
real board entry point; a bare Boundary B heading must not authorize archive.
Add loop tests in the existing test home for actual
CLI behavior and each stop, including meter failure; the fake command is only
the launched agent. S2 mutations removing filename, dirty-tree and
Maintainer-status guards must each fail their tests; S3 tests explicit invocation.
S1/S4/S5 remain the accepted preflight. Scientific check: N/A.

Ordinary and separate Security code reviews falsify committed work before a
wide Boundary B on a clean final commit with canonical Python 3.13.x: reviewed
range's selector list plus named integration/workflow consumers and gates.
Record SHA/range, interpreter, clean pre/post state, commands, counts, elapsed,
tokens or unknown, non-passes, mutations and omissions. No full suite is
authorized by this plan opening.

## Plan review -- Codex Terra (MEDIUM) -- 2026-11-05

**Foundations**

1. **Should this happen as framed?** Yes. C1 covers the fourteen current statuses but stops on ambiguous authority; C2-C3 retain the Maintainer's keep-D decision and the spending-stop dependency -- accepted proposal, Decision and F1-F6/SR1-SR4 response; plan, C1-C3; `tools/session.py::_STATUS_VOCABULARY`.
2. **Best alternative.** Deliver and measure A-C first, as planned; this can expose whether a loop is useful without preempting the conditional Decision or inventing a meter -- accepted proposal, Alternatives; plan, Sequence and C3.
3. **What would show it wrong?** A malformed ledger or hostile filename producing a selectable step, an ambiguous review assigning the wrong role, or a loop launching after a meter failure would falsify the implementation -- plan, C1 and Verification; `tools/_intent/record_io.py::read_log`.

Reviewed commit: f5adce2e9de0d39b41842ec84766b9e5ec7cd39f

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: SHIP

The current reader skips malformed lines and treats a missing log as empty; the planned strict mode must change that for NEXT without changing existing callers. A claim is not authority, and an unverifiable foreign root stops. The trial measures typed continuations rather than assuming benefit. D remains conditional, with no inferred consent or automatic scope concession.

**Elapsed**: unknown. **Tokens**: unknown.

**Coverage**: Committed plan, accepted proposal, reviews, response and Decision, current plan template, status vocabulary, claims reader/resolver and drain skill. **Not covered**: implementation, actual hook delivery, identity and ledger probes, meter interface, trial, Security Review or suite.

## Plan review -- Codex Sol (HIGH) -- 2026-11-05

**Foundations**

1. **Should this happen as framed?** The safety envelope preserves limits, but default light work cannot continue -- plan, C1 accepted-proposal row; `AGENTS.md`, Lifecycle/Review; accepted proposal, A/F1 response.
2. **Best alternative.** Trial thin A-C before D; complete light using existing records, not another status or registry -- accepted proposal, Alternatives/Decision; plan, Sequence.
3. **What would show it wrong?** Authorized light work always stopping, malformed claims producing NEXT, or a missing meter permitting D falsifies delivery -- plan, C1/C3/Verification; `tools/_intent/record_io.py::read_log`.

Reviewed commit: f5adce2e9de0d39b41842ec84766b9e5ec7cd39f
Ordinary review read: 72ad37e4.

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: one blocking contract gap, 8B-1
**Verdict**: REVISE

**8B-1 -- Default light work has no continuation path.** C1 permits an
accepted proposal only to open a standard/heavy plan; otherwise it stops.
`AGENTS.md` makes light the default with no plan, and current doctrine places
its final verification in the accepted proposal. Thus even explicit accepted
authority and unfinished agent-owned work always stop. Missing execution
evidence is not itself missing permission.

Close with an explicit light branch and its written-evidence rules for
implementation, verification and archive preparation, preserving task-based
model floors and all existing stops. Real-entry tests must distinguish valid
unfinished light work from ambiguous/missing Decision or review evidence,
claims/fences and completed work. Do not infer authority merely from status,
an own claim or absence of a completion record.

C1 requires strict NEXT reads to reject malformed/nonobject/ill-typed ledgers,
missing/linked logs and resolver fallbacks without changing legacy readers.
Helpers must remain trusted installed code, never loaded from `--root`;
foreign-root uncertainty stops. Optional-module absence means unavailable
claim checking, not conflict freedom; claims are neither authentication nor a
mutex. D requires both the keep Decision and completed spending stop;
current meter-plan status supplies neither consent nor an interface.

**Elapsed**: unknown. **Tokens**: unknown.

**Coverage**: Committed plan/source/reviews/response/Decision, ordinary review,
current template, light-lane doctrine, board reader, claim resolver/reader,
drain skill and test bodies. **Not covered**: implementation, strict-ledger
execution, hook delivery, meter binding, actual trial or host-command controls.
No tests or suite run; no authority or scope waiver granted.

## Response -- Codex Terra -- 2026-11-05

**Model**: Terra (medium). Responds to ordinary review `72ad37e4` and
Security Review `99411c1b`; their records remain unchanged.

- **8B-1 -- accepted.** C1 now gives accepted light work an implementer and
  carries its scope, checks, Boundary B and archive on the proposal. This
  repairs the default lane's stop while retaining Decision, claim, wait and
  fence stops. NEXT is advisory, not proof of completion or authority; the
  owner examines the evidence before archive. Verification tests the real
  entry point and C1's mixed trial includes light through archive. The parent
  High judgment supplied the light/advisory clarification; no new proof parser,
  status or registry is required.
- **Security boundary and D comments -- retained.** Strict claims handling,
  trusted installed helpers, foreign-root refusal and the optional-module
  limitation remain in Scope; D still requires the actual keep-D Decision and
  completed spending stop. Neither the meter plan nor this response grants
  consent or permits activation.
- **Ordinary review -- no findings.** Its coverage and unmeasured items remain
  recorded; implementation and the trial have not run.

**Elapsed**: unknown. **Tokens**: unknown.
