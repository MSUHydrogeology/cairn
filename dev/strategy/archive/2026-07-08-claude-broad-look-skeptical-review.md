# Cairn's adopter-facing audit — what a skeptical outsider would find

**Author**: Claude (Strategy), Antigravity (Strategy)
**Model**: Claude Fable 5, Gemini 3.1 Pro
**Date**: 2026-07-08; updated for `0.5-dev` 2026-10-26
**Status**: settled
**Type**: product-strategy
**Surfaces this feeds**: [`dev/PLANNING.md`](../PLANNING.md); [`dev/strategy/2026-08-05-codex-security-strategy.md`](2026-08-05-codex-security-strategy.md); the eventual first-adopter comprehension check.

## Summary

Cairn's machinery, installer, and review trail hold up under direct inspection. The adopter path that was broken in earlier audits—where the lightweight level had no installer recipe, onboarding prompts waited on delayed triggers that never fired, and `upgrade` had never been exercised—is now unified on `0.5-dev` under `scaffold.py` (`install`, `upgrade`, `repin`), install-time onboarding, and **Cairn Plain Language 1.0** ([`docs/plain-language.md`](../../docs/plain-language.md)).

What a skeptical outsider would still flag today is narrower and mostly empirical:
1. **No outside-adopter trial yet.** Every deployment so far (`Cairn`, `modflow_tools`, `LHM`, `Assai`) shares one Maintainer.
2. **Prose-meaning drift.** Automated gates verify file paths, links, vendor neutrality, and duplicate rules, but cannot tell when a summary's meaning falls behind a changed rule.
3. **Specific `upgrade` and session-binding edges** documented openly in [`CHANGELOG.md`](../../CHANGELOG.md), [`bootstrap/UPGRADE.md`](../../bootstrap/UPGRADE.md), and [`dev/PLANNING.md`](../PLANNING.md).
4. **Native Windows support** is still not stated at the front door.
5. **The zero-rejections archive optic**, which needs its plain explanation wherever archive numbers are cited: bad ideas are filtered in conversation or strategy notes before a proposal opens.

---

## The two questions

This note combines two audits of Cairn's adopter surface (the 2026-07-08 broad skeptical review and the 2026-06-12 adopter-friction audit, archived at [`dev/strategy/archive/2026-06-12-claude-adopter-friction-audit.md`](archive/2026-06-12-claude-adopter-friction-audit.md)):

1. **The skeptic's question:** If a skeptical, technically competent scientist spent an afternoon reading Cairn's claims, re-running its checks, and walking its install, what would they find that could cost us their trust?
2. **The solo adopter's question:** Can a scientist move from curious, to trying Cairn, to installing and upgrading it on a real repository—and explain what they installed and agreed to—without Cairn's author in the room?

Those four transitions (**try → choose → install → understand**) remain the test for any change to the entry path.

---

## What holds up under inspection

* **Zero external runtime dependencies.** Every shipped Python tool (`bootstrap/scaffold.py`, `scripts/*.py`, `tools/*.py`) uses only the Python 3.13 standard library.
* **Installer containment and symlink safety.** `scaffold.py` refuses symlink traversal, confines writes to the target repository, verifies recorded hashes before overwriting during `upgrade`, and refuses unsafe lockfile paths.
* **One installer across every adoption level.** `scaffold.py` drives `minimal`, `standard`, and `full` installs alike (`dev/proposals/archive/2026-08-20-claude-adopter-path-consolidation.md`). Post-install reports list only the modules installed for the chosen profile and name unfilled slots for uninstalled modules separately (`dev/plans/archive/engine-batch-f8-slots.md`).
* **Install-time onboarding replaces dead triggers.** Delayed trigger-based onboarding prompts that never fired in practice are retired on `0.5-dev` (`dev/proposals/archive/2026-10-26-claude-retire-delayed-onboarding-prompts.md`) in favor of filling project-specific slots during installation.
* **Comprehension is a rule, backed by a style guide.** [`AGENTS.md`](../../AGENTS.md) makes comprehension a precondition of the Maintainer's Decision, and **Cairn Plain Language 1.0** ([`docs/plain-language.md`](../../docs/plain-language.md), [`dev/agent_collaboration.md`](../agent_collaboration.md)) enforces 17 writing rules so agents lead with conclusions and keep what was measured separate from what was assumed.
* **Upgrades are exercised on real repositories.** Cross-version upgrades (`install` → `upgrade --plan` → `upgrade --stage` → `upgrade --apply`, plus `repin`) have been run across sister repositories (`modflow_tools`, `LHM`) and hardened against lockfile-path and merge edge cases.
* **Honest positioning against prior art.** [`docs/related-practices.md`](../../docs/related-practices.md) compares Cairn directly to architecture decision records (ADRs), RFC processes, lab notebooks, and pre-registration, and says plainly where Cairn adds nothing new.

