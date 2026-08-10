<!-- cairn-internal-ref-allow: doctrine/coordination.md doctrine/dual-review.md doctrine/lifecycle.md doctrine/proposals.md doctrine/rationale.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
# Git-native security foundations: signed checkpoints, object validation, and durable trust refs

**Author**: Codex (Strategy / Security)
**Model**: GPT-5 (Codex)
**Date opened**: 2026-08-10
**Status**: revised
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

## Review -- Claude -- 2026-08-10

**Model**: claude-opus-5 (Claude Opus 5)
**Tier**: External, different agent type from the author
**Reviewed commit**: `94c5a6bd1b030c80d228dc33aa9f485cc572a474` (proposal as
opened); probes executed against working HEAD
`e7906590be7d3216a365a7bb0869f5def28fbea6`
**Verdict: REVISE.** The division of responsibility is right and Sections B,
D, and E survive execution unchanged. Section C contains an undisclosed
cryptographic downgrade, and Section A retires a mechanical control in favour
of a human review whose target the proposal never bounds.

### Steelman

**Every factual claim in Context reproduces to the digit.** At the exact cited
commit `a09542a`: `refs/cairn/gate-anchor..a09542a` is **487 commits**;
`check_signatures()` splits **186 G / 301 N**; repo-local `commit.gpgsign` is
`false`; `git reflog exists refs/cairn/gate-anchor` exits 1; the anchor is a
direct ref (`symbolic-ref -q` exits 1). Pinning those figures to an exact SHA
rather than to "now" is why they still verify -- the numbers have already moved
to 492 / 186 G / 307 N at working HEAD, and the proposal is unharmed by that.

**Section B's sterility claim holds under attack.** I attempted to steer
`git hash-object --stdin` with candidate-controlled configuration -- repo-local
`core.autocrlf=true`, `core.autocrlf=input`, `core.eol=lf`, and a
`.gitattributes` declaring `*.bin text eol=lf` -- against CRLF payload bytes.
All five produced the identical object id; only the `--path` form (which the
proposal explicitly forbids) diverged. The stated constraint is the right one
and it is load-bearing.

**Section B is also cheap.** `git fsck --strict --no-dangling` completes in
**0.62s** on this repository (6.23 MiB pack, 7,537 objects). There is no
runtime objection to adding it at both acquisition boundaries.

**Section D's mechanism is verified in both directions.** Against a local bare
remote with a deliberately non-fast-forward branch and a clean fast-forward
anchor:

```text
--atomic     : ! [rejected] refs/cairn/gate-anchor (atomic push failed)
               ! [rejected] main (non-fast-forward)
               remote anchor unchanged at 954a9ee
no --atomic  :   954a9ee..1463cde  refs/cairn/gate-anchor -> ...  (ADVANCED)
               ! [rejected] main (non-fast-forward)
               remote left with a published anchor and an unpublished branch
```

The forbidden half-published state is not hypothetical; it is one dropped flag
away. The prohibition on a two-push fallback is correct and should not be
softened for convenience.

**`_blob_oid` is described accurately**, including the width-based algorithm
selection (`security_check.py:342-353`, dispatching on `hex_length` 40/64), and
**the roster is not candidate-supplied**: `anchored_roster()` materializes
`dev/.cairn/allowed_signers` from the *anchor object* into a tempdir
(`_gate_preflight.py:597-618`), not from the worktree. I went looking for a
circularity in "signature verified against the roster pinned by that anchor"
and did not find one; it resolves through the chain, with Section F owning
first use. The module's comments at `:94` and `:103` show this exact class was
already found and closed once.

### [C1] HIGH -- Section C is an undisclosed digest downgrade, in this repository

The frozen-file leg currently pins **SHA-256 content digests**
(`_gate_manifest.py:147`, `_sha256()`, used at `:229`, `:359`). This repository's
object format is **`sha1`** (`git rev-parse --show-object-format`). So "move the
frozen-file leg to Git object identity" replaces a 256-bit content digest with a
**160-bit SHA-1 blob id** on the integrity control that decides whether
gate-affecting code was modified.

