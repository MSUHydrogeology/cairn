# Module: dual-language-tests

**Selected when:** the codebase is **multi-language** (the
Language axis) — more than one language carries load-bearing code.
**Adds to:** the test doctrine — a `tests/` guide in the adopting
repository.

A single-language project has one test framework and one test-tier
doctrine. A multi-language project needs its test architecture to
span languages without losing coherence.

## Template content

The module's test doctrine:

> **Multi-language test architecture.** Each language keeps its
> native test framework; the test-tier doctrine (unit / contract /
> integration / ...) spans them as one scheme, so a tier means the
> same thing regardless of language.
>
> **Cross-language seams are named.** The boundary where one
> language calls into another is a documented surface with its own
> tests — never an implicit join.
>
> **Port stewardship.** If a language transition is in flight, a
> port-stewardship note tracks which surfaces have moved, which
> are dual-maintained, and which are frozen pending the port.

The lifecycle and roles are unchanged — only the test architecture
gains the cross-language structure.

## One instance of a restricted verification surface

Multi-language code is the most common case of a **restricted
verification surface** — a surface the reviewing agent cannot fully
execute, here because it cannot run one of the languages. When the
reviewer cannot run a language, review of that language's code is
weaker in practice than its tier suggests.

The general discipline is not language-specific and lives in
`doctrine/dual-review.md` > "Restricted verification surfaces":
record a **`verification command`** (the exact command that checks
a change) and a human-gated **`verification owner`** (who can
actually run it) per surface, and apply the pre-framework rule that
an unverifiable surface's behavior changes carry `verification
owner = the Maintainer` until an executable path exists. Selection
on the Language axis is one trigger; a single-language project with
other execution asymmetries reaches the same doctrine through that
general home.

Concretely here:

> **Cross-language seams carry a verification command and owner.**
> The boundary where one language calls into another records the
> command that exercises it and the contributor who can run that
> command — so a change to the seam has a named, runnable check, or
> an explicit Maintainer-gated fallback when no reviewer can run it.
