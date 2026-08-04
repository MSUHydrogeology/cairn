<!-- cairn-internal-ref-allow: doctrine/plans.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- The test module is a forward reference registered under `Proposed paths`; the
     marker exempts only its own contiguous block, and the file table rows cite it
     many sections later, so it needs the file-scoped directive too.  Drop this
     directive once the path lands (Chunk A), per the marker discipline. -->
<!-- claim-check-allow: bootstrap/tests/test_verify_ref.py -->

# Plan: release authenticity — a public trust root before v0.4.0 mints a DOI

**Source proposal**: `release-authenticity` (accepted 2026-08-03; the Decision
commit is `a08ead8`). It currently sits under `dev/proposals/` and moves to
`dev/proposals/archive/` when it archives.
**Status**: open
**Plan review**: required(**External**, security lens) — carried from the
proposal header, mandated by the superseding `identity-not-name` Decision, and
**not** discharged by the External round the proposal already had. **No
implementation commit lands before the `## Plan review` section is in the tree.**
**Last update**: 2026-08-03
**Opened**: 2026-08-03

## Source proposal

`release-authenticity` is scope 1 of the superseded `identity-not-name`
proposal. It establishes one contract: **an adopter can establish, from outside
the artifact, that a Cairn release was signed by Cairn's maintainer — and Cairn
never claims provenance it did not check.** It went through an External security
review (SHIP), an author Response that corrected one of that review's exhibits,
an author-initiated revision, an Internal security review with one BLOCKING
finding, a second revision, and a Response. The Decision accepted it *as
revised*.

The proposal settles the design. This plan executes it and does not re-litigate
it. Five parts, in the proposal's own lettering:

* **Part A** — the out-of-band trust bootstrap: the signing key's fingerprint is
  published on channels independent of the release artifact, the adopter
  compares it on at least two, writes a roster themselves, and verifies with
  system `git` in a throwaway workspace the adopter created.
* **Part B** — exact annotated-tag resolution and honest output labels: the
  caller's ref is resolved to one tag object, that object's *signed* name must
  equal the ref asked for, and the signature is checked over that object id.
* **Part C** — `bootstrap/PROVENANCE.md` reconciled to what is actually
  enforced, including retiring the unenforceable "maintainer-authored commit on
  the protected default branch" branch of the stated control.
* **Part D** — key distribution and rotation, including the honest limit that
  OpenSSH validity windows are hygiene, not revocation.
* **Part E** — the v0.4.0 handoff, which is **the Maintainer's and no
  implementing agent's**.

### Glossary — every term glossed on first use

The audience is a scientist who codes, and this scope is jargon-dense.

* **Annotated tag** — a real git object with an author, a date, a message, and
  optionally a signature (`git tag -a` / `git tag -s`). It has its own object
  id, distinct from the commit it points at.
* **Tag *ref*** — the *name* `refs/tags/<something>`. A ref can point at any
  object: a commit, or an annotated tag object. "Lightweight tag" is the
  informal name for a ref pointing straight at a commit — but at the ref level
  there is no tag *class*, only a name and whatever object it points at. That
  distinction is the whole of the finding below.
* **`allowed_signers` (a "roster")** — an OpenSSH text file, one line per key,
  of the form `principal <keytype> <key>`. It answers "whose signatures count?"
* **Principal** — the identity string on a roster line; here, an email address.
* **Fingerprint** — a short hash of a public key (`SHA256:` plus 43 characters)
  a human can compare across two web pages without transcribing the whole key.
* **Bare repository** — a git repository with no working tree, just the object
  database and refs. A forge serves this shape.
* **Refspec** — the `<source>:<destination>` argument to `git fetch` naming
  which refs to copy.
* **TOFU (trust on first use)** — you decide once, out of band, whom to trust,
  and everything afterwards chains off that decision. SSH host keys work this
  way.

### The condition carried from the Decision — unresolved here, and not this plan's to resolve

The Decision records a condition **flagged for Maintainer confirmation**, and
this plan carries it forward without resolving it. In the Decision's own words:

> The ledger entry the Maintainer approved read *"Accept, conditioned on a
> scoped External round for the tag-substitution fix only."* That condition is
> recorded here as adopted, because it was part of the item approved — but the
> Maintainer's quoted words say "as revised" and do not name it. **If an
> unconditioned accept was intended, the condition is theirs to strike in one
> line.**

Two facts an implementing agent must hold together, because conflating them
would silently discharge a control:

1. **The condition (if it stands) is a *proposal-level* round** — External,
   scoped to the tag-substitution finding. The proposal's own Response
   recommended widening that scope slightly (the finding, plus a sweep of the
   five acceptance properties over Parts A and B, plus the hardlink/TOCTOU
   question on the roster-containment check) and stated in terms: *"This does
   not discharge the plan's `required(External, security lens)` tier."*
2. **The plan review is a separate, *plan-level* round.** It is required by the
   superseding Decision, it is recorded in the header above, and it gates
   implementation.

**What the Maintainer must settle before implementation starts** (recorded as a
question, not answered here):

* Does the condition stand, or was an unconditioned accept intended?
* If it stands: is it satisfied by a distinct proposal-level round appended to
  the proposal, or may the plan-review round carry both briefs in one pass? The
  proposal's author recommended they stay distinct; only the Maintainer can
  merge them.

Two other judgments the proposal's Response raised (MD-1, whether correcting the
settled Part B design at proposal time is compliance with the supersession's
binding rather than a departure; and MD-3, ratifying residual RA1's re-marking
from mechanical to non-mechanical plus its new Cairn-side tripwire) are read here
as carried by the Decision's "as revised", since both are changes *inside* the
revision that phrase accepts. That is a reading, not a ruling; if the Maintainer
reads either differently, say so before Chunk A.

**Not in this plan at all:** the `SECURITY_MUTATIONS.md` Class C follow-on. Both
successor scopes declined it, neither claims it, and it is recorded as deferred
Maintainer question 1 on `dev/PLANNING.md`. This plan does no Class C work and
makes no claim on it.

## The finding this plan exists to close: tag substitution

This is placed before *Scope* because it is the reason the plan is
security-tiered rather than a docs-and-a-shell-script pass. It is the Internal
review's BLOCKING finding [I1], and it survived the proposal's *first* fix for
the same failure shape.

**The attack.** An attacker who holds write access to the git forge and **no
signing key** re-points a new version name at an older, genuinely signed tag
object. The documented bootstrap returns exit 0 with a good signature from the
genuine maintainer key, while the signed payload names the *old* release.

**Reproduced independently for this plan**, 2026-08-03, git 2.53.0, in throwaway
repositories under the session scratch directory with freshly generated
throwaway SSH keys and `GIT_CONFIG_GLOBAL` / `GIT_CONFIG_SYSTEM` neutralised to
empty files. No key material belonging to the Maintainer was used and nothing was
written into the Cairn tree:

```
$ git clone -q --bare "$LAB/cand" "$LAB/mirror"
$ git -C "$LAB/mirror" update-ref refs/tags/v0.4.0 \
      "$(git -C "$LAB/cand" rev-parse refs/tags/v0.3.0)"

=== the adopter runs the documented bootstrap, asking for v0.4.0 ===
  fetch rc=0
  Good "git" signature for maint@example.org with ED25519 key SHA256:2DVjXvPq…
  verify-tag v0.4.0 rc=0
  proposal Part-B-original resolver says: dd5323804406cb0a63ab26d516cf50a72548ffbd
  signed payload says:
    object a3c4a320288eb1089101419ee84847520382cce9
    type commit
    tag v0.3.0
```

The adopter asked for `v0.4.0`. The signature is genuine. The signed name is
`v0.3.0`. Exit code 0, and the bootstrap's own instruction — *"judge the exit
code, never the text"* — points the reader away from the one line where the real
name appears.

**The shipped script has the same defect today, in a louder form.** Against the
same substituted mirror:

```
$ bash bootstrap/container/verify-ref.sh <victim-clone> v0.4.0
verify-ref: OK — release tag 'v0.3.0' -> a3c4a320288eb1089101419ee84847520382cce9
rc=0
```

The caller asked about `v0.4.0`; the script answered about `v0.3.0`, called it a
release tag, and exited 0 — with no signature checked anywhere.

**The fix, verified here in both directions.** Resolve the caller's ref to **one
object id**; require that object's signed `tag` header to equal the ref asked
for; verify **that object id**, not the ref name. Measured in the same lab:

