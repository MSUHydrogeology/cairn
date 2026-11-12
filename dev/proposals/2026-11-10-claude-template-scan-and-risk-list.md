# Prose templates off the high-risk list; scan all shipped template prose before release

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: heavy — it edits the high-risk list itself and `bootstrap/SAFETY.md` Rule 7.
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-10
**In brief**: Remove prose-template high-risk per-edit friction; replace its injection review with a complete, commit-bound pre-release read, not detector proof. Development checkouts can expose users before that read; acceptance must explicitly acknowledge this tradeoff.

## Decision summary

Today any shipped-template edit is high-risk work. The Maintainer's direction, chat, 2026-11-10:

> "Changing prose templates should not be high risk during the implementation phase. I want to remove that restriction. But a pre-release security scan of all of them is a really good idea."

> "Pinning template bytes seems like a bad idea. They should be pinned on release for some verification or another. But we don't need a bunch of obstacles in the way of updating prose."

> "The content scanner should include all shipped template prose. It should not scan CLAUDE.md as that is not a Cairn product."

Outcomes: (A) prose templates leave the high-risk list; (B) one pre-release scan and security read of all shipped prose, including onboarding docs outside `templates/`; (C) prose bytes pinned at release only; (D) Cairn's scan list gains `templates` and drops `CLAUDE.md`. **Intended release: v0.8.** No new per-edit approval or substitute safeguard is proposed. Code, installer structure and other Rule 7 duties remain protected.

A *high-risk surface* is a file class whose change needs a proposal and Security Review. A *pin* is a test or hash that fails when wording or bytes change. The *content scanner* is a *tripwire*: it flags text that looks like a hidden instruction; silence proves nothing.

## Context

Measured 2026-11-10 at commit 1d21845d:

- `templates/` has 116 tracked files: 64 `.md`, 4 `.txt`, 37 `.py`, 11 other. The 68 prose files total 68,234 words.
- Pins: none of the 150 hashed files in `bootstrap/tests/fixtures/gate_manifest.json` is a `.md` template; its 28 template entries are `.py`. Wording pins are tests: 50 of 125 top-level test files mention `templates/`; I did not count those asserting exact text.
- `scripts/content_scan_runner.py` read 123 files over the 7 roots in `scripts/content_scan_roots.txt`: clean. In a throwaway copy with `templates` added and `CLAUDE.md` dropped: 190 files (123 − 1 + 68), 0 flags.
- `python scripts/check_cairn.py`, already in `docs/release-process.md` (line 138), scanned 204 selected Markdown files, templates included: no issues, 2.5 seconds. Its default filter excludes some tracked Markdown; it skips the 4 `.txt` templates.
- The secrets scanner cannot yet report "clean" (empty approved-build list, `scripts/run_portable_security_sweeps.py`, line 242); not used here.

These are historical measurements, not the next release inventory. Detector coverage excludes `.json`/`.yml`; the release read must inspect any prose they carry.

## Proposal

Intended release: v0.8.

**A.** Change the authoritative high-risk list in `dev/rules/protected-surfaces.md`, not `AGENTS.md`, to exempt prose-only template changes. Preserve protection for the scaffold engine, protected tests, install/fidelity/gate manifests, lockfile schema, interpreter binding, portable sweeps, and every `.py` under `templates/`. Installer structure (`cairn:slot`, `{{token}}` and parsed task syntax) is not prose. Reconcile both proposal-template declarations. In `bootstrap/SAFETY.md` Rule 7, replace per-change injection review only for shipped prose in B with release review; retain applicable scanner duties, ordinary review, vendor neutrality, code protection and on-change duties for other agent-loaded content, including methodology and case studies. Mixed structural/code edits remain protected.

**B.** The Maintainer-assigned sweep B security reader reads the exact release-candidate commit before each cut. Enumerate tracked `templates/` with `git ls-tree -r --name-only <candidate> -- templates`, reconcile against installer sources, and include `docs/agent-team-onboarding.md` and `docs/dev-tour.md` (`install_onboarding`). Read every shipped prose source, including prose in new formats or structured files; classify non-prose exclusions explicitly. Record candidate ID, covered paths, exclusions, reader, findings and dispositions in existing release evidence. Run `python scripts/check_cairn.py` and `python scripts/content_scan_runner.py`; their narrower selections do not define read coverage. Missing coverage, failed checks or unresolved unsafe instructions leave release readiness unpassed. No new code.

