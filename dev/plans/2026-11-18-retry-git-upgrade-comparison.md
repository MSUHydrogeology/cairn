# Plan: Retry the isolated Git upgrade comparison

**Source proposal**: dev/proposals/archive/2026-11-18-terra-retry-git-upgrade-comparison.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-18
**Rules that apply**: dev/rules/conventions.md, dev/rules/protected-surfaces.md, dev/rules/working-agreements.md, dev/rules/development-environment.md
**In brief**: Compare a Git merge with Cairn's upgrade on matched synthetic projects inside a verified guest boundary.

## Build summary

Use the existing Linux guest for one controlled comparison, after a reviewed guest setup and nonvacuous confinement controls. Reconstruct the prior install faithfully, run both paths against three identical variants, and record the outcomes and limits. A failed control stops the comparison; no result authorizes an engine replacement.

## Source proposal

The Maintainer accepted the revised heavy proposal and temporary guest administrator setup under a reviewed plan. The earlier Mac trial stopped before comparison; the Linux isolation candidate is untested. Approval includes neither a broader fallback nor release of existing protections.

## Scope

Use the shared `linux-dev` guest described in `dev/rules/development-environment.md`; do not alter other projects or global policy, add packages or create a VM. Create an owned temporary workspace with no host shares. Pin the v0.5.0 source `3bb27388fccaf51ae490e80ca4b4ab94aa5e2206`, a clean candidate commit, guest Python and Git, profile, driver and corpus hashes. The recorded Mac interpreter is `/Users/kendal30/conda_envs/lhm/bin/python3.13`; record the guest runtime actually used. Synthetic inputs only; no production engine, installed contract, trust record or real adopter data changes. No doctrine surface changes.

The reviewed setup must make a private filesystem, network and PID view and install a unique deny-default AppArmor trial profile. Pinned sources and driver are read-only; only the synthetic writable island W and `/dev/null` are writable. Allow exact Python and Git applications to execute, with loader and libraries read or mapped but not directly executable. Drop setup privilege before trial, deny network, remove the temporary profile and owned workspace afterward, and verify cleanup. No comparison writes precede startup and all C0 controls; no unsafe fallback.

**Design prerequisite, High:** the exact privileged setup and cleanup commands, namespace and mount construction, AppArmor rules and dependency paths, privilege-drop proof and safe failure cleanup are not yet specified. A High-tier designer must fill these operative cells before the required plan reviews; this draft does not authorize guest changes or delegate that design to the implementer.

**Reuse.** The archived `dev/plans/archive/2026-11-12-upgrade-growth.md` C0–C1 supplies the bounded driver, controls, Git isolation settings and corpus. Searched `install/_scaffold/install.py` and `install/_scaffold/upgrade.py`: installer assembly includes module-merge and onboarding overlays; raw-cache reconstruction deliberately excludes generated overlays. Reuse those version-appropriate routines and verified `dev/tools/git_read.py`; old scratch drivers are absent. Temporary drivers belong in scratch, with no retained tooling or evidence folder unless strictly needed.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Set up the private guest view, prove startup and C0 controls | High design and both plan reviews | Controlled trial island and recorded evidence |
| C2 | Reconstruct old baseline and compare six matched cells | C1 passes | Trial results and 37-case classification |
| C3 | Remove owned guest profile and workspace; record cleanup | C1 setup, including failures | Cleanup evidence and remaining limits |

## Acceptance criteria

**C1.** Under the same final restrictive profile, the pinned Python `-I -B -c` constant print succeeds after privilege drop. A write to a protected outside canary is denied and its parent-observed digest unchanged; deliberately alter W's outside sentinel, detect it and restore it. A controlled guest-side unsandboxed loopback reaches its listener; the confined child cannot connect and is not observed. The verified read helper returns the exact synthetic root and refuses `push --all` without launch. Record exact commands, profile and hashes, outputs and limits. Failure stops comparison writes and remains incomplete; earlier broad-read probes do not satisfy C0.

**C2.** Reconstruct each recorded predecessor destination from verified base hashes, conditional sizing and tokens, with the actual security-module merge for `AGENTS.md` and onboarding overlay for `dev/PLANNING.md`. Compare bytes against an independently saved clean install; classify unrecorded install outputs. A mismatch stops the Git leg. From identical customizations run benign, committed leaf-link and committed linked-parent variants through both Git merge and public `upgrade --plan`, `--stage`, `--apply` (six cells). Record conflicts, marker preservation, sentinel and outside changes, operator steps, modules exercised, migration result, timings, platform, versions, hashes, exclusions and limits. Classify all 37 pinned hostile functions and parameter classes applicable, inapplicable or untested, with reason and remaining mechanism; this is not a security-equivalence claim.

**C3.** On success or failure, remove only the owned profile and scratch root without following planted links; verify absence and unchanged unrelated policy and projects. Failure to establish cleanup stays open. No routine human action is a final chunk.

## Scope delta

**Scope delta**: preserved

## Verification

Before implementation, map changed paths with `tests/tier_inventory.py`; use applicable claim, link, snippet, neutrality and `tests/check_cairn.py` prose gates and known-positive controls for negative searches. C1's setup and control commands, exact read dependencies, privilege and cleanup proofs must be supplied by the High design before review; startup alone does not satisfy them. C2 uses the old snapshot's `bootstrap/scaffold.py`, candidate `install/scaffold.py` and trusted Git. Retain the archived C1 controlled Git environment, empty hooks/templates, configuration checks, isolated home/temp, timeout/process-group handling and no execution of target-installed code. The driver uses temporary artifacts only; no permanent promise test is required solely for observations. Record elapsed time, tokens and all failures. Independent ordinary and Security code reviews follow; the arc owner runs one joined integration at the arc end.