```
--- (a) the substitution attack ---
REFUSED: ref 'v0.4.0' resolves to a tag object whose SIGNED name is 'v0.3.0'   rc=1
--- (b) the honest case must still pass ---
PROVENANCED: tag 'v0.3.0' (object dd532380…) signed and name-bound             rc=0
--- (c) honest tag, wrong roster -- the name check must not mask the crypto check ---
REFUSED: signature on 'v0.3.0' did not verify against the trusted roster       rc=1
--- MUTATION: delete the name-binding line, replay (a) ---
PROVENANCED: tag 'v0.4.0' (object dd532380…)                                   rc=0
```

The mutation line is the important one: with the name binding removed, the
substitution passes. That is what makes the negative test discriminating rather
than decorative, and it is written into Chunk A's acceptance criteria as such.

**Two implementation details measured here, because both change the code.**

* **Nested tag wrap.** An attacker needs no key to write an *unsigned* tag object
  named `v0.5.0` whose target is the genuine signed tag object. Measured:
  `^{tag}` does **not** peel through — it returns the outer object — so the name
  check *passes* (the outer really is named `v0.5.0`) and the signature check
  refuses (`error: no signature found`, rc=1). **Both halves are load-bearing;
  neither alone is sufficient.**
* **Resolver exit codes under `set -euo pipefail`.** `git rev-parse --verify
  'refs/tags/<lightweight>^{tag}'` exits **128** without `--quiet` and **1** with
  it, and `--quiet` does **not** suppress the `dereferences to tree type` line on
  stderr. So the script needs `--verify --quiet … 2>/dev/null` **and** an explicit
  `|| refuse` guard, the second because the exit code must be translated to the
  script's documented `1 = refused` regardless.

**What this reproduction does not establish.** It does not establish that any
particular forge's push rules would accept a tag ref pointing at a tag object of
another name — I built the manipulation on a bare clone, which is the shape a
forge serves, and tested no forge. If a forge rejects it, the finding narrows to
hostile mirrors, typosquats, and local candidates; `verify-ref.sh` and the
container recipe accept all three as inputs, so it does not narrow to zero. It
also does not establish that no further instance of this shape remains in the
design — this is the *second* time a fix aimed at "the output must answer the
question that was asked" left another instance of it standing.

## Timing — why this plan is ahead of the v0.4.0 tag

`dev/PLANNING.md`'s public-launch sequence is, in order: eyeball the private
mirror → flip the repo public → enable Zenodo integration → **tag `v0.4.0` and
push (triggers Zenodo deposition → DOI)** → commit the issued DOI into
`CITATION.cff`.

A DOI is a permanent, citable pointer to a byte snapshot. It travels **with the
provenance claim attached and none of the repository's controls attached**. If
`v0.4.0` ships as an unsigned tag while `bootstrap/PROVENANCE.md` still says a
release tag is signed, the false claim is archived into the one channel Cairn
cannot later correct in place — a Zenodo version record is immutable once
published, and a methods-section citation is not recallable.

The marginal cost of preventing that is `-s` instead of `-a` on a tag step
already on the schedule; the signing apparatus (key, roster, repository signing
config) has existed since `a07fac8`. The cost of *not* preventing it rises, after
the DOI, from one flag to an erratum against a permanent archival record.

**The scheduling consequence, stated as a constraint rather than a hope:** this
plan's Chunk M step 1 (publishing the fingerprint) must precede the `v0.4.0` tag,
and the tag must be `git tag -s`. If the launch sequence reaches the tag step
before this plan completes, the correct move is to hold the tag, not to ship an
unsigned one and fix it later.

## Proposed paths

Proposed paths:
- `bootstrap/tests/test_verify_ref.py` — the pytest home for the class table, the negative tests and the mutation ledger; lands in Chunk A and grows through Chunks B, C, E and G.

## Scope

Executes the proposal as revised through its second revision, across the five
Parts. Chunk M is the Maintainer's and is fenced from the implementing agent's
work by construction (see *Maintainer-only steps* below).

**Out of scope, fenced explicitly:**

* **The `SECURITY_MUTATIONS.md` Class C follow-on** — declined by both successor
  scopes, deferred Maintainer question 1 on `dev/PLANNING.md`, and not touched
  here.
* **Install-side provenance** (residual RA6). The lockfile's `source_repository`
  / `source_licenses` stay **declared**, not attested, and `scaffold.py
  --manifest` stays unsigned. This plan fixes source-side only and says so in
  `bootstrap/PROVENANCE.md`.
* **Verifying the tree you build from** (residual RA3). The bootstrap proves a
  tag object is signed; it does not prove an adopter's working tree equals that
  tag's tree. Closing that needs a scaffold-side entry point this plan does not
  add.
* **A transparency log / Sigstore-style keyless signing** (residual RA1's named
  upgrade path). Rejected in the proposal for the stated reason — it adds a
  network service and a non-stdlib client to a path system `git` satisfies today,
  against a zero-adopter-runtime-dependency budget.
* **Retro-attesting `v0.2.0` / `v0.3.0`** (residual RA7). Tag objects are
  immutable; re-signing changes the hash. `bootstrap/PROVENANCE.md` states the
  control boundary as a date instead.
* **Sweeping every other Cairn `git` invocation against trees it does not
  control** (residual RA5). That sweep is a *mandate to the plan reviewer*, below
  — not implementation work in this plan. If the reviewer returns a clean
  enumeration, RA5 closes at plan time; if not, it expires later.
* **Hardlink / TOCTOU evasion of the roster-containment check.** Surfaced by the
  Internal review, not closed by the proposal, and explicitly routed to the
  External round's brief. This plan implements containment as a *path* property
  and does not claim it is a content property.
* **Any `bootstrap/_scaffold/` change.** None. That is what keeps the engine gate
  set and the AST re-anchor off this plan.
* **Any new module, preset, or manifest row.** The install *contract* is
  untouched; exactly one already-installed file's prose changes.

**Sequencing invariant — every intermediate commit is fail-closed.** The chunks
below split the script's contract across three commits. At no point does a
partially-implemented path *accept* something the finished script would refuse:
an unimplemented branch refuses. A reviewer should check this claim per chunk
rather than take it here.

### Documentation / doctrine surface

* **Descriptive layer** — `bootstrap/PROVENANCE.md` is the main change (a stated
  control corrected to match what is enforced, plus a bootstrap procedure and a
  rotation policy that exist nowhere today). `bootstrap/UPGRADE.md`,
  `bootstrap/container/recipe.md` and `docs/quickstart.md` each change by one
  sentence or one pointer.
* **A shipped module** — `dev/modules/security-review.md` and its
  `templates/modules/team-gated/security-review.md` twin, edited in lockstep.
  This is the only **adopter-installed** file this plan touches. The two are
  byte-identical today (`sha256:b838724c729a9e37…`, `as_of 2026-08-03`,
  re-measured for this plan); re-measure at implementation and edit both or
  neither.
* **Deliberation layer** — this plan, its plan review, its code review, and the
  residual rows it lands on `dev/PLANNING.md`.
* **Entry layer** — none. No new document is created; a separate
  `verifying-a-release` document was considered and rejected in the proposal as a
  third place to keep in sync.
* **Governing layer** — **none.** No `AGENTS.md` change, no `doctrine/` change.
  The new procedure is a control Cairn offers adopters, not a rule contributors
  follow.

<!-- cairn:slot documentation-tier-home -->
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
plan's *Scope* must name the doctrine-surface touched (or an explicit
"no doctrine surface").
<!-- cairn:end documentation-tier-home -->

### Gate accounting

Checked rather than assumed, and each figure is a dated snapshot to re-check at
implementation:

* **No gate re-anchor ceremony.** `bootstrap/tests/test_verify_ref.py` is a
  **new** file under a frozen glob, which the gate records as `FROZEN-NEW`
  (*"new gate/test file — allowed, recorded"*) rather than as a HOLD. No frozen
  file is modified: the frozen set holds 164 entries `as_of 2026-08-03`, and none
  of them is under `bootstrap/container/`, nor is `bootstrap/PROVENANCE.md`,
  `bootstrap/UPGRADE.md`, `docs/quickstart.md`, or either copy of the
  security-review module.
* **No AST re-anchor.** No `bootstrap/_scaffold/` file is touched, so
  `bootstrap/REANCHOR_RUNBOOK.md` is not engaged and no engine-gate obligation
  attaches.
