# Plan: Test trust boundary

**Source proposal**: dev/proposals/archive/2026-10-28-codex-test-trust-boundary.md
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-28
**In brief**: Protect the tests that defend trust while reporting ordinary test changes without requiring a new trust anchor.

## Source proposal

The Maintainer accepted the narrower boundary and its recorded assurance loss at `cca436a9`. Blanket protection remains in force until a reviewed authority transition and Maintainer ceremony install the new boundary.

## Scope

Inventory tests and dependencies; bind a protected roster to the signed anchor; change manifest production, independent derivation, verification and both ceremony stages; test transition and steady state; update the runbook and high-risk rule. Retain existing script, shipped-module and fixture byte protection. Actual release skip, xfail and xpass outcomes still refuse.

**Reuse.** Search `bootstrap/tests/_gate_manifest.py` and `_gate_preflight.py` for `_frozen_files`, `produce`, `rederive_static_manifest` and reviewed transitions: these provide the collection, independent comparison and authority-closure path to extend. 

### Documentation / doctrine surface

`AGENTS.md` names protected tests and control machinery as high risk, without making ordinary tests high risk solely by location. Governing text states that the re-anchor verifier freezes named security and trust tests, records full collection, and holds on lost or newly skipped protected nodes. `bootstrap/REANCHOR_RUNBOOK.md` describes the actual human-triggered launcher and its checks. Route by `docs/DOCUMENTATION_PLAN.md`. All source and governing writes wait for model-floor and scoped-verification code reviews to finish.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1a | Factual inventory | Reviewed plan | Current dependency evidence in a plan-owned folder |
| C1b | Security classification | C1a; high-tier security judgment | Proposed exact roster and reasons |
| C1c | Approve classification | MAINTAINER-GATED: approve exact initial roster before narrowing | Maintainer's decision on roster |
| C2 | Implement and test | C1c approval | Authority, gate changes, tests and documentation |
| C3 | Independent code and security review | C2 committed and verified; before installation where current gates permit | Reviews and dispositions |
| C4 | Install initial authority | MAINTAINER-ONLY: existing reviewed transition and re-anchor/root approval | Signed anchor and ceremony evidence |
| C5 | Prove steady state and close | C4; any required additional ceremony | Transition evidence, verification and archive |

## Acceptance criteria

### C1a — inventory

Enumerate every current Python test, controlling helper, import, dynamic loading path and fixture using current tree and actual dependency paths; identify existing protected scripts, shipped modules and fixture patterns. Include all current `bootstrap/tests/security_manifest.py` entries and the ten additional tests named in the accepted contract, not historical counts. Record evidence in a plan-owned folder.

### C1b–C1c — classify and approve

A high-tier agent proposes each protected or ordinary classification with reasons and roster. Include controlling `conftest.py`, `__init__.py`, `security_manifest.py`, `_ast_attest.py`, `_loader_proto.py`, current `_gate_*.py` and `_oracle*.py`, and gate/AST fixtures. The Maintainer approves the precise initial classification before narrowing. A new protected helper is frozen and, if it decides ceremony, joins authority closure; candidate labels cannot classify it.

### C2 — design and tests

Reviewed initial transition binds approved roster bytes; thereafter the trusted previous signed anchor supplies membership. Stage 1 passes it to candidate `produce`; trusted `rederive_static_manifest` checks identity against raw candidate bytes; stage 2 rebuilds the same roster and manifest. Preserve closure validation, static comparison and stage-2 manifest-byte equality. Missing/malformed roster or manifest, membership mismatch, collection error or invalid authority refuses. Protected bytes, node loss/rename and new skip/xfail markers HOLD. Ordinary edits, additions, deletions, renames and marker changes are visible nonblocking notes; new unrostered `test_*.py` emits `UNPROTECTED-NEW` with path and nodes. A new trust test stays unprotected until reviewed admission and re-anchor. Preserve full collection and actual release skip/xfail/xpass refusal.

### C3 — challenge

Real `produce` → `verify` → stage 1 → stage 2 tests prove approved first roster, prior-anchor steady state, candidate substitution refusal at each stage, and new ordinary and protective admission. Exercise separately protected and ordinary edits, additions, deletions, renames and new markers, plus missing/malformed inputs and collection errors; demonstrate an ordinary edit's lifecycle lane. Try one existing reviewed transition first. Only a measured old-checker refusal of a specific comparison permits the compatibility bridge and second transition; record failure and extra ceremony cost, without weakening old-anchor checks. Independent code and Security Reviews challenge evidence and execution-influence risk.

### C4–C5 — authority and steady state

The Maintainer alone authorizes and performs the applicable root and re-anchor ceremony under the existing runbook. Show initial transition and later steady state against the signed roster. No claim that the new boundary is active precedes installation. The ordinary-test pilot remains blocked until the delivered roster excludes its board test file. If neither route preserves old-anchor checks, stop for repair; do not waive ceremony.

