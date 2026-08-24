# Retire External plan review: plans take Internal fresh-agent reviews only

**Author**: Claude (Strategy)
**Model**: Fable 5
**Date opened**: 2026-08-24
**Status**: accepted
**Assurance path**: high-assurance (governing doctrine and lifecycle)
**Touches**: `AGENTS.md` + `templates/core/AGENTS.md`;
`doctrine/dual-review.md`, `doctrine/plans.md`, `doctrine/proposals.md`,
`doctrine/lifecycle.md`, `doctrine/lifecycle-contract.md`,
`doctrine/session-routines.md`; `dev/proposals/_template.md`,
`dev/plans/_template.md` + shipped twins;
`dev/agent_collaboration.md` + shipped twin; `tools/lifecycle_planner.py` +
shipped twin; `bootstrap/tests/test_lifecycle_contract.py`,
`bootstrap/tests/test_pilot_evidence.py`,
`bootstrap/tests/fixtures/gate_manifest.json`
**Related**: `2026-08-21-claude-convergent-lifecycle` (**accepted** `47315b6`;
see "Relationship" below and Decision preamble item 2 — the migration §4
anticipates is already discharged),
`dev/strategy/2026-08-21-claude-nimbleness-recovery.md`
**Plan review**: required(Internal) — set by the Maintainer direction this
proposal records; a recorded readiness token is a preserved recommendation
the Maintainer resolves at the Decision

## Origin

Maintainer direction, 2026-08-24, verbatim: *"we need to completely remove
the doctrine for External Plan Review from this project. It is not, and
should not ever, be required. We can thus remove all machinery and doctrine
for making such recommendations in the Plan. Plans only ever have internal
fresh-agent reviews, be they security or standard."*

## Proposal

**One rule replaces the apparatus: a plan review is an Internal,
fresh-context review — always.** Standard or security-flavored, the reviewer
is a fresh session of the same agent type, never a mandated different-type
round. External plan review ceases to exist as a tier, a requirement, a
recommendation slot, or an escalation target. Concretely:

1. **Doctrine.** `doctrine/dual-review.md` loses "Plan-readiness
   inheritance" and every External-plan-review pathway; the review-allocation
   statement becomes: *External independence lives at the proposal; Internal
   freshness lives at the plan and at code review; the Maintainer decides.*
   `AGENTS.md`'s Review section (and its shipped twin) drops the
   inheritance/escalation paragraph — including `DISTINCT REVIEW REQUIRED`,
   readiness invalidation, and "spending" an External plan round. The other
   doctrine files' mentions are conformed.
2. **Templates.** The proposal template loses the `Plan readiness` slot
   entirely — reviewers no longer record plan-review recommendations of any
   kind; that is the "machinery for making such recommendations" the
   direction removes. The plan template's review declaration becomes a closed
   two-token vocabulary: `required(Internal)` (default) or
   `not required(<rationale>)` (trivial-accept collapse, unchanged). A
   security-sensitive plan declares `required(Internal, security)` — same
   floor, security lens, still a fresh same-type session.
3. **Machinery.** `tools/lifecycle_planner.py` + shipped twin: delete
   readiness parsing and the External-tier validation for plans; a plan
   declaring an unknown tier draws a warning naming the closed vocabulary
   (advisory, per the standing direction). Tests updated:
   `test_lifecycle_contract.py`, `test_pilot_evidence.py`, and the
   `gate_manifest.json` fixture, plus a directed test that a legacy
   `required(External)` or `Plan readiness:` line in an *active* artifact
   warns and is read as `required(Internal)`.
4. **What does not change.** Proposal review: the External floor on the
   deliberate lane stays — the proposal is where different-type independence
   pays, because the design is still movable there. Code review: floor
   unchanged (independent context, never the implementing agent). Security
   Reviews attached to high-risk *surfaces*: unchanged wherever they attach
   to proposals or code; where one attaches to a plan, it is conducted as
   `required(Internal, security)`. The Maintainer may still *choose* to ask
   any additional reader for any artifact — a choice is not a tier, and
   removing the mandate does not remove the option.
5. **Archives are immutable.** Archived artifacts keep their recorded
   readiness tokens and External plan reviews as history; nothing is
   retro-edited. The tokens remain readable in longitudinal metrics and are
   refused nowhere.

## Rationale

* **The mechanism never once did useful work in its cheap direction.** The
  readiness vocabulary existed so an External proposal pass could grant a
  lighter plan review. Recorded outcomes: **19 `DISTINCT REVIEW REQUIRED`, 0
  grants** — every recorded use produced only the expensive branch. The toll
  bridge never opened; this removes the toll booth.
* **A plan is implementation detail, and implementation detail is the
  agents' lane** (expertise routing, `nimbleness-recovery` 1.2). External
  plan review re-litigates a design the proposal's External pass already
  read, at the highest per-round cost the project has — the plan corpus
  (median ~1,800 lines) outweighs the proposal corpus it restates.
* **The Internal floor is not a soft floor.** Fresh-context same-type review
  has caught real, shipping-grade defects in this project's record; what it
  trades away is a different failure lens, which the proposal-stage External
  read still provides where the design is actually at stake.

## Relationship to `convergent-lifecycle`

This proposal **goes further than** `convergent-lifecycle` §2 and, where they
conflict, **this one governs**: that proposal retires the reviewer *trigger*
but preserves declared `required(External)` plan floors and, per its RCL-06
response, binds its own derived plan to External review under the current
rule. If this proposal is **accepted first**, External plan review no longer
exists, `convergent-lifecycle`'s derived plan takes `required(Internal)`, and
its §2 floors-vs-trigger rule is read with "declared floor" meaning
`required(Internal)` and Security Review only. If this proposal is rejected,
`convergent-lifecycle` stands as written. The two do not need to merge: this
is a strict subtraction from either baseline.

## Evidence / verification plan

Doctrine and template edits pass the claim, link, and neutrality gates. The
planner change carries directed tests: the closed two-token vocabulary
accepted; a legacy External/readiness line warns and resolves to Internal; an
archived artifact with either token draws no warning. Falsification for the
review of this proposal: grep the post-change tree for `Plan readiness` and
`required(External)` across the **governing surfaces** — `AGENTS.md`,
`doctrine/`, `templates/`, both live `_template.md` files, `tools/`,
`scripts/`, `bootstrap/` — and the result must be empty. Append-only records
of active and archived deliberation artifacts legitimately retain the tokens
as history and are out of scope. The instrument is confirmed against the
pre-change tree, where the same grep matches **24 files** (as_of 2026-08-24,
archives and this proposal excluded).

## Signals the change is wrong

* A plan-stage defect ships that a different-agent-type read would plausibly
  have caught *and* the proposal-stage External read could not have — audit
  against the actual finding, not the counterfactual's flattery.
* The Maintainer finds themselves manually requesting extra plan readers
  often — the option is carrying load the tier used to carry; reintroduce
  deliberately, not by drift.

## Reviewer brief

One round expected; Internal floor (this is a subtraction whose design
question — should the tier exist — the Maintainer has already decided; the
review verifies the removal is complete and coherent, not whether to do it).
Seams: (1) the surface list above against the live grep — name any carrier
of the doctrine the removal misses; (2) the legacy-token warning path —
active vs archived handling; (3) doctrine wording — confirm no sentence
survives that makes External plan review *available as a requirement*, since
a dormant requirement is how the ratchet rebuilds.

## Review -- Codex (External) -- 2026-08-24

**Model**: GPT-5.6 (Codex)

Reviewed commit: e753882621b4a8da245eb4e350003084c1efaec7
Target: the complete opened contract, especially the security-plan form, legacy handling, convergent-lifecycle relationship, and removal evidence
Prior findings: none
Assurance path: high-assurance
**Tier**: External
**Findings**: raised (5 blocking)
**Plan readiness**: DISTINCT REVIEW REQUIRED

### Steelman

The Maintainer direction is unambiguous about removing External *plan* review,
and the proposal correctly keeps proposal-stage External independence and the
separate code-review floor. A smaller allocation model is viable, but only if
security review and migration of the live grammar remain explicit rather than
becoming ignored text after a tier name.

### Findings

#### RERP-01 — BLOCKING: `required(Internal, security)` is an ordinary Internal review, not a Security Review

The proposed security-plan spelling has no enforceable security semantics in
the current planner. `normalize_required_tier` deliberately reads only the
first word inside `required(...)`; its docstring calls remaining text a lens
annotation. `normalize_required_obligations` likewise sees one Internal-tier
clause unless `+` introduces distinct obligations. An ordinary Internal pass
therefore clears `required(Internal, security)` today, with no Security Review
record, protocol, high-capability role, or separate falsification obligation.
That contradicts item 4's claim that high-risk Security Reviews are unchanged.

