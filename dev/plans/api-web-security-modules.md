<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/dual-review.md doctrine/lifecycle.md doctrine/coordination.md doctrine/rationale.md doctrine/runtime-contract.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: templates/modules/team-gated/api-access-security.md, templates/modules/team-gated/api_access_security.py, templates/modules/team-gated/api_access_policy_stub.json, templates/modules/team-gated/web-hosting-security.md, templates/modules/team-gated/web_hosting_security.py, templates/modules/team-gated/web_hosting_policy_stub.json, templates/modules/team-gated/_security_net/__init__.py, templates/modules/team-gated/_security_net/policy.py, templates/modules/team-gated/_security_net/net.py, templates/modules/team-gated/_security_net/report.py, templates/modules/default-on/security-verification.md, templates/modules/default-on/run_security_verification.py, dev/modules/api-access-security.md, dev/modules/web-hosting-security.md, dev/modules/security-verification.md, scripts/api_access_security.py, scripts/web_hosting_security.py, scripts/run_security_verification.py, scripts/_api_access_security/net.py, scripts/_web_hosting_security/net.py, dev/.cairn/api-access-policy.json, dev/.cairn/web-hosting-policy.json, bootstrap/tests/test_security_net.py, bootstrap/tests/test_api_access_security.py, bootstrap/tests/test_web_hosting_security.py, bootstrap/tests/test_security_capability_install.py, bootstrap/tests/test_security_finding_confidentiality.py, bootstrap/tests/test_security_verification.py -->
<!-- claim-check-allow: dev/plans/review-gate-enforcement.md, dev/plans/scan-coverage.md -->
<!-- ^ Archived 2026-08-04; the plans moved to dev/plans/archive/. These are
<!-- claim-check-allow: dev/proposals/2026-08-03-codex-security-verification-activation.md -->
<!-- ^ Source/sibling proposals archived 2026-08-04. These citations sit in
     append-only sections, so the path is exempted rather than rewritten. -->
<!-- claim-check-allow: dev/plans/corpus-tier-cost.md -->
<!-- ^ Archived 2026-08-11; the plan moved to dev/plans/archive/.  Cited once,
     at :3768, inside this plan's own append-only "Implementation verification
     -- Chunks H and D" record, which names it among the other sessions' live
     working-tree files that pass explicitly did NOT touch.  The statement was
     true when written; exempting the path is the only correction available,
     since rewriting a prior section to chase a later move is exactly what the
     append-only rule forbids.  Added by the corpus-tier-cost archive commit,
     which caused the move -- no content of this plan was edited. -->

     historical citations in append-only or logged content, so the path is
     exempted rather than rewritten -- editing a prior section to chase a
     file move is what AGENTS.md's cite-by-stem convention exists to avoid. -->

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
| Δ2 | `Assign:_LIVING_STATE_DSTS` | `bootstrap/_scaffold/lockfile.py` | The two adopter-filled policy destinations. **Contingent** — see *Contract question 1* — **and FENCED by B3**: Δ2 is written only by Chunk F's fenced part, so it is **absent from the landing commit's delta** and its appearance there is a fence breach (F-7). |
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
* **The inter-scope ordering edge reaches Chunk F2, not only Chunk G.** It is
  one-directional — activation is harmless without the capabilities, the reverse is
  not — but the fence is wider than this plan first drew it, and it is now the
  single condition **B3** states identically in both plans. **Chunks A–E land
  unblocked** (they touch no `bootstrap/_scaffold/` file). **F1 and F3–F6 land**
  as Chunk F's landing part. **F2 and Chunk G wait on B3**, because F2 is the
  installer act that *produces* the living-state record the dispatcher has no
  ratified binding mode for. If the landing part is done and B3 is unsatisfied,
  the capabilities are directly invocable but **neither integrity-classified nor
  standing checks**, and the module doctrine (Chunk E) and `bootstrap/SAFETY.md`
  (Chunk H) must **say so** rather than claim otherwise.

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

**Four** classes of act in or around this plan are **not** an implementing
agent's to perform. Each is fenced here rather than left to be discovered at the
moment it is convenient to cross.

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
   **And a fourth obligation, on when the ceremony may be *requested*: the
   Maintainer is not asked to move the ref until the live-runner evidence
   exists.** Verified at `d73d436`: `bootstrap/tests/_gate_reanchor.py:64` fixes
   `_DESIGNATED_REF = "refs/cairn/gate-anchor"`, and `promote` advances that ref
   by expected-old CAS — so **the ceremony *is* the ref movement.** Before this
   scope's delta is submitted for any ceremony, **two ledgers must be recorded in
   landed commit bodies**: (1) **A-12**'s live end-to-end transport proof, with
   the observed connected-peer values; and (2) **D-2**'s per-channel phase-(a)
   liveness results for every D1 channel, including any channel recorded as
   *uncovered*. A ceremony requested on a design rather than on executed evidence
   is the failure the External security round named; the fence against
   *performing* the ceremony is above, and this is the fence against *asking for*
   it prematurely.
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
4. **Producing or recording the first-use trust hash set (G-5).** The Maintainer
   computes it out-of-band over the reviewed template sources and records it in
   the supervised commit message. An implementing agent may **report** the
   installed destinations and may **report** a mismatch; it never produces the
   authorized hashes, never re-records them from an installed tree, and never
   treats its own computation as the reviewed set — that is the circularity G-5
   exists to break.

**A fifth act is fenced by B3 below and is the Maintainer's, but it is a
*decision* rather than a class of act**: ratifying the living-state narrowing
that F2 and Chunk G wait on. It is listed here so an implementing agent reading
only this section does not find B3 by surprise.

### Folded, not amended — how to read this plan

**An implementing agent who reads only the chunk tables and their acceptance
criteria executes the current spec.** The review-driven decisions are folded
into the operative rows below rather than bound by reference from an amendment
table. `doctrine/plans.md:202-207` makes chunk-table cell text mutable in place
while a plan's status is `open` with no commits in flight against the chunks
being edited — this plan's exact state: status `open`, zero implementation
commits. The `## Plan review`, `## Response to plan review` and `Sharpening`
sections are **untouched and stay append-only**; the fold ledger in
`### Sharpening — the 2026-08-05 fold pass` at the end of this file names every
amendment row now carried by a cell.

**Where the shared block below and an earlier amendment row disagree, the block
governs.** It supersedes **AM25**'s four-binding ask, **AM26**'s Chunk F
split, and **AM27**'s F2 wording.

**The 2026-08-05 External REVISE round is disposed of by the Maintainer.** The
authorizing instruction, verbatim:

> Go ahead with implementation once you've revised these. I don't want another review round

Recorded in full at `## Maintainer disposition of the 2026-08-05 External review
round` below. **It disposes of the review round and nothing else** — it is not a
bypass of the round, and it supplies no Maintainer credential, no signing ref, no
AST re-anchor ceremony, no ratification of the B3 narrowing below, and no
approval to push.

### The binding contract, and the admission fence it shares

**This block is shared, verbatim, with the reciprocal plan
(`api-web-security-modules` <-> `security-verification-activation`). A change to
it lands in both files in the same commit, or it has not landed.**

**B1 — v1's four named bindings resolve to two apparatus bindings.** The v1
question named four: runner, policy, principal, scope. Exactly two are
apparatus-level: `runner_binding_mode` and `policy_binding_mode`, both in the
registry's closed vocabulary. **Principal and scope are child-policy semantics
and have no apparatus field, by decision and not by oversight.** Verified
against the tree rather than asserted: the installer record binds `src`, `dst`,
`verbatim` and `hash` plus optional living-state / base-cache fields, and
`bootstrap/_scaffold/install.py` contains no `principal` field and no `scope`
binding field — its only occurrences of "scope" are a destination-set comment
and the base-template-cache docstring. Inventing either field is out of scope
for this pair and takes its own design.

**B2 — extra-field disposition.** An unrecognized key in a registry entry or an
installer record is **refused**, not ignored: the reader is a closed-vocabulary
validator and an unknown key is a violation naming the key. Two tests, not one:
the existing missing-field refusal, plus an extra-field refusal. If a
source-owned exact constructor makes an extra field structurally unreachable,
*that* is the contract to state and to test — a structural impossibility is
asserted by a test that tries it, never inferred.

**B3 — the admission fence, one condition on both sides.** The dispatcher and
the registry schema may land with an **empty registry**. What waits is the
*living-state entry and every producer of it*: no entry using
`policy_binding_mode: living_state`, and no chunk that writes the living-state
record, lands until the Maintainer ratifies the narrowing and this shared block
is in force in both files. This is one fence stated identically on both sides,
not a registry fence on one side and a chunk fence on the other.

**B4 — the Chunk F split is replaced, because the old one contradicted its own
criteria.** Fencing F2 while letting F1 and F3--F6 land left Chunk F's
acceptance criteria requiring filled-policy and living-state behavior that F2
was fenced from producing. Chunk F's criteria are rewritten to the B3 line: the
landing part asserts dispatcher-plus-empty-registry behavior only, and every
criterion that needs a filled policy or a living-state record moves to the
fenced part with F2 and Chunk G.


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
6. Chunk F, landing part -- F1, F3-F6: manifest rows, notice, tests         [commit pending]
   >>> ADMISSION FENCE (B3, above): everything below waits on the Maintainer's
   >>> ratification of the living-state narrowing. Dispatcher + schema may land
   >>> with an EMPTY registry; the living-state entry and every producer of it
   >>> wait. An implementing agent that reaches step 7 unratified STOPS.
