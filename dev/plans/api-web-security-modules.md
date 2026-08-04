<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/dual-review.md doctrine/lifecycle.md doctrine/coordination.md doctrine/rationale.md doctrine/runtime-contract.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: templates/modules/team-gated/api-access-security.md, templates/modules/team-gated/api_access_security.py, templates/modules/team-gated/api_access_policy_stub.json, templates/modules/team-gated/web-hosting-security.md, templates/modules/team-gated/web_hosting_security.py, templates/modules/team-gated/web_hosting_policy_stub.json, templates/modules/team-gated/_security_net/__init__.py, templates/modules/team-gated/_security_net/policy.py, templates/modules/team-gated/_security_net/net.py, templates/modules/team-gated/_security_net/report.py, templates/modules/default-on/security-verification.md, templates/modules/default-on/run_security_verification.py, dev/modules/api-access-security.md, dev/modules/web-hosting-security.md, dev/modules/security-verification.md, scripts/api_access_security.py, scripts/web_hosting_security.py, scripts/run_security_verification.py, scripts/_api_access_security/net.py, scripts/_web_hosting_security/net.py, dev/.cairn/api-access-policy.json, dev/.cairn/web-hosting-policy.json, bootstrap/tests/test_security_net.py, bootstrap/tests/test_api_access_security.py, bootstrap/tests/test_web_hosting_security.py, bootstrap/tests/test_security_capability_install.py, bootstrap/tests/test_security_finding_confidentiality.py, bootstrap/tests/test_security_verification.py -->
<!-- link-check-allow: ../../bootstrap/tests/test_security_net.py, ../../bootstrap/tests/test_api_access_security.py, ../../bootstrap/tests/test_web_hosting_security.py, ../../bootstrap/tests/test_security_capability_install.py, ../../bootstrap/tests/test_security_finding_confidentiality.py -->

# Plan: two selectable network-security capabilities, and the evidence that their clients are safe

**Source proposal**: `api-web-security-modules` — accepted 2026-08-03 by
Maintainer Decision at `156305f`, *"ACCEPTED as revised"*. It currently sits
under `dev/proposals/` and moves to `dev/proposals/archive/` when it archives.
**Status**: open
**Plan review**: required(**External** + **External Security Review**) — carried
verbatim from the proposal header, where the tier is a *declared trigger*, not a
judgement call. **No implementation commit lands before a review section is in
the tree.** See `## Plan review — the brief` for why an Internal round cannot
discharge it.
**Last update**: 2026-08-04
**Opened**: 2026-08-04 (one day after the Decision commit; the dependency
Decision on `security-verification-activation` landed first, at `4dfcf19`)

## Source proposal

`api-web-security-modules` settles one contract: **an adopter may select either
of two narrow security capabilities, each of which produces re-runnable evidence
about a boundary Cairn's existing modules do not reach — cross-principal API
authorization, and deployed-site HTTP/TLS posture — where the agent-facing leg
can reach only a loopback fixture, the deployed leg is a separate
Maintainer-invoked passive command, and no output channel may carry observed
content.** The plan executes that decision and does not re-litigate it.

The artifact took four External Security rounds (AW1–AW8). Every finding closed
by *removing an authority or a field*, not by adding a caveat: `--allow-mutation`
was deleted rather than constrained; `deployed` left the dispatcher; a public
salted digest became an ephemeral keyed HMAC; an exact byte count became a
five-value bucket; adopter-supplied `principal_labels` became ordinal
`principal_ids`. The Decision records those three properties as the ones the
acceptance rests on, and routes the **AW4 adversarial network-client fixtures**
here as a blocking gate this plan must clear.

### What the Decision governs, and where earlier proposal text is superseded

The Decision accepts the proposal **"as revised through round 3."** Three places
where the header or the original body disagrees with a later revision, and the
revision wins:

1. **`templates/core/AGENTS.md` is not touched by this plan.** The header's
   *Touches* line names it, and the original §1 gave it a merge slot. The round-1
   revision moved the default-on module, the standing command, and the
   `AGENTS.md` slot to `security-verification-activation` and states plainly that
   this proposal "does not modify `templates/core/AGENTS.md`". Throughout this
   plan, `templates/core/AGENTS.md` means the **shipped adopter template** — the
   file the scaffold installs into an adopter's repository as their `AGENTS.md`.
   Cairn's own root `AGENTS.md` is a different file, is a serialized shared
   surface, and is likewise untouched. Where a row below has to say which, it
   says which.