Define the replacement security obligation: its record grammar, reviewer role
and fresh-context requirement, preflight, and predicate that blocks advancement
until it lands. It may be same-agent-type if the recorded Maintainer direction
requires that, but it cannot be an ignored annotation. Pin the directed pair:
an ordinary Internal pass cannot clear a security-plan requirement; the
required Internal Security Review record does. Keep proposal/code triggers
distinct and intact.

#### RERP-02 — BLOCKING: active and archived legacy records have incompatible grammars, not one warn-and-reinterpret path

`required(External)` is a plan header, while `Plan readiness:` is a
proposal-review field. The proposal says either line in an active artifact
warns and is read as `required(Internal)`, but a readiness finding cannot be
read as a plan declaration. The planner's shared External vocabulary also
validates proposal-review tiers and event records that must survive. Deleting
External-tier validation without a type-scoped replacement can invalidate the
External proposal floor item 4 keeps or discard archived metric evidence. No
inventory or migration rule states which record supplies the new Internal
requirement, how an inherited basis retires, or what `scan`, `next`, and metrics
report during the transition.

Specify separate dispositions for active External plans, active proposals with
readiness records, and immutable archives. Name parser branches and output
fields that remain proposal-External versus plan-Internal, then test each class
across `scan`, `next`, and longitudinal metrics. A warning cannot manufacture a
different artifact type.

#### RERP-03 — BLOCKING: the relationship section is stale and omits the accepted-scope migration it now requires

`convergent-lifecycle` is no longer awaiting review: commit `47315b6` records
the Maintainer Decision accepting Revision 2. Its accepted contract says a
declared `required(External)` floor is non-downgradable and that its own derived
plan takes that External review under the current rule. This proposal instead
uses a counterfactual — "if accepted first" — and declares the later plan
Internal. That is a change to accepted scope and a live review obligation, not
a choice between two unaccepted baselines.

Replace the hypothetical with a commit-bound migration: identify the accepted
commitments superseded, quote the Maintainer authorization allowing the
review-floor change, name the new plan declaration/linkage, and state whether
the former External obligation is waived or remains. A new rule can govern
future plans after acceptance, but cannot silently make itself the first
beneficiary or rewrite a sibling's accepted floor.

#### RERP-04 — BLOCKING: the falsification baseline is wrong and the grep cannot prove the claimed removal

The stated instrument does not reproduce its claim. At the reviewed commit,
the proposal's governing-surface query for `Plan readiness` or
`required(External)` over its named roots, excluding this proposal, matches
**17 files**, not 24. Its post-change empty-result test also cannot show that
External validation remains for proposal reviews/events while being removed
only for plans; lexical absence cannot distinguish correct type scoping from
deleting the shared vocabulary.

Publish the literal command, exclusions, and checked-in expected file list,
corrected to 17 or accompanied by the different measurement that yields 24.
Pair it with behavioral oracles: an External proposal review and archived
External event still parse, while a new plan receives the accepted legacy
disposition. Mutate each property in a way the grep misses and the oracle
catches.

#### RERP-05 — BLOCKING: the mandatory security preflight is absent

This proposal has no `#### Security preflight` section or N/A statement. The
template requires one or the other, and this is not credibly N/A: it changes how
a high-risk surface's Security Review is declared, selected, and allowed to
clear a plan. RERP-01 gives the concrete failure mode — an ordinary Internal
pass can impersonate the proposed security review.

Answer S1--S5 for the replacement security-review record and legacy parser:
classification source, mutation proving a standard Internal pass cannot clear
it, triggering command and artifact scope, failure direction, remaining
attacker capability, and the Security Review/current-contract verification the
implementation requires.

### Coverage and recommendation

**Covered**: the complete opened contract at
`e753882621b4a8da245eb4e350003084c1efaec7`; review-allocation and Security
Review rules in `AGENTS.md`, `doctrine/dual-review.md`, and `doctrine/roles.md`;
live and shipped templates; planner tier/multi-obligation parsing and review
predicate; the stated governing-surface grep; and the accepted
`convergent-lifecycle` Decision history.

**Not covered / low confidence**: no replacement parser, migration fixture, or
security-plan record exists yet, so proposed behavior cannot be executed. I did
not run the full suite; this is a pre-implementation review.

**Second-round recommendation**: recommended. Security-plan review and the
accepted-artifact migration must be testable before this subtraction is decided.