7. Chunk F, fenced part -- F2 (lockfile.py _LIVING_STATE_DSTS)              [blocked: B3]
8. Chunk G -- activation registry admission                                 [blocked: B3]
9. Chunk H -- SAFETY / DEPENDENCY_BUDGET / CHANGELOG                        [commit pending]
```

**Sequence revision, 2026-08-05.** The list above is revised rather than
rewritten in prose: step 6 splits into a landing part and a fenced part, and the
fence marker between them is B3's single shared condition. Prior entries were not
in flight — no implementation commit exists — so the split is an inline revision
under `doctrine/plans.md:202-207`, not a re-planning of executed work. **Chunk H
may land with the fenced part still outstanding**, and if it does, its prose says
which capabilities are directly invocable but not standing checks rather than
claiming otherwise.

Rough size, approximate because it is decision-irrelevant: nine commits, of
which A and D are each larger than the rest combined, and of which two (steps 7
and 8) may never land under this plan.

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
| A4 | `templates/modules/team-gated/_security_net/report.py` | The sanitized output layer: fixed error-code enumeration (no `str(exc)`, no `repr`, no traceback, no peer-supplied reason phrase or certificate string ever crosses it). **The enumeration must give *policy/target/actor refusal* and *absent-or-unreadable credential* two DISTINCT fixed codes** — A-8(c) is only checkable if they differ, and collapsing them would make "refused before credential lookup" unobservable from outside the process. Also: `observed_magnitude` bucketing; the per-run HMAC key from `secrets.token_bytes(32)` with DEGRADED-before-first-request on randomness failure; and the off-tree report directory — `tempfile.mkdtemp`, `lstat`/realpath verification that the directory and every ancestor are outside the repository and contain no symlink hop, owner-only permissions, exactly one exclusively created `report.json` at mode `0600` on POSIX. |
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
  credential lookup. *Hazard perturbation, in three parts.* **(a) Transport
  ordering** — patch `socket.getaddrinfo` and `socket.socket` with probes that
  record invocation, feed a policy that must be refused, assert both probes
  untouched. **(b) Credential confidentiality** — set every credential
  environment variable to a unique marker (the D1 machinery); assert the marker
  appears in no request the recording server saw, no output channel, and no
  report. **(c) Credential ordering** — there is **no probe on `os.environ.get`**:
  `os.getenv`, `os.environ[...]` and an import-time `from os import environ` all
  evade it, so a runner that reads credentials would leave it untouched *while
  performing the lookup this criterion claims to exclude*. Instead, run the
  refusal in a **subprocess whose environment does not contain the credential
  variables at all** and require the **policy-refusal** fixed error code, never
  the absent-credential code. *Deletion mutant:* move one validation below the
  resolve call — (a) fires; move one validation below the credential read — (c)
  flips to the absent-credential code. **Why (b) alone is insufficient:**
  marker-absence cannot distinguish "refused before reading" from "read, then
  refused, and did not emit", and the ordering claim is this criterion's entire
  content.
* **A-9 Off-tree report.** *Claim:* the report cannot land in the repository.
  *Hazard perturbation:* hostile `TMPDIR` pointing (i) inside the checkout,
  (ii) through a symlink into the checkout, (iii) at an existing file,
  (iv) at an unreadable location. Each must refuse **before** any network or
  credential activity. *Deletion mutant:* remove the realpath containment check.
* **A-10 Engine completeness.** *Claim:* a missing engine member is DEGRADED, not
  a partial run. *Hazard perturbation:* install a copy of the engine into
  `tmp_path` with one member removed and execute the facade; expect exit 20 and
  no policy read. *Deletion mutant:* remove the A1 self-check.
* **A-11 Rebinding, the `local` direction.** *Claim:* the agent-facing leg cannot
  reach a non-loopback peer even when the DNS answer changes **after** validation
  — the mirror of A-1 and the direction this plan's highest invariant actually
  names. *Hazard perturbation:* a resolver stub returns `127.0.0.1` on the
  validation call and a **non-loopback** bound address on the connect call, with
  the socket layer recording the peer actually connected to; expect refusal, exit
  20, and a recorded peer that is absent or immediately closed. *Deletion mutant:*
  delete the post-connect peer check in A3 — **its own mutant, not "as A-1"**, so
  the two directions are independently discriminated. **Why this criterion
  exists:** A-1 covers public→loopback (the deployed hazard), A-2 never says its
  second address is non-loopback, and B-3 refuses *before DNS* and so cannot reach
  a post-connect check at all. Without A-11 the invariant *"the agent-facing leg
  cannot reach a non-loopback peer, under any policy shape"* is asserted in
  Author-accounting and evidenced nowhere.
* **A-12 Live end-to-end transport proof — the runner, not the design.** *Claim:*
  the socket implementation **as built** obeys the address decision, and no
  populated credential reaches any channel, in a run where nothing in the
  transport path is stubbed. *Required form, and it is a post-implementation
  criterion by construction:* execute each of the four public entry points against
  a **real** loopback socket with **no resolver stub, no patched `socket`, no
  patched `ssl`** anywhere in the path; record the **connected peer address as
  observed by the listening fixture** (a different process's view, not the
  runner's own bookkeeping); and, with every credential environment variable
  populated with a distinct marker, assert each marker absent from raw stdout
  bytes, raw stderr bytes, the complete report file, and every file in the
  temporary directory. **A-1 / A-2 / A-11 remain resolver-stub tests and remain
  required — they establish the *decision*; A-12 establishes that the
  *implementation* obeyed it, and neither substitutes for the other.** *Deletion
  mutant:* delete the post-connect peer check; A-12 must go red independently of
  A-1 / A-2 / A-11. Recorded in this chunk's commit body with the observed peer
  values verbatim. **This criterion is also a precondition on *asking for* the AST
  re-anchor ceremony** — see the Maintainer fence.
* **Channel note.** Subject: the engine modules. Oracles: a recording socket
  server (a different process's view of what was sent), probe objects patched over
  the standard library (an assertion about what was *not* called), a subprocess
  whose environment omits the credential variables (A-8(c)), and — for A-12 — a
  listening fixture in a **different process** with nothing in the transport path
  stubbed. **None of these is derived from the code under test.** A-1/A-2/A-11
  are the weakest of them by construction: a stubbed resolver cannot prove the
  socket obeyed the decision, which is exactly why A-12 exists and why a stub-only
  ledger is not accepted as transport evidence.

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
  check; **the corresponding fixture row must go green, which is the failure being
  prevented — so the test must fail.** (Aligned with C-2's wording; "must stop
  failing" reads inverted and, in a plan this precise, would be read as intent.)
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
* **D-2 Each channel is independently covered — liveness before
  confidentiality.** For **each** channel (reason phrase; redirect query;
  certificate subject; exception text; timeout diagnostic; and each remaining D1
  channel), **two phases, run in this order**: **(a) liveness / deletion mutant**
  — suppress sanitization *for that channel only*, plant the marker in that
  channel alone, run, and assert the marker **does appear** in the named output.
  This proves the runner reaches the channel. **(b) confidentiality / the claim**
  — restore sanitization, re-run, assert absence. **A channel whose (a) does not
  go red is not covered and must be recorded as uncovered, not as clean.** *Why:*
  "no marker found" and "the channel is never exercised" are indistinguishable
  without (a) — the exact per-channel reappearance of the failure D-1 closes at
  the aggregate level, and the case this plan's own standard (*"a row with only a
  deletion mutant is not accepted"*, and its converse) exists to forbid. **The
  phase-(a) results for every channel, including any channel recorded as
  *uncovered*, are a precondition on *asking for* the AST re-anchor ceremony** —
  see the Maintainer fence.
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

**This chunk is split by B3, and the split is executable.** The **landing part**
is F1 and F3–F6 and asserts only dispatcher-plus-empty-registry behavior: no
criterion in it needs a filled policy or a living-state record. The **fenced
part** is F2, which travels with Chunk G behind B3's single condition, and every
criterion that needs a filled policy or a living-state record is stated under
*Acceptance criteria — Chunk F, fenced part* and is **not** a condition of the
landing commit. The earlier split — fence F2, keep Chunk F's criteria — is
replaced, because those criteria demanded the behavior F2 was fenced from
producing (B4).

**Landing part — F1, F3–F6.**

| # | File | Change |
|---|------|--------|
| F1 | `bootstrap/_scaffold/config.py` | **Δ1.** Two new `_MODULE_MAPPINGS` keys. `api-access-security`: doctrine → `dev/modules/api-access-security.md` (substituted); facade → `scripts/api_access_security.py` (verbatim); four engine members → `scripts/_api_access_security/net.py` and its three siblings (verbatim); policy stub → `dev/.cairn/api-access-policy.json` (substituted). `web-hosting-security`: the same shape with its own destinations. **Nothing else in this file moves** — see the delta declaration. |
| F3 | `bootstrap/_scaffold/install.py` | **Δ4 + Δ5.** `_CAPABILITY_NOTICE_MODULES` and `capability_install_notice_lines(module_names)` — a pure renderer producing the lines the revised install contract requires: the local aggregate command, the separate Maintainer-owned deployed command, the exact-target re-authorization requirement, and the statement that **no deployed credential is read during install or during local evidence**. |
| F4 | `bootstrap/_scaffold/cli.py` | **Δ3.** Two one-line call sites in `main`: after `format_profile_summary(cfg)` on the `--summary` path, and in the post-install block beside the existing `model-selection` notice. No other behaviour changes. |
| F5 | `bootstrap/tests/test_security_capability_install.py` | New: explicit selection via `modules_add` and via an exact `modules:` list; `modules_remove`; **absence from every preset and from the default-on set**; complete mapping-group installation; the summary and post-install notice text; upgrade/`--adopt-module` behaviour; the manifest/lockfile accounting below; and **B2's installer-record field vocabulary, in three parts** — (a) *exact writer vocabulary*: for each of the ten new destinations, the lockfile record's key set is exactly `{src, dst, verbatim, hash}` plus, and only where the branch that adds it is taken, `base_cache` / `base_hash` (substituted destinations) — measured at `d73d436`, the record is a source-owned exact dict literal at `bootstrap/_scaffold/install.py:1627-1646`, so an extra key is structurally unreachable **at write time**; the test asserts the key set rather than inferring the impossibility. (b) *the tried impossibility*: attempt to introduce an eleventh key by hand-editing an installed lockfile record, then run `python bootstrap/verify_integrity.py`. **Measured at `d73d436`: it does not refuse.** `bootstrap/verify_integrity.py:63-111` reads each record with `rec.get(...)` and never enumerates the permitted keys, so an unrecognized key is **ignored**, not named. Land this as a **characterization** test whose docstring says in those words that a green result is a recorded gap, not B2 satisfied. (c) *where B2 is actually satisfied*: the closed-vocabulary refusal that names the key lives in the **dispatcher's** lockfile-record reader, which `security-verification-activation` owns and tests (its T44). Closing the `verify_integrity` half is a change to `bootstrap/verify_integrity.py`, which is **outside this plan's declared symbol delta and outside its Proposed paths** — it does not land here; it is routed as a lasting truth at archive. |
| F6 | `bootstrap/tests/test_notice_install.py` **and** `bootstrap/tests/test_security_lint.py` | Move **three** pins, not one: `test_manifest_has_the_expected_py_source_count` (`44` manifest `.py` sources, `bootstrap/tests/test_notice_install.py:75`), `test_notice_appears_in_manifest_data_row_count` (`95` total manifest rows, same file line 145), and `test_templates_py_count_is_pinned` (`44` distinct `.py` on disk under `templates/`, `bootstrap/tests/test_security_lint.py:291`). All three values verified at `d73d436`. They now move to **different** numbers — predicted 54 / 109 / 50, and a prediction is not a measurement: **re-measure each; do not apply a number from this plan.** Both files are frozen in the 164-entry `frozen_files` map — note them for the Maintainer, do not re-pin. In the same commit, retire the two committed comments that assert the pins agree: `bootstrap/tests/test_security_lint.py:296` (*"the two must agree"*) and its `_SCAN_EXCLUSIONS` docstring at line 48 (*"all agree at 44"*). Neither is executable, so nothing goes red — which is why leaving them is worse than moving them. |

**Fenced part — F2. Blocked by B3; does not land with the part above.**

| # | File | Change |
|---|------|--------|
| F2 | `bootstrap/_scaffold/lockfile.py` | **Δ2 — FENCED by B3. Do not write this row on the strength of this plan alone.** Add the two `dev/.cairn/*-policy.json` destinations to `_LIVING_STATE_DSTS`, with the reasoning inline — adopter-filled configuration, tracked for upgrade, excluded from the tamper check, and **not** the integrity anchor for the deployed leg. **This is the installer act that *produces* the living-state policy record**, so B3 holds it with Chunk G: it lands only after the Maintainer ratifies the narrowing and the shared binding-contract block is in force in both plans. An implementing agent who reaches F2 unratified **stops and reports**, and records F2 as deferred in the landing commit's body. The Maintainer's disposition of the 2026-08-05 review round does **not** ratify this — see *Folded, not amended* above. |

**Acceptance criteria — Chunk F, landing part (F1, F3–F6).**

Every criterion here is assertable with an **empty registry, no living-state
record, and no filled policy**. If a criterion below turns out to need one, it is
mis-sited and moves to the fenced part rather than being weakened.

* **F-1 The manifest moves by exactly the declared rows.** Capture
  `python bootstrap/scaffold.py --manifest` into the session scratch directory at
  the Chunk-E commit; after F1, diff. Expect **exactly 14 added rows and zero
  removed, zero modified**. Assert the delta, then re-measure the total. The
  pre-capture total is **95 data rows** measured at `d73d436` — a *starting
  point to re-take at the Chunk-E commit*, not a constant: every sibling scope
  adding module files moves it, and 14 is a **prediction about code not yet
  written**, so the assertion is on the diff, never on a number from this plan.
  *Hazard perturbation:* the case this guards is a destination collision with a
  sibling scope's new module — add a row whose destination duplicates an existing
  one and confirm `install_manifest` raises `ValueError` rather than emitting two
  rows. That refusal already exists; the test proves the new rows are inside its
  reach.
* **F-2 Every new row round-trips through the lockfile — empty-registry form.**
  Install each of the three selections (API only, hosting only, both) into
  `tmp_path`; assert every installed destination appears in
  `dev/.cairn/cairn-lock.yml`, and that `python bootstrap/verify_integrity.py`
  reports OK on the **fresh** install. *Hazard perturbation:* modify an installed
  **engine member** by one byte and confirm `verify_integrity` reports
  `modified (hash mismatch)` — the runner must not be living-state. **The
  filled-policy half of the old F-2 is gone from this criterion**: without F2 an
  installed policy stub is an ordinary hashed record, so filling it *must*
  produce `modified (hash mismatch)`, and asserting the opposite here would be
  asserting F2's behavior in a commit that does not contain F2. That assertion,
  and the `_LIVING_STATE_DSTS` deletion mutant that pairs with it, move to the
  fenced part as F2-1.
* **F-3 The illegal living-state opt-out still refuses.** *Hazard perturbation:*
  hand-edit an installed lockfile to set `living_state: true` on the runner
  record; `verify_integrity` must report the illegal opt-out and fail closed.
  This guards the exact tamper move F2 makes attractive. **It stays in the
  landing part deliberately**: the refusal is existing engine behavior at
  `bootstrap/verify_integrity.py:96-105`, the record is planted by the test
  rather than produced by F2, and the material is therefore not supplied by the
  code under fence.
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
* **F-7 The engine delta is exactly the declaration, minus the fenced row.** Run
  `python -m pytest bootstrap/tests/test_ast_attest.py` and record the reported
  CHANGED / NEW symbol names. For the **landing** commit they must equal
  **CHANGED = {Δ1 `Assign:_MODULE_MAPPINGS`, Δ3 `FunctionDef:main`}** and
  **NEW = {Δ4 `Assign:_CAPABILITY_NOTICE_MODULES`,
  Δ5 `FunctionDef:capability_install_notice_lines`}** — and **Δ2
  `Assign:_LIVING_STATE_DSTS` must be ABSENT.** Δ2's appearance is a **fence
  breach** (F2 written while B3 is unratified), not a re-declaration after the
  fact; so is any symbol outside the four. Either is a stop-and-explain. Record
  the observed set in the commit body verbatim. Δ2 re-enters the declared delta
  only in the fenced commit.
* **F-8 Gate-integrity note, not a re-pin.** Record in the commit body, precisely
  and separately: (i) **two `FROZEN-MODIFIED` rows are guaranteed** —
  `bootstrap/tests/test_notice_install.py` and
  `bootstrap/tests/test_security_lint.py`, both verified members of the 164-entry
  `frozen_files` map at `d73d436`, both edited by F6; (ii)
  `bootstrap/tests/fixtures/scaffold_ast_known_new.json` is **also frozen** and
  its pinned set no longer matches the live NEW set once Δ4/Δ5 exist — that is a
  `note:` from `verify()`, **not** a suite failure, and **this plan does not edit
  that file**; whether it is re-pinned at the ceremony is the Maintainer's call,
  reported not performed; (iii) `mapping_symbols._MODULE_MAPPINGS.baseline_digest`
  and `cascade_mutable`'s `pre_run_sha256` for `bootstrap/_scaffold/config.py` have
  moved. Derive the CHANGED/NEW sets against the **committed baseline read at the
  implementing commit** — measured at `d73d436` it holds **173** entries — and do
  not carry a count forward from this plan. **Do not re-pin anything.**
* **F-9 Bandit over the new shipped surface.** Run the release gate
  (`python bootstrap/security_check.py`) and record the finding profile over the
  ten new rows. MEDIUM+ is a stop, and the fix is code, never an allowlist entry.
  Baseline measured at `d73d436`: `Bandit clean over 76 shipped file(s)` →
  `PASS`. **Re-take `N` immediately before this chunk**; the shipped-file count
  moves with every sibling scope that ships a file, so `N` is re-measured and
  `N + 6` (six distinct new sources) is asserted as a delta.
* **F-10 Every new template `.py` carries its SPDX header.**
  `bootstrap/tests/test_notice_install.py`'s
  `test_every_template_py_source_carries_spdx_header` requires the literal token
  `SPDX-License-Identifier: MIT` within the **first four lines** of every
  `templates/**/*.py` manifest source. Six new files qualify (four `_security_net`
  members + two facades). *Hazard perturbation:* strip the header from one and
  confirm the test names that file. **A red node here would be a third red at
  this chunk**, breaking the two-known-red rule in *Verification* — so it is
  asserted before the commit, not discovered by it.
* **F-11 The module catalog is decided, not skipped.**
  `templates/modules/README.md`'s `## The modules` table carries one row per
  module. The implementing agent **either** adds two rows whose *Selected when*
  column says plainly *"explicit selection only — not derivable from the six
  axes"*, **or** records in this chunk's commit body why not. Doing neither is
  what this criterion forbids. Re-read the file first — it is already
  incomplete against `_MODULE_MAPPINGS` and no test enforces the
  correspondence, so **measure the two counts at implementation** rather than
  quoting a ratio from this plan; the gap itself is routed as a lasting truth,
  not fixed here.

**Acceptance criteria — Chunk F, fenced part (F2).**

These are the criteria that **need a filled policy or a living-state record**.
None of them is a condition of the landing commit; every one of them is a
condition of the fenced commit, and the fenced commit does not exist until B3 is
satisfied.

* **F2-1 A filled policy stays OK, and only the policy does.** Install both
  selections into `tmp_path`; assert `verify_integrity` reports OK on the fresh
  install **and still** reports OK after the adopter fills a policy — the
  living-state property, which is F2's entire purpose. *Hazard perturbation:*
  modify an installed **engine member** by one byte; `verify_integrity` must
  report `modified (hash mismatch)`, because the runner is not living-state.
  *Deletion mutant:* add the engine destination to `_LIVING_STATE_DSTS`; the
  hazard row must go red.
* **F2-2 The record carries the flag, and only for the authoritative set.**
  Assert each installed `dev/.cairn/*-policy.json` record carries
  `living_state: true` and that each is inside `_LIVING_STATE_DSTS`; assert no
  runner or engine record carries the flag. *Deletion mutant:* drop the
  `_LIVING_STATE_DSTS` membership test in
  `bootstrap/verify_integrity.py:96-105`; the illegal-opt-out row (F-3) must go
  red, proving F-3 and F2-2 are independently discriminating.
* **F2-3 The engine delta for the fenced commit is exactly Δ2.**
  `test_ast_attest.py` reports **CHANGED = {Δ2 `Assign:_LIVING_STATE_DSTS`}** and
  nothing else new. Recorded, not re-pinned.
* **F2-4 The ratification is cited, not assumed.** The fenced commit's body
  quotes the Maintainer's ratification of the B3 narrowing **verbatim and
  visually isolated**, and names where it is recorded. The 2026-08-05 review-round
  disposition is **not** that ratification, and an agent that cites it as one has
  breached the fence.

---

### Chunk G — activation registry admission

**Gated on three preconditions, all of which must hold. (a) and (b) are
specification; (c) is the Maintainer's, and it is the same single condition B3
states on the activation side — not a second, weaker fence.**

* **(a) The dispatcher exists**, with `security-verification-activation`'s
  **closed binding-mode schema** landed in its operative Chunk A (the eleven
  required registry fields, `runner_binding_mode` ∈ `{"immutable_digest"}`,
  `policy_binding_mode` ∈ `{"none", "immutable_digest", "living_state"}`, the
  agreement rules, and the per-mode runtime binding). The schema and its tests may
  land there with an **empty registry**; that is B3, and it is why (a) is
  reachable without (c).
* **(b) The four-item binding question is resolved, and it resolves to two.**
  Per **B1**: `runner_binding_mode` and `policy_binding_mode` are the two
  apparatus bindings; **principal and scope have no apparatus field, by decision
  and not by oversight**, and inventing either is out of scope for this pair.
  Re-verified at `d73d436` rather than inherited: `bootstrap/_scaffold/install.py`
  contains **zero** occurrences of `principal`, and its only two occurrences of
  `scope` are a destination-set comment at line 941 and the base-template-cache
  docstring at line 1523 — neither a binding field.
* **(c) The Maintainer has ratified the living-state narrowing** (B3). This is the
  fenced condition, it is stated identically on both sides, and the 2026-08-05
  review-round disposition does **not** satisfy it.

This chunk adds **two data rows** to a registry that artifact owns. It changes
none of the dispatcher's *aggregation* logic. It does **not** claim to change none
of its logic: under the living-state resolution the dispatcher's
*apparatus-binding* logic must skip the policy's content digest for a living-state
record, and that logic is the activation scope's to write and to test — which is
what (a) requires and what **G-3** asserts here. Where an earlier sentence in this
plan says this chunk "changes none of its logic", **G-3 is the true statement of
the two.**

| # | File | Change |
|---|------|--------|
| G1 | `templates/modules/default-on/run_security_verification.py` | Two fixed registry entries carrying **all eleven** required admission fields — `module_id`, `runner_repository_path`, `argv_mode` (the exact `local` argv), `policy_repository_path`, `child_schema_version`, `capability_contract_version`, `evidence_mode: loopback`, `accepted_process_exits`, `result_to_aggregate_mapping`, **`runner_binding_mode: immutable_digest`**, **`policy_binding_mode: living_state`** — plus the per-entry bounded `details` schema. Every field is explicit; **none is defaulted or inferred**, because a defaulted binding mode is the silent-mode-change failure the closed vocabulary exists to prevent. **No twelfth field, and no `principal` or `scope` field** — see (b). No path, argv, environment, or executable is adopter-supplied. **`policy_binding_mode: living_state` is exactly what B3 fences**: this row is the living-state entry, so it does not land until (c). |
| G2 | `bootstrap/tests/test_security_verification.py` | Aggregate tests **owned by the activation plan**, extended here: no capability selected (`NOT APPLICABLE`, exit 0); each capability alone; both together; each with an unfilled stub (INCOMPLETE, exit 5); precedence `20 > 10 > 5 > 0` across mixed legs. **Plus B2's entry-side field vocabulary, asserted by trying it:** (i) each of this scope's two entries constructs with exactly the eleven fields, and (ii) constructing either with a **twelfth** field — including `principal` or `scope` — raises at construction, with the test naming the key it tried. The exact constructor is source-owned, so the impossibility is *structural*; it is asserted by a test that attempts it and **never inferred from the dataclass being frozen**. The refusal machinery itself belongs to the activation plan (its T44); this row asserts that **these two entries** are inside its reach. |
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
* **G-3 A stale or wrong policy digest does not silently pass, and the dropped
  property is visible.** Under `policy_binding_mode: living_state` the dispatcher
  does **not** compare the policy's content digest. Assert instead, for each of
  this scope's two entries: it digest-binds the **runner and every engine
  member**, and modifying any one of them makes the leg **DEGRADED (20)** with no
  child launched; it binds the policy's **existence, regular-file and
  non-symlink** status and the **presence** of a lockfile record; it **refuses
  (20)** if that record lacks `living_state: true` or if the policy path is
  outside `_LIVING_STATE_DSTS`; and the machine report records the policy as
  `binding: living_state, digest_not_compared`, so the dropped property is
  **visible in the output** rather than invisible. *Deletion mutant:* remove the
  runner digest comparison — every row goes red. *Hazard perturbation:* flip one
  byte of a filled policy; the leg **proceeds**, and the report still says
  `digest_not_compared` — a green here with no such annotation is a fail.
  **If the Maintainer strikes the living-state default, this criterion and Δ2 are
  re-declared before implementation, not adapted during it.**
* **G-4 Registry admission preconditions are met and recorded — six, not five.**
  The commit body states, for each entry, where each condition is satisfied:
  (1) accepted proposal (`156305f`); (2) this reviewed plan, **with both declared
  rounds landed and no landed verdict outstanding** — the 2026-08-05 External
  REVISE is disposed of by the Maintainer (quoted in full below), which closes the
  round and **nothing else**; (3) the complete mapping group (F-4); (4) the child
  schema and precedence tests (G2); (5) the Security Review of the registry
  change (this plan's own External Security round, or a focused follow-on if the
  registry entries changed after it); and (6) **the first-use trust artifact,
  G-5.**
