# Protect upgrade bases and install output

**Author**: Codex GPT-6
**Status**: revising
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Check saved upgrade bases before merging and make supplied paths and names safe to recognize in output.

## Context

An upgrade uses a saved original template as the common ancestor for a three-way merge. A changed ancestor can cause the merge to discard an adopter edit or an upstream fix. The earlier Security Review demonstrated this risk (`dev/proposals/archive/2026-10-26-claude-engine-batch-f8-slots.md`, SR6). In the current tree `bootstrap/_scaffold/upgrade.py` reads the cache and passes it to `merge_file` without comparing `base_hash`. I inspected that path; I have not repeated the end-to-end loss demonstration.

The lockfile path guard in the same file uses `isprintable()`. Python reports U+034F COMBINING GRAPHEME JOINER printable even though it is invisible. `bootstrap/_scaffold/install.py` prints an unknown module name and install-report slot names directly; `bootstrap/_scaffold/cli.py` also prints slot names in merge and fidelity results. These are code observations, not end-to-end reproductions. The profile loader restricts control characters, but that does not establish that all remaining characters are visually unambiguous. The four findings and their authorization are recorded in `dev/PLANNING.md`.

## Proposal

1. Before any three-way merge at plan, stage or apply, compare the exact saved ancestor bytes with the recorded base digest. Missing, malformed or mismatched evidence must produce a by-hand review result, never an automatic merge or replacement. Preserve existing adopter files and the original cache; do not silently regenerate a base from the current file. Define legacy records and race handling in the plan, and test each command through its real entry point. A matching digest detects accidental or isolated cache alteration; it does not authenticate a lockfile and cache controlled together.
2. Reject invisible Unicode in lockfile paths at the shared admission boundary, including source, destination and cache paths, without rejecting ordinary visible non-ASCII names. Specify the character policy and compatibility consequences in the plan; escape offending values in diagnostics. Do not claim that a finite list catches all visual deception.
3. Escape profile- or template-supplied module and slot names in all install report and module merge/fidelity output paths, including warnings. Preserve ordinary ASCII readability and distinguish escaped characters from literal escape sequences. Cover each output path through the real command, including both normal and absent-module slot reports.

## Rationale

The digest makes the merge's stated ancestor checkable before it can influence a write; manual review preserves work when that evidence is absent. Path admission and terminal rendering address related human-recognition risks and overlap the security queue's terminal-escaping row. The saved-base integrity issue is distinct but shares the same engine and Security Review; the plan can keep its checks independent.

## Alternatives considered

Doing nothing leaves the documented loss and misleading-output risks in place. Escaping paths alone leaves invisible names admitted to filesystem operations; automatically replacing a bad cache with the adopter's file invents an ancestor and can lose edits. Restricting all paths to ASCII would reject legitimate visible names without establishing a need.

## Documentation / doctrine surface

Update `bootstrap/UPGRADE.md` to describe the manual-review outcome and the limits of the digest, and the relevant install/lockfile guidance for path and display behavior. These describe software behavior; they belong in the descriptive layer under `bootstrap/`, per `docs/DOCUMENTATION_PLAN.md`. No doctrine change is proposed.

## Evidence / verification plan

### Tests required

In `bootstrap/tests/`, exercise matching, missing, malformed and altered bases, including a crafted ancestor that would otherwise drop an edit; assert no automatic write on plan, stage and apply. Test paths containing invisible characters, ordinary visible Unicode and escaped diagnostics; test untrusted module and slot names in each output route. Include legacy records and a cache change between planning and application. Map all affected consumers and standing gates in the plan; run scoped checks and record Boundary B on the implementation commit. Certification is separate.

### Examples / smoke checks

Exercise install and upgrade in scratch projects; run `python scripts/check_cairn.py` and the applicable claim, link, snippet and neutrality gates for changed prose. The engine change also requires the Maintainer-run AST re-anchor under its existing ceremony; this proposal does not authorize installing a baseline or reconciling the old anchor.

#### Security preflight — five questions

