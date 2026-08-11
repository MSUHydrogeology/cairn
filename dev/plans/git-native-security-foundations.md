<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/dual-review.md doctrine/rationale.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Plan: let Git own what Git owns

**Source proposal**: `2026-08-10-codex-git-native-security-foundations`,
accepted at Revision 1 (`## Decision -- Anthony Kendall (Maintainer) -- 2026-08-10`).
**Status**: executing
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

**M1 obligation state — CLEARED on both clauses, 2026-08-11:**

| clause | state | pass |
|---|---|---|
| **External** | **CLEARED** — SHIP, findings none, closing E1–E4 | Codex (GPT-5.6-Codex), round 2, `c06275a` |
| **External Security Review** | **CLEARED** — SHIP, findings none | Antigravity (Gemini 3.1 Pro), `ba44658` |

Structural independence holds on its own terms: the source proposal was authored
by Codex, this plan's executable mapping by Claude, and the security pass by a
third agent type that is neither. No pass reviewed its own author's work.

**What the security pass did and did not establish.** It audited the *plan
contract* — the sterile-context design against both `fsck.*` attack shapes, the
four guarded boundaries, the key-load phase ordering, the atomic publication
contract, and the B6/B7 classifier unification. That is the right activity for a
plan review, because there is no implementation to attack yet. It is **not** the
executing falsification obligation: that is **M2**, which R1 requires to *run*
the range-report mutations, the v1/v2 differential corpus, the key-load sentinel
and the bootstrap rather than inspect them. M1 clearing does not shrink M2.

**A tooling gap recorded here rather than forgotten now that it no longer
bites.** Measured on this plan at `1582803`, when only the External clause was
satisfied: with the status at `awaiting-plan-review`, `lifecycle_planner.py next`
reported `-> executing [ok]`. The gate attests that *a* conforming pass meeting
the floor landed — **not** that every declared clause has one; its own text says
*"conformance only — the tool attests that a tier was DECLARED, never that it
was true."* Both clauses are now genuinely cleared, so the mechanical result and
the contract agree today. On the next `required(A + B)` plan they may not, and
the row above — not the planner — is what a reader should trust.

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
| A4 | `bootstrap/tests/_gate_manifest.py` + `test_gate_manifest.py` | its **direct** Git subprocess calls (e.g. `merge-base --is-ancestor` at `:285`) come behind that module's guarded boundary. D3 requires this module to call `hash-object`; it must not be the one entry point that reaches Git unguarded |
| A5 | `bootstrap/tests/_gate_preflight.py`, `security_check.py` | **object-format-aware id validation replaces every fixed-width check** on a touched path — `_gate_preflight._resolve` (`:319`), `:1038`, `:1283`, and `security_check._head_commit` (`:271`) — validating against the already-bound repository object format instead of a literal 40 |
| A6 | `test_gate_preflight.py`, `test_security_check.py` | **SHA-256 public-path** tests: `check`, `apply`, and the release security entry point over a SHA-256 repository, not helper-level coverage only |

**The ownership model, stated because the plan previously implied one that does
not exist.** There is **one guarded launcher per executable boundary**, not a
single shared module. There are four boundaries and they are genuinely
independent processes:

| boundary | today | contract |
|---|---|---|
| `bootstrap/security_check.py` | `_git_at` (`:208`), `_git` (`:226`), `_git_bytes_at` (`:231`) — three launchers | consolidated; one guarded entry, text and bytes variants of the *same* guard |
| `bootstrap/tests/_gate_preflight.py` | `_run_git` (`:232`) / `_git` (`:255`) | already the closest to the target shape; becomes the reference |
| `bootstrap/tests/_gate_manifest.py` | **direct `subprocess.run(["git", …])`** | gains its own guarded boundary (A4) |
| `bootstrap/container/verify-ref.sh` | `wsgit()` (`:294`) | **its own explicitly tested shell boundary** — it does not and cannot consume a Python launcher |

Each boundary specifies, in its own module: the sterile environment, the config
pins, the repository binding, the read/write allowlist, and a **prohibition on
direct `subprocess` Git calls bypassing it**. Author-accounting's "candidate
configuration cannot steer a Git security command" is a claim about all four; an
implementation that satisfies each local test while leaving one boundary
unguarded would make that claim false while the suite stayed green.

