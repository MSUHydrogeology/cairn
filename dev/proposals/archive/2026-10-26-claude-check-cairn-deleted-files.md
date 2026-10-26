# check_cairn crashes when a tracked Markdown file is deleted but not yet committed

**Author**: Claude (Implementation)
**Status**: accepted
**Review**: usual
**Plan review**: not required(one commit: the same one-line filter in `link_check.py` and `sync_doc_snippets.py` and their shipped twins, `check_cairn.py` delegating to the fixed shared copy, one new test file; the frozen-file re-anchor is the already-queued Maintainer ceremony)
**Opened**: 2026-10-26
**In brief**: Make the three Markdown scans (`check_cairn`, `link_check`, `sync_doc_snippets`) skip tracked files that are deleted from disk but not yet committed, and say how many they skipped, so they report findings instead of crashing with a traceback.

## Context

**The check crashes whenever the working tree holds an uncommitted deletion of a tracked `.md` file.** Run on the live tree on 2026-10-26, under Python 3.13 (`/Users/kendal30/conda_envs/lhm/bin/python3.13`), at commit `a8970806`, with two such deletions present (`git status` shows `D dev/strategy/2026-10-19-codex-assai-runtime-architecture.md` and `D dev/strategy/2026-10-19-codex-cairn-and-assai.md`):

```
FileNotFoundError: [Errno 2] No such file or directory:
'/Users/kendal30/Code/cairn/dev/strategy/2026-10-19-codex-assai-runtime-architecture.md'
```

**Cause.** The default scan set comes from `tracked_markdown()` at `scripts/check_cairn.py:177-182`, which runs `git ls-files '*.md'`. That command lists what the git index tracks, and the index still lists a file whose deletion is not committed (`git ls-files -d` prints both paths). `main()` passes that list through `link_check.filter_sources` (`scripts/check_cairn.py:547`; the filter drops archives and vendored directories by path, never by existence) and into `check_tree()`. The first thing `check_tree()` does with each file is read it, at `scripts/check_cairn.py:491` (`md.read_text(...)`), which raises.

**Only that one read is reachable with a missing file.** The other reads of file text (`scripts/check_cairn.py:336` in the incident-tracker check and `:454` in the loop-fidelity check) come after line 491 has already succeeded for the same file. So one filter in front of the loop covers every site; there is nothing to fix at the others.

**Why it matters beyond annoyance.** The gate manifest lists `python scripts/check_cairn.py` as the `check-cairn` gate command, expecting "green" (`bootstrap/tests/fixtures/gate_manifest.json`, `gate_commands`, id `check-cairn`). A deletion in progress, which is an ordinary state during a rename, a move or a cleanup, turns a gate into a traceback with no finding to act on.

**What the check does once past the crash.** I ran it with the two deleted paths filtered out, from a throwaway wrapper outside the repo (it patched `tracked_markdown` to drop paths absent on disk and called `main([])`). It scanned 182 files and returned exit 1 with one finding: `dev/PLANNING.md:42: [path] cited path does not resolve: dev/strategy/2026-10-19-codex-cairn-and-assai.md`. That is correct behaviour: a live document cites a file that is being deleted. A fix must let that finding through, not hide it.

## Proposal

Proposed paths:
- `bootstrap/tests/test_check_cairn_deleted_files.py`

Change `tracked_markdown()` to return only tracked paths that exist on disk:

```python
return [root / line for line in out.stdout.splitlines()
        if line.strip() and (root / line).is_file()]
```

A deleted file has no content to check, so it is not scanned. Files named explicitly on the command line (`check_cairn.py some.md`) are unchanged: naming a path that does not exist is a user error and should still fail loudly.

Add one test that builds a temporary git repository, commits a Markdown file, deletes it from disk without committing, runs the default scan, and asserts it completes and does not scan the deleted file.

## Rationale

The filter is at the source of the list, the single place the missing paths enter, rather than a `try/except` around the read at line 491. A `try/except FileNotFoundError` would also swallow a file that vanishes mid-scan and would hide the cause. One line, and the behaviour reads from the code.

**Why this is a proposal and not a trivial-lane commit.** `scripts/check_cairn.py` is frozen: it has an entry in `frozen_files` in `bootstrap/tests/fixtures/gate_manifest.json` (oid `48679dd7...`). `AGENTS.md` says "a frozen-file edit owes the gate-manifest ceremony", and the manifest goes stale silently, so after the edit the committed manifest is out of date until the Maintainer-run re-anchor (`bootstrap/REANCHOR_RUNBOOK.md`). The code change is small; the ceremony it owes is what makes it more than a simple fix. I did not edit the file.

## Alternatives considered

* **Do nothing.** Costs a traceback in any working tree with an uncommitted deletion, and makes the `check-cairn` gate command unusable in that state. Workaround today: commit or restore the deletion first.
* **`try/except FileNotFoundError` around line 491.** Rejected, as above: broader than the defect, and it would hide a real mid-scan failure.
* **Use `git ls-files --cached --exclude-standard` with `--deleted` subtracted.** Same effect with a second git call and more code than an `is_file()` test.
* **Treat a deleted file as a finding.** Rejected: a deletion in progress is not a defect in the tree, and the useful signal (a live document citing the deleted file) already comes from the link and claim checks, as the run above showed.
* **Do the same fix in `link_check.py` / `claim_check.py`.** Not needed: neither is given the deleted paths by `check_cairn` beyond this list. I did not audit their own standalone default scans; the plan should state whether they share the defect.

## Documentation / doctrine surface

No doctrine, rule text or adopter-facing document changes. The one-line behaviour (deleted files are skipped) belongs in the module docstring's "Scanned set" paragraph at `scripts/check_cairn.py:50` ("the whole tracked Markdown tree"), which would gain "that exists on disk". Routing: descriptive layer, inside the file being edited.

## Evidence / verification plan

### Tests required

* **New test**, in a new file `bootstrap/tests/test_check_cairn_deleted_files.py` (a new file avoids editing the frozen `test_check_cairn_counts.py` and `test_check_cairn_content.py`, which are both in `frozen_files`). Name it for the property, for example `test_default_scan_skips_tracked_markdown_deleted_from_disk`. It must fail before the fix with `FileNotFoundError` and pass after.
* **Owning tests to re-run, scoped**: `bootstrap/tests/test_check_cairn_counts.py`, `test_check_cairn_content.py`, `test_loop_fidelity_gate.py`, `test_security_check.py::test_check_cairn_fails_closed_when_the_interpreter_cannot_be_spawned` (all import or run `scripts/check_cairn.py`; found with `grep -rl check_cairn bootstrap/tests`). Boundary B: this edits a frozen file, so the record is a bounded run only if the reviewer accepts that no contract surface is touched; the gate manifest is part of the install contract, so the Maintainer's call on `full` versus `bounded` applies. Certification comes from the next certifying run, not this change.
* **Live check**: `python scripts/check_cairn.py` on the tree above must complete and report the `PLANNING.md:42` finding, not crash.