2. **No default-on module, no preset membership.** Both capabilities are
   team-gated and reachable only through an explicit `modules_add` or an exact
   `modules:` list. The proposal rejects preset membership in terms
   (applicability is not derivable from Cairn's six axes), so `_PRESETS` and
   `_DEFAULT_ON_MODULES` are untouched — an assertion this plan verifies rather
   than an aside.
3. **The finding schema is the round-3 one.** `principal_ids` ordinals,
   `observed_magnitude` enum, optional keyed `observation_fingerprint`, and **no**
   exact byte length, character length, member count, or index count anywhere in
   any output schema.

### Glossary — every term glossed on first use

The audience is a scientist who codes. This scope is the most jargon-dense in
the `dev/` tree, and several of the terms name the exact thing that goes wrong.

* **Loopback** — the network address a machine uses to talk to itself
  (`127.0.0.1`, `::1`). A loopback-only client cannot leave the host, which is
  the property the agent-facing leg rests on.
* **SSRF** (server-side request forgery) — persuading a program that makes HTTP
  requests to make one *you* chose, typically to an address it should not reach
  (a cloud metadata endpoint, an internal admin service).
* **DNS rebinding** — a hostname whose DNS answer is a public address when the
  program *checks* it and a private address when the program *connects*. The
  defence is to validate the address you actually connected to (the **connected
  peer address**), not the one you resolved. This is the single hardest property
  in the plan and the reason Chunk A exists.
* **BOLA** (broken object-level authorization) — principal B reads principal A's
  object because the endpoint checked authentication and not ownership. The
  API module's whole purpose is to make a project *state* the intended denial
  and then execute it.
* **Cross-principal / ownership swap** — the same object requested twice, once
  with the owner's credential (expect allow) and once with a second principal's
  (expect deny). One half alone proves nothing.
* **HSTS / CSP / `frame-ancestors` / `X-Content-Type-Options` /
  `Referrer-Policy` / `Permissions-Policy`** — response headers a browser
  enforces. `HSTS` forces HTTPS on later visits; `CSP` restricts what a page may
  load and `frame-ancestors` who may frame it; the rest narrow sniffing,
  referrer leakage, and feature access.
* **Passive check** — a request that only reads (`GET` / `HEAD`), sends no attack
  payload, and follows no crawl. The opposite is an **active scan**, which is out
  of scope in v1 and named as such.
* **HMAC-SHA-256 under an ephemeral key** — a keyed fingerprint. Two equal
  observations fingerprint equally *within one run*; without the key (which is
  never printed, persisted, or reused) a pasted report cannot be dictionary-
  tested back to the value. This is why it replaced a salted digest.
* **Magnitude bucket** — `empty` / `short` / `medium` / `large` / `oversized`.
  A five-value enum standing in for a size, chosen so that formatted national
  IDs, phone numbers, dates, ordinary names and most email addresses all collapse
  into `short` and therefore carry no width signal.
* **Off-tree report** — the sanitized `report.json`, written into a freshly
  created private temporary directory verified to be outside the repository, so
  security evidence cannot land in a commit by accident.
* **The dispatcher** — `scripts/run_security_verification.py`, owned by
  `security-verification-activation`. It is the standing agent-facing command;
  it may invoke only a capability's `local` subcommand, through a **fixed
  registry** of module → exact argv that lives in the dispatcher's own source.
* **Mapping group** — the set of files one module installs
  (`InstallSpec` rows in `_MODULE_MAPPINGS`). The activation contract requires a
  *complete* group — doctrine, runner, policy — before a registry entry is
  admitted.
* **AST attestation baseline** —
  `bootstrap/tests/fixtures/scaffold_ast_baseline.json`, a per-symbol structural
  digest of the scaffold engine package. `verify` reports CHANGED / MISSING /
  DUPLICATE against it; re-pinning is a supervised ceremony, never an
  implementing agent's step.
* **Perturbation** — a deliberate change to repository or fixture state that a
  test is claimed to detect. This repository accepts a test only when its author
  can name a state in which it fails **and has run** the change producing that
  state. Two flavours are used below and are **not** interchangeable: a
  **deletion mutant** removes the guard and proves the *test* discriminates; a
  **hazard perturbation** changes the world the guard is claimed to protect
  against and proves the *claim*. A test with only a deletion mutant has been
  validated; only a hazard perturbation validates the security property.

## Proposed paths

Every path below is a forward reference: nothing here exists on disk at
plan-open. Cairn itself selects neither capability, so the `scripts/`,
`dev/modules/` and `dev/.cairn/` entries are **adopter-tree destinations only**
and will never resolve in this repository.

Proposed paths:
- `templates/modules/team-gated/api-access-security.md` — API module doctrine; Chunk E.
- `templates/modules/team-gated/api_access_security.py` — API runner facade (`local` / `deployed-passive`); Chunk B.
- `templates/modules/team-gated/api_access_policy_stub.json` — strict, `configured: false` API policy stub; Chunk E.
- `templates/modules/team-gated/web-hosting-security.md` — hosting module doctrine; Chunk E.
- `templates/modules/team-gated/web_hosting_security.py` — hosting runner facade; Chunk C.
- `templates/modules/team-gated/web_hosting_policy_stub.json` — strict, `configured: false` hosting policy stub; Chunk E.
- `templates/modules/team-gated/_security_net/__init__.py` — shared engine package marker + version constant; Chunk A.
- `templates/modules/team-gated/_security_net/policy.py` — strict policy schema, ordinal principals, derived credential env names; Chunk A.
- `templates/modules/team-gated/_security_net/net.py` — URL normalization, address classification, resolve-connect-verify-peer, redirect policy, caps, TLS; Chunk A.
- `templates/modules/team-gated/_security_net/report.py` — sanitized schemas, magnitude buckets, ephemeral HMAC, off-tree report, fixed error codes; Chunk A.
- `bootstrap/tests/test_security_net.py` — the transport/addressing adversarial socket suite; Chunk A.
- `bootstrap/tests/test_api_access_security.py` — API public-path, actor-boundary, authorization-matrix tests; Chunk B.
- `bootstrap/tests/test_web_hosting_security.py` — hosting public-path HTTP/TLS tests; Chunk C.
- `bootstrap/tests/test_security_finding_confidentiality.py` — the cross-runner marker sweep over every channel and exit path; Chunk D.
- `bootstrap/tests/test_security_capability_install.py` — selection, mapping-group completeness, manifest/lockfile accounting, summary and install output; Chunk F.
- `scripts/api_access_security.py` — adopter-tree destination of the API facade.
- `scripts/web_hosting_security.py` — adopter-tree destination of the hosting facade.
- `scripts/_api_access_security/net.py` — adopter-tree destination of the shared engine, API copy (with its three siblings).
- `scripts/_web_hosting_security/net.py` — adopter-tree destination of the shared engine, hosting copy (with its three siblings).
- `dev/modules/api-access-security.md` — adopter-tree destination of the API doctrine.
- `dev/modules/web-hosting-security.md` — adopter-tree destination of the hosting doctrine.
- `dev/.cairn/api-access-policy.json` — adopter-owned API policy, generated from the stub.
- `dev/.cairn/web-hosting-policy.json` — adopter-owned hosting policy, generated from the stub.
- `scripts/run_security_verification.py` — the dispatcher; owned by `security-verification-activation`, cited here for the registry entry only.
- `templates/modules/default-on/run_security_verification.py` — the dispatcher template; likewise owned there.

## Scope

Executes the accepted contract across eight chunks. Two of them
(**A** and **D**) are where the risk actually is: everything else is
registration and prose around **two HTTPS clients written from scratch under the
standard-library-only constraint**, which is what External finding AW4 named and
what the Decision routed here as a blocking gate.

Exactly **one** chunk (**F**) touches `bootstrap/_scaffold/`. That is deliberate
and is the plan's main concession to the five-scope cluster contending for that
package; see *The engine surface this plan shares*.

**Out of scope, fenced explicitly** — carried from the proposal's
*Deliberately not touched* line, its v1 boundaries, and the residuals its four
review rounds established:

* **Application authorization implementation.** The modules require a project to
  *state* its intended allow/deny facts and then execute them. They do not
  implement, generate, or infer an authorization model. OPA, Cedar and OpenFGA
  remain architectural choices the project owns; their policy-unit tests are
  named as required companion evidence in module doctrine and are **not**
  installed or invoked.
* **Cloud accounts and provider posture.** No AWS/Azure/GCP/hosting-provider
  credential is requested, discovered, or accepted. The proposal walls this off
  as a future `cloud-hosting-security` proposal with its own least-privilege,
  allowlisting, egress, retention and cost review. Nothing in this plan reserves
  an extension point for it.
* **Production penetration testing and active scanning.** No crawl, no payload,
  no fuzzing, no ID inference, no ZAP/Nuclei adapter. `deployed-passive` sends
  only declared `GET` and `HEAD`.
* **Credential provisioning.** The runners read values from environment
  variables whose **names** are derived from ordinals; they never create, store,
  rotate, print, or persist a credential, and no step of this plan asks anyone to
  paste one. See *The Maintainer fence*.
* **WAF / CDN configuration.** Origin exposure behind a CDN is a named residual
  of the hosting module, not a check.
* **The `python-security` and `content-security` detection contracts.**
  Untouched. No finding class, allowlist, exit code, or scan root of either moves.
  This plan adds modules beside them; it does not edit them.
* **Remote mutation, in any form.** There is no `--allow-mutation`, no policy
  field that enables a non-loopback write, and no hidden extension point for one.
  A future staging-mutation capability returns through its own proposal.
* **YAML OpenAPI and GraphQL inventory.** Deferred by the proposal until a parser
  and query contract exist that do not weaken the standard-library boundary. v1
  compares operation IDs against a committed OpenAPI **JSON** document only.
* **`testssl.sh`, MDN HTTP Observatory's API, Trivy.** Documented extensions;
  none enters the v1 fixed registry. Trivy stays with `portable-security-sweeps`.
* **The activation dispatcher itself.** `run_security_verification.py`, the
  aggregate exit precedence, the `AGENTS.md` slot in the **shipped adopter
  template**, and the default-on install are owned by
  `security-verification-activation`. This plan adds two registry entries to a
  dispatcher that artifact builds (Chunk G) and changes none of its logic.
* **Cairn self-hosting either capability.** Cairn has no API and hosts no site;
  it will not select these modules, will not carry
  `scripts/api_access_security.py`, and will not create a
  `dev/.cairn/*-policy.json`. Consequence, checked rather than assumed: the two
  runners acquire **no self-hosted twin**, so
  `test_every_self_hosted_twin_stays_byte_identical_to_its_source` in
  [`bootstrap/tests/test_notice_install.py`](../../bootstrap/tests/test_notice_install.py)
  gains no pair.

### Documentation / doctrine surface

* **Governing layer, Cairn's own `AGENTS.md` — none.** Cairn's root `AGENTS.md`
  is a serialized shared file and is untouched. Its *High-risk surfaces* list
  already covers the scaffold/merge engine and the install contract, which is
  what Chunk F moves; no new Cairn-side rule is created.
* **Governing layer, the shipped adopter template — none.**
  `templates/core/AGENTS.md` is untouched, per the round-1 revision. **Where this
  reading could be wrong, stated so the Maintainer can strike it in one line:**
  the activation artifact says its `AGENTS.md` slot registers "every registry
  entry" as a Security-Review surface. If the landed activation implementation
  wrote a *literal enumeration* rather than that general clause, then admitting
  two registry entries requires two rows in the adopter template after all. Chunk
  G row **G3** is that row, written conditional on inspection, and it is the one
  to strike if the general clause landed. This is checked at implementation, not
  predicted here.
* **Descriptive / governing files that describe the software as it is** —
  `bootstrap/SAFETY.md` (a new rule; Chunk H) and
  `bootstrap/DEPENDENCY_BUDGET.md` (a no-new-exception statement; Chunk H). Both
  describe behaviour this plan changes: SAFETY's Rule 5 currently says "the
  bootstrap does not read from the internet", which stays true of the scaffold
  and becomes materially incomplete once Cairn *ships* a network client.
* **Module doctrine — new, and the durable home for most residuals.**
  `templates/modules/team-gated/api-access-security.md` and
  `…/web-hosting-security.md` carry each capability's threat model, schema,
  evidence interpretation, trigger, omissions, actor rules, and recovery
  procedure. Deliberation-layer content does **not** go there; see
  *Lasting-truth migration*.
* **Release-facing** — one `CHANGELOG.md > Unreleased > Added` line. `CHANGELOG.md`
  is a serialized shared file: the row lands at the defined serialization point
  (the final chunk's commit or the goodnight routine), never opportunistically
  mid-sequence.
* **Deliberation layer** — this plan, its plan review, its code review, and the
  one-line `dev/PLANNING.md` row-move that serializes the plan-open.

<!-- cairn:slot documentation-tier-home -->
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
plan's *Scope* must name the doctrine-surface touched (or an explicit
"no doctrine surface").
<!-- cairn:end documentation-tier-home -->

## The engine surface this plan shares — declared symbol delta, one ceremony

**Five accepted scopes edit `bootstrap/_scaffold/`:** `profile-parse-fail-open`
(in implementation now), `default-security-stance`, this scope,
`portable-security-sweeps`, and `security-verification-activation`. Four are
being planned in parallel with this one.

That is not ordinary file overlap. `bootstrap/_scaffold/` is covered by an AST
attestation baseline whose re-anchor ceremony pins a **falsifiable union of
CHANGED symbols agreed in advance**. The property the ceremony exists to provide
is *"any symbol outside the union is a stop-and-explain."* A concurrent engine
change from a scope that did not declare its symbols does not enlarge the union
— it **destroys that property**, because the discriminator stops discriminating.
So this plan declares its own delta, and states what it measured rather than
quoting a figure written earlier.

### Measured baseline, `as_of 2026-08-04`

Read from `bootstrap/tests/fixtures/scaffold_ast_baseline.json` at HEAD
`eacb7dd` under the canonical interpreter (`~/conda_envs/lhm/bin/python3.13`):

```
total baselined entries      174
  FunctionDef  98
  Assign       53
  ClassDef     10
  Import        8
  Docstring/Expr/If/If#2/Try  5
FunctionDef + Assign + ClassDef = 161
```

Both figures match the ones this plan was briefed with, so the brief's numbers
are confirmed rather than assumed. Re-measure at implementation: the four
sibling scopes may have landed by then.

### This plan's declared delta

**CHANGED (present in the baseline; digest will move):**

| # | Symbol | File | Why |
|---|--------|------|-----|
| Δ1 | `Assign:_MODULE_MAPPINGS` | `bootstrap/_scaffold/config.py` | Two new module keys, each a complete `InstallSpec` group. |
| Δ2 | `Assign:_LIVING_STATE_DSTS` | `bootstrap/_scaffold/lockfile.py` | The two adopter-filled policy destinations. **Contingent** — see *Contract question 1*. |
| Δ3 | `FunctionDef:main` | `bootstrap/_scaffold/cli.py` | Two one-line call sites: the `--summary` path and the post-install path emit the capability notice. |

**NEW (absent from the baseline; must be added to the pinned
`bootstrap/tests/fixtures/scaffold_ast_known_new.json`):**

| # | Symbol | File | Why |
|---|--------|------|-----|
| Δ4 | `Assign:_CAPABILITY_NOTICE_MODULES` | `bootstrap/_scaffold/install.py` | The module → notice-line data the two call sites render. |
| Δ5 | `FunctionDef:capability_install_notice_lines` | `bootstrap/_scaffold/install.py` | Pure renderer; no I/O, no policy read. |

**Declared NOT changed**, so the union can discriminate — each verified present
in the baseline `as_of 2026-08-04`: `Assign:_CORE_MAPPINGS`,
`Assign:_SKILLS_MAPPINGS`, `Assign:_DEFAULT_ON_MODULES`, `Assign:_PRESETS`,
`Assign:_AXES`, `Assign:_TEAM_STAFFING_GATES`, `Assign:_TEAM_STAFFING_GATED`,
`Assign:_MODULE_SUPERSEDES`, `Assign:_GITIGNORE_SEEDS`,
`Assign:_REFERENCE_SCRIPT_TOKEN`, `Assign:_OPTIONAL_TEMPLATES`,
`ClassDef:InstallSpec`, `FunctionDef:install_manifest`,
`FunctionDef:write_install_lockfile`, `FunctionDef:expand_preset`,
`FunctionDef:_canonical_order`, `FunctionDef:_can_staff_module`,
`FunctionDef:format_profile_summary`, `FunctionDef:reference_script_token_defaults`,
`FunctionDef:read_lockfile`, `FunctionDef:classify_verbatim`,
`FunctionDef:build_arg_parser`.

Two of those deserve their reason recorded, because each is a design choice made
*to shrink this delta* and a reviewer should be able to strike it:

* **`format_profile_summary` is deliberately not touched.**
  `bootstrap/_scaffold/config.py` is `cascade_mutable` in the gate manifest,
  governed by *"one predeclared mapping-symbol delta only"*. Adding a summary
  line inside `format_profile_summary` would put a second, non-mapping symbol
  change into that file and break its governance. The `--summary` requirement is
  met instead by `cli.main` appending the notice **after** it prints
  `format_profile_summary(cfg)` — same visible output, one governed file
  untouched.
* **`FunctionDef:install_modules` is deliberately not touched**, even though it
  warns-and-continues on a missing module source (a partial mapping group
  installs silently — a fail-open for a security capability). Closing that in the
  engine is a change to a shared install path four other scopes are editing.
  Completeness is enforced instead from two ends that need no engine byte:
  a Cairn-side test that every source in both mapping groups exists under
  `templates/` (Chunk F), and the shipped runner's own import self-check, which
  exits **20 / DEGRADED** if an engine member is absent (Chunk A). Named as a
  known omission rather than smuggled.

### Contingency, stated because a delta that quietly changes is worthless

Δ2 is contingent on *Contract question 1* resolving to **living-state**. If the
Maintainer or the plan review picks the alternative, Δ2 **drops** and is replaced
by whatever the alternative needs. **A change to this delta is re-declared to the
Maintainer before the ceremony, not absorbed silently** — that is the whole point
of declaring it.

### One ceremony, and the fence around it

* **This scope shares a single re-anchor ceremony with the rest of the cluster.**
  The union is formed **by the Maintainer at ceremony time** from each scope's
  declared delta. This plan supplies its five rows and asserts nothing about the
  other four scopes' rows.
* **The surgical path is unavailable to the cluster, and this is measured rather
  than assumed.** `update_symbol` in `bootstrap/tests/_ast_attest.py` refuses
  unless the target is the **only** CHANGED symbol with no MISSING/DUPLICATE
  drift, its `_UPDATE_ALLOWLIST` is `{_MODULE_MAPPINGS, _SKILLS_MAPPINGS,
  _CORE_MAPPINGS, install_onboarding}`, and every NEW top-level symbol matches the
  pinned `known_new` manifest by **complete-set equality**. Δ1 alone would qualify.
  Δ1 + Δ2 + Δ3 do not, and Δ4/Δ5 additionally require the frozen `known_new`
  fixture to move. So the cluster needs **one full supervised re-anchor**, not
  four surgical updates — and if three scopes each add module rows, they cannot
  each surgically bless `_MODULE_MAPPINGS` in turn regardless of order.
* **The re-anchor is a Maintainer act. An implementing agent never performs it.**
  See *The Maintainer fence*.

### What is true regardless of intra-cluster order

* Δ1–Δ5 are the symbols this scope moves, whether it lands first or last.
* Chunks **A–E** touch no `bootstrap/_scaffold/` file at all. Only **F** does.
  Order within the cluster therefore constrains one commit of this plan, not
  eight.
* This plan asserts no baseline digest value. It names symbols; digests are read
  at ceremony time.

### What is order-sensitive, named

* **`bootstrap/tests/test_notice_install.py` pins `44`** template `.py` manifest
  sources, and that file is **frozen** in the gate manifest. Three cluster scopes
  add template `.py` files. **Whoever lands second re-measures; nobody applies a
  number from their own plan.** Note the counting rule, which is easy to get
  wrong: `_manifest_py_sources()` returns a **list**, not a set, so a template
  source installed to two destinations counts **twice**.
* **`dev/plans/scan-coverage.md` Chunk C4** introduces a second `44` pin, in
  `bootstrap/tests/test_security_lint.py`, over `.py` files physically on disk
  under `templates/`. Its own text says the two pins must move in the same commit.
  If `scan-coverage` has landed, this plan moves both; if it has not, this plan
  moves one and `scan-coverage` inherits the new number. Either way: re-measure.
* **The published install manifest emits 95 data rows** (`96` lines including the
  header comment), `as_of 2026-08-04`. Every scope adding module files moves it.
* **`gate_manifest.json > mapping_symbols._MODULE_MAPPINGS.baseline_digest`**
  moves for the same reason, and `cascade_mutable` records a `pre_run_sha256` for
  `bootstrap/_scaffold/config.py`. Both are Maintainer-facing consequences to
  report, never to re-pin.
* **Chunk G cannot land before `security-verification-activation`'s dispatcher
  exists.** That is the one hard inter-scope ordering edge, and it is
  one-directional: activation is harmless without the capabilities, the reverse
  is not. If activation has not landed when Chunks A–F are ready, A–F still land
  and G waits; the capabilities are then directly invocable but not standing
  checks, and the module doctrine must say so rather than claim otherwise.

## Two contract questions the proposal underdetermines

Both are load-bearing, neither is settled by the Decision, and each is written
so the Maintainer or the plan reviewer can strike the default in one line. They
are the first two questions in the plan-review brief.

### Contract question 1 — how a *filled* policy stays integrity-covered

The proposal states the property twice: the committed policy is
"lockfile-covered, so a candidate change cannot redirect the standing check to a
different host without first producing a visible integrity failure", and the
activation dispatcher "opens the runner and policy as regular non-symlink files,
computes their SHA-256 values itself, and compares them with the lockfile."

Read against the machinery, the two halves of that cannot both hold, and this
was verified by reading the code rather than inferred:

* `bootstrap/verify_integrity.py` compares each recorded destination's on-disk
  sha256 against the lockfile and reports `modified (hash mismatch)` on any
  difference, **unless** the destination is in `_LIVING_STATE_DSTS` in
  `bootstrap/_scaffold/lockfile.py`, in which case it is skipped entirely. The
  `living_state` flag is honoured only for that authoritative set; a record
  outside it that claims the flag is treated as tamper.
* The module *requires* the adopter to fill the stub — an unfilled
  `configured: false` policy is INCOMPLETE by design. So the correct-use state is
  exactly the state that differs from the recorded install.
* Therefore: **not** living-state ⇒ every correctly-configured adopter runs a
  permanently red `verify_integrity`. Living-state ⇒ the lockfile hash for the
  policy is stale by construction, so a dispatcher digest comparison against it
  can never pass on a filled policy.

**Default this plan implements, and why it is not a weakening.**

1. The **runner and its engine members are verbatim, hash-pinned, and not
   living-state.** They are the executable; the dispatcher's parent-computed
   digest binding applies to them unchanged. Nothing about the accepted
   activation contract moves.
2. The **policy files are living-state.** Their integrity property is delivered
   by three controls the proposal already accepted, not by a lockfile digest:
   * the **strict schema** — unknown keys, duplicate IDs, unsupported methods,
     invalid URLs, control characters, embedded credentials and secret-shaped
     literals are refused before anything else happens;
   * the **loopback-only local leg** — a silently redirected `local` policy
     cannot leave the host under *any* policy content, which is the case that
     mattered, since `local` is the only leg an agent can reach; and
   * **`--authorize-base-url`** — the deployed leg refuses unless the operator
     restates the exact normalized base URL at invocation. This is AW1's own
     satisfier, and it already makes a silent policy host-change ineffective:
     the redirected host cannot match a URL the Maintainer typed.
   * plus the ordinary one: the policy is a **tracked file**, so a candidate
     change to it appears in the diff a reviewer reads.
3. Module doctrine states the residual in terms: *a filled policy's bytes are
   not lockfile-attested; its review channel is git, and the deployed leg's
   authority comes from the invocation argument, not the file.*

**The alternative, if the default is struck.** Keep the policy non-living-state
and add an explicit re-record step (an `upgrade`-side rehash for adopter-filled
policy files, analogous to the existing `verbatim_rehash`). That is **new engine
mechanism**, it enlarges this plan's symbol delta into `bootstrap/_scaffold/`
paths four other scopes are editing, and — since the re-record command would be
run by whoever edited the policy — it re-establishes the digest without
establishing review. It is a legitimate choice; it is not this plan's default,
and it would need its own proposal.

### Contract question 2 — how two capabilities share one hardened client

The proposal's path list gives each capability exactly one `.py` runner and says
"the scripts share parsing and transport hardening." It does not say where the
shared code lives. Duplicating a hardened HTTPS client across two files is the
worst available answer for a security surface, so this is a plan decision.

**Measured constraint** — `install_manifest` refuses duplicate *destinations*
and only destinations. Verified against the real function `as_of 2026-08-04`:

```
one source → two destinations: {}                       (accepted)
two sources → one destination:  {'p/x.py': [...]}       (refused, ValueError)
```

**Default this plan implements.** One template source tree — a shared
`_security_net` package under `templates/modules/team-gated/`, four files —
listed in *both* modules' `InstallSpec` groups with **different destinations**:
an `_api_access_security/` engine directory under `scripts/` for the API module
and a `_web_hosting_security/` one for the hosting module. Single source, single
review, no engine mechanism, no module-dependency concept Cairn does not have,
and no duplicate-destination refusal. `scripts/<name>.py` + `scripts/_<name>/` is
also the established facade↔engine convention `_facade_engine_dir` already
recognises, so an adopter who forks a facade gets the existing advisory.

**Costs, named rather than discovered.** An adopter selecting both capabilities
carries two byte-identical copies of the engine. Manifest rows grow by 8 for the
engine alone. `test_notice_install.py`'s `.py` source count grows by 10 (4 × 2
destinations + 2 facades) from this scope, since it counts rows and not distinct
files. And the two copies can drift only if someone edits an installed tree by
hand — which `verify_integrity` catches, because engine members are **not**
living-state.

**The alternative, if struck.** Ship each runner self-contained. It removes the
duplication mechanism and doubles the security-critical bytes under review. Not
recommended, but a reviewer may prefer it; if so, Chunk A's file table collapses
into Chunks B and C and the delta is unchanged.

## Gate accounting

Each figure is a dated snapshot measured for this plan at HEAD `eacb7dd` under
the canonical interpreter, to be **re-taken at implementation** rather than
quoted from here. The working tree was dirty at measurement time — four sibling
workflows had uncommitted changes under `bootstrap/` — so every count below is a
lower-confidence snapshot than usual and is marked as such.

* **Suite collection: 1746 tests collected**, `as_of 2026-08-04`, via
  `python -m pytest bootstrap/tests --collect-only -q`. Collected, not run —
  a full run was not performed for this plan because the tree carried another
  workflow's in-flight edits and the resulting figure would attribute their state
  to this plan. **The implementing agent takes a clean baseline before Chunk A.**
  Collection may only grow; a dropped node or a new skip/xfail marker is a HOLD
  class.
* **Published install manifest: 95 data rows** (96 lines with the header),
  `as_of 2026-08-04`. Expected after Chunk F: **95 + 14 = 109** from this scope
  alone (2 doctrine + 2 policy stubs + 2 facades + 8 engine copies). Assert the
  delta, re-measure the total.
* **AST baseline: 174 entries, 161 of `FunctionDef`/`Assign`/`ClassDef`**,
  `as_of 2026-08-04`. See the delta table above.
* **Frozen-file accounting.** Two files this plan modifies are literal keys in
  the 164-entry `frozen_files` map, `as_of 2026-08-04`:
  `bootstrap/tests/fixtures/scaffold_ast_known_new.json` (Δ4/Δ5) and
  `bootstrap/tests/test_notice_install.py` (the `44` pin). Five new test files
  are created, so `FROZEN-NEW` rows appear as well. `bootstrap/_scaffold/config.py`,
  `cli.py`, `lockfile.py` and `install.py` are **not** frozen; `config.py` is
  `cascade_mutable` under *"one predeclared mapping-symbol delta only"*, which
  Δ1 satisfies exactly and which is why nothing else in that file moves.
* **The frozen map does not gate the suite** — `bootstrap/tests/test_gate_manifest.py`
  verifies against a manifest produced from the live tree at test time; the
  committed fixture is read only by the batch tooling when an operator runs it.
  So `python -m pytest bootstrap/tests` stays green across these edits, and the
  implementing agent's obligation is to **report** the stale entries in the final
  commit body, never to re-pin them.
* **Bandit release-scan reach.** Ten new template `.py` **rows** (six distinct
  new source files) enter `install_manifest`, and therefore enter
  `bootstrap/security_check.py`'s scan set — *if* `scan-coverage` has landed its
  manifest union. If it has not, these files ship unscanned, which is exactly the
  defect `scan-coverage` exists to close. **Measure the blocking-finding count
  over the new files before Chunk F lands**; a MEDIUM+ finding in a security
  client is a stop, not an allowlist entry.
