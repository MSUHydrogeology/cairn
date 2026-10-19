# PROVENANCE.md — release provenance (Layer 1)

The first-order question an adopter should be able to answer is
**"which Cairn did I install, and where did it come from?"** A content
scanner inspects *what is present*; provenance proves *where it came
from*. Provenance is the foundation the other security layers rest on —
[`SAFETY.md`](SAFETY.md) Rules 7-8 (templates are agent-executed
instructions; the profile is operationally-trusted input), the
executable hardening in [`scaffold.py`](scaffold.py), and the
content-integrity scanner run by
[`check_cairn.py`](../scripts/check_cairn.py).

This is **Layer 1** of the four-layer agent-instruction-supply-chain
model. The blast radius is the reason it matters: Cairn's templates
become an adopter's `AGENTS.md` + `dev/` tree, auto-loaded by the
adopter's agents as governing instructions, so an upstream compromise
reaches every adopter at once. Provenance is how an adopter pins what
they are trusting.

**Every claim below names a command.** If you find a sentence here that
asserts a property with no command behind it, that is a defect in this
document, not a subtlety you are missing.

## Controls

* **Named release artifacts.** Cairn ships tagged releases (e.g.
  `v0.2.0`), not a rolling `main`. A release is the unit an adopter
  installs and cites. Run `git -C <cairn> tag --list` to see them.
* **Signed release tags, from v0.4.0 onward.** A Cairn release is an
  **annotated tag object** (`git tag -s`) whose signature verifies
  against the maintainer's public signing key, and whose *signed* name
  equals the name you asked about. Both halves are checked by the
  bootstrap below; neither alone is sufficient.

  This control has a **date boundary, stated rather than implied**:

  | Release | Tag object | Signed | Verifiable by the bootstrap below |
  |---|---|---|---|
  | `v0.2.0` | annotated | **no** | **no** |
  | `v0.3.0` | annotated | **no** | **no** |
  | `v0.4.0` and later | annotated | yes | yes |

  Tag objects are immutable — re-signing one changes its object id and
  therefore its identity — so `v0.2.0` and `v0.3.0` are **not**
  retro-attested and never will be. Check any tag's shape yourself with
  `git -C <cairn> cat-file -t refs/tags/v0.3.0` (prints `tag` for an
  annotated tag, `commit` for a ref pointing straight at a commit) and
  `git -C <cairn> cat-file -p refs/tags/v0.3.0` (a signed tag's payload
  ends in a `-----BEGIN SSH SIGNATURE-----` block).

  **What was retired here, and why.** This control used to read *"a
  release tag is signed, **or** the release commit is a
  maintainer-authored commit on the protected default branch."* The
  second branch is **retired outright, not softened**: an adopter cannot
  check "maintainer-authored" (`git log --format='%an <%ae>'` prints a
  free-text string any committer can set with `git -c user.name=…`), and
  cannot check "on the protected default branch" (branch protection is
  forge-side configuration; nothing in a clone reports it — `git
  for-each-ref refs/heads` shows the branch, never its protection). A
  control an adopter cannot run is not a control.

* **A published install manifest.** The exact set of files the scaffold
  installs is *emitted from the scaffold's own mappings*, not
  hand-maintained — run:

  ```
  python bootstrap/scaffold.py --manifest
  ```

  The manifest lists each `(source → destination)` pair (and whether the
  file is copied verbatim). It cannot drift from what the scaffold
  actually writes, because it is derived from the same `_CORE_MAPPINGS` +
  `_MODULE_MAPPINGS` the install uses. An adopter (or a reviewer) diffs
  the manifest against what landed in their tree to confirm nothing
  unexpected was written.

* **Scaffold from releases, not arbitrary branches.** Adopters should
  bootstrap from a tagged release checkout, not from a feature branch or
  an unreviewed fork. The scaffold prints a **provenance warning** when
  it is run from a `--cairn-root` whose git `HEAD` is not a tagged commit
  or has uncommitted changes; pass `--allow-dev` to silence it when
  developing Cairn itself. The warning is advisory — it never blocks an
  install — and it degrades silently when git is unavailable or the
  source is not a checkout.

## Verifying a release — the out-of-band bootstrap

This is the **primary** documented path. It runs system `git` in a
workspace you created, against a key fingerprint you compared on two
independent web pages, and it never executes a byte from the thing it is
checking.

### Step 1 — get the fingerprint from at least two channels

Cairn publishes the release signing key's full public-key line and its
`SHA256:` fingerprint on channels that are independent of the release
artifact. Channels are named **generically** so a fork inherits the
procedure rather than Cairn's accounts; the URLs are the *current*
instantiation.

