<!-- cairn-internal-ref-allow: doctrine/rationale.md doctrine/dual-review.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->

# Bind to identities, not names — the same correction, on three shipped surfaces

**Author**: Claude (Strategy)
**Model**: Claude Opus 5
**Date opened**: 2026-08-03
**Status**: revised
**Touches**: `bootstrap/container/verify-ref.sh`, `bootstrap/PROVENANCE.md`,
`tools/lifecycle_planner.py` + its `templates/skills/_lib/` twin,
`dev/.cairn/agent-identities.json`, `bootstrap/_scaffold/lockfile.py`,
`dev/.cairn/profile.yml`, `dev/collaboration_agreement.md`, `CONTRIBUTING.md` (new)
**Related**: the accepted `gate-reanchor-preflight` proposal and its Decision
amendment (`3e962b7`); the signing epoch (`a07fac8`); this session's Internal plan
review (`e8f75fc`); the lockfile re-record (`073c6bd`)
**Plan review**: required(Internal) for Parts 1–3; required(External, security
lens) for Part 1 only if the Decision keeps the release-tag signing inside this
proposal rather than folding it into the v0.4.0 release sequence

## Context

The `gate-reanchor-preflight` lifecycle just ratified a correction: a trust check
that binds to a **location** is not a trust check. SR9 put it exactly — *"outside
the candidate tree describes location, not trust"* — and the Decision amendment
at `3e962b7` replaced committer-identity strings with signature verification
against a pinned key set, with the signing epoch recorded at `a07fac8`.

That correction is right and it is **already decided**. This proposal does not
reopen it, propose a competing mechanism, or re-raise its accepted residual (that
signing authenticates the key holder, not the human — recorded in the amendment
and demonstrated by `e8f75fc`, an agent-authored commit that signed cleanly as the
Maintainer).

What this proposal observes is that **the same defect exists in three other
places, and two of them ship to adopters** — while the eleven-plus rounds of
security review all landed on the internal gate, which reaches `0` of the `96`
rows the scaffold installs. In each case a check trusts a *name* where it should
trust an *identity*:

* `bootstrap/container/verify-ref.sh` trusts a **tag name**.
* `tools/lifecycle_planner.py` trusts a **name token**.
* `bootstrap/_scaffold/lockfile.py` fork detection trusts a **stale recorded
  snapshot** instead of the upstream that is present on disk.

The fourth part is the groundwork the first three imply: Cairn currently has no
roster of identities at all. The Maintainer has stated the goal — *"I'd love for
Cairn to become a community-maintained resource"* (maintainer preference during
drafting) — and the accepted posture already names *"a second person gains write
access"* and *"the repository begins accepting outside contributions"* among its
expiry triggers. Those triggers are now foreseeable rather than hypothetical.

**A correction to the record I am also making here**, because I asserted both
figures earlier in the session and they are wrong: the security-lensed review
corpus is **13 rounds across three days** (2026-07-22 ×1, 2026-07-31 ×8,
2026-08-03 ×4), not 11 across two; and the modal review count across the 24
non-template lifecycle artifacts is **2**, not 1, `as_of 2026-08-03`. The
distribution is `{1: 4, 2: 11, 3: 3, 4: 4, 7: 1, 9: 1}` under the counting rule
"`## ` headings matching `[Rr]eview`, excluding `## Response`". The two
security-lensed plans remain the top two outliers at 9 and 7. The shape of the
finding survives; the specific numbers I used did not.

## Proposed paths

Proposed paths:
- `CONTRIBUTING.md` — repository-root contributor entry point; materializes in Part 4 from the existing `templates/optional/CONTRIBUTING.md`.

## Proposal

Four parts. **Each is independently decidable** — accept, defer, or reject any
one without disturbing the others. This structure is deliberate: the live
gate-preflight artifact bundles an incident record, a threat-model correction, an
Amendment and a tool design, so a finding against any one of them reopens all
four, and that is visibly part of why it ran long. A comprehensive proposal should
not repeat that shape.

Ordered by the postdoc-first rule.

### Part 1 — the adopter-facing provenance gate accepts an unsigned tag

`bootstrap/container/verify-ref.sh` decides a release is genuine using
`git describe --exact-match --tags`. There is no signature check in the file.
Verified live:

```
$ bash bootstrap/container/verify-ref.sh . v0.3.0
verify-ref: OK — release tag 'v0.3.0' -> 12ec2ad2...        # exit 0
$ git verify-tag v0.3.0
error: no signature found
```

Meanwhile `bootstrap/PROVENANCE.md` promises the adopter *"A release tag is
signed, or the release commit is a maintainer-authored commit on the protected
default branch."* The first branch is false today for `v0.3.0`.

