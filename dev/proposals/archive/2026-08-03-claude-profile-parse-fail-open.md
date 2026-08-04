# The profile loader guesses: make the installer's one input boundary report or refuse

**Author**: Claude (Strategy)
**Model**: Claude Opus 5
**Date opened**: 2026-08-03
**Status**: accepted
**Touches**: `bootstrap/_scaffold/config.py` (the `_minimal_yaml_parse` fallback parser and `load_config`), `bootstrap/_scaffold/cli.py` (the profile-key report and the module docstring that `--help` prints), `bootstrap/BOOTSTRAP.md` (Appendix B schema rules), `bootstrap/tests/test_presets.py`, `bootstrap/tests/test_scaffold.py`, and the AST attestation baseline `bootstrap/tests/fixtures/scaffold_ast_baseline.json` (mandatory re-anchor — this touches `bootstrap/_scaffold/`)
**Related**: `2026-07-08-claude-broad-look-skeptical-review` (Theme 3, item 3 — "the one place the installer guesses instead of stopping"); `2026-07-11-claude-solo-legacy-adopter-path` (review finding R1, the first sighting of the same parser defect, worked around in prose only)
**Plan review**: required(External + External Security Review) — this changes behavior inside `bootstrap/_scaffold/`, the high-risk scaffold/merge engine named in `AGENTS.md`; it converts several fail-open readings of an untrusted input file into fail-closed refusals on the install contract; and it mandates an AST attestation re-anchor. Each of those is independently a Security-Review trigger under the proposal template's protected-contract list.

## Context

An adopter's **profile** — the small YAML file passed as `scaffold.py
--config` — is the installer's only substantive input. It names the
project, the test command, the governance preset, the six dimension
axes, and the module roster. Everything the scaffold writes into the
adopter's repository is downstream of how that one file is read.

*Glossary, first use.* **YAML** is a plain-text configuration format
(`key: value` lines). **PyYAML** is the standard third-party library
that parses it. Cairn ships **zero runtime dependencies**, so
`bootstrap/_scaffold/config.py` uses PyYAML *only if it happens to be
installed* and otherwise falls back to a ~55-line hand-written parser,
`_minimal_yaml_parse`, defined at `bootstrap/_scaffold/config.py:84`.
The **fallback is the path Cairn's own promise makes normal**: a
scientist who installs Cairn into a fresh stdlib-only environment gets
the hand-written parser, not PyYAML.

Two distinct defects live at that boundary, both reproduced at HEAD
(`3292f21`) on 2026-08-03 under the canonical interpreter (Python
3.13.13):

**(A) The two parsers read the same file differently, and the
installer's own documentation is written in the divergent style.** The
example printed by `scaffold.py --help` and the preset example in
`bootstrap/BOOTSTRAP.md` both put a trailing `# comment` on a
`key: value` line. PyYAML strips it; `_minimal_yaml_parse` keeps it as
part of the value. So the same profile installs two different trees
depending on an environment detail the adopter never chose. One of the
two outcomes fails *open*: exit 0, a warning buried in ~100 lines of
output, five fewer files installed.

**(B) A misspelled profile key is discarded in total silence.** There
is no list of recognized keys and no report of what was ignored. A
one-character typo in `preset:`, in `modules_add:`, or in an axis key
changes the installed governance apparatus with no error, no warning,
and — for two of those three — no visible difference in the
`--summary` acceptance artifact the Maintainer is told to read before
installing.

Defect (A) is not new. It was caught on 2026-07-11 as a **blocking**
review finding on a different artifact, and the response was to fix
the prose in that one recipe. A sweep of the tracked tree on
2026-08-03 shows the same shape still shipping in two adopter-facing
files, including the installer's own `--help`. Prose fixes did not
hold, because nothing checks them.

Both defects land squarely on the POSTDOC-FIRST test: the first
external adopter's first two weeks begin with running this installer
against this documentation.

## Proposal

**One contract, one seam:** *the profile loader either reads a value
exactly as PyYAML would, or it refuses the line and says which line
and why; and it never discards a key without naming it.* Both parts
below change the same input-boundary function region in
`bootstrap/_scaffold/config.py`, carry the same gate set (engine
obligations + AST re-anchor + Bandit + External Security Review), and
are verified by the same test sweep. They are deliberately **not** a
bundle of unrelated work — but see *Alternatives* for the severance
line if a reviewer disagrees.

The two parts take **opposite dispositions on purpose**, and the
asymmetry is the argument, not an inconsistency:

* A **mis-parsed value** causes a *wrong write* — a corrupted project
  name rendered into the adopter's `AGENTS.md`, a forge reference
  silently omitted. Fail **closed**.
* An **unrecognized key** can only cause an *omission* — a module not
  installed, a token not filled. It also carries a real
  forward-compatibility cost (below). **Warn**, loudly and in the
  right places.

### Part A — the fallback parser reaches parity or refuses

Rework `_minimal_yaml_parse` and its helper `_list_item_text` (defined
at `bootstrap/_scaffold/config.py:98`) so that, for every input it
accepts, its result is equal to `yaml.safe_load`'s:

* **A1 — strip an unquoted trailing `#` comment on scalar lines.**
  The scalar branch at `bootstrap/_scaffold/config.py:133` does not do
  this; the list-item helper already tries to. Closing that internal
  inconsistency is the single change that makes the shipped `--help`
  and `BOOTSTRAP.md` examples parse identically under both parsers.
* **A2 — fix the unbalanced unquote.** Both branches call
  `.strip('"').strip("'")`, which removes a *legitimate* trailing
  quote character from any value that ends in one. Replace with a
  single balanced unquote (strip only a matching leading+trailing
  pair).
* **A3 — make comment-stripping quote-aware**, in one shared helper
  used by both branches, so a `#` inside a quoted value survives.
* **A4 — refuse, with a `<path>:<line>:` message, any construct the
  parser cannot represent faithfully.** `load_config` (at
  `bootstrap/_scaffold/config.py:147`) already raises on a non-mapping
  document; this extends the same fail-closed posture down to the line
  level. The refusal list, each entry with its demonstrated or
  by-construction divergence:
  * a flow collection with content — `modules: [a, b]` or `{a: 1}`
    (demonstrated: fallback yields the literal string);
  * a **nested mapping** — an indented `key: value` under a bare
    `key:` (demonstrated: fallback yields `[]`, silently dropping the
    whole sub-tree);
  * a **tab-indented** line (demonstrated: PyYAML raises, fallback
    accepts — the fallback is *more* permissive here, so neither
    parser is a subset of the other);
  * `key:value` with **no space** after the colon (demonstrated:
    PyYAML yields a plain scalar and `load_config` then raises;
    fallback silently manufactures a mapping);
  * a bare YAML-1.1 **boolean or null** as a value — `yes`, `no`,
    `true`, `false`, `on`, `off`, `null`, `~` (demonstrated:
    `forge: no` is `False` under PyYAML, `'no'` under the fallback);
    the message tells the adopter to quote it;
  * anchors, aliases, tags, and block-scalar indicators — `&`, `*`,
    `!`, `|`, `>` (**not individually demonstrated**; refused as
    unsupported-by-construction, stated plainly so a reviewer can
    challenge the inclusion);
  * a **second YAML document** after a `---` separator (a single
    leading `---` is verified equivalent today and stays accepted).

  **Explicitly out of scope, with evidence:** bare integers diverge
  (`3` vs `'3'`) but the divergence is *inert* — every engine consumer
  of a profile value passes it through `str()` before use. Reproducing
  YAML's full typed-scalar coercion in a stdlib fallback is exactly
  the "reimplement PyYAML" trap this proposal avoids. Named here so
  the omission is a decision, not an oversight.

* **A5 — the refusal message must be actionable without PyYAML.**
  "Install PyYAML" is not an acceptable remedy in a zero-dependency
  project. Every refusal names the line, the construct, and the simple
  rewrite (`modules: [a, b]` → a `- ` list; `forge: no` → `forge: "no"`).

### Part B — the loader reports the keys it did not recognize

* **B1** — add one module-level constant to
  `bootstrap/_scaffold/config.py`: `RECOGNIZED_PROFILE_KEYS`, the union
  of `KNOWN_TOKENS`, the six `_AXES` keys, and the five structural keys
  the engine reads (`preset`, `modules`, `modules_add`,
  `modules_remove`, `forge`). This is a **derived** constant, computed
  from the existing definitions, not a fourth hand-maintained list that
  can drift — with a test asserting it stays derived.
* **B2** — add one pure function,
  `unrecognized_profile_keys(cfg) -> list[str]`. No filesystem, no
  mutation.
* **B3** — `bootstrap/_scaffold/cli.py` prints, when the list is
  non-empty, one warning naming every unrecognized key *and* the full
  recognized set on the next line, so a `presets:` / `preset:` typo is
  visible by inspection.
* **B4 — put the warning where it is actually read.** Today's
  `[WARN] ... unfilled token(s) remain` fires at output line 97 of an
  install, after every write, exit 0. Verified 2026-08-03. So the new
  warning goes in **three** places: the `--summary` acceptance
  artifact (which exists precisely to be read before installing), the
  pre-write section of the install run, and the end-of-run summary
  block. "Warn loudly" is a placement claim, and this is the placement.
* **B5 — no refusal.** Argued in *Rationale*, not assumed.

### Part C — the durable guard against prose drift

Add a sweep test: every profile-YAML block in a tracked Markdown file
plus the `bootstrap/_scaffold/cli.py` module docstring (the text
`--help` prints) is parsed through **both** parsers and asserted equal.
This is the mechanism the strategy note itself calls for — a check
that fails when a hand-maintained example falls behind. It is what the
2026-07-11 prose-only fix lacked, and why the same defect is still
shipping today.

### Documentation / doctrine surface

* `bootstrap/BOOTSTRAP.md` — the "Schema rules" list in the preset
  section gains the fallback parser's refusal list, stated as a
  contract an adopter can rely on. The two divergent example lines at
  `bootstrap/BOOTSTRAP.md:734` and `bootstrap/BOOTSTRAP.md:739` become
  *correct* under Part A rather than needing rewriting — that is a
  deliberate design goal, not a coincidence.
* `bootstrap/_scaffold/cli.py` module docstring — the `--help` text.
  Its `forge:` example likewise becomes correct under A1.
* **Descriptive layer** (`docs/`) — no change. **Deliberation layer**
  — this proposal and its plan. **Governing layer** (`AGENTS.md`) — no
  change: nothing here alters how a contributor works.
* The **published install manifest** (`scaffold.py --manifest`) and
  the **fidelity manifest** are byte-unchanged — no file enters or
  leaves the install set. The *behavior* of reading a profile changes;
  the *contract of what gets installed* does not. Both statements are
  gated in *Evidence*.

### Doctrine-change rate-limit

This proposal changes a documented contract (`BOOTSTRAP.md` schema
rules), which the proposal template lists under the invariant kernel.
It clears the gate on **recurrence** — the same failure shape twice in
a rolling window:

1. **2026-07-11** — `2026-07-11-claude-solo-legacy-adopter-path`,
   review finding R1, *blocking*: a shipped copy-pasteable profile did
   not parse under the fallback because of trailing scalar comments.
   Remedy applied: rewrite that one document's prose.
2. **2026-08-03** — this reproduction: the identical shape still ships
   in `bootstrap/BOOTSTRAP.md` and in the installer's own `--help`.

The recurrence *is* the evidence that the first remedy was the wrong
layer. A prose fix cannot hold a property that nothing checks.

## Rationale

**Which adopter workflow does it improve?** The first one. A postdoc's
day-one sequence is: read `BOOTSTRAP.md`, copy the preset example,
run `scaffold.py --summary`, run the install. Today, on a stdlib-only
interpreter, step three prints:

> `error: unknown preset 'collaborative-team        # solo-greenfield | collaborative-team | high-rigor-legacy'; choose one of collaborative-team, high-rigor-legacy, solo-greenfield.`

An error that rejects a preset and then lists that same preset as a
valid choice is not a diagnosable failure — it reads as a broken tool.

**What contract does it clarify?** That the profile is the install
contract's *input*, and an input boundary that guesses is not a
contract. `load_config` already fails closed on a non-mapping
document; A4 extends that same posture consistently rather than
inventing one.

**Reproducibility.** Cairn's pitch to research-software teams is a
recorded, reviewable process. An installer whose output depends on
whether an unrelated library is present in the ambient environment is
the opposite of that: two colleagues running byte-identical commands on
the same profile get different trees, and neither is told.

**Why now?** Pre-first-external-adopter is the last moment this is
free. After adoption, changing how a profile is read is a migration.

**Against FIX DEFECTS, BUILD NOTHING NEW.** Stated plainly: Part B
adds a constant, a pure function, and a warning line. That is a new
code path. The defect-shaped framing is that the CLI **already
reports every other resolution decision it makes** — preset expansion,
staffability, default-on fallback, unknown forge, optional templates,
unfilled tokens. The set of profile keys it honored is the one
resolution decision it performs silently. B is filling a hole in an
existing reporting behavior, not adding a mechanism. Parts A and C are
unambiguously defect repair. If a reviewer judges B to be new
construction anyway, it is the severable part (see *Alternatives*).

