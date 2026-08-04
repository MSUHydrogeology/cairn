<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/dual-review.md doctrine/lifecycle.md doctrine/rationale.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- cairn-accept: instruction-html-comment reason="The comment below is an explanatory note to human readers and to the claim checker about two deliberately non-resolving probe paths; it carries no directive to an agent and names no action to take." reviewer="Claude (author)" date=2026-08-03 -->
<!-- Two paths below are DELIBERATELY non-resolving: they are the throwaway
     probe files the Chunk C perturbations create and delete (`templates/optional/rogue.py`
     inside a tmp_path tree, `templates/_probe.py` transiently in the working tree).
     Neither is ever committed, so neither will ever resolve -- they are not
     forward references and must not be registered under `Proposed paths:`. -->
<!-- claim-check-allow: templates/optional/rogue.py, templates/_probe.py -->

# Plan: the release scan reaches every shipped Python file — and its guard can fail

**Source proposal**: `scan-coverage` (accepted 2026-08-03 by Maintainer Decision,
*"as revised"*). It currently sits under `dev/proposals/` and moves to
`dev/proposals/archive/` when it archives.
**Status**: archived
**Plan review**: required(**External**, security lens) — carried from the
proposal header, where the tier is the *declared trigger* rather than a judgement
call (`dev/proposals/_template.md`'s triage list names both touched security
files). The proposal's own External round returned SHIP **against a version of
item 3 that the author addendum then superseded**; the Decision says so in terms
and routes the replacement here. **No implementation commit lands before the
`## Plan review` section is in the tree.**
**Last update**: 2026-08-03
**Opened**: 2026-08-03

## Source proposal

`scan-coverage` settles one contract: **the release Bandit scan covers every file
the scaffold ships as byte-for-byte Python, derived from the published install
manifest rather than from a hand-picked subset of the registries behind it.**
The plan executes that decision and does not re-litigate it.

The proposal went through an External security review (SHIP, four verifications),
an author addendum that turned the proposal's own acceptance criterion back on
its own regression test and found the test cannot fail, an author Response to the
External round, and an Internal security review with eight findings. The Decision
accepted it *as revised*.

### Glossary — every term glossed on first use

The audience is a scientist who codes; this scope is jargon-dense and half of it
is about a distinction that is easy to nod at and hard to hold.

* **Bandit** — a code-security linter. It reads Python source and reports
  patterns associated with vulnerabilities, each carrying a *severity*
  (LOW / MEDIUM / HIGH) and a *confidence*. Cairn's gate blocks on MEDIUM+.
* **The release gate** — `bootstrap/security_check.py`, run before cutting a
  release. It is **fail-closed**: a missing Bandit, a scanner error, or any
  unallowlisted MEDIUM+ finding is a non-zero exit.
* **The dev gate** — `bootstrap/tests/test_security_lint.py`, the same scan
  driven from the test suite. It *imports* the release command's target set and
  allowlist so the two cannot drift apart.
* **Delivery registry** — a module-level data structure in
  `bootstrap/_scaffold/config.py` saying "install this template file to that
  path in the adopter's repository". There are four that reach the manifest
  (`_CORE_MAPPINGS`, `_SKILLS_MAPPINGS`, `_ALWAYS_ON_MAPPINGS`,
  `_MODULE_MAPPINGS`) and one that does not (`_OPTIONAL_TEMPLATES`).
* **The install manifest** — `install_manifest()` in
  `bootstrap/_scaffold/install.py`, which unions the four registries and emits
  `(source relative to templates/, destination, verbatim)`. It is the same
  enumeration adopters depend on through the published `scaffold.py --manifest`
  contract.
* **Verbatim** — copied byte-for-byte, with no `{{token}}` substitution. The
  opposite is **substituted**. Only verbatim files are Python that ships
  unchanged; a substituted `.py` would be a template, not a program.
* **Oracle** and **subject** — a test is an oracle plus a subject. The *oracle*
  states what ought to be true; the *subject* is the code being checked. When the
  oracle is computed from the same object the subject reads, the test can check
  that the subject *consumes* that object correctly but never that the object is
  *complete* — a gap moves both together and the difference between them stays
  empty. This distinction is the whole of Chunk C.
* **Frozen file** — a file whose sha256 is pinned in
  `bootstrap/tests/fixtures/gate_manifest.json`. During an active gate batch
  window, editing one HOLDs by default.
* **Perturbation** — a deliberate change to repository state that a regression
  test is claimed to detect. This repository accepts a regression test only when
  its author can name a future state in which it fails **and has run** the change
  that produces that state.

### What "as revised" is read to mean, and where that reading could be wrong

The Decision quotes the Maintainer verbatim — *"I approve each of the seven
proposals that you have listed as ready to accept, as revised"* — and no author
Response to the Internal review exists. So the phrase *as revised* has to be
interpreted before this plan can have a scope. This plan reads it as covering,
in order of how safe the reading is:

1. **Proposal items 1 and 2** (the manifest union; the fail-closed wrap on a
   refusing manifest) — untouched by every reviewer, verified by three parties.
   No interpretation needed.
2. **The author addendum's replacement of item 3** (split-and-rename the
   conformance test; add an oracle the code does not read; the acceptance
   criterion that a regression test needs a *run* perturbation). The addendum
   was appended and committed **before** the Decision, in the same file, and the
   Decision names it explicitly. Safe.
3. **The Internal review's findings [I1]–[I7] as corrections** — [I1] the
   fail-open on Bandit's own error array, [I2] the second tautology one file
   over, [I3] plus [I6c] settling item 4's fate as struck, [I4] the
   verbatim-vs-shipped wording, [I5] the rename's fidelity, [I6a/b] the oracle's
   unnamed boundaries, [I7] the perturbation trap. This is the *interpretive*
   step: no Response disposed of them, so the plan disposes of them, in the open,
   one chunk at a time.

**Where this reading could be wrong, stated so the Maintainer can strike it in
one line rather than discover it at code review.** Point 3 enlarges the
proposal's *Touches* line by one file (`bootstrap/tests/test_security_check.py`,
per [I2]) and adds two code behaviours the proposal did not describe (the
`errors`-array fail-close, per [I1]; the pinned count and no-symlink assertions,
per [I6b] and [I6c]). Each is a *defect fix inside the surface the proposal
opened*, none is a new mechanism, and each is fenced into its own chunk so
striking one does not unpick the others. If the Maintainer reads *as revised*
more narrowly, Chunks A and D are the ones to strike, and the plan still delivers
the accepted contract through Chunks B, C and E.

## The two defects this plan closes

Placed before *Scope* because they are why the plan is security-tiered rather
than a one-line coverage fix. Both were re-measured for this plan at HEAD
`05515df` under the canonical interpreter `~/conda_envs/lhm/bin/python`
(Python 3.13.13, Bandit 1.9.4), with `PYTHONDONTWRITEBYTECODE=1`. **No repository
file was modified**: every "post-fix" figure comes from a throwaway script that
imports the real registries and the real `install_manifest`.

### Defect 1 — the gate has never read the two files an adopter runs every day

`scan_targets()` at `bootstrap/security_check.py:57` walks two registries by
hand: `_MODULE_MAPPINGS` at `bootstrap/security_check.py:64` and
`_ALWAYS_ON_MAPPINGS` at `bootstrap/security_check.py:74`. `_SKILLS_MAPPINGS`
at `bootstrap/_scaffold/config.py:214` ships two `.py` files unconditionally to
every adoption — the command-line backend behind the `session-start` and
`session-end` routines — and nothing scans them.

Re-measured for this plan:

```
targets 72
templates .py in targets 42
manifest verbatim py 44
disk py 44
disk - targets: ['templates/skills/_lib/lifecycle.py', 'templates/skills/_lib/lifecycle_planner.py']
manifest - disk: []
disk - manifest: []
```

Three independent channels agree on 44 (the manifest, the working tree, and
`git ls-files templates | grep '\.py$' | wc -l` → 44), and the scan sees 42.

### Defect 2 — the guard that was supposed to catch that cannot fail

`test_scan_targets_cover_all_shipped_scripts` at
`bootstrap/tests/test_security_lint.py:134` calls itself *"the anti-drift
assertion"*. It builds its expected set by walking `_MODULE_MAPPINGS` — character
for character the code's first loop. The assertion is `X - (X ∪ …) == ∅`, empty
for every possible content of that registry. It was live and green on the day
`_SKILLS_MAPPINGS` was created and stayed green for 63 days while the drift it
was named for occurred.

**Item 3 as originally drafted reproduced this one abstraction higher** (oracle
and subject would both derive from `install_manifest()`). That is what the
addendum caught and what no External reviewer has yet read.

### The measurement that decides Chunk C — run for this plan, not carried forward

Four states, one script, the real registries. `T1` is the manifest-derived
conformance oracle; `T2` is the on-disk oracle Chunk C introduces:

```
=== baseline states ===
HEAD (no union)                          |t|= 72  T1_missing=[2 skills files]  T2_unscanned=[2 skills files]
post-fix (item 1 union)                  |t|= 74  T1_missing=[]                T2_unscanned=[]
union DELETED + explicit skills loop     |t|= 74  T1_missing=[]                T2_unscanned=[]

=== PERTURBATION: a registry stops delivering the two skills .py ===
post-fix, config patched (no-op trap)    |t|= 74  T1_missing=[]                T2_unscanned=[]
post-fix, install patched (real)         |t|= 72  T1_missing=[]                T2_unscanned=[2 skills files]

=== PERTURBATION: a templates/ .py no registry delivers (scratch root) ===
   scratch disk - targets: ['templates/optional/rogue.py']
```

Read the fourth data line and the fifth together. Under a real perturbation —
a delivery registry stops shipping two files that are still on disk — **the
manifest-derived oracle stays green and the on-disk oracle goes red naming
exactly the two files.** That single pair is the argument for Chunk C, and it is
the pair an External reviewer should reproduce first.

Two further facts fall out and are used below. The `config`-patched line is
[I7]'s trap reproduced: `bootstrap/_scaffold/install.py` binds the registry by
value at import, so patching the module that *defines* it does nothing — the
perturbation must target `bootstrap._scaffold.install`. And the third baseline
line is [I5]'s point reproduced: with the manifest union deleted and a
hand-written skills loop added, the conformance oracle is green again, so it
pins "scanned by *some* path", not "consumes the manifest".