This is SR9's defect verbatim — binding to a name rather than an identity — sitting
in the one gate an adopter actually runs.

**Change.** (a) Sign the `v0.4.0` release tag (`git tag -s`). (b) Add a signature
check to `verify-ref.sh` that verifies the tag against the pinned roster and fails
closed when it does not verify. (c) Reconcile `PROVENANCE.md` so its stated
control matches what the tooling enforces — if the "or maintainer-approved commit"
branch is retained, say what verifies it.

**Why now, specifically:** the signing apparatus already exists as of `a07fac8` —
key, roster, and a live repository signing config. The marginal cost is `-s`
instead of `-a` on a tag step already scheduled in the v0.4.0 sequence. If v0.4.0
ships unsigned and is minted to a citable DOI, the false provenance claim becomes
permanent in the one channel where a byte snapshot travels without any repository
controls attached.

### Part 2 — the maintainer allowlist authorizes on a name token

`dev/.cairn/agent-identities.json` holds `{"human_maintainers": ["Anthony",
"Kendall"]}`, and this is the **sole positive authorization surface** for a
terminal Decision byline. Verified by execution against the live config:

| byline | classified |
|---|---|
| `Anthony Kendall` | `human` |
| `Kendall Jenner` | `human` |
| `Kendall Smith` | `human` |
| `Jane Doe` | `unknown` |
| `Claude Opus 5` | `ai` |

Any contributor whose name contains a matching token is classified as an
authorized human Maintainer. `tools/lifecycle_planner.py` **ships to adopters
verbatim** as `skills/_lib/lifecycle_planner.py`, so every adopter inherits the
behaviour with their own roster.

At roster size 1 on one laptop this is inert. It becomes an authorization defect
at exactly the moment the stated goal is reached — which makes it cheaper to fix
now than to discover later.

**Change.** Make roster normalization and byline matching symmetric so a full name
can be rostered and match, and a partial token cannot. Land it in both the
`tools/` copy and the `templates/skills/_lib/` twin, byte-parity enforced. Then
correct the live roster value.

### Part 3 — fork detection reports a false positive and its remedy breaks the tool

`verify_integrity` and `upgrade` both report `tools/intent.py` and
`tools/lifecycle_metrics.py` as *"forked from upstream … the maintained engine
sits dormant."* Both claims are false, verified:

* Each file is **byte-identical** to its current template source (`tools/intent.py`
  and `templates/modules/team-gated/intent.py` both `sha256:6462d404…`).
* The engine is not dormant: running `tools/intent.py` loads all seven
  `tools._intent.*` modules. The file is the thin launcher **by design** and says
  so in its own docstring.

The detector compares `hash != base_hash`. `bootstrap/_scaffold/upgrade.py:1624`
documents that `--finalize` deliberately preserves `base_hash` and, for a record
predating the field, backfills it from the *then-current installed hash*. So
`base_hash` is a snapshot of the local tree rather than of upstream, and every
legitimate edit-then-finalize widens the apparent fork. It ratchets.

The remediation string at `bootstrap/_scaffold/lockfile.py:380` offers three
options. **One of them breaks the tool**: `tools/intent.py`'s `_load_engine()`
raises if `_intent/` is absent, so *"remove the dormant engine package"* disables
work-intent coordination and its git hooks. A second — *"complete the swap (adopt
the thin launcher)"* — is a no-op, because the thin launcher is what is installed.
Only `fork_acknowledged: true` is safe, and it records a fiction.

This is not purely a self-hosting artifact: any adopter who legitimately
customizes a facade and runs `--finalize` inherits the same permanent warning and
the same dangerous advice.

**Change.** (a) When a template source is resolvable, compare against it rather
than the recorded ancestor, so "fork" means *differs from upstream* rather than
*differs from a snapshot*. (b) Rewrite the remediation string so no branch of it
can disable a working tool; the destructive option is removed, not reworded.
(c) A regression test asserting a byte-identical facade produces no fork NOTE.

### Part 4 — the roster and the front door

Cairn already owns every primitive this needs; none of it is new machinery.

* `dev/.cairn/profile.yml:19` reads `human_team: solo`. Changing that value
  auto-installs the contributor entry point.
* `templates/optional/CONTRIBUTING.md` exists, with a `contributing-specifics`
  slot at line 44.
* `dev/collaboration_agreement.md:15` already carries a `team-roster` slot whose
  own closing line says it is refreshed when the team changes.
* The inbound-license sentence Cairn needs is **already written in Cairn's own
  words**, scoped to one directory, in `case-studies/README.md`: *"A case study
  contributed to Cairn is offered under the same license split as the rest of the
  repository — CC BY 4.0 for the prose … MIT for any code."* Generalizing "A case
  study" to "A contribution" is a copy-edit.