| # | Channel (generic) | Current instantiation | Independent of | **Not** independent of |
|---|---|---|---|---|
| 1 | the git forge account that owns the repository, and its published SSH **signing**-key set | the GitHub account owning `MSUHydrogeology/cairn` | the tag, the tarball, the DOI archive — served by the forge from its own host, not from any release artifact | the forge account itself; whoever holds that account holds this channel |
| 2 | the maintainer's research-identity registry record | the ORCID record published in [`CITATION.cff`](../CITATION.cff) (`orcid:` field) | the forge entirely — different provider, different login, different operator | the maintainer's own credential hygiene |
| 3 | the per-version archival deposition for each release | the Zenodo deposition minted for each release tag | later edits — a Zenodo version record is immutable once published, so the fingerprint recorded beside `v0.4.0` stays recorded | the archive account |

**The rule is one sentence: compare the fingerprint on at least two
channels; a mismatch is a refusal, not a retry.** There is no third
attempt, no "the other page is probably stale", and no reading the
fingerprint out of this file — a fingerprint published inside the
artifact would be a fingerprint an attacker who rewrote the artifact
also rewrote.

**Established** (`as_of 2026-08-04`, by the maintainer): the forge serves
SSH **signing** keys at a stable public endpoint, **distinctly** from SSH
*authentication* keys. Measured on both endpoints for this account:
`https://api.github.com/users/<account>/ssh_signing_keys` returned the
release signing key, and `https://github.com/<account>.keys` — the
*authentication* set — returned a **different** key that does not include
it. The two sets being disjoint is what makes channel 1 usable: an
authentication key an attacker added would not appear on the signing
endpoint. Channel 1 therefore stands as written, channel 2 stays
secondary, and no third channel is required.

Note the endpoint is the **REST API path**, not a `<account>.keys`-style
page: the forge publishes no plain-text signing-key path. A verifier
reads the signing key from the API endpoint above.

**No fingerprint is recorded in this file, deliberately** — see the rule
above. A fingerprint published inside the artifact is one an attacker who
rewrote the artifact also rewrote. Read it from the channels, never from
here.

### Step 2 — write the roster yourself

The roster is an OpenSSH `allowed_signers` file: one line per key, of
the form `principal <keytype> <key>`. **You type it**, from the
fingerprint you just compared:

```sh
mkdir -p ~/.config/cairn
printf '%s %s\n' "$CAIRN_SIGNER" "$CAIRN_KEY" > ~/.config/cairn/release-signers
ssh-keygen -l -f ~/.config/cairn/release-signers    # print the fingerprint back
```

Compare that printed `SHA256:` line against the two channels one more
time. If `$CAIRN_KEY` was unset, the file now holds a principal with no
key; `ssh-keygen -l -f` fails and every verification below refuses.

`~/.config/cairn/release-signers` is deliberately a **different
directory and a different basename** from Cairn's in-repository
`dev/.cairn/allowed_signers`. That in-repository file is the roster for
Cairn's *internal* commit gate. It is **never** consulted for release
verification, and there is no fallback to it: a roster that lives inside
the artifact cannot authenticate the artifact.

### Step 3 — run the bootstrap

Export the three inputs, then run the block. It is exactly the block
Cairn's own test suite extracts from this file and executes against
fixture repositories (`bootstrap/tests/test_verify_ref.py`), so a change
here that breaks the procedure fails Cairn's suite rather than an
adopter's install.

