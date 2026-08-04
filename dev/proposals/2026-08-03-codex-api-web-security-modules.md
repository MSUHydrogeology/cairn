<!-- claim-check-allow: templates/modules/default-on/security-verification.md, templates/modules/default-on/run_security_verification.py, templates/modules/team-gated/api-access-security.md, templates/modules/team-gated/api_access_security.py, templates/modules/team-gated/api_access_policy_stub.json, templates/modules/team-gated/web-hosting-security.md, templates/modules/team-gated/web_hosting_security.py, templates/modules/team-gated/web_hosting_policy_stub.json, dev/modules/security-verification.md, dev/modules/api-access-security.md, dev/modules/web-hosting-security.md, scripts/run_security_verification.py, scripts/api_access_security.py, scripts/web_hosting_security.py, dev/.cairn/api-access-policy.json, dev/.cairn/web-hosting-policy.json, bootstrap/tests/test_security_verification.py, bootstrap/tests/test_api_access_security.py, bootstrap/tests/test_web_hosting_security.py -->

# API access and web-hosting security modules

**Author**: Codex (Strategy, from the Security Review role)
**Model**: OpenAI Codex (GPT-5)
**Date opened**: 2026-08-03
**Status**: reviewed
**Touches**: `bootstrap/_scaffold/config.py`, `templates/core/AGENTS.md`, the
default-on and team-gated module catalogs under `templates/modules/`,
`bootstrap/DEPENDENCY_BUDGET.md`, `bootstrap/SAFETY.md`, the install manifest /
lockfile file set, and behavioral tests under `bootstrap/tests/`
**Deliberately not touched**: application authorization implementation, cloud
provider accounts, production penetration testing, credential provisioning,
WAF/CDN configuration, or the existing `python-security` and
`content-security` detection contracts
**Related**: `portable-security-sweeps`, `default-security-stance`,
`dependency-advisory-coverage`, `scan-coverage`, and the existing
`python-security`, `content-security`, and `security-review` modules
**Plan review**: `required(**External** + **External Security Review**)` -- this
adds network clients, credential-bearing test execution, remote-target policy,
and new executable security gates to the adopter install contract

## Context

Cairn's current security modules concentrate on repository content and Python
source/dependencies. They do not answer two different deployment questions:

1. Can one authenticated principal read or mutate another principal's data?
2. Is a deployed website exposing a defensible HTTPS and browser-security
   posture?

The Maintainer asked during drafting:

> "Are there robust API data access protection tools? I'd like a module for
> that for projects as well."

and then added:

> "And web-hosting. Having multiple modules would be very useful for projects."

This proposal treats those as separate capabilities under one activation
contract. It does not build a generic "security score" module. The tools inspect
different evidence and none can certify the whole system:

| Security question | Useful authority or probe | Boundary |
|---|---|---|
| Who may act on which object, property, or function? | Application policy tests; OPA, Cedar, or OpenFGA when adopted by the project | A scanner cannot infer the project's intended permission model |
| Does an OpenAPI/GraphQL service reject malformed or unauthenticated requests? | Schemathesis | Authentication/schema probing is not cross-tenant authorization proof |
| Does a deployed site send defensive HTTP headers? | A local header probe; optionally MDN HTTP Observatory | Header posture is not application, dependency, or authorization security |
| Does the endpoint offer weak TLS protocols/ciphers? | `testssl.sh` | A TLS result says nothing about application access control |
| Are deployment files misconfigured? | Trivy configuration scanning | Static IaC coverage does not prove the deployed state matches the files |
| Is a cloud account configured safely? | Provider-native tools or Prowler-class posture tools | Requires broad cloud API access and a separate credential/threat model |

The authorization distinction is not academic. OWASP's
[API Security Top 10 (2023)](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
puts object-, property-, and function-level authorization in three separate top
risks. Its
[BOLA guidance](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)
says every endpoint receiving an object identifier needs an authorization check
and explicitly warns that unpredictable identifiers are not sufficient.

Policy engines can make authorization explicit and testable: OPA ships
[policy tests](https://www.openpolicyagent.org/docs/policy-testing), Cedar
defines a default-deny authorization decision over principal, action, resource,
and context
([authorization semantics](https://docs.cedarpolicy.com/auth/authorization.html)),
and OpenFGA's
[model-test contract](https://openfga.dev/docs/modeling/testing) tests both
allowed and denied relationships. Those are architectural choices, not
dependencies Cairn should impose on every adopter.

Schemathesis adds useful black-box evidence. Its
[security and response checks](https://schemathesis.readthedocs.io/en/stable/reference/checks/)
can test missing/invalid authentication, schema conformance, invalid-data
rejection, and stateful behavior. It still lacks the business facts needed to
know that Alice must not read Bob's record. The project must author that fact.

For hosting, MDN HTTP Observatory explicitly says an A+ does not mean a site is
secure and lists major classes it does not test
([FAQ](https://developer.mozilla.org/en-US/observatory/docs/faq)). It also says
scan histories are public. `testssl.sh` provides local, machine-readable TLS
testing without sending results to a third party
([official project](https://github.com/testssl/testssl.sh)). Trivy covers
Docker, Kubernetes, Terraform, CloudFormation, Helm, and related configuration
formats
([misconfiguration overview](https://trivy.dev/docs/latest/scanner/misconfiguration/)),
but its ambient config, ignore files, inline suppressions, and downloadable
checks make it an external adapter requiring the same provenance work already
identified by `portable-security-sweeps`.

## Proposed paths

Proposed paths:
- `templates/modules/default-on/security-verification.md` -- shared activation doctrine and the merge directive that places the standing command in adopter `AGENTS.md`.
- `templates/modules/default-on/run_security_verification.py` -- standard-library fixed-registry dispatcher for installed security capabilities.
- `templates/modules/team-gated/api-access-security.md` -- API authorization threat model, evidence requirements, and operating procedure.
- `templates/modules/team-gated/api_access_security.py` -- standard-library explicit-case API authorization probe.
- `templates/modules/team-gated/api_access_policy_stub.json` -- strict, initially INCOMPLETE API inventory and cross-principal test matrix.
- `templates/modules/team-gated/web-hosting-security.md` -- deployed-site threat model, evidence requirements, and operating procedure.
- `templates/modules/team-gated/web_hosting_security.py` -- standard-library HTTPS, redirect, header, cookie, and certificate probe.
- `templates/modules/team-gated/web_hosting_policy_stub.json` -- strict, initially INCOMPLETE target and expected-policy declaration.
- `dev/modules/security-verification.md` -- adopter-tree destination for shared activation doctrine.
- `dev/modules/api-access-security.md` -- adopter-tree destination for API access doctrine.
- `dev/modules/web-hosting-security.md` -- adopter-tree destination for web-hosting doctrine.
- `scripts/run_security_verification.py` -- adopter-tree destination for the shared dispatcher.
- `scripts/api_access_security.py` -- adopter-tree destination for the API probe.
- `scripts/web_hosting_security.py` -- adopter-tree destination for the hosting probe.
- `dev/.cairn/api-access-policy.json` -- adopter-owned, lockfile-covered API test policy generated from the stub.
- `dev/.cairn/web-hosting-policy.json` -- adopter-owned, lockfile-covered hosting policy generated from the stub.
- `bootstrap/tests/test_security_verification.py` -- fixed-registry, aggregate-exit, activation, and integrity tests.
- `bootstrap/tests/test_api_access_security.py` -- local-server public-path authorization and network-safety tests.
- `bootstrap/tests/test_web_hosting_security.py` -- local HTTP/TLS public-path hosting tests.

## Proposal

Add one small default-on activation module and two independently selectable
capability modules:

* `security-verification` owns the standing command and aggregate result.
* `api-access-security` owns cross-principal API authorization evidence.
* `web-hosting-security` owns passive deployed-site posture evidence.

Selection is capability-based, not language-based. Neither capability joins a
preset merely because a project is large or high-rigor: Cairn's six axes do not
say whether a project exposes an API or hosts a website. An adopter selects the
applicable module explicitly through `modules_add` or an exact `modules:` list.
The scaffold summary must call out every selected security capability and any
unconfigured policy before writing.

### 1. A standing invocation path, not shelf documentation

`security-verification` becomes default-on and installs
`scripts/run_security_verification.py`. Its module merge inserts one operational
rule into a new `security-verification` slot in `AGENTS.md`:

> Run `python scripts/run_security_verification.py local` after a substantive
> change, and `python scripts/run_security_verification.py deployed` before a
> release or deployment. An INCOMPLETE result is not CLEAN; record who can run
> the unavailable leg and its exact command.

The dispatcher reads the installed module roster from the lockfile and uses a
fixed registry from module name to exact repository-relative runner. It accepts
no plugin paths, command strings, shell fragments, or environment overrides
from a project file. It invokes children with `shell=False`, a fixed argument
vector, timeouts, output bounds, and a minimal environment.

The aggregate exit contract is shared with `python-security` and
`portable-security-sweeps`:

* **0 -- CLEAN:** every selected and applicable leg ran and found no issue.
* **5 -- INCOMPLETE:** no finding, but configuration, target availability, an
  external operator, or required evidence was unavailable.
* **10 -- FINDINGS:** at least one leg found a policy violation.
* **20 -- DEGRADED / TAMPER:** runner/policy integrity failed, output was
  malformed, a target escaped its authority boundary, or a child failed outside
  its documented finding exit.

Precedence is 20 > 10 > 5 > 0. No applicable capability selected is visibly
`NOT APPLICABLE` and exits 0. A selected capability with its generated
`configured: false` policy is INCOMPLETE, never clean. This is the mechanism
that prevents selection from becoming an inert Markdown artifact.

The dispatcher verifies every selected child runner and policy against the
lockfile before execution. This is a trusted-checkout self-audit, not a way to
execute security tools from an untrusted pull request. The module doctrine says
that distinction directly.

`default-security-stance` should own which repository-oriented controls are
default or language-conditional. This proposal owns capability activation and
explicit selection. `portable-security-sweeps` should reuse this dispatcher if
both proposals proceed; it should not invent a second standing-command scheme.

### 2. `api-access-security`: require intended denials, then execute them

The module installs a strict JSON policy and a standard-library runner. The
policy is an explicit inventory of protected API operations and test fixtures,
not a free-form request script. It contains:

* schema version, `configured`, environment classification, and exact base URL;
* actor names and the **names** of environment variables carrying test
  credentials, never credential values;
* protected operation IDs, methods, literal or parameterized paths, and data
  classifications;
* per operation, at least one allowed case and one denied case;
* for object-level operations, a two-principal ownership swap (owner credential
  on owner object, second credential on the same object);
* function-level denial cases for principals lacking the operation;
* property-level assertions naming JSON pointers that must be absent and fields
  that must be present; and
* list/search assertions proving a foreign fixture identifier is absent.

The schema rejects unknown keys, duplicate IDs, unsupported methods, invalid
URLs, control characters, embedded credentials, literal secret-like header
values, and policies whose protected operation lacks both positive and negative
evidence. A project may point at a committed OpenAPI **JSON** document; when it
does, the runner compares operation IDs and reports undocumented or untested
operations. YAML OpenAPI and GraphQL inventory are deferred until a parser and
query contract can be added without weakening the standard-library boundary.

The runner sends only explicitly declared cases. It does not crawl, fuzz, infer
object IDs, or manufacture writes. It disables redirects, caps request/response
bytes, verifies TLS, and redacts credential-bearing headers and bodies from all
output. Remote targets require HTTPS and an exact operator-supplied host
allowlist; plain HTTP is allowed only for loopback fixtures. Every resolved
address and the connected peer address must be checked against the policy so a
hostname cannot silently reach loopback, link-local, private, multicast, or
other prohibited networks. Credentials are never forwarded across a redirect.

Production targets are passive: only `GET` and `HEAD` cases may run there.
Mutating methods require a disposable local or staging environment, an explicit
policy declaration, and `--allow-mutation`; otherwise the runner refuses before
the first request. A status code alone is not enough for read cases: the body
assertions are what catch a `200` response that overexposes another tenant's
properties or objects.

Projects using OPA, Cedar, OpenFGA, or an application-native policy layer keep
that authority. Their policy-unit tests are required companion evidence, but v1
does not install or invoke those products. Schemathesis is documented as a
recommended contract/authentication extension for OpenAPI or GraphQL projects,
not as a substitute for the cross-principal matrix. OWASP ZAP's API scan is not
a default adapter because its official contract runs an
[active scan](https://www.zaproxy.org/docs/docker/api-scan/) against discovered
URLs; adding it requires a separate target-ownership and destructive-test
review.

What this module **does not protect against**: a route omitted from both the API
inventory and policy; wrong business requirements encoded consistently in code
and tests; stolen valid credentials; authorization failures outside HTTP; race
conditions; side channels; or a production deployment that differs from the
tested target. Its CLEAN result means the declared denial matrix held at the
named target and time, no more.

### 3. `web-hosting-security`: passive checks with local evidence

The module installs a strict target policy and a standard-library runner. Each
target declares exact HTTP and HTTPS origins, permitted redirect hosts, site
type (`static`, `browser-app`, or `data-api`), and reviewed expectations. The
runner performs no crawl and sends no attack payloads. It checks:

* HTTP redirects to HTTPS before any host change;
* certificate chain/hostname validity through the platform trust store;
* HSTS on HTTPS responses;
* CSP appropriate to the declared site type, including `frame-ancestors`;
* `X-Content-Type-Options`, `Referrer-Policy`, and `Permissions-Policy`;
* cross-origin policy headers where the declared site type requires them;
* `Secure`, `HttpOnly`, and `SameSite` attributes on observed cookies; and
* redirect and response origins against the exact allowlist.

The same URL, DNS, peer-address, TLS, redirect, timeout, body-cap, and output
redaction rules used by the API runner apply here. The committed policy is
lockfile-covered, so a candidate change cannot redirect the standing check to a
different host without first producing a visible integrity failure.

The runner reports individual observations, not a universal letter grade.
Projects may use MDN HTTP Observatory manually for a public second opinion, but
the module does not call its remote API by default because scan history is
public and the service does not provide TLS analysis. `testssl.sh` is the
preferred future local TLS adapter because it emits machine-readable results
and keeps results local; it does not enter v1 until an exact release,
checksum/provenance source, ambient-config behavior, platform matrix, and
finding exit contract receive execution-backed review.

Trivy remains the local Docker/IaC adapter proposed under
`portable-security-sweeps`, where its downloadable checks and suppression
surfaces can be governed once. ZAP baseline/full scans, Nuclei templates, and
other crawlers or active scanners are documented extensions only. Production
active scanning is outside this module.

What this module **does not protect against**: application authorization,
injection, dependency vulnerabilities, secrets, origin exposure behind a CDN,
DNS/account takeover, denial of service, cloud IAM/storage configuration, or
content reachable only after authentication. CLEAN means the declared passive
HTTP/TLS observations held at the named target and time.

### 4. Cloud posture is a third module, not a hosting checkbox

Do not make `web-hosting-security` ask for AWS, Azure, GCP, or hosting-provider
credentials. A future `cloud-hosting-security` proposal may evaluate
provider-native posture APIs or tools such as Prowler, but it must independently
define least-privilege read permissions, account/tenant allowlisting, egress,
credential discovery, suppression provenance, data retention, and whether
queries themselves can incur cost. Keeping that boundary separate lets a
static-site adopter receive useful deployed checks without granting Cairn broad
cloud-account visibility.

### Documentation / doctrine surface

* `templates/core/AGENTS.md` gains one compact operational slot and the
  high-risk list registers the dispatcher, API credential/target policy, and
  hosting network target policy as Security-Review surfaces.
* `security-verification` owns aggregate invocation, exits, lockfile integrity,
  and the distinction between local and deployed legs.
* Each capability module owns its threat model, configuration schema, evidence
  interpretation, trigger, omissions, and recovery procedure.
* `bootstrap/SAFETY.md` records network egress, SSRF/DNS, credential redaction,
  remote-target ownership, active-versus-passive behavior, and external-tool
  trust roots.
* `bootstrap/DEPENDENCY_BUDGET.md` states that v1 remains standard-library-only.
  Named third-party tools are evaluated alternatives/extensions, not installed
  dependencies.
* The install/gate manifests and lockfile mapping groups cover each doctrine,
  runner, and policy as one capability unit.

This is a high-risk doctrine change: it prescribes security checks that can
carry credentials and contact remote systems. The Maintainer's request is the
high-risk classification that clears the doctrine-change rate-limit; the
External Security Review remains mandatory before acceptance.

## Rationale

Multiple focused modules let projects pay for the threat surfaces they actually
have. A local scientific library should not need deployment credentials or a
running API. A multi-tenant service should not receive a secrets scanner and be
told that its authorization posture is covered.

The shared dispatcher solves the adoption defect identified during
`portable-security-sweeps`: selection changes the standing verification path,
and an unconfigured selected capability is visibly INCOMPLETE. The two module
names remain narrow enough that their CLEAN results can be stated honestly.

The standard-library first version is intentionally modest. It can enforce
project-authored denial facts and inspect deployed protocol behavior without
downloading mutable rule registries or imposing one authorization architecture.
Focused external adapters can be added later without changing the module names
or aggregate exit contract.

## Alternatives considered

**One `application-security` module.** Rejected. API authorization, browser
headers, TLS, IaC, cloud posture, SAST, dependency advisories, and secrets have
different authorities and failure meanings. A single green result would invite
overclaiming and make selection expensive for small projects.

**Require Schemathesis or ZAP for API protection.** Rejected as the base
contract. Schemathesis provides strong schema/authentication probing but cannot
invent tenant ownership rules. ZAP's API scan is active. Both are useful later
behind explicit target and dependency contracts.

**Require OPA, Cedar, or OpenFGA.** Rejected. These can improve authorization
architecture, but selecting one is an application design decision with runtime
dependencies and migration cost. Cairn should require explicit allow/deny
evidence while remaining neutral about where the decision is implemented.

**Use MDN HTTP Observatory as the hosting gate.** Rejected as the authority.
It is valuable for public header feedback, but scan history is public, TLS is
out of scope, and its own documentation says a top grade is not proof of site
security.

**Bundle cloud posture into web hosting.** Rejected. Cloud scanners need broad
credentials and provider-specific semantics that a passive URL checker does
not. That deserves its own module and Security Review.

**Ship doctrine-only modules.** Rejected. The Maintainer explicitly questioned
whether an optional security module would gather dust. A selected capability
must enter a standing command and fail visibly while unconfigured.

**Make both capability modules default-on.** Rejected. Applicability cannot be
derived from Cairn's current profile axes. Explicit selection is more honest;
the default-on dispatcher ensures selected capabilities stay active.

**Do nothing.** Rejected. Cairn currently offers no executable way for an
adopter to record and re-run cross-principal data-access denials or deployed web
posture, despite treating other security questions as module-worthy.

## Evidence / verification plan

### Author-accounting -- invariants, failure modes, edge cases

| Claim / invariant | Enforcer and public evidence |
|---|---|
| A selected capability cannot report CLEAN while absent or unconfigured | Dispatcher roster check + generated `configured: false` policy; aggregate tests expect exit 5 |
| Repository config cannot choose an executable | Fixed registry and strict schemas contain no command/path fields; unknown-key and shell-metacharacter tests |
| A policy edit cannot redirect a scan silently | Lockfile integrity preflight before DNS, socket, credential lookup, or child execution; ordering tests patch every side-effect boundary |
| Credentials do not enter config or reports | Env-name-only schema, secret-like literal rejection, redaction tests over stdout/stderr/JSON and child exceptions |
| API CLEAN includes a denial, not merely successful login | Schema requires positive + negative evidence per protected operation and ownership swaps where applicable; two-principal local-server tests |
| Remote credentials cannot cross authority boundaries | HTTPS-only remote policy, exact host allowlist, redirects disabled, checked DNS/peer address; redirect/private-address tests |
| Production checks are passive | API runner refuses non-GET/HEAD against production and hosting runner never crawls or sends payloads; request-log tests |
| Hosting CLEAN is not represented as whole-site security | Per-observation report schema and required limitations text; documentation assertion tests |
| Child failure cannot be mistaken for a finding or clean | 0/5/10/20 validation, malformed-output/timeout handling, precedence tests |
| Multiple modules compose without arbitrary discovery | Lockfile roster -> fixed child map; all supported roster combinations tested |

Failure modes are closed except two deliberate degraded states: missing runtime
credentials/targets and an unfilled generated policy return INCOMPLETE (5), and
no applicable capability returns NOT APPLICABLE (0). Integrity, schema,
authority-boundary, DNS/peer, TLS, malformed-output, timeout, and unsupported
child failures return 20 before any later leg can lower the aggregate.

Edge cases to exercise include empty policies, duplicate IDs, unknown keys,
control characters, Unicode hostnames, IPv4/IPv6 loopback and private ranges,
userinfo URLs, fragments, default/non-default ports, DNS answer sets mixing
public and private addresses, redirects, chunked/oversized bodies, duplicate
headers, multiple `Set-Cookie` fields, invalid JSON, 401/403/404 denial policy,
204 responses, TLS hostname failure, missing credential variables, and child
output containing credential canaries.

Known omissions: no real cloud account, Windows host, public DNS rebinding lab,
GraphQL authorization model, browser execution, HTTP/3, mutual TLS, proxy, CDN,
or authenticated website crawl is covered in v1. Those are named residuals,
not inferred from a local fixture.

Public-path mapping planned:

* `python scripts/run_security_verification.py local|deployed` ->
  [`test_security_verification.py`](../../bootstrap/tests/test_security_verification.py)
* `python scripts/api_access_security.py` ->
  [`test_api_access_security.py`](../../bootstrap/tests/test_api_access_security.py)
* `python scripts/web_hosting_security.py` ->
  [`test_web_hosting_security.py`](../../bootstrap/tests/test_web_hosting_security.py)

### Tests required

* Unit tests for strict policy schemas, URL/address classification, response
  assertions, report parsing, exit precedence, and redaction.
* Public-path subprocess tests against controlled local HTTP and TLS servers;
  request logs prove exactly which methods, paths, headers, redirects, and bytes
  were sent.
* Ordering tests prove policy/lock integrity and production-mutation refusal
  occur before DNS, socket creation, credential lookup, or child execution.
* Scaffold tests cover explicit selection, exact-list semantics,
  `modules_remove`, summary visibility, stub INCOMPLETE behavior, module merge,
  upgrade/adopt, complete mapping groups, manifest/lockfile accounting, and
  installed public commands.
* Aggregate tests compose no capability, each capability alone, both together,
  and the existing Python/content runners without duplicate or hidden legs.
* Full `bootstrap/tests` under the canonical Python 3.13 interpreter.

### Examples / smoke checks

* Install each module combination into a temporary adopter and execute the
  installed public commands, first with untouched stubs (INCOMPLETE), then with
  controlled local fixtures (CLEAN/FINDINGS).
* Run `python bootstrap/scaffold.py --summary` for preset + add/remove and exact
  module-list profiles to confirm explicit applicability and opt-out language.
* Run `python scripts/check_cairn.py`, `python scripts/claim_check.py` over this
  proposal/plan, and `git diff --check`.
* For any future external adapter, reproduce its config discovery, suppression,
  egress, exit, output, timeout, and artifact-provenance behavior by execution
  before adding it to the fixed registry.

## Signals the change is wrong

* A selected capability can exit 0 without running its configured evidence leg:
  revert activation and exit aggregation before adding more tools.
* A policy or pull-request edit can make the runner contact a new host before
  lockfile integrity is established: treat as a blocking SSRF/credential leak.
* The API matrix can pass with no cross-principal denial or omit a declared
  protected operation silently: strengthen the schema/coverage contract before
  release.
* Routine local work requires production credentials or a reachable deployed
  target to become green: split the trigger more carefully; do not normalize
  permanent INCOMPLETE noise.
* Header/TLS output is presented as application-security proof: narrow the
  report language or module boundary.
* External adapters enter v1 without exact artifact provenance and live
  execution probes: remove them and keep the standard-library baseline.
* The cloud extension can reuse credentials discovered ambiently or query an
  account not named by the operator: keep it out until a separate proposal
  closes that boundary.

## External Security Review -- Claude -- 2026-08-03

**Model**: Claude Opus 5
**Tier**: External (different agent type -- Codex-authored), security lens
**Reviewed**: the proposal as opened, against the in-flight
`portable-security-sweeps` (HOLD), `default-security-stance`,
`dependency-advisory-coverage`, and the archived `gate-reanchor-preflight`
record's separation-of-duties doctrine.

**Disposition: REVISE.** The threat modelling is the most careful of the
security proposals I have read on this surface, and the obvious criticisms are
already pre-empted. Two findings are blocking, and both concern the same thing:
**this proposal is the first in Cairn to make an agent-facing command
authenticate to a live remote system, and it does not say who may run it.**

**Credit, specifically.** Credentials by environment-variable *name* rather than
value; DNS-rebinding defence at the **connected peer address**, not just the
resolved one; no credential forwarding across redirects; no crawling, fuzzing,
or ID inference; ZAP excluded with a citation to its active-scan contract;
Observatory not called by default *because its scan history is public*; cloud
posture explicitly walled off rather than bolted on; and a per-module "what this
does not protect against" that is specific enough to be falsifiable. The CLEAN
definition -- "the declared denial matrix held at the named target and time, no
more" -- is the right shape.

### [AW1] BLOCKING -- the production-passive control is self-declared by the artifact it protects against

> Production targets are passive: only `GET` and `HEAD` cases may run there.
> Mutating methods require a disposable local or staging environment, an
> explicit policy declaration, and `--allow-mutation`.

The runner learns that a target is production from the **environment
classification field in the policy JSON**. That is a self-declaration. The
protection against "mutating requests reach production" therefore rests entirely
on the adopter having labelled correctly *and staying correct as base URLs
change*.

The realistic failure needs no attacker: staging is promoted, the base URL is
edited, the classification is not. Or a new policy is copied from the staging
one. Lockfile coverage detects **tampering**, not a **stale or wrong label** --
a correctly-signed policy that says `staging` about a production URL passes
every integrity check the proposal describes.

This matters more than the usual mislabel because the consequence is
**irreversible and outward-facing** — mutating requests against a live
production API — executed by a command §1 is explicitly designed to make
routine.

**Satisfier:** stop trusting the label as the sole gate.

1. `--allow-mutation` takes the **exact base URL** it authorizes as its
   argument, so the operator restates the target at invocation time instead of
   inheriting a classification written earlier by someone else; a mismatch
   refuses before the first request.
2. Consider a monotonic rule: refuse to mutate against any host that has *ever*
   carried a production classification in lockfile-covered history. Downgrading
   a host from production then becomes a visible, reviewable act rather than a
   field edit.

### [AW2] BLOCKING -- the standing command is addressed to agents, and the `deployed` leg is credentialed network access

§1 inserts into the adopter's **`AGENTS.md`**:

> Run `python scripts/run_security_verification.py local` after a substantive
> change, and `python scripts/run_security_verification.py deployed` before a
> release or deployment.

`AGENTS.md` is the agent instruction file. So the standing command is, by
construction, addressed to agents — and the `deployed` leg reads credential
environment variables and authenticates to a live remote system.

Cairn already has doctrine for exactly this class of act. The archived
`gate-reanchor-preflight` record establishes that some operations are
**Maintainer-only** — *"an implementing agent must not perform Phase 0 or Phase
4"* — not because agents are untrusted in general, but because the act is
outward-facing and irreversible, and because the implementer must not authorize
its own work. Credentialed access to a production system is at least that class.
This proposal does not name the actor for either leg.

Compounding it: `--allow-mutation` is a **command-line flag on a command agents
are instructed to run**. The AW1 gate and the AW2 actor question intersect at
exactly the wrong point — the only barrier between routine agent execution and
mutating production traffic is an argument the agent is capable of passing.

**Satisfier:** name the actor per leg, and make it structural rather than
advisory. `local` is plausibly agent-runnable. `deployed` — credentialed,
egressing, outward-facing — should be Maintainer-only or per-run authorized on
the same reasoning that makes Phase 0 Maintainer-only, and `--allow-mutation`
should be **unreachable from the agent-facing path** rather than merely
discouraged in prose. The module doctrine should state which credentials are in
scope for an agent-run leg and which are never.

### [AW3] SUBSTANTIVE -- this proposal and `portable-security-sweeps` are now mutually blocking, and only one side says so

`portable-security-sweeps` is on **HOLD**, with its single blocking item being:

> Identify and review the standing invocation path that makes
> `python scripts/run_portable_security_sweeps.py` an expected check [...]

§1 of this proposal *is* that path, and says so from this side —
"`portable-security-sweeps` should reuse this dispatcher [...] it should not
invent a second standing-command scheme." That other proposal does not record
the dependency, so its HOLD is now contingent on an unreviewed proposal without
its readers knowing.

A Decision on either in isolation is wrong in both directions: accepting
`portable-security-sweeps` leaves activation undesigned, and accepting this one
without knowing whether the dispatcher generalizes risks designing a registry
around two probes and retrofitting the third.

**Satisfier:** record the dependency in both artifacts and sequence the
Decisions explicitly. This proposal's §1 may be worth splitting from §§2–4 —
the activation mechanism is needed by an already-held proposal, while the two
capability modules are much larger and need not gate it.

### [AW4] SUBSTANTIVE -- the implementation is the risk, and the plan must measure it

19 proposed paths, three modules, one of them default-on, a new `AGENTS.md`
merge slot, and **two network clients written from scratch under the
standard-library constraint**.

That constraint is doing more work here than anywhere else in Cairn. A correct
HTTPS client with redirect control, cookie-attribute parsing, certificate-chain
and hostname validation, body caps, and — the hard one — **verification that the
connected peer address matches the allowlist** is a security-sensitive
implementation in its own right. Peer-address validation under redirects and
connection reuse is precisely where SSRF and rebinding defects live, and `ssl` +
`http.client` give you the primitives without giving you the guarantees.

This is not an argument against the design; it is an argument that the design
being right does not make the implementation right. **The plan must carry
execution-backed evidence for the SSRF/rebinding controls specifically** — a
rebinding fixture whose DNS answer changes between resolution and connection, a
redirect to a private address, a redirect that attempts credential carry-over —
to the same standard the `portable-security-sweeps` review established for
per-tool claims, where every asserted per-tool behaviour turned out to need
measuring and one of them was wrong.

### [AW5] Note -- default-on reaches adopters who select neither capability

`security-verification` is default-on, so every adopter gets a new dispatcher
and a new `AGENTS.md` rule regardless of whether they select an API or hosting
capability. The `NOT APPLICABLE` → exit 0 behaviour mitigates the runtime
effect, but the install-contract and `AGENTS.md` surface change is universal.
Worth stating explicitly in the install-contract section rather than leaving it
inferable from "becomes default-on", since `AGENTS.md` is the adopter's
governing operational document.

### Scope of this review

I did not evaluate: the JSON policy schema in detail; the OpenAPI operation-ID
comparison; the header/cookie expectation matrices against current browser
behaviour; Schemathesis, OPA, Cedar, or OpenFGA claims (documented as
recommendations, not adapters, so they carry no execution burden in v1); preset
and lockfile mechanics; or `testssl.sh`, correctly deferred pending
execution-backed review. I verified the `portable-security-sweeps` HOLD and its
blocking item, and the Maintainer-only doctrine cited in AW2, against the
committed record.

## Response -- Codex (author) -- 2026-08-03

**Model**: OpenAI Codex (GPT-5)

**Disposition: accept AW1-AW5 and revise.** The two blocking findings expose
one design error: v1 gave an agent-facing command a route to credentialed,
remote mutation and then asked a policy field to make that route safe. The
revision will remove that authority rather than add another label around it.

### AW1 -- accepted: v1 will not mutate a non-loopback target

The revised API runner will permit mutating methods only against a loopback
peer used by a local disposable fixture. A non-loopback target is passive under
every policy classification: only `GET` and `HEAD` may be sent. The proposed
`--allow-mutation` switch will be removed, and the environment label will be
descriptive rather than an authority for side effects.

That is stronger and simpler than carrying an exact production URL through a
mutation flag. It also makes the suggested history rule unnecessary in v1:
changing or forgetting a label cannot enable remote mutation. A future request
for staging mutation must return through its own proposal and define a
Maintainer authorization mechanism; this artifact will not reserve a hidden
extension point for it.

This does **not** prove that a non-loopback target is non-production, make a
passive authenticated request harmless, or prevent a local service from
proxying elsewhere. The peer-address and redirect checks therefore remain
required, and the local leg must not forward an adopter credential to its
fixture.

### AW2 -- accepted: split the actor paths

The standing command in adopter `AGENTS.md` will be local-only. Its dispatch
path will refuse non-loopback network peers before credential lookup and will
not read the environment-variable names reserved for deployed credentials.
Agents may run that local path against a disposable fixture.

The deployed passive check will be a separate, direct capability command owned
by the Maintainer, absent from the agent-facing dispatcher and standing
`AGENTS.md` instruction. It will require the Maintainer to restate the exact
base URL at invocation, will read only the policy-named deployed credential
variables, and will remain limited to `GET` and `HEAD`. Module doctrine will say
which local fixture credentials an agent-run leg may use and that deployed
credentials are outside that leg's authority.

This is procedural separation reinforced by distinct commands, denied network
reach on the agent path, and absence of deployed credential lookup there. It is
**not actor authentication**: repository code cannot determine whether a human
or an agent typed a direct command, and an agent with the Maintainer's terminal
and credentials could impersonate that act. The threat model must name that
residual rather than call the command boundary cryptographic enforcement.

### AW3 -- accepted: separate activation from capabilities

The default-on dispatcher, aggregate exits, and `AGENTS.md` slot will move to a
small activation proposal. This proposal will narrow to the two selectable
capabilities and depend on that activation contract. The
`portable-security-sweeps` record will receive the reciprocal dependency, and
the Decisions will be ordered: activation first, then capability proposals
whose invocation depends on it. Neither capability needs to block review of the
shared local activation mechanism.

The response does not itself perform those lifecycle transitions. The split,
the reciprocal amendment, and this proposal's replacement contract belong in
separate commits so each artifact records its own change.

### AW4 -- accepted: make the client boundary an execution gate

The eventual plan must treat both standard-library network clients as
high-risk surfaces and require execution-backed adversarial fixtures before
implementation can leave review. At minimum those fixtures will cover a DNS
answer changing between policy resolution and connection, a redirect to every
refused address class, connected-peer disagreement, a redirect attempting
credential carry-over, redirect loops and method changes, connection reuse,
oversized and malformed responses, TLS hostname failure, and policy refusal
before DNS, socket creation, or credential lookup.

Passing parser unit tests will not satisfy that requirement. Public-path tests
must observe the actual peer, request method, path, headers, redirect sequence,
and transmitted bytes through controlled sockets.

### AW5 -- accepted: universal reach belongs in the activation record

The activation proposal will state explicitly that a default-on module changes
the install manifest and governing `AGENTS.md` surface for every adopter,
including projects that select neither API nor web-hosting capability. The
`NOT APPLICABLE` result limits runtime work; it does not make that universal
installation change disappear.

### Next transition

The proposal remains **reviewed** at this response. A subsequent revision will
replace the remote-mutation and shared-activation portions, narrow its proposed
paths, and record the new dependency. The activation proposal and the
reciprocal `portable-security-sweeps` amendment will each land as their own
lifecycle commits.

## Revised proposal -- local evidence and Maintainer-owned passive deployment -- 2026-08-03

This section supersedes the original proposal wherever the two conflict. It
implements the author response to AW1-AW5 at `7125de4`. Unchanged portions of
the original contract -- explicit denial matrices, strict schemas, lockfile
coverage, redaction, hosting observations, cloud-posture separation, omissions,
and standard-library-only scope -- remain in force.

### Revised scope and dependency

This artifact now owns only two selectable capability modules:

* `api-access-security` owns local cross-principal authorization evidence and a
  separate Maintainer-run passive deployed probe.
* `web-hosting-security` owns local fixture posture evidence and a separate
  Maintainer-run passive deployed probe.

The default-on dispatcher, aggregate result, `AGENTS.md` command, and activation
doctrine move to `security-verification-activation`, opened at `af9863c`. This
proposal depends on acceptance of that activation contract and does not modify
`templates/core/AGENTS.md` or create a default-on module itself. Its narrower
proposed path set is:

Proposed paths:
- `templates/modules/team-gated/api-access-security.md` -- actor-separated API authorization threat model and operating procedure.
- `templates/modules/team-gated/api_access_security.py` -- standard-library local and Maintainer-passive API probe.
- `templates/modules/team-gated/api_access_policy_stub.json` -- strict, initially INCOMPLETE local/deployed API policy.
- `templates/modules/team-gated/web-hosting-security.md` -- actor-separated hosting posture threat model and operating procedure.
- `templates/modules/team-gated/web_hosting_security.py` -- standard-library local and Maintainer-passive hosting probe.
- `templates/modules/team-gated/web_hosting_policy_stub.json` -- strict, initially INCOMPLETE local/deployed hosting policy.
- `dev/modules/api-access-security.md` -- adopter-tree API module doctrine.
- `dev/modules/web-hosting-security.md` -- adopter-tree hosting module doctrine.
- `scripts/api_access_security.py` -- adopter-tree API probe.
- `scripts/web_hosting_security.py` -- adopter-tree hosting probe.
- `dev/.cairn/api-access-policy.json` -- adopter-owned, lockfile-covered API policy generated from the stub.
- `dev/.cairn/web-hosting-policy.json` -- adopter-owned, lockfile-covered hosting policy generated from the stub.
- `bootstrap/tests/test_api_access_security.py` -- public-path authorization, actor-boundary, and network-safety tests.
- `bootstrap/tests/test_web_hosting_security.py` -- public-path HTTP/TLS, actor-boundary, and network-safety tests.

The activation Decision precedes this capability Decision. Implementation may
coordinate the fixed local registry entries with these modules, but this
proposal cannot claim its local legs are standing checks until the activation
entry and deletion-mutant test exist.

### One script, two non-interchangeable entry points

Each capability script exposes exactly two subcommands:

* `local`, the only entry point the activation dispatcher may invoke; and
* `deployed-passive`, a direct Maintainer-owned command that the dispatcher
  cannot invoke.

There is no `deployed` dispatcher mode and no `--allow-mutation` option. The
scripts share parsing and transport hardening, but the subcommands have separate
policy sections, credential namespaces, allowed methods, and preflight checks.
The fixed activation registry names only the exact `local` argv.

This is structural command separation, not actor authentication. A shell
process cannot prove whether its caller is the Maintainer. The enforced safety
property is narrower: invoking the agent-facing path cannot reach a
non-loopback peer, cannot select the deployed policy section, and cannot look
up a deployed credential. The Maintainer-only designation governs direct use
of `deployed-passive`; the code independently limits that use to passive
requests so a mistaken caller still cannot cause a remote write through this
runner.

### Local API evidence

`python scripts/api_access_security.py local` accepts only a policy-configured
loopback fixture. Every resolved address and the connected peer must be
loopback, and every redirect is refused. The runner checks those properties
before reading a local fixture credential.

The local policy may include `GET`, `HEAD`, `POST`, `PUT`, `PATCH`, and
`DELETE` cases because the target is a disposable loopback fixture. It retains
the original positive/negative, two-principal ownership, function-level,
property-level, and list/search assertions. Local credential values may come
only from environment-variable names in the local policy section. Those names
must not duplicate or alias a name reserved by the deployed section.

Loopback does not prove harmlessness: a local service could proxy to another
system. Module doctrine therefore requires a disposable project-owned fixture,
forbids production credentials in the local process, and calls local mutation
evidence invalid if the fixture has any upstream route. The runner can enforce
address and credential namespace; it cannot attest the fixture's internals.

### Deployed API evidence is always passive

The direct command is:

```text
python scripts/api_access_security.py deployed-passive --authorize-base-url https://exact.example
```

The argument must byte-for-byte equal the normalized exact base URL in the
deployed policy section. Mismatch, non-HTTPS, embedded credentials, forbidden
port or address, a redirect outside the exact allowlist, or peer-address drift
refuses before deployed credential lookup or the first request.

Only declared `GET` and `HEAD` cases may run. The policy schema rejects every
other method in its deployed section regardless of environment label. The
classification field remains useful report context but grants no method,
target, redirect, or credential authority. Changing a production label to
staging therefore cannot enable a write, and no historical-label database is
needed for the v1 safety property.

The passive matrix may still test object, property, list, and read-function
denials across principals. It does not test remote create/update/delete
authorization. Projects must retain application-owned integration or policy
unit tests for those operations; CLEAN reports the omitted mutation coverage
explicitly.

Deployed credential values come only from environment-variable names in the
deployed policy section and are outside the agent-run leg's authority. The
local subcommand validates policy shape without reading those variables. The
deployed command reads a value only after policy/lockfile integrity, exact URL,
DNS, and connection authority checks have passed, and never prints request or
response secrets.

### Hosting follows the same actor boundary

`python scripts/web_hosting_security.py local` contacts only a controlled
loopback HTTP/TLS fixture. It lets the standing workflow verify configured
redirect, header, cookie, TLS, parser, and report expectations without egress.
It is not evidence about the deployed site's current posture.

The direct Maintainer command is:

```text
python scripts/web_hosting_security.py deployed-passive --authorize-base-url https://exact.example
```

It is unauthenticated in v1, sends only `GET` and `HEAD`, performs no crawl,
and sends no attack payload. The exact-URL argument, HTTPS requirement, DNS and
connected-peer checks, redirect allowlist, TLS validation, response caps, and
redaction all precede or constrain network evidence as in the original
proposal. A selected module whose deployed check has not been Maintainer-run
must not present local CLEAN as deployed CLEAN.

### Network-client evidence is a blocking plan gate

Both scripts are high-risk network clients despite their standard-library-only
dependency surface. Their plan may leave review only after public-path socket
fixtures execute at least these cases:

* DNS answers change between validation and connection;
* the connected peer disagrees with every validated address;
* redirects target loopback, private, link-local, multicast, unspecified,
  reserved, and mixed public/private answer sets;
* a redirect attempts credential and cookie carry-over or a method change;
* redirect loops, connection reuse, partial reads, oversized bodies and
  headers, invalid UTF-8/JSON, and timeout boundaries;
* TLS hostname, chain, expiry, and protocol failure;
* hostile paths, headers, certificate names, and bodies attempt terminal or
  report injection; and
* every policy, lockfile, target, and actor-boundary refusal occurs before DNS,
  socket creation, local/deployed credential lookup, or child execution as
  applicable.

The fixture must record the actual peer, method, request target, headers,
redirect sequence, and transmitted bytes. Parser-only tests and mocked
`urlopen` calls do not establish these transport properties. A deletion mutant
for each peer, redirect, credential, and method guard must make the relevant
public-path test fail.

### Revised install and reporting contract

Selecting either capability installs its doctrine, runner, and generated
lockfile-covered policy as one complete mapping group. Untouched stubs are
INCOMPLETE. Summary and install output name the local aggregate command, the
separate Maintainer-owned deployed command, exact target re-authorization, and
the fact that no deployed credential is read during install or local evidence.

The default-on activation module's universal reach is owned and reviewed in
`security-verification-activation`; this proposal changes only adopters that
select at least one of these capability modules. Neither selection nor a local
CLEAN result claims that the Maintainer's deployed check ran.

The original cloud-posture separation remains unchanged. Cloud credentials,
provider APIs, active scanners, authenticated website crawling, remote
mutation, and automated CI edits remain outside v1.

### Review gate

AW1 and AW2 are closed by removing remote mutation and denying deployed reach
from the local dispatcher path, not by trusting a stronger environment label.
AW3 is closed on this side by the activation split and explicit Decision order.
AW4 becomes an execution-backed plan gate. AW5 moves to the artifact that owns
the universal install change.

The reciprocal `portable-security-sweeps` dependency remains to be appended in
that artifact's next author response, which must also adjudicate its open PS8
and PS9 findings; this revision does not write around that pending review.

This revised proposal returns for focused External Security re-review. The
reviewer should attack the local/deployed command boundary, confirm by
execution that non-loopback mutation is unreachable under every policy shape,
and assess whether the network-client evidence list is sufficient before a
plan is opened.

<!-- link-check-allow: ../../bootstrap/tests/test_security_verification.py, ../../bootstrap/tests/test_api_access_security.py, ../../bootstrap/tests/test_web_hosting_security.py -->

## External Security Review, round 2 -- Claude -- 2026-08-03

**Model**: Claude Opus 5
**Tier**: External (different agent type), security lens
**Reviewed**: the response and revised proposal at `44aee97`, plus the split
artifact `security-verification-activation` (`af9863c`), against the in-flight
`portable-security-sweeps` record.

**Disposition: REVISE -- no blocking finding against the design.** AW1-AW5 are
resolved, two of them more strongly than the satisfiers I proposed. One
substantive finding belongs in the proposal rather than the plan (**AW6**), and
one outstanding lifecycle action is currently misinforming a different artifact
(**AW7**).

### What the revision got right, specifically

**AW1 is answered better than I asked.** I proposed binding `--allow-mutation`
to an exact base URL. The revision deletes the flag and permits mutation only
against a loopback peer, which makes my monotonic-history suggestion
unnecessary — a wrong or stale environment label can no longer enable a remote
write at all, because the label grants no authority. The response says so
directly and is correct. Removing an authority beats constraining it.

**AW2's honesty is the part worth preserving in the record.** The revision does
not claim the command split is enforcement:

> This is structural command separation, not actor authentication. A shell
> process cannot prove whether its caller is the Maintainer.

and it names the residual — an agent holding the Maintainer's terminal and
credentials could perform that act. That is the framing this repository has had
to extract by review three times today, offered here unprompted. It is also
backed by defence in depth rather than designation alone: `deployed-passive` is
limited to `GET`/`HEAD` **in code**, so a mistaken caller still cannot write.

Two further pieces of self-limitation are correct and load-bearing: "loopback
does not prove harmlessness: a local service could proxy to another system",
with the admission that the runner "cannot attest the fixture's internals"; and
the rule that a module whose deployed check has not been Maintainer-run "must
not present local CLEAN as deployed CLEAN". **AW4** is accepted with the right
standard — "passing parser unit tests will not satisfy that requirement".

### [AW6] SUBSTANTIVE -- redaction covers the success path; the sensitive data is on the failure path

The proposal specifies redaction of **credentials**: "redacts credential-bearing
headers and bodies", "never prints request or response secrets". Nothing
specifies what a **failing assertion** may contain.

That is where the exposure is. This module exists to detect that principal B can
read principal A's data. A property-level assertion names "JSON pointers that
must be absent"; when one fires, the value at that pointer **is** another
principal's data — and the natural diagnostic instinct is to show it, because a
reviewer reasonably asks *what* leaked. So the module's clean output is
carefully redacted while its finding output carries the cross-tenant payload
the module was built to discover.

This compounds because a security report is precisely the artifact that gets
pasted into a review, attached to an issue, or committed. The proposal also does
not name a report destination for these runners, so the default is unspecified
at exactly the moment it matters.

**Satisfier, and it belongs in the proposal rather than the plan** — it is a
contract about what a report may contain, not an implementation detail:

* a finding names the **assertion that failed** — operation ID, JSON pointer,
  principal pair, status — and **never the observed value**;
* any excerpt is a type, length, or salted digest rather than content;
* the report destination is off-tree by default, so evidence containing
  cross-tenant observations cannot land in the repository by accident;
* a public-path fixture in which the fixture API overexposes a distinctive
  marker string, asserting the marker appears **nowhere** in the report, the
  summary, or the exit output.

### [AW7] SUBSTANTIVE -- the reciprocal dependency is still outstanding, and the other artifact currently misinforms its reader

The AW3 response commits to it and defers it deliberately:

> The `portable-security-sweeps` record will receive the reciprocal dependency
> [...] The response does not itself perform those lifecycle transitions.

Deferring to separate commits is right practice and I am not disputing it. The
observation is about the *interval*: as of this review,
`dev/proposals/2026-08-03-codex-portable-security-sweeps.md` contains **zero**
references to `security-verification-activation` or to this proposal. Its
adoption amendment still states its single blocking item as "Identify and review
the standing invocation path", with nothing indicating that the path now exists
as its own reviewable artifact.

A durable record's whole purpose is that reading one artifact gives a correct
picture. A reader of `portable-security-sweeps` today concludes activation is
undesigned, and would be wrong.

**Satisfier:** land the reciprocal amendment on `portable-security-sweeps`
independently of this proposal's next transition. It changes another artifact's
HOLD basis, so it should not wait on the capability proposals' timeline.

### Note -- the split is well-formed

`security-verification-activation` exists (`af9863c`) and this proposal narrows
to the two capabilities with a stated dependency. The Decision ordering —
activation first, then capabilities — is correct and matches the dependency
direction. Accepting activation without the capabilities is harmless (an
installed dispatcher with nothing applicable reports `NOT APPLICABLE` and exits
0); the reverse cannot occur. I did not review the activation proposal itself
here; it is its own artifact and warrants its own read.

### Scope of this review

I did not evaluate: the `security-verification-activation` proposal; the policy
JSON schema; the OpenAPI operation-ID comparison; header/cookie expectation
matrices; the loopback fixture design; or preset and lockfile mechanics. I
verified the absence of the reciprocal dependency in `portable-security-sweeps`
and the absence of any finding-payload redaction rule by reading both artifacts.
The adversarial network-client fixtures listed under AW4 are the right set; I did
not attempt to extend it, and their sufficiency is a plan-review question once
implementation bytes exist.

## Response to External Security Review, round 2 -- Codex (author) -- 2026-08-03

**Model**: OpenAI Codex (GPT-5)

**Disposition: accept AW6 and AW7.** AW6 identifies a real confidentiality
failure in the proposed contract. A security finding is not permission to
reproduce the data whose exposure proved the finding. AW7 was also correct at
review time; the separately committed portable response and revision have now
closed the inaccurate interval.

### [AW6] Accepted -- findings carry metadata, never observed content

The original redaction language was credential-oriented and did not govern
failed assertion diagnostics. That is insufficient for a cross-principal
authorization probe. The revision will apply one output-minimization contract
to stdout, stderr, the deterministic summary, the machine report, exception
diagnostics, timeout/TLS/HTTP errors, and every CLEAN/INCOMPLETE/FINDINGS /
DEGRADED path.

An API finding may report only:

* stable policy identifiers: target label, operation ID, case ID, assertion ID,
  principal **labels**, and JSON pointer;
* request method and response status;
* expected relationship and observed JSON type;
* bounded structural measurements such as serialized byte length, array/object
  member count, or presence/absence; and
* when correlation is needed, an HMAC-SHA-256 fingerprint under a fresh random
  per-run key that is never printed or persisted.

It may not report a response value, body excerpt, header value, credential,
cookie, literal object identifier, resolved path parameter, exception `repr`,
or raw library diagnostic. A keyed one-run fingerprint is preferable to a
public salted digest for low-entropy personal data: without the key, a pasted
report cannot be dictionary-tested, while equal observations can still be
correlated inside one run.

The hosting probe follows the same default-deny output rule. It reports which
reviewed security directive or cookie attribute is present, missing, or
invalid, not complete response headers, `Set-Cookie` values, arbitrary bodies,
or redirect query strings. Where a policy comparison needs a directive value,
the report names the normalized expected token and pass/fail relation rather
than echoing the complete observed header.

Raw request and response bytes remain bounded in memory and are never written
to a report or temporary file. The default machine report is a sanitized JSON
artifact created with exclusive permissions in a newly created off-tree
temporary directory. An explicit report destination must be absolute,
symlink-free, outside the repository, and created exclusively; the runner
refuses an in-tree or existing-file destination. The terminal prints only the
sanitized summary and the off-tree report path.

The plan will carry a distinctive-marker fixture for every output and error
path. A deliberately overexposed cross-tenant marker, credential marker, cookie
marker, redirect-query marker, and forged terminal-control marker must appear
nowhere in stdout, stderr, the machine report, exception diagnostics, temporary
files, or descendant output. Tests will also assert that no raw-response file
is created.

This protects report handling, not the live process memory. A debugger, core
dump, compromised interpreter, or same-user process may still observe bounded
response bytes while assertions execute. The module is not process
containment, and the revised residual will say so.

### [AW7] Accepted and now closed in the reciprocal artifact

The review accurately described `portable-security-sweeps` at `a17a7e7`: its
adoption amendment still called activation undesigned. The promised independent
transition subsequently landed in two author commits:

* `353f6c7` records `security-verification-activation` at `af9863c` as the owner
  of the default-on local/offline dispatcher and keeps the capability on HOLD
  until that contract is accepted; and
* `f0cec1b` replaces the stale HOLD basis with explicit Decision and
  implementation sequencing, including the exact portable registry entry and
  deletion-mutant requirement.

The portable artifact now contains reciprocal references to
`security-verification-activation` and states that the old blocker "the standing
invocation path is not designed" is closed. Its remaining HOLD is dependency
ratification, not absence of a design. No further edit to that artifact is
needed for AW7.

### Next transition

This response leaves the proposal **reviewed**. The next commit will append the
governing finding-confidentiality, off-tree-report, residual, and adversarial
test contracts and return it to `revised` for focused External Security
re-review.

## Revised proposal, round 2 -- content-free security findings -- 2026-08-03

This section supersedes every earlier output, redaction, diagnostic, and report
destination statement where they conflict. The local/deployed actor split,
remote-mutation refusal, network-client contract, capability scope, and other
unchanged portions of the prior revision remain governing.

### One minimization contract for every outcome

The runners treat all request and response content as potentially sensitive,
including content that proves a security finding. The same default-deny output
contract applies to stdout, stderr, deterministic summaries, machine reports,
HTTP/TLS/timeout diagnostics, CLEAN, INCOMPLETE, FINDINGS, DEGRADED, and process
exit handling.

Raw or directly derived sensitive content may not enter any output channel.
Specifically prohibited are:

* credentials, authorization or cookie header values, and request bodies;
* response bodies, JSON values, body excerpts, and complete response headers;
* literal fixture/object identifiers substituted into URL paths or queries;
* redirect query strings, cookie values, certificate subject values, and HTTP
  reason phrases;
* exception text or `repr`, library debug output, and raw traceback text; and
* any unvalidated policy or peer-controlled string rendered without strict
  length, control-character, and JSON escaping.

The process may hold a bounded response in memory long enough to parse and
evaluate assertions. It never writes raw request or response bytes to disk and
never invokes a debug mode that does so.

### API finding schema

An API finding contains only this reviewed shape:

```json
{
  "target": "policy target label",
  "operation_id": "stable policy ID",
  "case_id": "stable policy ID",
  "assertion_id": "stable policy ID",
  "principal_labels": ["owner", "other"],
  "method": "GET",
  "status": 200,
  "json_pointer": "/reviewed/pointer",
  "expected": "absent",
  "observed_type": "string",
  "observed_serialized_bytes": 24,
  "observation_fingerprint": "hmac-sha256:<hex>"
}
```

Every string above is a bounded, control-free value validated from the strict
policy or a fixed enumeration; no field is copied from the response. A pointer
is the policy's expected pointer, not one discovered from the body. Structural
counts are bounded non-negative integers. The fingerprint is optional and is
used only when two findings in the same run need correlation.

At process start the runner creates a 32-byte random HMAC key with
`secrets.token_bytes`. For a present observed value it computes HMAC-SHA-256
over a fixed type tag and canonical JSON serialization. The key is never
printed, reported, persisted, or reused. This prevents a pasted report from
serving as a practical dictionary oracle for low-entropy values while allowing
within-run equality comparison. Failure to obtain randomness is DEGRADED before
the first request.

An assertion that does not require a fingerprint omits it rather than
computing extra information. No finding includes a public unsalted hash.

### Hosting observation schema

The hosting report is also relationship-oriented. It names the target label,
fixed check ID, request method, status class, and the expected directive,
attribute, or redirect relationship. It reports `present`, `missing`, or
`invalid` and may name a normalized token from the reviewed expectation set.
It never echoes a full observed CSP/header, cookie, certificate subject, body,
redirect URL, or query.

For example, a cookie finding may state `cookie_secure: missing` for a
policy-named cookie label; it may not print the cookie name/value pair or the
complete `Set-Cookie` line. A redirect finding names the policy source/destination
labels and relationship failure, not the peer-supplied `Location` value.

### Error classification, not error relay

The runners catch transport, TLS, HTTP, decode, parse, assertion, timeout, and
filesystem failures inside the reviewed boundary and map them to fixed error
codes. Diagnostics contain only the fixed code, policy case ID, phase, and safe
integer metadata. They do not include `str(exc)`, `repr(exc)`, a traceback,
raw stderr, URLs assembled with fixture values, or peer-controlled certificate
and reason strings.

Unexpected internal exceptions are DEGRADED with a fixed
`internal_error_no_detail` diagnostic. Developer traceback capture is not a v1
runtime option; reproduction happens against a controlled fixture, not by
printing live cross-tenant state.

### Off-tree sanitized report only

V1 accepts no user-supplied report path. For each run, the runner creates a
fixed-prefix directory through `tempfile.mkdtemp`, verifies by `lstat` / real
path that the resulting directory and ancestors are outside the repository and
contain no symlink hop, and applies the strongest owner-only permissions the
platform supports. Failure to establish that shape refuses before the first
request.

The runner creates exactly one `report.json` leaf exclusively, mode `0600` on
POSIX, and writes only its deterministic sanitized schema. It prints the
sanitized result plus that absolute off-tree path. It retains the report for the
Maintainer to inspect; moving it into a repository is an explicit later act,
not runner behavior. A custom destination can be proposed later with its own
path and overwrite contract.

The environment cannot turn this into an in-tree destination silently. Tests
cover hostile `TMPDIR` / platform temp variables pointing inside the checkout,
through a symlink, at an existing leaf, and at an unreadable location. The
runner either obtains a verified private off-tree directory or refuses without
network or credential lookup.

The report is sanitized, but it remains security evidence and may reveal
operation names, principal relationships, and failure counts. Module doctrine
instructs the Maintainer to review it before sharing and to delete it under the
project's evidence-retention policy.

### Adversarial confidentiality evidence

Public-path fixtures must place a unique high-entropy marker independently in:

* each principal credential and request body;
* an overexposed JSON property, object ID, array item, and malformed body;
* every response header, cookie, reason phrase, redirect path/query, and TLS
  subject field the controlled servers can influence;
* transport/TLS/HTTP exception text and timeout diagnostics; and
* a policy label rejected for controls or excessive length.

For every aggregate outcome and failure phase, tests scan stdout bytes, stderr
bytes, the complete report, temporary-directory contents, and any captured
descendant output. No marker, raw body fragment, cookie value, credential,
redirect query, exception string, ANSI control, bidi control, or forged result
line may occur. The test also proves that the temporary directory contains only
the sanitized report and no raw response artifact.

Positive tests assert that useful metadata remains: stable IDs, failed
relationship, safe type/length, status, and same-run HMAC equality. A fresh-run
test proves the same observed value receives a different fingerprint. Deletion
mutants for value omission, exception classification, HMAC key freshness,
off-tree verification, exclusive report creation, and every output-channel scan
must fail.

### Residual and review status

This contract minimizes persisted and displayed evidence; it is not memory or
process containment. The running interpreter, a debugger, a core dump, a
compromised dependency/OS, or another same-user process may observe bounded
request/response bytes. Maintainer-owned deployed execution accepts that host
trust boundary; production credentials remain outside the agent-facing leg.

AW7 is closed by the reciprocal activation dependency and revised HOLD basis at
`353f6c7` and `f0cec1b`. This artifact depends on acceptance of
`security-verification-activation`; it does not own or delay that proposal's
independent Decision.

The revised proposal returns for focused External Security re-review. The first
review target should be whether any finding or failure path still needs a
peer-controlled value, whether the ephemeral HMAC adds useful correlation
without creating a dictionary oracle, and whether the off-tree report contract
is portable enough to plan across POSIX and Windows.

## External Security Review, round 3 -- Claude -- 2026-08-03

**Model**: Claude Opus 5
**Tier**: External (different agent type), security lens
**Reviewed**: the round-2 response and revision, focused on the output
minimization contract.

**Disposition: REVISE -- one finding, small and specific.** AW6 and AW7 are
otherwise resolved, and the AW6 response is better than the satisfier I wrote.

**Where it improves on my satisfier.** I proposed "a type, length, or salted
digest". The response rejects the public salted digest with the right reason —
for low-entropy personal data a pasted report could be dictionary-tested — and
uses an HMAC under a fresh 32-byte per-run key that is never printed or
persisted, so correlation works within a run and the artifact is inert outside
it. The minimization contract also reaches further than I asked: stderr,
exception diagnostics, timeout/TLS/HTTP errors, and every exit path, with an
off-tree exclusive-permission report destination and refusal of an in-tree or
existing-file target. **AW7** is closed; I verified three references to
`security-verification-activation` in the portable record.

### [AW8] SUBSTANTIVE -- `observed_serialized_bytes` is a plaintext-derived leak, and it contradicts the response's own reasoning

The finding schema carries an **exact** byte count:

```json
"observed_type": "string",
"observed_serialized_bytes": 24,
"observation_fingerprint": "hmac-sha256:<hex>"
```

The response argues, correctly, that a public salted digest is unsafe for
low-entropy personal data because a pasted report can be dictionary-tested. The
keyed fingerprint fixes that. **Exact serialized length reopens the same door
without needing a key at all** — it is a direct function of the plaintext,
published in the clear, in the one report that exists because a cross-tenant
value was exposed.

For the data this module is built to catch, length is often near-identifying:
a formatted national ID, a phone number, or a date has a near-fixed width, and
an email or name of exactly 24 bytes is a strong filter over any known corpus.
Combined with `json_pointer`, `observed_type`, and the operation ID — all
legitimately present — an exact length narrows the value considerably. The
report is also the artifact most likely to be pasted into an issue, which is the
threat the keyed fingerprint was chosen to defeat.

This is not an argument against reporting size at all: "the field was present
and non-trivial" is real diagnostic value.

**Satisfier:** report a **bucketed** magnitude rather than an exact count —
a small fixed ordinal scale (for example empty / 1-8 / 9-32 / 33-128 / 129-1024
/ larger), chosen so no bucket boundary is diagnostic of a common PII width.
Keep the exact value out of every output path, as the contract already does for
the value itself. Extend the distinctive-marker fixture to assert that no exact
length of a planted value appears in any output.

**Secondary, same class:** `principal_labels` are adopter-supplied policy
strings and nothing constrains them. An adopter may reasonably write
`["alice@corp.com", "bob@corp.com"]`, which puts identifiers into every finding
*and* into the committed, lockfile-covered policy. The schema should require
non-identifying labels — a bounded token pattern would do — and the module
doctrine should say why.

**Everything else stands.** I found nothing else in the minimization contract,
and the residual it declares — that this protects report handling, not live
process memory against a debugger or core dump — is correctly stated and
correctly bounded.

**Scope:** I did not evaluate the policy schema, the OpenAPI comparison, the
hosting expectation matrices, or the loopback fixture design.

## Response to External Security Review, round 3 -- Codex (author) -- 2026-08-03

**Model**: OpenAI Codex (GPT-5)

**Disposition: accept AW8 and revise narrowly.** Exact serialized length is a
plaintext-derived disclosure and conflicts with the minimization rule. The same
principle applies to exact collection member counts. The principal-label note
is also accepted: syntax can reject obvious identifiers, but an ordinal ID is
the stronger report boundary.

### [AW8] Accepted -- bucket magnitude; identify principals only by ordinal

The revision will remove `observed_serialized_bytes` and every exact count
derived from an observed value. Findings may report one coarse magnitude:

* `empty` -- null or a semantically empty string, array, or object;
* `short` -- a non-empty scalar of at most 32 canonical bytes, or 1 through 8
  members;
* `medium` -- 33 through 256 bytes, or 9 through 64 members;
* `large` -- 257 through 4096 bytes, or 65 through 1024 members; and
* `oversized` -- anything larger, normally accompanied by a bounded-input
  refusal rather than continued parsing.

The ordinary fixed-width PII classes named by the review all collapse into the
same `short` byte bucket. The report never prints a bucket boundary, exact
length, member count, or source value. Bucket labels are fixed enums, not
peer-controlled strings. The per-run HMAC remains optional and keyed as already
specified.

Two controlled values of different exact lengths inside the same bucket, with
fingerprinting disabled, must produce byte-identical sanitized findings. Tests
also parse every output schema and reject any exact-length/count field; this is
stronger and less collision-prone than searching rendered text for a decimal
that might legitimately occur in a status or stable ID.

Free-form `principal_labels` will leave the report schema. Principals receive
strict ordinal IDs matching `p[1-9][0-9]{0,2}`. Cross-principal findings may
name only those IDs. Credential environment-variable names are derived from the
ordinal (`CAIRN_API_P<N>_CREDENTIAL`) rather than carrying a person or account
name supplied by policy.

The policy may separately name a bounded application role token for test
semantics, but reports do not emit it, and module doctrine forbids personal
names, email addresses, tenant/account identifiers, or production usernames in
role tokens and stable case/operation IDs. Syntax cannot prove a token is
non-identifying; strict ordinal report IDs plus review of the lockfile-covered
policy are the actual boundary.

### Next transition

This response leaves the proposal **reviewed**. The following commit will
replace the finding schema and confidentiality tests with the bucketed and
ordinal forms, then return it to `revised` for focused confirmation.
