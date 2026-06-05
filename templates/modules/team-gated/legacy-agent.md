<!-- cairn-internal-ref-allow: doctrine/coordination.md doctrine/dual-review.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
# Module: legacy-agent

**Selected when:** the codebase is **legacy** (the Age axis) — it
predates the methodology and carries untrusted surfaces. For a
**mixed** codebase the module scopes to the legacy surfaces only.
**Adds to:** the role roster in `dev/agent_collaboration.md`, plus
a new `dev/` surface-readiness map.

A retrofit needs apparatus a greenfield project does not: a
standing role for the untrusted surfaces, and a safe way to change
legacy behavior.

## Template content

The role, merged into the roster:

> **Legacy Agent.** A standing role responsible for the codebase's
> legacy surfaces — the regions whose behavior is load-bearing but
> not fully understood or tested.

### "Ready" means more than "has a test"

For legacy *scientific* code, the cheap three-label reading of
readiness is a trap. A surface with a passing test is not
automatically safe for an agent to change: the test may pin an
incidental output rather than the scientific contract, and a result
that *looks* right can still be wrong. So **"Ready" is redefined**
for legacy scientific surfaces to require all four of:

* **documented** — what the surface computes is written down;
* **characterized** — its *current* behavior is pinned by tests
  (the discipline below);
* **an executable verification path** — a command a reviewer can
  run to check a change, *and* someone who can run it (see
  "Restricted verification" below);
* **a known scientific contract** — inputs, outputs, assumptions,
  and units are stated, so a change is judged against intent, not
  merely against "tests still pass."

A surface missing any of the four is **Transitional** at best,
regardless of test coverage.

### The surface-readiness map and its schema

The module adds a **surface-readiness map**: one record per legacy
surface. The tier is the headline — **Ready** (changeable freely),
**Transitional** (changeable with care), **Frozen** (not changed
without a proposal) — but the record carries the fields that make
the tier *mean* something. These are fields an adopter fills, not a
fixed ledger to copy:

| Field | What it records |
|---|---|
| surface | the path / module / region |
| owning domain | who is responsible (if domain-agents is in play) |
| shared domains | other domains that read or depend on it |
| language | the implementation language |
| readiness tier | Ready / Transitional / Frozen |
| characterization status | are current-behavior tests pinned? |
| end-to-end coverage | is it exercised by an integration path? |
| doc home | where the surface is documented |
| scientific assumptions / unknowns | the known contract + the gaps |
| external-data dependencies | inputs sourced from outside the repo |
| verification command | the command that checks a change |
| verification owner | who can actually run it |
| allowed agent actions | what an agent may do here unsupervised |
| last reviewed | the date the record was last confirmed |

Relocated legacy material goes to an **attic** directory rather than
being deleted outright. Greenfield surfaces in a mixed codebase do
not carry this apparatus — they follow the kernel's absorbed-test
path.

### Characterization testing

Before changing legacy behavior, pin the *current* behavior with
tests, so the change is visible against a known baseline. A
characterization test is not a correctness test — it records what
the surface *does today*, which is exactly what a refactor must not
silently alter.

### The readiness map is shared-state governance

The map is read before every change to a legacy surface and
rewritten whenever characterization work lands — which makes it the
most collision-prone surface the legacy apparatus adds. Treat it as
a **shared-communication surface** (`doctrine/coordination.md`), not
a casually-edited doc:

* **The tier column is single-writer.** The Legacy Agent owns it;
  no other agent silently re-tiers a surface.
* **Tier changes go through a request.** A domain owner who lands
  characterization work appends a dated "characterization landed —
  tier-bump requested" note; the Legacy Agent confirms and moves
  the tier. Request and confirmation are separate acts by separate
  roles.
* **Owners may edit the non-tier fields of rows they own**
  directly (doc home, verification command, assumptions) — those
  are not the contested column.

### Single file vs. many — a concurrency tradeoff

A single monolithic readiness file is the simplest form, but for a
**highly concurrent team it is a collision hotspot**: every legacy
change reads it and characterization work rewrites it, so edits
serialize badly. Cairn names the tradeoff and lets the adopter
choose by concurrency level rather than mandating the single-file
form. The decentralized alternative is **per-surface records** (one
small file per surface under a readiness directory) or **readiness
frontmatter inside each target file**, aggregated into the map view
by a validation script. A low-concurrency team keeps the single
file; a high-concurrency team decentralizes.

### Restricted verification

The `verification command` / `verification owner` fields above are
the legacy-surface instance of a general discipline: when a reviewer
**cannot execute** a surface, review is weaker in practice than on
paper. The general rule — and its pre-framework fallback
(`verification owner = the Maintainer` until an executable path
exists) — lives in `doctrine/dual-review.md` > "Restricted
verification surfaces". A legacy surface in a language or
environment the reviewer cannot run is one such case; the readiness
record is where that gap is made explicit, per surface.
