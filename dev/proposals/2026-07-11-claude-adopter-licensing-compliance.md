<!-- claim-check-allow: templates/core/NOTICE.md, NOTICE.md, bootstrap/tests/test_notice_install.py -->
<!-- The three paths above are forward-reference files this proposal would create; they materialize in the implementing plan. -->
<!-- cairn-internal-ref-allow: doctrine/rationale.md doctrine/proposals.md doctrine/runtime-contract.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Adopter licensing compliance: install a notice file, self-propagate SPDX headers, and make the record carry license + source provenance

**Author**: Claude (Strategy)
**Model**: Claude Opus 4.8
**Date opened**: 2026-07-11
**Status**: proposed
**Touches**: a new installed notice template (`templates/core/NOTICE.md` → adopter `NOTICE.md`, wired into `_CORE_MAPPINGS` in `bootstrap/_scaffold/config.py`); SPDX/copyright headers on the shipped `.py` under `templates/` and `scripts/`; the lockfile writer `bootstrap/_scaffold/install.py` (~1584-1592) + `bootstrap/_scaffold/lockfile.py` (new `source_repository` + `licenses` fields); an adopter-facing "Licensing of the installed files" paragraph in `bootstrap/BOOTSTRAP.md`; an inbound=outbound sentence for `case-studies/README.md`; a `.yml`/`.txt` disposition sentence in `LICENSE-MIT.md`; a new test `bootstrap/tests/test_notice_install.py`. **Explicitly out of scope / Maintainer-only:** any downstream-permission clause in `LICENSE-CC-BY.md` (surfaced as the open question below, not decided here).
**Related**: broad-look skeptical review `dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md` (Theme 4, lines 288-323; Phase A item A4, lines 562-565; Maintainer open question 1, lines 637-639). Follows the shape of the accepted `2026-07-08-claude-review-record-integrity` proposal (fix the live instance + correct the record + guard recurrence). Triage triggers: the proposal template's "Licensing / provenance — the by-file license split or `bootstrap/PROVENANCE.md`" trigger (`dev/proposals/_template.md:69-70`) and the "install contract … byte-level stable" high-risk surface (`AGENTS.md:310-314`).
**Plan review**: required(Internal) — touches the install contract (a new install-set member + a lockfile-schema field addition) and a high-risk licensing surface; Internal floor is a fresh-context read, with an External (cross-type) read recommended before the Decision because the change alters what every adopter's tree redistributes. Ratified at Decision.

## Context

Cairn's license split is real and carefully written: source code is MIT
wherever it lives, prose and document templates are CC BY 4.0, the brand
mark alone is CC BY-ND (`LICENSE-MIT.md:3-13`, `LICENSE-CC-BY.md:5-24`,
`LICENSE-CC-BY-ND.md:15-27`). Both operative licenses carry exactly one
real downstream obligation, and **neither is discharged by anything the
scaffold installs**:

1. **MIT notice is stripped from every shipped tool.** `LICENSE-MIT.md:24-25`
   requires "The above copyright notice and this permission notice shall
   be included in all copies or substantial portions of the Software,"
   and `LICENSE-MIT.md:3-8` explicitly scopes the shipped Python tools
   under `templates/` as that Software. Yet **no shipped `.py` carries a
   copyright or SPDX header** — grepping `templates/` and `scripts/` for
   `SPDX`/`Copyright (c)` returns zero header hits (the only `templates/`
   matches are the words "licenses a steal" in
   `templates/skills/_lib/lifecycle.py:740`, unrelated prose). This
   is all 44 shipped `.py` under `templates/` and all 16 under `scripts/`
   (as_of 2026-07-11).

2. **CC BY attribution is never installed.** `LICENSE-CC-BY.md:45-48`
   requires credit, a license link, and indication of changes; the file
   even ships a ready-made attribution block (`LICENSE-CC-BY.md:54-62`).
   None of it is installed, and **no link back to the source repo exists
   anywhere in the installed tree** — the install manifest
   (`python bootstrap/scaffold.py --manifest`) is 94 rows, 44 of them
   `.md` prose templates (as_of 2026-07-11), none carrying an
   attribution line.

3. **The scaffold caches raw, notice-free CC-BY prose into the adopter's
   *tracked* tree.** For every mergeable `.md`, the installer writes the
   raw pre-substitution template to `dev/.cairn/base/<dst>`
   (`bootstrap/_scaffold/install.py:1559-1562`;
   `_BASE_CACHE_REL = "dev/.cairn/base"` at `lockfile.py:40`), and
   `bootstrap/UPGRADE.md:28-35` documents it as **tracked and hidden**.
   That is verbatim CC-BY redistribution (43 cached `.md`, as_of
   2026-07-11), notice-free, inside the adopter's own version control.

4. **The install receipt records no provenance a license needs.** The
   lockfile writer records schema / version / commit / profile / modules
   / optional_templates / tokens / files
   (`bootstrap/_scaffold/install.py:1584-1592`) — **no creator, no
   license, no source-repo URL.** Both existing provenance fields can
   degrade to `"unknown"` (`_cairn_commit`, `lockfile.py:114-124`), and
   Cairn's own `dev/.cairn/cairn-lock.yml:4` already reads
   `cairn_commit: "unknown"`.

5. **No adopter-facing doc mentions licensing at all.** `bootstrap/BOOTSTRAP.md`,
   `bootstrap/UPGRADE.md`, `docs/quickstart.md`, and `on-ramp/README.md`
   carry no licensing paragraph (their "licens"/"commit" grep hits are
   unrelated). `bootstrap/PROVENANCE.md` covers *which Cairn* an adopter
   installed (`PROVENANCE.md:74-83`) but explicitly "says nothing about"
   content or terms (`PROVENANCE.md:59-63`) — provenance-of-origin, not
   license-obligation.

6. **Two smaller gaps.** There is no inbound-license statement for the
   case studies `case-studies/README.md:88-99` invites, and the shipped
   config/data files (`.yml`/`.txt` — e.g.
   `templates/skills/_data/vendor_targets.yml`, shipped verbatim at
   `config.py:213`; `templates/modules/team-gated/content_scan_*.txt`)
   sit outside both declared license families (code=`.py`, prose=`.md`).

**Consequence.** The day the postdoc's repository goes public alongside
a paper — the normal, desired outcome — it redistributes MIT code with
its required notice stripped and CC-BY prose with no attribution, with no
way for the adopter to know an obligation ever existed. Theme 4 of the
broad-look review verified this "from every angle" and flagged it as a
release blocker (`dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md:288-310`).
This proposal is scoped to **land before 0.4**.

## Proposed paths

Proposed paths:
- `templates/core/NOTICE.md` — the shipped notice template (source); installed to the adopter as `NOTICE.md` via a new `_CORE_MAPPINGS` entry.
- `NOTICE.md` — the adopter-tree destination, and Cairn's own repo-root copy added in the same implementing commit.
- `bootstrap/tests/test_notice_install.py` — behavioral test: the notice installs, is recorded in the lockfile `files[]`, and appears in `--manifest`.

## Proposal

Six elements, one argument (an adopter must be able to redistribute what
Cairn installed without silently breaching Cairn's own licenses, and the
tree must carry enough provenance to prove where it came from).

### P1 — Install one notice file (the live fix)

* Add `templates/core/NOTICE.md`: a short adopter-facing notice carrying
  (a) the MIT copyright + permission notice verbatim from
  `LICENSE-MIT.md:15-33`, (b) the CC BY 4.0 attribution block verbatim
  from `LICENSE-CC-BY.md:54-62` including the license link, (c) the
  CC BY-ND note for the brand mark, and (d) the source-repo URL
  (`https://github.com/MSUHydrogeology/cairn-scientist-ai-teams`, per
  `CITATION.cff:18`). One installed file discharges the attribution +
  notice-retention obligation for the whole installed tree.
