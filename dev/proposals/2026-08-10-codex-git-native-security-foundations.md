<!-- cairn-internal-ref-allow: doctrine/coordination.md doctrine/dual-review.md doctrine/lifecycle.md doctrine/proposals.md doctrine/rationale.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
# Git-native security foundations: signed checkpoints, object validation, and durable trust refs

**Author**: Codex (Strategy / Security)
**Model**: GPT-5 (Codex)
**Date opened**: 2026-08-10
**Status**: proposed
**Touches**: `bootstrap/tests/_gate_preflight.py`,
`bootstrap/tests/_gate_manifest.py`, `bootstrap/tests/test_gate_preflight.py`,
`bootstrap/tests/test_gate_manifest.py`, `bootstrap/REANCHOR_RUNBOOK.md`,
`bootstrap/security_check.py`, `bootstrap/tests/test_security_check.py`,
`bootstrap/container/verify-ref.sh`, `bootstrap/tests/test_verify_ref.py`,
`bootstrap/SAFETY.md`, `bootstrap/PROVENANCE.md`, `SECURITY.md`,
`dev/strategy/2026-08-05-codex-security-strategy.md`, `dev/PLANNING.md`, and
`CHANGELOG.md`
**Related**: archived proposal and plan `gate-reanchor-preflight`; security
strategy owners [TRU-4], [TRU-5], [TRU-7], and [REL-4]; the Maintainer's
2026-08-10 drafting direction that routine signing caused agent commits to
fail and that Cairn should use Git's security primitives instead of building a
parallel set
**Plan review**: required(**External** + **External Security Review**) -- this
changes the local trust root, its manifest schema, release verification, and
the exact mechanism that authorizes unsigned agent work. Before the replacement
checker is first blessed, its exact bytes and the bootstrap invocation also
require a focused External Security Review.

## Context

Cairn already uses Git well at its highest-risk point. The gate preflight reads
raw objects with `cat-file` and `ls-tree`, establishes ancestry with
`merge-base` and `rev-list`, asks Git to verify SSH signatures, constructs the
checkpoint with `commit-tree -S`, and advances two refs through one
expected-old `update-ref --stdin` transaction. Cairn's surrounding code decides
which paths, principals, and refs matter and removes candidate-controlled Git
configuration from the decision path.

The boundary is not yet consistent. Some controls duplicate Git object logic,
some native integrity facilities are absent from decisive paths, and the
signing policy conflicts with the way agents actually work.

At exact commit `a09542ac6cc2078f64c729a6d94457ec7500da4b`, re-derived on
2026-08-10:

* repository-local `commit.gpgsign` is `false`, intentionally, because automatic
  signing interfered with agent commits;
* `refs/cairn/gate-anchor..HEAD` contains **487 commits** and all 487 fall at or
  after the recorded signing epoch;
* the live, pinned-roster `check_signatures()` reports **301 unsigned commits**;
  the other 186 verify as signed; therefore the next re-anchor is mechanically
  unable to pass even if every candidate byte and test result is correct;
* `git fsck --strict --no-dangling` exits 0, but neither the release security
  command nor release-source verifier records that native object-graph check;
* `refs/cairn/gate-anchor` exists but `git reflog exists
  refs/cairn/gate-anchor` exits 1, so its transitions have no Git-native local
  diagnostic history; and
* `bootstrap/security_check.py::_blob_oid` manually implements Git's blob
  framing and selects SHA-1 or SHA-256 from output width, even though read-only
  `git hash-object --stdin` already performs that operation under the
  repository's object format. A live Git 2.53.0 probe against a SHA-256
  repository returned the expected 64-hex object id without custom framing.

The unpublished-anchor issue is already recorded as [TRU-7]: ordinary pushes
do not transport `refs/cairn/*`, and the runbook says nothing about publishing
or recovering the durable anchor. The temporary
`refs/cairn/gate-authorization` ref is mentioned in the same finding, but it is
not the same kind of object: it grants one ceremony authority and should not be
made a durable remote capability merely because the anchor needs transport.

This proposal is not an argument that Git replaces security review. Git can
answer which bytes an object contains, whether a graph is structurally valid,
whether a key signed an object, and whether refs moved atomically. It cannot
decide which tests constitute the gate, whether scientific behavior is valid,
whether a reviewer was independent, or whether the person holding a key
understood what they approved.