## Scope

Executes the accepted contract, plus the corrections read into *as revised*
above, across five chunks and five files. Every touched file is Cairn-internal:
**nothing ships to an adopter, and no manifest row is added, removed or
changed.** That last is an assertion this plan verifies, not an aside.

**Out of scope, fenced explicitly:**

* **Item 4 / addendum change 3 — the registry census. STRUCK.** The proposal
  marks it strikeable and names it as the part a reviewer can remove without
  breaking the primary fix. [I3] then showed the name-keyed census is blind on
  the day it is written: `_OPTIONAL_TEMPLATES` at
  `bootstrap/_scaffold/config.py:249` is a live delivery registry that never
  reaches the manifest and whose name does not match `*_MAPPINGS`. [I6c] adds
  that its declared table is the hand-maintained fail-open shape the addendum's
  own level table condemns. Chunk C's oracle covers the case the census was for —
  measured above, a rogue `templates/optional/rogue.py` is caught — at no
  hand-maintained cost. If anyone wants the census later it needs its own
  proposal and a shape-based, not name-based, key.
* **Remediating the sixteen LOW subprocess findings.** `B404` (imports
  `subprocess`), `B603` (call with non-literal arguments), `B607` (`git` invoked
  by name rather than absolute path) in the two newly-scanned files. Recorded,
  not fixed. The four `B607` findings run inside an adopter's own repository and
  are a real question; bundling a code-hardening contract into a coverage
  contract is what cost `identity-not-name` a REVISE/SPLIT verdict.
* **Lowering the blocking threshold to LOW.** A different contract. It would turn
  the gate red on 113 LOW findings, only 16 of them newly visible.
* **Scanning Cairn's own `tools/*.py` and `scripts/*.py` twins of template
  sources.** Byte-identical to their template twins today, enforced by
  `test_every_self_hosted_twin_stays_byte_identical_to_its_source` in
  [`bootstrap/tests/test_notice_install.py`](../../bootstrap/tests/test_notice_install.py);
  coverage-neutral, and not addressed.
* **Any `bootstrap/_scaffold/` change.** None. The gate *imports from* the engine
  package — which `bootstrap/security_check.py` already does — and edits nothing
  in it. This is what keeps the engine gate set and the AST-attestation re-anchor
  off this plan; see *Gate accounting*.
* **The default-security-stance question the Maintainer opened 2026-08-03.** The
  proposal's Response verified that no preset selects `content-security` and
  routed the fix to the preset → module table in `bootstrap/_scaffold/config.py`,
  explicitly **not here**. This plan does not touch `_PRESETS` and makes no claim
  on that work.
* **Replacing the two existing registry loops with the manifest derivation.**
  They are kept, unmodified, on purpose — that retention is what makes "coverage
  cannot shrink" checkable by reading three lines. Removing them is a separate
  change at this same review tier. Note the honest consequence, recorded in Chunk
  D: after Chunk B they are strictly redundant (measured — `loop1 ∪ loop2` is a
  44-element manifest set's 42-element subset), so they are defence in depth, not
  a second guard.

### Documentation / doctrine surface

* **Governing layer — none.** No `AGENTS.md` change, no `doctrine/` change. The
  rule ("the whole shipped Python surface" is Layer-4 code, gated by Bandit) is
  unchanged, already accepted and already written down; this plan brings the code
  up to it. The doctrine-change rate-limit in `doctrine/rationale.md` is therefore
  not engaged.
* **Descriptive / governing files that describe the software as it is** —
  `bootstrap/SAFETY.md` (two edits, Chunk E) and `SECURITY.md` (one, Chunk E).
  Both are descriptions of a gate whose behaviour this plan changes; leaving
  them is how a claim outruns its implementation, which is the defect class.
* **Code-adjacent prose** — the module docstring and `scan_targets()` docstring
  in `bootstrap/security_check.py`, corrected in the same commit as the
  behaviour they describe (Chunk B), never later.
* **Release-facing** — `CHANGELOG.md > Unreleased > Fixed`, one line.
* **Deliberation layer** — this plan, its plan review, its code review, and the
  `dev/PLANNING.md` row-move that serializes the plan-open.
* **Adopter-installed files — none.** Checked, not assumed: the verification
  below diffs `scaffold.py --manifest` against a pre-change capture and expects
  it empty.

<!-- cairn:slot documentation-tier-home -->
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
plan's *Scope* must name the doctrine-surface touched (or an explicit
"no doctrine surface").
<!-- cairn:end documentation-tier-home -->

### Gate accounting

Each figure is a dated snapshot, measured for this plan, to be re-taken at
implementation rather than quoted from here.

* **Suite baseline: 1601 passed, 0 failed, 0 skipped**, `as_of 2026-08-03`, under
  `~/conda_envs/lhm/bin/python` (3.13.13), full `python -m pytest bootstrap/tests`
  run for this plan (151s). Collection may only grow; a dropped node or a new
  skip/xfail marker is a HOLD class.
* **Three frozen files are modified**: `bootstrap/security_check.py`,
  `bootstrap/tests/test_security_lint.py`, and — per [I2], the scope call above —
  `bootstrap/tests/test_security_check.py`. All three are literal keys in the
  164-entry `frozen_files` map, `as_of 2026-08-03`. No new file is created, so
  there is no `FROZEN-NEW` row either. **This estimate proved incomplete at
  implementation** — the two renames and A4's skipif add three further rows in
  two classes it did not anticipate; the measured accounting is in *Verification
  > Gate-integrity accounting*, and that is the one to re-pin from.
* **The frozen map does not gate the suite, and this was checked rather than
  assumed.** `bootstrap/tests/test_gate_manifest.py` verifies against a manifest
  *produced from the live tree at test time*; the committed
  `bootstrap/tests/fixtures/gate_manifest.json` is read only by the batch tooling
  (`bootstrap/tests/_gate_manifest.py`, `bootstrap/tests/_gate_preflight.py`)
  when an operator runs it. So `python -m pytest bootstrap/tests` stays green
  across these edits.
* **But the committed manifest goes stale, and that is a Maintainer-facing
  consequence.** After this plan lands, `_gate_manifest.py verify` reports
  `FROZEN-MODIFIED` for the three files. The `gate-reanchor-preflight` batch
  archived earlier today, so the HOLD default that applied during the window is
  no longer in force — but **re-pinning the manifest is a supervised act under
  `bootstrap/REANCHOR_RUNBOOK.md` and is not an implementing agent's to perform.**
  The implementing agent's obligation is to say, in the final commit body, that
  three frozen entries are now stale and name them.
* **No AST re-anchor.** No `bootstrap/_scaffold/` file is touched, so
  `bootstrap/tests/fixtures/scaffold_ast_baseline.json` is unaffected and the
  runbook's attestation half is not engaged. Chunk B adds an *import from*
  `bootstrap/_scaffold/install.py`, which changes no engine byte. Checked: the
  trust-anchor guard `test_security_check_imports_trust_anchor_from_narrowest_owner`
  at `bootstrap/tests/test_config_module.py:50` constrains only the `ImportFrom`
  node that names `_MODULE_MAPPINGS`, so a separate `install_manifest` import
  does not trip it — and importing `bootstrap.security_check` already executes
  the whole engine package, so the runtime trust surface does not widen.
* **The install contract must not move.** `python bootstrap/scaffold.py
  --manifest` emits 95 data rows, `as_of 2026-08-03`. Expected diff: empty. A
  diff means `install_manifest()` was *edited* rather than merely read — stop and
  re-review.
* **Doc gates.** `python scripts/check_cairn.py` → OK over 174 Markdown files,
  `as_of 2026-08-03`. `python scripts/quality_gate.py --sub neutrality` →
  `fail=99`, `as_of 2026-08-03`; `bootstrap/*.md` is inside its scan roots, so
  the `SAFETY.md` edits pass through it and the figure must not move.
* **Bandit's own error channel is empty today** — measured for this plan over
  *both* target sets, which is what makes Chunk A free:

  ```
  base     n=72  rc=1  errors=[]  sev={'LOW': 97}
  extended n=74  rc=1  errors=[]  sev={'LOW': 113}
  ```

  Zero MEDIUM-or-higher in both. The +16 are the two skills files' subprocess
  family. **This is a snapshot, not a property of those files** — it is only free
  today, which is the whole argument for landing before the three proposals that
  edit them.

### Sequencing against the sibling proposals

The proposal's *Sequencing* section argues this change should land **first**, and
its stated blocker was the open frozen-file window. That premise has moved twice.
[I8] reported the `gate-reanchor-preflight` plan archived at `b67fabc`; verified
again for this plan at HEAD `05515df`, the batch is closed and the frozen set is
re-pinned at 164. So the preferred position is now schedulable.

Verified `as_of 2026-08-03`: none of the four proposals in the ordering argument
has landed — `agent-context-scrub`, `gate-claims-vs-enforcement`,
`planner-line-semantics` and `byline-classification` are all still open under
`dev/proposals/`. Two consequences bind this plan:

* **File collisions — one proposal per shared file, in flight at a time.** This
  plan claims `SECURITY.md` (shared with `agent-context-scrub`), and
  `bootstrap/SAFETY.md` plus `bootstrap/tests/test_security_lint.py` (both shared
  with `gate-claims-vs-enforcement`, whose disposition A5 corrects a docstring
  and a skip message in that test file — the *same* docstring Chunk B rewrites).
  Whichever of the two lands second must **re-read the file and re-verify each
  quoted sentence**, not apply its recorded text.
* **The ordering benefit is real and measured on one side only.** Landing first
  costs zero today (0 blocking over the extended set, re-measured above); landing
  last costs whatever the three intervening changes introduce, which cannot be
  measured until they land.

If a sibling has landed by the time implementation starts, the quoted line
citations in Chunk E may have moved. That is a signal to re-read, not to apply
blind.

## Sequence

