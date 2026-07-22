<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/lifecycle.md doctrine/runtime-contract.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: templates/core/NOTICE.md, NOTICE.md, bootstrap/tests/test_notice_install.py -->
<!-- The three paths above are forward-reference files this plan creates; they materialize as the chunks land. -->

# Plan: adopter licensing compliance (P1, P2, P4, P5, P6)

**Source proposal**: `dev/proposals/archive/2026-07-11-claude-adopter-licensing-compliance.md`
**Status**: awaiting-plan-review
**Plan review**: required(Internal) — ratified at Decision; touches the install
contract (a new `_CORE_MAPPINGS` member) and legal instruments, and this plan
pins the exact NOTICE.md/BOOTSTRAP.md/LICENSE text the proposal left to plan
stage, plus the file-population mechanics for P2's ~91-file header sweep.
**Last update**: 2026-07-22
**Opened**: 2026-07-22

## Source proposal

The accepted, Revised proposal (P1+P2+P4+P5+P6; P3 — lockfile provenance
fields — withdrawn to its own future install-contract proposal) fixes a
verified pre-0.4 release blocker: the default Cairn install strips the MIT
notice from every shipped tool and installs no CC-BY attribution. Fix: one
installed `NOTICE.md` (P1) discharges both obligations for the whole tree;
self-propagating SPDX headers on shipped `.py` (P2) keep the MIT notice with
any file copied out; an adopter-facing paragraph (P4), an inbound=outbound
sentence for case studies (P5), and a `.yml`/`.txt` classification
clarification (P6) round out the package. The proposal cleared a 3-lens
Internal panel (12 critiques, all accepted) and a Gemini External SHIP, and
was accepted 2026-07-22 with two reserved co-decisions resolved (no CC-BY
downstream-permission clause; `NOTICE.md` at repo root) and the AST re-anchor
scoping corrected (P1 requires it, P2 does not).

## Proposed paths

Proposed paths:
- `templates/core/NOTICE.md` — the shipped notice template (source); installed to the adopter as `NOTICE.md` via a new `_CORE_MAPPINGS` entry (Chunk C).
- `NOTICE.md` — Cairn's own repo-root copy, added in the same commit as the source template (Chunk C).
- `bootstrap/tests/test_notice_install.py` — new test file; the P2 header-presence + parity assertions land in Chunk B, the P1 install-behavior assertions in Chunk C.

## Scope

Implements the Revised proposal's P1 + P2 + P4 + P5 + P6 in full.

**Scope fence (what this does NOT do):**
* **P3** (lockfile `source_repository` + `licenses` fields) is out of scope —
  withdrawn to its own future install-contract proposal (R4), which will also
  carry the R7 fix (the `licenses` field's CITATION.cff-vs-illustrative-value
  mismatch).
* **Headers on `bootstrap/_scaffold/` + `bootstrap/tests/`** are explicitly
  **not** added by this plan. The Revised proposal names this as the plan's
  call ("the plan may include them"); the proposal's own `Touches` line only
  commits to `templates/` and `scripts/`, and adding ~130 more files to an
  already-large sweep for a benefit that is real but secondary (Cairn's own
  non-shipped-engine MIT hygiene, not adopter-facing compliance) is scope
  this plan declines. A future proposal can pick it up; nothing here forecloses
  it (comment-only headers are AST-invisible regardless of when they land).
* **The CC-BY downstream-permission clause** is not added — resolved at
  Decision (declined).

### Documentation / doctrine surface

Legal instruments (`LICENSE-MIT.md`, `LICENSE-CC-BY.md`), a new legal-adjacent
adopter file (`NOTICE.md`), install machinery (`bootstrap/_scaffold/config.py`),
and descriptive adopter docs (`bootstrap/BOOTSTRAP.md`, `case-studies/README.md`).
No `doctrine/` change — per the proposal's own routing (P4/P5/P6 are
descriptive/procedural; the install-contract touch (P1) is governed by
`AGENTS.md`'s existing high-risk-surface rule, not a doctrine change).

<!-- cairn:slot documentation-tier-home -->
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
plan's *Scope* must name the doctrine-surface touched (or an explicit
"no doctrine surface").
<!-- cairn:end documentation-tier-home -->