* **Doc gates.** `python scripts/check_cairn.py` and
  `python scripts/quality_gate.py --sub neutrality` figures are deliberately
  **not** quoted here: `bootstrap/*.md` is inside the neutrality scan roots and
  four sibling scopes are editing Markdown concurrently, so any number written
  today would be stale on arrival. Capture both before Chunk H and assert
  *unchanged*, not a value.

## The Maintainer fence

Three classes of act in or around this plan are **not** an implementing agent's
to perform. Each is fenced here rather than left to be discovered at the moment
it is convenient to cross.

1. **The AST re-anchor ceremony.** Re-pinning
   `bootstrap/tests/fixtures/scaffold_ast_baseline.json` and
   `bootstrap/tests/fixtures/scaffold_ast_known_new.json`, and re-pinning
   `bootstrap/tests/fixtures/gate_manifest.json`, are supervised acts under
   `bootstrap/REANCHOR_RUNBOOK.md` — signing keys, a clean child shell, recorded
   absolute utility paths, an authorization ref. The implementing agent's entire
   obligation is to (a) declare the delta above, (b) report in the final commit
   body which frozen and cascade-governed entries are now stale, naming them, and
   (c) stop. **No implementing agent runs `update_symbol`, `_gate_manifest.py`
   re-pin, or `_gate_reanchor.py prepare|promote` under this plan.**
2. **Anything needing a key or credential.** No step of this plan asks for, or
   may accept, a credential value. The deployed legs read values only from
   environment variables the Maintainer has set in their own shell; the runner
   never prints, persists, or logs one; and the modules' documentation contains
   no example with a real value. **An agent does not run `deployed-passive`
   against any non-loopback target**, and no test, fixture, or example in this
   plan does so — every `deployed-passive` test in Chunks B, C and D drives a
   *local TLS fixture* through the deployed code path, never a real site.
3. **The `--authorize-base-url` restatement.** By construction this is a human
   act: the operator retypes the exact target. An agent that types it has
   defeated the control. Module doctrine says so, and says plainly — carrying the
   proposal's own honesty forward — that this is **structural command separation,
   not actor authentication**: a shell process cannot prove who invoked it, and an
   agent with the Maintainer's terminal and credentials could perform that act.

## Sequence

Chunk order is load-bearing. **A before B and C**, because both runners are
thin layers over one hardened client and a client whose peer-address property is
unproven makes every later claim unfalsifiable. **F last among the code chunks**,
because the install contract should move exactly once, and only when the bytes it
points at have their evidence. **G after F and after activation.**

```
0. plan-open   -- this plan + the dev/PLANNING.md row-move          [commit pending]
   (plan review) -- required(External + External Security Review); NO code before it lands
1. Chunk A -- the shared hardened client, and the SSRF/rebinding evidence   [commit pending]
2. Chunk B -- api_access_security.py: policy, matrix, finding schema        [commit pending]
3. Chunk C -- web_hosting_security.py: policy, observations                 [commit pending]
4. Chunk D -- the cross-runner confidentiality sweep (AW6/AW8 gate)         [commit pending]
5. Chunk E -- module doctrine + the two INCOMPLETE policy stubs             [commit pending]
6. Chunk F -- install-contract movement (the only bootstrap/_scaffold chunk)[commit pending]
7. Chunk G -- activation registry admission (gated on activation landing)   [commit pending]
8. Chunk H -- SAFETY / DEPENDENCY_BUDGET / CHANGELOG                        [commit pending]
```

Rough size, approximate because it is decision-irrelevant: eight commits, of
which A and D are each larger than the rest combined.

---

### Chunk A — the shared hardened client, and the evidence that it is one

The AW4 gate. Everything here is a template source in the shared `_security_net`
package under `templates/modules/team-gated/`; **no `bootstrap/_scaffold/` file
is touched**, and the module is not yet registered, so nothing installs. Tests
load it by path (`importlib.util.spec_from_file_location`, the idiom already used
across `bootstrap/tests/`).

| # | File | Change |
|---|------|--------|
| A1 | `templates/modules/team-gated/_security_net/__init__.py` | Package marker, an `ENGINE_CONTRACT` version constant, and the **import self-check**: if any sibling engine member is absent or its contract constant disagrees, raise a fixed `EngineIncomplete` the facades map to exit **20 / DEGRADED** before any policy read. This is the runtime half of the mapping-group completeness guard the engine deliberately does not provide. |
| A2 | `templates/modules/team-gated/_security_net/policy.py` | Strict JSON policy loading: reject unknown keys, duplicate IDs, unsupported methods, invalid/absent-scheme URLs, userinfo in URLs, control characters, embedded credentials, secret-shaped literal header values. Ordinal principals matching `p[1-9][0-9]{0,2}`; the credential environment-variable name is **derived** as `CAIRN_API_P<N>_CREDENTIAL` and cannot be supplied by policy. Local and deployed sections have disjoint credential namespaces; a name appearing in both is refused. Optional bounded role token `[a-z][a-z0-9_-]{0,31}`, never emitted. |
| A3 | `templates/modules/team-gated/_security_net/net.py` | URL normalization; address classification (loopback / private / link-local / multicast / unspecified / reserved / public, IPv4 and IPv6); and one **atomic** `resolve → connect → verify-peer` function. Addressing and transport live in one module on purpose: the peer check must be inside the connect path, and a module seam is an invitation to a caller that skips it. Redirects are **never followed** — a `3xx` is classified and returned, and the caller decides; credentials and cookies are never carried anywhere. Byte caps on request and response, header-count and header-length caps, connect/read timeouts, TLS chain + hostname validation through the platform trust store, no connection reuse across targets. |
| A4 | `templates/modules/team-gated/_security_net/report.py` | The sanitized output layer: fixed error-code enumeration (no `str(exc)`, no `repr`, no traceback, no peer-supplied reason phrase or certificate string ever crosses it); `observed_magnitude` bucketing; the per-run HMAC key from `secrets.token_bytes(32)` with DEGRADED-before-first-request on randomness failure; and the off-tree report directory — `tempfile.mkdtemp`, `lstat`/realpath verification that the directory and every ancestor are outside the repository and contain no symlink hop, owner-only permissions, exactly one exclusively created `report.json` at mode `0600` on POSIX. |
| A5 | `bootstrap/tests/test_security_net.py` | The adversarial socket suite. Controlled local HTTP and TLS servers with a **recording** harness: every test can read back the actual peer address, method, request target, header set, redirect sequence, and transmitted byte count. No `urlopen` is mocked anywhere in this file — a mocked client cannot establish a transport property. |

**Acceptance criteria — Chunk A.**

Each row below names the test, the **deletion mutant** that proves the test
discriminates, and the **hazard perturbation** that proves the claim. Both are
run; a row with only a deletion mutant is not accepted.

* **A-1 Rebinding.** *Claim:* a DNS answer that changes between validation and
  connection cannot reach a refused address.
  *Hazard perturbation:* a resolver stub returns a public address on the
  validation call and `127.0.0.1` on the connect call, with the socket layer
  recording the peer actually connected to. Expect refusal, exit 20, and a
  recorded peer that is either absent or immediately closed.
  *Deletion mutant:* delete the post-connect peer check in A3; the same test
  must fail.
* **A-2 Peer disagreement.** *Claim:* the connected peer disagreeing with **every**
  validated address is refused, not merely logged.
  *Hazard perturbation:* the fixture accepts on a second bound address absent
  from the validated set. *Deletion mutant:* as A-1.
* **A-3 Redirect address classes.** *Claim:* a `3xx` to loopback, private,
  link-local, multicast, unspecified, and reserved addresses — and to a mixed
  public/private DNS answer set — is refused in every case.
  *Hazard perturbation:* a table-driven fixture emitting one `Location` per class.
  *Deletion mutant:* remove the redirect classifier; every row must fail.
* **A-4 No credential or cookie carry-over.** *Claim:* nothing authenticating is
  ever sent to a redirect target.
  *Hazard perturbation:* the fixture 302s to a second recording server on a
  different port; assert that server saw **no** `Authorization`, `Cookie`, or
  policy-named header, and that the recorded byte stream to it is empty because
  the redirect was not followed at all. *Deletion mutant:* make the client follow
  redirects; the test must fail.
* **A-5 Redirect loops, method changes, connection reuse.** *Claim:* none of
  these can produce an unvalidated connection. *Hazard perturbation:* a
  self-referential 302 chain; a 302 that a naive client would turn into a `GET`
  after a `POST`; two sequential requests to different hosts on a keep-alive
  socket. *Deletion mutant:* remove the per-target connection isolation.
* **A-6 Caps and malformed input.** *Claim:* oversized bodies, oversized and
  duplicated headers, chunked responses, partial reads, invalid UTF-8, invalid
  JSON, and timeout boundaries are all classified, never crashed through.
  *Hazard perturbation:* a fixture that writes one byte over each cap and then
  stalls. *Deletion mutant:* remove each cap in turn.
* **A-7 TLS.** *Claim:* hostname mismatch, untrusted chain, expiry, and protocol
  failure each refuse. *Hazard perturbation:* four locally generated certificate
  fixtures. *Deletion mutant:* pass `verify_mode=CERT_NONE`; all four must fail.
  **Fence:** the certificates are generated into `tmp_path` by the test and never
  committed; no key material enters the repository.
* **A-8 Order of refusal.** *Claim:* every policy, target, and actor-boundary
  refusal happens **before** DNS, before socket creation, and before any
  credential lookup. *Hazard perturbation:* patch each of `socket.getaddrinfo`,
  `socket.socket` and `os.environ.get` with a probe that records invocation, feed
  a policy that must be refused, and assert **all three probes are untouched**.
  *Deletion mutant:* move one validation below the resolve call; the probe fires
  and the test fails.
* **A-9 Off-tree report.** *Claim:* the report cannot land in the repository.
  *Hazard perturbation:* hostile `TMPDIR` pointing (i) inside the checkout,
  (ii) through a symlink into the checkout, (iii) at an existing file,
  (iv) at an unreadable location. Each must refuse **before** any network or
  credential activity. *Deletion mutant:* remove the realpath containment check.
* **A-10 Engine completeness.** *Claim:* a missing engine member is DEGRADED, not
  a partial run. *Hazard perturbation:* install a copy of the engine into
  `tmp_path` with one member removed and execute the facade; expect exit 20 and
  no policy read. *Deletion mutant:* remove the A1 self-check.
