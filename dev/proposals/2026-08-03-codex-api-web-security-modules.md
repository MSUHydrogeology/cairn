<!-- claim-check-allow: templates/modules/default-on/security-verification.md, templates/modules/default-on/run_security_verification.py, templates/modules/team-gated/api-access-security.md, templates/modules/team-gated/api_access_security.py, templates/modules/team-gated/api_access_policy_stub.json, templates/modules/team-gated/web-hosting-security.md, templates/modules/team-gated/web_hosting_security.py, templates/modules/team-gated/web_hosting_policy_stub.json, dev/modules/security-verification.md, dev/modules/api-access-security.md, dev/modules/web-hosting-security.md, scripts/run_security_verification.py, scripts/api_access_security.py, scripts/web_hosting_security.py, dev/.cairn/api-access-policy.json, dev/.cairn/web-hosting-policy.json, bootstrap/tests/test_security_verification.py, bootstrap/tests/test_api_access_security.py, bootstrap/tests/test_web_hosting_security.py -->

# API access and web-hosting security modules

**Author**: Codex (Strategy, from the Security Review role)
**Model**: OpenAI Codex (GPT-5)
**Date opened**: 2026-08-03
**Status**: proposed
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
