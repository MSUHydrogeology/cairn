# Module: claim-check

**Selected when:** default-on.
**Adds to:** a note in `AGENTS.md` documenting the
verify-before-asserting discipline, **plus a runnable checker** the
scaffold installs as `claim_check.py` in the target's `scripts/`
directory (see "Reference implementation" below).

The claim-check module operationalizes **verify-before-asserting**:
before a load-bearing claim about the repository — a file path, a
line citation, a count — an author checks it rather than asserting
it from memory. The checker does the mechanically-checkable subset:
it scans a Markdown proposal / plan / doc and hard-flags broken
repository paths and out-of-bounds line citations, and soft-flags
absolute count claims.

## What the checker covers — and the costlier kind it cannot

Most check-before-you-assert claims are about *what a thing **is***
— does this attribute exist, what does this function return, what
does this file contain — and a quick read or a grep settles them.
That is the mechanically-checkable subset, and it is exactly what
the installed checker covers: paths, line citations, counts.

A distinct, **costlier** class is about *what a call **does** at run
time*: its side-effects, ordering, atomicity or concurrency
guarantees, argument escaping, or the artifact / filename it
actually emits. A signature read confirms a method exists and its
return type; it does **not** confirm a runtime behavioral
guarantee. For a load-bearing behavioral claim, run a **small
empirical probe** — invoke the call in a scratch shell and observe —
or read the library's behavioral contract; never infer runtime
behavior from the API name or an adjacent call site.

**This second class is outside any scanner's reach, including this
one.** The installed checker does not — and cannot — verify a
runtime-behavior claim: it has no way to know what a call *does*,
only that a path or citation resolves. Treat the tool as covering
the first kind and the *discipline* (the empirical probe) as
covering the second; do not let the checker's clean exit stand in
for having verified a behavioral claim it never inspected.

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

**The scaffold installs a runnable checker.** Enabling this module
writes `claim_check.py` into the target's `scripts/` directory (copied
verbatim -- no token substitution over the code) and fills
`{{claim_check_command}}` to point at it. The script is vendor-neutral and **standard-library
only**: it hard-flags broken repo paths and out-of-bounds line
citations, and soft-flags absolute count claims. Run it via the
command the module installs:

> `{{claim_check_command}}`

Nothing to clone, port, or reimplement -- the default is a working tool.

**Adapting for project-specific conventions.** The checker derives its
top-level path set by listing the repo root (so it tracks your tree as
it grows) and recognizes the marker grammar (`Proposed path:` /
`Untracked path:` / `External-repo path:`) plus a `--root` override.
Two knobs cover most local needs:

* **External-path allowance** (`--external-allow GLOB`, repeatable):
  some files exist to *describe other repositories* (a `case-studies/`
  write-up) and cite that repo's relative paths, which may collide with
  a local top-level dir name. Naming such file globs marks their
  path-claims as external so they are not resolved against the local
  tree -- the file-scoped sibling of the per-line `External-repo path:`
  marker.
* The recognized count-nouns and markdown-context rules are small,
  readable edits at the top of the script if your conventions differ.

Cairn runs this exact script on itself: `scripts/check_cairn.py` imports
its claim-path checker (and adds link-checking on top), so the
methodology's own gate and the tool it ships an adopter are the same
code -- no drift between what Cairn preaches and what it hands out.

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

**Not to be confused with the work-intent pre-commit check.** The
deferred hook above is the **Markdown content gate** — a `pre-commit`
wrapping *this* checker (`{{claim_check_command}}`), which scans
proposals / plans / docs for broken path claims and out-of-bounds line
citations. It is **distinct** from the **work-intent pre-commit check**
shipped (opt-in) by the team-gated `coordination-tiers` module, which
warns when an about-to-be-committed edit touches a collision-prone path
with no active work-intent claim. Different surface (Markdown content vs.
coordination claims), different tool (`claim_check` vs. the intent tool);
one being deferred here does not contradict the other being shipped there.

**Clearing the flags this checker raises.** A `claim_check` hard flag on a
genuine forward-reference or sibling-repo path is cleared by inserting a
marker line (`Proposed/Untracked/External-repo paths:`) adjacent to the
token. Doing so inside an append-only proposal/plan section is the
sanctioned **claim-marker maintenance** carve-out (mechanical, additive-only,
its own labeled commit, typo-guarded) — see the lifecycle doctrine.