* **Channel note.** Subject: the engine modules. Oracles: a recording socket
  server (a different process's view of what was sent) and probe objects patched
  over the standard library (an assertion about what was *not* called). Neither
  is derived from the code under test.

---

### Chunk B — `api_access_security.py`: require the denial, then execute it

| # | File | Change |
|---|------|--------|
| B1 | `templates/modules/team-gated/api_access_security.py` | The facade. Exactly two subcommands, `local` and `deployed-passive`, with **separate** policy sections, credential namespaces, allowed method sets and preflights. No third mode, no `--allow-mutation`, no environment override, no plugin path. |
| B2 | same | `local`: refuses unless every resolved address **and** the connected peer are loopback, refuses every redirect, and performs both checks **before** reading a local fixture credential. Permits `GET`/`HEAD`/`POST`/`PUT`/`PATCH`/`DELETE` because the target is a disposable loopback fixture. Reads only local-section credential env names; the deployed names are not looked up on this path at all. |
| B3 | same | `deployed-passive --authorize-base-url <url>`: the argument must byte-for-byte equal the normalized exact base URL in the deployed policy section. Mismatch, non-HTTPS, embedded credentials, forbidden port or address class, a redirect outside the exact allowlist, or peer drift refuses **before** deployed credential lookup and before the first request. The schema rejects any method other than `GET`/`HEAD` in the deployed section **regardless of the environment label**. |
| B4 | same | The assertion engine: per protected operation, at least one allowed and one denied case; two-principal ownership swap for object-level operations; function-level denials; property-level assertions naming policy-declared JSON pointers that must be absent and fields that must be present; list/search assertions proving a foreign fixture identifier is absent. A status code alone never satisfies a read case. |
| B5 | same | Optional committed OpenAPI **JSON** comparison: operation IDs only, reporting undocumented and untested operations. No YAML, no GraphQL. |
| B6 | same | The child result document for the dispatcher: on the `local` path, one bounded strict-UTF-8 JSON object with the fixed `schema` / `capability` / `contract` / `evidence_mode: loopback` / `result` / `details` shape the activation contract fixes. Direct invocation prints the sanitized human summary plus the off-tree report path instead. The two output modes are a documented seam, and B-6 below is the test that they cannot be confused. |
| B7 | `bootstrap/tests/test_api_access_security.py` | Public-path subprocess tests against a two-principal loopback fixture API, driven through the installed command line, with the request-recording harness from A5. |

**Acceptance criteria — Chunk B.**

* **B-1 The matrix requires a denial.** *Claim:* a policy whose protected
  operation carries only a positive case cannot report CLEAN.
  *Hazard perturbation:* a fixture API that authorizes **everything** — every
  request succeeds — plus a policy declaring only allowed cases. Expect a schema
  refusal, not a green run. *Deletion mutant:* remove the positive+negative
  requirement from A2's schema; the test must fail.
* **B-2 The swap actually catches BOLA.** *Claim:* CLEAN means the declared
  denial held. *Hazard perturbation:* the fixture returns principal A's object to
  principal B's credential. Expect exit 10 / FINDINGS naming the operation, case
  and assertion IDs. Then fix the fixture and expect exit 0. *Deletion mutant:*
  drop the second-principal request; the FINDINGS case must stop firing —
  recorded as the mutant that proves the swap is what fires, not the status code.
* **B-3 Non-loopback is unreachable from `local`, under every policy shape.**
  *Claim:* the AW1 property. *Hazard perturbation:* a table of policies — public
  hostname, IPv4 and IPv6 private literals, a hostname resolving to a mix, a
  `0.0.0.0`/`[::]` form, a userinfo URL, a non-default port, a trailing-dot FQDN,
  and each with the environment label set to `staging`, `production`, and absent.
  Every row must refuse before DNS. *Deletion mutant:* remove the loopback
  constraint on `local`.
* **B-4 Deployed credentials are outside the local leg's authority.**
  *Claim:* `local` never reads a deployed credential name.
  *Hazard perturbation:* set every deployed-section environment variable to a
  distinctive marker, run `local` against the fixture, and assert the marker
  appears in no request the recording server saw and in no output channel.
  *Deletion mutant:* have `local` resolve the deployed namespace.
* **B-5 Exact re-authorization.** *Claim:* `deployed-passive` refuses a URL that
  is not byte-for-byte the policy's normalized base URL.
  *Hazard perturbation:* a table of near-misses — trailing slash, uppercase host,
  default port made explicit, IDN/punycode form, added query, `http` for `https`.
  Each must refuse before credential lookup. **Every row runs against a local TLS
  fixture; no test contacts a real site.** *Deletion mutant:* compare with
  `startswith`; the near-miss rows must fail.
* **B-6 The two output modes cannot be confused.** *Claim:* the dispatcher child
  document never carries the human summary and the human summary is never parsed
  as a child document. *Hazard perturbation:* run the facade both ways over the
  identical fixture and assert the dispatcher-mode stdout parses as exactly the
  fixed schema with no extra key, while direct-mode stdout does not parse as that
  schema at all. *Deletion mutant:* emit the human summary on the dispatcher path.
* **B-7 Mutation reaches only loopback.** *Claim:* there is no v1 route to a
  non-loopback write. *Hazard perturbation:* a deployed-section policy containing
  a `POST` case; expect a **schema** refusal (not a runtime one), so the refusal
  precedes every other consideration. *Deletion mutant:* remove the deployed
  method restriction from the schema.
* **Channel note.** Subject: the facade. Oracle: the fixture API's own request
  log — a separate process's record of what arrived — plus the parsed output
  schema. Neither derives from the runner's own bookkeeping.

---

### Chunk C — `web_hosting_security.py`: passive observations, local evidence

| # | File | Change |
|---|------|--------|
| C1 | `templates/modules/team-gated/web_hosting_security.py` | Facade with the same two subcommands and the same actor boundary. `local` contacts only a controlled loopback HTTP/TLS fixture; `deployed-passive --authorize-base-url` is unauthenticated in v1, sends only `GET`/`HEAD`, performs no crawl and sends no payload. |
| C2 | same | Target policy: exact HTTP and HTTPS origins, permitted redirect hosts (exact allowlist), site type (`static` / `browser-app` / `data-api`), and reviewed expectations. Same strict-schema rules as B via A2. |
| C3 | same | The checks: HTTP→HTTPS redirect before any host change; certificate chain and hostname validity through the platform trust store; HSTS on HTTPS responses; CSP appropriate to the declared site type including `frame-ancestors`; `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`; cross-origin policy headers where the site type requires them; `Secure`/`HttpOnly`/`SameSite` on observed cookies; redirect and response origins against the exact allowlist. |
| C4 | same | The observation schema: target label, fixed check ID, method, status class, and the expected directive/attribute/redirect relationship, reported as `present` / `missing` / `invalid`, optionally naming a **normalized token from the reviewed expectation set**. Never a full observed header, `Set-Cookie` value, certificate subject, body, redirect URL, or query. No letter grade, ever. |
| C5 | same | The "local CLEAN is not deployed CLEAN" rule, enforced in output: a run whose deployed leg has not executed says so in the summary and in the report, and the child document's `evidence_mode` is `loopback`. |
| C6 | `bootstrap/tests/test_web_hosting_security.py` | Public-path tests against local HTTP and TLS fixtures with controllable headers, cookies, redirects and certificates. |

**Acceptance criteria — Chunk C.**

* **C-1 Each check can fail for its own reason.** *Claim:* every check in C3 is
  live. *Hazard perturbation:* a table-driven fixture that removes exactly one
  header/attribute per row; each row must produce exactly the one corresponding
  `missing`/`invalid` observation and no other. *Deletion mutant:* remove each
  check; the corresponding row must stop failing.
* **C-2 Redirect-before-host-change.** *Claim:* an HTTP origin that redirects to
  a *different host* before upgrading to HTTPS is a finding.
  *Hazard perturbation:* a fixture that 302s `http://a` → `http://b` → `https://b`.
  *Deletion mutant:* drop the ordering assertion; the fixture must go green,
  which is the failure being prevented.
* **C-3 Redirect allowlist.** *Claim:* a redirect to a host outside the exact
  allowlist refuses. *Hazard perturbation:* a `Location` to a second local origin
  not in the policy. *Deletion mutant:* accept any redirect host.
* **C-4 No crawl, no payload.** *Claim:* the runner sends only what the policy
  declares. *Hazard perturbation:* a fixture whose HTML body contains links,
  forms, and an obvious admin path; assert the recording server saw **exactly**
  the declared request targets and methods and nothing else — asserted against the
  server's log, not against the runner's intent. *Deletion mutant:* add a single
  link-following step.
* **C-5 Local is not deployed.** *Claim:* a local CLEAN never presents as deployed
  CLEAN. *Hazard perturbation:* run `local` to completion and assert the summary,
  the report, and the child document all carry `loopback` and the explicit
  not-deployed statement. *Deletion mutant:* remove the C5 marker; the assertion
  must fail.
* **Channel note.** Subject: the hosting facade. Oracle: the fixture's own
  configured header/cookie/redirect table plus its request log — both authored
  outside the runner.

---

### Chunk D — the cross-runner confidentiality sweep

The AW6/AW8 gate. It cannot exist until both runners do, and it is the chunk
that decides whether the accepted output-minimization contract is real. All of D
lands in `bootstrap/tests/test_security_finding_confidentiality.py`.

| # | File | Change |
|---|------|--------|
| D1 | `bootstrap/tests/test_security_finding_confidentiality.py` | The marker fixtures. A unique high-entropy marker is planted **independently** in: each principal credential; each request body; an overexposed JSON property, object ID, array item, and malformed body; every response header, cookie, reason phrase, redirect path and query, and TLS subject field the fixtures can influence; transport/TLS/HTTP exception text and timeout diagnostics; and a policy label deliberately rejected for control characters or excessive length. |
| D2 | same | The sweep: for **every** aggregate outcome (CLEAN / INCOMPLETE / FINDINGS / DEGRADED / NOT APPLICABLE) and every failure phase, scan raw stdout **bytes**, raw stderr bytes, the complete report file, the whole temporary directory, and any captured descendant output. No marker, body fragment, cookie value, credential, redirect query, exception string, ANSI control, bidi control, or forged result line may occur. |
| D3 | same | The temporary directory contains **only** `report.json`. No raw-response artifact is created anywhere, at any exit path. |
| D4 | same | Bucket-boundary table tests across every scalar and collection bucket; **two distinct values of different exact lengths in each non-empty bucket produce byte-identical findings** when fingerprinting is omitted; likewise two collections of different member counts. |
| D5 | same | **Parsed-schema** assertions — not text search — that no output schema contains a byte-length, character-length, member-count, index-count, or any other exact value-derived cardinality key or value. Parsing is used deliberately: a text search for a decimal collides with legitimate statuses and stable IDs. |
| D6 | same | Ordinal-principal tests: valid ordinals, duplicates, zero/negative/oversized ordinals, and email/name/account-shaped labels rejected; the derived credential env name is exactly `CAIRN_API_P<N>_CREDENTIAL` and policy cannot substitute another; a role token is accepted by policy and appears in **no** finding. |
| D7 | same | HMAC tests: equal observations fingerprint equally **within** a run; the same observation fingerprints **differently** across two runs; the key appears in no output, no report, and no temporary file; a failure to obtain randomness is DEGRADED before the first request. |

**Acceptance criteria — Chunk D.**

* **D-1 The sweep is not vacuous.** *Deletion mutant, run first:* delete the
  sanitizer's value-omission step in A4 and confirm the sweep goes red naming the
  channel. Restore and confirm `git diff` is empty. A sweep that stays green with
  the sanitizer removed is decoration.
* **D-2 Each channel is independently covered.** *Hazard perturbation:* re-plant
  the marker in exactly one channel at a time — reason phrase only; redirect
  query only; certificate subject only; exception text only; timeout diagnostic
  only — and confirm the sweep still reports nothing. Each of these is a channel
  that would not exist if the fixture had planted the marker only in a body,
  which is the shallow version of this test.
* **D-3 Exact cardinality is closed as a class, not as a field.** *Hazard
  perturbation:* add a *new* diagnostic field carrying `len(value)` to the
  finding builder; D5 must fail on the parsed schema. This is the perturbation
  that distinguishes "we removed `observed_serialized_bytes`" from "no exact
  cardinality can appear", which is what the round-3 revision actually promised.
* **D-4 Bucket indistinguishability.** *Hazard perturbation:* two `short` values
  of 3 and 31 bytes; assert the two sanitized findings are **byte-identical**.
  *Deletion mutant:* emit the exact length; identity must break.
* **D-5 Fingerprint is not an oracle.** *Hazard perturbation:* the same planted
  value across two separate process runs must yield different fingerprints.
  *Deletion mutant:* derive the key from a constant; the test must fail.
* **D-6 Terminal integrity.** *Hazard perturbation:* fixture-supplied ANSI and
  bidi control sequences, and a string shaped exactly like the runner's own
  result line, in a header and in a JSON value. None may reach stdout, and none
  may be mistakable for a result line. *Deletion mutant:* remove the control
  filtering.
* **Channel note.** Subject: both runners' complete output surface. Oracle: a
  marker string the *test* authored and planted in a fixture the runner does not
  read as configuration. The independence is structural: the runner has no way to
  know the marker is special.

---

### Chunk E — module doctrine and the two INCOMPLETE stubs

| # | File | Change |
|---|------|--------|
| E1 | `templates/modules/team-gated/api-access-security.md` | Threat model; the actor split and its residual stated as the proposal states it (structural command separation, **not** actor authentication); the disposable-fixture requirement and the rule that local mutation evidence is invalid if the fixture has any upstream route; the policy schema; how to read CLEAN — *"the declared denial matrix held at the named target and time, no more"*; the omissions list; the recovery procedure; and the companion-evidence expectation for projects using a policy layer. Names Schemathesis as a recommended contract/authentication extension and says why ZAP's API scan is excluded. |
| E2 | `templates/modules/team-gated/web-hosting-security.md` | The hosting equivalent: threat model, actor split, per-observation reporting and the explicit refusal to issue a grade, the "local CLEAN is not deployed CLEAN" rule, the omissions list, and the deferred adapters (`testssl.sh`, Observatory, Trivy) with the reason each is deferred. |
| E3 | Both files | The **report-handling** section AW6 requires: the report is sanitized but is still security evidence — it may reveal operation names, principal relationships and failure counts — so the Maintainer reviews it before sharing and deletes it under the project's evidence-retention policy. Plus the residual: this protects report handling, **not** live process memory against a debugger, core dump, or same-user process. |
| E4 | `templates/modules/team-gated/api_access_policy_stub.json` | Strict, valid-but-`configured: false` stub. Selecting the module and running the local leg yields **INCOMPLETE (5)**, never CLEAN. Carries the ordinal principals and the two-case-per-operation shape as commented examples that the schema itself accepts. |
| E5 | `templates/modules/team-gated/web_hosting_policy_stub.json` | The same for hosting. |

**Acceptance criteria — Chunk E.**

* **E-1 The stub is INCOMPLETE, and INCOMPLETE is not CLEAN.**
  *Hazard perturbation:* install into a `tmp_path` adopter, run each local leg
  with the untouched stub; expect exit **5** and a summary that names the
  unconfigured policy. Then fill the stub against the local fixture and expect
  **0**. *Deletion mutant:* make `configured: false` a warning; the exit must stop
  being 5.
* **E-2 The stub cannot be accidentally valid.** *Hazard perturbation:* flip
  `configured` to `true` while leaving the operation list empty; expect a schema
  refusal, not a CLEAN over zero operations. This is the "CLEAN over an empty
  matrix" failure and it is a **hazard**, not a test-body concern.
* **E-3 The doctrine says the things the reviews extracted.** Assertion tests
  over both `.md` files for the presence of: the not-actor-authentication
  sentence, the upstream-route invalidation rule, the "no more" CLEAN wording,
  the local-is-not-deployed rule, the report-retention instruction, and the
  process-memory residual. *Hazard perturbation:* delete one sentence at a time
  and confirm exactly one assertion fails per deletion. These are cheap
  documentation-presence tests and the plan says so plainly: they pin that a
  required statement exists, never that it is true.
* `python scripts/claim_check.py <file>` over each new Markdown file, **one file
  per invocation**.

---

### Chunk F — install-contract movement

The only chunk that touches `bootstrap/_scaffold/`, and the only one that moves
the install contract. Treat every new manifest row as a contract change with its
own criteria, not as a side effect of registering a module.

| # | File | Change |
|---|------|--------|
| F1 | `bootstrap/_scaffold/config.py` | **Δ1.** Two new `_MODULE_MAPPINGS` keys. `api-access-security`: doctrine → `dev/modules/api-access-security.md` (substituted); facade → `scripts/api_access_security.py` (verbatim); four engine members → `scripts/_api_access_security/net.py` and its three siblings (verbatim); policy stub → `dev/.cairn/api-access-policy.json` (substituted). `web-hosting-security`: the same shape with its own destinations. **Nothing else in this file moves** — see the delta declaration. |
| F2 | `bootstrap/_scaffold/lockfile.py` | **Δ2**, contingent on *Contract question 1*: add the two `dev/.cairn/*-policy.json` destinations to `_LIVING_STATE_DSTS`, with the reasoning inline — adopter-filled configuration, tracked for upgrade, excluded from the tamper check, and **not** the integrity anchor for the deployed leg. |
| F3 | `bootstrap/_scaffold/install.py` | **Δ4 + Δ5.** `_CAPABILITY_NOTICE_MODULES` and `capability_install_notice_lines(module_names)` — a pure renderer producing the lines the revised install contract requires: the local aggregate command, the separate Maintainer-owned deployed command, the exact-target re-authorization requirement, and the statement that **no deployed credential is read during install or during local evidence**. |
| F4 | `bootstrap/_scaffold/cli.py` | **Δ3.** Two one-line call sites in `main`: after `format_profile_summary(cfg)` on the `--summary` path, and in the post-install block beside the existing `model-selection` notice. No other behaviour changes. |
| F5 | `bootstrap/tests/test_security_capability_install.py` | New: explicit selection via `modules_add` and via an exact `modules:` list; `modules_remove`; **absence from every preset and from the default-on set**; complete mapping-group installation; the summary and post-install notice text; upgrade/`--adopt-module` behaviour; and the manifest/lockfile accounting below. |
| F6 | `bootstrap/tests/test_notice_install.py` | Move the `44` pin. **Re-measure; do not apply a number from this plan.** The file is frozen — note it for the Maintainer. |

**Acceptance criteria — Chunk F.**

* **F-1 The manifest moves by exactly the declared rows.** Capture
  `python bootstrap/scaffold.py --manifest` into the session scratch directory at
  the Chunk-E commit; after F1, diff. Expect **exactly 14 added rows and zero
  removed, zero modified**. Assert the delta, then re-measure the total.
  *Hazard perturbation:* the case this guards is a destination collision with a
  sibling scope's new module — add a row whose destination duplicates an existing
  one and confirm `install_manifest` raises `ValueError` rather than emitting two
  rows. That refusal already exists; the test proves the new rows are inside its
  reach.
* **F-2 Every new row round-trips through the lockfile.** Install each of the
  three selections (API only, hosting only, both) into `tmp_path`; assert every
  installed destination appears in `dev/.cairn/cairn-lock.yml`, that
  `python bootstrap/verify_integrity.py` reports OK on the fresh install, and that
  it **still** reports OK after the adopter fills a policy (the living-state
  property). *Hazard perturbation:* modify an installed **engine member** by one
  byte and confirm `verify_integrity` reports `modified (hash mismatch)` — the
  runner must not be living-state. *Deletion mutant:* add the engine destination
  to `_LIVING_STATE_DSTS`; the hazard test must fail.
* **F-3 The illegal living-state opt-out still refuses.** *Hazard perturbation:*
  hand-edit an installed lockfile to set `living_state: true` on the runner
  record; `verify_integrity` must report the illegal opt-out and fail closed. This
  guards the exact tamper move F2 makes attractive.
* **F-4 Mapping-group completeness.** *Hazard perturbation:* a test that every
  `InstallSpec.src` in both new groups exists under `templates/modules/`; then
  rename one source in a `tmp_path` copy of the templates tree and confirm the
  install is caught — by the test at Cairn build time, and at runtime by A-10's
  DEGRADED exit. Both are asserted, because `install_modules` itself warns and
  continues.
* **F-5 No preset, no default-on.** Assert both names are absent from
  `_DEFAULT_ON_MODULES` and from every `_PRESETS` baseline roster, and that
  `python bootstrap/scaffold.py --summary` for each preset lists neither.
  *Hazard perturbation:* add one to a preset roster in a patched copy and confirm
  the test fails. This is the assertion that the proposal's explicit-selection
  decision cannot erode by a later preset edit.
* **F-6 The notice is emitted on both surfaces and says the four things.**
  Assert the four required statements appear in `--summary` output and in
  post-install output when either module is selected, and appear in **neither**
  when neither is selected. *Deletion mutant:* remove each call site in turn.
* **F-7 The engine delta is exactly the declaration.** Run
  `python -m pytest bootstrap/tests/test_ast_attest.py` and record the reported
  CHANGED / NEW symbol names. They must equal Δ1–Δ5 and nothing else. **A symbol
  outside the declaration is a stop-and-explain, not a re-declaration after the
  fact.** Record the observed set in the commit body verbatim.
* **F-8 Gate-integrity note, not a re-pin.** Record in the commit body that
  `bootstrap/tests/fixtures/scaffold_ast_known_new.json` and
  `bootstrap/tests/test_notice_install.py` are now stale against
  `gate_manifest.json`, that `mapping_symbols._MODULE_MAPPINGS.baseline_digest`
  and `cascade_mutable`'s `pre_run_sha256` for `config.py` have moved, and that
  re-pinning is the Maintainer's supervised act. **Do not re-pin.**
* **F-9 Bandit over the new shipped surface.** Run the release gate and record
  the finding profile over the ten new rows. MEDIUM+ is a stop.

---

### Chunk G — activation registry admission

Gated on `security-verification-activation`'s dispatcher existing. This chunk
adds **two data rows** to a registry that artifact owns and changes none of its
logic.

| # | File | Change |
|---|------|--------|
| G1 | `templates/modules/default-on/run_security_verification.py` | Two fixed registry entries — `module_id`, `runner_repository_path`, `argv_mode` (the exact `local` argv), `policy_repository_path`, `child_schema_version`, `capability_contract_version`, `evidence_mode: loopback`, `accepted_process_exits`, `result_to_aggregate_mapping` — plus the per-entry bounded `details` schema. No path, argv, environment, or executable is adopter-supplied. |
| G2 | `bootstrap/tests/test_security_verification.py` | Aggregate tests **owned by the activation plan**, extended here: no capability selected (`NOT APPLICABLE`, exit 0); each capability alone; both together; each with an unfilled stub (INCOMPLETE, exit 5); precedence `20 > 10 > 5 > 0` across mixed legs. |
| G3 | `templates/core/AGENTS.md` — the **shipped adopter template** | **Conditional, and strikeable.** Only if the landed activation implementation wrote a literal enumeration of registry entries rather than the general "every registry entry" clause. Determined by reading the file at implementation time. If the general clause landed, this row is struck and the chunk touches no template. |

**Acceptance criteria — Chunk G.**

* **G-1 The dispatcher can reach `local` and cannot reach `deployed-passive`.**
  *Hazard perturbation:* attempt, from the dispatcher's own code path, to invoke
  the capability with a `deployed-passive` argv — by patching the registry entry's
  `argv_mode` in a `tmp_path` copy. Expect refusal at registry validation, not at
  the child. *Deletion mutant:* remove the argv-mode validation.
* **G-2 Aggregation cannot strengthen a child.** *Hazard perturbation:* a child
  returning INCOMPLETE alongside a child returning CLEAN must aggregate to 5, and
  a child whose process exit and result disagree must aggregate to 20.
  *Deletion mutant:* remove the exit/result agreement check.
* **G-3 A stale or wrong policy digest does not silently pass.** *Hazard
  perturbation:* under the living-state resolution of *Contract question 1*, the
  dispatcher does **not** digest-bind the policy; assert instead that it
  digest-binds the runner and every engine member, and that modifying one makes
  the leg DEGRADED. *Deletion mutant:* remove the runner digest comparison. **If
  Contract question 1 resolves the other way, this criterion is rewritten before
  implementation, not adapted during it.**
* **G-4 Registry admission preconditions are met and recorded.** The commit body
  states, for each entry, where the five admission conditions are satisfied:
  accepted proposal (`156305f`), this reviewed plan, the complete mapping group
  (F-4), the child schema and precedence tests (G2), and the Security Review of
  the registry change (the plan's own External Security round, or a focused
  follow-on if the registry entries changed after it).

---

### Chunk H — the prose, and the release note

| # | File | Change |
|---|------|--------|
| H1 | `bootstrap/SAFETY.md` | A new rule recording what Cairn now **ships**: network egress from two capability runners; the SSRF / DNS-rebinding controls and where they live; credential handling by environment-variable name only, with derived names; remote-target ownership and the exact-URL re-authorization; the active-versus-passive boundary; and the external-tool trust roots that are deferred rather than adopted. Rule 5 ("the bootstrap does not read from the internet") is left **true and re-scoped in place** — it is about the scaffold, and the new rule says so explicitly so a reader cannot take Rule 5 as covering shipped modules. |
| H2 | `bootstrap/DEPENDENCY_BUDGET.md` | A statement that v1 of both modules is **standard-library-only** and declares **no new exception**: Schemathesis, OPA, Cedar, OpenFGA, `testssl.sh`, Trivy, ZAP and Observatory are evaluated alternatives or documented extensions, not installed dependencies. Placed so it cannot be misread as a third exception beside `bandit`/`pip-audit` and `vermin`. |
| H3 | `CHANGELOG.md > Unreleased > Added` | One line naming the two selectable capabilities, the loopback-only agent-facing leg, the separate Maintainer-owned passive deployed command, and the content-free finding contract. Cross-reference the proposal and plan **by filename stem, not path link**. **Serialized shared file** — lands at the defined serialization point, in this chunk's commit. |

**Acceptance criteria — Chunk H.**

* `python scripts/check_cairn.py` → OK. Capture the file count before and after;
  it may only grow.
* `python scripts/quality_gate.py --sub neutrality` → **unchanged** against a
  capture taken immediately before H1. `bootstrap/*.md` is inside the scan roots
  and both new module doctrine files name no vendor or model.
* `python scripts/claim_check.py <file>` over each edited Markdown file, one file
  per invocation.
* **Verify the quoted text before editing.** H1 and H2 quote lines that sibling
  scopes may have moved. Re-read both files at implementation; do not apply the
  edits from this plan's text alone.
* **Channel note.** The claim is that the prose matches the shipped behaviour.
  The evidence is a reading of the landed runners plus a live run of each
  installed command, not a reading of the prose just written. `check_cairn`
  checks link and claim-path integrity, never whether a sentence is true.

## Acceptance criteria

Per-chunk criteria are above; these are the plan-level deliverables.

* **Tests that must pass.**
  * `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests` — the whole
    suite, green, **0 failed / 0 skipped / 0 xfailed**, under the canonical
    interpreter (Python 3.13.x) with `PYTHONDONTWRITEBYTECODE=1`. Baseline
    **taken clean before Chunk A**, not carried from this plan's dirty-tree
    collection figure of 1746 (`as_of 2026-08-04`).
  * [`bootstrap/tests/test_security_net.py`](../../bootstrap/tests/test_security_net.py)
    — A-1 … A-10, the AW4 gate.
  * [`bootstrap/tests/test_api_access_security.py`](../../bootstrap/tests/test_api_access_security.py)
    — B-1 … B-7.
  * [`bootstrap/tests/test_web_hosting_security.py`](../../bootstrap/tests/test_web_hosting_security.py)
    — C-1 … C-5.
  * [`bootstrap/tests/test_security_finding_confidentiality.py`](../../bootstrap/tests/test_security_finding_confidentiality.py)
    — D-1 … D-6, the AW6/AW8 gate.
  * [`bootstrap/tests/test_security_capability_install.py`](../../bootstrap/tests/test_security_capability_install.py)
    — F-1 … F-6.
  * [`bootstrap/tests/test_notice_install.py`](../../bootstrap/tests/test_notice_install.py)
    — re-pinned count, otherwise unchanged and green.
  * **Every new test shown non-vacuous by a run deletion mutant *and* a run
    hazard perturbation**, with the ledger — the change made, the failure
    observed with its message, the byte-identical restore verified against
    `git rev-parse HEAD:<path>` — in the commit body. Where a test can only carry
    one of the two, the plan says which and why, rather than letting the absence
    read as coverage.
* **Doc updates that must land.** All hand-authored: the two module doctrine
  files (Chunk E), `bootstrap/SAFETY.md`, `bootstrap/DEPENDENCY_BUDGET.md`, and
  `CHANGELOG.md > Unreleased > Added`. No generated docs, no snippet-synced
  blocks. **N/A**: `docs/` — nothing here changes a description of the software
  an adopter reads outside the module doctrine.
* **Examples / smoke checks required.** Install each of the three selections into
  a temporary adopter and execute the installed public commands — first with
  untouched stubs (expect INCOMPLETE), then against controlled local fixtures
  (expect CLEAN, then FINDINGS with a deliberately over-permissive fixture).
  `python bootstrap/scaffold.py --summary` for preset, preset + add/remove, and
  exact-module-list profiles. `python bootstrap/scaffold.py --manifest` diffed
  against the pre-Chunk-F capture. **N/A**: the `examples/` gallery — this change
  touches nothing the runnable examples demonstrate.
* **Inbound path-link updates.** None expected. `dev/PLANNING.md` and
  `dev/NEXT_SESSION.md` refer to plans by filename stem, not path link, so the
  archive-move needs no edit there. Confirm at archive time rather than assume.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants, each with the chunk that enforces it and the test that can fail.**
  * *The agent-facing leg cannot reach a non-loopback peer, under any policy
    shape.* Chunk B, B-3, with the transport half in A-1/A-2.
  * *No v1 route produces a non-loopback write.* Chunk B, B-7 — enforced at
    **schema** level so the refusal precedes every runtime consideration.
  * *A deployed credential name is never resolved on the local path.* Chunk B,
    B-4, asserted by marker absence rather than by inspection.
  * *Every refusal precedes DNS, socket creation, and credential lookup.*
    Chunk A, A-8, asserted by probes that must remain untouched.
  * *No output channel carries observed content, on any exit path.* Chunk D,
    D-1/D-2.
  * *No output schema carries an exact value-derived cardinality.* Chunk D, D-3,
    asserted on the parsed schema, not on rendered text.
  * *A finding names principals only by ordinal.* Chunk D, D-6.
  * *A selected-but-unconfigured capability is INCOMPLETE, never CLEAN.*
    Chunk E, E-1.
  * *The install contract moves by exactly the declared rows.* Chunk F, F-1.
  * *The engine symbol delta equals the declaration.* Chunk F, F-7. **This is the
    invariant the cluster depends on**, and it is the one with no automatic
    enforcement — `test_ast_attest.py` reports the set, a human compares it to the
    declaration. Named as the weakest link rather than presented as guarded.
* **Public-path → test mapping.** Four public entry points ship:
  `python scripts/api_access_security.py local|deployed-passive` and
  `python scripts/web_hosting_security.py local|deployed-passive`. All four are
  exercised **through the installed command line as subprocesses**, against
  controlled servers, by
  [`bootstrap/tests/test_api_access_security.py`](../../bootstrap/tests/test_api_access_security.py)
  and
  [`bootstrap/tests/test_web_hosting_security.py`](../../bootstrap/tests/test_web_hosting_security.py),
  with the confidentiality sweep in
  [`bootstrap/tests/test_security_finding_confidentiality.py`](../../bootstrap/tests/test_security_finding_confidentiality.py)
  driving the same four paths. **No test mocks `urlopen` or any transport call**
  — the proposal rules that insufficient in terms, and the plan holds to it.
  A fifth path, the dispatcher's `local` invocation, is exercised in Chunk G.
* **Failure modes.**
  * DNS answer changes between validation and connection → **closed**, A-1.
  * Connected peer disagrees with every validated address → **closed**, A-2.
  * Redirect to a refused address class → **closed**, A-3 (redirects are not
    followed at all in v1, which is stronger than classifying them safely).
  * Credential or cookie carry-over → **closed**, A-4.
  * Oversized / malformed / stalled responses → **closed**, A-6.
  * TLS failure of any of four kinds → **closed**, A-7.
  * Report lands in the repository → **closed**, A-9.
  * A partial mapping group installs → **open at the engine**, closed at Cairn
    build time (F-4) and at adopter runtime (A-10). Named, because
    `install_modules` warns and continues and this plan deliberately does not
    change it.
  * A filled policy's bytes are not lockfile-attested → **open by design** under
    the living-state resolution; the compensating controls are the strict schema,
    the loopback-only local leg, the exact-URL re-authorization, and git review.
    See *Contract question 1*.
  * A local fixture that proxies to another system → **open, and unclosable by
    this runner.** The runner enforces address and credential namespace; it cannot
    attest the fixture's internals. Module doctrine requires a disposable
    project-owned fixture and calls local mutation evidence invalid if the fixture
    has any upstream route.
  * An agent with the Maintainer's terminal runs `deployed-passive` →
    **open, and named.** Structural command separation is not actor
    authentication. Defence in depth: `deployed-passive` is `GET`/`HEAD` in code,
    so a mistaken or malicious caller still cannot write.
  * A route absent from both the API inventory and the policy → **open**, by
    construction. CLEAN means the declared matrix held, no more.
  * Live process memory observed by a debugger, core dump, or same-user process →
    **open**, stated in doctrine (E3).
* **Edge cases exercised.** Empty policies; duplicate IDs; unknown keys; control
  characters; Unicode and punycode hostnames; trailing-dot FQDNs; IPv4 and IPv6
  loopback and private ranges; userinfo URLs; fragments; default and non-default
  ports; DNS answer sets mixing public and private addresses; redirects and
  redirect loops; chunked and oversized bodies; duplicate headers; multiple
  `Set-Cookie` fields; invalid JSON and invalid UTF-8; 401/403/404 denial
  policies; 204 responses; TLS hostname failure; missing credential variables;
  hostile `TMPDIR`; and child output containing credential canaries.
* **Known omissions, stated rather than implied.** (a) No real cloud account,
  Windows host, public DNS-rebinding lab, GraphQL authorization model, browser
  execution, HTTP/3, mutual TLS, proxy, CDN, or authenticated crawl is covered;
  these are the proposal's named residuals and remain residuals. (b) The off-tree
  report's `0600` mode is POSIX; **Windows behaviour is asserted nowhere in this
  plan and no Windows runner has been executed** — the module doctrine must say
  the report's permission property is POSIX-only until a Windows run exists.
  (c) No human has read the two runners line by line for security content; the
  tests and Bandit are a different thing. (d) The engine symbol-delta invariant
  (F-7) has no automatic enforcement. (e) The duplicated engine copy under a
  both-modules install is enforced identical only by the lockfile hash of each
  copy, not by a cross-copy comparison. (f) Whether the two `44` pins should be
  re-measured by this scope or by whichever cluster scope lands last is a
  sequencing question this plan raises and does not answer.

## Verification

Run under the canonical interpreter (`~/conda_envs/lhm/bin/python3.13`,
Python 3.13.x) with `PYTHONDONTWRITEBYTECODE=1`. A different minor silently
changes the suite figure and, more importantly here, `ssl` and `socket`
behaviour that Chunk A's claims rest on — so the interpreter is named alongside
every figure asserted.

<!-- cairn:slot verification-commands -->
The standing gates Cairn runs before a change lands (the same ones CI
enforces):

* **Engine suite** — `python -m pytest bootstrap/tests` (the whole
  suite; scope to `bootstrap/tests/test_<surface>.py` while iterating,
  but the full suite gates the cut).
* **Prose integrity** — `python scripts/check_cairn.py` (internal link
  / anchor resolution + claim-path check over the Markdown tree).
* **Quality gate** — `python scripts/quality_gate.py` (order-
  independence + vendor-neutrality + redundancy; `--sub neutrality`
  alone for a doctrine / template wording change).
* **Write-time claim check** — `python scripts/claim_check.py <file>` over
  each proposal / plan / doc the change authored. **One file per
  invocation** — the checker takes a single path and exits 2 (usage) on
  more, so loop rather than passing a list.

Plan-specific gates (a security-lint budget, a doc-drift gate, the
model-selection mapping check `python scripts/check_model_selection.py`)
are added per plan when the change touches that surface.
<!-- cairn:end verification-commands -->

**Plan-specific gates, added here because this change touches those surfaces.**

* **The release security gate** — `python bootstrap/security_check.py`. Expected
  `PASS`. Record the finding profile over the ten new template `.py` rows
  separately from the total; a MEDIUM+ finding in a network client is a stop, not
  an allowlist entry.
* **The install-contract assertion** — `python bootstrap/scaffold.py --manifest`,
  diffed against a capture taken at the Chunk-E commit. Expected: **+14 rows,
  −0, ~0**. Re-measure the total; do not assert 109 from this text.
* **The AST delta assertion** — `python -m pytest bootstrap/tests/test_ast_attest.py`
  after Chunk F, with the reported CHANGED and NEW symbol names recorded verbatim
  in the commit body and compared by a human against Δ1–Δ5.
* **Integrity round-trip** — `python bootstrap/verify_integrity.py <tmp adopter>`
  on a fresh install (OK), after a policy fill (OK), and after a one-byte engine
  edit (fail closed).
* **The perturbation ledgers** — per chunk, in the commit body: for each test,
  the deletion mutant and the hazard perturbation, the failure observed with its
  message, and the byte-identical restore verified with `git hash-object` against
  `git rev-parse HEAD:<path>`.
* **The gate-integrity note** — after Chunk F, record which frozen and
  cascade-governed entries are stale and name them. **Do not re-pin**: that is a
  supervised act under `bootstrap/REANCHOR_RUNBOOK.md`, behind the Maintainer
  fence above.

## Plan review — the brief, and why the tier is not discharged

*Required — **External** + **External Security Review**. Implementation does not
start until a review has landed under this heading.*

The tier is carried from the proposal header, where it is a declared trigger
rather than a judgement call: this scope adds network clients,
credential-bearing execution, remote-target policy, and new executable security
gates to the adopter install contract.

**An Internal round does not discharge it, and cannot.** Internal review's floor
is the same agent type in a fresh session; the declared tier names two
structurally independent reads, one of them a security lens. The proposal's own
four External Security rounds do **not** discharge it either — they reviewed a
design, and the Decision says so in terms: the AW4 adversarial fixtures are "a
blocking gate" on the plan, and "this Decision does not discharge that." An
Internal round is welcome as a *sharpening* pass and would be recorded as such;
it does not move the gate. Concretely: implementation may begin only when a
review section written by a different agent type or a human has landed under this
heading.

**The five questions this review should aim at**, in descending weight:

1. **Contract question 1 — is the living-state resolution right?** It is the
   plan's largest deviation from a literal reading of the proposal, and the
   argument for it is that AW1's own satisfier (`--authorize-base-url`) already
   provides the property the lockfile digest was asked to provide. Attack that:
   find the case where a silently edited policy causes harm that the strict
   schema, loopback-only local leg, exact-URL re-authorization and git review do
   not catch. If one exists, the default is wrong.
2. **Is Chunk A's peer-address property actually established by A-1 and A-2?**
   This is the AW4 gate and the place where SSRF and rebinding defects live.
   Reproduce A-1 against the real edited files: change the resolver answer
   between validation and connection and read the recorded peer. If the test
   passes with the peer check deleted, the gate is decoration. Also check that
   A-8's probes are the right three boundaries and that none of them can be
   satisfied vacuously.
3. **Is the confidentiality sweep exhaustive over channels, or over bodies?**
   D-2 exists because a sweep that plants a marker only in a response body proves
   almost nothing. Check the channel list against the runners as implemented and
   name a channel D1 misses. Check D-3 specifically: does the parsed-schema
   assertion close the exact-cardinality **class**, or only the fields the plan
   thought of?
4. **Is the declared engine symbol delta complete and minimal?** Two design
   choices exist only to shrink it — routing the summary line through `cli.main`
   instead of `format_profile_summary`, and refusing to fix `install_modules`'
   warn-and-continue. Say whether either trades real safety for a smaller
   ceremony union. If `install_modules` should be fixed, say so and it moves to
   its own scope rather than riding here.
5. **Is Contract question 2's two-destination engine copy acceptable?** It is a
   plan invention on top of the proposal's path list. The alternative is two
   self-contained runners. Say which you would rather review.

Two further things a reviewer is invited to **strike** rather than accept: row
**G3** (the conditional adopter-template edit), and the documentation-presence
tests in **E-3**, which pin that a sentence exists and never that it is true.

> **The landed review appends here as a `### Plan review -- <reviewer> --
> YYYY-MM-DD` sub-heading** (plus a `### Sharpening` sub-heading if it raised
> findings). **Do not rename this heading to a bare `## Plan review`** — the
> lifecycle checker matches a section *kind*, not a review, so a bare heading
> lets an empty section satisfy the gate.

## Code review

*Filled in after implementation commits land.* The reviewer is not the
implementing agent. Begin with `**Model**: <model or tier when known; "unknown"
if not. Do not copy-paste old model labels; query and state your actual running
model identity.>` immediately below the section header (or below a
`### Code review -- <reviewer> -- YYYY-MM-DD` sub-heading).

The falsification ledger this review owes, at minimum:

* **Independently reproduce A-1 and A-2** rather than re-trusting the
  implementing session's transcript. These are the two claims the whole scope
  rests on.
* **Independently reproduce D-1** — delete the sanitizer, confirm the sweep goes
  red, restore, confirm `git hash-object` matches `git rev-parse HEAD:<path>`.
* **Confirm the observed AST delta equals Δ1–Δ5** by running the attestation and
  reading the reported symbol names, not by reading this plan.
* **Confirm no test mocks a transport call.** Grep the three runner test files
  for `urlopen`, `monkeypatch.setattr` over `http.client`/`ssl`, and any
  `MagicMock` in a request path; the proposal rules mocked transport
  insufficient, and a single mocked socket would hollow out the whole gate.
* **Confirm the deployed legs were exercised only against local fixtures** — no
  test, fixture, or recorded transcript contacts a real host.

## Lasting-truth migration

*Pre-declared at plan-open so that no deferred item arrives at archive time
without a home.* Per the
[Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home outside the
plan. This section is append-only once written; the entries below are the
**intended** homes, confirmed or corrected at archive.

| Deferred item | Durable home |
|---|---|
| YAML OpenAPI and GraphQL authorization inventory | A new proposal (`api-access-security` v2). Backlog row in `dev/PLANNING.md` at archive; named as deferred in `templates/modules/team-gated/api-access-security.md`. |
| `testssl.sh` as a local TLS adapter | A new proposal, gated on exact release, checksum/provenance source, ambient-config behaviour, platform matrix, and finding-exit contract. Deferral reason recorded in `templates/modules/team-gated/web-hosting-security.md`. |
| MDN HTTP Observatory as a manual second opinion | Module doctrine (`web-hosting-security.md`) extensions section, with the public-scan-history reason. No proposal needed — it stays a documented manual step. |
| Cloud posture (`cloud-hosting-security`) | A new proposal with its own least-privilege, allowlisting, egress, credential-discovery, suppression-provenance, retention and cost review. Boundary statement lives in both module doctrine files so the wall does not depend on this plan surviving. |
| Staging or remote mutation authorization | A new proposal, per the author response: v1 reserves no extension point. Recorded in `api-access-security.md` as explicitly absent. |
| Trivy, ZAP, Nuclei adapters | `portable-security-sweeps`, which already owns the external-adapter provenance surface. |
| Schemathesis / OPA / Cedar / OpenFGA companion evidence | `api-access-security.md` — a standing expectation on the adopter, not a Cairn deliverable. |
| The unattested filled-policy residual (*Contract question 1*) | `bootstrap/SAFETY.md` (Chunk H1) **and** both module doctrine files. Two homes on purpose: one describes Cairn's shipped posture, the other tells the adopter what their CLEAN does not mean. |
| POSIX-only report permissions; no Windows run | `web-hosting-security.md` and `api-access-security.md` residual sections, plus a `dev/PLANNING.md` backlog row for a Windows execution pass. |
| `install_modules` warn-and-continue on a missing module source | Its own scope. Recorded at archive as a backlog row in `dev/PLANNING.md`; if it recurs as an incident rather than a known gap, the `incident-trackers` module is the home. |
| The duplicated engine copy under a both-modules install | `dev/PLANNING.md` backlog row — revisit if Cairn ever gains a module-dependency mechanism. Cost is recorded in both module doctrine files so an adopter is not surprised. |
| The engine symbol-delta invariant having no automatic enforcement | Raised to the Maintainer with the cluster ceremony; if it should become mechanical, that is a change to `bootstrap/REANCHOR_RUNBOOK.md` and belongs to whoever owns the gate, not to this plan. |
