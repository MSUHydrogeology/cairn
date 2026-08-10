<!-- cairn-internal-ref-allow: doctrine/plans.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- The new test module is a forward reference registered under `Proposed paths`; the
     marker exempts only its own contiguous block, and the chunk tables cite it many
     sections later, so it needs the file-scoped directive too.  Drop this directive
     once the path lands (Chunk A), per the marker discipline. -->
<!-- claim-check-allow: bootstrap/tests/test_fork_advisory.py -->

# Plan: fork advisory semantics — the comparison bytes come from the caller, never from the tree being checked

**Source proposal**: `fork-advisory-semantics` (accepted 2026-08-03; the Decision
commit is `86a0a78`). It currently sits under `dev/proposals/` and moves to
`dev/proposals/archive/` when it archives.
**Status**: open
**Plan review**: required(**External**, security lens) — carried from the proposal
header, mandated by the superseding `identity-not-name` Decision, and **not**
discharged by either round the proposal already had (the External round returned
SHIP before two BLOCKING-class gaps were found; the Internal round says in terms
that it "must not be counted toward it"). **No implementation commit lands before
the `## Plan review` section carries a real review.**
**Last update**: 2026-08-03
**Opened**: 2026-08-03

## Source proposal

`fork-advisory-semantics` is scope 3 of the superseded `identity-not-name`
proposal. It fixes one defect and closes one defect *class*.

**The defect.** `bootstrap/_scaffold/lockfile.py` carries a **fork advisory** — a
detector that warns when a *facade* has diverged from upstream while its *engine
package* sits installed. It fires today on Cairn's own tree, twice, and both
notes are false in both of their claims. Re-measured for this plan at HEAD
`05515df` under the canonical interpreter (`~/conda_envs/lhm/bin/python`,
3.13.13), with `PYTHONDONTWRITEBYTECODE=1`:

```
$ python bootstrap/verify_integrity.py --target .
verify_integrity: NOTE -- facade 'tools/intent.py' is forked from upstream ...
verify_integrity: NOTE -- facade 'tools/lifecycle_metrics.py' is forked from upstream ...
verify_integrity: OK -- 76 recorded file(s) match dev/.cairn/cairn-lock.yml
  (5 adopter-authored living-state file(s) ...)
rc=0
```

**The class.** The detector's fork test is `hash != base_hash`, and both operands
are fields the tree under check writes into its own lockfile. The invariant that
survived the whole parent exchange is one sentence:

> **The artifact under verification must not supply the material used to verify it.**

**The design, settled by the Decision and not re-opened here.** The detector gains
a required, keyword-only, no-default `upstream: UpstreamSource | None` parameter.
Each caller supplies it from a root resolved from the caller's own on-disk
location. The destination→source map is built from the engine's own in-memory
registries, never from the lockfile's `src`. The target-side operand is **bytes
read from disk**, never a recorded hash. Both joins are containment-checked. Every
degradation path **retains** the finding as `unconfirmed`; the only removal path is
byte-equality between two validated reads.

The proposal went through an External security review (SHIP), an author Response
that declined two of its summary-level absolutes, a first revision (A1–A3), an
Internal security review (BLOCKING, seven findings), a second revision (B1–B8,
which closed [I1] at proposal time rather than deferring it), and a Response. The
Decision accepted it *as revised*, added the engine obligations, and directed that
the re-anchor ceremony be **batched with `profile-parse-fail-open`** so it is paid
once.

### Glossary — every term glossed on first use

The audience is a scientist who codes.

* **Facade** — a thin launcher script Cairn installs into an adopter tree
  (`tools/intent.py`) that loads an **engine package** sitting beside it
  (`tools/_intent/`). The launcher is deliberately tiny; the real code is in the
  package.
* **Lockfile** — `dev/.cairn/cairn-lock.yml`, a machine-generated record of every
  file the install wrote, with a SHA-256 hash each, so `bootstrap/verify_integrity.py`
  can later attest that nobody swapped a shipped script.
* **`hash` / `base_hash`** — two hashes per lockfile record: what is on disk now
  (as last attested), and nominally the upstream template the file started from.
  `base_hash` is **not** reliably upstream: `--finalize` backfills it from the
  then-current installed hash, so every legitimate edit-then-finalize widens the
  apparent gap. It ratchets and never narrows.
* **Operand** — one of the two things a comparison compares. This whole plan is
  about pinning where each of the two comes from.
* **Oracle** — whatever supplies a test's expected answer. An oracle computed by
  the code under test cannot fail; it agrees with the code by construction,
  however wrong the code is.
* **AST attestation** — `bootstrap/tests/test_ast_attest.py` pins every top-level
  symbol in `bootstrap/_scaffold/*.py` against a committed baseline by a
  structural digest that ignores comments and formatting but catches any logic
  change. It does **not** auto-update.
* **Frozen set / `FROZEN-MODIFIED`** — `bootstrap/tests/_gate_manifest.py` freezes
  the byte-hashes of files whose content *defines* a gate's pass/fail semantics.
  Editing one is reported as `FROZEN-MODIFIED`, a HOLD.
* **Re-anchor** — the supervised ceremony that moves a gate's committed baseline
  forward after a legitimate change. Cairn has two, they are routinely conflated,
  and this plan needs both (see *Correction 4*).

## Five plan-time corrections to the proposal's gate accounting

Placed before *Scope* because they change what an implementing agent must do, and
because the proposal's own Internal review closed with the discipline point that
produced them: *"Re-measure at plan-open rather than inheriting."* Every figure
below was measured for this plan at HEAD `05515df`, not carried from the proposal.

### Correction 1 — a **third** frozen file must be edited, and neither review found it

**This is the finding this plan contributes.** The proposal's gate accounting
names two frozen-file edits (`bootstrap/verify_integrity.py` and
`bootstrap/tests/test_verify_integrity.py`) and states that *"any third hold is a
stop."* There is a third, and it is forced by the design.

The design requires `bootstrap/_scaffold/lockfile.py` to import the containment
guard — B3 makes it validate joins on *both* sides, and B7 keeps
`_assert_safe_write` as the primitive rather than growing the security leaf.
`bootstrap/tests/test_lockfile_module.py` pins that module's import set to the
standard library plus the `config` leaf and nothing else. Reproduced in a scratch
copy of `bootstrap/` under the session scratchpad — nothing was written into the
repository:

```
$ # scratch copy; add the import the design requires, then run the layering test
$ python -m pytest bootstrap/tests/test_lockfile_module.py -q
E  AssertionError: lockfile imports 'security' (level=1)
FAILED bootstrap/tests/test_lockfile_module.py::test_lockfile_depends_only_on_stdlib_and_the_config_leaf
1 failed, 6 passed in 0.07s
```

`bootstrap/tests/test_lockfile_module.py` is in the frozen set — confirmed by
direct membership check against the committed manifest at HEAD. So the design as
accepted requires **three** frozen-file edits, and the third one is an
**assertion widening on a gate file**, which is a strictly worse character than
the other two (`bootstrap/tests/test_verify_integrity.py`'s edit adds one keyword
argument to one call and leaves its assertions untouched).

**This plan does not weaken the gate quietly, and it does not reshape the design
to dodge it.** Chunk C widens the admitted set from `{config}` to
`{config, security}`, in the same commit as the import that requires it, with a
discrimination test that proves the widened assertion still refuses everything
else.

**The shape of that edit, corrected at plan review (per [E1]).** The assertion is
**not** a set literal — it is a suffix predicate, `assert
mod.endswith("config")`, so there is no set to add a name to. The falsifiable
check the Maintainer is owed is therefore: the diff touches **only** that one
layering assertion, leaves the other six nodes in the file untouched, and the
widened assertion is written as **membership of the module's final dotted
component in `{"config", "security"}`** — not as a widened suffix test. The
distinction is load-bearing and was measured, not reasoned: under the current
interpreter, `"insecurity".endswith("security")` is `True`, so the suffix form of
the widening admits a `.insecurity` leaf that is *not* in `{config, security}`,
which is exactly the over-widening [E1] asks the gate to refuse. The membership
form incidentally tightens a pre-existing looseness on `config` (a `.fakeconfig`
leaf passes the assertion **today**); that side effect makes the gate strictly
narrower, never wider, and is visible in the C7 diff.

**The alternative was considered and is recorded rather than silently passed
over.** `lockfile.py` could inline three private containment checks instead of
importing the leaf. That trades one frozen-file edit for a second, unreviewed copy
of a security primitive inside a near-leaf — which is the shape the proposal's own
*Alternatives* section rejected when it declined to grow the security leaf for one
caller. Widening a layering assertion in the open is the cheaper honesty. **If the
plan reviewer disagrees, this is the right place to say so**, because it is the
one point at which this plan departs from the accepted gate accounting.

### Correction 2 — the gate manifest already HOLDs at HEAD, on two unrelated files

The proposal expects *"exactly 2 `FROZEN-MODIFIED` holds … Any third hold is a
stop."* That expectation is false as an absolute before this plan writes a byte:

```
$ python bootstrap/tests/_gate_manifest.py verify --no-collect
[gate-manifest] HOLD — 2 gate-integrity violation(s):
  FROZEN-MODIFIED: bootstrap/tests/test_quality_gate_redundancy.py (gate file edited — sha differs)
  FROZEN-MODIFIED: scripts/quality_gate.py (gate file edited — sha differs)
rc=1
```

