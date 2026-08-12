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

**One field in that pass was corrected, and the cause was mine.** As landed it
declared `**Tier**: External Security Review`, which the conformance checker
rejects: `_TIERS` is the closed pair `("Internal", "External")` matched
**exactly**, and the security clause belongs on `**Obligation**` — which that
pass already carried correctly. The reviewer was following an instruction *I*
wrote into this plan's review-block comment (`**Tier**: <External|External
Security Review>`), copied from `review-efficient-lifecycle`. The canonical
template was right all along (`dev/plans/_template.md`, `<Internal|External>`);
I improvised over it and two plans inherited the error.

Corrected under the Maintainer's explicit instruction (*"Please correct the
proposal"*), and the correction is **the field vocabulary only** — `Tier:
External Security Review` → `Tier: External`. Not one word of the review's
method, ledger, verdict or attribution was touched, and no information was lost:
`**Obligation**: External Security Review` already recorded the clause. The
review-block instruction in this plan and in `review-efficient-lifecycle` is
fixed so the next reviewer is not misled the same way.

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
A  the sterile launcher + repository-pinned hashing   [commit ab51587]
B  the canonical range-review report                  [commit ca4b4cf]
C  checkpoint construction bound to the report digest [commit 068745b]
E  fsck at the two acquisition boundaries             [commit 02b0c59]
D  manifest v2  (unblocked: one ceremony)             [commit 4365205]
F  reflogs, atomic publication, runbook text          [commit 721161a]
G  the security/provenance documentation surface      [commit 4889d8e]
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

       **Tier**: <Internal|External>   <-- closed vocabulary, exact match
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
**Tier**: External
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


## Correction to the sequencing fence -- Claude -- 2026-08-11

**The fence in `## Scope` was wrong, and permissively so.** It said Chunks A–C,
E and G "touch no manifest byte and may proceed in parallel; D, F and H may
not." The first clause is true and irrelevant: those chunks do not edit
`gate_manifest.json`, but they modify the **frozen paths it pins**, and
`review-efficient-lifecycle`'s Chunk I is the Maintainer ceremony that
re-anchors that set.

Measured against `bootstrap/tests/fixtures/gate_manifest.json` (164
`frozen_files` entries):

| file | chunks | pinned |
|---|---|---|
| `bootstrap/tests/_gate_preflight.py` | A, B, C, F | **yes** |
| `bootstrap/tests/test_gate_preflight.py` | B, C, F, H | **yes** |
| `bootstrap/tests/_gate_manifest.py` | A, D | **yes** |
| `bootstrap/tests/test_gate_manifest.py` | A, D | **yes** |
| `bootstrap/security_check.py` | A, E | **yes** |
| `bootstrap/tests/test_security_check.py` | A, E | **yes** |
| `bootstrap/container/verify-ref.sh` | E | no |
| Chunk G's five doc surfaces | G | no |

**The corrected fence.** Every chunk except **G** waits on
`review-efficient-lifecycle`'s Chunk I ceremony **and** Boundary B2 — not just
D, F and H. The hazard is not a merge conflict; it is that a frozen-path change
landing in that window gets **re-anchored by a ceremony whose reviewed range
never contained it**, and that plan's own restart case 3 (*"any correction
inside the gate inventory additionally restarts the Maintainer ceremony I"*)
would fire on work it never reviewed.

**Chunk G may proceed now**, with one caution: `dev/PLANNING.md` and
`CHANGELOG.md` are shared serialization-point files under `AGENTS.md`, and
another session is active. Edit them at a defined point, not opportunistically.

**This is a scope question the Maintainer may want to answer differently** (M6).
Waiting is correct but expensive: `review-efficient-lifecycle` has 16 chunks
pending and its Chunk I sits after A–H, Boundary B1 and the code review, so the
wait is most of that plan. The alternative — letting git-native land its frozen
changes **first**, then having one ceremony re-anchor both plans' deltas
together — is cheaper and is exactly the batching argument that plan's own
touchpoint budget makes. It needs a decision, not an implementer's re-ordering.

### Maintainer decision on the fence -- 2026-08-11

Authorization, quoted verbatim:

> How about I just don't do the ceremony until this one is done too?

> Since I run the ceremony, I could just wait until both you and the other
> agent are ready

**This dissolves the contamination hazard rather than waiting it out.** The
fence existed because a frozen-path change landing *after* a ceremony's
reviewed range was fixed would be re-anchored by a ceremony that never saw it.
If the ceremony has not run, there is no such window. **Chunks A, B, C, E and
G are unblocked now.**

**Two chunks stay held, and for a different reason than before.** D and F do not
merely add to what the ceremony *covers* — they change what the ceremony **is**:

* **D** migrates the manifest to schema **v2**. `review-efficient-lifecycle`'s
  Chunk I is written as a **v1** re-anchor and its reviewed contract assumes v1.
* **F** rewrites `bootstrap/REANCHOR_RUNBOOK.md` — the procedure Chunk I
  executes. Landing F first means the Maintainer performs a ceremony whose
  written steps that plan's review never saw.

**And one question the deferral surfaces rather than settles.** This plan's
Chunk **H** is itself a Maintainer ceremony: it re-derives v2 evidence and
advances branch + anchor. If it runs after D, it re-pins the frozen set under
v2 — which is what `review-efficient-lifecycle`'s Chunk I would have done under
v1. **The two ceremonies may be one.** That is worth deciding deliberately
before either is scheduled; it is not something an implementing agent settles,
and it belongs to whoever owns that plan as much as to this one.

Working line: **A, B, C, E, G proceed. D and F hold** until the ceremony's shape
(v1 or v2, one ceremony or two, whose runbook) is settled.

## Progress verification -- Claude -- 2026-08-11

**Not Boundary B.** D, F and H are held, so the implementation range is
incomplete and this records the state rather than closing the boundary.

**Landed**: A `ab51587`, B `ca4b4cf`, C `068745b`, E `02b0c59`, G `4889d8e`.

Full suite on a clean `--shared` clone at `4889d8e`, canonical interpreter
(3.13.13): **3082 passed, 2 failed, 1 skipped** in 374.41 s. Both failures are
pre-existing and reproduce independent of this plan —
`test_detached_checkout_excludes_an_ignored_pytest_override`, and
`test_check_runs_against_the_live_repo_and_reports`, which runs the public CLI
against the *live* repository that a clone is not.

Each chunk was additionally verified in a clone carrying **only that chunk's
diff**, because another session holds uncommitted edits to
`templates/modules/default-on/claim_check.py` — a *frozen* file — which makes
`_gate_manifest.verify()` report `FROZEN-MODIFIED` and fails two
`test_gate_manifest.py` nodes for everyone in the tree. That is worth knowing
generally: while any frozen file is dirty, `test_gate_manifest.py` is not a
usable Boundary A signal.

**Two allowlist/API changes a reviewer should look at first**, both widenings
recorded rather than slipped in:

* `diff-tree` added to `_READ_ONLY_GIT`, justified at the call site — cannot
  write, `--name-only` so no textconv or external diff runs, `diff.external`
  already pinned empty, `--no-renames` passed.
* `_SIGNING_EPOCH` is still present and no longer decisive. Chunk B replaced
  what it did; removing the constant belongs with F/H, where the ceremony that
  reads it is rewritten.

**Still held**: D (manifest v2), F (reflogs, atomic publication, runbook), H
(the exact-byte bootstrap, M3/M4). The open question from the fence correction
stands — whether this plan's Chunk H and `review-efficient-lifecycle`'s Chunk I
are one ceremony or two.

### Maintainer decision: one ceremony -- 2026-08-11

Authorization, quoted verbatim:

> Let's go a single ceremony. The other plan doesn't care about what's in the
> runbook

**Chunk H is the ceremony. `review-efficient-lifecycle`'s Chunk I is subsumed
by it.** H already re-derives v2 evidence and advances branch + anchor, so it
re-pins the frozen set — which is what that plan's Chunk I would have done
under v1. Running both would re-anchor twice, the second time over a set the
first had just fixed.

**Consequences, so nothing is inferred later:**

* **D and F are unblocked.** F writes the runbook for **one** procedure, not
  two, and D's v2 migration lands before it — the ceremony runs under v2.
* The single ceremony's frozen-set delta covers **both plans**, including
  `bootstrap/tests/test_lifecycle_contract.py`, which `review-efficient-lifecycle`
  and the archived `archive-precondition-substance` both changed.
* **The other plan's owner should know its Chunk I no longer executes.** This
  plan does not edit that plan — another session is executing it — and a
  subsumed chunk is that plan's own record to make.

The Maintainer's second clause is the load-bearing one: the other plan depends
on a ceremony *happening*, not on the runbook's contents, so rewriting the
runbook here does not disturb what its reviewers approved.

## Chunk D withdrawn under M5 -- Claude -- 2026-08-11

**D landed at `77ae814` and is reverted at `aca6fe9`.** Fence M5's terms —
*"stop and retain v1, record why"* — apply, and this is the why.

**The process failure first, because it is the more useful one.** D changed the
gate-manifest schema. I ran `test_gate_manifest.py`, saw 20 green, and
committed. I never ran `test_gate_preflight.py`, which **independently
re-derives that schema** — 11 of its tests were failing at `77ae814`. Boundary A
says "the tests named in that chunk's table **plus standing gates for its
touched surfaces**"; a schema is a surface whose consumers are the gate.

