<!-- cairn-internal-ref-allow: doctrine/consolidation-review.md doctrine/rationale.md doctrine/proposals.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- The two paths below are illustrative pytest fixture files written into a `tmp_path`
     sandbox by the proposed tests (the fixture shape the shipped `TestR6UnusedDef` class
     already uses); they are deliberately absent from this repository and always will be. -->
<!-- claim-check-allow: scripts/x.py, scripts/__init__.py -->

# R6's unused-def detector is blind to `from X import Y`, so 11 of its 13 current alarms are false — and one of them says to delete the installer's security boundary

**Author**: Claude (Strategy)
**Model**: Claude Opus 5
**Date opened**: 2026-08-03
**Status**: proposed
**Touches**: one function in `scripts/quality_gate.py` (the R6 reference harvester) + new behavioral tests in `bootstrap/tests/test_quality_gate_redundancy.py` + one appended dogfood-log row in `doctrine/consolidation-review.md`. **No `AGENTS.md`, no doctrine rule, no shipped template, no install manifest, no gate manifest, no `bootstrap/_scaffold/` engine code.**
**Related**: `dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md:305-309` (Theme 3, item 4, "Our dead-code detector cries wolf"); the R6 dogfood-log rows at `doctrine/consolidation-review.md:79`, last appended 2026-05-28.
**Plan review**: not required — the accepted change is a single implementing commit: ~4 lines inside one function of a **dev-only, non-shipped** script, plus three regression tests and one log row. There is no plan, so there is no plan review. If the Maintainer prefers a plan anyway, Internal is the ceiling: no shipped-template, install-contract, doctrine-rule, gate-manifest, or security surface is touched (see *Rationale > Why this needs no Security Review*). Ratified at Decision.

## Context

Cairn's consolidated pre-release lint, `scripts/quality_gate.py`, carries a
sub-gate called **R6**: a standard-library AST ("abstract syntax tree" — the
parsed structure of a Python file) walk that flags top-level functions and
classes nothing in the scanned tree appears to use, so dead code gets deleted
instead of accumulating. Its message ends "…or delete it".

**R6 is broken, and it has been red for a while.** Run today against HEAD
`8d17d9a` under the canonical interpreter (Python 3.13.13):

```
$ python scripts/quality_gate.py --sub redundancy   # exit 1
  FAIL  scripts/_onboarding/cli.py:230: R6 def `derive_held_task_ids` is never referenced …
  FAIL  scripts/_onboarding/cli.py:247: R6 def `derive_completed_task_ids` …
  FAIL  scripts/_onboarding/prompts.py:124: R6 def `render_outcome_with_active_prompt` …
  FAIL  scripts/_onboarding/slotparse.py:202: R6 def `parse_seed_task_ids` …
  FAIL  bootstrap/_scaffold/_guard.py:108: R6 def `install` …
  FAIL  bootstrap/_scaffold/install.py:386: R6 def `render_compatibility_matrix` …
  FAIL  templates/modules/default-on/_onboarding/cli.py:230: … (+3 more twins)
  info  bootstrap/_scaffold/upgrade.py:86: R6 def `_find_cairn_root` …
  info  templates/modules/default-on/_lifecycle_metrics/subsystems.py:216: …
  info  templates/modules/default-on/_lifecycle_metrics/subsystems.py:253: …
```

**13 findings — 10 `fail`, 3 `info` (snapshot, as_of 2026-08-03).** Every one
of the 10 `fail` findings is false, and so is one of the three `info`
findings: **11 of 13 are false, 0 of the 10 gate-failing findings are true.**

### The single cause

`_collect_py_defs_and_refs` at `scripts/quality_gate.py:559` builds the
"referenced names" set by walking the AST and collecting two node types only
(`scripts/quality_gate.py:578`): `ast.Name` and `ast.Attribute`. A
`from X import Y` statement is neither. Python represents it as an
`ast.ImportFrom` node whose imported symbols live in `alias` child nodes, and
the walker never looks at them. Reproduced directly against the shipped
function:

