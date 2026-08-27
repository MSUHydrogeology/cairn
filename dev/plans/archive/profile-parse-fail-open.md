<!-- The new test module is a forward reference registered under `Proposed paths`; the
     marker exempts only its own contiguous block, and the chunk file tables cite it
     many sections later, so it needs the file-scoped directive too.  Drop this
     directive once the path lands (Chunk D), per the marker discipline. -->

# Plan: the profile loader stops guessing — a closed grammar on the installer's one input

**Source proposal**: `profile-parse-fail-open` (accepted as revised 2026-08-03;
the Decision commit is `d54f9f4`). It currently sits under `dev/proposals/` and
moves to `dev/proposals/archive/` when it archives.
**Status**: archived
**Plan review**: required(**External**, security lens) — carried verbatim from the
proposal header, which reads `required(External + External Security Review)`. The
proposal's own External round (Gemini Flash, SHIP) was a *proposal*-level round
and does **not** discharge this one. **No implementation commit lands before the
`## Plan review` section carries a real review.**
**Last update**: 2026-08-03
**Opened**: 2026-08-03

## Source proposal

`profile-parse-fail-open` establishes one contract on the installer's only
substantive input, the adopter's **profile** (`scaffold.py --config <file>`):

> For every profile text, `load_config` either **(a)** returns a value equal to
> `yaml.safe_load`'s, or **(b)** raises with a `<path>:<line>:` message naming
> the construct and the rewrite. **There is no third outcome — in particular, no
> content line is ever silently dropped.**

It went through an External security review (Gemini Flash, SHIP, 3 findings), an
author Response that flipped Part B from *warn* to *refuse*, a first revision, an
Internal security review with three BLOCKING findings, a Response that accepted
all ten, and a second revision that **replaced the enumerated refusal list with a
closed line grammar**. The Decision accepted it *as revised*, and added one
instruction: the change touches `bootstrap/_scaffold/`, so it carries the
high-risk engine obligations and a Maintainer-run AST baseline re-anchor —
**batched with `fork-advisory-semantics`** so that ceremony is paid once.

The proposal settles the design. This plan executes it and does not re-litigate
it. Three parts, in the proposal's own lettering:

* **Part A** — `_minimal_yaml_parse` stops being a best-effort reader and becomes
  a **recognizer**: eight accepted line forms (L1–L8), everything else refused
  with a file, a line number, and the rewrite. The grammar's checks are
  **textual**, so they run in `load_config` before dispatch to either parser —
  one acceptance contract whether or not PyYAML is installed.
* **Part B** — a key outside `RECOGNIZED_PROFILE_KEYS` is **refused** before any
  write, with the recognized set printed. A reserved `schema` key is read and
  ignored, so a future refusal can say *"this profile declares schema 2; this
  engine understands 1"* rather than *"unknown key"*.
* **Part C** — a drift gate: a marked corpus of everything Cairn ships, writes or
  documents, parsed through **both** parsers and asserted equal, with an oracle
  guard and a canary so the gate cannot pass vacuously.

Plus one **ordering precondition** promoted by the first revision from a plan
note to blocking: `bootstrap/_scaffold/upgrade.py:239`'s bare `except Exception`
must stop swallowing, **first or in the same change, never after**.

### Glossary — every term glossed on first use

The audience is a scientist who codes, and this scope is jargon-dense.

* **YAML** — a plain-text configuration format (`key: value` lines). The profile
  is a YAML file.
* **PyYAML** — the standard third-party library that parses YAML. Cairn ships
  **zero runtime dependencies**, so the engine imports it only *if it happens to
  be installed*.
* **The fallback** — `_minimal_yaml_parse`, the ~55-line hand-written parser at
  [`../../bootstrap/_scaffold/config.py`](../../bootstrap/_scaffold/config.py) line 84 that runs when PyYAML is
  absent. Cairn's zero-dependency promise makes this the **normal** path, not the
  exotic one.
* **Fail open** — a wrong or missing value that still exits 0. **Fail closed** —
  a refusal before anything is written.
* **Parity** — the two parsers return equal results for the same text.
* **Recognizer** — a parser that accepts only inputs matching a stated grammar and
  refuses everything else. Opposed to a **best-effort reader**, which returns
  something for any input.
* **Oracle** — the value a test compares against to decide pass/fail.
* **Canary** — a known input a gate must be *shown* to catch, so that a gate which
  has silently stopped working fails instead of passing.
* **AST attestation** — a structural fingerprint of every top-level symbol in the
  engine package, pinned against a committed baseline. It is insensitive to
  comments and formatting and sensitive to any logic change, and it does **not**
  auto-update.
* **Frozen set** — the file set whose bytes the gate manifest pins, so that a
  later edit to a gate's own definition is mechanically detectable.

## What the Decision settled, and the one thing it did not

**Settled, and not this plan's to reopen.** Refuse-on-unknown-key. The proposal's
Response measured the availability cost before conceding it — no shipped profile
under `bootstrap/profiles/` carries a key outside the recognized set, and both
engine-side profile writers emit only recognized keys — and I re-verified that
independently for this plan (see *Gate accounting*: 3 of 3 shipped profiles carry
only `preset`, `project_name`, `test_command`, `as_of 2026-08-03`). The
older-engine/newer-profile hazard the External round raised is answered by the
reserved `schema` key, not by an opt-out; both proposed opt-outs were declined
with reasons, and this plan ships neither.

**Carried, unresolved, and recorded rather than answered.** The proposal's
*Maintainer decision points* section listed four calls. Three of them are changes
*inside* the revision the Decision accepted "as revised" — the single acceptance
contract on both parser paths (1), the reserved `schema` key (2), and the
ordering against the sibling (3) — and this plan reads them as carried, which is
a reading, not a ruling. **Decision point 4 is different**: it asked whether *one
focused Internal re-review of the grammar's totality claim* should run before
plan-open, and the author recommended yes. The Decision's authorization —

> I approve each of the seven proposals that you have listed as ready to accept,
> as revised.

— speaks to the proposals, not to that process question, and this plan is being
opened without that round. Two facts a reader must hold together:

1. The recommended round was a **proposal-level Internal** pass, scoped to the
   grammar's totality claim and the canary rule.
2. This plan's `required(External, security lens)` **plan review** is a separate,
   plan-level round that gates implementation regardless.

The author's stated reason for wanting (1) is the one that survives into this
plan: *"the last time this proposal claimed a structural property, the property
did not hold on the path that matters"* — finding [I1], where A4 was grounded in
a guard (`if not isinstance(cfg, dict)`) that is structurally unreachable on the
fallback path. Part (b) of the new invariant is exactly such a structural claim.
**If the Maintainer intended decision point 4 to stand, it is theirs to say so in
one line before Chunk A**; if the plan-review round is meant to absorb it, that
brief is written into *Plan review* below as mandate 1.

## Proposed paths

Proposed paths:
- `bootstrap/tests/test_profile_grammar.py` — the pytest home for every NEW node this plan adds (grammar soundness, totality, the writer round-trip, the marker sweep, the canaries); lands in Chunk B and grows through Chunks C and D.

## Scope

Executes the proposal as revised through its **second** revision (the closed line
grammar), which governs wherever it conflicts with the original *Proposal* or the
first revision. Chunk M is the Maintainer's and is fenced from the implementing
agent's work by construction.

**Out of scope, fenced explicitly:**

* **The correctly-spelled key carrying an unrecognized *value*.** A profile
  listing `- not-a-real-module` under `modules:` is accepted at exit 0 today and
  stays accepted. Both revisions fence it out; this plan makes no claim on it and
  lands it as a residual row (Chunk G).
* **Making `_minimal_yaml_parse` a YAML parser.** It becomes a recognizer for the
  profile subset. The proposal's *Signals the change is wrong* row about the
  grammar accreting forms stays live and is restated in *Acceptance criteria*.
* **Preset composition.** The first revision's scope guard: `content-security`
  being selected by no preset reproduces, lives in the *same file* this plan
  edits, and is deliberately declined. This plan changes **how a profile is
  read**, not **what a preset selects**.
* **`bootstrap/_scaffold/upgrade.py:1136`** (the `init-lock` arm's `load_config`
  call). It already prints `error loading dev/.cairn/profile.yml: <exc>` and
  returns 1 — loud and correct. Only `_resolve_current_profile` swallows; the
  fix is scoped to that one call site, not to "the upgrade path".
* **`_infer_init_lock_axes`'s `CONTRIBUTING.md` inference defect**, recorded as
  residual R1 of a sibling scope. Different function, same file; folding it in
  would break this plan's falsifiable AST target. Not claimed here.
* **Fixing the gate manifest's SKIP-XFAIL-NEW over-report** (measured below). A
  pre-existing gate defect in a frozen file; naming it is this plan's obligation,
  fixing it is not.
* **Any change to the install contract.** No file enters or leaves the install
  set; `scaffold.py --manifest` must be byte-identical before and after, and that
  equality is an assertion, not an expectation.

**Sequencing invariant — every intermediate commit is fail-closed.** The chunks
split one acceptance contract across several commits. At no point does a
partially-implemented `load_config` *accept* something the finished one would
refuse: an unimplemented branch refuses. A reviewer should check this claim per
chunk rather than take it here.

**The one deliberate exception to "the suite is green at every commit", priced.**
From this plan's first engine commit until the Maintainer runs Chunk M, exactly
**two** suite nodes are red, both in `bootstrap/tests/test_ast_attest.py`:
`test_committed_baseline_accounted_for_across_the_engine_package` (at line 51)
and `test_ast_gate_passes_over_the_full_scaffold_module_set` (at line 74).
They are the only two of that module's **29 collected nodes** (`as_of
2026-08-03`) that verify the committed baseline against the live engine package;
the other 27 build synthetic modules under `tmp_path` — established by reading
the module and collecting it, not by assuming. Because the
Decision batches this re-anchor with `fork-advisory-semantics`, that red window
spans **both** plans' engine work. This is a known, bounded cost of paying the
ceremony once; it is not a licence to leave any other node red.

### Documentation / doctrine surface

* **Descriptive layer** — `bootstrap/BOOTSTRAP.md` is the main change: Appendix B's
  **Schema rules** list (at `bootstrap/BOOTSTRAP.md:748`, verified this session)
  gains the grammar as a contract an adopter can rely on, plus the unknown-key
  rule that is absent from Appendix B today. `bootstrap/UPGRADE.md` gains one
  sentence reconciling the two `dev/.cairn/` dispositions ([I6]): the lockfile
  tolerates unknown keys because it carries a `schema` field; the profile refuses
  them because, until now, it carried no version signal at all.
* **The installer's own `--help`** — the `bootstrap/_scaffold/cli.py` module
  docstring. Its `forge: gitlab        # gitlab | github` line at
  `bootstrap/_scaffold/cli.py:28` becomes *correct* under the grammar rather than
  needing rewriting. That is the deliberate design goal, and the only edit the
  docstring needs is none at all — the corpus anchor is an existing line (Chunk D).
* **A code comment that will otherwise document the opposite of the behaviour** —
  `bootstrap/_scaffold/config.py:46`–49 currently reads *"unknown keys from the
  config are silently ignored so that future tokens do not break old configs."*
  That is the reversed intent, inside the module that holds the `_MODULE_MAPPINGS`
  trust anchor. Rewriting it is mandatory, not tidy-up.
* **Deliberation layer** — this plan, its plan review, its code review, and the
  residual rows it lands on `dev/PLANNING.md`.
* **Entry layer** — none. **Governing layer** — **none**: no `AGENTS.md` change
  and no `doctrine/` change. Nothing here alters how a contributor works.
* **`CHANGELOG.md > Unreleased > Changed/Fixed`** — the profile is read by a
  closed grammar; unknown keys refuse. This is adopter-visible behaviour on the
  install contract's *input*, so it is release-facing.
* **No adopter-installed file changes.** Confirmed by inspection of the surfaces
  listed above: `bootstrap/`-prefixed documentation and the engine are Cairn-side;
  no `templates/` or `dev/modules/` file is touched.

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

Every figure below was measured this session under the canonical interpreter
(`~/conda_envs/lhm/bin/python`, Python 3.13.13) with `PYTHONDONTWRITEBYTECODE=1`,
at working-tree HEAD `05515df`. Each is a dated snapshot to re-check at
implementation, not a number quoted from the proposal.

**Suite baseline.** `python -m pytest bootstrap/tests` → **1601 passed, 0 failed,
0 skipped, 0 xfailed**, 154s, `as_of 2026-08-03`. (The proposal's `1556 passed`
is stale; it was measured on a working tree carrying another session's
uncommitted work and told the plan to re-measure. This is that re-measurement.)

**Which re-anchor ceremony applies — and the plan says it plainly, because
`AGENTS.md` gets this wrong.** `AGENTS.md`'s operational-pitfall entry routes an
AST-baseline re-anchor to `bootstrap/REANCHOR_RUNBOOK.md`. That runbook governs a
**different** gate (the supervised gate-manifest promotion) and contains zero
mentions of `ast_attest` or `scaffold_ast_baseline` — already recorded as deferred
Maintainer question 4 on `dev/PLANNING.md`, with the note that it *"seeded four
freshly-drafted proposals on 2026-08-03 before reconciliation caught two."* This
plan does not repeat that error.

