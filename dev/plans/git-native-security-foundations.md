<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/dual-review.md doctrine/rationale.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Plan: let Git own what Git owns

**Source proposal**: `2026-08-10-codex-git-native-security-foundations`,
accepted at Revision 1 (`## Decision -- Anthony Kendall (Maintainer) -- 2026-08-10`).
**Status**: open
**Plan review**: required(**External** + **External Security Review**) — set by
the proposal, not by this plan. Two passes, one per clause; **one pass cannot
discharge both**.
**Last update**: 2026-08-11
**Opened**: 2026-08-11

## Source proposal

The proposal draws one line: Git owns object ids, trees, ancestry, signature
verification and ref transactions; Cairn owns *which* paths are protected, what
the accepted range is, when integrity is decisive, and what authorization
*means*. Custom code may constrain and interpret a Git command; it must not
reimplement a Git object algorithm. Concretely it retires per-commit signing in
favour of a **Maintainer-signed checkpoint bound to a canonical range-review
report**, moves blob hashing to `git hash-object --stdin`, adds `fsck` at the
two acquisition boundaries, takes the gate manifest to a v2 schema carrying
Git mode + oid *alongside* SHA-256, gives the custom refs reflogs and an atomic
publication contract, and ends candidate execution before the ceremony key is
loaded. This plan executes that decision; it does not re-litigate it.

## Scope

Eight chunks. The contract is **Revision 1** — R1-A through R1-F plus the R1
verification additions — which "replaces the corresponding terms in Context and
Sections A, B, C, D, F, Evidence, and Author-accounting". Where the original
sections and Revision 1 differ, **Revision 1 governs**, and this plan sequences
Revision 1.

**This is the local executable trust root.** `bootstrap/tests/_gate_preflight.py`
(1617 lines) and `bootstrap/tests/_gate_manifest.py` (453 lines) decide whether
a release ceremony proceeds. Every chunk below is a high-risk surface by
`AGENTS.md`'s own list, which is why the proposal set a two-clause review floor
and why the first-use bootstrap is an exact-byte ceremony rather than a merge.

### Sequencing — this plan is not independent of `review-efficient-lifecycle`

**They collide on the gate manifest, and the collision is not obvious.**
`review-efficient-lifecycle`'s Chunk I re-anchors the frozen set through
`bootstrap/REANCHOR_RUNBOOK.md` under manifest **v1**; this plan's Chunk D
migrates that manifest to **v2**. A re-anchor executed mid-migration would pin
a frozen set under one schema and verify it under another.

**Therefore: `review-efficient-lifecycle` completes its Chunk I ceremony and
Boundary B2 before this plan's Chunk D lands.** Chunks A–C, E and G here touch
no manifest byte and may proceed in parallel; D, F and H may not. If the two
plans must overlap further, that is a scope question for the Maintainer
(**M6**), not something an implementing agent resolves by re-ordering.

### Documentation / doctrine surface

**No published Cairn doctrine changes**, and the proposal's own rate-limit
section says so explicitly — the high-risk classification is what required the
proposal, not a doctrine amendment. What does change is Cairn's **project
security and release contract**:

* `bootstrap/SAFETY.md` — the Git-native division of responsibility, and the
  hook limitation (local hooks are bypassable and are not an authorization
  gate).
* `bootstrap/PROVENANCE.md` — signed release tags vs. internal signed
  checkpoints, kept distinct.
* `SECURITY.md` — the authorization model and its residuals.
* `bootstrap/REANCHOR_RUNBOOK.md` — the ceremony, reflog, publication, recovery
  and bootstrap commands.
* `dev/PLANNING.md` and the living security strategy — retire the obsolete
  signing-epoch tripwire and disposition [TRU-7].
* `CHANGELOG.md` — the behavior change.

**No adopter template gains mandatory commit signing.** `verify-ref.sh` remains
signed-release verification and gains only native incoming-object validation.

## Maintainer interventions — the complete list

**Read this before executing anything.** Everything in this plan is agent work
**except** what is listed here. This section is the single authoritative
enumeration: a stop not in this table is not a stop, and no chunk may introduce
one without adding a row here.

This plan has **more** Maintainer stops than a normal plan, and that is not
accumulated ceremony — it is the point. The subject *is* the trust root, and
three of the four scheduled stops exist because an agent must not be able to
authorize its own replacement.