**Why warn rather than refuse on an unknown key.** The failure
direction that matters is *older engine, newer profile*. Cairn ships
an upgrade path that re-reads a committed `dev/.cairn/profile.yml`,
and `bootstrap/PROVENANCE.md`'s own warning contemplates scaffolding
from a non-tagged source — so a profile written against a newer Cairn
meeting an older `scaffold.py` is a supported situation, not an
exotic one. `bootstrap/_scaffold/config.py:47` states the intent
directly: unknown keys are ignored "so that future tokens do not break
old configs." A hard refusal converts an inert forward reference into
a full stop whose only remedy is editing a file the adopter may not
own. There is a second, quieter hazard:
`_resolve_current_profile` in `bootstrap/_scaffold/upgrade.py` wraps
`load_config` in a bare `except Exception` and falls back to the
lockfile profile. A stricter loader would push more adopters into that
*silent* fallback during an upgrade — trading a loud install-time
problem for a quiet upgrade-time one. That interaction alone makes
"refuse unknown keys" the wrong call, and it is a hazard Part A must
also account for (below).

## Alternatives considered

1. **Do nothing.** Rejected. The failure has already recurred once
   after a fix, it is in the installer's own `--help`, and it lands on
   the first external adopter. The strategy note's framing is exactly
   right: an installer that guesses on its main input undercuts the
   security story the project is telling.

2. **Fix only the three divergent documentation lines.** This is the
   2026-07-11 remedy. Rejected because it has already been tried and
   already failed: the identical shape is still shipping 23 days
   later, in files a reviewer reads constantly. Prose cannot hold an
   invariant.

3. **Require PyYAML.** Rejected on the strongest possible grounds:
   zero runtime dependencies is a headline promise to adopters, and
   `bootstrap/DEPENDENCY_BUDGET.md` governs additions. This would trade
   a parser defect for a broken promise.

4. **Delete the fallback and refuse to run without PyYAML.** A
   coherent fail-closed design — one parser, no divergence class at
   all. Rejected for the same reason as (3), plus it is strictly worse
   for the target audience: a scientist on a locked-down cluster
   Python is precisely who cannot `pip install`.

5. **Refuse unrecognized profile keys (fail-closed on Part B).**
   The strongest rejected option, and the one a reviewer should press
   hardest on. Rejected for the forward-compatibility and
   silent-upgrade-fallback reasons argued above. Named here rather
   than assumed away, per the drafting brief.

6. **Refuse only unknown keys within edit distance 1 of a recognized
   key that is itself absent** (`presets:` when `preset:` is missing).
   This has near-zero forward-compat cost — Cairn controls its own key
   names and would not ship a new key one character from an existing
   one. Genuinely tempting. Declined because it is a *heuristic* on an
   input boundary, and a heuristic is the category of thing this
   proposal exists to remove. A warning that prints both the
   unrecognized key and the recognized set gets the adopter unstuck
   without one.

7. **Add a `difflib.get_close_matches` "did you mean?" suggestion.**
   Declined. `difflib` appears nowhere in the shipped surface today;
   adding an import to the engine to produce a nicety collides with
   FIX DEFECTS, BUILD NOTHING NEW. Printing the recognized set beside
   the unrecognized key achieves the same outcome with no new import.

8. **Split this into two proposals (A+C, and B).** Legitimate. The
   parts share a file, a seam, a gate set, and a review tier, so they
   do not trip the "one plan cannot hold four gate sets" failure. But
   if the External review judges the dispositions too different to
   decide together, **Part B is the severable half**; A+C is the
   smaller, more urgent, more clearly defect-shaped change and can
   land alone. Flagged now so a reviewer does not have to discover it.

## Evidence / verification plan

All commands below were run at HEAD `3292f21` on 2026-08-03 under
`~/conda_envs/lhm/bin/python` (Python 3.13.13, PyYAML 6.0.3 present).
The no-PyYAML condition was produced by a `sys.meta_path` finder that
raises `ImportError` on `yaml`, asserted effective by checking that
`config._yaml is None` before the CLI was imported — the genuine
fallback branch, not a simulation. No file was written into the
repository; all scratch artifacts live outside it.

**(i) Unknown-key handling — reproduced, fail-open.** Four
single-character typos, each via `scaffold.py --summary --config`,
each exit 0, each silently different:

| profile line | intended | actual result |
|---|---|---|
| `presets: high-rigor-legacy` | 12-module high-rigor roster | 6 default-on modules; summary prints `Preset: (none -- literal module list)` |
| `module_add:` + `- security-review` | security-review installed | silently absent; summary is *identical* to a correct `solo-greenfield` run |
| `agent_teams: concurrent-multi-type` | axis override | silently ignored; no `dual-review`, no `coordination-tiers`; summary identical |
| `project_nmae: "PostdocProject"` | token filled | 20 installed files, as_of 2026-08-03, still carry the literal `{{project_name}}` |

The `module_add` and `agent_teams` rows are the sharpest: the
`--summary` acceptance artifact an adopter is told to inspect shows a
*missing line*, which is not observable. The `project_nmae` row is
partly backstopped — a real install prints `[WARN] 2 unfilled
token(s) remain` — but at output line 97, after every write, exit 0,
and the message reads "Add these to the profile config and re-run",
which is precisely what the adopter did.

**(ii) Parser divergence — reproduced, by execution.** Twenty-four
inputs run through `yaml.safe_load` and `_minimal_yaml_parse` side by
side. Divergent classes found (each row a distinct root cause):

| input | PyYAML | fallback | disposition today |
|---|---|---|---|
| `forge: gitlab   # gitlab \| github` | `'gitlab'` | `'gitlab   # gitlab \| github'` | **fail open** |
| `project_name: X   # note` | `'X'` | `'X   # note'` | **fail open** — corrupts the value |
| `preset: X   # note` | `'X'` | `'X   # note'` | fail closed, misleading message |
| `<axis>: v   # note` | `'v'` | `'v   # note'` | fail closed |
| `test_command: "pytest -k 'a # b'"` | `"pytest -k 'a # b'"` | `"pytest -k 'a # b"` | **fail open** — trailing quote eaten |
| `modules:` / `- "a # b"` | `['a # b']` | `['a']` | **fail open** — value truncated |
| `modules: [a, b]` | list | string | fail closed, wrong message |
| nested mapping | dict | `[]` | **fail open** — sub-tree dropped |
| tab-indented list item | `ScannerError` | accepted | fallback *more* permissive |
| `preset:solo-greenfield` | plain scalar → `load_config` raises | mapping | fallback *more* permissive |
| `forge: no` | `False` | `'no'` | type divergence |
| `some_count: 3` | `3` | `'3'` | inert (all consumers `str()`) |

**(iii) The `--help` example is among the divergent cases — confirmed,
and it fails open.** `bootstrap/_scaffold/cli.py:28` is the line
`forge: gitlab        # gitlab | github`, printed verbatim by
`scaffold.py --help`. Installing that profile (with `issue-capture`
selected) into two empty targets:

* PyYAML present → `Installing issue-capture gitlab reference ...`, exit 0
* PyYAML absent → `[warn] unknown forge 'gitlab        # gitlab | github' (known: github, gitlab); issue-capture reference not auto-copied.`, **exit 0**
* `diff` of the two installed trees: **5 files present in one and absent in the other**, all under `.gitlab/issue_templates/` plus `.gitlab/labels.yml`.

The stronger case, `project_name: Photosynthesis-Model   # the
postdoc's repo`, installs cleanly both ways (exit 0, exit 0) and
produces trees whose **11 files differ in content**, with the
adopter's `AGENTS.md` line 2 reading
`# AGENTS.md — Photosynthesis-Model   # the postdoc's repo`.

**And `BOOTSTRAP.md`'s own preset example is divergent.** Extracting
the fenced block at `bootstrap/BOOTSTRAP.md:734` and running the real
CLI: with PyYAML, a clean 12-module summary, exit 0. Without PyYAML,
exit 1 and the self-contradicting `unknown preset ...; choose one of
collaborative-team, ...` message quoted in *Rationale*.

**Sweep of the tracked tree, as_of 2026-08-03**: exactly **3**
divergent-shape lines in adopter-facing files — two in
`bootstrap/BOOTSTRAP.md`, one in `bootstrap/_scaffold/cli.py`. Two
further hits are Python dataclass annotations (false positives) and
two are inside an archived proposal (a historical record, correctly
left alone).

**Suite baseline**: `python -m pytest bootstrap/tests` → **1556
passed**, as_of 2026-08-03, Python 3.13.13. Measured on a working tree
carrying another session's uncommitted work; re-measure at plan open.

### Author-accounting — invariants, failure modes, edge cases

**Invariants, and what enforces each:**

* *For every input `_minimal_yaml_parse` accepts, its output equals
  `yaml.safe_load`'s.* **Live invariant.** Enforced by a
  differential-parity property test over a table of profile-shaped
  inputs, skipped-with-a-message if PyYAML is absent (so the
  environment never silently voids it).
* *Every profile-YAML block shipped in a tracked Markdown file, and
  the `--help` docstring, parses identically under both parsers.*
  **Live invariant.** Enforced by the Part C sweep test — this is the
  drift-gate that the 2026-07-11 prose remedy lacked.
* *`RECOGNIZED_PROFILE_KEYS` equals the union of the definitions it is
  derived from.* Enforced by an equality test against
  `KNOWN_TOKENS`, `_AXES`, and the structural key set — so it cannot
  become a fourth hand-maintained list.
* *The published install manifest and the fidelity manifest are
  byte-unchanged.* Enforced by diffing `scaffold.py --manifest` before
  and after, plus the existing manifest tests.

**Failure modes, closed or open:**

* Unparseable line → **closed**: `ValueError` from `load_config`
  before any write. Intentional; this is the change.
* Unrecognized key → **open**: warned, install proceeds. Intentional;
  argued at length in *Rationale*.
* **The one genuinely dangerous interaction, named up front:**
  `_resolve_current_profile` in `bootstrap/_scaffold/upgrade.py`
  catches `Exception` from `load_config` and silently falls back to
  the lockfile profile. A stricter `load_config` therefore turns some
  *install-time loud failures* into *upgrade-time silent fallbacks* —
  a fail-open path this proposal would otherwise widen. **The plan
  must make that fallback print what it swallowed**, or the change
  makes upgrade quieter while making install louder. A reviewer should
  treat this row as the first thing to challenge.
* PyYAML absent → the fallback runs, as today. Unchanged.

**Edge-case inventory.** Empty profile (`{}`): accepted, default-on
path, unchanged. Empty file (zero bytes): `load_config` already
raises. `modules: []`: verified equivalent under both parsers today;
must stay equivalent. Comment-only file: verified equivalent. Single
leading `---`: verified equivalent, stays accepted. CRLF line endings:
**not tested — an explicit gap for the plan.** Non-UTF-8 profile: out
of scope (`read_text(encoding="utf-8")` already raises). Bare integers:
divergent but inert, out of scope with evidence.

**Public-path → test mapping** (targets relative to this document):

* `_minimal_yaml_parse` and `load_config` → new parity and refusal
  tests in [`../../bootstrap/tests/test_scaffold.py`](../../bootstrap/tests/test_scaffold.py), which already houses the
  minimal-parser tests.
* `unrecognized_profile_keys`, `RECOGNIZED_PROFILE_KEYS`, and the
  shipped-documentation sweep → [`../../bootstrap/tests/test_presets.py`](../../bootstrap/tests/test_presets.py), which
  already houses `TestParserParity` and the forced-no-PyYAML
  subprocess pattern this work should reuse rather than reinvent.
* The engine package's AST attestation → [`../../bootstrap/tests/test_ast_attest.py`](../../bootstrap/tests/test_ast_attest.py),
  which globs every `*.py` under `bootstrap/_scaffold/` and therefore
  covers both changed files.

**Known omissions / intentionally untested edges.** Integer-scalar
divergence (inert, argued). CRLF handling (a named gap). The
anchor/alias/tag/block-scalar refusals are asserted by construction,
not by a demonstrated PyYAML disagreement — a reviewer may reasonably
ask that they be dropped from A4 or backed by a demonstration.

### Tests required

Both new-test homes are existing files; no new test module.

1. **Differential parity** (`test_scaffold.py`) — a table-driven test
   asserting `_minimal_yaml_parse(text) == yaml.safe_load(text)` for
   every accepted input, covering all twelve divergence rows above.
2. **Refusal** (`test_scaffold.py`) — each A4 construct raises with
   the offending line number and the construct named in the message.
3. **Regression pins for A2 and A3** (`test_scaffold.py`) — a value
   ending in a quote character, and a `#` inside a quoted list item.
4. **Shipped-documentation sweep** (`test_presets.py`) — every
   profile-YAML block in a tracked `.md` plus the `cli.py` docstring,
   both parsers, asserted equal. This test must **fail** against
   today's HEAD; a plan that lands it green is a plan that did not
   reproduce the defect.
5. **`RECOGNIZED_PROFILE_KEYS` derivation** (`test_presets.py`).
6. **Unrecognized-key warning placement** (`test_presets.py`) — the
   warning appears in `--summary` output *and* pre-write install
   output, and install still exits 0.
7. **End-to-end under a genuinely forced no-PyYAML interpreter**,
   reusing the existing subprocess pattern in `test_presets.py`:
   `BOOTSTRAP.md`'s preset example and the `--help` example each
   install to trees byte-identical to the PyYAML runs.
8. **AST attestation re-anchor** — mandatory, per
   `bootstrap/REANCHOR_RUNBOOK.md`. This is not optional cleanup: the
   baseline does not auto-update, and the plan carries the full
   supervised re-anchor obligation for the engine package.

### Examples / smoke checks

* `scaffold.py --manifest` diffed before/after — must be byte-identical.
* `scaffold.py --summary --config <profile>` and `--dry-run` on all
  three shipped profiles under `bootstrap/profiles/`, run twice: with
  PyYAML and with PyYAML blocked. Outputs must match across the pair.
