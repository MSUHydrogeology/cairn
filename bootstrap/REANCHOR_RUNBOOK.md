<!-- `dev/.cairn/trusted-activation.yml` and `dev/.cairn/promotion-authorization.yml`
     are Maintainer-supplied trust-root configs, absent unless the supervised
     re-anchor flow creates them.  Their claim-check exemption moved to
     dev/.cairn/claim-check-allow.json on 2026-08-27; this note names them so a
     reader still learns why the paths do not resolve. -->

# Supervised re-anchor runbook (differential-oracle gate)

> **Maintainer-only, supervised.** This runbook is how the **trust root** for the
> two-stage re-anchor (`bootstrap/tests/_gate_reanchor.py`) is established and how
> the supervised promotion is run. The *code* is reviewed and tested; **running
> the steps below is the Maintainer's act** — an implementing agent must not
> perform Phase 0, Phase 4 or Phase 5 (that is the forbidden "implementer
> blesses its own verifier" self-authorization; Phase 5 is additionally the
> standing rule that pushing is always the Maintainer's).

The re-anchor is **two-stage** (round-4 contract): Stage A gathers executable but
non-authoritative *evidence*; Stage B is data-only and *authoritative*. Stage B
resolves authority from fixed refs, pins the **executing verifier code** against
the prior gate state `P`, constructs `N = C + the reviewed gate manifest`, and
advances the one designated ref `P → N` by an expected-old compare-and-swap.

Because Stage B pins the executing verifier code against `P`'s frozen gate
manifest, the **current** `P` must already pin those verifier modules. The
existing anchored manifests do **not** (the Stage-B modules were introduced later
and read as `FROZEN-NEW`). Establishing a `P` that pins them is itself a
trust-root transition — so it is done **once, supervised**, never
silently by the promotion command (round-6 Finding 1).

---

## Before you start — what you need, and what performs each step

**One command performs the ceremony.** The stages below are no longer typed out
of this document: the procedure is `bootstrap/reanchor.sh`, frozen into the
authority closure, started by a launcher an External Security review produced.
This document explains what each step establishes and why; it is not the thing
you copy.

### Prerequisites

Have all of these before you begin. Every one of them is a thing the ceremony
refuses without, and discovering that at stage 2 costs a full authorization
package.

| | what | where it comes from |
|---|---|---|
| 1 | **The instantiated launcher** | The External Security review that read it. Delivered with its SHA-256, which you verify against the review's record before running it. |
| 2 | **The authorization packet** | The same review, as a pair with the launcher. You do not verify it separately — its digest is bound into the launcher, so checking the launcher's digest covers both. |
| 3 | **Your values file** | You, once. Copy `bootstrap/reanchor-values.example`, fill it in outside the repository, and keep it. See the refresh note below. |
| 4 | **The ceremony key** | You. Dedicated, encrypted at rest, in no agent, used for nothing else — the **N4** precondition, and the one fence in this ceremony that no code can enforce. See `SECURITY.md` > *The ceremony key is dedicated*. |
| 5 | **The candidate ref** | The commit you are re-anchoring to. An argument to the launcher, never a value inside a reviewed artifact. |

**The values file goes stale, and that is not a malfunction.** It records
*resolved* executable paths, because a symlinked executable is a path whose
target can change between the check and the execution. On a Homebrew host the
resolved `git` is a version-pinned Cellar path, so **a toolchain upgrade breaks
it**. Re-run `validate` after upgrading git, python, or the coreutils:

```
sh <launcher> <packet> <values> <candidate-ref> --validate
```

The refusal you get from a stale path is correct. Fix the path; do not relax
the rule.

### The step registry is the authority on what happens

`sh bootstrap/reanchor.sh steps` prints the closed, ordered registry — every
step's stable ID, its stage, the command that performs it, and what it
establishes. **The IDs below are that registry's**, cited here so the two cannot
drift apart: a step in the code and not in this document, or the reverse, fails
a test.

What this buys is a drift signal on the procedure's *shape*. It attests nothing
about whether the prose around each citation is accurate — that is reviewed, not
machine-checked, and this sentence is here so the presence of a check is not
mistaken for the stronger claim.

### Where each thing comes from — the two questions this runbook used not to answer

**"Where does the review manifest come from?"** The launcher composes it.
It is not a file you write, and it is not a file the review hands
you: every value in it comes either from the packet (the review's own output) or
from the candidate OID the launcher resolved itself. Nothing in it is
read from the candidate. That is what removes the last point at which a human or
an agent had to assemble an authority input by hand.

**"How do I read the report?"** Run the launcher with `--show-report`:
`sh <launcher> <packet> <values> <candidate-ref> --show-report`.
The digest you confirm binds a *state*, and the report is that state.
A confirmed digest over an unread report authorizes something you have not seen,
so this step is not optional politeness — it is the only step at which you
exercise judgement rather than checking arithmetic.

### The ceremony, step by step

Each step below cites its registry ID once. Run
`sh bootstrap/reanchor.sh steps` for the registry itself.

**You run two commands.** The launcher, and then stage 2. Everything between
them is you looking at what you are about to authorize.

#### The one command that does the pre-candidate work

```
sh /path/to/reanchor-launcher.sh  <packet>  <values>  <candidate-ref>
```

Everything in this phase runs on **reviewed bytes** — the launcher the review
produced, the packet bound into it, and your own values file. No candidate byte
executes until the last step of it.

* **[RA-01]** Your values file is read by the launcher, and only by the
  launcher, under a closed grammar. The launcher needs `git`, `shasum` and `cat`
  before it can verify the artifact, so it cannot use candidate code to read the
  file; it checks every value and hands the artifact the checked values.
* **[RA-02]** The packet on disk is hashed and compared against the digest bound
  into the launcher. This is the comparison that makes the pair a pair.
* **[RA-03]** The packet is snapshotted into memory and **re-hashed**, and the
  two digests must agree. This catches a byte the shell could not carry, and a
  rewrite between the two reads. It **detects**; it does not prevent — see the
  residual below.
* **[RA-04]** The packet's member set is compared against the closure fixed
  *in the launcher*. Everything else validates the packet against itself; a
  packet that dropped a member parses cleanly and hashes correctly, and only
  this comparison catches it.
* **[RA-05]** The ceremony artifact is confirmed to be a closure member by
  construction: exactly one row names it, that row's digest is its digest, and
  the launcher will start no other file.
* **[RA-06]** The candidate ref is resolved **once**, to a full object id. A
  moving ref read twice is two different answers wearing one name.
* **[RA-07]** Every closure blob is read at that object id and checked against
  its reviewed digest. Not a sample — every one.
* **[RA-08]** The extracted ceremony artifact is hashed and checked again,
  separately.
* **[RA-09]** The review manifest is **composed** from the packet and the
  resolution the launcher just performed. Nothing in it is read from the
  candidate.
* **[RA-10]** **The first candidate byte runs.** The artifact starts, and it
  starts only because its digest matched.
* **[RA-11]** The complete effective configuration prints. This is your
  stop-point: everything that could refuse already has, so what you see is what
  will run. Read it before letting it continue.
* **[RA-12]** The key channel is probed. **If a passphrase prompt appears,
  decline it** — the prompt is the ceremony asking whether the key is reachable,
  and answering it makes the probe succeed, which is the failure case.
* **[RA-13]** The read-only checks run and the authorization package is written.
  No key is held and no ref moves.

#### Between the stages — the part that is yours

```
sh <launcher> <packet> <values> <candidate-ref> --show-report
sh <launcher> <packet> <values> <candidate-ref> --hash-package
```

* **[RA-14]** Read the report. The digest binds a state; this is the state.
* **[RA-15]** Compute the package digest yourself, over the bytes on disk. Never
  take a digest from inside the package — a file can assert anything about
  itself.
* **[RA-16]** **Now** make the ceremony key available, and not before. Until
  this moment the **N4** key-at-rest precondition holds and stage 1 proved it could not
  sign; loading it earlier collapses the boundary the two stages exist to
  create.

#### The command that signs

```
sh <launcher> <packet> <values> <candidate-ref> --stage2 <the digest you computed>
```

* **[RA-17]** The package is validated against **your** digest, and stage 2
  re-extracts and re-verifies its own bytes rather than reusing stage 1's. No
  candidate code runs in this stage at all.
* **[RA-18]** The checkpoint is signed and **branch and anchor move in one
  transaction**.
* **[RA-19]** Put the key away, then publish both refs in one atomic push.

#### What this does not close

**The two stages want opposite states**, and that is the boundary, not a
copying slip: stage 1 is invoked with no agent socket and refuses if the key can
sign anyway; stage 2 needs the socket, because without it the signer has no
controlling terminal and dies naming an `ssh-askpass` that does not exist on a
stock host. So the key goes in between the stages and comes out after.

**The packet is read twice** — once to hash, once to snapshot — so a writer
running as you can change it in between. Re-hashing the snapshot detects that.
It does not prevent it. That is the accepted same-user residual, unchanged.

**Sequencing is not containment.** Candidate code that ran in stage 1 shared the
machine with the key stage 2 loads. Splitting the processes removes the
simultaneity, not the residual.

---

## Phase 0 — establish the trust root (supervised, one-time)

The mechanism reuses the **existing gate-manifest prerequisite-commit flow**
(`bootstrap/tests/_gate_manifest.py`), the same machinery already used to pin
gate-control files for the six-proposal batch.

### Phase 0 pre-flight — `_gate_preflight.py`

**Step 1 — obtain this document from the anchor, sterilely.** The acquisition
command is *itself* a trust boundary, and a weaker one than it looks: an
alternate runbook is the instruction source, so it can simply omit the loader.
An earlier version of this section claimed to use "the same sterile invocation
the loader below uses" and did not — it had no environment scrub, and an
inherited `GIT_DIR` redirected `cat-file` away (**FUR7**) from the explicitly named `-C`
checkout to a second repository, returning 0 and emitting *that* repository's
runbook (FUR7, reproduced). The command below is the real thing:

```
<maintainer-recorded-env> -i HOME=/nonexistent \
    <maintainer-recorded-git> --no-replace-objects \
        -c core.useReplaceRefs=false \
        -c core.hooksPath=/dev/null \
        -c core.fsmonitor=false \
        -C <absolute-path-of-the-checkout-to-bless> \
        cat-file blob refs/cairn/gate-anchor:bootstrap/REANCHOR_RUNBOOK.md
```

This one command is irreducibly the operator's to know — it is the bootstrap of
the bootstrap — and it lives in the residual trust set.

**The launcher is its own trust boundary.** Everything it does runs *before* the
checker exists, so none of the checker's internal pinning protects it. It is
reviewed as its own unit, and the reason is a real failure: an earlier
arrangement obtained the checkout by ambient discovery and extracted with `git
archive`, and repository-local object substitution caused the literal block to
execute substituted checker bytes while returning success — the same
trust-source failure as the acquisition command's (**FUR1**), one step
earlier (**FUR6**).

### Why the launcher looks the way it does

Five properties, each of which was learned by a defect rather than designed in
advance. They are recorded here because the launcher is now a file rather than a
block you paste, and a reader who cannot see *why* a line is there will
eventually simplify it away.

* **Every utility is invoked by absolute recorded path.** An ambient `PATH` is
  what once let a replacement `shasum` vouch for bytes it had just rewritten
  (**FUR8**).
  Absolute paths are what no inherited shell function or alias can shadow.
* **An inherited shell function could rewrite what the loader verified**, so
  the whole thing runs in a clean child: an inherited `echo` once rewrote the
  extracted checker and wrote the rewritten file's digest into the checklist,
  so the pinned absolute `shasum` verified the wrong list and reported success
  (**FUR9**). Pinning `echo` would not have closed it either -- `read`, `cd`,
  `[` and the redirections are the same class.
* **The environment is emptied for every git read.** An inherited `GIT_DIR`
  redirected `cat-file` away from the explicitly named `-C` checkout to a second
  repository, returned 0, and emitted *that* repository's bytes.
* **Object replacement, hooks and monitors are disabled before the first read**,
  not after — a replacement ref configured in the candidate repository is read
  by the very command that would otherwise discover it.
* **`cat-file blob` reads raw object bytes; `git archive` is not used.** Archive
  is attribute-aware, so a candidate `.gitattributes` can reshape what lands.
* **The artifact is started by the literal `/bin/sh`.** Not a recorded value and
  not a preference: a non-interactive `/bin/sh` reads no startup file, which is
  the entire reason the child is clean. The obvious alternative on this host is
  the login default `/bin/zsh` (**FUR10**), and `zsh` sources `$HOME/.zshenv` even
  non-interactively — which puts the operator's own command definitions straight
  back inside the supposedly clean child. An earlier version left this as a
  recorded choice while claiming the boundary removed startup files.

**One launcher, two modes, and the mode is measured.** The procedure used to
carry two near-identical loaders — steady state and transition — and an
instruction to "replace the final command" of one to get the other. That
instruction produced a live failure: the edited block still extracted from
`refs/cairn/gate-anchor`, so stage 1 ran the candidate's checker and stage 2 ran
the old one — the old authority vouching for its own replacement, after the key
was loaded. There is now **one** launcher, and it decides by comparing every
closure member at the anchor against the resolved candidate. There is no second
block to edit and no instruction to mis-follow.

### The launcher, reproduced — **NOT the authority source**

> **Do not copy this.** It is here so you can read what you are about to run.
> The launcher you actually run is the one the External Security review
> produced and delivered, with its SHA-256 recorded in that
> review — and its bytes differ from these by exactly one filled slot. Verify
> the digest of *that* file against *that* record. A launcher assembled from
> this document is a launcher nobody reviewed.
>
> The reviewed source lives at
> [`bootstrap/reanchor-launcher.template.sh`](reanchor-launcher.template.sh),
> and a test asserts that this section and that file do not drift apart.

The shape of it, in the order it runs:

| | what it does | why it is *there* and not later |
|---|---|---|
| 1 | reads your values file with its **only** parser | it needs `git`, `shasum` and `cat` before it can verify the artifact, so it reads the file itself and hands the artifact the checked values |
| 2 | hashes the packet, compares against the digest **bound into itself** | this is the comparison that makes the launcher and the packet a pair |
| 3 | snapshots the packet and **re-hashes the snapshot** | detects a byte the shell could not carry, and a rewrite between the two reads |
| 4 | compares the packet's member set against its **own fixed list** | everything else validates the packet against itself; only a fixed list catches a packet that dropped a member |
| 5 | resolves the candidate **once** | a moving ref read twice is two different answers wearing one name |
| 6 | verifies **every** closure blob at that OID | not a sample |
| 7 | composes the review manifest | so that nobody hands the ceremony an authority input |
| 8 | **starts the artifact** | the first candidate byte, and only because its digest matched |

**Stage 2 runs through the launcher too**, with `--stage2 <digest>`, and that is
a security property rather than a convenience: it repeats the whole verification
into a *fresh* directory. Candidate code ran in stage 1, as the same user, while
stage 1's directory sat on disk — so reusing it would hand the signing stage
bytes the candidate had a window to rewrite, after the key was loaded.

### Phase 0 transition mode — measured, never chosen

A **transition** is a ceremony that carries a change to the authority closure
itself: the checker, the roster, the runbook, the ceremony artifact. A
**steady-state** re-anchor carries none.

**You do not select between them, and there is no flag.** The launcher compares
every closure member at the anchor against the resolved candidate, and a single
difference makes it a transition. That is deliberate: an operator who picks the
mode can pick wrong in the unsafe direction, and declaring "steady state" over a
real closure change is precisely the substitution the reviewed-transition path
exists to prevent.

**What a transition additionally requires** is a reviewed member set — which is
what the authorization packet is. The launcher composes the review manifest from
it and hands both the manifest and the resolved OID to the stage commands; in
steady state it passes neither, because there is nothing to carry.

**If the checker refuses saying the closure is identical**, this ceremony is not
a transition and does not need one. Re-run without expecting a closure change:
the launcher will detect steady state by itself.

This section used to hold a second loader block for the transition case,
alongside an instruction to "replace the final command" of the steady-state one.
That instruction produced a live failure — the edited block still extracted from
`refs/cairn/gate-anchor`, so stage 1 ran the candidate's checker and stage 2 ran
the old one. One launcher removes the class.

### The dated posture, and what ends it

The trusted-contributor threat model is scoped to **Cairn's own trust root,
single-maintainer, as of 2026-08-03** — not a standing assumption. One trigger is
mechanical: `apply` refuses to construct a checkpoint unless the commit it builds
verifies against the **anchored** roster (`dev/.cairn/allowed_signers`) under a
pinned verifier.

**This used to say something stronger, and the weaker statement is the accurate
one.** The earlier text claimed `apply` refuses if any commit at or after a
*signing epoch* is unsigned or signed by an unpinned key. That per-commit range
check was retired (plan `git-native-security-foundations`, Chunk B): the epoch
constant lived in the checker's own bytes inside the tree being blessed, so a
candidate could move it to grandfather its own commits, and it refused the
ordinary unsigned-agent-commit workflow, which meant operators disabled it.
Authorization is now the Maintainer's signature on a checkpoint binding the
range-report digest. Signature counts over the range survive as **diagnostics**
in the report and in `check`'s output — never as a verdict.

**Two triggers are not mechanical, and live here because nothing can observe
them:**

1. **The ceremony is run on a checkout the Maintainer does not solely control.**
2. **An adopter takes this mechanism** (it is Cairn-internal today; nothing under
   `bootstrap/tests/` is installed).

On either, revisit the posture before blessing. The named upgrade paths are OS
containment for the evidence stage, external anchoring via `_gate_manifest.py
verify --trusted-repo` (already supported, merely unused here), and a single-use
nonce for replay.

**First use is different.** The invocation above executes the checker *from the
anchor*, so it cannot be used until the checker is in the anchor. Introducing it
is a one-time manual bootstrap under the steps below, gated on a focused External
security review of the exact checker bytes and this invocation text, with the
reviewed hashes recorded by the Maintainer alongside who compared them and at
which commit.

1. **Review the exact verifier bytes and compute their hashes yourself** (`shasum -a 256`,
   independently of the tool, before and apart from step 2). The Maintainer reviews and
   records the sha256 of each Stage-B authority module *at the reviewed commit*:

   * `bootstrap/tests/_gate_reanchor.py`
   * `bootstrap/tests/_gate_transition.py`
   * `bootstrap/tests/_oracle_activation.py`
   * `bootstrap/tests/_gate_manifest.py`
   * `bootstrap/tests/_oracle.py`
   * `bootstrap/tests/_oracle_trust.py`

   These are exactly the modules `_gate_reanchor._authority_code_files()`
   enumerates. Record the authorized hashes in the supervised commit message (the
   audit trail of *what the Maintainer blessed*).

2. **Generate the new gate manifest over the reviewed tree.** From the trusted
   checkout at the reviewed commit:

   ```
   python bootstrap/tests/_gate_manifest.py produce \
       > bootstrap/tests/fixtures/gate_manifest.json
   ```

   `produce()` frozen-hashes every `bootstrap/tests/**/*.py` — so the new manifest
   **pins all six Stage-B verifier modules** (they move from `FROZEN-NEW` to
   pinned). Confirm the pinned hashes equal the values you recorded in
   step 1 before committing — that equality is what makes this a *reviewed* pin and
   not a self-generated one.

3. **Commit the prerequisite commit — this becomes `P`.** A supervised,
   Maintainer-authored commit containing the new `gate_manifest.json` (and the
   Stage-B gate-control file edits being promoted). This is the new prior gate
   state `P`. Confirm it with the existing external anchor check:

   ```
   python bootstrap/tests/_gate_manifest.py verify \
       --anchor-ref <P-sha> --trusted-repo <trusted-clone> --trusted-ref <trusted-branch>
   ```

   The anchor check proves the working-tree manifest equals the immutable object at
   `P` — the manifest cannot be altered without altering the externally-anchored
   commit.

4. **Create the one fixed designated gate ref at `P`:**

   ```
   git update-ref --create-reflog -m "cairn: supervised gate re-anchor" \
       refs/cairn/gate-anchor <P-sha>
   ```

   `--create-reflog` is not optional and not tidiness. Custom refs carry **no**
   reflog by default, which is how a mis-set anchor once became unrecoverable —
   the prior value was written down nowhere, so "put it back" had nothing to put
   back. This command creates the ref, so it is the one place where omitting the
   flag means the ref has no reflog *for its whole life*: every later transaction
   appends to a log that starts here. The reason string is the same fixed one the
   checker writes (`_gate_preflight._CEREMONY_REFLOG_REASON`), so anchor movement
   is labelled identically whether a human or the ceremony performed it.

   The reflog remains a **local, mutable diagnostic** — see *Audit trail*.

**Why this is not circular / self-authorizing.** The verifier code is pinned by a
commit the Maintainer authored and reviewed separately (step 1's recorded
hashes == step 2's produced pins), confirmed by the externally-anchored
gate-manifest verify (step 3). The promotion command never creates `P`; it only
*reads* it. The new verifier code is trusted because the Maintainer blessed its
exact bytes, not because it asserted its own trust.

**Dated 2026-10-27.** Handing a file to the Maintainer on the machine the
ceremony runs on adds no assurance of its own; the assurance is the review and
the digest you compare. Revisit this section if the ceremony gains an external
or hardware-backed authority. Nothing observes that: no job fires this, and
only a person remembering it does.

---

## Phase 4 — run the supervised promotion

For each candidate `C` to promote:

1. **Author the authorization anchor `A`.** A one-parent commit **on `P`** whose
   diff from `P` contains **only** the two authorization artifacts:

   * `dev/.cairn/promotion-authorization.yml` — the `PromotionManifest` binding
     `prior_anchor=P`, `candidate_sha=C`, `checker_hash` (= the executing
     `_gate_transition.py` hash), `evidence_hash` (= the Stage-A bundle digest),
     `prospective_manifest_hash`, and each changed gate-file hash;
   * `dev/.cairn/trusted-activation.yml` — the trusted `Activation` expectation.

   Point the one fixed authorization ref at it:

   ```
   git update-ref refs/cairn/gate-authorization <A-sha>
   ```

   No `--create-reflog` here, deliberately, and the asymmetry with the anchor
   above is the reason: this ref is ceremony-local and is deleted in step 5, and
   `update-ref -d` removes a ref's reflog with it. A log that cannot outlive the
   thing it documents buys no recoverability — and a *surviving* authorization
   reflog would be worse than none, since it is a readable record of grants that
   is trivially confused for the grants themselves.

   Stage B refuses any `A` that is not a one-parent commit on `P`, or whose diff
   from `P` exceeds those two files — so `A` cannot smuggle candidate content.

2. **Dry-run (`prepare`) — no ref advance.** Runs Stage A + the full data-only
   Stage B validation, constructs `N`, and statically verifies `N`, but stops
   before the CAS:

   ```
   python bootstrap/tests/_gate_reanchor.py prepare \
       --repo <trusted-checkout> --candidate-ref <C> \
       --baseline-ref <pre-refactor-baseline> --trusted-ref <out-of-band-trusted-ref>
   ```

   Every control must read `PASS`.

3. **Promote (supervised CAS).** Identical, with the explicit confirmation flag —
   this is the only step that advances the gate ref:

   ```
   python bootstrap/tests/_gate_reanchor.py promote \
       --repo <trusted-checkout> --candidate-ref <C> \
       --baseline-ref <...> --trusted-ref <...> \
       --confirm-supervised-reanchor
   ```

   The command resolves `A` from `refs/cairn/gate-authorization` and `P` from
   `refs/cairn/gate-anchor` (neither is a CLI override), runs both stages, then
   atomically advances `refs/cairn/gate-anchor` `P → N` by expected-old CAS. A
   replayed or stale promotion cannot advance the ref. `reanchored=True` is
   reported only after the CAS **and** the materialized-`N` static gate
   verification succeed.

4. **The new `N` is the next `P`.** Subsequent promotions resolve their prior gate
   state from the now-advanced `refs/cairn/gate-anchor`.

5. **Retire the authorization ref, by its exact expected-old value.**

   `refs/cairn/gate-authorization` is **ceremony-local**. It authorizes exactly
   one promotion, it is **never published** (it does not appear in any push
   refspec in Phase 5, and there is no configuration under which it is pushed),
   and it is deleted once that promotion has advanced the anchor:

   ```
   git update-ref -d refs/cairn/gate-authorization <A-sha>
   ```

   **Naming `<A-sha>` is the whole point.** A bare `git update-ref -d
   refs/cairn/gate-authorization` deletes whatever the ref happens to point at,
   which is a different operation whenever the ref is not what this ceremony
   left there — a concurrent or interrupted run's authorization, discarded
   silently, with no record that the value removed was not the value promoted.
   The expected-old form fails instead, and a failure here is information.

   **A failed deletion is unresolved ceremony residue.** Report it that way and
   stop: a live authorization ref is a standing grant to promote a specific
   candidate, so leaving one behind is not untidiness, it is an authorization
   that outlived its ceremony. It is never reported as cleanup success, never
   retried with the expected-old value dropped, and never left for a later run
   to trip over. Resolve it — determine what moved the ref and why — before the
   next promotion.

---

## Phase 5 — publish, in one atomic push (M4)

**The Maintainer's step, and no one else's.** `AGENTS.md` makes pushing always
the Maintainer's; here the push is additionally *part of the authorization
ceremony*, because an anchor nobody else can fetch has authorized nothing. No
reviewer and no implementing agent pushes to `origin` on the Maintainer's
behalf.

**Step 1 — one push, both refs, explicit refspecs.**

```
<maintainer-recorded-git> -C <absolute-path-of-the-checkout-to-bless> \
    push --atomic origin \
        refs/heads/<branch>:refs/heads/<branch> \
        refs/cairn/gate-anchor:refs/cairn/gate-anchor
```

* **`--atomic`** — the branch and the anchor are *one* fact. Without it git
  publishes each ref it can and reports partial success, which leaves the remote
  carrying a moved branch whose anchor still names the previous trust root. Every
  fetcher then verifies new code against an anchor that never blessed it, and
  nothing on the remote records that the pair was ever meant to be one update.
* **Explicit refspecs.** Not `--all`, not `--mirror`, and not whatever
  `push.default` resolves to: the ceremony names the two refs it publishes, so
  the set is read off this page rather than out of a config file the ceremony
  does not control. It is also what keeps `refs/cairn/gate-authorization`
  unpublished — the ref is absent because the refspecs are a closed list, not
  because something is expected to filter it out.

**Step 2 — there is no two-push fallback.** If the atomic push is rejected,
**stop and report incomplete publication.** Do not re-push ref-by-ref, do not
push the branch "to at least get the code up", and do not `--force`. A rejection
means the remote's state is not what this ceremony assumed, and the two-push
recovery reproduces by hand exactly the split state `--atomic` exists to
prevent. Diagnose the rejection against the remote's current refs, then re-run
the ceremony from the point the diagnosis indicates.

**Step 3 — verify against the remote, by reading it back.** The push's own exit
status says the client believed it succeeded. Resolve both refs on the remote
and record the object ids in the audit trail:

```
<maintainer-recorded-git> -C <absolute-path-of-the-checkout-to-bless> \
    ls-remote origin refs/heads/<branch> refs/cairn/gate-anchor
```

Exactly two lines, both naming `N`. One line, or two that disagree, is
incomplete publication under step 2 — not a partial success to be topped up.

**Fresh clones need an explicit fetch refspec for the anchor.** `git clone`
fetches `refs/heads/*` and `refs/tags/*`; `refs/cairn/*` is in neither, so a
clone that looks complete has no anchor at all and the gate has nothing to
verify against:

```
git clone <remote-url> <dir>
git -C <dir> fetch origin '+refs/cairn/gate-anchor:refs/cairn/gate-anchor'
```

**Receiving the anchor proves availability, not authenticity.** The fetch says
the remote had a ref by that name; it says nothing about who put it there. What
makes the anchor trustworthy is the signature on the object it names, verified
against the anchored roster — the same check the ceremony ran before publishing.
A fetched anchor is verified, never assumed.

---

## Audit trail

Each supervised run records, in commit messages / the plan execution log: the
authorized verifier-module hashes (Phase 0 step 1), the prerequisite `P` SHA, the
authorization `A` SHA, the candidate `C` SHA, the resulting `N` SHA, and the two
**remote** object ids read back in Phase 5 step 3. The expected-old CAS is the
single-use authority — the ref's own history is the replay ledger.

**The reflogs are a diagnostic, not part of this ledger.** Both refs carry a
fixed ceremony reason (`_gate_preflight._CEREMONY_REFLOG_REASON`), which is what
makes a mis-set anchor recoverable — the prior value is written down somewhere.
But a reflog is local and mutable: whoever can write a ref can write its reflog,
so it is never tamper evidence and never authentication. No decision predicate
in the ceremony reads reflog content, and none may.
