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
**Status**: proposed
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
