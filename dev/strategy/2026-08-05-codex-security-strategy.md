# Cairn security strategy: boundaries, evidence, and open gaps

**Author**: Codex (Strategy), Antigravity (Strategy)
**Model**: GPT-5 (Codex), Gemini 3.1 Pro
**Date**: 2026-08-05; rewritten around `0.5-dev` 2026-10-27
**Status**: living
**Type**: living-reference
**Surfaces this feeds**: [`dev/PLANNING.md`](../PLANNING.md); [`SECURITY.md`](../../SECURITY.md); [`bootstrap/SAFETY.md`](../../bootstrap/SAFETY.md); [`bootstrap/PROVENANCE.md`](../../bootstrap/PROVENANCE.md); [`bootstrap/UPGRADE.md`](../../bootstrap/UPGRADE.md)

## Summary

Cairn's goal is practical: **help scientists build and release secure software without turning security assurance into an endless ceremony.**

Because Cairn's templates and scripts are installed into an adopter's repository and loaded by their AI agents as instructions, **template integrity and path containment are security properties.** Cairn enforces those properties through standard-library-only Python tools, fail-closed path and symlink guards, content and static-analysis scanners, and Maintainer-run release ceremonies.

This document states Cairn's current security posture, the six design principles that govern security work, the five boundary clusters (`[BND]`, `[VER]`, `[TRU]`, `[REC]`, `[REL]`), and the **Live residual register** of open gaps and revival triggers. Historical records of completed security work live in [`CHANGELOG.md`](../../CHANGELOG.md) and `dev/plans/archive/`.

---

## Security objective and threat posture

Cairn protects five things:

1. **The scientist's tree** — installation and upgrade must never read or write outside the target repository, follow symlinks across boundaries, silently select a different profile, or execute a program configured inside the target repository.
2. **Scientific and project data** — scanners and network checks must not leak source code, credentials, findings, or identifiers through network or logging paths.
3. **The deliberation record** — untrusted repository text, git metadata, or issue text must never be executed as instructions or impersonate trusted tool output.
4. **The release trust chain** — a verified release tag, the source tree used to build, the installed bytes, and the release evidence must not silently substitute for one another.
5. **The Maintainer's attention** — a control that is too complex to run, habitually noisy, or described as stronger than it actually is becomes a security liability.

### Two postures: Cairn's own repository vs. adopter inputs
* **Cairn's own repository** operates under a **trusted-contributor, single-Maintainer, Maintainer-controlled machine** posture. Signatures authenticate the key holder, not the host process. The gate re-anchor (`refs/cairn/gate-anchor`) and [`scripts/repin.py`](../../scripts/repin.py) verify that frozen tests and engine AST pins move only with explicit Maintainer authorization.
* **Adopter-facing paths** treat all target-repository inputs as **untrusted data** until validated: profile files (`dev/.cairn/profile.yml`), lockfiles (`dev/.cairn/cairn-lock.yml`), review areas (`dev/.cairn-upgrade/`), module policies, repository paths, filenames, `.git/config` settings, git metadata, issue text, and network responses. A target under inspection never supplies the trust material that declares itself clean.

---

## Design principles

1. **Trust material comes from outside the candidate.**
   A hash stored next to the bytes it covers detects accidental corruption or unilateral edits, not coordinated tampering. Any check that claims tamper evidence must read its expected hashes or public keys from a trusted source outside the directory being inspected.
2. **Derive scanner coverage from delivery, then test with an independent check.**
   Scanner target lists come from the same manifest (`scaffold.py --manifest`) that delivers shipped files, backed by an on-disk check so a shared bug cannot hide both a file and its scan.
3. **Optional tools may be incomplete; authority checks fail closed.**
   An optional external scanner may report `INCOMPLETE` (exit 5) when not installed locally. Malformed policy, unsafe paths or symlinks, altered trust material, scanner errors, credential violations, or a skipped check in release mode (`CAIRN_RELEASE_GATE_ACTIVE`) must fail closed. Aggregation never upgrades `INCOMPLETE`, `DEGRADED`, or `FINDINGS` into `CLEAN`.
4. **Name every trigger at its real strength.**
   Cairn has no hosted CI. A Maintainer-run release command ([`bootstrap/security_check.py`](../../bootstrap/security_check.py)) is described as Maintainer-run. A test suite check is described as suite-run. Doctrinal rules are described as read by reviewers and the Maintainer, never as mechanical authentication.
5. **Mechanical checks belong on bytes, not process.**
   Mechanical gates earn their keep on **formatting, correctness, and security** (claims about bytes that either hold or fail) and lose it on **process** (claims about whether people followed a workflow, which drift and invite workarounds).
6. **Every security check needs a negative control.**
   A security test must prove it fails when the hazard is present, and its pass condition must observe state directly rather than relying on wall-clock timing or silent skips.

---

## Cluster map

Every security capability, boundary, or open gap belongs to one of five clusters. Findings share a ceremony only when they share the same trust boundary, implementation owner, and verification path.

### 1. `[BND]` Input, execution, and containment boundaries
**Question:** Can repository-controlled input choose what Cairn reads, writes, deletes, executes, or prints raw to the terminal?
* **Current controls:**
  * **Write containment (`Class A` / `Class B` in [`bootstrap/_scaffold/SECURITY_MUTATIONS.md`](../../bootstrap/_scaffold/SECURITY_MUTATIONS.md)):** Every install and upgrade write routes through `_assert_safe_write` or `_assert_fanout_contained`, staging via exclusive sibling files (`_stage_exclusive`, `_write_by_replacing`). `upgrade --remove-retired` unlinks untouched retired files through `O_NOFOLLOW` directory descriptors after verifying SHA-256 digests against Cairn's built-in table and a sterile `git cat-file` check.
  * **Read containment (`Class D` in [`bootstrap/_scaffold/SECURITY_MUTATIONS.md`](../../bootstrap/_scaffold/SECURITY_MUTATIONS.md)):** `upgrade` validates lockfile paths (`_contained_lockfile_path`), refuses symlinked profiles and lockfiles (`_refuse_if_linked`), refuses symlinked review areas (`_assert_stage_has_no_links`), and validates `cairn_commit` as lowercase hex before invoking `git`.
  * **Session & orientation boundaries:** [`tools/session.py`](../../tools/session.py) (and its template twin) refuses tracked project binaries when resolving the local Python interpreter, terminal-encodes untrusted git and path strings via `encode_display`, refuses symlinked or tracked `next-session.md` notes in `dev/reflections/`, and treats issue/board text in `/session-start --drain` strictly as data, never instructions.
  * **Network boundaries:** `api-access-security` and `web-hosting-security` share a standard-library HTTP client that resolves DNS once, rejects private/out-of-class address sets, re-verifies the connected peer IP after connect, never follows redirects, and restricts agent-run checks to loopback (`127.0.0.1` / `::1`).

### 2. `[VER]` Verification capabilities and coverage
**Question:** What security evidence can an adopter or Maintainer gather, what files does each check inspect, and can coverage silently narrow?
* **Current controls:**
  * **Default-on content scanning (`content-security`) and local verification dispatcher (`security-verification`):** `scripts/check_cairn.py` scans templates and docs for hidden Unicode, bidirectional overrides, and prompt-injection patterns; `run_security_verification.py` dispatches admitted local runners with a stripped environment and fixed `0 / 5 / 10 / 20` exit codes.
  * **Language and portable sweeps:** `python-security` (Bandit + `pip-audit` against OSV) and `portable-security-sweeps` (offline Gitleaks with binary digest verification before launch).
  * **Design-time preflight:** Proposal templates include a 5-question security preflight block for changes touching untrusted input, filesystem/process boundaries, or trust roots.

### 3. `[TRU]` Trust roots and provenance
**Question:** Which material is allowed to say *"these are the expected bytes or authorized identities,"* and how is trust in that material established?
* **Current controls:**
  * **Release provenance ([`bootstrap/PROVENANCE.md`](../../bootstrap/PROVENANCE.md)):** Signed release tags verified via `bootstrap/container/verify-ref.sh` in an isolated workspace with `fetch.fsckObjects=true`.
  * **Gate manifest, AST attestation, and `repin` ([`bootstrap/REANCHOR_RUNBOOK.md`](../../bootstrap/REANCHOR_RUNBOOK.md), [`scripts/repin.py`](../../scripts/repin.py)):** `bootstrap/tests/_gate_manifest.py` and `_ast_attest.py` pin frozen test files and scaffold engine AST symbols against `refs/cairn/gate-anchor`. `scripts/repin.py` (`status`, `package`, `ceremony`) loads verifier code directly from the anchor commit's tree and walks the Maintainer up to the passphrase-signed ceremony step.
  * **Install integrity ([`bootstrap/verify_integrity.py`](../../bootstrap/verify_integrity.py)):** Fail-closed SHA-256 check of installed files against the target's `dev/.cairn/cairn-lock.yml` (detects unilateral modification and reports unfilled template slots to stderr).

### 4. `[REC]` Deliberation authority and record integrity
**Question:** Can a tool or untrusted text mutate lifecycle state, forge a review, or impersonate Maintainer authorization?
* **Current controls:**
  * **Commit-mediated, append-only lifecycle ([`AGENTS.md`](../../AGENTS.md)):** Reviews read a committed tree, never a shared working directory, and are self-committed by the reviewing session. Reviewer independence is enforced by doctrine and Maintainer inspection, not by a name-matching script.
  * **Verbatim Decision scribing:** Any scribed Maintainer Decision or scope allowance must quote the Maintainer's words verbatim in both the artifact and the commit body.

### 5. `[REL]` Release evidence, disclosure, and ceremonies
**Question:** What finite check blocks a release, who runs it, and how are vulnerabilities reported?
* **Current controls:**
  * **Single local release gate ([`bootstrap/security_check.py`](../../bootstrap/security_check.py)):** Materializes a detached checkout from committed Git blobs (`git hash-object --stdin`), verifies clean pre/post repo state, runs Bandit + `check_cairn.py` with zero unallowlisted MEDIUM+ findings and allowlist-liveness checks, runs `bootstrap/tests` with `CAIRN_RELEASE_GATE_ACTIVE=1` (where any skip/xfail/xpass fails the run), and runs `scripts/quality_gate.py`.

---

## Live residual register (open gaps and revival triggers)

Each entry below is an open gap we want to close or a deliberate residual with the trigger that revives it. A row leaves this register only when a change closes it with a test or when a measurement shows the subject no longer exists.

### Active for `0.5`
* **`[BND-3]` `upgrade` dirty-tree check runs a target repository's `core.fsmonitor` hook.** `_dirty_tracked_paths` in `bootstrap/_scaffold/upgrade.py` runs a plain `git status`, which can execute a program configured in a target repo's `.git/config` (`core.fsmonitor`) and misreads dirty files when the project sits in a subdirectory. *Status:* Proposal accepted 2026-10-27 ([`2026-10-26-claude-upgrade-dirty-check-runs-no-repository-programs.md`](../proposals/2026-10-26-claude-upgrade-dirty-check-runs-no-repository-programs.md)); reuses the sterile git helper from `upgrade --remove-retired`.
* **`[REL-3 / TRU-4]` First live run of `scripts/repin.py` and the `0.5` AST/gate-manifest re-anchor.** `repin` is built and tested against scratch repos; its first real ceremony run is the `0.5` cut (`dev/PLANNING.md`).

### Queued gaps (concrete improvements to schedule)
* **`[BND-1 / BND-6]` Verify the saved base copy against `base_hash` before 3-way merge (`SR6`).** `upgrade` does not check that the cached file in `dev/.cairn/` still matches the lockfile's `base_hash` before merging, so a corrupted or crafted base copy can silently drop an adopter edit or an upstream fix. *Fix:* verify `base_hash` at `--plan`, `--stage`, and `--apply`, falling back to a manual (`review-only`) merge on mismatch (`dev/PLANNING.md`).
* **`[BND-2 / BND-6]` Refuse nested `.git/` paths in an upgrade review area.** `_contained_lockfile_path` refuses `.git/` at the project root, but a crafted review area naming `sub/.git/hooks/post-merge` is not yet refused (`dev/PLANNING.md`).
* **`[BND-2 / BND-6]` Decide how `upgrade --init-lock` handles a symlinked tracked file.** Currently `--init-lock` hashes a tracked module file (such as `AGENTS.md`) through a symlink if one sits there, recording the target's digest in the new lockfile (`dev/PLANNING.md`, `SECURITY_MUTATIONS.md`). Needs a proposal choosing whether to refuse or record the link state.
* **`[BND-4]` Escape profile-supplied module/slot names in install reports, invisible characters in lockfile paths, and child-process output in `session.py`.**
  1. `bootstrap/_scaffold/install.py` and `cli.py` print unknown module names and profile-supplied slot names without terminal escaping (`dev/PLANNING.md`).
  2. `_contained_lockfile_path` uses Python's `str.isprintable()`, which admits some invisible/bidirectional Unicode characters (`dev/PLANNING.md`).
  3. `tools/session.py` (and its skill twin) passes three `proc.stderr` streams and child `stdout` through without `encode_display` (`dev/PLANNING.md`).
* **`[TRU-1]` Anchor `verify_integrity.py` against a trusted `CAIRN_ROOT` for verbatim files.** Today `verify_integrity.py` reads expected hashes from the target's own `dev/.cairn/cairn-lock.yml`, which detects accidental or unilateral edits (`SECURITY.md` and `doctrine/runtime-contract.md` state this limit plainly) but not an attacker who rewrites both a file and `cairn-lock.yml`. *Goal:* cross-check verbatim-installed files against the operator's trusted `CAIRN_ROOT` checkout while distinguishing legitimate forks.
* **`[TRU-4 / TRU-5]` Sign the `refs/cairn/gate-anchor` commit and strip `PYTEST_*`/`PYTHON*` in the re-anchor ceremony.**
  1. `refs/cairn/gate-anchor` (`6f29519d`) is currently unsigned (`git verify-commit` exits 1), whereas `AGENTS.md` states the anchor is trusted by the signature on the commit it names (`SR-8`, `dev/PLANNING.md`). Either sign the anchor commit at the ceremony or update the claim in `AGENTS.md`.
  2. The re-anchor ceremony's Stage A inherits `PYTEST_*` and `PYTHON*` environment variables, which can drop tests from the pinned collection without failing (`dev/PLANNING.md`).
  3. `bootstrap/REANCHOR_RUNBOOK.md` documents updating `refs/cairn/gate-anchor` locally via `git update-ref` but does not yet document pushing `refs/cairn/*` to the remote (`[TRU-7]`).
* **`[TRU-4]` Protect root pytest configuration and `--noconftest` in release mode.**
  1. `_frozen_files` freezes `bootstrap/tests/conftest.py` using five globs, but a repository-root `conftest.py`, `pytest.ini`, or `pyproject.toml` outside those globs would still be loaded by pytest.
  2. Passing `--noconftest` skips `bootstrap/tests/conftest.py` (which enforces the release-mode fail-on-skip rule). A release run should assert that its own conftest loaded and that no root pytest config or `PYTEST_PLUGINS`/`PYTEST_ADDOPTS` overrides are present.
  3. Explicitly list the 16 trust-apparatus files (`conftest.py`, `_gate_*.py`, `_ast_attest.py`, `_oracle*.py`, `_loader_proto.py` and their tests) in `AGENTS.md` > High-risk surfaces before ever narrowing the `bootstrap/tests/**/*.py` contract-surface glob.
* **`[REL-6]` Name a concrete private vulnerability reporting route in `SECURITY.md` and `README.md`.** `SECURITY.md` currently says *"report privately to the maintainer"* without naming a mechanism (such as GitHub Private Vulnerability Reporting) or linking it from `README.md`. Requires the Maintainer to verify the repository setting is enabled on GitHub.

### Triggered residuals (wait for their trigger before opening work)
* **`[BND-1]` Profile authority & lockfile schema validation (`_LOCK_SCHEMA`).**
  * Unknown module names under `modules:` in `profile.yml` are not yet rejected at parse time (*trigger:* first mistyped-module report or edit to `expand_preset`).
  * `_infer_init_lock_axes` infers `human_team` from whether `CONTRIBUTING.md` exists (*trigger:* next edit to `--init-lock` axis inference).
  * `read_lockfile` does not yet reject unknown `_LOCK_SCHEMA` versions on read (*trigger:* next lockfile schema change or `[TRU-1]` trusted-source anchoring).
* **`[BND-3 / TRU-5]` Local interpreter binding (`dev/.cairn/local-env.json`) residuals.**
  * Accepted residual `SW-SR-10` ([`bootstrap/SAFETY.md`](../../bootstrap/SAFETY.md)): an untracked binding arriving via a downloaded archive, `git apply`, `git reset`, or `git rm --cached` is trusted until a future post-`0.5` proposal moves the binding into `.git/`.
  * `_has_symlink_component` has a check/use race if a local process swaps a parent directory between the symlink walk and execution (*trigger:* next edit to interpreter resolution in `session.py`).
* **`[BND-3]` Facade-loader symlink checks and `B607` relative `git` lookups.**
  * Facade submodule loader symlink checks and partial `sys.modules` cleanup on failed import (*trigger:* next change to the scaffold facade loader).
  * `session.py` invokes `git` by name (`B607` LOW×2) rather than absolute path (*trigger:* an adopter PATH-hijack report or lowering the Bandit blocking floor to LOW).