```
$ python -c "…load quality_gate.py; feed it 'from ._guard import install as _g\n_g(1, 2)\n'…"
node kinds in a `from X import Y as Z` file: ['Call', 'Constant', 'Expr',
    'ImportFrom', 'Load', 'Module', 'Name', 'alias']
refs harvested from that file: ['_g']
'install' in refs -> False
```

So **any function whose only in-corpus reference is a package-facade
re-export is reported as dead.** That is not an exotic pattern here — it is
how every one of Cairn's split engine packages exposes its API. All 11 false
alarms are exactly this shape:

* `bootstrap/_scaffold/_guard.py:108` defines `install`; it is imported and
  called at `bootstrap/_scaffold/__init__.py:68` as
  `from ._guard import install as _install_engine_guard`.
* `bootstrap/_scaffold/install.py:386` defines `render_compatibility_matrix`;
  re-exported at `bootstrap/_scaffold/__init__.py:200`.
* the four `_onboarding` helpers are re-exported through the facade at
  `scripts/_onboarding/__init__.py:149` and its neighbours (and each has live
  test coverage under `bootstrap/tests/`, which R6 deliberately does not
  scan).
* `_find_cairn_root` is re-exported at `bootstrap/_scaffold/__init__.py:233`.

### Why this is worse than ordinary lint noise

The `install` finding is the sharp one. `bootstrap/_scaffold/_guard.py:108`
is the **engine import boundary** — the function that installs the
`EngineFinder` on `sys.meta_path` and refuses a polluted or out-of-tree
cached engine child (the SR1 containment control). It runs on every
`bootstrap/scaffold.py` invocation, which is to say on every adopter install.
R6 tells a reader, in `fail` severity, that it is never referenced and to
delete it. Deleting it would remove a security control *and* break the engine
import at `bootstrap/_scaffold/__init__.py:68`.

Four more of the ten point at `templates/modules/default-on/_onboarding/`, i.e.
at code the scaffold copies into an adopter's repository. "Delete it" there
would break the shipped onboarding module.

### What is not in scope (a withdrawn sibling finding)

Theme 3's item 5 (`dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md:310`)
alleged the same defect class in `tools/lifecycle.py` — a session-start help
text claiming "read-only". **It does not reproduce.** Commit `b8d9e0b`
("scaffold: correct session-start's self-description (F4)", 2026-07-22)
reworded the module docstring, the parser `description=`, and the
`session-start` subparser `help=` to name the one self-heal write plainly and
to scope the `--dry-run` claim to `session-end`, and pinned all three with
tests in `bootstrap/tests/test_lifecycle_cli.py`. Verified today: `python
tools/lifecycle.py --help` prints "Orientation gather (plus one idempotent
skills-fan-out self-heal write)…" with no "read-only" claim anywhere. That
half of the theme is **withdrawn**, and this proposal deliberately does not
carry it — one proposal, one contract.

## Proposal

Add `ast.ImportFrom` alias names to the reference set harvested by
`_collect_py_defs_and_refs` at `scripts/quality_gate.py:559`. Concretely, one
extra branch in the existing `ast.walk` loop at `scripts/quality_gate.py:578`:

```python
elif isinstance(node, ast.ImportFrom):
    # `from X import Y` binds Y as a reference to the def named Y in
    # module X.  The alias nodes are neither Name nor Attribute, so
    # without this branch a def whose only in-corpus reference is a
    # package-facade re-export reads as dead.
    for alias in node.names:
        refs.add(alias.name)
```

Nothing else in `_run_r6_redundancy` (`scripts/quality_gate.py:590`) changes:
the scan roots (`scripts/quality_gate.py:497`), the severity split, the
dunder / `Test*` skips, and the whitelist lookup against
`scripts/quality_gate_unused_def_whitelist.py` are all untouched.

**Two deliberate narrowings, both measured rather than assumed:**

1. **`ast.ImportFrom` only, not `ast.Import`.** `import x.y` binds a *module*
   name; any subsequent use already produces an `ast.Name` (`x`) and an
   `ast.Attribute` (`y`) that today's walker catches. Harvesting from
   `ast.Import` would inject module path components into the set as though
   they were symbol names — over-suppression with zero recall gain. Both
   variants were simulated against the real corpus and collapse it to the
   same residual set, so the narrower one wins.
