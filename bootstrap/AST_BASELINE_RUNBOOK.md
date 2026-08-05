<!-- cairn-internal-ref-allow: doctrine/coordination.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file -->

# AST baseline re-anchor runbook

**Scope, stated first because the two are easy to confuse.** This runbook governs
the **AST attestation baseline** — `bootstrap/tests/fixtures/scaffold_ast_baseline.json`,
enforced by `bootstrap/tests/test_ast_attest.py` over the engine package
`bootstrap/_scaffold/`.

It is **not** `bootstrap/REANCHOR_RUNBOOK.md`. That runbook governs the
differential-oracle **gate anchor** (`refs/cairn/gate-anchor`) and says nothing
about this baseline. Two different trust artifacts, two different ceremonies; a
step from one does not transfer to the other.

## When this fires

`test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package`
fails after a `bootstrap/_scaffold/` change. **The baseline does not auto-update.**
The failure text is `AST baseline not accounted for across the engine package`.

## Who may perform it

Per `AGENTS.md` > *Operational pitfalls*:

* **Self-service** reaches only the four symbols in
  `_ast_attest._UPDATE_ALLOWLIST` — `_MODULE_MAPPINGS`, `_SKILLS_MAPPINGS`,
  `_CORE_MAPPINGS` (all `Assign`) and `install_onboarding` (`FunctionDef`) — and
  only when the additional preconditions in step 3 hold.
* **Anything else** is a **Maintainer-run, dry-run-verified direct correction
  that an implementing agent does not perform** (precedent `c3d5bd9`).

An agent that reaches step 3 and finds the preconditions unmet stops and reports;
it does not widen the allowlist, regenerate the whole baseline, or declare
symbols it did not author.

## Step 1 — diagnose, and derive the figures

**Never carry a delta figure forward from a plan, a commit message, or this
file.** Derive it against the committed baseline, at the commit you are repairing:

```
PYTHONDONTWRITEBYTECODE=1 python - <<'PY'
import json, pathlib, sys
sys.path.insert(0, 'bootstrap/tests'); import _ast_attest as A
baseline = json.loads(pathlib.Path(
    'bootstrap/tests/fixtures/scaffold_ast_baseline.json').read_text())
modules = sorted(pathlib.Path('bootstrap/_scaffold').glob('*.py'))
merged, _ = A._merge_current(modules)
problems, changed, missing, dup, new = A._classify(baseline, merged)
print(f"CHANGED {len(changed)}  MISSING {len(missing)}  "
      f"DUPLICATE {len(dup)}  NEW {len(new)}")
for p in problems: print("  problem:", p)
PY
```

**Read the classes correctly — this is where a diagnosis goes wrong:**

* **NEW is allowed by design.** `verify()` prints `note: NEW …` for every new
  top-level symbol and returns non-zero **only** on `problems`
  (CHANGED / MISSING / DUPLICATE). A grep for `^note:` therefore reports *nothing
  about whether the gate failed* — the problems print under a different prefix.
  Do not conclude "all NEW, nothing changed" from the notes alone.
* **CHANGED** means a baselined symbol's logic moved — not pure motion.
* **MISSING / DUPLICATE** mean a symbol left the package or now appears twice.
  Either is a review item in its own right, never a re-anchor.

Then **trace every CHANGED and every logic-bearing NEW symbol to the commit that
introduced it** (`git log --oneline -1 -S'<symbol>' -- bootstrap/_scaffold/`). A
symbol that traces to a landed, reviewed proposal is accounted for. One that
traces to nothing is the reason this ceremony exists.

## Step 2 — regenerate the known-new manifest

`update-symbol` refuses unless every NEW symbol is declared in
`bootstrap/tests/fixtures/scaffold_ast_known_new.json`, a
`{"<Kind>:<name>": ["<digest>", …]}` map enforced as a **complete-set match on
digest and multiplicity**. That refusal is the guard that stops a re-anchor
silently absorbing unreviewed additions. **No subcommand generates this file** —
compute it from `_ast_attest`'s own `_merge_current` / `_classify` (never a
reimplementation of them), and report the delta against the pinned file before
writing:

**Two delta classes are review items, not paperwork:**

* **DROPPED** — a key in the pinned manifest that no longer exists. A removed
  facade symbol is a behavioural change; find out why before proceeding.
* **REKEYED** — a key whose digest changed. This one is subtle and is the reason
  the report exists: **a symbol in known-new is invisible to the baseline gate.**
  `verify` classifies it NEW-and-allowed, so its logic can change without ever
  appearing as CHANGED. Regenerating the manifest would absorb that change
  silently. Trace every rekeyed symbol to its commit and satisfy yourself the
  change was reviewed.

