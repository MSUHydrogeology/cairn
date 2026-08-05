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
**Status**: accepted
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

## Response to the External security review -- Claude (author) -- 2026-08-03

**Model**: Claude Opus 5

**All seven findings accepted.** Two I reproduced independently before
accepting; the rest I accept on the reviewer's execution evidence and my own
reading of the shipped code. **HOLD stands**, and one question in DAC3 is a
Maintainer Decision I will not settle in a response.

### Independently reproduced

**DAC2 reproduces exactly.** Normalized under the canonical interpreter:

| | |
|---|---:|
| conda unique names | 391 |
| Python distribution unique names | 288 |
| intersection | 244 |
| conda-only | 147 |
| **Python-only** | **44** |
| **union** | **435** |

The Python-only set includes `great-circle-calculator`, `aiosqlite`, `cattrs`,
Sphinx components — packages installed with pip *after* environment creation,
which is the ordinary way a scientific environment grows. Amendment 2 widened
the claim to "100% of the environment accounted for" while keeping **391** — a
conda-only denominator — as the target. That silently drops 44 packages,
including the editable project distributions. The denominator must be the
reconciled union.

**DAC7's contradiction reproduces**, and it is in two authoritative places:

* `bootstrap/DEPENDENCY_BUDGET.md:46` — "pip-audit runs against its local cache only"
* `templates/modules/team-gated/run_security_audit.py:392` — the same sentence

`run_pip_audit_pass` returns `_AGG_INCOMPLETE` at the egress check **before**
invoking pip-audit at all. Neither statement is true; only the runtime message
("the lookup did NOT run") is.

### DAC1 — accepted, and it is the finding I have made against others twice today

`PIPAPI_PYTHON_LOCATION` redirecting pip-audit's enumeration from 28 packages to
288, and `PIP_AUDIT_VULNERABILITY_SERVICE` / `PIP_AUDIT_OSV_URL` /
`PIP_AUDIT_OUTPUT` redirecting service, endpoint, and evidence destination — this
is ambient environment steering a security tool, which is precisely PS8 against
`portable-security-sweeps` and FUR1/FUR2 in the archived gate-reanchor record.

I read `_run_tool` closely enough to quote its four stripped variables in my own
proposal, and did not notice that everything else passes through. Worse, my
Part 1 proposed to *print* `sys.executable` — reporting the parent's identity as
though it established what the child enumerated. The reviewer's framing is the
correction: **bind the inventory the child observed to the named interpreter,
rather than inferring identity from the parent process.**

### DAC3 — accepted, and it puts a Decision to the Maintainer

The epistemic point is right and I will not defend the label. A 404 from PyPI
means *not found in PyPI*; an empty OSV response means *no associated
vulnerability in OSV*. Neither establishes that no advisory source exists. I
named the category `NO-ADVISORY-SOURCE` and let it participate in CLEAN, which
asserts a universal negative from a bounded query. `NO-MATCH-IN-PINNED-SOURCES`
is the honest name, it must record every queried source and version, and it is
**accepted non-coverage, not evidence of safety**.

**The Decision this forces, stated plainly rather than deferred to a plan.** The
reviewer resolved both candidates I had marked UNVERIFIED, from primary
documentation: Trivy's Conda coverage supports SBOM and license extraction but
marks **vulnerability scanning unsupported**, and OSV-Scanner does not list Conda
among supported ecosystems. If that holds, **no off-the-shelf Conda-native
advisory authority exists**, and amendment 1's own fallback triggers — narrow
the module's declared scope and say so at selection.

That sits directly against the Maintainer's requirement that the module
comprehensively scan. The options, and none is free:

1. **Narrow scope** — `python-security` audits Python distributions, says so at
   selection, and the 147 conda-only packages become declared non-coverage. The
   reviewer's recommendation, and honest.
2. **Build and own a name→CPE map** — which DAC3 correctly says makes Cairn *the
   security authority for product identity*. That is a much larger commitment
   than an adapter, with its own review burden and staleness failure mode.
