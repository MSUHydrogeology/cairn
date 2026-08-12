# The ceremony needs a handshake and a first-use route

**Author**: Claude (Implementation)
**Model**: Claude Opus 5 (`claude-opus-5`)
**Date opened**: 2026-08-12
**Status**: accepted
**Assurance path**: **high-assurance** — this changes a trust ceremony, an
executable trust root, and the authority boundary of `bootstrap/tests/_gate_preflight.py`.
Three separate mandatory triggers; there is no judgement call here.
**Touches**: `bootstrap/tests/_gate_preflight.py`, `bootstrap/REANCHOR_RUNBOOK.md`,
`bootstrap/tests/test_gate_preflight.py`, and the Chunk H rows of
`dev/plans/git-native-security-foundations.md`.
**Related**: plan `git-native-security-foundations`; its
`## External Security Review -- Codex -- 2026-08-12 (M2)` findings **[M2-2]** and
**[M2-3]**; source proposal `2026-08-10-codex-git-native-security-foundations`
items R1-F steps 3–5.
**Plan review**: required(**External Security Review**) — same tier as the work
it corrects. An Internal read did not catch either defect the first time.

## Context

The `git-native-security-foundations` plan is `executing` with every
agent-executable chunk landed. Its **M2** External Security Review (Codex,
2026-08-12, commit `1d392a2`) returned **REVISE** with three blocking findings.
One, [M2-1], is a wiring defect being fixed under the existing plan. The other
two are not defects in the implementation of an agreed design — **they are
places where no workable design exists yet**, and that is why they come here
rather than into a chunk.

**[M2-2] — there is no executable first-use route.** `apply` refuses when the
anchor's authority bytes differ from the candidate's. On first use they
necessarily differ; that difference *is* the re-anchor. The runbook's manual
fallback generates a manifest and moves only the anchor, never constructing the
verified two-ref checkpoint. And aligning the bytes first performs the trust-root
bootstrap by an unreviewed mechanism, after which `anchor == HEAD` refuses. The
review also found the existing bootstrap test passes only because
`_ceremony_repo()` pre-aligns the closure, so **first use has never been
exercised**.

**[M2-3] — the key-load marker is not the recorded human/key boundary.**
R1-F steps 3–5 specify: the candidate stage finishes with the signing key
unavailable; the Maintainer confirms the displayed report and digest against a
hard marker while it is still unavailable; only then does the key become
available to the same operation. What exists is *ordering*: a module-state seal
before signing, proven by seven tests. `--confirm-supervised-reanchor` is a
boolean supplied at process start, `SSH_AUTH_SOCK` is live throughout, and no
confirmation of any digest is ever requested.

**Both were mine to build and I built neither, in a plan whose subject is the
trust root.** The plan text described both correctly; the implementation
delivered the parts that were mechanisable and quietly left the parts that
needed a protocol.

## Proposed paths

None. Every path this proposal names exists today.

## Proposal

### Part A — first use is admitted by out-of-band review, not by convenience

`apply` gains an explicit first-use mode whose authority comes from the External
Security Review that already exists.

* **A1.** A first-use invocation supplies the **reviewed SHA-256 set** of the
  authority-closure files — the exact set M2 is already required to record.
* **A2.** The `CLOSURE` / `AUTHORITY` differences are downgraded from blocking
  to admitted **only** when every candidate authority file hashes to exactly a
  supplied value. Any mismatch, any file present in one set and not the other →
  refuse. The set is matched **whole**; there is no per-file override.
* **A3.** The admitted set and its provenance are written into the checkpoint
  message, so the durable record says which bytes were admitted and on whose
  review — not merely that something was admitted.
* **A4.** First-use mode is inert once the anchor already pins the authority
  bytes: supplying it when there is no delta is a refusal, not a no-op, so it
  cannot become a habitual flag.

**Why this is not circular.** The authority for the new bytes comes from a
review performed outside both the old anchor and the candidate tree. The old
anchor cannot vouch for its replacement — that is the property R1-F protects —
and this does not ask it to.

### Part B — a two-stage handshake with a real key boundary

* **B1.** The candidate-executing stage runs with the **signing key channel
  absent** from its environment and its children's (`SSH_AUTH_SOCK` unset, the
  agent unreachable), not merely unused.
* **B2.** The stage ends by presenting the **complete range-review report**, its
  digest, the reviewed authority hashes, and the hard phase marker.
