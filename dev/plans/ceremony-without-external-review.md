# Plan: re-anchor ceremony without an outside reader

**Author**: Claude Sonnet 5.5 (Strategy)
**Source proposal**: [dev/proposals/archive/2026-10-27-claude-ceremony-without-external-review.md](../proposals/archive/2026-10-27-claude-ceremony-without-external-review.md)
**Status**: revising-code
**Waiting on Maintainer**: first ceremony (final chunk)
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-27
**In brief**: A fresh agent and automated scanners replace the outside reviewer of the re-anchor ceremony, and the Maintainer compares digests on a plain page and signs.

## Source proposal

Accepted 2026-10-27 as revised (Decision `c88e4a62`); **Revision 3 is the whole contract**, with the Revision 2 sections it names. His six answers: both fences lifted; he authorizes the first ceremony in his words then; the runbook stays pinned; chunk 6 built; no stale-pin warning; a fresh same-vendor reader accepted, stated in each record.

## Scope

**In.** C1 to C7b (Revision 3's chunks 1 to 7, with 2 and 7 split) and C8, the ceremony. **Out.** `bootstrap/_scaffold/`, `scaffold_ast_known_new.json`, the AST baseline, `gate_manifest.json`, the gate anchor (never edited or moved by an implementer), `dev/PLANNING.md`, `CHANGELOG.md`.

**Rules for implementers.** Everyone first reads the current `dev/plans/_template.md` and its word budgets. Tests, comments and docstrings carry no finding ids, chunk letters or plan coordinates. Start each chunk with `python tools/intent.py list` showing no other claim on its files. A mutant is one deliberate break in its own detached worktree beside an unmutated control; a skipped node or unmeasured equivalence is a survivor. Nobody runs a ceremony, re-anchor or signing.

**Reuse.** Searched `git grep -n "raw_tree\|_batch_blobs\|_blob_at\|_classify_path\|is_sensitive" -- bootstrap scripts`: C2 reuses them. C4 generalizes the test helpers `_compose_packet` and `_instantiate` (`test_reanchor.py:989-1006`); `repin` keeps its own blob reader (it runs before the checker loads).

**Doctrine / descriptive surface.** `bootstrap/REANCHOR_RUNBOOK.md`, `doctrine/dual-review.md:85-91`, `SECURITY.md:167,:234`, `bootstrap/SAFETY.md:657-658`, template and artifact comments. Rule text changes only as the Maintainer's Decision above authorizes. `SECURITY_MUTATIONS.md`: no change.

**Plain glosses.** He compares: E1 the launcher's digest (fingerprint) with the record's; E2 the page's commit with his `git rev-parse HEAD`; E3 the two package digests; E4 his key's fingerprint with the page's list; E5 both SAME commands print SAME (1: the candidate's launcher template is the reviewed one; 2: the launcher is that template with one slot filled); E6 each tool path in his values file with `readlink -f "$(command -v <tool>)"` (plain `command -v git` is a symlink the file refuses); E7 the scan digest the anchor's own code prints with the page's. Y1 to Y5 are his yes/no answers. Summary 2 is `repin`'s last screen before signing; stage 2 is the signing run.

**The record.** `dev/ceremony-record.md`, one fixed path: the commit the reader read (R), the packet, launcher and 11 member digests, the reader's statements. It is the candidate's tip: committed on R, changing only that file. The packet holds no commit id by design (`bootstrap/reanchor-launcher.template.sh:376-383`), so naming digests is not circular. `repin` (C4) and, for hand runs, the page (C7) check that `HEAD^` equals R, `git diff --name-only HEAD^ HEAD` prints only that path, and the digests match; E2 compares his `HEAD`. It binds what is signed to what was read plus one file; without it a later commit (to `bootstrap/_scaffold/`, say) passes E1 to E6, since the packet pins only 11 files.

**Transitions (second and later).** The anchored runbook prints one command that extracts the anchor's own `bootstrap/tests` into an empty folder and runs its checker's `scan-digest` (C2); he compares it with the page's (E7), so candidate code does not judge itself. The first ceremony has no anchored scan; the page and record say it rests on builder and reader.

Proposed paths:
* `dev/ceremony-record.md`

**Frozen files and AST, derived 2026-10-27** from `_frozen_files` globs, the 195 keys of `gate_manifest.json` and read-only `verify --no-collect`.

| File | State |
|---|---|
| `security_check.py`, `_gate_preflight.py`, `test_gate_preflight.py`, `test_reanchor.py`, `test_review_stance_in_shipped_files.py` | keyed, already FROZEN-MODIFIED: no new entry |
| `scripts/reanchor_ceremony.py` | keyed; new FROZEN-MODIFIED |
| `correct_pinned_digests.py`, its test | keyed; new FROZEN-MISSING, nine nodes dropped, plus C7's |
| `scripts/repin.py`, `test_repin*.py`, the new test file | unkeyed: FROZEN-NEW, free |
| `reanchor.sh`, launcher template, runbook | closure, not globbed: pinned by the packet |

**AST:** none expected. `_ast_attest.py verify` covers only `bootstrap/_scaffold/*.py` (59 lines red today); no chunk edits it. Save its output before C1 and after the last commit; they must match.

## Sequence

C1 to C7b land as **one reviewed range**: C2, C2b, C5, C6 and C7 edit closure members, so `scripts/repin.py:1027` refuses ordinary ceremonies from C2 on; one hand ceremony pins all. Each chunk is green on its mapped tests (the manifest and AST gates are already red). Never split: C6's parser removal and its callers; C7's page and its tests. C6 is droppable only until C7 lands: its mode commands sit in one runbook block, so a later drop reverts C6 and edits that block alone.