## Scope delta

**Scope delta**: preserved against the accepted contract. The Decision accepted loss of blanket ordinary-test byte protection and HOLDs on ordinary node and marker changes. Ordinary code can influence protected collection or execution; this is not equivalent tamper resistance.

## Verification

Boundary A mapping: `bootstrap/tests/test_gate_manifest.py` owns produce/verify, protected and ordinary changes, roster/manifest refusal and collection errors; `test_gate_transition.py` and `test_gate_preflight.py` own authority closure, initial roster, static re-derivation, candidate substitution and transition; `test_gate_reanchor.py` owns real stage 1/stage 2, byte equality and steady state; `test_security_check.py` and `test_security_marker.py` own actual release skip/xfail/xpass refusal. Add cases in those families as needed. `test_reanchor_driver_disclosures.py`, `test_repin.py` and `test_repin_ceremony.py` cover ceremony surfaces; trace changed imports and fixtures for further owners. Run applicable claim, link, snippet, neutrality and prose-integrity gates. Trace the runbook's actual human-invoked launcher through functions and tests to protected HOLDs, full census and ordinary notes; do not claim the unused external verifier invocation runs.

Boundary B is **full** for gate manifest and trust ceremony surfaces. After the final implementation commit, run the scoped mapping and standing gates on a clean unchanged tree under `/Users/kendal30/conda_envs/lhm/bin/python3.13`; record commit, range, pre/post state, commands, counts, timing, non-pass dispositions and omissions. Set **Certified by**: pending until the next authorized certifying run supplies the full suite and quality pair. Reviewers independently falsify the evidence; they do not run the full suite.

## Plan review -- Codex (gpt-6.1-terra), Internal reviewer -- 2026-10-28

```
Reviewed commit: 1640a3595aec0d36e48e65de3d184aefb66b42d4
Target: opening plan, Source proposal through Verification
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** The plan follows the accepted narrower boundary, but its classification gate, verification mapping and governing-text criterion need clarification before it can reliably deliver it. -- plan C1, Verification and Documentation / doctrine surface; accepted proposal Complete current contract and S3.
2. **Best alternative.** Produce the inventory first, then gate narrowing on approval; use the existing reviewed transition first and the existing test families for a specific mapping. This keeps all accepted outcomes. -- plan Sequence and C3; `bootstrap/tests/test_gate_preflight.py:2111`; `bootstrap/tests/test_gate_reanchor.py`.
3. **What would show it wrong.** A real transition that cannot retain the old anchor's admission checks, a protected loss that passes, or ordinary maintenance still held after installation would defeat the plan. -- accepted proposal Complete current contract; `bootstrap/tests/_gate_preflight.py:3204`; `bootstrap/tests/_gate_manifest.py:671`.

**F1 -- Blocking: order the classification approval after its evidence exists.** C1 is itself marked Maintainer-gated to approve an exact classification, yet C1 is the chunk that produces the inventory and proposed roster. That makes the gate's input unavailable when the chunk starts. **Satisfier:** separate inventory and proposed classification from the approval fence, and put the fence after that evidence exists and before any narrowing; explicitly trace actual dependency paths including dynamic imports and fixtures. Retain the stated floors and give the Maintainer the precise classification to approve. -- plan Sequence and C1; `bootstrap/tests/test_gate_preflight.py:810`.

**F2 -- Blocking: map the accepted verification to owning paths.** Verification names several families and generic real-path and release probes, but does not map each invariant and public path to its test file or node. It omits the accepted proposal's named `test_gate_reanchor.py` and `test_security_check.py` from the listed families even though they own two-stage and actual release-outcome behavior. C3's broad “ordinary changes” also leaves the accepted separate edit, addition, deletion, rename and marker cases implicit. **Satisfier:** map the accepted cases and each stage to specific owning test files or nodes, including these families, and identify where new real-path cases will be added; retain the separate ordinary and protected cases and actual skip/xfail/xpass release probes. -- accepted proposal Tests required and Verification and withdrawal; `bootstrap/tests/test_gate_reanchor.py:94`; `bootstrap/tests/test_security_check.py:624`; plan C3 and Verification.

**F3 -- Blocking: carry the accepted governing statement.** The plan says the high-risk rule will name protected tests and machinery, but does not require the separate S3 statement describing what the re-anchor verifier freezes, records and holds. A correct roster rule alone would not satisfy that accepted documentation outcome. **Satisfier:** require that governing text convey the accepted S3 statement and that the runbook's actual human-triggered verifier invocation agrees. -- accepted proposal S3; plan Documentation / doctrine surface; `bootstrap/REANCHOR_RUNBOOK.md:173`.

**Coverage.** Covered claims and current behavior (#1: `bootstrap/tests/_gate_manifest.py:337`, `:402`, `:678`); production paths and refusal design (#2–4: `bootstrap/tests/_gate_preflight.py:1933`, `:2097`, `:3425`; `bootstrap/tests/conftest.py:421`); reuse, drift and lifecycle placement (#5–7: plan Reuse and Sequence; `bootstrap/REANCHOR_RUNBOOK.md:173`; `dev/plans/ordinary-test-maintenance.md` C1); accepted scope and satisfiers (#8–9: accepted proposal Complete current contract and findings above). Not covered: no test execution, complete dependency inventory, or future implementation; the separate Internal Security Review remains open.

## Plan review -- Codex (Sol, high), Internal Security reviewer -- 2026-10-28

```
Reviewed commit: 1640a3595aec0d36e48e65de3d184aefb66b42d4
Target: opening plan, Source proposal through Verification
Prior findings: none for this obligation
Assurance path: high-assurance
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** Yes, after the clarifications below. The accepted
   assurance loss is settled; the plan retains anchor-owned membership, independent
   derivation and Maintainer installation. -- Decision `cca436a9`; plan C2 and C4–C5;
   `bootstrap/tests/_gate_preflight.py:1933`.