* **S1:** The project supplies the lockfile, saved base and local files; the source supplies new templates; profiles and templates supply displayed names. The lockfile supplies the expected digest for the base it describes, so a party changing both can defeat this check.
* **S2:** Planned controls: mutate the base without updating its digest and inject invisible names; the corresponding behavior tests must fail if digest checking or escaping is removed. These mutations have not yet been run; no new check exists yet.
* **S3:** Upgrade plan, stage and apply select the affected lockfile records; install and merge commands select profile/template names. The plan must enumerate entry points and reconcile the exact adopter-facing wording with those tests before implementation; no new adopter-facing claim is asserted yet.
* **S4:** Missing or invalid digest and unreadable base lead to manual review, not automatic merge. Rejected path names cannot acquire filesystem authority; output encoding changes display only. The plan must resolve races and errors without granting more authority.
* **S5:** An actor can edit the project cache or supply names. An actor controlling both lockfile digest and cache can still forge a matching ancestor; visible confusables and misleading ordinary text also remain possible. This is a consistency check, not authentication or a complete defense against deception.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A valid existing install cannot upgrade without an explained recovery path; a mismatch still writes an automatic merge; or a visible legitimate path is rejected by an unspecified policy. Withdraw or revise the design if a safe digest check cannot coexist with the documented legacy and review workflow.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance


## Review -- Codex gpt-6.1-sol -- 2026-10-29

```
Reviewed commit: ea14ccbf9053e6bc46a017ce01ff39f12b0e2185
Target: opening proposal and cited code, queue and prior review
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised
**Verdict**: ACCEPT

**Foundations**

1. **Should this happen as framed?** Yes: protect the ancestor before trusting a clean merge and make supplied names recognizable. Doing nothing retains a real unchecked read, not merely a hypothetical new feature -- `bootstrap/_scaffold/upgrade.py`, `_compute_upgrade`.
2. **Best alternative.** Extend existing review-only classification and existing escaping practice; avoid a second recovery mechanism or an ASCII-only filesystem policy. This retains all three proposed outcomes -- `bootstrap/UPGRADE.md`, completion gate; `bootstrap/_scaffold/install.py`, local `esc` helper.
3. **What would show it wrong.** A cache mismatch can still advance an automatic result, or a previously supported visible name loses an explained upgrade route. Existing staged acknowledgement must remain a meaningful recovery path -- `bootstrap/_scaffold/upgrade.py`, `_apply_upgrade`; `bootstrap/UPGRADE.md`, migrating an existing project.

The strongest case is preservation of an adopter's accumulated methodology edits: a clean three-way merge is trustworthy only relative to its ancestor. The queue explicitly groups these four older findings; this proposal preserves them without claiming authentication or a universal defense against misleading text (`dev/PLANNING.md`, four older upgrade and install findings).

**R1 (non-blocking): make recovery a plan acceptance criterion.** Specify what happens after a damaged ancestor becomes review-only, including `--ack-review-only`, advancement of unaffected files, preservation of the bad cache and the next upgrade. Test that full sequence, rather than only refusal. The existing documentation tells migrated adopters to reconcile pairs and acknowledge them; an unconditional apply-time check could accidentally make that recovery impossible. A command-level recovery test and updated `bootstrap/UPGRADE.md` close this recommendation. This specifies the promised recovery; it removes no scope.

**R2 (non-blocking): choose compatibility examples before the character rule.** Include decomposed accented names and a visible non-Latin name, alongside isolated invisible characters. A rule rejecting all combining marks would reject ordinary visible names. State how a project whose existing lockfile contains a newly forbidden name can recover without hand-editing tool-owned provenance. Public-command tests plus the documented policy close this recommendation -- `bootstrap/_scaffold/upgrade.py`, `_contained_lockfile_path`; `bootstrap/UPGRADE.md`, two on-disk artifacts.

Implementation cost includes more than a digest call: apply consumes staged results, output has multiple producers, and the engine requires review and AST ceremony. These costs are proportionate to preventing silent loss; there is no scientific calculation change. Reuse the existing digest comparison pattern (`bootstrap/verify_integrity.py`, `_note_file`) while hashing raw bytes before decoding or conditional-region sizing.

**Coverage:** claims and failure behavior: `_compute_upgrade` and prior SR6; production routes and completeness: `_apply_upgrade`, R1/R2; consistency and drift: queue and `bootstrap/UPGRADE.md`; lifecycle: declared Security obligations and existing AST ceremony; scientific scope: methodology-file preservation, no numerical result; satisfiers: R1/R2. **Not covered / low confidence:** no end-to-end loss reproduction, implementation tests, measured runtime, Unicode policy implementation or Windows rendering; no suite run. This ordinary pass does not discharge Security Review.


## Review -- Codex GPT-6 Security reviewer -- 2026-10-29

```
Reviewed commit: 7137c0ad7ca21b612e00770c9bbef8de1c902810
Target: opening proposal, usual review, and committed engine paths
Prior findings: none
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: ACCEPT

