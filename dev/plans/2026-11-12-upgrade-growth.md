# Plan: Bound upgrade growth and trial Git merge

**Source proposal**: dev/proposals/archive/2026-11-05-codex-upgrade-growth.md
**Author**: gpt-6.1-terra (Medium), plan author
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-12
**In brief**: Require an evidenced threat for new upgrade refusals and compare the existing upgrade with an isolated Git merge.

## Build summary

Add the accepted review rule without weakening existing protections, then measure one finite comparison on synthetic projects. A failed or incomplete comparison is a result; it authorizes no engine replacement. The temporary trial uses an operating-system write boundary, not production machinery or a new shipped framework.

## Source proposal

Decision `15264bf4` accepted both outcomes and no scope reduction. The source Proposal 1–3 and its security preflight govern the rule, controls, comparisons and reporting. The High-tier trial design was supplied by gpt-6.1-sol on 2026-11-12; it is design input, not a Security Review or a waiver.

## Scope

Add the rule to `AGENTS.md` review guidance: every proposed new upgrade refusal identifies attacker, controlled input, harmful action, threat-model connection and distinguishing evidence or test. Outside-model risk needs the Maintainer's explicit disposition; unexplained threats and unmet protection stay open. Existing refusals and checks remain. This is governing doctrine; explanatory methodology belongs in `docs/methodology/` only if needed. Record trial evidence here; do not change the engine or installed contract.

Reuse: searches of `bootstrap/_scaffold/{upgrade,merge,security,lockfile}.py`, `bootstrap/container/recipe.md` and `bootstrap/tests/test_upgrade_refuses_hostile_project_data.py` found the real CLI, merge, containment, recorded bases, existing containment pattern and hostile cases. Use those, the verified `tools/git_read.py`, system Git and macOS `sandbox-exec`; no new shipped launcher or harness. Scratch drivers and profiles are developmental and removed after evidence is recorded.

## Sequence

Estimate two focused windows plus review and verification; uncertainty is whether the untried sandbox profile and recorded-base reconstruction work on the host. C0 establishes the available read boundary and safe trial island locally; C1 ships rule and bounded trial evidence. Neither depends on a future plan review or archive.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C0 | Pin sources and establish read and confinement controls below. | Plan reviews | Recorded controls or incomplete trial |
| C1 | Rule and matched comparison below. | C0 controls pass for writes | Governing rule and observations, including negative/incomplete outcomes |

### C0: source and isolation

Use canonical `/Users/kendal30/conda_envs/lhm/bin/python3.13` on macOS; freeze candidate `326f9474eeae060c655e4a5ed051d9639187c0c7` (or explicitly pin a later clean commit and compare relevant bytes) and v0.5.0 `3bb27388fccaf51ae490e80ca4b4ab94aa5e2206`. Verify `tools/git_read.py` and its template twin match SHA256 `a1c54924ef70e15d583ed265aba1fbaa3195554f7e29e36fdd726cb7cc322cec` and trusted caller. In the synthetic repo, its public `run_git` must return the exact canonical root for `rev-parse --show-toplevel`, and `('push','--all')` must return failed/`unsupported-read-form` without launch. This uses existing reviewed and cap-accepted 3.13 mechanism plus local controls, not a claim that Safe Git's final wide Boundary B passed. That separate obligation remains open.

Create a canonical temporary root outside the project, with frozen committed source exports, driver, profile and protected canary outside writable island W; W holds synthetic copies, home, temp, empty hooks/templates, logs and outside sentinel. Resolve and hash trusted Python and Git outside W; recheck before each spawn. Run fixed driver with `/usr/bin/sandbox-exec -f PROFILE PYTHON -I -B DRIVER` and a fresh environment, no credentials or agent/socket, `PYTHONDONTWRITEBYTECODE=1`, PATH limited to trusted Git's parent. Deny by default, allow needed reads, mappings, process and interpreter facilities; allow exec only those exact Python and Git paths, writes only W and `/dev/null`, and no network. Never execute target-installed code. Do not broaden to allow-default or an unisolated fallback if it fails.

