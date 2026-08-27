<!-- The three paths above are forward-reference files this plan creates; they materialize as the chunks land. -->

# Plan: adopter licensing compliance (P1, P2, P4, P5, P6)

**Source proposal**: `dev/proposals/archive/2026-07-11-claude-adopter-licensing-compliance.md`
**Status**: archived
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

**The re-anchor gate (why this plan cannot fully archive on its own; corrected
per plan-review PR1, then corrected again on an interpreter-version finding
— see Chunk D for the full account).** Chunk C's `_CORE_MAPPINGS` edit moves
an AST-baselined symbol off its committed digest. The mechanism that
actually governs that file (`bootstrap/tests/_ast_attest.py update-symbol`)
refuses to run while unrelated drift is present. Under the sandbox's default
interpreter (Python 3.12) that looked like 133 symbols; under the
project's canonical interpreter (`lhm`, Python 3.13 — `ast.dump` digests are
minor-version-sensitive) it is exactly **one**: `print_report` in
`bootstrap/_scaffold/install.py`, a stale baseline hash left over from an
already-reviewed change earlier this session (`63db56f`). Because
`print_report` isn't an allowlisted symbol, closing this gate still needs a
Maintainer-supervised direct baseline correction, not a self-run command —
same "implementer must not bless its own verifier" principle
`bootstrap/REANCHOR_RUNBOOK.md` states for its own (different) ceremony —
but it is now a small, well-understood fix, not a wholesale regeneration.
This plan's Sequence therefore ends at a
**Maintainer-gated** Chunk D — parked, not executed by the implementing
agent — analogous to the release-gated-plan pattern (`doctrine/plans.md` >
"Release-gated plans"): the plan may sit `executing` past code review until
the Maintainer runs the re-pin, at which point a final commit records the
outcome and archives.

## Sequence

```
A. P4 + P5 + P6 -- legal/doc text, no code, no re-anchor risk       [commit pending]
B. P2 -- SPDX headers (comment-only, AST-invisible, proven by diff) [commit pending]
C. P1 -- NOTICE.md + _CORE_MAPPINGS entry (STOPS before re-anchor)  [commit pending]
D. Supervised AST baseline re-pin (Maintainer-gated, NOT Phase 4)   [parked -- not this agent's act]
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
scope. This is a **transitive**, not direct, satisfaction of R6's "point to
the canonical home" (ND → MIT → CC-BY's Exception 1, not a direct ND → CC-BY
pointer like A4's) — correctly per plan-review PR3: defensible given the
existing triangular cross-reference structure, not worth a fourth edit, but
not identical to A4's treatment.

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
| B3 | verification only, no file change | Confirm P2 is AST-invisible: re-run `python -m pytest bootstrap/tests/test_ast_attest.py` **under the canonical `lhm`/Python 3.13 interpreter** (`ast.dump` digests are minor-version-sensitive — the sandbox default Python 3.12 inflates the CHANGED set to 133 spurious entries, per Chunk D), diff against the pre-chunk baseline (exactly one entry — `FunctionDef:print_report` in `install.py`, captured this session at `/tmp/ast_baseline_before_lhm.txt`) — the sets must be **identical** (comment-only edits, per R1's `ast.dump(include_attributes=False)` finding). Any new CHANGED entry here would mean a header landed somewhere it changes logic (a bug), not a re-anchor-worthy change. |

### Chunk C — P1 (NOTICE.md + `_CORE_MAPPINGS`)

| # | File | Change |
|---|------|--------|
| C1 | `templates/core/NOTICE.md` (new) | Adopter-facing notice, reassurance-first (R12) opening line mirroring A1's tone. Carries, in order: (a) the MIT copyright + permission notice **verbatim** from `LICENSE-MIT.md:15-33`; (b) the CC BY 4.0 attribution block **verbatim** — the "How to attribute" example at `LICENSE-CC-BY.md:56-61` (the Cairn citation blockquote); (c) a CC BY-ND note for the brand mark, summarizing `LICENSE-CC-BY-ND.md`; (d) the source-repo URL (`https://github.com/MSUHydrogeology/cairn-scientist-ai-teams`, `CITATION.cff:18`). **Per plan-review PR2: these line numbers are pre-Chunk-A.** Chunk A (A3/A4) inserts new clauses above both cited ranges, shifting them down — locate the two verbatim blocks live in the post-Chunk-A files by content (the copyright-through-disclaimer paragraph; the "How to attribute" blockquote), not by trusting these line numbers. |
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

### Chunk D — supervised baseline re-pin (Maintainer-gated; not executed by this agent; corrected per plan-review PR1)

**Not `bootstrap/REANCHOR_RUNBOOK.md` Phase 4.** Plan-review PR1 found, and
this session independently re-verified, that `scaffold_ast_baseline.json` and
`bootstrap/_scaffold/config.py` are explicitly **excluded** from the
differential-oracle gate's frozen-hash surface —
`bootstrap/tests/_gate_manifest.py`'s own `CASCADE_MUTABLE` dict (`:77-82`)
names both, with the comment "integrity governed by the named mechanism, not
a byte hash," and `REANCHOR_RUNBOOK.md` itself never mentions `ast_attest` or
`scaffold_ast_baseline.json` anywhere (`grep` confirms zero hits). Running
Phase 4 would not touch this file at all. The Decision's "supervised AST
re-anchor... per `bootstrap/REANCHOR_RUNBOOK.md`" citation is a genuine,
load-bearing citation error, inherited into the plan from the proposal (and
present verbatim in the sibling `first-session-survivability` proposal's
Decision too — flagged, not yet corrected there).

