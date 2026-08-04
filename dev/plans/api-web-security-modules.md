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

## Plan review -- Claude (Internal, same-agent-type; security lens) -- 2026-08-04

**Model**: Claude Opus 5 (`claude-opus-5`).

**Standing, stated first because it decides what this section is worth.** I am
the **same agent type as the plan's author** — a fresh Claude session, no
cross-type structural independence. This is an **Internal** round: a sharpening
pass, nothing more. **It does not discharge the declared
`required(External + External Security Review)` tier, and cannot.** The plan
says so itself under *Plan review — the brief*, and I agree with its reasoning
without reservation. Everything below is offered as material for the External
rounds to use or discard, not as a clearance. **Implementation must not start on
the strength of this section.** See **[I1]**, which is about that sentence being
mechanically ignorable.

Method: I re-measured every figure the plan asserts against the working tree
under the canonical interpreter (`~/conda_envs/lhm/bin/python3.13`, 3.13.13) at
HEAD `eacb7dd`, read the two source proposals for the quoted contract text, and
executed both required gates. I did not write, run, or design any of the
proposed code.

### Steelman

This is the strongest plan I have read in this tree, and most of its strength is
in places that are easy to skip past.

The **declared symbol delta is real work, honestly done.** I re-derived it from
`bootstrap/tests/fixtures/scaffold_ast_baseline.json` independently: 174
entries, 98 `FunctionDef` + 53 `Assign` + 10 `ClassDef` = 161. Every one of the
22 *declared-not-changed* symbols is present in the baseline; Δ1–Δ3 are present;
Δ4–Δ5 are absent, which is what "NEW" has to mean. The `_UPDATE_ALLOWLIST` in
`bootstrap/tests/_ast_attest.py` is exactly the four names the plan quotes, and
the plan's conclusion — that Δ1+Δ2+Δ3 disqualifies the surgical path and the
cluster needs one supervised re-anchor — follows from the code, not from
assertion. The `install_manifest` duplicate-destination measurement reproduces
byte-for-byte (`one src → two dsts: {}`; `two srcs → one dst:
{'p/x.py': [...]}`). The 95-row manifest reproduces. The 164-entry `frozen_files`
map, the `cascade_mutable` governance string *"one predeclared mapping-symbol
delta only"*, the `44` pin, and `_manifest_py_sources()` returning a **list**
(so a two-destination source counts twice) all reproduce. That is a plan whose
numbers survive an adversarial re-measure, which is rare.

**The two design choices offered for striking are both correct, and I would
strike neither.** Routing the notice through `cli.main` rather than
`format_profile_summary` genuinely preserves `config.py`'s cascade governance —
I confirmed `main` spans lines 187–698 of `bootstrap/_scaffold/cli.py`, so both
call sites (the `--summary` print and the post-install `model-selection` block)
fall inside one already-CHANGED symbol, at a cost of zero additional governed
surface. And refusing to fix `install_modules`' warn-and-continue is the right
call for a plan that is one of five editing this package; the two-ended
compensation (F-4 at build time, A-10 at runtime) is a better trade than a
shared-path engine edit, and the plan books it as a named open failure mode
rather than pretending it is closed.

**Contract question 2's answer is right, and has stronger precedent than the
plan claims for itself.** `_facade_engine_dir` in `bootstrap/_scaffold/lockfile.py`
does implement exactly the `<dir>/<name>.py` → `<dir>/_<name>` convention, and
`_MODULE_MAPPINGS` already ships a nested engine package this way (the
`team-gated/_intent/*` group). Two byte-identical installed copies is a real
cost, honestly named, and it is much the smaller cost than two independently
reviewed hand-rolled TLS clients. I would rather review one.

**Contract question 1's default also has an uncited precedent in its favour**:
`dev/.cairn/model-selection-mapping.yml` is already in `_LIVING_STATE_DSTS`
(`bootstrap/_scaffold/lockfile.py`, line 84 ff.) for precisely the reason given
here — adopter-filled configuration whose correct-use state differs from the
recorded install. And I verified the fourth compensating control actually
holds: `_GITIGNORE_SEEDS` ignores only specific `dev/.cairn/` *patterns*, never
the directory, so a filled policy really is a tracked file that shows up in a
diff. The plan's reasoning about `verify_integrity` is also exactly right,
including the illegal-opt-out path that F-3 targets.

Finally, the **perturbation discipline is the best part**. The glossary's
deletion-mutant vs hazard-perturbation distinction is a genuinely useful
contribution, D-1's "run the deletion mutant *first*, before trusting the
sweep" is the right ordering, and every *Channel note* correctly identifies an
oracle the subject does not consume. My concerns below are almost all cases
where the plan set that bar and then, in one or two rows, did not clear its own
bar.

### Concerns

#### [I1] This review section mechanically discharges the review-before-implement gate that it explicitly cannot discharge

The plan warns that the lifecycle checker "matches a section *kind*, not a
review", and defends its brief heading by using an em-dash so it will not parse.
That defence works — I confirmed it. But it does not cover the case that has now
occurred: an **Internal** section landing under a *well-formed* heading.

Measured against `templates/skills/_lib/lifecycle_planner.py`:

```
'## Plan review -- Claude (Internal, same-agent-type; security lens) -- 2026-08-04'
  -> {'kind': 'Plan review', 'name': 'Claude',
      'role': 'Internal, same-agent-type; security lens', 'date': '2026-08-04'}
'## Plan review — the brief, and why the tier is not discharged'
  -> None
```

`_HEADER_RE` accepts `#{2,3}`, so the prescribed `### Plan review -- <reviewer>
-- YYYY-MM-DD` sub-heading form parses identically. `_has_kind(art, "Plan
review")` is a `startswith` on the *kind* alone — it reads neither the role, nor
the tier, nor the reviewer's agent type. The conformance check that gates
implementation therefore now reports satisfied: *"status is 'open' and 'Plan
review: required', but no '## Plan review' section has landed"* will no longer
fire on this plan.

This is the plan's own recurring defect class turned on itself — the artifact
under verification supplying the material that verifies it. The gate is
satisfied by a token this plan now carries, produced by a round the plan itself
argues is insufficient.

I was instructed to use this exact heading, so I have; I am not going to
silently deviate from an instruction and I am not going to hide the
consequence. **Recommended fix, for the Maintainer, not for me:** rename this
section to a kind the checker does not key on — `## Sharpening pass -- Claude
(Internal, same-agent-type; security lens) -- 2026-08-04` — leaving `## Plan
review` unclaimed until an External round lands under it. Longer-term, the tier
gap is real for every artifact in this tree, not just this one, and belongs to
whoever owns `lifecycle_planner.py`.

#### [I2] Chunk F makes the suite red, and the plan-level acceptance criterion says it must be green

*Acceptance criteria* requires "the whole suite, green, **0 failed / 0 skipped /
0 xfailed**". The *Maintainer fence* forbids the implementing agent from
re-pinning `scaffold_ast_baseline.json`. Those two cannot both hold after Chunk F.

`bootstrap/tests/test_ast_attest.py` carries two tests —
`test_committed_baseline_accounted_for_across_the_engine_package` and
`test_ast_gate_passes_over_the_full_scaffold_module_set` — that both assert
`A.verify(_BASELINE, modules) == 0` over `bootstrap/_scaffold/*.py`. `verify()`
returns 1 whenever `_classify` produces any CHANGED entry. Δ1, Δ2 and Δ3 are
CHANGED entries by construction. So the moment F1/F2/F4 land, those two tests
fail, and stay failed until the Maintainer's ceremony.

This is not hypothetical — it is the tree's state right now, from the sibling
scopes' in-flight edits:

```
AST attestation FAILED — 6 non-pure-motion symbol(s):
  CHANGED FunctionDef:_minimal_yaml_parse   in bootstrap/_scaffold/config.py
  CHANGED FunctionDef:cmd_upgrade           in bootstrap/_scaffold/upgrade.py
  CHANGED FunctionDef:forked_facade_findings in bootstrap/_scaffold/lockfile.py
  CHANGED FunctionDef:format_forked_facade_warning in bootstrap/_scaffold/lockfile.py
  CHANGED FunctionDef:load_config           in bootstrap/_scaffold/config.py
  MISSING Try
2 failed, 27 passed
```