Under the same profile prove a mode-0600 outside canary write is denied and its parent-observed digest unchanged; deliberately alter W's outside sentinel and detect its changed digest, then restore it. An unsandboxed loopback connection must reach a controlled listener; the sandboxed child connection must be denied and not observed. Failure of any control or runtime stops writes and records incomplete. Use DEVNULL stdin, bounded captured output, 60-second command and 15-minute driver limits; on timeout kill the owned process group before bounded reap. Snapshot and cleanup never follow planted links; remove only the owned canonical temporary root after recording evidence. Profile and commands are temporary evidence, not shipped code.

### C1: comparison

Use trusted Git directly for writes, not the read-only helper. Initialize scratch repositories with empty templates; synthetic author, committer and fixed dates; `HOME`, `XDG_CONFIG_HOME`, `TMPDIR` in W; `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_ATTR_NOSYSTEM=1`, `GIT_TERMINAL_PROMPT=0`, `GIT_NO_LAZY_FETCH=1`, `LC_ALL=C`. Prefix every Git call with `-c core.hooksPath=EMPTY -c core.fsmonitor=false -c core.attributesFile=/dev/null -c core.pager= -c core.editor=/dev/null -c sequence.editor=/dev/null -c commit.gpgSign=false -c tag.gpgSign=false -c protocol.allow=never -c protocol.file.allow=never -c gc.auto=0 -c maintenance.auto=false -c submodule.recurse=false`. Check known local config before each call: no includes, aliases, external filters or drivers, remotes or submodules. Copy full synthetic `.git` without alternates, hardlinks or gitfiles; do not use clone protocol. The exec restriction is a backstop. Existing `merge.py` uses the frozen Git via PATH unchanged.

Profile: `project_name: UpgradeTrial`, `test_command: pytest`, `preset: solo-greenfield`. Install old source with `python bootstrap/scaffold.py --config PROFILE --target A --cairn-root OLD --allow-dev --non-interactive`; render candidate into B with the same command and profile. In A fill a project-conventions slot with `TRIAL_SLOT_KEEP`, append `TRIAL_ORDINARY_KEEP` to `dev/README.md`, and commit. Copy identical snapshots for each path and three variants: benign; committed `dev/proposals/_template.md` symlink to an outside sentinel file; committed `dev/proposals` symlink to an outside directory with `_template.md` sentinel. Before each path record sorted lstat types, modes, targets and regular-file hashes, marker bytes and outside inventory/digests.

Build template baseline T0 from A's recorded ancestors: check cached raw bytes against each `base_hash`, apply existing `strip_conditional_regions` and `substitute_tokens` using the old profile; for verbatim records require pristine old-install bytes match. Compare reconstructed destinations to clean A; a mismatch is a negative migration result and stops that prototype leg, never substitute a guessed baseline. Exclude Git and runtime/lock/base/profile bookkeeping, name exclusions and report stale inert metadata; include other supported installed destinations. Build T0 and candidate T1 with Git `hash-object -w`, temporary `GIT_INDEX_FILE`, `read-tree --empty`, `update-index --index-info`, `write-tree`, `commit-tree` and `update-ref refs/heads/cairn/template`; T1's parent is T0. The adopter commit has T0 as parent and the entire same customized snapshot, including metadata and link. Run `git merge --no-ff --no-commit --no-edit --no-stat cairn/template`; record exit, unmerged stages and bytes, no auto-resolution. In the matched copy run candidate `scaffold.py upgrade --target TARGET --cairn-root NEW --plan`, then `--stage`, then `--apply`; a refusal or conflict is a result, never bypassed.

## Acceptance criteria

### C0

The pinned read controls and three nonvacuous isolation controls above pass before comparison writes. A denied write leaves the protected digest unchanged; the positive sentinel and loopback controls prove observation. Record profile, commands, results and limits. Any missing control stops writes and is an incomplete trial, not a safety conclusion.

### C1

The rule retains existing protections and assigns out-of-model risk only to the Maintainer. For each path and variant record conflicts/count, marker preservation or loss, sentinel and outside changes, operator steps, engine modules exercised, migration result, elapsed time, platform, Python/Git versions, source/config/profile/corpus hashes and limitations. Inventory all 37 hostile-test functions and their parameter classes from the pinned source; label each applicable, inapplicable or untested with reason and remaining mechanism. Only three variants run; no security equivalence or replacement readiness is claimed. More conflicts, lost edits, sentinel writes or unaccounted cases falsify readiness. A blocked or unfavorable trial remains an honest result; future replacement requires a separate proposal.

