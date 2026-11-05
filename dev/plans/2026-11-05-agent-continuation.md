# Plan: Continue agent-owned work

**Source proposal**: dev/proposals/archive/2026-11-03-claude-agent-continuation.md
**Author**: Codex Terra (ordinary plan author; medium)
**Status**: awaiting-plan-review
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

**C1.** Select from written fields, review headings and Decision blocks only;
missing, duplicated, conflicting, unreadable or unrecognized authority stops.
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
| proposal `accepted` | plan author, medium, for standard/heavy with no plan; otherwise stop |
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
subagents for reviews. Run one lower-tier three-item practice board without B
and C, then with both, recording typed continue counts and conditions; no
claimed improvement without measurements.

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
not fake success evidence. Add loop tests in the existing test home for actual
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