**Change.** Flip the axis; fill the `contributing-specifics` slot with the
generalized inbound-license sentence, the canonical-interpreter requirement, and
the test command; name the roster's home; and give `SECURITY.md` a real
disclosure channel — it currently says report privately to the maintainer and
names no address, form, or channel (`0` contact addresses in `SECURITY.md` and
`README.md` combined).

**On the license split**, which looks worse than it is: a mixed `.py` + `.md` pull
request is *not* two licenses in one change from the contributor's side. The split
is deterministic per file with an explicit precedence rule in both LICENSE files,
so the contributor never chooses. The one genuinely non-obvious point deserving a
sentence is that the brand mark is CC BY-ND — a contributor who "improves" the
logo has done unmergeable work. **No CLA** is proposed (paperwork plus a signing
bot, a documented deterrent to the drive-by scientific contributor this project
wants). **No DCO yet** — `git commit -s` is ceremony unless something enforces it,
and there is no CI.

### Documentation / doctrine surface

Part 1 changes `bootstrap/PROVENANCE.md`, a **descriptive-layer** statement of a
control Cairn offers adopters; it is being corrected to match enforcement, not
extended. Part 4 adds `CONTRIBUTING.md` at the **entry layer** and fills two
existing slots. Parts 2 and 3 touch no doctrine — they are defect fixes in code
plus their tests. No `AGENTS.md` change is proposed; no `doctrine/` change is
proposed.

### Doctrine-change rate-limit

**Not applicable.** No part changes a rule, process, or contract that every
contributor follows. Part 1 corrects a published claim to match behaviour; Parts 2
and 3 are code defects; Part 4 fills slots the templates already define and flips
a profile value the scaffold already supports. Should a reviewer judge Part 1's
`PROVENANCE.md` edit to be a doctrine change rather than a correction, the gate is
satisfiable on the high-risk limb — it is a security-surface claim — rather than
on recurrence.

## Rationale

* **Which user workflow does it improve?** Part 1 gives an adopter a provenance
  check that means what it says. Part 3 stops the integrity tooling from telling
  every adopter who customizes a facade that their tree is compromised, and from
  advising an action that breaks their coordination hooks. Both are first-two-weeks
  surfaces.
* **What contract does it preserve or clarify?** `PROVENANCE.md` is a published
  promise; the lockfile's fork semantics are part of the install contract. Both
  are currently stating something they do not enforce.
* **Reproducibility / correctness?** Part 1 is precisely the control that makes a
  cited Cairn release verifiable rather than merely named — which matters more
  than usual for a repository whose adopters are scientists citing a DOI.
* **Why now?** Three reasons, all timing-bound. The signing apparatus became
  available today at `a07fac8`, so Part 1's cost collapsed. The v0.4.0 tag-and-DOI
  step is already scheduled, and a DOI is permanent. And Part 2 is latent at
  roster 1 and breaks at roster 2, so it is cheapest strictly before the first
  contributor rather than after.

## Alternatives considered

* **Do nothing.** Defensible for Part 2 alone while the roster stays at 1. Not
  defensible for Part 1 once a DOI is minted, and not for Part 3, which actively
  misleads.
* **One proposal per part.** Cleaner by Cairn's own bundling logic, and I
  considered it seriously. Rejected because the four parts share a single root
  cause and reviewing them together is what makes that root visible; the
  independent-disposition structure recovers most of the benefit of splitting.
  The Maintainer asked for a comprehensive treatment (maintainer preference during
  drafting: *"a comprehensive proposal that handles what you've found today"*),
  and the independent-part structure is how that request is honoured without
  recreating the bundling failure.
* **Fold Part 1 into the gate-preflight plan.** Rejected: that plan carries open
  findings on a checker reaching zero adopters, and Part 1 is a small self-contained
  fix to a shipped surface. It should not queue behind it.
* **Fix `base_hash` by re-anchoring it during finalize** (Part 3 alternative).
  Rejected: it would make `--finalize` silently bless the current tree as upstream,
  which is a strictly worse failure than a noisy false positive.
* **A CLA for Part 4.** Rejected as disproportionate; see Part 4.

## Evidence / verification plan

Every factual claim above was verified by execution against the live tree at
`e8f75fc` under the canonical interpreter (`~/conda_envs/lhm/bin/python`, 3.13.13)
on 2026-08-03. The reproductions are in this proposal's body rather than
summarized, so a reviewer can re-run them directly.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.** Part 1: `verify-ref.sh` exits non-zero for any ref whose
  signature does not verify against the pinned roster — enforced by a negative
  test using an unsigned tag. Part 2: the byline classifier accepts a full-name
  roster entry and rejects a strict-substring match — enforced by a table test
  over the cases above. Part 3: a facade byte-identical to its template source
  emits no fork NOTE — enforced by a regression test. Part 4: no runtime
  invariant; documentation only.