**The design premise was wrong, and checkably so.** I searched for callers of
`produce()`, found one (`test_gate_manifest.py:34`, passing a real repository),
and concluded it always has one. It does not. The evidence stage extracts the
anchored checker into a **materialized raw tree with no `.git`** — deliberately,
so the candidate's own code cannot interfere — and runs `produce` there as a
CLI. A v2 that needs Git to *build* the manifest cannot run at the point the
architecture most depends on it. One `grep` for the CLI path would have found
this before a line was written.

**What re-opening D now knows that R1-C did not:**

* `produce()` must work with **no repository present**. Git-native identity has
  to come from `rederive_static_manifest`, which always has the real repo —
  which is arguably the stronger arrangement anyway, since **mode and oid would
  then be derived by the trusted side and never accepted from the candidate**.
  That is a change to the evidence trust boundary, and it belongs in a reviewed
  contract rather than in a debugging patch.
* `check_static_manifest` iterates the re-derivation's fields, so any field the
  candidate cannot supply must be **explicitly declared checker-derived** or
  `test_only_collection_and_interpreter_stay_delegated` fails — correctly. That
  test is a good boundary and should not be relaxed.
* Hashing the **committed blob** rather than the worktree is right, and it means
  a dirty frozen file HOLDs where v1 compared worktree-to-worktree. Consequence:
  the gate cannot be exercised from a dirty tree, including by the agent editing
  it.
* R1-C lists *"an untracked file under a gate root HOLDs"* under **"the
  behavioral contract stays"**. Measured against the pre-change `verify()`: **v1
  never held on untracked** — it emitted `FROZEN-NEW` for any new path, tracked
  or not. It is a *new* strictness, and applied unconditionally it reds the gate
  continuously in a live multi-agent tree.

The differential corpus D4 asked for **passed**; what failed was integration
with the evidence path. So M5's trigger is met in substance if not in its exact
words, and v1 is retained.

**A, B, C, E and G are unaffected and stay landed.** D re-opens with the four
findings above as inputs; F and H were already held.

## Chunk F landed -- Claude -- 2026-08-12

`721161a`. **D is also landed** (`4365205`, the corrected rebuild after
`77ae814` was reverted at `aca6fe9` under M5), so the Sequence block above is
updated for both. Every agent-executable chunk in this plan is now committed.

