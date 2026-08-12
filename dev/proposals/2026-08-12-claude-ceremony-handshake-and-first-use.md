# The ceremony needs a handshake and a first-use route

**Author**: Claude (Implementation)
**Model**: Claude Opus 5 (`claude-opus-5`)
**Date opened**: 2026-08-12
**Status**: proposed
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
