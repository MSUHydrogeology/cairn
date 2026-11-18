# Retry the isolated Git upgrade comparison

**Author**: gpt-6.1-terra (Implementation, Medium)
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy — the trial runs Git and installer writes across an isolation boundary
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-18
**Rules that apply**: dev/rules/conventions.md, dev/rules/protected-surfaces.md, dev/rules/working-agreements.md
**In brief**: Retry the stopped comparison of Cairn's upgrade with a Git merge without risking a real project.

## Decision summary

The earlier trial stopped before comparison: restricted Python would not start and two installed files did not reconstruct. Authorize temporary administrator setup in the existing Linux guest to try a confined comparison, or leave it incomplete. Repair the baseline recipe and compare three matched synthetic projects only after the required controls pass. Setup, review and cleanup cost time not yet measured; the result cannot authorize replacement or prove equivalent security.

## Context

The [archived trial plan](../plans/archive/2026-11-12-upgrade-growth.md) records restricted Mac Python exiting 134 and its driver -6; a broader-read preflight did not meet the boundary. Reconstruction matched 37 of 39 destinations: `AGENTS.md` missed the security-module merge and `dev/PLANNING.md` the onboarding overlay. All six comparison cells and classification of 37 hostile cases remain unrun. A fresh strict Mac profile still exited 134 after an approved outer launch; a Linux user namespace failed with EPERM, while an unprivileged Landlock launch needed a directly executable loader and left metadata outside its control. Neither is a qualified boundary. The [accepted source proposal](archive/2026-11-05-codex-upgrade-growth.md) permits an incomplete result, not engine replacement.

## Proposal

If accepted, use the existing local Linux VM instead of the failed Mac profile. Temporarily use guest administrator authority to set up a private filesystem, network and PID view and a uniquely named deny-default AppArmor trial profile. The guest has no host shares; pinned sources and driver are read-only; only the synthetic writable island W and `/dev/null` may be written. Permit only the exact Python and Git applications to execute, with the loader and libraries mapped or read but not directly executed. Drop setup privilege before the trial and remove the temporary profile afterward; do not weaken system-wide policy or alter other projects. This High-tier design candidate is untested. A Decision and reviewed plan are required before administrator setup. Retain the old C0/C1 protections and stop conditions: no comparison writes until a confined constant-print startup and all C0 controls pass. A failure leaves the comparison incomplete; no broader or unconfined fallback is authorized.

Pin the v0.5.0 predecessor, clean candidate, profile, interpreter and Git identities and hashes. Reconstruct the old baseline using the security-module merge, onboarding overlay, conditional sizing and token substitution; compare every applicable destination with an independently saved clean old install and classify unrecorded outputs. A mismatch stops the Git leg. Reuse installer assembly and `install/_scaffold/install.py` lockfile rendering with version differences; `install/_scaffold/upgrade.py` does not infer generated overlays from raw cache.

Use matching customized snapshots for three variants: benign, a committed leaf link to an outside sentinel, and a committed linked parent directory. For each, exercise both the actual `install/scaffold.py upgrade --plan`, `--stage`, `--apply` path and the scratch Git template-branch merge: six cells. Compare conflicts, slot and ordinary-edit preservation, sentinel and outside writes, operator steps and engine modules touched. Record elapsed time, platform, Python and Git versions, identities, configuration, corpus hashes, exclusions and limits. Inventory the original 37 hostile functions and their parameter classes from the archived plan's pinned corpus; classify every one as applicable, inapplicable or untested with reason and remaining protection. Do not imply that classification runs all 37 or proves equivalence.

Reuse the archived plan's fixed driver, trusted Git, verified `dev/tools/git_read.py` and fixtures. The old scratch driver is absent. Retain no new tool or evidence folder unless strictly needed, and add no Maintainer command. Record results in the plan; change no production engine, contract, trust record or real adopter project.

## Rationale

Matching edits and planted links can reveal migration losses and effort without turning failure into a safety claim.

## Alternatives considered

Leave the comparison incomplete without guest administrator setup: this avoids its privilege and cleanup cost but leaves six cells and hostile-case classifications unknown. Replacing the engine now is outside this proposal.

## Documentation / doctrine surface

No doctrine or installed contract change. The proposal and, if accepted, one plan hold deliberation and evidence in `dev/`; temporary drivers and profiles stay in scratch and are removed. Any separately needed production change requires its own proposal.

## Evidence / verification plan

A failed boundary, unreconstructed baseline, unobserved cell or unclassified hostile case leaves the comparison incomplete. An outside write, lost marker or unexpected conflict is a finding, not proof of readiness.

### Tests required

No new permanent test is proposed. Public entry points are the old snapshot's `bootstrap/scaffold.py`, the candidate's `install/scaffold.py` and trusted Git merge. The plan selects exact inputs and checks through `tests/tier_inventory.py`. The arc owner performs one joined integration; no full suite or repeated test family is added.

### Examples / smoke checks

