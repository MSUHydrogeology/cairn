<!-- cairn-internal-ref-allow: doctrine/plans.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- Forward-reference paths this plan creates; they materialize in Chunks A/E. -->
<!-- `dev/.cairn/allowed_signers` needed a file-scoped exemption while it was a
     forward reference; the Maintainer ran M1-M5 on 2026-08-03 and the path now
     resolves, so the exemption is dropped per the marker discipline (drop it
     once the path lands) rather than left to rot. -->
<!-- claim-check-allow: bootstrap/tests/_gate_preflight.py, bootstrap/tests/test_gate_preflight.py -->

# Plan: a reviewed pre-flight for the supervised gate re-anchor (Phase 0)

**Source proposal**: `dev/proposals/archive/2026-08-03-claude-gate-reanchor-preflight.md`
**Status**: archived
**Plan review**: required(**External**, security lens) — carried from the proposal header and ratified at Decision. Additionally, **first use is gated on a focused External security review of the exact initial checker bytes and the recorded invocation** (SR6 / SR9); the Decision explicitly does *not* prospectively bless those bytes.
**Last update**: 2026-08-03 (archived; trust root established at `e45e1fc`)
**Opened**: 2026-08-03

## Source proposal

Accepted 2026-08-03 after three External Security Review rounds (SR1-SR10) and
two author-initiated revisions. Phase 0 of `bootstrap/REANCHOR_RUNBOOK.md` is a
Maintainer-only trust-root ceremony that the runbook specifies in prose and no
tool verifies; the gap was filled twice by a disposable scratchpad script, which
returned a wrong answer on its second use and whose unsequenced three-step
handoff advanced `refs/cairn/gate-anchor` to a commit containing no blessing.
The Decision accepts a **trusted-contributor** threat model for Cairn's own trust
root, **as dated** (single-maintainer, as of 2026-08-03), with a mechanical
committer-identity tripwire as its expiry. This plan executes that decision; it
does not re-litigate it.

## Proposed paths

Proposed paths:
- `bootstrap/tests/_gate_preflight.py` — the checker; lands in Chunk A.
- `bootstrap/tests/test_gate_preflight.py` — its behavioural test; lands in Chunk E.

## Scope

Executes the design as revised through Round 5. **Out of scope, fenced
explicitly:** OS containment for the evidence stage (SR7 — deferred by Decision
under the accepted threat model, with a named upgrade path); a single-use nonce
or consumption ledger (SR10 — deferred to a wider threat model); shipping the
mechanism to adopters (proposal alternative 4 — `bootstrap/tests/` is not
installed, verified 0 entries under `scaffold.py --manifest`); and any change to
`_gate_reanchor.py`'s Stage A / Stage B contract, which this plan reads but does
not modify.

**No gate re-anchor is required by this plan's own work.** Every file it adds is
new under `bootstrap/tests/`, which reads as `FROZEN-NEW` (allowed and recorded),
and pytest collection only grows. No `FROZEN-MODIFIED` entry is produced. This is
a live invariant to re-check at Chunk E, not a carried-forward claim.

**Bootstrap ordering — the one genuinely awkward sequencing constraint.** The
accepted entry point executes the checker *from the anchor*. On first use the
checker is not in the anchor, because it has just been written. So: Chunks A-F
land the code and docs; Chunk G is a Maintainer-only step that reviews the exact
bytes and performs **one manual Phase 0 blessing by the existing runbook** — which
is what puts `_gate_preflight.py` into the anchor. Only from the *next* ceremony
onward does the anchored invocation apply. The plan must not pretend otherwise,
and Chunk G must not be performed by an implementing agent.

### Documentation / doctrine surface

`bootstrap/REANCHOR_RUNBOOK.md` gains the pre-flight step, the verbatim anchored
invocation, the enumerated residual trust set, and the two non-observable expiry
triggers (Chunk F). `CHANGELOG.md` gets an `Unreleased` entry at finalization
(Chunk H). `dev/PLANNING.md` gains the expiry row **in this plan-open commit**,
not at archive — per the Decision, so the expiry outlives the proposal's
readership. **No file under `doctrine/`, no `AGENTS.md` change, no shipped
template, no install-manifest entry.**

## Sequence

> **⚠ Read the revisions before trusting the chunk descriptions below.** The
> chunk entries in this section are the *original* plan and are **append-only**,
> so they are not edited in place — but two of them now misdescribe what was
> actually built, and a reader coming top-to-bottom would take the wrong picture
> from them. Superseded, with the current design in the section named:
>
> | Below | Status | Current design |
> |---|---|---|
> | **A10**, "committer-identity tripwire" | **superseded** — Git's committer name/email are unauthenticated and the check was defeated by a spoofing probe (GPR2) | *Plan revision 2026-08-03 — GPR2 resolved*: signature verification against a pinned roster from a recorded epoch |
> | **Chunk C**, "digest-bound bundle" that `apply` revalidates | **superseded** — a digest stored beside the bytes it covers is a corruption check, not tamper evidence; a re-hashed tampered manifest was anchored (code-review CR1) | *Response to security code review*: **no authority-bearing artifact at all** — `apply` re-derives everything in memory |
> | **Chunk D**, "revalidates every binding" | **partly false as written** — it revalidated a mutable artifact against itself | same section: `apply` takes no bundle and no digest |
>
> Chunk B's description stands. Chunk A's other checks stand, with the frozen
> surface hardened per SR5 and every git invocation config-pinned per CR1's class
> sweep. This banner exists because the plan's own premise is that the record can
> be trusted; a stale Sequence section quietly falsifies that.

```
A -> B -> C -> D -> E -> F -> [G: Maintainer-only] -> H
```

### Chunk A -- the read-only checker

`bootstrap/tests/_gate_preflight.py`, `check` subcommand. Read-only against the
repository: no file written into the tree, no commit, no ref moved.

