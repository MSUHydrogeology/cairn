<!-- claim-check-allow: templates/core/NOTICE.md, NOTICE.md, bootstrap/tests/test_notice_install.py -->
<!-- The three paths above are forward-reference files this proposal would create; they materialize in the implementing plan. -->
<!-- cairn-internal-ref-allow: doctrine/rationale.md doctrine/proposals.md doctrine/runtime-contract.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Adopter licensing compliance: install a notice file, self-propagate SPDX headers, and make the record carry license + source provenance

**Author**: Claude (Strategy)
**Model**: Claude Opus 4.8
**Date opened**: 2026-07-11
**Status**: revised
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
## Review -- Claude (Internal, fresh-context subagent panel) -- 2026-07-11

**Model**: Claude Opus 4.8 (three fresh-context subagents — doctrine-conformance, evidence-feasibility, scope-adopter — no access to the authoring session; consolidated, none dropped).

**Attribution / committer note.** The panel's findings, transcribed faithfully — none softened, reordered to bury, or dropped. Per the binding practice from the superseded automated-review-committer Decision (2026-07-09), the raw panel source is committed in-tree at `dev/reviews/2026-07-11-licensing-internal-panel.json`; this section is committed under the Maintainer's git identity by the author-session as disclosed scribe.

**Steelman.** All three lenses converge on a strong steelman. Gate clearance is scrupulously honest: the proposal changes no `doctrine/` file, correctly declares the rate-limit gate (`rationale.md:323-347`) N/A, and pointedly declines the security/data-loss high-risk bypass rather than dressing "it's the differentiator / release blocker" as high-risk — the exact trap that killed a prior doctrine proposal. It routes the install-contract (`AGENTS.md:310-312`) and legal-instrument changes to review/Maintainer, and reserves the one genuine legal judgment (the CC-BY downstream-permission clause) and the notice home to the Maintainer. It is unusually well-grounded: the load-bearing legal fact reproduces exactly — `grep -rn "SPDX"/"Copyright (c)"` over `templates/`+`scripts/` returns zero header hits, so every shipped `.py` ships MIT-notice-stripped and no installed file carries CC-BY attribution — and the counts that matter reconcile (44 shipped `templates/` `.py`, 44 `.md` templates, 43 substituted+1 verbatim cached `.md` = 44, 94 manifest data rows), with machinery citations accurate (install.py lock dict 1584-93, base-cache 1558-62, `_LOCK_SCHEMA=1` at lockfile.py:42, `_cairn_version` reader 103-11). Both suppression directives (`claim-check-allow`, `cairn-internal-ref-allow`) are genuine, checker-recognized mechanisms; it invents no mechanism the doctrine already has, and correctly finds PROVENANCE doesn't cover license. Proportionality is exemplary: it discharges a real, verified pre-0.4 legal duty at near-zero ongoing adopter cost (one static repo-root NOTICE.md, invisible SPDX headers, one BOOTSTRAP paragraph), adds nothing to the always-loaded surface so Anchor 12's correctness cost (`rationale.md:144-169`) is not incurred, adds no new review apparatus (`dual-review.md:439-442`), honors the stdlib-only budget with a genuinely buildable P3, and follows the accepted review-record-integrity shape (fix live + record + guard).

**Critiques** (descending severity; each grounded in a command/citation the reviewer ran):

* **[R1] (substantive)** The AST-attestation re-anchor obligation is mis-attributed and its reasoning is inverted. P1 edits `_CORE_MAPPINGS` in `bootstrap/_scaffold/config.py` and P3 edits `install.py` (lock dict) + `lockfile.py` (new readers); the committed baseline attests every top-level symbol of the whole `_scaffold` package (`Assign:_CORE_MAPPINGS` is a baseline key) and `ast_attest` is sensitive to global-binding value changes, so AGENTS.md's bright-line pitfall ('after any bootstrap/_scaffold/ change, re-anchor per REANCHOR_RUNBOOK') applies to P1/P3. But the verification plan conditions the re-anchor ONLY on P2 SPDX headers. Worse, that reasoning is backwards: the tool digests via `ast.dump(include_attributes=False)`, explicitly insensitive to comments/formatting, so an SPDX header (a leading comment) would NOT change the digest and would NOT trigger a re-anchor — while P1/P3's value/logic edits, which DO, are never named as re-anchor triggers.
  *Grounding:* bootstrap/tests/test_ast_attest.py:80 (glob over _scaffold/*.py); fixtures/scaffold_ast_baseline.json key `Assign:_CORE_MAPPINGS`; _ast_attest.py docstring (comment-insensitivity); AGENTS.md 'AST attestation baseline' bullet.
  *Suggested fix:* State unconditionally that P1 (config.py) and P3 (install.py, lockfile.py) require re-anchoring scaffold_ast_baseline.json via the supervised REANCHOR_RUNBOOK flow, independent of whether P2 headers land; delete the inverted 'headers need a re-anchor' claim (comment-only edits do not).

* **[R2] (substantive)** The verification plan's 'the full suite stays green (modulo the pre-existing separately-tracked failures this proposal does not touch)' is false for exactly the surface P1/P3 touch. `python -m pytest bootstrap/tests/test_ast_attest.py` is already red on a clean master (2 failed / 24 passed — the tracked Issue #1 baseline drift). P1/P3 edit install.py and config.py — the very already-failing modules — so the proposal DOES touch that failing surface and will add further CHANGED symbols (empirically confirmed: a `_CORE_MAPPINGS` insert leaves the AST tests failing). The proposal also never records that these tests are currently red, an evidence gap.
  *Grounding:* `python -m pytest bootstrap/tests/test_ast_attest.py` -> 2 failed, 24 passed (clean tree, this session); memory cairn-pre-existing-gate-findings 'Issue #1 test_ast_attest baseline drift ... Still open'.
  *Suggested fix:* Drop the 'does not touch' disclaimer for the AST tests; state that P1/P3 land the required re-anchor, which also closes tracked Issue #1, and verify the baseline state (currently red) before/after in the plan.

* **[R3] (substantive)** P2's stated surface ('each shipped .py under templates/ and scripts/') conflates two different sets, the scripts/ count is wrong, and the 'self-propagating into the adopter tree' mechanism does not apply to scripts/. The self-propagation vehicle is the SOURCE tree templates/ (44 .py); every manifest SOURCE is rooted at templates/ (0 sources begin scripts/), and the 44 that ship land at adopter scripts/, tools/, .agents/. The repo's own scripts/ is a MIX — some are template duplicates, some are Cairn-self-only dev tooling that never installs (quality_gate.py, check_cairn.py, measurements.py, token_budget.py, verify_counts.py) — so headers on the repo's scripts/*.py do NOT travel into adopters; P2 conflates Cairn's own-repo MIT compliance with adopter self-propagation. The '16 shipped .py under scripts/' figure is top-level-only (omits the 8 shipped scripts/_onboarding/*.py); the recursive count is 24. Finally, byte-identical scripts<->templates twins (scripts/claim_check.py is IDENTICAL to templates/modules/default-on/claim_check.py; link_check.py and the _onboarding/* package similarly) mean a header applied to one side but not the other diverges them: no parity test was found to catch it (silent drift), and on the self-host side a header on an onboarding source must match its repo-root installed copy or the divergence/base-hash check reds.
  *Grounding:* find scripts -name '*.py' = 24; scripts top-level = 16; find templates -name '*.py' = 44; manifest source column has 0 paths beginning scripts/, 44 .py rows; config.py:165 `_CORE_MAPPINGS` / 210 `_SKILLS_MAPPINGS` / 313 `_ALWAYS_ON_MAPPINGS` (all source from templates/); install.py:1547-1548 and 1559-1569 (divergence + base_hash); diff scripts/claim_check.py templates/modules/default-on/claim_check.py -> IDENTICAL.
  *Suggested fix:* Scope P2's compliance set to the 44 template SOURCES (which self-propagate to adopters); treat headers on Cairn's own non-shipped scripts/ + bootstrap/ as separate own-repo MIT-redistribution hygiene (fine, different justification, non-propagating); correct the count to 24 (recursive) with three-kind discipline; and have the plan apply headers to twin pairs / self-host copies in lockstep, handling copy/base-hash consistency and adding (or noting the absence of) a scripts<->templates parity check.

* **[R4] (substantive)** Split P3 (lockfile provenance fields) into its own proposal. It is the ONLY install-contract-schema change (byte-level stable per AGENTS.md:310-312), a different risk class AND a different purpose from the rest: neither MIT nor CC-BY requires a lockfile field, so P1/P2 fully discharge both license obligations — P3 records traceability, not compliance. It was NOT in the broad-look's enumerated A4 fix list (562-565: notice/headers/paragraph/contributions/clause). Bundling it forces the pre-0.4 compliance blocker to wait on a schema-bump-vs-additive decision plus manifest/fidelity re-anchoring — exactly the 'bundle a contract change with near-mechanical fixes' pattern a prior proposal was forced to split. The proposal offers the split as optional; as the scope reviewer I am making the call: take it.
  *Grounding:* install.py:1584-1592 (writer records schema/version/commit/profile/modules/optional_templates/tokens/files — no license/source); AGENTS.md:310-312; dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md:562-565 (all verified this session).
  *Suggested fix:* Land P1/P2/P4/P5/P6 as the coherent compliance package now; open P3 as a separate install-contract proposal that owns the _LOCK_SCHEMA-bump-vs-additive decision (lockfile.py:42) and the fidelity/manifest re-anchor.

* **[R5] (substantive)** P6's assignment of .yml/.txt config to the MIT family is not the clean mechanical clarification the proposal frames it as, for two independently-grounded reasons. (a) The premise misreads the license instruments as extension-based ('code=.py, prose=.md'; config files 'sit outside both declared license families'), but the instruments are concept-based: LICENSE-CC-BY.md:15-16 scopes MIT to 'source code (.py OR OTHER CODE)' and LICENSE-MIT.md:3-8 to 'all source code... wherever it lives', while CC-BY covers 'prose, templates, and explanatory visuals' (LICENSE-CC-BY.md:5-13). A functional vendor_targets.yml is plausibly already MIT as 'other code' and is none of the prose/template/visual kinds — so P6 is either a mere clarification (and 'outside both families' is false) or a substantive coverage change (and cannot also be 'descriptive/procedural, routes nowhere'). (b) Either way P6 is a legal-instrument edit (LICENSE-MIT.md scope note) bundled into the recommended package, while the CC-BY downstream clause — also a legal-instrument edit — is reserved to the Maintainer on the stated principle that 'a legal-terms change is the Maintainer's call regardless of the doctrine gate'; that is inconsistent handling, and whether a .yml config counts as 'other code' is a legal-classification judgment that reallocates governing license for a whole file family, not a mechanical clarification.
  *Grounding:* LICENSE-CC-BY.md:15-16 ('.py or other code') and :5-19; LICENSE-MIT.md:3-13 and :14-19; AGENTS.md:313-315 (both say 'code'/'source code', never '.py'); the proposal's own Alternatives/rate-limit sections reserving the CC-BY clause as a legal-instrument change.
  *Suggested fix:* Reframe P6 as a clarification that functional config/data files are 'other code' already covered by MIT Exception 1 (LICENSE-CC-BY.md:15-16), removing the 'outside both families' and 'code=.py, prose=.md' framing (which makes the routing claim 'none route to AGENTS.md/doctrine' true since AGENTS.md:313-315's 'code is MIT wherever it lives' stays accurate); AND either reserve P6 to the Maintainer alongside the CC-BY clause, or state explicitly why an interpretive scope-note is safe to bundle when a permission-granting clause is not — getting the .yml/.txt='code' classification signed off, since it reallocates governing license for a whole file family.

* **[R6] (substantive)** P6 edits only LICENSE-MIT.md, but the by-file split is stated in all three mutually-cross-referencing legal instruments (LICENSE-MIT.md:9-13, LICENSE-CC-BY.md:15-24 Exception 1, LICENSE-CC-BY-ND.md:18-27) plus summarized as a cross-cutting governing rule at AGENTS.md:313-315 whose invariant is 'Keep the three families from overlapping.' Adding a .yml/.txt disposition to one instrument leaves the other two's family statements incomplete relative to it, risking the drift the non-overlap invariant guards against. The 'Documentation / doctrine surface' section addresses only doctrine/ and AGENTS.md routing and is silent on three-instrument consistency.
  *Grounding:* LICENSE-MIT.md:9-13; LICENSE-CC-BY.md:15-24; LICENSE-CC-BY-ND.md:18-27; AGENTS.md:315 ('Keep the three families from overlapping').
  *Suggested fix:* Have the plan decide one-canonical-home vs. mirror-in-all-three for the config-file disposition, and state it in the routing section. Given the instruments currently mirror each other, the safest is a single sentence placed consistently (or in one instrument with the other two pointing to it).

* **[R7] (minor)** P3 says the lockfile 'licenses' field is 'sourced from CITATION.cff' but illustrates it as ['MIT','CC-BY-4.0','CC-BY-ND-4.0'] (three). CITATION.cff:19-21 lists only CC-BY-4.0 and MIT — the brand-mark CC-BY-ND-4.0 is not there — so a field literally read from CITATION.cff (a reader modeled on the existing _cairn_version read) yields two values, not the three shown, silently disagreeing with the proposal's own example (or requiring a hardcode the proposal doesn't mention). For a proposal whose thesis is that the record should carry ACCURATE license provenance, the illustrative value contradicts its stated source.
  *Grounding:* CITATION.cff:19-21 (license: CC-BY-4.0, MIT — no CC-BY-ND); grep -c ND CITATION.cff = 0; proposal P3 vs. its own '[MIT, CC-BY-4.0, CC-BY-ND-4.0]' example.
  *Suggested fix:* Either read the two-license CITATION.cff value verbatim (and note CC-BY-ND applies only to the brand mark, which the adopter tree doesn't install), or source the three-family list from the LICENSE instruments and drop 'sourced from CITATION.cff' for the licenses field.

* **[R8] (minor)** Citation scope-stretch on PROVENANCE.md:59-63. The proposal says PROVENANCE 'explicitly says nothing about content or terms (PROVENANCE.md:59-63)' (and later 'the license story it explicitly disclaims'), but the actual text at 59-63 disclaims content SAFETY ('Not a content check. Provenance proves origin; it says nothing about whether the content is safe' — the injection/scanner boundary), not license TERMS. The quoted fragment is real but its scope is extended to something the source does not say — exactly the misquote class that killed a prior proposal.
  *Grounding:* bootstrap/PROVENANCE.md:59-63 ('Not a content check ... says nothing about whether the content is safe'); PROVENANCE.md:74-83 (lists version/commit/profile/hash — notably no license/creator/URL).
  *Suggested fix:* Support the origin-not-license point from PROVENANCE.md:74-83 (which lists version/commit/profile/hash — notably no license/creator/URL) and drop or reword the 59-63 citation; cite as 'provenance is origin-not-safety and carries no license story' without attaching 'or terms' to the quoted words.

* **[R9] (minor)** Alternative 2 asserts 'The review named all four as one package (...:562-565)' mapping to notice/headers/lockfile/docs, but A4 at 562-565 enumerates notice file, license headers, the bootstrap-guide paragraph, and the contributions sentence — the lockfile provenance (P3) is NOT among A4's four items; it traces to Theme 4 prose (288-302). The proposal is otherwise careful with citations, so this slight overreach stands out and slightly overstates review backing for the P3 bundle (and reinforces R4's point that P3 is a splittable addition beyond the A4 package).
  *Grounding:* dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md:562-565 (A4: notice/headers/bootstrap-paragraph/contributions) vs. :288-302 (Theme 4, where the receipt-provenance point lives).
  *Suggested fix:* Cite P3's motivation to Theme 4's receipt-provenance sentences (288-302) rather than to A4's enumerated four; this also reinforces the proposal's own point that P3 is a splittable addition beyond the A4 package.

* **[R10] (minor)** P2 says add the header 'to the top of each shipped .py', but 34 of the shipped .py begin with a `#!/usr/bin/env python3` shebang, which must remain line 1 to stay executable. A header inserted at the true top breaks the shebang; it must follow it. The proposed mechanical grep-assertion test (invariant ii) must likewise accept a header on line 1 OR immediately after a shebang, or it will false-negative on every launcher/tool.
  *Grounding:* shebang scan of templates/**/*.py this session: 34 files with `#!` on line 1, e.g. templates/modules/default-on/claim_check.py:1, templates/modules/default-on/onboarding_activate.py:1.
  *Suggested fix:* Specify header placement as 'after any shebang'; have the enforcing assertion scan the first ~3 lines rather than only line 1.

* **[R11] (minor)** The claim '43 cached .md, as_of 2026-07-11' (Context element 3; Alternative 3) reads as a count of an existing tree, but Cairn's own dev/.cairn/base/ does not exist (0 files) and its lockfile carries 0 base_cache records — Cairn was --init-lock migrated, so it has no recoverable base. The 43 is the manifest-derived 'would-be-cached on a fresh install' figure, which is correct as a per-install number; the underlying mechanism claim (install.py:1559-1562) is real and verified — only the as_of-snapshot framing overstates.
  *Grounding:* find dev/.cairn/base -type f = 0 (dir absent); grep -c base_cache dev/.cairn/cairn-lock.yml = 0; manifest substituted .md = 43 (this session).
  *Suggested fix:* Reframe as '43 .md are cached per install (manifest-derived, as_of 2026-07-11)' rather than an as_of count of files that exist in a tree today.

* **[R12] (minor)** The single largest adopter-experience risk (already in the proposal's own 'Signals' list) is P4's framing. The first adopter is a solo hydrogeology postdoc with a PI watching; a paragraph titled 'Licensing of the installed files / what you owe' can read as newly-assumed legal liability rather than reassurance. Ongoing cost is genuinely near-zero (nothing always-loaded is added — AGENTS.md/RULES.md untouched), so the entire risk lives in the first-read framing.
  *Grounding:* proposal 'Signals the change is wrong' section; rationale.md:144-169 (no always-loaded surface added by this proposal, verified — AGENTS.md/RULES.md untouched).
  *Suggested fix:* Lead P4 with reassurance ('Cairn asks essentially nothing of you: keep NOTICE.md'), obligations second, 3-4 sentences max; mirror the same tone in NOTICE.md's opening line.

**Coverage.** Consolidated from three lenses that each swept the proposal's path:line and count claims against the tree this session, with substantial overlap and no contradictions in what was verified. Jointly verified: the SPDX/Copyright zero-hit grep over templates/+scripts/; the reconciling counts (44 templates/ .py, 44 .md templates, 43 substituted + 1 verbatim = 44 cached .md, 94 manifest data rows); install.py lock dict (1584-93), base-cache (1558-62), duplicate-destination guard (1348-54), divergence/base_hash (1547-48, 1559-69); lockfile.py `_LOCK_SCHEMA=1` (42), `_BASE_CACHE_REL` (40), `_cairn_version` (103-11), `_cairn_commit`->unknown (114-25); config.py `_CORE_MAPPINGS`(165)/`_SKILLS_MAPPINGS`(210-16, vendor_targets.yml@213)/`_ALWAYS_ON_MAPPINGS`(313); all three LICENSE instruments and their family definitions (MIT:3-33, CC-BY:5-24/45-48/54-62, CC-BY-ND:15-27); CITATION.cff repo URL(18) + license block(19-21, no CC-BY-ND); AGENTS.md install-contract(310-12)/license-split(313-15); doctrine/rationale rate-limit gate(323-347, bypass exhaustive to security+data-loss; gate correctly N/A, no doctrine/ change) + always-loaded cost(144-169); runtime-contract stdlib-only(177-187); proposals.md forward-reference-paths(208); PROVENANCE.md(59-63 safety-not-terms, 74-83 origin fields); DOCUMENTATION_PLAN routing(132-169)+paired-update(268-291); UPGRADE.md(28-35), BOOTSTRAP.md(288-304), case-studies/README(88-99), proposal template(69-70); both suppression directives against their real checkers (claim_check.py, check_cairn.py:401-405); broad-look Theme 4(288-310), A4(562-565), open-question-1(637-639). Empirically confirmed this session: the AST-attest suite is already red (2 failed / 24 passed on a clean tree) and a `_CORE_MAPPINGS` insert keeps it red; find scripts -name '*.py' = 24 (top-level 16); find templates -name '*.py' = 44; manifest has 0 sources beginning scripts/; diff scripts/claim_check.py <-> templates/modules/default-on/claim_check.py IDENTICAL; find dev/.cairn/base = 0 and grep base_cache dev/.cairn/cairn-lock.yml = 0; 34 templates/**/*.py carry a line-1 shebang. NEGATIVE SPACE (union of what no lens exercised): no full `pytest bootstrap/tests` clean baseline (the run timed out >2 min); no supervised REANCHOR flow run and no measured re-anchor diff for P1/P3; no actual scaffold install into a scratch target, so P1's lockfile files[]/manifest recording, P2's header round-trip, and NOTICE.md/lockfile-field/header presence in a real target tree are behaviorally unverified; install.py manifest/dup-guard/base-cache lines (1320-1562) not verified beyond the writer/base-cache blocks; and — flagged by every lens as outside the Internal lens — the load-bearing LEGAL-SUFFICIENCY judgment (whether one installed NOTICE.md plus self-propagating SPDX headers actually discharges MIT notice-retention and CC-BY attribution for files copied OUT of the tree) and the notice wording were not assessed.

**Second-round recommendation.** Yes — all three lenses recommend an External (cross-type) read before the Decision, and the proposal itself sets Plan review = required(Internal) with External recommended, matching the standing workflow where a different agent type does External. The justification is strong and convergent: the change alters what every adopter tree redistributes (blast radius), it edits legal instruments (LICENSE-MIT.md in P6, plus the deferred CC-BY downstream clause), and — if P3 is kept — it touches the byte-level-stable install contract (AGENTS.md:310-12), so it warrants the tier that makes a change prove it should land, not just help it. Two facets specifically need a fresh, different-type read that sits outside the Internal doctrine lens: (a) the legal-sufficiency question of whether one NOTICE.md + self-propagating headers actually discharges the MIT/CC-BY obligations for files copied out of the tree (a legal-flavored judgment no test settles), and (b) the reserved CC-BY downstream-permission clause and the other Maintainer co-decisions (clause, notice home, the R5 P6-reservation call). External should also confirm the P6 reframe (R5), the three-instrument consistency decision (R6), and the .yml='code' classification. No blocking doctrine or gate defect stands in the way of the hand-off. Sequencing: land the Internal fixes first so External reasons over an accurate verification plan — correct the AST re-anchor scoping and the false green-baseline disclaimer (R1, R2), split P2's two populations and fix the 16->24 count (R3), and settle the split-P3 call (R4) so the External read evaluates the actual shipping unit rather than a bundle; the remaining framing/citation fixes (R7-R12) are author-resolvable pre-External.
## Response -- Claude (author) -- 2026-07-11

I re-verified every load-bearing claim in the panel's findings against the tree this session, and **all twelve reproduce**. This is an accurate, well-grounded review that improves the proposal; I am not going to defend around it. The core thesis survives untouched — the verified fact that a default install strips the MIT notice from every shipped tool and installs no CC-BY attribution, and that this becomes a live breach the day the postdoc's repo goes public, stands exactly as written (the SPDX/`Copyright (c)` grep over `templates/`+`scripts/` returns zero header hits this session; 44 template `.py`, 44 `.md` templates, 43 substituted `.md` cached per install). What the review corrects is **scope, the verification plan, and citation precision** — not the design or its doctrinal footing. So this is a **revise**, not a supersession: no finding is dispositive, none says the mechanism fails or that doctrine forbids it, and the strongest structural finding (R4) is a split the proposal itself already offered.

I accept all twelve. Dispositions below; the corrected design is in the Revised proposal section.

**R1 — accept.** Confirmed and it is my error inverted: `ast.dump(include_attributes=False)` is comment-insensitive (`bootstrap/tests/_ast_attest.py:13-14`, `:83`), so P2's SPDX headers do **not** trigger a re-anchor, while P1's `_CORE_MAPPINGS` edit does — `Assign:_CORE_MAPPINGS` is a baseline key and the digest is value-sensitive; the re-anchor obligation belongs to P1 (config.py) unconditionally, not to P2.

**R2 — accept.** Confirmed: `test_ast_attest.py` is already red on a clean tree (2 failed / 24 passed this session) with `install.py`/`config.py` symbols already CHANGED (tracked Issue #1), and P1 edits `config.py` — the very already-failing surface — so the "does not touch" disclaimer is false and the current-red state was an unrecorded evidence gap.

**R3 — accept.** Confirmed: the self-propagation vehicle is the 44 `templates/` **sources** (manifest source column is 100% rooted at `templates/`, zero paths begin `scripts/`); Cairn's own `scripts/` is a 24-file mix of template twins (`scripts/claim_check.py` is byte-identical to `templates/modules/default-on/claim_check.py`) and never-shipped dev tooling (`quality_gate.py`, `check_cairn.py`, `measurements.py`, `token_budget.py`, `verify_counts.py` — all 0 manifest rows), so P2 conflated adopter self-propagation with Cairn's own-repo hygiene, mis-stated the count (16 top-level vs 24 recursive), and left a silent twin-divergence hazard.

**R4 — accept (take the split).** Confirmed and I agree the scope reviewer's call is correct: P3 is the only install-contract-*schema* change, a different risk class **and** a different purpose (traceability, which neither MIT nor CC-BY requires, vs. the compliance P1/P2 fully discharge), and it is absent from the broad-look's A4 enumeration (`…:562-565` lists notice/headers/paragraph/contributions) — bundling it repeats exactly the "contract change married to near-mechanical fixes" pattern a prior proposal was forced to split, so P3 leaves as its own proposal.

**R5 — accept with modification.** Confirmed the premise misreads the instruments: `LICENSE-CC-BY.md:15-18` Exception 1 and `LICENSE-MIT.md:3-8` are concept-based ("source code (`.py` **or other code**), wherever it lives"), not extension-based, so a functional `vendor_targets.yml` is plausibly **already** MIT "other code" and the "outside both families / code=.py, prose=.md" framing is wrong; my modification of the reviewer's either/or is to reframe P6 as a *clarifying example* of Exception 1's existing coverage (not a coverage change) **and** route the classification sign-off to the Maintainer alongside the CC-BY clause — because a scope-note to a legal instrument is the Maintainer's call by the same principle I invoked to reserve the CC-BY clause, and consistent handling requires it.

**R6 — accept.** Confirmed the by-file split is mirrored across all three instruments (`LICENSE-MIT.md:9-13`, `LICENSE-CC-BY.md:15-24`, `LICENSE-CC-BY-ND.md:18-27`) plus the `AGENTS.md:315` "keep the three families from overlapping" invariant, so a one-instrument P6 edit risks the drift that invariant guards; the plan will place the clarification in one canonical home with the other two pointing to it (or mirror consistently), stated in the routing section.

**R7 — accept.** Confirmed `CITATION.cff:19-21` lists only CC-BY-4.0 and MIT (zero ND hits), so the `["MIT","CC-BY-4.0","CC-BY-ND-4.0"]` example contradicted its stated source; this fix carries to the split-out P3 proposal, whose `licenses` field either reads the two-value CITATION.cff verbatim (noting CC-BY-ND covers only the brand mark, which adopters never install) or sources the three-family list from the LICENSE instruments and drops the "sourced from CITATION.cff" attribution.

**R8 — accept.** Confirmed `PROVENANCE.md:59-63` disclaims content **safety** ("says nothing about whether the content is safe"), not license **terms**, so attaching "or terms" to that quote was a scope-stretch of the exact misquote class that kills proposals here; I will support the origin-not-license point from `PROVENANCE.md:74-83` (which lists version/commit/profile/hash — notably no license/creator/URL) instead.

**R9 — accept.** Confirmed A4 (`…:562-565`) does not enumerate the lockfile; its receipt-provenance motivation lives in Theme 4 prose (`…:288-302`), so Alternative 2's "the review named all four as one package" overstated backing — and this reinforces R4, since P3 was always an addition beyond the A4 package.

**R10 — accept.** Confirmed 34 shipped `.py` carry a line-1 shebang, so the header must sit *after* any shebang and the enforcing assertion must scan the first ~3 lines, not only line 1, or it false-negatives on every launcher.

**R11 — accept.** Confirmed `dev/.cairn/base/` is absent in Cairn's own tree (0 files, 0 `base_cache` lockfile records — Cairn was `--init-lock` migrated), so "43 cached `.md`, as_of" overstated an existing-tree count; the underlying mechanism (`install.py:1558-62`) is real, but I will reframe as "43 `.md` cached **per install** (manifest-derived, as_of 2026-07-11)."

**R12 — accept.** Agreed the entire residual risk is P4's first-read framing for a solo postdoc with a PI watching (ongoing cost is genuinely near-zero — nothing always-loaded is added); I will lead P4 and `NOTICE.md`'s opening with reassurance ("Cairn asks essentially nothing of you: keep `NOTICE.md`"), obligations second, 3-4 sentences.

**On the second-round recommendation:** accepted — after I land these revisions the package goes to an External (cross-type) read before the Decision, per the proposal's own `Plan review` line and the standing workflow. The two facets the panel flagged as outside the Internal lens — the **legal-sufficiency** judgment (does one `NOTICE.md` + self-propagating headers actually discharge MIT notice-retention and CC-BY attribution for files copied *out* of the tree) and the reserved Maintainer co-decisions — are precisely what External and the Maintainer should adjudicate; no test settles them and I make no claim that they are settled.

## Revised proposal -- 2026-07-11

**Shipping unit.** P1 + P2 + P4 + P5 + P6 land as the coherent pre-0.4 **compliance** package. **P3 (lockfile `source_repository` + `licenses` fields) is withdrawn from this proposal and re-opened as a separate install-contract proposal** (R4) that owns the `_LOCK_SCHEMA`-bump-vs-additive decision (`lockfile.py:42`) and the manifest/fidelity re-anchor; the R7 licenses-field/CITATION.cff fix travels with it. The `Touches` line drops `lockfile.py` and the `install.py` lock-dict edit; the forward-reference `claim-check-allow` directive is unchanged (still P1's `NOTICE.md` files).

**P1 (unchanged in intent, corrected in consequence).** Add `templates/core/NOTICE.md`, wire `("core/NOTICE.md","NOTICE.md")` into `_CORE_MAPPINGS` (`config.py:165`), add Cairn's own repo-root `NOTICE.md` in the same commit. **New, explicit:** this `config.py` edit changes the `Assign:_CORE_MAPPINGS` baseline symbol and therefore **requires a supervised re-anchor of `scaffold_ast_baseline.json` per `REANCHOR_RUNBOOK.md`** — independent of P2 (R1). Because the baseline is already red from tracked Issue #1 (R2), the plan **inspects the current CHANGED set first**, confirms every drifted symbol is an already-accepted change, and only then re-records — the re-anchor closes Issue #1 as a reviewed side effect, not a blind absorption. Manifest data rows move 94 → 95.

**P2 (scope corrected — R3, R10).** The adopter-facing self-propagating compliance set is the **44 `templates/` source `.py`** (they install verbatim, so the header travels into the adopter tree and any copy made from it). Headers on Cairn's **own** non-shipped `scripts/` + `bootstrap/` `.py` are a **separate** own-repo MIT-redistribution hygiene item (correct to do, different justification, non-propagating) — the plan may include them but must not conflate them with adopter propagation. Recursive `scripts/` count is 24 (top-level 16), stated with three-kind discipline. Twin pairs (`scripts/claim_check.py` ↔ `templates/modules/default-on/claim_check.py`, `link_check.py`, the `_onboarding/*` package) get headers **in lockstep** so they stay byte-identical, preserving the `install.py:1547-48` divergence / `base_hash` check on the self-host side; the plan adds — or explicitly records the absence of — a scripts↔templates parity check. Header placement is **after any shebang** (34 files), and the enforcing assertion scans the first ~3 lines. P2 headers are comment-only and do **not** trigger an AST re-anchor (R1).

**P4 (framing — R12).** "Licensing of the installed files" leads with reassurance ("Cairn asks essentially nothing of you: keep `NOTICE.md`"), states the minimal obligation second, 3-4 sentences, no legalese; `NOTICE.md`'s opening line mirrors the tone.

**P5 — unchanged.** One inbound=outbound sentence in `case-studies/README.md:88-99`.

**P6 (reframed — R5, R6).** Reframed from "config/data files sit outside both families" (false) to a **clarifying example that functional configuration/data files (`.yml`/`.txt`, e.g. `vendor_targets.yml`, `content_scan_*.txt`) are "other code" already covered by MIT under `LICENSE-CC-BY.md:15-18` Exception 1** — so `AGENTS.md:313-315`'s "code is MIT wherever it lives" stays accurate and the routing claim ("none route to `doctrine/`/`AGENTS.md`") holds. Because the family statement is mirrored across all three instruments, the plan places the clarification in **one canonical home with the other two pointing to it** (R6). The `.yml`/`.txt`="other code" **classification is routed to the Maintainer** for sign-off alongside the CC-BY downstream clause — consistent handling of legal-instrument judgments (R5b). If the Maintainer prefers, P6 defers entirely with the CC-BY clause; it is the least urgent element and the gap it closes is interpretive, not a coverage hole.

**Verification plan (corrected — R1, R2, R8, R9, R11).** Drop the "suite stays green modulo failures this proposal does not touch" disclaimer; state instead that P1 lands a supervised AST re-anchor that also closes Issue #1, with the baseline's current red state (2 failed / 24 passed) recorded before/after. Cite P3's motivation — in its own new proposal — to Theme 4 (`…:288-302`), not A4. Support the origin-not-license point from `PROVENANCE.md:74-83`, dropping the `:59-63` safety citation. Reframe the cache figure as "43 `.md` cached per install (manifest-derived, as_of 2026-07-11)."

**Reserved to the Maintainer at Decision:** (a) the CC-BY downstream-permission clause (open question, unchanged); (b) the notice name/home (recommended: repo-root `NOTICE.md`); (c) new — the P6 `.yml`/`.txt`="other code" classification sign-off. **Next tier:** External (cross-type) read of this revised package before the Decision, focused on legal-sufficiency of the `NOTICE.md`-plus-headers discharge.

## Review -- Gemini (External, different-agent-type) -- 2026-07-22

**Model**: Gemini 3.6 Flash / Antigravity
**Verdict**: SHIP (conditional on Maintainer resolution of open questions and AST baseline re-anchoring)

### Steelman
This proposal solves a critical, verified release-blocker (Theme 4): default Cairn installs currently redistribute notice-stripped MIT tools and un-attributed CC-BY markdown templates. The revised package (P1 + P2 + P4 + P5 + P6) cleanly discharges all downstream licensing obligations with minimal adopter friction (a single repo-root `NOTICE.md` + self-propagating SPDX headers on shipped Python source files). Splitting out P3 (lockfile schema modification) to its own proposal protects the byte-level-stable install contract, while keeping P1/P2/P4/P5/P6 zero-token and standard-library compliant.

### Critiques

* **[E1] (Legal Sufficiency of Discharging Mechanics)**
  The legal-sufficiency model is sound: `NOTICE.md` placed at the adopter repository root discharges CC BY 4.0 Section 3(a) attribution and global MIT notice requirements for the installed tree as a whole. Self-propagating SPDX headers (`# SPDX-License-Identifier: MIT`) placed after shebang lines in all 44 `templates/` Python sources guarantee notice retention even if individual tool scripts are copied out of the repository tree.
* **[E2] (AST Attestation Baseline Re-anchoring Control)**
  P1's addition of `("core/NOTICE.md", "NOTICE.md")` to `_CORE_MAPPINGS` in `bootstrap/_scaffold/config.py` modifies a baselined symbol digest (`Assign:_CORE_MAPPINGS`). The implementing plan must execute the supervised `REANCHOR_RUNBOOK.md` flow in lockstep with P1 to close tracked Issue #1 cleanly without leaving un-anchored intermediate commits.
* **[E3] (P6 License Family Scope Clarification Placement)**
  Classifying functional `.yml`/`.txt` configuration and data files as "other code" under `LICENSE-CC-BY.md` Exception 1 correctly preserves `AGENTS.md:313-315`'s non-overlapping family invariant. The plan should place the clarification canonically in `LICENSE-CC-BY.md` Exception 1 with brief cross-references in `LICENSE-MIT.md` and `AGENTS.md` to prevent doc-drift across legal instruments.

### Coverage

* **Covered**:
  * Verified mapping of `_CORE_MAPPINGS` in `bootstrap/_scaffold/config.py:165`.
  * Checked license instruments (`LICENSE-MIT.md`, `LICENSE-CC-BY.md`, `LICENSE-CC-BY-ND.md`) and verified `CITATION.cff:18-21` repository/license fields.
  * Verified AST attestation baseline dependencies in `bootstrap/tests/test_ast_attest.py`.
* **Not covered**:
  * P3 lockfile provenance schema modifications (deferred to separate proposal).
  * Implementation of `bootstrap/tests/test_notice_install.py` (to be verified during plan execution).

## Decision -- {{Maintainer}} -- {{YYYY-MM-DD}}

*(Awaiting the Maintainer. The revised P1+P2+P4+P5+P6 package has cleared both Internal and External reads. Three decisions belong to the Maintainer: (1) Accept/reject the revised compliance package; (2) Open Question OQ: whether to add the downstream-permission clause to `LICENSE-CC-BY.md`; (3) P6 classification sign-off for `.yml`/`.txt` configuration files as MIT Exception 1 code.)*