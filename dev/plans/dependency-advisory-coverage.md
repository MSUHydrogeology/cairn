<!-- cairn-internal-ref-allow: doctrine/rationale.md doctrine/plans.md doctrine/dual-review.md doctrine/coordination.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: scripts/run_security_audit.py -->
<!-- ^ ADOPTER-TREE DESTINATION path -- where the orchestrator lands in an installed
     target. It does not resolve in Cairn's source tree (verified: `ls scripts/`
     has no such file, and Cairn's own dev/.cairn/cairn-lock.yml records zero
     `run_security_audit` entries, so python-security is not installed on Cairn
     itself). The source of truth is templates/modules/team-gated/run_security_audit.py.
     Same directive and reason as the source proposal. -->

# Plan: the dependency leg audits Python distributions — and can prove which ones

**Source proposal**: `dependency-advisory-coverage` (accepted 2026-08-03 by
Maintainer Decision, *"I accept the dependency-advisory-coverage proposal as
revised"*). It currently sits under `dev/proposals/` and moves to
`dev/proposals/archive/` when it archives.
**Status**: open
**Plan review**: required(**External**, security lens) — carried from the
proposal's Decision (*"Next transition: plan-open, carrying `required(External,
security lens)` in its own right"*) and independently triggered: `AGENTS.md` >
*High-risk surfaces* names the shipped security stack. **Not** discharged by an
Internal round — see *Plan review — the brief*. **No implementation commit lands
before a `### Plan review -- <reviewer> -- YYYY-MM-DD` sub-heading is in the
tree.**
**Last update**: 2026-08-04
**Opened**: 2026-08-04

## Source proposal

`dependency-advisory-coverage` settles one contract: **`python-security` audits
the Python distributions in the named environment, says so at selection, and
returns CLEAN only when nothing about that set is UNKNOWN.** The plan executes
that decision and does not re-litigate it.

The artifact is long because it changed shape twice. The order that matters:
the original proposal → amendment 1 (*coverage gates CLEAN*) → amendment 2 (*the
binary rule was defective; 100% accounted-for, not 100% scanned*) → a Codex
External security review (seven findings, `DAC1`–`DAC7`, all accepted, HOLD) →
Maintainer direction *"Let's go scope narrowing"* → the **Revised proposal** →
a Gemini Flash External re-review (SHIP, two concerns) → the author Response
bounding the residual → the **Decision**.

**Where earlier text disagrees, the Decision wins**, and this plan is written
against the Decision. Two consequences a reader of the amendments would get
wrong:

* Amendment 1's *"a leg returns CLEAN only when it has established coverage over
  the thing it names"*, with *the environment* as the denominator, is
  **superseded**. Amendment 2 recorded that the two-state (binary) rule was
  defective — it yields permanent INCOMPLETE, which is finding `PS4`'s failure
  mode. The scope narrowing then replaced the denominator: it is the **Python
  distribution inventory the child enumerated**, not the environment.
* Amendment 2's `NO-ADVISORY-SOURCE` disposition is **withdrawn** (`DAC3`): it
  asserted a universal negative from a bounded query. The accepted third
  disposition is `NO-MATCH-IN-PINNED-SOURCES`, which names every source and
  version queried and is **accepted non-coverage, not evidence of safety**.

### Glossary — every term glossed on first use

The audience is a scientist who codes, and this scope turns on distinctions that
are easy to nod at and hard to hold.

* **pip-audit** — a third-party tool that reads the installed Python
  distributions of an interpreter and looks each up in a vulnerability service.
  Cairn **does not install it**; the adopter provides it. It is Exception 1 in
  [`bootstrap/DEPENDENCY_BUDGET.md`](../../bootstrap/DEPENDENCY_BUDGET.md).
* **The orchestrator** — `templates/modules/team-gated/run_security_audit.py`,
  installed verbatim as the adopter's `scripts/run_security_audit.py`. It runs
  five passes and returns one **aggregate** exit in a distinct space:
  `0` clean / `5` incomplete / `10` findings / `20` degraded, precedence
  degraded > findings > incomplete > clean.
* **The dependency leg** — the pip-audit pass, `run_pip_audit_pass` at
  `templates/modules/team-gated/run_security_audit.py:387`.
* **`_run_tool`** — the shared subprocess boundary at
  `templates/modules/team-gated/run_security_audit.py:258`, used by **both** the
  bandit and pip-audit legs. Fixing it fixes both.
* **The denominator** — the set of things a leg claims to have checked. The
  whole proposal is about who computes it. **Parent-derived**: the orchestrator
  counts distributions itself and assumes the tool saw the same ones.
  **Child-observed**: the orchestrator reads what the tool *reported* it
  enumerated. Only the second is evidence.
* **Ambient environment steering** — changing what a tool does by setting an
  environment variable rather than by passing an argument. The finding `DAC1` is
  built on: `PIPAPI_PYTHON_LOCATION` moved pip-audit's enumeration from 28
  packages to 288 without touching argv.
* **Denylist vs allowlist (of environment variables)** — a denylist strips names
  you thought of; an allowlist passes only names you chose. A denylist cannot be
  complete, and completeness is the property under test here.
* **PEP 610 / `direct_url.json`** — a file inside an installed distribution's
  metadata recording *where it came from*: a local directory (`dir_info`, with
  an `editable` flag), a version-control checkout (`vcs_info`), or an archive
  URL. The Decision uses it as the **mechanical** test for "locally built", in
  place of a human assertion.
* **Perturbation** — a deliberate change that a test is claimed to detect. This
  repository accepts a test only when its author can name a state in which it
  fails **and has run** the change producing that state. *Perturbing a test's own
  body validates the test; only perturbing the hazard validates the claim.*
* **The AST attestation baseline** —
  `bootstrap/tests/fixtures/scaffold_ast_baseline.json`, which pins a per-symbol
  digest of every `bootstrap/_scaffold/` module. Re-anchoring it is a supervised
  ceremony under [`bootstrap/REANCHOR_RUNBOOK.md`](../../bootstrap/REANCHOR_RUNBOOK.md).

## What was measured for this plan

