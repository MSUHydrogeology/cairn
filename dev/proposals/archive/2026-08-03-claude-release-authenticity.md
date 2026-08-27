
# Release authenticity — a public trust root for a Cairn release, before v0.4.0 mints a DOI

**Author**: Claude (Strategy)
**Model**: Claude Opus 5
**Date opened**: 2026-08-03
**Status**: accepted
**Touches**: `bootstrap/PROVENANCE.md`, `bootstrap/container/verify-ref.sh`,
`bootstrap/container/recipe.md`, `bootstrap/container/acceptance.sh`,
`bootstrap/tests/test_verify_ref.py` (new), `bootstrap/UPGRADE.md`,
`dev/modules/security-review.md` and its `templates/modules/team-gated/` twin,
`docs/quickstart.md`, `CHANGELOG.md`, `dev/PLANNING.md`
**Related**: successor scope 1 of the superseded `identity-not-name` proposal
(Decision at `6c6ce39`); its External Security Review findings [IDN1] and [IDN2];
the `gate-reanchor-preflight` lifecycle and its [CR1] fix at `0c6d9de`; the
signing epoch at `a07fac8`; the concurrent `gate-claims-vs-enforcement` proposal,
which hands row E1 here under a reversion clause
**Plan review**: required(External, security lens) — see *Plan review tier* below
for why, and for the two specific sweeps this proposal asks that reviewer to run

## Context

`identity-not-name` was superseded on 2026-08-03 into four scopes. This is scope
1, and its Decision binds it more tightly than the others: **[IDN1] and [IDN2]
must be resolved at proposal time, not deferred into the plan.** Everything below
the *Proposal* heading is therefore a settled design, not a direction of travel.

The problem, in one sentence a first-time adopter would recognise: **Cairn tells
you a release is genuine, and nothing it does could tell the difference.**

Three facts, each verified by execution today (2026-08-03) and reproduced in this
document rather than summarized, so a reviewer can re-run them:

* `bootstrap/container/verify-ref.sh` accepts `v0.3.0` and prints `OK — release
  tag`. `git verify-tag v0.3.0` reports `error: no signature found`. There is no
  signature check anywhere in the script.
* `bootstrap/PROVENANCE.md` promises the adopter *"A release tag is signed, or the
  release commit is a maintainer-authored commit on the protected default
  branch."* Neither branch is enforced by anything an adopter can run.
* The same script labels an **unsigned commit authored by an attacker in an
  attacker-controlled repository** as a *"Maintainer-approved commit"*. That is
  not an inference about wording; it is the literal output, reproduced below.

The timing is the reason this is scope 1 rather than scope 4.
`dev/PLANNING.md`'s public-launch sequence schedules *tag `v0.4.0` and push
(triggers Zenodo deposition → DOI) → commit the issued DOI into `CITATION.cff`*.
A DOI is a permanent, citable pointer to a byte snapshot that travels **with the
provenance claim attached and none of the repository's controls attached**. If
v0.4.0 ships with an unsigned tag, the false claim is archived into the one
channel Cairn cannot later correct in place. The marginal cost of preventing that
is `-s` instead of `-a` on a tag step already on the schedule: the signing
apparatus — key, roster, repository signing config — has existed since `a07fac8`.

### Glossary, because this scope is unusually jargon-dense

Cairn's audience is a scientist who codes, so every term is glossed on first use.

* **Annotated tag** — a real git object with an author, a date, a message, and
  optionally a signature. `git tag -a` / `git tag -s`.
* **Lightweight tag** — *not* an object: just a name pointing straight at a
  commit, like a bookmark. It carries no signature and nothing records who moved
  it. `git tag` with no flags.
* **`allowed_signers`** — an OpenSSH text file, one line per key, of the form
  `principal <keytype> <key>`. It is the answer to "whose signatures count?"
* **Fingerprint** — a short hash of a public key (`SHA256:` plus 43 characters)
  that a human can compare across two web pages without transcribing the whole
  key.
* **Principal** — the identity string on an `allowed_signers` line; here, an
  email address.
* **TOFU (trust on first use)** — you decide once who to trust, out of band, and
  everything afterwards chains off that decision. SSH host keys work this way.

## Proposed paths

Proposed paths:
- `bootstrap/tests/test_verify_ref.py` — the negative-test home for this scope; lands with the implementation.

## Proposal

Five parts, one contract: **an adopter can establish, from outside the artifact,
that a Cairn release was signed by Cairn's maintainer — and Cairn never claims
provenance it did not check.**

### Part A — the public trust bootstrap ([IDN1] resolved)

[IDN1] is that a signer roster carried *inside* the thing being verified cannot
bootstrap that thing's provenance. The reviewer reproduced the circular pass; I
reproduced it again independently, in a throwaway repository, before designing
against it:

```
$ git verify-tag v9.9.9                     # attacker key, attacker-committed
Good "git" signature for kendal30@msu.edu   # allowed_signers, attacker .git/config
  with ED25519 key SHA256:JxWKjpks…         # exit 0
```

The attacker chose the key, chose the roster, chose the principal string, and
chose where git looked for the roster. Cryptography confirmed all four were
consistent with each other. That is a tautology, not a provenance check.

**The anchor is a published key fingerprint, not a file in the repository.**

Cairn's own `dev/.cairn/allowed_signers` is a *tracked* file — it is the internal
gate's roster, pinned at `a07fac8` for the re-anchor ceremony, and it is exactly
the file [IDN1] forbids as a release-verification anchor. This proposal keeps the
two rosters strictly separate and states the separation in `bootstrap/PROVENANCE.md`:
the in-repository file is **never** consulted for release verification, and there
is **no fallback** to it.

**The channels.** Cairn publishes the release signing key's full public-key line
and its `SHA256:` fingerprint through channels that are independent of the
release artifact, and instructs the adopter to compare **at least two**:

| # | Channel | Independent of what | Independent of what *not* |
|---|---|---|---|
| 1 (primary) | the git forge account's published SSH **signing** key set for the account owning the Cairn repository | the tag, the tarball, the DOI archive — served over TLS by the forge from its own host, not from any release artifact | the forge account itself; whoever holds that account holds this channel |
| 2 (required second) | the maintainer's **ORCID** record, an institutional research-identity registry with separate credentials and a separate operator | the forge entirely — different provider, different login, different failure mode | the maintainer's own credential hygiene |
| 3 (per-version, immutable) | the **Zenodo** deposition description for each release | later edits — a Zenodo version record is immutable once published, so the fingerprint recorded beside v0.4.0 stays recorded | the Zenodo account |

The rule stated to the adopter is one sentence: **compare the fingerprint on at
least two channels; a mismatch is a refusal, not a retry.**

Channels are named generically in the doctrine (*"the git forge account that owns
the repository"*, *"the maintainer's ORCID record"*) with the concrete URLs given
as the current instantiation, so a fork inherits the procedure rather than
Cairn's accounts. This also keeps the text clear of the vendor-neutrality gate,
which governs AI model/vendor names and does not reach hosting providers, but the
generic form is better doctrine regardless.

**The verification procedure — system `git` only, no Cairn script.**
[IDN1]'s satisfier asks for a bootstrap that does not execute the candidate
checkout. `bootstrap/PROVENANCE.md` gains exactly that, as the *primary*
documented path:

```sh
# 1. Write the roster from the fingerprint you compared across two channels.
mkdir -p ~/.cairn && printf '%s %s\n' "$CAIRN_SIGNER" "$CAIRN_KEY" \
    > ~/.cairn/allowed_signers

# 2. Fetch ONLY the tag object, into a repository whose config YOU wrote.
git init --bare ~/.cairn/verify.git
git -C ~/.cairn/verify.git fetch <cairn-url> refs/tags/v0.4.0:refs/tags/v0.4.0

# 3. Verify. Judge the EXIT CODE, never the text.
git -C ~/.cairn/verify.git \
    -c gpg.ssh.allowedSignersFile=$HOME/.cairn/allowed_signers \
    verify-tag v0.4.0
```

Three properties make this the trust bootstrap rather than another instance of
the circle:

1. The roster arrives by a channel that is not the artifact — the adopter typed
   it, from two web pages, before any Cairn byte ran.
2. The roster is supplied **by invocation** (`-c`), which outranks repository
   config. Verified: with the attacker repository above still configured to point
   at its own roster, `-c` pointing at the genuine roster returns exit 1.
3. **The verification does not happen inside the candidate repository at all.**
   The tag object is fetched into a bare repository the adopter created, whose
   `.git/config` the adopter wrote. Git config does not travel over a fetch;
   objects do.

Property 3 is not decoration, and it is the part of this design that goes beyond
[IDN1]'s stated satisfier. See *A finding the satisfier does not close*, below.

**`verify-ref.sh` uses the same pattern, and demands the roster.** In provenance
mode the script:

* **requires** a trusted roster — `--signers <path>` or `CAIRN_ALLOWED_SIGNERS`;
  absent, it refuses. There is no fallback to repository config, to the
  candidate's files, or to the adopter's global git config.
* **refuses a roster path that resolves inside the candidate tree**, resolving
  symlinks first. A trusted roster that lives in the thing being verified is
  [IDN1] wearing a flag.
* performs verification in a temporary bare repository it creates, fetching only
  `refs/tags/<ref>` from the candidate — never `git -C <candidate> verify-tag`.
* judges the **exit code**. It never greps the output, because the output lies:
  every refusal reproduced for this proposal — wrong key, empty roster, missing
  roster file — still printed a line beginning `Good "git" signature` while
  exiting 1.

### A finding the satisfier does not close, found while designing against it

[IDN1]'s satisfier says to pass the trusted roster explicitly on every
invocation. **That is necessary and it is not sufficient**, and I would rather
record that here than have it found later.

A candidate repository's `.git/config` also names the **program git runs to
verify the signature** — `gpg.ssh.program`. Reproduced today, in a throwaway
repository, against a tag signed by an attacker key, with the *genuine* roster
supplied by `-c` exactly as the satisfier prescribes:

```
$ git -C <candidate> -c gpg.ssh.allowedSignersFile=<GENUINE roster> \
      verify-tag v1.0.0
Good "git" signature for maint@example.org with ED25519 key SHA256:FORGEDFORGEDFORGED
$ echo $?
0
```

The candidate's config pointed `gpg.ssh.program` at a four-line shell script in
its own tree. Git executed it — attacker code, run by the verification step, on
the verifier's machine — and believed its answer. The genuine roster was passed
on the command line and never consulted by anything real.

The same tag, fetched into an adopter-authored bare repository first, refuses:

```
$ git -C <adopter-authored> -c gpg.ssh.allowedSignersFile=<GENUINE roster> \
      verify-tag v1.0.0
Good "git" signature with ED25519 key SHA256:bBPe2Bu9…
No principal matched.
$ echo $?
1
```

This is the same class as [CR1] on the `gate-reanchor-preflight` plan, fixed at
`0c6d9de` by materializing the roster from a trusted anchor into a path outside
the candidate. The lesson that fix recorded — *the artifact under verification
must not supply the material used to verify it* — turns out to have a wider
scope than "the roster": the **verifier program** is verification material too,
and so is every other candidate-controlled config key that influences the
invocation. Enumerating and pinning those keys with `-c` is a fix by
enumeration, and enumeration ages badly; not being in the candidate's git
context at all is a fix by construction. This proposal takes the second, and
adds the enumerated pin (`gpg.ssh.program`, `gpg.program`, `gpg.format`) as
defence in depth rather than as the mechanism.

**What I do not claim:** I found one such key by looking for it. I did not
enumerate every candidate-controlled git config key that can influence a
verification, and I did not sweep the rest of Cairn for other places it shells
out to git against a tree it does not control. That is recorded as residual
**RA5** with an explicit mandate to the plan reviewer, not implied to be handled.

### Part B — exact ref semantics, and honest labels ([IDN2] resolved)

[IDN2] has two limbs. Both are settled here.

**Limb 1 — a SHA proves byte identity, not approval.** Reproduced today against
a throwaway repository whose only commit was authored by
`Attacker <attacker@evil.example>`, unsigned:

```
$ bash bootstrap/container/verify-ref.sh <attacker-repo> <sha>
verify-ref: OK — commit pin 80de7f01… (no exact tag; Maintainer-approved commit)
$ echo $?
0
```

`HEAD`, a full SHA, and a **four-character** abbreviation all produce that line.
The words *"Maintainer-approved"* are printed by a script that has checked no
signature, no branch membership, and no authorization of any kind.

**Disposition — the vocabulary changes, and the mode does.** The script gains two
explicit outcomes, and the word "Maintainer-approved" is deleted from the
codebase:

* `verify-ref: PROVENANCED — annotated tag '<ref>' signed by <principal> -> <sha>`
* `verify-ref: NOT PROVENANCED — commit pin <sha> (integrity only; no signature
  checked)`
* `verify-ref: REFUSED — <reason>`

Provenance mode is the default and requires a signed annotated tag. The
integrity-pin path is reachable only under an explicit `--unprovenanced` flag,
which is what `bootstrap/container/acceptance.sh` will pass for its own dev-tree
run (it currently calls the script with no ref and requires exit 0; that call
site is updated in the same change).

**Limb 2 — `git describe --exact-match --tags` selects *a* tag on a commit; it
does not prove the caller's ref *is* that annotated tag object.** Reproduced with
three tags on one commit (`lw-v9.9.9` lightweight, `v9.9.9` annotated-signed,
`v9.9.9-alt` annotated): `describe` returned `v9.9.9-alt`. And against the real
shipped script, asking about a **lightweight** tag:

```
$ bash bootstrap/container/verify-ref.sh <repo> lw-only
verify-ref: OK — release tag 'real-v1' -> a04874f4…
```

The caller asked about `lw-only`. The script answered about `real-v1`. That is
label substitution in a security gate's output.

**Disposition — the resolver changes.** Resolution starts from the caller's ref
and never from the commit: `git rev-parse --verify "refs/tags/<ref>^{tag}"`,
which yields the annotated tag object or fails. `git describe` leaves the
provenance path entirely.

**The full class table**, decided here rather than at plan time:

| Input | Provenance mode | Why |
|---|---|---|
| annotated tag, signed, key on the trusted roster | **PROVENANCED**, exit 0 | the one case that carries authenticity |
| annotated tag, signed, key **not** on the roster | REFUSED | a signature by an unknown party is not a signature by Cairn |
| annotated tag, unsigned | REFUSED | this is what `v0.3.0` is |
| **lightweight** tag | REFUSED, with its own message naming the distinction | not an object; carries no signature; anyone with push access can move it |
| several tags on one commit | only the tag **named by the caller** is resolved and reported; the others are invisible | the output must answer the question that was asked |
| full 40-hex commit SHA | **NOT PROVENANCED**, exit 0 only under `--unprovenanced` | an integrity pin: proves bytes, proves nothing about who approved them |
| **abbreviated** SHA | REFUSED, always | ambiguous by construction, and today a 4-character prefix is accepted |
| `HEAD` | REFUSED in provenance mode; **NOT PROVENANCED** under `--unprovenanced` | see below |
| branch ref (any spelling) | REFUSED (unchanged) | a mutable tip is not a pin — the existing Codex S5 control, regression-pinned |
| dirty/untracked build surface | REFUSED (unchanged) | the existing cross-phase F#2 control, regression-pinned |

**Does `HEAD` belong at all?** [IDN2] asks for a decision. Mine: **not in
provenance mode**. `HEAD` is whatever the checkout happens to be pointing at; it
is a statement about the operator's filesystem, not about Cairn. It stays
reachable under `--unprovenanced` for one concrete reason — `acceptance.sh` runs
the container recipe against a live development checkout and legitimately has no
tag — and in that mode it is labelled `NOT PROVENANCED` and the word "release"
never appears. It also stops being the **default**: a bare
`verify-ref.sh <repo>` currently means "HEAD, and call it approved", and that
default is how the false label got printed with nobody typing anything.

### Part C — `bootstrap/PROVENANCE.md` reconciled to what is enforced

The sentence *"A release tag is signed, or the release commit is a
maintainer-authored commit on the protected default branch"* is replaced, not
softened. Its second branch is retired outright: an adopter cannot check
"maintainer-authored" (a git author field is a free-text string) and cannot check
"protected default branch" (branch protection is forge-side configuration
invisible from a clone), so the branch describes a control the reader has no way
to exercise. What lands instead:

* **The control, stated as a boundary with a date.** From v0.4.0, a Cairn release
  is a **signed annotated tag** verifiable against the published fingerprint.
  `v0.2.0` and `v0.3.0` are annotated but unsigned and are **not** verifiable —
  stated plainly, because a control that quietly did not exist before today is
  worse than one that says when it began.
* **The out-of-band bootstrap** from Part A, as the primary procedure, with the
  channels table and the compare-two rule.
* **The rotation section** from Part D.
* **Two additions to the existing *"What this is not"* section**: this is
  account-credential trust-on-first-use, not a transparency log (residual RA1);
  and verifying a tag does not verify the tree you build from (residual RA3).
* **`verify-ref.sh` demoted to a convenience**, explicitly downstream of the
  bootstrap, with the reason stated: it lives in the candidate checkout, so
  running it is already executing candidate bytes.

`bootstrap/container/recipe.md` Phase 1 and `docs/quickstart.md` gain one pointer
each to the procedure. `docs/quickstart.md` is where the adopter's clone command
lives, which is where the trust decision actually happens.

**The retired claim is restated in two other places, and both are in scope.** I
found this by grepping for the phrase rather than by assuming
`bootstrap/PROVENANCE.md` was its only home, and it changes the size of the
surface:

* `bootstrap/UPGRADE.md` line 225 — *"Signed tags and Maintainer-approved release
  commits … remain the lockfile's actual origin/integrity controls."*
* `dev/modules/security-review.md` line 169 — *"named releases, signed tags /
  maintainer-approved release commits …"* — and this one **ships**. The install
  manifest carries a row whose source is
  `templates/modules/team-gated/security-review.md` and whose destination is
  `dev/modules/security-review.md` in the adopter's tree, so an adopter who
  selects the security-review module is handed the retired claim in their own
  repository, restated as a checklist item. Cairn's self-hosted copy and the
  template source are byte-identical today (both `sha256:b838724c…`, `as_of
  2026-08-03`), so the edit lands in both or in neither.

Both are edited to match the corrected control, and **only** those sentences.
This is not a second contract riding along: it is one claim across its full
textual surface, which is exactly the drift a corrected
`bootstrap/PROVENANCE.md` would otherwise create. Leaving the shipped module
saying the old thing while the source document says the new thing would be a
review finding on this proposal, and rightly.

Historical occurrences in `CHANGELOG.md` and in the archived deliberation record
are **not** edited — those are append-only records of what was believed at the
time, and rewriting them is exactly what the append-only rule forbids.

### Part D — key distribution and rotation

**Distribution** is Part A: fingerprint published on the channels, compared on
two, roster written by the adopter.

**Rotation** has a mechanical component, which was worth finding. OpenSSH
`allowed_signers` lines accept `valid-after=` and `valid-before=` options, and
git enforces them — verified today, including the part that decides whether the
mechanism is usable at all: **git verifies against the tag's own tagger
timestamp, not against "now".** A tag with a 2021 tagger date verified cleanly
against a roster line carrying `valid-before="20230101"`, while the same key
refused a tag dated today. Retiring a key therefore stops it signing new releases
**without** breaking verification of the releases it legitimately signed.

The rotation procedure, in `bootstrap/PROVENANCE.md`:

1. Generate the new key; publish its fingerprint on **every** named channel. The
   rotation is not complete until all channels agree — a partial rotation is a
   cross-channel mismatch, which the adopter is instructed to treat as a refusal.
2. Announce the transition in an annotated tag **signed by the outgoing key**,
   naming the incoming fingerprint. An adopter already holding the old
   fingerprint can then verify the transition without a second out-of-band trip.
3. Publish the outgoing key's roster line with `valid-before=<rotation date>`,
   and the incoming line with `valid-after=<rotation date>`. Both stay published:
   old releases keep verifying.
4. **On suspected compromise, step 2 is void** — the attacker holds the outgoing
   key and can sign the announcement. The response is out-of-band re-anchoring on
   every channel plus explicit publication of the revoked fingerprint. Cairn
   cannot *push* that to anyone. Residual **RA2**.

**The honest limit of step 3**, demonstrated rather than assumed: the tagger
timestamp is inside the signed payload, so a holder of a compromised key can
back-date a tag to before its `valid-before` boundary and it verifies. I built
exactly that tag today to check. Validity windows are hygiene for honest
rotation; they are not revocation.

### Part E — the v0.4.0 handoff (Maintainer-only)

**Signing the release tag is not this proposal's act and not any implementing
agent's act.** It requires the private key. The plan's implementation ends at:
the verifier, its tests, the documentation, and a stated readiness condition. The
Maintainer then, as part of the existing launch sequence:

1. publishes the fingerprint on the named channels (this is the step that creates
   the trust root, and it must precede the tag so the tag is verifiable the
   moment it exists);
2. cuts `v0.4.0` with `git tag -s`;
3. runs the three-command bootstrap from Part C against the pushed tag, from a
   machine and a roster that did not come from the repository — the acceptance
   check for this whole scope.

The `gate-reanchor-preflight` plan's Chunk G is the precedent for an
implementation whose last step is explicitly the Maintainer's.

### Class C — a declared departure from the Decision's *Carried forward*, needing ratification

> **This section is worded identically in scope 3 (`fork-advisory-semantics`),**
> **apart from two cross-reference sentences that necessarily point the other way.**
> It records a *joint* disposition reached by both drafting authors, so the two
> proposals cannot be read as disagreeing. A reader needs it in only one place;
> it appears in both so that whichever proposal is read first carries it.

The superseding Decision carries forward the `SECURITY_MUTATIONS.md` Class C
follow-on — six `upgrade`-family commands (`cmd_update_profile`, `cmd_init_lock`,
`cmd_rebase`, `cmd_verify`, `cmd_drift`, `cmd_complete_merge`) that write into an
adopter tree without routing through the `_assert_safe_write` containment guard —
as a candidate for scope 1 or scope 3, *"at the drafting author's judgment"*. The
Decision's own condition 1 exists because that follow-on was routed to a roadmap
row in a prior lifecycle and **never opened**.

**Both authors exercised that judgment and both declined.** That is the departure,
and it is stated rather than disguised, because a candidate that each scope
assumes the other took is exactly how this item went missing the first time.

* **Scope 1 declines** because it touches **no** `bootstrap/_scaffold/` file at
  all. Absorbing Class C would attach the entire engine gate set — the Bandit
  engine gate and a Maintainer-run AST baseline re-anchor — to a change that is
  otherwise a shell script and three markdown files, and would stall the v0.4.0
  tag behind it. That coupling is precisely what the four-way split exists to
  prevent.
* **Scope 3 declines** because Class C is a **behavioral change to six write
  paths**, and scope 3 adds no write at all: its detector reads, and
  `test_security_leaf.py`'s pinned `_GUARDED_WRITE_FUNCS` set is untouched by it.
  Folding Class C in would put two contracts and two gate sets in one plan — the
  same failure. Scope 3 already carries two `FROZEN-MODIFIED` HOLDs and an AST
  re-anchor; a six-command write-capability redesign is not a rider on that.

**Shared-package adjacency is not a shared contract.** The one argument for
folding Class C into scope 3 is that both live in `bootstrap/_scaffold/`. Both
authors judged that insufficient: co-location in a package is not co-location in
a *contract*, and "it is in the same directory" is the reasoning that produced
the parent proposal's four-gate-sets-in-one-artifact failure.

**The consequence, stated plainly:** on this disposition Class C is **not claimed
by any of the four successors**, and it therefore needs **its own proposal**.
Neither drafting author has authority to open a fifth scope, so this is put to the
Maintainer as a decision, not resolved here.

**What the Maintainer must choose.** Option 1 is what both authors propose;
options 2 and 3 are recorded as honest alternatives, not straw men.

1. **Ratify the departure and open Class C as its own proposal** — *the option
   both authors propose.* It gets the same anti-debt treatment condition 1 gave
   the four: it is *opened*, not routed. The cheapest form matching condition 1's
   shape is to extend that condition — `identity-not-name` does not archive until
   Class C is opened either. That is a Maintainer condition and only the
   Maintainer can add it.
2. **Overrule scope 3's decline** and direct it to absorb Class C. The cost is
   named above and it is real: two contracts, two gate sets, and a longer
   External security read on the successor that already carries the heaviest gate
   accounting.
3. **Overrule scope 1's decline.** Both authors judge this the worst of the three
   — it puts adopter-tree write containment inside a cryptographic
   release-provenance proposal, and the two share no surface, no test home and no
   reviewer lens — but it is recorded so the choice is a full one.

**The anti-drop mechanism, whichever branch is taken**, because naming a home is
what failed last time: the disposition lands as a `dev/PLANNING.md` row in the
Decision commit of **whichever successor is decided first**, and as one recorded
sentence in `SECURITY_MUTATIONS.md`'s own Class C section (scope 3's `R7` owns
that sentence and its trigger). An accepted proposal archives, and archived
proposals are not read — that is the lesson `gate-reanchor-preflight` Round 5
recorded when it moved its non-mechanical expiry triggers out of the proposal and
into `dev/PLANNING.md` and the runbook. What is not acceptable is the row existing
nowhere; that state is what the Decision's conditions were written to make
impossible.