## Scope delta

**Scope delta**: preserved.

## Verification

Before implementation use `/Users/kendal30/conda_envs/lhm/bin/python3.13 tools/test_tiers.py for <changed paths>`; for `AGENTS.md` pass the reviewed range. Run its mapped readers and pinned-prose checks, plus claim, link/content, snippet and neutrality gates. The real install and upgrade CLI and Git merge are the trial entry points; no permanent tests are required solely for scratch observations. Boundary C is targeted ordinary and Security code review. Boundary B is wide for governing and trust surfaces, after review on a clean unchanged commit: mapped readers, owning and public paths, standing prose gates and the trial controls and evidence. Record commands, outcomes, tested SHA, interpreter, pre/post state, elapsed time, non-passes and omissions. Certification is separate.


## Plan review -- GPT-6.1 Sol (Security Review, High) -- 2026-11-12

Reviewed commit: `abd8efdb`.

**Obligation**: Internal Security Review
**Tier**: Internal
**Findings**: none
**Verdict**: APPROVE
**Elapsed**: approximately 12 minutes, shared across both plans.
**Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: the review rule preserves existing protections, and the synthetic comparison requires frozen trusted code, operating-system write confinement, exact executable restrictions and no network before writes -- Scope, C0 and source Proposal 1–3.
2. **Best alternative.** Retain the three matched variants and applicability inventory instead of building a shipped harness or replaying the full hostile matrix; this measures the accepted question with less continuing burden -- C1 and Acceptance criteria.
3. **What would show it wrong?** A successful protected write, undetected sentinel change or observed sandboxed loopback connection stops the trial; missing controls must be incomplete rather than safety evidence -- C0 controls and C1 reporting.

I found no new boundary design left to the executor: C0 fixes write and executable authority, source hashes, environment, command/process limits, cleanup and refusal behavior; runtime-specific profile syntax must satisfy those fixed constraints or stop. Safe Git's reviewed component is distinguished from its unpassed final Boundary B. Trusted direct Git writes are distinct from the read-only helper. Recorded-base reconstruction must match the old install; mismatches cannot be repaired by guessing. No rule weakens, no engine replacement is authorized, and temporary developmental probes need no permanent test contract.

**Coverage:** I compared the committed plan, accepted source, current template and Safe Git/merge entry-point source; the 37 hostile-test functions need classification, not full runtime replay. I did not run profiles, controls, Git writes, comparisons, tests or suites. Only the previously reported availability probe exists; executable provenance and actual confinement remain implementation evidence. This pass grants neither Safe Git archive clearance nor trial success.


## Plan review -- GPT-6.1 Terra (ordinary reviewer, Medium) -- 2026-11-12

Reviewed commit: `abd8efdb35cf0480fed488bebd88360336cd6609`.

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: approximately 10 minutes across both queued plans.
**Tokens**: unknown.

The plan measures whether a simpler upgrade approach merits further work while retaining today's protections.

1. **Should this happen as framed?** Yes. C0 and C1 deliver both accepted outcomes without making an engine replacement or another plan's archive a prerequisite. The source permits an honestly incomplete trial; C0's stop conditions preserve that distinction -- source Proposal 1–3; plan Sequence and Acceptance criteria.
2. **Best alternative.** Keep the fixed three variants and classify the existing hostile cases instead of building a reusable trial framework or replaying every case. This meets the comparison objective with temporary machinery -- C1; the current hostile-test file contains 37 test functions.
3. **What would show it wrong?** Failure to reconstruct the recorded baseline, observe the sentinel, or preserve a customization must appear as a negative result, not a guessed baseline or replacement recommendation -- C0 controls and C1 reconstruction/reporting.

The assigned executor has source identities, environment, command limits, write authority, controls and comparison inputs. Platform profile syntax remains implementation detail constrained by a stop, not permission to redesign isolation. The source's prerequisite remains a locally verified reviewed Git boundary; its unrun final integration is explicitly not claimed passed. The governing rule belongs in installed instructions; trial observations belong here. No existing protection weakens or disappears.

**Coverage:** Compared accepted scope, current template, helper/merge/config entry points and the hostile-test inventory; verified the named token renderer also exists in `slotmerge.py`. No sandbox, command-control or comparison execution, runtime tests, Security clearance or final integration was performed. Those outcomes remain unmeasured.
