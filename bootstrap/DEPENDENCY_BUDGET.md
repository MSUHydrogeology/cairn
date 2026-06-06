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

## Out of scope (this record)

Third-party **binary** provenance (downloaded solver / compiler executables and
their behavior) is a separate future capability, not covered by this exception:
the adopted-executable gate verifies adopted Python *sources* against the
lockfile only.
