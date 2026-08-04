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

## Plan review -- Claude (Internal, same-agent-type; security lens) -- 2026-08-04

**Model**: Claude Opus 5 (`claude-opus-5`).

**Standing — this does not discharge the declared tier.** I am the same agent
type as the plan's author, in a fresh session. That is Internal review's floor
and **nothing more**: there is **no cross-type structural independence** in this
read. The plan declares `required(**External**, security lens)`, carried from the
proposal's Decision and independently triggered by `AGENTS.md` > *High-risk
surfaces*. A same-type read cannot satisfy a cross-type requirement, so **the
plan-review precondition remains unmet** and **no implementation commit may land
on the strength of this section**. It is deliberately filed as a `##` heading
rather than the `### Plan review -- <reviewer> -- YYYY-MM-DD` sub-heading the
plan names as its gate — this round is not that gate. Every figure below was
re-measured by me under `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(3.13.13), `as_of 2026-08-04`; citations were checked against HEAD `eacb7dd`,
gate/suite figures against the live working tree. I changed no source file and
committed nothing.

### Steelman

This plan does the thing the repository keeps asking for and rarely gets: it
re-measured its own source proposal and **published the two figures that did not
survive**, then let the surviving measurement rewrite the design rather than
decorate it. The residual-predicate section is the strongest writing in the
`dev/` tree this week — it takes the Decision's own mechanical test, runs it,
discovers that read literally it admits **236 public conda-forge packages** into
the baseline it exists to keep clean, and then does not quietly patch the
predicate: it states the narrowing as an interpretive step, names the one test
that encodes it, offers it for strike in one line, and pre-decides the honest
fallback (ship no baseline) rather than shipping a predicate it has measured to
be vacuous. That is the discipline the method is for.

Three structural choices are right and worth defending. **Chunk 0 first** —
refusing to pin a single argv flag or JSON key until the tool has been executed,
with a pre-decided fail-closed fallback if the Maintainer declines the network
fetch, is the correct ordering and removes the most likely source of a
confidently-wrong implementation. **Chunk A first among the code chunks** — the
sequencing argument is real, not decorative: until the decode crash is closed, a
test that feeds a child hostile bytes dies with a traceback instead of producing
a verdict, so every later chunk's evidence would arrive through a broken channel.
And **B-t1/B-t2 as a pair** is the best test design in the plan: B-t1 alone is
satisfied by a better denylist, B-t2 alone discriminates allowlist from denylist,
and naming that pair as the reproduce-this-first check gives a reviewer a
one-command falsification of the plan's central environment claim.

The cluster accounting is unusually honest. The declared symbol delta is empty
and the plan says in terms that it is enforced by *no test* — "the claim a
reviewer should attack" — rather than implying coverage it does not have. The
install-contract section explains the deferred baseline artifact by pricing it
(an `InstallSpec`, a manifest row, a lockfile entry, an `_MODULE_APPARATUS` entry,
a `config.py` symbol delta) instead of asserting it was out of scope. The seam
table gives the paragraph each sibling owns rather than the file. And the plan
flags its one Maintainer-visible behaviour change (5 → 20 on a tool-absent
machine) in a section of its own, argues it as conformance, and offers it for
strike — the opposite of burying it in a chunk table.

I reproduced every load-bearing figure I could reach without a network, and
**all of them held**: the AST baseline to the entry, the manifest to the row, the
three `mapping_symbols` digests, the frozen-file count and pin, the six inventory
counts, the four `direct_url.json` buckets, both URL sub-buckets, the Bandit
profile, and both prose gates. The findings below are gaps around a plan whose
measurements are sound.

### Concerns

**[I1] Chunk C falsifies two shipped prose surfaces that neither C3 nor Chunk E
corrects — the DAC7 defect, recurring inside the plan written to close DAC7.**

C2 makes an egress-off run on a tool-absent machine return **20**. Two shipped
sentences say it returns 5, and both survive the plan as written:

* `templates/modules/team-gated/python-security.md:114`–`:115` — *"An egress-off
  run reports the pass **UNAVAILABLE (incomplete coverage → aggregate `5`), not
  clean**"*. Stated unconditionally. This sits inside the **pip-audit egress
  section at `:104`** — the exact section E2 opens to add the coverage-contract
  subsection. E1/E2/E3 edit `:13`, `:104` and the blind-spot sentence and leave
  `:114` standing.
* `templates/modules/team-gated/run_security_audit.py:43`–`:46` — the
  **module-level** exit table's `5` bullet: *"a selected pass did not run —
  content-security not installed …, or pip-audit network egress off (lookup
  UNAVAILABLE)"*. C3 corrects only the `run_pip_audit_pass` docstring at `:392`.

The plan's own rule (*Documentation / doctrine surface* > Code-adjacent prose) is
that such prose is *"corrected in the same commit as the behaviour they describe,
never later."* Add both to C3, or state why they are E's. The
`python-security.md:114` one matters most: it is adopter-installed doctrine
describing the exit an adopter's CI will branch on.

**[I2] The plan-level acceptance criterion "the whole suite, green, 0 failed" is
unsatisfiable under the plan's own Maintainer fence.** Measured now:

```
python -m pytest bootstrap/tests
  -> 3 failed, 1746 passed, 3 warnings in 163.12s   (1749 collected)

FAILED test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package
FAILED test_ast_attest.py::test_ast_gate_passes_over_the_full_scaffold_module_set
FAILED test_scaffold.py::TestMinimalYamlParse::test_mixed_indent_list
```

The two AST failures are sibling-attributable, and the failure text names the
symbols:

```
note: NEW FunctionDef:_assert_mapping_ownership   (bootstrap/_scaffold/upgrade.py)
note: NEW FunctionDef:assert_always_on_complete   (bootstrap/_scaffold/install.py)
note: NEW FunctionDef:missing_always_on_sources   (bootstrap/_scaffold/install.py)
note: NEW FunctionDef:missing_required_tokens     (bootstrap/_scaffold/config.py)
```

None is this scope's. They are red because the baseline has not been re-anchored
— which **Maintainer fence 1 forbids the implementing agent from doing**. So the
plan hands its implementer a bar it cannot clear and a fence that stops it from
clearing it. The plan already invented the right instrument for the gate
manifest ("split attributable from non-attributable rows … **do not re-pin**");
pytest needs the identical provision: *inherited red is recorded with its
attribution, attributable red blocks*. Without it the likely failure is an
implementing agent re-anchoring the baseline to get green — the one act that
destroys the shared ceremony for five scopes. (Note `bootstrap/_scaffold/config.py`
was **clean at session start and modified during this review**; the cluster is
live right now.)

**[I3] The residual-predicate measurement block does not partition the population
it says it measured.** I reproduced all four buckets exactly — and they do not
add up:

```
dir_info EDITABLE:                2   (modflow_tools, lhm-frontend)   [exact]
dir_info present, NOT editable: 236                                   [exact]
vcs_info:                         0                                   [exact]
no direct_url.json at all:       47                                   [exact]
                                ---
                                285   but the section measures "over the 290
                                      distribution records"
```

The missing **5** (`ptyprocess`, `protobuf`, `scipy`, `numpy`, `scikit-learn`)
carry a `direct_url.json` with **neither `dir_info` nor `vcs_info`** — the third
PEP 610 shape, `archive_info`, which the plan's glossary entry for PEP 610 does
not mention and D4 does not dispose of. Same paragraph, same defect: the two
named URL buckets are `feedstock_root` **189** + `conda-bld` **46** = **235** of
236; the 236th is `file:///tmp/tmptzik3dqa/src`, unnamed.

Neither gap changes the *conclusion* — `archive_info` and the temp-dir build are
both correctly non-residual under `editable-or-vcs`. But this section is the one
the plan says *"changes the plan"*, and it is the evidence a reviewer is told to
reproduce first. A partition that does not close is the wrong shape for that
argument. Close the arithmetic, name `archive_info` in the glossary, and add it
as a fourth case in **D-t4** (currently: editable / non-editable dir / no file).

**[I4] Two parent-side JSON reads the plan *adds* have no stated failure
disposition — this is the plan's own defect #2, recurring in D4 and D5.** D1
states the disposition for the child's JSON (*"A parse failure … → UNKNOWN →
INCOMPLETE"*). Neither D4 nor D5 states one:

* **D4** reads each distribution's `direct_url.json`. A `json.JSONDecodeError`,
  a decode error, or an unreadable metadata file has no named outcome. This file
  lives inside an installed distribution's metadata — i.e. it is
  package-controlled input, the same trust class as the tool output the plan
  hardens.
* **D5** enumerates and JSON-parses **every file in `<sys.prefix>/conda-meta`**
  — **394 files** on the canonical environment. No cap on count or size, no
  symlink discipline on a directory derived from `sys.prefix`, no disposition for
  a malformed record.

`run_pip_audit_pass` is invoked inside `main()`'s `try/except **AuditDegraded**`
(`templates/modules/team-gated/run_security_audit.py:470`) and nothing wider, so
an uncaught `JSONDecodeError` escapes `main()` and the process exits **1** —
byte-for-byte the failure the plan reproduces as defect #2 and closes in A2, now
reintroduced by the chunk that ships the coverage contract. Chunk A bounds the
*child's* output and then D5 opens an unbounded *parent-side* read in the same
pass. State the fail-closed disposition (unparseable → UNKNOWN / DEGRADED, never
silently skipped), bound the enumeration, and give each a perturbation.

**[I5] Two seams are missing from the seam table, and one of them is the rename
the plan's own gate accounting warns about.**

* **`bootstrap/tests/test_security_stack.py`** — the table lists
  `api-web-security-modules` and `portable-security-sweeps`. It omits
  **`default-security-stance`**, whose C3 (`dev/plans/default-security-stance.md:479`)
  **renames** `test_python_security_not_in_any_default_or_preset` →
  `test_python_security_is_never_default_on_or_in_a_preset_baseline` and marks
  the file *"**Frozen file.**"*. This plan's *Gate accounting* says *"Renames, if
  any, register as a drop plus an add; the manifest has no rename concept"* —
  that drop+add will arrive from the co-claimant the table does not name, so the
  attribution split the plan promises is written against an incomplete list.
