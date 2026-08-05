# Proposal: classify by file class in the adopter-facing content-scan runner

**Author**: Claude (Implementation)
**Status**: proposed
**Opened**: 2026-08-05
**Review**: required(External Security Review) — this changes a detector's reach
on a security surface adopters install

## Context

`content_scan.py` is single-sourced and serves two callers (its own module
docstring says so): Cairn composes it via `scripts/check_cairn.py` over its own
prose, and the `content-security` module ships it verbatim to adopters, where
`content_scan_runner.py` drives it.

**The two callers disagree about one detector, and the shipped one is wrong.**

| caller | line | `scan_urls` |
|---|---|---|
| `scripts/check_cairn.py` | `:392` | `scan_urls = _is_template_instruction(rel)` |
| `templates/modules/team-gated/content_scan_runner.py` | `:402` | `scan_urls=True` — hardcoded, every file |

The detector's own declared scope, from `content_scan.py`'s module docstring:

> `suspicious-url` -- a non-allowlisted external `http(s)` URL, in files scanned
> with `scan_urls=True` (**executed templates**).

and the parameter's own docstring at `:384-386`:

> `scan_urls` enables the `suspicious-url` detector (use for executed templates;
> **off for discussion prose**).

So the shipped runner applies a template-scoped detector to every file in the
audited roots, which are mostly discussion prose (`dev`, `docs`).

## The measurement

Over the runner's **own** declared roots (`content_scan_roots.txt`: `AGENTS.md`,
`.agents/skills`, `dev`, `docs`, `RULES.md`, `CLAUDE.md`, `VENDOR.md`),
git-tracked `.md`/`.txt`, same allowlist, `as_of` 2026-08-05 at `6b731ad`,
Python 3.13.13:

| configuration | flags |
|---|---|
| as shipped (`scan_urls=True` everywhere) | **79**, all `suspicious-url` |
| classified (`check_cairn.py:392`'s rule) | **0** |

140 files, 7 roots. **Every flag is `suspicious-url`; no other detector fires in
either configuration.**

**What supplied the material.** The classifier is `check_cairn.py`'s existing
`_is_template_instruction`, not a predicate written for this measurement — the
change under test does not supply the rule used to evaluate it. The file set comes
from the runner's own `load_audit_roots()` and `git ls-files`, not a glob of mine.
Script retained at the harness scratch path named in the implementing commit.

## Why this is not a coverage reduction

The obvious objection is that `dev/` prose *is* agent-loaded, so silencing a
detector there loses real coverage. It does not, and the reason is that two
different detectors cover two different threats:

* **`suspicious-url`** answers *"is there an external URL here at all"*. In an
  executed template a bare URL is an instruction to fetch. In prose it is a
  citation. That is why its declared scope is templates.
* **`egress`** answers *"is there an exfiltration verb near a destination"* —
  `send`/`upload`/`post`/... near a URL or an `@` address. **It is unconditional
  and this change does not touch it.** The dangerous prose pattern ("upload the
  results to http://…") is `egress`'s, not `suspicious-url`'s.

The measurement corroborates it rather than asserting it: `egress`,
`imperative-override`, `unicode-zero-width`, `unicode-bidi`, `homoglyph` and
`instruction-html-comment` return **zero** in both configurations, so
classification changes exactly one detector's reach and leaves six untouched.

## Proposed change

1. `content_scan_runner.py` classifies per file instead of hardcoding `True`,
   using the same rule as `check_cairn.py:392`. The rule is **single-sourced**:
   the predicate moves into `content_scan.py` (which both callers already
   import) and both call sites use it. Two copies of a classification rule is
   the defect this proposal is fixing, one level up.
2. A test that pins the asymmetry: an external URL in an instruction-class file
   flags; the same URL in a prose-class file does not; and an `egress` pattern in
   a **prose-class** file still flags. That third assertion is the one that keeps
   a future "just turn URLs off everywhere" change from passing.
3. The runner's docstring states the classification and why, so the next reader
   does not re-derive it from two disagreeing call sites.

## Consequences for work in flight

`default-security-stance` Gate **D-ON-3** requires a named default-adoption
corpus, and **D-ON-2** requires a recorded disposition of the default-on
consequence. This proposal removes the consequence rather than dispositioning it:
the "alarm-fatigue budget" that plan reserves was 79 flags of misconfiguration,
and the residual after this change is **zero**. `default-security-stance`
Amendment 44 row 11 (the allowlist-vs-reviewed-residual policy for those flags)
has nothing left to decide, and `content_scan_residuals.txt` needs no entries for
them.

That is a claim about *this* tree at *this* commit. It does not promise an
adopter's tree is clean, and D-ON's conditions are unchanged by it.

## Scope fence

* **Does not** flip any default selection. `content-security` remains
  team-gated; whether it becomes default-on is `default-security-stance`'s
  question and this proposal takes no position on it.
* **Does not** touch `content_scan.py`'s detectors, the allowlist mechanism, the
  suppression-marker grammar, or the roots manifest.
* **Does not** touch `check_cairn.py`'s behaviour — it already does the right
  thing; it only stops owning a private copy of the predicate.
* The 79 flags are **not** allowlisted, suppressed, or added to
  `content_scan_residuals.txt`. They stop being flags because the detector stops
  being applied outside its declared scope.

## Verification

* `python -m pytest bootstrap/tests` green, count re-measured at the implementing
  commit rather than carried from here (it has reported four different totals in
  three days).
* `python scripts/check_cairn.py` green — it must stay green *and* its flag
  behaviour must not change, since its call site is only being re-pointed at a
  shared predicate.
* The runner over the declared roots: 0 flags, exit 0, re-run at the implementing
  commit.
* `python scripts/quality_gate.py --sub neutrality` — no new FAIL in touched
  files.
