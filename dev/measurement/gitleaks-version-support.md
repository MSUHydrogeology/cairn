# Adapter version-support evidence ledger — `portable-security-sweeps`

**What this file is.** The durable record behind the `portable-security-sweeps`
module's *admitted-artifact set*. One section per admitted
`(version, platform, architecture)`, each embedding **verbatim** the record
emitted by

```
python dev/tools/run_portable_security_sweeps.py \
    --verify-version-support /abs/path/to/candidate \
    --confirm-executing-an-unadmitted-binary
```

plus a retirement log. Sits beside `dev/measurement/attestation-replay-failures.md`
and `dev/measurement/review-floor-deviations.md`, which is where this repository
already keeps measurement records.

**Why it is a gate, not a document.** `tests/test_portable_security_sweeps.py`
asserts a **bijection** between the runner's source-owned admitted-artifact set
and the sections below: adding a version in source without a section here turns
that node red, and leaving a retired version in the active list turns its
reverse red. The test is run by a person typing
`python -m pytest tests` — **Cairn has no CI**, so nothing runs it
automatically.

## How a version is admitted

1. The Maintainer supplies a candidate binary at a **stable** path with its
   publisher checksum verified. An implementing agent does not download, fetch
   or install one.
2. `--verify-version-support` runs the admission matrix against it and emits a
   record. Its exit code distinguishes *matrix passed, record emitted* (`0`)
   from *matrix failed, do not admit* (`20`); a refusing record carries
   `"admit": false` and its reasons.
3. A **security-lens review** reads the recorded evidence.
4. Only then does a reviewed source change add the
   `(version, platform, architecture)` key and its measured SHA-256 to the
   runner's admitted-artifact set, and a section here carrying the record.

Nothing the runner does at scan time can admit a version. The subcommand never
mutates the set.

## What the matrix establishes, and what it does not

* **Establishes**: the candidate accepts the runner-owned argv on both legs;
  its report validates against the output schema; it invokes no Git subcommand
  outside the accounted set (`config` runner-owned, `log` and `ls-remote`
  adapter-owned); it did not reach the network canary; and the runner's own
  pre-execution refusals fired.
* **Does not establish**: absence of egress. The network observation is a
  loopback canary advertised through the proxy variables plus the Git-shim
  subcommand log. It is **not a sandbox**, and the record says so in its own
  `network_observation.bound` field.
* **Does not establish**: anything about a platform other than the one recorded.
  Each admitted key is one `(version, platform, architecture)` triple.

## What a record must contain before it can be reviewed

The runner **depends** on the candidate's exit contract: it pins `--exit-code`
so a findings result and a usage error are different codes, and a candidate
that ignores that flag would make every other row unreadable. That contract is
therefore **measured per candidate**, not assumed from its major — one
candidate and a source read are evidence about a candidate.

A record a security-lens review can act on carries, for **each** subcommand
(`current-tree` → `dir`, `history` → `git`), three rows under `end_to_end`:

| Row | Fixture | What must hold |
|---|---|---|
| `clean` | a fixture carrying nothing to find | exit `0`, and a report that validates with no finding |
| `planted_finding` | a fresh high-entropy value in the `generic-api-key` shape | the **pinned** findings exit, **and** a report that validates with at least one finding |
| `invalid_argv` | the clean fixture, with `--timeout` given a non-integer | an exit that is neither `0` nor the pinned findings value |

A record missing any row **does not admit**: an incomplete measurement of the
exit contract is not a weaker admission, it is no admission. The record shows
the rows it did measure, so a reader can tell *this candidate failed the
matrix* from *the matrix never ran*.

**The planted value is generated, never a published example.** Measured on
8.30.1 darwin/arm64 (2026-08-31): the default ruleset **allowlists** AWS's own
documented `AKIAIOSFODNN7EXAMPLE`, so a matrix planted with it scans clean and
the findings row reads as a passing scan of a tree that had nothing in it —
a silently wrong measurement, which is worse than a missing one.

