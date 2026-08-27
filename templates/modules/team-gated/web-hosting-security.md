<!-- ^ ADOPTER-TREE destinations. This file is a template: the scaffold
     installs it as dev/modules/<name>.md in an adopter's repository,
     where these paths resolve. Cairn selects neither capability -- it has
     no API and hosts no site -- so they will never resolve HERE, and the
     exemption is the correct handling rather than rewriting a citation an
     adopter needs to be able to follow. -->

# Module: web-hosting-security

> **Team-gated, explicit selection only.** Not derivable from the six
> dimensional axes and absent from every preset — a project either hosts a site
> whose transport posture matters or it does not, and no axis answer tells you
> which.

## What this capability is for

A deployed site's security posture lives largely in response headers a browser
enforces and in the TLS it is served over. Those are set in hosting
configuration, change when someone edits a CDN rule, and are checked by nobody.
This module records **passive observations** of that posture against
expectations your project wrote down and reviewed.

## How to read CLEAN, and the rule that matters most

> **A local CLEAN is not a deployed CLEAN.**

The runner says so in its summary, in the report (`deployed_leg_executed`), and
in the dispatcher child document (`evidence_mode: loopback`). A fixture you
configured to be correct tells you your expectations parse and the checks are
live. It tells you **nothing** about the site your users reach.

CLEAN means: *every check that ran, ran against the target named in the policy at
the time it ran, and found what the reviewed expectation said it should.* Not
that the site is secure.

**INCOMPLETE is not CLEAN.** An unconfigured stub exits **5**.

## No grade, ever

This module **refuses to issue a letter grade**. A grade invites reading a
summary instead of the observations, and it compresses independent facts —
"HSTS is absent" and "a cookie lacks `SameSite`" — into one number that hides
which is which. Every check reports `present` / `missing` / `invalid` on its own.

## The two legs, and the actor boundary

| Leg | Reaches | Methods | Who runs it |
|---|---|---|---|
| `local` | **loopback only** | GET/HEAD | anyone, including an agent |
| `deployed-passive` | the declared HTTPS origin | GET/HEAD only | the **Maintainer**, by hand |

`python scripts/web_hosting_security.py local`

`python scripts/web_hosting_security.py deployed-passive --authorize-base-url <exact normalized https origin>`

The deployed leg is **unauthenticated in v1**, sends only declared `GET` and
`HEAD`, performs **no crawl** and sends **no payload**, and refuses unless
`--authorize-base-url` is byte-for-byte the normalized origin in your policy.

**This is structural command separation, not actor authentication.** A shell
process cannot prove who invoked it; an agent with the Maintainer's terminal could
type that argument. What the boundary buys is that the standing agent-facing
command cannot reach the deployed leg at all, and that the deployed leg is
read-only in code.

## What is checked

Against the declared `site_type` (`static`, `browser-app`, `data-api`):

<!-- cairn-accept: suspicious-url reason="prose naming the two URL schemes it contrasts; the scanner reads a backtick-quoted scheme prefix as a URL. No host is named." reviewer="Claude (Implementation)" date=2026-08-10 -->
* **HTTP → HTTPS upgrade, and the ordering of it.** An HTTP origin must reach
  HTTPS **before** it changes host. A redirect that moves host while still on
  `http://` has carried the request over a channel an attacker on the path can
  rewrite, and arriving at `https://` afterwards does not undo that.
<!-- cairn-accept-end: suspicious-url -->
* **Certificate chain and hostname validity**, through the platform trust store.
  There is no code path in this module that can weaken it — no `CERT_NONE`, no
  disabled hostname check, and no policy field that reaches either.
* **HSTS** on HTTPS responses.
* **CSP** where the site type requires one, including whichever directives your
  policy lists as reviewed expectations (`frame-ancestors` among them for a site
  that must not be framed).
* **`X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`.**
* **Cross-origin policy headers** where the site type requires them.
* **`Secure` / `HttpOnly` / `SameSite`** on every observed cookie.
* **Redirect and response origins** against your **exact** host allowlist.

## The policy

Lives at `dev/.cairn/web-hosting-policy.json`, generated from the installed stub,
and is a **tracked file** whose review channel is git.

