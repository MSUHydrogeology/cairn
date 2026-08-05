<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/dual-review.md doctrine/rationale.md doctrine/runtime-contract.md doctrine/coordination.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- cairn-accept: instruction-html-comment reason="The comment below explains to human readers and to the claim checker which cited paths are forward references this plan creates and which are deliberately non-resolving; it carries no directive to an agent and names no action to take." reviewer="Claude (author)" date=2026-08-04 -->
<!-- Three classes of cited path do not resolve today, and the allow directive
     below covers all three.  (a) FORWARD REFERENCES this plan creates -- the
     three shipped module files, their three adopter-tree destinations, the new
     test module, and the version-support ledger; each is also registered under
     `Proposed paths:` with the chunk that lands it.  (b) An ADOPTER-TREE path
     that never exists in Cairn's own tree: `scripts/run_security_audit.py` is
     where `python-security` installs its orchestrator, and Cairn does not
     install that module (settled by the `default-security-stance` Decision).
     (c) `templates/_probe.py`, the throwaway file `scan-coverage`'s own
     perturbation created and deleted; it was never committed and never will
     resolve, so it is a historical citation rather than a forward reference. -->
<!-- claim-check-allow: templates/modules/team-gated/portable-security-sweeps.md, templates/modules/team-gated/run_portable_security_sweeps.py, templates/modules/team-gated/portable_security_policy.json, dev/modules/portable-security-sweeps.md, scripts/run_portable_security_sweeps.py, scripts/portable_security_policy.json, bootstrap/tests/test_portable_security_sweeps.py, dev/measurement/gitleaks-version-support.md, scripts/run_security_audit.py, templates/_probe.py -->

# Plan: one measured offline sweep, and the apparatus that keeps it measured

**Source proposal**: `portable-security-sweeps` (accepted 2026-08-03 by
Maintainer Decision, *"as revised, with two conditions binding on the plan"*).
It currently sits under `dev/proposals/` as
`dev/proposals/archive/2026-08-03-codex-portable-security-sweeps.md` and moves to
`dev/proposals/archive/` when it archives.
**Status**: open
**Plan review**: required(**External**, security lens) — carried from the
proposal header *and re-imposed by the Decision in terms*: *"The plan carries
`required(External, security lens)` in its own right, and both conditions above
are in its scope; this Decision does not discharge that review."* **An Internal
round does not discharge this tier** (see *Plan review — the brief*). **No
implementation commit lands before the `## Plan review` section is in the tree.**
**Last update**: 2026-08-04
**Opened**: 2026-08-04

## Proposed paths

*Every path below is a forward reference this plan creates. Each line is the
path and when it materializes. Drop a line once the path resolves on disk.*

Proposed paths:
- `templates/modules/team-gated/portable-security-sweeps.md` — shipped module doctrine; Chunk A.
- `templates/modules/team-gated/run_portable_security_sweeps.py` — shipped stdlib runner; Chunk A.
- `templates/modules/team-gated/portable_security_policy.json` — shipped strict policy; Chunk A.
- `dev/modules/portable-security-sweeps.md` — Cairn's own installed copy; Chunk F.
- `scripts/run_portable_security_sweeps.py` — Cairn's own installed twin; Chunk F.
- `scripts/portable_security_policy.json` — Cairn's own installed twin; Chunk F.
- `bootstrap/tests/test_portable_security_sweeps.py` — the new behavioural test module; Chunk A onward.
- `dev/measurement/gitleaks-version-support.md` — the version-support evidence ledger; Chunk E.

## Source proposal

`portable-security-sweeps` settles one contract: **a team-gated, opt-in module
that installs a standard-library orchestrator, a strict JSON policy, and a fixed
adapter registry carrying exactly one adapter — Gitleaks, offline, with no
network flag — over two scan questions (current tree, committed history), under
the shared aggregate exit space `0 / 5 / 10 / 20` with precedence
`20 > 10 > 5 > 0`.** The module installs no scanner. The plan executes that
decision and does not re-litigate it.

### What survived the lifecycle — established before planning, because the original scope is gone

The artifact is long and the original §1–§6 no longer govern. Establishing the
surviving contract is the first act of planning, not a courtesy summary.

| Stage | What it did to the scope |
|---|---|
| Original proposal (§1–§6) | **Four adapters** — OSV-Scanner, Gitleaks, zizmor, Trivy — plus `--allow-network`, a network-egress disclosure, and an OSV/pip-audit overlap-labelling contract. |
| External Security Review r1 ([PS1]–[PS7]) | Two blocking findings; recommended **accept the contract, ship one adapter**. |
| Response r1 | **All seven accepted. The four-adapter v1 is withdrawn.** PS2's per-tool ambient-config claims were *measured*, and the measurement changed the design. |
| Revised proposal (2026-08-03) | **One adapter, Gitleaks.** `--allow-network` **deleted**. OSV/zizmor/Trivy are "not supported adapters and not names the policy accepts". Exactly **Gitleaks 8.30.1**. |
| Adoption amendment | *availability is not adoption*; a preset table stated as a **coordination requirement, not an independently implemented `_PRESETS` edit**; **HOLD before Decision** on the missing standing invocation path. |
| External Security Review r2 ([PS8]–[PS10]) | Two substantive findings: the threat model excluded repository-local `.git/config`; exact-version pinning made INCOMPLETE the steady state for most adopters. |
| Response r2 + Revised proposal r2 | **PS8**: a logging `git` shim found **two** transitive Git invocations, not one; the environment pins the *tier* via `GIT_CONFIG_COUNT`, not the symptoms. **PS9**: **two version modes** — reviewed full mode (source-owned exact set, the only mode that can reach CLEAN) and reduced-provenance current-tree mode. |
| External Security Review r3 | **NO BLOCKING FINDINGS.** |
| **Decision** | **ACCEPTED as revised, with two conditions binding on the plan.** |

**Where earlier text disagrees, the Decision wins.** Three consequences bind
this plan and are stated once, here:

1. **The Decision's Condition 1 escalates PS9's answer.** The revision's
   two-mode design is *"the starting point, not the end state"*; the plan must
   build the **apparatus** by which a version is *admitted, re-measured, and
   retired* — the Decision's words are *"the mechanism, not a one-off mode"*,
   and what it must make *"routine rather than heroic"* is rerunning the
   hostile-ambient-config and output-schema matrix against a candidate version,
   recording what was measured, and admitting or refusing on evidence. Chunk E
   is that mechanism, and it is why Chunk E is not merely a data table.
2. **The Decision's Condition 2 adds Cairn's own adoption to the scope.** Cairn
   installs and runs the module on its own tree. Two consequences the Decision
   records explicitly: Cairn takes on Gitleaks as a **dev/CI dependency of its
   own**, and the zero-dependency contract for *shipped runtime* is unchanged.
   Chunk F.
3. **The adoption HOLD is resolved and does not survive into the plan.** The
   standing invocation path exists — `security-verification-activation`,
   accepted the same day — and the Decision answers the "worth building at all"
   question affirmatively by directing adoption.

## Scope

Executes the accepted contract plus both Decision conditions, across eight
chunks and one Maintainer-only ceremony chunk. This plan adds **three rows to
the published install manifest** and **one changed symbol** to the scaffold
engine.

**Out of scope, fenced explicitly. Each line is a thing a reader might
reasonably expect to find here and will not.**

* **Preset rosters — `_PRESETS`, `_DEFAULT_ON_MODULES`. Not touched.** The
  adoption amendment's five-row selection table (`solo-greenfield` opt-in;
  `collaborative-team` and `high-rigor-legacy` baseline) is a **coordination
  requirement**, and its own sequencing rule put `default-security-stance`
  first. That proposal reached its Decision on 2026-08-03 and settled four
  changes, **none of which is the portable preset rows** — verified by reading
  its `## Decision` rather than assumed. The amendment's step 3 then permits
  this plan to add them *"only with explicit ordering and one shared AST-baseline
  accounting pass"*. **This plan declines that option** and defers the rows: the
  Decision's *What is accepted* paragraph names the module, the runner, the
  policy, the registry and the one adapter, and does not name a preset change;
  and adding `_PRESETS` to this plan's engine delta would enlarge the shared
  re-anchor union for work the Decision did not direct. The deferral has a home
  (*Lasting-truth migration*, LT-1).
* **The four withdrawn adapters.** OSV-Scanner, zizmor, Trivy — removed in
  revision r1 and *"not names the policy accepts"*. Each returns as its own
  proposal with its own executable chain, ambient-config execution evidence,
  network posture, output schema, and offline-CLEAN disposition.
* **Any network path.** `--allow-network` was deleted in revision r1. There is
  no network flag, no remote-data path, and no advisory cache in v1. A
  re-introduction is a new Decision, not a plan-time convenience.
* **`python-security` — its exit contract, Bandit / pip-audit policy, the
  missing `_run_tool` timeout (PS7), and the raw-output relay (PS3).** All four
  are owned by `dependency-advisory-coverage`, whose Part 3 the r2 review
  confirmed carries them. This plan neither edits nor waits on that artifact.
  The portable runner's own timeout and output-escaping controls are
  independent and land here.
* **External-tool installation.** The scaffold installs no scanner, and
  **executes no scanner during installation** — the revision refuses that
  explicitly, since it would move the executable trust root into the installer.
* **The lockfile schema.** Three new rows use the existing shape. No field is
  added, no version bumped.
* **The activation dispatcher itself.** `security-verification-activation` owns
  the default-on dispatcher, its `AGENTS.md` slot, and the registry data
  structure. This plan owns the **child side** — the runner's local/offline
  entry point and its validated JSON result document — plus, order-permitting,
  the one registry row (Chunk G, and see *Intra-cluster order* below).
* **Semgrep, CodeQL, govulncheck, cargo-audit, npm audit.** Documented choices
  in the proposal, never v1 adapters.

### Documentation / doctrine surface

* **Governing layer — one entry, serialized.** `AGENTS.md`'s *High-risk
  surfaces* list gains the new external-executable trust root. `AGENTS.md` is a
  serialized shared file; the edit lands at this plan's serialization point
  (Chunk H), not opportunistically, and its exact wording is proposed there
  rather than applied early. **No `doctrine/` change**: the rule this module
  obeys (a security gate is a tripwire, not a proof; a missing tool is never
  clean) is already written and unchanged, so the doctrine-evolution rate-limit
  in `doctrine/rationale.md` is not engaged by the plan. *(The proposal argued
  the rate limit was cleared anyway by the high-risk limb; the plan does not
  need to rely on that, because it changes no cross-project doctrine.)*
* **Descriptive / contract layer** — [`bootstrap/DEPENDENCY_BUDGET.md`](../../bootstrap/DEPENDENCY_BUDGET.md)
  (a new external-tool adapter category beside Exceptions 1 and 2) and
  [`bootstrap/SAFETY.md`](../../bootstrap/SAFETY.md) (the subprocess /
  external-executable / candidate-`.git/config` trust boundary). Chunk H.
* **Adopter-facing** — the shipped module doctrine
  (`templates/modules/team-gated/portable-security-sweeps.md`) owns selection,
  threat model, both version modes, exits, trust roots, suppressions, residuals,
  and the pinning remedy. [`docs/tool-usage.md`](../../docs/tool-usage.md) gains
  the runner's entry alongside the other module-gated tools.
* **Release-facing** — `CHANGELOG.md > Unreleased > Added`, one line, at the
  serialization point.
* **Deliberation layer** — this plan, its plan review, its code review, the
  version-support evidence ledger (`dev/measurement/gitleaks-version-support.md`),
  and the `dev/PLANNING.md` row-move that serializes the plan-open.
* **Adopter-installed files — three, and that is install-contract movement.**
  Treated as a contract change with its own acceptance criteria in Chunk A, not
  as a side effect of adding a module.

<!-- cairn:slot documentation-tier-home -->
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
plan's *Scope* must name the doctrine-surface touched (or an explicit
"no doctrine surface").
<!-- cairn:end documentation-tier-home -->

---

## The engine delta, the shared ceremony, and the Maintainer fence

**This section is load-bearing and is placed before the chunks because it
constrains all of them.**

### The declared symbol delta — measured, not quoted

`bootstrap/_scaffold/` is covered by an AST source-motion attestation:
`bootstrap/tests/fixtures/scaffold_ast_baseline.json`, verified inside the suite
by `bootstrap/tests/test_ast_attest.py` (two nodes:
`test_committed_baseline_accounted_for_across_the_engine_package` and
`test_ast_gate_passes_over_the_full_scaffold_module_set`). Re-measured for this
plan under the canonical interpreter `~/conda_envs/lhm/bin/python3.13`
(3.13.13), `as_of 2026-08-04`:

```
AST attestation OK — 174 baselined symbol(s) accounted for, unchanged
```

**174 entries total; 161 of the three declarable kinds** — `FunctionDef` 98,
`Assign` 53, `ClassDef` 10. The remaining 13 are `Import` 8, `Docstring` 1,
`Expr` 1, `If` 1, `If#2` 1, `Try` 1, which
`bootstrap/tests/_ast_attest.py`'s `_is_per_module_necessity` exempts in both
directions. That verification was run against a **HEAD-only copy** of
`bootstrap/_scaffold/*.py` extracted with `git show`, precisely because the live
working tree is not clean (below).

> **Declared delta for `portable-security-sweeps`:**
>
> ```
> CHANGED   Assign:_MODULE_MAPPINGS   (baseline digest 26957a8924042a0a)
> ```
>
> **Exactly one symbol. 0 MISSING, 0 DUPLICATE, 0 non-exempt NEW.**

**Derived by execution, not by reading.** A scratch copy of HEAD's
`bootstrap/_scaffold/` received the literal Chunk A4 registration — the
`"portable-security-sweeps"` key with its three `InstallSpec` rows inserted
before the `"architecture-review"` key in `_MODULE_MAPPINGS` — and
`_ast_attest.py verify` reported:

```
AST attestation FAILED — 1 non-pure-motion symbol(s):
  CHANGED   Assign:_MODULE_MAPPINGS  in .../config.py
            (baseline 26957a8924042a0a != 4f72dfcb7ce39f20 — NOT pure motion)
```

The post-change digest `4f72dfcb7ce39f20` is **not** a target — it is an
artifact of the probe's exact text and will differ from the shipped
registration. The *shape* is the claim: one CHANGED `Assign:`, nothing else.

**Why nothing else moves, stated so a reviewer can attack each line.**
`_MODULE_REQUIRED_TOKENS` in `bootstrap/_scaffold/config.py` is untouched —
this module declares **no required token**; its three files are one substituted
`.md` and two verbatim assets, and `KNOWN_TOKENS` (measured: `claim_check_command`,
`metrics_command`, `project_name`, `python_package`, `test_command`) gains
nothing. `_MODULE_SUPERSEDES` is untouched — this module supersedes nothing.
`_PRESETS` and `_DEFAULT_ON_MODULES` are out of scope by the fence above.
No engine function changes: registration is data.

### One ceremony, shared with the cluster

**Five accepted scopes edit `bootstrap/_scaffold/config.py`** —
`profile-parse-fail-open`, `default-security-stance`, `api-web-security-modules`,
`portable-security-sweeps`, and `security-verification-activation`. Four are
being planned in parallel with this one.

The re-anchor ceremony's value is a **falsifiable union of CHANGED symbols agreed
in advance**: any symbol outside the union is a stop-and-explain. A concurrent
engine change from an unplanned scope does not enlarge that union — it destroys
the property, because the discriminator stops discriminating.

**This plan therefore declares its delta above and asserts nothing about the
union.** The union is formed **by the Maintainer at ceremony time** from each
scope's declared delta. Three facts this plan can contribute to that formation,
each measured or read rather than assumed:

1. **The three module-adding cluster scopes collapse into one CHANGED symbol.**
   `portable-security-sweeps`, `api-web-security-modules`, and
   `security-verification-activation` all register modules, and a registration is
   an edit to the *same* `Assign:_MODULE_MAPPINGS` key. Their combined
   contribution to the union is **one** entry, not three. This is a property of
   the baseline's keying (bare symbol name, one entry per key) and reduces the
   ceremony's surface — it does **not** license any of them to skip declaring.
2. **The one-symbol self-service repair path exists but will almost certainly
   refuse.** `_MODULE_MAPPINGS` *is* in `bootstrap/tests/_ast_attest.py`'s
   `_UPDATE_ALLOWLIST` (line 141, alongside `_SKILLS_MAPPINGS`, `_CORE_MAPPINGS`,
   `install_onboarding`), so `update-symbol` is mechanically available for this
   delta alone. But its contract refuses (exit 4) when *"the live module set"*
   shows any other CHANGED / MISSING / DUPLICATE symbol. With four sibling scopes
   in flight — at least one of which (`default-security-stance`) must change
   `_PRESETS`, a symbol the allowlist does **not** admit — the one-symbol path is
   the exception, not the plan. **The plan does not depend on it either way**,
   because of the fence below.
3. **The working tree is already carrying another scope's delta.** Measured
   `as_of 2026-08-04` against the live tree, before this plan writes anything:
   `AST attestation FAILED — 3 non-pure-motion symbol(s)` —
   `FunctionDef:cmd_upgrade` (`bootstrap/_scaffold/upgrade.py`),
   `FunctionDef:forked_facade_findings` and
   `FunctionDef:format_forked_facade_warning`
   (`bootstrap/_scaffold/lockfile.py`). None is this plan's. An implementing
   agent who sees those three at Chunk A has **not** broken anything and must not
   "fix" them; they belong to `fork-advisory-semantics`. This is exactly the
   confusion the shared-ceremony framing exists to prevent, and it is recorded
   here so it is read rather than discovered.

### What is true regardless of intra-cluster order

* The delta is **one CHANGED `Assign:_MODULE_MAPPINGS`**, whether this plan lands
  first, last, or between siblings. Registration data does not interact.
* Chunk A's commit **turns the two AST suite nodes red**, and they stay red until
  the ceremony. That is the declared, expected state — not a regression, and not
  a licence to leave any *other* node red.
* Every non-AST gate must be green at every commit. If a suite node other than
  those two is red after a chunk, stop.
* The three manifest rows this plan adds are **additive**; they collide with no
  sibling destination. Verified `as_of 2026-08-04`: no `portable` path exists
  anywhere under `templates/`, `scripts/`, or `dev/modules/`.

### What is order-sensitive, named

* **The four count pins.** `bootstrap/tests/test_notice_install.py:75` (44
  `templates/**/*.py` manifest sources), `bootstrap/tests/test_notice_install.py:145`
  (95 manifest data rows), `bootstrap/tests/test_security_lint.py:291` (44
  `templates/**/*.py` on disk), and the prose figure at
  `bootstrap/security_check.py:74`. **Every module-adding cluster scope moves
  the same pins.** Whichever lands second must **re-read and re-measure**, never
  apply the arithmetic written here. Chunk A's acceptance criteria are written as
  *"re-measure, then assert"* for exactly this reason.
* **Chunk G — the activation registry row.** It cannot precede the dispatcher
  existing. Both branches are specified in Chunk G; neither is assumed.
* **The `dev/PLANNING.md` row-move and the `CHANGELOG.md` line** are serialized
  shared files; a second scope editing them concurrently is a merge conflict, not
  a correctness problem, and the standing rule already covers it.
* **Line citations into `bootstrap/_scaffold/config.py` are volatile and this
  plan deliberately carries none.** Observed while this plan was being written:
  a concurrent scope added 13 net lines to that file in a single edit, moving
  `_MODULE_MAPPINGS` from line 365 to 378 and `_MODULE_REQUIRED_TOKENS` from 793
  to 806. Every reference to that file here is therefore by **symbol name**, and
  the line citations that remain in this plan point at files no cluster scope
  claims. Re-read before applying any of them; the claim checker verifies a line
  is in bounds, never that it still says what a plan said it said.

### The Maintainer fence

> **An implementing agent must not perform any step in Chunk M, and must not run
> `bootstrap/tests/_ast_attest.py update-symbol`, `_gate_manifest.py produce`, or
> `_gate_reanchor.py` under any circumstance.** The re-anchor is the Maintainer's
> act. The implementing agent's obligation is to *report* — in the final commit
> body, the exact `AST attestation FAILED` line and the exact stale
> `FROZEN-MODIFIED` / `FROZEN-NEW` entries — and stop.

A second fence, for a different reason:

> **An implementing agent must not download, fetch, or install a Gitleaks
> binary.** The live-contract matrix (Chunk E, Chunk I) runs only against a
> binary the **Maintainer** has supplied at a stable path with its publisher
> checksum verified. Absent that, every live-contract test **skips loudly** and
> the plan's fake-executable tests carry the deterministic contract. Fake-tool
> green does not establish third-party CLI behaviour, and this plan never claims
> it does.

---

## Sequence

Chunk order is load-bearing. **A `.py` file cannot appear under `templates/`
without its `_MODULE_MAPPINGS` registration in the same commit** — the shipped
tree carries two live oracles that go red on an unregistered template script
(`test_every_templates_py_on_disk_is_release_scanned` and
`test_templates_py_count_is_pinned`, both in
[`bootstrap/tests/test_security_lint.py`](../../bootstrap/tests/test_security_lint.py),
landed by `scan-coverage` earlier today). Chunk A is therefore atomic and large
by construction; every later chunk grows the runner in place.

```
0. plan-open  -- this plan + the dev/PLANNING.md row-move            [commit pending]
   (plan review) -- required(External, security lens); NO code before it lands
1. Chunk A -- install-contract movement: three files, one registration [commit pending]
2. Chunk B -- the executable trust boundary (Gitleaks + Git)          [commit pending]
3. Chunk C -- the candidate-configuration boundary (argv + env)       [commit pending]
4. Chunk D -- structured output, the aggregate, the child contract    [commit pending]
5. Chunk E -- the version apparatus (Decision Condition 1)            [commit pending]
6. Chunk F -- Cairn adopts the module (Decision Condition 2)          [commit pending]
7. Chunk G -- the activation registry row (ORDER-SENSITIVE)           [commit pending]
8. Chunk H -- docs, contract records, and the serialized surfaces     [commit pending]
9. Chunk I -- the live-contract matrix                        [Maintainer-gated]
M. Chunk M -- MAINTAINER-ONLY: the shared AST re-anchor ceremony      [not an agent's]
```

**Every intermediate commit ships a module that is honest about what it has
not done.** The runner's adapter path returns INCOMPLETE with a named reason
until Chunk D completes it. Nothing in this plan ever ships a state where a leg
that did not run can render as CLEAN — which is the plan's single most important
structural property and the one an External reviewer should attack first.

---

### Chunk A — install-contract movement: three files land and the catalog registers them

**This chunk is a contract change, not a side effect.** It adds three rows to
`install_manifest()` — the published enumeration adopters depend on through
`scaffold.py --manifest` — and ships the first `.json` file Cairn has ever placed
under `templates/` (measured: `git ls-files templates | grep '\.json$'` is empty
`as_of 2026-08-04`).