3. **Evaluate an authority neither party has executed.** Grype/Syft match by CPE
   rather than ecosystem, and whether their catalogers read `conda-meta` is
   **unverified by either reviewer or author** — I am naming it as an unevaluated
   candidate, not as a solution.

This is a scope-and-risk-acceptance Decision, not a technical one, and it is the
Maintainer's.

### DAC4, DAC5, DAC6 — accepted without qualification

* **DAC4** — I made a reviewed residual load-bearing for CLEAN and specified no
  artifact, schema, identity tuple, reviewer, expiry, or update authority for
  it, and omitted it from *Touches*. A residual baseline with no schema is the
  blanket exemption I claimed it would prevent. Either it becomes a complete
  policy artifact or the mechanism goes with the scope narrowing.
* **DAC5** — "the project's recorded interpreter" does resolve to
  `dev/.cairn/local-env.json`, which `AGENTS.md` registers as a high-risk
  **executable trust root** with a strict reader. I wrote the phrase without
  naming the record, the reader, or the consequence, and did not put it in
  *Touches* or raise the review tier. Either narrow the claim to recording
  `sys.executable` and version, or add the binding to scope and take the
  Security Review it requires. I will not create a second `_resolve_interpreter`.
* **DAC6** — accepted, and the invalid-UTF-8 traceback is worse than the defect I
  described: `text=True` raises before `_run_tool` can classify anything, so a
  hostile tree produces an uncaught traceback rather than DEGRADED. Capture
  bytes, bound the combined output, decode with an explicit error policy, escape
  before rendering, and parse fixed JSON.

### DAC7 — accepted, including the self-contradiction

I wrote "No doctrine change" and then, across two amendments, wrote a *governing
rule* for when a security leg may return CLEAN, selection-time semantics, and
rules for widening a residual. Those are prescriptions, not descriptive
corrections. The rate-limit gate has a straightforward basis — the Maintainer has
classified this surface high-risk — and the proposal should state it rather than
deny that the gate applies.

### Pattern note

Three of these — DAC1, DAC5, DAC7 — are the same failure this session has
recorded repeatedly against my own work: **asserting a property at the strength
intended rather than the strength delivered.** DAC1 is the ambient-environment
finding I raised against two other proposals today and missed in mine. DAC7 is a
category claim I made about my own document without reading what it had become
by amendment 2. Recording it again because the count now matters more than any
individual instance.

### Recommended next step

Do not revise Parts 1 and 3 in isolation. They are sound and get stronger under
DAC1/DAC2/DAC6, but Part 2's feasibility now governs the module's declared scope,
and revising the reporting design before that Decision would design a denominator
for a contract that may be about to shrink. **The Maintainer's answer to DAC3 is
the next lifecycle event**, not another author revision.

## Maintainer direction 2026-08-03 — narrow the scope

**Quoted verbatim:**

> Let's go scope narrowing

This settles **DAC3** option 1 and unblocks the author revision below. It is a
direction on content, not a lifecycle Decision: the proposal moves
`reviewed -> revised` and still needs re-review and a Decision.

**What it settles.** `python-security` declares what it actually audits —
Python distributions in the named environment — rather than implying the
environment. The 147 conda-only packages become **declared, quantified
non-coverage** instead of an invisible gap inside a CLEAN result.

**What it does not settle, stated so it is not quietly lost.** The Maintainer's
requirement — *"we need Conda coverage"* — is **not** satisfied by this
revision. Narrowing makes the module honest about a gap it does not close. The
147 conda-only packages, 82 of them native (`krb5`, `openssl`, `freetype`,
`icu`, `hdf5`, the `aws-c-*` stack), remain unaudited by anything Cairn ships.
That need survives this proposal and **must have a durable home before this one
archives** — see *Successor requirement* below.

## Revised proposal — `python-security` audits Python distributions, and says so

Supersedes Parts 1 and 2 of the original and both prior amendments where they
conflict. Part 3 stands unchanged except as DAC6 strengthens it.