**Known gap, measured 2026-08-31 on 8.30.1 darwin/arm64.** Against the real
adapter the `planted_finding` row does **not** complete: `--redact=100` empties
`Secret` to `REDACTED` but leaves `Match` as `api_key = "REDACTED"` — the
redacted secret inside its surrounding context — and the runner's
redaction check requires the whole field to be `REDACTED`. The matrix
therefore refuses with `admit: false` and the reason
`carries an unredacted 'Match'`. **This is the runner's own pre-existing
control, not a matrix defect**, and it means an ordinary sweep would also
DEGRADE on a real finding. Reconciling the check with what the adapter
actually emits is outside the change that added these rows and is not decided
here.

## Admitted artifacts

*One `### <evidence-id>` section per admitted triple, each with the emitted
record in a fenced `json` block. The evidence-id is the identifier the runner's
admitted-artifact set carries.*

Historical disposition (preserved for auditability):

* Measured `as_of 2026-08-05`: the admitted-artifact set shipped **empty** —
  `gitleaks` was **not on this host's `PATH`**, and the plan's second
  Maintainer fence forbade an implementing agent acquiring one.
* Superseded `as_of 2026-08-31`: `gitleaks 8.30.1` **was** on this host's
  `PATH`, at `/opt/homebrew/bin/gitleaks`. **The disposition did not change and
  the set stayed empty** — availability was never the control. What admission
  required was a *Maintainer-supplied, checksum-verified* binary and a
  security-lens review of the record measured against it; a binary an agent
  found on `PATH` satisfied neither, and the fence above still forbade
  acquiring one.

Superseded `as_of 2026-11-18`: the Maintainer supplied and verified the two
`8.30.1` builds below (`darwin/arm64` and `windows/arm64`), and `--verify-version-support`
emitted `"admit": true` on both. Unmeasured `(version, platform, architecture)`
triples remain in **reduced-provenance** mode (`INCOMPLETE` rather than `0`);
full mode is reachable on the two admitted triples below.

### GL-2026-11-18-darwin-arm64-8.30.1

* **Triple**: `("8.30.1", "darwin", "arm64")`
* **Provenance**: Homebrew `gitleaks` 8.30.1 bottle (`/opt/homebrew/bin/gitleaks` -> `/opt/homebrew/Cellar/gitleaks/8.30.1/bin/gitleaks`)
* **Binary SHA-256**: `f414bc2fb952be6c9072b75cb411e3368614ef4b16d48dbd9ad238034afd2302`
* **Measured date**: `2026-11-18`

```json
{"admit": true, "candidate_version": "gitleaks version 8.30.1", "candidate_version_key": "8.30.1", "end_to_end": {"current-tree": {"clean": {"exit": 0, "validated_findings": 0}, "invalid_argv": {"element": "--timeout=cairn-not-an-integer", "exit": 1}, "planted_finding": {"exit": 42, "validated_findings": 1}}, "history": {"clean": {"exit": 0, "validated_findings": 0}, "invalid_argv": {"element": "--timeout=cairn-not-an-integer", "exit": 1}, "planted_finding": {"exit": 42, "validated_findings": 1}}}, "git_invocations": ["runner:common-dir", "runner:config", "runner:version", "shim:log", "shim:url"], "git_version": "git version 2.53.0", "hostile_config": {"candidate_ignore_file": "refused before execution", "counted_git_config_keys": "8", "runner_owned_config_flag": "sent off-tree"}, "kind": "portable-security-sweeps/version-support-record", "network_observation": {"bound": "This observes a candidate that honours proxy variables or connects to the advertised address and the exact Git URL query.  It is NOT a sandbox and does not establish absence of egress.", "canary_connections": 0, "method": "loopback canary advertised as http_proxy/https_proxy/ALL_PROXY and as CAIRN_PORTABLE_NETWORK_CANARY, plus helper-mediated fixed Git operations"}, "output_schema": "validated on both legs", "platform": ["darwin", "arm64"], "refusals": [], "schema": 1, "screen": "ran through the bound helper token", "unadmitted_binary_executed": {"declared_source": "Homebrew gitleaks 8.30.1 bottle (/opt/homebrew/Cellar/gitleaks/8.30.1/bin/gitleaks)", "path": "/opt/homebrew/bin/gitleaks", "resolved": "/opt/homebrew/Cellar/gitleaks/8.30.1/bin/gitleaks", "sha256": "f414bc2fb952be6c9072b75cb411e3368614ef4b16d48dbd9ad238034afd2302", "statement": "This command executed an external file that Cairn has NOT admitted, at the operator's instruction."}}
```

