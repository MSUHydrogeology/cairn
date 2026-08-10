<!-- claim-check-allow: dev/.cairn/api-access-policy.json, dev/modules/api-access-security.md, scripts/api_access_security.py -->
<!-- ^ ADOPTER-TREE destinations. This file is a template: the scaffold
     installs it as dev/modules/<name>.md in an adopter's repository,
     where these paths resolve. Cairn selects neither capability -- it has
     no API and hosts no site -- so they will never resolve HERE, and the
     exemption is the correct handling rather than rewriting a citation an
     adopter needs to be able to follow. -->

# Module: api-access-security

> **Team-gated, explicit selection only.** Not derivable from the six
> dimensional axes and absent from every preset — a project either has a
> cross-principal API to check or it does not, and no axis answer tells you
> which.

## What this capability is for

An endpoint that checks *authentication* and forgets *ownership* returns
principal A's object to principal B. That is **broken object-level
authorization** (BOLA), and it is invisible to a test suite that only ever
authenticates as one user. This module makes a project **state its intended
allow/deny facts** and then executes them.

It does **not** implement, generate, or infer an authorization model. OPA,
Cedar and OpenFGA remain architectural choices you own, and their policy-unit
tests are **required companion evidence** — this module checks that your
deployed behaviour matches what you declared, not that what you declared is
right.

## How to read CLEAN

> **CLEAN means the declared denial matrix held at the named target and time,
> no more.**

It does not mean the API is authorized correctly. A route absent from both your
OpenAPI document and your policy is not checked, by construction. A denial you
did not think to declare is not a denial this module tested.

**INCOMPLETE is not CLEAN.** A selected-but-unconfigured capability exits **5**
and says so. That is the state the installed stub ships in, deliberately: a
capability that reported CLEAN over an empty matrix would be worse than absent.

## The two legs, and the actor boundary

| Leg | Reaches | Methods | Who runs it |
|---|---|---|---|
| `local` | **loopback only** | GET/HEAD/POST/PUT/PATCH/DELETE | anyone, including an agent |
| `deployed-passive` | the declared HTTPS origin | GET/HEAD only | the **Maintainer**, by hand |

`python scripts/api_access_security.py local`

`python scripts/api_access_security.py deployed-passive --authorize-base-url <exact normalized base url>`

The deployed leg refuses unless that argument is **byte-for-byte** the
normalized base URL in your policy's deployed section. A trailing slash, an
upper-case host, an explicit default port, a punycode spelling, an added query,
or `http` for `https` all refuse.

**This is structural command separation, not actor authentication.** A shell
process cannot prove who invoked it. An agent with the Maintainer's terminal and
credentials could perform that act. The control is that the deployed leg is
**not reachable from the standing agent-facing command at all** — the activation
dispatcher's fixed registry admits only the `local` argv — and that the deployed
leg is `GET`/`HEAD` in code, so even a mistaken or malicious caller cannot write.

## The fixture requirement, and when local evidence is invalid

The `local` leg's target must be a **disposable, project-owned fixture** you can
destroy and rebuild.

> **Local mutation evidence is invalid if the fixture has any upstream route.**

The runner enforces the address and the credential namespace. It **cannot**
attest the fixture's internals: a loopback service that proxies to staging is
loopback from the socket's point of view, and a `DELETE` you thought landed on a
throwaway record can land on a real one. That is an open failure mode this
module does not close and no address check can.

## The policy

Lives at `dev/.cairn/api-access-policy.json`, generated from the installed stub.
It is a **tracked file**: its review channel is git.

**Principals are ordinals, never labels.** `p1`, `p2`, … and nothing else. The
credential environment-variable name is **derived** from the ordinal as
`CAIRN_API_P<N>_CREDENTIAL` and **cannot be supplied by policy** — a policy that
tries is refused. This is why no finding can name a person: there is no name in
the system to name.

**The local and deployed sections use disjoint ordinal sets.** An ordinal in both
is refused, which makes the two legs' credential namespaces disjoint by
construction — so the loopback leg cannot read a deployed credential even by
mistake.

**Every protected operation must declare both an allowed and a denied case**, and
an object-level operation must name two principals. A matrix of positive cases
alone is refused at schema level, because an API that authorized *everything*
would satisfy it.

Worked example:

```json
{
  "schema": "cairn.security.api-access-policy.v1",
  "configured": true,
  "local": {
    "base_url": "http://127.0.0.1:8099",
    "environment": "local",
    "principals": [{"id": "p1", "role": "owner"}, {"id": "p2"}],
    "operations": [
      {
        "id": "read-order", "method": "GET", "path": "/orders/1",
        "kind": "object",
        "cases": [
          {"id": "owner-reads", "principal": "p1", "expect": "allow",
           "status": [200], "require_present": ["/id"],
           "require_absent": ["/internal_note"]},
          {"id": "other-denied", "principal": "p2", "expect": "deny",
           "status": [403, 404]}
        ]
      }
    ]
  }
}
```

