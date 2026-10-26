# Code review (Internal) — C5+C6, the removals — Claude Opus 5 — 2026-08-27

**Obligation**: Internal code review, fresh context, not the implementing agent.
Chunk group **C5+C6** of `dev/plans/subtraction-sweep.md`, commits `3b6f51e`,
`f9f2483`, `e0b83b9`, `6558f3f`, `bfe6bbf`, `984fdb1` (the last two read
together as one logical removal).

**Verdict**: ACCEPT-WITH-FOLLOWUPS

Three blocking findings, six non-blocking. **None of the three is the failure
this chunk group was most at risk of.** The silent-coverage-loss hazard — a
`skipif` guard naming more paths than its tests need — is *closed*, and I
verified that with a control-tested instrument rather than by reading the
record (see Verified negatives). What C5/C6 did leave is a different class:
**registry and prose surfaces that still describe the deleted mechanism**, one
of which now makes Cairn's own supply-chain checker report tamper, one of which
ships to every adopter, and one of which quietly converted a kept behaviour
into an untested one.

## What I ran

* **Full suite**, canonical interpreter (Python 3.13.13, the binding at
  `dev/.cairn/local-env.json`), at `HEAD` = `610f521`, working tree clean apart
  from the two long-standing untracked paths (`.claude/`,
  `dev/measurement/collision_log.md`):

  ```
  PYTHONDONTWRITEBYTECODE=1 CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests -q -rs
    -> 3168 passed, 1 skipped, 0 failed   (475.79s / 7m56s)
  ```

  I ran at `HEAD` and not at `984fdb1`: three reviewers are working
  concurrently in this tree, so a checkout was not available to me. C7/C8 sit
  between, and I attribute each finding to C5/C6 by measuring the *same
  property* at `3b6f51e~1` through `git show`, never by assuming.

* `bootstrap/verify_integrity.py --target .`
* An AST scanner over every module-level `pytestmark` guard in
  `bootstrap/tests/`, control-tested at `6558f3f`.
* A mutation falsification against a throwaway `git worktree` (removed after).

---

## Finding 1 (blocking) — C5/C6 deleted 19 files that the self-hosted lockfile still records, and one of the resulting violations reads as *tamper*

**What is wrong.** No commit in this chunk group touched
`dev/.cairn/cairn-lock.yml`. Cairn's own supply-chain checker now refuses on
Cairn's own tree:

```
$ python bootstrap/verify_integrity.py --target .
verify_integrity: 32 integrity violation(s) vs. dev/.cairn/cairn-lock.yml:
  ...
  illegal living_state opt-out: dev/.cairn/cairn_foldback.md is not an
  authoritative living-state path -- only [...] may set living_state
  (tamper / malformed lockfile)
  ...
  missing: tools/lifecycle.py
  missing: tools/lifecycle_planner.py
  missing: tools/lifecycle_metrics.py
  missing: tools/_lifecycle_metrics/{__init__,cli,config,extract,gitmeta,parse,report,snapshot,subsystems}.py
  missing: scripts/foldback_export_scan.py
  missing: scripts/foldback_suggest.py
  missing: dev/modules/{fold-back-active-prompt,fold-back-ledger,foldback_export_scan,lifecycle-metrics}.md
The on-disk tree no longer matches its recorded install. Do not trust the
shipped scripts until this is resolved.
```

The `illegal living_state opt-out` line is the sharp one, and it is a
**self-inflicted contradiction inside one commit**. `e0b83b9` removed
`"dev/.cairn/cairn_foldback.md"` from `_LIVING_STATE_DSTS` in
`bootstrap/_scaffold/lockfile.py` (now at `:87-89`) — the authoritative list —
while leaving the record that asserts the flag at `dev/.cairn/cairn-lock.yml:44-50`:

```
    {
      "dst": "dev/.cairn/cairn_foldback.md",
      "hash": "sha256:52f7df56...",
      "living_state": true,
```

The comment above `_LIVING_STATE_DSTS` states the intent exactly — the checker
"fails closed on any other record that asserts it (so a modified script cannot
hide by flipping the flag)". The removal edited the allowlist and not the
data, so the fail-closed branch now fires on Cairn's own lockfile and reports
the highest-severity class the tool has.

