# Module: python-security

**Selected when:** the adopter ships **Python** and wants a self-audit gate
over their own package — a dependency-vulnerability check, a static-analysis
contract, and a source-integrity scan of the Python files agents adopt.
Team-gated and **opt-in**: never default-on, and never installed for a
non-Python adopter.

**Adds to:** the adopter's `dev/modules/` doctrine set (this file), plus the
Python gate stack the module installs. The gate scans the adopter's own
package, named by the required `python_package` token (see below).

## What this module is — and is not (v1 scope)

**v1 is a self-audit drift tripwire on a *trusted* tree**, not a reviewer for
untrusted code. It runs in the adopter's **own** CI / dev loop over the
adopter's **own** committed tree, to catch accidental drift and
content-injection that slipped past human review. The apparatus *and its
policy inputs* — the gate scripts, any allowlist or residual baseline — are
**trusted input**: committed, reviewed-as-code, and integrity-covered by the
lockfile.

**v1 is explicitly NOT** a containment boundary or reviewer for *untrusted
code that can modify the apparatus itself* — a hostile pull request that swaps
a gate script, blesses a finding, or narrows what is scanned and then reports
success. **Do not wire this module's gates into untrusted-PR / fork CI**: a
gate run from an attacker's checkout executes the attacker's version of the
gate. That trusted-runner-against-untrusted-candidate mode is out of v1 scope.

A clean run is **a tripwire, not a proof**: it is evidence that the known
patterns did not fire over the scanned set, not evidence that the adopter's
Python or its dependencies are safe. Novel issues and anything outside the
scanned set remain human-review work.

## Required configuration

This module requires the **`python_package`** token: the repo-relative path of
the Python package the gate scans (for example, a single top-level package
directory). It has no safe default — the scaffold cannot guess an adopter's
package — so selecting `python-security` without supplying `python_package`
**fails the install closed before any file is written**. Supply it in the
profile alongside the module selection.

## The orchestrator (`run_security_audit.py`)

Enabling this module installs a standalone, **standard-library-only**
orchestrator. Run it with no arguments — no pytest, no dev dependency required
to invoke it:

> `python scripts/run_security_audit.py`

It composes the adopter's self-audit passes in order:

1. **Integrity preflight (SR-1).** Before any pass, it verifies its own
   apparatus and policy inputs against the install lockfile. A run from a tree
   whose scanner / runner / allowlist / baseline / roots-manifest / gate
   scripts are not lockfile-clean **refuses** rather than runs — the one guard
   that makes "self-audit of a trusted tree" enforceable, not just claimed.
2. **Content-scan** — the content-security runner, **only when content-security
   is an installed module** (consulted from the lockfile roster, not a
   filesystem guess). Not installed → a loud **NOT APPLICABLE** line, never a
   silent clean. Selected but missing/tampered → fail closed.
3. **bandit** over the adopter's `python_package`.
4. **Adopted-executable source gate** — verifies every `.py` this install
   adopted is byte-for-byte its vetted, lockfile-recorded source (an integrity
   gate, not a re-lint of Cairn's already-gated scripts). Binary provenance
   (downloaded solver / compiler executables) is **out of scope**.
5. **pip-audit** — dependency CVE check; see the egress note below.

### Exit contract

The orchestrator's aggregate exit uses a **distinct space** that never collides
with a component's own `0/1/2/3` (or a `127` missing-tool code); each
component's raw outcome is printed separately. Precedence is
degraded > findings > incomplete > clean:

* **`0`** — clean: **every applicable pass ran** and found nothing blocking
  (content-scan *advisory* findings may be present; they are printed and do not
  fail the aggregate).
* **`5`** — INCOMPLETE COVERAGE: no findings, but a **selected pass did not
  run** — content-security not installed (injection NOT APPLICABLE), or
  pip-audit network egress off (lookup UNAVAILABLE). Distinct from clean so
  automation cannot read "a pass did not run" as "scan ran clean"; install /
  enable the pass (or deliberately narrow scope) for a clean `0`.
* **`10`** — FINDINGS: bandit or pip-audit found issues. Dominates incomplete.
* **`20`** — DEGRADED / UNAVAILABLE / TAMPER: a pass could not be trusted to
  run — the integrity preflight failed, `python_package` is missing/invalid, a
  selected content-scan returned scan-failure or stale, an adopted source was
  tampered, or a tool hit a missing/usage/network error. Dominates findings.

A `NOT APPLICABLE` injection pass (content-security not installed) and an
egress-off `UNAVAILABLE` pip-audit are printed as their own lines and map to
`5` (incomplete) — never a silent clean `0`.

### `python_package` — single contained package (v1)

`python_package` is **one repo-relative package directory**. The orchestrator
validates it fail-closed: present, repo-relative (no `..` / absolute), **not the
repo root**, an existing directory, symlink-contained within the repo. Selecting
this module without a filled `python_package` **fails the install closed before
any write** (the required-token preflight). Multi-package layouts are a
documented **v2** limitation, not silently mis-scanned.

### pip-audit — network egress is opt-in

pip-audit audits the **active interpreter's pip-visible distributions only**;
conda-managed and locked-but-not-installed dependencies are documented blind
spots, and its findings are advisory. **Network egress is off by default**: an
unconfigured run does not contact a remote service. Re-run with
`--allow-network` to enable the remote CVE lookup — only then are package
**names + versions** (never source, data, or credentials) sent to pip-audit's
vulnerability service. An egress-off run reports the pass **UNAVAILABLE
(incomplete coverage → aggregate `5`), not clean**; a tool / usage / network
error with egress on is **degraded** (`20`), never reported as vulnerabilities.

### Composition with content-security

The content-injection pass runs **only when the `content-security` module is
also installed**, and reports as *absent* (NOT APPLICABLE), never silently
clean, when it is not. Install both modules for the full stack.