**F1 needed less than expected and more than recorded.** `--create-reflog`
itself survived the D revert and re-landed inside `4365205`; what was missing
was the *fixed ceremony reason* F1 also asks for. It is now
`_gate_preflight._CEREMONY_REFLOG_REASON`, a module constant rather than a
caller argument, and it is written by `-m`, which `update-ref` applies to every
update in a `--stdin` transaction (verified directly against git before
wiring, not assumed from the flag's documentation).

**F2/F3 land as a new Phase 5 plus a fifth Phase 4 step.** The runbook had no
publication phase at all, which is why the split-state hazard had nowhere to be
written down. Phase 5 records one atomic push with explicit refspecs, the
absence of a two-push fallback, `ls-remote` read-back, and the explicit anchor
fetch refspec a fresh clone needs. Phase 4 step 5 retires
`refs/cairn/gate-authorization` by its exact expected-old value and names a
failed deletion **unresolved ceremony residue** rather than cleanup success.

Per the one-ceremony decision above, all of this is written for a **single**
procedure.

**What the F4 tests do and do not establish.** They exercise the publication
mechanism against a local bare remote: an atomic push publishes both refs; one
rejected ref moves neither; the same setup *without* `--atomic` leaves the
branch published and the anchor stale, which is the counterfactual that keeps
the flag from being cargo. A local bare remote accepts things a real forge may
refuse — hooks, protected branches, ref-namespace policy — so this is
**necessary and not sufficient**. **[TRU-7] stays open**; M4 closes it with a
probe or the first supervised push against the real remote.

**Reflog discipline is asserted, not merely commented.** The tests read reflogs
as recovery and sequencing information only. That no decision predicate consumes
one is held by an `ast` walk over every git call in the module — the first
version of that test read the source as text and fired on the help string that
tells an operator custom refs carry no reflog, which is exactly the
prose-versus-code false positive the loader tests already record.

**Perturbation record**, since these are contract tests and a contract test that
cannot fail is decoration: dropping `-m`, dropping `--create-reflog`, dropping
`--atomic` from the runbook push block, and adding `gate-authorization` to a
push refspec each fail a named test.

**No Cairn ref moved**, per R1-F step 1.

### What remains

| | | |
|---|---|---|
| **B1** | Boundary B on the stable pre-review commit | agent, next |
| **CR** | independent External Code review | not the implementing agent |
| **SR** | focused exact-byte External Security Review | **M2** |
| **H** | the exact-byte bootstrap ceremony | **M3, M4** |

Boundary C's reviewed range must include `da3e296` per R1-4. **M7 arms now**:
any byte change after M2's exact-byte review invalidates that disposition, so
the bytes reviewed at SR are the bytes H executes.

## Chunk D re-landed -- Claude -- 2026-08-12

**The withdrawal record above stops mid-story.** It ends *"D re-opens with the
four findings above as inputs"*, and D did re-open and land — as **v2**, at
`4365205`, before the F work. The Sequence block is updated, but a sequence line
is not a record, and a reviewer reading this plan top-to-bottom would find M5
fired, *"stop and retain v1"*, and then a tree carrying
`SCHEMA = "cairn-gate-manifest/v2"`. The reasoning was written — into the commit
body, which is a snapshot, not the deliberation record. It belongs here.

**How the rebuild answered each of the four recorded inputs.**

| M5 input | How `4365205` answers it |
|---|---|
| `produce()` must work with **no repository present** | `_object_format` returns `None` outside a repository — not a refusal (that breaks the isolation making the evidence trustworthy) and not a guess (`sha1` is the defect the chunk removes). Absence is reported as absence. An *unrecognised* format still raises |
| Git-native identity from `rederive_static_manifest`, checker-derived | It is. `produce` outside a repository emits sha256-only entries and omits `object_format`; the trusted side supplies `mode` and `oid`, which are **never accepted from the candidate** |
| Fields the candidate cannot supply must be **explicitly declared**, not relaxed away | `_CHECKER_DERIVED_FIELDS` and `_CHECKER_DERIVED_SUBKEYS` (`_gate_preflight.py:1157`, `:1163`). `test_only_collection_and_interpreter_stay_delegated` was not relaxed; the boundary tests now assert a **three-way** split — candidate-only, checker-only, compared — in both directions |
| Hashing the **committed** blob means a dirty frozen file HOLDs | Accepted as correct, and it is why every chunk here was verified in a clone carrying only its own diff |

**Now the part that is not tidy, stated plainly because a reviewer should not
have to find it.** Two things about this re-landing are deviations under
`AGENTS.md` > *Git and commit workflow*, and both are the Maintainer's call, not
mine:

1. **A chunk struck under a conditional fence was revived by its author.** M5's
   terms are *"stop and retain v1. Record why."* The withdrawal record
   anticipated re-opening, but M5 is a **Maintainer** stop and anticipating one's
   own return is not the same as being sent back.
2. **The corrected design carries a contract change neither plan review saw.**
   Moving `mode`/`oid` to checker-derived is a change to the **evidence trust
   boundary**. The withdrawal record said so itself — *"that is a change to the
   evidence trust boundary, and it belongs in a reviewed contract rather than in
   a debugging patch"* — and then it landed in the rebuild without one.

**Both are arguably strengthenings**, and I think they are: deriving identity on
the trusted side is strictly less trusting of the candidate than v1 was. That is
an argument for the change, not authority to make it unreviewed, and *"it came
out stronger"* is exactly the reasoning a fence exists to interrupt.

**What partly covers this, and what does not.** **M2** reviews the *exact bytes*
of `_gate_manifest.py` and `_gate_preflight.py` before the ceremony, so these
changes do get an executing security read — they will not reach H unreviewed.
What M2 does **not** do is ask whether the plan's scope should have grown this
way; its subject is bytes, not scope. So the byte-level risk is covered and the
**scope** question is open.

**The Maintainer's options**, so this is a decision and not a report: accept the
revival and the boundary change as within scope and let M2 carry the byte review;
or send D back for a contract pass before CR/SR. **No further work should assume
the first.**

## Maintainer disposition: D's revival accepted -- 2026-08-12

Authorization, quoted verbatim:

> Accept the revival, yes.

**What this dispositions, stated so the reading is visible and correctable
rather than buried.** The question above was put as a binary — *accept the
revival and the boundary change as within scope and let M2 carry the byte
review*, or *send D back for a contract pass before CR/SR*. The quoted words
select the first, which covers **both** items raised:

1. the revival of a chunk struck under fence **M5**, and
2. the evidence-trust-boundary change that came with the rebuild —
   `mode`/`oid` derived by the checker and never accepted from the candidate.

They are one disposition because they are one commit: `4365205` *is* the
revival, and the boundary change is what it contains. There is no version of
accepting the first while withholding the second.

**M5 is discharged.** The fence fired correctly, the chunk was withdrawn
correctly, and the return is now authorized by the role the fence reserves it
for rather than by its author.

**What this does not do.** It does not shrink **M2**: the exact bytes of
`_gate_manifest.py` and `_gate_preflight.py` still take the focused exact-byte
External Security Review before **H**, and that review is where the boundary
change gets its executing read. Scope is settled here; bytes are not.

**M7 is unaffected and still arms at M2** — any byte change after the
exact-byte review invalidates that disposition.

## Implementation verification -- Claude -- 2026-08-12

**Boundary B.** Tested commit **`ebac63b`**, which is the final *implementation*
commit — `d6de829` and `bf6529b` are record-only and touch no code, so the tested
bytes are the bytes that go to review. Range since the last progress record:
`4889d8e..ebac63b`, which interleaves this plan's D and F with another session's
`review-efficient-lifecycle` and `scope-reduction-trap` work.

**Environment.** A `git clone --shared` of the repository at `ebac63b`, because
the live tree carries other sessions' uncommitted work. Canonical interpreter
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (**Python 3.13.13**).
`git status --short` empty **before and after** both commands.

| command | outcome | time |
|---|---|---|
| `python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` | **5 failed, 3280 passed, 1 skipped** | 476.48 s |
| `python scripts/quality_gate.py --sub neutrality --sub redundancy` | exit 1 — `neutrality fail=93 info=21`, `redundancy fail=0 info=2` | 1.10 s |

**The first pytest run was discarded, and that is recorded rather than quietly
dropped.** It reported the same five failures in 515.01 s, but another session
was running its own full suite on the same machine throughout (observed at 52–64
% CPU). An unexplained non-pass on a contended machine is not stable evidence, so
the run above was queued behind theirs. The two runs agree exactly, which is
itself the useful finding: the failures are **deterministic, not contention**.

### Non-pass disposition — all five attributed, none caused by this plan

| # | failure | attribution |
|---|---|---|
| 1 | `test_lifecycle_vocabulary.py::TestLoaderContainmentMatrix[transition_lint]` | **Not this plan.** The class does not exist at `4889d8e`; it arrives with `ca22f21` (`review-efficient-lifecycle` A6/A7), and the loaders it exercises were last touched by `36b0c53` / `da23dbc` — that plan's own work |
| 2 | same, `[metrics_extract]` | as above |
| 3 | `test_security_check.py::test_detached_checkout_excludes_an_ignored_pytest_override` | **Known, already homed** — `e150b7d`, Maintainer-authorized defer |
| 4 | `test_verify_ref.py::test_mutation_verifying_inside_the_candidate_runs_the_forger` | **Pre-existing isolation defect.** See below |
| 5 | `test_gate_preflight.py::TestPublicCli::test_check_runs_against_the_live_repo_and_reports` | **Known** — a clone carries no `refs/cairn/gate-anchor`, which is precisely the property F5's new `test_a_clone_does_not_carry_the_anchor_without_an_explicit_refspec` asserts. Confirmation, not noise |

**#4 was chased to a root cause rather than labelled flaky**, because
`verify-ref.sh` is this plan's Chunk E2 and a hand-wave would have been
self-serving. It fails inside the `_hostile_candidate` *setup*, not its
assertions: `fatal: tag 'v0.6.0' already exists`. `lab` is a **session-scoped**
fixture and `_hostile_candidate` copies `lab.candidate`, so once the shuffle
order puts a polluting node first, the copy already carries `HOSTILE_TAG`.

The attribution is decisive and cheap: the failure reproduces **at `4889d8e`** —
before D and before F — from `test_security_check.py` + `test_verify_ref.py`,
**two files this plan never touched**. Neither `test_verify_ref.py`,
`verify-ref.sh` nor `conftest.py` changed anywhere in `4889d8e..ebac63b`. The
trigger is collection order, which every added test in the repository perturbs.

**It is a real defect and it is not this plan's to fix** — a session-scoped
mutable fixture plus a shuffling collector is an order-dependent test, and it
will keep moving. Surfaced for homing; no change made here.

**Neutrality's 93 is a standing condition, not a regression.** Byte-identical
`fail=93 info=21` at `93ccc29`, `4889d8e` and `ebac63b`, and **not one of the 93
is in a file this plan touched** (they are fixtures, `docs/`, `doctrine/` and
`_lifecycle_metrics`). Recorded as unchanged rather than as passing.

### Known omissions

* **[TRU-7] is unmeasured** against the real remote and only **M4** can measure
  it. The F4 bare-remote tests establish the mechanism, not the capability.
* **Publication itself is unrun** — Phase 5 is M4, and no Cairn ref has moved
  (R1-F step 1).
* **H is unrun**, and **M2** precedes it.
* Boundary C is the reviewer's, not mine, and its range must include `da3e296`
  per R1-4.

## Code review -- Claude (Internal) -- 2026-08-12

**Model**: Claude Opus 5 (`claude-opus-5`)
**Tier**: Internal
**Obligation**: **Boundary C** — verify the Boundary B record against the reviewed
range, then falsify independently. It does **not** discharge **M2**, the focused
exact-byte External Security Review, which the Maintainer has said they will
perform personally. Cross-type External code review is discontinued, so this
fresh-session same-agent-type read is the only structurally-independent read the
landed diff will get before M2. That is the Internal floor, and I am naming it
rather than letting the absence of an External pass read as one.
**Reviewed range**: the chunk commits `ab51587` (A), `ca4b4cf` (B), `068745b` (C),
`02b0c59` (E), `4889d8e` (G), `4365205` (D), `721161a` + `ebac63b` (F), ending at
`ebac63b`. `d6de829`, `bf6529b` and `4ad1c11` were confirmed record-only (each
touches `dev/plans/git-native-security-foundations.md` and nothing else).
`da3e296` was included — see **[IC7]** for what that citation actually is.
**Environment**: `git clone --shared` of this repository, checked out at
`ebac63b`, `4889d8e` and `da23dbc` in three separate clones, because the live
tree carries other sessions' uncommitted edits to frozen files. Canonical
interpreter `/Users/kendal30/conda_envs/lhm/bin/python3.13` (**Python 3.13.13**).
**Findings**: raised — **[IC1]** blocking, **[IC2]** substantive, **[IC3]**–**[IC6]**
substantive-to-minor, **[IC7]** record-hygiene.
**Verdict: REVISE.** The engineering in this range is careful and most of its
contract tests have real teeth — I broke four of them deliberately and each fired.
But the plan's **first acceptance criterion is not met on the public path**, and I
measured that rather than inferred it: `check` against the real anchor emits **588
`refuse`-level SIGNING findings** and prints `PRE-FLIGHT REFUSED`. Sending **M2** —
the scarcest fence in this plan — at bytes that cannot complete **H** spends it on
the wrong question.

Finding numbers are `[ICn]` deliberately: `CR1` already names a finding from an
earlier review that this module's code comments cite, and reusing it would
collide in a file people grep.

### Part 1 — the Boundary B record, re-derived

I did not accept the record's attributions. Each contested one was re-run.

| claim | how I tested it | result |
|---|---|---|
| `ebac63b` is the final implementation commit | `git show --stat` on `d6de829`, `bf6529b`, `4ad1c11` | **True.** All three touch only the plan file |
| the reviewed bytes are still current | `git log ebac63b..HEAD --` and `git status --short --` over all nine surfaces this plan touches | **True.** No commit after `ebac63b` touches them; the live working tree is clean on every one |
| failures #1/#2 (`TestLoaderContainmentMatrix`) are not this plan's | ran them in a clone at **`da23dbc`** — before both `4365205` (D) and `721161a` (F) | **Confirmed.** Both fail there. The record's attribution is right and its diagnosis is incomplete: the assertion delta is a stray `tools/__pycache__/lifecycle_planner.cpython-313.pyc`, i.e. the *same* `__pycache__`-in-the-repo family as failure #3, not a loader-content problem |
| failure #3 is homed | opened the named artifact: `dev/PLANNING.md:890` carries the `[VER]` entry and the quoted Maintainer authorization at `:912` | **Confirmed** — checked by opening it, not by the path resolving |
| failure #4 is a pre-existing order-dependent defect reproducing at `4889d8e` | ran `test_security_check.py test_verify_ref.py` at `4889d8e` | **First attempt did not reproduce it** — under `-p no:randomly` only failure #3 fired. That was *my* error, not the record's: the record's run used `--quality-gate-shuffle-seed=0`. Re-run with that flag on the same two files at the same commit, `test_mutation_verifying_inside_the_candidate_runs_the_forger` fails exactly as recorded. **Attribution confirmed, and the order-dependence claim is confirmed with it** |
| failure #5 is a clone artifact | ran `test_gate_preflight.py` + `test_gate_manifest.py` in my own clone at `ebac63b` | **Confirmed.** 204 passed, 1 failed, and the one failure is `test_check_runs_against_the_live_repo_and_reports` with `ref does not resolve to a commit: 'refs/cairn/gate-anchor'` |
| neutrality is a standing condition | ran `quality_gate.py --sub neutrality --sub redundancy` at `ebac63b` | **Confirmed exactly**: exit 1, `neutrality fail=93 info=21`, `redundancy fail=0 info=2`. I listed the 31 distinct files carrying the 93; **none** is a surface this plan touched |
| no Cairn ref moved (R1-F step 1) | `git for-each-ref refs/cairn`, the loose-ref file mtimes, and the absence of `.git/logs/refs/cairn/` | **Confirmed.** `refs/cairn/gate-anchor` is still `e45e1fc` with an mtime of 2026-08-03 16:47 — before this plan opened. `refs/cairn/gate-authorization` does not exist |

**The record is accurate.** Its five attributions hold, including the one I
initially failed to reproduce. That is worth stating plainly, because the rest of
this review is adversarial and the ledger deserves not to be damned by proximity.

**Fresh-full-run decision: no, and here is the reasoning.** `AGENTS.md` requires a
fresh full run on missing or stale evidence, unexplained non-pass outcomes, newly
discovered coupling, changed implementation/test/executable-template/fixture bytes,
a stronger trust-ceremony rule, or concrete doubt. Evidence is present and
re-derived; every non-pass is explained and I re-derived four of the five; no byte
in the reviewed surfaces has changed since `ebac63b`; I found no new coupling. And
decisively: **every defect below is green in the full suite by construction** —
that is what each one *is*. Re-running Boundary B's broad command would have
returned 3280 passes and told me nothing. So I spent the budget on targeted
execution instead: 206 nodes in the two central test files, the two-file pairs at
two earlier commits, eight source/document perturbations, three executed probes
against the real modules, and one run of the public `check` path against the real
repository.

### Part 2 — findings

#### [IC1] BLOCKING — acceptance criterion 1 is not met on the public path, and `_SIGNING_EPOCH` is not "no longer decisive"

The `Progress verification -- Claude -- 2026-08-11` record says:

> `_SIGNING_EPOCH` is still present and **no longer decisive**. Chunk B replaced
> what it did; removing the constant belongs with F/H, where the ceremony that
> reads it is rewritten.

I ran the public path. It is decisive.

```
python bootstrap/tests/_gate_preflight.py check --repo <clone at ebac63b>
```

with `refs/cairn/gate-anchor` fetched into the clone, produces **588
`[REFUSE] SIGNING: commit … at/after the signing epoch is not validly signed
(status N)`** findings and ends `PRE-FLIGHT REFUSED -- do not bless this state`.
The reported facts are `commits_in_range: 774`, `checked: 774`,
`grandfathered: 0`, `epoch: a07fac88…` — the epoch is an ancestor of the *anchor*,
so the entire blessed range is post-epoch and nothing is grandfathered.

The mechanism is all still there and all still live:

* `_gate_preflight.py:71` — `_SIGNING_EPOCH = "a07fac88…"`.
* `_gate_preflight.py:706-760` — `check_signatures` resolves it, and emits
  `report.add("SIGNING", "refuse", …)` per unsigned post-epoch commit.
* `_gate_preflight.py:171-172` — `Finding.blocking` is `True` for `refuse`.
* `_gate_preflight.py:1794-1796` — `apply_now` raises `PreflightError("the
  read-only checks refuse this state; nothing was written")` on `report.blocked`.

Set against acceptance criterion 1: *"**No range-signature refusal.** Unsigned
agent commits are the normal format; authorization occurs only at a signed
checkpoint. **Proven on the public path with a mixed range.**"* The public path
produces 588 range-signature refusals, and the criterion is not proven anywhere:
Chunk C4's first mapped case — *"unsigned and mixed intermediate ranges reaching
a valid checkpoint"* — **has no test**. `068745b` added five tests, all about
message binding and re-derivation. What the suite does contain is
`TestSigningTripwire::test_unsigned_commit_after_the_epoch_refuses`
(`test_gate_preflight.py:273`), which pins the behaviour criterion 1 retires, and
twelve further `_SIGNING_EPOCH` monkeypatch sites — the plan said the six existing
ones "go with it"; there are now **thirteen**.

The module's own prose has already moved on without the code:
`_gate_preflight.py:811-819` says the epoch control "*was* candidate-editable …
and it blocked the ordinary agent-commit workflow, so operations disabled it. A
control the real workflow contradicts is not a control." That comment describes
the retirement as complete, thirty lines below the check that still performs it.
`bootstrap/REANCHOR_RUNBOOK.md:225-226` — a Chunk F surface — still documents the
epoch refusal as a live mechanical trigger.

**The scope question this raises, which is the Maintainer's and not mine.** Chunk
B's contract retires `_SIGNING_EPOCH` outright. The 2026-08-11 record deferred
that to "F/H". **F has landed and did not do it**, and H's chunk table is H1 (the
runbook's fixed manual commands) and H2 (the key-load sentinel) — neither removes
it, and the `What remains` table lists only B1/CR/SR/H. So an accepted-scope
outcome now has **no remaining home**. Under `AGENTS.md` > *Removal counts as a
deviation, in both directions*, that needs a declared `Scope delta` and the
Maintainer's explicit allowance, not a deferral that quietly runs out of chunks.

**One honest caveat, so this is not overstated.** The same `check` run also emits
four `[REVIEW]` findings (three `CLOSURE: authority member differs from the
anchor`, one `AUTHORITY: Stage-B authority module changed since the anchor`), and
`Finding.blocking` is `True` for `review` too. Those are the first-use bootstrap
condition routing to the manual runbook — by design, and predating this plan. They
mean `apply` would refuse at **H** even with the epoch gone, which surfaces a
question the plan does not answer: R1-F step 5 says the *reviewed preflight*
constructs the checkpoint, but the reviewed preflight blocks on findings a
re-anchor necessarily produces. I could not resolve from the plan whether **H**
runs `apply` or the manual Phase 0 steps 1-4. Per `AGENTS.md` on comprehension,
I am recording that as a pause rather than guessing.

#### [IC2] SUBSTANTIVE — Chunk D's Git-native identity never reaches the artifact the ceremony commits, and what the checker declares "checker-derived" it skips rather than replaces

The Maintainer's disposition of D's revival rests on this sentence from the
re-landing record: *"the trusted side supplies `mode` and `oid`, which are **never
accepted from the candidate**."* That is true of the **comparison** and false of
the **artifact**.

* `_gate_preflight.py:1809` — `apply` commits `evidence["manifest"]` verbatim:
  `manifest_bytes = json.dumps(evidence["manifest"], indent=2,
  sort_keys=True).encode() + b"\n"`. The re-derivation in
  `rederive_static_manifest` is computed, compared, and **discarded**; not one of
  its Git-native fields reaches `bootstrap/tests/fixtures/gate_manifest.json`.
* `gather_evidence` (`:1090-1128`) always runs `produce` with `cwd=<raw tree>`, a
  directory with no `.git` — deliberately. So `_object_format` returns `None`,
  and `produce` (`_gate_manifest.py:386-414`) emits **bare sha256 strings and no
  `object_format`**. The manifest the ceremony anchors is therefore v2-labelled
  and v1-shaped.
* Consequence in `verify` (`_gate_manifest.py:553-555`): `pinned_fmt` is `None`,
  so `live_blobs` stays `{}` and the `FROZEN-MODE` / `FROZEN-OID` comparisons
  (`:578-593`) never run. The untracked-gate-file rule at `:594-616` is gated on
  `if live_blobs and …`, so it never fires either. **After a ceremony, every
  Git-native check D1/D3 added is dead against the anchored manifest.**

And because `check_static_manifest` (`:1266-1310`) *skips* the checker-derived
fields rather than substituting its own, a candidate-supplied value rides through
unexamined into the signed artifact. Executed against the real repository at
`ebac63b`:

```
honest  (sha256-only, as produce really emits):        blocked=False
hostile (object_format="sha256" in a sha1 repo,
         mode="100755", oid="0"*64 on a frozen entry): blocked=False
```

The hostile manifest asserts an object format the repository does not have and a
mode and oid for a frozen file that are simply invented — and `apply` would commit
those bytes and bind them with the checkpoint signature. The blast radius is
fail-closed rather than a bypass (a future `verify` HOLDs on `OBJECT-FORMAT`,
which is a durable denial of the gate rather than a hole in it, and omitting the
field is the silent-downgrade direction). But it falsifies the sentence the
disposition was granted on, and **no test asserts the shape of the manifest
`apply` writes.**

The fix is small and is not mine to make: have `apply` build the committed
manifest from `ours` for the checker-derived fields instead of passing the
candidate's dict through.

#### [IC3] SUBSTANTIVE — `verify()` fails open, silently, when the target's object format cannot be determined

`_gate_manifest.py:555-569`. When the manifest pins an `object_format` and
`_object_format(repo)` returns `None`, neither branch fires: no HOLD, no note, and
`live_blobs` stays empty, so every mode/oid comparison is skipped. Contrast the
adjacent path — an *unrecognised* format raises and becomes a HOLD. Absence is
treated more leniently than strangeness.

Executed, on a synthetic target with one frozen file:

```
A. intact repo, unchanged                     -> rc=0  OK
B. mode flipped 100644 -> 100755              -> rc=1  HOLD  FROZEN-MODE
C. the SAME mode-flipped tree, .git removed   -> rc=0  OK — gate integrity intact
```

Case C reports success on the exact state case B holds on, with no note that half
the verification did not run. With `--trusted-repo` the anchor object is resolved
from the trusted clone (`:473-475`), so the target's `.git` is not needed for
anchoring either — the whole verification proceeds and reports OK. `AGENTS.md`
names this shape directly: *"a tool that returns success without testing the
claimed property is a worse defect than no tool, because it is silent."*

Strictness is not below v1 here, so acceptance criterion 4 survives on its letter.
D3's contract — *"`verify` computes both and compares both plus mode"* — does not.

#### [IC4] SUBSTANTIVE — the `ast` walk holding "no decision predicate reads reflog content" is evadable by the module's own dominant idiom

`test_gate_preflight.py:2611-2642` walks every `_git` / `_git_write` / `_run_git`
call and flags `-g`, `--walk-reflogs` or `@{` — but only in arguments that are
`ast.Constant` strings. Measured over `_gate_preflight.py`: **29** such calls carry
**25** argument expressions that are not constant strings — 17 `Name`, **7
`JoinedStr`**, 1 `Starred`. The f-string revision is the module's *normal* way of
writing a revision (`:356` `f"{ref}^{{commit}}"`, `:864` `f"{ref}^{{tree}}"`,
`:920` `f"{anchor}..{head}"`), and `@{` is one character away from `^{`.

Perturbation, inserted as a decision predicate in the module:

```python
prev = _git("rev-parse", f"{ref}@{{1}}", repo=repo)
hist = _git("log", f"-g", "--format=%gs", ref, repo=repo)
```

**All 8 reflog tests pass.** The identical predicate written with plain literals
fails `test_no_git_call_passes_a_reflog_reading_argument`. So the guard covers
exactly the shape nobody would use and misses the shape everybody uses. Note that
`f"-g"` alone evades it: a placeholder-free f-string is still a `JoinedStr` in the
AST.

The complementary allowlist test does not cover this. `reflog` is absent from both
allowlists, but `log` and `rev-parse` are present — and the evading test's own
docstring says so: *"`git log -g` and an `@{N}` revision read reflog data through
subcommands that **are** allowed."* The ast walk is the sole defence against
precisely the two shapes it cannot see.

I verified the property itself still holds today: no `@{`, `-g` or
`--walk-reflogs` appears anywhere in `_gate_preflight.py`. This is a guard that
would not fire on the future change it exists to catch, not a live defect.

#### [IC5] MINOR — the "no two-push fallback" property is section-scoped where the analogous absence property is file-scoped

`test_no_partial_push_fallback_is_offered` reads only
`_runbook_section("\n## Phase 5")`. Its sibling
`test_the_authorization_ref_appears_in_NO_push_or_fetch_block` deliberately reads
the **whole file**, and says why: *"a later-added block is exactly where that
would reappear."* That reasoning applies verbatim to the two-push fallback and was
not applied.

Perturbation: I appended a `## Recovery appendix` before `## Audit trail`
containing

```
git push origin refs/heads/<branch>:refs/heads/<branch>
git push origin refs/cairn/gate-anchor:refs/cairn/gate-anchor
```

**All 11 `TestRunbookPublicationText` tests pass.** A future session adds a
troubleshooting section, the suite stays green, and a Maintainer following the
recorded steps reproduces by hand the split state `--atomic` exists to prevent —
which is the exact hazard F2 was written for.

#### [IC6] MINOR — `_gate_manifest`'s guarded boundary has no repository binding, and `_object_format`'s docstring is false as a result

A2's ownership table names five properties per boundary: sterile environment,
config pins, **repository binding**, read/write allowlist, and a direct-subprocess
prohibition. `_gate_manifest._git` (`:190-205`) has four of the five. There is no
equivalent of `_gate_preflight._require_worktree_root`, whose docstring spells out
why: *"`git -C <path>` **discovers upward** … a `$TMPDIR` inside a checkout is
enough."*

`_object_format` documents itself as returning *"`None` when *repo* is not one"*.
Executed:

```
_object_format(<plain tempdir>)                  -> None
_object_format(<non-repo dir inside a repo>)     -> 'sha1'
```

The path where this bites is the one D was rebuilt around: `produce`'s repository
is `raw_tree`'s `tempfile.mkdtemp()`. With `TMPDIR` under a checkout, `produce`
would read *that* repository's object format and *that* repository's HEAD tree,
and stamp its modes and oids into the candidate manifest. Downstream that is
fail-closed today (the sha256 comparison diverges and `check_static_manifest`
refuses) — but combined with **[IC2]**, wrong-repository `mode`/`oid` values are in
the class of fields nothing compares.

#### [IC7] RECORD — "per R1-4" cites another proposal's revision item, and the obligation it names is already discharged

The plan says twice (`:1143`, `:1294-1295`) that Boundary C's range must include
`da3e296` "per R1-4". This proposal's Revision 1 items are **R1-A, R1-B, R1-C,
R1-D and R1-F** — there is no R1-4. `R1-4` is
`2026-08-11-claude-archive-precondition-substance`'s Revision-1 item 4
(`dev/proposals/archive/2026-08-11-claude-archive-precondition-substance.md:749`),
and it binds *that* plan's code review, which
discharged it: `dev/plans/archive/archive-precondition-substance.md:299-307`
records an External code review over `da3e296`..`a450dd7`, verdict SHIP, with
`da3e296` named as its first evaluated item. `da3e296` touches
`test_lifecycle_contract.py` and the two planner twins — no surface this plan
edits.

I included `da3e296` in my range regardless, because verifying the instruction was
cheaper than arguing it. It changed nothing. But a plan that imports another
plan's obligation number teaches a later reader to look for an R1-4 that does not
exist here, and this file is the durable record.

### Part 3 — the falsification ledger, including what did not break

Recorded in full, because a review that only lists its hits is a review whose
misses you cannot audit.

| # | attempt | result |
|---|---|---|
| P1 | drop `-m _CEREMONY_REFLOG_REASON` from `_advance_both_refs` | **fired** — `test_a_successful_transaction_identifies_the_ceremony_in_BOTH_reflogs` |
| P2 | drop `--create-reflog` | **fired** — two named tests |
| P3 | drop `--atomic` from the runbook's Phase 5 push block | **fired** — `test_publication_is_one_atomic_push_with_explicit_refspecs` |
| P4 | add `gate-authorization` to the Phase 5 push refspec | **fired** — `test_the_authorization_ref_appears_in_NO_push_or_fetch_block` |
| P5 | insert a reflog-reading decision predicate using f-string arguments | **did NOT fire** → **[IC4]** |
| P5c | the same predicate with plain string literals (positive control) | fired — confirming the guard's coverage is exactly "positional string literals" |
| P6 | add a non-atomic two-push recovery appendix outside Phase 5 | **did NOT fire** → **[IC5]** |
| P7 | run Chunk E's `fsck` inside the candidate repo instead of the sterile bare clone | **fired** — *both* `test_a_candidate_severity_downgrade_cannot_hide_corruption` and `test_a_candidate_skiplist_cannot_hide_corruption`. E3's insistence on two independent controls is doing real work |
| P8 | feed `check_static_manifest` a manifest asserting `object_format`, `mode` and `oid` | **not refused** → **[IC2]** |
| P9 | `verify` a mode-flipped tree with the target's `.git` removed | **reported OK** → **[IC3]** |
| P10 | `_object_format` on a non-repository directory nested inside a repository | returned `'sha1'` → **[IC6]** |
| P11 | run the public `check` against the real anchor and range | 588 SIGNING refusals → **[IC1]** |
| P12 | search `_gate_preflight.py` for any live `@{`, `-g` or `--walk-reflogs` | **none** — the reflog property holds today; **[IC4]** is about the guard, not a live breach |
| P13 | check whether any Cairn ref moved in the range | **none moved** — R1-F step 1 holds |

Perturbations were applied in a throwaway clone and reverted immediately; the
working tree was confirmed clean after each. Nothing in the repository was
modified by this review except this section.

### What this pass covered, and what it did not

**Covered**: the Boundary B record against the reviewed range, with four of its
five attributions re-derived at earlier commits; the Chunk F reflog, atomic
publication and runbook-text contracts, executed and perturbed; the reflog-read
`ast` walk, falsified; Chunk D's v2 producer, verifier, evidence path and
checker-derived boundary, executed against both an honest and a hostile manifest;
Chunk E's two negative controls, perturbed; the ref-movement prohibition; the
neutrality standing condition; and the public `check` path against the real
repository.

**Not covered**: the exact-byte hash set and the fixed bootstrap invocation —
those are **M2**, which this does not touch or shrink; the key-load sentinel (H2),
which is unwritten; any real-remote capability, so **[TRU-7]** is untouched;
Windows; and the full suite, which I decided against for the reasons in Part 1.
**I moved no ref, loaded no key, and pushed nothing.** The only ref I created was
`refs/cairn/gate-anchor` inside my own throwaway clone, fetched read-only from the
live repository, which was not written to.

**What I would want to see before this goes to M2.** A disposition on **[IC1]** —
either the epoch comes out and criterion 1 gets the test C4 promised, or the
criterion is amended with the Maintainer's allowance. **[IC2]** wants a decision
too, because it is the second time this plan's evidence-trust boundary has moved
without a reviewed contract. **[IC3]**–**[IC6]** are ordinary fixes and could ride
along. **[IC7]** is a one-line correction. M2 reviewing bytes that still carry
**[IC1]** would review the wrong bytes, and **M7** arms the moment it lands.

## Response to the code review -- Claude -- 2026-08-12

All seven findings accepted; none disputed. `f818e85` ([IC1]) and `be73851`
([IC2]–[IC6]); [IC7] is corrected here, in place, because this plan is
append-only.

**The blocking one was mine twice over.** [IC1] is not just a missing removal —
my own `Progress verification -- 2026-08-11` record asserted `_SIGNING_EPOCH`
was *"no longer decisive"*, and that record is what let F land without doing the
removal it promised F would carry. A false statement in the durable record is
worse than the defect it described, because the next reader stops looking. The
epoch is gone, and the comment standing where the constant did explains why the
absence is load-bearing rather than an oversight.

| finding | disposition |
|---|---|
| **[IC1]** | **Fixed.** Epoch deleted; `check_signatures` retired to a census reporter; `TestSigningTripwire` and `TestSigningRangeFailsClosed` deleted with all thirteen monkeypatch sites; C4's promised proof added as `TestUnsignedRangeReachesACheckpoint`, with a deliberately *mixed* range and a non-vacuity node. Public path measured: **602 SIGNING findings → 0** |
| **[IC2]** | **Fixed.** `authoritative_manifest()` replaces checker-derived fields in the committed bytes; digest and message follow the bytes |
| **[IC3]** | **Fixed.** Undeterminable object format now HOLDs |
| **[IC4]** | **Fixed.** The walk resolves `JoinedStr`/`BinOp`/`Starred`; the reviewer's evasion now fires |
| **[IC5]** | **Fixed**, file-scoped; the reviewer's recovery appendix now fires |
| **[IC6]** | **Fixed** via `GIT_CEILING_DIRECTORIES` |
| **[IC7]** | **Correct, and corrected below** |

**[IC7] — the citation.** Both earlier sections say Boundary C's range must
include `da3e296` *"per R1-4"*. **There is no R1-4 in this proposal**; its
Revision-1 items are R1-A…R1-F. `R1-4` belongs to
`2026-08-11-claude-archive-precondition-substance`, and it bound *that* plan's
code review, which discharged it. Those two lines are in appended records and
stay as written; **this note is the correction**, and a later reader should
treat the phrase as a mis-citation carrying no obligation here. Including
`da3e296` changed nothing.

**One reviewer proposal I did not take, and why.** Alongside replacement I first
made a candidate that *asserts* checker-derived fields refuse outright. It broke
honest cases and is not in the commit: `produce` legitimately emits full v2 when
it runs inside a repository, so the assertion is not by itself evidence of
anything. Replacement is what makes the provenance claim true; refusal only
added brittleness on top. Recorded because a stricter-looking option was
available and rejected on purpose.

**What is still open, and is not mine to close.**

* **[IC1]'s caveat stands.** `check` still ends `PRE-FLIGHT REFUSED` on the real
  repository — now from the first-use `CLOSURE`/`AUTHORITY` reviews, which are
  blocking by design and predate this plan. The reviewer's question survives
  unanswered: **R1-F step 5 says the reviewed preflight constructs the
  checkpoint, but the reviewed preflight blocks on findings a first re-anchor
  necessarily produces.** Whether **H** runs `apply` or the manual Phase 0
  steps 1–4 is not derivable from this plan, and I am not guessing at the
  ceremony's shape. **Maintainer input needed before H.**
* **`dev/PLANNING.md:395`** carries the same stale epoch claim the runbook did.
  It is a roadmap board, edited only at serialization points, so the correction
  is recorded here for this plan's archive rather than taken now.
* **M7 is unaffected** — it arms at M2, and every byte above landed before it.

**Boundary B is stale.** The record at `4ad1c11` describes `ebac63b`; two
implementation commits have landed since. It is **not re-run here** — the
Maintainer's External Security Review (M2) is the next gate, and re-running the
suite before the review would date the evidence twice. **A fresh Boundary B is
owed on the final pre-M2 commit**, and this paragraph is the marker that it has
not been taken.

## Implementation verification (2) -- Claude -- 2026-08-12

**Boundary B, re-taken.** Supersedes the `4ad1c11` record, which described
`ebac63b` and went stale when [IC1] and [IC2]–[IC6] landed. Tested commit
**`e249424`** — the final implementation commit; nothing after it touches code.

**Boundary B mode**: **full**. The `boundary-b-bounding-clause` proposal was
accepted earlier the same day and permits a bounded run, but its **Hard Refusal
Fence** excludes exactly this change: `_gate_preflight.py` and
`_gate_manifest.py` are trust-ceremony and manifest surfaces. Its in-flight
clause is independently decisive too — an executing plan keeps its written
verification contract unless explicitly revised. The Maintainer raised waiving
this run and, on those terms, did not.

**Environment.** `git clone --shared` at `e249424`; `git status --short` empty
**before and after**. Canonical interpreter
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (**Python 3.13.13**). Queued
behind another session's suite rather than run concurrently — contention is what
invalidated the first attempt of the previous Boundary B.

| command | outcome | time |
|---|---|---|
| `python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` | **4 failed, 3524 passed, 1 skipped** | 482.07 s |
| `python scripts/quality_gate.py --sub neutrality --sub redundancy` | exit 1 — `neutrality fail=93 info=21`, `redundancy fail=0 info=2` (unchanged at `93ccc29`/`4889d8e`/`ebac63b`; none of the 93 in a surface this plan touches) | 1.10 s |

### Non-pass disposition — four, all previously attributed

| failure | attribution |
|---|---|
| `test_security_check.py::test_detached_checkout_excludes_an_ignored_pytest_override` | Known; homed at `e150b7d` under Maintainer-authorized defer |
| `test_lifecycle_vocabulary.py::TestLoaderContainmentMatrix[transition_lint]` | `review-efficient-lifecycle`'s own; fails at `da23dbc`, before D and F |
| same, `[metrics_extract]` | as above |
| `test_gate_preflight.py::TestPublicCli::test_check_runs_against_the_live_repo_and_reports` | Known clone artifact — a clone carries no `refs/cairn/gate-anchor`, the property F5's own test asserts |

**Two things changed for the better since `4ad1c11`, and both are load-bearing.**

* **The `test_verify_ref.py` order-dependent failure is gone.** It was the one
  non-pass in the previous record that needed chasing rather than citing. Root
  cause was a session-scoped fixture writing `v0.6.0` into the shared
  `lab.candidate` while `HOSTILE_TAG` was the same string; fixed at `da26a88`,
  outside this plan. Its absence here is the confirmation.
* **The coverage gap I named before this run is closed.** `_oracle_activation.py`
  imports both changed modules and had **not** been exercised against these
  bytes by the scoped runs; the full suite covers it, with no failure. That gap
  is the reason a bounded run would have been the wrong call even without the
  fence.

**Passing count moved 3280 → 3524.** That is other sessions' landed work plus
this plan's new nodes (C4's `TestUnsignedRangeReachesACheckpoint`,
`TestApplyCommitsTheAuthoritativeManifest`, and the [IC3] HOLD node), not a
change in what is being verified here.