Every figure below was taken **for this plan**, at HEAD `eacb7dd`, under the
canonical interpreter `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(Python 3.13.13), `as_of 2026-08-04`. **No repository file was modified**: the
orchestrator was loaded from its template source the way
[`bootstrap/tests/test_security_stack.py`](../../bootstrap/tests/test_security_stack.py)
already loads it (`_ORCH_SRC` at `bootstrap/tests/test_security_stack.py:535`).

The proposal's own measurements are *not* carried forward on trust; several are
re-stated below because they reproduced, and **two did not survive**, which is
why this section exists.

### The four runtime defects, reproduced at HEAD

1. **Ambient variables reach the tool.** `_IMPORT_ENV_VARS` at
   `templates/modules/team-gated/run_security_audit.py:255` strips exactly four
   names; everything else passes through. Probed with a child that dumps its own
   environment:

   ```
   CHILD_SEES: {'PIPAPI_PYTHON_LOCATION': '/some/other/python',
                'PIP_AUDIT_VULNERABILITY_SERVICE': 'osv',
                'PIP_AUDIT_OSV_URL': 'http://127.0.0.1:7777/collect',
                'HTTPS_PROXY': 'http://127.0.0.1:8888',
                'REQUESTS_CA_BUNDLE': '/tmp/evil.pem'}
   ```

   Interpreter selection, vulnerability service, endpoint, proxy and trust store
   are all ambient. This is `DAC1`, reproduced independently of the reviewer.

2. **One invalid byte crashes the pass before it can classify anything.**
   `capture_output=True, text=True` at
   `templates/modules/team-gated/run_security_audit.py:277`:

   ```
   --- invalid UTF-8 probe ---
   RAISED: UnicodeDecodeError 'utf-8' codec can't decode byte 0xff in position 0
   ```

   The exception escapes `_run_tool`. `main()` catches only `AuditDegraded`
   (`templates/modules/team-gated/run_security_audit.py:470`), so it escapes
   `main()` too: the process dies with a traceback and exit **1** — a code inside
   the *component* space the module's own exit table promises the aggregate never
   collides with.

3. **Tool output forges report lines.** A child printing
   `ESC [2K CR aggregate exit 0: CLEAN (tripwire, not proof)` was relayed
   byte-for-byte to the operator's terminal, which is the evidence for a security
   decision. This is `PS3`.

4. **No timeout, no bound.** `subprocess.run` at
   `templates/modules/team-gated/run_security_audit.py:275` passes no `timeout`
   and captures stdout/stderr without limit (`PS7`, plus `DAC6`'s second edge).

### The reporting defect, and the state of the canonical machine

pip-audit is **not installed** here — `shutil.which("pip-audit")` is `None` and
`importlib.util.find_spec("pip_audit")` is `None`. So the default run reports
INCOMPLETE citing egress and never mentions the absent tool; enabling
`--allow-network` yields DEGRADED instead of a scan. Both halves of the
proposal's Evidence reproduce.

**This binds the test design, and it is not a detail.** Cairn ships an adopter
zero runtime dependencies and `bootstrap/requirements-dev.txt` contains only
`vermin`. Every test this plan adds must therefore pass on a machine with **no
pip-audit**, which means the tests drive `_run_tool` and the classifiers with
fabricated tool output, never with the real scanner. The one thing that *does*
need the real tool — the argv and JSON schema — is fenced into Chunk 0.

### The false sentence, still false, in two places

* `bootstrap/DEPENDENCY_BUDGET.md:46` — *"pip-audit runs against its local cache
  only"*
* `templates/modules/team-gated/run_security_audit.py:392` — the same sentence

`run_pip_audit_pass` returns at the egress check
(`templates/modules/team-gated/run_security_audit.py:406`) before pip-audit is
invoked at all. Only the runtime message (*"the lookup did NOT run"*) is true.
This is `DAC7`'s second half.

### The inventory arithmetic reproduces exactly

| | as_of 2026-08-04 |
|---|---:|
| conda JSON records / unique names | 394 / **391** |
| Python distribution records / unique names | 290 / **288** |
| intersection | 244 |
| conda-only | **147** |
| Python-only | **44** |
| union | **435** |

Identical to the figures three parties reproduced on 2026-08-03. The narrowed
denominator's arithmetic is stable.

### The residual predicate, as literally worded, does not discriminate

**This is the measurement that changes the plan, and it is the reason this
section exists rather than a restatement of the proposal.**

The Decision's residual rule: *"an entry qualifies only if **locally built** — a
local path or VCS install, exposed by `direct_url.json` (PEP 610) rather than
asserted by a human."* Measured over the 290 distribution records:

```
dir_info EDITABLE:                2   (lhm-frontend, modflow_tools)
dir_info present, NOT editable: 236   (conda-forge build artifacts)
vcs_info:                         0
no direct_url.json at all:       47
```

The 236 are ordinary public packages: conda-forge builds every package from a
local build directory, and the resulting metadata records it —
`file:///home/conda/feedstock_root/build_artifacts/…` (189) and
`file:///Users/runner/miniforge3/conda-bld/…` (46). Under the rule read
literally — *installed from a local path* — **236 public packages qualify for the
residual baseline** on the canonical environment. That is precisely the drift the
rule was written to prevent (*"stops the baseline becoming a place to park public
packages the sources happen not to cover"*).

Two of the proposal's illustrative examples also fail measurement:
`modflow_tools` **is** editable, but `great-circle-calculator` is version
**1.3.1 with no `direct_url.json` at all** — an ordinary index install, and one
that has a PyPI record, so it is a `SCANNED` package, not a residual.

**The plan's disposition, flagged for the Maintainer rather than absorbed.** The
predicate is implemented as **`dir_info.editable is True`, or `vcs_info`
present** — which yields exactly the 2 distributions the Decision's own prose
describes ("editable and local project distributions"), and rejects all 236. This
is a *narrowing of a mechanical predicate in the direction the Decision's stated
purpose requires*, not a new rule; but it is an interpretive step, so it is
stated here in one place, tested by name (D4), and offered to the plan reviewer
and the Maintainer to strike in one line. **If it is struck, the honest
alternative is to ship no baseline at all in v1** and report every non-matching
distribution — not to ship the literal predicate, which is measurably vacuous.

## Scope

Executes the accepted contract across six chunks and three shipped files plus
one test file. **No file is added to any delivery registry; no adopter receives a
new file.** That is an assertion this plan verifies, not an aside — see *Install
contract*.

**In scope:**

* the shared `_run_tool` boundary (`Part 3`, strengthened by `DAC6`);
* the per-tool minimal environment and fixed argv (`DAC1`);
* reporting every blocking reason rather than the first (`Part 1`);
* the child-observed denominator, the three dispositions, and CLEAN gating on
  zero UNKNOWN (revision §2–§3);
* the residual predicate (`E2`, as narrowed above);
* quantified non-coverage at selection and at run (revision §4);
* the module-doctrine routing and the two false cache sentences (`DAC7`).

**Out of scope, fenced explicitly** (the proposal's own *Deliberately not
touched* list, plus what this plan adds):

* **Which modules a preset selects.** `default-security-stance` owns it. This
  plan does not touch `_PRESETS`, the default-on set, or any profile document.
* **Cross-language sweep composition.** `portable-security-sweeps` owns it.
* **Bandit's file reach.** `scan-coverage` owns it.
* **The onboarding prose that overclaims.** `gate-claims-vs-enforcement` owns it.
* **The aggregate exit-code space.** `{0, 5, 10, 20}` and the
  degraded > findings > incomplete > clean precedence are correct and unchanged;
  Chunk C adds a test that pins them so this fence is checkable rather than
  promised. **One state changes which tier it maps to** — see *The one
  Maintainer-visible behaviour change*.
* **Conda / native coverage.** Closed by the Maintainer's scope narrowing and
  already homed: `dev/PLANNING.md` > *Deferred follow-ups (durable home)* >
  **Security apparatus** > *Conda advisory coverage*. Nothing in this plan
  re-opens it. The run-time enumeration in D5 **counts** conda-only packages in
  order to state what was *not* audited; it never looks any of them up, and the
  report must not let the two be confused.
* **`dev/.cairn/local-env.json` and `_resolve_interpreter`.** Withdrawn by the
  revision per `DAC5`. No second reader is created; the plan adds a test (B4)
  that the orchestrator never reads that path, so the withdrawal is enforced
  rather than intended.
* **Any `bootstrap/_scaffold/` change.** None — see *Cluster accounting*.
* **A stored, integrity-covered residual baseline file.** See *Author-accounting*
  and *Lasting-truth migration*: v1 computes the residual mechanically per run,
  because a committed baseline artifact would need a delivery-registry row in
  `bootstrap/_scaffold/config.py` and would pull this scope into the config.py
  cluster it is explicitly outside.

### Documentation / doctrine surface

* **Module doctrine — yes, and named as such.** The original proposal said "No
  doctrine change"; `DAC7` showed that was false by amendment 2, and the revision
  routes the CLEAN predicate, the disposition vocabulary, and the declared-scope
  statement as **module doctrine** in
  `templates/modules/team-gated/python-security.md`. The
  `doctrine/rationale.md` rate-limit gate is **cleared, not denied**: the
  Maintainer classified this surface high-risk, which is that rule's high-risk
  limb. Recorded here because a plan that quietly ships prescription as
  description is the defect `DAC7` named.
* **Governing layer — none.** No `AGENTS.md` change, no `doctrine/` change.
* **Descriptive layer** — `bootstrap/DEPENDENCY_BUDGET.md` (Exception 1's
  network-egress contract and its blind-spot bullet).
* **Code-adjacent prose** — the module docstring and `run_pip_audit_pass`
  docstring in `templates/modules/team-gated/run_security_audit.py`, corrected in
  the same commit as the behaviour they describe, never later.
* **Release-facing** — `CHANGELOG.md > Unreleased > Fixed`, one line, written by
  the implementing agent at its serialization point.
* **Deliberation layer** — this plan, its plan review, its code review, and the
  one-line `dev/PLANNING.md` row-move that serializes the plan-open.
* **Adopter-installed files — content changes only, no new rows.** Checked, not
  assumed; the verification diffs `scaffold.py --manifest` against a pre-change
  capture and expects it empty.

<!-- cairn:slot documentation-tier-home -->
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
plan's *Scope* must name the doctrine-surface touched (or an explicit
"no doctrine surface").
<!-- cairn:end documentation-tier-home -->

## Cluster accounting — the AST ceremony, the install contract, and the seams

Five accepted scopes edit `bootstrap/_scaffold/config.py`:
`profile-parse-fail-open`, `default-security-stance`, `api-web-security-modules`,
`portable-security-sweeps`, and `security-verification-activation`. **This plan
is not one of them**, and this section is what makes that claim falsifiable
rather than asserted.

### Declared `bootstrap/_scaffold/` symbol delta — **empty**

Measured for this plan from
`bootstrap/tests/fixtures/scaffold_ast_baseline.json`, `as_of 2026-08-04`:

```
total entries: 174
by kind: Assign 53, ClassDef 10, FunctionDef 98   (= 161 of the three kinds)
         Docstring 1, Expr 1, If 1, If#2 1, Import 8, Try 1
```

**This plan's declared delta is the empty set**: it changes and adds **zero**
`FunctionDef:`, `Assign:` and `ClassDef:` entries, because it opens no file under
`bootstrap/_scaffold/`. The three shipped files it edits are template content and
a descriptive record; the fourth is a test.

Three statements follow, and each is a stop-and-explain if violated:

* **The union is formed by the Maintainer at ceremony time** from each cluster
  scope's declared delta. This scope contributes nothing to it. One shared
  ceremony covers the cluster; there is not one per scope.
* **Any engine symbol that appears in a re-anchor diff and is attributed to this
  scope is a defect in this scope**, not a widening of the union. The whole value
  of the ceremony is that "outside the union" discriminates; a scope that
  declares empty and then moves a symbol destroys that property for everyone.
* **The re-anchor is behind a Maintainer fence** (below). It is never an
  implementing agent's step, and this plan does not schedule one.

### Install contract — no movement

`AGENTS.md` calls the install contract byte-level stable and
adopter-depended-upon. **A new manifest row would be a contract change with its
own acceptance criteria; this plan adds none**, and here is why that is
structural rather than a promise:

* The only file `python-security` installs besides its doctrine is the
  orchestrator, registered at `bootstrap/_scaffold/config.py:671`. Editing that
  file's **content** moves no row.
* `python bootstrap/scaffold.py --manifest` emits **95 data rows** (96 lines
  including the header), `as_of 2026-08-04`. Expected diff after every chunk:
  **empty**.
* The gate manifest's `mapping_symbols` digests must not move:
  `_CORE_MAPPINGS c74e6013783bf4fe`, `_MODULE_MAPPINGS 26957a8924042a0a`,
  `_SKILLS_MAPPINGS 8ec105a84b5e65bf`, `as_of 2026-08-04`.
* **This is what the deferred residual-baseline artifact would have cost.** A
  committed baseline file would need an `InstallSpec` in `_MODULE_MAPPINGS`, a
  manifest row, a lockfile entry, an `_MODULE_APPARATUS` entry in the
  orchestrator (`templates/modules/team-gated/run_security_audit.py:94`) so the
  SR-1 preflight covers it — and a `config.py` symbol delta that would make this
  a sixth cluster scope. That is the reason v1 computes the residual per run.

### Gate accounting

* **Two touched files are gate-manifest frozen**, out of a 164-entry
  `frozen_files` map, `as_of 2026-08-04`:
  `templates/modules/team-gated/run_security_audit.py` (pinned
  `04cedaa2cd133fca3042c99f1c25daefd268744273c878b403c31435a60d1f6f`) and
  `bootstrap/tests/test_security_stack.py`. `test_gate_manifest.py:69` asserts
  the orchestrator is in that map, so the freeze is itself pinned.
  `templates/modules/team-gated/python-security.md` and
  `bootstrap/DEPENDENCY_BUDGET.md` are **not** frozen — checked, not assumed.
* **`FROZEN-NEW`: zero.** This plan creates no file.
* **`COLLECTION-ADDED` rows are expected** for every new test node, and at least
  one **modified existing assertion** (C2 re-expresses
  `test_pip_audit_egress_off_is_incomplete_not_clean` at
  `bootstrap/tests/test_security_stack.py:630`). Renames, if any, register as a
  drop plus an add; the manifest has no rename concept.
* **`SKIP-XFAIL-NEW`: avoid where possible.** `TestOrchestrator` carries a
  class-level `skipif(not _HAS_GIT)`. Pure-unit tests for `_run_tool`, the env
  builder, the argv builder and the classifiers **go at module level, outside
  that class** — they need no git and no adopter tree, so they add no skip row
  and run everywhere.
* **Bandit budget.** The orchestrator is in the release scan set. Measured today
  over that one file: `errors: []`, `{('LOW','B404'): 1, ('LOW','B603'): 1}`,
  **zero MEDIUM-or-higher**. Chunk A adds process handling, so the post-change
  measurement must be re-taken; the acceptance bar is **still zero MEDIUM+**, and
  any new LOW is recorded in the commit body rather than allowlisted silently.
* **The re-pin is not this plan's act.** After the last chunk,
  `_gate_manifest.py verify` will report `FROZEN-MODIFIED` for the two frozen
  files plus the collection rows. The implementing agent's obligation is to run
  it, **split attributable from non-attributable rows** (the tree carries other
  scopes' work — `git status --short` at plan-open already shows modifications
  under `bootstrap/_scaffold/` from concurrent workflows), and record the split
  in the final commit body. Re-pinning is supervised under
  [`bootstrap/REANCHOR_RUNBOOK.md`](../../bootstrap/REANCHOR_RUNBOOK.md).

### Shared-file seams — named, with the paragraph each scope owns

The proposal verified zero hits for `pip-audit`/`pip_audit` across in-flight
proposals and plans; re-checked for this plan and still true. The seams are on
*files*, not on the pip-audit leg.

| File | Also claimed by | The seam |
|---|---|---|
| `templates/modules/team-gated/python-security.md` | `default-security-stance` | That scope rewrites the **"Selected when:" / team-gated-and-opt-in** sentence at `templates/modules/team-gated/python-security.md:3`. This plan edits the **v1-scope block** (`:13`) and the **pip-audit egress section** (`:104`) and adds a coverage-contract subsection. **Paragraph-disjoint by construction** — this plan does not touch the "Selected when" line. |
| `bootstrap/DEPENDENCY_BUDGET.md` | `api-web-security-modules`, `portable-security-sweeps`, `gate-claims-vs-enforcement` | This plan owns the **Exception 1 network-egress contract** (`:44`–`:53`). `gate-claims-vs-enforcement` claims **line 101** (the `vermin` CI sentence) — verified from its own chunk table, a different section. The other two add **new exception sections**. File-level overlap, line-level disjoint. |
| `templates/modules/team-gated/run_security_audit.py` | `portable-security-sweeps` (reads `_run_tool`; its *Deliberately not touched* line disclaims "the existing `python-security` exit contract, Bandit and pip-audit policy") | **This plan claims `_run_tool` and rewrites it.** If that scope's adapter work turns out to modify rather than reuse the boundary, the two must re-coordinate before either lands. |
| `bootstrap/tests/test_security_stack.py` | `api-web-security-modules`, `portable-security-sweeps` (both say "behavioral tests under `bootstrap/tests/`") | A shared `FROZEN-MODIFIED` row. Attribution must be split at re-pin; do not re-pin from a raw violation count. |

### What is true regardless of intra-cluster order

* **Order-independent**: the symbol delta (empty), the install contract (no
  movement), the preset table (untouched), and every behaviour this plan
  changes. Nothing here depends on which cluster scope lands first.
* **Order-sensitive, and the response is the same in each case — re-read, do not
  apply from this plan's text**:
  * **Line citations move.** Every `path:line` in this plan is `as_of
    2026-08-04`. Verify by **content**, not by line number, at implementation.
  * **`python-security.md`'s opening lines** shift if `default-security-stance`
    lands first.
  * **The suite collection baseline** (1746 collected, `as_of 2026-08-04`,
    against a tree already carrying concurrent work) moves with any sibling.
  * **The gate-manifest violation count** grows with every sibling; only the
    attributable split is usable.

## Sequence

Chunk order is load-bearing. **Chunk A lands first** because every later chunk's
evidence arrives through `_run_tool`: until the decode crash is closed, a test
that feeds a child hostile bytes dies with a traceback instead of producing a
verdict, and until output is bounded and escaped, nothing read back from a tool
is trustworthy evidence.

```
0. plan-open   -- this plan + the dev/PLANNING.md row-move            [commit pending]
   (plan review) -- required(External, security lens); NO code before it lands
1. Chunk 0 -- establish pip-audit's argv + JSON schema by execution   [commit pending]
2. Chunk A -- the shared runner boundary: timeout, bytes, bound, escape [commit pending]
3. Chunk B -- per-tool minimal environment + fixed argv (DAC1)        [commit pending]
4. Chunk C -- report every blocking reason, tier by precedence        [commit pending]
5. Chunk D -- child-observed denominator, dispositions, CLEAN gating  [commit pending]
6. Chunk E -- selection-time coverage contract + the two false claims [commit pending]
```

**Dependencies, stated so a reviewer can check the order rather than take it:**
D depends on A (bounded, decoded bytes) and on Chunk 0 (the real schema); B and C
are independent of each other; E depends on nothing but is last so its prose
describes shipped behaviour rather than intended behaviour.

---

### Chunk 0 — establish the tool contract by execution, before pinning anything

The proposal refused to assert a tool capability it had not executed, and the
Decision inherited that discipline. **Chunk 0 changes no repository file**: it
produces a measurement, recorded as an append-only evidence sub-section of this
plan, and the pinned pip-audit version.

**Maintainer fence — this chunk needs network egress.** pip-audit is not
installed and Cairn must not install it into the canonical environment (Exception
1 is an *adopter* dependency; `bootstrap/requirements-dev.txt` carries only
`vermin`). The measurement therefore requires creating a **throwaway virtual
environment outside the repository** (the Codex reviewer used `/private/tmp`) and
`pip install pip-audit` into it — a network fetch from a public index. **The
implementing agent asks first and does not proceed on this plan's say-so.** If
the Maintainer declines, Chunk 0 has a fallback, below.

| # | Deliverable | Content |
|---|---|---|
| 0a | pinned version | the exact pip-audit version measured, recorded by name. The reviewer measured 2.10.0; do not assume it is still current. |
| 0b | argv inventory | which of `--format`, `--output`, `--vulnerability-service`, `--cache-dir`, `--strict`, `--progress-spinner`, `--no-deps`, `--local`, `--dry-run` exist in that version, with `--help` output quoted. **Every flag named in Chunk B is unverified until this lands.** |
| 0c | JSON schema | the actual shape of `--format json` output: the key holding enumerated distributions, the key holding vulnerabilities per distribution, and **whether a skipped/unresolved set is exposed at all**. Chunk D's UNKNOWN count depends entirely on 0c. |
| 0d | ambient re-confirmation | that `PIPAPI_PYTHON_LOCATION` still redirects enumeration in the pinned version, and that `PIP_AUDIT_*` still parse as configuration. If a later version closed these, Chunk B's tests stay (a boundary should not depend on the tool's good behaviour) but the *finding* is downgraded and the plan says so. |

