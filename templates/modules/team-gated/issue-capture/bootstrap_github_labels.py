#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Bootstrap the project's GitHub labels from ``.github/labels.yml``.

Reads the declarative labels manifest, queries the remote repository for
existing labels via the ``gh`` CLI, and creates any that are missing.
Idempotent and safe to re-run -- existing labels with matching name +
color + description are left untouched.

Auth model
----------

This script requires a ``GITHUB_TOKEN`` environment variable with
``repo`` scope (or ``public_repo`` for public repositories).  Generate
one at ``https://github.com/settings/tokens`` or use the token that
``gh auth login`` stores -- ``gh`` picks it up automatically when the
env var is set.

If ``GITHUB_TOKEN`` is not set, the script checks whether ``gh`` has a
stored credential (``gh auth status``).  If neither is available, the
script exits with a clear "set GITHUB_TOKEN" error before making any
network call.

gh-flag drift -- verify before first run
-----------------------------------------

The script invokes ``gh repo view --json id`` and ``gh api
repos/:owner/:repo/labels --paginate``.  gh versions evolve; before
the first run on a new machine, verify both::

    gh repo view --help | grep -- '--json'      # should list --json
    gh api --help       | grep -- '--paginate'  # should list --paginate

If either flag is missing on the installed version, the script will
exit with a clear error pointing at the failing subprocess; the
maintainer can then either upgrade ``gh`` or fall back to creating
the labels manually via the GitHub web UI's Labels page.

Additive-only mode (``--additive-only``)
-----------------------------------------

Some projects carry legacy labels that pre-date this bootstrap.  Pass
``--additive-only`` to only CREATE new labels from the manifest without
touching labels that already exist but are not in the manifest.

Usage
-----

    # Inspect what would happen (no API writes; safe):
    python scripts/bootstrap_github_labels.py --dry-run

    # Apply (creates missing labels; leaves existing alone):
    python scripts/bootstrap_github_labels.py

    # Apply, including color/description updates on existing labels:
    python scripts/bootstrap_github_labels.py --force-update

    # Read a different manifest (e.g., for testing):
    python scripts/bootstrap_github_labels.py --manifest /tmp/labels.yml

    # Additive-only (never touch labels not in the manifest):
    python scripts/bootstrap_github_labels.py --additive-only

Behavior
--------

For each label in the manifest:

* Label exists with matching name, color, AND description -> no-op;
  logs "exists, unchanged."
* Label exists with matching name but DIFFERENT color or description ->
  warn-and-skip; logs "exists, manifest drift detected; use
  --force-update to apply."
* Label does not exist -> create via ``gh api --method POST
  repos/:owner/:repo/labels``; logs "created."

When ``--force-update`` is set, drift-detected labels are updated in
place via ``gh api --method PATCH repos/:owner/:repo/labels/<name>``.

Source
------

Installed by the Cairn ``issue-capture`` module.  GitHub variant of the
generic label bootstrap; no project-specific references.
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
DEFAULT_MANIFEST = REPO_ROOT / ".github" / "labels.yml"


# ---------------------------------------------------------------------------
# Auth check
# ---------------------------------------------------------------------------


def _check_auth() -> None:
    """Emit a clear error if ``gh`` has no credential.

    ``gh`` can pick up auth from its own config file OR from the
    ``GITHUB_TOKEN`` env var.  When neither is set the downstream API
    calls fail with a confusing error; we surface the missing-token
    situation explicitly before making any network call.
    """
    if os.environ.get("GITHUB_TOKEN"):
        return  # env-var credential -- proceed.
    # Try to detect a stored gh credential.
    try:
        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True, text=True, check=False,
        )
        if result.returncode == 0:
            return  # gh has a stored credential -- proceed.
    except FileNotFoundError:
        pass  # gh not installed; the later _run_gh will catch this.
    # No stored credential and no env var.
    print(
        "ERROR: gh is not authenticated.  Set the GITHUB_TOKEN "
        "environment variable to a token with `repo` scope, or run "
        "`gh auth login` to store a credential.\n"
        "  export GITHUB_TOKEN=<your-token>  # then re-run this script",
        file=sys.stderr,
    )
    sys.exit(2)


# ---------------------------------------------------------------------------
# gh subprocess helpers
# ---------------------------------------------------------------------------


def _run_gh(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess:
    """Run a ``gh`` subprocess; return CompletedProcess.

    Captures stdout / stderr so logs land in our log stream, not
    interleaved with the script's own output.
    """
    return subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        check=check,
    )