* Wire it into `_CORE_MAPPINGS` (`bootstrap/_scaffold/config.py:165`)
  as `("core/NOTICE.md", "NOTICE.md")` so it installs unconditionally
  and is recorded in the lockfile `files[]` and the published
  `--manifest` (`install.py:1320-1347`) — making its presence auditable
  and upgrade-carried like any other core file.
* **Home / name are a sub-decision** (below): repo-root `NOTICE.md` is
  the recommended default (discoverable, conventional). Cairn's own repo
  root gains a `NOTICE.md` in the same commit so the self-host tree is
  consistent.

### P2 — Self-propagating SPDX headers on shipped `.py`

* Add a two-line SPDX/copyright header to the top of each shipped
  `.py` under `templates/` and `scripts/`, e.g.
  `# SPDX-License-Identifier: MIT` /
  `# Copyright (c) 2026 Anthony Kendall and the Cairn contributors`.
  Because the tools install **verbatim** (hash-policy scripts, e.g.
  `config.py:210-216`, `_ALWAYS_ON_MAPPINGS` at `config.py:313`), the
  header travels into the adopter's tree automatically and stays with
  any copy they make — the notice self-propagates.
* This is near-mechanical and touches many files but changes no
  behavior; it is the lowest-risk element. The AST attestation baseline
  (`bootstrap/tests/test_ast_attest.py`) pins engine *structure*, not
  leading comments, so headers on `bootstrap/_scaffold/*.py` (if the
  Maintainer wants them there too) need a re-anchor per
  `bootstrap/REANCHOR_RUNBOOK.md`; the plan scopes whether engine files
  are in or out.

### P3 — License + source provenance in the lockfile

* Add two additive top-level fields to the lockfile written at
  `install.py:1584-1592`: `source_repository` (the Cairn repo URL) and
  `licenses` (e.g. `["MIT", "CC-BY-4.0", "CC-BY-ND-4.0"]`), sourced from
  `CITATION.cff` alongside the existing `_cairn_version` read
  (`lockfile.py:103-111`). This makes the receipt answer "under what
  license, and from where" — the two questions Theme 4 named as missing
  (`dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md:300-302`).
* **This is the one install-contract change** (`AGENTS.md:310-312`
  treats the lockfile schema as byte-level stable). The fields are
  purely additive; the plan decides whether that warrants a
  `_LOCK_SCHEMA` bump (`lockfile.py:42`, currently `1`) or reads as a
  back-compatible minor addition, and re-anchors any manifest/fidelity
  test that asserts an exact field set. **If review judges this a
  different enough risk class, P3 splits cleanly into its own
  proposal** — P1/P2/P4-P6 stand without it.

### P4 — Adopter-facing licensing paragraph

* Add a "Licensing of the installed files" paragraph to
  `bootstrap/BOOTSTRAP.md` (near the II-2 Scaffold description of what
  the script writes, `BOOTSTRAP.md:288-304`): what an adopter owes
  (keep `NOTICE.md`; keep the SPDX headers on any tool they
  redistribute), what they do **not** owe, and a pointer to the notice
  file. One paragraph, adopter-language, no legalese.

### P5 — Inbound = outbound

* Add one sentence to `case-studies/README.md` (near the contribution
  invite, `case-studies/README.md:88-99`): a case study contributed to
  Cairn is offered under the same CC BY 4.0 / MIT split as the rest of
  the repository. This is the inbound-license statement the invite
  currently lacks. (If the Maintainer prefers a repo-wide inbound
  statement, a one-line note in `NOTICE.md` or a future `CONTRIBUTING.md`
  is the alternative home — flagged, not decided.)

### P6 — Disposition for the `.yml`/`.txt` family gap

* Add one clarifying sentence to `LICENSE-MIT.md` (the scope note,
  `LICENSE-MIT.md:3-13`): functional configuration and data files that
  are operational parts of the tools (`.yml`/`.txt`, e.g.
  `vendor_targets.yml`, `content_scan_*.txt`) travel with the **code**
  family (MIT), not the prose family — they are not creative prose.
  (Prose `.md` such as the verbatim-shipped `dev/reflections/README.md`
  remains CC BY, already covered.) This closes the "outside both
  families" gap the review's follow-up sweep noted
  (`dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md:321-323`)
  without inventing a fourth license.

### Documentation / doctrine surface

* **No `doctrine/` file changes.** This proposal touches legal
  instruments (`LICENSE-*.md`, a new `NOTICE.md`), install machinery
  (`config.py`, `install.py`, `lockfile.py`), a descriptive adopter
  procedure (`bootstrap/BOOTSTRAP.md`), and a descriptive doc
  (`case-studies/README.md`). Per the doc-tier home rule
  (`docs/DOCUMENTATION_PLAN.md`), P4 and P5/P6 are **descriptive /
  procedural** adopter surfaces, not governing doctrine; none route to
  `AGENTS.md` or `doctrine/`.
* **Install-contract surface (declared).** P1 and P3 touch the install
  set / lockfile schema — the byte-level-stable contract
  (`AGENTS.md:310-312`). That is why this is a proposal, not a direct
  commit; the plan pins the schema decision and the re-anchors.
* **No vendor-neutrality impact.** The notice/headers name a license and
  a repo URL, not an AI vendor; the `quality_gate.py --sub neutrality`
  surface is untouched.

### Doctrine-change rate-limit (if this proposal changes doctrine)

**N/A — this proposal changes no `doctrine/` rule, process, or
contract.** The doctrine-evolution rate-limit gate
(`doctrine/rationale.md:323-347`) governs changes to doctrine under
`doctrine/`; none are made here, so the gate does not apply and I make
no high-risk / recurrence claim under it. Two honesty notes:

* The **install contract** (P3) is a protected contract but not a
  `doctrine/` rule — it is guarded by the "install contract … byte-level
  stable" triage trigger (`AGENTS.md:310-312`) and by review, which is
  exactly the gate being cleared by opening this proposal.
* The **LICENSE-CC-BY.md downstream-permission clause** is a change to a
  legal instrument, not to doctrine. It is **not decided in this
  proposal** and is deliberately reserved to the Maintainer (open
  question below); a legal-terms change is the Maintainer's call
  regardless of the doctrine gate.

## Rationale

* **Which user workflow does it improve?** The adopter's publish-a-paper
  moment: the first external adopter can make their repo public without
  silently breaching Cairn's licenses, because the obligation is
  discharged by a single installed file plus self-propagating headers,
  and the tree records where it all came from.
* **What contract does it preserve/clarify?** The by-file license split
  (`AGENTS.md:313-315`) — currently correct on paper but undischarged in
  every install. It also *extends* the install contract cleanly (a new
  recorded file, additive lockfile fields) rather than working around
  it.
* **Transparency / reproducibility improved?** A published tree can be
  traced to its Cairn source and license from the tree itself (P3),
  complementing `PROVENANCE.md`'s origin story with the license story it
  explicitly disclaims (`PROVENANCE.md:59-63`).
* **Why now?** The postdoc install is imminent and 0.4 is the earliest
  public release; the broad-look review classes this as the clearest
  pre-0.4 blocker (`dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md:290-291`).
  A stripped-notice tree published with a paper is far costlier to
  unwind after the fact than before the first install.
* **Stack-neutrality preserved.** All mechanism (write one more file,
  read two `CITATION.cff` fields) is stdlib-only, honoring the
  stdlib-only engine contract (`doctrine/runtime-contract.md:177-187`;
  `bootstrap/DEPENDENCY_BUDGET.md`) — no new dependency.

## Alternatives considered

1. **Do nothing.** Rejected — Theme 4 is a verified release blocker; the
   default install breaches Cairn's own licenses in every adopter tree.
2. **Notice file only (P1), skip headers/lockfile/docs.** Partial — one
   `NOTICE.md` discharges the *attribution* obligation, but a tool file
   copied *out* of the tree loses its MIT notice without the
   self-propagating header (P2), and the receipt still can't answer
   "under what license" (P3). The review named all four as one package
   (`…:562-565`).