* Two full installs of the `--help` example into empty targets, one
  per parser path, `diff -r` clean.
* `python scripts/check_cairn.py` for the `BOOTSTRAP.md` edit.
* `python scripts/claim_check.py` over this proposal and its plan.
* **Engine gates**: the Bandit gate over `bootstrap/_scaffold/`, the
  `vermin` floor check (declared floor 3.11 — the new code must not
  raise it), and `python -m pytest bootstrap/tests` against the
  re-measured baseline.

## Signals the change is wrong

* **An adopter's previously-working profile stops installing.** The
  A4 refusal list is too broad. Recovery: narrow it to the classes
  with a *demonstrated* divergence and drop the by-construction
  entries.
* **The upgrade path gets quieter.** If post-change upgrade runs
  silently fall back to the lockfile profile more often, the fail-open
  hazard moved rather than closed. Recovery: make that
  `except Exception` report before anything else ships.
* **The unrecognized-key warning is ignored in practice.** If the
  first adopter still installs a typo'd profile, warning was the wrong
  disposition and Alternative 6 deserves a second look. Recovery: a
  follow-up proposal, not a quiet strictening.
* **The documentation sweep test becomes a nuisance** — contributors
  routing around it with skips or allowlists. That would mean the
  invariant is wrong, not the examples. Recovery: scope the sweep to
  blocks explicitly marked as adopter-copyable.
* **The parity table starts accreting special cases.** If closing
  divergences requires steadily more YAML knowledge in
  `_minimal_yaml_parse`, the fallback is drifting toward a
  reimplementation of PyYAML. Recovery: stop, and revisit Alternative
  4 — refuse rather than reimplement.
* **The AST re-anchor surfaces unexpected symbol motion.** Recovery:
  halt; an unexplained engine-baseline delta is a stop-the-line event,
  not a re-pin.

## Review -- Gemini Flash (External, Security Review) -- 2026-08-03

**Model**: Gemini 3.6 Flash (External, different-agent-type)
**Verdict**: SHIP (recommend ACCEPT; reproduced all 12 claimed divergence cases, verified `--help` example 5-file discrepancy, took position on warn vs refuse)

### Steelman

This proposal addresses a critical, long-standing reliability defect in Cairn's zero-dependency fallback parser (`_minimal_yaml_parse` in `bootstrap/_scaffold/config.py`). Because `_minimal_yaml_parse` fails to strip unquoted scalar comments (`#`), strips quotes unbalancedly, and handles comments inside quoted strings incorrectly, the exact profile example shipped in `scaffold.py --help` and `bootstrap/BOOTSTRAP.md` parses differently depending on whether the ambient Python environment has PyYAML installed.

Part A brings strict, deterministic parity between `_minimal_yaml_parse` and `yaml.safe_load` for all supported profile constructs and fails closed with clear `<file>:<line>` error messages on unrepresentable YAML structures. Part C introduces a mandatory sweep test asserting parity across all Markdown profile blocks and `--help` text, preventing prose drift from recurring.

### Concerns and Findings

* **[G1] (Reproduction of the Divergence Table — 12 of 12 Reproduced)**
  * *Verification:* Executed all 12 profile input cases through `yaml.safe_load` and `_minimal_yaml_parse` side-by-side using canonical interpreter `~/conda_envs/lhm/bin/python` (Python 3.13.13).
  * *Results:* Reproduced **12 out of 12** claimed divergence cases (100%).
  * *Verbatim Test Script & Output:*
    ```bash
    ~/conda_envs/lhm/bin/python -c "import yaml
    from bootstrap._scaffold.config import _minimal_yaml_parse

    cases = [
        ('forge: gitlab   # gitlab | github', 'forge: gitlab   # gitlab | github'),
        ('project_name: X   # note', 'project_name: X   # note'),
        ('preset: X   # note', 'preset: X   # note'),
        ('dual_review: v   # note', 'dual_review: v   # note'),
        ('test_command: \"pytest -k \'a # b\'\"', 'test_command: \"pytest -k \'a # b\'\"'),
        ('modules:\n  - \"a # b\"', 'modules:\n  - \"a # b\"'),
        ('modules: [a, b]', 'modules: [a, b]'),
        ('parent:\n  child: val', 'parent:\n  child: val'),
        ('\t- item', 'modules:\n\t- item'),
        ('preset:solo-greenfield', 'preset:solo-greenfield'),
        ('forge: no', 'forge: no'),
        ('some_count: 3', 'some_count: 3')
    ]

    for label, inp in cases:
        try: py_res = yaml.safe_load(inp)
        except Exception as e: py_res = f'{type(e).__name__}'
        try: fb_res = _minimal_yaml_parse(inp)
        except Exception as e: fb_res = f'{type(e).__name__}'
        print(f'{inp!r} | PyYAML: {py_res!r} | Fallback: {fb_res!r} | Div: {py_res != fb_res}')
    "
    ```
    Output:
    ```
    'forge: gitlab   # gitlab | github' | PyYAML: {'forge': 'gitlab'} | Fallback: {'forge': 'gitlab   # gitlab | github'} | Div: True
    'project_name: X   # note' | PyYAML: {'project_name': 'X'} | Fallback: {'project_name': 'X   # note'} | Div: True
    'preset: X   # note' | PyYAML: {'preset': 'X'} | Fallback: {'preset': 'X   # note'} | Div: True
    'dual_review: v   # note' | PyYAML: {'dual_review': 'v'} | Fallback: {'dual_review': 'v   # note'} | Div: True
    'test_command: "pytest -k \'a # b\'"' | PyYAML: {'test_command': "pytest -k 'a # b'"} | Fallback: {'test_command': "pytest -k 'a # b"} | Div: True
    'modules:\n  - "a # b"' | PyYAML: {'modules': ['a # b']} | Fallback: {'modules': ['a']} | Div: True
    'modules: [a, b]' | PyYAML: {'modules': ['a', 'b']} | Fallback: {'modules': '[a, b]'} | Div: True
    'parent:\n  child: val' | PyYAML: {'parent': {'child': 'val'}} | Fallback: {'parent': []} | Div: True
    'modules:\n\t- item' | PyYAML: 'ScannerError' | Fallback: {'modules': ['item']} | Div: True
    'preset:solo-greenfield' | PyYAML: 'preset:solo-greenfield' | Fallback: {'preset': 'solo-greenfield'} | Div: True
    'forge: no' | PyYAML: {'forge': False} | Fallback: {'forge': 'no'} | Div: True
    'some_count: 3' | PyYAML: {'some_count': 3} | Fallback: {'some_count': '3'} | Div: True
    ```

* **[G2] (Confirmation of `--help` Example Discrepancy & 5-File Installation Delta)**
  * *Verification:* Executed `scaffold.py` against identical profile carrying `forge: gitlab        # gitlab | github` in two scratch targets under `/tmp`: one with PyYAML active and one with PyYAML import blocked.
  * *Result:* **CONFIRMED.** Both runs exit 0. The PyYAML install writes 75 files; the fallback install writes 70 files (differing by **exactly 5 files** under `.gitlab/issue_templates/` and `.gitlab/labels.yml`).
  * *Verbatim Test Script & Output:*
    Executed via in-process meta-path import blocker under Python 3.13.13:
    ```
    === INSTALLATION COMPARISON RESULTS ===
    Files in PyYAML target: 75
    Files in Fallback target: 70
    Difference count (PyYAML only): 5
    Files present in PyYAML target but missing in Fallback target:
      - .gitlab/issue_templates/Bug.md
      - .gitlab/issue_templates/Friction.md
      - .gitlab/issue_templates/Gap.md
      - .gitlab/issue_templates/Wish.md
      - .gitlab/labels.yml
    ```

* **[G3] (Judgment on Unknown-Key Handling: Warn-Loudly vs. Refuse)**
  * *Analysis:* The proposal advocates for "Warn-Loudly" on unrecognized keys (Part B5) to protect forward compatibility when an older Cairn engine reads a newer profile carrying future keys.
  * *Position:* **REFUSE (fail closed) should be the default, with an explicit opt-out.**
    * *Rationale:* As demonstrated in Evidence item (i), typos in profile keys (`presets:`, `module_add:`, `project_nmae:`) cause silent misconfigurations, dropped modules, or un-substituted tokens while exiting 0. In automated setups or fast adoption runs, warnings buried in CLI output are easily missed.
    * *Forward Compatibility:* True forward compatibility is better served by either an explicit `allow_unknown_keys: true` profile flag or an explicit CLI flag (`--allow-unknown-keys`), rather than defaulting the primary installer input boundary to fail-open on misspelled keys.
    * *Upgrade Fallback Risk:* The proposal correctly highlights that `_resolve_current_profile` in `upgrade.py` catches `Exception` and falls back to the lockfile profile. That exception handler should be narrowed or made explicit so that profile typos fail closed at install time while upgrades handle schema evolution cleanly.

### Covered (Lenses Swept & Verbatim Executions)

All commands executed under canonical interpreter `~/conda_envs/lhm/bin/python` (Python 3.13.13).

1. **Divergence Table Parity Sweep (12 Cases):**
   * *Command:* Executed side-by-side comparison script over `yaml.safe_load` vs `_minimal_yaml_parse`. All 12 outputs match proposal table.
2. **`scaffold.py --help` Example Differential Install:**
   * *Command:* Installed profile with `forge: gitlab        # gitlab | github` into `/tmp` scratch targets under PyYAML vs forced stdlib fallback. Verified 5-file delta.

### Not Covered / Low Confidence (Negative Space)

* **AST Attestation Baseline Re-Anchor:** The proposal requires an AST attestation baseline re-anchor for `bootstrap/_scaffold/config.py` and `cli.py`. Since no code edits have been made yet, the AST attestation baseline re-anchor remains un-derived.
* **CRLF Line Endings:** Profile parsing with CRLF line endings was not tested; the behavior of `_minimal_yaml_parse` on CRLF input remains an open edge for implementation.

## Decision (placeholder -- superseded by the Decision at the end of this file)

*(Awaiting the Maintainer. The proposal has cleared External Security Review. The Maintainer may accept the proposal to proceed with plan creation.)*

## Response -- Claude (author, to External Security Review) -- 2026-08-03

**Model**: Claude Opus 5. Proposal-Response grammar (no implementing commits
exist). Every finding was re-run this session under
`~/conda_envs/lhm/bin/python` (Python 3.13.13, PyYAML 6.0.3), against the
working tree at HEAD `292e2c6` — a later commit than the `3292f21` the proposal
cites, because another session has committed since. No file was written into
the repository; all scratch artifacts live outside it, and every interpreter
invocation ran under `PYTHONDONTWRITEBYTECODE=1`.

* **[G1] accept -- reproduced 12/12, with one precision about what the sweep
  establishes.** I re-ran the twelve cases independently rather than reading
  the reviewer's transcript: every row diverges, and my outputs match the
  review's byte for byte (`{'forge': 'gitlab'}` vs
  `{'forge': 'gitlab   # gitlab | github'}`; `{'modules': ['a # b']}` vs
  `{'modules': ['a']}`; `ScannerError` vs `{'modules': ['item']}`; and the
  rest). Two precisions, neither of which weakens the finding: the script
  exercises the **divergence** column only — the *disposition* column (fail
  open / fail closed) is not touched by a side-by-side parse and remains
  author-asserted; and the review's row D substitutes `dual_review:` for
  `<axis>`, which is not one of the six axis keys (`_AXES` is `age`,
  `agent_team`, `complexity`, `human_team`, `language`, `size`). The parse is
  key-agnostic, so the reproduction holds regardless — but that row's "fail
  closed" claim went unverified by the review.

* **[G2] accept -- the five-file delta reproduces exactly; the absolute totals
  do not, and should not be cited.** Two installs of the `--help` example
  profile (`bootstrap/_scaffold/cli.py:28`) with `issue-capture` selected, one
  under PyYAML and one under a `sys.modules['yaml'] = None` blocker asserted
  effective before import: both exit 0, and the delta is exactly the five
  files the review names — `.gitlab/labels.yml` plus the four
  `.gitlab/issue_templates/` files — with the fallback run emitting
  `[warn] unknown forge 'gitlab        # gitlab | github' ...` verbatim. My
  totals were 83/78, not the review's 75/70; re-running with a single-module
  roster gave 63/58 and the same five-file delta. So the totals track the
  roster while the **delta is roster-invariant** — which strengthens the
  finding, but means "writes 75 files" is not a reproducible number and the
  Decision should not rest on it. I also re-verified the stronger case the
  review did not touch: `project_name: Photosynthesis-Model   # the postdoc's
  repo` installs at exit 0 both ways with an *identical file set* and **11
  common files differing in content**, the fallback tree's `AGENTS.md` line 2
  reading `# AGENTS.md — Photosynthesis-Model   # the postdoc's repo`.

