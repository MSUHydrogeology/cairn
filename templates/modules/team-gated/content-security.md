# Module: content-security

**Selected when:** the team's agents **auto-load text files from the
working tree** (Markdown, `dev/` artifacts, incoming-PR diffs) as context or
governing instructions, and the team wants a tripwire against
prompt-injection / obfuscation reaching those agents. Team-gated.
**Adds to:** a content-integrity note in the docs guide (and a
cross-reference from `dev/agent_collaboration.md`), **plus a runnable,
stdlib-only scanner** the scaffold installs verbatim as `content_scan.py`
in the target's `scripts/` directory.

An adopter's agents ingest files an outsider can influence — a Markdown doc
in a contributor's PR, a pasted-in spec, a vendored README. A
**static-content variant of prompt injection** rides those files:
imperative-override phrases, egress instructions, instruction-bearing HTML
comments, and *invisible* obfuscation (zero-width characters, bidi controls,
homoglyph/mixed-script tokens) that a human skims past but a parser ingests.
This module ships the scanner that flags them **before** an agent reads the
file.

## Template content

Merged into the project's docs guide:

> **Scan untrusted text before agents ingest it.** Files that enter the
> working tree from outside the team — PR diffs, pasted specs, vendored
> docs — are scanned by `python scripts/content_scan.py <files>` for
> prompt-injection and
> obfuscation patterns (imperative overrides, egress-to-URL, suspicious
> URLs, zero-width / bidi / homoglyph unicode, instruction-bearing HTML
> comments) before an agent is pointed at them. A hit is a **tripwire that
> forces human review, not a proof of compromise**; a reviewed, legitimate
> hit is cleared with an inline `cairn-accept <pattern-id> reason=…` marker.

## Reference implementation

Enabling this module writes `content_scan.py` into the target's `scripts/`
directory (copied **verbatim** — no token substitution over the code). It is
vendor-neutral and **standard-library only**. Run it over specific files or
a PR's changed set:

> `python scripts/content_scan.py <file> [<file> ...]`

Nothing to clone or reimplement — the default is a working tool. The scanner
is a **witness, not a safety proof**: a static pattern set is high-noise and
incomplete *by design* (semantic injection evades any fixed pattern set), so
it forces human review and never certifies a file safe.

## The self-audit runner (`content_scan_runner.py`)

Alongside the raw scanner, the module installs a **standard-library-only
advisory runner** that turns `content_scan.py` into a repeatable self-audit
pass over your project's whole agent-loaded surface. Run it with no arguments:

> `python scripts/content_scan_runner.py`

It resolves the audited set, scans it, compares each flag against a reviewed
baseline, and prints a fail-closed result. It is the content-scan half of the
security stack; the Python `python-security` module's orchestrator composes it
with `pip-audit` + bandit, but it runs standalone with no dev dependency.

**Self-audit scope.** The runner is a drift / content-injection tripwire on
your **own trusted tree**, run in your **own** CI or dev loop. The apparatus
*and its policy inputs* — the runner, the scanner, the allowlist, the reviewed
baseline, the audited-roots manifest, and their lockfile records — are
**trusted input**: committed, reviewed-as-code, integrity-covered. It is
**not** a reviewer for untrusted code that can modify the apparatus itself.
**Do not wire it into untrusted-PR / fork CI** — a run from an attacker's
checkout executes the attacker's scanner. A clean result is **a tripwire, not
a proof** (the runner prints this on every run). Scan genuinely untrusted
incoming content explicitly with `content_scan.py <file>` *before* an agent
ingests it.

### Exit contract

The runner's exit code is the fail-closed contract a CI step keys on:

* **`0`** — clean: a non-empty audited set scanned with no flags.
* **`1`** — tripwire findings surfaced; **advisory**. A composing orchestrator
  does **not** fail its aggregate on this alone — it is a human-review signal.
* **`2`** — the scan could not be trusted to have run: git unavailable, an
  empty / unresolvable audited set, a missing / malformed audited-roots
  manifest, a missing / sentinel-less reviewed baseline, a containment
  violation (a symlink or a path escaping the repo), or a resource-budget
  breach (a file or the set over the size budget, or the wall-clock ceiling).
  **Fails closed** — "did not actually scan" must never read as "clean".
