# Repository layout: one folder per purpose, Cairn self-contained under `dev/`

**Author**: Claude Opus 5.5 (`claude-opus-5-5`), Strategy
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: heavy — the moves touch the installer, every protected test, the gate manifest, the interpreter-binding reader and both `AGENTS.md` files
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-09
**In brief**: Reorganize Cairn's folders so each one's name says what it holds, and install everything Cairn puts in an adopter's repository under `dev/`.

## Decision summary

Give Cairn one coherent layout and exercise it through self-adoption in v0.8:
installer inputs in `templates/`, installation guidance in `install/`, Cairn-only
tests and release machinery in `tests/` and `release/`, installed tools in
`dev/tools/`. Adopters keep root governing files and `.agents/skills/`.

Cost: one heavy plan, a quiet migration window, adopter command-path changes,
and one Maintainer re-anchor shared with v0.8; zero recurring human operations.
Local modifications must survive; uncertainty stops migration, not protection.

## Context

Sources: `bootstrap/_scaffold/config.py` mixes tool destinations;
`bootstrap/_scaffold/install.py` Write E copies onboarding guides from `docs/`.
`bootstrap/_scaffold/upgrade.py` retains recorded destinations and reads historical
templates by recorded source path. Cairn's lock says 0.3.0/`unknown`, includes
unrecoverable bases and omits `tools/code_map.py`. `scripts/repin.py` freezes
exact paths and module names before import; renames alone cannot preserve trust.

## Proposal

One plan, eleven items, delivered in v0.8:

1. **Root discovery before moves.** Give tests one shared repository-root helper, then move
   `bootstrap/tests/` to `tests/`; fix installed command/configuration root
   discovery too, including `content_scan_runner.py`.
2. **Release machinery → `release/`**: re-anchor/AST runbooks, `reanchor.sh`,
   launcher/values files, `repin.py`, `reanchor_ceremony.py` and both release
   checks. The plan lists every destination.
3. **`bootstrap/` → `install/`.** It keeps the installer, `BOOTSTRAP.md`,
   `SAFETY.md`, `verify_integrity.py`, `UPGRADE.md`, `profiles/` and `prompts/`,
   and gains `templates/phase-0/`, the readiness report, and root `dimensions/`
   and `on-ramp/`.
4. **`templates/` holds exactly what the installer reads**: the two onboarding
   guides move in; the pre-install files move out (item 3).
5. **Cairn-only scripts → `tests/` or `release/`.** Test tooling and reporting
   tools go to `tests/`, with `audit_report` beside `gauge`, which it loads.
6. **Layout test**: every file in `dev/tools/` is an install destination, no root
   `scripts/` or `tools/` exists, every installer source is under `templates/`,
   and everything under `templates/` is read by the installer.
7. **Citations to Cairn's source**: extend the citation rule so `cairn/…` always
   means Cairn's source; rewrite bare citations of `bootstrap/` files; run the
   link checker on a test install.
8. **Folder roles written once** in `docs/DOCUMENTATION_PLAN.md`, linked from
   `README.md`.
9. **`case-studies/` → `docs/case-studies/`**, with the vendor-neutrality
   exemption in `quality_gate.py` and the allowance in `check_cairn.py` moved to
   that exact path, not widened to `docs/`.
10. **Installed tools → one flat `dev/tools/`.** Move all 46 destinations, keeping module
    docs in `dev/modules/`. Both `AGENTS.md` and folder-role documentation define
    `dev/` as records, state and tools, not deliberation alone.
11. **Installer-driven self-adoption.** Cairn's real upgrade performs item 10
    first, producing installed files through the adopter migration; its profile
    excludes modules it does not self-host.

**Destination migration, not retirement.** Use explicit old/new source and
destination mappings with unique ownership. Move proven unchanged tracked files;
carry local executable forks unchanged and marked as forks; merge modified prose
only against a verified base. Preserve installed hashes separately from upstream
base hashes and migrate cache references. Unprovable files stay untouched with
named reconciliation instructions. Occupied destinations, conflicting ownership,
links or non-files refuse without overwrite or traversal. Unrelated adopter
files in root tool folders stay; only Cairn's own root folders disappear.

