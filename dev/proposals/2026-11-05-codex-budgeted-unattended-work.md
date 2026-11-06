# Budgeted unattended work for v0.8

**Author**: Codex Terra (proposal author; medium)
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy -- unattended admission and configured command execution cross trust boundaries
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-05
**In brief**: Consider a cooperative spending guard and a conditional, bounded unattended loop after v0.7 measurement and continuation trials.
**Elapsed**: unknown
**Tokens**: unknown

## Decision summary

For v0.8, propose a spending guard before unattended items and, only if the
Maintainer later chooses to keep it, a bounded launcher for those items. The
guard is not a provider billing cap: forged logs and work already underway
can exceed its limit. v0.7 loses unattended launches, not the safeguards on
its advisory continuation work. Scheduling this proposal authorizes neither
implementation nor activation, private collection, or host configuration.

## Context

The accepted [meter proposal](archive/2026-10-30-claude-metered-cost.md)
requires a cooperative pre-item stop; the accepted
[continuation proposal](archive/2026-11-03-claude-agent-continuation.md)
requires A-C and a trial before a later Maintainer choice whether to keep D,
the optional loop. Their current plans are
[metering](../plans/2026-11-04-metered-cost.md) and
[continuation](../plans/archive/2026-11-05-agent-continuation.md); the
[planning board](../PLANNING.md) tracks the split. The meter plan's sanitized
source investigation did not establish a source binding the live account
and observation time to a reading. That is an open evidence gap, not proof
that no source exists. No functioning budget stop is claimed.

The [continuation comparison](../plans/archive/2026-11-05-agent-continuation.md)
(`2b65f921`) used the same synthetic three-item workload in both arms: the
baseline needed zero post-stop prompts and the arm with B/C needed two. Setup,
identity and the existing hook confound the comparison; it does not establish
prompt reduction, a causal effect or human benefit. The later keep-D choice
remains open.

## Proposal

Use v0.7 measurements and the mixed light/standard A-C trial as inputs to the
later choice. Preserve the choice: trial results do not automatically keep or
drop D. Before each unattended item, refresh and admit only a fresh, finite,
nonnegative reading with complete coverage matching the Maintainer-controlled
allowed source, account, unit and window, within configured `max_age` and
strictly below its limit. Policy limits and ages are finite and positive;
units are named-window plan percentage or weighted tokens per day, not
interchangeable. Readings, limits and ages must be actual JSON numbers, not
booleans or strings; plan percentages are 0..100, limits and ages are positive
and finite, duplicate keys and NaN/infinities are rejected, and unknown or
missing units or cache-weight semantics are not zero and cannot admit work.
Missing, stale, future, invalid, mismatched, unknown or
refused refresh stops unattended admission; attended work remains available.
Policy and consent cannot come from logs or artifacts. Account-at-observation
and source observation time must be proven by supported evidence, not inferred
from a policy label or collection time. No RPC, capture, host setting or
provider transport is authorized or invented now.

If the Maintainer later keeps D, and the guard exists, an explicitly invoked
loop may start one fresh agent per item. An item is one selected next move on
one artifact, in the selected role and tier, from the parent's recorded starting
commit/status. The parent supplies a single-item context outside artifact text.
In that context, the shipped drain step overrides its usual continuation rule:
do only that move, return after the first commit touching the artifact, or stop
earlier on uncertainty, failure or a fence. Additional commits, required review,
author response and later moves return to the parent for a separate refresh and
admission, even on the same artifact or in the same role. Review obligations
remain owed; the parent selects the fresh reviewer as another item. Helpers may
assist only the current move and must inherit its stop boundary; they may not
start another move or an independent drain. Ordinary attended drain is unchanged.