## Proposal

Adopt one explicit division of responsibility:

| Property | Git owns | Cairn owns |
|---|---|---|
| Committed bytes and modes | object ids, trees, `cat-file`, `ls-tree`, `hash-object` | protected-path selection and allowed mode policy |
| History | parent links, reachability, ancestry | accepted range and expiry conditions |
| Object integrity | `fsck --strict`, fetch-time object checks | when integrity is decisive and how failure is reported |
| Key authentication | signed commit/tag objects and Git's verifier | out-of-band roster, exact signed name, and authorization meaning |
| Ref movement | expected-old transactions, no-deref behavior, reflogs | exact ref set, Maintainer fence, publication policy |
| Gate semantics | no native facility | pytest collection identity, skip/xfail policy, frozen-set exceptions, scientific/security review |

Custom code may constrain, sterilize, and interpret a Git command. It should not
reimplement a Git object algorithm when the native plumbing can produce the
same fact without executing candidate code or accepting candidate policy.

### A. Replace per-commit signing with Maintainer-signed checkpoints

Retire `_SIGNING_EPOCH` and the rule that every intermediate commit must carry
the Maintainer's signature. Unsigned commits are the normal agent-work format
and do not independently refuse a ceremony.

The authorization contract becomes:

1. The current `refs/cairn/gate-anchor` resolves to a direct ref whose commit
   carries a valid signature from the roster pinned by that trusted anchor.
2. Preflight re-derives the complete candidate evidence, authority closure,
   exact `anchor..HEAD` range, branch, parent, tree, and manifest content. It
   reports signed, unsigned, and foreign-signed intermediate commit counts as
   facts, not authorization verdicts.
3. `apply` constructs one new commit with exact parent `HEAD`, exact candidate
   tree plus the reviewed manifest, exact audit message, and an explicit `-S`
   signature. It verifies parent, changed path and mode, blob bytes, message,
   signature status, and pinned principal from the object before moving a ref.
4. Git advances the branch and `refs/cairn/gate-anchor` together in one
   expected-old, `--no-deref` transaction.
5. The resulting signed checkpoint authorizes that exact state and binds its
   complete parent history. It does not claim that the Maintainer authored or
   separately reviewed every intermediate commit.

Repository-wide `commit.gpgsign=true` is neither required nor recommended by
this contract. Release tags remain signed and name-bound under
`verify-ref.sh`; this proposal does not weaken that public provenance boundary.

The lost property is explicit: an unauthorized second person can create an
unsigned intermediate commit that is indistinguishable from an agent commit by
signature status alone. The checkpoint is safe only if the Maintainer reviews
the preflight result and controls the final signing act. The posture expires
before use when the checkout is not solely Maintainer-controlled, another human
gains ordinary write authority, or the ceremony is adopted outside Cairn. At
that point branch/forge authorization and contributor identity need a new
design; silently restoring automatic per-commit signing is not the default.

Signing still authenticates a key holder, not a human or process. The preferred
operational form makes the checkpoint key available only for the supervised
ceremony, without repository-wide automatic signing. If an agent process can
invoke the same key, the cryptographic statement remains only "this key signed
the checkpoint"; the Maintainer-only boundary is procedural under the accepted
trusted-contributor posture. A hardware-presence or separately loaded ceremony
key is a future strengthening, not a claim made here.

### B. Delegate Git object hashing and graph validation to Git

Replace `bootstrap/security_check.py::_blob_oid` with a sterile, read-only
`git hash-object --stdin` call. The call must never use `-w`, a path argument,
or attributes/filters. It hashes the bytes supplied on stdin under the
repository's object format and compares the returned full object id to
`ls-tree`.

Add native object validation at two decisive acquisition boundaries:

* `bootstrap/security_check.py` runs `git fsck --strict --no-dangling HEAD`
  before creating its detached execution tree. Failure is distinct from a
  scanner finding and fails the release check closed.
* `bootstrap/container/verify-ref.sh` fetches into its operator-created bare
  workspace with `-c fetch.fsckObjects=true`, then runs a strict reachable-object
  check before tag-name and signature verification.

