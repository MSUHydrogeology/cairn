<!-- claim-check-allow: scripts/check_cairn.py -->
<!-- claim-check-allow-count: 1,294 lines -->
<!-- ^ Adopter-safety: this module doc cites Cairn's own `scripts/check_cairn.py`
     (which exists in Cairn but not in an adopter tree) and uses a
     thousands-grouped count as a *grammar example*, not a live claim about the
     adopter repo. The directives travel with the rendered copy so every
     installed adopter passes its own claim checker. -->

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

## The verify-before-asserting typology (A–E)

The discipline covers more than the checker's mechanical subset. Naming
the **categories of load-bearing claim** makes the right verification
obvious at write-time — each category has a different cheapest check, and
only one (E) is outside any scanner's reach:

* **A — code-shape.** Does this attribute / method / signature exist as
  written? *Check:* read the definition or `grep` it — never quote a
  signature from memory.
* **B — file-existence.** Does this path / file exist where cited? *Check:*
  the installed path checker (or `ls`); this is what the scanner hard-flags.
* **C — tree-history.** Did this commit / change land; is this the right
  SHA or range? *Check:* `git log` / `git show` — not recollection of what
  you committed.
* **D — counts.** How many tests / files / lines / call-sites? *Check:*
  compute it **live** (or cite a delta); a count from memory is the soft
  flag, and "consciously accept a point-in-time snapshot" is the only
  honest shortcut.
* **E — API-behavior-under-invocation.** What does this call *do* at run
  time — side-effects, ordering, atomicity, escaping, the artifact it
  emits? *Check:* a **small empirical probe** (invoke it in a scratch
  shell) or the library's behavioral contract — never infer from the API
  name or an adjacent call site. This is the costlier class above; **no
  scanner reaches it.**

Cutting across all five: the **self-contradiction cross-check** — before
asserting, confirm the claim does not contradict something else in the
same artifact (a count stated two ways, a path named differently above, a
"done" that an earlier line calls "deferred"). Self-contradiction is the
cheapest tell that a claim was asserted, not checked.

Also cutting across all five: a **forward / future-tense claim is probed
exactly like a present-tense one.** "Will exist", "the translator will
support X", "the fixture will be created", "the write will be atomic" — the
future tense is not a license to skip the check; it is the most common
*disguise* for an unverified A / B / E claim. Resolve it against the
**current** tree: if what the claim depends on exists now, probe it now; if
it genuinely does not exist yet, the claim is a **forward reference** and is
*marked as such* (e.g. the checker's forward-reference marker), never asserted
as present fact. A reviewer's claims-lens applies the same rule — a
"will work" gets the same probe as a "works."

The framing is **write-time, not review-time**: verify each category as
you write the claim (the cheap moment), so the claim enters the record
already true — not as something the reviewer has to catch.

## Template content

Merged into `AGENTS.md`:

> **Verify before asserting.** Before committing a proposal, plan,
> or doc, run the claim checker (`{{claim_check_command}}`) over
> it: it hard-flags broken repo paths and out-of-bounds line
> citations and soft-flags count claims. A hard flag is resolved
> before commit; a deliberate forward-reference is *marked*, not
> left to assert. A count that is a deliberate point-in-time
> snapshot — a verification count, a line count — is *consciously
> accepted* document-wide with a `claim-check-allow-count` directive
> (`<!-- claim-check-allow-count: <count>, <count> -->`, each token
> named exactly as number + tree-noun); it is the count sibling of
> the path markers, and a `claim-check-allow` directive is the
> file-scoped path equivalent.

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
Three knobs cover most local needs:

* **External-path allowance** (`--external-allow GLOB`, repeatable):
  some files exist to *describe other repositories* (a `case-studies/`
  write-up) and cite that repo's relative paths, which may collide with
  a local top-level dir name. Naming such file globs marks their
  path-claims as external so they are not resolved against the local
  tree -- the file-scoped sibling of the per-line `External-repo path:`
  marker. Its in-document equivalent is the `claim-check-allow`
  directive (`<!-- claim-check-allow: GLOB, GLOB -->`), which exempts
  the named path globs document-wide.
* **Conscious count acceptance** (`<!-- claim-check-allow-count:
  <count>, <count> -->`): a deliberate point-in-time count -- a
  verification snapshot, a line count -- is named in this
  document-scoped directive (each token exactly: number + tree-noun) so
  its soft flag is suppressed and recorded for audit. It is the count
  sibling of the path-marker grammar; a `claim-check-allow` directive is
  the path equivalent. Counts are extracted from the directive with the
  same detector the body scan uses, so the separator is irrelevant and a
  thousands-grouped count (`1,294 lines`) is named as one token.
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