Before comparison writes, prove the constant-print startup and, under the same guest profile, the old C0 outside-write denial and unchanged digest, sentinel positive control and loopback host/child control. Verify the read helper returns the synthetic root and refuses `push --all`. Record guest runtime, exact commands, results and limits. Run claim, link, snippet, neutrality and prose-integrity gates on changed prose; negative searches need known-positive controls.

#### Security preflight — five questions, answered in writing

**S1:** The trial supplies synthetic project paths and data; trusted pinned sources, guest executables and the reviewed plan supply the boundary and commands. Project-controlled Git paths and configuration are untrusted.

**S2:** The denied outside write, changed-sentinel positive control and host/child loopback pair independently challenge confinement and observation; a known-absent marker challenges preservation reporting. The earlier broad-read controls are not a pass for the narrow profile.

**S3:** The reviewed plan binds the exact guest setup, deny-default profile, driver, executable identities and input set to both public paths and the controls. Guest startup and C0 are unproven; neither the Mac nor unprivileged Linux probes establish them.

**S4:** Failed interpreter startup, missing controls, a baseline mismatch or ambiguous output stops the affected writes or leg and remains incomplete. There is no unconfined fallback, production migration or authority to bypass an existing refusal.

**S5:** A hostile synthetic project can plant paths and Git metadata. Confinement controls are finite observations, not proof against all Git behavior, concurrent filesystem races or untrusted executable code; the trial uses no real adopter data.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

The comparison cannot run under demonstrated confinement, cannot reproduce both paths, or its limited cases are presented as a general security or replacement conclusion.

## Scope delta

**Scope delta**: preserved.

## Assurance path

Usual and Security proposal reviews, a heavy plan with Internal and Internal Security Review, then independent ordinary and Security code reviews of the trial and evidence. No implementation, Decision or completed comparison is claimed. Elapsed: unknown; tokens: unknown.

## Review -- Codex Sol (Security Review, High) -- 2026-11-18

Reviewed commit: f9a6211c17157e2621c2b20aad2cf0af64f3fbc5

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Steelman.** A comparison on matched synthetic projects can measure preservation and write behavior without putting adopter data at risk.

**Foundations**

1. **Should this happen as framed?** A retry is defensible once the confined launcher can start. Rebuilding the two omitted overlays and comparing against the saved clean install keeps a guessed baseline out of the trial (Proposal; archived plan lines 124–134).
2. **Best alternative.** Keep the existing operating-system boundary and test the trusted interpreter before building the trial fixtures. Reuse the fixed driver and require all C0 controls before writes (archived plan C0).
3. **What would show it wrong?** A protected write, a confined loopback connection, an undetected sentinel change or an unmatched baseline would stop the affected work (archived C0; S2–S4).

**Blocking — demonstrate a usable strict launch.** Exit 134 and driver −6 do not identify the denied operation. The archived profile file is absent at its recorded path. Before Decision, specify a reproducible deny-default profile with named read-only dependencies, exact executable paths, no network and writes confined to the island and `/dev/null`. Show the canonical interpreter's constant `-I -B -c` print starting under that profile. If outer launch permissions are suspected, compare using the same inner profile bytes. Startup alone clears no C0 pre-write check (archived plan line 124; Proposal S3–S4).

**Coverage.** Read committed records and checked scratch profile presence. No startup probe, sandbox control, Git write or comparison ran. The historical abort remains unexplained.

## Review -- Terra (Reviewer, Medium) -- 2026-11-18

**Reviewed commit**: f9a6211c17157e2621c2b20aad2cf0af64f3fbc5
**Tier**: usual
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: a confined comparison of matched synthetic projects can expose preservation and effort differences without authorizing an engine replacement. -- Proposal, archived upgrade-growth plan C0–C1
2. **Best alternative.** Leave the trial incomplete; it costs no further setup but leaves six comparison cells and hostile-case classifications unknown. -- Context, Alternatives considered
3. **What would show it wrong?** A failed confinement control, unreconstructed baseline or unobserved comparison cell makes the trial incomplete; a lost marker or outside write is a finding. -- Proposal, Evidence / verification plan

The proposal retains the old controls, three variants and full hostile-case classification without claiming equivalence. Its High-tier confinement design is a genuine prerequisite, and a new deny-default profile can address it without recovering old scratch bytes. The larger opening carries the trial boundary and recorded failure, not a permanent harness or Maintainer operation. No doctrine or installed contract change is proposed. Coverage: compared the committed proposal with the archived C0–C1 and review rules; did not run a profile, reconstruct a baseline, execute Git or installer writes, or assess the security boundary. The separate Security Review has a blocking finding.

## Response -- Terra (author) -- 2026-11-18

The Security finding is accepted: neither Mac nor unprivileged Linux established
a usable strict launch. A High-tier bounded diagnostic identified the temporary
administered guest design now proposed, but did not prove startup or C0 under
it. The new host and administrator scope needs fresh proposal reviews and the
Maintainer's Decision; the comparison remains incomplete until controls pass.
The ordinary review raised no findings.

**Elapsed**: unknown. **Tokens**: unknown.

### Withdrawn / superseded commitments

The Mac-only execution mechanism is replaced by the explicit Linux guest option;
the original confinement outcomes, stop conditions and comparison remain.