## Response + Revision 1 -- Claude -- 2026-08-24

All five findings **accepted**; RERP-01, -03, and -04 were reproduced before
acceptance (`normalize_required_tier` reads the first word of the first
parenthesised group — verified at `tools/lifecycle_planner.py:668-672`;
`convergent-lifecycle` accepted at `47315b6`; the stated governing-surface
grep returns **17** files, and zero active plans declare `required(External)`
— `grep -H 'Plan review' dev/plans/*.md` matches none).

| finding | disposition |
|---|---|
| RERP-01 | **Accept.** §2 of the contract below defines the security-plan review as a distinct, testable obligation with its own record; an ordinary Internal review provably cannot clear it. |
| RERP-02 | **Accept.** The removal is type-scoped and the three legacy classes get separate dispositions, each with a named oracle; a warning never manufactures a different artifact type. |
| RERP-03 | **Accept.** The hypothetical is withdrawn; §4 is a commit-bound migration quoting the Maintainer's authorization, exercising exactly the recorded-waiver path the accepted sibling's own amendment defines. |
| RERP-04 | **Accept.** Count corrected to 17; literal command and file list published; three behavioral oracles and the mutations the grep misses are specified. |
| RERP-05 | **Accept.** Security preflight answered below. |

On `Plan readiness: DISTINCT REVIEW REQUIRED`: under the now-accepted
`convergent-lifecycle` contract, the token is a preserved recommendation and
the tier is the Maintainer's to assign at the Decision.

### Withdrawn / superseded commitments

* The **24-file** falsification baseline — measurement error (broader roots
  than the stated scope); corrected to **17** under the published command.
* *"a legacy `required(External)` or `Plan readiness:` line in an active
  artifact warns and is read as `required(Internal)`"* — withdrawn; the two
  grammars are different artifact types and get the class dispositions in §3.
* The *"if this proposal is accepted first"* relationship hypothetical —
  withdrawn; superseded by §4's commit-bound migration.
* `required(Internal, security)` as a lens annotation — superseded by §2's
  defined obligation.

---

## THE COMPLETE CURRENT CONTRACT (Revision 1)

Supersedes the opened Proposal section in full. Origin, header fields, and
Rationale stand as opened.

### 1. One rule

A plan review is an **Internal, fresh-context review — always**. External
plan review ceases to exist as a tier, requirement, recommendation slot, or
escalation target. The proposal template's `Plan readiness` slot is deleted;
reviewers record no plan-tier recommendations of any kind. Unchanged:
the External floor on deliberate-lane **proposal** review; the code-review
floor (never the implementing agent); Security Reviews wherever they attach
to proposals or code; and the Maintainer's option to ask any reader for
anything — a choice is not a tier.

### 2. The security-plan review is an obligation, not an annotation (RERP-01)

