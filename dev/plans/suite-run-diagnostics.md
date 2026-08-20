# Plan: the suite reports its own cost

**Source proposal**: `dev/proposals/archive/2026-08-19-claude-suite-run-diagnostics.md`
**Status**: revising-plan
**Plan review**: required(**Internal**) — ratified by Maintainer amendment at
`e6e854d58f7083b5497cfa77a5d319285e7626b9`, overriding the plan-review
template's default escalation path. See "Plan-review tier rationale" below
for why, and for the field this plan deliberately omits.
**Last update**: 2026-08-20
**Opened**: 2026-08-20

## Source proposal

Accepted as revised (Revision 5) at `a3226c7`, amended at `e6e854d`. The suite's
cost has been re-measured by hand at least four times and lost every time
because the number, not the place to look it up, is what survived. The proposal
makes `bootstrap/tests/conftest.py` write one JSONL row per top-level pytest
session to a gitignored ledger, `dev/measurement/suite-runs.jsonl`, and adds a
standalone reader, `tools/suite_cost.py`, that renders it for a human without
re-running anything. Five hooks, five fail-closed guards, a fixed row schema
with a `scope` classifier that only asserts `full` under both an exact-argv
check and a resolved-postcondition check, a 4,096-byte encoded-row budget with
deterministic eviction and a total skeleton fallback, and POSIX `flock` +
tail-repair durability. Zero subprocesses; zero dependencies; nothing executed.
This plan executes that decision; it does not re-litigate it.

### Plan-review tier rationale

The proposal's final External review (`64830d961f378a72e3f16a5313abfb9bb7f0891e`)
recorded a "plan readiness" finding of the value that, under
`doctrine/dual-review.md` > "Plan-readiness inheritance," ordinarily sends the
derived plan to `required(External)` and forbids inheriting the proposal's
basis. The Maintainer amended the Decision at `e6e854d` to ratify
`required(Internal)` instead, reallocating deliberative weight to the proposal
itself — five External review rounds (E1 through E20) across Revisions 1–5.

**This plan does not declare a field naming an "inherited proposal basis."**
That field is reserved for a proposal review recording the *opposite*
finding — readiness, not the distinct-review finding this proposal's last
review actually recorded. `tools/lifecycle_planner.py`'s
`plan_inheritance_violations` function (read directly at
`tools/lifecycle_planner.py:3608-3614`) hard-refuses any plan that pairs that
field with a source proposal whose last-recorded finding is the distinct-review
one; declaring it here would trip that refusal, not satisfy it.
`required(Internal)` with no such field is the correct, and only correct,
declaration for this plan — the Maintainer's amendment is what authorizes the
tier, not an inheritance claim this proposal's review history does not
support.

## Proposed paths

Proposed paths:
- `tools/suite_cost.py` — the ledger reader; lands in Chunk B.
- `bootstrap/tests/test_suite_ledger.py` — the contract test file (writer and reader falsifiers — see Scope); lands in Chunk C.

Untracked paths:
- `dev/measurement/suite-runs.jsonl` — the gitignored live ledger the `pytest_sessionfinish` hook appends to; never committed, wired by Chunk D's `.gitignore` rule.

## Scope

**In** (Revision 5, "Scope"): five hooks in `bootstrap/tests/conftest.py`
(`pytest_configure` claim marker, `pytest_runtest_logreport`,
`pytest_collectreport`, `pytest_deselected`, `pytest_sessionfinish`); the
gitignored JSONL ledger and its `.gitignore` rule; the reader
`tools/suite_cost.py`; **one** new test file; a note in
`dev/measurement/README.md`.

**Excluded** (Revision 5, "Scope"): any subprocess; any doctrine,
canonical-command, template or adopter surface; any dependency; any
enforcement. This plan adds no capability that changes what any command does or
what any doctrine text says — it only adds a side-channel write and a reader.

**Assurance path is high-assurance**, for two independent reasons named in the
proposal header and unchanged here: the edit lands in gate-frozen
`bootstrap/tests/conftest.py` (re-anchor required), and it adds a file write to
every non-child, non-release test session in the one file that can already
decide a session's exit status.

### Sequencing — this plan lands FIRST, before `full-suite-interception`

`dev/proposals/archive/2026-08-19-claude-full-suite-interception.md` (accepted
the same day; its plan `dev/plans/full-suite-interception.md` opened at
`517d66b`, under a minute after this plan's own opening commit, and the
proposal archived with it) also
edits
`bootstrap/tests/conftest.py` — a `PreToolUse`-style refusal hook over an
unnarrowed full-suite invocation. The two proposals' own "Related" fields state
neither depends on the other's *design*, but they share exactly one file, and
the sequencing decision has already been made outside this plan: **this plan
(`suite-run-diagnostics`) implements first; `full-suite-interception` implements
second**, against the tree this plan leaves behind. This plan's scope is
bounded to Revision 5's contract only — no hook, refusal behaviour, or
`AGENTS.md`/vendor-wrapper sentence belonging to `full-suite-interception` is
implemented here, planned here, or anticipated here beyond this note.

### A scope-adjacent decision this plan had to make: where the reader's test lives

Revision 5 commits to **exactly one** new test file, but its own Evidence table
carries a "Reader outcomes" falsifier that exercises `tools/suite_cost.py` —
a script that lives outside `bootstrap/tests/` entirely. The proposal never
resolves this explicitly. This plan resolves it by putting the reader-outcomes
falsifier **inside** `bootstrap/tests/test_suite_ledger.py` alongside the
writer's falsifiers (importing `tools/suite_cost.py` as a module rather than
shelling out to it, consistent with "zero subprocesses"), so the "one new test
file" commitment holds literally. See Chunk C and "Not settled by the proposal"
below.

### A scope-adjacent decision this plan had to make: `tools/suite_cost.py` must not be installed

`tools/` in this repository is **not** a plain scratch directory — measured by
reading `bootstrap/scaffold.py --manifest`, essentially every `.py` file
currently under `tools/` (`lifecycle.py`, `lifecycle_planner.py`,
`lifecycle_metrics.py`, `intent.py`, `evolution_infer.py`, `prune_intents.py`,
`prune_reflections.py`, the `_intent/` and `_lifecycle_metrics/` packages) is a
verbatim-mapped install target from `templates/modules/*` — i.e. this
directory is otherwise **entirely** adopter-shipped surface. Revision 5's
scope explicitly excludes "any … adopter surface," so `tools/suite_cost.py`
must land as a Cairn-repo-only file that `bootstrap/_scaffold/config.py`'s
mapping table never references. This is not unprecedented: `scripts/` is the
same dual-purpose shape, and `scripts/quality_gate.py` and
`scripts/check_cairn.py` already coexist there as genuinely Cairn-only,
unmapped files alongside `scripts/claim_check.py`,
`scripts/content_scan.py` and `scripts/link_check.py`, which *are* mapped
(verified against the same `--manifest` output). Chunk B's acceptance
criterion states this explicitly so an implementer does not "complete" the
tool by pattern-matching its mapped neighbours into `config.py`.

### Documentation / doctrine surface

* `dev/measurement/README.md` **and `templates/core/dev/measurement/README.md`**
  — **a shipped adopter surface, contrary to this plan's first reading of it.
  The Maintainer has allowed the template edit** (allowance recorded under
  Chunk D); both copies are edited, in the same commit, byte-identical.
  Measured, not assumed: `python
  bootstrap/scaffold.py --manifest` emits it as an install destination
  (`dev/measurement/README.md <- core/dev/measurement/README.md`,
  `substituted`), the mapping is declared in `bootstrap/_scaffold/config.py`,
  and `diff templates/core/dev/measurement/README.md
  dev/measurement/README.md` is byte-identical. Editing only Cairn's copy
  desynchronizes the twin and leaves the tree failing
  `bootstrap/verify_integrity.py` against the recorded lockfile hash until an
  `upgrade --finalize`. Revision 5 excludes "any doctrine, canonical-command,
  template or adopter surface", so the accepted contract did not authorize
  this on its own — the Maintainer's allowance is what does, and the
  generic-phrasing constraint under Chunk D is what keeps the widened surface
  from carrying Cairn's specifics into adopter trees.
