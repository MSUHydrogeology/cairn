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

## Single-sourced with Cairn's own self-check

Cairn runs this **exact** scanner on its own tree:
[`scripts/check_cairn.py`](../../../scripts/check_cairn.py) composes
`content_scan.py` from this same module file, so the methodology's own
content gate and the tool it hands an adopter are one source — no drift
between what Cairn preaches and what it ships.

## Learn it deeply

See the four-layer agent-instruction supply-chain model in
[`bootstrap/SAFETY.md`](../../../bootstrap/SAFETY.md) (Rules 7–8) and the
public [`SECURITY.md`](../../../SECURITY.md) for the threat model this
scanner is one layer of.