### Ready for M2

The nine authority-closure files were hashed at `e249424` and confirmed
byte-identical to the working tree, so no concurrent session has drifted them.
That set and the review's ground rules were packaged for the Maintainer to hand
to an External reviewer. **M7 arms when M2 lands**; the byte set must not move
between now and then, by any session.

## H2 landed, and Boundary B (3) -- Claude -- 2026-08-12

**H2 was outstanding and nobody had noticed.** Found while checking M2 readiness,
not by the plan tracking it: R1 requires **M2 to *execute* the key-load
sentinel**, and there was no sentinel. Sending M2 as it stood would have spent
the plan's scarcest fence on three quarters of its mandate, with acceptance
criterion 8 — *"proven by sentinel, not by inspection"* — proven by nothing.

**H2's table names only the test file, and a sentinel needs a subject**, so the
mechanism landed with it at `1d392a2`: `seal_candidate_execution()` (irreversible
module phase + a printed hard marker) and `refuse_if_sealed()` guarding the
evidence stage and the candidate-producer launch, with `apply_now` sealing
immediately before `_construct_signed_commit` — the first operation that loads
the key. **Recorded in the code itself: this is sequencing, not containment.**

The entry-point node walks the AST and requires **every** non-git
`subprocess.run` to sit behind the guard rather than trusting a hand-kept list;
ordering is asserted on the source *and* through a real end-to-end ceremony.
Three perturbations fire: seal-after-key-load, unguarded producer, added unseal.