### Scheduled stops

| # | Stop | Where | What the Maintainer does | What an agent must not do |
|---|---|---|---|---|
| **M1** | Two plan-review passes | Before any implementation | Obtains one **External** and one **External Security Review** pass | Begin implementation. One pass cannot discharge both clauses |
| **M2** | Focused exact-byte Security Review | After Chunk G, before H | Obtains a focused review of the exact `_gate_preflight.py`, `_gate_manifest.py`, runbook and imported authority bytes; it **records their SHA-256 set and the exact manual bootstrap invocation** | Treat the ordinary Code review as this review, or accept a prose inspection — R1 requires it to *execute* the range-report mutations, the v1/v2 differential corpus, the key-load sentinel and the bootstrap |
| **M3** | The exact-byte bootstrap ceremony | **Chunk H** | Confirms reviewed hashes **while the ceremony key is unavailable**, then loads the key, constructs the signed checkpoint, verifies the object and pinned principal, and advances branch + anchor in one expected-old `--no-deref` transaction | Perform any of it. R1-F: *"No author or implementing agent performs this step."* An agent does not load the key, construct the checkpoint, or move a Cairn ref |
| **M4** | Atomic publication + the [TRU-7] probe | **Chunk F/H** | Records a non-mutating capability probe **or** the first supervised publication result against the **real** remote, then publishes branch + `refs/cairn/gate-anchor` atomically | Push to `origin`. R1-D: *"No reviewer or implementation agent pushes to `origin` on the Maintainer's behalf, and no two-push fallback is allowed."* A local bare-remote test is necessary but **not sufficient** to close [TRU-7] |

**Everything else is agent work**: Chunks A–G's implementation and tests, the
v1/v2 differential corpus, every fixture, the runbook *text*, and Boundary B.

### Conditional stops

| # | Trigger | Action |
|---|---|---|
| **M5** | Chunk D's differential corpus shows v2 cannot preserve a v1 disposition, the `--trusted-repo` cross-check, addition semantics or a mode refusal | **Stop and retain v1.** Record why. The proposal is explicit: *"It does not ship a narrower manifest merely to reduce code."* |
| **M6** | A discovery needs its own contract, or this plan and `review-efficient-lifecycle` need to overlap beyond the fence above | Raise it as a **scope question**. Do not open a sub-plan and do not re-order the two plans |
| **M7** | Any byte changes after M2's exact-byte review | That disposition is **invalid**; M2 is re-taken. R1-F: *"Any byte change after the exact-byte review invalidates that disposition."* |

### Standing

**Pushing** is always the Maintainer's, per `AGENTS.md` — and here it is also
**M4**, because in this plan a push *is* part of the authorization ceremony.

## Sequence

```
A  the sterile launcher + repository-pinned hashing   [commit pending]
B  the canonical range-review report                  [commit pending]
C  checkpoint construction bound to the report digest [commit pending]
E  fsck at the two acquisition boundaries             [commit pending]
D  manifest v2  (blocked: see Sequencing)             [commit pending]
F  reflogs, atomic publication, runbook text          [commit pending]
G  the security/provenance documentation surface      [commit pending]
--- stable bytes -----------------------------------------------------
B1 Boundary B on the stable pre-review commit         [record]
CR independent External Code review                   [review]
SR focused exact-byte External Security Review        [M2]
H  the exact-byte bootstrap ceremony                  [M3, M4]
```

Orderings that are load-bearing rather than preference:

* **A first, always.** Every later chunk calls the sterile launcher; R1-B
  forbids any `hash-object` call outside it. Building B or D on a direct call
  would have to be unpicked.
* **B before C.** The checkpoint message binds the range-report digest, so the
  report must exist and be deterministic before anything can bind it.
* **D after `review-efficient-lifecycle`'s Chunk I and B2** — see *Sequencing*.
* **H last, and only after CR *and* SR.** This is the whole point of R1-F: the
  old anchored checker cannot authorize its replacement, so first use is a
  reviewed exact-byte ceremony, not a normal run.

**No chunk moves a Cairn ref.** R1-F step 1: land implementation and tests
*without* moving `refs/cairn/gate-anchor` or `refs/cairn/gate-authorization`.
That is an agent-side rule, not just a ceremony rule.