2. **`alias.name` only, not `alias.asname`.** The def being matched is named
   `alias.name`; the local rebinding `alias.asname` is already an `ast.Name`
   at every use site. Adding it would silence unrelated defs that happen to
   share a local alias.

**Measured effect on the real corpus** (simulated in a scratch copy — no
repository file was modified — against HEAD `8d17d9a`, canonical interpreter
3.13.13, as_of 2026-08-03):

| | findings | `fail` | `info` |
|---|---|---|---|
| HEAD today | 13 | 10 | 3 |
| with the fix | 2 | 0 | 2 |

The two survivors are `_per_role_per_tier_summary`
(`templates/modules/default-on/_lifecycle_metrics/subsystems.py:216`) and
`_author_reviewer_matrix`
(`templates/modules/default-on/_lifecycle_metrics/subsystems.py:253`) — both
genuinely unreferenced anywhere in the tree, both `info` severity, and both
**out of scope here**. Whether they are dead code to delete or an unfinished
metrics feature to keep is a content decision about a shipped module, not a
decision about the detector; bundling it would put two contracts in one
proposal. This proposal leaves them surfaced for the next dogfood pass and
says so in the implementing commit body.

Also noted, not acted on: under the fix, the `iter_log` entry in
`scripts/quality_gate_unused_def_whitelist.py` becomes redundant — it is
re-exported at `templates/modules/team-gated/_intent/__init__.py:47` and
would go silent on its own. The sibling `check_text` entry stays load-bearing
(it has no facade re-export). Pruning the whitelist is deliberately not part
of this change: the whitelist is a stated contract with its own rationale
comments, and shrinking it is a separate call.

### Documentation / doctrine surface

* **`doctrine/consolidation-review.md`** — one appended row in the "Dogfood
  disposition log" table, disposition `fixed`, recording that the 2026-08-03
  R6 pass surfaced 11 false alarms of one shape and that the implementing
  commit corrects the gate. This is **not a doctrine change**: that file's own
  standing instruction is that "Each dogfood pass of `quality_gate.py` appends
  a dated table row naming the per-finding disposition." Appending the row is
  operating the doctrine, not amending it. The log's last R6 rows date to
  2026-05-28 (`doctrine/consolidation-review.md:79`); this pass is overdue for
  one either way.
* **`CHANGELOG.md`** — one line at the implementing commit, or deferred to the
  release-cut serialization point; Maintainer's call.