| # | File | Change |
|---|------|--------|
| A1 | `templates/modules/team-gated/portable-security-sweeps.md` | **New.** Module doctrine: `Selected when:` / `Adds to:` header in the house shape (see `templates/modules/team-gated/python-security.md:1-11`); what the module is and is **not** (a self-audit tripwire on a trusted checkout, never a reviewer for untrusted PRs); the complete two-executable residual trust set; both version modes; the exit table; the suppression boundary; the pinning remedy; and the plain statement that a clean run is a tripwire, not a proof. Substituted (not verbatim). |
| A2 | `templates/modules/team-gated/portable_security_policy.json` | **New.** The v1 policy, exactly `{"schema": 1, "gitleaks": {"fingerprints": []}}`. Verbatim. No SPDX header — JSON carries no comment syntax, and the SPDX tests in [`bootstrap/tests/test_notice_install.py`](../../bootstrap/tests/test_notice_install.py) scope to `.py` sources (verified by reading `_manifest_py_sources`, which filters `src.endswith(".py")`). **A2's licence disposition is stated in Chunk H, not left implicit.** |
| A3 | `templates/modules/team-gated/run_portable_security_sweeps.py` | **New.** Verbatim, standard-library-only, SPDX MIT header in the first four lines. This chunk lands: the CLI (`--target`, `--policy`, `--json`, and the `security-verification` local/offline entry point); strict policy load + schema validation; strict version parsing and mode selection; the aggregate exit constants reusing the `python-security` space (`5` / `10` / `20`, mirroring `templates/modules/team-gated/run_security_audit.py:76-78`); the deterministic summary structure; and a single adapter-execution seam that returns **INCOMPLETE with the reason `adapter execution not yet enabled`**. No subprocess call exists in the file at this commit. |
| A4 | `bootstrap/_scaffold/config.py` | **The plan's entire engine delta.** Add `"portable-security-sweeps"` to the `_MODULE_MAPPINGS` dict, immediately before its `"architecture-review"` key: the doctrine spec (substituted, → `dev/modules/portable-security-sweeps.md`), the runner (`verbatim=True`, → `scripts/run_portable_security_sweeps.py`), and the policy (`verbatim=True`, → `scripts/portable_security_policy.json`). A comment states the two facts a later reader needs: the three files are **one complete mapping group** (an upgrade cannot advance part of the apparatus), and the module declares **no required token** — unlike the `"python-security"` key two entries above it. |
| A5 | `bootstrap/tests/test_notice_install.py` | Re-measure, then move, **both** pins: `test_manifest_has_the_expected_py_source_count` at `bootstrap/tests/test_notice_install.py:75` (44 → 45) and `test_notice_appears_in_manifest_data_row_count` at `bootstrap/tests/test_notice_install.py:145` (95 → 98). The message text on each already says *"if this moved intentionally, update this test"* — the update must also say **why** it moved, naming this plan. |
| A6 | `bootstrap/tests/test_security_lint.py` | Re-measure, then move `test_templates_py_count_is_pinned` at `bootstrap/tests/test_security_lint.py:291` (44 → 45). **A5's first pin and A6 must agree and move in the same commit** — the `scan-coverage` plan established that coupling and its message points at the sibling. |
| A7 | `bootstrap/security_check.py` | The comment at `bootstrap/security_check.py:74` reads *"42 entries are a subset of the manifest's 44"*. Re-measure and correct. Prose that outruns the gate is the defect class `scan-coverage` closed; do not leave it one commit behind. |
| A8 | `bootstrap/tests/test_portable_security_sweeps.py` | **New test module.** Deliberately a *new* file: it reads as `FROZEN-NEW` (allowed, recorded) to the gate manifest rather than `FROZEN-MODIFIED`, and it carries **no module-level `pytestmark`**, so its nodes do not register as `SKIP-XFAIL-NEW` (the defect `profile-parse-fail-open` measured in `bootstrap/tests/test_presets.py`). This chunk's nodes: the install/manifest/complete-group/collision matrix, the strict-policy matrix, and the version-mode classification matrix. |

**Tests landing in A8 — each with the perturbation that makes it RED.**

*Perturbing a test's own body validates the test. Only perturbing the hazard
validates the claim. Every perturbation below targets the subject or the
repository state.*

| Test | Hazard perturbation that makes it RED |
|---|---|
| `test_the_module_installs_exactly_three_files` — scaffold a `tmp_path` target selecting only this module; assert the three destinations exist and no fourth. | Delete one `InstallSpec` from A4's registration. |
| `test_the_three_files_are_one_complete_mapping_group` — assert an upgrade cannot advance the runner without the policy and doctrine. | Remove the policy spec from A4's group; the group check must refuse. |
| `test_the_module_declares_no_required_token` — a profile selecting only this module installs with **no** `python_package`, exit 0. | Add `"portable-security-sweeps"` to `_MODULE_REQUIRED_TOKENS`; the install must then refuse and the test go red. |
| `test_module_destinations_collide_with_nothing` — assert `install_manifest(modules=None)` has no duplicate destination. | Point A4's runner `dst` at `scripts/run_security_audit.py`; `install_manifest` must raise. |
| `test_adopt_module_and_upgrade_carry_the_whole_group` — `--adopt-module portable-security-sweeps` on a tree installed before it existed writes all three files and records all three in the lockfile. | Drop one file from the lockfile record; the integrity read must not report clean. |
| `test_policy_accepts_the_shipped_v1_document` — the byte content of A2 validates. | Change A2's `"schema"` to `2`; validation must refuse. |
| `test_policy_refuses_every_named_malformation` — parametrized: unknown top-level key, unknown key under `gitleaks`, duplicate JSON key, non-string fingerprint, duplicate fingerprint, empty fingerprint, oversized fingerprint, control character in a fingerprint, a newline in a fingerprint (the ignore-file line-injection case), an unsupported `schema`, and any attempt to name a path / argv / environment variable / executable / config file / baseline. | Delete the corresponding branch from the validator; the parametrized case must go red. **Each malformation gets its own case** so deleting one branch fails exactly one node, not a lump. |
| `test_policy_refusal_precedes_every_side_effect` — a malformed policy refuses **before** executable resolution and before any temp file is materialized. | Move the validation call after resolution in the runner; the test observes a resolution attempt and goes red. |
| `test_version_string_parsing_is_strict` — parametrized over `8.30.1` (accept), `v8.30.1`, `8.30`, `8.30.1-rc1`, `8.30.1\n`, `8.30.1 `, `8.30.01x`, a control character, non-ASCII digits (all refuse). | Relax the parser to `str.startswith` / a permissive regex; the refusing cases go red. |
| `test_mode_selection_maps_versions_to_modes` — `8.30.1` → full; another strict `8.x.y` → reduced; `9.0.0`, `7.9.9`, a prerelease, an unparsable string → no execution, INCOMPLETE. | Add `"8.31.0"` to the source-owned full-mode set without an evidence record; Chunk E's admission test (below) goes red, and this test's reduced-mode case goes red too. |
| `test_policy_cannot_select_a_version_or_mode` — a policy carrying `"version"`, `"mode"`, or `"versions"` refuses. | Read the version from the policy in the runner; the test goes red. |

**Acceptance criteria — Chunk A.**

* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests -q` → green **except
  the two declared AST nodes**, which report exactly
  `CHANGED Assign:_MODULE_MAPPINGS` and nothing else. **A third CHANGED symbol
  that is not attributable to a named sibling scope is a stop-and-explain, not a
  re-run.** Suite collection grows by A8's nodes and drops none. Baseline to
  re-measure at a clean HEAD before starting: **1601 passed, 0 failed, 0 skipped,
  0 xfailed**, `as_of 2026-08-03` (measured by the `profile-parse-fail-open`
  plan; not re-measured here because the live tree carries three sibling scopes'
  uncommitted work, which would make any figure taken now meaningless).
* **The install contract moved, deliberately, and by exactly three rows.**
  Capture `python bootstrap/scaffold.py --manifest` to a scratch file *before*
  A4; diff after. **Expected: exactly three added lines, zero removed, zero
  modified.** Baseline `as_of 2026-08-04`: **95 data rows** (the command emits 96
  lines including its header); target 98. A removed or modified row means the
  registration edited something it should only have appended to — stop.
* **Every count pin re-measured before it is moved.** Do not apply `44 → 45` and
  `95 → 98` from this text. Run the three channels — `git ls-files templates |
  grep '\.py$' | wc -l`, the working-tree glob, and `install_manifest(modules=None)`
  verbatim-`.py` — and assert all three agree at the new figure. Measured
  `as_of 2026-08-04`, all three agree at **44**; three channels disagreeing is a
  finding wherever it appears.
* **The release gate still passes and its figure moved by one.**
  `~/conda_envs/lhm/bin/python3.13 bootstrap/security_check.py` → `PASS`.
  `scan_targets()` is **74** `as_of 2026-08-04`; expected **75** after A4.
  Bandit's `errors` array must stay empty and the blocking count must stay zero
  (the gate blocks at MEDIUM+). **The runner's `subprocess` import lands in
  Chunk B, not here** — so this chunk's Bandit delta is zero, which is why the
  chunk is safe to land before the subprocess boundary exists.
* **The `.json` template source is the first of its kind — verify, do not
  assume.** Confirm it installs byte-for-byte (`verbatim=True`), that no
  extension-keyed filter drops it from the manifest, and that the post-scaffold
  unfilled-token scan does not run over it (`InstallSpec`'s own docstring in
  `bootstrap/_scaffold/config.py` says verbatim files are exempt — check that it
  holds for a non-`.py` verbatim asset, which has no prior instance).
* **Perturbation, RUN, ledger in the commit body.** Revert A4 alone, leaving A1–A3
  on disk; confirm **`test_every_templates_py_on_disk_is_release_scanned` and
  `test_templates_py_count_is_pinned` both go red**, naming
  `templates/modules/team-gated/run_portable_security_sweeps.py`. Restore;
  confirm `git diff bootstrap/_scaffold/config.py` is empty. This is the
  perturbation that establishes the atomicity claim the chunk ordering rests on —
  **it is derived by reading the two oracles for this plan and must be run, not
  assumed.** (The same mechanism was demonstrated by `scan-coverage`'s own P-C4,
  which made the count pin fail at 45 ≠ 44 with a transient
  `templates/_probe.py`.)
* **Channel note.** Subject: `install_manifest()` and `scan_targets()`. Oracle
  for the count pins: `git ls-files` and a `pathlib` walk of the working tree —
  neither of which the subject reads. Oracle for the policy matrix: JSON
  documents the test authors, never the validator's own output.

---

### Chunk B — the executable trust boundary

Establishes the two host executable trust roots. **This is the chunk that first
puts `subprocess` in a shipped file**, so it is also the chunk that moves the
Bandit LOW count.

| # | File | Change |
|---|------|--------|
| B1 | `templates/modules/team-gated/run_portable_security_sweeps.py` | Resolve `gitleaks` **once** from the trusted host environment. Reject when either the lexical or the resolved path is inside the target repository. Require a regular file with the executable bit. Record lexical path, resolved path, and the `--version` output. Package-manager symlinks are allowed **only** when both paths are outside the repository. |
| B2 | same | Resolve and validate `git` by the identical rules — it is the **second** trust root, invoked transitively by Gitleaks for the history leg, and it was absent from the original review's four-binary enumeration until the author's own execution found it. |
| B3 | same | Build the child `PATH`: full mode gets a minimal `PATH` containing **only** the verified Git directory; reduced mode gets an **off-tree empty directory**, so Git is neither resolved nor reachable. |
| B4 | same | Classification: a missing binary → **INCOMPLETE (5)**. Unsafe shape, repository containment failure, `--version` failure, or a path that drifts between validation and invocation → **DEGRADED (20)**. Never CLEAN, never silent. |
| B5 | same | Re-validate the resolved path immediately before `subprocess` invocation and record that the accepted residual is a same-user race on a trusted checkout, not a containment claim. |
| B6 | `bootstrap/tests/test_portable_security_sweeps.py` | The executable-boundary matrix, using fake executables written into `tmp_path`. |

**Tests landing in B6 — each with its hazard perturbation.**

| Test | Hazard perturbation that makes it RED |
|---|---|
| `test_absent_gitleaks_is_incomplete_not_clean` — empty `PATH`, no binary; assert exit **5** and that the report names the absence. | Change B4's absent-binary branch to return the CLEAN aggregate; the test goes red. **This is the plan's canonical "did not run must not read as clean" node.** |
| `test_absent_git_is_incomplete_for_the_history_leg` — Gitleaks present, Git absent. | Make the history leg optional-and-clean; red. |
| `test_a_repo_local_executable_is_refused` — plant an executable named `gitleaks` inside the target tree and put it first on `PATH`. | Delete the lexical containment check; the test observes the repo-local binary being invoked and goes red. |
| `test_a_symlink_resolving_into_the_repo_is_refused` — an outside-the-repo symlink whose target resolves inside. | Delete the *resolved*-path containment check (keeping the lexical one); red. This case exists **because** the lexical check alone passes it. |
| `test_a_package_manager_symlink_outside_the_repo_is_accepted_and_both_paths_recorded` | Make containment reject all symlinks; the legitimate case goes red — the test guards against over-refusal, which is the failure mode that makes a security control get disabled. |
| `test_a_non_executable_file_is_degraded` | Drop the executable-bit check; red. |
| `test_a_version_command_failure_is_degraded_not_incomplete` — the fake binary exits non-zero on `--version`. | Map version failure to INCOMPLETE; red. The distinction is the contract: *absent* is 5, *present but unsound* is 20. |
| `test_path_drift_between_validation_and_invocation_is_degraded` — replace the fake binary between the two moments. | Delete B5's re-validation; red. |
| `test_reduced_mode_child_path_is_an_empty_off_tree_directory` — capture the child environment. | Give reduced mode the full-mode `PATH`; red. This is the node that proves reduced mode cannot reach Git. |
| `test_full_mode_child_path_contains_only_the_verified_git_directory` | Pass the inherited `PATH` through; red. |

**Acceptance criteria — Chunk B.**

* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_portable_security_sweeps.py -q`
  → all pass, **0 skipped** (every node here uses a fake executable and needs no
  real Gitleaks).
* **The Bandit budget moves, and by a stated amount.** Re-run
  `~/conda_envs/lhm/bin/python3.13 bootstrap/security_check.py` and record the
  LOW delta. Expect the `subprocess` family — `B404` (import), `B603` (call with
  non-literal argv). **`B607` (partial executable path) must NOT appear**: this
  runner invokes an absolute resolved path by construction, and a `B607` finding
  is evidence that B1/B2 were not actually applied. **A MEDIUM-or-higher finding
  is a stop, not an allowlist entry** — the allowlist idiom in
  [`bootstrap/tests/test_security_lint.py`](../../bootstrap/tests/test_security_lint.py)
  requires a rationale, and "the security module needed it" is not one.
* **The two trust roots are enumerated, not generalized.** The module doctrine
  (A1) must name `gitleaks` and `git` as a list a reader can audit — the form the
  round-1 review asked for by analogy to how `bootstrap/REANCHOR_RUNBOOK.md`
  enumerates its own residual executable — and must say plainly that this is
  **shape and containment validation, not provenance**.
* **Channel note.** Subject: the resolution and validation functions. Oracle:
  filesystem state the test constructs (a planted binary, a symlink, a cleared
  bit) — none of it derived from the runner.

---

### Chunk C — the candidate-configuration boundary

The chunk the round-1 review's blocking finding [PS2] produced, and the one whose
design came from execution rather than documentation. **Every control below
exists because a probe contradicted the obvious design.**