| # | Chunk | Gate |
|---|---|---|
| C1 | Scanner coverage | none |
| C2 | Report items, `scan-digest` | none |
| C2b | The page (`reanchor.sh`) | after C2 |
| C3 | Driver cleanup | none |
| C4 | `repin`: packet, launcher, record | after C3 |
| C5 | Evidence environment | none |
| C6 | One values reader | after C1-C5 |
| C7 | Runbook page, exact commands | after C6 |
| C7b | Doctrine prose | after C7 |
| C8 | The ceremony | **MAINTAINER-ONLY** |

## Acceptance criteria

**C1.** `scan_targets()` lists the seven `bootstrap/tests` Python closure members. A node in `bootstrap/tests/test_ceremony_review_report.py` compares them with `declared_authority_closure()` (a new member fails it). Control: Bandit on the seven (54 LOW, measured today) leaves `test_security_lint.py::test_no_blocking_security_findings` passed; the record shows that node ran, not skipped, and cites `python bootstrap/security_check.py` (it fails closed without Bandit). A planted `shell=True` in a scratch copy blocks. Re-run `test_security_lint` after C2 and C5 and at the last commit. Mutants: drop one member; drop the comparison.

**C2.** Schema `cairn-range-review/v2`; stage 2's re-derivation still matches. Each path has a role (decides, pinned, other). Scan over raw blobs with a fixed pattern list in `_gate_preflight.py` (process start, network, dynamic code, `shell=True`, file writes, `nosec`): a `-diff` attribute still scans; unreadable or oversized blobs and modes 100755, 120000, 160000 are listed; every hit is kept, escaped as `_display_path` does; counts per pattern include zeros. Scanned: decides paths, the sensitive roster, new `scripts/` and `bootstrap/` files outside tests; the rest is listed "not line-scanned: class, N". `scan-digest` prints SHA-256 of the canonical scan. Nodes: a planted line per pattern; zero-hit control; scope (roster file scanned, test file listed); a candidate scan that hides a hit gives a digest unequal to the anchor-code run. Mutants: `git diff`; truncate; skip a decides path; drop `nosec`; drop the roster; run `scan-digest` from the candidate's checker (the hiding node must then fail).

**C2b.** `show-report` prints, with no per-class cut (today 40, `reanchor.sh:703`): roles, hits, modes, every `allowed_signers` fingerprint with a change flagged, the candidate id, package digest, each tool path the values file names (E6), the scan digest (E7), and Y1 to Y5 as numbered yes/no lines. Text with unprintable bytes is refused. A report with no anchored scan prints "not computed", never "equal". Control: existing `show-report` nodes pass. Nodes: one per element. Mutants: cut at 40; print raw bytes; print "equal" when not computed; drop the E6 lines; drop a Y line.

**C3.** `git grep -n "def drive\|--run\|correct_pinned_digests" -- scripts` finds nothing (control: the parent finds them). The undefined `template`, stale docstring, "out of band" sentence and printed commands are fixed; a node runs each printed command form against the real artifact; a candidate with no `EXPECTED_PATHS` stops naming the template path. `values_field`, `compare`, `check_packet_pair` and `packet_artifact_digest` stay (`repin` calls them, `scripts/repin.py:952-988`); `test_repin*.py` pass. Nine dropped ids listed from the fixture. The code review reads the whole driver diff. Mutant: restore the undefined name.