* **[G3] narrow -- the default flips to refuse, as argued; neither proposed
  opt-out ships.** I reproduced the premise before conceding it: all four typo
  rows of Evidence (i) hold at exit 0, and the two sharpest are worse than the
  review's own framing. The review says warnings "are easily missed"; in fact
  for `module_add:` and `agent_teams:` there is **nothing to miss** — the
  `--summary` acceptance artifact is byte-identical to a correct
  `solo-greenfield` run (compared programmatically; both `True`), and the
  `module_add:` typo silently drops `security-review` from the roster. A
  one-character typo that removes a *security* module while leaving the
  acceptance artifact byte-identical is a fail-open default on the shipped
  security posture, which is what the Maintainer's direction of 2026-08-03
  puts out of bounds — verbatim: "Obviously we need to change the default
  security stance for all installations. Otherwise we are shipping a
  potentially dangerous tool." I also measured the availability cost I had
  merely asserted, and it is smaller than I claimed: no shipped profile under
  `bootstrap/profiles/` carries a key outside the recognized set (they use
  only `preset`, `project_name`, `test_command`), and both engine-side
  `profile.yml` writers emit only recognized keys — so refusal breaks nothing
  that exists today. Two corrections against myself: my *Rationale* said the
  remedy would mean "editing a file the adopter may not own", which is
  **wrong** — `dev/.cairn/profile.yml` is committed in the adopter's own
  repository (`bootstrap/_scaffold/lockfile.py:41`); and Alternative 5, which I
  called "the strongest rejected option", was rejected partly on that mistaken
  cost. **Where I decline the finding:** neither opt-out mechanism works. An
  `allow_unknown_keys: true` line is itself a profile key, so any engine older
  than the release introducing it refuses the flag as unrecognized — it cannot
  rescue the older-engine case for any Cairn shipped to date, only for engines
  released after it, in exchange for a permanent documented fail-open switch.
  And `--allow-unknown-keys` cannot reach the upgrade path at all:
  `bootstrap/_scaffold/upgrade.py:237` calls `load_config` with no argv
  plumbing, so the hatch would be absent in exactly the `upgrade` scenario
  G3's own third bullet is about. **Where I agree without reservation:** that
  third bullet. The bare `except Exception` at
  `bootstrap/_scaffold/upgrade.py:239` becomes a blocking, order-constrained
  precondition rather than a plan note — see *Revised proposal* below.

**Status.** The accepted findings reverse Part B's central disposition, so the
status moves to `revised`. Parts A and C are unchanged in substance; A4 is
narrowed to indicator-position refusals for a reason the review did not raise,
recorded below.

## Revised proposal -- Part B flips to fail-closed -- 2026-08-03

Append-only: nothing above is edited. Where this section and the original
*Proposal* conflict, **this section governs**.

The Maintainer direction quoted at G3 bears on Part B as a *premise* rather
than an open question, because Part B is a shipped default on the installer's
input boundary. It does not settle the question by fiat — the availability cost
still had to be measured, and G3 records that measurement — but it removes
"fail-open is the safe default" from the set of positions I may assume.

**Scope guard, stated so it cannot be mistaken for scope creep.** The
direction's own concrete referent — the `content-security` module being
selected by no preset — reproduces here (`_PRESETS` in
`bootstrap/_scaffold/config.py`, checked 2026-08-03: `content-security` is in
the roster of none of `solo-greenfield`, `collaborative-team`,
`high-rigor-legacy`). That roster lives in the *same file* this proposal
touches, which makes the temptation to fix it here real. I decline it. Preset
composition is a module-doctrine decision with a different evidence base than
an input-boundary contract, and it belongs to
`2026-08-03-claude-content-scan-detectors`, which owns the `content-security`
module surface, or to a dedicated preset-roster proposal. This proposal changes
**how a profile is read**, not **what a preset selects**.

### What changes

* **B3, B4 and B5 are withdrawn.** The three-placement warning and the
  "no refusal" argument go. In their place: **`load_config` refuses a profile
  carrying any key outside `RECOGNIZED_PROFILE_KEYS`**, naming every
  unrecognized key and printing the recognized set, before any write. B1 (the
  derived constant) and B2 (the pure function) stand unchanged — they are now
  the inputs to a refusal instead of to a warning.
* **Part B is now smaller, not larger.** One refusal in one function replaces a
  warning threaded into `--summary`, the pre-write section and the end-of-run
  block. That is a judgment about code volume, not a measurement — but it does
  mean the *FIX DEFECTS, BUILD NOTHING NEW* objection I raised against my own
  Part B in *Rationale* gets weaker under the flip, not stronger.
* **No opt-out ships.** Neither `allow_unknown_keys: true` nor
  `--allow-unknown-keys`; reasons at G3.
* **The asymmetry argument in *Proposal* dissolves.** A and B now take the
  *same* disposition. The two-part structure survives as a division of labor
  (value parity vs. key recognition), not as a deliberate opposition.
* **Alternative 5 is adopted** and its rejection paragraph superseded.
  Alternative 6 (the edit-distance heuristic) stays declined — a blanket
  refusal subsumes it and needs no heuristic. Alternative 8's severance line
  moves to the ordering constraint below.

### The precondition, promoted from "the plan must" to blocking

`bootstrap/_scaffold/upgrade.py:239` is a bare `except Exception` that silently
substitutes the lockfile profile when `load_config` raises. A stricter
`load_config` feeds it more exceptions. **Narrowing that handler so it reports
what it swallowed lands first, or in the same change — never after.** This is
now an ordering constraint on the plan, and it is the natural severance line if
the work is split.

One precision neither the proposal nor the review made: there are **two**
upgrade-side `load_config` callers and only one is the hazard.
`bootstrap/_scaffold/upgrade.py:1136` (the `init-lock` arm) already prints
`error loading dev/.cairn/profile.yml: <exc>` and returns 1 — loud, and correct
as-is. Only `_resolve_current_profile` swallows. Scope the fix to that one call
site rather than to "the upgrade path".

**Touches grows by one file** — `bootstrap/_scaffold/upgrade.py`. The gate set
does **not** grow: that file is inside `bootstrap/_scaffold/`, which the Bandit
gate and the AST attestation baseline (it globs every `*.py` under the package)
already cover.

### A4 is sharpened: indicator position, not character presence

The engine writes profile files itself. `_write_init_lock_profile_template`
(`bootstrap/_scaffold/upgrade.py:1084`) emits `size: <small|medium|large>` and
`test_command: "<your test command, e.g. pytest>"`. Verified 2026-08-03 under
Python 3.13.13: a synthesized init-lock template parses **identically** under
`yaml.safe_load` and `_minimal_yaml_parse` today. So A4's refusal of `|`, `>`,
`&`, `*` and `!` must be scoped to **indicator position** — the first character
of the value — because a refusal keyed on "the line contains `|`" would make
the engine refuse the file it just generated. The Part C sweep corpus gains
that generated template alongside the Markdown blocks and the `--help`
docstring.

### What this revision does *not* establish

* It closes the **misspelled-key** omission class. It does not close the
  adjacent one: a correctly-spelled key carrying an unrecognized *value*.
  Verified 2026-08-03 — a profile listing `- not-a-real-module` under
  `modules:` is accepted at exit 0 and the bogus name appears in the
  `--summary` roster. That is a separate defect and is outside this fence.
* The forward-compatibility cost of refusing is **argued, not measured**.
  Cairn has zero external adopters, so there is no field data in either
  direction. If a genuine older-engine/newer-profile break appears, the remedy
  is a follow-up proposal reversing this, not a quiet loosening.
* Parity does not make `_minimal_yaml_parse` a YAML parser. It makes it
  agree-or-refuse on the profile subset — the *Signals the change is wrong*
  row about accreting special cases stays live.
* CRLF handling remains untested and the AST attestation baseline remains
  un-derived, exactly as the review's negative space records.

## Review -- Claude (Internal, same-agent-type; security lens) -- 2026-08-03

**Model**: Claude Opus 5.

*Terms, first use.* **PyYAML** is the standard third-party YAML parsing
library; **the fallback** is `_minimal_yaml_parse`, the ~55-line hand-written
parser in `bootstrap/_scaffold/config.py` that runs when PyYAML is absent —
the path Cairn's zero-dependency promise makes normal. **Fail open** = a wrong
or missing value that still exits 0; **fail closed** = a refusal before any
write. **Parity** = the two parsers return equal results for the same text.
**Oracle** = the value a test compares against to decide pass/fail.

All commands below were run this session under `~/conda_envs/lhm/bin/python`
(Python 3.13.13, PyYAML 6.0.3), at working-tree HEAD `af4b2ee`, with
`PYTHONDONTWRITEBYTECODE=1`. No file was written into the repository; every
scratch artifact lives outside it. Where I say COULD NOT REPRODUCE I show what
I ran.

### Steelman

The proposal is right about the thing that matters most, and the External pass
and Response have already hardened it further. Its core insight — that a
profile is the *input* to the install contract, and an input boundary that
guesses is not a contract — is exactly the correct frame, and the recurrence
argument (`2026-07-11-claude-solo-legacy-adopter-path` finding R1 fixed in
prose, the identical shape still shipping 23 days later in the installer's own
`--help`) is the strongest possible case that a prose remedy cannot hold a
mechanical invariant. Part C, the sweep test, is the piece that makes the
change durable rather than another prose fix, and it is the piece a weaker
proposal would have omitted.

The revised Part B is well-argued and, on my reading, correct: the flip from
warn to refuse is backed by a *measured* availability cost (no shipped profile
under `bootstrap/profiles/` carries an unrecognized key — I confirmed this
independently, see *Covered*), and the Response's rejection of both proposed
opt-outs is sound reasoning I could not fault: an `allow_unknown_keys:` line is
itself a key an older engine would refuse, and a CLI flag cannot reach
`load_config` on the upgrade path because `bootstrap/_scaffold/upgrade.py:237`
has no argv plumbing. The Response's two self-corrections — that
`dev/.cairn/profile.yml` *is* the adopter's own committed file, and that the
five-file install delta reproduces while the absolute file totals do not — are
the kind of author accounting that makes a record trustworthy. The A4
sharpening to indicator position, prompted by the engine's own template writer,
is a genuine catch nobody asked for.

I did not find a reason to reverse any of that. What I found is that the
proposal's *specification* is not yet strong enough to be executed as written:
three of its own stated protections do not hold on the fallback path, and the
fix as described regresses inputs that are correct today.

---

### [I1] BLOCKING — the fail-closed posture A4 says it "extends" does not exist on the fallback path, and two edge-case rows in the record are false

The proposal twice grounds A4 in an existing guard:

> `load_config` (at `bootstrap/_scaffold/config.py:147`) already raises on a
> non-mapping document; this extends the same fail-closed posture down to the
> line level.

and, in *Rationale*:

> `load_config` already fails closed on a non-mapping document; A4 extends that
> same posture consistently rather than inventing one.

That guard is `if not isinstance(cfg, dict)` at `bootstrap/_scaffold/config.py:151`.
`_minimal_yaml_parse` initialises `result` as a dict at
`bootstrap/_scaffold/config.py:95` and returns it unconditionally at
`bootstrap/_scaffold/config.py:140` — it **cannot** return a non-dict. So on
the stdlib-only path the guard is unreachable. The posture A4 says it is
extending exists only when PyYAML is installed.

This is not academic. Three inputs that PyYAML refuses are silently accepted as
an empty profile by the fallback:

```
$ PYTHONDONTWRITEBYTECODE=1 ~/conda_envs/lhm/bin/python probe3.py          # PyYAML present
PyYAML seen by config module: <module 'yaml' from '.../site-packages/yaml/__init__.py'>
  zero-byte        -> REFUSED  ValueError: .../zero-byte.yml: expected a YAML mapping at the top level, got NoneType
  whitespace-only  -> REFUSED  ValueError: .../whitespace-only.yml: expected a YAML mapping at the top level, got NoneType
  comment-only     -> REFUSED  ValueError: .../comment-only.yml: expected a YAML mapping at the top level, got NoneType
  modules-{}       -> ACCEPTED {'project_name': 'X', 'modules': {}}

$ PYTHONDONTWRITEBYTECODE=1 ~/conda_envs/lhm/bin/python probe3.py block    # PyYAML blocked
PyYAML seen by config module: None
  zero-byte        -> ACCEPTED {}
  whitespace-only  -> ACCEPTED {}
  comment-only     -> ACCEPTED {}
  modules-{}       -> ACCEPTED {'project_name': 'X', 'modules': []}
```

(`probe3.py` blocks PyYAML with a `sys.meta_path` finder that raises
`ImportError` on `yaml`, and prints `config._yaml` to prove the branch was
taken before any `load_config` call.)

The proposal's *Edge-case inventory* therefore contains two false rows:

> Empty file (zero bytes): `load_config` already raises.

> Comment-only file: verified equivalent.

Neither holds on the path the proposal itself calls normal.

The sharpest instance is not the empty file — it is the **uniformly indented**
profile, which is what a copy-paste out of a documentation page or an email
actually produces:

```
$ PYTHONDONTWRITEBYTECODE=1 ~/conda_envs/lhm/bin/python probe9.py
config._yaml = None
profile text (every line indented two spaces): '  project_name: Photosynthesis-Model\n  preset: high-rigor-legacy\n'
load_config -> {}

$ ... python -c "import yaml; print(yaml.safe_load('  project_name: ...\n  preset: high-rigor-legacy\n'))"
{'project_name': 'Photosynthesis-Model', 'preset': 'high-rigor-legacy'}
```

With PyYAML the postdoc gets the twelve-module high-rigor tree. Without it they
get `{}` — the six default-on modules, exit 0, and the only signal is the
unfilled-token warning the proposal already measured at output line 97. That is
the *same* fail-open class the proposal exists to close, triggered by
indentation rather than by a typo, and it survives the change as specified.

**Ask.** A4's refusal list needs one more entry, and it is arguably the most
important one: *a document that produced no keys at all is refused, not
returned as `{}`*. Correspondingly, the two edge-case rows should be corrected
in an appended section rather than left standing.

---

### [I2] BLOCKING — A1 + A3 as specified regress inputs that are correct today, and the parity table is missing the row that proves it