| # | File | Change |
|---|------|--------|
| C1 | `templates/modules/team-gated/run_portable_security_sweeps.py` | Adapter-owned argv for both legs: off-tree `--config`, off-tree `--gitleaks-ignore-path`, `--ignore-gitleaks-allow`, `--redact=100`, `--no-color`, `--no-banner`, `--report-format json`, off-tree `--report-path`, archive/decode depths fixed at zero, and a Gitleaks `--timeout` strictly shorter than the outer `subprocess` deadline. **Policy contributes no argv.** |
| C2 | same | The runner-owned Gitleaks TOML config, materialized off-tree per run, extending the binary's built-in rules. Never copied from the repository; carries no policy-supplied TOML. |
| C3 | same | **The `.gitleaksignore` pre-execution refusal.** Walk the candidate tree without following symlinks; if **any** `.gitleaksignore` exists — regular file *or* symlink — refuse before execution with **DEGRADED (20)**. Required because Gitleaks 8.30.1 loads the target's ignore file *even when* `--gitleaks-ignore-path` names a trusted empty file, and exposes no observed switch to disable it. |
| C4 | same | Reviewed fingerprint suppressions are materialized from the validated policy, one per line, into an **off-tree temporary** ignore file. A candidate-tree suppression file never becomes policy by discovery. |
| C5 | same | The history leg's fixed `--log-opts`: `--all --full-history --text --no-textconv --no-ext-diff`. `--text` defeats a tracked `.gitattributes` `binary` rule that otherwise made a committed token invisible; `--no-textconv` and `--no-ext-diff` keep Git diff drivers from extending the scan into executable helpers. |
| C6 | same | The child environment: start from an allowlist; drop **every** inherited `GIT_*`, `GITLEAKS_*`, proxy, Python-import, pager and prompt variable; then set `GIT_TERMINAL_PROMPT=0`, `GIT_NO_REPLACE_OBJECTS=1`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=<off-tree empty file>`, `GIT_OPTIONAL_LOCKS=0`, and `GIT_CONFIG_COUNT=8` with ordered `GIT_CONFIG_KEY_0..7` / `GIT_CONFIG_VALUE_0..7` carrying `core.useReplaceRefs=false`, `core.hooksPath=<os.devnull>`, `core.fsmonitor=false`, `core.pager=cat`, `core.quotePath=false`, `diff.external=`, `protocol.allow=never`, `protocol.file.allow=never`. |
| C7 | same | The current-tree leg does not follow symlinks and does scan `.gitignore`d ordinary files. |
| C8 | `bootstrap/tests/test_portable_security_sweeps.py` | The hostile-fixture matrix. |

**Why C6 pins keys rather than symptoms — stated because it is the finding.**
`GIT_CONFIG_NOSYSTEM` and `GIT_CONFIG_GLOBAL` neutralize the system and global
config tiers. They do **not** neutralize the **repository-local** tier — the only
one the candidate controls. `GIT_CONFIG_COUNT` entries behave like `-c` and
outrank repository-local config, which matters precisely because *Gitleaks*
spawns Git, so the runner cannot pass `-c` itself. **This is a measured finite
boundary, not complete Git-config sterilization**, and the doctrine must say so
in those terms.

**Tests landing in C8 — each with its hazard perturbation.**

| Test | Hazard perturbation that makes it RED |
|---|---|
| `test_a_hostile_gitleaks_toml_does_not_suppress` — plant `.gitleaks.toml` in the fixture that would suppress the planted token. | Remove `--config` from C1; the fake tool records the absent flag and the test goes red. |
| `test_both_gitleaks_config_env_vars_are_dropped` — set `GITLEAKS_CONFIG` and `GITLEAKS_CONFIG_TOML` in the parent environment; capture the child's. | Switch C6 from an allowlist to a denylist that misses one; red. |
| `test_an_inline_gitleaks_allow_comment_does_not_suppress` | Remove `--ignore-gitleaks-allow`; red. |
| `test_a_candidate_gitleaksignore_refuses_before_execution` — plant `.gitleaksignore` anywhere in the tree; assert exit **20** and that **no subprocess was spawned**. | Delete C3's walk; the runner executes and the "zero invocations" assertion goes red. **Assert on the invocation count, not only the exit code** — an exit 20 reached *after* execution is a different, weaker control. |
| `test_a_gitleaksignore_symlink_also_refuses` | Make C3's walk follow or skip symlinks; red. |
| `test_a_nested_gitleaksignore_refuses` — plant it three directories deep. | Make C3 check only the repository root; red. |
| `test_a_tracked_gitattributes_binary_rule_cannot_hide_a_committed_token` — the `.gitattributes` `secret.txt binary` fixture. | Remove `--text` from C5; red. |
| `test_hostile_repo_local_config_loses_to_the_counted_keys` — set all eight pinned keys hostilely in `.git/config`, with executable sentinels for hooks, fsmonitor, external diff, pager and transport; assert **no sentinel executed**. | Drop `GIT_CONFIG_COUNT` from C6; a sentinel fires and the test goes red. |
| `test_every_inherited_git_variable_is_dropped` — seed the parent environment with a broad `GIT_*` set. | Change C6 to pass the parent environment through with overrides; red. |
| `test_the_current_tree_leg_does_not_follow_a_symlink_out_of_the_repo` — a symlink to an outside secret; assert **zero outside bytes** scanned. | Enable symlink following in C7; red. |
| `test_a_gitignored_ordinary_file_is_still_scanned` | Add a `.gitignore`-respecting filter to C7; red. |
| `test_policy_fingerprints_reach_an_off_tree_ignore_file_only` — assert the materialized file is outside the target tree and that no candidate file was read as an ignore source. | Materialize inside the target tree; red. |
| `test_a_fingerprint_cannot_inject_a_second_ignore_line` — a fingerprint containing `\n`. | Remove the newline branch from A8's validator; **this node and the A8 parametrized case both go red**, which is the intended belt-and-braces. |
| `test_the_gitleaks_timeout_is_strictly_inside_the_outer_deadline` — capture both. | Set them equal; red. Equal deadlines make the inner timeout unobservable. |

**Acceptance criteria — Chunk C.**

* Every C8 node passes with **fake executables**, and the fake tool asserts on
  the **exact argv and the exact child environment**, not on a substring.
* **The `.gitleaksignore` refusal is proved by invocation count, not exit code.**
  Named separately because it is the one control whose weaker form passes an
  exit-code-only assertion.
* **The residual is printed, not just documented.** The runner's own report must
  name the accepted delete/create race between the C3 walk and execution, and the
  test asserts the residual text is present in the human report — a residual that
  exists only in a doctrine file an adopter may never open is the shelf-artifact
  failure restated.
* **Channel note.** Subject: the argv/environment construction. Oracle: a fake
  executable that records what it actually received, plus filesystem fixtures the
  test plants. The runner never supplies its own oracle. **The limit, stated:
  fake-tool green establishes what Cairn *sends*; it establishes nothing about
  what Gitleaks *does* with it.** That is Chunk I's job and it is Maintainer-gated.

---

### Chunk D — structured output, the aggregate, and the child contract

| # | File | Change |
|---|------|--------|
| D1 | `templates/modules/team-gated/run_portable_security_sweeps.py` | Gitleaks writes redacted JSON to an **off-tree** report file. The runner checks the file's size **before** reading, parses with the standard library, validates the result-list shape and field types, and selects only rule ID, repository-relative path, line, commit/fingerprint, and scan leg. Secret, match, author, email and commit-message fields are **never** selected. |
| D2 | same | Every displayed string is serialized with `json.dumps(..., ensure_ascii=True)`, escaping C0/C1 controls, newlines, ANSI escapes and bidi code points rather than letting them become terminal controls. **No child stdout or stderr is relayed verbatim, ever.** Bounded, escaped stderr appears only as an opaque diagnostic on tool failure. |
| D3 | same | The deterministic JSON summary is written after both legs; the human report is a **rendering of that validated summary**, never of scanner text. |
| D4 | same | The aggregate: `0` CLEAN, `5` INCOMPLETE, `10` FINDINGS, `20` DEGRADED, precedence `20 > 10 > 5 > 0`. NOT APPLICABLE is distinct from INCOMPLETE and never weakens another leg. Non-Git export → current-tree leg runs, history leg INCOMPLETE. Shallow clone → the observed boundary is reported and full-history coverage is not claimed. |
| D5 | same | The reduced-mode classification: validated finding → **10**; validated no-finding → **5**, naming unsupported version and missing history evidence; CLI/output-schema drift → **20**; missing binary / other major / prerelease / unparsable → **5 without execution**. **Reduced mode never emits CLEAN and never describes itself as offline-verified.** |
| D6 | same | The `security-verification` child document: `{"schema": 1, "capability": "portable-security-sweeps", "contract": "portable-security-sweeps/local-v1", "evidence_mode": "offline", "result": …, "details": {…}}` — one bounded strict-UTF-8 JSON document, with `details` under its own bounded schema. |
| D7 | `bootstrap/tests/test_portable_security_sweeps.py` | The output-integrity, aggregate, and child-contract matrices. |

**Tests landing in D7 — each with its hazard perturbation.**

| Test | Hazard perturbation that makes it RED |
|---|---|
| `test_a_hostile_path_string_cannot_forge_a_report_line` — a fake tool emits a JSON result whose `File` carries ESC, a newline, and the literal text `[portable] CLEAN`; assert the rendered report contains `` and `\n` **escaped** and contains no line that reads as a status. | Replace D2's `ensure_ascii=True` rendering with plain interpolation; red. |
| `test_bidi_and_nul_in_a_result_field_render_escaped` | Same perturbation; a separate node so the control classes are individually pinned. |
| `test_no_child_stdout_or_stderr_is_relayed` — the fake tool writes forged status text to **both** streams. | Print `proc.stdout` in the runner — the defect the round-1 review cited in the existing `python-security` runner and told this one not to copy; red. |
| `test_an_oversized_report_is_degraded_and_never_read_whole` — a report exceeding the cap; assert exit **20** and that the runner did not read the whole file. | Read before checking size; red on the memory-bound assertion even if the exit code still happens to be 20. |
| `test_invalid_utf8_and_malformed_json_are_degraded` | Wrap the parse in a `try` that falls back to "no findings"; red. |
| `test_an_unknown_result_shape_is_degraded_not_clean` — a well-formed JSON document of the wrong shape. | Use `.get()` with defaults instead of validating; red. |
| `test_missing_redaction_is_degraded` — a result whose secret field is not redacted. | Drop the redaction assertion; red. |
| `test_an_undocumented_exit_code_is_degraded` | Treat unknown exits as clean; red. |
| `test_a_timeout_is_degraded_not_clean` | Remove the outer `timeout=`; the node hangs (fail by suite timeout) rather than passing — **note this explicitly in the ledger**: the perturbation's signature here is a hang, and a hang is the defect. |
| `test_signal_death_is_degraded` | Map negative return codes to the clean path; red. |
| `test_aggregate_precedence_over_every_pair` — parametrized over all ordered pairs of `{0, 5, 10, 20}`. | Reorder the precedence comparison to `10 > 20`; the pair cases go red. |
| `test_a_finding_is_not_hidden_by_an_incomplete_history_leg` — findings in the current tree, shallow history. | Make the aggregate take the *minimum*; red. **This node is the specific claim `20 > 10 > 5 > 0` exists to make.** |
| `test_not_applicable_is_distinct_from_incomplete` | Collapse NOT APPLICABLE into INCOMPLETE; red. |
| `test_a_shallow_clone_cannot_claim_full_history_coverage` | Drop the shallow detection; red. |
| `test_a_non_git_export_runs_the_current_tree_leg_and_reports_history_incomplete` | Refuse entirely on non-Git; red — over-refusal is also a defect. |
| `test_reduced_mode_never_emits_clean` — parametrized over every reduced-mode outcome. | Allow reduced mode to reach 0; red. **The single most important node in Chunk D.** |
| `test_the_child_document_matches_the_registry_contract_exactly` — schema, capability, contract, evidence_mode, result. | Change `evidence_mode` to `"local"`; red. |
| `test_the_child_cannot_emit_a_mode_or_capability_it_was_not_given` | Read `capability` from the policy; red — and A8's `test_policy_cannot_select_a_version_or_mode` goes red too. |

**Acceptance criteria — Chunk D.**

* Every D7 node passes with fake executables, **0 skipped**.
* **A parse of the runner's own report is not the oracle.** Every rendering
  assertion checks for the *escaped* form and for the *absence* of the raw
  control byte, so a renderer that strips rather than escapes fails too.
* **The child document is validated against the registry contract text, not
  against the runner's own constant.** Until Chunk G, the contract string is
  pinned as a literal in the test; after Chunk G it is pinned against the
  registry. Named because the pre-G form is the weaker one.
* **Channel note.** Subject: the parser, renderer and aggregate. Oracle: fake
  tool output the test authors byte by byte, plus a precedence table typed into
  the test. Neither is computed from the runner.

---

### Chunk E — the version apparatus (Decision Condition 1)

**This chunk exists because the Decision said the reduced-provenance mode is
"the starting point, not the end state" and asked for the *mechanism* by which a
version is admitted, re-measured, and retired.** A data table is not that
mechanism. What must become routine rather than heroic is *rerunning the
hostile-ambient-config and output-schema matrix against a candidate version,
recording what was measured, and admitting or refusing that version on evidence*.

| # | File | Change |
|---|------|--------|
| E1 | `templates/modules/team-gated/run_portable_security_sweeps.py` | The **source-owned** full-mode version set, initially `{"8.30.1"}`, with each member carrying the identifier of its evidence record. Not policy-controlled, not environment-controlled, not adopter-editable without editing reviewed code. |
| E2 | same | **`--verify-version-support <path-to-candidate-binary>`** — a public subcommand that runs the admission matrix against a candidate binary in throwaway fixtures and emits a structured evidence record to stdout. This keeps the complete mapping group at **three files** (the revision fixes it at three) while making the apparatus a first-class, testable public path rather than a runbook step. It runs the same hostile-ambient-config fixtures as Chunk C, the same output-schema validation as Chunk D, the Git-invocation oracle, and the end-to-end exits. **It never mutates E1** — admission stays a reviewed human code change. |
| E3 | same | The emitted record's fixed shape: candidate binary path + SHA-256 + declared source, platform, Gitleaks version, Git version, the exact observed Git invocation multiset, per-fixture hostile-config outcomes, the network-observation method and result, the output-schema result, and the end-to-end exit for each smoke scenario. |
| E4 | same | **Refusal rules for admission**, enforced by the subcommand, not by prose: a candidate that invokes an unaccounted Git subcommand, drops a required option, contacts a remote, or makes another local-config key security-relevant without a pinned or structural control emits a **refusing** record. The subcommand's exit code distinguishes "matrix passed, record emitted" from "matrix failed, do not admit". |
| E5 | `dev/measurement/gitleaks-version-support.md` | **New.** The evidence ledger: one section per admitted version, embedding the emitted record verbatim, plus the retirement log. Sits beside `dev/measurement/attestation-replay-failures.md` and `dev/measurement/review-floor-deviations.md`, which is where this repository already keeps measurement records. |
| E6 | `templates/modules/team-gated/portable-security-sweeps.md` | The **support cadence** as a contract, not an aspiration: at each Cairn release the Maintainer or a delegated Security Reviewer evaluates the newest candidate 8.x; a real-adopter reduced-mode report is *also* a trigger; promotion requires the full matrix plus a security-lens review of the recorded evidence; prior exact versions remain supported while their matrix passes; removal takes the same visible contract change and a migration note. Plus the honest interval statement: between updates an adopter gets useful current-tree findings and an honest INCOMPLETE, or pins a named full-mode release outside Cairn. |
| E7 | `bootstrap/tests/test_portable_security_sweeps.py` | The apparatus tests. |

**Tests landing in E7 — each with its hazard perturbation.**

| Test | Hazard perturbation that makes it RED |
|---|---|
| `test_every_full_mode_version_has_an_evidence_record_in_the_ledger` — parse E1's set and E5's ledger; assert a bijection. | Add `"8.31.0"` to E1 without a ledger section; red. **This is the node that makes Condition 1's apparatus binding rather than decorative.** |
| `test_the_ledger_names_no_version_absent_from_the_source_set` — the reverse direction; a retired version must move to the retirement log, not linger as an active section. | Leave a retired version in the active list; red. |
| `test_verify_version_support_emits_a_complete_record` — run E2 against a **fake** binary that satisfies the matrix; assert every E3 field is present and non-empty. | Delete a field from E3's emitter; red. |
| `test_verify_version_support_refuses_a_candidate_that_invokes_an_unaccounted_git_subcommand` — a fake Gitleaks that shells a third Git call. | Delete E4's invocation-set comparison; red. |
| `test_verify_version_support_refuses_a_candidate_that_drops_a_required_option` | Compare argv as a set-membership check instead of exact; red. |
| `test_verify_version_support_refuses_a_candidate_that_contacts_a_remote` — a fake binary that opens a socket. | Delete the network observation; red. |
| `test_verify_version_support_cannot_mutate_the_source_version_set` — run E2 against a passing fake for an unlisted version; assert E1 is byte-identical afterwards **and** that a subsequent ordinary run still classifies that version as reduced. | Make E2 write back to E1; red on both halves. **The second half matters: a mutation that is reverted before the assertion would pass a file-compare alone.** |
| `test_policy_cannot_promote_a_version` — a policy naming a version. | Read the set from the policy; red (and A8's node goes red too). |
| `test_reduced_mode_is_reachable_without_any_source_change` — a strict `8.x.y` outside the set executes the current-tree leg. | Refuse every unlisted version outright — the PS9 failure the Decision named as *shelf apparatus with extra steps*; red. |

**Acceptance criteria — Chunk E.**

* Every E7 node passes with **fake** binaries, `0 skipped`. The apparatus is
  testable without Gitleaks; only *admitting a real version* needs the real one.
* **The ledger is a gate, not a document.** `test_every_full_mode_version_has_an_evidence_record_in_the_ledger`
  must fail on a source-only addition. Confirm by running the perturbation.
* **The subcommand's refusal path is exercised at least four ways** (unaccounted
  subcommand, dropped option, remote contact, schema drift) — one refusal test is
  not evidence that refusal works.
* **What this chunk does not establish, stated plainly.** It establishes that the
  *apparatus* is correct against fakes. It establishes nothing about Gitleaks
  8.30.1's real behaviour. The only artifact that does is a record emitted by E2
  against a Maintainer-supplied, checksum-verified real binary — Chunk I.
* **Channel note.** Subject: E1's set, E2's matrix runner, E4's refusal rules.
  Oracle: fake binaries that deliberately violate one rule each, plus a ledger
  file the test reads independently of the source set.

---

### Chunk F — Cairn adopts the module (Decision Condition 2)

The Decision directs it: *"Cairn installs and runs this module on its own tree,
so the design is evaluated by use rather than by argument."* It is also what
makes Condition 1 testable — Cairn's own runs exercise the version apparatus,
**including the case where the installed Gitleaks is not the pinned one**.

| # | File | Change |
|---|------|--------|
| F1 | `dev/.cairn/profile.yml` | Add `portable-security-sweeps` to `modules_add` (the block at `dev/.cairn/profile.yml:21-24`), with a one-line comment naming the trust root it takes on, matching the existing entries' idiom. |
| F2 | `dev/.cairn/cairn-lock.yml` | Regenerated — **never hand-edited** (its header says so in terms). Regenerate with the documented command and commit the result. |
| F3 | `dev/modules/portable-security-sweeps.md` | **New**, installed. Cairn's own copy of the doctrine, substituted from A1. |
| F4 | `scripts/run_portable_security_sweeps.py` | **New**, installed. Byte-identical twin of A3 — bound by the existing `test_every_self_hosted_twin_stays_byte_identical_to_its_source` in [`bootstrap/tests/test_notice_install.py`](../../bootstrap/tests/test_notice_install.py), which discovers twins by globbing `*.py`. Carries the same SPDX MIT header (also already bound, by `test_every_self_hosted_twin_carries_spdx_header`). |
| F5 | `scripts/portable_security_policy.json` | **New**, installed. **No existing test binds this twin** — `_self_hosted_twins()` globs `*.py` only, verified by reading it. F6 closes that gap rather than leaving the policy free to diverge from its source. |
| F6 | `bootstrap/tests/test_portable_security_sweeps.py` | A parity node for the policy twin, and Cairn's own first-run node. |

**Tests landing in F6 — each with its hazard perturbation.**

| Test | Hazard perturbation that makes it RED |
|---|---|
| `test_the_policy_twin_is_byte_identical_to_its_template_source` | Change one byte in `scripts/portable_security_policy.json`; red. **This test exists because the `.py`-only twin helper does not cover it** — a real, measured gap, not a hypothetical. |
| `test_cairns_own_install_records_all_three_files_in_the_lockfile` — read `dev/.cairn/cairn-lock.yml`. | Remove `portable-security-sweeps` from `dev/.cairn/profile.yml` without regenerating; red. |
| `test_cairns_own_run_with_gitleaks_absent_is_incomplete` — execute `scripts/run_portable_security_sweeps.py` against Cairn's own tree with an empty `PATH`; assert exit **5** and a report naming the absent binary and the pinning remedy. | Make the absent-binary path exit 0; red. **This is the node that turns Condition 2 into evidence**: measured `as_of 2026-08-04`, `gitleaks` is **not on this host's `PATH`**, so 5 is Cairn's actual first-run result and the plan says so rather than implying a clean first run. |

**Acceptance criteria — Chunk F.**

* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests -q` → green except
  the two declared AST nodes.
* **Cairn's own first run is recorded as a figure, in the commit body**: the exact
  aggregate, the reason line, and the installed Gitleaks version or its absence.
  This is the Decision's *"first evidence about whether the module is usable
  rather than merely correct"* and it belongs in the durable record, not in a
  session.
* **The lockfile is regenerated, not edited.** Verify with
  `python bootstrap/verify_integrity.py` (or the documented equivalent) that the
  three new records validate.
* **Cairn's dev/CI dependency posture is stated, not implied.** Chunk H's
  `bootstrap/DEPENDENCY_BUDGET.md` entry must say that Cairn itself now carries
  Gitleaks as a dev/CI tool, and that this does **not** change the
  zero-dependency contract for shipped runtime — the Decision records both halves
  and the budget file is where they become checkable.
* **Explicitly not done here.** No CI workflow is edited. No scanner is
  installed. Cairn's standing verification cadence is `security-verification-activation`'s
  surface, reached through Chunk G.
* **Channel note.** Subject: the installed twins and Cairn's own lockfile.
  Oracle: a byte-compare against the template sources, and the lockfile file read
  independently of the installer.

---

### Chunk G — the activation registry row (ORDER-SENSITIVE)

`security-verification-activation` was accepted the same day and its Decision
established the ordering in terms: it is *"the dependency root for
`api-web-security-modules` and `portable-security-sweeps`; their invocation
contract is defined here."* Its registry admission rule requires, among other
things, an accepted capability proposal, a reviewed plan with public-path
execution evidence for the exact `evidence_mode`, a complete lockfile mapping
group, child output-schema and exit-precedence tests, and a Security Review of
the registry change. **Chunks A–F produce every one of those inputs**, which is
why this chunk sits after them regardless of which plan lands first.

**Branch 1 — the activation dispatcher and its registry are already in the tree.**

| # | File | Change |
|---|------|--------|
| G1 | the activation module's registry source *(path owned by that plan)* | One entry: module ID `portable-security-sweeps`, runner path `scripts/run_portable_security_sweeps.py`, the exact local/offline argv, the accepted child result schema and exit mapping, and `policy required: true` with its mapping group. |
| G2 | `bootstrap/tests/test_portable_security_sweeps.py` | The registry-conformance node, and the **deletion mutant** the adoption amendment requires. |

**Branch 2 — the dispatcher does not exist yet.** Chunk G does **not** land. The
plan records the row's exact content in this section for the activation plan to
consume, adds no dormant entry (that plan's rule forbids one for an uninstalled
capability), and the deletion-mutant obligation transfers to whichever plan lands
second. **Neither branch is assumed; the implementing agent reads the tree and
picks.**

| Test | Hazard perturbation that makes it RED |
|---|---|
| `test_the_registry_row_matches_the_child_document` — the registry's `contract` / `capability` / `evidence_mode` equal what the runner emits. | Change `evidence_mode` on either side; red. Both directions, so the row and the runner cannot drift apart silently. |
| `test_the_standing_command_includes_the_portable_leg` — **the deletion mutant**: remove the registry row and assert the standing verification command no longer reaches the portable runner **and that a test fails**. | The perturbation *is* the deletion; the node is red when the row is absent. This is the amendment's explicit requirement — *"the selected standing verification surface actually containing the command, with a deletion mutant that fails its test"*. |
| `test_the_registry_cannot_reach_a_network_or_credential_mode` — assert the row names only the offline entry point. | Add a second argv variant to the row; red. |

**Acceptance criteria — Chunk G.**

* Under Branch 1: all three nodes pass, and the deletion mutant is **run**, with
  its ledger in the commit body.
* Under Branch 2: this section is left in place, the chunk is marked *not landed
  — deferred to `security-verification-activation`'s plan*, and LT-2 in
  *Lasting-truth migration* carries it.
* **This chunk changes an executable trust boundary reachable from a standing
  agent command.** It is the single most review-sensitive commit in the plan and
  the External security reviewer should be pointed at it by name.

---

### Chunk H — docs, contract records, and the serialized surfaces

| # | File | Change |
|---|------|--------|
| H1 | [`bootstrap/DEPENDENCY_BUDGET.md`](../../bootstrap/DEPENDENCY_BUDGET.md) | A new **external-tool adapter** category beside Exception 1 (`bandit` + `pip-audit`, at `bootstrap/DEPENDENCY_BUDGET.md:17`) and Exception 2 (`vermin`, at `bootstrap/DEPENDENCY_BUDGET.md:97`). It must state four things and be checkable on each: **what is assumed installed** (Gitleaks at an admitted exact version, and Git, which Gitleaks invokes transitively); **what happens when it is absent** (INCOMPLETE, exit 5, loudly, never clean); **why this is not a new dependency** (the scaffold installs no scanner and executes none during installation; the shipped runtime stays standard-library-only; the tool is an adopter-selected dev/CI dependency acquired only by selecting the module); and **what Cairn itself took on** under Decision Condition 2. It must also carry the no-network statement — unlike Exception 1's pip-audit, this adapter has **no** egress path and no `--allow-network`. |
| H2 | [`bootstrap/SAFETY.md`](../../bootstrap/SAFETY.md) | The subprocess / external-executable trust boundary: the two host trust roots; `PATH` resolution as execution authority (**new to this module family** — the existing `python-security` runner executes `[sys.executable, "-I", "-m", …]` and uses `which()` only as presence detection); repository-local `.git/config`, refs, shallow boundaries and remote metadata as **candidate-controlled input**; the measured-finite nature of the Git-config boundary; and the accepted preflight/execution race. |
| H3 | [`docs/tool-usage.md`](../../docs/tool-usage.md) | A section in the file's existing per-tool shape, gated as `*(team-gated: portable-security-sweeps)*`: the installation check, the runner command, the offline/default behaviour, both version modes, and how to read `0 / 5 / 10 / 20`. |
| H4 | `AGENTS.md` > *High-risk surfaces* — **SERIALIZED** | One bullet naming the module's executable trust root, in the shape of the existing *local interpreter binding* entry. **Proposed wording is drafted in the commit message and applied at the plan's serialization point**, not opportunistically mid-plan. |
| H5 | `CHANGELOG.md > Unreleased > Added` — **SERIALIZED** | One line: a team-gated, opt-in cross-language security-sweep module shipping a standard-library orchestrator and strict policy with one offline adapter; **no scanner is bundled**. Cross-link proposal and plan by stem. |
| H6 | `dev/PLANNING.md` — **SERIALIZED** | The one-line row-move that serializes the plan-open (at plan-open, not here) and the archive move (at archive). |

**Acceptance criteria — Chunk H.**

* `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py` → OK. **180 Markdown
  files `as_of 2026-08-04`**; the count may only grow (this plan adds at least
  three: the plan, the shipped doctrine, the ledger — and one more when Cairn's
  installed copy lands in Chunk F).
* `~/conda_envs/lhm/bin/python3.13 scripts/quality_gate.py --sub neutrality` →
  unchanged. `templates/` and `bootstrap/*.md` are inside its scan roots, so the
  new doctrine passes through it. **"Gitleaks" and "Git" are tool names, not AI
  model or vendor names**, so the neutrality rule is not engaged — confirm rather
  than assume, since a moved figure here is a finding.
* `~/conda_envs/lhm/bin/python3.13 scripts/claim_check.py <file>` over each
  authored Markdown file, **one file per invocation** (the checker exits 2 on
  more than one path).
* **Re-read every quoted line before editing.** H1 and H2 quote line-cited
  sentences in files that sibling scopes may have moved. Do not apply this plan's
  text blind.
* **The licence split is stated for the three new files** (`AGENTS.md` >
  *Project-specific conventions* keeps code MIT wherever it lives, prose and
  document templates CC BY 4.0, the brand mark CC BY-ND): the runner is code
  (MIT, SPDX header); the doctrine is a document template (CC BY 4.0); **the
  policy JSON is the ambiguous one** — it is a data asset with no comment syntax
  and therefore no header. Chunk H states its disposition explicitly rather than
  letting the first `.json` under `templates/` set an unexamined precedent.

---

### Chunk I — the live-contract matrix *(Maintainer-gated)*

**No implementing agent starts this chunk.** It requires a real Gitleaks binary,
which requires a download, which is the Maintainer's to authorize and perform.

