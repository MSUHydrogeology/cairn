# Module: portable-security-sweeps

**Selected when:** the project wants a **cross-language** secret-exposure
tripwire over its own checkout — the current working tree and the committed
history — that runs **offline**, installs no scanner, and never reports a clean
result for a scan that did not happen. Team-gated and **opt-in**: no preset
selects it, and selecting it is how a project takes on the external tool.

**Adds to:** the project's `dev/modules/` doctrine set (this file), plus a
standard-library orchestrator (`scripts/run_portable_security_sweeps.py`) and a strict JSON
policy. The module **installs no scanner**; the adapter binary is a host
executable the project supplies.

## What this module is — and is not

It **is** a self-audit tripwire on a **trusted checkout**: a cheap, offline,
repeatable question — *does this tree, or its history, carry something that
looks like a credential?*

It is **not**:

* **a reviewer for untrusted changes.** Everything in the tree under check is
  candidate-controlled input. The controls below bound what that input can
  steer; they do not make the module safe to point at a hostile repository you
  would not otherwise check out.
* **a proof.** A clean run is a tripwire that did not trip. Detection quality
  is the adapter's, and the adapter's built-in rule corpus is trusted as part
  of that binary — it is not independently pinned or evaluated here.
* **a dependency the scaffold installs.** No scanner is downloaded, bundled, or
  executed during installation. Moving an executable trust root into the
  installer is refused by design.

## The one adapter

Exactly one: **Gitleaks**, offline, with **no network flag**. There is no
`--allow-network`, no remote-data path and no advisory cache. OSV-Scanner,
zizmor and Trivy are **not supported adapters and not names the policy
accepts**; each would return as its own proposal carrying its own executable
chain, ambient-configuration evidence, network posture, output schema and
offline-clean disposition.

Two scan questions, run as two legs:

| Leg | Question |
|---|---|
| `current-tree` | Does the working tree carry a match? |
| `history` | Does the committed history carry a match? |

## The residual trust set — two executables, enumerated

The complete set of host executables this module trusts, so a reader can audit
it rather than infer it:

1. **`gitleaks`** — the adapter, resolved from the trusted host environment.
2. **`git`** — resolved by the identical rules. It is a trust root in its own
   right for three reasons: the runner itself invokes it for the
   pre-execution configuration screen (which discovers its own configuration
   boundary with a Git call first, so an ordinary repository and a linked
   worktree are both handled correctly) and to determine, from Git's own
   object model, whether the history question has an applicable input at
   all; and **Gitleaks invokes it transitively** for the history leg. The
   transitive invocation was found by execution, not by reading
   documentation, and it was absent from the first enumeration of this
   module's trust set.

Both are validated for **shape and containment, not provenance**:

* absolute path; regular file; executable bit set;
* **neither the lexical nor the resolved path may be inside the tree under
  check** — a package-manager symlink is fine, a symlink whose target resolves
  into the candidate tree is refused;
* re-validated immediately before invocation.

**v1 does not authenticate host binaries.** A project needing provenance pins
and verifies them outside this module.

## Two version modes, and what each may report

The runner selects a mode from the adapter's self-reported version **and** a
digest the admission ceremony measured.

| Mode | Entered when | May report |
|---|---|---|
| **full** | the resolved binary's SHA-256 matches a digest recorded for this exact `(version, platform, architecture)` | `0`, `5`, `10`, `20` |
| **reduced** | the version parses as a supported `8.x.y` but **no** digest is recorded for this `(version, platform, architecture)` | `5`, `10`, `20` — **never `0`** |

Three refusals sit alongside them, and none of them runs a scan leg:

* **digest mismatch** — a digest *is* recorded for this
  `(version, platform, architecture)` and the resolved binary is not it. That is
  a contradiction, not an absence: **DEGRADED (20)**.
* **unparsable version** — anything that is not an exact `X.Y.Z`:
  **INCOMPLETE (5)**.
* **unsupported major** — **INCOMPLETE (5)**.

**Full mode — the only mode that can reach `0` — is unreachable without a
digest match.** Reduced mode never emits CLEAN and never describes itself as
offline-verified. Between admissions a project gets useful current-tree
findings and an honest INCOMPLETE, or pins an admitted release itself.

## The exit space

| Exit | Meaning |
|---|---|
| `0` | CLEAN — every selected leg ran, in full mode, and found nothing |
| `5` | INCOMPLETE — a selected leg did not fully run (absent binary, shallow clone, non-Git export, unadmitted version) |
| `10` | FINDINGS — at least one validated finding |
| `20` | DEGRADED — a refusal, or a result the runner cannot trust |

