# Complexity — simple ↔ complex

A codebase's **complexity** is how much can go subtly,
consequentially wrong — independent of how *large* it is. A small
codebase that computes a scientific result is complex; a large
codebase of plumbing may be simple. Complexity drives review
weight and verification depth.

## Scoring rubric

* **Consequence of a quiet error.** If a change is wrong but the
  software still runs, how bad is the outcome — a cosmetic glitch,
  or a wrong scientific answer that looks right?
* **Contract density.** How much of the code is a contract that
  other code, or other projects, depend on?
* **Scientific assumptions.** Does the code encode domain
  assumptions — numerical methods, units, physical models — that a
  reviewer must know the science to check?
* **Surface for untrusted input.** Does the software ingest data
  or files from outside the team?

## Positions

### Simple

* **Internal review** is usually sufficient; **External** review
  is reserved for genuinely contract-touching changes.
* A thinner evidence / verification plan in each proposal.
* The proposal template's "signals the change is wrong" prompt
  stays light.

### Complex

* **External review is mandatory** for any change touching a
  contract or a scientific assumption — the make-it-prove-itself
  tier is not optional where a quiet error is costly.
* The proposal template's **independent scientific check** is expected
  of every change that touches a scientific assumption or a published
  result: one check whose expected value neither the code nor its
  tests compute, shown to fail under the mistake it names. The block
  is gated on the change, not on this axis. Here, an unexplained "N/A"
  on a change that touches a computed result is a review finding.
* The full **verify-before-asserting** discipline applies — claims
  about the tree, the data, or the result are checked, not
  asserted from memory. The costliest claims are about *what a call
  does at run time* (side-effects, ordering, atomicity, the artifact
  it emits), which no scanner can confirm — see the A-vs-E
  distinction in the `claim-check` module: a runtime-behavior claim
  needs an empirical probe or the library's contract, not a
  signature read.
* The proposal template's "signals the change is wrong"
  subsection earns its keep, and a **Security Review** focused
  mode is available for the untrusted-input surfaces.

Most scientific software is complex on this axis even when it is
small — which is why complexity is its own axis and not folded
into size.