### Chunk A — the sterile launcher and repository-pinned hashing

| # | File | Change |
|---|------|--------|
| A1 | `bootstrap/security_check.py` | replace `_blob_oid` (`:342`, called at `:562`) with a call through the sterile launcher. **No `-w`, no path argument, no `--path`, no attribute/filter participation** |
| A2 | same + `bootstrap/tests/_gate_preflight.py` | the launcher itself: every hashing call takes an **explicit repository path**; there is no default repository. It establishes the path resolves to the operation's already-bound repository, obtains that repository's object format, and validates the returned full-width id against it |
| A3 | `bootstrap/tests/test_security_check.py` | SHA-1 **and** SHA-256 `hash-object --stdin`; an object-directory before/after check proving **no object is written**; explicit-repository success; and refusal on missing, non-repository, wrong-format and omitted-repository roots |

**The negative control is named by the proposal and must not be dropped**: the
outside-repository plausible-SHA-1 case. A missing or mismatched root must
**refuse**, never fall back to Git's process default SHA-1 — that fallback is
the defect this chunk exists to make impossible.

### Chunk B — the canonical range-review report

| # | File | Change |
|---|------|--------|
| B1 | `bootstrap/tests/_gate_preflight.py` | derive one canonical report from the trusted anchor and candidate HEAD, binding: schema id, anchor commit, candidate HEAD, candidate tree, branch ref and expected-old branch value; manifest schema and exact manifest SHA-256; the complete endpoint changed-path set; one classification per changed path; the complete sorted path list per class; and signed / unsigned / foreign-signed intermediate counts **as diagnostics, not verdicts** |
| B2 | same | the path set comes from sterile plumbing with exactly `-r --no-commit-id --name-only -z --no-renames` over the exact trees |
| B3 | same | **path identity is raw bytes.** Each canonical JSON entry carries the raw bytes as padded base64 plus a deterministic ASCII-only escaped display, and the implementation *verifies the display is a pure rendering of the bound bytes*. Ordering is by raw bytes. No locale, filesystem decoding, `quotePath`, rename detection or terminal rendering decides identity |
| B4 | same | duplicate, unclassifiable, or multiply-classified paths **refuse** |
| B5 | `bootstrap/tests/test_gate_preflight.py` | determinism; NUL-safe raw-byte ingestion; base64 identity; ASCII-only display escaping; rename/config independence; exhaustive one-class-per-path partitioning; complete outside-coverage list; and **digest change on every bound field** |

`_SIGNING_EPOCH` (`bootstrap/tests/_gate_preflight.py:64`) is **retired**, and
its six current monkeypatch sites in `test_gate_preflight.py` go with it. B5
carries the proof obligation R1 words precisely: *no* candidate-editable epoch
exists after this change, so the self-grandfathering attack is eliminated
rather than renamed.

### Chunk C — the checkpoint, bound to the report digest

| # | File | Change |
|---|------|--------|
| C1 | `bootstrap/tests/_gate_preflight.py` | `apply` **re-derives the report in memory** from the same exact refs immediately before construction. It neither reads nor trusts a handoff file |
| C2 | same | the constructed checkpoint's fixed audit message includes the report digest, anchor, candidate HEAD and candidate tree; `verify_constructed` re-parses the **commit object** and checks the exact message **before either ref moves** |
| C3 | same | branch and `refs/cairn/gate-anchor` advance together in one expected-old, `--no-deref` transaction |
| C4 | `bootstrap/tests/test_gate_preflight.py` | unsigned and mixed intermediate ranges reaching a valid checkpoint; invalid prior anchor signature; wrong principal; unsigned constructed checkpoint; wrong parent / tree / message; roster drift; direct-ref; stale expected-old; and `commit.gpgsign=false` |
| C5 | same | refusal when the report, anchor, HEAD, tree, manifest, confirmation or message **drifts** between derivation and construction |

### Chunk E — `fsck` at the two acquisition boundaries