Stage bytes, provenance and lock/cache changes together; recheck inputs before
apply. Retain old bytes until destination verification and recoverable transaction
state are durable. Interrupted retries recognize completed steps by recorded
bytes, refuse changed inputs, and never delete the only copy. Report retained old
paths and require reconciliation before declaring migration complete.

**Self-lock prerequisite.** Inventory every selected installed file, including
unlisted copies. Recover bases from actual source commits/blobs or verified
caches with rendering inputs; record provenance and local adaptations through
tool-generated reconciliation, not guessed hashes or a fresh-install overwrite.
Unrecoverable ancestry stays unknown: preserve bytes and stop the affected move.
Reconciliation explicitly compares the local copy to an identified upstream
revision, preserving adaptations as a fork rather than inventing a historical
base. Any required trust acceptance remains the Maintainer's, never an inferred
permission. No blanket integrity bypass or automatic blessing.

**Compatibility.** Update hooks and shipped paths; `bootstrap/scaffold.py` only
errors with the new `python install/scaffold.py` command until v1.0. Resolve
historical sources by revision-specific mappings, not today's path. Cover moved
onboarding guides separately: Write E is outside the normal template lock loop;
preserve existing copies and never infer their ancestry from a new template.

**Queued outcome, separate proposal.** Ship `token_budget.py` in the
`documentation-plan` module and `verify_counts.py` with an empty registry in
`claim-check`, each with its doctrine paragraph; hold `audit_report.py`, the
slimmed replacement for the `lifecycle-metrics` module retired at `6558f3ff`.
Revival: after this plan lands, so they install straight into `dev/tools/`.

**Pending Maintainer choices.** Recommend keeping `dev/architecture_review.md`
and `dev/ceremony-record.md` where they are. Moving the former to
`dev/measurement/` mixes living reference with process evidence; moving the
latter to `dev/.cairn/` changes committed-record ceremony checks. Keeping them
costs no migration but retains the placement exceptions; moving adds mapping,
reference and verification work of uncertain duration, zero recurring operations.
Neither choice removes an outcome; no move is authorized here.

**Authority and sequence.** Root fixes; reviewed mapping and provenance recovery;
moves/references; real self-upgrade; verification and fresh AST baseline. Preserve
the old anchor's verifier and interpreter binding while preparing the new layout.
Verify exact candidate bytes, paths and import roster before any candidate import;
no candidate may authorize its own loader. The reviewed transition must establish
this chain or stop for a named Maintainer risk decision, not invent permission.
The Maintainer alone authorizes exact new authority and re-anchors, as a separate
owned/evidenced board wait, never a plan-closure task. An awaiting anchor remains
unpassed and cannot activate/release; defects or missing checks remain plan work.
Start v0.8 without competing plans; estimate remains two to four sessions,
uncertain until provenance recovery.

## Rationale

One layout/self-adoption objective avoids repeated migrations; behavior and
authority preservation are acceptance conditions, not consequences of renaming.

## Alternatives considered

Do nothing avoids migration but retains misleading folders and duplicate upkeep.
Moving only sources/citations loses the self-contained footprint; rejected without
conceding scope. Root `tools/` remains an adopter namespace collision.

## Documentation / doctrine surface

Prescription: both `AGENTS.md` files (certification command path, `dev/` role,
citation rule). Description: `docs/DOCUMENTATION_PLAN.md` folder roles,
`README.md`, `install/UPGRADE.md`. Deliberation: this proposal and its plan.
Shipped module docs and skills change paths only.
Retain every agent duty in its installed authoritative home, not source-only docs.

## Evidence / verification plan

### Tests required

Through scaffold install/upgrade: fresh install, v0.7 migration and Cairn's real
self-upgrade; unchanged, forked, unprovable, occupied/linked and interrupted/retry
cases, checking bytes, ownership, lock/cache provenance and stale-command absence.
Exercise historical reads across source moves and installed entry points against
misleading nested roots. Layout mutations must fail item 6. Authorized clean
before/after certification compares pass/skip/node counts; counts alone prove
neither behavior nor authority. Ceremony entry points must reject substituted
helpers, unauthorized candidate code and wrong interpreters before import.

### Examples / smoke checks

Scaffold summary/dry-run, both example self-tests, prose gates at their new
paths, and the link checker on a test install. These are future checks, not run.

#### Security preflight — five questions, answered in writing