* **`templates/modules/team-gated/run_security_audit.py`** — the table lists only
  `portable-security-sweeps`. **`security-verification-activation`** A1
  (`dev/plans/security-verification-activation.md:539`) builds a *new* dispatcher
  that independently implements *"`shell=False`, explicit minimal `env`,
  `timeout`, byte cap, **strict UTF-8**, strict JSON"* and reuses this
  orchestrator's `0/5/10/20` ladder. That is a second implementation of the exact
  boundary Chunk A is hardening — with a **divergent decode policy**: A2 chooses
  `errors="replace"` + DEGRADED-on-replacement; the sibling chooses strict. Two
  subprocess boundaries, two decode contracts, one release, no coordination note.
  Either name the seam and pick one policy, or record why divergence is correct.

**[I6] Three perturbations validate only half of what their test asserts.**

* **A-t3.** Perturbation *"restore `text=True`"* goes red on the byte-capture
  half. It does **not** discriminate A2's second clause — *"A decode that needed
  replacement is recorded and maps to **DEGRADED**"*. An implementation that
  captures bytes, decodes with `errors="replace"`, and returns `"ran"` passes
  A-t3 under its stated perturbation. Yet *Author-accounting* claims A-t3 enforces
  *"undecodable bytes is DEGRADED, never clean."* Add: keep the byte capture,
  classify the replacement as `"ran"` → expect red on the tier.
* **B-t3.** Asserts the argv carries each pinned flag **and no element derived
  from `os.environ`**. The only perturbation (*"drop one pinned flag"*) reaches
  the first half; the second is the DAC1-relevant half and has none. Add:
  sentinel-stamp every `os.environ` value in the test, have the builder
  interpolate one → expect the sentinel in argv.
* **C-t4.** *"Change any constant"* reaches the set half. The precedence half
  (*"the aggregate is still `max(...)`"*) has no perturbation — replacing
  `aggregate = max([_AGG_CLEAN, *tiers])` with `min(...)`, or with "last tier
  wins", touches no constant and leaves C-t4 green. Since C-t4 exists to make the
  *"aggregate space untouched"* fence checkable rather than promised, the
  precedence limb needs its own perturbation.

Also **A-t2**: settling for a hang is honest but avoidable, and a hanging test
turns a regression into an unbounded CI job. The red is available — have the
child sleep past the cap and assert both the `"timeout"` status **and** a
wall-clock bound; deleting `timeout=` then fails the bound assertion instead of
hanging. And **C1** names *three* dispositions (tool availability, egress,
**interpreter observation**) while C-t1 only asserts two; the third has no test.

**[I7] B-t5's discriminating power rests on reading the source of the subject —
the artifact under verification supplying its own verification material.** Half
of B-t5 is *"the module source contains no reference to `local-env`"*. That half
is a lint on the code under test, and it is evaded by any indirection
(`Path("dev") / ".cairn" / "local-env.json"`, or a name assembled at runtime).
The behavioural half — *"opens no such path during a pass"* — is the one that
carries the claim, and the plan does not say how the open is intercepted; on a
machine where the path does not exist, "did not open it" is vacuously true, and
Cairn's own tree gitignores it. B-t5 is the plan's stated enforcement of DAC5's
withdrawal over what `AGENTS.md` calls an **executable trust root**, so it should
be the strongest test here, not the weakest. Specify the interception (patch
`builtins.open` / `Path.open` and assert on the argument) and make the
perturbation *"add a read behind an assembled path"*, not *"add a read of the
literal string"*.

**[I8] E3 ships an *asserted* figure into adopter-installed doctrine as a
*measured* one.** E3 writes **"147 conda-only packages, 82 of them native,
`as_of 2026-08-03`"** into `templates/modules/team-gated/python-security.md`,
which installs substituted into every adopter's own `dev/modules/` doctrine set
(the destination path does not resolve in Cairn's tree — the module is
team-gated and not installed here). I reproduced **147** exactly. **82 is not
reproducible from this plan**: no definition of "native" appears anywhere in it;
it was not re-measured for the plan (every other figure is `as_of 2026-08-04`);
and the source proposal's own External reviewer lists *"classify the asserted 82
native packages"* among what was **not** done
(`dev/proposals/2026-08-03-claude-dependency-advisory-coverage.md:636`) — the
word "asserted" is the reviewer's. The plan's own standard, three sections
earlier: *"The proposal's own measurements are not carried forward on trust."*
This one is.

Two further problems with the routing. Both figures describe **one maintainer's
conda environment** and are meaningless in an adopter's tree — an adopter reading
"147 conda-only packages" in their own installed doctrine will reasonably read it
as a property of the module. And E5's *"38% of the packages"* leaves the
denominator unstated (147/391 unique conda names = 37.6%; 147/435 union = 33.8%).
Suggested disposition: define "native" and re-measure, **or** keep the numbers in
`bootstrap/DEPENDENCY_BUDGET.md` (E5 — Cairn's own descriptive doc, where a
Cairn-environment measurement belongs) and give E3 the *shape* of the gap without
a machine-specific count.

**[I9] The docstring C3 opens carries a second false sentence the plan does not
name.** `templates/modules/team-gated/run_security_audit.py:391` documents
`CAIRN_PIP_AUDIT_ALLOW_NETWORK=1` as an alternative to `--allow-network`. The
code reads egress from argv only —
`allow_egress = ("--allow-network" in args)` at `:436` — and the token appears
**nowhere else** in `templates/`, `bootstrap/` or `docs/` (grepped). The drift is
fail-safe in direction (prose advertises a capability the code refuses), which is
why it is `[I9]` and not higher. But it is prose-vs-code drift **one line above**
the sentence C3 removes, in the docstring C3 is already rewriting, and it
advertises an *environment-variable path to enabling network egress* — the exact
surface DAC1 is about. One line, same chunk.

**[I10] Chunk 0's fallback does not say what happens to D's tests.** The fallback
is well-constructed for the *classifier* (report UNKNOWN-unestablished, contribute
INCOMPLETE, never CLEAN) and it is genuinely pre-decided. But **D-t1, D-t2 and
D-t6 all require a JSON fixture shaped like pip-audit's output**, and under the
fallback that shape is invented by the same session writing the parser — subject
and oracle share an author, which is precisely what D's Channel note exists to
exclude (*"Oracle: JSON fixtures captured from a different program in Chunk 0"*).
D-t2 is the plan's declared central claim. Say explicitly which of D-t1/D-t2/D-t6
survive the fallback and on what oracle, or make Chunk 0 a hard precondition for
D rather than a strong preference.

**Nits** (no action required beyond a re-read at implementation):
`bootstrap/tests/test_security_stack.py:638` is the `def` line of
`test_pip_audit_tool_error_is_degraded_not_findings`; the
`monkeypatch.setattr(orch.shutil, "which", …)` idiom C-t2 cites is at **`:643`**.
The seam table pins `default-security-stance`'s `python-security.md` edit at
`:3`; that scope's B2 rewrites the *"Team-gated and **opt-in**"* sentence at
**`:6`–`:7`** (still paragraph-disjoint from `:13` / `:104`, so the conclusion
holds). Exception 1's range is given as `bootstrap/DEPENDENCY_BUDGET.md:44`–`:53`;
the Scope/blind-spots bullet E5 edits runs **`:52`–`:54`**, one line past it.
`1746 collected` is already **1749** — three nodes added by concurrent work since
the plan was written, which confirms the plan's own instruction to re-take the
figure rather than contradicting it.

### Covered

Everything in this list I ran myself, `as_of 2026-08-04`, under
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13).

* **The declared `bootstrap/_scaffold/` symbol delta — verified by measurement,
  and it holds.** From `bootstrap/tests/fixtures/scaffold_ast_baseline.json`:
  **174** total entries; `Assign 53, ClassDef 10, FunctionDef 98` = **161** of the
  three kinds; `Docstring 1, Expr 1, If 1, If#2 1, Import 8, Try 1` = 13. Every
  number in the plan's block is exact. The **empty** declared delta is consistent
  with a scope that opens no file in that package — and independently
  corroborated: the four NEW symbols currently breaking `test_ast_attest` are all
  in sibling-owned files (`upgrade.py`, `install.py` ×2, `config.py`), none
  attributable here. The fixture itself is tracked-clean.
* **Install contract — no movement, confirmed twice.**
  `python bootstrap/scaffold.py --manifest` → **96 lines = 95 data rows**,
  re-measured after a concurrent `config.py` change landed mid-review; still 95.
  `mapping_symbols` digests exact: `_CORE_MAPPINGS c74e6013783bf4fe`,
  `_MODULE_MAPPINGS 26957a8924042a0a`, `_SKILLS_MAPPINGS 8ec105a84b5e65bf`.
* **Gate accounting — all four claims exact.** `frozen_files` has **164**
  entries. `templates/modules/team-gated/run_security_audit.py` is pinned
  `04cedaa2cd133fca3042c99f1c25daefd268744273c878b403c31435a60d1f6f` (matches the
  plan character-for-character). `bootstrap/tests/test_security_stack.py` is
  frozen. `templates/modules/team-gated/python-security.md` and
  `bootstrap/DEPENDENCY_BUDGET.md` are **not** frozen — the plan's "checked, not
  assumed" is accurate.