Read settings once from Git's administration folder; refuse links and tracked
files. That folder is candidate-controlled under `bootstrap/SAFETY.md` rule 10,
so freezing it does not prove authorship. Require an invocation-supplied expected
digest of the exact settings bytes the trusted caller has reviewed and approved,
including each full command argument vector and its declared host executables.
The digest only binds those approved bytes; it does not establish provenance or
authorize arguments. Never derive approval from candidate settings, logs or
artifacts. Missing approval or a digest mismatch refuses launch. This uses
ordinary trusted host invocation, with no new registry or approval service;
same-user substitution of settings or invocation remains a printed residual.
Resolve and immediately revalidate declared executables under rule 10, including
its lexical/resolved containment and digest requirements; no executable or
undeclared command reference comes from artifact text. Use the approved command
for the selected tier as an argument vector without a shell, with the full
artifact path as one argument. Default to five items and require a positive,
finite per-item timeout. Stop on a dirty tree,
missing or invalid meter, selector uncertainty or stop, unconfigured tier,
failure, timeout or limit, no new commit touching the artifact, or a newly
written Maintainer-only status. Report items, commits and stop reason. Artifact
names must independently match the accepted date-stem rule before display or
selection; artifacts never supply authority, commands, target or limits.

The parent checks the starting state, admits every launch and checks the returned
commit/status boundary; an extra commit or move stops the loop as a violation,
not as another admitted item. These checks cannot prevent a child from ignoring
its instructions: the single-item and helper rules are cooperative. On timeout,
the launcher terminates and waits for its managed child process group/tree, then
stops; inability to establish that cleanup is unavailable, not success. Escaped
descendants, remote provider work and other sessions may continue. The guard
does not kill work merely because a reading crosses its limit or enforce a
provider cap. Mutable-log forgery, one-item overshoot and concurrent-session
overshoot remain residuals.
No agent scores, per-artifact budgets, new service or registry are proposed.

## Rationale

Joining the dependent guard and loop puts their shared admission boundary in
one review, while v0.7 can measure and trial A-C without waiting for it. The
cost is later design, tests and maintenance for a control that cannot guarantee
spending; the evidence and keep-D choice may show that cost is unnecessary.
The recommendation is to deliver the accepted guard first and retain the later
keep-D choice until supported source evidence and a meaningful comparison justify
the extra launcher burden. Neither is established by the current records.

## Alternatives considered

Guard alone with A-C is the least involved option that preserves the accepted
stop: no launcher, child-boundary or timeout machinery to build and maintain,
but each fresh-agent handoff needs attended initiation. Source binding and guard
maintenance remain necessary. Optional D adds automatic handoffs, single-item
instructions, parent checks and process cleanup; callers must review settings
and supply their approved digest again when those bytes change. That adds setup,
understanding and recurring command/version maintenance, with implementation
effort still uncertain until the plan maps the actual harnesses. Without caller
approval, candidate-controlled settings cannot safely choose commands, so this
option loses unattended launches rather than falling back to unchecked settings.
Doing nothing further costs least but loses the already-accepted cooperative
stop and would require the Maintainer's explicit scope disposition. A provider
cap could offer another enforcement boundary, but is not established by these
records and cannot substitute for the accepted local contract.

## Documentation / doctrine surface

Put deliberation and decisions in `dev/`, cross-cutting prescription in the
governing layer or shipped drain step as applicable, and software description in
`docs/`, following `docs/DOCUMENTATION_PLAN.md`. The later plan must identify
the actual shipped and self-hosted consumers and any doctrine rate-limit gate.
The single-item override belongs in the launched path of the shipped and
self-hosted session-start drain instructions; their ordinary attended path stays
unchanged. No such override is implemented by this proposal.

## Evidence / verification plan

### Tests required

The future plan maps real admission and launcher entry points and their owning
test families. Synthetic tests must prove no next item starts for each invalid
reading, policy mismatch, refresh failure or missing meter, while attended work
remains possible; include booleans, strings, out-of-range percentages, duplicate
keys, NaN/infinities and unknown units or cache weights. Exercise every loop stop,
hostile names, link/tracked settings, rule 10 resolution, tier argv and explicit
invocation through real entry points, using a fake launched agent. Test that
artifacts and logs cannot change policy or commands. Ordinary and separate Security code reviews precede wide
Boundary B; tests and source evidence must not be represented as already run.