No command changes global or repository Git configuration. Server-side
`receive.fsckObjects` is documented as a forge/operator option because Cairn
cannot enforce a remote server's configuration. `fsck` proves structural
object integrity, not authorization, safety, or signature validity; prose and
result labels must keep those claims separate.

### C. Move the frozen-file leg to Git object identity

Introduce gate-manifest schema `cairn-gate-manifest/v2`. For each tracked
frozen path, record the committed mode and Git blob object id derived from the
candidate commit's raw tree, plus the repository object format. Verification
uses `git hash-object --stdin` over worktree bytes and compares the mode and id
to the pinned entry. A target/trusted-repository object-format mismatch refuses
instead of comparing incomparable ids.

The behavioral contract stays:

* modification or deletion of an already pinned frozen path HOLDs;
* a newly added, tracked gate path is reported and joins the next checkpoint;
* an untracked file under a gate root HOLDs, because code that can affect
  collection or execution must be bound to a commit;
* symlinks, gitlinks, and unsupported modes refuse;
* cascade/phase-mutable entries record their prior Git mode and object id but
  retain their existing non-HOLD disposition; and
* pytest node ids, skip/xfail identities, mapping-symbol digests, and their
  asymmetric added/removed rules remain domain-specific manifest data. Git has
  no equivalent and this proposal does not flatten them into file identity.

SHA-256 remains appropriate for the out-of-band exact-byte first-use review,
for installed files outside Git, and for domain records whose contract is a
portable content digest. This proposal removes custom implementation of *Git
object ids*; it does not ban SHA-256 where the evidence channel deliberately
needs to be independent of a repository's object format.

If implementation probes show that v2 cannot preserve the existing
`--trusted-repo` cross-check, addition semantics, or mode refusals, this chunk
stops and records why the SHA-256 map remains. It does not ship a narrower
manifest merely to reduce code.

### D. Give custom refs native diagnostics and an honest transport story

Every successful local gate-anchor transaction uses `--create-reflog` and a
fixed reason identifying the ceremony. Tests prove a stale expected-old abort
changes neither refs nor either reflog. Reflogs are local, mutable diagnostics
for recovery and sequencing; they are never described as authentication or
tamper evidence.

After a successful Cairn ceremony, the runbook publishes the branch and
`refs/cairn/gate-anchor` in one `git push --atomic` operation with explicit
refspecs. If the remote does not support atomic push or rejects the custom
namespace, publication reports incomplete and stops; there is no silent
two-push fallback that can publish only half the state. The runbook then
resolves both remote refs and records their object ids.

`refs/cairn/gate-authorization` is explicitly ceremony-local and is never
published. It grants authority to the Stage-B transition. After successful
promotion, the runbook deletes it with its exact expected-old `A` value; a
failed deletion is reported as unresolved ceremony residue and never disguised
as cleanup success. Treating it as a backup ref would widen authority rather
than improve recovery.

Fresh-clone instructions use an explicit fetch refspec for the durable anchor.
Receiving that ref proves availability, not authenticity. Initial trust still
comes from a signed release/tag and independently obtained roster or from the
existing exact-byte bootstrap. The signed checkpoint and ancestry checks can
then bind the fetched anchor to that trusted history. Remote ACLs and custom-ref
protection are forge concerns and must be named as such, not attributed to
`git push`.

### E. Keep hooks and status output out of the authority model

Cairn may continue using pre-commit and post-commit hooks for intent
coordination. Security documentation will state that local hooks are bypassable,
replaceable, and not an authorization gate. No decisive release, trust-root, or
review claim may depend only on a hook having run.

Likewise, porcelain status and reflog output are evidence about local state, not
identity. Security-sensitive decisions remain bound to object ids, explicit
refs, verifier exit status, and pinned policy.

### F. Bootstrap and sequencing

The old anchored checker cannot authorize its replacement: it will reject the
existing unsigned range before reaching the new checkpoint rule. There is no
override flag.

Implementation therefore uses one explicit trust-root rule-change bootstrap:

1. Land implementation and focused tests without moving a Cairn ref.
2. Obtain an External code review and a separate focused External Security
   Review of the exact `_gate_preflight.py`, `_gate_manifest.py`, runbook, and
   imported authority bytes. The security review records their SHA-256 set and
   the exact manual bootstrap invocation.