* `CHANGELOG.md > Unreleased > Added` — one release-note line (Chunk D).
* **No `AGENTS.md` or `doctrine/` change.** The claim of "no template-surface
  change" that stood here was false for `dev/measurement/README.md` and is
  withdrawn.

**Contract expansion**: adopter surface — `templates/core/dev/measurement/README.md`
joins the touched set. Authorized by the Maintainer, quoted verbatim and
visually isolated:

> "Totally allow the template edit"

Recorded here rather than paraphrased into the chunk row, because an allowance
that widens accepted scope is the one thing a plan cannot grant itself. What
the allowance was asked for, and therefore what it covers: editing the shipped
`templates/core/dev/measurement/README.md` alongside Cairn's installed copy so
the twin stays byte-identical. It does **not** extend to any other shipped
template, to doctrine, or to the canonical-command surface, all of which
Revision 5 still excludes.

## Sequence

```
1. Chunk A -- the ledger writer (bootstrap/tests/conftest.py)      [commit pending]
2. Chunk B -- the reader (tools/suite_cost.py)                     [commit pending]
3. Chunk C -- the contract tests (test_suite_ledger.py)            [commit pending]
4. Chunk D -- gitignore, README note, CHANGELOG                    [commit pending]
5. Code review (independent, not the implementing agent)           [pending]
6. Chunk E -- Security Review + re-anchor ceremony (Maintainer-owned) [pending]
```