2. **Best alternative.** Use the existing reviewed transition first; add the bridge only
   for a measured old-checker refusal. This preserves every accepted outcome with
   potentially one ceremony. -- plan C3; `bootstrap/tests/test_gate_preflight.py:2111`.
3. **What would show it wrong.** An approved roster replaced by candidate expectations,
   a protected loss passing, or ordinary maintenance still held after installation
   defeats the boundary. -- accepted proposal Complete current contract;
   `bootstrap/tests/_gate_manifest.py:671`; `bootstrap/tests/_gate_preflight.py:3425`.

**S1 — Blocking: make classification precede its approval fence.** Agree with ordinary
F1: C1 currently gates the chunk producing its own approval input. **Satisfier:** permit
evidence collection first, then have a high-tier agent make the security/trust
classification judgment, then seek Maintainer approval of the exact roster before
narrowing. Inventory current imports, dynamic loading, fixtures and controlling helpers,
not only filenames or the historical floor. Keep new unrostered test paths ordinary by
default; classify new protected helpers through the controlled roster/authority path,
never candidate labels. -- plan C1; `AGENTS.md` Model tier;
`bootstrap/tests/_gate_preflight.py:1815`.

**S2 — Blocking: specify the refusal and provenance tests.** Agree with ordinary F2;
“roster tampering” and “ordinary changes” leave consequential cases implicit.
**Satisfier:** map protected and ordinary edit/add/delete/rename/new-marker cases,
missing/malformed roster and manifest, collection errors, and actual release
skip/xfail/xpass to owning tests. Name real stage-1/stage-2 transition and steady-state
cases proving the first roster matches approved reviewed bytes and later membership
comes from the verified prior anchor; candidate membership substitution must refuse in
each stage. Include `bootstrap/tests/test_gate_reanchor.py`, `test_gate_preflight.py`
and `test_security_check.py`. Preserve closure validation, static comparison and stage-2
manifest-byte equality rather than bypassing them to demonstrate success. --
`bootstrap/tests/_gate_preflight.py:2097`, `:3204`, `:3425`;
`bootstrap/tests/test_security_check.py:684`.

**S3 — Blocking: connect the governing promise to the actual trigger.** Agree with
ordinary F3: require the accepted S3 governing statement and its exact human-run
verifier invocation. The current runbook's executable page calls the launcher; its later
reference describes external `verify --trusted-repo` as unused. **Satisfier:** trace the
delivered command through its real entry point and tests to protected HOLDs, full census
and ordinary notes; do not imply an automatic or existing invocation that does not run.
Keep narrowed mode inactive until the verified Maintainer ceremony installs it. --
accepted proposal S3; `bootstrap/REANCHOR_RUNBOOK.md:24`, `:228`; plan C4–C5.

