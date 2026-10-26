# Code review -- second look at the session-binding revision -- Claude Sonnet 5.5 (fresh session) -- 2026-10-26

**Model**: claude-sonnet-5-5
**Tier**: usual (one short second look at a code revision; a fresh session, not the revision's author and not the first fix's reviewer)
**Reviewed commits**: `62508ef0` (code and tests: `tools/session.py`, its twin `templates/skills/_lib/session.py`, `bootstrap/tests/test_session_binding_gate_and_printing_hold.py`) and `9f61e8c8` (prose: `bootstrap/SAFETY.md`, one line of `dev/NEXT_SESSION.md`), read against the parent `bad52be1`.
**Answers**: `dev/reviews/2026-10-26-code-review-session-write-findings.md` (commit `3bcee549`), findings F1, F2, F4, F6 (code) and F3, F7(c) (prose).
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13), macOS on APFS. The default volume ignores letter case and Unicode form (measured below).
**Where things ran**: two detached worktrees in fresh folders (the revision; the parent with only the new test file copied in) and one throwaway case-sensitive disk image. All removed.
**Called by**: none. **Not reopened**: the Decision. This is not a Security Review.
**Safety**: resolver level only. Nothing a binding names was run; the stand-in programs are two-line shell files that are only read and `stat`ed. `CAIRN_FULL_SUITE` was never set and I ran no full suite.

**Verdict**: NO BLOCKING FINDINGS -- 0 blocking, 2 non-blocking, 1 informational.

