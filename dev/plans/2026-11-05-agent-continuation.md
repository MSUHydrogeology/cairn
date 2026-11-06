# Plan: Continue agent-owned work

**Source proposal**: dev/proposals/archive/2026-11-03-claude-agent-continuation.md
**Author**: Codex Terra (ordinary plan author; medium)
**Status**: revising-code
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

## Maintainer scope disposition -- Luna LOW -- 2026-11-05

**Authority**: Maintainer chat, 2026-11-05. This is scope approval only; it
does not change plan status, complete implementation, satisfy a review or
check, authorize activation, or grant another review pass.

> Okay, move the budget guard and unattended loop to v0.8. Update the plan and PLANNING board, and let's get measurement and reporting moving for v0.7. I don't want the planning/proposal docs for this left over, so please make a new v0.8 proposal be part of closing out this plan.

**Disposition**: Move the automatic account-bound between-item budget guard
and conditional unattended loop to v0.8. For v0.7, measurement and reporting
for all three tools and advisory A-C remain in scope. No accepted privacy,
accuracy, required-trial, or retirement check is waived; no unmetered automatic
launcher is authorized.

**v0.8 handoff**: Before either v0.7 plan archives, write one current joint
v0.8 proposal for the deferred guard and loop and link it from both v0.7 plans.
The archived v0.7 source proposals remain unchanged. Review, Decision, and
implementation of the v0.8 proposal are not completion criteria for these
v0.7 plans.

**Plan handling**: Implementation has begun, so removal of the deferred work
must be recorded as an append-only scope amendment authored at Medium tier.
This authorization does not itself complete or authorize implementation of
the remaining v0.7 work.

## v0.7 scope amendment -- Codex Terra (MEDIUM) -- 2026-11-05

The Maintainer's disposition above amends this implementing plan without
rewriting its earlier operative text or history. **Scope delta: deferred** to
v0.8: old C2's keep-D choice and old C3's conditional unattended loop. Neither
holds this v0.7 plan open. No unattended launcher or budget guard is delivered
or activated by this amendment; v0.7 loses unattended launches, not the
safeguards on its advisory continuation work.

C1 remains binding: deliver A-C and the mixed light/standard three-item trial,
including its recorded typed-continue counts and conditions. The ordinary and
separate Security code reviews and the wide Boundary B after review remain
required for A-C. Existing authority, claims, selector, role, tier and stop
conditions remain in force. This amendment does not claim the prototype, trial,
reviews or checks are complete. Status remains `implementing`.

Before archive, ensure the one joint [v0.8 proposal](../proposals/2026-11-05-codex-budgeted-unattended-work.md)
exists, remains current with the deferred guard and conditional D, and is
linked from both this plan and the [meter plan](2026-11-04-metered-cost.md)
and the [planning board](../PLANNING.md). Its future review, Decision and
implementation are not v0.7 completion conditions. The later Maintainer
choice whether to keep D remains open; scheduling the proposal grants no
implementation, activation or private-collection permission.

**Elapsed**: unknown. **Tokens**: unknown.

## Implementation log -- A-C source checkpoint -- Codex Sol (HIGH) -- 2026-11-05

Source `04afb655` publishes advisory NEXT, strict opt-in claims reading,
generated-hook output and drain-only guidance. No live hook was installed;
no unattended loop, budget admission or private collection was added.

High author-side integration resolved two false-clearance risks before
publication: unknown review declarations now stop rather than becoming an
empty obligation, and strict readers check the opened ledger's identity and
named path before parsing. A synthetic leaf swap reproduced the old reader
accepting a different file; symlink/FIFO/regular swaps now refuse beside a
passing control. Later concurrent edits remain possible: this is not a lock.

**Disposition boundary.** A prior REVISE needs a later nonempty response in an
existing response section before the selector advises a post-review move.
This establishes recorded response coverage, not that findings were resolved.
The owner reads the actual findings, response, authority and checks; a response
cannot replace an owed Security Review or make a Boundary B heading sufficient
for archive. No new status, clearance field or registry was introduced.

**Boundary A:** clean committed `04afb655`, separate Git-backed copy, Python
3.13.13; clean pre/post. `tools/test_tiers.py for` on the commit's thirteen
changed paths selected 31 files. Pytest received those paths with `-q
--durations=10 --junitxml=/private/tmp/cairn-continuation-a-04afb655.xml`:
2,083 passed, one Windows-drive-normalization skip, zero failures;
235.12 seconds pytest / 235.89 seconds wall. Local test listeners were permitted.
No full-suite override or certification. Slow-file observations are in 2a.
Claim/content/link/snippet/neutrality/redundancy and byte checks passed;
all twelve candidate-publication hashes and four twin pairs matched.
Focused selector and reader controls were earlier passes, not added to this
node count. The original worker's pre-publication run reported eleven frozen
failures; those eleven passed on its clean committed candidate without changing
trust records or the verifier. They are not a green same-SHA union with this run.

**Still open:** mixed light/standard comparative practice trial, remaining
required guard mutations, ordinary and separate Security code reviews, and
final wide Boundary B. Duplicate review records remain a conservative stop,
not proof of conflicting authority. Status stays `implementing`; the v0.8
handoff remains linked by the scope amendment. **Elapsed**: 235.89 seconds
wall for mapped A; overall unknown. **Tokens**: unknown.

## Implementation verification -- Codex Luna (LOW) -- 2026-11-05

Bounded mutation checkpoint against clean `git archive` copies of source
`04afb65525c622afb58fe87f5dab97853e3030f6`, Python 3.13.13
(`/Users/kendal30/conda_envs/lhm/bin/python`). Controls:
`pytest -q test_board_json_contract.py::test_next_real_entry_covers_every_status_row
test_next_heavy_review_floor_is_not_downshifted
test_next_foreign_root_stops_without_echoing_invalid_artifact
test_intents_tool.py::test_next_installed_plan_review_and_identity_stops
test_strict_claim_reader_rejects_malformed_authority
test_strict_claim_reader_requires_existing_regular_ledger
TestInterpreterAndEndToEnd::test_generated_hook_captures_interpreter` --
24 passed. Also called `board.main --next --json` on synthetic eligible
artifacts: control stops for a Maintainer wait and hostile name.