### Examples / smoke checks

`python scripts/check_cairn.py` itself. After the re-anchor: `python bootstrap/tests/_gate_manifest.py verify`.

#### Security preflight

N/A: no trust boundary added, moved, or widened. The change narrows the list of files read; it adds no subprocess, parsing or path handling beyond an `is_file()` test on paths git already returned.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

* The new test passes before the fix (it did not reproduce the crash).
* The live run stops reporting `PLANNING.md:42` (the filter hid a real finding).
* A path that exists but is unreadable (permissions) starts being skipped silently; `is_file()` is true for it, so it should still raise. If it does not, the filter is too broad.

## Scope delta

**Scope delta**: preserved

No baseline outcome removed.

## Assurance path

**Assurance path**: high-assurance

Declared high-assurance because the change owes a gate-manifest re-anchor, and the gate manifest is part of the install contract (`AGENTS.md` > "High-risk surfaces"). The code itself touches no trust boundary; if the Maintainer reads the re-anchor as routine ceremony rather than a contract change, `standard` would fit.

## Review -- Claude (Reviewer, Sonnet) -- 2026-10-26

```
Reviewed commit: 4c5bc159
Target: the whole proposal, weighted to the stated cause, the claim that one filter covers every site, the gate-manifest cost, and what the proposal leaves out
Prior findings: none
Assurance path: high-assurance (as declared)
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Foundations**:

1. **Should this happen as framed?** Yes. The cause is the one stated, and the two-line filter in `tracked_markdown()` is the right size. I reproduced the crash and the fix in a detached worktree of `4c5bc159`: before the fix, `python scripts/check_cairn.py` ends in `FileNotFoundError` at `scripts/check_cairn.py:491`; after it, the run completes (M2, M3 below).
2. **Best alternative.** Doing nothing is allowed but weak: the workaround is to commit or restore the deletion first, and an in-flight deletion is the normal state when two agents share a tree. The strongest real alternative is to fix the shared helper once instead of one of its copies (RV1). The author's `try/except` alternative is correctly rejected.
3. **What would show it wrong.** A tracked path whose absence from the scan hides a finding. I tried that case and the finding survives (M5). What the proposal does not yet show is that the same defect sits in two sibling scripts (RV1, M4).

### Verdict in brief

**Revise, then decide.** The proposal should exist and its code change is correct. Three things need an answer before you decide:

* **The same defect lives in two other scripts, and one of them ships to adopters (RV1).** The proposal says it did not audit them. I did: both crash the same way.
* **The re-anchor it says this change owes is already owed (RV2).** That changes what the change costs you, and the order it should land in.
* **The test does not pin the property the proposal says matters most (RV3).** A fix that hid real findings would pass it.

### Steelman

The proposal keeps a gate script from turning an ordinary state, a deletion in progress, into a traceback. It finds the one place the missing paths enter. It refuses the broader `try/except`. It says out loud that the fix must let the real finding through, and it ran the check with the deletions filtered to show that it does. It declares its own cost (a frozen-file edit) and why that makes it a proposal. The strongest form: one filter at the source, no new name, one new test file.

### What I measured

Detached worktrees of `4c5bc159` in my scratch directory, Python 3.13 (`/Users/kendal30/conda_envs/lhm/bin/python3.13`), both removed afterwards. The main tree was not written. `CAIRN_FULL_SUITE` was not set.

| # | Measurement | Result |
|---|---|---|
| M1 | Claims against the tree | `scripts/check_cairn.py:177` is `tracked_markdown`, `:547` is the `filter_sources` call, `:491` is the first read, `:336` and `:454` are later reads (`check_tree` reaches `_check_incident_tracker_schema` and the internal-ref check only after `:491`), `:50` is the "Scanned set" line. `tracked_markdown` has one caller in `check_cairn` (`:548`). `git ls-files -d` printed both deleted paths. All as the proposal says |
| M2 | Crash, then fix, in the worktree with the two `dev/strategy/` files removed | Before: `FileNotFoundError` on the first deleted path. After the two-line change: exit 1, 183 files, two findings. The proposal's "182 files, one finding" was taken at `a8970806`; its own file is the 183rd, and the second finding is explained in M6 |
| M3 | The proposal's new test, written as described (temporary git repo, commit a file, delete it, run `main(["--root", ...])`) | Fails before the fix with `FileNotFoundError`, passes after. With the fix: the three `check_cairn` test files plus my 3 probe tests, 19 passed in 0.29 s. On the unfixed file the owning tests also pass (50 passed, adding `test_notice_install.py`, `test_gate_manifest.py` and the `test_security_check.py` node) |
| M4 | The other default scans, same deletion, same worktree | `scripts/link_check.py` and `scripts/sync_doc_snippets.py` both end in `FileNotFoundError`: each has its own copy of the same `tracked_markdown` (`scripts/link_check.py:491`, `scripts/sync_doc_snippets.py:249`). `scripts/claim_check.py` takes one file, so is not affected. `diff -q` reports both scripts byte-identical to `templates/modules/team-gated/link_check.py` and `.../sync_doc_snippets.py` |
| M5 | Does the filter hide a real finding? A temporary repo with `keep.md` linking to `gone.md`; `gone.md` committed, then deleted | Exit 1 and `keep.md:1: [link] broken link target: gone.md`. The finding survives |
| M6 | Clean checkout of `4c5bc159`, nothing deleted | `check_cairn` reports 1 issue across 185 files: `dev/reviews/2026-10-18-security-review-session-writes.md:131` cites a build-cache directory that is gitignored and exists only in a tree where Python has run. So the `check-cairn` gate is already red on a fresh checkout, with or without this change |
| M7 | `python bootstrap/tests/_gate_manifest.py verify` on the main tree (read-only) | Already reports a HOLD: `FROZEN-MODIFIED` and `FROZEN-OID` for `bootstrap/tests/test_quickstart_sequence.py`. In the worktree with the fix and a new test file, it adds `FROZEN-MODIFIED: scripts/check_cairn.py` and records the new test nodes as `COLLECTION-ADDED` (allowed) |

### Findings

**RV1 -- Medium -- blocking for the Decision: the Response states what happens to the two sibling copies.**
**The same defect is in `link_check.py` and `sync_doc_snippets.py`, and `link_check.py` is shipped to adopters.**

*Plain.* `tracked_markdown()` exists in three scripts as a copy. The proposal fixes one and says "I did not audit" the others. I ran them (M4): two crash on an uncommitted deletion exactly as `check_cairn` does. `link_check.py` is a shipped module with a byte-identical twin, so an adopter hits this in their own tree during any rename.

*Evidence.* M4. `AGENTS.md` says to generalize rather than copy, and `check_cairn` already imports `link_check` (it calls `link_check.filter_sources` at `scripts/check_cairn.py:547`).

*Recommendation.* Two ways to close it; the author decides.
* **Widen now.** Fix `tracked_markdown` in `link_check.py` and `sync_doc_snippets.py` (each with its template twin), and have `check_cairn` call `link_check.tracked_markdown` so there is one copy of that function to fix. All of these are frozen, so they ride the same re-anchor (RV2) at no extra ceremony. The cost is a shipped-template change and a second review round, because widening is new scope. I think this reaches the cause; the narrow change leaves two known crashes.
* **Keep it narrow and name the rest.** State in the Response that the siblings are unfixed and why, and queue a row for them. The easy-defect permission in `AGENTS.md` does not cover them: it reaches only files the work already edits.

Either way, "Not needed" in Alternatives and "the plan should state whether they share the defect" cannot stand: they do share it, and the Plan review line says no plan is written.

**RV2 -- Medium -- non-blocking: the proposal's cost statement is out of date. The re-anchor is already owed.**
**This edit adds one file to a ceremony the Maintainer already has queued.**

*Plain.* The proposal says the committed manifest "is out of date until the Maintainer-run re-anchor". It is already out of date for another file (M7), and `dev/PLANNING.md:100` queues the re-anchor, "one frozen test changed". So this change costs nothing extra if it lands before that ceremony. If the re-anchor runs first, it costs a second ceremony.

*Satisfier.* The Response names the ordering ("land before the queued re-anchor") and says who updates the `dev/PLANNING.md` row, whose "one frozen test changed" and "no engine symbol changed" wording would no longer be true. That edit belongs at a serialization point, not in this commit.

**RV3 -- Low -- non-blocking: the test should pin "the real finding survives".**
**The proposal's own bar is not in its test.**

*Plain.* Context says "a fix must let that finding through, not hide it". The test it proposes asserts only that the scan completes and skips the deleted file. A different fix that swallowed every flag would pass it. The "live check" meant to cover this cites `dev/PLANNING.md:42`, which stops being true when the other agent's deletion is committed or that line is edited, and which a later reader cannot reproduce.

*Satisfier.* Add one assertion to the new test, as in M5: a surviving file links to the deleted one, and the run exits 1 with that link flagged. It passed under the fix. Drop the live check as an acceptance criterion, or label it a one-off observation.

**RV4 -- Low -- non-blocking: three statements to correct or add.**

* **`test_security_check.py` does not run `check_cairn`.** The node named in Tests required (`bootstrap/tests/test_security_check.py:500`) patches `subprocess.run` and never runs or imports it, so "all import or run" is wrong for that node. The real consumer is `security_check.run_check_cairn` (`bootstrap/security_check.py:959`), which runs `check_cairn` on the live tree in the release security check; `docs/release-process.md:84` names it too. This strengthens the motivation (the release check would also stop on a deletion in progress). Cite it, instead of the gate manifest alone.
* **A tracked Markdown symlink whose target is gone** also crashes today (I tried it) and would be silently skipped after the fix, because `is_file()` is false for it. That may be right, but the Signals section lists only the unreadable-file case. Say which way it should go.
* **The skip is silent.** After the fix a scan of "182 files" says nothing about the files left out. A one-line note on stderr ("skipped N tracked file(s) deleted from disk") would keep the count honest. Optional; if taken, the test asserts it.

**RV5 -- Low -- non-blocking: the declared assurance path and the Boundary B wording.**
Nothing in this change edits the gate manifest or its schema; only a pinned hash changes, through the same ceremony every frozen edit owes. `standard` fits at least as well as `high-assurance`; if you keep `high-assurance`, say what it adds here. On Boundary B, `AGENTS.md` makes `full` the rule when a contract surface is touched, and the full run is the next certifying run, so "the Maintainer's call on full versus bounded" is not a call. The record is scoped with `Certified by: pending`.

**Observation, no satisfier here.** M6: the `check-cairn` gate is red on a clean checkout because of one review citing a build-cache directory. It is separate from this proposal. The proposal is right that a deletion turns the gate into a traceback; it is not the only reason the gate is not green on a fresh clone. Worth a row, not a change here.

### What I tried to break

* **Fix hides a finding.** M5: it does not.
* **Fix swallows a real failure.** An explicitly named missing path (`check_cairn.py gone.md`) still raises `FileNotFoundError` with the fix applied, as the proposal says.
* **Other read sites.** Listed from the tree (`read_text` in `scripts/check_cairn.py`: `:336`, `:454`, `:491`); the loop order puts `:491` first.
* **Unreadable file.** Not run. `is_file()` follows `stat`, which succeeds on an unreadable file, so it should still raise. Unverified.

Coverage -- **Covered**: lens 1 (claims: M1, M2, M7), lens 2 (production path: M3 calls `main()`, not a helper), lens 3 (edge cases: deleted file, dangling symlink, explicit path, citing doc, M5), lens 4 (silent skip: RV4), lens 5 (sibling copies and consumers: M4, RV1, RV4), lens 6 (drift: file and finding counts, M2/M6; the PLANNING row, RV2), lens 7 (re-anchor placement: RV2), lens 9 (each finding names a satisfier). Lens 8 does not apply. **Not covered / low confidence**: I did not run the full suite or a certifying run (not mine to run); I did not run `bootstrap/reanchor.sh` or look past the runbook's opening and `_gate_manifest.py verify`; I did not test an unreadable file or a Windows path; I did not check whether widening to the shipped templates (RV1) disturbs the adopter upgrade path or any pin outside `_gate_manifest.py`.

## Response -- Claude (author) -- 2026-10-26

**Conclusion first.** I accept RV1 and widen the proposal to all three scripts and the two shipped twins. I accept RV2, RV3 and RV4 in full, and RV5 in part. Because scope widened, the status returns to `awaiting-review`: under the one-round rule the second review reads **only the added material** (the two sibling scripts, their shipped twins, the delegation, the stderr note, the PLANNING ordering). The `check_cairn.py` change reviewed in round one is unchanged.

**I checked RV1 myself before widening.** All on `a8970806` plus the live tree, Python 3.13 (`/Users/kendal30/conda_envs/lhm/bin/python3.13`), nothing written to the repo:

* `scripts/link_check.py:489-494` and `scripts/sync_doc_snippets.py:247-252` each carry the same four-line `tracked_markdown()` as `scripts/check_cairn.py:177-182`.
* Run on the live tree, `python scripts/link_check.py` and `python scripts/sync_doc_snippets.py` each end in `FileNotFoundError` on the first of the two uncommitted deletions under `dev/strategy/`.
* `cmp` reports `scripts/link_check.py` and `scripts/sync_doc_snippets.py` byte-identical to `templates/modules/team-gated/link_check.py` and `.../sync_doc_snippets.py`. `test_every_self_hosted_twin_stays_byte_identical_to_its_source` (`bootstrap/tests/test_notice_install.py:114`) fails if only one side of a pair is edited, so the twins must change together and the repository already enforces it.
* All five files are in `frozen_files` in `bootstrap/tests/fixtures/gate_manifest.json`.
* **Something the review did not say, and it changes the design:** `check_cairn.py` does not load `scripts/link_check.py`. It loads the shipped **template** copy (`_LINK_CHECK_SRC`, `scripts/check_cairn.py:98-101`, bound to `link_check` at `:136`). So once the template is fixed, `check_cairn` can call `link_check.tracked_markdown` and need not carry its own copy.

**RV1 -- accepted, as "widen now."** Fix `tracked_markdown()` in `link_check.py` and `sync_doc_snippets.py` (each with its twin), and have `check_cairn.py` call the shared one and drop its own copy. The review's cost note holds: a second review of the added material, and a shipped-template change. I did not choose "keep it narrow": the siblings crash today, and one of them ships.

**RV2 -- accepted.** The change lands **before** the queued re-anchor so one ceremony pins everything. `dev/PLANNING.md` (the row "Re-anchor the gate manifest -- one frozen test changed", around line 100) will then be wrong in two ways: more than one frozen file changed, and the changed set is five files plus one new test file. I do not edit that row in the proposal commit or the implementation commit (shared files change only at serialization points). I ask the Maintainer to have the goodnight scrub rewrite it once the implementation commit exists, and the re-anchor derives its changed set from the final committed tree, as the runbook says.

**RV3 -- accepted.** The test now asserts that a surviving document linking to the deleted file still exits 1 with that link flagged. The live `PLANNING.md:42` check is demoted from an acceptance criterion to a one-off observation: it is not reproducible once the other agent's deletion is committed.

**RV4 -- accepted, three parts.**
* The `test_security_check.py` node does not run `check_cairn`. I withdraw it from the owning-test list. The real consumer is `security_check.run_check_cairn` (`bootstrap/security_check.py:959-972`), which runs `scripts/check_cairn.py` on the live tree in the release security check, and `docs/release-process.md:84` names the same command. That strengthens the motivation and is now cited.
* **Dangling symlink: skip it, and say so.** A tracked `.md` symlink whose target is gone is, like a deleted file, a path with nothing to read. It is skipped and counted in the note below. Raising would put the traceback back for a state the scan cannot do anything with.
* **The skip is no longer silent.** When one or more paths are skipped, `tracked_markdown()` writes one line to stderr: `skipped N tracked Markdown file(s) not present on disk`. It writes nothing when N is 0. The tests assert both.

**RV5 -- accepted in part.** `standard`: no schema or manifest field changes, only pinned hashes, through the ceremony every frozen edit owes. I drop the claim that the re-anchor is a contract change. On Boundary B I accept the correction: the record is scoped, with `Certified by: pending`, and the certifying run covers the full suite. I do not pre-declare `bounded`; at implementation the mapping decides, and the shipped templates and frozen files mean uncertainty resolves to `full`.

**Observation (M6, the gate is red on a clean checkout).** Agreed, and kept out of this proposal. I am not queuing the row myself; the Maintainer or the goodnight scrub can.

## Revision -- Claude (author) -- 2026-10-26

This is the complete current contract. It replaces the Proposal, Evidence and Assurance sections above; earlier sections stay as history.

### What changes

One defect, three copies. `git ls-files '*.md'` lists a file whose deletion is not yet committed, and each scan then reads it and raises. Fix it once in the shared checker and in the one sibling that does not share it:

| File | Change |
| --- | --- |
| `templates/modules/team-gated/link_check.py` and `scripts/link_check.py` (byte-identical pair) | `tracked_markdown()` keeps only paths where `is_file()` is true. If any were dropped, print one stderr line giving the count. |
| `templates/modules/team-gated/sync_doc_snippets.py` and `scripts/sync_doc_snippets.py` (byte-identical pair) | The same change to its own copy. It does not load `link_check`, so it keeps its own function. |
| `scripts/check_cairn.py` (Cairn-only, no twin) | Delete its own `tracked_markdown()` (`:177-182`) and call `link_check.tracked_markdown(root)` at `:548`. Update the "Scanned set" line at `:50` to say tracked files **that exist on disk**. |

Files named explicitly on a command line are unchanged: a named path that does not exist still raises. The one function's behaviour is: tracked, regular-file-or-symlink-to-a-file paths pass; deleted paths and dangling symlinks are dropped and counted.

No new public name is added; one function is removed from `check_cairn.py` (nothing in `bootstrap/tests` references `tracked_markdown`; searched with `grep -rn tracked_markdown bootstrap/tests`, no match).

Proposed paths:
- `bootstrap/tests/test_deleted_tracked_markdown.py`

### Tests required

One new file, `bootstrap/tests/test_deleted_tracked_markdown.py` (a new file, because the existing `check_cairn` test files are frozen). Each test builds a temporary git repository, commits Markdown, deletes or breaks a file on disk without committing, and calls the script's real `main(["--root", <tmp>])`. Parametrized over the three scripts (`link_check`, `sync_doc_snippets`, `check_cairn`), three properties, so nine small nodes at most:

1. **A deleted tracked file does not crash the default scan.** Fails before the fix with `FileNotFoundError`, passes after.
2. **A surviving document that links to the deleted file is still flagged** (exit 1, `[link]` finding naming the deleted target). This pins that the filter hides the missing file, not the finding. For `sync_doc_snippets`, which has no link finding, the assertion is that it completes and does not touch the deleted path; the finding assertion applies to `link_check` and `check_cairn`.
3. **The skip is reported, a dangling symlink counts, and a clean tree prints nothing.** One commit deletes a file and adds a dangling `.md` symlink: stderr contains `skipped 2 tracked Markdown file(s) not present on disk`; a clean repo prints no such line; an explicitly named missing path still raises.

Twin parity needs no new test: `test_every_self_hosted_twin_stays_byte_identical_to_its_source` fails if either side of a pair is edited alone.

**Owning tests to re-run, scoped** (found by what imports or runs the touched files): `bootstrap/tests/test_doc_drift_tools.py`, `test_link_check_exclusions.py`, `test_loop_fidelity_gate.py`, `test_check_cairn_counts.py`, `test_check_cairn_content.py`, `test_content_scan.py`, `test_notice_install.py`, `test_practice_modules.py` (references `sync_doc_snippets`), `test_gate_manifest.py`, and the new file. The Boundary B mode is decided at implementation by the `AGENTS.md` rule (uncertainty resolves to `full`); the change's record is scoped with `**Certified by**: pending`, and the next certifying run covers the full suite.

**Smoke:** `python scripts/check_cairn.py`, `python scripts/link_check.py` and `python scripts/sync_doc_snippets.py --check` each complete on a tree with an uncommitted deletion (a one-off observation, not an acceptance criterion). Before the re-anchor: `python bootstrap/tests/_gate_manifest.py verify` is expected to report `FROZEN-MODIFIED` for the five edited files and `COLLECTION-ADDED` for the new nodes.

### Re-anchor ordering

This change lands **before** the queued gate-manifest re-anchor (`dev/PLANNING.md`, "Re-anchor the gate manifest"), so one Maintainer-run ceremony pins the already-owed `test_quickstart_sequence.py` change and these five files together. If the re-anchor runs first, this change costs a second one. The PLANNING row's wording ("one frozen test changed", "no engine symbol changed") needs rewriting at the next serialization point; the implementer does not edit it. A CHANGELOG entry for the shipped `link_check` and `sync_doc_snippets` change is likewise written at a serialization point.

### Documentation / doctrine surface

No doctrine or rule text. The `check_cairn.py` "Scanned set" docstring line changes as above. The shipped-script change reaches adopters through the normal template upgrade path; I did not test that path, and the second reviewer is asked to look at it (see below).

### Signals the change is wrong

* Property 1 passes before the fix (the test did not reproduce the crash).
* Property 2 fails to flag the link, or the run stops reporting a finding it reported before (the filter hid something).
* A readable file is skipped, or an unreadable-but-present file stops raising (`is_file()` is true for it, so it should still raise; unverified, as in round one).
* Any twin pair differs after the edit (the parity test names it).
* An adopter's `link_check` run changes output on a clean tree (the note must print nothing when N is 0).

### Scope delta

**Scope delta**: preserved

The baseline outcome (`check_cairn` completes with an uncommitted deletion) is delivered. The widening adds outcomes; nothing opened with is dropped.

### Assurance path

**Assurance path**: standard

Per RV5. The change adds no subprocess, parsing or path handling beyond an `is_file()` test on paths git already returned, and adds one stderr line. What it does touch that the first version did not: two shipped templates, which is why the second review is requested.

### Questions for the second review

Only the added material: (a) does `check_cairn` delegating to `link_check.tracked_markdown` leave any caller or doc that still expects its own function; (b) does editing the two shipped templates disturb the adopter upgrade or any pin outside the gate manifest (round one did not cover this); (c) is the stderr note safe for any caller that parses stderr or stdout of these scripts.

### Withdrawn / superseded commitments

* "Fix `check_cairn.py` only; the sibling scripts are 'not needed'" -- withdrawn: both crash the same way (RV1).
* "`test_security_check.py::test_check_cairn_fails_closed_when_the_interpreter_cannot_be_spawned` is an owning test" -- withdrawn: it never runs `check_cairn` (RV4).
* "The live `dev/PLANNING.md:42` finding is part of the acceptance check" -- superseded by the property-2 test (RV3).
* The test file name `bootstrap/tests/test_check_cairn_deleted_files.py` in the first Proposal -- superseded by `bootstrap/tests/test_deleted_tracked_markdown.py`, which covers all three scripts.
* "A skipped file is silent" -- superseded by the stderr count (RV4).
* "Assurance path `high-assurance`; Boundary B `full` vs `bounded` is the Maintainer's call" -- superseded: `standard`; the mode follows the `AGENTS.md` rule (RV5).
* "The re-anchor is a new cost of this change" -- superseded: it rides the already-queued one, if this lands first (RV2).

## Review (second round, widened scope) -- Claude (Reviewer, Sonnet) -- 2026-10-26

```
Reviewed commit: 41b7f9e1
Target: only the added material -- the Response, the Revision, and the changed Status, Plan review and In brief lines
Prior findings: RV1 to RV5 (my first review, at c685c496)
Assurance path: standard (as now declared)
```

**Tier**: usual
**Findings**: raised (all Low, none blocking)
**Verdict**: PROCEED to Decision

**Foundations**:

1. **Should this happen as framed?** Yes. The widened change is one defect fixed in all three copies, and `check_cairn` can delegate as claimed: it loads the shipped `link_check.py` template (`scripts/check_cairn.py:98` and `:136`), so a fix there reaches it. I built the whole change in a detached worktree of `41b7f9e1` and it behaves as the Revision says (M1 to M4 below).
2. **Best alternative.** The Response took the alternative I judged strongest. A simpler path I looked for does not exist: `sync_doc_snippets.py` does not load `link_check`, so it needs its own edit, as the Revision says.
3. **What would show it wrong.** A caller that parses the new stderr line, a one-sided twin edit, or an adopter whose upgrade breaks. I tried each: no consumer parses it (M5), a one-sided edit fails the parity test (M3), and an adopter upgrade applies cleanly (M4).

### What I measured

Detached worktrees of `41b7f9e1` in my scratch directory, Python 3.13 (`/Users/kendal30/conda_envs/lhm/bin/python3.13`), removed afterwards. The main tree was not written. `CAIRN_FULL_SUITE` was not set.

| # | Measurement | Result |
|---|---|---|
| M1 | The Revision's change built by hand: `is_file()` filter plus a stderr count in `tracked_markdown()` of the four frozen-pair files; `check_cairn` loses its copy and calls `link_check.tracked_markdown(root)` | Applies cleanly. `tracked_markdown` now has no other definition or caller in the tree (`grep` over `*.py`, `*.md`, `*.json`, `*.yml`); `check_cairn` was its only outside user, at `scripts/check_cairn.py:548` |
| M2 | The Revision's three properties, written as described, across the three scripts' real `main(["--root", ...])` (repo with one deleted file, one dangling `.md` symlink, one document linking to the deleted file) | 6 passed. Deleted-file scan completes; `link_check` and `check_cairn` exit 1 and flag `gone.md`; stderr reads `skipped 2 tracked Markdown file(s) not present on disk`; a clean repo prints no `skipped` on either stream. An explicitly named missing path still raises `FileNotFoundError` in `link_check` and `sync_doc_snippets` (and did in `check_cairn` in round one) |
| M3 | Scoped tests on the committed change: `test_doc_drift_tools`, `test_link_check_exclusions`, `test_loop_fidelity_gate`, `test_check_cairn_counts`, `test_check_cairn_content`, `test_content_scan`, `test_notice_install`, `test_practice_modules`, `test_gate_manifest` | 299 passed, 5 failed with the edit uncommitted (all in `test_gate_manifest.py`, all `FROZEN-MODIFIED` on the working tree, the documented effect of an uncommitted frozen edit). After committing the change in the worktree: `test_gate_manifest.py` and `test_notice_install.py` 33 passed. Editing only `scripts/link_check.py` makes `test_every_self_hosted_twin_stays_byte_identical_to_its_source` fail, so the parity test does bind the pairs. `quality_gate.py --sub redundancy`: no findings |
| M4 | An adopter: `collaborative-team` installed from the base tree into a scratch repo, then `upgrade --plan`, `--stage`, `--apply` with the changed tree | The plan reports `verbatim-update 2: scripts/link_check.py, scripts/sync_doc_snippets.py`. After apply both are byte-identical to the new templates. With a tracked `.md` deleted, the adopter's `link_check.py` and `sync_doc_snippets.py` both complete and print the skip line |
| M5 | Who parses the new line | None found. Inside the tree, `check_cairn` calls `link_check` in-process, and `bootstrap/security_check.py:959` runs `check_cairn` and reads only its return code. The shipped templates and docs contain no subprocess consumer of either script's output (`grep` for `subprocess`, `stderr`, `hook` over `templates`, `docs`, `scripts`). The line prints only when N is above 0, and no exit code changes. Not testable from here: an adopter's own wrapper or hook |
| M6 | The gate-manifest effect of the change as built | `_gate_manifest.py verify` reports `FROZEN-MODIFIED` and `FROZEN-OID` for exactly the five edited files. The already-owed `test_quickstart_sequence.py` entry is a sixth, as the Revision's ordering implies |
| M7 | Pins outside the gate manifest | The self-hosted `dev/.cairn/cairn-lock.yml` records a hash for `scripts/link_check.py` and `scripts/sync_doc_snippets.py` that equals today's bytes. `verify_integrity --target .` reports a hash mismatch for them after the edit, but it already reports 21 other files in the main tree; no test I ran reads that result |

### Whether each first-round finding is closed

* **RV1 -- closed.** All three scripts fixed, twins edited together, `check_cairn` delegating (M1, M2, M3).
* **RV2 -- closed.** The Revision's ordering matches M6: land before the queued re-anchor, and the PLANNING row is left for a serialization point.
* **RV3 -- closed.** Property 2 is in the plan, and it passes in M2. Its `sync_doc_snippets` carve-out is right: that tool has no link finding.
* **RV4 -- closed.** The `test_security_check.py` node is withdrawn and the real consumer is cited. A dangling symlink is skipped and counted (M2 shows `skipped 2`). The skip is no longer silent.
* **RV5 -- closed.** `standard` and the Boundary B wording are corrected.

The Revision's questions: (a) no caller or doc still expects the removed function (M1). (b) The upgrade path is undisturbed (M4); the one pin outside the gate manifest is the self-hosted lockfile (M7, SR3). (c) Nothing I could find parses the line (M5).

### Findings

**SR1 -- Low -- non-blocking: the shipped docs still say "whole tracked tree".**
`templates/modules/team-gated/link_check.py:49` and `docs/tool-usage.md:87` describe the default scan without the new rule, and the Revision edits only the "Scanned set" line in `check_cairn.py`. Satisfier: add "that exists on disk" to the `link_check.py` docstring while that file is already open (the byte-identical twin follows by the parity test), and one clause to `docs/tool-usage.md`. Both are prose in files the work already edits, or a descriptive doc with no test pinning it.

**SR2 -- Low -- non-blocking: the skip line carries no tool name.**
Other lines from these tools start `link_check:` or `check_cairn:`. This one does not, and because `check_cairn` calls the shared function, a prefix inside it would name the wrong tool. Leaving it bare is acceptable; the Response should say that is deliberate, or take the tool name as an argument. The tests assert the text, so whichever is chosen, the test must match.

**SR3 -- Low -- non-blocking: name the lockfile in the Documentation section.**
M7. The change makes two more files differ from `dev/.cairn/cairn-lock.yml`. That is not new in kind (21 files already differ) and nothing fails, but the Revision answers question (b) only for the upgrade path. State that the self-hosted lock is not refreshed by this change, and that its refresh belongs to whoever next regenerates it.

**Implementation reminder, not a finding.** The first Boundary B run for this change must be on a committed tree (M3: five `test_gate_manifest.py` failures appear only while the edit is uncommitted).

Coverage -- **Covered**: lens 1 (claims: the delegation, `_LINK_CHECK_SRC`, the twin and frozen statements, M1/M6), lens 2 (production path: M2 calls `main()` of each script), lens 3 (edge cases: deleted file, dangling symlink, clean tree, named missing path, M2), lens 4 (silent failure: the count line, M2), lens 5 (callers, docs and consumers: M1, M5, SR1), lens 6 (drift: SR1), lens 7 (ordering against the queued re-anchor: M6), lens 9 (each finding names a satisfier). **Not covered / low confidence**: I did not run the full suite or the certifying pair; I did not read the reanchor ceremony beyond `_gate_manifest.py verify`; I tested one profile (`collaborative-team`) for the adopter upgrade, not an adopter who had edited `link_check.py` locally (the merge path); I could not see any adopter-side wrapper that parses these tools' output; I did not test an unreadable file or Windows paths.

## Decision -- Anthony Kendall (Maintainer) -- 2026-10-26

**ACCEPTED, with the second-round findings folded in.** The Maintainer's
authorization, quoted **verbatim and visually isolated**:

> "Accept it, with SR1–SR3 folded into implementation"

*Scribe's note, separate from the quoted words.* The Revision of 2026-10-26 is
the contract. The implementation also closes the three Low findings of the
second-round review, each by the satisfier that review names: SR1, the
"whole tracked tree" wording in the shipped `link_check.py` docstring and in
`docs/tool-usage.md`; SR2, the skip line's missing tool name, either stated as
deliberate or passed in, with the test matching; SR3, a sentence saying the
self-hosted `dev/.cairn/cairn-lock.yml` is not refreshed by this change.

## Code review -- Claude Sonnet 5.5 (fresh session) -- 2026-10-26

```
Reviewed commit: 9ec53a43 (parent f58c5ed0, the Decision)
Target: the implementation against the Revision of 2026-10-26 and the Decision's SR1 to SR3
Prior findings: SR1 to SR3 (second-round review), folded in by the Decision
Interpreter: /Users/kendal30/conda_envs/lhm/bin/python3.13 (Python 3.13.13)
```

**Tier**: usual (code review by a fresh reviewer who did not write the work; no External call)
**Findings**: raised (one Medium, two Low)
**Verdict**: REVISE -- the change does what it claims for a deleted file and a dangling symlink, but it turns one loud failure into a quiet wrong answer (CR1). Fix CR1, then proceed to archive.
**Bounding**: FULL RUN REQUIRED

**Foundations**:

1. **Does it really do what it claims?** For the case it was built for, yes: with a tracked file deleted from disk, all three scans complete, a document linking to the deleted file is still flagged, and the skip count is printed (M1, M2; ledger rows A1 to A4). It does not hold for a file whose name git quotes (any non-ASCII name): that file is present on disk, yet it is dropped from the scan and reported as "not present on disk" (CR1; ledger row B4).
2. **Best alternative.** The build is the simple one and I would not replace it. One small change makes it safer: ask git for NUL-separated names (`ls-files -z`), which Cairn's own `scripts/content_scan_runner.py:262` already does, so the names arrive unquoted (M7 shows this reaches the cause).
3. **What would show it wrong.** The Revision's own signal, "a readable file is skipped". I tried to produce it and did, in the falsification ledger below (B4). The same ledger records the cases that held.

### Falsification ledger

Everything ran in detached worktrees of `9ec53a43` (and of its parent for the "before" side), in my scratch directory, under Python 3.13.13. The main tree was not written. `CAIRN_FULL_SUITE` was not set. Each case ran the script's real command line (`python scripts/<name>.py --root <repo>`) in a throwaway git repository.

**Control runs.**

| # | Control | Result |
|---|---|---|
| C1 | New test file, unmutated, at `9ec53a43` | 10 passed in 1.6 s |
| C2 | The same test file copied into a worktree of the parent `f58c5ed0`, run against the unfixed scripts | 8 failed, 2 passed. The two that pass are the "explicitly named missing file still raises" nodes. The commit body's "8 of 10 failed before" is reproduced |
| C3 | The implementer's reported bounded set (new file, `test_doc_drift_tools`, `test_link_check_exclusions`, `test_loop_fidelity_gate`, `test_check_cairn_counts`, `test_check_cairn_content`, `test_content_scan`, `test_notice_install`, `test_practice_modules`, `test_gate_manifest`, `test_security_check`) at `9ec53a43` | 425 passed in 52 s. The reported figure (425 in 51 s) reproduces |
| C4 | Fourteen further test files that install modules, upgrade, or read the shipped scripts and were not in the reported set (`test_scaffold`, `test_upgrade`, `test_upgrade_module_additions`, `test_profiles_smoke`, `test_lockfile_provenance`, `test_reference_scripts`, `test_doc_governance`, `test_presets`, `test_security_net`, `test_security_stack`, `test_security_lint`, `test_security_verification`, `test_generated_output_scan`, `test_claim_check_module`) | 729 passed, 0 failed, 1 min 46 s. This is a targeted check of the bound, not the full suite |

**A. Cases that held** (before = parent commit, after = `9ec53a43`; each across `link_check`, `sync_doc_snippets`, `check_cairn`):

| # | Case | Before | After | New or old |
|---|---|---|---|---|
| A1 | Tracked file deleted from disk | `FileNotFoundError` in all three | completes, "skipped 1" line | the defect, fixed |
| A2 | `--root` is a subdirectory of the repo, one deleted file inside it and one outside | `FileNotFoundError` | completes, "skipped 1" (only the file under the root is counted) | fixed |
| A3 | Tracked `.md` is now a directory | `IsADirectoryError` | completes, "skipped 1" | fixed |
| A4 | Unreadable but present file (mode 000) | `PermissionError` | `PermissionError` | unchanged, as the Revision's signals require |
| A5 | Tracked symlink to a file outside the repo | `link_check` and `check_cairn` scan it and exit 0; `sync_doc_snippets` refuses ("outside the repo root") | identical | unchanged, not this change's |
| A6 | A name with a space | scanned | scanned | unchanged |

**B. Cases that failed or were left open.**

| # | Case | Before | After | Verdict |
|---|---|---|---|---|
| B4 | A tracked `café doc.md` (non-ASCII name) that exists on disk and contains a broken link | `FileNotFoundError` (git prints the name as `"caf\303\251 doc.md"` with quotes, and the code treats those quotes as part of the path) | exit 0, "OK -- 1 Markdown file(s) scanned; no issues", and the stderr line "skipped 1 tracked Markdown file(s) not present on disk". The file was never read; its broken link is not reported | **CR1**. The old crash was a bug of its own; the filter turns it into a false pass |
| B5 | The same repository with `ls-files -z` and NUL splitting applied by hand to all four copies, in a separate copy | not applicable | 3 files scanned, broken link flagged (exit 1) in `link_check` and `check_cairn`; the 58 tests in the new file, `test_link_check_exclusions`, `test_doc_drift_tools` and the twin-parity node all pass | the satisfier for CR1 works |
| B6 | Cairn's own tracked tree | `git ls-files '*.md'` lists no quoted name (`git ls-files '*.md' | grep -c '^"'` prints 0) | not applicable | Cairn is not hit; an adopter with non-ASCII file names (accented or non-Latin names) is |

**C. Mutation ledger (every member of the set).** The set, listed from the tree with `git grep` over `scripts`, `templates`, `bootstrap` and `tools`: `tracked_markdown()` in `scripts/link_check.py`, its twin `templates/modules/team-gated/link_check.py` (the copy `check_cairn` loads, `scripts/check_cairn.py:98` and `:136`), `scripts/sync_doc_snippets.py` and its twin, and `check_cairn`'s call site (`scripts/check_cairn.py:542`). The other `git ls-files` users are not default Markdown scans: `scripts/content_scan_runner.py` (and its twin) already uses `-z` and skips an absent file (`is_file()` then `continue`, `:358`; read, not run), `scripts/correct_pinned_digests.py:96` tests one named path, and `tools/session.py:806` reads the index with `--stage`. Each mutant was made in a separate copy and reset afterwards. "Behaviour" is the new test file; "parity" is `test_every_self_hosted_twin_stays_byte_identical_to_its_source`.

| Mutant | Behaviour tests | Parity test | Result |
|---|---|---|---|
| Control (no mutation) | 10 pass | pass | baseline |
| M1 filter removed, `scripts/link_check.py` | 3 fail (link_check) | fails | killed |
| M2 filter removed, `link_check.py` template | 3 fail (check_cairn) | fails | killed |
| M3 filter removed, `scripts/sync_doc_snippets.py` | 2 fail (sync_doc_snippets) | fails | killed |
| M4 filter removed, `sync_doc_snippets.py` template | none | fails | killed by parity only. No behaviour test runs this copy |
| M5 `check_cairn` back to its own unfiltered copy | 3 fail (check_cairn) | pass | killed |
| M6 to M9 skip line removed, one copy each | 1 fails (M6, M7, M8); none (M9) | fail | killed; M9 by parity only |
| M10, M11 `is_file()` to `exists()`, one copy only | none | fails | killed by parity only |
| M10b `is_file()` to `exists()` in all four copies together | none | pass | **survived**; not equivalent: a tracked path that is now a directory goes back to `IsADirectoryError` in all three scripts (measured). See CR2 |
| M12, M13 skip line printed on every run | 1 fails each | fail | killed |

Tally: 14 mutants made (M1 to M13 and M10b); 13 killed (4 of those, M4, M9, M10 and M11, only by the parity test and by no behaviour test), 1 survived (M10b), 0 equivalent. The control is clean after each reset (11 passed).

### Bounding verdict

**FULL RUN REQUIRED.** The implementer reports a `bounded` run (425 passed in 51 s, Python 3.13, `**Certified by**: pending`), and I reproduced the number (C3). I rule it cannot stand as `bounded`, for three reasons:

1. **It touches contract surfaces.** The gate manifest pins the bytes of five edited files (`frozen_files` in `bootstrap/tests/fixtures/gate_manifest.json` lists `scripts/check_cairn.py`, both `link_check.py` copies and both `sync_doc_snippets.py` copies; `_gate_manifest.py verify` at this commit reports `FROZEN-MODIFIED` and `FROZEN-OID` for each). Both templates are installed `verbatim=True` into adopters (`bootstrap/_scaffold/config.py:924-927`), so their bytes are what adopters receive and what the upgrade path hashes (`bootstrap/UPGRADE.md:229`). AGENTS.md says bounded mode refuses for "the install contract" and "the fidelity or gate manifest", and that uncertainty resolves to full. The Revision itself said the same ("the shipped templates and frozen files mean uncertainty resolves to full").
2. **No valid record exists in the commit body.** AGENTS.md puts a no-plan change's Boundary B record in its commit body, before the commit. This commit's body says Boundary B "follow[s] separately". The 425 figure arrived later, in a report. That is a missing record, one of the triggers for a fresh full run.
3. **CR1 changes the bytes again.** Fixing it edits the same four shipped files, which invalidates any record taken at `9ec53a43`.

The challenge I made to the bound found no failure outside it: 729 tests the report left out passed (C4). That is evidence the bound was reasonable, not a reason to accept it. What "full" requires here is a scoped record with `**Certified by**: pending` and the next certifying run; I did not run the suite and will not. The record for the CR1 fix commit should carry the mode (`full`), interpreter, the tests above, and counts in its commit body.

### Findings

**CR1 -- Medium -- fix before archive: a present file with a non-ASCII name is skipped and reported as absent.**

*Plain.* Git prints a file name containing a non-ASCII character in quotes with octal escapes (`"caf\303\251.md"`) unless asked for NUL-separated output. The scans read git's lines as paths, so a file like `café.md` was already crashing them. After this change the same file is quietly dropped: it is never read, the scan says "OK", and the only hint is a stderr line claiming the file is "not present on disk", which is false. That is the Revision's own signal ("a readable file is skipped") and the new docstring's promise ("paths that exist on disk"). Cairn's own tree has no such name (B6), so no test or gate here sees it; an adopter with accented or non-Latin file names would.

*Evidence.* B4 and B5, on all three scripts.

*Satisfier.* In the four `tracked_markdown()` copies, pass `-z` to `git ls-files` and split on NUL instead of newline (B5 shows it reaches the cause and breaks none of the 58 tests I ran). Add one test node: a present file with a non-ASCII name and a broken link, expecting it scanned and the link flagged (exit 1) in `link_check` and `check_cairn`. The easy-defect permission fits: the promise broken is the one this commit wrote into the docstring, the files are already edited, and no rule text changes. It is not cheap if it slides into a different design; keep it to `-z` and the split. The pre-existing crash and this false pass are the same defect, so one fix closes both.

**CR2 -- Low -- non-blocking: "the path is now a directory" is not pinned, and one mutation survives.**

*Plain.* The docstring says files that exist on disk; the code uses `is_file()` so a directory is skipped and counted (A3). No test fails if `is_file()` becomes `exists()` in all four copies, and then the directory case is a traceback again (M10b).

*Satisfier.* One test node alongside the others: replace a tracked `.md` with a directory, expect no traceback and "skipped 1". Add it in the same commit as CR1.

**CR3 -- Low -- non-blocking: the Boundary B record is missing from the commit and is labelled `bounded`.**

*Plain.* See the Bounding verdict. The verification the commit body reports is Boundary A (scoped), which is fine; the Boundary B record is promised for later and the later figure is not in any commit.

*Satisfier.* Put the Boundary B record (`full`, Python 3.13, tests, counts, `Certified by: pending`) in the body of the commit that fixes CR1 and CR2. Nothing else is owed by the implementer; the certifying run comes at the next integration point.

### SR1 to SR3

* **SR1 -- closed.** `scripts/link_check.py:49` and its template twin now read "whole tracked tree (files on disk)"; `docs/tool-usage.md` gained the sentence at its `link_check` entry; `scripts/check_cairn.py:50` says "that exists on disk". The twin-parity test passes (C3). `bootstrap/SAFETY.md:141` describes the filter, not the existence rule, and needs no change.
* **SR2 -- closed.** The docstring of each `tracked_markdown()` says the line names no tool on purpose because `check_cairn` calls the same function. The tests assert the bare text (`skipped 2 tracked Markdown file(s) not present on disk`), and mutants M6 to M9 and M12, M13 confirm they bind it.
* **SR3 -- closed.** The commit body says the self-hosted `dev/.cairn/cairn-lock.yml` is not refreshed and its two hashes go stale. I checked: the lock's hashes for `scripts/link_check.py` and `scripts/sync_doc_snippets.py` equal the parent commit's file bytes and differ from the new ones. The Decision asked for "a sentence", not a place; a commit body is a durable home. If the Maintainer wants it in a document the next regenerator will read, that is theirs to say.

### Tests

`bootstrap/tests/test_deleted_tracked_markdown.py` runs each script's real command line (a subprocess of `python scripts/<name>.py --root <repo>`, so the path a person or a hook runs, including `main()`), not a helper. The "8 of 10 failed before" claim reproduces exactly (C2). Names state the property, and the docstrings carry the reason, with no finding or chunk coordinates, as AGENTS.md asks. Gaps: no non-ASCII name (CR1), no directory (CR2), and no behaviour test reaches the `sync_doc_snippets` template copy, which only the parity test guards (M4, M9).

Coverage -- **Covered**: lens 1 (claims: the 8-of-10 and 425 figures reproduced, the docstring's "exists on disk" tested against A3 and B4), lens 2 (production path: real command lines, every script), lens 3 (edge cases: A1 to A6, B4), lens 4 (silent failure: B4 is one), lens 5 (set and callers: listed from the tree, mutated), lens 6 (drift: SR1 to SR3 opened against the lock and docs), lens 7 (ordering against the queued re-anchor: `_gate_manifest.py verify` shows the five files plus the owed test file, as the commit says), lens 9 (each finding names a satisfier). **Not covered / low confidence**: I did not run the full suite, the certifying pair, or the re-anchor (not mine); I did not run an adopter install or upgrade of the changed templates (the second-round review did, at the earlier commit); I read but did not run `content_scan_runner`'s handling of an absent file; I did not test Windows paths, a sparse checkout, a submodule, or a `--root` outside any git repository (that last case raises a `CalledProcessError` before and after).

**Status** stays `accepted`: this proposal has no plan, so the code review does not move it. Archiving it is the implementing-commit housekeeping that AGENTS.md and the lifecycle doctrine leave until review has passed; it is owed after CR1 to CR3 are answered.
