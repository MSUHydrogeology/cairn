from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

#: Default repo root when ``--root`` is not given.  For the installed
#: script at ``<target>/tools/_lifecycle_metrics/config.py`` this is
#: ``<target>`` (two parents up: _lifecycle_metrics/ -> tools/ -> repo root).
#: ``--root`` overrides it for any layout.
_REPO_ROOT = Path(__file__).resolve().parents[2]  # moved one dir deeper than tools/


def proposals_dir(root: Path) -> Path:
    """The proposals corpus root under *root*."""
    return root / 'dev' / 'proposals'


def plans_dir(root: Path) -> Path:
    """The plans corpus root under *root*."""
    return root / 'dev' / 'plans'


# ------------------------------------------------------------- configuration

#: Built-in, vendor-neutral default model-tier vocabulary.  An **open**
#: ordered ``[substring, label]`` list (first case-insensitive substring
#: match wins); ``unknown`` self-disclosure maps to ``tier-unknown``.
#: A project overrides this wholesale via the ``model_tiers`` key of
#: ``dev/.cairn/metrics-config.json`` -- the list stays open so a new
#: vendor / model is a config edit, never a code edit.  Shipped defaults
#: cover the agent families the reference corpus exercises; they carry
#: no project-specific roster (the human/AI split a closed roster would
#: encode is deliberately absent -- see ``_agent_of``).
_DEFAULT_MODEL_TIERS: List[Tuple[str, str]] = [
    ('opus', 'Opus'),
    ('sonnet', 'Sonnet'),
    ('haiku', 'Haiku'),
    ('gpt-5', 'GPT-5'),
    ('gpt-4', 'GPT-4'),
    ('codex', 'Codex'),
    ('unknown', 'tier-unknown'),
]

#: Default config values (all overridable via
#: ``dev/.cairn/metrics-config.json``).  Path values are repo-root-
#: relative POSIX strings, resolved against ``--root`` at load time.
_DEFAULT_CONFIG: Dict[str, object] = {
    'annotations_dir': 'dev/metrics_annotations',
    'collision_log': 'dev/collision_log.md',
    'collision_window_days': 14,
    'collision_counted_kind': 'true-staged-index',
    'snapshots_dir': 'dev/measurement/snapshots',
    'backfill_max_days': 14,
    'model_tiers': _DEFAULT_MODEL_TIERS,
}

#: Config file location, relative to the repo root.  Cairn convention:
#: ``dev/.cairn/`` holds machine-edited config; ``dev/measurement/``
#: holds the measurement evidence the tool produces.
_CONFIG_RELPATH = ('dev', '.cairn', 'metrics-config.json')


def _safe_int(value: object, default: int) -> int:
    """Coerce a config scalar to ``int``, falling back to *default* on a
    wrong type or unparseable value -- the load path must never raise on a
    malformed config."""
    try:
        return int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return default


def _safe_rel(root: Path, value: object, default: str) -> Path:
    """Resolve a config-supplied, repo-root-relative path under *root*,
    falling back to the built-in *default* when the value would escape the
    repo (an absolute path or a ``..`` traversal).  Containment keeps the
    tool's only write surface -- the snapshots dir -- and, for consistency,
    its read paths inside the repo even under a hostile or careless
    ``metrics-config.json``, preserving the module's "writes stay under
    ``dev/measurement/``" invariant.  Never raises (the forgiving load
    contract); an in-bounds value returns the exact ``root / value`` join
    unchanged, so the default (no-config) behaviour is byte-identical."""
    candidate = root / Path(str(value))
    try:
        root_res = root.resolve()
        cand_res = candidate.resolve()
    except OSError:
        return root / Path(default)
    if cand_res == root_res or root_res in cand_res.parents:
        return candidate
    return root / Path(default)


class MetricsConfig:
    """Resolved, project-agnostic configuration for one repo root.

    Built by :func:`load_config`.  Path attributes are absolute (resolved
    against the repo root); scalar tunables and the open model-tier list
    are plain values.  Constructed with defaults when no config file is
    present, so every consumer can assume a fully-populated object.
    """

    def __init__(
        self,
        *,
        root: Path,
        annotations_dir: Path,
        collision_log: Path,
        collision_window_days: int,
        collision_counted_kind: str,
        snapshots_dir: Path,
        backfill_max_days: int,
        model_tiers: List[Tuple[str, str]],
    ) -> None:
        self.root = root
        self.annotations_dir = annotations_dir
        self.collision_log = collision_log
        self.collision_window_days = collision_window_days
        self.collision_counted_kind = collision_counted_kind
        self.snapshots_dir = snapshots_dir
        self.backfill_max_days = backfill_max_days
        self.model_tiers = model_tiers


def load_config(root: Path) -> MetricsConfig:
    """Load + resolve ``dev/.cairn/metrics-config.json`` under *root*.

    Forgiving by design (the metrics path is read-only and must never
    raise on a missing / malformed config): a missing file, unreadable
    file, or non-JSON content falls back to the built-in defaults; a
    present-but-partial config overrides only the keys it sets.  The
    ``model_tiers`` list -- the one field a project is expected to set
    explicitly, since tier vocabulary is inherently vendor-specific --
    falls back to :data:`_DEFAULT_MODEL_TIERS` when absent or malformed.

    Wrong-typed scalar values fall back to their defaults rather than
    raising (e.g. a non-numeric ``collision_window_days``), and
    config-supplied paths that would escape the repo root (absolute or
    ``..``-traversing) fall back to the built-in repo-relative default, so
    the tool's write surface stays contained -- see :func:`_safe_int` and
    :func:`_safe_rel`.
    """
    data = dict(_DEFAULT_CONFIG)
    cfg_path = root.joinpath(*_CONFIG_RELPATH)
    try:
        raw = json.loads(cfg_path.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        raw = None
    if isinstance(raw, dict):
        for key in _DEFAULT_CONFIG:
            if raw.get(key) is not None:
                data[key] = raw[key]

    tiers: List[Tuple[str, str]] = []
    raw_tiers = data.get('model_tiers') or ()
    if isinstance(raw_tiers, (list, tuple)):
        for item in raw_tiers:
            if isinstance(item, (list, tuple)) and len(item) == 2:
                tiers.append((str(item[0]), str(item[1])))
    if not tiers:
        tiers = [(s, l) for s, l in _DEFAULT_MODEL_TIERS]

    return MetricsConfig(
        root=root,
        annotations_dir=_safe_rel(
            root, data['annotations_dir'], str(_DEFAULT_CONFIG['annotations_dir'])),
        collision_log=_safe_rel(
            root, data['collision_log'], str(_DEFAULT_CONFIG['collision_log'])),
        collision_window_days=_safe_int(
            data['collision_window_days'], int(_DEFAULT_CONFIG['collision_window_days'])),
        collision_counted_kind=str(data['collision_counted_kind']),
        snapshots_dir=_safe_rel(
            root, data['snapshots_dir'], str(_DEFAULT_CONFIG['snapshots_dir'])),
        backfill_max_days=_safe_int(
            data['backfill_max_days'], int(_DEFAULT_CONFIG['backfill_max_days'])),
        model_tiers=tiers,
    )