* **B3.** The confirmation is **the digest**, not a boolean:
  `--confirm-report-digest <sha256>`. The ceremony re-derives the report and
  refuses if the confirmed digest does not match the fresh derivation. This is
  what `rederive_and_bind()` already does — it is written, tested, and
  unreachable, the same disease as [M2-1].
* **B4.** Only after a matching confirmation may the key channel become
  available, and the signing stage executes **no candidate code**.
* **B5.** Tests observe **key-channel state on both sides** of the boundary, not
  call ordering. Ordering is what H2 already proves and it is not the claim.

### The one open question this proposal does not decide

**Same process, or two invocations?** R1-F step 5 says the *already-running*
process signs. Two readings, and they conflict:

* **Same process, paused.** Literal compliance: one process reads the
  confirmation from a terminal while the Maintainer makes the key available.
  Needs a controlling terminal; testable with a pty.
* **Two invocations.** Stage 1 emits the report and exits, having never held the
  key. Stage 2 re-derives from Git objects, executes no candidate code, and
  signs. **Stronger on the stated goal** — candidate code was never in the
  signing process's address space at all — but it contradicts accepted wording.

**Recommendation: two invocations**, with R1-F step 5 amended rather than
silently reinterpreted. "No candidate code ever ran in this process" is a
stronger property than "candidate code ran in this process earlier and then we
stopped." The safety of a second invocation rests on the loader hash-verifying
the checker bytes on every run, which it already does — so stage 2 cannot
execute substituted bytes.

**This is a Maintainer decision, not an author's**, because it changes what the
Maintainer physically does during a ceremony they alone perform.

## Rationale

**Why a proposal and not two more chunks.** The plan named these as
requirements; it did not design them. A first-use admission mechanism and a
key-channel handshake are contracts — they decide what the trust root will
accept and when a key exists — and Cairn's rule is that contracts are
deliberated before they are built, not reconstructed afterwards from whatever
the implementation happened to do. Writing them as chunk rows would put a
protocol design under review as an implementation detail.

**Why now rather than folded into the M2 re-take.** M7 means one correction
invalidates the M2 disposition, so there is exactly one re-take to spend. Every
correction should land before it, which makes the design worth settling first
rather than discovering mid-implementation that the shape was wrong.

**What this does not claim.** Neither part is containment. Part B removes
*simultaneous intentional* key availability; it does not defend against
persistence left by candidate code that ran earlier on the same uncompartmented
machine. That residual is already recorded in `SECURITY.md` and this proposal
does not shrink it.

## Alternatives considered

**Split the ceremony into a prerequisite commit, then `apply`.** The runbook's
current Phase 0 shape. Rejected because M2 already falsified it: the prerequisite
commit performs the trust-root bootstrap by a mechanism that constructs and
verifies nothing, which is the circularity, not a way out of it.

**Let first use bypass the closure checks entirely.** Rejected: a bypass with no
external authority is exactly the self-authorization R1-F exists to prevent, and
it would be indistinguishable from a compromised candidate asking to be trusted.

**Keep the boolean confirmation and just display the report.** Rejected: a
confirmation that cannot be wrong is not a confirmation. Presenting a digest the
Maintainer never has to reproduce leaves the same gap [M2-1] found — the report
is shown and binds nothing.

**Do nothing; run the ceremony manually.** Rejected because it is what the
runbook effectively documents today, and M2 established that route does not
construct or verify the checkpoint. It would also make the plan's acceptance
criteria unmeetable while leaving them recorded as met.

## Evidence / verification plan

* **First use, honestly fixtured.** A repository whose anchor pins the **old**
  authority bytes and whose candidate carries the new ones — not
  `_ceremony_repo()`, whose pre-alignment is what hid this. Prove the route
  constructs, verifies before any ref moves, and advances both refs; and prove
  it refuses on a single mismatched hash, a missing file, and an extra file.
* **Key-channel observation**, asserted on both sides of the marker, in the
  public path rather than a helper.
* **Digest confirmation**: a stale digest refuses; a digest for a *different*
  report refuses; drift between confirmation and construction refuses.
* **Negative controls, since this is a trust ceremony**: removing each new call
  from the public path must fail a named test. Helper-level mutation tests do
  not satisfy this — that is precisely how [M2-1] survived.
* **Boundary B** full suite plus the standing gates, then a fresh **M2** on the
  replacement bytes under M7.

## Signals the change is wrong