### GL-2026-11-18-windows-arm64-8.30.1

* **Triple**: `("8.30.1", "windows", "arm64")`
* **Provenance**: Installed on `cairn-windows` at `C:\Program Files\Git\cmd\gitleaks.exe` from official `https://github.com/gitleaks/gitleaks/releases/download/v8.30.1/gitleaks_8.30.1_windows_arm64.zip` (archive SHA-256 verified against `gitleaks_8.30.1_checksums.txt`: `b95f5e4f5c425cedca7ee203d9afd29597e692c4924a12ed42f970537c72cc0f`)
* **Binary SHA-256**: `200df852fdecbedb19a33960657333cba5e231740bc8968972b507b50f93b194`
* **Measured date**: `2026-11-18`

```json
{"admit": true, "candidate_version": "gitleaks version 8.30.1", "candidate_version_key": "8.30.1", "end_to_end": {"current-tree": {"clean": {"exit": 0, "validated_findings": 0}, "invalid_argv": {"element": "--timeout=cairn-not-an-integer", "exit": 1}, "planted_finding": {"exit": 42, "validated_findings": 1}}, "history": {"clean": {"exit": 0, "validated_findings": 0}, "invalid_argv": {"element": "--timeout=cairn-not-an-integer", "exit": 1}, "planted_finding": {"exit": 42, "validated_findings": 1}}}, "git_invocations": ["runner:common-dir", "runner:config", "runner:version", "shim:log", "shim:url"], "git_version": "git version 2.56.0.windows.4", "hostile_config": {"candidate_ignore_file": "refused before execution", "counted_git_config_keys": "8", "runner_owned_config_flag": "sent off-tree"}, "kind": "portable-security-sweeps/version-support-record", "network_observation": {"bound": "This observes a candidate that honours proxy variables or connects to the advertised address and the exact Git URL query.  It is NOT a sandbox and does not establish absence of egress.", "canary_connections": 0, "method": "loopback canary advertised as http_proxy/https_proxy/ALL_PROXY and as CAIRN_PORTABLE_NETWORK_CANARY, plus helper-mediated fixed Git operations"}, "output_schema": "validated on both legs", "platform": ["windows", "arm64"], "refusals": [], "schema": 1, "screen": "ran through the bound helper token", "unadmitted_binary_executed": {"declared_source": "https://github.com/gitleaks/gitleaks/releases/download/v8.30.1/gitleaks_8.30.1_windows_arm64.zip (zip sha256:b95f5e4f5c425cedca7ee203d9afd29597e692c4924a12ed42f970537c72cc0f)", "path": "C:\\Program Files\\Git\\cmd\\gitleaks.exe", "resolved": "C:\\Program Files\\Git\\cmd\\gitleaks.exe", "sha256": "200df852fdecbedb19a33960657333cba5e231740bc8968972b507b50f93b194", "statement": "This command executed an external file that Cairn has NOT admitted, at the operator's instruction."}}
```

## Retirement log

*A triple leaves the active list by moving here, with the reason and the date.
A retired triple does not linger above.*

**Empty.** Nothing has been retired yet.

## Known gaps, per admitted triple

* **Resolution of the `2026-08-31` `Match` redaction gap.** The `release-secrets-scanning`
  work (archived at commit `f68f5dba`) resolved the redaction gap noted above:
  the runner now checks `Secret == "REDACTED"` and `"REDACTED" in Match` and
  discards `Match` wholesale so surrounding context is not retained. Both
  `GL-2026-11-18-darwin-arm64-8.30.1` and `GL-2026-11-18-windows-arm64-8.30.1`
  passed `planted_finding` under that control.
* **Cross-platform coverage.** Only `("8.30.1", "darwin", "arm64")` and
  `("8.30.1", "windows", "arm64")` are admitted. Other platforms and
  architectures (such as `linux/x86_64`, `linux/arm64`, `darwin/x86_64`, and
  `windows/x86_64`) remain unmeasured and therefore run in reduced-provenance
  mode until a Maintainer-supplied, checksum-verified build is measured and
  reviewed under the cadence above.
