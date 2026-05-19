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
