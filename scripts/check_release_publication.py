#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Read-only check that a GitHub Release exists for a tag on the gate commit.

This checks publication state and the remote annotated-tag target. It does not
verify the tag signature, release-note links, or the bytes in GitHub's cached
source archives; those remain part of the Maintainer's release review.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

_API_ROOT = "https://api.github.com/repos"
_GITHUB_GIT_ROOT = "https://github.com"
_HTTP_TIMEOUT_SECONDS = 30
_GIT_TIMEOUT_SECONDS = 30
_MAX_RELEASE_BYTES = 1024 * 1024
_COMPONENT_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*\Z")
_OBJECT_ID_RE = re.compile(r"[0-9a-fA-F]{40}\Z")


class CheckError(Exception):
    """A fail-closed input or remote-read failure."""


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Do not let urllib forward the fixed API request to a redirect target."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _safe_detail(value: object, limit: int = 400) -> str:
    """Bound and escape control characters from a host or network diagnostic."""
    text = str(value)
    escaped = "".join(
        f"\\x{ord(char):02x}" if ord(char) < 32 or ord(char) == 127 else char
        for char in text
    )
    return escaped[:limit] or "no diagnostic"


def _validate_components(owner: str, repository: str, tag: str,
                         expected_commit: str) -> None:
    for label, value in (("owner", owner), ("repository", repository)):
        if (not _COMPONENT_RE.fullmatch(value) or value in {".", ".."}):
            raise CheckError(
                f"{label} must be one safe GitHub path component")
    if not tag or any(ord(char) < 32 or ord(char) == 127 for char in tag):
        raise CheckError("tag must be a nonempty Git tag name without controls")
    if not _OBJECT_ID_RE.fullmatch(expected_commit):
        raise CheckError("expected commit must be a full 40-hex object id")


def _resolve_git() -> Path:
    path_value = os.environ.get("PATH", "")
    found = shutil.which("git", path=path_value)
    if not found:
        raise CheckError("Git is unavailable on PATH")
    try:
        resolved = Path(found).resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise CheckError(f"Git executable could not be resolved: {_safe_detail(exc)}") from exc
    if not resolved.is_file() or not os.access(resolved, os.X_OK):
        raise CheckError("resolved Git executable is not an executable file")
    return resolved


def _git_child_env(ceiling: Path) -> dict[str, str]:
    """Construct a fresh environment for Git with no ambient config or proxy."""
    env = {"PATH": os.environ.get("PATH", "")}
    if os.name == "nt" and os.environ.get("SYSTEMROOT"):
        env["SYSTEMROOT"] = os.environ["SYSTEMROOT"]
    env.update({
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_CEILING_DIRECTORIES": str(ceiling),
    })
    return env


def _run_git(git: Path, args: list[str], *, cwd: Path,
             env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            [str(git), *args], cwd=cwd, env=env, shell=False,
            stdin=subprocess.DEVNULL, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            check=False, timeout=_GIT_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        raise CheckError(f"Git command timed out after {_GIT_TIMEOUT_SECONDS} seconds") from exc
    except (OSError, subprocess.SubprocessError) as exc:
        raise CheckError(f"Git command could not run: {_safe_detail(exc)}") from exc


def _check_tag_name(git: Path, tag: str, *, cwd: Path,
                    env: dict[str, str]) -> None:
    result = _run_git(git, ["check-ref-format", f"refs/tags/{tag}"],
                      cwd=cwd, env=env)
    if result.returncode != 0:
        raise CheckError("tag is not a valid Git tag name")


def _release_api_url(owner: str, repository: str, tag: str) -> str:
    tag_component = urllib.parse.quote(tag, safe="")
    return f"{_API_ROOT}/{owner}/{repository}/releases/tags/{tag_component}"


def _read_release_body(response, deadline: float) -> bytes:
    """Read one chunk at a time, shrinking socket timeouts to the deadline."""
    response_file = getattr(response, "fp", None)
    body_file = getattr(response_file, "fp", response_file)
    raw = getattr(body_file, "raw", None)
    sock = getattr(raw, "_sock", None)
    read_chunk = getattr(response, "read1", None)
    if sock is None or not callable(read_chunk):
        raise CheckError("GitHub Release API response cannot be read with a total deadline")

    body = bytearray()
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("GitHub Release API response exceeded its total deadline")
        sock.settimeout(remaining)
        chunk = read_chunk(min(64 * 1024, _MAX_RELEASE_BYTES + 1 - len(body)))
        if time.monotonic() > deadline:
            raise TimeoutError("GitHub Release API response exceeded its total deadline")
        if not chunk:
            return bytes(body)
        body.extend(chunk)
        if len(body) > _MAX_RELEASE_BYTES:
            raise CheckError("GitHub Release API response exceeded 1 MiB")


def _fetch_release(owner: str, repository: str, tag: str) -> None:
    """Require the fixed-host Release API to report a published matching tag."""
    url = _release_api_url(owner, repository, tag)
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "Cairn-release-publication-check",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        method="GET",
    )
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({}), _NoRedirect())
    deadline = time.monotonic() + _HTTP_TIMEOUT_SECONDS
    try:
        with opener.open(request, timeout=_HTTP_TIMEOUT_SECONDS) as response:
            status = response.getcode()
            if status != 200:
                raise CheckError(f"GitHub Release API returned HTTP {status}")
            body = _read_release_body(response, deadline)
    except urllib.error.HTTPError as exc:
        exc.close()
        raise CheckError(
            f"GitHub Release API returned HTTP {exc.code}; a published Release is required"
        ) from exc
    except urllib.error.URLError as exc:
        raise CheckError(
            f"GitHub Release API read failed: {_safe_detail(exc.reason)}") from exc
    except (OSError, TimeoutError) as exc:
        raise CheckError(
            f"GitHub Release API read failed: {_safe_detail(exc)}") from exc
    try:
        release = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CheckError("GitHub Release API returned malformed JSON") from exc
    if not isinstance(release, dict):
        raise CheckError("GitHub Release API response must be a JSON object")
    if release.get("tag_name") != tag:
        raise CheckError("published Release tag_name does not match the requested tag")
    if release.get("draft") is not False:
        raise CheckError("Release is not published (draft must be false)")
    published_at = release.get("published_at")
    if not isinstance(published_at, str) or not published_at.strip():
        raise CheckError("Release has no nonempty published_at timestamp")


