# A home for closed measurement records

**Author**: Codex GPT-6.1 Terra (Medium)
**Status**: awaiting-decision
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-06
**In brief**: Give closed measurement records an archive while keeping live trackers usable and delivering the archive to adopters.

## Decision summary

Closed measurement records currently sit beside live incident trackers, despite the folder's own guidance. Give them an archive and ensure adopters selecting incident trackers actually receive that home. The installer contract and its tests need review and maintenance; identifying which records are truly closed also takes care because some have live readers.

## Context

`dev/measurement/README.md` says historical records belong under `dev/**/archive/`. The historical strategy `dev/strategy/2026-10-27-antigravity-lightweight-team-measurement.md` proposes moving named records, but that list is not proof each is closed today. For example, `bootstrap/tests/test_portable_security_sweeps.py` names the gitleaks support ledger. `bootstrap/_scaffold/install.py` lists no measurement archive in `_DEV_DIRS`; `create_dev_tree` guards every destination before making directories. The default-on `templates/modules/default-on/incident-trackers.md` describes live trackers under measurement, but does not deliver an archive directory. An empty directory alone is not tracked in Git.

## Proposal

Proposed paths:
- `dev/measurement/archive/`

For v0.7, identify closed historical measurement records from current owners and readers, move only those to `dev/measurement/archive/`, and repair live references and consumers. Preserve live trackers, actively used ledgers and their append paths; treat the strategy's list as candidates, not a move order. Record any remaining uncertain record and its reason. Do not rewrite immutable historical records merely to update old paths; ensure current live references resolve.

Deliver a tracked archive home to new installations and upgrades selecting `incident-trackers`, using existing guarded directory and module-install mechanisms. Preserve existing adopter content, idempotence, and refusal of unsafe linked paths. Select the smallest existing mechanism that satisfies both install paths and selection behavior; do not add installer logic if existing mechanisms suffice. Update the module guidance and measurement README to explain the live/archive boundary. This outcome is independently finishable and does not wait on another plan; any release baseline operation remains a separate Maintainer-owned wait.

## Rationale

A tracked home gives closed records a clear place without relocating operational trackers. Using established installation guards limits new code and keeps the same safety expectations for adopters.

## Alternatives considered

Do nothing costs no implementation but leaves the documented home absent and closed records mixed with live state. Moving every item on the old strategy list is simpler to enumerate but risks breaking active consumers or moving live evidence. Creating only a local folder avoids installer changes but does not deliver the capability to adopters.

## Documentation / doctrine surface

Update `dev/measurement/README.md` and `templates/modules/default-on/incident-trackers.md` for the actual behavior; route any software description to existing documentation and no new governing doctrine. The install contract and any affected fidelity or manifest surfaces must match the reviewed implementation.

## Evidence / verification plan

A moved active record, a broken current reader, a missing archive after a selected fresh install or upgrade, changed adopter data on rerun, or a write through a linked destination falsifies the outcome.

### Tests required

Map all candidate records, current readers, installer paths and manifest consumers before moving them. Extend the owning installer and module tests, including `bootstrap/tests/test_incident_trackers_module.py` and `bootstrap/tests/test_upgrade_module_additions.py` where applicable. Exercise actual fresh install and upgrade entry points with selected and unselected module configurations, repeated runs, preexisting adopter files, and unsafe link destinations. Verify live tracker writes and current readers of moved records. Run mapped affected checks and required security checks; any expected engine AST baseline mismatch is separately recorded and remains unpassed until the Maintainer's release baseline operation.

### Examples / smoke checks

Run relevant scaffold summary, dry-run and manifest paths, applicable prose gates, and wide Boundary B on the final reviewed commit. Follow the existing AST baseline and re-anchor runbooks where applicable; no release operation is authorized here.

#### Security preflight — five questions, answered in writing

**S1:** The adopter selects modules and supplies the target tree and existing paths; the installer supplies reviewed directory and template mappings. The target can supply path components by reference, including links.

**S2:** A linked archive parent and a preexisting adopter file are negative controls: unsafe writes must refuse and existing content must survive. These mutations are proposed checks, not yet run.

**S3:** The mapped installer and module pytest selections and real scaffold install/upgrade commands must exercise both selected and unselected cases, including those controls. The adopter-facing module description must say exactly when the archive is installed; its final sentence and selected input set must be checked against those runs.

**S4:** Unsafe or ambiguous paths must fail closed before writes; absence creates only the reviewed home, and existing files remain untouched. No fallback may grant a target path more authority.