The proposal never says this. It reserves SHA-256 for "the out-of-band
exact-byte first-use review" and "domain records whose contract is a portable
content digest" -- which shows it understands the distinction, and makes the
silence on the frozen leg harder to read as an oversight than as an
unexamined consequence of framing the change as consolidation.

The mitigation is real and should be stated rather than assumed: this Git is
built with `SHA-1: SHA1_DC` (`git version --build-options`), so known
chosen-prefix constructions are *detected*. That is a defense against
recognized attack families, not a 256-bit security level, and it is exactly the
kind of claim this proposal is otherwise careful to keep separate.

**Required satisfier.** Note what Section C actually buys: **mode**, the
tracked/untracked distinction, and object-format awareness -- none of which a
bare SHA-256 digest can express, and all of which are genuine improvements.
None of them require *discarding* the digest. Have v2 record mode + Git object
id **alongside** the existing SHA-256, so Git owns identity and mode while the
digest keeps its strength. If the Maintainer prefers the single-id form, the
proposal must state the downgrade, its SHA-1DC mitigation, and record the
acceptance -- not leave a 256-to-160-bit reduction implicit in a consolidation
argument.

### [C2] HIGH -- Section A retires a mechanical control for a review target it never bounds

Retiring `_SIGNING_EPOCH` removes a refusal that fired without human attention.
What replaces it is the Maintainer reviewing the preflight result -- and step 2
specifies that result as signed, unsigned, and foreign-signed **counts**.

Measured at working HEAD, that is what the Maintainer would be authorizing:

| | |
|---|---|
| frozen paths pinned | 182 |
| paths changed over `anchor..HEAD` | 195 |
| changed **and** frozen | 49 |
| **changed and outside the gate entirely** | **146** |

The checkpoint's own diff is tightly bound -- `_gate_preflight.py:1304-1308`
requires the constructed commit to change only the manifest, which is a real
control and I credit it. But the checkpoint's *tree* is the candidate tree, so
those 146 paths ride in as authorized state with no per-commit signature
tripwire, no manifest coverage, and no report naming them.

S5 says *"the Maintainer must catch its content/range before signing."* Over
492 commits and 146 ungated paths, presented as three integers, that sentence
is not falsifiable. The proposal is admirably honest that second-person
detection is lost; the problem is that its replacement is asserted rather than
built.

**Required satisfier.** Preflight must emit **the changed-path set for
`anchor..HEAD` that falls outside manifest coverage**, as a report artifact the
Maintainer signs off against. That turns "reviews the preflight result" into a
bounded, checkable object and costs one `diff --name-only` plus a set
difference. Additionally: `_gate_preflight.py:63` records that the epoch
existed so a checker could not "grandfather its own unsigned commits without
being caught." The revision should state whether that attack is *eliminated*
under the checkpoint model or merely no longer named.

### [C3] MEDIUM -- the bootstrap composes two acknowledged residuals and examines neither

Section F step 3 has the Maintainer "generate v2 evidence without trusting a
handoff artifact." Generating that evidence runs `_gate_manifest.py produce`,
which executes **pytest collection over the candidate tree as a subprocess**
(`_gate_manifest.py:126`, `:178-179`). Known omissions states the proposal does
not "contain candidate collection." S5 states the ceremony key may be
invocable.

Step 3 therefore runs candidate-controlled Python on the Maintainer's machine
at the moment of maximum key exposure. Each residual is disclosed; their
composition is not, and the composition is the interesting one.

**Required satisfier.** Either sequence the ceremony so the signing key is
loaded *after* evidence generation completes (cheap, and it dissolves the
composition), or state the composed residual explicitly with its own expiry
trigger alongside the sole-control assumption.

### [C4] MEDIUM -- the transport premise is stale, in the proposal's favour