**Foundations**

1. **Should this happen as framed?** Yes. An unchecked saved ancestor can steer a merge, and printable text is not necessarily recognizable. The proposal correctly limits its digest claim to consistency, rather than authentication -- `bootstrap/_scaffold/upgrade.py`, `_compute_upgrade` and `_contained_lockfile_path`.
2. **Best alternative.** Use the existing review-only path for invalid ancestors, one explicit character policy at path admission, and consistent escaping at display boundaries. Doing nothing preserves the unchecked merge input; ASCII-only paths sacrifice legitimate names without fixing ancestor integrity -- `bootstrap/_scaffold/upgrade.py`, `_apply_upgrade`; `bootstrap/_scaffold/install.py`, `print_report`.
3. **What would show it wrong.** A changed ancestor or expected digest can still authorize an automatic staged result, or a legitimate supported name becomes unrecoverable. Test the real stage/apply and acknowledgement sequence, including the interval between commands -- `bootstrap/_scaffold/upgrade.py`, `_compute_upgrade` and `_apply_upgrade`.

The strongest benefit is preventing silent loss when a saved ancestor is damaged or changed independently. Someone already controlling both the cache and lockfile can forge their agreement; someone controlling staged output can also edit what will be applied. This change should not be presented as containing arbitrary project write access. The separate display risk is misleading the operator; these observations do not establish code execution.

**SR1 (non-blocking): bind verification to the bytes consumed.** The plan should hash raw ancestor bytes before decoding, then merge that same read. Bind staged automatic results to the relevant expected digest and checked ancestor, and define what changes between stage and apply invalidate them. Current apply compares lock commit, tokens and roster, not the base digest; recomputing only a current cache/digest agreement would not prove that the staged result used it. Cover altered cache, altered digest, missing/malformed digest, unreadable/invalid-UTF-8 base, legacy records, and an unmodified control through public commands. Specify recovery without overwriting the original bad cache. This sharpens the proposal's existing race and preservation commitments -- `bootstrap/_scaffold/upgrade.py`, `_compute_upgrade`, `_stage_upgrade`, `_apply_upgrade`.

**SR2 (non-blocking): make recognition policy measurable.** Name rejected character classes and test U+034F, zero-width and bidi controls, terminal escape/control bytes, and literal backslash escape text. Include decomposed accents, non-Latin visible names and contextual joiner/variation-selector examples, with an explicit compatibility disposition where invisibility serves legitimate spelling or presentation. Do not equate all combining marks with invisible names. Exercise normal and absent-module slot reports, unpaired-marker warnings, unknown modules and merge/fidelity output; escape data without changing the names used for lookup. Reuse the existing `ascii`-based display practice where suitable -- `bootstrap/_scaffold/install.py`, `esc`, `install_file`, `install_modules`, `print_report`; `bootstrap/_scaffold/cli.py`, module-merge output; `bootstrap/_scaffold/slotmerge.py`, `_SLOT_RE`.

**Coverage:** claims, production routes, completeness and fail-closed behavior: cited merge/admission/apply paths; consistency and drift: proposal limits and `bootstrap/UPGRADE.md`; lifecycle: declared plan Security Review and AST ceremony; scientific scope: no scientific result; satisfiers: SR1/SR2 command tests and recovery/policy documentation. No implementation, attack reproduction, platform rendering measurement or suite run; enumeration cannot close all visual deception. This clears the proposal Security Review obligation, not implementation assurance.