A1 says the scalar branch must "strip an unquoted trailing `#` comment", noting
that "the list-item helper already tries to". A3 says to make comment-stripping
"quote-aware, in one shared helper used by both branches, so a `#` inside a
quoted value survives".

Quote-awareness is not the whole rule. YAML starts a comment at `#` only when
the `#` is at line start or preceded by whitespace; `a#b` is a plain scalar
containing a hash. The existing helper at `bootstrap/_scaffold/config.py:101`
does `.split("#")[0]`, which ignores that. So the helper A1 points at as the
model is *itself wrong in a way the proposal's twelve-row divergence table does
not record* — and a shared helper built to that model propagates the bug from
the list branch to the scalar branch, where today the behaviour is correct.

I implemented A1+A2+A3 as literally described (a quote-aware stripper plus a
balanced unquote) and ran the corpus through current vs. proposed:

```
$ PYTHONDONTWRITEBYTECODE=1 ~/conda_envs/lhm/bin/python probe5.py
input                          | PyYAML                    | CURRENT                   | PROPOSED
'project_name: a#b'            | {'project_name': 'a#b'}   | {'project_name': 'a#b'}   | {'project_name': 'a'}   <<< REGRESSION
'project_name: issue#42-tracker' | {'...': 'issue#42-tracker'} | {'...': 'issue#42-tracker'} | {'...': 'issue'}   <<< REGRESSION
'modules:\n  - a#b'            | {'modules': ['a#b']}      | {'modules': ['a']}        | {'modules': ['a']}   (still divergent)
'forge: gitlab        # gitlab | github' | {'forge': 'gitlab'} | {'forge': 'gitlab        # ...'} | {'forge': 'gitlab'}   (fixed)
'test_command: "pytest -k \'a # b\'"' | "pytest -k 'a # b'" | "pytest -k 'a # b"      | "pytest -k 'a # b'"   (fixed)
```

Two of the seven rows are cases where the fallback is **correct today and wrong
after the fix**. The `- a#b` row is a thirteenth divergence class, present at
HEAD, absent from the proposal's table, and *not* closed by A1/A3 as written.

This matters beyond tidiness because of the direction of the failure: A1's
stated purpose is to make the shipped `--help` and `BOOTSTRAP.md` examples
parse identically, and it does — while quietly corrupting any profile value
containing a hash without a preceding space. `project_name` and `test_command`
are exactly the free-text fields where that occurs.

**Ask.** Specify the whitespace rule explicitly in A3 (a `#` is a comment
start only at line start or preceded by space/tab); add the `- a#b` row to the
parity table; and pin **both** directions in the Part A regression tests —
comment stripped when preceded by whitespace, hash preserved when not.

---

### [I3] BLOCKING — the engine's own `profile.yml` writer emits values the fallback misreads, A2 does not fix them, and the Part C corpus names the wrong writer

The Response adds the init-lock template to the Part C sweep corpus:

> Verified 2026-08-03 under Python 3.13.13: a synthesized init-lock template
> parses **identically** under `yaml.safe_load` and `_minimal_yaml_parse`
> today.

There are two engine-side writers, and the sweep corpus gained the benign one.
The other is `_self_heal_profile_config` at `bootstrap/_scaffold/upgrade.py:2046`,
which emits every token through `_yaml_sq` (`bootstrap/_scaffold/upgrade.py:2039`)
— a YAML single-quoted scalar that **doubles any embedded single quote**. I ran
both writers and round-tripped their real output:

```
$ PYTHONDONTWRITEBYTECODE=1 ~/conda_envs/lhm/bin/python probe6.py
--- self-healed profile.yml ---
project_name: 'O''Brien Lab Model'
test_command: 'pytest -k ''not slow'''
preset: solo-greenfield
...
PyYAML  : {'project_name': "O'Brien Lab Model", 'test_command': "pytest -k 'not slow'", ...}
fallback: {'project_name': "O''Brien Lab Model", 'test_command': "pytest -k ''not slow", ...}
EQUAL   : False

--- init-lock template (no installed modules), rc=2 ---
'... (inferred from dev/modules/):\nmodules:\n'
PyYAML  : {..., 'modules': None}
fallback: {..., 'modules': []}
EQUAL   : False
```

Two distinct problems:

1. **The quote-doubling survives A2.** A2 replaces the unbalanced
   `.strip('"').strip("'")` at `bootstrap/_scaffold/config.py:133` with a
   balanced pair-strip. `probe5.py` shows the result: `'O''Brien'` goes from
   `O''Brien` to `O''Brien` (unchanged) and `'pytest -k ''a b'''` goes from
   `pytest -k ''a b` to `pytest -k ''a b''` — differently wrong, still not
   `pytest -k 'a b'`. The same gap exists for double-quoted escapes:
   `test_command: "pytest -k \"x\""` is `pytest -k "x"` under PyYAML and
   `pytest -k \"x\` under the fallback (probe1). Neither construct is in the A4
   refusal list, so after Part A they are *accepted and still divergent* —
   directly falsifying the live invariant "for every input
   `_minimal_yaml_parse` accepts, its output equals `yaml.safe_load`'s".

2. **The corrupted value propagates into the install contract.** These are not
   read-only misreadings; they feed the lockfile:

```
$ printf "project_name: 'O''Brien Lab Model'\ntest_command: 'pytest -k ''not slow'''\npreset: solo-greenfield\n" | ... python probe7.py
PyYAML    tokens -> {'project_name': "O'Brien Lab Model", 'test_command': "pytest -k 'not slow'"}
fallback  tokens -> {'project_name': "O''Brien Lab Model", 'test_command': "pytest -k ''not slow"}
```

   `_resolve_lock_profile_fields` is what `upgrade --init-lock` uses to build
   the lockfile `tokens` block. So an adopter whose name or test command
   contains an apostrophe — not exotic — gets a mangled test command recorded
   in the install contract *and* rendered into their `AGENTS.md`. This is the
   proposal's own "wrong write, fail closed" category, produced by a file the
   engine wrote itself.

Separately, the init-lock template's *own* output diverges in the
zero-installed-modules shape: `bootstrap/_scaffold/upgrade.py:1099` appends the
bare string `"modules:"` and then appends nothing when the module scan is
empty, giving `None` under PyYAML and `[]` under the fallback. The Response's
"parses identically" verification is true for the shape it synthesized and not
true of the writer.

**Ask.** Either extend A2/A3 to handle single-quote doubling and
double-quoted escape sequences, or add both to A4's refusal list (refusing a
file the engine writes is not acceptable, so the first option is likely
forced for `_yaml_sq` output specifically). Put **both** writers' output in the
Part C corpus, generated across shapes — including zero modules and a token
containing an apostrophe — rather than one synthesized example.

---

### [I4] The parity invariant is stated as live but is false for a further set of accepted inputs that A4 does not refuse

Beyond [I2] and [I3], these shapes are accepted by the fallback today and are
neither fixed by A1–A3 nor refused by A4 (probe1, probe2, probe8):

| input | PyYAML | fallback | class |
|---|---|---|---|
| `modules:` with nothing under it | `None` | `[]` | shape divergence, inert downstream |
| `project_name: foo` / newline / `  bar` | `'foo bar'` | `'foo'` | **silent truncation** |
| `project_name: "a\nb"` | real newline | literal `\n` | escape not processed |
| `modules: {}` | `{}` → `PresetError` | `[]` → silent opt-out | **fallback more permissive** |
| `project_name: My Project: Phase 2` | `ScannerError` | accepted | **fallback more permissive** |
| `modules:` / `  - a` / `- b` (mixed indent) | `ParserError` | accepted | **fallback more permissive** |
| `project_name: >` + folded block | `'folded text\n'` | `'>'` | block scalar mis-read |

The last three are the same "neither parser is a subset of the other" shape the
proposal already identified for tab indentation, so the *category* is
acknowledged — but A4 enumerates only two members of it (tab indent,
`key:value`), and there are at least five. The `modules: {}` row is worth
singling out: the code comment at `bootstrap/_scaffold/config.py:129` says the
`[]`/`{}` branch exists so `modules: []` "is honored as an explicit opt-out",
and for `{}` that documented behaviour is a fallback-only invention — under
PyYAML the same line is a hard `PresetError`.

This is the *Signals the change is wrong* row about "the parity table starts
accreting special cases" firing on day one. It is not an argument against the
change; it is an argument that the plan must **enumerate the closure before
implementation**, because the honest form of the invariant is "equal, or
refused with a demonstrated reason", and the refusal list is currently
demonstrably incomplete.

---

### [I5] New failure mode not named: A4 makes the installer's *acceptance set* environment-dependent, and the doc surface will present it as a universal contract

Part A is scoped to the fallback ("Rework `_minimal_yaml_parse` and its helper
`_list_item_text`"). The refusals therefore fire only when PyYAML is absent.
The documentation surface says:

> `bootstrap/BOOTSTRAP.md` — the "Schema rules" list in the preset section
> gains the fallback parser's refusal list, stated as a contract an adopter can
> rely on.

After the change, an adopter with PyYAML writes `modules: [a, b]` and installs
cleanly; their stdlib-only collaborator running the byte-identical command gets
a refusal. That is strictly better than today (loud rather than silent), and I
am not asking to reverse it — but it is a *new* environment-dependent outcome,
it is the mirror image of the reproducibility argument the proposal makes in
*Rationale*, and the proposal does not name it. A schema rule that binds on one
of two code paths is not "a contract an adopter can rely on".

**Ask.** Consider applying the A4 construct checks in `load_config` over the
raw text, independent of which parser ran, so there is one acceptance contract
on both paths and the shipped `BOOTSTRAP.md` rules are true as written. If that
is judged out of scope, say plainly in `BOOTSTRAP.md` that the refusal list is
the stdlib-parser contract and a PyYAML environment is more permissive.

---

### [I6] Forward compatibility: Cairn already has a written unknown-key doctrine for the sibling install-contract file, and the revised Part B contradicts it without reconciling

This is the lens I was asked to aim at, and it is not the G3 argument. I accept
the flip to refuse; the measured availability cost is real and I re-verified it
(see *Covered*). What is missing is what must ship *with* the flip.

`bootstrap/UPGRADE.md:208` states the opposite discipline for
`dev/.cairn/cairn-lock.yml`, the profile's sibling in the same directory and
the other half of the install contract:

> An additive **optional** top-level field does not bump `schema` — readers
> must use `.get()` with a default and tolerate unknown keys.

That rule is safe there because the lockfile carries a `schema` field, so a
reader can distinguish "a field I don't know" from "a file from the future".
`dev/.cairn/profile.yml` has **no version key**, and the proposed
`RECOGNIZED_PROFILE_KEYS` (five tokens + six axes + five structural keys) does
not add one. The consequence is structural: because the refusal is enforced by
the *reading* engine, every profile key Cairn ever adds after this ships is a
hard break for every engine released before it, with no carrier for the
"newer profile" signal and no way to say "this profile was written by a newer
Cairn". The Response is right that neither proposed opt-out works — but a
reserved version key is not an opt-out. It does not weaken typo detection
(`presets:` is not a version key) and it costs one entry in a set.

Two smaller items in the same area:

* The comment at `bootstrap/_scaffold/config.py:46-49` — inside the file the
  proposal is changing, and inside the module that holds the `_MODULE_MAPPINGS`
  trust anchor — states the now-reversed intent: unknown keys are ignored "so
  that future tokens do not break old configs". The revised Part B must update
  it, or the trust-anchor file will document the opposite of its behaviour.
* The proposal's *Touches* names "`bootstrap/BOOTSTRAP.md` (Appendix B schema
  rules)". I could not find an Appendix B statement of unknown-key handling;
  the token vocabulary lives in Appendix A (`bootstrap/BOOTSTRAP.md:652`), and
  `bootstrap/UPGRADE.md` is the file that actually states an unknown-key rule.
  The doc-surface list should be re-derived at plan open.

**Ask.** Add a reserved version/`schema` key to `RECOGNIZED_PROFILE_KEYS` now,
or state explicitly in `BOOTSTRAP.md` that the profile schema is closed for
every engine shipped to date and that adding a key is a breaking change.
Reconcile the two `dev/.cairn/` dispositions in one sentence somewhere a
future contributor will find it.

---

### [I7] The parity oracle collapses in exactly the environment that matters — the Part C sweep as specified cannot fail on a stdlib-only interpreter

This is the vacuous-guard shape the brief asks about, and it is already
shipping. `_yaml_load` (`bootstrap/_scaffold/config.py:36-43`) *is* the
fallback when PyYAML is absent. So any assertion of the form
`_yaml_load(x) == _minimal_yaml_parse(x)` compares the function under test to
itself:

```
$ PYTHONDONTWRITEBYTECODE=1 ~/conda_envs/lhm/bin/python probe4.py
config._yaml = None
input: 'forge: gitlab        # gitlab | github\n'
_yaml_load        -> {'forge': 'gitlab        # gitlab | github'}
_minimal_yaml_parse -> {'forge': 'gitlab        # gitlab | github'}
assert _yaml_load(x) == _minimal_yaml_parse(x)  PASSES: True
(true PyYAML answer for this input is {'forge': 'gitlab'})
```

Two existing tests are written in exactly that form —
`test_flat_schema_parses_identically` (`bootstrap/tests/test_presets.py:292`)
and the parity check at `bootstrap/tests/test_presets.py:423` — and the
proposal points the plan at that file precisely because it "already houses
`TestParserParity` ... this work should reuse rather than reinvent".

The proposal protects the *differential parity* test (Tests-required #1) with
"skipped-with-a-message if PyYAML is absent (so the environment never silently
voids it)" — good. It gives **no** such guard to Tests-required #4, the Part C
sweep, which is the drift gate the entire recurrence argument rests on. Worse,
#4 carries a reproduction check —

> This test must **fail** against today's HEAD; a plan that lands it green is a
> plan that did not reproduce the defect.

— which on a stdlib-only interpreter would pass green at HEAD, vacuously, and
be recorded as "the defect did not reproduce".

**Ask.** State in Part C that the sweep imports `yaml` directly (never
`_yaml_load`) and hard-skips with a message when it is absent; and name the
`_yaml_load`-as-oracle pattern as banned in the plan, since two live tests
model it.

---

### [I8] Part C's corpus definition is over-inclusive as written, with evidence

"Every profile-YAML block in a tracked Markdown file" is a shape heuristic. I
implemented it (fenced `yaml`/`yml` blocks in `git ls-files '*.md'` containing
a top-level `project_name`/`preset`/`modules`/`test_command`/`forge` key) and
got seven blocks, four divergent:

```
$ PYTHONDONTWRITEBYTECODE=1 ~/conda_envs/lhm/bin/python sweep.py
profile-shaped yaml blocks in tracked .md: 7
=== blocks whose two parsers DISAGREE (4) ===
  bootstrap/BOOTSTRAP.md (fence opens ~line 730)      [the two known divergent lines]
  bootstrap/fidelity-check.md (fence opens ~line 115)
     PyYAML  : {... 'profile': {'age': ..., 'size': ...}, 'modules': {'kernel': [...], ...}}
     fallback: {... 'profile': [], 'modules': ['AGENTS.md', ...]}
  dev/proposals/archive/2026-07-11-claude-solo-legacy-adopter-path.md (~line 49)
     PyYAML  : {'project_name': '<your-repo>', ...}   fallback: {}
  dev/proposals/archive/2026-07-11-claude-solo-legacy-adopter-path.md (~line 248)