### 1. Declared scope

The module audits **Python distributions discoverable in the audited
environment**. It does not audit conda-managed native packages, system packages,
vendored or statically-linked libraries, or anything outside Python distribution
metadata.

This is stated in `templates/modules/team-gated/python-security.md` — the
document an adopter reads when **selecting** the module — not only in a run
report they read after they already trust it.

### 2. The denominator, and binding it to a real environment

The denominator is the **Python distribution inventory the child actually
enumerated**, not a count derived from the parent.

DAC1 makes this the load-bearing control rather than a nicety: the narrowed
contract's entire value is "we audited the Python distributions in *this*
environment", and `PIPAPI_PYTHON_LOCATION` moved pip-audit's enumeration from 28
to 288 packages without touching argv. A narrowed claim over an ambient
environment is exactly as false as the wide one. Therefore:

* a per-tool **minimal environment**: strip `PIPAPI_PYTHON_LOCATION`, every
  `PIP_AUDIT_*`, and proxy / CA-bundle variables; any pass-through is explicit,
  printed, and risk-accepted;
* **fixed argv** pinning service, endpoint policy, format, output destination,
  cache, and strictness — `--allow-network` must authorize the *documented*
  service, not an ambient one;
* the report **binds the child-observed inventory to the named interpreter**,
  and records `sys.executable` and version as *observations*, with no assertion
  of equivalence to any project record.

Per **DAC5**, the phrase "the project's recorded interpreter" is withdrawn.
`dev/.cairn/local-env.json` and `_resolve_interpreter` stay out of scope; no
second reader is created, and the review tier does not need to rise for this
surface.

### 3. Dispositions, over the narrowed denominator

Per **DAC3**, `NO-ADVISORY-SOURCE` is withdrawn — it asserted a universal
negative from a bounded query. Each enumerated distribution resolves to:

| Disposition | Meaning |
|---|---|
| **SCANNED** | queried against the pinned sources, result recorded |
| **NO-MATCH-IN-PINNED-SOURCES** | queried; the pinned sources hold no record. Names every source and version queried. **Accepted non-coverage, not evidence of safety.** |
| **UNKNOWN** | not enumerated, or the query did not complete |

**CLEAN requires zero UNKNOWN**, and reports the NO-MATCH count alongside. In
the narrowed scope this set is small and characterisable — editable and local
project distributions such as `great-circle-calculator` and `modflow_tools`,
which have no PyPI record by construction — rather than the native layer.

**DAC4 scales down accordingly.** The residual baseline is now a short list of
locally-built distributions, not a standing exemption over 82 native libraries.
It still needs a schema, identity tuple (name, version, queried-source set), and
integrity coverage, and additions must surface as a diff — but it is no longer
load-bearing for the module's credibility, which is what made the unspecified
version untenable.

### 4. Non-coverage is quantified at selection and at run

The module states, at selection and in every report, what it did **not** audit —
with a count, not a caveat. On the canonical environment today that is 147
conda-only packages, 82 native. An adopter selecting `python-security` on a
conda environment learns before installing that the native layer is outside the
contract.

### 5. Documentation / doctrine surface — corrected per DAC7

The original said "No doctrine change". That was wrong by amendment 2: rules for
when a security leg may return CLEAN, and how non-coverage is declared, are
**prescriptions**. This revision routes them as **module doctrine** in
`python-security.md`, and records the rate-limit basis explicitly — the
Maintainer has classified this surface high-risk, which is the
`doctrine/rationale.md` high-risk limb, so the gate is cleared rather than
denied.

Also corrected: `bootstrap/DEPENDENCY_BUDGET.md:46` and
`run_security_audit.py:392` both claim the default-off pass "runs against its
local cache only". Verified false — `run_pip_audit_pass` returns at the egress
check before invoking pip-audit. Both become "does not run", matching the
runtime message.

### 6. Part 3 — the shared runner, strengthened by DAC6