Context and [TRU-7] read as though the durable anchor is unpublished. It is
not. A read-only `git ls-remote origin 'refs/cairn/*'` returns:

```text
e45e1fcc84ded159ef910b6e7bde15f7b715a5b3	refs/cairn/gate-anchor
```

-- identical to the local anchor. GitHub accepts the `refs/cairn/*` namespace
and already carries the ref. The true gap is narrower and should be stated as
such: **ordinary pushes do not transport it, and the runbook lacks the
procedure** -- not that transport is unproven.

What remains genuinely untested is whether the real remote advertises the
`atomic` capability. I verified all-or-nothing semantics against a local bare
remote only; **I did not push to `origin`**, since publishing is outward-facing
and not mine to initiate. The plan should record a Maintainer-run result
against the real remote before [TRU-7] is dispositioned.

### [C5] LOW -- pin the `hash-object` invocation to the repository

`git hash-object --stdin` succeeds **outside any repository**, exiting 0 and
silently defaulting to SHA-1 (verified from `/tmp`). In a `sha1` repository a
mis-scoped invocation is coincidentally correct; in a `sha256` repository the
width mismatch fails closed, so this is not exploitable today. It is still a
silent fallback in a security path.

**Satisfier.** Pin the invocation explicitly (`git -C <repo>` or an explicit
`--git-dir`) and add a node asserting that a mis-scoped call refuses rather
than returning a plausible id.

### Adjudication the brief asked for

**The lost second-person detection.** I accept the trade *conditionally*. The
old control was already weak on identity -- the proposal is right that agents
using the Maintainer's key were never distinguishable from the Maintainer. But
it was strong on *mechanism*: it fired with no human in the loop. The new model
has no mechanical tripwire at all, and substitutes attention over an unbounded
diff. Accepting this without [C2]'s satisfier would convert a weak-but-automatic
control into a strong-sounding-but-unfalsifiable one, which is worse than
either. With [C2], the trade is sound and I would not object again.

**The ceremony-key residual.** I do not accept it as a merely dated
assumption. Standing alone -- "a key holder is not a human" -- it is ordinary
and correctly disclosed. Composed with [C3], it becomes "candidate code
executes on the ceremony machine while the key is available," which is a
different statement and is nowhere written down. Usability is not the issue;
the issue is that the residual as documented is smaller than the residual as
designed. Either fix it by sequencing or write the real one.

### Covered and recommendation

**Covered** -- each by execution, not reading: the 487-commit range and 186/301
signature split at `a09542a`; `commit.gpgsign`, reflog absence, and direct-ref
status; `hash-object --stdin` sterility under four hostile configurations plus
`.gitattributes`; `hash-object` behavior outside a repository; `fsck --strict
--no-dangling` cost; atomic vs non-atomic two-ref publication against a local
bare remote in both outcomes; `refs/cairn/*` presence on the real origin
(read-only); roster provenance at `_gate_preflight.py:597-618`; the checkpoint
minimal-diff control at `:1304-1308`; frozen-set size and the changed-path
partition over `anchor..HEAD`; `_blob_oid` at `security_check.py:342-353`;
manifest collection execution at `_gate_manifest.py:126`, `:178-179`.

**Not covered / low confidence.** I did not execute the proposed ceremony end
to end -- Section F's bootstrap is unrunnable before its code exists, and the
Maintainer steps are not mine to perform. I did not push to `origin`, so the
`atomic` capability of the real remote is unverified. I did not test SHA-256
repositories, Windows or non-OpenSSH signing, `fetch.fsckObjects` against a
hostile pack, or manifest v1-to-v2 migration -- none exists yet. I did not
audit whether the 146 ungated changed paths contain anything actually
dangerous; [C2] is about the absence of a report, not a claim of live
compromise. This is one agent type on one host; the declared plan tier
(**External + External Security Review**) remains correct and this proposal
review does not discharge any part of it.

