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
  a fail-closed SHA-256 check of every file in your tree against the hashes
  **your own `dev/.cairn/cairn-lock.yml` records**, flagging any file that has
  changed since that lockfile was written. It detects *unilateral* modification;
  it is **not** tamper evidence, because the lockfile lives inside the tree being
  checked — an actor who rewrites a file and regenerates the lockfile over it
  verifies as `OK`. (Integrity
  verification is a Cairn-bootstrap operation run against your repo, like
  `scaffold` / `upgrade` — the verifier ships with Cairn's bootstrap, not
  into your tree.)
* **A clean scanner run as proof.** A clean `check_cairn` / content scan plus
  a by-class human injection review is the bar; the scanner alone never
  certifies a template safe.

## Release security checklist

**One command, and its output belongs in the release notes.**

```
python bootstrap/security_check.py
```

This is the **fail-closed** release gate. It is the whole **locally
machine-checkable** bar — not a first item in a list a Maintainer then has to
remember the rest of. (It is not the *whole* release bar: the contained floor
check `bootstrap/container/floor-gate.sh`, the release-authenticity ceremony,
and the by-hand review items are separate Maintainer-run steps that this
command does **not** dispatch.) Four phases; phase 1 stops the command, and
phases 2–4 are all attempted even after one fails, so a single run yields a
complete repair list:

1. **Repository state.** The invocation must name the checkout root, the
   worktree must be clean of tracked **and untracked** changes, and `HEAD`
   must resolve to a full commit id. The checking phases execute from a
   temporary detached worktree materialized directly from that commit's Git
   blobs and byte-verified before and after use, so ignored repository files
   and checkout filters cannot influence the verdict. The operator checkout
   is re-checked after the phases, so a candidate that changed mid-run cannot
   be reported as clean.
2. **Bandit + `check_cairn`.** Unlike the dev test (which skips locally when
   Bandit is absent), this **fails** if Bandit is missing, errors, reports a
   file it could not open, reports any unallowlisted MEDIUM+ finding over the
   shipped Python surface — every file the scaffold ships **byte-for-byte** as
   Python — or carries an allowlist entry the scan no longer reports at
   MEDIUM+ (a suppression that suppresses nothing is deleted, not kept).
3. **The engine suite in release mode.** `bootstrap/tests` with
   `CAIRN_RELEASE_GATE_ACTIVE` set, where a **skipped, xfailed or xpassed**
   outcome makes the session non-zero. A suite that exits 0 after a skip says
   nothing about the code that did not run. (Outside release mode a local skip
   stays a local skip — contributor behaviour is unchanged.)
4. **`python scripts/quality_gate.py`** — order-independence,
   vendor-neutrality, redundancy.

A phase that failed, errored, was **unavailable**, produced **incomplete
evidence**, or ran against a **changed candidate** is non-zero. An absent tool
never reads as a pass.

**Record the full `HEAD` the command prints**, alongside its output, in the
release notes. That commit id is what binds the evidence to something a reader
can fetch; without it the run is a screenshot of an unnamed tree.

### What this command does not do — the residual, and when it expires

The command is machine-checkable. **Running it, reading it, and recording it
are not.** Three residuals are accepted deliberately, not overlooked:

* **Omission is possible.** Nothing forces the command to be run before a tag
  is cut. Its only trigger is a Maintainer typing it; Cairn has no CI, no
  mandatory hook, and no tag wrapper.
* **No self-authentication.** The command does not verify its own bytes or its
  own process. A modified `bootstrap/security_check.py` reports whatever it
  was modified to report.
* **No cryptographic binding to the tag.** The printed `HEAD` is copied into
  the release notes by hand. Nothing signs the gate result, and nothing ties
  it to the signed tag object beyond that transcription.

Cairn will not pretend to mechanize the Maintainer's act, so these are named
rather than papered over with machinery that would only move the trust one
step. **They expire — and this becomes a real gap needing real
machinery — on any of:** a second release Maintainer; accepting release-path
contributions from outside the trusted set; adding forge automation that can
cut or publish a tag; or a check being missed in practice even once.

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
* **Lifecycle orientation escaping constrains shape, not meaning.** Externally
  sourced fields cannot create control sequences or imitate the stream's line
  and section grammar, but printable text is unchanged. An escaped payload is
  still legible, and an AI model may still interpret instructions contained in
  that one-line string.
* **Lifecycle relay coverage is deliberately partial.** The known sub-tool
  stdout relays remain unescaped because they carry another tool's structured
  stream, and git-derived lines are escaped but not length-capped. This is the
  set found during review, not a claim that every future relay is enumerated.
  Invalid UTF-8 from git is rendered with replacement characters; invalid
  UTF-8 in an artifact status degrades to `(no status line)` so it cannot abort
  the remainder of either lifecycle survey.