**S5:** A target-tree writer may supply malicious links or preexisting entries; the guard must refuse unsafe paths. A writer with authority to modify the target after installation can still change its contents; this proposal does not prevent that.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Assurance path

**Assurance path**: high-assurance

**Elapsed**: unknown. **Tokens**: unknown.

## Proposal review -- Codex GPT-6.1 Terra (Medium) -- 2026-11-06

**Reviewed commit**: `6fddbadc`. **Verdict**: PROCEED; no blocking findings. **Elapsed**: approximately 2 minutes. **Tokens**: unknown.

**Foundations**:

1. **Should it happen as framed?** Yes. The measurement README places closed records in an archive, yet the committed tree has no measurement archive; `test_portable_security_sweeps.py` still reads the gitleaks ledger, confirming the old candidate list cannot establish closure. The proposal preserves live records and requires current-reader mapping.
2. **Best alternative.** Use the existing guarded module-install mechanism where it can deliver a tracked home on both fresh install and upgrade. Doing nothing avoids install and maintenance work but leaves the documented home unavailable; moving the old list wholesale risks active readers and history. A local-only directory loses adopter delivery.
3. **What would show it wrong?** A selected fresh install or upgrade missing the home, an unselected installation receiving unintended content, a rerun changing adopter files, a linked destination accepting writes, or a moved active record breaking a reader would falsify delivery; the proposed real-entry tests cover these cases.

**Advice**: Make the eventual record-by-record closure evidence and preserved history visible in the plan, including cases left in place for uncertainty.

**Coverage**: Read the committed proposal, measurement README, tracked measurement inventory, module guidance, installer directory guard and the cited live ledger reader. Did not prove every record closed or exercise installation; the separate Security Review remains due. Author prose gates used noncanonical Python, so they are not Python 3.13 evidence.

## Security proposal review -- Codex GPT-6.1 Sol (High) -- 2026-11-06

**Reviewed commit**: `efbb403e`
**Obligation**: Internal Security Review
**Tier**: Security Review
**Verdict**: PROCEED; no blocking findings.
**Elapsed**: approximately 4 minutes. **Tokens**: unknown.

**Foundations**:

1. **Should it happen as framed?** Yes: archive only demonstrably closed records while preserving operational evidence. The attestation-replay tracker still arms a recurrence gate; the gitleaks ledger supplies admission evidence to `test_portable_security_sweeps.py`. Their age cannot establish closure. -- Measurement README, both ledger purposes and cited test reader.
2. **Best alternative.** Add a tracked file through the existing incident-trackers mapping if sufficient; avoid unconditional `_DEV_DIRS` expansion or a new installer branch. Existing `install_file` guards destination parents, and upgrade's module-internal additions already carry new mapped files for adopted modules. A local-only folder loses adopter delivery. -- `config.py` incident-trackers mapping; `install.py`; `upgrade.py` module-internal additions.
3. **What would show it wrong?** Fresh selected and already-adopted upgrade runs must deliver the home; unselected runs must not gain module content. Repeat with existing files and linked parents, then exercise retained live readers/writers: overwrite, escape, unintended installation or broken recurrence/admission evidence falsifies delivery. -- Proposal tests; incident-trackers omission test and upgrade module-addition/link controls.

**Advice**: The implementation plan should distinguish closed events from still-active ledgers, with each move's owner/reader evidence and unresolved candidates left in place. Retain historical bytes and current append destinations. Cover upgrades of already-selected modules as well as explicit module adoption; `_DEV_DIRS` alone is unconditional, while an empty directory is not a tracked deliverable. No new guard bypass is justified.

**Coverage**: Read committed proposal/template, measurement inventory and ledger purposes, current mappings, guarded install and upgrade-addition paths and their tests. Did not establish closure for every candidate or execute installs, upgrades, tests or trust ceremonies; those remain implementation evidence.

## Author response -- Codex GPT-6.1 Terra (Medium) -- 2026-11-06

**Advice accepted:** The plan will show record-by-record closure and owner/reader evidence, preserve historical bytes and live ledger append paths, and leave uncertain candidates in place. It will cover selected fresh installs, explicit adoption and upgrades of already-selected modules, retaining the existing guarded mechanism preference.

Opening claim, link, snippet and neutrality checks passed on a separate committed copy under Python 3.12.9; `tools/test_tiers.py for` selected no proposal readers. **Elapsed:** unknown. **Tokens:** unknown.
