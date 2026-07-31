<!-- claim-check-allow: bootstrap/tests/test_lockfile_provenance.py -->
<!-- The path above is this plan's own forward reference; it materializes at Chunk F. -->
<!-- claim-check-allow: scripts/run_security_audit.py -->
<!-- The path above is cited only to explain it does NOT exist in Cairn's own
     tree (the module is team-gated / optional, not installed here) -- the
     real Cairn-tree source is templates/modules/team-gated/run_security_audit.py. -->

# Plan: lockfile provenance fields (P1-P5)

**Source proposal**: `dev/proposals/archive/2026-07-22-claude-lockfile-provenance-fields.md`
**Status**: open
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
   * **`python bootstrap/scaffold.py --manifest` currently emits 96 data
     rows**, not the proposal's snapshot of 94 (nor the 95 the proposal
     predicted post-licensing-Chunk-C). The proposal's own Revised design
     already treats this correctly as a **live invariant** ("equal row
     count before and after, captured at implementation time"), not a
     literal — this plan re-derives 96 as its own pre-edit snapshot and
     re-verifies at implementation time per that same discipline.
   * **The full suite baseline is now 2 failed / 1441 passed / 3 skipped**
     (147s), not 3 failed / 1408 passed / 3 skipped. The proposal's
     separately-tracked clock-dependent `test_evolution_infer` failure was
     independently fixed earlier this session (commit `0bfba10`); the
     remaining two failures are the same sandbox-interpreter AST artifacts
     every sibling plan this session has documented (clean under canonical
     `lhm`).

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
| F4 | (same file) | **Upgrade nodes** (using the imported `_install` harness, a real `--stage`/`--apply` cycle — closing the proposal's own named "weakest link," the untested old-engine direction): an `--apply` backfills a pre-provenance lockfile's two fields from stage metadata; an old stage (meta dict with no `new_source_*` keys, simulating a stage produced before this change) applied by a new engine degrades via `.get()` to the current lock's existing values, never writes null; a `--finalize` round-trip preserves unknown top-level keys verbatim (R3a's stated limit — `--finalize`/`--adopt-module` do not backfill, only preserve). |
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
  (Chunk F, all nodes). Full `python -m pytest bootstrap/tests` at **2
  failed / (1441 + new node count) passed / 3 skipped** — the two
  pre-existing sandbox-interpreter AST artifacts, unchanged; canonical
  `lhm` interpreter must show `test_ast_attest.py` reporting **exactly the
  5-CHANGED delta** above before Chunk G's handoff runs, and fully green
  (26/26 plus whatever `ast-known-new-repin` landed) after it.
* **Gate-manifest check** — `python bootstrap/tests/_gate_manifest.py
  produce --dry-run` (or the equivalent read-only check) confirms
  `bootstrap/tests/test_upgrade.py`'s hash is unchanged and the new test
  file reads `FROZEN-NEW`, not `FROZEN-MODIFIED` anywhere.
* **`--manifest` row-count invariant** — re-derive the pre-edit count at
  implementation time (this plan's own snapshot: 96, as_of this session;
  re-verify fresh, don't copy) and assert the post-edit count is identical
  — the fields are lockfile-only, the manifest is field-independent.
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