Through the real launcher and continuation entry points, have a fake agent commit
the first move, then encounter another same-role move on the same artifact and a
required review. Single-item context must return control instead of starting
either. Make the next reading refuse and assert that neither a successor nor a
review child starts; in the positive control, a fresh admission starts the next
selected move. Repeat for a helper attempting continuation, and retain required
review work as pending when the item cap is reached. Exercise the actual supplied
single-item context and shipped drain instructions, not a fake-agent convention
alone. Test an extra-commit violation stopping subsequent launches, approved
settings versus changed bytes, and timeout cleanup versus escaped/in-flight work.
These demonstrate the cooperative workflow and parent checks, not hostile-agent
confinement; the future plan must name their real executable entry points.

### Examples / smoke checks

Use synthetic settings and readings to demonstrate one allowed item followed
by a refused one, including its reported reason. The future plan specifies
source-binding evidence and applicable claim, link, snippet and prose gates;
any actual private collection requires separate permission.

#### Security preflight

- S1: Maintainer-controlled local policy supplies limits and allowed identity;
  the source supplies observations, and selector records supply candidate work.
  The trusted caller approves command arguments/executables and supplies the
  expected settings digest through host invocation. Git-administration settings
  are candidate input; a matching digest binds approved bytes, not authorship.
  An agent may influence logs or artifacts, so neither supplies policy or command authority.
- S2: Removing freshness, identity, filename, dirty-tree or Maintainer-status
  guards, the single-item override or settings-digest comparison must fail their
  tests. These mutations have not been run; no implementation exists here.
- S3: The future admission and explicitly invoked loop commands and exact test
  selections are not yet designed; the plan must name them and compare their
  scope with the eventual adopter-facing instructions. No such instruction is
  claimed to exist now.
- S4: Missing, malformed, unrecognized or unverifiable inputs stop unattended
  admission or launch, never increase authority; attended work stays available.
- S5: A hostile agent can alter mutable logs or instruct its launched successor;
  it can disregard the cooperative work boundary or escape managed descendants.
  Same-user substitution, forgery and in-flight/concurrent overshoot remain
  possible; the parent can stop later launches, not undo spending.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A stale or mismatched reading starts work, an artifact chooses a command, the
trial shows no need for D, or the account binding cannot be established without
an unapproved collection boundary.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance -- admission and process-launch boundaries;
usual review plus a separate Security Review.

## Review -- Codex GPT-6.1 Terra -- 2026-11-06

Reviewed commit: `95ea28b81985c79e47abe524443b31fe00efb2ee`

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: approximately 3 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes, conditionally: preserve the accepted guard while making D depend on a later choice and a source that actually proves account and observation time; neither is established today. -- Context and `dev/plans/2026-11-04-metered-cost.md`, deferred source blocker.
2. **Best alternative.** Deliver the guard alone and retain A-C; it avoids launcher maintenance and launch risk but loses automatic fresh-agent handoffs if D is not kept. It preserves the accepted stop, unlike dropping the guard. -- Alternatives and `dev/proposals/archive/2026-10-30-claude-metered-cost.md`, section 3.
3. **What would show it wrong?** A supported source that cannot bind account and time, or a comparative trial with a meaningful workload showing no benefit from D, would challenge the proposed delivery; test those before a keep-D choice. -- Context and `dev/plans/archive/2026-11-05-agent-continuation.md`, comparison at `2b65f921`.

The proposal honestly reports the zero versus two post-stop prompt observation and its confounds; it does not present that trial as evidence of benefit.

**Finding 1 -- Blocking: bound work inside each launched item.** The loop refreshes before each item, but the existing drain rule lets an agent continue its own next move on the same target (`templates/skills/session-start/SKILL.md`, section 4). A launched agent could therefore take another move before the loop regains control and refreshes, defeating the accepted per-item stop without being a hostile agent. Specify how ordinary launched work is limited to one item and how the real launch/continuation entry points will demonstrate that a second item cannot start before another refresh. Preserve the stated residual that a hostile agent can disregard instructions; do not claim an enforcement guarantee the mechanism cannot provide.

**Coverage:** Read the committed proposal, accepted meter and continuation contracts, trial record and drain rule. No execution, private source inspection, provider verification or Security Review; source feasibility and actual launcher behavior remain unmeasured.