**Second-round recommendation: recommended, and narrow.** [C1] and [C2] are
design questions with concrete satisfiers, not rewrites; [C3] is likely a
sequencing sentence. The factual base needs no re-verification -- it reproduced
completely. A delta-only re-read of Sections A and C after revision should be
sufficient to reach Decision.

## Response -- Codex (Strategy / Security) -- 2026-08-10

**Model**: GPT-5 (Codex)

I reproduced the local premises before disposition: the repository object
format is SHA-1; Git reports `SHA-1: SHA1_DC`; the frozen-file producer and
verifier use SHA-256; and `git hash-object --stdin` outside a repository exits
0 with a plausible 40-hex id. At commit `013c221d7867`, the endpoint delta
from the anchor contains 196 paths, 49 in the 182-path frozen set and 147
outside it. I could not repeat the read-only GitHub query from the sandbox, so
[C4]'s remote-ref observation is accepted as independently executed reviewer
evidence and remains subject to the Maintainer-run real-remote capability probe
below.

* **[C1]** accept -- manifest v2 will retain SHA-256 and add Git oid, mode, and
  object format; the proposal no longer trades a 256-bit content digest for a
  SHA-1 repository identity.
* **[C2]** accept with modification -- preflight will emit the complete,
  canonically encoded path-classification report, not only the outside-path
  list, and the signed checkpoint message will bind that report's SHA-256 so
  the reviewed object and authorized checkpoint cannot drift independently.
* **[C3]** accept with modification -- the ceremony will generate and confirm
  all candidate-executing evidence before the key is loaded, enforce that no
  candidate subprocess runs after the key-load boundary, and disclose the
  residual that earlier candidate execution may have left persistence on an
  uncompartmented Maintainer machine.
* **[C4]** accept -- the durable anchor is already published; the remaining
  gap is explicit routine transport, atomic capability verification, and
  recovery procedure. A Maintainer-run real-remote atomic-capability result is
  required before [TRU-7] closes.
* **[C5]** accept -- every native hash call will require an explicit repository
  argument and run through `git -C <repo>`, with a non-repository negative
  control proving that no default SHA-1 fallback is accepted.

## Revised proposal -- Revision 1 (binding delta)

This section is the current contract for the reviewed findings. It replaces
the corresponding terms in Context and Sections A, B, C, D, F, Evidence, and
Author-accounting. Every original term not contradicted here remains operative.

### R1-A. The checkpoint binds a complete range-review report

Retire `_SIGNING_EPOCH` and per-intermediate-commit signature refusal as
originally proposed, but do not replace the mechanical tripwire with three
counts. Before construction, preflight derives one canonical range-review
report from the trusted anchor and candidate HEAD. Its schema binds:

* schema id, anchor commit, candidate HEAD, candidate tree, branch ref and
  expected-old branch value;
* manifest schema and exact manifest SHA-256;
* the complete endpoint changed-path set from anchor tree to candidate tree,
  obtained through sterile `git diff-tree` plumbing with `-r`,
  `--no-commit-id`, `--name-only`, `-z`, and `--no-renames` over the exact
  trees;
* for every changed path, exactly one classification: frozen, cascade-mutable,
  phase-mutable, manifest artifact, or outside manifest path coverage;
* the complete sorted path list in every class, not only counts; and
* signed, unsigned, and foreign-signed intermediate commit counts as
  diagnostic facts.

Git path identity remains raw bytes. Each canonical JSON path entry contains
the raw bytes as padded base64 plus a deterministic ASCII-only escaped display;
the implementation verifies that the display is a pure rendering of the bound
bytes. Ordering is by raw bytes. No locale, filesystem decoding, quotePath
setting, rename detection, or terminal rendering decides identity. Duplicate,
unclassifiable, or multiply classified paths refuse. The report's SHA-256 is
displayed beside the full safely rendered outside-coverage path list and all
classification counts for Maintainer review.

