# Retry the isolated Git upgrade comparison

**Author**: gpt-6.1-terra (Implementation, Medium)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — the trial runs Git and installer writes across an isolation boundary
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-18
**Rules that apply**: dev/rules/conventions.md, dev/rules/protected-surfaces.md, dev/rules/working-agreements.md
**In brief**: Retry the stopped comparison of Cairn's upgrade with a Git merge without risking a real project.

## Decision summary

The earlier trial stopped before comparing either approach: its restricted environment could not start Python, and its recipe did not rebuild two installed files. Diagnose those failures, repair the trial recipe, and compare both approaches on the same three synthetic projects. Record what each preserves, writes and costs, including the existing hostile-case inventory. This buys evidence for a future decision, not a replacement or a claim that Git is equally safe. The trial takes development and security-review time; its cost is not yet measured.

## Context

The [archived trial plan](../plans/archive/2026-11-12-upgrade-growth.md) records a harmless Python print exiting 134 and the driver exiting -6 under the restricted macOS profile. A broader-read preflight passed some controls but did not meet that plan's read boundary. Reconstruction matched 37 of 39 recorded destinations: `AGENTS.md` missed the security-module merge and `dev/PLANNING.md` missed the onboarding overlay. All six comparison cells and classification of 37 hostile cases remain unrun. The [accepted source proposal](archive/2026-11-05-codex-upgrade-growth.md) permits an incomplete result but does not authorize replacing the upgrade engine.

## Proposal

If accepted, retry the entire comparison in disposable synthetic repositories, retaining the old plan's C0/C1 controls and stop conditions. Diagnose the interpreter failure without reading secrets or relaxing isolation by assumption. A High-tier designer resolves which narrowly scoped reads let Python start while retaining exact-executable, write-island and no-network controls; the old narrowed macOS profile failed. Broad reads, allow-default or an unconfined fallback do not clear it; a different isolation mechanism requires an explicit proposed change. Stop writes and record incomplete if the required boundary or controls cannot be demonstrated. A Decision and reviewed plan precede trial writes.

Pin the v0.5.0 predecessor, a clean candidate, profile, interpreter and Git identities and hashes. Reconstruct the recorded old baseline using the old install's actual security-module merge and onboarding overlay, alongside conditional sizing and token substitution; validate all applicable recorded destinations against an independently saved clean old install and classify unrecorded installation outputs. A mismatch stops the affected Git leg, not a guessed ancestor. Reuse the existing installer assembly and `install/_scaffold/install.py` lockfile rendering as evidence, while respecting version differences; `install/_scaffold/upgrade.py` explicitly declines to infer generated overlays from raw cache alone.

Use matching customized snapshots for three variants: benign, a committed leaf link to an outside sentinel, and a committed linked parent directory. For each, exercise both the actual `install/scaffold.py upgrade --plan`, `--stage`, `--apply` path and the scratch Git template-branch merge: six cells. Compare conflicts, slot and ordinary-edit preservation, sentinel and outside writes, operator steps and engine modules touched. Record elapsed time, platform, Python and Git versions, identities, configuration, corpus hashes, exclusions and limits. Inventory the original 37 hostile functions and their parameter classes from the archived plan's pinned corpus; classify every one as applicable, inapplicable or untested with reason and remaining protection. Do not imply that classification runs all 37 or proves equivalence.

Reuse the archived plan's fixed-driver, trusted Git and verified `dev/tools/git_read.py` approach and fixtures. The former local scratch island has an empty `drivers/`; it is not evidence. Recreate disposable inputs as needed; retain no new tool or evidence folder unless implementation strictly needs it, and add no Maintainer command. Record observations in the plan; change no production engine, install contract, trust record or real adopter project.

## Rationale

Matching edits and planted links can reveal migration losses and effort without turning failure into a safety claim.

## Alternatives considered

Leave the trial unrun: this avoids its setup and review cost but leaves all six comparison cells and the hostile-case classification unknown. Replace the engine now: that risks adopter work without the promised comparison and is outside this proposal.

## Documentation / doctrine surface

No doctrine or installed contract change. The proposal and, if accepted, one plan hold deliberation and evidence in `dev/`; temporary drivers and profiles stay in scratch and are removed. Any separately needed production change requires its own proposal.

## Evidence / verification plan

A comparison is incomplete if confinement fails, either baseline mismatch remains, a cell is unobserved, or a hostile case is unclassified. An outside write, lost marker, unexpected conflict or unaccounted case is a finding, not proof of readiness. Report unfavorable and incomplete outcomes honestly; do not reduce accepted scope to obtain a clean result.

### Tests required

No new permanent test is proposed. Public entry points are the old snapshot's `bootstrap/scaffold.py`, the candidate's `install/scaffold.py` and trusted Git merge. The plan selects exact inputs and checks through `tests/tier_inventory.py`. The arc owner performs one joined integration; no full suite or repeated test family is added.

### Examples / smoke checks

Before writes, demonstrate under the same restrictive profile: a protected outside write is denied and its digest unchanged; a deliberately changed sentinel is detected and restored; a host loopback connection succeeds while the confined child is denied. Verify the read helper returns the synthetic root and refuses `push --all`. Record exact commands, results and limits. Run claim, link, snippet, neutrality and prose-integrity gates on changed prose; negative searches need known-positive controls. Use `/Users/kendal30/conda_envs/lhm/bin/python3.13` on Mac.

#### Security preflight — five questions, answered in writing

**S1:** The trial supplies synthetic project paths and data; trusted pinned sources, host executables and the reviewed plan supply the boundary and commands. Project-controlled Git paths and configuration are untrusted.

**S2:** The denied outside write, changed-sentinel positive control and host/child loopback pair independently challenge confinement and observation; a known-absent marker challenges preservation reporting. The earlier broad-read controls are not a pass for the narrow profile.

**S3:** The reviewed plan must bind the exact confined driver invocation, profile, executable identities and input set to these controls and both public paths before execution; the archived plan's `sandbox-exec` and public command forms are the starting point, not an observed success on the new run.

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