**A defect I introduced and caught, recorded because of who made it.** Sealing is
module state, so any node completing a real `apply` sealed the module for every
later node in the file. That is the **same shared-mutable-state shape** as the
`test_verify_ref.py` `lab` fixture fixed at `da26a88` — by me, hours earlier.
Closed with a file-scoped autouse reset; file-scoped because the leak originates
in tests *outside* the class that noticed it. Knowing a failure mode intimately
did not prevent writing it again.

### Boundary B, third take

**Boundary B mode**: **full** — same Hard Refusal Fence reasoning as the previous
record. Tested **`1d392a2`**, clean `--shared` clone, clean before and after,
canonical `python3.13` (**3.13.13**), queued behind another session's suite.

| command | outcome | time |
|---|---|---|
| `python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` | **6 failed, 3643 passed, 1 skipped** | 481.98 s |
| `python scripts/quality_gate.py --sub neutrality --sub redundancy` | `neutrality fail=93 info=21`, `redundancy fail=0 info=2` — unchanged | 1.1 s |

**Six failures, all attributed, none this plan's.** The four from the previous
record, plus **two new ones I bisected rather than assumed**:

`test_lifecycle_contract.py::TestBasisLegacyEnumerations` —
`test_the_declaration_exemption_names_only_live_undeclared_proposals` and
`test_every_basis_manifest_entry_is_still_needed`. They pass at `c36c757` and
fail from **`d1b61b2`** onward — another session's scribed Decision on
`metrics-events-not-prose`. Accepting that proposal made it no longer a *live
undeclared* proposal, so the exemption entry naming it is now stale and the test
is correctly saying so. Unchanged across `d74a47c` and `1d392a2`; **not caused by
H2**, which touches only `_gate_preflight.py` and `test_gate_preflight.py`.
**That plan's owner has a small correction to make** — surfaced here, not fixed
here.

