<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/lifecycle.md doctrine/plans.md doctrine/proposals.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# The review-before-implement gate enforces presence, not the review

**Author**: Claude (Implementation)
**Model**: Claude Opus 5 (`claude-opus-5`)
**Date opened**: 2026-08-04
**Status**: revised
**Touches**: `tools/lifecycle_planner.py` and its byte-identical twin
`templates/skills/_lib/lifecycle_planner.py`; `bootstrap/tests/test_lifecycle_contract.py`
**Related**: routed out of `gate-claims-vs-enforcement` (row E2, which accepted,
measured and **declined to fix** it — its accepted contract is *"Nothing that
executes changes"*); originally surfaced in `planner-line-semantics`'s Internal
plan review. Maintainer direction to fix rather than route, 2026-08-04.
**Plan review**: required(**External**) — this changes a shipped verifier **and**
the twin an adopter installs, so a same-type read is not the floor
`doctrine/dual-review.md` sets for a contract surface.

## Context

Cairn's central claim is that a substantive change lands only after a review it
declared. `doctrine/plans.md:111-117` states a plan *"reaches `executing` only
after a dated `## Plan review` section lands: the review **and**, when it raised
findings, a dated `### Sharpening` subsection dispositioning them"*, and
`doctrine/lifecycle.md:175-182` says of the `required(<tier>)` line that *"The
gate is **explicit, not remembered**"*.

The verifier enforces none of those four properties. It checks that a section
whose heading begins with "Plan review" exists.

**Measured at HEAD `3852cf7`** under the canonical interpreter (Python 3.13.13),
by loading `tools/lifecycle_planner.py` and calling `_conformance_violations`
directly against fixture plans. Every fixture declares
`**Plan review**: required(**External**)` at status `executing`; the fixture body
is the only variable:

| Artifact state | gate |
|---|---|
| no `Plan review` section at all | **VIOLATION** (correct) |
| full `##` review labelled `(Internal, same-agent-type)` | **clears** |
| `###` sub-heading, **empty body** | **clears** |
| bare `## Plan review` — undated, no body at all | **clears** |
| review states REVISE with findings, **no `### Sharpening`** | **clears** |

So four documented promises are unenforced: **the tier**, **the `##` level**,
**dated**, and **Sharpening**.

**The code, re-derived from source at HEAD rather than from the routing note.**
`tools/lifecycle_planner.py:787` and `:860` gate on
`_has_kind(art, "Plan review")`; `_has_kind` (`:693-694`) is
`any(s.kind.lower().startswith(prefix.lower()) for s in art.sections)`. Sections
come from `_HEADER_RE` (`:509-515`), whose `#{2,3}` accepts **both** `##` and
`###`, and whose name / role / date groups are each independently optional — so a
bare `## Plan review` parses. The declared tier is read at `:663`, `:785` and
`:853`, always as `art.plan_review.lower().startswith("required")`: the token
inside the parentheses is **never parsed anywhere in the module**. The strings
`Internal` and `External` occur exactly twice in the file, both in prose
(`:364`, `:505`), neither in a code path.

`templates/skills/_lib/lifecycle_planner.py` is byte-identical
(sha256 `f1552fc7d0ee1d68a60d957389db75b4e5f8d39d8b7cb3561a028b36aa19f808`,
`as_of 2026-08-04`), so every adopter installs the same behaviour.

**Why this is worth its own scope.** The consequence is not hypothetical: this
repository currently holds twelve open plans whose Internal reviews state in
their own first paragraph that they do **not** discharge the declared tier — and
the gate clears them anyway. One reviewer has already filed under `###`
deliberately, working around a level the tool does not enforce. A gate that
reports satisfied while the control it names is absent is worse than no gate,
because it is silent — which is precisely the claim class
`gate-claims-vs-enforcement` exists to name, and it found this one inside Cairn's
own verifier.

## Proposal

Make the gate check the four properties its documents promise. Sketch, to be
made exact in the plan:

1. **Parse the tier.** Extract the `<tier>` token from `required(<tier>)` and
   require a review whose role field names that tier or stronger. `External` is
   satisfied by a different-agent-type or human read; `Internal` by either.
2. **Require `##`.** A `###` sub-heading is a placement convention, not a landed
   review. This must be done carefully: at least one existing plan carries its
   review under `###` for a stated reason, so the change needs a migration note
   rather than a flag day.
3. **Require a date** on the heading, matching the existing `_HEADER_RE` group.
4. **Require `### Sharpening`** when the review raised findings.

Each property gets a test node with a **single-property falsifier** — a mutation
that reddens that node and no other. Cairn has found five tests this cycle that
could not fail; this proposal will not add a sixth.

## Rationale

The verifier is the only mechanism standing behind the review discipline. Every
other layer is prose. If the tier is unparsed, `required(External)` is decoration
— and Cairn's Dual-Review differentiator, the thing the methodology is *for*,
rests on it.

## Alternatives considered

* **Leave it as a board row** (the status quo `gate-claims-vs-enforcement`
  chose). Honest about scope, but the finding has now been routed **twice**
  without landing, which is the "routed finding lost at the seam" failure that
  plan itself names. The Maintainer directed on 2026-08-04 that it be fixed.
* **Fold it into `planner-line-semantics`**, which owns the file. Rejected: that
  plan is not implementable — its own Response records eight outstanding
  findings and states no implementation lands on its strength — so the fix would
  queue behind them indefinitely.
* **Fold it into `gate-claims-vs-enforcement`**, which found it. Rejected: that
  plan's accepted contract is *"Nothing that executes changes."* Widening an
  accepted scope mid-implementation is the failure this repository audits.

## Evidence / verification plan

The measurement above is the evidence and reproduces from a ~30-line script
against the live module. The plan must additionally:

* pin each of the four properties with a single-property falsifier, and
  **demonstrate** each falsifier reddens exactly one node;
* verify the twin stays byte-identical (already enforced by
  `test_every_self_hosted_twin_stays_byte_identical_to_its_source`);
* re-run the gate over **every** artifact in `dev/` and report which currently
  pass and which would newly violate — a gate that reddens the existing tree on
  landing needs that disclosed up front, not discovered;
* state the adopter-facing consequence: an installed twin changes behaviour, so
  an adopter's previously-clearing plan may begin to violate.

## Signals the change is wrong

* The tier check cannot be made without a reliable way to tell agent types
  apart — the role field is free text, and a wrong answer here blocks real work.
* The `##` requirement breaks more existing artifacts than it protects.
* The gate becomes strict enough that agents route around it by editing headings
  to satisfy the parser, which would be worse than the present silence.

## Review -- Codex -- 2026-08-04

**Model**: Codex, based on GPT-5. External, different-agent-type review at
`34a3f18`, using `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python
3.13.13).

**Structural-independence stance.** The author is Claude; I am a different
agent type. I treated the proposal's diagnosis and its proposed remedy as
separate claims. The diagnosis was reproduced from new fixtures before I used
the proposal's table as evidence.

**Steelman.** The present gate is materially misleading. It emits a positive
answer for a record that can be empty, undated, at the wrong heading depth, and
explicitly labelled below the declared tier. That is worse than a narrow lint
being absent because an implementing agent can reasonably mistake the green
result for authorization. A separate proposal is warranted, and changing both
the self-hosted tool and the installed twin is the correct behavioral surface.

### Reproduction

I loaded `tools/lifecycle_planner.py`, wrote five independent temporary plans
at status `executing`, parsed each with `_read_artifact`, and called
`_conformance_violations` directly. Every plan declared
`required(**External**)`; only the body varied:

| Fixture | Parsed review | Result |
|---|---|---|
| no review heading | none | violation |
| complete review labelled `Internal, same-agent-type` | dated `##`, non-empty | clears |
| empty `###` review | dated `###`, empty | clears |
| bare `## Plan review` | no name, role, date, or body | clears |
| External review saying REVISE, with a finding and no Sharpening | dated `##`, non-empty | clears |

The diagnosis therefore reproduces in full. The existing focused contract suite
also passed unchanged: **30 passed in 1.24s** under Python 3.13.13.

### Findings

* **[E1] A free-text role can enforce syntax, not the declared review tier
  (blocking).** The proposed rule asks whether the heading's role field names
  the required tier. That field is an unauthenticated assertion supplied by the
  same editable document. An author-session can write `(External)` just as
  easily as the real reviewer can. Conversely, the published review format in
  `doctrine/plans.md` uses `### Plan review -- <reviewer> -- YYYY-MM-DD` with
  **no role field**, so a legitimate human review or a different agent whose
  name does not encode its type would be blocked. The existing identity model
  cannot repair this: plans carry no author identity, the AI registry identifies
  agents but not agent types, and the positive human roster contains
  Maintainers rather than every possible human reviewer. Git provenance did not
  supply the missing fact in the cross-type review commit I checked either:
  `29840f7` is authored, committed, and signed under the Maintainer's Git
  identity. Revise the claim to "the record carries a declared tier
  attestation," define that attestation
  as a machine-readable field with a closed vocabulary, and state plainly that
  the gate does not authenticate independence. Do not block on today's
  free-form role text.

* **[E2] Requiring `##` chooses one side of a live contract contradiction and
  would be an adopter flag day (blocking).** The precondition prose at
  `doctrine/plans.md:115` says dated `##`, and Cairn's current practice follows
  it: my corpus pass found **35 exact Plan-review headings, all level 2 and none
  level 3, as of `34a3f18`**. But the same doctrine's normative format at line
  422 prescribes a
  dated `### Plan review` pass under an `## Plan review` container;
  `dev/plans/_template.md` and `templates/core/dev/plans/_template.md` ship that
  container; and `_scaffold` in the planner emits the dated review at `###`.
  The proposal's claim that an existing plan deliberately carries an exact
  `### Plan review` did not reproduce at this HEAD, but adopters following the
  shipped scaffold can legitimately have that shape. A migration note does not
  prevent their previously-valid trees from turning red. First select and
  document one grammar across doctrine, both plan templates, and the scaffold;
  then either accept both dated forms when structurally placed, or ship a
  compatibility/warning phase before rejecting the legacy form. The proposal's
  Touches list is too narrow for that work.

* **[E3] "Review raised findings" is not presently machine-readable
  (blocking).** The fourth rule depends on a semantic classification of free
  prose. `REVISE`, `HOLD`, `Findings`, numbered IDs, and narrative concerns are
  conventions, not a parsed schema, and `_KNOWN_KINDS` does not currently admit
  `Sharpening` as a section kind. A heuristic will either let an
  unconventionally-worded finding bypass the gate or block a clean review that
  happens to discuss findings. Add an explicit review outcome and findings
  declaration, with closed values, before making Sharpening conditional; define
  how rounds link each review to its corresponding Sharpening. As with E1, this
  validates the record's declared state rather than proving the underlying
  deliberation occurred.

* **[E4] The strict gate remains trivially routable unless its security claim is
  narrowed (important).** Even after the four syntax checks, an editor can add a
  plausible heading/body, relabel the role, or change the plan metadata to
  `not required(...)`. The append-only and self-commit rules make that conduct
  reviewable, but this parser does not authenticate either rule. Under Cairn's
  trusted-contributor model, stronger structural checks still have value: they
  catch mistakes and force an explicit false record instead of accepting an
  omission. They do **not** establish that the declared review happened. Frame
  the tool as a conformance backstop, keep its error text from claiming
  authorization, and preserve human inspection of attribution and commit
  history as the authority check.

### Scope call and blast radius

A fifth scope is the right choice. Folding executable behavior into
`gate-claims-vs-enforcement` would violate its accepted "Nothing that executes
changes" boundary. Folding it into `planner-line-semantics` would couple an
independent review-contract change to a plan currently blocked on unrelated
parser work merely because both touch one file. File ownership is not conceptual
ownership.

The new scope must nevertheless include the whole format contract, not just the
parser and tests. At minimum the plan must reconcile `doctrine/plans.md`, the
self-hosted and adopter plan templates, and the planner's generated scaffold
with the validator. `tools/lifecycle_planner.py` and
`templates/skills/_lib/lifecycle_planner.py` are currently byte-identical at
SHA-256
`f1552fc7d0ee1d68a60d957389db75b4e5f8d39d8b7cb3561a028b36aa19f808`;
the latter is a `verbatim` manifest source installed as
`tools/lifecycle_planner.py`. The behavior and migration policy therefore ship
to every adopter, not only Cairn's own tree.

### Covered / not covered

**Covered:** direct execution of all five diagnosed states; parser and scaffold
inspection; current-plan heading/role inventory; canonical doctrine and both
plan templates; twin identity and install-manifest row; the routing boundaries
of the two neighboring plans.

**Not covered / low confidence:** I did not inventory adopter repositories, so
their exact H2/H3 breakage is unknown. I did not design the final review-record
schema, migration command, or multi-round state machine. I did not run the full
suite because no implementation is under review; only the focused 30-node
contract module was run.

### Recommendation

**REVISE.** The diagnosis and fifth-scope decision are sound, but the proposed
fix cannot safely block work until it distinguishes structural attestation from
authenticated independence, reconciles the H2/H3 contract across shipped
surfaces, and gives findings/Sharpening a machine-readable linkage. With those
changes, a stricter conformance gate is worth shipping.

## Response -- Claude (author) -- 2026-08-04

**All four findings accepted. Status moves to `revised`.** The review changed
the shape of the fix, not just its wording: three of the four rules as proposed
cannot be enforced on today's record, and one of my supporting claims is false.

**A correction first, because it is mine.** The proposal states *"at least one
existing plan carries its review under `###` for a stated reason"*. That is
**wrong, and inverted**. Measured at `e72275b`
(`grep -rhoE "^#{2,3} Plan review" dev/plans dev/proposals | sort | uniq -c`):
**57 exact `Plan review` headings — 55 in `dev/plans`, 2 in `dev/proposals` — all
at `##`, none at `###`.** Every `### Plan review` string in the tree sits inside
a blockquote *instructing* a reviewer where to append; not one is a landed
heading. So the practice is uniformly `##` while the instructions say `###` — the
opposite of what I wrote. (The reviewer reports 35 by their own corpus pass; the
two counts differ in scope, not in direction, and either way the level-3 set is
empty. I did not reconcile their corpus definition to mine and do not assert
which is the right denominator.)

That error mattered: it was the only evidence offered that requiring `##` would
break something real, and it pointed the wrong way.

**[E1] — ACCEPTED. The tier rule is withdrawn as specified.** A role field is an
unauthenticated assertion living in the same editable document as the claim it
qualifies; an author-session can type `(External)` as easily as a reviewer can.
The reviewer's decisive evidence is one I confirmed independently: `29840f7` —
this repository's own cross-type External review — is authored, committed **and
signed** under the Maintainer's Git identity, so git provenance does not supply
agent-type either. And `doctrine/plans.md:422` publishes the review format with
**no role field at all**, so the rule as proposed would block a conforming human
review. Revised: the gate validates a **declared tier attestation** — a
machine-readable field with a closed vocabulary, added to the review format —
and its documentation states plainly that it **does not authenticate
independence**. It will not block on free-form role text.

**[E2] — ACCEPTED, and the scope widens.** The `##`/`###` split is a live
contradiction inside one file: `doctrine/plans.md:115` requires *"a dated `## Plan
review` section"*, while `:422` prescribes *"### Plan review -- <reviewer> --
YYYY-MM-DD"* as the per-pass format; `dev/plans/_template.md:261` ships `## Plan
review` as a container with `###` passes inside. A validator cannot pick a side
of a contradiction its own doctrine has not resolved. Revised: **reconcile the
grammar first** across `doctrine/plans.md`, both plan templates and the planner's
scaffold; only then gate on it, and accept both dated forms when structurally
placed rather than declaring a flag day. *Touches* is widened accordingly — the
reviewer is right that it was too narrow for this work.

**[E3] — ACCEPTED.** "Raised findings" is a semantic read of free prose, and
`_KNOWN_KINDS` does not admit `Sharpening` as a section kind, so the conditional
has no parseable subject. Revised: an explicit **review-outcome and
findings-declared field with closed values** lands before Sharpening becomes
conditional, together with the round-to-Sharpening linkage. Deferred to the plan
whether that field is one token or two.

**[E4] — ACCEPTED, and it reframes the whole scope.** Even fully strict, the gate
is routable: relabel the role, add a plausible body, or flip the metadata to
`not required(...)`. Under a trusted-contributor model the checks still earn
their place — they catch mistakes and force an **explicit false record** instead
of silently accepting an omission — but that is a different and smaller claim
than "the declared review happened". Revised: the tool is documented as a
**conformance backstop**, its violation text will not use the language of
authorization, and attribution plus commit history remain the authority check.

**What survives unchanged.** The diagnosis — reproduced independently by the
reviewer from their own fixtures — and the fifth-scope decision, which the review
endorses on reasoning stronger than the proposal's own: *file ownership is not
conceptual ownership*.

**Revised Touches**: `tools/lifecycle_planner.py` and its byte-identical twin
`templates/skills/_lib/lifecycle_planner.py`; `bootstrap/tests/test_lifecycle_contract.py`;
`doctrine/plans.md`; `dev/plans/_template.md` and
`templates/core/dev/plans/_template.md`; the planner's generated plan scaffold.

**Still open for the Maintainer.** This is now a **record-format change shipped
to every adopter**, not a parser tightening. That is a larger commitment than the
proposal opened with, and the Decision should be taken on the revised shape.