**The re-anchor gate (why this plan cannot fully archive on its own).**
`bootstrap/REANCHOR_RUNBOOK.md` is explicit: *"an implementing agent must not
perform Phase 0 or Phase 4 — that is the forbidden 'implementer blesses its
own verifier' self-authorization."* Phase 0 (trust root) is already
established (`refs/cairn/gate-anchor` exists). Chunk C's `_CORE_MAPPINGS` edit
requires Phase 4 (the supervised promotion), which only the Maintainer may
run. This plan's Sequence therefore ends at a **Maintainer-gated** Chunk D —
parked, not executed by the implementing agent — analogous to the
release-gated-plan pattern (`doctrine/plans.md` > "Release-gated plans"): the
plan may sit `executing` past code review until the Maintainer runs Phase 4,
at which point a final commit records the outcome and archives.

## Sequence

```
A. P4 + P5 + P6 -- legal/doc text, no code, no re-anchor risk       [commit pending]
B. P2 -- SPDX headers (comment-only, AST-invisible, proven by diff) [commit pending]
C. P1 -- NOTICE.md + _CORE_MAPPINGS entry (STOPS before re-anchor)  [commit pending]
D. Supervised re-anchor (Maintainer-gated, Phase 4)                 [parked -- not this agent's act]
```

### Chunk A — P4, P5, P6 (legal/doc text)

| # | File | Change |
|---|------|--------|
| A1 | `bootstrap/BOOTSTRAP.md` | Add a "Licensing of the installed files" paragraph near the II-2 Scaffold description (`:288-304`). Reassurance-first per R12: *"Cairn asks essentially nothing of you: keep the installed `NOTICE.md`, and keep the SPDX header on any tool you redistribute."* Then, briefly: what's **not** owed (no attribution burden beyond that; no relicensing of your own code), and a pointer to `NOTICE.md`. 3-4 sentences, no legalese. |
| A2 | `case-studies/README.md` | One sentence near the contribution invite (`:88-99`): a case study contributed to Cairn is offered under the same CC BY 4.0 / MIT split as the rest of the repository (the inbound=outbound statement P5 asks for). |
| A3 | `LICENSE-CC-BY.md` | P6, canonical home (R6): extend Exception 1 (`:14-19`, which already reads "Any source-code file (`.py` or other code) is MIT, wherever it lives") with a clarifying example: functional configuration/data files that are operational parts of the tools (`.yml`/`.txt`, e.g. `vendor_targets.yml`, `content_scan_*.txt`) are "other code," not prose — reframed per R5 as an example of Exception 1's *existing* coverage, not a coverage change. |
| A4 | `LICENSE-MIT.md` | One-clause pointer in the scope note (`:3-13`) to Exception 1's fuller "other code" definition in `LICENSE-CC-BY.md`, so the two instruments stay consistent (R6) without duplicating the example. |

`LICENSE-CC-BY-ND.md` is **not** edited: its source-code bullet (`:19-22`)
already cross-references `LICENSE-MIT.md` rather than independently asserting
scope, so R6's "point to the canonical home" is already structurally
satisfied there.

### Chunk B — P2 (SPDX headers)

**The populations (verified this session, not re-derived from the proposal's
prose):**

| Set | Count | Header purpose |
|---|---|---|
| `templates/**/*.py` (manifest sources) | 44 | Self-propagating — the adopter-facing compliance core of P2. |
| `scripts/**/*.py` + `tools/**/*.py` that are byte-identical self-hosted twins of a `templates/` source | 41 (18 in `scripts/`, 23 in `tools/`) | Own-repo consistency — **must** be updated in lockstep with their `templates/` source or `install.py`'s divergence/`base_hash` check reds on Cairn's own tree (`install.py:1547-48`, `:1559-69`). **Extends R3's named examples (`scripts/claim_check.py`, `link_check.py`, the `_onboarding/*` package) to `tools/` twins too** — the same divergence-check invariant applies uniformly to every self-hosted destination, not only the ones the review happened to name; flagged here for plan-review to confirm. |
| `scripts/*.py` never shipped (Cairn-own dev tooling: `check_cairn.py`, `measurements.py`, `quality_gate.py`, `quality_gate_unused_def_whitelist.py`, `token_budget.py`, `verify_counts.py`) | 6 | Own-repo MIT hygiene (R3) — correct to do, non-propagating, explicitly named in the proposal's `Touches` line ("scripts/"). |

91 files total. Header (after any shebang — 34 of the 44 `templates/` sources
carry one, R10): two lines,
`# SPDX-License-Identifier: MIT` /
`# Copyright (c) 2026 Anthony Kendall and the Cairn contributors`,
followed by a blank line before existing content.

