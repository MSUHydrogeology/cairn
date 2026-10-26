<!-- Four deliberate backward references: files this sweep deleted, cited here
     because the review is about what moved out of them. Each is marked rather
     than left to assert. -->


# Code review (Internal) — C1, the session kernel — Claude Opus 5 — 2026-08-27

**Obligation**: Internal code review, C1 chunk group.
**Reviewed range**: `ea3d649`, `82671c7`, `ea455ca`, `2a93482`, `0701ee3`.
**Baseline compared against**: `8c83c0c` (`tools/lifecycle.py`, pre-extraction).
**Interpreter**: Python 3.13.13 at `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
`PYTHONDONTWRITEBYTECODE=1`. Platform: darwin. All runs performed in throwaway
`git worktree` checkouts, never in the live tree (three reviews are concurrent).

**Verdict**: BLOCK — 2 blocking, 6 non-blocking.

The extraction itself is good work and I want to say so before the findings.
The trust root moved **byte-for-byte**, the twins are byte-identical, the
encoder claim holds at HEAD, and the trust root's own falsifier passes
independently from its new home. What blocks is not the code: it is that C1
moved a trust root out from under the install-integrity anchor without anyone
recording it, and that C1's own falsifiable acceptance criterion is not
satisfied as written while the record reads as though it were.

## What I verified as sound, before the findings

Stated up front so the blocking findings are read at their real size.

* **The extraction is pure motion where it claims to be.** An AST-level
  symbol-by-symbol comparison of `8c83c0c:tools/lifecycle.py` against
  `ea3d649:tools/session.py` gives **59 common top-level symbols, 56 of them
  byte-identical**. The three that differ are exactly the three the commit
  message declares: `_safe_field` (docstring rewrite plus the direct
  `encode_display` call), `build_parser` (the four monitoring subcommands
  dropped), and `main` (the `MonitoringIncomplete` handler dropped). Nothing
  else moved silently.
* **The trust root is unmodified.** `_resolve_interpreter`,
  `_has_symlink_component`, `_probe_interpreter` and `_warn_stale_once` are
  byte-identical to the pre-extraction file, both at `ea3d649` and at HEAD.
* **The encoder is unmodified.** `encode_display`, `_escape_code_point`,
  `_display_unsafe_code_point`, `_DISPLAY_UNSAFE_RANGES`,
  `_DISPLAY_UNSAFE_FLOOR`, `_DISPLAY_SYNTAX_CHARS`, `_BOARD_FIELD_DELIMITER`
  and `_BOARD_ROW_DELIMITER` are byte-identical to their pre-extraction home in
  `8c83c0c:tools/lifecycle_planner.py`.
* **The twins are byte-identical.** `cmp tools/session.py
  templates/skills/_lib/session.py` → identical; both md5
  `23b162d4dfbc29e634ca8ebba10d7a5d`, 1,523 lines each. Verified, not assumed.
* **`encode_display` is the single encoder at HEAD.** A tree-wide grep outside
  `dev/` finds it defined only in the two twins, consumed by `_safe_field`
  (`tools/session.py:275`) and by `tools/board.py:56`, which loads the kernel
  rather than carrying a table. `scripts/content_scan.py` holds its own ranges,
  but it is a detector, and the duplication is documented as deliberate.
* **No dangling references.** A static walk of `tools/session.py` for
  module-private `Name` loads with no binding returns only `__file__`.
  `MonitoringIncomplete`, `_vocabulary`, `_validated_planner_path`,
  `VocabularyUnavailable`, `lifecycle_planner`, `_EVENT_KINDS`,
  `cmd_review_brief` and `cmd_pilot*` are all absent from the source.
* **The kernel runs.** `python tools/session.py session-end --dry-run` in a
  worktree at HEAD exits 0 and produces the expected orientation output.
* **C1's security falsifier passes from the new home.** I constructed six
  bindings against `_resolve_interpreter` in a worktree at HEAD, deliberately
  avoiding `/etc` and `/tmp` (see finding 4). Output:

  ```
  non-executable file  -> REFUSED: "interpreter" is not an executable file
  a real directory     -> REFUSED: "interpreter" is not an executable file
  symlinked leaf       -> REFUSED: must not be reached through a symlink
  symlinked parent     -> REFUSED: must not be reached through a symlink
  parent-traversal     -> REFUSED: must not contain a parent-traversal (..) segment
  valid executable     -> ACCEPTED ('/private/tmp/.../bin2/python', 'local-env.json')
  ```

  This is the acceptance criterion's named falsifier and it is satisfied.

---

## 1 — BLOCKING — the relocated trust root is not covered by the install lockfile, and C8's measurement of that gap is wrong

**What is wrong.** Before C1, the interpreter trust root lived in
`tools/lifecycle.py`, which carried a `verbatim: true` record in
`dev/.cairn/cairn-lock.yml`. `bootstrap/verify_integrity.py` — described in
`bootstrap/_scaffold/lockfile.py:3` as "the second trust anchor" — hashes every
such record. After C1 the trust root lives in `tools/session.py`, which has
**no record at all**. The tool that exists so a cold adopter can decide whether
to trust the shipped scripts no longer looks at the file holding the executable
trust root. It does not report this as a gap; a file with no record is simply
invisible to it.

**Evidence.**

```
$ python - <<'EOF'   # parse dev/.cairn/cairn-lock.yml, compare each record to disk
...
records: 90
session.py recorded? False
board.py   recorded? False
MISSING dst (19): ... ('tools/lifecycle.py', True), ('tools/lifecycle_planner.py', True),
                  ('tools/lifecycle_metrics.py', True), 9x tools/_lifecycle_metrics/*.py (True),
                  scripts/foldback_export_scan.py (True), scripts/foldback_suggest.py (True),
                  + 5 non-verbatim dev/ docs
CHANGED verbatim: []
EOF
```

```
$ python bootstrap/verify_integrity.py --target .
  ... missing: tools/lifecycle.py
  ... missing: tools/lifecycle_planner.py
  ... (14 verbatim records in total naming files that no longer exist)
The on-disk tree no longer matches its recorded install. Do not trust the
shipped scripts until this is resolved.
```

`tools/session.py` appears nowhere in that output — not as missing, not as
verified. It is not covered.

**The second half, which is why this blocks rather than waits.** The plan's C8
block (`dev/plans/subtraction-sweep.md:976` onward) says:

> **(a) Three verbatim lockfile records disagree with disk.** The raw count of
> records diverging is 19, and **that number is misleading**: 16 are substituted
> or living-state files an adopter is *expected* to edit. Restricted to
> `verbatim` records, where byte-identity is the contract, it is **three**.

Measured at HEAD, that is not the shape of the divergence. The three
hash-mismatched verbatim records it names (`scripts/claim_check.py`,
`tools/evolution_infer.py`, `tools/prune_reflections.py`) are **already
corrected** — `610f521` applied the Maintainer's three digests, and my
recomputation finds zero verbatim hash mismatches. What actually remains is a
different problem the block never counted: **14 verbatim records naming files
that no longer exist**, and **two new shipped verbatim files with no record**
(`tools/session.py`, `tools/board.py`). C8 has not run. It is about to run
against a measurement that describes the wrong 19 and misses the trust root
entirely.

**Why no test caught it.** Every lockfile test I could find
(`test_verify_integrity.py`, `test_skills_install.py`, `test_lockfile_provenance.py`,
`test_module_merge_lockfile.py`) operates on a freshly scaffolded temp target,
where the lockfile is written from `_SKILLS_MAPPINGS` and therefore always
agrees. Nothing asserts that **Cairn's own** tracked
`dev/.cairn/cairn-lock.yml` matches Cairn's own tree. A fresh adopter is fine;
the dogfood repo is the one that drifts, silently, which is the worse direction
because that is the tree everything else is measured in.

**What would fix it.** Two things, and neither is a code change to C1:

1. Correct the plan's C8 block with the measured shape above, so the
   Maintainer's regeneration covers **14 stale verbatim records plus two
   unrecorded verbatim files**, not three digests. This is the actionable half
   and it is why the finding blocks: C8 is next.
2. Record, in C1's own row or in the C8 block, that the interpreter trust root
   moved from a lockfile-covered file to an uncovered one, so the fact does not
   have to be rediscovered. `AGENTS.md` already documents
   `dev/.cairn/local-env.json` as "lockfile-uncovered"; it does not say the same
   of the reader, and until C1 the reader was covered.

I am not asking the implementer to hand-edit the lockfile. `[TRU-1]` says there
is no regeneration command, which is precisely why the measurement being right
matters more than usual.

---

## 2 — BLOCKING — C1's own acceptance criterion ("repointed **in C1**, not C6") is not satisfied, and no deviation was declared

**What is wrong.** The plan states the criterion twice, in the imperative, and
explains why the ordering is the whole point:

> **Every `skipif`-guarded loader of `lifecycle.py` is repointed in C1, not C6.**
> That ordering is what converts a silent skip into a real test.
> — `dev/plans/subtraction-sweep.md:244`

> * **C1** — every `skipif`-guarded loader of `lifecycle.py` is repointed at the
>   kernel **in C1**, and each such test is shown *failing* against a tree without
>   the kernel before it is called repointed.
>   — `dev/plans/subtraction-sweep.md:799`

At C1's final commit `0701ee3`, five test files still loaded `lifecycle.py`
behind a guard. Two of them are not incidental:
`bootstrap/tests/test_lifecycle_cli.py` and
`bootstrap/tests/test_lifecycle_failsafe.py`, which C6's own commit message
describes as
"1,222 lines testing the SURVIVING kernel: handoff locking, marker gating,
dead-holder lease reclamation, reflection scaffolding, **interpreter
resolution**." They are the bulk of the trust root's coverage. They were
repointed in `bfe6bbf` — **the same commit that deleted the file**, which is
exactly the ordering the criterion was written to forbid.

**Evidence.**

```
$ cd <worktree at 0701ee3>
$ grep -rln '_lib" / "lifecycle.py"|tools/lifecycle.py|"lifecycle.py"' bootstrap/tests/
bootstrap/tests/test_lifecycle_brief.py
bootstrap/tests/test_lifecycle_cli.py
bootstrap/tests/test_lifecycle_contract.py
bootstrap/tests/test_lifecycle_failsafe.py
bootstrap/tests/test_lifecycle_vocabulary.py
bootstrap/tests/test_pilot_evidence.py
bootstrap/tests/test_security_stack.py
bootstrap/tests/test_skills_security.py
```

`git log --oneline -- bootstrap/tests/test_session_failsafe.py` shows the
rename and repoint landing at `bfe6bbf` (C6), not in C1's range.

**The mitigating half, stated fairly.** C6 did find them, and said so loudly in
its own message ("The manifest was wrong in the expensive direction, twice
more"), and 52 of 54 passed immediately on repointing. The hazard did not
materialize. But it did not materialize because the C6 implementer went looking
— not because C1's fence fired. A fence that depends on the next chunk's
diligence is not a fence, and the plan says so in its own words.

**The evidence half was also never produced.** "Each such test is shown
*failing* against a tree without the kernel" appears in no C1 commit message
and in no plan record. `ea455ca` records a different mutation check (reverting
the scaffold string reddens the first-session assertion), which is good work
but is not this. I ran the missing demonstration myself, at `0701ee3`, and it
**passes** — so the property holds for the files C1 did repoint:

```
$ <worktree at 0701ee3>  # baseline, all eight touched files
82 passed in 4.36s

$ mv tools/session.py templates/skills/_lib/session.py aside; re-run
ERROR collecting bootstrap/tests/test_skills_self_heal.py  - FileNotFoundError
ERROR collecting bootstrap/tests/test_skills_security.py   - FileNotFoundError
ERROR collecting bootstrap/tests/test_session_kernel.py    - FileNotFoundError
8 failed, 28 passed        # the remaining five files
```

Red and erroring, not skipped. That is the right answer. It should have been in
the record.

**What would fix it.** An appended note in the plan that (a) names the two
files repointed in C6 rather than C1, (b) records the demonstration above or an
equivalent one, and (c) either declares the ordering change as a deviation with
the Maintainer's allowance or argues on the record why it does not need one.
As it stands the acceptance criteria section reads as satisfied and it is not.

---

## 3 — non-blocking — there is no Boundary B record for C1

**What is wrong.** `dev/plans/subtraction-sweep.md:830` says: "Run after the
final implementation commit of **each of C1, C5, C6, C7**". The plan contains
exactly one `## Implementation verification` heading, at line 894, tested at
`b1e655d` — C7's final commit. C1, C5 and C6 have none.

**Evidence.** `grep -n "^## Implementation verification" dev/plans/subtraction-sweep.md`
returns a single line: `894`.

**Why it is non-blocking.** The one record that exists is `full` mode and sits
downstream of C1, so C1's code was in fact exercised by a full canonical run.
What is lost is the per-chunk reconciliation the plan demanded and argued for
at length — "A falling test count is expected and must be accounted for, not
observed", and "Reconcile the SKIP count too, and reconcile it first." The C1
delta was never reconciled against its own chunk, so nobody can now say from
the record what C1 alone added or moved.

**What would fix it.** Either append a retrospective C1 record reconciling its
delta, or amend the Verification section (append-only) to say the sweep
consolidated to a single terminal Boundary B and why. Do not leave the contract
saying four and the record holding one.

---

## 4 — non-blocking — `test_session_kernel.py`'s hostile-binding cases pass for the wrong reason on the platform that runs them

**What is wrong.** `bootstrap/tests/test_session_kernel.py:95-100` parametrizes
four bindings, with the names in comments:

```python
{"interpreter": "python3"},          # not absolute
{},                                  # no interpreter key
{"interpreter": "/etc/hosts"},       # not executable
{"interpreter": "/tmp"},             # a directory
```

On macOS, `/etc` and `/tmp` are both symlinks. `_probe_interpreter` walks
parents for symlink components **before** any file-type or permission check, so
both of those bindings are refused by the symlink branch. The executable-bit
branch and the not-a-file branch are never reached. The test is green and
proves neither of the two properties it names.

**Evidence.**

```
$ python - <<'EOF'  # loads tools/session.py directly
probe /etc/hosts: symlinked
probe /tmp:       symlinked
symlink? /etc: True   /tmp: True
{'interpreter': '/etc/hosts'} -> refused with the _REBIND_REMEDY symlink message
{'interpreter': '/tmp'}       -> refused with the _REBIND_REMEDY symlink message
EOF
```

`ea3d649`'s commit message inherits the error, claiming `_resolve_interpreter`
was matched "on five hostile bindings (relative path, missing key,
**non-executable**, **directory**, vanished interpreter)". Two of those five
did not run as described on the machine that ran them. This is the
"confirm the instrument before trusting an absence" rule in `AGENTS.md`, applied
to a positive result: the case could not have failed for the stated reason.
Cairn has no CI, so darwin is the only platform this ever runs on.

**Why it is non-blocking.** The properties themselves *are* covered — by
`bootstrap/tests/test_session_failsafe.py`, which builds its fixtures inside a
scratch repo (`test_symlinked_leaf_refuses`, `test_symlinked_parent_with_absent_leaf_still_refuses`,
`test_tampered_binding_warns_in_intent_whoami` for the non-executable path). No
coverage is actually absent. But the file that is *supposed* to be the loud,
unconditional guard on this surface is the one carrying the weak fixtures.

**What would fix it.** Build the fixtures under `tmp_path` — a real
non-executable file, a real directory, a real symlink — as the failsafe file
already does, and add the symlink case explicitly instead of getting it twice by
accident. My finding-0 harness above is a working template.

---

## 5 — non-blocking — the shipped trust-root file cites a test file that no longer exists

**What is wrong.** `tools/session.py:100` and `tools/session.py:255` (and both
lines in the byte-identical twin) name `bootstrap/tests/test_lifecycle_board.py`
as the drift guard that "keeps the range table ahead of the content scanner".
That file was deleted in `bfe6bbf`. The oracle itself survived — C6 moved
`TestDirectionalDriftGuard` into `bootstrap/tests/test_session_kernel.py` — so
the property is still enforced, but the pointer in the shipped file is dead.

**Evidence.**

```
$ grep -rn "test_lifecycle_board" --include='*.py' --include='*.md' . | grep -v '^\./dev/'
tools/session.py:100
tools/session.py:255
templates/skills/_lib/session.py:100
templates/skills/_lib/session.py:255
$ ls bootstrap/tests/ | grep board
(no output)
```

This is `AGENTS.md`'s "Name the trigger, check what it checks, and **open it**"
rule failing on its most sensitive file: a reader auditing the encoder is told
where the guard lives, opens it, finds nothing, and is left unable to tell
whether the guard was deleted or merely moved. Note also that `claim_check.py`
reads Markdown, not Python source, so nothing mechanical will ever surface this.

**What would fix it.** Point both lines at `bootstrap/tests/test_session_kernel.py`.
Two-line edit in one file plus the twin.

---

## 6 — non-blocking — the kernel and its tests still speak as if they were the lifecycle CLI

Four instances, each small, together a comprehension cost on the surface the
project most wants readable:

* `tools/session.py:267` — "**The encoder lives in this module, beside its only
  two callers.**" There is exactly **one** in-module caller: `_safe_field` at
  `tools/session.py:275`. The second caller is `tools/board.py:56`, a different
  file that loads the module dynamically. Verified: `grep -n encode_display
  tools/session.py` returns lines 33, 168, 244, 275 — one definition, two
  docstring mentions, one call.
* `tools/session.py:227` — `_PREFIX = "lifecycle:"`. Every line the tool prints
  is prefixed with the name of a CLI that no longer exists. Defensible as pure
  motion, and "lifecycle" is still a live domain word in Cairn, but a reader who
  runs `tools/session.py` and greps the tree for the tool that printed
  `lifecycle:` finds nothing.
* `bootstrap/tests/test_skills_security.py:44` and `:62` — the constant is still
  `LIFECYCLE_SRC` and the module alias still `lifecycle`, both now bound to
  `session.py`. Line 95 asserts with the message `"network primitive in
  lifecycle CLI"`. This is the same defect C6 fixed by renaming
  `test_lifecycle_cli.py` → `test_session_routines.py`, with the stated reason
  "a file named for the CLI it no longer tests misleads the next reader." The
  same reasoning applies to a symbol.
* `bootstrap/tests/test_session_failsafe.py:52` and
  `bootstrap/tests/test_session_routines.py:45` — module aliases
  `cairn_lifecycle_fs` / `cairn_lifecycle`, inherited at C6's rename.

**What would fix it.** Correct the "two callers" sentence (it is a factual claim
in a trust root's docstring). Rename `LIFECYCLE_SRC`/`lifecycle` in
`test_skills_security.py` and fix the assertion message. `_PREFIX` is a
user-visible string with test assertions keyed to it
(`bootstrap/tests/test_skills_security.py:143`, `:229`) — leave it or change it
deliberately,
but do not change it as a drive-by.

---

## 7 — non-blocking — the residual `skipif` guards on the kernel's own tests can never fire

**What is wrong.** `test_session_routines.py:39`, `test_session_failsafe.py:46`
and `test_skills_self_heal.py:36` each carry
`pytestmark = pytest.mark.skipif(not MODULE_PATH.exists(), ...)` and then call
`_load()` **at module scope** (`test_session_failsafe.py:59`,
`bootstrap/tests/test_session_routines.py:52`). Module-level code runs during collection,
before pytest evaluates the marker, so a missing kernel raises
`FileNotFoundError` at collection and the guard is dead code.

**Evidence.** This is the good news half of finding 2's demonstration: with both
kernel copies moved aside at `0701ee3`, `test_skills_self_heal.py` and
`test_skills_security.py` produced `ERROR collecting ... FileNotFoundError`,
not `SKIPPED`.

**Why this matters anyway.** The guards advertise a protection they do not
provide, and the plan spends real length on how a `skipif` on this surface hid
a deletion. A reader who takes them at face value will conclude the kernel's
trust-root tests can go silent — they cannot, but only by accident of load
order. Removing the inert markers would make the file say what it does.

---

## 8 — non-blocking — C1's stated reason for deferring `templates/onboarding/` was wrong in fact

**What is wrong.** `2a93482`'s message says:

> Left alone deliberately: the docstrings inside tools/lifecycle.py and its twin
> (the file is the thing being removed), and templates/onboarding/, which the
> sweep removes in the same order.

The sweep does **not** remove `templates/onboarding/`. That removal is
MAINTAINER-GATED on `_ALWAYS_ON_MAPPINGS` and has not run — `1211005` records
the implementer's own correction that "there is no safe prefix" and the edit was
validated in a throwaway worktree and **discarded**. So three shipped adopter
documents kept telling readers to run `python tools/lifecycle.py session-start`
from C1 through C6, past the commit that deleted that file, until C7's `81cdcfb`
repaired them.

**Evidence.** In a worktree at `0701ee3`, all three shipped onboarding documents
read `` `python tools/lifecycle.py session-start` `` —
`templates/onboarding/solo-greenfield.md` line 34,
`templates/onboarding/high-rigor-legacy.md` line 38, and
`templates/onboarding/collaborative-team.md` line 32. At HEAD all three read
`tools/session.py` (lines 34, 37 and 32 respectively), fixed by `81cdcfb`
("C7: close the orphaned surfaces the sweep left pointing at removed tools").

**Why it matters.** C1's acceptance criterion is "every call site resolves
through it." Three shipped call sites did not, and the reason recorded for
leaving them was a prediction about a chunk that has not happened. The outcome
is repaired; the reasoning pattern — deferring a live surface on the strength of
a future deletion — is the one worth naming, because C8 and C9 are still ahead
and the same move is available there.

---

## What I could not reach

Named honestly, because an incomplete review that says so is worth more than one
that implies completeness.

* **I did not run the full suite.** No `CAIRN_FULL_SUITE=1 python -m pytest
  bootstrap/tests --quality-gate-shuffle-seed=0` and no `quality_gate.py --sub
  neutrality --sub redundancy`. My runs were scoped to the eight files C1
  touched plus the kernel suite (82 tests), plus targeted trust-root
  falsification. Boundary C's "independent targeted falsification" is satisfied;
  Boundary C's "verify the record against the reviewed range" is **not**, because
  for C1 there is no record to verify (finding 3). If the Maintainer wants that
  leg closed, a full run against a clean `0701ee3` is the missing measurement.
* **I did not challenge the Boundary B record that does exist.** The record at
  line 894 is C7's; challenging its bounding, its 2 failures or its 1 skip
  belongs to the C7 reviewer, and I deliberately stayed out of it to avoid
  duplicating a concurrent round.
* **I did not verify the AST attestation baseline.** `ea3d649` states the kernel
  row is allowlisted for self-service repair but could not be repaired while
  `adopt-into-existing-tree`'s four `upgrade.py` symbols were un-re-anchored, and
  that the Maintainer's re-anchor covers five. I did not run
  `test_ast_attest.py` or derive the expected CHANGED set against the committed
  baseline. The plan's own record says both `test_ast_attest.py` failures were
  red at clean HEAD before this session's work.
* **I did not verify the gate manifest re-anchor.** `ea455ca` says all nine
  touched files are gate-frozen and joins an already-owed re-anchor. I took that
  on the record rather than running `_gate_manifest.py verify`. Note that
  `AGENTS.md` warns this goes stale *silently* for a changed file, so a green
  suite is not evidence here — but re-anchoring is the Maintainer's ceremony and
  C8 is where it belongs.
* **I did not test the adopter install path.** Everything I ran was against
  Cairn's self-hosted tree. I did not scaffold a fresh target and confirm that
  `tools/session.py` installs, that its lockfile record is written from
  `_SKILLS_MAPPINGS`, or that `verify_integrity` passes there. Finding 1's claim
  is scoped to **this repository's own** install record, and I say so explicitly:
  a fresh adopter is very likely fine.
* **I did not review C2's `tools/board.py` beyond its encoder call.** It loads
  the kernel via `_repo_root() / "tools" / "session.py"`, and in the shipped twin
  `templates/skills/_lib/board.py` that expression resolves relative to
  `_lib/`'s parent rather than a repo root. Whether that is correct in an
  installed tree is a C2/C3 question and I left it for that reviewer; I flag it
  only because it touches the single-encoder claim I was asked to test.
* **I did not exercise `session-start`.** It performs the skills fan-out
  self-heal write, and with three reviewers in the tree I confined myself to
  `session-end --dry-run`, which writes nothing. `82671c7` records
  `session-start` exiting 0 from the new path and I did not independently
  reproduce it.
