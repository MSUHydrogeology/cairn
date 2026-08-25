# The subtraction sweep: execute the refocus, then bring the sisters into compliance

**Author**: Claude (Strategy)
**Model**: Fable 5
**Date opened**: 2026-08-25
**Status**: awaiting-review
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