**C.** No new byte or phrase pins on development prose. Bind release evidence to the candidate commit and path inventory, not a count alone. If the candidate changes, reconcile coverage, read changed/new shipped prose bytes, rerun affected scans and bind evidence to the final candidate before release. Unchanged reads may carry forward only after byte equality is established. The `.py` hashes stay.

**D.** Add required `!templates` to Cairn's `scripts/content_scan_roots.txt`; drop `CLAUDE.md`. Leave the adopter starter unchanged (optional `CLAUDE.md`). Reconcile Cairn's dispatcher lockfile record in the same implementation change. The runner scans tracked `.md`/`.txt`, excluding base cache and archives; `check_cairn.py` scans Markdown with its default exclusions. Neither covers every format. `CLAUDE.md` leaves this scan and, absent another root, functional-prose exact-replacement protection; templates retain it through `scripts/prose_roots.txt`.

## Rationale

The release read consolidates assurance but is not equivalent protection: `docs/quickstart.md` clones the default branch and installs from it before a release read. Update that guidance to distinguish unreviewed source bytes from the candidate identified in release evidence, without removing the user's trust decision. Earlier exposure is the explicit price of lower per-edit burden, not a claim that risk starts at release.

## Alternatives considered

1. **Do nothing.** Loses no assurance; keeps the friction.
2. **Least involved: retain the protected-surfaces rule; exempt prose-only template edits case by case.** Loses relief (each exemption is a fresh argument) and any guaranteed full read. Keeps per-edit assurance.
3. **Scan only (B, D).** Keeps heavy review per edit; no relief.
4. **A to D.** Gives up per-edit Security Review; a planted instruction may reach source-checkout users before the release read.

**Recommendation: option 4**, matching the Maintainer's lower-burden direction. Read cost is unmeasured; the historical template inventory alone suggests about 90,000 tokens (68,234 words at ~1.3 tokens/word), before onboarding prose. Being wrong means unsafe instructions can reach users earlier or survive the read.

**Human operations added** (estimates): option 1: 0; option 2: 0, plus about one exemption disposition per template-editing plan; option 3: 0; option 4: 0 recurring (sweep B is already assigned each cut), 1 one-time (the Decision). Recurring addition (option 4): one recorded read per release.

## Documentation / doctrine surface

`dev/rules/protected-surfaces.md`; `bootstrap/SAFETY.md` Rule 7; `docs/release-process.md` sweep B; `docs/quickstart.md`; `dev/proposals/_template.md` and `templates/core/dev/proposals/_template.md`; Cairn's roots manifest and lockfile record. Implementation must locate readers and wording pins before edits; this revision changes only this proposal.

## Evidence / verification plan

Implementation checks the actual runner inventory includes template `.md` and `.txt` and excludes `CLAUDE.md`; run only mapped tests, including roots/dispatcher consumers selected for changed files. Release coverage is established by the recorded read and installer reconciliation, not these tests.

### Security preflight

**S1 -- Inputs.** Scan selection comes from candidate tracked paths, roots manifest, extensions and exclusions; scanner, allowlist, residual baseline and lockfile supply interpretation/authority. The candidate supplies these inputs itself. The reader uses installer sources and shipped prose from that same candidate: independent judgment, not an independent authenticity root. Existing release provenance duties remain.

**S2 -- Failure controls.** Use a known supported bidi-control fixture and ordinary-prose negative control, not an arbitrary malicious sentence: direct scanner must distinguish them for `.md` and `.txt`; `check_cairn.py` must flag the Markdown fixture, not the unsupported `.txt`. At implementation, exercise both public callers in a disposable tracked tree with the proposed roots, and remove required `templates` to demonstrate runner failure. For the procedural read, omit a known onboarding source from a trial inventory; reconciliation must report missing coverage. These runner/coverage trials are not yet run; current direct-detector evidence is recorded below. Candidate-derived enumeration alone cannot prove its own completeness. No control promises detection of every malicious instruction.

**S3 -- Trigger/scope.** Existing release sweep B owns the read and commands in B; proposed adopter-facing wording: "Release evidence identifies the candidate and shipped prose read for unsafe instructions; development checkouts may contain prose not yet read. Scanner silence is not proof of safety." The quickstart must carry this distinction alongside its existing user trust decision. Scanner exclusions in D remain visible; the read covers shipped prose they omit.

