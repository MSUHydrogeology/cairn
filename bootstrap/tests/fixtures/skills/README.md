# Skills compatibility fixture harness

This directory anchors the **per-release fixture harness** for the lifecycle
skills (plan `2026-06-01-claude-cairn-vendor-neutral-skills`, Chunk 7). The
compatibility matrix (`docs/skills-compatibility.md`) is **generated** from the
vendor-targets table (`templates/skills/_data/vendor_targets.yml`) by
`bootstrap.scaffold.render_compatibility_matrix`, and `test_skills_matrix.py`
fails the build if the committed matrix drifts from the generator output.

## What "fixture-backed" means, honestly (II3 / II4b)

A target's **level** is `claimed-pending-fixture` until a fixture actually
exercises install + invoke on that harness and promotes it to `native-tested`.
**Cairn has no CI**, and no automated trigger of any kind can drive a
proprietary external harness (Claude Code, Cursor, ...), so: <!-- vendor-ok: fixture README names the harnesses its levels describe -->

* The **mechanism** tiers are **suite-proven** here and in
  `test_skills_fanout.py` / `test_skills_install.py`: alias (canonical
  read-path), symlink + copy-fallback fan-out, install + lockfile provenance.
  "Suite-proven" names an exact trigger — these are test nodes inside `python
  -m pytest bootstrap/tests`, which a person or an agent types, and which the
  release run (`python bootstrap/security_check.py`, phase 3) also executes.
* A **per-target native invocation** fixture (does this harness actually load
  and run the skill?) is a maintainer / release-time step. As each lands, flip
  that target's `level` in the table to `native-tested` and drop a fixture
  transcript beside this README; the matrix regenerates and the drift gate
  re-pins it.

## v1 cut (II4b)

* **Claude Code** ships first as the intended `native-tested` target (it <!-- vendor-ok: fixture README names the harness whose level it tracks -->
  **declares** `disable-model-invocation`, so its auto-suppress is
  `declared-flag` until a fixture/transcript proves the harness actually
  suppresses model-invocation -- only then does it become `native-tested`);
  it reads the symlinked `.claude/skills/` -> canonical.
* Other SKILL.md-native targets ship `native-claimed-unverified` until their
  fixture lands.
* Different-format targets (e.g. Cursor `.mdc`) ship `manual-fallback` with a <!-- vendor-ok: fixture README names an example of a different-format harness -->
  `mitigated` auto-suppress (anti-semantic description only), pending an
  automated compile path proven out by a fixture.

Per-target effort to promote: write a minimal repo fixture that installs the
skill into the target's read-path and asserts the harness loads it; wire it as a
`native-tested` row. Roughly an afternoon per harness, dominated by standing up
the harness at all.

**Where the suite cannot run the harness, the evidence is a recorded
native-harness transcript** — the session output showing that harness loading
and running the skill — **committed beside this README and read by a human.**
That is the whole trigger: a person runs the harness, saves the transcript,
reviews it, and flips the `level`. There is no automated substitute and this
file does not pretend otherwise; a `native-tested` row with no transcript
beside it is an unbacked claim.