def _git_config_args() -> list[str]:
    return [
        "-c", "protocol.allow=never",
        "-c", "protocol.https.allow=always",
        "-c", "http.followRedirects=false",
        "-c", "credential.helper=",
    ]


def _parse_remote_refs(stdout: str, tag: str, expected_commit: str) -> None:
    plain_ref = f"refs/tags/{tag}"
    peeled_ref = plain_ref + "^{}"
    expected_refs = {plain_ref, peeled_ref}
    found: dict[str, str] = {}
    lines = stdout.splitlines()
    if any(line.count("\t") != 1 for line in lines):
        raise CheckError("remote returned a malformed ls-remote record")
    if len(lines) != 2:
        raise CheckError(
            "remote must return exactly one annotated tag ref and one peeled ref")
    for line in lines:
        fields = line.split("\t")
        if len(fields) != 2:
            raise CheckError("remote returned a malformed ls-remote record")
        object_id, refname = fields
        if refname not in expected_refs:
            raise CheckError("remote returned an unexpected tag ref")
        if refname in found:
            raise CheckError("remote returned a duplicate tag ref")
        if not _OBJECT_ID_RE.fullmatch(object_id):
            raise CheckError("remote returned a malformed object id")
        found[refname] = object_id.lower()
    if set(found) != expected_refs:
        raise CheckError("remote annotated tag is missing its peeled ref")
    tag_object = found[plain_ref]
    peeled_commit = found[peeled_ref]
    if tag_object == peeled_commit:
        raise CheckError("remote tag is lightweight, not annotated")
    if peeled_commit != expected_commit.lower():
        raise CheckError("remote annotated tag does not peel to the expected commit")


def _query_remote_tag(git: Path, remote: str, tag: str,
                      expected_commit: str, *, cwd: Path,
                      env: dict[str, str]) -> None:
    plain_ref = f"refs/tags/{tag}"
    peeled_ref = plain_ref + "^{}"
    args = [*_git_config_args(), "ls-remote", "--exit-code", "--tags",
            remote, plain_ref, peeled_ref]
    result = _run_git(git, args, cwd=cwd, env=env)
    if result.returncode != 0:
        detail = _safe_detail(result.stderr.strip())
        raise CheckError(
            f"Git remote tag read failed (exit {result.returncode}): {detail}")
    _parse_remote_refs(result.stdout, tag, expected_commit)


def _check(owner: str, repository: str, tag: str,
           expected_commit: str) -> None:
    _validate_components(owner, repository, tag, expected_commit)
    git = _resolve_git()
    try:
        with tempfile.TemporaryDirectory(prefix="cairn-release-publication-") as raw_cwd:
            cwd = Path(raw_cwd).resolve()
            env = _git_child_env(cwd.parent)
            _check_tag_name(git, tag, cwd=cwd, env=env)
            _fetch_release(owner, repository, tag)
            remote = f"{_GITHUB_GIT_ROOT}/{owner}/{repository}.git"
            _query_remote_tag(git, remote, tag, expected_commit,
                              cwd=cwd, env=env)
    except OSError as exc:
        raise CheckError(f"temporary Git workspace failed: {_safe_detail(exc)}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=("Check that a published GitHub Release exists for an "
                     "annotated remote tag on the independently supplied gate commit."))
    parser.add_argument("--repository", required=True, metavar="OWNER/REPO",
                        help="GitHub owner and repository")
    parser.add_argument("--tag", required=True, help="published Git tag")
    parser.add_argument("--expected-commit", required=True, metavar="FULL_SHA",
                        help="full 40-hex commit id recorded by the release gate")
    args = parser.parse_args(argv)
    if args.repository.count("/") != 1:
        print("ERROR: --repository must have the form OWNER/REPO", file=sys.stderr)
        return 2
    owner, repository = args.repository.split("/", 1)
    try:
        _check(owner, repository, args.tag, args.expected_commit)
    except CheckError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(
        f"OK: published Release {tag_display(args.tag)} exists for "
        f"{owner}/{repository}; its remote annotated tag peels to "
        f"gate commit {args.expected_commit.lower()}."
    )
    return 0


def tag_display(tag: str) -> str:
    """Quote the operator-supplied tag for an unambiguous one-line report."""
    return repr(tag)


if __name__ == "__main__":
    raise SystemExit(main())
