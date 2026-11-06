# Plan: A home for closed measurement records

**Source proposal**: dev/proposals/archive/2026-11-06-codex-measurement-archive-home.md
**Author**: Codex GPT-6.1 Terra (Medium)
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-06
**In brief**: Put proven closed measurement records in an archive and deliver that home safely to adopters who select incident trackers.

## Source proposal

The Maintainer accepted the heavy proposal on 2026-11-06. It retains live
trackers and readers while giving closed records and selected adopters a
tracked archive home; the old strategy list is only a set of candidates.

## Scope

Establish current closure, owner and reader evidence for each candidate before
moving it. Move only proven closed records, preserve their bytes, repair current
references and consumers, and leave uncertain records in place with reasons.
Preserve active ledger append paths and historical references. Deliver a tracked
home for selected fresh installations, explicit module adoption and upgrades
of already-selected modules; preserve unselected behavior, existing content,
idempotence and guarded refusal of unsafe links. Update measurement and module
guidance, and affected install contract, fidelity and manifest surfaces.

**Reuse.** Searches for `incident-trackers`, `_DEV_DIRS`, `install_file` and
module-internal additions found the existing mapping in
`bootstrap/_scaffold/config.py`, guarded tree creation in `install.py` and
upgrade addition handling in `upgrade.py`. Prefer these existing mechanisms;
do not add installer logic if they meet both install paths and selection.

### Documentation / doctrine surface

`dev/measurement/README.md` and the incident-trackers module describe the
live/archive boundary and selected delivery. Software description stays in
existing documentation; no new governing doctrine is proposed.

## Sequence

The existing module mapping, guarded installer and upgrade paths are available
now; no unfinished plan is a prerequisite. Estimate 1–2 workdays including
reviews and verification; closure research, guarded upgrade behavior and
security findings may extend this. A release baseline operation, if needed,
is a separate Maintainer-owned wait, not a plan completion gate.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Map candidates, ownership, readers and installation consumers; classify and move closed records | Usual and Security plan reviews | Preserved history, repaired current references and concise closure evidence |
| C2 | Deliver and explain the selected archive home using guarded existing paths | C1 | Fresh, adoption and upgrade delivery with preservation and refusal evidence |
| C3 | Review and verify the complete change | C1–C2; usual and Security code reviews | Final wide Boundary B and recorded dispositions |

## Acceptance criteria

**C1.** Each moved record has evidence of closure and current owners/readers;
current consumers resolve and live trackers and append destinations remain
usable. Historical record bytes remain unchanged. Uncertain candidates stay
in place with a reason; the old list alone is not proof of closure.

**C2.** Real selected fresh install, explicit adoption and upgrade of an
already-selected module provide a tracked archive home. Unselected paths do
not introduce module content. Repeated runs preserve existing adopter files;
unsafe linked destinations refuse before writes. Module guidance accurately
states selection behavior and the live/archive boundary. Summary, dry-run and
manifest paths agree with the delivered mapping.

**C3.** Both code review obligations and all mapped checks pass. Any expected
engine AST mismatch from reviewed changes is recorded as unpassed pending the
separate release baseline operation; unexpected drift or unexplained integrity
failure remains implementation work.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A: map candidate readers, writers, installer and manifest consumers;
run `python tools/test_tiers.py for <changed paths>` and its selected tests,
including the applicable incident-trackers and upgrade-module-addition tests.
Exercise real install and upgrade entry points for selected, unselected,
repeated, existing-file and linked-destination cases, and live record readers
and writers. Extend owning tests only for uncovered faults. Run applicable
claim, link, snippet and neutrality prose gates and required security checks.
Follow the AST and re-anchor runbooks when applicable; no release operation is
authorized by this plan.

Boundary C: an independent reviewer runs tight falsification checks; a separate
Security Review is also required. Boundary B: after review, run wide on the
clean final commit with canonical Python 3.13.x, the mapped iteration and
integration/workflow checks, public install/upgrade paths, standing gates and
plan-specific cases. Record tested SHA/range, interpreter, clean pre/post
state, commands, counts, timing, non-pass dispositions and omissions. Tree
certification remains a separate authorized ceremony.