- **S1.** Committed mappings define ownership; lock claims alone confer no trust.
- **S2.** Mutation and refusal cases above test plausible damage; not yet run.
- **S3.** Plan verification runs migration/ceremony checks; certification runs layout checks.
- **S4.** Wrong roots can silently select real files; item 1 covers commands too.
- **S5.** Audit every text-only assumption about `dev/`; retain integrity and containment checks.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Lost edits, competing commands after declared completion, altered test counts,
or executing candidate authority before verification falsifies this design.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance

Proposed paths:
- `dev/tools/`
- `docs/case-studies/`

## Review -- Terra -- 2026-11-12

Reviewed commit: be015399831b62898f10696191cd60b1b325a6c1

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

The strongest case is a recognizable, self-contained install, with Cairn's
own upgrade exercising the same migration adopters use.

**Foundations**

1. **Should this happen as framed?** Not yet: the transition needs to account for preserved local copies and Cairn's stale lock before promising one clean migration. -- `bootstrap/_scaffold/upgrade.py` `_classify_retired_records`; `dev/.cairn/cairn-lock.yml`.
2. **Best alternative.** Move installer sources and repair citations first while retaining the existing tool destinations; this loses the single `dev/tools/` footprint but avoids forcing the tool migration now. -- Proposal items 4, 7 and 10.
3. **What would show it wrong?** A real upgrade with a modified old tool or stale lock that loses the modification, silently leaves competing commands, or cannot complete falsifies the migration promise. -- `bootstrap/_scaffold/upgrade.py` `_cmd_remove_retired`.

1. **Blocking: define the adopter migration for modified and unprovable files.** Retirement currently removes only known unchanged copies and keeps others; the proposal both promises retirement and treats both copies remaining as failure. Specify how users find, reconcile and safely remove retained copies, and test unchanged, modified and unprovable cases through upgrade, including interrupted reruns. -- `bootstrap/_scaffold/upgrade.py` `_classify_retired_records`, `_cmd_remove_retired`.
2. **Blocking: establish the self-upgrade prerequisite.** Cairn's lock says 0.3.0 and unknown commit, and has unrecoverable bases; item 11 does not explain how the first real upgrade preserves local adaptations or handles files missing from the lock. Specify a verified reconciliation and a real self-upgrade check before relying on it. -- `dev/.cairn/cairn-lock.yml`.
3. **Non-blocking: reconcile the historical-read claim.** Keeping the `templates/` directory does not keep moved source paths stable: `_theirs_text` reads the lock's `src` at the requested revision. Explain compatibility for moved onboarding sources and historical revisions, or demonstrate those files are outside that contract. -- `bootstrap/_scaffold/upgrade.py` `_theirs_text`; `bootstrap/_scaffold/install.py` Write E.

**Audience and rule loss:** The summary communicates the goal, but the migration
needs the user-facing distinction in finding 1. No rule loss established from
the proposed prose; actual rewritten installed instructions were not available.

**Coverage:** Read the committed proposal, template, upgrade retirement and
historical reads, onboarding source and lock header; opening is 1,649 words
including headings, above the 1,000-word target. Did not independently recount
all historical figures, run an install, mutation, suite or security review.

## Security Review -- Sol -- 2026-11-12

Reviewed commit: be015399831b62898f10696191cd60b1b325a6c1

**Tier**: Security Review
**Model basis**: Sol High, explicitly assigned by the Maintainer through the coordinator.
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: initial read/probes approximately 7 minutes; recording/checks unknown.
**Tokens**: unknown

One-purpose folders and installer-driven self-adoption would reduce duplicate
maintenance while making Cairn easier to inspect.

**Foundations**

1. **Should this happen as framed?** Yes, with explicit migration and authority preservation: upgrade currently retains recorded destinations. -- `bootstrap/_scaffold/upgrade.py:802`.
2. **Best alternative.** Keep the proposed layout, but specify destination migration rather than retirement plus installation; retirement requires the template to disappear. -- `bootstrap/_scaffold/upgrade.py:663`.
3. **What would show it wrong?** A relocated executable selecting the wrong repository falsifies behavior preservation: executing committed root-selection statements with old/new paths produced `/tmp/adopter` versus `/tmp/adopter/dev`. -- `scripts/content_scan_runner.py:83`.

