# Pass local API credentials to the dispatched API check

**Author**: Codex (GPT-6)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — credential environment crosses a subprocess boundary
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Allow the local API check to receive only the credentials its local policy declares when the security dispatcher runs it.

## Context

The dispatcher filters its child environment through a closed allowlist in
`templates/modules/default-on/run_security_verification.py`; the API runner
reads policy-derived `CAIRN_API_P<N>_CREDENTIAL` variables in
`templates/modules/team-gated/api_access_security.py`. A local probe of the
actual `_build_child_env` with P1 and P2 set found two variables in the parent
and zero in the child. The runner refuses missing credentials before running
its matrix. The existing real dispatcher integration test in
`bootstrap/tests/test_security_verification.py` uses an unconfigured policy,
so it does not demonstrate a configured matrix through this path. This probe
establishes the environment mismatch, not an end-to-end network result.

## Proposal

For the API local leg alone, derive the exact local principal credential names
from the validated local API policy and pass only present values to that child.
Do not pass credentials declared only in the deployed section, arbitrary matching
prefixes, or credentials to other legs. Preserve refusal for invalid policy and
missing credentials; do not print values or names in reports. Reuse the existing
policy validation and ordinal derivation rather than inventing a second parser.
Resolve how to do that without weakening the dispatcher's existing binding and
isolation checks in the reviewed plan. If that cannot be done safely, stop for
reassessment rather than broaden the environment.

## Rationale

The runner already restricts local execution to loopback and derives names from
validated principal ordinals. Passing exactly those names enables the intended
local check while retaining the closed environment for unrelated processes.

## Alternatives considered

Forwarding every matching credential variable is simpler but exposes deployed
or unrelated credentials to the local child. Leaving the behavior unchanged
makes configured local API evidence unavailable through the dispatcher.

## Documentation / doctrine surface

Describe the local handoff in the shipped security-verification module if its
current description needs correction; deliberation stays here. No governing
doctrine change is proposed.

## Evidence / verification plan

### Tests required

In `bootstrap/tests/test_security_verification.py`, exercise the installed
actual dispatcher and API runner with a configured local two-principal
loopback fixture, asserting its result matches direct execution and that local
credentials reach it. Also verify invalid and missing policy/credentials fail
closed; deployed-only, unrelated and malformed names never reach the API child
and no credentials reach other legs or reports. Use the existing API fixture in
`bootstrap/tests/test_api_access_security.py` where practical. Mutation of the
handoff to omit a local credential must fail the positive integration test;
mutation to pass a deployed-only credential must fail the isolation test.
Identify exact nodes and additional callers in the plan. A mismatch in either
behavior falsifies the proposal.

### Examples / smoke checks

Run the applicable standing gates and `python scripts/check_cairn.py` for any
changed Markdown. The reviewed plan maps the wide Boundary B checks and records
interpreter, counts, mutations and omissions; full-tree certification remains a
separate ceremony.

#### Security preflight — five questions, answered in writing

- **S1:** The adopter supplies the local policy file and parent environment;
  the dispatcher selects the API leg. Policy supplies principal ordinals by
  reference, while credential values come from the environment. The child is
  not trusted to authorize its own inputs.
- **S2:** The proposed tests must fail if the handoff drops a local credential
  or admits a deployed-only credential. These mutations have not yet been run;
  the plan and implementation must record their results.
- **S3:** The planned installed-dispatcher test selects the local API leg and
  covers the fixture's declared local and deployed principals plus unrelated
  names. The current adopter-facing statement in
  `templates/modules/team-gated/api-access-security.md` must be checked against
  that behavior during planning; no new statement has yet been written.
- **S4:** Invalid or unreadable policy and missing credentials must yield
  incomplete/refusal without a broader environment fallback; parse errors must
  never increase authority.
- **S5:** A party controlling the local policy and corresponding environment
  values can still direct the local check to an allowed loopback service and
  supply its credentials. This does not protect a compromised authorized local
  runner or host.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A local test receives a deployed-only credential, another leg receives an API
credential, or a configured direct and dispatched run disagree after accounting
for their execution context.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance
