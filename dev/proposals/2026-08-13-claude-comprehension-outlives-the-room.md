# The comprehension floor outlives the room

**Author**: Claude (Strategy)
**Model**: Claude Opus 5 (`claude-opus-5`)
**Date opened**: 2026-08-13
**Status**: reviewed
**Touches**: `doctrine/rationale.md` — Anchor 16, "The comprehension floor"
**Related**: `2026-08-13-claude-test-names-outlive-their-plans` and
`2026-08-13-claude-finding-tags-are-not-reasons` — the two operational rules
this principle generalises. **All three are intended to drain into one plan.**
**Plan review**: required(Internal) — a doctrine change, but a one-paragraph
extension of an existing anchor with two measured instances behind it

## Context

Anchor 16 states the comprehension floor, and scopes it to the reader **in the
room**:

> a decision surface the Maintainer cannot follow is not decidable

Every clause is decision-time: the Maintainer, now, deciding. The anchor closes
by bounding itself explicitly and naming one dimension it has not harvested —
calibrating communication to the recipient's domain expertise.

**There is a second unharvested dimension, and two measured instances of it.**

* **217 of 3546 test names** (`as_of 2026-08-13`) carry a plan coordinate:
  `TestP2AmendmentBScopeReduction`, `TestCF1AssurancePathOnTheEvent`.
* **262 occurrences of 37 finding tags** in `.py` comments and docstrings:
  `[FUR5]`, `[M2-1]`, `[S1]`.

Both were perfectly comprehensible **when written**. `FUR5` was clear to the
reviewer who had just read finding FUR5. `TestP2AmendmentB` was clear to the
agent executing chunk P2 that afternoon. Both were written for a reader who
will never exist again.

The Maintainer's report, from `dev/PLANNING.md`:

> *"They don't inform anyone anything. I don't know what FUR5 is."*

That is not a failure of the anchor as written. The Maintainer was not in the
room when the tag was written, and the anchor does not reach them.

## Proposal

Extend Anchor 16 with the temporal dimension. Roughly:

> **The floor extends past the room.** The reader who must understand a durable
> artifact is usually not the one who decided on it — it is whoever meets it
> next, with no plan open and no memory of the review. A name, comment or
> message written for the reviewer who had just read the finding is written for
> a reader who ceases to exist the moment the plan archives.
>
> So **a durable artifact must stand without the deliberation that produced
> it.** The record is a by-product of a good process, not a dependency of the
> code: an artifact whose meaning requires the record inverts that relation and
> decays at exactly the rate the record archives. Write the reason into the
> artifact; leave the coordinate to `git blame`, which is maintained.

### Grounding

Naur (1985), *Programming as Theory Building* (Microprocessing and
Microprogramming 15(5):253–261), is the direct antecedent and the strongest
available: a program's real content is the **theory** held by the people who
built it, and when they disperse the theory is lost even though the text
survives. Naur's conclusion is that the artifact cannot recover it — Cairn's
position has to be the weaker, actionable one: *write down what the artifact
cannot otherwise carry.*

**Verification owed at implementation**: the citation's volume, issue and page
range should be checked against the source before this lands. I am confident of
author, title, venue and year; I have not verified the pagination, and this
repository has been bitten by unverified specifics twice this week.

### Why this is a doctrine change and clears the rate-limit gate

It is a doctrine change — `doctrine/rationale.md` is the invariant kernel, and
the triage trigger fires. The rate-limit gate requires more than a single
incident:

* **two independent instances**, in different artifact classes (names, comments),
  both measured rather than estimated;
* **plus the Maintainer's own report** of hitting it as a reader.

That is recurrence, not one bad afternoon.

### Why doctrine rather than only `AGENTS.md`

The two sibling proposals put operational rules in `AGENTS.md`, which is right
and sufficient for names and comments. Neither prevents the **next** instance:
an error message that says "refused per S3", a log line, a module name, a
variable called `fur5_path`. A rule per artifact class is a rule per incident.

The principle is what generalises. That is what `doctrine/rationale.md` is for.

## Alternatives considered

* **Do nothing; the two operational rules suffice.** Rejected: they are rules
  about names and comments, and the failure is not about names or comments. It
  is about who the artifact is written for.
* **Fold this into the tag proposal's revision.** One artifact instead of two,
  and that proposal is being revised anyway. Rejected because it buries a
  general principle inside a document about comments, where nobody looking for
  the principle will find it. *(The Maintainer settled this: three proposals,
  one plan.)*