Unchanged in intent, extended in specifics: capture **bytes** under a hard
combined-output bound, decode with an explicit error policy, escape controls
before rendering, parse fixed JSON rather than prose, and map decode failure,
truncation, malformed output, timeout, and descendant-cleanup failure to
DEGRADED. A single invalid UTF-8 byte currently raises an uncaught
`UnicodeDecodeError` before classification — worse than the unsanitized-output
defect originally described.

### Successor requirement — conda coverage does not die here

**This proposal must not archive until the conda gap has a durable home.** The
evidence is established and should be carried forward rather than re-derived:

* 147 conda-only packages on the canonical environment, 82 native, `as_of 2026-08-03`;
* **Trivy** conda coverage is SBOM/license only — vulnerability scanning
  unsupported (reviewer, primary docs);
* **OSV-Scanner** does not list Conda among supported ecosystems (same);
* **Grype/Syft** match by CPE rather than ecosystem and are **unevaluated by
  either party** — the first candidate a successor should execute;
* a hand-built name→CPE map would make Cairn the security authority for product
  identity, which is a commitment, not an adapter.

Recommended form: a successor proposal `conda-advisory-coverage`, or a board row
under the deferred-questions section. The Decision that accepts this revision
should also record which, per the archive-precondition rule.

## Successor form settled — Maintainer, 2026-08-03

**Quoted verbatim:**

> Let's just record the Conda part as a future security module improvement in
> PLANNING.md

**Follow-ups migrated to:** `dev/PLANNING.md` > *Deferred follow-ups (durable
home)* > **Security apparatus** > *Conda advisory coverage*.

That discharges this revision's successor requirement, so the archive
precondition is satisfied ahead of the Decision rather than at it. The board row
carries the measured gap (147 conda-only, 82 native, `as_of 2026-08-03`), the
three candidate dispositions including Grype/Syft as unevaluated, the
name→CPE warning, and the revival condition — **a maintained conda-forge
advisory authority demonstrated by execution, not documentation**.

The board section's own rule is that a parked item "becomes its own proposal
when picked up", so choosing the row over opening `conda-advisory-coverage` now
defers the artifact without dropping the requirement.

## Re-Review -- Gemini Flash (External, security lens) -- 2026-08-03

**Steelman.** The revised proposal resolves all seven findings (`DAC1`–`DAC7`) raised in the prior External Security Review. Following Maintainer direction to narrow scope, `python-security` now explicitly audits discoverable Python distributions in the active environment rather than making false claims over 100% of a Conda environment. Crucially, the proposal fixes ambient environment redirection vulnerabilities (`PIPAPI_PYTHON_LOCATION` and `PIP_AUDIT_*` variable overrides), enforces minimal subprocess environments, pins fixed `pip-audit` argv parameters, captures raw bytes with hard output bounds, escapes control sequences before rendering, and reports three explicit package dispositions (`SCANNED`, `NO-MATCH-IN-PINNED-SOURCES`, `UNKNOWN`). CLEAN strictly requires zero `UNKNOWN` distributions, and non-coverage is quantified at both module selection and execution time. The Conda native library coverage gap (147 conda-only packages, 82 native) is explicitly recorded as a future security module improvement in `PLANNING.md`.

### Concerns

* **[E1] Native dependency non-coverage remains an unclosed gap.**
  Scope narrowing to Python distributions is the correct technical choice to prevent high-noise false positive/negative version matching, but leaves the 147 conda-only packages (including 82 native libraries such as `openssl`, `krb5`, `libcurl`) un-audited by Cairn. Adopters must rely on the follow-up roadmap item in `PLANNING.md` for future native Conda/CPE coverage.
* **[E2] Residual tracking for local non-PyPI packages.**
  Local project distributions without PyPI records (e.g. `great-circle-calculator`, `modflow_tools`) resolve to `NO-MATCH-IN-PINNED-SOURCES`. This residual baseline must be strictly schema-validated and diffed across runs to prevent silent expansion.

### Covered

* **Empirical Reproduction of Package Inventories**:
  - Re-ran inventory analysis on Python 3.13.13 (`/Users/kendal30/conda_envs/lhm/bin/python`).
  - Confirmed exact numbers: 394 Conda JSON files, 391 Conda unique names, 288 Python distribution names, 244 intersection, 147 conda-only, 44 python-only, 435 union.

```
$ ~/conda_envs/lhm/bin/python -c "
import os, json, glob, importlib.metadata
conda_meta = glob.glob('/Users/kendal30/conda_envs/lhm/conda-meta/*.json')
c_names = {json.load(open(f)).get('name','').lower().replace('-','_') for f in conda_meta} - {''}
p_names = {d.metadata.get('Name','').lower().replace('-','_') for d in importlib.metadata.distributions()} - {''}
print(f'Conda JSON files: {len(conda_meta)}')
print(f'Conda names: {len(c_names)}, Python dists: {len(p_names)}')
print(f'Intersection: {len(c_names & p_names)}, Conda-only: {len(c_names - p_names)}, Python-only: {len(p_names - c_names)}, Union: {len(c_names | p_names)}')
"
Conda JSON files: 394
Conda names: 391, Python dists: 288
Intersection: 244, Conda-only: 147, Python-only: 44, Union: 435
```

* **Documentation Contradiction Verification (DAC7)**:
  - Inspected `templates/modules/team-gated/run_security_audit.py` lines 387-405; confirmed `run_pip_audit_pass` returns `egress-off-unavailable` at the egress check prior to tool checking or cache inspection, verifying the docstring claim ("runs against its local cache only") is false and requires the proposed correction to "does not run".

* **Claim-check Verification**:
  - `claim_check.py`: verified clean output on `dev/proposals/2026-08-03-claude-dependency-advisory-coverage.md`.

```
$ ~/conda_envs/lhm/bin/python scripts/claim_check.py dev/proposals/2026-08-03-claude-dependency-advisory-coverage.md
claim_check: dev/proposals/2026-08-03-claude-dependency-advisory-coverage.md -- OK, no claim-check flags.
```

### Not covered / low confidence

* Subprocess byte bounding and structured JSON parsing of `pip-audit` stdout will be verified by unit tests in `bootstrap/tests/` during plan execution.

### Recommendation

**SHIP (LIFT HOLD).** The revised proposal successfully addresses all seven security findings (`DAC1`–`DAC7`), fixes ambient environment redirection vulnerabilities, establishes rigorous environment sanitization, and provides an honest, quantified contract for Python distribution security auditing.


## Response to the External re-review -- Claude (author) -- 2026-08-03

**Model**: Claude Opus 5

**Both concerns accepted; neither needs a further round.** The re-review lifts
the HOLD and independently reproduced the inventory numbers — 394 conda JSON
records, 391 unique conda names, 288 Python distributions, 244 intersection,
147 conda-only, **44 Python-only**, 435 union — which is the arithmetic the
narrowed denominator depends on.

### [E1] — accepted as a confirmation; already homed

Native non-coverage remains open, and that is the intended outcome of the
Maintainer's scope narrowing rather than a gap this proposal leaves untended. It
has a durable home: `dev/PLANNING.md` > *Deferred follow-ups* > **Security
apparatus** > *Conda advisory coverage*, carrying the measured gap, the two
eliminated candidates (Trivy conda is SBOM/license only; OSV-Scanner does not
list Conda), Grype/Syft as the first unevaluated candidate, and an
execution-bound revival condition.

Nothing to add. The finding is correct and the disposition is already recorded.

### [E2] — accepted, and the residual set is bounded here rather than left to the plan

Local project distributions with no PyPI record — `great-circle-calculator`,
`modflow_tools`, and the editables — resolve to `NO-MATCH-IN-PINNED-SOURCES`.
The revision already scaled DAC4's baseline down to "a short list of
locally-built distributions"; the re-review is right that *short* is not a
specification.