**Acceptance criteria — Chunk 0.**

* The evidence sub-section is appended to this plan (append-only; do not edit
  prior sections) and committed as a deliberation-layer commit.
* Every command is quoted with its output. A flag asserted without `--help`
  output behind it is exactly the error the proposal was written to avoid.
* **The fallback, pre-decided so it is not improvised.** If the Maintainer
  declines the network install, or if 0c shows the pinned version exposes **no**
  unresolved/skipped set: the dependency leg **cannot establish zero UNKNOWN**,
  so it reports UNKNOWN-unestablished and contributes **INCOMPLETE (5)**, never
  CLEAN. That is the fail-closed default and it is a shippable outcome — Chunks
  A, B, C and E still land in full, and Chunk D ships the classifier plus the
  gate with the "cannot establish" path as the live one. The plan does **not**
  guess a schema in order to reach CLEAN.

---

### Chunk A — the shared runner boundary

Part 3, strengthened by `DAC6`. Both legs benefit; `PS7` was split out of
`portable-security-sweeps` for exactly this reason.

| # | File | Change |
|---|---|---|
| A1 | `templates/modules/team-gated/run_security_audit.py` | `_run_tool` gains a **timeout** (module constant; not environment-configurable — the environment is the attack surface this plan is closing). `subprocess.TimeoutExpired` → terminate, then kill, then return a `"timeout"` status the callers map to **DEGRADED**. A timeout is never clean. |
| A2 | (same file) | **Capture bytes, not text.** Drop `text=True`; decode with an explicit error policy (`errors="replace"`) at render time only. A decode that needed replacement is recorded and maps to **DEGRADED** for the pass, because output that could not be read is output that cannot be parsed. |
| A3 | (same file) | **Bound the combined output** at a module constant. Exceeding it terminates the child and returns a `"truncated"` status mapped to **DEGRADED**. Honest limit, stated in the docstring: this bounds the *parent's memory*, not the child's disk. |
| A4 | (same file) | **Escape control characters before rendering.** Render tool output through an escaper that neutralises `ESC`, `CR`, and other C0/C1 controls (keeping `\n` and `\t`), so a crafted filename cannot forge a report line. Text is otherwise verbatim, per the proposal's own recovery note ("sanitize only control characters and keep the text verbatim"). |
| A5 | (same file) | **Descendant cleanup.** Start the child in its own process group (`start_new_session=True` on POSIX) and kill the group on timeout / truncation. A cleanup failure is DEGRADED, not silent. Windows is a **named residual**, not a claim. |
| A6 | `bootstrap/tests/test_security_stack.py` | Module-level tests (outside the git-gated `TestOrchestrator` class) for A1–A5 — see the perturbation table below. |
| A7 | (same file, docstring) | `_run_tool`'s docstring gains the four new guarantees and the two named residuals. Same commit as the behaviour. |