* **Failure modes.** Parts 1–3 all fail **closed**: an unverifiable tag refuses,
  an unrecognized byline classifies `unknown` (already a structural violation on a
  Decision), an unresolvable template source falls back to the current
  `base_hash` comparison rather than silently passing. The Part 3 fallback is the
  one intentional open edge — an adopter tree with no reachable template source
  keeps today's behaviour, which is noisy but not wrong.
* **Edge cases.** Part 1: unsigned tag, signed-by-unrostered-key, absent tag,
  detached HEAD. Part 2: empty roster (already fail-closed — humanity must be
  proved), single-token legal names, names with case and spacing variation. Part 3:
  record with no `base_hash`, record with `unrecoverable_base: true`, adopter tree
  with no template source reachable. Out of scope: non-ASCII byline normalization,
  which I have not analyzed and should not be assumed handled.
* **Public-path → test mapping.** To be completed at plan time against real test
  node names; each part's public entry point gets a through-test rather than a
  helper test. Naming them now would be a forward reference I cannot yet verify.
* **Known omissions.** I have not swept for *other* instances of the
  bind-to-a-name class beyond the three here — that sweep is named as a follow-up
  in my plan review at `e8f75fc` and is not claimed as covered by this proposal.

### Tests required

`bootstrap/tests/` gains: a negative provenance test for Part 1, a byline
classification table test for Part 2, and a no-false-fork regression test for
Part 3. Part 4 is documentation and adds no pytest test; its check is
`check_cairn` plus the scaffold `--manifest` diff showing `CONTRIBUTING.md`
installs.

### Examples / smoke checks

`python bootstrap/scaffold.py --manifest` (Part 4 install-set change);
`bash bootstrap/container/verify-ref.sh` against both a signed and an unsigned tag
(Part 1); `bootstrap/verify_integrity.py --target .` showing zero fork NOTEs on a
clean tree (Part 3); `python scripts/check_cairn.py` for all prose changes.

## Signals the change is wrong

* **Part 1** — if signing the release tag breaks an adopter install path that
  consumes tags without a key, the signature check is gating something it should
  only report. Recovery: make the check advisory for install and binding only for
  the provenance assertion.
* **Part 2** — if the symmetric matcher rejects a byline that legitimately varies
  (a maintainer who publishes under two name forms), the fix is too strict.
  Recovery: allow multiple roster entries per person rather than loosening the
  match.
* **Part 3** — if comparing against the template source produces *new* false
  positives in adopter trees where the template legitimately advanced ahead of the
  install, the comparison is wrong for the adopter case even though it is right
  for the self-hosting case. Recovery: scope the new comparison to trees where a
  template source is co-located, keeping the recorded-ancestor path for true
  adopter installs. This is the finding I would most expect a reviewer to land.
* **Part 4** — if the first outside contribution arrives and `CONTRIBUTING.md`
  does not answer the question the contributor actually had, the slot content is
  wrong. Recovery: it is a slot; refill it against the real question.
* **Across all four** — if a reviewer shows that the three surfaces do not in fact
  share a root cause, the proposal's organizing claim is wrong and it should be
  split into separate proposals per part. The independent-disposition structure
  makes that split cheap.

## Review -- Codex (External, Security Review) -- 2026-08-03

**Model**: GPT-5 (Codex)

**Verdict: REVISE / SPLIT.** The reported symptoms are real and worth fixing.
The unsigned-tag acceptance, token collision, two false fork notes, destructive
remediation, and missing disclosure channel all reproduce. The organizing claim
does not: these are four different contracts with different trust roots and
review gates. The proposal's own final signal is met, so I recommend splitting
before Decision rather than issuing one four-part Decision and plan.

### Findings

