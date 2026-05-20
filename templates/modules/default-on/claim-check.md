# Module: claim-check

**Selected when:** default-on.
**Adds to:** a `scripts/`-level write-time checker, plus a note in
`AGENTS.md`.

The claim-check module operationalizes **verify-before-asserting**:
before a load-bearing claim about the repository — a file path, a
line citation, a count — an author checks it rather than asserting
it from memory. The checker does the mechanically-checkable subset:
it scans a Markdown proposal / plan / doc and hard-flags broken
repository paths and out-of-bounds line citations, and soft-flags
absolute count claims.

## Template content

The module ships the checker as a `scripts/`-level tool,
generalized from the methodology's reference instance. The note
merged into `AGENTS.md`:

> **Verify before asserting.** Before committing a proposal, plan,
> or doc, run the claim checker (`{{claim_check_command}}`) over
> it: it hard-flags broken repo paths and out-of-bounds line
> citations and soft-flags count claims. A hard flag is resolved
> before commit; a deliberate forward-reference is *marked*, not
> left to assert.

The checker is a **discipline aid, not a gate** — the
verify-before-asserting habit is the doctrine; the tool only
shifts its cheap, mechanical part left, ahead of review.

## Out of scope (deferred)

A **git `pre-commit` hook wrapping `{{claim_check_command}}`** was
floated during Phase 2 of the Cairn methodology repo construction
and is deliberately deferred from v1:

* The "discipline aid, not a gate" framing above is load-bearing —
  a pre-commit hook would convert the checker from advisory into
  blocking, and an honest forward-reference (a `Proposed path:`
  citation, a count expressed as a delta) would fail the hook
  unless the hook learned the same exemptions the doctrine carries.
  That apparatus is its own design problem, not a one-line wrap.
* The discipline already lands without it: the checker is invoked
  in the goodnight routine and at proposal / plan write-time, the
  cheap moment.  A hook would catch the rare case of an author
  who skips both — at the cost of churn for the common case.

If a future adopter wants the hook anyway, an opt-in version
running with `--fail-on-soft` only when the user installs a
project-side `.git/hooks/pre-commit` is the right shape; we have
not specified the exemption protocol it would need, and the
specification is a Cairn follow-up rather than a bootstrap-time
choice.
