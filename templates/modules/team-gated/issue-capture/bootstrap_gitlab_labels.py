#!/usr/bin/env python3
"""Bootstrap the project's GitLab labels from ``.gitlab/labels.yml``.

Reads the declarative labels manifest, queries the remote project for
existing labels via the ``glab`` CLI, and creates any that are missing.
Idempotent and safe to re-run -- existing labels with matching name +
color + description are left untouched.

Auth model
----------

This script uses the ``glab`` CLI as a subprocess.  ``glab`` carries the
PAT in its own config (``~/.config/glab-cli/config.yml``) so the script
does not need to know about tokens directly.  Verify ``glab issue list``
works from the repo root before running this script.

Alternatively, set ``GITLAB_PRIVATE_TOKEN`` (or ``GITLAB_TOKEN``) in the
environment -- ``glab`` will use it in place of the stored credential.  If
neither a stored credential nor the env var is set, ``glab`` will fail;
this script surfaces that failure with a clear "set GITLAB_PRIVATE_TOKEN"
message.

glab-flag drift -- verify before first run
-------------------------------------------

The script invokes ``glab repo view --output json`` and ``glab api
projects/:id/labels --paginate``.  glab versions evolve; before the
first run on a new machine, verify both::

    glab repo view --help | grep -- '--output'      # should list --output json
    glab api --help       | grep -- '--paginate'    # should list --paginate

If either flag is missing on the installed version, the script will
exit with a clear error pointing at the failing subprocess; the
maintainer can then either upgrade ``glab`` or fall back to creating
the labels manually via the GitLab web UI's Labels page.

Additive-only mode (``--additive-only``)
-----------------------------------------

Some projects carry legacy labels that pre-date this bootstrap.  Pass
``--additive-only`` to suppress the delete/retire logic and only CREATE
new labels from the manifest.  Manifest-diverged existing labels are
still warn-and-skipped (or updated with ``--force-update``); labels
not in the manifest are not touched.  This is the safe default for
projects with a large pre-existing label set.

Usage
-----

    # Inspect what would happen (no API writes; safe):
    python scripts/bootstrap_gitlab_labels.py --dry-run

    # Apply (creates missing labels; leaves existing alone):
    python scripts/bootstrap_gitlab_labels.py

    # Apply, including color/description updates on existing labels:
    python scripts/bootstrap_gitlab_labels.py --force-update

    # Read a different manifest (e.g., for testing):
    python scripts/bootstrap_gitlab_labels.py --manifest /tmp/labels.yml

    # Additive-only (never touch labels not in the manifest):
    python scripts/bootstrap_gitlab_labels.py --additive-only

Behavior
--------

For each label in the manifest:

* Label exists with matching name, color, AND description -> no-op;
  logs "exists, unchanged."
* Label exists with matching name but DIFFERENT color or description ->
  warn-and-skip; logs "exists, manifest drift detected; use
  --force-update to apply."
* Label does not exist -> create via ``glab api --method POST
  projects/:id/labels``; logs "created."

When ``--force-update`` is set, drift-detected labels are updated in
place via ``glab api --method PUT projects/:id/labels/<id>``.

Source
------

Installed by the Cairn ``issue-capture`` module.  Generalizes the
per-adopter ``scripts/bootstrap_gitlab_labels.py`` scripts; no
project-specific references.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable

try:
    import yaml
except ImportError:  # pragma: no cover -- yaml is a soft dep here
    print(
        "ERROR: PyYAML is required.  Install it via `pip install pyyaml`.",
        file=sys.stderr,
    )
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = REPO_ROOT / ".gitlab" / "labels.yml"


# ---------------------------------------------------------------------------
# Auth check
# ---------------------------------------------------------------------------


def _check_auth() -> None:
    """Emit a clear error if ``glab`` has no credential.

    ``glab`` can pick up auth from its own config file OR from the
    ``GITLAB_PRIVATE_TOKEN`` / ``GITLAB_TOKEN`` env vars.  When neither
    is set the downstream API calls fail with a confusing error; we
    surface the missing-token situation explicitly before making any
    network call.
    """
    if (
        os.environ.get("GITLAB_PRIVATE_TOKEN")
        or os.environ.get("GITLAB_TOKEN")
    ):
        return  # env-var credential -- proceed.
    # Try to detect a stored glab credential by listing a trivial endpoint.
    try:
        result = subprocess.run(
            ["glab", "auth", "status"],
            capture_output=True, text=True, check=False,
        )
        if result.returncode == 0:
            return  # glab has a stored credential -- proceed.
    except FileNotFoundError:
        pass  # glab not installed; the later _run_glab will catch this.
    # No stored credential and no env var.
    print(
        "ERROR: glab is not authenticated.  Set the GITLAB_PRIVATE_TOKEN "
        "environment variable to a token with `api` scope, or run "
        "`glab auth login` to store a credential.\n"
        "  export GITLAB_PRIVATE_TOKEN=<your-token>  # then re-run this script",
        file=sys.stderr,
    )
    sys.exit(2)


# ---------------------------------------------------------------------------
# glab subprocess helpers
# ---------------------------------------------------------------------------


def _run_glab(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess:
    """Run a ``glab`` subprocess; return CompletedProcess.

    Captures stdout / stderr so logs land in our log stream, not
    interleaved with the script's own output.
    """
    return subprocess.run(
        ["glab", *args],
        capture_output=True,
        text=True,
        check=check,
    )


def get_project_id() -> int:
    """Resolve the current repo's GitLab project ID via ``glab repo view``."""
    try:
        result = _run_glab(["repo", "view", "--output", "json"])
    except subprocess.CalledProcessError as exc:
        print(
            "ERROR: `glab repo view --output json` failed.  Two likely "
            "causes:\n"
            "  1. glab not installed or not authenticated -- verify with "
            "`glab issue list` from the repo root first.  If authentication "
            "is missing, set the GITLAB_PRIVATE_TOKEN environment variable.\n"
            "  2. glab-flag drift -- run `glab repo view --help` to confirm "
            "`--output json` is supported; older glab versions used "
            "different flags.  If unsupported, upgrade glab or create labels "
            "manually via the GitLab web UI's Labels page.\n"
            f"stderr: {exc.stderr}",
            file=sys.stderr,
        )
        sys.exit(2)
    except FileNotFoundError:
        print(
            "ERROR: `glab` CLI not found.  Install it from "
            "https://gitlab.com/gitlab-org/cli before running this script.",
            file=sys.stderr,
        )
        sys.exit(2)

    try:
        info = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        print(
            f"ERROR: could not parse `glab repo view --output json` "
            f"output as JSON: {exc}.\nstdout: {result.stdout[:200]}",
            file=sys.stderr,
        )
        sys.exit(2)

    project_id = info.get("id")
    if not isinstance(project_id, int):
        print(
            "ERROR: `glab repo view` JSON did not include an integer "
            f"'id' field.  Got: {info!r}",
            file=sys.stderr,
        )
        sys.exit(2)

    return project_id