Chunks A–D are ordinary implementing-agent commits under the standing
commit-workflow rule (no per-commit approval gate; approval attaches to
pushing, a Decision, a plan deviation, or a plan's own explicit fence). Step 5
is the plan-archive precondition. Chunk E is fenced — see its own section.

### Chunk A — the ledger writer

`bootstrap/tests/conftest.py` currently carries `pytest_addoption`,
`pytest_collection_modifyitems`, `pytest_runtest_logreport`,
`pytest_collectreport`, and `pytest_sessionfinish` (the shuffle hook and the
existing release-mode outcome rule). This chunk extends three of those and
adds two hooks that do not yet exist.

| # | File | Change |
|---|------|--------|
| A1 | `bootstrap/tests/conftest.py` | Add `pytest_configure`: claim `CAIRN_SUITE_LEDGER_SESSION=1` if unset (guard 2, reentrancy-with-ownership); a pre-existing marker means this session is a child and every later ledger hook becomes a no-op for it. |
| A2 | `bootstrap/tests/conftest.py` | Add `pytest_deselected`, and extend `pytest_runtest_logreport` / `pytest_collectreport` to also accumulate per-node phase durations, outcome counts (the seven-outcome precedence: setup/teardown failure → `errors`; call failure → `failed`; `wasxfail` → `xpassed`/`xfailed`; any `skipped` → `skipped`; passing setup with no call report → `aborted`; else `passed`), and `by_file` timing, **alongside**, never replacing, the existing `_record_refused_report` release-evidence accumulation — release logic first, ledger accumulation last, in the same hook bodies. |
| A3 | `bootstrap/tests/conftest.py` | Extend `pytest_sessionfinish`: after the existing release-mode block (unchanged), add the ledger block **last**, wrapped in `except BaseException` (not `Exception` — a `KeyboardInterrupt` mid-retry must not turn exit 1 with a release report into exit 130 with none). Implements: guards 3–5 (containment against the resolved `tempfile.gettempdir()`, the release-mode exemption, and the `CAIRN_SUITE_LEDGER=0` / absent-directory opt-outs); `head` resolution by direct `.git`/`HEAD`/`commondir`/refs reads; the `scope`/`scope_basis` classifier (both channels — exact-argv-family membership *and* resolved postconditions); the pinned encoder (`json.dumps(row, ensure_ascii=True, separators=(",", ":"), allow_nan=False, sort_keys=True)`) with ASCII-sanitize-then-cap, `by_file` smallest-duration-first eviction, and the total skeleton-row fallback; the `flock`-with-250ms-deadline / tail-repair durability; the row-per-session invariant. |

**Guard-atomicity note.** The five guards are not independently useful —
an unguarded intermediate hook is exactly the "diagnostics hook that can fail a
suite" hazard the proposal's Assurance path names. If this chunk lands across
more than one commit, no intermediate commit may leave a hook wired without
its own outcome-inert wrapping and without guards 2–5 already in place; the
guard set lands as one atomic unit even if the schema/encoding logic around it
is refined in a follow-up commit within this same chunk.

### Chunk B — the reader

| # | File | Change |
|---|------|--------|
| B1 | `tools/suite_cost.py` | New, standalone, stdlib-only (no dependency, per Excluded scope). Renders `dev/measurement/suite-runs.jsonl`: opens with the do-not-re-run instruction; every figure carries date/commit/interpreter/overlap conditions; cost concentration and trend from `by_file`, stating `by_file_total`/`by_file_kept` whenever pruned; `full`-run frequency **per day, never per plan** (plan attribution only via `CAIRN_SUITE_LEDGER_LABEL`); overlap reported only as "overlapped another recorded top-level session," computed from row intervals; malformed lines reported, never skipped; session frequency stated as a lower bound; the reader's own known-limits list (release, nested, opted-out, crashed, uninstrumented); dirty-tree state reported as `unknown`, never as measured (deferred behind its own future Security Review); re-derives `scope` from `invocation` + `scope_basis` + runtime fields and reports a disagreement against the stored value; no bare identifiers. |

**Acceptance criterion for this chunk (binding):** `tools/suite_cost.py` is
**not** added to `bootstrap/_scaffold/config.py`'s file-mapping table, and
`bootstrap/scaffold.py --manifest` must show no `tools/suite_cost.py` row
after this chunk lands — see "A scope-adjacent decision" above.

### Chunk C — the contract tests

| # | File | Change |
|---|------|--------|
| C1 | `bootstrap/tests/test_suite_ledger.py` | New. The full falsifier matrix from Revision 5's "Evidence" table (see Acceptance criteria below for the binding list), covering both Chunk A's writer and Chunk B's reader — this is the "one new test file" the proposal commits to; the reader-outcomes rows import `tools/suite_cost.py` as a module. |

C1 cannot be authored until both A and B exist; it is sequenced last among the
three not because tests come last in general but because this file's own
falsifiers exercise both prior chunks' finished behaviour, including the
`scope` re-derivation-and-disagreement check that spans both.

### Chunk D — gitignore, README note, CHANGELOG

| # | File | Change |
|---|------|--------|
| D1 | `.gitignore` | Add `dev/measurement/suite-runs.jsonl` so the live ledger stays untracked (same rule shape as the existing `dev/measurement/snapshots/` and `dev/measurement/suite-cost.md` entries). |
| D2 | `dev/measurement/README.md` **and its shipped twin `templates/core/dev/measurement/README.md`** | **Maintainer-allowed template-surface edit — see the allowance below.** Add a note under "What belongs here" naming an operational-ledger-that-feeds-measurement slot, cross-linking its reader. **Both copies, same commit, byte-identical.** This file is a shipped install destination (`bootstrap/scaffold.py --manifest`; mapping in `bootstrap/_scaffold/config.py`), and the two copies are byte-identical today — so editing Cairn's alone would desynchronize the twin and fail `bootstrap/verify_integrity.py` against the recorded lockfile hash. **Write the note generically**, in the register the rest of that shipped README uses: it lands in every adopter's tree, so it describes the *slot* ("an operational ledger a measurement reader consumes"), not Cairn's own `suite-runs.jsonl` filename or `tools/suite_cost.py`. Cairn's specific ledger and reader are named in the CHANGELOG line at D3, which ships to nobody. |
| D3 | `CHANGELOG.md > Unreleased > Added` | One line: in-suite cost telemetry (`bootstrap/tests/conftest.py` hooks + gitignored ledger) and its reader `tools/suite_cost.py`; cross-link the archived proposal by filename stem. |

**Note on `dev/measurement/suite-cost.md`:** a file by that name already exists
(gitignored, a hand-run dated snapshot from 2026-08-19 predating this plan —
not the same artifact as `tools/suite_cost.py`, which is a script, not a
markdown render). This plan does not touch it and creates no naming collision;
flagged here only so a reader who greps for "suite-cost" is not confused by
the coincidence.

## Acceptance criteria

* **Tests that must pass**: `bootstrap/tests/test_suite_ledger.py` (Chunk C),
  encoding the following invariants from Revision 5's "Evidence" table as
  distinct falsifiers — named for the property each pins, not for the review
  round that produced it:
  - exit status and outcomes never change, fault-injected in each of the five
    hooks separately against a collector-disabled control;
  - a diagnostics fault never suppresses release evidence (inject with the
    ledger's own guards removed; both an `Exception` from the accumulator and
    a `BaseException` from the `sessionfinish` block; the `RELEASE MODE`
    report still prints with its nodeids and exit is still 1);
  - node accounting holds `0 <= executed <= collected` and reconciles against
    `terminalreporter.stats` under `-x`, `--maxfail=2`, `pytest.exit()`,
    `KeyboardInterrupt`, setup error, teardown error, and module-level skip;
  - `scope` classification: the canonical and order-independence invocations
    resolve `full`; `--ignore`, `--ignore-glob`, `PYTEST_ADDOPTS`, ini
    `addopts`, `-p no:python`, zero positionals, module-level skip, and
    `importorskip` each resolve `unknown`;
  - `scope` is re-derivable: the same invocation with and without
    `PYTEST_ADDOPTS` set produces rows differing in `scope_basis`, the
    reader's re-derived `scope` matches the stored value, and a deliberately
    wrong stored `scope` is reported by the reader as a disagreement;
  - a capped `scope_basis` forces `scope == "unknown"`;
  - `by_file` eviction preserves cost (a low-node/high-duration file survives
    ahead of a high-node/low-duration one), and summed-then-converted
    sub-millisecond durations are not lost to rounding;
  - the sanitizer is total across ASCII, non-ASCII, emoji, a lone surrogate,
    **and a mixed string**, and in each case **the intended sanitized and
    capped field survives** with the specified `truncated` value — **not
    merely that some valid line exists**. The survival half is the half that
    can fail: a sanitizer returning `""` for every non-ASCII input is total,
    and sets `truncated` correctly on every named case, so a criterion
    asserting only totality-plus-disposition admits an implementation the
    accepted contract rejects;
  - the skeleton row is total (forced non-finite timing still yields a
    written row);
  - the encoded budget holds — an oversized label, 64+ tokens, control
    characters, and **every real test-file path in `bootstrap/tests/`,
    enumerated at run time** all still produce exactly one line, ≤ 4096
    bytes, that round-trips through `json.loads`; the encoder call site
    matches the pinned signature exactly. **Registered as a live invariant,
    not a fixed count**: the accepted contract's evidence row quotes "all 115
    real paths", and this plan's own Chunk C adds `test_suite_ledger.py`,
    making that figure 116 the moment the falsifier is authored. A hardcoded
    count would be stale before it was first run, so the test enumerates the
    directory instead of asserting a number;
  - `head` resolves correctly in a linked worktree on a branch, in the main
    checkout, in a packed-refs checkout, and against a malformed `.git`
    (`null`, with a row still written);
  - containment: a ledger directory under `gettempdir()` via the unresolved
    `/var` spelling produces no row;
  - the lock is bounded (externally held lock: completion within 1s of a
    control, no row) and the tail is repaired (partial tail then normal
    append: the reader reports the fragment *and* returns the later row);
  - reentrancy: nested pytest writes nothing, two sequential
    `pytest.main()` calls write two rows, and a pre-existing marker survives
    across a child;
  - reader outcomes: the rendered output opens with the do-not-re-run
    instruction, reports `full` runs per day and not per plan, phrases
    overlap as "another recorded top-level session," surfaces a malformed
    line, states the lower bound, and reports dirty state as `unknown`.
* **Standing gates for the touched surface** (per Revision 5's own "Standing
  gates" line): `bootstrap/tests/test_gate_manifest.py`,
  `bootstrap/tests/test_gate_preflight.py`,
  `bootstrap/tests/test_security_check.py`,
  `bootstrap/tests/test_python_floor.py`.
* **Doc updates that must land**: the `.gitignore` rule (Chunk D1);
  `dev/measurement/README.md` **and** `templates/core/dev/measurement/README.md`
  (Chunk D2); `CHANGELOG.md > Unreleased > Added` (Chunk D3).
* **Two criteria that apply to D2 and to nothing else**, because it is the only
  row touching a shipped install destination: `diff
  templates/core/dev/measurement/README.md dev/measurement/README.md` produces
  no output, and `python bootstrap/verify_integrity.py` reports no hash
  mismatch for that destination once the lockfile hash is advanced. A D2 that
  edits one copy and not the other satisfies neither.
* **The D2 note names no Cairn-specific artifact.** It ships to every adopter,
  so a reviewer should read it as an adopter would: a reference to
  `suite-runs.jsonl` or `tools/suite_cost.py` in that file is a defect even
  though both are correct in Cairn's own tree.
* **Examples / smoke checks required**: **N/A as a separate artifact** — the
  reader-outcomes rows inside `test_suite_ledger.py` (Chunk C) are the smoke
  check for `tools/suite_cost.py`; no standalone example doc renders it.
* Inbound path-link updates: none — `PLANNING.md` and any `NEXT_SESSION.md`
  reference plans/proposals by filename stem, not path link, so the
  proposal-to-archive move needs no inbound-link repair.

### Author-accounting — invariants, failure modes, edge cases

**Invariants and their enforcing test** — each row above in "Tests that must
pass" is one invariant with its own falsifier; none is left as a bare "table
present" claim. **Public entry points this plan touches:**

* The pytest hook surface (`pytest_configure`, `pytest_runtest_logreport`,
  `pytest_collectreport`, `pytest_deselected`, `pytest_sessionfinish`) —
  exercised through its actual public path, in-process `pytest.main()` calls
  from `test_suite_ledger.py`, not by importing and calling hook functions
  directly.
* `tools/suite_cost.py`'s rendering entry point — exercised by the
  reader-outcomes falsifier importing it as a module against fixture ledger
  files.

**Security preflight (S1–S5) — re-answered only where chunking changes the
answer**, per Revision 5's own S1–S5 (unchanged in substance):

* **S2 (can it fail?)** — each invariant's falsifier lives in Chunk C, and the
  load-bearing ones derive their expectation from a collector-disabled
  control run, not from the collector's own output.
* **S3 (what fires it, over what?)** — the mutation (the write) is Chunk A's
  `pytest_sessionfinish` extension, firing on every non-child, non-release
  session under `bootstrap/tests/`, with no selector. The check that verifies
  it is the standing-gates list above plus `test_suite_ledger.py`, run via
  `python -m pytest bootstrap/tests`. Cairn has no CI; the trigger is a
  person or the goodnight routine.

S1, S4, and S5 are unchanged by this plan's chunking (the input sources, the
fail-toward-silence direction, and the no-new-execution-capability posture are
properties of the design, not of how it is sequenced into commits) and are not
re-derived here.

**Known omissions.** Carried forward from Revision 5's own `### Known
omissions`, and still omitted after this plan: dirty-tree state is deferred
behind its own Security Review and reported as `unknown` rather than as
measured; release-mode and nested sessions are unmeasured by design; **Windows
is unclaimed**; **network filesystems are excluded** — which is the stated
boundary on the `flock` durability contract this plan carries, not an
incidental gap; plan attribution is manual unless `CAIRN_SUITE_LEDGER_LABEL`
is set; in-process `pytest.main()` calls are treated as children; and the
session count is a **lower bound**.

**One omission this plan closes rather than carries.** Revision 5 lists
"collector overhead unmeasured **until implementation**" — an omission
explicitly bounded to end here. It is self-undermining to leave open: the
collector writes `wall_s` into a ledger the reader renders as the suite's
cost, so its own contribution to that figure must be quantified or the
headline number is unattributable. Chunk C's falsifier set therefore includes
a collector-disabled control run against a collector-enabled run over the same
selection, recording the delta; that control already exists in this plan's S2
answer above as the source of the load-bearing expectations, so the
measurement is a by-product of a run the plan already requires rather than new
work. If it cannot be produced, that is a blocking gap for the code reviewer,
not a silent carry-forward.

## Verification

**Boundary A (iteration, scoped).** Reviewed mapping, once Chunk C exists:
`bootstrap/tests/test_suite_ledger.py` plus the four standing gates named
above. **Chunks A and B land before that mapping exists** — there is no
reviewed test for the writer or the reader until Chunk C lands, so an
implementer iterating on A or B alone has, at minimum, the standing gates and
collection-still-succeeds as a floor; land A, B, and C close together in
practice rather than treating the gap as a place to skip iteration checking.

**Boundary B (integration, stable evidence) is `full` — not a choice, a
refusal.** `bootstrap/tests/conftest.py` is both a **contract surface** in the
sense the Boundary B rule cares about (gate-frozen, re-anchor-owed) and sits
under a **trust-ceremony surface** (Chunk E's Security Review + re-anchor
ceremony). `AGENTS.md`'s Boundary B rule refuses bounded mode on either
condition alone; this plan trips both, so **bounded mode is unavailable
regardless of how narrowly the diff can be mapped**, and this is declared now
rather than left for the implementer to discover and argue past at the
integration checkpoint.

**Boundary B mode: `full`.**

Commands (run once, against a clean, unchanged commit, under the canonical
interpreter — Python 3.13.x):

* `python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0`
* `python scripts/quality_gate.py --sub neutrality --sub redundancy`
* `python scripts/check_cairn.py`
* `python scripts/claim_check.py dev/plans/suite-run-diagnostics.md` (once per
  authored/revised plan text)

**The bare pytest form above is correct only until the sibling plan lands.**
`dev/plans/full-suite-interception.md` appends to `AGENTS.md` the sentence the
Maintainer's authorization quoted in this proposal's own Decision — "Boundary
B's canonical pair now requires `CAIRN_FULL_SUITE=1`" — and installs the guard
that enforces it. This plan sequences first, so at its own Boundary B the bare
form still runs. **Boundary C sits after code review**, with nothing fencing it
against the sibling landing in between: whoever runs it checks whether that
guard is in `bootstrap/tests/conftest.py` at the commit under review and
prefixes `CAIRN_FULL_SUITE=1` if it is. A run that comes back exit 4 with a
refusal message has been refused, not passed.

**Do not trust `claim_check` to catch a stale sibling path.** Its lifecycle
archive-fallback silently resolves a dead active path through the archived
sibling, so a citation of a proposal at its pre-archive path returns clean.
That is how the stale sequencing sentence corrected above survived the check
this plan ran before its own opening commit. The instrument cannot fail on
this class, so its clean result is not evidence about it.

Record the dated `## Implementation verification -- <agent> -- YYYY-MM-DD`
section per the template's mandatory fields (`Boundary B mode`, `Tested
commit`, `Reviewed range`, `Interpreter/runtime`, pre/post state, the command
table, non-pass disposition, known omissions) after the final implementation
commit (the end of Chunk D).

**Boundary C (falsification, independent)** is the code reviewer's job: verify
the Boundary B record against the reviewed range, then run independent
targeted falsification against the Evidence-table rows above — not a repeat
of the broad command.

**Trigger 5 does not fire here, and an earlier draft of this section wrongly
claimed it did.** The template's trigger 5 requires that the ceremony
"explicitly requires independent full execution"; `bootstrap/REANCHOR_RUNBOOK.md`
contains no reference to the suite, to a full run, or to pytest at all, so the
condition is unmet. Saying otherwise would tell the code reviewer a fresh full
run is mandatory regardless of their own judgement, on the strength of text
that does not exist. The reviewer decides under triggers 1-4 and 6 on what they
actually find — and **trigger 4 fires on its own terms** if review sharpening
changes any implementation, test, executable-template or fixture bytes in the
reviewed range, which for a chunked change of this size should be treated as
the expected case rather than the exception.

## Code review

*Filled in after implementation commits land.* See `doctrine/plans.md` >
"Code review" for the full doctrine: falsification ledger, coverage line,
reviewer identity (not the implementing agent), and the append-only rule.

Each pass is its own dated H2 section, `## Code review -- <reviewer> --
YYYY-MM-DD[ (round N)]`, and opens with the mandatory review basis on its own
lines above the pass's first `###` heading:

    Reviewed commit: <full commit id>
    Target: <the code range this pass reviewed>
    Prior findings: <ids being closed, or none>
    Assurance path: high-assurance

Then the reviewer identity line, the verdict, and the findings declaration.

**This code review is a separate obligation from Chunk E's Security Review.**
`AGENTS.md` > "Review" states a high-risk surface's Security Review trigger
is "untouched by" plan-review routing and is an explicit escalation, not a
substitute for the ordinary code-review floor; nothing in this plan collapses
the two into one pass. Both must land — code review before this plan reaches
`ready-to-archive` (the archive precondition), and the Security Review on the
Decision's own term — "implementation carries a Security Review trigger and
re-anchor ceremony".

**The Security Review has no mechanical enforcer, and this plan says so
rather than implying one.** An earlier draft of this section grounded it in
"a prerequisite the re-anchor ceremony's own runbook already imposes". That
was false, and checked: every occurrence of "Security review" in
`bootstrap/REANCHOR_RUNBOOK.md` governs the *ceremony machinery* — the
instantiated launcher and the checker bytes — and none of them governs the
implementation entering the anchor. The archive precondition in
`doctrine/plans.md` requires a **code** review only. So the Security Review is
enforced by this plan's Chunk E1 gate and by nothing else; if E1 is skipped,
no tool, test, or precondition anywhere will notice. Treat E1 as
load-bearing, not as a restatement of a control that already exists.

## Chunk E — Security Review + re-anchor ceremony (Maintainer-owned)

Neither the Security Review's scheduling, the batching decision, nor the
ceremony itself is this plan's or any implementing agent's act to perform
unsupervised. The implementer's job ends at Chunks A–D landing clean and the
Boundary B full run recorded.

**E1 — Security Review (may be performed by any capable agent filling that
role; not gated on the Maintainer to *start*).** A focused-mode pass per
`dev/modules/security-review.md`'s trust-boundary checklist, over the exact
final bytes of Chunks A–D after code review has stabilized them (re-reviewing
bytes that later change is wasted work) — the direct `.git`/`HEAD`/refs reads,
the write path derived from the conftest's location, the five guards'
fail-toward-silence behaviour, and the sanitize/cap logic on attacker-influenced
strings (paths, argv tokens, resolved targets). This mirrors Revision 5's own
"S5 — who still wins?" framing: the assumed attacker already runs arbitrary
code in the suite; the review's job is confirming the write adds no new
capability and that write-path targeting is closed by enumeration, not merely
asserted.

**E2 — MAINTAINER-GATED: the batching decision.** `dev/PLANNING.md` > "Queued"
already carries an owed re-anchor for an unrelated reason: the AST attestation
baseline row (filed 2026-08-19) reports 13 CHANGED symbols against the
committed baseline (11 in `bootstrap/_scaffold/upgrade.py`, 2 in
`bootstrap/_scaffold/config.py`), not self-serviceable per
`_ast_attest._UPDATE_ALLOWLIST`, procedure at `bootstrap/AST_BASELINE_RUNBOOK.md`.
Landing this plan's Chunk A adds a second, independent trigger for the same
kind of ceremony (a `FROZEN-MODIFIED` entry on `bootstrap/tests/conftest.py`,
this time via the differential-oracle gate rather than the AST baseline). **One
re-anchor covering both is the natural shape** — the same supervised ceremony
already re-derives the expected CHANGED set at ceremony time regardless of how
many triggers fed it — but this plan does not decide that for the Maintainer;
it presents the fact and leaves the batch/split call, and its timing, to
`bootstrap/reanchor.sh`'s operator.

**E3 — MAINTAINER-ONLY: the ceremony itself.** `bootstrap/reanchor.sh` per
`bootstrap/REANCHOR_RUNBOOK.md` — the instantiated launcher, the values file,
the dedicated ceremony key, and the candidate ref are all Maintainer-held
prerequisites this plan does not and cannot supply. Advances the one
designated ref, `refs/cairn/gate-anchor`, by the runbook's expected-old
compare-and-swap. Not performed by an implementing agent under any
circumstance (precedent: `c3d5bd9`, cited in `AGENTS.md` > "AST attestation
baseline").

## Not settled by the proposal — flagged, not papered over

* **Which single test file carries the reader-outcomes falsifier.** Revision
  5 commits to exactly one new test file but its Evidence table names a
  reader-only falsifier row; the proposal text never states where that row
  lives given the reader is outside `bootstrap/tests/`. This plan resolves it
  (Chunk C, importing `tools/suite_cost.py` as a module) rather than leaving
  it for the implementer to discover mid-chunk. A plan reviewer who disagrees
  with folding the reader's test into the writer's contract file — e.g.
  preferring a second file and treating "one new test file" as descriptive
  rather than a hard cap — should say so as a finding; the proposal record
  does not settle which reading is correct.
* **Whether `tools/suite_cost.py` is adopter-facing.** Revision 5's Scope
  says "excluded: … any … adopter surface" but never states the mechanism by
  which a new file under `tools/` avoids becoming one, and `tools/` in this
  repository is otherwise entirely a mapped install target. This plan decided
  the mechanism (no `config.py` entry) by analogy to `scripts/quality_gate.py`
  / `scripts/check_cairn.py`, not by proposal instruction.
* **Whether Chunk E's Security Review and the plan's ordinary code review are
  one pass or two.** `AGENTS.md` states the Security Review trigger is
  untouched by plan-review routing and is an "explicit escalation," which
  this plan reads as *additional to*, not a substitute for, the standard
  code-review floor — but neither the proposal nor the Decision states this
  in so many words for *this specific* pairing of triggers. Recorded as a
  plan-authoring judgement call, not a proposal citation.
* **Whether E2's batching actually happens**, and if so its exact timing
  relative to the AST-baseline ceremony, is explicitly left to the Maintainer
  per the plan's own MAINTAINER-GATED fence — this plan presents the fact,
  not a recommendation binding on anyone.

## Internal inconsistency noted in the accepted contract

None found at the level this plan operates on. Revision 5's own "Section
inventory carried forward from Revision 4" mechanism (an explicit
carry-forward ledger checked against the prior revision) is itself evidence
the proposal's review history already hunted for, and caught, exactly this
kind of silent regression twice (E19's dropped sections, E20's non-reproducible
`scope` distinction) before Revision 5 shipped. Nothing surfaced in reading
Revision 5 end-to-end, the Decision, or the two ratifying review passes
(Codex External at `64830d961f378a72e3f16a5313abfb9bb7f0891e`; the Maintainer's
Decision and amendment) that contradicts another part of the same set. The two
items above are gaps — things the contract leaves unstated — not
contradictions within it.

## Lasting-truth migration

*Filled in at archive time.* See `doctrine/plans.md` > "Lasting-truth
migration doctrine" for the full rule: the disposition vocabulary, the
`Dispositions:` commit-body form, the evidence ledger, and the loop-fidelity
sign-off.

**The archive gate now checks substance, not the label.** An attestation is
required **every time**: either at least one entry naming `accept`, `guard`,
`wontfix` or `defer`, or the explicit form `Dispositions: none` on its own
line when there are genuinely no follow-ups.

The loop-fidelity sign-off must sit **inside this section** and name at least
one implementing commit id plus the governing accepted/Revised section.
Promising that it is owed does not satisfy it.

This section is append-only once written.

## Plan review -- Claude Opus 5 (Internal, fresh context) -- 2026-08-20

Reviewed commit: 86adf62dbc63e0c43eeea7f83cbd4f53f1456306
Target: the plan in full — Source proposal and tier rationale, Proposed paths, Scope
(including both scope-adjacent decisions and the Maintainer allowance), Sequence and
Chunks A–E, Acceptance criteria, Author-accounting, Verification (Boundaries A/B/C),
Code review, and "Not settled by the proposal" — read against Revision 5 (`~2172-2444`),
its final External review, and the Decision of the accepted source proposal
`2026-08-19-claude-suite-run-diagnostics`
Prior findings: none
Assurance path: high-assurance
**Tier**: Internal
**Findings**: raised

**Model**: Claude Opus 5 (`claude-opus-5`).

**Note on the independence checker.** `python tools/lifecycle_planner.py scan` compares
the byline's *first word* against the author's, and Cairn's Internal floor is "the same
agent in a fresh session" — so an honest Internal byline collides by construction. This
review will read as author-written to that checker. It is not: this is a fresh context
that did not author the plan and will not implement it. The defect is filed in
`dev/PLANNING.md` as a `[TOOL]` row. Declaring a byline that is not mine to silence a
known checker defect would put a false attribution on the one record whose integrity
*is* its attribution.

**Verdict: REVISE.** → `revising-plan`.

This is a careful plan. Its scope fidelity is good — I mapped all twenty rows of
Revision 5's Evidence table and all eleven accepted reader outcomes into the plan's
Acceptance criteria and Chunk B, and found none dropped; two proposal rows are merged
into neighbouring bullets (sub-millisecond conversion into the `by_file` bullet, encoder
pinning into the budget bullet) but neither is lost, and three rows are *strengthened*
past the accepted falsifier. Its three "Not settled by the proposal" disclosures are
honest, its citations check out (I opened `plan_inheritance_violations` at
`tools/lifecycle_planner.py:3608-3614`, confirmed `bootstrap/tests/conftest.py` is in
`_gate_manifest._frozen_files()`'s 203-entry set, confirmed
`bootstrap/REANCHOR_RUNBOOK.md` contains zero references to pytest/the suite/a full run
and that all four of its "Security review" occurrences govern ceremony machinery, and
confirmed the byte-identity of the `dev/measurement/README.md` twin), and
`python scripts/claim_check.py` on it is clean.

It blocks on something narrower and harder: **Chunk C is not constructible as
specified.** The accepted design's own guards close every route a test inside
`bootstrap/tests/` has to observe a written ledger row, and the one falsifier that pins
the classifier's positive case has no admitted route at all. That is not a polish
finding — an implementer meets it in the first hour of Chunk C, and the path of least
resistance from there writes test rows into the live ledger this plan exists to produce.
Findings PR1 and PR2. PR3 and PR4 are independently blocking; PR5–PR7 are substantive;
PR8–PR10 are minor.

### Blocking findings

**PR1 — Chunk C's write-observing falsifiers have no constructible mechanism, and the
plan names none while asserting the opposite as settled.**

Three of the accepted guards jointly close every route:

* **Guard 2 (reentrancy with ownership).** The parent session claims
  `CAIRN_SUITE_LEDGER_SESSION=1` in `pytest_configure`; a pre-existing marker means
  child. So an in-process `pytest.main()` — the public path this plan's Author-accounting
  explicitly declares — is a child of the running suite and writes **nothing**. Revision
  5's Known omissions say so outright: "in-process `pytest.main()` treated as children."
* **Guard 3 (containment).** The ledger directory is derived from the conftest's location
  (Revision 5, S5), so a fixture tree under `tmp_path` puts it under the resolved
  `tempfile.gettempdir()`. Measured on this host: `gettempdir()` resolves to
  `/private/var/folders/.../T`, and a `mkdtemp` sample resolves beneath it. Guard 3
  skips → no row. This is not incidental: it is exactly the property the containment
  falsifier is written to prove.
* **Guard 5 (opt-out).** No-op when `dev/measurement/` is absent — which it is in any
  fresh fixture tree.

The only directory that satisfies all three is the repository's own `dev/measurement/`.
Under `bootstrap/tests/fixtures/` (which already exists) Cairn's conftest applies to the
whole subtree, so the naive construction writes test rows into the live
`dev/measurement/suite-runs.jsonl` — contaminating the artifact `tools/suite_cost.py`
renders, in a plan whose headline output is a cost figure.

The contract offers no escape. Its complete environment surface is three names —
`CAIRN_SUITE_LEDGER`, `CAIRN_SUITE_LEDGER_SESSION`, `CAIRN_SUITE_LEDGER_LABEL` — and none
redirects the write path. **Adding one is a contract expansion**, not an implementation
detail: it re-opens S5's load-bearing claim that "write-path targeting [is closed] by
enumeration", and would take a Maintainer allowance plus a Security-Review re-read, not
a plan-authoring judgement call.

Two aggravating facts the plan should carry:

* The plan's Author-accounting states the hooks are "exercised through its actual public
  path, in-process `pytest.main()` calls from `test_suite_ledger.py`". Under guard 2 that
  path writes nothing. Every falsifier that asserts a row must therefore run under a
  **doctored** environment (marker cleared, and containment or the derived path
  suspended) — which is a defensible mechanism but is not "the actual public path", and
  which changes what the collector-disabled *control* runs are controlling for.
* There are currently **zero** `pytest.main(` call sites anywhere in `bootstrap/tests/`.
  This is a new harness pattern with no precedent in the tree to copy, asserted as
  settled.

**Ask.** Name the mechanism, per falsifier class, in the plan — not at implementation
time. For each class say which guard it suspends, how (monkeypatch target, env
manipulation, non-temp scratch root), and why suspending that guard does not invalidate
that falsifier. In particular the containment and reentrancy falsifiers must **not** run
under a suspended guard 3 or a cleared marker, or they prove nothing. If the chosen
mechanism is a contract-level path override, say so and take it to the Maintainer.

**PR2 — the `scope == "full"` falsifier is unconstructible, and every escape closes on
the classifier's own rules.**

Acceptance bullet 4 requires "the canonical and order-independence invocations resolve
`full`". Revision 5 makes `full` require **both** channels: channel 1, the raw invocation
is a member of an exact closed argv family (the canonical command, or the
order-independence command with its four known display/shuffle options — *any* other
token yields `unknown`); and channel 2, the resolved postconditions, including
`scope_basis.targets` resolving to the suite root, `deselected == 0`, `not_run == 0`,
`collected > 0`, `executed > 0`, `interrupted` false.

Targeting the suite root from a test that lives in the suite root re-collects
`test_suite_ledger.py`, which runs the nested invocation again: **non-terminating
recursion**. Every way out is closed by one channel or the other:

* `--ignore` / `--ignore-glob` / `-k` / `-m` — not in the closed family → channel 1 →
  `unknown` (the proposal names `--ignore` and `--ignore-glob` explicitly).
* `--deselect` — `deselected != 0` → channel 2.
* a module-level skip on the recursing module — on the proposal's own `unknown` list in
  the same Evidence row.
* a custom env marker making the module skip itself in the child — lands back on the
  module-level-skip case.
* a subprocess — excluded by Revision 5's Scope, and **this plan already reads that
  exclusion as binding on tests**: it chose to import `tools/suite_cost.py` as a module
  rather than shell out to it, "consistent with 'zero subprocesses'".
* a copied suite root under `tmp_path` — argv is a temp path, not the canonical command
  (channel 1), and guard 3 suppresses the row anyway (PR1).

So the single falsifier that pins the classifier's **positive** case — the one that
separates "resolves `full` correctly" from "never resolves `full`" — has no route this
plan admits. Note the asymmetry this creates: an implementation that returns `unknown`
unconditionally satisfies every one of the eight negative cases in the same bullet, plus
the capped-basis bullet, plus the re-derivation bullet (a stored `unknown` and a
re-derived `unknown` agree). Without a working positive case, the `scope` classifier is
pinned only against over-claiming, never against under-claiming — and under-claiming is
the failure that makes the whole ledger useless, because no run is ever counted as a
full run.

**Ask.** Either name a concrete construction for the positive case, or state plainly that
it cannot be produced in-process and take the remedy to the Maintainer. Dropping the row
is a **scope reduction** against an accepted Evidence row — `AGENTS.md` is explicit that
a plan may not draw that fence for itself and that a reviewer cannot create the authority
by calling it out of scope, so I am not offering it. Record it as `Scope delta: degraded`
with a Maintainer allowance if that is where it lands.

**PR3 — `bootstrap/verify_integrity.py` is named as a check for D2 and does not check
the claimed property. The command as written cannot run at all.**

The criterion under Acceptance is: "`python bootstrap/verify_integrity.py` reports no
hash mismatch for that destination once the lockfile hash is advanced." Opened and run:

* **(a) The command exits 2.** `--target` is `required=True`. Measured:
  `python3 bootstrap/verify_integrity.py` → `error: the following arguments are
  required: --target`, exit 2. As written it verifies nothing, ever.
* **(b) It is blind to the property D2 is about.** It compares on-disk bytes to
  `dev/.cairn/cairn-lock.yml`. The record is `dst: dev/measurement/README.md`,
  `src: core/dev/measurement/README.md`, `hash: sha256:726ee2b8…` — the hash of the
  **installed** copy. The checker never reads `templates/core/**`. So it cannot detect
  twin desync in either direction, and editing **both** copies byte-identically fails it
  exactly as editing one does. The plan's stated rationale — that editing Cairn's copy
  *alone* "leaves the tree failing `bootstrap/verify_integrity.py`" — attributes to this
  tool a discrimination it does not have.
* **(c) "once the lockfile hash is advanced" names no owner and no chunk.** Nothing in
  Chunks A–E advances it. The plan's own prose says the state persists "until an
  `upgrade --finalize`" — a command no chunk runs, no acceptance criterion names, and no
  fence assigns.
* **(d) The baseline is already red.** `python3 bootstrap/verify_integrity.py --target .`
  on the current tree reports 2 violations (`dev/plans/_template.md`,
  `docs/DOCUMENTATION_PLAN.md`) and exits 1. An implementer handed "reports no hash
  mismatch" meets a failure they cannot clear and that has nothing to do with D2.

**And there is no substitute gate.** I looked for one. The suite's generic twin-parity
gate is `bootstrap/tests/test_notice_install.py::test_every_self_hosted_twin_stays_byte_identical_to_its_source`,
and `_self_hosted_twins()` globs `*.py` under `scripts/`/`tools/` only — a gap already
documented in this tree at `bootstrap/tests/test_portable_security_sweeps.py:2286-2291`
("the suite's generic twin-parity helper globs `*.py` only -- a real, measured gap").
Nothing anywhere enforces `.md` twin parity.

**Ask.** Drop the `verify_integrity` clause or replace it with the invocation and the
scope it actually has. D2's real protection is the `diff` command in the criterion above
it plus reviewer attention — say that plainly. This repository's own rule is that a tool
returning success without testing the claimed property is worse than no tool; here the
tool cannot even return success. This is the third instance of the pattern in this plan,
after the two it already documents and withdraws (trigger 5 / `REANCHOR_RUNBOOK.md`, and
the Security Review's non-existent mechanical enforcer). The plan's instinct to name a
mechanism is right; the habit that needs adding is opening the mechanism before naming it.

**PR4 — the encoded-budget criterion is satisfied by an implementation that always emits
the skeleton row.**

The bullet asks that an oversized label, 64+ tokens, control characters, and every real
test-file path "all still produce exactly one line, ≤ 4096 bytes, that round-trips
through `json.loads`". The accepted design has a **total** skeleton fallback: `label`,
`invocation` and `scope_basis` null, `by_file` empty, `truncated` true, `scope` unknown,
measured at 451 bytes. An encoder that skeletonizes **unconditionally** satisfies every
clause on every named case, on the first try, forever.

This is the identical failure the plan catches one bullet earlier and fixes for the
sanitizer — *"a sanitizer returning `""` for every non-ASCII input is total, and sets
`truncated` correctly on every named case, so a criterion asserting only
totality-plus-disposition admits an implementation the accepted contract rejects."* The
reasoning is right and was not carried across to its neighbour.

**Ask.** Add the survival half: for the cases that fit within budget, `truncated` is
false and the intended `label`, `invocation` and `by_file` content is present in the
decoded row; the skeleton appears only where the budget genuinely forces it. The
`by_file` eviction bullet needs the same read — "eviction preserves cost" is directional
and fine, but pair it with the assertion that eviction happens only when required.

### Substantive findings

**PR5 — "reconciles against `terminalreporter.stats`" is undefined, and it is the only
directional half of a criterion this repository has already been burned by.**

Acceptance bullet 3 is `0 <= executed <= collected` plus reconciliation, across seven
abort shapes. The inequality is the weak half by construction, and the sibling plan
demonstrates it concretely: `full-suite-interception` shows a refused session produces
`(executed=0, collected≈4,443)`, satisfies the inequality, and "cannot catch this". So
the criterion's entire discriminating power sits in the word "reconciles" — which neither
Revision 5 nor this plan defines. An implementer may satisfy it with a tautology.

**Ask.** State the relation concretely, e.g. `executed` equals the count of distinct
nodeids with ≥1 runtest report derived from `stats`, and each of the seven outcome counts
equals its corresponding `stats` bucket size, per shape. The plan's own criterion for
naming falsifiers — "name any criterion a wrong implementation would satisfy" — applies
here more than anywhere.

**PR6 — the sequencing seam: whatever form PR2's `full` falsifier takes, the sibling
breaks it, and neither plan owns the repair.**

`dev/plans/full-suite-interception.md` row A1 refuses the canonical Boundary B argv
(`pytest.UsageError`, exit 4), and row A6 makes the sibling's classifier resolve a refused
session `unknown` rather than `full` — under a Maintainer allowance, correctly. That is
precisely this plan's acceptance bullet 4 inverted: any `full` falsifier that exercises
the canonical argv against the suite root becomes a refusal after the sibling lands and
resolves `unknown`, failing this plan's own criterion.

The sibling has no declared authority to repair it. Its Proposed paths record
`bootstrap/tests/test_suite_ledger.py` as "the sibling plan's contract-test file, likewise
created there and only *read* here"; its Boundary A mapping runs the file but does not
claim the right to edit it. So a break lands in a gap between two plans, discovered at
the sibling's Chunk A.

This plan lands first and is the cheap place to close it. **Ask.** State in the
sequencing section that the `full`-classification falsifiers must be constructed so the
sibling's guard cannot perturb them — carrying `CAIRN_FULL_SUITE=1`, which is inert today
and correct after the sibling lands, is the obvious candidate and costs nothing now — or
hand the seam to the sibling explicitly so it can declare the file as touched. Do not
leave it implicit; the sibling's own author found this class of cross-plan defect only by
looking for it.

**PR7 — the one omission the plan claims to close is bound by no acceptance criterion.**

Revision 5's Known omissions bound collector overhead to "unmeasured **until
implementation**". The plan says it closes it via "a collector-disabled control run
against a collector-enabled run over the same selection, recording the delta", and argues
"the measurement is a by-product of a run the plan already requires."

It is not a by-product. The S2 control establishes **outcome** expectations — exit status,
node counts, release evidence. An outcome comparison yields no timing delta. To produce
one you need repetitions, a selection, a noise floor and a stated method, none of which
the plan gives. And nothing binds it: there is no bullet in "Tests that must pass", no
artifact named, no field named — while the paragraph tells the code reviewer that failure
to produce it "is a blocking gap". That is an obligation with no defined deliverable,
which is the same shape as the named-trigger defect in PR3 one level up.

Note the schema already has the obvious home: `collector_ms` is a pinned field in
Revision 5's row schema, and neither the proposal nor this plan has a falsifier for it —
the plan's Chunk A3 summary does not name it either.

**Ask.** Bind it: an acceptance-criteria bullet naming the method, the selection, the
repetition count, and where the number is recorded (the `## Implementation verification`
section is the natural place). Add a falsifier that `collector_ms` is populated and
consistent with the observed delta. If it cannot be bound, it is still an open omission
and should be carried as one rather than declared closed.

### Minor findings

**PR8 — Chunk B's "not shipped" property gets a one-shot manual check where the repo
already has a standing test for exactly that property.**

The criterion is "`bootstrap/scaffold.py --manifest` must show no `tools/suite_cost.py`
row **after this chunk lands**" — a single observation at landing time. The analogy the
plan draws is right but incompletely read: `scripts/quality_gate.py` and
`scripts/check_cairn.py` are not protected by having been checked once. They sit in
`_OWN_ONLY_SCRIPTS` in `bootstrap/tests/test_notice_install.py`, and
`test_own_only_dev_scripts_are_not_shipped` re-asserts zero manifest rows for each on
every run. Extending that roster (or adding a `tools/` arm to it) converts the plan's
promise into a standing gate for about three lines.

Related, from the same file: `test_own_only_dev_scripts_carry_spdx_header` requires an
SPDX MIT header on Cairn's own non-shipped dev tooling, and `AGENTS.md` > High-risk
surfaces makes "code is MIT wherever it lives" a licence-split obligation. Chunk B says
nothing about the header. I confirmed no *existing* test breaks without it —
`_self_hosted_twins()` only sees manifest-mapped destinations, so an unmapped
`tools/suite_cost.py` is invisible to it — which is exactly why it should be added to the
roster rather than left invisible.

**PR9 — E2's AST-baseline figure is stale within its own cited source.**

E2 cites `dev/PLANNING.md` > "Queued" as reporting "13 CHANGED symbols (11 in
`upgrade.py`, 2 in `config.py`)". The Queued row does say that. But a later entry in the
same file (under "Migrated Cairn roadmap") records **37 CHANGED symbols across 74 node
lines, `as_of 2026-08-19` at `f129178`, explicitly "up from 13"**, with a seven-file
breakdown — `upgrade.py` 26, `install.py` 18, `slotmerge.py` 10, `merge.py` 8,
`config.py` 6, `lockfile.py` 4, `security.py` 2.

E2's job is to show the Maintainer the size of the batch they are being asked to
disposition. Presenting 13 understates it roughly threefold, and names two files where
the later record names seven. `AGENTS.md` > Operational pitfalls says to derive the set
against the committed baseline rather than carry a figure forward, "including from that
runbook" — a roadmap row is the same hazard. The sibling plan handles the analogous
situation well ("A Maintainer walking into Chunk D expecting two entries would meet four
holds and one note").

**Ask.** Cite both and say which is current, or drop the figure entirely and cite only
the derivation procedure. Either is fine; presenting the stale one as the fact is not.

**PR10 — the bounded-lock criterion tests only the ceiling.**

"the lock is bounded (externally held lock: completion within 1s of a control, no row)"
is satisfied by an implementation with **no retry loop at all** — a zero deadline
completes instantly and writes no row. Nothing pins the other direction: that a lock
released *within* the 250 ms deadline yields a row. The retry loop, which is the part of
the durability contract that does work, is therefore unfalsified. Add the companion case.

### Things I checked and found correct

Recorded because a reviewer's silence is not evidence they looked.

* **Scope fidelity.** All twenty Evidence rows and all eleven accepted reader outcomes
  are present. Nothing accepted is dropped. Three falsifiers are strengthened past the
  accepted text (`head` in the main and packed-refs checkouts moves from "assert a row"
  to "resolves correctly"; the sanitizer gains its survival half; the 115-path count
  becomes a run-time enumeration) — all improvements, none a contract change.
* **The two Maintainer allowances.** The `Contract expansion: adopter surface` for
  `templates/core/dev/measurement/README.md` is quoted verbatim and visually isolated, and
  its coverage is stated rather than assumed. The `required(Internal)` declaration with
  **no** `Inherited proposal basis:` line is the only correct form: I read
  `plan_inheritance_violations` at `tools/lifecycle_planner.py:3608-3614` and the
  `_PLAN_READINESS_DISTINCT` branch does hard-refuse the pairing, exactly as the plan
  says.
* **Boundary B = `full`.** The reasoning holds independently on both stated grounds.
  `bootstrap/tests/conftest.py` is in `_gate_manifest._frozen_files()` (verified: 203
  entries, `bootstrap/tests/conftest.py` among them), and Chunk E is a trust ceremony.
  `AGENTS.md`'s fence refuses bounded mode on either alone.
* **Trigger 5.** Correct, and correctly withdrawn: `bootstrap/REANCHOR_RUNBOOK.md`
  contains **zero** case-insensitive matches for pytest / "full run" / "full suite" /
  "test suite", and all four "Security review" occurrences govern the instantiated
  launcher and the checker bytes, never the implementation entering the anchor.
* **The `tools/` install-surface reading.** `--manifest` emits 23 `tools/` rows covering
  every existing `.py` there; `dev/measurement/README.md <- core/dev/measurement/README.md
  substituted` is a real install destination; `bootstrap/tests` has **0** manifest rows;
  the twin is byte-identical today. The `scripts/quality_gate.py` /
  `check_cairn.py` precedent is real (both are in `_OWN_ONLY_SCRIPTS` and pinned unshipped).
* **`claim_check`.** Clean on this plan, exit 0, with the `Proposed paths:` /
  `Untracked paths:` exemptions resolving as declared. The plan's warning that
  `claim_check`'s archive fallback cannot fail on a stale sibling path is a good instance
  of confirming the instrument before trusting an absence.
* Structural claims about the current `conftest.py` (five hooks, `_release_mode`,
  `_record_refused_report`), the `.gitignore` rule shape, `CHANGELOG.md > Unreleased >
  Added` (present at line 60), `dev/measurement/README.md`'s "What belongs here" heading,
  the pre-existing gitignored `dev/measurement/suite-cost.md`, and
  `dev/modules/security-review.md`'s focused mode and trust-boundary checklist — all
  verified present and as described.

### Sharpening

**Scope delta**: preserved.

Nothing in this review narrows what the plan delivers. PR2 and PR7 push in the opposite
direction: PR2 refuses to concede a `full`-classification falsifier that only the
Maintainer may concede, and PR7 asks that a claimed closure be bound rather than dropped.
PR1, PR3, PR4, PR5 and PR10 ask for mechanism and falsifiability the accepted contract
already implies. PR6, PR8 and PR9 ask for accuracy in text that will be read by someone
acting on it.

### Coverage

**Read in full**: the plan under review; `dev/plans/full-suite-interception.md`;
Revision 5 of the source proposal (`~2172-2444`), its final Codex External review, and
the Decision; `dev/plans/_template.md` lines 360-564 (the four-field basis, the
inheritance two-field rule, the SCOPE DELTA block, the six code-review triggers, the
lasting-truth rules); `AGENTS.md` (auto-loaded, re-read deliberately at the named
sections); `bootstrap/verify_integrity.py`;
`bootstrap/tests/test_notice_install.py`.

**Opened as check targets**: `dev/.cairn/cairn-lock.yml` (the `dev/measurement/README.md`
record); `bootstrap/tests/_gate_manifest.py::_frozen_files`;
`tools/lifecycle_planner.py:3595-3616`; `bootstrap/REANCHOR_RUNBOOK.md` (greps for
pytest / full run / "Security review" with context);
`bootstrap/tests/test_portable_security_sweeps.py:2280-2310`;
`dev/modules/security-review.md`; `dev/PLANNING.md` (the Queued `[VER]` AST row, the
migrated-roadmap AST record, and the Archive-preconditions section); `CHANGELOG.md`
(Unreleased subsections); `dev/measurement/README.md`; `.gitignore`;
`bootstrap/tests/conftest.py`.

**Ran** (read-only, no suite run): `python scripts/claim_check.py
dev/plans/suite-run-diagnostics.md` (clean); `python tools/lifecycle_planner.py scan`;
`python bootstrap/scaffold.py --manifest` (grepped for `tools/`, `scripts/`,
`bootstrap/tests`, `measurement`); `python bootstrap/verify_integrity.py` bare (exit 2)
and `--target .` (exit 1, 2 pre-existing violations); a `tempfile.gettempdir()` /
`mkdtemp` containment probe; `diff templates/core/dev/measurement/README.md
dev/measurement/README.md` (no output); a grep for `pytest.main(` across
`bootstrap/tests/` (zero call sites).

**Not read**: Revisions 1-4 of the source proposal and the earlier review rounds, except
through Revision 5's carried section inventory and the per-Response withdrawal ledgers —
so a commitment withdrawn and *not* recorded in a ledger would have escaped me;
`doctrine/plans.md` and `doctrine/dual-review.md` in full (grepped for the archive
precondition and the plan-readiness rules only); `bootstrap/reanchor.sh` and
`bootstrap/AST_BASELINE_RUNBOOK.md` bytes; the other 200 entries of the frozen-file set;
`scripts/quality_gate.py`'s neutrality/redundancy internals (I relied on the sibling
plan's measured `_NEUTRALITY_FILE_SUFFIXES` finding rather than re-measuring, and it does
not bear on any finding above).

**Not done, by constraint**: no test-suite run — Cairn's rule is that verification is not
delegated, and no implementation exists to run against. Every claim above is from static
reading or a targeted read-only probe of *existing* code, and each probe's output is
quoted or characterized where it carries a finding.

**Out of scope by construction**: I did not re-litigate the accepted design — the five
hooks, the guard set, the 4,096-byte budget, the `flock` durability contract, the
`scope_basis` mechanism, or the Internal plan-review tier. PR2 questions whether an
accepted falsifier is *constructible*, not whether it is correct.