**Evidence that C5/C6 caused it, measured not assumed.** Comparing each
lockfile record's `dst` against the tracked tree at each revision:

```
before C5 (3b6f51e~1)   records= 90   dst-missing-from-tree=0
after  C5 (f9f2483)     records= 90   dst-missing-from-tree=0
after  C6 (984fdb1)     records= 90   dst-missing-from-tree=19
HEAD    (610f521)       records= 90   dst-missing-from-tree=19
```

Zero before, 19 after. The instrument is confirmed by the pre-C5 zero: it
*could* have reported non-zero and did not.

**Why the plan's own C8 measurement did not see this.** The C8 section reports
*"The raw count of records diverging is 19 ... Restricted to `verbatim`
records, where byte-identity is the contract, it is **three**."* I reproduced
that figure and it is a **different 19**. Hashing each record's `dst` blob
directly:

```
before C5:  90 records w/ hash;  missing=0   hash-mismatch=19
HEAD:       90 records w/ hash;  missing=19  hash-mismatch=16
```

The plan's 19 is the *pre-existing hash divergence among files that exist*
(16 today plus the 3 the Maintainer corrected at `610f521`). The 19 deletions
and the malformed `living_state` flag are a **disjoint set that the C8
measurement never counted**, because a record whose file is gone cannot show a
hash mismatch. So C8's *"Fidelity / integrity — 108 tests across the lockfile,
fidelity and `verify_integrity` suites pass"* is true of the tool's tests and
false of the tool's verdict.

This is also the C5/C6 acceptance criterion *"each installed-source deletion is
atomic with its registry row"* unmet for one registry. The other registries
(`_MODULE_MAPPINGS`, `_SKILLS_MAPPINGS`, `_GITIGNORE_SEEDS`, `KNOWN_TOKENS`)
were edited atomically and correctly; the lockfile was not edited at all.

**What would fix it.** Two separable pieces, and only the second is blocked:

1. **The malformed `living_state` flag is not blocked on anything** and should
   not wait for [TRU-1]. Either restore the path to `_LIVING_STATE_DSTS` or
   drop the record — but a tamper verdict on the project's own integrity root
   must not sit open, because the standing hazard AGENTS.md already names for
   the gate anchor applies verbatim here: a refusal that becomes routine trains
   the habit of routing around refusals.
2. The 19 stale records need the same purpose-built, dry-run-verified
   correction [TRU-1] describes. That is genuinely blocked — but the plan
   should record **19 + a malformed flag**, not three, so the size of the debt
   is the size on the page.

---

## Finding 2 (blocking) — the shipped session kernel names a deleted test file as the guard that makes a deliberate code duplication safe

**What is wrong.** `tools/session.py` and its byte-identical twin
`templates/skills/_lib/session.py` — which installs **verbatim into every
adopter tree** via `_SKILLS_MAPPINGS` — carry two comments pointing at
`bootstrap/tests/test_lifecycle_board.py`, which `bfe6bbf` deleted.

`tools/session.py:94-102`, over the encoder's code-point table:

> "duplicated deliberately, because the board must not import the *conditional*
> content scanner at runtime ... The duplication is admitted **only** with the
> **one-way** drift guard in `bootstrap/tests/test_lifecycle_board.py`"

`tools/session.py:254-256`, in `encode_display`'s own docstring:

> "the board's directional drift test (`bootstrap/tests/test_lifecycle_board.py`)
> is what keeps the range table ahead of the content scanner for **both**
> consumers at once."

Both line numbers are identical in the twin (the files are byte-identical;
`diff` returns empty).

