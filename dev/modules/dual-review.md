# Module: dual-review

**Selected when:** the team has two agent types, or multiple
humans — i.e. it can staff a read from a different agent type or
from a different person.
**Adds to:** the review section of `dev/agent_collaboration.md`.

Every install already carries the one review, the nine lenses of
the review sweep and the scope-reduction trap, in
`dev/agent_collaboration.md` > "The review sweep". This module adds
one thing: how a team with two agent types, or several people,
staffs a read the Maintainer has called. `AGENTS.md` > "Review"
holds the one definition of that call.

## Template content

Merged into `dev/agent_collaboration.md`:

> **Staffing a read the Maintainer has called.** The Maintainer
> names the artifact and the distance they want: a different agent
> type, a person, or a brief to try to break the work. Whoever
> staffs it follows that brief, answers the same three questions as
> any review, and says in the coverage line what distance the pass
> actually had. With one agent type, the person asked reads it;
> with two, the other type can. This module changes who is
> available to be asked. It never lets an agent pick a reviewer or
> add a read.
>
> **`scope-cut` means claim correction, and nothing else** — narrowing
> an artifact's *stated claim* to match what it always did, with no
> work removed. Removing previously proposed or accepted work is a
> **scope reduction**: it takes the outcome test below, and only the
> Maintainer may concede it.
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

Without this module a project still reviews: the one review, the
sweep and the trap are in every install.