| # | File | Change |
|---|------|--------|
| E1 | `bootstrap/security_check.py` | `git fsck --strict --no-dangling HEAD` **before** creating the detached execution tree. Failure is typed distinctly from a scanner finding and fails the release check **closed** |
| E2 | `bootstrap/container/verify-ref.sh` | fetch into the operator-created bare workspace with `-c fetch.fsckObjects=true`, then a strict reachable-object check **before** tag-name and signature verification |
| E3 | `bootstrap/tests/test_verify_ref.py`, `test_security_check.py` | strict-fsck success; a **malformed reachable-object negative control**; unchanged signed-name/signature behavior; proof candidate Git configuration cannot disable either object check; and distinct command-error reporting |

No command changes global or repository Git config. `receive.fsckObjects` is
documented as a forge/operator option because Cairn cannot enforce a remote's
configuration. **`fsck` proves structural object integrity — not authorization,
not safety, not signature validity** — and the result labels must keep those
apart.

### Chunk D — manifest v2 *(blocked; see Sequencing)*

| # | File | Change |
|---|------|--------|
| D1 | `bootstrap/tests/_gate_manifest.py` | `SCHEMA` (`:70`) → `cairn-gate-manifest/v2`. Each tracked frozen entry records committed Git **mode**, full Git **blob oid**, lowercase **SHA-256** over the exact blob bytes, and repository **object format** at the manifest level |
| D2 | same | cascade-mutable and phase-mutable records carry the same mode/oid/SHA-256 tuple while **retaining their existing non-HOLD dispositions** |
| D3 | same | `produce` (`:216`) takes mode and oid from the candidate commit's raw tree and computes SHA-256 independently over raw blob bytes; `verify` (`:311`) computes both and compares both plus mode; trusted-repository verification compares the same tuple and **refuses object-format mismatch** |
| D4 | `bootstrap/tests/test_gate_manifest.py` | the **v1/v2 differential corpus** — every v1 modification/deletion HOLD, addition disposition, cascade/phase exception and collection rule proven **at least as strict** under v2 — plus SHA-1/SHA-256 formats, mode changes, symlink/gitlink refusal, modified/missing/new tracked files, untracked gate files, object-format mismatch, trusted-repository verification, collection identity, and mutable-exception behavior, with independent single-field mutations |

**v2 does not ship unless D4's corpus passes.** A disagreement stops the
migration and retains v1 (**M5**). SHA-256 is *kept*, not replaced: Git oid
supplies repository-native identity and mode; SHA-256 preserves an independent
content digest. **Neither is authenticity** — the checkpoint signature and the
pinned roster own that claim, and no label here may imply otherwise.

pytest node ids, skip/xfail identities and mapping-symbol digests stay
domain-specific manifest data. Git has no equivalent; this chunk does not
flatten them into file identity.

### Chunk F — reflogs, atomic publication, runbook text

| # | File | Change |
|---|------|--------|
| F1 | `bootstrap/tests/_gate_preflight.py` | every successful local gate-anchor transaction uses `--create-reflog` with a fixed ceremony reason |
| F2 | `bootstrap/REANCHOR_RUNBOOK.md` | one `git push --atomic` with explicit refspecs for branch + `refs/cairn/gate-anchor`; **no silent two-push fallback**; incomplete publication reports and stops; then resolve both remote refs and record their object ids. Fresh-clone instructions use an explicit fetch refspec for the durable anchor |
| F3 | same | `refs/cairn/gate-authorization` is ceremony-local, **never published**, and deleted after promotion by its exact expected-old value; a failed deletion is reported as **unresolved ceremony residue**, never disguised as cleanup success |
| F4 | `bootstrap/tests/test_gate_preflight.py` | a stale expected-old abort changes **neither ref nor either reflog**; success identifies the ceremony in both reflogs; atomic push against a local bare remote with one ref rejected moves **neither** remote ref |
| F5 | same | runbook **literal-block tests**: `--create-reflog`, atomic publication, no partial-push fallback, remote verification, expected-old authorization-ref deletion, and the **absence** of `gate-authorization` from every push/fetch block |

Reflogs are local, mutable diagnostics for recovery and sequencing. They are
never described as authentication or tamper evidence, and **no decision
predicate consumes reflog content**. Receiving the durable anchor proves
availability, not authenticity.

### Chunk G — the security and provenance surface