Independent faults, each in a separate copy, were caught: heavy Security
review tier lowered (`test_next_heavy_review_floor_is_not_downshifted`);
conflict stop bypassed (`test_next_installed_plan_review_and_identity_stops`);
strict malformed-line rejection bypassed (five malformed payload cases);
Maintainer-wait guard bypassed (real entry returned implementer instead of
stop); hostile-name pattern widened (real entry selected and echoed the
hostile filename); generated hook changed from `--next || true` to `--json`
(`test_generated_hook_captures_interpreter`). The existing hostile-name test
alone did not catch its mutation because its fixture was not otherwise
selector-eligible; the additional CLI control/fault pair did. Hook generation
only occurred in the test's temporary synthetic repository; its hook was not
run. Fence/name CLI probes stubbed only claim resolution; the separate installed
claim test exercised the real resolver. No unattended launcher, meter, private
log, host configuration, user key, or live hook was exercised.

This is a bounded mutation checkpoint, not complete A-C falsification or
Boundary A/B. Unmeasured: remaining table/evidence mutations, every ledger
field and resolver-fallback mutation, additional generated-hook failure modes,
the mixed trial, ordinary and separate Security code reviews, and final wide
Boundary B. No source guard was found missing. This same-type source author
verification is not an independent code review. **Elapsed**: about 10 seconds
of test runtime, excluding setup and inspection. **Tokens**: unknown.

## Trial feasibility -- Codex Luna (LOW) -- 2026-11-05

**Disposition: not run; no trial observations collected.** The requested trial
requires a lower-tier agent to perform both three-item conditions, actual
typed-continue counts from a person, and distinct eligible roles to carry
accepted light work through implementation, verification, review and archive.
This session has no separate agent-runner or eligible independent role sessions
available. A simulated prompt, locally scripted continuation, or authored
review/archive record would manufacture the evidence the trial is meant to
observe. Synthetic CLI exercises alone would not satisfy the accepted practice
trial. No practice items were completed, so there are no starting conditions,
outcomes or counts to report.

**Smallest valid next step:** the Maintainer arranges an actual lower-tier
agent session and a person to record each continue they type, plus distinct
eligible reviewer(s) for the light and standard lifecycle steps. Run the same
isolated three-item board first without the advisory hook/drain sentence and
then with both; capture starting conditions, typed counts and item outcomes in
each arm. Until then the C1 trial remains open. No live hook, host setting,
private log, unattended launcher, spending guard, push or full suite was used.

**Elapsed**: about 3 minutes of inspection. **Tokens**: unknown.

**Coverage**: plan and accepted proposal trial requirements; available session
tooling and current plan records. **Not covered**: either trial arm, human
typed inputs, or separate role execution.

## Implementation verification -- Codex Luna (LOW) -- 2026-11-05

Bounded mutation checkpoint; not a review, Security Review, or Boundary B.
Source snapshot: clean commit
`7da64a9180688bd156b1630ad09972806992611c`. Candidate tests were committed
only in an isolated local clone as `1afa916a119de301b45a46e6671d7556445bba13`
(two owning test files); that candidate tree was clean before and after the
mapped run. The corresponding paths are unchanged at current branch commit
`725a23ab942e5beca9696a029885768a25bb68a9`.

**Positive controls and mapped checks:** Python 3.13.13. `python
tools/test_tiers.py for bootstrap/tests/test_board_json_contract.py
bootstrap/tests/test_intents_tool.py` selected exactly three files:
`test_board_json_contract.py`, `test_gate_manifest.py`, and
`test_intents_tool.py`. `python -m pytest -q --durations=10` on those files:
320 passed, 1 skipped, 0 failures, 36.42 seconds. The archive-evidence test's
valid code-review record routes to implementer/low; the installed CLI's empty
ledger routes to reviewer/medium. The table test keeps the Maintainer-only
`awaiting-decision` row at stop.

**Separate-copy mutations; each fault was isolated and its affected node
rerun:**

- Changed the `awaiting-decision` refusal to return an implementer move.
  `test_next_real_entry_covers_every_status_row`: 13 passed, 1 failed on the
  named `proposal-awaiting-decision` case; the expected refusal was lost.
- Bypassed the `ready-to-archive` required-code-review guard.
  `test_next_ready_to_archive_requires_code_review_evidence`: 1 failed because
  an unreviewed plan was selected instead of `archive status lacks required
  code reviews`. This was a genuine missing regression test; it now has a
  positive reviewed control in `test_board_json_contract.py`.
- Downgraded NEXT's strict ledger read to best-effort in both board twins.
  `test_next_installed_cli_refuses_malformed_ledger_and_resolver_fallback`:
  1 failed at the malformed-ledger case; the real CLI selected the reviewer
  instead of stopping with `claims ledger is unreadable or invalid`.
- Bypassed the resolver-fallback stop in both board twins. The same CLI node:
  1 failed only after its normal and malformed-ledger controls passed, when an
  invalid `.git` pointer should have produced `claims ledger is unreadable or
  invalid` but NEXT selected the reviewer. This was a second missing
  integration test; it now shares the owning installed-tool test.

The strict-reader test initially passed when only `tools/board.py` was mutated:
the integration fixture installs the shipped template twin. That attempt did
not exercise the fault; I repeated the affected check with the shipped twin
mutated (and both twins mutated for the final batch), which failed as above.
An earlier archive extraction lacked Git metadata and produced three unrelated
Git-history/gate-manifest failures; the mapped run was repeated on the clean
committed clone and passed. A temporary one-line archive mutation briefly
touched the shared source file during setup; I inspected and restored that
exact line immediately. It is absent from the candidate and commit.