3. The Maintainer confirms the reviewed commit and hashes, generates v2 evidence
   without trusting a handoff artifact, and constructs a signed checkpoint whose
   parent is that exact commit.
4. The Maintainer verifies the checkpoint object and advances branch and anchor
   through the reviewed expected-old transaction. No author or implementing
   agent performs this step.
5. Publish the durable anchor atomically with the branch, verify the remote
   object ids, and leave the authorization ref unpublished.
6. All later ceremonies execute the newly anchored checker normally.

The implementation plan must write the fixed manual commands before code review.
Chat-generated ceremony commands are not accepted evidence. Any byte change
after the exact-byte review invalidates that disposition.

### Documentation / doctrine surface

This changes Cairn's project security and release contracts, not the general
proposal/review doctrine. `bootstrap/SAFETY.md` records the Git-native division
of responsibility and hook limitation. `bootstrap/PROVENANCE.md` distinguishes
signed release tags from internal signed checkpoints. `SECURITY.md` states the
authorization and residual model. `bootstrap/REANCHOR_RUNBOOK.md` owns the
ceremony, reflog, publication, recovery, and bootstrap commands. The living
security strategy and `dev/PLANNING.md` replace the obsolete signing-epoch
tripwire and disposition [TRU-7]. `CHANGELOG.md` records the behavior change.

No adopter template gains mandatory commit signing. The public
`verify-ref.sh` behavior remains signed-release verification and gains only
native incoming-object validation.

### Doctrine-change rate-limit

No published Cairn doctrine changes. The high-risk classification independently
requires this proposal: it changes the local executable trust root, gate
manifest, signature disposition, and release verifier. The recurrence evidence
is nevertheless strong: per-commit signing blocked ordinary agent commits,
operations disabled it, and the unchanged gate accumulated an unsigned range it
must refuse. The control and the real workflow now contradict each other.

## Rationale

The goal is not fewer controls. It is fewer independently implemented claims
about facts Git already knows, and a more accurate placement of human
authorization.

Scientists using agents need commits to remain reliable and unattended enough
for ordinary development. Requiring every agent commit to reach a signing key
turns key prompts, unavailable agents, and harness behavior into development
failures while adding little process identity: the original design already
admitted that agents using the Maintainer's key were indistinguishable from the
Maintainer. One deliberate signed checkpoint is both less disruptive and more
truthful.

Using Git's object parser and transaction engine reduces security code Cairn
must maintain across SHA-1 and SHA-256 repositories. Adding `fsck`, reflogs, and
explicit ref transport uses mature native capabilities at the points where they
actually help, without inflating them into authenticity guarantees they do not
provide.

Maintainer preference during drafting, 2026-08-10: routine signing caused
problems for agent commits; the Maintainer agreed that agents may commit
unsigned while signed checkpoints and release tags carry authorization, and
asked that all identified Git-native consolidation items be proposed together.
This preference shapes the proposal and is not the lifecycle Decision.

## Alternatives considered

**Restore `commit.gpgsign=true` for every commit.** Rejected. It recreates the
observed agent failure and still authenticates only access to the shared key,
not who performed the work or review.

**Grandfather the 301 unsigned commits under a new signing epoch.** Rejected.
It repairs one blocked ceremony but preserves the incompatible policy and
guarantees another accumulation after automatic signing is disabled again.

**Rewrite and sign historical commits.** Rejected. It rewrites reviewed history,
invalidates citations and anchors, and assigns signatures after the fact without
proving contemporaneous authorization.

**Use signed notes or a signed JSON handoff artifact.** Rejected. Notes are
separately mutable refs, and a file carrying its own signature reintroduces a
handoff surface. The signed commit already binds tree, parent, message, and
history through Git's native object model.

**Treat `git fsck` as the release security gate.** Rejected. A malicious but
well-formed repository passes `fsck`. It is one structural-integrity leg before
signature, scanner, test, and policy checks.

**Replace the entire gate manifest with `git diff`.** Rejected. Git cannot
represent pytest collection identity, skip/xfail changes, mutable exceptions,
or the asymmetric rule that new tests are recorded while removed tests HOLD.
Only the file-identity leg migrates.