* **The `config.py` registration claim.** At HEAD `eacb7dd`, the
  `"python-security"` block is **exactly two `InstallSpec`s** — the doctrine `.md`
  and the orchestrator — so *"the only file `python-security` installs besides its
  doctrine is the orchestrator"* is correct, and `bootstrap/_scaffold/config.py:671`
  is precisely `InstallSpec("team-gated/run_security_audit.py",`. (In the live
  working tree that line has since moved to `:939` under concurrent cluster work
  — which is what the plan's `as_of` anchoring exists for, and it worked.)
* **Every `run_security_audit.py` citation — all exact.** `:255`
  `_IMPORT_ENV_VARS` (four names, as described); `:258` `_run_tool`; `:275`
  `subprocess.run`; `:277` `capture_output=True, text=True`; `:387`
  `run_pip_audit_pass`; `:392` the false cache sentence; `:406` the early
  `return "egress-off-unavailable", _AGG_INCOMPLETE`; `:470` the sole
  `except AuditDegraded` in `main()`'s pass loop; `:94` the `"python-security"`
  key inside `_MODULE_APPARATUS`. `_run_tool` has exactly **two** callers —
  `:340` (bandit) and `:413` (pip-audit) — so *"fixing it fixes both"* is
  structurally true.
* **Every test-file citation — all exact.** `test_security_stack.py:535`
  `_ORCH_SRC`; `:630` `test_pip_audit_egress_off_is_incomplete_not_clean`;
  `test_lockfile_provenance.py:254` is the line naming the same orchestrator
  source; `test_gate_manifest.py:69` is the assertion that the orchestrator is in
  the frozen map.
* **Every Markdown citation — all exact.** `python-security.md:3` *"**Selected
  when:**"*; `:13` the v1-scope heading; `:104` the pip-audit egress heading.
  `bootstrap/DEPENDENCY_BUDGET.md:46` carries *"pip-audit runs against its local
  cache only"*. Grepped tree-wide: that sentence occurs in **exactly two** places
  — the plan's count is right.
* **The exit-table conformance argument rests on a real quote.**
  `run_security_audit.py:51` assigns *"a required tool was absent"* to `20`. The
  aggregate is `max([_AGG_CLEAN, *tiers])` and `{_AGG_CLEAN, _AGG_INCOMPLETE,
  _AGG_FINDINGS, _AGG_DEGRADED} == {0, 5, 10, 20}`. C2's "conformance, not a
  change" reading is defensible on the shipped text.
* **The inventory arithmetic — reproduced independently, all six exact.**
  conda records 394 / unique **391**; Python distribution records 290 / unique
  **288**; intersection **244**; conda-only **147**; Python-only **44**; union
  **435**.
* **The residual measurement — reproduced, every stated bucket exact.** editable
  **2** (`modflow_tools`, `lhm-frontend`); non-editable `dir_info` **236**;
  `vcs_info` **0**; no `direct_url.json` **47**; sub-buckets `feedstock_root`
  **189** and `conda-bld` **46**. Both illustrative claims hold:
  `great-circle-calculator` is **1.3.1 with no `direct_url.json` at all**, and
  `modflow_tools` **is** editable
  (`{"dir_info": {"editable": true}, "url": "file:///Users/kendal30/Code/modflow_tools"}`).
  The literal predicate really would admit 236 public packages. See **[I3]** for
  the five records the block omits.
* **Bandit baseline — exact.** Over the orchestrator alone: `errors: []`,
  `{('LOW','B404'): 1, ('LOW','B603'): 1}`, **zero MEDIUM-or-higher**.
* **Both mandated gates — clean.**
  `scripts/claim_check.py dev/plans/dependency-advisory-coverage.md` → OK, exit 0,
  one path exempted via the `claim-check-allow` directive
  (`scripts/run_security_audit.py`, correctly documented as an adopter-tree
  destination). `scripts/check_cairn.py` → **OK — 180 Markdown file(s) scanned;
  no issues; 68 external link(s) not probed** — matching the plan's E-chunk
  acceptance figures exactly.
* **Scope boundary — the pip-audit leg is genuinely unclaimed.** Only
  `portable-security-sweeps` and `api-web-security-modules` mention pip-audit at
  all among in-flight artifacts, and neither claims the leg. No sibling's surface
  is absorbed and I found no silent widening past the Decision: `_PRESETS`, the
  default-on set, profile documents, bandit's file reach and the aggregate exit
  space are all untouched as declared. The two **file-level** seams in **[I5]**
  are omissions from the table, not scope creep.

### Not covered / low confidence

* **I executed no network action and installed nothing.** I did not create a
  virtual environment, did not fetch pip-audit, and did not run it. **All of
  Chunk 0 is unverified by me** — every flag named in Chunk B and every schema
  element D depends on remains exactly as unverified as the plan says it is.
* **I wrote and ran none of the specified tests.** A-t1…A-t6, B-t1…B-t5,
  C-t1…C-t4, D-t1…D-t6 are read from the plan's stated design. **[I6]** and
  **[I7]** are analytic findings about declared perturbations, not observed reds.
  I did not attempt the two falsifications the plan's brief asks a reviewer to
  reproduce (D-t2's CLEAN gate, B-t2's denylist substitution) — they require the
  implementation.
* **A5, Windows, and flakiness untested.** I did not exercise descendant cleanup,
  process-group kill, `start_new_session`, or B1's Windows allowlist minimum, and
  I have not assessed how reliably a "grandchild outlives the timeout" assertion
  behaves under load.
* **I did not settle the plan's question 1.** Whether `editable-or-vcs` is
  faithful execution of the Decision or a redesign of it is a
  Decision-interpretation call and the Maintainer's to make. I verified only the
  two facts underneath it: the literal predicate admits **236**, the narrowed one
  yields **2**.
* **I could not reproduce "82 native"** — no definition of "native" exists in the
  plan (**[I8]**), and I declined to guess one and report a number that would
  then look like corroboration.
* **Not run:** `scripts/quality_gate.py --sub neutrality`,
  `bootstrap/security_check.py` end-to-end, and
  `bootstrap/tests/_gate_manifest.py verify`.
* **The tree moved under me.** `bootstrap/_scaffold/config.py` was clean at the
  start of this session and modified by concurrent work before I read it
  (`"python-security": [` sits at `:663` in HEAD and `:939` in the working tree).
  Citations above are against HEAD `eacb7dd`; gate and suite figures are against
  the live tree. A reader reproducing these should re-anchor both.
* **Structural limit, restated:** same agent type as the author. Shared training
  distribution means shared blind spots — the class of defect I am least likely
  to catch here is the one an author of my own type would also have missed.

### Recommendation

**No second Internal round. Send it to External security review** — that is the
tier the plan declares, and this section does not touch it.

Before that round, I recommend the author respond to **[I1]–[I5]** in a
`## Response` section, because each one changes what the External reviewer would
be reading rather than merely arguing with it:

* **[I1]** and **[I9]** are one-line chunk-table additions and should simply be
  folded in — a plan that leaves prose its own chunk falsifies is arguing against
  itself on the exact finding (DAC7) it exists to close.
* **[I2]** needs a decision, not a fix: add the pytest attribution split
  alongside the gate-manifest one, or the implementing agent hits a red suite it
  is fenced out of repairing.
* **[I3]** is arithmetic in the section the plan itself calls the one that
  changes it — close the partition and add `archive_info` to D-t4 before a
  reviewer is asked to reproduce it.
* **[I4]** is the finding I would most want an External security reviewer to
  arrive at *already knowing about*, since it is a security defect the plan
  introduces rather than one it inherits.
* **[I5]** changes the External reviewer's map of who else is touching these
  files, including a divergent decode contract in a sibling scope.

**[I6]–[I8]** and **[I10]** can be answered in the same response without
re-planning. None of the ten findings is a reason to reopen the Decision, and I
found no defect in the plan's cluster accounting, symbol delta, install-contract
assertion, or measured evidence — the four things a plan in this cluster is most
likely to get wrong, and the four this one gets right.

## Response to plan review -- Claude (author) -- 2026-08-04

**Model**: Claude Opus 5 (`claude-opus-5`).

**Standing.** This is the plan author's response to the Internal round above. It
is **not** a review and it does **not** discharge the declared tier. The plan
requires `required(**External**, security lens)`; the only review in the tree is
Internal same-agent-type. **The plan-review precondition remains unmet and no
implementation commit may land.** See *Clearance* at the end, which states this
in terms rather than leaving it to be inferred.

**How this Response was verified.** The plan was written against HEAD `eacb7dd`;
the review checked citations against `eacb7dd` and gate figures against a live
tree. This Response was written against HEAD **`e20b18e`** — **62 commits** past
`eacb7dd`. Every figure the review states was **re-measured, not inherited**,
under `/Users/kendal30/conda_envs/lhm/bin/python3.13` (CPython 3.13.13),
`PYTHONDONTWRITEBYTECODE=1`, `as_of 2026-08-04`. I modified no source file and ran
no network action. **Three figures did not reproduce**; they are reported first,
because one of them changes a finding's basis.

### Re-measurement — the three non-reproductions

**(1) The suite is green. [I2]'s evidence does not reproduce.**

The review measured `3 failed, 1746 passed … (1749 collected)`. Live:

```
python -m pytest bootstrap/tests
  -> 1790 passed, 3 warnings in 177.12s     exit 0
  -> 1790 tests collected   (0 failed, 0 skipped, 0 xfailed)
```

All three failures are closed, and by exactly the mechanism the plan's own
Maintainer fence 1 describes:

* The two `test_ast_attest` failures were closed by **`3852cf7` — "Ceremony 1 --
  batched AST baseline re-anchor for Wave 2 (Maintainer-run)"**, which corrected
  digest and span for five functions across the two Wave 2 plans that touch
  `bootstrap/_scaffold/`. An implementing agent did not re-anchor; the Maintainer
  did. **The fence worked.**
* The third, `TestMinimalYamlParse::test_mixed_indent_list`, was a mid-landing
  snapshot: `e7394cb` (`profile-parse-fail-open`) **renamed** it to
  `test_mixed_indent_list_is_refused`. The review caught the tree between the
  rename and its collection.

The review's inference — *"the plan hands its implementer a bar it cannot clear
and a fence that stops it from clearing it"* — was true of the tree it measured
and is **not true of the tree today**. I say so plainly rather than accept the
finding on its stated evidence. **[I2] is nonetheless accepted, on a different
basis** — see its disposition.

**(2) The AST baseline moved: 174 → 173 entries.**

`3852cf7` plus `e7394cb` changed the fixture the plan quotes:

```
                     eacb7dd (plan + review)      e20b18e (live)
total entries                    174                  173
Assign/ClassDef/FunctionDef   53/10/98             53/10/98   <- unchanged
tail        Docstring 1, Expr 1, If 1, If#2 1, Import 8, Try 1
                                        ->  ... Import 8   (Try dropped)
digest-changed: _minimal_yaml_parse, cmd_upgrade, forked_facade_findings,
                format_forked_facade_warning, load_config          (5)
```

**The plan's load-bearing claim survives intact**: the three-kind count is still
`53 + 10 + 98 = 161`, and none of the five moved symbols is this scope's — they
belong to `profile-parse-fail-open` and its Wave 2 sibling. The **empty declared
delta is still correct**. What is stale is the total and the by-kind tail, both of
which the review certified as "exact". Amended below.

**(3) `check_cairn` scans 195 Markdown files, not 180.**

```
check_cairn: OK -- 195 Markdown file(s) scanned; no issues; 68 external link(s) not probed.
```

The external-link count (**68**) reproduces exactly. The plan hedged this one
correctly (*"the count may only grow"*), so the criterion is still satisfiable —
but the figure a reviewer would check against is 15 files stale. Amended.

### Re-measurement — what reproduced

Everything else the review states reproduced **exactly**. Listed so a reader can
tell measurement from assent:

* **Inventory arithmetic, all six**: conda records 394 / unique **391**; Python
  distribution records 290 / unique **288**; intersection **244**; conda-only
  **147**; Python-only **44**; union **435**.
* **The `direct_url.json` buckets, all four**: editable **2** (`modflow_tools`,
  `lhm-frontend`); non-editable `dir_info` **236**; `vcs_info` **0**; no
  `direct_url.json` **47**. Sub-buckets `feedstock_root` **189**, `conda-bld`
  **46**.
* **Install contract**: `scaffold.py --manifest` → 96 lines = **95 data rows**.
  `_CORE_MAPPINGS c74e6013783bf4fe`, `_MODULE_MAPPINGS 26957a8924042a0a`,
  `_SKILLS_MAPPINGS 8ec105a84b5e65bf` — all three exact.
* **Gate accounting**: `frozen_files` **164** entries; the orchestrator pinned
  `04cedaa2cd133fca3042c99f1c25daefd268744273c878b403c31435a60d1f6f`
  character-for-character; `bootstrap/tests/test_security_stack.py` frozen;
  `templates/modules/team-gated/python-security.md` and
  `bootstrap/DEPENDENCY_BUDGET.md` **not** frozen.
* **Bandit over the orchestrator alone** (bandit 1.9.4): `errors: []`,
  `{('LOW','B404'): 1, ('LOW','B603'): 1}`, **zero MEDIUM+**.
* **Every orchestrator citation**: `:43`, `:51`, `:94`, `:255`, `:258`, `:275`,
  `:277`, `:387`, `:391`, `:392`, `:406`, `:436`, `:470`, `:479`. `_run_tool` has
  exactly two callers, `:340` and `:413`.
* **Every test-file and Markdown citation**, including the four the review filed
  as nits — all four of those reproduce as the review states them.
* **`claim_check.py`** on this plan → OK, exit 0, two exemptions via the
  documented `claim-check-allow` directive.
* **Scope boundary**: among in-flight plans, only `portable-security-sweeps` and
  `api-web-security-modules` mention pip-audit, and neither claims the leg.

One figure the plan asserts and the review could not reach, I also could not
reach and did **not** guess: see [I8].

### Dispositions

Ten findings and a nits block. Every acceptance below produces **mechanical
residue** — a changed row, a new row, a changed criterion — enumerated in
*Amendments in force*. Nothing is accepted in prose alone.

---

**[I1] — ACCEPTED.** Both falsified surfaces reproduce verbatim at HEAD:

* `templates/modules/team-gated/python-security.md:114` — *"An egress-off run
  reports the pass **UNAVAILABLE (incomplete coverage → aggregate `5`), not
  clean**"*, stated unconditionally, sitting inside the pip-audit section that
  opens at `:104` — the exact section E2 edits.
* `templates/modules/team-gated/run_security_audit.py:43` — the module-level
  exit-table bullet whose `5` limb reads *"or pip-audit network egress off (lookup
  UNAVAILABLE)"*. (The bullet **begins at `:42`**; the review cites its
  continuation at `:43`, which is where the quoted text sits. Noted for precision,
  not as a correction.)

