<!-- The paths below appear inside the appended Internal review: illustrative/deliberately-absent example paths, adopter-tree install destinations quoted from a manifest row, and multi-part line citations on real files. Marked, not edited -- reviewer prose is append-only. -->
<!-- claim-check-allow: scripts/run_security_audit.py*, dev/plans/adopter-licensing-compliance.md* -->
<!-- The path below is a forward-reference test file this proposal would create; it materializes in the implementing plan. -->
<!-- claim-check-allow: bootstrap/tests/test_lockfile_provenance.py -->
<!-- cairn-internal-ref-allow: doctrine/rationale.md doctrine/runtime-contract.md doctrine/proposals.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Lockfile provenance fields: make the install receipt say where it came from and under what licenses — without bumping the schema

**Author**: Claude (Strategy)
**Model**: Claude Opus 4.8
**Date opened**: 2026-07-22
**Status**: revised
**Touches**: `bootstrap/_scaffold/lockfile.py` (one new `_cairn_provenance` reader beside `_cairn_version` at `bootstrap/_scaffold/lockfile.py:103`, plus a schema-evolution rule on `_LOCK_SCHEMA` at `bootstrap/_scaffold/lockfile.py:42`); the install lock dict in `bootstrap/_scaffold/install.py:1584`; the two upgrade-side lock writers in `bootstrap/_scaffold/upgrade.py` (`_cmd_init_lock` at `bootstrap/_scaffold/upgrade.py:1111`, `_apply_upgrade` at `bootstrap/_scaffold/upgrade.py:1781`); the engine facade re-export block in `bootstrap/_scaffold/__init__.py:282`; a short "what the lockfile records" subsection in `bootstrap/UPGRADE.md`; a new `bootstrap/tests/test_lockfile_provenance.py`. **Explicitly out of scope:** any `_LOCK_SCHEMA` bump, any validate-on-read behavior in `read_lockfile` (`bootstrap/_scaffold/lockfile.py:193`), and any `creator` / author field.
**Related**: split out of the ACCEPTED `2026-07-11-claude-adopter-licensing-compliance` (its P3; both review tiers independently called the split — Internal R4 and External E3). Motivation traces to the broad-look review's Theme 4 receipt-provenance sentences, `dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md:300-302`. Triage triggers: the "Bootstrap fidelity / install contract … the lockfile schema" trigger at `dev/proposals/_template.md:58-61`, and the "install contract … byte-level stable" high-risk surface at `AGENTS.md:310-312`.
**Plan review**: required(Internal) — it edits four engine functions under `bootstrap/_scaffold/` and changes the bytes every newly-written lockfile carries, so the Internal floor (a fresh-context read) applies; an External (cross-type) read is **recommended** before the Decision because the surface is the byte-level-stable install contract and the load-bearing judgment is a compatibility argument, not a test result. Ratified at Decision.

## Context

The install lockfile is the machine record of an adoption. It answers
"which files, from which sources, at which hashes, under which profile,
with which tokens" — the dict written at
`bootstrap/_scaffold/install.py:1584` carries `schema`, `cairn_version`,
`cairn_commit`, `profile`, `modules`, `optional_templates`, `tokens`,
`files`. `bootstrap/PROVENANCE.md:72-83` names exactly this the
**install-side** half of provenance: "*which Cairn this tree actually
got*".

It does not answer **where that Cairn came from**, or **under what
terms**. The broad-look review put it plainly
(`dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md:300-302`):

> The install receipt records file fingerprints but not who made the
> files, under what license, or where they came from — and in our own
> installation, the "which version of Cairn" field just says "unknown."

The last clause reproduces: Cairn's own lockfile reads `cairn_commit:
"unknown"` at `dev/.cairn/cairn-lock.yml:4` (it is a `migrated: true`
record synthesized by `upgrade --init-lock`, carrying 81 file records,
as_of 2026-07-22). So the *one* field that could point at a specific
upstream is already degraded in the reference tree, and there is no URL
anywhere in the record to fall back to.

This proposal was **split out** of the accepted
`2026-07-11-claude-adopter-licensing-compliance` at both review tiers'
insistence, on the ground that it is a different risk class *and a
different purpose* from that proposal's legal-compliance package: the
accepted sibling installs a root `NOTICE.md` and self-propagating SPDX
headers, which is what MIT notice-retention and CC-BY attribution
actually require. **Neither license requires a lockfile field.** This
proposal is about *traceability* — making the machine record
self-describing — not compliance. The Maintainer's Decision (2026-07-22)
recorded the hand-off verbatim:

> **Split out (not accepted here): P3** — the lockfile
> `source_repository` + `licenses` fields. Both review tiers
> independently reached this split: P3 alters the byte-level-stable
> install contract (`_LOCK_SCHEMA`), a different risk class from legal
> compliance, and a routine compliance fix should not wait on a
> schema-bump deliberation. P3 opens as its own install-contract
> proposal.

The Revised proposal added one binding detail the Decision adopts by
reference: the split-out proposal "owns the `_LOCK_SCHEMA`-bump-vs-additive
decision (`lockfile.py:42`) and the manifest/fidelity re-anchor" — which
is what the rest of this document does.

Two facts about the current schema make the "additive vs. bump"
question sharper than it looks, and both were verified this session:

* **`_LOCK_SCHEMA` is write-only.** It is defined at
  `bootstrap/_scaffold/lockfile.py:42` (`= 1`) and written at
  `bootstrap/_scaffold/install.py:1585` and
  `bootstrap/_scaffold/upgrade.py:1197`. Grepping the tree for a read of
  the lockfile's `schema` key returns **none** (as_of 2026-07-22); the
  only `["schema"]` assertions in the suite are
  `bootstrap/tests/test_gate_manifest.py:37` and
  `bootstrap/tests/test_oracle.py:127`, which are the *gate-manifest*
  and *oracle-report* schemas, not the lockfile's.
* **`read_lockfile` does not validate.** It strips `#` lines,
  `json.loads`, and returns the object if it is a dict
  (`bootstrap/_scaffold/lockfile.py:193-210`) — no shape check, no
  version check. Forward-compatibility today is entirely ad-hoc `.get()`
  fallbacks at the call sites (`bootstrap/_scaffold/upgrade.py:632-633`,
  `bootstrap/_scaffold/upgrade.py:901-902`,
  `bootstrap/verify_integrity.py:53`).

So a schema *number* currently communicates nothing to any code. That
is the fact the compatibility argument below turns on.

## Proposed paths

Proposed paths:
- `bootstrap/tests/test_lockfile_provenance.py` — the new behavioral test for the two fields (writer, degradation, upgrade backfill, unknown-key round-trip); materializes in the implementing plan.

## Proposal

### P1 — one CITATION.cff reader

Add a single new helper to `bootstrap/_scaffold/lockfile.py`, beside its
siblings `_cairn_version` (`bootstrap/_scaffold/lockfile.py:103`) and
`_cairn_commit` (`bootstrap/_scaffold/lockfile.py:114`):

```python
def _cairn_provenance(cairn_root: Path) -> tuple[str, list[str]]:
    """Source repository URL + declared SPDX license ids, read from
    ``CITATION.cff``.  Degrades to ``("unknown", [])`` (absent / unreadable /
    key missing), matching ``_cairn_version``'s sentinel discipline."""
```

* `source_repository` comes from `repository-code:` (`CITATION.cff:18`).
* `licenses` comes from the `license:` block (`CITATION.cff:19-21`,
  which lists `CC-BY-4.0` and `MIT`).

**One helper, not two**, so `CITATION.cff` is read once and the AST
delta is one new symbol rather than two. `_cairn_version` is left
untouched — refactoring it to share the read would mutate a symbol
`bootstrap/_scaffold/upgrade.py` depends on, for no behavioral gain.

Line-scanner parsing, standard library only, in keeping with the
stdlib-only runtime contract (`doctrine/runtime-contract.md:177-179`:
"Cairn's scaffold engine is **stdlib-only by default** — no third-party
packages are required to run `bootstrap/scaffold.py install` or
`upgrade`.").

### P2 — the two fields, at all three lock writers

Add `source_repository` (str) and `licenses` (list of str) to:

* the fresh-install lock dict, `bootstrap/_scaffold/install.py:1584`;
* the synthesized migration lock in `_cmd_init_lock`,
  `bootstrap/_scaffold/upgrade.py:1197`;
* the advanced lock in `_apply_upgrade`, beside the existing
  version/commit advance at `bootstrap/_scaffold/upgrade.py:1944-1945`.

The third is the **backfill**, and it is deliberate. `--apply` already
re-sources `cairn_version` / `cairn_commit` from the Cairn being
upgraded to; the provenance fields describe the same thing (which Cairn
this tree now tracks), so sourcing them the same way is symmetric.
Without it, every tree installed before this lands stays permanently
provenance-free — which would make the fields nearly worthless for the
adopters who already exist.

### P3 — no `_LOCK_SCHEMA` bump; write the compat rule down instead

**`_LOCK_SCHEMA` stays `1`.** The argument, in full:

* **Additive-optional fields are already compatible in both
  directions, empirically.** A *new* engine reading an *old* lockfile
  finds the keys absent; nothing reads them, and every existing consumer
  already uses `.get()`. An *old* engine reading a *new* lockfile parses
  it (`json.loads` accepts unknown keys), ignores the extras
  (`bootstrap/verify_integrity.py:53` reads only `files`), and — at the
  current `--apply` implementation — *preserves* them, because the
  advanced lock is built as `new_lock = dict(lock)`
  (`bootstrap/_scaffold/upgrade.py:1943`). Unknown top-level keys
  survive an upgrade round-trip rather than being silently dropped.
* **A bump would spend the only discriminator we have on a
  non-breaking change.** `_LOCK_SCHEMA` is a single integer with no
  minor component. The first validator anyone writes will be
  fail-closed on `schema > known`. If provenance is `schema: 2`, that
  validator makes an older engine *refuse* a lockfile it can in fact
  read perfectly — the bump would **manufacture** the incompatibility it
  claims to signal. For a purely additive field, the presence or absence
  of the field is already a complete discriminator; the version number
  adds nothing and costs the increment.
* **What the contract is actually missing is the rule, not the
  number.** `AGENTS.md:310-312` names the lockfile schema as
  byte-level-stable, but nothing anywhere states *what* stability means
  for it. This proposal writes it down, in two places:
  * a docstring block on `_LOCK_SCHEMA`
    (`bootstrap/_scaffold/lockfile.py:42`): an additive **optional**
    top-level field does **not** bump `schema`; readers must use `.get()`
    with a default and must tolerate unknown keys; a **removal, rename,
    or change of meaning** of an existing field **does** bump, and a bump
    is the point at which a reader-side validator becomes mandatory;
  * a short "what the lockfile records" subsection in
    `bootstrap/UPGRADE.md` enumerating the top-level fields (it currently
    documents the lockfile's role but never its field set), carrying the
    same rule in adopter language.

### P4 — validate-on-read: deliberately deferred, and why

The write-only schema is a real unenforced contract, and this proposal
**does not fix it**. That is a choice, not an oversight:

* **`read_lockfile` is a trust anchor.** Its own module docstring says
  so — `bootstrap/_scaffold/lockfile.py:3`: "The install lockfile is the
  second trust anchor". `bootstrap/verify_integrity.py:47-52` **fails
  closed** on an unparseable lockfile. Teaching that reader to *reject*
  a lockfile on a version predicate is a fail-closed behavior change on
  the path an adopter's `upgrade` and `verify_integrity` both traverse;
  get the predicate wrong and a working tree stops upgrading. That is a
  different risk class — plausibly a Security-Review trigger — and it is
  exactly the "contract change married to a smaller change" bundling
  that produced *this* proposal in the first place.
* **Under the no-bump decision there is nothing to mismatch.** A
  validator here would guard against a version skew this change does not
  create. Adding it would be solving a problem this proposal does not
  have, on the most safety-critical reader in the engine.
* **It gets a durable home, not a shrug.** The deferred item — "validate
  `schema` on read, with a migration hint, and decide the fail-open /
  fail-closed disposition" — goes to a `dev/PLANNING.md` deferred-row at
  Decision, to be revived as its own proposal. Naming it here is the
  point: the reviewer should push on this if they disagree.

### P5 — Cairn's own lockfile is not backfilled

`dev/.cairn/cairn-lock.yml` is not hand-edited (its own header declares
it "tool-owned; regenerate-only; do not hand-edit") and it is a
`migrated: true` record. Regenerating it means re-running `upgrade
--init-lock --target .`, which rewrites all 81 file records (as_of
2026-07-22) — a whole-file churn with its own review surface, for two
keys. Worse, it would **not** fix the symptom the broad-look actually
named: `_manifest_cairn_commit`
(`bootstrap/_scaffold/upgrade.py:998-1012`) recovers `cairn_commit` from
a fidelity manifest, and `dev/.cairn/` contains no fidelity manifest
(as_of 2026-07-22 its members are `agent-identities.json`,
`cairn-lock.yml`, `cairn_foldback.md`, `local-env.json`,
`model-selection-mapping.yml`, `onboarding-activated.jsonl`,
`profile.yml`), so a re-init would still write `cairn_commit:
"unknown"`.

So: **leave it**. Cairn's own record gains the fields at its next
re-init or re-install. The `cairn_commit: "unknown"` symptom is a
separate defect with a separate cause, and this proposal does not claim
to fix it. Surfaced as an open question below in case the Maintainer
wants the regeneration bundled anyway.

### Documentation / doctrine surface

* **No `doctrine/` file changes.** Nothing under `doctrine/` is edited,
  added, or removed.
* **Descriptive layer** — the `bootstrap/UPGRADE.md` subsection (P3) is
  a description of the software as it is, which per the doc-tier home
  rule (`docs/DOCUMENTATION_PLAN.md`) routes to the descriptive layer,
  not to `AGENTS.md` and not to `doctrine/`.
* **Governing layer — untouched.** `AGENTS.md:310-312` already names the
  lockfile schema a byte-level-stable install contract. This proposal
  does not amend that sentence; it supplies the missing operational
  definition *below* it, in the module and the adopter doc. If the
  Maintainer would rather the additive-vs-breaking rule live in
  `AGENTS.md`, that is a routing call worth making at Decision — flagged
  as an open question, not decided here.
* **`bootstrap/fidelity-check.md` — deliberately untouched.**
  `bootstrap/fidelity-check.md:66-77` establishes the one-way relation:
  the lockfile is the machine authority, and the manifest "**cites** the
  lockfile's `cairn_version` / `cairn_commit` rather than re-listing the
  file/module inventory the lockfile already owns." Putting provenance
  in the lockfile *only* is the behavior that doctrine already
  prescribes; duplicating it into the manifest would create the second
  parsed inventory that section exists to prevent.
* **No vendor-neutrality impact.** The added values are a repository URL
  and SPDX license identifiers — no AI model or vendor name — so the
  `scripts/quality_gate.py --sub neutrality` surface is untouched.

### Doctrine-change rate-limit (if this proposal changes doctrine)

**N/A — this proposal changes no `doctrine/` rule, process, or
contract.** The doctrine-evolution gate at `doctrine/rationale.md:323-347`
governs changes to doctrine under `doctrine/`; none are made here.

I make **no high-risk claim** under that gate. Its bypass is exhaustive
to two surfaces — a security surface and a data-loss surface
(`doctrine/rationale.md:339-344`) — and this is neither: no
vulnerability is closed, no authentication path hardened, no
credential-leak vector removed, and no irrecoverable loss of work
prevented. `doctrine/rationale.md:346-347` is explicit:

> Any other "this feels urgent" framing falls outside the bypass and
> obeys the recurrence requirement.

The imminence of the first external adopter is precisely such a framing,
and I am not offering it as a bypass.

The install contract *is* a protected contract, but it is guarded by the
triage trigger at `dev/proposals/_template.md:58-61` and by review — the
gate being cleared by opening this proposal at all.

## Rationale

* **Which user workflow does it improve?** The adopter's "what is this
  tree, and where did it come from" question, answered from the tree
  itself. Today an adopter (or a reviewer, or a journal's
  reproducibility check) reading `dev/.cairn/cairn-lock.yml` sees a wall
  of per-file hashes (81 records in Cairn's own tree; the full published
  manifest is 94 data rows — both as_of 2026-07-22) and a version
  string, with no way to reach the upstream those files came from. After
  this, the receipt names the repository and
  the terms. That matters most in the case Cairn is built for: a
  research repo goes public alongside a paper, and someone downstream
  needs to trace the apparatus.
* **What stable contract or module boundary does it preserve or
  clarify?** It *clarifies* the one that was implicit. The lockfile
  schema has been "byte-level stable" per `AGENTS.md:310-312` with no
  stated meaning; P3 gives it an operational definition (additive =
  no bump; breaking = bump + validator) and puts it where a future
  author will find it. That is arguably worth more than the two fields.
* **What transparency / reproducibility does it improve?** Provenance
  is a reproducibility primitive: `bootstrap/PROVENANCE.md:72-83` already
  frames the lockfile as the install-side answer to "which Cairn is this
  tree?" — and a version number with no origin URL only half-answers it.
  Note the honest limit: this is **declared** provenance, not attested.
  `bootstrap/PROVENANCE.md:55-58` is explicit that Cairn's provenance
  posture is "named-releases + signed-tags + the derived manifest, which
  establishes origin without non-repudiation"; a `source_repository`
  read out of the source tree's own `CITATION.cff` inherits exactly that
  limit and no more.
* **Why now?** The parent proposal is accepted and its Decision
  explicitly re-opens this as its own proposal — leaving it unopened
  loses the split's point. And there is a real sequencing asymmetry: the
  fields are written at install / upgrade time, so an adopter who
  installs before this lands carries a provenance-free receipt until
  they upgrade. P2's `--apply` backfill is what keeps that from being
  permanent, which is itself a reason to land the two together rather
  than shipping fresh-install-only now and backfill later.

## Alternatives considered

1. **Do nothing.** Genuinely on the table: neither license *requires*
   this (the accepted sibling's `NOTICE.md` + SPDX headers fully
   discharge MIT notice-retention and CC-BY attribution), no test is
   red, and no adopter has reported the gap. The cost of doing nothing
   is narrow but real: the machine record stays unable to name its own
   upstream, and the human answer lives only in a prose file an adopter
   may delete or fork away from. Doing nothing is a defensible call and
   the Maintainer should feel free to make it — the proposal's honest
   claim is "cheap and correct," not "blocking."
2. **Additive fields *plus* a `_LOCK_SCHEMA` bump to 2.** Rejected on
   the argument in P3: with a single-integer version and no reader, the
   bump signals nothing today and mis-signals tomorrow, because the
   first fail-closed validator would reject a lockfile that is
   compatible. If a reviewer disagrees, this is the alternative to argue
   for — it is the conservative-looking choice, and I think it is the
   wrong one for a specific, stateable reason rather than a stylistic
   one.
3. **Additive + bump + validate-on-read, all in one.** Rejected as a
   bundle (P4): it marries a two-key addition to a fail-closed behavior
   change on the engine's second trust anchor — the exact bundling
   pattern that got this proposal split out of its parent.
4. **Put the provenance in the fidelity manifest instead.** Rejected:
   `bootstrap/fidelity-check.md:66-77` makes the manifest the *human*
   narrative that cites the lockfile, and the manifest is optional —
   Cairn's own `dev/.cairn/` has none (as_of 2026-07-22), which is
   precisely why its `cairn_commit` reads `"unknown"`. Putting
   machine-provenance in the optional human file inverts the documented
   relationship.
5. **Put it only in `NOTICE.md` (prose).** Rejected on two grounds. It
   is not machine-readable, so no tool can act on it. And it is
   *actively hazardous*: `bootstrap/tests/test_generated_output_scan.py`
   scans every generated `*.md` in an installed tree
   (`bootstrap/tests/test_generated_output_scan.py:48-55`) with an
   **empty** URL allowlist, and `content_scan`'s detector flags *any*
   non-allowlisted external URL
   (`templates/modules/team-gated/content_scan.py:285-290`). The
   lockfile is `dev/.cairn/cairn-lock.yml` — a `.yml`, not matched by
   that scan's `rglob("*.md")` — so a URL there is out of scope by
   construction. (This is a live hazard for the *sibling* proposal's
   `NOTICE.md`, which will carry a repo URL into an installed `.md`. I
   flag it as a cross-proposal signal; I have verified the scanner and
   the test, not the sibling's unwritten file.)
6. **Hardcode the URL and the license list in the engine.** Rejected:
   two sources of truth for a value `CITATION.cff` already holds, and
   `_cairn_version` already establishes the read-from-CITATION.cff
   pattern (`bootstrap/_scaffold/lockfile.py:103-111`).
7. **Also record `creator` / authors** — the third of the broad-look's
   three questions ("who made the files"). Declined for scope: the
   copyright holder is what a *legal* reader needs and the accepted
   sibling's `NOTICE.md` carries it; an author list drifts and is the
   one provenance value that is personal data. Named here so the
   omission is deliberate rather than silent.
8. **Fresh-install only — no `--apply` backfill.** Considered
   seriously (it is the smallest diff, and touches one engine function
   instead of three). Rejected because it leaves every already-installed
   tree permanently provenance-free and creates an asymmetry with
   `cairn_version` / `cairn_commit`, which `--apply` *does* advance
   (`bootstrap/_scaffold/upgrade.py:1944-1945`) — a reader would
   reasonably read that asymmetry as a bug.
9. **Name the field `source_licenses` rather than `licenses`.**
   Genuinely better as a contract (it would pair with
   `source_repository` and make plain that the value describes the
   *source Cairn*, not any individual installed file). Not adopted here
   because `licenses` is the field name the accepted parent proposal
   named and this is its split-out continuation; raised as an open
   question instead, since renaming is free *now* and expensive after
   one release ships.

No maintainer chat-mode preferences were incorporated into this draft.

## Evidence / verification plan

**Baseline, stated honestly.** `python -m pytest bootstrap/tests` on a
clean `master` is **3 failed, 1408 passed, 3 skipped (102s), as_of
2026-07-22**. The failures are pre-existing and this proposal does not
claim to leave the suite green:

* Two nodes in `bootstrap/tests/test_ast_attest.py` —
  `test_committed_baseline_accounted_for_across_the_engine_package` and
  `test_ast_gate_passes_over_the_full_scaffold_module_set` — the tracked
  stale-baseline issue. This is **not** a one-symbol drift: each failing
  node reports **133 CHANGED top-level symbols** across the engine
  package (as_of 2026-07-22), and `FunctionDef:write_install_lockfile`,
  `FunctionDef:_apply_upgrade`, and `FunctionDef:_cmd_init_lock` are
  *already* among them.
* One node in `bootstrap/tests/test_evolution_infer.py` —
  `TestGateEval::test_main_suggests_and_json` — the separately-tracked
  clock-dependent failure.

The plan records this before/after; the target is **no new failures**,
not "green."

**AST re-anchor — required, supervised, and it cannot use the surgical
path.** `bootstrap/_scaffold/` is engine code, so per `AGENTS.md:323-325`
this change re-anchors `bootstrap/tests/fixtures/scaffold_ast_baseline.json`
per `bootstrap/REANCHOR_RUNBOOK.md`. Concretely the delta is: one **new**
`FunctionDef:_cairn_provenance` key in `lockfile.py`; **CHANGED** digests
for `FunctionDef:write_install_lockfile`, `FunctionDef:_cmd_init_lock`,
and `FunctionDef:_apply_upgrade`; and **rotated `Import:` keys** in
`install.py`, `upgrade.py`, and `__init__.py` — imports are keyed by a
hash of their structural content
(`bootstrap/tests/_ast_attest.py:80-83`), so extending an import list
deletes one key and adds another rather than changing one in place.

The surgical `_ast_attest.py update-symbol` path is **not available**:
its allowlist (`bootstrap/tests/_ast_attest.py:141`) admits only
`_MODULE_MAPPINGS`, `_SKILLS_MAPPINGS`, `_CORE_MAPPINGS`, and
`install_onboarding`. So the full supervised flow applies — and
`bootstrap/REANCHOR_RUNBOOK.md:6-11` reserves Phase 0 and Phase 4 to the
Maintainer ("an implementing agent must not perform Phase 0 or Phase 4").
**Sequencing:** the accepted licensing proposal's plan already commits to
one supervised re-anchor (its P1 mutates `Assign:_CORE_MAPPINGS`). This
plan should land **after** that re-anchor, so it re-anchors from a fresh
baseline rather than contending with a 133-symbol stale one.

**Blast radius — checked, not assumed.**

* **`scaffold.py --manifest`: unchanged.** `format_manifest`
  (`bootstrap/_scaffold/install.py:1362`) emits only
  `destination<TAB>source<TAB>{verbatim|substituted}` rows; it never
  reads the lock dict. 94 data rows, as_of 2026-07-22, before and after.
* **`bootstrap/verify_integrity.py`: unchanged.** It reads only
  `lock.get("files")` (`bootstrap/verify_integrity.py:53`); unknown
  top-level keys are invisible to it.
* **The fidelity manifest: unchanged**, by design — see the
  documentation surface above.
* **The gate manifest: no HOLD from the engine edit.** Its frozen globs
  are `bootstrap/*.py` (non-recursive), `bootstrap/tests/**/*.py`,
  `bootstrap/tests/fixtures/**/*`, `scripts/*.py`,
  `templates/modules/**/*.py`
  (`bootstrap/tests/_gate_manifest.py:165-167`) — `bootstrap/_scaffold/*.py`
  is a subdirectory and is **not** matched. The new test file reads as
  `FROZEN-NEW` (allowed and recorded, `bootstrap/tests/_gate_manifest.py:366`),
  and `scaffold_ast_baseline.json` is declared cascade-mutable
  (`bootstrap/tests/_gate_manifest.py:80-81`).
* **The differential oracle: a diff is expected and must not be
  normalized away.** `bootstrap/tests/_oracle.py:94` normalizes exactly
  `cairn_version` and `cairn_commit` before byte-compare. If a baseline
  ref is ever configured across this change, the lockfile will report
  `bytes_differ` — which is **correct detection of a real behavior
  change**, not a false positive. The new fields must **not** be added
  to `_PROVENANCE_KEYS`; `bootstrap/tests/_oracle.py:31-33` explicitly
  rejects "A broad normalization that could hide a content diff."
  Separately, `bootstrap/_scaffold/` is on the oracle's
  `SENSITIVE_ROSTER` (`bootstrap/tests/_oracle_activation.py:37`), so
  this diff is classified sensitive; no activation artifact is present
  in `dev/.cairn/` (as_of 2026-07-22) and the acceptance check is not
  wired to a pytest node that evaluates the working tree, so nothing
  HOLDs automatically — the plan records the classification for the
  Maintainer rather than relying on a gate to raise it.
* **The content scanner: out of scope by file type**, per alternative 5.

### Author-accounting — invariants, failure modes, edge cases

**In scope: this is a protected-schema change**, so the block is filled.

**Invariants.**

| Invariant | Enforcer |
| --- | --- |
| `source_repository` is always a `str`; `"unknown"` when `CITATION.cff` is absent/unreadable/keyless | new degradation test (below) |
| `licenses` is always a `list[str]`, possibly empty — never a sentinel *string* inside a list field | new shape test |
| Unknown top-level keys survive an `upgrade --apply` round-trip | new round-trip test (today the behavior falls out of `new_lock = dict(lock)` at `bootstrap/_scaffold/upgrade.py:1943` and is **untested**) |
| A fresh install and an `--apply` produce the *same* provenance values for the same `cairn_root` | new install-vs-upgrade parity assertion |
| `_LOCK_SCHEMA` stays `1` for an additive change | **no enforcer** — this is the honest gap, and it is the deferred P4 item; today the rule lives only in a docstring a human must read |

**Failure modes.**

* `CITATION.cff` absent / unreadable → **open** (degrades to
  `("unknown", [])`). Intentional: it matches `_cairn_version` and
  `_cairn_commit`, both of which already degrade to `"unknown"`
  (`bootstrap/_scaffold/lockfile.py:103-124`), and Cairn's own lockfile
  already carries that sentinel at `dev/.cairn/cairn-lock.yml:4`. A
  provenance read must never be able to fail an install.
* `license:` block present but malformed → **open** (empty list).
  Intentional, same reason.
* The pre-existing lockfile-write refusal on a diverged tree
  (`bootstrap/_scaffold/install.py:1575-1582`) stays **closed** and is
  unchanged.

**Edge-case inventory.** Handled: no `CITATION.cff`; `repository-code`
absent; `license:` present-but-empty; a single license; a lockfile
written by a pre-provenance engine (fields absent); an unknown extra
top-level key. Out of scope: a *forked* Cairn whose `CITATION.cff` still
names upstream (the field is **declared**, not attested — see Rationale
and the signals below); a per-file license map; non-UTF-8
`CITATION.cff`.

**Public-path → test mapping.**

* `python bootstrap/scaffold.py --config … --target …` (fresh install →
  the two fields present and equal to `_cairn_provenance(CAIRN_ROOT)`) →
  `bootstrap/tests/test_lockfile_provenance.py` (forward-referenced;
  listed under *Proposed paths* and shown as a bare path so this
  document stays link-clean until the file exists).
* `python bootstrap/scaffold.py upgrade --apply --target …` (backfill of
  a pre-provenance lockfile; unknown-key preservation) → new nodes added
  to the existing
  [`bootstrap/tests/test_upgrade.py`](../../bootstrap/tests/test_upgrade.py),
  whose `_install` + delta harness already drives a real `--stage` /
  `--apply` cycle. The plan pins the exact node names; **no existing
  assertion is modified.**
* `python bootstrap/scaffold.py upgrade --init-lock --target …` →
  `bootstrap/tests/test_lockfile_provenance.py` (forward-referenced).

**Known omissions / intentionally untested edges.** No test asserts
`_LOCK_SCHEMA == 1` as a contract (that is P4's deferred job, and a test
pinning the constant would be a tautology, not an enforcement). No test
exercises a *genuinely old* engine binary against a new lockfile — the
old-engine direction is argued from the current source
(`bootstrap/_scaffold/upgrade.py:1943`,
`bootstrap/verify_integrity.py:53`), not demonstrated, and the
differential oracle is the only harness that could demonstrate it. That
is the weakest link in the compatibility argument and a reviewer should
press on it.

### Tests required

New file `bootstrap/tests/test_lockfile_provenance.py` (four behavioral
nodes: fresh-install writer, `("unknown", [])` degradation on a
`CITATION.cff`-less root, `--init-lock` synthesis, field shape); plus
new nodes appended to `bootstrap/tests/test_upgrade.py` for the
`--apply` backfill and the unknown-key round-trip. Both homes are the
engine suite (`python -m pytest bootstrap/tests`), stdlib + pytest only.

I have read the existing assertions that could plausibly collide and
they do not: `bootstrap/tests/test_lockfile_module.py:111-115` builds
its *own* two-key dict for the emit/read round-trip rather than reading
an installed lockfile, and
`bootstrap/tests/test_upgrade.py:1513` compares a lockfile to itself
after a *refused* finalize. Neither pins the writer's key set. No test
in `bootstrap/tests/` asserts an exact top-level key set for an
installed lockfile (as_of 2026-07-22).

### Examples / smoke checks

* `python bootstrap/scaffold.py --manifest` — must emit the same 94 data
  rows before and after (the manifest is field-independent; this is the
  cheap proof).
* `python bootstrap/scaffold.py --summary --config <profile>` and
  `--dry-run` — the no-write install paths still run clean.
* A real scratch install into a temp target, then `python
  bootstrap/verify_integrity.py --target <scratch>` — exit 0 with the
  new fields present (the trust anchor is indifferent to them).
* `python scripts/check_cairn.py` — the prose-integrity gate for the
  `bootstrap/UPGRADE.md` addition.
* **N/A**: the example gallery (`examples/minimal/`,
  `examples/scientific-minimal/`) — this change touches no shipped
  example.

## Open questions for the Maintainer

1. **Field name: `licenses` or `source_licenses`?** The parent proposal
   named `licenses`; `source_licenses` is the better contract
   (alternative 9). Free to change now.
2. **Does the additive-vs-breaking schema rule belong in `AGENTS.md`
   instead of the module docstring + `bootstrap/UPGRADE.md`?** It is
   arguably a cross-cutting prescription, which would route it to the
   governing layer.
3. **Should the deferred validate-on-read item get its
   `dev/PLANNING.md` deferred row at this Decision**, or wait?
4. **Backfill Cairn's own `dev/.cairn/cairn-lock.yml` via `upgrade
   --init-lock --target .`** (81 records rewritten, and `cairn_commit`
   stays `"unknown"` regardless), or leave it to a future re-init as P5
   recommends?

## Signals the change is wrong

* **Someone reads `licenses` as a per-file license.** It is the *source
  Cairn's* declared set (`CITATION.cff:19-21`), not a claim about any
  installed file — the brand mark's CC BY-ND is correctly absent because
  it is not installed (`python bootstrap/scaffold.py --manifest` returns
  zero `.svg` / `.png` / logo / brand rows, as_of 2026-07-22; the mark is
  `docs/assets/cairn-banner.svg` per `LICENSE-CC-BY-ND.md:26-27`).
  *Recovery:* rename to `source_licenses` (alternative 9) and tighten the
  `bootstrap/UPGRADE.md` wording. Cheap now; expensive after a release.
* **`source_repository` is trusted as attested origin.** It is read out
  of the source tree's own `CITATION.cff`, so a fork that did not update
  that file will report upstream. *Recovery:* the field is documented as
  *declared* provenance; the attestation story stays the source-side
  controls at `bootstrap/PROVENANCE.md:55-58`. If the field starts being
  cited as proof of origin, that is the signal to say so louder — or to
  drop it.
* **A future breaking schema change finds `schema: 1` uninformative**
  because two field generations share the number. *Recovery:* the
  written rule already says a breaking change bumps; the migration keys
  on field *presence* (`"source_repository" in lock`), which is exactly
  the discriminator P3 argues is sufficient. If that turns out to be
  awkward in practice, it falsifies P3's core claim and the bump should
  be taken then.
* **An old engine drops the fields on `--apply`** in some version I did
  not inspect. *Recovery:* this would break the "no bump needed"
  argument's forward half; the answer is P4's validator, promoted from
  deferred to required. This is the single observation most likely to
  overturn the proposal.
* **The suite gets worse than 3 failed / 1408 passed / 3 skipped** after
  the supervised re-anchor, or the re-anchor diff touches anything
  beyond the four function keys and the three `Import:` rotations named
  above. *Recovery:* revert — the change is one
  helper and two dict keys in three writers, so a revert is clean.
* **Nobody ever reads the fields.** Twelve months on, if no tool, doc,
  or adopter has consulted `source_repository` or `licenses`, the fields
  are inert weight on a protected contract. *Recovery:* they are additive
  and optional by construction, so removal is a schema *bump* away — an
  acknowledged asymmetry, and the strongest argument for alternative 1
  (do nothing).

## Review -- Claude (Internal, fresh-context subagent panel) -- 2026-07-22

**Model**: Claude Opus 4.8 (three fresh-context subagents on lenses tailored to this proposal's failure modes; no access to the authoring session; consolidated, none dropped).

**Attribution / committer note.** The panel's findings, transcribed faithfully — none softened, reordered to bury, or dropped. Per the binding practice from the superseded automated-review-committer Decision (2026-07-09), the raw panel source is committed in-tree at `dev/reviews/2026-07-22-lockfile-provenance-internal-panel.json`; committed under the Maintainer's git identity by the author-session as disclosed scribe.

**Steelman.** All three lenses independently found this proposal unusually well-evidenced, and two of them tried hard to break its central argument and could not.

Citation fidelity: every doctrine and code citation opened by any panelist was verbatim and in-bounds — `doctrine/rationale.md:339-347`, `doctrine/runtime-contract.md:177-179`, `doctrine/dual-review.md:30-49`, `bootstrap/REANCHOR_RUNBOOK.md:6-11`, `bootstrap/fidelity-check.md:66-77`, `bootstrap/PROVENANCE.md:55-58` and `:77-78`, `dev/proposals/_template.md:58-61`, `AGENTS.md:310-312` and `:323-325`, `LICENSE-CC-BY-ND.md:26-27` — and the parent Decision quote is verbatim at `dev/proposals/archive/2026-07-11-claude-adopter-licensing-compliance.md:631-635`. Only three edge-of-span slips were found in the whole document (R12).

The empirical claims reproduce. Two lenses independently ran `python -m pytest bootstrap/tests` and got the stated baseline exactly — 3 failed / 1408 passed / 3 skipped, same three node names — and one confirmed the "133 CHANGED per node" figure precisely (266 CHANGED lines across two nodes). `scaffold.py --manifest` emits 94 data rows today; Cairn's own lockfile parses to 81 file records, 9 top-level keys, `cairn_commit: "unknown"`; `dev/.cairn/` has 7 members and no fidelity manifest. The blast-radius sweep is checked rather than asserted: the gate-manifest globs, `_PROVENANCE_KEYS`, and the `.md`-only generated-output scan all hold as claimed.

P3's no-bump argument is correct and survived every attack mounted against it. No code anywhere reads the lockfile `schema` key (`_LOCK_SCHEMA` is written at `install.py:1585/1602` and `upgrade.py:1197/1207` and read nowhere); `read_lockfile` (`lockfile.py:193-210`) performs no shape or version validation; every consumer uses `.get()`; of 120 `read_lockfile` uses in tests only two compare whole dicts, both benign; and no test pins an exact top-level key set. "A bump would manufacture the incompatibility it claims to signal" is a genuinely good argument that no lens could break — and, as R3 records, it is better supported by the tree than the document itself claims.

The rate-limit section refuses the adopter-deadline framing outright, which is the correct call under `doctrine/rationale.md:346-347`. P4's deferral and alternatives 1 and 8 are honestly argued rather than shrugged. P5 correctly diagnoses that a re-init would still write `cairn_commit: "unknown"` — `_find_manifest_path` finds nothing in `dev/.cairn/` or `dev/strategy/`. The gate-manifest non-match (`bootstrap/*.py` is non-recursive), the FROZEN-NEW read, and the unavailability of a surgical baseline-update path are all correct. The defects below are localized — the mechanism description in P2, the plan's gate accounting, and one lifecycle-header tier — not structural.

**Critiques** (descending severity; each grounded in a command/citation the reviewer ran):

* **[R1] (blocking)** P2 mis-describes how `--apply` obtains provenance, and every implementation route it leaves open is unnamed. The proposal asserts `--apply` "already re-sources `cairn_version` / `cairn_commit` from the Cairn being upgraded to" and places the new fields "beside the existing version/commit advance at upgrade.py:1944-1945". Those two lines read `meta.get("new_version")` / `meta.get("new_commit")` — values captured at **--stage** time in `_compute_upgrade` (`"new_version": _cairn_version(cairn_root)` / `"new_commit": to_ref or _cairn_commit(cairn_root)`, upgrade.py:906-907), persisted to `dev/.cairn-upgrade/stage-metadata.json` (written at :932, `_STAGE_META` at :104), and re-read by `_apply_upgrade` at :1801-1806. `--apply` re-sources nothing and never receives `args.to` (:2249-2252). That leaves an unnamed fork: (a) call `_cairn_provenance(cairn_root)` live in `_apply_upgrade` (the `cairn_root` param exists at :1782) — which records the *working tree's* CITATION.cff rather than the ref the staged content came from, the exact asymmetry P2 claims to avoid and that alternative 8 says a reader would read as a bug, since `new_commit` already honours `to_ref`; or (b) source the values in `_write_stage` (:743, meta dict at :900) — a **fourth** engine function that Touches does not list and the AST re-anchor delta does not enumerate, and which makes `stage-metadata.json` a second cross-version compat surface. That surface is already treated as one in-tree: upgrade.py:920 reads `# Key name kept ``module_blocked`` for stage/apply compatibility`. A stage produced by an old engine and applied by a new one will carry no provenance keys in meta.
  *Grounding:* bootstrap/_scaffold/upgrade.py:906-907 (stage-time capture, `to_ref`-aware), :920 (stage/apply compat precedent), :932 (`json.dumps(meta)` written), :1782 (`_apply_upgrade` signature takes `cairn_root`), :1801-1806 (apply reads meta), :1944-1945 (`new_lock` reads `meta.get`), :2249-2252 (apply gets no `--to`)
  *Suggested fix:* Correct the sentence to "--apply copies version/commit from the staged metadata" and pick the fork explicitly in P2. Recommended route: source `source_repository` / `licenses` in `_write_stage` as `new_source_repository` / `new_licenses` in the meta dict (upgrade.py:900), and have `_apply_upgrade` read them with a `.get()` fallback to the current lock value so an old stage applied by a new engine degrades instead of writing nulls. Decide and state the ref-awareness question explicitly (working-tree CITATION.cff vs `git show <to_ref>:CITATION.cff`), since `new_commit` already honours `to_ref`. If the stage route is taken, add `FunctionDef:_write_stage` / `_compute_upgrade` to Touches and to the enumerated re-anchor delta (a 4th CHANGED FunctionDef), and name the old-stage/new-engine `.get()` default in the edge-case inventory.

* **[R2] (blocking)** The gate-manifest blast-radius bullet is wrong about the test plan. `bootstrap/tests/test_upgrade.py` is in the pinned frozen set of the committed gate manifest (147 frozen entries; the file is present), and it is not in `CASCADE_MUTABLE` or `PHASE_SPLIT_TARGETS`. Editing it produces `FROZEN-MODIFIED: ... (gate file edited — sha differs)`, which `_gate_manifest.py` appends to `holds`, not `notes`. The proposal plans exactly that edit ("new nodes added to the existing bootstrap/tests/test_upgrade.py") while asserting "The gate manifest: no HOLD from the engine edit" and citing only the FROZEN-NEW path for the new file. This is not hypothetical: the `PHASE_SPLIT_TARGETS` entry for `test_intents_tool.py` exists because a prior batch hit this exact wall — "That edits this gate file → the pre-run manifest froze it → a hard-stop the run cannot self-certify" — and required a supervised, Maintainer-authorized re-anchor.
  *Grounding:* bootstrap/tests/_gate_manifest.py:364 (FROZEN-MODIFIED appended to `holds`) vs :366 (FROZEN-NEW appended to `notes`); :165-167 frozen globs include `bootstrap/tests/**/*.py`; :93-101 the `test_intents_tool.py` precedent; `bootstrap/tests/test_upgrade.py` verified present in `frozen_files` of bootstrap/tests/fixtures/gate_manifest.json
  *Suggested fix:* Put the `--apply` backfill and unknown-key round-trip nodes in the NEW `bootstrap/tests/test_lockfile_provenance.py` (FROZEN-NEW, allowed and recorded) rather than appending to `test_upgrade.py`; the `_install` / delta harness can be imported or re-created there. If appending to `test_upgrade.py` is genuinely necessary, say so and sequence the gate-manifest re-anchor alongside the AST one in the same supervised Maintainer step.

* **[R3] (blocking)** P3's compatibility argument is argued from materially less in-tree evidence than the tree actually offers, in two ways a reviewer cannot check from the document. (a) **The lockfile writer inventory is undercounted — five writers, not three.** Beyond install.py:1602 and upgrade.py:1207 (`--init-lock`) and :1997 (`--apply`), the lockfile is also written by `_commit_adoption` / `_commit_lock_and_caches` (upgrade.py:1308, the `--adopt-module` / `--adopt-collisions` path, defined at :1255) and by `_cmd_finalize_lockfile` (upgrade.py:1709, defined at :1592). Both were read this session: each writes back the dict obtained from `read_lockfile` (upgrade.py:1352, :2173), so unknown keys ARE preserved — which strengthens P3 beyond what it claims — but the proposal rests the entire forward half on `new_lock = dict(lock)` at :1943 alone, so a reviewer cannot tell whether the other two were checked or missed. There is also a behavioral consequence the proposal misses: neither unlisted writer backfills, so an adopter whose only upgrade traffic is `--finalize` or `upgrade --adopt-module` never gains the fields — which qualifies P2's "keeps that from being permanent" and the stated invariant that a fresh install and an `--apply` agree. (b) **The strongest single precedent is omitted:** the lockfile already carries an optional top-level key that varies by writer at `schema: 1`. Cairn's own top-level key set is {cairn_commit, cairn_version, files, migrated, modules, optional_templates, profile, schema, tokens}; `migrated` is written only by `_cmd_init_lock` (upgrade.py:1197), is absent from every fresh install (install.py:1584-1593), and the only read anywhere is a test assertion (test_upgrade.py:797). That is a live, additive, writer-varying optional key coexisting with `schema: 1` — far more persuasive than the argument-from-absence P3 currently rests on, and its omission cuts the other way too: a reviewer who finds `migrated` independently may wonder whether the author swept the actual key set.
  *Grounding:* (a) grep `_emit_lock_yaml` across bootstrap/scripts/templates: install.py:1602, upgrade.py:1207, :1308 (`lock_tmp.write_text(_emit_lock_yaml(lock)...)` in `_commit_adoption`), :1709 (`(target / _LOCKFILE_REL).write_text(_emit_lock_yaml(lock)...)` in finalize), :1997; both unlisted sites operate on the dict from `read_lockfile` (upgrade.py:1352, :2173). (b) dev/.cairn/cairn-lock.yml parsed this session (9 top-level keys, 81 file records, migrated=True, cairn_commit="unknown"); bootstrap/_scaffold/upgrade.py:1197; bootstrap/tests/test_upgrade.py:797
  *Suggested fix:* Enumerate all five write sites in Touches and in P3's compatibility bullet with a construct-vs-copy classification (construct: install.py, `_cmd_init_lock`; copy/mutate: `_commit_lock_and_caches`, `_cmd_finalize_lockfile`, `_apply_upgrade`), stating that :1308 and :1709 round-trip the read dict verbatim — that is the strongest in-tree evidence for no-bump. State explicitly which writers backfill and which merely preserve, and either extend the backfill to `--finalize` or record the non-backfilling paths as a known limit. Add one cheap `--finalize` round-trip node to the unknown-key test so the invariant is enforced on more than one path. Separately, add a bullet citing `migrated` as the existing precedent, and note in the P3 rule text that `migrated` is the first instance of the rule being written down retroactively — making the rule a codification of existing practice rather than a new invention (which also softens R11a).

* **[R4] (blocking)** The declared plan-review tier is below the doctrinal floor for this surface. `doctrine/dual-review.md:184-187` reads: "that tier is chosen on the same structural-independence axis as any other review here — an Internal-floor read for an ordinary plan, a different-agent-type External round for a high-risk or contract-touching one." The proposal declares `required(Internal)` and demotes External to "recommended", while in the same sentence calling the surface "the byte-level-stable install contract" and citing the install-contract trigger (`dev/proposals/_template.md:58-61`, `AGENTS.md:310-312`). Contract-touching is exactly the case doctrine assigns an External round. `doctrine/dual-review.md:325-329` compounds this: "A declared-`required` tier stays a floor. Recommend-and-decide governs only the *optional escalation beyond* what the lifecycle already declared" — the recommend-and-decide instrument cannot be used to soften a tier downward.
  *Grounding:* doctrine/dual-review.md:184-187 and :325-329, read this session; cross-checked against the proposal's own surface claim vs AGENTS.md:310-312 and dev/proposals/_template.md:58-61
  *Suggested fix:* Change the header line to `Plan review: required(External cross-type); ratified at Decision`, and state the reason in one clause (contract-touching per dual-review.md:186-187). If the author wants to argue the surface is not "high-risk or contract-touching", that argument must be made explicitly against :186-187 — it cannot be left implicit while the body asserts the opposite.

* **[R5] (substantive)** P5's disposition — "Cairn's own record gains the fields at its next re-init or re-install" — names two paths that are both structurally blocked. `_cmd_init_lock` returns early with "[info] ... already exists; nothing to migrate" whenever `read_lockfile(target) is not None`, and `write_install_lockfile` refuses on a diverged tree (Cairn's tree is heavily diverged). So neither `--init-lock` nor a re-install will ever backfill `dev/.cairn/cairn-lock.yml`. The only real paths are a self-targeted `upgrade --stage/--apply` or a manual delete-then-init. As written, P5 promises an eventual fix that cannot occur, which weakens the "leave it" recommendation the Maintainer is being asked to ratify.
  *Grounding:* bootstrap/_scaffold/upgrade.py:1121-1122 (`if read_lockfile(target) is not None:` early return in `_cmd_init_lock`, which begins at :1111); bootstrap/_scaffold/install.py:1572-1582 (diverged-tree refusal, `return None`)
  *Suggested fix:* Restate P5 honestly: Cairn's own lockfile stays provenance-free until either a self-targeted `--apply` runs or the file is deleted and re-inited by hand. That makes open question 4 a real choice rather than a deferral to a trigger that never fires.

* **[R6] (substantive)** P3's "a docstring block on `_LOCK_SCHEMA` (lockfile.py:42)" is not implementable as written, and the ambiguity changes the AST delta. `_LOCK_SCHEMA = 1` is a module-level `Assign`; Python attaches no docstring to it. If the rule is written as a bare string literal after the assignment it becomes a new top-level `ast.Expr`, which `_ast_attest` keys as `"Docstring"` — and since `lockfile.py` already has a module docstring, `digest_module` suffixes it to `Docstring#2`, a NEW baseline key the proposal's enumerated delta (one new FunctionDef, three CHANGED FunctionDefs, three rotated `Import:` keys) does not list. The module's own convention for annotating a constant is the `#:` comment form used on `_LIVING_STATE_DSTS` immediately below, which is AST-invisible and triggers no delta. Left as written, the implementer can pick either and the enumerated re-anchor delta stops being a falsifiable check.
  *Grounding:* bootstrap/tests/_ast_attest.py:84-88 (bare string Expr → key `"Docstring"`), :97-107 / :103-105 (`seen` counter suffixes duplicates `#<n>`), :30-34 (`test_digest_is_position_and_comment_insensitive`); bootstrap/_scaffold/lockfile.py:42 (`_LOCK_SCHEMA = 1`) and :44/:45 onward (the `#:` comment convention)
  *Suggested fix:* Say "a `#:` comment block on `_LOCK_SCHEMA`", not "docstring" — AST-invisible, matches the file's own convention, and keeps the enumerated re-anchor delta exactly as stated. If a string literal is preferred for any reason, add `Docstring#2` in `lockfile.py` to the enumerated AST delta.

* **[R7] (substantive)** The verification plan does not state a falsifiable expected gate output, and slightly overstates how the AST gate reacts. Both failing nodes simply call `A.verify(_BASELINE, modules) == 0`. `verify` fails only on `problems`; `_classify` `continue`s over baseline entries of type Import/ImportFrom and over any `Docstring*` key, and NEW keys are printed as notes, never failures. So the new `FunctionDef:_cairn_provenance` and every rotated `Import:` key produce ZERO new gate failures; only the three CHANGED function digests move, and all three (`write_install_lockfile`, `_cmd_init_lock`, `_apply_upgrade`) are ALREADY in the stale-baseline CHANGED set. The correct pre-re-anchor expectation is therefore "the CHANGED count stays at exactly 133 per node, with three digests differing from before" — a check that would actually catch an accidental extra symbol. "No new failures" is too coarse to catch that.
  *Grounding:* bootstrap/tests/test_ast_attest.py:66 and :82 (`assert A.verify(_BASELINE, modules) == 0`); bootstrap/tests/_ast_attest.py:162-170 (Import/Docstring skip) and :187-192 (NEW reported as a note); `python -m pytest bootstrap/tests/test_ast_attest.py -q | grep -cE '^\s+CHANGED '` = 266 (133 per node), with `_apply_upgrade`, `_cmd_init_lock`, `write_install_lockfile` present
  *Suggested fix:* Replace "no new failures" with the concrete target: CHANGED count unchanged at 133 per node, the three named digests differ from their pre-change values, and the NEW-note set is exactly `FunctionDef:_cairn_provenance` plus the Import rotations. Carry that into the plan's per-chunk verification row. (Note the interaction with R1: if the stage-metadata route is taken, the expected CHANGED set becomes four functions, not three.)

* **[R8] (substantive)** The manifest smoke-check number is invalidated by the proposal's own sequencing. "Examples / smoke checks" says `--manifest` "must emit the same 94 data rows before and after", and the blast-radius section pins "94 data rows, as_of 2026-07-22". Both were run this session and are correct today (95 lines including the header = 94 data rows). But the proposal sequences its plan AFTER the accepted licensing plan's Chunk C/D, and that plan adds a `NOTICE.md` `_CORE_MAPPINGS` entry whose own acceptance criteria require `test_manifest.py` to extend "cleanly to 95 rows" and expect "95 total". At the landing point the correct expectation is 95-before / 95-after, so a plan chunk written to the literal 94 would fail its own smoke check for a reason unrelated to this change. This is a snapshot used where a live invariant was needed.
  *Grounding:* `python bootstrap/scaffold.py --manifest | wc -l` = 95 (94 data rows), run this session by two lenses; dev/plans/adopter-licensing-compliance.md:142 (the `_CORE_MAPPINGS` edit), :167-168 / :168-169 ("extends cleanly to 95 rows") and :179-180 ("95 total")
  *Suggested fix:* Register the invariant, not the count, per the three-kind count discipline: "`--manifest` emits the same number of data rows before and after this change; capture the pre-edit count at implementation time and assert equality" — optionally footnoting "94 as_of 2026-07-22; 95 once the licensing plan's Chunk C lands". Same treatment for the blast-radius bullet. Whoever writes the plan must re-derive the count at implementation time rather than copying 94.

* **[R9] (substantive)** The reader inventory omits the one lockfile reader that actually skews across versions — and it is the missing demonstration the proposal itself calls its "weakest link". `templates/modules/team-gated/run_security_audit.py` installs verbatim as `scripts/run_security_audit.py` into the adopter's tree and parses the whole lockfile itself (`json.loads(text[brace:])`) rather than going through `read_lockfile`. Because it is installed and hash-tracked, an adopter can be running a lagging copy against a lockfile a newer engine just wrote — a real old-reader/new-lockfile case, unlike the hypothetical "old engine binary" the proposal says it cannot demonstrate. Its key accesses were read: `lock.get("modules")`, `lock.get("files")`, `lock.get("tokens")` only, so unknown top-level keys are harmless — but that is a fact the proposal should assert and test, not one a reviewer should have to discover.
  *Grounding:* templates/modules/team-gated/run_security_audit.py:117-124 (whole-file `json.loads`), :140, :161, :200, :307, :357 (all `.get()` access); manifest row `scripts/run_security_audit.py\tmodules/team-gated/run_security_audit.py\tverbatim`
  *Suggested fix:* Add this reader to the blast-radius list, and add a node to the new test file that feeds a provenance-bearing lockfile to `run_security_audit.load_lockfile` + `required_apparatus_dsts` and asserts unchanged behavior. That converts the "argued from source, not demonstrated" caveat into a real test at near-zero cost, on a file that is frozen gate surface and shipped to adopters.

* **[R10] (substantive)** Where the additive-vs-breaking rule lives is wrong on three counts, and the chosen home cannot reach the audience it names. (a) **Routing rationale is wrong on its own cited source.** The proposal routes the `UPGRADE.md` subsection to "the descriptive layer" — but the descriptive layer is `docs/` (`dev/proposals/_template.md:159`; `docs/DOCUMENTATION_PLAN.md:151-155`), and `bootstrap/UPGRADE.md` is not in `docs/`. The content is prescriptive ("readers **must** use `.get()`", "**does** bump"), which `docs/DOCUMENTATION_PLAN.md:143-146` routes to "the governing layer's domain-local range, **in that domain**" — whose named exemplars are `bootstrap/BOOTSTRAP.md` and `bootstrap/fidelity-check.md`. So `bootstrap/` is the right directory for the opposite reason given. (b) **The rule is stated in full twice** — the `_LOCK_SCHEMA` annotation and `UPGRADE.md`, "carrying the same rule in adopter language" — which `docs/DOCUMENTATION_PLAN.md:253-257` calls "drift-prone duplication" and `doctrine/doc-governance.md:74-81` forbids: "Each rule lives in **exactly one** ... The other file may *point* to it ... but never restates it." (c) **`bootstrap/UPGRADE.md` cannot reach adopters at all.** `scaffold.py --manifest` emits zero `bootstrap/` rows, so `UPGRADE.md` is never installed into an adopter tree, and no installed template documents the lockfile field set either (a grep of `templates/**/*.md` for `cairn_version` / `cairn-lock` returns nothing). Describing it as carrying the rule "in adopter language" overstates its reach, and collides with the proposal's own headline framing ("make the install receipt say where it came from"): the receipt gains two values but no in-tree way to interpret them.
  *Grounding:* docs/DOCUMENTATION_PLAN.md:143-146, :151-155, :253-257; doctrine/doc-governance.md:74-81; dev/proposals/_template.md:159; `python bootstrap/scaffold.py --manifest` run this session: 94 data rows, `grep -c 'bootstrap/'` = 0; `_emit_lock_yaml`'s existing comment header at bootstrap/_scaffold/lockfile.py:184-189
  *Suggested fix:* Restate the routing per `docs/DOCUMENTATION_PLAN.md:143-146` (domain-local governing range, in `bootstrap/`). Name ONE canonical home for the additive-vs-breaking rule and make the other a one-line pointer. Widen open question 2 from two options to three: `AGENTS.md` (cross-cutting governing), a `bootstrap/` domain-governance file (`BOOTSTRAP.md` / `fidelity-check.md`), or the adopter how-to `UPGRADE.md`. For adopter reach, use the slot that already exists: `_emit_lock_yaml` writes a comment header into every lockfile (lockfile.py:184-189) — add one header line naming the provenance fields and where the rule lives, and describe the `UPGRADE.md` subsection as the Cairn-repo reference (like `doctrine/` citations), not adopter-tree documentation. If that header change is taken, enumerate the extra CHANGED `FunctionDef:_emit_lock_yaml` digest in the re-anchor delta.

* **[R11] (substantive)** Two template-required blocks are argued incorrectly or incompletely. (a) **The rate-limit N/A is argued on a scope test the template does not use, and it contradicts P3.** `dev/proposals/_template.md:166-168` scopes the gate to a proposal that "**changes doctrine** — a rule, process, or contract every contributor follows" — not to files under `doctrine/`. The proposal narrows this to "changes no `doctrine/` rule, process, or contract. The doctrine-evolution gate ... governs changes to doctrine under `doctrine/`; none are made here." But P3 explicitly authors a new rule on a protected contract — its own words are "What the contract is actually missing is the rule, not the number" — binding every future author of `_LOCK_SCHEMA`. The proposal simultaneously claims it writes a new contract rule and that it changes no contract rule. (b) **`bootstrap/PROVENANCE.md` is silently omitted from the Documentation/doctrine surface, and it is its own triage trigger.** `dev/proposals/_template.md:69-70` lists "**Licensing / provenance** — the by-file license split or `bootstrap/PROVENANCE.md`" as a proposal trigger; the proposal names only the install-contract trigger at :58-61. Worse, `bootstrap/PROVENANCE.md:72-83` is the canonical definition of install-side provenance and enumerates what the lockfile carries — "the exact `cairn_version` + `cairn_commit`, the resolved profile, and the per-file source / hash" (:77-79). Adding two provenance fields makes that enumeration stale in the very document the proposal quotes twice as its motivation. The section names `fidelity-check.md` as deliberately untouched but is silent on `PROVENANCE.md`, and the template is explicit at :150-152: "If none, say so explicitly — silent omission is a review finding."
  *Grounding:* (a) dev/proposals/_template.md:164-183 (gate scope) vs the proposal's own P3 text; doctrine/rationale.md:323-324 read this session. (b) dev/proposals/_template.md:69-70 and :150-152; bootstrap/PROVENANCE.md:72-83 (file is 83 lines; :77-79 enumerates the field set) — all read this session
  *Suggested fix:* (a) Keep the conclusion (no bypass claimed; the deadline framing correctly refused per `doctrine/rationale.md:346-347`, verified verbatim) but re-argue the N/A on the gate's own terms: `doctrine/rationale.md:323-324` states "No doctrine change from a single incident" — the gate is incident-triggered and rate-limits reactive churn, whereas P3 is a forward-looking definition of an already-declared contract with no incident behind it. That argument survives review; the `doctrine/`-directory scope test does not. (b) Add the licensing/provenance trigger to **Related**, and either add a one-sentence `PROVENANCE.md:77-79` amendment to **Touches** (extending the enumeration to name the two new fields) or state explicitly why the enumeration stays as-is. A one-line edit there is cheaper than the staleness it prevents.

* **[R12] (minor)** Three small accuracy items, each independently verified. (a) **The CITATION.cff parse contract is under-specified for the one input the change does not control.** `_cairn_version` matches a single `version:` line; `licenses` needs a *block* read, and CFF permits `license:` as either a scalar (`license: MIT`) or a sequence. The proposal cites CITATION.cff:19-21 correctly but never states the stop condition or the scalar form — and the real file puts `keywords:` with its own `- ` items immediately below the `license:` block (:22-28), so a scanner that keeps consuming `- ` lines would silently record six keywords as licenses. `cairn_root` is not always Cairn's own checkout (a fork, or `--cairn-root` pointed elsewhere), and a fork that drops the CC-BY half would most likely write the scalar form, against a stated return type of `list[str]` with no coercion rule. The inventory lists "present-but-empty" and "a single license" but not "list terminated by the next key" — the one case the shipped file exercises. (b) **The Bandit gate is missing from a blast-radius sweep that claims to be "checked, not assumed".** `AGENTS.md:303-306` names "a Bandit gate over the whole engine package" as a guard on the high-risk scaffold surface, and `bootstrap/tests/test_security_lint.py:160-179` proves every `.py` under `bootstrap/_scaffold/` is scanned recursively, with :80-89 making a missing bandit *fail* rather than skip in CI. The sweep enumerates `--manifest`, verify_integrity, the fidelity manifest, the gate manifest, the differential oracle, and the content scanner — but not the one security gate covering the file being edited. (c) **Citation slips.** The `cairn-internal-ref-allow` header comment is inert for a file under `dev/proposals/`: `scripts/check_cairn.py:504` gates `_check_dangling_internal_refs` on `_is_template_instruction(rel)`, defined at :283-290 as `return rel.startswith('templates/')` — so the directive does nothing here and reads as copied from `templates/core/AGENTS.md:1`; it also exempts `doctrine/proposals.md`, a path the proposal never cites. The `_oracle.py` quote "A broad normalization that could hide a content diff" begins at :30, not the cited :31-33. The broad-look block quote begins mid-line at :299 ("... in the adopter's repository. The install"), so the span is :299-302, not :300-302. The `PROVENANCE.md:55-58` quote is verbatim but the frame universalizes it: the source says "**v0.2** provenance is named-releases + signed-tags + the derived manifest...", while the proposal presents it as "Cairn's provenance posture is". Both line slips are in-bounds so `claim_check.py` passes them, but an External reviewer spot-checking will find the ranges wrong before finding the text right.
  *Grounding:* (a) CITATION.cff:18 `repository-code:`, :19-21 `license:` block, :22-28 `keywords:` block with sibling `- ` items; bootstrap/_scaffold/lockfile.py:103-111 (the single-line `_cairn_version` pattern being generalized). (b) bootstrap/tests/test_security_lint.py:51-59 and :160-179 (scan targets recurse `bootstrap/_scaffold/`), :80-89 (CI fails on missing bandit); AGENTS.md:303-306. (c) scripts/check_cairn.py:283-290 and :504; templates/core/AGENTS.md:1; bootstrap/tests/_oracle.py:28-33 (phrase begins :30); dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md:299 (`grep -n "The install"` → 299); bootstrap/PROVENANCE.md:55-58
  *Suggested fix:* (a) State the parse contract in P1: stop the `license:` block at the first line that is not an indented `- ` item; accept the scalar form as a one-element list; require every value to look like an SPDX id or drop it. Add both cases to the edge-case inventory and to the degradation test node — a `license:` block followed by a sibling block list must yield exactly `["CC-BY-4.0", "MIT"]`, and a scalar `license: MIT` must yield `["MIT"]` (or be documented as degrading to `[]`). (b) Add a sweep bullet: the new `_cairn_provenance` helper is inside Bandit scan scope; it uses `Path.read_text` + `re` exactly as `_cairn_version` (lockfile.py:103-111) already does, introduces no subprocess/eval/deserialization, so no new finding is expected — and list `python -m pytest bootstrap/tests/test_security_lint.py` in the smoke checks. (c) Drop the `cairn-internal-ref-allow` header (or keep it only if the author verified a checker path this panel did not, in which case trim `doctrine/proposals.md` from the token list); correct the oracle span to begin at :30 (`:30-32`, or widen to `:28-32`); correct the broad-look span to `:299-302`; and either keep "v0.2" inside the quotation or move the frame outside it (e.g. "PROVENANCE.md:55-58 states the v0.2 posture: ...").

**Coverage.** **Combined sweep (three lenses, all verified in-repo this session; HEAD 57d1daf, tree clean apart from `dev/plans/adopter-licensing-compliance.md`).**

*Doctrine and lifecycle:* every `doctrine/` citation opened and quote-matched — `rationale.md:323-347` (rate-limit gate, the two exhaustive bypass surfaces, the :346-347 sentence), `runtime-contract.md:177-179`, `dual-review.md:30-49` + :181-187 + :320-329, `doc-governance.md:74-81`. Grepped `doctrine/` for any pre-existing lockfile schema-stability rule (none) and `bootstrap/*.md` for "additive|schema" (none), so P3 is not redundant with existing doctrine. Doc-tier routing checked against `docs/DOCUMENTATION_PLAN.md:130-170`, :218-257. Triage triggers checked against `dev/proposals/_template.md:37-72`; template-required blocks (doc surface :148-162, rate-limit :164-183, forward-ref marker :73-82, count claims :99-103). Parent Decision quote verified verbatim at `dev/proposals/archive/2026-07-11-claude-adopter-licensing-compliance.md:631-635`.

*Engine and contract:* every lockfile writer (`grep _emit_lock_yaml` → install.py:1602, upgrade.py:1207, :1308, :1709, :1997) and every reader (`grep read_lockfile` plus the shipped `run_security_audit.load_lockfile`); the write-only `_LOCK_SCHEMA` claim (no read of the lockfile `schema` key anywhere in the tree); `read_lockfile` non-validation (lockfile.py:193-210); `verify_integrity.py:40-58` fail-closed path; the `--apply` meta plumbing (upgrade.py:900-932, :1801-1806, :1944-1945, :2249-2252); `_cmd_init_lock` (:1111-1207), `_commit_lock_and_caches` (:1255-1310), `_cmd_finalize_lockfile` (:1592-1709); `format_manifest` (install.py:1362-1370) and the diverged-tree refusal (:1572-1602); `__init__.py:282-298`; CITATION.cff:18-21.

*Gates:* `_gate_manifest.py:77-101/:165-167/:364-366` and the 147-entry pinned `frozen_files` fixture; `_ast_attest.py` node keying, duplicate `#<n>` suffixing, Import/Docstring skip, NEW-as-note, `_UPDATE_ALLOWLIST:141`; `_oracle.py:28-33/:94` (`_PROVENANCE_KEYS`) and `_oracle_activation.py:34-37` roster; `test_generated_output_scan.py:48-55`; `content_scan.py:285-290`; `test_security_lint.py:51-59/:160-179`; `claim_check.py` marker-continuation logic at :371-397/:625-635 (the Proposed-paths block is line-adjacent, so it parses) and the `cairn-internal-ref-allow` directive at :398-473 (real, not invented).

*Runs reproduced independently by two lenses:* `python -m pytest bootstrap/tests` → 3 failed / 1408 passed / 3 skipped (~105s), matching the proposal's baseline exactly including the three node names; the AST gate's 266 CHANGED lines = 133 per node with `write_install_lockfile`, `_cmd_init_lock`, `_apply_upgrade` all already in the CHANGED set; `python bootstrap/scaffold.py --manifest` → 95 lines / 94 data rows, zero `bootstrap/` rows, zero `.svg`/`.png`/logo/brand rows; `dev/.cairn/cairn-lock.yml` parsed (9 top-level keys, 81 file records, `schema: 1`, `migrated: true`, `cairn_commit: "unknown"`) and `dev/.cairn/` membership (7 files, no fidelity manifest, no URL anywhere). Collision-risk tests read, not assumed (`test_lockfile_module.py:108-115`, `test_upgrade.py:797`, `:1505-1520`) plus a grep for any exact-key-set assertion (none). Sibling-plan sequencing checked at `dev/plans/adopter-licensing-compliance.md:78-96/:142/:155-180` — its Chunk D does close Issue #1 as a reviewed side effect, so the proposal's "fresh baseline" sequencing claim is CORRECT (one lens specifically hunted for a false claim there and found none).

**Negative space — what the panel did NOT cover, and someone should.** (1) No lens executed a real scratch install or an actual `--stage`/`--apply` cycle with a synthetic provenance-bearing lockfile, so the round-trip preservation claim and all findings on the stage-metadata path (R1) are read from source, not observed — this is the single largest uncovered surface and it is exactly where the blocking finding sits. (2) No lens ran `scripts/claim_check.py` or `scripts/check_cairn.py` over the proposal text (it is not on disk); someone must before commit. (3) No lens evaluated the security disposition of writing a URL and license identifiers into a tracked, adopter-committed machine file — P4's own text calls a read-side change "plausibly a Security-Review trigger", the write side deserves the same question, and `bootstrap/_scaffold/` is on the SENSITIVE_ROSTER. (4) No lens evaluated P3's no-bump call as a *contract* question rather than a code question — that is the External tier's job and it is the right escalation. (5) The cross-proposal `NOTICE.md` URL-scanner hazard in alternative 5 is unverified from the sibling side (the scanner and its empty allowlist were verified; the unwritten `NOTICE.md` was not), as is the drift risk between `NOTICE.md` prose and the lockfile `licenses` field once both exist. (6) No lens assessed the `dev/PLANNING.md` deferred-row mechanics for P4. Two items from one lens's negative space were closed by the others: the suite baseline and the 133-CHANGED figure were independently reproduced twice, and the P1 line-scanner's parse behavior was evaluated (R12a) though not against a real malformed multi-line YAML fixture.

**Second-round recommendation.** **Consolidated: a narrow, gated second Internal read, then External cross-type before the Decision. The panel split on the first half; the split is recorded, not adjudicated.**

Two of three lenses (install-contract-compat, evidence-feasibility) call for revise-and-re-review rather than Response-and-move-on, for the same reason: R1, R2, and R3 each change what the *implementing plan must do* — a fourth engine function, a stage-metadata cross-version compat rule, and either a relocated test file or a second supervised gate-manifest re-anchor — so they are not correctable by a Response that leaves the mechanism description standing. The doctrine-conformance lens dissents: it judged all its findings fixable in a Response without new reasoning, and warned that a full second same-type read would re-cover lenses already swept.

The reconciliation both sides support: **do not run a full second Internal pass; run a targeted re-read gated on exactly four things.** (a) The corrected P2, showing which fork was taken for the `--apply` backfill (stage-metadata vs live read) with Touches and the AST delta re-derived to match — this is the one change that alters the proposal's contract surface, and the one surface no lens could test-drive. (b) The re-scoped test homes and gate-manifest sequencing per R2. (c) The P5 rewrite acknowledging that neither `--init-lock` nor re-install can backfill Cairn's own lockfile. (d) The revised verification plan carrying the falsifiable gate expectation (CHANGED stays 133/node, or 4 CHANGED functions if the stage route is taken) and the row-count invariant instead of the bare 94. Everything else the panel verified — the doctrine quotes, the write-only-schema finding, the suite baseline, the gate-manifest and oracle blast radius, the no-collision test survey — does not need re-checking, and the re-read should not re-litigate citations.

R4 is blocking on `doctrine/dual-review.md:186-187` and lands as an **edit to the header line, not a defense**: correcting the tier to `required(External cross-type)` means the plan gets a cross-type read regardless, which is what covers the compatibility argument's weakest link (the untested old-engine direction the proposal itself flags).

**All three lenses converge on an External cross-type read of the proposal before the Decision**, narrowly briefed on facts only, carrying R1 and R9 as its starting questions plus exactly two framing questions: (i) does an old engine preserve unknown top-level keys on `--apply` in any released version — i.e. is no-bump correct for a byte-level-stable install contract, and does the old-engine-preserves-unknown-keys argument survive without a demonstration; (ii) is the additive-vs-breaking rule better sited in a `bootstrap/` domain-governance file than in `UPGRADE.md`. Both are cross-version-skew and rule-siting questions that a fresh same-type reader is structurally weak at. Per `doctrine/dual-review.md:320-323` that recommendation is the Maintainer's to weigh, not the panel's to impose.

Open questions: 1 (`licenses` vs `source_licenses`) and 2 (rule home, which R10 says must be widened to three options) are genuinely Maintainer calls and need no further review to resolve; open question 4 is answered by P5's own analysis — but only once R5's correction lands, which converts it from a deferral-to-a-trigger-that-never-fires into a real choice.
## Response — Claude (author) — 2026-07-22

**Verdict: revise, not withdraw.** I want to be plain about what the panel found before I dispose of it item by item.

Three lenses attacked P3's no-bump argument — the load-bearing judgment in this proposal — and none of them broke it. R3 goes further and says the argument is *better* supported by the tree than I claimed. The motivation, the evidence base, the blast-radius sweep, the doctrine quotes, and the suite baseline all reproduced independently. So the proposal's central claim is sound and I am not going to concede it.

But I made a **factual error about code behavior that I did not open the file to check** (R1), and I **under-enumerated the writers I was reasoning about** (R3a). Those are exactly the failure modes this repository has killed proposals for, and the fact that the conclusions happen to survive does not make the method acceptable. I asserted that `--apply` "already re-sources `cairn_version` / `cairn_commit` from the Cairn being upgraded to." It does not. It reads values captured at `--stage` time out of `stage-metadata.json` (`bootstrap/_scaffold/upgrade.py:906-907` → `:931-932` → `:1801` → `:1944-1945`), and `--apply` never receives `--to` at all. I built P2's entire symmetry argument on a sentence I inferred from two lines instead of reading the path. I own that.

This is not the automated-review-committer case. There, the premise was invalidated and no revision could rescue it. Here every defect is localized — a mechanism description, a gate accounting error, a writer inventory, a rule-siting call, a tier label — and each has a concrete correction that makes the proposal *more* accurate rather than papering over a hole. The revised design below is smaller in claim and larger in verified surface than what I opened.

All twelve findings were re-verified against the tree this session at HEAD `57d1daf`. I found no finding to be wrong.

---

### R1 — `--apply` provenance mechanism mis-described; the implementation fork is unnamed — **accept**

Correct as stated, and the most important finding in the panel. I re-read the path: `_write_stage` captures `"new_version": _cairn_version(cairn_root)` and `"new_commit": to_ref or _cairn_commit(cairn_root)` at `bootstrap/_scaffold/upgrade.py:906-907`, writes the meta dict at `:931-932`, and `_apply_upgrade` re-reads it at `:1801` and consumes it at `:1944-1945`. `--apply` re-sources nothing.

**I take the stage-metadata route (the review's option b), and I have a cleaner argument for it than the one the review offered.** The review framed the ref-awareness question as an open fork; it is already answered in-tree. `new_commit` is ref-aware, but `new_version` is **not** — `_cairn_version(cairn_root)` at `:906` reads the working tree's `CITATION.cff` (`bootstrap/_scaffold/lockfile.py:103-111`) with no `to_ref` consultation. `source_repository` and `licenses` come from **that same file, by the same reader shape**. So the correct disposition is not a judgment call about ref-awareness: it is to source them exactly where and how `new_version` is sourced, in `_write_stage`'s meta dict, non-ref-aware, and to say so explicitly. Consistency with the sibling field read from the same file is the whole argument.

`_write_stage` joins Touches and the AST delta as a fourth CHANGED `FunctionDef`. `_apply_upgrade` reads the new keys with a `.get()` fallback to the current lock value, so an old stage applied by a new engine degrades to "keep what the lockfile already had" rather than writing nulls — and that old-stage/new-engine case joins the edge-case inventory. The in-tree precedent for treating `stage-metadata.json` as a compat surface is real (`upgrade.py:920`, the `module_blocked` key-name comment).

### R2 — editing `test_upgrade.py` HOLDs the gate manifest — **accept**

Correct, and my blast-radius bullet was wrong by omission: I checked whether the *engine* edit matched a frozen glob and never checked the *test* edit. `bootstrap/tests/test_upgrade.py` is in the 147-entry pinned `frozen_files` set (verified by parsing `bootstrap/tests/fixtures/gate_manifest.json` this session), it is in neither `CASCADE_MUTABLE` nor `PHASE_SPLIT_TARGETS`, and `_gate_manifest.py:364` appends `FROZEN-MODIFIED` to `holds` — not `notes`. The `test_intents_tool.py` entry at `:93-101` documents a prior batch hitting this exact wall.

All new nodes move into `bootstrap/tests/test_lockfile_provenance.py`, which reads `FROZEN-NEW` (`:366`, a note). It imports `_install` from `test_upgrade.py` (module-level at `:45`) rather than duplicating the harness — importing a frozen file does not modify it, so no HOLD. No second gate-manifest re-anchor is needed.

### R3 — five lockfile writers, not three; the `migrated` precedent is the strongest evidence and I omitted it — **accept**

Both halves correct. `grep _emit_lock_yaml` returns five write sites: `install.py:1602`, `upgrade.py:1207`, `:1308` (`_commit_lock_and_caches`), `:1709` (`_cmd_finalize_lockfile`), `:1997`. I read the two I had missed: both operate on the dict returned by `read_lockfile` and write it back, so unknown keys round-trip verbatim — which strengthens P3 rather than weakening it. But the reviewer's point stands that a reader could not tell whether I checked them or missed them, and I missed them.

The behavioral consequence I also missed: neither backfills, so an adopter whose only upgrade traffic is `--finalize` or `--adopt-module` never gains the fields. That qualifies P2's "keeps that from being permanent" and my install-vs-apply parity invariant, and it goes in as a stated limit, not a footnote.

On `migrated`: this is the finding I am most annoyed to have missed, because it is the best evidence in the proposal and it was sitting in Cairn's own lockfile. `migrated` is written only by `_cmd_init_lock` (`upgrade.py:1197`), is absent from every fresh install, is read only by a test assertion (`test_upgrade.py:797`), and coexists with `schema: 1` today. That is a live, additive, writer-varying optional key at the current schema number. It converts P3 from an argument-from-absence into an argument from existing practice — and, as R11 will need, it means P3 **codifies** a rule the engine already follows rather than authoring a new one.

### R4 — declared plan-review tier is below the doctrinal floor — **accept**

Correct, and it is an edit, not a defense. `doctrine/dual-review.md:184-187` reads verbatim: "that tier is chosen on the same structural-independence axis as any other review here — an Internal-floor read for an ordinary plan, a different-agent-type External round for a high-risk or contract-touching one." I called the surface "the byte-level-stable install contract" in the same sentence where I demoted External to "recommended." Contract-touching is precisely the case doctrine assigns an External round, and `:325-329` forbids using recommend-and-decide to soften a tier downward. The header becomes `required(External cross-type)`.

### R5 — P5 promises a backfill path that cannot fire — **accept**

Correct. `_cmd_init_lock` returns early whenever `read_lockfile(target) is not None` (`upgrade.py:1121-1123`), and `write_install_lockfile` refuses on a diverged tree (`install.py:1572-1582`); Cairn's tree is heavily diverged. So "gains the fields at its next re-init or re-install" names two paths that are both structurally blocked. Restated honestly below. This converts open question 4 into a real choice, which is the right outcome.

### R6 — `_LOCK_SCHEMA` takes a `#:` comment, not a docstring — **accept**

Correct on both counts. `_LOCK_SCHEMA = 1` is a module-level `Assign` (`lockfile.py:42`); Python attaches no docstring to it, and a bare string literal after it becomes a top-level `ast.Expr` keyed `"Docstring"` (`_ast_attest.py:84-88`), suffixed to `Docstring#2` by the `seen` counter (`:97-105`) because `lockfile.py` already has a module docstring — a NEW baseline key my enumerated delta did not list. The file's own convention two lines below is the `#:` comment form. Taking it keeps the delta exactly falsifiable.

### R7 — the gate expectation is not falsifiable and slightly overstated — **accept**

Correct. `_classify` `continue`s over baseline entries typed `Import`/`ImportFrom` and over any `Docstring*` key (`_ast_attest.py:162-170`), and NEW keys are reported as notes (`:187-192`), so neither the new helper nor the rotated imports can produce a gate failure. Only CHANGED digests move.

I re-derived the target for the **revised** delta, which now touches five functions rather than three. Verified this session: the CHANGED set is 133 per node (266 lines across two nodes), and **all five** touched functions — `write_install_lockfile`, `_cmd_init_lock`, `_apply_upgrade`, `_write_stage`, `_emit_lock_yaml` — are *already* in it. So the falsifiable pre-re-anchor target is unchanged by the expansion: **CHANGED stays at exactly 133 per node**, five named digests differ from their prior values, and the NEW-note set is exactly `FunctionDef:_cairn_provenance` plus Import rotations. Any 134 means an accidental extra symbol.

### R8 — the 94-row smoke check is invalidated by my own sequencing — **accept**

Correct, and it is a clean instance of me using a snapshot where a live invariant was required — the exact three-kind discipline the repo asks for. 94 data rows is right today and wrong at the landing point, because I sequence this plan after the licensing plan's Chunk C, which adds a `NOTICE.md` `_CORE_MAPPINGS` entry and expects 95. The plan registers the invariant (row count equal before and after, captured at implementation time) rather than the number.

### R9 — the shipped `run_security_audit.py` is the real old-reader case — **accept**

Correct, and this is the finding that most improves the proposal. I wrote that the old-reader direction was "argued from source, not demonstrated" and called it my weakest link. R9 supplies a reader that makes it demonstrable: `templates/modules/team-gated/run_security_audit.py` installs verbatim as `scripts/run_security_audit.py` (manifest row 70, verified), parses the whole lockfile itself with `json.loads(text[brace:])` at `:122` rather than going through `read_lockfile`, and touches only `modules` / `files` / `tokens` via `.get()`. Because it is installed and hash-tracked, an adopter genuinely can run a lagging copy against a newer lockfile. A test node against `load_lockfile` + `required_apparatus_dsts` converts my caveat into an actual test at near-zero cost.

### R10 — rule-siting is wrong on routing, duplicated, and cannot reach adopters — **accept with modification**

I accept all three sub-findings. (a) My "descriptive layer" routing was wrong on its own cited source: the descriptive layer is `docs/` (`docs/DOCUMENTATION_PLAN.md:151-155`), the content is prescriptive, and `:143-146` routes prescribing-how-one-domain-is-organized to "the governing layer's domain-local range, **in that domain**." `bootstrap/` is the right directory for the opposite reason I gave. (b) Stating the rule in full in two places is duplication drift, forbidden by `doctrine/doc-governance.md:76-77`: "Each rule lives in **exactly one** of the two files. The other file may *point* to it — a one-line cross-reference — but never restates it." (c) `--manifest` emits zero `bootstrap/` rows, so `UPGRADE.md` never reaches an adopter tree and describing it as carrying the rule "in adopter language" was an overstatement.

**Modification:** the review left the canonical home open and widened the question to three options. I name it instead, because leaving it open is how the duplication happened. Canonical home is the **`bootstrap/UPGRADE.md` subsection** — right directory per `:143-146`, and it is already the lockfile's documented home (`bootstrap/PROVENANCE.md:76` points there). The `#:` block on `_LOCK_SCHEMA` becomes a **one-line pointer**, not a restatement. I still carry open question 2 with all three options, since siting is a Maintainer call.

I also take the review's `_emit_lock_yaml` header suggestion, because it is an existing slot rather than a new mechanism — the header already writes two comment lines into every lockfile (`lockfile.py:184-189`). One added pointer line naming the provenance fields is the only thing in this proposal that actually reaches an adopter's tree. It makes `_emit_lock_yaml` a fifth CHANGED `FunctionDef`, enumerated above and confirmed already-CHANGED.

### R11 — the rate-limit N/A is argued on the wrong test; `PROVENANCE.md` silently omitted — **accept with modification**

**(a) Accept the finding; modify the replacement argument.** My scope test was wrong: `dev/proposals/_template.md:166-167` scopes the gate to a proposal that "**changes doctrine** — a rule, process, or contract every contributor follows," not to files under `doctrine/`. And the reviewer is right that I claimed to author a contract rule and to change no contract rule in the same document.

The review proposes re-arguing on incident-triggering. I think there is a better argument, and R3(b) is what supplies it: **`migrated` proves the additive-optional-key rule is already the engine's practice.** It has been a writer-varying optional top-level key at `schema: 1` since `--init-lock` shipped. So P3 does not introduce a rule contributors must newly follow — it writes down one the code has followed all along, which is documentation of existing behavior, not doctrine evolution. I offer the incident-triggering point as a secondary: `doctrine/rationale.md:323-324` gates a change arising *from an incident* ("**No doctrine change from a single incident** unless the Maintainer explicitly classifies the incident as high-risk"), and there is no incident behind this.

My refusal of the bypass stands unchanged and I restate it: the two qualifying surfaces at `:339-344` are exhaustive, this is neither, and the first-adopter deadline is exactly the framing `:346-347` excludes — "Any other 'this feels urgent' framing falls outside the bypass and obeys the recurrence requirement." I claim no bypass.

**(b) Accept in full.** `dev/proposals/_template.md:69-70` lists "**Licensing / provenance** — the by-file license split or `bootstrap/PROVENANCE.md`" as its own trigger and I named only the install-contract one. Worse, `bootstrap/PROVENANCE.md:78-79` enumerates what the lockfile carries — "the exact `cairn_version` + `cairn_commit`, the resolved profile, and the per-file source / hash" — and adding two fields makes that enumeration stale in the document I quote twice as motivation. I named `fidelity-check.md` as deliberately untouched and said nothing about `PROVENANCE.md`, against `:150-152` ("silent omission is a review finding"). A one-line amendment goes into Touches.

### R12 — three accuracy items — **accept** (all three)

**(a) The CITATION.cff parse contract.** The most consequential of the three and a live bug, not a nit. `license:` at `CITATION.cff:19-21` is immediately followed by `keywords:` at `:22` with its own six `- ` items at `:23-28`. A scanner generalized from `_cairn_version`'s single-line pattern that simply keeps consuming `- ` lines would silently record six keywords as licenses. The parse contract is now stated in P1 and both cases are test nodes.

**(b) Bandit.** Correct — I claimed a sweep that was "checked, not assumed" and omitted the one security gate covering the file I am editing. `bootstrap/tests/test_security_lint.py:160-180` proves every `.py` under `bootstrap/_scaffold/` is scanned recursively. Added as a sweep bullet and a smoke check.

**(c) Citation slips.** All three verified and all three mine. The `cairn-internal-ref-allow` header is inert here: `scripts/check_cairn.py:504` gates the check on `_is_template_instruction(rel)`, which is `return rel.startswith('templates/')` (`:283-290`) — so it does nothing in `dev/proposals/` and it also exempted `doctrine/proposals.md`, a path I never cite. Dropped. The `_oracle.py` phrase begins at `:30`, not `:31`. The broad-look quote begins mid-line at `:299` ("... in the adopter's repository. The install"), so the span is `:299-302`. And the `PROVENANCE.md:55-58` frame universalized a version-scoped statement — the source says "**v0.2** provenance is named-releases + signed-tags + the derived manifest"; I wrote "Cairn's provenance posture is." That last one is the same drift class the batch has been warned about twice, and it is on me: the words were verbatim, the frame silently widened them. Fixed by moving "v0.2" inside the quotation.

### On the panel's second-round recommendation — **accept**

I accept the gated re-read, and I would ask for it even if the panel had not. R1's fork is a change to what the implementing plan must do, on the one surface no lens could test-drive (no lens ran a real `--stage`/`--apply` cycle). A Response that left the mechanism description standing would not have been correctable on paper. The four gating items — corrected P2 with the fork named, re-scoped test homes, honest P5, falsifiable gate expectation with the row-count invariant — are all discharged below.

R4 makes the External cross-type read mandatory rather than recommended, which is also what covers the compatibility argument's weakest link. I endorse the panel's two framing questions and add R9's reader as the concrete handle on question (i).

---

## Revised proposal — 2026-07-22

**Status: revised.** Changes from the opened version, in one place:

**Header.**
* `Plan review:` becomes **`required(External cross-type)`** — contract-touching per `doctrine/dual-review.md:184-187`; ratified at Decision. (R4)
* `Touches` gains `_write_stage` (`bootstrap/_scaffold/upgrade.py:743`, meta dict at `:900-906`), `_emit_lock_yaml` (`bootstrap/_scaffold/lockfile.py:179`), and a one-sentence amendment to `bootstrap/PROVENANCE.md:78-79`. (R1, R10, R11b)
* `Related` gains the **licensing / provenance** triage trigger, `dev/proposals/_template.md:69-70`. (R11b)
* The inert `cairn-internal-ref-allow` header comment is removed. (R12c)

**P1 — the CITATION.cff reader.** Unchanged in shape; the parse contract is now stated rather than left to the implementer (R12a): stop the `license:` block at the first line that is not an indented `- ` item; accept the scalar form (`license: MIT`) as a one-element list; drop any value that does not look like an SPDX identifier. Degradation to `("unknown", [])` is unchanged and matches `_cairn_version` (`lockfile.py:103-111`).

**P2 — the fields, at the writers that construct.** Corrected mechanism (R1): `--apply` does not re-source; it consumes `stage-metadata.json`. So `_write_stage` captures `source_repository` / `licenses` via `_cairn_provenance(cairn_root)` in the meta dict at `upgrade.py:900-906`, **beside `new_version` and non-ref-aware for the same reason** — both read the working tree's `CITATION.cff`, and `new_version` is already not ref-aware at `:906`. `_apply_upgrade` reads them at `:1944-1945` with a `.get()` fallback to the current lock value, so an old stage applied by a new engine degrades rather than writing nulls.

Writer inventory corrected to five, classified (R3a):
* **construct** (gain the fields): `write_install_lockfile` (`install.py:1602`), `_cmd_init_lock` (`upgrade.py:1207`).
* **advance** (backfill from stage meta): `_apply_upgrade` (`upgrade.py:1997`).
* **copy/mutate** (preserve, do not backfill): `_commit_lock_and_caches` (`upgrade.py:1308`), `_cmd_finalize_lockfile` (`upgrade.py:1709`) — both write back the dict from `read_lockfile`, which is the strongest in-tree evidence for no-bump.

**Stated limit, replacing an overclaim:** an adopter whose only upgrade traffic is `--finalize` or `--adopt-module` does not gain the fields. The parity invariant is narrowed to fresh-install vs `--apply`.

**P3 — no bump; rule sited once.** The argument is unchanged and now rests on `migrated` (R3b): a live additive, writer-varying, optional top-level key coexisting with `schema: 1` — written only by `_cmd_init_lock` (`upgrade.py:1197`), absent from every fresh install, read only at `test_upgrade.py:797`. P3 therefore **codifies existing practice** rather than authoring a new rule. Canonical home is the `bootstrap/UPGRADE.md` subsection (domain-local governing range, `docs/DOCUMENTATION_PLAN.md:143-146`); the `#:` comment on `_LOCK_SCHEMA` is a one-line **pointer**, not a restatement (R6, R10a/b); one added line in the `_emit_lock_yaml` header (`lockfile.py:184-189`) is the only adopter-reaching surface (R10c).

**P4 — validate-on-read.** Unchanged; still deferred, still gets a `dev/PLANNING.md` row.

**P5 — Cairn's own lockfile.** Corrected (R5): it stays provenance-free **until either a self-targeted `--stage`/`--apply` runs or the file is deleted and re-inited by hand** — `--init-lock` early-returns on an existing lockfile (`upgrade.py:1121-1123`) and a re-install refuses on a diverged tree (`install.py:1572-1582`). Recommendation to leave it stands; open question 4 is now a real choice.

**Rate-limit block.** Conclusion unchanged (no bypass claimed; deadline framing refused per `doctrine/rationale.md:346-347`); the `doctrine/`-directory scope test is replaced by the codification argument, with incident-triggering (`:323-324`) as secondary. (R11a)

**Documentation surface.** Adds the `bootstrap/PROVENANCE.md:78-79` enumeration amendment, and corrects the `UPGRADE.md` routing rationale from descriptive to domain-local governing. (R10a, R11b)

**Tests and verification.**
* All new nodes live in `bootstrap/tests/test_lockfile_provenance.py`, importing `_install` from `test_upgrade.py:45`; **no frozen gate file is edited** (R2).
* New nodes: the `license:`-block-terminated-by-`keywords:` case must yield exactly `["CC-BY-4.0", "MIT"]`; scalar `license: MIT` must yield `["MIT"]` (R12a); a `--finalize` round-trip for unknown-key preservation (R3a); `run_security_audit.load_lockfile` + `required_apparatus_dsts` against a provenance-bearing lockfile (R9).
* **Falsifiable gate target** (R7), re-derived for the five-function delta and verified this session: CHANGED stays at **exactly 133 per node**; five named digests differ; the NEW-note set is exactly `FunctionDef:_cairn_provenance` plus Import rotations. All five touched functions are already in the stale CHANGED set at HEAD `57d1daf`, so the expansion does not move the count.
* `--manifest` becomes an **invariant** — equal row count before and after, captured at implementation time — not the literal 94, which the licensing plan's Chunk C moves to 95 (R8).
* Baseline restated, re-run this session: **3 failed / 1408 passed / 3 skipped (100s), as_of 2026-07-22**. Target is no new failures, not green.
* Bandit added to the sweep and the smoke checks: `_cairn_provenance` is inside scan scope (`test_security_lint.py:160-180`) and uses `Path.read_text` + `re` exactly as `_cairn_version` does — no subprocess, eval, or deserialization, so no new finding expected (R12b).

**Citation corrections** (R12c): oracle span → `:30-32`; broad-look span → `:299-302`; `PROVENANCE.md:55-58` quoted with "v0.2" inside the quotation.

**Open questions.** 1 and 3 unchanged. **2 widened to three options** — `AGENTS.md` (cross-cutting governing) / a `bootstrap/` domain-governance file / the `UPGRADE.md` subsection as revised. **4 is now a live choice**, not a deferral to a trigger that cannot fire.

## Review -- Gemini (External, different-agent-type) -- 2026-07-22

**Model**: Gemini 3.6 Flash / Antigravity
**Verdict**: SHIP (conditional on Maintainer resolution of open questions 1–4 and AST baseline re-anchoring)

### Steelman
This proposal adds declared machine-readable install traceability (`source_repository` and `licenses` read from `CITATION.cff`) without risking install-contract instability. By keeping `_LOCK_SCHEMA = 1` and codifying the additive-optional-key compatibility rule, it avoids manufacturing artificial breaking changes for existing adopters. The revised proposal thoroughly addresses the Internal panel's findings: it corrects the `--apply` metadata plumbing (`_write_stage` -> `stage-metadata.json` -> `_apply_upgrade`), enumerates all five lockfile writers, provides an exact falsifiable gate target (CHANGED stays 133/node), isolates tests into a new `FROZEN-NEW` file to avoid gate-manifest HOLDs, and elevates the plan-review tier to `required(External cross-type)`.

### Critiques

* **[E1] (No-Bump Compatibility & Old-Engine Interrogation)**
  Interrogating the no-bump compatibility argument and the two panel framing questions:
  1. *Does an old engine preserve unknown top-level keys on `--apply`?* **Yes.** In all released versions, `_apply_upgrade` initializes `new_lock = dict(lock)` (`upgrade.py:1943`). When `read_lockfile` parses a lockfile containing top-level `source_repository` and `licenses` keys, `new_lock` retains those keys in memory and writes them back via `_emit_lock_yaml`. When an old engine stages an upgrade, its `stage-metadata.json` lacks new provenance keys, so a new engine applying an old stage gracefully falls back via `.get()` to existing lock values.
  2. *Is no-bump correct for a byte-level-stable contract?* **Yes.** `AGENTS.md:310-312` mandates byte-level stability for the install contract. Because `_LOCK_SCHEMA` is a single integer with no minor component, bumping to `schema: 2` for purely additive optional fields would manufacture an incompatibility—causing old engines or future strict validators to refuse lockfiles they can read cleanly. The `migrated: true` key (written only by `_cmd_init_lock` at `upgrade.py:1197`, absent from fresh installs, coexisting with `schema: 1`) demonstrates that optional top-level fields without a schema bump represent established engine practice.

* **[E2] (Verification of `--apply` Stage-Metadata Plumbing)**
  The corrected `--apply` mechanism is sound: `_write_stage` (`upgrade.py:900-906`) captures `"new_source_repository"` and `"new_licenses"` via `_cairn_provenance(cairn_root)` into `stage-metadata.json` beside `"new_version"`. `_apply_upgrade` (`upgrade.py:1944-1945`) reads them with `.get()` fallbacks to the existing lock dict. Sourcing both from working-tree `CITATION.cff` maintains complete structural symmetry with `new_version`.

* **[E3] (Verification of Five-Writer Inventory & Falsifiable Gate Target)**
  * **Writer Inventory:** Verified all five `_emit_lock_yaml` write sites in `bootstrap/_scaffold/`: `install.py:1602` (fresh install), `upgrade.py:1207` (`_cmd_init_lock`), `upgrade.py:1308` (`_commit_lock_and_caches`), `upgrade.py:1709` (`_cmd_finalize_lockfile`), and `upgrade.py:1997` (`_apply_upgrade`). `_commit_lock_and_caches` and `_cmd_finalize_lockfile` preserve existing keys verbatim via `read_lockfile`.
  * **Gate Target:** Verified in `bootstrap/tests/test_ast_attest.py` that all five touched functions (`write_install_lockfile`, `_cmd_init_lock`, `_apply_upgrade`, `_write_stage`, `_emit_lock_yaml`) are already present in the stale baseline's CHANGED set. The falsifiable gate target pre-re-anchor is exactly **133 CHANGED per node** (266 lines across two nodes).

* **[E4] (Plan Review Tier Alignment)**
  Elevating `Plan review` to `required(External cross-type)` complies with `doctrine/dual-review.md:184-187` (contract-touching surfaces require an External round) and `:325-329` (recommend-and-decide cannot soften a required tier downward).

### Coverage

* **Covered**:
  * Verified `_apply_upgrade` lock dict building in `bootstrap/_scaffold/upgrade.py:1943-1946` and `_write_stage` metadata dict at `upgrade.py:900-932`.
  * Checked all five `_emit_lock_yaml` call sites in `install.py` and `upgrade.py`.
  * Evaluated `migrated` top-level key precedent in `dev/.cairn/cairn-lock.yml:7` and `upgrade.py:1197`.
  * Verified AST attestation behavior in `bootstrap/tests/test_ast_attest.py` and `bootstrap/tests/_ast_attest.py`.
  * Inspected `run_security_audit.py:117-124` lockfile parsing.
* **Not covered**:
  * End-to-end execution of `--stage`/`--apply` with a synthetic provenance lockfile (to be executed during plan implementation).
  * Implementation of `bootstrap/tests/test_lockfile_provenance.py`.

## Decision -- {{Maintainer}} -- {{YYYY-MM-DD}}

*(Awaiting the Maintainer. The revised proposal has cleared both Internal and External reads. Four decisions belong to the Maintainer: (1) Accept/reject the provenance fields and compatibility rule; (2) Open Question 1: field naming `licenses` vs. `source_licenses`; (3) Open Question 2: rule siting in `bootstrap/UPGRADE.md` vs. `AGENTS.md` vs. domain-governance file; (4) Open Question 4: whether to backfill `dev/.cairn/cairn-lock.yml` via self-targeted `--apply`.)*
