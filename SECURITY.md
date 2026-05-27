# Security

Cairn is a **methodology** — mostly prose (doctrine, templates, docs) plus
a small set of stdlib-only Python tools. This file is the public,
maintainer-facing security statement; the operational rules live in
[`bootstrap/SAFETY.md`](bootstrap/SAFETY.md) and the release-provenance
controls in [`bootstrap/PROVENANCE.md`](bootstrap/PROVENANCE.md).

## The threat model in one paragraph

Cairn's templates and doctrine are **forked into an adopter's repository
and auto-loaded by their AI agents as governing instructions** — Cairn is,
in effect, a *supply chain of agent-executed instructions*, and an upstream
compromise has a downstream blast radius across every adopter. So **template
integrity is a security property**, defended in four layers: release
provenance (which Cairn did I install?), source-integrity review *by file
class*, generated-output scanning (the artifact agents actually read), and
executable hardening of the shipped Python. The content scanner is a
**witness, not a proof** — it forces human review, it does not certify
safety. Full detail: `bootstrap/SAFETY.md` (Rules 7–8).

## Supported versions

Security fixes target the **latest released minor** and the `main` branch.
Adopters should **scaffold from a released tag, not an arbitrary branch**
(`bootstrap/PROVENANCE.md`), and pull doctrine forward via the documented
upgrade path rather than copying ad hoc.

## Reporting a vulnerability

Report suspected vulnerabilities **privately to the maintainer** (do not
open a public issue for an unfixed vulnerability): a hidden instruction in a
template, a way to make the scaffold write outside its target, a bypass of
the SSRF / content-integrity guards, or anything that could subvert a
downstream adopter's agents. Include a reproducer where possible.

## What an adopter should *not* trust blindly

* **A bootstrap profile from a third party.** The scaffold substitutes
  profile token values verbatim into agent-loaded files — treat a profile as
  **operationally-trusted input**: review it as code, diff it against the
  generated output, never run an unreviewed third-party profile
  (`SAFETY.md` Rule 8).
* **An unverified shipped script.** Run the shipped tools through a trusted
  interpreter — **`python scripts/x.py`**, never `./scripts/x.py` — so a
  hijacked `PATH` cannot substitute a shebang interpreter in a shared CI
  environment. After pulling or upgrading, confirm the installed tree still
  matches its recorded install: **from a trusted Cairn checkout / release,
  run `python <cairn>/bootstrap/verify_integrity.py --target <your-repo>`** —
  a fail-closed SHA-256 check of every file in your tree against its
  `dev/cairn-lock.yml`, flagging any post-install modification. (Integrity
  verification is a Cairn-bootstrap operation run against your repo, like
  `scaffold` / `upgrade` — the verifier ships with Cairn's bootstrap, not
  into your tree.)
* **A clean scanner run as proof.** A clean `check_cairn` / content scan plus
  a by-class human injection review is the bar; the scanner alone never
  certifies a template safe.

## Release security checklist

Before cutting a release, run — and record the output in the release notes:

* **`python bootstrap/security_check.py`** — the **fail-closed** release
  gate. Unlike the dev test (which skips locally when Bandit is absent), this
  command **fails** if Bandit is missing, errors, or reports any
  unallowlisted MEDIUM+ finding over the shipped Python surface, and also
  runs the Markdown self-check. A release must not be cut on a run that
  silently skipped the security gate.
* `python -m pytest bootstrap/tests/` — green (includes the dev Bandit gate
  and the content / generated-output scans).

## Documented residual risks (consciously accepted)

Recorded so a reviewer can tell *known and accepted* from *missed*, under the
stated threat model (no concurrent-filesystem attacker; no untrusted code
path):

* **`scaffold.py` write TOCTOU** — a small window between the
  `_assert_safe_write` containment check and the write; defense-in-depth
  only.
* **`check_cairn.py` `importlib` composition** — it loads sibling tools from
  **fixed, script-relative** paths (a deliberate dogfood), not from user
  input; not a dynamic-exec vector.
* **`link_check.py --check-external` DNS-rebind** — the SSRF guard validates
  each hop's resolved address against an `is_global` allowlist, but a
  rebinding resolver could change the answer between the check and
  `urllib`'s own connect. The probe is opt-in/off-by-default and blind (HEAD,
  response discarded); the residual is documented on the flag.
