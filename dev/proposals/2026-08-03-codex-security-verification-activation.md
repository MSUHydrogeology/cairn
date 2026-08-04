<!-- claim-check-allow: templates/modules/default-on/security-verification.md, templates/modules/default-on/run_security_verification.py, dev/modules/security-verification.md, scripts/run_security_verification.py, bootstrap/tests/test_security_verification.py -->

# Local security-verification activation

**Author**: Codex (Strategy, from the Security Review role)
**Model**: OpenAI Codex (GPT-5)
**Date opened**: 2026-08-03
**Status**: proposed
**Touches**: `bootstrap/_scaffold/config.py`, `templates/core/AGENTS.md`, the
default-on module catalog, `bootstrap/SAFETY.md`, the install manifest /
lockfile file set, and behavioral tests under `bootstrap/tests/`
**Deliberately not touched**: deployed or credentialed checks, capability
policy schemas, third-party scanner installation, arbitrary adopter CI, or the
existing finding semantics of any security runner
**Related**: `api-web-security-modules`, `portable-security-sweeps`,
`default-security-stance`, and External finding AW3 at `7125de4`
**Plan review**: `required(**External**, security lens)` -- this adds a
default-on executable dispatcher and governing `AGENTS.md` instruction to every
adopter

## Context

Two otherwise separate capability proposals reached the same adoption defect.
`portable-security-sweeps` can install a carefully bounded scanner without
giving adopters a standing reason to run it. The original
`api-web-security-modules` proposal tried to solve that problem by combining a
default-on dispatcher with two much larger network capabilities.

The External Security Review at `7125de4` found that combination unsafe. Its
agent-facing `deployed` route could read credentials and contact a live remote
system, while a policy label controlled whether mutation was allowed. The
author response at `7728fc1` accepted the findings, removed remote mutation
from the intended v1 capability design, and committed to splitting activation
from capability behavior.

This proposal is that split. It answers one narrow question: how does selecting
a security capability make its **local or offline** evidence runner part of the
expected trusted-checkout workflow? It does not make deployed checks
agent-runnable and does not create a generic plugin framework.

## Proposed paths

Proposed paths:
- `templates/modules/default-on/security-verification.md` -- activation doctrine and the merge directive for the local standing command.
- `templates/modules/default-on/run_security_verification.py` -- standard-library fixed-registry local dispatcher.
- `dev/modules/security-verification.md` -- adopter-tree destination for activation doctrine.
- `scripts/run_security_verification.py` -- adopter-tree destination for the dispatcher.
- `bootstrap/tests/test_security_verification.py` -- activation, integrity, dispatch, and aggregate-exit tests.

## Proposal

Add a small default-on module named `security-verification`. It installs a
fixed-registry dispatcher and one compact operational rule in a new
`security-verification` slot in adopter `AGENTS.md`:

> Run `python scripts/run_security_verification.py local` after a substantive
> change. An INCOMPLETE result is not CLEAN; report the unavailable evidence
> and its owner.

The command is deliberately local-only. There is no `deployed` subcommand, no
mutation flag, and no arbitrary command or plugin path. A capability that needs
credentialed or remote evidence owns a separate Maintainer command in its own
reviewed module doctrine. That command is not reachable through this
dispatcher and is not placed in the agent-facing standing rule.

### Fixed registry and installed roster

The dispatcher reads selected modules from the installed lockfile and consults
a source-owned registry. Each entry fixes:

* the exact module ID and repository-relative runner path;
* one exact local/offline argument vector;
* the child's accepted result schema and exit mapping; and
* whether the policy file is required and which lockfile mapping group owns it.

The lockfile cannot add an entry, executable path, argument, environment
variable, or shell fragment. An unknown selected security capability is
reported as unsupported rather than executed. The dispatcher uses
`shell=False`, bounded output, a timeout, strict UTF-8 and JSON decoding, and a
minimal explicit environment.

The initial registry may name reviewed local legs from
`portable-security-sweeps`, `api-access-security`, and
`web-hosting-security`. A named entry remains dormant unless the corresponding
module is installed. Adding a new entry changes this executable trust boundary
and requires proposal-backed review of the child's local contract.

### Local means no authority to perform a deployed act

