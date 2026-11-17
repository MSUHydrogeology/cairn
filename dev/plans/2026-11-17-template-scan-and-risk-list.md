# Plan: Shipped prose security read and risk list

**Source proposal**: [Template scan and risk list](../proposals/archive/2026-11-10-claude-template-scan-and-risk-list.md)
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-17
**In brief**: Move template prose security review to the release sweep while retaining protections for code and installer structure.

## Build summary

Remove the per-edit high-risk classification for prose-only template changes and specify a complete, candidate-bound release security read. Update Cairn's scan roots and explain to users that development checkouts may contain prose not yet reviewed for release. The release read and scanners are distinct: scanner silence does not establish safety.

## Source proposal

The accepted heavy proposal authorizes outcomes A–D, including the Maintainer's explicit acceptance of exposure before the release read. It retains other security duties and requires ordinary and Security plan reviews. The v0.8 work starts on `0.8-dev` after group 1 finishes; this plan does not authorize changes to shipped files on `master`.

## Scope

Deliver the authority change in `dev/rules/protected-surfaces.md`, the Rule 7 distinction in `bootstrap/SAFETY.md`, consistent declarations in both proposal templates, the sweep B procedure in `docs/release-process.md`, and the trust distinction in `docs/quickstart.md`. Update `scripts/content_scan_roots.txt` and Cairn's corresponding dispatcher lockfile record. Preserve the adopter starter roots. Inspect the current installer sources, consumers and wording pins before editing; reconcile any affected references or mapped tests without adding development prose byte or phrase pins. The doctrine surfaces are the protected-surface rule, Rule 7 and proposal templates; release and quickstart are procedures for their readers.

N/A: no code added. Reuse the existing scanner, dispatcher, release evidence and sweep B; do not create a new gate or evidence sidecar.

## Sequence

Low execution after both required plan reviews and their author disposition; no implementation until the v0.8 branch exists. Estimate one to two focused workdays plus reviews; the inventory reconciliation and lockfile consumers are uncertain. The release read itself is the existing Maintainer-assigned sweep B operation at each cut, not a final implementation chunk.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Locate authority, install sources, readers, tests and pins; revise the risk and Rule 7 text. | Plan ready; `0.8-dev` | Consistent protection boundaries and proposal templates |
| C2 | Specify the release read and checkout trust distinction. | C1 | Sweep B instructions and quickstart |
| C3 | Change Cairn's scanner roots and lockfile record; exercise controls and verify all chunks. | C1–C2 | Required template scan, evidence and applicable fixes |

## Acceptance criteria

**C1.** Prose-only template changes are exempt from the high-risk list; scaffold engine, protected tests, manifests, lockfile schema, interpreter binding, portable sweeps, all template Python, and installer structure (`cairn:slot`, `{{token}}`, parsed task syntax) remain protected. Mixed structural or code edits remain protected. Rule 7 replaces per-change injection review only for the shipped prose in C2, retaining applicable scanner duties, ordinary review, vendor neutrality, code protection and on-change duties for other agent-loaded content including methodology and case studies. Both proposal templates agree with the authoritative rule. Record the searches for readers and wording pins and resolve affected references.

**C2.** Sweep B directs its Maintainer-assigned security reader to enumerate `git ls-tree -r --name-only <candidate> -- templates`, reconcile that inventory with installer sources, include `docs/agent-team-onboarding.md` and `docs/dev-tour.md`, read every shipped prose source including structured or new formats, and explicitly classify non-prose exclusions. Existing release evidence records candidate ID, covered paths, exclusions, reader, findings and dispositions. It requires `python scripts/check_cairn.py` and `python scripts/content_scan_runner.py`; neither scanner defines read coverage. Missing coverage, failed checks or unresolved unsafe instructions leave readiness unpassed. If candidate bytes change, reconcile inventory, read changed/new shipped prose, rerun affected scans and bind evidence to the final candidate; carry unchanged reads only after byte equality. Quickstart distinguishes unreviewed checkout bytes from the candidate in release evidence while preserving the user's trust decision.

**C3.** Cairn's roots require `!templates` and omit `CLAUDE.md`; the adopter starter remains unchanged and template exact-replacement protection remains through `scripts/prose_roots.txt`. Reconcile the dispatcher lockfile record in the same implementation change. In a disposable tracked tree, exercise both public callers with supported bidi-control and ordinary-prose controls: the content runner distinguishes them in `.md` and `.txt`, and `check_cairn.py` flags the Markdown control but is not claimed to scan `.txt`. Removing required `templates` makes the runner fail. Trial inventory reconciliation with a known onboarding source omitted reports the missing coverage. Record results and limits; these controls do not establish semantic detection or completeness by candidate enumeration alone.

