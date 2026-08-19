#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Lifecycle-metrics extractor for the proposal / plan corpus.

The Cairn ``lifecycle-metrics`` module's reference implementation.  The
scaffold installs this script into an adopting repo's ``tools/``
directory (verbatim -- no token substitution over code); the
``{{metrics_command}}`` token in the adopter's ``dev/agent_collaboration.md``
points at it.  It is vendor-neutral and **standard-library only**.

It walks ``dev/proposals/`` and ``dev/plans/`` (live and archived),
parses the in-file lifecycle headers + section grammar that the Cairn
scaffold installs, and emits a tidy CSV (or markdown) table of
per-proposal / per-plan lifecycle metrics -- review rounds, revision
counts, time-to-decision, finding severities, plus the measurement
subsystems (annotations, collision-rate, review-yield / model-tier,
output manifest) and a longitudinal snapshot layer.  It turns a team's
discipline self-claims ("External review catches structural problems",
"revision counts spike when scope is too large") from unfalsifiable
assertions into quantified, checkable rows.

**No repo-mutation surface over the corpus.**  The tool parses files,
mutates nothing in the corpus, and touches no git state except an
optional read-only ``git log`` for sub-day commit timestamps.  The
``--out`` flag writes only the derived report file; ``--snapshot`` /
``--backfill-from`` persist derived CSV snapshots under the
measurement directory (the only write surface, and an additive,
regenerable one).

**Project-agnostic by construction.**  Every project-specific value --
the model-tier vocabulary, the annotation / collision-log locations,
the snapshot directory, the rolling-window tunables -- is read from
``dev/.cairn/metrics-config.json`` (machine-readable; Cairn convention:
``dev/.cairn/`` holds config, ``dev/measurement/`` holds measurement
evidence).  When the config file is absent every value falls back to a
vendor-neutral built-in default, so the tool runs unconfigured.  The
model-tier list is an **open** ``[substring, label]`` list -- never a
closed enum -- so new vendors / models classify without a code edit.

Snapshot layer: ``--snapshot`` persists an indexed CSV
(``<snapshots_dir>/<YYYY-MM-DD>-<N>.csv``, default
``dev/measurement/snapshots/``) carrying the unified proposal+plan
schema plus ``corpus_commit`` / ``snapshot_event`` /
``snapshot_timestamp_utc`` / ``corpus_collision_count_14d`` meta-columns.
``--backfill-from`` emits one snapshot per ``Goodnight:``-tagged commit
in a bounded window.  The snapshot is always CSV regardless of
``--format``; the normal stdout / ``--out`` emission is unaffected.

Usage::

    python tools/lifecycle_metrics.py proposals             # default
    python tools/lifecycle_metrics.py plans
    python tools/lifecycle_metrics.py proposals --out m.csv
    python tools/lifecycle_metrics.py proposals --format md
    python tools/lifecycle_metrics.py proposals --root /path/to/repo
    python tools/lifecycle_metrics.py --snapshot --event goodnight
    python tools/lifecycle_metrics.py --manifest
    python tools/lifecycle_metrics.py --backfill-from 2026-05-20

Reliability tiers (the source corpus is prose-structured, not
schema-structured):

* **Exact** -- header fields, section-header counts, reviewer agent
  identity.
* **Good** -- ``total_findings`` (finding-heading bullet counts).
* **Best-effort** -- ``findings_p1/_p2/_p3`` severity (the
  bracketed-tag convention); ``external_tier_review`` (role-
  label parse, ``unknown`` bucket for label-less headers);
  ``paired_proposal`` slug-match fallback; the annotation /
  collision-log / disposition parsers (forgiving by design).

Robust across VCS settings: when git is absent, the path is not a
checkout, the default branch is named ``main`` rather than ``master``,
or **no commit subject in a file's history matches the stage
vocabulary**, the optional commit-timestamp augmentation degrades
quietly (empty hour-delta columns + a ``Best-effort`` reliability tier)
rather than raising.  That last cause is the common one in a project
whose commit subjects do not carry the lifecycle-stage wording the
reader looks for, and it is indistinguishable in the output from having
no git at all.

What the ``hours_*`` columns measure is the interval between the
**commits that recorded** each transition -- not how long the
deliberation itself took.  A session that reviews, responds and decides
in one sitting and commits the results together reports deltas at or
near ``0.0``, which is an honest reading of the commit record.  Test an
hour delta against ``''`` rather than for truthiness: ``0.0`` is a
populated value, not a missing one.

``hours_*`` and ``days_*`` can therefore disagree, legitimately.  The
day counts come from the dates written in the document's own section
headers; the hour deltas come from the commit timestamps.  A proposal
whose ``**Date opened**`` predates the commit that opened it reports a
larger day count than the hour delta spans.  Neither column is wrong --
they read two different clocks.
"""
from __future__ import annotations

import importlib as _importlib

# Leaf-first load order (acyclic): config/parse/report have no sibling deps;
# subsystems -> parse,config; extract -> config,parse,gitmeta,subsystems;
# snapshot -> config,extract,subsystems,gitmeta,report; cli -> the rest.
# Loaded via ``import_module`` (not ``from . import ...``) so resolution needs
# only THIS package in ``sys.modules`` -- no top-level ``tools`` parent, keeping
# the launcher's fail-closed containment surface minimal.
_SUBMODULES = (
    "config", "parse", "gitmeta", "report",
    "subsystems", "extract", "snapshot", "cli",
)

for _name in _SUBMODULES:
    _m = _importlib.import_module("." + _name, __name__)
    globals().update({k: v for k, v in vars(_m).items() if not k.startswith("__")})

if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())  # noqa: F821
