# Runtime contract

This document is the **authoritative declaration of Cairn's runtime
requirements** — the environment an adopter must provide to run the
Python scaffold engine. It is the single source of truth for the
Python floor, the tested matrix, and the capability/degradation
matrix. It supersedes any other claim in the repository.

## Python floor

**`requires-python = ">=3.11"`**

The engine (`bootstrap/_scaffold/`, ~6,044 lines across eight owned
modules plus the verifying loader `_guard`) was measured with `vermin`
(see `bootstrap/tests/`) against
the post-scaffold-split topology. The measured **syntactic** minimum
is **Python 3.7** — the engine is written conservatively and uses no
syntax newer than 3.7. The declared **supported** minimum, however, is
**Python 3.11**: it is a *support / test* policy, not a syntactic
requirement, and is set to the **earliest non-EOL Python with meaningful
runway**. 3.7 (EOL Jun 2023), 3.8 (EOL Oct 2024), and 3.9 (EOL Oct 2025)
are all past end-of-life; 3.10 reaches EOL ~Oct 2026, so 3.11 (EOL Oct
2027) is the first floor that does not force an immediate re-bump. We do
not test or support an EOL Python even though the syntax still runs on it.

Cairn is not a pip-installable package and carries no `pyproject.toml`,
so this document is the **authoritative** floor declaration (the floor is
not machine-enforced at install time). If Cairn ever gains a
`pyproject.toml`, it should carry `requires-python = ">=3.11"`.

The previous claim of "Python 3.10+" in `bootstrap/prompts/bootstrap-lite.md`
and an implicit "scaffold.py syntax is 3.10+" are **refuted** by
measurement — the engine is syntactically 3.7-clean, comfortably within the
declared `>=3.11` support line. (`templates/modules/team-gated/intent.py`'s
"3.8-era syntax" note describes that same conservatism; the *supported*
floor is the 3.11 policy, not the syntactic floor.)

**Engine topology (post-scaffold-split, 2026-06).** The scaffold
engine is split across two surfaces:

* `bootstrap/scaffold.py` — a **143-line fail-closed launcher and
  facade**; the public entry point for all import and CLI uses.
* `bootstrap/_scaffold/` — the **engine** (~6,044 lines): eight owned
  modules in an acyclic DAG (`security`, `slotmerge`, `merge`,
  `config`, `lockfile`, `install`, `upgrade`, `cli`) plus the verifying
  loader (`_guard`). This is the surface measured for the floor CI check.

This topology strengthens the "run-it-in-a-container, don't port"
argument: the engine depth is real, and the contained-kernel recipe
is the practical non-Python adoption path.

## Tested matrix

### Python versions

| Version | Status |
|---------|--------|
| 3.11    | Supported minimum (earliest non-EOL with runway) |
| 3.12    | Supported |
| 3.13    | Supported (canonical interpreter; gates run here) |
| 3.10    | Below floor; EOL ~Oct 2026; not supported |
| 3.8–3.9 | EOL (Oct 2024 / Oct 2025); not supported |
| 3.7     | Measured syntactic floor; not supported (EOL Jun 2023) |
| < 3.7   | Not supported |

### Launcher resolution

**Do not assume `python` exists.** The canonical launcher name varies
by OS and Python installation method:

* `python3` — the standard name on macOS (via Homebrew, pyenv) and
  most Linux distributions.
* `python` — available when a venv or conda environment is activated;
  absent or aliased to Python 2 on many systems.
* `py` — the Windows Python Launcher; maps to `python` on Windows
  where the launcher is installed.

**Adopter guidance:** activate an environment (`conda activate <env>`,
`source venv/bin/activate`) before invoking scaffold commands, so
`python` resolves to the expected interpreter. Document scripts with
`python3` as the default launcher; accept `py` in Windows docs.

The scaffold CLI entry point (`python bootstrap/scaffold.py`) and the
shebang on that file (`#!/usr/bin/env python3`) both use `python3`.
Invoke it as: `python3 bootstrap/scaffold.py --help`.

### Required external executables

| Executable | Required by | Notes |
|------------|-------------|-------|
| `git` | Engine (upgrade, lockfile, install) | Must be on PATH; minimum tested version: 2.30 |

`git` is the only external executable the scaffold engine requires at
runtime. No other subprocess-invoked binaries are required for the
core engine. (The `python-security` optional module requires `bandit`
and `pip-audit` — but those are opt-in, module-gated, and declared
in `DEPENDENCY_BUDGET.md` Exception 1.)

### Encoding and filesystem assumptions

* **Source encoding:** all scaffold engine files are UTF-8. Template
  files are UTF-8. Adopter repository files processed by the scaffold
  (AGENTS.md, dev/ tree, etc.) are expected to be UTF-8.
* **Filesystem:** no case-sensitivity assumption is made for the
  template or target trees; path components use lowercase with hyphens
  or underscores per the respective convention.
