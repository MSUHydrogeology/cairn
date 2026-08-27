<!-- Why exempt: these are illustrative adopter-tree / framework-runtime / historical `dev/` paths this proposal cites as EXAMPLES of the very findings it resolves -- dogfooding the category-C exemption mechanism it recommends. (claim-check-allow takes no reason= field, so the rationale lives here.) -->



# check_cairn: resolve the `dev/` claim-path findings self-hosting introduced

> **Erratum (2026-07-14, link-maintenance only per `doctrine/proposals.md:136-140`
> — no other edit to this closed file).** This proposal's Internal review
> below is headed "same-session," not fresh-session (below the doctrine
> floor), and its `Plan review: required(Internal)` header line was never
> addressed by the Decision (no plan was opened). Both are dated,
> recorded incidents at `dev/measurement/review-floor-deviations.md`. The
> accurate provenance of this file's review-section commit history (what
> `17b7e5c` and `f4a8308` actually each contain) is recorded at
> `dev/plans/archive/review-record-integrity.md` > "Showcase-arc
> provenance record." Everything below this notice is unedited.

**Author**: Claude (Strategy)
**Model**: Claude Opus 4.8
**Date opened**: 2026-06-12
**Status**: accepted
**Touches**: `templates/modules/default-on/claim_check.py` (the shipped claim-path checker), `scripts/check_cairn.py` (Cairn's self-check wiring), and a handful of product-prose files that cite `dev/` paths (`CHANGELOG.md`, `doctrine/*`, `templates/*`, `examples/*/README.md`, `bootstrap/*`, `docs/quickstart.md`).
**Related**: the Cairn self-host adoption (2026-06-12, `dev/.cairn/profile.yml`); BOOTSTRAP Act II-5 (R-F gate); the existing `_CAIRN_INTERNAL_PREFIXES` loop-fidelity gate in `scripts/check_cairn.py` (the mirror-image precedent).
**Plan review**: required(Internal) — touches the shipped claim-check (a protected install contract); ratified at Decision.

## Context

Adopting Cairn within Cairn created a real top-level `dev/` tree for the
first time. `scripts/check_cairn.py` runs the **shipped** claim-path
checker (`templates/modules/default-on/claim_check.py`) over Cairn's
Markdown. That checker resolves a backticked `X/…` token **only when
`X` is a real top-level entry of the repo** (`check_path_claim`: `first
= token.split('/', 1)[0]; if first not in top_level: return None`).

Before self-hosting, `dev/` was not a top-level entry, so every
`dev/` citation in Cairn's product prose was silently skipped. Now
`dev/` exists, those tokens resolve against Cairn's own tree, and **66
hard-fail** (`python scripts/check_cairn.py` → 66 issues). **None are in
the installed apparatus** (`AGENTS.md`, the `dev/` tree) — all are in
product prose that cites `dev/` paths describing an *adopter's* tree, a
*framework-runtime* path, or *another repo's* history.

This is a genuine self-compatibility gap the adoption surfaced — the
prose gate was written assuming Cairn has no `dev/` tree.

## Proposal

Resolve the findings with Cairn's **standard exemption mechanisms** — not
a bespoke `check_cairn`-local filter (a local filter would be exactly the
"second copy that drifts" the file's design philosophy forbids; it was
prototyped and rejected). The 66 cites fall into three categories, each
mapped to the standard surface designed for it:

### Category B — framework runtime/config paths (~18 cites)

`dev/.cairn/base/`, `dev/.cairn-upgrade/`, `dev/cairn-lock.yml`,
`dev/.cairn/metrics-config.json`, `dev/intent-config.json`,
`dev/.cairn/foldback_export_denylist.txt`, … — generated or
gitignored framework paths that are **absent by design** in any tree.

* **Mechanism:** extend the shipped `claim_check._DEFAULT_EXEMPT_PATHS`
  — the frozenset that **already** holds `dev/intents.jsonl` for exactly
  this reason. Because several of these are directories / prefixes
  (`dev/.cairn/`, `dev/.cairn-upgrade/`), `_DEFAULT_EXEMPT_PATHS` gains
  **prefix matching** (today it is exact-membership only). This is the
  *only* change to the shipped tool, and it is correct for **every**
  self-hosting adopter: these are framework-managed, absent-by-design
  paths, not project claims.

### Category A — historical / other-repo references (~28 cites)

`CHANGELOG.md` cites the **reference repo's** lifecycle
(stems under `dev/proposals/archive/` + `dev/plans/archive/`) — Cairn's
construction was tracked in modflow_tools' `dev/`, not Cairn's own.
`examples/*/README.md` cite their own **hypothetical** example tree
(`dev/proposals/archive/0001-add-name-argument.md`).

* **Mechanism:** the standard file-scoped `external_allow` already used
  for `case-studies/*.md` (these files describe *another* tree), for the
  example READMEs; and a **document-scoped `claim-check-allow`**
  directive at the top of `CHANGELOG.md` naming the historical
  `dev/proposals/**` + `dev/plans/**` globs (surgical — CHANGELOG also
  cites *real* Cairn paths, so it must not be whole-file exempted).

### Category C — illustrative adopter-tree doc paths (~20 cites)

`dev/vision.md`, `dev/architecture_review.md`,
`dev/measurement/incident_log.md`, `dev/rules/custom_session_routines.md`,
`dev/modules/legacy-agent.md` (a module **not** in Cairn's own profile)
— doctrine/templates describing where an *adopter* would keep things.

* **Mechanism:** document-scoped `claim-check-allow` directives in the
  citing doctrine/template files, naming the specific `dev/` globs. This
  is the direct mirror of the existing `cairn-internal-ref-allow`
  directive the loop-fidelity gate already uses for the opposite
  direction (an adopter surface citing Cairn-internal `doctrine/`).

### Documentation / doctrine surface

* `templates/modules/default-on/claim_check.py` docstring — document the
  prefix-matching of `_DEFAULT_EXEMPT_PATHS` and the framework-path
  rationale (it ships to adopters).
* `scripts/check_cairn.py` docstring — note the self-host exemption set.
* `CHANGELOG.md > Unreleased > Fixed` — one line.
* No `doctrine/` change: this is tooling behaviour, not a rule every
  contributor follows. The doctrine-change rate-limit gate does not apply.

## Rationale

* **Keeps the "run the exact shipped tool, no local fork" invariant.**
  The fix lives in standard exemption surfaces (`_DEFAULT_EXEMPT_PATHS`,
  `external_allow`, `claim-check-allow`), not a parallel `check_cairn`
  filter — so Cairn keeps dogfooding the same checker it hands adopters.
* **The one shipped-tool change is a general improvement.** Prefix-
  capable `_DEFAULT_EXEMPT_PATHS` is something *every* self-hosting
  adopter needs the moment they cite a `dev/.cairn/` runtime path in
  their own docs — Cairn is just the first to hit it.
* **The gate stays sharp.** A *real* broken `dev/` link authored from
  **inside** Cairn's own `dev/` tree still fails — only product-prose
  cites of adopter/runtime/historical paths are exempted, and each
  exemption is auditable (a named directive or the framework path set).
* **Now is the right time.** The adoption commit should not land a repo
  whose own prose gate reports 66 findings; fixing it via the lifecycle
  is also the cleanest first exercise of the apparatus we just installed.

## Alternatives considered

1. **Do nothing** — leave the gate red on Cairn. Rejected: a red
   self-check erodes the "we pass the gate we preach" claim and buries
   any *real* future `dev/` finding in 66 standing false positives.
2. **A bespoke `check_cairn`-local filter** (`_ADOPTER_TREE_PREFIXES` +
   a post-filter over the shipped checker's flags). Prototyped, then
   rejected on Maintainer steer: it forks behaviour away from the
   shipped tool — the exact drift `check_cairn`'s design forbids.
3. **Whole-file `external_allow` for every citing file.** Rejected:
   `CHANGELOG.md` and the doctrine files cite *real* Cairn paths too, so
   a whole-file exemption over-exempts and blunts the gate.
4. **Recommended: per-category standard mechanisms** (above).

## Evidence / verification plan

The three things this change accounts for: the **tests**, the
**examples / smoke checks**, and the **docs** (named above).

### Author-accounting — invariants, failure modes, edge cases

* **Invariant** — a `dev/` claim authored from *inside* Cairn's own
  `dev/` tree still hard-fails when broken (the exemptions are scoped to
  product-prose surfaces + the framework path set, never to `dev/`-tree
  self-references). *Enforcer:* a new test (below).
* **Failure mode** — the exemption is *open* (it suppresses a finding);
  the risk is suppressing a real one. Bounded by scoping each exemption
  to a named glob / the explicit framework-path set, and by the
  invariant test for the `dev/`-internal case.
* **Edge cases** — a `dev/.cairn/` *directory* cite (prefix match, not
  exact); a `dev/` cite that *does* resolve in Cairn's tree (must still
  pass without an exemption); a future not-yet-installed module's
  `dev/modules/<m>.md` cite.
* **Known omission** — the directive-glob specificity rule (`claim_check`
  requires ≥2 literal segments + a literal final stem) may not express a
  blanket `dev/measurement/*.md`; the plan resolves the exact globs.

### Tests required

* A new `bootstrap/tests/test_check_cairn_*` case asserting: (a) a
  `dev/.cairn/base/` cite in a product file is exempt; (b) a broken
  `dev/` cite from a file *under* `dev/` still fails; (c) prefix vs
  exact matching in `_DEFAULT_EXEMPT_PATHS`.
* The shipped `claim_check`'s own suite stays green (the change is
  additive to its default-exempt set).

### Examples / smoke checks

* `python scripts/check_cairn.py` → **0 issues** (from 66).
* `python -m pytest bootstrap/tests` stays green **except** the
  separately-tracked pre-existing `test_ast_attest` baseline-drift
  failures (a distinct issue, captured separately — not regressed here).

## Signals the change is wrong

* `check_cairn` goes green but a genuinely broken `dev/` link inside
  Cairn's own `dev/` tree no longer fails → the exemption is too broad;
  tighten the scoping.
* An adopter reports their own legitimate broken `dev/` path is no longer
  caught → the shipped `_DEFAULT_EXEMPT_PATHS` extension over-reached;
  narrow it to the framework-managed set.

## Review -- Claude (Internal, same-session) -- 2026-06-12

**Model**: Claude Opus 4.8

*Independence caveat: this is a same-session Internal read — independence
by intent, not yet by fresh session or structure. Because the change
touches **shipped** code (`claim_check.py`, every adopter inherits it), a
cross-type External pass (a second agent type) is recommended before
implementation; see the second-round recommendation.*

**Steelman.** The proposal is right on the load-bearing point: the fix
belongs in standard exemption surfaces, not a `check_cairn`-local filter,
and it correctly identifies that the *one* shipped-tool change
(prefix-capable `_DEFAULT_EXEMPT_PATHS`) is a general improvement every
self-hosting adopter needs — not a Cairn-only patch. The
three-category decomposition is accurate and each cite was verified
against the live gate. Keeping the `dev/`-internal self-reference case
*failing* is the right invariant and is testable.

**Concerns** (numbered for point-by-point Response):

* **[R1] Three mechanisms vs. one — the consistency question.** The
  repo already has a code-level mirror of exactly this problem:
  `_CAIRN_INTERNAL_PREFIXES` + the `cairn-internal-ref-allow` marker
  handle "an adopter surface cites a Cairn-only `doctrine/` path." This
  proposal handles the inverse ("a Cairn-product surface cites an
  adopter `dev/` path") with *three* mechanisms instead of a single
  symmetric prefix-set. Worth deciding deliberately: is the asymmetry
  justified (the inverse genuinely spans runtime + historical +
  illustrative), or would a `_PRODUCT_CITES_ADOPTER_PREFIXES` set —
  scoped to resolve `dev/…` only from inside `dev/` — be the cleaner,
  single, symmetric design? The latter is closer to "one standard
  mechanism" and avoids per-file directive sprawl (R2).

* **[R2] Category-C directive sprawl + the glob-specificity wall.**
  Category C wants `claim-check-allow` directives across ~8
  doctrine/template files, and the directive forbids subtree globs
  (`dev/measurement/*.md` is rejected — only fully-literal or
  ≥2-literal-segment-plus-stem). So each illustrative path is named
  individually, and a *new* illustrative cite later silently re-breaks
  the gate until someone adds it. That maintenance tail is real; it
  strengthens the R1 case for a code-level prefix rule for category C
  specifically.

* **[R3] `_DEFAULT_EXEMPT_PATHS` prefix breadth.** Exempting the
  `dev/.cairn/` *prefix* in the **shipped** checker means an adopter's
  own broken `dev/.cairn/<typo>.json` doc cite stops being caught
  everywhere. That is probably acceptable (the whole subtree is
  tool-owned machine state) but it is a real widening of the shipped
  tool's blind spot and should be a conscious Decision, scoped to the
  `.cairn/` machine-state subtree rather than `dev/` broadly.

* **[R4] CHANGELOG maintenance.** The historical-cite directive on
  `CHANGELOG.md` grows every time a future entry references a
  `dev/proposals/archive/…` stem. Minor, but name it as expected cost.

**Coverage.**
* *Covered* — the mechanism mapping against the 66 live findings
  (re-ran `check_cairn`; categorized every cite); the `_DEFAULT_EXEMPT_PATHS`
  precedent (`claim_check.py:408` already holds `dev/intents.jsonl`); the
  directive-parser constraint (verified empirically — `reason=` is not
  supported; fully-literal globs incl. trailing-slash dirs are accepted);
  the self-reference invariant is testable.
* *Not covered / low confidence* — I did **not** prototype the R1
  unified-prefix alternative to compare diff size; no cross-type
  independence on this pass (same author and reviewer agent type); the
  exact category-C glob list is deferred to the plan and unverified.

**Second-round recommendation: recommended.** The mechanism choice (R1:
three standard mechanisms vs. one symmetric prefix-set) is a genuine
design fork on a shipped, adopter-facing surface — exactly where a
different-agent-type read earns its keep. Recommend a cross-type
External review before implementation. The Decision may still proceed on
the Internal read if the Maintainer prefers the documented three-mechanism
approach.

## Review -- Gemini (External, different-agent-type) -- 2026-06-12

**Model**: Gemini 3.5 Flash (High)

**Steelman first:**
The proposal correctly identifies that adopting Cairn within Cairn has introduced a mismatch where the prose-integrity gate (`check_cairn.py`) tries to resolve illustrative or hypothetical `dev/` paths against Cairn's own actual `dev/` tree. The three-category structure maps the findings cleanly to the precise scope of each exemption, ensuring we keep the shipped tool clean and the self-check gate sharp.

### Substantive Critiques and Feedback

* **[R1] On Internal Review's suggestion of a single symmetric prefix-set:**
  The Internal Reviewer suggests replacing the three mechanisms with a single symmetric prefix-set `_PRODUCT_CITES_ADOPTER_PREFIXES` in `scripts/check_cairn.py` to prevent "directive sprawl".
  **We strongly disagree.** The proposed three-mechanism approach is structurally correct because it scopes each exemption to its appropriate layer:
  1. *Category B (Framework runtime paths):* Shipped code-level exemption (`_DEFAULT_EXEMPT_PATHS`) because *every* adopter's repository will have these same gitignored, generated paths.
  2. *Category C (Illustrative template paths):* File-level `claim-check-allow` comment directives inside the templates. Because they are in the templates, they travel with the files when adopted. If we used a Cairn-only code-level prefix filter, these template files would fail the claim check in the adopter's repo unless the adopter also added custom exemptions.
  3. *Category A (Historical modflow_tools path):* File-level `claim-check-allow` in `CHANGELOG.md`. This is specific to Cairn's history and should not be in any shipped tool.
  Thus, a single symmetric prefix-set in `scripts/check_cairn.py` would only cover Cairn's own self-check, leaving adopters to face dangling claims when they run `check_cairn` on their adopted templates.

* **[R2] On Internal Review's glob-specificity concern (R2):**
  We agree with the author that the glob-specificity rule (`allow_glob_error` in `claim_check.py`) must remain strict. Allowing wildcard-leading final segments (`dev/measurement/*.md`) would create a significant blind spot in the gate, allowing typos or missing files to pass unchecked. Spelling out the paths is a necessary cost to keep the gate sharp.

* **[R3] Prefix matching implementation details (Addressing R3):**
  The prefix matching on `_DEFAULT_EXEMPT_PATHS` must be implemented carefully to avoid over-exemption. If we do a simple `any(token.startswith(p) for p in _DEFAULT_EXEMPT_PATHS)`, then `dev/intents.jsonl.bak` would be silently exempted because it starts with `dev/intents.jsonl`.
  *Satisfier:* We must ensure that prefix matching only matches exact paths or actual subpaths of directories (i.e. by ensuring directory prefix entries in `_DEFAULT_EXEMPT_PATHS` end with a `/` and matching on `p` or `p.rstrip('/') + '/'`).

**Coverage Line:**
* **Covered:** Lenses 1-9 swept against `templates/modules/default-on/claim_check.py` and `scripts/check_cairn.py`.
* **Not covered / low confidence:** We did not write or test the exact implementation changes to `claim_check.py` yet (deferred to the plan).

**Second-round recommendation: recommended.**
The proposal is sound, and the three-mechanism approach is the correct architectural choice. The Maintainer should approve the proposal once the prefix-matching safety detail (above) is integrated.

## Revised proposal -- 2026-06-12

The two reviews converge on the three-mechanism approach; two refinements
land, and nothing else in the original Proposal changes.

1. **The layering rationale is now load-bearing (External E-R1).** The
   three mechanisms are not merely convenient — each lives at the layer its
   exemption must live at, and that is *why* the asymmetry with the
   `_CAIRN_INTERNAL_PREFIXES` gate is correct rather than an oversight:
   * `_DEFAULT_EXEMPT_PATHS` (shipped code) for the framework paths
     **every** adopter has;
   * in-template `claim-check-allow` directives for illustrative paths, **so
     the exemption travels with the adopted template** — a Cairn-only
     code-level prefix filter would leave every adopter facing dangling
     claims on those same templates when they run their own `check_cairn`;
   * a Cairn-only `CHANGELOG.md` directive for Cairn's own history, which
     should never ship in a tool.

2. **Prefix-match safety constraint (Internal I-R3 / External E-R3).** The
   `_DEFAULT_EXEMPT_PATHS` prefix matching is `/`-terminated and subtree-
   scoped. A directory entry is stored with a trailing `/` and matches a
   token only when `token == p.rstrip('/')` **or**
   `token.startswith(p.rstrip('/') + '/')` — so `dev/intents.jsonl` still
   exempts exactly itself and `dev/intents.jsonl.bak` is **not** silently
   exempted. The directory-prefix entries are limited to the
   `dev/.cairn/` machine-state subtree plus the named `dev/.cairn-upgrade/`
   — never `dev/` broadly. The plan adds an explicit edge-case test for the
   `.bak` non-exemption.

## Response -- Claude (author) -- 2026-06-12

**Model**: Claude Opus 4.8

Both reviews recommend approval and converge on the three-mechanism
approach; the External (Gemini) read resolved the one open fork (R1) with
an argument the proposal had not made explicit — that the Category-C
directives must travel with adopted templates. Dispositions, no silent
drops:

**Internal review (Claude, same-session):**
* **[I-R1] unified prefix-set alternative — reject.** The External review
  is decisive: a single code-level prefix-set in `scripts/check_cairn.py`
  covers only Cairn's own self-check, but the Category-C exemptions live in
  template files that get *adopted*, so a Cairn-only filter would leave
  every adopter with dangling claims on the same templates. The asymmetry
  with `_CAIRN_INTERNAL_PREFIXES` is justified by the layering.
* **[I-R2] directive sprawl / glob-specificity — accept.** Recorded as an
  accepted maintenance cost; the glob-specificity rule stays strict (both
  reviewers agree relaxing it would blind the gate).
* **[I-R3] `_DEFAULT_EXEMPT_PATHS` prefix breadth — accept with modification.**
  Scoped to the `dev/.cairn/` machine-state subtree (+ named entries), not
  `dev/` broadly, and `/`-terminated — see the Revised proposal.
* **[I-R4] CHANGELOG maintenance — accept.** Named as expected cost.

**External review (Gemini via Antigravity, different-agent-type):**
* **[E-R1] three mechanisms are structurally correct — accept.** Adopted as
  the load-bearing rationale (Revised proposal §1); this is the argument
  that settles the design fork.
* **[E-R2] keep glob-specificity strict — accept.** No relaxation of
  `allow_glob_error`; spelling out paths is the necessary cost.
* **[E-R3] prefix-match safety (`/`-terminated) — accept with modification.**
  Folded into the Revised proposal §2 and the verification plan, with an
  explicit `dev/intents.jsonl.bak` non-exemption edge-case test.

## Decision -- Anthony Kendall (Maintainer) -- 2026-06-12

**Accepted — implement directly (no formal plan).**

Maintainer authorization (verbatim, via the kickoff Decision prompt):

> "Accept — implement directly"

Scribed by Claude at the Maintainer's explicit instruction. The revised
proposal is the implementation contract: the three-mechanism mapping
(shipped `_DEFAULT_EXEMPT_PATHS` for framework paths; in-template
`claim-check-allow` directives for illustrative paths so they travel with
adopted templates; a Cairn-only `CHANGELOG.md` directive for history) plus
the `/`-terminated, `dev/.cairn/`-scoped prefix-match safety constraint
(R3). Per the Maintainer's direction the fix lands directly in a couple of
well-scoped commits rather than via a plan; this proposal archives at the
implementing commit.

## Code review -- Gemini (External, different-agent-type) -- 2026-06-12

**Model**: Gemini 3.5 Flash (High)

### 1. Falsification Ledger

* **Surfaces probed**:
  - Examined the implementation of `_is_default_exempt` and the updated `_DEFAULT_EXEMPT_PATHS` and `_DEFAULT_EXEMPT_PREFIXES` in [claim_check.py](file:///Users/kendal30/Code/cairn/templates/modules/default-on/claim_check.py#L408-L470).
  - Validated that the copy in [scripts/claim_check.py](file:///Users/kendal30/Code/cairn/scripts/claim_check.py) is byte-identical to the template source.
  - Verified the 7 added `claim-check-allow` directives in the files changed by the commit to ensure they are minimal and correct.
  - Verified that restoring the `.gitkeep` file in [strategy/archive/.gitkeep](file:///Users/kendal30/Code/cairn/templates/core/dev/strategy/archive/.gitkeep) is correct because `dev/strategy/README.md` explicitly links `archive/`, whereas proposals/archive and plans/archive do not have linking READMEs in templates.

* **Negative / edge-case attempt**:
  - Traced the `_is_default_exempt` function logic for negative cases to ensure that:
    1. A suffix-matched file like `dev/intents.jsonl.bak` does *not* match `dev/intents.jsonl`.
    2. A directory sibling like `dev/.cairn-upgrade-bak/` does *not* match the prefix `dev/.cairn-upgrade/`.
    3. A missing committed file like `dev/.cairn/cairn-lock.yml` is *not* exempted by `_DEFAULT_EXEMPT_PREFIXES` and will correctly flag if absent.

* **Verification**:
  - Ran `python scripts/check_cairn.py` over the entire repository to confirm that all 69 + 3 path-claim errors have been resolved (exited with code `0` / OK).
  - Ran `python -m pytest bootstrap/tests` to verify the 5 new tests in [test_claim_check_module.py](file:///Users/kendal30/Code/cairn/bootstrap/tests/test_claim_check_module.py#L282-L332) pass successfully, pinning the exact matching, prefix matching, slash-termination, suffix rejection, and committed-file verification.

* **Residual risk**:
  - Pre-existing AST baseline failures (`test_ast_attest.py` failures under Python 3.12 due to minor version serialization differences) remain present (tracked as issue #1). This is unrelated to the self-host compatibility changes.

### 2. Coverage Line
* **Covered**: Swept lenses 1-9 (Claims, Production path, Design completeness, Silent failure, Cross-document consistency, Drift, Lifecycle placement, Domain scope, and Satisfier) against commit `f9464b2`.
* **Not covered / low confidence**: None. Full execution and verification checks were run locally.

### 3. Verdict
**Accept (commit f9464b2).** The changes are faithful to the accepted proposal contract, correct, minimal, and completely safe.