**The actual mechanism is `bootstrap/tests/_ast_attest.py update-symbol`**
(confirmed both by `_gate_manifest.py`'s own docstring and directly:
`_CORE_MAPPINGS` is in `_UPDATE_ALLOWLIST`, `_ast_attest.py:144`).

**Correction to the plan-review's own captured evidence (found immediately
after Sharpening, before this plan-review commit landed): the "133
CHANGED symbols" figure is an interpreter-version artifact, not real
drift.** `_ast_attest.py:24-30`'s own docstring warns that `ast.dump`
digests are Python-minor-sensitive and mandates the canonical `lhm`
(Python 3.13) interpreter; this session's captures — including the plan
review's — ran under the sandbox default (`python3`, 3.12.9). Re-run under
`/Users/kendal30/conda_envs/lhm/bin/python3` (3.13.13): **exactly one**
CHANGED symbol, `FunctionDef:print_report` in `bootstrap/_scaffold/install.py`
(`baseline c3fb06e5... != 19c50962...`) — not 133. `git log -- bootstrap/_scaffold/install.py`
traces it to `63db56f` ("implement adopter-entry-doc-refresh"), a commit
*from earlier in this same session*, whose own code review already
confirmed at the time: *"this commit's `install.py` edit only moves
`print_report`'s hash (no new drifting function, no new failure)"* — i.e.
this is a small, already-understood, already-reviewed piece of technical
debt (a baseline hash never re-recorded after an accepted change), not a
133-symbol mystery.