**Publish every `refs/cairn/*` ref.** Rejected. The durable anchor needs
transport; the authorization ref is a temporary capability and publishing it
would widen the attack surface.

**Do nothing.** Rejected. The next ceremony is already blocked by a policy the
repository intentionally stopped following, and custom object hashing remains
unnecessary security-sensitive code.

## Evidence / verification plan

### Tests required

* Extend `bootstrap/tests/test_gate_preflight.py` with unsigned and mixed
  intermediate ranges that reach a valid signed checkpoint; invalid prior
  anchor signature, wrong principal, unsigned constructed checkpoint, wrong
  parent/tree/message, roster drift, direct-ref, stale expected-old, reflog
  success, reflog abort, and `commit.gpgsign=false` cases.
* Extend `bootstrap/tests/test_gate_manifest.py` with v1 refusal/migration,
  SHA-1 and SHA-256 object formats, mode changes, symlink/gitlink refusal,
  modified/missing/new tracked files, untracked gate files, object-format
  mismatch, trusted-repository verification, collection identity, and mutable
  exception behavior.
* Extend `bootstrap/tests/test_security_check.py` with SHA-1/SHA-256
  `hash-object --stdin`, proof that no object is written, strict-fsck success,
  a malformed reachable-object negative control, and distinct command-error
  reporting.
* Extend `bootstrap/tests/test_verify_ref.py` with fetch-time object checking,
  strict-fsck refusal, unchanged signed-name/signature behavior, and proof that
  candidate Git configuration cannot disable either object check.
* Add runbook literal-block tests for `--create-reflog`, atomic durable-ref
  publication, no partial-push fallback, remote verification, expected-old
  authorization-ref deletion, and absence of `gate-authorization` from every
  push/fetch publication block.
* Run the complete canonical suite once at the final stable implementation
  boundary. Ceremony suites remain exhaustive; this proposal does not apply
  ordinary-suite runtime optimizations to them.

### Examples / smoke checks

* In throwaway repositories, execute the public `check` and `apply` paths over
  an unsigned agent range and verify the resulting checkpoint with Git against
  a pinned throwaway roster.
* Corrupt a reachable object created with test-only Git plumbing and show both
  release acquisition paths fail before making signature or scanner claims.
* Run a two-ref stale expected-old transaction and prove refs and reflogs are
  unchanged; run success and prove both reflogs identify the ceremony.
* Exercise atomic push against a local bare remote and inject rejection of one
  ref, proving neither remote ref moves.
* Run `scripts/check_cairn.py`, claim/link checks, the security lint, and the
  gate-manifest/AST standing checks over every changed protected surface.

### Docs required

The documentation surfaces named under `Proposal > Documentation / doctrine
surface` are required. No proposal/plan doctrine or adopter commit-signing
instruction changes.

### Author-accounting -- invariants, failure modes, edge cases

| Invariant or edge | Enforcer / decisive evidence |
|---|---|
| Agent commits may be unsigned; authorization occurs only at a signed checkpoint | no range-signature refusal; public-path mixed-range test; exact checkpoint verification |
| The prior and new anchors are signed by a pinned principal | Git signature verification with roster supplied from the trusted anchor; wrong-key and unsigned mutations |
| A signature does not claim human authorship or review | explicit docs and output language; no author/committer-name authorization fallback |
| Candidate configuration cannot steer Git security commands | one sterile launcher, all `GIT_*` variables removed, command-line config pins, hostile config fixtures |
| Git object ids are computed by Git without writing | `hash-object --stdin` without `-w`; object-directory before/after test |
| `fsck` failure cannot become CLEAN or a signature verdict | typed fail-closed result and malformed-object negative control |
| Manifest v2 preserves frozen and collection semantics | v1/v2 differential corpus and independent mutation tests for every disposition |
| Reflog is diagnostic only | docs plus no decision predicate consuming reflog content |
| Branch and anchor publish together or neither does | local-bare-remote atomic rejection test |
| The authorization ref never leaves the ceremony repository or survives successful use | literal runbook tests, expected-old deletion, and remote-ref assertion |
| First use cannot self-authorize changed checker bytes | exact-byte External Security Review, Maintainer-recorded hashes, fixed manual bootstrap, no override |

