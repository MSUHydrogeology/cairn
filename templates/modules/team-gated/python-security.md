# Module: python-security

**Selected when:** the adopter ships **Python** and wants a self-audit gate
over their own package — a dependency-vulnerability check, a static-analysis
contract, and a source-integrity scan of the Python files agents adopt.
**Token-gated**: selected automatically when the adopter declares a filled
`python_package` token, and never installed for a non-Python adopter.

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

### Declared scope — what the dependency check covers

The dependency leg audits the **Python distributions discoverable in the
audited environment**, and nothing else. It does **not** audit conda-managed
native packages, system packages installed by the OS, or libraries vendored or
statically linked into a wheel. This is stated here, where you decide whether
to install the module, rather than in a report you read after you have already
started trusting it.

The gap is not a rounding error. A scientific conda environment routinely
carries substantially more packages than the Python distributions the tool can
enumerate, and the excess is concentrated in exactly the **native** layer —
compression, cryptography, image, and numerics libraries — where a
vulnerability is most likely to be remotely reachable. Those packages are
outside this module's scope in v1. The orchestrator **counts** them and prints
the number as *not audited*, so the gap is a figure you can see rather than a
caveat you have to remember; it never looks any of them up, and the report says
so.

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
  run, or could not establish what it covered** — content-security not
  installed (injection NOT APPLICABLE), pip-audit network egress off **while
  pip-audit itself is present** (lookup UNAVAILABLE), or a dependency-coverage
  set the run could not establish (UNKNOWN). Distinct from clean so automation
  cannot read "a pass did not run" as "scan ran clean"; install / enable the
  pass (or deliberately narrow scope) for a clean `0`.
* **`10`** — FINDINGS: bandit or pip-audit found issues. Dominates incomplete.
* **`20`** — DEGRADED / UNAVAILABLE / TAMPER: a pass could not be trusted to
  run — the integrity preflight failed, `python_package` is missing/invalid, a
  selected content-scan returned scan-failure or stale, an adopted source was
  tampered, a **required tool was absent** (pip-audit included), a tool timed
  out / flooded its output / emitted undecodable bytes, or a tool hit a
  usage/network error. Dominates findings.

Every blocking reason a pass finds is reported, not only the first, and the
pass's tier is the **worst applicable** reason. So a run with pip-audit
**absent** *and* egress off reports both and exits `20`, not `5`: an absent
required tool is degraded, and degraded dominates incomplete.

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

pip-audit audits the **active interpreter's Python distributions only** — see
*Declared scope* above for what that leaves out. A pip-audit vulnerability
finding is **blocking** — it fails the aggregate at the FINDINGS tier (`10`),
like a bandit finding; only the **content-scan** pass is advisory. **Network
egress is off by default**: an unconfigured run does not contact a remote
service, and the lookup **does not run at all** — the pass returns before
pip-audit is invoked, so nothing is checked, not even against a local cache.
Re-run with `--allow-network` to enable the remote CVE lookup — only then are
package **names + versions** (never source, data, or credentials) sent to the
**pinned** vulnerability service named in the orchestrator's fixed argument
vector. `--allow-network` authorizes *that documented service*, never one
selected by an environment variable: the tool runs with a closed-allowlist
child environment, so interpreter, service, endpoint, proxy and trust store are
argv decisions, not ambient ones. A variable outside the allowlist reaches the
tool only through the explicit `--pass-env NAME` opt-in, and every name passed
that way is **printed in the report**.

An egress-off run **with pip-audit present** reports the pass **UNAVAILABLE
(incomplete coverage → aggregate `5`), not clean**. If pip-audit is **absent**,
that is a required tool that was absent → **degraded (`20`)**, and it dominates:
every blocking reason is reported, and the tier is the worst applicable one, not
the first found. A tool / usage / network error with egress on is likewise
**degraded** (`20`), never reported as vulnerabilities — as is a tool that
timed out, flooded its output, or emitted bytes that could not be decoded.

### Coverage contract — what CLEAN means for this leg

Every distribution the tool reported carries a **disposition** from this
vocabulary of three:

* **`SCANNED`** — the pinned advisory sources were queried and returned no
  vulnerabilities for it. Read it exactly that narrowly: it does **not**
  establish that those sources carry a record for the distribution at all.
* **`NO-MATCH-IN-PINNED-SOURCES`** — the sources named in the report hold no
  record for it. This is **accepted non-coverage, not evidence of safety**: it
  states what those sources contain at that version, and asserts nothing about
  the world. It is reported alongside a clean result and never folded into it.
  **It is not separately observable at the pinned tool version**, because the
  tool's report gives an empty vulnerability list both for a distribution its
  sources have a record for and for one they do not. Rather than print a
  structural `0` — which would read as "every distribution had a record", the
  universal negative this vocabulary exists to avoid — the run says so in as
  many words. Nothing about the tier changes: only `UNKNOWN` ever gated the
  verdict.
* **`UNKNOWN`** — the disposition could not be established at all: the tool's
  enumeration could not be read, its output could not be parsed, or a
  distribution's own metadata could not be read.

**A clean `0` from this leg requires zero `UNKNOWN`.** The denominator is the
set the **tool itself reported** enumerating — the orchestrator does not count
distributions on its own and assume the tool saw the same ones, because that is
an assumption rather than evidence. Where the enumeration cannot be
established, the leg reports UNKNOWN and contributes **incomplete (`5`)** — it
never guesses in order to reach clean. Findings still dominate incomplete, and
degraded dominates both.

**Reading that enumeration depends on a tool-version-specific report shape**,
established by measurement against one pinned pip-audit version rather than
assumed from a published contract. If you upgrade pip-audit and its report shape
changes, the leg **fails closed** — UNKNOWN, incomplete, loud — rather than
quietly counting nothing; re-establishing the shape against the new version is
what clears it.

**v1 stores no residual baseline.** Locally built distributions (editable
installs and VCS checkouts, identified mechanically from PEP 610
`direct_url.json` rather than by assertion) are classified and reported per
run. Nothing is committed: a baseline derived from a single mutable local
environment would make an unrepresentative local classification look like a
portable security fact.

### Composition with content-security

The content-injection pass runs **only when the `content-security` module is
also installed**, and reports as *absent* (NOT APPLICABLE), never silently
clean, when it is not. Install both modules for the full stack.
