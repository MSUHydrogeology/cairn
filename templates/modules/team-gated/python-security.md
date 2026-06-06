# Module: python-security

**Selected when:** the adopter ships **Python** and wants a self-audit gate
over their own package — a dependency-vulnerability check, a static-analysis
contract, and a source-integrity scan of the Python files agents adopt.
Team-gated and **opt-in**: never default-on, and never installed for a
non-Python adopter.

**Adds to:** the adopter's `dev/modules/` doctrine set (this file), plus the
Python gate stack the module installs. The gate scans the adopter's own
package, named by the required `python_package` token (see below).

> **Stub note (Cairn-internal, removed before the module is complete).** This
> doctrine file is the Chunk-B0 stub of the security-apparatus-enrichment
> arc: it registers the module and its required `python_package` token so the
> selected-module required-token preflight has a real module to gate. The
> runnable gate stack — the `run_security_audit` orchestrator, the templated
> `bandit` contract gate, and the adopted-executable source gate — lands in a
> later chunk. Until then this module installs doctrine only.

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

## Reference implementation

Enabling this module installs the Python gate stack into the adopter tree
(vendor-neutral; the gates run against the package named by `python_package`).
The stack composes the dependency-vulnerability check and the static-analysis
contract with the content-injection pass **only when the `content-security`
module is also installed** — and reports that pass as *absent*, never as
silently clean, when it is not. The gate details and their exact pass/fail
contract are documented with the runnable stack.