Chunk order is load-bearing and is not the proposal's order. **Chunk A lands
before the widening** so that at no intermediate commit can the gate print
"clean over 74 shipped file(s)" without having actually opened 74 — the message
counts *requested* targets, and until Chunk A a target that could not be read was
silently skipped.

```
0. plan-open   -- this plan + the dev/PLANNING.md row-move             [commit pending]
   (plan review) -- required(External, security lens); NO code before it lands
1. Chunk A -- fail closed on Bandit's own error array ([I1])           [commit pending]
2. Chunk B -- bind the scan set to the install manifest (items 1 + 2)  [commit pending]
3. Chunk C -- an oracle the code under test does not read (change 2)   [commit pending]
4. Chunk D -- retire the second overclaiming test name ([I2])          [commit pending]
5. Chunk E -- the prose that outruns the gate, and the changelog       [commit pending]
```

---

### Chunk A — the scan must not report clean over a file it never opened

Closes [I1]. The proposal's *Author-accounting* asserts that a shipped file
missing from disk is caught by the scanner-error branch. It is not: Bandit
records the failure in a JSON `errors` array, scans the rest, and exits **0**.
Reproduced for this plan in a scratch directory:

```
$ ~/conda_envs/lhm/bin/python -m bandit -q -f json ok.py /nonexistent/missing_file.py; echo RC=$?
RC=0
errors: [{'filename': '/nonexistent/missing_file.py', 'reason': 'No such file or directory'}]
results: 0
$ ~/conda_envs/lhm/bin/python -m bandit -q -f json ok.py broken.py; echo RC=$?
RC=0
errors: [{'filename': './broken.py', 'reason': 'syntax error while parsing AST from file'}]
results: 0
```

`rc == 0` never reaches the branch at `bootstrap/security_check.py:128`, and
nothing reads `report["errors"]`. A shipped `.py` that does not parse is
scanned-as-clean, silently, forever. This is pre-existing — Chunk B does not
create it — but Chunk B makes manifest-vs-disk divergence the governing risk, and
this fail-open is exactly what that divergence lands on.

| # | File | Change |
|---|------|--------|
| A1 | `bootstrap/security_check.py` | In `run_bandit()`, immediately after the `json.loads` at `bootstrap/security_check.py:132`, fail closed when `report.get("errors")` is non-empty: print one line per error (filename + reason) to stderr and `return 1`. Placed **before** allowlist filtering, matching the existing scanner-error posture. |
| A2 | `bootstrap/tests/test_security_lint.py` | The same check in `test_no_blocking_security_findings`, as a `pytest.fail` with the same message shape. The dev gate consumes the same report and had the same hole; fixing one and not the other is how the two drift. |
| A3 | `bootstrap/tests/test_security_check.py` | New `test_fail_closed_on_bandit_file_errors(monkeypatch)`: stub `subprocess.run` to return `returncode=0` and a JSON body carrying one `errors` entry and zero `results`; assert `run_bandit() == 1`. Follows the existing stub idiom already in that file. |
| A4 | `bootstrap/tests/test_security_check.py` | New end-to-end under the file's existing `_bandit_available()` skipif: build a `tmp_path` root holding one real `ok.py`, monkeypatch `security_check.CAIRN_ROOT` to it and `security_check.scan_targets` to `lambda: ["ok.py", "gone.py"]`, and assert `run_bandit() == 1`. Two files, so it costs milliseconds, and the verdict comes from **real Bandit**, not from a stub of it. |

**Acceptance criteria — Chunk A.**

* `~/conda_envs/lhm/bin/python -m pytest bootstrap/tests/test_security_check.py bootstrap/tests/test_security_lint.py -q` → all pass, 0 skipped.
* `~/conda_envs/lhm/bin/python bootstrap/security_check.py` → still `PASS`. Free
  today: `errors` is `[]` over both the 72- and 74-target sets, measured above.
* **Perturbation, must be RUN and its ledger written into the commit body.**
  Delete the A1 branch; confirm A3 **and** A4 both fail; restore and confirm
  `git diff bootstrap/security_check.py` is empty. Then delete the A2 branch and
  confirm the dev-gate test still passes today (it *cannot* fail on live data
  while `errors` is empty) — record that honestly rather than claiming A2 is
  independently guarded; A3 and A4 are what guard the behaviour, A2 is the
  symmetric application of it.
* **The future state in which A3/A4 fail** is not hypothetical and is the reason
  the chunk exists: any commit that removes the branch, and — independently —
  any repository state where a manifest row names a file absent from disk or a
  shipped `.py` stops parsing. A4 constructs that second state directly.
* **Channel note.** Subject: `run_bandit()` in `bootstrap/security_check.py`.
  Oracle: the `errors` array in Bandit's JSON, produced by a different program
  (A4) or by a fixture the test authors (A3). Neither input is derived from the
  file under verification.

---

### Chunk B — bind the scan set to the published install manifest

Executes proposal items 1 and 2, and rewrites the conformance test to say what it
actually pins ([I5]).

| # | File | Change |
|---|------|--------|
| B1 | `bootstrap/security_check.py` | Add `from bootstrap._scaffold.install import install_manifest` alongside the existing config import. Append to `scan_targets()`, as a **union with** — never a replacement for — the two loops at `bootstrap/security_check.py:64` and `bootstrap/security_check.py:74`: `for src, _dst, verbatim in install_manifest(modules=None): if verbatim and src.endswith(".py"): targets.add(f"templates/{src}")`. The comment must state the two load-bearing facts: `modules=None` means the **full** published catalog (a module subset would silently shrink the scanned surface), and the union framing is what makes "coverage cannot shrink" true by inspection rather than by measurement. |
| B2 | `bootstrap/security_check.py` | Wrap the `scan_targets()` call at `bootstrap/security_check.py:111` in `try` / `except ValueError as exc`, printing `security_check: cannot enumerate the shipped surface (…) -- FAIL CLOSED.` to stderr and returning 1. **This is legibility, not new safety**, and the plan says so where the code says so: `main()` wraps `run_bandit()` in no handler, so an uncaught `ValueError` already exits non-zero. The wrapper buys a security message instead of a traceback. |
| B3 | `bootstrap/security_check.py` | Module docstring and `scan_targets()` docstring corrected: both currently describe a `_MODULE_MAPPINGS`-only derivation. Same commit as the behaviour, never later. |
| B4 | `bootstrap/tests/test_security_lint.py` | Rename `test_scan_targets_cover_all_shipped_scripts` (at `bootstrap/tests/test_security_lint.py:134`) to **`test_every_manifest_verbatim_py_is_scanned_by_some_path`**, and derive `shipped` from `install_manifest(modules=None)` joined as `templates/{src}` instead of from `_MODULE_MAPPINGS`. Docstring rewritten to drop *"the source of truth"* and *"the anti-drift assertion"* and to state the limit measured above: this pins that every manifest-verbatim `.py` is reached by **some** path, not that `scan_targets()` consumes the manifest — a future author who deletes the union and adds a third explicit loop leaves it green. Retain the three assertions that can already fail (the named-dev-file loop, the every-target-ends-in-`.py` guard, the `assert shipped, …` non-emptiness guard at `bootstrap/tests/test_security_lint.py:147`). |
| B5 | `bootstrap/tests/test_security_check.py` | New `test_fail_closed_when_the_manifest_refuses(monkeypatch)`: monkeypatch `security_check.scan_targets` to raise `ValueError("destination-ownership conflict")`; assert `run_bandit() == 1` and that the captured stderr carries the security message rather than a traceback. |

**Acceptance criteria — Chunk B.**

* `~/conda_envs/lhm/bin/python bootstrap/security_check.py` → `security_check:
  Bandit clean over 74 shipped file(s).` and `PASS`. **Note what this line is and
  is not evidence of.** It counts *requested* targets; it becomes evidence that
  74 files were *opened* only because Chunk A landed first. That dependency is
  the reason for the chunk order, and a reviewer should check it rather than take
  it here.
* **Monotonicity, verified against a pre-change capture.** Before Chunk A, write
  `sorted(scan_targets())` to a scratch file outside the tree; after B1, assert
  `set(pre) <= set(post)` and `len(post) - len(pre) == 2`. The baseline arrives
  from a *pre-change execution recorded outside the repository* — the artifact
  under verification cannot supply it.
* **The install contract is unchanged.** Capture `python bootstrap/scaffold.py
  --manifest` to a scratch file at the plan-open commit; diff after B1. Expected
  empty, 95 data rows.
* `~/conda_envs/lhm/bin/python -m pytest bootstrap/tests/test_config_module.py -q`
  → green, confirming the narrowest-owner trust-anchor guard is not tripped by
  the new import.
* **Perturbations, both RUN, ledger in the commit body.**
  * *P-B1 (B4 discriminates the deletion case).* Delete the B1 union loop; B4
    fails naming exactly `templates/skills/_lib/lifecycle.py` and
    `templates/skills/_lib/lifecycle_planner.py`. Already measured in simulation
    for this plan (the `HEAD (no union)` row above); re-run against the real
    edited file.
  * *P-B2 (B5 discriminates the guard).* Delete the B2 `try` / `except`; B5 fails
    with an uncaught `ValueError` rather than a clean `== 1`.
* **The stated non-failure, recorded rather than discovered.** With the union
  deleted **and** a hand-written `_SKILLS_MAPPINGS` loop added, B4 is green
  (measured: the `union DELETED + explicit skills loop` row). B4 therefore cannot
  be the durable guard, and its docstring says so. That is Chunk C's job.
* **Channel note.** Subject: `scan_targets()`. B4's oracle is
  `install_manifest()` — the *same* enumeration the subject now reads, which is
  why B4 is labelled a conformance check and not an anti-drift check. The
  independent channel arrives in Chunk C.

---

### Chunk C — an oracle the code under test does not read

The durable half, and the part no External reviewer has seen. `scan_targets()`
performs no filesystem read under `templates/` — it joins strings from registry
data and globs only `scripts/`, `bootstrap/`, and `bootstrap/_scaffold/`. So the
working tree under `templates/` is a channel the subject does not consume.

All of C lands in `bootstrap/tests/test_security_lint.py`.