```

The `bootstrap/fidelity-check.md` hit is the *fidelity manifest* example — a
different document type entirely, deeply nested, which the fallback is never
meant to parse. The two archived-proposal hits reduce to `{}` because the fence
is indented inside a list item. A sweep defined by shape will pick all of these
up on day one and force either a permanent allowlist or a skip — which is the
proposal's own "the documentation sweep test becomes a nuisance" signal firing
before the test is written.

The repository already has the right mechanism: `bootstrap/tests/test_presets.py`
anchors on an explicit marker string and asserts the marker appears exactly
once, so a second block cannot silently join the corpus.

**Ask.** Define the Part C corpus by explicit marker, not by shape, and carry
the "marker appears exactly once" assertion forward.

---

### [I9] Two existing tests contradict Part A and are not named in the plan

* `test_mixed_indent_list` (`bootstrap/tests/test_scaffold.py:204`) pins
  fallback-more-permissive-than-PyYAML behaviour, and its docstring endorses it:
  "not valid YAML strictly speaking, but the minimal parser is forgiving". I
  confirmed PyYAML raises `ParserError` on that input while the fallback
  accepts it (probe8). Part A's invariant requires refusing it, so this test
  must be inverted or deleted.
* `test_raises_on_invalid_yaml` (`bootstrap/tests/test_scaffold.py:246`) has
  **no assertion at all** — its body is `write_text` followed by three comment
  lines ending "We tolerate the minimal parser's inaccuracy here." A test named
  for a refusal that asserts nothing, expressing the exact posture this
  proposal reverses, sitting in the file the new refusal tests will land in.

The proposal says "Both new-test homes are existing files; no new test module"
and never mentions retiring or inverting an existing pin.

---

### [I10] Sibling collision on the shared AST attestation baseline

`2026-08-03-claude-fork-advisory-semantics` is also at status `revised`, also
touches `bootstrap/_scaffold/upgrade.py`, and therefore also mandates a
re-anchor of the same committed baseline
`bootstrap/tests/fixtures/scaffold_ast_baseline.json`. This proposal's revision
adds `upgrade.py` to its own *Touches*. That sibling has already priced the
hazard in its own *Coordination* section — including the finding that an
engine-package edit landing without a re-anchor leaves the canonical suite red
for the whole interval. This proposal's record is silent on it, and its own
stop-the-line signal ("an unexplained engine-baseline delta is a stop-the-line
event, not a re-pin") will fire on the *sibling's* legitimate symbol motion if
the two are executed without an ordering.

**Ask.** One sentence of coordination naming the sibling and the ordering, so
the second executor is not surprised.

---

### Covered

Every command below was run this session, `PYTHONDONTWRITEBYTECODE=1`,
`~/conda_envs/lhm/bin/python` (3.13.13), scratch files under the session
scratchpad, nothing written into the repository.

* **Boundary sweep (empty, None, one, N, non-ASCII, CRLF, symlink-free,
  indented).** `probe1.py`, `probe2.py`, `probe3.py`, `probe9.py` — 25 inputs
  through `yaml.safe_load` vs `_minimal_yaml_parse`, plus `load_config` under a
  real `sys.meta_path` PyYAML blocker with `config._yaml` printed to prove the
  branch. Yielded [I1], [I4].
* **Does the fix introduce new divergence?** `probe5.py` — A1+A2+A3
  implemented as literally specified and diffed against current behaviour over
  seven inputs. Yielded [I2] and the A2-insufficiency half of [I3].
* **Round-trip of the engine's own writers.** `probe6.py` calls the real
  `_self_heal_profile_config` and `_write_init_lock_profile_template` into a
  temp tree and parses their output both ways; `probe7.py` feeds the mis-parsed
  result to the real `_resolve_lock_profile_fields`. Yielded [I3].
* **Test-vacuity / oracle-collapse check.** `probe4.py` under a blocked-PyYAML
  interpreter, plus reading `bootstrap/tests/test_presets.py:281-300` and
  `bootstrap/tests/test_scaffold.py:165-255`. Yielded [I7], [I9].
* **Part C corpus feasibility.** `sweep.py` over `git ls-files '*.md'`.
  Yielded [I8].
* **Forward-compatibility / doctrine consistency.** `grep -rn 'silently
  ignored|are ignored|unknown keys|ignores unknown'` over `bootstrap/*.md`,
  `docs/*.md`, `templates/core/*.md`; read `bootstrap/UPGRADE.md:199-215`.
  Yielded [I6].
* **Confirmations of author claims that HELD.** The recognized-key set is
  complete against the engine's real reads —
  `grep -rn 'cfg\.get(|cfg\[|config\.get(|profile\.get('` over
  `bootstrap/_scaffold/*.py` returns exactly `preset`, `modules`,
  `modules_add`, `modules_remove`, `forge`, `project_name`, the six `_AXES`
  keys and the `KNOWN_TOKENS` filter, so the proposed five structural keys are
  right. `load_config` has exactly four call sites, all profile-reading
  (`bootstrap/_scaffold/cli.py:218`, `bootstrap/_scaffold/cli.py:296`,
  `bootstrap/_scaffold/upgrade.py:237`, `bootstrap/_scaffold/upgrade.py:1136`),
  so a key whitelist there cannot leak onto other YAML files. All three shipped
  profiles under `bootstrap/profiles/` carry only `project_name`,
  `test_command`, `preset` and no divergent line — the Response's measured
  availability cost reproduces. The "exactly 3 divergent-shape lines in
  adopter-facing files" count reproduces (two in the `bootstrap/BOOTSTRAP.md`
  block at `bootstrap/BOOTSTRAP.md:734` and `bootstrap/BOOTSTRAP.md:739`, one at
  `bootstrap/_scaffold/cli.py:28`), and both cited line numbers are correct.
  `python scripts/claim_check.py` over the proposal: OK, no flags.

### Not covered / low confidence

* **This is a same-agent-type review and carries no cross-type independence.**
  The author is Claude; I am Claude in a fresh session. Whatever blind spot
  produced the overstatements in [I1] and [I3] is a blind spot I share by
  construction. The External tier for this proposal was Gemini Flash, and this
  review does not substitute for it — treat these findings as a second read
  from inside the same head, not as independent confirmation.
* **I did not re-run the suite.** The `1556 passed` baseline is unverified by
  me; the proposal already says to re-measure at plan open.
* **I did not run a full install.** The five-file `--help` delta, the 11
  differing-content files for the `project_name` case, and the four typo rows
  of Evidence (i) were reproduced by the External pass and re-reproduced by the
  Response; I relied on that and spent the budget on unexercised surface
  instead.
* **COULD NOT REPRODUCE: a CRLF problem.** The proposal names CRLF as an
  explicit gap. I ran `project_name: X\r\nmodules:\r\n  - claim-check\r\n`
  through both parsers (probe1) and got identical results, because
  `line.strip()` removes the `\r`. I tested three shapes only; I did not test
  CRLF combined with quoting or comments, so the gap is narrowed, not closed.
* **Not examined:** the AST attestation delta itself (no code exists yet); the
  Bandit and `vermin` gates; concurrent-writer behaviour on
  `dev/.cairn/profile.yml` (no locking is involved on the read path, but I did
  not test a writer racing `load_config`); non-UTF-8 profiles (the proposal
  scopes them out and `read_text(encoding="utf-8")` does raise); symlinked
  profile paths.
* **[I5]'s recommendation is a design opinion, not a defect.** Applying A4 on
  both paths is more work and may collide with *FIX DEFECTS, BUILD NOTHING
  NEW*; I flag the unnamed failure mode as a finding and the remedy as a
  suggestion.

### Second-round recommendation

**A second round is recommended — a Revised-proposal round, not a re-review of
the direction.** The proposal's direction survives this pass intact: Part A,
Part C, and the revised fail-closed Part B are all the right calls, and I found
nothing that should reverse them. But three of its stated protections do not
hold on the stdlib-only path ([I1], [I2], [I3]), and a plan opened against the
current text would ship a change that closes the documented fail-opens while
leaving the largest one — an empty or indented profile accepted as `{}` — wide
open, and would regress `project_name: issue#42-tracker` in the process.

The remedy is cheap and entirely within the existing fence: an appended
*Revised proposal* section that (a) adds the empty-parse refusal to A4 and
corrects the two false edge-case rows, (b) specifies the whitespace rule in A3
and adds the missing parity row, (c) decides the quote-doubling/escape question
and fixes the Part C corpus to both writers, (d) states the sweep's PyYAML
guard, and (e) adds one sentence each on the version carrier ([I6]) and the
sibling ordering ([I10]). [I4], [I5], [I8] and [I9] are plan-scoping items that
can be recorded as constraints rather than resolved in the proposal.

I would not send this back to External review. Everything above is
specification detail below the level the External tier is for, and the External
tier already did its job — including on the question ([I3]'s writer
round-trip) that its own A4-sharpening exchange opened and did not finish.

## Response -- Claude (author, to Internal review) -- 2026-08-03

**Model**: Claude Opus 5. Proposal-Response grammar (no implementing commits
exist). Every finding below was reproduced this session before it was
dispositioned — I ran the review's probes myself rather than reading its
transcript, under `~/conda_envs/lhm/bin/python` (Python 3.13.13, PyYAML 6.0.3)
at working-tree HEAD `54478e2`, with `PYTHONDONTWRITEBYTECODE=1`. No file was
written into the repository; every scratch artifact lives outside it. The
no-PyYAML condition was produced by a `sys.meta_path` finder raising
`ImportError` on `yaml`, with `config._yaml` printed to prove the fallback
branch was taken before any `load_config` call.

*Terms, first use.* A **recognizer** is a parser that accepts only inputs
matching a stated grammar and refuses everything else, as opposed to a
**best-effort reader**, which returns something for any input. An **oracle** is
the value a test compares against to decide pass/fail. A **canary** is a known-
bad input a gate must be shown to catch, so that a gate which has silently
stopped working fails instead of passing.

### [I1] accept -- without qualification; this is the gate-honesty failure shape, and it is mine

The finding is correct, and it is correct in the way that matters most in this
repository. I wrote, twice, that A4 "extends the same fail-closed posture" of an
existing guard. That guard is `if not isinstance(cfg, dict)` at
`bootstrap/_scaffold/config.py:151`. `_minimal_yaml_parse` initialises `result`
as a dict at `bootstrap/_scaffold/config.py:95` and returns it unconditionally
at `bootstrap/_scaffold/config.py:140`. On the stdlib-only path the guard cannot
fire. I grounded a security argument in a protection that does not exist on the
path I myself called normal — the same shape this repository has ledgered
roughly a dozen times as *a document claiming a mechanical gate that nothing
fires*. Naming it plainly: this proposal was, on that sentence, an instance of
the class it exists to close.

Reproduced, both paths, five inputs:

```
$ PYTHONDONTWRITEBYTECODE=1 ~/conda_envs/lhm/bin/python p_i1.py         # PyYAML present
config._yaml = <module 'yaml' from '.../site-packages/yaml/__init__.py'>
  zero-byte            -> REFUSED   ValueError: expected a YAML mapping at the top level, got NoneType
  whitespace-only      -> REFUSED   ValueError: expected a YAML mapping at the top level, got NoneType
  comment-only         -> REFUSED   ValueError: expected a YAML mapping at the top level, got NoneType
  uniformly-indented   -> ACCEPTED {'project_name': 'Photosynthesis-Model', 'preset': 'high-rigor-legacy'}
  modules-{}           -> ACCEPTED {'project_name': 'X', 'modules': {}}

$ ... p_i1.py block                                                     # PyYAML blocked
config._yaml = None
  zero-byte            -> ACCEPTED {}
  whitespace-only      -> ACCEPTED {}
  comment-only         -> ACCEPTED {}
  uniformly-indented   -> ACCEPTED {}
  modules-{}           -> ACCEPTED {'project_name': 'X', 'modules': []}
```