* **Collection only grows.** The gate HOLDs on a *dropped* node or a *new*
  skip/xfail marker; added nodes are recorded. Baseline: **1598 passed**, `as_of
  2026-08-03`, under the canonical interpreter (`~/conda_envs/lhm/bin/python`,
  3.13.13) — re-measured for this plan, not quoted from memory.
* **The install manifest is unchanged, and that is the assertion.** Re-measured
  under the canonical interpreter: `python bootstrap/scaffold.py --manifest`
  emits 96 lines — 1 comment header, **95 data rows**, `as_of 2026-08-03`. Zero
  rows match `PROVENANCE` or `container`; exactly one names the security-review
  module. So this plan adds and removes no row and changes the *content* of one
  installed file.
* **The suite must stay at 0 skipped / 0 xfailed.** The new tests need `git` and
  `ssh-keygen` on `PATH`. Their guards must therefore not fire on the canonical
  host — and if they ever do, the gate fails, which is the correct fail-closed
  direction. This is a decision, not a surprise.

## Sequence

```
0. plan-open       -- this plan + the dev/PLANNING.md row-move        [commit pending]
   (plan review)   -- required(External, security lens); NO code before it lands
1. Chunk A -- name-bound resolution: the [I1] fix + its negative test  [commit pending]
2. Chunk B -- the roster contract: required, external, contained       [commit pending]
3. Chunk C -- mode split, exit contract, and the retired vocabulary    [commit pending]
4. Chunk D -- acceptance.sh: five call sites, pins that can fail       [commit pending]
5. Chunk E -- bootstrap/PROVENANCE.md + the extract-and-run doc test   [commit pending]
6. Chunk F -- the retired claim's other homes (4 files, 1 sentence ea) [commit pending]
7. Chunk G -- residual homes, the Cairn-side tripwire, CHANGELOG       [commit pending]
8. Chunk M -- MAINTAINER-ONLY: fingerprint, signed tag, cold bootstrap [not an agent's]
```

### Chunk A — name-bound resolution (the tag-substitution fix)

The security core, and the smallest self-contained unit the scoped External round
can be run against. After this chunk `bootstrap/container/verify-ref.sh` has a
provenance path that resolves the caller's ref to one tag object, binds the
signed name, and verifies that object id against a roster supplied by
`--signers`. Absent `--signers`, this chunk **refuses** (the fuller roster
contract arrives in Chunk B; the intermediate state is fail-closed).

| # | File | Change |
|---|------|--------|
| A1 | `bootstrap/container/verify-ref.sh` | Replace `git describe --exact-match --tags` with `git rev-parse --verify --quiet "refs/tags/<ref>^{tag}" 2>/dev/null` + an explicit `\|\| refuse`; resolution starts from the caller's ref and never from a commit. The `\|\| refuse` branch **names which of its two collapsed causes fired** — no such ref, versus a ref that exists and points at a **non-tag object** (the case informally called a lightweight tag) — by re-probing the bare `refs/tags/<ref>` on failure. Measured 2026-08-03, git 2.53.0: the peeling form returns rc=1 with empty stdout for *both*, and the mandated `2>/dev/null` discards the one line that distinguished them, so the reason is not recoverable from the resolver's own exit status. |
| A2 | `bootstrap/container/verify-ref.sh` | Name binding: read the signed payload's `tag` header with a **header-bounded** parse (stop at the first blank line), refuse an empty result, and refuse unless it equals the ref asked for — naming *both* names in the refusal. |
| A3 | `bootstrap/container/verify-ref.sh` | Verify **the resolved object id**, not the ref name, with the roster pinned by invocation (`-c gpg.ssh.allowedSignersFile=<path>`), plus the defence-in-depth pins on `gpg.ssh.program`, `gpg.program`, `gpg.format`. |
| A4 | `bootstrap/container/verify-ref.sh` | Verification runs in a **temporary bare repository the script creates** (`mktemp -d`, discarded on exit), fetching `--no-tags` exactly `refs/tags/<ref>` from the candidate — never `git -C <candidate> verify-tag`. |
| A5 | `bootstrap/tests/test_verify_ref.py` *(new)* | The negative test: a fixture builds a genuine signed tag, an attacker bare mirror re-points a new version name at it, and the substitution must **refuse**; the honest tag must **pass**; an honest tag against a wrong roster must **refuse**. |
| A6 | `bootstrap/tests/test_verify_ref.py` | The nested-wrap test: an unsigned tag object named `<new>` wrapping the genuine signed object — name check passes, signature check refuses. Asserts *which* half refused, so the two halves stay independently load-bearing. |
| A7 | `bootstrap/tests/test_verify_ref.py` | The `gpg.ssh.program` test: a hostile candidate whose config names a forging verifier that emits the principal on **stdout** (a stderr forger exits 1 and the test would pass for the wrong reason). Asserts refusal **and** that the forger never executed, via a witness file. |
| A8 | `bootstrap/tests/test_verify_ref.py` | The resolver-refusal pair: a ref pointing straight at a commit, and a ref that does not exist. Both refuse (exit 1), and each asserts on **its own** reason string — so a resolver that refuses both with one message cannot satisfy both nodes. This lands the Part B class table's *non-tag object* row in Chunk A, where the resolver lands; C5's per-row sweep inherits the node rather than adding a second. |

**Acceptance criteria — Chunk A**

* The substitution attack **refuses** (exit 1) and names both the asked-for name
  and the signed name; the honest tag **passes** (exit 0). Both asserted through
  the script's command line via `subprocess`, never by sourcing a function.
* **Mutation ledger, recorded in the commit body**: delete the name-binding
  comparison → the substitution test **fails**; restore the source byte-identical
  → green. Same for the `^{tag}` resolver and the object-id verification. A test
  whose deletion-mutant stays green is not accepted.
* **Red-then-green evidence.** The new test module is run once against a copy of
  the *pre-fix* script in a scratch directory and the failure captured, before
  the fix is applied. This is what shows the tests discriminate against the real
  historical defect rather than only against a synthetic mutant.
* Case (c) — honest tag, wrong roster — refuses. This is the check that the name
  binding has not become the *only* check.
* A ref pointing at a **non-tag object** and a ref that does not exist both
  refuse, with **different** reasons, each asserted on the reason and not on exit
  1 alone (A8). Two reasons rather than one is not cosmetic: it is P3 at the
  resolver — a node asserting only *"refused"* on the non-tag-object row passes
  equally against a script that simply could not find the tag, so the row would
  have an oracle that discriminates nothing. It is also the difference between
  telling an adopter whose fork tagged with `git tag` that their tag does not
  exist and telling them it exists but is not an annotated tag object — only the
  second is something they can act on.
* No `git describe` remains on any provenance path (`grep` asserted).
* Suite green under the canonical interpreter, 0 skipped / 0 xfailed, collection
  grown by exactly the new nodes.

### Chunk B — the roster contract: required, external, contained

| # | File | Change |
|---|------|--------|
| B1 | `bootstrap/container/verify-ref.sh` | Provenance mode **requires** a trusted roster: `--signers <path>` or `CAIRN_ALLOWED_SIGNERS`. Absent both, refuse. **No fallback** to repository config, to the candidate's files, or to the adopter's global git config. |
| B2 | `bootstrap/container/verify-ref.sh` | Refuse a roster path that resolves **inside the candidate tree**, resolving symlinks first. Cairn's own `dev/.cairn/allowed_signers` is the internal gate roster and is never consulted for release verification. |
| B3 | `bootstrap/container/verify-ref.sh` | Refuse (never degrade) when `git` or `ssh-keygen` is absent, or when the temporary directory cannot be created. |
| B4 | `bootstrap/tests/test_verify_ref.py` | Roster-boundary tests: missing roster; empty roster; roster naming a principal with no key; roster path that is a directory; roster path inside the candidate, directly **and** via symlink. All refuse. |
| B5 | `bootstrap/tests/test_verify_ref.py` | The self-consistent attacker pair: attacker key, attacker-committed roster naming the *genuine* principal string, attacker `.git/config` pointing git at it. Refusal asserted. This is the [IDN1] boundary test — the unsigned-tag and unrostered-key tests do not reach the bootstrap question at all. |
| B6 | `bootstrap/tests/test_verify_ref.py` | Roster with comma-separated principals (the parsing defect the sibling surface found at `0c6d9de`); and the `$CAIRN_KEY`-unset copy-paste failure, which must land on the keyless-roster refusal. |

**Acceptance criteria — Chunk B**