**S4 -- Failure direction.** Required-root absence, malformed manifest, containment/resource errors and stale residual authority make the runner incomplete/failing, not clean; findings are advisory and need disposition. Optional absent roots, extension filters, archive/base exclusions and `check_cairn.py` defaults reduce detector coverage. They do not excuse missing read coverage. A missing read record or changed bytes without recheck cannot inherit release approval. This is a procedural obligation, not a new automatic gate.

**S5 -- Residual attacker.** Assume an attacker can plant prose in a development candidate. Semantically plausible hostile instructions can evade patterns and reader judgment; source-checkout users can encounter them before release. Control of scanner/policy or installer selection can also defeat self-audit. No new safeguard is silently imposed; acceptance requires the Maintainer's explicit acknowledgement of the source-checkout exposure, and never grants agents users' trust decisions.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

- A release read finds a hidden instruction that per-edit review would have caught earlier.
- A "prose" edit breaks install or upgrade (structure edited as prose).
- A supported detector control goes unflagged, shipped prose is omitted from the read, or release bytes differ without recheck.

## Scope delta

**Scope delta**: preserved -- A-D remain; coverage and residual exposure are made explicit, not reduced.

**Unresolved Decision question:** Does the Maintainer accept removing per-edit prose-template Security Review despite unreviewed source-checkout exposure, with the release read and user-facing distinction specified here? No additional safeguard is proposed or authorized by this revision.

## Assurance path

**Assurance path**: high-assurance — touches the security reference.

## Review -- Terra Medium -- 2026-11-12

Reviewed commit: be015399831b62898f10696191cd60b1b325a6c1

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

The strongest case is less friction for prose edits while checking the entire shipped instruction supply before release, with scanners treated as tripwires rather than proof.

**Foundations**

1. **Should this happen as framed?** Not yet: the proposed replacement needs a defined boundary for unreleased installs and a realizable control (findings 1-2). -- `docs/quickstart.md` Steps 1-2; `scripts/check_cairn.py`
2. **Best alternative.** Retain the per-change instruction review until the release-only boundary and its residual exposure are explicit; still add the full release read. -- `bootstrap/SAFETY.md` Rule 7
3. **What would show it wrong?** Try the stated positive control in both a tracked `.md` and `.txt` template through both public scanners; inability to detect the planted instruction would falsify the promised control. -- `scripts/content_scan_runner.py`; `scripts/check_cairn.py`

1. **Blocking.** Release review does not cover a development checkout: the quickstart clones the default branch and runs that copy for its exercise; real projects are directed to a verified release. Removing per-change review therefore exposes the former path before the proposed read. Close by specifying the intended protection or explicit residual and how users are told which bytes were reviewed. -- `docs/quickstart.md` Steps 1-2; `bootstrap/SAFETY.md` Rule 7
2. **Non-blocking.** The positive control requires both scanners to flag one template, but `check_cairn.py` skips `.txt`, four files in the stated inventory. Specify separate `.md` and `.txt` controls and which scanner must catch each; do not imply both cover the latter. -- proposal Context and Evidence / verification plan
3. **Non-blocking.** Define the release read's enumeration, reviewer record and failure handling, including new prose formats, rather than relying on a file count. This also matters to the separate style-guides proposal, whose shipped prose would enter that inventory. Close with a reproducible inventory and release-step ownership. -- proposal B; `docs/release-process.md`

**Audience / rule loss:** Rule 7's per-change injection review is intentionally weakened; the proposed release read needs an actionable owner and scope for an agent without a person-level decision in context.

**Coverage:** Read the committed proposal, Rule 7, release process, scanner selection and quickstart; did not execute scanners, independently recount historical figures, or assess the separate Security Review. The positive-control result remains unverified.

## Review -- Sol High -- 2026-11-12