<!-- cairn:bootstrap-block start -->
```sh
# 0. The three inputs. Nothing below reads anything else.
: "${CAIRN_TAG:?set to the release tag you were told to install, e.g. v0.4.0}"
: "${CAIRN_CANDIDATE:?set to the clone URL, or the local path, you are checking}"
: "${CAIRN_ROSTER:?set to the roster you wrote in step 2}"

# 0b. If the candidate is a LOCAL PATH, make it ABSOLUTE. The fetch in step 2
#     runs `git -C "$CAIRN_WS/verify"`, so a RELATIVE path would be resolved
#     against the workspace instead of against your shell, and the fetch would
#     fail with `couldn't find remote ref` — a misleading reason for a tag that
#     is right there. A URL is left alone. Remote means EITHER a scheme
#     (`proto://…`) OR scp-style `[user@]host:path` — and scp-style is decided
#     the way git decides it: the first colon precedes any slash. The `user@`
#     is OPTIONAL, so matching on `@` alone would misread `host:path` as a
#     local path and refuse a legal clone URL.
case "$CAIRN_CANDIDATE" in
  *://*) CAIRN_REMOTE=1 ;;
  *:*)   case "${CAIRN_CANDIDATE%%:*}" in
           */*) CAIRN_REMOTE=0 ;;   # colon sits inside a path segment
           *)   CAIRN_REMOTE=1 ;;   # scp-style host:path
         esac ;;
  *)     CAIRN_REMOTE=0 ;;
esac
if [ "$CAIRN_REMOTE" -eq 0 ]; then
  CAIRN_ABS="$(cd -P "$CAIRN_CANDIDATE" 2>/dev/null && pwd -P)" || {
    echo "REFUSED: local candidate '$CAIRN_CANDIDATE' is not a directory" >&2
    exit 1; }
  CAIRN_CANDIDATE="$CAIRN_ABS"
fi

# 1. A fresh workspace YOU create, discarded at the end. Nothing persists
#    between runs, so a second run can never pass on a first run's object.
CAIRN_WS="$(mktemp -d)" || exit 1

# 2. A bare repository you created, and exactly ONE ref fetched into it.
#    Git config does not travel over a fetch; objects do.
git init --quiet --bare "$CAIRN_WS/verify" || { rm -rf "$CAIRN_WS"; exit 1; }
git -C "$CAIRN_WS/verify" fetch --no-tags --quiet "$CAIRN_CANDIDATE" \
    "+refs/tags/$CAIRN_TAG:refs/tags/$CAIRN_TAG" || { rm -rf "$CAIRN_WS"; exit 1; }

# 3. Resolve the ref you asked about to ONE tag object. `^{tag}` refuses a ref
#    that points at a commit or a tree, and does not peel through a tag that
#    wraps another tag.
CAIRN_OBJ="$(git -C "$CAIRN_WS/verify" rev-parse --verify --quiet \
             "refs/tags/$CAIRN_TAG^{tag}" 2>/dev/null)" || {
  echo "REFUSED: '$CAIRN_TAG' does not resolve to an annotated tag object" >&2
  rm -rf "$CAIRN_WS"; exit 1; }

# 4. Bind the SIGNED name to the name you asked about. Without this step a
#    genuine signature on an OLDER release verifies under a NEWER name.
CAIRN_SIGNED_NAME="$(git -C "$CAIRN_WS/verify" cat-file -p "$CAIRN_OBJ" | awk '
    /^$/ { stop = 1 }
    !stop && /^tag / && name == "" { name = substr($0, 5) }
    END { print name }')"
[ "$CAIRN_SIGNED_NAME" = "$CAIRN_TAG" ] || {
  echo "REFUSED: '$CAIRN_TAG' resolves to a tag object whose SIGNED name is '$CAIRN_SIGNED_NAME'" >&2
  rm -rf "$CAIRN_WS"; exit 1; }

# 5. Verify THE OBJECT ID — not the ref name — against YOUR roster, supplied by
#    invocation so no config anywhere can substitute another one.
#    JUDGE THE EXIT CODE, NEVER THE TEXT: git prints a line beginning
#    `Good "git" signature` on some refusals too, and exits non-zero.
git -C "$CAIRN_WS/verify" \
    -c gpg.format=ssh \
    -c gpg.ssh.allowedSignersFile="$CAIRN_ROSTER" \
    -c gpg.ssh.program=ssh-keygen \
    verify-tag "$CAIRN_OBJ" || {
  echo "REFUSED: the signature on '$CAIRN_TAG' did not verify against $CAIRN_ROSTER" >&2
  rm -rf "$CAIRN_WS"; exit 1; }

# 6. Discard the workspace and report.
rm -rf "$CAIRN_WS"
echo "PROVENANCED: tag '$CAIRN_TAG' (object $CAIRN_OBJ) signed and name-bound"
```
<!-- cairn:bootstrap-block end -->

Each numbered step judges its **own** exit code and stops there. Nothing
in the block reads the text of a git message to make a decision.

**What makes this a bootstrap rather than another circle.** Three
properties, each checkable by reading the block:

1. **The roster arrives by a channel that is not the artifact.** You
   typed it in step 2, from two web pages, before any Cairn byte ran.
2. **The roster is supplied by invocation** (`-c
   gpg.ssh.allowedSignersFile=…`), which outranks repository config, so
   a candidate that points git at its own roster gets no vote.
3. **The verification does not happen inside the candidate at all.** The
   tag object is fetched into a bare repository whose config you wrote.

## Key distribution and rotation

**Distribution** is step 1 above: the fingerprint on at least two
independent channels, compared by a human, before anything runs. That is
trust-on-first-use over account credentials — the same shape as an SSH
host key, with the same properties and the same limits.

**Rotation**, when it happens:

1. The new key's fingerprint is published on **every** channel in the
   table, exactly as the first one was.
2. The transition is announced in an annotated tag signed by the
   **outgoing** key, naming the incoming fingerprint. Read it with
   `git -C <cairn> cat-file -p refs/tags/<announcement-tag>`.
3. The outgoing roster line is republished with `valid-before=<date>`
   and the incoming line with `valid-after=<date>`. **Both stay
   published**, so releases signed before the rotation keep verifying.
   A roster line carrying a validity window looks like:

   ```
   maint@example.org valid-before="20260101" ssh-ed25519 AAAA…
   ```

   Verified behaviour (`git 2.53.0`, `as_of 2026-08-03`, pinned by
   `bootstrap/tests/test_verify_ref.py`): git checks the window against
   the **tagger timestamp inside the signed payload**, not against the
   current clock — a tag dated before `valid-before` verifies, one dated
   after refuses. Read the timestamp being judged with
   `git -C <cairn> cat-file -p refs/tags/<tag> | sed -n '4p'`.

**The honest limit — validity windows are hygiene, not revocation.**
The tagger timestamp is *inside the signed payload*, so whoever holds a
compromised key can set it (`GIT_COMMITTER_DATE=… git tag -s`) and
back-date a tag past a `valid-before` boundary. Cairn's suite pins that
this back-dated tag **still verifies**, precisely so nobody later reads
the window as revocation.

**On suspected compromise the signed-announcement step is void** — the
attacker holds the outgoing key and can sign the announcement. The
response is out-of-band re-anchoring on every channel plus explicit
publication of the revoked fingerprint. **Cairn cannot push that to
anyone**: there is no callback, no revocation list, and no way to reach
an adopter who verified once and never looked again. Re-check the
channels before each upgrade if that risk matters to you.

## `verify-ref.sh` — a convenience, downstream of the bootstrap

`bootstrap/container/verify-ref.sh` performs the same resolve →
name-bind → verify-the-object-id sequence with one command, and the
contained-kernel recipe uses it as its Phase 1 gate.

**It is not the trust root, and it cannot be.** It lives in the
candidate checkout, so running it is already executing candidate bytes.
Use it *after* the bootstrap above has established that the checkout is
what it claims to be, never instead of it.

```sh
bootstrap/container/verify-ref.sh --signers ~/.config/cairn/release-signers <cairn> v0.4.0
```

Its exit contract, which is what a caller should judge:

| Exit | Meaning |
|---|---|
| `0` | `PROVENANCED` — annotated tag object, signed by a rostered principal, signed name equals the name asked for |
| `3` | `NOT PROVENANCED` — an integrity pin accepted under `--unprovenanced`; **no signature was checked** |
| `1` | `REFUSED` — a named control failed |
| `2` | usage error, or not a git repository |

Provenance mode is the **default**, and it **requires** a roster from
outside the candidate (`--signers <path>` or `$CAIRN_ALLOWED_SIGNERS`);
absent one it refuses, with no fallback to repository config, to the
candidate's files, or to your global git config. It also refuses a
roster path that resolves *inside* the candidate tree, symlinks resolved
first — a **path** property, not a content property: a hardlinked or
concurrently-rewritten roster is not covered.

## Signed release tags vs. internal signed checkpoints

Two different signatures, two different claims, and conflating them would
overstate both.

**A signed release tag** is public provenance. It says: this named release
object was signed by a key on the published roster. `verify-ref.sh` checks it,
and adopters verify it without trusting this repository's internal machinery.

**An internal signed checkpoint** is an authorization record. It says: the
Maintainer reviewed a bounded, digest-bound report of a candidate state and
signed a commit whose message carries that digest. It authorizes *that exact
state* and binds its complete parent history.

What the checkpoint deliberately does **not** claim:

* that the Maintainer authored or separately reviewed every intermediate
  commit — unsigned intermediate commits are the normal agent-work format;
* that a signature identifies a human. Signing authenticates a **key holder**.
  If an agent process can invoke the same key, the cryptographic statement
  remains only "this key signed this checkpoint", and the Maintainer-only
  boundary is procedural under the accepted trusted-contributor posture.

Repository-wide `commit.gpgsign=true` is neither required nor recommended. The
release-tag boundary above is unchanged by any of this.

## What this is not

* **Not a transparency log.** This is trust-on-first-use over **account
  credentials**: whoever holds the forge account and the registry record
  holds the channels you compared. There is no independently-witnessed,
  append-only record of what was signed when, so an attacker who holds
  both channels *before* you first look is not detected by anything
  here. A transparency log or keyless signing would close that; both add
  a network service and a non-stdlib client to a path system `git`
  satisfies today, against a zero-adopter-runtime-dependency budget, so
  neither is here.
* **Not a check on the tree you build from.** The bootstrap proves a
  *tag object* is signed and name-bound. It does **not** prove that the
  working tree you then run `scaffold.py` from equals that tag's tree.
  `git -C <cairn> status --porcelain` and `git -C <cairn> rev-parse
  HEAD` are what you have; comparing a materialized tree against the
  tag's tree needs an entry point Cairn does not ship.
* **Not proof of who a human is.** A signature authenticates the
  **holder of the key**, not the person named beside it. Commit and tag
  metadata are free text (`git -c user.name=… -c user.email=… commit`
  will write any name you like); this repository's own record carries a
  demonstration of exactly that at commit `e8f75fc`.
* **Not a content check.** Provenance proves *origin*; it says nothing
  about whether the content is safe. That is what Rule 7's by-class
  injection-review and the content-integrity scanner are for. The layers
  compose: provenance pins *which* Cairn, the scanner + review judge
  *what* it contains.

## Relationship to the release cut

These controls are coupled to the release-cut mechanics (tagging the
release, recording the version, minting the archival DOI). The cut
itself is a separate, maintainer-run step; this document states the
provenance posture the cut is expected to satisfy. Three ordering
constraints follow from the sections above, and all are the
maintainer's:

* The fingerprint is published on the channels **before** the tag is
  cut, so the tag is verifiable the moment it exists.
* The release tag is cut with `git tag -s`, not `git tag -a`. A DOI is a
  permanent, citable pointer that travels with the provenance claim
  attached and none of this repository's controls attached; an unsigned
  tag archived beside a claim of signing is not correctable in place.
* **The security gate runs against the clean commit first; the tag is
  signed second, naming that same commit.** `python
  bootstrap/security_check.py` (see [`SECURITY.md`](../SECURITY.md) >
  *Release security checklist*) refuses a dirty or moved worktree and
  prints the full `HEAD` it checked. Sign the tag on **that** commit id,
  and record the id with the gate output in the release notes. The
  reverse order — tag, then check — produces a signed tag whose tree was
  never the tree that passed, and nothing downstream can tell.

**What that ordering does not establish.** The binding is a human
transcription, not a control: nothing signs the gate result, and the tag
signature attests the tag object only. An adopter who verifies the tag
learns *which* Cairn they have, not that Cairn's release gate was run
against it. That is the same class of residual as the two below in *What
this is not* — accepted under a single-maintainer, trusted-contributor
model, and expiring the moment there is a second release maintainer,
release-path contributions from outside the trusted set, or forge
automation able to cut or publish a tag (`SECURITY.md` states the same
expiry, canonically).

## Install-side provenance — the lockfile

Provenance has two sides. **Source-side** is the above: *which Cairn to
trust* (a named, signed, name-bound release tag). **Install-side** is the machine
lockfile `dev/.cairn/cairn-lock.yml` (see [`UPGRADE.md`](UPGRADE.md)) that the
scaffold writes *into the adopter's tree*: *which Cairn this tree actually
got* — the exact `cairn_commit`, the resolved profile, and the per-file
source / hash, all independently verifiable (the commit is `git
rev-parse`'d, the hashes are measured); plus `cairn_version` and, as of
this field's introduction, `source_repository` / `source_licenses` —
**declared**, not attested, values read from the source tree's
`CITATION.cff` (see `UPGRADE.md` > "Adding a lockfile field without
bumping the schema" for the full distinction). It makes "which Cairn is
this tree?" answerable from the tree itself, not from a human-maintained
manifest that can lag, and it is the ancestor anchor the `upgrade` 3-way
merge reads. A clean install from a signed release (source-side) pinned
by a lockfile (install-side) is the fully-provenanced state.

**What the install side does not cover.** Nothing the scaffold writes is
*signed*: `source_repository` and `source_licenses` are declarations
read from `CITATION.cff`, the per-file hashes attest that the bytes in
your tree match the bytes that were installed (not that those bytes came
from a signed release), and `python bootstrap/scaffold.py --manifest`
emits an unsigned listing. Source-side signing is what this document
fixed; install-side attestation is not built.
