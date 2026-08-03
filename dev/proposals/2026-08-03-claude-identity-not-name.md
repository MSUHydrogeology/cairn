<!-- cairn-internal-ref-allow: doctrine/rationale.md doctrine/dual-review.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->

# Bind to identities, not names — the same correction, on three shipped surfaces

**Author**: Claude (Strategy)
**Model**: Claude Opus 5
**Date opened**: 2026-08-03
**Status**: proposed
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