* **A new anchor (18) rather than extending 16.** Rejected: it is the same
  principle — comprehension as a precondition — reaching a reader the original
  scoping excluded. A second anchor would split one idea across two homes, which
  is the failure `doc-governance.md` exists to prevent.
* **State it in `doctrine/doc-governance.md` instead.** Rejected: that governs
  *where content belongs*, not *who it is for*.

## Evidence / verification plan

* **Both counts are measured** and reproduced in the sibling proposals;
  `as_of 2026-08-13`.
* **The scoping claim is checkable**: Anchor 16's operative norm is quoted above
  from `doctrine/rationale.md`, and its self-bounding paragraph names the one
  dimension it defers.
* **The Naur citation needs its pagination verified** before landing, as above.

**Tests required**: **none.** The two operational rules carry whatever
checkability exists, and both sibling proposals concluded no test can decide
whether a comment carries its reason. A doctrine anchor is prose that grounds
those rules; inventing a test for it would be the proxy-check failure
`doctrine/dual-review.md`'s mechanize-criterion warns against.

**Docs**: `doctrine/rationale.md` only. No `AGENTS.md` change here — the
operational reach is the siblings' business, and E3 of the tag proposal's review
already redirects it to the code-authoring conventions rather than `## Review`.

## Signals the change is wrong

* The anchor gets cited to justify verbose comments that restate obvious code —
  "writing the reason in" taken as licence to narrate. That would mean the
  extension needs the restraint anchor (17) named beside it as a bound.
* Agents stop citing findings anywhere, losing the traceability `git blame`
  depends on being able to reach. That would mean the commit-body discipline
  needs strengthening at the same time, since it becomes the only carrier.
* A future instance appears in an artifact class this principle plainly covers
  and nobody applies it — which would mean the principle is in the right file
  but not reaching authors, and the operational rules need to enumerate more
  classes after all.

## Review -- Antigravity (External) -- 2026-08-13

**Model**: Antigravity (Gemini 3.1 Pro)
**Tier**: External, different agent type from the author (Claude Opus 5)
**Reviewed commit**: `7daa275fff80144ed88f3d682e61effb65129470`
**Reviewed proposal blob**: `5773161c22a37294ea3412a3f3d1d62146f4aa57`
**Assurance path**: high-assurance
**Findings**: 4 raised (1 citation verification, 1 plan inheritance rule, 1 restraint boundary gap, 1 header wording cleanup)
**Verdict: REVISE.** The theoretical grounding (Naur 1985) and temporal extension of Anchor 16 are conceptually outstanding. However, the proposal should record the confirmed Naur pagination, clarify how the single combined plan inherits the doctrine proposal's Internal plan-review obligation, proactively pair the extension with Anchor 17 (Restraint) to prevent comment bloat, and clean up the header trigger justification.

### Findings

1. **[E1 -- Naur (1985) Citation Verification]**:
   - The proposal leaves pagination unverified at line 70.
   - *Verification*: Confirmed exact: Naur, Peter. (1985). "Programming as theory building." *Microprocessing and Microprogramming*, 15(5), pp. 253–261.
   - *Required satisfier*: Retire the unverified citation warning and record the confirmed citation.

2. **[E2 -- Single Plan Review Tier Inheritance]**:
   - The proposal notes that all three sibling proposals (`test-names-outlive-their-plans`, `finding-tags-are-not-reasons`, and `comprehension-outlives-the-room`) will drain into **one combined plan**.
   - *Issue*: The first two proposals declared `Plan review: not required`, while this doctrine proposal declares `Plan review: required(Internal)`.
   - *Required satisfier*: Explicitly record that the combined plan inherits `Plan review: required(Internal)` from this proposal (highest review tier among constituent proposals).

3. **[E3 -- Proactive Pairing with Anchor 17 (Restraint)]**:
   - Line 134 acknowledges the risk that "writing the reason in" could be cited to justify verbose narration in code comments.
   - *Required satisfier*: Explicitly pair the temporal extension text in `doctrine/rationale.md` with Anchor 17 (Restraint / Minimal Sufficiency) directly, stating that writing the reason in does not authorize redundant code narration.

4. **[E4 -- Header Justification Formatting]**:
   - Line 11 includes a softening clause (`but a one-paragraph extension...`).
   - *Required satisfier*: Simplify line 11 to `Plan review: required(Internal)` citing the `doctrine/` triage trigger cleanly.

### Summary Verdict
**Verdict**: **REVISE** (4 findings). Address E1–E4 in a short Response and Revised proposal.

