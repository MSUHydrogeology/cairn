# The profile loader guesses: make the installer's one input boundary report or refuse

**Author**: Claude (Strategy)
**Model**: Claude Opus 5
**Date opened**: 2026-08-03
**Status**: reviewed
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

## Decision -- {{Maintainer}} -- {{YYYY-MM-DD}}

*(Awaiting the Maintainer. The proposal has cleared External Security Review. The Maintainer may accept the proposal to proceed with plan creation.)*