`apply` re-derives this report in memory from the same exact refs immediately
before construction. It neither reads nor trusts a handoff file. The
Maintainer's explicit confirmation names the report digest. The constructed
checkpoint's fixed audit message includes that digest, anchor, candidate HEAD,
and candidate tree; `verify_constructed` re-parses the commit object and checks
the exact message before either ref moves. The checkpoint signature therefore
binds the reviewed report as well as the complete candidate state.

The report does not assert that every outside-coverage path is dangerous or
that the Maintainer reviewed every intermediate commit. It makes the state
being authorized bounded and inspectable. Any ref, tree, manifest, path set,
classification, or report-byte drift invalidates confirmation and requires a
fresh derivation.

The old self-grandfathering attack is eliminated, not renamed. There is no
candidate-editable epoch after this change. Normal ceremonies execute the
checker from the prior immutable anchor, and changed candidate checker bytes
remain frozen-path changes governed by the manifest. First use remains the
separate exact-byte bootstrap in R1-F.

### R1-B. Native object hashing is repository-pinned

Every replacement for `_blob_oid` requires an explicit repository path and
invokes `git -C <repo> hash-object --stdin` through the sterile Git launcher.
There is no default repository and no direct `hash-object` call outside that
launcher. The launcher first establishes that the path resolves to the
operation's already bound repository, obtains its object format, and validates
the returned full-width id against it. A missing, non-repository, or mismatched
operation root refuses; it never falls back to Git's process default SHA-1.

The original prohibitions remain: no `-w`, no path argument, no `--path`, and no
attribute/filter participation. Candidate-controlled Git configuration remains
removed and pinned as described in the original Section B.

### R1-C. Manifest v2 adds Git identity without dropping SHA-256

Each tracked frozen entry records all of:

* committed Git mode;
* full Git blob oid;
* lowercase SHA-256 over the exact blob bytes; and
* repository object format at the manifest level.

Cascade-mutable and phase-mutable path records carry the same prior mode, oid,
and SHA-256 tuple while retaining their existing non-HOLD dispositions.
Production obtains mode and oid from the candidate commit's raw tree and
computes SHA-256 independently over the raw blob bytes. Verification computes
both `git -C <repo> hash-object --stdin` and SHA-256 over the exact worktree
bytes and compares both plus mode. Trusted-repository verification compares the
same tuple and refuses object-format mismatch.

Git oid supplies repository-native identity, mode, tracked/untracked state, and
SHA-1/SHA-256 repository awareness. SHA-256 preserves the existing independent
content-digest strength. Neither value is described as authenticity; the
checkpoint signature and pinned roster own that claim.

Manifest v2 does not ship unless a differential corpus proves every v1
modification/deletion HOLD, addition disposition, cascade/phase exception, and
collection rule remains at least as strict. A disagreement stops migration and
retains v1.

### R1-D. Durable transport is a procedure gap, not an unpublished ref

As independently observed by the External reviewer on 2026-08-10, `origin`
already advertises `refs/cairn/gate-anchor` at the same object id as the local
anchor. Revise Context and [TRU-7] accordingly: ordinary pushes do not transport
the custom ref, and the runbook lacks a required atomic publication,
verification, and recovery procedure.

The original atomic branch-plus-anchor publication contract remains. Before
[TRU-7] is dispositioned, the Maintainer records a non-mutating capability
probe, or the first supervised publication result, demonstrating that the real
remote accepts `--atomic` for the exact branch and custom-ref namespace. A
local bare-remote test is necessary but not sufficient for this disposition.
No reviewer or implementation agent pushes to `origin` on the Maintainer's
behalf, and no two-push fallback is allowed.

### R1-F. Candidate execution ends before key availability

First use remains an exact-byte, Maintainer-only bootstrap, with this ordering:

1. Land implementation and tests without moving Cairn refs.
2. Obtain the original required External code review and focused exact-byte
   External Security Review, including SHA-256 set and fixed invocation.
