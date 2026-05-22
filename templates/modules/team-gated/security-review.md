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