**Acceptance criteria — Chunk A.**

* `python -m pytest bootstrap/tests/test_security_stack.py -q` → all pass.
* Bandit over the edited orchestrator: **zero MEDIUM+**, `errors: []`. Any new
  LOW is named in the commit body against the 2-LOW baseline measured above.
* **Perturbations, each RUN, ledger in the commit body.** Every row perturbs the
  **hazard**, not the test body.

| Test | Hazard perturbation | Expected failure |
|---|---|---|
| A-t1 timeout classification | make the `TimeoutExpired` branch return the clean status instead of `"timeout"` | red: tier is CLEAN where DEGRADED is asserted |
| A-t2 timeout exists at all | delete the `timeout=` argument | the test **hangs** — recorded honestly as a hang, since an unbounded wait *is* the defect being closed |
| A-t3 invalid UTF-8 | restore `text=True` | red with `UnicodeDecodeError`. **Already red at HEAD today** — measured above, so the future state in which this test fails is the present one |
| A-t4 output bound | remove the cap (leave the constant in place, remove its enforcement) | red: status is `"ran"` and the captured length exceeds the cap |
| A-t5 control escaping | remove the escaper call | red: raw `ESC`/`CR` present in rendered output. **Already red at HEAD today** |
| A-t6 descendant cleanup | remove `start_new_session` / the group kill | red: the grandchild outlives the timeout |

