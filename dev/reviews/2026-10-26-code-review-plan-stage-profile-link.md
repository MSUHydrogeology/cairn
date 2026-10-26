# Code review -- `upgrade --plan` and `--stage` refuse a linked `profile.yml` -- Claude Sonnet 5.5 (fresh session) -- 2026-10-26

**Model**: claude-sonnet-5-5
**Tier**: usual (code stage; a fresh session, not the implementer)
**Reviewed commits**: `f247980b` (10 new tests, red by design), `63eb8a1a` (the fix: 8 lines in `cmd_upgrade`, `bootstrap/_scaffold/upgrade.py`), `7667b479` (prose: `bootstrap/UPGRADE.md`, `bootstrap/_scaffold/SECURITY_MUTATIONS.md`, `CHANGELOG.md`). Read against `f0753b59` and `6f25d630`; their `upgrade.py` is the same file (diff of 0 lines).
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13, `PYTHONDONTWRITEBYTECODE=1`. No full suite, no `CAIRN_FULL_SUITE`.
**Called by**: none (the usual review; not an External read). **Not reopened**: the Decision.
**Where things ran**: `git archive` extractions of `f0753b59`, `6f25d630`, `63eb8a1a`, `7667b479` and four mutated copies, in one scratch folder, removed at the end. The only writes to the shared tree are the intent claim and this file. I did not open either adopter repository.

**Verdict: no blocking findings.** The fix does what it claims, in the right place, with nothing else changed. Three findings follow; none stops it. The one that needs a decision is F1: `--adopt-module` and `--adopt-collisions` still read through a link, and the guard for them is four lines.

Terms. A **link** is a symbolic link. A **mutant** is one deliberate break made in a copy to see whether any test notices: **killed** if a test fails, **survived** if none does, **equivalent** if the break changes no behaviour. To see reads I ran the command under a Python audit hook that logs every `open()` of `profile.yml` or of the outside folder; on the parent it logs the read, so the instrument can see one.

## Foundations

1. **Does it really do what it claims?** Yes. Over six link shapes, `--plan` and `--stage` exit 2 with the two-line refusal, print nothing on stdout, open nothing behind the link, and change nothing in the project or outside it; the parent exits 0, and `--stage` also writes its review area. Evidence: ledger P1-P7.
2. **Is there a simpler or safer build?** This is the simplest one: one existing guard call at the single point `--plan` and `--stage` share, no new symbol. One safer addition exists (F1). Evidence: P18 (68 symbols before and after, only `cmd_upgrade` changed), P21.
3. **What input or run breaks it?** None I found breaks the repaired paths. What still reads through a link is outside the repair: `--adopt-module` and `--adopt-collisions`. Evidence: P10, P11.

## Rulings on the five points

1. **The guard sits before any read through the link: yes.** Link to an outside file, dangling, link to an inside file, link to a folder, linked `dev/.cairn`, linked lockfile: `--plan` and `--stage` all exit 2, link left in place, no `open()` of the target (P1-P6). The last two are refused by the lockfile guard first, so their message names the lockfile.
2. **The unlinked paths are unchanged: yes.** Regular, absent and incomplete-regular profile, each for `--plan` and `--stage`, give byte-identical output, exit code and set of changed files on the parent and the fix, with paths normalized (6 pairs, P8).
3. **The prose is true; one fact is missing, and one correction is right.** `--finalize` opens nothing and exits 0 (P9). `--adopt-module python-security` over a link puts the linked file's `python_package` into the lockfile; the same run over a regular file gives the same result (P10). `--adopt-collisions` opens the profile through the link (P11). **"Writes it when it is absent" is correct:** `_self_heal_profile_config` calls the guard first, whatever the file holds, then returns if the file exists, so it writes only an absent file. The refusal measured earlier on a linked incomplete profile was the guard firing before that test; an incomplete regular profile is left unchanged and an absent one is written (P12). The missing fact is in F1.
4. **Tests and mutants: the net catches what it claims.** The red check on `f0753b59` plus the new file gives 6 failed, 4 passed (P13). Three mutants of mine, beside an unmutated control of 10 passed: guard on `--plan` only, 3 killed; guard on `--stage` only, 3 killed; guard after the read, 4 killed and 2 equivalent (P14-P16).
5. **Scope is clean.** `cmd_upgrade` is the only changed symbol in `upgrade.py`, no symbol added, digest `e336d4f8c828dc40` to `aed70ad254a35e17` as stated (P18). The AST pair is red on both the parent and the fix with the same 12 CHANGED and 5 NEW symbols. None of the five touched files is among the 195 `frozen_files` keys (P19). The `63eb8a1a` body carries mode `full`, interpreter, `Certified by: pending`; it is 31 lines with blanks (26 without), one over the 15-30 target; no action.

## Findings

