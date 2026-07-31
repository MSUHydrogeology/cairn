# PROVENANCE.md — release provenance (Layer 1)

The first-order question an adopter should be able to answer is
**"which Cairn did I install, and where did it come from?"** A content
scanner inspects *what is present*; provenance proves *where it came
from*. Provenance is the foundation the other security layers rest on —
[`SAFETY.md`](SAFETY.md) Rules 7-8 (templates are agent-executed
instructions; the profile is operationally-trusted input), the
executable hardening in [`scaffold.py`](scaffold.py), and the
content-integrity scanner run by
[`check_cairn.py`](../scripts/check_cairn.py).

This is **Layer 1** of the four-layer agent-instruction-supply-chain
model. The blast radius is the reason it matters: Cairn's templates
become an adopter's `AGENTS.md` + `dev/` tree, auto-loaded by the
adopter's agents as governing instructions, so an upstream compromise
reaches every adopter at once. Provenance is how an adopter pins what
they are trusting.

## Controls

* **Named release artifacts.** Cairn ships tagged releases (e.g.
  `v0.2.0`), not a rolling `main`. A release is the unit an adopter
  installs and cites.
* **Signed tags or maintainer-approved release commits.** A release tag
  is signed, or the release commit is a maintainer-authored commit on
  the protected default branch. The adopter can verify the tag rather
  than trusting an arbitrary commit.
* **A published install manifest.** The exact set of files the scaffold
  installs is *emitted from the scaffold's own mappings*, not
  hand-maintained — run:

  ```
  python bootstrap/scaffold.py --manifest
  ```

  The manifest lists each `(source → destination)` pair (and whether the
  file is copied verbatim). It cannot drift from what the scaffold
  actually writes, because it is derived from the same `_CORE_MAPPINGS` +
  `_MODULE_MAPPINGS` the install uses. An adopter (or a reviewer) diffs
  the manifest against what landed in their tree to confirm nothing
  unexpected was written.

* **Scaffold from releases, not arbitrary branches.** Adopters should
  bootstrap from a tagged release checkout, not from a feature branch or
  an unreviewed fork. The scaffold prints a **provenance warning** when
  it is run from a `--cairn-root` whose git `HEAD` is not a tagged commit
  or has uncommitted changes; pass `--allow-dev` to silence it when
  developing Cairn itself. The warning is advisory — it never blocks an
  install — and it degrades silently when git is unavailable or the
  source is not a checkout.

## What this is not

* **Not cryptographic attestation.** Sigstore-style signed provenance
  attestation is a *future* enhancement; v0.2 provenance is
  named-releases + signed-tags + the derived manifest, which establishes
  origin without non-repudiation.
* **Not a content check.** Provenance proves *origin*; it says nothing
  about whether the content is safe. That is what Rule 7's by-class
  injection-review and the content-integrity scanner are for. The layers
  compose: provenance pins *which* Cairn, the scanner + review judge
  *what* it contains.

## Relationship to the release cut

These controls are coupled to the release-cut mechanics (tagging the
release, recording the version, minting the archival DOI). The cut
itself is a separate, maintainer-run step; this document states the
provenance posture the cut is expected to satisfy.

## Install-side provenance — the lockfile

Provenance has two sides. **Source-side** is the above: *which Cairn to
trust* (a named, tagged release). **Install-side** is the machine
lockfile `dev/.cairn/cairn-lock.yml` (see [`UPGRADE.md`](UPGRADE.md)) that the
scaffold writes *into the adopter's tree*: *which Cairn this tree actually
got* — the exact `cairn_commit`, the resolved profile, and the per-file
source / hash, all independently verifiable (the commit is `git
rev-parse`'d, the hashes are measured); plus `cairn_version` and, as of
this field's introduction, `source_repository` / `source_licenses` —
**declared**, not attested, values read from the source tree's
`CITATION.cff` (see `UPGRADE.md` > "Adding a lockfile field without
bumping the schema" for the full distinction). It makes "which Cairn is
this tree?" answerable from the tree itself, not from a human-maintained
manifest that can lag, and it is the ancestor anchor the `upgrade` 3-way
merge reads. A clean install from a tagged release (source-side) pinned
by a lockfile (install-side) is the fully-provenanced state.