def list_existing_labels(project_id: int) -> list[dict]:
    """Fetch existing labels from the project via the GitLab API."""
    try:
        result = _run_glab(
            ["api", f"projects/{project_id}/labels", "--paginate"],
        )
    except subprocess.CalledProcessError as exc:
        print(
            "ERROR: `glab api projects/:id/labels --paginate` failed.  "
            "Two likely causes:\n"
            "  1. Token missing `api` scope -- regenerate your "
            "GITLAB_PRIVATE_TOKEN with the `api` scope, or check "
            "the stored glab credential.\n"
            "  2. glab-flag drift -- run `glab api --help` to confirm "
            "`--paginate` is supported.  If unsupported, upgrade glab or "
            "iterate manually via per-page calls.\n"
            f"stderr: {exc.stderr}",
            file=sys.stderr,
        )
        sys.exit(2)

    try:
        labels = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        print(
            f"ERROR: could not parse labels API response as JSON: {exc}.\n"
            f"stdout: {result.stdout[:200]}",
            file=sys.stderr,
        )
        sys.exit(2)

    if not isinstance(labels, list):
        print(
            f"ERROR: labels API returned non-list payload: {labels!r}",
            file=sys.stderr,
        )
        sys.exit(2)

    return labels


def create_label(project_id: int, spec: dict, *, dry_run: bool) -> None:
    """Create a single label via the GitLab API."""
    if dry_run:
        print(f"  [dry-run] would create: {spec['name']!r}")
        return

    try:
        _run_glab(
            [
                "api",
                "--method", "POST",
                f"projects/{project_id}/labels",
                "-f", f"name={spec['name']}",
                "-f", f"color={spec['color']}",
                "-f", f"description={spec.get('description', '')}",
            ],
        )
    except subprocess.CalledProcessError as exc:
        print(
            f"ERROR: failed to create label {spec['name']!r}.\n"
            f"stderr: {exc.stderr}",
            file=sys.stderr,
        )
        sys.exit(2)
    print(f"  created: {spec['name']!r}")


def update_label(
    project_id: int, existing: dict, spec: dict, *, dry_run: bool,
) -> None:
    """Update an existing label's color / description via the GitLab API."""
    label_id = existing["id"]
    if dry_run:
        print(
            f"  [dry-run] would update: {spec['name']!r} "
            f"(color/description drift)"
        )
        return

    try:
        _run_glab(
            [
                "api",
                "--method", "PUT",
                f"projects/{project_id}/labels/{label_id}",
                "-f", f"new_name={spec['name']}",
                "-f", f"color={spec['color']}",
                "-f", f"description={spec.get('description', '')}",
            ],
        )
    except subprocess.CalledProcessError as exc:
        print(
            f"ERROR: failed to update label {spec['name']!r}.\n"
            f"stderr: {exc.stderr}",
            file=sys.stderr,
        )
        sys.exit(2)
    print(f"  updated: {spec['name']!r} (color/description applied)")