**In plain terms.** The revision does what it says. The three changed meanings are the ones the commit body states, and each is acceptable. The order of the checks did not change. The one mutant that survived (N07) is equivalent: I measured it. I found one gap in the tests (a name that only starts like the project's name is not pinned) and one sentence the safety note should add.

## Foundations

1. **Does it really do what it claims?** Yes. 36 of 36 new tests pass on the revision; 11 of them fail on the parent by wrong results. The binding gate refuses every tracked or fold-equal interpreter I tried and trusts every untracked one -- `bootstrap/tests/test_session_binding_gate_and_printing_hold.py`; rulings 1 and 5.
2. **Best alternative.** None simpler. The revision is 48 changed lines per twin and adds one constant and one helper. Folding both sides of the comparison is the smallest build that keeps the gate on case-insensitive disks -- `templates/skills/_lib/session.py:836-846, 893-904`.
3. **What would show it wrong.** A tracked interpreter the new test treats as untracked, or a binding trusted on a disk that cannot answer. I tried 100000 random path pairs, three disks and five inode pairings and found neither -- see the falsification ledger (rulings 1 to 3).

## Rulings on the five points

**1a. The folded in-project test: correct, and stricter only.** Wrong answers, by direction. *Said "inside the project" for a safe program:* the binding is refused, the run uses the current interpreter, one warning. *Said "outside" for a tracked program:* the binding is trusted and a checkout can swap the program under it. That second kind is the harmful one. The folded test cannot produce it where the parent's exact test would not: the folded prefix matches whenever the exact one does (100000 random project and interpreter pairs, seed 1, characters chosen for the awkward folds -- sharp s, long s, Kelvin sign, dotted capital I, combining marks: 0 pairs where the parent looked the program up and the revision did not; 21 where only the revision did). What I measured on this Mac:
- Other-case spelling of the project folder, index tracks the interpreter: refused. The same spelling with an untracked interpreter: trusted (control).
- Composed project folder name, binding spelled decomposed: refused. This volume does treat the two spellings as one folder (measured), so the test had something to catch.
- Two real folders `Proj` and `proj` on a case-sensitive disk image (`samefile` is false): project `Proj` tracks `env/bin/python3`, the binding names `proj/env/bin/python3`, a different, untracked file. The revision refuses it, and its warning says "inside the project", which is not true. By reading, the parent trusts it. This is the cost of the stricter fold: a wrong refusal on a rare disk layout. I recommend no change; fail-closed is the right side to err on.
- Does it require the separator? Yes, in the code (`:839, :843`). The prefix ends in "/", so `Proj-other`, `PROJ2`, `proj2` and `Proj.d` next to `Proj` are all trusted. But no test pins this -- finding S1.

**1b. Inode 0 skips the identity checks: acceptable.** On a disk that reports 0 for every file, the parent compared (device, 0) with (device, 0), so every comparison matched. A project with any tracked file three folders deep, or any one- or two-part submodule entry, had its binding refused by a gate that could never be satisfied there. The revision keeps the name checks only. What is lost: a spelling that the disk treats as one name but the fold does not, on a disk that gives no inode numbers. I could not name which real disks report 0 (not measured; the code comment says "some disks"); I assume network or FUSE mounts and some FAT-type volumes, and that is an assumption. All three stored identities are covered: the binding's own (three-part file), `dev` (one-part submodule entry) and `dev/.cairn` (two-part) -- the three `test_a_disk_that_reports_inode_zero_gives_no_identity_to_match` cases all fail on the parent (wrong refusal) and pass now. The safety note does not yet say this -- finding S2.

**1c. A failed `stat` has its own words: the decision is unchanged.** The parent returned `_BINDING_UNVERIFIED`; the revision returns `_BINDING_DISK_UNANSWERED` (`:835`). Both are text, and `_resolve_interpreter` turns any text into `(sys.executable, "fallback-untrusted")` plus one warning; `_resolve_interpreter` is byte-identical in the two commits (empty diff). `_BINDING_UNVERIFIED` is untouched and the three git-failure returns still use it (`:856, :858, :866`). The four frozen assertions of "could not ask git" (`test_session_binding_untracked.py` lines 228, 320, 594, 630) all fail git itself (exit 128, git missing, timeout, unreadable output); none reaches a failed `stat`, and the file passes (84 passed with the new file).

**2. The trailing "/" strip: right, and not an opening.** The text of a project path ends in "/" only when the project is the filesystem root (or a Windows drive root, `C:/`). There, without the strip the prefix is "//", nothing matches, and the lookup is silently skipped. I computed it: with the strip the prefix is "/" and "/bin/python3" matches; without it, it does not. For every other path `rstrip` removes nothing. It goes slightly past the finding's recipe (`folded_root + "/"`), inside the same two lines, with no new name. It is untested: the resolver cannot be run with root "/" because the state folder would be `/dev/.cairn`. Informational only.

**3. N07: equivalent.** See the ledger.

**4. Order of the binding checks: unchanged.** `_resolve_interpreter`: empty diff against the parent. `_binding_untrusted`: link check, three `stat`s, interpreter target, the question to git, then in the loop the same five tests in the same order (folded name, submodule holding the binding, three-part identity, one- and two-part submodule identity, interpreter). The returns are at the same sites; one of them (the `stat` failure) returns the new constant. None added, moved or removed. One small shift: the interpreter fold now sits outside the `try`. It cannot raise: a lone surrogate went through `casefold` and `normalize` unchanged.

**5. Twins and tests.** `git rev-parse` gives one blob (`8039d192`) for both files at `62508ef0`, and `cmp` of the two files in the tree is clean. The new file run against the parent's `session.py`: 11 failed, 25 passed. All 11 are assertion failures on a wrong result; none is an import or name error (I read each failure line). The count the author gave is right. **`9f61e8c8` SAFETY.md paragraph**: every claim I could check is supported -- the program also runs at `session-end --handoff` and through the intent tool's name lookup (`session.py:426, :1562, :2009`; `CAIRN_AGENT` and `CAIRN_SESSION` are read at `:466, :502`); the binding needs only an executable file (the `_resolve_interpreter` docstring says so); the new tests skip on Windows (`pytestmark`, line 42 of the new file). I did not verify "never been run on HFS+" -- it is a statement about history.

## Falsification ledger

| What I tried | Result |
|---|---|
| New test file on `62508ef0` | 36 passed |
| New test file on the parent's `session.py` | 11 failed (wrong results), 25 passed |
| Owner set: 28 test files found by searching for what reads `session.py`, `_lib`, `local-env`, `session-start` (not the author's 25; his list is not in the commit), unmutated, twice | 1427 passed, 0 failed, no skips, shuffle seed 0, about 2m25 each |
| Folded prefix vs the parent's `relative_to`, 100000 random pairs | 0 lost, 21 gained |
| Case, Unicode form, collision, sibling-name probes (above) | as stated in 1a |
| Boundary mutant: drop the boundary but keep the lookup (prefix without "/", tail left-stripped) | probe: wrong refusal in the sibling case; repo binding tests: 84 passed -- survives (S1) |
| Recommended S1 test, written and run | passes on `62508ef0`, fails on the boundary mutant |

## N07 ledger

N07 moves the inode-0 guard in `_has_identity` from the stored identity to the looked-up file's identity (both twins).
- **Control, unmutated**: binding test files (new file plus `test_session_binding_untracked.py`) 84 passed; 28-file set 1427 passed.
- **N07**: 84 passed; 1427 passed. It survives the repo tests.
- **Behaviour probe through `_binding_untrusted`** (stand-in files, `stat` patched to report chosen inode numbers, 3 lookup kinds x 5 pairings of stored and looked-up inode: (0,0), (0,7), (7,0), (7,7), (7,8)): the original and N07 give the same answer in all 15 cells. Only (7,7) refuses, in all three kinds, so the probe could match.
- **Recovery site**: the tuple comparison `_identity(...) == identity` is what rejects a stored 0 against a nonzero file, and a nonzero stored value against a 0. Mutated so a stored 0 acts as a wildcard (N07b): the probe differs in 3 cells, (0,7) in each kind. Control with the guard deleted entirely: the probe differs in 3 cells, (0,0), and the repo tests fail 3 (the inode-zero tests), so the instrument can see a break.
- **Ruling: EQUIVALENT** (measured). One gap: N07b survives the repo tests (84 passed), because no test pairs a stored inode of 0 with a nonzero looked-up inode. In the shipped code the guard covers that pairing, so nothing is exposed; no action.

## Findings of my own

**S1 (non-blocking, low): no test pins the project-folder boundary.** The parent got the boundary free from `Path.relative_to`; the revision rebuilt it with the "/" and nothing fails if it is dropped (the boundary mutant above passes all 84 tests; it makes a wrong refusal, not a wrong trust). *Recommended fix:* one test beside `test_an_interpreter_outside_the_project_is_not_looked_up` -- project `project`, program in the sibling `project2/env/bin/python3`, listing `100755 2/env/bin/python3`, expect `_binding_untrusted(root, cfg, program) is None`. I ran this exact test: it passes on the revision and fails on the mutant. Test bytes change, so the next certifying run covers it.

**S2 (non-blocking, low): the safety note leaves out the inode-0 case.** `bootstrap/SAFETY.md`, the paragraph `9f61e8c8` edited, says what is shown "for the disks tried" but not that on a disk reporting no inode numbers only the folded-name checks run. *Recommended fix:* one clause saying so. Prose; the commit body says no test reads those bytes (I did not re-search).

**S3 (informational): the printed `git rm <entry>` cannot be pasted when the name holds a non-printing character.** The entry is printed encoded (`alias\u3164.json`), so a shell will not turn it back into the real name. The command fails safely (git finds no match) and the binding stays refused; the line "git tracks it as ..." still shows the name. No fix needed.

## Bounding

**Bounding**: ACCEPTED. The author's record is `full` mode with `Certified by: pending`, not a bounded one; I challenged it by reproducing the scoped runs on the revision's bytes (36, 84 and 1427 passed, no skip, xfail or xpass) and by the mutants above. Nothing here invalidates it. The two F1 case tests skip on a case-sensitive disk; they ran here because this disk ignores case, so a run on a case-sensitive disk will execute fewer of them.

## Coverage -- what I did not check

I did not run the full suite or a certifying run (by rule). I did not run Windows or an HFS+ volume (none here), so equivalences beyond the Unicode canonical-caseless fold (HFS+'s own table, NTFS short names) are untested. I did not find out which real disks report inode 0. I did not run the parent in the case-sensitive collision (read, not run). I did not run root "/" through the resolver (needs `/dev/.cairn`). I did not check a project that sits in a subfolder of a larger repository (outside this revision). I did not see the author's list of 17 mutants, so I cannot say which 16 were killed. F3, F5 and F7 in full are outside this look.
