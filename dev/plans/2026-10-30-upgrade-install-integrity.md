# Plan: Protect upgrade bases and install output

**Source proposal**: dev/proposals/archive/2026-10-29-codex-upgrade-install-integrity.md
**Status**: ready-to-implement
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Check upgrade ancestors before merging and make supplied names recognizable in paths and output.

## Source proposal

The Maintainer accepted the revised proposal: check saved merge ancestors and bind staged results to the evidence checked, refuse specified invisible path characters, and escape supplied names in output. Preserve work and provide recovery; the digest is consistency evidence, not authentication.

## Scope

Change `bootstrap/_scaffold/upgrade.py`, `install.py`, and `cli.py`, shared helpers where appropriate, their tests, `bootstrap/UPGRADE.md` and relevant descriptive install/lockfile guidance. No doctrine surface. The existing Maintainer-run AST re-anchor remains required; this plan does not authorize baseline installation or old-anchor reconciliation.

**Stage and apply.** Stage records each automatic result’s source, destination and cache identity, expected digest and digest of the exact checked bytes. Apply compares the current record and bytes to that snapshot, then revalidates immediately before each automatic destination write; a changed or unreadable record or cache stops that write and lockfile advancement. Earlier unaffected writes may already have occurred: report them, retain staged data and original bad cache, and allow a safe restage and retry without overwriting adopter edits. This bounds changes observable at the checks, not arbitrary concurrent writes between a check and write; tell operators to stop concurrent writers. Recovery stores the preserved bad cache separately and establishes the new upstream ancestor at a distinct safe cache path before advancing provenance; failures leave the old evidence and adopter content recoverable. 

**Reuse.** Searching `bootstrap/_scaffold` for `base_hash`, `_contained_lockfile_path`, `print_report`, and `fidelity_warnings` found existing digest production, shared path admission, report rendering and merge output. Extend the review-only and stage/apply mechanisms, and existing display escaping, rather than duplicate them. Search test consumers with `rg` for those symbols and command flags before implementation; update the mapping below if further consumers are found.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Verify ancestors, bind stage to checked evidence, and implement recovery | Both plan reviews | Upgrade behavior, recovery and public-command tests |
| C2 | Enforce character policy and escape supplied names at all output routes | C1 and both plan reviews | Admission, display, tests and descriptive guidance |
| C3 | Record stable verification and hand off for independent code and Security reviews | C1–C2 complete | Boundary B evidence and review handoff; AST ceremony remains Maintainer-run |

## Acceptance criteria

### C1

Hash raw saved bytes against a well-formed `sha256` base digest before decoding; merge that same read. Missing, malformed, mismatched, unreadable or invalid UTF-8 evidence, including legacy records without a valid base digest, produces review-only, preserving the adopter file and original bad cache. Public plan, stage and apply tests cover matching control and a crafted loss case. Recovery tests reconcile the affected file, acknowledge review-only, advance unaffected files, preserve the bad cache as evidence, and complete a subsequent upgrade with a valid new ancestor derived from the applicable upstream template, never silently from the adopter file. Document exact operator steps and digest limitations.

### C2

Retain existing containment and path-shape restrictions. At shared admission reject Unicode categories Cc and Cf, U+034F and variation selectors in source, destination and cache paths; escape rejected values in diagnostics. Permit decomposed accents and visible non-Latin names; test zero-width, bidi, terminal controls, contextual joiners and selectors. Explain the compatibility cost and a supported recovery for existing refused names without hand-editing tool-owned provenance. Escape supplied module and slot names for display, preserving ASCII readability and distinguishing literal backslashes from escapes; lookup uses unchanged names. Public commands cover unknown modules, unpaired-marker warnings, normal and absent-module slot reports, and merge and fidelity output. No claim of complete protection against visual deception.

### C3

Run the mapped checks and scratch install/upgrade, including the recovery sequence; record results and omissions against the exact clean implementation commit. In separate scratch copies, remove the digest check and display escaping respectively: relevant behavior tests must fail, with controls passing. Record each mutation and outcome. Security preflight S2 is exercised here; S3 is the public commands and gates below. Unmet checks keep the work open. The existing AST ceremony is not performed by this plan's implementation agent.