**Why this still doesn't close cleanly without the Maintainer.**
`print_report` is **not** in `_UPDATE_ALLOWLIST` (only the three mapping
symbols + `install_onboarding` are), so `update-symbol` cannot surgically
fix it — and while it remains CHANGED, `update-symbol` will still refuse to
write `_CORE_MAPPINGS` too ("unrelated drift present," one-symbol-delta
rule). Resolving `print_report`'s stale hash requires a **direct baseline
edit outside the allowlist/`--expect-old` guard** — exactly the
"implementer blesses its own verifier" self-authorization class of action
this plan does not perform. **What actually needs to happen (Maintainer-gated,
not this agent's act):** under the canonical `lhm` interpreter, confirm
`print_report`'s live digest is the expected one from `63db56f` (a one-line
check), correct its baseline entry, then run
`_ast_attest.py update-symbol _CORE_MAPPINGS --expect-old <digest>` for this
plan's own addition (now the sole remaining CHANGED symbol, so the
allowlisted, guarded path applies cleanly). Once done, a final plan commit
records the outcome, confirms `test_ast_attest.py` green under `lhm`, and
archives this plan.

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
  `bootstrap/tests/test_notice_install.py` (not yet real; linked once Chunk
  B/C land). `_CORE_MAPPINGS` membership →
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
python -m pytest bootstrap/tests/test_ast_attest.py -q   # before/after diff, each chunk -- run under the canonical lhm/Python 3.13 interpreter (ast.dump digests are interpreter-minor sensitive, per plan-review PR4)
python scripts/check_cairn.py
python scripts/claim_check.py <each changed/new file>
python scripts/quality_gate.py --sub neutrality
python bootstrap/scaffold.py --manifest
```

## Plan review -- Claude (Internal, fresh-context) -- 2026-07-22

**Attribution / committer note.** Fresh-context subagent read of this plan
(Internal floor: same agent type, fresh session). The subagent cannot
commit; the author-session commits this section as a disclosed scribe, the
accepted deviation model used throughout this repo's lifecycle (see e.g.
`dev/plans/archive/review-record-integrity.md`).

**Model**: Claude Sonnet 5 (fresh session, no access to the plan-authoring session; read the plan, the full accepted proposal record, the runbook, both license/gate-machinery source trees, and independently re-derived every count this review names).

**Steelman.** The plan is a faithful, well-organized translation of the Revised proposal's P1+P2+P4+P5+P6 into four sequenced chunks, and its concrete specifics hold up under independent re-derivation to a degree that's unusual for a plan this size. I recomputed every population claim in the Chunk B table from the live tree rather than trusting the plan's prose, and every number reproduced exactly: 44 `templates/**/*.py` manifest sources (`python bootstrap/scaffold.py --manifest` and `find templates -name '*.py'` agree, zero diff); 41 byte-identical `scripts/`+`tools/` twins split precisely 18/23 (verified via `diff -q` against each twin's `templates/` source — zero mismatches — after excluding the 3 manifest-listed `scripts/` destinations, `content_scan.py`/`content_scan_runner.py`/`run_security_audit.py`, that don't actually exist in Cairn's own `scripts/` tree); the 6 named own-only dev-tooling files confirmed to have zero manifest hits; 91 total (44+41+6, arithmetic checks); the 34/10 shebang split confirmed byte-for-byte. The legal-text line citations for the *current* file state are all correct — `LICENSE-MIT.md:15-33` is exactly the copyright-through-disclaimer block, `LICENSE-CC-BY.md:56-61` is exactly the "How to attribute" blockquote, `LICENSE-CC-BY.md:14-19` is exactly Exception 1, `LICENSE-MIT.md:3-13` is exactly the scope note, and `LICENSE-CC-BY-ND.md:19-22` does cross-reference `LICENSE-MIT.md` rather than independently asserting scope, as claimed. The extension of "in-lockstep" twin headers from R3's three named examples to *all* `scripts/`+`tools/` twins is justified, not overreach: `install.py`'s divergence check (`:1547-48`) and base-hash recording (`:1559-69`) sit inside a loop over `_lock_file_list(modules, optional)` that is not scoped to any one source directory, so the same-hash-fails-clean invariant genuinely applies uniformly, `tools/` included. `refs/cairn/gate-anchor` does exist (`git show-ref`), so the Phase-0-already-established claim is correct. `claim_check.py` runs clean over the plan, and the AST comment-insensitivity claim for P2 is correct — `ast.dump(include_attributes=False)` strips comments, confirmed both by reading `_ast_attest.py` and by its own `test_digest_is_position_and_comment_insensitive`. Nothing from the Revised proposal or the ratified Decision conditions appears silently dropped.

**Critiques** (descending severity):

* **[PR1] (critical — verify before Chunk D executes)** Chunk D's described mechanism does not, on the evidence, do what the plan says it does. The plan states: *"Per `bootstrap/REANCHOR_RUNBOOK.md` Phase 4 ... The Maintainer runs the promotion over the Chunk C commit as candidate `C` ... Once run, a final plan commit records the resulting `N` SHA, confirms `test_ast_attest.py` green."* I read `bootstrap/REANCHOR_RUNBOOK.md` in full (154 lines) and it never once mentions `scaffold_ast_baseline.json`, `_ast_attest.py`, or `_CORE_MAPPINGS` (`grep -i "ast" bootstrap/REANCHOR_RUNBOOK.md` — zero hits). Its title is literally "(differential-oracle gate)," and its Phase 0/4 procedure is entirely about establishing and then CAS-advancing `refs/cairn/gate-anchor`, the trust anchor for six *other* verifier modules (`_gate_reanchor.py`, `_gate_transition.py`, `_oracle_activation.py`, `_gate_manifest.py`, `_oracle.py`, `_oracle_trust.py`) and a "frozen" set of gate-defining tests/harnesses/scanners. `bootstrap/tests/_gate_manifest.py` — the module that defines what that promotion protects — has an explicit `CASCADE_MUTABLE` dict (lines 77-82) naming `bootstrap/_scaffold/config.py` and `bootstrap/tests/fixtures/scaffold_ast_baseline.json` as **excluded from frozen hashing**, with the code comment "integrity governed by the named mechanism, not a byte hash," and the verifier's own runtime behavior (line 385, `_gate_transition.py`-style diff logic) is "Cascade-mutable ... digests — report deltas, **never HOLD**." So running the Phase-4 promotion exactly as described would not itself write, validate, or gate `scaffold_ast_baseline.json` at all — it would silently pass over the file. Compounding this: Issue #1's drift is much larger than the plan's framing implies. I ran `python -m pytest bootstrap/tests/test_ast_attest.py -q` live and it reproduces the plan's own captured evidence exactly (`/tmp/ast_baseline_before_dedup.txt`, still present, 133 lines) — **133 pre-existing CHANGED symbols**, not a handful. That number rules out using the self-service `_ast_attest.py update-symbol` escape hatch (which *is* already allowlisted for `_CORE_MAPPINGS` and, per `_gate_manifest.py`'s own docstring, is the tool that actually governs this file's integrity) as a quick fix, because `update_symbol()` hard-refuses ("REFUSED — unrelated drift present") unless the target key is the *only* CHANGED symbol in the live set. Net: neither the mechanism the plan names (Phase-4 gate-anchor promotion) nor the mechanism that's actually wired to this file (`update-symbol`) will, on its own, turn `test_ast_attest.py` green here. Some third step — almost certainly a wholesale baseline regeneration (`_ast_attest.py baseline ...` over the full `_scaffold` package, reviewed line-by-line by the Maintainer to confirm all 133+1 drifted symbols are legitimate) — is the thing that actually needs to happen, and the plan never names it.
  *Grounding:* `bootstrap/REANCHOR_RUNBOOK.md` (full file, no AST/ast_attest/scaffold_ast_baseline hits); `bootstrap/tests/_gate_manifest.py:75-82` (`CASCADE_MUTABLE`), `:151-175` (`_frozen_files` excludes it), `:385-401` ("report deltas, never HOLD"), `:240-247` (`produce()` reads whatever digest is currently in `scaffold_ast_baseline.json` with no green-suite precondition); `bootstrap/tests/_ast_attest.py:209-251` (`update_symbol`'s refuse-on-unrelated-drift guard); live run `python -m pytest bootstrap/tests/test_ast_attest.py -q` → 2 failed / 24 passed, 133 CHANGED symbols, matching `/tmp/ast_baseline_before_dedup.txt` (133 lines, timestamped this session). Note this is not unique to this plan: the sibling `dev/proposals/2026-07-11-claude-first-session-survivability.md` cites the identical "supervised AST re-anchor ... per `bootstrap/REANCHOR_RUNBOOK.md`" framing (also ratified at Decision the same day), so if this citation is wrong it's a repeated pattern across both review tiers on two proposals, not a slip specific to this plan.
  *Fix:* Before Chunk D executes, have the plan (or a quick confirmation with whoever owns the gate tooling) name the *actual* command sequence that regenerates `scaffold_ast_baseline.json` — most likely a Maintainer-reviewed wholesale re-pin under the canonical `lhm`/Python 3.13 interpreter, done separately from (or in addition to, if it's genuinely required for some other reason not visible in this code) the `refs/cairn/gate-anchor` promotion. If the Phase-4 promotion turns out to be immaterial to fixing this specific file, say so explicitly and drop the Chunk-D framing to "supervised baseline re-pin," citing the real mechanism rather than `REANCHOR_RUNBOOK.md` Phase 4.

* **[PR2] (substantive — legal-text precision)** Chunk C1's line citations for the verbatim NOTICE.md quotes will already be stale by the time Chunk C executes, because the plan's own Sequence lands Chunk A — which edits both source files C1 quotes from — *before* Chunk C. A4 inserts a new clause into `LICENSE-MIT.md`'s scope note at `:3-13`, i.e. *above* line 15 where C1's "verbatim from `LICENSE-MIT.md:15-33`" quote starts; A3 inserts a new clarifying example into `LICENSE-CC-BY.md`'s Exception 1 at `:14-19`, i.e. *above* line 56 where C1's "verbatim ... at `LICENSE-CC-BY.md:56-61`" quote starts. Both cited ranges will shift down by however many lines A3/A4 add, so a literal read of the plan's citations at Chunk-C time points at the wrong text. Given the task's own emphasis that legal-text handling needs above-normal precision, this is worth naming rather than leaving implicit.
  *Grounding:* `LICENSE-MIT.md:3-13` (A4's target, above :15-33 C1 cites) and `:15-33` (verified exact copyright+permission+disclaimer block); `LICENSE-CC-BY.md:14-19` (A3's target, above :56-61 C1 cites) and `:56-61` (verified exact "How to attribute" blockquote); plan Sequence `A → B → C`.
  *Fix:* Either re-run the citation check on the post-Chunk-A file state before executing C1 (cheap — `grep -n` the two updated files), or add a one-line note in Chunk C1 instructing the implementing agent to locate the two blocks live rather than trust the plan's pre-Chunk-A line numbers. Functionally low-risk (a competent execution reads the file before copying text verbatim regardless), but worth being explicit given the stakes named in this review's brief.

* **[PR3] (minor)** R6 asked for "one canonical home with the other two pointing to it." The plan gives `LICENSE-MIT.md` a direct pointer to `LICENSE-CC-BY.md`'s Exception 1 (A4 — good), but leaves `LICENSE-CC-BY-ND.md` unedited on the reasoning that its existing bullet "already cross-references `LICENSE-MIT.md` rather than independently asserting scope." That's true, but it means CC-BY-ND's reader reaches the canonical `.yml`/`.txt` clarification only via a two-hop chain (ND → MIT → CC-BY), not a direct pointer — a partial, not full, satisfaction of "the other two pointing to it." Defensible given the existing triangular cross-reference structure between the three files, and not worth adding a fourth edit for, but the plan should say so explicitly rather than imply full symmetry with A4's direct pointer.
  *Grounding:* `LICENSE-CC-BY-ND.md:19-22` (points only to `LICENSE-MIT.md`, not directly to `LICENSE-CC-BY.md`'s Exception 1); plan text "already structurally satisfied there."
  *Fix:* One clause in the plan's LICENSE-CC-BY-ND.md note acknowledging the pointer is transitive (via MIT), not direct — so a reviewer doesn't read "structurally satisfied" as "identically satisfied."

* **[PR4] (minor)** The Verification section's `test_ast_attest.py` re-run command doesn't mention the canonical-interpreter requirement that `_ast_attest.py`'s own docstring flags as load-bearing ("`ast.dump` output ... varies across Python minor versions ... every `verify` run **must** use the project's canonical interpreter — the `lhm` env, Python 3.13"). Low risk in practice (the repo presumably always runs under `lhm`), but given PR1's finding that Chunk D likely needs a genuine baseline regeneration, this becomes more than boilerplate — a regeneration run under the wrong interpreter would produce spurious CHANGED entries that look like real drift.
  *Grounding:* `bootstrap/tests/_ast_attest.py:24-30` ("Interpreter pinning" docstring section).
  *Fix:* Add "(canonical `lhm`/Python 3.13 interpreter)" to the Chunk C5 / Verification section's `test_ast_attest.py` command lines, matching the emphasis the tool's own docs give it.

**Coverage.** Verified independently this session: all Chunk B population counts (44 templates/, 41 twins split 18 scripts/+23 tools/, 6 own-only, 91 total, 34/10 shebang split) via `scaffold.py --manifest`, `find`, and `diff -q` over every twin pair; the LICENSE-MIT.md/LICENSE-CC-BY.md/LICENSE-CC-BY-ND.md line citations against the live files; `config.py:165`'s `_CORE_MAPPINGS` location; `install.py:1515,1547-48,1559-69`'s divergence/base-hash loop and its `tools/`-inclusive scope (via `_lock_file_list`); `refs/cairn/gate-anchor`'s existence (`git show-ref`); `test_ast_attest.py`'s comment-insensitivity behavior (code + its own unit test); `bootstrap/REANCHOR_RUNBOOK.md`'s full text and `bootstrap/tests/_gate_manifest.py`'s `CASCADE_MUTABLE`/frozen-file/promotion-report code; a live `pytest bootstrap/tests/test_ast_attest.py` run (133 CHANGED, 2 failed / 24 passed) cross-checked against the plan's own `/tmp/ast_baseline_before_dedup.txt` snapshot; `python scripts/claim_check.py` and `python scripts/quality_gate.py --sub neutrality` both clean; `BOOTSTRAP.md:288-304` and `case-studies/README.md:88-99` as sane insertion points; `test_manifest.py` has no hardcoded row count to break. NOT independently verified (out of this review's reach): whether the differential-oracle gate apparatus is still an *active* standing requirement for every `bootstrap/_scaffold/` change versus a mechanism purpose-built for the historical "six-proposal superplan" batch and now potentially dormant for ordinary single-plan review — this bears directly on PR1 but is a question about tooling *intent*, not something the code alone settles; no attempt was made to actually run any part of Chunk D (correctly out of scope for an implementing agent per the ratified Decision).

### Sharpening -- Claude (author) -- 2026-07-22

All four findings accepted; none dropped.

* **[PR1] accept — independently re-verified beyond the reviewer's own
  hedged confidence.** The reviewer flagged its own coverage gap ("a
  question about tooling intent, not something the code alone settles").
  I re-ran the load-bearing checks myself: `grep -n "CASCADE_MUTABLE"
  bootstrap/tests/_gate_manifest.py` confirms the dict and its four use
  sites; the module's docstring block (`:14-24`) states outright that
  `config.py` / `scaffold_ast_baseline.json` integrity is "governed by the
  AST source-motion attest ... + the hardened `_ast_attest.py
  update-symbol`," not the differential-oracle gate; `grep -n
  "_CORE_MAPPINGS" bootstrap/tests/_ast_attest.py` independently confirms
  the allowlist entry at `:144`. This is not a coverage gap the reviewer
  merely couldn't rule out — it is confirmed, load-bearing, and it means
  the Decision's re-anchor citation is a genuine error (the same misquote
  class the `review-record-integrity` proposal exists to catch, now found
  in two more Decided proposals). **A second correction on top of the
  first:** re-running the reviewer's own "133 CHANGED symbols" capture
  under the project's canonical `lhm`/Python 3.13 interpreter (rather than
  the sandbox default 3.12 both the review and this plan's earlier
  captures used) drops the count to **exactly one** — `print_report` in
  `install.py`, a stale baseline hash from an already-reviewed commit
  earlier this session (`63db56f`). Fixed: Chunk D and the Scope section's
  "re-anchor gate" note are rewritten above to name the real mechanism
  (`update-symbol`) and the actual, now much smaller, remediation (a
  Maintainer-supervised correction of one stale baseline entry, then a
  clean allowlisted `update-symbol` run for `_CORE_MAPPINGS`). This is
  surfaced to the Maintainer directly (see the session's user-facing
  message) rather than silently corrected only in the plan file.
* **[PR2] accept.** Chunk C1 now carries an explicit note: locate the two
  verbatim source blocks live in the post-Chunk-A files rather than trust
  this plan's pre-Chunk-A line numbers, since A3/A4 land first and shift
  both cited ranges down.
* **[PR3] accept.** The `LICENSE-CC-BY-ND.md` note is corrected to say the
  pointer is *transitive* (ND → MIT → CC-BY's Exception 1), not a direct
  R6-style pointer, so it isn't read as identical to A4's treatment.
* **[PR4] accept.** The Verification section's `test_ast_attest.py` line
  now notes the canonical `lhm`/Python 3.13 interpreter requirement,
  load-bearing for Chunk D's eventual regeneration, not just boilerplate.

**Status: awaiting-plan-review → executing.** All findings disposed;
Chunks A and B do not depend on PR1's resolution and proceed as planned;
Chunk C proceeds through implementation and its own verification step
(unaffected by which mechanism eventually reconciles the baseline); Chunk
D's corrected framing is surfaced to the Maintainer before any baseline-
mutating command runs, per the standing rule that this agent does not
self-authorize that class of action.

## Code review -- Claude (sub-agent, fresh context, not the implementer) -- 2026-07-22

**Attribution / committer note.** Fresh-context subagent review of the four
implementation commits; the subagent cannot commit, so the author-session
commits this section as a disclosed scribe, the accepted deviation model
used throughout this repo's lifecycle.

**Verdict: Accept-with-followups**, applying to the four commits `597c882` (Chunk A), `501efe3` (Chunk B), `a8bb2a7` (Chunk C), `c7a144b` (Chunk C follow-up).

**Model**: Claude Sonnet 5, fresh session, no access to the implementing session. Read all four diffs in full, the plan (including Plan review + Sharpening), the accepted proposal's Revised proposal + Decision, every touched legal instrument, and independently re-ran every gate the commit messages cite.

### Falsification ledger

**Legal-text fidelity (the highest-stakes surface).**
* MIT block in `templates/core/NOTICE.md` diffed byte-for-byte against `LICENSE-MIT.md:19-37` (copyright line through the disclaimer paragraph) — `diff` empty, **verbatim**.
* CC BY 4.0 attribution blockquote in `NOTICE.md` diffed against `LICENSE-CC-BY.md:62-64` ("How to attribute" example) — identical apart from the intentional `cairn-accept` HTML-comment marker inserted between the visible lines (invisible when rendered) — **verbatim**.
* `NOTICE.md` (repo root) is byte-identical to `templates/core/NOTICE.md` (`diff` empty).
* P6's `.yml`/`.txt` reframing checked in both `LICENSE-CC-BY.md` (Exception 1) and `LICENSE-MIT.md` (pointer clause) — matches the plan's A3/A4 text; `LICENSE-CC-BY-ND.md` correctly left unedited (its bullet already cross-references `LICENSE-MIT.md`).
* `bootstrap/BOOTSTRAP.md`'s new paragraph names `NOTICE.md` by backtick only, no markdown link (correct — the plan required this since the file didn't exist until Chunk C); `case-studies/README.md` links only to the two real LICENSE files.

**`_CORE_MAPPINGS` edit.** Read `bootstrap/_scaffold/config.py:165-171` — `("core/NOTICE.md", "NOTICE.md")` is correctly placed in the repo-root section immediately after `AGENTS.md`, with an explanatory comment. `python3 bootstrap/scaffold.py --manifest` → 96 lines (1 header + 95 data rows), `NOTICE.md ← core/NOTICE.md, substituted` present — matches AGENTS.md's own row shape (`substituted`, not `verbatim`), i.e. no unintended behavioral divergence.

**91-file SPDX sweep (P2).** `git show --numstat 501efe3` → 71 `templates/`+`scripts/`+`tools/` files touched but the true population (correcting for `git --stat`'s path truncation, confirmed via `--numstat`) is 44 `templates/` + 24 `scripts/` + 23 `tools/` = **91**, matching the plan and commit message exactly. All 91 files carry byte-identical two-line headers (`grep`-verified, one unique SPDX line, one unique copyright line across the whole set); all 91 `py_compile` clean; header placement correct in both populations — after the shebang (34/44 `templates/` sources, confirmed by direct count) and at the true top for the 10 shebang-less sources — with the required blank line before existing content in both cases (spot-checked). Twin byte-identity spot-checked across 8 pairs (`claim_check.py`, `link_check.py`, `evolution_infer.py`, `lifecycle_metrics.py`, `intent.py`, `lifecycle.py`, `prune_reflections.py`, `_onboarding/cli.py` ↔ its `_intent/cli.py` decoy which correctly *differs*, confirming the diff tool itself works) — all identical. `docs/tool-usage.md`'s `claim_check_watch_file_lines` invariant (837→840) verified live: `wc -l scripts/claim_check.py` = 840, `python3 scripts/verify_counts.py docs/tool-usage.md` → "matches."

**The three claimed bugs-fixed-during-implementation.**
1. `test_skills_security.py`'s "kendal" leak scan: the fix does an exact `str.replace()` of the one deterministic copyright line (not a regex, not a lowercase/partial match), so any other "kendal" occurrence — a leaked path fragment, a stray debug string — still fails the test. Precise, not overbroad. `pytest bootstrap/tests/test_skills_security.py` → 10 passed.
2. `test_generated_output_scan.py`'s NOTICE.md-by-name exclusion (added in `a8bb2a7`) is fully reverted in `c7a144b` — `git diff a8bb2a7~1 HEAD -- bootstrap/tests/test_generated_output_scan.py` is **empty**, confirming byte-identical to the pre-P1 state, no leftover special-casing. Independently ran `content_scan.scan_file` against the committed `templates/core/NOTICE.md` → `[]` (clean via the standard `cairn-accept` mechanism, not a test carve-out). Confirmed the mechanism is doing real work, not vacuous: stripping the two markers from a scratch copy and re-scanning reproduces both original flags (`suspicious-url` at lines 5 and 42). Both markers sit on the line immediately preceding the flagged URL line — including the blockquote case (`> <!-- cairn-accept: ... -->` immediately before `> <https://...>`) — which satisfies `content_scan.py`'s own documented "own line or immediately-preceding line" scope rule (`templates/modules/team-gated/content_scan.py:62-63`), confirmed empirically rather than just by reading the docstring.
3. Vendor-neutrality: `python3 scripts/quality_gate.py --sub neutrality` → **99** FAIL lines at current HEAD (matches "fail=99, was 100" in `c7a144b`); zero FAIL/info lines reference `NOTICE.md`, `LICENSE-*.md`, `BOOTSTRAP.md`, or `case-studies/README.md`; `reviewer="agent"` confirmed in both marker lines, no `reviewer="Claude"` anywhere in the diffs.

**The AST re-anchor citation correction — independently re-derived, not trusted.**
* `grep -n -iE 'ast_attest|scaffold_ast_baseline' bootstrap/REANCHOR_RUNBOOK.md` → **zero hits**, confirming the Decision's "per `REANCHOR_RUNBOOK.md`" citation is a genuine error.
* `bootstrap/tests/_gate_manifest.py:77-82`'s `CASCADE_MUTABLE` dict does explicitly exclude `bootstrap/_scaffold/config.py` and `bootstrap/tests/fixtures/scaffold_ast_baseline.json` from the frozen-hash gate, with the comment "integrity governed by the named mechanism, not a byte hash" — read directly, confirmed.
* **Interpreter-version claim, re-run from scratch under both interpreters** (not just at HEAD — at the exact commits the plan's narrative describes, via disposable `git worktree`s, cleaned up afterward):
  - At `51f2c10` (plan-review point, pre-Chunk-A): sandbox default `python3` (3.12.9) → **133** unique CHANGED symbols.
  - At `501efe3` (post-Chunk-B): canonical `lhm`/`python3` (3.13.13) → **exactly 1** CHANGED symbol, `FunctionDef:print_report` — proving P2 is AST-invisible as claimed.
  - At `a8bb2a7` (post-Chunk-C): canonical `lhm` → **exactly 2** CHANGED symbols, `Assign:_CORE_MAPPINGS` + `FunctionDef:print_report` — exactly "Chunk-B baseline plus exactly one new entry," as the commit message claims.
  - At current HEAD, sandbox default `python3` (3.12) → **134** unique CHANGED symbols, not 133. This is **not a discrepancy**: it is the pre-Chunk-C 133 (132 interpreter artifacts + `print_report`) plus exactly one new real entry, `Assign:_CORE_MAPPINGS`, from Chunk C — confirmed by diffing the symbol sets directly. The plan's own logic predicts exactly this delta; I verified it rather than assuming it.

**Regression / gate sweep at current HEAD.**
* `python3 -m pytest bootstrap/tests -q` → **1418 passed / 3 skipped / 3 failed**, matching `c7a144b`'s claim exactly. The 3 failures (`test_ast_attest.py` x2, `test_evolution_infer.py`'s clock-expired case) independently confirmed **pre-existing** — reproduced identically at `597c882~1` (before any of the four reviewed commits), via a throwaway worktree.
* `python3 scripts/check_cairn.py` → OK, 163 files, no issues.
* `python3 scripts/claim_check.py templates/core/NOTICE.md` and `NOTICE.md` → clean, both.
* `python3 scripts/link_check.py` over all 8 touched/new docs (NOTICE.md ×2, BOOTSTRAP.md, case-studies/README.md, the three LICENSE files, the plan itself) → OK, no issues.
* One **pre-existing, unrelated** `claim_check.py` hard flag found in passing: `case-studies/README.md:67` cites dev/plans/cairn_methodology_repo.md (a path in the external `modflow_tools` repo, not this one). Confirmed present verbatim at `597c882~1`, i.e. it predates and is untouched by this plan's work — not a regression, not this plan's responsibility, but worth a note since `check_cairn.py`'s repo-wide run doesn't currently surface it as a hard stop the way a direct `claim_check.py <file>` invocation does.