Precedence is **`20 > 10 > 5 > 0`**: a finding is never hidden by an incomplete
sibling leg. **NOT APPLICABLE** is distinct from INCOMPLETE and contributes
nothing to the aggregate — it never weakens another leg.

## The suppression boundary

The policy document carries **reviewed fingerprint suppressions and nothing
else**. It names no path, no argv element, no environment variable, no
executable, no configuration file, no baseline, and no digest, hash, checksum
or admitted artifact. It cannot select a version or a mode.

A suppression file discovered **inside** the candidate tree never becomes
policy. Reviewed fingerprints are materialized one per line into an
**off-tree** ignore file; a fingerprint carrying a newline is refused, because
one fingerprint may never become two ignore-file lines.

An existing `.gitleaksignore` anywhere in the candidate tree — regular file or
symlink, at any depth — is a **pre-execution refusal**, DEGRADED (20), because
the adapter loads it even when a trusted empty ignore path is named and exposes
no observed switch to disable that.

## The candidate-configuration boundary

Everything under the candidate's `.git/` is candidate-controlled. Two controls,
and the honest description of what each does:

1. **A deny-by-default pre-execution screen.** The runner enumerates the
   candidate's **include-expanded** repository-local configuration and
   **refuses** on any key outside a named, reviewed inert allowlist, on any
   `include` / `includeIf` whose origin file resolves outside the
   repository's *actual* common/config directory, and on a listing that
   fails, times out or exceeds a byte cap. The allowlist is source-owned, not
   policy-controlled. The boundary itself is discovered with a hardened
   `git rev-parse --path-format=absolute --git-common-dir` call rather than
   assumed from `.git`'s path, because in a **linked worktree** `.git` is a
   *file* naming the main repository's per-worktree metadata directory, not
   the directory holding the local config the screen must bound — asking Git
   is what makes an ordinary repository and a linked worktree both work
   correctly. `--path-format=absolute` requires Git 2.31 or newer; an older
   Git refuses the flag and the screen DEGRADES rather than guessing.
2. **Counted config keys on the child process.** The child environment pins a
   fixed set of Git configuration keys that outrank repository-local config.

**The pinned key set is defence in depth over the keys it names — it is not a
boundary.** Measured: a candidate steps around it with one `include.path` line
or one `includeIf`, needing no new Git version and no exotic key, and Git offers
no way to disable the repository-local tier at all. What bounds the
configuration surface is the screen in (1). Its residual is stated in the same
breath: the screen is a **snapshot**, subject to the same delete/create race the
ignore-file refusal accepts, and it bounds *configuration* — not everything a
candidate repository controls.

## The version-support cadence — a contract, not an aspiration

* At each release the Maintainer, or a delegated Security Reviewer, evaluates
  the newest candidate `8.x`.
* A real-project reduced-mode report is **also** a trigger.
* Promotion to full mode requires the **whole admission matrix** — run by
  `--verify-version-support` against a checksum-verified binary — **plus** a
  security-lens review of the recorded evidence. Admission is a reviewed source
  change; nothing the runner does at scan time can admit a version.
* Prior admitted `(version, platform, architecture)` triples stay supported
  while their matrix passes.
* Removal takes the same visible contract change and a migration note; the
  retired triple moves to the retirement log rather than lingering.

## Running it

```
python scripts/run_portable_security_sweeps.py --target . --policy scripts/portable_security_policy.json
python scripts/run_portable_security_sweeps.py --json          # the deterministic summary
python scripts/run_portable_security_sweeps.py --security-verification   # the bounded child document
```

Admitting a candidate version — an operator act, never part of a sweep and
never reachable from a standing command:

```
python scripts/run_portable_security_sweeps.py --verify-version-support /abs/path/to/candidate \
    --confirm-executing-an-unadmitted-binary
```

## Residuals, stated rather than implied

* v1 does not authenticate host binaries.
* There is **no process containment**. A malicious adapter is not contained,
  and reduced mode in particular executes a binary whose behaviour has not
  received this module's matrix.
* The adapter's built-in rule corpus is trusted as part of that binary.
* The configuration screen and the ignore-file refusal are snapshots; the
  same-user preflight/execution race on a trusted checkout is accepted.
* Cross-platform behaviour is established only where an admission record says
  so.
* A clean run is a tripwire, not a proof.