## Scope delta

**Scope delta**: preserved.

## Verification

The reviewed command, input, test and wording mapping is `dev/plans/2026-10-30-upgrade-install-integrity/public-paths.md`.

Boundary A uses the canonical Python 3.13 interpreter and scoped tests. For ancestor and recovery behavior run `python -m pytest bootstrap/tests/test_upgrade.py bootstrap/tests/test_upgrade_lockfile_path_containment.py bootstrap/tests/test_upgrade_side_door_parity.py`; for module addition and provenance consumers run `python -m pytest bootstrap/tests/test_upgrade_module_additions.py bootstrap/tests/test_lockfile_provenance.py`; for display and install paths run `python -m pytest bootstrap/tests/test_install_report_slots.py bootstrap/tests/test_install_module.py bootstrap/tests/test_module_merge.py bootstrap/tests/test_scaffold.py`. Add public-command tests in the owning files and include their files in these commands. Split selections within the broad-run guard's file limit and reconcile the union; do not override the guard. Search actual readers and extend this mapping if affected consumers are missing.

Exercise `python bootstrap/scaffold.py upgrade --target <repo>` with `--plan`, `--stage`, `--apply` and `--apply --ack-review-only` in a scratch project, and `bootstrap/scaffold.py` install with normal, absent and unknown module cases. The new behavior tests must cover all C1/C2 cases, not just the smoke. Run `python scripts/claim_check.py` on changed documentation, `python scripts/check_cairn.py`, `python scripts/link_check.py`, `python scripts/sync_doc_snippets.py` where synced snippets change, and `python scripts/quality_gate.py --sub neutrality` for prose. Run `python -m pytest bootstrap/tests/test_security_lint.py` for the engine Bandit gate, treating a skip as an unmet check; do not run the full suite here.

Boundary B is **wide** for the engine contract and security boundary: repeat the mapped owning families, public paths, mutation and standing gates on a clean, unchanged final implementation commit under the canonical interpreter. Record tested SHA and reviewed range, interpreter, clean pre/post state, commands, outcomes, timing, non-pass dispositions, omissions, and **Certified by**: pending. Certification is separate. Boundary C is independent targeted falsification by the code reviewer, including the set of output routes and staged-evidence changes; the reviewer records bounding and any missing check. An AST re-anchor follows its existing Maintainer-run ceremony, separately authorized.


## Plan review -- Codex GPT-6 -- 2026-10-30

```
Reviewed commit: 353fb15cde122dcd4489dea77075269e96acb48b
Target: operative plan, accepted proposal and named production paths
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** The recovery and character-policy criteria carry the accepted outcomes, but the entry-point mapping is incomplete before implementation -- `dev/plans/2026-10-30-upgrade-install-integrity.md`, Verification.
2. **Best alternative.** Keep the existing review-only recovery and shared admission path, and complete the route-to-test mapping in the plan rather than adding another recovery mechanism -- `bootstrap/_scaffold/upgrade.py`, `_apply_upgrade`; `bootstrap/_scaffold/install.py`, `print_report`.
3. **What would show it wrong.** A supported recovery cannot preserve the bad ancestor and reach a later upgrade, or a named output route lacks a public test that checks the displayed value -- `dev/proposals/archive/2026-10-29-codex-upgrade-install-integrity.md`, Current contract.

**PR1: Complete the reviewed entry-point and wording mapping before implementation.** The accepted security preflight requires the plan to enumerate entry points and reconcile the exact adopter-facing wording with the selected tests before implementation. The plan instead says to check help and entry points and search for consumers before implementation, and groups output paths under broad test families. For example, `install.py` emits unpaired-marker warnings while `cli.py` emits merge and fidelity results; their distinct routes are not mapped to commands and tests. This leaves the author to decide coverage after the one plan review. Enumerate each public entry point and selected input, map each named output and recovery route to its owning test file or node, and reconcile the planned adopter-facing wording with those assertions in the operative cells. Retain all accepted routes and the scoped guard-respecting runs.

**Coverage:** Compared accepted current contract, recovery, character policy, stage binding, public paths and verification with the plan; inspected the named production output routes and template requirements. No implementation, command execution, timing or Windows rendering was tested. This pass clears only the ordinary Internal obligation.


## Plan review -- Codex GPT-6 Security reviewer -- 2026-10-30

```
Reviewed commit: a40d1e88f1ae19feb317aed8468ea37275727e92
Target: operative plan, accepted proposal, ordinary review and engine boundaries
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** The plan preserves the accepted raw-byte check, stage binding, recovery and display policy, but leaves the promised race handling undefined -- `dev/plans/2026-10-30-upgrade-install-integrity.md`, C1; `dev/proposals/archive/2026-10-29-codex-upgrade-install-integrity.md`, Current contract.
2. **Best alternative.** Extend the existing stage metadata and pre-write apply gates with an explicit evidence snapshot and revalidation contract; no new authentication or general transaction system is needed -- `bootstrap/_scaffold/upgrade.py`, `_write_stage` and `_apply_upgrade`.
3. **What would show it wrong.** A cache or digest change after an initial apply check still permits an automatic write, or failed recovery replaces the original bad cache -- `bootstrap/_scaffold/upgrade.py`, `_apply_upgrade`, file swap and new-base refresh.

