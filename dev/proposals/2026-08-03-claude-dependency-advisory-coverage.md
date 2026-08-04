<!-- cairn-internal-ref-allow: doctrine/runtime-contract.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: scripts/run_security_audit.py -->
<!-- ^ ADOPTER-TREE DESTINATION path -- where the orchestrator lands in an installed
     target. It does not resolve in Cairn's source tree; the source of truth is
     templates/modules/team-gated/run_security_audit.py. Same directive and reason as
     default-security-stance and release-security-bar. -->

# The dependency-advisory leg does not know what it scanned — and it scans 62% of a conda environment

**Author**: Claude (Strategy)
**Model**: Claude Opus 5
**Date opened**: 2026-08-03
**Status**: reviewed
**Touches**: `templates/modules/team-gated/run_security_audit.py` (the pip-audit
pass and the shared `_run_tool` boundary), `templates/modules/team-gated/python-security.md`
(the module's scope and blind-spot statement), and `bootstrap/DEPENDENCY_BUDGET.md`
(the pip-audit scope paragraph, which understates the gap)
**Deliberately not touched**: which modules a preset selects (`default-security-stance`),
cross-language sweep composition (`portable-security-sweeps`), Bandit's file reach
(`scan-coverage`), the onboarding prose that overclaims (`gate-claims-vs-enforcement`),
and the aggregate exit-code space itself, which is correct and stays as-is
**Related**: `default-security-stance`, `release-security-bar` and
`portable-security-sweeps` all touch `run_security_audit.py`; **none claims the
pip-audit leg** — verified, zero hits for `pip-audit`/`pip_audit` across in-flight
proposals and plans. Findings **PS3** and **PS7** in the External review of
`portable-security-sweeps` are folded in here, as that review recommended
**Plan review**: `required(**External**, security lens)` — this is the shipped
security stack (`AGENTS.md` names it a Security Review trigger)

## Context

Cairn ships `python-security`: Bandit over source, pip-audit over dependencies.
The Bandit leg works. The dependency leg has a coverage problem it cannot
report, and a reporting problem that hides it.

This is a **defect repair**, not a new capability, in the sense that matters:
the module already claims to audit dependencies. The claim is what is wrong.

## Evidence

Measured on the canonical interpreter (`/Users/kendal30/conda_envs/lhm`,
Python 3.13.13), `as_of 2026-08-03`.

### The coverage gap

pip-audit enumerates the active interpreter's **Python distributions**. A conda
environment contains considerably more than that:

| | count |
|---|---|
| conda-installed packages (`conda-meta/*.json`) | **391** |
| visible to pip-audit | 244 |
| **invisible to pip-audit** | **147 (38%)** |
| — of those, native / system libraries | **82** |

The invisible set is not incidental. It is `krb5`, `freetype`, `icu`, `hdf5`,
`geos`, `libabseil`, `bzip2`, and the `aws-c-*` networking stack — the native
layer where advisories concentrate, and the layer a scientific Python
environment leans on hardest. A clean pip-audit result on this machine is a
statement about 62% of the environment, presented as a statement about the
environment.

`bootstrap/DEPENDENCY_BUDGET.md` records "conda-managed and
locked-but-not-installed dependencies are documented blind spots". That is true
and too gentle: it reads as an edge case, and it is 38% of the packages and most
of the native ones.

### The reporting defects

1. **The pass reports the first reason it cannot run, not every reason.**
   `run_security_audit.py` checks egress before installation:

   ```python
   if not allow_egress:
       return "egress-off-unavailable", _AGG_INCOMPLETE
   if shutil.which("pip-audit") is None and find_spec("pip_audit") is None:
       return "tool-absent", _AGG_DEGRADED
   ```

   pip-audit is **not installed** in this environment. A default run therefore
   reports INCOMPLETE citing egress, never mentioning the tool is absent; an
   operator who enables `--allow-network` expecting a scan gets DEGRADED
   instead. The report named a true fact and concealed an independent one.

2. **Nothing records which environment was audited.** The pass runs
   `[sys.executable, "-I", "-m", "pip_audit"]`, so it audits whichever
   interpreter invoked the orchestrator. This repository has two on `PATH`
   (canonical 3.13.13; a plain 3.12.9), and nothing pins or reports the choice.
   The same footgun the gate manifest guards against for the manifest producer
   is unguarded here.

3. **`_run_tool` has no timeout.** `subprocess.run(argv, cwd=neutral,
   shell=False, env=env, capture_output=True, text=True)` — a hung tool blocks
   indefinitely and is indistinguishable from a slow scan. (**PS7**.)

4. **Tool output is echoed unsanitized.** `_run_tool` prints `proc.stdout` and
   `proc.stderr` straight through. Scanner output embeds repository-controlled
   strings — filenames, matched lines — so a crafted filename carrying ANSI
   escapes or an embedded newline can forge report lines in the operator's
   terminal, which is the evidence for a security decision. (**PS3**.)

## Proposal

### Part 1 — the leg reports its own coverage (repair)

* **Report every blocking reason**, not the first. Check tool availability,
  egress disposition, and interpreter identity independently and print all
  three dispositions before the aggregate.
* **Print the denominator.** Report packages enumerated, packages resolved to an
  advisory record, and packages neither — so `clean` can never be read as
  `everything looked up`. A leg that cannot state its own coverage should not
  contribute a CLEAN.
* **Record the audited interpreter** (`sys.executable`, its version, and whether
  it matches the project's recorded interpreter) in the report; a mismatch is at
  minimum loud, and the plan should decide whether it refuses.
* **Soften nothing in the aggregate.** The 0/5/10/20 space and its precedence
  are correct and unchanged.

### Part 2 — conda coverage (the gap)

Bring the 147 invisible packages into the dependency leg. The mechanism is
**deliberately not decided here**, because I have not verified any candidate and
this proposal will not repeat the error of asserting a tool capability it did
not execute:

* **Trivy** is understood to carry a conda package analyzer over
  `conda-meta/*.json`. **Unverified.** If real, it is the cheapest path and
  `portable-security-sweeps` already proposes Trivy as an adapter.
* **OSV-Scanner** covers many ecosystems; whether conda-forge is among them, and
  whether conda-forge versions resolve against PyPI advisory records, is
  **unverified**.
* **Name/version mapping** from `conda-meta` to PyPI coordinates, feeding the
  existing pip-audit path. Homegrown and fragile at exactly the native packages
  that matter, since `krb5` and `openssl` have no PyPI record at all.

**The plan must establish the mechanism by execution before implementation** —
run each candidate against this environment, report how many of the 391 resolve,
and pick on measured coverage rather than documentation. A candidate that cannot
resolve the native layer does not close this gap and should be rejected for it.

The environment is favourable for this: all 391 packages come from a **single
channel** (conda-forge), and each `conda-meta` record carries `name`, `version`,
`channel`, `subdir`, `build`, `depends`, and `license`.

### Part 3 — the shared runner boundary (PS3, PS7)

* Add a **timeout** to `_run_tool`; a timeout is DEGRADED, never clean.
* **Sanitize adapter output before rendering** — strip or escape control
  characters, or render only parsed fields. Add a fixture with a hostile
  filename asserting the report cannot be forged.

Both improve the Bandit leg equally; both were raised in the `portable-security-sweeps`
review, which recommended PS7 be split out rather than ride that proposal.

### Documentation / doctrine surface

No doctrine change. `bootstrap/DEPENDENCY_BUDGET.md`'s pip-audit scope paragraph
gains the measured figure in place of "documented blind spots", and
`python-security.md` states what the leg does and does not cover. This is the
descriptive layer telling the truth about shipped behaviour, not a new rule.

## Alternatives considered

**Fold this into `portable-security-sweeps`.** That proposal owns cross-ecosystem
dependency advisories via OSV-Scanner, and conda is another ecosystem. Rejected
as the primary home: it is currently held on two blocking findings, and its
recommended v1 is Gitleaks-only — so routing a 38% coverage gap through it defers
the gap indefinitely. The two should coordinate: if that proposal's OSV or Trivy
adapter proves to cover conda, this proposal's Part 2 adopts it rather than
building a parallel path.

**Document the gap and stop.** Cheaper, and it is what `DEPENDENCY_BUDGET.md`
already does. Rejected: the module's output still contributes a CLEAN over 62% of
an environment, and a documented blind spot that the tool does not surface at run
time is a footnote, not a control.

**Drop the pip-audit leg.** Rejected. It genuinely covers the 244 pip-visible
distributions, and removing it would trade a partial control for none.

## Signals the change is wrong

* Coverage reporting proves impossible to compute cheaply, so every run pays a
  large cost to print a denominator. Recovery: report enumerated-vs-resolved
  counts only, and drop the per-package accounting.
* No candidate mechanism resolves the native layer at acceptable fidelity.
  Recovery: say so plainly in `python-security.md` and scope the module to
  Python distributions by name, rather than shipping a conda adapter that
  reports mostly `unknown`.
* Sanitizing output makes real findings harder to read. Recovery: sanitize only
  control characters and keep the text verbatim.
* The interpreter check produces false refusals for adopters with legitimate
  multi-environment setups. Recovery: keep it loud and advisory rather than
  blocking.

## Amendment 2026-08-03 — coverage gates CLEAN, and comprehensiveness is the contract

**Maintainer direction, quoted:**

> if we implement the python_security module, I think the expectation is that it
> should comprehensively scan, not just report a series of holes that it doesn't
> address. That is a false sense of security

Accepted, and it reorders this proposal. The original draft treated coverage
reporting as the repair and conda coverage as the gap to close afterwards. That
is backwards: **honest reporting of a hole is not a control**, because the
operator reads the exit code, not the caveats. A module named `python-security`
returning `0` teaches "my dependencies are clean" no matter how carefully the
body of the report hedges.

### This is Cairn's existing principle, not a new one

`bootstrap/DEPENDENCY_BUDGET.md` already states the rule for the pip-audit pass:

> **Fail-closed reporting.** A denied / offline / failed lookup is reported
> **unavailable, not clean**.

The module therefore already refuses to call an unavailable *lookup* clean. It
does not apply the same rule to unknown *coverage* — a lookup that succeeded
over 62% of the environment returns `0`. Those are the same category of
ignorance and they should have the same disposition. Extending the rule is
consistency, not escalation, which also means it needs no doctrine-evolution
argument.

### The governing rule this proposal now carries

**A leg returns CLEAN only when it has established coverage over the thing it
names.** The dependency leg names *dependencies* — so its denominator is the
environment, not the subset it happens to enumerate. Concretely:

* coverage established and no findings → **0 CLEAN**;
* coverage **not** established, or established as partial → **5 INCOMPLETE**,
  naming the unscanned count and class;
* findings → **10**, unchanged;
* unsafe/failed/timed-out → **20**, unchanged.

**Stated plainly, because it is the point:** on this machine today, a
correctly-behaving module reports **INCOMPLETE**, not CLEAN — 147 packages
unscanned, 82 of them native. That is the honest reading of the current state,
and it is the reading the exit code should have been carrying all along.

### Consequence — Part 2 becomes load-bearing, not optional

Conda coverage stops being an enhancement queued behind the repair. It is what
makes `0` **reachable** on a conda environment. The proposal's parts reorder
accordingly: the coverage mechanism is the substance, and the reporting repair
is what makes its absence visible in the meantime.

### The counter-argument, and where it bites

A gate whose usual result is INCOMPLETE trains its operator to stop reading it —
which is exactly finding **PS4** in this author's External review of
`portable-security-sweeps`, so it cannot be waved away here. The resolution is a
condition, and the plan must hold itself to it:

**INCOMPLETE is acceptable only while it is closable.** If Part 2 establishes a
mechanism that resolves the native layer, `0` becomes reachable and INCOMPLETE
is a transient true statement. If no mechanism can, then the module is not
capable of the contract its name implies, and the correct response is **to shrink
the module's declared scope to what it can honestly cover** — audit Python
distributions, say so in the name or the doctrine, and stop implying environment
coverage — rather than to keep returning INCOMPLETE forever or to keep returning
CLEAN over a fraction.

That is a Decision the plan must reach explicitly on measured evidence, not a
residual to carry. Recorded here so the plan cannot quietly settle for
permanent INCOMPLETE.

### What does not change

The zero-dependency contract stands: Cairn still installs no scanner, and an
adopter still provides the tools. This amendment constrains what the module may
**claim**, not what Cairn may **install**. Those were conflated in the original
draft's closing note, which argued that loud reporting of a missing tool was "the
design working" — true for a *missing tool*, and not an answer for a *missing
38% of the environment*.

### The expectation is created at selection, so the contract belongs there

**Maintainer clarification, quoted:**

> I mean if a user selects python_security

This scopes the rule and strengthens it. `python-security` is **opt-in and
team-gated** — an adopter does not drift into it, they *choose* it, and the
choice is an affirmative request for Python security coverage. Delivering 62% of
an environment under that name is not a caveat problem; it is a mismatch between
what the selection asked for and what the module does.

Two consequences the plan must carry:

1. **The coverage contract is stated in the module's selection doctrine.**
   `templates/modules/team-gated/python-security.md` is what an adopter reads
   when deciding, and it must say what the module covers, what it does not, and
   under what conditions it can return CLEAN — before they install it, not
   buried in a run report they read after they already trust it.

2. **Partial coverage is discoverable at first run, not on inspection.** An
   adopter who selects the module on a conda environment should learn
   immediately, from the aggregate, that coverage is not established — which is
   what the CLEAN-gating rule above delivers. The failure mode being closed is
   an adopter who selects a security module, sees `0`, and reasonably concludes
   their dependencies were audited.

This also disposes of a weaker reading of the zero-dependency contract that the
original draft leaned on. "Cairn does not install scanners" is a constraint on
Cairn's runtime, and it is *not* a licence to ship a module whose name promises
more than its mechanism delivers. If the selection promises comprehensive Python
security, the module either delivers it on the adopter's real environment or
says — at selection, and in the exit code — exactly where it stops.

## Amendment 2 (2026-08-03) — 100% *scanned* is unreachable; 100% *accounted for* is the contract

**Maintainer question:**

> Is there no way for us to get to 100% coverage?

**No — not 100% scanned.** And amendment 1's rule is defective as written, which
this question exposed. Correcting it here rather than letting the plan inherit
it.

### Why 100% scanned is unreachable

conda-meta metadata is better than expected: records carry the **upstream**
version, which is what advisory databases index — `openssl 3.6.2`,
`krb5 1.22.2`, `libcurl 8.19.0`, `freetype 2.14.3`. Mapping is therefore
tractable, not hopeless. Four obstacles remain, and none is closable by effort:

1. **Build-level patching breaks version matching in both directions.**
   `openssl 3.6.2` build `hd24854e_0` — conda-forge can carry a security patch
   without bumping the upstream version. Matching on version alone reports CVEs
   the build already fixed (false positive); a rebuild that did *not* patch is
   indistinguishable (false negative). The build string carries no patch
   manifest.
2. **No canonical name → CPE mapping.** Native advisories are indexed by CPE
   (`libcurl` → `cpe:2.3:a:haxx:curl`, `krb5` → `cpe:2.3:a:mit:kerberos`).
   conda names diverge from CPE product names and no authoritative table exists.
3. **Vendored and statically-linked code.** A package may bundle a vulnerable
   library with no separate record in any inventory. This is the general SBOM
   completeness problem and it does not have a local solution.
4. **No conda-forge advisory feed** mapping its packages to CVEs — stated as
   author understanding, **not verified**, and the plan must confirm it rather
   than inherit it.

### The defect in amendment 1

Amendment 1 offered two states — coverage *established* → CLEAN, coverage *not
established or partial* → INCOMPLETE. Given obstacles 1–4, coverage is
permanently partial, so that rule yields **permanent INCOMPLETE** — which the
same amendment identified (via **PS4**) as the failure mode that trains operators
to stop reading the gate. The rule contradicted its own stated condition that
"INCOMPLETE is acceptable only while it is closable."

The error was treating *unknown* and *unknowable* as one category. They are not,
and Cairn already distinguishes them everywhere else: the evidence stage's
non-containment and the key-holder-not-process limit are **declared residuals**,
not INCOMPLETE states.

### The corrected rule — three dispositions per package

Every enumerated package resolves to exactly one:

| Disposition | Meaning |
|---|---|
| **SCANNED** | resolved to an advisory source and checked |
| **NO-ADVISORY-SOURCE** | enumerated, lookup attempted, and no advisory source exists for it — a **declared residual** |
| **UNKNOWN** | not enumerated, or lookup not attempted |

**CLEAN requires: zero UNKNOWN, and the NO-ADVISORY-SOURCE set enumerated and
within the reviewed residual.** Findings still dominate; unsafe/failed still
dominates both.

The target is therefore **100% accounted for**, not 100% scanned:

* today — 244 scanned, **147 UNKNOWN** (unenumerated, uncharacterised);
* achievable — 391 accounted for, with each unresolvable package **named**.

That is a real improvement and an honest ceiling. What it removes is not the
residual but the *invisibility* of the residual.

### The residual must be diffable, or it becomes a blob

A named residual decays into a blanket exemption the moment it stops being
reviewed. So the residual set is **recorded and compared run over run**: a newly
unresolvable package is a **delta that surfaces**, not a silent addition to an
existing exemption. A residual that grows without anyone noticing is
indistinguishable from no control — the same lesson the archived
`gate-reanchor-preflight` record states as *a control that is present is not a
control that is reached*.

### What the plan must decide, on evidence

* whether any candidate mechanism resolves the native layer, and at what
  measured rate against these 391 packages;
* whether build-level patch divergence makes version matching produce
  false positives at a rate that would train operators to ignore findings —
  which would be a worse outcome than the current gap;
* the initial residual set, reviewed and recorded, and what governs adding to it.

**If the measured NO-ADVISORY-SOURCE set turns out to be most of the native
layer**, the honest conclusion is amendment 1's fallback: shrink the module's
declared scope and say so at selection. This amendment makes CLEAN *reachable*;
it does not assume the measurement will be favourable.

## Review -- OpenAI Codex (GPT-5) (External, security lens) -- 2026-08-03

**Model**: OpenAI Codex (GPT-5)

### Steelman

The proposal finds a real defect and the amendments improve its governing idea:
a security leg must account for its denominator, and a tool returning no known
vulnerabilities over the subset it recognized must not silently imply that the
whole environment was checked. I independently reproduced the proposal's core
intersection: the current canonical environment has 391 normalized conda
package names, 244 of which intersect the Python-distribution inventory, leaving
147 conda-only names. The proposed 0/5/10/20 distinction is the right vocabulary
for keeping absence, findings, and tool failure separate.

The author is also right to refuse an unexecuted scanner choice. Current primary
documentation resolves two candidates more sharply than the draft could:
Trivy's current
[Conda coverage table](https://trivy.dev/docs/v0.62/coverage/others/conda/)
supports Conda SBOM and license extraction but marks vulnerability scanning
unsupported, while OSV-Scanner's
[supported artifacts and manifests](https://google.github.io/osv-scanner/supported-languages-and-lockfiles/)
does not list Conda. The proposal should use those facts to narrow the next
revision rather than send the core feasibility decision downstream to a plan.

**Disposition: HOLD.** The objective is sound, but the current CLEAN predicate
can be reached without establishing the environment, lookup destination, or
meaning of the residual it relies on.

### [DAC1] HIGH / BLOCKING -- ambient environment can change both the audited interpreter and the egress authority

Part 1 proposes printing `sys.executable` and comparing it with the recorded
interpreter. That does not establish what pip-audit enumerated.

I installed pip-audit 2.10.0 into an isolated `/private/tmp` virtual environment
and ran its no-network `--dry-run`. Normally it reported 28 packages. With only
this ambient variable added:

```text
PIPAPI_PYTHON_LOCATION=/Users/kendal30/conda_envs/lhm/bin/python3.13
```

the same pip-audit executable reported 288 packages. pip-audit's installed
`_dependency_source/pip.py` reads that variable as the effective Python. The
current `_run_tool` copies every environment variable except four Python import
variables, so the shipped runner permits this redirection while still printing
its own unchanged `sys.executable`.

The egress destination is equally ambient. pip-audit 2.10.0's parser accepted:

```text
PIP_AUDIT_VULNERABILITY_SERVICE=osv
PIP_AUDIT_OSV_URL=http://127.0.0.1:7777/collect
PIP_AUDIT_OUTPUT=/private/tmp/diverted.json
```

as its service, endpoint, and output without any argv change. In the shipped
runner, `--allow-network` therefore authorizes an ambient destination, not the
documented vulnerability service. Proxy and CA-bundle variables are additional
network authority the proposal does not classify.

**Satisfier:** define a per-tool minimal environment and fixed argv before the
coverage design. Remove `PIPAPI_PYTHON_LOCATION` and all `PIP_AUDIT_*` /
dependency-tool configuration variables; pin the service, endpoint policy,
format, output destination, progress, cache, and strictness on argv. Any proxy
or custom trust-store pass-through must be explicit, printed, and risk-accepted,
not inherited. Tests must prove an ambient alternate interpreter, OSV URL,
output path, proxy, and CA bundle cannot change inventory, destination, or
evidence. The report should bind the child-observed inventory to the named
interpreter, not infer that identity from the parent process.

### [DAC2] HIGH / BLOCKING -- 391 is the conda inventory, not the environment denominator

The initial 147-package gap reproduces, but amendment 2 widens the claim from
"conda packages pip-audit cannot see" to "100% of the environment accounted
for" while retaining 391 as the denominator.

I parsed both inventories under canonical Python 3.13.13:

| Current canonical inventory | Unique normalized names |
|---|---:|
| conda metadata | 391 (394 JSON records) |
| Python distributions | 288 (290 metadata records) |
| intersection | 244 |
| conda-only | 147 |
| Python-only | **44** |
| union | **435** |

The Python-only set includes the editable project distributions
`lhm-frontend` and `modflow_tools`, along with `uvicorn`, `pydantic`, Sphinx
components, and others. A conda-only denominator drops precisely the packages a
developer may have installed with pip after environment creation. Conversely,
pip-audit's dry-run reported 288 packages, not only the 244-name intersection.

**Satisfier:** define the installed-environment denominator as a reconciled
union of conda records and Python distribution metadata. Specify normalized
identity, version/build conflicts, duplicate records, editable/direct-URL
packages, unreadable metadata, pip-only packages, and a package appearing in
both inventories with divergent versions. Any enumerator failure or unreconciled
identity is UNKNOWN. Tests need a conda-only native package, a pip-only wheel, an
editable package, duplicate metadata, and a cross-inventory version conflict.

### [DAC3] HIGH / BLOCKING -- `NO-ADVISORY-SOURCE` claims an absence no queried tool can establish

Amendment 2 defines this category as "lookup attempted, and no advisory source
exists for it" and allows it to participate in CLEAN. A negative lookup cannot
prove that proposition.

The live pip-audit 2.10.0 source makes the ambiguity concrete:

* its PyPI service turns a package/version 404 into `SkippedDependency` with
  "not found on PyPI";
* its OSV service treats an empty response as no associated vulnerabilities;
* neither result establishes that no advisory source exists elsewhere, that the
  submitted conda name maps to the upstream product, or that the source simply
  lacks a record.

Trivy currently extracts Conda packages for SBOM/license purposes but does not
scan them for vulnerabilities. OSV-Scanner supports a custom intermediate file,
but each entry still needs an ecosystem/name identity; Conda is not a supported
ecosystem in its published matrix. A home-grown Conda-name-to-PyPI/CPE map is
therefore not merely another adapter: it becomes the security authority for
product identity.

**Satisfier:** replace `NO-ADVISORY-SOURCE` with a factual disposition such as
`NO-MATCH-IN-PINNED-SOURCES`, name and version every queried source, and state
that this is accepted non-coverage rather than evidence of safety. Decide in
the proposal, not the plan, whether such accepted non-coverage may contribute
to CLEAN and who owns that risk acceptance. My security recommendation is to
narrow `python-security` to Python distributions unless execution demonstrates
a maintained Conda-native advisory authority. A large hand-mapped native
residual does not satisfy the Maintainer's comprehensiveness requirement.

### [DAC4] HIGH / BLOCKING -- the residual baseline has no artifact, schema, or update authority

Amendment 2 makes a reviewed residual load-bearing: CLEAN requires the current
no-match set to be "within the reviewed residual," and additions must surface
as a diff. But the proposal names no file, install mapping, strict schema,
integrity check, identity tuple, reviewer, expiry, or update command for that
baseline. It is absent from *Touches* and there is no proposed path.

Without those details, a name-only entry can silently bless every future build;
a report from a different source/version can be compared to an incomparable
baseline; and `upgrade --finalize` can re-record a weakened policy under the
existing human-only posture control.

**Satisfier:** either remove this mechanism by narrowing scope, or define the
baseline as a complete security-policy artifact. At minimum bind each entry to
normalized package name, version, Conda build, channel/subdir, queried source
set/version, reason, reviewer, review date, and expiry; reject unknown keys and
duplicates; integrity-cover it with the module apparatus; and make additions,
expiry, source drift, and identity drift non-clean. State who may accept an
entry and require Security Review for widening it.

### [DAC5] MEDIUM / BLOCKING -- "the project's recorded interpreter" silently reaches a registered trust root

Part 1 requires a match against "the project's recorded interpreter" without
naming the record or reader. In this repository that phrase resolves naturally
to gitignored `dev/.cairn/local-env.json`. `AGENTS.md` registers that file, its
strict reader `_resolve_interpreter`, and every subprocess call site using its
result as a high-risk executable trust root. A new parser in
`run_security_audit.py` would duplicate security semantics; importing the
lifecycle helper would couple an optional module to a skill that may not be
installed.

This surface is absent from *Touches*, and the declared plan review asks for an
External security lens rather than the explicit Security Review required for a
new reader/call site.

**Satisfier:** either narrow the claim to recording `sys.executable` + version
without asserting project-binding equivalence, or explicitly add the local
interpreter binding, reader strategy, fallback/refusal semantics, and call-site
tests to scope and require External Security Review. Do not create a second
near-copy of `_resolve_interpreter`.

### [DAC6] MEDIUM -- timeout plus control-character stripping does not close `_run_tool`

The proposed shared-boundary repair handles hangs and terminal controls, but
`capture_output=True, text=True` still has two unbounded failure modes.

Execution reproduced both edges of the current path:

* a child emitting ESC + `aggregate exit 0: CLEAN` was relayed byte-for-byte;
* a child emitting one invalid UTF-8 byte raised an uncaught
  `UnicodeDecodeError` traceback before `_run_tool` could classify it.

Captured stdout/stderr are also unlimited, so a scanner processing a hostile
tree can exhaust memory before sanitization. A subprocess timeout alone does not
bound output or specify cleanup of descendants.

**Satisfier:** capture bytes under a hard combined-output bound, decode with an
explicit error policy, escape controls before rendering, and parse fixed JSON
for pip-audit rather than trusting prose. Specify timeout/termination behavior
and map decode, truncation, malformed structured output, timeout, and cleanup
failure to DEGRADED. Test invalid UTF-8, oversized output, split control
sequences, stdout/stderr interleaving, timeout, and a spawned descendant.

### [DAC7] MEDIUM -- this is governing security doctrine, and one existing egress statement is false

The proposal says "No doctrine change" at lines 155-160. Its amendments then
introduce a "governing rule," selection-time CLEAN semantics, a reviewed
residual, and rules for widening that residual. Those are prescriptions every
module adopter and reviewer must follow, not descriptive corrections. The
Maintainer has already classified the surface as high-risk, so the
doctrine-evolution gate has a straightforward justification; it should be
stated rather than denied.

While touching the egress description, correct a pre-existing contradiction:
`bootstrap/DEPENDENCY_BUDGET.md` and the runner docstring say the default-off
pass "runs against its local cache only," but execution cannot reach pip-audit
at all because `run_pip_audit_pass` returns at the egress check first. The
runtime message correctly says "the lookup did NOT run." One authoritative
statement should match that behavior.

**Satisfier:** route the CLEAN/residual/selection rules as module doctrine,
record the Maintainer's high-risk classification as the rate-limit basis, and
make all default-off text say either "does not run" or implement a genuine
offline-cache mode with freshness/provenance semantics.

### Coverage and recommendation

**Covered:** I read the complete proposal through amendment 2; inspected
`run_security_audit.py`, `python-security.md`, `DEPENDENCY_BUDGET.md`, and the
portable-sweeps PS3/PS7 history; parsed both live inventories under
`/Users/kendal30/conda_envs/lhm/bin/python3.13`; installed pip-audit 2.10.0 only
inside `/private/tmp`; ran no-network dry runs; reproduced ambient interpreter,
service, endpoint, and output authority; reproduced ANSI/newline report forgery
and invalid-UTF-8 failure; and checked current primary Trivy, OSV-Scanner, and
pip-audit documentation/source.

**Not covered / low confidence:** I did not send the canonical package inventory
to PyPI/OSV because that network action was not approved; I did not execute
Trivy or OSV-Scanner, classify the asserted 82 native packages, inspect
conda-forge build patch provenance, test Windows, design a CPE map, or review an
implementation/plan that does not yet exist. No full pytest suite was warranted
for this proposal-only transition.

**Second round: required and recommended.** DAC1-DAC4 alter the mechanism that
decides CLEAN, DAC5 changes scope/review routing, and DAC6-DAC7 close adjacent
evidence/doctrine defects. The author should respond point-by-point and revise;
a fresh External security pass should then execute the chosen denominator,
source, and residual design before Decision.