# ---------------------------------------------------------------------------
# Manifest loading
# ---------------------------------------------------------------------------


def load_manifest(path: Path) -> list[dict]:
    """Load the labels manifest YAML; validate basic shape."""
    if not path.exists():
        print(f"ERROR: manifest not found: {path}", file=sys.stderr)
        sys.exit(2)

    with path.open() as f:
        data = yaml.safe_load(f)

    if not isinstance(data, list):
        print(
            f"ERROR: manifest {path} must be a YAML list of label dicts; "
            f"got {type(data).__name__}",
            file=sys.stderr,
        )
        sys.exit(2)

    for i, spec in enumerate(data):
        if not isinstance(spec, dict):
            print(
                f"ERROR: manifest entry {i} is not a dict: {spec!r}",
                file=sys.stderr,
            )
            sys.exit(2)
        if "name" not in spec or "color" not in spec:
            print(
                f"ERROR: manifest entry {i} missing required 'name' or "
                f"'color' field: {spec!r}",
                file=sys.stderr,
            )
            sys.exit(2)

    return data


# ---------------------------------------------------------------------------
# Reconciliation
# ---------------------------------------------------------------------------


def reconcile(
    manifest: list[dict],
    existing: Iterable[dict],
    project_id: int,
    *,
    dry_run: bool,
    force_update: bool,
) -> tuple[int, int, int]:
    """Apply the manifest to the project; return (created, drift, unchanged)."""
    existing_by_name = {item["name"]: item for item in existing}

    n_created = 0
    n_drift = 0
    n_unchanged = 0

    for spec in manifest:
        name = spec["name"]
        match = existing_by_name.get(name)

        if match is None:
            create_label(project_id, spec, dry_run=dry_run)
            n_created += 1
            continue

        # Label exists -- check for color / description drift.
        color_drift = match.get("color") != spec["color"]
        desc_drift = (match.get("description") or "") != (
            spec.get("description") or ""
        )

        if not (color_drift or desc_drift):
            print(f"  exists, unchanged: {name!r}")
            n_unchanged += 1
            continue

        if force_update:
            update_label(project_id, match, spec, dry_run=dry_run)
            n_drift += 1
        else:
            print(
                f"  WARN: {name!r} exists with manifest drift "
                f"(color_drift={color_drift}, desc_drift={desc_drift}); "
                f"use --force-update to apply."
            )
            n_drift += 1

    return n_created, n_drift, n_unchanged


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Apply the GitLab labels manifest to the project's remote "
            "labels.  Idempotent."
        ),
    )
    parser.add_argument(
        "--manifest", type=Path, default=DEFAULT_MANIFEST,
        help=f"Path to labels manifest YAML (default: {DEFAULT_MANIFEST}).",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print what would happen; make no API writes.",
    )
    parser.add_argument(
        "--force-update", action="store_true",
        help=(
            "Apply color/description updates to existing labels that drift "
            "from the manifest.  Without this, drift is warn-and-skip."
        ),
    )
    parser.add_argument(
        "--additive-only", action="store_true",
        help=(
            "Only create new labels from the manifest; never delete or retire "
            "labels not present in the manifest.  Use this when the project "
            "carries legacy labels that should be preserved."
        ),
    )
    args = parser.parse_args()

    if not args.dry_run:
        _check_auth()

    print(f"Reading manifest: {args.manifest}")
    manifest = load_manifest(args.manifest)
    print(f"  {len(manifest)} label(s) declared in manifest.")

    print("Resolving project ID via `glab repo view --output json`...")
    project_id = get_project_id()
    print(f"  project ID: {project_id}")

    print("Fetching existing labels from project...")
    existing = list_existing_labels(project_id)
    print(f"  {len(existing)} label(s) currently on the project.")

    if args.additive_only:
        print(
            "  [additive-only] existing labels not in the manifest will be "
            "left untouched."
        )

    print("Reconciling manifest with existing labels...")
    n_created, n_drift, n_unchanged = reconcile(
        manifest, existing, project_id,
        dry_run=args.dry_run, force_update=args.force_update,
    )

    print()
    if args.dry_run:
        print(
            f"Dry-run summary: "
            f"{n_created} would-create, {n_drift} drift, "
            f"{n_unchanged} unchanged."
        )
    else:
        verb = "updated" if args.force_update else "warn-and-skipped"
        print(
            f"Summary: {n_created} created, {n_drift} {verb}, "
            f"{n_unchanged} unchanged."
        )


if __name__ == "__main__":
    main()