| # | File | Change |
|---|------|--------|
| G1 | `bootstrap/SAFETY.md` | the Git-native division of responsibility; hooks are bypassable and are not an authorization gate |
| G2 | `bootstrap/PROVENANCE.md` | signed release tags vs. internal signed checkpoints, kept distinct |
| G3 | `SECURITY.md` | the authorization model and the accepted residuals, including the composed ceremony-key residual and its **expiry conditions** |
| G4 | `dev/PLANNING.md`, the living security strategy | retire the signing-epoch tripwire; disposition [TRU-7] only after **M4** |
| G5 | `CHANGELOG.md` | the behavior change |

**The residuals are part of the contract, not commentary.** G3 states plainly
that an unauthorized second person can create an unsigned intermediate commit
indistinguishable from an agent commit by signature status alone; that signing
authenticates a key holder, not a human; and that the posture is dated to the
solo trusted-contributor model and **expires** when the checkout is not solely
Maintainer-controlled, when another human gains ordinary write authority, or
when the ceremony key's availability cannot be separated operationally.

### Chunk H — the exact-byte bootstrap *(M3, M4 — Maintainer-only)*

R1-F's ordering, which no agent performs beyond step 1:

1. *(agent)* implementation and tests landed, **no Cairn ref moved**.
2. *(M2)* the External code review and the focused exact-byte External Security
   Review, with the SHA-256 set and the fixed invocation recorded.
3. *(M3)* start the reviewed preflight **with the ceremony signing key
   unavailable** to the process and its subprocesses; re-derive v2 evidence
   including pytest collection, the complete range report and every
   candidate-executing check; terminate all candidate subprocesses.
4. *(M3)* present the report, digest, reviewed-byte hashes and a **hard phase
   marker** stating that no later operation may execute or import candidate
   code; the Maintainer confirms while the key is still unavailable.
5. *(M3)* only then load the key. The already-running reviewed preflight
   executes fixed Git plumbing, constructs the checkpoint, verifies object and
   pinned principal, and performs the expected-old local transaction.
   **Crossing back into candidate collection or imports after this boundary
   refuses.**
6. *(M4)* atomic publication and remote verification; the authorization ref
   stays unpublished and is deleted locally by expected-old value.

| # | File | Change |
|---|------|--------|
| H1 | `bootstrap/REANCHOR_RUNBOOK.md` | the **fixed manual commands, written before code review**. R1-F: *"Chat-generated ceremony commands are not accepted evidence"* |
| H2 | `bootstrap/tests/test_gate_preflight.py` | the key-load phase sentinel: tests instrument **every** subprocess/import entry point and fail if a candidate-executing operation occurs after the marker — collection, imports, hooks, filters, subprocess launch |

**This sequencing removes simultaneous intentional key availability during
candidate collection. It is not containment**, and the plan does not claim it
is: candidate code run earlier on the same uncompartmented machine may exploit
the accepted host-access residual, leave persistence, or compromise a later
signing process. A separate evidence host or hardware-presence key is the
strengthening path, and neither exists today.

## Acceptance criteria

1. **No range-signature refusal.** Unsigned agent commits are the normal format;
   authorization occurs only at a signed checkpoint. Proven on the public path
   with a mixed range.
2. **The checkpoint binds the report.** A checkpoint cannot verify without the
   exact range-report digest in its message.
3. **Complete, unambiguous classification.** No changed path omitted, none
   multiply classified, and the outside-coverage list is complete rather than
   counted.
4. **v2 is at least as strict as v1**, proven by the differential corpus — or
   v2 does not ship (**M5**).
5. **Hashing cannot run without an explicit repository**, and no object is
   written.
6. **`fsck` failure cannot become CLEAN or a signature verdict.**
7. **Branch and anchor publish together or neither does.**
8. **No candidate execution after the key-load marker**, proven by sentinel,
   not by inspection.

* **Tests**: the four extended files named in Chunks A–F, plus standing gates
  for every touched surface. **Ceremony suites stay exhaustive** — the proposal
  is explicit that ordinary-suite runtime optimizations do **not** apply here,
  which fences this plan off `corpus-tier-cost`'s memo pattern.
* **Docs**: Chunk G's five surfaces, each confirmed updated rather than assumed.
* **Examples / smoke**: the public `check`/`apply` paths over an unsigned range
  in throwaway repositories, verified with Git against a pinned throwaway
  roster; a corrupted reachable object failing **both** acquisition paths before
  any signature or scanner claim; the two-ref stale expected-old transaction;
  atomic push with one ref rejected; and `scripts/check_cairn.py`, claim/link
  checks, the security lint and the gate-manifest/AST standing checks over every
  changed protected surface.

