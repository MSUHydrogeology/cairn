# Adapter version-support evidence ledger — `portable-security-sweeps`

**What this file is.** The durable record behind the `portable-security-sweeps`
module's *admitted-artifact set*. One section per admitted
`(version, platform, architecture)`, each embedding **verbatim** the record
emitted by

```
python scripts/run_portable_security_sweeps.py \
    --verify-version-support /abs/path/to/candidate \
    --confirm-executing-an-unadmitted-binary
```

plus a retirement log. Sits beside `dev/measurement/attestation-replay-failures.md`
and `dev/measurement/review-floor-deviations.md`, which is where this repository
already keeps measurement records.

**Why it is a gate, not a document.** `bootstrap/tests/test_portable_security_sweeps.py`
asserts a **bijection** between the runner's source-owned admitted-artifact set
and the sections below: adding a version in source without a section here turns
that node red, and leaving a retired version in the active list turns its
reverse red. The test is run by a person typing
`python -m pytest bootstrap/tests` — **Cairn has no CI**, so nothing runs it
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

**Empty.** The admitted-artifact set ships **empty**: no
`(version, platform, architecture)` has been measured against a
Maintainer-supplied, checksum-verified binary yet. Measured `as_of 2026-08-05`:
`gitleaks` is **not on this host's `PATH`**, and the plan's second Maintainer
fence forbids an implementing agent acquiring one.

Superseded `as_of 2026-08-31`: `gitleaks 8.30.1` **is** now on this host's
`PATH`, at `/opt/homebrew/bin/gitleaks`. **The disposition does not change and
the set stays empty** — availability was never the control. What admission
requires is a *Maintainer-supplied, checksum-verified* binary and a
security-lens review of the record measured against it; a binary an agent finds
on `PATH` satisfies neither, and the fence above still forbids acquiring one.
The earlier line is left standing rather than overwritten, so a reader can see
which fact was true when.

The consequence, stated plainly rather than left to be discovered: the module
ships **reduced-provenance-only**. Full mode — the only mode that can report
`0` — is unreachable until a record lands here. An adopter gets useful
current-tree findings and an honest `INCOMPLETE`, or admits a release
themselves through the procedure above.

## Retirement log

*A triple leaves the active list by moving here, with the reason and the date.
A retired triple does not linger above.*

**Empty.** Nothing has been admitted, so nothing has been retired.

## Known gaps, per admitted triple

* **Cross-platform coverage.** All measurement anyone has taken for this module
  is Darwin arm64. Admitting a second platform is ledger work under the cadence
  above — one more triple, one more record — not a new proposal.