* **A note on A-t4's constant.** The test monkeypatches the cap *down* so the
  child writes a kilobyte rather than megabytes. That is configuring the
  **subject**; the oracle is the returned status and the measured buffer length,
  neither of which the subject supplies.
* **Channel note.** Subject: `_run_tool`. Oracles: a separate child process's
  behaviour (A-t1, A-t2, A-t6), raw bytes the test itself authors (A-t3, A-t4,
  A-t5). No oracle is derived from the code under test.

---

### Chunk B — the per-tool minimal environment and fixed argv

`DAC1`, the finding the Decision calls load-bearing rather than cosmetic: *a
narrowed claim over an ambient environment is exactly as false as the wide one*.

| # | File | Change |
|---|---|---|
| B1 | `templates/modules/team-gated/run_security_audit.py` | Replace the denylist at `templates/modules/team-gated/run_security_audit.py:255` with a **closed allowlist** child environment: only variables the plan names pass through (`PATH`, `HOME`, `TMPDIR`/`TEMP`, `LANG`/`LC_*`, and on Windows the minimum the interpreter needs). Everything else — `PIPAPI_PYTHON_LOCATION`, every `PIP_AUDIT_*`, `*_PROXY`, `REQUESTS_CA_BUNDLE`, `SSL_CERT_FILE`, `PIP_*` — is dropped. Keep the existing `-I` isolation; the allowlist is belt to its braces. |
| B2 | (same file) | **Explicit, printed, risk-accepted pass-through.** If an adopter genuinely needs a proxy or custom trust store, it is passed through only by an explicit opt-in, and the report **prints the name of every variable passed through**. Inheritance is never silent. |
| B3 | (same file) | **Fixed argv** for the pip-audit pass, pinning (per Chunk 0's measured flag inventory) the vulnerability service, the output format, the output destination (stdout, never a path from the environment), the cache disposition, progress, and strictness. `--allow-network` authorizes the **documented** service, not an ambient one. |
| B4 | (same file) | The report records `sys.executable` and its version as **observations**, with no assertion of equivalence to any project record. `dev/.cairn/local-env.json` is not read and `_resolve_interpreter` is not duplicated (`DAC5`). |
| B5 | `bootstrap/tests/test_security_stack.py` | Module-level tests B-t1…B-t5 below. |

**Acceptance criteria — Chunk B.**

* `python -m pytest bootstrap/tests/test_security_stack.py -q` → all pass.
* **Perturbations, each RUN.**

| Test | What it asserts | Hazard perturbation | Expected failure |
|---|---|---|---|
| B-t1 known steering vars | with all five ambient names set, a probe child sees none of them | restore the four-name denylist | red, naming the leaked variables. **Already red at HEAD today** — measured above |
| B-t2 the allowlist is closed | a **novel** name (`PIP_AUDIT_FUTURE_KNOB`) the code has never heard of is also absent | implement B1 as a denylist of the *known* names | **B-t1 green, B-t2 red.** That pair is the entire argument for the allowlist shape; a reviewer should reproduce it first |
| B-t3 fixed argv | the built argv carries each pinned flag and **no element derived from `os.environ`** | drop one pinned flag | red, naming the missing flag |
| B-t4 pass-through is printed | an opted-in pass-through variable appears by name in the report | make the pass-through silent | red |
| B-t5 no trust-root read | the module source contains no reference to `local-env` and opens no such path during a pass | add a read of `dev/.cairn/local-env.json` | red. This enforces `DAC5`'s withdrawal rather than trusting it |

* **Channel note.** B-t1/B-t2's oracle is a child process's own view of its
  environment — a different process from the one that built it. B-t3's oracle is
  a list of literals typed into the test. Neither derives from the builder.
* **Named residual.** A closed allowlist can break a tool that legitimately needs
  an unlisted variable (a corporate trust store is the realistic case). B2 is the
  release valve, and the failure mode is loud (the tool errors → DEGRADED), not
  silent. Stated here rather than discovered by an adopter.

---

### Chunk C — every blocking reason, and the tier the documented table already specifies

| # | File | Change |
|---|---|---|
| C1 | `templates/modules/team-gated/run_security_audit.py` | `run_pip_audit_pass` stops returning at the first blocker. It evaluates **tool availability**, **egress disposition** and **interpreter observation** independently, prints all three dispositions, and *then* returns. The early `return` at `templates/modules/team-gated/run_security_audit.py:406` goes. |
| C2 | (same file) | The tier is the **worst applicable** reason, using the module's own documented precedence. Tool-absent is DEGRADED per the shipped exit table (*"a required tool was absent"*); egress-off is INCOMPLETE. Both true → **DEGRADED**. |
| C3 | (same file, docstring) | `run_pip_audit_pass`'s docstring loses *"pip-audit runs against its local cache only"* (`templates/modules/team-gated/run_security_audit.py:392`) — verified false — in favour of "does not run", matching the runtime message. Lands here, with the behaviour, **not** in Chunk E. |
| C4 | `bootstrap/tests/test_security_stack.py` | C-t1…C-t4 below, including the re-expression of the existing test at `bootstrap/tests/test_security_stack.py:630`. |

**The one Maintainer-visible behaviour change, stated plainly.** On a machine
where pip-audit is **absent** — which includes this repository's canonical
environment today — the default `run_security_audit.py` aggregate moves from
**5 (INCOMPLETE)** to **20 (DEGRADED)**. The plan's position: this is not a
change to the exit table but **conformance to it**, since the shipped table
already assigns "a required tool was absent" to `20`; the current code simply
never reaches that branch when egress is off, which is the reporting defect the
proposal opens with. It is nonetheless a live behaviour change for adopters, it
is flagged rather than buried, and it is strikeable in one line — if struck, C1
still lands (both reasons printed) and only C2's tier arithmetic reverts.

**Acceptance criteria — Chunk C.**

| Test | What it asserts | Hazard perturbation | Expected failure |
|---|---|---|---|
| C-t1 both reasons | with egress off **and** the tool absent, the output names both, and the status carries both | restore the early `return` on egress | red: only one reason present |
| C-t2 egress-off alone | egress off with the tool forced present → **INCOMPLETE**, unchanged | make tool-absence dominate unconditionally | red. This is the re-expression of the existing frozen test, and it preserves the contract that test was written for |
| C-t3 tool-absent dominates | egress off **and** tool absent → DEGRADED | take the first reason rather than the worst | red: tier is 5 |
| C-t4 the space is unchanged | `{_AGG_CLEAN, _AGG_INCOMPLETE, _AGG_FINDINGS, _AGG_DEGRADED} == {0, 5, 10, 20}` and the aggregate is still `max(...)` | change any constant | red. A cheap tripwire that makes the "aggregate space untouched" fence checkable rather than promised |

* **Channel note.** The oracles are literal tier constants and captured output
  text; the subject is the pass function. C-t2 forces tool-presence by
  monkeypatching `shutil.which` — the idiom already in use at
  `bootstrap/tests/test_security_stack.py:638` — so the test is deterministic on
  a machine with or without pip-audit.

---

### Chunk D — the child-observed denominator, three dispositions, and CLEAN gating

The substance of the accepted contract. **Every design element here is
conditional on Chunk 0's measured schema**; where 0c comes back empty, the
fail-closed fallback in Chunk 0's acceptance criteria is what ships.

| # | File | Change |
|---|---|---|
| D1 | `templates/modules/team-gated/run_security_audit.py` | Parse pip-audit's **pinned JSON** rather than prose. The denominator is the distribution set **the child reported**; the orchestrator does not count distributions itself and assume the child saw the same ones. A parse failure, a truncation, a decode replacement or a timeout → the enumeration is **not established** → UNKNOWN → INCOMPLETE (or DEGRADED where Chunk A classified the failure as such). |
| D2 | (same file) | Classify every reported distribution into **SCANNED**, **NO-MATCH-IN-PINNED-SOURCES** (naming every source and version queried; *accepted non-coverage, not evidence of safety*), or **UNKNOWN**. Print the three counts. |
| D3 | (same file) | **CLEAN requires zero UNKNOWN.** Findings still dominate; degraded still dominates both. The NO-MATCH count is reported alongside CLEAN, never folded into it. |
| D4 | (same file) | The residual predicate: a distribution qualifies as locally built iff its `direct_url.json` carries `dir_info` with `editable` true, **or** carries `vcs_info`. A non-editable local path (the conda-forge build-artifact shape) and a distribution with no `direct_url.json` do **not** qualify. See *What was measured* for why the literal wording fails. |
| D5 | (same file) | **Quantified non-coverage in the report.** When the interpreter's prefix has a `conda-meta` directory, enumerate it and report the count of conda-only names — what the module did **not** audit — as a number, not a caveat. This is *enumeration for reporting*; the report must state that these packages were **not looked up**, so a count can never be read as coverage. On a non-conda environment the scope statement prints without a count. |
| D6 | `bootstrap/tests/test_security_stack.py` | D-t1…D-t6 below, driven by fixtures captured in Chunk 0 — no live pip-audit required. |

**Acceptance criteria — Chunk D.**

| Test | What it asserts | Hazard perturbation | Expected failure |
|---|---|---|---|
| D-t1 skipped ≠ scanned | a distribution the tool reported as skipped classifies UNKNOWN or NO-MATCH, never SCANNED | classify skipped entries as SCANNED | red: the UNKNOWN count drops to zero and CLEAN becomes reachable — the exact hazard |
| **D-t2 CLEAN gating** | one UNKNOWN, zero vulnerabilities → **INCOMPLETE**, not CLEAN | remove the zero-UNKNOWN gate | red: returns CLEAN. **This is the central claim of the proposal; reproduce it first** |
| D-t3 malformed output | non-JSON / truncated / decode-replaced output → never CLEAN | fall back to "assume clean on parse failure" | red |
| D-t4 residual predicate | editable → qualifies; **non-editable local dir → does not**; no `direct_url.json` → does not | implement the predicate as "any `dir_info` present" (the literal Decision wording) | red on the conda-forge-shaped case. This test **encodes today's 236-record measurement** and is the one that would have caught the over-qualification |
| D-t5 non-coverage count | with a synthetic prefix whose `conda-meta` holds 3 records, 1 also a Python distribution, the report names **2** out of scope | report the raw conda count instead of the set difference | red: 3 |
| D-t6 denominator provenance | the reported denominator equals the child's reported set, not a parent-side enumeration | compute the denominator from `importlib.metadata` in the parent | red where the two differ — which the fixture makes them do by construction |

* **The independence D-t6 buys, and its honest limit.** The residual predicate
  (D4) and the non-coverage count (D5) *are* parent-side reads. They are
  legitimate only because Chunk B pins the child to the parent's interpreter; if
  that pin were removed, both would silently describe a different environment.
  **Named as a coupling, not hidden**: B-t1/B-t2 are what keep it true, and
  D4/D5's docstrings must say so.
* **Channel note.** Subject: the classifier and the pass. Oracle: JSON fixtures
  captured from a different program in Chunk 0, plus synthetic metadata trees the
  test authors. Neither is derived from the code under test.

---

### Chunk E — the contract an adopter reads before installing

| # | File | Change |
|---|---|---|
| E1 | `templates/modules/team-gated/python-security.md` | A **declared-scope** statement in the v1-scope block (`templates/modules/team-gated/python-security.md:13`): the module audits **Python distributions discoverable in the audited environment**, and does not audit conda-managed native packages, system packages, or vendored / statically-linked libraries. Stated where an adopter decides, not in a report they read after they already trust it. |
| E2 | (same file) | A **coverage-contract** subsection under the pip-audit section (`templates/modules/team-gated/python-security.md:104`): the three dispositions, that **CLEAN requires zero UNKNOWN**, and that NO-MATCH-IN-PINNED-SOURCES is accepted non-coverage rather than evidence of safety. Routed explicitly as **module doctrine** per `DAC7`, with the rate-limit basis recorded — the Maintainer classified this surface high-risk, which is `doctrine/rationale.md`'s high-risk limb. |
| E3 | (same file) | The *"conda-managed and locked-but-not-installed dependencies are documented blind spots"* sentence gains the measured figure: **147 conda-only packages, 82 of them native, `as_of 2026-08-03`** on the canonical environment, and the pointer that this gap is homed in `dev/PLANNING.md` rather than closed here. |
| E4 | `bootstrap/DEPENDENCY_BUDGET.md` | `bootstrap/DEPENDENCY_BUDGET.md:46` — *"pip-audit runs against its local cache only"* → **"does not run"**, matching the runtime message and the verified behaviour. |
| E5 | (same file) | The *Scope / blind spots* bullet gains the same measured figure and `as_of`, replacing "documented blind spots" — which reads as an edge case and is 38% of the packages. |
| E6 | (docstring) | **Not here** — the orchestrator docstring correction landed in Chunk C3, with the behaviour it describes. Listed so its absence is deliberate rather than an omission. |
| E7 | `CHANGELOG.md > Unreleased > Fixed` | One line, written by the implementing agent at its serialization point: the dependency leg now reports every blocking reason, binds its denominator to what the tool enumerated, gates CLEAN on zero UNKNOWN, and the shared runner boundary gained a timeout, bounded byte capture and control-character escaping. Cross-reference proposal and plan **by stem**, per `AGENTS.md > Shared communication files`. |

**Acceptance criteria — Chunk E.**

* `python scripts/check_cairn.py` → OK. **180 Markdown files, 68 external links
  not probed**, `as_of 2026-08-04`; the count may only grow.
* `python scripts/claim_check.py <file>` over each edited Markdown file, **one
  file per invocation** — the checker takes a single path and exits 2 on more.
* `python scripts/quality_gate.py --sub neutrality` → unchanged. Re-measure the
  baseline immediately before editing rather than quoting a figure; three other
  scopes are editing files inside its scan roots.
* **Verify every quoted sentence before editing.** E1–E3 and E4–E5 quote lines in
  files three other scopes claim. Re-read `python-security.md` and
  `DEPENDENCY_BUDGET.md` at implementation time and match on **content**; do not
  apply from this plan's line numbers.
* **Channel note.** The claim is that the prose now matches the code. The
  evidence is a reading of the edited code plus a live run, **not** a reading of
  the prose that was just written. `check_cairn` verifies link and claim-path
  integrity, never whether a sentence is true — it catches drift, not absence,
  and this plan does not lean on it for E.

## Acceptance criteria

Per-chunk criteria are above; these are the plan-level deliverables.

* **Tests that must pass.**
  * `python -m pytest bootstrap/tests` — the whole suite, green, **0 failed / 0
    skipped / 0 xfailed**, under the canonical interpreter (3.13.13). Baseline
    **1746 collected**, `as_of 2026-08-04`, measured against a tree already
    carrying concurrent cluster work — **re-take it at implementation rather than
    quoting this figure**. Collection grows by exactly the new nodes and drops
    none.
  * [`bootstrap/tests/test_security_stack.py`](../../bootstrap/tests/test_security_stack.py)
    — the boundary tests (A-t1…A-t6), the environment and argv tests
    (B-t1…B-t5), the reason-reporting tests (C-t1…C-t4), and the denominator /
    disposition tests (D-t1…D-t6).
  * [`bootstrap/tests/test_gate_manifest.py`](../../bootstrap/tests/test_gate_manifest.py)
    — unchanged and green; it asserts the orchestrator stays in the frozen map.
  * [`bootstrap/tests/test_lockfile_provenance.py`](../../bootstrap/tests/test_lockfile_provenance.py)
    — unchanged and green. It loads the **same** orchestrator source
    (`bootstrap/tests/test_lockfile_provenance.py:254`) to prove the shipped
    lockfile reader tolerates provenance fields; this plan must not break that
    reader.
  * **Every new test shown non-vacuous by a RUN perturbation of the hazard**,
    with the ledger — the change made, the failure observed, the byte-identical
    restore verified against `git rev-parse HEAD:<path>` — in the commit body.
    Where a test cannot be made to fail by an assertion (A-t2's hang), the plan
    says so instead of claiming otherwise.
* **Doc updates that must land.** All hand-authored:
  `templates/modules/team-gated/python-security.md` (three edits),
  `bootstrap/DEPENDENCY_BUDGET.md` (two), the two docstrings inside
  `templates/modules/team-gated/run_security_audit.py`, and
  `CHANGELOG.md > Unreleased > Fixed`. No generated docs, no snippet-synced
  blocks.
* **Examples / smoke checks required.** `python bootstrap/scaffold.py --manifest`
  — expected **unchanged at 95 data rows**, which is itself the assertion that
  this plan installs nothing new into an adopter tree. **N/A**: the runnable
  example gallery — this change touches nothing it demonstrates. **N/A**: an
  end-to-end real-pip-audit run — the tool is not installed and Cairn must not
  install it; Chunk 0's throwaway environment is the only place the real tool is
  executed.
* **Inbound path-link updates.** None expected. `dev/PLANNING.md` and
  `dev/NEXT_SESSION.md` refer to plans by filename stem, not path link, so the
  archive-move needs no edit there. Confirm at archive time rather than assume.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants, each with the chunk that enforces it.**
  * *No environment variable reaches a security tool unless this code named it.*
    Enforced by B-t1 **and** B-t2 in
    [`bootstrap/tests/test_security_stack.py`](../../bootstrap/tests/test_security_stack.py);
    B-t2 alone discriminates allowlist from denylist.
  * *A leg never returns CLEAN with a non-zero UNKNOWN count.* Enforced by D-t2.
    This is the accepted contract's core and the first thing a reviewer should
    attack.
  * *The denominator is the child's, not the parent's.* Enforced by D-t6, and
    **coupled** to B-t1/B-t2 — stated as a coupling above rather than presented
    as independent.
  * *Tool output cannot forge a report line.* Enforced by A-t5.
  * *A tool that hangs, floods, or emits undecodable bytes is DEGRADED, never
    clean.* Enforced by A-t1, A-t4, A-t3.
  * *The aggregate space `{0,5,10,20}` and its precedence are unchanged.*
    Enforced by C-t4.
  * *The install contract does not move.* Enforced by the `--manifest` diff
    against a pre-change capture, plus the three `mapping_symbols` digests.
  * *No `bootstrap/_scaffold/` symbol changes.* Enforced by **the empty declared
    delta plus `git status --short`** — and **not by any test**. This is the
    claim a reviewer should attack; the mitigation is that the plan opens no file
    in that package, which is checkable by reading the diff.
* **Public-path → test mapping.** `_run_tool` and `run_pip_audit_pass` are the
  two public entry points this plan changes, and both are exercised through their
  public paths — not via stubs of themselves — by
  [`bootstrap/tests/test_security_stack.py`](../../bootstrap/tests/test_security_stack.py).
  Where a test monkeypatches `shutil.which` or feeds a JSON fixture, the stub is
  the **input**, never the oracle.
* **Failure modes.**
  * Tool absent, egress off → **both reported**, DEGRADED (C).
  * Tool hangs → **closed** by A1, DEGRADED.
  * Tool floods stdout → **closed for memory** by A3; **open for the child's
    disk**, named residual.
  * Tool emits invalid UTF-8 → **closed** by A2. Today it is an uncaught
    traceback exiting 1.
  * Tool output contains terminal control sequences → **closed** by A4.
  * Grandchild outlives the timeout → **closed on POSIX** by A5; **open on
    Windows**, named residual.
  * Ambient variable redirects interpreter / service / endpoint / output →
    **closed** by B1, pinned by B-t1/B-t2.
  * A future tool honours a variable nobody has heard of → **closed by the
    allowlist shape**, which is why B-t2 exists.
  * Pinned JSON schema changes in a later tool version → **fails closed**: parse
    failure → UNKNOWN → not CLEAN (D-t3). Loud, not silent.
  * A public package with no advisory record → **NO-MATCH-IN-PINNED-SOURCES**,
    reported, and it does **not** qualify for the residual (D-t4).
  * Conda-only native packages → **outside the declared scope**, counted and
    named in the report (D5), homed in `dev/PLANNING.md`. Not closed, and the
    plan says so where the module says so.
* **Edge cases handled.** A non-conda environment (D5 prints no count). A
  distribution appearing in both inventories with divergent versions — outside
  the narrowed denominator, since only the child's Python-distribution report is
  the denominator. An adopter needing a proxy (B2). A machine with no pip-audit
  (every test still runs). A machine with no git (the new tests sit outside the
  git-gated class).
* **Known omissions, stated rather than implied.** (a) No live pip-audit run
  against the canonical environment; the tool is absent and Cairn will not
  install it. (b) Windows is untested for A5 and for B1's allowlist minimum. (c)
  The residual predicate narrowing is an **interpretive** step on the Decision's
  wording, flagged above and strikeable. (d) No stored, integrity-covered
  residual baseline ships in v1, so there is no in-apparatus run-over-run diff —
  the diff is the operator's, comparing two reports. (e) The parent-side reads in
  D4/D5 are coupled to Chunk B's interpreter pin. (f) Whether the DEGRADED tier
  change in Chunk C is desirable is a Maintainer call this plan raises and flags
  rather than settles.

## Verification

Run under the canonical interpreter
(`/Users/kendal30/conda_envs/lhm/bin/python3.13`, 3.13.13); a different minor
silently changes the suite figure and the AST digests.

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

* **The release Bandit budget** — `python bootstrap/security_check.py` → `PASS`.
  Plus a scoped re-measure over the edited orchestrator alone; baseline
  `errors: []`, 2 LOW (`B404`, `B603`), **zero MEDIUM+**, `as_of 2026-08-04`.
  Zero MEDIUM+ is the bar; new LOWs are recorded, not allowlisted.
* **The install-contract assertion** — `python bootstrap/scaffold.py --manifest`
  diffed against a capture taken at the plan-open commit. **Expected empty**, 95
  data rows.
* **The engine-untouched assertion** — `git status --short bootstrap/_scaffold/`
  attributable to this plan is **empty** at every commit. Any entry is a
  stop-and-explain, not a re-scoped delta.
* **The gate-integrity split** —
  `python bootstrap/tests/_gate_manifest.py verify` after the last chunk. Record
  in the commit body which violations are **attributable to this plan** (the two
  frozen files plus its own collection rows) and which are concurrent cluster
  work. **Do not re-pin.**
* **The perturbation ledgers** — per chunk, in the commit body: the change made,
  the failure observed with its message, and the byte-identical restore verified
  with `git hash-object` against `git rev-parse HEAD:<path>`.

### Maintainer fences — three, none of them an implementing agent's step

1. **The AST attestation re-anchor ceremony.** This plan declares an **empty**
   symbol delta and schedules no re-anchor. It shares one ceremony with the
   config.py cluster, and **the union is formed by the Maintainer at ceremony
   time from each scope's declared delta**. An implementing agent never
   re-anchors, never edits
   `bootstrap/tests/fixtures/scaffold_ast_baseline.json`, and never edits
   [`bootstrap/REANCHOR_RUNBOOK.md`](../../bootstrap/REANCHOR_RUNBOOK.md).
2. **The gate-manifest re-pin.** Two frozen files go stale. Re-pinning is
   supervised under the same runbook. The implementing agent's obligation is to
   report the stale entries and their attribution split, nothing more.
3. **Chunk 0's network fetch.** Measuring pip-audit's real argv and JSON schema
   needs a throwaway virtual environment outside the repository and a package
   install from a public index. **Ask before doing it.** No credential or key is
   involved anywhere in this plan; if any step appears to need one, that is a
   signal the plan has drifted, and it stops.

## Plan review — the brief

*Required — **External**, security lens. Implementation does not start until a
review has landed under this heading as a `### Plan review -- <reviewer> --
YYYY-MM-DD` sub-heading.*

**The tier is declared, not chosen, and an Internal round does not discharge
it.** Two independent triggers: the proposal's Decision routes
`required(External, security lens)` to the plan in its own right, and `AGENTS.md`
> *High-risk surfaces* names the shipped security stack. Internal review's floor
is the same agent in a fresh session; External's floor is a different agent type
or a human. A same-type read cannot satisfy a cross-type requirement, so **an
Internal round is welcome and is not a substitute** — the plan-review precondition
stays unmet until an External security round lands.

Nor is it discharged by the proposal's two External rounds. Those read the
*proposal*. This plan makes three moves no reviewer has seen:

**The three questions this review should aim at, in descending weight:**

1. **Is the residual predicate narrowing right, and is D-t4 the test that proves
   it?** Reproduce the measurement: on the canonical environment, 236
   distributions carry a non-editable `dir_info` from a conda-forge build
   directory, and only 2 are editable. Then decide whether implementing
   `editable-or-vcs` is faithful execution of the Decision or a redesign of it.
   **If it is a redesign, say so and strike it** — the fallback is to ship no
   baseline in v1, not to ship the literal predicate.
2. **Does D-t2 actually gate CLEAN, and does the denominator survive Chunk B's
   removal?** Attack the coupling: delete B1's allowlist and check whether any
   test goes red other than B-t1/B-t2. If the denominator can be silently
   redirected while D's tests stay green, the plan's central independence claim
   is weaker than stated.
3. **Is the Chunk C tier change (5 → 20 on a tool-absent machine) conformance to
   the documented exit table, or a change to it?** The plan argues conformance.
   It is a live behaviour change for adopters either way, and it is offered for
   strike.

Two further things a reviewer is invited to strike rather than accept: **D5's
conda enumeration**, which reaches into conda metadata inside a scope that was
narrowed away from conda — the defence is that it counts and never looks up, and
a reviewer may judge that too fine a line; and **Chunk 0's network fetch**, if
the reviewer thinks the fail-closed fallback is good enough to ship without ever
executing the real tool.

## Code review

*Filled in after implementation commits land.* The reviewer is not the
implementing agent. Begin with `**Model**: <model or tier when known; "unknown"
if not. Do not copy-paste old model labels; query and state your actual running
model identity.>` immediately below the section header (or below a
`### Code review -- <reviewer> -- YYYY-MM-DD` sub-heading).

The falsification ledger this review owes, at minimum: independently reproduce
**D-t2** (remove the zero-UNKNOWN gate and observe CLEAN) and **B-t2** (implement
the environment filter as a denylist and observe B-t1 green while B-t2 goes red)
rather than re-trusting the implementing session's transcript; confirm each
perturbation's byte-identical restore with `git hash-object` against
`git rev-parse HEAD:<path>`; and confirm `git status --short bootstrap/_scaffold/`
carries nothing attributable to this plan, since the empty symbol delta is the
whole of this scope's obligation to the shared ceremony.

## Lasting-truth migration

*Pre-declared here so no follow-up is discovered at archive time; the archive
record itself is appended when the plan archives, and this section is append-only
once written.* Per the
[Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home outside the
plan.

| Follow-up | Pre-declared home | State |
|---|---|---|
| **Conda / native advisory coverage** — 147 conda-only, 82 native, `as_of 2026-08-03` | `dev/PLANNING.md` > *Deferred follow-ups (durable home)* > **Security apparatus** > *Conda advisory coverage* | **Already homed**, ahead of the Decision. Verified present in the working tree. Nothing to migrate. |
| **A stored, integrity-covered residual baseline with a run-over-run diff** (the revision's schema / identity-tuple / integrity requirement, which v1 satisfies through the report rather than a file) | A new row under the same **Security apparatus** section, written at archive time — **unless the plan reviewer or Maintainer strikes the requirement**, in which case the disposition is recorded in the archive note instead. Its cost is a `bootstrap/_scaffold/config.py` delivery-registry row, which is why it is not v1. | To be written at archive |
| **Windows descendant cleanup** (A5's residual) and **child-disk exhaustion** (A3's residual) | One row under **Security apparatus**, named as two residuals of the shared runner boundary | To be written at archive |
| **The Chunk C tier change**, if the Maintainer strikes it | Recorded in the archive note as a struck item with the reason, not silently dropped | Conditional |
| **Chunk 0's fail-closed fallback**, if it is what shipped | Recorded in the archive note: the leg cannot establish zero UNKNOWN against the pinned tool version, so CLEAN is unreachable and the follow-up is a version-bump re-measurement | Conditional |

The evidence ledger this plan owes at archive: the Chunk 0 measurement block, the
per-chunk perturbation ledgers, the pre/post Bandit measurement over the
orchestrator, the `--manifest` empty diff, and the gate-integrity attribution
split.

See also `doctrine/lifecycle.md` > "Loop-fidelity verification" for the
Decision→implementation fidelity sign-off checkpoint.
