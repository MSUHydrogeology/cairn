# Plan: re-anchor ceremony without an outside reader

**Author**: Claude Sonnet 5.5 (Strategy)
**Source proposal**: [dev/proposals/archive/2026-10-27-claude-ceremony-without-external-review.md](../proposals/archive/2026-10-27-claude-ceremony-without-external-review.md)
**Status**: awaiting-plan-review
**Waiting on Maintainer**: first ceremony (final chunk)
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-27
**In brief**: A fresh agent and automated scanners replace the outside reviewer of the re-anchor ceremony, the report gets a plain page, the runbook shrinks to one page, and the Maintainer only compares digests and signs.

The Security Review is a separate pass; the ordinary pass never clears it.

## Source proposal

Accepted 2026-10-27 as revised (Decision `c88e4a62`). **Revision 3 is the whole contract**, with the Revision 2 sections it names. His six answers: yes to lifting the driver-cleanup and runbook-cut fences; yes to authorizing the first ceremony in his own words at that ceremony; the one-page runbook stays a pinned closure member; chunk 6 is built (last, droppable); no stale-pin warning; a fresh same-vendor reader is acceptable, stated in each record.

## Scope

**In.** Chunks C1 to C7 (Revision 3 chunks 1 to 7) and C8, the ceremony. **Out.** `bootstrap/_scaffold/`, `scaffold_ast_known_new.json`, the AST baseline, `gate_manifest.json`, the gate anchor (an implementer never edits or moves them), `dev/PLANNING.md`, `CHANGELOG.md` (the planning session's), and `_gate_reanchor.py promote` (stays callable).

**Rules for implementers.** Every implementer, editor and reviewer first reads the current `dev/plans/_template.md` and its word budgets. Tests, comments and docstrings carry no finding ids, chunk letters or plan coordinates. Each chunk's first criterion: `python tools/intent.py list` shows no other claim on its files. A mutant is one deliberate break in its own detached worktree beside an unmutated control; a skipped node is a survivor (`pytest -rs`). Nobody runs a ceremony, a re-anchor or a signing.

**Reuse.** Searched `git grep -n "raw_tree\|_batch_blobs\|_blob_at\|_classify_path\|is_sensitive" -- bootstrap scripts`: C2 reuses them, extends `scan_targets()` rather than adding a scanner, and adds no closure member. C4 generalizes the test helpers `_compose_packet` and `_instantiate` (`test_reanchor.py:989-1006`); `repin` keeps its own blob reader because it runs before the checker loads. One placement the proposal left open: its condition that a test compares the record's digests lands in C4.

**Doctrine / descriptive surface.** `bootstrap/REANCHOR_RUNBOOK.md`, `doctrine/dual-review.md:85-91`, `SECURITY.md:167,:234`, `bootstrap/SAFETY.md:657-658`, template and artifact comments. Rule text in them changes only as the Maintainer's Decision above authorizes; `SECURITY_MUTATIONS.md` says only past reviews (no change).

Proposed paths:
* `bootstrap/tests/test_ceremony_review_report.py`

**Frozen files and AST, derived 2026-10-27** from `_frozen_files` globs, the 195 keys of `gate_manifest.json` and read-only `verify --no-collect`.

| File | Chunk | State |
|---|---|---|
| `security_check.py`, `_gate_preflight.py`, `test_gate_preflight.py`, `test_reanchor.py`, `test_review_stance_in_shipped_files.py` | 1, 2, 5, 6, 7 | keyed, already FROZEN-MODIFIED: no new entry |
| `scripts/reanchor_ceremony.py` | 3 | keyed; new FROZEN-MODIFIED |
| `correct_pinned_digests.py` and its test | 3 | keyed; new FROZEN-MISSING, nine COLLECTION-DROPPED |
| `scripts/repin.py`, `test_repin*.py`, the new test file | 4, 1-6 | unkeyed: FROZEN-NEW, free |
| `reanchor.sh`, launcher template, runbook | 2, 6, 7 | closure, not globbed: pinned by the packet |

Plus the runbook-reading nodes C7 drops (derived at the cut). **AST:** none expected. Read-only `_ast_attest.py verify` covers only `bootstrap/_scaffold/*.py` (59 lines red today, from the range); no chunk edits that directory. Save its output before C1 and after the last commit; they must match.

## Sequence

C1 to C7 land as **one reviewed range**: C2, C5, C6 and C7 edit closure members, so `scripts/repin.py:1027` refuses any ordinary ceremony from C2 on and one hand ceremony pins them all. Each chunk is green on its mapped tests; the manifest and AST gates are already red and stay red until C8, so this plan adds to the owed list, not to a new kind of red. Two commits never split: C6's parser removal with all its callers, and C7's prose with the tests that read it.

| # | Chunk | Gate |
|---|---|---|
| C1 | Scanner coverage: seven closure Python members | none |
| C2 | Report items in `range_review_report` and `reanchor.sh` | none |
| C3 | Driver cleanup | none |
| C4 | `repin`: `packet` verb, launcher check, Summary 2, record check | after C3 |
| C5 | Evidence environment: reproduce, then refuse | none |
| C6 | One values reader (last code chunk, droppable) | after C1-C5 |
| C7 | Prose and tests; runbook to one page | after C6 |
| C8 | The ceremony | **MAINTAINER-ONLY** |

## Acceptance criteria

**C1.** `scan_targets()` lists the seven `bootstrap/tests` Python closure members. A node in `bootstrap/tests/test_ceremony_review_report.py` compares them with `declared_authority_closure()` (a new Python member fails it). Control: Bandit on the seven (54 LOW, measured today) leaves `test_security_lint.py::test_no_blocking_security_findings` passed; the record shows that node ran, not skipped, and the Bandit version. A planted `subprocess.run(..., shell=True)` in a scratch copy of one member blocks. Mutants (each beside the control): drop one member; drop the comparison.

**C2.** Schema `cairn-range-review/v2`; stage 2's re-derivation still matches. Each path has a role (decides, pinned, other). Scan per Revision 3 over raw blobs: a `-diff` attribute still scans; unreadable or oversized blobs and modes 100755, 120000, 160000 are listed; all hits are shown; each pattern prints a count, zeros included. Every `allowed_signers` fingerprint is printed and a change flagged. The renderer encodes new fields and refuses unprintable text. In a transition the scan is recomputed from `raw_tree(anchor)` and compared; a difference stops; an anchor with no scan prints "not computed" and never "equal". Nodes: planted line per pattern; zero-hit control; the three transition cases. Mutants: use `git diff`; truncate hits; skip one decides path; drop the flag.

**C3.** `git grep -n "def drive\|--run\|correct_pinned_digests" -- scripts` finds nothing (control: the parent finds them). The undefined `template`, the stale docstring, the "out of band" sentence and the printed commands are fixed; a node runs each printed command form against the real artifact; a candidate with no `EXPECTED_PATHS` stops with the template path. The nine dropped ids are listed from the fixture. The code review reads the whole driver diff. Mutant: restore the undefined name.

**C4.** `repin packet` writes the packet and the launcher (the anchor's template with the slot filled), byte-equal to the helper's output on the same tree; in a transition it refuses and writes nothing. A launcher differing by one byte from the anchor's template refuses before any child runs; control: the derived one passes. Summary 2 prints the new report items; the prompt says "the record". A missing record, or one whose packet, launcher or member digest differs, refuses. Nodes in the unkeyed repin tests. Mutants: skip the launcher check; skip each record digest.

**C5.** Reproduce first: `PYTEST_ADDOPTS` into `gather_evidence` directly and through the launcher; commit the result. If only the direct call drops nodes, `dev/PLANNING.md` closes that row. Direct call refuses `PYTEST_ADDOPTS`, `PYTEST_PLUGINS`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD`, one node each; control: `PYTEST_CURRENT_TEST` set does not refuse. `-B` only if a committed compiled file is shown to load. Mutants: drop each name; refuse every `PYTEST_*`.

**C6.** Parity matrix over all 13 keys passes both ways before the artifact's parser goes; then hostile values files are refused by the real launcher before any stand-in program logs a call. A node counts programs before the first `exec`: six (`env git shasum mktemp mkdir cat`). The artifact keeps its own argument checks (a bad path refuses when called directly). `hash-package` uses the launcher's `shasum`. Callers changed: `repin.py:1001,1056,1060`, `reanchor.sh:544-546`, runbook, `test_reanchor.py`, `test_repin_ceremony.py`. **Falsifier:** a seventh program or a new grammar drops this chunk. Mutant: add a seventh.

**C7.** Operative runbook page at most 80 lines (my figure); Phase 0 steps 1-4 and Phase 4 gone; the atomic push, transition-mode and dated-posture text kept, so the file is not one page (named to the Maintainer). The page holds the values-file step and E6, the launcher command, the exact stage-2 command (no `ssh-add`; the artifact's advice text is edited to match), the push, the first-ceremony authorization. Edited with their tests: `test_gate_preflight.py:1936,3081,5569-5687`, `test_reanchor.py:1603-1720`, `test_review_stance_in_shipped_files.py:1117-1126`, `doctrine/dual-review.md`, `SAFETY.md`, `SECURITY.md`, comments. Dropped nodes are listed. Mutant: delete the push block; its node fails.

**C8.** Fence below.

**C8 fence (MAINTAINER-ONLY).** Builder agent hand-builds the first packet and launcher; a distinct fresh reader reads the diff, runs the scanners with planted controls, states that it is a same-vendor fresh session that wrote nothing in the range (a statement, not checkable) and commits the record before he signs. He authorizes in his words, naming `bootstrap/_scaffold/`, `bootstrap/security_check.py`, `bootstrap/tests/_gate_manifest.py` and the dropped nodes re-derived from the final tree (`_gate_manifest.py verify`). He compares E1-E6 and runs the exact stage-2 command. Stage 2 should sign the new anchor (`git verify-commit` with the roster); if it does not, the `AGENTS.md` sentence is corrected instead.

## Scope delta

**Scope delta**: degraded, one unit as accepted: the standing outside reader is replaced by the fresh local reader; **disposition**: guard. Nothing else is cut. C6 may drop only through its falsifier, with the Maintainer told.

## Verification

**Boundary A**, owners re-found by `git grep -l '<symbol>' -- bootstrap/tests` at each landing: C1 `test_security_check`, `test_security_lint`, `test_scaffold_substrate`; C2, C5 `test_gate_preflight`, the new file, `test_reanchor`; C3 `test_reanchor_driver_disclosures`, `test_repin*`; C4 `test_repin*`; C6 `test_reanchor`, `test_repin_ceremony`; C7 those, `test_review_stance_in_shipped_files`, `check_cairn.py`, `claim_check.py`, `link_check.py`, `quality_gate.py --sub neutrality --sub redundancy`.

**Boundary B mode: `full`** (trust-ceremony surface). The record is scoped: `**Certified by**: pending`. Nobody sets `CAIRN_FULL_SUITE`. Interpreter `/Users/kendal30/conda_envs/lhm/bin/python3.13`.

**After C7:** one code review; a Security Review that reads the launcher and artifact whole, the checker's changed hunks, `repin`'s verb and launcher check, the driver diff, the `security_check.py` hunk and the one-page runbook; a certifying run; builder and reader; C8. **Not measured:** a real ceremony; the several-day cost is assumed.
