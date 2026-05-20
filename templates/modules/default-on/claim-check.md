# Module: claim-check

**Selected when:** default-on.
**Adds to:** a note in `AGENTS.md` documenting the
verify-before-asserting discipline. The actual checker tool is
the adopter's to supply (see "Reference implementation" below).

The claim-check module operationalizes **verify-before-asserting**:
before a load-bearing claim about the repository — a file path, a
line citation, a count — an author checks it rather than asserting
it from memory. The checker does the mechanically-checkable subset:
it scans a Markdown proposal / plan / doc and hard-flags broken
repository paths and out-of-bounds line citations, and soft-flags
absolute count claims.

## Template content

Merged into `AGENTS.md`:

> **Verify before asserting.** Before committing a proposal, plan,
> or doc, run the claim checker (`{{claim_check_command}}`) over
> it: it hard-flags broken repo paths and out-of-bounds line
> citations and soft-flags count claims. A hard flag is resolved
> before commit; a deliberate forward-reference is *marked*, not
> left to assert.

The `{{claim_check_command}}` token is filled from the adopter's
profile YAML with whatever invocation runs their checker (e.g.
`python scripts/claim_check.py`).

The checker is a **discipline aid, not a gate** — the
verify-before-asserting habit is the doctrine; the tool only
shifts its cheap, mechanical part left, ahead of review.

## Reference implementation

Cairn ships the discipline (this module, the `{{claim_check_command}}`
token, the `AGENTS.md` note) but does **not** yet ship a generic
checker script. The methodology's reference implementation lives at
[`modflow_tools/scripts/claim_check.py`](https://gitlab.msu.edu/hydrogeology/code-projects/modflow_tools)
— roughly 200 lines of Python that hard-flags broken repo paths
and out-of-bounds line citations, and soft-flags absolute count
claims. Adopters have two paths:

* **Copy and adapt the reference**: clone the file from the
  modflow_tools repo into the target project's `scripts/` (or
  `tools/`, or wherever the project keeps utility scripts) and
  point `{{claim_check_command}}` at it. The reference is
  vendor-neutral Python; the patterns it recognises may need
  light editing for project-specific markdown conventions.
* **Write your own**: a checker as small as a regex pass over
  Markdown headings and link targets suffices for the discipline.
  Use the reference as a behavioral spec rather than as code.

A generalized, in-tree reference script that the scaffold installs
to a target's `scripts/` directory is queued as a future Cairn
enhancement; see Cairn's own roadmap for the follow-up.

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