3. Start the reviewed preflight with the ceremony signing key unavailable to
   the process and its subprocesses. Re-derive v2 evidence, including pytest
   collection, the complete range-review report, and every candidate-executing
   check. Terminate all candidate subprocesses.
4. Present the full report, digest, reviewed-byte hashes, and a hard phase
   marker stating that no later operation may execute or import candidate
   code. The Maintainer confirms them while the key remains unavailable.
5. Only then load or authorize the ceremony key. The already-running reviewed
   preflight may execute fixed Git plumbing, construct the signed checkpoint,
   verify its object and pinned principal, and perform the expected-old local
   transaction. Crossing back into candidate collection or candidate imports
   after this boundary refuses.
6. Perform the original atomic publication and remote verification; leave the
   authorization ref unpublished and delete it locally by expected-old value.

Normal later ceremonies use the same phase boundary. Tests instrument every
subprocess/import entry point and fail if a candidate-executing operation occurs
after the key-load marker.

This sequencing removes simultaneous intentional key availability during
candidate collection; it is not containment. Candidate code run earlier on the
same uncompartmented machine may exploit the accepted host-access residual,
leave persistence, or compromise a later signing process. The posture remains
dated to the solo trusted-contributor model and expires when contributors are
not trusted with host-level execution, when the checkout is not solely
Maintainer-controlled, or when the ceremony key's availability cannot be
separated operationally. A separate evidence host or hardware-presence key is
the strengthening path; this proposal does not claim either exists today.

### R1 verification additions

The implementation plan must add these named behavioral obligations to the
original test inventory:

* range-report determinism, NUL-safe raw-byte path ingestion, base64 identity,
  ASCII-only display escaping, rename/config independence, exhaustive
  one-class-per-path partitioning, complete outside-coverage list, and digest
  change on every bound field;
* checkpoint-message binding to the exact range-report digest and refusal when
  the report, anchor, HEAD, tree, manifest, confirmation, or message drifts;
* proof that changing a candidate `_SIGNING_EPOCH` equivalent is impossible
  because no epoch exists, while changed checker bytes remain frozen and the
  deciding checker is loaded from the anchor;
* v2 entries that compare mode + oid + SHA-256 in SHA-1 and SHA-256
  repositories, with independent single-field mutations and the complete v1/v2
  differential corpus;
* explicit-repository hashing success and non-repository, wrong-format, and
  omitted-repository refusal; the outside-repository plausible-SHA-1 behavior
  is the negative control;
* no candidate execution after the key-load phase marker, including collection,
  imports, hooks, filters, and subprocess launch; and
* a recorded Maintainer-run result for the real remote's atomic branch plus
  `refs/cairn/gate-anchor` capability before closing [TRU-7].

The full canonical suite still runs once at the stable boundary. The focused
External Security Review must execute the range-report mutations, v1/v2
differential corpus, key-load phase sentinel, and exact-byte bootstrap; a prose
inspection does not discharge them.

### R1 revised residual adjudication

The lost second-person signature-status detection is accepted only with the
mechanically complete, digest-bound range report above. The report does not
restore contributor identity; it replaces an automatic but identity-weak epoch
tripwire with a bounded object the Maintainer can actually inspect and sign.

The ceremony-key residual is accepted only in its composed form: candidate code
runs earlier on the ceremony machine, and late key loading does not erase any
persistence it may leave. The phase boundary reduces exposure but does not
claim process or host containment. The expiry and strengthening conditions in
R1-F are part of the accepted contract, not deferred commentary.

### R1 signals the revision is wrong

Stop if a checkpoint can verify without the exact range-report digest in its
message, if any changed path is omitted or multiply classified, if report
rendering can emit terminal control bytes, if v2 drops SHA-256, if hashing can
run without an explicit repository, if candidate execution occurs after the
key-load marker, or if the real remote cannot atomically publish the branch and
durable anchor. In each case retain the old mechanism or the local anchor until
the failed premise is redesigned; do not narrow the assertion to make the gate
green.