**Coverage.** Claims, production paths, completeness and refusal (#1–4): cited producer,
static comparison, both stages and release tests; reuse, drift and placement (#5–7):
repeated Reuse search, launcher/runbook and S3; scope and satisfiers (#8–9): accepted
contract and S1–S3. Source files cited above are unchanged between reviewed commit and
`0ac350c0`. No pytest, mutation, complete inventory or future implementation validation
performed. This pass supplies the Security Review; the author must fold its findings
before implementation.

## Response to plan review -- Codex (gpt-6.1-terra) -- 2026-10-28

| Findings | Disposition | Operative cells |
|---|---|---|
| F1, S1 | Accepted | Sequence; C1a–C1c |
| F2, S2 | Accepted | C2–C3; Verification |
| F3, S3 | Accepted | Documentation / doctrine surface; Verification |

## Implementation log -- C1a factual inventory -- Codex (Luna, low) -- 2026-10-28

Measured the committed source tree `7f12a3f648c525446b041f523ae967b4f1d20cae`. A read-only archive collection with `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest --collect-only -q --disable-warnings bootstrap/tests` collected 5,479 node IDs across 129 test files; all 129 test files yielded nodes. The syntactic dependency scan covers all 141 Python paths under `bootstrap/tests`, resolving import candidates against 227 repository Python paths and recording fixture definitions/arguments, dynamic-load calls and path-like literals with exact matches separated from basename candidates. The exact node list and per-file hashes/references are in `dev/plans/test-trust-boundary/c1a-node-inventory.jsonl` and `c1a-dependency-inventory.json`.

The source manifest has 17 entries and the accepted contract adds 10 distinct test paths (27-floor union). Existing byte-freeze discovery yields 197 paths across its five source patterns; seven Python authority-closure members are joined by the runbook, launcher, re-anchor script and allowed-signers file (11 total). The inventory records the fixture files and excluded frozen paths. Positive controls found a collected `test_gate_manifest.py` node and the `conftest.py` manifest load. Collection only ran; no test body ran and `CAIRN_FULL_SUITE` was not set.

This is factual input, not a completed protected-set decision. The high-tier pass still needs to decide which import/collection/execution dependencies require protected membership beyond the already-required floor, how to treat path-level fixtures and helper modules, and which new trust helpers enter authority closure. The scan is syntactic and does not establish runtime reachability or security classification.

## Implementation log -- C1b proposed classification -- Codex (Sol, high) -- 2026-10-28

The exact proposed roster is `dev/plans/test-trust-boundary/c1b-proposed-roster.json`;
per-file reasons, source hashes, code witnesses, imports, dynamic-load expressions,
fixture candidates and census deltas are in
`dev/plans/test-trust-boundary/c1b-classification-evidence.json`. Both are
**proposed-not-approved** deliberation data, never candidate authority. Source:
`2ed8ddabc80c985ebc93171c7e628a7ec070459f`. Roster raw SHA-256:
`fc0d99bf361534cce21cb7923223d751589d0fc2e3207e27108327a8e8671803`.

The recommendation protects 78 test files and all 12 controlling Python modules,
and leaves 51 test files ordinary: all 141 current Python paths are classified,
including the 27-file required test floor. It preserves the seven fixture paths'
existing protection mechanisms, including both existing self/cascade exceptions,
and the 57 non-test frozen paths. No helper is introduced; the existing
11-member authority closure is unchanged. A future roster-deciding helper must
join it. The currently excluded intent-tool test is proposed for protected
admission because it contains hostile-link and temporary-write defenses; C2 must
reconcile its existing exception. These bytes install nothing.

The measured prospective frozen union is 147 paths versus today's 197: 51 ordinary
test files leave byte freezing and one previously excluded test joins. This may
reduce ceremony work for ordinary maintenance; no timing or assurance equivalence
was measured. Ordinary Python can still affect protected execution, and the
syntactic dependency inventory does not close that accepted influence risk.

The board file remains protected: its planted-encoder and linked-source cases
are actual defenses. The two-node maintenance pilot therefore remains blocked.
The evidence recommends one grouped Maintainer scope request: separately review
extraction of the two ordinary clusters to a new ordinary file, retaining the
security cases and helpers in the protected file, with a pilot-path allowance,
scoped fault evidence and applicable review/ceremony costs. No pilot edit or
substitution is authorized here.

C1c is **not ready**. Refresh the census, dependencies, hashes and exact proposal
after the model-floor and scoped-verification code reviews finish; only then
present the refreshed roster for approval. The approval fence has not been reached.

Verification used `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13):
collect-only on the named commit's archive returned 5,482 nodes in 129 files
(exit 0; 3.40 seconds), without running test bodies. Data assertions passed for
all 141 source hashes, the disjoint/exhaustive partition, required floor,
reconstructed node census, witness line bounds and roster hash. The existing
C1a node list plus the recorded delta reconstructs this census exactly. A
reader search across Python under tests, scripts and templates found no readers
of these plan/data names; a known gate-manifest import was the positive control.
Claim check and the plan-scoped prose/link/content check passed; neutrality had
zero failures and 43 informational exemptions. No executable snippet changed,
no full suite ran and certification remains pending. Shared unrelated edits
were excluded from the commit; measured source came only from the named commit.


## Filename maintenance -- Codex (Coordination) -- 2026-10-28

Maintainer naming instruction, verbatim:

> "Your plan docs aren't following the right naming convention. See the archive. Can you check if the template specifies this? If not, please modify it and the other templates (And shipped copies) to specify the date as part of the naming."

The filename now uses its original Opened date. Its document-owned evidence
folder, where present, uses the same dated stem and archives with the plan.
This is a path migration, not a scope or lifecycle change. Historical review
and evidence citations retain the paths valid at their named commits; current
link destinations and operative targets use the dated paths.

## Implementation log -- C1a factual inventory refresh -- Codex (Luna, low) -- 2026-10-28

Measured source `918638f5a11eb6985d0fa2cc26989b8a1d6541ca` in a plain archive. Python 3.13.13 collection-only returned 5,490 node IDs in 129 test files (exit 0; 3.95 seconds); no test body ran and no `CAIRN_FULL_SUITE` value was set. Compared with C1b's reconstructed 5,482-node census, 45 node IDs are added and 37 removed. The full node list is `dev/plans/2026-10-28-test-trust-boundary/c1a-refresh-918638f-nodes.jsonl`; current test/helper hashes, refreshed dependency facts, fixture hashes, and freeze paths are in `c1a-refresh-918638f.json`.

The current test tree still has 141 Python paths and 129 test files. C1b's per-path dependency evidence remains byte-current for 136 paths; five changed paths (`conftest.py`, `test_certifying_run_rule.py`, `test_model_tier_rule_ships.py`, `test_review_and_verification_rules_ship.py`, `test_verification_boundaries.py`) have refreshed hashes, imports, dynamic-load calls, fixture candidates, definitions and path literals. The five-pattern raw union has 201 paths; the current `_frozen_files` exclusions reduce it to the effective 197 paths, identical to C1a's list. Its four raw-only additions are the manifest fixture, cascade baseline fixture, phase-split intent test and phase-split intent template; all four are excluded. No freeze path was added or removed. C1b's proposed roster count remains 147 and `proposed-not-approved`; these facts do not approve a roster or classify paths.

The two named board-pilot nodes and their source locations/helpers are recorded in the refresh artifact. The node census, dependency sources and freeze implementation were checked against final HEAD `e9928009078b666b753b3b0502af14d9d2421922`; the two later commits changed only `doctrine/plans.md`, `doctrine/proposals.md` and the scoped-verification plan, with no `bootstrap/tests` path changes. Collection and static source inspection only; no test bodies, suite, gate or manifest production ran. The current plan remains open at its Maintainer ceremony fence.

## C1a inventory precision correction -- Codex (Luna, low) -- 2026-10-28

In `c1a-refresh-918638f.json`, `BASELINE_PATH` is removed from the helper list for the line-928 pilot node: that node does not read it. The adjacent line-892 anti-forgery node reads `BASELINE_PATH` at line 898; the constant is defined at line 723. No test or source code changed.

## Implementation log -- C1b refresh and C1c gate -- Codex (Sol, high) -- 2026-10-28

C1c now has its exact approval input. The current candidate is
`dev/plans/2026-10-28-test-trust-boundary/c1b-refresh-roster.json`, raw SHA-256
`02435039b9325950671a715df269194d345a9696d2ecb585c4818614ed868dee`.
The per-file reasons, source witnesses, dependency pointers, preserved mechanisms
and grouped pilot recommendation are in
`dev/plans/2026-10-28-test-trust-boundary/c1b-refresh-classification-evidence.json`.
This supersedes the earlier candidate for approval, without rewriting its record.
Both remain proposed, unapproved data; the signed boundary is unchanged.

The committed factual refresh (`c387dec7`, precision correction `833817bc`)
collected 5,490 nodes in 129 test files from source `918638f5`. Classification
source is `e9928009078b666b753b3b0502af14d9d2421922`; all 238 repository-Python,
effective-frozen, fixture and authority paths compared byte-identical across
those sources. The five changed Python paths since the first C1b pass were read;
no membership change follows: 78 protected test files, 12 protected controls and
51 ordinary files, including every required floor member. Of the collected
nodes, 3,954 are in protected files and 1,536 in ordinary files.

The effective current frozen set is 197, after four exclusions from the raw
201-path glob. The proposed union is 147, preserving 57 non-test frozen paths
and all seven fixture mechanisms. The ordinary-maintenance saving is prospective
and unmeasured; ordinary Python retains its accepted influence on protected execution.
No helper or authority member is added by this classification.

The board file stays protected because its linked-source and planted-encoder
checks are actual defenses. The separate pilot therefore cannot start as written.
The evidence recommends one grouped allowance: separately review relocation of
exactly the two named ordinary methods to a new ordinary file, preserving their
class/method names, then update the pilot's path. Leave its protected helpers and
all security cases in place; the adjacent anti-forgery method, not either pilot
method, reads the baseline fixture. This adds extraction, dependency/fault
evidence, independent reviews and the applicable protected-node transition and
Maintainer ceremony. No extraction or pilot deviation is authorized here.

Ordinary and Security code reads of scoped verification (`f19f4f53`, `9d813013`)
are complete; their required Maintainer frozen-file ceremony remains open under
the author's response `e9928009`. Roster approval clears neither that ceremony
nor this plan's C2–C4 implementation, review and installation fences. The next
move is the Maintainer's exact roster decision; related pilot scope belongs in
the consolidated decision batch.

Verification: canonical Python 3.13.13 checked all 141 source hashes, exact
partition/floor membership, code-witness bounds, 5,490 source-bound node IDs,
raw data/roster hashes and the effective/proposed freeze sets. Claim and
plan-scoped prose/link/content checks passed; neutrality had zero failures
and 43 informational exemptions. A reader search found no Python consumers of
the new data names, with a known manifest import as positive control. No new
executable snippet, collection, test-body run, certification or ceremony ran.

## C1c source refresh after checker description changes -- Codex (Sol, high) -- 2026-10-28

Use `dev/plans/2026-10-28-test-trust-boundary/c1b-roster-6cc95fa7.json`
for the next exact roster decision. Its raw SHA-256 is
`188fa76d82744be571bdc7ca91a43d605776b9df5ba0ac729e2cf22af66b8cc4`.
The source/frozen/dependency assessment is
`dev/plans/2026-10-28-test-trust-boundary/c1b-evidence-6cc95fa7.json`.
This candidate supersedes `fd1c820e` for approval; prior candidates and records
remain intact. No previous governing-text approval approved this roster.

Source is `6cc95fa7f2688bb63495af76f454ce13963b841e`. Against the previous
classification source `e9928009`, 236 of the 238 compared Python/frozen/fixture/
authority paths are byte-identical. The two exceptions are
`scripts/claim_check.py` and `templates/modules/default-on/claim_check.py`.
Their module descriptions changed; their ASTs excluding that first docstring
are equal, and the two current copies are byte-identical. The CLI description
is an explicit string rather than the module docstring. A positive-controlled
scan of seven named checker/owner consumers found no direct docstring reads;
this does not rule out unknown reflective consumers or prove whole-program
equivalence. Both files keep their existing frozen membership.

All 141 test/control sources and all 11 authority members are byte-identical.
The committed 5,490-node census and source-current per-file dependency evidence
are reused; no collection is repeated. The exact path classification stays
78 protected test files, 12 protected controls and 51 ordinary test files.
The effective frozen set is still 197 (201 raw matches minus four exclusions),
and the proposed union is 147. A fresh committed archive and the unchanged
producer's actual exclusion dictionaries confirm those sets. New hashes record
the two changed frozen sources; the manifest is untouched.

The governing-text record at `dd0b6bc1` reports 91 canonical Python 3.13.13
owner tests passing on `860481db`, and explicitly leaves the two checkers'
Maintainer frozen-file ceremony pending under C4. This refresh reads that
evidence; it neither repeats those tests nor clears their ceremony. Roster
authorization would permit C2 work only, retaining all review, installation
and ceremony fences. Ordinary Python's accepted influence on protected
execution remains a risk, and the protected board file still blocks its
separate ordinary-maintenance pilot. No classification conflict was found.

Verification used canonical Python 3.13.13 for source/hash/AST assertions, the
unchanged 141-path partition, 197 current frozen hashes, exact 238-path delta,
reused node-inventory hash and preserved fixture/authority counts. Claim and
plan-scoped prose/link/content checks passed; neutrality had zero failures
and 43 informational records. A search found no Python readers of the two
new artifact names, with a known manifest import as positive control. No
executable snippet, test body, collection, full suite or ceremony ran.

## C1c roster approval -- Maintainer, relayed by Codex (Terra) -- 2026-10-28

Maintainer authorization in chat, verbatim, in response to the request to approve
the linked list as the initial protected roster:

> Yes, I approve

The approved exact roster is
`dev/plans/2026-10-28-test-trust-boundary/c1b-roster-6cc95fa7.json`, committed
at `884e6d53b4f6ff6329a1148dc49a32294628109f`, raw SHA-256
`188fa76d82744be571bdc7ca91a43d605776b9df5ba0ac729e2cf22af66b8cc4`.
The approval permits the plan's C2 implementation; it does not install the
boundary, approve the pilot extraction, waive reviews, or authorize the
Maintainer-only authority transition and re-anchor. Existing frozen-file and
certification obligations remain open.

## Implementation log -- C2 -- Codex (Implementation Luna, low) -- 2026-10-28

Implemented the approved 90-path Python roster without changing its raw bytes
or SHA-256. Its seven protected fixtures and 57 preserved non-test paths remain
in the prospective freeze. The new roster artifact joins the fixed authority
closure, so the prospective frozen set is 148 paths (147 from the approved
union plus the roster artifact). The launcher's fixed list and hand-built
packet instructions now both name all 12 closure members. test_intents_tool.py
is frozen as approved while its existing phase-split handling remains in place.

Membership is supplied only by a verified prior signed anchor or the exact
approved roster bytes admitted by the reviewed initial transition. The first
transition tests pass without a compatibility bridge. Thereafter, the
candidate producer receives the trusted roster explicitly; trusted static
derivation compares roster identity and frozen/ordinary hashes to raw candidate
objects; stage 2 resolves the same roster from the observed anchor and retains
manifest-byte equality. The public check command also resolves from its prior
anchor. Missing or malformed anchor state refuses. With a valid pre-roster
anchor, the public data-only path keeps its broad legacy policy and cannot
introduce a candidate roster.

The tree-wide caller read used:

    rg -n "_trusted_roster_from_anchor|resolve_protected_roster|rederive_static_manifest|produce\(protected_roster|_frozen_files\(" bootstrap/tests/_gate_manifest.py bootstrap/tests/_gate_preflight.py bootstrap/tests/_gate_reanchor.py scripts/repin.py

The narrowed call paths are _gate_manifest.produce and verify;
_gate_preflight.gather_evidence, rederive_static_manifest,
check_static_manifest, check, stage1 and apply_now; and
_gate_reanchor.gather_evidence plus its data-only Stage B. The two
_gate_reanchor paths resolve from the previous signed manifest; Stage B
independently validates candidate evidence before constructing a commit or
advancing a ref. _frozen_files with no roster now means broad legacy policy,
never local candidate membership. The ordinary census is computed while the
raw object tree is still materialized. Existing ordinary additions, removals,
renames and marker changes remain visible notes; lost or changed protected
members remain HOLDs, and a new ordinary test_*.py is named in
ordinary_test_files and reported as UNPROTECTED-NEW.

Changes are in 979018d4, 26f65e18, 71ec71b3, cd6e1ddf, f66732ea
and bef293ff; the approved-roster count note is b97e71fd. The main
checkout's pre-existing untracked .claude/ and
dev/measurement/collision_log.md were not edited. No signed ref, manifest
authority installation, anchor, board pilot, push or waiver was changed.

## Implementation verification -- Codex (Implementation Luna, low) -- 2026-10-28

**Boundary B mode**: wide
**Certified by**: pending
**Tested commit**: bef293ffc65852c4513e65660c8a037eb5a0e8bf
**Reviewed range**: d866caef605e1dc7ae7a3b6a14a9269909513d67 to bef293ffc65852c4513e65660c8a037eb5a0e8bf
**Interpreter/runtime**: /Users/kendal30/conda_envs/lhm/bin/python3.13, Python 3.13.13
**Pre-run state**: clean detached worktree at the tested commit; git status --porcelain empty.
**Post-run state**: same HEAD and clean status after all commands.

Commands used PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest <paths> -q --tb=short in /private/tmp/cairn-c2-bef293ff; the two agent tests and the repin ceremony family ran with local signing/PTY capability enabled.

| Command | Exit | Outcomes | Elapsed |
|---|---:|---|---:|
| bootstrap/tests/test_gate_manifest.py | 0 | 23 passed | 24.11 s |
| bootstrap/tests/test_gate_transition.py bootstrap/tests/test_gate_reanchor.py | 0 | 25 passed | 5.56 s |
| bootstrap/tests/test_security_check.py bootstrap/tests/test_security_marker.py | 0 | 120 passed; 3 upstream deprecation warnings | 48.80 s |
| bootstrap/tests/test_repin.py | 0 | 106 passed | 102.14 s |
| bootstrap/tests/test_gate_preflight.py | 1 | 318 passed; 2 agent tests could not start /usr/bin/ssh-agent in the restricted run (exit 255) | 136.99 s |
| The two TestCandidateCodeCannotSignFromStageOne agent nodes, rerun with local agent access | 0 | 2 passed | 0.60 s |
| bootstrap/tests/test_reanchor_driver_disclosures.py | 0 | 21 passed | 5.31 s |
| bootstrap/tests/test_repin_ceremony.py with local signing/PTY capability | 0 | 130 passed | 417.97 s |

The scoped preflight family therefore passed 320/320; all listed mapped tests
passed, for 745 passing tests. No skips, xfails or xpasses were reported in
these runs. The initial restricted preflight non-pass was reproduced as an
environment denial and the same two nodes passed with local agent access. The
ceremony signing test's restricted-run passphrase failure also occurred on
pre-C2 commit d866caef under the same interpreter; it passed in the elevated
current run. No signing assertion or test was bypassed.

Plan-specific acceptance: first-transition and steady-state two-stage flows,
exact roster identity, static re-derivation, closure, candidate substitution,
legacy broad data-only promotion, protected and ordinary changes, actual
release skip/xfail/xpass handling, and the 12-member repin packet/runbook path
were exercised by the listed families. The old-checker comparison refused no
required first-transition case, so no bridge was added. The shared signed
anchor remains unchanged and still predates this implementation.

**Plan-specific acceptance commands**: the mapped test commands above. Claim,
link, snippet, neutrality and prose-integrity checks remain to be recorded
after this plan entry is checked. **Known omissions**: no full-suite or
certifying run; C3 independent code and Security Reviews remain pending; C4
Maintainer-only installation and re-anchor remain pending. No claim that the
narrow boundary is active is made.

## Implementation verification follow-up -- Codex (Implementation Luna, low) -- 2026-10-28

This record supersedes the preceding Boundary B result for the final
implementation. That earlier record describes `bef293ff`, before the actual
old-checker E7 comparison and bridge repair; its claim that no bridge was
needed is false for that candidate. Its test counts remain historical only.

**Boundary B mode**: wide
**Certified by**: pending
**Tested commit**: e1b8f8e9dd98bfa35acbb33a402be1e2d634cbe2
**Reviewed range**: d866caef605e1dc7ae7a3b6a14a9269909513d67 to e1b8f8e9dd98bfa35acbb33a402be1e2d634cbe2
**Interpreter/runtime**: /Users/kendal30/conda_envs/lhm/bin/python3.13, Python 3.13.13
**Pre-run state**: clean detached clone `/private/tmp/cairn-c2-e1b8f8e9`, HEAD e1b8f8e9; empty `git status --porcelain`.
**Post-run state**: same HEAD and empty status.

The mapped wide command was:

    PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_gate_manifest.py bootstrap/tests/test_gate_transition.py bootstrap/tests/test_gate_preflight.py bootstrap/tests/test_gate_reanchor.py bootstrap/tests/test_ceremony_review_report.py bootstrap/tests/test_reanchor.py bootstrap/tests/test_reanchor_driver_disclosures.py bootstrap/tests/test_repin.py bootstrap/tests/test_repin_ceremony.py bootstrap/tests/test_oracle_activation.py bootstrap/tests/test_security_check.py bootstrap/tests/test_security_marker.py -q --tb=short

Outcome: **939 passed, 146 failed, 3 warnings in 690.94 seconds**. No skips,
xfails or xpasses were reported in the aggregate output. Known environment
failures are `test_the_candidate_position_cannot_sign_through_a_live_agent`
and `test_the_same_key_signs_when_the_socket_is_present` in
`test_gate_preflight.py`: `/usr/bin/ssh-agent -s` exited 255 in this run. The
first visible report-family trace is
`test_ceremony_review_report.py::TestReportRolesAndSchema::test_the_schema_is_the_second_version_and_every_path_has_a_role`, refusing
because its synthetic prior anchor has no gate manifest. The same refusal
appeared across report, line-scan, and launcher consumers. Other failures were
listed across the mapped report and repin ceremony families, but the captured
tool output was truncated before a complete per-node ledger could be retained.
Terra follow-up is required to separate the remaining defects from dependent
fixture failures; this result does not establish Boundary B acceptance.

The exact final-SHA actual first-bridge E7 probe used P
`443de20f81169fabe36c4ca3cc620206f7850254` and candidate C
`e1b8f8e9dd98bfa35acbb33a402be1e2d634cbe2` in a separate clean isolated clone.
Real stage 1 ran against a generated, revalidated 12-member transition
manifest. Its broad prospective manifest omitted `protected_roster` and froze
the approved roster file. The stage-1 report scan digest and the sterile
Python 3.13 `-E -s -S` invocation of exact P `_gate_preflight.py scan-digest`
both returned
`1deb11c6fc93444b6367a35b2e6d0c91a9a656124adb3ea9bad93b7317157c70`; the
old checker exited 0, and the anchor ref was unchanged. The two-transition
integration fixture also exercised its simulated bridge checkpoint, extracted
that fixture P checker for the second E7 comparison, and completed stage 2's
exact prospective-manifest/report re-derivation. It signs only disposable
fixture commits and is not a real anchor installation.

The full mapped run's captured output was truncated; its aggregate is recorded
without claiming the omitted node-level dispositions. No full suite,
certifying run, root update, signature or Maintainer ceremony occurred. C3
independent code and Security Reviews, C4 installation/re-anchor and C5
steady-state approval remain pending. Do not treat the prospective narrowed
manifest as installed or the implementation as verified until Terra resolves
the mapped non-passes and a new final-commit Boundary B record succeeds.

## Maintainer operator clarification -- relayed by Codex (Implementation Terra) -- 2026-10-29

> I am fine with running something, it just has to meet the skills of this maintainer.

The earlier capability statement relayed in the same instruction was:

> I could definitely do a `reanchor` and a `repin` and confirm shas and enter my passphrase

The builder prepares the verifier command and its paths, and the reader checks
its provenance; the Maintainer compares the recorded hashes and runs it with the
key away. This does not authorize a ceremony or waive a HOLD.

## Maintainer script instruction -- relayed by Codex (Implementation Terra) -- 2026-10-29

> And remember we want scripts, not one-off commands!

This adds a reusable script deliverable to the human-run verifier outcome.
Its design and verification remain subject to the plan's independent code and
Security Reviews; the instruction does not authorize installation or waive a HOLD.