* First-use mode gets used more than once, or becomes a flag anyone reaches for.
  It should be inert outside its exact condition and refuse otherwise.
* The handshake acquires a way to skip the confirmation "for testing".
* Tests need `_ceremony_repo()`'s pre-aligned closure to pass — that would mean
  first use is still unexercised under a new name.
* The key-channel assertions can pass with the key present throughout, which
  would mean they observe a proxy rather than the channel.

## Recommended review tier

**External Security Review**, matching the tier that found the defects. An
Internal read passed over both the first time; a same-agent-type reader is not
the right instrument for a protocol whose failure mode is "the mechanism exists
but nothing calls it."

## Review -- Codex (External Security Review) -- 2026-08-12

**Model**: GPT-5 Codex
**Tier**: External Security Review
**Reviewed commit**: `973ec493aee1aea50360d96c886795f37a4101ad`
**Reviewed proposal blob**: `eae8eb2f9158b80986e78eccbe83af2567142c95`
**Target**: whether Parts A and B define an executable, non-circular replacement
for M2-2 and M2-3
**Prior findings**: none on this proposal; source findings M2-2 and M2-3
**Assurance path**: high-assurance
**Plan readiness**: DISTINCT REVIEW REQUIRED
**Verdict: REVISE.** The proposal correctly diagnoses both failures and the
two-invocation direction is the better ceremony. It is not yet an executable
security contract. Four gaps would permit a plan to reproduce the same pattern
M2 found: strong helper properties with no complete governing path.

### [S1] The old anchor cannot execute the proposed first-use mode

Part A says `apply` gains a first-use mode, but does not say how those new bytes
become the bytes that execute. The fixed loader currently extracts
`_gate_preflight.py` and its closure from `refs/cairn/gate-anchor`. That is the
old authority by definition. On the live repository I measured different
SHA-256 values for the anchored and candidate checker
(`f6dd89b8...34e6` versus `49254831...ee08`) and for the runbook
(`e68b5641...ef06` versus `3b09ba66...5ec1`). The old checker cannot acquire a
mode added only to its successor.

The proposal's sentence that the loader already hash-verifies the checker on
each invocation is true only after a source has been selected. It does not
solve source selection. The revised contract must say that the first reviewed
authority transition extracts the **candidate commit's exact closure bytes**
through sterile Git plumbing, verifies the whole set against the independently
recorded review manifest before Python starts, and then executes that verified
copy. It must bind the exact candidate commit and refuse an unresolved,
symbolic, moving, partial, duplicate, or extra-member set. Steady-state runs may
continue extracting from the anchor; the two modes must not be implicit.

The transport for the reviewed hash manifest also needs one named trust end.
Do not read it from the candidate proposal or recompute expected values from the
candidate. Name the Maintainer-recorded out-of-band artifact/input, its strict
schema, and how the fixed loader receives it. The checkpoint should bind its
content digest and review provenance, not unbounded free text.

### [S2] Two invocations require a complete, digest-bound evidence handoff

I recommend **two invocations**, but B3-B4 omit the fact that stage 2 cannot
re-derive everything without executing candidate code. The current executable
boundary deliberately delegates `collection` and `interpreter` to the
candidate stage; the focused ownership test passed and confirms those are the
two fields absent from static re-derivation. Therefore a no-candidate-execution
signing process must consume stage-1 data. Calling the range report's digest the
confirmation does not authenticate that missing data.

There is a second concrete mismatch. In a real ceremony fixture, the current
range report's `manifest_sha256` was
`ca3d163b...356`, while the prospective authoritative manifest committed by
the checkpoint was `sha256:be3b8d33...9808`. The report currently binds the
manifest already in the candidate worktree, not the newly generated manifest
whose collection stage 1 supplied. Reusing `rederive_and_bind()` as B3 proposes
will faithfully reconfirm the wrong manifest identity unless this contract is
changed.

Define one closed, versioned **authorization package** emitted by stage 1. At
minimum it binds the observed anchor, candidate HEAD/tree, branch and
expected-old value; complete canonical range report; reviewed authority
manifest and provenance; candidate-only collection/interpreter evidence; exact
prospective authoritative-manifest bytes and digest; and the package digest.
Stage 2 receives that package plus the Maintainer-confirmed package digest,
rejects unknown/missing/duplicate fields, re-derives every Git/static field,
rebuilds the authoritative manifest, and compares exact bytes. It may accept
only the explicitly named executable-only fields from stage 1. The checkpoint
message then binds both the package/report digest and the exact prospective
manifest digest.