**Bounding it, so the plan inherits a rule rather than a judgement:** an entry
qualifies for the baseline only if it is **locally built** — installed from a
local path or VCS URL, which `importlib.metadata` exposes via `direct_url.json`
(PEP 610) rather than requiring a human to assert it. A distribution that
resolves to a public index and simply has no advisory record does **not**
qualify; it stays `NO-MATCH-IN-PINNED-SOURCES` and is reported as such, because
that is a fact about the advisory sources, not about provenance.

That distinction matters: it stops the baseline from becoming a place to park
public packages the sources happen not to cover, which is exactly the drift the
diffable-residual requirement exists to catch. The identity tuple, schema,
integrity coverage and diff-on-addition requirements from the revision are
unchanged.

**No Maintainer input required.** This tightens a rule the revision already
carried; it adds no scope, no file, and no dependency. Status stays `revised`;
this response makes the artifact Decision-ready.

## Decision -- Anthony Kendall (Maintainer) -- 2026-08-03

**ACCEPTED as revised.** Scribed and committed by Claude at the Maintainer's
explicit instruction. The re-review's disposition was **SHIP (LIFT HOLD)**.

**Maintainer's authorization, quoted verbatim:**

> I accept the dependency-advisory-coverage proposal as revised

**What is accepted.** `python-security` declares that it audits **Python
distributions in the named environment**, together with the reporting repairs
and the shared `_run_tool` fixes.

**The properties the acceptance rests on:**

* **The denominator is what the child enumerated**, bound to the named
  interpreter — not a count derived from the parent. `DAC1` made this
  load-bearing rather than cosmetic: `PIPAPI_PYTHON_LOCATION` moved pip-audit's
  enumeration from 28 packages to 288 without touching argv, so a narrowed claim
  over an ambient environment would be exactly as false as the wide one. A
  per-tool minimal environment and fixed argv pin the service, endpoint, format
  and output destination.
* **Three dispositions, and CLEAN requires zero `UNKNOWN`.** `NO-ADVISORY-SOURCE`
  was withdrawn as asserting a universal negative from a bounded query;
  `NO-MATCH-IN-PINNED-SOURCES` names every source queried and is **accepted
  non-coverage, not evidence of safety**.
* **The residual baseline is bounded by a mechanical rule**, per the re-review's
  `[E2]`: an entry qualifies only if **locally built** — a local path or VCS
  install, exposed by `direct_url.json` (PEP 610) rather than asserted by a
  human. A distribution that resolves to a public index and merely lacks an
  advisory record does **not** qualify, which stops the baseline becoming a
  place to park public packages the sources happen not to cover.
* **Non-coverage is quantified at selection**, not caveated in a run report.

**What accepting does NOT do.** It does not close the conda gap. 147 conda-only
packages, 82 of them native, remain unaudited by anything Cairn ships. Narrowing
made the module honest about that; it did not fix it. The re-review's `[E1]`
confirms this as the intended consequence of the scope narrowing rather than an
untended gap.

**Follow-ups migrated to:** `dev/PLANNING.md` > *Deferred follow-ups (durable
home)* > **Security apparatus** — *Conda advisory coverage* (the 147/82 gap,
with Trivy and OSV-Scanner eliminated on primary documentation, Grype/Syft named
as the first unevaluated candidate, and an execution-bound revival condition)
and *Install-integrity trust anchor*. The successor requirement this proposal
carried is therefore discharged **ahead of** the Decision rather than at it.

**Also corrected by this acceptance.** `bootstrap/DEPENDENCY_BUDGET.md:46` and
`run_security_audit.py:392` both claim the default-off pass "runs against its
local cache only"; verified false — `run_pip_audit_pass` returns at the egress
check before invoking pip-audit at all.

**Review tier discharged.** Required `required(External, security lens)`;
received a Codex External round (seven findings, all accepted) and a Gemini Flash
External re-review returning SHIP with the inventory arithmetic independently
reproduced.

**Next transition:** plan-open, carrying `required(External, security lens)` in
its own right.

**Decision-only commit.** Status flip and this section, nothing else.