Both come from commit `7066489` (today's `r6-unused-def-blindspot` fix), which is
outside this plan entirely. The expectation is therefore a **delta** claim, not a
set claim: this plan's contribution is exactly **3** additional
`FROZEN-MODIFIED` entries and exactly **1** `FROZEN-NEW`, on top of whatever the
pre-edit run reports. Chunk A captures that pre-edit run as its own baseline.

**Two pre-existing entries are not this plan's to clear.** They are recorded as a
`dev/PLANNING.md` row at plan-open, noting the seam with
`gate-claims-vs-enforcement` (status `proposed`), which already reasons about
frozen-file HOLDs blocking edits. This plan makes no claim on them.

### Correction 3 — nothing in the suite fires the gate-manifest check

Stated because a documented gate that nothing fires is a defect, and because this
plan's Verification section names that command. Swept at HEAD: no
`.github/workflows/` directory exists; the repository's `pre-commit` hook runs
only `tools/intent.py _precommit_check`; and `bootstrap/tests/test_gate_manifest.py`
exercises the tool's mechanics against a freshly-`produce`d manifest through a
fixture, never against the committed one. So:

* **`bootstrap/tests/test_ast_attest.py` is fired by the suite.** `python -m pytest
  bootstrap/tests` collects and runs it. It is a real gate and it will go red.
* **`bootstrap/tests/_gate_manifest.py verify` is fired by a human typing the
  command.** It is an operator tool. This plan names the operator (the Maintainer
  at Chunk R; the implementing agent at each chunk's acceptance check) rather than
  implying an automatic gate that does not exist.

### Correction 4 — two different re-anchor ceremonies apply, and Phase 0 is not the AST one

Both are **Maintainer-only**; an implementing agent performs neither. They are
different mechanisms and the proposal's own text conflates them once.

* **The AST source-motion baseline** (`bootstrap/tests/fixtures/scaffold_ast_baseline.json`)
  is **not** governed by `bootstrap/REANCHOR_RUNBOOK.md`. Confirmed for this plan:
  `grep -n -iE 'ast_attest|scaffold_ast_baseline' bootstrap/REANCHOR_RUNBOOK.md`
  returns zero hits. The mechanism that applies is the one
  `lockfile-provenance-fields` established and used — a Maintainer-run,
  dry-run-verified direct-correction script, in a commit the Maintainer authors.
  The self-service `update-symbol` path is unavailable: its allowlist admits four
  registry symbols and none of this plan's symbols is among them.
* **The frozen-set / gate-manifest trust root** *is* what
  `bootstrap/REANCHOR_RUNBOOK.md` governs, and its **Phase 0 and Phase 4 are
  explicitly Maintainer-only** — the runbook's own words are that an implementing
  agent must not perform them, "the forbidden *implementer blesses its own
  gate*". This plan puts them in their own chunk (Chunk R) and an implementing
  agent must not enter it.

The mispointing in `AGENTS.md` that causes this conflation is the proposal's R8.
It is **claimed by `gate-claims-vs-enforcement`** and is not fixed here.

### Correction 5 — the batched ceremony changes the falsifiable target from a set to a union

The Decision directs: *"**Batch it** with `profile-parse-fail-open` so that
ceremony is paid once."* That supersedes the proposal's B6 recommendation that only
one of the two lifecycles hold an open plan at a time. Three consequences an
implementing agent and a reviewer must both hold:

1. **The suite is red across both plans' execution windows.** From this plan's
   first engine-touching commit until Chunk R, `bootstrap/tests/test_ast_attest.py`
   fails. That window now also spans the sibling's chunks. **The mitigating
   invariant, which is checkable per chunk**: between Chunk B and Chunk R, the
   *only* failing nodes attributable to this plan are the AST-attestation nodes.
   Any other failure is a stop, not a known-red.
2. **"Exactly 3 CHANGED" is this plan's contribution, measured in isolation.** The
   combined ceremony sees the union of two disjoint sets. The two sets are
   disjoint by inspection — this plan changes `forked_facade_findings` and
   `format_forked_facade_warning` in `bootstrap/_scaffold/lockfile.py` and
   `cmd_upgrade` in `bootstrap/_scaffold/upgrade.py`; the sibling changes
   `load_config` and the fallback parser in `bootstrap/_scaffold/config.py` plus
   `bootstrap/_scaffold/cli.py`. **A symbol outside the union is a stop.**
3. **The isolation measurement must not be taken from the shared working tree.**
   Chunk D's acceptance runs the attestation in a throwaway `git worktree` at this
   plan's own last engine commit, so the sibling's edits are absent by
   construction rather than by an implementer's care.

**Re-measured NEW-note accounting, because the proposal states it as a set and it
is a delta.** At HEAD the attestation already emits **29** non-`Import:` NEW notes
and **32** `Import:` notes, all informational, `rc 0` — pre-existing drift the
`ast-known-new-repin` lifecycle tracks separately. This plan's contribution is
therefore *exactly two additional* non-`Import:` NEW notes
(`FunctionDef:trusted_upstream`, `ClassDef:UpstreamSource`) plus rotated `Import:`
keys. Verified in a scratch copy that an import-only edit to `lockfile.py` rotates
`Import:` keys and still returns `rc 0`, so no NEW note can fail the gate.

### The condition-3 sequencing question, put to the Maintainer and not resolved here

The `identity-not-name` Decision's condition 3 routes the remediation-string fix
out of all four successor scopes: it *"lands immediately as trivial-class"*. It is
**not landed** — the string still reads *"remove the dormant engine package"*, and
`tools/intent.py`'s `_load_engine()` raises `RuntimeError` when that package is
absent, so the advice disables work-intent coordination. Confirmed at HEAD.

The proposal priced three shapes. The Decision's "batch it" answers the *ceremony*
question but not this one, and no `dev/PLANNING.md` row records a choice. What has
changed since the proposal priced it is **Correction 5**: because the suite is
already red from this plan's first engine commit until Chunk R, folding the
trivial fix into that window costs **no additional red time**. Landing it *before*
plan review extends the red window backwards by the whole review interval.

* **Shape (1)** — trivial commit now, with its own Maintainer-run re-anchor in the
  same sitting. Tree stays green; the dangerous advice dies today; costs a second
  ceremony, which is what the Decision's "paid once" argues against. This plan
  then re-derives its AST target against the new baseline commit.
* **Shape (2)** — trivial commit now, re-anchor deferred to Chunk R. Cheapest in
  ceremony; the tree is red from today until Chunk R, which now spans two plans'
  execution windows and a required External plan review.
* **Shape (3)** — the trivial fix lands as **Chunk B of this plan**, inside the
  already-red window. One ceremony, no additional red, and the dangerous advice
  stays live until Chunk B. **This shape requires the Maintainer to amend
  condition 3**, which neither the proposal nor this plan asks for.

**This plan is sequenced on shape (3) as its default** because it is the only
shape consistent with both "paid once" and "no gratuitous red", and because Chunk
B rewrites the same function Chunk C rewrites — but Chunk B is fenced as
Maintainer-gated and **does not execute without an explicit amendment to condition
3**. If the Maintainer picks shape (1) or (2), Chunk B is struck, the trivial
commit's landing sha is recorded here, and Chunk R's target is re-derived against
the baseline that leaves. Nothing else in the sequence moves.

## Proposed paths

Proposed paths:
- `bootstrap/tests/test_fork_advisory.py` — the new test home: the fixture matrix, the committed F1 oracle literal, and all 18 nodes; lands in Chunk A and grows through Chunks C and D.

## Scope

Executes `fork-advisory-semantics` as revised through its second revision
(A1–A3, B1–B8), across `bootstrap/_scaffold/lockfile.py`,
`bootstrap/_scaffold/install.py`, `bootstrap/_scaffold/upgrade.py`,
`bootstrap/verify_integrity.py`, three frozen test files, one new test file, and
two descriptive-layer documents. Chunk R is the Maintainer's and is fenced from
the implementing agent's work by construction.

**Out of scope, fenced explicitly:**

* **The `SECURITY_MUTATIONS.md` Class C follow-on.** Declined by this scope and by
  `release-authenticity`, unclaimed by any of the four successors, and recorded as
  deferred Maintainer question 1 on `dev/PLANNING.md`. Chunk E writes **one
  sentence** recording that it is unclaimed and naming R7's three triggers. That
  sentence is a *durable home for a residual*, not Class C work, and it is not a
  re-classification.
* **Repairing `base_hash`** (residual R2). `--finalize`'s backfill is unchanged.
  Re-anchoring it was rejected in the parent proposal — it would make finalize
  bless the current tree as upstream, a silent wrong answer replacing a noisy one.
* **Candidate selection** (residual R10). F5 pins the *verdict* to trusted-vs-disk
  bytes; `hash`, `base_hash`, `dst` and the engine-directory probe still decide
  *which* records are examined. A lockfile asserting `hash == base_hash` evades
  the advisory entirely. Unfixable while `base_hash` is a lockfile field.
* **Any exit-code change** (F3). The advisory stays advisory. A genuinely forked
  facade still passes `verify_integrity`.
* **`fork_acknowledged`** (residual R5), the target-controlled verify-time
  opt-out. Unchanged.
* **Materializing `--to <ref>`'s templates** (residual R3). `--to` falls back to
  `unconfirmed`. The engine already owns a primitive that reads a ref's template
  bytes, but reusing it would invert the module edge (`upgrade` imports *from*
  `lockfile`) and would import an unguarded join into the one path this plan is
  adding a guard to.
* **Authenticating the checkout that supplies the comparison bytes** (residual
  R1). This change moves the comparison from target-controlled to
  caller-controlled; it does not move it to cryptographically anchored. That is
  `release-authenticity`'s job.
* **Attesting the engine package's contents** — only its presence.
* **`_infer_init_lock_axes`** in `bootstrap/_scaffold/upgrade.py`, which infers
  `human_team` from the mere presence of a root `CONTRIBUTING.md`. A different
  function; folding it in would break the falsifiable AST target. Carried as a
  residual by scope 4.
* **A read-flavoured containment sibling in the security leaf** (residual R6).
  Deferred; it grows a high-risk surface by a symbol with one caller.
* **The `AGENTS.md` re-anchor mispointing** (residual R8) — claimed by
  `gate-claims-vs-enforcement`.
* **The two pre-existing `FROZEN-MODIFIED` entries** from `7066489`
  (*Correction 2*).

### Documentation / doctrine surface

* **Descriptive layer** — `bootstrap/UPGRADE.md` gains a short subsection stating
  the advisory's three note kinds and what each means. Today `UPGRADE.md` does not
  document the fork advisory at all, so an adopter who receives the note has no
  documented referent; confirmed by grep for this plan. This is the doc
  deliverable.
* **Engine-local record** — `bootstrap/_scaffold/SECURITY_MUTATIONS.md` gains one
  sentence in its Class C section (see *Scope*, above).
* **Release-facing** — `CHANGELOG.md > Unreleased > Fixed`.
* **Deliberation layer** — this plan, its plan review, its code review, and the
  `dev/PLANNING.md` rows it opens at plan-open.
* **Governing layer** — **none.** No `AGENTS.md` change and no `doctrine/` change.
  The one `AGENTS.md` correction this lifecycle identified (R8) is claimed
  elsewhere; bundling it would lose the git-workflow approval carve-out and mix
  two review tiers.
* **Doctrine-change rate-limit** — **not engaged.** This plan changes no rule,
  process, or contract that every contributor follows.

<!-- cairn:slot documentation-tier-home -->
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
plan's *Scope* must name the doctrine-surface touched (or an explicit
"no doctrine surface").
<!-- cairn:end documentation-tier-home -->

## Sequence

```
0. plan-open       -- this plan + dev/PLANNING.md rows + proposal archive    [commit pending]
   (plan review)   -- required(External, security lens); NO code before it lands
1. Chunk A -- the pre-change oracle and the fixture matrix (tree stays green) [commit pending]
2. Chunk B -- MAINTAINER-GATED: the trivial remediation-string fix            [commit pending]
3. Chunk C -- the engine core: operands pinned, both joins guarded            [commit pending]
4. Chunk D -- trusted_upstream + the two callers + the isolation measurement  [commit pending]
5. Chunk E -- UPGRADE.md, SECURITY_MUTATIONS.md, CHANGELOG, residual homes    [commit pending]
6. Chunk R -- MAINTAINER-ONLY: the batched re-anchor ceremonies               [not an agent's]
```

**Sequencing invariant — every intermediate commit is fail-loud.** At no point
does a partially-implemented path *suppress* a finding the finished detector would
retain. An unimplemented branch degrades to `unconfirmed`, which keeps the note. A
reviewer should check this per chunk rather than take it here.

### Chunk A — the pre-change oracle and the fixture matrix

Lands **before any engine edit**, so the tree is still green and the F1 oracle
provably predates the change. This is the chunk that makes the rest reviewable.

| # | File | Change |
|---|------|--------|
| A1 | `bootstrap/tests/test_fork_advisory.py` *(new)* | The fixture matrix: a builder that constructs a throwaway target tree (facade, optional engine package, lockfile record) **and** a throwaway trusted-templates tree, independently parameterised. Imports the existing helpers in `bootstrap/tests/test_verify_integrity.py` rather than duplicating them. |
| A2 | `bootstrap/tests/test_fork_advisory.py` | The **F1 golden oracle** as a committed literal: the finding set the *pre-change* detector produces over every matrix row, generated once by running the engine at this plan's pre-Chunk-B commit in a throwaway `git worktree`, and pasted in. Never computed at test time; never derived from `forked_facade_findings`. |
| A3 | `bootstrap/tests/test_fork_advisory.py` | Node 8 (**F3**) — `verify_integrity.verify(target) == 0` with a live finding present. Green before and after the change; it is the exit-code pin and R5's mechanical trigger. |
| A4 | `bootstrap/tests/test_fork_advisory.py` | The **red-then-green ledger fixture**: the nodes that assert post-change behaviour are marked in the module with the commit at which they are expected to flip, and Chunk A's commit body records the observed pre-change failure list. |

**Acceptance criteria — Chunk A**

* **The suite is green at this commit.** `python -m pytest bootstrap/tests` under
  the canonical interpreter: **1601 passed, 0 failed, 0 skipped** at HEAD
  `05515df` — measured for this plan, 150.69s, not quoted from memory — plus
  exactly the new nodes, none dropped, none skipped or xfailed.
* **The oracle's channel is named and is not the artifact.** The literal is
  produced by `python bootstrap/tests/_ast_attest.py`-era code at a **named
  commit**, read through a throwaway `git worktree`, under the canonical
  interpreter. The commit sha goes in the commit body. **A regeneration from the
  working tree is a review finding**, because the working tree is what the later
  chunks change.
* **Pre-edit gate baselines captured, not inherited.** The commit body records the
  output of `python bootstrap/tests/_gate_manifest.py verify --no-collect`
  (expected: the 2 pre-existing holds from `7066489`, *Correction 2*) and the
  attestation's pre-edit NEW-note counts (expected: 29 non-`Import:`, 32
  `Import:`, `rc 0`).