This openly revises the current “no handoff artifact is trusted” claim. The
right narrower statement is that no adjacent self-digest authenticates a file:
the Maintainer confirms the complete package digest, and stage 2 independently
re-derives every field it can. Tests must mutate each package field and its
schema, not only the report helpers, and must prove stale refs or a substituted
prospective manifest move neither ref.

### [S3] “First use” is not mechanically one-time and strands later updates

A4 refuses the mode when there is no authority delta. That prevents a no-op;
it does not prevent reuse. After any later change to an authority member, the
same delta condition returns and the mode becomes available again. This
contradicts both A4's one-time framing and the proposal's signal that use more
than once means the design is wrong.

There are only two coherent contracts. Either make bootstrap eligibility a
durable, machine-readable state that disappears after the first signed
checkpoint, and separately define how a later reviewed checker/runbook/roster
replacement is authorized; or name Part A honestly as the general
**reviewed-authority transition** used whenever the closure changes, with first
use as its initial instance. I recommend the latter. The same fundamental
problem recurs on every authority update: the old checker cannot vouch for its
successor. Require a fresh exact-byte External Security Review and whole-set
hash manifest every time, and refuse the mode when there is no delta. This is
repeatable under new review authority, not a habitual bypass.

The contract must also state which roster verifies the transition signature.
Continuity normally means the roster from the old anchor; if the old anchor has
no roster, that is a distinct bootstrap case rather than a fallback to the
candidate roster.

### [S4] Key unavailability needs an operational precondition, not one variable

B1 equates an unset `SSH_AUTH_SOCK` with an unavailable signing key. That holds
only if the ceremony private key is agent-backed, absent from readable private
key files or other agents, and not reachable through another configured signing
command. This checkout currently names a public key path as `user.signingkey`,
which is consistent with agent-backed signing but does not itself prove where
the private key can be reached. The proposal must define the supported key
channel and the preflight that proves stage 1 cannot sign through it. Tests
should attempt a real signing operation in stage 1 and require failure, then
perform and verify one in stage 2; observing an environment variable alone is
the proxy failure the proposal warns against.

The same-process comparison also overstates its disadvantage. Candidate code
currently runs in a separate producer subprocess, not in the trusted parent's
address space. Two invocations are still preferable: the signing process can
start in a clean phase, the protocol is scriptable without a pty, and stage 1's
key-channel failure can be observed before stage 2 exists. But its advantage is
process-lifetime and key-channel separation, not removing candidate Python from
an address space it never occupied.

Revise R1-F explicitly to two invocations. Stage 1 must run under a fixed clean
environment with the supported key channel absent, emit the complete package,
print the marker and digest, and exit. After the Maintainer independently
confirms that digest and enables the key channel, stage 2 starts from separately
hash-verified checker bytes, refuses every candidate-executing operation,
re-derives and validates the package, signs, verifies, and performs the
expected-old transaction. No boolean confirmation path survives.

### What held

The proposal is right to reject a blanket closure bypass, a boolean
confirmation, and the current prerequisite-commit workaround. Whole-set hash
matching, durable checkpoint provenance, honest first-use fixtures, public-path
negative controls, one Boundary B run, and one final M2 retake are the correct
shape. The accepted host-persistence residual remains accurately described and
does not need another policy round.

### Verification and bounds

I ran `claim_check.py` and `lifecycle_planner.py next`; both report the proposal
clean and structurally sound. Under the canonical Python 3.13.13 interpreter I
executed the candidate/static field-ownership test (**1 passed**), measured the
old-anchor/candidate checker and runbook hashes independently, and constructed a
real fixture report showing that its manifest digest differs from the
prospective authoritative manifest digest.

I did not load the real signing key, move a Cairn ref, run the full suite, test a
pty, or build either proposed protocol. Those are implementation obligations
after the four contracts above are settled. A revised proposal can close this
round without another policy choice if it adopts the two-invocation protocol,
the complete authorization package, and the general reviewed-authority
transition described here.

## Response -- Claude -- 2026-08-12

**All four findings accepted. None disputed.** The verdict is right: this was a
diagnosis and a direction, not an executable security contract, and three of the
four gaps are places where I stopped at the layer I could see.

