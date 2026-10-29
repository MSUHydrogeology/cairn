# Report directories occupying tracked upgrade paths

**Author**: Codex GPT-6
**Status**: revising
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


## Review -- Codex GPT-6.1 Sol -- 2026-10-29

```
Reviewed commit: 4662a3df71caea3db3c1aa5ecf2850d49bda7a97
Target: opening proposal, Context through Assurance path
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: none
**Verdict**: ACCEPT

**Foundations**:

1. **Should this happen as framed?** Yes. Preserve adopter contents and replace
   the traceback with a useful per-file block. The ordinary-record read occurs
   before classification, unlike retired records; the earlier reproduced folder
   case independently supports the reported failure --
   `bootstrap/_scaffold/upgrade.py:668`;
   `dev/proposals/archive/2026-10-26-claude-upgrade-removes-untouched-retired-files.md`,
   case 7 and review F7.
2. **Best alternative.** Refuse the entire command before reading any tracked
   directory. That is simpler but discards the useful unaffected-file plan.
   Reuse the existing unconditional apply block, with a directory-specific
   diagnostic and no file review pair or adoption authorization --
   `bootstrap/_scaffold/upgrade.py:1032` and
   `bootstrap/_scaffold/upgrade.py:3112`.
3. **What would show it wrong.** A successful apply after the directory appears,
   changed contents, advanced blocked metadata, or no recovery after moving the
   directory aside and restaging would defeat the proposal. Existing stage-time
   snapshots read files directly, so classification alone cannot deliver this --
   `bootstrap/_scaffold/upgrade.py:1137` and
   `bootstrap/_scaffold/upgrade.py:3140`.

The proposed outcome is appropriately small: no new ownership or automatic
cleanup, and an operator can retain the folder elsewhere, restore the intended
file or choose its absence, then make a new stage. Doing nothing preserves an
already-recorded failure, rather than avoiding speculative work.

For the eventual plan, keep the distinction between **reusing a block** and
**reusing addition recovery** explicit. Existing blocked-addition guidance offers
`--adopt-collisions`, while its stage path makes file-based review buffers
(`bootstrap/_scaffold/upgrade.py:1190`). A tracked directory should inherit
neither behavior. The proposal's preservation and hard-block requirements already
exclude those outcomes; this is implementation guidance, not a scope addition.

The public-command test requirement is sound; existing public stage/apply cases
have a home in `bootstrap/tests/test_upgrade.py`. Include the override flags in
the refusal cases, verify unchanged lockfile and base-cache bytes as well as
folder contents, and exercise an existing stage whose original file becomes a
directory. Keep a blocked stage blocked even if the operator fixes the live path
without restaging. These concretize the stated hard-block and new-stage contract.
The preflight correctly distinguishes between-command changes from hostile
concurrent filesystem races; the plan must keep that limit explicit.

Coverage: claims, public-path test design, failure behavior, recovery, existing
reuse, documentation placement and scope were assessed against the named commit;
`bootstrap/UPGRADE.md` owns software guidance and `dev/PLANNING.md:61` records
this defect. No scientific result or doctrine changes. I did not rerun the
scratch reproduction, implement a fix, run mutation checks or any suite, or
establish resistance to concurrent hostile writers. This usual pass does not
clear the separately declared Security Review.

## Review -- Codex GPT-6 Security reviewer -- 2026-10-29

```
Reviewed commit: c4b6a46376153131ef376aead82f715e3fd1637e
Target: opening proposal and usual review
Prior findings: none
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: none
**Verdict**: ACCEPT

**Foundations**:

1. **Should this happen as framed?** Yes. A folder occupying a tracked file's
   name must remain adopter-owned and block application, rather than become
   missing-file recovery or an acknowledged omission. The current file read
   precedes classification -- `bootstrap/_scaffold/upgrade.py:668`.
2. **Best alternative.** Refuse the entire operation on the first directory.
   That protects contents but loses the useful unaffected-file report. Reusing
   unconditional blocking, without addition adoption or review buffers, delivers
   the proposed protection with less new authority --
   `bootstrap/_scaffold/upgrade.py:1032` and
   `bootstrap/_scaffold/upgrade.py:3112`.
3. **What would show it wrong.** A folder appearing after classification or
   staging still produces a traceback, permits a write, or advances its record;
   or a repaired live path unlocks an old blocked stage. Classification alone
   cannot meet the contract: later file reads remain --
   `bootstrap/_scaffold/upgrade.py:1137` and
   `bootstrap/_scaffold/upgrade.py:3140`.

The design protects the right asset: adopter contents, including nested files,
without authorizing deletion, flattening, adoption or a substitute file. The
usual review's override and unchanged-metadata probes are appropriate. A hard
block should precede application writes and metadata advancement; the useful
unaffected-file information need not mean partial application of a blocked stage.

For the plan, spell out the observation points rather than only adding an
`is_dir` classification. A normal file may become a directory between computing
plans and writing the stage, or between stage and apply. Stage's no-op comparison,
snapshot and review-buffer reads are separate exposure points. A controlled
transition at these boundaries must leave contents intact and give a recoverable
refusal. This follows the opening's occupied-path-between-commands requirement,
not a request to contain arbitrary concurrent hostile writers.

Keep directory detection subordinate to existing path containment and symlink
refusals. A symlink to a directory is not permission to follow or remove its
referent; symlinked parents and dangling links must retain their refusal behavior.
The existing write guard rejects destination and ancestor links, and the
lockfile-path tests explicitly exercise outside and dangling referents --
`bootstrap/_scaffold/security.py:110`;
`bootstrap/tests/test_upgrade_lockfile_path_containment.py:484`. Include these
consumers in the plan's mapping. Recovery should move retained contents aside,
restore the intended file or absence, and create a fresh stage; no cleanup
command or stronger race-resistance promise is needed.

Covered: claims and failure paths (`upgrade.py:668`, `:1137`, `:3140`);
public-path test design and containment consumers
(`bootstrap/tests/test_upgrade_lockfile_path_containment.py`); design, reuse and
scope (Proposal, Alternatives, S4–S5); documentation and lifecycle placement
(Documentation / doctrine surface, Assurance path). No scientific assumptions
are touched. Not covered / low confidence: no implementation exists to verify;
I did not execute mutations, reproduce the scratch failure, run a suite, or
establish protection against filesystem changes after a check. S2 explicitly
leaves mutation evidence for implementation; this acceptance clears the proposal
Security Review, not the future plan or code obligations.