**SRP1: Define the race and preservation contract before implementation.** C1 requires invalidation “including race/error paths,” but does not say when evidence is revalidated, what snapshot is compared, or what state survives a late failure. The accepted contract explicitly requires the plan to define races. Existing apply reads the lockfile before entering `_apply_upgrade`, performs several gates, writes staged destinations, then overwrites new-base cache paths and finally replaces the lockfile. Simply comparing cache/digest agreement once at entry would leave a later change unaddressed; comparing only current agreement would also admit jointly changed evidence unrelated to the stage.

In the operative cells, name the stage-bound evidence (including expected digest and identity of the ancestor record), its apply comparison and revalidation point relative to writes, and the supported concurrency boundary. State what happens when evidence changes or becomes unreadable during that interval, including whether any earlier writes can have occurred and how retry preserves adopter content and the original bad cache. Define where recovery stores a new valid ancestor without replacing that preserved evidence. This need not promise protection against arbitrary concurrent project write access, which the accepted proposal excludes. Map deterministic changed-after-check and read/write-failure cases, with a matching control, to the public apply/recovery tests. These criteria specify accepted race handling and preservation; they remove no outcome.

The character policy correctly separates admission from display and retains decomposed accents and visible non-Latin names. Keep existing containment and path-shape restrictions when extending admission; do not substitute a smaller forbidden-character set for them. The named display routes and compatibility recovery still need the command/input/assertion mapping requested by ordinary PR1; this pass does not duplicate that finding.

**Coverage:** claims, completeness and fail-closed behavior: C1 and `_compute_upgrade`/`_apply_upgrade`; production paths and drift: `_write_stage`, install `print_report`, CLI merge/fidelity output and ordinary PR1; reuse and consistency: searches for `base_hash`, `_contained_lockfile_path`, `print_report` and `fidelity_warnings`; lifecycle: declared obligations and Maintainer-only AST ceremony; domain/scope: consistency rather than authentication, no scientific result; satisfier: explicit operative contract and mapped race/failure tests above. **Not covered / low confidence:** no implementation, mutation, runtime, command execution or platform rendering tests; no suite run. This is the Security plan pass, not implementation assurance.

## Response to plan review -- Codex GPT-6 -- 2026-10-30

| Finding | Disposition |
|---|---|
| PR1 | Accepted. The public paths mapping records each selected input, test home and operator-facing assertion; verification retains scoped runs. |
| SRP1 | Accepted. C1 defines stage snapshot, pre-write comparison, observable concurrency boundary, partial-write and retry handling, and distinct recovery evidence; the mapping records deterministic race and failure tests. C2 retains existing path restrictions. |

Both plan-review obligations are complete. Scope remains preserved; implementation remains subject to the Maintainer-run AST ceremony already applicable.