## Security Review -- Codex GPT-6.1 Sol -- 2026-11-06

**Reviewed commit**: `9b3da7cd`
**Tier**: Security Review
**Obligation**: Internal Security Review
**Verdict**: REVISE
**Elapsed**: approximately 5 minutes. **Tokens**: unknown.

**Foundations**

1. **Should it happen as framed?** Preserve the accepted cooperative guard, conditionally: consent stays separate from mutable observations; account/time binding remains unproven. -- Proposal; metering plan, “Deferred source blocker”.
2. **Best alternative.** Guard alone with attended initiation retains the accepted stop without launcher maintenance; it loses automatic handoffs. Keep D conditional: baseline zero versus B/C two post-stop prompts establishes no benefit. -- Alternatives; continuation plan, CR4 comparison at `2b65f921`.
3. **What would show it wrong?** At real launch/continuation entry points, attempt a second move when the next reading refuses; any second start falsifies the boundary. Require supported account/observation-time evidence before activation. -- Proposal admission contract; shipped session-start skill, section 4.

**Blocking -- shared with ordinary finding 1:** “one fresh agent per item” does not bound that agent's work: section 4 permits another same-role move on its target. Close by defining the single admitted work unit, overriding ordinary continuation for launched items, and requiring the real-entry test above. Distinguish cooperative compliance from hostile-agent enforcement.

**Non-blocking advice:** Name settings provenance and execution limits. Refusing links/tracked files and reading once freezes settings; it does not prove Maintainer authorship. SAFETY rule 10 treats `.git` as candidate-controlled. State the trusted configuration assumption and same-user substitution residual, and whether timeout ends descendants or merely stops further launches. These remain cooperative limits.

**Coverage:** Read committed proposal/template, accepted meter/continuation contracts, source blocker, trial and drain/rule-10 boundaries. No tests, collectors, private inputs, native behavior or provider transport executed or verified; no implementation, activation or host changes authorized.

## Response -- Codex GPT-6.1 Sol (High) -- 2026-11-06

**Ordinary finding 1 and the shared Security blocker -- accepted.** The operative
text now bounds one admission to one selected move and its first artifact
commit, with the launched single-item context overriding ordinary drain
continuation. Required review, author response and further same-role work
remain pending for a fresh parent admission. Helpers inherit the same boundary.
The parent checks state and returned commits and stops later launches on a
violation; instructions inside the child remain cooperative. The verification
plan exercises the real launch/continuation path, a refused next reading and a
positive fresh-admission control, including review children and helpers. This
closes the missing proposal contract, not its future implementation evidence.

**Security advice -- accepted.** Git-administration settings remain candidate
input. Ordinary trusted host invocation supplies approval of the full arguments
and executable declarations; an expected digest binds the reviewed bytes and
proves neither authorship nor argument authority. Existing rule 10 governs
executable validation/revalidation. The comparison explicitly names recurring
settings review/digest and command-version maintenance, and the loss of launches
without approval. No trust registry, provider transport or approval service is
added. Timeout cleanup covers the managed process group/tree, while escaped
descendants, in-flight provider work, same-user substitution and concurrent work
remain residuals.

**Scope and recommendation.** Preserve the accepted guard, conditional D and
later keep-D choice. These restrictions refine their already-proposed admission
and execution boundaries; they add no launch authority or capability. Recommend
the guard-first path with A-C while source binding and meaningful benefit remain
unproven. The zero-versus-two prompt comparison and its confounds remain intact.
Both existing review records are unchanged; no additional proposal pass is
claimed or required for widened scope because none is proposed.

### Withdrawn / superseded commitments

- The ambiguous launcher item is replaced by the explicit single-move/first-commit
  boundary; ordinary attended drain keeps its existing continuation behavior.
- Read-once settings are retained as a snapshot, with caller approval made
  explicit; no snapshot-as-provenance or universal timeout-confinement claim is
  made. No accepted outcome or required check is withdrawn.

**Verification:** pending the committed-copy prose checks below; no behavioral,
native, provider or private-data execution. **Elapsed:** unknown. **Tokens:**
unknown.