| # | File | Change |
|---|------|--------|
| C1 | `bootstrap/tests/test_security_lint.py` | Module-level helper `_templates_py_on_disk(root)` returning `{str(p.relative_to(root)) for p in (root / "templates").rglob("*.py")}`, and `_unscanned_disk_py(root)` returning `sorted(_templates_py_on_disk(root) - set(_scan_targets()) - set(_SCAN_EXCLUSIONS))`. Factored as helpers so the perturbation tests can call them directly instead of catching `AssertionError`. |
| C2 | `bootstrap/tests/test_security_lint.py` | `_SCAN_EXCLUSIONS: dict[str, str]` — declared exclusions, path → mandatory rationale. **Empty today**: disk, manifest-verbatim and `git ls-files` all agree at 44, so the table costs nothing to introduce and fires the moment they disagree. Mirrors the `ALLOWLIST` + `test_allowlist_entries_have_rationale` idiom already in this file rather than inventing a second one. |
| C3 | `bootstrap/tests/test_security_lint.py` | `test_every_templates_py_on_disk_is_release_scanned`: (a) `assert _templates_py_on_disk(CAIRN_ROOT)` — the non-emptiness guard [I6a] asks for, since empty-minus-anything is empty and a missing `templates/` would make the oracle vacuous; (b) `assert _unscanned_disk_py(CAIRN_ROOT) == []`; (c) the **reverse direction** [I1] asks for — every manifest-verbatim `.py` exists on disk, so a manifest row naming an absent file is caught here as well as by Chunk A; (d) every `_SCAN_EXCLUSIONS` key exists on disk and carries a non-empty rationale, so an exclusion cannot outlive the file it excuses; (e) every `_SCAN_EXCLUSIONS` key is **absent from** `_scan_targets()`, so an exclusion the scan has since made redundant is deleted rather than left as a latch. (e) is the other half of stale and does not follow from (d): measured for the plan-review Response, an entry that is on disk, rationale'd *and* already scanned passes (a)–(d) unchanged, then silently absorbs a later coverage regression for that same file — the subtraction is a no-op until the moment it is not. |
| C4 | `bootstrap/tests/test_security_lint.py` | `test_templates_py_count_is_pinned`: `assert len(_templates_py_on_disk(CAIRN_ROOT)) == 44`, with a message naming the deliberate-move path *and* pointing at the sibling pin at `bootstrap/tests/test_notice_install.py:75`, which must move in the same commit. [I6c]'s antidote to a fail-open exclusion table: the count fails loudly when the shipped surface grows, forcing a human to look, exactly as `assert scanned == 9` at `bootstrap/tests/test_upgrade_side_door_parity.py:168` already does for the always-on group. |
| C5 | `bootstrap/tests/test_security_lint.py` | `test_templates_tree_contains_no_symlink`: `assert not [p for p in (CAIRN_ROOT / "templates").rglob("*") if p.is_symlink()]`. This *enforces* the `recurse_symlinks` decision [I6b] says must be recorded rather than defaulted: `Path.rglob` does not descend symlinked directories in Python 3.13, so "physically present under `templates/`" is glob-scoped, not filesystem-scoped. The choice is to keep the default and assert the condition under which default and filesystem agree. Measured today: `find templates -type l` returns nothing. |
| C6 | `bootstrap/tests/test_security_lint.py` | `test_the_on_disk_oracle_goes_red_when_a_registry_stops_delivering(monkeypatch)`: `monkeypatch.setattr("bootstrap._scaffold.install._SKILLS_MAPPINGS", <the tuple with both .py entries removed>)`, then assert `_unscanned_disk_py(CAIRN_ROOT) == ["templates/skills/_lib/lifecycle.py", "templates/skills/_lib/lifecycle_planner.py"]`. **The target module is load-bearing and is [I7]'s trap**: `bootstrap/_scaffold/install.py` binds the registry by value at import, so patching `bootstrap._scaffold.config` is a silent no-op. A comment in the test says so, citing `bootstrap/tests/test_scaffold_substrate.py`, which already documents the patch-the-owning-module rule for a different symbol. |
| C7 | `bootstrap/tests/test_security_lint.py` | `test_a_templates_py_no_registry_delivers_is_reported_unscanned(tmp_path, monkeypatch)`: monkeypatch `security_check.CAIRN_ROOT` to `tmp_path` (the idiom `test_scan_targets_recurses_the_scaffold_engine_package` already uses in this file), write `tmp_path/templates/optional/rogue.py`, and assert `_unscanned_disk_py(tmp_path) == ["templates/optional/rogue.py"]`. This is [I3]'s `_OPTIONAL_TEMPLATES` class — a live delivery registry that never reaches the manifest — held by the oracle rather than by the struck census. |
| C8 | `bootstrap/tests/test_security_lint.py` | The named-file pin proposal item 3 calls for: assert both `templates/skills/_lib/lifecycle.py` and `templates/skills/_lib/lifecycle_planner.py` are literal members of `_scan_targets()`, so this specific miss cannot recur silently even if the derivation is later refactored. Belt to C3's braces. |

**Acceptance criteria — Chunk C.**

* `~/conda_envs/lhm/bin/python -m pytest bootstrap/tests/test_security_lint.py -q`
  → all pass, 0 skipped.
* **Perturbation P-C1 — the one that matters, and it must be RUN.** With Chunk B
  in place, patch `bootstrap._scaffold.install._SKILLS_MAPPINGS` to drop the two
  `.py` entries and observe, in the same run: **B4 green, C3 red naming exactly
  the two files.** That pair is the whole claim of this chunk. Simulated for this
  plan against the real objects with the predicted result; the implementing agent
  reproduces it against the real edited files.
* **Perturbation P-C2 — C6 is not itself hollow.** Repeat C6 patching
  `bootstrap._scaffold.config._SKILLS_MAPPINGS` instead; confirm C6 **fails**
  (the oracle stays empty because the patch is a no-op). This is the discipline
  applied one level down: a perturbation test whose perturbation does nothing is
  the failure mode [I7] names.
* **Perturbation P-C3 — C7 is not vacuous.** Remove the `rogue.py` write; confirm
  C7 fails.
* **Perturbation P-C4 — C4's pin can fire.** Create a throwaway
  `templates/_probe.py` in the working tree, run C4, confirm it fails at 45 ≠ 44,
  delete it, confirm `git status --short` is clean. A transient working-tree
  file, never committed.
* **Perturbation P-C5 — C5's assertion can fire.** `ln -s` a directory containing
  a `.py` under `templates/` in the working tree, run C5, confirm it fails,
  remove the link, confirm `git status --short` is clean.
* **Perturbation P-C6 — C3(d)/(e)'s exclusion guards can fire.** They are
  **vacuous while the table is empty**, and the plan says so rather than letting an
  empty loop read as a passing check. Temporarily add `{"templates/does_not_exist.py":
  "probe"}` and confirm the exists-on-disk assertion fails; then `{"<a real
  path>": ""}` and confirm the rationale assertion fails; then `{"<a real path
  already in _scan_targets()>": "looks legitimate"}` and confirm the (e)
  redundancy assertion fails — this third case is the one that passes (a)–(d),
  so it is the case that proves (e) is carrying weight rather than restating (d).
  Revert all three. Run, do not ship.
* **The future states in which C3 fails**, named because that is the acceptance
  bar: (i) today's pre-Chunk-B state — measured, `disk - targets` names exactly
  the two skills files; (ii) the union deleted from `scan_targets()` by a later
  refactor, which is the case the proposal's own monotonicity guarantee is
  *unguarded* against; (iii) any registry — including `_OPTIONAL_TEMPLATES` —
  shipping a `.py` under `templates/` the manifest never sees; (iv) a substituted
  (non-verbatim) `.py` added to `_CORE_MAPPINGS` or `_OPTIONAL_TEMPLATES`, which
  the `verbatim` filter would exclude from the scan while the file sits on disk.
  Case (iv) is [I4]'s scenario and the oracle turns it into a decision — an
  exclusion entry with a rationale, or a coverage change — instead of a silent
  ship.
* **Channel note.** Subject: `scan_targets()`, whose inputs are Python data
  structures in `bootstrap/_scaffold/config.py` and `bootstrap/_scaffold/install.py`.
  Oracle: `pathlib` enumeration of the working tree under `templates/`, which the
  subject never reads. The independence is demonstrated, not asserted — under
  P-C1 the registry changes and the disk does not, and the two sets come apart.
* **A named residual, not assumed away.** The oracle globs the working tree, so a
  developer who parks a scratch `.py` under `templates/` turns the dev security
  test red. That is intended (an authored-but-unwired template *should* force a
  decision), but it is a real ergonomic cost and it is stated here rather than
  discovered. A second residual: independence holds only while every registry
  sources from under `templates/`, true `as_of 2026-08-03`; a future registry
  sourcing elsewhere escapes the oracle, and the test docstring must say so.

---

### Chunk D — retire the second overclaiming test name

Closes [I2]. `test_scan_targets_are_explicit_files_covering_shipped_surface` at
`bootstrap/tests/test_security_check.py:28` carries an always-on coverage loop at
`bootstrap/tests/test_security_check.py:43` that is, character for character, the
code's second loop. Same defect as Defect 2, in a file the proposal's *Touches*
line does not name, and it is the one whose *name* makes the shipped-surface
claim.

| # | File | Change |
|---|------|--------|
| D1 | `bootstrap/tests/test_security_check.py` | Rename to `test_scan_targets_are_explicit_files_and_name_the_expected_executables`. The name is the fix: a test that names a property it does not have is worse than a missing test, because it retires the question. |
| D2 | `bootstrap/tests/test_security_check.py` | Docstring stating, plainly, what each part can and cannot do: the named literals can fail (a file dropping out of the scan set fails them); the `_ALWAYS_ON_MAPPINGS` loop **cannot fail on registry drift**, because its oracle is the registry the subject reads — and, after Chunk B, cannot fail on the loop's deletion either, since the manifest union covers the identical `templates/modules/{src}` strings. Point at the two real guards: the growth tripwire `assert scanned == 9` at `bootstrap/tests/test_upgrade_side_door_parity.py:168`, and Chunk C's on-disk oracle. |
| D3 | `bootstrap/tests/test_security_check.py` | Add the two skills tools to the named-literal assertions, alongside the five already there. These are genuine: they fail if the union is removed. |