A plan whose surface or triggers require security treatment declares
`required(Internal, security)`, which is a **distinct obligation**: it is
satisfied **only** by an appended `## Security review (Internal)` record —
authored by a fresh-context same-agent-type session acting in the Security
Review role (the role's high-capability floor and the security-review
protocol, including its trust-boundary checklist, apply unchanged) — and it
is **not** satisfied by an ordinary Internal review record, however clean.
The planner parses the second token as an obligation, not decoration.
Violation disposition follows the accepted `convergent-lifecycle` lanes
(warn on the standard lane; the deliberate lane keeps today's behavior).
**Pinned directed pair**: (a) security-declared plan + ordinary Internal
review → the obligation reports unmet; (b) the same plan + a Security review
(Internal) record → clears. Proposal-stage and code-stage Security Review
triggers are untouched.

### 3. Type-scoped removal, three legacy classes (RERP-02)

`External` remains valid vocabulary where it survives: **proposal** reviews
and **archived** records, including longitudinal metrics (where event-record
handling intersects the accepted `retire-event-blocks` contract, that
contract governs). Only the **plan-tier** meaning retires. Classes:

* **Active plans declaring `required(External)`** — measured **zero** at
  this revision (`grep -H 'Plan review' dev/plans/*.md`, command committed
  with the change). Should one exist at implementation time, it is warned
  and the **Maintainer re-declares its tier at its next transition** — never
  silently rewritten.
* **Active proposals carrying `Plan readiness` records** — the token is a
  preserved recommendation (already the accepted rule); the derived plan's
  tier is assigned at the Decision. The readiness field is removed from the
  template, not from history.
* **Archives** — immutable, parse as today, draw no warnings.

**Behavioral oracles** (each with a mutation the grep cannot see): (a) an
archived External *proposal* review still parses in `scan` and metrics —
catches deleting the shared vocabulary instead of scoping it; (b) a
readiness line in an active proposal is reported as recommendation, never as
a plan declaration — catches grammar conflation; (c) a new plan declaring
`required(External)` draws the legacy warning — catches silent acceptance.

### 4. Commit-bound migration for `convergent-lifecycle` (RERP-03)

`convergent-lifecycle` was **accepted** (`47315b6`); its Revision 2 binds
its derived plan to External review under the then-current rule, and its
floors rule makes a declared `required(External)` non-downgradable — *"short
of the standing deviation/allowance process,"* which its own amendment
defines as **the Maintainer, on the record**. This proposal's Decision, if
acceptance, **is that recorded waiver**, authorized by the Maintainer's
origin direction, verbatim: *"It is not, and should not ever, be required."*
Effect, bound to the accepted commitments it supersedes: the derived plan of
`convergent-lifecycle` declares `required(Internal)`; its separately
declared Security Review for the marker/conftest work **survives unchanged**
and is conducted per §2's form; nothing else in its accepted scope moves. If
this proposal is rejected, the External obligation stands as accepted.

### 5. Evidence / verification plan (RERP-04 folded in)

Doctrine and template edits pass the claim, link, and neutrality gates. The
falsification instrument, literally:
`grep -rl 'Plan readiness\|required(External)' AGENTS.md doctrine templates
dev/proposals/_template.md dev/plans/_template.md tools scripts bootstrap |
grep -v archive` — **17 files pre-change** (list committed as a fixture with
the implementing change; unclassified paths printed), **empty post-change**,
with §3's three oracles as the behavioral half the grep cannot supply. The
planner change carries the §2 directed pair and the §3 class tests across
`scan`, `next`, and metrics.

#### Security preflight (RERP-05)

* **S1 — Who supplied it?** The security-obligation token and its satisfying
  record are both repo-committed and reviewed; the record is appended by the
  Security-Review-role session, not by the plan's author — the classifier
  (the declared token) and the satisfier (the review record) have different
  authors, so no artifact clears its own obligation.
* **S2 — Can it fail?** Mutation: satisfy a `required(Internal, security)`
  plan with an ordinary Internal review record → the obligation must report
  unmet (§2 pair (a); run and recorded by the implementing change). Today
  this mutation *passes silently* — that is RERP-01, and the test exists to
  make it impossible to reintroduce.
* **S3 — What fires it, over what?** `python tools/lifecycle_planner.py
  scan` (and the shipped twin) over active plans; the directed pair and
  class oracles run in `bootstrap/tests/test_lifecycle_contract.py`'s
  updated suite under the standing Boundary-B command.
* **S4 — Which way does it break?** An unrecognized or malformed tier token
  warns and leaves the obligation **unmet** (fail-closed toward more review,
  not less); archived records are excluded from warning paths entirely, so
  the fail-closed direction cannot retro-flag history.
* **S5 — Who still wins?** An attacker with trunk commit access can append a
  fabricated Security-review record; that class is closed by review of the
  record's attribution and commit authorship (enumeration, not
  construction), unchanged from today's exposure for every review kind.
  The implementation itself changes lifecycle enforcement and takes the
  full current-contract Boundary B.

### 6. Archives are immutable

As opened: recorded readiness tokens and past External plan reviews remain
readable history, refused nowhere.

### Signals the change is wrong

As opened, plus: the §2 obligation is routinely satisfied late or nagged
about — the security-plan form is too heavy for its blast radius and needs
its own look, not silent skipping.

### Reviewer brief (round 2)

Closure verification: RERP-01 on §2's record grammar and pinned pair;
RERP-02 on §3's classes and oracles; RERP-03 on §4's quoted authorization
and named superseded commitments; RERP-04 on the corrected instrument;
RERP-05 on the preflight. The Maintainer assigns the derived plan's tier at
the Decision.

## Decision -- Anthony Kendall (Maintainer) -- 2026-08-24

### Preamble -- findings at the Decision

Recorded by the scribe at the Maintainer's instruction and **binding on the
implementing agent**. These are not review findings; item 2 could not have been
a review finding, because the fact it rests on was created after the round-1
review was written.