The dispatcher itself opens no socket and looks up no credential. Before child
execution it verifies the dispatcher, selected child runner, and required
policy against the lockfile. It strips proxy and credential-bearing environment
variables rather than forwarding ambient process state.

Each child receives only its fixed `local` or `offline` mode. A local network
fixture capability must independently enforce loopback at resolution and at the
connected peer, refuse redirects outside loopback, and avoid reading deployed
credential variable names. An offline capability must independently enforce
its no-network contract. The parent cannot prove those child properties by
argv alone; they are high-risk capability contracts tested and reviewed where
the child is owned.

This separation is structural at the dispatcher boundary but is not actor
authentication. A person or agent with shell access can invoke another script
directly. Cairn therefore combines the absence of any deployed dispatcher path
with capability-side refusals and a doctrine rule that deployed credentials
are Maintainer-owned. It does not claim to distinguish a human process from an
agent process.

### Result contract

The dispatcher owns one aggregate result space:

* **0 -- CLEAN:** every selected, applicable local/offline leg ran and reported
  no finding.
* **5 -- INCOMPLETE:** no finding, but a selected applicable leg or required
  local evidence was unavailable.
* **10 -- FINDINGS:** at least one validated child result contains a finding.
* **20 -- DEGRADED / TAMPER:** integrity failed, dispatch escaped the registry,
  output was invalid or oversized, a timeout occurred, or a child failed
  outside its contract.

Precedence is 20 > 10 > 5 > 0. No selected local capability is visibly `NOT
APPLICABLE` and exits 0. A selected module whose generated policy remains
`configured: false` is INCOMPLETE. CLEAN is scoped to the local/offline legs
that ran; it says nothing about Maintainer-owned deployed evidence.

The dispatcher emits its own deterministic JSON summary after validating child
results. It does not relay raw child output. Every result names the selected
module, applicability reason, exact runner digest, evidence mode, result, and
omitted deployed responsibility when one exists.

### Adoption must be non-silent

Default-on means **every adopter** receives the dispatcher, module doctrine,
install-manifest entries, lockfile mapping, and `AGENTS.md` rule, including an
adopter that selects no security capability. The no-capability result is cheap
and explicitly not applicable; that does not make the install-contract change
non-universal.

Three points make selection visible without running a host tool during
installation:

* scaffold summary names each selected security capability, its local command,
  prerequisites, and the meaning of a missing tool or policy;
* successful installation prints the first-run aggregate command and never
  claims that installation itself produced security evidence; and
* the installed `AGENTS.md` rule establishes the trusted-checkout cadence.

The scaffold does not edit third-party CI and does not execute a selected
scanner. A project may add CI after reviewing its platform and secret boundary,
but this proposal does not infer that authority.

### Sequencing and ownership

This proposal owns activation only. `portable-security-sweeps` and
`api-web-security-modules` must record the reciprocal dependency before their
Decisions. The intended order is:

1. decide this activation contract;
2. decide each capability's evidence and trust boundary independently; and
3. coordinate implementation plans so registry entries land with, not before,
   their accepted capability.

An activation implementation may ship with no dormant entry whose capability
has not been accepted. Conversely, a capability must not call itself activated
until its fixed entry and the deletion-mutant test for the standing command are
present.

### Documentation / doctrine surface

* `templates/core/AGENTS.md` receives only the local standing command and adds
  the dispatcher to its high-risk surfaces.
* `security-verification` doctrine owns registry rules, aggregate exits,
  trusted-checkout scope, local/deployed separation, and recovery from
  incomplete or degraded evidence.
* Capability doctrine owns credentials, network targets, fixture safety,
  findings, omissions, and any Maintainer-run deployed procedure.
* `bootstrap/SAFETY.md` records child-process execution, lockfile integrity,
  ambient-environment reduction, and the fact that command separation is not
  actor authentication.

This is a governing operational change. The Maintainer-classified security
surface and the credential/egress finding at `7125de4` clear the doctrine
rate-limit and require the stated security-lens review.

## Rationale

A selected security module should change expected work, not merely add a file
that can be forgotten. One local command gives adopters a stable habit while
preserving the important boundary: agents can gather reversible evidence from
a trusted checkout, while outward-facing or credentialed acts remain explicit
Maintainer procedures.

Splitting activation also keeps review proportional. The dispatcher can be
judged on registry integrity, subprocess behavior, and universal installation
without forcing that Decision to settle API authorization, HTTPS parsing, or a
specific scanner's transitive configuration surface.

## Alternatives considered

**Keep activation in `api-web-security-modules`.** Rejected after AW3. It makes
an already-needed local adoption mechanism wait on two unrelated network
clients and obscures which artifact owns the shared command.

**Put local and deployed modes in one dispatcher.** Rejected after AW1/AW2. A
mode flag on an agent-facing command is not an actor boundary, and it creates a
routine path toward credentials and live systems.

**Make the dispatcher opt-in.** Rejected as shelf apparatus. Capability
selection would still require an adopter to discover and install the mechanism
that makes selection operational.

**Edit adopter CI automatically.** Rejected. CI providers, credentials,
untrusted-change behavior, and secret exposure need platform-specific review.

**Do nothing.** Safe but ineffective: portable sweeps remains correctly held,
and future capability modules can be installed without entering normal work.

## Evidence / verification plan

The plan must include:

* strict lockfile and fixed-registry tests, including unknown module and
  candidate-controlled path/argv/environment attempts;
* public-path subprocess tests for exact child argv, minimal environment,
  timeouts, output caps, invalid UTF-8/JSON, forged terminal controls, and every
  aggregate precedence pair;
* proof that the dispatcher opens no socket, performs no DNS lookup, and does
  not read deployed credential variables;
* child fixtures proving only the fixed local/offline subcommand is reachable;
* scaffold tests for every preset/module combination, literal `modules:` lists,
  removal, complete mapping groups, summary/install messaging, lockfile and
  manifest coverage, upgrade/adopt, and collision handling;
* an installed-output test proving the exact `AGENTS.md` command exists, plus a
  deletion mutant that fails;
* composition tests for no capability, each capability alone, and multiple
  capabilities without duplicate or silently delegated evidence; and
* the full `bootstrap/tests` suite under canonical Python 3.13.

The implementation is wrong if a project file can add or steer a child, a
deployed route or credential lookup becomes reachable from the dispatcher,
raw child output reaches the terminal, selection can be CLEAN without running
its applicable local leg, or installation claims evidence it did not gather.

## Review -- Gemini Flash (External, security lens) -- 2026-08-03

**Steelman.** This proposal cleanly resolves the architectural security defect identified in review AW3 by separating local, offline evidence collection from credentialed, deployed operations. By introducing a default-on local dispatcher (`run_security_verification.py`) governed by a fixed source-owned registry, strict environment sanitization (stripping credential and proxy variables), `shell=False` execution, and a 4-tier aggregate exit contract (0 CLEAN, 5 INCOMPLETE, 10 FINDINGS, 20 DEGRADED/TAMPER), it establishes a safe, predictable trusted-checkout verification habit for adopters without exposing remote endpoints or ambient credentials.

### Concerns

* **[E1] Structural reliance on child runner network/credential safety.**
  Although the dispatcher strips credential-bearing environment variables and enforces `shell=False` with fixed argument vectors, it cannot independently prevent a child script from attempting network I/O if the child itself is flawed. Child modules registered in the fixed registry (e.g., from `portable-security-sweeps`) must maintain strict loopback/offline guarantees verified at their own boundary.
* **[E2] Universal default-on installation footprint.**
  Making `security-verification` a default-on module adds dispatcher scripts and `AGENTS.md` rules to every adopter tree, including minimal presets. The proposal handles this appropriately by ensuring zero-capability runs complete cheaply without reporting false security claims.

### Covered

* **Claim-check Verification**:
  - `claim_check.py`: verified clean output on `dev/proposals/2026-08-03-codex-security-verification-activation.md`.

```
$ ~/conda_envs/lhm/bin/python scripts/claim_check.py dev/proposals/2026-08-03-codex-security-verification-activation.md
claim_check: dev/proposals/2026-08-03-codex-security-verification-activation.md -- OK, no claim-check flags.
```

### Not covered / low confidence

* Subprocess isolation and aggregate exit precedence behavior will be verified when `bootstrap/tests/test_security_verification.py` is implemented.

### Recommendation

**SHIP.** The proposal's separation of local dispatcher routes from deployed actions, fixed registry model, and aggregate exit contract are structurally sound and resolve prior security review concerns.