* **Line endings:** template files use LF line endings. The engine does
  not normalize line endings on write; platform-specific line-ending
  normalization (via `.gitattributes`) is the adopter's responsibility.
* **Path length:** no assumption of short paths; pathlib.Path is used
  throughout the engine.

## Capability / degradation matrix

Cairn's discipline-aid tools operate at different criticality levels.
This matrix answers, per tool: is no-tool operation *equivalent*,
*weaker-but-supported* (degraded), or *unsupported*; and what
assurance is lost.

### Minimum mechanized kernel

The following tools constitute the **minimum mechanized kernel** —
the floor for a "Cairn" adoption. Running without the kernel means
the methodology can still be practiced (doctrine + git is always
sufficient), but the mechanized assurances that make Cairn
reproducible across agents and sessions are absent.

| Tool | Module | Degradable? | Notes |
|------|--------|-------------|-------|
| Lifecycle backend (`scaffold.py install` / `upgrade`) | core | **Required** | Installs and upgrades the `dev/` tree; no equivalent hand-operation |
| Lockfile / upgrade engine (`scaffold.py upgrade`) | core | **Required** | Lockfile integrity + upstream sync; no equivalent hand-operation |
| Integrity check (`verify_integrity.py`) | core | **Required** | Detects tampered apparatus before it can self-audit; fail-closed |

### Degradable discipline aids

The following tools improve Cairn's quality assurance surface but
are **degradable**: omitting them forfeits the named assurance, but
does not prevent the methodology from operating. An adoption running
below the full aid set is in **degraded assurance state** — this is a
recorded, visible condition, not a silent omission (see
"Degraded-assurance state" below).

| Tool | Module | No-tool mode | Assurance forfeited |
|------|--------|--------------|---------------------|
| `claim_check.py` | `default-on` | Weaker-but-supported | Broken doc paths, stale line citations, wrong count claims pass undetected until human review |
| `link_check` | `default-on` | Weaker-but-supported | Broken cross-references in docs pass undetected; doc rot accumulates silently |
| `lifecycle_metrics` | `default-on` | Weaker-but-supported | Proposal/plan cycle-time and throughput are unmeasured; the Measurement Compact's quality surface is blank |
| `python-security` (`bandit` + `pip-audit`) | `python-security` (team-gated, opt-in) | Equivalent (for non-Python adopters); weaker for Python adopters | Python static-analysis + CVE scan missing for Python adopters; non-Python adopters never acquire this module |
| `doc-drift-prevention` | team-gated | Equivalent | Drift gate for generated/reference docs absent; docs can silently diverge from source of truth |

### Degraded-assurance state

When an adopter runs below the full aid set, this condition must be
**visible and recorded** — not a silent green check implying full
coverage. The rule:

* **Per disabled aid**: the quality/fidelity surface (e.g., the
  project's quality gate output or the `check_cairn` surface) must
  report the disabled aid as **DEGRADED** or **UNAVAILABLE** — not
  PASS. A missing tool that returns a silent green is a false-pass
  and is prohibited.
* **Named forfeitures**: the degraded report names exactly which
  assurances are forfeited (from the table above) — e.g.,
  "claim_check UNAVAILABLE: broken doc paths and stale citations
  will not be detected mechanically."
* **Kernel absence is unsupported**: running without the minimum
  mechanized kernel (lockfile / upgrade / integrity check) is not a
  declared supported degradation tier — it is an unsupported
  configuration.

This "degraded assurance" state is the formal answer to an adopter
who asks: "I am below the full aid set — what exactly am I missing?"
It is explicit, named, and visible — not inferred.

## The dependency budget

Cairn's scaffold engine is **stdlib-only by default** — no third-party
packages are required to run `bootstrap/scaffold.py install` or
`upgrade`. This is a deliberate constraint: a stdlib-only engine means
"just an interpreter, no pip or PyPI to vet" — a genuine saving for a
non-Python team provisioning Python for the contained-kernel recipe.

Declared exceptions to this default are in
`bootstrap/DEPENDENCY_BUDGET.md`. Dev-only and test-only tools (e.g.,
`vermin` for the floor CI check) are not adopted-runtime dependencies
and are listed in `bootstrap/requirements-dev.txt`; they are noted in
the budget ledger but do not affect the stdlib-only runtime contract.

## Floor CI check

A test in `bootstrap/tests/test_python_floor.py` runs `vermin` over
the engine (`bootstrap/_scaffold/`) and asserts that the detected
minimum does not **exceed** the declared floor (>=3.11). The check
skips gracefully if `vermin` is not importable or on PATH. Install
dev dependencies to run it:

```
pip install -r bootstrap/requirements-dev.txt
python3 -m pytest bootstrap/tests/test_python_floor.py -v
```

The vermin-based check is the v1 mechanism. A container-pinned compile
check (compiling the engine inside a container pinned to exactly
Python 3.11) provides deeper assurance and is a noted future
enhancement; the vermin check is sufficient for v1.