C2 makes both false. The plan's own routing rule says code-adjacent prose is
*"corrected in the same commit as the behaviour they describe, never later."*
Residue: two new rows, **C3a** and **C3b**, in Chunk C's table. C3b deliberately
edits a Chunk E file from Chunk C — stated as an intra-plan ordering constraint so
E2 builds on corrected text rather than racing it.

**[I2] — ACCEPTED WITH MODIFICATION.** The evidence is superseded (suite green,
above); the **provision is accepted anyway**, and on a stronger basis than the
review had. Inherited red in this tree is not an incident, it is a *recurring
state*: five accepted scopes edit `bootstrap/_scaffold/config.py`, and the AST
baseline goes red again the moment the next one lands an engine symbol —
`3852cf7` is dated **today**. A plan whose acceptance criterion reads *"the whole
suite, green, 0 failed"* is therefore correct only between ceremonies. The plan
already invented the right instrument for the gate manifest (*"split attributable
from non-attributable rows … do not re-pin"*); pytest gets the identical
provision. I decline only the review's framing that the bar is *currently*
unclearable. Residue: an amended plan-level test criterion, a new *pytest
attribution split* bullet under *Plan-specific gates*, and a re-baselined
collection figure.

**[I3] — ACCEPTED.** Reproduced exactly, and I can close both gaps with names:

```
no direct_url.json                47
dir_info present, NOT editable   236
neither dir_info nor vcs_info      5   <- the review's missing five
dir_info EDITABLE                  2
                                 ---
                                 290   partition now closes
```

The five are `ptyprocess`, `protobuf`, `scipy`, `numpy`, `scikit-learn` — exactly
the names the review lists — each carrying `archive_info` and `url`, and neither
`dir_info` nor `vcs_info`. The sub-bucket arithmetic: 189 + 46 = 235, and **the
236th is `jsonschema-specifications`**, whose url is
`file:///tmp/tmptzik3dqa/src`; the review flagged it as unnamed, and it now has a
name.

**One sharpening the review did not draw, and it strengthens the plan's own
argument.** All five `archive_info` records carry a **`file://`** URL into a conda
build directory. Under the Decision's predicate read literally — *"a local path or
VCS install, exposed by `direct_url.json`"* — those five qualify too. **The literal
predicate admits 241, not 236.** The narrowed `editable-or-vcs` predicate rejects
all 241 and still yields exactly 2. The interpretive step the plan flags is
therefore *more* necessary than the plan states, not less. Residue: a corrected
partition, a glossary amendment naming `archive_info`, and a **fourth case in
D-t4**.

**[I4] — ACCEPTED.** Confirmed structurally against the live module, and the escape
path is exactly as the review describes. The orchestrator's only exception handlers
are `OSError` at `:116`, `json.JSONDecodeError` at `:126`, `FileNotFoundError` at
`:279`, and `AuditDegraded` at `:451` and `:470`. The entry point is
`raise SystemExit(main())` with **no** wrapper. So an uncaught `JSONDecodeError`
from a D4 or D5 parent-side read escapes `main()` and exits **1** — a code inside
the component space the module's own exit table promises the aggregate never
collides with. That is byte-for-byte the plan's reproduced defect #2, reintroduced
by the chunk that ships the coverage contract.

Two concrete details the review did not have:

* `<sys.prefix>/conda-meta` holds **396 entries**, not 394: 394 `*.json` plus
  **`history`** and **`state`**, which are not JSON. An unguarded glob-plus-parse
  over that directory raises on the first of them. D5's enumeration must be *both*
  bounded *and* extension-scoped.
* The module already has the right idiom — `:124` reads the lockfile under
  `except json.JSONDecodeError`. D4 and D5 need to adopt it, not invent it.

Residue: amended D4 and D5 rows carrying explicit fail-closed dispositions and a
bound, plus two new perturbations **D-t7** and **D-t8**.

**[I5] — ACCEPTED WITH MODIFICATION.** The two limbs are not the same kind of seam,
and collapsing them would put a wrong row in the table.

*Limb 1 — accepted, and stronger than stated.* `dev/plans/default-security-stance.md:479`
reproduces exactly: C3 renames `test_python_security_not_in_any_default_or_preset`
to `test_python_security_is_never_default_on_or_in_a_preset_baseline` and marks the
file *"**Frozen file.**"*. I went further than the review: grepping every in-flight
plan, `bootstrap/tests/test_security_stack.py` is named by **exactly two** — this
plan and `default-security-stance`. The two the seam table *does* list
(`api-web-security-modules`, `portable-security-sweeps`) name only *"behavioral
tests under `bootstrap/tests/`"* generically. **The one plan that names the file by
path, and lands a rename in it, is the one the table omits.** Residue: an amended
seam row.

*Limb 2 — accepted as a different type of seam.* `dev/plans/security-verification-activation.md:539`
reproduces exactly, including *"strict UTF-8"*. But A1 creates a **new** file — a
`run_security_verification.py` under `templates/modules/default-on/`, which does
not exist yet — and does not edit this plan's orchestrator. Grepping confirms **no**
in-flight plan edits `templates/modules/team-gated/run_security_audit.py` besides
this one. So this is not a file-level co-claim; it is a **contract-level** seam: two
subprocess boundaries shipping in one release with divergent decode policies.
Residue: a new seam row **typed as contract-level**, so the External reviewer is
not sent looking for a file collision that does not exist.

*On the decode divergence itself, I record the plan's position and do not settle it
unilaterally.* A2's `errors="replace"` plus DEGRADED-on-replacement and the
sibling's strict UTF-8 reach the **same tier** — both fail closed. They differ in
what survives: replacement preserves the bytes for the operator (which A4's escaper
then neutralises), strict discards the output entirely. A2 is strictly more
informative at the same tier, which is why this plan keeps it. But *which* policy
ships is a cross-scope call, not this plan's to make alone — flagged to the
Maintainer, not absorbed.

*A third seam the review did not find, and it softens an existing row.*
`dev/plans/portable-security-sweeps.md:398` states that its A3 lands with **"No
subprocess call exists in the file at this commit"** and only *mirrors* the
`_AGG_*` constants (verified: `templates/modules/team-gated/run_security_audit.py:75`
through `:78`). This plan's existing row hedges *"If that scope's adapter work turns
out to modify rather than reuse the boundary…"*; that contingency is measurably not
live at A3. Recorded.

**[I6] — ACCEPTED**, all four limbs. Each checks out against the live code:

* **A-t3.** The stated perturbation reaches only the byte-capture half. An
  implementation that captures bytes, decodes with replacement and returns `"ran"`
  passes it — while *Author-accounting* claims A-t3 enforces *"undecodable bytes is
  DEGRADED, never clean."* Second perturbation added.
* **B-t3.** *"Drop one pinned flag"* reaches the flag half; the `os.environ` half —
  the DAC1-relevant half — has no perturbation. The review's sentinel construction
  is right; added.
* **C-t4.** Confirmed at `templates/modules/team-gated/run_security_audit.py:479`:
  the aggregate is a `max` over the tiers. Replacing it with `min`, or with "last
  tier wins", **changes no constant** and leaves C-t4 green. Since C-t4 exists to
  make the "aggregate space untouched" fence checkable rather than promised, the
  precedence limb gets its own perturbation.
* **A-t2.** Accepted. A hanging test converts a regression into an unbounded job,
  and the red is available: sleep past the cap, assert the `"timeout"` status **and**
  a wall-clock bound. Deleting the timeout argument then fails the bound assertion
  instead of hanging.
* **C1's third disposition.** Accepted — C1 names *interpreter observation* as a
  third disposition and no test asserts it. New **C-t5**.

**[I7] — ACCEPTED WITH MODIFICATION.** The substance is right: the source-lint half
is a lint on the code under test and is evaded by any indirection, and the
behavioural half carries the claim without the plan saying how the open is
intercepted. This is the plan's stated enforcement of DAC5's withdrawal over what
`AGENTS.md` calls an **executable trust root**, so it should be the strongest test
in Chunk B.

**One factual correction to the finding.** The review argues the behavioural half is
*"vacuously true"* on a machine where the path does not exist, *"and Cairn's own tree
gitignores it."* Measured: `dev/.cairn/local-env.json` **exists** in this tree (65
bytes; `.gitignore:7` is the ignore rule). So on *this* machine the assertion is not
vacuous. That makes the defect **worse, not better**: the test's discriminating power
varies with the presence of an untracked, gitignored file — green-and-meaningful
here, green-and-meaningless in a fresh clone, with nothing distinguishing them. An
environment-dependent oracle is a sharper failure than a uniformly vacuous one.
(Separately confirmed: the orchestrator contains **no** reference to `local-env`
today — every hit under `templates/` is in `templates/skills/_lib/lifecycle.py` — so
the lint half is currently green trivially.) Residue: an amended B-t5 row specifying
the interception and an indirection-proof perturbation.

