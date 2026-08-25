# The subtraction sweep: execute the refocus, then bring the sisters into compliance

**Author**: Claude (Strategy)
**Model**: Fable 5
**Date opened**: 2026-08-25
**Status**: accepted
**Assurance path**: high-assurance — added by the scribe at the Decision; the
field is still live doctrine (`convergent-lifecycle`'s own accepted header
carries one, and `Lane:` is defined there only as `Lane: standard`, the
change-note discriminator). It is a label on a fact nobody disputed, not a gate.
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

## Response + Revision 1 -- Claude -- 2026-08-25

All four findings **accepted**; each was reproduced or source-verified before
acceptance (`_SKILLS_MAPPINGS` at `config.py:586`, `_ALWAYS_ON_MAPPINGS` at
`:689` and absent from `_ast_attest._UPDATE_ALLOWLIST`; `scan_targets()`
deriving from the registries at `security_check.py:683-717`; 112 files
carrying `claim-check-allow`; the convergent-lifecycle plan at
`awaiting-code-review`).

| finding | disposition |
|---|---|
| SSP-1 | **Accept.** The claim "the scaffold engine is not touched" was false for the accepted inventory — the registries publish what chunk 4 deletes. Withdrawn; replaced by atomic source+registry commits, the Security Review moved ahead of the first shipped-file removal, and the AST-baseline ceremony named (§4–5 below). |
| SSP-2 | **Accept.** The inventory moves inside the reviewed material: the strategy basis is pinned by commit, the per-file manifest becomes a deliverable of the *plan* (checked at plan review), every chunk is a closed subset of it, and the convergent-lifecycle code-review fence is explicit (§1). |
| SSP-3 | **Accept, and the design is now chosen** (author's call — implementation detail): `cairn-internal-ref-allow` retires into checker-internal knowledge of the doctrine-citation convention (this kills the repeated file-top boilerplate, which was the Maintainer's actual complaint); `claim-check-allow` survives as the sole, rare inline escape hatch per the accepted exemption-hygiene precedent; archives are excluded from bulk scans and labeled informational on direct invocation; a directive that matches nothing draws a stale-exemption warning. Four falsifiers pinned (§4). |
| SSP-4 | **Accept.** Byte-identity checked the wrong property. Replaced by a set comparison — shipped verbatim Python surface vs `scan_targets()` — with a positive-control mutation, the release scanner after each registry commit, and the canonical full pair after the final install-contract commit (§5). |

### Withdrawn / superseded commitments

* *"The … scaffold engine … [is] not touched"* — false for the registries;
  withdrawn (SSP-1). The engine's *logic* is untouched; its **registries are
  edited under ceremony**.
* The chunk 4 → chunk 5 ordering (delete sources, then fix the contract) —
  superseded by atomic per-source commits (SSP-1).
* The manifest as implementation Chunk 1 — superseded: it is plan-review
  material (SSP-2).
* *"checker-internal convention or one config"* — the undecided disjunction
  is withdrawn; the design is chosen (SSP-3).
* *"`security_check.py` byte-identical throughout"* as a coverage guarantee —
  superseded by the set comparison (SSP-4).

---

## THE COMPLETE CURRENT CONTRACT (Revision 1)

Supersedes the opened Proposal, Evidence, and Signals sections in full.
Header fields and Origin stand, with one correction: **Touches** gains
`bootstrap/_scaffold/config.py` (the three install registries) and the
AST baseline. **Basis pin**: this contract executes the strategy note's
build table **as of commit `570fedb`**; later note edits do not change this
proposal's scope without a revision here.

### 1. Fence, then manifest — nothing deletes before both

No chunk of this proposal executes until the `convergent-lifecycle` plan's
code review has cleared and any corrections from it are folded into the
basis. The **per-file / per-function manifest** is authored *in the derived
plan* and checked at its (Internal, security) plan review: every file, the
property removed, its replacement or the explicit decision the property
ends, its registry row, its twins and tests, and its commit grouping. Every
implementation chunk is a closed subset of that reviewed inventory.

### 2. The constitution rewrite

As opened: `dev/agent_collaboration.md` to ~150 lines around the accepted
lifecycle; `AGENTS.md` conformed; both templates to ~80. Falsifier: no
governing document references a tool this sweep removes.

### 3. The three small tools, before their predecessors die

As opened: the warn-only audit reporter (hash-picked sample, `Return:` and
`pending`), the ~100-line standalone board view, the gauge classifier with
dated snapshot — each landing with its build-table probe passing.

### 4. The removals — atomic with their registries (SSP-1), checkers de-scoped by the chosen design (SSP-3)

Cairn-internal removals (transition lint, pilot ledgers, slot ratchet; the
suite-run ledger, **whose accepted-scope allowance is granted by this
proposal's Decision**) proceed in table order after §3's probes pass.
**Every installed-source removal is one atomic commit** carrying: the source
files, their owning registry rows in `bootstrap/_scaffold/config.py`, the
fidelity/gate/`--manifest` consequences, lockfile and upgrade expectations,
and the directly affected tests — with a **green fresh scaffold install**
recorded per commit. Registry edits to `_SKILLS_MAPPINGS` and
`_MODULE_MAPPINGS` use the AST runbook's self-service path under its
one-change preconditions; **`_ALWAYS_ON_MAPPINGS` is not in the AST
allowlist, so its edit is the Maintainer-run, dry-run-verified direct
correction — a MAINTAINER-GATED step**. Foldback retires into "file a Cairn
issue" (sister goodnights updated); onboarding removed; prose phase as
opened. Claim/link checkers: the chosen design above, pinned by four
falsifiers — a broken live path still fails; an archived artifact is
excluded from bulk scans and labeled informational when invoked directly; a
legitimate `claim-check-allow` still works; a directive matching nothing
draws a stale warning (so an unused exemption cannot silently persist).
Untouched: the intent system, board view, security stack, scaffold engine
*logic*, and the `_resolve_interpreter` validator.

### 5. The install-contract ceremony — before, not after (SSP-1, SSP-4)

**The Security Review clears the exact registry-edit plan before the first
installed-source removal lands.** The differential-oracle gate re-anchor
(Maintainer-run) and the AST-baseline handling accompany the registry
commits they belong to, not a later phase. Security coverage is proven by
**set comparison, not byte identity**: after each registry commit, the
shipped verbatim Python surface equals `scan_targets()`'s derivation, with a
positive-control mutation (one unexpected shipped executable must fail the
check) recorded once; the release scanner runs after each registry-removal
commit; the canonical full suite and neutrality/redundancy pair run after
the final install-contract commit.

### 6. Sister migrations — as opened

Sequential, each MAINTAINER-GATED: `modflow_tools`, then `lhm` after modflow
is green; per-repo discovery beyond the manifest (tracked references,
provenance, ignored state and hooks, project-owned routines), positive
probes per retained/replaced command, native verification, Maintainer
sign-off fires each. Retired modules removed from sister trees; nothing
frozen.

### Evidence / verification plan

Per chunk: the build-table probe, run and recorded. Sweep-wide: the
dangling-reference grep (instrument confirmed pre-change); suite green and
re-timed per removal phase (target ≈ 2 minutes inner loop); §5's set
comparison and ceremonies; prose through the de-scoped gates. This
proposal's archive line states `Return:` against its header's attention
balance.

### Signals the change is wrong

As opened, plus: a fresh scaffold install fails at any atomic
source+registry commit — stop and restore, never patch forward; and any
registry edit found outside its declared ceremony path.

### Reviewer brief (round 2, narrow, if the Maintainer spends it)

Verify closure only: the manifest-in-plan and atomic commit partition
(SSP-1/-2), the single chosen claim-check contract and its four falsifiers
(SSP-3), the fence on the convergent-lifecycle code review (SSP-2), and the
set-comparison ceremony (SSP-4).

## Decision -- Anthony Kendall (Maintainer) -- 2026-08-25

### Preamble -- findings at the Decision

Recorded by the scribe at the Maintainer's instruction. Only items that survive
the sweep are here: an earlier draft of this preamble carried three findings
about conformance to `lifecycle_planner.py`, and the Maintainer struck them by
asking the right question -- *the tools doing the checking are the tools being
dismantled.* That correction is item 4, and it is the most useful thing in this
section.

**1. The ~61k figure is an estimate, not a verified account.** No one has
derived it: the External reviewer explicitly declined ("I did not independently
re-derive the 61k-line total"), correctly deferring to the per-file manifest.
Scribe's magnitude check, 2026-08-25: the planner twins plus the lifecycle CLI
are 16,616 lines and the lifecycle test modules 16,799, before onboarding,
foldback, metrics, or the prose phase -- so the order of magnitude is plausible
and nothing more. **Treat 61k as a headline until the manifest lands**, and do
not let it appear in a published claim before then.

**2. The plan review is the load-bearing moment of this entire sweep.** It is
the last point at which the deletion inventory is inspectable *while the thing
being deleted still exists*. §1 puts the per-file/per-function manifest there
deliberately; §5's Security Review obligation is stated in prose, which is what
a human reviewer reads, and prose is the right carrier because the parser that
would otherwise express it is itself on the removal list. Spend the attention
there rather than on a second proposal round.

**3. `Assurance path: high-assurance` was added to the header at this
Decision.** The field remains live doctrine and had been dropped in favour of
`Lane: deliberate`, which is not a defined proposal field. It is a label on an
undisputed fact -- the header already named the install contract, the reviewer
recorded high-assurance, and §5 declares a Security Review -- so it changes no
obligation. Recorded so the addition is visible rather than silent.

**4. Findings against retiring machinery are not findings.** Verifying an
artifact's conformance to `lifecycle_planner.py` -- its scan, its predicates,
its field vocabularies -- stops meaning anything as this sweep proceeds, because
that instrument is part of what is being removed. Cairn's own checks are
advisory by the accepted `convergent-lifecycle` contract ("warn, never refuse"),
so they were never the thing producing safety in the first place. **The plan
review, the Security Review, and every code review in this sweep should anchor
findings in code behaviour, trust roots, and install-contract consequences --
the class the External review actually used**: the registries publishing what
chunk 4 deletes (reproduced with a named failing test), `_ALWAYS_ON_MAPPINGS`
being absent from `_ast_attest._UPDATE_ALLOWLIST` and therefore Maintainer-run,
and `scan_targets()` deriving coverage from those same registries. A reviewer
who spends a round on field spellings against a dying parser is doing the
ratchet the strategy note names, on the proposal that removes it.

### The Decision

**ACCEPTED as revised (Revision 1).** Authorization, quoted verbatim and
visually isolated:

> "Please scribe my decision as accept as revised."

**Accepted terms**: execute the strategy note's build table as of commit
`570fedb`, in dependency order -- the constitution rewrite; the three small
replacement tools before their predecessors die; the removals, each installed-
source deletion **atomic with its owning registry row** in
`bootstrap/_scaffold/config.py` and a green fresh scaffold recorded per commit;
the claim/link checkers kept and de-scoped on the chosen design; the install-
contract ceremony with its Security Review clearing the registry-edit plan
**before** the first removal lands, and security coverage proven by set
comparison rather than byte identity; then the two sister migrations,
sequential and each MAINTAINER-GATED. Nothing executes until the
`convergent-lifecycle` plan's code review has cleared.

**This Decision is also the Maintainer's explicit allowance for the accepted-
scope reduction** the suite-run ledger's removal causes to
`full-suite-interception`, as §4 states.

**`_ALWAYS_ON_MAPPINGS` remains a MAINTAINER-GATED edit** -- it is not in the
AST update allowlist, so its registry change is the Maintainer-run,
dry-run-verified direct correction, not self-service.

**Scribed by** Claude (claude-opus-5) on explicit Maintainer instruction. The
scribe wrote no part of the authorization quoted above; the preamble is the
scribe's own finding record, adopted into this Decision.