**No `assert scanned == 9` is added here** — checked rather than assumed: the
growth tripwire already exists at `bootstrap/tests/test_upgrade_side_door_parity.py:168`,
and a second copy would be a second thing to keep in sync.

**Acceptance criteria — Chunk D.**

* `~/conda_envs/lhm/bin/python -m pytest bootstrap/tests/test_security_check.py -q`
  → all pass.
* **Perturbation, RUN.** Delete the Chunk B union loop; confirm D3's two literals
  fail. Restore; confirm `git diff` empty.
* **The honest non-perturbation, recorded.** There is *no* perturbation that
  makes the retained `_ALWAYS_ON_MAPPINGS` loop fail on drift. That is the
  finding, not an omission, and D2's docstring now says it where the test can be
  read rather than leaving the name to imply otherwise.
* **Channel note.** D3's oracle is two path literals typed by a human into the
  test; the subject is `scan_targets()`. No shared derivation.

---

### Chunk E — the prose that outruns the gate, and the changelog

| # | File | Change |
|---|------|--------|
| E1 | `bootstrap/SAFETY.md` | The scan-set derivation sentence at `bootstrap/SAFETY.md:158` — *"The Bandit gate derives its scan set from `_MODULE_MAPPINGS` (verbatim scripts) plus `scripts/` + `bootstrap/`"* — corrected to name the install-manifest derivation, while keeping the `scripts/` + `bootstrap/` + recursive `bootstrap/_scaffold/` clauses that remain true. |
| E2 | `bootstrap/SAFETY.md` | The Layer-4 enumeration of verbatim reference scripts mentions neither `lifecycle.py` nor `lifecycle_planner.py`. A reviewer using that list to decide *"does my change ship as code?"* would today conclude, wrongly, that the skills tools are not Layer-4 code. Both are added, with their `tools/` destinations. |
| E3 | `SECURITY.md` | `SECURITY.md:66` reads *"over the shipped Python surface"*. The proposal concluded this needs no change; [I4] showed it becomes true only because the substituted-`.py` set is empty today — `install_manifest` stamps `verbatim=False` unconditionally on every core row at `bootstrap/_scaffold/install.py:1374`, so a `.py` with `{{token}}` slots added to `_CORE_MAPPINGS` would ship as executable code and be filtered out of the scan. Say what the contract is: every file the scaffold ships **byte-for-byte** as Python. One clause; the *Release security checklist* structure is unchanged. |
| E4 | `bootstrap/security_check.py` module docstring | **Not here** — landed in Chunk B, with the behaviour it describes. Listed so its absence from this chunk is deliberate rather than an omission. |
| E5 | `CHANGELOG.md > Unreleased > Fixed` | One line: the release Bandit gate now derives its scan set from the published install manifest and reaches the two session-lifecycle tools it had never read, and it fails closed when Bandit reports a file it could not open. Cross-link the proposal and plan by stem. |

**Acceptance criteria — Chunk E.**

* `~/conda_envs/lhm/bin/python scripts/check_cairn.py` → OK; 174 Markdown files
  `as_of 2026-08-03`, and the count may only grow.
* `~/conda_envs/lhm/bin/python scripts/quality_gate.py --sub neutrality` →
  `fail=99`, unchanged. `bootstrap/*.md` is inside the scan roots.
* `~/conda_envs/lhm/bin/python scripts/claim_check.py <file>` over each edited
  Markdown file, **one file per invocation** — the checker takes a single path
  and exits 2 on more.
* **Verify the quoted sentences before editing.** E1 and E3 quote lines that a
  sibling proposal may have moved. Re-read `bootstrap/SAFETY.md` and
  `SECURITY.md` at implementation time; do not apply the edits from this plan's
  text alone.
* **Channel note.** The claim being verified is that the prose now matches the
  gate. The evidence is a *reading of the edited gate code plus a live run of it*
  (`python bootstrap/security_check.py` reporting 74), not a reading of the prose
  that was just written. `check_cairn` checks link and claim-path integrity, not
  whether a sentence is true — it catches drift, never absence, and the plan does
  not lean on it for this.

## Acceptance criteria

Per-chunk criteria are above; these are the plan-level deliverables.

