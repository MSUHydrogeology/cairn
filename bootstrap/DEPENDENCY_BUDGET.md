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
  egress, and the lookup **does not run at all** — the pass returns before
  pip-audit is invoked, so nothing is checked, not even against a local cache.
* **Opt-in.** `--allow-network` enables the remote lookup. Only package
  **names + versions** are sent to the **pinned** vulnerability service named
  in the orchestrator's fixed argument vector — never repository source,
  scientific data, credentials, or other IP. The tool runs with a
  closed-allowlist child environment, so `--allow-network` authorizes *that
  documented service* rather than whatever an environment variable points at.
* **Fail-closed reporting.** A denied / offline / failed lookup is reported
  **unavailable, not clean**; so is a coverage set the run could not establish.
  A clean result from this leg requires zero `UNKNOWN` dispositions.
* **Scope / blind spots.** pip-audit audits the **active interpreter's Python
  distributions only**. Conda-managed and locked-but-not-installed dependencies
  are outside that scope, and on Cairn's own canonical environment the gap is
  **147 of 391 unique conda-installed packages (37.6%), `as_of 2026-08-04`** —
  not an edge case. The orchestrator counts and reports them as *not audited*;
  it never looks any of them up. Closing that gap is tracked as a deferred
  follow-up, not by this module.
* **Finding policy.** A pip-audit vulnerability finding is **blocking** — it
  fails the orchestrator aggregate at the FINDINGS tier (`10`), like a bandit
  finding. (Only the content-scan injection pass is advisory; a CVE is not.)

### Audit-evidence contract (tool environment)

The orchestrator records the **active interpreter** (`sys.executable`) and the
repo root as audit evidence, and runs every tool with a trusted subprocess
boundary: `shell=False`, a fixed argument vector, a `--` terminator before file
arguments (with refusal of option-shaped paths), resolved + contained targets,
and a neutral working directory. The child environment is a **closed
allowlist**, not a denylist, so a variable nobody has heard of cannot steer a
tool; the boundary also imposes a timeout, captures output as bounded bytes
with an explicit decode policy, and escapes control characters before rendering
so tool output cannot forge a report line. Any of those failing makes the pass
**degraded**, never clean. The audit is only as trustworthy as the
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

## Exception 3 — `portable-security-sweeps`: an **external-tool adapter**

A different *category* from Exceptions 1 and 2, not a longer list of the same
kind. Exception 1 admits Python **packages** the scaffold installs into the
adopter's environment; Exception 2 admits a **dev-only** package. This admits a
**host executable the scaffold never installs and never runs** — the dependency
is acquired by the adopter, out of band, and the scaffold's only relationship to
it is that an installed script may later invoke it.

Four things it must state, each checkable:

* **What is assumed installed.** **Gitleaks**, at a
  `(version, platform, architecture)` the admitted-artifact set records, and
  **Git**, which the runner invokes for its pre-execution configuration screen
  and which Gitleaks invokes **transitively** for the history leg. Two host
  executables, enumerated in
  `templates/modules/team-gated/run_portable_security_sweeps.py` as
  `TRUST_ROOTS` and in the module doctrine as an auditable list.
* **What happens when it is absent.** **INCOMPLETE, exit `5`, loudly** — never
  clean, and never a silent skip. This is the opposite posture from Exception 2,
  where an absent `vermin` *skips* the floor check and the skip reads as a pass.
  Verified by `test_absent_gitleaks_is_incomplete_not_clean` and
  `test_cairns_own_run_with_gitleaks_absent_is_incomplete` in
  `bootstrap/tests/test_portable_security_sweeps.py`, run by a person typing
  `python -m pytest bootstrap/tests` — **Cairn has no CI**, so nothing runs them
  automatically.
* **Why this is not a new dependency.** The scaffold **installs no scanner and
  executes none during installation** — doing so would move an executable trust
  root into the installer, which the module refuses by design. The shipped
  runtime stays **standard-library-only**: the runner imports nothing outside
  the standard library. The tool is an adopter-selected **dev/CI** dependency
  acquired only by selecting a team-gated, opt-in module that no preset selects.
* **No network path, and this is where it differs from Exception 1.** Exception
  1's `pip-audit` has an egress path (opt-in). This adapter has **none**: there
  is no `--allow-network`, no remote-data path and no advisory cache, and the
  child environment drops every inherited proxy variable by building from an
  allowlist. Re-introducing egress would be a new Decision, not a flag.

