# Report directories occupying tracked upgrade paths

**Author**: Codex GPT-6
**Status**: awaiting-review
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Report a directory where an upgrade expects a tracked file, while preserving its contents.

## Context

`bootstrap/_scaffold/upgrade.py` reads each ordinary tracked destination as a file before classifying it. In a scratch installation, replacing the tracked `.agents/skills/session-end/SKILL.md` file with a directory caused both `upgrade --plan` and `upgrade --stage` to raise `IsADirectoryError` through `scaffold.main`. The archived retired-files proposal recorded the same failure and repaired retired records only (`dev/proposals/archive/2026-10-26-claude-upgrade-removes-untouched-retired-files.md`, case 7 and F7). The Maintainer promoted the general defect in `dev/PLANNING.md`.

## Proposal

Classify an ordinary tracked destination occupied by a directory as a blocking conflict with an actionable diagnostic. Both plan and stage must finish without a traceback and preserve the directory and its contents; apply must not replace it or advance its record until the operator resolves the collision and creates a new stage. Define the stage and apply behavior using the existing hard-block machinery where suitable, including an occupied path appearing or changing between commands. Cover mergeable and verbatim records, nested destinations, and unaffected files. Keep retired-record behavior intact.

## Rationale

A directory may contain adopter work; treating it as an absent file or a review-only file that can be acknowledged risks replacing or silently advancing it. An explicit hard block gives the operator a recoverable path without losing contents.

## Alternatives considered

Doing nothing retains the traceback. Treating a directory as missing hides the collision; copying its contents into a file review pair misrepresents the object. Refusing the entire command is simpler, but loses the useful per-file plan and unaffected-file information.

## Documentation / doctrine surface

Describe the blocking diagnostic and recovery in `bootstrap/UPGRADE.md`, the domain's software guidance. No doctrine change is proposed; deliberation remains in `dev/`, consistent with `docs/DOCUMENTATION_PLAN.md`.

## Evidence / verification plan

### Tests required

Add public-command tests under `bootstrap/tests/` for plan, stage and apply with directory collisions on mergeable and verbatim tracked destinations, nested paths, contents preserved, unaffected files, and collision appearing after stage. Verify resolution followed by a new stage and apply; retain retired-record coverage. The plan must map owning tests, consumers and standing gates, and record Boundary B on the final implementation commit. Certification is separate.

### Examples / smoke checks

Exercise the public commands in a scratch installation. Run `python scripts/check_cairn.py` and applicable claim, link, snippet and neutrality checks for changed prose. Engine changes require the existing Maintainer-run AST re-anchor; this proposal does not authorize it.

#### Security preflight — five questions

* **S1:** The adopter supplies the lockfile and destination filesystem; Cairn supplies upstream templates. The object classified is therefore supplied by the project.
* **S2:** A test must fail if a directory is classified as absent or an apply block is removed. These mutations have not yet been run.
* **S3:** The public `upgrade --plan`, `--stage` and `--apply` commands select tracked destinations from the lockfile. The eventual guidance must say that a directory collision blocks application until resolved and restaged; the plan must reconcile that sentence with the tests.
* **S4:** A directory or changed destination fails toward a block, never replacement or automatic advancement. The plan must specify errors and races without granting more authority.
* **S5:** An actor can modify project paths between commands; checks must detect a collision at application. An actor able to race filesystem operations after a check may still succeed unless the plan establishes a stronger boundary; do not claim arbitrary hostile concurrent writers are contained.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A directory or its contents can be overwritten, a blocked record advances, an ordinary valid file cannot be upgraded, or a resolved collision lacks a workable recovery path.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance
