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
> **Code review** — the implementation-side pass before a plan
> archives — takes the same independence floor: not the
> implementing agent, and, for contract-touching work, a
> different agent type.
>
> **A clean code review must show its work.** A pre-archive code
> review that approves does not clear the gate by *asserting*
> approval — a bare "unconditional approval" clears nothing. It
> either carries a **falsification ledger** or is confirmed by a
> second independent different-agent-type pass. The ledger is a
> lightweight four-part record:
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