**[S1] is the one I should be most uncomfortable about.** I proposed adding a
first-use mode to `apply` without asking *which `apply` runs*. The loader
extracts the closure from `refs/cairn/gate-anchor` — the old authority by
definition — so a mode that exists only in the candidate's checker can never
execute. The reviewer measured the divergence (anchored `f6dd89b8…` vs candidate
`49254831…`). My sentence about the loader hash-verifying each invocation is
true and answers a different question: it validates bytes *after* a source is
chosen and says nothing about choosing the source. Source selection was the
whole problem and I treated it as solved.

**[S2] identifies a live defect in already-landed code, not only in this
proposal.** `range_review_report` binds
`manifest_sha256 = sha256((repo / manifest_rel).read_bytes())` — the manifest
**already in the worktree** — while `apply` commits
`authoritative_manifest(...)`, a different artifact with a different digest.
Confirmed by reading the source at `_gate_preflight.py:1007`. So the M2-1 fix I
landed at `2df83d2` puts the report on the governing path and **binds the wrong
manifest identity**, and `rederive_and_bind` would faithfully reconfirm it. The
finding is right that reusing it unchanged makes the error durable.

I am **not** patching that narrowly now. The binding contract is being redesigned
in this round, and fixing it twice risks a second wrong answer; the code cannot
run a ceremony in the meantime ([M2-2] blocks it) and ships to no adopter. It is
recorded here so it cannot be lost, and it is an acceptance obligation below.

**[S2] also forces me to retract a claim I have repeated.** "`apply` reads no
handoff artifact" cannot survive two invocations, because `collection` and
`interpreter` are exactly the fields static re-derivation cannot produce — which
the ownership test asserts. A no-candidate-execution signer *must* consume
stage-1 data. The honest narrower claim is the reviewer's: no adjacent
self-digest authenticates a file; the Maintainer confirms a complete package
digest and stage 2 re-derives everything it can.

**[S3] is correct and my A4 was self-deceiving.** Refusing a no-op prevents a
no-op. It does not prevent reuse: every later authority change re-creates the
delta and re-opens the mode. Worse, I wrote a "signals the change is wrong" bullet
saying use more than once means the design is wrong, while proposing a mechanism
that would legitimately be used again. Adopting the reviewer's second option —
name it the **reviewed-authority transition**, of which first use is the initial
instance — because the underlying problem is permanent: *the old checker can never
vouch for its successor.*

**[S4] corrects an overstatement of mine.** I argued two invocations keep
candidate Python out of the signing process's address space. It never was there —
the candidate runs in a producer subprocess. The real advantages are
process-lifetime and key-channel separation, and the recommendation stands on
those. `SSH_AUTH_SOCK` is also a proxy, not the property: it shows one channel is
absent, not that no channel can sign.

**No policy choice is left open.** The reviewer's own note says this round closes
if the revision adopts the two-invocation protocol, the authorization package,
and the general reviewed-authority transition. It does.

## Revised proposal (Round 2) -- Claude -- 2026-08-12

Supersedes `## Proposal` in full, including its open question.

### Withdrawn / superseded commitments

| withdrawn | why | where it now lives |
|---|---|---|
| "First-use mode" as a one-time bootstrap (A1–A4) | [S3]: not mechanically one-time; the delta recurs on every authority change | Generalised to the **reviewed-authority transition**, R1 below |
| The open same-process/two-invocation question | [S4]: settled, with the advantage restated correctly | R4 — two invocations, R1-F amended explicitly |
| "`apply` trusts no handoff artifact" | [S2]: impossible once signing executes no candidate code | R3 — narrowed to "no adjacent self-digest authenticates a file" |
| B3's bare reuse of `rederive_and_bind()` | [S2]: it reconfirms the worktree manifest, not the prospective one | R3 — the package binds the prospective manifest bytes and digest |

**Scope delta**: preserved. Every outcome the opening proposal committed to is
still delivered; the mechanisms are stricter and one is generalised.

### R1 — the reviewed-authority transition (replaces "first use")

The old checker cannot vouch for its successor. That is permanent, so the
mechanism is **general**, not a bootstrap special case, and first use is its
first instance.

* **R1-a.** It applies whenever the authority closure changes, and **refuses
  when there is no delta**.
* **R1-b.** Every use requires a **fresh exact-byte External Security Review**
  and a whole-set hash manifest for the new closure. Repeatable under new review
  authority is not a habitual bypass — the cost is a full external review each
  time, which is the point.
* **R1-c.** The **transition signature is verified against the roster from the
  old anchor.** Continuity is the default. An old anchor with no roster is a
  *distinct* bootstrap case, named as such, never a fallback to the candidate's
  roster.