The plan carefully establishes the analogous point for the *frozen map* ("The
frozen map does not gate the suite — `test_gate_manifest.py` verifies against a
manifest produced from the live tree at test time"), which I confirmed. It then
does not ask the same question of the AST baseline, which does gate the suite.

**Fix:** state, in *Gate accounting* and in Chunk F's criteria, that from the F1
commit until the Maintainer's re-anchor the suite carries exactly two known-red
nodes, name them by node ID, and re-scope the plan-level criterion to "green
except those two, which are the ceremony's to clear". Without that sentence the
implementing agent reaches a hard stop with the fence on one side and an
impossible criterion on the other — and the tempting resolution is the one the
fence exists to forbid.

#### [I3] `scan-coverage` has already landed, so a third frozen file moves and the two `44` pins diverge for the first time

*What is order-sensitive* frames this conditionally: "If `scan-coverage` has
landed, this plan moves both; if it has not, this plan moves one." It has
landed, at `5c91c23`. `bootstrap/tests/test_security_lint.py` is tracked at
HEAD, clean in the working tree, and already carries the second pin
(`test_templates_py_count_is_pinned`, `assert len(on_disk) == 44`). Three
consequences the plan does not carry:

1. **`bootstrap/tests/test_security_lint.py` is a *third* frozen file this scope
   modifies.** I confirmed it is a literal key in the 164-entry `frozen_files`
   map. *Gate accounting* names exactly two (`scaffold_ast_known_new.json`,
   `test_notice_install.py`); F-8's stale-entry report would omit it. Chunk F's
   file table (F1–F6) does not list the file at all.
2. **The two pins now move to different numbers, and this scope is what makes
   them differ.** Measured today: manifest `.py` rows = 44, verbatim `.py` rows
   = 44, distinct `.py` sources = 44 — all three coincide. This scope adds **10
   rows** over **6 distinct files**, so `test_notice_install.py` → **54** while
   `test_security_lint.py`'s on-disk count → **50**. The plan correctly explains
   *why* the counting rules differ, but never says the two pins stop agreeing.
3. **Two committed comments assert the agreement that this scope breaks.**
   `test_security_lint.py`'s own failure message instructs a future editor to
   update both pins in the same commit because *"the two must agree"*, and its
   `_SCAN_EXCLUSIONS` docstring rests on "disk, manifest-verbatim and `git
   ls-files` all agree at 44". Neither is an executable assertion, so nothing
   goes red — which is worse, not better: the next person to touch either pin
   inherits guidance that is now false. This scope should retire that guidance
   in the same commit that falsifies it.

This also resolves the Bandit conditional in the plan's favour: `scan_targets()`
already unions the verbatim-`.py` manifest, so the six new sources enter the
release scan automatically. Worth converting from a hedge to a statement — and
worth flagging that Bandit over a hand-rolled socket/TLS client is where a
MEDIUM+ stop is *likely*, not merely possible.

#### [I4] Contract question 1 narrows a *different* accepted proposal's contract, and Chunk G contradicts itself about it

The plan opens Contract question 1 with "**The proposal** states the property
twice" and gives two quotes. They are from two different artifacts:

* *"lockfile-covered, so a candidate change cannot redirect the standing check
  to a different host without first producing a visible integrity failure"* —
  this scope's source proposal, `2026-08-03-codex-api-web-security-modules.md`.
* *"opens the runner and policy as regular non-symlink files, computes their
  SHA-256 values itself, and compares them with the lockfile"* —
  `dev/proposals/2026-08-03-codex-security-verification-activation.md`, in its
  **Parent-computed apparatus binding** section, accepted separately at
  `4dfcf19`.

That matters because it changes who may resolve the conflict. Framed as one
proposal contradicting itself, it is this plan's to settle. Framed correctly, it
is **this plan proposing to narrow an accepted contract that another scope
owns** — the dispatcher would have to stop digest-binding the policy.

The plan then states both sides of the contradiction:

* *Contract question 1*: "Nothing about the accepted activation contract moves."
* *Scope* and Chunk G: this chunk "adds two registry entries to a dispatcher
  that artifact builds and changes none of its logic."
* G-3: "under the living-state resolution ... the dispatcher does **not**
  digest-bind the policy."

G-3 is the true one. The first two are not. Dropping half of the parent-computed
apparatus binding is a logic change, and it is not this plan's logic.

I want to be clear that I think the **default is substantively right** — the
living-state resolution is correct, the compensating-control argument is sound,
`--authorize-base-url` genuinely does the work the lockfile digest was asked to
do, and the `model-selection-mapping.yml` precedent supports it. The defect is
procedural and it is the kind this tree cares about: an accepted contract being
narrowed by a sibling plan's default rather than by its owner. **Fix:** name the
activation artifact explicitly as the second source, state that the resolution
requires the activation scope to drop the policy half of its digest binding, and
route that as an agreed cross-scope amendment (or a one-line Maintainer ruling)
*before* Chunk G — not as a G-3 assertion discovered at implementation.

#### [I5] The `local` leg's rebinding direction — the leg an agent can reach — has no named test

A-1's hazard perturbation is: "a resolver stub returns a public address on the
validation call and `127.0.0.1` on the connect call." That is the classic
external→internal rebinding, and it is the **deployed** leg's hazard.

The invariant the whole scope rests on is the other one: *"The agent-facing leg
cannot reach a non-loopback peer, under any policy shape"* (Author-accounting).
Its rebinding form is the mirror image — a name that answers **loopback at
validation and a non-loopback address at connect** — and no criterion names it:

* A-1 is the public→loopback direction.
* A-2 is generic ("a second bound address absent from the validated set") but
  never says the second address is non-loopback, and its deletion mutant is "as
  A-1".
* B-3 is the right *leg* but the wrong *phase*: every row "must refuse **before
  DNS**", so B-3 exercises pre-resolution policy validation and by construction
  cannot reach a post-connect peer check at all.

So the plan's own highest invariant is asserted at B-3 and evidenced at
A-1/A-2, and the join between them has a hole exactly where the agent-reachable
leg lives. This is squarely inside the AW4 gate the Decision routed here.

**Fix:** add an explicit `local`-leg row — validated answer `127.0.0.1`,
connected peer a non-loopback bound address, assert refusal and a recorded peer
that is closed immediately — with its own deletion mutant. One row; the fixture
machinery A-2 already needs covers it.

#### [I6] D-2 has neither a deletion mutant nor a hazard perturbation, and can pass vacuously on every channel it names

The plan's own glossary is the standard here: "A test with only a deletion
mutant has been validated; only a hazard perturbation validates the security
property," and "a row with only a deletion mutant is not accepted." D-2 has
neither.

Its stated perturbation is: "re-plant the marker in exactly one channel at a
time — reason phrase only; redirect query only; certificate subject only;
exception text only; timeout diagnostic only — and confirm the sweep **still
reports nothing**." Confirming a green result under a differently-configured
fixture is the base assertion restated, not a perturbation. And it is *exactly*
the shape that passes when the channel is never exercised: if the runner never
reads the reason phrase into any code path that could emit it, the marker
cannot leak, the sweep reports nothing, and D-2 is green while proving zero
coverage of that channel.

This is the same failure D-1 is designed to prevent at the whole-sweep level
("a sweep that stays green with the sanitizer removed is decoration"), reappearing
per-channel. D-1 protects the aggregate; nothing protects the individual
channels, and D-2's whole purpose is the individual channels.

**Fix:** make each channel prove **liveness before confidentiality**. Per
channel: (a) suppress sanitization for that channel only, run, and assert the
marker **does** appear in the named output — proving the runner reaches it;
(b) restore, run, assert absence. (a) is the deletion mutant and (b) is the
claim. Without (a), "no marker found" and "channel never reached" are
indistinguishable, which is the exact evidential failure the plan's own glossary
was written to prevent.

#### [I7] A-8's third probe is bypassable, so the "before any credential lookup" half can be satisfied vacuously

A-8 patches `socket.getaddrinfo`, `socket.socket` and `os.environ.get`, feeds a
policy that must be refused, and asserts all three probes are untouched. The
first two are good boundaries. The third is not a boundary at all:

* `os.getenv(name)` does not call `os.environ.get`.
* `os.environ[name]` goes through `__getitem__`, not `get`.
* A module that binds `from os import environ` at import time, or caches a value
  at import, evades it as well.

So a runner that reads credentials by any of those routes leaves the probe
untouched **while performing the credential lookup the criterion claims to have
excluded**. The perturbation then validates the test, not the hazard — the
category the plan warns against. A-8's deletion mutant ("move one validation
below the resolve call") only exercises the first two probes, so nothing catches
the gap either.

**Fix:** stop probing the accessor and probe the *value*. Set each credential
environment variable to a unique marker (the D1 machinery already does this for
B-4), refuse the policy, and assert the marker appears in no request, no output
channel, and no report — an assertion no access idiom can route around. Keep the
`getaddrinfo` / `socket.socket` probes as-is; they are sound. Also worth
stating: patching `os.environ.get` process-wide during a test is itself noisy,
since pytest and the standard library call it constantly.

#### [I8] Δ2's strikeability is exactly the state the cluster ceremony cannot tolerate, and the alternative's symbols are undeclared

The plan is right that "a delta that quietly changes is worthless" and right to
promise re-declaration. But the sequencing is the problem, not the honesty. The
union is "formed **by the Maintainer at ceremony time** from each scope's
declared delta", and four sibling scopes may re-anchor before Contract question
1 is settled. A declared delta with a live conditional branch is not a
discriminator; it is a discriminator with a hole whose shape is unknown.

The alternative branch makes it concrete: an "`upgrade`-side rehash for
adopter-filled policy files, analogous to the existing `verbatim_rehash`" would
add at least one new `FunctionDef` and change `cmd_upgrade` — and
`FunctionDef:cmd_upgrade` in `bootstrap/_scaffold/upgrade.py` is *already* being
changed by a sibling scope in the current tree (see the CHANGED list in **[I2]**).
Two scopes silently landing in one symbol is precisely the collision the
declaration exists to make impossible.

**Fix:** either resolve Contract question 1 before any cluster scope's ceremony
(cheapest, and [I4] argues it needs a cross-scope ruling anyway), or declare the
alternative branch's symbols *now*, as a conditional Δ2′/Δ6, so the union is
well-defined under both resolutions.

#### Minor, not numbered

* **C-1's deletion-mutant expectation reads inverted.** "*Deletion mutant:*
  remove each check; the corresponding row must stop failing." The fixture row
  is one that *should* produce a `missing`/`invalid` observation, so removing
  the check makes the observation disappear and the **test** fail. C-2 states
  the same idea correctly ("the fixture must go green, which is the failure
  being prevented"). Worth aligning the wording; in a plan this precise the
  inversion will be read as intent.
* **The 1746 collection figure is already stale**, exactly as the plan predicted.
  I measure **1759** on the same tree today. The two untracked sibling test
  files account for 71 nodes, so the drift is not a simple add — it is ordinary
  concurrent churn. No fix needed: the plan already marks the figure
  low-confidence and instructs a clean re-baseline before Chunk A. Recording it
  as confirmation that the caution was warranted.
* **G3's conditional is probably strikeable, but not yet decidable.** The
  activation *proposal* carries the general clause — `templates/core/AGENTS.md`
  "registers the dispatcher, fixed registry, child result schema, and every
  registry entry as high-risk Security Review surfaces". If that lands verbatim,
  G3 is struck. The plan is right to defer to the landed implementation rather
  than the proposal text; noting only that the evidence currently points at
  "strike".

### Covered

Verified by measurement or by reading the cited artifact. Reported as output,
not as reassurance.

* **AST baseline, re-derived independently from
  `bootstrap/tests/fixtures/scaffold_ast_baseline.json`:** 174 total entries;
  `FunctionDef` 98, `Assign` 53, `ClassDef` 10, `Import` 8, and one each of
  `Docstring`/`Expr`/`If`/`If#2`/`Try`. `FunctionDef + Assign + ClassDef = 161`.
  **Both plan figures confirmed exactly.**
* **Declared delta, symbol by symbol.** `Assign:_MODULE_MAPPINGS`,
  `Assign:_LIVING_STATE_DSTS`, `FunctionDef:main` — all present in the baseline,
  so CHANGED is the right classification.
  `Assign:_CAPABILITY_NOTICE_MODULES`, `FunctionDef:capability_install_notice_lines`
  — both absent, so NEW is right. **All 22** *declared-not-changed* symbols are
  present in the baseline; zero missing. The delta is **internally correct and,
  as far as I can measure, complete** — with the [I8] caveat about the
  conditional branch.
* **No undeclared Δ from module registration.** I specifically checked the
  registries a new module could be expected to touch:
  `_MODULE_REQUIRED_TOKENS` is optional per module (only `python-security` has
  an entry), `_TEAM_STAFFING_GATES`/`_TEAM_STAFFING_GATED` cover only
  `dual-review` and `coordination-tiers` (a different concept from the
  `team-gated/` directory), and `_GITIGNORE_SEEDS`/`_MODULE_SUPERSEDES` need no
  row. Nothing forces a sixth symbol.
* **`cli.main` really is the whole surface.** `FunctionDef:main` spans lines
  187–698 of `bootstrap/_scaffold/cli.py`; `args.summary` /
  `format_profile_summary(cfg)` and the post-install `model-selection` block are
  both inside it. Δ3 is one symbol, as declared.
* **Surgical-path unavailability.** `_UPDATE_ALLOWLIST` in
  `bootstrap/tests/_ast_attest.py` (line 141 ff.) is exactly
  `{_MODULE_MAPPINGS, _SKILLS_MAPPINGS, _CORE_MAPPINGS, install_onboarding}`.
  `update_symbol` requires sole-CHANGED plus complete-set `known_new` equality.
  The plan's conclusion holds.
* **Install-contract accounting.** `scaffold.py --manifest` emits 96 lines / 1
  header / **95 data rows** — confirmed. Of those, 44 are `.py` rows, all 44
  verbatim, over 44 distinct sources. The plan's arithmetic checks out:
  +14 rows (2 doctrine + 2 stubs + 2 facades + 8 engine) → 109; +10 `.py` rows
  over 6 distinct new files. `duplicate_destinations` reproduces the plan's
  quoted measurement exactly.
* **Gate manifest.** 164 `frozen_files` entries. `scaffold_ast_known_new.json`
  and `test_notice_install.py` are frozen; `config.py`, `cli.py`, `lockfile.py`,
  `install.py` are **not**. `config.py`'s `cascade_mutable` `governed_by` string
  is verbatim what the plan quotes. `test_gate_manifest.py` does build from the
  live tree at test time, so the plan is right that the frozen map itself does
  not gate the suite. **`test_security_lint.py` is also frozen** — see [I3].
* **`verify_integrity` semantics.** Confirmed line by line: `living_state: true`
  is honoured only for `_LIVING_STATE_DSTS` members and is otherwise reported as
  an *illegal living_state opt-out* that fails closed. F-2 and F-3 target real
  behaviour.
* **The `dev/.cairn/` policy files will be tracked.** `_GITIGNORE_SEEDS` seeds
  only `dev/.cairn/.foldback-draft-*.md`, and Cairn's own `.gitignore` names
  only `local-env.json`, `handoff.lock` and the draft pattern. Contract question
  1's fourth compensating control (git review) is real, not assumed.
* **Facade↔engine convention.** `_facade_engine_dir` (line 318 ff. of
  `bootstrap/_scaffold/lockfile.py`) implements `<dir>/<name>.py` →
  `<dir>/_<name>`; `_MODULE_MAPPINGS` already ships a nested `team-gated/_intent/*`
  package. Contract question 2's claim is accurate on both counts.
* **Decision-side quotes.** `156305f` is the Decision commit; *"ACCEPTED as
  revised"*, *"as revised through round 3"*, AW4 as *"a blocking gate"* and
  *"This Decision does not discharge that"* all verify verbatim. The proposal
  header's *Touches* line does name `templates/core/AGENTS.md`, and the round-1
  revision does contain the exact words *"does not modify
  `templates/core/AGENTS.md`"* — so the plan's supersession reading is right.
  `4dfcf19` is the activation Decision, landed ahead of this one as stated.
* **No missed doc surface.** I searched for a module catalog that a new module
  would have to join — `bootstrap/BOOTSTRAP.md`, `docs/`, `templates/modules/README.md`,
  `templates/core/` — and found none enumerating module names. The plan's
  documentation-surface list and its `docs/` **N/A** hold.
* **Both required gates, run as instructed:**
  `claim_check.py dev/plans/api-web-security-modules.md` → **OK, no flags**
  (35 paths exempted via `claim-check-allow`, all forward references);
  `check_cairn.py dev/plans/api-web-security-modules.md` → **OK, 1 file scanned,
  no issues.** The author's report is accurate.

### Not covered / low confidence

* **The tier is not discharged.** Same agent type, no structural independence.
  Nothing here substitutes for the External + External Security rounds, and
  [I1] is about the gate not knowing that.
* **No code exists, so every claim about runtime behaviour is unverifiable.**
  Chunk A's peer-address property — the AW4 gate — cannot be reproduced against
  a plan. I checked whether the *specified tests would establish the claimed
  properties* ([I5], [I6], [I7]); I could not check whether they *do*. Review
  question 2 ("reproduce A-1 against the real edited files") is untouched here
  and remains entirely the code review's.
* **The confidentiality channel list versus the runners as implemented.** Review
  question 3 asks whether D1's channel list misses a channel. I cannot answer
  that without the runners; I could only test the D-2 *method*, which is where
  [I6] came from. I did not find a missing channel by inspection, and I would
  not read that as evidence there is none.
* **D-3 and D-5's exact-cardinality class closure.** "No exact value-derived
  cardinality key or value" over a parsed schema is a strong formulation and I
  could not construct a counterexample on paper — but a paper attempt is weak
  evidence about a class claim. This needs a real schema.
* **I did not run the full suite.** The tree carries four sibling workflows'
  uncommitted edits; a suite figure taken here would attribute their state to
  this plan, which is the plan's own stated reason for not quoting one. I ran
  only `test_ast_attest.py` (read-only, and the result is reported in [I2]) and
  a `--collect-only` pass.
* **Bandit's likely finding profile over a hand-rolled socket/TLS client.** I
  flagged the risk in [I3] but did not estimate it; that needs the code.
* **Whether the two-copy engine install has an upgrade-path wrinkle.** Both
  copies are verbatim and hash-pinned, and `verify_integrity` covers each
  independently, so drift is caught. I did not trace `cmd_upgrade`'s behaviour
  when one source feeds two destinations — it looks fine, and `install_manifest`
  keys on destination throughout, but I did not execute it and would not assert
  it.
* **Sequencing across the five-scope cluster.** I verified this plan's own
  declaration; I made no attempt to reconcile it with the other four scopes'
  deltas, and [I8]'s `cmd_upgrade` observation is an incidental sighting, not a
  cluster analysis.

### Recommendation

**Second round: yes — but the second round is the External + External Security
pair the plan already declares, not a further Internal one.** This plan does not
need another same-type read; it needs the independent reads it asked for.

Before those rounds open, three items are cheap and would sharpen what they
review — and two of them are questions only the Maintainer can settle:

1. **[I1] — rename this section** so an Internal round does not hold the gate
   open. Maintainer's call; one line.
2. **[I4] — route the activation-contract narrowing** as a cross-scope
   amendment or a Maintainer ruling, and correct the two sentences that say the
   activation contract does not move. The *substance* of the living-state
   default I would keep; it is right.
3. **[I2] + [I3] — repair the gate accounting**: name the two known-red AST
   nodes and re-scope the green-suite criterion; add `test_security_lint.py` as
   the third frozen file, with its pin moving to a *different* number (50) than
   `test_notice_install.py`'s (54), and retire the two committed comments that
   assert they agree.

The three evidential findings — **[I5]** (the `local` leg's rebinding
direction), **[I6]** (D-2 proves nothing per channel), **[I7]** (A-8's third
probe is bypassable) — are the ones I would most want the External Security
reviewer to arrive at independently rather than inherit from me. All three are
one-row fixes; none of them changes the plan's shape. Fixed, the AW4 and
AW6/AW8 gates say what they claim to say.

On the plan's two explicit invitations to strike: **keep both**. The
`cli.main` routing and the `install_modules` non-fix are correct trades, and
Contract question 2's shared engine is the version I would rather review. On
**G3**, the evidence points at "strike", but the plan is right to decide it by
reading the landed file. On **E-3**, keep the presence tests — the plan already
says out loud that they pin existence and never truth, which is the honesty that
makes a cheap test acceptable.
## Response to plan review -- Claude (author) -- 2026-08-04

**Model**: Claude Opus 5 (`claude-opus-5`).

**What this section is.** The author's disposition of the Internal (sharpening)
round above. It **does not discharge** the declared
`required(External + External Security Review)` tier, and nothing below should
be read as clearing implementation. See *Does this clear the plan?* at the end,
which says plainly that it does not and names what remains.

**Method, stated because the round below turns on it.** The review was written
at HEAD `eacb7dd`. I re-derived **every figure it states** against the live tree
under the canonical interpreter (`~/conda_envs/lhm/bin/python3.13`, CPython
3.13.13, `PYTHONDONTWRITEBYTECODE=1`), from the artifacts themselves rather than
from the review's or the plan's text — the baseline JSON, the gate manifest, the
live `install_manifest`, the pinned test files, the two source proposals, and
the running suite. Where a figure did not reproduce I say so and say why. I
also ran the full suite, which neither the plan nor the review did.

**Two of the review's premises no longer hold**, and one of its *Covered*
assurances is wrong on the facts. Both are recorded below at the same weight as
the findings, because a review's confirmations are load-bearing too.

### Re-measurement — what reproduced and what did not

Live tree, canonical interpreter. Cited commits all resolve: `eacb7dd`,
`5c91c23`, `156305f`, `4dfcf19`, `3852cf7`.

| Figure (stated by) | Stated | Live | Verdict |
|---|---|---|---|
| AST baseline total entries (plan + review) | 174 | **173** | **NOT reproduced** — see R1 |
| `FunctionDef`+`Assign`+`ClassDef` (plan + review) | 161 | 161 | reproduces |
| Kind split `FunctionDef` 98 / `Assign` 53 / `ClassDef` 10 / `Import` 8 | as stated | as stated | reproduces |
| The five singletons `Docstring/Expr/If/If#2/Try` | 5 | **4** — `Try` deleted | **NOT reproduced** — see R1 |
| Δ1–Δ3 present in the baseline | present | present | reproduces |
| Δ4–Δ5 absent from the baseline | absent | absent | reproduces |
| All 22 *declared-not-changed* symbols present | 22/22 | 22/22, zero missing | reproduces |
| `_UPDATE_ALLOWLIST` = 4 names, `bootstrap/tests/_ast_attest.py` line 141 | as stated | line 141, exactly those 4 | reproduces |
| `cli.main` spans lines 187–698 of `bootstrap/_scaffold/cli.py` | 187–698 | 187–698 | reproduces |
| `_facade_engine_dir`, `bootstrap/_scaffold/lockfile.py` line 318 | line 318 | line 318 | reproduces |
| `install_manifest` duplicate-destination probe | `{}` / `{'p/x.py': [...]}` | byte-identical | reproduces |
| Published manifest data rows | 95 (96 lines) | 95 (96 lines) | reproduces |
| `.py` manifest rows / distinct sources / verbatim / on disk / `git ls-files` | 44 / 44 / 44 / 44 / 44 | 44 / 44 / 44 / 44 / 44 | reproduces |
| `frozen_files` map size | 164 | 164 | reproduces |
| `bootstrap/tests/test_security_lint.py` is frozen | yes | yes | reproduces |
| `config.py` `cascade_mutable` `governed_by` string | as quoted | verbatim | reproduces |
| `dev/.cairn/model-selection-mapping.yml` in `_LIVING_STATE_DSTS` | yes | yes (5 members) | reproduces |
| `_GITIGNORE_SEEDS` seeds only `dev/.cairn/.foldback-draft-*.md` under `dev/.cairn/` | yes | yes (3 modules seeded; one `dev/.cairn/` pattern) | reproduces |
| `scan_targets()` unions the verbatim-`.py` manifest | yes | yes, `bootstrap/security_check.py` | reproduces |
| `scan-coverage` landed at `5c91c23` | yes | yes | reproduces |
| The two committed "the two must agree at 44" comments | as quoted | verbatim | reproduces |
| `_manifest_py_sources()` returns a list, so a 2-destination source counts twice | yes | yes | reproduces |
| [I4]'s two quotes come from two different proposals | yes | verbatim in both | reproduces |
| [I1]'s heading-parse result | as shown | as shown; live plan parses to kinds `['Code review', 'Plan review']` | reproduces (one correction, see [I1]) |
| **[I2] tree state: "AST attestation FAILED — 6 … 2 failed, 27 passed"** | as quoted | **29 passed, 0 failed; zero CHANGED** | **NOT reproduced** — see R2 |
| Suite collection (plan 1746 / review 1759) | 1746 / 1759 | **1790** | **neither reproduces** |
| Full suite (neither ran it) | — | **1790 passed, 0 failed, 0 skipped, 0 xfailed, 185.9 s** | new measurement |
| `claim_check` "35 paths exempted" | 35 | 36 exemption lines over **22 distinct paths** | **NOT reproduced** (cosmetic) |
| `check_cairn` → OK, 1 file | yes | yes | reproduces |
| Review *Covered*: "no module catalog enumerates module names" | none found | **`templates/modules/README.md` carries a 12-row table** | **NOT reproduced** — see [C1] |

**R1 — the baseline moved because the ceremony already happened.** Commit
`3852cf7`, *"Ceremony 1 -- batched AST baseline re-anchor for Wave 2
(Maintainer-run)"*, re-anchored five function digests and **deleted the `Try`
key** (`config.py`'s module-level `try: import yaml` block, removed by
`profile-parse-fail-open`). Baseline 174 → 173. The `FunctionDef`/`Assign`/
`ClassDef` figure of 161 is unaffected and still reproduces, because `Try` is
none of those kinds. This is the plan's own instruction working as intended
("Re-measure at implementation: the four sibling scopes may have landed by
then") — but the number in the text is now wrong and is amended.

**R2 — [I2]'s evidence is gone; [I2]'s conclusion is stronger for it.** The six
CHANGED/MISSING symbols the review pasted were exactly what Ceremony 1
blessed. `test_ast_attest.py` is now **29 passed**, and the full suite is
**1790 passed, 0 failed, 0 skipped, 0 xfailed**. So the plan's green-suite
criterion is *currently satisfiable* — which removes the cover [I2] implicitly
leaned on and makes Δ1/Δ2/Δ3 the **sole** cause of the red nodes the moment
Chunk F lands. [I2] is accepted on that stronger footing.

### Findings — disposition

Every finding is dispositioned. Accepted findings appear as rows in
*Amendments in force*; nothing is "accepted" here that changes no row.

#### [I1] — the Internal section mechanically discharges the gate. **ACCEPTED, with one correction and a new home.**

Reproduced. `_parse_sections` over the live plan returns section kinds
`['Code review', 'Plan review']`; `_has_kind(art, "Plan review")` is a
`startswith` on the kind alone and returns `True`. The em-dash defence on the
brief heading also reproduces (that heading parses to `None`).

**Correction.** The review renders the violation as *"status is 'open' and
'Plan review: required' …"*. That message cannot fire at `open`: the check is
guarded by `if s in ("executing", "review", "archived")`. Nothing was firing
before, and nothing is being silenced now. What [I1] actually establishes —
and this is the finding, undiminished — is that the gate which would **block
the transition to `executing`** is now pre-satisfied by an Internal round that
argues in its own text that it cannot satisfy it.

**New since the review: the general defect has an owner.** Proposal
`2026-08-04-claude-review-gate-enforcement` is **accepted**, and
`dev/plans/review-gate-enforcement.md` is open against it. Its own measured
table records `full ## review labelled (Internal, same-agent-type)` → **clears**
— an independent reproduction of [I1] from a different session. So [I1]'s
closing "belongs to whoever owns `lifecycle_planner.py`" resolves to a named
scope rather than to nobody.

I have **not** renamed the reviewer's section: it is another agent's attributed
work, this Response is append-only, and the review itself routes the rename to
the Maintainer. Residue instead: an explicit gate-status note in the plan, and
a Lasting-truth row naming `review-gate-enforcement` as the durable home. The
rename remains a Maintainer decision — carried to `openQuestions`.

#### [I2] — Chunk F reds the suite against a green-suite criterion. **ACCEPTED, with the premise corrected and one refinement.**

Premise correction is R2 above. The refinement is measured and matters for what
the amendment must say:

**Only CHANGED reds the suite. NEW does not.** `verify()` prints every NEW
top-level symbol as a `note:` on stderr and returns `0`; only `_classify`'s
CHANGED / MISSING / DUPLICATE entries produce a non-zero return. Measured on
the live tree: **78 live NEW symbols against a 28-key `scaffold_ast_known_new.json`
— 50 of them unpinned — and `test_ast_attest.py` is green**. A concrete instance
landed since the review: `FunctionDef:trusted_upstream` (`bootstrap/_scaffold/install.py`,
from `fork-advisory-semantics` at `9bd6752`) is NEW, absent from `known_new`,
and the suite does not care.

Two consequences. (a) The known-red set after Chunk F is caused by Δ1/Δ2/Δ3
alone; Δ4/Δ5 contribute nothing. (b) The plan's *"NEW … must be added to the
pinned `scaffold_ast_known_new.json`"* is **not** a suite requirement. It is a
precondition of the surgical `update_symbol` path — which this plan has already
established is unavailable to the cluster — and editing that file is a
`FROZEN-MODIFIED` event. Stating it as a "must" invites an implementing agent to
edit a frozen fixture the Maintainer fence forbids. Amended.

The two red nodes, confirmed by collection, are the two tests in
`bootstrap/tests/test_ast_attest.py`:
`test_committed_baseline_accounted_for_across_the_engine_package` and
`test_ast_gate_passes_over_the_full_scaffold_module_set`.

#### [I3] — `scan-coverage` has landed; a third frozen file; the pins diverge. **ACCEPTED, and extended.**

All three sub-points reproduce. Additionally: `bootstrap/tests/test_security_lint.py`
is **already** `FROZEN-MODIFIED` today (`_gate_manifest.py verify` reports
HOLD / 17 violations, that file among them), and `dev/PLANNING.md` carries a
standing Maintainer disposition on it — *"SC4 - fold in"* — routing the re-pin
to the next supervised ceremony. That does not relieve this scope of naming the
file; it tells the implementing agent where the re-pin goes.

The Bandit conditional resolves in the plan's favour, confirmed by reading
`bootstrap/security_check.py`: `scan_targets()` ends with a union over
`install_manifest(modules=None)`'s verbatim `.py` rows, so the six new sources
enter the release scan automatically. Converted from a hedge to a statement.

**Extension the review did not reach — a fourth pin, in the same frozen file.**
`bootstrap/tests/test_notice_install.py` carries a **second** count assertion:
`test_notice_appears_in_manifest_data_row_count`, `assert len(rows) == 95`
(line 145). Chunk F row **F6** names only *"the `44` pin"*, and the plan-level
criteria say *"re-pinned count"*, singular. An implementing agent following F6
literally moves line 75 and leaves line 145 red. Three pins move, in two frozen
files:

| Pin | File / test | Today | After this scope |
|---|---|---|---|
| manifest `.py` **rows** (a list; 2-destination source counts twice) | `test_notice_install.py::test_manifest_has_the_expected_py_source_count` | 44 | **54** (+10) |
| manifest **total data rows** | `test_notice_install.py::test_notice_appears_in_manifest_data_row_count` | 95 | **109** (+14) |
| distinct `.py` **on disk** under `templates/` | `test_security_lint.py::test_templates_py_count_is_pinned` | 44 | **50** (+6) |

Every one of these is *"re-measure, do not apply a number from this plan"* —
the arithmetic above is a prediction to falsify, not a value to type in.

#### [I4] — Contract question 1 narrows another scope's accepted contract. **ACCEPTED, and sharpened by reading the write path.**

Both quotes verified verbatim in their respective artifacts; the second is in
`dev/proposals/2026-08-03-codex-security-verification-activation.md` §
*Parent-computed apparatus binding*. The review is right that framing them as
one proposal contradicting itself is what makes the conflict look like this
plan's to settle.

**Sharpening, from `bootstrap/_scaffold/install.py`'s lockfile writer.** A
living-state record is **not** hash-less: the record dict is built with
`"hash": "sha256:" + …` and `living_state: True` is added *afterwards* as an
extra key. So the dispatcher's *"computes their SHA-256 values itself, and
compares them with the lockfile"* does not degrade into a no-op on a
living-state policy — it degrades into a **guaranteed mismatch** on every
correctly-filled policy, because the recorded hash is the as-installed stub's.
The activation dispatcher must therefore *explicitly skip* living-state records
(or drop the policy leg of the binding). That is a behaviour change in code
this plan does not own, and G-3 as written asserts it from the outside.

`security-verification-activation`'s plan is still `**Status**: open`, so the
amendment is cheap to route now and expensive later. Chunk G gains a blocking
precondition and a Lasting-truth row.

#### [I5] — the `local` leg's rebinding direction has no named test. **ACCEPTED.**

Verified against the plan text, not inherited: A-1's hazard is public-at-validate
→ `127.0.0.1`-at-connect (the deployed direction); A-2 says only *"a second
bound address absent from the validated set"* and its deletion mutant is *"as
A-1"*; B-3 requires every row to *"refuse **before DNS**"*, so it structurally
cannot reach a post-connect peer check. The join has a hole exactly under the
agent-reachable leg, which is the plan's own highest invariant. New criterion
**A-11**, written out in *Amendments in force*.

#### [I6] — D-2 proves nothing per channel. **ACCEPTED.**

Verified. D-2's stated perturbation is *"confirm the sweep still reports
nothing"* — the base assertion restated, and green in exactly the case the
channel is never exercised. **One attribution correction:** the review cites
both standards to "the plan's own glossary"; *"a row with only a deletion mutant
is not accepted"* is from Chunk A's acceptance-criteria preamble, not the
glossary. Immaterial to the finding. D-2 is replaced in full with the
liveness-then-confidentiality two-phase form.

#### [I7] — A-8's third probe is bypassable. **ACCEPTED WITH MODIFICATION.**

The diagnosis is right and reproduces against the plan text: `os.getenv`,
`os.environ[...]`, and an import-time `from os import environ` all leave a patch
on `os.environ.get` untouched.

**Where I modify the fix.** The review's replacement — set markers, refuse, and
assert the marker appears in no request, output channel, or report — is a
*confidentiality* assertion. It cannot distinguish *"refused before the
credential was read"* from *"read the credential, then refused, and didn't emit
it"*, and the ordering claim (*"every refusal happens … before any credential
lookup"*) is the whole point of A-8. Marker-absence would leave A-8 vacuously
satisfiable by a runner that reads first and refuses second.

So A-8 is amended to keep the two sound socket probes, adopt the marker
assertion as the *confidentiality* half, **and** add an ordering oracle no
access idiom can route around: run the refusal in a **subprocess whose
environment does not contain the credential variables at all**, and require the
process to exit with the **policy-refusal** fixed error code — never the
absent-credential code. That is only checkable if those are two distinct fixed
codes, so **A4 gains that requirement** as its own residue row.

#### [I8] — Δ2's live conditional vs the ceremony union. **ACCEPTED WITH MODIFICATION — and the ground under it has moved.**

The specific evidence does not reproduce: `FunctionDef:cmd_upgrade` is no longer
concurrently CHANGED — Ceremony 1 re-anchored it
(`0b3cf4e1a4ed2ba4 → 3a1480d796d59488`) and the tree is clean.

The finding is nonetheless **strengthened by a fact neither the plan nor the
review had**: the cluster ceremony is *not* shared and has already been paid
once. `3852cf7` was **batched for the two Wave 2 plans** — `9bd6752`
(`fork-advisory-semantics`) and `e7394cb` (`profile-parse-fail-open`). Two
consequences for this plan's text:

1. *"This scope shares a single re-anchor ceremony with the rest of the
   cluster"* is **false as written**. This scope's Δ1–Δ5 were not in Ceremony 1's
   union and will need a later one.
2. The five-scope enumeration **omits `fork-advisory-semantics`**, which has
   landed real `bootstrap/_scaffold/` changes (`lockfile.py`, `install.py`,
   `upgrade.py`). Six scopes have touched the package; two have landed.

The review's fix — resolve Contract question 1 *before* this scope's ceremony —
is adopted, and now folds into [I4]'s cross-scope routing rather than standing
alone. I decline the alternative half ("declare the alternative branch's symbols
now as Δ2′/Δ6"): the alternative is explicitly *"new engine mechanism"* the plan
says would need its own proposal, and declaring speculative symbols for a branch
that would not be implemented here would put unfalsifiable rows into a union
whose only value is falsifiability. Declining it is only safe because the
ordering fix is adopted — the resolution lands before the ceremony, so the
conditional is dead by then.

#### Minors

* **C-1's inverted deletion mutant.** Accepted; C-1 amended to C-2's correct
  form.
* **The 1746 collection figure is stale.** Accepted — and the review's own
  replacement is stale too. Live: **1790**. The figure is amended with a fresh
  `as_of` and the standing instruction to re-baseline clean before Chunk A is
  reaffirmed, since 1746 → 1759 → 1790 in two days is the argument for it.
* **G3 is probably strikeable but not decidable.** Accepted, no change.
  Re-verified: `templates/core/AGENTS.md` carries no registry clause today, and
  `dev/plans/security-verification-activation.md` is `**Status**: open`. The
  plan is right to decide G3 by reading the landed file.
* **On the two strike invitations and E-3.** The review says keep all three. I
  agree and record it: the `cli.main` routing and the `install_modules` non-fix
  stay, Contract question 2's shared engine stays, and E-3's presence tests stay
  with their honesty label intact. No amendment.

### Findings the review's *Covered* section asserted that do not hold

Reported at the same weight as its concerns, because a confirmation that is
wrong is worse than a missing one.

#### [C1] — "no module catalog enumerates module names". **DOES NOT REPRODUCE.**

`templates/modules/README.md` (49 lines) carries a `## The modules` table with
one row per module: `| Set | Module | Selected when |`. It is one of the four
places the review says it searched.

Measured, the table lists **12** of the **20** keys in `_MODULE_MAPPINGS`; eight
registered modules — `content-security`, `doc-drift-prevention`,
`documentation-plan`, `examples-gallery`, `incident-trackers`,
`model-selection`, `python-security`, `testing-discipline` — are already absent,
and no test enforces the correspondence. So the plan's `docs/` **N/A** survives
and the omission is not novel; but the plan's *Documentation / doctrine surface*
list is incomplete, and *"Selected when"* is precisely the column where these
two modules are anomalous (not derivable from the six axes; explicit selection
only). Amended: the file is named, with the measured staleness, and the
implementing agent must either add two rows or record why not — not silently do
neither.

#### [C2] — "35 paths exempted via `claim-check-allow`". **DOES NOT REPRODUCE (cosmetic).**

Live: **36** exemption lines over **22 distinct paths**. The gate result is
unchanged (`OK, no claim-check flags`). Recorded for completeness; no amendment.

### Findings of my own, from re-measurement

* **[N1] SPDX headers are a hard, unnamed constraint on six new files.**
  `bootstrap/tests/test_notice_install.py`'s
  `test_every_template_py_source_carries_spdx_header` requires every
  `templates/**/*.py` **manifest source** to carry
  `SPDX-License-Identifier: MIT` within its **first four lines**. The plan never
  mentions SPDX or licensing anywhere. Six new template `.py` files (four engine
  members + two facades) must each carry it, or the suite goes red at Chunk F
  for a reason unrelated to the AST ceremony — and the two red nodes named in
  [I2] would no longer be the whole known-red set. New criterion **F-10**.
* **[N2] The 95-row pin** — folded into [I3] above.
* **[N3] `dev/PLANNING.md` carries no row for this plan.** The *Sequence*'s step
  0 is *"this plan + the dev/PLANNING.md row-move [commit pending]"*; the plan
  is committed and no row exists. Neither do rows for
  `security-verification-activation`, `portable-security-sweeps`, or
  `default-security-stance`, so this is a Wave-wide serialization gap rather
  than this plan's alone. `dev/PLANNING.md` is a serialized shared file and this
  Response does not touch it; raised to the Maintainer instead.

### Amendments in force

Each row names the superseded text **verbatim** and states what replaces it.
This plan is append-only: the rows below **govern** the earlier text and are
what an implementing agent follows where the two disagree.

| # | Superseded text (verbatim) | Replacement / addition | From |
|---|---|---|---|
| **AM1** | `total baselined entries      174` and `  Docstring/Expr/If/If#2/Try  5` (the *Measured baseline* fence) | `total baselined entries      173` and `  Docstring/Expr/If/If#2  4`. `FunctionDef + Assign + ClassDef = 161` is unchanged. Cause: Ceremony 1 (`3852cf7`, Maintainer-run) deleted the `Try` key. `as_of 2026-08-04`, HEAD after `3852cf7`. | R1 |
| **AM2** | "Both figures match the ones this plan was briefed with, so the brief's numbers are confirmed rather than assumed." | "The 161 figure reproduces; the 174 figure did **not** survive two days — it is 173 after Ceremony 1. Treat *both* as snapshots to re-take, not as confirmed constants." | R1 |
| **AM3** | "**AST baseline: 174 entries, 161 of `FunctionDef`/`Assign`/`ClassDef`**, `as_of 2026-08-04`." | "**AST baseline: 173 entries, 161 of `FunctionDef`/`Assign`/`ClassDef`**, `as_of 2026-08-04` (post-`3852cf7`)." | R1 |
| **AM4** | "**NEW (absent from the baseline; must be added to the pinned `bootstrap/tests/fixtures/scaffold_ast_known_new.json`):**" | "**NEW (absent from the baseline; reported by `verify()` as a `note:` and *not* suite-affecting):** Adding Δ4/Δ5 to `scaffold_ast_known_new.json` is a precondition of the surgical `update_symbol` path only — which this plan has already established is unavailable — and that file is frozen. **The implementing agent does not edit it.** Measured `as_of 2026-08-04`: 78 live NEW symbols against 28 pinned keys, 50 unpinned, suite green. Whether `known_new` is re-pinned at the ceremony is the Maintainer's call, reported not performed." | [I2] / N5 |
| **AM5** | "* **This scope shares a single re-anchor ceremony with the rest of the cluster.** The union is formed **by the Maintainer at ceremony time** from each scope's declared delta. This plan supplies its five rows and asserts nothing about the other four scopes' rows." | "* **The cluster ceremony is not single and is already partly spent.** `3852cf7` (*Ceremony 1*, Maintainer-run) was batched for **Wave 2 only** — `9bd6752` `fork-advisory-semantics` and `e7394cb` `profile-parse-fail-open` — and this scope's Δ1–Δ5 were **not** in its union. This scope therefore needs a **later** ceremony, whose union the Maintainer forms at ceremony time. This plan supplies its five rows and asserts nothing about any other scope's rows." | [I8] |
| **AM6** | "**Five accepted scopes edit `bootstrap/_scaffold/`:** `profile-parse-fail-open` (in implementation now), `default-security-stance`, this scope, `portable-security-sweeps`, and `security-verification-activation`. Four are being planned in parallel with this one." | "**Six accepted scopes edit `bootstrap/_scaffold/`:** `fork-advisory-semantics` (**landed**, `9bd6752`), `profile-parse-fail-open` (**landed**, `e7394cb`), `default-security-stance`, this scope, `portable-security-sweeps`, and `security-verification-activation`. Two have landed and been re-anchored; four remain. Re-enumerate at implementation — this list was already wrong by one within a day of being written." | [I8] |
| **AM7** | "**Frozen-file accounting.** Two files this plan modifies are literal keys in the 164-entry `frozen_files` map, `as_of 2026-08-04`: `bootstrap/tests/fixtures/scaffold_ast_known_new.json` (Δ4/Δ5) and `bootstrap/tests/test_notice_install.py` (the `44` pin)." | "**Frozen-file accounting.** **Two** files this plan modifies are literal keys in the 164-entry `frozen_files` map, `as_of 2026-08-04`: `bootstrap/tests/test_notice_install.py` (**two** pins — the `44` `.py`-source count *and* the `95` total-row count) and `bootstrap/tests/test_security_lint.py` (the `44` on-disk count). `scaffold_ast_known_new.json` is frozen but is **no longer modified** by this plan — see AM4. `test_security_lint.py` is already `FROZEN-MODIFIED` today, with a standing Maintainer disposition in `dev/PLANNING.md` (*'SC4 - fold in'*) routing its re-pin to the next supervised ceremony." | [I3] / N2 |
| **AM8** | Chunk F row **F6**, verbatim: `\| F6 \| `bootstrap/tests/test_notice_install.py` \| Move the `44` pin. **Re-measure; do not apply a number from this plan.** The file is frozen — note it for the Maintainer. \|` | F6 becomes: file column `bootstrap/tests/test_notice_install.py` **and** `bootstrap/tests/test_security_lint.py`; change column — Move **three** pins: `test_manifest_has_the_expected_py_source_count` (`44`, rows), `test_notice_appears_in_manifest_data_row_count` (`95`, total rows), and `test_templates_py_count_is_pinned` (`44`, distinct files on disk). The three now move to **different** numbers — predicted 54 / 109 / 50. **Re-measure each; do not apply a number from this plan.** Both files are frozen — note them for the Maintainer. In the same commit, retire the two committed comments that assert the pins agree: `test_security_lint.py`'s failure message (*"the two must agree"*) and its `_SCAN_EXCLUSIONS` docstring (*"disk, manifest-verbatim and `git ls-files` all agree at 44"*). Neither is executable, so nothing goes red — which is why leaving them is worse than moving them. | [I3] / N2 |
| **AM9** | "* **Bandit release-scan reach.** Ten new template `.py` **rows** (six distinct new source files) enter `install_manifest`, and therefore enter `bootstrap/security_check.py`'s scan set — *if* `scan-coverage` has landed its manifest union. If it has not, these files ship unscanned, which is exactly the defect `scan-coverage` exists to close." | "* **Bandit release-scan reach — the conditional is resolved.** `scan-coverage` landed at `5c91c23`; `scan_targets()` ends with a union over `install_manifest(modules=None)`'s verbatim `.py` rows, verified by reading `bootstrap/security_check.py`. The six new sources enter the release scan **automatically**. Bandit over a hand-rolled socket/TLS client is where a MEDIUM+ stop is *likely*, not merely possible — budget for it." | [I3] |
| **AM10** | "* **Suite collection: 1746 tests collected**, `as_of 2026-08-04`" | "* **Suite collection: 1790 tests collected, and the full suite is 1790 passed / 0 failed / 0 skipped / 0 xfailed in 185.9 s**, `as_of 2026-08-04`, HEAD post-`3852cf7`, clean tree. The prior figures were 1746 (this plan) and 1759 (the plan review) — three values in two days. The clean baseline before Chunk A is not optional bookkeeping; it is the only figure that will be true." | Minor / R2 |
| **AM11** | "`~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests` — the whole suite, green, **0 failed / 0 skipped / 0 xfailed**, under the canonical interpreter (Python 3.13.x) with `PYTHONDONTWRITEBYTECODE=1`." | "…green, **0 failed / 0 skipped / 0 xfailed** — **except** that from the F1/F2/F4 commit until the Maintainer's re-anchor the suite carries exactly **two known-red nodes**, which are the ceremony's to clear and **not** the implementing agent's — both in `bootstrap/tests/test_ast_attest.py`: `test_committed_baseline_accounted_for_across_the_engine_package` and `test_ast_gate_passes_over_the_full_scaffold_module_set`. Both fail because `verify()` returns 1 on any CHANGED entry and Δ1/Δ2/Δ3 are CHANGED by construction. Δ4/Δ5 do **not** contribute — NEW is a `note:`, not a failure. **Any third red node is a stop-and-explain, not a second known-red.** The baseline stays green through Chunks A–E, which touch no `bootstrap/_scaffold/` file." | [I2] |
| **AM12** | "The proposal states the property twice" (opening *Contract question 1*) | "**Two accepted proposals** state the property, one each: *'lockfile-covered, so a candidate change cannot redirect the standing check to a different host without first producing a visible integrity failure'* is this scope's own source proposal; *'opens the runner and policy as regular non-symlink files, computes their SHA-256 values itself, and compares them with the lockfile'* is `dev/proposals/2026-08-03-codex-security-verification-activation.md` § *Parent-computed apparatus binding*, accepted separately at `4dfcf19`. This is therefore **not** one proposal contradicting itself; it is this plan proposing to narrow a contract another scope owns." | [I4] |
| **AM13** | "Nothing about the accepted activation contract moves." | "**The accepted activation contract does move, and this plan cannot move it alone.** The living-state resolution requires the dispatcher to stop comparing the *policy* digest. Verified in `bootstrap/_scaffold/install.py`: a living-state lockfile record still carries `hash`, so the comparison does not become a no-op — it becomes a **guaranteed mismatch on every correctly-filled policy**. The dispatcher must explicitly skip living-state records. That is the activation scope's logic, and the change is routed as a cross-scope amendment or a one-line Maintainer ruling **before Chunk G**." | [I4] |
| **AM14** | "This plan adds two registry entries to a dispatcher that artifact builds (Chunk G) and changes none of its logic." — and in Chunk G: "This chunk adds **two data rows** to a registry that artifact owns and changes none of its logic." | Both replaced by: "This plan adds two registry entries to a dispatcher that artifact builds. It changes none of the dispatcher's *aggregation* logic, but under the living-state resolution it **does** require one change to the dispatcher's *apparatus-binding* logic (skip living-state records) — see AM13. **G-3 is the true statement of the three; the two 'changes none of its logic' sentences are not.**" | [I4] |
| **AM15** | Chunk G's gating sentence: "Gated on `security-verification-activation`'s dispatcher existing." | "Gated on **two** preconditions: (a) `security-verification-activation`'s dispatcher exists, and (b) the AM13 cross-scope amendment (or Maintainer ruling) on the policy digest binding has landed. **(b) is blocking regardless of (a).** As of 2026-08-04 neither holds: `dev/plans/security-verification-activation.md` is `**Status**: open`." | [I4] |
| **AM16** | A-2's row: "*Hazard perturbation:* the fixture accepts on a second bound address absent from the validated set. *Deletion mutant:* as A-1." | Unchanged, **plus a new sibling row A-11**: "**A-11 Rebinding, the `local` direction.** *Claim:* the agent-facing leg cannot reach a non-loopback peer even when the DNS answer changes **after** validation — the mirror of A-1 and the direction the plan's highest invariant actually names. *Hazard perturbation:* a resolver stub returns `127.0.0.1` on the validation call and a **non-loopback** bound address on the connect call, with the socket layer recording the peer actually connected to; expect refusal, exit 20, and a recorded peer that is absent or immediately closed. *Deletion mutant:* delete the post-connect peer check in A3 — its own mutant, not 'as A-1', so the two directions are independently discriminated. **Why this row exists:** A-1 covers public→loopback (the deployed hazard), A-2 never says its second address is non-loopback, and B-3 refuses *before DNS* and so cannot reach a post-connect check at all. Without A-11 the invariant *'the agent-facing leg cannot reach a non-loopback peer, under any policy shape'* is asserted in Author-accounting and evidenced nowhere." | [I5] |
| **AM17** | A-8's row, from "*Hazard perturbation:* patch each of `socket.getaddrinfo`, `socket.socket` and `os.environ.get` with a probe that records invocation, feed a policy that must be refused, and assert **all three probes are untouched**." to "…the probe fires and the test fails." | "*Hazard perturbation, in three parts.* **(a) Transport ordering** — patch `socket.getaddrinfo` and `socket.socket` with probes that record invocation, feed a policy that must be refused, assert both probes untouched. These two are sound and are kept. **(b) Credential confidentiality** — set every credential environment variable to a unique marker (the D1 machinery); assert the marker appears in no request the recording server saw, no output channel, and no report. **(c) Credential ordering** — the probe on `os.environ.get` is **deleted**: `os.getenv`, `os.environ[...]` and an import-time `from os import environ` all evade it, so a runner that reads credentials leaves it untouched *while performing the lookup the criterion claims to exclude*. Replaced by an idiom-proof oracle: run the refusal in a **subprocess whose environment does not contain the credential variables at all** and require the **policy-refusal** fixed error code, never the absent-credential code. *Deletion mutant:* move one validation below the resolve call — (a) fires; move one validation below the credential read — (c) flips to the absent-credential code. **Why (b) alone is insufficient:** marker-absence cannot distinguish 'refused before reading' from 'read, then refused, and did not emit', and the ordering claim is A-8's entire content." | [I7] |
| **AM18** | A4's row, at "fixed error-code enumeration (no `str(exc)`, no `repr`, no traceback, no peer-supplied reason phrase or certificate string ever crosses it)" | Unchanged, **plus**: "The enumeration must give **policy/target/actor refusal** and **absent-or-unreadable credential** two **distinct** fixed codes. A-8(c) is only checkable if they differ, and collapsing them would make 'refused before credential lookup' unobservable from outside the process." | [I7] |
| **AM19** | D-2's row: "**D-2 Each channel is independently covered.** *Hazard perturbation:* re-plant the marker in exactly one channel at a time — reason phrase only; redirect query only; certificate subject only; exception text only; timeout diagnostic only — and confirm the sweep still reports nothing." | "**D-2 Each channel is independently covered — liveness before confidentiality.** For **each** channel (reason phrase; redirect query; certificate subject; exception text; timeout diagnostic; and each remaining D1 channel), **two phases, run in this order**: **(a) liveness / deletion mutant** — suppress sanitization *for that channel only*, plant the marker in that channel alone, run, and assert the marker **does appear** in the named output. This proves the runner reaches the channel. **(b) confidentiality / the claim** — restore sanitization, re-run, assert absence. **A channel whose (a) does not go red is not covered and must be recorded as uncovered, not as clean.** *Why:* 'no marker found' and 'the channel is never exercised' are indistinguishable without (a) — the exact per-channel reappearance of the failure D-1 closes at the aggregate level, and the case the plan's own standard (*'a row with only a deletion mutant is not accepted'*, and its converse) exists to forbid." | [I6] |
| **AM20** | C-1's mutant: "*Deletion mutant:* remove each check; the corresponding row must stop failing." | "*Deletion mutant:* remove each check; **the corresponding fixture row must go green, which is the failure being prevented — so the test must fail.** (Aligned with C-2's correct wording; the earlier phrasing reads inverted and, in a plan this precise, would be read as intent.)" | Minor |
| **AM21** | *Documentation / doctrine surface* — the bullet list, after "**Module doctrine — new, and the durable home for most residuals.**" | **Adds a bullet:** "**Module catalog — `templates/modules/README.md`, decided rather than skipped.** Its `## The modules` table carries one row per module, with the columns *Set*, *Module*, *Selected when*. Measured `as_of 2026-08-04`: it lists **12** of the **20** `_MODULE_MAPPINGS` keys — eight registered modules are already absent and no test enforces the correspondence. The implementing agent **either** adds two rows whose *Selected when* says plainly *'explicit selection only — not derivable from the six axes'*, **or** records in the Chunk-F commit body why not. Doing neither is the outcome this row forbids. (This row exists because the plan review's *Covered* section asserted no such catalog exists; it does.)" | [C1] |
| **AM22** | Chunk F's *Acceptance criteria*, after F-9 | **Adds F-10:** "**F-10 Every new template `.py` carries its SPDX header.** `bootstrap/tests/test_notice_install.py`'s `test_every_template_py_source_carries_spdx_header` requires the literal token `SPDX-License-Identifier: MIT` within the **first four lines** of every `templates/**/*.py` manifest source. Six new files qualify (four `_security_net` members + two facades). *Hazard perturbation:* strip the header from one and confirm the test names that file. Unnamed in the plan until now, and a red node here would be a **third** red at Chunk F, breaking AM11's 'any third red node is a stop-and-explain'." | [N1] |
| **AM23** | *Plan review — the brief* — after the paragraph beginning "**An Internal round does not discharge it, and cannot.**" | **Adds a gate-status note:** "**The lifecycle gate no longer distinguishes.** An Internal `## Plan review -- …` section has landed above. Measured against `templates/skills/_lib/lifecycle_planner.py`: `_has_kind(art, 'Plan review')` is a `startswith` on the section *kind* alone, so the conformance check guarded by `status in ('executing','review','archived')` is **pre-satisfied** and will not block the transition to `executing`. **The tier is nevertheless not discharged**, and the fence is this sentence plus the Maintainer, not the tool. The general defect is owned by accepted proposal `review-gate-enforcement` (plan open). Whether the Internal section is renamed to `## Sharpening pass -- …` is the Maintainer's one-line call." | [I1] |
| **AM24** | *Lasting-truth migration* — the table | **Adds three rows.** (1) *"The review-before-implement gate is satisfied by section **kind**, so an Internal round holds it open"* → `review-gate-enforcement` (accepted proposal + open plan); this plan records the local instance only. (2) *"The activation dispatcher must skip living-state policy records"* → a cross-scope amendment to `dev/plans/security-verification-activation.md`, or a Maintainer ruling; **blocking on Chunk G**, and it does not archive with this plan. (3) *"`templates/modules/README.md`'s module table is 8 of 20 stale and unenforced"* → a `dev/PLANNING.md` backlog row at archive; not this scope's to fix, but not this scope's to pretend does not exist either. | [I1] / [I4] / [C1] |

### Findings declined

* **[I8]'s second alternative — "declare the alternative branch's symbols now as
  a conditional Δ2′/Δ6".** Declined. The alternative branch is, by the plan's own
  text, *"new engine mechanism"* that *"would need its own proposal"*; declaring
  symbols for code that would not be written under this plan puts unfalsifiable
  rows into a union whose only value is that every row is falsifiable. The safety
  the review wanted is delivered instead by adopting its **first** alternative —
  resolve Contract question 1 before this scope's ceremony — which AM13/AM15 make
  a blocking precondition. If the Maintainer strikes the living-state default,
  the delta is re-declared before the ceremony, as the plan already promises.

Nothing else is declined.

### Does this Response clear the plan to implement?

**No.** Stated flatly, because a Response is exactly the artifact that gets
mistaken for a clearance.

* **The declared tier is `required(External + External Security Review)`. Zero
  External rounds have landed.** The section above is Internal (same agent type),
  says so itself, and this Response is by the **plan's own author** — the least
  independent read available. Neither is a tier, and the two together are not
  one either.
* **The lifecycle checker will not stop anyone**, per AM23. The gate on
  implementation is this sentence and the Maintainer.
* **One blocking cross-scope item is open**: AM13/AM15 — the activation
  dispatcher's policy digest binding. Chunk G cannot land until it is ruled on,
  and `dev/plans/security-verification-activation.md` is still `open`.
* **One Maintainer decision is open**: whether to rename the Internal section
  (AM23), and whether to strike the Contract question 1 default (which would
  drop Δ2 and change the declared delta before the ceremony).

**What this Response does establish**, so the External rounds do not re-do it:
the plan's engine measurements were re-derived independently and stand except
where AM1–AM3 correct them; the declared delta is internally correct and
complete against the live baseline; the gate accounting is now three pins in two
frozen files plus an SPDX constraint; the ceremony is later and separate, not
shared; and the five questions the plan's brief poses are **untouched** by both
Internal rounds — questions 2, 3 and 5 in particular need code that does not
exist, and question 1 now needs a cross-scope ruling before it can be answered
at all.

The three evidential findings [I5], [I6] and [I7] are accepted and amended into
criteria. They remain the ones I would most want the External Security reviewer
to arrive at independently rather than inherit — an amended criterion is a
hypothesis about what will establish a property, not the establishment of it.