## Plan review -- Codex GPT-6.1 Terra (Medium) -- 2026-11-06

**Reviewed commit**: `aac2fcf9417571e30a18e1f9e951a81f05da2faa`
**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: PROCEED
**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**:

1. **Should this happen as framed?** Yes. C1 requires closure and reader evidence before each move, and C2 covers all three selected delivery paths, preservation and refusal; C3 retains both reviews and wide final verification. The 1–2 day estimate is plausible but uncertain because closure research and security findings remain unmeasured. -- Plan Scope, Sequence, Acceptance criteria and Verification; accepted proposal Decision.
2. **Best alternative.** A tracked module file using the existing guarded mapping is the simplest identified route that retains the selected install and upgrade outcomes; the plan already prefers it if sufficient. An unconditional directory or local-only home would lose selection or adopter delivery. -- `bootstrap/_scaffold/config.py` incident-trackers mapping, `bootstrap/_scaffold/install.py` `_DEV_DIRS`, and `bootstrap/_scaffold/upgrade.py` module-internal additions.
3. **What would show it wrong?** A moved record still needed for append or read, missing home on any selected path, content introduced unselected, changed existing file on repeat, or a write through a linked destination would falsify the plan; exercise the real install and upgrade paths and live readers in the specified cases. -- Plan C1–C2 and Boundary A; `dev/measurement/attestation-replay-failures.md`.

**Coverage**: Read the committed plan and accepted proposal, template, review sweep, module mapping, directory and upgrade-addition references, and live ledger evidence. Did not establish each record's closure or run installs, tests or security checks; a separate Internal Security Review remains required.

## Plan review -- Codex GPT-6.1 Sol (High) -- 2026-11-06

**Reviewed commit**: `bfdffc0212afe1e138ae04d368b3c7a6eb73b4d5`
**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none
**Verdict**: PROCEED
**Elapsed**: approximately 5 minutes. **Tokens**: unknown.

**Foundations**:

1. **Should this happen as framed?** Yes. C1 makes closure and current owner/reader evidence prerequisites to movement, preserving history and active append destinations. C2 covers selected fresh installation, explicit adoption and already-selected upgrades without granting target paths more authority. C3 keeps both code reviews, required checks and unresolved integrity failures in implementation. -- Plan C1–C3; accepted source Decision; `dev/measurement/attestation-replay-failures.md` still arms recurrence rather than documenting a closed ledger.
2. **Best alternative.** Prefer a tracked file in the existing incident-trackers mapping, provided the implementation demonstrates every selected delivery path. This preserves the accepted outcome with fewer branches than new directory logic. `_DEV_DIRS` is unconditional; upgrade already enumerates module-internal additions and blocks occupied destinations rather than silently replacing them. A local directory alone loses adopter delivery. -- `bootstrap/_scaffold/config.py:1061`, `bootstrap/_scaffold/install.py:159`, `bootstrap/_scaffold/upgrade.py:997`.
3. **What would show it wrong?** Through real install, adoption and upgrade entry points, try unselected modules, existing content, repeat runs and linked destinations; any unintended content, overwrite or escaped write falsifies C2. For every proposed move, exercise current readers and appenders and compare historical bytes; a broken active ledger falsifies C1. Summary, dry-run and manifest disagreement also fails delivery. -- Plan Acceptance criteria and Verification; `bootstrap/tests/test_incident_trackers_module.py` omission path; `bootstrap/tests/test_upgrade_module_additions.py` occupied-destination and post-stage symlink controls.

**Coverage**: Examined committed scope, Decision, template, live-ledger purpose, selected mappings, directory creation and upgrade collision/refusal design. Closure classification and safety are planned requirements, not measured results here. Did not establish each candidate's closure, execute installation or tests, inspect adopter state, or perform a release/baseline operation; code and security verification remain due.