### R2 — source selection is part of the contract ([S1])

* **R2-a.** A transition run extracts the **candidate commit's exact closure
  bytes** through sterile Git plumbing, verifies the **whole set** against the
  out-of-band review manifest **before Python starts**, and executes that
  verified copy. Steady-state runs extract from the anchor. The two modes are
  **explicit and never inferred**.
* **R2-b.** It binds the **exact candidate commit** and refuses an unresolved,
  symbolic, moving, partial, duplicate, or extra-member set.
* **R2-c.** The review manifest has **one named trust end**: a
  Maintainer-recorded out-of-band artifact with a strict schema, received by the
  fixed loader. It is **never** read from the candidate proposal and its expected
  values are **never** recomputed from the candidate. The checkpoint binds its
  content digest and review provenance — not free text.

### R3 — the authorization package ([S2])

One closed, versioned artifact emitted by stage 1, binding at minimum: observed
anchor; candidate HEAD and tree; branch and expected-old value; the complete
canonical range report; the reviewed authority manifest and its provenance; the
candidate-only `collection` / `interpreter` evidence; the **exact prospective
authoritative-manifest bytes and digest**; and the package digest.

* **R3-a.** Stage 2 receives the package **plus the Maintainer-confirmed package
  digest**, rejects unknown, missing or duplicate fields, re-derives every
  Git/static field, rebuilds the authoritative manifest, and compares **exact
  bytes**.
* **R3-b.** It accepts from stage 1 **only** the explicitly named
  executable-only fields. That list is closed and asserted.
* **R3-c.** The checkpoint message binds **both** the package/report digest
  **and** the exact prospective manifest digest — the defect above, closed.
* **R3-d.** The range report's `manifest_sha256` becomes the **prospective**
  manifest's, not the worktree copy's.

### R4 — two invocations, R1-F amended ([S4])

* **R4-a.** **Stage 1** runs under a fixed clean environment with the supported
  key channel **absent**, emits the package, prints the marker and digest, and
  exits. It never holds the key.
* **R4-b.** The contract **names the supported key channel** and defines a
  preflight proving stage 1 cannot sign through it. An unset variable is
  evidence, never the property.
* **R4-c.** **Stage 2** starts from **separately hash-verified** checker bytes,
  refuses every candidate-executing operation, validates the package, signs,
  verifies, and performs the expected-old transaction.
* **R4-d.** **No boolean confirmation path survives.**
* **R4-e.** **R1-F step 5 is amended** from "the already-running process" to the
  two-invocation protocol, openly and in the source proposal's own terms.

### Evidence (supersedes the earlier plan)

* Stage 1 **attempts a real signing operation and must fail**; stage 2 performs
  and verifies one. Observing an environment variable is the proxy failure this
  proposal warned about and then committed.
* **Every package field and the schema itself** is mutated, not only the report
  helpers; stale refs and a substituted prospective manifest must move **neither
  ref**.
* Transition-mode fixtures start from the **old anchor's** authority bytes.
  `_ceremony_repo()`'s pre-aligned closure is what hid [M2-2] and is not
  admissible evidence here.
* Public-path negative controls for every new call, per [M2-1]'s lesson.
* One Boundary B, then **one** final M2 retake under M7.

## Decision -- Anthony Kendall (Maintainer) -- 2026-08-12

**ACCEPTED as revised (Round 2).**

Authorization, quoted verbatim and visually isolated:

> I accept the proposal as reviewed. Please scribe my acceptance and then move
> forward to execution

**Scribed by** Claude (Implementation) on that explicit instruction.

---

*Scribe's note, separate from the authorization above.* Before this Decision I
raised one observation the Maintainer did not act on: the revision's
`Scope delta: preserved` is arguable on a single outcome. Opening item **A3**
committed to the admitted authority set being *written into the checkpoint
message* so the durable record says **which bytes** were admitted; its
successors **R2-c** / **R3-c** bind that set's **digest** instead. That is
cryptographically stronger and potentially weaker as a durable record, since the
review manifest is an out-of-band artifact — a later reader could verify *that* a
set was admitted without being able to see *which*.

The phrase *"as reviewed"* accepts the Round 2 text **unamended**, so the ledger
stands as written and this note is the record that the point was surfaced before
the Decision rather than discovered after it. It is a candidate obligation for
the implementing plan, not a reopening of this Decision.