* Running with no `--signers` and no environment variable **refuses**.
* A roster inside the candidate tree refuses, and so does a symlink into it.
* Every refusal is asserted on the **exit code**, never on the output text —
  every refusal path measured in the proposal's lab still printed a line
  beginning `Good "git" signature` while exiting non-zero.
* Mutation ledger: delete the containment check → the containment test fails.
* Suite green; 0 skipped / 0 xfailed.
* **Recorded as not established**: containment is enforced as a *path* property.
  A hardlinked or concurrently-rewritten roster is a *content* property and is
  not covered. This is stated in the code comment and in the commit body, and it
  is on the External round's brief.

### Chunk C — the mode split, the exit contract, and the retired vocabulary

| # | File | Change |
|---|------|--------|
| C1 | `bootstrap/container/verify-ref.sh` | **Provenance mode becomes the default** and requires a signed, name-bound annotated tag. The integrity-pin path is reachable only under an explicit `--unprovenanced` flag. A bare `verify-ref.sh <repo>` no longer means "HEAD, and call it approved". |
| C2 | `bootstrap/container/verify-ref.sh` | Three outcome vocabularies: `PROVENANCED — annotated tag '<ref>' signed by <principal> -> <sha>`; `NOT PROVENANCED — commit pin <sha> (integrity only; no signature checked)`; `REFUSED — <reason>`. The string `Maintainer-approved` is **deleted**. |
| C3 | `bootstrap/container/verify-ref.sh` | Exit contract extended: `0` = provenanced, **`3` = accepted-but-not-provenanced**, `1` = refused, `2` = usage / not-a-repo. The new code is what lets negative callers discriminate without matching message text. Documented in the script header. |
| C4 | `bootstrap/container/verify-ref.sh` | **Abbreviated SHAs refuse, always** (today a 4-character prefix is accepted). `HEAD` refuses in provenance mode and is `NOT PROVENANCED` under `--unprovenanced`. The existing mutable-branch refusal and dirty/untracked-build-surface refusal are preserved unchanged. |
| C5 | `bootstrap/tests/test_verify_ref.py` | One test per row of the proposal's Part B class table, including the two rows the second revision added (a ref whose object is signed under a different name; a ref resolving to an unsigned tag object, including one wrapping a signed one). |
| C6 | `bootstrap/tests/test_verify_ref.py` | A grep-shaped test: the string `Maintainer-approved` appears in **no tool output string and nowhere under `bootstrap/container/`**. Scoped that way deliberately — the phrase legitimately survives in `CHANGELOG.md` and in the archived deliberation record, which are append-only history. |
| C7 | `bootstrap/tests/test_verify_ref.py` | The multi-tag test: three tags on one commit; asking about tag X never prints tag Y. Plus the regression pins — a mutable branch ref refuses (Codex S5), a dirty or untracked build surface refuses (cross-phase F#2) — each asserted on its **refusal reason**, not only its exit code. |

**Acceptance criteria — Chunk C**

* Every row of the Part B class table has a test, and each test names the row.
* `PROVENANCED` and `NOT PROVENANCED` are distinguishable by exit code alone
  (0 vs 3).
* The `Maintainer-approved` grep test passes and does **not** reach `CHANGELOG.md`
  or `dev/proposals/archive/`.
* The two regression pins fail when their named control is deleted (mutation
  ledger), and they assert on the reason string, so they cannot be satisfied by
  the provenance-mode refusal.
* Suite green; 0 skipped / 0 xfailed.

### Chunk D — `bootstrap/container/acceptance.sh`: five call sites, pins that can fail

The Internal review's [I2]. The proposal originally named *one* call site,
singular; there are five, and three of them are negative assertions that pass on
**any** refusal — so once provenance mode is the default they go green against a
script with both controls deleted.

| # | File | Change |
|---|------|--------|
| D1 | `bootstrap/container/acceptance.sh` | All four no-ref call sites plus the branch pin pass `--unprovenanced`. |
| D2 | `bootstrap/container/acceptance.sh` | Every negative assertion asserts on the refusal **reason** — the dirty pin matches `uncommitted or untracked`, the branch pin matches `mutable branch` — not on the exit code alone. |
| D3 | `bootstrap/container/acceptance.sh` | Where a pin can use the new exit code 3 to discriminate accepted-but-unprovenanced from refused, it does; the reason match is belt-and-braces, not the only mechanism. |
| D4 | `bootstrap/tests/test_verify_ref.py` | The shell-harness mutation test: replay each negative pin against a **stub** with the named control deleted, and assert the pin **fails**. This extends the proposal's mutation discipline — previously scoped to the pytest module — to the shell harness, which is precisely why the defect was reachable. |
| D5 | `bootstrap/tests/test_verify_ref.py` | A provenance-path fixture: the suite builds its own throwaway signed tag and roster and exercises the provenance path end to end, because `acceptance.sh` now runs permanently in `--unprovenanced` mode and therefore never does. |

**Acceptance criteria — Chunk D**

* `bash bootstrap/container/acceptance.sh` passes on the canonical host, or
  reports its documented `[F4 SKIPPED]` when no OCI runtime is present. A skip
  is **not** a pass: if it skips, the D4 pytest nodes are the evidence, and the
  commit body says which of the two ran.
* Each of the three negative pins **fails** against a stub with its named control
  deleted. Recorded as a mutation ledger in the commit body, with the stub kept
  in the scratch directory, not in the repository.
* The provenance path is exercised by at least one suite node that does not
  depend on `acceptance.sh`.
* **Recorded as not established**: with `acceptance.sh` permanently
  `--unprovenanced`, Cairn's end-to-end container harness smoke-checks the mode
  this plan did not add. D5 mitigates; it does not restore end-to-end coverage of
  the provenance path through the container recipe.

### Chunk E — `bootstrap/PROVENANCE.md`, and a test that reads the document

| # | File | Change |
|---|------|--------|
| E1 | `bootstrap/PROVENANCE.md` | Replace the *"Signed tags or maintainer-approved release commits"* control. The second branch is **retired**, not softened: an adopter cannot check "maintainer-authored" (a git author field is free text) and cannot check "protected default branch" (forge-side configuration, invisible from a clone). |
| E2 | `bootstrap/PROVENANCE.md` | State the control as a **dated boundary**: from v0.4.0 a Cairn release is a signed annotated tag verifiable against the published fingerprint; `v0.2.0` and `v0.3.0` are annotated but unsigned and are **not** verifiable (residual RA7). |
| E3 | `bootstrap/PROVENANCE.md` | The out-of-band bootstrap as the **primary** documented path: the channels table (forge signing-key set / ORCID / the per-version Zenodo deposition), the compare-on-at-least-two rule stated as *a mismatch is a refusal, not a retry*, and the command block — fresh `mktemp -d` workspace per run, `--no-tags` fetch, resolve, name-bind, verify the object id, discard the workspace. Every step's exit code is judged, as its own numbered step. |
| E4 | `bootstrap/PROVENANCE.md` | The adopter's roster is `~/.config/cairn/release-signers` — a different directory and a different basename from `dev/.cairn/allowed_signers`, so the forbidden fallback is not invited by naming ([I7]). Channels are named **generically** (*"the git forge account that owns the repository"*, *"the maintainer's ORCID record"*) with concrete URLs as the current instantiation, so a fork inherits the procedure rather than Cairn's accounts. |
| E5 | `bootstrap/PROVENANCE.md` | The rotation section (Part D), including its honest limit: the tagger timestamp is inside the signed payload, so a holder of a compromised key can back-date a tag past a `valid-before` boundary. **Validity windows are hygiene for honest rotation; they are not revocation.** |
| E6 | `bootstrap/PROVENANCE.md` | Three additions to *"What this is not"*: this is account-credential TOFU, not a transparency log (RA1); verifying a tag does not verify the tree you build from (RA3); signing authenticates the *key holder*, not the *human* (inherited from the parent lifecycle, with `e8f75fc` as the recorded demonstration). Plus one sentence in *"Install-side provenance"* naming what RA6 does not cover. |
| E7 | `bootstrap/PROVENANCE.md` | `verify-ref.sh` demoted to a **convenience**, explicitly downstream of the bootstrap, with the reason stated: it lives in the candidate checkout, so running it is already executing candidate bytes (residual RA4). The same sentence goes in the script's own header. |
| E8 | `bootstrap/tests/test_verify_ref.py` | The documented-path test **extracts the command block from `bootstrap/PROVENANCE.md` and runs it** against fixture repositories. The form is decided, not deferred ([I4]): a test running a private copy cannot detect that the document still tells adopters something unsafe. |
| E9 | `bootstrap/tests/test_verify_ref.py` | The two-candidates-same-tag-name test: run the documented sequence twice, against two candidates publishing the same tag name, and assert the second run either reports on the second candidate's object or refuses — never a silent pass on the first candidate's cached object. |
| E10 | `bootstrap/tests/test_verify_ref.py` | The rotation tests: a key retired by `valid-before` refuses a tag dated after retirement and accepts one dated before; **and** the back-dating test, which asserts a back-dated tag from a retired key *still verifies*. That last one is a **residual-pinning** test — it exists so nobody later reads the validity window as revocation. |

**Acceptance criteria — Chunk E**

* Every sentence in `bootstrap/PROVENANCE.md` names something the reader can run.
  The reviewer's check is to read the document and, for each claim, name the
  command; a claim with no command is a finding.
* The E8 test **fails** when the document's block is changed in a way that breaks
  the procedure. Demonstrated by mutating the block in a scratch copy — not
  asserted.
* The rotation tests pin **behaviour**, not a version string: the git floor is
  established by probing for `valid-after` / `valid-before` enforcement against
  the tagger timestamp, so an older git that verifies against "now" is caught at
  execution rather than in production.
* `python scripts/check_cairn.py` green over the changed prose.
* **Recorded as not established**: the forge's SSH *signing*-key endpoint has not
  been verified to be a stable public endpoint for this account. That is Chunk M
  step 1 and it is the single most likely factual correction in this scope. If it
  is false, ORCID is promoted to primary and a third channel is added; the
  procedure is unchanged, only the table is.

### Chunk F — the retired claim's other homes

Found by grepping for the phrase rather than assuming `bootstrap/PROVENANCE.md`
was its only home. One sentence each; **only** those sentences.

| # | File | Change |
|---|------|--------|
| F1 | `bootstrap/UPGRADE.md` | The *"Signed tags and Maintainer-approved release commits … remain the lockfile's actual origin/integrity controls"* sentence, corrected to the enforced control. |
| F2 | `templates/modules/team-gated/security-review.md` | The Layer 1 restatement *"named releases, signed tags / maintainer-approved release commits …"*, corrected. **This one ships**: an adopter selecting the security-review module is handed the retired claim in their own tree. |
| F3 | `dev/modules/security-review.md` | The identical edit to Cairn's self-hosted twin. Byte parity re-measured before and after; the edit lands in both or in neither. |
| F4 | `bootstrap/container/recipe.md` | Phase 1 gains one pointer to the bootstrap procedure, and its description of `verify-ref.sh` is corrected (it currently says a dirty working tree is "reported (advisory)"; it is a refusal). |
| F5 | `docs/quickstart.md` | One pointer, beside the clone command — where the trust decision actually happens. |

**Acceptance criteria — Chunk F**

* `grep -rn "Maintainer-approved\|maintainer-approved"` over the tree returns
  hits **only** in `CHANGELOG.md`, `dev/proposals/`, and `dev/plans/archive/` —
  append-only history, which the append-only rule forbids rewriting.
* `shasum -a 256` byte parity of the two security-review copies holds after the
  edit.
* `python bootstrap/scaffold.py --manifest` diff is **empty** — the assertion is
  that no row is added or removed.
* `python scripts/check_cairn.py` and `python scripts/quality_gate.py --sub
  neutrality` green. The channels are hosting providers, not AI vendors, so the
  neutrality gate does not reach them — but the generic-naming form in E4 is
  better doctrine regardless, and the gate is run to confirm rather than to
  assume.
* The `docs/quickstart.md` edit does not disturb the two load-bearing numbers
  that `bootstrap/tests/test_quickstart_sequence.py` reads out of the prose.

### Chunk G — residual homes, the Cairn-side tripwire, and the changelog

Every residual's expiry trigger names the place it will actually be read from. A
trigger recorded only in a proposal is inert, because accepted proposals archive
and archived proposals are not read.

| # | File | Change |
|---|------|--------|
| G1 | `dev/PLANNING.md` | Rows for the non-mechanical residuals: RA1 (b) and (c), RA3's upgrade path, RA5's next-surface trigger, RA6's seam with the sibling scope, and RA1 (a) re-marked **non-mechanical** per the proposal's Response to [I3]. |
| G2 | `bootstrap/tests/test_verify_ref.py` | The genuinely mechanical RA1 tripwire, on **Cairn's** side: a suite assertion that `dev/.cairn/allowed_signers` names exactly **1** principal (`as_of 2026-08-03`, re-measured for this plan), failing when Cairn's own signing authority widens. It fires in Cairn's suite, where Cairn will see it. |
| G3 | `bootstrap/container/verify-ref.sh` | The adopter-facing principal-count **warning** (not a refusal) stays, as adopter hygiene. It is no longer claimed as a posture-expiry trigger for Cairn: it counts principals in a file the *adopter* typed, it lives in the script Part C demotes to a convenience, and there is no channel back to Cairn. A fork with two maintainers trips it on day one, which is why it warns. |
| G4 | `CHANGELOG.md > Unreleased > Fixed` *(and `Added`)* | One line for the corrected control and one for the new verification procedure. |

**Acceptance criteria — Chunk G**

* Every residual in the proposal's table has a home that is **not** the proposal:
  RA1 (a) in code + test, RA1 (b)(c) / RA3 / RA5 / RA6 on `dev/PLANNING.md`, RA2
  in the rotation section plus the back-dating pin, RA4 in the script header and
  the recipe, RA7 in the dated control boundary.
* G2 fails when `dev/.cairn/allowed_signers` gains a second principal
  (demonstrated against a fixture, not asserted).
* `python scripts/claim_check.py` clean on every Markdown file this chunk edits,
  one file per invocation.

### Chunk M (Maintainer-only) — the v0.4.0 handoff

> **An implementing agent must not perform any step in this chunk.** Every step
> requires the private signing key or an account credential. The plan's
> implementation *ends* at Chunk G plus a stated readiness condition; Chunk M is
> the Maintainer's, in the shape `gate-reanchor-preflight`'s Chunk G established.

1. **Publish the fingerprint on the named channels.** This is the step that
   creates the trust root, and it must **precede** the tag so the tag is
   verifiable the moment it exists. It includes confirming that the forge
   actually serves SSH *signing* keys at a stable public endpoint for this
   account — the fact this scope most expects to be corrected.
2. **Cut `v0.4.0` with `git tag -s`** (not `-a`), as part of the existing launch
   sequence.
3. **Run the bootstrap block cold** against the pushed tag, from a machine and a
   roster that did not come from the repository. This is the acceptance check for
   the whole scope: if it does not pass here, nothing else in this plan
   established the control.
4. **Only then** let the launch sequence proceed to Zenodo deposition and the
   DOI.

**Rotation, when it happens** (also Maintainer-only, and documented in Chunk E5
rather than performed here): generate the new key and publish its fingerprint on
**every** channel; announce the transition in an annotated tag signed by the
**outgoing** key naming the incoming fingerprint; publish the outgoing line with
`valid-before=<date>` and the incoming line with `valid-after=<date>`, both
staying published so old releases keep verifying. **On suspected compromise, the
signed-announcement step is void** — the attacker holds the outgoing key and can
sign the announcement. The response is out-of-band re-anchoring on every channel
plus explicit publication of the revoked fingerprint. Cairn cannot *push* that to
anyone (residual RA2).

## Acceptance criteria

Per-chunk criteria are above. These are the plan-level deliverables.

* **Tests that must pass.**
  * `python -m pytest bootstrap/tests` — the whole suite, green, **0 skipped / 0
    xfailed**, under the canonical interpreter (3.13.13). Baseline 1598 passed,
    `as_of 2026-08-03`; collection grows by exactly the new nodes and drops none.
  * `bootstrap/tests/test_verify_ref.py` — the new module, driving the shell
    script **through its command line** via `subprocess`, never by sourcing a
    function, in throwaway repositories built by a fixture that generates
    ephemeral SSH keys. One node per row of the Part B class table, plus the
    named negative tests.
  * `bash bootstrap/container/acceptance.sh` — green, or its documented skip with
    the D4 pytest nodes standing in and the commit body saying which ran.
  * **Every test shown non-vacuous by mutation**: remove the check, confirm the
    test fails, restore the source byte-identical. The ledger goes in the commit
    body. This is `gate-reanchor-preflight`'s Chunk E discipline, adopted
    unmodified and — per [I2] — extended to the shell harness.
* **Doc updates that must land.** All hand-authored: `bootstrap/PROVENANCE.md`
  (substantial), `bootstrap/UPGRADE.md`, `bootstrap/container/recipe.md`,
  `docs/quickstart.md`, and the security-review module in both copies. Plus
  `CHANGELOG.md > Unreleased > Added/Fixed`. No generated docs and no
  snippet-synced blocks are involved — but note that E8 makes
  `bootstrap/PROVENANCE.md`'s command block *executable by the suite*, which is a
  drift control of the same family reached from the other side.
* **Examples / smoke checks required.** `bash bootstrap/container/acceptance.sh`;
  the bootstrap block run by hand against the pushed `v0.4.0` tag (Chunk M step
  3); `python bootstrap/scaffold.py --manifest`, expected **unchanged**, which is
  itself the assertion that this plan installs nothing new into an adopter tree.
* **Inbound path-link updates.** None expected: `dev/PLANNING.md` and
  `dev/NEXT_SESSION.md` refer to plans by filename stem, not path link, so the
  archive-move needs no edit there. Confirm at archive time rather than assume.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants, each with the chunk that enforces it.**
  * *No provenance claim without a verified signature.* Chunk C's class-table
    tests, one per row, plus the `Maintainer-approved` grep test (C6).
  * *The candidate never supplies verification material.* Structural — the script
    verifies in a repository it created (A4) — plus two tests: the
    self-consistent attacker pair (B5) and the `gpg.ssh.program` case (A7).
  * *The trusted roster is required and never defaulted.* B1/B2, pinned by B4's
    missing-roster and containment tests.
  * *The caller's ref is the ref reported, and the ref signed.* A1–A3, pinned by
    A5 (substitution), A6 (nested wrap) and C7 (multi-tag).
  * *Nothing persists between verification runs.* A4's `mktemp -d` workspace,
    pinned by E9's two-candidates-same-name test.
* **Public-path → test mapping.** `bootstrap/container/verify-ref.sh` has exactly
  one public entry point — its command line — and every test drives it through
  that command line. The bootstrap block in `bootstrap/PROVENANCE.md` is a
  *documented* public path with no executable home; E8 gives it one by extracting
  and running it. The test module is cited as a code span rather than a relative
  markdown link because it does not exist yet — the template's link form assumes
  an existing test, which a plan that creates the test cannot satisfy; it is
  registered under *Proposed paths* instead, and the link form is adopted at code
  review once the file resolves.
* **Failure modes — all closed.** Missing roster → refuse. Unresolvable ref →
  refuse. Non-tag object → refuse. Signed name ≠ asked-for name → refuse.
  Signature not verifying → refuse. `git` or `ssh-keygen` absent → refuse, not
  degrade. Temporary-directory creation failing → refuse. The one deliberately
  **open** path is `--unprovenanced`, which is open by construction, says so in
  its own output, exits 3 rather than 0, and is reachable only when an operator
  types the flag.
* **Edge cases handled.** Every row of the Part B class table; empty roster;
  roster naming a principal with no key; roster with comma-separated principals;
  candidate with no tags; ref containing shell metacharacters; a refspec
  metacharacter (`REF='*'` produces a valid refspec and fetches every tag, then
  fails closed at the resolve step); a `--signers` path that is a symlink into
  the candidate; slash-namespaced tag names such as `release/v0.7.0` (the
  comparison is on the full ref name, not a basename).
* **Known omissions, stated rather than implied.** (a) The candidate-git-config
  class is closed *for this surface* by construction, **not swept** — no
  enumeration of every config key that can influence a git verification, and no
  sweep of Cairn's other `git` invocations against trees it does not control
  (residual RA5, and mandate 2 to the plan reviewer). (b) No git other than
  2.53.0 has been tested; the rotation tests probe for behaviour instead of
  parsing a version string. (c) SHA-256 repositories (Cairn is SHA-1; the
  resolver's hex-length check admits 64-hex but is untested), non-UTF-8
  principals, concurrent rotation, and adopters behind a TLS-intercepting proxy
  are all **out of scope and stated as such**. (d) Hardlink / TOCTOU evasion of
  the roster-containment check is not covered. (e) No network-side fact has been
  checked: the forge's signing-key endpoint, ORCID, and Zenodo are all Chunk M
  step 1.

## Verification

The concrete commands the implementation must pass.

<!-- cairn:slot verification-commands -->
The standing gates Cairn runs before a change lands (the same ones CI
enforces):

* **Engine suite** — `python -m pytest bootstrap/tests` (the whole
  suite; scope to `bootstrap/tests/test_<surface>.py` while iterating,
  but the full suite gates the cut).
* **Prose integrity** — `python scripts/check_cairn.py` (internal link
  / anchor resolution + claim-path check over the Markdown tree).
* **Quality gate** — `python scripts/quality_gate.py` (order-
  independence + vendor-neutrality + redundancy; `--sub neutrality`
  alone for a doctrine / template wording change).
* **Write-time claim check** — `python scripts/claim_check.py <file>` over
  each proposal / plan / doc the change authored. **One file per
  invocation** — the checker takes a single path and exits 2 (usage) on
  more, so loop rather than passing a list.

Plan-specific gates (a security-lint budget, a doc-drift gate, the
model-selection mapping check `python scripts/check_model_selection.py`)
are added per plan when the change touches that surface.
<!-- cairn:end verification-commands -->

**Plan-specific gates, added here because this change touches those surfaces.**
Run under the canonical interpreter (`~/conda_envs/lhm/bin/python`, 3.13.13) with
`PYTHONDONTWRITEBYTECODE=1`; a different Python minor silently changes
AST-attestation and oracle results.

* **The container harness** — `bash bootstrap/container/acceptance.sh`. Green, or
  the documented `[F4 SKIPPED]` with D4's pytest nodes named as the standing
  evidence.
* **The install-contract assertion** — `python bootstrap/scaffold.py --manifest`,
  diffed against the pre-change output. **Expected empty.** 95 data rows across
  96 lines, `as_of 2026-08-03`.
* **Module byte parity** — `shasum -a 256 dev/modules/security-review.md
  templates/modules/team-gated/security-review.md`, equal before and after.
* **The retired-claim sweep** — `grep -rn "Maintainer-approved\|maintainer-approved"`
  over the tree, expected to hit only append-only history.
* **The gate manifest** — the frozen-file and collection checks, confirming
  `bootstrap/tests/test_verify_ref.py` reads as `FROZEN-NEW` and no
  `FROZEN-MODIFIED` or `COLLECTION-DROPPED` entry appears.
* **The mutation ledgers** — per chunk, in the commit body: the deletion, the
  observed test failure, and the byte-identical restore.

**Note on doc gates**: drift gates (broken references, stale renders,
snippets that diverged from their source) catch **drift**, not
**absence** of new doc updates. Confirm each doc named in Acceptance
was actually updated; the gates don't enforce that.

## Plan review — the brief, and why the tier is not discharged

*Required — External, security lens. Implementation does not start until a review
has landed under this heading.* The tier is not the author's to set: the
superseding Decision mandates it, and the proposal's Response records that a SHIP
verdict at proposal time does **not** partly discharge it.

> **The landed review appends here as a `### Plan review -- <reviewer> --
> YYYY-MM-DD` sub-heading** (plus a `### Sharpening` sub-heading if it raised
> findings). **Do not rename this heading to a bare `## Plan review`.** Measured
> 2026-08-03: with a bare `## Plan review` heading and this plan at
> `awaiting-plan-review`, `python tools/lifecycle_planner.py next <plan>` reports
> `[ok] a '## Plan review' section has landed` — a section that exists but is
> empty of any review satisfies the checker's gate. With the heading as written
> above, the same command correctly reports `[MISSING]` until a real `###`
> review sub-heading lands. The checker matches a section *kind*, not a review;
> this heading is shaped so the gate cannot be satisfied by a placeholder.

**Why the tier is right independent of the mandate.** This lifecycle has now
produced **five** instances of one failure shape inside a single rolling week —
the pre-flight checker resolving its roster through the candidate's config
(`0c6d9de`); an in-repository roster bootstrapping the tag containing it; the
`gpg.ssh.program` vector; the fixed-workspace false pass on a second run; and the
tag substitution reproduced at the top of this plan. Four of the five were found
by the same agent type as the author, three of them only after deliberately going
looking for the class. Same-agent vigilance has a measured failure rate here.

**Mandates for the reviewer** — offered so the pass has a target rather than a
lens. The first two are carried from the proposal and are **entirely unrun**; the
third and fourth are this plan's.

1. **Channel discipline over every step.** For each verification step in Chunks
   A, B, C and E — the fetch, the resolve, the name-bind, the verify, the roster
   read, the containment check — name the channel each input arrives by and show
   it is not the thing being verified.
2. **Sweep the enumeration the proposal did not finish (residual RA5).** Are
   there other candidate-controlled git config keys, or other `git` invocations
   in Cairn against trees it does not control, in this class? A clean answer
   closes RA5 at plan time instead of leaving it to expire.
3. **Sweep the five acceptance properties over the sequenced chunks.** The
   proposal's second revision states them: **P1** anchor independence (no input
   to a step is supplied by the artifact under verification — including the
   roster, the verifier program, the config that selects either, and the
   workspace); **P2** question fidelity (the caller's ref, the ref resolved, the
   name inside the signed payload, and the object the signature was checked over
   are all the same thing); **P3** oracle discrimination (every assertion fails
   when the control it names is deleted); **P4** statelessness (nothing persists
   between runs; the anchor is durable, the workspace never is); **P5** claim ≤
   evidence (no output label, document sentence, or residual marking asserts more
   than was checked). For each chunk: which properties does it touch, and does it
   satisfy them? This is the first pass on this scope that could return a
   *positive* answer rather than "nothing found this time."
4. **The hardlink / TOCTOU question on the roster-containment check.**
   Containment is enforced as a *path* property; a hardlinked or
   concurrently-rewritten roster is a *content* property. Is that reachable in
   practice? Nobody has built it.

**The stopping rule the proposal set, restated so the reviewer can use it.** A
finding on this scope is one of exactly two things. Either it names a violation
of P1–P5 — then it is a bug against a stated property and the fix is bounded. Or
it names a property *not* in P1–P5 — then the specification was incomplete, the
property is added, and **every earlier step is re-swept against the new
property**, not just the one the finding landed on. The second branch is the
expensive one and is supposed to be; it is the only branch that makes the list
converge. P1–P5 are derived from failures observed in this repository. They are a
floor, not a completeness proof.

**What the reviewer should not spend attention on.** The trust model itself — the
channel table, Part C's disposition, Part D's rotation mechanics, Part E's
handoff — survived an External round and an Internal round and is not re-opened
by this plan.

## Code review — the brief (no review has landed)

*Filled in after implementation commits land.* Per `doctrine/plans.md`, the
reviewer is **not** the implementing agent, the section is append-only, and a
clean final review carries a falsification ledger and a coverage line. The landed
review appends here as a `### Code review -- <reviewer> -- YYYY-MM-DD`
sub-heading; the heading above is shaped the same way as the plan-review one, and
for the same measured reason — `_has_kind` gates `review -> archived` on a
section *kind*, so a bare placeholder heading would report the archive gate
satisfied before any review existed.

Three checks this plan asks its code reviewer to run rather than read:

* **Re-run the substitution attack** against the landed script — build the bare
  mirror, re-point a version name at an older signed tag object, and confirm the
  refusal names both names. A code review that asserts the fix without re-running
  the attack does not close it; that is the process note the Internal reviewer
  attached to the finding, and it is the shape this lifecycle has repeatedly
  shown to be necessary.
* **Re-run one mutation from each chunk's ledger**, chosen by the reviewer, not
  by the implementer.
* **Read `bootstrap/PROVENANCE.md` end to end and name the command behind each
  claim.** A sentence with no command behind it is a P5 finding.

## Lasting-truth migration

*Filled in at archive time.* Per `doctrine/plans.md`, the archive commit body
carries the literal `Follow-ups migrated to:` block naming where each deferred
item went, so the migration is auditable from the commit log alone — and the
plan does not archive until every deferred follow-up has a durable home outside
it.

The homes are pre-declared here so archive time is bookkeeping rather than
recall: residuals RA1 (b)(c), RA3, RA5 and RA6 → `dev/PLANNING.md` rows (Chunk
G1); RA1 (a) → the adopter-facing warning and the Cairn-side suite tripwire
(G2/G3); RA2 → `bootstrap/PROVENANCE.md`'s rotation section plus the back-dating
residual-pinning test (E5/E10); RA4 → the script header and
`bootstrap/container/recipe.md` Phase 1 (E7/F4); RA7 → the dated control boundary
(E2), expiring by construction at v0.4.0.

**Two items that are not residuals and must not be archived away as if they
were:** the Decision's flagged condition (a scoped External round for the
tag-substitution fix), which is the Maintainer's to confirm or strike; and the
`gate-claims-vs-enforcement` seam — that proposal deferred its
`bootstrap/PROVENANCE.md` row (E1) here under a reversion clause, and Chunk E
discharges it. Marking that discharged is a one-line note in **that** proposal's
own record, not an edit made from this plan.