## Verification

Before implementation, run `python tools/test_tiers.py for <changed paths>` and the mapped tests; for governing text pass the reviewed range. Run claim, link, snippet and neutrality prose gates. Verify the actual runner inventory includes tracked template `.md` and `.txt` and excludes `CLAUDE.md`, and record the disposable-tree controls and inventory trial from C3. Check the dispatcher against its reconciled lockfile and retain existing fail-closed behavior. Treat the release read as a procedural obligation, not an automatic gate; the actual candidate read occurs in sweep B and is not claimed by implementation. No scientific check applies. Record the final benefit versus cost and the checks not run; ordinary and Security code reviews remain due.

## Plan review -- Terra Medium -- 2026-11-17

Reviewed commit: 62105804784ba8dafe52d7d099c77751ceccdf7c

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** The accepted outcomes are mapped to focused chunks, but the scan can run on different bytes than the candidate (finding 1). -- plan C1–C3; proposal A–D
2. **Best alternative.** Keep the existing sweep and evidence, adding an explicit candidate-matched scan execution condition rather than a new gate. -- `docs/release-process.md`, sweep B and checks
3. **What would show it wrong?** A changed or dirty checkout producing scan results recorded against another candidate would show the evidence is not candidate-bound. -- `scripts/content_scan_runner.py`, `audit`; `scripts/check_cairn.py`

1. **Blocking -- bind scans to candidate bytes.** C2 binds the read and evidence to the candidate, but only says to run the scanners and rerun affected scans after changes. Both public commands scan their working tree, so a different or dirty checkout can yield scan results for bytes other than the recorded candidate. Require execution against the exact candidate tree, including relevant scanner inputs, and record or verify that identity before carrying results forward. -- plan C2; `scripts/content_scan_runner.py`, `audit`; `scripts/check_cairn.py`

**Audience / rule loss:** The intended loss is per-edit injection review for shipped template prose; C1 retains the other Rule 7 duties and C2 tells checkout users about the remaining exposure. The release reader needs the candidate-matching condition above.

**Coverage:** Read the accepted proposal, plan, template, release roster and checks, installer onboarding sources and scanner entry points. The plan reuses existing sweep and evidence and separates the later release operation from implementation; its stated controls address accepted outcomes. Did not run scanners or the release sweep, independently inventory all installer sources, or perform Security Review.

## Plan review -- Sol High -- 2026-11-17

Reviewed commit: 62105804784ba8dafe52d7d099c77751ceccdf7c

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown
**Model basis**: assigned Sol High Security Review.

**Foundations**

1. **Should this happen as framed?** A–D preserve the accepted exposure tradeoff and code protections, but candidate-bound assurance needs the scan identity condition below. -- source Decision; plan C1–C3
2. **Best alternative.** Use the existing sweep and evidence with explicit candidate-matched scanner execution; no new gate is needed. -- `docs/release-process.md`, sweep B; plan Verification
3. **What would show it wrong?** Scan a checkout whose template bytes differ from the recorded candidate; carrying that result forward would falsify candidate binding. -- `scripts/content_scan_runner.py`, `audit`; `scripts/check_cairn.py`, script-relative inputs

1. **Blocking -- scan the candidate.** C2 binds the read and evidence to a candidate but leaves scanner execution against those bytes implicit. The runner resolves files and policy from its checkout; the Markdown caller likewise reads its checkout. Require both scans against the exact candidate tree, including relevant scanner inputs, and verify or record that identity before carrying results forward. This closes the same gap as the ordinary finding without adding tooling.

**Audience / rule loss:** Per-edit shipped-prose review intentionally disappears with the Maintainer's accepted checkout exposure. C1 retains other Rule 7 duties, Python and parsed installer structure. C2 covers structured prose, both external onboarding sources, exclusions, changed-byte reads and byte-equality carryover. The proposed condition makes the release procedure executable for Low without changing user trust authority.

**Coverage:** Inspected candidate template inventory, installer registries/onboarding delivery, protected surfaces, scanner selection, and dispatcher immutable roots binding against its lockfile record. No further blocker found. Did not read every template for unsafe instructions, execute controls or scans, or run tests/full suites; implementation verification and release reading remain due.