The two *Edge-case inventory* rows the review calls false are false. I withdraw
both; they are corrected in *Author-accounting — corrections to the record*
below.

The uniformly-indented case is worse downstream than the review states. I ran
the real `--summary` on it both ways:

```
PyYAML present:  exit 0   Preset: high-rigor-legacy              14 module lines
PyYAML blocked:  exit 0   Preset: (none -- literal module list)   6 module lines
                          header reads: ## Dimension profile -- <project_name>
```

A copy-paste that picked up leading whitespace — the ordinary result of copying
out of a rendered documentation page — silently installs a six-module tree
instead of a fourteen-module one, at exit 0, with the project name left as the
raw `<project_name>` placeholder. That is a larger fail-open than any row in the
proposal's own divergence table, and the change as specified left it open.

**Replacement grounding, and it is a better one.** A4 does not need an invented
posture. `bootstrap/BOOTSTRAP.md:748` already states, as a shipped schema rule,
that the profile format is "flat, stdlib-parseable — no nested mappings". That
rule is documented and enforced by nothing on either path — a nested mapping is
accepted by PyYAML and by the fallback alike. A4 is therefore *enforcement of an
existing written contract that no code fires*, which is defect repair against
the same ledger, not a new posture. That is what I should have written.

### [I2] accept -- with a third regression row the review did not name

Reproduced by implementing A1+A2+A3 exactly as the proposal words them (a
quote-aware comment stripper plus a balanced pair-unquote) and diffing against
current behaviour:

```
input                                    | PyYAML              | CURRENT             | PROPOSED
'project_name: a#b'                      | 'a#b'               | 'a#b'               | 'a'        <<< REGRESSION
'project_name: issue#42-tracker'         | 'issue#42-tracker'  | 'issue#42-tracker'  | 'issue'    <<< REGRESSION
'test_command: pytest -k not-slow#fast'  | 'pytest -k not-slow#fast' | 'pytest -k not-slow#fast' | 'pytest -k not-slow'  <<< REGRESSION
'modules:' / '  - a#b'                   | ['a#b']             | ['a']               | ['a']      (still divergent)
'forge: gitlab        # gitlab | github' | 'gitlab'            | 'gitlab        # ...' | 'gitlab' (fixed)
```

The `test_command` row is mine, not the review's, and it is the one that would
have hurt: a `pytest -k` selector containing a hash is silently truncated into a
*different, still-valid* test command, recorded into the adopter's lockfile and
rendered into their `AGENTS.md`. Three of five rows regress. YAML starts a
comment at `#` only at line start or after whitespace; the helper the proposal
points at as its model (`bootstrap/_scaffold/config.py:101`) does
`.split("#")[0]`, so A1's "make the scalar branch do what the list branch does"
would have propagated a bug into the one branch that is correct today. The
whitespace rule is now stated explicitly in the grammar below, and both
directions are pinned as required tests.

### [I3] accept -- and the decision the review left open is decided here

Reproduced by calling the real writer rather than a synthesized approximation:

```
$ ... p_i3.py
--- _self_heal_profile_config output ---
project_name: 'O''Brien Lab Model'
test_command: 'pytest -k ''not slow'''
PyYAML  : {'project_name': "O'Brien Lab Model",  'test_command': "pytest -k 'not slow'"}
fallback: {'project_name': "O''Brien Lab Model", 'test_command': "pytest -k ''not slow"}
EQUAL   : False

A2 (balanced pair-strip) applied to the same values:
  "'O''Brien Lab Model'"      -> "O''Brien Lab Model"      (PyYAML: "O'Brien Lab Model")
  "'pytest -k ''not slow'''"  -> "pytest -k ''not slow''"  (PyYAML: "pytest -k 'not slow'")

and it reaches the install contract:
fallback cfg -> _resolve_lock_profile_fields tokens: {'project_name': "O''Brien Lab Model", ...}
PyYAML   cfg -> _resolve_lock_profile_fields tokens: {'project_name': "O'Brien Lab Model",  ...}

--- init-lock template, zero installed modules, rc = 2 ---
PyYAML modules: None      fallback modules: []      EQUAL: False
```

Both halves hold. A2 does not fix quote doubling — it makes one case
*differently* wrong. And the Response's "parses identically" verification was
true of the shape I synthesized and not of the writer, which is the same
verify-the-artifact-with-material-the-artifact-supplied error in miniature: I
checked my own reconstruction instead of calling the function.

**The decision.** The review offered two options and declined to pick. I pick
the first, scoped: implement YAML's single-quoted scalar rule (`''` → `'`,
which is that form's *entire* escape vocabulary — two lines, no drift), accept a
double-quoted scalar only when it contains no backslash, and refuse a
backslash-bearing double-quoted value with a message pointing at the
single-quoted form. Refusing the engine's own output is not acceptable and does
not arise: `_yaml_sq` (`bootstrap/_scaffold/upgrade.py:2039`) emits
single-quoted scalars, and the init-lock template's double-quoted placeholders
carry no backslash. Verified below — both writers' real output is accepted, and
equals PyYAML, under the grammar.

The init-lock zero-modules divergence is closed by making a bare `key:` yield
`None` rather than `[]`, which is simply the faithful reading. I confirmed the
review's "inert downstream" label independently: `modules:` and `modules: []`
both exit 1 through the real CLI, so nothing behavioural rides on it today.
I am closing it anyway, because "divergent but inert" is the category this
record has twice been wrong about.

### [I4] accept with modification -- the enumeration is replaced, not extended

The seven rows reproduce. I decline the implied remedy of enumerating the
closure, because enumerating is what has failed each round: the External pass
found twelve divergence classes, this Internal pass found seven more plus a
thirteenth in [I2], and there is no reason to believe a third pass finds zero.
An enumerated refusal list is a *diagnosis*, and a diagnosis has no stopping
point. The *Revised proposal* below replaces A4's list with a closed line
grammar, so the refusal set becomes the complement of what is accepted — derived
rather than catalogued. Every one of the seven rows falls out of it without
being named.

### [I5] accept -- one contract on both paths, and the cost is measured at zero

The finding is right that a schema rule binding on one of two code paths is not
a contract, and right that the proposal did not name the new failure mode. The
review flagged its own remedy as "a design opinion, not a defect"; I adopt the
remedy anyway, because the alternative is shipping `BOOTSTRAP.md` text that is
true only in a stdlib-only environment, which is a documented-gate-that-does-not-
fire — the [I1] shape again, deliberately this time.

Measured before adopting: across every tracked `.md` and `.yml` outside
`dev/proposals/` and `dev/plans/`, the number of profile-shaped lines that the
A4 checks would refuse is **zero** (3 apparent hits, all `key: []` empty flow
collections, which A4 keeps accepted, all in `bootstrap/fidelity-check.md`,
which is the fidelity manifest and not a profile — the over-inclusion [I8]
predicts). All three shipped profiles under `bootstrap/profiles/` and both
engine writers' output are accepted unchanged. Snapshot as_of 2026-08-03.

### [I6] accept with modification -- the version carrier ships; one sub-item is corrected

The reconciliation ask is right and the remedy is cheap, so `schema` joins
`RECOGNIZED_PROFILE_KEYS` as a reserved read-and-ignore key. Its value is
precisely what lets a refusal say *"this profile declares schema 2; this engine
understands 1 — upgrade Cairn"* instead of *"unknown key"*, which is the
difference between a diagnosable stop and a dead end. It does not weaken typo
detection: `presets:` is not `schema`.

One precision the review's framing needs: adding it now rescues no engine
already released, because those engines do not know the key either. What makes
it free is that Cairn has zero external adopters as_of 2026-08-03, so "engines
already deployed" is an empty set. That is the honest reason to do it now and
the reason it stops being free after the first adopter.

**One sub-item corrected against the reviewer.** The review says it "could not
find an Appendix B statement of unknown-key handling" and suggests the *Touches*
line is wrong. `bootstrap/BOOTSTRAP.md:692` is "Appendix B — profile config YAML
format" and `bootstrap/BOOTSTRAP.md:748` is its **Schema rules** list, so the
*Touches* entry is accurate. What is absent from Appendix B is any unknown-key
rule at all — which is what Part B adds, not a mislocation. The comment at
`bootstrap/_scaffold/config.py:46` stating the now-reversed intent must be
rewritten, exactly as the review says.

### [I7] accept -- and the fix is a canary, not only a skip

The oracle collapse reproduces, and it is the same shape as this repository's
ledgered anti-drift assertion that could not fail — a gate whose expected value
is produced by the thing under test:

```
$ ... p_i7.py                                    # PyYAML blocked
config._yaml = None
_yaml_load(x)          = {'forge': 'gitlab        # gitlab | github'}
_minimal_yaml_parse(x) = {'forge': 'gitlab        # gitlab | github'}
assert _yaml_load(x) == _minimal_yaml_parse(x) PASSES: True
(the true PyYAML answer is {'forge': 'gitlab'})
canary detected as divergent by this oracle pair: False
```

That last line is the point. A hard-skip guard is necessary but it is a promise
that the *next* test author must remember to keep. A canary is structural: the
sweep asserts that a known-divergent input **is** reported divergent, so an
oracle that has collapsed fails the gate instead of passing it vacuously. The
guard and the canary both ship; the canary is the one that survives a future
refactor. Naming the two live instances of the banned pattern:
`test_flat_schema_parses_identically` at `bootstrap/tests/test_presets.py:292`
and the parity check at `bootstrap/tests/test_presets.py:423` — the latter named
`test_literal_recipe_yaml_also_parses_via_pyyaml`, a test whose name asserts the
very thing its body cannot guarantee.

### [I8] accept

Corpus by explicit marker, carrying forward the existing
"marker appears exactly once" assertion. The shape heuristic's four false
positives reproduce as described.

### [I9] accept

`test_mixed_indent_list` (`bootstrap/tests/test_scaffold.py:204`) is inverted —
mixed indentation is refused, and its docstring's "the minimal parser is
forgiving" is the posture this proposal reverses. `test_raises_on_invalid_yaml`
(`bootstrap/tests/test_scaffold.py:246`) has no assertion at all and becomes a
real refusal test. Both are named in *Tests required* below. I was wrong to
write "no new test module" as though nothing existing needed retiring.

### [I10] accept

Coordination sentence added below. Confirmed independently across the twelve
`2026-08-03-claude-*` proposals, as_of 2026-08-03: two others name a
`bootstrap/_scaffold/` file in *Touches* — `2026-08-03-claude-identity-not-name`,
which is `superseded` and therefore inert, and
`2026-08-03-claude-fork-advisory-semantics`, status `revised`, which names
`install.py`, `lockfile.py` and `upgrade.py`. Only the second is live, and its
`upgrade.py` overlap with this proposal's revised *Touches* is real.

**Status.** Stays `revised`. No finding reversed the direction; three of them
showed the specification could not be executed as written.

---

## Revised proposal -- A4 becomes a closed line grammar -- 2026-08-03

Append-only: nothing above is edited. Where this section conflicts with the
original *Proposal* or the first *Revised proposal*, **this section governs**.

### Why the shape changes, not just the content

Each review round on this proposal has found one more divergence class and the
horizon has receded by exactly one step: twelve at External, seven more plus a
thirteenth at Internal. That is not reviewer diligence compounding — it is what a
specification written as *a list of known-bad inputs* does. A list cannot tell
you when you are finished, because "finished" is a property of the inputs you
have not thought of.

So A4's enumerated refusal list is withdrawn and replaced by a **closed line
grammar**. `_minimal_yaml_parse` becomes a *recognizer*: every non-blank line
matches one of a small number of accepted forms, or `load_config` refuses with
`<path>:<line>: <reason>`. The refusal set is then the complement of the
grammar — derived, not catalogued — and a future reviewer cannot find a
"silently dropped line", because that outcome no longer exists in the code.

This is not additional construction. Part A already mandated rewriting
`_minimal_yaml_parse`; the grammar is a smaller rewrite than a growing catalogue
of pattern checks, and it deletes the "divergent but inert, out of scope" third
bucket rather than maintaining it.

### The invariant, restated so it is two-valued

The old invariant — *"for every input `_minimal_yaml_parse` accepts, its output
equals `yaml.safe_load`'s"* — was false at HEAD ([I3]'s quote doubling, [I4]'s
seven rows) and is withdrawn. It is replaced by:

> For every profile text, `load_config` either **(a)** returns a value equal to
> `yaml.safe_load`'s, or **(b)** raises with a `<path>:<line>:` message naming
> the construct and the rewrite. **There is no third outcome — in particular, no
> content line is ever silently dropped.**

The two halves have different evidentiary status, and saying so is the point:

* **(b)-totality is structural.** The parse loop refuses any line matching no
  form, so "accepted but not represented" is unreachable by construction. Every
  finding that recurred across rounds — [I1]'s empty and indented profiles,
  [I4]'s truncation and folded-block rows — lived in that bucket. Closing it is
  what stops the horizon receding.
* **(a) is verified over a finite corpus, not proved.** A future reviewer may
  still find an accepted input whose value diverges. That risk is now bounded by
  a small closed grammar instead of by an open-ended parser, but it is not zero,
  and this proposal does not claim it is.

### The grammar

Every line is exactly one of these, or the profile is refused. `<path>:<line>:`
prefix and the A5 actionable-rewrite requirement apply to every refusal.

| form | accepted | yields |
|---|---|---|
| **L1** | blank line, or a line whose first non-space character is `#` | skipped |
| **L2** | `---` as the first content line, once | skipped |
| **L3** | `key: <plain scalar>` | string, or a canonical integer |
| **L4** | `key: '<single-quoted>'` | body with `''` → `'` |
| **L5** | `key: "<double-quoted>"`, no backslash, no interior `"` | body verbatim |
| **L6** | `key: []` | empty list |
| **L7** | `key:` with nothing after it | `None`, and opens a list block |
| **L8** | `- <scalar>` at a consistent indent under an open L7 key | appends to that list |