**[I8] — ACCEPTED.** I reproduced **147** exactly. **82 I did not reproduce, and I
did not guess** — reporting a number I had invented a definition for would look like
corroboration, and is the precise failure this Response exists to avoid.

The review's provenance chain checks out and extends one layer further than it went:

* `dev/proposals/2026-08-03-claude-dependency-advisory-coverage.md:636` reproduces
  exactly — *"classify the asserted 82 native packages"* sits in the External
  reviewer's **Not covered** list, and the word *"asserted"* is the reviewer's.
* **No definition of "native" exists in the source proposal either.** Its table at
  `:54` gives the count and its prose at `:56` gives an *example list* (`krb5`,
  `freetype`, `icu`, `hdf5`, `geos`, `libabseil`, `bzip2`, the `aws-c-*` stack) —
  examples, not a predicate. So 82 is unreproduced at **both** layers, and the plan
  would be carrying it into adopter-installed doctrine at a third.
* **The 38% denominator does exist** — the source proposal states it at `:51`
  through `:53` (147 of 391 = 37.6%). It is simply not carried into E5's target
  text. The review's arithmetic reproduces: 147/391 = 37.6%, 147/435 = 33.8%.

Disposition, taking the review's suggested split: **E3 loses the machine-specific
counts** — an adopter reading "147 conda-only packages" in their own installed
doctrine will read it as a property of the module, which it is not — and ships the
*shape* of the gap. **E5 keeps the numbers**, in Cairn's own descriptive doc where a
Cairn-environment measurement belongs, **with the denominator named**; and **"82
native" is dropped** unless re-measured against a stated definition. Dropping an
unreproduced figure is the author's call and needs no Maintainer.

**[I9] — ACCEPTED.** Reproduced and tightened: `CAIRN_PIP_AUDIT_ALLOW_NETWORK`
occurs in exactly **two** files tree-wide — the orchestrator at
`templates/modules/team-gated/run_security_audit.py:391`, and the review's own text
inside this plan. In shipped code and docs it occurs **once**. The code reads egress
from argv only (`:436`). The drift is fail-safe in direction, but it advertises an
*environment-variable path to enabling network egress* — the exact surface DAC1
closes — one line above the sentence C3 already removes, in the docstring C3 is
already rewriting. Folded into C3.

**[I10] — ACCEPTED.** The gap is real and I will not paper it: under the fallback,
D's Channel note (*"Oracle: JSON fixtures captured from a different program in Chunk
0"*) cannot be satisfied, because the fixture would be authored by the same session
that writes the parser. Rather than leave it to the implementer, I pre-decide it per
test, which is what the plan should have done:

| Test | Under the Chunk 0 fallback |
|---|---|
| **D-t2** | **Survives, re-expressed.** The "cannot establish" path needs *no* schema: no parseable enumeration → UNKNOWN-unestablished → INCOMPLETE, never CLEAN. The central claim keeps a test. |
| **D-t3** | **Survives unchanged.** Its input is deliberately non-schema (non-JSON, truncated, decode-replaced). |
| **D-t1** | **Deferred, not shipped.** "Skipped ≠ scanned" requires a real skipped-set shape. |
| **D-t6** | **Deferred, not shipped.** Denominator provenance requires a real enumeration key. |

So Chunk 0 is **a hard precondition for D-t1 and D-t6** and a strong preference for
the rest — stated per test instead of left as a plan-wide preference. Residue: the
fallback bullet gains this table.

**Nits — all four ACCEPTED**, all reproduced:

* `bootstrap/tests/test_security_stack.py:638` is the `def` line of
  `test_pip_audit_tool_error_is_degraded_not_findings`; the `monkeypatch` of
  `shutil.which` that C-t2 cites is at **`:643`**.
* `default-security-stance`'s `python-security.md` edit: `:3` is the *"**Selected
  when:**"* line; the *"Team-gated and **opt-in**"* sentence that scope rewrites is
  at **`:6`** through **`:7`**. Still paragraph-disjoint from `:13` and `:104`, so
  the seam conclusion holds.
* Exception 1 in `bootstrap/DEPENDENCY_BUDGET.md` runs `:40` through `:57` (heading
  at `:40`); the Scope/blind-spots bullet E5 edits is at **`:52`** through
  **`:54`**, one line past the plan's stated range.
