<!-- claim-check-allow: dev/.cairn/trusted-activation.yml, dev/.cairn/promotion-authorization.yml -->
<!-- ^ Maintainer-supplied trust-root configs, absent unless the supervised re-anchor flow creates them. -->

# Supervised re-anchor runbook (differential-oracle gate)

> **Maintainer-only, supervised.** This runbook is how the **trust root** for the
> two-stage re-anchor (`bootstrap/tests/_gate_reanchor.py`) is established and how
> the supervised promotion is run. The *code* is reviewed and tested; **running
> the steps below is the Maintainer's act** — an implementing agent must not
> perform Phase 0 or Phase 4 (that is the forbidden "implementer blesses its own
> verifier" self-authorization).

The re-anchor is **two-stage** (round-4 contract): Stage A gathers executable but
non-authoritative *evidence*; Stage B is data-only and *authoritative*. Stage B
resolves authority from fixed refs, pins the **executing verifier code** against
the prior gate state `P`, constructs `N = C + the reviewed gate manifest`, and
advances the one designated ref `P → N` by an expected-old compare-and-swap.

Because Stage B pins the executing verifier code against `P`'s frozen gate
manifest, the **current** `P` must already pin those verifier modules. The
existing anchored manifests do **not** (the Stage-B modules were introduced later
and read as `FROZEN-NEW`). Establishing a `P` that pins them is itself a
trust-root transition — so it is done **once, supervised, out-of-band**, never
silently by the promotion command (round-6 Finding 1).

---

## Phase 0 — establish the trust root (supervised, one-time)

The mechanism reuses the **existing gate-manifest prerequisite-commit flow**
(`bootstrap/tests/_gate_manifest.py`), the same machinery already used to pin
gate-control files for the six-proposal batch.

### Phase 0 pre-flight — `_gate_preflight.py`

> **Obtain this invocation from the anchor, never from the working tree:**
> `git show refs/cairn/gate-anchor:bootstrap/REANCHOR_RUNBOOK.md`.
> Reading it from the checkout you are about to bless would let the candidate
> choose which bytes you execute.

```
CHECKOUT=$(git rev-parse --show-toplevel)   # record the target BEFORE extracting
T=$(mktemp -d)
git -C "$CHECKOUT" archive refs/cairn/gate-anchor bootstrap/tests | tar -x -C "$T"
<maintainer-recorded-interpreter> -E -s "$T/bootstrap/tests/_gate_preflight.py" \
    apply --repo "$CHECKOUT" --confirm-supervised-reanchor
```

**`--repo` is not optional, and the order of those lines is the point.** The
checker runs from `$T`, so its own location is the *extraction directory*, not
the checkout — an earlier version of this block omitted `--repo` and the checker
defaulted to `$T`, which is not a repository. That was fail-closed by luck, not
design: `git -C` **discovers upward**, so an extraction anywhere beneath a
repository (a `$TMPDIR` inside a checkout is enough) would have found *that*
repository and reported against a target you never named. The checker now
refuses any path that is not the top level of the worktree it names. `$CHECKOUT`
is captured before `mktemp` because afterwards nothing guarantees where you are.

`apply` re-derives everything itself and **trusts no handoff file**. It runs the
evidence stage, then the read-only checks, then constructs and verifies a signed
commit, then advances the branch and `refs/cairn/gate-anchor` in one expected-old
transaction. `check` is available as a non-mutating preview; its output is a
record to read, not an input.

There is **no flag that turns a refusal into a pass.** A refusal routes here, to
the manual steps below.

**Residual trust set — where the chain actually ends.** The `git` and `tar`
binaries; **the signature backend `/usr/bin/ssh-keygen`**, which the checker pins
by absolute path and uses for both signing and verification — an earlier version
let repository config choose it, and a fake verifier made a commit signed by a
key *absent from the roster* report a good signature under a rostered name; the
Maintainer-recorded interpreter path; `PATH` and `HOME` in the operator's shell,
which the checker deliberately does **not** scrub because signing needs them; the
operator's discipline of reading this invocation from the anchor rather than the
checkout; and **local write access to `refs/cairn/gate-anchor` itself** — whoever
can move that ref chooses what executes. That last one is not closable here:
moving that ref *is* the authority this ceremony protects. It is in scope only
under the accepted trusted-contributor posture.

**What the checker does take out of the repository's hands.** Every git
invocation — read *and* write — is pinned so that repository-local
configuration, hooks, and attributes cannot steer it: replacement objects are
disabled (they substituted anchored reads while `rev-parse` reported the real
SHA), hooks are disabled including the default `.git/hooks` (a
`reference-transaction` hook moved a *third* ref while the two-ref transaction
reported success), the filesystem monitor is disabled (it executed a program
during `git status`), and the tree is materialized from raw objects rather than
`git archive` (which honours `.gitattributes`, so `export-ignore` hid a tracked
file from the manifest while leaving it in the blessed tree). Each of these was
reproduced as a working attack before it was closed.

**The evidence stage executes candidate code.** It runs in a tree materialized
without `.git` and with credential-shaped variables dropped and `HOME`
redirected. That is best-effort isolation and **not containment** — the executed
code retains filesystem access outside that tree, process creation, and network
access. Accepted by Maintainer Decision under the dated posture; the tool prints
this on every run.

Its output is **not** wholly non-authoritative, and the runbook says so rather
than leaving it implied: `check` independently re-derives every *static*
manifest field from raw commit objects and refuses on any difference. What stays
trusted to this stage is the pytest **collection** — which cannot be derived
from object bytes, and is the reason the stage exists.

### The dated posture, and what ends it

The trusted-contributor threat model is scoped to **Cairn's own trust root,
single-maintainer, as of 2026-08-03** — not a standing assumption. One trigger is
mechanical: `apply` refuses if any commit at or after the signing epoch is
unsigned or signed by a key outside `dev/.cairn/allowed_signers`. **Two triggers
are not mechanical, and live here because nothing can observe them:**

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

1. **Review the exact verifier bytes out-of-band.** The Maintainer reviews and
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
   pinned). Confirm the pinned hashes equal the out-of-band-authorized values from
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
   git update-ref refs/cairn/gate-anchor <P-sha>
   ```

**Why this is not circular / self-authorizing.** The verifier code is pinned by a
commit the Maintainer authored and reviewed out-of-band (step 1's recorded
hashes == step 2's produced pins), confirmed by the externally-anchored
gate-manifest verify (step 3). The promotion command never creates `P`; it only
*reads* it. The new verifier code is trusted because the Maintainer blessed its
exact bytes, not because it asserted its own trust.

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

---

## Audit trail

Each supervised run records, in commit messages / the plan execution log: the
authorized verifier-module hashes (Phase 0 step 1), the prerequisite `P` SHA, the
authorization `A` SHA, the candidate `C` SHA, and the resulting `N` SHA. The
expected-old CAS is the single-use authority — the ref's own history is the replay
ledger.