A **plain scalar** (L3, and the L8 item form) is accepted only when, after
removing a trailing comment introduced by `#` **at line start or preceded by a
space or tab** — the rule [I2] showed A1 was missing — the remaining value:

* does not begin with a YAML indicator character (`&` `*` `!` `|` `>` `[` `{`
  `@` `` ` `` `%`) — the indicator-position scoping the first revision
  established, now applied by position rather than by presence;
* is not a bare YAML 1.1 boolean or null (`yes` `no` `true` `false` `on` `off`
  `null` `~`, case-insensitive);
* contains no `: ` and does not end in `:`;
* contains no `"` or `'`;
* and, if it begins with a digit, `-`, `+`, or `.`, matches the **canonical
  integer** form `-?(0|[1-9][0-9]*)` — in which case it yields an `int` — and is
  otherwise refused with *"may be read as a number, date or time; write it
  quoted"*.

That last clause is the one that earns its keep. Verified against PyYAML on
2026-08-03: `010` is **8** (YAML 1.1 octal), `1:30` is **90** (sexagesimal),
`2024-01-01` is a `datetime.date`, and `.5` is a float. A best-effort fallback
returns the literal string for all four. The canonical-integer carve is what
lets `schema: 1` work ([I6]) while leaving every other numeric-looking shape
fail-closed. It also retires the "bare integers diverge but the divergence is
inert" carve-out in the original *Proposal*; there is no inert bucket now.

Anything else — a flow collection with content, a nested mapping, tab
indentation, `key:value` with no space, a second document, an unexpected
indent, a duplicate key, an unterminated or backslash-bearing quoted value, a
list item with no preceding key, inconsistent list indentation — is refused. So
is a document that produced **no content lines at all** (zero-byte,
whitespace-only, comment-only), which is [I1]'s ask and matches PyYAML's `None`.
A literal `{}` document is the one carve in the other direction: PyYAML accepts
it as an empty mapping, so the grammar does too, by explicit rule rather than by
falling through.

### One acceptance contract, both parsers -- [I5]

The grammar's checks are **textual**, so they run in `load_config` over the raw
text *before* dispatch to either parser. One acceptance set on both paths;
`BOOTSTRAP.md`'s schema rules become true as written rather than true in one
environment. The measured cost is zero refusals across everything Cairn ships,
writes, or documents (above). This makes the PyYAML path stricter than it is
today — see *Maintainer decision points*.

### The canary rule -- [I7]

Every differential-parity gate this change adds must satisfy three properties,
and the third is new doctrine for this repository's test surface:

1. It imports `yaml` **directly**. `_yaml_load` is banned as an oracle — it *is*
   the function under test when PyYAML is absent.
2. It hard-skips with a message when `yaml` is unimportable, so an environment
   cannot silently void it.
3. **It carries a canary**: a known-divergent input the gate must report as
   divergent. If the oracle has collapsed, the canary is reported equal and the
   gate **fails**. A parity gate that cannot detect its own canary is not a gate.

### Corpus and coordination

* **Part C corpus, by explicit marker** ([I8]), carrying the existing
  "marker appears exactly once" assertion, and containing: the marked blocks in
  tracked Markdown, the `bootstrap/_scaffold/cli.py` module docstring, and the
  real output of **both** engine writers —
  `_write_init_lock_profile_template` and `_self_heal_profile_config`
  (`bootstrap/_scaffold/upgrade.py:2046`) — generated across shapes including
  zero installed modules and a token containing an apostrophe ([I3]).
* **The `upgrade.py:239` precondition stands unchanged** from the first
  revision: narrowing that bare `except Exception` so it reports what it
  swallowed lands first or in the same change, never after.
* **Sibling coordination** ([I10]): `2026-08-03-claude-fork-advisory-semantics`
  also touches `bootstrap/_scaffold/upgrade.py` and also mandates a re-anchor of
  the shared baseline `bootstrap/tests/fixtures/scaffold_ast_baseline.json`.
  The two must not execute concurrently. Recommended ordering below; whichever
  lands second re-anchors against the first's result, and this proposal's
  stop-the-line signal for "unexplained engine-baseline delta" is read *after*
  accounting for the sibling's symbol motion, not before.

### Tests required -- replacing the original list where they conflict

1. **Grammar soundness, generative** — inputs generated from the grammar's
   accepted forms, each asserted equal to `yaml.safe_load`. Replaces the
   table-driven parity test; the table becomes seed cases, not the whole test.
2. **Grammar totality** — for a corpus of malformed inputs, `load_config` raises
   with a line number; no input returns a partial dict. Includes every row from
   [I1], [I2], [I3] and [I4].
3. **Both directions of the comment rule** ([I2]) — comment stripped when
   preceded by whitespace; `a#b`, `issue#42-tracker`, and
   `pytest -k not-slow#fast` preserved intact.
4. **Both engine writers round-trip** ([I3]) — real writer output, across
   shapes, parsed both ways, asserted equal.
5. **Part C marker sweep** with the PyYAML guard **and the canary** ([I7]),
   asserted to fail against today's HEAD *on an interpreter where the canary is
   detected* — the reproduction check the original stated without the guard that
   makes it meaningful.
6. **`RECOGNIZED_PROFILE_KEYS` derivation**, now including reserved `schema`.
7. **Unrecognized-key refusal** before any write, with the recognized set
   printed.
8. **Inverted / completed existing tests** ([I9]) —
   `bootstrap/tests/test_scaffold.py:204` inverted to assert refusal;
   `bootstrap/tests/test_scaffold.py:246` given the assertion it never had.
9. **End-to-end under a genuinely forced no-PyYAML interpreter**, reusing the
   existing subprocess pattern at `bootstrap/tests/test_presets.py:425`.
10. **AST attestation re-anchor**, mandatory, per `bootstrap/REANCHOR_RUNBOOK.md`,
    sequenced against the sibling.

### Author-accounting -- corrections to the record

* **Withdrawn as false**: *"Empty file (zero bytes): `load_config` already
  raises"* and *"Comment-only file: verified equivalent"*. Both hold only when
  PyYAML is present.
* **Withdrawn as false**: the live invariant *"for every input
  `_minimal_yaml_parse` accepts, its output equals `yaml.safe_load`'s"* — it was
  already false at HEAD. Replaced by the two-valued form above.
* **Withdrawn as unsound grounding**: both sentences claiming A4 "extends" an
  existing fail-closed posture. The posture is unreachable on the fallback path.
  The real grounding is `bootstrap/BOOTSTRAP.md:748`.
* **Withdrawn**: the *"bare integers diverge but the divergence is inert"*
  scope-out. There is no inert bucket under a two-valued invariant.
* **Corrected**: the first revision's claim that a synthesized init-lock
  template "parses identically". True of the synthesized shape, false of the
  writer at zero installed modules.
* **Retained and re-verified**: the recognized-key set is complete against the
  engine's real reads; all three shipped profiles carry only recognized keys and
  no divergent line; `bootstrap/BOOTSTRAP.md:734`, `bootstrap/BOOTSTRAP.md:739`
  and `bootstrap/_scaffold/cli.py:28` are the three divergent adopter-facing
  lines, as_of 2026-08-03.
* **Not re-measured this session**: the `1556 passed` suite baseline. Re-measure
  at plan open under Python 3.13.13, per the original.

### Verification of this revision

The grammar was implemented and run before being specified, on 2026-08-03 under
Python 3.13.13 — not a design sketch:

* **Availability** — all three shipped profiles under `bootstrap/profiles/`,
  the real output of `_self_heal_profile_config` (with an apostrophe-bearing
  project name and test command), the real output of
  `_write_init_lock_profile_template` at one and at zero installed modules, the
  `bootstrap/BOOTSTRAP.md` preset block and the `cli.py --help` block: **8 of 8
  accepted, and all 8 equal to `yaml.safe_load`. Zero refusals.**
* **Soundness and totality** — 35 inputs covering every divergence row from the
  External pass, the Response, and findings [I1] through [I4]: **0 soundness
  violations (accepted but unequal to PyYAML) and 0 specification misses
  (accepted-but-should-refuse, or refused-but-should-accept).**

**What that does not establish.** 35 inputs is a corpus, not a proof. It
establishes that the grammar is implementable, that it accepts everything real
today, and that it closes every divergence found across three review passes. It
does not establish that no accepted input diverges — see the invariant's
part (a) above. The generative test in *Tests required* is what would raise that
confidence, and it too samples rather than proves.

### Signals the change is wrong -- additions

* **A real adopter profile is refused.** The measured cost is zero *today*, on a
  corpus Cairn controls. A refusal on a profile a person actually wrote means
  the grammar is too tight; recovery is to widen the accepted form, never to
  restore best-effort reading.
* **The grammar accretes forms.** If closing a divergence needs a ninth, tenth,
  eleventh accepted line form, the recognizer is drifting into the PyYAML
  reimplementation the original *Signals* section warns about. Recovery: stop,
  and revisit Alternative 4.
* **A canary is ever deleted or skipped to make a suite green.** That is the
  vacuous-gate failure returning by the front door.

### What this revision does not establish

* It does not close the **correctly-spelled key, unrecognized value** class — a
  profile listing `- not-a-real-module` is still accepted at exit 0. Unchanged
  from the first revision; still outside this fence.
* It does not make `_minimal_yaml_parse` a YAML parser. It makes it a recognizer
  for the profile subset.
* CRLF remains partially tested: the review found `line.strip()` removes `\r` on
  three shapes, so the gap is narrowed, not closed. CRLF combined with quoting
  and comments is a named plan obligation.
* The forward-compatibility cost of refusing unknown keys remains **argued, not
  measured** — zero external adopters means no field data in either direction.
* This response was written by the proposal's author, and the review it answers
  was same-agent-type. Neither is cross-type independence. The External tier for
  this proposal was Gemini Flash, and it did not see the grammar.

### Maintainer decision points

**A note on this section.** An earlier draft supplied pre-written sentences for
the Maintainer to say back. They have been removed: the scribing guard-rail
requires an authorization be quoted **verbatim**, and a sentence an agent wrote
for the Maintainer to repeat is the agent's decision wearing the Maintainer's
name. The options below describe what each choice means; the wording is theirs.


Four calls belong to the Maintainer. Each carries a recommendation and the exact
words that would authorize it; none is left open.

**1. One acceptance contract on both parser paths ([I5]).** This makes the
PyYAML path *stricter than it is today* — an adopter with PyYAML who writes
`modules: [a, b]` would be refused where they are accepted now. Measured cost on
everything Cairn ships, writes or documents: zero. **Recommendation: adopt.** The
alternative is shipping a documented schema rule that binds on one of two paths,
which is the [I1] failure committed knowingly.

  Adopt the single acceptance contract — run the grammar checks on both parser
  paths.

> *(to decline)* *"Keep the refusal list on the stdlib path only, and say plainly
  in BOOTSTRAP.md that a PyYAML environment is more permissive.

**2. The reserved `schema` key ([I6]).** One entry in a set; free only while
external adopters number zero. **Recommendation: adopt now.**

  Reserve `schema` in the recognized profile keys now.

**3. Ordering against the sibling ([I10]).** Both proposals re-anchor the same
AST baseline. **Recommendation: `fork-advisory-semantics` first** — it is
already `revised`, has already priced the re-anchor in its own Coordination
section, and this proposal is the one still absorbing specification findings.

  Land fork-advisory-semantics first; profile-parse-fail-open re-anchors
  against its result.

**4. Whether one more Internal round runs before plan-open.** The Internal review
recommended a Revised-proposal round and explicitly advised against returning to
External. This revision goes further than that review asked — it replaces A4's
structure rather than extending it. **Recommendation: one focused Internal
re-review, scoped to the grammar's totality claim and the canary rule only** —
not a re-read of the direction, which has now survived two passes intact. The
reason is [I1]: the last time this proposal claimed a structural property, the
property did not hold on the path that matters, and a structural claim is
exactly what part (b) of the new invariant is.

  Run one focused Internal re-review on the grammar's totality claim, then open
  the plan.

  *(to skip it)* *"The grammar verification is sufficient — open the plan.

## Decision -- Anthony Kendall (Maintainer) -- 2026-08-03

**Accepted, as revised.** Scribed by Claude (Strategy) at the Maintainer's
explicit instruction.

**Maintainer's authorization (verbatim):**

> I approve each of the seven proposals that you have listed as ready to accept,
> as revised.

The seven were presented as a ledger with a per-proposal recommendation; this is
one of them. The authorization is quoted rather than paraphrased, per the
scribing guard-rail: a paraphrase admits semantic drift, condition-softening, or
a hallucinated approval.

**Scribe-coupling disclosure.** The scribe is the proposal's author. That is the
weaker configuration -- the party whose work was reviewed transcribes the ruling
on it. Mitigations: the authorization is quoted verbatim, and this commit carries
the Decision only.

**Engine obligations.** Touches `bootstrap/_scaffold/`, so the plan carries the
high-risk engine obligations and a Maintainer-run AST baseline re-anchor.
**Batch it** with `fork-advisory-semantics` so that ceremony is paid once.