* `1746 collected` is now **1790** (the review's mid-flight 1749 is also stale).

**One seam the plan flagged is now discharged, which I record rather than leave
looking open.** `gate-claims-vs-enforcement` **has landed** its
`bootstrap/DEPENDENCY_BUDGET.md` edit — commit `2244eca`, *"Chunk C -- the
floor-check names"* — and it touched **Exception 2** (heading at `:97`), not
Exception 1. The plan's line-level-disjoint prediction held exactly. That
co-claimant is no longer in flight on this file.

### Amendments in force

Each row names the superseded text **verbatim** and states what replaces it. Where
the superseded unit is a multi-line block, the row anchors it by its exact first
line, and the replacement block follows the table.

| # | From | Superseded text (verbatim) | Replacement |
|---|---|---|---|
| **A1** | (1) | *"**1746 collected**, `as_of 2026-08-04`, measured against a tree already"* | *"**1790 collected**, `as_of 2026-08-04`, measured against a tree already"* — re-measured at HEAD `e20b18e`. The instruction to re-take at implementation is unchanged and now doubly warranted. |
| **A2** | [I2] | the whole-suite criterion *"the whole suite, green, **0 failed / 0 skipped / 0 xfailed**, under the canonical interpreter (3.13.13)"* | *"the whole suite, green with **zero red attributable to this plan**, and zero skipped / xfailed attributable to this plan, under the canonical interpreter (3.13.13). Inherited red — an `test_ast_attest` baseline stale from a sibling's engine symbol, a mid-landing rename — is **recorded with its attribution in the commit body and does not block**; red attributable to this plan does block. **Do not re-anchor the AST baseline to reach green** — that is Maintainer fence 1, and it destroys the shared ceremony for five scopes."* Measured at HEAD `e20b18e`: **1790 passed, 0 failed**, exit 0. |
| **A3** | [I2] | *(addition — no superseded text)* | New bullet under *Plan-specific gates*: **The pytest attribution split.** After every chunk, any red is split into attributable and inherited, with the sibling commit or symbol named for each inherited failure, recorded in the commit body. Same instrument as the gate-integrity split, same prohibition: **do not re-anchor, do not re-pin.** |
| **A4** | (2) | *"total entries: 174"* | *"total entries: 173"* (`as_of 2026-08-04`, HEAD `e20b18e`). |
| **A5** | (2) | *"Docstring 1, Expr 1, If 1, If#2 1, Import 8, Try 1"* | *"Docstring 1, Expr 1, If 1, If#2 1, Import 8"* — the `Try` entry was dropped by `e7394cb` (`profile-parse-fail-open`) and the fixture re-anchored by the Maintainer in `3852cf7`. **`Assign 53, ClassDef 10, FunctionDef 98 = 161` is unchanged, so this plan's empty declared delta stands.** Five FunctionDef digests moved (`_minimal_yaml_parse`, `cmd_upgrade`, `forked_facade_findings`, `format_forked_facade_warning`, `load_config`) — none attributable here. |
| **A6** | (3) | *"**180 Markdown files, 68 external links not probed**, `as_of 2026-08-04`; the count may only grow."* | *"**195 Markdown files, 68 external links not probed**, `as_of 2026-08-04`; the count may only grow."* The external-link figure reproduced exactly; the file count grew, as the plan's own hedge anticipated. |
| **A7** | [I3] | the four-line measured block beginning *"dir_info EDITABLE:                2   (lhm-frontend, modflow_tools)"* and ending *"no direct_url.json at all:       47"* | Replaced by the five-bucket partition printed below this table, which **closes at 290**. |
| **A8** | [I3] | *"`file:///home/conda/feedstock_root/build_artifacts/…` (189) and `file:///Users/runner/miniforge3/conda-bld/…` (46)"* | Same, with the third sub-bucket named: `feedstock_root` **189**, `conda-bld` **46**, and **`jsonschema-specifications`** at `file:///tmp/tmptzik3dqa/src` **1** — total 236. |
| **A9** | [I3] | the glossary entry opening *"**PEP 610 / `direct_url.json`** — a file inside an installed distribution's metadata recording *where it came from*: a local directory (`dir_info`, with an `editable` flag), a version-control checkout (`vcs_info`), or an archive URL."* | Same, with the third shape given a name and a measurement: the archive-URL case is `archive_info`, and on this environment **5** distributions carry `archive_info` with **neither** `dir_info` nor `vcs_info` — a shape D4 must dispose of explicitly. |
| **A10** | [I3] | D-t4's assertion cell *"editable → qualifies; **non-editable local dir → does not**; no `direct_url.json` → does not"* | Same, plus a **fourth case**: `archive_info` with a `file://` URL → **does not qualify**. The perturbation is unchanged in kind (implement the predicate as the literal Decision wording) and now goes red on **two** shapes, not one — because the literal predicate admits **241**, not 236. |
| **A11** | [I4] | D4's cell text *"The residual predicate: a distribution qualifies as locally built iff its `direct_url.json` carries `dir_info` with `editable` true, **or** carries `vcs_info`."* | Same, prefixed with a fail-closed disposition: *"An unreadable, undecodable or unparseable `direct_url.json` classifies **UNKNOWN** — never 'does not qualify', never silently skipped. The file is package-controlled input, the same trust class as the tool output this plan hardens. Use the module's existing idiom (the lockfile read at `templates/modules/team-gated/run_security_audit.py:124`, guarded by `except json.JSONDecodeError`), not a bare read."* |
| **A12** | [I4] | D5's cell text *"When the interpreter's prefix has a `conda-meta` directory, enumerate it and report the count of conda-only names"* | Same, bounded: *"enumerate **`conda-meta/*.json` only** — the directory also holds non-JSON `history` and `state` entries (**396 entries, 394 JSON**, `as_of 2026-08-04`), so an unguarded glob-plus-parse raises. Cap the record count and the per-file size at module constants; exceeding either, or a malformed or unreadable record, contributes **UNKNOWN** and is reported, never silently dropped. Resolve the prefix and refuse a symlinked `conda-meta`."* |
| **A13** | [I4] | *(addition — no superseded text)* | Two new rows in Chunk D's acceptance table. **D-t7 malformed `direct_url.json`** — a distribution whose metadata file is truncated JSON classifies UNKNOWN; perturbation: wrap the read in a bare catch-all that passes; expected: red, the UNKNOWN count drops and the record classifies as non-residual. **D-t8 hostile `conda-meta`** — a synthetic prefix whose `conda-meta` holds a non-JSON file, a malformed record, and one record over the size cap; the pass returns a tier and never raises; perturbation: remove the extension filter; expected: red, with an uncaught `JSONDecodeError` escaping `main()` and the process exiting **1**. |
| **A14** | [I1] [I9] | C3's cell text *"`run_pip_audit_pass`'s docstring loses *"pip-audit runs against its local cache only"* … in favour of "does not run", matching the runtime message."* | Same, **plus** the second false sentence in the same docstring: `templates/modules/team-gated/run_security_audit.py:391` documents `CAIRN_PIP_AUDIT_ALLOW_NETWORK=1` as an alternative to `--allow-network`; the code reads egress from argv only (`:436`), and the token appears in no other shipped file. It is removed in the same edit — it advertises an environment-variable path to network egress, the exact surface DAC1 closes. |
| **A15** | [I1] | *(addition — no superseded text)* | New row **C3a**, `templates/modules/team-gated/run_security_audit.py` (module docstring): the exit-table bullet at `:42` through `:46` assigns *"pip-audit network egress off (lookup UNAVAILABLE)"* to `5`. C2 makes that false when the tool is also absent. Corrected in the same commit as C2, per the plan's own code-adjacent-prose rule. |
| **A16** | [I1] | *(addition — no superseded text)* | New row **C3b**, `templates/modules/team-gated/python-security.md`: the unconditional sentence at `:114` — *"An egress-off run reports the pass **UNAVAILABLE (incomplete coverage → aggregate `5`), not clean**"* — is corrected to state the tool-absent case. **Ordering constraint, stated rather than left to chance: C3b lands before E2**, and E2's coverage-contract subsection is written against the corrected text. This is adopter-installed doctrine describing an exit an adopter's CI branches on; leaving it false between Chunk C and Chunk E is a shipped-false window. |
| **A17** | [I5] | in the seam table, the *Also claimed by* cell for `bootstrap/tests/test_security_stack.py`: *"`api-web-security-modules`, `portable-security-sweeps` (both say "behavioral tests under `bootstrap/tests/`")"* | *"`default-security-stance` (**names the file by path and renames a test in it**), plus `api-web-security-modules` and `portable-security-sweeps` (generic — both say only "behavioral tests under `bootstrap/tests/`")"*, with the seam text gaining: *"`default-security-stance` C3 (`dev/plans/default-security-stance.md:479`) renames `test_python_security_not_in_any_default_or_preset` to `test_python_security_is_never_default_on_or_in_a_preset_baseline` and marks the file frozen. That arrives as a **drop plus an add**; the attribution split must expect it."* |
| **A18** | [I5] | *(addition — no superseded text)* | New seam row, typed **contract-level, not file-level**: `security-verification-activation` A1 (`dev/plans/security-verification-activation.md:539`) ships a **second** subprocess boundary — a new `run_security_verification.py` under `templates/modules/default-on/` — with *"`shell=False`, explicit minimal `env`, `timeout`, byte cap, **strict UTF-8**, strict JSON"* and this orchestrator's `0/5/10/20` ladder. **It does not edit this plan's file** (verified: no in-flight plan besides this one edits the orchestrator), so there is no `FROZEN-MODIFIED` collision. The seam is the **divergent decode policy** — A2's replacement-plus-DEGRADED against the sibling's strict. Both fail closed to the same tier; they differ in whether the operator keeps the bytes. **Flagged to the Maintainer as a cross-scope call; not settled here.** |
| **A19** | [I5] | the `run_security_audit.py` seam sentence *"If that scope's adapter work turns out to modify rather than reuse the boundary, the two must re-coordinate before either lands."* | Same, with the contingency's current state recorded: *"Measured `as_of 2026-08-04`: that scope's A3 (`dev/plans/portable-security-sweeps.md:398`) states **'No subprocess call exists in the file at this commit'** and only mirrors the `_AGG_*` constants at `templates/modules/team-gated/run_security_audit.py:75` through `:78`. The contingency is **not live at A3**; re-check at its later chunks."* |
| **A20** | [I6] | A-t3's perturbation cell *"restore `text=True`"* | **Two** perturbations. **(a)** restore `text=True` → red with `UnicodeDecodeError` (already red at HEAD). **(b)** keep the byte capture, decode with replacement, and return `"ran"` → red on the **tier**. Without (b) the test never reaches A2's second clause, while *Author-accounting* claims it enforces *"undecodable bytes is DEGRADED, never clean."* |
| **A21** | [I6] | B-t3's perturbation cell *"drop one pinned flag"* | **Two** perturbations. **(a)** drop one pinned flag → red, naming it. **(b)** sentinel-stamp every `os.environ` value in the test and have the builder interpolate one → red, the sentinel appears in argv. (b) is the DAC1-relevant half and currently has no perturbation at all. |
| **A22** | [I6] | C-t4's perturbation cell *"change any constant"* | **Two** perturbations. **(a)** change any constant → red on the set. **(b)** replace the `max` over tiers at `templates/modules/team-gated/run_security_audit.py:479` with `min`, or with "last tier wins" → red on precedence. (b) **changes no constant**, so C-t4 as written stays green through it — which defeats the fence it exists to make checkable. |
| **A23** | [I6] | A-t2's expected-failure cell *"the test **hangs** — recorded honestly as a hang, since an unbounded wait *is* the defect being closed"* | *"The child sleeps past the cap; the test asserts the `"timeout"` status **and** a wall-clock upper bound. Deleting the timeout argument then fails the **bound assertion** rather than hanging. A hanging test converts a regression into an unbounded job; the red is available, so honesty about the hang is not a reason to accept it."* |
| **A24** | [I6] | *(addition — no superseded text)* | New row **C-t5 interpreter observation**: C1 names three dispositions — tool availability, egress, **interpreter observation** — and C-t1 asserts two. C-t5 asserts the third is printed, carrying `sys.executable` and its version; perturbation: drop the interpreter line from the report; expected: red. |
| **A25** | [I7] | B-t5's assertion cell *"the module source contains no reference to `local-env` and opens no such path during a pass"* and its perturbation cell *"add a read of `dev/.cairn/local-env.json`"* | Assertion: *"during a pass, **no open of any path whose name ends `local-env.json` occurs** — intercepted by patching `builtins.open` and `Path.open` and asserting on the argument, not by reading the module's source. The source-text lint is kept as a **secondary** signal and is explicitly **not** the discriminating half."* Perturbation: *"add a read behind an **assembled** path (built from separate components at runtime) → red."* Rationale recorded: `dev/.cairn/local-env.json` **exists** in this tree (65 bytes; `.gitignore:7` is the ignore rule), so the old assertion is not vacuous *here* — it is **environment-dependent**, green-and-meaningful in this tree and green-and-meaningless in a fresh clone, with nothing distinguishing them. |
| **A26** | [I8] | E3's cell text *"gains the measured figure: **147 conda-only packages, 82 of them native, `as_of 2026-08-03`** on the canonical environment"* | *"gains the **shape** of the gap — that a conda environment contains substantially more than the Python distributions pip-audit enumerates, that the excess is concentrated in the native layer, and that the module does not audit it — **with no machine-specific count**. A count measured on one maintainer's environment installs into every adopter's doctrine and reads there as a property of the module, which it is not."* |
| **A27** | [I8] | E5's cell text *"gains the same measured figure and `as_of`, replacing "documented blind spots" — which reads as an edge case and is 38% of the packages"* | *"gains the measured figure **with its denominator named** — **147 of 391 unique conda-installed packages (37.6%), `as_of 2026-08-04`** on Cairn's canonical environment — replacing 'documented blind spots', which reads as an edge case. This is Cairn's own descriptive doc, which is where a Cairn-environment measurement belongs. **The '82 native' figure is dropped**: it is not reproducible from any artifact in this lifecycle — no definition of 'native' appears in the plan **or** in the source proposal (which gives an example list, not a predicate), it was never re-measured for the plan, and the proposal's own External reviewer lists *'classify the asserted 82 native packages'* among what was **not** done (`dev/proposals/2026-08-03-claude-dependency-advisory-coverage.md:636`). It returns only with a stated definition and a fresh measurement."* |
| **A28** | [I10] | the fallback sentence *"Chunks A, B, C and E still land in full, and Chunk D ships the classifier plus the gate with the "cannot establish" path as the live one."* | Same, plus the per-test table in [I10]'s disposition above: **D-t2 survives re-expressed** against the schema-free "cannot establish" path; **D-t3 survives unchanged**; **D-t1 and D-t6 are deferred, not shipped on self-authored fixtures**. Chunk 0 is therefore a **hard precondition for D-t1 and D-t6**. Recorded because D's Channel note requires an oracle *"captured from a different program"*, and under the fallback a fixture would share an author with the parser. |
| **A29** | nits | the seam cell fragment *"sentence at `templates/modules/team-gated/python-security.md:3`"* | *"sentence at `templates/modules/team-gated/python-security.md:6` through `:7`"* — `:3` is the *"**Selected when:**"* line. Still paragraph-disjoint from `:13` and `:104`; the conclusion is unchanged. |
| **A30** | nits | the seam cell fragment *"This plan owns the **Exception 1 network-egress contract** (`:44`–`:53`)."* | *"This plan owns the **Exception 1 network-egress contract** (`:40` through `:57`, heading at `:40`; the Scope/blind-spots bullet E5 edits is `:52` through `:54`)."* Also recorded: `gate-claims-vs-enforcement` **has landed** its edit to this file (`2244eca`), in **Exception 2** (heading at `:97`). The line-disjoint prediction held; that co-claimant is discharged. |
| **A31** | nits | the Channel-note citation *"the idiom already in use at `bootstrap/tests/test_security_stack.py:638`"* | *"the idiom already in use at `bootstrap/tests/test_security_stack.py:643`"* — `:638` is the `def` line of `test_pip_audit_tool_error_is_degraded_not_findings`; the `monkeypatch` of `shutil.which` is at `:643`. |

**Replacement block for A7** — the residual partition, re-measured at HEAD
`e20b18e`, `as_of 2026-08-04`, over the **290** distribution records:

```
no direct_url.json at all:       47
dir_info present, NOT editable: 236   (conda-forge build artifacts)
archive_info only (neither
  dir_info nor vcs_info):          5   (ptyprocess, protobuf, scipy,
                                        numpy, scikit-learn)
vcs_info:                          0
dir_info EDITABLE:                 2   (modflow_tools, lhm-frontend)
                                ----
                                 290   partition closes
```

The 236 sub-buckets: `file:///home/conda/feedstock_root/build_artifacts/…` **189**,
`file:///Users/runner/miniforge3/conda-bld/…` **46**, and
`jsonschema-specifications` at `file:///tmp/tmptzik3dqa/src` **1**.

**The conclusion is unchanged in direction and stronger in degree.** All five
`archive_info` records carry a **`file://`** URL into a conda build tree, so they
too satisfy *"installed from a local path"* read literally. **The literal predicate
admits 241 public packages, not 236.** `editable-or-vcs` rejects all 241 and yields
exactly **2**. The interpretive step this plan flags for strike is therefore more
necessary than the plan's own text argues, and the fallback if it is struck is
unchanged: **ship no baseline in v1**, not the literal predicate.

### What this Response does *not* change

* **The Decision is not reopened.** No finding required it, and I did not use one as
  cover to revisit scope.
* **The residual-predicate question is not settled.** Whether `editable-or-vcs` is
  faithful execution or a redesign remains the Maintainer's call, exactly as the plan
  and the Internal reviewer both left it. This Response only sharpens the measurement
  underneath it: **241**, not 236.
* **The Chunk C tier change (5 → 20) is not settled.** Still offered for strike, and
  [I1]'s prose corrections are contingent on it: if C2 is struck, C3a and C3b are
  struck with it, and only C3's two false sentences remain to be corrected.
* **The decode-policy divergence is not settled.** Recorded as a cross-scope
  question, not absorbed.
* **No test was written and no perturbation was run.** Every amendment above is a
  change to the *plan*. [I6], [I7] and [I10] remain analytic findings about declared
  perturbations; none has been observed red.

### Clearance — stated explicitly

**This Response does NOT clear the plan to implement.**

What it discharges: the Internal round is answered, all ten findings have a
disposition, and every acceptance has mechanical residue in the table above.

What remains, and it is the gate:

1. **`required(External, security lens)` is UNMET.** No External review has landed.
   The plan requires a `### Plan review -- <reviewer> -- YYYY-MM-DD` sub-heading from
   a **different agent type or a human**; the tree contains only an Internal
   same-type `##` section and this author Response. Two independent triggers keep it
   live — the proposal's Decision, and `AGENTS.md` > *High-risk surfaces*. **No
   implementation commit lands before that sub-heading is in the tree.** This
   Response is written by the plan's **author**, and is structurally the least
   qualified artifact in the tree to discharge an independence requirement.
2. **Three Maintainer calls are open**, all flagged, none absorbed: the residual
   predicate narrowing; the Chunk C tier change; and — new from [I5] — the
   cross-scope decode-policy divergence with `security-verification-activation`.
3. **Maintainer fence 3 stands.** Chunk 0's network fetch is unapproved and
   unattempted.

### For the External reviewer

Three things changed under this Response that alter what you would be reading:

* **Do not reproduce the plan's suite, AST-total or `check_cairn` figures as
  written** — all three are superseded by A1/A2, A4/A5 and A6. The live tree is green
  at **1790 passed, 0 failed**; the AST baseline is **173** entries; `check_cairn`
  scans **195** files. The plan's *three-kind* delta claim (161, empty) is unaffected
  and still correct.
* **The residual measurement now closes at 290 across five buckets**, and the literal
  predicate admits **241**. Reproduce that before judging the plan's question 1; it is
  a stronger version of the argument the plan makes, not a weaker one.
* **[I4] is a security defect this plan would *introduce*.** It is now dispositioned
  (A11, A12, A13) but not implemented, and it is the finding worth attacking hardest:
  the module has **no** broad exception handler, so an unguarded parent-side JSON read
  exits **1** into the component code space the exit table promises the aggregate
  never uses.

### Figure correction -- Claude -- 2026-08-04

**Model**: Claude Opus 5 (`claude-opus-5`). **Standing**: a *measurement* record
appended to the Response above. It re-litigates **no disposition** — every finding
stays accepted or declined exactly as the Response left it — and it overturns no
amendment's conclusion. It corrects figures, and nothing else.

**Two provenance facts, stated before any number, because they bound what this
section is entitled to claim.**

1. I was directed to a plan file named 147.md under dev/plans/. **No such file
   exists.** 147 is a *figure* in this plan, not a stem. I identified this plan as
   the subject from that figure plus the described shape — a Response carrying
   re-measurements and a binding *Amendments in force* table an implementing agent
   would act on. That inference is strong, but it *is* an inference, and it is
   recorded here rather than hidden behind the result.
2. **The audit's body never reached me.** I was told an audit disputed specific
   figures and that its text was included in full; what arrived was a single
   character. I therefore could not compare against the auditor's numbers, and
   **nothing below adopts one.** I re-measured every figure this Response asserts,
   from scratch, and let my own measurement stand alone. Where this section says a
   figure is correct, that is *my run* saying so — not the Response, and not the
   auditor.

**Conditions.** `/Users/kendal30/conda_envs/lhm/bin/python3.13` (CPython 3.13.13),
`PYTHONDONTWRITEBYTECODE=1`, `as_of 2026-08-04`, at HEAD **`83b910c`** — **43
commits** past the Response's `e20b18e`. Sibling agents were committing *during* the
run (HEAD reached `758448a` before this section was written); both volatile figures
were re-checked at that later HEAD and were unchanged. The working tree carried one
uncommitted sibling file, `bootstrap/tests/test_transition_lint.py` (+116 lines, **0**
new `def test_`, **0** new parametrize cases), so it contributes nothing to the suite
count. I modified no source file and ran no network action.

#### The result: every figure reproduces. Two are stale, none is wrong.

| Figure | Response claims | I measured | |
|---|---|---|---|
| Suite | 1790 passed / 0 failed / 3 warnings | **1956 passed / 0 failed / 3 warnings**, 277.85 s, exit 0 | **stale** |
| `check_cairn` Markdown files | 195 | **191** | **stale** |
| `check_cairn` external links | 68 | 68 | exact |
| AST baseline total entries | 173 | 173 | exact |
| AST by-kind | `Assign 53 / ClassDef 10 / FunctionDef 98 = 161` | identical | exact |
| AST tail | `Docstring 1, Expr 1, If 1, If#2 1, Import 8`, no `Try` | identical | exact |
| conda records / unique | 394 / 391 | 394 / 391 | exact |
| `conda-meta` entries | 396 entries, 394 JSON | 396 / 394 | exact |
| Python dist records / unique | 290 / 288 | 290 / 288 | exact |
| intersection | 244 | 244 | exact |
| **conda-only** | **147** | **147** | exact |
| Python-only / union | 44 / 435 | 44 / 435 | exact |
| Five-bucket partition | 47 / 236 / 5 / 0 / 2 = 290 | identical, closes at 290 | exact |
| 236 sub-buckets | 189 / 46 / 1 | identical | exact |
| `archive_info` records | 5, all `file://` | 5, all `file://` into conda build trees | exact |
| `editable-or-vcs` yield | 2 | 2 | exact |
| Literal predicate | 241 *public* | 241 public (243 counting the 2 editable) | exact — see note |
| `scaffold.py --manifest` | 96 lines = 95 data rows | 96 / 95 | exact |
| `_CORE_MAPPINGS` digest | `c74e6013783bf4fe` | identical | exact |
| `_MODULE_MAPPINGS` digest | `26957a8924042a0a` | identical | exact |
| `_SKILLS_MAPPINGS` digest | `8ec105a84b5e65bf` | identical | exact |
| `frozen_files` entries | 164 | 164 | exact |
| Orchestrator pinned hash | `04cedaa2…d1f6f` | identical, character-for-character | exact |
| Frozen / not-frozen probes | stack frozen; the two docs not | identical | exact |
| Bandit (1.9.4) on orchestrator | `errors: []`, LOW `B404` 1 + `B603` 1, 0 MEDIUM+ | identical | exact |
| `claim_check.py` on this plan | OK, exit 0, 2 exemptions | OK, exit 0, 2 exemptions | exact |
| Every line citation carried by an amendment | as stated | all resolve (see below) | exact |

Commands, in the order run:

```
python -m pytest bootstrap/tests                     -> 1956 passed, 3 warnings, 277.85s, exit 0
python scripts/check_cairn.py                        -> 191 Markdown file(s); 68 external link(s)
python scripts/claim_check.py dev/plans/dependency-advisory-coverage.md   -> OK, exit 0
python -m bandit -f json templates/modules/team-gated/run_security_audit.py
json.load(bootstrap/tests/fixtures/scaffold_ast_baseline.json)   -> 173 entries; Counter by kind
json.load(bootstrap/tests/fixtures/gate_manifest.json)           -> len(frozen_files) == 164
importlib.metadata + $CONDA_PREFIX/conda-meta walk               -> the inventory and bucket figures
```

#### The two stale figures — and why neither is an error

Both were **correct at the commit the Response names**, and I verified that rather
than assuming it.

**(1) The suite: 1790 → 1956.** The Response measured at `e20b18e`; 43 sibling
commits have since landed, most of them test-bearing (the `transition-lint` chunks
among them). The uncommitted working-tree file adds no tests, so the entire +166 is
committed sibling work. **A1's figure is superseded to 1956; A1 itself stands** — its
conclusion is *"the instruction to re-take at implementation is unchanged and now
doubly warranted,"* which this measurement makes triply so. **A2 and A3 are
untouched**: both are about the *attribution split* between inherited and
attributable red, and 0 failed at both commits.

**(2) `check_cairn`: 195 → 191.** I did not take this on faith either way. I replayed
`link_check.filter_sources`' path rules over `git ls-tree -r` at each commit:

```
e20b18e: tracked .md = 249, scanned (filtered) = 195     <- the Response's figure, confirmed
a9bc372: tracked .md = 251, scanned (filtered) = 195
2ec7ca4: tracked .md = 252, scanned (filtered) = 191
83b910c: tracked .md = 252, scanned (filtered) = 191     <- and at the later HEAD 758448a
```

The drop is the **five archive moves** (`a9bc372`, `89a8f1f`, `e59f9d4`, `8595274`,
`640864e`): `filter_sources` excludes `dev/**/archive/` as a *source*, so archiving a
plan removes it from the scan set. **195 was right; 191 is right now. A6's figure is
superseded to 191; A6 stands.** The external-link half (68) reproduced at both.

One consequence A6 should carry: **its retained hedge — *"the count may only grow"* —
is now falsified by measurement.** The count *shrank*, by an ordinary archive
operation, and will shrink again at the next archive. An acceptance criterion resting
on a monotonicity that does not hold is a criterion that will go spuriously red. The
hedge should read *"the count moves in both directions; re-measure, do not compare."*
This corrects the *evidence* under A6, not its disposition.

#### The one place my raw number differs — a scope question, not a discrepancy

The Response asserts *"the literal predicate admits **241**, not 236."* Counting every
distribution installed from a local path, I get **243**: 236 non-editable `dir_info` +
5 `archive_info`-with-`file://` + **2** editable. The 241 excludes the 2 editable
(`modflow_tools`, `lhm-frontend`). That exclusion is **correct as worded**: the claim
is scoped to *"241 **public** packages,"* and those 2 are the maintainer's own local
projects, not public packages. The Response's very next clause — *"`editable-or-vcs`
rejects all 241 and yields exactly **2**"* — requires the two sets to be disjoint, and
they are. **241 is right; A10 stands unchanged.** I record 243 only so a later reader
who counts local-path installs without the public/private qualifier is not left
thinking the record is broken.

#### Citations carried by amendments — all resolve

Spot-checked at `83b910c` because these are what an implementing agent edits against.
**A29**: `templates/modules/team-gated/python-security.md:3` is indeed the
*"**Selected when:**"* line, and `:6`–`:7` the sentence that replaces it. **A30**: all
four land in `bootstrap/DEPENDENCY_BUDGET.md` — `:40` *is* the
*"### Network-egress contract (pip-audit)"* heading, `:52`–`:54` *is* the Scope /
blind-spots bullet E5 edits, `:97` *is* the *"## Exception 2"* heading. (I first
checked these against `python-security.md` and they failed; the seam cell is about
`DEPENDENCY_BUDGET.md`. Recorded so the next reader does not repeat the error.)
**A31**: `bootstrap/tests/test_security_stack.py:638` is the `def` line and `:643` the
`shutil.which` monkeypatch. **A11/A12/A14/A15/A16/A22** all resolve in
`templates/modules/team-gated/run_security_audit.py` — `:124` is the
`json.JSONDecodeError`-guarded lockfile read, `:391` the
`CAIRN_PIP_AUDIT_ALLOW_NETWORK` sentence, `:436` the argv-only egress read, `:479` the
`max` over tiers, `:42`–`:46` the exit-`5` bullet. A14's *"the token appears in no
other shipped file"* holds: outside `dev/`, `:391` is the only hit. **A17, A18, A19,
A27** resolve in the three sibling plans and the source proposal at both `e20b18e`
and HEAD — those siblings appended rather than edited, so their line numbers held.
`templates/modules/team-gated/python-security.md` and
`templates/modules/team-gated/run_security_audit.py` are **byte-identical** to
`e20b18e`.

*Nit, non-load-bearing:* A19 describes the sibling as mirroring the `_AGG_*` constants
at `:75` through `:78`; the sibling's own text cites `:76-78`, and `:75` is
`_AGG_CLEAN = 0`, which it does not mirror. A19's conclusion — the contingency is not
live at A3 — is unaffected.

#### Amendment dispositions

**No amendment is withdrawn.** The test is whether a conclusion *depended* on a figure
that moved; none did.

* **A1 — in force, figure superseded** (1790 → **1956**). Conclusion was already
  "re-take at implementation."
* **A6 — in force, figure superseded** (195 → **191**), plus the monotonicity hedge
  corrected above. Conclusion — the criterion is still satisfiable — survives.
* **A4, A5, A7, A8, A9, A10, A12, A29, A30, A31 — in force, figures confirmed
  exactly.** A4/A5 in particular: `161` and the empty declared delta both reproduce,
  so this plan's load-bearing AST claim is untouched.
* **A2, A3, A11, A13, A14, A15, A16, A17, A18, A19, A20–A28 — in force, unaffected**;
  these carry dispositions and citations rather than measured counts, and every
  citation resolves.

#### The finding under the findings

Both stale figures carry `as_of 2026-08-04` — **and so does this correction.** The
tree moved 43 commits *inside a single calendar day*, so a date stamp cannot
discriminate between a fresh figure and a stale one. The commit SHA can, and the
Response was right to name `e20b18e`; that is the only reason I could establish that
195 was correct rather than merely different. **Recommendation for the External
reviewer and the implementer: treat `as_of <date>` on a fast-moving tree as
decorative, and read the SHA.** The two figures here are volatile by nature — a suite
count and a file count — and both should be re-taken at implementation rather than
compared to any number in this document, including mine.