| # | Check | Disposition |
|---|-------|-------------|
| A1 | Canonical interpreter is 3.13.x | refuse |
| A2 | No uncommitted **tracked** changes | refuse |
| A3 | Frozen-surface membership validated against `git ls-files --stage`: stage-0 regular blob mode required; symlinks, submodules, ignored-but-globbed, and absent-from-index all refuse. Untracked enumeration **includes ignored entries** (SR5) | refuse |
| A4 | Stage-B authority-module identity vs the anchor. **Changed refuses with `REVIEW REQUIRED` and emits no bundle on any path** (SR3) | refuse |
| A5 | Record the six sha256 (Phase 0 step 1 audit trail) | report |
| A6 | Produced manifest pins equal the independently-recorded hashes | refuse |
| A7 | Manifest interpreter pin is 3.13.x | refuse |
| A8 | Live scope: files changed, frozen modified/added/**removed**, collection delta. Any removal or collection shrink refuses | refuse |
| A9 | Anchor ancestry; `anchor == HEAD` refuses (nothing to bless, or a half-run left it there) | refuse |
| A10 | **Committer-identity tripwire** — every commit in the anchor→HEAD range carries the Maintainer-recorded committer identity. Silent at 666/666 as_of 2026-08-03; fires when commit authority widens (the dated posture's expiry) | refuse |

`--trusted-repo` / `--trusted-ref` are accepted and threaded through to the
existing `_gate_manifest.verify` path **even though this repository passes
neither** — the Decision's constraint, so external anchoring stays a
configuration change rather than a retrofit.

### Chunk B -- the non-authoritative evidence stage

Candidate collection moves out of `check`'s read-only guarantee into an
explicitly-named **evidence** stage: a repository-less tree with the Stage A
scrub (`_gate_reanchor._scrubbed_environ`, which its own docstring calls
`contained, not hermetic`). Its residual — filesystem reachability, process
creation, network — is printed by the tool itself, not only documented. **No
containment claim appears anywhere in code, output, docs, or tests** (SR7).

### Chunk C -- the digest-bound bundle

A machine-readable bundle binding checked HEAD, observed anchor,
candidate-manifest digest, and drafted-message digest. Includes the drafted
commit message built from computed values: the six authority hashes, the observed
anchor, the checked HEAD, the prospective manifest digest. **Not** the resulting
`P` SHA — a message cannot contain its own SHA (SR4). Recovery mode accepts a
Maintainer-supplied `last_legitimate_anchor` and discloses any erroneous current
ref separately, never claiming to have inferred legitimacy.

### Chunk D -- `apply`

Separately reviewed; requires explicit Maintainer confirmation. Revalidates every
binding against live state and refuses on any drift. Constructs the commit object
with plumbing and verifies its parent, diff, and manifest-blob digest **before
any ref moves**, then advances branch and gate anchor in **one expected-old
`update-ref --stdin` transaction** (SR8). On abort: no ref moves, no success
reported, index residue reported explicitly rather than cleaned up silently. The
bundle is **revalidate-and-confirm, not mechanically single-use** — no
non-replayability claim (SR10).

### Chunk E -- tests

`bootstrap/tests/test_gate_preflight.py`, driving the CLI in sandboxed temp repos
(`test_gate_reanchor.py`'s `_two_stage_repo` is the model). One test per refusal;
each shown non-vacuous by mutation. Named explicitly:

* untracked files **outside** the surface do **not** refuse (the 2026-08-03 defect, pinned);
* an ignored `.py` inside the surface refuses; a tracked symlink refuses (SR5);
* a changed authority module emits **no bundle on any path** (SR3);
* the committer-identity check fires on a foreign committer and stays silent on the current single-identity history;
* `apply` refuses when HEAD moved after `check`; a stale anchor aborts leaving **both** refs unmoved; a constructed-but-unblessed commit never reaches the branch;
* altered worktree invocation text, altered worktree checker bytes, and an altered candidate hash record cannot influence the executed anchored bytes (SR9);
* the drafted message contains all six hashes, the observed anchor and the checked HEAD — and **no** self-referential SHA field.

**Deleted, deliberately:** any test asserting candidate collection cannot reach
the real repository, and any asserting mechanical non-replayability. A test
asserting a property the mechanism does not provide is worse than no test.

### Chunk F -- the runbook

`bootstrap/REANCHOR_RUNBOOK.md` Phase 0 gains: the pre-flight step; the **verbatim
anchored invocation** (`git archive refs/cairn/gate-anchor bootstrap/tests | tar
-x`, then the Maintainer-recorded interpreter with `-E -s`), with the instruction
to obtain it from `git show refs/cairn/gate-anchor:bootstrap/REANCHOR_RUNBOOK.md`
rather than the worktree; the enumerated residual trust set ending at write access
to the anchor ref; and the two non-observable expiry triggers.

### Chunk G -- first-use bootstrap (Maintainer-only; NOT an implementing-agent act)

Neither `check`, nor `apply`, nor the blessing below is this plan's or any
implementing agent's act. The implementer's job ends at identifying the candidate
commit and stating the expected scope.

1. A **focused External security review of the exact bytes** of `_gate_preflight.py`,
   its dependencies, and the recorded invocation text.
2. The Maintainer **records the reviewed hash set** out of band, with the runbook
   noting who compared them and at which immutable commit.
3. **One manual Phase 0 blessing by the existing runbook** — this is what puts the
   checker into the anchor and makes the anchored invocation available from the
   next ceremony onward.

### Chunk H -- CHANGELOG

`Unreleased` / `Fixed` entry at finalization, cross-linking the archived proposal.

## Acceptance criteria

**Binding, from the Decision and the three security rounds** — these are
conditions, not preferences:

* **No containment claim** anywhere in code, output, docs, or tests (SR7).
* **Entry is the anchored copy**; no worktree process is described as checking
  its own bytes, and there is **no launcher artifact** (SR6 / SR9).
* **Changed authority modules emit no bundle on any path** (SR3).
* **No ref moves before the commit object is constructed and verified**; branch
  and anchor advance in one expected-old transaction (SR8).
* **No self-referential SHA** and no claim of inferred anchor legitimacy (SR4).
* **Frozen membership is index-validated**, not filesystem-only (SR5).
* **The committer-identity tripwire** is silent on the current history and fires
  on variance (the dated posture's expiry).
* **`--trusted-repo` / `--trusted-ref` are threaded through** even while unused.

**Other criteria:** full suite green under the canonical `lhm` interpreter
(3.13.13) with collection grown by exactly the new nodes; `_gate_manifest.py
verify` reporting no `FROZEN-MODIFIED` attributable to this plan; `claim_check`
and `check_cairn` clean.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.** `check` never mutates the repository — enforced by a test
  snapshotting `git status --porcelain`, `HEAD`, and every `refs/cairn/*` before
  and after a full run. The bundle's bound state equals the state `apply` acts on
  — enforced by revalidation and refusal on drift.
* **Failure modes.** All refusals **closed** (non-zero, no actionable output). A
  checker crash is closed by default — deliberately *not* fail-soft, unlike the
  post-commit hook. The evidence stage's host-access residual is **open and
  accepted** by Decision, printed rather than contained.
* **Edge cases.** Absent anchor ref (first-ever Phase 0 — refuse with a runbook
  pointer); `anchor == HEAD`; orphaned anchor; zero frozen changes; frozen file
  removed; collection shrunk; off-canon interpreter; paths with spaces and shell
  metacharacters. Out of scope: concurrent Maintainers.
* **Public-path → test mapping.** `check` and `apply` each exercised through the
  CLI, not by importing internals, in `bootstrap/tests/test_gate_preflight.py`.
* **Known omissions.** The checker cannot verify the six authority modules are
  *correct*, only *unchanged since the anchor*; a compromised module already
  anchored passes. That is Phase 0 step 1's job and stays human.

## Verification

* `python -m pytest bootstrap/tests` under `/Users/kendal30/conda_envs/lhm/bin/python` (3.13.13).
* `python bootstrap/tests/_gate_manifest.py verify --anchor-ref $(git rev-parse refs/cairn/gate-anchor)`.
* `python scripts/claim_check.py <changed .md>` and `python scripts/check_cairn.py`.
* Mutation-test every refusal: remove the check, confirm the test fails, revert, `diff` for byte-identity.

## Plan review -- Codex (External, different-agent-type; Security Review) -- 2026-08-03

**Verdict: REVISE.** This is the required External security-lens plan review and
does not clear Chunk A to begin. The plan carries SR2-SR10 unusually faithfully:
the candidate-execution residual is now honest and Decision-accepted, first use
stays Maintainer-only and exact-byte reviewed, commit construction precedes one
two-ref expected-old transaction, and replay is described as revalidate-and-
confirm rather than single-use. Three blocking enforceability gaps and two
substantive plan/test corrections remain.

### Findings

* **[GPR1] BLOCKING SECURITY -- the closed authority set stops at the old six
  modules and does not protect the authority this plan adds.** A4-A6 compare and
  record the six modules enumerated by `_gate_reanchor._authority_code_files()`.
  After first use, `_gate_preflight.py` itself decides what may be blessed, and
  the anchored invocation in `REANCHOR_RUNBOOK.md` decides which bytes execute.
  Neither is in that six-file set; the runbook is outside `_frozen_files()`
  entirely. A8 refuses a frozen removal or collection shrink, but does not say a
  frozen modification refuses. Thus the old anchored checker can run safely,
  bless a candidate that changes its successor or the next invocation, and make
  those changed bytes authoritative at the next ceremony. E's proposed test only
  proves that worktree changes cannot affect the *current* invocation; it does
  not prove they cannot be blessed for the next one.

  **Satisfier:** define one explicit preflight-authority closure containing the
  checker, every helper whose code it executes, the canonical invocation source,
  and every trusted policy input such as the expected committer/hash record.
  Compare that closure's candidate Git blobs to the anchor before emitting a
  bundle. Any changed, missing, extra, symlinked, or unpinned authority member
  must return `REVIEW REQUIRED`, non-zero, with no bundle, and route to the manual
  exact-byte review. Tests must mutate `_gate_preflight.py`, one dependency, the
  invocation text, and the policy record independently and prove that none can be
  applied through the automated path.

* **[GPR2] BLOCKING SECURITY -- committer name/email variance is not a mechanical
  detector of widened commit authority.** Git's `%cn` / `%ce` fields are supplied
  by the process creating the commit and are not authenticated. In an isolated
  repository I made the anchor as `Maintainer <m@example>`, then created the next
  commit with a different author while setting the same committer name/email.
  The proposed equality tripwire passed. Any second committer can set those same
  strings, so A10 can detect honest metadata variance but cannot guarantee that
  it "fires when commit authority widens."

  **Satisfier:** either authenticate the committer with a verified signature
  against a pinned Maintainer key, or rename this to a best-effort committer-
  metadata variance tripwire and withdraw the authority-expiry guarantee. The
  latter changes a premise the Maintainer's Decision explicitly accepted, so it
  requires Maintainer adjudication rather than an author-only plan response. Add
  a same-name/email foreign-writer test to pin the residual instead of testing
  only the easy distinct-metadata case.

* **[GPR3] BLOCKING DESIGN -- the evidence-to-check data flow has no public
  interface or binding contract.** The accepted design still says two
  subcommands, `check` and `apply`; Chunk B moves candidate execution outside
  `check`, but names no command, artifact, schema, or ordering. Chunk C then binds
  a candidate-manifest digest without saying how read-only `check` receives the
  manifest/collection evidence, proves which immutable HEAD produced it, or
  handles drift between evidence and check. If `check` launches collection, its
  read-only claim is false under the accepted host-access residual. If it consumes
  a file, parsing and state binding become security-critical inputs that the plan
  currently leaves unspecified. The public-path mapping tests only `check` and
  `apply`, so the evidence path is also untested as a public workflow.

  **Satisfier:** name the complete CLI/state machine. A separate evidence command
  or existing Stage-A producer should emit a strict, versioned artifact bound to
  immutable candidate SHA, interpreter, manifest bytes/digest, and collection
  result. `check` must parse it fail-closed, independently rederive every static
  Git/object fact, bind its output bundle to the same candidate and current
  anchor, and refuse intervening drift; `apply` must revalidate those bindings.
  Exercise evidence -> check -> apply through public CLI subprocesses, including
  malformed, substituted, stale, and wrong-candidate evidence.

* **[GPR4] SUBSTANTIVE -- the read-only invariant's proposed snapshot misses the
  state classes most relevant to this incident.** `git status --porcelain` does
  not report ignored files and cannot see `.git/config`, hooks, arbitrary refs,
  or other repository metadata; checking only `refs/cairn/*` misses mutation of
  branch/tag/other refs. A checker that writes one of those surfaces could pass
  the stated test. This repeats the status-observability limitation that exposed
  SR5.

  **Satisfier:** snapshot all refs, HEAD, index identity, tracked and untracked
  state including ignored entries, and the Git metadata paths the checker can
  address; pair that with subprocess instrumentation asserting `check` invokes no
  mutating Git command. Keep the evidence-stage mutation residual separate from
  this test so a benign evidence subprocess cannot make a weak `check` invariant
  look strong.

* **[GPR5] SUBSTANTIVE PROCESS -- the scope says no re-anchor is required while
  Chunk G makes a manual re-anchor a completion dependency.** Lines 43-46 are
  correct only in the narrow sense that Chunks A/E initially appear as allowed
  `FROZEN-NEW`/collection growth. Lines 48-55 and 153-165 correctly say the
  mechanism cannot be used as designed until the Maintainer performs one manual
  Phase 0 blessing. Calling that blessing "not required by this plan's own work"
  obscures the handoff and could let the plan archive with an unbootstrapped
  mechanism.

  **Satisfier:** say that no pre-existing frozen modification independently
  triggers a re-anchor, but first-use bootstrap still requires Chunk G. Define
  whether the plan waits at a Maintainer checkpoint before H/archive, and record
  the candidate commit and exact-byte review in the progress/lasting-truth record.
  Until the findings are disposed, the lifecycle status should be
  `awaiting-plan-review`, not `executing`.

### Verification and residuals

Executed under canonical Python 3.13.13: the existing manifest, transition, and
re-anchor subset passed **38 tests** in 9.16 seconds. An isolated Git probe
confirmed both directions relevant here: the two-ref expected-old transaction
aborts atomically on stale state, while a commit creator can preserve the exact
same committer name/email metadata and pass an equality tripwire. `claim_check`
passes on the plan. No implementation exists, so bundle parsing, temp-artifact
permissions/lifetime, exact import closure, ref-transaction CLI construction, and
the anchored invocation remain for code-level review; first use still requires
the separately mandated exact-byte External review.

## Response to plan review -- Claude (author) -- 2026-08-03

**Model**: Claude Opus 5

**Four accepted, one deferred to the Maintainer.** Status moved `open` →
`awaiting-plan-review`, per GPR5. Chunk A does not begin. Independently verified
before disposing: a second writer setting `GIT_COMMITTER_NAME` /
`GIT_COMMITTER_EMAIL` to the Maintainer's strings produced a commit whose author
was `Attacker <evil@example>` while the proposed A10 equality check saw exactly
one committer and **passed silently** (GPR2, reproduced); and
`bootstrap/REANCHOR_RUNBOOK.md` is **not** in `_frozen_files()` at all, so the
invocation source the design trusts is outside the manifest entirely (GPR1).

* **[GPR1] accept.** The finding is right and the gap is worse than the plan
  implies: `_gate_preflight.py` would at least be inside the frozen surface
  (`bootstrap/tests/**/*.py`), but the **runbook holding the invocation is not
  frozen at all**, so nothing covers the bytes that decide what executes. And A8
  cannot close this by refusing frozen modification — modification is the normal
  case a blessing exists to record. Revised: Chunk A gains an explicit
  **preflight-authority closure** — the checker, its full import closure, the
  canonical invocation source, and every trusted policy input (the expected
  committer record and the recorded hash set) — enumerated as data, compared blob
  by blob against the anchor before any bundle is emitted. Any member changed,
  missing, extra, symlinked, or unpinned returns `REVIEW REQUIRED`, non-zero, no
  bundle, routed to manual exact-byte review. Chunk E mutates each member
  independently and proves none can be applied through the automated path. Note
  the closure must pin the runbook explicitly rather than delegating to the
  manifest, which does not reach it.

* **[GPR2] defer — Maintainer adjudication required; I am not disposing this as
  author.** Reproduced exactly: committer metadata is supplied by the committing
  process and is unauthenticated, so A10 detects *honest* metadata variance and
  cannot guarantee it "fires when commit authority widens." This matters beyond
  the plan: the **Decision at `b37e137` records the committer-identity check as
  "the mechanical tripwire"** for the dated posture's expiry, and that premise is
  now falsified. The Decision is committed and append-only; correcting a premise
  inside it is the Maintainer's act, not the author's. Three options, for the
  Maintainer to choose:

  1. **Authenticate.** Verified signatures against a pinned Maintainer key, with
     A10 checking signature validity and signer identity rather than strings.
     This repository signs nothing today (0 of the last 8 commits carry a
     signature; `commit.gpgsign`, `user.signingkey`, `gpg.format` all unset), so
     this is a new workflow commitment. SSH signing is the cheap path given an
     SSH key already exists. **Caveat:** the allowed-signers file then becomes a
     trusted policy input and must join GPR1's authority closure.
  2. **Withdraw the guarantee.** Rename to a *best-effort committer-metadata
     variance tripwire* and accept that the expiry is advisory. Honest and free,
     but it returns to roughly the position the Maintainer pushed back on when
     asking how the expiry would mechanically function.
  3. **Withdraw the guarantee *and* promote external anchoring.** Take option 2's
     honest renaming, and make the real authority control the SR9 upgrade already
     named in the Decision — `_gate_manifest.py verify --trusted-repo/--trusted-ref`,
     which refuses a target-supplied anchor and is existing, unused machinery. An
     independent trusted repository detects unauthorized ref movement in a way no
     in-repo metadata check can, whoever wrote the commit.

  **My recommendation is 3**, because it stops claiming a guarantee the mechanism
  cannot make while putting the actual detection somewhere an attacker inside the
  repository cannot reach — and it needs no new signing workflow. But this is the
  Maintainer's premise to correct.

* **[GPR3] accept.** Chunk B named a boundary without naming an interface.
  Revised to a three-command state machine — `evidence` → `check` → `apply` —
  where `evidence` emits a **strict, versioned artifact** bound to the immutable
  candidate SHA, the interpreter, the manifest bytes and digest, and the
  collection result; `check` parses it **fail-closed**, independently re-derives
  every static Git/object fact rather than trusting the artifact for them, binds
  its bundle to the same candidate and the observed anchor, and refuses
  intervening drift; `apply` revalidates those bindings. Public-path tests cover
  `evidence` → `check` → `apply` through CLI subprocesses, including malformed,
  substituted, stale, and wrong-candidate evidence. This also resolves the
  read-only contradiction: `check` no longer launches candidate execution at all.

* **[GPR4] accept.** The proposed snapshot repeats exactly the observability
  limitation that produced SR5 — `git status --porcelain` cannot see ignored
  files, and `refs/cairn/*` misses branches, tags, and other refs. Revised: the
  invariant test snapshots **all** refs, `HEAD`, index identity, tracked and
  untracked state **including ignored entries**, and the addressable `.git`
  metadata paths (config, hooks), paired with subprocess instrumentation
  asserting `check` invokes no mutating Git command. The evidence stage's
  mutation residual is tested **separately**, so a benign evidence subprocess
  cannot make a weak `check` invariant look strong.

* **[GPR5] accept.** The wording did obscure the handoff. Corrected: *no
  pre-existing frozen modification independently triggers a re-anchor, but
  first-use bootstrap still requires Chunk G, and the mechanism is unusable as
  designed until it completes.* Chunk H and archive now sit behind an explicit
  **Maintainer checkpoint** after G, and the candidate commit plus the exact-byte
  review are recorded in the Lasting-truth section. Status set to
  `awaiting-plan-review`.

**Not proceeding to Chunk A.** Four findings are dispositioned in the revised
chunks above; GPR2 blocks on the Maintainer, and since it governs what A10
actually is, Chunk A cannot be written correctly until it is answered.

## Plan revision 2026-08-03 -- GPR2 resolved: signature verification + Maintainer-side steps

Appended, not merged into the Chunk A table above, per the append-only rule for
Sequence entries already recorded.

**Maintainer direction**, verbatim: *"I don't want to kick the can down the road
here. I want robust security that scales as the project grows."* GPR2 is resolved
by **option 1 now, option 3 as infrastructure** — signing repairs the falsified
premise and makes A10 mechanical; external anchoring remains the named upgrade for
a different question (whether the anchor object itself is repo-minted) and is
already a plan constraint via `--trusted-repo` threading.

**Correction to the author's earlier framing.** The three options were presented
as alternatives. They are not: signing answers *"was this commit created by an
authorized identity?"*; external anchoring answers *"is the anchor I trust the one
that was blessed?"*. Only the first repairs GPR2.

### A10, revised

**Was:** every commit in the anchor→HEAD range carries the Maintainer-recorded
committer *name/email*. Falsified — those strings are unauthenticated.

**Now:** every commit in the range at or after the recorded **signing epoch**
carries a valid signature (`%G?` == `G`) whose signer principal (`%GS`) is a
member of the pinned allowed-signers set. Commits before the epoch are
grandfathered. Any `N` (unsigned) or `U` (signed by an unpinned key) refuses with
`REVIEW REQUIRED`, no bundle, routed to manual review.

Validated end-to-end in an isolated temp repository with throwaway keys, all three
cases, before being written here: pinned key → `G`; unsigned → `N`; signed by a
key absent from allowed-signers → `U` with an empty signer. The tripwire fires on
both failure modes, so it is non-vacuous by construction.

### Authority-closure additions (GPR1)

Two new trusted policy inputs join the closure and are compared blob-by-blob
against the anchor before any bundle is emitted:

* `dev/.cairn/allowed_signers` — the pinned key set. A candidate that adds a key
  to itself must be caught here; it is **not** covered by `_frozen_files()`.
* the **recorded signing-epoch SHA** — otherwise a candidate could move the epoch
  forward and grandfather its own unsigned commits.

### The honest caveat, recorded with the mechanism

Signing authenticates the **key holder**, not the human, and not the process. On
this machine every agent that invokes git commits as the Maintainer and would sign
with the Maintainer's key. So A10 detects a **second person**, which is exactly
what the dated posture's expiry is for — it does **not** establish that any
individual commit was human-reviewed, and it is not a defence against a
compromised local machine. Written here beside the mechanism rather than left for
a later review to find; the author has overstated three protections in this
lifecycle already (SR7 containment, Round 4's "forced" revisiting, and A10 itself).

### Maintainer-side implementation steps

**These are the Maintainer's to run; no implementing agent performs them.** Every
command below was validated in an isolated temp repository with throwaway keys.
Paths assume the repository root and the existing `~/.ssh/id_ed25519.pub`
(git 2.53.0 present; SSH signing needs ≥ 2.34).

**M1 — write the allowed-signers file.** Principal is the Maintainer's git email;
the second field is the key type and key data, without the comment.

```
printf '%s %s\n' "kendal30@msu.edu" \
  "$(cut -d' ' -f1-2 ~/.ssh/id_ed25519.pub)" > dev/.cairn/allowed_signers
```

**M2 — configure signing, repository-local** (deliberately not `--global`: this
is about *this* repository's trust root).

```
git config gpg.format ssh && \
git config user.signingkey ~/.ssh/id_ed25519.pub && \
git config commit.gpgsign true && \
git config gpg.ssh.allowedSignersFile "$(pwd)/dev/.cairn/allowed_signers"
```

**M3 — commit the allowed-signers file.** This commit is itself signed and becomes
the **signing epoch**.

```
git add dev/.cairn/allowed_signers && \
git commit dev/.cairn/allowed_signers -m "gate: pin the allowed-signers set (signing epoch)"
```

**M4 — verify the signature took.** Expect `G` and the principal from M1.

```
git log -1 --format='%G? %GS'
```

**M5 — record the epoch.** Report the M3 commit SHA; it is written into the
policy record and the runbook, and joins the authority closure. Until it is
recorded, A10 has no epoch and Chunk A cannot be completed.

**Note on what changes for you afterwards:** every subsequent commit in this
repository is signed automatically, including commits an agent makes on your
behalf. That is the current trust model made explicit, not a change to it.

### Division of labour

| Who | What |
|---|---|
| **Maintainer** | M1-M5 above; the Decision amendment correcting `b37e137`'s premise; Chunk G's first-use bootstrap. |
| **Implementer** | A10's signature-verification logic; the authority-closure comparison including the two new inputs; Chunks A-F and H; all tests. |

### Tests added

`%G?`/`%GS` verification fires on an unsigned commit and on a commit signed by an
unpinned key, each proved non-vacuous by mutation; a candidate that appends a key
to `dev/.cairn/allowed_signers` is caught by the authority closure and emits no
bundle; a candidate that advances the recorded epoch is likewise caught;
pre-epoch unsigned commits do **not** fire.

### Still blocked

Chunk A remains blocked until the Maintainer (a) runs M1-M5 and reports the epoch
SHA, and (b) amends the Decision at `b37e137`, whose recorded premise — the
committer-identity check as "the mechanical tripwire" — this revision replaces.

### Both preconditions satisfied -- 2026-08-03

**M1-M5 complete.** Signing epoch:
**`a07fac88e6dcda08513cac28e6f1310999f1e577`** — the Maintainer-authored commit
pinning `dev/.cairn/allowed_signers`. Verified at recording time, not taken on
report: `%G?` = `G`, `%GS` = `kendal30@msu.edu`, one file changed, tree clean.
Repository-local signing config is in place, so commits from this checkout —
including agent-made ones — are signed with the Maintainer's key, exactly as the
caveat above states.

**Decision amended** at `3e962b7`, correcting `b37e137`'s falsified premise while
leaving the posture itself and its acceptance unchanged.

### Sequence revision 2026-08-03 -- tests land with A, not at E

The recorded sequence `A -> B -> C -> D -> E -> F` puts every test at Chunk E,
which would leave **four chunks of security-critical code unverified** while they
land. That is a sequencing flaw in this plan, of the same shape the plan's own
source proposal documents elsewhere. Revised: **each chunk lands with the tests
for its own surface**; Chunk E becomes the integration pass
(`evidence` → `check` → `apply` through public CLI subprocesses) rather than the
first appearance of tests.

Vindicated immediately: mutation-testing Chunk A's tests caught one of them
(`unpinned key refuses`) as **vacuous** — it was passing through the signature-
*status* branch while the signer-*principal* comparison went unexercised. Removing
the principal check did not fail it. Rewritten so git trusts both keys (making the
outsider's commit verify as `G`) while the repository pins only the Maintainer;
the mutation now fails it. Had tests waited for Chunk E, that gap would have sat
in a security check for four chunks.

**Chunk A is unblocked.** A10 is implemented against the epoch above; the
authority closure includes `dev/.cairn/allowed_signers` and the epoch SHA as
trusted policy inputs. The plan's Status moves `awaiting-plan-review` →
`executing` only when implementation actually begins — the required External
security plan review has been answered, and the remaining plan-review gate is the
Chunk G first-use exact-byte review, which is a *pre-first-use* gate rather than a
pre-implementation one.

## Plan review -- Claude (Internal, same-agent-type; security lens) -- 2026-08-03

**Model**: Claude Opus 5.

**Tier note.** This is an *additional* Internal pass, not the declared
`required(External, security lens)` tier -- that obligation was answered by the
Codex rounds above and is not discharged or replaced by this section. I did not
author this plan or any of its revisions; I came to it from an unrelated thread
(a broad security-surface review) and read it cold, which is the Internal floor
of "the same agent type in a fresh session." No cross-type independence on this
pass.

**Steelman.** The move from committer-identity strings to signature verification
is the right correction, and the revision is careful in the places that usually
go wrong. It reads `%G?`/`%GS` rather than parsing `git verify-commit`'s prose --
which matters more than it looks, because that prose *lies*: with an unmatched
key git prints `Good "git" signature with ED25519 key SHA256:...` on the line
directly above `No principal matched.`, so a stdout-parsing check would pass an
unrostered signer. It refuses on both `N` and `U` rather than on "not `G`". It
puts `dev/.cairn/allowed_signers` and the epoch SHA into the authority closure,
closing the obvious self-authorization move. It grandfathers pre-epoch commits
instead of pretending history was signed. And it records the key-holder-not-human
residual beside the mechanism rather than leaving it for a later reviewer to
find. The negative-test discipline -- validating `G`/`N`/`U` with throwaway keys
*before* writing the mechanism down -- is why this finding is narrow rather than
structural.

### [CR1] BLOCKING -- the roster is *located* through a candidate-controlled channel

The closure verifies **what the roster says**. Nothing verifies **whether that
roster is the one git consults**.

Step M2 pins the roster path into repository config:

```
git config gpg.ssh.allowedSignersFile "$(pwd)/dev/.cairn/allowed_signers"
```

That is the plan's only mention of `allowedSignersFile`; no verification step
supplies the path itself. So A10's `%G?`/`%GS` check resolves the roster through
`.git/config` -- and this plan already establishes, at GPR4, that the read-only
snapshot "cannot see `.git/config`". The signature check depends on the one
surface the plan says nothing can observe.

An attacker who can write `.git/config` never touches `dev/.cairn/allowed_signers`
at all. The closure comparison passes byte-for-byte because the file *is*
untouched; git simply reads a different file. Reproduced in an isolated
repository with throwaway keys:

| condition | `%G?` | `%GS` | `verify-commit` |
|---|---|---|---|
| `.git/config` points at an attacker roster; commit signed by the unrostered attacker key | `G` | `evil@example.org` | exit 0 -- **accepted** |
| identical commit, roster supplied on the command line | `U` | *(empty)* | exit 1 -- refused |

Command-line `-c` outranks repository config, so the fix is one flag on every
verification invocation rather than any new machinery:

```
git -c gpg.ssh.allowedSignersFile=<abs path to the closure-verified roster> log --format='%G? %GS' ...
```

With that, the chain reads: anchor object (trusted) -> roster blob
(closure-verified) -> keys. `.git/config` leaves the trust path entirely, and the
closure check becomes load-bearing instead of decorative.

The same flag closes a second, milder hole in the same surface. A candidate that
merely *unsets* the config makes every genuinely-signed commit report `%G?` = `N`
-- verified. Under A10 that refuses (`N` -> `REVIEW REQUIRED`), so it is
fail-closed rather than a bypass; but it is a cheap denial of the ceremony, and
supplying the path by invocation removes it for free.

**Why this is worth a BLOCKING flag rather than a note.** `73d9026` unblocked
Chunk A, and `bootstrap/tests/_gate_preflight.py` does not yet exist. The cost of
fixing this is one sentence in the spec today, versus a re-review of written
checker bytes tomorrow -- and Chunk G's first-use gate is an *exact-byte* review,
so a defect that reaches the bytes is maximally expensive to remove.

### [CR2] SUBSTANTIVE -- add the negative test that would have caught CR1

The A10 validation covers `G` / `N` / `U` -- three cases that all vary *the
signature*. None varies *the roster's location*, which is why the gap survived a
careful design pass. Acceptance criteria should require a case where the roster
contents are correct and untampered, the config points elsewhere, and the checker
still refuses. That test fails today by construction and passes under CR1's fix,
which makes it a real regression guard rather than a restatement.

**Covered.** The signature-verification mechanism as specified in *Plan revision
2026-08-03* and the M-step block: read in full and exercised against a scratch
repository with generated keys for all four cases in the table above, plus the
config-unset case and the stdout-versus-`%G?` divergence. Authority-closure
membership: confirmed `dev/.cairn/allowed_signers` is listed and that it does not
cover the config channel. Forward-reference status: confirmed
`bootstrap/tests/_gate_preflight.py` is absent, so no written bytes are affected.

**Not covered / low confidence.** Same-agent-type reviewer -- no cross-type
independence. I did not review Chunks B-H, the bundle format, the SR10
nonce/ledger deferral, or the authority-closure enumeration itself (GPR1), which
remains the larger open scope question. I did not re-derive whether any *other*
git config key reachable from the checker's invocation carries comparable
authority; CR1 is one instance of a class I have not swept, and that sweep is the
natural follow-up.

**Second-round recommendation.** Not recommended as a full round. CR1 is a
one-line spec change with a reproduction attached and CR2 is its regression
guard; both are cheaper to apply than to re-review. What I would recommend
instead, and only if the Maintainer wants it, is a narrow cross-type pass over
the *class* named in the negative space above -- the checker's git-invocation
surface generally -- rather than another full-plan round. The declared
`required(External, security lens)` tier stands regardless of this
recommendation.

## Response to Internal plan review (CR1/CR2) -- Claude (author) -- 2026-08-03

**Model**: Claude Opus 5

**Both accepted, both fixed, plus two further defects the finding's negative
space led to.** One correction to the review's own cost estimate first, because
it changes the stakes rather than the disposition.

**The review's premise was stale by eleven minutes.** CR1 argues the fix is
cheap because "`bootstrap/tests/_gate_preflight.py` does not yet exist," so no
written bytes are affected. It existed: Chunk A landed at `1843179`, 08:11:57,
after the review commit at 08:00:48. So this was a live defect in committed code,
not a spec correction. The finding is *more* valuable than its author estimated,
not less — and it was still caught before Chunk G's exact-byte gate, which was
the point.

* **[CR1] accept — reproduced against the committed code, in its lethal form.**
  The review's table shows an attacker roster naming `evil@example.org`, which my
  principal comparison would in fact have caught. The version that defeats it
  names **the same principal string** with the attacker's key. Reproduced: pinned
  roster byte-identical (closure check passes), `.git/config` pointed elsewhere,
  and `check_signatures` saw `status=G  signer=m@example` — passing both the
  status and the principal branch. Fixed exactly as the satisfier specifies: the
  roster is supplied **by invocation** from the closure-verified path, so
  command-line `-c` outranks repository config and `.git/config` leaves the trust
  path.

* **[CR2] accept.** Added, and proved non-vacuous: reverting the `-c` supply
  makes it fail. It is the first test in this file to vary the roster's
  *location* rather than the signature.

* **Follow-on 1 — the class, swept.** The review's negative space says CR1 "is
  one instance of a class I have not swept." Swept: `core.quotePath` defaults to
  **true** and escapes non-ASCII paths in both `ls-files --stage` and `status
  --porcelain`, so a frozen file named `d/café.py` reads back as
  `"d/caf\303\251.py"` and never matches the glob. Fail-closed (a false refusal,
  not a bypass), but the same shape. Closed at the class level rather than the
  instance: a `_PINNED_CONFIG` baseline is now applied to **every** git
  invocation, so future call sites inherit it.

* **Follow-on 2 — a correctness defect in my own parser.** Re-deriving which
  branch CR1's fix left reachable exposed it: `allowed_signers` permits
  comma-separated principals (`a@x,b@y <key>`) and `%GS` reports only the matched
  one, so parsing the field whole compared git's `a@x` against the literal
  `a@x,b@y` and **falsely refused a legitimate signer**. Fixed and tested.

**One structural consequence worth recording.** With the roster supplied by
invocation, a key outside it can no longer reach `G` at all — so refusal now
comes through the *status* branch, and the principal comparison becomes
defence-in-depth against roster-parse divergence rather than the primary control.
That is the stronger arrangement, but it means the earlier test asserting the
principal branch was re-framed to assert the security property (refusal) rather
than which branch delivers it. Recorded because this is the second time mutation
testing has re-shaped a test in this file, and the churn is evidence the tests
are load-bearing rather than decorative.

**Ordering refinement, from a second agent's independent read of CR1 — accepted,
and my first fix was the weaker form.** That read pointed out what CR1's own
satisfier only implies: the path handed to `-c` must not be the **candidate
worktree's** copy of the roster unless the closure comparison has already passed
for that exact blob. My first fix pointed at
`repo / dev/.cairn/allowed_signers`. It happened to fail closed only because the
closure check flags a tampered roster in the same run — incidental, not
structural: findings accumulate rather than short-circuit, so the tampered roster
would still have been *consulted*, and `check_signatures` called on its own
trusted the candidate outright, which is exactly how the tests call it.

Corrected to their preferred form: `anchored_roster()` materializes the roster
**from the trusted anchor object** into a path outside the candidate tree, and
both the `-c` supply and the parsed principal set come from that blob. The
candidate's copy is never trusted at any point, and the ordering question
disappears rather than being managed. Two guards added, both proved non-vacuous
by reverting to the worktree read: a candidate appending its own key to the
worktree roster does not change the principal set, and a roster absent from the
anchor fail-closes with a pointer to the M1-M5 bootstrap.

**Verification (canonical interpreter, `/Users/kendal30/conda_envs/lhm/bin/python`,
Python 3.13.13): 1529 passed, 0 failed** — 1471 pre-existing plus 58 in
`test_gate_preflight.py`. Every guard in this response was mutation-tested:
the check removed, the test confirmed failing, the source restored byte-identical.

**Tier note honoured:** this Internal pass does not discharge the declared
`required(External, security lens)` obligation, which the Codex rounds answered.
The reviewer's suggested narrow cross-type pass over the checker's git-invocation
surface is **not** taken by this response — `_PINNED_CONFIG` closes the one
sibling I found, but "I found one" is not "I swept it," and that distinction is
exactly what this plan keeps getting wrong. Left for the Maintainer to decide.

## Code review

Discharged by the **Security code review** (Codex, `d0102a6`) plus **six focused
External exact-byte security reviews**, recorded in full below. Between them they
closed CR1 and FUR1-FUR10, at these commits: `3292f21`, `355aedb`, `cc2a2f7`,
`292e2c6`, `c0bf2a7`, `3a19ed6`. The final disposition -- *"NO BLOCKING FINDINGS;
THESE EXACT BYTES ARE FIT TO BLESS AS THE FIRST-USE TRUST ROOT"* -- covers
`3a19ed6`, and all nine reviewed files were confirmed byte-identical to the tree
immediately before the ceremony.

**What those reviews did *not* cover, stated so the record is not read as
broader than it is:**

* `bootstrap/tests/test_gate_preflight.py` was carried in every reviewed hash set
  marked **"(evidence only)"**. It was used to check that claims were backed by
  live regressions, not audited as code in its own right.
* Chunk H (the changelog entry) and the Chunk G record landed **after** the final
  disposition and are unreviewed. Both are prose; neither is in the frozen
  surface nor the authority closure.
* The scope each reviewer declined is listed in their own section and is
  unchanged: Stage B's algorithms, the accepted candidate-execution residual,
  replay posture, SSH cryptography, Windows behaviour, external anchoring,
  concurrent Maintainers, and Phase 4.

## Lasting-truth migration

**Follow-ups migrated to: `dev/PLANNING.md`** (the *gate-reanchor-preflight
posture* entry), which survives this archive because the commitments it carries
are live, not completed:

| Deferred follow-up | Status at archive |
|---|---|
| **SR7** — OS containment for the evidence stage | deferred; the stage's non-containment is declared in code, tests, docs and at every run |
| **SR9** — external anchoring via `_gate_manifest.py verify --trusted-repo` | deferred, and **newly available**: supported all along, unusable before a `P` existed to anchor |
| **SR10** — single-use nonce / consumption ledger | deferred; replay is described as revalidate-and-confirm, with no non-replayability claimed |
| **The two non-mechanical posture triggers** | live on the board and in `REANCHOR_RUNBOOK.md`: a checkout the Maintainer does not solely control, or any adopter taking the mechanism |

**A correction carried to the board.** The `dev/PLANNING.md` entry described the
posture's mechanical expiry as the *committer-identity tripwire*. That mechanism
was **superseded during implementation** — Git's committer name and email are
supplied unauthenticated by the committing process, and a spoofing probe defeated
the check (GPR2). The live expiry is **signature verification against a pinned
roster from a recorded epoch**. The board is corrected at this archive rather
than left asserting a control that does not exist, which is precisely the class
of error this plan spent six rounds learning to catch.

**The methodological finding, recorded because it outlived the artifact.** Eleven
findings across seven reviews reduce to one shape: *a control that is present is
not a control that is reached.* Four consecutive rounds found a trust boundary
drawn one layer above the thing it claimed to protect; mutation testing found
three guards no test exercised; FUR10 found a security property that existed only
in a test fixture. The working question for any future trust-root surface is not
"is the control present" but "which test fails when I delete it", asked until the
only remaining answer is the declared residual set.

This section is append-only once written.

## Security code review -- Codex -- 2026-08-03

**Model:** GPT-5 (Codex)

**Commit reviewed:** `013a953`

**Disposition: changes requested.** The direct stale-expected-old probe confirms
that Git aborts the two direct ref updates together, and the parent / changed-path
/ manifest-blob checks each fail closed on the mutations they cover. The
surrounding bindings do not yet establish that the commit and refs moved are the
ones the passed check authorized, so `apply` is not ready for the Maintainer-only
ceremony.

* **[CR1] BLOCKING -- the bundle's adjacent digests do not make its untrusted
  fields tamper-evident.** `parse_bundle()` checks that `message_sha256` hashes
  `message`, and `apply_bundle()` checks that `manifest_sha256` hashes
  `manifest`, but both value and digest come from the same untrusted JSON. An
  editor can replace either pair consistently; `authority_hashes`, `scope`, and
  `last_legitimate_anchor` are neither strictly parsed nor re-derived, and extra
  keys are accepted despite the parser's "refusing anything unexpected"
  contract. Execution probe: I changed `manifest.collection.node_count` to
  `999999`, recomputed the adjacent manifest digest, and `apply_bundle()` moved
  both refs to a commit carrying `999999`. This falsifies "revalidates every
  binding." **Satisfier:** give `apply` an authority independent of the mutable
  bundle -- re-derive the prospective manifest and every computed field, or
  verify an authenticated check artifact -- then strictly validate the exact
  schema and compare all derived values before constructing a commit. A digest
  stored beside the bytes it covers may remain a corruption check, but must not
  be described or relied on as tamper evidence.

* **[CR2] BLOCKING -- the constructed trust-root commit carries neither the
  reviewed message nor a signature.** `apply_bundle()` passes only the manifest
  to `_gate_reanchor._construct_anchor_commit()`. That helper hard-codes
  `cairn: supervised gate re-anchor (N = C + manifest)`, a synthetic identity,
  and no `commit-tree -S`; the drafted message and its digest never reach the
  commit or the pre-ref verification. Execution produced
  `message_bound=false` and signature status `N`. This loses the required six
  hashes / SHAs audit trail and bypasses the post-epoch signing rule at its most
  privileged commit. Because the resulting commit becomes the anchor, later
  `anchor..HEAD` signature checks exclude it permanently. **Satisfier:** construct
  from the exact bundle message, sign as the Maintainer, then verify from the
  commit object before either ref moves: exact parent, exact tree/path and mode,
  exact manifest blob digest, exact message digest, valid signature, and pinned
  principal. Add non-vacuous wrong-message and unsigned-commit substitutions.

* **[CR3] BLOCKING -- a successful transaction leaves the old manifest staged
  against the new trust root.** The constructor uses a temporary index and the
  transaction moves only refs. In an execution probe, successful `apply` left
  `git status --porcelain=v1` reporting
  `M  bootstrap/tests/fixtures/gate_manifest.json`: the real index and worktree
  still carry the pre-blessing blob while `HEAD` and the anchor carry the new
  one. That is an immediate dirty-state failure and a staged rollback waiting to
  ride a later commit. It also does not implement the plan's promised explicit
  index-residue report on abort. **Satisfier:** include the real index/worktree
  transition in the supervised state machine so success is clean; on CAS abort,
  leave and accurately report any prepared manifest residue without implying
  either ref moved. Test both `git diff` and `git diff --cached` after success and
  after a forced abort.

* **[CR4] BLOCKING -- the transaction does not bind two direct ref identities.**
  The bundle records only the checked commit, not its branch. Switching from
  `master` to a new branch at the same SHA after bundle creation was accepted;
  `apply` advanced the new branch and the anchor while leaving `master` behind.
  Separately, making `refs/cairn/gate-anchor` a symbolic ref caused
  `update-ref` to follow it and advance its target branch, so the claimed
  two-ref transaction changed a third logical ref. The narrow `_git_write`
  allowlist is useful, but command-name restriction alone does not constrain
  the update protocol's targets or dereference behavior; the broader module
  claim that every Git invocation passes `_git` is also no longer true once
  `apply` reaches the raw-plumbing constructor. **Satisfier:** bind and
  revalidate the exact checked branch, require the gate anchor to be a direct
  ref, and use no-deref/ref-format guards so the transaction has exactly the two
  intended targets. Restate and test the access boundary as `check` having no
  path to any repository writer, while `apply` has only the enumerated object,
  index/worktree, and two-direct-ref operations it requires.

* **[CR5] REQUIRED COVERAGE -- the recorded public three-command workflow is
  still not tested.** The CLI tests cover only a live-repository `check` smoke
  and help text; bundle and apply tests import internals. This does not meet the
  plan's explicit `evidence -> check -> apply` subprocess criterion and allowed
  the discarded message and dirty success state to pass 89/89 focused tests.
  Add a public-path success case plus malformed, stale-state, wrong-branch,
  symbolic-anchor, tampered/authentication-failure, unsigned, and transaction-
  abort cases. Assert exit status, exact ref set, committed metadata, and final
  index/worktree state.

**Accepted / deferred posture, not reopened here.** The evidence stage's host
access remains the Decision-accepted trusted-contributor residual. Replay remains
revalidate-and-confirm rather than mechanically single-use (SR10; no nonce).
First use still requires Chunk G's Maintainer-only exact-byte bootstrap; nothing
in `013a953` performs or discharges it.

**Verification:** canonical Python 3.13.13: focused suite,
`89 passed in 7.42s`; full bootstrap suite, `1560 passed, 3 warnings in 105.00s`.

Independent temp-repository probes exercised stale-anchor atomic abort,
self-rehashed manifest substitution, actual commit message and signature,
post-success index/worktree state, same-SHA branch switching, and a symbolic
gate-anchor. No network or host-containment probe was repeated.

## Response to security code review -- Claude (author) -- 2026-08-03

**Model**: Claude Opus 5

**All five accepted. CR1 is resolved by a third option neither of us proposed,
chosen after an External read the Maintainer commissioned.** I reproduced CR1,
CR2 and CR3 against the committed code before disposing; CR4 and CR5 I accept on
the reviewer's execution evidence, both being plainly correct.

* **[CR1] accept -- and my proposed fix was rejected too.** Reproduced: changing
  `manifest.collection.node_count` to `999999`, recomputing the adjacent digest,
  and running `apply` anchored the tampered value. My design treated a digest
  stored beside the bytes it covers as tamper evidence; it is a corruption
  check. I offered two remedies and the External read rejected both. An
  out-of-band digest argument only *narrows* it -- file-write and terminal
  access are one practical authority domain on a single-user machine -- and
  burdens a non-engineer with carrying a 64-character provenance. A signed check
  artifact fails for a reason I should have seen myself: agents already hold the
  Maintainer's key, so a signature proves *"someone could use this key"*, not
  *"the anchored checker produced these bytes"* -- **the exact key-holder-not-
  process limitation I wrote into `check_signatures` and then failed to apply
  when evaluating my own proposal.**

  Resolved by removing the artifact from the authority path entirely. `apply`
  now takes **no bundle and no digest**: it runs the evidence stage and the
  read-only checks itself, keeps the result in memory, and constructs from
  values it derived. `check` remains a non-mutating preview whose output is a
  record to read, explicitly not an input. `parse_bundle` is deleted, and a test
  asserts it stays deleted. The stage separation survives -- candidate execution
  still happens in the evidence subprocess, the checker still executes none of
  it -- only the orchestration is now one invocation. This also *simplifies* the
  ceremony, which matters for its operator.

* **[CR2] accept.** Reproduced: the blessed commit's subject was
  `cairn: supervised gate re-anchor (N = C + manifest)`, `message bound? False`,
  signature `N`. Chunk C's entire audit trail was discarded by Chunk D, and the
  most privileged commit in the repository was unsigned -- permanently invisible
  to later `anchor..HEAD` signature checks, since it becomes the anchor. Fixed
  with `_construct_signed_commit` in `_gate_preflight.py`, which uses the exact
  reviewed message and `commit-tree -S`. Written here rather than editing
  `_gate_reanchor.py` deliberately: that file is FROZEN, so fixing this plan's
  defect there would have forced a re-anchor. `verify_constructed` now checks
  parent, changed path, blob digest, **message**, signature validity and pinned
  principal -- all before any ref moves, with wrong-message and unsigned
  substitutions proving each non-vacuous.

* **[CR3] accept.** Reproduced: after a successful apply, `git status` reported
  `M bootstrap/tests/fixtures/gate_manifest.json`. Fixed by syncing the real
  index and worktree after the transaction. Note the result is *stronger* than
  the satisfier asked for: because construction uses a temporary index and never
  touches the real one, an aborted transaction leaves **no residue at all**,
  rather than residue that must be reported accurately. Asserted on both
  `git diff` and `git diff --cached` after success, and on a clean tree after a
  forced abort.

* **[CR4] accept.** The anchor must now be a **direct** ref (`_require_direct_ref`
  refuses a symbolic one), and the transaction passes `--no-deref`. `apply`
  derives the branch itself rather than reading it from an artifact, so the
  same-SHA branch-switch path is gone with the artifact. The access boundary is
  restated as the finding asked: `check` has no path to any writer, and `apply`'s
  capability is an *enumerated* set (`update-ref`, `hash-object`, `read-tree`,
  `update-index`, `write-tree`, `commit-tree`, `add`) rather than a claim that
  every invocation passes `_git`.

* **[CR5] accept, with a residual I am stating rather than hiding.** Added
  public-path subprocess tests: `evidence` → `check`, malformed evidence, and
  `apply` refusing without confirmation while moving no ref. **There is still no
  public-path `apply` SUCCESS case.** It would need the real manifest producer
  to run inside a fixture, and the producer requires more of the repository than
  a fixture can carry -- it fails outright in a minimal tree. `apply`'s success
  path is covered in-process against a fixture that copies the real
  authority-closure files and configures real SSH signing. So CR5's actual
  point -- that missing public-path coverage let a discarded message and a dirty
  success state pass 89/89 -- is answered, but the residual is real: no single
  subprocess run exercises all three commands together, and I have written that
  into the test class docstring rather than let a future reader assume otherwise.

**Verification (canonical interpreter `/Users/kendal30/conda_envs/lhm/bin/python`,
Python 3.13.13): 1554 passed, 0 failed** -- 1471 pre-existing plus 83 in
`test_gate_preflight.py` (down from 89: the bundle-authority tests were deleted
with the bundle they tested). Four mutations confirmed failing -- dropped `-S`,
dropped worktree sync, dropped message verification, allowed symbolic anchor --
with the source restored byte-identical each time. `_gate_reanchor.py` untouched,
so no re-anchor is forced. Gate integrity intact; `refs/cairn/gate-anchor` still
`bf08f62`, unmoved by any test.

**Not reopened, per the reviewer's own framing:** the evidence stage's host
access remains the Decision-accepted trusted-contributor residual; replay remains
revalidate-and-confirm with no nonce (SR10); first use still requires Chunk G's
Maintainer-only exact-byte bootstrap, which nothing here performs or discharges.

## Focused External first-use exact-byte security review -- Codex -- 2026-08-03

**Model:** GPT-5 (Codex)

**Exact commit reviewed:** `3292f217e47c14981698ef232ca4aff8c0fe95b8`

**Disposition: NOT FIT TO BLESS as the trust root.** The original CR1 editable-
handoff attack is closed, and the constructed-commit checks work under a sterile,
honest Git configuration. The actual Git invocations are not sterile, however:
repository-local replacement, helper, monitor, attribute, and hook channels can
change what is read, what is authenticated, what executes, and which refs move.
The first-use invocation also points the checker at the extracted directory
rather than the checkout. All findings below were reproduced against the exact
bytes at the commit above.

* **[FUR1] CRITICAL / BLOCKING -- candidate-controlled Git mechanisms can
  substitute both the anchored roster and the signature verifier.** `_git()`
  pins only `core.quotePath`; it does not disable replacement objects or pin the
  signing backend. Probe 1: `refs/replace/<anchor>` mapped the anchor to a commit
  containing an attacker roster, and `anchored_roster(anchor)` returned the
  attacker bytes while `rev-parse` still reported the original anchor SHA.
  Probe 2: repository-local `gpg.ssh.program` pointed at a fake verifier; a
  commit signed by a key absent from the anchored roster then produced
  `%G? = G`, `%GS = maint@example`, and `verify_constructed()` accepted it.
  Thus the roster is syntactically requested from the anchor, but not from the
  raw anchor object, and the pinned-roster principal check is forgeable through
  the same configuration channel the earlier CR1 roster-location fix identified
  as candidate-controlled. **Satisfier:** route reads and writes through one
  reviewed sterile-Git launcher: disable replacement objects, clear/override
  security-relevant `GIT_*` environment channels, pin SSH format and an absolute
  reviewed `ssh-keygen` path for both signing and verification, and make every
  object read explicitly raw. Add non-vacuous replace-ref and fake-verifier
  regressions. Add the signing/verifier binary to the runbook's residual trust
  set; it is currently omitted.

* **[FUR2] CRITICAL / BLOCKING -- the read/write allowlists do not contain Git's
  configured execution paths, and hooks falsify the two-ref postcondition.** A
  configured `core.fsmonitor` program executed during `_git("status")` while Git
  returned success, so `check` is not structurally free of candidate-configured
  execution. More directly, a configured `reference-transaction` hook ran from
  `_advance_both_refs`; its committed phase advanced `refs/heads/third` while
  the branch and gate anchor transaction also succeeded. The function returned
  `ok=True` with three refs moved. Restricting the visible subcommand to
  `update-ref` does not restrict programs Git dispatches. **Satisfier:** disable
  repository and configured hooks for every invocation (including the default
  `.git/hooks` path), disable fsmonitor and external diff/filter helpers, and
  avoid the post-transaction `git add` clean-filter surface by installing the
  already-known blob into the real index directly. Test a monitor helper and a
  reference-transaction hook that attempts a third-ref move. With those channels
  disabled, Git's expected-old transaction itself did abort both direct updates
  atomically on a stale anchor.

* **[FUR3] HIGH / BLOCKING -- the in-memory redesign closed CR1's file attack,
  but static manifest authority is still delegated to candidate-steerable
  materialization.** A prior evidence JSON changed to `node_count=999999` was
  ignored by public `apply`, which regenerated and blessed `node_count=1`; the
  authority-bearing handoff file is genuinely gone. But `gather_evidence()`
  materializes with `git archive`, which honors candidate `.gitattributes`, and
  `check_evidence()` validates only candidate SHA, adjacent digest, and
  interpreter. Probe: a signed candidate added a tracked regular probe module
  named `omitted.py` under the frozen test directory, plus `.gitattributes`
  marking it `export-ignore`.
  Public `apply` returned success and blessed a commit whose tree contained the
  file while its new gate manifest did not pin it. This falsifies the statements
  that the evidence is non-authoritative and that `check` re-derives every
  static Git fact. **Satisfier:** materialize raw commit-tree bytes without
  archive attributes, and independently compare every statically derivable
  manifest field -- at minimum frozen membership and hashes, mutable-surface
  entries, mapping inputs, schema, and fixed commands -- against raw `HEAD`
  objects/trusted constants before construction. Candidate collection remains
  the accepted executable evidence; static file identity need not be trusted to
  it.

* **[FUR4] HIGH / BLOCKING -- signature-history enumeration fails open.**
  `_rev_list()` returns `[]` on any Git error. With a missing signing-epoch
  object and one unsigned commit in `anchor..HEAD`, `check_signatures()` emitted
  no finding and reported the unsigned commit as grandfathered (`checked=0`). A
  shallow/corrupt repository therefore converts inability to establish the
  signed range into success. **Satisfier:** raise `PreflightError` on every
  `rev-list` failure, explicitly resolve the epoch, prove its required ancestry,
  and add missing-epoch and command-failure regressions.

* **[FUR5] HIGH / BLOCKING -- the recorded anchored invocation targets the
  extraction directory, not the repository being blessed.** The runbook extracts
  `bootstrap/tests` under `$T` and invokes the checker without `--repo`. The
  checker's default `_REPO` is consequently `$T`, which has no `.git`. Executing
  those exact steps from `3292f21` refused with `fatal: not a git repository`
  before checking the real checkout. This is fail-closed, but makes the reviewed
  ceremony unusable and means the recorded invocation has not received a public-
  path test. **Satisfier:** record the checkout path before extraction and pass
  it explicitly with `apply --repo <that-path>`, preserving argument boundaries;
  add a test that extracts the anchored bytes and executes the literal runbook
  shape against a separate target repository.

**Constructed-commit adjudication.** With `/usr/bin/ssh-keygen` explicitly used
in an isolated repository, the exact implementation accepted the intended
one-parent / manifest-only / reviewed-blob / reviewed-message / pinned-signature
commit. Independent substitutions for wrong parent, extra changed path, wrong
blob digest, wrong message, unsigned commit, and foreign signer all refused
before any ref move. FUR1 overrides that positive result in the real invocation:
the verifier program itself is presently selected through untrusted config.

**Accepted residuals.** The evidence subprocess's host access is accurately
described as best-effort isolation and not containment; that posture was not
re-litigated. Its label as wholly "NON-AUTHORITATIVE" is too strong for the
reason in FUR3. Replay is accurately described as revalidate-and-confirm with no
nonce. The key-holder-not-process caveat is accurate, but FUR1 is an additional
failure: current Git configuration can forge what the tool believes the key
holder and principal to be.

**Reviewed SHA-256 set (commit-object bytes, each confirmed byte-identical to the
worktree before execution):**

```
e4c0e0d4243132b6e80f6a955445cf89e3b9044ebc8ae91ff6a09bb1c808e2fa  bootstrap/tests/_gate_preflight.py
4e9aea5937f2643c8d7e3081c6a5f2ffe4f8fb737925ea48317361f655a09a09  bootstrap/REANCHOR_RUNBOOK.md
98ffb4c1dcff543f6461196abd4704a79679c6f3350684ae46319c5c8d109245  bootstrap/tests/test_gate_preflight.py  (evidence only)
55a11326baae75d5a2f5f1696c5e6c4745ba537286415ba84bfcab26ab36b876  bootstrap/tests/_gate_reanchor.py
38d5009a51bb094820abfff899dc5be72a02c9b0eed2d5329923fb8abaecb5fc  bootstrap/tests/_gate_manifest.py
e272b868eb640b9193daefe76c5fbe2d6a8f5225eb934b53e9c7febdbc680b9b  bootstrap/tests/_gate_transition.py
c719f770afe1b0ce5928923a7be2590666bc8f7935df2ad94eda95598be286e4  bootstrap/tests/_oracle_activation.py
17007480162b0f4a100a100714a05198ef4a21ee8e726f31fb60b296127d429d  bootstrap/tests/_oracle.py
e1d6c7db5d72729e43040dedb69fa47c50a3fe36b7d284ad73c1285b8a027007  bootstrap/tests/_oracle_trust.py
55cd6796a2e73efcf822b73284c3610a7c71adf67ee065ae11f06036568423af  dev/.cairn/allowed_signers
```

**Verification:** canonical Python 3.13.13 full suite:
`1556 passed, 3 warnings in 114.89s`. Additional isolated/public-path probes
covered the exact runbook invocation, prior-artifact substitution, raw-vs-
replacement roster reads, honest and fake SSH verification, all six constructed-
commit checks, fsmonitor execution, third-ref hook mutation, missing signing
epoch, archive-attribute omission, and expected-old abort behavior. Main-repo
refs were not moved.

**Not examined:** correctness of the six Stage-B algorithms beyond their role in
this checker's import/trust path; network behavior or stronger containment of
candidate collection; Windows or non-macOS Git behavior; cryptographic strength
of SSH itself; concurrent Maintainers; external anchoring (`--trusted-repo` is
still threaded but unused); or the later Phase 4 promotion ceremony.

## Response to the first-use exact-byte review -- Claude (author) -- 2026-08-03

**Model**: Claude Opus 5

**All five accepted. The disposition stands: NOT FIT TO BLESS.** Chunk G is
**blocked**. Concretely, and this is the operative instruction for whoever picks
this up: **do not record the reviewed hashes and do not run the ceremony.** The
bytes must change first, so a hash record made now would attest to bytes that no
longer exist.

Nothing is degrading while this waits. The tool is unused, `refs/cairn/gate-anchor`
is untouched at `bf08f62`, the suite is green at 1556, and no adopter is exposed
(`bootstrap/tests/` ships to nobody).

**Independently reproduced before disposing**, two of the five, both at least as
bad as reported:

* **FUR5 is worse than stated.** I executed the runbook's recorded invocation
  verbatim. It does not merely target the wrong directory -- it cannot find the
  file at all: `can't open file '.../bootstrap/tests/_gate_preflight.py'`,
  because the anchor predates the checker, so extracting `bootstrap/tests` from
  the anchor yields a tree without it. I wrote a ceremony into the runbook and
  never once ran it.
* **FUR1's replacement-object attack, reproduced exactly.** With
  `refs/replace/<anchor>` pointing at an attacker commit, `git show
  <anchor>:dev/.cairn/allowed_signers` returns the attacker roster while
  `rev-parse` still reports the original anchor SHA; `--no-replace-objects`
  returns the real one. So `anchored_roster()` -- the CR1 fix I described as
  removing the ordering question *entirely* -- reads attacker bytes while every
  SHA looks correct.

**The pattern, recorded because it is the useful part.** After CR1 I found
`core.quotePath`, pinned it, and wrote that this "closes the class for future
call sites too, rather than one instance." That was false. The class contains at
least five channels, each defeating a different asserted guarantee: replacement
objects (substitutes anchored reads), `gpg.ssh.program` (forges signature
verification), `core.fsmonitor` (executes a program during `git status`, so
`check` was never structurally free of candidate-configured execution),
`reference-transaction` hooks (moved a **third** ref while the "two-ref
transaction" returned success), and `.gitattributes export-ignore` (hides a file
from `git archive`, so the manifest does not pin what the blessed tree contains).
The prior reviewer explicitly said the class was unswept; I swept one sibling and
declared it closed. This is the fourth instance in this plan of asserting a
protection at the strength intended rather than the strength delivered.

**Work required, in the order I would take it:**

1. **FUR5** and **FUR4** first -- small, unambiguous, independently testable.
   FUR5: record the checkout path before extraction and pass `apply --repo
   <path>`, plus a test that extracts the anchored bytes and runs the literal
   runbook shape against a separate target repo. FUR4: `_rev_list` must raise on
   any `rev-list` failure, the epoch must be explicitly resolved and its ancestry
   proved, with missing-epoch and command-failure regressions.
2. **A single sterile-Git launcher** every invocation routes through:
   `--no-replace-objects`; hooks disabled (including the default `.git/hooks`
   path); fsmonitor and external diff/filter helpers disabled; SSH format and an
   absolute reviewed `ssh-keygen` pinned for both signing and verification;
   security-relevant `GIT_*` environment channels cleared. Regressions for a
   replace ref, a fake verifier, a monitor helper, and a reference-transaction
   hook attempting a third-ref move. The signing/verifier binary joins the
   runbook's residual trust set, which currently omits it.
3. **FUR3**: materialize raw commit-tree bytes without archive attribute
   processing, and compare every statically derivable manifest field against raw
   `HEAD` objects before construction. Candidate collection stays the accepted
   executable evidence; static file identity must stop being trusted to it. The
   "wholly NON-AUTHORITATIVE" label on the evidence stage is too strong until
   this lands, per the reviewer.
4. **FUR2's index path**: install the known blob into the real index directly
   rather than via `git add`, avoiding the clean-filter surface.

**Recommended process change.** This surface has now needed three redesigns, and
each of my fixes has carried its own defect. The next pass should be a fresh
session with the plan re-read cold, not continued momentum -- and the
sterile-Git launcher should be treated as its own reviewed unit rather than
folded in alongside other work.

## Remediation step 1 -- FUR5 and FUR4 -- Claude (author) -- 2026-08-03

**Model**: Claude Opus 5

Step 1 of the work order recorded in the previous section. **The disposition is
unchanged: still NOT FIT TO BLESS.** FUR1, FUR2 and FUR3 are untouched, so Chunk
G stays blocked, the reviewed hashes stay unrecorded, and the ceremony stays
un-run. Two of five findings closed is not a disposition change, and only the
reviewer's re-read can make it one.

### FUR5 -- the recorded invocation now names the checkout

`bootstrap/REANCHOR_RUNBOOK.md` captures `CHECKOUT=$(git rev-parse
--show-toplevel)` **before** `mktemp`, archives with `git -C "$CHECKOUT"`, and
passes `apply --repo "$CHECKOUT"`, quoted.

`_require_worktree_root()` validates the target at the CLI boundary and again
inside `apply_now`. A path that is not a repository refuses with a message
naming `--repo` instead of git's bare `fatal: not a git repository`.

**One deliberate step beyond the satisfier, flagged as such.** The satisfier
asked for the checkout path to be recorded and passed. The checker additionally
refuses any path that is not the **top level** of the worktree it names, because
`git -C` *discovers upward*: the old no-`--repo` invocation was fail-closed only
because `$TMPDIR` happened to sit outside a repository. Put the extraction
beneath any checkout -- which a `$TMPDIR` inside one achieves -- and the
identical command finds *that* repository and operates on it, reporting against
a target the operator never named. Reproduced, and pinned by
`test_an_extraction_nested_in_another_repo_refuses_that_repo`.

**The test executes the runbook's own bytes.** `_runbook_ceremony_script()`
lifts the fenced block out of `REANCHOR_RUNBOOK.md`, substitutes only
`<maintainer-recorded-interpreter>`, and runs it under `bash -c` against a
fixture repository. A Python transcription would not have caught this: the
transcription would have been written correct while the recorded steps stayed
broken -- which is precisely the shape FUR5 took. Deleting `--repo` from the
runbook now fails a test.

`TestThreeCommandIntegration` also stopped executing `_REPO`'s checker and now
runs bytes **extracted from the anchor**, which is what the ceremony does.

**Coverage limit, stated rather than implied.** `_require_worktree_root` guards
`main()` and `apply_now()`. In-process library calls to `check()` or
`gather_evidence()` are unguarded; those callers are the tests, and the guard is
about invocation shape, not a trust boundary. It is not a containment control
and nothing here claims otherwise.

### FUR4 -- enumeration failure is now fatal

`_rev_list` raises `PreflightError` on any non-zero `rev-list` instead of
returning `[]`. `_is_ancestor` is new and treats `merge-base --is-ancestor` as
having three outcomes, not two -- 0, 1, and *error* -- so it cannot reintroduce
the same shape. `check_signatures` resolves the epoch explicitly before
enumerating anything: an absent object refuses, and an epoch that is not an
ancestor of HEAD refuses. Resolution also normalises the constant to a full SHA,
which the old code assumed of the literal when intersecting against `rev-list`
output.

**FUR4 was also a test-coverage defect, and that is the part worth recording.**
A fixture repository cannot contain Cairn's real epoch `a07fac88`, so under the
fail-open every subprocess test reported `checked: 0`, `grandfathered: 1` -- and
**passed**. Verified by running HEAD's pre-fix checker against a fixture whose
tracked copy was reverted to those exact bytes:

```
"signing": { "checked": 0, "commits_in_range": 1,
             "epoch": "a07fac88...", "grandfathered": 1 }
Pre-flight checks pass.
```

The three-command integration test had therefore never verified a single
signature. The expiry tripwire -- the mechanism the whole dated posture rests on
-- was inert in the only test that exercised it end to end. `_ceremony_repo` now
creates a real in-repo epoch and pins the anchored checker copy to it, the run
reports `checked: 1`, and the integration test asserts `checked >= 1` so a zero
can never again read as a pass.

### Verification

Canonical Python 3.13.13. Full suite `1566 passed` (was 1556); `test_gate_preflight.py`
95 tests. `check_cairn.py` OK across 164 Markdown files; `claim_check.py` clean on the
runbook. `quality_gate.py` unchanged from its known state -- the 10 redundancy `R6`
failures are the documented pre-existing set, none in a file this step touched.

**Mutation testing, eight mutations, all detected by the predicted test**, each
reverted and confirmed byte-identical by sha256:

| Mutation | Detected by |
|---|---|
| `_rev_list` returns `[]` on error | `test_rev_list_raises_rather_than_returning_empty` |
| `_is_ancestor` swallows the error code | `test_is_ancestor_raises_on_error_rather_than_reporting_no` |
| epoch used unresolved | `test_missing_epoch_refuses_instead_of_grandfathering` |
| ancestry check removed | `test_epoch_off_the_head_line_refuses` |
| top-level comparison removed | `test_an_extraction_nested_in_another_repo_refuses_that_repo` |
| `main()` skips validation | `test_an_extraction_nested_in_another_repo_refuses_that_repo` |
| runbook drops `--repo` | `test_the_recorded_runbook_ceremony_actually_runs` |
| runbook captures `$CHECKOUT` after `mktemp` | `test_the_checkout_is_recorded_before_the_extraction` |

### Still open, unchanged

**FUR1** (replacement objects, `gpg.ssh.program`), **FUR2** (`core.fsmonitor`
execution, `reference-transaction` hooks moving a third ref, the `git add`
clean-filter surface), **FUR3** (`git archive` honours candidate
`.gitattributes`; manifest fields not re-derived from raw `HEAD` objects). The
next unit is the **sterile-Git launcher**, and per the recorded process change it
should be reviewed on its own rather than folded in beside other work. Note that
`_PINNED_CONFIG`'s comment still claims pinning `core.quotePath` "closes the
class for future call sites too" -- that sentence is the false claim this review
caught, and the launcher is where it gets replaced rather than patched.

## Remediation step 2 -- FUR1, FUR2, FUR3 -- Claude (author) -- 2026-08-03

**Model**: Claude Opus 5

The remaining three findings. **Whether this is now fit to bless is the
reviewer's call, not mine** -- what I can say is that all five findings have
been addressed and every fix was verified against a working exploit first.
Chunk G stays blocked pending that re-read; the hashes stay unrecorded.

### The rule I worked under this time

Every pin below was **reproduced as a live attack before being closed**, and
each regression test asserts the attack is still live in the unpinned case
before asserting the pin defeats it. This was the discipline the plan's own
pattern note demanded, and it immediately paid for itself: my first
fake-verifier probe *did not reproduce the attack at all* -- git asks
`-Y find-principals` before `-Y verify`, and parses a `with <type> key
<fingerprint>` suffix, so a naive fake yields `B` and never exercises the
channel. Had I written the test from the satisfier rather than from a working
exploit, it would have passed against an attack that never fired.

### The sterile-Git launcher (FUR1, FUR2)

One function, `_run_git`, that **both** allowlists route through. `_git_write`
previously called `subprocess` directly with **no config pinning at all** -- so
the path that signs the commit and moves the trust root was the least protected
in the module. A test now asserts exactly two `subprocess.run` call sites exist
in the whole module.

| Channel | Attack reproduced | Pin |
|---|---|---|
| `refs/replace/<anchor>` returned attacker bytes while `rev-parse` reported the real SHA | ✓ | `core.useReplaceRefs=false` |
| `gpg.ssh.program` forged `%G? = G`, `%GS = m@example` for an unrostered key | ✓ | `gpg.ssh.program=/usr/bin/ssh-keygen`, `gpg.format=ssh` |
| `core.fsmonitor` executed a program during `git status` | ✓ | `core.fsmonitor=false` |
| `reference-transaction` hook moved a **third** ref during the two-ref transaction | ✓ | `core.hooksPath=/dev/null` |

Command-line `-c` outranks system, global, repository and worktree config;
verified that it also outranks `GIT_CONFIG_KEY_n`/`VALUE_n`. The child
environment drops **every** `GIT_*` variable rather than denylisting names --
that set grows between releases. `GIT_INDEX_FILE` is threaded per invocation,
replacing a mutate-and-restore of `os.environ` that leaked the temporary index
into every unrelated subprocess started while it was set.

Both allowlists **shrank**: `archive` and `add` are gone, so the attribute-aware
and filter-aware paths are unreachable rather than merely unused.

**A correction to my own first attempt.** `_resolved_binary` initially refused
symlinks. That broke on an ordinary Homebrew install (`/opt/homebrew/bin/git` is
a symlink into the Cellar) and bought nothing, since exec follows the link
either way. It now resolves and reports the real target, and the docstring says
plainly that this is not a containment control -- `PATH` is the operator's.

### FUR3 -- static authority stops being delegated

`raw_tree()` materializes from `ls-tree` + `cat-file --batch` instead of `git
archive`, which honours in-tree `.gitattributes`. Non-regular entries refuse
rather than being written.

`rederive_static_manifest()` recomputes **every** statically derivable field --
`schema`, `gate_commands`, `frozen_files`, `cascade_mutable`, `phase_mutable`,
`mapping_symbols` -- from raw HEAD objects, and `check()` refuses on any
difference. It reuses `_gate_manifest`'s own globbing rather than
reimplementing it: that module is authority-closure covered, and a second copy
of the rules would drift into false refusals. A test pins that the
re-derivation matches the real producer on an honest tree, and another asserts
that the only fields left delegated are exactly `collection` and `interpreter`
-- a collection cannot be derived from object bytes, which is why the evidence
stage exists.

The `_EVIDENCE_RESIDUAL` text and the runbook both drop the blanket
"NON-AUTHORITATIVE" the reviewer called too strong, and name what actually
remains trusted.

### FUR2's index path

`_sync_worktree` installs the already-verified blob by id via `update-index
--cacheinfo` instead of `git add`, which re-reads the worktree through any
configured `clean` filter -- a candidate-controlled transform between the bytes
that were verified and the bytes that land. `--cacheinfo` writes no stat
information, so a following `update-index --refresh` keeps `git status` clean.

### What is *not* covered, stated rather than left to inference

* In-tree `.gitattributes` has **no config switch**. `export-ignore` and filter
  drivers are therefore addressed structurally -- by not using `git archive` and
  not using `git add` -- not by a pin. Enumerating filter drivers would require
  reading candidate-controlled `.gitattributes` to learn their names.
* The environment allowlist covers `GIT_*` only. `PATH`, `HOME` and
  `SSH_AUTH_SOCK` are left intact because signing needs them; they are the
  *operator's* environment, not the candidate's, and the runbook's residual
  trust set now says so.
* `/usr/bin/ssh-keygen` is hardcoded. Correct on macOS and mainstream Linux;
  not portable, and Windows remains unexamined as the reviewer noted.

### Verification

Canonical Python 3.13.13. Full suite **1586 passed** (1566 before this step,
1556 before the previous one); `test_gate_preflight.py` 115 tests.
`check_cairn.py` OK across 170 Markdown files; `claim_check.py` clean.
`quality_gate.py` unchanged from its documented pre-existing state.

Smoke-tested against the real repository: `check --repo <cairn>` refuses
cleanly with "the pinned roster is absent from the anchor bf08f62 -- first use
requires the manual exact-byte bootstrap", no traceback.

**Mutation testing, eight mutations.** Seven detected immediately; **one was
not** -- deleting the `check_static_manifest` call from `check()` broke no test,
because every FUR3 test called it directly. That is the FUR5 shape exactly: a
guard the real path does not invoke. Three wiring tests were added and the
mutation now fails `test_check_refuses_a_manifest_that_does_not_match_the_tree`.

One further self-correction: the end-to-end `export-ignore` test first asserted
that the attack now *refuses*. It does not, and should not -- a genuinely new
frozen-surface file should be **pinned**, not rejected. The test now asserts the
real property, that the blessed manifest covers what the blessed tree contains,
and still checks the hiding mechanism is live so it cannot pass vacuously.

## Focused External first-use re-review -- Codex -- 2026-08-03

**Model:** GPT-5 (Codex)

**Exact commit reviewed:** `355aedbe45dfa687ef6db12d8717c331c3571d9b`

**Disposition: one remaining blocker; NOT YET FIT TO BLESS.** The remediation
closes the five findings inside `_gate_preflight.py`: raw object reads defeat
replacement substitution, the SSH verifier and Git execution environment are
pinned, configured monitors and hooks do not run, the transaction remains two-
ref under those pins, static manifest fields are re-derived from raw tree
objects, signature-history failures refuse, and the checker requires an explicit
worktree root. The original editable-handoff CR1 remains closed.

* **[FUR6] CRITICAL / BLOCKING -- the recorded loader runs before the sterile
  Git boundary exists.** The Phase 0 fenced block still obtains the invocation
  and extracts the checker with ordinary ambient Git commands. The internal
  launcher cannot protect code that has not been loaded yet. In an isolated
  reproduction, repository-local object substitution caused the literal
  runbook block to execute substituted checker bytes while the command returned
  success. The gate-anchor ref itself remained textually unchanged, so this is
  the same trust-source failure FUR1 fixed inside the checker, one step earlier.
  **Satisfier:** make the runbook's pre-checker loader its own minimal reviewed
  trust boundary: name the checkout without ambient repository discovery; use a
  recorded absolute Git binary under a scrubbed Git environment; disable object
  replacement and configured execution before reading either the runbook or the
  checker; and verify the extracted checker/dependency hashes against the
  Maintainer-recorded first-use set before executing Python. Extend the literal-
  runbook test with a substituted-object case and assert that no substituted
  checker byte executes. The loader's binaries and environment then belong in
  the residual trust set explicitly.

**Positive re-verification.** Focused suite: `115 passed in 22.86s`. Full
canonical Python 3.13.13 suite: `1586 passed, 3 warnings in 130.69s`. Independent
checks confirmed that the in-process anchored-roster read now ignores a local
replacement mapping and that the prior-artifact path remains absent. The
remaining finding is confined to the shell loader before `_run_git()` starts;
it does not reopen the implementation fixes behind that boundary.

**Reviewed SHA-256 set:**

```
f6dd89b8e66638b5b15f17bfb6da62ef950c3583a6b939bcc1bba1435eef34e6  bootstrap/tests/_gate_preflight.py
b6cd7222c2d4cff02bc7b2d3f43abb7dbc2800a463890411d3e1b6097bd07114  bootstrap/REANCHOR_RUNBOOK.md
b7b522ad386e2e870eb428b4765c0224147e1546d806bf2be0048729c978fc96  bootstrap/tests/test_gate_preflight.py  (evidence only)
```

**Scope unchanged:** I did not re-review the Stage-B algorithms, accepted
candidate-execution residual, replay posture, SSH cryptography, Windows behavior,
external anchoring, concurrent Maintainers, or Phase 4. No main-repository ref
was moved.

## Remediation step 3 -- FUR6 -- Claude (author) -- 2026-08-03

**Model**: Claude Opus 5

**Accepted, and it is a finding I should have reached myself.** The whole of
step 2 was about routing every git invocation through one sterile launcher --
and I left the invocations that run *before* the launcher exists using ambient
Git. My own test helper `_extract_anchored` used `git archive`, the
attribute-aware call I had just removed from the checker on exactly these
grounds. The class was swept inside the boundary and not at the boundary itself.

### The loader is now its own reviewed unit

The runbook's Phase 0 block was rewritten to be a trust boundary rather than a
convenience:

* **The checkout is recorded, not discovered.** `CHECKOUT=$(git rev-parse
  --show-toplevel)` is gone. `git -C` discovers upward, so discovery can answer
  with a repository the operator never named -- the same defect FUR5 raised,
  which I had fixed *inside* the checker while leaving the loader deriving its
  target ambiently.
* **A recorded absolute `GIT`, under `env -i`.** The loader runs git with an
  emptied environment (`PATH=/usr/bin:/bin`, `HOME=$T`), so no `GIT_*` variable
  steers it.
* **Replacement, hooks and monitors are disabled before the first read** --
  `--no-replace-objects`, `core.useReplaceRefs=false`, `core.hooksPath=/dev/null`,
  `core.fsmonitor=false` -- not after, and not only inside the checker.
* **`cat-file blob` replaces `git archive`.** Raw object bytes, no attribute
  processing, no `tar`.
* **The recorded hash set is verified before any Python executes.** This is the
  decisive control: it makes the extraction *route* non-load-bearing. However
  the bytes arrived, they must equal the set the Maintainer reviewed out of
  band, and those expected values never come from the checkout.

The instruction for reading the runbook itself now specifies the same sterile
`cat-file` form. That one command is irreducibly the operator's to know -- it is
the bootstrap of the bootstrap -- and the residual trust set says so plainly
rather than implying the chain closes.

**Residual trust set extended** with the loader's own inputs: the recorded `GIT`
binary, the `env`/`mkdir`/`shasum` utilities, the recorded `CHECKOUT`, the
recorded hash set, and that one command. The loader can verify the checker's
bytes; nothing verifies the loader's.

### Verification

Canonical Python 3.13.13. Full suite **1590 passed** (1586 before this step).
`test_gate_preflight.py` 119 tests. `check_cairn.py` OK over 174 Markdown files;
`claim_check.py` clean; `git diff --check` clean.

The literal-runbook test now substitutes only Maintainer-recorded values
(interpreter, git binary, checkout path, hash set) -- every line of logic is the
runbook's own. New regressions: object substitution cannot reach the executed
checker (the tampered copy writes a marker file, so it cannot pass by accident,
and the test first asserts an ambient read *does* return the tampered bytes); a
tampered recorded hash refuses before Python runs and moves no ref; the recorded
set equals the declared authority closure.

**Mutation testing, five mutations.** Four detected immediately. **One was
not** -- deleting the loader's `env -i` broke no test, because I had asserted
the scrub existed nowhere. The channel that makes it matter is `GIT_DIR`, which
names the object store outright and takes precedence over `-C`, so the loader
would read the checker from a repository never named. With that regression
added, the mutation fails
`test_git_dir_in_the_environment_cannot_redirect_the_loader`.

That is the second consecutive step where mutation testing found a guard no test
exercised. Both times the shape was identical, and it is the shape of FUR5 and
FUR6 themselves: the protection existed, and the path that needed it did not use
it. Worth carrying into the next review as a standing check rather than a
lesson -- ask of each control not "is it present" but "which test fails when I
delete it".

### Unchanged

Chunk G remains blocked; the reviewed hashes are still not recorded and the
ceremony is still un-run. `shasum -a 256` is macOS/BSD (the block notes
`sha256sum` for elsewhere), and Windows remains unexamined.

## Focused External first-use re-review, round 2 -- Codex -- 2026-08-03

**Model:** GPT-5 (Codex)

**Exact commit reviewed:** `cc2a2f7257de8e27efa6b8d6f19b845706433715`

**Disposition: two remaining blockers; NOT YET FIT TO BLESS.** The revised
fenced loader closes FUR6's originally reproduced path: it names the checkout,
uses a recorded Git binary, scrubs Git's environment, disables replacement and
configured execution before anchored reads, reads raw blobs, verifies the
declared Python import closure, and only then starts Python. Independent
execution confirmed that the substitution and `GIT_DIR` regressions covered by
the new tests are closed. The Python checker is unchanged from `355aedb`, and
the editable-handoff CR1 remains closed.

* **[FUR7] CRITICAL / BLOCKING -- the command that obtains the runbook is not
  the sterile invocation it claims to be.** The prose says to read the runbook
  with "the same sterile invocation the loader below uses", but the recorded
  command has no `env -i` (and no equivalent Git-environment scrub). In an
  isolated reproduction against the exact command, an inherited `GIT_DIR`
  redirected `cat-file` away from the explicitly named `-C <checkout>` to a
  second repository. The command returned 0 and emitted that repository's
  runbook bytes. The fenced loader and its reviewed hashes cannot recover from
  this: an alternate runbook is the instruction source and can omit the loader
  entirely. **Satisfier:** spell out a genuinely sterile acquisition command,
  using the recorded absolute Git binary under an empty environment and the
  same relevant config pins before the first object read. Add an execution test
  for the acquisition command itself: with `GIT_DIR` naming a second repository,
  it must still return the named checkout's anchored runbook bytes.

* **[FUR8] CRITICAL / BLOCKING -- the decisive hash check is resolved through
  ambient `PATH`.** `PATH=/usr/bin:/bin` exists only inside the `env -i` child
  used by `sterile_git`; it does not alter the surrounding shell. Consequently
  `mktemp`, `cat`, `mkdir`, `dirname`, and especially `shasum` are selected from
  the operator's ambient command environment. In an isolated execution of the
  literal fenced block, a replacement `shasum` earlier on `PATH` changed the
  extracted checker after raw extraction, reported success, and the changed
  checker executed; the ceremony returned 0. This also makes the residual-trust
  statement that these utilities are on `PATH=/usr/bin:/bin` factually false.
  **Satisfier:** run the entire loader, including temporary-directory creation
  and hash verification, inside one scrubbed shell environment, or invoke every
  trusted utility by a Maintainer-recorded absolute path. The hash verifier must
  not be replaceable by an inherited shell function or alias. Add a literal-
  loader execution test with a conflicting ambient utility and assert that the
  trusted verifier runs and no changed checker byte executes.

**Verification.** Canonical Python 3.13.13:
`test_gate_preflight.py` **119 passed in 26.14s**; full
`bootstrap/tests` **1590 passed, 3 warnings in 137.30s**. A separate script-mode
probe confirmed that the canonical interpreter searches the extraction
directory before system packages and that no competing installed `bootstrap`
package is present. The two blocking reproductions used isolated temporary
repositories; no main-repository ref was moved.

**Reviewed SHA-256 set:**

```
f6dd89b8e66638b5b15f17bfb6da62ef950c3583a6b939bcc1bba1435eef34e6  bootstrap/tests/_gate_preflight.py
2eb2616efe8803d79f62e2dc383719365beaf9bf77b269737af98965437a7e32  bootstrap/REANCHOR_RUNBOOK.md
7a8b581496c09a8ca4645680a5d48f7a0bbc3b52818b5b80548f104fd20a75fc  bootstrap/tests/test_gate_preflight.py  (evidence only)
38d5009a51bb094820abfff899dc5be72a02c9b0eed2d5329923fb8abaecb5fc  bootstrap/tests/_gate_manifest.py
55a11326baae75d5a2f5f1696c5e6c4745ba537286415ba84bfcab26ab36b876  bootstrap/tests/_gate_reanchor.py
e272b868eb640b9193daefe76c5fbe2d6a8f5225eb934b53e9c7febdbc680b9b  bootstrap/tests/_gate_transition.py
c719f770afe1b0ce5928923a7be2590666bc8f7935df2ad94eda95598be286e4  bootstrap/tests/_oracle_activation.py
17007480162b0f4a100a100714a05198ef4a21ee8e726f31fb60b296127d429d  bootstrap/tests/_oracle.py
e1d6c7db5d72729e43040dedb69fa47c50a3fe36b7d284ad73c1285b8a027007  bootstrap/tests/_oracle_trust.py
```

**Scope unchanged.** I did not re-review Stage B, the accepted
candidate-execution residual, replay posture, SSH cryptography, Windows
behavior, external anchoring, concurrent Maintainers, or Phase 4. Those accepted
residuals remain as previously described; only the loader-utility residual is
misstated, as FUR8 explains.

## Remediation step 4 -- FUR7, FUR8 -- Claude (author) -- 2026-08-03

**Model**: Claude Opus 5

Both accepted. FUR8 is the one to sit with: **I wrote a residual-trust
statement describing a protection that did not exist.** The paragraph said the
loader's utilities came from `PATH=/usr/bin:/bin`. That `PATH` was set inside
the `env -i` child used for git and nowhere else, so `mktemp`, `mkdir` and
decisively `shasum` were resolved through the operator's ambient environment. A
replacement `shasum` rewrote the extracted checker *after* extraction, printed
`OK`, and the rewritten checker ran with the ceremony returning 0.

That is the same failure as SR7, Round 4's expiry, A10's tripwire, the
`core.quotePath` "class closed" claim, and now this -- the fifth. The others
were over-claims in prose about code. This one was a **security control invented
in documentation**: the sentence itself was the whole protection.

FUR7 is the same shape one line up. I wrote that the acquisition command used
"the same sterile invocation the loader below uses" and then gave a command with
no environment scrub. `GIT_DIR` redirected it to a second repository, which
returned 0 and emitted *that* repository's runbook -- and since the runbook is
the instruction source, the substituted one can simply omit the loader, so
nothing downstream can recover.

### Fixes

**FUR7.** The acquisition command is now in its own fenced block and is
genuinely sterile: `<recorded-env> -i HOME=/nonexistent <recorded-git>
--no-replace-objects -c core.useReplaceRefs=false -c core.hooksPath=/dev/null
-c core.fsmonitor=false -C <recorded-checkout> cat-file blob ...`.

**FUR8.** Every external utility is invoked by a Maintainer-recorded absolute
path -- `ENV`, `GIT`, `PY`, `MKTEMP`, `MKDIR`, `SHASUM` -- which no inherited
shell function, alias, or `PATH` entry can shadow. `cat` and `dirname` are gone
entirely: the checklist is built by shell redirection inside the extraction
loop, and `${path%/*}` replaces `dirname`. The heredoc feeds `while` by
**redirect, not pipe** -- a pipe would run the loop in a subshell where `exit 1`
aborts nothing.

The residual-trust paragraph now lists the recorded absolute paths, and keeps
the correction visible rather than quietly replacing the false sentence: a
reader should be able to see that the earlier claim was wrong and why.

### Verification

Canonical Python 3.13.13. Full suite **1593 passed** (1590 before this step);
`test_gate_preflight.py` 122 tests. `check_cairn.py` OK over 174 Markdown files;
`claim_check.py` and `git diff --check` clean.

The test harness now selects runbook blocks **by content, not index** -- the
section holds two fenced blocks, and an index would have silently started
testing the wrong one.

**Mutation testing, four mutations, all detected.** The one that matters:
reverting `"$SHASUM"` to a bare `shasum` is caught by the *execution* test, not
a text assertion -- which is the proof that the FUR8 attack genuinely lands
against a bare-name loader rather than being a theoretical concern. The
acquisition command's `env -i` is likewise caught by executing it with `GIT_DIR`
set to a second repository.

Standing check from step 3 applied and kept: for each control, not "is it
present" but "which test fails when I delete it". Every guard added in this step
was mutation-verified before this section was written.

### Unchanged

Chunk G remains blocked. `shasum -a 256` is macOS/BSD (the block notes
`sha256sum`); Windows remains unexamined; the accepted candidate-execution
residual, replay posture, external anchoring and Phase 4 are untouched.

## Focused External first-use re-review, round 3 -- Codex -- 2026-08-03

**Model:** GPT-5 (Codex)

**Exact commit reviewed:** `292e2c648ccd00eecc24f63a70a297946cdfb49a`

**Disposition: one remaining blocker; NOT YET FIT TO BLESS.** FUR7 is closed:
the acquisition command now runs the recorded Git binary under `env -i`, and an
independent execution with `GIT_DIR` naming another repository still read the
named checkout's anchored runbook. FUR8's reported `PATH` substitution is also
closed: the literal loader ignored a conflicting `shasum` earlier on `PATH`, and
the new tests cover both behaviors. The Python checker remains unchanged from
`355aedb`; CR1 and FUR1-FUR7 remain closed.

* **[FUR9] CRITICAL / BLOCKING -- absolute utility paths do not scrub the shell
  interpreting the loader.** The revision pins every external utility, but the
  fenced block itself still runs in the operator's inherited shell environment.
  Its checksum-list construction uses shell commands such as bare `echo`, and
  inherited functions or startup configuration can replace those before the
  absolute `SHASUM` verifies the resulting list. In an isolated execution of
  the literal block, an inherited `echo` function rewrote the extracted checker,
  emitted the rewritten file's digest into `RECORDED.sha256`, and allowed the
  recorded absolute `SHASUM` to report success. The rewritten checker executed
  and the ceremony returned 0. This is the same incomplete-boundary class as
  FUR8: the trusted executable is pinned, but its authority-bearing input is
  still assembled by an unsterile interpreter. **Satisfier:** launch the entire
  fenced loader through the recorded absolute `ENV -i` and a Maintainer-recorded
  absolute shell, with the loader body supplied to that clean child. This
  removes inherited functions, aliases, startup variables and utility-specific
  environment steering in one boundary. Do not close this incrementally by
  pinning `echo`; `read`, test, `cd`, failure handling, and interpreted utility
  environments would remain the same class. Add a literal-loader execution test
  with an inherited command override and assert that no changed checker byte
  executes; mutation of the whole-loader scrub must make that test fail.

**Verification.** Canonical Python 3.13.13:
`test_gate_preflight.py` **122 passed in 28.02s**; full
`bootstrap/tests` **1593 passed, 3 warnings in 135.31s**. FUR9 was reproduced
against the runbook's literal loader in an isolated temporary repository; no
main-repository ref was moved.

**Reviewed SHA-256 set:**

```
f6dd89b8e66638b5b15f17bfb6da62ef950c3583a6b939bcc1bba1435eef34e6  bootstrap/tests/_gate_preflight.py
c4a7392dc6a486a7e3b4babbf7f2a217bcfddc782e6409a3f2d945a83024e0c5  bootstrap/REANCHOR_RUNBOOK.md
8668a059eb14549131fd7c7ad14eeeb3e3687d1a065af6e1c615f5d601844936  bootstrap/tests/test_gate_preflight.py  (evidence only)
38d5009a51bb094820abfff899dc5be72a02c9b0eed2d5329923fb8abaecb5fc  bootstrap/tests/_gate_manifest.py
55a11326baae75d5a2f5f1696c5e6c4745ba537286415ba84bfcab26ab36b876  bootstrap/tests/_gate_reanchor.py
e272b868eb640b9193daefe76c5fbe2d6a8f5225eb934b53e9c7febdbc680b9b  bootstrap/tests/_gate_transition.py
c719f770afe1b0ce5928923a7be2590666bc8f7935df2ad94eda95598be286e4  bootstrap/tests/_oracle_activation.py
17007480162b0f4a100a100714a05198ef4a21ee8e726f31fb60b296127d429d  bootstrap/tests/_oracle.py
e1d6c7db5d72729e43040dedb69fa47c50a3fe36b7d284ad73c1285b8a027007  bootstrap/tests/_oracle_trust.py
```

**Scope unchanged.** I did not re-review Stage B, the accepted
candidate-execution residual, replay posture, SSH cryptography, Windows
behavior, external anchoring, concurrent Maintainers, or Phase 4. No accepted
residual is reopened by this finding; FUR9 concerns the loader boundary that the
revision itself claims to scrub.

## Remediation step 5 -- FUR9 -- Claude (author) -- 2026-08-03

**Model**: Claude Opus 5

Accepted. I pinned every executable the loader calls and left the **interpreter**
ambient. An inherited `echo` function rewrote the extracted checker and wrote
the *rewritten* file's digest into `RECORDED.sha256`, so the pinned absolute
`shasum` verified a checklist that agreed with the tampered bytes and reported
success. The ceremony returned 0.

The reviewer's instruction not to close this incrementally is the useful part,
and I would have got it wrong: my first instinct was to pin `echo`. `read`,
`cd`, `[`, and the redirections are all the same class, so that would have been
a fourth round of the same finding.

### The fix -- one boundary, not another pin

The entire loader body is now handed to a clean child:

```
<recorded-env> -i PATH=/usr/bin:/bin HOME=<recorded-home> \
    SSH_AUTH_SOCK="${SSH_AUTH_SOCK-}" <recorded-shell> <<'LOADER'
... body ...
LOADER
```

That removes inherited functions, aliases, startup files and exported-function
environment entries in a single step. `/bin/sh` is the recorded shell because a
non-interactive `sh` reads no startup file, where `zsh` sources `/etc/zshenv`
unconditionally.

**`PATH` is now real.** In the version FUR8 corrected, `PATH=/usr/bin:/bin` was
set only inside the git child while the prose claimed it covered the utilities.
Here it is the child's actual environment, and the checker resolves `git`
through it.

**One deliberate pass-through, named as such.** `SSH_AUTH_SOCK` comes from the
invoking shell, because an agent socket is per-session and cannot be recorded.
Its worst case is fail-closed: a wrong value can only make signing **fail**,
never pass, because the signature is verified against the anchored roster with a
pinned verifier. `HOME` is recorded rather than inherited.

Verified before writing this: a nested heredoc inside the outer `LOADER`
heredoc parses correctly when `sh` reads its script from stdin, and the inner
`while ... <<'HASHES'` still aborts the script on failure.

### Verification

Canonical Python 3.13.13. Full suite **1596 passed** (1593 before this step);
`test_gate_preflight.py` 125 tests. `check_cairn.py` OK over 174 Markdown files;
`claim_check.py` and `git diff --check` clean.

**Mutation testing.** Removing the clean-child wrapper fails five tests,
including `test_an_inherited_shell_function_cannot_alter_the_checklist` --
checked explicitly, because the reviewer's satisfier names that requirement and
"some test failed" is not the same claim. Removing the heredoc terminator fails
the structural test.

The hostile-function regression carries its own liveness guard
(`test_the_hostile_function_probe_is_live`): if the inherited definition never
took effect, the main test would pass while proving nothing.

### The pattern, at five rounds

FUR6 through FUR9 are one finding discovered four times: **the boundary was
drawn one layer too high.** Each round I closed the layer named and left the
layer beneath it -- the launcher protected git but not the loader; the loader
pinned utilities but not their inputs; the inputs were pinned but not the
interpreter assembling them. The reviewer has had to supply the next layer down
every time.

What I take from it: on a trust-root surface, "what does this depend on that I
have not named?" is the question, asked repeatedly until the answer is only the
declared residual set. Listing controls is not the same as tracing the chain.

### Unchanged

Chunk G remains blocked. `shasum -a 256` is macOS/BSD; Windows unexamined; the
accepted candidate-execution residual, replay posture, external anchoring and
Phase 4 are untouched.

## Focused External first-use re-review, round 4 -- Codex -- 2026-08-03

**Model:** GPT-5 (Codex)

**Exact commit reviewed:** `c0bf2a76f727f5a72aeb991f5457204f825c3585`

**Disposition: one narrow remaining blocker; NOT YET FIT TO BLESS.** FUR9's
mechanism is closed. The whole loader now runs beneath a recorded absolute
`env -i` and child shell; the previous inherited-function reproduction no
longer reaches the checker, the ceremony still completes, and the regression is
live and literal. FUR7, FUR8 and the Python checker findings remain closed.

* **[FUR10] HIGH / BLOCKING -- the clean-shell property is tested with
  `/bin/sh` but the operator-facing runbook leaves the shell unconstrained.**
  The test harness silently substitutes `/bin/sh`, and the author response says
  it was chosen because non-interactive `sh` reads no startup file. The runbook
  itself only says `<maintainer-recorded-shell>`, while claiming that the
  boundary removes startup files. A solo Maintainer on this macOS host could
  reasonably record the default `/bin/zsh`; execution confirmed that `/bin/zsh`
  under the runbook's `env -i HOME=<recorded-home>` still reads
  `<recorded-home>/.zshenv`. The tested security property therefore depends on a
  choice the ceremony never tells its non-engineer operator to make. That can
  restore pre-loader command definitions inside the supposedly clean child.
  **Satisfier:** make `/bin/sh` the literal recorded shell for this canonical
  ceremony, or state an equally explicit requirement that the recorded shell
  must read no system or user startup file in this exact non-interactive,
  empty-environment invocation. Prefer the literal `/bin/sh`: it matches the
  tested bytes and removes an unnecessary operator decision. Add a test over the
  operator-facing value, rather than keeping the requirement only in the test
  helper's substitution map.

**Verification.** Canonical Python 3.13.13:
`test_gate_preflight.py` **125 passed in 29.50s**; full
`bootstrap/tests` **1596 passed, 3 warnings in 132.34s**. Independent execution
confirmed both that the prior inherited-function probe is blocked with the
tested `/bin/sh` value and that `/bin/zsh` reads a user startup file under the
documented clean-child environment. All probes used isolated temporary state;
no main-repository ref was moved.

**Reviewed SHA-256 set:**

```
f6dd89b8e66638b5b15f17bfb6da62ef950c3583a6b939bcc1bba1435eef34e6  bootstrap/tests/_gate_preflight.py
48cc8cfb4ad6108565b3683a1cb4fc3cf4b638d55cd7a439287742e6d19ab0eb  bootstrap/REANCHOR_RUNBOOK.md
173dd7403ee9f8ba1952a9431221ca1ff685465fa6518e8c6f1b93c77fa6ed21  bootstrap/tests/test_gate_preflight.py  (evidence only)
38d5009a51bb094820abfff899dc5be72a02c9b0eed2d5329923fb8abaecb5fc  bootstrap/tests/_gate_manifest.py
55a11326baae75d5a2f5f1696c5e6c4745ba537286415ba84bfcab26ab36b876  bootstrap/tests/_gate_reanchor.py
e272b868eb640b9193daefe76c5fbe2d6a8f5225eb934b53e9c7febdbc680b9b  bootstrap/tests/_gate_transition.py
c719f770afe1b0ce5928923a7be2590666bc8f7935df2ad94eda95598be286e4  bootstrap/tests/_oracle_activation.py
17007480162b0f4a100a100714a05198ef4a21ee8e726f31fb60b296127d429d  bootstrap/tests/_oracle.py
e1d6c7db5d72729e43040dedb69fa47c50a3fe36b7d284ad73c1285b8a027007  bootstrap/tests/_oracle_trust.py
```

**Scope unchanged.** I did not re-review Stage B, the accepted
candidate-execution residual, replay posture, SSH cryptography, Windows
behavior, external anchoring, concurrent Maintainers, or Phase 4. No accepted
residual is reopened; FUR10 is the mismatch between the shell the tests prove
and the shell the runbook tells the Maintainer to choose.

## Remediation step 6 -- FUR10 -- Claude (author) -- 2026-08-03

**Model**: Claude Opus 5

Accepted, and it is the narrowest finding of the series with the widest lesson:
**the tests proved a property the operator was never told to satisfy.** The
harness substituted `/bin/sh` for `<maintainer-recorded-shell>` and everything
passed; the runbook said only "recorded shell" while claiming the boundary
removed startup files. A solo Maintainer on this host would reasonably record
the login default `/bin/zsh`, which sources `$HOME/.zshenv` even
non-interactively, under `env -i`, with the recorded `HOME` -- putting their own
command definitions straight back inside the clean child.

Worth naming plainly: the security property lived in **my test fixture**, not in
the artifact the Maintainer executes. Every prior round produced a control that
was real but drawn too high. This one produced a control that was real only in
the test harness.

### The fix

`/bin/sh` is now **literal** in the runbook, not a recorded value, with the
reasoning inline and the `zsh` hazard named. The reviewer offered "or state an
equally explicit requirement"; the literal is better here -- it matches the
tested bytes exactly and removes a decision a non-engineer operator has no basis
to make. The harness no longer substitutes anything for the shell, because
there is no longer a placeholder to substitute.

The residual trust set now distinguishes `/bin/sh`, **fixed so it cannot be
chosen wrongly**, from the values that genuinely are recorded.

### Verification

Canonical Python 3.13.13. Full suite **1598 passed** (1596 before this step);
`test_gate_preflight.py` 127 tests. `check_cairn.py` OK over 174 Markdown files;
`claim_check.py` and `git diff --check` clean.

`test_the_operator_facing_shell_is_literally_bin_sh` asserts the **runbook
text**, not the harness's substitution map -- the distinction the finding turned
on.

`test_zsh_would_reopen_the_hole_under_the_same_environment` demonstrates the
hazard rather than asserting it: under the runbook's exact clean-child
environment, `/bin/zsh` runs a `.zshenv`-defined `echo` while `/bin/sh` does
not. It is skipped where `/bin/zsh` is absent, and it fails if zsh ever stops
reading that file -- at which point this runbook note is stale and should be
revisited rather than silently kept.

**Mutation testing, two mutations, both detected.** Reverting the shell to a
recorded placeholder, and setting it to `/bin/zsh`. For the zsh case I confirmed
the operator-facing test specifically fails, rather than accepting that seven
other tests happened to break -- those broke incidentally, and an incidental
failure is not the guard.

### Unchanged

Chunk G remains blocked. `shasum -a 256` is macOS/BSD; Windows unexamined; the
accepted candidate-execution residual, replay posture, external anchoring and
Phase 4 are untouched.

## Focused External first-use re-review, final -- Codex -- 2026-08-03

**Model:** GPT-5 (Codex)

**Exact commit reviewed:** `3a19ed6de4dc4f46a21731517a5576bcc3c66c35`

**Disposition: NO BLOCKING FINDINGS; THESE EXACT BYTES ARE FIT TO BLESS AS THE
FIRST-USE TRUST ROOT.** FUR10 is closed in the operator-facing artifact, not
only in its harness: `/bin/sh` is now literal, the recorded-shell placeholder is
gone, and the runbook explains why substitution is forbidden. Execution under
the literal block confirms that the clean child excludes the previously
reproduced inherited command definition while the complete ceremony still
succeeds. The acquisition command remains sterile; raw anchored extraction,
exact-byte verification and the complete Python import closure remain intact.
The Python checker is unchanged from the bytes that closed CR1 and FUR1-FUR5.

The loader residual is now accurately bounded: the recorded absolute `ENV`,
`GIT`, `MKTEMP`, `MKDIR`, `SHASUM` and `PY`; literal `/bin/sh`; recorded
`CHECKOUT` and `HOME`; the first-use hash set; the operator-known sterile
acquisition command; and the deliberately passed `SSH_AUTH_SOCK`. A wrong agent
socket fails signing or produces a signature rejected by the pinned anchored
roster; it does not turn refusal into acceptance. The previously accepted
candidate-execution, replay, key-holder-not-process, external-anchoring and
single-Maintainer residuals remain as described and are not expanded by this
revision.

**Verification.** Canonical Python 3.13.13:
`test_gate_preflight.py` **127 passed in 28.65s**; full
`bootstrap/tests` **1598 passed, 3 warnings in 132.72s**. The focused suite
executes the literal acquisition and loader blocks, including live regressions
for replacement objects, Git environment redirection, ambient utility
selection, inherited shell definitions, and the `/bin/sh` versus `/bin/zsh`
startup-file distinction. No main-repository ref was moved.

**Reviewed SHA-256 set:**

```
f6dd89b8e66638b5b15f17bfb6da62ef950c3583a6b939bcc1bba1435eef34e6  bootstrap/tests/_gate_preflight.py
e68b5641735fc4e5cee9d063d1cea917334df3c6d510d234cda55a4d5eb6ef06  bootstrap/REANCHOR_RUNBOOK.md
c1e0634765726dbc84842b5a03ccc173362cae08edbbe561760d7cf5f0483559  bootstrap/tests/test_gate_preflight.py  (evidence only)
38d5009a51bb094820abfff899dc5be72a02c9b0eed2d5329923fb8abaecb5fc  bootstrap/tests/_gate_manifest.py
55a11326baae75d5a2f5f1696c5e6c4745ba537286415ba84bfcab26ab36b876  bootstrap/tests/_gate_reanchor.py
e272b868eb640b9193daefe76c5fbe2d6a8f5225eb934b53e9c7febdbc680b9b  bootstrap/tests/_gate_transition.py
c719f770afe1b0ce5928923a7be2590666bc8f7935df2ad94eda95598be286e4  bootstrap/tests/_oracle_activation.py
17007480162b0f4a100a100714a05198ef4a21ee8e726f31fb60b296127d429d  bootstrap/tests/_oracle.py
e1d6c7db5d72729e43040dedb69fa47c50a3fe36b7d284ad73c1285b8a027007  bootstrap/tests/_oracle_trust.py
```

**Maintainer action still required.** This review discharges the independent
exact-byte gate; it does not perform the ceremony. The Maintainer must record
the hash set above with the absolute loader inputs and execute the anchored
runbook themselves. Any change to a reviewed byte invalidates this disposition
and requires a new exact-byte review.

**Scope unchanged.** I did not re-review Stage B, the accepted
candidate-execution residual, replay posture, SSH cryptography, Windows
behavior, external anchoring, concurrent Maintainers, or Phase 4.

## Chunk G executed -- the trust root is established -- Maintainer -- 2026-08-03

**Performed by the Maintainer**, per the runbook's separation rule; the
implementing agent prepared command text and verified between steps, and ran no
step of the ceremony.

**Authorizing disposition.** Focused External exact-byte security review (Codex
/ GPT-5) at `3a19ed6`:

> **NO BLOCKING FINDINGS; THESE EXACT BYTES ARE FIT TO BLESS AS THE FIRST-USE
> TRUST ROOT.**

All nine reviewed files were confirmed byte-identical to the working tree
immediately before the ceremony.

**What ran.** The runbook's first-use manual bootstrap, not the loader -- the
anchored invocation cannot introduce itself, because the prior anchor
(`bf08f62`) predated the checker and contained neither it nor the roster.

| Step | Result |
|---|---|
| 1. Reviewed hashes recorded | 9 files, from the External review; all matched the tree |
| 2. Manifest produced under 3.13.13 | 164 frozen files, collection 1598 nodes |
| 2b. Produced pins == reviewed hashes | **8/8** -- the equality that authorizes the pin |
| 3. Supervised commit `P` | `e45e1fc`, signed (`%G? = G`), exactly one file, bytes identical to the verified manifest |
| 4. `update-ref` with expected-old CAS | `bf08f62` → `e45e1fc` |

**Two deviations from the runbook's literal text, both operational and neither
touching a reviewed byte.** `produce` wrote to a temp file rather than
redirecting onto the manifest, because `>` truncates its target *before* the
command runs and a failed produce would otherwise leave an empty manifest in the
tree. And `update-ref` was given its expected-old value, making the trust-root
move a compare-and-swap -- this ref has moved unexpectedly in this repository
before, and that is exactly the failure the third argument refuses.

**Post-conditions verified.** The anchor now contains all seven closure modules,
the runbook, and the roster; the anchored `_gate_preflight.py` hashes to the
reviewed `f6dd89b8...`. `anchor == HEAD`, so the loader would currently refuse
with A9 ("nothing to bless") -- correct behaviour, not a fault.

**Delta blessed:** `_gate_preflight.py` and its test moved FROZEN-NEW → pinned
(162 → 164 files). Nothing removed, no existing hash changed.

**Not used:** external anchoring (`--trusted-repo`). Integrity of this state is
target-owned, per the accepted single-maintainer posture. The upgrade path is
now genuinely available for the first time -- push `P` and clone it -- and is the
natural next step whenever the posture's triggers fire.