**Why this is blocking and not cosmetic.** This is not a stale "see also". It
is the **entire safety argument for a knowingly duplicated security-relevant
table**, on a surface AGENTS.md lists as high-risk (`encode_display`, "the
single terminal encoder — there is no second escape table in this tree"). A
reader who follows AGENTS.md's own rule — *"A named trigger is checked by
opening it — a path that resolves is not a trigger that governs"* — opens
nothing, and the correct conclusion available to them is that the duplication
is unguarded.

**And the guard did not die — it moved.** `bfe6bbf`'s own commit body says so:
*"**The drift oracle moved rather than dying.** ... It lived in
test_lifecycle_board.py. Now in test_session_kernel.py."* It is live at
`bootstrap/tests/test_session_kernel.py:158`, `class TestDirectionalDriftGuard`.
So the author moved the oracle, wrote about moving it, and left both pointers
in the shipped file aimed at the old address.

**Why no gate caught it.** I control-tested the checker rather than assuming:

```
# copy of test_session_routines.py with a definitely-broken path planted
# in the same docstring position
$ python scripts/claim_check.py --root . <scratch>/probe.py
claim_check: <scratch>/probe.py -- OK, no claim-check flags.
```

`claim_check` does not flag an unresolvable repo path inside a `.py`
docstring or comment. The pattern *could not* have matched, so its silence on
`session.py` is not evidence. That is a second, smaller finding folded in
here: the project's stated verify-before-asserting instrument has a blind
spot on exactly the file class this sweep edited most.

**What would fix it.** Repoint both comments at
`bootstrap/tests/test_session_kernel.py::TestDirectionalDriftGuard`, in both
twins, keeping them byte-identical.

---

## Finding 3 (blocking) — C6 deleted the only positive test of a behaviour it deliberately kept, leaving a negative twin that passes *harder* when the behaviour is gone

**What is wrong.** `e0b83b9`'s commit body names the standing capture prompt as
something it consciously preserved:

> "The goodnight's standing capture prompt survives, repointed. The practice is
> not being retired — only the local staging ledger ... Deleting it would have
> removed a habit nobody decided to remove."

The prompt lives at `tools/session.py:1421-1426` and its twin. `984fdb1` then
deleted `test_handoff_surfaces_foldback_candidates`, whose body (visible at
`git show e0b83b9:bootstrap/tests/test_lifecycle_cli.py`, lines 379-403) held
the only positive pin on it:

```python
    # The standing capture prompt must appear.
    assert "scan today's doctrine activity" in out, (
        f"capture prompt not found in:\n{out}"
    )
```

What survives is its negative twin,
`bootstrap/tests/test_session_routines.py:381-400`
(`test_session_end_without_handoff_does_NOT_surface_foldback`), which asserts
only *absence*. A tree-wide grep finds exactly one test mentioning the string,
and it is that `not in`:

```
tools/session.py:1423:            "scan today's doctrine activity for portable ...
bootstrap/tests/test_session_routines.py:400:    assert "scan today's doctrine activity" not in out
templates/skills/_lib/session.py:1423:            "scan today's doctrine activity for portable ...
```

**Falsified, not argued.** In a throwaway `git worktree` at `HEAD` (removed
after; the working tree was untouched) I deleted the `_emit(...)` block from
**both** twins — so twin byte-identity still holds — and ran the three suites
that own this surface:

```
capture prompt DELETED from both twins
$ pytest bootstrap/tests/test_session_routines.py \
         bootstrap/tests/test_session_failsafe.py \
         bootstrap/tests/test_session_kernel.py -q
71 passed in 5.78s
```

The behaviour C6 went out of its way to keep can be deleted outright and the
suite is greener than before.

**Two of the surviving test's three assertions are already vacuous.** The
kernel contains neither string the fixture stub emits:

```
$ grep -n "Surfaceable candidates\|MyAgingCandidate" tools/session.py templates/skills/_lib/session.py
(no output)
```

Only the third assertion (`"scan today's doctrine activity" not in out`) still
pins anything real — the `--handoff`-only gating. The fixture scaffolding
supporting the other two — `_FOLDBACK_SUGGEST_STUB` (`:333-340`), `_AGING_LEDGER`
(`:342-351`), and the `repo_with_foldback` fixture (`:353-376`), which seeds a
`scripts/foldback_suggest.py` and a `dev/.cairn/cairn_foldback.md` that no code
reads — makes the test *look* like it covers fold-back surfacing.

**What would fix it.** Rehome the positive assertion: one test that runs
`session-end --handoff` and asserts the capture prompt **is** emitted. Its
falsifier is the mutation above — deleting the `_emit` block must redden it.
Then strip the two dead assertions and the fixture machinery that exists only
for them.

---

## Finding 4 (non-blocking) — there is no Boundary B record for C5 or C6, and C6's test-count delta was never reconciled

`dev/plans/subtraction-sweep.md` requires (Verification section) a record *"after
the final implementation commit of each of C1, C5, C6, C7"* in a named format,
and states: *"Every Boundary B record states the expected delta and reconciles
it against the files that chunk removed. An unexplained drop is a defect, not a
success."*

The plan contains exactly **one** `## Implementation verification` heading
(`dev/plans/subtraction-sweep.md:894`), and it is C7's — its own tested SHA is
`b1e655d`. There is no C5 record and no C6 record, in this plan or anywhere in
`dev/`.

The commit bodies carry partial evidence, and C5's is genuinely good
(`f9f2483`: *"4,574 collected -> 4,494, a drop of 80: 79 nodes from
test_suite_ledger.py plus test_a_refused_session_is_scoped_unknown"* — an exact
reconciliation). **C6's is not.** `bfe6bbf` reports pass/skip figures and
`984fdb1` repeats them, but neither states an expected node delta or
reconciles it against the files removed — which is the one thing the plan
singles out as mandatory for this chunk. For scale, the 16 test files C6
deleted define **837** `def test_` functions:

```
test_lifecycle_contract.py 408   test_lifecycle_board.py 101   test_pilot_evidence.py 83
test_lifecycle_brief.py     48   test_foldback_export_scan.py 36  test_foldback_active_prompt.py 27
test_lifecycle_metrics_events.py 24  test_lifecycle_vocabulary.py 22  test_foldback_suggest.py 20
test_lifecycle_stage_patterns.py 17  test_byline_identity.py 13  test_foldback_ledger_module.py 10
test_lifecycle_metrics_config.py 10  test_fold_back_ledger_module.py 7  test_metrics_status_normalization.py 7
test_doctrine_vocabulary_drift.py 4
```

Under AGENTS.md's Boundary C rules the absence of a valid Boundary B record is
itself a trigger for a fresh full run — which is why I ran one. **The suite is
green and the skip count reconciles** (below), so this is a record gap and not
a coverage gap. But the plan cannot archive with two of its four required
records missing, and the reconciliation the plan calls the whole point of the
exercise was never written for the chunk that removed 837 tests.

## Finding 5 (non-blocking) — dead residue in `bootstrap/tests/test_session_routines.py`

`984fdb1` deleted the tests but not their scaffolding. At `HEAD`:

* `:403` — a section banner `# --- lifecycle-metrics v2 snapshot layer ---` over
  a module that no longer exists.
* `:405` — `#: The lifecycle_metrics template source (loaded directly, no
  scaffold needed).` — a doc-comment for `_LM_PATH`, which was deleted, followed
  by three blank lines where the code was.
* `:409-418` — `_SAMPLE_PROPOSAL`, used only by
* `:421-430` — the `lm_repo` fixture, which is requested by **zero** tests
  (`grep -n "lm_repo" ` returns only the definition).
* `:22` — the module docstring's run instruction (Finding 6).

This is the same residue class `f9f2483`'s own commit body describes catching in
`conftest.py` — *"a 30-line orphaned section header"*. Here it shipped.

**Fix**: delete `:403-430`, and the `importlib` / `ModuleType` imports if the
surviving `_load()` at `:44-47` is the only remaining consumer (it is not — it
still uses both, so leave the imports).

## Finding 6 (non-blocking) — both renamed test files still name their old paths, and one still describes itself as testing the CLI the rename removed

`bfe6bbf` renamed two files with an explicit reason: *"Renamed to
test_session_routines.py and test_session_failsafe.py, because a file named for
the CLI it no longer tests misleads the next reader."* The filenames moved; the
self-descriptions did not.

* `bootstrap/tests/test_session_routines.py:22` — `python -m pytest
  bootstrap/tests/test_lifecycle_cli.py`
* `bootstrap/tests/test_session_failsafe.py:26` — `python -m pytest
  bootstrap/tests/test_lifecycle_failsafe.py`
* `bootstrap/tests/test_session_failsafe.py:1` — *"Tests for the **lifecycle
  CLI's** safety layer"* — the exact sentence the rename was performed to fix.
* `bootstrap/tests/test_session_routines.py:246` and
  `bootstrap/tests/test_session_failsafe.py:531` and
  `bootstrap/tests/test_scope_reduction_trap.py:402` cross-reference
  `test_lifecycle_failsafe.py` / `test_lifecycle_contract.py` for the "full
  matrix", pointing at files that do not exist.

Copy-pasting either run instruction produces `ERROR: file or directory not
found`. As Finding 2 establishes by control test, `claim_check` cannot catch
this class in `.py`.

## Finding 7 (non-blocking) — `TestMultiScriptModules` still *claims* the coverage it lost

The empty-parametrize skip is correctly filed as `[VER-5]` and disposed in the
C7 Boundary B record, and I confirm it is the suite's only skip. What the
disposition does not reach is that the file still asserts the coverage in
prose, so a reader of the file — rather than of the register — is told the
property is pinned:

* `bootstrap/tests/test_reference_scripts.py:126-131` — the class docstring:
  *"this test covers fold-back-ledger's 2-script case (export_scan + suggest)"*.
  It covers nothing; `_MULTI_SCRIPT_MODULES` is `{}`.
* `bootstrap/tests/test_reference_scripts.py:48-60` — a 13-line comment inside
  `_SCRIPT_MODULES` narrating a deleted entry (*"we deviate here only because
  the fold-back-ledger module ships 2 verbatim scripts"*). The deviation is
  gone; the narration stayed. `_SCRIPT_MODULES` now has one entry,
  `claim-check`, and the comment sits after it describing a second.

The `#:` note on `_MULTI_SCRIPT_MODULES` itself (`:67-70`) is honest and
well-written — it says the dict is empty and why it is kept. The docstring
above the class contradicts it.

Also note the `defer` batch carrying `[VER-5]` is marked
**"REQUESTED AS ONE BATCH, NOT YET AUTHORIZED"**, so this is deferred without
the Maintainer's allowance yet in hand.

## Finding 8 (non-blocking) — orphaned ignore rules and orphaned data files that the clean-tree check structurally cannot see

C5's manifest dispositions `dev/measurement/suite-runs.jsonl` as **whole**
(i.e. removed). It is still on disk:

```
dev/measurement/suite-runs.jsonl    PRESENT (188424 bytes)
dev/measurement/suite-cost.md       PRESENT (  6671 bytes)
dev/measurement/pilot-activation.md absent
dev/measurement/pilot-events.md     absent
```

The two pilot records were correctly removed; the two suite-ledger outputs were
not. `suite-cost.md` is the output of `tools/suite_cost.py`, deleted by
`f9f2483`; nothing regenerates or reads either file now.

Three `.gitignore` rules are likewise orphaned — every producer is deleted:

* `.gitignore:11` — `dev/.cairn/.foldback-draft-*.md` (producer:
  `foldback_suggest.py`, deleted `e0b83b9`)
* `.gitignore:18` — `dev/measurement/suite-cost.md` (producer:
  `tools/suite_cost.py`, deleted `f9f2483`)
* `.gitignore:19` — `dev/measurement/suite-runs.jsonl` (producer: the
  `conftest.py` ledger hooks, deleted `f9f2483`)

**Why this is worth a finding rather than a tidy-up.** These files are
gitignored, so `git status --short` reports a clean tree with 195 KB of a
deleted mechanism's output sitting in it. The "clean pre/post working-tree
state" a Boundary B record attests **cannot** observe them by construction, so
this residue class is invisible to the plan's own verification, permanently.
`bootstrap/_scaffold/config.py`'s `_GITIGNORE_SEEDS` was correctly pruned of
the fold-back row; only the self-hosted `.gitignore` was missed.

## Finding 9 (non-blocking) — stale exemplars that a reader cannot resolve

Small, uniform class: a comment cites a removed module as the pattern to
imitate.

* `bootstrap/_scaffold/config.py:793` — *"the claim-check / lifecycle-metrics
  reflections module pattern"*; `:829` — *"the claim-check / lifecycle-metrics
  pattern"*. `lifecycle-metrics` is gone, so half of each two-example pattern
  is unresolvable.
* `bootstrap/tests/test_default_security_stance.py:17-27` —
  `NO_PRESET_MODULE_SENTINELS` still maps `"lifecycle-metrics"` and
  `"fold-back-ledger"` to their removed sentinel files. **The test is not
  broken**: the dict drives a set-membership comparison at `:185-189`, so dead
  rows are inert and a *new* default-on module would still redden it. But two
  of nine entries in a table named "sentinels" sentinel nothing.
* `bootstrap/tests/test_skills_security.py:44` and `:62` — the constant is still
  `LIFECYCLE_SRC` and the loaded module name still `cairn_lifecycle_sec`,
  though both now point at the session kernel. Against the project's own
  "name a test for the property it pins" convention.
* `doctrine/onboarding.md:5` — *"parallel to the fold-back.md pattern"*, citing
  a doctrine file `e0b83b9` deleted.

I did **not** flag the ~20 `foldback #12` / `fold-back #42` provenance markers.
`e0b83b9` left those deliberately and argued the case correctly in its commit
body: they record *which fold-back produced a decision*, which stays true after
the mechanism goes. I agree, and I looked at them precisely so this review does
not read as "make the grep clean".

---

## Verified negatives

Stated because a code review that reports only faults gives the next reader no
way to tell a checked surface from an unchecked one.

**1. The silent-coverage-loss hazard is closed, and I measured it rather than
reading the record.** I parsed every one of the **105** test modules in
`bootstrap/tests/`, evaluated each module-level `pytestmark` guard's path
expressions, and resolved them against disk:

```
105 test modules scanned
Every module-level pytestmark skipif path RESOLVES on disk.
```

**The instrument is control-tested.** Run unchanged against the tree at
`6558f3f` — the commit whose own body documents the two incidents — it flags
both by name:

```
POSITIVE CONTROL at 6558f3f:
    test_lifecycle_vocabulary.py     -> TL_SRC = scripts/transition_lint.py
    test_upgrade_module_additions.py -> ..._lifecycle_metrics
```

So the zero at `HEAD` is a measurement, not an absence of measurement.

**2. The skip count reconciles.** `-rs` names exactly one skip, and it is the
one already disposed:

```
SKIPPED [1] bootstrap/tests/test_reference_scripts.py:133: got empty parameter set for (module_name)
3168 passed, 1 skipped, 3 warnings in 475.79s
```

No passed→skipped transition anywhere. The two AST-attestation failures in the
C7 record have cleared (the Maintainer's correction at `d283589`), so the suite
is fully green at `HEAD` — better than any record in the plan.

**3. Twin byte-identity survived the rehoming.** The plan flagged
`test_the_two_lifecycle_copies_are_byte_identical` as "rehoming, not deletion".
It was rehomed:
`bootstrap/tests/test_session_kernel.py:123-128`,
`class TestTheTwinIsByteIdentical`, and the assertion is unconditional. I
confirmed the property independently — `diff tools/session.py
templates/skills/_lib/session.py` is empty. `test_session_kernel.py` also has
**no `skipif` guard at all**, and its module docstring says why in as many
words. That is the correct structural answer to this sweep's hazard, and it is
the best thing in the chunk group.

**4. The security scan-target repointing is correct, and widened rather than
narrowed.** `_SKILLS_PY` in `bootstrap/tests/test_security_lint.py` moved from
`{lifecycle.py, lifecycle_planner.py}` to `{board.py, session.py}` — **not** to
`{session.py}`. `tools/board.py` is newly twinned and registered in
`_SKILLS_MAPPINGS` (`bootstrap/_scaffold/config.py:582-588`) and was added to
the by-name scan assertion in the same commit, so the 63-day release-unscanned
miss that assertion exists to prevent cannot recur through the new file. The
count pins (`53 -> 40` on-disk templates `.py`, manifest rows `57 -> 44`) moved
with it. The tamper-target fixture in `test_security_stack.py` was repointed at
`tools/session.py` rather than deleted.

**5. The fold-back replacement channel is coherent, and honest about what it
lost.** `.github/ISSUE_TEMPLATE/foldback.md` and
`.github/PULL_REQUEST_TEMPLATE/foldback.md` both state plainly that
`foldback_export_scan.py` was retired, that **no command replaces it**, and
that the human affirmation is therefore "the WHOLE export boundary, not half of
one" — rather than leaving a checkbox implying a scan happened. Both declare
themselves the surviving statement of the retired doctrine. Nothing in
`doctrine/`, `docs/`, `templates/`, `AGENTS.md` or `README.md` still cites
`doctrine/fold-back.md` as extant. This is exactly the "describe the check by
its real trigger" discipline, applied to a check that was removed.

**6. `TestVocabularyLoader` had genuinely nothing to rehome.** The plan listed
it (`test_pilot_evidence.py:362-514`) as shared surface, on the ground that the
vocabulary loader is called by `cmd_review_brief`, `_declared_assurance` and
`_build_closeout`. All three died with the CLI in the same chunk, so the
surface it protected does not survive. Correctly deleted rather than rehomed —
and `test_session_kernel.py:51` (`assert "lifecycle_planner" not in source`)
pins the property that actually matters now.

---

## Claim-check disposition

`python scripts/claim_check.py dev/plans/archive/2026-08-27-code-review-c5-c6-removals.md`
reports **11 hard flags**, all of one kind: a repo path that does not resolve
**because the chunk group under review deleted it**. Six are in the findings
themselves; the other five are this table restating those same six paths, which
is the checker being consistent rather than a second defect. A review of a deletion
necessarily names what was deleted, and the citation *is* the finding. Marked
here rather than left to assert, and rather than routed around by editing the
shared `dev/.cairn/claim-check-allow.json` — three reviewers are working in this
tree concurrently and that config is not mine to change mid-round.

| flag | deleted by |
|---|---|
| `bootstrap/tests/test_lifecycle_board.py` (Finding 2) | `bfe6bbf` |
| `scripts/foldback_suggest.py` (Finding 3) | `e0b83b9` |
| `dev/.cairn/cairn_foldback.md` (Finding 3) | `e0b83b9` |
| `tools/suite_cost.py` x2 (Finding 8) | `f9f2483` |
| `doctrine/fold-back.md` (Finding 9) | `e0b83b9` |

Two further flags in my first draft were **my own** malformed line citations
(`file.py:18,21` — a form the checker cannot parse, on files that do exist).
Both corrected before commit; the checker earned that one.

## What I could not reach

* **I did not run at `984fdb1`.** Three reviewers share this tree and a
  checkout would have collided with them, so my suite figure is `HEAD`
  (`610f521`) with C7 and C8 included. Every *attribution* to C5/C6 in this
  review is instead a same-property measurement at `3b6f51e~1` or `6558f3f`
  through `git show` / `git ls-tree`, which does not touch the tree. What this
  costs: if C7 or C8 masked a C5/C6 regression, my green suite would not
  separate them.
* **I did not run `scripts/quality_gate.py --sub neutrality --sub redundancy`**
  or `check_cairn.py`. The C7 record reports neutrality `fail=79` as
  pre-existing, and I did not independently establish that any of those 79 are
  or are not C5/C6's.
* **I did not verify the four install-contract surfaces agree** (fidelity
  manifest, gate manifest, lockfile schema, published `scaffold.py --manifest`)
  beyond the lockfile leg in Finding 1. That is C8's, and it is unexecuted.
* **I did not attempt a fresh scaffold per commit**, which the C5/C6 acceptance
  criteria require (*"a fresh scaffold is recorded green per commit"*). No such
  record exists in the plan for either chunk, and I did not reconstruct one.
  Related: the criteria's **positive-control mutation** — *"one unexpected
  shipped executable **must fail** the check — is recorded **once**"* — I found
  no record of, and did not run.
* **I did not read the ~50,000 deleted lines.** I read the deletion manifest,
  every surviving file that referenced a deleted symbol (via tree-wide greps
  for each removed module and each deleted test file), and the diffs of the
  partial edits. A deleted behaviour that nothing in the surviving tree ever
  named would not appear in that search.
* **The `[VER-5]` repopulation and the onboarding findings** (deferred items 1,
  3 and 4) I confirmed are correctly *filed*; I did not assess whether the
  proposed remedies are right, since all three are unauthorized deferrals and
  the onboarding decision is MAINTAINER-GATED.
* **Finding 3's falsification covered three test modules, not the full suite.**
  I established by tree-wide grep that no other test mentions the string, which
  is why I did not spend a second 8-minute run to prove the same thing.

---

Untracked paths: `dev/measurement/suite-runs.jsonl`, `dev/measurement/suite-cost.md` -- both are gitignored local measurement files (`.gitignore` lines 18-19), so a fresh checkout does not carry them. Added 2026-10-18 so the citations above resolve on any checkout.