No production guard was found missing. The two regression tests add no
production behavior. No formal code or Security Review, Boundary B, full suite,
live hook, host configuration, private log, unattended launcher, spending
guard, or push was performed. **Still open:** the mixed three-item human/agent
trial, required reviews and final wide Boundary B. **Elapsed**: about 10
minutes wall, including setup and mutation runs; mapped suite 36.42 seconds.
**Tokens**: unknown.

**Coverage**: every NEXT status row; ready-to-archive code-review evidence;
installed CLI behavior for malformed strict-ledger input and resolver fallback;
positive controls and the named mutations above. **Not covered**: other
strict-ledger field mutations, all remaining selector/evidence mutations,
hook delivery, the practice trial, formal reviews or Boundary B.

## Code review -- Codex Terra -- 2026-11-05

Reviewed source: `04afb65525c622afb58fe87f5dab97853e3030f6`; follow-up tests:
`204da99e1d3c013ac23c45461ff512b5f8bfe385`; plan and review basis:
`595a280b851b6c14acd0e6427752cc7c15cc0a44`.

**Foundations**

1. **Should this happen as framed?** Not yet: the advisory selector can name work despite contradictory or missing authority and a reached fence; C1 requires a stop -- `tools/board.py::_next_decision`, `_next_for_artifact`.
2. **Best alternative.** Keep the existing advisory design, but refuse ambiguous Decisions, missing source reviews and unresolved fences, with real-entry regression tests -- plan C1 and Verification.
3. **What would show it wrong?** Re-run the three counterexamples below through installed and no-coordination entry points; each must stop, while valid controls still route -- `bootstrap/tests/test_board_json_contract.py`.

**Verdict**: REVISE. **Findings**: blocking; accepted criteria remain unmet.

- **CR1 Decision conflict.** `_next_decision` accepts any occurrence of `ACCEPTED`, including `NOT ACCEPTED` and `ACCEPTED but REJECTED`; both selected a low implementer in a real `--next --json` no-coordination copy. Require unambiguous acceptance and test contradictory Decisions.
- **CR2 Source review evidence.** A plan joined to an archived heavy proposal with no proposal reviews selected an implementer: the plan branch checks the source status and Decision but never its required reviews. Validate the source obligation and records, including the separate Security Review, before routing; test the real entry point.
- **CR3 Reached fence.** An implementing plan with `MAINTAINER-GATED: stop before proceeding`, otherwise valid evidence and no wait field selected an implementer. C1 requires a reached fence to stop; distinguish an active fence from historical or future text and test both through the entry point.
- **CR4 Trial.** The accepted comparative three-item human/agent trial has not run and has no typed counts or outcomes (Trial feasibility above). Complete and record both conditions; it cannot be inferred from synthetic tests or waived by this review.

**Bounding**: WIDER RUN REQUIRED. The mapped status and archive tests do not cover the three authority/fence counterexamples; add those focused behavior checks and include them in final wide Boundary B. On a clean archived copy at the review basis, Python 3.13.13 ran six targeted nodes: 21 passed. Three separate real-entry probes reproduced CR1-CR3; claim checking was unavailable in those probes. No mutation was run by this reviewer.

**Elapsed**: unknown. **Tokens**: unknown.

**Coverage**: committed plan, Decision, selector, strict ledger, hook and drain skill; tested selected status, archive, floor, ledger, fallback, swap and hook-generation nodes. **Not covered**: live hook delivery, all ledger/name mutations, the trial, D, separate Security Review, final Boundary B or full suite. This pass exceeds the word target to preserve distinct blockers and evidence.

## Response -- Codex Luna (LOW) -- 2026-11-05

Responds to ordinary Code review `fe6b94816c9c7421a707d3e877ad1b9935570f10`.

- **CR1 -- accepted and addressed.** `_next_decision` now parses explicit
  outcome markers rather than searching for `ACCEPTED`; a negated marker,
  contradictory qualifier, or more than one outcome stops. Real-entry tests
  cover `NOT ACCEPTED`, `ACCEPTED but REJECTED`, two outcome markers, and a
  positive acceptance whose narrative mentions an unrelated rejected option.
- **CR2 -- accepted and addressed.** Before routing any plan, NEXT parses the
  joined accepted proposal's declared `Review` obligation and requires its
  ordinary review plus its declared Security Review, rejecting undeclared
  extra Security evidence. Real-entry tests cover missing ordinary evidence,
  missing required Security evidence, valid complete evidence and conflicting
  extra evidence. Existing valid plan fixtures now include their source review
  evidence.
- **CR3 -- unresolved; no fence rule inferred.** The artifacts do not define a
  machine-readable current-chunk/progress signal that distinguishes a reached
  fence from a future Sequence row or historical mention when the Waiting line
  is absent. CR3 remains open for a deterministic Maintainer-authorized rule;
  this change does not scan or classify fences.
- **CR4 -- open.** No human/agent trial, typed-continue count or trial outcome
  is claimed. The earlier feasibility record and required next step stand.

Plan remains `revising-code`. This is a partial response only; the CR1/CR2
fixes await targeted Code review. CR3, CR4, the required separate Security
Review and final wide Boundary B remain open. No D work or scope reduction is
included.

## Implementation verification -- Codex Luna (LOW) -- 2026-11-05

Bounded CR1/CR2 checks only. Source base: clean commit
`04c7638b64df1748718d91f15b8c58017d41b418`; candidate with the selector twins
and focused tests: clean scratch commit
`aa27a71b69f47d5634529cca3c328292e832a7a5`. Those source/test paths are
unchanged between the source base and current project commit
`fa3b2854a66e6a102d75323e20023e030d3d29be`. Twins were byte-identical.
Python 3.13.13.