**What Cairn itself took on.** Under the accepting Decision's Condition 2, Cairn
installs and runs this module on its own tree, so **Cairn now carries Gitleaks
as a dev/CI tool of its own**. That does **not** change the zero-dependency
contract for shipped runtime — both halves are true at once, and this is where
they become checkable. Measured `as_of 2026-08-05`: `gitleaks` is **not** on this
host's `PATH`, so Cairn's own first run reports aggregate **5** with the absent
binary named. An honest INCOMPLETE is the contract working.

**Licence disposition of the three shipped files**, stated rather than left for
the first `.json` under `templates/` to set an unexamined precedent:

| File | Family |
|---|---|
| `run_portable_security_sweeps.py` | **code — MIT**, SPDX header in the first four lines |
| `portable-security-sweeps.md` | **document template — CC BY 4.0** |
| `portable_security_policy.json` | **code — MIT.** A data asset with no comment syntax, so it carries **no header**; it is a machine-read policy input to an MIT script, not prose. |

## No exception — `api-access-security` and `web-hosting-security`

**This section is not Exception 4.** It is here so the ledger records a
capability family that *looks* like it should need an exception and does not, and
so a later reader cannot mistake the tools named below for admitted
dependencies.

The two network-security capabilities install six Python sources — two facades
and one four-member `_security_net` engine per capability — and **v1 of both is
standard-library-only**. The complete import set across all six, measured rather
than summarized: `argparse`, `hashlib`, `hmac`, `importlib.util`, `ipaddress`,
`json`, `os`, `pathlib`, `re`, `secrets`, `shutil`, `socket`, `ssl`, `sys`,
`tempfile`, `urllib.parse`. Nothing is installed into the adopter's
environment, nothing is resolved from `PATH`, and no host executable is invoked
— so unlike Exception 3 there is no external trust root to enumerate, and
**Rule 10 of [`SAFETY.md`](SAFETY.md) does not attach to these modules.**

What *is* new is network egress from an installed runner, which is a safety
boundary rather than a dependency: see
[`SAFETY.md`](SAFETY.md) > *Rule 11*. A dependency budget and an egress boundary
are different ledgers, and this record deliberately keeps them apart.

**The eight tools these modules name are not dependencies of any kind.** Each is
either a recommended companion the adopter may adopt on their own, a deferred
adapter, or a deliberate exclusion — and none is installed, imported, resolved,
or executed by anything Cairn ships:

| Tool | Named in | Status |
|---|---|---|
| Schemathesis | `api-access-security.md` | recommended companion for contract/authentication testing — **adopter's own choice, not installed** |
| OPA, Cedar, OpenFGA | `api-access-security.md` | architectural choices the project owns; the module executes a *declared* matrix and implements no authorization model |
| ZAP (API scan) | `api-access-security.md` | **excluded** — it is an active scanner; both capabilities' remote legs are passive |
| `testssl.sh` | `web-hosting-security.md` | **deferred adapter** — a better local TLS analyser, deferred rather than shipped |
| MDN HTTP Observatory | `web-hosting-security.md` | **deferred adapter**, kept as a documented extension |
| Trivy | `web-hosting-security.md` | stays with `portable-security-sweeps`, which already owns the external-tool boundary (Exception 3) |

Shipping any one of them as an *adapter* would make it an external-tool
dependency of Exception 3's category — an executable the scaffold neither
installs nor ships, whose `PATH` resolution is execution authority. That would
be a new declared exception and a Security Review, not a flag.

**Licence disposition of the ten shipped template sources** (six `.py`, two
`.md`, two `.json` — installed to fourteen destinations, because one engine tree
is installed once per capability), on the same footing as Exception 3's table:

| File | Family |
|---|---|
| `api_access_security.py`, `web_hosting_security.py`, and the four `_security_net` members | **code — MIT**, SPDX header in the first four lines |
| `api-access-security.md`, `web-hosting-security.md` | **document template — CC BY 4.0** |
| `api_access_policy_stub.json`, `web_hosting_policy_stub.json` | **code — MIT.** Data assets with no comment syntax, so they carry **no header** — machine-read policy inputs to MIT scripts, not prose. |

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