**F1 (non-blocking; recommend fixing now): `--adopt-module` and `--adopt-collisions` still read through a link, and show what they read.** Over a link to an outside file, `--adopt-collisions` printed `age='OUTSIDESECRETVALUE'` from that file in its warning, and `--adopt-module` wrote the file's token value into the lockfile (P10, P11). Neither writes outside the project, and the file must look like a profile, so the exposure is small. But it is the same rule the repair enforces, in the same function. The fix is simple: in `cmd_upgrade`, before `if args.adopt_module:`, add `if args.adopt_module or args.adopt_collisions:` around the same `_refuse_if_linked(target, _PROFILE_REL, ...)` call (4 lines). On a copy of `7667b479` it makes both actions exit 2 with the same message and open nothing, the regular-profile run is unchanged, and 253 owner tests pass (P21). Finishing it takes about 4 test nodes (two actions, two link shapes, controls) and deleting the three "still read through a link" sentences in `UPGRADE.md`, `SECURITY_MUTATIONS.md` and `CHANGELOG.md`. It is outside this review's three commits, so it needs its own one fresh look. Under the Maintainer's rule it is simple, so do it now rather than queue it. If it is queued, the prose should also say that both actions print lines from the linked file.

**F2 (non-blocking; a wording point for the planning session): the `Defect fix:` line cites a promise the parent's `UPGRADE.md` did not make for these two actions.** The parent text said `--plan` and `--stage` read the profile through a link and exit 0, and its heading listed only `--apply` and `--init-lock` as refusing. The nearest standing text is "the rule is stricter on purpose and the same for every link", and the `.gitignore` bullet. So this repair changes documented behaviour; it does not restore a promise. If the Maintainer asked for it, say so in the handoff as the authority. I would not amend the commits. I did not check chat history for the request.

**F3 (info; no action): the profile guard's "or above it" cannot be seen on the command line.** A link above `profile.yml` is also above the lockfile, so the lockfile guard answers first (P5). The `SECURITY_MUTATIONS.md` row is still true; no test could separate the two, and none is needed.

## Falsification ledger

| # | Probe | Result |
|---|---|---|
| P1 | Fix, `--plan` and `--stage`, link to an outside file holding unparseable text | exit 2, stdout 0 bytes, link intact, project and outside unchanged, no `open()` of the target |
| P2 | Same, dangling absolute link | exit 2, same |
| P3 | Same, link to a file inside the project | exit 2, same |
| P4 | Same, link to a folder | exit 2, same (parent: exit 0, silent) |
| P5 | Same, `dev/.cairn` a link to a copy outside | exit 2, lockfile refusal, nothing changed |
| P6 | Same, lockfile a link | exit 2, lockfile refusal, nothing changed |
| P7 | Control: parent, same link to outside file | `--plan` exit 0 and `open()` of the profile logged; `--stage` exit 0 and wrote `.gitignore` and the review area |
| P8 | Fix vs parent, regular, absent, incomplete-regular, each `--plan` and `--stage` | 6 of 6 pairs byte-identical |
| P9 | Fix, `--finalize` over a link (incomplete and complete content) | exit 0, no `open()`, nothing changed |
| P10 | Fix, `--adopt-module python-security` over a link vs a regular file vs absent | link and regular: exit 0, `OUTSIDEPKG` in lockfile, `open()` logged; absent: exit 2, token required |
| P11 | Fix, `--adopt-collisions` over a link | `open()` logged; warning printed the linked file's `age` value |
| P12 | Fix, `--apply` over complete link, incomplete link, dangling link, incomplete regular, absent | link cases exit 2 (self-heal refusal); incomplete regular unchanged; absent written |
| P13 | `f0753b59` plus `f247980b`'s test file, the 10 plan/stage nodes | 6 failed (exit 0 not 2), 4 passed |
| P14 | Mutant A: guard on `--plan` only | 3 killed (the `--stage` link nodes); control 10 passed |
| P15 | Mutant B: guard on `--stage` only | 3 killed (the `--plan` link nodes) |
| P16 | Mutant C: guard after `_compute_upgrade` | 4 killed; 2 dangling nodes survived, equivalent: no `open()`, output and changes identical to the fix, and mutant C on the outside-file link does open |
| P17 | `7667b479` archive: the six files that read the changed prose or test it | 860 passed, 1 failed (`test_a_real_saved_commit_still_gets_its_behind_by_count` needs a git checkout; fails the same on the `6f25d630` archive) |
| P18 | Symbol digests, `upgrade.py`, parent vs fix; `test_ast_attest.py` on both | one changed symbol, none added; 2 failed on both, same 12 CHANGED and 5 NEW |
| P19 | The three commits' files against `frozen_files` | 0 of 5 are frozen |
| P20 | `claim_check.py` on the three prose files; neutrality gate | OK on all three; `fail=0` |
| P21 | Mutant D: adopt guard (F1) on a copy of `7667b479`, then `test_upgrade_refuses_hostile_project_data.py`, the sibling containment file, `test_upgrade_module_additions.py` | adopt on a link and a dangling link: exit 2, no `open()`; regular profile unchanged; 253 passed, 2 failed (both need a git checkout; one fails the same on the unmutated archive) |

**Bounding**: ACCEPTED. The record is scoped, mode `full`, pending, which is the rule's reading for the scaffold engine. I challenged the mapped test (killed by A, B, C), the stated survivors (equivalent by measurement), and the claim that the AST pair is red as on the parent (same set on both). I did not reproduce the `2344 passed` figure; the certifying run covers it.

**Coverage.** Not covered: the full suite and the `2344` count; a link swapped in between the guard and the read (`--stage` reads the profile twice, once in `_compute_upgrade` and once itself, behind one check); `--to <ref>` with a link; hard links and special files; non-macOS filesystems; the one test that needs a git checkout, in a real checkout. Security-flavoured, for the planning session: F1 (reads and prints through the link; nothing written outside the project in any probe) and the read-twice window. No Security Review was mine to run.