---

## What a skeptical outsider would still find on `0.5-dev`

### 1. Every deployment so far shares one Maintainer (unmeasured)
Cairn has been used on four repositories (`Cairn`, `modflow_tools`, `LHM`, and `Assai`), all led by the same Maintainer. We have not yet run a cold comprehension walk with an outside scientist who did not write the docs—measuring elapsed time, confusion points, terms looked up, and whether they can restate their Decision obligations in their own words—nor a comparative trial against a lighter baseline. Completing the install commands proves the scripts run; it does not prove an outsider understood what they agreed to.

### 2. Prose drift when doctrine changes (structural risk)
`scripts/claim_check.py`, `scripts/link_check.py`, and `scripts/quality_gate.py` catch broken paths, dead links, vendor-specific terms, and duplicated rule blocks. No script catches a strategy note, README paragraph, or comment whose *meaning* has fallen behind a changed rule. The only defense that works is keeping documents short, stating present reality rather than historical roadmaps, and pointing to [`AGENTS.md`](../../AGENTS.md) and [`dev/agent_collaboration.md`](../agent_collaboration.md) rather than restating them.

### 3. Known `upgrade` and ceremony edges (tracked on `dev/PLANNING.md`)
Because `upgrade` is now exercised on real trees, its remaining sharp edges are concrete and documented rather than unknown:
* **Retiring untouched template files on upgrade** — removing shipped files that a newer Cairn version retires when the adopter never edited them (`dev/proposals/archive/2026-10-26-claude-upgrade-removes-untouched-retired-files.md`).
* **Untrusted `.git/config` hooks during dirty-tree checks** — passing `-c core.fsmonitor=false` when `upgrade` runs `git status` on a target repository so a repository's `fsmonitor` hook cannot execute during a read-only check (`dev/PLANNING.md`).
* **Verifying the saved base copy against its recorded hash** before three-way merge (`CHANGELOG.md`, `dev/PLANNING.md`).
* **File-to-directory replacement during `upgrade`** — reporting a clean conflict instead of an `IsADirectoryError` traceback when an adopter replaces a tracked file with a directory (`dev/PLANNING.md`).
* **Re-anchoring (`repin`)** — replacing manual hash and commit-floor edits in `.cairn/cairn.lock` with a single checked `scaffold.py repin` command (`dev/plans/repin-build.md`).

### 4. Windows support is still unstated at the front door
Cairn is tested on macOS and Linux (POSIX). Whether native Windows is supported (via LF line-ending normalization) or unsupported in favor of WSL is still an open Maintainer call (`dev/PLANNING.md`). Until that call is made, an adopter on native Windows gets no upfront warning in [`README.md`](../../README.md) or [`docs/getting-started.md`](../../docs/getting-started.md).

### 5. Small public-surface mismatches
* [`CITATION.cff`](../../CITATION.cff) still titles Cairn *"An Adaptable Framework for Scientist-AI Research Software Teams"* while [`README.md`](../../README.md) and [`AGENTS.md`](../../AGENTS.md) lead with *"Cairn is a methodology, not a framework."*
* The repository does not yet ship a `CONTRIBUTING.md` for outside contributors.
* **The zero-rejections optic:** every proposal in `dev/proposals/archive/` is either `accepted` or `superseded`. To an outsider, zero `rejected` proposals can look like rubber-stamping unless we state the reason where archive counts appear: weak ideas are killed in chat or strategy notes before a proposal is ever opened, and proposals that fail under review are either substantially revised in place or superseded (`dev/strategy/archive/2026-05-20-claude-team-productivity-metrics.md`).

---

## Durable lessons from both audits

* **A claim that checks passed is a claim like any other.** Verification records and release notes carry machine output and the exact Python interpreter (`Python 3.13.x`), never a summary from memory.
* **Derive scanner target lists from the installer's manifest.** Every scanner coverage gap in the original audit came from a hand-copied file list that fell behind `scaffold.py`.
* **Tests must not depend on wall-clock dates.** Date-sensitive tests that turn red on their own train people to ignore failing tests.
* **Adoption levels describe human obligations, not manual file copying.** A lighter adoption level means fewer ceremonies and fewer files to read, not copying files by hand without an installer or lockfile.
* **Report what is active now, not every optional slot.** Installing a template file or leaving an optional slot unfilled should not flood the adopter's day-one report (`dev/plans/archive/engine-batch-f8-slots.md`).
* **Test the exact published command.** A test that checks a helper function without running the documented CLI command and checking the resulting working tree will miss handoff bugs.
* **Strategy notes owe dated corrections when a finding is falsified.** Both audits initially over-reported tool failures that were actually caused by running under the wrong Python environment; recording the correction openly led directly to the canonical-interpreter rule in [`AGENTS.md`](../../AGENTS.md).
