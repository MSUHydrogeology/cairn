# Repair the strict release-security runner for v0.7

**Author**: Codex gpt-6-sol (Strategy, High)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-05
**In brief**: Make the release security check finish on Mac and Windows without missing tests or running the whole suite twice.

## Decision summary

Repair the strict runner before v0.7. Run its full applicable suite once per
native platform and join Mac and Windows evidence for one commit before calling
release security passed. This costs two host runs and a reviewed rule for
platform-only tests. A local pass alone is not a release pass.

## Context

`dev/PLANNING.md` item 7a requires a corrected strict run on the final v0.7
candidate. The v0.6.1-only exception explicitly left this runner unpassed
(`dev/plans/archive/2026-11-03-baseline-checker-alignment.md`, Maintainer
dispositions). `bootstrap/security_check.py::run_suite` runs all
`bootstrap/tests` without an explicit shuffle seed. Its `run_quality_gate`
then invokes all sub-gates; `scripts/quality_gate.py` defaults to seed 0 and
starts another whole-suite pytest process. Both child processes inherit release
mode, where `bootstrap/tests/conftest.py` refuses actual skips, xfails and
xpasses. The tree has native-Windows junction and POSIX-only cases, so neither
host can pass every case. Earlier focused runs are not a strict runner pass at
the final v0.7 SHA. No full-suite reproduction ran for this proposal.

## Proposal

1. Preserve the clean committed candidate, detached exact-byte checkout,
   pre/post verification, Bandit over the derived shipped surface and live
   allowlist, and `check_cairn.py`. Preserve refusal on tool absence, scanner
   errors, malformed reports, changed bytes, test failures and incomplete
   outcomes. Do not alter trust records, configured suite members or security
   test assertions.
2. In `bootstrap/security_check.py`, run the release-mode suite with explicit
   `--quality-gate-shuffle-seed=0` and call `quality_gate.py` for **both**
   neutrality and redundancy only. The order-independence sub-gate remains
   available through its own public command; its seed-0 whole-suite behavior
   is fulfilled by the direct release suite, not silently deleted.
3. Define a narrow, reviewed platform-only outcome rule at the existing
   `bootstrap/tests/conftest.py` release boundary. Name the exact nodes or
   conditions eligible on each host from collection; all other
   skips, collection-time skips, xfails and xpasses still refuse. A member
   excused on one host must pass on its native host at the **same candidate
   SHA**. Each host's output names its platform, SHA, eligible non-runs and
   failures; neither local success is labelled complete release security.
   The existing release record may call the joined result passed only with
   both matching, passing outputs. Add no parallel evidence store or general
   skip switch.
4. Investigate Windows committed-path comparison: Git tree keys use `/`,
   whereas `_checkout_leaf_paths` currently stringifies native relative
   paths. Normalize only that representation if a nested-path Windows probe
   confirms the mismatch. Investigate whether the unconditional POSIX
   executable-bit comparison works on Windows; preserve meaningful mode
   detection or name an unresolved barrier. Neither is claimed as a proven
   fix by this proposal.

Coordinate node identities and fixtures with suite-consolidation 2a **before**
editing control flow. Its unfinished C1-C4, growth report and archive are not
prerequisites for #7a plan archive. The final strict run belongs to the
separate release point on the final candidate; no agent plan waits on human
signing, baseline installation or publication.

## Rationale

Local tests cannot hide unexpected non-runs; release cannot claim native
coverage without both hosts. Named quality sub-gates remove a duplicate suite
launch without changing `AGENTS.md`'s certifying pair or substituting ordinary
certification for strict security evidence.

## Alternatives considered

* **Do nothing:** no build or upkeep cost, but the v0.6.1 exception cannot
  renew and #7a stays unpassed; repeated full runs and platform skips remain.
* **Fixture-only/platform emulation:** simpler runner, but cannot prove native
  junction or POSIX behavior; it loses the native safeguard.
* **Keep both suite launches and join platform logs manually:** smaller
  control-flow edit, but costs another full run on each host and leaves the
  duplicate invocation. It can meet coverage only if the same-SHA join is
  still explicit.

**Recommendation:** the narrow two-host evidence rule and one suite launch.
The classification and release-record work buys native coverage without
another runner or database; review must challenge the roster and Windows path.

## Documentation / doctrine surface

Describe the behavior in `SECURITY.md` (one-command claim and phases),
`docs/release-process.md` (checks) and `bootstrap/PROVENANCE.md` (ordering).
Keep `AGENTS.md`'s certification commands and triggers unchanged; deliberation
stays in `dev/`. Update only affected source comments. No board or changelog
edit is proposed here.

## Evidence / verification plan

### Tests required

Use `tools/test_tiers.py for` on changed paths. Owning tests:
`bootstrap/tests/test_security_check.py` (phases, bytes, tools, platform
output), `test_broad_run_guard.py` (incomplete outcomes), and
`test_quality_gate_cli.py` / `test_quality_gate_order_independence.py`
(sub-gates, seed); resolve moved paths after 2a. Add native Windows path/mode
probes where absent. Unknown or falsely eligible skips, collection skips,
missing/wrong-SHA/failed native evidence and removed suite members must not
produce complete release success. Mutate each eligible native case in separate
copies to test its reach. Ordinary and Security code reviews precede wide
Boundary B on a clean Python 3.13.x commit.

### Examples / smoke checks

Through the real `security_check.py` entry point on committed fixtures, show
one suite process per host, seed 0, both quality sub-gates, Bandit,
`check_cairn` and byte-integrity refusal. Run prose claim/link/snippet and
neutrality gates for changed docs. At the authorized release point, require
native Mac and Windows outputs at one SHA and their joined record. The
certifying pair remains separately required; no full suite runs during this
proposal or routine iteration.

#### Security preflight

* **S1 — Who supplied it?** The checked commit comes from the local Git
  checkout; suite membership, skip conditions, checker and test code come
  from that commit. Host OS, interpreter and subprocess outcomes come from
  each machine, and the Maintainer joins the two recorded outputs. Candidate
  code partly judges itself, as today.
* **S2 — Can it fail?** Mutation controls must make a non-platform skip,
  wrong SHA, omitted native node, stale allowlist, removed phase or changed
  checkout byte fail. None ran in this proposal-only turn.
* **S3 — What fires it, over what?** `python bootstrap/security_check.py`
  selects committed bytes, derived Bandit targets, all `bootstrap/tests` with
  seed 0, and both named quality sub-gates. The
  adopter-facing `SECURITY.md` says: "One command, and its output belongs in
  the release notes." The revised text must explain why two native outputs
  and their join are needed for a complete record.
* **S4 — Which way does it break?** Unknown platform, malformed or missing
  counterpart evidence, unclassified skip, failed subprocess or path/mode
  mismatch must prevent a release pass. Normalization cannot drop a leaf.
* **S5 — Who still wins?** A party able to change candidate checker and tests
  before review can weaken both; independent review and Maintainer judgment
  remain necessary. Exact-byte matching cannot detect malicious committed logic.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

One host reports complete release success without its counterpart; a
non-platform skip passes; a native case is absent from the collected suite;
seed 0 or a quality sub-gate is missing; Windows cannot verify committed
paths or modes; or the final two outputs refer to different SHAs. Any such
result keeps #7a open rather than becoming another release exception.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance.
