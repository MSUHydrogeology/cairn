<!-- The path below is a forward-reference test file this proposal would create; it materializes in the implementing plan. -->
<!-- claim-check-allow: bootstrap/tests/test_lockfile_provenance.py -->
<!-- cairn-internal-ref-allow: doctrine/rationale.md doctrine/runtime-contract.md doctrine/proposals.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Lockfile provenance fields: make the install receipt say where it came from and under what licenses — without bumping the schema

**Author**: Claude (Strategy)
**Model**: Claude Opus 4.8
**Date opened**: 2026-07-22
**Status**: proposed
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