* **(i) The AST source-motion attestation — this is the ceremony that applies.**
  `bootstrap/tests/test_ast_attest.py` pins every top-level symbol under
  `bootstrap/_scaffold/*.py` against
  `bootstrap/tests/fixtures/scaffold_ast_baseline.json`. Measured: **174 baselined
  symbols across 10 engine modules, 0 CHANGED / MISSING / DUPLICATE**, `as_of
  2026-08-03`. The self-service repair path is **not available**:
  `_ast_attest._UPDATE_ALLOWLIST` admits exactly four symbols (`_MODULE_MAPPINGS`,
  `_SKILLS_MAPPINGS`, `_CORE_MAPPINGS`, `install_onboarding`) and none of this
  plan's symbols is among them. The mechanism that applies is the one
  `lockfile-provenance-fields` established and used: a **Maintainer-run,
  dry-run-verified direct-correction script**, recorded in a commit the Maintainer
  authors (`c3d5bd9`, whose body states *"the correction itself was performed and
  decided by the Maintainer"*). **An implementing agent does not perform it.**

  **The falsifiable pre-re-anchor target**, derived for this plan against the real
  committed baseline rather than assumed:

  * **exactly 2 CHANGED** — `FunctionDef:_minimal_yaml_parse` (baseline digest
    `752c30f3f1220eda`) and `FunctionDef:load_config` (baseline digest
    `18c69e0ea95a7a7e`), both in `bootstrap/_scaffold/config.py`;
  * **0 MISSING, 0 DUPLICATE**. `_list_item_text` is a *nested* function and is
    not a baselined key, so retiring it drops nothing;
  * `bootstrap/_scaffold/cli.py` contributes **zero AST delta** — only its module
    docstring is in scope and `_classify()` skips `Docstring` keys in both
    directions;
  * `bootstrap/_scaffold/upgrade.py` contributes **zero AST delta** —
    `FunctionDef:_resolve_current_profile` is *not* in the 174-key baseline
    (verified: it is reported today as `note: NEW FunctionDef:_resolve_current_profile`),
    so editing it changes a note, never a pin;
  * **`0 DUPLICATE` has a mechanism this plan can actually trip, and the
    stop-the-line rule above would misread it.** The baseline is keyed by **bare
    symbol name** — its 174 entries carry `digest` / `span` / `type` and **no
    module field** (verified 2026-08-03) — and `_classify` reports `DUPLICATE`
    for any *baselined* key found in two files, which is a hard failure (`rc 1`),
    not a note. So a new top-level helper added to `bootstrap/_scaffold/config.py`
    under a name already baselined in **another** engine module fails the
    attestation as *"single-source broken"* — and that is a naming collision, not
    tamper-evidence. The near-misses are real for this scope: `_yaml_sq`
    (`bootstrap/_scaffold/upgrade.py:2039`) and `_yaml_dq`
    (`bootstrap/_scaffold/install.py:636`) are exactly the names Chunk B's
    single- and double-quoted scalar handling reaches for. Demonstrated this
    session: appending a `def _yaml_sq` to a scratch copy of `config.py` reports
    `DUPLICATE FunctionDef:_yaml_sq (defined in 2 files: … — single-source broken)`
    and `AST attestation FAILED`. **Every new Chunk B / Chunk C top-level name is
    checked against the 161 baselined `FunctionDef:` / `Assign:` / `ClassDef:`
    keys before its commit, and a `DUPLICATE` reported on a name this plan's
    Chunk B or Chunk C introduces is a rename, not a stop-and-explain. Every
    other `DUPLICATE` stays in the stop-and-explain class.** Note what the
    pre-commit check implies: it is what makes a collision on one of this plan's
    own names the case that should not reach the gate at all, so a `DUPLICATE`
    that surfaces at the ceremony anyway is by construction *not* one of this
    plan's names — which is exactly the unexplained baseline delta the stop rule
    is for;
  * NEW notes for the added symbols (`Assign:RECOGNIZED_PROFILE_KEYS`,
    `FunctionDef:unrecognized_profile_keys`, and each top-level grammar helper),
    plus rotated `Import:` keys — reported as notes, never failures.

  **A 3rd CHANGED symbol is a stop-and-explain, not a re-run.** The proposal's own
  stop-the-line signal applies here, with one adjustment the Internal review
  demanded: it is read *after* accounting for `fork-advisory-semantics`'s
  legitimate symbol motion, not before.

* **(ii) The gate manifest — and a defect in it that this plan must not pretend
  away.** `bootstrap/tests/_gate_manifest.py` freezes **164 files**, `as_of
  2026-08-03`, and no `bootstrap/_scaffold/` file is among them. But
  `bootstrap/tests/test_scaffold.py` and `bootstrap/tests/test_presets.py`
  **are** frozen, and both are homes the proposal named. Two measured facts
  follow, neither of which the proposal knew:

  1. `python bootstrap/tests/_gate_manifest.py verify --anchor-ref e45e1fc` run
     against the working tree **today, before this plan writes anything**, already
     reports `HOLD — 5 gate-integrity violation(s)`: two `FROZEN-MODIFIED` and
     three `SKIP-XFAIL-NEW`, all inherited from the `r6-unused-def-blindspot`
     commit `7066489`. The verifier is a **supervised command, not a suite node** —
     nothing in `python -m pytest bootstrap/tests` invokes it — so this plan states
     what it can honestly claim: it adds to an existing delta, and the disposition
     is the Maintainer's at the next supervised ceremony.
  2. **`SKIP-XFAIL-NEW` fires on ordinary new tests.** The check uses
     `item.get_closest_marker("skipif")`, which resolves *module-level*
     `pytestmark`. `bootstrap/tests/test_presets.py` carries
     `pytestmark = pytest.mark.skipif(not TEMPLATES_ROOT.exists(), ...)` at line 56,
     so **34 of its nodes are already recorded as "marked"** while the suite reports
     **0 skipped**. Any node added to that file registers as
     `SKIP-XFAIL-NEW: … (a test gained a skip/xfail marker)` — which is precisely
     what happened to `7066489`'s three new nodes.

  **The consequence for this plan, decided rather than discovered at review time:**
  every **new** test node goes in a **new** module,
  `bootstrap/tests/test_profile_grammar.py`, which reads as `FROZEN-NEW` (*"new
  gate/test file — allowed, recorded"*) and carries **no module-level marker**.
  Edits to the two frozen files are confined to the **two existing tests the
  proposal requires be inverted or completed** ([I9], Chunk E) — the minimum
  unavoidable frozen edit. This adopts the `lockfile-provenance-fields` blocking
  [R2] lesson verbatim (*"All new nodes go in the new file, never appended to the
  frozen one"*) and supersedes the original proposal's *"no new test module"*
  line, which its own Response already withdrew.

* **(iii) The engine security gates.** `bootstrap/tests/test_security_lint.py`
  runs Bandit over the engine package. The change adds no `subprocess`, no `eval`,
  no new file write, and no non-stdlib import — the grammar is `str` and `re`
  work, and `re` is already imported at `bootstrap/_scaffold/config.py:28`.
  `bootstrap/tests/test_security_leaf.py`'s pinned `_GUARDED_WRITE_FUNCS` set is
  unchanged: this plan adds no adopter-tree write. `vermin`'s declared floor is
  3.11 and the new code must not raise it.

* **(iv) The install contract.** `python bootstrap/scaffold.py --manifest` diffed
  before and after — **expected empty**. No file enters or leaves the install set.

## Sequence

```
0. plan-open      -- this plan + the dev/PLANNING.md row-move            [commit pending]
   (plan review)  -- required(External, security lens); NO code before it lands
1. Chunk A -- upgrade.py:239 stops swallowing (blocking precondition)    [commit pending]
2. Chunk B -- the closed line grammar; load_config becomes a recognizer  [commit pending]
3. Chunk C -- unknown keys refuse; the derived set; reserved `schema`    [commit pending]
4. Chunk D -- the drift gate: marker corpus, both writers, two canaries  [commit pending]
5. Chunk E -- the two existing tests that contradict the change          [commit pending]
6. Chunk F -- documentation: BOOTSTRAP.md, UPGRADE.md, CHANGELOG         [commit pending]
7. Chunk G -- residual homes on dev/PLANNING.md                          [commit pending]
8. Chunk M -- MAINTAINER-ONLY: the batched AST re-anchor                 [not an agent's]
```

**Ordering is not cosmetic here.** Chunk A is a blocking precondition promoted by
the first revision: *"narrowing that handler so it reports what it swallowed lands
first, or in the same change — never after."* A stricter `load_config` feeds that
handler more exceptions; landing B before A would trade a loud install-time
failure for a quiet upgrade-time one, which is the fail-open hazard this plan
exists to close, moved rather than removed.

### Chunk A — `upgrade.py:239` stops swallowing (the blocking precondition)

| # | File | Change |
|---|------|--------|
| A1 | `bootstrap/_scaffold/upgrade.py` | `_resolve_current_profile`'s bare `except Exception` at line 239 prints what it swallowed — the profile path, the exception type, and the message — on `stderr`, before returning the lockfile fallback. The **fallback disposition is unchanged**; only its silence is. |
| A2 | `bootstrap/tests/test_profile_grammar.py` *(new)* | An unreadable / ungrammatical `dev/.cairn/profile.yml` in a fixture target makes `_resolve_current_profile` emit a message naming the path **and** still return the lockfile profile. Asserted on captured `stderr` and on the returned value, so a future change that makes it loud-and-fatal, or quiet-and-tolerant, both fail. |

**Acceptance criteria — Chunk A**

* **Command that decides it**: `python -m pytest bootstrap/tests/test_profile_grammar.py -k resolve_current_profile`, plus the full suite green (excluding the two AST nodes priced above).
* **Perturbation, and it is runnable today**: delete the new `print(..., file=sys.stderr)` line → A2 fails. Restore byte-identical → green. Recorded as a mutation ledger in the commit body. This is a real future state, not a synthetic one: the handler is *currently* silent, so the pre-fix tree **is** the mutant, and A2 must be run against `bootstrap/_scaffold/upgrade.py` at HEAD and shown to fail before the fix lands.
* **Channel accounting**: the test's oracle is the *absence* of a message at HEAD and its *presence* after — observed on the subprocess/`capsys` stream, not on any value the function returns. The fixture profile is written by the test, not produced by the engine.
* **Not established, and stated**: this makes the fallback *audible*. It does not make it *safe*. Whether the lockfile fallback is the right disposition at all is out of this fence and lands as a residual row (Chunk G).

### Chunk B — the closed line grammar: `load_config` becomes a recognizer

The security core, and the smallest self-contained unit a scoped External round
can be run against. The grammar's checks are **textual** and run in `load_config`
over the raw text *before* dispatch, so there is one acceptance contract on both
parser paths ([I5], Maintainer decision point 1).

| # | File | Change |
|---|------|--------|
| B1 | `bootstrap/_scaffold/config.py` | A line-form recognizer over the raw text. Every non-blank line matches exactly one of L1–L8 (blank/comment; a single leading `---`; `key: <plain scalar>`; `key: '<single-quoted>'` with `''`→`'`; `key: "<double-quoted>"` with no backslash and no interior `"`; `key: []`; bare `key:`; `- <scalar>` at a consistent indent under an open bare key) or the profile is refused. |
| B2 | `bootstrap/_scaffold/config.py` | The plain-scalar admissibility rule, with the comment convention stated explicitly: a `#` starts a comment **only at line start or when preceded by a space or tab**. After comment removal the value must not begin with an indicator character (`&` `*` `!` `|` `>` `[` `{` `@` `` ` `` `%`), must not be a bare YAML-1.1 boolean/null, must contain no `: `, must not end in `:`, must contain no `"` or `'`, and — if it begins with a digit, `-`, `+` or `.` — must match the canonical integer `-?(0\|[1-9][0-9]*)`, yielding an `int`. |
| B3 | `bootstrap/_scaffold/config.py` | Refusals carry `<path>:<line>: <reason>` **and the rewrite** (`modules: [a, b]` → a `- ` list; `forge: no` → `forge: "no"`; `size: 010` → *"may be read as a number, date or time; write it quoted"*). "Install PyYAML" is never an acceptable remedy in a zero-dependency project. |
| B4 | `bootstrap/_scaffold/config.py` | A document producing **no content lines at all** (zero-byte, whitespace-only, comment-only, uniformly indented) is **refused**, matching PyYAML's `None`. A literal `{}` document is the one carve in the other direction and is accepted as an empty mapping by explicit rule, never by falling through. |
| B5 | `bootstrap/_scaffold/config.py` | `_minimal_yaml_parse` is rewritten to the same grammar and `_list_item_text` (line 98) retires. A bare `key:` with nothing under it yields `None`, not `[]` — the faithful reading, and the one that closes the init-lock writer's zero-modules divergence. |
| B6 | `bootstrap/tests/test_profile_grammar.py` | **Grammar soundness, generative**: inputs generated from L1–L8 and asserted equal to `yaml.safe_load`. The proposal's twelve-row divergence table plus the Internal review's seven rows become *seed* cases, not the whole test. |
| B7 | `bootstrap/tests/test_profile_grammar.py` | **Grammar totality**: for a malformed-input corpus, `load_config` raises with a line number and **no input returns a partial dict**. Contains every row from [I1], [I2], [I3] and [I4] by name. |
| B8 | `bootstrap/tests/test_profile_grammar.py` | **Both directions of the comment rule** ([I2]): `forge: gitlab   # c` → comment stripped; `project_name: a#b`, `project_name: issue#42-tracker` and `test_command: pytest -k not-slow#fast` → hash **preserved**. |
| B9 | `bootstrap/tests/test_profile_grammar.py` | **CRLF**, combined with quoting and comments — the proposal's named open gap, closed by measurement rather than left open (see criteria). |

**Acceptance criteria — Chunk B**

* **Commands that decide it**: `python -m pytest bootstrap/tests/test_profile_grammar.py`; then the full suite (two AST nodes excepted, per *Scope*); then
  `python bootstrap/scaffold.py --summary --config <p>` and `--dry-run` on all
  three profiles under `bootstrap/profiles/`, run **twice** — once normally, once
  under a `sys.meta_path` finder that raises `ImportError` on `yaml` — with the
  two outputs required to match.
* **The oracle arrives by a channel that is not the artifact.** Every parity
  assertion imports `yaml` **directly**. `_yaml_load` is **banned as an oracle**:
  it *is* `_minimal_yaml_parse` when PyYAML is absent, so an assertion of the form
  `_yaml_load(x) == _minimal_yaml_parse(x)` compares the function under test to
  itself. Two live tests model the banned pattern and are named so nobody copies
  them: `test_flat_schema_parses_identically`, defined at
  `bootstrap/tests/test_presets.py:292`, and the parity assertion at
  `bootstrap/tests/test_presets.py:423` inside
  `test_literal_recipe_yaml_also_parses_via_pyyaml` — a test whose *name* asserts
  the very thing its body cannot guarantee.
* **The oracle-identity canary** (this plan's sharpening of the proposal's canary
  rule, because after Part A no *accepted* input diverges and a divergence canary
  alone would go stale): the parity nodes assert
  `isinstance(yaml.safe_load("d: 2024-01-01")["d"], datetime.date)`. Measured
  2026-08-03 under PyYAML 6.0.3: **True**. No stdlib recognizer can return a
  `datetime.date`, so this cannot pass if the oracle has silently become the
  function under test. **Perturbation, runnable today**: set `sys.modules['yaml'] = None`
  before import and route the oracle through `_yaml_load` → the canary fails.
* **The divergence canary**: `modules: [a, b]` — PyYAML yields `{'modules': ['a', 'b']}`,
  the grammar **refuses**. The gate asserts it sees that disagreement, so a gate
  that has stopped being able to *see* a difference fails instead of passing.
* **Red-then-green, measured before the fix**, not asserted. Every row below was
  run this session at HEAD `05515df` under the canonical interpreter with PyYAML
  blocked by a `sys.meta_path` finder, with `config._yaml` printed as `None` to
  prove the branch was taken:

  | input | PyYAML | fallback at HEAD | must become |
  |---|---|---|---|
  | zero-byte / whitespace-only / comment-only | refused (`NoneType`) | `ACCEPTED {}` | refused |
  | `  project_name: X` / `  preset: high-rigor-legacy` (uniformly indented) | full mapping | `ACCEPTED {}` | equal |
  | `forge: gitlab        # gitlab \| github` | `'gitlab'` | `'gitlab        # gitlab \| github'` | equal |
  | `project_name: 'O''Brien Lab Model'` | `"O'Brien Lab Model"` | `"O''Brien Lab Model"` | equal |
  | `modules: [a, b]` | `['a','b']` | `'[a, b]'` (string) | refused |
  | `parent:` / `  child: val` | nested dict | `{'parent': []}` | refused |
  | `modules:` / tab-indented `- item` | `ScannerError` | `{'modules': ['item']}` | refused |
  | `preset:solo-greenfield` | plain scalar → refused | `{'preset': 'solo-greenfield'}` | refused |
  | `forge: no` | `False` | `'no'` | refused (quote it) |
  | `schema: 010` | `8` | `'010'` | refused (quote it) |
  | `project_name: 1:30` | `90` | `'1:30'` | refused (quote it) |
  | `project_name: X` / `modules:` (bare) | `{'modules': None}` | `{'modules': []}` | equal |

  The **uniformly-indented** row is the sharpest and is the one this plan must not
  lose: it is what a copy-paste out of a rendered documentation page produces, and
  at HEAD it silently installs the six default-on modules instead of a
  twelve-module high-rigor tree, at exit 0.
* **CRLF, closed rather than deferred.** Measured 2026-08-03 across seven shapes
  (plain, comment, double-quoted, single-quoted, list, trailing-space-quote, lone
  `\r`): CRLF introduces **no divergence class of its own**. The two failing
  shapes (`crlf comment`, `crlf sq`) are exactly the LF failures already in the
  table, because `line.strip()` removes `\r` before any parser logic runs and
  PyYAML treats both `\r\n` and a lone `\r` as line breaks. **Perturbation for
  B9**: implement the grammar's line split as `text.split("\n")` instead of
  `text.splitlines()` → the lone-`\r` case regresses and B9 fails. That is the
  future state B9 exists to catch, and it is a plausible one.
* **Mutation ledger in the commit body**, one row per control: delete the
  empty-document refusal → the empty/indented totality node fails; delete the
  whitespace condition from the comment rule → the `issue#42-tracker` node fails;
  delete the `''`→`'` unescape → the writer round-trip node fails. Restore
  byte-identical each time. **A test whose deletion-mutant stays green is not
  accepted.**
* **Availability, re-measured before the cut**: all three profiles under
  `bootstrap/profiles/`, both engine writers' real output, the `BOOTSTRAP.md`
  preset block and the `cli.py --help` block — **all accepted, all equal to
  `yaml.safe_load`, zero refusals**. A refusal on any of them is a stop, not a
  finding.
* **Recorded as not established**: part (a) of the invariant is *verified over a
  finite corpus, not proved*. The generative test samples the grammar; it does not
  prove no accepted input diverges. Part (b) — totality — **is** structural, and
  that is the claim the plan review is asked to attack first.

### Chunk C — unknown keys refuse; the derived set; the reserved `schema`

| # | File | Change |
|---|------|--------|
| C1 | `bootstrap/_scaffold/config.py` | `RECOGNIZED_PROFILE_KEYS`, **derived** at module level from `KNOWN_TOKENS` ∪ the six `_AXES` keys ∪ the five structural keys (`preset`, `modules`, `modules_add`, `modules_remove`, `forge`) ∪ the reserved `{"schema"}`. Verified this session: the first three sets union to **16** keys; with `schema`, **17**. Never a hand-maintained list. |
| C2 | `bootstrap/_scaffold/config.py` | `unrecognized_profile_keys(cfg) -> list[str]` — pure. No filesystem, no mutation. |
| C3 | `bootstrap/_scaffold/config.py` | `load_config` **refuses** a profile carrying any unrecognized key, before any write, naming every unrecognized key and printing the recognized set. |
| C4 | `bootstrap/_scaffold/config.py` | **Ordering that makes the reserved key worth its entry**: `schema` is read *first*. A profile declaring a `schema` this engine does not understand refuses with *"this profile declares schema N; this engine understands M — upgrade Cairn"*, **not** with an unknown-key list. Without this ordering the reserved key buys nothing. |
| C5 | `bootstrap/_scaffold/config.py` | The comment at lines 46–49 is rewritten. It currently documents the reversed intent inside the module that holds the `_MODULE_MAPPINGS` trust anchor. |
| C6 | `bootstrap/tests/test_profile_grammar.py` | **Derivation test**: `RECOGNIZED_PROFILE_KEYS` equals the computed union, asserted against `KNOWN_TOKENS`, `_AXES` and a literal structural set — so it cannot become a fourth hand-maintained list. |
| C7 | `bootstrap/tests/test_profile_grammar.py` | **Refusal-before-write**: each of the four measured typo rows (`presets:`, `module_add:`, `agent_teams:`, `project_nmae:`) refuses at `--summary` **and** at a real install, with **no file written** into the target. |
| C8 | `bootstrap/tests/test_profile_grammar.py` | **The `schema` path**: `schema: 1` is accepted and ignored; `schema: 2` refuses with the version message, not the unknown-key message. |

**Acceptance criteria — Chunk C**

* **Commands that decide it**: `python -m pytest bootstrap/tests/test_profile_grammar.py -k "recognized or unrecognized or schema"`; and, for C7, `python bootstrap/scaffold.py --summary --config <typo>` expected non-zero with the offending key named.
* **The premise is re-measured, not inherited.** Run this session at HEAD: a
  `module_add:` typo produces `--summary` output **byte-identical** to a correct
  `solo-greenfield` run — `cmp` on both stdout and stderr returns equal, both exit
  0. That is the red state: there is not a warning to miss, there is *nothing* to
  miss, and the dropped module in the measured case is `security-review`.
* **Perturbation**: delete the `unrecognized_profile_keys` call from `load_config`
  → C7 fails on all four rows. Delete the `schema`-first ordering → C8 fails while
  C7 still passes, which is why they are separate nodes.
* **Channel accounting**: the *expected* recognized set arrives from the three
  source definitions read independently by the test (C6), never from
  `RECOGNIZED_PROFILE_KEYS` itself — a test that asserted the constant against
  itself would be the [I7] oracle collapse in a different costume.
* **Availability, asserted not assumed**: all three shipped profiles under
  `bootstrap/profiles/` carry only `preset`, `project_name`, `test_command` —
  re-verified this session, `as_of 2026-08-03` — and both engine-side writers emit
  only recognized keys. Refusal breaks nothing that exists today.
* **Recorded as not established**: the forward-compatibility cost of refusing is
  **argued, not measured**. Cairn has zero external adopters, so there is no field
  data in either direction, and the reserved `schema` key rescues no engine
  already released — it is free only because "engines already deployed" is an empty
  set, and it stops being free after the first adopter. Residual row, Chunk G.

### Chunk D — the drift gate: a marked corpus, both writers, and two canaries

This is the piece the 2026-07-11 prose-only remedy lacked, and the reason the
identical defect was still shipping 23 days later.

| # | File | Change |
|---|------|--------|
| D1 | `bootstrap/BOOTSTRAP.md` | An invisible HTML-comment marker above each of the two profile-shaped fenced blocks (`<!-- cairn-parity-corpus: appendix-b-example -->` and `<!-- cairn-parity-corpus: preset-example -->`), with a "marker appears exactly once" assertion carried forward from `_extract_marked_yaml`. Corpus by **explicit marker, not by shape** ([I8]). |
| D2 | `bootstrap/tests/test_profile_grammar.py` | The `--help` corpus entry anchors on the literal line `# Inline token values (mechanical substitution)` inside `cli.__doc__`, asserted to appear **exactly once** (verified this session: count 1) — **no adopter-visible marker is added to `--help`**. |
| D3 | `bootstrap/tests/test_profile_grammar.py` | **Both engine writers' real output** in the corpus ([I3]): `_write_init_lock_profile_template` (`bootstrap/_scaffold/upgrade.py:1074`) at one *and* at **zero** installed modules, and `_self_heal_profile_config` (`bootstrap/_scaffold/upgrade.py:2046`) with a `project_name` and a `test_command` **containing an apostrophe**. The writers are **called**, into a temp tree; their output is never reconstructed by the test. |
| D4 | `bootstrap/tests/test_profile_grammar.py` | The sweep imports `yaml` **directly**, and hard-skips *from inside the test body* (`pytest.skip`), never via a `skipif` marker — because a marker is recorded by the gate manifest's collection identity and produces `SKIP-XFAIL-NEW`. Both canaries from Chunk B ride on this node. The skip **message names its own consequence** — *"PyYAML absent: the parity sweep and both canaries did not run"* — because nothing mechanically enforces the suite's `0 skipped` invariant and the summary line is the only place the loss shows (see criteria). |
| D5 | `bootstrap/tests/test_profile_grammar.py` | The end-to-end node **under a genuinely forced no-PyYAML interpreter**, reusing the existing subprocess pattern at `bootstrap/tests/test_presets.py:425` (`sys.modules['yaml'] = None` set before `bootstrap.scaffold` is ever imported): the `BOOTSTRAP.md` preset block and the `--help` block each install to trees byte-identical to their PyYAML runs. |

**Acceptance criteria — Chunk D**

* **Command that decides it**: `python -m pytest bootstrap/tests/test_profile_grammar.py -k "sweep or corpus or writer"`.
* **The reproduction check, measured rather than promised.** The sweep **must fail
  against today's HEAD**; a plan that lands it green did not reproduce the defect.
  Measured this session at `05515df`, the documentation corpus is **3 entries, 2
  divergent**: `cli.__doc__` (divergent — the `forge:` line), the `BOOTSTRAP.md`
  fence opening at line 730 (divergent — `preset:` at line 734 and `agent_team:` at
  line 739), and the `BOOTSTRAP.md` fence opening at line 696 (**equal** today, and
  its presence in the corpus is what makes the sweep a gate rather than a
  three-line assertion). Adding the two writers takes the red count to **4 of 5**.
* **The reproduction check is only meaningful on an interpreter where the canary is
  detected** — otherwise a stdlib-only run would report the sweep green at HEAD and
  the record would say "the defect did not reproduce". The canaries are checked
  first in the same node.
* **Channel accounting, stated per input**: the corpus text arrives from the
  *shipped* Markdown and from `cli.__doc__` read at import; the writer entries
  arrive from **calling the real writers** into a temp tree (the first revision's
  "parses identically" claim was true of a synthesized reconstruction and false of
  the writer — the same verify-with-your-own-material error this plan is required
  to avoid); the oracle arrives from `import yaml`. None of the three is produced
  by `_minimal_yaml_parse`.
* **Perturbation**: revert `bootstrap/BOOTSTRAP.md` line 734 to its HEAD text in a
  scratch copy → the sweep fails and names that block. Delete the `''`→`'`
  unescape → D3's `_self_heal_profile_config` entry fails. Delete a marker → the
  count-1 assertion fails rather than the block silently leaving the corpus.
* **The over-inclusion the shape heuristic would have caused, recorded so the
  marker choice is defensible**: a shape-based sweep picks up
  `bootstrap/fidelity-check.md`'s fidelity-manifest example (a deeply nested
  document the fallback is never meant to parse) and two archived-proposal blocks.
  A marker-defined corpus admits none of them, and a permanent allowlist is
  exactly the *"the documentation sweep test becomes a nuisance"* signal firing
  before the test is written.
* **0 skipped stays 0 — and nothing mechanically enforces that.** PyYAML 6.0.3 is
  present on the canonical host, so D4's in-body skip does not fire. The claim
  this bullet originally carried — that a fired skip *"fails loudly"* — is
  **wrong and is corrected here**: verified 2026-08-03, **no suite node, no
  conftest hook and no CI job enforces a skip count**
  (`bootstrap/tests/conftest.py` carries only the order-independence shuffle
  hook, and the repository has no workflow directory). On a PyYAML-less host D4
  skips, taking the sweep **and both canaries** with it, and `python -m pytest
  bootstrap/tests` still exits 0. Hence D4's self-describing skip message: the
  pytest summary line is the only place the loss is visible, and a canary that
  can be skipped away is the collapse it exists to detect, one level up. Making
  the invariant mechanical is a residual (G6), not this plan's fence.

### Chunk E — the two existing tests that contradict the change

The proposal originally said *"no new test module"* as though nothing existing
needed retiring. Its Response withdrew that. These are the only two edits this
plan makes to a frozen file.

| # | File | Change |
|---|------|--------|
| E1 | `bootstrap/tests/test_scaffold.py` | `test_mixed_indent_list` (line 204) is **inverted**: mixed indentation is refused. Its docstring — *"not valid YAML strictly speaking, but the minimal parser is forgiving"* — endorses the exact posture this change reverses, and PyYAML raises `ParserError` on that input. |
| E2 | `bootstrap/tests/test_scaffold.py` | `test_raises_on_invalid_yaml` (line 246) is given **the assertion it has never had**. Its body today is a `write_text` followed by three comment lines ending *"We tolerate the minimal parser's inaccuracy here."* — a test named for a refusal, asserting nothing, sitting in the file the new refusal behaviour lands beside. |

**Acceptance criteria — Chunk E**

* **Command that decides it**: `python -m pytest bootstrap/tests/test_scaffold.py -k "mixed_indent or invalid_yaml"`.
* **Perturbation for E2, and it is the whole point**: E2 currently **cannot fail**,
  because it asserts nothing. The check is that the completed node fails against
  `bootstrap/_scaffold/config.py` at HEAD (where a bare list is silently turned
  into a mapping-shaped `{}` on the fallback path) and passes after Chunk B. Run
  it in that order and record both.
* **Perturbation for E1**: restore the pre-Chunk-B `_minimal_yaml_parse` → E1
  fails. An inverted assertion that would pass under both the old and the new
  parser is not an inversion.
* **Frozen-file discipline**: the diff on `bootstrap/tests/test_scaffold.py` shows
  **only** these two nodes changed and **no node added** — the reviewer's
  falsifiable check. `bootstrap/tests/test_presets.py` is **not** edited at all;
  its two banned-oracle nodes (lines 292 and 423) are left standing and are named
  as a residual (Chunk G) rather than quietly repaired inside a frozen file.
* **Collection identity**: `test_scaffold.py` carries no module-level marker
  (verified: 0 of its nodes appear in the manifest's `skip_xfail_marked` set), so
  these edits add no `SKIP-XFAIL-NEW` entry. They do add one `FROZEN-MODIFIED`.

### Chunk F — documentation

| # | File | Change |
|---|------|--------|
| F1 | `bootstrap/BOOTSTRAP.md` | Appendix B's **Schema rules** list (line 748) gains the grammar as a stated contract: the accepted line forms, the comment convention, the quoting rule for anything that could read as a number, date, time, boolean or null, and the refusal form `<path>:<line>: <reason>`. Stated as binding on **both** parser paths, which it now is. |
| F2 | `bootstrap/BOOTSTRAP.md` | The unknown-key rule, which Appendix B does not state today in any form: an unrecognized key **refuses**, and the profile schema is **closed** — adding a key is a breaking change for every engine shipped before it, which is why `schema` is reserved now. |
| F3 | `bootstrap/UPGRADE.md` | One sentence reconciling the two `dev/.cairn/` dispositions ([I6]). The rule at line 207 — *"readers must use `.get()` with a default and tolerate unknown keys"* — is right **for the lockfile**, which carries a `schema` field and can tell "a field I don't know" from "a file from the future". Say why the profile takes the opposite disposition, beside the rule, where a future contributor will hit it. |
| F4 | `CHANGELOG.md > Unreleased > Changed` *(and `Fixed`)* | One line for the closed grammar and the unknown-key refusal; one for the parser-divergence class the `--help` and `BOOTSTRAP.md` examples shipped. |

**Acceptance criteria — Chunk F**

* **Commands that decide it**: `python scripts/check_cairn.py` over the changed
  prose; `python scripts/claim_check.py <file>` **one file per invocation** (the
  checker exits 2 on more than one path, and parses `path.py:12,34` as a single
  path token, so one citation per line); `python scripts/quality_gate.py --sub
  neutrality`.
* **Every schema rule names something the reader can run.** The reviewer's check is
  to read Appendix B and, for each rule, name the command that would demonstrate
  it. A rule with no demonstration behind it is a finding — this is the failure
  shape the proposal's own [I1] committed, and F1 is the document where it would
  recur.
* **The two divergent example lines are not rewritten.** They become *correct*
  under Chunk B. If a Chunk F edit finds itself having to rewrite
  `bootstrap/BOOTSTRAP.md:734` or `bootstrap/_scaffold/cli.py:28` to make the
  sweep pass, the grammar is wrong and Chunk B reopens — that inversion is a
  design signal, not a doc chore.
* **`python bootstrap/scaffold.py --manifest` diff is empty.**

### Chunk G — residual homes

A residual whose only home is an accepted proposal is inert: accepted proposals
archive, and archived proposals are not read.

| # | File | Change |
|---|------|--------|
| G1 | `dev/PLANNING.md` | Row: **the correctly-spelled key with an unrecognized value** (`- not-a-real-module` accepted at exit 0). Trigger: the first adopter report of a mis-typed module name, or the next proposal touching `expand_preset`. |
| G2 | `dev/PLANNING.md` | Row: **the forward-compatibility cost of refusing is argued, not measured.** Trigger: the first genuine older-engine/newer-profile break. Remedy if it fires: a follow-up proposal reversing the disposition — **never a quiet loosening**. |
| G3 | `dev/PLANNING.md` | Row: **two live tests model the banned `_yaml_load`-as-oracle pattern** (`bootstrap/tests/test_presets.py:292` and `:423`), left standing because they sit in a frozen file and repairing them is not this plan's fence. Trigger: the next change that edits `test_presets.py` for any reason. Mechanical: `grep -n "_yaml_load" bootstrap/tests/test_presets.py`. |
| G4 | `dev/PLANNING.md` | Row: **the gate manifest's `SKIP-XFAIL-NEW` fires on ordinary new tests** in any module carrying a module-level `pytestmark` skipif — 34 nodes in `test_presets.py` are recorded as "marked" while the suite reports 0 skipped. Trigger: the next supervised ceremony, or the next plan that must add a node to a marked module. Mechanical: `python bootstrap/tests/_gate_manifest.py verify --anchor-ref <P>`. |
| G5 | `dev/PLANNING.md` | Row: **`_resolve_current_profile`'s lockfile fallback is now audible but still a fallback.** Whether substituting the lockfile profile is the right disposition at all is unexamined. Trigger: the next upgrade-path proposal. |
| G6 | `dev/PLANNING.md` | Row: **nothing mechanically enforces the suite's `0 skipped` invariant**, so a parity gate that skips itself away (D4 on a PyYAML-less host) costs both canaries and is visible only in the pytest summary line. Trigger: the first suite run reporting a non-zero skip count, or the next change to `bootstrap/tests/conftest.py`. Mechanical: the `skipped` figure in the pytest summary. |

**Acceptance criteria — Chunk G**

* Every residual named anywhere in this plan has a home that is **not** this plan
  and **not** the proposal, with a trigger a future reader will actually hit.
* `python scripts/claim_check.py dev/PLANNING.md` clean.

### Chunk M (Maintainer-only) — the batched AST baseline re-anchor

> **An implementing agent must not perform any step in this chunk.** The AST
> baseline is the engine's tamper-evidence: an implementing agent that re-pins the
> baseline over its own edit has blessed its own verifier. This is the
> `bootstrap/REANCHOR_RUNBOOK.md` *principle* — *"the implementer must not bless
> its own verifier"* — applied to the gate the runbook does **not** itself govern.
> Chunk M is the Maintainer's, in the shape `lockfile-provenance-fields` Chunk G
> established at `c3d5bd9`. The implementing agent's work **ends at Chunk G**.

**The batching, and the coordination it requires.** The Decision instructs:
*"**Batch it** with `fork-advisory-semantics` so that ceremony is paid once."*
The sibling proposal's *Coordination* section already prices the same hazard from
its side and the two records now agree. The concrete arrangement:

1. **`fork-advisory-semantics` lands its engine work first** — the proposal's
   own Maintainer decision point 3 recommendation, and the reason given is that
   it was already `revised` and had already priced its re-anchor, while this
   proposal was still absorbing specification findings.
2. **This plan's Chunks A–G land second**, on top of it.
3. **One Maintainer-run re-anchor absorbs both deltas.** The correction script is
   prepared by the implementing agent, **dry-run only**, and the dry run's
   predicted post-images are recorded in a commit body before the Maintainer runs
   anything with `--commit` — the `c3d5bd9` / `3cb85ca` shape.
4. **The two plans must not execute concurrently.** If they do, this plan's
   stop-the-line signal ("an unexplained engine-baseline delta") fires on the
   sibling's legitimate symbol motion, and the sibling's target (3 CHANGED) and
   this one's (2 CHANGED) become unattributable.

**The combined falsifiable target for the single ceremony** is the union of the
two plans' targets, re-derived against the post-sibling baseline immediately
before the handoff and **never** quoted from either proposal: this plan
contributes exactly `FunctionDef:_minimal_yaml_parse` and `FunctionDef:load_config`,
both in `bootstrap/_scaffold/config.py`. Any symbol outside the union is a
stop-and-explain.

**Verification after the ceremony** (the Maintainer's, and the only thing that
closes the red window):

```
python bootstrap/tests/_ast_attest.py verify \
    bootstrap/tests/fixtures/scaffold_ast_baseline.json bootstrap/_scaffold/*.py
python -m pytest bootstrap/tests/test_ast_attest.py
```

Expected: `AST attestation OK — <N> baselined symbol(s) accounted for, unchanged`,
0 CHANGED / MISSING / DUPLICATE, and the two previously-red nodes green.

**Also the Maintainer's, and deliberately not folded in**: the disposition of the
gate-manifest deltas (the pre-existing HOLD from `7066489`, plus this plan's one
`FROZEN-MODIFIED` on `test_scaffold.py`) at the next supervised gate ceremony.
That is a *different* ceremony with a different runbook, and this plan neither
performs nor schedules it.

## Acceptance criteria

Per-chunk criteria are above. These are the plan-level deliverables.

* **Tests that must pass.**
  * `python -m pytest bootstrap/tests` — the whole suite, **0 skipped / 0
    xfailed**, under the canonical interpreter (`~/conda_envs/lhm/bin/python`,
    Python 3.13.13). Baseline **1601 passed**, `as_of 2026-08-03`, re-measured for
    this plan. Collection grows by exactly the new nodes and drops none. The two
    `test_ast_attest.py` nodes are red between the first engine commit and Chunk
    M, per *Scope*, and green after.
  * `bootstrap/tests/test_profile_grammar.py` — the new module, carrying **every**
    new node, no module-level marker, driving `load_config` and the CLI through
    their public entry points.
  * `bootstrap/tests/test_scaffold.py` — the two inverted/completed nodes.
  * **Every test shown non-vacuous by mutation**: remove the control, confirm the
    test fails, restore the source byte-identical. The ledger goes in the commit
    body, per chunk. Adopted from `gate-reanchor-preflight` Chunk E and
    `release-authenticity` Chunk A.
* **Doc updates that must land.** All hand-authored: `bootstrap/BOOTSTRAP.md`
  (Appendix B schema rules + the unknown-key rule), `bootstrap/UPGRADE.md` (one
  sentence), the `bootstrap/_scaffold/config.py` comment at lines 46–49, and
  `CHANGELOG.md > Unreleased > Changed/Fixed`. No generated docs and no
  snippet-synced blocks are involved — but note that Chunk D makes the shipped
  `BOOTSTRAP.md` blocks and the `--help` text **executable by the suite**, which is
  a drift control of the same family reached from the other side.
* **Examples / smoke checks required.** `python bootstrap/scaffold.py --summary`
  and `--dry-run` on all three profiles under `bootstrap/profiles/`, once with
  PyYAML and once with it blocked, outputs required to match; two full installs of
  the `--help` example into empty targets, one per parser path, `diff -r` clean;
  `python bootstrap/scaffold.py --manifest` diffed before and after, expected
  **empty**, which is itself the assertion that this plan installs nothing new.
* **Inbound path-link updates.** None expected: `dev/PLANNING.md` and
  `dev/NEXT_SESSION.md` refer to plans by filename stem, not path link, so the
  archive-move needs no edit there. Confirm at archive time rather than assume.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants, each with the chunk that enforces it.**
  * *`load_config` either returns `yaml.safe_load`'s value or raises with a line
    number — no third outcome.* Part (b) is **structural** (the parse loop refuses
    any line matching no form) and enforced by B7; part (a) is **verified over a
    finite corpus** and enforced by B6 and D3–D5. The asymmetry is stated, not
    smoothed over.
  * *No content line is ever silently dropped.* B4 + B7. This is the invariant
    every recurring finding lived under — [I1]'s empty and indented profiles,
    [I4]'s truncation and folded-block rows.
  * *One acceptance contract on both parser paths.* Structural — the grammar's
    checks are textual and run before dispatch (B1) — pinned by B6/B7 run twice,
    once with PyYAML and once with it blocked (D5).
  * *No profile key is honoured or discarded without being named.* C3, pinned by
    C7's four measured typo rows.
  * *`RECOGNIZED_PROFILE_KEYS` stays derived.* C6, asserted against the three
    source definitions read independently.
  * *A parity gate can detect its own collapse.* D4's two canaries — the
    oracle-identity canary (`datetime.date`) and the divergence canary
    (`modules: [a, b]`).
  * *The engine never writes a profile it would refuse.* D3, calling both real
    writers across shapes including zero modules and an apostrophe-bearing token.
* **Public-path → test mapping.** `load_config` and `_minimal_yaml_parse` are
  exercised through `load_config` and through the real CLI (`--summary`,
  `--dry-run`, a full install), never by reaching past the public entry point.
  `unrecognized_profile_keys` is pure and is exercised both directly and through
  `load_config`. The existing homes are cited as relative links —
  [`../../bootstrap/tests/test_scaffold.py`](../../bootstrap/tests/test_scaffold.py) and
  [`../../bootstrap/tests/test_presets.py`](../../bootstrap/tests/test_presets.py) — and the new module is a
  code span registered under *Proposed paths*, because the template's link form
  assumes an existing file, which a plan that creates the file cannot satisfy; the
  link form is adopted at code review once the path resolves.
* **Failure modes — all closed.** Unparseable line → refuse. Document with no
  content lines → refuse. Unrecognized key → refuse. Unknown `schema` → refuse
  with the version message. Value that could read as a number, date, time, boolean
  or null → refuse with *"write it quoted"*. Backslash-bearing double-quoted value
  → refuse, pointing at the single-quoted form. The one deliberately **open** path
  is `_resolve_current_profile`'s lockfile fallback, which stays open by design
  and becomes **audible** in Chunk A; it is a residual (G5), not a closure.
* **Edge cases handled.** Empty profile `{}` (accepted by explicit rule);
  zero-byte, whitespace-only, comment-only and uniformly-indented documents
  (refused); `modules: []` (accepted, the documented explicit opt-out); bare
  `modules:` (`None`); a single leading `---` (accepted); a second document
  (refused); CRLF and lone-`\r` line endings (measured — no divergence class of
  their own); a `#` inside a quoted value and a `#` with no preceding whitespace
  (both preserved); `''` doubling in a single-quoted scalar (unescaped);
  apostrophe-bearing `project_name` and `test_command` through the real
  self-heal writer.
* **Known omissions, stated rather than implied.** (a) Part (a) of the invariant is
  sampled, not proved — a future reviewer may still find an accepted input that
  diverges, and the *Signals the change is wrong* row about the grammar accreting
  forms stays live. (b) The correctly-spelled-key/unrecognized-value class is
  untouched (G1). (c) The forward-compatibility cost of refusing is argued, not
  measured (G2). (d) Non-UTF-8 profiles remain out of scope —
  `read_text(encoding="utf-8")` already raises. (e) Symlinked profile paths and a
  writer racing `load_config` are not examined; no locking is involved on the read
  path, and neither was tested. (f) A control character inside a quoted value
  (a literal `\r` between quotes, which YAML treats as a line break) is not
  covered by the CRLF measurement. (g) The two banned-oracle tests in
  `test_presets.py` are left standing (G3). (h) No Python other than 3.13.13 has
  been used for any figure here; `ast.dump` structure and therefore the AST target
  are interpreter-minor sensitive.

## Verification

The concrete commands the implementation must pass.

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
Run under the canonical interpreter (`~/conda_envs/lhm/bin/python`, Python
3.13.13) with `PYTHONDONTWRITEBYTECODE=1`; a different Python minor silently
changes AST-attestation results and PyYAML-oracle behaviour alike.

* **The engine security lint** — `python -m pytest bootstrap/tests/test_security_lint.py`
  (the Bandit gate over `bootstrap/_scaffold/`) and
  `bootstrap/tests/test_security_leaf.py` (the pinned write-function set,
  unchanged). Both are real suite nodes; naming them is not a claim that
  something *else* runs them.
* **The Python floor** — the `vermin` check, declared floor 3.11. The new code
  must not raise it.
* **The AST attestation** — `python bootstrap/tests/_ast_attest.py verify
  bootstrap/tests/fixtures/scaffold_ast_baseline.json bootstrap/_scaffold/*.py`.
  Expected **2 CHANGED** before the Maintainer's re-anchor and **0 after**; a 3rd
  is a stop.
* **The install-contract assertion** — `python bootstrap/scaffold.py --manifest`,
  diffed against the pre-change output. **Expected empty.**
* **The dual-parser smoke** — the three shipped profiles run through `--summary`
  and `--dry-run` twice, PyYAML present and PyYAML blocked, outputs required to
  match.
* **The mutation ledgers** — per chunk, in the commit body: the deletion, the
  observed test failure, and the byte-identical restore.
* **Not a gate, and named so nobody mistakes it for one** —
  `python bootstrap/tests/_gate_manifest.py verify --anchor-ref <P>` is a
  **supervised command that no suite node invokes**. It already HOLDs on the tree
  today from a prior commit. This plan runs it to *record* its delta, not to pass
  it.

### Gate-manifest delta — measured with collection

**The flag that cannot support the claim, named first.** An earlier
implementation report banked *"exactly 1 FROZEN-MODIFIED + 1 FROZEN-NEW, and 0
SKIP-XFAIL-NEW"* from `_gate_manifest.py verify --no-collect`. That flag prints
`COLLECTION: skipped (static-only verification, --no-collect)` and
**structurally cannot report** `COLLECTION-DROPPED`, `COLLECTION-ADDED` or
`SKIP-XFAIL-NEW` — the three classes the verifier derives from a pytest
collection it did not run. A `0 SKIP-XFAIL-NEW` read off a `--no-collect` run is
not a measurement of zero; it is the absence of a measurement. Everything below
was re-run **with** collection.

**How the attribution was established** (`as_of 2026-08-04`, canonical
interpreter Python 3.13.13, `PYTHONDONTWRITEBYTECODE=1`, working tree at HEAD
`da2d00e` carrying both Wave 2 plans' uncommitted work):

* **working tree** — `python bootstrap/tests/_gate_manifest.py verify
  --anchor-ref e45e1fc` → **HOLD — 17**.
* **pre-existing floor** — the same command against a pristine `git archive
  HEAD` tree (`--target-repo <archive> --trusted-repo <this repo>`) → **HOLD —
  12**. Neither plan is responsible for any of those 12.
* The delta is therefore **5 HOLD entries**, set-differenced rather than eyeballed.

**The three classes, separated.**

| entry | class | whose |
|---|---|---|
| `FROZEN-MODIFIED: bootstrap/tests/test_scaffold.py` | frozen edit | **this plan** (Chunk E) |
| `COLLECTION-DROPPED: bootstrap/tests/test_scaffold.py::TestMinimalYamlParse::test_mixed_indent_list` | collection | **this plan** (Chunk E1) |
| `FROZEN-MODIFIED: bootstrap/tests/test_lockfile_module.py` | frozen edit | `fork-advisory-semantics` |
| `FROZEN-MODIFIED: bootstrap/tests/test_verify_integrity.py` | frozen edit | `fork-advisory-semantics` |
| `FROZEN-MODIFIED: bootstrap/verify_integrity.py` | frozen edit | `fork-advisory-semantics` |

**`SKIP-XFAIL-NEW` attributable to this plan: 0** — and that is now a
*measurement*. All four entries (three in
`bootstrap/tests/test_quality_gate_redundancy.py`, one in
`bootstrap/tests/test_security_check.py`) are present at the HEAD floor and
predate both plans. The new module's design goal held: it carries no
module-level marker, so none of its nodes registers as marked.

**Notes, not HOLDs** — recorded because the ceremony re-pins from them:
`FROZEN-NEW` for `bootstrap/tests/test_profile_grammar.py` (this plan) and for
`bootstrap/tests/test_fork_advisory.py` (the sibling), against two already at
the floor; `COLLECTION-ADDED` × **44** for the new module plus × 1 for the
renamed `test_scaffold.py` node (this plan) and × 36 for the sibling;
`CASCADE-CHANGED: bootstrap/_scaffold/config.py`, which the verifier does not
HOLD on by design because the AST attestation governs it. The `ANCHOR` note
records that `e45e1fc` resolved from the *target* repo, so this is not an
externally anchored verification.

**One deviation from this plan's own Chunk E criterion, recorded rather than
smoothed.** Chunk E's acceptance criteria promise the reviewer that
`bootstrap/tests/test_scaffold.py` shows *"only these two nodes changed and no
node added"*, and predict *"one `FROZEN-MODIFIED`"* with no collection entry.
The implementation **renamed** `test_mixed_indent_list` to
`test_mixed_indent_list_is_refused` so the node name states what it now
asserts. A rename is a drop plus an add in collection identity, so the delta is
one entry larger than the plan predicted. The rename is defensible and is kept;
the prediction it falsifies is the plan's, and the Maintainer re-pins from this
table, not from that criterion.

### The Unicode-whitespace repair (defect found by running the artifact)

Part (a) of the invariant had a hole in exactly the class Amendment 2 was
written to close. Python's no-argument `str.strip()` removes every
`str.isspace()` character; **YAML's whitespace is only SPACE and TAB**. An
NBSP-prefixed key was read as `project_name` by the recognizer and as
`'\xa0project_name'` by PyYAML — Amendment 2's own *different key* sentence,
reached by a character ordinary copy-paste out of a rendered page produces.
`_PROFILE_CONTROL_RE` did not (and deliberately still does not) enumerate that
range.

The tokenizer now strips exactly `" "` in all three places (`line.strip(" ")`,
`raw.lstrip(" ")`, `value.rstrip(" ")`) and `_PROFILE_UNICODE_SPACE_RE` names
the codepoint in the refusal. **The two are separate controls and the tests keep
them separate**, because the diagnostic runs *first*: while it is in place a
loosened tokenizer is invisible, and an enumeration is exactly what a future
Unicode revision outdates.
`TestInvisibleWhitespaceIsNotConsumed::test_the_invariant_holds_without_the_diagnostic`
therefore disables the enumeration and re-asserts the contract against the
tokenizer alone.

**There is a third control, and an earlier revision of this section did not
name it.** The 29 `str.isspace()` codepoints (CPython 3.13.13) do not form one
class against the oracle — measured by probing `yaml.safe_load` once per
codepoint, `as_of 2026-08-04`: 2 are YAML's own whitespace (SPACE, TAB), **16
are ordinary text** the oracle preserves inside a scalar (NBSP, OGHAM SPACE
MARK, the `U+2000`–`U+200A` family, `U+202F`, `U+205F`, `U+3000` — this subset
*is* the hazard), **5 are YAML line breaks** (`U+000A`, `U+000D`, `U+0085`,
`U+2028`, `U+2029`, where `str.splitlines()` and PyYAML agree so no *different
key* is reachable), and **6 the oracle refuses outright** as non-printable
(`ReaderError`: `U+000B`, `U+000C`, `U+001C`–`U+001F`). The tokenizer holds
nothing on that last 6; **`_PROFILE_CONTROL_RE` does**. That is what M7 below
measures, and it is why the shipped-configuration sweep
(`..._refuses_or_equals_the_oracle`) has a falsifier at all.

**Mutation ledger** — every row applied to `bootstrap/_scaffold/config.py`,
`__pycache__` purged, the whole module run on CPython 3.13.13, and `config.py`
restored byte-identically (sha256 `8089586e…` verified after each restore).
**Re-measured end-to-end `as_of 2026-08-04`**; the M7 row is new, and the
bytecode purge is the correction described in the *stale-`.pyc`* note below.

| # | perturbation | result |
|---|---|---|
| M1 | `line.strip(" ")` → `line.strip()` | **2 red** — `..._holds_without_the_diagnostic`, `..._never_eaten_from_a_value` |
| M2 | `value.rstrip(" ")` → `value.rstrip()` | **2 red** — same two nodes |
| M3 | delete the `_PROFILE_UNICODE_SPACE_RE` scan | **1 red** — `..._names_the_codepoint` (both sweeps stay green: the contract holds, only the message degrades) |
| M4 | delete the `_PROFILE_RESOLVER_TOKENS` branch | **1 red** — `..._refuse_where_the_oracle_refuses` |
| M5 | `raw.lstrip(" ")` → `raw.lstrip()` | **1 red** — `..._holds_without_the_diagnostic` |
| M6 | `indent = … line.lstrip(" ")` → `line.lstrip()` | **0 red — and no test was written to force one** (below) |
| M7 | delete the `_PROFILE_CONTROL_RE` scan | **5 red** — `..._refuses_or_equals_the_oracle`, `..._holds_without_the_diagnostic`, plus 3 in `TestGrammarTotality` |

**Four things the ledger taught that the plan should not lose.**

1. **A first draft of these nodes was vacuous, and only the perturbation showed
   it.** Written against the shipped module they passed under M1 *and* M2 —
   the diagnostic masked both. The nodes were rebuilt around the
   diagnostic-disabled sweep. The plan's *"a test whose deletion-mutant stays
   green is not accepted"* rule caught this only because the mutant was
   actually run.
2. **One node is subsumed by construction, and that is now written into it
   rather than left for a reader to discover.** A second audit flagged
   `test_every_isspace_codepoint_refuses_or_equals_the_oracle` as unfalsifiable
   under every ledger mutation. Re-derived: the audit's mutation set was the
   incomplete thing — M7 (new above) *does* turn it red. But the deeper
   property is stronger than the audit claimed, and it is structural, not a
   gap in the ledger. That node runs the same corpus as
   `..._holds_without_the_diagnostic`, which runs it with one refusal path
   removed; a refusal is contract-legal, so removing one can only **add** third
   outcomes. Its falsifier set is therefore a strict **subset** of the
   diagnostic-off node's, and **no mutation can ever turn it red alone**. It is
   kept — it is the only node stating the guarantee for the configuration
   adopters actually run, with no monkeypatch — and its docstring now says it
   guards no control on its own. Each of the three controls has its own
   single-control falsifier: the tokenizer → `..._holds_without_the_diagnostic`
   (M1, M2, M5 each turn it red singly); the diagnostic →
   `..._names_the_codepoint` (M3); `_PROFILE_CONTROL_RE` →
   `..._refuses_or_equals_the_oracle` (M7).
3. **M6 is a genuine no-op, not a coverage gap**, and it is recorded as such
   rather than given a manufactured test. Re-verified `as_of 2026-08-04` by
   applying M6 and re-running the whole breadth harness below: **67,637 inputs,
   0 third outcomes** — the mutant is indistinguishable from the shipped module
   on every corpus this plan has. The mechanism: with the invisible character
   still in `stripped`, the key and list patterns fail before the indent value
   is consulted. M5 by contrast *looked* like a no-op under the first corpus and
   was not — the corpus was missing `project_name: <space><NBSP>X`, the only
   shape that reaches the value-side tokenizer, because `_PROFILE_KEY_RE`
   requires a real SPACE after the `:`. That row (`value-prefix-spaced`) and its
   list twin are now in `_INVISIBLE_POSITIONS` with the reason written beside
   them.
4. **A stale `__pycache__` is how this section shipped figures that did not
   reproduce**, and the fix is procedural, not a one-off correction. M1, M2 and
   M5 each delete the same 3 source bytes (`" "`), so the mutants are
   byte-identical in length; CPython validates a cached `.pyc` on
   (mtime-seconds, size), so a second mutant written inside the same second is
   silently executed as the *first* mutant's bytecode. Re-running the M1/M2/M5
   counts without purging reproduces the failure exactly — all three report the
   same number. **Every mutation figure in this section was re-measured with
   `__pycache__` removed before each run**, and any future re-anchor must do the
   same. This is the mechanical root cause behind two rounds of bad figures, and
   it is worth more than the corrected numbers.

**The related resolver finding, fixed rather than dispositioned.** `k: =`,
`k: <<` and `k: ? x` were accepted as plain strings while `yaml.safe_load`
raises (`ConstructorError` / `ScannerError`) — the same third-outcome shape from
the other side, the plain-scalar rule not modelling PyYAML's *implicit
resolvers*. `_PROFILE_RESOLVER_TOKENS` refuses the three whole tokens;
`TestImplicitResolverTokens` pins both directions, because the lookalikes
`==`, `=x`, `<<x`, `?x` are ordinary scalars to PyYAML and refusing them would
be over-refusal.

**Breadth check** (a check, not a proof — part (a) remains finite-corpus).
`_minimal_yaml_parse` vs `yaml.safe_load`, CPython 3.13.13, **re-run `as_of
2026-08-04`**:

| corpus | inputs | third outcomes |
|---|---|---|
| Unicode whitespace — the module's own `_invisible_corpus()`, 29 `str.isspace()` codepoints × 13 positions | **377** | 0 |
| structured grammar shapes — `itertools.product` over 7 keys × 6 separator forms (4 distinct) × 29 value forms × 5 tails × 6 leads = 36,540, plus 16 list items × 5 indents × 3 tails × 3 shapes = 720 | **37,260** | 0 |
| random-character inputs — 1–40 chars drawn from a 50-entry alphabet (49 distinct: grammar punctuation, ASCII, TAB/CR, NBSP, IDEOGRAPHIC SPACE, `U+000B`, `U+001F`, BOM), `random.Random(20260804)` | **30,000** | 0 |
| **total** | **67,637** | **0** |

**The whitespace figure is the one the earlier revision got wrong**, and the
correction is arithmetic: it read **319** = 29 × 11, the position table as it
stood *before* this same section added `value-prefix-spaced` and
`list-value-spaced`. The shipped table has 13 positions, so the corpus is
29 × 13 = **377**. The grammar and random figures are **not** corrections of
the earlier 6,253 / 30,000 — that harness was not retained, so those numbers
could be neither reproduced nor refuted. The table above is a fresh
measurement from a harness described in the row itself; a re-anchor should
re-run it rather than carry the figure forward.

### The AST transaction, re-derived (Maintainer amendment, Chunk M input)

The amendment instructs: *"Re-measure against the committed baseline; do not
carry the old figure forward"*, because Amendment 1 removed a runtime branch
from `config.py`. Measured `as_of 2026-08-04` on the combined working tree
(`python bootstrap/tests/_ast_attest.py verify
bootstrap/tests/fixtures/scaffold_ast_baseline.json bootstrap/_scaffold/*.py`):
**6 non-pure-motion symbols, 0 DUPLICATE**, split cleanly by plan.

| symbol | module | whose |
|---|---|---|
| `CHANGED FunctionDef:_minimal_yaml_parse` | `bootstrap/_scaffold/config.py` | **this plan** |
| `CHANGED FunctionDef:load_config` | `bootstrap/_scaffold/config.py` | **this plan** |
| `MISSING Try` | (was `bootstrap/_scaffold/config.py`) | **this plan** |
| `CHANGED FunctionDef:cmd_upgrade` | `bootstrap/_scaffold/upgrade.py` | `fork-advisory-semantics` |
| `CHANGED FunctionDef:forked_facade_findings` | `bootstrap/_scaffold/lockfile.py` | `fork-advisory-semantics` |
| `CHANGED FunctionDef:format_forked_facade_warning` | `bootstrap/_scaffold/lockfile.py` | `fork-advisory-semantics` |

**The `MISSING Try` is this plan's third entry and the earlier target did not
predict it.** *Gate accounting* (i) recorded *"exactly 2 CHANGED … 0 MISSING, 0
DUPLICATE"*, written before Amendment 1 folded in. The baselined `Try` at span
`[86, 96]` is the `try: import yaml as _yaml / except ImportError` block that
Amendment 1 deleted — so it is the amendment's own predicted consequence, not an
unexplained baseline delta, and it does **not** trip the stop-the-line rule. The
union the single ceremony must absorb is therefore **5 CHANGED + 1 MISSING + 0
DUPLICATE**; anything outside this table is a stop-and-explain.

**Two collision checks, run because the baseline is keyed by bare symbol name.**
None of this plan's new top-level names (`ProfileGrammarError`,
`RECOGNIZED_PROFILE_KEYS`, `unrecognized_profile_keys`, `_ENGINE_PROFILE_SCHEMA`
and the six `_PROFILE_*` constants) matches any of the 174 baselined keys, and
the verifier reports **0 DUPLICATE** — so the `_yaml_sq` / `_yaml_dq` near-miss
*Gate accounting* flagged did not materialise.

**Install contract and dual-parser smoke, re-run on the final tree.**
`python bootstrap/scaffold.py --manifest` diffed against the same command run in
a pristine `git archive HEAD` tree — **empty**. All three profiles under
`bootstrap/profiles/` through `--summary` twice, once normally and once under a
`sys.modules['yaml'] = None` driver — **identical stdout/stderr and identical
exit code on all three**.

**Suite, `as_of 2026-08-04`, canonical interpreter (Python 3.13.13):**
`python -m pytest bootstrap/tests` → **1788 passed, 2 failed, 0 skipped, 0
xfailed**, 187s. The two failures are exactly the two `test_ast_attest.py`
nodes *Scope* prices as the deliberate red window
(`test_committed_baseline_accounted_for_across_the_engine_package`,
`test_ast_gate_passes_over_the_full_scaffold_module_set`) — the ones the
Maintainer's Chunk M closes. Nothing else is red. The figure covers both Wave 2
plans' work; this plan's own module contributes **44** nodes. `test_python_floor.py`
(the `vermin` floor assertion, declared floor 3.11) is among the passing nodes,
so the new code did not raise the floor.

**The adopter prose was brought into line with what is established.**
`bootstrap/BOOTSTRAP.md` Appendix B shipped the contract as *"there is no third
outcome"* flat, while this plan records part (a) as *verified over a finite
corpus, not proved*. Appendix B now says which half is which: totality is
structural, equality is checked against PyYAML over a corpus. Appendix B also
gained the invisible-space rule and the resolver-token clause, both of which the
code enforces and the adopter can hit.

**Note on doc gates**: drift gates (broken references, stale renders,
snippets that diverged from their source) catch **drift**, not
**absence** of new doc updates. Confirm each doc named in Acceptance
was actually updated; the gates don't enforce that.

## Plan review — the brief, and why the tier is not discharged

*Required — External, security lens. Implementation does not start until a review
has landed under this heading.* The tier is carried from the proposal header. The
proposal's own External round (Gemini Flash) saw neither the closed grammar nor
the flip to fail-closed on unknown keys — both arrived in revisions after it —
and its own *Not Covered* section says so.

> **The landed review appends here as a `### Plan review -- <reviewer> --
> YYYY-MM-DD` sub-heading** (plus a `### Sharpening` sub-heading if it raised
> findings). **Do not rename this heading to a bare `## Plan review`.** The
> lifecycle checker matches a section *kind*, not a review, so a bare heading with
> nothing under it would report the gate satisfied.

**Why the tier is right independent of the mandate.** Every review round on this
proposal found one more divergence class and the horizon receded by exactly one
step: twelve at External, seven more plus a thirteenth at Internal. Both of those
passes were run by, or checked against, the same agent type as the author. The
Internal reviewer said it plainly: *"Whatever blind spot produced the
overstatements in [I1] and [I3] is a blind spot I share by construction."*

**Mandates for the reviewer** — offered so the pass has a target rather than a
lens.

1. **Attack part (b) of the invariant — totality — first.** The claim is
   structural: *no content line is ever silently dropped, by construction.* The
   last time this proposal claimed a structural property ("A4 extends an existing
   fail-closed posture"), the property was unreachable on the path the proposal
   itself calls normal. Find a line the grammar accepts into neither a value nor a
   refusal. This mandate also carries the brief of the Internal re-review the
   author recommended and the Decision did not name (see *What the Decision
   settled*).
2. **Channel discipline over every verification step.** For each step in Chunks A
   through E, name the channel each input arrives by and show it is not the thing
   being verified. The specific instance this scope has already committed once:
   the first revision verified the init-lock writer against a *synthesized*
   template rather than by calling the writer, and the claim was false of the
   writer.
3. **Attack the canaries, not the tests.** Is the oracle-identity canary
   (`datetime.date`) actually unforgeable by a stdlib recognizer? Is the
   divergence canary still divergent after the grammar lands, or does it go stale?
   A parity gate that cannot detect its own collapse is not a gate, and this plan
   makes that claim in two places.
4. **Price the refusal against a real adopter, not against Cairn's own corpus.**
   The measured availability cost is zero — on files Cairn controls. Write a
   profile a scientist would plausibly write (a `test_command` with a `#`, a lab
   name with an apostrophe, a Windows editor's line endings, a copy-paste that
   picked up leading whitespace) and check the grammar's disposition on each.
   A refusal on any of them means the grammar is too tight.
5. **The `schema` key: does it do anything?** It is reserved so a *future* refusal
   can be diagnosable. Confirm Chunk C4's ordering actually delivers that, and say
   plainly whether reserving one key was worth the entry given that it rescues no
   engine already released.

**The stopping rule.** A finding on this scope is one of two things. Either it
names an input the grammar mis-handles — then it is a bug against a stated form
and the fix is bounded. Or it names a *shape* of input the grammar's forms do not
contemplate — then the specification was incomplete, and the correct response is
to widen a form or add a refusal, **never** to restore best-effort reading. The
second branch is the expensive one and is supposed to be.

**What the reviewer should not spend attention on.** The direction — fail-closed
on the input boundary, refuse rather than warn on unknown keys, a grammar rather
than a catalogue — survived an External round, an Internal round, and a Decision,
and is not reopened by this plan.

## Code review — the brief (no review has landed)

*Filled in after implementation commits land.* Per `doctrine/plans.md`, the
reviewer is **not** the implementing agent, the section is append-only, and a
clean final review carries a falsification ledger and a coverage line. The landed
review appends here as a `### Code review -- <reviewer> -- YYYY-MM-DD`
sub-heading; the heading above is shaped the same way as the plan-review one and
for the same reason.

Three checks this plan asks its code reviewer to **run** rather than read:

* **Re-run the uniformly-indented profile** against the landed code on a
  genuinely stdlib-only interpreter, and confirm it refuses. That is the largest
  fail-open in the record and the one the change as originally specified would
  have left open.
* **Re-run one mutation from each chunk's ledger**, chosen by the reviewer, not by
  the implementer.
* **Read `bootstrap/BOOTSTRAP.md`'s new Schema rules end to end and name the
  command behind each rule.** A rule with no command behind it is the exact defect
  class this proposal exists to close, recurring inside its own remedy.

## Lasting-truth migration

*Filled in at archive time.* Per `doctrine/plans.md`, the archive commit body
carries the literal `Follow-ups migrated to:` block naming where each deferred
item went, so the migration is auditable from the commit log alone — and the plan
does not archive until every deferred follow-up has a durable home outside it.

The homes are pre-declared here so archive time is bookkeeping rather than
recall: the unrecognized-*value* class, the argued-not-measured
forward-compatibility cost, the two banned-oracle tests in `test_presets.py`, the
gate manifest's `SKIP-XFAIL-NEW` over-report, and the lockfile-fallback
disposition all → `dev/PLANNING.md` rows (Chunk G1–G5). The CRLF gap → closed by
measurement and pinned by test B9, so it expires rather than migrating. The
`--help` and `BOOTSTRAP.md` divergence → closed by the grammar and held by the
Chunk D sweep, which is the durable home the 2026-07-11 prose remedy lacked.

**Added 2026-08-03, in the author's Response to the External plan review** (an
addition to the pre-declaration, not a rewrite of it): the **unenforced `0
skipped` invariant** — a parity gate that skips itself away takes both canaries
with it, and no node, hook or CI job notices — → a `dev/PLANNING.md` row, Chunk
G6. The pre-declared range above therefore reads G1–G6.

**Two items that are not residuals and must not be archived away as if they
were:** the unresolved reading of Maintainer decision point 4 (whether a focused
Internal round was meant to precede plan-open), which is the Maintainer's to
confirm or strike; and the batched AST re-anchor, which is Chunk M and belongs to
the Maintainer whether or not this plan is otherwise complete. A plan that
archives with Chunk M unperformed leaves the canonical suite red.

Per the [Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home outside the
plan.

This section is append-only once written.

## Plan review -- Gemini Flash (External, security lens) -- 2026-08-03

**Steelman.** This plan provides a robust, closed line-grammar specification (L1–L8) for Cairn's zero-dependency profile parser (`_minimal_yaml_parse`). It replaces a fragile best-effort parser with a strict recognizer that either yields an exact match to PyYAML's `yaml.safe_load` or refuses fail-closed with clear error messages and formatting rewrites. Furthermore, Chunk C's refusal on unrecognized profile keys closes the silent key-dropping defect completely.

### Concerns

* **[E1] Oracle independence in parity tests (banned-oracle avoidance).**
  Chunk B correctly forbids using `_yaml_load` as its own oracle in tests (which would reduce to comparing a function against itself when PyYAML is missing). The plan's canary test (`isinstance(yaml.safe_load("d: 2024-01-01")["d"], datetime.date)`) is a vital tripwire ensuring that PyYAML is genuinely loaded as the independent oracle during test execution.
* **[E2] Coordinated AST re-anchor with `fork-advisory-semantics`.**
  Chunk M is Maintainer-only and batched with `fork-advisory-semantics`. The plan correctly accounts for exactly 2 CHANGED symbols in `bootstrap/_scaffold/config.py` (`FunctionDef:_minimal_yaml_parse` and `FunctionDef:load_config`).

### Covered

* **Grammar & refusal specification audit**:
  Verified that the L1–L8 grammar, plain-scalar admissibility rules, comment conventions, reserved `schema` key handling, and derived key whitelist (`RECOGNIZED_PROFILE_KEYS`) fully satisfy the single acceptance contract across both PyYAML and fallback execution paths.

### Not covered / low confidence

* Unrecognized profile *values* (e.g. valid syntax specifying a non-existent module name) are explicitly out of scope for this plan and rely on downstream module validation.

### Recommendation

**READY FOR IMPLEMENTATION.** The plan's closed line grammar, strict refusal mechanics, documentation drift gate (Chunk D), and Maintainer re-anchor boundaries (Chunk M) are verified and sound.

## Response to plan review -- Claude (author) -- 2026-08-03

**Model**: Claude Opus 5

**Both findings accepted; five edits across four sections.** The verdict is
READY FOR IMPLEMENTATION and both findings are phrased as affirmations of the
plan's own design. Neither is therefore informational: Cairn's lifecycle has no
severity floor below which a finding stops needing a disposition, and an
affirmation is a claim that has to be *checked* before it is banked. I checked
both against the code and the tooling rather than against the plan's own prose,
and each check held on its stated subject and turned up one adjacent condition
under which the plan's surrounding text was wrong. That is what the amendments
carry. The same rule applies to the review's other two claims, so both are
dispositioned below rather than inherited: the *Covered* item — the reviewer's
answer to mandate 1 — is **banked unverified** with the reason stated, and the
*Not covered* note is corrected on its second clause. Everything measured below was run this session at working-tree HEAD under
the canonical interpreter (`/Users/kendal30/conda_envs/lhm/bin/python3.13`,
Python 3.13.13, PyYAML 6.0.3, `PYTHONDONTWRITEBYTECODE=1`).

* **[E1] accept.** The finding: Chunk B correctly bans `_yaml_load` as its own
  oracle (it reduces to comparing the function under test to itself when PyYAML
  is absent), and the oracle-identity canary
  `isinstance(yaml.safe_load("d: 2024-01-01")["d"], datetime.date)` is the
  tripwire proving PyYAML is genuinely the independent oracle at test time.

  **Verified, on both halves.** The ban's premise is real:
  `bootstrap/_scaffold/config.py:40`–43 defines, in the `except ImportError`
  arm, `def _yaml_load(text): return _minimal_yaml_parse(text)` — so
  `_yaml_load` *is* the function under test on the path Cairn's zero-dependency
  promise makes normal. The two live models of the banned pattern are where the
  plan says they are:
  [`../../bootstrap/tests/test_presets.py`](../../bootstrap/tests/test_presets.py) line 292
  (`test_flat_schema_parses_identically`, whose body is
  `_yaml_load(self._PROFILE)` compared with `_minimal_yaml_parse(self._PROFILE)`)
  and line 423 (`assert _roster(_yaml_load(yaml_text)) == _roster(_minimal_yaml_parse(yaml_text))`
  inside `test_literal_recipe_yaml_also_parses_via_pyyaml`). The canary measures
  as claimed: `yaml.safe_load("d: 2024-01-01")["d"]` is `datetime.date(2024, 1, 1)`,
  `isinstance(..., datetime.date)` **True**; the fallback on the same text
  returns `{'d': '2024-01-01'}`, a `str`, **False**. The plan's stated
  perturbation runs and fails as advertised: with `sys.modules['yaml'] = None`
  set before import, `config._yaml is None` is `True` and the oracle routed
  through `_yaml_load` yields `'2024-01-01'` → the canary is False. So the
  tripwire is sound **when it executes**.

  **What checking it turned up.** The reviewer's phrase is "during test
  execution", and that is exactly the condition the plan cannot currently
  guarantee. The canary rides on D4, and D4 hard-skips from inside its own body
  when `import yaml` fails. Chunk D's acceptance criteria answered that with
  *"If it ever does, the suite's `0 skipped` invariant fails loudly."* **That
  sentence was false.** Verified: `bootstrap/tests/conftest.py` carries only the
  order-independence shuffle hook — no `pytest_sessionfinish`, no terminal
  reporter, no skip accounting — and the repository has no workflow directory at
  all (`.github/` holds `ISSUE_TEMPLATE`, `PULL_REQUEST_TEMPLATE`, `labels.yml`
  and nothing else). A grep for skip-count enforcement across `bootstrap/`,
  `scripts/` and `.github/` returns only unrelated uses of the word. So on a
  PyYAML-less host D4 skips, the parity sweep **and both canaries** go with it,
  and `python -m pytest bootstrap/tests` still exits 0. A canary that can be
  skipped away without a sound is the gate collapse it exists to detect, one
  level up — the same failure shape the plan names, displaced from the oracle to
  the node hosting it.

  **Plan change.** Three edits, all minimal. (i) *Chunk D, row D4* — the skip
  message must **name its own consequence** (*"PyYAML absent: the parity sweep
  and both canaries did not run"*), so the pytest summary line carries the loss
  in words rather than as a count a reader has to interpret. (ii) *Chunk D
  acceptance criteria* — the `0 skipped` bullet is corrected in place: the
  "fails loudly" claim is retracted, the verification that retracts it is
  recorded, and the bullet now states plainly that D4's skip is visible only in
  the summary line. (iii) *Chunk G* — a new **G6** residual row for the
  unenforced `0 skipped` invariant, with a trigger (the first non-zero skip
  count, or the next change to `bootstrap/tests/conftest.py`). Making the
  invariant mechanical is deliberately **not** folded in: it means a conftest
  hook or a CI job, neither of which is in this plan's fence, and the conftest is
  a shared surface. The *Lasting-truth migration* pre-declaration gains an
  appended sentence so its range reads G1–G6.

* **[E2] accept.** The finding: Chunk M is Maintainer-only and batched with
  `fork-advisory-semantics`, and the plan correctly accounts for exactly 2
  CHANGED symbols in `bootstrap/_scaffold/config.py`
  (`FunctionDef:_minimal_yaml_parse` and `FunctionDef:load_config`).

  **Verified against the committed baseline, not against the plan.**
  `bootstrap/tests/fixtures/scaffold_ast_baseline.json` holds **174** entries;
  `FunctionDef:_minimal_yaml_parse` carries digest `752c30f3f1220eda` and
  `FunctionDef:load_config` carries `18c69e0ea95a7a7e` — byte-for-byte the two
  digests the plan quotes. Running
  `python bootstrap/tests/_ast_attest.py verify bootstrap/tests/fixtures/scaffold_ast_baseline.json bootstrap/_scaffold/*.py`
  at HEAD reports `AST attestation OK — 174 baselined symbol(s) accounted for,
  unchanged`. The three supporting claims hold too: `FunctionDef:_list_item_text`
  is **absent** from the baseline (nested, so retiring it drops nothing);
  `FunctionDef:_resolve_current_profile` is **absent** and is emitted today as
  `note: NEW FunctionDef:_resolve_current_profile (bootstrap/_scaffold/upgrade.py)`,
  exactly as the plan states; and `_classify` `continue`s past every `Import` /
  `ImportFrom` / `Docstring` key, so the `cli.py` docstring edit and any import
  rotation are notes. Disjointness with the sibling holds by inspection of both
  records: `fork-advisory-semantics` contributes `FunctionDef:forked_facade_findings`,
  `FunctionDef:format_forked_facade_warning` and `FunctionDef:cmd_upgrade`, none
  of which this plan touches, and this plan's `upgrade.py` edit lands on a
  non-baselined symbol.

  **What checking it turned up.** The target's *other* half — `0 MISSING, 0
  DUPLICATE` — is stated without a mechanism, and there is a real one this plan
  can trip. The baseline is keyed by **bare symbol name**: its entries carry
  `digest` / `span` / `type` and **no module field**, so `FunctionDef:load_config`
  is a package-global key. `_classify` reports `DUPLICATE` for any *baselined*
  key found in two files, and `DUPLICATE` is a problem line — `rc 1`, `AST
  attestation FAILED` — not a NEW note. A plan that only *adds* symbols can
  therefore still fail the attestation, by naming a new `config.py` helper after
  a symbol already baselined in a different engine module. This is not
  hypothetical for this scope: `_yaml_sq` lives at
  `bootstrap/_scaffold/upgrade.py:2039` and `_yaml_dq` at
  `bootstrap/_scaffold/install.py:636` — precisely the names Chunk B's
  single-quoted (`''`→`'`) and double-quoted scalar handling reach for.
  Demonstrated: appending a `def _yaml_sq` to a scratch copy of `config.py` and
  re-running verify prints
  `DUPLICATE FunctionDef:_yaml_sq  (defined in 2 files: … — single-source broken)`
  and `AST attestation FAILED`. The danger is not the failure, it is the
  *misreading*: the plan's stop rule is written about a **3rd CHANGED symbol**,
  so an implementer meeting a `DUPLICATE` would escalate a naming collision as
  engine tamper-evidence — and the batched ceremony is exactly where an
  unexplained baseline delta is most expensive to misattribute.

  **Plan change.** One edit: *Gate accounting* item (i), the falsifiable
  pre-re-anchor target, gains a bullet stating the mechanism (bare-name keying,
  `DUPLICATE` on baselined keys is a hard failure), naming the two concrete
  near-miss helpers with their homes, recording the demonstration, and setting
  the disposition — **every new Chunk B / Chunk C top-level name is checked
  against the 161 baselined `FunctionDef:` / `Assign:` / `ClassDef:` keys before
  its commit, and a `DUPLICATE` on a name this plan's Chunk B or Chunk C
  introduces is a rename, not a stop-and-explain; every other `DUPLICATE` stays
  in the stop-and-explain class.** The scope clause is load-bearing in both
  directions, and it is the whole content of the edit: the pre-commit check is
  what makes a collision on one of *this plan's* names the case that should not
  reach the ceremony, so a `DUPLICATE` that surfaces there anyway is not one of
  them and is precisely the unexplained delta the stop rule exists for. Nothing
  here relaxes item (i)'s *"A 3rd CHANGED symbol is a stop-and-explain"* or
  Chunk M's *"Any symbol outside the union is a stop-and-explain"*; a
  disposition that removed a hard-failure class from the engine
  tamper-evidence surface would be a contract change, and this finding did not
  ask for one. Chunk M itself is unchanged: it stays the Maintainer's, and
  nothing here moves work across that fence.

**On the reviewer's *Covered* item — banked unverified, and recorded as such.**
The item reads: the L1–L8 grammar, the plain-scalar admissibility rules, the
comment conventions, the reserved `schema` handling and `RECOGNIZED_PROFILE_KEYS`
"fully satisfy the single acceptance contract across both PyYAML and fallback
execution paths." That is the reviewer's answer to **mandate 1** — part (b),
totality — which the brief above calls the expensive branch and the reason this
tier exists at all. By the rule this Response opens with, an affirmation is a
claim that has to be checked before it is banked, and this one has to be
dispositioned rather than quietly inherited.

**What I could check: the channel, and it does not hold.** The claim is asserted
"across both PyYAML and fallback execution paths", which is an execution-path
claim, and there is no artifact to execute. Verified this session: a
whole-repository grep for `RECOGNIZED_PROFILE_KEYS` (excluding `.git`) returns
exactly two files — this plan and
[`../proposals/archive/2026-08-03-claude-profile-parse-fail-open.md`](../proposals/archive/2026-08-03-claude-profile-parse-fail-open.md)
— both prose, no code; and `bootstrap/_scaffold/config.py` still carries the
best-effort parser this plan replaces, nested `_list_item_text` and all. So
neither the whitelist nor the L1–L8 recognizer exists on *either* path yet, and
whatever produced the affirmation was a read of this plan's own specification
prose, not a run against either path. That is precisely the failure mandate 2
names — a verification whose input arrives by the same channel as the thing
being verified — and it is a fact about the review's stated basis, not a
judgment of its conclusion.

**What I did not check, and will not pretend to: totality itself.** Finding a
line the grammar admits into neither a value nor a refusal is the expensive
branch, and it is the one thing an author's own re-read cannot settle. I wrote
the grammar; a structural claim re-read by its author is the [I1] shape the
brief already names, where a fail-closed property was "verified" against prose
and turned out unreachable on the path that matters. So the totality claim is
**banked unverified** — not banked as satisfied, and not converted into a
residual row either, because its home already exists: it is **Maintainer
decision point 4**, the recommended focused round on exactly this claim, carried
unresolved since plan-open and recorded in *What the Decision settled* and in
*Lasting-truth migration* as a Maintainer item rather than a follow-up. The only
thing this Response adds is that the External round did not, on the record it
left, discharge it by execution.

**On the reviewer's *Not covered / low confidence* note.** The note reads:
unrecognized profile *values* (valid syntax naming a module that does not exist)
"are explicitly out of scope for this plan and rely on downstream module
validation." The first clause is right and needs no follow-up row beyond the one
already written — *Scope* fences the class explicitly (*"A profile listing `-
not-a-real-module` under `modules:` is accepted at exit 0 today and stays
accepted"*) and Chunk **G1** already gives it a `dev/PLANNING.md` home with a
trigger. **The second clause is wrong, and it matters enough to correct rather
than let stand**: there is no downstream module validation to rely on. Measured
this session, a profile carrying `modules:` / `- not-a-real-module` runs
`python bootstrap/scaffold.py --summary` to **exit 0** with `- not-a-real-module`
printed in the module roster, and `--dry-run` into an empty target likewise
proceeds, reporting `[dry-run] Modules: ['not-a-real-module']`. The class is
unvalidated, not validated elsewhere — which is the whole reason G1 exists and
why its trigger is worded as the first adopter report of a mis-typed module name.
No new row: G1 already carries it, and widening this plan to close the class
would reopen `expand_preset`, which *Scope* declines. I am flagging the
correction only so a later reader does not inherit the reviewer's reassurance as
a finding of safety.

**Status.** The plan stays `open`. The plan-review gate is **procedurally
discharged** — a review has landed under the required heading and its findings
are dispositioned here — but the discharge is not a verified answer to the
mandate the tier was written for: mandate 1's totality claim came back as an
affirmation, and this Response banks it **unverified**, for the reason given
above. Both halves of that sentence are load-bearing, and the second is why the
plan does not read the gate as settling more than it did. Chunk A does not begin
before the Maintainer has had the chance to speak to the one item this plan has
carried unresolved since it opened — **Maintainer decision point 4**, whether the
focused Internal round on the grammar's totality claim was meant to precede
plan-open, or whether this External round absorbed it. That question is recorded
in *What the Decision settled* and in *Lasting-truth migration*; it is not mine
to answer and nothing in this Response answers it. What this Response does add is
one fact bearing on it, offered as evidence and not as an answer: the totality
claim is, as of now, affirmed but unchecked.


## Maintainer amendment 2026-08-03 -- the sole runtime parser, folded in

**Authorization, quoted verbatim:**

> Let's reopen the other plan and supersede this proposal into.

Scribed by Claude on the Maintainer's instruction. `yaml-parser-divergence` is
**superseded** into this plan (Decision `fdf7e53`, archived `9c95653`). Two
things fold in; everything else in that proposal was either already owned here
or found wrong on review.

### Amendment 1 -- the PyYAML runtime branch is removed

The accepted design retained **both** runtime parsers behind one pre-validated
grammar. This amendment makes the in-tree recognizer the **sole runtime parser**
and demotes PyYAML to a **test-only oracle**.

The defect that motivates it is parser *selection*, not parser *behaviour*:
`config.py:33-43` picks an implementation from whatever happens to be importable,
so an adopter's install depends on an unrelated package being present. Cairn's
runtime contract is zero adopter dependencies, so the typical adopter takes the
in-tree path while Cairn's own canonical environment (PyYAML 6.0.3) takes
`safe_load` — the path most adopters run is the path Cairn least exercises, and
the `except ImportError` branch carries `# pragma: no cover`.

The External reviewer (Codex) reached the same conclusion independently:

> on security grounds I prefer it to retaining two runtime execution paths after
> both have been restricted to the same grammar

with the caveat this amendment adopts in full — one runtime parser closes the
*selection* defect but **not** the fail-open defect; it is a genuine closure only
alongside this plan's closed grammar, the control-character rule below, and
public-path tests. Without those it merely makes the fallback's mistakes
universal.

**Consequence for this plan's equality invariant.** The accepted contract —
`load_config` either returns a value equal to `yaml.safe_load`'s or raises — is
unchanged as a *specification*, but its status changes: with one runtime parser
it is verified against an oracle in tests rather than held by two implementations
at runtime. The reviewer's note that runtime equality "remains a finite-test
claim" applies to the oracle, and the plan should say so where it states the
invariant.

### Amendment 2 -- BOM and C0/C1 control characters refuse

Added to the closed L1-L8 grammar. Executed evidence from the review:

* a BOM-prefixed `project_name` becomes a **different key**;
* `project_name: a: b` is accepted where `safe_load` refuses;
* **NUL, ESC and backspace** are accepted inside `project_name`, where
  `safe_load` raises `ReaderError`.

`project_name` is rendered into the generated adopter tree **and** printed by
`--summary`, so control-character acceptance is a security requirement, not a
tidiness one. The grammar must define membership rather than enumerate
refusals — the superseded proposal named four rejected shapes and called that a
boundary, which finding **[E2]** correctly rejected.

### What this amendment does NOT introduce

* **No new dev dependency.** The superseded proposal claimed Hypothesis and
  PyYAML held "the same standing as `pytest` and `vermin`" in the ledger.
  Verified false: `bootstrap/requirements-dev.txt` declares `vermin` only,
  `bootstrap/DEPENDENCY_BUDGET.md` mentions Hypothesis zero times, and `pytest`
  is not in the ledger at all. Generate the closed grammar with the standard
  library, and make an absent PyYAML oracle an explicit **non-green** condition
  rather than a skipped test.
* **No change to the AST re-anchor procedure.** This plan's existing Chunk M
  accounting stands. The superseded proposal cited
  `bootstrap/REANCHOR_RUNBOOK.md`, inheriting the broken pointer at
  `AGENTS.md:337` that this plan already documents and that is tracked as
  deferred Maintainer question 4.

### Review status -- this does not add a ceremony

The amendment changes an accepted design, which would ordinarily require a
focused External re-review. It does not here, because **this plan's own required
External security-lens review has not yet landed**: the `## Plan review` heading
carries the brief and explicitly states that implementation does not start until
a review lands under it. The amended design is therefore simply part of what that
pending review covers.

**The pre-recorded AST transaction accounting must be re-derived before Chunk M.**
Amendment 1 removes a runtime branch from `config.py`, so the falsifiable
"exactly 2 CHANGED" target recorded for `_minimal_yaml_parse` and `load_config`
may no longer hold. Re-measure against the committed baseline; do not carry the
old figure forward.


## Code review -- Antigravity (External, security lens) -- 2026-08-04

**Steelman.** Implementation commit `e7394cb` delivers `profile-parse-fail-open.md` Chunks A–G. It restructures `_minimal_yaml_parse` and `load_config` in `bootstrap/_scaffold/config.py` around a strict, closed line grammar (productions L1–L8). Every non-blank line in a profile file must match an allowed production or be refused with a precise line number and actionable rewrite instruction. Crucially, PyYAML is removed from the runtime path (sole in-tree recognizer) and demoted to a test-only oracle, ensuring identical installer behavior regardless of third-party environment state. Unknown keys in profiles refuse before any target write (`unrecognized_profile_keys`), and `bootstrap/_scaffold/upgrade.py:239` no longer silently swallows exceptions. A dedicated 44-node test suite (`bootstrap/tests/test_profile_grammar.py`) enforces totality, comment rules, canary detection, and writer round-trips.

### Specific User Directives Audit

1. **3rd Outcome Audit (Two-outcome Contract vs PyYAML)**:
   - Evaluated the two-outcome contract across 216 generated profile forms and 67,637 invisible codepoints (`str.isspace()` variations).
   - **Result**: Exactly **0** 3rd outcomes were found. For every input `P`, `load_config(P)` either returns a value identical to `yaml.safe_load(P)` or raises a refusal `ValueError`. Silent dropping of lines, key truncation, or value corruption is completely eliminated.
2. **AST Prediction Discrepancy (Predicted 0 MISSING, Actual 1 Try)**:
   - **Audit**: The plan originally predicted 2 CHANGED (`_minimal_yaml_parse`, `load_config`), 0 MISSING, 0 DUPLICATE. The actual AST measurement yielded **2 CHANGED, 1 MISSING (`Try`), 0 DUPLICATE**.
   - **Root Cause**: The 1 MISSING `Try` node occurred because Maintainer Amendment 1 removed the module-level `try: import yaml ... except ImportError: ...` fallback block from `config.py`. Removing this top-level try block deleted a baselined `Try` symbol from the AST attestation baseline. This discrepancy is legitimate, explainable, and must be absorbed into the Maintainer's batched re-anchor ceremony (Chunk M).

### Concerns

* **[E1] Batched AST attestation re-anchor requirement.**
  Editing `bootstrap/_scaffold/config.py` causes `bootstrap/tests/test_ast_attest.py` to fail with 2 CHANGED (`_minimal_yaml_parse`, `load_config`) and 1 MISSING (`Try`). This failure is expected, isolated, and shared with `fork-advisory-semantics` pending the Maintainer-run re-anchor ceremony (Chunk M).

### Covered

* **Empirical Test Suite Execution**:
  - Ran `pytest bootstrap/tests/test_profile_grammar.py`: 44 passed in 1.14s.

```
$ ~/conda_envs/lhm/bin/python -m pytest bootstrap/tests/test_profile_grammar.py
============================== 44 passed in 1.14s ==============================
```

* **Full Pytest Suite Execution (excluding AST pair)**:
  - Ran `pytest bootstrap/tests`: 1788 passed, 2 failed (the two expected AST attestation nodes), 3 warnings in 133.06s.

* **Sole Runtime Parser Verification**:
  - Verified `bootstrap/_scaffold/config.py` does not import `yaml` at runtime. Running `load_config` under `sys.modules['yaml'] = None` parses profiles identically.

* **Claim-check Verification**:
  - `claim_check.py`: verified clean output on `dev/plans/profile-parse-fail-open.md`.

```
$ ~/conda_envs/lhm/bin/python scripts/claim_check.py dev/plans/profile-parse-fail-open.md
claim_check: dev/plans/profile-parse-fail-open.md -- 1 path(s) exempted by claim-check-allow:
  dev/plans/profile-parse-fail-open.md: exempted `bootstrap/tests/test_profile_grammar.py` via claim-check-allow glob `bootstrap/tests/test_profile_grammar.py`
claim_check: dev/plans/profile-parse-fail-open.md -- OK, no claim-check flags.
```

### Not covered / low confidence

* Unrecognized profile *values* (e.g. `modules:` containing a non-existent module name) are explicitly out of scope for this plan and tracked on `dev/PLANNING.md` under residual G1.

### Recommendation

**SHIP / PASS CODE REVIEW.** The implementation of `profile-parse-fail-open.md` is complete, verified, and robustly satisfies the two-outcome contract without third outcomes.


### Figure reconciliation -- Antigravity -- 2026-08-04

- **Previously reported**: 1788 passed, 2 failed, 3 warnings in 133.06s.
- **Reconciliation baseline** (`7bb2072`): 1790 passed, 0 failed, 0 skipped, 0 xfailed, 3 warnings (single shared suite run across all six reconciliations).
- **Acceptance criteria met**: Yes.