### Documentation / doctrine surface

* **Descriptive layer** — `bootstrap/PROVENANCE.md` is the main change: a stated
  control corrected to match what is enforced, plus a procedure and a rotation
  policy that did not previously exist anywhere. `bootstrap/UPGRADE.md`,
  `bootstrap/container/recipe.md`, and `docs/quickstart.md` each change by one
  sentence or one pointer.
* **A shipped module** — `dev/modules/security-review.md` and its
  `templates/modules/team-gated/` twin, edited in lockstep (byte-parity between
  the self-hosted copy and the template source is an existing invariant, not
  something this proposal introduces). This is the only **adopter-installed**
  file the scope touches.
* **Entry layer** — none. No new document is created.
* **Governing layer** — **none.** No `AGENTS.md` change, no `doctrine/` change.
  The new procedure is a control Cairn offers adopters, not a rule contributors
  follow.
* **Deliberation layer** — this proposal, its plan, and the residual
  `dev/PLANNING.md` rows below. If this proposal is the first of the four to be
  decided, its Decision commit also carries the Class C disposition row (above);
  if another successor is decided first, that row lands there instead. Either is
  acceptable; the row existing nowhere is not.

`bootstrap/PROVENANCE.md` is named in the proposal template's
`triage-extra-triggers` slot under *Licensing / provenance*, so this is a
proposal-required change on Cairn's own triage rules independent of its security
weight. Touching a module template additionally engages the *Bootstrap fidelity /
install contract* trigger — satisfied here in the weakest form it takes, since
the manifest's row set is unchanged and only one installed file's prose moves.

### Doctrine-change rate-limit

