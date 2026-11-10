# Prose templates off the high-risk list; scan all shipped template prose before release

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — it edits the high-risk list itself and `bootstrap/SAFETY.md` Rule 7.
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-10
**In brief**: Editing the prose files Cairn ships to adopters would stop counting as high-risk work, and in return every one of those files gets a security read before each release.

## Decision summary

Today any shipped-template edit is high-risk work. The Maintainer's direction, chat, 2026-11-10:

> "Changing prose templates should not be high risk during the implementation phase. I want to remove that restriction. But a pre-release security scan of all of them is a really good idea."

> "Pinning template bytes seems like a bad idea. They should be pinned on release for some verification or another. But we don't need a bunch of obstacles in the way of updating prose."

> "The content scanner should include all shipped template prose. It should not scan CLAUDE.md as that is not a Cairn product."

Outcomes: (A) prose templates leave the high-risk list; (B) one pre-release scan of every shipped template's prose; (C) bytes pinned at release only; (D) Cairn's own scan list gains `templates` and drops `CLAUDE.md`. **Intended release: v0.8.** Price: template edits lose their own Security Review; the release read replaces it.

A *high-risk surface* is a file class whose change needs a proposal and Security Review. A *pin* is a test or hash that fails when wording or bytes change. The *content scanner* is a *tripwire*: it flags text that looks like a hidden instruction; silence proves nothing.

## Context

Measured 2026-11-10 at commit 1d21845d:

- `templates/` has 116 tracked files: 64 `.md`, 4 `.txt`, 37 `.py`, 11 other. The 68 prose files total 68,234 words.
- Pins: none of the 150 hashed files in `bootstrap/tests/fixtures/gate_manifest.json` is a `.md` template; its 28 template entries are `.py`. Wording pins are tests: 50 of 125 top-level test files mention `templates/`; I did not count those asserting exact text.
- `scripts/content_scan_runner.py` read 123 files over the 7 roots in `scripts/content_scan_roots.txt`: clean. In a throwaway copy with `templates` added and `CLAUDE.md` dropped: 190 files (123 − 1 + 68), 0 flags.
- `python scripts/check_cairn.py`, already in `docs/release-process.md` (line 138), scans every tracked Markdown file, templates included: 204 files, no issues, 2.5 seconds. It skips the 4 `.txt` templates.
- The secrets scanner cannot yet report "clean" (empty approved-build list, `scripts/run_portable_security_sweeps.py`, line 242); not used here.

Not established: whether the 8 `.json`/`.yml` templates hide anything; nothing scans them.

## Proposal

Intended release: v0.8.

**A.** In `AGENTS.md` (near line 434) drop "and templates" from the high-risk list. Still protected: the scaffold engine, protected tests, install, fidelity and gate manifests, lockfile schema, interpreter binding, portable sweeps, and every `.py` under `templates/`. Structure the installer reads (`cairn:slot` markers, `{{token}}` placeholders) is not prose; editing it stays protected. `docs/methodology/` is unchanged. Edit `SAFETY.md` Rule 7 (per-change injection review becomes release review) and the line naming "the authoring templates themselves" in both `_template.md` copies.

**B.** Before each cut, sweep B runs on the release-candidate commit: `check_cairn.py`; `content_scan_runner.py` with `templates` as a root; and a recorded agent read of each prose file in `git ls-files templates` (68 now). The read is the safeguard; `SAFETY.md` already calls the scanner a witness, not a proof. New code: none.

**C.** No new byte or phrase pin on prose templates in development. At release the pin is the scanned commit id and file count, recorded with the release evidence; a later edit means a re-scan. The `.py` hashes stay.

**D.** Cairn's `scripts/content_scan_roots.txt` adds `templates` and drops `CLAUDE.md`. The starter adopters receive (`templates/modules/team-gated/content_scan_roots.txt`) is unchanged, `CLAUDE.md` optional. Consequences: the security-verification dispatcher checks Cairn's copy against its lockfile hash (`run_security_verification.py`, line 576), so the record must be refreshed in the same change (read, not run); and `CLAUDE.md` would leave the functional-prose list built from this file, losing its exact-replacement rule (read, not tested).

## Rationale

The risk `SAFETY.md` Rule 7 names, a hidden instruction reaching every adopter, bites when files ship; one full read per release covers it more cheaply than a review per edit.

## Alternatives considered

1. **Do nothing.** Loses no assurance; keeps the friction.
2. **Least involved: leave `AGENTS.md` alone; exempt prose-only template edits case by case.** Loses relief (each exemption is a fresh argument) and any guaranteed full read. Keeps per-edit assurance.
3. **Scan only (B, D).** Keeps heavy review per edit; no relief.
4. **A to D.** Gives up per-edit Security Review; a planted instruction waits for the release read.

**Recommendation: option 4**: the Maintainer asked for it and the release read covers the named risk. Assumed: the read costs about 90,000 tokens per release (68,234 words at ~1.3 tokens each).

**Human operations added** (estimates): option 1: 0; option 2: 0, plus about one exemption disposition per template-editing plan; option 3: 0; option 4: 0 recurring (sweep B is already assigned each cut), 1 one-time (the Decision). Recurring addition (option 4): one recorded read per release.

## Documentation / doctrine surface

`AGENTS.md`; `bootstrap/SAFETY.md` Rule 7; `docs/release-process.md` sweep B; both `_template.md` copies; `scripts/content_scan_roots.txt` and its lockfile record. I did not search for tests pinning nearby text.

## Evidence / verification plan

Real entry points: `python scripts/content_scan_runner.py` reads `templates`, not `CLAUDE.md` (190 files today); `test_security_stack.py::TestAuditRootsManifest` passes (starter unchanged); tests naming the roots file in `test_security_verification.py` pass after the refresh. Positive control: plant a hidden instruction in a copy of one template; both scanners must flag it. Security preflight: no input, parser or execution path is added. Scientific check: N/A.

## Signals the change is wrong

- A release read finds a hidden instruction that per-edit review would have caught earlier.
- A "prose" edit breaks install or upgrade (structure edited as prose).
- The planted instruction goes unflagged, or the read is skipped twice.

## Scope delta

N/A.

## Assurance path

**Assurance path**: high-assurance — touches the security reference.