* **`[VER-1]` Content-scanner Unicode coverage limits.**
  * Curated 12-member Greek homoglyph denylist (waiting on stdlib `unicodedata` exposing UTS #39 confusables) and unflagged whole-script Cyrillic (avoiding false positives on international names).
  * `_scan_unicode` reports at most one finding per category per line (*trigger:* a demonstrated multi-hit-per-line bypass).
* **`[VER-3]` Security test and catalog hygiene.**
  * `test_a_t6_descendants_do_not_outlive_the_timeout` in `test_security_stack.py` uses a time-window absence check rather than a process-group probe, so a slow machine can pass by timeout (*trigger:* **must fix before enabling parallel pytest `-n auto`**).
  * `test_detached_checkout_excludes_an_ignored_pytest_override` in `test_security_check.py` fails unless `PYTHONDONTWRITEBYTECODE=1` is set when `__pycache__` is present (*trigger:* next edit to `security_check.py`'s detached-checkout guard).
  * `test_security_verification.py` child-env test should account for CPython auto-injecting `LC_CTYPE="C.UTF-8"` when absent from the parent environment; `test_verify_ref.py` has two nodes sensitive to prior-test state in a full-suite run (*trigger:* next edit to either test file).
  * Derive `templates/modules/README.md` catalog rows (`api-access-security`, `web-hosting-security`, `portable-security-sweeps`, `dependency-advisory-coverage`) and `content_scan_roots.txt` vendor-wrapper paths mechanically from the scaffold mappings (*trigger:* next module addition).
* **`[VER-4 / SP8-3]` Dispatcher & scanner extensions.**
  * `portable-security-sweeps` runs via its own command (`run_portable_security_sweeps.py`) rather than through `run_security_verification.py` (`LT-2`, accepted by Maintainer).
  * `api-access-security` and `web-hosting-security` cannot report `CLEAN` through `run_security_verification.py` when credentials are required because the dispatcher strips credential env vars (`SP8-3`; *trigger:* proposal defining dispatcher behavior for credentialed local checks).
  * Conda-native package vulnerability scanning remains open until an offline/zero-dependency advisory source (such as Grype + Syft) is evaluated against conda-forge build strings.
* **`[VER-5]` Unify shipped-executable discovery and multi-script install tests.**
  * Replace separate traversal helpers across install, manifest, security scan, and upgrade with one `shipped_executables()` source (`dev/PLANNING.md`).
  * Populate `_MULTI_SCRIPT_MODULES` in `bootstrap/tests/test_reference_scripts.py` for the remaining multi-file modules beyond `issue-capture` (`coordination-tiers`, `api-access-security`, `web-hosting-security`, `claim-check`, `content-security`, `doc-drift-prevention`).
* **`[TRU-2 / TRU-3]` Source-to-install provenance (`FA-R1`, `RA3`, `RA6`) and Zenodo fingerprint (`REL-4`).**
  * `--cairn-root` in the fork advisory is caller-designated rather than cryptographically verified, and `cairn-lock.yml` provenance fields (`source_repository`, `source_licenses`) are declared rather than signed (*trigger:* when an adopter verifies an install from a checkout they did not clone and verify themselves).
  * Either record the release signing key fingerprint in the Zenodo deposition metadata at release time or mark channel 3 in `bootstrap/PROVENANCE.md` as prospective.
* **`[REL-5 / RB5]` Loop-fidelity prefix scope and release-bar staleness helpers.**
  * `check_cairn.py` checks shipped `templates/**` files for dangling internal references to `doctrine/`, but does not yet check references to `bootstrap/` or Cairn-only `dev/` paths (*trigger:* next edit to `_CAIRN_INTERNAL_PREFIXES`).
  * If the release-security-bar staleness script (`[RB5-1]`–`[RB5-6]`) is revived for a future audit, quote its pathspec array and exclude untracked `dev/.cairn/local-env.json` so `git log` cannot return an empty false-`FRESH` result.

---

## Decision test for new security findings

When a new security finding arrives:

1. **Reproduce it on the canonical interpreter (`Python 3.13.x`).** If it does not reproduce, record the check and do not open work.
2. **Name the protected asset and cluster (`[BND]`, `[VER]`, `[TRU]`, `[REC]`, or `[REL]`).** Put it in one primary cluster.
3. **Check active ownership.** If an open plan already owns the same trust boundary and verification path, fold it there; otherwise keep it separate.
4. **Pick one disposition:**
   * Fix now (with a negative-control test);
   * Queue on [`dev/PLANNING.md`](../PLANNING.md) for the next batch on that boundary;
   * Record as a triggered residual above with an explicit revival condition; or
   * Decline with a stated reason.
5. **Stop once the boundary holds.** Do not build process automation or speculative hardening without a reproduced hazard.
