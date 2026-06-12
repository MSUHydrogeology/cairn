<!-- cairn-internal-ref-allow: doctrine/dual-review.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
# Module: security-review

**Selected when:** the project has a non-trivial **trust boundary**
— a place where untrusted input meets the system (deserialization,
subprocess invocation, file or network I/O, path handling,
credential or environment-variable use). The gate is
**trust-boundary-first**: a small project with a real trust
boundary still selects this module. Project **complexity** tunes
the *cadence and depth* of the review, not whether the module
installs.
**Adds to:** the role roster in `dev/agent_collaboration.md` (the
Security Review focused-mode role, `roles.md`), plus a
`dev/` security-review protocol surface.

A named Security Review role with no doctrine home operates
ad-hoc — it fires when someone remembers, against no checklist. The
module gives the role a standing protocol so the review is
repeatable and its cadence is explicit.

## Template content

The focused-mode role, merged into the roster:

> **Security Review.** A focused-mode pass over the surfaces where
> untrusted input meets the system. It is not a standing
> implementation role; it is invoked on a cadence (below) and
> whenever a change adds or moves a trust boundary.

### Trust-boundary checklist (tool-neutral)

The review walks the project's trust boundaries. The checklist is
framed for scientific-computing projects and names *kinds* of
boundary, not specific libraries:

* **Deserialization** — loading objects, configs, or models from
  disk or the network. Is the format safe (no arbitrary-code
  execution on load)? Is the source trusted?
* **Subprocess invocation** — shelling out to solvers, compilers,
  or external tools. Is the command built from trusted parts, or
  can input inject arguments? Is the shell avoided where it can be?
* **Parsing** — reading structured input (config, data files,
  user-supplied parameters). Does the parser reject malformed or
  hostile input safely rather than crashing or mis-binding?
* **File and path handling** — paths derived from input. Are they
  validated against traversal (escaping the intended directory)?
* **Network I/O** — fetching remote data or services. Are
  endpoints, transport, and responses validated?
* **Credentials and environment** — secrets, tokens, and
  environment variables. Are they kept out of the repository, out
  of logs, and out of committed artifacts?

A change that adds, moves, or widens any of these boundaries is a
trigger for a Security Review pass regardless of cadence.