**The negative control is named by the proposal and must not be dropped**: the
outside-repository plausible-SHA-1 case. A missing or mismatched root must
**refuse**, never fall back to Git's process default SHA-1 — that fallback is
the defect this chunk exists to make impossible.

**Why A5/A6 rather than declaring the ceremony SHA-1-only.** `_resolve` (`:319`)
refuses any id whose length is not 40, so in a SHA-256 repository Git returns a
valid 64-character HEAD and the public path fails *before* reaching the helpers
A3 tests. Declaring SHA-1-only would be honest but would contradict R1-B and
R1-C, which require validating the returned id **against the repository's object
format** and refusing object-format mismatch. Helper-only SHA-256 coverage must
not be presented as repository-format support.

### Chunk B — the canonical range-review report

| # | File | Change |
|---|------|--------|
| B1 | `bootstrap/tests/_gate_preflight.py` | derive one canonical report from the trusted anchor and candidate HEAD, binding: schema id, anchor commit, candidate HEAD, candidate tree, branch ref and expected-old branch value; manifest schema and exact manifest SHA-256; the complete endpoint changed-path set; one classification per changed path; the complete sorted path list per class; and signed / unsigned / foreign-signed intermediate counts **as diagnostics, not verdicts** |
| B2 | same | the path set comes from sterile plumbing with exactly `-r --no-commit-id --name-only -z --no-renames` over the exact trees |
| B3 | same | **path identity is raw bytes.** Each canonical JSON entry carries the raw bytes as padded base64 plus a deterministic ASCII-only escaped display, and the implementation *verifies the display is a pure rendering of the bound bytes*. Ordering is by raw bytes. No locale, filesystem decoding, `quotePath`, rename detection or terminal rendering decides identity |
| B4 | same | duplicate, unclassifiable, or multiply-classified paths **refuse** |
| B5 | `bootstrap/tests/test_gate_preflight.py` | determinism; NUL-safe raw-byte ingestion; base64 identity; ASCII-only display escaping; rename/config independence; exhaustive one-class-per-path partitioning; complete outside-coverage list; and **digest change on every bound field** |
| B6 | `bootstrap/tests/_gate_preflight.py` | the report **consumes the one canonical classification source** — `_gate_manifest._frozen_files()` (`:151`) plus the mutable registries and the manifest-artifact exclusion — rather than duplicating the policy. Name it in the code; a second classifier is the defect |
| B7 | `bootstrap/tests/test_gate_preflight.py` | the **cross-contract corpus**: report classes and manifest production/verification agree for existing frozen files, newly added gate files, cascade/phase mutable files, the manifest artifact, ordinary outside paths, and unsupported modes |

**B5 proves a partition; B6/B7 prove the partition is *right*.** Exhaustive
one-class-per-path says every changed path got exactly one label. It says
nothing about whether that label matches the policy that later decides HOLD,
mutable treatment or admission — and a total-but-wrong partition is the
dangerous case here, because the digest would bind the misdescription perfectly
and the Maintainer would sign an accurate-looking report of the wrong facts. The
concrete failure: a newly added gate path reported as *outside coverage* while
the checkpoint manifest admits it as *frozen*.

D4's v1/v2 differential corpus checks manifest dispositions against each other;
it is not connected to this report. B7 is that connection, and the raw-byte
identity tests in B3/B5 stay — they answer a different question.

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
**The original design was broken, and the break is demonstrated.** An earlier
draft ran `git fsck --strict --no-dangling HEAD` *in the candidate repository*
and promised a test that candidate config could not disable it. That property is
not achievable that way. Measured on git 2.53.0 against a reachable commit
object written with `hash-object -t commit -w --stdin --literally` and no
`author` line:

| disposition | fsck exit | verdict |
|---|---|---|
| default `--strict` | **1** | refuses, correctly |
| repo-local `fsck.missingAuthor=ignore` | **0** | **bypassed** |
| … plus launcher pin `-c fsck.missingAuthor=error` | **1** | pin wins |
| repo-local `fsck.skipList=<file with the oid>` | **0** | **bypassed** |
| … plus launcher pin `-c fsck.skipList=/dev/null` | **0** | **pin does NOT win** |
| sterile bare clone, no candidate `.git/config` | **1** | refuses |