```
Reviewed commit: be015399831b62898f10696191cd60b1b325a6c1
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown
**Model basis**: coordinator's explicit Sol High assignment.

The strongest case replaces repeated prose-edit security reviews with one
complete, commit-bound release read, retaining protection for code and installer
structure.

**Foundations**

1. **Should this happen as framed?** Only with complete coverage and operative
   rule changes; the high-risk authority moved. --
   `dev/rules/protected-surfaces.md`, high-risk list
2. **Best alternative.** Keep A-D, explicitly reconciling existing duties with
   the release read. -- `bootstrap/SAFETY.md`, Rule 7
3. **What would show it wrong.** A shipped instruction source missing from the
   recorded read falsifies completeness. -- `bootstrap/_scaffold/install.py`,
   `_ONBOARDING_DOC_NAMES`

1. **Blocking: wrong authoritative home.** A targets a high-risk list no longer
   in `AGENTS.md`. Close by specifying the change in
   `dev/rules/protected-surfaces.md` and reconciling template declarations.
2. **Blocking: substitution coverage is ambiguous.** B enumerates only
   `templates/`; Rule 7 also governs other agent-loaded prose. Close by including
   the two onboarding documents shipped from `docs/` and explicitly preserving
   existing duties outside the replacement set. --
   `bootstrap/_scaffold/install.py`, `install_onboarding`
3. **Blocking: required preflight absent.** No new execution path does not exempt
   a named high-risk change. Close with S1-S5, including scan-selection inputs,
   failure controls and remaining attacker capabilities. --
   `dev/proposals/_template.md`, Security preflight

**Audience / rule loss:** Per-edit Security Review deliberately disappears;
release instructions must explicitly replace it. Removing `CLAUDE.md` also
removes exact-replacement protection.

**Coverage:** I verified historical counts: 116 templates, 68 prose files,
68,234 words; 150 frozen files, including 28 Python templates, at cited ancestor
1d21845dccc1019d86d32e48ea0240b5c9020770. A bidi-character positive control
triggered `scripts/content_scan.py`; ordinary prose did not. Not covered:
complete release scan, dispatcher execution or semantic attack detection.
This records the initial pass after ordinary-review serialization, not another
pass. Any word-target overrun preserves the three closures and coverage evidence.

## Response -- Sol High -- 2026-11-12

**Role**: revising author; High security-policy judgment (assigned Sol High).
**Elapsed**: unknown
**Tokens**: unknown

1. **Ordinary 1 -- accept.** The top, rationale and S5 explicitly expose default-branch users before release review. The Decision must acknowledge that tradeoff; quickstart wording preserves the user's trust decision. I decline retaining per-edit friction as the alternative because it defeats the Maintainer's stated goal.
2. **Ordinary 2 -- accept.** Replace arbitrary malicious-text detection with a supported bidi control; distinguish Markdown caller coverage from `.txt` and semantic detection limits.
3. **Ordinary 3 -- accept.** B-C specify owner, candidate, installer-reconciled inventory, new formats, evidence, failures and changed-byte rechecks.
4. **Security 1 -- accept.** A targets the actual protected-surfaces home and reconciles authoring-template declarations.
5. **Security 2 -- accept.** Include both shipped onboarding docs; retain other Rule 7 duties and code/structure protection.
6. **Security 3 -- accept.** S1-S5 now identify candidate-controlled inputs, failure trials, triggers, exclusions and residual attackers, without adding per-edit safeguards.

I reread and revised the top. In an isolated source copy, ordinary prose produced zero direct-detector flags; adding U+202E produced `unicode-bidi`. Claim, single-file prose and snippet checks passed; neutrality had zero failures. No tests selected by the path mapper; no proposal-specific reader/pin references found in tests/tools/scripts (search matched the known-positive security-stack filename). Public-runner and inventory trials remain implementation work. Session-start and default snippet discovery failed repository discovery; explicit-file snippet checking passed. No suite or release sweep ran.

### Withdrawn / superseded commitments

Superseded: obsolete `AGENTS.md` edit location; template-directory-only read; count-only release binding; both-scanners/arbitrary-instruction control; claim that exposure begins at shipping; twice-skipped-read tolerance. Their replacements close the findings without dropping A-D. No new safeguard or Decision is adopted.

## Decision -- Maintainer (scribed by Antigravity Gemini 4 Hydrogen) -- 2026-11-12

**Tier**: heavy

**ACCEPTED.**

> "Accept both as revised, acknowledging the development-checkout tradeoff on template scanning"

This accepts the v0.8 proposal as revised (outcomes A–D, explicitly acknowledging the development-checkout exposure tradeoff prior to the pre-release read). New recurring human operations: zero (uses the existing per-release sweep B read).

**Elapsed:** under 1 minute. **Tokens:** unknown.