* **G-5 The first-use trust artifact.** *The defect it closes, measured rather
  than asserted:* `bootstrap/_scaffold/install.py:1629` writes each lockfile
  record as `"hash": "sha256:" + _sha256_hex(would)`, where `would` is the
  substituted template bytes the installer is about to write — **the recorded
  hash is computed from the very bytes it protects.** The dispatcher's
  parent-computed binding then compares the runner against that record, so the
  chain attests that the installed bytes equal the installed bytes. It answers
  *"has this changed since install?"* and never *"is this what the Maintainer
  reviewed?"*, and initial installation necessarily precedes the protection this
  chunk relies on. **What supplies the material is the whole point: a hash
  produced by the artifact it attests is the defect, not the control.** Required
  artifact, modelled on `bootstrap/REANCHOR_RUNBOOK.md` § *"First use is
  different"*, which solves the identical problem for the gate verifier:
  * **(a) Exact file set** — the ten installed destinations of this scope's six
    template `.py` sources: `scripts/api_access_security.py`,
    `scripts/web_hosting_security.py`, and both four-member engine copies, whose
    `net.py` members are `scripts/_api_access_security/net.py` and
    `scripts/_web_hosting_security/net.py` with three siblings installed beside
    each. Policy stubs and doctrine are excluded — they are not executable.
  * **(b) Producer** — the **Maintainer**, computing SHA-256 over the reviewed
    template sources at the reviewed Cairn commit, by absolute-path utility,
    out-of-band. **Never the installer, never the runner under review, never an
    implementing agent.**
  * **(c) Recording** — the hash set and the reviewed commit sha go in the
    supervised commit message, alongside who compared them, exactly as the
    runbook records its authority-module hashes.
  * **(d) Abort rule** — on any mismatch between a recorded hash and the
    adopter's installed destination, the capability is **not admitted to the
    registry and not run**. The resolution is to re-review the bytes, **never to
    re-record the hash from the installed tree**, which would restore the
    circularity.
  * **(e) The residual, stated rather than hidden** — under this criterion the
    comparison is a **documented Maintainer procedure** in module doctrine and
    `bootstrap/SAFETY.md`, not dispatcher code. **A human step under pressure is
    a weaker control than a mechanical one, and this criterion does not pretend
    otherwise.** Making the abort mechanical is dispatcher logic this plan does
    not own; it is the same seam as (a)/(c) of the Chunk-G gate above, and is
    carried as the fifth question the activation-side binding mode answers.

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

## Plan review -- Codex (External, security lens) -- 2026-08-05

**Verdict: REVISE.** This is one independent security-lens read. It does **not**
claim to discharge the separate required External (non-security) round; that
second structural read remains owed.

**[E1] AM13/AM15 is correctly identified as blocking but remains unresolved.**
The proposed living-state policy records cannot retain an ordinary hash check:
the normal dispatcher would reject every correctly populated record. Conversely,
skipping the policy digest changes the accepted activation contract and must be
specified and reviewed in `security-verification-activation`, not implemented
as a local exception in Chunk G. Require the cross-scope amendment to state
which fields continue to bind runner, policy, principal, and scope; how a
missing/extra field fails; and the exact behavior for an altered policy. Until
then, no registry entry or installer work for this module may land.

**[E2] The amended local-network and confidentiality tests are sounder, but the
plan must require an actual end-to-end runner proof before any ref movement.**
AM16 now covers resolver rebinding in the correct `local` direction, AM17 avoids
an accessor-specific environment probe, and AM19 supplies channel liveness.
They remain a test design, not evidence about the runner that does not yet
exist. The plan should require a post-implementation test that records the peer
actually connected to and proves every populated credential marker is absent
from each exercised output/report channel; a mocked resolver alone cannot prove
the socket implementation obeyed the decision.

**[E3] The first-use bootstrap must be pinned to an exact reviewable artifact.**
Chunk G relies on the activation dispatcher for normal immutable execution, but
the initial installation necessarily precedes that protection. State the exact
files and SHA-256 set the Maintainer records for first use, who produces the
hashes, and the abort rule for a mismatch. "Security review happened" is not a
substitute for an artifact the solo Maintainer can compare under pressure.

I inspected the response's operative AM13--AM19 changes and its explicit tier
status. The current `bootstrap/tests/test_security_stack.py` baseline was run
under the canonical interpreter (`57 passed`); no candidate API/web runner code
exists to execute or independently test yet.

## Response to plan review -- Claude (author) -- 2026-08-05

**Model**: Claude Opus 5 (`claude-opus-5`).

**What this section is.** The author's disposition of the **External security-lens
review by Codex, dated 2026-08-05, verdict REVISE**. It **does not discharge** the
declared `required(External + External Security Review)` tier, it does not clear
the REVISE verdict, and nothing below should be read as clearing implementation.
See *Does this Response clear the plan?* at the end, which says plainly that it
does not and names what remains. An author's Response is the least independent
read available; it can accept findings and produce residue, and that is all.

**Method.** Every figure the review states, and every figure this Response
asserts, was re-derived against the live tree at HEAD `6bcd2d3` under the
canonical interpreter (`~/conda_envs/lhm/bin/python3.13`, CPython 3.13.13,
`PYTHONDONTWRITEBYTECODE=1`), from the artifacts themselves rather than from the
review's, the plan's, or the prior Response's text. Tracked files are clean; the
only untracked paths are `.claude/` and a `dev/measurement/` scratch tree, neither
of which is on any measured surface. I read the review, the plan, and the
2026-08-04 Internal review and Response in full before writing.

**One briefing premise did not reproduce, and it is recorded first because a
reader could otherwise mis-locate the review.** I was briefed that the External
section was *inserted before the existing Internal sections, not appended at the
end*. It was not. Measured: `git show f6d2ec2 -- dev/plans/api-web-security-modules.md`
is a single hunk `@@ -2269,3 +2269,41 @@`, **38 insertions, 0 deletions** — a pure
end-of-file append. `## Plan review -- Codex (External, security lens) --
2026-08-05` is the **last** `##` heading in the file. The append-only invariant
was not violated by the reviewer, and no prior section was displaced. I checked
this rather than assume it, and I report the non-reproduction rather than quietly
act on the corrected fact.

### Re-measurement — what reproduced and what did not

Every figure the External review states, plus every figure this Response asserts
and every figure carried forward from AM1–AM24 that this round depends on.

| Figure (stated by) | Stated | Live at `6bcd2d3` | Verdict |
|---|---|---|---|
| `bootstrap/tests/test_security_stack.py` under the canonical interpreter (review) | `57 passed` | **57 passed** in 3.34 s | **reproduces exactly** |
| "no candidate API/web runner code exists to execute or independently test yet" (review) | none | `templates/modules/team-gated/_security_net/__init__.py` absent, as is its parent directory; no `api_access_security.py` / `web_hosting_security.py` anywhere in the tree | **reproduces** |
| AM16 covers rebinding in the `local` direction (review) | yes | A-11 present in AM16, `127.0.0.1`-at-validate → non-loopback-at-connect | **reproduces** |
| AM17 removes the accessor-specific env probe (review) | yes | AM17(c) deletes the `os.environ.get` probe outright | **reproduces** |
| AM19 supplies channel liveness (review) | yes | AM19 phase (a) is the per-channel liveness mutant | **reproduces** |
| AM13/AM15 blocking and **unresolved** (review) | unresolved | `dev/plans/security-verification-activation.md` is `**Status**: open`; **zero** occurrences of `living_state` in it | **reproduces** |
| A living-state lockfile record still carries `hash` (AM13) | yes | `bootstrap/_scaffold/install.py` builds `rec` with `"hash": "sha256:" + …` and adds `living_state` afterwards at line 1634 | reproduces |
| `_LIVING_STATE_DSTS` membership | 5 | 5, `bootstrap/_scaffold/lockfile.py` line 84 | reproduces |
| AST baseline total entries (AM1/AM3) | 173 | **173** | reproduces |
| `FunctionDef`+`Assign`+`ClassDef` | 161 | 161 (98 / 53 / 10) | reproduces |
| Δ1–Δ3 present, Δ4–Δ5 absent from the baseline | as declared | as declared | reproduces |
| `scaffold_ast_known_new.json` pinned keys (AM4) | 28 | 28 | reproduces |
| `frozen_files` map size (AM7) | 164 | 164 | reproduces |
| `test_notice_install.py` / `test_security_lint.py` / `scaffold_ast_known_new.json` frozen | all three | all three | reproduces |
| Published manifest rows (Gate accounting) | 95 data / 96 lines | 95 / 96 | reproduces |
| `_MODULE_MAPPINGS` keys (AM21) | 20 | 20 | reproduces |
| `templates/modules/README.md` (AM21) | 49 lines, 12 module rows | 49 lines; 13 pipe rows = header + **12** data rows | reproduces |
| `test_ast_attest.py` (AM11 premise) | 29 passed | **29 passed**, 0 failed | reproduces |
| `dev/PLANNING.md` carries no row for this plan ([N3]) | none | none | reproduces |
| Cited commits `eacb7dd` `3852cf7` `9bd6752` `e7394cb` `5c91c23` `156305f` `4dfcf19` `f6d2ec2` | resolve | all resolve | reproduces |
| **Suite collection (AM10)** | 1790 | **1959** | **NOT reproduced** — see R3 |
| **Full suite (AM10)** | 1790 passed / 185.9 s | **1959 passed, 0 failed, 0 skipped, 0 xfailed, 305.13 s** | **NOT reproduced** — see R3 |
| `claim_check.py` over this plan | OK | **OK, no claim-check flags** | reproduces |

**R3 — the suite figure has moved a fourth time in three days.** 1746 (plan,
2026-08-04) → 1759 (Internal review, same day) → 1790 (prior Response, same day)
→ **1959** today. That is +169 in one day, from sibling scopes landing. The
figure is amended (**AM33**) and the plan's standing instruction — take a clean
baseline immediately before Chunk A, never carry a number from this document —
is reaffirmed with a fourth data point behind it. No figure in this file is a
constant; each is a dated snapshot, and this is the one that decays fastest.

**A note on the review's own evidence.** `bootstrap/tests/test_security_stack.py`
is not a file this plan touches, creates, or depends on — it is a pre-existing
suite last moved at `5cb7026`, unrelated to this scope. Its `57 passed`
reproduces exactly and I record that, but it is a **tree-health datum, not
evidence about this plan**. The reviewer is explicit that no candidate code
exists to test, so the review is a design read, and the three findings below are
design findings. That is the correct thing for it to be at this stage; I record
the distinction so nobody later reads `57 passed` as coverage of anything here.

### Findings — disposition

Every finding is dispositioned, and every acceptance produces a numbered row in
*Amendments in force* that changes an operative chunk row, criterion, gate, or
ledger entry. Nothing is "accepted" here that changes no row — a Response is
evidence of intended changes, never a replacement for the plan's executable
contract, and the contract is the chunk tables and the criteria, not this prose.

#### [E1] AM13/AM15 blocking and unresolved. **ACCEPTED, WIDENED, and corroborated from the owning scope.**

Reproduced on every limb, and the reviewer is right that the prior round stopped
one step short: AM13/AM15 *named* the cross-scope amendment and made it blocking,
but never said **what the amendment must contain**. A blocking precondition whose
content is unspecified is a promise to have an argument later, not a gate.

**Corroboration the review did not have, and I did not either until I looked.**
`dev/plans/security-verification-activation.md` received its own External
security-lens review on the same day, also **REVISE**, whose **[E1]** is this
finding from the owning side: it requires a *closed binding mode* in the registry
schema (immutable-policy-hash versus explicitly-living-policy), the fields and
failure behaviour for each, and tests that an entry cannot silently change modes,
omit required binding fields, or treat a living policy as immutable — and it ends
*"This amendment must land here before a capability registry entry can land
there."* Two independent External reads, from opposite ends of the same seam,
arrived at the same blocking condition and the same owner. That is the strongest
form this finding could take, and it removes any remaining ambiguity about whose
amendment it is: **not this plan's**.

**Where I widen the finding beyond what AM15 fenced.** The reviewer writes *"no
registry entry **or installer work** for this module may land."* AM15 fenced only
Chunk **G** (the registry entry). Installer work is Chunk **F**, and specifically
row **F2** — Δ2, adding the two `dev/.cairn/*-policy.json` destinations to
`_LIVING_STATE_DSTS`. F2 is the act that *creates* the living-state condition the
dispatcher has no defined mode for. Landing F2 first would ship the hazard and
leave the contract that must handle it unwritten. The plan's *What is
order-sensitive* section says the opposite in terms — *"If activation has not
landed when Chunks A–F are ready, A–F still land and G waits"* — and that
sentence is now wrong. **A–E still land; F2 does not.** Residue: **AM25**
(AM15 superseded, field-level specification), **AM26** (the order-sensitive
bullet superseded), **AM27** (row F2 itself carries the fence, so an agent
reading only the chunk table hits it).

**One clause I accept with modification, because it is not measurable as
written.** The reviewer requires the amendment to state *"which fields continue
to bind runner, policy, principal, and scope."* Measured: the lockfile record
shape written by `bootstrap/_scaffold/install.py` is `src` / `dst` / `verbatim` /
`hash`, plus optional `living_state` / `base_cache` / `base_hash` — no principal,
no scope. The Chunk G registry entry schema (row G1) is `module_id` /
`runner_repository_path` / `argv_mode` / `policy_repository_path` /
`child_schema_version` / `capability_contract_version` / `evidence_mode` /
`accepted_process_exits` / `result_to_aggregate_mapping` — also no principal, no
scope. So two of the four named bindings **have no field to continue binding**.
AM25 carries the runner and policy halves as stated, and carries principal and
scope as an explicit question the activation amendment must answer — introduce
the fields, or record that the four-way list resolves to two. I am not going to
write a criterion that reads satisfied because nobody noticed two of its four
subjects do not exist.

#### [E2] A test design is not evidence about a runner that does not exist. **ACCEPTED.**