Set `CAIRN_API_P1_CREDENTIAL` and `CAIRN_API_P2_CREDENTIAL` in your own shell.
The runner never creates, stores, rotates, prints, or persists a credential, and
nothing in this document contains a real value.

## What a finding contains, and what it cannot

A finding carries a fixed check id, the operation, case and assertion ids you
wrote, ordinal principal ids, the method, a status **class** (`4xx`, not `403`),
a five-value **magnitude bucket**, and optionally a keyed fingerprint.

It carries **no** value, no byte or character length, no member or index count,
no header, no cookie, no body fragment, no certificate string, no redirect URL,
no exception text, and no credential. A finding contains **no integer at all** —
which closes exact cardinality as a *class* rather than field by field.

The **fingerprint** is HMAC-SHA-256 under a key generated fresh each run and
never printed, persisted, or reused. Two equal observations fingerprint equally
*within* one run, so a report is readable; across runs they differ, so a pasted
report cannot be dictionary-tested back to the value.

## Handling the report

The report is written to a freshly created private temporary directory verified
to resolve **outside** the repository, at owner-only permissions, so security
evidence cannot land in a commit by accident.

**It is sanitized but it is still security evidence.** It can reveal operation
names, principal relationships, and which of your declared denials failed.
Review it before sharing it and delete it under your project's evidence-retention
policy.

> **This protects report handling, not live process memory.** A debugger, a core
> dump, or another process running as the same user can read a credential out of
> the running runner. Nothing here changes that.

The `0600` report mode is a **POSIX** property. **No Windows run has established
the equivalent**, and until one has, treat the permission property as unverified
there.

## Recovery procedure

| Outcome | Exit | What to do |
|---|---|---|
| CLEAN | 0 | Nothing. Re-read *How to read CLEAN* before believing it means more. |
| FINDINGS | 10 | A declared denial did not hold. Fix the endpoint, not the policy — unless the policy declared the wrong thing, in which case say so in the commit. |
| INCOMPLETE | 5 | The policy is unconfigured. Fill the stub. |
| DEGRADED | 20 | The run could not produce evidence: a refused policy, a non-loopback target, a redirect, a peer that disagreed with the validated address, a TLS failure, a cap, a timeout, an absent credential, or an incomplete engine. The printed `code:reason` pair names which. **Do not** treat DEGRADED as CLEAN. |

A DEGRADED caused by `engine_incomplete` means the module's engine package is
partially installed. Re-run the scaffold upgrade for this module; do not edit the
installed tree by hand, which `bootstrap/verify_integrity.py` will report.

## Deliberately absent, and what returns through its own proposal

* **Remote mutation, in any form.** There is no `--allow-mutation`, no policy
  field that enables a non-loopback write, and **no reserved extension point for
  one**. A staging-mutation capability returns through its own proposal.
* **Cloud accounts and provider posture.** No AWS/Azure/GCP credential is
  requested, discovered, or accepted. That is a future `cloud-hosting-security`
  proposal with its own least-privilege, egress, retention and cost review.
* **Active scanning and penetration testing.** No crawl, no payload, no fuzzing,
  no ID inference. `deployed-passive` sends only declared `GET` and `HEAD`.
* **YAML OpenAPI and GraphQL inventory.** v1 compares operation ids against a
  committed OpenAPI **JSON** document only.
* **ZAP's API scan**, excluded because it is an active scanner: it sends attack
  payloads, which is out of scope for a capability whose deployed leg is passive
  by contract.

**Recommended companion, not installed:** Schemathesis, for contract and
authentication testing derived from your schema. It is a documented extension you
run yourself; nothing here installs or invokes it.

## What your integrity check does not mean

Your filled policy's bytes are **not** lockfile-attested. The install lockfile
classifies `dev/.cairn/api-access-policy.json` as living state, because the
correct-use state of an adopter-filled file differs from the recorded install by
design — hash-pinning it would report your ordinary work as tampering.

So the policy's review channel is **git**, and the deployed leg's authority comes
from the `--authorize-base-url` argument you type, **not** from the file. The
runner and its engine members are a different matter: they are verbatim,
hash-pinned, and **not** living state, so a one-byte edit to them is reported.

Separately, and worth knowing: the lockfile hash for any installed file is
computed from the bytes the installer is about to write. It answers *"has this
changed since install?"* and never *"is this what the Maintainer reviewed?"* The
first-use comparison against Maintainer-recorded hashes is what answers the
second question, and it is a **documented human procedure**, not code — which is
a weaker control than a mechanical one, and this document does not pretend
otherwise.
