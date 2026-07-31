<!-- claim-check-allow: bootstrap/tests/test_lockfile_provenance.py -->
<!-- The path above is this plan's own forward reference; it materializes at Chunk F. -->
<!-- claim-check-allow: scripts/run_security_audit.py -->
<!-- The path above is cited only to explain it does NOT exist in Cairn's own
     tree (the module is team-gated / optional, not installed here) -- the
     real Cairn-tree source is templates/modules/team-gated/run_security_audit.py. -->

# Plan: lockfile provenance fields (P1-P5)

**Source proposal**: `dev/proposals/archive/2026-07-22-claude-lockfile-provenance-fields.md`
**Status**: awaiting-plan-review
**Plan review**: required(**External cross-type**) — this is the Decision's
own ratified condition (`doctrine/dual-review.md:184-187`, contract-touching
surfaces get an External round; `:325-329` forbids softening a declared tier
downward), and it is an escalation beyond every other plan this session,
which all cleared at Internal. **This plan cannot proceed to implementation
on an Internal pass alone.** The fresh-context Internal read below is the
floor, not the ceiling; a genuinely different-agent-type or human read is
still required before Chunk A lands, matching how the proposal itself needed
both tiers before its own Decision.

## Context

The Decision (2026-07-22, Anthony Kendall) accepted the Revised proposal in
full, with the field renamed (`licenses` → `source_licenses`, OQ1) and four
open questions resolved. Full detail:
`dev/proposals/archive/2026-07-22-claude-lockfile-provenance-fields.md` — its
`## Revised proposal` section and `## Decision` are authoritative. This is
the largest, most heavily-reviewed proposal in this session's queue: a
3-lens Internal panel found **4 blocking + 8 substantive/minor** findings,
all accepted (one full round of revision, no re-review needed per the
panel's own gated-re-read reconciliation); Gemini's External read then
independently answered the two hardest framing questions the panel could
only pose, and returned SHIP.

**Two significant findings from this plan's own preparation, neither
caught by either proposal-stage review round — disclosed up front:**

1. **The proposal's citation for the AST re-anchor mechanism is the same
   error already found and corrected twice this session** (once for
   `adopter-licensing-compliance`, once for `first-session-survivability`).
   The proposal states: *"per `AGENTS.md:323-325` this change re-anchors
   `bootstrap/tests/fixtures/scaffold_ast_baseline.json` per
   `bootstrap/REANCHOR_RUNBOOK.md`... the full supervised flow applies...
   `bootstrap/REANCHOR_RUNBOOK.md:6-11` reserves Phase 0 and Phase 4 to the
   Maintainer."* Re-verified this session: `grep -c -i
   "scaffold_ast_baseline\|ast_attest" bootstrap/REANCHOR_RUNBOOK.md` →
   **0** — that runbook never mentions the AST baseline at all; its Phase
   0/4 governs the *differential-oracle gate's* trust root
   (`refs/cairn/gate-anchor`), a structurally separate mechanism.
   `bootstrap/tests/_gate_manifest.py`'s own `CASCADE_MUTABLE` dict
   explicitly excludes `scaffold_ast_baseline.json`, with the comment
   *"integrity governed by the named mechanism, not a byte hash"* — naming
   `_ast_attest.py update-symbol` as that mechanism. **The citation error's
   root is in `AGENTS.md` itself** (`:335-337`, "AST attestation
   baseline... re-anchor it per `bootstrap/REANCHOR_RUNBOOK.md`") — neither
   the 3-lens Internal panel, Gemini's External read, nor the Decision
   caught this, despite the identical error having already been found,
   corrected, and independently re-verified by fresh-context review twice
   in this same session on sibling plans. **Consequence:** none of the five
   touched functions are in `_ast_attest._UPDATE_ALLOWLIST`
   (`_MODULE_MAPPINGS`/`_SKILLS_MAPPINGS`/`_CORE_MAPPINGS`/
   `install_onboarding` only) — on that narrow point the proposal is
   correct, the surgical guarded path genuinely isn't available — but the
   fallback is the **established, Maintainer-validated direct-edit script
   pattern** used three times already this session (`adopter-licensing-
   compliance`'s Chunk D, `first-session-survivability`'s Chunk D, and
   `ast-known-new-repin`'s design), not the heavy Phase 0/4 ceremony.
   Chunk H below prepares that lighter, already-proven handoff.
2. **Every quantitative baseline the proposal cites has moved, in this
   plan's favor.** Re-verified this session, under the canonical `lhm`
   interpreter and current `master`:
   * **The AST baseline is currently fully clean — 0 CHANGED, not 133.**
     `_classify()` reports zero problems across the whole `_scaffold`
     package. All five of the proposal's "already CHANGED" target functions
     (`write_install_lockfile`, `_cmd_init_lock`, `_apply_upgrade`,
     `_write_stage`, `_emit_lock_yaml`) now show **no diff** against the
     baseline — several supervised corrections landed on other plans this
     session since the proposal's 2026-07-22 evidence was captured. This
     makes the eventual re-anchor **simpler than the proposal assumed**: a
     clean 5-symbol CHANGED delta this plan's own edits produce, not a
     133-symbol pile to sort a real delta out of. The proposal's own
     falsifiable gate target ("CHANGED stays at 133 per node") is
     **superseded**, not violated — Chunk G's acceptance criterion is
     revised accordingly (0 → exactly 5 CHANGED, no MISSING/DUPLICATE, the
     NEW-note set exactly `FunctionDef:_cairn_provenance` plus rotated
     `Import:` keys).
   * **`python bootstrap/scaffold.py --manifest` currently emits 95 data
     rows** (96 total lines: 1 `#`-prefixed header comment + 95 data rows,
     per `test_manifest.py`'s own header-stripping convention), matching
     the 95 the proposal predicted post-licensing-Chunk-C, not the
     proposal's original snapshot of 94. **Corrected at plan-review
     (PR2):** this plan's first draft conflated the 96-line total with the
     data-row count. The proposal's own Revised design already treats this
     correctly as a **live invariant** ("equal row count before and
     after, captured at implementation time"), not a literal — this plan
     re-derives 95 as its own pre-edit data-row snapshot and re-verifies
     at implementation time per that same discipline.
   * **The full suite baseline under the canonical `lhm` interpreter
     (Python 3.13.13, `bootstrap/DEPENDENCY_BUDGET.md`'s pin) is fully
     green — 1446 passed, 0 failed, 0 skipped** (independently re-run
     twice this session, most recently 238.72s), not the proposal's 3
     failed / 1408 passed / 3 skipped. The proposal's separately-tracked
     clock-dependent `test_evolution_infer` failure was independently
     fixed earlier this session (commit `0bfba10`). **Corrected at
     plan-review (PR1):** this plan's first draft mislabeled the
     non-canonical Python 3.12 sandbox run — 2 failed / 1441 passed / 3
     skipped, two spurious `test_ast_attest.py` "NOT pure motion"
     artifacts, the exact `ast.dump` minor-version phenomenon
     `DEPENDENCY_BUDGET.md` warns about — as the canonical baseline. That
     3.12 figure is real (and is what `dev/.cairn/local-env.json`
     currently binds to) but is a sandbox-only comparison point, never
     the target.

**Everything else in the Revised proposal + Decision is taken as
settled** — the stage-metadata mechanism (R1), the five-writer inventory
(R3), the gate-manifest FROZEN-NEW test placement (R2), the `#:` comment
convention (R6), the `run_security_audit.py` reader test (R9), the
CITATION.cff parse contract (R12a), and all four resolved open questions.
This plan does not re-litigate any of it.

### Documentation / doctrine surface

Per the Decision: `bootstrap/UPGRADE.md` (domain-local governing range, a
new subsection) is the canonical home for the additive-vs-breaking rule;
the `_LOCK_SCHEMA` `#:` comment and the `_emit_lock_yaml` header line are
both **pointers**, not restatements (doc-governance's one-canonical-home
rule). `bootstrap/PROVENANCE.md:77-79`'s field enumeration gets a
one-sentence amendment (R11b). No `doctrine/` change; no `AGENTS.md`
change (OQ2 explicitly declined that home).

## Sequence

```
A. P1 -- the _cairn_provenance reader (lockfile.py)                [commit pending]
B. P2 -- the two fields at the constructing writers                [commit pending]
C. P2 -- stage-metadata plumbing for --apply                       [commit pending]
D. P3 -- schema-evolution rule, sited once (UPGRADE.md + pointers)  [commit pending]
E. P3/R11b -- PROVENANCE.md enumeration amendment                  [commit pending]
F. Tests -- bootstrap/tests/test_lockfile_provenance.py (new)      [commit pending]
G. Supervised AST re-anchor handoff (Maintainer-gated)              [parked]
```

`dev/PLANNING.md`'s deferred row for P4 (validate-on-read) lands **now, at
plan-open**, per the Decision's OQ3 ("gets a `dev/PLANNING.md` row at
plan-open... not in this Decision commit") — see below, committed in the
same commit as this plan.

### Chunk A — P1 (the `_cairn_provenance` reader)

| # | File | Change |
|---|------|--------|
| A1 | `bootstrap/_scaffold/lockfile.py` | New helper `_cairn_provenance(cairn_root: Path) -> tuple[str, list[str]]`, placed beside `_cairn_version` (`:103-111`) and `_cairn_commit` (`:114-124`), reading `CITATION.cff` once. `source_repository` from the `repository-code:` line (single-line match, mirroring `_cairn_version`'s pattern). `source_licenses` from the `license:` block — **the exact parse contract from R12a/the Revised proposal**: consume indented `- ` items starting immediately after the `license:` line; stop at the first line that is not an indented `- ` item (this is load-bearing — `CITATION.cff:19-21`'s `license:` block is immediately followed by a `keywords:` block with 6 of its own `- ` items at `:22-28`, and a scanner that kept consuming would silently record six keywords as licenses); accept the scalar form (`license: MIT`) as a one-element list; drop any consumed value that doesn't look like an SPDX identifier (no whitespace, non-empty). Degrades to `("unknown", [])` on any absence/unreadable/keyless case — matching `_cairn_version`/`_cairn_commit`'s sentinel discipline exactly (never able to fail an install). |
| A2 | `bootstrap/_scaffold/lockfile.py` | `_LOCK_SCHEMA = 1` (`:42`) gains a `#:` comment (AST-invisible, R6 — **not** a docstring or a bare string literal, both of which would mint a new `Docstring#2` baseline key the re-anchor delta doesn't enumerate) — a one-line **pointer** to `bootstrap/UPGRADE.md`'s new subsection (Chunk D), not a restatement of the rule. |
| A3 | `bootstrap/_scaffold/__init__.py` | Add `_cairn_provenance` to the facade re-export block beside `_cairn_commit`/`_cairn_version` (`:290-291`), matching the existing pattern for that block. |

### Chunk B — P2 (the two fields at the constructing writers)

| # | File | Change |
|---|------|--------|
| B1 | `bootstrap/_scaffold/install.py` | `write_install_lockfile`'s lock dict (`:1627-1636`) gains `"source_repository": ...` and `"source_licenses": ...` from `_cairn_provenance(cairn_root)`, beside `cairn_version`/`cairn_commit`. |
| B2 | `bootstrap/_scaffold/upgrade.py` | `_cmd_init_lock`'s synthesized migration lock dict (`:1196-1203`) gains the same two fields, same source. |

### Chunk C — P2 continued (stage-metadata plumbing for `--apply`)

| # | File | Change |
|---|------|--------|
| C1 | `bootstrap/_scaffold/upgrade.py` | `_write_stage`'s meta dict (`:900-930`) gains `"new_source_repository"` / `"new_source_licenses"` via `_cairn_provenance(cairn_root)`, immediately beside `"new_version"` / `"new_commit"` (`:906-907`) — **non-ref-aware, deliberately, for the same reason `new_version` already is**: both read the working tree's `CITATION.cff` with no `to_ref` consultation (only `new_commit` is ref-aware, via `to_ref or _cairn_commit(...)`); consistency with the sibling field sourced from the same file is the whole argument, not an open ref-awareness judgment call (R1's corrected framing). |
| C2 | `bootstrap/_scaffold/upgrade.py` | `_apply_upgrade`'s lock advance (`:1943-1945`) gains `new_lock["source_repository"] = meta.get("new_source_repository", lock.get("source_repository"))` and the same pattern for `source_licenses` — a `.get()` fallback to the *current lock's* value, so an old stage (no provenance keys in its meta) applied by a new engine degrades to "keep what the lockfile already had," never writes a null. |

### Chunk D — P3 (schema-evolution rule, sited once)

| # | File | Change |
|---|------|--------|
| D1 | `bootstrap/UPGRADE.md` | New subsection, canonical home (Decision OQ2 — domain-local governing range per `docs/DOCUMENTATION_PLAN.md:143-146`), inserted after the existing `## The lockfile and the fidelity manifest` section (`:189-197`) and before `## A note on secrets` (`:199`): enumerates the lockfile's top-level fields (`schema`, `cairn_version`, `cairn_commit`, `source_repository`, `source_licenses`, `profile`, `modules`, `optional_templates`, `tokens`, `files`, plus the writer-varying `migrated`), and states the additive-vs-breaking rule in full: an additive **optional** top-level field does not bump `schema`; readers must use `.get()` with a default and tolerate unknown keys; a removal, rename, or change of meaning of an existing field does bump, and a bump is the point a reader-side validator becomes mandatory. Cites `migrated` (`_cmd_init_lock`-only, absent from fresh installs, coexisting with `schema: 1` since it shipped) as the existing precedent this rule codifies, not a new invention. |
| D2 | `bootstrap/_scaffold/lockfile.py` | `_emit_lock_yaml`'s header (`:184-186`) gains one line pointing to the rule's home — the only surface in this whole change that actually reaches an adopter's tree (`--manifest` emits zero `bootstrap/` rows, confirmed this session; `UPGRADE.md` itself never installs). |

### Chunk E — R11b (`PROVENANCE.md` enumeration amendment)

| # | File | Change |
|---|------|--------|
| E1 | `bootstrap/PROVENANCE.md` | One-sentence amendment to the install-side provenance enumeration (`:77-79`, "the exact `cairn_version` + `cairn_commit`, the resolved profile, and the per-file source / hash") — add `source_repository` + `source_licenses` to the list, so the document that this proposal quotes twice as its own motivation doesn't go stale the moment the fields it's arguing for actually ship. |

### Chunk F — tests (`bootstrap/tests/test_lockfile_provenance.py`, new)

| # | File | Change |
|---|------|--------|
| F1 | `bootstrap/tests/test_lockfile_provenance.py` (new) | **Not** `bootstrap/tests/test_upgrade.py` — that file is in the gate manifest's pinned 147-entry `frozen_files` set (confirmed this session), and editing a frozen file produces `FROZEN-MODIFIED`, appended to `holds` (a hard-stop), not `notes` (R2's blocking finding). The new file reads `FROZEN-NEW` (allowed, recorded as a note) instead. Imports `_install` from `test_upgrade.py` (module-level, `:45`) rather than duplicating the install/delta harness — importing a frozen file does not modify it, so this creates no HOLD. |
| F2 | (same file) | **Reader nodes**: `_cairn_provenance` degrades to `("unknown", [])` on a `CITATION.cff`-less root; the `license:`-block-terminated-by-`keywords:` case yields exactly `["CC-BY-4.0", "MIT"]` (the live shape of Cairn's own `CITATION.cff`, the load-bearing regression case per R12a); a scalar `license: MIT` yields `["MIT"]`. |
| F3 | (same file) | **Writer nodes**: a fresh install's lockfile carries `source_repository`/`source_licenses` equal to `_cairn_provenance(CAIRN_ROOT)`; `--init-lock`'s synthesized lock carries the same. |
| F4 | (same file) | **Upgrade nodes** (using the imported `_install` harness, a real `--stage`/`--apply` cycle — closing the proposal's own named "weakest link," the untested old-engine direction): an `--apply` backfills a pre-provenance lockfile's two fields from stage metadata, and asserts the backfilled values equal `_cairn_provenance(cairn_root)` for the same root — the proposal's own stated **install-vs-apply parity invariant**, named explicitly here (per plan-review/PR6) rather than left implicit in F3+F4's combined coverage; an old stage (meta dict with no `new_source_*` keys, simulating a stage produced before this change) applied by a new engine degrades via `.get()` to the current lock's existing values, never writes null; a `--finalize` round-trip preserves unknown top-level keys verbatim (R3a's stated limit — `--finalize`/`--adopt-module` do not backfill, only preserve). |
| F5 | (same file) | **`run_security_audit.py` compatibility node** (R9): feed a provenance-bearing lockfile to `templates/modules/team-gated/run_security_audit.py`'s `load_lockfile` + `required_apparatus_dsts` (this is the actual Cairn-tree source; it installs verbatim into an adopter tree as `scripts/run_security_audit.py`, which does not exist in Cairn's own `scripts/` — the module is team-gated / optional and not installed here) — the shipped, hash-tracked reader that parses the whole lockfile itself rather than via `read_lockfile` — and assert unchanged behavior. The real, demonstrable old-reader-vs-new-lockfile case the proposal's evidence plan named as its weakest link, now closed with an actual test rather than an argument from source. |

### Chunk G — supervised AST re-anchor handoff (Maintainer-gated; not this agent's act)

**Not `bootstrap/REANCHOR_RUNBOOK.md` Phase 0/4** (this plan's own finding
1, above) — that ceremony governs the differential-oracle gate's trust
root, a different mechanism the proposal's own citation conflated with the
AST baseline. The real, already-validated mechanism (used identically
three times this session) is a Maintainer-run, dry-run-verified script
that directly corrects `scaffold_ast_baseline.json`'s digest+span for the
non-allowlisted symbols this plan's own edits touch — none of the five
(`_cairn_provenance` is new, not a correction; `write_install_lockfile`,
`_cmd_init_lock`, `_apply_upgrade`, `_write_stage`, `_emit_lock_yaml` are
all CHANGED, none in `_UPDATE_ALLOWLIST`) qualify for the guarded
`update-symbol` self-service path.

**Named explicitly, per plan-review (PR4):** the Decision's own "Plan
conditions, ratified here (bind the plan)" text — not only the
proposal's evidence-section prose — states the mechanism as "a
supervised AST re-anchor for the five touched engine functions per
`bootstrap/REANCHOR_RUNBOOK.md`." This chunk's substitution is therefore
a deviation from the **literal binding language the Maintainer
ratified**, not merely a correction of stale proposal narrative — the
underlying technical claim (the runbook never governs the AST baseline)
is independently verified correct twice over (this plan's own
preparation, and its Internal plan-review), but the choice of mechanism
is being made here, by this plan, on that verification alone. This is
flagged as a specific, nameable item for the required External
cross-type reviewer — and ideally the Maintainer directly — to affirm,
rather than left to be inferred from Finding 1's narrative.

Prepared once Chunks A-F land and their real live digests are known — not
before, since the digests depend on the actual shipped code, not this
plan's preparation-time estimates. The falsifiable target (superseded from
the proposal's stale 133/node): after Chunks A-F, `_classify()` reports
**exactly 5 CHANGED** (`write_install_lockfile`, `_cmd_init_lock`,
`_apply_upgrade`, `_write_stage`, `_emit_lock_yaml`), **0 MISSING, 0
DUPLICATE**, and the NEW-note set is exactly `FunctionDef:_cairn_provenance`
plus whatever `Import:` keys rotate from the new imports each edit
introduces (informational only, never a failure — confirmed this session
per `_classify()`'s own Import/Docstring skip).

## Acceptance criteria

* **Tests that must pass** — `bootstrap/tests/test_lockfile_provenance.py`
  (Chunk F, all nodes). Full `python -m pytest bootstrap/tests`, run
  under the **canonical `lhm` interpreter** (Python 3.13.13), at **0
  failed / (1446 + new node count) passed / 0 skipped** — the current
  canonical baseline, independently re-verified twice this session (the
  3.12 sandbox interpreter reports 2 failed / 1441 passed / 3 skipped on
  the same tree today, a known documented artifact, never the target —
  name the interpreter alongside any figure you assert, per
  `DEPENDENCY_BUDGET.md`). Before Chunk G's handoff runs, canonical
  `lhm`'s `test_ast_attest.py` must show **exactly the 5-CHANGED delta**
  above; its pre-Chunk-A baseline is already **29 passed, 0 failed**
  (re-verified this session under canonical `lhm`) — after Chunk G's
  handoff it returns to that same 29 passed, 0 failed (the handoff
  corrects the baseline JSON to match the new code; it adds no test
  nodes of its own).
* **Gate-manifest check** — `python bootstrap/tests/_gate_manifest.py
  verify` (optionally `--no-collect` to skip the pytest-collection check;
  both read-only — `produce` takes no arguments, confirmed at
  plan-review/PR3) confirms `bootstrap/tests/test_upgrade.py`'s hash is
  unchanged and the new test file reads `FROZEN-NEW`, not
  `FROZEN-MODIFIED`, anywhere.
* **`--manifest` row-count invariant** — re-derive the pre-edit *data-row*
  count at implementation time (this plan's own snapshot: 95 data rows,
  96 total lines including the header comment, as_of this session;
  re-verify fresh, don't copy) and assert the post-edit count is
  identical — the fields are lockfile-only, the manifest is
  field-independent.
* **Bandit** — `python -m pytest bootstrap/tests/test_security_lint.py`
  green; `_cairn_provenance` uses only `Path.read_text` + `re`, no
  subprocess/eval/deserialization, so no new finding is expected (R12b).
* **Docs**: `python scripts/check_cairn.py` and `python scripts/claim_check.py`
  clean over this plan and every touched/new file.
* **Smoke**: a real scratch install into a temp target, then `python
  bootstrap/verify_integrity.py --target <scratch>` exits 0 with the new
  fields present (the trust anchor is indifferent to unknown-to-it keys).

## Signals the change is wrong

Carried forward from the proposal's own list (`:585-624`), unchanged —
still the right failure signals: `licenses` misread as per-file (recovery:
already renamed `source_licenses` at Decision, so this signal is largely
closed pre-emptively); `source_repository` trusted as attested origin
(recovery: the field stays documented as declared, not attested);
`schema: 1` becoming uninformative across two field generations (recovery:
the written rule already keys on field presence); an old engine dropping
fields on `--apply` in some version not inspected (recovery: promotes P4
from deferred to required); the suite getting worse than this plan's own
re-derived baseline, or the re-anchor diff touching anything beyond the
five function keys (recovery: revert — one helper, two dict keys in two
writers, one meta-dict addition, one read-side `.get()` addition). Add one
from this plan's own preparation: **the AST re-anchor handoff's
Maintainer-run script produces a CHANGED set that isn't exactly the 5
named functions** → the plan's own edits touched something unintended;
do not hand off the script until the live delta matches exactly.

## Review

*Filled in after the fresh-context Internal plan-review subagent pass, and
separately after the required External cross-type read this plan's own
declared tier mandates before implementation.*

## Code review

*Filled in after implementation commits land (Chunks A-G).*

## Lasting-truth migration

*Filled in at archive time. Per the [Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home
outside the plan — P4 (validate-on-read) is already homed at its
`dev/PLANNING.md` Queued row (added at this plan's own open, per Decision
OQ3), and Cairn's own `dev/.cairn/cairn-lock.yml` staying provenance-free
until its next self-targeted `--stage`/`--apply` (Decision OQ4) is a
stated, accepted disposition, not a deferred follow-up needing its own
home.*

This section is append-only once written.

## Plan review -- Claude (Internal, fresh-context) -- 2026-07-31

**Tier reminder, per the task that produced this review.** This plan's own
header declares `Plan review: required(External cross-type)` — the Decision's
own ratified condition (`doctrine/dual-review.md:184-187`,`:325-329`). What
follows is a fresh-context Internal pass only (same agent type as the plan's
author, new context, no memory of its drafting). **A clean Internal pass does
not satisfy this plan's own declared gate.** Nothing below should be read as
clearing the plan for Chunk A; a genuinely different-agent-type or human read
is still required, exactly as the plan's own Context section already states.

Chunk-by-chunk citation re-verification (independently re-read, not trusted
from the plan's prose): every line citation in Chunks A-E and the two
disclosed findings checked out **exactly** against the live tree —
`lockfile.py:42` (`_LOCK_SCHEMA`), `:103-111`/`:114-124` (`_cairn_version`/
`_cairn_commit`), `:184-190` (`_emit_lock_yaml`'s header); `install.py:1627-
1636` (`write_install_lockfile`'s lock dict); `upgrade.py:1196-1203`
(`_cmd_init_lock`'s lock dict), `:900-930` with `new_version`/`new_commit` at
`:906-907` (`_write_stage`'s meta dict), `:1943-1945` (`_apply_upgrade`'s lock
advance); `__init__.py:290-291` (the `_cairn_commit`/`_cairn_version` facade
re-export pair); `UPGRADE.md`'s `## The lockfile and the fidelity manifest`
at `:189-197` immediately followed by `## A note on secrets` at `:199`;
`PROVENANCE.md:77-79`; `test_upgrade.py:45`'s module-level `_install`;
`CITATION.cff:19-21`'s `license:` block immediately followed by `:22-28`'s
6-item `keywords:` block. Both disclosed findings independently reproduced:
`grep -c -i "scaffold_ast_baseline\|ast_attest" bootstrap/REANCHOR_RUNBOOK.md`
→ 0; `bootstrap/tests/_gate_manifest.py`'s `CASCADE_MUTABLE` dict names
`scaffold_ast_baseline.json`'s integrity mechanism as "`_ast_attest.py
update-symbol`" with the "governed by the named mechanism, not a byte hash"
comment, verbatim; `_ast_attest._UPDATE_ALLOWLIST` is exactly `{_MODULE_
MAPPINGS, _SKILLS_MAPPINGS, _CORE_MAPPINGS, install_onboarding}`, none of the
five touched functions among them; the "established... direct-edit script
pattern" is real (`adopter-licensing-compliance` Chunk D, `first-session-
survivability` Chunk D). `test_ast_attest.py` currently reports **29 passed,
0 failed** under canonical `lhm`/Python 3.13.13 — confirming "0 CHANGED."
`CITATION.cff`'s parse-contract edge case is real and P1's stop-at-first-
non-`- `-line design handles it correctly. Chunk F1's FROZEN-NEW claim
verified against `_gate_manifest.py:357-366`'s actual set-difference logic (a
file not in the pinned `frozen_files` dict logs as a `note`, never a
`hold`); the pinned manifest's frozen-file count is genuinely 147 (`bootstrap/
tests/fixtures/gate_manifest.json`, `len(frozen_files) == 147` — a fresh
`produce` gives 161, which is expected: the gate compares against the
*pinned* commit, not a live regeneration). No stale citation found in
Chunks A-F.

**PR1 [SUBSTANTIVE].** The plan's disclosed Finding 2's full-suite figure —
"2 failed / 1441 passed / 3 skipped (147s)... re-verified this session, under
the canonical `lhm` interpreter" — is not what the canonical interpreter
reports. I ran both, just now:

* `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests -q`
  (Python 3.13.13, the canonical interpreter per `bootstrap/DEPENDENCY_
  BUDGET.md`'s "The canonical interpreter" section and `gate_manifest.json`'s
  pin) → **1446 passed, 0 failed, 0 skipped, 217.79s**. `test_ast_attest.py`
  alone: 29 passed, 0 failed.
* The sandbox default `python3` (`/Users/kendal30/conda_envs/miniforge3/bin/
  python3.12`, Python 3.12.9 — also what `dev/.cairn/local-env.json` currently
  binds) → **2 failed, 1441 passed, 3 skipped, 202.17s** — the two failures
  are the same `test_ast_attest.py` nodes, both reporting dozens of spurious
  "NOT pure motion" `CHANGED` entries (an `ast.dump` minor-version artifact,
  exactly the phenomenon `DEPENDENCY_BUDGET.md`'s canonical-interpreter table
  documents).

The plan's cited numbers are the **3.12 sandbox run**, not a canonical-`lhm`
run — they match the 3.12 figures I reproduced exactly (2/1441/3, down to the
"NOT pure motion" AST spam), while the actual canonical-`lhm` baseline is
fully green (0/1446/0). This is the identical failure class `bootstrap/
DEPENDENCY_BUDGET.md`'s own "canonical interpreter" section warns about
("Two honest agents on the same tree otherwise report different facts... If
you assert a suite figure or a gate outcome, name the interpreter with it")
— and the same class of citation-mislabeling this plan's own Finding 1
prides itself on catching. It also propagates into the **Acceptance
criteria** section's literal target ("Full `python -m pytest bootstrap/tests`
at 2 failed / (1441 + new node count) passed / 3 skipped"), which as written
would read a genuinely clean canonical run as a regression from expectation.
**Fix:** restate Finding 2's suite baseline and the Acceptance-criteria
bullet as the canonical-`lhm` figure (0 failed / 1446 passed / 0 skipped),
and either drop the sandbox figure or explicitly label it as the non-
canonical comparison point, not the target.

**PR2 [SUBSTANTIVE].** Finding 2's manifest-row claim — "`python bootstrap/
scaffold.py --manifest` currently emits 96 data rows, not... the 95 the
proposal predicted post-licensing-Chunk-C" — is off by one. Live count, just
run: `python bootstrap/scaffold.py --manifest | wc -l` → 96 **total lines**,
of which line 1 is the `# Cairn install manifest...` header; `grep -vc '^#'`
→ **95** actual data rows. This is exactly the "95" the plan explicitly says
is *not* the correct figure. The established convention distinguishing the
two is not new: `bootstrap/tests/test_manifest.py`'s own `test_format_
manifest_is_stable_and_tabbed` computes `body = [ln for ln in text.
splitlines() if not ln.startswith("#")]` before counting, and the sibling
`adopter-licensing-compliance` plan's own review already phrased the
identical post-Chunk-C state as "96 lines (1 header + 95 data rows)" — the
plan's "96 data rows" conflates the total line count with the data-row
count. Low practical stakes (the Acceptance criteria correctly instructs
"re-derive the pre-edit count at implementation time... re-verify fresh,
don't copy," which self-corrects the number actually used), but the
disclosed-finding prose itself is wrong and should say 95, not 96.

**PR3 [MINOR].** The Acceptance criteria's gate-manifest check cites `python
bootstrap/tests/_gate_manifest.py produce --dry-run`. `_gate_manifest.py`'s
`produce` subcommand takes **no arguments** (`sub.add_parser("produce", ...)`
with zero `add_argument` calls, `_gate_manifest.py:420`) — `--dry-run` would
be rejected by argparse. `produce` is already read-only (emits JSON to
stdout, mutates nothing), so a `--dry-run` flag on it wouldn't be meaningful
even if it existed; the actual read-only integrity check is the `verify`
subcommand, which is what would report the new file as `FROZEN-NEW` in its
`notes` (confirmed at `_gate_manifest.py:357-366`). **Fix:** cite `python
bootstrap/tests/_gate_manifest.py verify` (optionally `--no-collect` to skip
the pytest-collection check), not `produce --dry-run`.

**PR4 [SUBSTANTIVE, process].** The Decision's own "**Plan conditions,
ratified here (bind the plan)**" text (not just the proposal's evidence
section) states: *"a supervised AST re-anchor for the five touched engine
functions **per `bootstrap/REANCHOR_RUNBOOK.md`**."* Finding 1's underlying
technical claim is independently verified correct (the runbook never
mentions the AST baseline; `CASCADE_MUTABLE` names a different mechanism) —
but the plan's Chunk G substitutes a different procedure than the one the
Maintainer's own ratified language names, on this plan's own authority. The
plan does note "neither... the Decision caught this," which is honest
disclosure that the error reaches the Decision text, but Chunk G doesn't
explicitly flag that it is deviating from the **literal binding language of
the ratified Plan conditions**, as distinct from correcting the proposal's
stale prose — those are different weights of correction. Chunk G is already
Maintainer-gated for its *execution*, but the *choice of mechanism* is being
made now, by this plan, not deferred to that gate. **Suggested fix:** add one
sentence to Chunk G (or the Context disclosure) naming this explicitly as a
deviation from the Decision's own ratified condition text, not only the
proposal's evidence — surfacing it as a specific, nameable item for the
required External cross-type reviewer (and ideally the Maintainer directly)
to affirm, rather than leaving the substitution to be inferred from the
finding-1 narrative.

**PR5 [MINOR].** The Acceptance criteria's AST-reanchor bullet targets
"fully green (26/26 plus whatever `ast-known-new-repin` landed)" after
Chunk G. Live count under canonical `lhm` right now (pre-Chunk-A) is already
**29 passed, 0 failed** in `test_ast_attest.py` — i.e., the uncertain
"26 + whatever landed" arithmetic already resolves to a known number today.
Not wrong (the hedge covers it), but there's no reason to leave it a guess
when it's cheaply re-derivable; state 29 (or re-derive at Chunk-G time) as
the concrete pre-Chunk-A baseline rather than carrying the "26 + X" formula
forward.

**PR6 [MINOR].** The source proposal's own Author-accounting invariants
table lists *"A fresh install and an `--apply` produce the *same* provenance
values for the same `cairn_root`"*, enforced by a stated *"new install-vs-
upgrade parity assertion."* The plan's Context section says the proposal's
invariants are "taken as settled" and not re-litigated, but Chunk F's five
rows (F1-F5) don't name this parity assertion as its own test node — F3
covers fresh-install-vs-`--init-lock` (both call `_cairn_provenance`
directly, so parity there is close to definitional) and F4 covers the
`--apply` backfill's degradation behavior, but neither explicitly asserts
that a real `--apply`-backfilled value equals `_cairn_provenance(CAIRN_
ROOT)` for the same root. Likely subsumed by F4 in practice, but the plan
should either name the parity assertion explicitly as its own bullet or note
why F3+F4 jointly discharge it, so the coverage isn't silently narrower than
the invariant the settled proposal commits to.

**Coverage note.** Read `AGENTS.md` and skimmed `dev/agent_collaboration.md`
for the review-tier/lifecycle grounding this task asked for. Did not attempt
to independently re-derive the `--apply` stage-metadata backward/forward
compatibility argument from scratch (E1/E2 in Gemini's External read) — that
argument is unchanged from the Decision-ratified Revised proposal and is not
something this plan's own edits touch differently; taken as settled per the
plan's own Context section, consistent with this review's scope (auditing
*this plan's* preparation, not re-litigating the proposal). Did not run a
scratch install / `verify_integrity.py` smoke test (Chunk A-F code does not
exist yet to smoke-test — nothing in the plan's design depends on that
result before implementation). BLOCKING: 0. SUBSTANTIVE: 4 (PR1, PR2, PR4,
and the tier reminder above). MINOR: 3 (PR3, PR5, PR6).

### Sharpening -- Claude (author) -- 2026-07-31

All six findings independently re-verified before disposing, not taken
on the reviewer's word: re-ran the full suite under both interpreters
myself (`/Users/kendal30/conda_envs/lhm/bin/python3.13`, 3.13.13 →
**1446 passed, 0 failed, 0 skipped, 238.72s**; sandbox default `python3`,
3.12.9, unchanged at 2 failed / 1441 passed / 3 skipped); re-ran
`python bootstrap/scaffold.py --manifest | wc -l` (96) and `| grep -vc
'^#'` (95) directly; read `_gate_manifest.py`'s `produce` subcommand
construction directly (`sub.add_parser("produce", ...)` with zero
`add_argument` calls — `--dry-run` is not a valid flag); re-read the
Decision's own "Plan conditions, ratified here" text in the archived
proposal and confirmed the literal "per `bootstrap/REANCHOR_RUNBOOK.md`"
wording (`:1012-1015`); re-read the proposal's invariants table and
confirmed the install-vs-apply parity row (`:482`) verbatim.

* **[PR1] accept.** Context Finding 2's suite bullet and the Acceptance
  criteria's tests bullet both corrected to the canonical-`lhm` figure
  (0 failed / 1446 passed / 0 skipped), with the 3.12 sandbox figure
  (2 failed / 1441 passed / 3 skipped) kept only as an explicitly-labeled
  non-canonical comparison point, never the target. Also noted:
  `dev/.cairn/local-env.json` currently binds the non-canonical 3.12
  interpreter — worth the Maintainer's attention independent of this
  plan, not something this plan's scope should fix.
* **[PR2] accept.** Context Finding 2's manifest bullet and the
  Acceptance criteria's row-count-invariant bullet both corrected to 95
  data rows (96 total lines, 1 header comment), matching the proposal's
  own post-Chunk-C prediction exactly.
* **[PR3] accept.** Acceptance criteria's gate-manifest check corrected
  from the nonexistent `produce --dry-run` to `verify` (optionally
  `--no-collect`), the actual read-only integrity check.
* **[PR4] accept.** Chunk G gains an explicit paragraph naming the
  mechanism substitution as a deviation from the Decision's own literal
  "Plan conditions" binding text, not only the proposal's stale
  evidence-section prose — flagged as a specific item for the required
  External cross-type reviewer (and the Maintainer) to affirm.
* **[PR5] accept, folded into PR1's fix.** The Acceptance criteria's
  "26/26 plus whatever landed" hedge is replaced with the concrete
  pre-Chunk-A baseline (29 passed, 0 failed) and the exact post-Chunk-G
  target (the same 29/0 — the handoff corrects the baseline, it adds no
  test nodes).
* **[PR6] accept.** Chunk F's F4 row now names the install-vs-apply
  parity invariant explicitly as an assertion the `--apply` backfill node
  makes, rather than leaving it to be inferred from F3+F4's combined
  coverage.

**Also corrected, self-caught (not from the Internal review):** the
plan's `**Status**` line read `open`; `doctrine/plans.md`'s "plan-review
precondition" names the correct status for a `required`-tier plan with
no landed review as **`awaiting-plan-review`**, explicitly distinct from
plain `open`. Corrected above.

**Status: remains `awaiting-plan-review`.** This Internal pass and its
sharpening are the floor, not the plan's declared gate — the header's
`Plan review: required(External cross-type)` is not satisfied by an
Internal read at any thoroughness, per `doctrine/dual-review.md:325-329`
("forbids softening a declared tier downward") and this review's own
tier-reminder paragraph above. Implementation on Chunk A does not begin
until a genuinely different-agent-type or human review lands as its own
dated `## Plan review` section.

This section is append-only once written.
