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
  (dependency CVE check) — invoked as subprocesses by
  `scripts/run_security_audit.py`.
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
  dependencies are documented blind spots, and its findings are advisory.

### Audit-evidence contract (tool environment)

The orchestrator records the **active interpreter** (`sys.executable`) and the
repo root as audit evidence, and runs every tool with a trusted subprocess
boundary: `shell=False`, a fixed argument vector, a `--` terminator before file
arguments (with refusal of option-shaped paths), resolved + contained targets,
and a neutral working directory. The audit is only as trustworthy as the
interpreter/tool environment it ran in, so that environment is part of the
record.

## Posture-change visibility (a high-signal review surface)

The security apparatus's **policy inputs** — the URL allowlist, the
reviewed-residual baseline, the audited-roots manifest, and the lockfile
records of every apparatus file — plus **module removal** are high-signal
review surfaces. A change that weakens the posture (removing a security module,
narrowing the audited roots, blessing a new residual) must be **visible**, not
silently normalized:

* The orchestrator's **integrity preflight** verifies every apparatus + policy
  file against its lockfile record before any pass runs. An edit to a policy
  input that has not been deliberately re-recorded (via `upgrade --finalize`)
  makes the preflight **fail closed** — a weakened apparatus cannot quietly
  self-audit and report results.
* Treat any diff to these files, or any module-removal, as a deliberate
  posture change requiring review and explicit re-authorization — not a routine
  edit. The integrity machinery surfaces it; the human ratifies it.

## Out of scope (this record)

Third-party **binary** provenance (downloaded solver / compiler executables and
their behavior) is a separate future capability, not covered by this exception:
the adopted-executable gate verifies adopted Python *sources* against the
lockfile only.