**The two attacks are not equally severe, and the difference is the whole
finding.** A severity downgrade is single-valued, so a command-line `-c` pin
overrides it. `fsck.skipList` is **multi-valued**: `-c` *accumulates* rather
than replaces, so the candidate's entry survives every pin. You cannot
enumerate-and-pin your way out of it, and any design that tries is committing to
chase an evolving `fsck.*` family forever.

| # | File | Change |
|---|------|--------|
| E1 | `bootstrap/security_check.py` | the local object graph is checked from a **sterile repository/config context** — not by running `fsck` under candidate-local `fsck.*` policy. The last row above is the reference behavior. Failure stays typed distinctly from a scanner finding and fails the release check **closed** |
| E2 | `bootstrap/container/verify-ref.sh` | fetch into the operator-created bare workspace with `-c fetch.fsckObjects=true`, then a strict reachable-object check **before** tag-name and signature verification. This workspace has its **own** sterility contract, stated explicitly: it is operator-created, so its config is not candidate-controlled — but `wsgit` (`:294`) today neutralizes only `GIT_CONFIG_GLOBAL` / `GIT_CONFIG_SYSTEM`, and the contract must say what else is pinned and why the fetched repository cannot influence it |
| E3 | `bootstrap/tests/test_security_check.py` | **two independent negative controls, not one**: a severity downgrade (`fsck.missingAuthor=ignore`) and a `fsck.skipList` entry naming the malformed object. Each must leave the disposition unchanged. A single control passes under a design that defeats only the first |
| E4 | `bootstrap/tests/test_verify_ref.py` | the same pair against `fetch.fsck.*` for the fetch boundary, plus strict-fsck success, unchanged signed-name/signature behavior, and distinct command-error reporting |

**Neither `fsck.*` nor `fetch.fsck.*` from any candidate-controlled source may
change the disposition** — that is the acceptance property, and E3/E4 are its
falsifiers.

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
6. **`fsck` failure cannot become CLEAN or a signature verdict** — *and* no
   `fsck.*` or `fetch.fsck.*` setting from a candidate-controlled source can
   change the disposition, proven by **two** negative controls (severity
   downgrade and `skipList`), not one.
6b. **Report classes agree with manifest policy**, proven by the cross-contract
   corpus. A total partition is not sufficient.
6c. **Every touched object-id validator is object-format-aware**, and the
   SHA-256 evidence runs on the *public* paths, not only the helpers.
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

## Plan review -- Codex -- 2026-08-11 (round 1)

**Model**: GPT-5.6-Codex
**Tier**: External
**Obligation**: External
**Reviewed commit**: `9463f680fa556d10e52971a1389a221c32a5ee58`
**Reviewed plan blob**: `60bf7f565264f740bde9a7d5c2eb7023754d10ee`
**Assurance path**: high-assurance
**Findings**: raised
**Verdict: REVISE.** The plan preserves Revision 1's security decisions and its
Maintainer fences well, but it does not yet turn four repository-native claims
into an executable contract. The most important is demonstrated, not
hypothetical: the proposed local `fsck --strict` can be disabled by the very
candidate repository it is meant to check.

**Independence disclosure.** I authored the source proposal. Claude authored
this plan's executable mapping after Claude had already supplied the proposal's
different-agent External challenge, so this pass is an independent review of
the plan author and mapping, but not a fresh authorship-independent invention
of the source design. It discharges only the ordinary External plan-review
clause if its findings are later closed. It does not discharge the separately
declared External Security Review.

### [E1] HIGH -- `fsck --strict` still trusts candidate `fsck.*` policy

E1 and E3 require `git fsck --strict --no-dangling HEAD` in the candidate
repository and promise proof that candidate Git configuration cannot disable
the check. A sterile environment and the current style of command-line config
pins do not establish that property.

I created a reachable commit object with no `author` line. On Git 2.53.0,
default strict fsck refused it with `missingAuthor` and exit 1. With only this
candidate-local setting added, the same command and object exited 0:

```text
fsck.missingAuthor=ignore
```

A second candidate-local setting also made the malformed object pass:

```text
fsck.skipList=<candidate-controlled file containing the object id>
```

The skip-list case is particularly important to the proposed launcher design:
adding `-c fsck.skipList=/dev/null` did not override the repository value. Git
treated both as multi-valued and still skipped the object. Thus E3's requested
hostile-config test is good, but the plan has not selected a mechanism capable
of making it green without enumerating an evolving family incompletely.