| # | File | Change |
|---|------|--------|
| B1 | a throwaway header-insertion script (scratch, not committed) | Mechanical: for each of the 91 files, detect an optional line-1 shebang, insert the two-line header + blank line immediately after (or at the true top if no shebang), skip a file that already carries the header (idempotent). Applied to `templates/` sources and their `scripts/`/`tools/` twins **identically** (same two lines, same placement) so byte-identity is preserved. |
| B2 | `bootstrap/tests/test_notice_install.py` (new) | Two assertions: (i) every manifest `.py` source under `templates/` carries the SPDX header within its first 3 lines (scans first ~3 lines, not only line 1, per R10); (ii) a new parity check — every `scripts/`/`tools/` file identified as a `templates/` twin is still byte-identical to its source post-header (closing the gap R3 flagged: "no parity test was found to catch it"). |
| B3 | verification only, no file change | Confirm P2 is AST-invisible: re-run `python -m pytest bootstrap/tests/test_ast_attest.py`, diff the CHANGED-symbol set against the pre-chunk baseline (`/tmp/ast_baseline_before_dedup.txt`, 133 symbols, captured this session before any edit) — the sets must be **identical** (comment-only edits, per R1's `ast.dump(include_attributes=False)` finding). Any new CHANGED entry here would mean a header landed somewhere it changes logic (a bug), not a re-anchor-worthy change. |

### Chunk C — P1 (NOTICE.md + `_CORE_MAPPINGS`)

| # | File | Change |
|---|------|--------|
| C1 | `templates/core/NOTICE.md` (new) | Adopter-facing notice, reassurance-first (R12) opening line mirroring A1's tone. Carries, in order: (a) the MIT copyright + permission notice **verbatim** from `LICENSE-MIT.md:15-33`; (b) the CC BY 4.0 attribution block **verbatim** — the "How to attribute" example at `LICENSE-CC-BY.md:56-61` (the Cairn citation blockquote); (c) a CC BY-ND note for the brand mark, summarizing `LICENSE-CC-BY-ND.md`; (d) the source-repo URL (`https://github.com/MSUHydrogeology/cairn-scientist-ai-teams`, `CITATION.cff:18`). |
| C2 | `NOTICE.md` (new, repo root) | Cairn's own copy, added in the same commit so the self-host tree is consistent (P1's own instruction). |
| C3 | `bootstrap/_scaffold/config.py` | Add `("core/NOTICE.md", "NOTICE.md")` to `_CORE_MAPPINGS` (`:165`). This is the edit that moves `Assign:_CORE_MAPPINGS` off its baselined digest and is the **sole** trigger for the Chunk D re-anchor (R1). |
| C4 | `bootstrap/tests/test_notice_install.py` (extend) | P1 assertions: the notice installs to the adopter target, is recorded in the lockfile `files[]`, and appears in `--manifest` (manifest data rows move 94 → 95). |

**Verification-before-stop (C5, no file change):** re-run
`python -m pytest bootstrap/tests/test_ast_attest.py`; the CHANGED set must
now equal the Chunk-B-confirmed baseline **plus exactly one new entry**,
`Assign:_CORE_MAPPINGS` in `bootstrap/_scaffold/config.py`. Record the exact
before/after diff in the commit message and in the Code review section below
— this is the "inspect the current CHANGED set first, confirm every drifted
symbol is an already-accepted change" step the Revised proposal requires
before any re-anchor. **The implementing agent stops here.** No re-anchor
command runs in this plan's commits.

### Chunk D — supervised re-anchor (Maintainer-gated; not executed by this agent)

Per `bootstrap/REANCHOR_RUNBOOK.md` Phase 4 (Phase 0's trust root already
exists at `refs/cairn/gate-anchor`). The Maintainer runs the promotion over
the Chunk C commit as candidate `C`; on success this closes the pre-existing
Issue #1 baseline drift as a reviewed side effect (not a blind absorption),
since Chunk C's verification step confirms the CHANGED set contains nothing
unexpected. Once run, a final plan commit records the resulting `N` SHA,
confirms `test_ast_attest.py` green, and archives this plan.

## Acceptance criteria

* **Tests that must pass** — `bootstrap/tests/test_notice_install.py` (new,
  both P2 and P1 assertions + the new twin-parity check); `bootstrap/tests/test_manifest.py`
  (extends cleanly to 95 rows, no duplicate-destination trip);
  `bootstrap/tests/test_lockfile_module.py` (unaffected — P3 is out of scope);
  the full `python -m pytest bootstrap/tests` suite green **modulo**: the two
  pre-existing `test_ast_attest.py` failures (Issue #1 + this plan's Chunk C
  addition, until Chunk D lands) and the separately-tracked clock-expired
  `test_evolution_infer.py` case.
* **Doc updates that must land** — `bootstrap/BOOTSTRAP.md` (A1);
  `case-studies/README.md` (A2); `LICENSE-CC-BY.md` (A3); `LICENSE-MIT.md`
  (A4); `templates/core/NOTICE.md` + repo-root `NOTICE.md` (C1, C2). All
  hand-authored Markdown; no generator, no snippet-sync surface touched.
* **Examples / smoke checks required** — `python bootstrap/scaffold.py --manifest`
  shows the `NOTICE.md` row (95 total); a scratch install into an empty
  target, then inspect the target's `NOTICE.md`, a shipped tool's SPDX
  header, and confirm no unrelated file changed; `python scripts/check_cairn.py`
  clean over every edited/new Markdown file; `python scripts/claim_check.py`
  clean over this plan and every proposal-listed forward-reference path.
* Inbound path-link updates: none required (`PLANNING.md` / `NEXT_SESSION.md`
  refer to plans by filename stem).

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.** (i) Every install writes exactly one `NOTICE.md`, recorded
  in `files[]` and `--manifest` — *enforced by* `test_notice_install.py` +
  the existing no-duplicate-destination guard. (ii) Every shipped `.py`
  carries an SPDX header within its first 3 lines — *enforced by*
  `test_notice_install.py`. (iii) Every self-hosted twin stays byte-identical
  to its `templates/` source after headers land — *enforced by* the new
  parity check (B2), closing the gap R3 named. (iv) P2 never changes an AST
  digest — *enforced by* the Chunk-B before/after CHANGED-set diff (B3).
* **Failure modes.** A missing/unreadable file during the header sweep is
  refused loudly (the throwaway script errors rather than silently skipping);
  a duplicate `NOTICE.md` destination fails closed at the existing
  `install.py:1348-54` guard; an AST digest change where only a comment was
  expected is a **closed** failure caught by B3 before Chunk C ever runs (so
  a genuine logic-touching mistake in the header sweep cannot masquerade as
  the expected re-anchor trigger).
* **Edge cases.** An adopter who deletes `NOTICE.md` gets it re-offered on
  the next `upgrade` (a core file); a `--force` re-run overwrites it like any
  other core file; a shipped `.py` with no shebang gets the header at the
  true top (10 of the 44 `templates/` sources, per R10's shebang count).
* **Public-path → test mapping.** `NOTICE.md` install path →
  [`bootstrap/tests/test_notice_install.py`](../../bootstrap/tests/test_notice_install.py)
  (populated once Chunk B/C land). `_CORE_MAPPINGS` membership →
  the existing `bootstrap/tests/test_manifest.py`.
* **Known omissions.** No runtime gate fails a build on a missing notice
  (advisory-only, matching the proposal); trees installed by earlier Cairn
  versions are not retro-attributed (their next `upgrade` brings the notice
  in); `bootstrap/_scaffold/`/`bootstrap/tests/` headers are out of scope
  (see Scope fence); the CC-BY downstream-permission clause is not added
  (Decision).

## Verification

```
python -m pytest bootstrap/tests
python -m pytest bootstrap/tests/test_notice_install.py -v
python -m pytest bootstrap/tests/test_ast_attest.py -q   # before/after diff, each chunk
python scripts/check_cairn.py
python scripts/claim_check.py <each changed/new file>
python scripts/quality_gate.py --sub neutrality
python bootstrap/scaffold.py --manifest
```

## Plan review

*Filled in below once the fresh-context Internal pass lands.*

## Code review

*Filled in after implementation commits land (Chunks A-C; Chunk D is
Maintainer-gated and reviewed separately once it runs).*

## Lasting-truth migration

*Filled in at archive time — which for this plan is gated on Chunk D (the
Maintainer's supervised re-anchor), not solely on code review. See "The
re-anchor gate" above.*

Per the [Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home outside
the plan.

This section is append-only once written.