**Public paths to tests:** `_gate_preflight.py check|apply` ->
`bootstrap/tests/test_gate_preflight.py`; `_gate_manifest.py produce|verify` ->
`bootstrap/tests/test_gate_manifest.py`; `bootstrap/security_check.py` ->
`bootstrap/tests/test_security_check.py`; `bootstrap/container/verify-ref.sh` ->
`bootstrap/tests/test_verify_ref.py`; runbook loader/publication blocks -> the
literal-block tests in those gate modules.

**Known omissions.** This does not authenticate the human at the keyboard,
contain candidate collection, secure a compromised Maintainer machine, define
forge-specific custom-ref ACLs, add transparency logging, or make the internal
gate an adopter feature. It does not convert Git object integrity into code
safety. Windows and non-OpenSSH signing behavior remain unproven unless the
implementation plan adds hosts and exact acceptance evidence.

#### Security preflight -- five questions

**S1 -- Who supplied it?** The candidate supplies object ids, paths, commits,
and tags to inspect. Git parses those objects. Expected refs are fixed by
reviewed code; signer keys come from the prior trusted anchor for re-anchor and
from an operator-supplied roster for releases. The candidate never supplies the
roster that authenticates itself.

**S2 -- Can it fail?** Removing `-S`, changing the checkpoint parent, using an
unpinned key, corrupting a reachable object, modifying a frozen blob, changing
its mode, adding an untracked gate file, forcing one atomic-push ref to reject,
or reintroducing `gate-authorization` into publication each has a named red
test. Deleting a test's decisive mutation is itself a coverage failure.

**S3 -- What fires it, over what?** The Maintainer-run re-anchor command fires
checkpoint, manifest, ref, and publication checks over the exact anchor-to-HEAD
range and protected gate set. `bootstrap/security_check.py` fires object
validation over the release commit before its full release phases.
`verify-ref.sh` fires fetch/fsck/name/signature checks over the exact requested
tag and reachable objects. None is represented as CI.

**S4 -- Which way does it break?** Unknown object formats, Git errors,
unclassifiable signature results, malformed manifest entries, unsupported
modes, fsck failures, non-atomic remotes, and stale refs all refuse. Reflog
absence can only remove diagnostics and never grants authority. Intermediate
unsigned commits deliberately do not refuse under the accepted checkpoint
model.

**S5 -- Who still wins?** An actor controlling the Maintainer machine or able
to invoke the checkpoint key can create an apparently authorized checkpoint.
An unauthorized person can add an unsigned intermediate commit if they gain
write access; the Maintainer must catch its content/range before signing. The
class is not closed. Sole-control and ceremony-key assumptions are dated
residuals with explicit expiry triggers.

## Signals the change is wrong

* Agent commits still prompt for or fail on signing. Remove any accidental
  repository-wide signing dependency before proceeding.
* A checkpoint can be created without an explicit signature or accepted under
  an unpinned principal. Stop; do not move or publish refs.
* Manifest v2 misses a mutation v1 caught, changes collection dispositions, or
  cannot verify through `--trusted-repo`. Retain v1 and record the failed
  migration rather than narrowing the gate.
* `fsck` reports authentication or code safety instead of structural integrity.
  Correct the claim and result vocabulary.
* A remote can receive branch or anchor alone after the publication command
  reports success. Stop publication and retain the local anchor until the
  transport design is corrected.
* Any process treats a reflog as tamper evidence or the remote anchor as
  self-authenticating. Remove that authority claim.
* The bootstrap requires executing candidate checker bytes before their
  reviewed hash is established, or an implementing agent can perform the
  Maintainer step. The trust transition is invalid.

## Reviewer brief

The External Security Reviewer should attack four claims by execution:

1. prove whether a signed checkpoint's exact parent and tree really bind an
   arbitrary unsigned intermediate range without implying per-commit identity;
2. inject candidate Git configuration, malformed objects, SHA-256 repositories,
   symlinks, modes, and untracked gate files against the native object paths;
3. force local and remote transaction aborts and inspect every ref and reflog;
4. execute the proposed first-use bootstrap from the old anchor and identify
   the first byte or command whose authority is not established externally.

The review should explicitly adjudicate the lost second-person detection and
the ceremony-key residual rather than treating usability as sufficient risk
acceptance.