**Automate what a tool can check.** Where the language ecosystem
offers a static-analysis scanner for these boundary classes, wire a
**tool-neutral linter command into the surface's `verification
command`** (the field the readiness schema and restricted-
verification doctrine already define — `templates/modules/team-gated/legacy-agent.md`,
`doctrine/dual-review.md`), so the boundary is checked
automatically on every change and the focused-mode pass spends its
attention on what a scanner cannot judge. The module names no
specific tool; the adopter supplies the scanner their stack offers.

### Cadence

The review runs on a **periodic cadence** (a "last full review"
date the project records and refreshes) *and* on the
boundary-change trigger above. Complexity sets how often and how
deep: a higher-complexity or higher-stakes project reviews more
often and more thoroughly; a lower-complexity project with a single
trust boundary reviews lightly but still has the role and the
checklist. The cadence interval itself is the adopter's to set and
record alongside the protocol.

The role carries a **high-capability floor** by default
(`roles.md` > "Capability floors") — a security pass is a
high-stakes role.

### Injection-review procedure — review by input class

The trust-boundary checklist above names *kinds of boundary*; this
procedure is the **cold-start method** a focused-mode reviewer
follows so they do not have to re-derive the taxonomy each pass. It
generalizes a battle-tested scientific-computing protocol to
**tool-agnostic input classes**; an adopter extends the taxonomy
with their own stack's specifics (their serialization formats,
their solver binaries, their data libraries).

**Trusted-input vs user-controlled — the load-bearing triage.**
Every audited call site classifies one of two ways, and the
classification, not the API alone, decides whether it is a finding:

* **trusted-input** — paths and bytes under repo control: shipped
  fixtures, artifacts this project's own prior runs produced,
  configs round-tripped through the project's own writers.
* **user-controlled** — paths and bytes whose source the maintainer
  did not author: a collaborator's bundle, a downloaded archive, an
  externally-supplied data file, an incoming PR's contents.

An unsafe-by-default operation (object deserialization, shelling
out, dynamic evaluation) on a **trusted-input** site is acceptable
with a documented rationale; the **same** operation on a
**user-controlled** site needs a code-level fix or an explicit
decision that the threat model does not apply.

**Sensitive-input taxonomy (tool-agnostic, priority-ordered).**
The external-party inputs a reviewer walks first — each adopter
maps these classes onto their own formats:

1. **Structured config files** — the project's primary input
   format (YAML/TOML/JSON). Does the loader construct arbitrary
   objects? Is input size / alias expansion bounded (the
   "billion laughs" class)?
2. **Pickled state stores** — serialized in-memory state the
   project saves and reloads. Safe **only** when the project's own
   runs produced them; a third-party copy is arbitrary-code-on-load.
3. **Standard tabular / spatial data files** — CSVs, rasters,
   vector features parsed by ecosystem libraries. The library's
   parser surface (out-of-bounds reads, decompression bombs) is
   transitively part of the threat model.
4. **External simulator / tool binaries and their outputs** —
   downloaded executables the project shells out to, and the result
   files it parses back. Binary *provenance* (hashes / behavior) is
   a separate capability (see the scope fence); this pass covers how
   the project *invokes* them and parses their output.
5. **Data-fetch network calls** — remote data the project pulls.
   Is transport verified (no disabled TLS)? Is the host constrained
   and the response size bounded?

A focused-mode reviewer reports each risky call site with
file:line, its trust-class, a one-line attack scenario, and a
suggested remediation, in severity tiers (critical / important /
informational). Per the External Review Norms, the reviewer
surfaces the list; the author decides what to act on.

### v1 scope — a self-audit gate, not an untrusted-PR reviewer

The runnable stack this methodology installs (the content-injection
scanner and, for Python adopters, the gate orchestrator) is a
**self-audit drift tripwire on the adopter's own *trusted* tree**.
It runs in the adopter's **own** CI / dev loop over their **own**
committed tree to catch accidental drift and content-injection that
slipped past human review. The apparatus *and its policy inputs* —
the scanner, any allowlist or reviewed-residual baseline, the
audited-roots manifest, the lockfile records — are **trusted
input**: committed, reviewed-as-code, integrity-covered.

It is **explicitly not** a containment boundary or reviewer for
*untrusted code that can modify the apparatus itself* — a hostile
pull request that swaps the scanner, blesses a finding, or narrows
what is scanned and then reports success. **Operational guidance:
do not wire the audit stack into untrusted-PR / fork CI.** A gate
run from an attacker's checkout executes the attacker's version of
the gate; that trusted-runner-against-untrusted-candidate mode is
out of v1 scope. Reviewing genuinely untrusted incoming content
stays human-review work — scan it explicitly *before* an agent
ingests it, and read a clean result as **a tripwire, not a proof**.

## Cairn-side controls (the agent-instruction supply chain)

Cairn governs its **own** instruction supply chain with a four-layer
model — and these are real, landed controls the module's
"automate what a tool can check" guidance now points at concretely:

* **Layer 1 — release provenance.**
  `cairn/bootstrap/PROVENANCE.md`: named
  releases, signed tags / maintainer-approved release commits, a
  derived install manifest (`scaffold.py --manifest`), and "scaffold
  from releases, not arbitrary branches" (with a tool-side provenance
  warning).
* **Layer 4 — executable hardening.**
  The scaffold engine — the thin launcher + facade `cairn/bootstrap/scaffold.py`
  over a private `_scaffold/` engine package under `cairn/bootstrap/` (loaded
  **file-relative and fail-closed** against import hijack): a symlink/containment
  guard that refuses to write through a symlink or outside the target on
  **every** write, plus a Cairn-dev Bandit gate that scans the **whole engine
  package recursively**.
* **Layers 2/3 — content integrity.** The
  [`content_scan.py`](content_scan.py) scanner,
  run over Cairn's source prose and over scaffolded generated output by
  `cairn/scripts/check_cairn.py` — a **tripwire
  that forces human review, not a safety proof**.
* **Doctrine.** `cairn/bootstrap/SAFETY.md`
  Rules 7-8 name the property: templates are agent-executed
  instructions (reviewed by file class), and the bootstrap profile is
  operationally-trusted input.

An adopter inherits this posture for *their own* repository: the same
trust-boundary discipline applies wherever they ship agent-loaded
instruction files.

### Threat-model summary — the agent-instruction supply chain

A methodology repository that distributes agent-loaded instruction files
is a **software supply chain whose blast radius is every adopter's
agents**. The mainstream prompt-injection literature treats injection as
a *runtime* problem — one application's untrusted input reaching a live
model. Cairn surfaces a **static, supply-chain variant**: the
instructions ship as version-controlled prose and are obeyed wherever
they are forked, so an upstream compromise propagates to every downstream
adopter at once.

* **Assets** — the integrity of the templates *as instructions agents
  obey*; the adopter's repository and secrets a subverted instruction
  could target; the methodology's reputation as a trustworthy source.
* **Trust boundaries** — the fork/pull boundary (upstream → adopter); the
  profile boundary (a profile's token values → generated agent-loaded
  files); the human-review boundary (where obfuscation defeats a skim).
* **Defenses** — release provenance + by-class review gates +
  content-integrity scanning of both source and generated output, **not**
  runtime input filtering. The four layers have distinct jobs:
  provenance proves *origin*; the scanner + by-class review judge
  *content* (the scanner a high-noise **witness** that forces review,
  never a proof); the profile is **trusted input** by doctrine; the
  scaffold writes **only inside its target**.

Off-the-shelf runtime LLM-guard frameworks target a different threat
model (a live application's I/O) and are not a Cairn dependency; they
belong in an adopter's *application*. The lesson generalizes to any
project that ships `AGENTS.md`-style files for others to adopt.