`python tools/test_tiers.py for tools/board.py templates/skills/_lib/board.py
bootstrap/tests/test_board_json_contract.py bootstrap/tests/test_intents_tool.py`
selected nine files:
`test_board_json_contract.py`, `test_gate_manifest.py`, `test_intents_tool.py`,
`test_onboarding_seed_roster.py`, `test_replacement_tools.py`,
`test_security_lint.py`, `test_session_start_drain_rules.py`,
`test_status_vocabulary_advisory.py`, and
`test_upgrade_side_door_parity.py`.

`python -m pytest -q --durations=10 bootstrap/tests/test_board_json_contract.py
bootstrap/tests/test_intents_tool.py bootstrap/tests/test_onboarding_seed_roster.py
bootstrap/tests/test_replacement_tools.py bootstrap/tests/test_security_lint.py
bootstrap/tests/test_session_start_drain_rules.py
bootstrap/tests/test_status_vocabulary_advisory.py
bootstrap/tests/test_upgrade_side_door_parity.py`: 398 passed, 1 skipped,
zero failures, 80.61 seconds. The additional mapped
`python -m pytest -q --durations=10 bootstrap/tests/test_gate_manifest.py`
passed 37 tests in 44.41 seconds. Combined mapped result: 435 passed, 1
skipped, zero failures, 125.02 seconds. Decision and source-review
positive/refusal controls are included. `test_gate_manifest.py` remains on the
existing test-consolidation list.

Separate clean candidate clones, one mutation at a time:

- Restoring keyword-search Decision acceptance in both twins made
  `python -m pytest -q bootstrap/tests/test_board_json_contract.py::test_next_decision_requires_one_unambiguous_outcome`
  fail on all three refusal cases and pass the narrative positive control
  (3 failed, 1 passed).
- Bypassing the source-review completeness guard in both twins made
  `python -m pytest -q bootstrap/tests/test_board_json_contract.py::test_next_plan_requires_source_proposal_reviews`
  fail on the missing-ordinary and missing-Security cases, while the complete
  and conflicting-evidence controls passed (2 failed, 2 passed).

The first mapped candidate run exposed 23 existing fixture failures because
those synthetic plans omitted source review declarations/records; fixtures
were corrected to provide valid authority. A subsequent collection attempt
found one indentation typo before tests ran; it was corrected, and the final
clean-candidate mapped run above passed. No full suite, live hook, private log,
trust edit or push. **Still open:** CR3 reached-fence semantics, CR4 trial,
targeted Code review, separate Security Review and final wide Boundary B.
**Elapsed**: about 15 minutes wall, including setup and reruns; mapped run
80.61 seconds. **Tokens**: unknown.

**Coverage**: CR1 contradictory/negated Decision outcomes and positive control;
CR2 joined source review obligation, ordinary and Security evidence, conflict
and positive controls; mapped tests and two targeted mutations. **Not covered**:
CR3 fence progress, CR4 practice trial, other selector mutations, reviews or
Boundary B.

## Targeted code-review look -- Codex Terra (MEDIUM) -- 2026-11-05

**Basis**: original ordinary review `fe6b94816c9c7421a707d3e877ad1b9935570f10`;
source `04afb65525c622afb58fe87f5dab97853e3030f6`; fix
`aa0ea4f13279f76ac730324d2391ab8167eba8b6`. This is a same-reviewer
look at CR1/CR2 only, not a second ordinary pass or Security Review.

**Foundations**

1. **Should this happen as framed?** CR2's joined-proposal check now refuses missing ordinary or declared Security evidence; CR1's parser still admits a contradictory Decision line -- `tools/board.py::_next_decision`, `_next_for_artifact`, real-entry probes below.
2. **Best alternative.** Validate the complete explicit outcome line, including text following a bold marker, while retaining the source-review obligation check and its positive control -- `tools/board.py::_next_decision`; `bootstrap/tests/test_board_json_contract.py`.
3. **What would show it wrong?** The real `--next --json` command must stop on `**ACCEPTED.** but REJECTED` and keep routing a valid accepted source with both required reviews -- clean-copy probes below.

**Targeted verdict**: CR2 addressed; CR1 remains blocking. In a clean `aa0ea4f1` archive copy, Python 3.13.13 ran the two focused test nodes: 8 passed. Through the real CLI without the optional coordination module, `NOT ACCEPTED` stopped; `**ACCEPTED.** but REJECTED` selected a low implementer, as did `**ACCEPTED.**` followed by `The proposal is REJECTED.` The parser examines only the bold marker when a line starts bold, so it misses contradictory remainder text. Add a focused real-entry regression and refuse that conflict. A joined heavy proposal stopped with no reviews or only its ordinary review, and routed only after its declared Security Review was present. Claim checking was reported unavailable in these probes; it did not supply authority.

**Bounding**: WIDER RUN REQUIRED for CR1's uncovered contradictory-line behavior; include its new check in final wide Boundary B. CR3 reached-fence semantics and CR4 human/agent trial remain open, unchanged by this look. Separate Security Review and final Boundary B have not run here.

**Elapsed**: about 4 minutes of focused execution and inspection. **Tokens**: unknown.

**Coverage**: committed fix, response, two focused nodes and real CLI Decision/source-review cases. **Not covered**: CR3, CR4, installed hook delivery, all parser phrasings, Security Review, D or full suite.

## Response -- Codex Luna (LOW) -- 2026-11-05 (CR1 retry)

First feedback-driven same-tier retry against the targeted look at `2ffe4865`.
In both board copies, the Decision parser now checks text after a bold outcome
marker for an immediate opposing outcome and recognizes explicit rejection of
the proposal or Decision elsewhere in the Decision body. It does not treat a
rejected alternative as rejection of the proposal. No other selector rule or
status semantics changed. CR1 awaits the same reviewer's targeted look; CR2
remains addressed. The plan stays `revising-code`. CR3's reached-fence signal
and CR4's human/agent trial remain open; this retry neither defines the former
nor claims the latter. Separate Security Review and final wide Boundary B are
also outstanding.

## Implementation verification -- Codex Luna (LOW) -- 2026-11-05 (CR1 retry)

Clean source base `3ce15b94d9d0269f9c76abef6cc9ad83054c8baa`; clean
scratch candidate `9044fc76` with only the two board copies and the focused
test changed. Python `/Users/kendal30/conda_envs/lhm/bin/python` is 3.13.13.
Candidate pre/post `git status --short` was empty; the board copies matched.
The focused real `--next --json` test executes each copy from an isolated
synthetic root without a claims resolver. It stopped on `**ACCEPTED.** but
REJECTED` and on a later `The proposal is REJECTED.`; it routed accepted
Decisions that reject an alternative. The existing source-review positive and
negative controls also passed.

`python -m pytest -q bootstrap/tests/test_board_json_contract.py::test_next_decision_requires_one_unambiguous_outcome bootstrap/tests/test_board_json_contract.py::test_next_plan_requires_source_proposal_reviews`:
18 passed, zero failures in 1.36 seconds on the clean candidate. In a separate
copy with only the two Decision parsers restored from the base, the Decision
node gave 4 failed, 10 passed in 1.76 seconds: both new refusal cases failed
for each copy, and all controls passed. `python tools/test_tiers.py for` on the
two board copies and owning test selected eight files; only the two affected
nodes above were rerun for this bounded retry. The other mapped files and full
suite were omitted, as were CR3/CR4, live hook, private logs, trust edits,
Security Review and Boundary B. No push. **Elapsed**: about 10 minutes,
including inspection and scratch setup. **Tokens**: unknown.
The plan's claim, link, snippet and neutrality checks passed; the four-path
`git diff --check` passed.

## Second targeted code-review look -- Codex Terra (MEDIUM) -- 2026-11-05

**Basis**: original ordinary review `fe6b94816c9c7421a707d3e877ad1b9935570f10`;
first targeted look `2ffe48652839f788217acc6479df8d22a8bf7924`;
CR1 retry `6f4abc93653c979d85db9d91871be5979fd74f00`. This is a
same-reviewer CR1 look, not a new ordinary pass or Security Review.

**Foundations**

1. **Should this happen as framed?** The reported bold-marker contradiction now stops, but an equivalent explicit contradiction still selects an implementer -- `tools/board.py::_next_decision`; real `--next --json` probe below.
2. **Best alternative.** Decide acceptance from a complete, unambiguous Decision outcome rather than a growing list of contradictory phrases; preserve rejection of an alternative as a valid narrative -- plan C1 and the valid control below.
3. **What would show it wrong?** `**ACCEPTED.** yet REJECTED` must stop through the real command while `**ACCEPTED.** Authorization.\nThe alternative was rejected.` still routes -- clean-copy probe below.

**Targeted verdict**: CR1 remains blocking. On a clean archive copy of `6f4abc93`, Python 3.13.13, the real CLI stopped for `**ACCEPTED.** but REJECTED` and for a later `The proposal is REJECTED.` A valid acceptance rejecting an alternative routed to implementer/low. Yet `**ACCEPTED.** yet REJECTED` also routed to implementer/low: the trailing-text check recognizes `but`, not this equivalent contradictory connector. The two focused test nodes passed, 18 cases in 1.57 seconds; none covers this counterexample. Add a real-entry refusal test and close the ambiguous-outcome rule without rejecting ordinary alternative discussion.

**Bounding**: WIDER RUN REQUIRED for this uncovered CR1 case before final wide Boundary B. CR2 remains addressed. CR3's fence signal, CR4's human/agent trial, separate Security Review and final Boundary B remain open; this look did not assess or perform them.

**Elapsed**: about 4 minutes of focused inspection and execution. **Tokens**: unknown.

**Coverage**: committed retry, response, owning focused nodes and four real-entry Decision cases without coordination. **Not covered**: all natural-language Decision phrasings, CR3, CR4, live hook, D, Security Review or full suite.

## Response and implementation verification -- Codex gpt-6.1-terra (Medium) -- 2026-11-05

**CR1 correction:** One-tier-up execution after the earlier low-tier retries.
Commit `db70b763` checks outcome words throughout the Decision body, independent
of connectors, in both board twins. It excludes an explicitly named alternative's
outcome before assessing the proposal; ambiguous or unrecognized outcomes stop.
The real-entry tests retain both earlier alternative-subject positive controls and
add `yet`, `nevertheless`, slash, later negation and later rejection cases.
This remains a conservative text check: other narrative uses of outcome words
may stop and need human interpretation, and arbitrary natural-language meaning
cannot be established by the selector.

**Focused verification:** On an isolated archive of `db70b763`, canonical
Python 3.13.13 ran `python -m pytest -p no:cacheprovider -q
bootstrap/tests/test_board_json_contract.py::test_next_decision_requires_one_unambiguous_outcome`:
24 passed in 1.45 seconds, covering both twins. Elapsed for this work: unknown;
tokens: unknown. The mapped iteration checks and wide Boundary B remain owed;
they were not run during the shared integration window. CR1 remains subject to
the existing review limits. CR3 remains fenced pending the Maintainer's
decision; CR4 trial and separate Security Review remain open. No status change.

## Response and implementation verification -- Codex gpt-6.1-terra (Medium) -- 2026-11-05 (CR3)

The Maintainer clarified in chat: "There should be no human-only steps in
plans. What is it?" This is context for CR3, not a new scope Decision. The
existing amendment defers old C2 and C3; it does not waive C1 or its checks.

Commit `f23cbca4` stops NEXT on the existing `MAINTAINER-GATED` and
`MAINTAINER-ONLY` markers in operative Scope or Sequence and on unquoted
standalone marker declarations anywhere. It preserves the Waiting header stop,
ignores recognizable blockquoted and fenced examples, and rejects duplicate
operative headings. Both twins have real-entry controls, including the original
standalone counterexample, historical prose, quoted examples, and clean work.
No progress field or additional authority was introduced.