3. **Headers only (P2), no notice file.** Rejected — SPDX headers cover
   code but nothing carries the CC-BY attribution for the prose tree,
   which is the larger surface (44 `.md` templates + 43 cached raw
   copies, as_of 2026-07-11).
4. **Put the notice under `dev/.cairn/` with the install machinery.**
   Rejected as default — a notice must be *discoverable*; a hidden path
   defeats its purpose. Repo-root `NOTICE.md` is recommended, but the
   home is offered as a sub-decision.
5. **Stop caching raw CC-BY prose into `dev/.cairn/base/` (element 3 of
   Context).** Rejected — the base cache is load-bearing for the
   distribution-mode-independent 3-way upgrade merge
   (`bootstrap/UPGRADE.md:28-35`); removing it breaks `upgrade`. The
   right fix is *attribution that covers it* (P1), not deleting the
   cache.
6. **Add the downstream-permission clause to `LICENSE-CC-BY.md` now.**
   Deferred to the Maintainer — it changes a legal instrument and is the
   open question below, not this proposal's to decide.
7. **Split P3 (lockfile fields) into its own proposal.** On the table —
   P3 is the only install-contract-*schema* change and a different risk
   class from the docs/notice work; the proposal is structured so P3
   detaches cleanly if review prefers (see P3). The default is to keep
   the coherent package together, matching the review's A4 framing.

**Recommended:** P1 + P2 + P4 + P5 + P6 as the coherent licensing
package, with P3 included but explicitly splittable, and the
LICENSE-CC-BY.md clause left to the Maintainer.

## Evidence / verification plan

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.** (i) Every install writes exactly one `NOTICE.md`
  recorded in the lockfile `files[]` and the `--manifest` — *enforced by*
  `bootstrap/tests/test_notice_install.py` and the existing
  `bootstrap/tests/test_manifest.py` no-duplicate-destination check
  (`install.py:1348-1354`). (ii) Every shipped `.py` carries an SPDX
  header — *enforced by* an assertion in the new test (or an extension
  of an existing shipped-tool test) that greps the install set for the
  header. (iii) The lockfile still round-trips as JSON/YAML with the two
  new fields — *enforced by* `bootstrap/tests/test_lockfile_module.py`.
* **Failure modes.** `source_repository` / `licenses` degrade **open**
  to a sentinel if `CITATION.cff` is unreadable, exactly as
  `cairn_version`/`cairn_commit` already degrade to `"unknown"`
  (`lockfile.py:103-124`) — a missing field never blocks an install.
  A duplicate `NOTICE.md` destination fails **closed** at
  `install.py:1348-1354` (existing guard). SPDX headers on verbatim
  tools change file hashes, so the lockfile `hash`/`base_hash` and any
  fidelity baseline must be re-recorded — a **closed** failure (the
  divergence check at `install.py:1547-1548` reds until re-recorded),
  caught before ship, not after.
* **Edge-case inventory.** Adopter who deletes `NOTICE.md` (upgrade
  re-offers it like any core file; `verify_integrity` flags the missing
  record); non-git / packaged-release source (`source_repository` still
  written from `CITATION.cff`, `cairn_commit` may be `"unknown"` —
  unchanged behavior); a `--force` re-run (overwrites `NOTICE.md` like
  other core files, `BOOTSTRAP.md:310-326`).