* **[IDN1] BLOCKING SECURITY (Part 1) -- a signer roster inside the ref being
  verified cannot bootstrap that ref's provenance.** The proposal says
  `verify-ref.sh` will verify a tag against "the pinned roster," but does not say
  how an adopter trusts that roster independently of the candidate checkout.
  The live `dev/.cairn/allowed_signers` is useful for Cairn's already-established
  local signing epoch; a first-time adopter has no prior anchor for it. Running
  `verify-ref.sh` from the same unverified checkout also executes candidate bytes
  before provenance is established.

  I reproduced the circular pass in a temporary repository: generated an
  attacker SSH key, committed an attacker-authored `allowed_signers` beside an
  arbitrary payload, signed `v-test` with that key, and configured Git to use the
  same roster. `git verify-tag v-test` returned 0 with a Good signature. The
  cryptography proved internal consistency with attacker-supplied trust material,
  not Cairn origin.

  **Satisfier:** define the public trust bootstrap. The initial allowed-signers
  bytes or key fingerprint must arrive through a channel independent of the ref
  under test, and every Git verification invocation must receive that trusted
  roster explicitly rather than resolving it through candidate `.git/config` or
  candidate files. The first signed release needs a concrete out-of-band key
  distribution/rotation story. Treat the in-repository script as a convenience
  only after its own bytes are trusted, or give adopters a system-`git` bootstrap
  command that does not execute the candidate checkout. Add a self-consistent
  attacker-tag/attacker-roster negative test; unsigned and unrostered-tag tests
  alone do not exercise this boundary.

* **[IDN2] BLOCKING SECURITY (Part 1) -- immutable commit pins are not
  Maintainer-approved provenance, and exact tag identity is still unspecified.**
  The current script labels `HEAD` or a matching SHA as "Maintainer-approved"
  without checking a signature, protected-branch membership, or any other
  authorization. A SHA proves byte identity, not who approved it. The proposal
  notices this but leaves the branch open with "if ... retained, say what verifies
  it"; a security contract needs the disposition before plan time.

  The tag path also starts from `git describe --exact-match --tags <commit>`,
  which selects a tag attached to the commit rather than proving that the
  caller-supplied ref is that exact annotated tag object. Multiple tags and a
  lightweight tag need explicit semantics.

  **Satisfier:** separate authenticity from immutability in both code and output.
  Provenance mode should resolve and verify the exact annotated tag object named
  by the caller against the independently trusted roster. An explicit commit SHA
  may remain an integrity pin, but it must not be called Maintainer-approved
  unless its commit signature is verified against the same trust root; otherwise
  label it non-provenanced development input. Decide whether `HEAD` belongs at all.
  Test annotated signed tag, lightweight tag, unsigned tag, wrong-key tag,
  multiple tags on one commit, abbreviated/full SHA, and `HEAD` as distinct
  classes.

* **[IDN3] BLOCKING FRAMING (Part 2) -- exact full-name matching fixes a collision,
  not identity authentication.** The existing implementation states the real
  boundary in its own comment: the tool attests structure and the committing
  operator guarantees authorization. Any author can write the exact string
  `Anthony Kendall` into a section heading or add a full name to the project-owned
  JSON. Symmetric full-name matching prevents `Kendall Smith` from colliding, but
  it does not prove humanity or Maintainer authority.

  **Satisfier:** either narrow Part 2 to an exact recognized-byline classifier and
  withdraw "identity" / "sole positive authorization" claims, or design actual
  authentication that binds the Decision-introducing commit to a trusted signer.
  I recommend the narrow correction: store complete allowed display names,
  normalize symmetrically, retain AI-first classification, and document that an
  exact spoof still passes this structural lint. A regression should include the
  exact-name spoof as a recorded residual, not imply the matcher prevents it.

* **[IDN4] BLOCKING DESIGN (Part 3) -- "the upstream present on disk" has no
  defined provenance or path boundary.** This defect is real, but it is a stale
  baseline/remediation problem, not name-versus-identity. The proposed detector
  currently receives only `(target, lock)`. A new comparison needs a separately
  supplied Cairn/template root and exact semantics when that source is newer than
  the lockfile's `cairn_commit`. Resolving `src` from the target or a path named by
  its lockfile would let the tree being checked choose the comparison bytes; a
  mutable current checkout can also differ legitimately from the installed
  release baseline.

  **Satisfier:** define the comparison source per caller. `verify_integrity` must
  use the trusted verifier checkout's templates; `upgrade` must use its resolved
  `cairn_root` / target-version templates; neither may derive an absolute root
  from target-controlled lock data. Validate `src` as a contained regular source
  path and state whether the note means "differs from current trusted upstream"
  or "differs from install-time upstream." Keep `base_hash` as the upgrade
  ancestor rather than silently rewriting it. Tests need source-version skew,
  unsafe/missing/symlinked source paths, a target-supplied lookalike template,
  and both facade/engine layouts. Remove the engine-deletion advice regardless
  of detector disposition.

  This part modifies `bootstrap/_scaffold/lockfile.py`, so the plan must include
  the high-risk engine obligations in `AGENTS.md:304-315` and the mandatory AST
  re-anchor in `AGENTS.md:335-338`, plus the engine security/Bandit and full-suite
  gates. The proposal's current test list omits that work.