## Step 3 — dry-run, and confirm the preconditions

```
python bootstrap/tests/_ast_attest.py update-symbol <SYMBOL> \
  --baseline bootstrap/tests/fixtures/scaffold_ast_baseline.json \
  --expect-old <CURRENT-BASELINE-DIGEST> \
  --known-new bootstrap/tests/fixtures/scaffold_ast_known_new.json \
  --dry-run bootstrap/_scaffold/*.py
```

The tool enforces all of these and refuses on any one:

1. `<SYMBOL>` is in `_UPDATE_ALLOWLIST` (which also supplies its kind);
2. `--expect-old` equals the symbol's **current** baseline digest;
3. the live module set shows it as the **only** CHANGED symbol, with no
   MISSING / DUPLICATE;
4. every NEW symbol matches the known-new manifest by digest and multiplicity.

**`--expect-old` is live state, not a constant. Re-derive it; never copy it from
a document — including this one.** In the 2026-08-05 exercise a value read from a
prepared command had gone stale because the tree moved, and the tool refused with
`expect-old mismatch … No write.` **That refusal is the guard working**, not an
error to route around: it is what stops the ceremony blessing a different change
than the one that was reviewed.

## Step 4 — apply, verify, commit

Apply by dropping `--dry-run`. Then:

```
python bootstrap/tests/_ast_attest.py verify \
  bootstrap/tests/fixtures/scaffold_ast_baseline.json bootstrap/_scaffold/*.py
PYTHONDONTWRITEBYTECODE=1 python -m pytest bootstrap/tests -q
```

`verify` must end `AST attestation OK — N baselined symbol(s) accounted for,
unchanged.` **N must not have grown**: `update-symbol` rewrites one digest in
place, so the baseline symbol count is unchanged by a correct re-anchor. A grown
count means a full re-pin happened instead.

Commit **both** fixtures, with explicit paths (the git index is shared with
concurrent sessions, so a bare `git commit` can take their staged work):

```
git commit bootstrap/tests/fixtures/scaffold_ast_baseline.json \
           bootstrap/tests/fixtures/scaffold_ast_known_new.json \
  -m "ast-attest: re-anchor <SYMBOL> and refresh the known-new manifest"
```

## What this ceremony never does

* **No full re-pin during extraction.** `test_ast_attest.py`'s own comment is
  binding: *"Do NOT re-pin the baseline during extraction — that would erase the
  motion reference."* A full regeneration destroys the pure-motion evidence the
  baseline exists to provide, and it converts every unreviewed change into an
  accepted one.
* **No allowlist widening to make a repair possible.** If the CHANGED symbol is
  not one of the four, the answer is a Maintainer correction, not a bigger
  allowlist.
* **No declaring symbols you did not author.** The known-new manifest is an
  attestation. An agent regenerating it for symbols from other sessions' work is
  blessing its own verifier.

## Worked example — 2026-08-05

Recorded because a runbook whose steps were never executed is a document, not a
procedure.

* **Diagnosis:** `CHANGED 1, MISSING 0, DUPLICATE 0, NEW 78`. The single CHANGED
  symbol was `Assign:_MODULE_MAPPINGS` in `_scaffold/config.py`,
  `26957a8924042a0a → 4f72dfcb7ce39f20` — exactly the *"one changed engine
  symbol"* its implementing commit (`8daecd2`) had declared.
* **Known-new:** pinned file carried **28** keys, last written 2026-07-31;
  the live NEW set was **78**. Of the 50 additions, 33 were plain `Import`
  statements and the 17 logic-bearing ones traced to three landed reviewed
  proposals — `e7394cb` (profile-parse-fail-open), `9bd6752`
  (fork-advisory-semantics), `949e6d4` (lockfile-provenance-fields). **0 dropped.**
* **One REKEYED item, and it is the example of why step 2 reports them:**
  `FunctionDef:_resolve_current_profile` (`_scaffold/upgrade.py`) changed digest
  `cba0f67404694e64 → b408719b6ffe88ff`. Because it sits in known-new rather than
  the baseline, the baseline gate never saw it as CHANGED. Traced to `e7394cb`,
  a reviewed proposal about reading the profile through a closed grammar — i.e.
  accounted for, but only because it was looked for.
* **Outcome:** `AST attestation OK — 173 baselined symbol(s) accounted for,
  unchanged.` Baseline count unchanged at **173** (surgical, not a re-pin);
  known-new at **78** keys.
* **The `--expect-old` guard fired** on a stale value read from a prepared
  command after the tree moved, and refused with no write. See step 3.
