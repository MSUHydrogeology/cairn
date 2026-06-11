#!/usr/bin/env python3
"""Phase 1 tests — trusted baseline materialization (plan
``2026-06-10-claude-cairn-differential-oracle-gitref-baseline``).

Covers the security-load-bearing gates: out-of-band trust (ancestry-not-name,
the two-commit malicious-ancestor refusal, object-absent vs unprovable), and the
two-pass bounded extraction (empty-on-refusal, the unsafe-member classes, and the
fixed v1 resource budgets).
"""
from __future__ import annotations

import io
import subprocess
import tarfile

import pytest

from bootstrap.tests import _oracle_trust as T


# --------------------------------------------------------------------------- git
def _git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, check=True)


def _repo(path):
    path.mkdir(parents=True, exist_ok=True)
    _git(path, "init", "-q", "-b", "master")
    _git(path, "config", "user.email", "t@t")
    _git(path, "config", "user.name", "t")
    return path


def _commit(repo, msg, content):
    (repo / "f.txt").write_text(content)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", msg)
    return _git(repo, "rev-parse", "HEAD").stdout.strip()


# ------------------------------------------------------------------- trust gates
def test_trust_accepts_ancestor_of_trusted_ref(tmp_path):
    r = _repo(tmp_path / "r")
    a = _commit(r, "a", "1")
    _commit(r, "b", "2")          # master now at b; a is an ancestor
    assert T.verify_baseline_trust(a, "master", r) == a


def test_trust_refuses_two_commit_malicious_ancestor(tmp_path):
    """The attack v3 closed: a malicious commit reachable from the evaluated
    branch but NOT from the trusted ref must be refused."""
    r = _repo(tmp_path / "r")
    base = _commit(r, "base", "1")
    # trusted line advances on master
    _git(r, "checkout", "-q", "master")
    _commit(r, "trusted", "2")
    # attacker lands a malicious commit on a side (evaluated) branch off base
    _git(r, "checkout", "-q", "-b", "evil", base)
    evil = _commit(r, "malicious", "owned")
    # evil is reachable from the evaluated branch but not from master (trusted)
    with pytest.raises(T.TrustError, match="NOT reachable"):
        T.verify_baseline_trust(evil, "master", r)


def test_trust_refuses_absent_object_fail_closed(tmp_path):
    r = _repo(tmp_path / "r")
    _commit(r, "a", "1")
    bogus = "0" * 40
    with pytest.raises(T.TrustError):
        T.verify_baseline_trust(bogus, "master", r)


def test_trust_unresolvable_ref_refused(tmp_path):
    r = _repo(tmp_path / "r")
    _commit(r, "a", "1")
    with pytest.raises(T.TrustError):
        T.verify_baseline_trust("no-such-ref", "master", r)


