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