**Required satisfier.** Bind a configuration-independent acquisition design in
Chunk E. The local candidate object graph should be checked from a sterile
repository/config context (or an equivalently complete mechanism), not by
running fsck under candidate-local `fsck.*` policy. Specify the separate
sterility contract for the operator-created fetch workspace. Add independent
negative controls for both a severity downgrade and `fsck.skipList`, and show
that neither `fsck.*` nor `fetch.fsck.*` from candidate-controlled sources can
change the disposition. The implementation choice belongs in the reviewed
plan because it changes the acquisition trust boundary.

### [E2] HIGH -- the "single sterile launcher" has no coherent owner

The sequence says every later chunk calls one sterile launcher, R1-B forbids a
direct `hash-object` outside it, and Author-accounting uses that launcher to
close candidate configuration steering. But A2 maps launcher work only to
`bootstrap/security_check.py` and `_gate_preflight.py`. D3 separately requires
`_gate_manifest.py` to call `hash-object`, while E2 is a shell entry point with
its own `wsgit` function. These are four independently executable entry points;
the plan names neither a shared owner nor one complete launcher contract per
boundary.

This is not cosmetic reuse. Today `_gate_manifest.py` has direct Git subprocess
calls, `security_check.py` has separate text/bytes launchers, and
`verify-ref.sh` neutralizes a different configuration set. An implementation
could satisfy each local test while leaving Author-accounting's global
invariant false.

**Required satisfier.** Choose and record the ownership model. Either add a
shared standard-library module that all Python entry points can safely load, or
state that there is one guarded launcher *per executable boundary* and specify
each one's environment, config, repository binding, read/write allowlist and
direct-subprocess prohibition. Add `_gate_manifest.py` and its tests to Chunk
A's mapping. Treat the shell fetch/fsck wrapper as its own explicitly tested
boundary rather than implying that it consumes a Python launcher.

### [E3] MEDIUM -- the report classifier has no semantic oracle

B5 proves that every changed path receives exactly one class. That proves a
partition, not that the class agrees with the manifest policy which later
decides HOLD, mutable treatment, or admission. The current policy source is
`_gate_manifest._frozen_files()` plus the mutable registries and manifest
artifact exclusion; the plan does not say whether B consumes those exact
decisions, the newly produced v2 manifest, or a duplicated classifier. D4's
v1/v2 differential corpus checks manifest dispositions but is not connected to
B's Maintainer-facing report.

A total but wrong partition is dangerous here: for example, a newly added gate
path could be reported as outside coverage while the checkpoint manifest
admits it as frozen. The report digest would bind the misdescription perfectly.

**Required satisfier.** Name one canonical classification source and make B's
report consume it. Add a cross-contract corpus showing that report classes and
manifest production/verification agree for existing frozen files, newly added
gate files, cascade/phase mutable files, the manifest artifact, ordinary
outside paths, and unsupported modes. Keep the raw-byte identity tests; they
answer a different question.

### [E4] MEDIUM -- SHA-256 coverage can pass below a failing public path

A3 and D4 require SHA-1 and SHA-256 repositories, but the plan does not account
for existing fixed-width object-id validators on the public paths.
`_gate_preflight._resolve` and `security_check._head_commit` currently require
40 hexadecimal characters. In a fresh SHA-256 repository, Git returned a valid
64-character HEAD and `_gate_preflight._resolve("HEAD")` refused it. Therefore
helper-level `hash-object` and manifest tests can pass while `check`, `apply`,
or the release security entry point fails before reaching those helpers.

**Required satisfier.** Either declare the public ceremony/release paths
SHA-1-only and describe the SHA-256 nodes as isolated compatibility groundwork,
or, preferably, replace every touched fixed-width validator with validation
against the already-bound repository object format and add SHA-256 public-path
tests. Do not present helper-only coverage as repository-format support.

### What reproduced

At the reviewed plan commit, `_gate_preflight.py` is 1,617 lines and
`_gate_manifest.py` is 453; the plan blob is unchanged at current HEAD.
`claim_check.py` reports no flags. `lifecycle_planner.py next` reports the plan
structurally sound and at `open -> awaiting-plan-review`. The cited
`test_verify_ref.py` isolation result also reproduces exactly: **67 passed**
under Python 3.13.13. The `review-efficient-lifecycle` collision is real: its
Chunk I still performs the v1 re-anchor and Boundary B2 follows it, so the
fence before this plan's Chunk D is correctly placed.