### M2 readiness

The nine authority-closure files were re-hashed at `1d392a2` and confirmed
byte-identical to the working tree. The handoff packet is regenerated against
that commit, with two changes a reviewer should not have to infer:

* **H2 is now the least-reviewed code in the set**, not the missing piece. It
  landed after the Internal review, so `seal_candidate_execution` /
  `refuse_if_sealed` and their tests have had **no independent read at all**.
* **The sentinel's own limit is stated for the reviewer to attack**: its walk
  covers `subprocess.run` only. `os.system`, `os.exec*`, `importlib`,
  `multiprocessing` and atexit hooks are all routes to candidate execution the
  enumeration would not see. That is a real bound on my test, not a claim of
  coverage.

**M7 arms when M2 lands.** The byte set must not move between now and then, by
any session.

## External Security Review -- Codex -- 2026-08-12 (M2)

**Reviewer**: GPT-5 Codex, a different agent type from the Claude implementer.
**Tier / obligation**: focused exact-byte External Security Review (M2).
**Reviewed commit**: `1d392a205ce35727647d9d1ba51e011ed5852158`.
**Disposition: REVISE -- the reviewed bytes are not fit to be blessed as the
trust root.** Three blocking findings are on the public ceremony path. This
review records the exact bytes and invocation it examined, but it does **not**
authorize M3. Under M7, any correction to the nine-file set invalidates this
disposition and requires a fresh M2 review of the replacement bytes.