### Coverage

Verified independently: all legal-text verbatim-quote claims (byte-diffed); the `_CORE_MAPPINGS` edit's placement and manifest-row effect (96-line `--manifest` output, live); the 91-file population split (44/24/23, cross-checked via `--numstat` against the plan's claim); twin byte-identity (8 pairs spot-checked, including a deliberately-mismatched pair to sanity-check the diff methodology itself); the 34/10 shebang split (recomputed independently, matches plan-review's own recount); all 91 files' `py_compile` cleanliness; the `docs/tool-usage.md` count update (live `verify_counts.py` run); both bug fixes' precision (read the diffs, ran the affected test files); the `cairn-accept` marker mechanism's non-vacuity (stripped-and-rescanned, not just docstring-read); the vendor-neutrality fix (live `quality_gate` run, zero hits on touched files); the AST re-anchor citation correction **from first principles**, at the actual historical commits, under both interpreters, rather than trusting the plan's prose — every number reproduced exactly, including the 133→134 shift the plan's own logic (but not its prose) predicts; the 3 pre-existing test failures' pre-existence (reproduced at the pre-Chunk-A commit); full-suite pass count; `check_cairn`/`link_check`/`claim_check` cleanliness.

**Not independently re-verified** (out of this review's reach, and not required by the task brief): the Gemini External review's own legal-sufficiency reasoning (E1) as a matter of copyright law — I verified the *mechanics* match what both reviews describe, not the underlying legal-sufficiency judgment itself, which is outside a code review's competence; whether any adopter-side tooling beyond this repo's own gates would choke on the `cairn-accept` HTML comments inside a rendered blockquote (cosmetically they're invisible in every Markdown renderer checked by inspection, but no external renderer was tested).

### Required follow-ups

1. **Chunk D remains open and Maintainer-gated, as the plan itself states** — `print_report`'s stale baseline hash (from `63db56f`, unrelated to this plan) still blocks a clean `update-symbol` run for `_CORE_MAPPINGS`. Nothing in these four commits should attempt to close it; this is a note, not a defect.
2. **Optional, low-priority, out-of-scope**: `case-studies/README.md:67`'s stale cross-repo path citation (pre-existing, unrelated to licensing) could use its own small fix at some point, but does not belong to this plan and should not block its own code review or archive.

No correctness defect, no legal-text inaccuracy, and no scope deviation was found in any of the four commits.

### Sharpening -- Claude (author) -- 2026-07-22

Both follow-ups noted, neither requires a code change:

* **[1] acknowledged.** Chunk D stays exactly as designed -- Maintainer-gated,
  parked, not this agent's act. No change.
* **[2] acknowledged, out of scope.** `case-studies/README.md:67`'s stale
  cross-repo citation predates this plan and is unrelated to licensing
  compliance. Not fixed here to avoid scope creep into an unrelated
  pre-existing gap; a candidate for its own small future fix.

**Status: executing → review** (not `archived`): code review has landed, so
the plan advances to `review` per the normal lifecycle, but it cannot reach
`archived` yet. Per the plan's own "re-anchor gate" section, that requires
the Maintainer to run the supervised baseline correction (Chunk D) first.
The plan is otherwise complete and gate-clean, parked at `review` exactly
like a release-gated plan pending that one external, Maintainer-only act.

## Lasting-truth migration

Archived 2026-07-22.

Follow-ups migrated to: the only deferred follow-up from this plan's scope
is P3 (the lockfile `source_repository` + `licenses` fields, withdrawn at
proposal stage per R4/E3) — it already has its own durable home: the
proposal `dev/proposals/2026-07-22-claude-lockfile-provenance-fields.md`
(Status: revised as of archive time), opened and carried forward
independently of this plan. No other deferred follow-up exists; P4/P5/P6
landed in full, and the CC-BY downstream-permission clause was declined
outright at Decision (not deferred — a closed question, not an open one).

**Chunk D closed.** The Maintainer ran the supervised baseline correction:
commit `e1eec63` ("Updated baseline") surgically updated exactly the two
reviewed keys (`FunctionDef:print_report`, `Assign:_CORE_MAPPINGS`) in
`bootstrap/tests/fixtures/scaffold_ast_baseline.json` — a 5-insertion/
5-deletion diff (digest + span per key), every other one of the 174 entries
untouched — using the dry-run-verified script this plan's implementing
session prepared and handed off (never run by the implementing agent
itself, per `bootstrap/REANCHOR_RUNBOOK.md`'s "must not bless its own
verifier" principle, extended here to the correctly-identified real
mechanism). Verified post-commit: `bootstrap/tests/test_ast_attest.py`
is fully green under the canonical `lhm`/Python 3.13 interpreter (26/26
passed) — resolving both the plan's own Chunk C addition *and* the
separately-tracked Issue #1 baseline drift (the `print_report` half of
it) in the same reviewed act, as designed.

**Loop-fidelity sign-off.** The Decision → implementation chain holds in
full, including through a real correction mid-stream: the accepted Revised
proposal's P1+P2+P4+P5+P6 shipped in `597c882`/`501efe3`/`a8bb2a7`/`c7a144b`,
and the Decision's own citation error (the AST re-anchor mechanism it named,
`bootstrap/REANCHOR_RUNBOOK.md` Phase 4, does not in fact govern
`scaffold_ast_baseline.json` — confirmed independently by both the plan
review and, separately again, by the code review) was caught, corrected on
the record, and routed to the *actual* governing mechanism
(`_ast_attest.py`'s allowlisted `update-symbol` path, extended by a
Maintainer-run script for the one non-allowlisted symbol blocking it)
rather than either silently working around it or blindly following a wrong
citation. Plan review: 4 findings, all accepted (one, PR1, itself
sharpened twice — first identifying the wrong mechanism, then finding even
the "133 blocking symbols" figure was an interpreter-version artifact).
Code review: Accept-with-followups, both informational, independently
re-derived from first principles at the historical commits rather than
trusted from prose. Verification green throughout: `check_cairn` OK at
every commit; `claim_check` clean; `quality_gate --sub neutrality`
returned to its pre-existing baseline (99) after two real, found-and-fixed
excursions (a security-test false positive, a vendor-token leak in a
suppression marker); the full suite is now genuinely green under the
canonical interpreter (1423 passed / 1 pre-existing, unrelated,
separately-tracked failure — the clock-expired `test_evolution_infer`
case) for the first time this session.

Per the [Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home outside
the plan.

This section is append-only once written.