# -------------------------------------------------------------- extraction gates
def _tar(members):
    """members: list of (TarInfo, bytes|None)."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as t:
        for ti, data in members:
            t.addfile(ti, io.BytesIO(data) if data is not None else None)
    return buf.getvalue()


def _file(name, data=b"x"):
    ti = tarfile.TarInfo(name)
    ti.size = len(data)
    ti.type = tarfile.REGTYPE
    return ti, data


def _dir(name):
    ti = tarfile.TarInfo(name)
    ti.type = tarfile.DIRTYPE
    return ti, None


def _empty(d):
    return not any(d.rglob("*")) if d.exists() else True


def test_extract_valid_tree(tmp_path):
    raw = _tar([_dir("pkg"), _file("pkg/a.py", b"print(1)\n"), _file("b.txt", b"hi")])
    dest = tmp_path / "out"
    T._validate_and_extract(raw, dest)
    assert (dest / "pkg" / "a.py").read_bytes() == b"print(1)\n"
    assert (dest / "b.txt").read_bytes() == b"hi"


@pytest.mark.parametrize("name", ["/etc/passwd", "../escape", "a/../../x", "C:/win"])
def test_extract_refuses_unsafe_paths_empty(tmp_path, name):
    raw = _tar([_file("ok.txt"), _file(name)])
    dest = tmp_path / "out"
    with pytest.raises(T.ExtractionError):
        T._validate_and_extract(raw, dest)
    assert _empty(dest)            # two-pass: destination empty on refusal


def test_extract_refuses_symlink_empty(tmp_path):
    sym = tarfile.TarInfo("link")
    sym.type = tarfile.SYMTYPE
    sym.linkname = "/etc/passwd"
    raw = _tar([_file("ok.txt"), (sym, None)])
    with pytest.raises(T.ExtractionError, match="link member"):
        T._validate_and_extract(raw, tmp_path / "out")
    assert _empty(tmp_path / "out")


def test_extract_refuses_hardlink_and_special(tmp_path):
    for typ, attr in [(tarfile.LNKTYPE, "linkname"), (tarfile.CHRTYPE, None),
                      (tarfile.FIFOTYPE, None), (tarfile.BLKTYPE, None)]:
        ti = tarfile.TarInfo("weird")
        ti.type = typ
        if attr:
            setattr(ti, attr, "ok.txt")
        with pytest.raises(T.ExtractionError):
            T._validate_and_extract(_tar([_file("ok.txt"), (ti, None)]), tmp_path / "o")


def test_extract_refuses_duplicate(tmp_path):
    raw = _tar([_file("dup.txt", b"a"), _file("dup.txt", b"b")])
    with pytest.raises(T.ExtractionError, match="duplicate"):
        T._validate_and_extract(raw, tmp_path / "out")
    assert _empty(tmp_path / "out")


def test_extract_refuses_file_dir_collision(tmp_path):
    raw = _tar([_file("a"), _file("a/b")])    # 'a' as file and as dir-prefix
    with pytest.raises(T.ExtractionError, match="collision"):
        T._validate_and_extract(raw, tmp_path / "out")
    assert _empty(tmp_path / "out")


def test_extract_refuses_member_count_budget(tmp_path, monkeypatch):
    monkeypatch.setattr(T, "MEMBER_MAX", 3)
    raw = _tar([_file(f"f{i}.txt") for i in range(5)])
    with pytest.raises(T.ExtractionError, match="member count"):
        T._validate_and_extract(raw, tmp_path / "out")
    assert _empty(tmp_path / "out")


def test_extract_refuses_per_file_budget(tmp_path, monkeypatch):
    monkeypatch.setattr(T, "PER_FILE_MAX", 4)
    raw = _tar([_file("big.txt", b"toolong")])
    with pytest.raises(T.ExtractionError, match="per-file"):
        T._validate_and_extract(raw, tmp_path / "out")
    assert _empty(tmp_path / "out")


def test_extract_refuses_total_budget(tmp_path, monkeypatch):
    monkeypatch.setattr(T, "TOTAL_EXPANDED_MAX", 5)
    raw = _tar([_file("a.txt", b"123"), _file("b.txt", b"456")])
    with pytest.raises(T.ExtractionError, match="total expanded"):
        T._validate_and_extract(raw, tmp_path / "out")
    assert _empty(tmp_path / "out")


def test_extract_refuses_raw_stream_budget_before_parse(tmp_path, monkeypatch):
    monkeypatch.setattr(T, "RAW_ARCHIVE_MAX", 8)
    raw = _tar([_file("a.txt", b"hello world")])
    with pytest.raises(T.ExtractionError, match="raw archive"):
        T._validate_and_extract(raw, tmp_path / "out")
    assert _empty(tmp_path / "out")


def test_extract_late_unsafe_member_leaves_empty(tmp_path):
    """A safe member FOLLOWED by an unsafe one — two-pass means nothing is
    written (the partial-write gap the review flagged)."""
    raw = _tar([_file("safe1.txt", b"a"), _file("safe2.txt", b"b"), _file("../evil")])
    with pytest.raises(T.ExtractionError):
        T._validate_and_extract(raw, tmp_path / "out")
    assert _empty(tmp_path / "out")


# ---- end-to-end against a real git ref (archive path) ----------------------
def test_extract_ref_tree_roundtrip(tmp_path):
    r = _repo(tmp_path / "r")
    (r / "pkg").mkdir()
    (r / "pkg" / "m.py").write_text("X = 1\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-q", "-m", "c")
    sha = _git(r, "rev-parse", "HEAD").stdout.strip()
    dest = tmp_path / "ex"
    T.extract_ref_tree(sha, dest, r)
    assert (dest / "pkg" / "m.py").read_text() == "X = 1\n"