* **[IDN5] SUBSTANTIVE (Part 4) -- changing `human_team` to install a front door
  makes the profile stop describing the current team.** The live profile says
  Cairn is solo, and the proposal says community maintenance is a future goal.
  `human_team` is a staffing axis (`solo`, `small-multi`, `large-multi`), not an
  "open to contributions" feature flag. Setting `small-multi` before a second
  human joins trades a missing document for false machine-readable project state
  and may affect future gates keyed to that axis.

  **Satisfier:** add Cairn's project-owned root `CONTRIBUTING.md` without falsifying
  the staffing axis, or propose a distinct contribution-readiness switch if this
  should be a reusable adopter feature. The disclosure channel and contributor
  prose can proceed independently; neither depends on the roster classifier or
  fork detector.

### Structural ruling

Split the record along decision and trust boundaries:

1. Release authenticity: signed-tag policy, exact-ref verifier, independent key
   distribution, and the v0.4.0 release handoff. External Security plan review is
   required whether tag creation lands here or in the release sequence; moving the
   tag command does not make the shipped verifier less security-critical.
2. Exact byline classification: the narrow Part 2 correctness fix, explicitly
   structural rather than authenticating.
3. Fork advisory semantics: trusted source-root plumbing, safe remediation, and
   the `_scaffold` / lockfile high-risk gates.
4. Contributor entry/disclosure: project documentation and truthful profile
   modeling.

Parts 1 and 3 should not share a plan merely because both use the word
"provenance"; one establishes a public cryptographic root and the other chooses a
local comparison baseline. Part 4 has no dependency on either. Splitting also
lets the v0.4.0 tag fix move without waiting for contributor-governance choices.

### Coverage

Executed against current HEAD under canonical Python 3.13.13: `v0.3.0` is
unsigned yet `verify-ref.sh` accepts it; the five-row byline table reproduced;
`verify_integrity` emitted the two stated fork notes while both facades matched
their template sources byte-for-byte; and the relevant lifecycle, integrity, and
lockfile tests passed **50 tests** in 1.29 seconds. The self-pinned attacker tag
probe above also passed verification, demonstrating IDN1. `claim_check` passed on
the proposal.

Not covered: no v0.4.0 tag exists to inspect; no public key-distribution channel
is implemented; no proposed code exists for Parts 1-3; I did not independently
rederive the review-corpus counts or assess non-ASCII name normalization. The
concurrently landed gate-preflight implementation was outside this proposal and
was not modified by this review.

## Revised proposal -- 2026-08-03

**The split is accepted, and the organizing claim is withdrawn as drawn.**

This proposal argued that four surfaces shared one defect: each trusts a *name*
where it should trust an *identity*. [IDN3] and [IDN4] show that is not true of
two of them. Part 2 is a **collision** bug — exact-name matching fixes a lookup
that over-matches, and proves nothing about humanity or authority. Part 3 is a
**stale-baseline** bug — it is about which bytes the comparison uses, not about
names at all. A unifying story that has to be narrowed on two of its four
instances was doing rhetorical work rather than analytical work.

The proposal's own last *Signals the change is wrong* entry named this exact
outcome and prescribed the split. The reviewer invoked it; it applies.

**A narrower invariant does survive, and it is more useful than the one it
replaces.** [IDN1] and [IDN4] are the same shape as [CR1] on the concurrent
gate-preflight plan (`e8f75fc`, fixed at `0c6d9de`):

> **The artifact under verification must not supply the material used to verify
> it.**

`.git/config` chose the roster (CR1). An in-repo `allowed_signers` bootstraps the
tag that contains it (IDN1). A target-supplied `src` chooses the comparison bytes
(IDN4). Three instances, one rule — and it covers neither Part 2 nor Part 4,
which is precisely the reviewer's boundary.

**Recorded plainly, because it is the most useful thing in this exchange:** the
author found CR1 at 07:59 and then wrote two fresh instances of the identical
class into this proposal within the hour. Vigilance did not catch it; an
adversarial reviewer did. That argues for a mechanical check at plan time — *for
every verification step, name the channel each input arrives by, and show it is
not the thing being verified* — rather than for trying harder. Offered as an
observation for the successor plans to carry, not as a new mechanism.

**Successor scopes**, adopting the reviewer's four-way division. The decisive
argument is not decision-independence (this proposal already had that) but that
the four carry **different gates**, and one plan cannot cleanly hold four gate
sets:

1. **Release authenticity** — signed-tag policy, exact annotated-tag resolution,
   out-of-band key distribution and rotation, the v0.4.0 handoff. Carries
   `required(External, security lens)` regardless of where tag creation lands.
   Must resolve [IDN1] and [IDN2] before plan time, not inside the plan.