1. **Blocking: preserve migration ownership and local edits.** Upgrade uses old `dst` and suppresses new core-like destinations for already-tracked sources (`bootstrap/_scaffold/upgrade.py:802`, `bootstrap/_scaffold/upgrade.py:987`). Retained templates cannot qualify for retirement. **Closure:** specify ownership, fork, merge-base and hash migration; require data-preserving refusal for occupied/linked destinations and safe interrupted reruns.
2. **Blocking: define the anchored authority transition.** Pure renames change exact frozen paths and module names checked before imports (`scripts/repin.py:635`, `scripts/repin.py:701`). Equal counts cannot establish equivalent authority. **Closure:** require an old-anchor-to-new-layout transition preserving verify-before-import, interpreter binding and Maintainer authorization, with rejection probes for substituted helpers and unauthorized candidate code.
3. **Non-blocking: root authority extends beyond tests.** Item 1 addresses tests, but the scanner probe selects `dev` after relocation. **Closure:** include installed executable/configuration root discovery and exercise installed entry points against misleading nested roots.

**Audience / rule loss:** The summary is understandable. Preserve duties in
installed authoritative instructions; source-only folder-role documentation
cannot replace them. Rewritten instructions were unavailable.

**Coverage:** I read committed rules/template, migration, integrity and anchored
loader code; confirmed 71 lock records and absent `code_map`. No full historical
recount, migration, ceremony or suite run. Session orientation failed repository
detection. This over-target record retains security closure evidence. This is
the previously reported first pass, recorded after ordinary review serialization.

## Response -- Sol -- 2026-11-12

**Role/model**: revising proposal author, Sol High (Maintainer-assigned).
**Disposition**: awaiting-decision; all eleven v0.8 outcomes retained as one
layout/self-adoption objective. No plan or implementation opened.
**Elapsed**: unknown. **Tokens**: unknown.

1. **Terra 1 / Security 1:** Replaced retirement with destination migration:
   explicit ownership, unchanged copies, preserved executable forks, verified
   prose bases, separate installed/base hashes, occupied/linked refusal and
   recoverable interrupted retries. Retained paths are reported, not success.
2. **Terra 2:** Added self-lock reconciliation before self-upgrade, including
   unlisted files. Actual commit/blob/cache provenance is required; unknown
   ancestry stays unknown. Local comparisons cannot manufacture a clean base
   or authorize trust acceptance.
3. **Terra 3:** Corrected historical-read compatibility: revision-specific
   source mappings and separate preservation for Write E onboarding copies,
   which the normal template lock loop does not cover.
4. **Security 2:** Added old-anchor-to-new-layout verification before candidate
   imports, interpreter/roster preservation and rejection evidence. Maintainer
   re-anchor stays a separate wait, not plan closure or automatic activation.
5. **Security 3 / audience:** Included installed command/configuration roots
   and misleading-root checks; installed instructions retain authoritative duties.

### Withdrawn / superseded commitments

Withdrawn: retirement suffices; unchanged template root guarantees historical
reads; renames/count equality establish behavior or authority preservation.
No outcome or safeguard withdrawn. I reject the smaller sources-only alternative
because it loses the agreed footprint. Pending Decisions: proposal acceptance
and the two named placement choices (recommend retain both paths). No current
risk waiver is requested or granted; unrecoverable provenance or a broken
authority chain must stop for a specific Maintainer decision if encountered.

**Coverage:** I read both reviews, migration/lock generation, historical reads,
scanner roots and anchored loader. Isolated claim/link/snippet/neutrality gates
passed (Python 3.13.13); the mapper selected zero tests. Reader/pin search found
no proposal-path matches, with a known-positive lock-path control. Opening exceeds
1,000 words for finding-required safeguards. Migration, ceremony, certification
and suite were not run. Read/revision/check elapsed and tokens: unknown.

## Decision -- Maintainer (scribed by Antigravity Gemini 4 Hydrogen) -- 2026-11-12

**Tier**: heavy

**ACCEPTED.**

> "Accept all four as revised, retaining core meter installation for v0.7"

This accepts the v0.8 repository layout and self-adoption proposal as revised in `68abed30` (destination migration, self-lock reconciliation, and old-anchor-to-new-layout verification). Implementation opens at the start of v0.8 with no plans in flight; new recurring human operations: zero (shares the single v0.8 release re-anchor).

**Elapsed:** under 1 minute. **Tokens:** unknown.
