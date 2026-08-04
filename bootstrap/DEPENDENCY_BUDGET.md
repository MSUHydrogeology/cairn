# The dependency-budget record

Cairn's tooling is **standard-library-only by default**: the scaffold engine,
the claim / link / content scanners, the lifecycle and work-intent tools all run
with no third-party dependency, so adopting Cairn never imposes a dependency on
an adopter's stack. That default is a deliberate constraint, not an accident —
it keeps the methodology stack-neutral.

This record is the **ledger of declared exceptions** to that default: the
places where a capability genuinely cannot be delivered stdlib-only, the
exception is named here, scoped narrowly, and capability-gated so only adopters
who opt in ever acquire the dependency. The full *dependency-budget doctrine*
(when an exception is justified, how the budget is governed) is deferred to a
strategy deliberation; this file establishes the **precedent** — the first
declared exception — that the doctrine will codify around.

## Exception 1 — `python-security`: `bandit` + `pip-audit`

* **Module:** `python-security` (team-gated, opt-in; never default-on, never
  installed for a non-Python adopter).
* **Executable dependencies:** `bandit` (static analysis) and `pip-audit`
  (dependency CVE check) — invoked as subprocesses by the orchestrator
  `run_security_audit.py` (installed in the adopter's `scripts/`).
* **Why the exception is justified:** a Python static-analysis gate and a
  dependency-CVE check cannot be reimplemented stdlib-only without rebuilding
  two mature tools. The value (a real Python self-audit gate) requires them.
* **Architectural rationale (framework Anchor 13 — the narrow-waist split):**
  the three-surface design keeps the dependency contained to the one surface
  that needs it. `security-review` (doctrine, language-neutral) and
  `content-security` (the stdlib injection apparatus) carry **no** runtime
  dependency; only `python-security` — explicitly Python, explicitly opt-in —
  does. The narrow waist is what lets the exception exist without taxing every
  adopter: a non-Python or stdlib-only adopter takes neither tool.
* **Capability gate:** the dependency is acquired only by installing
  `python-security`, and the module's required `python_package` token must be
  filled before any install write (the selected-module required-token
  preflight). A missing tool at run time is reported loudly (the pass is
  DEGRADED / unavailable), never silently skipped.

### Network-egress contract (pip-audit)

`pip-audit`'s vulnerability lookup is a **network-egress boundary**, disclosed
and constrained:

* **Default off.** An unconfigured `run_security_audit.py` run does **not**
  egress; pip-audit runs against its local cache only.
* **Opt-in.** `--allow-network` enables the remote lookup. Only package
  **names + versions** are sent to pip-audit's vulnerability service — never
  repository source, scientific data, credentials, or other IP.
* **Fail-closed reporting.** A denied / offline / failed lookup is reported
  **unavailable, not clean**.
* **Scope / blind spots.** pip-audit audits the **active interpreter's
  pip-visible distributions only**; conda-managed and locked-but-not-installed
  dependencies are documented blind spots.
* **Finding policy.** A pip-audit vulnerability finding is **blocking** — it
  fails the orchestrator aggregate at the FINDINGS tier (`10`), like a bandit
  finding. (Only the content-scan injection pass is advisory; a CVE is not.)

### Audit-evidence contract (tool environment)

The orchestrator records the **active interpreter** (`sys.executable`) and the
repo root as audit evidence, and runs every tool with a trusted subprocess
boundary: `shell=False`, a fixed argument vector, a `--` terminator before file
arguments (with refusal of option-shaped paths), resolved + contained targets,
and a neutral working directory. The audit is only as trustworthy as the
interpreter/tool environment it ran in, so that environment is part of the
record.

## Posture-change visibility — a human-review surface (v1 scope)

The security apparatus's **policy inputs** — the URL allowlist, the
reviewed-residual baseline, the audited-roots manifest, and the lockfile
records of every apparatus file — plus **module removal** are **high-signal
review surfaces**. A change that weakens the posture (removing a security
module, narrowing the audited roots, blessing a new residual) is a deliberate
posture change that must be **reviewed by a human** — it is not a routine edit.

**Scope honesty (v1).** v1 does **not** implement an automated posture-change
gate. The control is **detective + human**, not preventive-automated:

* The orchestrator's **integrity preflight** catches an **un-finalized** edit
  to any apparatus / policy file (its on-disk hash no longer matches the
  lockfile record) and **fails closed** — a tampered-but-not-re-recorded
  apparatus cannot self-audit. That is its guarantee.
* But once `upgrade --finalize` re-records the lockfile, the preflight accepts
  the new (possibly weaker) state — finalize advances the recorded hashes. The
  integrity preflight is therefore **not** posture-change detection: it does
  not compare against a prior authorized posture.
* So a **finalized** weakening (a removed module, a narrowed manifest, a newly
  blessed residual) is caught by **human review of the `upgrade --finalize`
  diff and the security-policy-file diffs**, not by an automated gate. Treat
  every such diff as requiring explicit review. *(An automated durable
  prior-posture / re-authorization comparison is a deliberate non-goal at v1 —
  it belongs to a later "untrusted-apparatus-change" capability, outside the v1
  self-audit-on-a-trusted-tree scope.)*

## Exception 2 — `vermin`: floor check (dev/test-only)

* **Scope:** **dev/test-only**. `vermin` is never in the adopter runtime path,
  never installed by the scaffold, and never a dependency of the scaffold
  engine itself. It runs only in Cairn's own test suite
  (`bootstrap/tests/test_python_floor.py`, run by
  `python -m pytest bootstrap/tests`) to assert that the engine's detected
  Python minimum does not exceed the declared floor. **That test skips — and
  so passes green — whenever no usable `vermin` executable is found on `PATH`
  or beside the running interpreter.**
* **Why the exception is justified:** accurately detecting a codebase's Python
  minimum version requires semantic analysis of the AST — not just syntax
  parsing — to identify stdlib APIs, type annotation forms, and language
  features by version. A stdlib-only equivalent would reproduce a large portion
  of `vermin`'s scope; `vermin` is a mature, well-maintained tool for exactly
  this purpose.
* **Why it is materially lighter than Exception 1:**
  * **No adopter impact.** Exception 1's tools (`bandit`, `pip-audit`) are
    opt-in but still recommended for Python adopters and installed into the
    adopter's `scripts/`. `vermin` is never installed into an adopter repo and
    never surfaces in adopter workflows.
  * **No runtime path.** Exception 1's tools run inside the scaffold's security
    orchestrator at audit time. `vermin` runs only in Cairn's own test suite.
  * **No network egress.** `vermin` is purely local static analysis; it sends
    nothing over the network.
* **Dev dependency home:** `bootstrap/requirements-dev.txt`. Install with
  `pip install -r bootstrap/requirements-dev.txt` to enable the floor check.
  The test skips gracefully when `vermin` is absent (using `pytest.mark.skipif`),
  so the main test suite runs cleanly without it.
* **Capability gate:** `vermin` is a dev tool; its absence does not degrade any
  adopter-facing capability. Absence causes the floor check test to be skipped
  and is reported as such.

## The canonical interpreter — Python 3.13.x

Every gate in this record assumes one interpreter. The gate manifest pins it
(`bootstrap/tests/fixtures/gate_manifest.json`, `interpreter.version`), and
running the suite under a different minor changes the results on an otherwise
identical tree.

Measured 2026-07-22, one tree, nothing differing between the two runs but the
interpreter:

| | Python 3.13.13 (canonical) | Python 3.12.9 |
|---|---|---|
| suite | 2 failed / 1435 passed / **0 skipped** | 2 failed / 1429 passed / 3 skipped |
| AST attestation | **3** real drifted symbols | *hundreds* of spurious mismatches |
| `bandit` (Exception 1) | present — the gate **runs** | absent — the gate silently **skips** |

Two independent causes. `ast.dump` structure varies across Python minors, so the
attestation reports phantom `CHANGED` symbols off-canon — the drift looks like a
logic change that never happened. And the dev-only tools this record admits
(`bandit`, `vermin`) live in the canonical environment, so elsewhere their gates
skip rather than fail, and a skip reads as a pass.

**If you assert a suite figure or a gate outcome, name the interpreter with it.**
Two honest agents on the same tree otherwise report different facts, each
correct about what they actually ran. That happened here: a published audit
finding — that the Bandit gate "runs nowhere" — was measured off-canon and had
to be corrected.

## Out of scope (this record)

Third-party **binary** provenance (downloaded solver / compiler executables and
their behavior) is a separate future capability, not covered by this exception:
the adopted-executable gate verifies adopted Python *sources* against the
lockfile only.