### Author-accounting — invariants, failure modes, edge cases

* **Invariant** — a signature never claims human authorship or review.
  *Enforced by* explicit output language plus the absence of any
  author/committer-name authorization fallback.
* **Invariant** — candidate configuration cannot steer a Git security command.
  *Enforced by* the single sterile launcher, all `GIT_*` removed, command-line
  config pins, and hostile-config fixtures.
* **Invariant** — path identity is raw bytes. *Enforced by* B3's base64
  round-trip and the display-is-a-pure-rendering check, with B5's escaping and
  rename/config-independence nodes.
* **Failure mode — the report is derived once and trusted twice.** *Closed* by
  C1: `apply` re-derives in memory and reads no handoff file.
* **Failure mode — a narrower v2 ships because it is tidier.** *Closed* by M5
  and D4; the plan retains v1 rather than weakening a disposition.
* **Failure mode — half-published state.** *Closed* by the atomic contract and
  F4's rejection test; there is no two-push fallback to disable.
* **Failure mode — the ceremony key is present while candidate code runs.**
  *Reduced, not closed*, and stated as such in G3. The phase boundary removes
  *simultaneous intentional* availability. It does not contain a host.
* **Public-path → test mapping**: the public paths are `check` and `apply` in
  `bootstrap/tests/_gate_preflight.py` and `main` in
  `bootstrap/tests/_gate_manifest.py` (`:416`), exercised through their real
  entry points by
  [`bootstrap/tests/test_gate_preflight.py`](../../bootstrap/tests/test_gate_preflight.py)
  and
  [`bootstrap/tests/test_gate_manifest.py`](../../bootstrap/tests/test_gate_manifest.py).
* **Known omissions at plan-open** — the [TRU-7] remote capability is
  **unmeasured** against the real remote; only **M4** can measure it, and a
  local bare-remote test is explicitly not sufficient. Chunk D's differential
  corpus is **unbuilt**, so "v2 is at least as strict" is an obligation here,
  not a finding.

## Verification

* **Boundary A**, per chunk: the tests named in that chunk's table plus standing
  gates for its touched surfaces. Any substantive change to
  `_gate_preflight.py` or `_gate_manifest.py` with effects this plan cannot
  bound runs the full suite.
* **Boundary B**, once, on a clean commit after the final implementation commit
  (Chunk G) and before code review: `python -m pytest bootstrap/tests
  --quality-gate-shuffle-seed=0` then `python scripts/quality_gate.py --sub
  neutrality --sub redundancy`, under the canonical interpreter, recorded as
  `## Implementation verification -- <agent> -- YYYY-MM-DD`. **The complete
  canonical suite runs once at this stable boundary** per the proposal.
* **Boundary C**: one independent External code review over that range — and
  separately **M2**, the focused exact-byte External Security Review, which is
  *not* discharged by Boundary C and must **execute** the range-report
  mutations, the v1/v2 differential corpus, the key-load sentinel and the
  bootstrap rather than inspect them.

Known at plan-open so a later reader does not mistake them for regressions:
`bootstrap/tests/test_ast_attest.py` carries pre-existing failures tracked to
other plans' `bootstrap/_scaffold/` changes, and `test_verify_ref.py` has a
full-suite-only order sensitivity that does not reproduce in isolation (67/67).
Neither is this plan's. An unexplained failure **inside the four files this
plan edits** is.

<!-- Each plan-review pass is its own dated H2 section appended below:

       ## Plan review -- <reviewer> -- YYYY-MM-DD

       **Tier**: <External|External Security Review>
       **Obligation**: <the exact clause from `Plan review:` this pass discharges>
       **Findings**: <none|raised>

     Two passes are required and one pass cannot discharge both clauses. -->

## Code review

*Filled in after implementation commits land.* One independent External pass
over the stable range, reviewer not the implementing agent — plus the separate
focused exact-byte Security Review (**M2**), which it does not replace.

## Lasting-truth migration

*Filled in at archive time.* Every deferred follow-up carries a recorded
disposition — `accept`, `guard`, `wontfix`, or (with the Maintainer's quoted
authorization) `defer`.