* **Public-path → test mapping.** New `NOTICE.md` install path →
  `bootstrap/tests/test_notice_install.py`; lockfile new fields →
  `bootstrap/tests/test_lockfile_module.py`; manifest membership →
  `bootstrap/tests/test_manifest.py`. (Written as real relative markdown
  links in the plan once the test file exists — shown here as bare paths
  to keep this proposal link-clean, per the accepted
  `review-record-integrity` proposal's precedent.)
* **Known omissions.** This proposal does not add a runtime *gate* that
  fails an adopter build on a missing notice (advisory-only posture, and
  a gate is a separable follow-up); it does not retro-attribute trees
  already installed by earlier Cairn versions (their next `upgrade`
  brings the notice in); and it does not change the CC-BY *terms*
  themselves (the open question).

### Tests required

* `bootstrap/tests/test_notice_install.py` (new) — the notice installs,
  is recorded in the lockfile `files[]`, and appears in `--manifest`;
  plus the shipped-`.py`-carry-SPDX-header assertion (P2).
* `bootstrap/tests/test_lockfile_module.py` (extend) — the two new
  provenance fields serialize and round-trip.
* `bootstrap/tests/test_manifest.py` (existing) — stays green with the
  new core-mapping row (row count moves from 94 by one, as_of
  2026-07-11).
* The full `python -m pytest bootstrap/tests` suite stays green (modulo
  the pre-existing separately-tracked failures this proposal does not
  touch).

### Examples / smoke checks

* `python bootstrap/scaffold.py --manifest` shows the `NOTICE.md` row;
  `--dry-run` / `--summary` exercise the install path with the new
  mapping and no side effects.
* A scratch install into an empty target, then inspect the target's
  `NOTICE.md`, its `dev/.cairn/cairn-lock.yml` (the two new fields
  present), and a shipped tool's SPDX header — the end-to-end
  "would-the-postdoc-be-covered" check.
* `python scripts/check_cairn.py` clean over the edited `BOOTSTRAP.md`,
  `case-studies/README.md`, `LICENSE-MIT.md`, and the new `NOTICE.md`.
* `python scripts/claim_check.py` clean over this proposal and the plan.
* If engine `.py` gain headers, re-anchor `test_ast_attest.py` per
  `bootstrap/REANCHOR_RUNBOOK.md` and confirm green.

## Open question — the one genuine Maintainer co-decision

Should `LICENSE-CC-BY.md` gain an explicit **downstream-permission
clause** — e.g. *"files installed into your repository by the bootstrap
may be maintained and relicensed under your repository's own terms,
provided the installed `NOTICE.md` is retained"*? This is the review's
open question 1 (`dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md:637-639`).

* **In favor:** it collapses an adopter's entire obligation to "keep one
  file," which converts a legal-compliance question a scientist cannot
  easily answer into a one-file rule — and research code is routinely
  GPL-2.0 or a custom license, so the interaction between Cairn's
  CC-BY/MIT material and the adopter's own repo license is otherwise
  unresolved (Context has no stated position on this today).
* **Against:** it weakens CC BY 4.0's standard reciprocal-attribution
  expectations for the installed prose and creates a Cairn-specific
  license variant that a downstream reader must reason about separately;
  plain attribution mechanics (P1) may be sufficient without amending
  the license text.

**This is the Maintainer's call and is not decided here.** P1's
`NOTICE.md` is drafted to work under *either* answer (it is the file the
clause would reference); only the LICENSE-CC-BY.md wording depends on the
decision. A secondary sub-decision for the Maintainer: the notice file's
name/home (recommended: repo-root `NOTICE.md`).

## Signals the change is wrong

* SPDX headers on verbatim tools cause churn in the lockfile /
  fidelity baselines on every unrelated upgrade → the header placement
  or the hash policy interacts badly; reconsider whether engine files
  carry headers, or record the baselines once and confirm they settle.
* Adopters read the BOOTSTRAP paragraph or `NOTICE.md` as a *new
  restriction* rather than a reassurance ("what you owe" reads as
  heavier than reality) → reword toward "keep one file, that's it,"
  and (if chosen) lean on the downstream-permission clause.
* The two new lockfile fields break a downstream consumer that pinned
  the exact field set → the additive-vs-schema-bump decision was wrong;
  bump `_LOCK_SCHEMA` and add a migration, or split P3 out entirely.
* The `.yml`/`.txt`-are-MIT sentence (P6) turns out to misclassify a
  genuinely-prose data file → narrow the sentence to name only the
  functional-config files, leaving prose data under CC BY.
* Review judges the package incoherent across risk classes → split P3
  (and, if needed, P2) into separate proposals, keeping P1/P4/P5/P6 as
  the minimal pre-0.4 fix.