def get_repo_slug() -> str:
    """Resolve the current repo's owner/name slug via ``gh repo view``."""
    try:
        result = _run_gh(["repo", "view", "--json", "nameWithOwner",
                          "--jq", ".nameWithOwner"])
    except subprocess.CalledProcessError as exc:
        print(
            "ERROR: `gh repo view --json nameWithOwner` failed.  Two likely "
            "causes:\n"
            "  1. gh not installed or not authenticated -- verify with "
            "`gh issue list` from the repo root first.  If authentication "
            "is missing, set the GITHUB_TOKEN environment variable.\n"
            "  2. gh-flag drift -- run `gh repo view --help` to confirm "
            "`--json` is supported; older gh versions used different flags.  "
            "If unsupported, upgrade gh or create labels manually via the "
            "GitHub web UI's Labels page.\n"
            f"stderr: {exc.stderr}",
            file=sys.stderr,
        )
        sys.exit(2)
    except FileNotFoundError:
        print(
            "ERROR: `gh` CLI not found.  Install it from "
            "https://cli.github.com before running this script.",
            file=sys.stderr,
        )
        sys.exit(2)

    slug = result.stdout.strip()
    if "/" not in slug:
        print(
            "ERROR: `gh repo view` did not return an owner/name slug.  "
            f"Got: {slug!r}",
            file=sys.stderr,
        )
        sys.exit(2)

    return slug


def list_existing_labels(slug: str) -> list[dict]:
    """Fetch existing labels from the repository via the GitHub API."""
    try:
        result = _run_gh(
            ["api", f"repos/{slug}/labels", "--paginate"],
        )
    except subprocess.CalledProcessError as exc:
        print(
            "ERROR: `gh api repos/:owner/:repo/labels --paginate` failed.  "
            "Two likely causes:\n"
            "  1. Token missing `repo` scope -- regenerate your "
            "GITHUB_TOKEN with `repo` scope (or `public_repo` for public "
            "repositories).\n"
            "  2. gh-flag drift -- run `gh api --help` to confirm "
            "`--paginate` is supported.  If unsupported, upgrade gh.\n"
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


def create_label(slug: str, spec: dict, *, dry_run: bool) -> None:
    """Create a single label via the GitHub API."""
    color = spec["color"].lstrip("#")  # GitHub API wants no '#' prefix.
    if dry_run:
        print(f"  [dry-run] would create: {spec['name']!r}")
        return

    try:
        _run_gh(
            [
                "api",
                "--method", "POST",
                f"repos/{slug}/labels",
                "-f", f"name={spec['name']}",
                "-f", f"color={color}",
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


def update_label(slug: str, spec: dict, *, dry_run: bool) -> None:
    """Update an existing label's color / description via the GitHub API."""
    color = spec["color"].lstrip("#")
    name = spec["name"]
    if dry_run:
        print(
            f"  [dry-run] would update: {name!r} "
            f"(color/description drift)"
        )
        return

    try:
        _run_gh(
            [
                "api",
                "--method", "PATCH",
                f"repos/{slug}/labels/{name}",
                "-f", f"new_name={name}",
                "-f", f"color={color}",
                "-f", f"description={spec.get('description', '')}",
            ],
        )
    except subprocess.CalledProcessError as exc:
        print(
            f"ERROR: failed to update label {name!r}.\n"
            f"stderr: {exc.stderr}",
            file=sys.stderr,
        )
        sys.exit(2)
    print(f"  updated: {name!r} (color/description applied)")


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
    slug: str,
    *,
    dry_run: bool,
    force_update: bool,
) -> tuple[int, int, int]:
    """Apply the manifest to the repository; return (created, drift, unchanged)."""
    existing_by_name = {item["name"]: item for item in existing}

    n_created = 0
    n_drift = 0
    n_unchanged = 0

    for spec in manifest:
        name = spec["name"]
        match = existing_by_name.get(name)

        if match is None:
            create_label(slug, spec, dry_run=dry_run)
            n_created += 1
            continue

        # Normalize colors: GitHub API omits '#'; compare without prefix.
        spec_color = spec["color"].lstrip("#")
        match_color = (match.get("color") or "").lstrip("#")
        color_drift = match_color != spec_color
        desc_drift = (match.get("description") or "") != (
            spec.get("description") or ""
        )

        if not (color_drift or desc_drift):
            print(f"  exists, unchanged: {name!r}")
            n_unchanged += 1
            continue

        if force_update:
            update_label(slug, spec, dry_run=dry_run)
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
            "Apply the GitHub labels manifest to the repository's remote "
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
            "labels not present in the manifest.  Use this when the repository "
            "carries legacy labels that should be preserved."
        ),
    )
    args = parser.parse_args()

    if not args.dry_run:
        _check_auth()

    print(f"Reading manifest: {args.manifest}")
    manifest = load_manifest(args.manifest)
    print(f"  {len(manifest)} label(s) declared in manifest.")

    print("Resolving repository slug via `gh repo view`...")
    slug = get_repo_slug()
    print(f"  repository: {slug}")

    print("Fetching existing labels from repository...")
    existing = list_existing_labels(slug)
    print(f"  {len(existing)} label(s) currently on the repository.")

    if args.additive_only:
        print(
            "  [additive-only] existing labels not in the manifest will be "
            "left untouched."
        )

    print("Reconciling manifest with existing labels...")
    n_created, n_drift, n_unchanged = reconcile(
        manifest, existing, slug,
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
