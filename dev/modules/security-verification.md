<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/rationale.md doctrine/coordination.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- ^ Adopter-tree destination: this is where the dispatcher lands in an
     ADOPTER's repository (this module's own InstallSpec dst). Cairn itself
     does not self-host the dispatcher (security-verification-activation's
     plan, "Cairn does not self-host the dispatcher"), so the path never
     resolves in Cairn's own tree; the directive travels with the rendered
     copy so every installed adopter passes its own claim checker too. -->
# Module: security-verification

**Selected when:** default-on — every adoption receives the dispatcher; an
adopter opts out explicitly with `modules_remove: [security-verification]`.
**Adds to:** a `## Security verification` standing-command note in
`AGENTS.md`, **plus a runnable dispatcher** the scaffold installs verbatim as
`run_security_verification.py` in the target's `scripts/` directory (see
"Reference implementation" below).

This module installs a **route, not any evidence**. It ships one
standard-library, fixed-registry, local-only dispatcher:
`scripts/run_security_verification.py`. Run it with `python
scripts/run_security_verification.py local`.

The dispatcher runs **no check itself**. It reads which security
capabilities the project has installed, looks each up in a **source-owned
registry** compiled into the dispatcher's own file — no adopter file (not
the profile, not the lockfile, not a policy file) can add an entry, a path,
an argument, or an environment variable to it — runs that capability's own
`local` runner as a child process under a hardened invocation, validates
what comes back, and prints one aggregate verdict.

## Template content

Merged into `AGENTS.md` (mechanically, via this file's `cairn:merge-target`
directive below):

> **Security verification.** `python scripts/run_security_verification.py
> local` runs every selected security capability's local evidence leg
> through the dispatcher's fixed registry and prints one aggregate verdict.
> A `NOT APPLICABLE` result means no capability has an admitted local entry
> yet — it is the absence of evidence, never a passing check. The
> dispatcher, its source-owned registry, its child result schema, its
> binding-mode schema, and every registry entry are **high-risk
> Security-Review surfaces**: a change to any of them takes a Security
> Review, the same tier as `bootstrap/_scaffold/` in Cairn's own
> `AGENTS.md`.

If `security-verification` is not installed, replace this section with `N/A:
security-verification not installed`. An unfilled slot is a review finding.

## `NOT_APPLICABLE` is not evidence

`NOT_APPLICABLE` is a state distinct from `CLEAN`. It means "no admitted
local capability was asked of me" — it is not evidence, and it must never be
reported, aggregated, or badged as a passing check. Its exit code, `0`,
means "nothing was asked of me," not "nothing is wrong." A tool that reads
exit `0` as a passing security gate before checking `aggregate ==
"NOT_APPLICABLE"` has misread the contract.

## The admission rule — six parts

An entry may be added to the dispatcher's registry only when **all six**
hold:

1. An **accepted capability proposal** covering the exact local evidence the
   entry claims.
2. A **reviewed plan with execution evidence** for that exact evidence mode
   (`offline` or `loopback` — never `deployed`, `credentialed`, `active`, or
   any other value; the set is closed at the type level, not merely
   validated at runtime).
3. A **complete lockfile mapping group** — runner, and (when the capability
   has one) policy, both tracked and hash-recorded.
4. **Schema and precedence tests** exercising the entry's admission fields
   and its interaction with the aggregate ladder.
5. A **Security Review of the registry change itself** — adding an entry is
   a Security-Review surface event, not a routine commit.
6. **The binding mode is part of what is admitted.** An entry is admitted
   *for a named* `policy_binding_mode`; changing an admitted entry's mode is
   a registry change and takes its own Security Review, not a follow-up
   commit. A `"living_state"` entry additionally requires the capability's
   own plan to carry execution evidence for the compensating controls that
   replace the digest (see "The binding-mode schema" below) — an executed
   run, never a design argument.

At v1 the shipped registry is **empty**: no capability meets this bar yet.
Every adopter's first run reports `NOT_APPLICABLE`.

## The aggregate ladder

Reused from `templates/modules/team-gated/run_security_audit.py`'s
precedent, plus a fifth, distinct state:

| Exit | Label | Meaning |
|---|---|---|
| `0` | `CLEAN` | Every selected capability's local leg is admitted and reports no finding. |
| `5` | `INCOMPLETE` | A selected capability has no admitted local registry entry, or a leg's own contract reports incomplete coverage. |
| `10` | `FINDINGS` | An admitted leg reports a finding. |
| `20` | `DEGRADED` | A binding check failed, or a child could not be trusted to have run cleanly. |
| (n/a, exit `0`) | `NOT_APPLICABLE` | No installed capability has an admitted local entry. **Not** a synonym for `CLEAN`. |

Precedence is `DEGRADED > FINDINGS > INCOMPLETE > CLEAN`: aggregation can
only ever **narrow**, never launder an incomplete or degraded leg into a
clean summary.

## The binding-mode schema