* **Perturbation, run not asserted (F3 / node 8):** make the advisory append a
  string to `violations` in `bootstrap/verify_integrity.py`'s loop in a scratch
  copy → node 8 fails. Restore byte-identical → green. This is what makes F3 a
  real tripwire on R5 rather than a decorative assertion.
* **Perturbation, run not asserted (the oracle, node 14 preview):** widen the
  candidate gate in a scratch copy to admit records with no `base_hash` → the
  branch-to-branch consistency assertion stays green while the golden assertion
  goes red. Recorded now, because it is the whole reason the oracle is external.

### Chunk B — the trivial remediation-string fix (MAINTAINER-GATED)

> **Does not execute without an explicit Maintainer amendment to `identity-not-name`
> condition 3.** See *The condition-3 sequencing question* above. If the Maintainer
> picks shape (1) or (2), this chunk is struck and the standalone commit's sha is
> recorded in its place.

| # | File | Change |
|---|------|--------|
| B1 | `bootstrap/_scaffold/lockfile.py` | `format_forked_facade_warning`'s remediation string: the destructive branch is **removed, not reworded**. "Remove the dormant engine package" raises `RuntimeError` in `tools/intent.py`'s `_load_engine()` and disables work-intent coordination outright. The no-op branch ("complete the swap") goes too — the thin launcher is what is installed. |
| B2 | `bootstrap/tests/test_fork_advisory.py` | A node asserting no branch of the remediation string advises removing the engine package, and that the surviving advice names an action that leaves the tool working. |

**Acceptance criteria — Chunk B**

* **This is the commit that turns the suite red, and it is the last time that is
  expected.** `python -m pytest bootstrap/tests` fails exactly the two
  AST-attestation nodes and nothing else. The commit body names them. Any third
  failing node is a stop.
* **Perturbation:** restore the destructive clause in a scratch copy → B2's node
  fails. A node that stays green against the string it forbids is not accepted.
* **`python scripts/claim_check.py` clean** on any Markdown this chunk touches
  (one file per invocation).

### Chunk C — the engine core: operands pinned, both joins guarded

The security core, and the smallest self-contained unit the plan reviewer can
attack. Everything here lands in `bootstrap/_scaffold/lockfile.py` except C7.