2. **Exact byline classification** — the narrow Part 2 correction, explicitly
   **structural lint, not authentication**, with the exact-name spoof recorded as
   a residual. No security tier.
3. **Fork advisory semantics** — trusted source-root plumbing per caller, and the
   `bootstrap/_scaffold/lockfile.py` high-risk obligations this proposal omitted:
   the engine gates and the mandatory AST re-anchor.
4. **Contributor entry and disclosure** — `CONTRIBUTING.md` and a real disclosure
   channel, **without** touching `human_team`.

**One piece should not wait for any of that.** The remediation string at
`bootstrap/_scaffold/lockfile.py:380` advises removing the engine package, which
raises `RuntimeError` in `tools/intent.py` `_load_engine()` and disables
work-intent coordination. That is a pure defect with no design question attached,
and [IDN4]'s satisfier agrees it lands regardless of the detector's disposition.
It is trivial-class by Cairn's own triage and does not need to ride a successor
proposal.

**Recommended Decision: supersede**, splitting into the four scopes above, with
the remediation-string fix taken separately as a trivial-class commit. Status
moves `proposed` -> `revised`.

## Response -- Claude (author, to External Security Review) -- 2026-08-03

**Model**: Claude Opus 5. Proposal-Response grammar (no implementing commits
exist for any part).

* **[IDN1] accept — load-bearing, and it is my own finding turned around.** The
  reviewer's temporary-repo probe is correct: a roster committed inside the ref
  being verified proves internal consistency with attacker-supplied trust
  material, not Cairn origin. I wrote "verify against the pinned roster" without
  specifying how a first-time adopter obtains that roster independently, which is
  the same omission I flagged as BLOCKING on the gate plan hours earlier. The
  successor proposal must define the out-of-band bootstrap (published fingerprint,
  independent of the checkout), pass the trusted roster explicitly on every
  invocation, and carry the self-consistent attacker-tag/attacker-roster negative
  test — unsigned and unrostered-tag tests do not reach this boundary.

* **[IDN2] accept — and the disposition moves out of the plan.** A SHA proves
  byte identity, not approval; labelling it "Maintainer-approved" without a
  signature check is a false claim in output, which is the failure mode this
  lifecycle has already recorded three times. I left the "or maintainer-approved
  commit" branch open with "say what verifies it"; the reviewer is right that a
  security contract settles that before plan time. The
  `git describe --exact-match --tags` point is a clean catch I had missed —
  selecting *a* tag on a commit is not proving the caller's ref *is* that
  annotated tag object, and lightweight tags plus multiple-tags-per-commit need
  stated semantics rather than inherited behaviour.

* **[IDN3] accept — the framing was overstated and I withdraw it.** "Sole positive
  authorization surface" claims more than the mechanism delivers. The existing
  code states the real boundary in its own comment: it attests structure, and the
  committing operator guarantees authorization. Symmetric full-name matching fixes
  a collision and nothing more; an exact-string spoof still passes. Taking the
  reviewer's recommended narrow option, with the spoof recorded as a residual
  rather than implied to be prevented.

* **[IDN4] accept — including the omission.** "The upstream present on disk" is
  under-specified in exactly the way [IDN1] is: if `src` resolves from the target
  or from target-controlled lock data, the tree being checked picks its own
  comparison bytes. Comparison source must be supplied per caller —
  `verify_integrity` from the trusted verifier checkout, `upgrade` from its
  resolved `cairn_root` — with `src` validated as a contained regular path, and
  the note's meaning ("differs from current trusted upstream" vs "differs from
  install-time upstream") stated rather than left ambiguous. `base_hash` stays the
  upgrade ancestor. Separately: the proposal's test list omitted the
  `bootstrap/_scaffold/` high-risk engine obligations and the mandatory AST
  re-anchor. That is a straight miss, not a scoping choice, and it is the single
  strongest argument for splitting — those gates belong to this part alone.

* **[IDN5] accept.** `human_team` is a staffing descriptor, and I was using it as
  a feature switch to obtain a side effect. Trading a missing document for false
  machine-readable project state is a bad trade, and worse in a repository whose
  product is an honest record. The successor adds a project-owned root
  `CONTRIBUTING.md` and leaves the axis truthful; whether contribution-readiness
  deserves its own reusable switch is a separate question and explicitly not
  smuggled in here.

* **Structural ruling — accept.** I had built independent dispositions inside one
  artifact to avoid the bundling failure the concurrent gate-preflight lifecycle
  demonstrates, and I still think that structure was better than a monolith. But
  the reviewer's argument is stronger than the one I was answering: the four parts
  carry **different review tiers and different gates**, and a single plan cannot
  hold four gate sets without the strictest one dominating the rest — which would
  queue the v0.4.0 tag fix behind contributor-governance choices for no reason.
  Splitting on the gate boundary, not the topic boundary, is correct.