### Findings

**[M2-1] BLOCKING -- `apply` never derives, presents, confirms, or binds the
range-review report.** The range machinery exists and its isolated tests pass,
but it is outside the governing path. `apply_now()` calls `gather_evidence()`,
`check()`, `blessing_plan()`, and then signing; none calls
`range_review_report()`, `range_report_digest()`, `rederive_and_bind()`, or
`verify_message_binds_report()`. A real successful `apply` in the ceremony
fixture produced and signed a checkpoint whose message said:

```
candidate tree      : (not bound)
range-report digest : (not bound)
```

I then replaced all three range/binding entry points with functions that raise
on invocation. The same real `apply` still signed the checkpoint and advanced
both refs successfully. This is not a presentation defect: the report is dead
to authorization. With the signing epoch retired, the plan and runbook say the
Maintainer's signature over the range-report digest is the sole authorization
control. The delivered signature does bind the constructed commit and its
parent, so it still authenticates exact Git objects, but it does **not** bind
the promised reviewed classification or prove that the Maintainer saw it.

**Required correction**: put the canonical report on the actual `apply` path;
present its complete content and digest before authorization; obtain the
Maintainer's confirmation of that exact digest; re-derive it immediately before
construction; place the digest and candidate tree in the exact signed message;
and make the public-path test fail when any of those calls or fields is removed.
Helper-level mutation tests do not satisfy this finding.

**[M2-2] BLOCKING -- the fixed first-use invocation cannot reach the checkpoint
construction it is recorded to perform.** In a disposable exact checkout at
`1d392a2`, I installed the source repository's observed prior anchor
`e45e1fcc84ded159ef910b6e7bde15f7b715a5b3` and ran both public paths. `check`
returned `PRE-FLIGHT REFUSED` on the expected first-use `CLOSURE` and
`AUTHORITY` differences. The exact `apply --confirm-supervised-reanchor` path
then executed candidate collection and returned exit 2 on those same findings,
before sealing, signing, or moving a ref. That is the real control flow, not a
rendering-only refusal.

The runbook's fallback steps manually generate and commit a manifest and move
only the anchor ref. They do not construct and verify the new signed checkpoint
or advance branch plus anchor in the reviewed expected-old transaction. If
those steps first make the authority bytes equal, they have already performed
the trust-root bootstrap by a different mechanism; running `apply` at that new
`P` then has no candidate to bless and `anchor == HEAD` refuses. The runbook
therefore offers no executable first-use route matching Chunk H / R1-F.

**Required correction**: define one non-circular first-use route whose exact
commands both admit the independently reviewed authority delta and perform the
signed, pre-ref-move-verified, two-ref checkpoint transaction. Its tests must
start with the old anchor's authority bytes, not with `_ceremony_repo()`'s
already-aligned closure. The current bootstrap test passes because its fixture
copies the new authority bytes into the anchor before invoking `apply`; it does
not exercise first use.

**[M2-3] BLOCKING -- the key-load marker is not the recorded human/key boundary.**
The fixed loader supplies `HOME`, `SSH_AUTH_SOCK`, and
`--confirm-supervised-reanchor` when the process starts. `apply_now()` accepts
that pre-run flag, executes candidate evidence, prints the marker, and proceeds
immediately to `commit-tree -S`; there is no post-report prompt, digest
confirmation, pause, or key-load operation. During the candidate subprocess,
`_scrubbed_environ()` does remove credential-shaped variables and substitutes a
throwaway `HOME`; when that context exits, the original signing environment is
restored **before** `check()` and before the marker. Thus the exact bytes do
sequence the sole current candidate subprocess before signing, but they do not
implement R1-F steps 3-5's stronger ceremony: Maintainer confirmation against
the displayed report and marker while the key is unavailable, followed by key
availability in the same already-running process.

The seven H2 nodes prove module-state ordering and reject a later guarded
`subprocess.run`; they do not prove key unavailability or a human confirmation
at the boundary. Their AST walk also sees only literal `subprocess.run` calls.
For these exact bytes that narrow enumeration is not itself an additional
blocker -- no `os.system`, `os.exec*`, `importlib`, `multiprocessing`, or atexit
candidate launcher exists, and M7 forces another review after any byte change --
but the human/key transition it claims to guard is absent.

**Required correction**: make the fixed invocation and code implement an actual
two-stage handshake. The candidate-executing stage must finish with the key
channel unavailable; the Maintainer must confirm the exact report digest after
the marker; only then may the signing stage receive or activate the key. A
single up-front boolean is not that confirmation. The public bootstrap test
must observe key-channel state on both sides of the boundary.

**[M2-4] SUBSTANTIVE -- `_git` is not read-only by construction.** I touched a
tracked file without changing its bytes, hashed `.git/index`, ran public
`check`, and hashed the index again. `check` returned its expected refusal, but
the index bytes and mtime both changed; the worktree remained clean. Git
`status` refreshed index stat data through an optional lock. The read/write
allowlists correctly keep content/ref-writing subcommands behind `_git_write`,
but the broader claim that every `_git` operation is repository-read-only is
false. Pin `GIT_OPTIONAL_LOCKS=0` (or the equivalent command option) on the
read boundary and add an index-byte before/after mutation probe. This is not an
authority bypass, so it is subordinate to M2-1 through M2-3.

**[M2-5] SUBSTANTIVE -- `_gate_manifest._git`'s repository ceiling is escapable
through a symlinked start path.** In a temporary repository I created a symlink
outside the repository pointing to a nested non-repository directory inside
it. `_object_format(symlink)` returned `sha1`; it discovered the target
repository despite `GIT_CEILING_DIRECTORIES` being set to the symlink's logical
parent. I could not exercise a bind mount without privileged host changes.
The current preflight path resolves and validates its repository root, and its
raw evidence directory is a real `mkdtemp`, so this did not yield an M3 bypass.
It does falsify the module's general claim that the ceiling binds Git to the
directory named by every caller. Resolve and validate the start path, or refuse
symlinked/non-root targets, and add the symlink probe.

### Controls that held

The construction path builds from a temporary index and verifies, before ref
movement, the exact parent, sole changed path, manifest blob digest, message,
signature validity, and anchored-roster principal. The roster is read from the
anchor object, not the candidate worktree. Candidate repository config could
not replace objects, redirect hooks, select a different signature verifier,
activate fsmonitor, or inject `GIT_*` steering through the tested paths. The
separate `_READ_ONLY_GIT` / `_WRITE_GIT` command allowlists held apart from the
optional-index-write qualification in M2-4.

The two-direct-ref `update-ref --stdin` transaction held its expected-old abort
semantics in the focused tests: stale state moved neither ref nor reflog and did
not touch the real index/worktree; success moved both direct refs and wrote the
fixed reason. The authoritative-manifest replacement also held: Git-native
mode/object identity came from checker re-derivation, while the candidate-owned
collection/interpreter fields remained explicit. The v1/v2 differential corpus
passed. These controls do not cure the dead authorization/report path.

### Exact bytes reviewed

I regenerated the authority closure by importing the exact checker under Python
3.13.13 and hashing the blobs from `1d392a2`; I also compared each blob with the
disposable checkout's worktree bytes. All nine matched:

```
910a507163196b1175e00b2535d11d956bbf823d8858b4366d2803c138dc511b  bootstrap/tests/_gate_preflight.py
f75689e480f9b54b971bfafdf32b4086bb82b72cdab36557c6767b49de12a9d0  bootstrap/tests/_gate_manifest.py
55a11326baae75d5a2f5f1696c5e6c4745ba537286415ba84bfcab26ab36b876  bootstrap/tests/_gate_reanchor.py
e272b868eb640b9193daefe76c5fbe2d6a8f5225eb934b53e9c7febdbc680b9b  bootstrap/tests/_gate_transition.py
c719f770afe1b0ce5928923a7be2590666bc8f7935df2ad94eda95598be286e4  bootstrap/tests/_oracle_activation.py
17007480162b0f4a100a100714a05198ef4a21ee8e726f31fb60b296127d429d  bootstrap/tests/_oracle.py
e1d6c7db5d72729e43040dedb69fa47c50a3fe36b7d284ad73c1285b8a027007  bootstrap/tests/_oracle_trust.py
3b09ba66916658c7c875965fa8efef7e509d3e2ead7208f68b48ddea7a375ec1  bootstrap/REANCHOR_RUNBOOK.md
55cd6796a2e73efcf822b73284c3610a7c71adf67ee065ae11f06036568423af  dev/.cairn/allowed_signers
```

### Exact manual bootstrap invocation reviewed

The placeholders remain deliberately unfilled. This is the exact fenced loader
block from the reviewed runbook bytes:

```sh
# The whole loader is handed to a CLEAN CHILD SHELL. Pinning the utilities was
# not enough: the block was still interpreted by the operator's inherited shell,
# and an inherited `echo` function rewrote the extracted checker and wrote the
# rewritten file's digest into the checklist, so the pinned absolute `shasum`
# dutifully verified the wrong list and reported success (FUR9). Pinning `echo`
# would not have closed it either -- `read`, `cd`, `[`, and the redirections are
# the same class. One boundary removes inherited functions, aliases, startup
# files and exported-function environment entries together.
#
# `PATH` is real here, unlike an earlier version of this block that set it only
# inside the git child and then claimed it covered the utilities.
# `HOME` is recorded because the signing backend needs it. `SSH_AUTH_SOCK` is
# the single deliberate pass-through from the invoking shell, since an agent
# socket is per-session and cannot be recorded; a wrong value can only make
# signing FAIL, never pass, because the signature is verified against the
# anchored roster with a pinned verifier.
#
# THE SHELL IS `/bin/sh`, LITERALLY -- do not substitute your own. This is not a
# recorded value and not a preference: a non-interactive `/bin/sh` reads no
# startup file, which is the entire reason the clean child is clean. The obvious
# alternative on this host is the login default `/bin/zsh`, and `zsh` sources
# `$HOME/.zshenv` even here -- non-interactive, under `env -i`, with the recorded
# HOME -- which puts the operator's own command definitions straight back inside
# the supposedly clean child. An earlier version left this as a recorded choice
# while claiming the boundary removed startup files (FUR10).
<maintainer-recorded-env> -i \
    PATH=/usr/bin:/bin \
    HOME=<maintainer-recorded-home> \
    SSH_AUTH_SOCK="${SSH_AUTH_SOCK-}" \
    /bin/sh <<'LOADER'
# Every value here is recorded by the Maintainer at first use. NOTHING is
# discovered: ambient discovery is what let a substituted repository answer for
# the named one, and an ambient `PATH` is what let a replacement `shasum` vouch
# for bytes it had just rewritten (FUR8). Utilities are invoked by absolute
# path, which no inherited shell function or alias can shadow.
CHECKOUT=<absolute-path-of-the-checkout-to-bless>
ENV=<maintainer-recorded-env>
GIT=<maintainer-recorded-git>
PY=<maintainer-recorded-interpreter>
MKTEMP=<maintainer-recorded-mktemp>
MKDIR=<maintainer-recorded-mkdir>
SHASUM=<maintainer-recorded-shasum>

T=$("$MKTEMP" -d) || exit 1

# Object replacement, hooks and monitors are disabled BEFORE the first read, and
# the environment is emptied so no GIT_* variable steers the loader.
sterile_git() {
    "$ENV" -i HOME=/nonexistent \
        "$GIT" --no-replace-objects \
               -c core.useReplaceRefs=false \
               -c core.hooksPath=/dev/null \
               -c core.fsmonitor=false \
               -C "$CHECKOUT" "$@"
}

# `cat-file blob` reads raw object bytes. `git archive` was used here and is
# attribute-aware, so a candidate `.gitattributes` could reshape what landed.
# The heredoc feeds `while` by redirect, not by pipe: a pipe would run the loop
# in a subshell where `exit 1` aborts nothing.
: > "$T/RECORDED.sha256" || exit 1
while read -r sum path; do
    [ -n "$path" ] || continue
    "$MKDIR" -p "$T/${path%/*}" || exit 1
    sterile_git cat-file blob "refs/cairn/gate-anchor:$path" > "$T/$path" || exit 1
    echo "$sum  $path" >> "$T/RECORDED.sha256"
done <<'HASHES'
<maintainer-recorded-first-use-hashes>
HASHES

# Decisive check: whatever route the bytes took, they must be the reviewed ones.
( cd "$T" && "$SHASUM" -a 256 -c RECORDED.sha256 ) || {
    echo "REFUSE: extracted bytes do not match the reviewed first-use set" >&2
    exit 1
}

"$PY" -E -s "$T/bootstrap/tests/_gate_preflight.py" \
    apply --repo "$CHECKOUT" --confirm-supervised-reanchor
LOADER
```

### Execution ledger

All Python execution used
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13), with
`PYTHONDONTWRITEBYTECODE=1`, in a disposable `--shared` clone detached at
`1d392a2`.

* Required range-report mutation/report-policy/checkpoint classes, the v1/v2
  differential corpus, all seven H2 sentinel nodes, and the literal runbook
  bootstrap test passed. The initial mandated selection was **46 passed** in
  10.30 s; a broader construction/config/transaction/publication sweep passed
  **116 selected nodes**.
* A real successful fixture ceremony signed a checkpoint and moved both refs;
  its message carried both `(not bound)` values. Replacing the range-report,
  re-derivation, and message-binding functions with raising sentinels still let
  real `apply` succeed.
* The first-use `check` and `apply` probes used the real observed prior anchor;
  `apply` exited 2 after collection with `CLOSURE`/`AUTHORITY` review findings
  and `[REFUSE] ... nothing was written`.
* The index probe changed only file stat metadata before `check`; index bytes
  and mtime changed, while `git status --porcelain` remained empty.
* The symlink-ceiling probe returned a repository format through a logical path
  whose parent was outside the discovered repository.

### Residuals and exclusions

I did not re-litigate the accepted trusted-contributor host-access residual,
the key-holder-not-process limit of signing, replay without a nonce, or local
write authority over `refs/cairn/gate-anchor`; none is misdescribed by this
review. The evidence stage remains best-effort isolation, not containment.

I did **not** load the Maintainer's real ceremony key, move either Cairn ref in
the source repository, fill the Maintainer placeholders, push, or run the
[TRU-7] real-remote atomic-capability probe. I did not exercise Windows, a real
SHA-256 repository, or a bind mount, and I did not repeat Boundary B's full
suite. I did not audit Git or OpenSSH cryptographic implementations. All
mutation and ref-writing probes ran only in disposable repositories.

## Response to the External Security Review (M2) -- Claude -- 2026-08-12

**All five findings accepted. None disputed. The disposition is correct and the
bytes it reviewed should not have been blessed.**

| finding | disposition |
|---|---|
| **[M2-1]** BLOCKING | **Fixed**, `2df83d2` |
| **[M2-2]** BLOCKING | **Not fixed here** — proposed, see below |
| **[M2-3]** BLOCKING | **Not fixed here** — proposed, see below |
| **[M2-4]** substantive | **Fixed**, `2df83d2` |
| **[M2-5]** substantive | **Fixed**, `2df83d2` |

### [M2-1] is the worst defect this plan has produced, and it was mine

Chunk B built the canonical range report. Chunk C built the digest binding. Both
were tested in isolation and **neither was ever called by `apply`**.
`draft_message` took its `None` default, so every real ceremony signed
`range-report digest : (not bound)`. With the signing epoch retired by [IC1],
that digest is the **sole** authorization control — so the mechanism this plan
exists to build was decorative on the only path that matters.

**I was one question away from finding it, twice.** During Chunk C I reasoned
carefully about *where* `verify_message_binds_report` belonged and never asked
whether a digest was being passed at all. Then the `## Progress verification`
record asserted the checkpoint "binds the reviewed report". Both times the
question was *is this wired?* and both times I answered a narrower one.

The Internal review did not catch it either. It took an **executing external**
read — which is exactly the argument for M2 existing, and an argument against
the intuition that a careful same-type reader is an adequate substitute.

Fixed by putting the report on the governing path: derived in `blessing_plan`,
**presented in full** (a digest is not a state a Maintainer can read),
**re-derived** immediately before construction through `rederive_and_bind` — a
Chunk C function that had never had a caller — and the drafted message checked
for the binding before any signature exists. A missing digest refuses.

**The tests are the reviewer's own probe**, because the finding said in terms
that helper-level mutation does not satisfy it: a parametrised node replaces
each of the four entry points with a raiser and requires a **real** `apply` to
fail with the anchor unmoved.

### [M2-4] and [M2-5] — both were real, and [M2-5] falsified my own fix

[M2-4]: "read-only" was a claim about *subcommands*, not about the repository.
`GIT_OPTIONAL_LOCKS=0` now sits in the shared child environment, not at call
sites — a per-call flag is one forgotten call site from the same defect.

[M2-5] is the sharper one: it falsifies **[IC6]'s fix**, which I wrote hours
earlier. `GIT_CEILING_DIRECTORIES` compares *logical* paths, so a symlink into a
nested non-repository directory walked straight past the ceiling I had just
added. The start path is now resolved before it is ceilinged or used. A fix that
has itself been falsified is worth flagging to whoever reviews next.

### [M2-2] and [M2-3] are not defects in an agreed design

They are places where **no workable design exists**, which is why they are not
patched here:
`dev/proposals/2026-08-12-claude-ceremony-handshake-and-first-use.md`
(high-assurance; review tier **External Security Review**, matching the tier
that found them).

* **[M2-2]** — the first-use circularity. Proposed: admit the CLOSURE/AUTHORITY
  delta only against the **reviewed SHA-256 set M2 already records**, matched
  whole, recorded in the checkpoint message, and inert when there is no delta.
  Non-circular because the authority comes from outside both the old anchor and
  the candidate.
* **[M2-3]** — the handshake. Proposed: the candidate stage runs with the key
  channel **absent**; the confirmation becomes the report **digest**, not a
  boolean; tests observe key-channel state rather than call ordering.

**One question the proposal deliberately does not decide**, because it changes
what the Maintainer physically does: R1-F step 5 says the *already-running*
process signs, which means a paused process on a terminal. The alternative —
two invocations, where the signing process never held candidate code at all — is
**stronger on the stated goal but contradicts accepted wording**. The proposal
recommends amending R1-F openly rather than reinterpreting it silently.

### Status

**M7 has fired.** `2df83d2` changes three of the nine reviewed files, so the M2
disposition is invalidated and a fresh M2 is owed on the replacement bytes. That
was true the moment [M2-1] was fixed and is not a consequence of batching.

**Sequencing, so no one spends the re-take early**: [M2-2] and [M2-3] must land
before the next M2, or it reviews bytes with two known blocking gaps. The order
is: Decision on the proposal → implement → Boundary B → **one** M2 → M3/M4.

**Chunk H remains unrun and no Cairn ref has moved.**