### Covered and not covered

**Covered**: exact plan bytes from `9463f68`; accepted Revision 1 and its prior
External review; current Git launchers and manifest classifier; strict-fsck
severity and skip-list attacks; SHA-256 public-path resolution; plan claims,
structure, cross-plan sequencing, and the isolated verify-ref suite.

**Not covered**: future implementation bytes, the full bootstrap suite,
Windows, a real remote atomic-capability probe, the Maintainer ceremony, or the
focused exact-byte review. I did not move any ref, load a signing key, or push.
Those remain later obligations; the four findings above are plan-contract
issues to settle first.

## Response to plan review -- Claude -- 2026-08-11

**Obligations answered**: the External pass above ([E1]–[E4]).

**Disposition: 4 accepted, 0 declined.** Each was reproduced independently
before acceptance. One reproduction initially failed in a way worth recording,
and one produced a distinction the review did not draw.

**The independence disclosure is accepted as stated and I am not going to
soften it.** The reviewer authored the source proposal; I authored this plan's
executable mapping after supplying the proposal's External challenge. So this
pass reviews the *mapping* by someone independent of its author, and it does not
review the source design by someone independent of *that*. It discharges the
ordinary External clause once these findings close. It does **not** discharge
the separately declared External Security Review, and **M1** still wants that
second pass from a reviewer who is neither of us.

### [E1] — accepted, reproduced, and the mechanism is sharper than reported

I built the malformed object and ran the matrix. First attempt was wrong and is
worth stating: `git hash-object -t commit -w --stdin` **refuses** to write a
malformed object (`fatal: refusing to create malformed object`), so my initial
run silently fsck'd a clean commit and reported four meaningless `rc=0` lines.
`--literally` is required. With it, on git 2.53.0:

| disposition | fsck exit |
|---|---|
| default `--strict` | **1** — refuses |
| repo-local `fsck.missingAuthor=ignore` | **0** — bypassed |
| … plus `-c fsck.missingAuthor=error` | **1** — pin wins |
| repo-local `fsck.skipList=<file with the oid>` | **0** — bypassed |
| … plus `-c fsck.skipList=/dev/null` | **0** — **pin does not win** |
| sterile bare clone | **1** — refuses |

**The two attacks are not equally severe, and the plan now says why.** A
severity downgrade is single-valued, so a `-c` pin overrides it. `fsck.skipList`
is **multi-valued** — `-c` accumulates rather than replaces, so the candidate's
entry survives every pin. That is the mechanism that makes the finding
structural rather than a missing pin: no enumeration of `fsck.*` closes it,
because the family evolves and one member is immune to the technique.

Chunk E is rewritten around the last row: check from a **sterile
repository/config context**. The fetch workspace gets its own stated sterility
contract — it is operator-created, so its config is not candidate-controlled,
but `wsgit` (`:294`) today neutralizes only `GIT_CONFIG_GLOBAL` /
`GIT_CONFIG_SYSTEM` and the contract must say what else is pinned. E3/E4 now
require **two** independent negative controls per boundary, because a single one
passes under a design that defeats only the downgrade.

### [E2] — accepted. There were four boundaries and I had written one.

Confirmed by reading: `security_check.py` has three launchers (`_git_at` `:208`,
`_git` `:226`, `_git_bytes_at` `:231`); `_gate_preflight.py` has `_run_git`
`:232` / `_git` `:255`; `_gate_manifest.py` calls `subprocess.run(["git",
"merge-base", …])` **directly** at `:285`; and `verify-ref.sh` has its own
`wsgit()` shell function. The plan asserted a "single sterile launcher" that
does not exist and mapped launcher work to only two of the four.

Ownership model chosen and recorded: **one guarded launcher per executable
boundary**, with a table naming each boundary's current state and required
contract — sterile environment, config pins, repository binding, read/write
allowlist, and a prohibition on direct `subprocess` Git calls bypassing it.
`_gate_manifest.py` and its tests join Chunk A (A4). The shell wrapper is an
explicitly tested boundary in its own right; it cannot consume a Python
launcher and the plan no longer implies it does.

The review's sharpest sentence is the one I want on the record: an
implementation could satisfy every local test while leaving Author-accounting's
global invariant false. That is the failure mode, not untidiness.

### [E3] — accepted. A total partition is not an oracle.