Per the [Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home outside the
plan.

This section is append-only once written.

## Plan review -- Gemini Flash (External, security lens) -- 2026-08-03

**Steelman.** This plan provides an exceptionally thorough operational roadmap for establishing an immutable release authenticity trust root in `bootstrap/PROVENANCE.md` and implementing exact signed-tag verification. In particular, Chunk A directly addresses the tag-substitution finding by binding the caller's requested ref name directly to the signed `tag <name>` header inside the OpenPGP/SSH signed tag payload (`cat-file -p <tag_obj>`).

### Concerns

* **[E1] Verification must guard against tag object vs commit object ref resolution.**
  When `git rev-parse refs/tags/<ref>^{tag}` is run against a unannotated (lightweight) tag, `rev-parse` returns an error or empty string because no annotated tag object exists. Chunk A correctly targets annotated/signed tags, but the resolver must fail closed with a distinct, actionable error if a caller requests verification of an unannotated tag ref rather than raising an uncaught exception or falling back to raw commit verification.

### Covered

* **Tag substitution attack reproduction and fix verification**:
  Reproduced the tag substitution attack in a bare git repository created under `/tmp`. Created signed tag `v0.3.0`, and then repointed `refs/tags/v0.5.0` to the `v0.3.0` tag object.
  - Raw `git verify-tag refs/tags/v0.5.0` returned exit code 0 (succumbing to substitution).
  - The plan's proposed exact-tag name binding logic (`signed_name != asked_ref`) correctly refused `v0.5.0` (exit code 1).
  - The honest case (`v0.3.0` ref pointing to `v0.3.0` signed tag object) passed with exit code 0.

```
=== RAW GIT VERIFY-TAG v0.5.0 (SUCCUMBS TO TAG SUBSTITUTION) ===
STDOUT: 
STDERR: Good "git" signature for maint@example.org with ED25519 key SHA256:z72TbxMmcikShPxZD9ezY88auzdKb3zS60MjYfsezVA
EXIT CODE: 0

=== PLAN PROPOSED NAME-BINDING CHECK ===
Asked ref: 'v0.5.0' | Resolved Object: c43c766bce805634448b4b0ec066c560d92a7561 | Signed Name: 'v0.3.0'
REFUSED: ref 'v0.5.0' resolves to a tag object whose SIGNED name is 'v0.3.0'
PLAN PROPOSED EXIT CODE FOR SUBSTITUTION ATTACK: 1

=== HONEST CASE CHECK (v0.3.0) ===
Asked ref: 'v0.3.0' | Signed Name: 'v0.3.0' | Matches: True
Crypto Verify Exit Code: 0
HONEST CASE FINAL EXIT CODE: 0
```

### Not covered / low confidence

* Live SSH key signature verification over hardware security keys (e.g. YubiKey SSH format) was simulated via software Ed25519 keys in temporary test directory; actual hardware token interaction remains out of test scope.

### Recommendation

**READY FOR IMPLEMENTATION.** The plan's sequencing, acceptance criteria, and exact-tag resolution logic are sound and verified.


## Response to plan review -- Claude (author) -- 2026-08-03

**Model**: Claude Opus 5

**One finding, accepted — but only one of its three limbs was open.** The verdict
was READY FOR IMPLEMENTATION; that is not a reason to leave [E1] undisposed, and
this lifecycle has already produced Decisions landing over reviews whose findings
were waved through on a favourable verdict. [E1] is answered on the merits below.
Everything asserted here was measured for this Response on 2026-08-03 under git
2.53.0, in throwaway repositories under the session scratch directory with
`GIT_CONFIG_GLOBAL` / `GIT_CONFIG_SYSTEM` neutralised. No key material was used,
and nothing was written into the Cairn tree outside this plan.

### [E1] ACCEPTED — in one limb of three: the resolver already fails closed and already refuses to fall back; what it does not do is say *which* cause fired

**The finding, restated.** `git rev-parse refs/tags/<ref>^{tag}` errors or returns
empty when the ref names no annotated tag object. Chunk A targets annotated
signed tags correctly, but the resolver must fail closed **with a distinct,
actionable error** when a caller asks about an unannotated (lightweight) tag ref —
not raise an uncaught exception, and not fall back to raw commit verification.

**Measured first, before disposing.** Three refs in one repository — `lw`
(pointing straight at a commit), `ann` (a real annotated tag object), and
`nosuch`:

```
=== refs/tags/lw -> commit 404c5a31 ===
  rev-parse --verify         'refs/tags/lw^{tag}'      rc=128  stdout=[]
      stderr: error: refs/tags/lw^{tag}: expected tag type, but the object
              dereferences to tree type / fatal: Needed a single revision
  rev-parse --verify --quiet 'refs/tags/lw^{tag}'      rc=1    stdout=[]
      stderr: error: ... dereferences to tree type          <-- NOT suppressed
=== refs/tags/nosuch (no such ref) ===
  rev-parse --verify --quiet 'refs/tags/nosuch^{tag}'  rc=1    stdout=[]  stderr=[]
=== refs/tags/ann -> tag object e35406d2 ===
  rev-parse --verify --quiet 'refs/tags/ann^{tag}'     rc=0    stdout=[e35406d2...]
```

The reviewer's premise is factually right, and it reproduces the plan's own
earlier measurement exactly. What the numbers then show is that the finding is
three claims, not one, and they do not have the same disposition.

**Limb 1 — "not an uncaught exception": ALREADY-COVERED, with a detail the review
does not carry.** The plan measured this before the review, in the section *The
finding this plan exists to close*, and specified the guard:

> **Resolver exit codes under `set -euo pipefail`.** `git rev-parse --verify
> 'refs/tags/<lightweight>^{tag}'` exits **128** without `--quiet` and **1** with
> it, and `--quiet` does **not** suppress the `dereferences to tree type` line on
> stderr. So the script needs `--verify --quiet … 2>/dev/null` **and** an explicit
> `|| refuse` guard, the second because the exit code must be translated to the
> script's documented `1 = refused` regardless.

Chunk A row A1 carries it into the contract: *"`git rev-parse --verify --quiet
"refs/tags/<ref>^{tag}" 2>/dev/null` + an explicit `|| refuse`"*. The `|| refuse`
is there precisely because `set -euo pipefail` would otherwise abort the script on
the resolver's non-zero exit — which is the uncaught-exception failure the
reviewer names — and because rc must be translated to the script's documented `1 =
refused` either way. The detail the review does not have is that `--quiet` leaves
the `dereferences to tree type` line on stderr, so `2>/dev/null` is load-bearing
too; a guard without it refuses *and* prints a raw git error at an adopter.

**Limb 2 — "not a fallback to raw commit verification": ALREADY-COVERED, and the
defect the reviewer is describing is live in the shipped script today.** The
contract already forbids it in three places: A1 (*"resolution starts from the
caller's ref and never from a commit"*), C1 (*"Provenance mode becomes the default
and requires a signed, name-bound annotated tag. The integrity-pin path is
reachable only under an explicit `--unprovenanced` flag"*), and the plan's
failure-mode list (*"Non-tag object → refuse"*, and `HEAD` refusing in provenance
mode per C4). It is worth recording *why* A1 deletes `git describe` rather than
adjusting it, because the pre-fix behaviour on the reviewer's own input is worse
than "falls back to the commit". `bootstrap/container/verify-ref.sh` today
resolves `${REF}^{commit}` (line 41) and then asks `git describe --exact-match
--tags "$COMMIT"` (line 44) — resolution *from a commit*, which is the shape A1
removes. Run against the lab repository above:

```
$ bash bootstrap/container/verify-ref.sh cand lw
verify-ref: OK — release tag 'ann' -> 404c5a3173cc26e6ffca94784091487b77b48a0a
rc=0
```

The caller asked about `lw`; the script answered about **`ann`** — a different tag
— called it a release tag, and exited 0. That is the [I1] shape again, on the
lightweight-tag input, and it is another reason the `describe`-from-a-commit path
is deleted rather than repaired.

**Limb 3 — "a *distinct*, actionable error": OPEN. This is the limb I accept.**
Nothing in the plan required the refusal to say which cause fired, and the
measurement above shows the two causes are not separable without a second probe:
`refs/tags/lw^{tag}` and `refs/tags/nosuch^{tag}` both return rc=1 with empty
stdout, and the mandated `2>/dev/null` discards the single stderr line that told
them apart. So a literal reading of A1 yields one refusal message for both. The
plan's own author-accounting already lists them as *two* failure modes —
*"Unresolvable ref → refuse. Non-tag object → refuse."* — but no chunk step bound
the **output** to the distinction, and an acceptance criterion that does not exist
is not a control.

**Routing it through this plan's stopping rule.** The rule says a finding either
violates P1–P5 (bounded fix) or names a property outside them (specification
incomplete, re-sweep every earlier step). This one is **P3, oracle
discrimination**, at the resolver: a test node asserting only *"refused"* for the
non-tag-object class-table row passes equally against a script that merely could
not find the tag, which is exactly P3's *"a negative assertion that passes for any
refusal reason is not a control"*. So it is the bounded branch — a bug against a
stated property, fixed inside Chunk A — and it triggers no re-sweep and no new
acceptance property.

**One thing the finding implies that was already covered, stated so it is not
double-counted.** The class-table row exists: the proposal's second revision
retired the old *"lightweight tag"* row and replaced it with *"tag ref resolving
to a non-tag object (a commit, a tree) | REFUSED | not an object that can carry a
signature"*, and Chunk C5 mandates *"One test per row of the proposal's Part B
class table"* with the Chunk C criterion *"Every row of the Part B class table has
a test, and each test names the row."* The case therefore already had a node
promised. What it lacked was an oracle strong enough to distinguish it, and a
resolver obliged to produce one.

**Plan change — three touches, all inside Chunk A, none widening its contract.**

* **Row A1 amended.** After the existing `|| refuse` sentence: the refuse branch
  **names which of its two collapsed causes fired** — no such ref, versus a ref
  that exists and points at a non-tag object — by re-probing the bare
  `refs/tags/<ref>` on failure, with the measurement recorded inline (rc=1, empty
  stdout, for both; `2>/dev/null` discards the distinguishing line).
* **Row A8 added** (`bootstrap/tests/test_verify_ref.py`): the resolver-refusal
  pair — a ref pointing straight at a commit and a ref that does not exist — both
  refusing, each asserting on **its own** reason string, so one message cannot
  satisfy both nodes. It states that this lands the class table's *non-tag object*
  row in Chunk A, where the resolver lands, and that C5's per-row sweep inherits
  the node rather than adding a second.
* **One Chunk A acceptance criterion added**, binding the two reasons to the P3
  argument above rather than leaving "distinct" as a taste preference.

The re-probe is two `git rev-parse` calls against the temporary bare repository
the script already creates (A4), so it adds no new input channel, no new trusted
material, and nothing for P1 to rule on. No new file, no manifest row, no gate
obligation: the gate accounting in *Gate accounting* stands unchanged, and
collection still only grows.

### The reviewer's "Not covered / low confidence" note

The note records that hardware-token SSH signing (a YubiKey-resident key) was
simulated with software Ed25519 keys. **Genuinely out of scope for the
implementing chunks, and no follow-up row is needed for them**: verification
consumes only the public key text an adopter typed into their own roster, and a
token participates at *signing* time only — which is Chunk M step 2 and the
Maintainer's, never an implementing agent's. The one place it could touch this
scope is the literal example roster line in Chunk E4 and the fingerprint published
in Chunk M step 1: both are parametric in the key type (`principal <keytype>
<key>`), so a hardware-backed key changes the literal in the example, not the
procedure. Whether that warrants a sentence in Chunk M step 1's confirmation —
which the plan already flags as *"the fact this scope most expects to be
corrected"* — is a Maintainer call, and I have not made it here.
