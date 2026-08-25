# The subtraction sweep: execute the refocus, then bring the sisters into compliance

**Author**: Claude (Strategy)
**Model**: Fable 5
**Date opened**: 2026-08-25
**Status**: revising
**Lane**: deliberate — touches the install contract (named high-risk surface)
and removes ~61k lines
**Attention asked**: one External proposal review; one Decision (which also
grants the suite-ledger allowance, §4); two per-sister sign-offs at the gated
chunks; the Security Review named in §5. No other Maintainer interactions
planned.
**Outcome that repays it**: the build table delivered — a ~2-minute inner
loop, two governing documents a scientist can read in a sitting, both sister
repos on the lean install, and ~61k lines of process machinery gone.
**Touches**: `AGENTS.md` + `dev/agent_collaboration.md` + both templates and
shipped twins; `tools/`, `scripts/`, `templates/skills/`,
`templates/modules/` per the build table; `bootstrap/tests/`; the fidelity,
gate, and `scaffold.py --manifest` install-contract surfaces; `dev/PLANNING.md`;
then `modflow_tools` and `lhm`
**Related**: `dev/strategy/2026-08-21-claude-nimbleness-recovery.md` (the
deliberation; its **build table governs** this proposal's inventory), the
accepted `convergent-lifecycle` and `retire-external-plan-review` contracts
**Plan review**: required(Internal, security) — the sweep touches the install
contract and the release apparatus's surroundings

## Origin

The Maintainer's refocus, deliberated in the strategy note across two
External review rounds, with the final three calls decided 2026-08-25,
verbatim: foldback — *"the foldback ledger should become just a 'file an
issue with Cairn', which we are already set up to do"*; the suite-ledger
allowance — *"I accept your recommendation here"*; the trust root — *"I like
the trust root concept."* Sister compliance is full and immediate:
*"Rip off the band-aid."*

## Proposal

Execute the strategy note's **build table** — the authoritative inventory —
as chunks in its dependency order. This proposal adds no design; where any
text here disagrees with the table, the table governs.

1. **The per-file manifest** (first chunk, the reviewable inventory): every
   file the sweep touches, with the property removed, its replacement or the
   explicit decision that the property ends, and the twins/tests that move
   with it. For mixed files, per-function. Committed before any deletion.
2. **The constitution rewrite**: `dev/agent_collaboration.md` to ~150 lines
   around the accepted lifecycle (the review question, three lanes, the
   irreversibility tripwire as a one-way latch, the consequences-based
   residual-rights rule, expertise routing, the attention balance);
   `AGENTS.md` conformed; both templates to ~80 lines. Falsifier: no
   governing document references a tool this sweep removes.
3. **The three small tools, before their predecessors die**: the warn-only
   audit reporter (hash-picked sample, `Return:` and `pending` outcome
   fields), the ~100-line standalone board view (header-block parsing only,
   no judgments), the gauge classifier with a dated snapshot. Each lands
   with its build-table probe passing.
4. **The removals, in table order**: transition lint, pilot ledgers, slot
   ratchet; the suite-run ledger — **whose removal drops accepted
   `full-suite-interception` scope, so acceptance of this proposal is the
   Maintainer's explicit allowance for it**; then, only after chunk 3's
   probes pass, the lifecycle CLI and planner with twins and tests; then
   onboarding and foldback (the replacement channel is filing a Cairn issue
   — sister goodnight routines are updated accordingly); then the prose
   phase (PLANNING bankruptcy to one-line rows, dead doctrine sections,
   attic notes pointing into git history). The claim/link checkers are
   **kept and de-scoped** in the same phase: archives out of scope,
   file-top directives retired into checker-internal convention or one
   config, silent success. The intent system, board view, security stack,
   scaffold engine, and the `_resolve_interpreter` trust-root validator are
   **not touched** (any future validator removal takes its own Security
   Review).
5. **The install-contract phase** (the one careful step): fidelity manifest,
   gate manifest, and published `scaffold.py --manifest` updated; the
   differential-oracle gate re-anchored per its runbook (Maintainer-run).
   **This phase takes the declared Security Review before it lands.**
6. **Sister migrations, sequential, each MAINTAINER-GATED**: `modflow_tools`
   first, `lhm` only after modflow is green. Per repo: discovery beyond the
   manifest (tracked command references, installed-file provenance, ignored
   operational state and hooks — e.g. the gitignored interpreter binding —
   and project-owned routines), a positive probe for every retained or
   replaced command, that repository's own verification green, then the
   Maintainer's sign-off fires the chunk. Retired modules are removed from
   the sister trees; nothing is frozen or deprecated.

## Evidence / verification plan

Per chunk: the build-table probe, run and recorded. Sweep-wide falsifiers:
the dangling-reference grep over governing surfaces (confirmed against the
pre-change tree, where it matches); the suite green and re-timed after each
removal phase (target: inner loop ≈ 2 minutes with security release-only);
`security_check.py` byte-identical throughout. Prose passes the de-scoped
claim/link/neutrality gates. The archive line of this proposal will state
`Return:` against the attention it asked above.

## Signals the change is wrong

* A build-table probe fails after its removal phase — restore first, then
  re-plan; never patch forward around a lost function.
* A sister routine breaks post-migration — the per-repo discovery missed a
  dependency class; stop, fix, and re-run that sister's full verification
  before proceeding.
* The constitution rewrite grows past ~200 lines — the container is being
  rebuilt in place; stop and re-read the strategy note's ratchets.

## Reviewer brief

External, one round, on the deliberate lane. The design was reviewed twice
in the strategy note; review *this contract* for faithfulness and execution
safety: (1) does any chunk delete a producer before its build-table
replacement's probe exists; (2) does the manifest procedure actually reach
the ignored-state and project-owned-routine classes the second strategy
review demonstrated; (3) is the suite-ledger allowance stated clearly enough
that the Decision grants it knowingly; (4) name anything in the build table
this contract silently drops.

## Review -- GPT-5.6-Sol (External) -- 2026-08-25

**Model**: GPT-5.6-Sol
**Tier**: External
**Findings**: raised (4 blocking)

Reviewed commit: c29c9c976e5731bbdfea58d87ab2461a3be969df
Target: the complete proposal (Origin through Reviewer brief), checked against
the authoritative build table at 570fedbc91d108564f6fc3135fd7655cd2d42f1f
and the current installer, attestation, security-scan, and claim-check contracts
Prior findings: none
Assurance path: high-assurance

### Verdict

**REVISE.** The direction is sound, the suite-ledger allowance is explicit,
and the sister-repository discovery reaches the ignored-state class the
strategy review found. The execution contract is not safe yet. In particular,
it schedules installed-source deletion before the registries that publish those
sources are changed, and it puts its central inventory after plan review rather
than inside the material a reviewer can inspect. Those are repairable ordering
problems, not objections to the subtraction.

### Steelman

This is unusually disciplined for a deletion proposal. It builds the three
small replacements before retiring their predecessors, uses a per-file account
rather than trusting a headline line count, names the accepted scope reduction
plainly, makes sister migration sequential and Maintainer-gated, and says to
restore rather than patch forward when a promised function disappears. The
minimum-product boundary in the strategy note remains recognizable after the
sweep. I found no reason to preserve the old lifecycle machinery as a whole.

### Findings, ranked by hard-to-undo harm

* **[SSP-1] The proposed phase boundary leaves the install contract broken.**
  Chunk 4 deletes the lifecycle, onboarding, foldback, and metrics sources;
  Chunk 5 updates the install contract. Today those sources are still published
  from `bootstrap/_scaffold/config.py`: lifecycle files by
  `_SKILLS_MAPPINGS` (lines 579-592), onboarding by
  `_ALWAYS_ON_MAPPINGS` (lines 667-708), and metrics/foldback by
  `_MODULE_MAPPINGS` (from line 737). `install_manifest()` consumes all three
  registries (`bootstrap/_scaffold/install.py`, lines 1477-1516). Concrete
  counter-example: in a clean export of the reviewed commit I moved only
  `templates/modules/default-on/onboarding_activate.py` aside and ran
  `python -m pytest bootstrap/tests/test_manifest.py::TestInstallManifest::test_manifest_sources_all_exist -q`;
  it failed because the published manifest still named the missing source.
  Therefore the statement that the scaffold engine is not touched is false for
  the accepted inventory. Co-commit each installed-source removal with its
  owning registry row, published/fidelity/gate-manifest consequences, lockfile
  and upgrade expectations, and directly affected tests; require a green fresh
  scaffold at every such commit. The Security Review must clear the exact
  registry edits before the first one lands, not after a source-only removal.
  The plan must also name the separate AST-baseline ceremony: changing
  `_SKILLS_MAPPINGS` or `_MODULE_MAPPINGS` is self-service only under the
  runbook's one-change preconditions, while `_ALWAYS_ON_MAPPINGS` is not in
  `_ast_attest._UPDATE_ALLOWLIST` and therefore requires the Maintainer-run
  direct-correction path. The differential gate re-anchor in §5 does not cover
  that second trust artifact.

* **[SSP-2] The safety inventory arrives after the decision that needs it.**
  The proposal delegates its scope to an inline-revised strategy note, without
  a commit pin, then schedules the per-file manifest as implementation Chunk 1.
  Plan review therefore cannot check the actual deletion inventory, twin
  pairing, or per-file replacement before approving the plan; later edits to
  the strategy note can also change what “the table governs” means without a
  proposal revision. Put the per-file/per-function manifest in the reviewed
  plan (or in the proposal's complete revision), pin its strategy basis to
  `570fedbc91d108564f6fc3135fd7655cd2d42f1f`, and make every implementation
  chunk a closed subset of that reviewed inventory. Also carry the table's
  first dependency as an explicit fence: the `convergent-lifecycle` plan is
  currently `awaiting-code-review`, so no constitution rewrite or subtraction
  should execute until its code review has cleared and any resulting corrections
  are in the basis the manifest inventories.

* **[SSP-3] The claim-checker contract still contains an undecided design.**
  “Checker-internal convention or one config” names two materially different
  public contracts. The current tree has 112 Markdown files containing
  `claim-check-allow`; the accepted `claim-check-exemption-hygiene` proposal
  retained that directive as a rare false-positive escape hatch after its
  removal exposed 124 reports across seven artifacts at that proposal's
  snapshot. The new strategy may legitimately supersede that choice, but this
  proposal says it adds no design and never chooses the replacement. Before
  Decision, select one mechanism and state: whether archives are excluded only
  from bulk checks or also from direct invocation; how a real heuristic false
  positive or forward reference is represented; where any shared config lives,
  its schema and adopter portability; and what happens to all existing
  directives. Pin it with behavioral falsifiers: a broken live path still
  fails, an archived artifact has the chosen direct/bulk behavior, a legitimate
  exception works, and an unused exception cannot silently broaden the check.
  “Success is silent” alone cannot distinguish a correct empty result from a
  disabled detector.

* **[SSP-4] Byte-identical security code does not prove byte-equivalent security
  coverage.** `bootstrap/security_check.py::scan_targets()` derives its shipped
  executable set from `_MODULE_MAPPINGS`, `_ALWAYS_ON_MAPPINGS`, and the
  published manifest (lines 683-717). Those inputs necessarily change during
  this sweep even if `security_check.py` remains untouched. Its byte identity
  therefore checks the wrong property and can stay true while executable scan
  coverage shrinks incorrectly. Replace that sweep-wide check with a set
  comparison between the post-removal shipped verbatim Python surface and
  `scan_targets()`, plus a positive-control mutation proving that one unexpected
  shipped executable makes the check fail. Run the release scanner after each
  registry-removal commit, and record the canonical full Boundary-B suite and
  neutrality/redundancy pair after the final install-contract commit.

### Coverage

**Covered:** the proposal in full at the reviewed commit; the strategy build
table and its dependency order; source-to-installer registration through
`_SKILLS_MAPPINGS`, `_ALWAYS_ON_MAPPINGS`, `_MODULE_MAPPINGS`, and
`install_manifest()`; AST re-anchor authority in
`bootstrap/AST_BASELINE_RUNBOOK.md` and
`bootstrap/tests/_ast_attest.py::_UPDATE_ALLOWLIST`; dynamic release-scan target
derivation in `bootstrap/security_check.py::scan_targets`; current claim-check
directive semantics and the accepted exemption-hygiene contract; current
artifact state through `python tools/lifecycle_planner.py board --compact`; and
the isolated missing-source falsifier reported in [SSP-1]. I also confirmed the
proposal file is byte-unchanged from `c29c9c9` before editing this review.

**Not covered / low confidence:** I did not run the full suite (there is no
implementation to verify), execute either sister migration, enumerate the
eventual 61k-line per-file deletion set, or perform the Security Review. I did
not independently re-derive the 61k-line total because the proposal correctly
makes the reviewed per-file manifest the eventual exact account. I treated the
soon-to-be-retired lifecycle parser's preferred review-field spelling as
non-substantive; the plain-language Security Review obligation in §5 is clear.

**Second-round recommendation:** recommended after revision. The next pass can
be narrow: verify the reviewed per-file manifest and atomic commit partition,
the single chosen claim-check contract, the convergent-plan fence, and the
Security/AST ceremonies. The Maintainer decides whether to spend that pass.