| # | File | Change |
|---|------|--------|
| C1 | `bootstrap/_scaffold/lockfile.py` | `UpstreamSource` (`NamedTuple`: `templates_root`, `src_for_dst`, `ref`) and the new keyword-only, **no-default** `upstream` parameter on `forked_facade_findings`. Omitting it is a `TypeError`; passing `None` is a legal, explicit "no trusted upstream". |
| C2 | `bootstrap/_scaffold/lockfile.py` | **Source-side validation** (B7's corrected motivation): `src_rel` relative, POSIX-shaped, no `..`; `_assert_safe_write(candidate, templates_root)`; result must be an existing regular non-symlink file. Any failure → **no comparison**, finding retained as `unconfirmed`. The `ScaffoldSecurityError` is caught inside this module so a malformed templates tree degrades the advisory instead of aborting the verifier. |
| C3 | `bootstrap/_scaffold/lockfile.py` | **Destination-side validation** (B3 / **F6**), the same three checks against `target`, plus: `forked_facade_findings` **resolves `target` once at entry** and uses the resolved root for the containment check, the destination join *and* the engine-directory probe — so containment never depends on caller ordering. |
| C4 | `bootstrap/_scaffold/lockfile.py` | **The target-side operand** (B2 / **F5**): `read_bytes(target / dst_rel)` after C3's checks. The comparison is `disk_bytes == upstream_bytes`, a comparison of two reads. `rec["hash"]`, `rec["base_hash"]` and every other lockfile field are **forbidden** as the target-side operand, and a caller may not pass precomputed hashes in to avoid the read. |
| C5 | `bootstrap/_scaffold/lockfile.py` | The three note kinds as a **field on the finding**, not a reader's guess: `differs-from-upstream` (names the upstream it compared against), `unconfirmed` (says the difference is from the *install-time baseline* and could not be confirmed against upstream), and the skew annotation line. `src_relabelled` is an **annotation on a finding that already exists** — never a new note (B4 / **R9**). `format_forked_facade_warning` renders all three. |
| C6 | `bootstrap/_scaffold/lockfile.py` | Residual comment homes, AST-invisible: **R6** at the `_assert_safe_write` call site (write-flavoured guard on a read path; restated trigger per A3), and **R10** at the candidate gate (selection remains lock-derived), alongside R2's existing comment. |
| C7 | `bootstrap/tests/test_lockfile_module.py` **(frozen file #3)** | The layering assertion in `test_lockfile_depends_only_on_stdlib_and_the_config_leaf` widens from `{config}` to `{config, security}` — *Correction 1*. The existing form is a suffix predicate (`mod.endswith("config")`); the widened form is **membership of the module's final dotted component in `{"config", "security"}`**, because the suffix form of the widening admits `.insecurity` (measured, *Correction 1*). Exactly that one assertion; **the other six nodes in the file are not touched**. |
| C8 | `bootstrap/tests/test_fork_advisory.py` | Nodes **1–6, 11–15, 18**. Detailed with their perturbations below. |

**The node table for Chunk C.** Every row states the future state in which the
node fails; the implementing commit's body carries the observed result of running
each perturbation, not a claim that it would fail.

| Node | What it pins | Perturbation that must make it fail |
|---|---|---|
| 1 | A facade byte-identical to its trusted template emits **no** note even when `hash != base_hash` — the headline regression, reproducing today's two live false notes as a fixture | Revert the verdict to `hash != base_hash` alone |
| 2 | Source-version skew: the skew line fires, the finding set does not grow (**F1**), a byte-identical facade is still suppressed | Delete the skew-annotation branch |
| 3 | Four unsafe **source** shapes (`src` absolute; `src` with `..`; source a symlink; source with a symlinked parent): comparison refused, finding **retained** as `unconfirmed`, no exception escapes | Delete C2's `_assert_safe_write` call. **The fixture is built so this matters**: the escape target's bytes are identical to the on-disk facade, so without the guard the finding is wrongly *suppressed* — the node fails rather than merely losing a message |
| 4 | `dst` absent from the trusted map, and source file absent: `unconfirmed`, retained | Make an unmapped `dst` fall through to "no finding" |
| 5 | **Target-supplied lookalike**: the target carries its own templates directory holding a file byte-identical to its forked facade **and** re-points the lockfile's `src` at it. The note is **not** suppressed; `src_relabelled` fires. This is [IDN4]'s regression proper | Resolve the template through `rec["src"]` instead of the trusted map |
| 6 | Both layouts: facade + populated engine dir (finding); facade + no engine dir (none); engine dir present but empty of `.py` (none); non-`.py` `dst` (none) | Drop the engine-directory probe |
| 11 | **F5, the operand**: a record whose `hash` equals the trusted template's hash while the on-disk bytes differ still produces a finding — at **both** callers | Suppress on `rec["hash"] == sha256(trusted)`. This is the Response's Reproduction B, re-run against real code |
| 12 | Target-side file missing while the record claims a fork: `unconfirmed`, retained, no exception | Let the missing file raise, or suppress |
| 13 | Four unsafe **destination** shapes (`dst` absolute; `dst` with `..`; `dst` a symlink; `dst` with a symlinked parent): the finding is retained as `unconfirmed`, the reason names which guard check fired, and **no bytes from outside `target` or `templates_root` reach the comparison**. **Corrected at implementation** — the row previously read "nothing is read outside `target`", which is false and was measured so: the candidate gate joins `target_root / engine_rel` **unguarded** (R10) and stats/globs an engine dir outside `target` on three shapes, and the guard must `lstat` what it refuses on two. The claim the code supports is about *bytes deciding the verdict*, not about filesystem touches | **Two perturbations, both required, because they exercise different halves.** (a) Replace C3's destination-side guarded read with a bare `(target_root / dst_rel).read_bytes()` — same fixture discipline as node 3 (a canary outside `target` byte-identical to the trusted template), so the unguarded read *suppresses* and retention fails. (b) **Leave** the guarded read and add an *unguarded* read ahead of it — the verdict is unchanged, so (a)'s assertions all still pass and only the containment assertions go red. A node carrying only (a) leaves the containment half untested |
| 14 | **F1 golden oracle** — the trusted-upstream finding set is a subset of Chunk A's committed literal. The branch-to-branch assertion is kept as a consistency check and is explicitly **not** labelled the F1 guard | Widen the shared candidate gate. The branch-to-branch assertion stays green; this one goes red. Already demonstrated by construction in the proposal's Response; **re-run here against real code** |
| 15 | **R9**: a relabelled `src` whose disk bytes match trusted upstream produces **no note at all** — the annotation's reach is exactly the complement of the change's success | Promote `src_relabelled` to a standalone finding kind → a note appears → node fails |
| 18 | **Correction 1's discrimination test**: the widened layering assertion still refuses anything but the stdlib, `config` and `security` | **Two perturbations, both required.** (a) Add `from .install import install_manifest` to a scratch copy of `lockfile.py` → `test_lockfile_module.py` must still fail. (Run for this plan already, against the *un*-widened assertion, which is how *Correction 1* was found.) (b) Add `from .insecurity import _assert_safe_write` → it must still fail. (b) is the one that discriminates the two candidate widenings: (a) fails under **both** the membership form and the loose suffix form, so (a) alone cannot show the gate was not over-widened, while (b) passes under the suffix form and fails under the membership form — measured for [E1]. A node carrying only (a) is not accepted |

**Acceptance criteria — Chunk C**

* **The only failing nodes are the two AST-attestation nodes.** Every node above
  passes; `test_lockfile_module.py` passes with C7's widening; nothing else is
  red. Any additional failure is a stop, not a known-red.
* **Every degradation path retains the finding.** Asserted by nodes 3, 4, 12 and
  13 collectively; the only removal path in the code is C4's byte-equality.
* **Mutation ledger in the commit body** — for each of nodes 1–6, 11–15 and 18:
  the deletion, the observed failure, the byte-identical restore. **A node whose
  deletion-mutant stays green is not accepted**, and is either re-shaped or
  removed with a reason.
* **C7's falsifiable check** (corrected per [E1]): `git diff
  bootstrap/tests/test_lockfile_module.py` shows a change to
  `test_lockfile_depends_only_on_stdlib_and_the_config_leaf`'s one layering
  assertion and **nothing else in the file** — the other six nodes byte-identical.
  The widened assertion is a **membership test on the module's final dotted
  component**, not a widened `endswith`; node 18's *two* perturbations prove it
  still discriminates, and (b) is what proves the widening admitted `security`
  rather than every leaf whose name ends in it.
* `python bootstrap/tests/_gate_manifest.py verify --no-collect` reports the 2
  pre-existing holds **plus** `FROZEN-MODIFIED: bootstrap/tests/test_lockfile_module.py`
  and `FROZEN-NEW: bootstrap/tests/test_fork_advisory.py`. Any entry outside that
  set is a stop.
* **Recorded as not established**: containment is a *path* property. A tampered
  file **inside** `templates_root`, or a symlinked `templates_root` itself, passes
  all three checks by construction — reproduced in the proposal's Internal review.
  Provenance of the checkout is **R1** and is not addressed here. This sentence
  goes in the code comment and in the commit body.

### Chunk D — `trusted_upstream`, the two callers, and the isolation measurement

| # | File | Change |
|---|------|--------|
| D1 | `bootstrap/_scaffold/install.py` | `trusted_upstream(cairn_root: Path) -> UpstreamSource`, beside `install_manifest()` which supplies its data. **The docstring pins A1's contract in writing**: `src_for_dst` is `install_manifest(modules=None)` — the full published catalog. The helper **takes no module list**, and must not be given one derived from the target (its lockfile's profile, its recorded module set, or anything else read from the tree under check). |
| D2 | `bootstrap/verify_integrity.py` **(frozen file #1)** | One call site: `upstream=trusted_upstream(CAIRN_ROOT)`, where `CAIRN_ROOT` is already resolved from the verifier script's own on-disk location. The note means *differs from the upstream in the verifier checkout you ran*. |
| D3 | `bootstrap/_scaffold/upgrade.py` | `cmd_upgrade`'s call site: `upstream=trusted_upstream(cairn_root)` using the `cairn_root` it already computes before dispatch — and **`None` when `--to <ref>` is given**, which yields `unconfirmed` (**R3**). |
| D4 | `bootstrap/tests/test_verify_integrity.py` **(frozen file #2)** | Call-signature update only: the one positional call becomes `forked_facade_findings(target, lock, upstream=None)`. **Assertions unchanged** — the same character as the `test_intents_tool.py` precedent already recorded in the gate manifest's phase-split targets. All *new* nodes go in the new file, never appended here. |
| D5 | `bootstrap/tests/test_fork_advisory.py` | Nodes **9, 10, 16, 17**. |

| Node | What it pins | Perturbation that must make it fail |
|---|---|---|
| 9 | **F4** — a positional two-argument call raises `TypeError` | Give `upstream` a default value |
| 10 | Both callers: `verify_integrity` honours `fork_acknowledged`; `cmd_upgrade` does **not** (upgrade is the active decision point and the tree gets no suppression lever there); `--to <ref>` yields `unconfirmed` | Make `cmd_upgrade` honour `fork_acknowledged` |
| 16 | **F5, parametric** over `hash`, `base_hash`, `src`, `fork_acknowledged`: mutating each in turn on a record whose disk bytes differ from trusted upstream leaves the finding standing at the `cmd_upgrade` caller | Key suppression on any one of the four → that parameter fails |
| 17 | **A1 structurally**: `inspect.signature(trusted_upstream)` takes exactly one parameter (`cairn_root`), and its `src_for_dst` equals the destination→source map of `install_manifest(modules=None)` | Add a `modules` parameter, or narrow the map → node fails. This is the closest thing to a *construction* for A1; the rule itself remains a written rule enforced by this node and by review, and this plan does not claim otherwise |

**Acceptance criteria — Chunk D**

* All nodes green; the only failing nodes remain the two AST-attestation ones.
* **The isolation measurement, taken through a channel the change does not
  control.** In a throwaway `git worktree` at this commit — so the sibling's edits
  are absent by construction — verify the engine against the AST baseline **read
  from git**, not from the working tree:

  ```
  $ git worktree add <scratch>/iso <this-commit>
  $ git show c3d5bd9:bootstrap/tests/fixtures/scaffold_ast_baseline.json > <scratch>/baseline.json
  $ python bootstrap/tests/_ast_attest.py verify <scratch>/baseline.json <scratch>/iso/bootstrap/_scaffold/*.py
  ```

  **Falsifiable target: exactly 3 CHANGED** — `FunctionDef:forked_facade_findings`,
  `FunctionDef:format_forked_facade_warning`, `FunctionDef:cmd_upgrade` — **0
  MISSING, 0 DUPLICATE**, `FunctionDef:_facade_engine_dir` **unchanged**, and
  exactly **two** additional non-`Import:` NEW notes over Chunk A's captured
  baseline. **A 4th CHANGED symbol is a stop-and-explain, not a re-run.** Reading
  the baseline from the working tree instead of from `c3d5bd9` is a review
  finding: the working-tree copy is the file Chunk R rewrites.
* `python bootstrap/scaffold.py --manifest` — **unchanged**: 96 lines, 95 data
  rows, `as_of 2026-08-03`, re-measured for this plan. This plan installs nothing
  new into an adopter tree and adds no manifest row.
* **D4's falsifiable check**: the diff on `bootstrap/tests/test_verify_integrity.py`
  shows only an added keyword argument. Any changed assertion on that file is a
  stop.
* **The self-host smoke check, and its stated limit.**
  `python bootstrap/verify_integrity.py --target .` emits **zero** fork notes
  (today: two). **This is a demonstration, not evidence of target-independence**:
  on Cairn's tree `CAIRN_ROOT` and the target are the same directory, which is the
  degenerate configuration. The fixture matrix is the evidence.

### Chunk E — documentation, residual homes, changelog

| # | File | Change |
|---|------|--------|
| E1 | `bootstrap/UPGRADE.md` | A short subsection stating the advisory's three note kinds and what each means, plus the residual homes the proposal assigns to this document: **R1** (the note prints the root and ref it compared against, so an operator sees whose bytes decided it), **R3** (`--to <ref>` is `unconfirmed`), **R4** (destinations absent from the trusted manifest keep `unconfirmed` semantics), **R9** (`src_relabelled`'s reach). |
| E2 | `bootstrap/_scaffold/SECURITY_MUTATIONS.md` | **One sentence** in the Class C section recording that the follow-on is unclaimed by any of the four successors and naming R7's three triggers. Its wording follows the Maintainer's disposition of deferred question 1; if that is unresolved when this chunk runs, the sentence records the state as unresolved and names the question, rather than asserting a disposition. |
| E3 | `CHANGELOG.md > Unreleased > Fixed` | One line for the corrected advisory semantics; one for the remediation string **if Chunk B ran under this plan** (otherwise the standalone commit owns it). |

**Acceptance criteria — Chunk E**

* Every residual has a home that is **not** this plan and **not** the proposal:
  R1 → the note string + `bootstrap/UPGRADE.md` + a `dev/PLANNING.md` row opened
  at plan-open; R2 → the existing comment at the backfill site; R3, R4, R9 →
  `bootstrap/UPGRADE.md` + their pinning nodes; R5 → node 8; R6, R10 → C6's
  comments; R7 → E2's sentence + a `dev/PLANNING.md` row; R8 → claimed by
  `gate-claims-vs-enforcement`.
* `python scripts/check_cairn.py` green over the changed prose.
* `python scripts/claim_check.py <file>` clean on each Markdown file this chunk
  edits — **one file per invocation** (the checker exits 2 on more than one path).
* `python scripts/quality_gate.py --sub neutrality` green — the new prose names no
  AI vendor or model.
* **Confirm each doc named here was actually updated.** Drift gates catch drift,
  not absence.
* **The implementing agent stops here, and the stop is a deliverable** (per
  [E2]). Chunk E touches no engine file, so the suite state must be **unchanged
  from Chunk D** — `python -m pytest bootstrap/tests` fails exactly the two
  AST-attestation nodes and nothing else. **Re-run and recorded at this chunk, not
  inherited from Chunk D**: a doc-only chunk is exactly where an unnoticed failure
  from the batched sibling would be mistaken for known-red. Any other failing node
  is a stop.
* **The readiness condition is written here, because Chunk R is not an agent's to
  enter.** Chunk R's fence ends the agent's work at "Chunk E plus a stated
  readiness condition", and Chunk R states what that condition names — but an
  agent must not perform a step in Chunk R, so the condition is authored in **this
  chunk's commit body**: this plan's last engine commit sha (Chunk D), the
  isolated `3 CHANGED / 0 MISSING / 0 DUPLICATE` measurement taken there and the
  three symbol names, and the statement that the batched ceremony additionally
  waits on `profile-parse-fail-open`'s last engine commit. **The agent does not
  measure the union** — the union is formed by the Maintainer at Chunk R from two
  per-plan isolated measurements, and an agent-measured union would be taken from
  the shared working tree, which *Correction 5* item 3 forbids.

### Chunk R (MAINTAINER-ONLY) — the batched re-anchor ceremonies

> **An implementing agent must not perform any step in this chunk.** Both
> ceremonies are the Maintainer's, for the reason `bootstrap/REANCHOR_RUNBOOK.md`
> states in its own words: an implementer must not bless its own gate. The
> implementing agent's work **ends at Chunk E plus a stated readiness condition**.
> The agent may *prepare* and *dry-run* the AST correction script — that is the
> `lockfile-provenance-fields` precedent — but the Maintainer runs the real one
> and authors the commit.

1. **Confirm the sibling has landed.** Per the Decision, this ceremony is batched
   with `profile-parse-fail-open`. Chunk R does not run until that plan's engine
   chunks are in the tree, and the readiness condition names its last engine
   commit.
2. **The AST baseline re-anchor** (`bootstrap/tests/fixtures/scaffold_ast_baseline.json`)
   — **not** `bootstrap/REANCHOR_RUNBOOK.md` Phase 0/4; the Maintainer-run,
   dry-run-verified direct-correction script established by
   `lockfile-provenance-fields`. The self-service `update-symbol` path is
   unavailable here (its allowlist admits four registry symbols, none of them
   this plan's). **The combined falsifiable target is the union of two disjoint
   per-plan targets** — this plan's 3 CHANGED (Chunk D) and the sibling's, each
   measured in isolation against the baseline at `c3d5bd9` before the ceremony. A
   symbol outside the union is a stop.
3. **The frozen-set decision.** Three frozen files are modified by this plan
   (*Correction 1*) and two more were already modified by `7066489`
   (*Correction 2*). Whether to re-pin `bootstrap/tests/fixtures/gate_manifest.json`,
   and whether the pre-existing two are cleared in the same act or routed to
   `gate-claims-vs-enforcement`, is the Maintainer's call. **This plan does not
   re-pin the manifest** and records the delta instead.
4. **Green.** `python -m pytest bootstrap/tests` returns to 0 failed / 0 skipped
   after the ceremony. That is the end of the red window opened at Chunk B.

## Acceptance criteria

Per-chunk criteria are above. These are the plan-level deliverables.

* **Tests that must pass.**
  * `python -m pytest bootstrap/tests` — the whole suite, green, **0 skipped / 0
    xfailed**, under the canonical interpreter (3.13.13). Baseline **1601 passed,
    0 failed, 0 skipped** at HEAD `05515df` — measured for this plan, 150.69s.
    Collection grows by exactly the new nodes and drops none. Green at Chunk A;
    red on exactly the two AST-attestation nodes from Chunk B to Chunk R; green
    after Chunk R.
  * `bootstrap/tests/test_fork_advisory.py` — the new module, 18 nodes, each
    exercising a **public** path (`forked_facade_findings`,
    `format_forked_facade_warning`, `trusted_upstream`, and
    `verify_integrity.verify` end to end) rather than a helper.
  * **Every node shown non-vacuous by mutation**: remove the check, confirm the
    node fails, restore the source byte-identical. The ledger goes in each chunk's
    commit body. A node whose author cannot name a future state in which it fails,
    and has not run that perturbation, is not accepted.
* **Doc updates that must land.** All hand-authored: `bootstrap/UPGRADE.md`,
  `bootstrap/_scaffold/SECURITY_MUTATIONS.md`, and
  `CHANGELOG.md > Unreleased > Fixed`. No generated docs and no snippet-synced
  blocks are involved.

  <!-- cairn:slot acceptance-doc-tooling -->
  Cairn's doc surface is mostly hand-authored Markdown read on GitHub;
  the doc tooling is drift-prevention, not generation:
  - **Snippet-sync** — `python scripts/sync_doc_snippets.py` pulls
    fenced blocks from runnable example sources into docs; update the
    source, then run the sync (never hand-edit a synced block).
  - **Prose-integrity gate** — `python scripts/check_cairn.py` resolves
    every internal Markdown link / anchor and every claim-path; it is
    the doc smoke for any Markdown change.
  - **Link check** — `python scripts/link_check.py` for the broader
    cross-reference sweep.
  There is no schema-render generator; a plan that introduces one names
  its source + render command here.
  <!-- cairn:end acceptance-doc-tooling -->
* **Examples / smoke checks required.**
  `python bootstrap/verify_integrity.py --target .` — zero fork notes (today:
  two), with its degeneracy stated; `python bootstrap/scaffold.py --manifest` —
  unchanged at 95 data rows across 96 lines; the isolated AST measurement in
  Chunk D; `python bootstrap/tests/_gate_manifest.py verify --no-collect` at each
  chunk.
* **Inbound path-link updates.** None expected: `dev/PLANNING.md` and
  `dev/NEXT_SESSION.md` refer to plans by filename stem, not path link, so the
  archive-move needs no edit there. Confirm at archive time rather than assume.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants, each with the chunk and node that enforces it.**
  * **F1** — the new finding set is a subset of today's. Chunk A's committed
    oracle + node 14. The branch-to-branch check is a consistency aid and is
    explicitly not the guard.
  * **F2** — the trusted upstream is never derived from `target` or from lock
    data. Nodes 5 and 17.
  * **F3** — the advisory never changes an exit code. Node 8 (Chunk A), which is
    also **R5**'s mechanical trigger: the moment someone makes the advisory
    blocking, node 8 fails and the target-controlled opt-out must be re-decided in
    the same change.
  * **F4** — a caller cannot omit the comparison source. Node 9.
  * **F5** — suppression provenance: a finding is removed by exactly one
    condition, byte-equality between two validated reads. Nodes 11 and 16.
  * **F6** — read containment on both sides; a refusal never suppresses. Nodes 3
    and 13.
* **Public-path → test mapping.** Four public paths, each with a through-test
  rather than a helper test: `forked_facade_findings` (nodes 1–6, 11–16),
  `format_forked_facade_warning` (nodes 5, 15, and B2), `trusted_upstream`
  (node 17), `verify_integrity.verify` end to end (nodes 8, 10, 11). The test
  module is cited as a code span rather than a relative markdown link because it
  does not exist yet; it is registered under *Proposed paths*, and the link form
  is adopted at code review once the file resolves.
* **The operand inventory (B1) is the completeness artifact**, and this plan
  sequences a pin for every row: O1 `templates_root` → F2/R1; O2 `src_for_dst` →
  node 17; O3 upstream bytes → C2; O4 target-side bytes → C4/nodes 11, 16;
  O5 `dst` → C3/node 13; O6 `hash`/`base_hash` → node 16 + R10; O7 `src` →
  nodes 5, 15 + R9; O8 `fork_acknowledged` → node 10 + R5; O9 version skew →
  node 2; O10 engine presence → node 6. **A reviewer who finds an eleventh
  operand has found a real gap in the central artifact** — the proposal's author
  named that as the attack they most want made, and this plan does not close it.
* **Failure modes — all fail-loud.** Every degradation path (no trusted map row,
  missing source, missing destination, containment refusal on either side,
  `--to <ref>`, `upstream=None`) **retains** the finding as `unconfirmed`. The one
  deliberately open edge is that a containment refusal is caught inside
  `lockfile.py` so a malformed templates tree degrades the advisory instead of
  aborting the verifier — an intentional choice on an advisory-only surface, and
  the only one.
* **Edge cases handled.** Source side: `src_rel` absolute or with `..`; source
  missing; source a symlink; source with a symlinked parent; `dst` absent from the
  trusted map. Destination side: `dst` absolute or with `..`; `dst` missing; `dst`
  not a regular file; `dst` a symlink; `dst` with a symlinked parent; `dst`
  non-`.py`; unresolvable `target`. Both: version skew in both directions; lock
  `src` disagreeing with the trusted map; a target-planted templates tree; facade
  present with engine absent; engine directory present but holding no `.py`;
  record with no `base_hash`; `upstream=None`.
* **Known omissions, stated rather than implied.** (a) **The nominated attack is
  still unattacked** — *"the trusted map is not actually trusted"*. An External
  round and an Internal round both stopped short of it; two same-family reasoners
  failing to break something is weaker evidence than it looks. A1 remains a
  written rule enforced by node 17 and by review, not a construction. (b) **No
  measurement on a real adopter tree.** Cairn's `templates/` is co-located with
  its install, so the self-host run is the degenerate configuration; the fixture
  matrix is the evidence. If, in practice, real adopter trees almost never resolve
  a trusted upstream, this change relabels the noise rather than removing it — the
  proposal's own recovery is to measure before the final chunk. (c) **No sweep for
  other consumers of `base_hash`** that inherit the same ratchet. Named in the
  proposal, still not measured, and not measured here. (d) **Candidate selection**
  remains lock-derived (R10). (e) **A concurrently-mutating templates tree** — the
  read is not atomic, and the advisory is not a security boundary.

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

**Plan-specific gates.** Run under the canonical interpreter
(`~/conda_envs/lhm/bin/python`, 3.13.13) with `PYTHONDONTWRITEBYTECODE=1` — a
different Python minor silently changes AST-attestation digests, which
`bootstrap/DEPENDENCY_BUDGET.md` warns about and which this repository has been
burned by before.

* **The AST attestation** — fired by the suite as
  `bootstrap/tests/test_ast_attest.py`, and run standalone in isolation at
  Chunk D. **29 tests pass, 174 baselined symbols, 0 CHANGED / MISSING /
  DUPLICATE at HEAD `05515df`** — re-measured for this plan.
* **The gate manifest** — `python bootstrap/tests/_gate_manifest.py verify
  --no-collect`, **run by a human** (*Correction 3*). For a check that does not
  read its expectation out of the tree being checked, use the external anchor
  form: `--anchor-ref e45e1fc --trusted-repo <a clean clone>`. Verified for this
  plan that `e45e1fc` is reachable from HEAD and that its committed manifest is
  byte-identical to the working-tree copy.
* **The engine security gates** — `bootstrap/tests/test_security_lint.py` (Bandit
  over the engine package) and `bootstrap/tests/test_security_leaf.py`. This
  change adds no `subprocess`, no `eval`, no new adopter-tree write, and no
  non-stdlib dependency, so `_GUARDED_WRITE_FUNCS` is untouched. **Assert it,
  don't assume it** — both modules are in the suite.
* **The install-contract assertion** — `python bootstrap/scaffold.py --manifest`,
  diffed against the pre-change output. **Expected empty.**
* **The mutation ledgers** — per chunk, in the commit body: the deletion, the
  observed node failure, the byte-identical restore.

### Where each verification input arrives from, and why it is not the thing under verification

The defect class this plan exists to close has produced four instances in this
repository in one week. The same discipline applies to the plan's own evidence.

| Verification step | Input | Channel | Why it is not the artifact |
|---|---|---|---|
| F1 subset (node 14) | the pre-change finding set | a throwaway `git worktree` at a **named commit** predating every engine edit; pasted in as a committed literal | code at that commit cannot be influenced by edits that do not exist yet; a later re-paste is a review-visible diff |
| AST attestation (Chunk D) | the baseline digests | `git show c3d5bd9:<baseline>` into a scratch file | the working-tree baseline is the file Chunk R rewrites; reading it from the tree lets the change bless itself |
| AST attestation (Chunk D) | the module set | a `git worktree` at this plan's own last engine commit | excludes the batched sibling's edits by construction, not by an implementer's care |
| gate manifest | the expected frozen hashes | `verify --anchor-ref e45e1fc --trusted-repo <clean clone>` | the working-tree manifest is editable by the same actor; the anchor is an immutable git object and the tool runs from a checkout this change did not touch |
| trusted upstream, at runtime | `src_for_dst` | `install_manifest(modules=None)` — four in-memory literals in `bootstrap/_scaffold/config.py`, zero filesystem reads | the target contributes only `dst`, which is also the path being read off disk, so it cannot select bytes independently of the file it is about |
| upstream bytes, at runtime | the template file | `templates_root` resolved from the **caller's own** on-disk location | never from `target`, never from the lockfile's `src` |
| target-side bytes, at runtime | the facade | `read_bytes(target / dst_rel)` after containment checks | target-supplied **and correctly so** — this is the thing under check. It may select *what* is examined; it may never decide that what was examined is clean |
| suite baseline | 1601 passed / 0 failed / 0 skipped | `python -m pytest bootstrap/tests` at HEAD `05515df`, measured for this plan | pre-change, pinned to a commit, not quoted from a session summary |
| self-host smoke | 2 → 0 fork notes | `bootstrap/verify_integrity.py --target .` | **degenerate — `CAIRN_ROOT` and the target are the same directory on this tree.** Demonstration only. The fixture matrix is the evidence |

**Note on doc gates**: drift gates (broken references, stale renders,
snippets that diverged from their source) catch **drift**, not
**absence** of new doc updates. Confirm each doc named in Acceptance
was actually updated; the gates don't enforce that.

## Plan review — the brief

*Required — External, security lens. Implementation does not start until a review
has landed under this heading.* The tier is not the author's to set: the
superseding `identity-not-name` Decision mandates it, and both prior rounds
disclaim discharging it — the Internal round says so in terms.

> **The landed review appends here as a `### Plan review -- <reviewer> --
> YYYY-MM-DD` sub-heading** (plus a `### Sharpening` sub-heading if it raised
> findings). **Do not rename this heading to a bare `## Plan review`** — the
> lifecycle checker matches a section *kind*, not a review, so a bare heading
> would report the gate satisfied before any review existed.

**Why the tier is right independent of the mandate.** `bootstrap/_scaffold/` is on
`AGENTS.md`'s high-risk-surface list, which is a Security-Review trigger by the
letter of the rule. And the defect class has a *measured* same-author blind spot
in this exact lineage: [IDN1], [IDN4] and [I1] are three instances of one shape,
the third written **into the proposal that exists to close the class**. An
Internal read is by construction the same reasoning that produced the error.

**Five questions this review should aim at**, in priority order. The first four
are the ones the proposal's own second revision nominated; the fifth is this
plan's.

1. **Is the target-side operand pinned to bytes read from disk at *both*
   callers** (C4 / F5 / nodes 11, 16)?
2. **Is the destination join containment-validated** (C3 / F6 / node 13), and does
   the refusal path retain rather than suppress?
3. **Is F1's oracle external to the function under test** (Chunk A / node 14), and
   does the *fixture design* make each perturbation discriminating — specifically,
   are nodes 3 and 13 built so that deleting the guard causes a wrong
   **suppression**, not merely a lost message?
4. **Can the trusted map's output be influenced by the target?** This is the
   attack the proposal nominates as its own most likely failure and **no reviewer
   has yet attempted it**. Two same-family reasoners have failed to break it,
   which is weaker evidence than it looks.
5. **Is *Correction 1* the right disposition?** The design forces a third
   frozen-file edit, and that edit *widens an assertion on a gate file*. Is
   widening the layering assertion in the open better than inlining a second copy
   of the containment checks in `lockfile.py`? This is the one point at which this
   plan departs from the accepted gate accounting, and it is the right place to
   attack it.

**Channel discipline over every step.** For each verification step in Chunks A, C
and D, name the channel each input arrives by and show it is not the thing being
verified. The table above is the plan's own answer; the reviewer's job is to find
the row it is wrong about or the row it is missing.

**What the reviewer should not spend attention on.** The design itself — the
per-caller trusted source, the trusted-map-not-`src` decision, the three note
kinds, F1–F6, the Class C disposition — is settled by the Decision and is not
re-opened by this plan. A finding that the design should be reshaped is a finding
against the Decision, not against this plan, and should say so.

**The stopping rule.** A finding is one of exactly two things. Either it names a
violation of an invariant F1–F6 or an operand row in B1's inventory — then it is a
bug against a stated property and the fix is bounded. Or it names a property *not*
in F1–F6 and an operand *not* in B1 — then the specification was incomplete, the
row is added, and **every earlier step is re-swept against it**. The second branch
is the expensive one and is supposed to be; it is the only branch that makes the
inventory converge.

## Code review — the brief (no review has landed)

*Filled in after implementation commits land.* Per `doctrine/plans.md`, the
reviewer is **not** the implementing agent, the section is append-only, and a
clean final review carries a falsification ledger and a coverage line. The landed
review appends here as a `### Code review -- <reviewer> -- YYYY-MM-DD`
sub-heading; the heading above is shaped the same way as the plan-review one, and
for the same reason.

Four checks this plan asks its code reviewer to **run**, not read:

* **Re-run the operand attack** against the landed code: a record whose `hash`
  equals the trusted template's hash while the on-disk bytes are hostile, at
  **both** callers. The note must survive. A review that asserts the fix without
  re-running it does not close it — that is this lifecycle's recorded lesson.
* **Re-run one perturbation from each chunk's ledger**, chosen by the reviewer,
  not by the implementer. Confirm in particular that nodes 3 and 13 fail on
  *suppression*, not on a message change.
* **Confirm the F1 oracle literal matches the pre-change commit it claims.**
  Regenerate it from that commit in a throwaway worktree and diff. A re-pasted
  oracle is a review-visible diff by design; this is the review that sees it.
* **Confirm the C7 widening did not widen further.** Diff
  `bootstrap/tests/test_lockfile_module.py` and run node 18's perturbation
  independently.

## Lasting-truth migration

*Filled in at archive time.* Per `doctrine/plans.md`, the archive commit body
carries the literal `Follow-ups migrated to:` block naming where each deferred
item went, so the migration is auditable from the commit log alone — and the plan
does not archive until every deferred follow-up has a durable home outside it.

The homes are pre-declared here so archive time is bookkeeping rather than
recall: **R1** → the note string, `bootstrap/UPGRADE.md`, and a `dev/PLANNING.md`
row opened at plan-open (including the `--cairn-root` clause, per B7);
**R2** → the existing comment at the `--finalize` backfill site;
**R3**, **R4**, **R9** → `bootstrap/UPGRADE.md` plus their pinning nodes;
**R5** → node 8, which fails the moment the advisory becomes blocking;
**R6**, **R10** → comments at their call sites in `bootstrap/_scaffold/lockfile.py`;
**R7** → one sentence in `bootstrap/_scaffold/SECURITY_MUTATIONS.md`'s Class C
section plus a `dev/PLANNING.md` row opened at plan-open;
**R8** → claimed by `gate-claims-vs-enforcement`, which records the hand-off by
name.

**Three items that are not residuals and must not be archived away as if they
were:** the **condition-3 sequencing choice** (the Maintainer's, and Chunk B does
not execute without it); the **two pre-existing `FROZEN-MODIFIED` entries** from
`7066489`, which this plan surfaced and does not claim; and the **`Touches`-line
mutability question**, deferred Maintainer question 2, raised by this lifecycle's
own [I5].

Per the [Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home outside the
plan.

This section is append-only once written.

## Plan review -- Gemini Flash (External, security lens) -- 2026-08-03

**Steelman.** This plan successfully closes defect class 1 ("the artifact under verification must not supply the material used to verify it") for the fork advisory detector. By forcing callers to supply a trusted `upstream: UpstreamSource` resolved from caller context rather than reading lockfile `src`/`base_hash` fields, it prevents target-controlled lockfiles from suppressing fork detection.

### Concerns

* **[E1] Layering assertion widening (`bootstrap/tests/test_lockfile_module.py`).**
  Correction 1 correctly notes that `lockfile.py` importing `bootstrap._scaffold.security` for `_assert_safe_write` widens the leaf dependency allowed set from `{config}` to `{config, security}`. Chunk C7/Node 18 must strictly test that `lockfile.py` still refuses imports outside `{config, security}`.
* **[E2] Coordinated AST re-anchor with `profile-parse-fail-open`.**
  As direct by Maintainer decision, Chunk R is Maintainer-only and batched with `profile-parse-fail-open`. Implementing agents must stop at Chunk E and verify that the only AST failures are the expected engine modifications.

### Covered

* **Defect Class 1 Structural Independence Verification**:
  Verified that `forked_facade_findings` requires keyword-only `upstream: UpstreamSource | None` and reads bytes directly from disk (`read_bytes(target / dst_rel)`) rather than relying on lockfile `hash` or `base_hash` fields.
* **Falsifiable AST Target Accounting**:
  Verified that this plan introduces exactly 3 CHANGED symbols in `bootstrap/_scaffold/` (`FunctionDef:forked_facade_findings`, `FunctionDef:format_forked_facade_warning`, `FunctionDef:cmd_upgrade`).

### Not covered / low confidence

* Provenance and authenticity of the caller's trusted upstream checkout itself is out of scope for this plan and relies on `release-authenticity`.

### Recommendation

**READY FOR IMPLEMENTATION.** The plan's design, containment checks (C2/C3), operand pinning (C4), and Maintainer ceremony boundaries (Chunk R) are verified and sound.

## Response to plan review -- Claude (author) -- 2026-08-03

**Model**: Claude Opus 5

**Both accepted; the plan changed for both.** A `READY FOR IMPLEMENTATION`
verdict does not make a finding informational — this lifecycle has no severity
floor below which a finding stops needing a disposition, and the two findings
here are the two the plan's own review brief nominated as its weakest points
(question 5, *Correction 1*; and *Correction 5*'s batched red window). Neither
was disposed as "already covered", because in both cases I went to the code and
found the plan's contract narrower than its prose implied.

The disposition below is written after independent verification, not after
reading the review. What the verification changed: **[E1] is not a restatement of
node 18.** Node 18 as written would have passed while admitting exactly the
over-widening [E1] asks the gate to refuse. That is the finding.

### [E1] — layering assertion widening — **ACCEPTED**

*The finding.* `bootstrap/_scaffold/lockfile.py` importing
`bootstrap._scaffold.security` for `_assert_safe_write` widens the leaf
dependency admitted set from `{config}` to `{config, security}`; C7 / node 18
must strictly test that `lockfile.py` still refuses imports **outside**
`{config, security}`.

*What I verified, and why "already covered" would have been wrong.* The plan
already *states* that requirement — the node 18 row reads "the widened layering
assertion still refuses anything but the stdlib, `config` and `security`". So the
lazy disposition was available. It is wrong, because the assertion is not the
shape the plan says it is. Read at HEAD,
`bootstrap/tests/test_lockfile_module.py:49-59` is a **suffix predicate**, not an
allowed set:

```python
if isinstance(node, ast.ImportFrom):
    mod = node.module or ""
    if mod.startswith("bootstrap") or node.level > 0:
        assert mod.endswith("config"), f"lockfile imports {mod!r} (level={node.level})"
```

There is no set literal to "add one module name to", so C7's stated falsifiable
check — *"exactly one added module name in one allowed set"* — was not a check an
implementing agent could satisfy or a reviewer could run. Worse, the widening the
prose implies is the suffix form, and I measured what that admits. Running the
predicate verbatim under the canonical interpreter
(`/Users/kendal30/conda_envs/lhm/bin/python3.13`), over four synthetic import
lines, against the current assertion and against the naive
`endswith(("config", "security"))` widening:

```
design import   current        -> FAILS (lockfile imports 'security' (level=1))
design import   naive-widened  -> PASSES
node 18 pert.   current        -> FAILS (lockfile imports 'install' (level=1))
node 18 pert.   naive-widened  -> FAILS (lockfile imports 'install' (level=1))
near-miss       current        -> FAILS (lockfile imports 'insecurity' (level=1))
near-miss       naive-widened  -> PASSES
near-miss 2     current        -> PASSES
near-miss 2     naive-widened  -> PASSES
```

Three things fall out, and they are the whole finding:

1. **The suffix widening over-widens.** `"insecurity".endswith("security")` is
   `True`, so a `.insecurity` leaf — not in `{config, security}` — is admitted.
   That is precisely the failure [E1] names.
2. **Node 18's perturbation does not discriminate.** Its `from .install import
   install_manifest` fails under *both* candidate widenings (rows 3 and 4 above).
   A node that goes red either way cannot show which widening landed. Node 18 as
   written was therefore a non-answer to [E1] dressed as one.
3. **A pre-existing looseness, surfaced not fixed.** Row 7: `.fakeconfig` passes
   the assertion **today**. The membership form removes it as a side effect. This
   makes the gate strictly narrower, never wider, so it cannot mask a layering
   violation; I record it rather than let it appear in the C7 diff unexplained.
   I did not touch the file.

Also confirmed, since the finding rests on them: `_assert_safe_write` exists at
`bootstrap/_scaffold/security.py:26`, so the design's import is real and not
hypothetical; and `test_lockfile_module.py`'s seven collected node ids sit in
`bootstrap/tests/fixtures/gate_manifest.json:780-786`, so *Correction 1*'s
frozen-set claim holds — this is an edit to a frozen gate file, which is why the
shape of it matters at all.

*Plan change.* Three amendments, all inside this plan's existing scope:

* **Correction 1** — the "falsifiable check the Maintainer is owed" sentence
  replaced with a corrected paragraph: the assertion is a suffix predicate, the
  widened form is **membership of the module's final dotted component in
  `{"config", "security"}`**, and the `.insecurity` / `.fakeconfig` measurements
  are stated inline.
* **Chunk C, row C7** — the change description now names the target node, the
  existing predicate form, the required membership form and its reason, and pins
  "the other six nodes in the file are not touched" (7 nodes collected; the
  scratch run in *Correction 1* shows `1 failed, 6 passed`).
* **Chunk C, node 18 row and the C7 acceptance criterion** — node 18 now carries
  **two** perturbations, (a) `.install` and (b) `.insecurity`, with the recorded
  reason that (a) alone cannot distinguish the two widenings and that a node
  carrying only (a) is not accepted. The acceptance criterion drops the
  unsatisfiable "one added module name in one allowed set" and states the diff
  boundary and the membership requirement instead.

No scope moved. The design is unchanged, the security leaf does not grow, and the
`{config, security}` disposition *Correction 1* argues for is the same one — only
its enforcement is now real.

### [E2] — batched Maintainer-only AST re-anchor: stop at Chunk E — **ACCEPTED**

*The finding.* Chunk R is Maintainer-only and batched with
`profile-parse-fail-open`; implementing agents must stop at Chunk E and verify
that the only AST failures are the expected engine modifications.

*What I verified.* Most of this is genuinely covered, and I will cite it rather
than re-accept it. The fence exists — Chunk R opens *"An implementing agent must
not perform any step in this chunk"*. The known-red invariant exists —
*Correction 5* item 1: *"between Chunk B and Chunk R, the only failing nodes
attributable to this plan are the AST-attestation nodes. Any other failure is a
stop, not a known-red."* And it is enforced at the two engine chunks: Chunk C's
*"The only failing nodes are the two AST-attestation nodes … Any additional
failure is a stop, not a known-red"*, and Chunk D's *"All nodes green; the only
failing nodes remain the two AST-attestation ones"* plus its isolated
`3 CHANGED / 0 MISSING / 0 DUPLICATE` measurement in a throwaway worktree.

What is **not** covered is the chunk [E2] actually names. I read Chunk E's
acceptance criteria against the finding: all five bullets are doc gates —
residual homes, `check_cairn.py`, `claim_check.py`, `--sub neutrality`, and
"confirm each doc was actually updated". **Chunk E states nothing about the suite
state and produces no handoff.** So the last chunk an implementing agent runs is
the one chunk with no red-set check on it. That is a real gap, and it is the
gap [E2] points at.

It compounds with a second one. Chunk R's fence says the agent's work *"ends at
Chunk E plus a stated readiness condition"* — but the only text describing that
condition is **inside Chunk R**, at step 1, which the same fence forbids the agent
to enter. The plan asked for a deliverable and then put its specification behind
a door the deliverer may not open.

A doc-only chunk is also the *worst* place to inherit a red set rather than
re-measure it. Chunk E changes no engine file, so an implementing agent has every
reason to assume Chunk D's failure list still holds — while the batched sibling
`profile-parse-fail-open` may have landed engine edits into the shared working
tree in between. An unrelated failure arriving through that channel is exactly
what "known-red" would swallow.

*Plan change.* **Chunk E acceptance criteria** gain two bullets:

* the suite state must be **re-run and recorded at Chunk E**, not inherited —
  exactly the two AST-attestation nodes red, any other failing node a stop, with
  the sibling named as the reason a doc-only chunk still re-measures;
* the **readiness condition is authored in Chunk E's commit body** — this plan's
  last engine commit sha, the isolated 3-CHANGED measurement and its three symbol
  names, and the statement that the ceremony additionally waits on the sibling's
  last engine commit. It states explicitly that the agent **does not measure the
  union**: the union is the Maintainer's at Chunk R, and an agent-measured union
  would come from the shared working tree, which *Correction 5* item 3 forbids.

Nothing was added to Chunk R, and no step moved out of it. The change makes the
agent's stopping point produce evidence instead of just stopping.

### On the reviewer's "Not covered / low confidence" note

The note is right, and it is genuinely out of scope rather than a gap: *"[the]
provenance and authenticity of the caller's trusted upstream checkout itself is
out of scope for this plan and relies on `release-authenticity`."* That is
residual **R1**, fenced in *Scope* in the same terms — *"This change moves the
comparison from target-controlled to caller-controlled; it does not move it to
cryptographically anchored. That is `release-authenticity`'s job"* — and stated
again in Chunk C's "Recorded as not established" criterion, which requires the
limit to appear in the code comment and the commit body. **No new follow-up row is
needed**: R1 already has three declared durable homes in *Lasting-truth
migration* (the note string, `bootstrap/UPGRADE.md`, and a `dev/PLANNING.md` row
opened at plan-open), so it cannot be archived away silently.

One thing the reviewer did not reach, recorded because the plan nominates it as
its own most likely failure: **review question 4 — "can the trusted map's output
be influenced by the target?" — remains unattacked**. This External round did not
attempt it either; its "Covered" section verifies the *signature and operand*
(that `upstream` is keyword-only and that the target-side operand is
`read_bytes`), which is F4/F5, not the trusted-map question. The plan already
states this under *Known omissions* (a), and node 17 plus review remain the only
enforcement. I am not proposing another round for it — but the code reviewer
should be pointed at it, and this Response is the record that three reasoners have
now declined the attack rather than made it.


## Code review -- Antigravity (External, security lens) -- 2026-08-04

**Steelman.** Implementation commit `9bd6752` delivers `fork-advisory-semantics.md` Chunks A and C–E. The core defect—where the fork advisory used lockfile-supplied hashes (`hash != base_hash`) to verify the file, allowing the candidate under verification to supply its own verification material—is robustly resolved. `forked_facade_findings` now requires a keyword-only, no-default `upstream: UpstreamSource` parameter, and performs exact byte comparison (`disk_bytes == upstream_bytes`) between two validated reads (`_guarded_read`). Both source and destination joins undergo containment checks (`_assert_safe_write`). Degradation paths (missing files, containment failures, un-materialized `--to <ref>`) correctly degrade to `unconfirmed` notes rather than suppressing findings.

### Specific User Directives Audit

1. **Restraint on Chunk B (Remediation String)**:
   - Chunk B was deliberately skipped because `identity-not-name` condition 3 required an explicit Maintainer amendment to alter `format_forked_facade_warning`'s remediation string.
   - **Verification**: This restraint was **100% correct**. Under Cairn governance doctrine, implementing agents cannot execute Maintainer-gated chunks without explicit authorization. The remediation string remains unchanged as expected.
2. **Residual R10 (Lock-derived Candidate Selection)**:
   - Verified lines 479–486 of `bootstrap/_scaffold/lockfile.py`: candidate selection still checks `if not (isinstance(h, str) and isinstance(base, str) and h != base): continue`.
   - **Verification**: As documented in the plan, candidate selection remains lock-derived while `base_hash` is a lockfile field, while the *verdict* itself is strictly determined by on-disk vs upstream byte comparison (F5/F6). The explicit comment at line 479 records this residual home accurately.

### Concerns

* **[E1] Supervised gate manifest and AST re-anchor requirements.**
  `bootstrap/verify_integrity.py` and `bootstrap/tests/test_verify_integrity.py` are modified frozen files. The AST attestation suite (`test_ast_attest.py`) is red by design until the Maintainer performs the batched re-anchor ceremony (Chunk R) alongside `profile-parse-fail-open`.

### Covered

* **Empirical Test Suite Execution**:
  - Executed `bootstrap/tests/test_fork_advisory.py`: 36 passed in 1.69s.

```
$ ~/conda_envs/lhm/bin/python -m pytest bootstrap/tests/test_fork_advisory.py
============================== 36 passed in 1.69s ==============================
```

* **Target-side Operand Verification (F5)**:
  - Verified `lockfile.py` lines 525–539: `disk_bytes` is read directly from `target_root / dst_rel` via `_guarded_read` and compared to `up_bytes`. Lockfile hashes are not used as operands.

* **Claim-check Verification**:
  - `claim_check.py`: verified clean output on `dev/plans/fork-advisory-semantics.md`.

```
$ ~/conda_envs/lhm/bin/python scripts/claim_check.py dev/plans/fork-advisory-semantics.md
claim_check: dev/plans/fork-advisory-semantics.md -- 1 path(s) exempted by claim-check-allow:
  dev/plans/fork-advisory-semantics.md: exempted `bootstrap/tests/test_fork_advisory.py` via claim-check-allow glob `bootstrap/tests/test_fork_advisory.py`
claim_check: dev/plans/fork-advisory-semantics.md -- OK, no claim-check flags.
```

### Not covered / low confidence

* Authenticating the caller's trusted upstream checkout itself is out of scope for this plan and relies on `release-authenticity` (tracked under residual R1).

### Recommendation

**SHIP / PASS CODE REVIEW.** The implementation of `fork-advisory-semantics.md` is complete, verified, and adheres strictly to governance fences.


### Figure reconciliation -- Antigravity -- 2026-08-04

- **Previously reported**: No full test suite run reported (focused unit test run only).
- **Reconciliation baseline** (`7bb2072`): 1790 passed, 0 failed, 0 skipped, 0 xfailed, 3 warnings (single shared suite run across all six reconciliations).
- **Acceptance criteria met**: Yes.




## Implementation verification -- Claude -- 2026-08-10

**Why this record exists now.** Chunk R -- the batched, Maintainer-only AST
re-anchor ceremony -- landed at `9724c0f`, closing the deliberate red window this
plan opened at Chunk B. That makes the plan **implementation-complete for the
first time**, and it is the first moment a Boundary B record could bind a green
tree. No prior `## Implementation verification` record exists for this plan.

| field | value |
|---|---|
| Tested commit | `9724c0f` |
| Reviewed range | `9bd6752` (Chunks A, C, D, E), `aba0242` (Chunk B -- the Maintainer-gated remediation string, unfenced by Decision amendment `d13c58a`), `9724c0f` (Chunk R -- the re-anchor ceremony). |
| Interpreter/runtime | `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python **3.13.13**, `PYTHONDONTWRITEBYTECODE=1` |
| Pre-run state | The suite was executed at `2cda515` with `bootstrap/tests/fixtures/scaffold_ast_baseline.json` and `scaffold_ast_known_new.json` modified on disk -- Chunk R's content, staged for the Maintainer's commit. **Stated exactly rather than as "clean":** those two files were the only tracked modifications. |
| Post-run state | The Maintainer committed exactly that fixture content as `9724c0f`. `git diff --name-only 2cda515..HEAD` outside `dev/` prose returns **only those two fixtures**, so the figures below bind `9724c0f`'s bytes rather than a superseded tree. `git status --short` reports **0 modified tracked files** at `9724c0f`. |
| Command | `python -m pytest bootstrap/tests -q` |
| Exit | 0 |
| Outcomes | **2593 passed, 0 failed**, 0 skipped, 0 xfailed, 3 warnings |
| Elapsed | 358.85s (0:05:58) |
| Non-pass disposition | **None. There is nothing to disposition.** This is the first fully green full-suite result recorded on this repository today; every earlier record on every sibling plan carried the two `test_ast_attest` nodes as a declared red, and Chunk R is what closed them. Independently re-confirmed at `9724c0f` on a clean tree: `pytest bootstrap/tests/test_ast_attest.py` -> **29 passed**, and `_ast_attest.py verify` -> `AST attestation OK — 173 baselined symbol(s) accounted for, unchanged` (N unmoved at 173, so the ceremony was surgical, not a re-pin). |
| Plan-specific acceptance commands | `python scripts/check_cairn.py` -> **OK**, 174 Markdown files, no issues, rc **0**. `python scripts/quality_gate.py --sub neutrality --sub redundancy` -> rc **1**; neutrality `fail=93 info=21`, redundancy `fail=0 info=2`. The rc-1 is the known pre-existing neutrality baseline, and it is **93 rather than the 96 recorded earlier today** because `0028b8b6` removed three vendor tokens from `templates/skills/_lib/lifecycle_planner.py`; no fail line falls in any file this plan touches. |
| Known omissions | **The code review does not cover the whole reviewed range, and this is the material gap.** `## Code review -- Antigravity (External, security lens) -- 2026-08-04` predates Chunk B (`aba0242`, 2026-08-10) and Chunk R (`9724c0f`, 2026-08-10) -- so two of this plan's six chunks, including the one that edits `bootstrap/_scaffold/lockfile.py` and the one that rewrites a trust-artifact baseline, have had no independent read. Under `doctrine/dual-review.md` trigger 4 -- *"review sharpening changes implementation, tests, executable templates, or fixtures in the reviewed range"* -- evidence reuse is unavailable for those two chunks and a fresh review round is owed before archive. This record supplies the broad run that round should validate; it does not substitute for it. |

**What was independently verified about Chunk B, and by whom.** The B2 node's
required perturbation was run before the chunk was committed: restoring the
forbidden destructive clause (*"remove the dormant engine package"*) to
`format_forked_facade_warning` makes
`test_node_b2_remediation_names_no_destructive_or_no_op_action` **fail**, and the
file was restored byte-exactly (md5 `46b9728cc53d0b0b4bb8fd1d61fdd162` before and
after). That establishes the node is not vacuous. It does **not** establish
independence: the perturbation was run by a Claude agent and Chunk B was authored
by one, which is the configuration the doctrine forbids from self-certifying.

**Chunk R's own ledger, for the reviewer.** Two CHANGED baselined symbols,
batched: `Assign:_MODULE_MAPPINGS` (`4f72dfcb7ce39f20` -> `df43d4d75f55a3e5`,
`8daecd2`, `portable-security-sweeps` Chunk A) via the guarded `update-symbol`
path; and `FunctionDef:format_forked_facade_warning` (`14e4bdf27ff6f1b3` ->
`a508f3c7ba8d7232`, `aba0242`, this plan's Chunk B) via Maintainer direct
correction, since it is not in `_ast_attest._UPDATE_ALLOWLIST`. Known-new
manifest 78 -> 80 keys, **REKEYED 0** -- no symbol changed logic while invisible
to the baseline gate. A reviewer should treat the baseline diff (exactly two
`digest` lines, no `span`/`type` movement) as the artifact to check.

This section is append-only once written.
