<!-- cairn-internal-ref-allow: doctrine/plans.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- Forward-reference paths this plan creates; they materialize in Chunks A/E. -->
<!-- `dev/.cairn/allowed_signers` needed a file-scoped exemption while it was a
     forward reference; the Maintainer ran M1-M5 on 2026-08-03 and the path now
     resolves, so the exemption is dropped per the marker discipline (drop it
     once the path lands) rather than left to rot. -->
<!-- claim-check-allow: bootstrap/tests/_gate_preflight.py, bootstrap/tests/test_gate_preflight.py -->

# Plan: a reviewed pre-flight for the supervised gate re-anchor (Phase 0)

**Source proposal**: `dev/proposals/archive/2026-08-03-claude-gate-reanchor-preflight.md`
**Status**: executing
**Plan review**: required(**External**, security lens) — carried from the proposal header and ratified at Decision. Additionally, **first use is gated on a focused External security review of the exact initial checker bytes and the recorded invocation** (SR6 / SR9); the Decision explicitly does *not* prospectively bless those bytes.
**Last update**: 2026-08-03 (Chunk A landed)
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

*Filled in after implementation commits land (Chunks A-F, H).*

## Lasting-truth migration

*Filled in at archive time. Per the archive-preconditions rule, this plan
archives only once every deferred follow-up has a durable home outside it — the
SR7 containment upgrade, the SR10 nonce/ledger, and the external-anchoring
upgrade are all named in the Decision and belong on `dev/PLANNING.md` before
archive if not already homed.*

This section is append-only once written.