* The Maintainer supplies a checksum-verified Gitleaks binary at a **stable**
  path. *(Measured `as_of 2026-08-04`: the binary the proposal's probes used sits
  at `/private/tmp/gitleaks-8.30.1/gitleaks` — a system temp directory that is
  wiped, so it is not a stable path and this plan does not depend on it.
  `gitleaks` is not on this host's `PATH`; `git` is 2.53.0.)*
* Chunk E's `--verify-version-support` runs against it and emits the evidence
  record; the record lands in `dev/measurement/gitleaks-version-support.md` (E5).
* The live-contract test nodes — the logging-`git`-shim invocation oracle
  (expecting exactly `git -C <repo> log -p -U0 --all --full-history --text
  --no-textconv --no-ext-diff` and `git ls-remote --quiet --get-url`, and
  **zero** Git calls from the current-tree leg), the hostile-config matrix, and
  the four end-to-end smoke scenarios — run **only** when that binary is present
  and **skip loudly** otherwise, naming what was not established.
* The end-to-end smoke set: a non-Python Git fixture with one current-tree and
  one history-only planted token → both found, network denied; tokens removed →
  offline **0**; shallow clone → **5**; hostile `.gitleaksignore` → **20**; all
  tooling absent → **5**.

**Acceptance criteria — Chunk I.** The evidence record exists in the ledger for
every version in E1's full-mode set, **or** E1's set is empty and the module
ships reduced-mode-only. There is no third state: a version in the set without a
record is exactly what E7's bijection node makes impossible.

---

### Chunk M — MAINTAINER-ONLY: the shared AST re-anchor ceremony

> **An implementing agent must not perform any step in this chunk.**

1. **This plan's declared contribution to the union is one entry:**
   `CHANGED Assign:_MODULE_MAPPINGS`, baseline digest `26957a8924042a0a`.
   0 MISSING, 0 DUPLICATE, 0 non-exempt NEW.
2. **The union is the Maintainer's to form** at ceremony time from every
   participating scope's declared delta. This plan asserts nothing about the
   other four scopes' contributions and does not compute a combined target.
3. **Two mechanisms are available and the choice is the Maintainer's.** The
   one-symbol `_ast_attest.py update-symbol` path admits `_MODULE_MAPPINGS`
   (`bootstrap/tests/_ast_attest.py:141`) but refuses (exit 4) when any unrelated
   baselined symbol differs — which is the expected state in a shared ceremony.
   The general mechanism is the Maintainer-run, dry-run-verified direct-correction
   script established by `lockfile-provenance-fields` and used by
   `profile-parse-fail-open`.
4. **Verification after the ceremony** (the Maintainer's, and the only thing that
   closes the red window):

   ```
   ~/conda_envs/lhm/bin/python3.13 bootstrap/tests/_ast_attest.py verify \
       bootstrap/tests/fixtures/scaffold_ast_baseline.json bootstrap/_scaffold/*.py
   ~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_ast_attest.py -q
   ```

   Expected: `AST attestation OK — <N> baselined symbol(s) accounted for,
   unchanged`, and both suite nodes green. `<N>` stays **174** for this plan's
   delta alone (a digest rewrite adds no key); a sibling adding a top-level symbol
   moves it, which is that scope's figure to declare, not this one's.
5. **Gate-manifest consequence, reported not repaired.** After Chunks A–H the
   committed `bootstrap/tests/fixtures/gate_manifest.json` (164 frozen files,
   `as_of 2026-08-04`) goes stale: `FROZEN-MODIFIED` for
   `bootstrap/security_check.py`, `bootstrap/tests/test_notice_install.py` and
   `bootstrap/tests/test_security_lint.py`, and `FROZEN-NEW` for
   `bootstrap/tests/test_portable_security_sweeps.py` and the three shipped module
   files. The manifest is **not** read by the suite (verified: only the batch
   tooling reads the committed fixture), so nothing goes red — but the
   implementing agent names every stale entry in the final commit body and
   re-pins nothing. Note also that the tree already carries an inherited
   `HOLD` delta from earlier commits; this plan adds to it and does not dispose
   of it.

---

## Acceptance criteria

Per-chunk criteria are above; these are the plan-level deliverables.

* **Tests that must pass.**
  * `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests` — the whole
    suite, **0 failed / 0 skipped / 0 xfailed**, under the canonical interpreter
    (3.13.13) with `PYTHONDONTWRITEBYTECODE=1`, **with the two declared AST nodes
    excepted between Chunk A and the ceremony**. Re-measure the baseline at a
    clean HEAD before Chunk A; the last recorded figure is **1601 passed**,
    `as_of 2026-08-03`.
  * `bootstrap/tests/test_portable_security_sweeps.py` — the new module's whole
    matrix: install/manifest/complete-group (A8), executable boundary (B6),
    candidate-config (C8), output/aggregate/child contract (D7), version
    apparatus (E7), Cairn's own adoption (F6), and the registry row (G2, Branch 1
    only).
  * [`bootstrap/tests/test_notice_install.py`](../../bootstrap/tests/test_notice_install.py)
    and [`bootstrap/tests/test_security_lint.py`](../../bootstrap/tests/test_security_lint.py)
    — green with re-measured pins; the two 44-pins must agree and move together.
  * [`bootstrap/tests/test_manifest.py`](../../bootstrap/tests/test_manifest.py)
    — unchanged and green; its `test_matches_actual_install` scaffolds **every**
    module, so it is the node that catches a registration whose sources do not
    exist or whose destinations collide.
  * **Every new node shown non-vacuous by a RUN perturbation of the hazard**, with
    the ledger — the change made, the failure observed with its message, the
    byte-identical restore verified by an empty `git diff <path>` — in the commit
    body. Where a node's perturbation signature is a hang rather than a failure
    (D7's timeout node), say so instead of claiming a clean red.
* **Doc updates that must land.** All hand-authored: the shipped module doctrine
  (A1, E6), `bootstrap/DEPENDENCY_BUDGET.md`, `bootstrap/SAFETY.md`,
  `docs/tool-usage.md`, the version-support ledger, plus the serialized
  `AGENTS.md` bullet and `CHANGELOG.md` line. **No generated docs, no
  snippet-synced blocks** — verified: nothing under `templates/modules/` is a
  `sync_doc_snippets.py` target.
* **Examples / smoke checks required.**
  `python bootstrap/scaffold.py --manifest` → **exactly three added rows**.
  `python bootstrap/security_check.py` → `PASS` with the shipped-file count up by
  one and zero MEDIUM+. The four end-to-end scenarios in Chunk I — **N/A until a
  Maintainer-supplied binary exists**, and that N/A is stated in the record rather
  than left as a silent gap. **N/A**: the `examples/` gallery — this change
  demonstrates nothing the runnable examples cover.
* **Inbound path-link updates.** None expected. `dev/PLANNING.md` and
  `dev/NEXT_SESSION.md` refer to plans by filename stem, not path link, so the
  archive-move needs no edit there. Confirm at archive time rather than assume.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants, each with the chunk and node that enforces it.**
  * *No adapter executes through a shell, and no policy value ever becomes argv,
    an environment variable, a path, or an executable name.* Chunk A8's policy
    matrix + Chunk C8's argv/environment capture.
  * *A leg that did not run never renders as CLEAN.* Chunk B6
    (`test_absent_gitleaks_is_incomplete_not_clean`), Chunk D7
    (`test_reduced_mode_never_emits_clean`), and the precedence table.
    **This is the plan's central claim and it has three independent enforcers.**
  * *Candidate-tree content cannot choose the executable, the configuration, or a
    suppression.* Chunk B6's containment nodes + Chunk C8's hostile fixtures +
    C3's pre-execution refusal.
  * *Repository-local `.git/config` cannot steer the transitive Git process on any
    of the eight pinned keys.* Chunk C8's `test_hostile_repo_local_config_loses_to_the_counted_keys`.
    **Bounded, not complete**: it pins eight named keys against a measured
    invocation set, and the doctrine says so.
  * *No raw child output reaches the operator.* Chunk D7's rendering nodes.
  * *A full-mode version exists only with a recorded evidence record.* Chunk E7's
    bijection node.
  * *The three module files are one complete mapping group.* Chunk A8.
  * *The published manifest grows by exactly three rows and loses none.* Chunk A's
    diff-against-a-pre-change-capture criterion. **Not guarded by a test that goes
    red on a later removal** — the count pin at
    `bootstrap/tests/test_notice_install.py:145` would, and that is the honest
    answer, but it is a count and not a set comparison. Named as the weakest
    invariant here, and the one an External reviewer should attack.
* **Public-path → test mapping.** The runner's public entry points are its CLI
  (`__main__` / `main()`), its `security-verification` local/offline entry, and
  `--verify-version-support`. **All three are exercised by subprocess through
  their real public paths**, not by importing internals: A8/B6/C8/D7 drive the
  CLI, D7 drives the child-document path, E7 drives the verify subcommand. Fake
  executables are the *input*, never the oracle. The scaffold's public paths
  (install, `--manifest`, `--adopt-module`, `upgrade`) are exercised through their
  existing CLIs in A8 and F6.
* **Failure modes.**
  * Gitleaks absent, Git absent, shallow clone, non-Git export → **INCOMPLETE (5)**,
    loudly, never clean.
  * A validated finding, in either leg or either mode → **FINDINGS (10)**, and
    precedence keeps it visible over an incomplete sibling leg.
  * Unsafe executable, containment failure, version-command failure, path drift,
    candidate `.gitleaksignore`, invalid policy, malformed/oversized/invalid-UTF-8
    output, unknown result shape, missing redaction, undocumented exit, timeout,
    signal death → **DEGRADED (20)**.
  * A conditional leg with no applicable input → **NOT APPLICABLE**, with the
    discovery inputs printed; it never weakens another leg.
  * A candidate ambient configuration that cannot be disabled → **refuse**, do not
    run with unknown suppression policy. That is the proposal's own recovery rule
    applied before shipping rather than after.
* **Edge cases handled.** Empty repository; shallow clone; detached HEAD;
  non-Git source export; a linked worktree's config; monorepo layouts; a
  `.gitattributes binary` rule; `.gitignore`d ordinary files; a symlink pointing
  out of the tree; a nested and a symlinked `.gitleaksignore`; a repository-local
  executable earlier on `PATH`; oversized output; invalid UTF-8; a filename
  carrying ESC / newline / bidi controls; intentionally committed test secrets
  (surfaced, then suppressed by reviewed fingerprint only).
* **Known omissions, stated rather than implied.**
  (a) **v1 does not authenticate host binaries.** Gitleaks and Git are declared
  executable trust roots; a project needing provenance pins and verifies them
  outside Cairn.
  (b) **No process containment.** A malicious scanner is not contained, and the
  reduced mode in particular executes a binary whose behaviour has not received
  Cairn's matrix — absence of new egress or child execution is *not* established
  there.
  (c) **Gitleaks' built-in rule corpus is trusted as part of that binary**, not
  independently hash-pinned; detection quality is not evaluated by this plan.
  (d) **The Git-config boundary is finite**, not complete sterilization: eight
  pinned keys against one measured invocation set on one version and one
  platform.
  (e) **Cross-platform behaviour is unestablished.** All evidence is Darwin
  arm64.
  (f) **The preflight/execution race** on a trusted checkout is accepted and
  printed.
  (g) **Preset selection is deferred** (LT-1), so v1 ships a module no preset
  selects — availability without preset-level adoption, which the adoption
  amendment warned about and which Condition 2 partially answers by making Cairn
  itself the first adopter.
  (h) **No human has security-read the shipped runner line by line** at plan
  time; Bandit's verdict is a different thing.

## Verification

Run under the canonical interpreter (`~/conda_envs/lhm/bin/python3.13`, 3.13.13)
with `PYTHONDONTWRITEBYTECODE=1`; a different Python minor silently changes both
the suite figure and the AST digests.

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

**Plan-specific gates, added because this change touches those surfaces.**

* **The release Bandit gate** — `python bootstrap/security_check.py`. Expected
  `PASS`; the shipped-file count moves **74 → 75** (`as_of 2026-08-04`); zero
  MEDIUM+; **no `B607`**.
* **The install-contract assertion** — `python bootstrap/scaffold.py --manifest`,
  diffed against a capture taken at the plan-open commit. **Expected: exactly
  three added rows.** 95 data rows `as_of 2026-08-04` → 98.
* **The AST attestation** — `python bootstrap/tests/_ast_attest.py verify
  bootstrap/tests/fixtures/scaffold_ast_baseline.json bootstrap/_scaffold/*.py`.
  Expected between Chunk A and the ceremony: **`AST attestation FAILED — 1
  non-pure-motion symbol(s)`** naming `CHANGED Assign:_MODULE_MAPPINGS` and
  nothing else *attributable to this plan*. Sibling scopes' CHANGED symbols may
  also appear; each must be attributable to a named scope, and one that is not is
  a stop-and-explain.
* **The three-channel count agreement** — `git ls-files templates | grep '\.py$'
  | wc -l`, the working-tree glob, and `install_manifest(modules=None)`
  verbatim-`.py`. All **44** `as_of 2026-08-04`; all **45** after Chunk A. A
  disagreement is a finding wherever it appears.
* **The gate-integrity note** — after the last chunk, record in the commit body
  the exact `FROZEN-MODIFIED` and `FROZEN-NEW` entries this plan creates. **Do
  not re-pin**: that is a supervised act.
* **The perturbation ledgers** — per chunk, in the commit body: the change made,
  the failure observed with its message, and the byte-identical restore verified
  with `git diff <path>` (empty).

## Plan review — the brief

**Declared tier: `required(External, security lens)`.** Carried from the
proposal header and re-imposed by the Decision, which says in terms that the
Decision *does not discharge it*.

**Does an Internal round discharge it? No.** Internal review's floor is the same
agent in a fresh session; External's floor is a different agent type or a human.
This plan's central claims are (i) that a leg which did not run can never render
as clean, (ii) that candidate-controlled repository content cannot steer an
executable, its configuration, its suppressions, or the operator's terminal, and
(iii) that a version outside the measured set cannot produce CLEAN. Those are the
claims the proposal's three External rounds attacked, and two of them were
falsified by *execution* rather than argument — the `.gitleaksignore` file loads
even when `--gitleaks-ignore-path` names a trusted empty file, and a logging Git
shim recorded two invocations where every prior artifact, including the
reviewer's, said one. **An Internal round may sharpen this plan and is welcome;
it does not close the tier, and implementation does not start on one.**

**Where the reviewer should look first, in order.**

1. **Chunk G** — the registry row is the one commit that makes new executable
   bytes reachable from a standing agent command.
2. **Chunk C** — whether the eight pinned Git-config keys plus one measured
   invocation set actually bound the candidate metadata surface, or only the
   symptoms enumerated so far. The r2 review's PS8 made exactly this argument and
   the answer is *"a measured finite boundary"*; a reviewer should test whether
   that framing survives contact with a second Git subcommand.
3. **Chunk E** — whether `--verify-version-support` is genuinely an apparatus
   (admits, re-measures, retires on evidence) or a matrix runner with a ledger
   bolted on. Condition 1 asked for the mechanism.
4. **Chunk B/D reduced mode** — whether automatically executing an unmeasured
   host binary is acceptable given the named residual, which is the question the
   r2 revision itself put to its reviewer.
5. **The weakest invariant, named by the author**: the manifest grows by exactly
   three rows and loses none, guarded by a diff and a count pin, not by a set
   comparison.

## Code review

*Filled in after implementation commits land.* See `doctrine/plans.md` >
"Code review" for the full doctrine: falsification ledger, coverage line,
reviewer identity (not the implementing agent), and the append-only rule.

## Lasting-truth migration

*Filled in at archive time — but each deferred follow-up's durable home is
**pre-declared here**, so an archive is a check rather than a scramble.*

| ID | Deferred item | Durable home |
|---|---|---|
| LT-1 | **Preset selection for portable sweeps** — the adoption amendment's five-row table (`collaborative-team` and `high-rigor-legacy` baseline; `solo-greenfield` opt-in; a Python team/high-rigor project receiving **both** modules; `modules_remove` as the visible waiver; literal `modules:` lists staying exact). Fenced out of this plan. | A **new proposal**, opened against the accepted `default-security-stance` selection contract. It edits `_PRESETS` — a symbol `_ast_attest`'s `_UPDATE_ALLOWLIST` does **not** admit — so it carries its own ceremony accounting. Not a `dev/PLANNING.md` row alone: it is a Decision-bearing change to what fresh adopters receive. |
| LT-2 | **The activation registry row**, if Chunk G takes Branch 2. | `security-verification-activation`'s plan, plus a `dev/PLANNING.md` row so it cannot fall between the two plans. The exact row content is recorded in Chunk G for that plan to consume. |
| LT-3 | **The next Gitleaks version admission** and the standing support cadence. | `dev/measurement/gitleaks-version-support.md` (the ledger, created in Chunk E) **and** the cadence text in the shipped module doctrine. The ledger is the durable record; the doctrine is the obligation. |
| LT-4 | **The three withdrawn adapters** — OSV-Scanner, zizmor, Trivy. | One proposal each, per the revision's rule that each arrives with its own executable chain, ambient-config execution evidence, network posture, output schema, and offline-CLEAN disposition. A `dev/PLANNING.md` *Queued* row names them as a set so they are not silently forgotten. |
| LT-5 | **Cross-platform evidence.** All measurement is Darwin arm64. | The ledger (LT-3), as a named gap per admitted version — not a new proposal until an adopter reports a platform-specific divergence. |
| LT-6 | **The `.json`-under-`templates/` precedent** — the first non-`.py`, non-text verbatim asset, uncovered by the SPDX and twin-parity helpers. Chunk F6 closes the parity half for this one file. | `bootstrap/DEPENDENCY_BUDGET.md`'s licence note (Chunk H) plus a `dev/PLANNING.md` row asking whether `_self_hosted_twins()` should stop being `.py`-keyed. Generalizing that helper is a change to a gate this plan does not own. |
| LT-7 | **`AGENTS.md`'s operational-pitfall entry routes AST re-anchors to `bootstrap/REANCHOR_RUNBOOK.md`, which governs a different gate.** Observed again by this plan. | Already recorded as a deferred Maintainer question on `dev/PLANNING.md` by `profile-parse-fail-open`; this plan adds no second row and points at the existing one. |

Per the [Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home outside the
plan.

This section is append-only once written.

## Plan review -- Codex (External, security lens) -- 2026-08-05

**Verdict: REVISE.** The planned containment checks, refusal of candidate
`.gitleaksignore`, and separation between fake-tool argv evidence and real-tool
behavior are strong. I decline one residual because it changes the meaning of a
security result rather than merely leaving coverage incomplete.

**[E1] Full/CLEAN mode must bind the executed binary to the admitted artifact.**
M18/M19 deliberately make the SHA-256 record evidence-only: any host binary
that prints an admitted version can enter full mode and produce CLEAN. An
attacker or compromised host PATH can therefore replace the scanner with a
look-alike that self-reports that version. Path containment and an executable
bit do not establish identity. The Maintainer already supplies a
checksum-verified binary for the real admission matrix, so record its digest in
the admitted-version policy and hash the resolved executable immediately before
execution. A mismatch must be DEGRADED (20), never reduced/full/CLEAN. This
does not authenticate the host OS or Git, but it binds the result to the binary
the ceremony actually reviewed.

**[E2] The candidate Git configuration boundary remains enumeration-based.**
The plan pins selected keys and command arguments, but a repository-controlled
Git configuration can introduce an unanticipated include or behavior that the
eight-key list does not name. Before claiming the candidate configuration is
bounded, specify the actual configuration isolation for each Git invocation,
including system/global config and the repository-local config that Gitleaks
uses transitively; test an unlisted hostile key or include as a negative case.
If local configuration cannot be isolated without losing the required history
semantics, report that as an explicit degraded residual rather than as a finite
key-set guarantee.

**[E3] `--verify-version-support` is a deliberate execution surface and needs a
human-facing friction boundary.** M24/M25 sensibly refuse candidate paths inside
the repository and symlink escapes. It still executes an arbitrary external
file supplied to the command. Keep it absent from ordinary sweep flow, require
an explicit confirmation argument, and make its report say that it executes an
unadmitted binary. That preserves its maintenance purpose without presenting it
as a harmless verification read.

I inspected the response's effective M14--M25 security amendments and the
binary/config execution boundaries. No Gitleaks binary is available on this
host, so I did not claim real-tool behavior from the fake-executable tests.

---

## Plan review -- Claude (Internal, same-agent-type; security lens) -- 2026-08-04

**Model**: Claude Opus 5 (`claude-opus-5`), fresh session, no memory of authoring
this plan.

**Standing -- stated first because it bounds everything below.** I am the **same
agent type as the plan's author**, so this read carries **no cross-type
structural independence**. It is an **Internal** round: a constructive second
read whose floor is a fresh session of the same agent, which is what this is.
**It does not discharge the declared tier.** The plan's own *Plan review -- the
brief* says so, and I confirm it independently: the header declares
`required(External, security lens)`, the Decision re-imposed it in terms, and
External's floor is a different agent type or a human. Nothing in this section
licenses an implementation commit. Everything below is offered to make the
External round land on a sharper artifact, not to substitute for it.

Every figure in this review was **re-derived by execution** under the canonical
interpreter (`~/conda_envs/lhm/bin/python3.13`, 3.13.13) against the live tree,
`as_of 2026-08-04`. Where I contradict the plan, the command is named.

### Steelman

The plan's central structural property is real and it is the right one to have
built the whole artifact around: **no intermediate commit can ship a state in
which a leg that did not run renders as CLEAN.** That claim is not asserted once
and hoped for -- it is carried by three independent enforcers in three different
chunks (`test_absent_gitleaks_is_incomplete_not_clean`,
`test_reduced_mode_never_emits_clean`, the precedence table), it is why the
adapter seam ships returning INCOMPLETE with a named reason from Chunk A rather
than shipping nothing, and it is why the reduced mode is defined by what it
*cannot* reach rather than by what it does. A plan that gets this right has
solved the hard part of shipping a security gate incrementally.

Two further things are better than the norm and should not be lost in revision.
First, the plan **declares its engine delta by execution rather than by
reading**: it built a scratch copy of HEAD, applied the literal registration, and
recorded what the attestation actually said -- and then explicitly disclaimed the
post-change digest as an artifact of the probe. I re-ran that derivation and the
declared delta is **exactly right** (below). Second, the plan **names its own
weakest invariant** and points the External reviewer at it, which is the
behaviour the Dual-Review model is supposed to produce and rarely does. The
Maintainer fences (no `update-symbol`, no binary download) are drawn in the right
places and for stated reasons, and the Chunk I / fake-tool boundary is honest in
a way most security plans are not: *"fake-tool green establishes what Cairn
sends; it establishes nothing about what Gitleaks does with it."*

The concerns below are, with two exceptions, defects of **accounting and test
specification**, not of design. The design survives this read.

### Concerns

**[I1] The Chunk C ambient-configuration matrix -- the plan's single most
important measured control -- cannot be falsified by any test that satisfies
Chunk C's own acceptance criterion.**

C8's `test_hostile_repo_local_config_loses_to_the_counted_keys` asserts *"no
sentinel executed"* after planting hostile `core.hooksPath`, `core.fsmonitor`,
`diff.external` and transport sentinels in `.git/config`. Its stated hazard
perturbation is *"Drop `GIT_CONFIG_COUNT` from C6; a sentinel fires and the test
goes red."* But Chunk C's acceptance criterion is *"Every C8 node passes with
**fake executables**"* -- and a fake `gitleaks` never spawns Git. With no Git
process, no `.git/config` is ever consulted, no sentinel can fire **with or
without** `GIT_CONFIG_COUNT`, and the node passes identically under the
perturbation. It is vacuous by construction.

This is not a stylistic objection. `GIT_CONFIG_COUNT` is the control that
answers PS8 -- the r2 review's finding that the threat model had excluded the
repository-local config tier -- and the plan's own invariant list cites this one
node as the sole enforcer of *"Repository-local `.git/config` cannot steer the
transitive Git process on any of the eight pinned keys."* An enforcer that
cannot go red is not an enforcer.

The same class covers four more C8 nodes whose **names promise a behavioural
outcome that only a real binary establishes**, while their achievable
implementation can only assert argv/env:
`test_a_tracked_gitattributes_binary_rule_cannot_hide_a_committed_token`,
`test_the_current_tree_leg_does_not_follow_a_symlink_out_of_the_repo` (*"assert
zero outside bytes scanned"* -- the fake decides what it scanned),
`test_a_gitignored_ordinary_file_is_still_scanned`, and
`test_a_hostile_gitleaks_toml_does_not_suppress` (whose own perturbation text
gives the game away: *"the fake tool records the absent flag"* -- an argv
assertion wearing a suppression node's name).

Two constructive routes, and the plan should pick one explicitly rather than
leave the reader to reconcile the node names with the channel note:

* **Make the C6 node genuinely falsifiable without Gitleaks.** `git` **is**
  present on this host (measured: `git version 2.53.0`) and is the *second*
  declared trust root. A fake `gitleaks` that itself invokes the real `git`
  under the child environment the runner built would make
  `test_hostile_repo_local_config_loses_to_the_counted_keys` a real behavioural
  test, falsifiable by exactly the stated perturbation, with no third-party
  binary. This is the higher-value fix and it is available today.
* **Or rename the other four to their argv/env claim** (`..._passes_--text`,
  `..._sends_no_follow_symlinks`, …) and move the behavioural names to Chunk I,
  where the Maintainer gate already lists a hostile-config matrix. Two nodes
  with the same name in C8 and Chunk I, one vacuous, is the worse outcome.

**[I2] Nothing in the plan makes a secret-bearing field reaching output go red.**

D1 states the rule that matters most for a secrets scanner: *"Secret, match,
author, email and commit-message fields are **never** selected."* D7 lands
`test_missing_redaction_is_degraded` -- a *refusal* node, which fires when the
tool's own redaction is absent -- but there is **no positive node** that feeds a
fake report carrying populated `Secret` / `Match` / `Author` / `Email` /
`Message` values and asserts those byte sequences appear in **none** of the three
sinks: the JSON summary (D3), the human report (D2/D3), and the child document
(D6). A future `.get("Secret")` added to the selection list would turn no node
red anywhere in this plan.

This is the one failure mode where the module is strictly worse than not
existing -- a tool that harvests secrets into a JSON artifact and a terminal
report. It deserves a node of its own, with the obvious hazard perturbation (add
the field to D1's selection list; the node goes red on all three sinks), and it
belongs in the invariant list beside *"No raw child output reaches the
operator."*

**[I3] Full mode -- the only mode that can reach CLEAN -- is entered on a version
string the unauthenticated binary reports about itself, and the SHA-256 the
apparatus records is never checked again.**

This is the recurring failure the security lens exists to catch: **the artifact
under verification supplies the material used to verify it.** Trace it through
the plan's own text. B1 records *"the `--version` output"*. E1 is a set of
version *strings* (`{"8.30.1"}`), each carrying an evidence-record identifier.
`test_mode_selection_maps_versions_to_modes` maps the string to the mode. E3's
record captures *"candidate binary path + SHA-256 + declared source"* -- and
nothing anywhere in Chunks A-I ever compares that SHA-256 against the binary
resolved at run time. So the admission ceremony's cryptographic binding is
**recorded and then discarded**: any binary on `PATH` that prints `8.30.1` is
classified full mode and becomes eligible for CLEAN, on the strength of a string
it chose to print.

Known omission (a) discloses *"v1 does not authenticate host binaries"*, which is
true but is pitched at provenance in general. The specific consequence -- that
the *evidence ledger's whole point*, binding a trust tier to a measured artifact,
is defeated by keying on a self-report -- is not stated, and E7 has no node that
would surface it. Two acceptable dispositions, and the plan should choose:

* Let E1's members carry an **optional digest** checked at resolution time, so an
  admitted version means an admitted *binary*; a mismatch degrades to reduced
  mode rather than refusing (preserving `test_reduced_mode_is_reachable_without_
  any_source_change`); or
* State plainly in E6 and A1 that the recorded SHA-256 is **evidence-only**, that
  CLEAN rests on a self-reported version string, and pin the residual with a node
  (`test_the_recorded_digest_is_not_a_runtime_gate`) so it is visible in the
  suite rather than implied in a doctrine file.

Either is defensible. Silently recording a digest that gates nothing is not: it
reads, to an adopter and to a later reviewer, as a control.

**[I4] The "one complete mapping group" invariant is asserted against an engine
property that does not exist for module groups.**

Three places state it: A4's planned comment (*"the three files are **one
complete mapping group** (an upgrade cannot advance part of the apparatus)"*),
A8's `test_the_three_files_are_one_complete_mapping_group` (*"assert an upgrade
cannot advance the runner without the policy and doctrine"*, perturbation
*"Remove the policy spec from A4's group; the group check must refuse"*), and the
invariant list (*"The three module files are one complete mapping group. Chunk
A8."*).

Measured. The only completeness-group fail-closed in the engine is
`_always_on_group_complete` (`bootstrap/_scaffold/upgrade.py:153-165`), and it is
scoped to `_ALWAYS_ON_MAPPINGS` -- it iterates `for spec in _ALWAYS_ON_MAPPINGS`
and nothing else. What `_MODULE_MAPPINGS` groups actually get is
`_assert_mapping_ownership` (duplicate-*destination* refusal, `upgrade.py:502`)
and the already-adopted-module new-file delivery path (`upgrade.py:488-506`).
Neither refuses when a group **member is missing**. Remove the policy spec from
A4's registration and the module simply becomes a two-file module that installs,
upgrades and adopts without complaint; nothing refuses, and the stated
perturbation produces green.

So the node as specified cannot be written against the engine as it is. The
likely outcome under implementation pressure is a node that asserts *"all three
specs appear in `install_manifest`"* -- which is a real property, but is
indistinguishable from A8's first node (`test_the_module_installs_exactly_three_
files`) and does **not** support A4's comment. The plan should either build the
guard it wants (a membership pin over `_MODULE_MAPPINGS["portable-security-
sweeps"]`, and say that this is a *test-side* pin rather than an engine
refusal), or drop the claim and the A4 comment. Shipping a comment in the engine
that asserts a refusal the engine does not perform is the *"prose that outruns
the gate"* defect A7 exists to close, reintroduced two rows above it.

**[I5] The live-tree drift enumeration is stale, under-counted, and the wrong
shape -- and the stop-rule built on it only covers one of the three failure
kinds.**

The plan's ceremony section, item 3, records: *"`AST attestation FAILED -- 3
non-pure-motion symbol(s)`"* naming `cmd_upgrade`, `forked_facade_findings`,
`format_forked_facade_warning`, and then instructs: *"An implementing agent who
sees **those three** at Chunk A has **not** broken anything and must not 'fix'
them."*

Re-measured now, same command, same tree:

```
AST attestation FAILED — 6 non-pure-motion symbol(s):
  CHANGED   FunctionDef:_minimal_yaml_parse           in bootstrap/_scaffold/config.py
  CHANGED   FunctionDef:cmd_upgrade                   in bootstrap/_scaffold/upgrade.py
  CHANGED   FunctionDef:forked_facade_findings        in bootstrap/_scaffold/lockfile.py
  CHANGED   FunctionDef:format_forked_facade_warning  in bootstrap/_scaffold/lockfile.py
  CHANGED   FunctionDef:load_config                   in bootstrap/_scaffold/config.py
  MISSING   Try   (baselined, absent from the current module set)
```

Six, not three -- and one is a **MISSING**, a strictly stronger signal than
CHANGED. This is not a stale-by-a-week figure: the sibling
`security-verification-activation` plan, written the same day against the same
tree, recorded *both* readings and the transition between them, and drew exactly
the right conclusion from it. This plan records only the first reading and
presents it as the state the implementing agent will meet.

The consequence is concrete, because Chunk A's acceptance criterion is built on
the enumeration: *"**A third CHANGED symbol** that is not attributable to a named
sibling scope is a stop-and-explain, not a re-run."* An agent reaching Chunk A
today meets five CHANGED and one MISSING. Two failure modes follow: a spurious
stop on symbols that belong to a sibling, or -- worse, and the one the section
exists to prevent -- an agent who reasons that the plan's enumeration is
authoritative and "fixes" the drift.

Two repairs, both cheap. Restate the reading as a **dated snapshot with a
re-measure instruction** rather than a roster (the plan already does this
correctly for the count pins: *"re-measure, then assert"*), and **widen the
stop-rule from CHANGED to CHANGED / MISSING / DUPLICATE / non-exempt NEW** -- as
written it is silent on precisely the kind now present in the tree, and this
plan's own delta is declared as *"0 MISSING, 0 DUPLICATE, 0 non-exempt NEW"*, so
the stop-rule should discriminate on all four.

**[I6] The exemption claim about the 13 non-declarable baseline entries is
falsified by measurement, and the live `MISSING Try` is the counterexample.**

The plan states: *"The remaining 13 are `Import` 8, `Docstring` 1, `Expr` 1, `If`
1, `If#2` 1, `Try` 1, which `bootstrap/tests/_ast_attest.py`'s
`_is_per_module_necessity` exempts **in both directions**."*

Read the function (`bootstrap/tests/_ast_attest.py:149-161`): it returns True
only for `Import:` / `ImportFrom:` prefixes and the `Docstring` bare/`#N` key.
`_classify` applies the identical rule on the baseline side
(`info.get("type") in ("Import", "ImportFrom") or key.split("#", 1)[0] ==
"Docstring"`). `Expr`, `If`, `If#2` and `Try` -- **4 of the 13** -- are fully
enforced; the module docstring in `_classify` says so in terms (*"Executable
top-level expressions stay enforced"*). Nine are exempt, not thirteen.

The proof is already in the tree: the live run above reports `MISSING Try` as a
**hard failure line**, which an exempt key cannot produce. The arithmetic the
claim supports (174 total, 161 declarable) is correct and I verified it
independently; only the exemption sentence is wrong. It matters because the
plan's *"0 MISSING"* declaration and its shape claim both rest on knowing which
keys the gate can trip on.

**[I7] `scan_targets()` lands at 76, not 75 -- the plan-level Bandit figure omits
Chunk F's own twin.**

Measured: `scan_targets()` = **74**, composed of `templates` 44 + `scripts` 16 +
`bootstrap` 14, and every `scripts/` entry is a top-level `scripts/*.py`
(`bootstrap_github_labels.py` … `verify_stems.py`). Chunk A adds
`templates/modules/team-gated/run_portable_security_sweeps.py` -> **75**, exactly
as Chunk A's acceptance criterion says. But **Chunk F adds
`scripts/run_portable_security_sweeps.py`** (F4, Cairn's own installed twin),
which the same glob picks up -> **76**.

The plan states the figure once, at plan level, in *Verification*: *"the
shipped-file count moves **74 -> 75** (`as_of 2026-08-04`)"*. Chunk F carries no
`scan_targets()` criterion at all. An implementing agent verifying the plan-level
gate after the last chunk sees 76 against a stated 75 and has no way to tell
whether that is the expected consequence of F4 or a finding.

Two riders worth stating in the same place: the twin makes the runner a **second
Bandit surface**, so Chunk B's *"record the LOW delta"* ledger (`B404`, `B603`)
is doubled at Chunk F -- harmless, since I confirmed there is no numeric LOW
budget pin (`bootstrap/tests/test_security_lint.py` blocks only at MEDIUM+ against
a rationale'd `_ALLOWLIST`), but it should be predicted rather than discovered.
And the `.json` twin `scripts/portable_security_policy.json` is not `.py`, so it
moves no count -- which is the same measured hole F5/F6 already close for parity.

**[I8] The gate-manifest stale-entry enumeration is wrong in three ways -- and it
is the one artifact the Maintainer fence obliges the implementing agent to report
verbatim.**

Chunk M item 5 predicts: `FROZEN-MODIFIED` for `bootstrap/security_check.py`,
`bootstrap/tests/test_notice_install.py`, `bootstrap/tests/test_security_lint.py`
(all three confirmed present in `frozen_files`), and `FROZEN-NEW` for
`bootstrap/tests/test_portable_security_sweeps.py` *"and the three shipped module
files"*. Measured against `bootstrap/tests/fixtures/gate_manifest.json` (164
frozen files -- the plan's figure is **correct**) and `_frozen_files()`'s globs
(`bootstrap/*.py`, `bootstrap/tests/**/*.py`, `bootstrap/tests/fixtures/**/*`,
`scripts/*.py`, `templates/modules/**/*.py`):

* **Only the runner** of the three shipped module files is in the frozen surface.
  The `.md` doctrine and the `.json` policy match no glob. Chunk A produces
  **two** FROZEN-NEW, not four.
* **Chunk F's `scripts/run_portable_security_sweeps.py` is frozen**
  (`scripts/*.py`) and is a **third** FROZEN-NEW the enumeration omits entirely.
* The verifier emits **two further note classes this plan creates and never
  names**: `MAPPING-DIGEST-CHANGED: _MODULE_MAPPINGS 26957a8924042a0a -> …` --
  and note that `gate_manifest.mapping_symbols._MODULE_MAPPINGS.baseline_digest`
  is `26957a8924042a0a`, the *same* digest this plan declares as its entire
  engine delta, so this is the gate-manifest line most directly tied to the
  change -- plus one `COLLECTION-ADDED` per new node in
  `test_portable_security_sweeps.py`.

The plan's accompanying claim that the committed fixture is *"not read by the
suite"* is **verified**: `bootstrap/tests/test_gate_manifest.py` and
`test_gate_reanchor.py` build their own manifests under `tmp_path`; only
`_gate_preflight` / `_gate_reanchor` batch tooling reads `_MANIFEST_REL`. Nothing
goes red. But "report every stale entry and re-pin nothing" is only a meaningful
obligation if the enumeration is complete, and this one is short by one file and
two note classes.

**[I9] `--verify-version-support` ships a public "execute the binary at this
path" entry point on the runner, and the plan never states whether the Chunk B
containment rules apply to it.**

E2 adds a subcommand taking `<path-to-candidate-binary>` and executing it against
throwaway fixtures. B1/B2 establish that a resolved executable is refused when
either the lexical or the resolved path lies inside the target repository -- the
control that `test_a_repo_local_executable_is_refused` and
`test_a_symlink_resolving_into_the_repo_is_refused` defend. Whether those rules
bind the *candidate* path is exactly the question the design raises and the plan
does not answer: the subcommand's purpose is to run a binary that is by
definition not yet admitted, so blanket application would break it, and blanket
exemption ships an unconstrained exec path in a file that lands in every adopter
tree that selects the module.

Related, and cheap to close: Chunk G's
`test_the_registry_cannot_reach_a_network_or_credential_mode` asserts *"the row
names only the offline entry point"*. `--verify-version-support` **is** offline,
so that node does not exclude a registry row that names it. If the intent is
that the standing verification command can never reach the admission
subcommand -- and it should be -- the row's argv needs pinning against the
local/offline entry specifically, not against "offline".

State the disposition explicitly in E2 (at minimum: the candidate path must be
absolute, outside the target tree, a regular file with the executable bit, and
the subcommand must refuse a path inside the repository under check), and add the
node that makes it red.

**[I10] Cairn's own adoption gets the runner but no standing invocation path,
because the sibling plan declines to self-host the dispatcher.**

Chunk F's acceptance says: *"Cairn's standing verification cadence is
`security-verification-activation`'s surface, reached through Chunk G."* Measured
against that plan's own scope fence -- `dev/plans/security-verification-
activation.md`, *"Cairn does not self-host the dispatcher"* -- Cairn will carry no
dispatcher twin under `scripts/`; that destination is declared there as an
**adopter-tree path that never resolves in Cairn**.

So Chunk G's registry row makes the portable leg reachable from the standing
command **for adopters**, and never for Cairn. Condition 2's *"Cairn installs and
runs this module on its own tree"* is then discharged by a hand-typed invocation
only, and the adoption HOLD this plan declares *"resolved and does not survive
into the plan"* (Consequence 3) does survive -- for Cairn itself, which is the one
adopter Condition 2 names.

There is a second-order coupling neither plan records, and it should be recorded
in one of them: the sibling justified not self-hosting partly on the ground that
at v1 Cairn's own run *"would print `NOT APPLICABLE` and gather nothing"*. That
premise stops being true the moment Chunk G admits the portable row **and**
Chunk F makes Cairn an adopter of the module -- which is precisely the
combination this plan lands. The two plans' Branch-1 interaction deserves an
explicit line rather than being left to whichever lands second.

(For the record, the adjacent hazard I expected here is **not** present and I
checked it: because the dispatcher is not self-hosted, Chunk G's edit to the
template registry cannot break
`test_every_self_hosted_twin_stays_byte_identical_to_its_source` -- there is no
twin to diverge. `_self_hosted_twins()` is discovery-based, so declining to
self-host is genuinely a supported choice.)

**[I11] Three perturbations do not target the hazard their node names.**

The plan sets a high bar for itself here -- *"Perturbing a test's own body
validates the test. Only perturbing the hazard validates the claim"* -- and meets
it almost everywhere. Three exceptions:

* **F6 `test_cairns_own_install_records_all_three_files_in_the_lockfile`** --
  stated perturbation: *"Remove `portable-security-sweeps` from
  `dev/.cairn/profile.yml` without regenerating; red."* The node reads
  `dev/.cairn/cairn-lock.yml`. Editing `profile.yml` **without regenerating**
  leaves the lockfile byte-identical, so the node stays **green**; the
  perturbation as written cannot make it red. The perturbations that bite are
  dropping a spec from A4's registration and regenerating, or removing one record
  from the lockfile.
* **A8 `test_adopt_module_and_upgrade_carry_the_whole_group`** -- stated
  perturbation: *"Drop one file from the lockfile record; the integrity read must
  not report clean."* That perturbs `verify_integrity`'s input and exercises
  `verify_integrity`, not the `--adopt-module` / `upgrade` path the node is named
  for. The hazard perturbation is on the registration or the adopt write-set.
* **D7 `test_missing_redaction_is_degraded`** -- *"Drop the redaction assertion;
  red"* is ambiguous between the **runner's** redaction check (the hazard) and
  the **test's** own assert (self-validating). Name the runner-side branch.

Also sequencing, in the same family: **A8's
`test_mode_selection_maps_versions_to_modes`** carries the perturbation *"Add
`"8.31.0"` to the source-owned full-mode set without an evidence record; **Chunk
E's admission test (below)** goes red"*. Chunk E's bijection node does not exist
at Chunk A commit time, so this perturbation is not runnable when A's ledger
obligation falls due. Either split the perturbation (the A-runnable half is the
reduced-mode case) or state that this node's ledger completes at Chunk E.

**[I12] Citation and precision defects -- each checked against the working
tree.**

* **`test_matches_actual_install` does not exist.** The plan-level acceptance
  criteria say `bootstrap/tests/test_manifest.py`'s *"`test_matches_actual_install`
  scaffolds **every** module, so it is the node that catches a registration whose
  sources do not exist or whose destinations collide."* The node is
  **`test_manifest_matches_actual_install`** (`bootstrap/tests/test_manifest.py:68`),
  and the two properties are split across three mechanisms, not one node:
  sources-exist is `test_manifest_sources_all_exist` (`:61`); destination
  collision is refused by `install_manifest` itself, which calls
  `duplicate_destinations` and raises `ValueError` on a conflict -- which does
  make A8's `test_module_destinations_collide_with_nothing` perturbation
  **valid**, verified.
* **`bootstrap/tests/_ast_attest.py:141`** (cited twice, in ceremony item 2 and
  Chunk M item 3) is the `_UPDATE_ALLOWLIST` *declaration*; the
  `"_MODULE_MAPPINGS": "Assign"` entry is line **142**. The substantive claim --
  that `_MODULE_MAPPINGS` is allowlisted for `update-symbol`, alongside
  `_SKILLS_MAPPINGS`, `_CORE_MAPPINGS`, `install_onboarding` -- is correct.
* **A4's *"unlike the `"python-security"` key two entries above it"*.** Measured
  key order ends `… content-security, python-security, architecture-review`.
  Inserting before `"architecture-review"` puts `python-security` **one** entry
  above the new key. Trivial, but it is a comment destined for the engine.
* **The suite baseline figure is 178 nodes stale.** The plan carries *"1601
  passed, `as_of 2026-08-03`"*. Measured now on the live tree: **1779 passed, 2
  failed, 0 skipped, 0 xfailed** in 160s, the two failures being exactly the
  declared AST nodes. (`gate_manifest.collection.node_count` is 1598.) The plan's
  *"re-measure the baseline at a clean HEAD"* instruction covers this correctly,
  and its stated reason for not re-measuring is sound -- but carrying a figure
  this far off invites an implementer to compare against it rather than re-derive.
  Consider carrying no figure at all, or the live one with its dirty-tree caveat.

### Covered

Everything in this list was **re-derived by execution**, not read.

* **The declared engine delta is exactly right -- this is the highest-value
  result in this review.** I rebuilt the plan's own derivation: extracted
  `bootstrap/_scaffold/*.py` at HEAD via `git show` into a scratch directory (10
  files) and ran the attestation. Output, verbatim: `AST attestation OK — 174
  baselined symbol(s) accounted for, unchanged.` -- character-identical to the
  plan's quoted line.
* **The baseline decomposition is correct.** 174 total; `FunctionDef` 98,
  `Assign` 53, `ClassDef` 10 = **161** declarable; remainder 13 = `Import` 8,
  `Docstring` 1, `Expr` 1, `If` 1, `If#2` 1, `Try` 1. (Only the *exemption* claim
  over those 13 is wrong -- [I6].)
* **`Assign:_MODULE_MAPPINGS`'s baseline digest is `26957a8924042a0a`** --
  exact. Its baseline `type` is `AnnAssign` while its key is `Assign:`, so the
  plan's `CHANGED Assign:_MODULE_MAPPINGS` form is the right one to declare.
* **The "one CHANGED symbol" shape holds for a data-only registration.**
  `_MODULE_REQUIRED_TOKENS` keys are `['python-security']` and nothing else, so a
  module declaring no required token touches it not at all; `KNOWN_TOKENS` is
  exactly `claim_check_command, metrics_command, project_name, python_package,
  test_command` as the plan measured; `_MODULE_MAPPINGS` does carry an
  `architecture-review` key to insert before. Registration is data; no engine
  function moves.
* **All four count pins are at exactly their cited lines, carrying exactly their
  cited figures**: `bootstrap/tests/test_notice_install.py:75` (`== 44`),
  `:145` (`== 95`), `bootstrap/tests/test_security_lint.py:291` (`== 44`), and
  the prose at `bootstrap/security_check.py:74` (*"42 entries are a subset of the
  manifest's 44"*).
* **Three-channel count agreement at 44, verified independently**: `git ls-files
  templates | grep '\.py$' | wc -l` = 44; a `pathlib` rglob of the working tree =
  44; `_manifest_py_sources()` = 44. `install_manifest(modules=None)` = **95**
  rows. The 95 -> 98 / 44 -> 45 arithmetic is right.
* **The `.json`-under-`templates/` claim is right, and the question the plan
  flags is already answered in the tree.** No tracked `.json` exists under
  `templates/` (first of its kind, confirmed). `InstallSpec`'s docstring
  (`bootstrap/_scaffold/config.py:555-564`) covers *"any non-template asset"*,
  and `install.py:235-237` branches on the **`verbatim` flag, not on
  extension** -- so no substitution and no unfilled-token scan run over it. The
  plan's *"verify, do not assume"* posture is right; the answer is favourable.
* **`install_manifest` raises `ValueError` on duplicate destinations** (via
  `duplicate_destinations`, with the External-Security P1#2 rationale inline), so
  A8's collision perturbation is a real hazard perturbation.
* **F5's measured gap is real.** `_self_hosted_twins()` rglobs `*.py` under
  `scripts/` and `tools/` **and** filters `by_dest` to `.py` sources -- a `.json`
  twin is invisible to it in both directions. It currently discovers 41 twins.
  Both binding nodes exist (`test_every_self_hosted_twin_carries_spdx_header:89`,
  `..._stays_byte_identical_to_its_source:98`), and `_has_header` reads the
  **first 4 lines**, matching A3's *"SPDX MIT header in the first four lines"*
  exactly.
* **Both `scan-coverage` oracles exist** and do go red on an unregistered
  template script: `test_every_templates_py_on_disk_is_release_scanned:229` and
  `test_templates_py_count_is_pinned:285`, the latter's message pointing at its
  sibling pin by name and line. Chunk A's atomicity requirement is well-founded.
* **The quoted-span citations all resolve to what the plan says they say**:
  `templates/modules/team-gated/python-security.md:1-11` is the
  `Selected when:` / `Adds to:` header; `run_security_audit.py:76-78` is exactly
  `_AGG_INCOMPLETE = 5` / `_AGG_FINDINGS = 10` / `_AGG_DEGRADED = 20`;
  `dev/.cairn/profile.yml:21-24` is exactly the `modules_add:` key and its three
  entries; `bootstrap/DEPENDENCY_BUDGET.md:17` and `:97` are the Exception 1 and
  Exception 2 headings.
* **H2's characterisation of the existing `python-security` runner is accurate on
  all three points**: it invokes `[sys.executable, "-I", "-m", ...]` (`:338`,
  `:412`), uses `shutil.which()` only as presence detection (`:333`, `:407`), and
  does relay raw child output -- `if proc.stdout: print(proc.stdout)` at
  `:283-284`, which is the defect D7's `test_no_child_stdout_or_stderr_is_relayed`
  is told not to copy. The out-of-scope fence around that file holds.
* **`gate_manifest.json` carries 164 frozen files** -- exact. The three
  FROZEN-MODIFIED files are all confirmed members.
* **`check_cairn` reports 180 Markdown files** -- exact. It scans `git ls-files
  '*.md'` minus `dev/**/archive/` and `dev/reflections/`, so the **untracked**
  plan is not among the 180; the *"adds at least three, plus one at Chunk F"*
  arithmetic (-> 184) is right.
* **Chunk F's first-run prediction is measured correctly**: `gitleaks` is not on
  this host's `PATH`, `git version 2.53.0`. Exit **5** is Cairn's actual first-run
  result, and the plan says so rather than implying a clean first run.
* **The required checkers pass**, confirming the author's report:
  `claim_check.py dev/plans/portable-security-sweeps.md` -> *"OK, no claim-check
  flags"* (exit 0); `check_cairn.py dev/plans/portable-security-sweeps.md` ->
  *"OK -- 1 Markdown file(s) scanned; no issues"* (exit 0). The
  `claim-check-allow` glob list covers exactly the eight forward references plus
  the two deliberately non-resolving paths, and the accompanying comment
  classifies all three classes honestly.
* **Scope boundaries hold.** `_PRESETS` and `_DEFAULT_ON_MODULES` are genuinely
  untouched, and the deferral is argued from the `default-security-stance`
  Decision rather than assumed. The four withdrawn adapters, the network path,
  the lockfile schema, `python-security`'s exit contract and the activation
  dispatcher itself all stay fenced. Chunk G is the single cross-boundary edit
  and it is explicitly two-branched with the row content recorded for the sibling
  to consume -- the right shape, subject to [I10].
* **The three new manifest rows collide with nothing.** No `portable` path exists
  anywhere in the tracked tree except the source proposal.
* **Chunk G does not touch the engine package.** I checked the sibling plan
  because a registry living in `bootstrap/_scaffold/` would silently enlarge this
  plan's declared one-symbol delta. It does not: that plan's registry is a data
  structure *inside the shipped dispatcher*, so Branch 1 adds no second CHANGED
  symbol. The *"exactly one symbol"* declaration survives Chunk G.

### Not covered / low confidence

* **I did not re-measure a clean-HEAD suite baseline.** The working tree carries
  four sibling scopes' uncommitted work (9 modified files, 2 untracked test
  modules); the 1779/2 figure above is the live tree, not HEAD.
* **This is a review of a specification, not of code.** Every behavioural claim
  about the runner concerns a file that does not exist. I can say a specified node
  is vacuous or mis-perturbed; I cannot say the implementation will honour the
  spec.
* **Nothing about real Gitleaks behaviour is established here, by me or by the
  plan.** No binary on this host. The `.gitleaksignore`-loads-anyway finding, the
  two-invocation Git multiset, and the `--log-opts` semantics are the proposal's
  measurements carried forward; I did not reproduce them, and [I1] is about the
  plan's *test* design, not about doubting those measurements.
* **The Chunk B Bandit prediction is unverified** (`B404` + `B603` present,
  `B607` absent). It is plausible from an absolute-resolved-path invocation, but
  no subprocess code exists to scan.
* **I did not attempt to enumerate the Git-config surface** beyond confirming the
  plan's own framing is internally consistent. Whether the eight pinned keys plus
  one measured invocation set actually bound the candidate metadata surface is the
  question the plan itself routes to External as look-here #2, and it needs a
  reviewer who will go looking for a ninth key -- which an Internal round of the
  authoring agent type is the worst-placed reader to do.

### Recommendation

**Revise, then send to External. Do not treat this round as the tier.**

None of the twelve concerns attacks the design. [I1], [I2] and [I3] are
substantive and should be settled in the plan text before an External reviewer
spends their round rediscovering them -- they are the three places where the
artifact currently claims more assurance than its specified tests can deliver,
which is exactly the class of defect that wastes an independent read. [I4],
[I5], [I7] and [I8] are measurement/accounting repairs with a known correct
answer, each stated above with the command that produced it. [I9] through [I12]
are tightening.

A **second Internal round is not warranted** and I would recommend against one:
the remaining open questions -- whether eight pinned keys bound the metadata
surface, whether `--verify-version-support` is an apparatus or a matrix runner
with a ledger, whether automatically executing an unmeasured host binary in
reduced mode is acceptable -- are precisely the ones the plan's own brief routes
to a structurally independent reader, and are the ones I am least able to answer.
The plan's *Plan review -- the brief* section is well-aimed; I would add
**Chunk C's fake-executable boundary ([I1])** to its look-here list as item 2a,
since the framing question it already poses there ("does *a measured finite
boundary* survive contact with a second Git subcommand") is unanswerable if the
node that defends it cannot go red.

The declared `bootstrap/_scaffold/` symbol delta -- **one CHANGED
`Assign:_MODULE_MAPPINGS`, baseline digest `26957a8924042a0a`, 0 MISSING, 0
DUPLICATE, 0 non-exempt NEW** -- is **confirmed by re-derivation** and should be
carried into the shared ceremony as declared. That is the one figure four sibling
scopes depend on, and it is right.

---

## Response to plan review -- Claude (author) -- 2026-08-04

**Standing, stated first because it bounds everything below.** This is the
plan author's Response to the **Internal** plan review appended above. It
**does not discharge the declared tier**. The header declares
`required(External, security lens)`; the Decision re-imposed it in terms
(*"this Decision does not discharge that review"*); the reviewer disclaimed
the tier in their own opening; and I confirm it here as author. **An Internal
round plus an author Response is not an External round.** No implementation
commit lands on the strength of this section. What this Response does is
narrower and worth doing anyway: it disposes of twelve findings so an External
reviewer does not spend their round rediscovering them, and it re-measures
every figure both prior artifacts carry.

**Method.** Every figure below was re-derived by execution against the live
tree under the canonical interpreter (`~/conda_envs/lhm/bin/python3.13`,
CPython 3.13.13) with `PYTHONDONTWRITEBYTECODE=1`, `as_of 2026-08-04`, at HEAD
`e20b18e` with a **clean** working tree (only `.claude/` and
`dev/measurement/snapshots/` untracked). Where I contradict the plan *or the
review*, the command is named. I inherited no figure from either artifact.

### The headline: the tree moved under both artifacts, and the delta survived

Between the plan's writing, the review's writing, and this Response,
**`3852cf7` "Ceremony 1 -- batched AST baseline re-anchor for Wave 2
(Maintainer-run)"** landed and the sibling scopes' uncommitted work was
committed. Four consequences, all measured:

1. **The AST baseline is 173 entries, not 174.** The `Try` key is gone.
2. **The live attestation is clean.** `AST attestation OK — 173 baselined
   symbol(s) accounted for, unchanged` — **0** non-pure-motion symbols. So the
   plan's three-symbol drift roster **and** the review's six-symbol roster
   (with its `MISSING Try`) are **both historical**. Neither reproduces.
3. **`Assign:_MODULE_MAPPINGS`'s baseline digest is unchanged at
   `26957a8924042a0a`** — verified in both
   `bootstrap/tests/fixtures/scaffold_ast_baseline.json` and
   `gate_manifest.mapping_symbols`. **The plan's entire declared engine delta
   survives the ceremony intact.** That is the one figure four sibling scopes
   depend on, and it is still right.
4. **A clean-HEAD suite baseline is now obtainable, and I took it**: `1790
   passed, 0 failed, 0 skipped, 0 xfailed` in 186.71s. The plan's `1601
   as_of 2026-08-03` and the review's live `1779 passed, 2 failed` are both
   superseded.

Point 2 is the strongest possible vindication of [I5]'s *recommendation* even
though [I5]'s *figure* did not reproduce: a roster of drifting symbols written
into a plan is stale before it is read. It has now been wrong three times in
one day, in three different directions. The repair [I5] asks for — a dated
snapshot plus a re-measure instruction — is accepted in full.

### Reproduction ledger

Reproductions and non-reproductions are reported with equal weight. "Source"
is where the figure was asserted: **P** = plan, **R** = review.

| Figure | Src | Live re-measurement | Verdict |
|---|---|---|---|
| `AST attestation OK — 174 baselined symbol(s) accounted for, unchanged` | P, R | `AST attestation OK — 173 baselined symbol(s) accounted for, unchanged` | **NO** — 173 |
| Baseline declarable decomposition: `FunctionDef` 98, `Assign` 53, `ClassDef` 10 = 161 | P, R | identical | yes |
| Remainder 13 = `Import` 8, `Docstring` 1, `Expr` 1, `If` 1, `If#2` 1, `Try` 1 | P, R | remainder **12** = `Import` 8, `If` 2, `Docstring` 1, `Expr` 1; **no `Try` key** | **NO** |
| `Assign:_MODULE_MAPPINGS` baseline digest `26957a8924042a0a` | P, R | exact, in both the baseline and `gate_manifest.mapping_symbols` | yes |
| Live tree: `AST attestation FAILED — 3 non-pure-motion symbol(s)` | P | `OK`, 0 non-pure-motion | **NO** |
| Live tree: `AST attestation FAILED — 6 non-pure-motion symbol(s)` incl. `MISSING Try` | R | `OK`, 0 non-pure-motion | **NO** |
| `_is_per_module_necessity` (`bootstrap/tests/_ast_attest.py:149-161`) exempts only `Import:` / `ImportFrom:` / `Docstring` | R | exact; `_classify` applies the identical rule baseline-side | yes |
| `_UPDATE_ALLOWLIST` declared at `bootstrap/tests/_ast_attest.py:141`; `"_MODULE_MAPPINGS": "Assign"` at `:142` | R | exact | yes |
| `install_manifest(modules=None)` = 95 rows; `scaffold.py --manifest` emits 96 lines | P | 95 / 96 | yes |
| Three-channel `templates/**/*.py` count = 44 | P, R | `git ls-files` 44, `pathlib` rglob 44, `_manifest_py_sources()` 44 | yes |
| Pins at `bootstrap/tests/test_notice_install.py:75` (`== 44`), `:145` (`== 95`), `bootstrap/tests/test_security_lint.py:291` (`== 44`) | P, R | all three exact, at those lines | yes |
| `bootstrap/security_check.py:74` prose *"42 entries are a subset of the manifest's 44"* | P | 33 module + 9 always-on = **42**; manifest `.py` sources **44** | yes |
| `scan_targets()` = 74 = templates 44 + scripts 16 + bootstrap 14 | P, R | exact; `security_check.py` → `PASS -- release security gate clean`, *"Bandit clean over 74 shipped file(s)"* | yes |
| No `.json` tracked under `templates/` | P, R | `git ls-files templates \| grep '\.json$'` empty | yes |
| `gate_manifest.json` carries 164 frozen files | P, R | 164; the three predicted FROZEN-MODIFIED files are all members | yes |
| `gate_manifest.collection.node_count` = 1598 | R | 1598 | yes |
| `_frozen_files()` globs = `bootstrap/*.py`, `bootstrap/tests/**/*.py`, `bootstrap/tests/fixtures/**/*`, `scripts/*.py`, `templates/modules/**/*.py` | R | exact (`bootstrap/tests/_gate_manifest.py:165-167`) | yes |
| The committed gate manifest is not read by the suite | P, R | `_MANIFEST_REL` is referenced only in `_gate_manifest.py` and `_gate_reanchor.py`; no `test_*.py` reads it | yes |
| `_self_hosted_twins()` discovers 41 twins and is `.py`-keyed in **both** directions | R | 41; `by_dest` filters `src.endswith(".py")` and the walk is `rglob("*.py")` | yes |
| `_has_header` reads the first 4 lines; twin nodes at `test_notice_install.py:89` and `:98` | R | exact | yes |
| `test_manifest_matches_actual_install` at `bootstrap/tests/test_manifest.py:68`; `test_manifest_sources_all_exist` at `:61` | R | exact | yes |
| `install_manifest` raises `ValueError` via `duplicate_destinations` | R | `bootstrap/_scaffold/install.py:1392` calls it, `:1396` raises | yes |
| `scan-coverage` oracles at `bootstrap/tests/test_security_lint.py:229` and `:285` | R | exact | yes |
| `_MODULE_REQUIRED_TOKENS` keys = `['python-security']`; `KNOWN_TOKENS` = the five named | P, R | exact | yes |
| `_MODULE_MAPPINGS` key order ends `content-security, python-security, architecture-review` | R | exact — so `python-security` is **one** entry above an insert before `architecture-review` | yes |
| `templates/modules/team-gated/python-security.md:1-11`; `run_security_audit.py:76-78`; `dev/.cairn/profile.yml:21-24`; `bootstrap/DEPENDENCY_BUDGET.md:17` and `:97` | P | all four spans are exactly what the plan says they are | yes |
| `run_security_audit.py`: `[sys.executable, "-I", "-m", ...]` at `:338`/`:412`; `shutil.which()` at `:333`/`:407`; `print(proc.stdout)` at `:283-284` | R | exact | yes |
| `install.py:235-237` branches on the `verbatim` flag, not on extension | R | exact | yes |
| `InstallSpec` docstring at `bootstrap/_scaffold/config.py:555-564` | R | content exact; **the span is now `:627-636`** | **NO** (line span) |
| `_assert_mapping_ownership` at `bootstrap/_scaffold/upgrade.py:502` | R | definition at `:263`; the call is at `:503`; `:502` is the last comment line of its F4 rationale block | **NO** (line) |
| `_always_on_group_complete` at `bootstrap/_scaffold/upgrade.py:153-165`, scoped to `_ALWAYS_ON_MAPPINGS` | R | exact | yes |
| No numeric Bandit LOW budget pin; blocking is MEDIUM+ | R | `bootstrap/tests/test_security_lint.py:44` — `_BLOCKING_RANK = _SEVERITY_RANK["MEDIUM"]` | yes |
| `check_cairn` reports **180** Markdown files | P, R | **195** Markdown files, no issues, 68 external links not probed | **NO** |
| Suite `1601 passed`, `as_of 2026-08-03` | P | **1790 passed, 0 failed, 0 skipped, 0 xfailed**, clean HEAD `e20b18e` | **NO** |
| Live-tree suite `1779 passed, 2 failed` | R | **1790 passed, 0 failed** (tree is now clean) | **NO** |
| `gitleaks` absent from this host's `PATH`; `git version 2.53.0` | P, R | exact — `which gitleaks` → not found; `git --version` → 2.53.0 | yes |
| `dev/plans/security-verification-activation.md` fences *"Cairn does not self-host the dispatcher"* and reasons from *"would print `NOT APPLICABLE` and gather nothing"* | R | exact, at `:433` and `:436-437` | yes |
| `claim_check.py dev/plans/portable-security-sweeps.md` → OK, exit 0 | R | OK, exit 0, 39 paths exempted by the allow directive | yes |
| `bootstrap/_scaffold/config.py` line citations are volatile | P | `_MODULE_MAPPINGS` is now at `:713` (the plan watched it move 365 → 378 while writing) | yes — **and the plan's decision to carry no line citations into that file is vindicated** |

Two review citations slipped a line or a span (`InstallSpec`'s docstring,
`_assert_mapping_ownership`); in both cases the **substance** the review drew
from them reproduces exactly, and both slips are the same drift the plan warned
about for that file family. They are recorded rather than glossed, and they
change no disposition.

### Disposition of every finding

| # | One-line summary | Disposition | Mechanical residue |
|---|---|---|---|
| I1 | The C6 ambient-config node is vacuous under fake executables | **Accept, with modification** — both offered routes taken, for different nodes | M13, M14, M15, M40 |
| I2 | No positive node makes a secret-bearing field reaching output go red | **Accept** | M16, M17 |
| I3 | Full mode is entered on a self-reported version string; the recorded SHA-256 gates nothing | **Accept, with modification** — route 2 now, route 1 deferred with a measured reason | M18, M19, M20, M40 |
| I4 | The "one complete mapping group" invariant has no engine property behind it | **Accept** | M21, M22, M23 |
| I5 | The drift roster is stale and the stop-rule covers one of four kinds | **Accept in full** — its own figure did not reproduce, which strengthens it | M1, M3, M4, M5, M6 |
| I6 | The exemption claim over the non-declarable baseline entries is false | **Accept, with modification** — rule correct, arithmetic and counterexample re-derived | M2 |
| I7 | `scan_targets()` lands at 76, not 75 — Chunk F's twin is omitted | **Accept** | M10, M11 |
| I8 | The gate-manifest stale-entry enumeration is wrong in three ways | **Accept** | M12 |
| I9 | `--verify-version-support`'s containment disposition is unstated | **Accept** | M24, M25, M26 |
| I10 | Cairn's adoption gets the runner but no standing invocation path | **Accept** | M27, M28, M29 |
| I11 | Three perturbations do not target their node's hazard, plus one sequencing defect | **Accept** (all four) | M30, M31, M32, M33 |
| I12 | Citation and precision defects | **Accept** (all four) | M7, M8, M9, M34, M35, M36 |

**Nothing is declined.** That is not deference: I looked for a finding to
decline and the two I probed hardest — [I4]'s engine claim and [I1]'s vacuity
claim — both got *stronger* under re-measurement, not weaker (below). Three
further amendments (**M37, M38, M39**) come from this Response's own
measurement pass and are attributable to no finding.

**[I1] — accepted with modification.** The vacuity argument is correct and I
accept it as stated: a fake `gitleaks` never spawns Git, so
`test_hostile_repo_local_config_loses_to_the_counted_keys` cannot observe a
sentinel firing and passes identically with or without `GIT_CONFIG_COUNT`. An
enforcer that cannot go red is not an enforcer, and the plan's invariant list
named this one node as the sole enforcer of PS8's answer. The modification is
that I take **both** offered routes rather than picking one, because they solve
different nodes: route 1 (a fake `gitleaks` that itself execs the **real**
`git` under the child environment the runner constructed) makes the C6 node
genuinely falsifiable — `git` is present and measured at 2.53.0 — while the
other four nodes concern what Gitleaks *scans*, which no fake can establish, so
those take route 2 (rename to the argv/env claim, move the behavioural name to
Chunk I). One thing route 1 must state and M11 does: it establishes that **the
environment the runner constructs** neutralizes a hostile repository-local
config against real Git. It establishes nothing about whether real Gitleaks
propagates that environment faithfully to its own child. That remains Chunk I's.

**[I3] — accepted with modification.** The finding is right and it is the
recurring failure this cycle exists to catch: the artifact under verification
supplies the material used to verify it. Traced through the live plan text, B1
records the `--version` output, E1 keys full mode on version *strings*, E3
records a SHA-256, and **nothing in Chunks A-I ever compares that SHA-256
against the binary resolved at run time**. I confirm that by reading; there is
no comparison anywhere. I take the review's **second** disposition for v1 —
state it plainly, and pin the residual with a node so it is visible in the
suite — and **defer rather than reject** the first, for a measured reason the
review did not have in front of it: all admission evidence is Darwin arm64
(known omission (e)), so a source-owned digest would make full mode
**unreachable on every other platform** and silently demote those adopters to
reduced mode. That is a behaviour change to the module's central classification
on a platform Cairn has never measured, and it is not a plan-time convenience.
M15 records both halves and opens LT-8. The design question — *should full mode
require a digest at all?* — is routed to the External round as a named
question rather than settled here.

**[I4] — accepted, and it is stronger than the review stated.** The review
checked `_always_on_group_complete` and found it `_ALWAYS_ON_MAPPINGS`-scoped.
I widened the search: `grep -n 'complete.*group\|group.*complete'
bootstrap/_scaffold/*.py` returns `cli.py:532`, `config.py:658`,
`install.py:893`, `:894`, `:897`, `:929`, `:1025`, `:1544`, `:1554`, and
`upgrade.py:153` — **every one of them scoped to the always-on onboarding
group**. There is no completeness enforcement of any kind for a
`_MODULE_MAPPINGS` group. So the node as specified cannot be written against
the engine as it is, and A4's planned engine comment would ship prose that
outruns the gate two rows above the criterion (A7) that exists to close exactly
that defect. M16 builds the guard the plan wanted and labels it honestly as a
**test-side membership pin, not an engine refusal**.

**[I5] and [I6] — the arithmetic is re-derived, the findings stand.** [I5]'s
recommendation is accepted whole; its roster is superseded by a third reading
(clean). [I6]'s *rule* reproduces exactly — `_is_per_module_necessity`
(`bootstrap/tests/_ast_attest.py:149-161`) returns True only for `Import:` /
`ImportFrom:` prefixes and the `Docstring` key, and `_classify` applies the
identical predicate baseline-side, so `Expr` and the `If` keys are fully
enforced. Its *arithmetic* does not: the baseline is now 12 non-declarable
entries, not 13, so **3 are enforced, not 4**, and its "nine are exempt" holds
by coincidence (`Import` 8 + `Docstring` 1 = 9 both before and after). Its
counterexample — *"the live run above reports `MISSING Try` as a hard failure
line"* — **does not reproduce**: there is no `Try` key in the baseline and the
live run is clean. The finding survives the loss of its counterexample because
the predicate is readable directly.

### Amendments in force

Each row names the superseded text **verbatim** (original emphasis marks
reproduced as written) and states what replaces it. Prior sections are not
edited; this table is the operative amendment and an implementing agent reads
it **before** the chunk it amends.

| ID | Location | Superseded text (verbatim) | Replaced by |
|---|---|---|---|
| **M1** | *The declared symbol delta — measured, not quoted* | "AST attestation OK — 174 baselined symbol(s) accounted for, unchanged" and "**174 entries total; 161 of the three declarable kinds**" | Re-measured at HEAD `e20b18e` on a clean tree, `as_of 2026-08-04`, after Ceremony 1 (`3852cf7`): **`AST attestation OK — 173 baselined symbol(s) accounted for, unchanged`**. **173 entries total; 161 of the three declarable kinds** — `FunctionDef` 98, `Assign` 53, `ClassDef` 10 (unchanged). The declared delta itself is **unchanged**: one CHANGED `Assign:_MODULE_MAPPINGS`, baseline digest `26957a8924042a0a`, 0 MISSING, 0 DUPLICATE, 0 non-exempt NEW. |
| **M2** | same section, next sentence | "The remaining 13 are `Import` 8, `Docstring` 1, `Expr` 1, `If` 1, `If#2` 1, `Try` 1, which `bootstrap/tests/_ast_attest.py`'s `_is_per_module_necessity` exempts in both directions." | The remaining **12** are `Import` 8, `If` 2 (`If`, `If#2`), `Docstring` 1, `Expr` 1; the `Try` key was removed by Ceremony 1. Of those 12, `_is_per_module_necessity` (`bootstrap/tests/_ast_attest.py:149-161`) exempts **9** — `Import` 8 plus `Docstring` 1 — and `_classify` applies the identical predicate on the baseline side. **`Expr` and both `If` keys are fully enforced in both directions**; the module docstring says so in terms (*"Executable top-level expressions stay enforced"*). The plan's "0 MISSING" declaration and its shape claim both depend on this, so the correction is load-bearing, not cosmetic. |
| **M3** | same section, next paragraph | "That verification was run against a **HEAD-only copy** of `bootstrap/_scaffold/*.py` extracted with `git show`, precisely because the live working tree is not clean (below)." | The working tree is **clean** as of this Response, so the figure above was taken directly against `bootstrap/_scaffold/*.py` in place. The HEAD-copy technique remains the correct method whenever the tree is dirty and an implementing agent should reach for it again rather than assume the tree is still clean. |
| **M4** | *One ceremony, shared with the cluster*, item 3 | "**The working tree is already carrying another scope's delta.** Measured `as_of 2026-08-04` against the live tree, before this plan writes anything: `AST attestation FAILED — 3 non-pure-motion symbol(s)`" — through — "This is exactly the confusion the shared-ceremony framing exists to prevent, and it is recorded here so it is read rather than discovered." | **The tree's drift state is a dated snapshot, never a roster, and must be re-measured at Chunk A start.** It has now read three different ways in one day: `FAILED — 3` when the plan was written, `FAILED — 6` (including a `MISSING Try`) when the review was written, and **`OK — 173 baselined symbol(s) accounted for, unchanged`, 0 non-pure-motion**, at HEAD `e20b18e` with a clean tree as of this Response. **Neither prior enumeration is authoritative and an implementing agent must not "fix" anything on the strength of either.** The standing rule, not the roster: run the attestation before Chunk A; attribute every reported entry to a named sibling scope; an entry attributable to none is a stop-and-explain. |
| **M5** | Chunk A, *Acceptance criteria*, first bullet | "**A third CHANGED symbol that is not attributable to a named sibling scope is a stop-and-explain, not a re-run.**" | **Any CHANGED, MISSING, DUPLICATE, or non-exempt NEW entry that is not attributable to a named sibling scope is a stop-and-explain, not a re-run.** The stop-rule discriminates on all four kinds because this plan's own delta is declared on all four ("0 MISSING, 0 DUPLICATE, 0 non-exempt NEW"), and because a `MISSING` — the kind the old rule was silent on — was present in this tree earlier today. No fixed count is asserted; the expected *attributable* set is whatever the pre-Chunk-A measurement shows. |
| **M6** | *Verification*, "The AST attestation" bullet | "Expected between Chunk A and the ceremony: **`AST attestation FAILED — 1 non-pure-motion symbol(s)`** naming `CHANGED Assign:_MODULE_MAPPINGS` and nothing else *attributable to this plan*." | Unchanged in substance and **confirmed** by re-derivation, with the stop-rule widened per M5: any CHANGED / MISSING / DUPLICATE / non-exempt NEW entry not attributable to a named sibling scope is a stop-and-explain. The pre-Chunk-A reading is measured, not predicted. |
| **M7** | Chunk M, item 4 | "`<N>` stays **174** for this plan's delta alone (a digest rewrite adds no key)" | `<N>` stays at whatever the pre-ceremony baseline carries — **173** `as_of 2026-08-04` — for this plan's delta alone (a digest rewrite adds no key). A sibling adding a top-level symbol moves it, which is that scope's figure to declare. |
| **M8** | Chunk A, *Acceptance criteria*, first bullet | "Baseline to re-measure at a clean HEAD before starting: **1601 passed, 0 failed, 0 skipped, 0 xfailed**, `as_of 2026-08-03` (measured by the `profile-parse-fail-open` plan; not re-measured here because the live tree carries three sibling scopes' uncommitted work, which would make any figure taken now meaningless)." | Measured at a clean HEAD (`e20b18e`, working tree clean) under the canonical interpreter, `as_of 2026-08-04`: **1790 passed, 0 failed, 0 skipped, 0 xfailed** in 186.71s. The 1601 figure was 189 nodes stale. **The re-measure instruction stands regardless** — the tree moved twice while this plan was under review and will move again; the figure is a sanity anchor, never a target to compare against. |
| **M9** | *Acceptance criteria* (plan level), first sub-bullet | "Re-measure the baseline at a clean HEAD before Chunk A; the last recorded figure is **1601 passed**, `as_of 2026-08-03`." | The last recorded figure is **1790 passed, 0 failed, 0 skipped, 0 xfailed**, `as_of 2026-08-04`, at clean HEAD `e20b18e`. Re-measure anyway. |
| **M10** | *Verification*, "The release Bandit gate" bullet | "Expected `PASS`; the shipped-file count moves **74 → 75** (`as_of 2026-08-04`); zero MEDIUM+; **no `B607`**." | Expected `PASS`; zero MEDIUM+; no `B607`. The shipped-file count moves **74 → 75 after Chunk A → 76 after Chunk F**. Measured mechanism, not inference: `scan_targets()` derives its `templates/` members from `_MODULE_MAPPINGS` / `_ALWAYS_ON_MAPPINGS` verbatim `.py` **sources**, so Chunk A's registration alone adds `templates/modules/team-gated/run_portable_security_sweeps.py`; and it derives its `scripts/` members from an **on-disk** `glob("*.py")`, so Chunk F's twin `scripts/run_portable_security_sweeps.py` adds a second. Live composition `as_of 2026-08-04`: 74 = templates 44 + scripts 16 + bootstrap 14. Chunk A's own criterion ("74 `as_of 2026-08-04`; expected **75** after A4") is **correct and unchanged**; it is the plan-level figure that was short by one. |
| **M11** | Chunk F, *Acceptance criteria* | (addition — Chunk F carried no `scan_targets()` criterion at all) | **New Chunk F criterion.** `~/conda_envs/lhm/bin/python3.13 bootstrap/security_check.py` → `PASS` with `scan_targets()` at **76**; zero MEDIUM+; no `B607`. The twin makes the runner a **second Bandit surface**, so Chunk B's LOW ledger (`B404`, `B603`) is **doubled** here — predicted, not discovered. This is harmless: there is no numeric LOW budget pin (verified — `bootstrap/tests/test_security_lint.py:44` sets `_BLOCKING_RANK = _SEVERITY_RANK["MEDIUM"]` and blocking is measured against a rationale'd `_ALLOWLIST`). `scripts/portable_security_policy.json` is not `.py` and moves no count — the same measured hole F5/F6 close for parity. |
| **M12** | Chunk M, item 5 | "`FROZEN-MODIFIED` for `bootstrap/security_check.py`, `bootstrap/tests/test_notice_install.py` and `bootstrap/tests/test_security_lint.py`, and `FROZEN-NEW` for `bootstrap/tests/test_portable_security_sweeps.py` and the three shipped module files." | The three FROZEN-MODIFIED entries are **correct** (all three confirmed members of `frozen_files`, 164 entries `as_of 2026-08-04`). The FROZEN-NEW enumeration is replaced. Measured against `_frozen_files()`'s five globs (`bootstrap/*.py`, `bootstrap/tests/**/*.py`, `bootstrap/tests/fixtures/**/*`, `scripts/*.py`, `templates/modules/**/*.py`), this plan creates **three** FROZEN-NEW across its whole span, not four: `templates/modules/team-gated/run_portable_security_sweeps.py` and `bootstrap/tests/test_portable_security_sweeps.py` at Chunk A, and **`scripts/run_portable_security_sweeps.py` at Chunk F**. The `.md` doctrine and the `.json` policy match **no** glob and produce no entry. Two further note classes must also be reported and were unnamed: **`MAPPING-DIGEST-CHANGED: _MODULE_MAPPINGS 26957a8924042a0a -> …`** — the gate-manifest line most directly tied to this change, since that digest *is* the declared delta — and **one `COLLECTION-ADDED` per new node** in `test_portable_security_sweeps.py` (`collection.node_count` = 1598 `as_of 2026-08-04`). The plan's *"not read by the suite"* claim is **verified**: `_MANIFEST_REL` is referenced only by `_gate_manifest.py` and `_gate_reanchor.py`; no `test_*.py` reads the committed fixture, so nothing goes red. "Report every stale entry and re-pin nothing" is only meaningful if the enumeration is complete; this one now is. |
| **M13** | Chunk C, C8 test table, first column of the `.git/config` row | "`test_hostile_repo_local_config_loses_to_the_counted_keys` — set all eight pinned keys hostilely in `.git/config`, with executable sentinels for hooks, fsmonitor, external diff, pager and transport; assert **no sentinel executed**." | Same name and same assertion, but the node is built on a **fake `gitleaks` that itself execs the real `git`** — measured present at `git version 2.53.0`, and the *second* declared trust root — under exactly the child environment the runner constructed, with a subcommand that would actually consult the sentinel keys (`git log -p` reaches `core.pager`, `diff.external`, `core.hooksPath`, `core.fsmonitor` and the transport keys). Only then is the stated perturbation ("Drop `GIT_CONFIG_COUNT` from C6; a sentinel fires and the test goes red") **runnable**, and the ledger must record it as a RUN. **What this establishes and does not**: it establishes that the environment *the runner constructs* neutralizes a hostile repository-local config against real Git. It establishes **nothing** about whether real Gitleaks propagates that environment faithfully to its own Git child — that stays Chunk I's, and the doctrine must not imply otherwise. |
| **M14** | Chunk C, C8 test table, four further rows | "`test_a_hostile_gitleaks_toml_does_not_suppress`", "`test_a_tracked_gitattributes_binary_rule_cannot_hide_a_committed_token`", "`test_the_current_tree_leg_does_not_follow_a_symlink_out_of_the_repo`", "`test_a_gitignored_ordinary_file_is_still_scanned`" | Renamed to the claim a fake executable can actually carry — an **argv/environment** claim, not a scanning outcome: `test_the_adapter_config_flag_is_sent_and_a_candidate_toml_is_never_read`, `test_the_history_leg_argv_carries_text_no_textconv_and_no_ext_diff`, `test_the_current_tree_leg_argv_disables_symlink_following`, `test_the_current_tree_leg_argv_adds_no_gitignore_filter`. Their perturbations are unchanged and remain valid (each drops the flag from C1/C5/C7 and the fake records its absence). **The four behavioural names move to Chunk I**, whose Maintainer-gated hostile-config matrix is where a real binary can establish them. Two nodes sharing a name across C8 and Chunk I, one of them vacuous, is the outcome this rename exists to prevent. |
| **M15** | Chunk C, *Acceptance criteria*, first bullet | "Every C8 node passes with **fake executables**, and the fake tool asserts on the **exact argv and the exact child environment**, not on a substring." | Every C8 node passes with **fake executables** and asserts on the **exact argv and the exact child environment**, not on a substring — **except `test_hostile_repo_local_config_loses_to_the_counted_keys`, which is behavioural against the real `git` per M13 and needs no third-party binary.** Add: **every C8 node's name must state a claim its own oracle can carry.** A node named for a scanning outcome whose oracle is a fake tool's argv log is vacuous by construction, and vacuity of that kind is a stop, not a style note. |
| **M16** | Chunk D, D7 test table | (addition) | **New D7 node — `test_no_secret_bearing_field_reaches_any_sink`.** Feed a fake report whose `Secret`, `Match`, `Author`, `Email` and `Message` fields carry distinct planted byte sequences; assert **none** of those sequences appears in any of the three sinks: the deterministic JSON summary (D3), the human report (D2/D3), **and** the child document (D6). Hazard perturbation: add one of those fields to D1's selection list; the node goes red on all three sinks. This is the positive counterpart to `test_missing_redaction_is_degraded`, which is a *refusal* node and fires only when the tool's own redaction is absent — as specified, a `.get("Secret")` added to D1's selection list would turn **no** node red anywhere in this plan. It is the one failure mode in which the module is strictly worse than not existing: a secrets scanner that harvests secrets into a JSON artifact and a terminal report. |
| **M17** | *Author-accounting*, invariant list | "*No raw child output reaches the operator.* Chunk D7's rendering nodes." | Two invariants, not one. (i) *No raw child output reaches the operator.* Chunk D7's rendering nodes. (ii) ***No secret-bearing scanner field reaches any sink — summary, human report, or child document.*** Chunk D7's `test_no_secret_bearing_field_reaches_any_sink` (M16). |
| **M18** | *Author-accounting*, known omissions, (a) | "(a) **v1 does not authenticate host binaries.** Gitleaks and Git are declared executable trust roots; a project needing provenance pins and verifies them outside Cairn." | (a) **v1 does not authenticate host binaries, and the specific consequence is named rather than left at the level of provenance-in-general: full mode — the only mode that can reach CLEAN — is entered on a version string the unauthenticated binary reports about itself.** E3's recorded SHA-256 is **evidence-only**: it documents which artifact the admission matrix was run against and is **never compared** against the binary resolved at run time. Any binary on `PATH` that prints an admitted version string is classified full mode. Gitleaks and Git remain declared executable trust roots; a project needing provenance pins and verifies them outside Cairn. **The shipped doctrine (A1) and the cadence text (E6) must state this in these terms** — that the recorded digest is evidence, not a gate — because a silently-recorded digest reads to an adopter and to a later reviewer as a control. |
| **M19** | Chunk E, E7 test table | (addition) | **New E7 node — `test_the_recorded_digest_is_not_a_runtime_gate`.** Admit a version in E1 whose evidence record carries digest X; resolve a fake binary that reports that version string and hashes to Y; assert the run **still selects full mode** and that the report **names the residual in words**. Hazard perturbation: make resolution compare the digest; the node goes red — which is the point. The node exists so the residual is visible **in the suite** rather than implied in a doctrine file an adopter may never open, and so that a future change from evidence-only to gate is a deliberate, red-turning edit rather than a silent one. |
| **M20** | *Lasting-truth migration* | (addition) | **LT-8 — the full-mode digest gate.** Deferred, not rejected. A source-owned optional digest checked at resolution (mismatch degrading to reduced mode rather than refusing, so `test_reduced_mode_is_reachable_without_any_source_change` survives) is the stronger design, and it is **blocked on cross-platform evidence**: all admission evidence is Darwin arm64 (known omission (e), LT-5), so a source-pinned digest today would make full mode **unreachable on every other platform** and silently demote those adopters to reduced mode. Durable home: `dev/measurement/gitleaks-version-support.md` carries the per-version, per-platform digests as they accumulate; the promotion from evidence-only to gate is its own proposal once more than one platform is admitted. |
| **M21** | Chunk A, A4 cell | "A comment states the two facts a later reader needs: the three files are **one complete mapping group** (an upgrade cannot advance part of the apparatus), and the module declares **no required token**" | A comment states the two facts a later reader needs: the three files are **registered as one group and pinned as one group by `bootstrap/tests/test_portable_security_sweeps.py`** — **the engine performs no group-completeness refusal for `_MODULE_MAPPINGS` and the comment must not imply one** — and the module declares **no required token**. Measured: `grep -n 'complete.*group\|group.*complete' bootstrap/_scaffold/*.py` returns ten hits (`cli.py:532`, `config.py:658`, `install.py:893`, `:894`, `:897`, `:929`, `:1025`, `:1544`, `:1554`, `upgrade.py:153`) and **every one is scoped to the always-on onboarding group**; `_always_on_group_complete` (`bootstrap/_scaffold/upgrade.py:153-165`) iterates `_ALWAYS_ON_MAPPINGS` and nothing else. What a `_MODULE_MAPPINGS` group actually gets is duplicate-**destination** refusal (`_assert_mapping_ownership`, defined at `upgrade.py:263`, called at `:503`) and the already-adopted-module new-file delivery path — **neither refuses a missing group member**. Shipping an engine comment that asserts a refusal the engine does not perform is the *"prose that outruns the gate"* defect A7 exists to close, two rows above it. |
| **M22** | Chunk A, A8 test table, second row | "`test_the_three_files_are_one_complete_mapping_group` — assert an upgrade cannot advance the runner without the policy and doctrine." / "Remove the policy spec from A4's group; the group check must refuse." | **`test_the_registration_pins_all_three_specs_as_one_group`** — a **test-side membership pin** over `_MODULE_MAPPINGS["portable-security-sweeps"]`: assert the group contains exactly the three declared `(src, dst, verbatim)` triples, no more and no fewer. Hazard perturbation: **remove the policy spec from A4's registration; this pin goes red — and nothing in the engine refuses, which is precisely why the pin exists.** The node must be distinguishable from `test_the_module_installs_exactly_three_files`: that one drives the scaffold's public install path and observes destinations on disk; this one pins the registration's declared shape. |
| **M23** | *Author-accounting*, invariant list | "*The three module files are one complete mapping group.* Chunk A8." | *The three module files are **registered and pinned** as one group.* Chunk A8's `test_the_registration_pins_all_three_specs_as_one_group`. **This is a test-side pin, not an engine refusal** — the engine's only group-completeness enforcement is scoped to the always-on onboarding group (M21). Named here as the **second** weakest invariant in this plan, beside the manifest-row invariant the plan already names, and an External reviewer should attack both. |
| **M24** | Chunk E, E2 cell | "It runs the same hostile-ambient-config fixtures as Chunk C, the same output-schema validation as Chunk D, the Git-invocation oracle, and the end-to-end exits. **It never mutates E1** — admission stays a reviewed human code change." | Unchanged, plus the **containment disposition the design raises and the plan did not answer**: `--verify-version-support` is a public "execute the binary at this path" entry point that ships in every adopter tree selecting the module, and Chunk B's containment rules bind it **in modified form**, because blanket application would break its purpose (the candidate is by definition not yet admitted) and blanket exemption ships an unconstrained exec path. The rules: the candidate path must be **absolute**, a **regular file** with the **executable bit**, and **outside the repository under check** on both its lexical and its resolved path. It is **not** required to be an admitted version — that is the subcommand's whole point. A candidate failing any of those refuses before execution. |
| **M25** | Chunk E, E7 test table | (addition) | **New E7 node — `test_verify_version_support_refuses_a_candidate_inside_the_repository_under_check`**, in both the lexical and the symlink-resolved form, mirroring B6's `test_a_repo_local_executable_is_refused` and `test_a_symlink_resolving_into_the_repo_is_refused`. Hazard perturbation: delete the containment check from E2; the subcommand executes the planted in-repo binary and the node goes red. |
| **M26** | Chunk G, test table, third row | "`test_the_registry_cannot_reach_a_network_or_credential_mode` — assert the row names only the offline entry point." | Same name, stronger assertion: pin the row's argv **exactly** against the local/offline entry point, and assert it does **not** name `--verify-version-support`. As written the node was satisfiable by a row naming the admission subcommand, which is *also* offline — so "offline" does not exclude it. A standing agent command must never be able to reach the admission path. Hazard perturbation: point the row's argv at `--verify-version-support`; the node goes red. |
| **M27** | Chunk F, *Acceptance criteria* | "**Explicitly not done here.** No CI workflow is edited. No scanner is installed. Cairn's standing verification cadence is `security-verification-activation`'s surface, reached through Chunk G." | No CI workflow is edited. No scanner is installed. **And Cairn gets no standing invocation path at v1**: `dev/plans/security-verification-activation.md` fences *"Cairn does not self-host the dispatcher"* (`:433`), so no dispatcher twin lands under Cairn's `scripts/`. Chunk G's registry row therefore makes the portable leg reachable from the standing command **for adopters only**. Condition 2's *"Cairn installs and runs this module on its own tree"* is discharged at v1 by a **hand-typed invocation** of `scripts/run_portable_security_sweeps.py`, and Chunk F's commit-body figure is that run's result. Stated plainly because the alternative is an implementing agent looking for a standing hook that does not exist. |
| **M28** | *What survived the lifecycle*, Consequence 3 | "**The adoption HOLD is resolved and does not survive into the plan.** The standing invocation path exists — `security-verification-activation`, accepted the same day — and the Decision answers the "worth building at all" question affirmatively by directing adoption." | The adoption HOLD is resolved **for adopters**: the standing invocation path exists in `security-verification-activation`, and the Decision answers the "worth building at all" question affirmatively by directing adoption. **For Cairn itself — the one adopter Condition 2 names — the standing path does not exist at v1**, because that plan declines to self-host the dispatcher (M27). The HOLD survives in that one place, and saying so is more useful than a clean claim. |
| **M29** | Chunk G / *Lasting-truth migration* | (addition) | **LT-9 — the two plans' Branch-1 interaction, recorded so neither plan can leave it to the other.** `security-verification-activation` justifies not self-hosting partly on the ground that at v1 Cairn's own run *"would print `NOT APPLICABLE` and gather nothing"* (`dev/plans/security-verification-activation.md:436-437`, reproduced exactly). **That premise expires the moment Chunk G admits the portable row and Chunk F makes Cairn an adopter of the module** — which is precisely the combination this plan lands. Chunk G's implementing agent, under either branch, must record this in the commit body and surface it to whichever plan lands second. Durable home: this row, plus a `dev/PLANNING.md` row so it cannot fall between the two plans. |
| **M30** | Chunk F, F6 test table | "Remove `portable-security-sweeps` from `dev/.cairn/profile.yml` without regenerating; red." | The node reads `dev/.cairn/cairn-lock.yml`; editing `profile.yml` **without regenerating** leaves the lockfile byte-identical, so the node stays **green** and the perturbation as written cannot make it red. Replaced by either of two perturbations that bite: **drop one spec from A4's registration and regenerate the lockfile**, or **remove one of the three records from the lockfile directly**. Name which was run in the ledger. |
| **M31** | Chunk A, A8 test table | "`test_adopt_module_and_upgrade_carry_the_whole_group` … Drop one file from the lockfile record; the integrity read must not report clean." | That perturbation perturbs `verify_integrity`'s **input** and exercises `verify_integrity`, not the `--adopt-module` / `upgrade` path the node is named for. Replaced: **remove one spec from A4's registration**, then run `--adopt-module portable-security-sweeps` against a tree installed before the module existed; the node's write-set assertion goes red because only two files are written. The hazard is the registration or the adopt write-set, not the lockfile reader. |
| **M32** | Chunk D, D7 test table | "`test_missing_redaction_is_degraded` … Drop the redaction assertion; red." | Ambiguous between the **runner's** redaction check (the hazard) and the **test's** own assert (self-validating). Replaced: **delete the runner-side branch in D1 that classifies an unredacted secret field as DEGRADED**; the node goes red. Perturbing the test's own body validates the test, not the claim — the plan says so in its own words two tables earlier. |
| **M33** | Chunk A, A8 test table | "`test_mode_selection_maps_versions_to_modes` … Add `"8.31.0"` to the source-owned full-mode set without an evidence record; Chunk E's admission test (below) goes red, and this test's reduced-mode case goes red too." | Chunk E's bijection node does not exist at Chunk A commit time, so half this perturbation is **not runnable when A's ledger obligation falls due**. Split it: **A's runnable half** is the reduced-mode case — add a strict `8.x.y` to the full-mode set and this node's reduced-mode assertion goes red, run and ledgered at Chunk A. **The bijection half completes at Chunk E** and is ledgered there, in the E7 entry for `test_every_full_mode_version_has_an_evidence_record_in_the_ledger`. State the split in A's ledger rather than claiming a red that could not be observed. |
| **M34** | *Acceptance criteria* (plan level), fourth sub-bullet | "`bootstrap/tests/test_manifest.py` — unchanged and green; its `test_matches_actual_install` scaffolds **every** module, so it is the node that catches a registration whose sources do not exist or whose destinations collide." | The node is **`test_manifest_matches_actual_install`** (`bootstrap/tests/test_manifest.py:68`), and the two properties are split across **three** mechanisms, not one node: sources-exist is `test_manifest_sources_all_exist` (`:61`); destination collision is refused by **`install_manifest` itself**, which calls `duplicate_destinations` (`bootstrap/_scaffold/install.py:1392`) and raises `ValueError` (`:1396`). That third mechanism is what makes A8's `test_module_destinations_collide_with_nothing` perturbation a real hazard perturbation — verified. |
| **M35** | *One ceremony*, item 2, and Chunk M, item 3 | "`bootstrap/tests/_ast_attest.py`'s `_UPDATE_ALLOWLIST` (line 141, alongside `_SKILLS_MAPPINGS`, `_CORE_MAPPINGS`, `install_onboarding`)" and "(`bootstrap/tests/_ast_attest.py:141`)" | `:141` is the `_UPDATE_ALLOWLIST` **declaration**; the `"_MODULE_MAPPINGS": "Assign"` entry is line **`:142`**. Cite `:141-146` for the allowlist or `:142` for the entry. The substantive claim — `_MODULE_MAPPINGS` is allowlisted for `update-symbol` alongside `_SKILLS_MAPPINGS`, `_CORE_MAPPINGS` and `install_onboarding`, and `update-symbol` refuses (exit 4) on any unrelated drift — is **correct and re-verified**. |
| **M36** | Chunk A, A4 cell | "unlike the `"python-security"` key two entries above it" | "unlike the `"python-security"` key **one entry above it**". Measured key order ends `… content-security, python-security, architecture-review`, so an insert before `"architecture-review"` puts `python-security` one entry above. Trivial, but it is a comment destined for the engine. |
| **M37** | Chunk H, *Acceptance criteria*, first bullet | "**180 Markdown files `as_of 2026-08-04`**; the count may only grow" | **195 Markdown files `as_of 2026-08-04`** — re-measured (`check_cairn: OK -- 195 Markdown file(s) scanned; no issues; 68 external link(s) not probed`). The 180 figure, correct when the plan and review were written, was overtaken the same day. The count may only grow, and the growth arithmetic is unchanged: this plan adds at least three (the plan, the shipped doctrine, the ledger) plus one at Chunk F. **Re-measure; do not assert 195 either.** |
| **M38** | Chunk A, A7 cell | "The comment at `bootstrap/security_check.py:74` reads *"42 entries are a subset of the manifest's 44"*. Re-measure and correct." | The cited prose is **verified exact**, and so is its arithmetic: the two registry loops yield 33 (`_MODULE_MAPPINGS`) + 9 (`_ALWAYS_ON_MAPPINGS`) = **42**, and `_manifest_py_sources()` = **44**. Predicted after Chunk A: **43 entries, a subset of the manifest's 45** (the registration adds one verbatim `.py` to `_MODULE_MAPPINGS`). **Re-measure and assert; do not apply that arithmetic from this text** — the same rule the plan applies to its count pins. |
| **M39** | Chunk A, *Acceptance criteria*, the `.json` bullet | "Confirm it installs byte-for-byte (`verbatim=True`)" | Confirm it installs byte-for-byte, **with the measured qualification the plan's own "verify, do not assume" posture asks for**: `verbatim=True` skips substitution and the unfilled-token / block-slot scan (`bootstrap/_scaffold/install.py:235-237`, branching on the flag and **not** on extension — verified, so the `.json` is not filtered out anywhere), but the install path is a **UTF-8 text round-trip**, not a byte copy: `text = src.read_text(encoding="utf-8")` runs *before* the verbatim branch and `dst.write_text(text, encoding="utf-8")` writes it back. Two consequences to assert rather than assume: the source must be **valid UTF-8** (else the install raises), and **universal-newline translation applies**, so a CRLF source would install as LF and would not be byte-identical. Keep the policy source UTF-8 and LF-only. The same qualification bounds F5/F6's twin-parity node. |
| **M40** | *Plan review — the brief*, "Where the reviewer should look first" | (addition, adopting the Internal reviewer's own recommendation) | **New item 2a — Chunk C's fake-executable boundary.** Whether each C8 node's *name* states a claim its own oracle can carry, and specifically whether `test_hostile_repo_local_config_loses_to_the_counted_keys` as amended by M13 is genuinely falsifiable. The framing question already at item 2 — does *"a measured finite boundary"* survive contact with a second Git subcommand — is unanswerable if the node defending it cannot go red. **New item 6 — the full-mode digest question ([I3] / M18-M20):** is it acceptable for the only CLEAN-capable mode to be selected on a self-reported version string, with the recorded SHA-256 evidence-only? The author's v1 answer is "yes, disclosed and pinned by a node"; the deferral of the stronger design rests on Darwin-arm64-only evidence. **This is a security-lens call and it is put to the External reviewer as a question, not presented as settled.** |

### What this Response clears, and what it does not

**It does not clear the plan to implement.** Stated without hedging:

* The declared tier is **`required(External, security lens)`** and it is
  **undischarged**. The Internal round did not close it (its author said so;
  the plan's brief says so; the Decision says so in terms). **An author's
  Response to an Internal round closes nothing** — it is the same agent type
  reading its own artifact, twice.
* **No implementation commit lands before a `## Plan review` section written by
  a different agent type or a human is in the tree.** The plan's own header
  rule is unchanged and this Response does not relax it.
* The plan's remaining open questions are exactly the ones the Internal
  reviewer identified as the ones they were worst-placed to answer, and I am
  worse-placed still, being the author: whether eight pinned Git-config keys
  plus one measured invocation set actually bound the candidate metadata
  surface, or only the symptoms enumerated so far; whether
  `--verify-version-support` is an apparatus or a matrix runner with a ledger
  bolted on; whether automatically executing an unmeasured host binary in
  reduced mode is acceptable given the named residual; and now, per M40,
  whether full mode may be entered on a self-report.

**What it does clear.** Forty amendments are in force. Every accepted finding
has mechanical residue — a renamed node, a rewritten perturbation, a new test
node, a new or corrected acceptance criterion, a corrected figure, or a new
`Lasting-truth` row. No finding was accepted in prose alone. Three defects the
Internal reviewer flagged as the ones that would waste an External round —
[I1]'s vacuous enforcer, [I2]'s missing positive redaction node, [I3]'s
recorded-but-unchecked digest — are settled in the plan text, so an External
reviewer meets an artifact that no longer claims more assurance than its
specified tests can deliver.

**One thing worth carrying into the ceremony unchanged.** The declared
`bootstrap/_scaffold/` symbol delta — **one CHANGED `Assign:_MODULE_MAPPINGS`,
baseline digest `26957a8924042a0a`, 0 MISSING, 0 DUPLICATE, 0 non-exempt NEW**
— was re-derived a third time today, after Ceremony 1 re-anchored the baseline
from 174 entries to 173, and it is **unchanged**. The baseline total moved; the
digest this plan declares did not.

**Verification of this Response.**
`~/conda_envs/lhm/bin/python3.13 scripts/claim_check.py dev/plans/portable-security-sweeps.md`
→ OK, no claim-check flags (exit 0). `git diff --numstat` on this file → 0
deletions (append-only, confirmed before commit).

This section is append-only once written.

### Figure correction -- Claude -- 2026-08-04

**What this is.** An audit of the Response above (commit `5a817ff`) reported
that two figures it labels *"Measured:"* / *"verified"* do not reproduce, and
that three narrative sentences cite the wrong amendment row. This section is a
**third, independent measurement**: I took no number from the Response and no
number from the audit, re-ran every disputed figure from scratch by two
methods, and record the commands and the commits. **No disposition moves.**
Nothing here accepts, declines, re-opens or withdraws a finding; two amendments
carry a corrected figure and both keep their conclusions, for reasons I
re-derived rather than inherited.

**Provenance of every run below.** Canonical interpreter
`~/conda_envs/lhm/bin/python3.13` (CPython 3.13.13),
`PYTHONDONTWRITEBYTECODE=1`, `as_of 2026-08-04`. Live-tree runs were executed
at HEAD `9052b09` and repeated at `e59f9d4` and `640864e` as sibling commits
landed under me — identical results at all three. **Tree drift cannot explain
any difference here**: `bootstrap/_scaffold/` is byte-identical between
`e20b18e` — the Response's own stated measurement HEAD — and every HEAD I ran
at (`git diff --stat e20b18e <HEAD> -- bootstrap/_scaffold/` is empty), and
`git status --short bootstrap/_scaffold/` is clean throughout. Both figures
were *also* taken against the `e20b18e` **tree object** with `git grep`, which
reads the committed tree and never the working copy, and both agree with the
live-tree runs exactly.

#### 1. The [I4] widened grep — M21, and the narrative that introduces it

| | figure |
|---|---|
| Response (`5a817ff`) | **ten hits** |
| Audit | 23 |
| **This measurement** | **23** |

Two commands, neither piped into anything that could truncate:

* live tree, HEAD `9052b09` —
  `grep -n 'complete.*group\|group.*complete' bootstrap/_scaffold/*.py | wc -l`
  → **23**
* committed tree at the Response's own stated HEAD —
  `git grep -n -e 'complete.*group' -e 'group.*complete' e20b18e -- 'bootstrap/_scaffold/*.py' | wc -l`
  → **23**

Per file: `cli.py` 1, `config.py` 1, `install.py` 7, `upgrade.py` **14**. The
thirteen hits the Response omitted are all in `upgrade.py`: `:157`, `:196`,
`:593`, `:608`, `:612`, `:615`, `:616`, `:720`, `:726`, `:1526`, `:1527`,
`:1532`, `:1534`.

**Why ten, specifically.** Re-running the command against an explicitly sorted
file list (`$(ls bootstrap/_scaffold/*.py | sort)`) and taking the first twelve
lines shows that the ten recorded hits are, byte-identically and in order, the
**first ten lines** of the command's output: `cli.py:532`, `config.py:658`,
`install.py` × 7, `upgrade.py:153`. A ten-line default `head` is the only
mechanism I can construct that yields exactly that prefix. The boundary is the
reader's, not the code's — `upgrade.py:157` is the docstring of the very
function whose `def` line at `:153` is the tenth hit.

**Does M21 still hold? YES — in force, figure corrected.** Its conclusion never
depended on the count, and I re-derived that conclusion rather than assuming
it: I read all 23 hits with their surrounding code, and every one is scoped to
the always-on launcher+engine group. `_always_on_group_complete`
(`bootstrap/_scaffold/upgrade.py:153-165`) is
`all(... for spec in _ALWAYS_ON_MAPPINGS)` — read, not quoted; its only two
call sites (`upgrade.py:612`, `:1532`) are both guarded by
`always_on_dsts = {spec.dst for spec in _ALWAYS_ON_MAPPINGS}` (`:611`,
`:1523`); `install.py`'s seven and `cli.py:532` are the R4 always-on onboarding
group; `config.py:658` documents *"the launcher + the eight engine members"*. I
also widened past the Response's vocabulary — `grep -n 'incomplete'
bootstrap/_scaffold/*.py` — and the hits that are **not** always-on are profile
completeness (`upgrade.py:225`, `:256`, `:1172`) and a merge-section note
(`config.py:1401`); none is a mapping-group refusal. So M21's operative
instruction to A4 — *"the engine performs no group-completeness refusal for
`_MODULE_MAPPINGS` and the comment must not imply one"* — is unchanged, and now
rests on 23 hits read rather than ten inherited from a truncated pipe.

**Correction to the text.** In M21 and in the [I4] narrative, read **"returns
twenty-three hits"**, with the thirteen `upgrade.py` lines above added to the
ten already listed. Everything else in M21 stands.

#### 2. `_MANIFEST_REL` — M12's closing evidence, and the reproduction-ledger row

Claimed: *"`_MANIFEST_REL` is referenced only in `_gate_manifest.py` and
`_gate_reanchor.py`; no `test_*.py` reads it"* (ledger row, verdict `yes`) and
*"the plan's `not read by the suite` claim is **verified**: `_MANIFEST_REL` is
referenced only by `_gate_manifest.py` and `_gate_reanchor.py`; no `test_*.py`
reads the committed fixture"* (M12).

Measured — `grep -rn '_MANIFEST_REL' bootstrap/ scripts/` (live, HEAD
`9052b09`) and `git grep -n '_MANIFEST_REL' e20b18e -- bootstrap scripts`,
identical sets: **six modules, 40 reference lines, three of them `test_*.py`.**

| module | reference lines | note |
|---|---|---|
| `bootstrap/tests/_gate_manifest.py` | 5 | **defines** the constant at `:72` |
| `bootstrap/tests/_gate_preflight.py` | 9 | **defines** it at `:54` |
| `bootstrap/tests/_gate_reanchor.py` | 5 | **defines** it at `:60` |
| `bootstrap/tests/test_gate_manifest.py` | 4 | `test_*.py` |
| `bootstrap/tests/test_gate_preflight.py` | 7 | `test_*.py` |
| `bootstrap/tests/test_gate_reanchor.py` | 10 | `test_*.py` |

**Does M12 still hold? YES — in force, evidence corrected.** M12's substantive
content — three FROZEN-MODIFIED confirmed, three FROZEN-NEW not four, the two
unnamed note classes (`MAPPING-DIGEST-CHANGED`, per-node `COLLECTION-ADDED`) —
is untouched by this and I re-checked none of it here. Its closing conclusion,
*"nothing goes red"*, also survives, but on a **different and stronger basis**
that I derived myself: no test reads the **committed** fixture. Every
`test_*.py` use of the constant addresses a synthetic repo — `_write(repo,
P._MANIFEST_REL, ...)`, `(repo / R._MANIFEST_REL).write_text(...)`, and in
`test_gate_manifest.py` a `tmp_path` target at `:166` and `:197`. The one
live-tree assertion, `test_gate_manifest.py:65`
(`assert G._MANIFEST_REL not in frozen`), reads `frozen =
produced["frozen_files"]` where `produced` is the module-scoped fixture
`G.produce(_REPO)` (`:30-33`, `:48-49`) — a manifest **recomputed at run
time**, not the committed artifact — and asserts only that the manifest path is
absent from `frozen_files`, which a stale manifest does not disturb. A search
for readers of the fixture path itself (`grep -rn "fixtures/gate_manifest"
--include="*.py" bootstrap scripts templates`) returns only the three `_gate_*`
helpers' own definitions and `_gate_manifest.py`'s docstring.

**Correction to the text.** In M12 and in the ledger row's middle column,
replace *"referenced only by `_gate_manifest.py` and `_gate_reanchor.py`; no
`test_*.py` reads it"* with: **the constant is defined in three helpers
(`_gate_manifest.py:72`, `_gate_preflight.py:54`, `_gate_reanchor.py:60`) and
referenced by six modules, three of them `test_*.py`; no test reads the
committed fixture — every `test_*.py` use targets a synthetic temp repo, and
`test_gate_manifest.py:65` asserts only non-membership in a freshly *produced*
`frozen_files`.** The ledger verdict stays `yes` for the *plan's* claim ("the
committed gate manifest is not read by the suite"), which is what that row
adjudicates; it is the evidence column that was false.

#### 3. Three narrative cross-references — verified, table unaffected

These are not figures, and I checked them by reading the amendment table in
this same section rather than by accepting the audit's mapping:

| narrative sentence | names | content actually lives in |
|---|---|---|
| *"One thing route 1 must state and **M11** does"* | M11 | **M13** — which carries *"What this establishes and does not"* verbatim. M11 is Chunk F's new `scan_targets()` = 76 criterion. |
| *"**M15** records both halves and opens LT-8"* | M15 | **M18** (both halves of [I3]) and **M20** (which opens LT-8), with **M19** pinning the residual as an E7 node. M15 is Chunk C's acceptance criteria. |
| *"**M16** builds the guard the plan wanted … a test-side membership pin"* | M16 | **M22** — which carries *"a **test-side membership pin**"* verbatim. M16 is the D7 `test_no_secret_bearing_field_reaches_any_sink` node. |

All three amendment **rows are correct where they sit**; only the sentences
pointing at them are wrong. Under this Response's own rule — the table *"is the
operative amendment and an implementing agent reads it before the chunk it
amends"* — no amendment changes. An implementing agent following the narrative
should read **M13**, **M18/M19/M20**, and **M22** respectively.

#### Where this measurement differs from the audit

Confirmed exactly, by independent runs: **23**; the thirteen omitted
`upgrade.py` line numbers; the head-ten-prefix explanation; **six** modules and
**three** `test_*.py`; and the `M11 → M13` and `M16 → M22` corrections.

One correction **to the audit**. It names `bootstrap/tests/_gate_preflight.py:54`
as *"where `_MANIFEST_REL` is DEFINED"* and says *"the module that defines the
constant is not named at all"*. There is no single definition site: the
constant is defined independently, with the same string literal, in **three**
modules — `_gate_manifest.py:72`, `_gate_preflight.py:54`,
`_gate_reanchor.py:60`. The Response named two of those three; the definer it
missed is `_gate_preflight.py`. The defect is real and its size is unchanged —
the false parts are "referenced only by two modules" and "no `test_*.py`" — but
a reader should not take "the definer" to be singular. One extension: for the
`M15` sentence the audit gives M18 + M20; **M19** belongs with them, since the
[I3] disposition row's own residue column reads "M18, M19, M20, M40" and M19 is
the node that makes the residual visible in the suite.

#### Standing

**This section corrects figures only.** No disposition moves. **No amendment is
withdrawn**: M21's and M12's conclusions are each independent of the figure that
was wrong, and each was re-derived here from the code rather than carried
forward. The declared tier remains **`required(External, security lens)`** and
**undischarged**; this section discharges nothing and no implementation commit
lands on its strength. The lesson is the one this cycle keeps finding, in a new
place: *what supplied the material this check ran on?* — here, twice, a reader
that stopped early, in a Response whose own method paragraph claims every figure
was re-derived by execution.

**Verification of this section.**
`~/conda_envs/lhm/bin/python3.13 scripts/claim_check.py dev/plans/portable-security-sweeps.md`
→ OK, no flags (exit 0). `git diff --numstat` on this file → **0 deletions**
(append-only, confirmed before commit). Path-scoped commit, this file only.

This section is append-only once written.