* **`3`** — **STALE baseline authority**: a reviewed-residual entry has no live
  occurrence. A distinct fail-closed class (a stale fingerprint could
  preauthorize a replay); prune the baseline.

### Audited-roots manifest (`content_scan_roots.txt`)

The runner scans the git-tracked `.md` / `.txt` under the roots named in
`content_scan_roots.txt` (installed beside the runner in `scripts/`) — an
explicit, adopter-owned manifest, never
a shell glob or a profile-derived guess. The manifest is read fail-closed:
paths must be repo-relative (no leading `/`, no `..`), a root that resolves
outside the repo (symlink / escape) is refused, and a missing / sentinel-less
manifest or a zero-file result fails the scan. A leading **`!` marks a root
required**: a required root that is absent or contributes no tracked text
**fails the scan** (a missing required root silently shrinks coverage); an
unmarked root is optional (scanned when present). The manifest is **itself in
the audited set** — a hostile edit to it is scanned. It ships with the
core-guaranteed surface required (`!AGENTS.md`, `!.agents/skills`, `!dev`) and
`docs` + the vendor wrapper optional, plus a section for your own extensions;
**if you add agent-loaded instruction files outside those roots, add their root
here** (mark it `!` if your repo guarantees it). The runner makes no
completeness claim — it scans exactly what the manifest names.

### Reviewed-residual baseline (`content_scan_residuals.txt`)

The tripwire is deliberately noisy, so a categorical "this class is expected"
stance would hide a *new* malicious entry among standing noise. Instead each
flag is fingerprinted `(relpath, pattern_id, hash(line))` and compared as a
**multiset** against the reviewed baseline:

* A flag occurrence **beyond** its reviewed count is **NEW** — so duplicating
  an already-reviewed line surfaces the extra copy (a plain set would hide it).
  **Review every NEW finding, regardless of class.**
* A baseline entry with no live occurrence is **STALE** and **fails** the scan
  (exit 3): it must be deleted before the baseline is current.
* When a NEW flag is reviewed and judged acceptable, add a baseline line
  `<fingerprint>  # [tag] reason` — every entry carries a non-placeholder
  rationale tag (e.g. `[multi-tenant-url]`, `[sci-unit]`, `[doctrine-comment]`).

The baseline must be a present file whose first non-blank line is **exactly**
the canonical sentinel `# content-scan-residual-baseline v1` — a zero-byte,
whitespace-only, or sentinel-less file is rejected (exit 2), so accidental
truncation cannot degrade to a clean pass. The shipped template is a
deliberately-empty, sentinel-bearing baseline.

The URL allowlist (`content_scan_allowlist.txt`) is a **noise policy, not a
trust boundary**: it clears trusted-publication citation hosts only.
Multi-tenant / user-content hosts (code-forge, content-sharing) stay flagged
as residuals — the scanner matches whole domains with no path scoping, so a
blanket allow there would also bless a future malicious URL on the same host.

### Scientific-unit homoglyph allowance

The `homoglyph` detector carries a narrow, exact-token **scientific-unit
allowance** (RV5): micro / ohm unit shapes (`µs`, `µmol`, `kΩ`, …) are
structurally mixed-script in scientific prose and are cleared, while a
mixed-script *credential* token still flags. The allowance is exact-token and
tightly bounded; it does not weaken the detector for any non-unit token.

## Single-sourced with Cairn's own self-check

Cairn runs this **exact** scanner on its own tree:
`cairn/scripts/check_cairn.py` composes
`content_scan.py` from this same module file, so the methodology's own
content gate and the tool it hands an adopter are one source — no drift
between what Cairn preaches and what it ships.

## Learn it deeply

See the four-layer agent-instruction supply-chain model in
`cairn/bootstrap/SAFETY.md` (Rules 7–8) and the
public `cairn/SECURITY.md` for the threat model this
scanner is one layer of.
