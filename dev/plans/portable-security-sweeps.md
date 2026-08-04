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
`dev/proposals/2026-08-03-codex-portable-security-sweeps.md` and moves to
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