<!-- cairn-accept: suspicious-url reason="documentation example: a loopback fixture address and RFC-2606 reserved example.org, in a policy example an adopter must be able to copy. Neither is a reachable third-party host." reviewer="Claude (Implementation)" date=2026-08-10 -->
```json
{
  "schema": "cairn.security.web-hosting-policy.v1",
  "configured": true,
  "local": {
    "targets": [
      {
        "id": "site",
        "http_origin": "http://127.0.0.1:9080",
        "https_origin": "https://localhost:9443",
        "site_type": "browser-app",
        "permitted_redirect_hosts": ["localhost", "127.0.0.1"],
        "expected_csp_directives": ["default-src", "frame-ancestors"],
        "expect_cookies": true
      }
    ]
  },
  "deployed": {
    "targets": [
      {"id": "prod", "http_origin": "http://example.org",
       "https_origin": "https://example.org", "site_type": "browser-app",
       "permitted_redirect_hosts": ["example.org", "www.example.org"],
       "expected_csp_directives": ["default-src", "frame-ancestors"]}
    ]
  }
}
```
<!-- cairn-accept-end: suspicious-url -->

A deployed target pointing at loopback is refused, so "deployed CLEAN" cannot be
manufactured by aiming the deployed leg at a local fixture.

## What an observation contains, and what it cannot

A target label, a fixed check id, the method, a status **class**, and
`present` / `missing` / `invalid`. Where a check must name what it looked for, it
names a **normalized token from your own reviewed expectation set** — never what
the peer actually sent.

It carries **no** full header, no `Set-Cookie` value, no certificate subject, no
body, no redirect URL, no query, no exception text, and no exact length or count.
Header and cookie values are reduced to their **directive and attribute names**
at the parse boundary, before anything can reach an output channel — a CSP value
can carry hostnames, nonces and report endpoints, and none of those belong in a
finding.

## Handling the report

Written to a freshly created private temporary directory verified to resolve
**outside** the repository, at owner-only permissions, so evidence cannot land in
a commit by accident.

**It is sanitized but it is still security evidence** — it reveals which of your
declared expectations your site fails. Review it before sharing and delete it
under your project's evidence-retention policy.

> **This protects report handling, not live process memory.** A debugger, a core
> dump, or another process running as the same user can read the running process.

The `0600` report mode is a **POSIX** property. **No Windows run has established
the equivalent.**

## Recovery procedure

| Outcome | Exit | What to do |
|---|---|---|
| CLEAN | 0 | Re-read *A local CLEAN is not a deployed CLEAN* before believing it means more. |
| FINDINGS | 10 | A reviewed expectation was not met. Fix the hosting configuration, or change the expectation and say why in the commit. |
| INCOMPLETE | 5 | Fill the policy stub. |
| DEGRADED | 20 | No evidence was produced: a refused policy, a non-loopback local target, a redirect outside the allowlist, a peer disagreeing with the validated address, a TLS failure, a cap, a timeout, or an incomplete engine. The printed `code:reason` pair names which. **DEGRADED is not CLEAN.** |

## Deliberately absent

* **Active scanning and penetration testing.** No crawl, no payload, no fuzzing.
* **Cloud and provider posture.** No hosting-provider credential is requested,
  discovered, or accepted. That is a future `cloud-hosting-security` proposal
  with its own least-privilege, egress, retention and cost review.
* **WAF / CDN configuration**, and **origin exposure behind a CDN** — a named
  residual, not a check. This module observes what the edge serves; it cannot
  tell you the origin is unreachable directly.
* **HTTP/3, mutual TLS, proxies, browser execution, and authenticated crawling.**

## Deferred adapters, and why each is deferred

* **`testssl.sh`** — a genuinely better local TLS analyser. Deferred until there
  is an exact pinned release, a checksum and provenance source, known
  ambient-configuration behaviour, a platform matrix, and a finding-to-exit
  contract. Adopting a shell script that reads the environment as a trust root is
  a supply-chain decision, not a convenience.
* **MDN HTTP Observatory** — deferred as an *adapter* and kept as a documented
  **manual second opinion**, because its scans have a public history: submitting
  a host publishes that you scanned it, and that is the project's call to make
  deliberately, not a side effect of running a check.
* **Trivy** — stays with `portable-security-sweeps`, which already owns the
  external-adapter provenance surface. It does not belong to two modules.

## What your integrity check does not mean

`dev/.cairn/web-hosting-policy.json` is classified as living state in the install
lockfile, because an adopter-filled file's correct-use state differs from the
recorded install by design. Its bytes are therefore **not** lockfile-attested:
its review channel is git, and the deployed leg's authority comes from the
`--authorize-base-url` argument you type, not from the file. The runner and its
engine members **are** hash-pinned and not living state, so a one-byte edit to
them is reported.

The lockfile hash for any installed file is computed from the bytes the installer
is about to write, so it answers *"has this changed since install?"* and never
*"is this what the Maintainer reviewed?"* The first-use comparison against
Maintainer-recorded hashes answers the second question, and it is a **documented
human procedure rather than code** — a weaker control than a mechanical one, and
this document does not pretend otherwise.