**Applicable, and satisfied on the high-risk limb.** A reasonable reviewer could
read Part C as a doctrine change rather than a correction: `bootstrap/PROVENANCE.md`
states a control adopters rely on, and this proposal *retires one branch of it*
rather than merely rewording. The gate (`doctrine/rationale.md` > "How the
doctrine evolves under evidence") is cleared on the Maintainer's
high-risk-classification limb — this is a security surface, and the superseding
Decision has already classified it as such by assigning
`required(External, security lens)`. The recurrence limb is *also* satisfiable —
[CR1], [IDN1], and now the `gpg.ssh.program` vector are three instances of one
failure shape inside a single rolling week — but the high-risk limb is the
cleaner ground and is the one relied on.

## Rationale

* **Which user workflow does it improve?** The very first one. A scientist's
  first Cairn action is `git clone`, and their second — if they are the kind of
  reviewer Cairn is written for — is "how do I know this is really Cairn?" Today
  the honest answer is "you don't, and the tool will tell you that you do." This
  scope replaces that with four commands and two web pages.
* **What contract does it preserve or clarify?** `bootstrap/PROVENANCE.md` is a
  published promise about a security control. This is the difference between a
  promise and a claim: after this change, every sentence in it names something
  the reader can run.
* **Reproducibility and correctness?** This is the control that makes a *cited*
  Cairn release verifiable rather than merely named. For a project whose adopters
  are scientists who will cite a DOI in a methods section, "which bytes were
  those, and who signed them" is the reproducibility question, not a security
  aside.
* **Why now?** Three timing facts, none of them rhetorical. The signing apparatus
  landed at `a07fac8` today, so the cost collapsed. The v0.4.0 tag-and-DOI step
  is on the schedule and a DOI is permanent. And the concurrent
  `gate-claims-vs-enforcement` proposal has *already deferred* its
  `bootstrap/PROVENANCE.md` row (E1) to this scope under a reversion clause —
  so a second live proposal is now blocked on this one's disposition.

## Alternatives considered

* **Do nothing.** Defensible for exactly as long as v0.4.0 is unscheduled. It is
  scheduled. After the DOI, the cost of the correction rises from "one flag on a
  tag command" to "an erratum against a permanent archival record."
* **Soften the `bootstrap/PROVENANCE.md` wording instead of building the
  control** — this is precisely `gate-claims-vs-enforcement`'s stated fallback if
  this scope is rejected, deferred past v0.4.0, or narrowed. It is a real
  option and it is cheap. Rejected as the *primary*: the sentence describes the
  control Cairn should have, at the moment Cairn is about to mint a permanent
  citation, with the apparatus already sitting on disk. Downgrading the claim
  buys honesty at the price of the control. **Recorded explicitly so the
  reversion clause has a live counterpart here**: if the Decision defers this
  scope, E1 returns to `gate-claims-vs-enforcement` as a wording downgrade and
  nothing is lost at the seam.
* **Pin the dangerous git config keys with `-c` and verify inside the candidate
  repository.** Simpler, one fewer temporary directory. Rejected: it is a fix by
  enumeration against an attacker who reads the same git release notes we do, and
  I do not trust my own enumeration — I found `gpg.ssh.program` by looking for
  it, which is not evidence that it is the last one. Retained as defence in
  depth, not as the mechanism.
* **Sigstore / gitsign keyless signing, or a transparency log.** The genuinely
  stronger answer to residual RA1, and the reason RA1 has a named upgrade path
  rather than a shrug. Rejected for now: it introduces a network service and a
  non-stdlib client into a verification path that system `git` alone currently
  satisfies, which is a poor trade for a project whose stated budget is zero
  adopter runtime dependencies and whose adopters include people on managed
  institutional machines.
* **Retro-sign `v0.3.0`.** Impossible as stated — a tag object is immutable and
  re-signing it changes its hash, breaking anyone who already fetched it. A
  *variant* is possible: publish a new signed annotated tag (`v0.3.0-attested`)
  pointing at the same commit and asserting the correspondence. Rejected as
  scope creep with a poor ratio — it adds a second name for one release, and
  `bootstrap/PROVENANCE.md` stating a dated control boundary is both honest and
  free. Recorded as residual RA7 with its own expiry.
* **A separate `verifying-a-release` document under `docs/`.** Rejected: the content belongs
  beside the control it describes, and `bootstrap/PROVENANCE.md` is that place by
  the documentation-plan routing rule. A new document would be a third place to
  keep in sync.
* **Fold this into the v0.4.0 release sequence as a checklist item rather than a
  proposal.** Rejected on the External reviewer's own ruling: *"moving the tag
  command does not make the shipped verifier less security-critical."* The tag is
  a one-line Maintainer act; the verifier and the published procedure are the
  security artifact, and they need a review tier a checklist does not carry.

## Evidence / verification plan

Every factual claim above was verified by execution on 2026-08-03 against the
live tree at `71abeb4`, with git 2.53.0 and the canonical interpreter
(`~/conda_envs/lhm/bin/python`, 3.13.13) where Python was involved. The
reproductions are inline rather than summarized. Six were run in throwaway
repositories under the session scratch directory, using freshly generated
throwaway SSH keys; **no key material belonging to the Maintainer was used, and
nothing was written into the Cairn tree.**

The measurements that are load-bearing, each independently re-runnable:

1. `verify-ref.sh . v0.3.0` → `OK — release tag`, exit 0; `git verify-tag v0.3.0`
   → `error: no signature found`, exit 1.
2. The self-consistent attacker-tag/attacker-roster pair passes `git verify-tag`
   with exit 0 ([IDN1] reproduced independently).
3. The same pair refuses (exit 1) when the roster is supplied by `-c` from
   outside the candidate.
4. A candidate-configured `gpg.ssh.program` executes attacker code and yields
   exit 0 **even with the genuine roster supplied by `-c`**; the same tag fetched
   into an adopter-authored bare repository refuses.
5. `describe --exact-match --tags` on a three-tag commit returns one arbitrary
   tag; the shipped script therefore answers about `real-v1` when asked about
   `lw-only`.
6. An unsigned attacker-authored commit is labelled `Maintainer-approved commit`
   by the shipped script, via `HEAD`, a full SHA, and a 4-character abbreviation.
7. `valid-before` / `valid-after` are enforced by git, **against the tag's tagger
   timestamp** — so retirement is clean for honest rotation and defeated by a
   back-dated tag from a compromised key. Both directions built and run.
8. Every refusal path tested printed a line beginning `Good "git" signature`
   while exiting non-zero.
9. `python bootstrap/scaffold.py --manifest` emits **96 rows** (`as_of
   2026-08-03`); **none** is `bootstrap/PROVENANCE.md` or anything under
   `bootstrap/container/`. One row *is* `dev/modules/security-review.md →
   modules/team-gated/security-review.md`. So the precise statement — and I had
   this wrong in an earlier draft of this document, which is why it is spelled
   out — is that this scope **adds and removes no manifest row** (the install
   *contract* is untouched) while changing the *content* of exactly **one**
   installed file, by one sentence. The manifest diff is the assertion: empty.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.**
  * *No provenance claim without a verified signature.* Enforced by the class
    table in Part B, one test per row, and by a grep-shaped test: the string
    `Maintainer-approved` appears in **no tool output string and nowhere under
    `bootstrap/container/`**. Scoped that way deliberately — the phrase
    legitimately survives in `CHANGELOG.md` and in the archived deliberation
    record, which are append-only history, and a naive repository-wide grep
    would be a test that has to be weakened the first time it runs.
  * *The candidate never supplies verification material.* Enforced structurally
    (verification runs in a repository the script created) and by two tests: the
    self-consistent attacker pair, and the `gpg.ssh.program` case.
  * *The trusted roster is required and never defaulted.* Enforced by a test that
    runs with no `--signers` and no environment variable and asserts refusal,
    and by a test that a roster path inside the candidate tree is refused.
  * *The caller's ref is the ref reported.* Enforced by the multi-tag test:
    asking about tag X never prints tag Y.
* **Failure modes.** All **closed**. Missing roster → refuse. Unresolvable ref →
  refuse. Non-tag object → refuse. Signature not verifying → refuse. `git` or
  `ssh-keygen` absent → refuse (not degrade). Temporary-directory creation
  failing → refuse. The one deliberately **open** path is `--unprovenanced`,
  which is open by construction and says so in its own output; it is reachable
  only when the operator types the flag.
* **Edge cases.** Handled: every row of the Part B class table; empty roster;
  roster naming a principal with no matching key; roster with comma-separated
  principals (the parsing defect `0c6d9de` found on the sibling surface);
  candidate with no tags; ref containing shell metacharacters; a `--signers` path
  that is a symlink into the candidate. **Out of scope and stated:** SHA-256
  repositories (Cairn is SHA-1; the resolver's hex-length check is written to
  admit 64-hex but is untested); non-UTF-8 principal strings; concurrent
  rotation (two rotations in flight at once); an adopter behind a TLS-intercepting
  proxy, for whom the channel independence argument weakens and who is told so.
* **Public-path → test mapping.** `verify-ref.sh` has exactly one public entry
  point — its command line — and every test drives it through that command line
  via `subprocess`, never by sourcing a function. The tests live in
  `bootstrap/tests/test_verify_ref.py` — registered under *Proposed paths*
  above. Cited as a path rather than a relative link because the file does not
  exist yet; the template's link form assumes an existing test, which a proposal
  that proposes the test cannot satisfy.
  The three-command bootstrap in `bootstrap/PROVENANCE.md` is a *documented*
  public path with no executable home; it is covered by a test that runs the same
  three-command sequence against a fixture repository. The plan decides — and
  states — which of two forms it takes: extracting the commands from the
  document's fenced block (drift-proof, more machinery) or duplicating them with
  a comment naming the source (cheaper, drift-prone). I am not deciding that
  here because it is a genuine implementation tradeoff with no security content;
  I am naming it so it is not silently skipped. That the procedure is three
  commands rather than a paragraph is *because* it has to be executable.
* **Known omissions / intentionally untested edges.** (a) I did not enumerate
  every candidate-controlled git config key that can influence verification —
  residual RA5. (b) I did not test against a git older than 2.53.0, and
  `valid-after`/`valid-before` enforcement and tagger-timestamp verify-time are
  version-dependent behaviours; the plan pins a minimum git version by testing
  for the behaviour rather than parsing a version string. (c) I did not verify
  that the forge actually serves SSH *signing* keys at a stable public endpoint
  for this account — that is a Maintainer-side check, listed in Part E step 1,
  and if it turns out to be false the channel table loses its primary and ORCID
  is promoted. That is the single most likely factual correction in this
  document and I would rather flag it than have it found.

### Tests required

`bootstrap/tests/test_verify_ref.py` (new), driving the shell script through its
command line in throwaway repositories built by a fixture that generates
ephemeral SSH keys. One test per row of the Part B class table, plus:

* the **required negative test** — a self-consistent attacker-tag/attacker-roster
  pair: attacker key, attacker-committed `allowed_signers` naming the genuine
  principal string, attacker `.git/config` pointing git at it. Refusal asserted.
  Unsigned-tag and unrostered-key tests are also present but are explicitly *not*
  the boundary test; they do not reach the bootstrap question at all.
* the **`gpg.ssh.program` test** — candidate config naming a forging verifier;
  refusal asserted **and** the forging script asserted never to have executed.
* the **roster-containment test** — `--signers` pointing inside the candidate
  tree, directly and via symlink; refusal asserted.
* the **single-signer tripwire test** — a roster naming two live principals emits
  the posture-expiry warning (residual RA1's mechanical trigger).
* the **rotation tests** — a key retired by `valid-before` refuses a tag dated
  after retirement and accepts one dated before; **and** the back-dating test,
  which asserts that a back-dated tag from a retired key *still verifies*. That
  last one is a **residual-pinning test**: it exists so that nobody later reads
  the validity window as revocation. `identity-not-name` scope 2 uses the same
  pattern for its exact-name spoof.
* **regression pins** for the two controls this change must not weaken: mutable
  branch refs refuse (Codex S5), and a dirty or untracked build surface refuses
  (cross-phase F#2).

Every test is shown non-vacuous by mutation: remove the check, confirm the test
fails, restore the source byte-identical. That is `gate-reanchor-preflight`'s
Chunk E discipline and it is adopted here without modification.

**Two gate constraints this scope must respect, both checked:**

* The gate's `bootstrap-suite` command expects *"all green; 0 skipped / 0
  xfailed"*. These tests require `git` and `ssh-keygen` on `PATH`. Their guards
  therefore must not fire on the canonical host — and if they ever do, the gate
  fails, which is the correct fail-closed direction. Stated so it is a decision
  rather than a surprise.
* The active gate batch freezes 162 files (`as_of 2026-08-03`) by glob, including
  `bootstrap/tests/**/*.py`. A **new** file there is recorded as `FROZEN-NEW` and
  is *allowed*, not a HOLD; only a **reduced** collection HOLDs. So this scope
  needs **no gate re-anchor ceremony**. And because it touches no
  `bootstrap/_scaffold/` file, it needs **no AST re-anchor** and carries none of
  the high-risk engine obligations. That asymmetry with scope 3 is the concrete
  reason the split lets this one move first.

### Examples / smoke checks

* `bash bootstrap/container/acceptance.sh` — the container recipe's own harness,
  which exercises Phase 1 end to end and whose `verify-ref.sh` call sites this
  change updates.
* The three-command bootstrap from `bootstrap/PROVENANCE.md`, run by hand against
  the pushed `v0.4.0` tag from a machine and roster that did not come from the
  repository (Part E step 3 — the acceptance check for the whole scope).
* `python scripts/check_cairn.py` for every prose change.
* `python -m pytest bootstrap/tests` under the canonical interpreter (3.13.13),
  with collection grown by exactly the new nodes.
* `python bootstrap/scaffold.py --manifest` — expected **unchanged**, and that
  is the assertion: this scope installs nothing into an adopter tree.

## Residuals and their expiry triggers

Per the superseding Decision's condition 2, each residual is enumerated with a
proposed expiry trigger for the Decision to ratify. The pattern is
`gate-reanchor-preflight`'s dated posture, including its hardest-won lesson:
**a trigger recorded only in a proposal is inert, because accepted proposals
archive and archived proposals are not read.** Every trigger below names the
place it will actually be read from.

| # | Residual | Why accepted | Expiry trigger | Mechanical? | Where the trigger lives |
|---|---|---|---|---|---|
| **RA1** | The trust anchor is **account-credential TOFU**: the fingerprint is anchored in the maintainer's control of two provider accounts, not in a transparency log. Compromise of both, or a provider serving split content, defeats it. | Two independent providers is a real bar for a solo-maintained project, and the alternative adds a network service and a non-stdlib client to a path system `git` satisfies today. | **(a)** the adopter-held roster names more than one live principal — Cairn has more than one signer, and a one-person-two-accounts model no longer describes it. **(b)** a transparency-log verifier becomes usable without a new adopter runtime dependency. **(c)** any adopter reports a cross-channel fingerprint mismatch. | **(a) yes** — a tripwire in `verify-ref.sh`, silent at one principal today, fires the moment signing authority widens. It is a **warning, not a refusal**, and it has a known cost: a fork with two maintainers trips it on day one. That is arguably correct (the two-accounts model was designed for one signer) but it is noise for them, and it is the reason the tripwire warns rather than refuses. (b) and (c) no. | (a) in the code and its test; (b) and (c) as a `dev/PLANNING.md` row and a `bootstrap/PROVENANCE.md` *"What this is not"* bullet |
| **RA2** | **Validity windows are not revocation.** `valid-before` retires a key for honest future releases, but the tagger timestamp is inside the signed payload, so a holder of a compromised key can back-date a tag and it verifies. Demonstrated today. | There is no timestamping authority in this design and adding one is RA1's upgrade path, not a separate project. Narrowing the window is still strictly better than not narrowing it. | **Any suspected key compromise.** At that moment the retirement mechanism is known-insufficient and the documented response is out-of-band re-anchoring on every channel plus publication of the revoked fingerprint. | No. | `bootstrap/PROVENANCE.md`'s rotation section — read at rotation time, which is exactly when it matters — and pinned by the back-dating residual test so the limitation cannot be quietly forgotten |
| **RA3** | **Verifying the tag does not verify the tree you build from.** The bootstrap proves a tag object is signed; it does not prove the adopter's working tree equals that tag's tree. | The container recipe closes it (build context materialized from the commit object, plus the dirty-surface refusal). The general clone-and-scaffold path does not, and closing it needs a scaffold-side entry point that is out of this scope. | The scaffold gaining a *"verify my source"* entry point, **or** the lockfile's `cairn_commit` being cross-checked against a verified tag — either of which makes this cheap to close as an addition rather than a redesign. | No. | `bootstrap/PROVENANCE.md` *"What this is not"*, plus a `dev/PLANNING.md` row naming the upgrade path |
| **RA4** | **`verify-ref.sh` still lives in the candidate checkout**, so an operator who runs it before the out-of-band bootstrap is executing untrusted bytes. Not fixable from inside the script. | The documented primary path is system `git` only and touches no Cairn script; the script is a convenience for an operator who has already anchored. | **Any automation** — CI, a Makefile, a recipe step, a skill — that invokes `verify-ref.sh` before the bootstrap. At that point the convenience has become the trust root and needs a different design. | No. | the script's own header and `bootstrap/container/recipe.md` Phase 1, both read at the moment of use |
| **RA5** | **The candidate-git-config class is closed for this surface, not swept.** I found `gpg.ssh.program` by looking for it. I did not enumerate every config key that influences a git verification, nor sweep Cairn's other git invocations against trees it does not control. | Structural avoidance (verify outside the candidate) closes the class *for this surface* regardless of enumeration, which is why the residual is about **other** surfaces, not this one. | **The next surface that shells out to git against a tree Cairn does not control.** Also discharged early if the External plan reviewer's sweep (below) returns a clean enumeration — in which case this residual closes at plan time rather than expiring later. | No. | a `dev/PLANNING.md` row, and an explicit mandate in this proposal's *Plan review tier* section |
| **RA6** | **Install-side provenance is unchanged.** This scope fixes source-side only. The lockfile's `source_repository` / `source_licenses` stay **declared**, not attested, and `scaffold.py --manifest` stays unsigned. | Two different questions with two different mechanisms; bundling them is what the four-way split exists to prevent. Explicitly **not** claimed as fixed. | An adopter asking *"how do I know my installed tree came from the release I verified?"* — **or** scope 3's fork-advisory work reaching the same seam from the other side, which is likely and which would make this cheap to close there. | No. | `bootstrap/PROVENANCE.md`'s existing *"Install-side provenance"* section gains the one sentence that says what is not covered |
| **RA7** | **`v0.2.0` and `v0.3.0` remain permanently unverifiable.** Tag objects are immutable; re-signing changes the hash and breaks anyone who already fetched. | Retro-attestation via a second tag name is possible but adds a second name per release for a project with no external adopters yet. | **Expires by construction at v0.4.0** — the residual is bounded by the release that closes it. Until then, `bootstrap/PROVENANCE.md` states the boundary as a date rather than implying a uniform control. | Yes, trivially — the residual ends when the signed tag exists. | `bootstrap/PROVENANCE.md`'s dated control boundary |

**One residual I am deliberately not carrying**, because it belongs to the parent
lifecycle and was already accepted there: signing authenticates the *key holder*,
not the *human*. `e8f75fc` is the recorded demonstration — an agent-authored
commit that signed cleanly as the Maintainer. This scope inherits that limit and
does not re-litigate it; `bootstrap/PROVENANCE.md` states it in one sentence and
points at the parent record.

## Plan review tier

**`required(External, security lens)`.** The superseding Decision mandates it for
this scope, so the tier is not mine to set — but it is worth recording that I
would ask for it independently, for a reason this proposal demonstrates about
itself.

This lifecycle has now produced **three** instances of one failure shape inside a
single week: [CR1] (the roster's *location* was candidate-controlled), [IDN1] (an
in-repo roster bootstrapping the tag containing it), and the `gpg.ssh.program`
vector in Part A (the *verifier program* was candidate-controlled). The parent
proposal's own Response records that its author found [CR1] at 07:59 and wrote
two fresh instances of the identical class within the hour. I found the third
only because I went looking for the class deliberately, after reading that
record. Vigilance has a demonstrated failure rate here and an adversarial
different-agent-type read has a demonstrated success rate.

Two specific mandates for that reviewer, offered so the pass has a target rather
than a lens:

1. **Run the channel discipline over every step.** For each verification step in
   Part A and Part B — the fetch, the resolve, the verify, the roster read, the
   containment check — name the channel each input arrives by and show it is not
   the thing being verified. That is the mechanical check the parent's Response
   proposed and did not have time to apply.
2. **Sweep the enumeration I did not finish (residual RA5).** Are there other
   candidate-controlled git config keys, or other `git` invocations in Cairn
   against trees it does not control, in this class? A clean answer closes RA5 at
   plan time instead of leaving it to expire.

An Internal review is not proposed as a substitute and would not reach either
mandate.

## Collisions with concurrently open work

* **`gate-claims-vs-enforcement`** — hands its row E1 (`bootstrap/PROVENANCE.md`)
  to this scope with an explicit reversion clause: if this scope is rejected,
  deferred past v0.4.0, or narrowed so `bootstrap/PROVENANCE.md` is left
  unedited, E1 returns there as a wording downgrade. **This proposal edits
  `bootstrap/PROVENANCE.md` and therefore discharges E1** — Part C rewrites the
  exact sentence that row cites. No file is edited by both. The reversion clause
  should be marked discharged when this proposal is accepted, and that is a
  one-line note in that proposal's own record, not an edit made from here.
* **`gate-claims-vs-enforcement`, second seam** — that proposal's sweep also
  cites `templates/modules/team-gated/security-review.md`, but at **line 62** (a
  linter suggestion), not the line 169 provenance restatement this proposal
  edits. Different sentences in one file. Recorded so whichever lands second
  rebases rather than discovers.
* **`planner-line-semantics`** — shares `tools/lifecycle_planner.py` with
  successor **scope 2**, not with this one. No overlap with scope 1; recorded so
  the Maintainer sequencing four successors plus seven Theme 3 proposals does not
  have to re-derive it.
* **The live work-intent claim on `bootstrap/tests/_gate_preflight.py`,
  `bootstrap/tests/test_gate_preflight.py`, and `bootstrap/REANCHOR_RUNBOOK.md`**
  — this scope touches none of those three. `bootstrap/tests/test_verify_ref.py`
  is a new file in the same directory, which the gate records as `FROZEN-NEW`
  rather than treating as a conflict.
* **Scope 3** — no file overlap: scope 3 works inside `bootstrap/_scaffold/`,
  this scope does not touch it. The two scopes reach the same seam from opposite
  sides (residual RA6), and they carry an **identically-worded** Class C section
  recording a joint disposition that needs Maintainer ratification — see *Class C*
  above. Neither proposal claims the follow-on, and each says so in the other's
  words rather than assuming the other took it.
* **Scope 2** — no file overlap. Scope 2's residual **R1** (the exact-name spoof)
  names *this* scope's signing trust root as its non-mechanical expiry condition:
  once a Decision-introducing commit can be bound to a verified signer, scope 2's
  byline classifier is re-decided as a lint over an authenticated signal rather
  than as the thing standing in for one. That is a dependency in one direction
  only and imposes no obligation here — this proposal does not promise to close
  it, and scope 2 does not wait on it.

## Signals the change is wrong

* **The forge does not serve a stable public endpoint for SSH signing keys.**
  Then the channel table has no primary and the design leans on ORCID plus
  Zenodo. Recovery: promote ORCID to primary and add a third channel; the
  procedure is unchanged, only the table is. This is the most likely factual
  correction in the document.
* **An adopter cannot complete the three-command bootstrap without help.** Then
  the trust root is theoretical, because a control nobody runs is a control
  nobody has. Recovery: this is what the postdoc adopter is for — watch the first
  one attempt it cold, and if it fails, the fix is a shorter procedure, not a
  longer explanation.
* **Requiring `--signers` breaks a legitimate workflow** — someone verifying in a
  loop, or an air-gapped operator with no way to write a roster path. Recovery:
  the environment variable already covers scripting; if a real case survives
  that, the answer is a config file in the *adopter's* home, never a fallback to
  the candidate.
* **Refusing abbreviated SHAs breaks the container recipe in practice**, because
  operators paste short SHAs from a log. Recovery: accept an abbreviation only
  when it resolves unambiguously **and** print the full SHA in the output — but
  keep the refusal in provenance mode, where the answer should be a tag anyway.
* **The `valid-before` rotation mechanism turns out to be version-fragile** — an
  older git verifying against "now" rather than the tagger timestamp would break
  verification of old releases after a rotation. Recovery: the plan's
  behaviour-probing test catches this at execution rather than in production;
  if it fires, rotation drops to publish-both-keys-forever and RA2 widens.
* **A reviewer shows that fetching into an adopter-authored repository does not
  actually escape candidate influence** — some fetch-time config or hook I did
  not find. That would invalidate the central structural claim of Part A.
  Recovery: fall back to the enumerate-and-pin design as the mechanism rather
  than as defence in depth, and widen RA5 from "not swept" to "load-bearing".
  This is the finding I would most expect an adversarial reviewer to land, and it
  is the one I would most want them to try.

## Addendum — 2026-08-03 — the mechanical reason Class C was dropped

> **This addendum is worded identically in scope 3 (`fork-advisory-semantics`), for the same reason
> the *Class C* section above is: the two proposals must not be readable as
> disagreeing about the disposition or about how it is held.** It is *appended*
> rather than folded into that section because that section is committed
> lifecycle record. It states what its authors believed when they wrote it —
> before anyone had measured whether the mechanism they proposed is the kind of
> mechanism that holds. Rewriting it would erase that, so the correction is a
> later section.

**What this adds.** The *Class C* section above establishes *that* the follow-on
was documented, routed, and never opened, and takes from it the lesson that
"naming a home is what failed last time." It does not say **why** naming a home
failed. A later audit proposed a mechanical answer. I re-measured it rather than
adopting it on report, and the measured version is stronger and more specific
than the reported one. The disposition does not change; the strength ranking of
the parts holding it does, and one drafting defect in the mechanism surfaces.

### The measurement

Two forms have to be kept apart, and the distinction is the finding.

* **The commit-body form** is what the doctrine actually requires. Cairn's
  archive precondition says the archive commit *body* must name where each
  deferred item went, in a literal `Follow-ups migrated to:` block — the stated
  purpose being that the migration is auditable from the commit log alone
  (`doctrine/proposals.md:370`).
* **The in-file form** is what the only checker in the tree actually looks for:
  a `Follow-ups migrated to:` block inside the artifact.

Measured on this repository, `as_of 2026-08-03`:

* **Commit-body form: 0 of 9** archived plans and **0 of 12** archived proposals.
  Across the entire history exactly one commit message contains the phrase, and
  it is the commit that *introduced* the doctrine, not an archive commit. Plans
  record the migration in prose instead ("Lasting-truth migration: … moved to
  `dev/PLANNING.md` > Queued"). Neither side satisfies the doctrine as written.
* **In-file form: 7 of 9** archived plans carry the block; **1 of 12** archived
  proposals do. The single compliant proposal is a *superseded* one that carries
  the block inside its own Decision section — hand-written, in a Decision commit
  that also performed the archive move.

Method, so this is re-runnable rather than asserted: for the in-file form,
`grep -rl` for the phrase across `dev/plans/archive/` and
`dev/proposals/archive/`; for the commit-body form, for each archived file the
commit that added it at its archive path, then that commit's message body. The
7-of-9 / 1-of-12 figures reproduce the audit's exactly. The commit-body figures
are new here.

### The mechanism, and it is not carelessness

`tools/lifecycle_planner.py` — with its byte-parity twin shipped under
`templates/skills/_lib/` — is the only place in the tree where this precondition
is checked at all. Two facts about it:

* The parser computes the field for **every** artifact, plan or proposal; it is
  kind-independent (`tools/lifecycle_planner.py:488`).
* The *check* is not. It sits inside the plan branch's archived-status arm
  (`tools/lifecycle_planner.py:654`). The proposal branch has no counterpart.

And in the current model it cannot have one, which is the real finding.
`archived` is a plan status; it is **not** a proposal status. The proposal state
tuple (`tools/lifecycle_planner.py:501`) runs `proposed → reviewed → revised →
accepted / rejected / superseded` and stops there; the transition table returns
the empty list from `accepted`, carrying an inline comment that says why — the
archive move is a file operation, not a status flip. There is therefore no
proposal state for an archive-time precondition to attach to. On the proposal
side the gate is not lax. It is **structurally absent**.

That asymmetry is visible in one pair of commands (output abridged,
`as_of 2026-08-03`):

```
$ python tools/lifecycle_planner.py next dev/plans/archive/interpreter-trust-root-fallback.md
lifecycle-planner: current state: archived
lifecycle-planner: VIOLATION: status is 'archived' but no 'Follow-ups migrated to:'
                   block is present (archive precondition).

$ python tools/lifecycle_planner.py next dev/proposals/archive/2026-07-11-claude-record-corrections.md
lifecycle-planner: current state: accepted
   ... three VIOLATIONs reported, none of them about follow-ups ...
lifecycle-planner: (terminal state -- no status transition; any archive move is a
                   file operation, not a status flip.)
```

An archived plan missing its migration block is told so by name. An archived
proposal missing its migration block is told about three unrelated things and
then told the archive is not a transition. (Both artifacts are cited by path in
the transcript because they are literal command arguments; in prose they are the
`interpreter-trust-root-fallback` plan and the `record-corrections` proposal.)

### What this corrects

The superseding Decision's condition 1 in `identity-not-name` diagnosed the loss
this way: the existing archive-precondition rule *"is satisfied by a roadmap
row, and a roadmap row is where `SECURITY_MUTATIONS.md`'s Class C gap went."*
That is right about the outcome and it understates the cause. The rule is not
merely satisfiable by a weak home on the proposal side — on the proposal side it
is not applied at all, and 1-of-12 is what that looks like from outside. Class C
did not slip past a permissive gate. It was routed to the one half of the
lifecycle where the gate does not run.

This is a correction *in favour of* condition 1's instinct, not against it. The
condition was written against the right failure; the failure is worse than
stated.

### Does the anti-drop mechanism inherit the weakness? Yes

Stated plainly, because the *Class C* section above rests on it. The mechanism
proposed there is a `dev/PLANNING.md` row landed in the first successor's
Decision commit. That is **a roadmap row on the proposal side of the lifecycle**
— the same class of object, on the same side, as the one that lost Class C. On
this measurement it is not a stronger mechanism than the one that failed; it is
the same mechanism.

The inheritance is not total, and the two refinements both cut the same way:

* The row lands at **Decision**, not at archive, and `accepted` / `rejected` /
  `superseded` *are* modeled proposal states that the checker validates. So the
  moment is one the tooling can see. But the terminal-state validation checks
  three things — that a `## Decision` section exists, that it carries an isolated
  verbatim-authorization blockquote, and that its byline classifies as a known
  human Maintainer — and follow-up migration is not among them. The row is
  unenforced at precisely the moment it is supposed to land.
* Nothing later can catch its absence. The transition table returns no legal
  target from `accepted`, so there is no subsequent modeled event at which a
  missing row becomes visible to anything.

The row's only guarantee is that a human remembered. That is exactly the
guarantee Class C already had, and it is the guarantee that failed.

### A second defect in the mechanism as written, found while checking this

The *Class C* section says the disposition "lands as a `dev/PLANNING.md` row in
the Decision commit of whichever successor is decided first." `AGENTS.md`'s
scribing guard-rail says a scribed Decision commit flips the status and appends
the Decision section *"and nothing else — no implementation, plan-open, archive,
or roadmap work rides in a scribed Decision commit."* A `dev/PLANNING.md` row is
roadmap work.

This is not hypothetical. The Decision that spawned these four scopes was itself
scribed: commit `6c6ce39` opens "Scribed by Claude (Strategy) at the Maintainer's
explicit instruction" and closes by attesting "no plan-open, **no board edit**,
no implementation." A `dev/PLANNING.md` row would have been excluded from it by
the rule the scribe was following.

So the mechanism as drafted is executable only when the Maintainer types the
Decision commit themselves. If it is scribed — the immediately preceding
precedent — the instruction is either to drop the row or to break the
guard-rail, and neither is what the section intends. This is a drafting defect
in the mechanism, not a problem with the guard-rail. The fix is cheap and is the
Maintainer's to choose: land the row in a **separate, immediately-following**
commit (a one-file `dev/PLANNING.md` commit, which the git-workflow carve-out
already lets land without per-commit approval), and have the Decision section
name that commit as its discharge.

### What would have to change for the row to actually hold

Three components are on the table. The *Class C* section lists them in what this
measurement shows is the wrong order of strength. Corrected ordering, strongest
first:

1. **Extend condition 1 — the only *blocking* component, and already option 1's
   real content.** Option 1 proposes that `identity-not-name` not archive until
   Class C is opened. That is not a row; it is a precondition on an act only the
   Maintainer performs. No tool enforces it either — but its holder is the one
   role that cannot delegate the archive, and its failure mode is a visibly stuck
   artifact rather than a silent missing line. On this measurement the
   *condition* is the load-bearing half of option 1, not the "open a proposal"
   half. Only the Maintainer can add it.
2. **The `SECURITY_MUTATIONS.md` sentence — stronger than the row, and it should
   have been named first.** It sits in the file that an engine change forces
   someone to open, and that file's own closing line already carries a
   re-inventory instruction firing on exactly that event — the trigger scope 3's
   residual **R7** names as its (b). A durable home on a path someone *must*
   walk beats a durable home on a board someone *might* scan. Concrete
   recommendation to the Maintainer: **if only one of the two is landed, land the
   sentence.**
3. **Wire the proposal side — named here, explicitly not taken here.** The
   parser already computes the field for both artifact kinds; what is missing is
   a proposal-side check and a modeled state for it to attach to. That is a
   change to `tools/lifecycle_planner.py` plus its byte-parity template twin, it
   touches the shipped lifecycle contract that adopters install, and on the
   numbers above it would immediately flag 11 of the 12 already-archived
   proposals — which is a disposition question about historical artifacts, not a
   code question. It is proposal-sized. Naming it is the correct treatment;
   taking it as a rider on either successor would repeat exactly the
   four-gate-sets-in-one-artifact failure the split exists to prevent. Recorded
   so whoever opens Class C, or whoever next touches the lifecycle checker,
   finds it rather than rediscovers it.

### What this addendum does not establish

* **It does not establish that the plan side works.** The checker is a read-only
  reporter run at session-start, not a CI gate — it reports, it does not block.
  And 0-of-9 on the commit-body form says the plan side fails the doctrine's own
  stated requirement too. Both sides are out of conformance with the archive
  precondition as written; the difference measured here is that only one side is
  ever *told*.
* **It does not prove this is why Class C specifically was lost.** It establishes
  that the check which should have caught it does not run on that side of the
  lifecycle. That is a sufficient and checkable explanation. Whether some further
  factor also contributed is not measured, and no claim is made that it did not.
* **It does not establish that a `dev/PLANNING.md` row never works.** Rows have
  carried follow-ups in this repository. It establishes that a row is the weakest
  of the three components on offer, and that this particular item has already
  been lost from one.
* **It does not change the disposition.** Both authors still decline Class C, for
  the reasons recorded above, and the three options put to the Maintainer are
  unchanged. What changes is the strength ranking in the anti-drop paragraph and
  the commit mechanics for the row.

### Status

**No status change.** This is an append to a proposal still in `proposed` status
with no review yet; it requests no re-review, adds no scope, changes no
deliverable, and moves no residual. A reviewer reading top-to-bottom should treat
this addendum's ordering — condition, then `SECURITY_MUTATIONS.md` sentence, then
row — as superseding the ordering in the *Class C* section's anti-drop paragraph,
and should treat the separate-commit note above as superseding "in the Decision
commit" there.

## Review -- Gemini Flash (External, Security Review) -- 2026-08-03

**Model**: Gemini 3.6 Flash (External, different-agent-type)
**Verdict**: SHIP (recommend ACCEPT; verified existing `verify-ref.sh` flaw, verified attack neutralization via bare fetch + external trusted roster, confirmed explicit roster requirement)

### Steelman

This proposal solves a critical circular trust defect ([IDN1] & [IDN2]) in Cairn's release verification process. Previously, `bootstrap/container/verify-ref.sh` accepted unsigned tags like `v0.3.0` while printing `Maintainer-approved commit`, and relying on in-repo `allowed_signers` files allowed an attacker repo to self-certify its own forged signatures.

The proposal fixes this by establishing an out-of-band trust bootstrap:
1. The maintainer's public key fingerprint is published out-of-band across multiple independent channels (e.g. GitHub SSH keys, ORCID, Zenodo).
2. The adopter writes a trusted `allowed_signers` file on their own machine.
3. Verification is performed strictly via system `git` into a fresh, bare repository (`git init --bare ~/.cairn/verify.git`), fetching *only* tag objects into a clean environment where candidate `.git/config` settings (such as forged `gpg.ssh.allowedSignersFile` or malicious `gpg.ssh.program` helpers) cannot hijack execution.
4. `verify-ref.sh` is refactored to require an explicit `--signers` roster path, refuse rosters located inside the candidate tree, and judge strict non-zero exit codes rather than string-matching stdout.

### Concerns and Findings

* **[G1] (Verification of Shipped `verify-ref.sh` vs `git verify-tag` on `v0.3.0`)**
  * *Verification:* Executed against Cairn repository at HEAD. `verify-ref.sh . v0.3.0` returns exit 0 while `git verify-tag v0.3.0` returns exit 1 (`error: no signature found`).
  * *Commands & Verbatim Output:*
    ```bash
    $ bash bootstrap/container/verify-ref.sh . v0.3.0
    verify-ref: OK — release tag 'v0.3.0' -> 12ec2ad28f22a7d3d9c19ce67e78d86cc625757a
    $ echo $?
    0

    $ git verify-tag v0.3.0
    error: no signature found
    $ echo $?
    1
    ```

* **[G2] (Proof of Attack Neutralization — Bare Fetch & External Roster Breaks Circularity)**
  * *Question:* Does the proposed design successfully reject a self-consistent attacker attack (attacker key, attacker-committed `allowed_signers`, attacker `gpg.ssh.program` hijack)?
  * *Demonstration:* Constructed a throwaway attacker repository under `/tmp/cairn_attack_demo_*`.
    1. **Attack 1 (Tautological In-Repo Roster):** Attacker signs tag `v9.9.9` with `attack_key` and sets `gpg.ssh.allowedSignersFile` to attacker's own `allowed_signers` in `.git/config`. `git -C <attacker_repo> verify-tag v9.9.9` yields `Good "git" signature for attacker@evil.com` with **exit code 0** (Tautology / In-repo circularity confirmed).
    2. **Attack 2 (In-Repo Verification with Malicious `gpg.ssh.program` Hijack):** Passing `-c gpg.ssh.allowedSignersFile=<trusted_signers>` directly to `git -C <attacker_repo> verify-tag` is hijacked by candidate's `.git/config` setting `gpg.ssh.program = ./fake_ssh.sh`. The attacker script prints forged output and returns **exit code 0** (Proves `-c` alone inside candidate directory is INSUFFICIENT).
    3. **Attack 3 (Proposed Design — Bare Fetch + Trusted External Roster):** Initialized bare repo `~/.cairn/verify.git`, fetched `v9.9.9` from candidate, and ran `git -C verify.git -c gpg.ssh.allowedSignersFile=<trusted_signers> verify-tag v9.9.9`. Result: `No principal matched.` with **exit code 1** (ATTACK REJECTED, circularity broken).
  * *Verbatim Output:*
    ```
    === TAUTOLOGICAL IN-REPO VERIFICATION (ATTACKER SIGNERS IN CONFIG) ===
    STDERR: Good "git" signature for attacker@evil.com with ED25519 key SHA256:ZwZna6If0nv7U4kTjAcqSzqOqnJX8riirl0zWPAtseY
    EXIT CODE: 0

    === IN-REPO VERIFICATION OVERRIDDEN WITH -c TRUSTED SIGNERS (FAILING IF GPG.SSH.PROGRAM TAMPERED) ===
    STDERR: Good "git" signature for maintainer@cairn.org with ED25519 key SHA256:FORGED
    EXIT CODE: 0

    === PROPOSED DESIGN VERIFICATION (BARE FETCH + TRUSTED ROSTER) ===
    STDERR: Good "git" signature with ED25519 key SHA256:ZwZna6If0nv7U4kTjAcqSzqOqnJX8riirl0zWPAtseY
    No principal matched.
    EXIT CODE: 1
    ```

* **[G3] (Confirmation of Explicit Roster Passing for all Invocations)**
  * Verified that every git verification command in the proposed design and updated `verify-ref.sh` script receives the trusted roster explicitly via `-c gpg.ssh.allowedSignersFile=<trusted_path>` and `--signers`, refusing any candidate `.git/config` resolution or in-tree roster file.

### Covered (Lenses Swept & Verbatim Executions)

1. **Shipped vs True Verification on `v0.3.0`:**
   * `bash bootstrap/container/verify-ref.sh . v0.3.0` (exit 0) vs `git verify-tag v0.3.0` (exit 1).
2. **Attacker Repository Simulation & Bare Fetch Test:**
   * Script executed under Python 3.13.13 / bash creating SSH key pairs and git tags in `/tmp`. Confirmed exit 1 rejection under bare fetch.

### Not Covered / Low Confidence (Negative Space)

* **Git Version Dependency:** `valid-before` / `valid-after` OpenSSH signer options were tested under git 2.53.0. Behavior on older system git versions (< 2.34.0) was not tested.
* **Maintainer Out-of-Band Channel Setup (Part E):** Verification of actual SSH public key serving on GitHub/ORCID endpoints for `kendal30` is a Maintainer action prior to `v0.4.0` release tagging.

## Decision (placeholder -- superseded by the Decision at the end of this file)

*(Awaiting the Maintainer. The proposal has cleared External Security Review. The Maintainer may accept the proposal to proceed with plan creation.)*

## Revised proposal -- 2026-08-03

**Scope of the revision: one command in Part A's bootstrap block, one added
test row, one drafting nit.** The trust model is unchanged — fingerprint
compared out of band on two channels, roster written by the adopter, verification
performed outside the candidate's git context. Nothing in Part B, C, D or E
moves, no residual changes disposition, and no gate accounting changes. It is
recorded as a revision rather than as a line in the Response because Part A's
command block *is* the artifact this scope ships to an adopter, and the
superseding Decision binds Part A as settled design rather than as a direction of
travel.

**What is wrong, and it is mine, not the reviewer's.** Part A tells the adopter
to verify in a **fixed, durable** location (a bare repository created at a fixed
path under the adopter's home) and to *"Judge the EXIT CODE, never the text."*
Those two instructions are safe on a first run and unsafe on every run after it.
Reproduced today, git 2.53.0, two throwaway candidate repositories publishing the
**same tag name** — one signed by the genuine key, one by an attacker key —
against **one** reused verification repository (paths abbreviated):

```
-- run 1: fetch from the GENUINE candidate --
 * [new tag]         v9.9.9     -> v9.9.9
fetch rc=0
Good "git" signature for maint@example.org with ED25519 key SHA256:H69QCGeW…
verify rc=0

-- run 2: SAME verification repo, fetch from the ATTACKER candidate --
 ! [rejected]        v9.9.9     -> v9.9.9  (would clobber existing tag)
fetch rc=1
Good "git" signature for maint@example.org with ED25519 key SHA256:H69QCGeW…
verify rc=0
```

The second fetch was **rejected** — git will not clobber an existing tag ref
without a force refspec — and `verify-tag` then exited **0** about the object
cached by the *first* run. An adopter following the documented procedure verbatim,
and judging the exit code they were explicitly told to judge, receives a pass for
bytes they did not fetch on this run.

This is not a cryptographic break: the object that verified was genuinely signed
by the genuine key. It is [IDN2] limb 2 wearing different clothes — *the output
must answer the question that was asked* — reappearing in the documented
procedure after Part B removed it from the script. I fixed the resolver and left
the same shape standing three sections earlier in my own document.

**The revision.**

1. **The verification repository is created fresh per run and discarded** — a
   temporary directory from `mktemp -d`, not a fixed path. The durable thing is
   the **anchor** (the roster the adopter wrote from two web pages); the
   **workspace** must not be durable, because durable workspace state is what
   carried the stale answer. Verified: a fresh bare repository per run refuses
   the attacker tag with exit 1 and has no cached-object path available at all.
2. **The fetch's exit code is judged too**, as its own numbered step. A
   copy-pasted procedure has no `set -e`, so a failed step 3 followed by a
   passing step 4 is exactly the observed failure.
3. A **forced** refspec (`+refs/tags/<ref>:refs/tags/<ref>`) also updates the ref
   and then correctly refuses — checked. It is recorded as the *inferior*
   alternative: it repairs the symptom while keeping cross-run state in a
   directory the adopter accumulates releases in.
4. **One test row added** under *Tests required*: run the documented sequence
   twice, against two candidates publishing the same tag name, and assert the
   second run either reports on the second candidate's object or refuses — never
   a silent pass on the first candidate's. This is a test of the **document**,
   which is what the existing "documented public path with no executable home"
   bullet already commits the plan to covering; it adds one case there, not a new
   test surface.
5. **Drafting nit, fixed in the same pass.** The block is called *"the
   three-command bootstrap"* in Part A and Part E and *"four commands"* in
   *Rationale*. It is four commands; with the revision it is four commands plus a
   discarded temporary directory. The document says "four" throughout, and Part
   E's cross-reference points at Part A, where the block lives, rather than at
   Part C.

**What the revision does not establish.** It removes one false-pass path from one
documented procedure. It does not make that procedure idempotent-safe in general;
it does not touch the case where the adopter's **roster** is stale rather than
their workspace (that stays the rotation section's problem, unchanged); and it is
not evidence that no third instance of this shape remains in the document. It is
one instance, found by re-running the review's own attack scenario twice instead
of once.

## Response -- Claude (author, to External Security Review) -- 2026-08-03

**Model**: Claude Opus 5. Proposal-Response grammar (no implementing commits
exist).

The verdict is SHIP and all three findings are **confirmations** rather than
critiques. That is the disposition profile most in need of independent re-running,
because a confirming finding that was not actually executed does double damage: it
leaves the defect in place *and* retires the suspicion that would have found it.
So each was re-run from scratch — throwaway repositories under the session scratch
directory, freshly generated throwaway SSH keys, git 2.53.0, `GIT_CONFIG_SYSTEM`
and `GIT_CONFIG_GLOBAL` neutralised so no ambient configuration could carry a
result. No key material belonging to the Maintainer was used and nothing was
written into the Cairn tree. Two confirm. One could not have been verified as
stated, and saying so is the value of the pass rather than a slight on it.

* **[G1] accept -- reproduced verbatim, down to the SHA.** `bash
  bootstrap/container/verify-ref.sh . v0.3.0` prints `verify-ref: OK — release
  tag 'v0.3.0' -> 12ec2ad2…` and exits 0; `git verify-tag v0.3.0` prints `error:
  no signature found` and exits 1. One clause the review did not draw out and the
  plan should keep: `12ec2ad2…` is the **commit**, while the tag *object* is
  `fb05e4c1…` — the script resolves `<ref>^{commit}` and never handles the tag
  object at all, which is the mechanical reason it cannot see a missing signature
  rather than merely failing to look for one.

* **[G2] accept -- the conclusion reproduces in full; the exhibit as printed does
  not, and the gap is load-bearing for the plan's test.** All three attacks were
  rebuilt independently. Attack 1 (attacker key, attacker-committed roster naming
  the genuine principal, candidate `.git/config` pointing git at it) passes with
  exit 0 — the tautology. Attack 3 (fetch only `refs/tags/<ref>` into an
  adopter-created bare repository, roster supplied by `-c`) refuses with `No
  principal matched.` and exit 1, and the forging program is **never invoked** in
  either the fetch or the verify — I instrumented it with a witness file to check
  that rather than infer it. So the central structural claim of Part A survives an
  independent reconstruction, and **the circularity is broken**. The correction is
  to Attack 2. The review's transcript labels the forged line `STDERR:` and
  reports exit 0. A forger that writes the `Good "git" signature…` line to
  **stderr** does not produce exit 0 — I built one, git ran it twice (`-Y
  find-principals`, then `-Y verify`), accepted both exit codes, and still exited
  **1**, because git parses the signer out of the program's **stdout**. Moving the
  identical line to stdout yields exit 0 with fingerprint `SHA256:FORGED…` while
  the genuine roster is passed on the command line. The finding is therefore
  right and the exhibit as printed would not produce it. This matters concretely:
  the `gpg.ssh.program` test named under *Tests required* must assert on a forger
  that emits the principal on **stdout** and must assert the forger *executed*, or
  it will pass for the wrong reason — git refusing a malformed forger — and be
  vacuous. That instruction is added to the test's description; it is a
  specification detail, not a design change, so it does not enlarge the revision
  above.

* **[G3] correct -- the property is the design's and I keep it, but there is no
  updated script for anyone to have verified.** G3 states that *"every git
  verification command in the proposed design **and updated `verify-ref.sh`
  script**"* was verified to receive the roster explicitly. The shipped script is
  71 lines and contains no occurrence of `signers`, `allowedSigners`,
  `verify-tag`, or any `gpg.` key (`grep` over the file returns nothing, exit 1);
  it is unmodified since `81ff0fd`, and the test module named under *Proposed
  paths* does not exist. There is nothing executable to have checked. Read as a
  statement about the **design text**, G3 is accurate and I am glad to have it
  read that way — the requirement, the no-fallback rule, and the
  roster-containment refusal are all specified in Part A. Read as a verification
  result it is unsupported, and I flag it because an unearned "verified" on the
  implementation is precisely what would let the implementation ship without one.
  No change to the proposal follows.

**On the review's negative space.** Both *Not Covered* items are already carried
and neither creates a new obligation: the git-version dependency is the
proposal's own known omission (b), which is why the plan pins a floor by probing
for the **behaviour** rather than parsing a version string; and the forge/ORCID
channel check is Part E step 1 plus the first bullet of *Signals the change is
wrong*, where it is already named as the single most likely factual correction in
the document.

**What the review did not attempt, and what I found in its place.** The proposal's
last *Signals the change is wrong* bullet invites exactly one adversarial test —
*show that fetching into an adopter-authored repository does not escape candidate
influence* — and says it is the finding I would most want a reviewer to try. The
review did not try it; its Attack 3 reproduces my own demonstration rather than
extending it. I ran the extension instead. Against a local fetch from a hostile
candidate I probed six candidate-controlled surfaces for code execution on the
verifier's side: `uploadpack.packObjectsHook`, `core.alternateRefsCommand`,
`core.fsmonitor`, `core.gitProxy`, `core.sshCommand`, and a `post-upload-pack`
hook on disk. None fired. That result is **weaker than six-for-six**, and the
weakness is the honest part: three of the six are transport- or
alternates-conditional and a local fetch may never reach them, so they are
inconclusive rather than negative. The three meaningful ones are meaningful
because of a positive control — the same hook, moved into a *trusted* (global)
config, fired and was caught by the witness, so the harness can see execution when
it happens. `uploadpack.packObjectsHook` in particular is ignored from
repository-level config by design, which is git protecting exactly this case.

**Residual RA5 does not close, and it does not narrow.** Six probes on one surface
is not an enumeration; it is one author looking again in the place he already
knew to look. RA5's expiry trigger and its mandate to the plan reviewer stand
unchanged, and the reviewer's second mandate — sweep Cairn's other `git`
invocations against trees it does not control — remains entirely unrun. So does
the first mandate (name the channel each verification input arrives by). Those
were written for the plan reviewer rather than this one, so their absence is not a
defect in this review; it does mean the plan's `required(External, security lens)`
tier is carrying its full original load and should not be read as partly
discharged by a SHIP verdict at proposal time.

**The Maintainer's 2026-08-03 direction on the default security stance, and where
it bears here.** The direction — *"Obviously we need to change the default
security stance for all installations. Otherwise we are shipping a potentially
dangerous tool."* — is a premise, not an open question, and it reaches exactly one
thing in this scope: Part B's flip of `verify-ref.sh`'s **default** from "HEAD,
and call it approved" to provenance-required, with the permissive path reachable
only when an operator types `--unprovenanced`. That flip is no longer a judgment
call this proposal has to argue for; it is the direction applied to this surface,
and I record it as ratification rather than re-arguing it. It reaches nothing
else here. This scope selects no module, changes no preset, and adds and removes
no manifest row — the *fail-closed-by-default* half of the direction is discharged
here, and the *selected-by-zero-presets* half belongs to the proposals that own
module selection (`scan-coverage` and `content-scan-detectors`), not to this one.
Naming that boundary rather than quietly widening the scope is the point.

**Status.** `reviewed` -> **`revised`**, on the Part A correction above. No
finding in this review caused the move; re-running one of its findings twice did.

## Review -- Claude (Internal, same-agent-type; security lens) -- 2026-08-03

**Model**: Claude Opus 5.

**Verdict**: REVISE, with one **BLOCKING** finding ([I1]) that must be resolved
at proposal time rather than deferred to the plan, because the superseding
Decision binds Part B as settled design and [I1] says the settled design is
wrong on one row of its own class table.

Every command below was run today against the live tree, git 2.53.0, in
throwaway repositories under the session scratch directory with freshly
generated throwaway SSH keys, `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM`
neutralised to empty files so no ambient configuration could carry a result. No
key material belonging to the Maintainer was used and nothing was written into
the Cairn tree. Where I could not reproduce something I say so.

### Steelman

The core structural move is right, it is the hard part, and it holds under an
independent reconstruction.

I rebuilt the hostile candidate from scratch — attacker signing key, an
attacker-committed roster naming the *genuine* principal string, and the
candidate's own `.git/config` pointing both `gpg.ssh.allowedSignersFile` and
`gpg.ssh.program` at attacker-controlled files in its own tree — and ran the
revised four-command bootstrap against it, with a witness file recording every
execution of the forging program:

```
$ git init --bare -q "$V/verify.git"
$ git -C "$V/verify.git" fetch "$LAB/hostile" 'refs/tags/v0.4.0:refs/tags/v0.4.0'
From .../ra-lab/hostile
 * [new tag]         v0.4.0     -> v0.4.0
fetch rc=0
$ git -C "$V/verify.git" -c gpg.ssh.allowedSignersFile="$LAB/trusted_signers" verify-tag v0.4.0
Good "git" signature with ED25519 key SHA256:AR+EbHSO6nLnvX6D4qLNqruLhEGPPkzvYzVlTmRz5Pw
No principal matched.
verify rc=1
forger executed at any point? NO
```

Fetching into an adopter-created bare repository does escape the candidate's git
context: the forging verifier never ran, and the forged key was refused. Contrast
the same candidate verified *in place* with the genuine roster supplied by `-c`,
exactly as [IDN1]'s satisfier prescribes — and note this also settles the author's
correction to the External review's [G2] exhibit, which I could otherwise not
have taken on trust:

```
$ git -C $LAB/hostile -c gpg.ssh.allowedSignersFile="$LAB/trusted_signers" verify-tag v0.4.0
Good "git" signature for maint@example.org with ED25519 key SHA256:FORGEDFORGEDFORGED
rc=0
forger executed? YES
--- what git asked the forger to do ---
ARGS: -Y find-principals -f .../trusted_signers -s /var/folders/.../.git_vtag_tmpDAoY4u -Overify-time=20260803170224
ARGS: -Y verify -n git -f .../trusted_signers -I maint@example.org -s /var/folders/.../.git_vtag_tmpDAoY4u -Overify-time=20260803170224
```

The author was right and the External reviewer's pasted exhibit was not: a forger
emitting the `Good "git" signature` line on **stderr** exits 1; the identical line
on **stdout** yields exit 0. My first attempt used a naive forger and got `rc=1`,
which is precisely the "passes for the wrong reason" vacuity the Response warns
the plan's test about. That warning is correct and load-bearing.

Part D's rotation mechanism also reproduces, including the part the whole
mechanism rests on:

```
$ printf 'maint@example.org valid-before="20230101" %s\n' "$(cut -d' ' -f1,2 maint_key.pub)" > retired_signers
$ git -c gpg.ssh.allowedSignersFile=retired_signers verify-tag v0.1.0-old   # tagger 2021-05-05
2021-dated tag  rc=0
$ git -c gpg.ssh.allowedSignersFile=retired_signers verify-tag v0.3.0       # tagger today
today-dated tag rc=1
```

And the premise reproduces exactly, down to the SHA:

```
$ bash bootstrap/container/verify-ref.sh . v0.3.0
verify-ref: OK — release tag 'v0.3.0' -> 12ec2ad28f22a7d3d9c19ce67e78d86cc625757a
verify-ref rc=0
$ git verify-tag v0.3.0
error: no signature found
git verify-tag rc=1
```

```
$ bash bootstrap/container/verify-ref.sh <attacker-repo> HEAD
verify-ref: OK — commit pin 823184c7aafb06d42d4a8894ba9d61a145bd3b8a (no exact tag; Maintainer-approved commit)
```
(same line for the full SHA and for the 4-character abbreviation `8231`; commit
authored by `Attacker <attacker@evil.example>`, unsigned.)

The claim-level bookkeeping is also honest. Byte-parity of the shipped module and
its self-hosted twin reproduces (`sha256:b838724c729a9e37…` for both). The
sibling-collision note is accurate: `templates/modules/team-gated/security-review.md`
line 62 is the "wire a linter" paragraph and line 169 is the provenance
restatement — different sentences, as claimed. `bootstrap/UPGRADE.md` line 225
carries "Maintainer-approved release commits" as stated. `FROZEN-NEW` semantics
are as described (`bootstrap/tests/_gate_manifest.py` line 366: "new gate/test
file — allowed, recorded"), and `frozen_files` held exactly 162 entries at the
proposal's own commit.

This is an unusually well-evidenced proposal. The findings below are what survived
that.

---

### [I1] BLOCKING — the exact-tag resolver binds the caller's ref to a tag *object*, but not to the *name that object was signed under*. A hostile mirror that never touches the signing key gets `exit 0`.

**The claim.** Part B's class table asserts:

> | **lightweight** tag | REFUSED, with its own message naming the distinction | not an object; carries no signature; anyone with push access can move it |

and the glossary that produces that row asserts:

> * **Lightweight tag** — *not* an object: just a name pointing straight at a
>   commit, like a bookmark.

The second sentence is the false premise. A lightweight tag is a ref pointing at
*any* object — including an **annotated tag object**. The specified resolver,
`git rev-parse --verify "refs/tags/<ref>^{tag}"`, refuses a lightweight tag only
when it points at a non-tag object. It accepts one that points at a tag object,
and `git verify-tag` never compares the ref name against the name inside the
signed payload.

**The consequence.** An attacker who holds the forge account but **not** the
signing key can publish any past genuinely-signed tag object under any new
version name, and the documented four-command bootstrap returns exit 0 with a
good signature from the genuine maintainer key. I built the forge-side repository
as a bare clone, which is the shape a forge actually serves:

```
$ git clone -q --bare "$LAB/cand" "$LAB/mirror"
$ git -C "$LAB/mirror" update-ref refs/tags/v0.5.0 "$(git -C $LAB/cand rev-parse refs/tags/v0.3.0)"

=== adopter runs the documented four-command bootstrap, asking for v0.5.0 ===
$ git -C "$V/verify.git" fetch "$LAB/mirror" 'refs/tags/v0.5.0:refs/tags/v0.5.0'
fetch rc=0
$ git -C "$V/verify.git" -c gpg.ssh.allowedSignersFile="$LAB/trusted_signers" verify-tag v0.5.0
Good "git" signature for maint@example.org with ED25519 key SHA256:KU/c8lGmOcMnL1PyJNkVG6UmdHi4xXsgXSlEeQ0PTl8
verify rc=0
--- and the proposal Part B resolver agrees it is an annotated tag ---
$ git -C "$V/verify.git" rev-parse --verify 'refs/tags/v0.5.0^{tag}'
e4d52de4c8482df65ad240b5f18049230619c25d
--- but the signed payload says: ---
$ git -C "$V/verify.git" cat-file tag v0.5.0
object 80e3c25696704cb1ae5a7ee5e1e0f399f9cc15b0
type commit
tag v0.3.0
```

The adopter asked about `v0.5.0`. The signed object says `v0.3.0`. Exit code 0.
The bootstrap's own instruction is *"Judge the EXIT CODE, never the text"*, so
the one place the real name appears — the payload echoed by `git tag -v` — is
the place the adopter has been told not to read.

**Why this is a finding and not a re-raise.** Nothing in the proposal, the
External review, or the Response mentions the tag object's embedded name; `grep
-n -i "embedded\|cat-file tag\|name field\|tag name"` over the proposal returns
only three hits, none of them about this. And this is [IDN2] limb 2 in its own
words — *"the output must answer the question that was asked"* — surviving the
resolver written to close it. The author already caught one recurrence of this
shape in the Revised proposal ("I fixed the resolver and left the same shape
standing three sections earlier in my own document"). This is a third instance,
inside the fixed resolver itself.

It also silently defeats Part D. Substitution reuses the old object with its old
tagger timestamp, and `valid-before` is evaluated against that timestamp — so a
rotated-out key's tags stay substitutable forever. That is adjacent to RA2 but is
not RA2: RA2 requires holding the compromised key, this requires no key at all.

**It also breaks two stated invariants.** *"The caller's ref is the ref
reported"* — the ref reported is `v0.5.0` and the ref signed is `v0.3.0`. And the
contract sentence, *"an adopter can establish, from outside the artifact, that a
Cairn release was signed by Cairn's maintainer"* — what the adopter establishes
is that *some* Cairn tag object was signed, not that *this version* was. For a
project about to mint a DOI per release, "which release did I verify" is the
whole question.

**Recommended fix, verified.** Bind the ref to the signed name. One extra command:

```
$ check_name () {
    obj="$(git -C "$1" rev-parse --verify "refs/tags/${2}^{tag}" 2>/dev/null)" || { echo "REFUSED: not an annotated tag"; return 1; }
    embedded="$(git -C "$1" cat-file tag "$obj" | awk '/^tag /{print $2; exit}')"
    [ "$embedded" = "$2" ] || { echo "REFUSED: ref '$2' resolves to a tag object whose signed name is '$embedded'"; return 1; }
    echo "name-bound OK: $2"; }
--- substituted ref ---
REFUSED: ref 'v0.5.0' resolves to a tag object whose signed name is 'v0.3.0'
rc=1
--- genuine ref (must still pass) ---
name-bound OK: v0.3.0
rc=0
```

It discriminates, it does not break the honest case, and it belongs in **both**
the `bootstrap/PROVENANCE.md` bootstrap block and `bootstrap/container/verify-ref.sh`
— the script inherits the defect because it inherits the resolver. Two class-table
rows need rewording with it: the lightweight row (refusal is *by object type*, not
by tag class) and a new row for name substitution. The glossary sentence needs
correcting too, since it is the premise that produced the wrong row.

Fairness note: the resolver *is* a strict improvement over `git describe
--exact-match --tags`, which I confirmed still picks an arbitrary tag from a
commit (`v0.3.0-alt`, given three tags on one commit) and still reports a
lightweight tag as a "release tag". [I1] is that the replacement closes most of
limb 2, not all of it.

---

### [I2] REVISE — the default flip makes two of `acceptance.sh`'s negative regression pins vacuous, and the proposal names only the one call site that fails loudly.

The proposal says of `bootstrap/container/acceptance.sh`:

> it currently calls the script with no ref and requires exit 0; that call site
> is updated in the same change

Singular. There are five invocations, and they split into two kinds:

* `acceptance.sh` line 55 and line 79 are **positive** assertions (`|| fail`) —
  they break loudly the moment provenance mode refuses `HEAD`, so an implementer
  will find and fix them.
* `acceptance.sh` line 81, line 84 and line 62 are **negative** assertions
  (`&& fail` / `if … then fail`) — they pass whenever the script refuses, *for
  any reason*.

Once provenance mode is the default, `HEAD` is refused unconditionally, so lines
81 and 84 pass without the dirty-surface check existing at all. I demonstrated
this by writing a stub that implements only "provenance mode refuses HEAD" and
has the dirty/untracked build-surface check **deleted entirely**, then replaying
those two lines verbatim:

```
=== replaying acceptance.sh lines 81 and 84 verbatim against the STUB ===
LINE 81 PASSES -- but the dirty check does not exist in this stub
LINE 84 PASSES -- but the dirty check does not exist in this stub
```

Line 62 has the same shape for the Codex S5 branch pin: the specified provenance
resolver refuses a branch name because it is not an annotated tag, not because
the branch guard fired —

```
$ for R in main HEAD v0.3.0; do git rev-parse --verify "refs/tags/${R}^{tag}"; done
main     -> fatal: Needed a single revision
HEAD     -> fatal: Needed a single revision
v0.3.0   -> e4d52de4c8482df65ad240b5f18049230619c25d
```

— so `bootstrap/container/verify-ref.sh` lines 31-39 could be deleted wholesale
and line 62 would still report `ok`.

This is exactly the shape the brief warned about: a regression guard whose oracle
stops discriminating. It is worse here than in the pytest module, because the
proposal's mutation discipline (*"remove the check, confirm the test fails"*) is
scoped to the new test module and does not cover a shell harness. And the
asymmetry is the trap: fixing only what breaks loudly leaves the two silent ones
vacuous, and the proposal's own sentence points at exactly the loud one.

**Fix**: state that *all four* no-ref call sites plus the branch pin take
`--unprovenanced`, and add one row to *Tests required* asserting that the
dirty-surface and branch refusals are still distinguishable from the
provenance-mode refusal — e.g. by asserting on the refusal *reason*, not only on
the exit code. Related and cheap: `PROVENANCED` and `NOT PROVENANCED` both exit 0,
so no caller can distinguish them by exit code; a distinct code for the
unprovenanced path would make these pins self-discriminating.

Second-order: because `acceptance.sh` will now run permanently in
`--unprovenanced` mode, Cairn's own end-to-end harness never exercises the
provenance path. The proposal lists `acceptance.sh` under *Examples / smoke
checks* for this scope; after this change it smoke-checks the mode this scope did
not add.

---

### [I3] REVISE — RA1's expiry trigger is marked mechanical, but no mechanism exists by which Cairn learns its own signing authority widened.

RA1 (a) is recorded as:

> **(a) yes** — a tripwire in `verify-ref.sh`, silent at one principal today,
> fires the moment signing authority widens.

Three facts make "fires the moment signing authority widens" stronger than the
mechanism delivers:

1. The tripwire counts principals in the **adopter-held** roster — the file the
   adopter typed from two web pages. Cairn adding a second signer changes nothing
   in any adopter's file until that adopter re-anchors. Cairn's *own* roster,
   `dev/.cairn/allowed_signers`, holds exactly one principal today (`wc -l` = 1)
   and this design explicitly forbids consulting it for release verification.
2. It lives in `bootstrap/container/verify-ref.sh` — the artifact Part C
   *demotes to a convenience* and RA4 tells operators not to reach for before the
   bootstrap. The documented primary path is system `git` only and never runs it.
3. The warning surfaces on an adopter's terminal. There is no channel back to
   Cairn. Meanwhile the proposed test asserts the warning fires against a
   two-principal fixture roster — so the one place it reliably fires is Cairn's
   own suite, where it is expected and carries no information.

This does not make the tripwire useless; it makes it an adopter-facing hygiene
warning, not a posture-expiry trigger for Cairn. **Fix**: either re-mark RA1 (a)
as non-mechanical and give it a `dev/PLANNING.md` home like (b) and (c), or add a
second, genuinely mechanical tripwire over `dev/.cairn/allowed_signers` that runs
in Cairn's own suite. The residuals table is the artifact a future Maintainer
reads to decide whether the posture still holds; a trigger marked "yes" that
cannot fire on Cairn's side is the failure mode the table exists to prevent.

---

### [I4] REVISE — the Revised proposal falsifies the reason the documented-path test's form was deferred, and the append-only record never says so.

*Public-path → test mapping* defers the form of the bootstrap test to the plan:

> The plan decides — and states — which of two forms it takes: extracting the
> commands from the document's fenced block (drift-proof, more machinery) or
> duplicating them with a comment naming the source (cheaper, drift-prone). I am
> not deciding that here because it is a genuine implementation tradeoff with no
> security content

That was written before the Revised proposal demonstrated that **the defect was
in the document text itself** — a fixed durable workspace plus "judge the exit
code" yielding a false pass on the second run. Under the *duplicating* form, the
test runs a private copy of the sequence; it cannot detect that
`bootstrap/PROVENANCE.md` still tells adopters something unsafe. The revision's
new test row (item 4) explicitly leans on this same bullet — so the revision's own
guard is only as good as a choice the proposal characterises as security-neutral.

It has security content now. **Fix**: one appended sentence choosing the
extract-from-the-document form for this test, or stating the constraint that
whichever form is chosen must fail when the document's fenced block changes.

---

### [I5] NIT — *"Fetch ONLY the tag object"* is not what step 2 does, and the gap is checkable.

`bootstrap/PROVENANCE.md`'s block will carry the comment `# 2. Fetch ONLY the tag
object, into a repository whose config YOU wrote.` The fetch transfers the full
reachable object graph *and* auto-follows other tags:

```
$ git -C "$V2/verify.git" fetch "$LAB/cand" 'refs/tags/v0.3.0:refs/tags/v0.3.0'
 * [new tag]         v0.3.0     -> v0.3.0
 * [new tag]         v0.4.0     -> v0.4.0
 * [new tag]         v0.3.0-alt -> v0.3.0-alt
$ git -C "$V2/verify.git" for-each-ref --format='%(refname) %(objecttype)'
refs/tags/v0.3.0 tag
refs/tags/v0.3.0-alt tag
refs/tags/v0.4.0 tag
```

Three refs the adopter did not ask for, named by the candidate, now exist in the
verification repository. Inert under the revised fresh-per-run design, and
harmless as long as nothing enumerates refs there — but the proposal's structural
argument is stated as *"Git config does not travel over a fetch; objects do"*, and
**refs travel too**. Since the whole document's standard is that every sentence
names something the reader can run, and since the mktemp revision now depends on
the workspace being clean, this deserves accuracy: `--no-tags`, or a comment that
says what actually arrives.

---

### [I6] NIT — "96 rows" is the manifest's line count, not its row count.

Evidence item 9 says `python bootstrap/scaffold.py --manifest` *"emits **96
rows** (`as_of 2026-08-03`)"*. Measured today under the canonical interpreter:

```
all lines:        96
comment/header:   1
actual data rows: 95
```

Line 1 is `# Cairn install manifest (destination<TAB>source<TAB>verbatim|substituted)`.
The load-bearing half of that item is exactly right and I checked it: `grep -c
"PROVENANCE\|container"` over the manifest returns **0**, and the one
security-review row is present as `dev/modules/security-review.md	modules/team-gated/security-review.md	substituted`.
So the conclusion ("adds and removes no manifest row; changes one installed
file") stands. But this is the item the author flagged as *"I had this wrong in
an earlier draft of this document, which is why it is spelled out"*, which is
precisely why the count should be right.

---

### [I7] NIT — the adopter's release roster is given the same directory and file name as the internal roster the proposal forbids as an anchor.

Part A's block writes `~/.cairn/allowed_signers`. Cairn's internal gate roster is
`dev/.cairn/allowed_signers` — and in an adopter's tree, `dev/.cairn/` is the
installed Cairn state directory (`ls -a dev/.cairn/` shows `allowed_signers`,
`cairn-lock.yml`, `local-env.json`, `profile.yml`, …). The proposal's own words
are that the in-repository file *"is **never** consulted for release verification,
and there is **no fallback** to it."* Giving the two rosters an identical
basename inside identically-named directories is the drafting choice most likely
to produce exactly that fallback in a future skill, doc, or grep. Cheap fix:
`~/.cairn/release-signers` or `~/.config/cairn/release-signers`.

---

### Covered — each lens swept, with the command that proves it

* **Does the bootstrap break the circularity?** Rebuilt the hostile candidate
  (attacker key, in-tree roster naming the genuine principal, `.git/config`
  pointing at both it and a forging `gpg.ssh.program`) and ran the revised
  bootstrap with an execution witness: `git init --bare` + `git fetch
  refs/tags/v0.4.0:refs/tags/v0.4.0` + `git verify-tag -c
  gpg.ssh.allowedSignersFile=<trusted>` → `No principal matched.`, `rc=1`, witness
  file absent. **Yes, for key forgery.** Not for name substitution — [I1].
* **Lightweight tags.** `git tag lw-commit HEAD` then `git rev-parse --verify
  "refs/tags/lw-commit^{tag}"` → `error: … dereferences to tree type`, rc=128
  (correctly refused). `git update-ref refs/tags/v0.4.0 <tag-object-sha>` then the
  same resolver → rc=0 (**not** refused) — [I1]. Note also that rc=128 rather than
  the script's documented `1 = refused` needs an explicit `|| refuse` guard under
  `set -euo pipefail`; the shipped script already uses that pattern at lines 41-42.
* **Multiple tags on one commit.** Three tags built on one commit; caller-ref
  resolution returned `e4d52de4…` for `v0.3.0` and `6958cd08…` for `v0.3.0-alt`
  (correct), while `git describe --exact-match --tags <commit>` returned
  `v0.3.0-alt` (the defect Part B removes). Reproduces the proposal's Limb 2.
* **Abbreviated SHAs.** Reproduced the current defect against an attacker-authored
  unsigned commit via `HEAD`, the full SHA, and the 4-character prefix `8231` —
  all three print `Maintainer-approved commit`, rc=0. The proposed refusal follows
  mechanically from the `^{tag}` resolver, which I confirmed fails on non-ref
  inputs.
* **Roster boundaries — empty, keyless, missing, directory.** All four refuse:
  `empty_signers -> rc=1`, `keyless_signers -> rc=1` (`missing key`),
  `does_not_exist -> rc=1`, directory-as-roster → rc=1; genuine roster → rc=0.
  Every one printed a line beginning `Good "git" signature` while exiting 1,
  confirming the proposal's evidence item 8 and its "judge the exit code, never
  the text" rule. The `$CAIRN_KEY`-unset copy-paste failure lands on the
  `keyless_signers` case and therefore fails closed.
* **Refspec metacharacters** (distinct from the shell metacharacters the edge-case
  list names). `REF='*'` produces the valid refspec `refs/tags/*:refs/tags/*` and
  fetches every tag; `verify-tag '*'` then cannot resolve, so it fails closed.
  Worth one line in the edge-case list, not a finding.
* **Part D rotation.** `valid-before="20230101"` roster: 2021-dated tag rc=0,
  today-dated tag rc=1 — enforced against the tagger timestamp, as claimed. Also
  observed directly in the args git passes the signer program
  (`-Overify-time=20260803170224`).
* **The External review's exhibits vs the Response's corrections.** [G1]
  reproduced verbatim including the SHA. [G2]'s conclusion reproduced; the
  Response's correction (stderr forger → rc=1, stdout forger → rc=0) reproduced in
  both directions. [G3]: `grep -c "signers\|allowedSigners\|verify-tag\|gpg\."`
  over the shipped script is 0, and the script is 71 lines — the Response's
  characterisation is right.
* **Bookkeeping claims.** `shasum -a 256` byte-parity of the two module copies;
  `sed -n '169p'` and `sed -n '62p'` on the module; `sed -n '225p'` on
  `bootstrap/UPGRADE.md`; `scaffold.py --manifest` row inspection;
  `bootstrap/tests/fixtures/gate_manifest.json` `frozen_files` length at the
  proposal's own commit (162) and at HEAD (164 — the same-day drift is `e45e1fc`,
  not an error in the proposal, but it shows day-granularity `as_of` is coarse for
  this figure); `FROZEN-NEW` semantics at `bootstrap/tests/_gate_manifest.py` line
  366.
* **Sibling-proposal collision.** `grep -n "security-review"` over
  `dev/proposals/2026-08-03-claude-gate-claims-vs-enforcement.md` returns exactly
  one citation, at line 62 of the template twin, and line 62 is inside the "wire a
  linter" paragraph. The claimed non-overlap holds.
* **Vacuity sweep over the proposed test list.** Found [I2]. The
  `gpg.ssh.program` test is already protected by the Response's stdout/executed
  instruction; the back-dating test is a deliberate residual pin and can fail if
  git changes; the multi-tag test can fail. The `Maintainer-approved` grep test is
  correctly scoped away from append-only history.

### Not covered / low confidence — the negative space

* **This review has no cross-type independence, and that is a structural limit,
  not a caveat.** The author is Claude and I am Claude, in a fresh session. This
  is an *Internal* read under Cairn's own definition and it cannot substitute for
  the `required(External, security lens)` tier the superseding Decision mandates.
  The specific risk is shared blind spots: I found [I1] by asking "what else can a
  ref point at", which is the same *class* of question the author was already
  asking. Whatever question neither of us thought to ask is still unasked.
* **Neither of the proposal's two mandates to the plan reviewer was run here.** I
  did not name the arrival channel of every input to every verification step, and
  I did not sweep Cairn's other `git` invocations against trees it does not
  control. RA5 does not narrow on this pass.
* **No git other than 2.53.0 was tested**, so the version-fragility of
  `valid-before` / tagger-timestamp verify-time remains unmeasured, as the
  proposal's known omission (b) already says.
* **Nothing network-side was checked** — the forge's SSH *signing*-key endpoint,
  ORCID, and Zenodo. That is Part E step 1 and remains the single most likely
  factual correction, exactly as the proposal predicts.
* **Not swept**: hardlink or TOCTOU evasion of the roster-containment check
  (containment is a path property; a hardlinked or concurrently-rewritten roster
  is a content property). I did not build this and have no evidence it is
  reachable in practice — flagged only so it is not mistaken for covered.
* **Not swept**: SHA-256 repositories, non-UTF-8 principals, concurrent rotation,
  and TLS-intercepting proxies — all four are already declared out of scope.
* **[I1]'s exploitability depends on a threat model I did not test end to end.**
  I demonstrated the ref manipulation on a bare clone, which is the shape a forge
  serves; I did not verify that a particular forge's push rules accept a tag ref
  pointing at a tag object of another name. If a forge rejects it, [I1] narrows to
  hostile mirrors, typosquats, and local candidates — which the container recipe
  and `verify-ref.sh` both accept as inputs, so it does not narrow to zero.

### Second-round recommendation

**Recommended, and scoped.** Not a full re-review — the structural design, the
channel model, Part C, Part D and Part E all survived this pass and re-reading
them would spend attention this repository is trying to conserve.

The second round should be **[I1] only, and it should be External**. Three
reasons. It is a defect in the mechanism the superseding Decision bound as
settled design, so it cannot be pushed to the plan the way a test-shape question
could. It is the fourth instance of one failure shape in a single week — [CR1],
[IDN1], the `gpg.ssh.program` vector, and now this — which is the pattern the
proposal itself cites as evidence that same-agent vigilance has a demonstrated
failure rate; I am the same agent. And the fix I verified is a two-line addition
whose correctness is exactly the kind of claim that ought to be checked by someone
who did not write it, especially since it is a *name-comparison* fix and
name-comparison spoofing is scope 2's entire subject.

[I2] through [I4] can be dispositioned in a Response without a further pass;
[I5] through [I7] are drafting.

One process note: **[I1] should not be closed by an append that asserts the fix
without re-running the substitution attack.** The exhibit above is four commands
and reproduces in under a minute; a Response that reproduces it and then shows it
refusing is the right shape, and it is the shape this lifecycle has repeatedly
shown to be necessary.

## Revised proposal (second revision) -- 2026-08-03

**Scope of the revision: [I1] is right, the settled design is wrong on the row it
names, and the fix is verified here rather than asserted.** Part A's command block
and Part B's resolver both change; the class table gains a row and loses a false
premise; `bootstrap/container/acceptance.sh`'s negative pins are re-specified so
they can fail; one residual is re-marked; two drafting defects are fixed. The
trust model does not move — fingerprint compared out of band on two channels,
roster written by the adopter, verification performed outside the candidate's git
context. Parts C, D and E are untouched, no residual is retired, and no gate
accounting changes.

The per-finding dispositions are in the Response below this section. This section
is the design delta only.

### The correction [I1] forces, and the reproduction that earns it

I rebuilt the substitution attack from scratch before touching the design —
throwaway repositories under the session scratch directory, freshly generated
throwaway SSH keys, git 2.53.0, `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM`
neutralised to empty files. No key material belonging to the Maintainer was used
and nothing was written into the Cairn tree.

An attacker with write access to the forge and **no signing key** re-points a new
version name at an old genuinely-signed tag object:

```
$ git clone -q --bare "$LAB/cand" "$LAB/mirror"
$ git -C "$LAB/mirror" update-ref refs/tags/v0.5.0 \
      "$(git -C $LAB/cand rev-parse refs/tags/v0.3.0)"

=== the adopter runs the documented bootstrap, asking for v0.5.0 ===
$ git -C "$V/verify.git" fetch "$LAB/mirror" 'refs/tags/v0.5.0:refs/tags/v0.5.0'
fetch rc=0
$ git -C "$V/verify.git" -c gpg.ssh.allowedSignersFile="$LAB/trusted_signers" \
      verify-tag v0.5.0
Good "git" signature for maint@example.org with ED25519 key SHA256:B8EwbahZ5sIB…
verify-tag rc=0
$ git -C "$V/verify.git" rev-parse --verify 'refs/tags/v0.5.0^{tag}'
09ba835c06848e2a207df1bf5cc530a6675e4eab        # the Part B resolver agrees
$ git -C "$V/verify.git" cat-file tag v0.5.0
object 49bce222f3c28b92369299a8a47dadf4487a81fa
type commit
tag v0.3.0                                      # the signed payload
```

The adopter asked for `v0.5.0`. The signature is genuine. The signed name is
`v0.3.0`. Exit code 0. There is no cryptographic failure anywhere in that
transcript, which is exactly why the design missed it.

**No defence of the original.** The glossary sentence *"a lightweight tag — not an
object: just a name pointing straight at a commit"* is false, the class-table row
it produced is wrong, the stated invariant *"The caller's ref is the ref
reported"* does not hold as specified, and the instruction *"Judge the EXIT CODE,
never the text"* points the adopter away from the only place the real name
appears. Four sentences of my own document, each wrong in the same direction.

### The fix, and every check I could think to run against it

The binding rule: **resolve the caller's ref to one object id, require that
object's signed `tag` header to equal the ref the caller asked for, and verify
that object id — not the ref name.** Resolving once and then verifying the
resolved object closes the gap between "what was name-checked" and "what was
signature-checked"; the reviewer's sketch verifies the ref name and name-checks
the object, which is one indirection short.

Verified, in the same lab, on the same objects:

```
--- (a) the substitution attack ---
REFUSED: ref 'v0.5.0' resolves to a tag object whose SIGNED name is 'v0.3.0'
rc=1
--- (b) the honest case must still pass ---
PROVENANCED: tag 'v0.3.0' (object 09ba835c…) signed and name-bound
rc=0
--- (c) honest tag, wrong roster -- the name check must not mask the crypto check ---
REFUSED: signature on 'v0.3.0' did not verify against the trusted roster
rc=1
--- MUTATION: delete the name-binding line, replay (a) ---
PROVENANCED: tag 'v0.5.0' (object 09ba835c…)
mutant rc=0        # the negative test discriminates
```

Case (c) and the mutation are the two that matter. (c) shows the new check has
not become the *only* check; the mutation shows the new test fails when the new
control is removed, which is the property `bootstrap/container/acceptance.sh`'s
pins turn out not to have (finding [I2], below).

**Four attacks on the fix itself**, because a two-line security addition verified
only against the attack that motivated it is how this lifecycle got here:

* **Nested tag wrap — the obvious keyless next move.** An attacker needs no key
  to write an *unsigned* tag object named `v0.5.0` whose target is the genuine
  signed `v0.3.0` tag object. Built it with `git hash-object -t tag -w`. Measured:
  `^{tag}` does **not** peel through — it returns the outer object — so the name
  check passes (the outer really is named `v0.5.0`) and the **signature** check
  refuses (`error: no signature found`, rc=1). Refused, but refused by the other
  half of the pair. Both halves are load-bearing; neither alone is sufficient.
* **Header/body confusion.** A genuine signed tag whose message body contains a
  line beginning `tag `. The reviewer's parse (`awk '/^tag /{print $2; exit}'`)
  reads the header first here and is correct on this input — but on a tag object
  with no `tag` header it walks into the body and returns a body string as the
  signed name. Measured, both forms, same input. The specified parse is therefore
  **header-bounded** — `awk 'NF==0{exit} /^tag /{print $2; exit}'` — plus an
  empty-result refusal. Not attacker-reachable that I can see (forging a
  header-less tag object still needs the signing key), so this is hardening, not
  a second finding.
* **Slash-namespaced tag names.** `release/v0.7.0` signs and name-binds
  correctly; the comparison is on the full ref name, not a basename.
* **Lightweight tag straight to a commit** — the row the class table was trying
  to describe. Still refused, at the resolver.

**One implementation detail the reviewer's coverage note gets backwards, and it
matters under `set -euo pipefail`.** The reviewer records rc=128 from the
resolver and asks for an explicit `|| refuse` guard. Measured: *without*
`--quiet` the exit code is 128; *with* `--quiet` it is 1. Both still print to
stderr, so the shipped script needs `--verify --quiet … 2>/dev/null` **and** the
`|| refuse` guard — the guard because rc must be translated to the script's
documented `1 = refused` regardless, and `2>/dev/null` because `--quiet` does not
suppress the `dereferences to tree type` line.

### What changes in the shipped artifacts

**Part A's adopter block** gains the resolve-and-name-bind pair, and the whole
block is re-specified so every step's exit code is judged:

```sh
# 0. Anchor: the roster you wrote from the fingerprint you compared on two channels.
mkdir -p ~/.config/cairn
printf '%s %s\n' "$CAIRN_SIGNER" "$CAIRN_KEY" > ~/.config/cairn/release-signers

# 1. A FRESH, THROWAWAY verification workspace.
V="$(mktemp -d)" && git init -q --bare "$V/verify.git"        || echo REFUSED

# 2. Fetch exactly the one ref you asked about, and nothing else.
git -C "$V/verify.git" fetch --no-tags <cairn-url> \
    "refs/tags/$REL:refs/tags/$REL"                            || echo REFUSED

# 3. Resolve the caller's ref to ONE tag object id.
OBJ="$(git -C "$V/verify.git" rev-parse --verify --quiet \
       "refs/tags/$REL^{tag}" 2>/dev/null)"                    || echo REFUSED

# 4. NAME BINDING: the name inside the signed payload must be the release you asked for.
NAME="$(git -C "$V/verify.git" cat-file tag "$OBJ" \
        | awk 'NF==0{exit} /^tag /{print $2; exit}')"
[ -n "$NAME" ] && [ "$NAME" = "$REL" ] || echo "REFUSED: '$REL' is signed as '$NAME'"

# 5. Verify THAT OBJECT ID -- not the ref name -- against YOUR roster.
git -C "$V/verify.git" \
    -c gpg.ssh.allowedSignersFile="$HOME/.config/cairn/release-signers" \
    verify-tag "$OBJ"                                          || echo REFUSED

rm -rf "$V"
```

Three smaller changes ride in that block and are called out so they are not read
as incidental: `--no-tags` (finding [I5]); `~/.config/cairn/release-signers`
rather than `~/.cairn/allowed_signers` (finding [I7]); and **the block is no
longer given a name that counts its commands.** It was "the three-command
bootstrap", then "four commands" after the first revision, and would now be six.
A prose count that has to track a code block is a drift surface that has already
drifted twice in one document; the text says *"the bootstrap block"* and the
count lives nowhere.

**`bootstrap/container/verify-ref.sh`** inherits the identical resolve → name-bind
→ verify-the-object sequence, because it inherits the resolver that had the
defect.

**Part B's class table** — the lightweight row is rewritten and a row is added:

| Input | Provenance mode | Why |
|---|---|---|
| tag ref whose object is an annotated tag object **signed under a different name** | **REFUSED**, naming both the asked-for name and the signed name | the release you asked about is not the release that was signed; no key is needed to construct this |
| tag ref resolving to a non-tag object (a commit, a tree) | REFUSED | not an object that can carry a signature |
| tag ref resolving to an **unsigned** tag object, including one wrapping a signed tag object | REFUSED | the name may bind and still carry no signature; both checks run |

The retired row said *"lightweight tag → REFUSED … not an object"*. The refusal is
by **object type and signed name**, never by "tag class" — at the ref level there
is no such thing as a lightweight tag, only a ref and whatever object it points
at. The glossary entry is corrected to say that.

**Part D is not re-opened, but its limit widens by one sentence.** Substitution
reuses the old object with its old tagger timestamp, and `valid-before` is
evaluated against that timestamp, so before this fix a rotated-out key's releases
stayed substitutable indefinitely. That is adjacent to residual RA2 and is not
RA2 — RA2 needs the compromised key, this needed none. The name binding closes
it; the sentence records that it was open.

### `bootstrap/container/acceptance.sh` — all five call sites, and pins that can fail ([I2])

The proposal said *"that call site is updated in the same change"*, singular.
There are five, and the split is the finding. I replayed the negative ones
verbatim against a stub implementing only *"provenance mode refuses anything that
is not an annotated tag"*, with the branch guard and the dirty/untracked
build-surface check **deleted entirely**:

```
=== replaying acceptance.sh lines 81 and 84 verbatim against the STUB ===
  LINE 81 PASSES -- but the dirty check does not exist in this stub
  LINE 84 PASSES -- but the dirty check does not exist in this stub
=== replaying line 62 (the Codex S5 branch pin) verbatim against the STUB ===
  LINE 62 PASSES ('refuses branch master') -- but the branch guard does not exist
```

Line 55 and line 79 are `|| fail` and break loudly. Lines 62, 81 and 84 are
`&& fail` / `if … then fail` and pass on **any** refusal — so once provenance
mode is the default, all three go green against a script with both controls
removed. `bootstrap/container/verify-ref.sh` lines 31-39 (the branch guard) and
lines 62-71 (the dirty-surface guard) could be deleted wholesale and the harness
would still report `ok`.

Four changes, and the third is the one that generalises:

1. All four no-ref call sites plus the branch pin pass `--unprovenanced`.
2. `--unprovenanced` gets its **own exit code (3)** for the accepted-but-not-
   provenanced outcome. Today `PROVENANCED` and `NOT PROVENANCED` would both exit
   0 and no caller could tell them apart; a distinct code makes the pins
   self-discriminating without any assertion changes at all. This is an addition
   to the script's documented exit contract (`0` verified / `1` refused / `2`
   usage), so it is named here rather than left to the plan.
3. **Every negative assertion asserts on the refusal *reason*, not the exit
   code** — the dirty pin must match `uncommitted or untracked`, the branch pin
   must match `mutable branch`. In the stub above the refusal reason reads
   `'HEAD' is not a signed annotated tag`, which is what a reason-matching
   assertion would have caught and an exit-code assertion did not.
4. *Tests required* gains a row: **replay each negative pin against a stub with
   the named control deleted and assert the pin fails.** That is the shell-harness
   analogue of the mutation discipline the proposal already adopts for the pytest
   module, and its absence is precisely why this defect was reachable — the
   mutation rule was scoped to `bootstrap/tests/test_verify_ref.py` and a shell
   harness is not a pytest module.

**This is an instance of a class, not an isolated slip.** The same shape was
measured elsewhere in this repository today: the regression test that names itself
*"the anti-drift assertion"* at `bootstrap/tests/test_security_lint.py` derives
its expected set from the same object the code under test walks, so it cannot
fail — and it was green throughout the period the drift it names was occurring
(see the `scan-coverage` proposal). Two instances, two surfaces, one shape: **an
assertion whose oracle stops discriminating while its name goes on claiming
otherwise.** Naming it as a class is not scope creep here — it is the reason
change 4 above is a stated requirement rather than a note.

**Second-order, and accepted rather than fixed here.** With `acceptance.sh`
permanently in `--unprovenanced` mode, Cairn's own end-to-end harness never
exercises the provenance path — the harness smoke-checks the mode this scope did
not add. The honest fix is a fixture: a throwaway signed tag and roster built by
the harness itself, exercising the provenance path end to end. That is one added
`bootstrap/tests/test_verify_ref.py` node, not a change to `acceptance.sh`, and
it is added to *Tests required*. `acceptance.sh` stays `--unprovenanced` because
a live development checkout legitimately has no signed tag.

### The other four deltas

* **[I3] — residual RA1 (a) is re-marked non-mechanical, and a mechanical
  tripwire is added on Cairn's own side.** The adopter-side principal-count
  warning stays (it is useful adopter hygiene) but it is no longer claimed as a
  posture-expiry trigger for Cairn: it counts principals in a file the *adopter*
  typed, it lives in the script Part C demotes to a convenience, and it has no
  channel back to Cairn. The genuinely mechanical replacement is a suite
  assertion over `dev/.cairn/allowed_signers` — 1 principal, `as_of 2026-08-03` —
  that fails when Cairn's own signing authority widens. That fires in Cairn's
  suite, where Cairn will see it.
* **[I4] — the documented-path test's form is decided here, not deferred.** It
  **extracts the command block from `bootstrap/PROVENANCE.md` and runs it**. The
  deferral said the choice had "no security content"; the first revision then
  demonstrated that the defect *was in the document text*, and a test running a
  private copy of the sequence cannot see that. The constraint, stated so the plan
  cannot satisfy it cheaply: the test must fail when the document's block changes
  in a way that breaks the procedure.
* **[I5] — `--no-tags`.** Measured: the documented fetch brought four refs into
  the workspace when one was asked for, three of them named by the candidate;
  `--no-tags` brings exactly one. I could not construct a bypass from the extra
  refs and do not claim one. It is adopted because the [I1] fix now *reads a ref
  out of that workspace*, and a workspace containing only what was asked for is a
  precondition worth having by construction rather than by argument.
* **[I6] — 95 rows, not 96.** Re-measured under the canonical interpreter
  (`~/conda_envs/lhm/bin/python`, 3.13.13): 96 lines, 1 comment header, **95 data
  rows**, `as_of 2026-08-03`. The load-bearing half is unchanged and re-checked:
  0 rows match `PROVENANCE` or `container`, and the one `security-review` row is
  present. Evidence item 9's conclusion stands; its count did not.
* **[I7] — `~/.config/cairn/release-signers`.** `dev/.cairn/` is a real installed
  state directory in an adopter tree (it holds `allowed_signers`,
  `cairn-lock.yml`, `local-env.json`, `profile.yml` and more), so giving the
  release roster the same basename in a same-named directory is an invitation to
  the exact fallback Part A forbids. Different directory, different basename.

### The acceptance specification — what "done" means for this contract

This is the part of the revision that is not a fix, and it is here because
four rounds of review on this scope have each found one more property and moved
the horizon by exactly one step. Every gate applied to this proposal so far has
been **diagnostic** — it says *this is wrong* — and none has been
**specificational** — none says *here is the complete set of properties this must
satisfy*. Without the second kind there is no principled place to stop.

So: a verification step in this scope is correct **iff** it satisfies all five
properties below. Each is stated as a property, each names the measured failure
that put it on the list, and each is checkable against a step by reading it.

| # | Property | The measured failure that put it here |
|---|---|---|
| **P1** | **Anchor independence.** No input to a step is supplied by the artifact under verification — and "input" includes the roster, the verifier program, the git config that selects either, and the workspace the step runs in. | the pre-flight checker resolving its roster through the candidate's `.git/config` (fixed at `0c6d9de`); [IDN1]'s in-repo roster; the `gpg.ssh.program` vector |
| **P2** | **Question fidelity.** The caller's ref, the ref resolved, the name inside the signed payload, and the object the signature was checked over are all the same thing. | `git describe` label substitution ([IDN2] limb 2); the tag substitution in [I1] |
| **P3** | **Oracle discrimination.** Every assertion — in the script, in the shell harness, in the suite — fails when the control it names is deleted. A negative assertion that passes for any refusal reason is not a control. | `acceptance.sh` lines 62, 81 and 84 ([I2]); the sibling instance at `bootstrap/tests/test_security_lint.py` |
| **P4** | **Statelessness.** Nothing persists between runs of a verification. The durable object is the anchor; the workspace never is. | the fixed `~/.cairn/verify.git` false pass, found in the first revision |
| **P5** | **Claim ≤ evidence.** No output label, document sentence, or residual marking asserts more than was actually checked. | `Maintainer-approved commit` on an unsigned attacker commit; `OK — release tag` on an unsigned tag; RA1 (a) marked mechanical ([I3]) |

**The stopping rule.** A future finding on this scope is one of exactly two
things. Either it names a **violation of P1–P5** — then it is a bug against a
stated property and the fix is bounded. Or it names a **property not in P1–P5** —
then the specification was incomplete, the property is added, and **every earlier
step is re-swept against the new property**, not just the one the finding landed
on. The second branch is the expensive one and it is supposed to be: it is the
only branch that makes the list converge.

Applied to this round as a check that the list is not post-hoc padding: [I1] is
P2. [I2] is P3. [I3] is P5. [I4] is P3 (a drift oracle that cannot see the drift).
[I5] is P1 and P4. [I7] is P1 (a naming choice that invites the forbidden
fallback). [I6] is none of them — it is an arithmetic error, and it should not
have a security property, which is the correct answer for a count.

**What the specification does not establish, stated plainly.** P1–P5 are
*derived from failures observed in this repository*. They are a floor, not a
completeness proof, and nothing here shows a sixth property does not exist — the
[I1] round is itself evidence that it might. What they buy is narrower and still
worth having: a reviewer can now report *"P1–P5 all hold, and here is the command
for each"* and that is a stopping point, where before there was only "nothing
found this time." They also do not generalise beyond this scope; whether they are
the right properties for Cairn's other verification surfaces is not claimed, not
tested, and not proposed here.

### What this second revision does not establish

It closes one substitution path in one procedure and one vacuity class in one
harness. It does not show that P2 now holds everywhere in the document — I found
[I1] in the resolver *after* the first revision found the same shape in the
workspace, which is two instances of P2 surviving a fix aimed at P2. It does not
narrow residual RA5. It does not touch the network-side facts in Part E. And the
fix's correctness rests on my own lab: six attacks, one mutation, one positive
control, all run by the author of the fix.

---

## Response -- Claude (author, to Internal Security Review) -- 2026-08-03

**Model**: Claude Opus 5. Proposal-Response grammar (no implementing commits
exist).

[I1] is correct, it is mine, and the design it breaks is the design the
superseding Decision bound as settled. Everything below was re-run from scratch
before it was dispositioned — throwaway repositories in the session scratch
directory, freshly generated throwaway SSH keys, git 2.53.0, `GIT_CONFIG_GLOBAL`
and `GIT_CONFIG_SYSTEM` neutralised. Nothing was written into the Cairn tree and
no key material belonging to the Maintainer was used.

* **[I1] accept -- reproduced before, fixed, and reproduced after.** The
  substitution attack is exactly as reported: a bare clone, one `update-ref`, and
  the documented bootstrap returns exit 0 on a genuine maintainer signature over
  a payload that says `tag v0.3.0`. No key is required. The transcript and the
  verified fix — including the honest case, the wrong-roster case, the mutation,
  and four attacks on the fix itself — are in the second revision above. Two
  points where I did not simply take the recommended fix: the signature check
  binds to the **resolved object id** rather than the ref name, closing the gap
  between what is name-checked and what is signature-checked; and the payload
  parse is **header-bounded**, because the unbounded form reads a message-body
  line as the signed name on a header-less object (measured, both forms). The
  reviewer's process note is also accepted on its own terms and is the reason
  this disposition is a transcript rather than an assertion.

* **[I2] accept with modification -- and it is an instance of a class this
  repository measured twice today.** All three negative pins go green against a
  stub with both named controls deleted; I built the stub and replayed lines 62,
  81 and 84 verbatim rather than reasoning about them. The modification is that
  the reviewer's suggested fix (assert on the refusal reason) is adopted **and**
  paired with two things it does not cover: a distinct exit code 3 for the
  unprovenanced path, so the pins discriminate without depending on message text
  at all; and a *Tests required* row extending the mutation discipline to the
  shell harness, since scoping that discipline to the pytest module is what made
  this reachable. The class framing is deliberate — the same shape sits in
  `bootstrap/tests/test_security_lint.py`, green while the drift it names
  occurred — and it is why P3 is a stated property in the specification above
  rather than a lesson in a Response.

* **[I3] accept with modification.** All three of the reviewer's facts hold, and
  I checked the load-bearing one: `dev/.cairn/allowed_signers` carries exactly 1
  principal (`as_of 2026-08-03`), and this design forbids consulting it for
  release verification. The modification is that I take *both* branches the
  reviewer offers rather than choosing: RA1 (a) is re-marked **non-mechanical**
  with a `dev/PLANNING.md` home, *and* a genuinely mechanical tripwire is added
  over Cairn's own roster in Cairn's own suite. Taking one branch leaves either a
  useful adopter warning deleted or a residuals table that still overclaims; the
  two branches are cheap and they are not substitutes.

* **[I4] accept.** The deferral said the choice had no security content; the
  first revision then proved the defect lived in the document text. The form is
  decided in the revision above — extract the block from
  `bootstrap/PROVENANCE.md` and run it — with the constraint that the test must
  fail when the block changes in a way that breaks the procedure. The reviewer is
  also right about the append-only point: the original bullet stays as written
  and this correction is a later section, which is why it appears above rather
  than as an edit.

* **[I5] accept.** Measured: four refs arrive when one is asked for, three named
  by the candidate; `--no-tags` brings exactly one. I could not construct a bypass
  from the extra refs and do not claim one — but the [I1] fix now reads a ref out
  of that workspace, which promotes this from a wording accuracy point to a
  precondition. The proposal's structural sentence *"Git config does not travel
  over a fetch; objects do"* is corrected to say that refs travel too.

* **[I6] accept.** 96 lines, 1 comment header, 95 data rows, `as_of 2026-08-03`,
  re-measured under the canonical interpreter. The conclusion the item exists to
  support is re-checked and unchanged (0 rows matching `PROVENANCE` or
  `container`; the one `security-review` row present). The reviewer's sting is
  fair: this is the item I flagged as previously wrong, which is the item that
  should have been counted rather than recalled.

* **[I7] accept.** `dev/.cairn/` is a real installed state directory holding a
  file of exactly that basename. Changed to `~/.config/cairn/release-signers`.

**On the review's negative space.** Four of the seven items are already carried
and create no new obligation (the git-version floor, the network-side channel
checks, the four declared out-of-scope classes, and the unrun plan-reviewer
mandates). Two are new and I am recording them rather than absorbing them: the
**hardlink / TOCTOU** angle on the roster-containment check — containment is a
path property and a hardlinked or concurrently-rewritten roster is a content
property — and the **refspec-metacharacter** observation, which the reviewer
correctly judges fails closed. The first is a genuine gap in an existing control
and I am not fixing it in this revision, because it belongs to the containment
check's own design rather than to [I1]; it goes to the External round's brief
below with that framing. The second becomes one line in the edge-case list.

**On [I1]'s threat model, where the reviewer's own caveat is right.** I did not
test any real forge's push rules either. If a forge rejects a tag ref pointing at
a tag object of another name, [I1] narrows to hostile mirrors, typosquats and
local candidates — all three of which `verify-ref.sh` and the container recipe
accept as inputs, so it does not narrow to zero. The fix costs two commands and
does not depend on which way that resolves, so I did not make it conditional on
finding out.

### On the second-round recommendation — I agree, and I would tighten the brief

The reviewer recommends a second round that is **External** and **scoped to [I1]
only**, on three grounds: [I1] is a defect in design the Decision bound as
settled; it is the fourth instance of one shape in a rolling week; and the
reviewer is the same agent type as the author. I accept all three, and the third
is the one I would underline — I wrote the fix, I designed the six attacks I ran
against it, and I chose which four to run. A clean result from that setup is
weaker evidence than it looks.

Two amendments, both widening the brief slightly rather than narrowing it:

1. **Scope it to [I1] *and* the acceptance specification, not [I1] alone.** [I1]
   is now two lines of shell whose correctness an External reviewer can check in
   minutes. The more valuable question is whether P1–P5 are the right five and
   whether any step in Parts A and B violates one of them — that is a bounded,
   falsifiable sweep, and it is the first review pass on this scope that could
   come back with a *positive* answer rather than "nothing found this time."
   Concretely: for each verification step, name its inputs and their arrival
   channels (P1), show the four names in P2 coincide, and name the deletion that
   would make each assertion fail (P3).
2. **Add the hardlink / TOCTOU question to the brief**, since it is the one new
   gap this round surfaced and did not close, and it is exactly the kind of
   content-vs-path distinction a fresh adversarial reader lands and an author
   re-reading his own containment check does not.

I do **not** propose folding in the two plan-reviewer mandates (channel discipline
over every step, and the RA5 sweep of Cairn's other `git` invocations). The first
is now largely P1 restated and the External round will exercise it; the second is
a different surface and folding it in would turn a scoped round into a broad one.
RA5 does not narrow on this round either.

### Decisions this Response cannot make

Three judgments belong to the Maintainer. Each has a recommendation and the exact
wording that would settle it, so none is left open.

* **MD-1 — Is correcting Part B a departure from the superseding Decision?** The
  Decision bound [IDN1] and [IDN2] to be resolved at proposal time rather than
  deferred to the plan. [I1] says the [IDN2] limb-2 resolution was incomplete, and
  the correction lands at proposal time. **My reading: this is compliance with
  that binding, not a departure from it** — the alternative, shipping a resolver
  known to be wrong on one row, is what the binding exists to prevent. It is
  recorded as a decision anyway because a reader could reasonably see bound design
  moving. *What settles it:* Confirmed: correcting Part B's resolver
  and class table at proposal time is compliance with the supersession's binding,
  not a departure from it. No ratification needed.

* **MD-2 — The second round.** Recommended: **External, scoped to [I1] plus the
  P1–P5 sweep and the hardlink/TOCTOU question**, per the section above. The
  reviewer recommended External-and-scoped and I agree; the scope is slightly
  wider than they proposed and the reasons are stated. *What settles it:* Run one more round: External, security lens, scoped to [I1], the P1–P5
  sweep over Parts A and B, and the hardlink/TOCTOU question on the
  roster-containment check. Not a full re-review. This does not discharge the
  plan's `required(External, security lens)` tier."** *If you would rather keep
  the reviewer's narrower scope:* **"Second round: External, [I1] only, as the
  Internal reviewer recommended."*

* **MD-3 — Residual RA1's disposition change.** The superseding Decision's
  condition 2 has the Decision ratify each residual's expiry trigger, and this
  revision re-marks RA1 (a) from mechanical to non-mechanical and adds a new
  mechanical trigger over `dev/.cairn/allowed_signers`. That is a change to a
  ratified-at-Decision item. *What settles it:* Ratified: RA1 (a) is
  non-mechanical with a `dev/PLANNING.md` home, and the new mechanical trigger is
  the suite assertion over Cairn's own roster.

The Class C disposition recorded earlier in this proposal is **unchanged** by this
revision and still awaits the Maintainer's choice among its three options; nothing
here re-opens or re-argues it.

**Status.** `revised` -> **`revised`** (unchanged; the second revision above is
appended to the same status). The BLOCKING finding is closed in the document, and
closed with a reproduction in both directions rather than an assertion. Whether it
is closed *well enough to accept* is the second round's question and then the
Maintainer's, not this Response's.

## Decision -- Anthony Kendall (Maintainer) -- 2026-08-03

**Accepted, as revised.** Scribed by Claude (Strategy) at the Maintainer's
explicit instruction.

**Maintainer's authorization (verbatim):**

> I approve each of the seven proposals that you have listed as ready to accept,
> as revised.

The seven were presented as a ledger with a per-proposal recommendation; this is
one of them. The authorization is quoted rather than paraphrased, per the
scribing guard-rail: a paraphrase admits semantic drift, condition-softening, or
a hallucinated approval.

**Scribe-coupling disclosure.** The scribe is the proposal's author. That is the
weaker configuration -- the party whose work was reviewed transcribes the ruling
on it. Mitigations: the authorization is quoted verbatim, and this commit carries
the Decision only.

**A condition carried from the recommendation, flagged for confirmation.** The
ledger entry the Maintainer approved read *"Accept, conditioned on a scoped
External round for the tag-substitution fix only."* That condition is recorded
here as adopted, because it was part of the item approved -- but the Maintainer's
quoted words say "as revised" and do not name it. **If an unconditioned accept
was intended, the condition is theirs to strike in one line.** The scribe records
it rather than silently dropping or silently imposing it.

The finding it guards is the fourth instance of one failure shape in a week, and
the Internal reviewer who found it is the same agent type as the author.
