<!-- claim-check-allow: scripts/foldback_export_scan.py -->
<!-- The cited path refers to the adopter-install location -- the
     module's scaffold mapping copies foldback_export_scan.py verbatim
     into the adopter's `<target>/scripts/`.  From Cairn's own checkout
     the path does not resolve (the source-of-truth lives at
     templates/modules/default-on/foldback_export_scan.py); exempted so
     the adopter-facing cite stays correct. -->

# Module: foldback-export-scan

**Selected when:** default-on (alongside the `fold-back-ledger`
module; the active-surfacing protocol's machine gate).
**Adds to:** a runnable export-scrub scanner installed at
`scripts/foldback_export_scan.py` in the adopter's target tree, plus
the active-surfacing protocol's reference in
`doctrine/fold-back.md` > "Active surfacing" (the protocol's
fail-closed Scrub step invokes this scanner).

The foldback-export-scan module operationalizes the **machine half**
of the export boundary's two-gate model.  The fold-back ledger is a
cross-repository export surface -- deployment content crossing into
public Cairn -- and the doctrine requires a fail-closed scrub before
any drafted issue / PR body crosses that boundary.  This scanner is
that scrub.

The companion **manual half** of the gate is the maintainer-signed
affirmation field in the Cairn issue / PR template (Component B of
the active-surfacing arc): the maintainer explicitly attests that the
two no-export classes regex cannot reliably detect (unpublished data
hints; proprietary domain detail in long-form prose) are clean.

## What the scanner covers

Five mechanical detector classes; each detector emits findings as
`file:line: [class] message` and non-zero exit on any finding:

* **`credentials`** -- assignment-pattern detectable secrets:
  `password = "..."`, `api_key = "..."`, `secret = "..."`,
  `token = "..."`, `AUTH_TOKEN=...`, and similar key=value shapes
  with a non-empty value of >= 6 chars.
* **`private-path`** -- user-scoped absolute paths that would identify
  the deployment maintainer or expose host structure:
  `/Users/<name>/`, `/home/<name>/`, `C:\Users\<name>\`,
  `/private/`, `/var/folders/`, `/tmp/<specific-name>`.
* **`ip-address`** -- IPv4 + IPv6 literals.  The maintainer
  bright-line covers **both deployment-internal AND remote-repo IPs**
  -- a literal in a drafted body would expose deployment topology or
  contributor IPs regardless of which side it came from.  An
  **RFC 5737 / 3849 documentation-IP allowlist** (`192.0.2.0/24`,
  `198.51.100.0/24`, `203.0.113.0/24`, `2001:db8::/32`) prevents
  legitimate documentation examples from false-positiving.
* **`internal-hostname`** -- network-local-convention TLD suffixes:
  `.local`, `.internal`, `.lan`, `.corp`, `.home`.  RFC 1918
  numeric IPs are covered by the `ip-address` detector if the same
  host is named numerically.
* **`proprietary-token`** -- **adopter-configurable** denylist.
  Default file: `dev/upstream/foldback_export_denylist.txt` (one
  token per line; blank lines and `#`-comments skipped); override
  via `--allowlist <path>`.  Case-sensitive word-boundary substring
  match.  The deployment maintainer enumerates the project
  codenames / client names / domain-specific terms that should not
  leak.  Empty / missing denylist = detector silent; the other four
  detectors still run (the scanner is not gated on the file's
  presence).

## What the scanner does NOT cover (manual classes)

Two no-export classes stay **outside the scanner's reach** because
no regex can reliably distinguish them from generic prose:

* **Unpublished data hints** -- "the client's marina sediment data"
  vs. generic "sediment data."
* **Proprietary domain detail** -- descriptive prose about
  client / project specifics.

These are covered by the **maintainer-signed manual-affirmation
field** in the Cairn issue / PR template (Component B of the
active-surfacing arc).  The protocol's two gates fire together: the
scanner is fail-closed, AND the maintainer signs the manual field.
Both must clear before the maintainer submits.

## Invocation

After the scaffold installs the module, the scanner lives at
`scripts/foldback_export_scan.py` in the adopter's target tree.  Run
from the deployment-repo root:

    python scripts/foldback_export_scan.py <draft-path>
    python scripts/foldback_export_scan.py <draft-path> --allowlist <denylist-path>

**Multi-file invocation** (the PR-shape filing case -- scan body +
every changed file in the diff together):

    python scripts/foldback_export_scan.py <draft-path> <file1> <file2> ...

The active-surfacing protocol invokes this as Step 4 (Scrub).  Exit 0
clean; exit 1 on any fail-severity finding in any file (fail-closed --
the maintainer dispositions findings before re-running or aborting);
exit 2 on usage error (file not found).  Info-severity findings
(see "Documented false-positive escape hatch" below) are reported but
do not contribute to the exit code.

## Documented false-positive escape hatch

A drafted body or changed file can carry a per-line marker that
suppresses every finding on that line:

    <token leak> <!-- foldback-accept: <rationale> -->   (Markdown)
    <token leak> # foldback-accept: <rationale>          (Python / shell)
    <token leak> /* foldback-accept: <rationale> */      (C / Java / etc.)

**Rationale is required** -- an empty `foldback-accept:` (with no
text after the colon) is itself a fail-severity finding.  Silent
waivers are not allowed; the marker exists for *documented*
dispositions where the maintainer has affirmatively reviewed and
accepted that the flagged token is a false positive.

When the marker fires, the scanner emits **info-severity** entries
naming each suppressed finding + the rationale, so the maintainer's
disposition stays visible in the run output.  A file with ONLY
info-severity findings (every flagged token suppressed) exits 0.
A file with any fail-severity finding remaining exits non-zero.

The marker is **line-scoped** -- a marker on line N suppresses only
findings on line N.  A marker on the line above a flagged token does
not extend; one marker per line of flagged content.

## Why this scanner exists (and how it differs from `content_scan`)

The team-gated `content_scan` module's scanner is a **prompt-injection
/ suspicious-content tripwire**: imperative overrides, egress
patterns, suspicious URLs, Unicode controls, homoglyphs, and
instruction-bearing HTML comments.  It exists to detect *adversarial
content* in agent-loaded prose -- a different surface from a
deployment-side export scrub.

The first iteration of this active-surfacing arc proposed reusing
`content_scan` as the export-scrub gate; empirical verification at
plan-review-time showed `content_scan` does NOT detect credential
patterns, private paths, IP literals, or proprietary tokens (those
are not its detector classes).  The two scanners are complementary;
a deployment that ships both modules can compose them in the active-
surfacing protocol if defense-in-depth is wanted, but
`foldback_export_scan` is the scanner the protocol's bright-line gate
binds to.

See Cairn's [`doctrine/fold-back.md`](../../../doctrine/fold-back.md) >
"The export boundary -- scrub before anything goes up" for the
underlying doctrine, and `doctrine/fold-back.md` > "Active surfacing"
for the protocol that invokes this scanner.

## Template content

Merged into the active-surfacing protocol (which lives in
`doctrine/fold-back.md` > "Active surfacing"); not into `AGENTS.md`.
The protocol's Scrub step (step 4) commits to:

> Run `python scripts/foldback_export_scan.py <draft-path>` against
> the drafted body's gitignored temp file.  Non-zero exit fails
> closed -- the maintainer dispositions findings (edit / documented
> false positive / abort).  The agent does not negotiate the gate.

A solo, single-deployment adopter that omits the `fold-back-ledger`
module also omits this scanner; the active-surfacing protocol
requires the ledger to operate, and the scanner is the protocol's
machine gate, so the two ship together by default.