**Limits:** The check recognizes explicit markers, not every natural-language
human-only instruction. Inline formatted markers remain conservative stops.
It cannot reconcile this plan's old C2 table against its appended amendment:
NEXT stops and an agent must read the present authority rather than infer that
the old table is operative. No scope concession is inferred.

**Focused verification:** On an isolated archive of `f23cbca4`, canonical
Python 3.13.13 ran `python -m pytest -p no:cacheprovider -q
bootstrap/tests/test_board_json_contract.py::test_next_plan_operative_human_only_steps_stop
bootstrap/tests/test_board_json_contract.py::test_next_decision_requires_one_unambiguous_outcome`:
48 passed in 2.89 seconds. Elapsed: unknown; tokens: unknown. Mapped iteration
checks, CR4 trial, separate Security Review and wide Boundary B remain owed.
No human evidence or trial is claimed; status remains `revising-code`.

## Targeted code-review continuation -- Codex gpt-6.1-terra (MEDIUM) -- 2026-11-05

**Handoff and basis**: I am a new ordinary reviewer continuing only CR1 and
CR3 from `fe6b9481` after the prior reviewer role closed; I did not author the
fixes. I read targeted looks `2ffe4865` and `78dce1a5`, fixes `db70b763` and
`f23cbca4`, and their records `e6614829` and `b8446f01`. This is not a new
full review or Security Review.

**Foundations**

1. **Should this happen as framed?** CR3's reported explicit fence now stops,
   but CR1's fix also stops an unambiguous repeated acceptance, losing an
   accepted C1 routing behavior; see the real-entry comparison below.
2. **Best alternative.** Preserve refusal of opposing outcomes while accepting
   consistent repeated statements of the same outcome, with real-entry controls;
   keep the conservative fence stop when the current step cannot be established.
3. **What would show this wrong?** A real-entry test must route the repeated
   acceptance below and stop an opposing outcome, and the fence and quoted-example
   controls must continue to stop and route respectively.

**Disposition: CR1 remains blocking; CR3 addressed for the original finding.**
The accepted source proposal itself uses `**ACCEPTED, as revised.**` and
`**Tier**: heavy. Accepted as revised ...` in its Decision. The new parser
requires exactly one occurrence of an outcome word. On a clean `b8446f01`
archive with Python 3.13.13, the real `--next --json` entry stopped on a light
proposal with that repeated-acceptance structure; replacing the second
`Accepted as revised` with `Authorization` routed implementer/low. Adding
`REJECTED` stopped. Claim checking was unavailable in these isolated probes.
The repeated outcome is consistent, not ambiguous; C1 calls for the accepted
light row to route. Close by retaining that behavior and the contradiction
stops in both twins, with a real-entry regression.

For CR3, 10 selected real-entry fence and example cases across both twins
passed in 0.57 seconds on the same snapshot. Explicit operative or standalone
markers stop; recognizable quoted examples route. This plan's historical C2
row still causes a conservative stop: the selector cannot reconcile the later
scope amendment and must not infer authority from absence. The Maintainer's
clarification did not authorize a progress tracker or waive accepted scope.

**Bounding**: WIDER RUN REQUIRED for the CR1 regression and final wide
Boundary B. CR2 remains addressed; CR4's actual-person trial, separate Security
Review and final Boundary B remain open. **Elapsed**: about 7 minutes;
**tokens**: unknown. **Coverage**: named commits, accepted source, exact diffs,
the described Decision probes and selected fence controls. **Not covered**:
all Decision phrasings, non-marker human instructions, live hook, trial, D,
Security Review or full suite.

## Response and implementation verification -- Codex gpt-6.1-terra (Medium) -- 2026-11-05 (CR1 repeated acceptance)

**CR1:** Accepted the targeted finding at `d4252672`. Commit `c225a807` allows
consistent repeated narrative acceptance while retaining one explicit outcome
declaration, one Decision and one valid tier. Opposing outcomes and `NOT
ACCEPTED` still stop after the existing alternative-subject exclusion; duplicate
explicit declarations still stop. The real-entry regression reads the actual
archived continuation proposal's Decision, including its heavy-tier repeated
acceptance, and pairs it with later negation and rejection in both twins.

**Focused verification:** On an isolated archive of `c225a807`, canonical
Python 3.13.13 ran `python -m pytest -p no:cacheprovider -q
bootstrap/tests/test_board_json_contract.py::test_next_decision_requires_one_unambiguous_outcome
bootstrap/tests/test_board_json_contract.py::test_next_actual_continuation_decision_repeated_acceptance`:
32 passed in 1.99 seconds. Elapsed: unknown; tokens: unknown. The correction
returns to the same reviewer for its targeted look. CR3's addressed original
finding is unchanged; the actual-person trial, separate Security Review, mapped
checks and wide Boundary B remain owed. Status remains `revising-code`.

## Targeted code-review continuation -- Codex gpt-6.1-terra (MEDIUM) -- 2026-11-05 (CR1 correction)

**Basis**: My finding at `d4252672`, correction `c225a807`, and response
`4855ae28`. This is the same reviewer's targeted follow-up, not a new pass.

**Foundations**

1. **Should this happen as framed?** Yes: the actual continuation Decision's
   repeated consistent acceptance now routes, while the tested contradictions
   and duplicate authority still stop.
2. **Best alternative.** Retain one explicit outcome declaration and allow
   consistent narrative repetition, with real-entry controls in both twins.
3. **What would show it wrong?** A real-entry counterexample routing a negated,
   opposing or duplicate Decision, or refusing consistent acceptance, would
   disprove this conclusion.