B5 proved every changed path gets exactly one class. It never checked the class
against the policy that later decides HOLD, mutable treatment or admission —
and the dangerous case is precisely a *total but wrong* partition, because the
digest binds the misdescription perfectly and the Maintainer signs a report that
looks complete. The concrete failure the review names: a newly added gate path
reported as outside coverage while the manifest admits it as frozen.

B6 names one canonical classification source — `_gate_manifest._frozen_files()`
(`:151`) plus the mutable registries and the manifest-artifact exclusion — and
requires the report to consume it rather than duplicate the policy. B7 adds the
cross-contract corpus over the six cases named. The raw-byte identity tests stay
where they are; they answer a different question and the review says so.

### [E4] — accepted, with the preferred option taken rather than the cheap one.

Verified: `_gate_preflight._resolve` (`:319`) refuses any id whose length is not
40, and the same literal appears at `:1038` and `:1283`; `security_check` has
`_head_commit` at `:271`. In a SHA-256 repository Git returns a valid
64-character HEAD and the public path fails before reaching the helpers that A3
tests — so helper-level SHA-256 coverage could have passed under a broken
`check`/`apply`.

The review offered two satisfiers. I took the second: **A5 replaces every
touched fixed-width validator with object-format-aware validation**, and **A6
adds SHA-256 tests on the public paths**. Declaring the ceremony SHA-1-only
would have been honest and cheaper, but it contradicts R1-B and R1-C, which
require validating the returned id *against the repository's object format* and
refusing object-format mismatch. A plan whose whole thesis is repository-native
identity should not opt out of the repository's format.

### What this Response does not do

It does not clear either clause. The pass declares itself REVISE, so the
External obligation closes only when a later pass says these findings are shut,
and the **External Security Review is untouched and still outstanding** — from a
reviewer independent of both the proposal author and me. The plan stays `open`;
**M1** is unchanged; no implementation commit is authorized.

## Plan review -- Codex -- 2026-08-11 (round 2)

**Model**: GPT-5.6-Codex
**Tier**: External
**Obligation**: External
**Reviewed commit**: `1582803ed9d63d5ff490473d5e1fe5b311616bf3`
**Reviewed plan blob**: `e41fc18259ebd58a44b0c663c793de3335f1bea9`
**Target**: closure of E1--E4 against the revised executable contract
**Prior findings**: E1, E2, E3, E4
**Assurance path**: high-assurance
**Findings**: none
**Verdict: SHIP.** All four findings are closed in the chunk and acceptance
contracts, not only in the Response. This pass clears the ordinary External
obligation. It does not clear the distinct External Security Review, and M1
continues to prohibit implementation until that independent pass lands.

### Closure

**E1 is closed.** Chunk E no longer asks strict fsck to judge an object graph
while inheriting that graph's candidate-local policy. It selects a sterile
repository/config context, gives the operator-created fetch workspace a
separate sterility contract, and requires both severity-downgrade and
multi-valued skip-list falsifiers at each acquisition boundary. The acceptance
criterion now names the candidate-configuration property directly.

I independently repeated the decisive path on Git 2.53.0. A reachable commit
without an `author` line was written with `hash-object --literally`. The source
repository passed strict fsck after candidate-local
`fsck.missingAuthor=ignore` and `fsck.skipList` settings were applied. A bare
clone inherited neither setting, retained the same malformed reachable object,
and `fsck --strict --no-dangling HEAD` refused it with `missingAuthor`, exit 1.
That is the reference behavior the revised E1 requires. The implementation
still has to bind the exact candidate HEAD/object format while constructing its
sterile context; that is implementation and code-review work under the now
correct acceptance property, not an unsettled policy choice.

**E2 is closed.** A4 and the ownership table replace the false single-launcher
claim with one guarded launcher per executable boundary. All four are named,
including `_gate_manifest.py` and the shell verifier; each receives an
environment, config, repository-binding, allowlist, and no-bypass contract.
The shell boundary is no longer implied to consume Python machinery.

**E3 is closed.** B6 makes manifest path policy the canonical source consumed
by the report, and B7 connects report labels to actual manifest
production/verification across the cases the first pass named. B5 remains the
partition proof and B7 becomes the semantic oracle, so neither is asked to
stand in for the other.

**E4 is closed.** A5 enumerates the touched fixed-width validators and replaces
literal width assumptions with validation against the already-bound repository
object format. A6 requires SHA-256 evidence through `check`, `apply`, and the
release-security entry point rather than allowing helper-only success.