**1. Use the obligation grammar that already exists.** §2 introduces
`required(Internal, security)` and asks the planner to parse the second token
as an obligation. That is a new parser branch on a proposal whose whole thesis
is subtraction. `normalize_required_obligations` **already** reads
`required(A + B)` as *"two obligations and two distinct review passes"*, it is
documented at `doctrine/plans.md` > the `required(External + External Security
Review)` example, and it exists **because that exact form silently discarded
its second obligation** -- RERP-01's failure mode, already found and already
fixed once. **Declare the security-plan obligation as
`required(Internal + Internal Security Review)`.** §2's semantics are
unchanged: satisfied only by an appended `## Security review (Internal)` record
from a fresh-context same-type session in the Security Review role, never by an
ordinary Internal pass, with §2's directed pair pinned as written. What changes
is that no new grammar is invented, and the tested path carries it. If the `+`
form turns out not to express something §2 needs, say what and why in the
implementation record rather than reverting silently to the comma form.

**2. §4's migration is already discharged; no accepted scope moves.** §4 states
that this Decision *"is that recorded waiver"* for `convergent-lifecycle`'s
derived plan. It is not: that waiver already exists. On 2026-08-24, before this
Decision, the Maintainer waived the External floor in `convergent-lifecycle`'s
**own** Decision (`47315b6`), through the recorded-waiver path its own Amendment
defines, and its header already reads `required(Internal)` with the reasoning
quoted verbatim. **Consequence, and it is favourable**: accepting this proposal
changes **no accepted commitment of any sibling artifact**, so RERP-03's concern
-- that a new rule must not make itself the first beneficiary or rewrite a
sibling's accepted floor -- does not arise. This is a pure doctrine subtraction
with no migration. Record that in the implementation rather than performing a
waiver that has already happened; a future reader of §4 as written would believe
this Decision moved a floor it did not touch. `convergent-lifecycle`'s separately
declared Security Review for the marker/conftest work survives unchanged, as §4
says.

**3. The `Related` header was stale and is corrected in this commit.** It
described `convergent-lifecycle` as `awaiting-review`; it is accepted. Noted
because the same staleness produced RERP-03 one round earlier, and this is the
second generation of it in the same file.

**4. Verify the gate-manifest fixture change is a consequence, not a cover.**
`Touches` lists `bootstrap/tests/fixtures/gate_manifest.json`. `AGENTS.md` names
the gate manifest part of the install contract, a high-risk surface -- but that
path is the **test fixture**, not the shipped manifest, so no fence is placed
here. The implementer should nonetheless show the fixture edit falls out of the
intended parser change, rather than masking an unintended one.

**5. Three-in-a-row: acceptance silences the check that reports the remaining
defect.** `scan` refuses this artifact once, for a missing
`### Withdrawn / superseded commitments` under
`## THE COMPLETE CURRENT CONTRACT (Revision 1)`. The ledger exists (line 287);
the heading's `(Revision 1)` suffix makes the contract detector demand a second
one. From this commit forward `_is_immutable` short-circuits that check and the
artifact reports clean. This is the third artifact today with the same
wording-artifact violation and the same silencing. **The checker's exact-match
rule is now a standing defect in its own right and wants a successor proposal**;
fix the wording here, and stop paying it three times a day.

### The Decision

**ACCEPTED as revised (Revision 1), with the implementing agent addressing the
preamble above.** Authorization, quoted verbatim and visually isolated:

> "Please scribe my acceptance as revised, and with your recommendations."

**Accepted terms**: a plan review is an Internal, fresh-context review --
always. External plan review ceases to exist as a tier, requirement,
recommendation slot, or escalation target; the proposal template's
`Plan readiness` slot is deleted. Unchanged: the External floor on
deliberate-lane **proposal** review; the code-review floor; Security Reviews
attaching to proposals or code; and the Maintainer's option to ask any reader
for anything. Removal is type-scoped -- `External` stays valid for proposal
reviews and archived records -- with §3's three legacy classes and behavioral
oracles, and archives immutable.

**Plan review for this proposal's own derived work**: `required(Internal)`, as
the header declares. Under the rule this proposal lands, that is the only
tier there is.

**Scribed by** Claude (claude-opus-5) on explicit Maintainer instruction. The
scribe wrote no part of the authorization quoted above; the preamble is the
scribe's own finding record, requested by the Maintainer and adopted into this
Decision.