**Disposition: CR1 addressed**, including the repeated-acceptance regression.
On a clean `4855ae28` archive, Python 3.13.13 ran 12 selected real-entry cases
in 0.82 seconds: actual archived Decision wording and later `NOT ACCEPTED` or
`REJECTED`, plus the prior standalone/operative fence and quoted-example
controls, across both twins. Separate real-entry probes in both twins stopped
on a duplicate explicit acceptance declaration and on a duplicate Decision
section. Claim checking was unavailable in these isolated probes. CR3's
original finding remains addressed; no additional authority is inferred.

**Bounding**: The CR1 correction is closed; the actual-person trial (CR4),
separate Security Review, mapped checks and final wide Boundary B remain owed.
**Elapsed**: about 3 minutes; **tokens**: unknown. **Coverage**: named fix,
record, controls and committed source. **Not covered**: all natural-language
phrasings, live hook, trial, Security Review or full suite.

## Security Review -- Codex GPT-6.1 Sol (HIGH) -- 2026-11-06

**Reviewed commit**: `9b839b0f2f6fbc5f3a5a607a86b2ac07ddaee058`, including
continuation source through `c225a807` and ordinary follow-up `d95b05c7`.
**Obligation**: Internal Security Review
**Tier**: Internal Security Review

**Foundations**

1. **Should this happen as framed?** Advisory A-C preserve the accepted boundaries, but heavy authority can route without required Security evidence -- `tools/board.py::_required_reviews`, `_next_for_artifact`; SR-C1 below.
2. **Best alternative.** Keep the selector and require review declarations to agree with the heavy Decision before routing -- this plan C1; `AGENTS.md`, Review.
3. **What would show it wrong?** Through real `--next --json`, heavy items with weakened proposal or plan obligations must stop, while a fully reviewed heavy control still routes -- the six probes below.

**Verdict**: REVISE. **Findings**: one blocking authority inconsistency.

**SR-C1 -- Heavy review requirements can be weakened by a header.** In separate
staged copies of both committed board twins, canonical Python 3.13.13 ran the
real CLI on an accepted heavy source joined to a `ready-to-implement` plan.
Both twins selected implementer/low when either (a) the source declared
`Review: usual` and had only ordinary proposal review, or (b) the fully reviewed
source joined a plan declaring `Plan review: required(Internal)` with only
ordinary plan review. The complete-heavy control also routed: six probes,
no claim resolver installed, explicitly reported unavailable. The selector
trusts each declaration without reconciling the heavy Decision's separate
Security obligation. This violates C1's conflicting-authority stop and the
heavy review requirement. Close by refusing both inconsistencies and adding
real-entry refusal/positive controls for both twins.

**Bounding**: WIDER RUN REQUIRED for these missing authority checks. CR4's
mixed trial and final wide Boundary B remain separately open; no usability
improvement or scope waiver is claimed. D remains deferred by the recorded
amendment.

**Elapsed**: about 8 minutes, inspection and probes. **Tokens**: unknown.

**Coverage**: fixed committed plan/template/source/reviews, selector/schema,
path/claims readers, generated hook, drain guidance; three source twins are
byte-identical and both skill copies preserve the same drain bounds. **Not
covered**: live hook delivery, all input/race mutations, trial, final Boundary B,
D or full suite. No implementation checks were rerun.

## Response and implementation verification -- Codex Luna (LOW) -- 2026-11-06 (SR-C1)

**SR-C1 response**: accepted. Commits
`dcfd0e64b3eae65eab8a54602ed31f7567b83620` and
`4a7a6631f77148641fe22157b850e18ec6a9b1e2` make heavy Decisions require the
existing proposal and plan Security Review declarations before NEXT routes;
the board copies remain byte-identical. Real CLI controls cover both weakened
declarations and complete-heavy routing through each copy.

**Initial focused check and correction**: the six new cases passed on the first
commit. Three neighboring source-review cases passed, while two failed because
their old heavy fixtures omitted plan Security Review; the source-evidence
conflict case also got the new missing-obligation stop before its existing,
more specific evidence-conflict stop. The follow-up preserves that specific
conflict check first and updates the valid heavy fixture to include its required
plan Security Review.

**Final focused verification**: from an isolated archive of
`4a7a6631f77148641fe22157b850e18ec6a9b1e2`, canonical Python 3.13.13 ran
`python -m pytest bootstrap/tests/test_board_json_contract.py -k
'heavy_requires_security_obligations_through_each_entrypoint or
heavy_review_floor_is_not_downshifted or
plan_requires_source_proposal_reviews'`: 11 passed, 143 deselected in 0.55
seconds. Elapsed: unknown; tokens: unknown. No test files over the 10-second
timing target. The failed initial selection is resolved by the corrected
committed fixtures and passing rerun. The same Security reviewer must perform
the targeted SR-C1 follow-up; CR4's trial and final wide Boundary B remain open.

## Targeted Security Review -- Codex GPT-6.1 Sol (HIGH) -- 2026-11-06 (SR-C1)

**Basis**: my SR-C1 at `a1a3dc41`; fixes `dcfd0e64` and `4a7a6631`;
response `121dfc44`. Same-reviewer second pass, limited to SR-C1.
**Obligation**: Internal Security Review
**Tier**: Internal Security Review

**Foundations**

1. **Should this happen as framed?** Yes: heavy Decisions now require matching proposal and plan Security declarations before routing -- `tools/board.py::_next_for_artifact`, `_next_review_move`.
2. **Best alternative.** Retain these existing obligation checks and both-entrypoint controls; no new authority field is needed -- `bootstrap/tests/test_board_json_contract.py::test_next_heavy_requires_security_obligations_through_each_entrypoint`.
3. **What would show it wrong?** A weakened heavy obligation routing work, or a complete-heavy control stopping, would falsify closure -- ten real-entry controls below.