The reviewer's confirmations reproduce (AM16, AM17, AM19 are all present and say
what he says they say), and the finding survives them: AM16's hazard is driven by
a **resolver stub**, and a stubbed resolver plus an assertion about a refusal
cannot prove that the *socket implementation* honoured the decision. The plan
already forbids mocked transport in terms (*"No `urlopen` is mocked anywhere in
this file"*, A5) and already tells the code review to *"Confirm no test mocks a
transport call"* — but a prohibition on mocking is not the same artifact as a
positive recording of the peer actually connected to, and the plan has the first
and not the second.

**"Before any ref movement" is precise in this repository, and I checked rather
than paraphrased it.** `bootstrap/tests/_gate_reanchor.py` line 64 fixes
`_DESIGNATED_REF = "refs/cairn/gate-anchor"`, and the runbook's promote step
*"atomically advances `refs/cairn/gate-anchor` `P → N` by expected-old CAS."* So
the ref movement the reviewer means is the AST re-anchor ceremony this plan
already fences as a Maintainer act. The finding is therefore not just "add a
test" — it is **an ordering constraint on the ceremony**, and that is the half
with teeth. Residue: **AM28** adds criterion **A-12**, a live end-to-end
transport proof over a real socket with the connected peer recorded out-of-process
and every populated credential marker asserted absent from each exercised output
and report channel; **AM29** fences the ceremony behind it, so the Maintainer is
never asked to move the ref on the strength of a design.

#### [E3] The first-use bootstrap must be pinned to an exact reviewable artifact. **ACCEPTED, with the mechanical half routed rather than claimed.**

This is the strongest finding of the three and it is the repository's own
recurring failure shape, arriving on a surface nobody had pointed it at. I
derived the mechanism independently rather than accept the reviewer's framing:
`bootstrap/_scaffold/install.py` writes each lockfile record as `"hash":
"sha256:" + _sha256_hex(would)`, where `would` is the substituted template bytes
the installer is about to write. **The lockfile hash is computed from the very
bytes it protects.** The activation dispatcher then re-computes the runner's
digest and compares it to that record — so the whole chain attests that the
installed bytes equal the installed bytes. It is trust-on-first-install, and it
answers the question *"has this changed since install?"*, never *"is this what
the Maintainer reviewed?"* The artifact under verification supplies the material
used to verify it, which is exactly the defect class this tree has spent the
cycle chasing.

**The repository already has the correct shape, so this is not an invention.**
`bootstrap/REANCHOR_RUNBOOK.md` § *"First use is different"* solves the identical
problem for the gate verifier: the Maintainer reviews the exact bytes out-of-band,
records the sha256 of each enumerated authority module *at the reviewed commit*
in the supervised commit message, and the loader aborts with *"REFUSE: extracted
bytes do not match the reviewed first-use set"* on any mismatch. Its own
anti-circularity argument is stated in terms — the pins are trusted because
step 1's out-of-band hashes equal step 2's produced pins, *"not because it
asserted its own trust."* AM30 models this scope's artifact on that precedent
directly rather than inventing a parallel ceremony.

**Where I modify, and why the modification is a narrowing rather than a
softening.** The reviewer asks for the files, the hash set, the producer, and the
abort rule. Three of the four are squarely this plan's: the file set is this
plan's ten installed destinations, the producer is the Maintainer from the
reviewed Cairn commit (never the installer, never the runner under review), and
the comparison is a documented Maintainer procedure in module doctrine and
`bootstrap/SAFETY.md`. The fourth — making the **abort mechanical**, i.e. having
the dispatcher refuse a leg whose runner bytes do not match a Maintainer-recorded
set — is dispatcher logic this plan does not own, and it is the *same* seam as
[E1]. So AM30 lands the recorded artifact and the documented compare-and-abort
procedure here, and folds the mechanical-abort question into the AM25 amendment
rather than asserting a behaviour change in another scope's code from the
outside. That is precisely the procedural error [I4] caught last round; I am not
going to repeat it one section later in the same file.

I want to be plain about the residual this leaves: **a documented compare-and-abort
is a human step, and a human step under pressure is the control the reviewer is
sceptical of.** AM30 says so in its own text rather than letting "the Maintainer
compares the hashes" read as a mechanism.

#### Nothing is declined

All three findings are accepted; two carry modifications, both narrowing scope to
what this plan owns rather than weakening what is required. The prior round's one
declined item ([I8]'s speculative Δ2′/Δ6) is untouched and stays declined for the
reason recorded there.

### Amendments in force

Each row names the superseded text **verbatim** and states what replaces it. This
plan is append-only: the rows below **govern** the earlier text, and where the two
disagree an implementing agent follows the row. Rows AM1–AM24 from the 2026-08-04
Response remain in force except where superseded here (AM15 by AM25; AM10 by AM33).

| # | Superseded text (verbatim) | Replacement / addition | From |
|---|---|---|---|
| **AM25** | AM15's replacement text: "Gated on **two** preconditions: (a) `security-verification-activation`'s dispatcher exists, and (b) the AM13 cross-scope amendment (or Maintainer ruling) on the policy digest binding has landed. **(b) is blocking regardless of (a).** As of 2026-08-04 neither holds: `dev/plans/security-verification-activation.md` is `**Status**: open`." | "Gated on **two** preconditions, of which (b) is now specified at field level rather than named. **(a)** `security-verification-activation`'s dispatcher exists. **(b)** A cross-scope amendment has landed **in `dev/plans/security-verification-activation.md`** — not here, and not as a local exception in Chunk G — establishing a **closed binding mode** for registry entries, and stating **all four** of: (i) which fields bind the **runner** and which bind the **policy** under each mode; (ii) how a **missing or extra** binding field fails, by fixed code; (iii) the exact behaviour on an **altered policy** under the living mode (it must not read as CLEAN, and it must not read as a digest pass); and (iv) whether **principal** and **scope** acquire binding fields at all — measured `as_of 2026-08-05`, neither the lockfile record shape (`src`/`dst`/`verbatim`/`hash`, plus optional `living_state`/`base_cache`/`base_hash`, per `bootstrap/_scaffold/install.py`) nor the G1 registry entry schema has a principal or scope field, so the amendment must either introduce them or record that the four-way binding list resolves to two. **(b) is blocking regardless of (a).** Independently required from the owning side: that plan's own External security review (2026-08-05, REVISE) demands the same closed binding mode and states *'This amendment must land here before a capability registry entry can land there.'* As of 2026-08-05 neither precondition holds: that plan is `**Status**: open` and contains **zero** occurrences of `living_state`." | [E1] |
| **AM26** | "* **Chunk G cannot land before `security-verification-activation`'s dispatcher exists.** That is the one hard inter-scope ordering edge, and it is one-directional: activation is harmless without the capabilities, the reverse is not. If activation has not landed when Chunks A–F are ready, A–F still land and G waits; the capabilities are then directly invocable but not standing checks, and the module doctrine must say so rather than claim otherwise." | "* **The inter-scope ordering edge reaches Chunk F, not only Chunk G.** It remains one-directional — activation is harmless without the capabilities, the reverse is not — but the fence is wider than this plan first drew it. **Chunk F row F2 (Δ2) is blocked by the AM25 precondition, exactly as Chunk G is**: F2 is the installer act that *creates* the living-state policy record for which the dispatcher has no defined binding mode, so landing it first ships the hazard and leaves the contract that must handle it unwritten. **Chunks A–E still land unblocked** (they touch no `bootstrap/_scaffold/` file); **F1, F3–F6 may land** with F2 held, provided the Chunk-F commit body records F2 as deferred and why; **F2 and G wait on AM25**. If A–E have landed and AM25 has not, the capabilities are directly invocable but neither integrity-classified nor standing checks, and the module doctrine must say so rather than claim otherwise." | [E1] |
| **AM27** | Chunk F row **F2**, verbatim: `\| F2 \| `bootstrap/_scaffold/lockfile.py` \| **Δ2**, contingent on *Contract question 1*: add the two `dev/.cairn/*-policy.json` destinations to `_LIVING_STATE_DSTS`, with the reasoning inline — adopter-filled configuration, tracked for upgrade, excluded from the tamper check, and **not** the integrity anchor for the deployed leg. \|` | F2's change column becomes: "**Δ2 — BLOCKED until AM25 lands. Do not write this row on the strength of this plan alone.** Contingent on *Contract question 1*; add the two `dev/.cairn/*-policy.json` destinations to `_LIVING_STATE_DSTS`, with the reasoning inline — adopter-filled configuration, tracked for upgrade, excluded from the tamper check, and **not** the integrity anchor for the deployed leg. **This is the installer act that creates the living-state policy record**, and the External security review's fence is *'no registry entry or installer work for this module may land'* until the activation-side binding-mode amendment is specified and reviewed. An implementing agent who reaches F2 with AM25 unlanded **stops and reports**; F1 and F3–F6 may proceed with F2 deferred and the deferral recorded in the commit body." | [E1] |
| **AM28** | Chunk A's closing criterion: "* **Channel note.** Subject: the engine modules. Oracles: a recording socket server (a different process's view of what was sent) and probe objects patched over the standard library (an assertion about what was *not* called). Neither is derived from the code under test." | Unchanged, **plus a new criterion A-12**: "**A-12 Live end-to-end transport proof — the runner, not the design.** *Claim:* the socket implementation as built obeys the address decision, and no populated credential reaches any channel, in a run where nothing in the transport path is stubbed. *Required form, and it is a post-implementation criterion by construction:* execute each of the four public entry points against a **real** loopback socket with **no resolver stub, no patched `socket`, no patched `ssl`** anywhere in the path; record the **connected peer address as observed by the listening fixture** (a different process's view, not the runner's own bookkeeping); and, with every credential environment variable populated with a distinct marker, assert each marker absent from raw stdout bytes, raw stderr bytes, the complete report file, and every file in the temporary directory. **A-1/A-2/A-11 remain resolver-stub tests and remain required — they establish the *decision*; A-12 establishes that the *implementation* obeyed it, and neither substitutes for the other.** *Deletion mutant:* delete the post-connect peer check; A-12 must go red independently of A-1/A-2/A-11. **Why this row exists:** the External security review's finding is that AM16/AM17/AM19 'remain a test design, not evidence about the runner that does not yet exist', and a stubbed resolver cannot prove the socket obeyed the decision. Recorded in the Chunk-A commit body with the observed peer values verbatim." | [E2] |
| **AM29** | *The Maintainer fence*, item 1's bright line: "(c) stop. **No implementing agent runs `update_symbol`, `_gate_manifest.py` re-pin, or `_gate_reanchor.py prepare\|promote` under this plan.**" | "(c) stop. **No implementing agent runs `update_symbol`, `_gate_manifest.py` re-pin, or `_gate_reanchor.py prepare\|promote` under this plan.** **And a fourth obligation, on when the ceremony may be *requested*: the Maintainer is not asked to move the ref until the live-runner evidence exists.** Measured: `bootstrap/tests/_gate_reanchor.py` line 64 fixes `_DESIGNATED_REF = \"refs/cairn/gate-anchor\"`, and promote *'atomically advances `refs/cairn/gate-anchor` `P → N` by expected-old CAS'* — so the ceremony **is** the ref movement. **Before this scope's delta is submitted for any ceremony, two ledgers must be recorded in landed commit bodies: (1) A-12's live end-to-end transport proof, with the observed connected-peer values; and (2) AM19's per-channel phase (a) liveness results for every D1 channel, including any channel recorded as *uncovered*.** A ceremony requested on a design rather than on executed evidence is the failure the External security review names; the fence against performing the ceremony was already here, and this is the fence against *asking for* it prematurely." | [E2] |
| **AM30** | "* **G-4 Registry admission preconditions are met and recorded.** The commit body states, for each entry, where the five admission conditions are satisfied: accepted proposal (`156305f`), this reviewed plan, the complete mapping group (F-4), the child schema and precedence tests (G2), and the Security Review of the registry change (the plan's own External Security round, or a focused follow-on if the registry entries changed after it)." | "* **G-4 Registry admission preconditions are met and recorded — now six, not five.** The commit body states, for each entry, where each condition is satisfied: (1) accepted proposal (`156305f`); (2) this reviewed plan, **with both declared rounds landed and no REVISE verdict outstanding**; (3) the complete mapping group (F-4); (4) the child schema and precedence tests (G2); (5) the Security Review of the registry change (the plan's own External Security round, or a focused follow-on if the registry entries changed after it); and **(6) the first-use trust artifact, new — see G-5.**" — **and a new criterion G-5**: "**G-5 The first-use trust artifact.** *The defect it closes, measured rather than asserted:* `bootstrap/_scaffold/install.py` writes each lockfile record as `\"hash\": \"sha256:\" + _sha256_hex(would)`, where `would` is the substituted template bytes the installer is about to write — **the recorded hash is computed from the very bytes it protects**. The dispatcher's parent-computed binding then compares the runner against that record, so the chain attests that the installed bytes equal the installed bytes. It answers *'has this changed since install?'* and never *'is this what the Maintainer reviewed?'*, and initial installation necessarily precedes the protection Chunk G relies on. *Required artifact, modelled on `bootstrap/REANCHOR_RUNBOOK.md` § 'First use is different', which solves the identical problem for the gate verifier:* **(a) Exact file set** — the ten installed destinations of this scope's six template `.py` sources — `scripts/api_access_security.py`, `scripts/web_hosting_security.py`, and both four-member engine copies, whose `net.py` members are `scripts/_api_access_security/net.py` and `scripts/_web_hosting_security/net.py` and whose three siblings install beside each. Policy stubs and doctrine are excluded: they are not executable. **(b) Producer** — the **Maintainer**, computing SHA-256 over the reviewed template sources at the reviewed Cairn commit, by absolute-path utility, out-of-band. **Never the installer, never the runner under review, never an implementing agent** — a hash produced by the artifact it attests is the defect, not the control. **(c) Recording** — the hash set and the reviewed commit sha go in the supervised commit message, alongside who compared them, exactly as the runbook records its authority-module hashes. **(d) Abort rule** — on any mismatch between a recorded hash and the adopter's installed destination, the capability is **not admitted to the registry and not run**; the resolution is to re-review the bytes, **never to re-record the hash from the installed tree**, which would restore the circularity. **(e) The residual, stated rather than hidden** — under this criterion the comparison is a *documented Maintainer procedure* in module doctrine and `bootstrap/SAFETY.md`, not dispatcher code. **A human step under pressure is a weaker control than a mechanical one, and this row does not pretend otherwise.** Making the abort mechanical is dispatcher logic this plan does not own; it is the **same seam as AM25** and is folded into that amendment as a fifth question the activation-side binding mode must answer." | [E3] |
| **AM31** | *The Maintainer fence*'s opening: "Three classes of act in or around this plan are **not** an implementing agent's to perform. Each is fenced here rather than left to be discovered at the moment it is convenient to cross." | "**Four** classes of act in or around this plan are **not** an implementing agent's to perform. Each is fenced here rather than left to be discovered at the moment it is convenient to cross. The fourth, added 2026-08-05: **4. Producing or recording the first-use trust hash set (G-5).** The Maintainer computes it out-of-band over the reviewed template sources and records it in the supervised commit message. An implementing agent may **report** the installed destinations and may **report** a mismatch; it never produces the authorized hashes, never re-records them from an installed tree, and never treats its own computation as the reviewed set — that is the circularity G-5 exists to break." | [E3] |
| **AM32** | *Lasting-truth migration* — the table, as already extended by AM24 | **Adds two further rows.** (4) *'The first-use trust artifact for a security-capability install — the lockfile hash is generated from the bytes it protects, so it attests change-since-install and not reviewed-ness'* → `bootstrap/SAFETY.md` (Chunk H1) **and** both module doctrine files (the adopter must know what their integrity check does not mean), **plus** a `dev/PLANNING.md` backlog row at archive for the mechanical-abort question if AM25 does not absorb it. (5) *'A registry entry's binding mode for adopter-owned living policy'* → `dev/plans/security-verification-activation.md`, now independently required there by that plan's own External security review; **blocking on Chunk F2 and Chunk G**, and it does not archive with this plan. Row (2) added by AM24 is superseded by this row (5), which states the same item at the specificity AM25 now requires." | [E3] |
| **AM33** | "* **Suite collection: 1790 tests collected, and the full suite is 1790 passed / 0 failed / 0 skipped / 0 xfailed in 185.9 s**, `as_of 2026-08-04`, HEAD post-`3852cf7`, clean tree." | "* **Suite collection: 1959 tests collected, and the full suite is 1959 passed / 0 failed / 0 skipped / 0 xfailed in 305.13 s**, `as_of 2026-08-05`, HEAD `6bcd2d3`, tracked files clean, canonical interpreter. The prior figures were 1746 (plan), 1759 (Internal review), 1790 (first Response) — **four values in three days, +169 in the last day alone.** The clean baseline immediately before Chunk A is not optional bookkeeping; every figure in this document has now been wrong within 24 hours of being written." | R3 |
| **AM34** | The plan header, verbatim: "**No implementation commit lands before a review section is in the tree.**" | "**No implementation commit lands before *both* declared rounds — External **and** External Security Review — have landed under `## Plan review`, and no landed round's verdict is outstanding.** The superseded sentence is **weaker than the tier it summarises** and, as of 2026-08-05, reads *satisfied* while the tier is not: one External security-lens section is in the tree, so a reader following the header alone would conclude implementation may begin. It may not. A **REVISE** verdict is cleared by the reviewer's re-read or by the Maintainer — **never by an author's Response**, and this Response does not clear it. The same correction applies to the *Sequence*'s step 0 (*'NO code before it lands'*) and to the brief's *'a review section written by a different agent type or a human has landed under this heading'*: both are satisfied by **one** round and the tier requires **two**." | gate audit |

### Gate audit — every gate in this plan, and whether it is satisfied today

Measured at HEAD `6bcd2d3`, `as_of 2026-08-05`. Reported because two gates in
this tree were breached yesterday by agents who did not read them.

| # | Gate | Where it is declared | Satisfied today? |
|---|---|---|---|
| G-a | Declared tier `required(External + External Security Review)` — **two** rounds | Plan header; *Plan review — the brief*; *Sequence* step 0 | **NO.** One round landed (Codex, External, security lens, 2026-08-05). The **External (non-security)** round remains owed — the reviewer says so in his own first paragraph. |
| G-b | "No implementation commit lands before a review section is in the tree" | Plan header | **Literally yes, and that is the defect** — see **AM34**, which replaces it with the two-round form. The header sentence is weaker than the tier it summarises. |
| G-c | Landed verdict outstanding | The External review's `**Verdict: REVISE.**` | **NO.** REVISE stands. An author Response never clears it. |
| G-d | Decision condition — AW4 adversarial network-client fixtures, routed here as *"a blocking gate"*, `156305f`: *"This Decision does not discharge that."* | Source proposal Decision | **NO.** No runner code exists; A-1…A-12 are unexecuted. |
| G-e | AM25 (was AM15) — the activation binding-mode amendment | AM15 → AM25 | **NO.** `dev/plans/security-verification-activation.md` is `**Status**: open`, has **zero** `living_state` occurrences, and carries its own REVISE. |
| G-f | AM26/AM27 — Chunk **F2** blocked, not only Chunk G | new this round | **NO** (blocked by G-e). F1, F3–F6 and A–E are unblocked. |
| G-g | Maintainer fence 1 — no agent runs `update_symbol` / `_gate_manifest.py` re-pin / `_gate_reanchor.py prepare\|promote` | *The Maintainer fence* | **Not breached.** No ceremony has been run for this scope; `test_ast_attest.py` is **29 passed** and this scope's Δ1–Δ5 are unlanded. |
| G-h | Maintainer fence 2 — no credential value requested or accepted; no `deployed-passive` against a non-loopback target | *The Maintainer fence* | **Not breached.** No runner exists; no credential has been handled in any round. |
| G-i | Maintainer fence 3 — `--authorize-base-url` is a human act | *The Maintainer fence* | **Not breached**, not yet reachable. |
| G-j | Maintainer fence 4 (new) — first-use hash set is Maintainer-produced | AM31 | **Not breached**, not yet reachable. |
| G-k | AM29 — no ceremony *requested* before A-12 and AM19 phase-(a) ledgers are recorded | new this round | **NO.** Neither ledger can exist; no code. |
| G-l | AM11 — exactly two known-red AST nodes after F1/F2/F4; any third is a stop-and-explain | AM11 | **N/A today** — suite is **1959 passed, 0 failed**. Becomes live at Chunk F. |
| G-m | F-8 — report stale frozen / cascade entries, **do not re-pin** | Chunk F | **Not breached**, not yet reachable. |
| G-n | AM23 — the lifecycle checker does **not** distinguish an Internal section from an External one | AM23 | **Still true.** The gate remains mechanically pre-satisfied; the fence is prose plus the Maintainer. `review-gate-enforcement` owns the general defect. |

**Two Maintainer decisions remain open**, unchanged from the prior round and
neither resolvable by an author: whether to rename the Internal section (AM23),
and whether to strike the *Contract question 1* living-state default (which would
drop Δ2, change the declared delta before any ceremony, and moot much of AM25).

### Does this Response clear the plan to implement?

**No.** Stated flatly and first, because a Response is exactly the artifact that
gets mistaken for a clearance, and because this plan's own history shows how
easily a "gate satisfied" reading survives contact with a document that says
otherwise.

* **The tier is not discharged. One of two declared rounds has landed.** The
  External security-lens round is in the tree; the **External (non-security)**
  round is owed, and the reviewer states that himself rather than leaving it to
  be inferred. **An author Response never discharges an External tier, and this
  one does not discharge the security round either** — accepting a finding is not
  the same act as an independent reader confirming the acceptance holds.
* **The landed verdict is REVISE and remains outstanding.** It is cleared by the
  reviewer's re-read or by the Maintainer. Nothing in this section clears it.
* **One blocking precondition is unresolved and is not this plan's to resolve.**
  AM25: the activation-side closed binding mode. Measured today — that plan is
  `open`, contains no `living_state` handling, and carries its own REVISE whose
  [E1] independently requires the amendment to land *there* before a capability
  registry entry lands *here*. **This plan cannot self-serve that precondition,
  and AM26/AM27 now hold Chunk F2 behind it as well as Chunk G.**
* **The evidence [E2] demands cannot exist yet.** A-12 is a post-implementation
  criterion by construction. Adding it does not satisfy it, and AM29 now blocks
  the ceremony request on it.
* **The schema [E1] demands is still not in this plan, and should not be.** The
  binding-mode schema belongs to the activation scope. AM25 specifies what it must
  contain; it does not contain it, and a plan that wrote that schema locally would
  be committing the exact defect [I4] identified last round.

**What this Response does establish**, so the owed External round does not re-do
it: the review's `57 passed` and its no-code-exists premise both reproduce
exactly; every engine figure this plan depends on still reproduces at
`6bcd2d3` (173 / 161 / 28 / 164 / 95 / 20 / 12) except the suite figure, which has
moved a fourth time and is amended; the E1 blocking condition is now specified at
field level and corroborated from the owning scope's own External review; the
[E3] circularity was re-derived from `bootstrap/_scaffold/install.py` rather than
inherited, and has an existing in-tree precedent to model on; and the fence that
was drawn around Chunk G is now correctly drawn around Chunk F2 as well.

**What remains genuinely open, and what I would most want the owed External round
to attack rather than inherit:** whether AM30's *documented* compare-and-abort is
worth anything at all against a solo Maintainer under pressure, or whether the
mechanical abort must be a precondition rather than a folded question; and
whether AM26's split — A–E and F1/F3–F6 land, F2 and G wait — is a real seam or a
convenience that leaves a half-registered capability in an adopter tree. I have
argued both are sound. Neither has been read by anyone but me.

## Plan review -- Codex (External) -- 2026-08-05

**Tier**: External
**Findings**: raised

**Verdict: REVISE.** AM28 closes the live-runner criterion in the executable
contract, and AM29--AM31 turn the first-use bootstrap into an explicit
Maintainer ceremony with exact destinations, out-of-band hashes, an independently
reviewed commit, and an abort path. Those settle my prior [E2] and [E3] at plan
level; implementation evidence is properly still future work.

The reciprocal binding contract remains incomplete. I re-read the current
installer record and registry schema: the record binds `src`, `dst`,
`verbatim`, and `hash`, with optional living-state/base-cache fields; the
registry binds runner and policy paths/modes plus capability and evidence
metadata. Neither has a principal or scope binding field. AM25 correctly asks
the activation plan to resolve all four named bindings, but the paired plan
currently specifies only runner and policy. The two plans should say explicitly
that v1's four-item question resolves to two apparatus bindings, and that
principal and scope are child-policy semantics rather than silently absent
apparatus fields. This confirms the absence; it does not recommend inventing
new fields without a separate design.

AM26's widening of my fence to F2 is justified: F2 creates the living-state
record for a dispatcher mode that has not yet been ratified. But permitting F1
and F3--F6 to land while F2 waits conflicts with the still-operative Chunk F
acceptance criteria, several of which require the filled policy and living-state
behavior. Either fence all of Chunk F with G, or replace the Chunk F criteria
and commit sequence with a genuinely executable split. The activation plan
must mirror the resulting F2/G admission fence; its present M29 only fences a
registry entry and does not close the other side of this contract.

### Sharpening

Add an explicit extra-field disposition to the pair as well as the existing
missing-field tests. A source-owned exact constructor may make extra fields
structurally inapplicable, but that is the contract to state and test rather
than leave inferred.

## Maintainer disposition of the 2026-08-05 External review round

The 2026-08-05 `## Plan review -- Codex (External)` section above returned
**REVISE**. This plan fences implementation behind the External reviewer, **or
the Maintainer**, disposing of that REVISE. The Maintainer disposed of it. The
authorizing instruction, **verbatim**:

> Go ahead with implementation once you've revised these. I don't want another review round

**What that authorization does.** It disposes of the review round: the REVISE
verdict on the 2026-08-05 External section is closed by the Maintainer, and no
further review round is required to open implementation on the *unfenced* work.
It is a disposition, **not a bypass** — the round happened, its findings are
closed by the fold recorded below, and the Maintainer exercised the authority the
plan's own gate names.

**What it does not do**, stated so no later reader can stretch it:

* It is **not** the B3 ratification of the living-state narrowing. F2 and Chunk G
  remain fenced. An agent that cites this instruction as ratification has breached
  the fence.
* It supplies **no** Maintainer credential and **no** signing ref.
* It authorizes **no** AST re-anchor ceremony, and does not relax the fence
  against *requesting* one before the A-12 and D-2 phase-(a) ledgers exist.
* It is **not** approval to push. Pushing needs its own approval, every time.
* It does not discharge the *other* declared round in the header tier; what it
  closes is the landed REVISE, which is the condition the plan's own fence names.

### Sharpening — the 2026-08-05 fold pass

Inline chunk-cell edits driven by the accepted plan-review findings, under
`doctrine/plans.md:202-207` (status `open`, no implementation commit, nothing in
flight against the edited chunks). **The reciprocal plan
`security-verification-activation` carries the identical shared block and lands
in the same commit** — that is B3's own requirement, not a convenience.

**Cells changed, and why.**

| Cell | Change | Why |
|---|---|---|
| *The Maintainer fence*, opening + item 1 + new item 4 | Three classes → four; item 1 gains the "when the ceremony may be *requested*" obligation and its two evidence ledgers | The fence said "three" while a fourth class was in force only in an amendment table; and the ceremony-request fence had no operative home |
| *Sequence*, the step list + a Sequence-revision note | Step 6 splits into a landing part and a fenced part with an explicit fence marker; step count 8 → 9 | B4: the old list showed one Chunk F while its criteria demanded behavior a fenced F2 could not produce |
| Chunk F preamble | States the executable split and that the old split is replaced | B4 |
| Chunk F row **F2** | Moved to a separate *fenced part* table; cell rewritten to the B3 condition | B3/B4. F2 is the *producer* of the living-state record, which is what B3 fences |
| Chunk F row **F5** | Adds B2's installer-record field vocabulary in three parts, including the measured fact that `verify_integrity` **ignores** an extra key today | B2. The impossibility is asserted by a test that tries it; the half that is *not* impossible is recorded as a characterization test, not claimed closed |
| Chunk F row **F6** | Three pins in two files, with line citations verified at `d73d436`; retires the two committed "must agree" comments | The cell said "the `44` pin", singular, while three pins move |
| Chunk F criteria | Split into *landing part* (F-1…F-11) and *fenced part* (F2-1…F2-4); F-2 loses its filled-policy half to F2-1; F-7 expects Δ2 **absent**; F-9 and F-8 re-baselined; F-10 (SPDX) and F-11 (module catalog) added | B4 directly: the landing part must assert only dispatcher-plus-empty-registry behavior |
| Chunk G preamble + gating | One gating sentence → three named preconditions, of which (c) is B3's single shared condition; the "changes none of its logic" claim corrected in place | Finding 3, and B1/B3 |
| Chunk G row **G1** | Eleven fields including `runner_binding_mode` / `policy_binding_mode`; no `principal` or `scope`; the entry named as exactly what B3 fences | B1 |
| Chunk G row **G2** | Adds the entry-side extra-field refusal, asserted by trying a twelfth field | B2 |
| Chunk G criteria **G-3 / G-4 / G-5** | G-3 rewritten to the living-state binding (and the `digest_not_compared` annotation); G-4 six conditions, naming the disposition's exact scope; G-5 the first-use trust artifact, with its defect measured at `bootstrap/_scaffold/install.py:1629` | Finding 3 plus the prior round's [E3] |
| Chunk A criteria **A-8**, new **A-11**, new **A-12**, *Channel note* | A-8's `os.environ.get` probe deleted and replaced by a subprocess oracle; A-11 the `local` rebinding direction; A-12 the live end-to-end transport proof; channel note now names A-1/A-2/A-11 as the weakest oracles | The stub-cannot-prove-the-socket finding, which had no operative home |
| Chunk A row **A4** | Refusal and absent-credential must be two **distinct** fixed codes | A-8(c) is unobservable otherwise |
| Chunk C criterion **C-1** | Inverted deletion-mutant wording corrected | It read as "must stop failing" |
| Chunk D criterion **D-2** | Two-phase per-channel form: liveness before confidentiality, uncovered recorded as uncovered | A confidentiality assertion over a channel never exercised proves nothing |

**Amendment rows now folded.** The rows below are **superseded as operative
instructions** — the cell named carries them. Their text is untouched and stays
part of the record; nothing in this pass rewrites an amendment, a review, a
Response, or a Lasting-truth entry.

| Row | Folded into | Note |
|---|---|---|
| AM8 | Chunk F row F6 | verbatim substance, line citations re-verified |
| AM14 | Chunk G preamble | the "changes none of its logic" correction is now in the cell |
| AM16 | Chunk A criterion A-11 | |
| AM17 | Chunk A criterion A-8 | |
| AM18 | Chunk A row A4 | |
| AM19 | Chunk D criterion D-2 | |
| AM20 | Chunk C criterion C-1 | |
| AM21 | Chunk F criterion F-11 | the stale-ratio figure is **deleted**, not carried: measure at implementation |
| AM22 | Chunk F criterion F-10 | |
| AM25 | Chunk G gating (a)/(b)/(c) | **superseded by B1** on the binding count: four resolves to two |
| AM26 | Chunk F preamble + Sequence + Chunk F criteria split | **superseded by B4**: its split was self-contradictory |
| AM27 | Chunk F fenced-part row F2 | **superseded by B3**: one condition, stated identically on both sides |
| AM28 | Chunk A criterion A-12 | |
| AM29 | Maintainer fence item 1 | |
| AM30 | Chunk G criteria G-4 and G-5 | |
| AM31 | Maintainer fence opening + item 4 | |

**Figures re-derived at `d73d436` under
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13).** Nothing below
is carried forward from an earlier revision of this plan. **Measurement
conditions, stated because they matter:** HEAD was `d73d436` and no tracked file
in any measured surface was modified in the working tree at read time, but
untracked files were present and **concurrent sessions moved HEAD to `d2f82e0`
before this commit landed.** So every row below is a **dated snapshot, not a
constant** — which is the disposition column's whole point.

| Figure | Stated before | Measured now | Disposition |
|---|---|---|---|
| Manifest data rows (pre-capture baseline) | 95 | **95** | reproduces; kept in F-1 explicitly as a starting point to re-take |
| Bandit shipped-file count | 76 (in an amendment row only) | **76**, `PASS` | folded into F-9 as `N` → `N + 6`, `N` re-taken |
| AST baseline entries | 173 | **173** | folded into F-8 as the set to derive against |
| `test_notice_install.py` `.py`-source pin | 44 | **44** at line 75 | folded into F6 with the citation |
| `test_notice_install.py` manifest-row pin | 95 | **95** at line 145 | folded into F6 |
| `test_security_lint.py` on-disk pin | 44 | **44** at line 291 | folded into F6 |
| `install.py` `principal` occurrences | 0 (asserted) | **0** | folded into Chunk G gating (b) |
| `install.py` `scope` occurrences | 2, non-binding | **2** — line 941 comment, line 1523 docstring | folded into Chunk G gating (b) |
| `_gate_reanchor.py` `_DESIGNATED_REF` | line 64 | **line 64** | folded into fence item 1 |
| Suite total | 1959 at `6bcd2d3` | **not re-measured** | **deliberately not restated anywhere in this pass.** The plan's own disposition — retire it as an oracle, re-take at the implementing commit — stands, and adding a fifth reading would only date faster |
| `templates/modules/README.md` 12-of-20 ratio | 12 / 20 | **not re-measured** | **deleted** from the operative cell rather than carried; F-11 requires measuring both counts at implementation |

**What this pass did not fold, and why.** Named rather than left for a reader to
discover:

* **The plan header's review-gate sentence.** AM34 replaces *"No implementation
  commit lands before a review section is in the tree"* with the two-round form.
  The header is not chunk-table cell text and not a status field, so this pass
  left it; AM34 governs it, and the Maintainer's disposition above is what closes
  the landed REVISE. **A reader who follows the header sentence alone will
  under-read the gate.**
* **The *Measured baseline* block, the frozen-file accounting, the brief, and the
  Lasting-truth table** (AM1–AM7, AM9–AM13, AM15, AM23, AM24, AM32–AM34). These
  target prose sections or an append-only table, not chunk cells. Their amendment
  rows remain the operative statement for those surfaces.
* **`verify_integrity`'s extra-key tolerance.** Measured and recorded in F5;
  closing it edits `bootstrap/verify_integrity.py`, which is outside this plan's
  declared symbol delta and its *Proposed paths*. It is a lasting truth to route
  at archive, not a silent widening of this scope.

## Maintainer ratification -- living-state policy binding -- 2026-08-05

The Maintainer's authorizing instruction, quoted verbatim and visually isolated:

> I ratify policy_binding_mode: living_state for adopter-owned API and web policy files. I accept that the dispatcher binds the runner digest and the policy path, type, and lockfile classification, but does not compare the policy content digest; git review is the policy-byte review channel. I authorize Codex to scribe and commit this ratification in both api-web-security-modules and security-verification-activation.

This ratifies the exact narrowing described by the shared B3 admission fence.
**B3 is MET:** a registry entry may now declare `policy_binding_mode:
living_state`, and the reciprocal capability plan may produce the corresponding
living-state lockfile record, subject to every other chunk criterion and review.

The ratification does not add principal or scope fields, weaken runner-digest
binding, authorize credentials or a non-loopback target, produce the first-use
trust hash set, run an AST or gate-manifest ceremony, authorize signing or
pushing, or waive independent code review.

## Maintainer ratification of the B3 living-state narrowing -- Anthony Kendall -- 2026-08-10

**Authorization, quoted verbatim and visually isolated:**

> Ratify

**What it answered, recorded so the record stands alone.** The one-word
authorization was given in direct answer to a question that named this narrowing,
summarised its effect, and closed *"Ratify, or want me to dig into anything
first?"* -- so the referent is the **B3 `policy_binding_mode: living_state`
admission fence** and nothing else. Scribed by Claude (Implementation). This block
is shared verbatim with the reciprocal plan and lands in both files in the same
commit, as the shared block requires.

**The narrowing, stated as what it drops.** The accepted proposal's revision
established parent-computed digest binding over *"the runner and policy"*.
`policy_binding_mode: living_state` keeps the runner digest binding and **drops the
policy content-digest comparison** for a declared class of records.

**Why the Maintainer accepted it -- the class is five human-edited coordination
documents, not "any policy."** `_LIVING_STATE_DSTS`
(`bootstrap/_scaffold/lockfile.py:84`) is a five-entry `frozenset`:
`dev/PLANNING.md`, `dev/NEXT_SESSION.md`, `dev/.cairn/cairn_foldback.md`,
`dev/collaboration_agreement.md`, `dev/.cairn/model-selection-mapping.yml`. Every
one is a file a human edits continuously; hash-pinning them would report ordinary
work as tampering. **The boundary is enforced by the verifier, not trusted from the
lockfile** -- `lockfile.py:80-83` records that `verify_integrity` honours
`living_state` only for a `dst` in that set and fails closed on any other record
asserting it, *"so a modified script cannot hide by flipping the flag."* A shipped
script therefore cannot opt itself into unverified status.

**The risk accepted, named rather than implied.**
`dev/collaboration_agreement.md` is in that set and it carries decision rights. An
unnoticed edit to it will not be caught by integrity checking; its protection is
git history and review, not a hash. The Maintainer was shown this specific
consequence before ratifying.

**What this unfences.** `F2` and **all of Chunk G** in
`dev/plans/api-web-security-modules.md`, and registry admission under
`"living_state"` in `dev/plans/security-verification-activation.md`. An
implementing agent may now admit such an entry and land the chunk that writes the
living-state record.

**What it does NOT do, enumerated so nothing further is read into it:**

* It does not widen `_LIVING_STATE_DSTS`. Adding a sixth entry is a separate
  change to an engine constant and carries its own Security Review.
* It does not relax `runner_binding_mode`, which remains the one-member set
  `{"immutable_digest"}`.
* It does not waive the four refusals already built and tested -- a record lacking
  `living_state: true`, a path outside the authoritative set, an
  `immutable_digest` declaration over a living record, and post-construction mode
  mutation all still fail closed at DEGRADED (20).
* It does not discharge any review tier, authorize a push, or open the AST
  re-anchor ceremony.
* It does not close the `verify_integrity.py:63-111` extra-key gap, which neither
  plan in this pair owns.

## Implementation blocker — Chunk A cannot land alone — Claude (Implementation), 2026-08-10

**Model**: Claude Opus 5 (`claude-opus-5`). **Interpreter**:
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (CPython 3.13.13),
`PYTHONDONTWRITEBYTECODE=1`. **Measured at HEAD `ef70da8`**; the baseline suite
figure below was taken at `caceda5`, six commits earlier, because concurrent
sessions moved HEAD nine times during this session. Every figure is a dated
snapshot, not a constant.

**Status: no implementation commit landed.** Chunk A's four engine members and
its adversarial suite are written and pass, and they are **not committed**,
because three independent gates make Chunk A un-landable on its own. That is a
measured falsification of an operative plan claim, so it is recorded here and
routed to the Maintainer rather than resolved by an implementing agent choosing
a mitigation.

### What was built and verified

* The four engine members under `templates/modules/team-gated/_security_net/`
  — `__init__.py`, `policy.py`, `net.py`, `report.py` — A1–A4 complete.
* `bootstrap/tests/test_security_net.py` — A5, **84 tests, all passing** in
  ~35 s. No transport call is mocked anywhere in the file: every request crosses
  a real socket to a real threaded listener, and every "what arrived" assertion
  reads that listener's record.
* Every deletion mutant is applied to a **throwaway copy** of the engine in
  `tmp_path`, not to the tree, and each perturbation anchor is asserted to match
  exactly once — so a mutant that silently stopped applying fails loudly instead
  of passing green. There is consequently **nothing to restore**, which is a
  stronger property than a verified restore.
* `python -m bandit -r templates/modules/team-gated/_security_net` → **zero
  issues** (see *Bandit finding, fixed in code* below).
* A2's schema carries a **positive control** and a 31-row refusal table in which
  every row is pinned to its own **reason token**, not merely to "a refusal".
  Pinning the code alone would be satisfied by a schema that refused everything
  with one generic token, which tells an adopter nothing about their file.

### The blocker, in three independent measurements

**Any new template `.py` must be registered in `_MODULE_MAPPINGS` in the same
commit that creates it.** Chunk A creates four and registers none — F1 does the
registering, and F is last.

1. **`bootstrap/tests/test_security_lint.py` — three red nodes.**
   `test_every_templates_py_on_disk_is_release_scanned` requires *every*
   `templates/**/*.py` on disk to be reachable from `scan_targets()`, which is
   derived from `install_manifest()`. Also red:
   `test_templates_py_count_is_pinned` and
   `test_the_on_disk_oracle_goes_red_when_a_registry_stops_delivering`.
2. **`python scripts/quality_gate.py --sub redundancy` — `fail=0` → `fail=8`.**
   Measured both ways in one session by holding the engine directory aside and
   restoring it (restore confirmed with `git status --short`). All eight are R6
   "never referenced in the scanned corpus" over engine functions whose only
   callers are the Chunk B and Chunk C facades.
3. **Bandit** was the third, and it is the one an implementing agent *can* fix;
   see below. It is recorded because it completes the pattern: three of Cairn's
   four standing gates treat a template `.py` with no caller and no manifest row
   as a defect.

Gates 1 and 2 both clear only when the facades (B, C), the doctrine and stubs
(E) and the mapping rows (F1) exist. **The natural commit boundary for this plan
is therefore A+B+C+E+F1, not A alone.**

**This falsifies AM11's** *"The baseline stays green through Chunks A–E, which
touch no `bootstrap/_scaffold/` file"*. The premise is true and the conclusion
does not follow: `test_security_lint.py` gates on-disk template `.py` files, not
on `bootstrap/_scaffold/`, and the redundancy sub-gate gates callers.

### Figures measured for this pass

| Figure | Plan / amendment says | Measured at `ef70da8` |
|---|---|---|
| Manifest data rows | 95 (F-1 pre-capture) | **100** |
| Manifest verbatim `.py` rows (`test_notice_install.py:75`) | 44 | **46** |
| Manifest total-row pin (`test_notice_install.py:175`) | 95 | **100** |
| Distinct `.py` on disk under `templates/` (`test_security_lint.py:372`) | 44 | **46** before Chunk A, **50** with it |
| `_SCAN_EXCLUSIONS` | not mentioned in this plan | `{}`; its own docstring records disk/manifest/`git ls-files` agreeing at **45** `as_of` 2026-08-05, itself already stale |
| Bandit shipped-file count baseline (F-9 `N`) | 76 | not re-taken — F-9 is not reachable |
| Full suite, clean tree | 1959 (AM33) | **2593 passed, 0 failed, 353.94 s** at `caceda5` |
| `check_cairn.py` | — | **OK**, 173 Markdown files, rc 0 |
| `quality_gate --sub neutrality --sub redundancy` | — | rc **1**; neutrality is the known pre-existing baseline, redundancy is the Chunk-A regression above |

### The two candidate resolutions, with their measured costs

Stated so the Maintainer can pick in one line. **Neither is adopted here.**

* **R1 — merge the commit boundary.** Land A, B, C, E and F1 as one commit (or a
  sequence whose intermediate states are not required to be green). Costs: one
  large commit on the highest-risk surface in the plan; F-1's "capture the
  manifest at the Chunk-E commit, then diff" loses its capture point and must be
  taken against the pre-A commit instead; the three frozen pins move once, as F6
  intends. Keeps *every* other plan invariant, including "exactly one chunk
  touches `bootstrap/_scaffold/`" and the single AST ceremony.
* **R2 — declare the interim exclusion.** Add the four engine paths to
  `_SCAN_EXCLUSIONS` in `bootstrap/tests/test_security_lint.py` with the
  mandatory rationale, move that file's count pin, and add the eight engine
  functions to `scripts/quality_gate_unused_def_whitelist.py`; F6 reverses all of
  it. Costs: edits a **frozen** file outside its planned chunk; moves two pins
  twice; and leaves a hand-rolled TLS client **outside the release Bandit scan**
  for the duration — which is the single worst file in the tree to leave
  unscanned, and is the defect `scan-coverage` was written to close.

R1 is the smaller deviation on the evidence. It is still a deviation from the
*Sequence*, which is why it is not taken unilaterally.

**Chunk E was checked as an alternative starting point and rejected on evidence,
not on gates.** The on-disk oracle is `.py`-only — measured by reading it — so
Chunk E's two doctrine files and two JSON stubs would very likely land green on
their own. They are not written, because E-1 and E-2 both require *installing
into a temporary adopter and running each local leg*, which needs the facades and
the mapping rows; and because both doctrine files must describe how to read the
output of runners that do not exist yet. Writing prose whose acceptance criteria
cannot be executed is how the *Channel note* for Chunk H says this goes wrong:
"the evidence is a reading of the landed runners plus a live run of each
installed command, not a reading of the prose just written."

### Measured corrections to Chunk A's acceptance criteria

Each was found by executing the criterion, not by reading it. All are recorded
as corrections to *expectations*, not relaxations of *claims*.

* **A-1/A-2/A-11 — the post-connect check is two independent guards, so a
  single-guard mutant does not reach the peer.** The plan predicts that deleting
  the post-connect peer check lets A-1 through. Measured: it does not. The check
  is `peer not in validated_addresses` **and**
  `classify_address(peer) not in allow_classes`, and A-1's hazard (public
  validated, loopback delivered) trips both — delete the set guard and the class
  guard still refuses, with `peer_class_refused`. Reaching the peer requires
  deleting **both**. This is a *stronger* result than the plan expected: each
  guard discriminates alone. Both mutants are landed as separate tests for each
  of the two directions, so A-1 and A-11 discriminate independently as AM16
  requires.
* **A-7 — the `CERT_NONE` mutant is over-broad by exactly one row.** The plan
  says "all four must fail". Measured: three do (untrusted chain, hostname
  mismatch, expired). The fourth — a peer that speaks no TLS at all — still
  refuses, because `CERT_NONE` does not make a non-TLS peer speak TLS. The test
  pins the accurate version and says so in its docstring. A positive control (a
  trusted, matching certificate that *is* accepted) was added: without it the
  four refusals could be "TLS never works in this fixture" rather than "these
  four shapes are refused".
* **A-11's mechanism, disclosed rather than glossed.** A-11 substitutes the peer
  *report* (`getpeername()`) rather than the peer itself, because no non-loopback
  address is bindable on an arbitrary host — macOS refuses `127.0.0.2`, and a
  machine may have no external interface — and a security criterion that only
  fires on a networked host is not a criterion. A-2 covers the
  genuinely-real-second-peer case with a real `::1` listener and the kernel's own
  `getpeername()`. The two rows together cover both branches of the check.
  Likewise the rebinding hazard is driven at the **socket layer** rather than by
  a second resolver call: the engine resolves exactly once (asserted), and a
  design that re-resolved at connect time would *be* the rebinding
  vulnerability.
* **A-4 gained a liveness half.** The plan's mutant ("make the client follow
  redirects") has no guard to delete — not following is a structural absence.
  Replaced with a test-authored naive client that *does* follow and carries its
  credential, which proves the second fixture is reachable and the assertion can
  fail. Without it, "the redirect target saw no credential" and "the redirect
  target is unreachable by this fixture" are indistinguishable.
* **A-5's connection-isolation row carries a hazard perturbation and no deletion
  mutant, and says so.** There is no connection pool to delete.
* **A-9's symlink check is scoped below the platform temporary root.** Walking to
  `/` and refusing any symlink component would refuse every default macOS
  configuration (`/var` → `/private/var`) rather than any hostile one. The
  security property — the report cannot land in the repository — is carried by
  realpath containment on **both** the literal and the resolved path, and the
  symlink-into-the-checkout hazard is asserted directly.
* **The hostile-`TMPDIR` rows drive `tempfile.tempdir`, not `TMPDIR`.**
  `gettempdir()` caches its answer and **silently falls back** to the next
  writable candidate when `TMPDIR` is unusable, so a test that only set the
  variable would exercise the platform default and pass without ever presenting
  the hazard. Recorded because it is precisely a check that could not fail.

### Bandit finding, fixed in code and not allowlisted

The first Bandit run over the engine reported **B613 `trojansource`, severity
HIGH**: `report.py`'s bidi-codepoint set was written with literal bidi
characters, which makes the file that *detects* Trojan Source into a carrier of
it. F-9 makes MEDIUM+ a stop whose fix is code; the literals were replaced with
`\uXXXX` escapes. Two Low `B105` false positives (attribute names containing
"token") were removed by renaming to `reason_withheld` / `redirect_withheld`.
Post-fix: zero issues over 1597 lines.

### Criteria that are not reachable in Chunk A, and where they go

Named rather than left to read as coverage. Each needs a facade, and the facades
are Chunks B and C:

* **A-8(b)** credential-marker confidentiality and **A-8(c)** the subprocess
  ordering oracle. A-8(a)'s two sound socket probes are landed, as is A-8(c)'s
  precondition — that policy refusal and absent-credential are two distinct
  fixed codes.
* **A-10's facade half** (exit 20 / DEGRADED with no policy read). The engine
  half — a missing member raises `EngineIncomplete` at import — is landed.
* **A-12's four-public-entry-point form.** The engine-level live transport proof
  is landed: real loopback socket, `net._RESOLVER is socket.getaddrinfo` and
  `net._SOCKET_FACTORY is socket.socket` asserted unpatched, and the connected
  peer read from the listening fixture's own record and compared with the
  engine's belief. Per the Maintainer fence, **no AST re-anchor ceremony may be
  requested** until A-12's full form and D-2's per-channel phase-(a) ledger exist
  in landed commit bodies; neither does.

### One disclosed test seam a code reviewer should look at directly

`report.py` carries `_CHANNEL_PASSTHROUGH: frozenset = frozenset()` — empty in
shipped source, with no writer: no environment variable, policy field, CLI flag
or import hook reaches it, and
the new suite's `test_channel_passthrough_is_empty_in_shipped_source` pins both the value and the literal. It exists so D-2's per-channel *liveness*
phase can be a genuine one-line source mutation on a throwaway copy. It is
disclosed here rather than discovered in review, and a reviewer who judges an
inert seam in a security module unacceptable should say so — the alternative is
asserting confidentiality over channels the runner may never reach, which D-2
exists to forbid.

### Fences not approached

No credential value was requested, accepted, or handled. No `deployed-passive`
path was executed against any non-loopback target; no test contacts a real host.
No `--authorize-base-url` was typed. No first-use trust hash set was produced.
No `update_symbol`, `_gate_manifest.py` re-pin or `_gate_reanchor.py` invocation
was run, and no ceremony was requested. Nothing was pushed. `B3` is ratified, so
F2 and Chunk G are unfenced — neither was reached.

**Whole-suite confirmation, added after the record above landed at `3ba31c6`.**
`python -m pytest bootstrap/tests -q` with Chunk A present, canonical
interpreter, `PYTHONDONTWRITEBYTECODE=1`: **3 failed, 2674 passed, 385.58 s**.
The red set is **exactly** the three nodes predicted above —
`test_every_templates_py_on_disk_is_release_scanned`,
`test_templates_py_count_is_pinned` and
`test_the_on_disk_oracle_goes_red_when_a_registry_stops_delivering`, all in
`bootstrap/tests/test_security_lint.py`. **There is no fourth red**, which is the
part worth recording: the coupling is entirely to the manifest registration and
touches nothing else in the suite, so R1 clears all three and needs no further
allowance. Arithmetic check on the count: 2674 passed + 3 failed = 2677 =
the 2593-node baseline plus this chunk's 84 new nodes, so no node was dropped
and no marker was added — the HOLD class *Gate accounting* names.

## Maintainer authorization of the R1 commit-boundary deviation -- 2026-08-10

**Authorization, quoted verbatim and visually isolated:**

> I'm completely fine with a big commit. We don't need to always have
> these atomic commits. Let's go R1

**What it authorizes.** The **R1** resolution recorded in
`## Implementation blocker` above: the implementation commit boundary is set by
what the standing gates actually permit, **not** by the *Sequence*'s chunk table.
Chunks A, B, C and E land together with Chunk F's row **F1** (and F6's pin
moves), because no smaller set leaves the suite green. **R2 -- declaring the four
engine sources in `_SCAN_EXCLUSIONS` -- is explicitly not taken:** putting a
suppression into a security gate to preserve a commit boundary is the wrong
trade, and the Maintainer did not choose it.

**Why the plan was wrong, which is the part worth keeping.** This is a
mechanism error, not a preference the Maintainer overrode. **AM11**'s premise is
true and its conclusion does not follow:

* *Premise, true:* Chunks A--E touch no `bootstrap/_scaffold/` file, so they
  cannot move the AST attestation baseline.
* *Conclusion, false:* "the baseline stays green through Chunks A--E".
* *The mechanism it missed:* `bootstrap/tests/test_security_lint.py`'s on-disk
  oracle gates **`templates/**/*.py` reachability from `install_manifest()`** --
  physical presence under `templates/`, not membership of `_scaffold/`. A
  template `.py` that exists without its `_MODULE_MAPPINGS` row is therefore a
  red node no matter which chunk created it. The same coupling appears a second
  time in `scripts/quality_gate.py --sub redundancy`, whose R6 rule reds an
  engine function that has no caller until the facades exist.

The durable rule this yields, stated so a later scope does not rediscover it:
**a new template `.py` and its `_MODULE_MAPPINGS` row are one commit, always.**
Any plan that sequences "add the source" before "register it" has an
unexecutable Sequence, and the defect is invisible until the source is written.

**What this authorization does not do.** It is not approval to push; pushing
needs its own approval, every time. It does not authorize an AST or
gate-manifest re-anchor, nor relax the fence against *requesting* one before the
A-12 and D-2 phase-(a) ledgers exist. It does not supply a credential, a signing
ref, or the G-5 first-use trust hash set. It does not discharge any review tier,
and it does not widen the plan's *content* -- only its commit granularity.

## Implementation verification -- Claude -- 2026-08-10

**Scope landed under the R1 authorization:** Chunks **A**, **B**, **C**, **E**,
and Chunk F's **F1** and **F6**. **Not landed:** F2, F3, F4, F5, Chunk D,
Chunk G, Chunk H — see *Known omissions*.

**Tested commit**: `ddffcd6` (the implementation commit).
**Reviewed range**: `3fd0c91..ddffcd6` for the implementation; the R1
authorization is at `3fd0c91` and the blocker record it disposes of at
`3ba31c6`/`7a71a7e`.
**Interpreter / runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
CPython **3.13.13**, `PYTHONDONTWRITEBYTECODE=1`. OpenSSL 3.6.2. macOS
(Darwin 25.5.0). `openssl(1)` 3.6.2 on `PATH`, required by the A-7 certificate
fixtures.

**Pre-run state — stated exactly rather than asserted clean, because it was
not.** At suite start the working tree carried, in addition to this scope's
files: `bootstrap/_scaffold/install.py`, `bootstrap/_scaffold/slotmerge.py`,
`bootstrap/_scaffold/__init__.py` (modified) and
`bootstrap/tests/test_module_merge_lockfile.py` (untracked). **These are another
session's live `write_install_lockfile` / module-merge fix**, covered by its own
intent claim (`claude-d8d22f62-20260810T145334-010708`). They were not touched,
not committed, and their state is **not** reported here as this scope's. Also
untracked and not this scope's: `.claude/`, `dev/measurement/collision_log.md`,
`dev/measurement/snapshots/`. This scope's own files were uncommitted at run
time and are byte-identical to what the tested commit contains.

**Post-run state**: unchanged. Every deletion mutant in this scope is applied to
a **copy** of the subject in `tmp_path` — an engine copy for Chunk A, an
installed-adopter copy for Chunks B/C/E — so no perturbation ever touches the
tree and there is nothing to restore. That is a stronger property than a verified
restore, and it is why no restore ledger appears below. Each perturbation anchor
is asserted to match **exactly once**, so a mutant that silently stopped applying
fails loudly instead of passing as a green test.

**Commands, exits, outcomes, elapsed.**

| Command | Exit | Outcomes | Elapsed |
|---|---|---|---|
| `python -m pytest bootstrap/tests -q` (**whole suite**) | 1 | **2785 passed, 2 failed**, 0 skipped, 0 xfailed | **416.24 s** |
| `python -m pytest bootstrap/tests/test_security_net.py bootstrap/tests/test_api_access_security.py bootstrap/tests/test_web_hosting_security.py -q` | 0 | **178 passed**, 0 failed, 0 skipped, 0 xfailed | 58.00 s |
| `python -m pytest bootstrap/tests/test_scaffold.py test_presets.py test_profile_grammar.py test_ast_attest.py test_gate_manifest.py test_security_leaf.py test_security_stack.py -q` (the install-contract-sensitive set) | 1 | **288 passed, 2 failed** | 28.61 s |
| `python -m pytest bootstrap/tests/test_security_lint.py bootstrap/tests/test_notice_install.py -q` (the two frozen pin files) | 0 | **23 passed** | 1.47 s |

**Baseline for comparison**: **2593 passed, 0 failed, 353.94 s** at `caceda5`,
measured clean earlier in this session before any of this scope existed. Node
count: 2785 + 2 = 2787 = 2593 + this scope's 178 new nodes + 16 from sibling
scopes that landed in between, so no node was dropped and no skip/xfail marker
was added.

**One honest qualification on the whole-suite run, because "against a clean,
unchanged commit" is the standard and this was not quite that.** The run was
launched from the working tree immediately before the implementation commit, so
it tested byte-identical *code* to `ddffcd6` but two of that commit's Markdown
files without their `claim-check-allow` headers, and it ran while a concurrent
session's `write_install_lockfile` fix was present in
`bootstrap/_scaffold/install.py` / `slotmerge.py` / `__init__.py` (those three
have since been committed by that session). No test reads either doctrine file,
so the Markdown difference cannot move a figure; the concurrent engine changes
are visible in the failure output and are named below. **A re-run against
`ddffcd6` alone would be the strictly correct Boundary-B artifact and has not
been performed.**

**Non-pass disposition.** Exactly **two** failed nodes, both in
`bootstrap/tests/test_ast_attest.py`:
`test_committed_baseline_accounted_for_across_the_engine_package` and
`test_ast_gate_passes_over_the_full_scaffold_module_set`. These are **AM11's two
predicted known-red nodes**, they fail because `verify()` returns 1 on any
CHANGED entry, and they are the ceremony's to clear — **not an implementing
agent's**. AM11's rule that *any third red node is a stop-and-explain* held:
there was no third. **What AM11 did not anticipate is that the two nodes were
already red before this scope touched anything**, from the concurrent
`write_install_lockfile` fix's three CHANGED symbols; Δ1 joins existing reds
rather than creating them.

### Plan-specific acceptance commands, with outcomes

| Command | Outcome |
|---|---|
| `python -m pytest bootstrap/tests/test_security_net.py -q` | **84 passed** (A-1…A-12 engine level, A2 schema) |
| `python -m pytest bootstrap/tests/test_api_access_security.py -q` | **65 passed** (B-1…B-7, A-8(b)/(c), A-10 facade half, E-1/E-2) |
| `python -m pytest bootstrap/tests/test_web_hosting_security.py -q` | **29 passed** (C-1…C-5) |
| `python -m bandit -r` over the six new shipped sources | **zero issues**, 1597+ lines. One **HIGH** was found and **fixed in code**, never allowlisted — see below |
| `python scripts/check_cairn.py` | **OK**, rc 0, **175** Markdown files (the two new doctrine files are inside its scan roots). It first reported **7 `suspicious-url` issues** over the policy examples and a prose bullet naming the two URL schemes; resolved with reasoned, **scoped** `cairn-accept` markers — a block marker around each JSON example and a line-scoped one on the bullet — never a domain added to `content_scan_allowlist.txt`, which is a noise policy for cited publication hosts and not the right instrument for an example address. |
| `python scripts/quality_gate.py --sub neutrality` | `fail=93 info=21` — **unchanged** from the pre-existing baseline |
| `python scripts/quality_gate.py --sub redundancy` | `fail=0 info=2` — **back to baseline**; it was `fail=8` with Chunk A alone, and the facades resolved it |
| `python scripts/claim_check.py <each new .md>` | **OK, no flags**, one file per invocation |
| `python bootstrap/scaffold.py --manifest` | **114 data rows**, exactly **+14** over the pre-scope 100, **−0, ~0** |
| `python bootstrap/scaffold.py --config … --target /tmp` (both selected) | installs 2 facades, 2 four-member engine copies, 2 stubs, 2 doctrine files; lockfile written |
| `python bootstrap/verify_integrity.py --target <tmp>` | fresh install **OK, 77 recorded files** |
| same, after a one-byte edit to an installed engine member | **`modified (hash mismatch)`** — the runner is correctly **not** living state (F-2's hazard) |
| same, after filling an installed policy | **`modified (hash mismatch)`** — the expected state **without F2**, and precisely why F2 exists |
| installed `api_access_security.py local` / `web_hosting_security.py local` on untouched stubs | **INCOMPLETE, exit 5**, both (E-1) |
| `cmp` across the two installed engine copies, and against the template source | all four members **byte-identical** both ways |

### The AST delta — reported, re-anchored nothing

Derived with `_ast_attest`'s **own** `_merge_current` / `_classify`, never a
reimplementation, against the committed baseline read at the implementing commit
(**173 entries**).

**This scope's delta is exactly Δ1, and nothing else:**

| Symbol | File | Old digest | New digest |
|---|---|---|---|
| `Assign:_MODULE_MAPPINGS` | `bootstrap/_scaffold/config.py` | `df43d4d75f55a3e5` | `0f42fa9a794a77da` |

**MISSING: none. DUPLICATE: none.**

**Three further CHANGED symbols are present in the tree and are NOT this
scope's** — they belong to the concurrent `write_install_lockfile` /
module-merge fix named in *Pre-run state*, and are recorded here only so the
Maintainer forming a ceremony union is not surprised by them:
`FunctionDef:write_install_lockfile` and `FunctionDef:run_module_merge_pass`
(`bootstrap/_scaffold/install.py`), and `FunctionDef:merge_module_into_slot`
(`bootstrap/_scaffold/slotmerge.py`).

**Δ2, Δ3, Δ4 and Δ5 are ABSENT, as they must be**: F2, F3 and F4 did not land.
Δ1 alone *is* a member of `_UPDATE_ALLOWLIST`, so the surgical path would apply
to this scope in isolation — it does not apply to the tree as it stands, because
of the three concurrent CHANGED symbols above. Either way: **no re-anchor was
performed and none was requested.** Both fence conditions on *requesting* one
remain unmet — A-12's four-public-entry-point form and D-2's per-channel
phase-(a) ledger do not exist, because Chunk D did not land.

**Frozen-file accounting, reported not re-pinned.** Two frozen files were edited
by F6: `bootstrap/tests/test_notice_install.py` (two pins) and
`bootstrap/tests/test_security_lint.py` (one pin). Both are literal keys in the
`frozen_files` map, so both are now `FROZEN-MODIFIED`.
`bootstrap/tests/fixtures/scaffold_ast_known_new.json` was **not** edited and
needed no edit — this scope adds no NEW symbol.
`mapping_symbols._MODULE_MAPPINGS.baseline_digest` and `cascade_mutable`'s
`pre_run_sha256` for `bootstrap/_scaffold/config.py` have moved.
`config.py`'s cascade governance — *"one predeclared mapping-symbol delta
only"* — is satisfied **exactly**: `_MODULE_MAPPINGS` is the only symbol in that
file this scope moves.

### The three pins moved, and they no longer agree

Measured, not carried forward. The plan predicted 54 / 109 / 50; every prediction
was wrong, because sibling scopes moved the baselines first.

| Pin | Before | After |
|---|---|---|
| `test_notice_install.py::test_manifest_has_the_expected_py_source_count` (manifest **rows**) | 46 | **56** |
| `test_notice_install.py::test_notice_appears_in_manifest_data_row_count` (total rows) | 100 | **114** |
| `test_security_lint.py::test_templates_py_count_is_pinned` (**distinct** `.py` on disk) | 46 | **52** |

**The first and third now diverge for the first time — 56 versus 52 — and must
not be made to agree.** One counts manifest rows, the other counts distinct files
on disk, and this scope installs one four-member engine tree to **two**
destination trees: six new files are six there and ten here. The two committed
comments asserting they agree are **retired in the same commit that falsifies
them**; neither was executable, which is exactly why leaving them would have been
worse than moving them. `_SCAN_EXCLUSIONS` stays **empty**.

### Bandit finding, fixed in code

The first run over the engine reported **B613 `trojansource`, severity HIGH**:
`report.py`'s bidi-codepoint set was spelled with literal bidi characters, which
made the module that *detects* Trojan Source a carrier of it — a reviewer reading
the source would have seen reordered text. F-9 makes MEDIUM+ a stop whose fix is
code, so the literals became `\uXXXX` escapes. Two Low `B105` false positives
(attribute names containing "token") were removed by renaming to
`reason_withheld` / `redirect_withheld`. Post-fix: **zero issues**.

`python bootstrap/security_check.py` was **not** run to completion: it fails
closed on an unclean worktree, and the worktree cannot be made clean while
another session's fix is in flight. Bandit was therefore run directly over the
six new shipped sources, which is the subset this scope adds; the release
ceremony remains the Maintainer's.

### Defects this scope's own tests caught

Recorded because a test that catches nothing is the recurring defect class here,
and these are the evidence that these do not.

1. **The facades crashed with a traceback instead of reporting DEGRADED.**
   `EngineIncomplete` is raised during the engine package's *import*, outside the
   `verify_engine_complete()` handler, so a missing engine member produced a
   traceback and exit **1** where criterion A-10 requires exit **20**. A traceback
   is also an uncontrolled output channel. Fixed in both facades: the import is
   wrapped, the failure is reduced to a fixed reason, and the first candidate
   engine directory is now **fatal on failure** rather than falling through to the
   other layout — so a broken install can never be masked by the fallback.
2. **A reason token that could never be produced.**
   `credential_name_supplied` was unreachable: the generic closed-key sweep ran
   first, so a policy naming its own credential variable was refused as an
   ordinary typo. Reordered, and the check widened to six spellings.
3. **A hostile-`TMPDIR` test that could not fail.** `gettempdir()` caches and
   **silently falls back** past an unusable `TMPDIR`, so setting the variable
   alone exercised the platform default. Now drives `tempfile.tempdir`.
4. **A URL length cap that refused correct policies.** All strings shared a
   64-byte label cap, which no real base URL survives. Split into a label cap and
   a wide cap for URLs, pointers and declared bodies.

### Measured corrections to the plan's stated expectations

* **A-1's deletion mutant does not do what the plan predicts.** The post-connect
  check is **two independent guards** — peer-in-validated-set and peer-class —
  and A-1's hazard trips both. Deleting one leaves the other refusing. Reaching
  the peer requires deleting both. This is *stronger* than the plan expected, and
  both mutants are landed per direction so A-1 and A-11 discriminate
  independently.
* **A-7's `CERT_NONE` mutant is over-broad by exactly one row.** Three of four TLS
  rows stop refusing; the non-TLS-peer row still refuses, because `CERT_NONE` does
  not make a peer that speaks no TLS speak TLS. The accurate version is pinned.
* **B-3's "non-default port" row does not belong to `local`.** A disposable
  loopback fixture binds an arbitrary high port by definition, so refusing one
  would refuse every correct use. That row belongs to B-5's deployed near-miss
  table. Pinned as an **accepted** shape so the discrepancy is visible rather than
  silently resolved.
* **C-1 is strictly one-to-one, including for `csp`.** An absent CSP header
  reports the missing header and does **not** additionally report every reviewed
  directive, because the directive check is guarded on the header being present.
  The first version of the test expected the noisier behaviour; the runner was the
  better of the two.

### Known omissions

* **Chunk D did not land.** The cross-runner confidentiality sweep — D-1…D-6, the
  AW6/AW8 gate — does not exist. What *does* exist: A-8(b)'s credential-marker
  absence across stdout, stderr, the report and the whole temporary directory;
  D-3's cardinality-class closure asserted structurally (a finding carries no
  integer at all); and per-check value-absence assertions in B and C. **None of
  that is the sweep**, and the plan's own standard is that a per-channel
  liveness-then-confidentiality ledger is what closes the gate.
* **F2 (Δ2, `_LIVING_STATE_DSTS`) did not land**, though B3 is now ratified and it
  is therefore unfenced. Consequence, measured above: a filled policy reports
  `modified (hash mismatch)`. It was held because `bootstrap/_scaffold/lockfile.py`
  sits beside another session's in-flight lockfile work and the correct move was
  to claim narrowly and report the interaction rather than edit around it.
* **F3, F4, F5 did not land** — the capability install notice (Δ4/Δ5), its two
  `cli.main` call sites (Δ3), and `test_security_capability_install.py`. So F-6
  (the notice on both surfaces), F-11 (the module catalog decision) and F5's
  three-part B2 field-vocabulary tests are **not** satisfied.
* **Chunk G did not land.** No registry entry, so both capabilities are directly
  invocable but **neither integrity-classified nor standing checks**. Both
  doctrine files say so rather than claiming otherwise. G-5's first-use trust hash
  set is the Maintainer's and was not produced.
* **Chunk H did not land** — no `bootstrap/SAFETY.md` rule, no
  `bootstrap/DEPENDENCY_BUDGET.md` statement, no `CHANGELOG.md` line. **Cairn now
  ships a network client and `SAFETY.md` does not yet say so.** That is the most
  important single omission in this list.
* **A-12's four-public-entry-point form** is not satisfied; only the engine-level
  live transport proof is.
* **The `deployed-passive` legs are exercised only up to their refusal
  boundaries.** No test drives a deployed leg to a successful request, because
  none supplies a deployed credential and none contacts a real host — which is the
  Maintainer fence working, and it means the deployed request path itself is
  **unexercised**.
* **`openssl(1)` on `PATH` is a hard test dependency** for the A-7 and hosting-TLS
  certificate fixtures, asserted rather than skipped (the plan requires zero
  skips). A machine without it fails those nodes rather than silently passing.
* **Windows is asserted nowhere.** The report's `0600` mode is POSIX; both
  doctrine files say so.
* **No human has read the two runners line by line for security content.** The
  tests and Bandit are a different thing.

## Implementation verification -- Claude -- 2026-08-10 (Chunks H and D)

**Scope landed in this pass:** Chunk **H** (`5d1e941`) and Chunk **D**
(`d2a3f4b`). **Deliberately not landed:** **F2** -- and therefore Chunk **G** --
stopped on a contradiction in the authorization they rest on; see *The F2 stop*
below. **Still outstanding:** F3, F4, F5.

**Interpreter / runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
CPython **3.13.13**, `PYTHONDONTWRITEBYTECODE=1`. macOS (Darwin 25.5.0).
`openssl(1)` on `PATH` (required by the hosting-TLS fixtures this pass reuses).

**Pre/post state -- stated exactly rather than asserted clean, because it was
not.** Throughout this pass the working tree carried other sessions' live work:
`bootstrap/_scaffold/config.py`, `docs/quickstart.md`,
`docs/solo-legacy-recipe.md`, and later `bootstrap/tests/test_presets.py`,
`test_upgrade.py`, `test_default_security_stance.py`,
`test_security_verification.py`, `test_module_merge_lockfile.py`,
`dev/plans/corpus-tier-cost.md` and an untracked
`dev/modules/security-verification.md`. **None was touched, committed, or
reported here as this scope's.** HEAD moved from `a62a5d2` to `5792298` to
`d2a3f4b` during the pass; every figure below is a dated snapshot at a named
commit, not a constant.

**Commands, exits, outcomes, elapsed.**

| Command | Exit | Outcome | Elapsed |
|---|---|---|---|
| `python -m pytest bootstrap/tests/test_security_finding_confidentiality.py -q` | 0 | **38 passed**, 0 failed, 0 skipped, 0 xfailed | 19.4 s |
| `python -m pytest bootstrap/tests/{test_security_lint,test_notice_install,test_security_net,test_api_access_security,test_web_hosting_security}.py -q` | 0 | **201 passed** | 59.0 s |
| `python scripts/check_cairn.py` (before H) | 0 | OK, **174** Markdown files | -- |
| `python scripts/check_cairn.py` (after H) | 0 | OK, **175** Markdown files | -- |
| `python scripts/quality_gate.py --sub neutrality` | 1 | `fail=93 info=21` -- **unchanged** at every point in the pass | -- |
| `python scripts/quality_gate.py --sub redundancy` | 0 | `fail=0 info=2` -- unchanged | -- |
| `python scripts/claim_check.py <file>` over each edited `.md`, one per invocation | 0 | OK, no flags | -- |

**Known omission on Boundary B, stated rather than implied.** **No full-suite run
was performed in this pass.** The tree was never clean for long enough to produce
a Boundary-B artifact against an unchanged commit -- five other sessions'
in-flight files were present continuously -- and Chunk D adds a test file that
moves no pin and ships no template, so its effects are bounded by the scoped runs
above (Boundary A). **A full suite against `d2a3f4b` alone remains owed** and is
the strictly correct Boundary-B artifact for this pass.

**check_cairn's one issue at the end of the pass is not this scope's.** After the
Chunk-D commit, `check_cairn` reports one unresolved-path flag inside the plan
`corpus-tier-cost` (referred to by stem, and its cited path is deliberately not
repeated here -- repeating it would import the same flag into this file). That
plan was another session's live working-tree modification. `check_cairn` was
**OK on 175 files** immediately after Chunk H.

### Chunk H -- what landed, and the evidence it was checked against behaviour

`bootstrap/SAFETY.md` Rule 11 (ten numbered controls, seven explicit
non-protections), Rule 5 re-scoped in place with a pointer, a
`bootstrap/DEPENDENCY_BUDGET.md` **non-exception** section, and one
`CHANGELOG.md > Unreleased > Added` entry. Chunk H's channel note requires the
evidence be a reading of the landed runners plus a live run of each installed
command, not a reading of the prose. Both were done:

| Live probe | Observed |
|---|---|
| both capabilities installed to a tmp adopter via `scaffold.py --config … --target` | 14 destinations; `--summary` lists them only under **Explicit add**, satisfying F-5's no-preset property at the public path |
| `api_access_security.py local` / `web_hosting_security.py local`, untouched stubs | **INCOMPLETE, exit 5**, both |
| `deployed-passive --authorize-base-url` with five near-misses (trailing slash, `:443`, upper-case host, `http` for `https`, added query) | **DEGRADED (20)**, `policy_refused:authorization_mismatch`, **before any network act** |
| `local` against a non-loopback policy host | **DEGRADED (20)**, `policy_refused:non_loopback_target`, before DNS |
| `local` against a loopback fixture, correct then over-permissive | **CLEAN (0)** then **FINDINGS (10)**; report dir `drwx------` holding **only** `report.json` at `-rw-------`; **zero integers** anywhere in the parsed findings; zero credential bytes in any sink |

**One measured correction to the shipped doctrine's worked example, found by
using it.** The API policy's `environment` field is constrained to
`("local", "staging", "production")`. A deployed section spelled
`"environment": "deployed"` -- the obvious guess, and the word the subcommand
itself uses -- is refused as `policy_refused:bad_expectation`, which reads as a
malformed policy rather than as an out-of-vocabulary label. Not changed here (it
is outside Chunk H's file set); recorded as a lasting truth for the archive.

### Chunk D -- the two corrections that change what the sweep can claim

**(1) `_CHANNEL_PASSTHROUGH` is an inert seam.** The engine ships it *for* D-2's
phase (a), documented as the one-line suppression a throwaway copy needs.
Measured at `ddffcd6`..`d2a3f4b`: `sanitize_channel` has exactly **two** live call
sites, and **both attributes they write are written and never read** --
`Response.reason_withheld` and `Response.redirect_withheld` have no consumer in
either facade, in any check, in any finding, in the report, in the summary, or in
the child document. The other **eleven** `CHANNEL_TOKENS` entries have **no call
site at all**. So suppression cannot make a marker appear in any sink, for any
channel, and D-2's stated instrument is unusable as written.
`test_d2_the_channel_passthrough_seam_cannot_demonstrate_liveness` pins the
measurement and fails the day a consumer is wired up.

**(2) The property is structural absence, so phase (a) is a leak injection.**
There is no shipped path that writes a peer-supplied or credential string to a
sink. An absence cannot be deleted. Phase (a) therefore *adds* the emission at
the site where the raw value is already in scope and requires the sweep to find
the marker; phase (b) restores the pristine runner and requires absence. This is
a change of **instrument**, not of purpose: it establishes exactly what D-2 asks
for -- that the runner really reaches the channel, and that the sweep really
would catch a leak there -- and it is strictly stronger than a suppression whose
output nothing reads.

**Per-channel disposition, and the maps are asserted to partition
`CHANNEL_TOKENS`.** Nine channels carry an end-to-end (a)+(b) row: reason phrase,
`Location`, an overexposed JSON property, an array member, an undeclared body
property, a credential, a refused policy label, a response header value, and a
`Set-Cookie`. Three -- TLS/transport **exception text**, **timeout diagnostics**,
and the **certificate subject** -- are closed as a *class* at
`SecurityRefusal.__init__`, which clamps every `reason` to `REASON_TOKENS`, and
the clamp is tested with a real deletion mutant; the certificate subject is
additionally pinned by a source-level assertion that no member reads any
certificate field. **One channel is recorded UNCOVERED**, per D-2's own rule: a
policy-declared **request body** has no finding, report field, summary line or
child-document site that takes it, so its absence is asserted and its liveness is
unproven. `test_d2_every_channel_token_has_a_recorded_disposition` fails if a new
channel token is added without a disposition, and asserts the three maps do not
overlap.

**Falsification ledger -- six external mutants.** Each was applied to the tree,
run, observed RED, then restored **byte-exactly** from a pre-saved copy, with the
restore proved by `shasum -a 256` equality and a blank `git status --short` on the
perturbed path.

| # | Mutation | Node | Observed |
|---|---|---|---|
| M1 | add a 14th `CHANNEL_TOKENS` entry | `test_d2_every_channel_token_has_a_recorded_disposition` | RED |
| M2 | add a `getpeercert()` call in `_wrap_tls` | `test_d2_no_engine_member_reads_a_certificate_field` | RED |
| M3 | `SecurityRefusal(E_TLS_REFUSED, str(exc))` | `test_d2_no_handler_interpolates_an_exception_into_a_refusal` | RED |
| M4 | `_ORDINAL_RE` -> `^.*$` | `test_d6row_a_non_ordinal_principal_is_refused` | RED **on `[P1]` only** -- see below |
| M5 | print the fingerprint key at construction | `test_d7_the_key_appears_in_no_sink` | RED |
| M6 | write `raw-response.bin` beside the report | `test_d3_the_temporary_directory_holds_only_the_report` | RED on `[clean]` and `[findings]` |

**Two defects this file's own falsification found in itself, and both are the
recurring class.**

1. **A test that could not fail.** The ordinal-principal rows renamed only the
   principal id, leaving the case's `principal` reference pointing at `p1`. The
   refusal therefore came from the *unknown-principal-reference* guard, not from
   the ordinal shape, and M4 left **all eight rows green**. Fixed by renaming the
   case reference too. **Re-measured: M4 then reddens exactly one row.** The other
   seven are refused one guard downstream, because the credential variable name is
   *derived* from the id -- `p0`, `p-1`, `p99999`, `p1x`, an email, a name and an
   account id all derive a name that is not set and refuse `credential_absent`.
   Only `P1` derives `CAIRN_API_P1_CREDENTIAL`, a name that *is* set, so only `P1`
   isolates the ordinal shape. All eight rows are kept -- each still asserts that
   the run refuses and that the label reaches no sink -- and the narrowness is
   recorded as a property of the design.
2. **A row asserting a property its fixture could not exhibit.** The within-run
   fingerprint row compared an overexposed scalar against an array and measured
   two *different* fingerprints -- correctly, because a list and a string are not
   equal observations. Fixed to two declared-absent properties carrying one value.
   Noted in the test body so it is not "fixed" back.

### The F2 stop -- the authorization for it contradicts itself

**F2 was not landed, and Chunk G is blocked behind it. This is a stop-and-report,
not an omission of convenience.** The block that unfences F2 --
`## Maintainer ratification of the B3 living-state narrowing -- Anthony Kendall --
2026-08-10`, present **verbatim in both plans** of the pair -- says two things
that cannot both be acted on:

> **What this unfences.** `F2` and **all of Chunk G** in
> `dev/plans/api-web-security-modules.md` […]

and, in the same block:

> * It does not widen `_LIVING_STATE_DSTS`. Adding a sixth entry is a separate
>   change to an engine constant and carries its own Security Review.

**F2 is, precisely and only, the addition of a sixth and seventh entry to
`_LIVING_STATE_DSTS`.** So the enumeration that exists "so nothing further is
read into it" forbids exactly the row the same block declares unfenced.

Three further facts make choosing an interpretation the wrong move for an
implementing agent:

* **The Maintainer's own words are one token, `Ratify`.** Every enumerated bullet
  is the *scribe's* characterization, written by an implementing agent. Reading
  one bullet as loose and the other as binding is an agent deciding the scope of
  a Maintainer authorization.
* **The stated rationale does not cover F2's two files.** The block accepts the
  narrowing because *"the class is five human-edited coordination documents, not
  'any policy'"* -- files a human edits continuously, where hash-pinning would
  report ordinary work as tampering. F2's two files are machine-read **security
  configuration for a shipped runner**, and its own row asserts the policy is
  *"**not** the integrity anchor for the deployed leg"* -- a claim that wants a
  Security Review, not an inference.
* **The constant is an executable trust boundary.** `_LIVING_STATE_DSTS` is what
  `verify_integrity` consults to decide which records may skip the tamper check.

What was verified instead of guessed: `bootstrap/_scaffold/lockfile.py` was
claimed, read at its current state (the `module_merge_directives` /
`resolve_slot_merge` work has landed, so the earlier collision is genuinely
resolved), **not edited**, and the claim was released. **Δ2 is absent from the
engine delta, as F-7 requires.**

**What the Maintainer is asked for:** one sentence saying whether the ratification
covers F2's two `dev/.cairn/*-policy.json` entries, or whether F2 takes its own
Security Review. Either answer unblocks; the contradiction is what does not.

### Known omissions after this pass

* **F2, and therefore Chunk G.** See above. Consequence, unchanged and measured
  in the Chunk-H live probes: a filled policy reports `modified (hash mismatch)`.
  Chunk G additionally needs G-5's first-use trust hash set, which is the
  Maintainer's to produce and was not produced.
* **F3, F4, F5 did not land** -- the capability install notice (Δ4/Δ5), its two
  `cli.main` call sites (Δ3), and `test_security_capability_install.py`. So F-6,
  F-11 and F5's three-part B2 field-vocabulary tests remain unsatisfied. This was
  a budget outcome, not a fence: nothing blocks them.
* **No Boundary-B full suite for this pass.** Named above with the reason.
* **`SAFETY.md` Rule 11 was written before Chunk D and refreshed after it**, in
  the same commit as this record, so its sweep paragraph describes the sweep that
  now exists rather than the gap that no longer does. It still records the
  `request_body` channel as uncovered, because it is.
* **A-12's four-public-entry-point form** and the **successful deployed-request
  path** remain unexercised, unchanged from the previous pass.
* **No human has read the two runners line by line for security content.**

## Maintainer authorization of row F2 -- Anthony Kendall -- 2026-08-10

**Authorization, quoted verbatim and visually isolated:**

> Go ahead with the F2 implementation

**What it answered, recorded so the record stands alone.** Given in direct answer
to a message that named row F2's single action -- adding the two
`dev/.cairn/*-policy.json` destinations to `_LIVING_STATE_DSTS` -- set out the
three call sites that read that set, named the Security Review the change carries,
and named the residual that F2's two entries are the first members of the set with
no witness in Cairn's own tree. F2 names exactly one action, so unlike the
one-word B3 ratification above this authorization identifies its own subject.
Scribed by Claude (Implementation).

### Correction to the B3 ratification block above -- its no-widening enumeration was wrong on the mechanism

The prior section is append-only and stands as written. This section records that
one of its enumerated items was **incorrect**, and why, so a later reader does not
cite it in good faith to block what the Maintainer has now authorized.

That block says both of these:

> **What this unfences.** `F2` and **all of Chunk G** [...]

> * It does not widen `_LIVING_STATE_DSTS`. Adding a sixth entry is a separate
>   change to an engine constant and carries its own Security Review.

Row F2 **is** the addition of a sixth and seventh entry to `_LIVING_STATE_DSTS`.
So the block unfences F2 and forbids the only thing F2 does. The two clauses are
not independent facts that happen to conflict: **set membership is the mechanism
by which `living_state` is honoured at all.** Measured at `625c161`:

* `bootstrap/verify_integrity.py:96-105` honours `living_state` **only** for a
  `dst` inside the set, and reports anything else asserting it as
  `illegal living_state opt-out ... (tamper / malformed lockfile)`.
* `bootstrap/_scaffold/install.py:1796` is the only site that writes the
  `living_state` key, and it writes it **only** for a `dst` inside the set.

So without F2 there are exactly two branches and both fail closed: the installer
omits `living_state: true` and the dispatcher refuses DEGRADED (20) for a record
lacking the flag, or the installer writes it and `verify_integrity` reports the
adopter's own policy file as a tamper attempt. `policy_binding_mode:
living_state` for the API and web policy files is **inoperative without F2**.

**What the enumeration was right about.** It was right that this carries its own
Security Review. Widening a fail-closed integrity boundary read by three
consumers -- `verify_integrity.py:97`, `install.py:1796`, `upgrade.py:1699` -- and
named part of the declared trust anchor at `bootstrap/_scaffold/__init__.py:281`
is a Security-Review-class engine change. It was wrong only that the change is
severable from what B3 ratified.

**The Security Review is therefore OWED, not satisfied.** The Maintainer's
authorization discharges the *fence*; it does not discharge a *review tier*, and
no agent writes its own Security Review. F2 lands with that recorded as
outstanding.

## Implementation verification -- Claude -- 2026-08-10 (Chunk F row F2)

**Commits.** `625c161` (F3, F4, F5 -- the landing part's remaining rows) and this
commit (F2). Interpreter: `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(3.13.13), `PYTHONDONTWRITEBYTECODE=1` throughout. Cairn has no CI; every figure
below is from a run on this host.

**What landed for F2.** Two entries in `_LIVING_STATE_DSTS`
(`bootstrap/_scaffold/lockfile.py`) with the inline reasoning row F2 requires --
adopter-filled configuration, tracked for upgrade, excluded from the tamper check,
and explicitly **not** the integrity anchor for the deployed leg -- plus the two
F2 criteria tests in `bootstrap/tests/test_security_capability_install.py`.

**A prose defect corrected in the same edit.** The contract comment above the set
read *"These **four** files are not apparatus"* while the set has held **five**
members since Fold 5 added `dev/.cairn/model-selection-mapping.yml`; the prose was
never updated. F2 takes it to seven, and the set now spans two classes rather than
one -- adopter-*authored* project state (a roadmap, a handoff, a fold-back ledger,
a governance agreement) and adopter-*filled* configuration installed as an
unconfigured stub. Both are now described. The count is stated as a class
breakdown, not a bare number, so the next widening does not re-stale it.

**A plan defect found by measurement, not accepted from the plan.** Row F5(a)
states the record key set is `{src, dst, verbatim, hash}` plus `base_cache` /
`base_hash` "only where the branch that adds it is taken (substituted
destinations)". Measured: `bootstrap/_scaffold/install.py:1810-1811` writes
`base_hash` on the **verbatim** branch too, deliberately and with a comment
explaining why. So verbatim destinations carry five keys and substituted carry
six; after F2 the two policy destinations carry seven. The test asserts a
**per-destination** map for exactly this reason.

**Falsification ledger -- three mutants, each restored byte-exactly (verified by
`shasum -a 256` before and after).**

| # | Mutation | File mutated | Expected | Observed |
|---|----------|--------------|----------|----------|
| M1 | Remove F2's two entries from `_LIVING_STATE_DSTS` | `bootstrap/_scaffold/lockfile.py` | F2's tests go red -- the entries are load-bearing | 3 failed (`test_f5a_*`, `test_f2_1_*`, `test_f2_2_*`), 30 passed |
| M2 | Add an **engine** destination (`scripts/_api_access_security/net.py`) to the set -- F2-1's own deletion mutant | `bootstrap/_scaffold/lockfile.py` | F2-1's hazard half goes red: a tampered engine member verifies OK | 2 failed (`test_f2_1_*`, `test_hazard_a_tampered_engine_member_*`) |
| M3 | Drop the `_LIVING_STATE_DSTS` membership test -- F2-2's deletion mutant | `bootstrap/verify_integrity.py` | the illegal-opt-out row goes red, proving F-3 and F2-2 discriminate independently | 1 failed (`test_hazard_an_illegal_living_state_opt_out_*`), F2-2 passed as designed |

`bootstrap/_scaffold/lockfile.py` has **no template twin** (the only other copy on
disk is inside an untracked `.claude/worktrees/` scratch tree), so the
twin-mutation trap does not apply here -- checked rather than assumed.

**A vacuity trap avoided, and recorded because it was tempting.** The test file's
`_POLICY_DESTINATIONS` states the two paths **literally** rather than deriving them
from `_LIVING_STATE_DSTS`. Deriving them would have made F2-2 vacuous under its own
M1 mutant: remove the two entries, an engine-derived set goes empty, and every
assertion over it passes trivially. The cost of stating them is a possible desync
from the engine, which `test_f2_2_*` closes by asserting the literal set against
`_LIVING_STATE_DSTS` directly.

**Suites run.** `test_security_capability_install.py` 33 passed (31 from F5, 2 from
F2). `test_lockfile_module.py`, `test_upgrade.py`, `test_scaffold.py`,
`test_default_security_stance.py`, `test_module_merge_lockfile.py` -- 190 passed
together. The real `dev/.cairn/cairn-lock.yml` was confirmed untouched by the test
installs (`git status --short` on that path, empty).

**F2-3, the engine delta -- RECORDED, NOT RE-PINNED.** Isolated by running
`test_ast_attest.py` against the committed `HEAD` version of `lockfile.py` and then
against the F2 version, and diffing:

```
CHANGED   Assign:_LIVING_STATE_DSTS  in bootstrap/_scaffold/lockfile.py
          (baseline dc478efb072ed310 != 8b7ceb939c3633d6 -- NOT pure motion)
```

That is F2's entire contribution and it is exactly the delta F2-3 requires --
`Assign:_LIVING_STATE_DSTS` and nothing else new. `Assign:_LIVING_STATE_DSTS` is
**not** in `_ast_attest._UPDATE_ALLOWLIST`, so re-anchoring is a **Maintainer-run,
dry-run-verified direct correction that an implementing agent does not perform**
(`bootstrap/AST_BASELINE_RUNBOOK.md`). The baseline additionally carries CHANGED
entries from other concurrent streams; the Maintainer's run should derive the whole
expected CHANGED set against the committed baseline at that time rather than carry
the figure above forward.

### Known omissions and follow-ups, named rather than left implicit

* **The Security Review for F2 is owed**, per the correction section above.
* **No Boundary-B full suite in this pass.** Still owed for Chunks H, D and now F2
  and F3-F5. The tree has not been quiet long enough for a clean-commit run.
* **Chunk G is now unblocked** and has not been implemented.
* **`verify_integrity`'s success message calls every living-state file
  "adopter-authored"**, which is inaccurate for the two policy files
  (adopter-*filled configuration*). `bootstrap/verify_integrity.py` is outside this
  plan's declared paths -- the same boundary F5(c) drew for the extra-key gap -- so
  the wording was not changed here. Routed as a lasting truth.
* **`install.py:1797-1798`'s comment** carries the same "Adopter-authored project
  state" gloss. It delegates to `_LIVING_STATE_DSTS`'s own docstring, which this
  commit corrected, so the pointer is now accurate even though the gloss is lossy.
* **F2's two entries are the first members of `_LIVING_STATE_DSTS` with no witness
  in Cairn's own tree** -- Cairn selects neither capability, so neither path exists
  here, and F2's behaviour can only ever be exercised by a scaffold into a
  temporary target. The same blind-path shape as `[RB5-6]`.