* **Tests that must pass.**
  * `~/conda_envs/lhm/bin/python -m pytest bootstrap/tests` — the whole suite,
    green, **0 failed / 0 skipped / 0 xfailed**, under the canonical interpreter
    (3.13.13) with `PYTHONDONTWRITEBYTECODE=1`. Baseline **1601 passed**,
    `as_of 2026-08-03`, measured for this plan. Collection grows by exactly the
    new nodes and drops none.
  * [`bootstrap/tests/test_security_lint.py`](../../bootstrap/tests/test_security_lint.py)
    — the rewritten conformance test (B4), the on-disk oracle and its four
    guards (C3–C5), the two perturbation tests (C6, C7), the named-file pin (C8).
  * [`bootstrap/tests/test_security_check.py`](../../bootstrap/tests/test_security_check.py)
    — the errors fail-close (A3, A4), the manifest-refusal fail-close (B5), the
    renamed and re-documented explicit-files test (D1–D3).
  * [`bootstrap/tests/test_config_module.py`](../../bootstrap/tests/test_config_module.py)
    — unchanged and green, confirming the new engine import does not trip the
    narrowest-owner trust-anchor guard.
  * [`bootstrap/tests/test_notice_install.py`](../../bootstrap/tests/test_notice_install.py)
    — unchanged and green; its own `44` pin and C4's must agree, and if either
    moves both move in the same commit.
  * **Every new test shown non-vacuous by a run perturbation**, with the ledger
    — the change made, the failure observed, the byte-identical restore — in the
    commit body. Where a test *cannot* be made to fail, the plan says so instead
    (A2 and D2's always-on loop).
* **Doc updates that must land.** All hand-authored: `bootstrap/SAFETY.md` (two
  edits), `SECURITY.md` (one), the two docstrings inside
  `bootstrap/security_check.py`, and `CHANGELOG.md > Unreleased > Fixed`. No
  generated docs, no snippet-synced blocks.
* **Examples / smoke checks required.** `python bootstrap/security_check.py` —
  the real release gate end to end, expected `PASS` with the Bandit line
  reporting **74** files. `python bootstrap/scaffold.py --manifest` — expected
  **unchanged**, which is itself the assertion that this plan installs nothing
  new into an adopter tree. **N/A**: the example gallery under `examples/` — this
  change touches nothing the runnable examples demonstrate.
* **Inbound path-link updates.** None expected. `dev/PLANNING.md` and
  `dev/NEXT_SESSION.md` refer to plans by filename stem, not path link, so the
  archive-move needs no edit there. Confirm at archive time rather than assume.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants, each with the chunk that enforces it.**
  * *Every verbatim `.py` in `install_manifest()` is in `scan_targets()`.*
    Enforced by B4 in
    [`bootstrap/tests/test_security_lint.py`](../../bootstrap/tests/test_security_lint.py).
  * *Every `.py` physically present under `templates/` is in `scan_targets()`,
    modulo a rationale'd exclusion.* Enforced by C3, with C6 and C7 proving it
    can fail.
  * *`scan_targets()` never shrinks as a result of this change.* Enforced
    structurally (a `set.add` into the same accumulator, both prior loops
    retained) and checked once against a pre-change capture. **Not guarded by any
    test, and that is the claim an External reviewer should attack** — no test
    goes red if a later author replaces the loops with the manifest derivation.
    The mitigation is indirect: a shipped file dropped from the scan by such a
    refactor is a file present on disk and absent from `scan_targets()`, which is
    exactly C3.
  * *`install_manifest` is called with `modules=None`.* Load-bearing — a module
    subset would silently shrink the scanned surface. Pinned by inspection of B1's
    code, **not** by B4, whose oracle shares the argument. Stated because the
    proposal's own accounting claimed the test pins it and it does not.
  * *Every target is a file, never a bare directory* (the missing-`-r` footgun).
    Pre-existing, retained in B4.
  * *The published install manifest does not move.* Enforced by the diff against
    a pre-change capture, in Chunk B's acceptance.
* **Public-path → test mapping.** `scan_targets()` and `run_bandit()` are the two
  public entry points this plan touches, and both are exercised through their
  public paths — not via stubs of themselves — by
  [`bootstrap/tests/test_security_lint.py`](../../bootstrap/tests/test_security_lint.py)
  and
  [`bootstrap/tests/test_security_check.py`](../../bootstrap/tests/test_security_check.py),
  which the release command and the dev gate share by import. A3, A4, B5 stub
  `subprocess.run` or `scan_targets` — they are testing `run_bandit()`'s handling
  of a scanner result, and the stub is the *input*, never the oracle.
* **Failure modes.**
  * `install_manifest()` raises on duplicate destinations → **closed**, with a
    security message (B2), pinned by B5.
  * A shipped file listed in the manifest is missing from disk, or present and
    unparseable → **closed** by A1, pinned by A3 and A4, and independently
    surfaced by C3's reverse-direction assertion. *This corrects the proposal's
    Author-accounting, which asserted the pre-existing scanner-error branch
    already closed it. It did not.*
  * Bandit absent, or a scanner error (`rc` outside `{0, 1}`) → **closed**,
    pre-existing.
  * A delivery path that bypasses `install_manifest()` entirely → **open at the
    gate, caught by the test** while the path sources from under `templates/`
    (C7). `_OPTIONAL_TEMPLATES` is the live instance.
  * A substituted (non-verbatim) `.py` shipped to adopters → **open at the gate,
    caught by the test** (C3, since the oracle globs disk without a `verbatim`
    filter). Forces a decision instead of a silent ship. Not closed at the gate,
    because closing it would change the contract from byte-for-byte to
    all-shipped — a different proposal.
  * `templates/` missing or empty → **closed** by C3's non-emptiness guard.
  * A registry sourcing from outside `templates/` → **open**, named in C3's
    docstring as the oracle's boundary. No mechanism proposed.
* **Edge cases handled.** Empty registry (the pre-existing `assert shipped, …`
  guard fires). Non-`.py` verbatim entries such as
  `templates/skills/_data/vendor_targets.yml` — filtered by `.endswith(".py")`,
  same as the existing loops. Substituted `.md` skills sources — correctly
  outside Layer-4 code; note the proposal's Response already corrected the
  reading that they are "covered by the content scanner", since no preset selects
  `content-security`. Symlinked directories under `templates/` — C5. A dirty
  working tree — the named residual in Chunk C. `argv` length: 74 absolute paths
  is roughly 6 KB, far under `ARG_MAX`.
* **Known omissions, stated rather than implied.** (a) No human has read the 2502
  physical lines of the two newly-scanned files for security content; Bandit's
  verdict has been reproduced by three parties, which is a different thing. (b)
  The four `B607` findings — `git` invoked by name inside an adopter's repository
  — are recorded and deferred. (c) The trust-anchor guard is not extended to
  cover the new `install_manifest` import; it constrains only the `_MODULE_MAPPINGS`
  `ImportFrom`, and widening it is a change to a gate this plan does not own. (d)
  No test guards the union-vs-replacement monotonicity claim directly. (e) The
  interaction of C3's working-tree glob with parallel test runners and a dirty CI
  checkout is unexplored. (f) Whether re-pinning the three stale frozen entries
  should happen now or at the next supervised re-anchor is a Maintainer question
  this plan raises and does not answer.

## Verification

The concrete commands the implementation must pass. Run under the canonical
interpreter (`~/conda_envs/lhm/bin/python`, 3.13.13) with
`PYTHONDONTWRITEBYTECODE=1`; a different Python minor silently changes both the
suite figure and `Path.rglob`'s symlink semantics, which C5 depends on.

<!-- cairn:slot verification-commands -->
The standing gates Cairn runs before a change lands (the same ones CI
enforces):

* **Engine suite** — `python -m pytest bootstrap/tests` (the whole
  suite; scope to `bootstrap/tests/test_<surface>.py` while iterating,
  but the full suite gates the cut).
* **Prose integrity** — `python scripts/check_cairn.py` (internal link
  / anchor resolution + claim-path check over the Markdown tree).
* **Quality gate** — `python scripts/quality_gate.py` (order-
  independence + vendor-neutrality + redundancy; `--sub neutrality`
  alone for a doctrine / template wording change).
* **Write-time claim check** — `python scripts/claim_check.py <file>` over
  each proposal / plan / doc the change authored. **One file per
  invocation** — the checker takes a single path and exits 2 (usage) on
  more, so loop rather than passing a list.

Plan-specific gates (a security-lint budget, a doc-drift gate, the
model-selection mapping check `python scripts/check_model_selection.py`)
are added per plan when the change touches that surface.
<!-- cairn:end verification-commands -->

**Plan-specific gates, added here because this change touches those surfaces.**

* **The release gate itself** — `python bootstrap/security_check.py`. Expected
  `PASS`, Bandit line reporting **74** files. Baseline before Chunk B: 72.
* **The install-contract assertion** — `python bootstrap/scaffold.py --manifest`,
  diffed against a capture taken at the plan-open commit. **Expected empty.** 95
  data rows, `as_of 2026-08-03`.
* **The monotonicity check** — `sorted(scan_targets())` captured before Chunk A
  into the session scratch directory; after Chunk B, `set(pre) <= set(post)` and
  `len(post) - len(pre) == 2`.
* **The three-channel agreement on 44** — `git ls-files templates | grep '\.py$'
  | wc -l` (the git index), the working-tree glob (C3's oracle), and
  `install_manifest(modules=None)` verbatim `.py` count. All 44,
  `as_of 2026-08-03`. Three channels, one of which is the subject's; a
  disagreement is a finding wherever it appears.
* **The perturbation ledgers** — per chunk, in the commit body: the change made,
  the failure observed with its message, and the byte-identical restore verified
  with `git diff <path>` (empty).
* **The gate-integrity note** — after the last chunk, record in the commit body
  that `bootstrap/security_check.py`, `bootstrap/tests/test_security_lint.py`
  and `bootstrap/tests/test_security_check.py` now differ from their pinned
  sha256 in `bootstrap/tests/fixtures/gate_manifest.json`, so a later
  `_gate_manifest.py verify` will report three `FROZEN-MODIFIED` entries. Do not
  re-pin: that is a supervised act under `bootstrap/REANCHOR_RUNBOOK.md`.

### Gate-integrity accounting — measured, not predicted

The bullet above is a *prediction written before implementation, and it was
incomplete*: three `FROZEN-MODIFIED` rows are only half of what this plan's work
puts in front of the re-pin. The measured accounting is below and supersedes it.
The Maintainer re-pins from **this** table.

Measured by running, after the last edit of this plan's work,

```
~/conda_envs/lhm/bin/python3.13 bootstrap/tests/_gate_manifest.py verify
```

`as_of 2026-08-03`, under the canonical interpreter (3.13.13). The command
reports **`HOLD — 12 gate-integrity violation(s)`** over a working tree that
carries **three plans' work concurrently**. **Six rows are attributable to
`scan-coverage`; six are not.** The split is what makes the figure usable — a
re-pin taken from the raw 12 would silently absorb another agent's changes.

**Attributable to this plan (6 violations):**

| Class | File / node | Origin in this plan |
|---|---|---|
| `FROZEN-MODIFIED` | `bootstrap/security_check.py` | A1, B1–B3 |
| `FROZEN-MODIFIED` | `bootstrap/tests/test_security_lint.py` | A2, B4, C1–C8 |
| `FROZEN-MODIFIED` | `bootstrap/tests/test_security_check.py` | A3, A4, B5, D1–D3 |
| `COLLECTION-DROPPED` | `test_security_lint.py::test_scan_targets_cover_all_shipped_scripts` | B4's rename — the stale id |
| `COLLECTION-DROPPED` | `test_security_check.py::test_scan_targets_are_explicit_files_covering_shipped_surface` | D1's rename — the stale id |
| `SKIP-XFAIL-NEW` | `test_security_check.py::test_fail_closed_on_a_missing_target_with_real_bandit` | A4's `@pytest.mark.skipif(not _bandit_available())` |

Three qualifications, each measured rather than assumed:

* **The two `COLLECTION-DROPPED` rows are renames, not lost coverage.** The
  manifest keys on node id and has no rename concept, so a rename registers as a
  drop plus an add. Both successor ids
  (`test_every_manifest_verbatim_py_is_scanned_by_some_path`,
  `test_scan_targets_are_explicit_files_and_name_the_expected_executables`)
  appear among the **11 `COLLECTION-ADDED` notes** this plan's two files produce
  — 9 genuinely new nodes (A3, A4, B5, C3–C8) plus those 2 successors. **Net
  collection change for this plan: +9, and no assertion was retired.** This is
  the one row class the pre-implementation prediction missed entirely, and it is
  the class a re-pin must handle explicitly: the two stale ids are removed, not
  carried.
* **The `SKIP-XFAIL-NEW` row does not skip here.** Bandit 1.9.4 is installed
  under the canonical interpreter, so A4 runs and passes; the manifest records
  the *marker*, not the outcome. Measured: `pytest
  bootstrap/tests/test_security_check.py bootstrap/tests/test_security_lint.py
  -q` → **17 passed, 0 skipped**. The marker is the file's existing idiom (the
  pre-existing `test_run_bandit_clean_with_bandit_present` carries the same one),
  so it is a new *row*, not a new *practice*.
* **`FROZEN-NEW`: zero.** This plan creates no file. The two Markdown files it
  edits (`bootstrap/SAFETY.md`, `SECURITY.md`) are **not** in the 164-entry
  `frozen_files` map — checked, not assumed — so Chunk E adds no gate row.

**Not attributable — concurrent work in the same tree**, listed so a re-pin
taken from this plan does not silently absorb it: `FROZEN-MODIFIED` for
`bootstrap/tests/test_lifecycle_contract.py`,
`bootstrap/tests/test_quality_gate_redundancy.py` and `scripts/quality_gate.py`,
plus three `SKIP-XFAIL-NEW` rows under
`test_quality_gate_redundancy.py::TestR6UnusedDef`. None of those files is in
this plan's *Scope*.

**The three live sha256, re-measured after every edit** (`shasum -a 256`,
`as_of 2026-08-03`), against the pins currently in
`bootstrap/tests/fixtures/gate_manifest.json`. Any earlier-quoted value for these
files that differs from these is wrong; these were taken last.

```
bootstrap/security_check.py
  pinned e937f782325bdf4ce9209f361737daa3fb0de413318a62713eae419bf3c96ec8
  live   e2d40dc1c6228d61bc91eb8faaa976b2dd24347208c7db1e2522c1fd2e4fe1d4
bootstrap/tests/test_security_lint.py
  pinned 15893daadab83ec6e96226aea0df2285ec5e47174d52e2de131786646d529437
  live   41a483075af8c2a9e007dfe1c2bf084fdc418ee1a44533bf431db22a7c284894
bootstrap/tests/test_security_check.py
  pinned fba271da95154044d48eb9924b558db10f3a8612c71cce7d3669d1e200167734
  live   d1815f0c8195c2af306141c2bc08dde8e226c01ed747ca17c3b494388f2065e1
```

**Do not re-pin from here.** Re-pinning is a supervised act under
`bootstrap/REANCHOR_RUNBOOK.md`; the live column is what that act should
reproduce, and a live value that does **not** match at re-pin time means the
tree moved between this measurement and the re-pin.

**Note on doc gates**: drift gates (broken references, stale renders,
snippets that diverged from their source) catch **drift**, not
**absence** of new doc updates. Confirm each doc named in Acceptance
was actually updated; the gates don't enforce that.

## Plan review — the brief, and why the tier is not discharged

*Required — External, security lens. Implementation does not start until a review
has landed under this heading.*

The tier is the proposal's declared trigger, not a judgement call. It is **not**
discharged by the External round the proposal already had: that round returned
SHIP against four verifications of items 1, 2 and the *Context* measurements, and
the Decision records in terms that *"no External reviewer has read the
replacement"* for item 3 — which is Chunk C, the part this plan spends most of
its length on.

**The three questions this review should aim at**, in descending weight:

1. **Is Chunk C's oracle actually independent, and does it fail in the states the
   plan claims?** Reproduce P-C1 — patch `bootstrap._scaffold.install._SKILLS_MAPPINGS`
   and confirm B4 stays green while C3 goes red naming exactly the two skills
   files. If B4 also goes red, the plan's central distinction is wrong. If C3
   stays green, Chunk C is decoration.
2. **Does the union survive as a union, and is anything guarding that?** The
   monotonicity guarantee is a property of the diff, not of any test. Attack it:
   find the refactor that shrinks the scan set while every test stays green, and
   say whether C3 catches it.
3. **Is Chunk A's fail-close correct and sufficient, and is the chunk order
   right?** The gate's "clean over N shipped file(s)" line counts requested, not
   scanned, targets. Check that A1 closes that, that no legitimate Bandit run
   populates `errors` (it is empty over both target sets today), and that landing
   A before B is actually necessary rather than tidy.

Two further things a reviewer is invited to strike rather than accept: the
[I2] absorption in Chunk D, which enlarges the proposal's *Touches* line by a
third frozen file; and C4/C5, the pinned count and the no-symlink assertion,
which are [I6b]/[I6c] corrections rather than proposal text.

> **The landed review appends here as a `### Plan review -- <reviewer> --
> YYYY-MM-DD` sub-heading** (plus a `### Sharpening` sub-heading if it raised
> findings). **Do not rename this heading to a bare `## Plan review`.** Measured
> for this plan, 2026-08-03, against scratch copies under a throwaway
> `dev/plans/` tree: with a bare `## Plan review` heading and the plan at
> `awaiting-plan-review`, `python tools/lifecycle_planner.py next <plan>` reports
> `[ok ] a '## Plan review' section has landed` — an *empty* section satisfies
> the gate. With the heading as written above, the same command reports
> `[MISSING]` until a real `###` review sub-heading lands. The checker matches a
> section *kind*, not a review; this heading is shaped so the gate cannot be
> satisfied by a placeholder.

## Code review

*Filled in after implementation commits land.* The reviewer is not the
implementing agent. Begin with `**Model**: <model or tier when known; "unknown"
if not.>` immediately below the section header (or below a `### Code review --
<reviewer> -- YYYY-MM-DD` sub-heading).

The falsification ledger this review owes, at minimum: independently repeat
P-C1 rather than re-trusting the implementing session's transcript; confirm each
perturbation's byte-identical restore with `git hash-object` against
`git rev-parse HEAD:<path>`; and confirm the two explicit registry loops in
`scan_targets()` are present and unmodified, since their retention is the whole
of the monotonicity argument.

## Plan review -- Gemini Flash (External, security lens) -- 2026-08-03

**Steelman.** This plan presents a remarkably detailed and rigorous design for ensuring Bandit release scans cover every Python script shipped by the scaffold engine. The central contribution is Chunk C's `_templates_py_on_disk()` oracle, which evaluates files physically present on disk in `templates/` rather than relying on `install_manifest()`.

### Concerns

* **[E1] Exclusions table hygiene (`_SCAN_EXCLUSIONS`).**
  While `_SCAN_EXCLUSIONS` is empty today, Chunk C introduces it to handle legitimate un-scanned files. To prevent `_SCAN_EXCLUSIONS` from becoming a silent fail-open side-door for unreviewed Python templates, C3(d) must strictly require non-empty rationale strings for every entry and ensure stale exclusions trip the suite.

### Covered

* **Oracle independence & perturbation P-C1 verification**:
  Tested the exact perturbation P-C1 in Python by removing the two skills lifecycle scripts (`templates/skills/_lib/lifecycle.py` and `templates/skills/_lib/lifecycle_planner.py`) from `bootstrap._scaffold.install._SKILLS_MAPPINGS`.
  - **B4 Oracle (Manifest-derived)**: evaluated to 42 files; `oracle_b4 - scan_targets()` was **empty** (`set()`), demonstrating B4 stays **GREEN** under perturbation.
  - **C3 Oracle (Disk-derived)**: evaluated to 44 files; `oracle_c3 - scan_targets()` went **RED**, reporting exactly `{'templates/skills/_lib/lifecycle.py', 'templates/skills/_lib/lifecycle_planner.py'}` as unscanned.
  - This empirically proves that Chunk C provides true structural independence from the registry/manifest data structures.

```
=== BASELINE AT HEAD ===
scan_targets() count at HEAD: 72

=== UNDER PERTURBATION: SKILLS REMOVED FROM MANIFEST ===
B4 Oracle (Manifest) count: 42
C3 Oracle (Disk) count: 44
B4 unscanned set under perturbation: set()
C3 unscanned set under perturbation: {'templates/skills/_lib/lifecycle.py', 'templates/skills/_lib/lifecycle_planner.py'}
```

### Not covered / low confidence

* Remediating the sixteen pre-existing LOW subprocess findings (`B404`, `B603`, `B607`) in the skills scripts is explicitly out of scope for this plan and remains unaddressed.

### Recommendation

**READY FOR IMPLEMENTATION.** The plan's sequencing, fail-closed Bandit error handling (Chunk A), and independent on-disk oracle (Chunk C) are verified and sound.

## Lasting-truth migration

*Filled in at archive time.* Per the
[Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home outside the
plan. The follow-ups this plan will owe a home: the struck registry census, the
four `B607` findings, the unguarded monotonicity claim, and the stale frozen
pins.

This section is append-only once written.

## Response to plan review -- Claude (author) -- 2026-08-03

**Model**: Claude Opus 5

**One finding, accepted in part — and the part that was not already covered is
the more dangerous half.** The reviewer's verdict was READY FOR IMPLEMENTATION;
that is not a reason to leave [E1] undisposed, and disposing it found a real hole.
Verified before answering, under the canonical interpreter
(`~/conda_envs/lhm/bin/python3.13`, 3.13.13), by reconstructing C1's helpers
verbatim from the plan text and running C3's assertions against candidate
exclusion tables — against the *post-Chunk-B* target set, since at HEAD the two
skills files make C3(b) red and mask everything else.

Also confirmed the reviewer independently reproduced P-C1 rather than restating
the plan's own numbers: their B4-green / C3-red-naming-exactly-two-files result
matches the plan's simulated prediction. That is the one result the plan asked a
reviewer to attack first, and it survived an independent run.

### [E1] Exclusions table hygiene (`_SCAN_EXCLUSIONS`) — **ACCEPTED (in part;
the rest ALREADY-COVERED, cited)**

*The finding.* `_SCAN_EXCLUSIONS` is empty today, but Chunk C introduces it as a
place to excuse un-scanned files. To stop it becoming a silent fail-open
side-door, C3(d) must require a non-empty rationale per entry, and a stale
exclusion — one naming a file that no longer exists, **or one that is now
scanned** — must trip the suite.

*Two of the three demands were already in the plan, and here is the text.* Chunk
C3 already reads: *"(d) every `_SCAN_EXCLUSIONS` key exists on disk and carries a
non-empty rationale, so an exclusion cannot outlive the file it excuses."* That
is the mandatory rationale and the file-no-longer-exists half of stale, both
already assertions rather than conventions. C2 already types the table as
*"path → mandatory rationale"*, and P-C6 already required both guards be shown
non-vacuous by a **run** perturbation, since an empty table makes them vacuous.
Reproduced: adding `{"templates/does_not_exist.py": "probe"}` fails the
exists-on-disk assertion, and `{"<a real path>": ""}` fails the rationale
assertion. So far the reviewer is describing the plan.

*The third demand is not covered, and it is the one with teeth.* "Is now scanned"
does not follow from (d). `_unscanned_disk_py` computes
`disk - scan_targets() - _SCAN_EXCLUSIONS`; if a key is already in
`scan_targets()`, the exclusion subtraction is a **no-op**, so the entry sits
there passing every assertion C3 makes. Measured — an entry that is on disk,
rationale'd, and already scanned:

```
shipped state: empty table                        -> GREEN
P-C6 case 1: absent from disk                     -> RED  (d) not on disk
P-C6 case 2: empty rationale                      -> RED  (d) empty rationale
THE GAP: on disk, rationale'd, ALREADY SCANNED    -> GREEN
```

It is not merely untidy. It is a **latch that arms itself silently and fires
later**, which is precisely the fail-open the reviewer named. With coverage for
that same file subsequently dropped from `scan_targets()` by a refactor:

```
regression, empty table          -> ['templates/modules/.../__init__.py']   RED: caught
regression, stale exclusion live -> []                                      GREEN: SILENT
```

That second line is the plan's own Defect-2 failure shape — a guard that cannot
fail — reintroduced through the exclusion table the plan added to be safe.

*The plan change.* **Chunk C3 amended**, adding a fifth assertion: *"(e) every
`_SCAN_EXCLUSIONS` key is **absent from** `_scan_targets()`, so an exclusion the
scan has since made redundant is deleted rather than left as a latch"*, with the
measurement recorded inline so a later reader sees why (e) is not a restatement
of (d). **Perturbation P-C6 amended** to a third case — a real path already in
`_scan_targets()`, with a plausible rationale — noted as *the* case that passes
(a)–(d), so it is the case that proves (e) carries weight. Re-verified against
the amended assertions: green on the empty shipped table, red on all three probe
cases, and case 3 fires on (e) alone.

Two things I deliberately did **not** do. I did not touch C2's "mirrors the
`ALLOWLIST` + `test_allowlist_entries_have_rationale` idiom" sentence, though the
mirror is now imperfect in Cairn's favour: that existing idiom at
`bootstrap/tests/test_security_lint.py:127` checks rationale non-emptiness only
and has no staleness guard at all, so C3(d)/(e) is strictly stronger than the
thing it copies. Whether the `ALLOWLIST` deserves the same staleness treatment is
a real question about a different guard, and it belongs in its own proposal, not
smuggled into this plan's scope. I also did not restate the invariant in
*Author-accounting* (*"modulo a rationale'd exclusion"*), which (e) strengthens
without changing.

### On the reviewer's "Not covered / low confidence" note

The note records that the sixteen pre-existing LOW subprocess findings
(`B404`/`B603`/`B607`) in the two newly-scanned skills scripts remain
unaddressed. **Genuinely out of scope, and it already has a durable home — no new
follow-up row needed.** *Scope* fences it explicitly (*"Remediating the sixteen
LOW subprocess findings … Recorded, not fixed"*, with the reason: bundling a
code-hardening contract into a coverage contract is what cost `identity-not-name`
a REVISE/SPLIT verdict), and *Lasting-truth migration* already names *"the four
`B607` findings"* among the follow-ups that must land somewhere outside the plan
before it can archive. The reviewer read the fence correctly; the archive
precondition is the mechanism that stops it being forgotten.

One honest caveat the plan should not lose: the four `B607` findings are the
subset with a real question behind them (`git` invoked by name inside an
adopter's repository), and the archive-time home is a *recording* obligation, not
a decision that they are safe. Whether that home is a new proposal or a row on a
tracker is the Maintainer's call at archive time.

## Maintainer amendment 2026-08-03 -- the three escalated findings, ratified

**Authorization, quoted verbatim:**

> I ratify the three findings the scan-coverage plan already carries: the Bandit errors fail-close [I1], absorbing bootstrap/tests/test_security_check.py into scope [I2], and the pinned count [I6c]. They are within scope as implemented. Record this as a Maintainer amendment on the plan and commit it.

Scribed by Claude on the Maintainer's instruction.

### What this settles

The author's Response to the Internal security review escalated three remedies
under *Findings the Decision did not see*, with the explicit instruction that
**"No plan should carry any of them under the current Decision."** This plan
carries all three anyway — a governance defect found when the escalated list was
re-read against the plan body, and recorded here rather than quietly absorbed.
This amendment closes the gap by authorizing what is already implemented:

| Finding | What it does | Where it lives |
|---|---|---|
| **[I1]** | `run_bandit()` fails closed when Bandit's JSON `errors` array is non-empty | Chunk A, rows A1–A4 |
| **[I2]** | `bootstrap/tests/test_security_check.py` enters scope | Chunks A, D |
| **[I6c]** | the on-disk `.py` count is pinned | Chunk C, row C4 |

### Two consequences the Maintainer is on record as accepting

* **The frozen-file footprint goes from two files to three.** [I2] brings
  `bootstrap/tests/test_security_check.py` into the gate-manifest frozen set,
  which enlarges the surface of the next supervised re-anchor. Small, but real,
  and it was named before this ratification was given.
* **[I6c] trips on growth by design.** The pinned count turns the dev suite red
  whenever a `.py` is added under `templates/` — *including when it is added
  correctly*. That trip-on-growth is the point of the shape, and it is now
  authorized rather than inferred.

### What this does not settle

Nothing about whether the implementation of these three is **correct**. This
amendment rules on *scope* — that the plan was entitled to carry them. Their
implementation is subject to the same verification as every other chunk, and at
the time of this amendment an independent re-audit has open findings against
Chunk E's prose (see the code-review record). Ratifying scope does not ratify
code.

Maintainer's instruction.

### What this settles

The author's Response to the Internal security review escalated three remedies
under *Findings the Decision did not see*, with the explicit instruction that
**"No plan should carry any of them under the current Decision."** This plan
carries all three anyway — a governance defect found when the escalated list was
re-read against the plan body, and recorded here rather than quietly absorbed.
This amendment closes the gap by authorizing what is already implemented:

| Finding | What it does | Where it lives |
|---|---|---|
| **[I1]** | `run_bandit()` fails closed when Bandit's JSON `errors` array is non-empty | Chunk A, rows A1–A4 |
| **[I2]** | `bootstrap/tests/test_security_check.py` enters scope | Chunks A, D |
| **[I6c]** | the on-disk `.py` count is pinned | Chunk C, row C4 |

### Two consequences the Maintainer is on record as accepting

* **The frozen-file footprint goes from two files to three.** [I2] brings
  `bootstrap/tests/test_security_check.py` into the gate-manifest frozen set,
  which enlarges the surface of the next supervised re-anchor. Small, but real,
  and it was named before this ratification was given.
* **[I6c] trips on growth by design.** The pinned count turns the dev suite red
  whenever a `.py` is added under `templates/` — *including when it is added
  correctly*. That trip-on-growth is the point of the shape, and it is now
  authorized rather than inferred.

### What this does not settle

Nothing about whether the implementation of these three is **correct**. This
amendment rules on *scope* — that the plan was entitled to carry them. Their
implementation is subject to the same verification as every other chunk, and at
the time of this amendment an independent re-audit has open findings against
Chunk E's prose (see the code-review record). Ratifying scope does not ratify
code.

This also closes three of the eleven items escalated across the three Responses
written on 2026-08-03. The remaining eight — three on `byline-classification`,
five on `agent-context-scrub` — are unaffected and stay undecided.


## Code review -- Antigravity (External, security lens) -- 2026-08-04

**Steelman.** Implementation commit `5c91c23` delivers `scan-coverage.md` Chunks A–E, closing the 63-day defect where `scan_targets()` missed the unconditionally shipped skills tools (`lifecycle.py` and `lifecycle_planner.py`). Chunk A hardens `run_bandit()` in `security_check.py` and `test_no_blocking_security_findings` in `test_security_lint.py` to fail closed when Bandit's JSON `errors` array is non-empty, preventing un-scanned files from reporting a false clean. Chunk B binds `scan_targets()` to `install_manifest(modules=None)` (all verbatim `.py` files in the manifest). Crucially, Chunk C builds an on-disk anti-drift oracle (`_templates_py_on_disk(root)` and `_unscanned_disk_py(root)`) that globs `templates/` independently of the registries, ensuring that registry perturbations or un-scanned files on disk immediately fail tests (`test_every_templates_py_on_disk_is_release_scanned`). Furthermore, `_SCAN_EXCLUSIONS` requires non-empty rationales, disk presence, and absence from `_scan_targets()` to prevent stale exclusion latches.

### Concerns

* **[E1] On-disk oracle sensitivity to un-tracked local scratch files.**
  Because `_templates_py_on_disk` walks the working tree on disk via `rglob("*.py")` rather than `git ls-files`, an uncommitted scratch `.py` file placed under `templates/` will immediately cause `test_every_templates_py_on_disk_is_release_scanned` to fail. As acknowledged in the plan's residual section, this is an intentional ergonomic tradeoff (forcing explicit decision/exclusion on unwired templates), but developers must be aware of it during local testing.
* **[E2] Supervised gate manifest re-anchor requirement.**
  Commit `5c91c23` modifies three frozen files (`bootstrap/security_check.py`, `bootstrap/tests/test_security_lint.py`, `bootstrap/tests/test_security_check.py`). While `pytest` remains 100% green, `_gate_manifest.py verify` flags these files as `FROZEN-MODIFIED`. Re-pinning `gate_manifest.json` remains a Maintainer-supervised step governed by `REANCHOR_RUNBOOK.md`.

### Covered

* **Empirical Verification of Replacement Oracle Perturbation**:
  - Perturbation P-C1 tested: patched `bootstrap._scaffold.install._SKILLS_MAPPINGS` in memory to strip the two `.py` entries.
  - Result: `test_every_manifest_verbatim_py_is_scanned_by_some_path` remained GREEN (proving it is only a conformance check), while `test_every_templates_py_on_disk_is_release_scanned` went RED naming `['templates/skills/_lib/lifecycle.py', 'templates/skills/_lib/lifecycle_planner.py']`.

```
$ ~/conda_envs/lhm/bin/python -c "
import bootstrap._scaffold.install as install_mod
from bootstrap.tests.test_security_lint import _unscanned_disk_py, CAIRN_ROOT
stripped = tuple(row for row in install_mod._SKILLS_MAPPINGS if not row[0].endswith('.py'))
install_mod._SKILLS_MAPPINGS = stripped
print('Unscanned on-disk py:', _unscanned_disk_py(CAIRN_ROOT))
"
Unscanned on-disk py: ['templates/skills/_lib/lifecycle.py', 'templates/skills/_lib/lifecycle_planner.py']
```

* **Pytest Suite Verification**:
  - Ran `pytest bootstrap/tests/test_security_lint.py`: 10 passed in 0.92s.
  - Ran full test suite `pytest bootstrap/tests`: 1790 passed, 0 failed, 3 warnings in 133.06s.

```
$ ~/conda_envs/lhm/bin/python -m pytest bootstrap/tests/test_security_lint.py
============================== 10 passed in 0.92s ==============================
```

* **Bandit Error Handling Verification**:
  - Verified `security_check.py:134-142`: `errors = report.get("errors") or []` prints errors to stderr and returns `1` before allowlist filtering.

* **Claim-check Verification**:
  - `claim_check.py`: verified clean output on `dev/plans/scan-coverage.md`.

```
$ ~/conda_envs/lhm/bin/python scripts/claim_check.py dev/plans/scan-coverage.md
claim_check: dev/plans/scan-coverage.md -- 2 path(s) exempted by claim-check-allow:
  dev/plans/scan-coverage.md: exempted `templates/optional/rogue.py` via claim-check-allow glob `templates/optional/rogue.py`
  dev/plans/scan-coverage.md: exempted `templates/_probe.py` via claim-check-allow glob `templates/_probe.py`
claim_check: dev/plans/scan-coverage.md -- OK, no claim-check flags.
```

### Not covered / low confidence

* Sixteen pre-existing LOW severity subprocess findings (`B404`/`B603`/`B607`) in `lifecycle.py` and `lifecycle_planner.py` remain un-remediated in accordance with the explicit scope fence, and are tracked as deferred follow-ups.

### Recommendation

**SHIP / PASS CODE REVIEW.** The implementation of `scan-coverage.md` is complete, verified by empirical perturbation testing, and robustly closes both defects.


### Figure reconciliation -- Antigravity -- 2026-08-04

- **Previously reported**: 1790 passed, 0 failed, 3 warnings in 133.06s.
- **Reconciliation baseline** (`7bb2072`): 1790 passed, 0 failed, 0 skipped, 0 xfailed, 3 warnings (single shared suite run across all six reconciliations).
- **Acceptance criteria met**: Yes.