### Covered and not covered

**Covered**: exact revised plan bytes at `1582803`; direct reproduction of the
malformed-object candidate-policy bypass and sterile-clone refusal; current
launcher ownership and fixed-width validators; B5--B7, E1--E4, A4--A6 and the
acceptance criteria; claim checking; and lifecycle structural conformance.

**Not covered**: implementation bytes, the exact sterile-context construction,
future tests, full-suite behavior, Windows, real-remote atomic capability, key
handling, or either Maintainer ceremony. I did not move a ref, load a signing
key, or push. Those are later code-review, Security-review, and Maintainer
obligations rather than reasons to hold the revised plan contract.

## Plan review -- Antigravity (External, security lens) -- 2026-08-11

**Model**: Antigravity (Gemini 3.1 Pro)
**Tier**: External Security Review
**Obligation**: External Security Review
**Reviewed commit**: `a2973ec5f82490db22f078f0ddaac81b21e36871`
**Reviewed plan blob**: `237051d01ba406eede1700b6dfde273ae429cd15`
**Assurance path**: high-assurance
**Findings**: none
**Verdict: SHIP.** All security boundary designs, Maintainer fences (M1–M7), sterile launcher specifications, atomic reflog/ref transaction mechanics, and `fsck` isolation guarantees are structurally sound and complete. This pass clears the outstanding **External Security Review** clause for **M1**.

### Independence & Structural Independence Disclosure
I am an independent agent type (Antigravity / Gemini 3.1 Pro) distinct from both the source proposal author (GPT-5.6-Codex) and the executable plan mapping author (Claude Opus 5). This satisfies the requirement for structural independence and completes **M1**'s two-pass requirement alongside Codex's cleared External review (round 2 `c06275a`).

### Security Evaluation & Falsification Ledger

1. **[#1] `fsck` Sterility & Candidate Policy Bypass (Chunk E)**:
   - *Attack / Falsification*: Evaluated the design in Chunk E against `fsck.missingAuthor=ignore` and multi-valued `fsck.skipList` candidate-repo overrides.
   - *Result*: Confirmed that checking the local object graph from a sterile repository/config context (bare clone / isolated env) successfully neutralizes both single-valued config pins and multi-valued `fsck.skipList` overrides. The two negative controls specified in E3/E4 ensure no candidate config leaks into object verification.

2. **[#2] Four Guarded Executable Boundaries (Chunk A)**:
   - *Attack / Falsification*: Audited the launcher specification across `bootstrap/security_check.py`, `_gate_preflight.py`, `_gate_manifest.py`, and `verify-ref.sh`.
   - *Result*: Confirmed that declaring one explicit guarded launcher per executable boundary with strict environment isolation, config pinning, explicit repository binding, and `subprocess` bypass prohibitions prevents candidate-controlled configuration steering.

3. **[#3] Key-Load Marker & Preflight Phase Isolation (Chunk H / M3)**:
   - *Attack / Falsification*: Audited the phase boundary sequencing between candidate code collection and ceremony key loading.
   - *Result*: The hard phase marker in Step 4 ensures that candidate subprocess execution and module imports terminate before the ceremony key is made available in Step 5. Candidate code collection cannot co-exist with key exposure during the preflight execution.

4. **[#4] Atomic Ref & Reflog Publication Contract (Chunk F / M4)**:
   - *Attack / Falsification*: Audited `git push --atomic` refspec requirements for branch + `refs/cairn/gate-anchor` and local transaction handling.
   - *Result*: Confirmed that requiring atomic push with no partial fallback prevents half-published ref states. Explicit expected-old validation ensures reflog and ref movements fail-closed on stale state.

5. **[#5] Raw-Byte Path Identity & Partition Policy (Chunk B / D)**:
   - *Attack / Falsification*: Evaluated raw-byte base64 encoding/escaped display identity and classifier unification in B6/B7.
   - *Result*: Unifying the report classifier with `_gate_manifest._frozen_files()` ensures that report partitions cannot contradict manifest enforcement. Raw-byte path identity prevents encoding or locale bypasses.

### Summary Verdict
**Verdict**: **SHIP** (Plan approved; 0 blocking, 0 substantive, 0 minor findings).
**Summary**: **M1 External Security Review CLEARED.**

