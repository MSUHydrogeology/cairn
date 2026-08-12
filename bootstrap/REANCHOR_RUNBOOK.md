<!-- claim-check-allow: dev/.cairn/trusted-activation.yml, dev/.cairn/promotion-authorization.yml -->
<!-- ^ Maintainer-supplied trust-root configs, absent unless the supervised re-anchor flow creates them. -->

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
trust-root transition — so it is done **once, supervised, out-of-band**, never
silently by the promotion command (round-6 Finding 1).

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
inherited `GIT_DIR` redirected `cat-file` away from the explicitly named `-C`
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

**The loader is its own trust boundary.** Everything below runs *before* the
checker exists, so none of the checker's internal pinning protects it. Reviewed
as its own unit (FUR6): an earlier version obtained the checkout by ambient
discovery and extracted with `git archive`, and repository-local object
substitution caused the literal block to execute substituted checker bytes while
returning success — the same trust-source failure as FUR1, one step earlier.

```
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

**Why each line is the way it is.** `CHECKOUT` is *typed*, not derived: `git -C`
**discovers upward**, so an extraction beneath any repository would otherwise
find *that* one and report against a target never named. `--repo` is not
optional — the checker runs from `$T`, so its own location is the extraction
directory, and it refuses any path that is not a worktree top level. The hash
comparison is the control that makes the extraction route non-load-bearing: it
runs before any Python executes, and its expected values come from the
Maintainer's out-of-band review (step M2 below), never from the checkout.
`shasum -a 256` is macOS/BSD; use `sha256sum -c` where that is what exists.

`apply` re-derives everything itself and **trusts no handoff file**. It runs the
evidence stage, then the read-only checks, then constructs and verifies a signed
commit, then advances the branch and `refs/cairn/gate-anchor` in one expected-old
transaction. `check` is available as a non-mutating preview; its output is a
record to read, not an input.

There is **no flag that turns a refusal into a pass.** A refusal routes here, to
the manual steps below.

**Residual trust set — where the chain actually ends.** **The loader's own
inputs, which nothing above them can check:** the recorded absolute paths
`ENV`, `GIT`, `MKTEMP`, `MKDIR`, `SHASUM` and `PY`; `/bin/sh` itself, which is
fixed rather than recorded so it cannot be chosen wrongly; the recorded
`CHECKOUT` and `HOME`; the recorded first-use hash set; and the operator's
knowledge of the acquisition command in step 1. That set is the bootstrap of the bootstrap: the loader can
verify the checker's bytes, but nothing verifies the loader's.

*A correction worth keeping, because it is the kind of error this document
exists to prevent.* An earlier version of this paragraph said these utilities
came from `PATH=/usr/bin:/bin`. That was **false**: the `PATH` assignment lived
only inside the `env -i` child used for git, and every other utility —
`mktemp`, `mkdir`, and decisively `shasum` — was resolved through the operator's
ambient environment. A replacement `shasum` earlier on `PATH` rewrote the
extracted checker, reported success, and the rewritten checker ran (FUR8). The
recorded absolute paths above are what actually holds; the sentence they replace
described a protection that did not exist. **The signature backend `/usr/bin/ssh-keygen`**,
which the checker pins
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