Every registry entry declares two apparatus-level bindings — the v1
question named four candidates (runner, policy, principal, scope); exactly
two are apparatus-level. **Principal and scope are child-policy semantics
with no apparatus field**, by decision, not by oversight: a capability's own
policy file states which principal or scope its checks cover, and the
dispatcher never reads that content.

* **`runner_binding_mode`** — a deliberately **one-member** closed set,
  `{"immutable_digest"}`. The runner is always parent-computed-digest bound
  against its lockfile record; a future "living runner" cannot appear by
  omission, only by a source edit widening this set, which is itself a
  registry-schema change and its own Security Review.
* **`policy_binding_mode`** — `{"none", "immutable_digest", "living_state"}`.
  * `"none"` — the capability has no policy file; `policy_repository_path`
    must be `None`.
  * `"immutable_digest"` — the parent computes the policy's SHA-256 and
    compares it with the lockfile's recorded hash, exactly like the runner.
    A policy under this mode that the lockfile marks `living_state: true` is
    a **misdeclaration**, refused (`DEGRADED`), not a pass.
  * `"living_state"` — for a policy an adopter is *expected* to fill (a
    strict-schema, `configured: false` stub become a filled, adopter-owned
    policy). The parent binds the policy's **existence**, its **regular-file
    and non-symlink status**, and the **presence** of a lockfile record
    flagged `living_state: true` whose destination is inside the
    dispatcher's own authoritative `_LIVING_STATE_DSTS` set — but does
    **not** compare the policy's content digest. The report records the
    policy as `"binding": "living_state", "digest_not_compared": true`, so
    the dropped property is **visible in the machine output**, never
    invisible. **This residual is stated, not hidden**: a filled policy's
    bytes are not lockfile-attested; its review channel is git (the policy
    is a tracked file, so a candidate change to it appears in the diff a
    reviewer reads), not a digest comparison.

**At v1, `_LIVING_STATE_DSTS` is empty and no `"living_state"` registry
entry exists.** No capability plan may add one until the Maintainer
ratifies the living-state narrowing (`B3`, shared between
`api-web-security-modules` and `security-verification-activation`).

## Recovery from INCOMPLETE or DEGRADED

* **`INCOMPLETE`** — a selected capability has no admitted registry entry at
  this Cairn version, or its own contract could not fully run (e.g. a
  network-egress-gated pass that was disabled). Enable the capability's own
  prerequisites, or wait for the capability to be admitted upstream; the
  dispatcher itself has no mechanism to widen coverage.
* **`DEGRADED`** — a runner or policy digest mismatch (the shipped file was
  modified after install — re-verify the install, or the file was
  legitimately upgraded and the lockfile needs a `verbatim_rehash`), a
  symlinked runner or policy (remove the symlink and restore the tracked
  file), a missing lockfile record (re-run the scaffold's upgrade path), or
  a child that timed out, exceeded the output byte cap, emitted invalid
  UTF-8/JSON, or reported a result whose identifying fields disagree with
  its registry entry (a capability-side bug — file it against that
  capability, not this dispatcher). `DEGRADED` never self-heals silently;
  each cause above is a distinct, named branch in the dispatcher's own
  source, not a single catch-all.

## Command separation is not actor authentication

A shell process cannot prove who invoked it. An agent with the operator's
terminal and credentials could run `scripts/run_security_verification.py`,
or any capability's own runner, directly — the dispatcher does not, and
cannot, distinguish a human process from an agent process. Its authority is
strictly **narrowing**: it can only ever refuse or downgrade a result, never
grant a capability an adopter file did not already select and Cairn's own
registry did not already admit. This is the same non-claim
`bootstrap/SAFETY.md` records for Cairn's own tree.

## Trusted-checkout scope

This is a drift / tamper tripwire on the adopter's **own trusted tree**, run
in the adopter's own dev loop or CI, over apparatus that is committed,
reviewed-as-code, and integrity-covered. It is **not** a reviewer for
untrusted code that can modify the apparatus itself — do not wire it into
untrusted-PR / fork CI, where a run from an attacker's checkout would
execute the attacker's own dispatcher and registry.

## Reference implementation

Enabling this module writes `run_security_verification.py` into the
target's `scripts/` directory (copied **verbatim** — no token substitution
over the code, and hash-pinned by the install lockfile). Standard library
only; no third-party dependency, no network egress of its own — a selected
capability's own runner may open a connection under its own `local` /
`deployed` split, which this module does not alter.

<!-- cairn:merge-target: AGENTS.md > security-verification -->
<!-- cairn:merge-content-start -->
**Security verification.** `python scripts/run_security_verification.py
local` runs every selected security capability's local evidence leg through
the dispatcher's fixed registry and prints one aggregate verdict. A `NOT
APPLICABLE` result means no capability has an admitted local entry yet — it
is the absence of evidence, never a passing check. The dispatcher, its
source-owned registry, its child result schema, its binding-mode schema,
and every registry entry are **high-risk Security-Review surfaces**.
<!-- cairn:merge-content-end -->
