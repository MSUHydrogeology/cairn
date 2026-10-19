<!-- cairn-internal-ref-allow: doctrine/lifecycle.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
# Module: dual-review

**Selected when:** the team has two agent types, or multiple
humans — i.e. it can staff a structurally-independent reviewer.
**Adds to:** the review section of `dev/agent_collaboration.md`.

The invariant kernel runs *one* review tier — the same agent in a
fresh session, independence by time. This module adds the **full
two-tier Dual-Review model**: a second, structurally-independent
External tier, and the floors that keep both honest.

## Template content

Merged into `dev/agent_collaboration.md`:

> **External review.** A change touching a contract or a
> load-bearing assumption gets an External review in addition to
> the Internal pass. The External reviewer's floor is **structural
> independence**: a different agent type — a different model
> architecture, with different failure modes — or a human. Where
> the team is a single agent type, a human fills the External
> tier.
>
> The External reviewer's stance is *make it prove itself*: look
> for the reason the change should not land, and report honestly
> when there is none.
>
> Both tiers work through the shared **review sweep** — the generic,
> change-agnostic lens roster below — and close with the **two-part
> coverage line**; neither tier prescribes a second round. The
> External tier layers its independence stance *on top* of that shared
> base — the *make-it-prove-itself* read is what a different agent type
> brings that the sweep alone cannot — and its coverage line names the
> cross-type independence this pass did (or did not) supply.
>
> **The review sweep — the lenses.** A review that finds zero issues on
> a *complex* change is treated with skepticism, not relief: read as if
> a hidden bug exists and probe for it. The standing discipline is a
> **fixed, change-agnostic roster** every reviewer works through and
> **reports coverage on** — the most common first-pass miss is not a
> wrong judgment but an *unswept category*. The lenses:
>
> 1. **Claims** — probe every load-bearing claim against the *current*
>    tree ("exists / works / is available / is atomic / fails closed").
>    A **forward** claim ("will exist / will support") gets the *same*
>    probe as a present-tense one — run the check, never accept on
>    assertion.
> 2. **Production path exercised by tests** — the public entry point is
>    tested *through*, not just a helper or a stub of the thing that
>    breaks.
> 3. **Design completeness** — preconditions, invariants, edge cases
>    (empty / None / zero / single / N≫1 / mismatched units or CRS), and
>    failure modes are stated, not left implicit.
> 4. **Silent failure / fail-closed** — guards raise loudly rather than
>    degrading or returning empty; they cover all configs and stages;
>    any fail-open path is intentional, not accidental.
> 5. **Cross-document consistency** — scan governing docs, the roadmap,
>    and code/tests/doctrine for orphaned references to old or deferred
>    behavior, or an existing tool/path the change should use or update.
> 6. **Drift** — docs, examples, changelog, and commit claims match the
>    behavior that actually shipped.
> 7. **Lifecycle / process placement** — for a doctrine/process change:
>    *who* runs this, *when*, in *which* ceremony or serialization point;
>    the change has a home in the lifecycle, not just a rule.
> 8. **Domain / scientific validity & scope** — methods are grounded and
>    documented; scope has not quietly expanded; each new abstraction
>    earns its existence.
> 9. **Name the satisfier** — every finding states the test / guard /
>    doc / scope-cut / explicit `wontfix` that would close it. A finding
>    with no satisfier is an observation, not yet a finding. At archive
>    time each satisfier maps onto a disposition token
>    (`doctrine/lifecycle.md` > "Archive precondition"), and the mapping
>    is total: *test* → `guard`, *guard* → `guard`, *doc* → `accept`,
>    *scope-cut* → `accept`, *wontfix* → `wontfix`. A finding whose
>    satisfier is **none of the five** — real work that must happen, but
>    not in this artifact — is the `defer` case, and `defer` is the
>    Maintainer's call. Naming the satisfier and naming who pays for it
>    are then the same act.
>
>    **`scope-cut` means claim correction, and nothing else** — narrowing
>    an artifact's *stated claim* to match what it always did, with no
>    work removed. Removing previously proposed or accepted work is a
>    **scope reduction**: it takes the outcome test below, and only the
>    Maintainer may concede it.
>
> **The scope-reduction trap — the mirror of the clean pass.** Narrowing
> is the path of least resistance in review: it costs the reviewer
> nothing, reads as prudence, and can never be shown wrong, because the
> wider version is never built. Treat a proposed reduction with the same
> skepticism as a clean pass. A reviewer recommending one states **what
> is lost** and **why the narrower change still reaches the cause** —
> "this is too large" is not a finding. An author who resolves an
> underspecification finding by *removing* the work says why specifying
> it was rejected.
>
> **The outcome test.** Judge a narrowing against the baseline
> artifact's own commitments — the scope **as opened** before a
> Decision, **as accepted** after it — never against a summary of
> purpose written afterwards by the party doing the narrowing.
> **preserved** (every baseline outcome still delivered) owes nothing.
> **degraded** or **lost** both take a `**Scope delta**` declaration, one
> grouped remainder record per source artifact, and the Maintainer's
> explicit allowance; partial changes what residual is recorded, never
> who may concede it. A stronger outcome proposed *only during review*
> was never in the baseline, so declining it is not a reduction and owes
> no record.
>
> **Falsifiable coverage, not "checked."** A swept lens is credible only
> if its claim is *falsifiable* — it cites the file path, test node,
> line, or command output that backs it ("#2: `tests/foo.py::test_bar`
> calls the public entry"). A bare "#2: checked" is an *incomplete*
> review, not a pass.
>
> *(Canonical source + the fuller rationale — the staged evidence bar,
> the ritual-going signal, don't-telegraph-the-lens — live in Cairn's
> `doctrine/dual-review.md` > "Review expectations — the clean-pass
> trap".)* <!-- cairn-internal-ref: doctrine/dual-review.md reason=deeper-why pointer; the operative lens roster is transplanted above into the installed body -->
>
> The External tier's independence stance layers on top of this shared
> sweep.
>
> **Code review** — the implementation-side pass before a plan
> archives — takes the same independence floor: not the
> implementing agent. A different agent type is the strongest
> distance and is recommended wherever it can be staffed; no
> tier requires one.
>
> **A clean code review must show its work.** A pre-archive code
> review that approves does not clear the gate by *asserting*
> approval — a bare "unconditional approval" clears nothing. It
> carries a **falsification ledger**. The ledger is a lightweight
> four-part record:
>
> * **Probed edge cases** — the boundary / empty / out-of-range
>   inputs actually tried.
> * **Failure modes tested** — what was checked to fail *closed*
>   (explicit errors, validation gates), not only the happy path.
> * **Verification run (or consciously not)** — the commands run,
>   with results; or an explicit statement of what was *not* run
>   and why.
> * **Residual risks** — what remains unverified (integration
>   paths, platform-dependent behavior, deferred follow-ups).
>
> The ledger is what makes a clean pass *legible*: a reviewer who
> tried to break the change and reports honestly that they could
> not has cleared the gate; a reviewer who merely read it has not.

Without this module a project still reviews — at the kernel's
single tier; the module is what makes review *two-tier and
structurally independent*.