**Disposition: SR-C1 addressed.** In an isolated archive of `121dfc44`,
canonical Python 3.13.13 executed ten independent real `--next --json` controls
across both staged board twins. Both now stop for the original weakened source
and weakened plan declarations; complete-heavy plans route implementer/low.
Direct accepted heavy proposals also stop with weakened declarations and route
plan author/medium with complete evidence. The twins are byte-identical. These
synthetic roots lacked coordination; selectable controls explicitly reported
claim checking unavailable. No claim clearance is inferred.

**Bounding**: no wider selection is required by this finding beyond its new
regressions in the owed final wide Boundary B. CR4's mixed trial and final
Boundary B remain open; this closes no missing check and claims no usability
result. No further clearing review is required for SR-C1.

**Elapsed**: about 3 minutes. **Tokens**: unknown.

**Coverage**: committed SR-C1 diffs, response, owning tests and changed authority
branches through both real entry points. **Not covered**: other selector rules,
CR1/CR3, claims, live hook, trial, final Boundary B, D or full suite; no
implementation selection was rerun.

## Maintainer scope allowance -- CR4 trial -- Codex Luna (LOW) -- 2026-11-06

**Authority**: Maintainer chat, 2026-11-06. This is a scope allowance for the
CR4 comparison only; it does not alter the other accepted plan criteria,
complete the trial, or waive review and verification requirements.

> Use an agent-operated comparison (Recommended)

Agents will operate both conditions and record their own continuation prompts.
This cannot measure human interruptions or establish human usability; those
remain adopter-feedback work. No human observations will be inferred.

## CR4 agent-operated comparison -- Codex Luna (LOW) -- 2026-11-06

**Authority and setup**: Maintainer scope allowance `70dd1601`. Two separate
committed fixture projects used the same light proposal and two standard plans;
all Decisions and prior reviews were marked synthetic test data. Baseline seed
`2b7a2027` ended at `0921f0697e3c5256088f1fc97a7ba987a226b81`. With B/C seed
`2c80ab69` ended at `daadc73f73b0b1691f1e7ffac7d6f98b82074eb4`. The latter
used the shipped drain guidance and generated hook. Baseline required one
pre-work correction after the participant used a nonexistent fixture path.
With B/C's initial prompt specified the same command-scoped identity for claims
and commits; baseline claims used its resolved session identity. The with-B/C
participant also self-corrected an invalid `session.py --drain` invocation
without a coordinator prompt. These are setup differences, not trial outcomes.

**Work and observed counts**: in each arm, the light artifact was created,
checked with `python tools/check_fixture.py light`, and archived; alpha was
created and checked with `python tools/check_fixture.py alpha`, then left at
`awaiting-code-review`; beta passed `python tools/check_fixture.py beta` and
was physically moved to `dev/plans/archive/`. All six named checks passed.
Each participant had one required medium code-review handoff for alpha and
reported zero safety stops. Baseline needed 0 coordinator prompts after its
stop. With B/C stopped first at `d4c35b98` with beta unprocessed; the
coordinator sent 1 retargeting prompt, then 1 prompt to physically move beta
after its status alone had been set to archived. The final with-B/C correction
commit `daadc73f` put the plan in `archive/`. Thus the observed counts were
baseline 0, with B/C 2 post-stop prompts, plus the separate baseline setup
recovery. This run demonstrates no prompt reduction.

**Limits and disposition**: both fixtures ended with modified
`dev/intents.jsonl` and untracked `tools/__pycache__/`; neither tree was clean.
Baseline retained three active claims, while the hook released matched claims
in the with-B/C arm. Hook-driven claim release is existing behavior and
confounds any comparison of role-handoff availability with advisory/drain
effects. The final board in both arms names the same medium reviewer for alpha.
These are descriptive observations on synthetic fixture work, not a causal
estimate or human-usability evidence. Human interruption and usability remain
unmeasured adopter-feedback work. The joint v0.8 proposal remains current and
awaiting review, with the guard and conditional D scope; its future Decision
and implementation do not gate this plan's archive. Ordinary review and final
wide Boundary B remain due; no archive is claimed. **Elapsed**: unknown.
**Tokens**: unknown.

## Targeted ordinary review -- Codex gpt-6.1-terra (MEDIUM) -- 2026-11-06

**Basis**: New source after my `d95b05c7` look: `dcfd0e64`, `4a7a6631`,
implementation evidence `121dfc44`, Security follow-up `ce82114e`, and CR4
allowance and comparison `70dd1601` and `2b65f921`. This is a targeted look,
not a new full pass or a substitute for Security Review.

**Foundations**

1. **Should this happen as framed?** Yes: the new checks reconcile heavy
   Decision tier with proposal and plan Security obligations before routing;
   the agent-operated trial supplies the comparison allowed by the Maintainer.
2. **Best alternative.** Keep the existing obligation checks and real-entry
   controls, and report the trial as descriptive: its baseline was zero prompts
   and its B/C arm required two, with the recorded setup and identity confounds.
3. **What would show it wrong?** A weakened heavy obligation routing work, a
   complete heavy case stopping, or evidence that the recorded trial endpoints
   or prompt counts differ from the fixture observations would challenge this.

**Disposition**: No new ordinary blocker in the changed source; CR4's missing
trial is supplied under the quoted allowance. The implementation record reports
11 focused cases passing, and the independent Security follow-up reports ten
real-entry controls across both twins, including complete-heavy routing. The
comparison records the same three-item endpoints in each arm: light and beta
archived, alpha awaiting its independent fixture review. It identifies dirty
fixture trees and hook/identity differences; it does not establish prompt
reduction, causation, or human usability. Alpha's reviewer is the trial endpoint,
not an unfinished product implementation step. Final wide Boundary B remains
owed before archive; this look does not clear or replace it.

**Elapsed**: about 3 minutes; **tokens**: unknown. **Coverage**: committed
source delta, regression changes, cited evidence and trial allowance/results.
**Not covered**: rerunning implementation tests, fixture logs independently,
live hook behavior, other selector rules, final Boundary B or full suite.