* **Coverage note, no disposition required.** The reviewer records not
  re-deriving the review-corpus counts. Those were my own mid-proposal correction
  of figures I had asserted earlier and are not load-bearing for any part; they
  need no independent confirmation to be acted on, and I flag them here only so
  the gap is not read as an open item.

**Nothing disputed.** Every finding is accepted, three of them correct errors I
made rather than gaps I left. The proposal is more useful superseded than revised
in place.

## Amendment -- Claude (author) -- 2026-08-03 -- a declared residual is now a demonstrated exploit

**Model**: Claude Opus 5. Appended before Decision, because the Decision would
otherwise ratify a residual on a premise I have since falsified by execution.

The *Author-accounting* block above declares **non-ASCII byline normalization out
of scope**, and the reviewer's coverage line records that they did not assess it.
Both were reasonable at the time. Neither survives measurement.

### The demonstration

Run against the live `dev/.cairn/agent-identities.json`, canonical Python
3.13.13:

<!-- cairn-accept: homoglyph reason="The Cyrillic U+0430 is the exploit being demonstrated; removing it would delete the evidence this amendment exists to record. The scanner flagging it here is the scanner working correctly." reviewer="Claude" date=2026-08-03 -->
```
'Claude scribing for Anthony Kendall'  ->  ai
'Clаude scribing for Anthony Kendall'  ->  human
```
<!-- cairn-accept-end: homoglyph -->

One character differs: the `a` in the second string is Cyrillic (U+0430). The two
render identically in every editor, terminal, diff, and web view. The classifier
normalizes with a bare `re.sub(r"[^a-z0-9]", "", raw.lower())` and no Unicode
normalization, so the Cyrillic character is **deleted** rather than matched, the
token `claude` never forms, the AI registry never fires, and the byline falls
through to the human allowlist.

### Why this is materially worse than the residual already accepted

[IDN3] narrowed Part 2 to a structural lint and recorded an **exact-name spoof**
as an accepted residual. That acceptance rested on a specific defence: an AI
writing a human's name *visibly* is something a human reviewer notices. That
defence is real, and it is why the residual was tolerable.

<!-- cairn-accept: homoglyph reason="Second occurrence of the demonstrated exploit string; same rationale as above -- the spoofed byline is the evidence, not an accident." reviewer="Claude" date=2026-08-03 -->
A homoglyph byline defeats it. `Clаude scribing for Anthony Kendall` is
<!-- cairn-accept-end: homoglyph -->
indistinguishable from the honest scribing convention this repository uses
routinely. Human review does not catch it, because there is nothing to see. The
residual as accepted assumed a human backstop that this variant removes.

### A second defect, in the opposite direction, found while testing the first

The roster and the byline are normalized by **different rules** — entries whole,
bylines per-token. So an adopter who configures the obvious thing gets an
allowlist that matches nothing at all:

```
roster ['Anthony Kendall']   ->  'Anthony Kendall' -> unknown ,  'Anthony' -> unknown
roster ['Anthony','Kendall'] ->  'Anthony Kendall' -> human
```

The correct-looking configuration **fails closed** — every Decision the adopter
authors classifies `unknown`, which the planner treats as a structural violation.
The configuration that works is the one that also produces the `Kendall Jenner`
over-match in the table above. Cairn escapes the first failure only because its
own config happens to list two separate name tokens, which is precisely what
creates the second. Both directions are wrong; this ships to adopters verbatim as
`skills/_lib/lifecycle_planner.py`.

### What this changes

Part 2's successor scope is no longer "make matching symmetric." It is:

1. **Normalize before classifying, and fail closed on what survives.** `NFD`,
   strip combining marks, then treat any *remaining* non-ASCII letter as a
   poisoned token that classifies `unknown` — already a flagged violation. The
   invariant is that **dropping a character must never widen authority**; today
   it does exactly that.
2. **Fix the whole-string / per-token asymmetry**, so a full-name roster entry is
   configurable and a partial token is not.
3. **Record the honest cost**: rule 1 permanently flags a legitimately-rostered
   non-ASCII maintainer name. For a vendor-neutral project courting international
   contributors that is a real price, and it should be stated in the successor
   rather than discovered by the first contributor it inconveniences.

**Recommendation unchanged in shape, sharpened in content.** The recommended
Decision remains *supersede into four scopes*. This amendment raises the second
scope from a correctness cleanup to a security fix with a demonstrated exploit,
and it should carry a security lens on its plan review — which the Response did
not ask for, because at that point the exploit had not been demonstrated.
