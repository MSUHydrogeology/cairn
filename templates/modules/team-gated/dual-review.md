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

Without this module a project still reviews — at the kernel's
single tier; the module is what makes review *two-tier and
structurally independent*.