* **N/A, explicitly**: `AGENTS.md`, any `doctrine/` rule, any
  `templates/` file, `bootstrap/fidelity-check.md`, the gate manifest at
  `bootstrap/tests/_gate_manifest.py:138`, the lockfile schema, and
  `docs/`. `scripts/quality_gate.py` is Cairn's own non-shipped dev tooling
  (it is listed as such in the notice-install test's own-only set), so no
  adopter-facing document describes its internals. The one adopter-facing
  mention, `bootstrap/BOOTSTRAP.md:557`, names the `--sub neutrality`
  sub-gate only and is unaffected.

### Doctrine-change rate-limit

**Not applicable — this proposal changes no doctrine.** It changes four lines
of a dev-only lint and appends a row to a log the doctrine already instructs
each pass to append. No rule, process, or contract that a contributor follows
is altered, so `doctrine/rationale.md` > "How the doctrine evolves under
evidence" does not engage.

## Rationale

**Which workflow does it improve?** The pre-release quality pass. Running
`python scripts/quality_gate.py` (no `--sub`) today exits 1, and every
gate-failing line in the redundancy sub-gate is wrong. A gate that is
unconditionally red is a gate that gets waved through — and the same command
carries the **neutrality** sub-gate, which is a real release control
(`bootstrap/BOOTSTRAP.md:557`, `bootstrap/tests/_gate_manifest.py:138`). The
cost of the noise is not paid by R6; it is paid by whatever true finding sits
next to it.

**Postdoc-first.** The postdoc never runs `quality_gate.py` — it does not
ship. The effect on them is one hop away and still concrete:

1. Cairn's own pre-cut gate is red immediately before the v0.3 cut that
   the postdoc adopts, so the pass that is supposed to catch problems in the
   thing they install is the pass nobody can read.
2. Four of the ten false alarms name `templates/modules/default-on/_onboarding/`
   files — code that lands in the postdoc's tree — and advise deleting them.
3. One names the installer's own containment boundary
   (`bootstrap/_scaffold/_guard.py:108`), which executes during their install.

**Fix defects, build nothing new.** This adds no tool, no flag, no file, no
mechanism, and no configuration. It is four lines inside an existing function
that make an existing detector recognize an ordinary Python import form. It
is squarely defect-shaped, and it is the cheapest item in Theme 3.

**Why now?** The gate is red before a release cut, and the dogfood
disposition log has carried no R6 row since 2026-05-28 — the standing
practice has already lapsed once under the noise.

### Why this needs no Security Review

Stating this explicitly, because declining a tier deserves the same
justification as requesting one. Checked against every high-risk surface
named in `AGENTS.md`:

* **Scaffold / merge engine** — not touched. The change is confined to
  `scripts/quality_gate.py`; no file under `bootstrap/_scaffold/` is edited,
  so the AST attestation baseline does not move and
  `bootstrap/REANCHOR_RUNBOOK.md` does not engage. (R6 *reports on* engine
  files; it does not modify them.)
* **Vendor-neutrality** — a different sub-gate, untouched.
* **The install contract** — the fidelity manifest, gate manifest, lockfile
  schema, and `scaffold.py --manifest` are all untouched;
  `--sub redundancy` is not in the gate manifest.
* **License split / `bootstrap/PROVENANCE.md`** — untouched.
* **The local interpreter binding** — untouched; no subprocess, no path
  resolution, no `dev/.cairn/local-env.json` read.
* **`bootstrap/SAFETY.md`, `bootstrap/security_check.py`, the content
  scanner** — untouched. R6 is a hygiene lint, not a security control; the
  security controls over this surface are Bandit and `security_check.py`,
  neither of which R6 feeds.

The change's failure direction is worth naming because it is the *only*
argument for a security tier and it does not survive contact: adding names to
a reference set can only make R6 report **fewer** findings, never more, so the
worst outcome of a wrong fix is under-reporting dead code in a dev-only lint
that no adopter runs and no security gate consumes. Meanwhile the *current*
state is the security-adjacent one — the unfixed gate is what tells a reader
to delete `bootstrap/_scaffold/_guard.py`'s containment boundary. The fix
reduces that exposure; it does not create any.

## Alternatives considered

1. **Do nothing.** The gate stays unconditionally red, the dogfood log stays
   lapsed, and the standing advice to delete the engine's containment
   boundary stays on screen. Rejected: the defect is four lines wide and the
   cost is a release gate nobody can read.
2. **Add the 11 names to `scripts/quality_gate_unused_def_whitelist.py`.**
   Cheapest possible edit, and wrong in kind: the code is fine, the detector
   is broken. The whitelist matches on unqualified name corpus-wide, so
   whitelisting `install` silences every future def named `install`; the list
   would then grow once per facade re-export forever, and each entry is a
   permanent blind spot. Rejected — it converts a bug into recurring
   maintenance.
3. **Delete the R6 sub-gate.** A defensible reading of "an alarm that is
   always false should be removed". Rejected on evidence: R6 has caught real
   things (the 2026-05-28 ledger rows) and still surfaces two true findings
   today. Removing a working check to avoid fixing four lines is a bad trade.
4. **Replace the AST walker with a real import-graph / scope resolver.**
   Correct in principle, and a new mechanism — it collides head-on with "fix
   defects, build nothing new", and R6 is explicitly a heuristic surfacing
   candidates for human disposition, not an adjudicator
   (`doctrine/consolidation-review.md`). Rejected as overbuild.
5. **Harvest `ast.Import` and `alias.asname` too.** Simulated; produces the
   same residual set on this corpus while suppressing strictly more. Rejected
   as needless imprecision (see *Proposal > Two deliberate narrowings*).
6. **Downgrade every R6 `fail` to `info`.** Makes the gate green by making it
   toothless. Rejected: it hides the true findings along with the false ones.

*Maintainer preference during drafting*: the standing directions
"postdoc-first" and "fix defects, build nothing new" shaped the choice of
alternative 1-vs-4 above; they are direction, not a Decision.

## Evidence / verification plan

Everything below was run against HEAD `8d17d9a` under
`~/conda_envs/lhm/bin/python` (Python 3.13.13, the canonical interpreter),
as_of 2026-08-03. **No repository file was modified to produce it** — the fix
was simulated by monkey-patching a scratch-loaded copy of the module.

* **Defect reproduction.** `python scripts/quality_gate.py --sub redundancy`
  → exit 1, 13 findings, 10 `fail`. All 10 `fail` lines are R6 (grep for
  non-R6 `FAIL` in that sub-gate returns nothing), so the sub-gate is red
  *solely* because of R6.
* **Cause reproduction.** Feeding `from ._guard import install as _g\n_g(1, 2)\n`
  to the shipped `_collect_py_defs_and_refs` yields `refs == {'_g'}`;
  `'install' in refs` is `False`, while the file's AST provably contains
  `ImportFrom` and `alias` nodes.
* **Falsity of each alarm.** Each of the 11 was traced to a live
  `from … import …` re-export or a live call site, listed under *Context*.
* **Effect of the fix.** Simulated harvester → 2 findings, 0 `fail`, 2 `info`
  (the table under *Proposal*).
* **No regression in the existing contract.** All five fixtures from the
  shipped `TestR6UnusedDef` class were re-run against the patched harvester
  and produce **byte-identical** finding sets: the unreferenced def still
  fails, the referenced defs stay silent, the whitelisted argparse callback
  stays silent, dunders stay silent, and the private helper stays `info`.
* **Non-vacuity of the proposed new test.** A two-file fixture
  (`scripts/x.py` defining `public_api`; `scripts/__init__.py` containing
  `from .x import public_api`) yields **one `fail` finding on `public_api`
  under HEAD** and **zero under the fix**. The test therefore fails today and
  passes after — it cannot pass vacuously.
* **Baseline for the touched test file.** `python -m pytest
  bootstrap/tests/test_quality_gate_redundancy.py` → 9 passed, as_of
  2026-08-03.

**Docs delivered**: the `doctrine/consolidation-review.md` log row named
under *Documentation / doctrine surface*. **Examples / smoke checks**: named
below. **Tests**: named below.

### Author-accounting — invariants, failure modes, edge cases

Triage says this is a routine mechanical change (no public API, no config
contract, no protected schema, no new abstraction), so a bare N/A would be
in-form. A short real block is more useful, because the interesting property
of a detector fix is its failure *direction*:

* **Invariant** — R6's finding set on the real corpus is exactly the two
  `info` findings listed above until a genuinely unreferenced def is added.
  *Enforced by*: the new re-export tests plus the five retained fixtures in
  `bootstrap/tests/test_quality_gate_redundancy.py`; observable at any time
  by running `--sub redundancy`.
* **Invariant** — the whitelist contract is unchanged: whitelisted names are
  still suppressed by name, independent of the harvester. *Enforced by*: the
  retained `test_whitelist_suppresses_argparse_callback` fixture.
* **Failure mode** — **open, and intentionally so**: the harvester can only
  *add* names to the reference set, so a wrong fix under-reports. It cannot
  raise, cannot emit a false `fail`, and cannot affect any shipped or
  adopter-executed code path. There is no closed-failure path to add, because
  R6 surfaces candidates for human disposition and does not adjudicate.
* **Edge cases handled** — aliased import (`import Y as Z`); relative and
  absolute `from` imports (`node.level` is not consulted, so both work);
  star-import (`from X import *` yields `alias.name == "*"`, which matches no
  def name — harmless no-op); syntactically broken file (the pre-existing
  `SyntaxError` guard still returns empty sets).
* **Edge cases out of scope** — `__all__` string lists, `getattr`-style
  dynamic dispatch, and entry points declared in packaging metadata. None
  occur in the current corpus; all three remain whitelist territory, which is
  what the whitelist is for.
* **Public path → test mapping** — R6's only public entry point is the CLI
  (`python scripts/quality_gate.py --sub redundancy`), exercised end-to-end
  through the shipped CLI contract tests and, at the function level, through
  [`bootstrap/tests/test_quality_gate_redundancy.py`](../../bootstrap/tests/test_quality_gate_redundancy.py).
* **Known omission** — the two surviving `info` findings are left
  undispositioned by design (see *Proposal*). If the Maintainer would rather
  they were resolved in the same pass, that is a scope instruction, and it
  belongs in the Decision.

### Tests required

All in `bootstrap/tests/test_quality_gate_redundancy.py`, class
`TestR6UnusedDef`; no new test file.

1. **`test_re_exported_def_not_flagged`** — two-file fixture; a def whose only
   reference is `from .x import public_api` in a sibling `__init__.py` must
   produce no finding. *Proven non-vacuous*: yields one `fail` under HEAD.
2. **`test_aliased_re_export_not_flagged`** — same, with
   `from .x import public_api as _p`, matching the real
   `bootstrap/_scaffold/__init__.py:68` shape.
3. **`test_import_does_not_silence_an_unreferenced_def`** — negative control:
   a file containing an unrelated `from y import z` alongside a genuinely
   unreferenced def must still `fail` on that def. This is the test that
   catches over-suppression, which is the fix's only failure direction.
4. **The five existing `TestR6UnusedDef` fixtures pass unchanged** — no edits
   to them. Already confirmed by simulation; the suite re-confirms it.

Full suite after the change: `python -m pytest bootstrap/tests` under the
canonical interpreter (Python 3.13.x), with the figure named alongside the
interpreter in the commit body.

### Examples / smoke checks

* `python scripts/quality_gate.py --sub redundancy` → expect **exit 0**, two
  `info` findings, zero `fail`. This is the headline smoke: the sub-gate goes
  from red to green with its true findings intact.
* `python scripts/quality_gate.py` (all sub-gates) → re-run to confirm the
  redundancy sub-gate no longer contributes to the exit code, and to record
  what, if anything, the other two sub-gates still report.
* `python scripts/check_cairn.py` → the prose-integrity smoke for the
  `doctrine/consolidation-review.md` row.
* `python scripts/claim_check.py` on this proposal file.
* **N/A**: no scaffold smoke (`--summary` / `--dry-run` / `--manifest`) and no
  example-gallery run — the change touches no install path and nothing the
  examples demonstrate.

## Signals the change is wrong

* **Over-suppression.** A def that is provably dead stops being reported. The
  before/after finding sets in this proposal are the pinned reference: any
  name that goes silent other than the 11 listed is a regression. *Recovery*:
  narrow the harvest to relative imports only (`node.level > 0`), which covers
  every facade in the corpus and none of the cross-package cases.
* **A name collision bites.** Two different modules define the same symbol
  name, one is imported somewhere and the other is genuinely dead, and R6 goes
  quiet on the dead one. *Recovery*: this is the corpus-wide-name-set
  limitation R6 already had for `ast.Attribute` refs; if it ever produces a
  real miss, that is the evidence that would justify the resolver rejected as
  alternative 4 — file it in the dogfood log rather than patching around it.
* **The whitelist starts growing again with facade names.** That would mean
  the fix did not reach the real shape and something else is also invisible to
  the harvester. *Recovery*: re-open with the new shape as evidence.
* **R6 reports zero findings for several consecutive passes and nobody looks
  at the `info` tier.** The gate has quietly become decorative. *Recovery*: a
  separate call about whether `info`-tier R6 findings should be surfaced more
  loudly — deliberately not decided here.
* **The dogfood log stays lapsed anyway.** If the log picks up no new row
  after this pass, the noise was not the reason it lapsed, and the real
  problem is the practice, not the detector.