**C4.** `repin packet` writes the packet and the launcher (the anchor's template, slot filled), byte-equal to the helper's output on the same tree; in a transition it refuses and writes nothing. A launcher one byte off the anchor's template refuses before any child runs. Summary 2 prints the C2b lines; the prompt says "the record". Record check per Scope, one node each: missing record; `HEAD^` not R; any other path changed; a differing packet, launcher or member digest. Control: a good record passes. Mutants: skip each of the four; write in a transition; skip the launcher check.

**C5.** Reproduce first: `PYTEST_ADDOPTS` into `gather_evidence` directly and through the launcher; commit the result. If only the direct call drops nodes, the `dev/PLANNING.md` row closes. The direct call refuses `PYTEST_ADDOPTS`, `PYTEST_PLUGINS`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD`, one node each; control: `PYTEST_CURRENT_TEST` set does not refuse. `-B` only if a committed compiled file is shown to load. Mutants: drop each name; refuse every `PYTEST_*`.

**C6.** Parity matrix over all 13 keys passes both ways before the artifact's parser goes; then hostile values files are refused by the real launcher before any stand-in program logs a call. A node counts programs before the first `exec`: six (`env git shasum mktemp mkdir cat`). The artifact keeps its argument checks (a bad path refuses when called directly). `hash-package` uses the launcher's `shasum`. Callers changed: `repin.py:1001,1056,1060`, `reanchor.sh:544-546`, runbook, `test_reanchor.py`, `test_repin_ceremony.py`. **Falsifier:** a seventh program or a new grammar drops this chunk. Mutants: add a seventh; delete one key's check (the hostile file must then be killed).

**C7.** The page is at most 80 lines above `<!-- end of page -->` (a node counts); kept text (atomic push, transition mode, dated posture) sits below, whole file about 250 to 300 lines (told to the Maintainer; his Q3 answer pinned it, not its length). Phase 0 steps 1 to 4 and Phase 4 are gone. The page says nothing calls `_gate_reanchor.py promote`, which stays. The page holds each exact command: E1 to E7, SAME (1) and (2), the record checks, and before stage 2 a launcher re-hash, a repeat of E6 and `ssh-add -l` not listing his key. Stage 2 runs under `env -i HOME=<home> PATH=/usr/bin:/bin TERM="$TERM" LANG=C`, no `SSH_AUTH_SOCK`; the artifact's `ssh-add` advice is edited to match. Nodes: stage-2 variable names equal `repin`'s (`scripts/repin.py:1075`). Mutants: add `SSH_AUTH_SOCK`; delete the push block. Dependent tests (`test_gate_preflight.py:1936,3081,5569-5687`, `test_reanchor.py:1603-1720`) edited; dropped nodes listed.

**C7b.** `doctrine/dual-review.md:85-91` and its pinned sentence (`test_review_stance_in_shipped_files.py:1117-1126`) change together; `SAFETY.md`, `SECURITY.md` and template, artifact and checker comments say a fresh local reader plus scanners, not an outside review. `git grep -n -i "external security review"` over those files finds no requirement (control: the parent does; history lines named in the commit). Gates: `check_cairn.py`, `claim_check.py`, `link_check.py`, neutrality and redundancy.

**C8 fence (MAINTAINER-ONLY).** The builder (a fresh session, key not loaded: `ssh-add -l` shows nothing of his) hand-builds the first packet and launcher and runs stage 1 on his trusted machine; a distinct fresh reader reads the diff, runs the scanners with planted controls, states it is a same-vendor session that wrote nothing in the range (a statement, not checkable), saves the re-derived dropped-node list, and commits the record on the candidate before he signs. He authorizes in his words, naming `bootstrap/_scaffold/`, `bootstrap/security_check.py`, `bootstrap/tests/_gate_manifest.py` and that list by count and commit, and names the known manifest and AST reds as the Y4 allowance. He runs the SAME commands and E1 to E6, then stage 2. It should sign the new anchor; if not, the `AGENTS.md` sentence is corrected instead.

## Scope delta

**Scope delta**: degraded, one unit as accepted: the outside reader is replaced by the fresh local reader; **disposition**: guard. C6 drops only through its falsifier, with the Maintainer told.

## Verification

**Boundary A**, owners re-found by `git grep -l '<symbol>' -- bootstrap/tests` at each landing: C1, C2, C5 `test_security_check`, `test_security_lint`, `test_gate_preflight`, the new file; C2b, C6 `test_reanchor`, `test_repin_ceremony`; C3, C4 `test_reanchor_driver_disclosures`, `test_repin*`; C7, C7b those, `test_review_stance_in_shipped_files`, the prose gates.

**Boundary B mode: `full`** (trust-ceremony surface); record scoped, `**Certified by**: pending`; nobody sets `CAIRN_FULL_SUITE`; interpreter `/Users/kendal30/conda_envs/lhm/bin/python3.13`.

**After C7b:** one code review; a Security Review reading the launcher and artifact whole, the changed checker hunks, `repin`'s new checks, the driver diff and the runbook; a certifying run; C8.

## Plan review -- Claude Sonnet 5.5 (Internal, fresh session) -- 2026-10-27

**Tier**: Internal. **Reviewed commit**: 91102afc. **Verdict**: three blocking, six non-blocking; Status to `revising-plan`. The Security Review is separate.

**Foundations**
1. *Delivers Revision 3?* In shape yes: each chunk maps to a Revision 3 chunk (plan `:59-71`); three outcomes lack an owner (B1 to B3). Backing: closure is 11 files, 7 Python (`_gate_preflight.py:627-639`); `scripts/repin.py:1026-1029` refuses closure changes.
2. *Simpler path?* Same chunks. C4's record check stays only if B1 is settled; else the C8 hand comparison carries it.
3. *Shows it cannot deliver?* A record whose digests change when committed (B1); a candidate scan that hides a hit yet passes the compare (B2). Read-only: `verify --no-collect` agrees with the plan's table (`gate_manifest.json:533-541` holds the nine nodes); AST verify is red on 59 lines; `bootstrap/_scaffold` has no diff from 91102afc.

### Blocking

**B1. The record has no home, and committing it moves HEAD.** C4's record check is a good owner for the proposal's condition, but the plan gives no path or format. A record inside the candidate cannot name that commit's packet digest (circular); one committed on top makes HEAD differ from the candidate, and E2 compares `git rev-parse HEAD`. *Fix*: state the path, the digest lines, and that the record sits one commit above the candidate it names; give `repin`, E2 and C8 that rule; list the check for the Security Review.

**B2. C2 does not say whose code computes the transition scan.** "Recomputed from `raw_tree(anchor)`" can mean the candidate's checker scanning the anchor's files. Revision 3 requires the anchor's own checker, extracted. *Fix*: say so; add a node where the candidate's scan hides a hit and the compare still stops, and the mutant "compute with the candidate's checker".

**B3. E6 and the Y-answers print nowhere.** Revision 3 says the page prints each values-file tool path. `show-report` (`reanchor.sh:686-748`) prints none; C7 only says "the page holds E6". *Fix*: C2 prints them, with a node; or say E6 is prose only. Name the chunk that prints Y1 to Y5.

### Non-blocking

* **N1.** C1 adds seven members to Bandit; C2 and C5 edit them, yet their owners omit `test_security_lint`. *Fix*: add it; re-run the Bandit node at the last commit.
* **N2.** C2 has no node or mutant for unprintable-text refusal, the sensitive-roster and new-file scope, or the "not line-scanned" list; the pattern list has no home. *Fix*: add them.
* **N3.** C7: the 80-line ceiling has no check, and Phase 5 alone is 67 lines (`REANCHOR_RUNBOOK.md:542-608`), so the push block may not fit. *Fix*: a marked end line, a counting node, and the expected whole-file length told to the Maintainer (Q3 promised one page). Add a grep, with a control, for leftover External-review wording (`_gate_preflight.py:9`, `test_reanchor.py:1790`); `SECURITY.md:237` is in Revision 2's list.
* **N4.** C6 is droppable only until C7 lands; the Security Review follows C7. *Fix*: keep C6's mode commands in one runbook block, so a late drop edits only it.
* **N5.** C8: say who runs stage 1 and the SAME commands, that no agent loads the key, the trusted-machine statement, and the Y4 allowance for the known manifest and AST reds. Save the re-derived dropped-node list in the record so his words cite it by count and commit.
* **N6.** E1 to E6, SAME, Summary 2 and "stage 2" are unglossed. *Fix*: gloss them once.

**Coverage.** Read-only. Not run: suite, Bandit, ceremony, `repin`. Not checked: the 54 LOW count, the six-program count, the C6 parity matrix, whether chunks stay green (hardening was red between chunks). Budgets measured: body 867, criteria at most 117 per chunk.

## Plan review -- Claude Opus 5.5 (Internal Security Review, fresh session) -- 2026-10-27

**Obligation**: plan review of the re-anchor ceremony rewrite and its chunk list (trust-ceremony surfaces; Security Review owed by the plan header `required(Internal + Internal Security Review)`)
**Reviewed commit**: 3e73c5dc. **Verdict**: three blocking, four non-blocking; stays `revising-plan`. Cleared by a revision adopting SB1 to SB3.

**Foundations**
1. *Delivers Revision 3?* Ordinary ceremonies yes: repin runs only anchored code (`scripts/repin.py:289-294`, `:1027`). The transition control and the record do not (SB1, SB2).
2. *Safer build?* Anchor code computes the transition scan as one more digest he compares; the record is the candidate's last commit (`bootstrap/reanchor-launcher.template.sh:376-383`).
3. *Shows it wrong?* A second-transition candidate whose `reanchor.sh` skips the comparison passes his checks; so does a post-read commit to `bootstrap/_scaffold/` (the packet pins only 11 files) (plan `:61`; template `:612-660`).

### Blocking

**SB1. Candidate code drives the transition scan** (extends B2). In a transition the launcher, artifact and checker are the candidate's, so it decides whether the anchor's checker is called and what "equal" prints. *Fix*: the anchored runbook prints one command that extracts the anchor's own code (`git show refs/cairn/gate-anchor:...`, `python -I`, empty folder) and prints a scan digest; he compares it with the page's (E7). Mutant: the candidate's artifact omits the comparison; E7 still stops.

**SB2. Nothing binds what the reader read to what he signs** (resolves B1). B1's premise is wrong, measured: the packet holds no commit id (template `:376-383`), so a record inside the candidate can name packet, launcher and member digests. *Fix*: the record is the candidate's tip commit, changing only the record file at one fixed path, and names the commit it read. Checks: `git rev-parse HEAD^` equals it; `git diff --name-only HEAD^ HEAD` prints only the record path; SAME command (1)'s `$REV` is it. C4 runs these in ordinary ceremonies; the page prints them for hand runs.

**SB3. No chunk owns the commands for E1 to E6** (extends B3). Measured: the two SAME commands exist only in `dev/plans/archive/repin-ceremony-hardening.md:86`. E6 cannot pass here: `command -v git` gives `/opt/homebrew/bin/git`, a symlink the values file refuses (`bootstrap/reanchor-values.example:30-36`). *Fix*: C7's page holds each exact command; E6 uses `readlink -f "$(command -v <tool>)"`. Before stage 2 he re-hashes the launcher and repeats E6, as repin does (`scripts/repin.py:974-977`), and `ssh-add -l` must not list his key (Y5 becomes a check). Stage 2 starts `env -i HOME=<home> PATH=/usr/bin:/bin TERM="$TERM" LANG=C`, so no agent socket reaches the signer (`bootstrap/reanchor.sh:661` forwards it; `scripts/repin.py:1075` does not).

### Non-blocking

* **SN1.** C1: `# nosec` silences Bandit; the seven hold none (measured). Add `nosec` to C2's patterns. The record cites `python bootstrap/security_check.py`, which fails closed without Bandit (`:862`).
* **SN2.** C2: `show-report` cuts each class at 40 (`reanchor.sh:703`); never cut hits or roles. Hit text is candidate bytes: escape it as `_display_path` does.
* **SN3.** Missing mutants: `repin packet` writes nothing in a transition; "not computed" never prints "equal"; hostile values refused before any program; no `EXPECTED_PATHS` stops. Add: equivalence measured, else a survivor.
* **SN4.** (g) holds (plan `:19`, `:21`). C3 keeps the four driver functions repin calls (`scripts/repin.py:952-988`).

**What still gets past.** First ceremony: every copy he compares comes from the builder, reader or candidate code; his checks prove agreement, not safety. Always: a harmful change matching no pattern, or a removed check, passes if the reader misses it. Stage 1 runs candidate code as him and can replace a tool he owns (`/opt/homebrew`); E6 compares paths, not bytes.

**Coverage.** Read-only: `repin status`, `verify --no-collect`, `claim_check`. Not run: suite, Bandit, mutants, `_ast_attest verify`. Not read: C6's reader, `_scrubbed_environ`, stage 2's checker.

## Response to plan review -- Claude Sonnet 5.5 (author) -- 2026-10-27

I checked each point in the tree. "Measured" is a command I ran, "read" is code I read, "not run" is a design nothing has exercised yet. The operative cells above are revised in place; this table points at them. Status moves to `ready-to-implement`: SB1 to SB3 and B1 to B3 are adopted.

**Internal pass**
* **B1 accept-modified (and SB2).** The reviews disagreed; the tree decides. Read: the packet is commit-id-free by design (`reanchor-launcher.template.sh:376-383`), so a record inside the candidate can name digests and the commit it read without naming itself. I took SB2's design over "one commit above": there HEAD would differ from the candidate and E2 would compare the wrong commit. Scope "The record": fixed path, tip commit on R, `HEAD^` equals R, diff shows only the record. C4 and C7 own the checks.
* **B2 accept.** The anchor's code computes the scan (`scan-digest`, C2); see SB1.
* **B3 accept.** C2b prints E6 paths and Y1 to Y5, a node for each; C7 holds the commands.
* **N1 accept.** C1 and the Boundary A line add `test_security_lint`, re-run after C2, C5 and at the last commit.
* **N2 accept.** C2 names the pattern list's home (`_gate_preflight.py`) and adds scope and "not line-scanned" nodes; C2b adds the unprintable-text node and mutant.
* **N3 accept-modified.** C7 adds a marked end line and a counting node. Whole file about 250 to 300 lines (assumed from today's kept sections: 28, 114 and 67 lines, read), told to the Maintainer. C7b greps for leftover requirement wording, with a control.
* **N4 accept.** Sequence: C6 is droppable only until C7; one runbook block.
* **N5 accept.** C8: who runs stage 1, key not loaded, the Y4 allowance, the dropped-node list saved in the record.
* **N6 accept.** Glosses in Scope.

**Security pass**
* **SB1 accept.** Read: in a transition every part of the page is candidate code (`scripts/repin.py:1027`). C2 adds `scan-digest` to the checker; C7's page holds the command that extracts the anchor's own tree and runs it (E7); C2b prints the page's digest. Node: a candidate scan that hides a hit gives an unequal digest. The compare is his, so the node tests the digests, not his eyes; mutant: run it from the candidate's checker. The first ceremony has no anchored scan and says so.
* **SB2 accept.** As B1.
* **SB3 accept.** Measured: `command -v git` is a symlink (`/opt/homebrew/bin/git`), and the values example refuses symlinks (`reanchor-values.example:30-36`), so E6 uses `readlink -f`. Read: the artifact forwards the key-agent socket (`reanchor.sh:655-661`), `repin` does not (`repin.py:1075`). C7 holds each exact command, the pre-stage-2 re-hash, E6 repeat, `ssh-add -l`, and `env -i`, with a node comparing variable names with `repin`'s. Not run: the commands.
* **SN1 accept.** `nosec` joins C2's patterns; C1 cites `security_check.py` (read: fails closed, `:862`).
* **SN2 accept.** Read: `show-report` counts but hides past 40 (`reanchor.sh:703`); C2b removes the cut; hits are escaped.
* **SN3 accept.** Added mutants: C2b ("equal" when not computed), C4 (write in a transition), C6 (a key check deleted); C3 already had the `EXPECTED_PATHS` one. Unmeasured equivalence is a survivor (Rules).
* **SN4 accept.** C3 keeps the four driver functions `repin` calls (read: `repin.py:952-988`).

**Not checked:** the E and Y commands as typed; whether the code can build the record check without a new closure member (C4 sits in `repin`, which is not one).

## Implementation verification (C1 to C4) -- Claude Sonnet 5.5 -- 2026-10-27

Range `8a4e7508..26b8709c`: C1 `2f4c8a1b`, C2 `dd92e83c`, C2b `ae1d47c2`, C3 `fed00f7b`, C4 `26b8709c`. Interpreter `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13), Bandit 1.9.4. **Boundary B mode**: full; **Certified by**: pending. No push, no suite, no ceremony. Mutants ran in detached worktrees beside a control.

* Tree before and after: clean apart from two untracked paths that are not mine (`.claude/`, `dev/measurement/collision_log.md`).
* C1: `scan_targets()` names the seven members; `test_ceremony_review_report.py` compares them with the closure. Mutants: drop a member, drop the union, add a closure member: 3 killed.
* C1: Bandit on the seven finds 54 LOW; `test_security_lint.py::test_no_blocking_security_findings` ran, not skipped, after C1, C2 and C4. A planted `shell=True` blocks; on the parent it passes. `python bootstrap/security_check.py` not run (a release command).
* C2: `test_ceremony_review_report.py` 25 nodes. 21 mutants killed (`git diff`, truncate, skip a deciding path, drop `nosec`, drop the roster, and more); 1 equivalent, measured: skipping `_oracle_trust.py` as a deciding path passes, skipping it from the roster too is killed.
* C2: over the real anchor to HEAD the scan reports 64 hits in 0.3 s; read as noise level, not as findings.
* C2b: `TestShowReport` 24 nodes; 17 mutants killed (cut at 40, raw bytes, "equal" unearned, E6 lines, Y lines, and more).
* C3: grep for `def drive|--run|correct_pinned_digests` over `scripts/`: 6 lines on `ae1d47c2`, 0 now. 7 mutants killed, including the undefined name.
* C4: 13 mutants killed (each record check and each digest kind, a write in a transition, the launcher check, packet bytes, the prompt).
* Tests: C2 owners 873 passed; C3 owners 203 passed; C4 owners 571 passed (`test_repin_ceremony`, `test_repin`, `test_reanchor`, driver disclosures, the new file, `test_security_lint`, `test_security_check`). 0 skipped, 0 failed.
* `_ast_attest.py verify`, read-only: output identical before and after (59 symbols red, as the plan says).
* `_gate_manifest.py verify --no-collect`, read-only: matches the plan's table (`reanchor_ceremony.py` new MODIFIED; `correct_pinned_digests.py` and its test MISSING; the rest NEW).
* Dropped nodes: nine in `gate_manifest.json:533-541`, plus `test_reanchor.py::TestShowReport::test_a_long_class_is_bounded_and_SAYS_it_was_bounded` (the cut it tested is gone; replaced by `test_no_class_is_cut_however_long`).
* Gates: neutrality and redundancy clean. `check_cairn` flags four citations of the deleted files in `dev/plans/repin-build.md` (ready-to-archive); not edited.

**Choices the plan left open.** The report names who made the scan (`scan_checker`), not an anchored digest in the package, so the package schema is untouched. "Decides" also holds `bootstrap/tests/__init__.py` and `_ast_attest.py`, which `repin` byte-compares. The existing "control: show-report nodes pass" holds for all but the cut node. `test_repin_ceremony.py`: `drive()` commits a good record first.

**Not verified.** The E and Y commands as typed; stage 1 through the launcher on real keys; the full suite; `python bootstrap/security_check.py`; C5 to C7b.

## Implementation verification (C5 to C7b) -- Claude Sonnet 5.5 -- 2026-10-27

Range `77f3e5d1..3ed66cf4`: C5 `95021c2d`, C6 `b748de2d`, C7 `8df7e2a2`, C7b `3ed66cf4`. Interpreter `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13). **Boundary B mode**: full; **Certified by**: pending. No push, suite, ceremony, launcher run or `security_check.py`. Owners and mutants ran in detached worktrees holding HEAD plus only the chunk's files, each beside a control.

* Tree: clean apart from two untracked paths that are not mine. Skipped nodes in any run: 0.
* C5 reproduced: `PYTEST_ADDOPTS=--ignore=<file>` into the direct `evidence` call kept 5321 of 5346 nodes and exited 0; the same under the `env -i ... python -E -s` form `reanchor.sh` uses kept 5346. The launcher itself was not run, so the `dev/PLANNING.md` row closes on that form (the planning session edits it). `-B` not added. 6 mutants killed.
* C6 falsifier did not fire: six programs before the first `exec` (a log node and a shell-trace node), no new grammar.
* C6 parity: a 77-case matrix over all 13 keys, old artifact parser against the new launcher reader, agreed and accepted the clean file; measured in a copy before the parser went, not committed; its control (one launcher check deleted) failed.
* C6 mutants: 71, 70 killed, 1 equivalent, measured: deleting the package-absolute check alone passes because the package-parent check recovers it; deleting both is killed.
* C6 owners: 914 passed (`test_reanchor`, `test_repin_ceremony`, `test_repin`, driver disclosures, `test_gate_preflight`, `test_ceremony_review_report`, `test_security_lint` (Bandit node ran), `test_security_check`, `test_gate_reanchor`).
* C7: 79 lines above the marker, held by `test_the_page_is_at_most_eighty_lines_above_its_marker`; file 296 lines. Every page command runs in a scratch bed; 27 mutants killed (SSH_AUTH_SOCK added, push block deleted, each E and R command altered); owners 918 passed.
* C7b: 10 mutants killed (the phrase put back in each file, the pinned sentence reversed); on the parent commit the new entries fail for doctrine, template and checker. Owners 1398 passed.
* Gates: neutrality, redundancy, `claim_check`, `link_check` clean; `check_cairn` only the four prior `repin-build` citations (not edited).
* `_ast_attest.py verify`, read-only: output identical before and after (59 symbols red, as the plan says). `_gate_manifest.py verify --no-collect`, read-only: matches the plan's table; no new entry.
* Closure files edited: launcher template, `reanchor.sh`, runbook. Keyed files edited: `_gate_preflight.py`, `scripts/reanchor_ceremony.py`, `test_gate_preflight.py`, `test_reanchor.py`, `test_review_stance_in_shipped_files.py` (all already `FROZEN-MODIFIED`).
* Dropped nodes against `77f3e5d1`, by collection: 62 ids, 93 added. `test_gate_preflight` 4, `test_reanchor` 54 (25 grammar nodes renamed under the launcher class, 13 parity nodes replaced by one, 7 missing-field nodes moved, 5 below, 4 renamed singles), `test_repin` 1, `test_repin_ceremony` 2, `test_review_stance` 1 (label renamed). Against the stale committed manifest: 168 ids, nine of them `test_correct_pinned_digests`.
* Runbook-reading nodes dropped, by id: `test_gate_preflight::TestLoaderTrustBoundary::test_the_acquisition_command_resists_git_dir_redirection`; `TestRunbookPublicationText::{test_the_anchor_is_created_with_a_reflog_and_the_fixed_reason, test_the_authorization_ref_is_created_without_a_reflog, test_the_authorization_ref_is_retired_by_expected_old_value}`; `test_reanchor::TestTheReproducedLauncherDoesNotDriftFromTheRealOne::{test_every_reproduced_step_is_still_in_the_launcher, test_no_ceremony_loader_block_survives_in_the_runbook (kept under a new class), test_the_reproduced_order_matches_the_launchers_order, test_the_reproduction_says_it_is_not_the_authority, test_the_runbook_keeps_the_first_use_review_history}`.

**Choices the plan left open.** The pin's label was renamed to name its property (two ids). `repin` lost its filter for the artifact's ssh-add advice, which nothing prints now. The record path joined the runbook's entry in `dev/.cairn/claim-check-allow.json` (a forward reference), and a line citation in `dev/measurement/tag-pass-dispositions.md` lost its number. The runbook dropped the launcher reproduction, the rationale list and the first-use history with the old phases.

**Not verified.** The page's commands in the Maintainer's own shell and with real keys; stage 1 and stage 2 through the launcher on a real anchor; the full suite; `security_check.py`.

## Code review -- Claude Sonnet 5.5 (fresh session) -- 2026-10-27

**Reviewed commit**: 88ad4a55 (range `8a4e7508..88ad4a55`). **Verdict**: three blocking, six non-blocking; Status to `revising-code`. The Security Review of the code still follows.

**Foundations**
1. *Does it do what it claims?* Mostly. Owners re-run in a detached copy: 953 passed, 0 skipped (3.13.13). Frozen and AST deltas match the plan (AST output equals the parent's). All 16 deciding paths scan; all 11 record members and 13 values keys refuse. Three claims fail (B1 to B3).
2. *Simpler or safer build?* Same build; the fixes are small guards.
3. *What breaks it?* An escape byte in a report field (B1), a typo in the page's first commands (B2), a committed compiled file (B3).

### Blocking
**B1. Two printed fields skip the unprintable-text refusal.** `reanchor.sh:732` (hit `line`) and `:758` (signature values) print raw; an ESC byte reached the page. `test_unprintable_text_is_refused_and_nothing_is_shown` covers three fields. *Fix*: `text(str(..))` on both; parametrize over every printed field.

**B2. Not every page command is one a test runs.** The three stage-1 commands (`REANCHOR_RUNBOOK.md:29-31`) run in no node; E6 without `-f` and E7 without `-E` still pass. Here plain `readlink` prints `../Cellar/...`, not a path. *Fix*: run that block through the real launcher; give E6's links two hops; run E7 with a hostile `PYTHONPATH`.

**B3. A committed compiled file runs in the evidence stage, unflagged.** An unchecked-hash `.pyc` under `bootstrap/tests/__pycache__/` ran in place of its source through `gather_evidence` (marker written; `-B` does not stop it). `repin` refuses it (`scripts/repin.py:189`); hand ceremonies, the first included, use `raw_tree` (`_gate_preflight.py:538`) and the scan lists it nowhere. *Fix*: list tracked `.pyc`/`__pycache__` paths in the scan as "compiled", or refuse them in `raw_tree`.

### Non-blocking
* **N1.** Deleting `require_regular_file "values file"` (launcher) survives 310 nodes; a symlinked, relative or link-parent values path is then accepted. Add one parametrized node.
* **N2.** `_added_lines` is quadratic: 109 s on one 1 MiB file. Past about 20k lines, count every new line as added.
* **N3.** `rm -rf $HOME` added to `reanchor.sh` gives 0 hits. Add shell words (`rm mv cp chmod ln tee ssh-add ssh-keygen`) for `.sh` paths.
* **N4.** E7 binds a digest, not the hit list shown, and "equal by construction" (`reanchor.sh:748`) is a candidate-written claim. Say so in the table's E7 cell; reword.
* **N5.** The page calls what follows its marker "not a step", yet sends him to Phase 5, which names `refs/cairn/gate-authorization`, made by no live step. Stage 1's next-step block (`reanchor.sh:435-470`) and the driver print stage 2 without `env -i`, unlike the page.
* **N6.** `_gate_preflight.py:1677` cites a gone "Phase 0 step 1".

**Open choices** (label rename, `repin`'s lost filter, `scan_checker`, tenth dropped node, wider "decides" set, allow-list entry): fine.

**Equivalents, measured.** C6: dropping the package-absolute check passes 310 nodes; dropping it with the parent check is killed. C2: skipping `_oracle_trust.py` as deciding passes; also skipping it from the roster is killed.

**Falsification ledger** (detached copies)
* 59 launcher mutants (13 keys, grammar, packet binds): survivors package-absolute (equivalent) and values-file state (N1).
* 25 page mutants: survivors validate, run, show-report, E6, E7 `-E`, `ls-remote`.
* 16 deciding paths, each given a planted line: all found; nosec, rename, mode-only, binary, symlink, 60 hits kept or listed.
* Hostile file name and `\x1b` text: escaped in the scan; B1 fields not.
* 11 record members each damaged: all refused.

**Bounding**: ACCEPTED for the scoped record (counts re-measured); the fixes change closure bytes, so the certifying run follows them.

**Coverage.** Not run: suite, ceremony, real keys, `security_check.py`, C1 to C4 mutants. Not read whole: `test_ceremony_review_report.py`.

## Response to code review -- Claude Sonnet 5.5 (implementer, fresh session) -- 2026-10-27

Reviewed `88ad4a55`; fixes at `263ea7d2`, `30967490`, `73d2feaa`, `87a4cd31`. All nine findings are answered; none is queued or wontfix. Status stays `revising-code`: the Security Review of the code follows, and the planning session moves it.

**Blocking**
* **B1 fixed (`263ea7d2`).** I listed every printed field from the tree. Two printed raw (hit `line`, signature values); both now go through `text()`. Counts go through a new `count()`. The test puts an escape-and-bidi probe at every value and key position of a report holding every field kind (about 110 positions); the shared-roster line and the eight tool paths (a real executable in an escape-named folder) have their own probes. Related gap found in the same set: a path with an unlisted role was silently left off the page; it is now refused. Not in your finding; added because a hidden path is worse than a raw one.
* **B2 fixed (`30967490`).** One node runs the three opening commands as typed. E6's links now take two hops by relative path, so plain `readlink` fails; E7 runs against a planted `PYTHONPATH` module and a user-site `.pth` file, each with a control that loads it when `-E` or `-s` is removed.
* **B3 fixed (`73d2feaa`).** Every tracked `.pyc` or `__pycache__` file in the candidate tree, touched or not, is a hit named `compiled-file`; the reader must explain it. **The checker does not refuse it.** Reason: `raw_tree` is shared by other readers, `repin` already refuses for an ordinary ceremony, and a hit stops the Maintainer at Y3. Tested through the hand path (`raw_tree` holds the file; the report names it).

**Non-blocking**
* **N1 fixed (`87a4cd31`).** One node gives the launcher a link, a link-parent folder, a relative path, a directory and a missing file; three mutants of the check are killed.
* **N2 fixed (`73d2feaa`).** Past 10,000 lines together a file is listed ("too many lines to compare") and every new line counts as added. The brief said "list as not line-scanned"; I kept the line scanned as well, because listing alone would let padding hide a hit. 109 s became 0.27 s on the same shape (150k lines).
* **N3 judged; pattern added, page says what it misses (`73d2feaa`, `87a4cd31`).** A `shell-command` pattern matches rm mv cp chmod chown ln tee ssh-add ssh-keygen at the start of a command. Cheap, and a hit means something. Prose, brackets and backticks do not match (I first included them and saw five false hits on the real range). The page now says what the scan finds and does not.
* **N4 fixed (`87a4cd31`).** The page says the report SAYS who made the scan, that only E7 tests it, and that E7 binds the digest, not the hits; the table cell says the same.
* **N5 fixed (`87a4cd31`).** Stage 1's next-step text (both branches) and the driver print the page's `env -i` form. The header says below the marker is reference except Phase 5; Phase 5 no longer names `refs/cairn/gate-authorization`. The launcher's usage line names `--stage2` but is not a command, so I left it.
* **N6 fixed (`73d2feaa`).** The comment no longer cites a gone step.

**One commit per step, not met.** B3, N2, N3 and N6 share a function and a test file; N1, N3's page lines, N4 and N5 share files. I committed each group together, and said so in the bodies.

**Not done:** the Security Review; any ceremony; the certifying run, which covers these closure-byte changes.

## Implementation verification (code-review fixes) -- Claude Sonnet 5.5 -- 2026-10-27

Range `26a15ff1..87a4cd31` (`263ea7d2`, `30967490`, `73d2feaa`, `87a4cd31`). Interpreter `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13). **Boundary B mode**: full; **Certified by**: pending. No push, suite, ceremony, key access or `security_check.py`; `CAIRN_FULL_SUITE` never set. The fixes change closure bytes (`reanchor.sh`, the runbook) and keyed files (`_gate_preflight.py`, `scripts/reanchor_ceremony.py`, `test_reanchor.py`), so the single certifying run after the ceremony covers them.

* Tree: clean apart from two untracked paths that are not mine. Skipped nodes in any run: 0.
* Owners, run in a detached copy holding HEAD plus the changed files: `test_reanchor` 217 and `test_repin_ceremony` 105 passed; `test_gate_preflight`, `test_repin`, driver disclosures, `test_ceremony_review_report` (52), `test_security_lint` (Bandit node ran), `test_security_check`, `test_gate_reanchor` 635 passed.
* Each fix's new nodes fail on the parent: the unprintable-text node (B1), the E6 and E7 nodes (B2, as mutants), the compiled and bound nodes (B3, N2).
* Mutants, each in a fresh detached copy beside a green control; a skipped node counted as a survivor:
  * B1: 11 killed, 1 equivalent, measured: dropping one `count()` call leaves `%d`, which refuses a string; `%d` to `%s` on that line is killed.
  * B2: 8 killed (E6 without `-f`, E7 without `-E`, without `-s`, E7 from HEAD, and four typos in the opening commands).
  * B3, N2, N3: 15 killed (each compiled rule, the count, the pattern name, the bound, the listing, each shell alternative).
  * N1: 3 killed. N4, N5, N3's page lines: 12 killed (wording, the `env -i` form, the home, the driver, the runbook sentences).
  * Total: 49 killed, 1 equivalent, 0 survived.
* Measured: 150k near-identical lines, 109 s per the review, 0.27 s now. Real anchor to HEAD: 73 hits, 0.2 s, one `shell-command`, no compiled file tracked.
* The runbook page is 79 of 80 lines above its marker, held by `test_the_page_is_at_most_eighty_lines_above_its_marker`; the file is 294 lines.
* `_ast_attest.py verify`, read-only: output identical to the parent's (59 symbols red). `_gate_manifest.py verify --no-collect`, read-only: no new entry; `_gate_preflight.py` and `test_gate_preflight.py` were already `FROZEN-MODIFIED`.
* Gates: neutrality and redundancy clean; `claim_check` and `link_check` on the runbook clean; `check_cairn` only the four prior `repin-build` citations (not edited).
* Frozen or closure files edited: closure `reanchor.sh` and the runbook; keyed `_gate_preflight.py`, `scripts/reanchor_ceremony.py`, `test_reanchor.py`. Not edited: the launcher template, `_scaffold`, the AST baseline, the gate manifest, the anchor, `PLANNING.md`, `CHANGELOG.md`.

**Not verified.** The page's commands in the Maintainer's own shell or with real keys; the full suite; `security_check.py`; a scan over a candidate that really carries a compiled file through `gather_evidence`.
