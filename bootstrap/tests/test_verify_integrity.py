"""Tests for the lockfile-backed install-integrity check (security-hardening
Chunk 12).

``bootstrap/verify_integrity.py`` recomputes each lockfile-recorded file's
SHA-256 against the on-disk tree and **fails closed** on any mismatch /
missing file / absent lockfile -- detecting a post-install modification of a
shipped file without trusting the file to vouch for itself.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap import verify_integrity  # noqa: E402
from bootstrap.scaffold import main, read_lockfile  # noqa: E402

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)


def _install(target: Path) -> int:
    cfg = target / "profile.yml"
    cfg.write_text("project_name: VI\ntest_command: pytest\nmodules: []\n")
    return main(["--config", str(cfg), "--target", str(target),
                 "--cairn-root", str(CAIRN_ROOT), "--allow-dev"])


def test_clean_install_verifies(tmp_path: Path) -> None:
    assert _install(tmp_path) == 0
    assert (tmp_path / "dev" / ".cairn" / "cairn-lock.yml").is_file()
    assert verify_integrity.verify(tmp_path) == 0


def test_tampered_file_fails_closed(tmp_path: Path) -> None:
    assert _install(tmp_path) == 0
    lock = read_lockfile(tmp_path)
    target_file = tmp_path / lock["files"][0]["dst"]
    target_file.write_text(
        target_file.read_text(encoding="utf-8") + "\n<!-- tampered -->\n",
        encoding="utf-8")
    assert verify_integrity.verify(tmp_path) == 1


def _fill_slot(path: Path, slot: str, marker: str, text: str) -> None:
    """Write *marker* and *text* into the body of slot *slot* in *path*."""
    content = path.read_text(encoding="utf-8")
    end = f"<!-- cairn:end {slot} -->"
    assert end in content, f"{path.name} has no {slot} slot"
    path.write_text(content.replace(end, f"{marker}\n{text}\n{end}"),
                    encoding="utf-8")


def test_a_filled_customized_slot_is_pointed_at_finalize(
    tmp_path: Path, capsys
) -> None:
    """Filling a slot and marking it customized is an expected edit, so the
    failure names the command that records it -- and following that advice
    clears the check.  The marker counts only inside a slot body, and in any
    spacing the merge engine accepts: a file that merely quotes the marker in
    prose, outside a slot, gets no hint, because suggesting --finalize there
    would invite blessing a change nobody can explain."""
    assert _install(tmp_path) == 0
    _fill_slot(tmp_path / "AGENTS.md", "project-conventions",
               "<!--cairn:customized-->", "Our own conventions.")
    vendor = tmp_path / "VENDOR.md"
    vendor.write_text(vendor.read_text(encoding="utf-8")
                      + "\nThe `<!-- cairn:customized -->` marker, quoted.\n",
                      encoding="utf-8")
    capsys.readouterr()
    assert verify_integrity.verify(tmp_path) == 1
    err = capsys.readouterr().err
    assert "--finalize AGENTS.md" in err
    assert "VENDOR.md" not in err.split("--finalize", 1)[1]
    # --finalize records the whole file, and the marker says nothing about
    # text outside the slot, so the hint must ask for that check first --
    # and say this tool cannot do it, since it keeps only a hash.
    assert "nothing outside its slots changed" in err
    assert "keeps only a hash" in err
    # History alone misses uncommitted edits, so it is not offered as enough.
    assert "history misses uncommitted edits" in err

    assert main(["upgrade", "--target", str(tmp_path), "--cairn-root",
                 str(CAIRN_ROOT), "--finalize", "AGENTS.md"]) == 0
    vendor.write_text(vendor.read_text(encoding="utf-8").replace(
        "\nThe `<!-- cairn:customized -->` marker, quoted.\n", ""),
        encoding="utf-8")
    assert verify_integrity.verify(tmp_path) == 0


class TestCustomizedSlotDetection:
    """Which files earn the --finalize hint: a marker inside a slot body,
    never one quoted outside a slot or left in a slot that has closed."""

    def test_a_marker_inside_a_slot_counts(self) -> None:
        text = ("<!-- cairn:slot a -->\n<!--CAIRN:customized-->\nours\n"
                "<!-- cairn:end a -->\n")
        assert verify_integrity._has_customized_slot(text)

    def test_a_marker_outside_every_slot_does_not(self) -> None:
        text = ("The `<!-- cairn:customized -->` marker, quoted.\n"
                "<!-- cairn:slot a -->\n\n<!-- cairn:end a -->\n")
        assert not verify_integrity._has_customized_slot(text)

    def test_a_marker_after_its_slot_closed_does_not(self) -> None:
        text = ("<!-- cairn:slot a -->\n<!-- cairn:end a -->\n"
                "<!-- cairn:customized -->\n")
        assert not verify_integrity._has_customized_slot(text)

    def test_a_stray_end_does_not_reopen_a_closed_slot(self) -> None:
        text = ("<!-- cairn:slot a -->\n<!-- cairn:end a -->\n"
                "<!-- cairn:customized -->\n<!-- cairn:end a -->\n")
        assert not verify_integrity._has_customized_slot(text)

    def test_unclosed_slots_cost_linear_time(self) -> None:
        """A modified file is attacker-shaped input. Scanning to the end of
        the file once per unclosed opener made 88 KB take seconds, so a
        crafted file could stall the trust check."""
        import time
        text = "<!-- cairn:slot a -->\n" * 20000      # about 440 KB
        start = time.perf_counter()
        assert not verify_integrity._has_customized_slot(text)
        assert time.perf_counter() - start < 2.0


def test_missing_file_fails_closed(tmp_path: Path) -> None:
    assert _install(tmp_path) == 0
    lock = read_lockfile(tmp_path)
    (tmp_path / lock["files"][0]["dst"]).unlink()
    assert verify_integrity.verify(tmp_path) == 1


def test_absent_lockfile_fails_closed(tmp_path: Path) -> None:
    # A target with no lockfile cannot attest integrity -> fail closed.
    assert verify_integrity.verify(tmp_path) == 1


def _write_lock(target: Path, files: list) -> None:
    (target / "dev").mkdir(parents=True, exist_ok=True)
    (target / "dev" / ".cairn").mkdir(parents=True, exist_ok=True)
    (target / "dev" / ".cairn" / "cairn-lock.yml").write_text(
        json.dumps({"files": files}), encoding="utf-8")


def test_escaping_dst_fails_closed(tmp_path: Path) -> None:
    """A lockfile record whose dst escapes the target (`../outside`) must
    FAIL CLOSED -- never read or attest an out-of-tree file even if its hash
    matches. The lockfile is itself a tamper target."""
    outside = tmp_path / "outside.txt"
    outside.write_text("secret", encoding="utf-8")
    target = tmp_path / "repo"
    good_hash = "sha256:" + hashlib.sha256(outside.read_bytes()).hexdigest()
    _write_lock(target, [{"dst": "../outside.txt", "hash": good_hash}])
    assert verify_integrity.verify(target) == 1


def test_absolute_dst_fails_closed(tmp_path: Path) -> None:
    target = tmp_path / "repo"
    _write_lock(target, [{"dst": "/etc/hostname", "hash": "sha256:" + "0" * 64}])
    assert verify_integrity.verify(target) == 1


def test_malformed_records_fail_closed(tmp_path: Path) -> None:
    target = tmp_path / "repo"
    _write_lock(target, [{"hash": "sha256:" + "0" * 64}])          # no dst
    assert verify_integrity.verify(target) == 1
    _write_lock(target, [{"dst": "AGENTS.md", "hash": "not-a-hash"}])  # bad hash
    assert verify_integrity.verify(target) == 1


def test_main_documented_invocation(tmp_path: Path) -> None:
    """The documented `--target` CLI shape returns 0 on a clean install
    (smoke test -- protects the invocation SECURITY.md publishes)."""
    assert _install(tmp_path) == 0
    assert verify_integrity.main(["--target", str(tmp_path)]) == 0


# ---------------------------------------------------------------------------
# Forked-facade / dormant-engine advisory (foldback rollup #4)
# ---------------------------------------------------------------------------

from bootstrap._scaffold.lockfile import (  # noqa: E402
    forked_facade_findings,
    format_forked_facade_warning,
)


def _facade_entry(
    target: Path, dst_rel: str, *, forked: bool, engine: bool,
    acknowledged: bool = False,
) -> dict:
    """Write a verbatim facade file (+ optionally its engine package) under
    *target* and return its lockfile record.  ``forked`` => base_hash != hash."""
    f = target / dst_rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text("# facade launcher\n", encoding="utf-8")
    h = "sha256:" + hashlib.sha256(f.read_bytes()).hexdigest()
    if engine:
        eng = target / Path(dst_rel).with_name("_" + Path(dst_rel).stem)
        eng.mkdir(parents=True, exist_ok=True)
        (eng / "__init__.py").write_text("", encoding="utf-8")
    rec = {
        "dst": dst_rel, "hash": h, "verbatim": True,
        "base_hash": ("sha256:" + "a" * 64) if forked else h,
    }
    if acknowledged:
        rec["fork_acknowledged"] = True
    return rec


def test_forked_facade_with_dormant_engine_warns(tmp_path, capsys) -> None:
    target = tmp_path / "repo"
    rec = _facade_entry(target, "tools/intent.py", forked=True, engine=True)
    _write_lock(target, [rec])
    assert verify_integrity.verify(target) == 0  # advisory only, never fails
    err = capsys.readouterr().err
    assert "forked from upstream" in err
    assert "tools/_intent" in err
    assert "fork_acknowledged" in err  # the verify-time opt-out is offered


def test_forked_facade_acknowledged_is_silent_at_verify(tmp_path, capsys) -> None:
    target = tmp_path / "repo"
    rec = _facade_entry(target, "tools/intent.py", forked=True, engine=True,
                        acknowledged=True)
    _write_lock(target, [rec])
    assert verify_integrity.verify(target) == 0
    err = capsys.readouterr().err
    assert "forked from upstream" not in err  # acknowledged -> silenced


def test_clean_facade_no_warning(tmp_path, capsys) -> None:
    target = tmp_path / "repo"
    rec = _facade_entry(target, "tools/intent.py", forked=False, engine=True)
    _write_lock(target, [rec])
    assert verify_integrity.verify(target) == 0
    assert "forked from upstream" not in capsys.readouterr().err


def test_forked_facade_without_engine_no_warning(tmp_path, capsys) -> None:
    target = tmp_path / "repo"
    rec = _facade_entry(target, "tools/intent.py", forked=True, engine=False)
    _write_lock(target, [rec])
    assert verify_integrity.verify(target) == 0
    assert "forked from upstream" not in capsys.readouterr().err


def test_findings_skip_non_verbatim_and_format_upgrade_branch(tmp_path) -> None:
    target = tmp_path / "repo"
    # A forked non-verbatim entry (mergeable) is not a facade fork -> skipped.
    rec = _facade_entry(target, "tools/intent.py", forked=True, engine=True)
    rec["verbatim"] = False
    _write_lock(target, [rec])
    lock = read_lockfile(target)
    assert forked_facade_findings(target, lock, upstream=None) == []
    # The upgrade-time formatting omits the verify-only fork_acknowledged hint.
    msg = format_forked_facade_warning(
        {"dst": "tools/intent.py", "engine": "tools/_intent",
         "acknowledged": False},
        at_upgrade=True,
    )
    assert "upgrade:" in msg
    assert "fork_acknowledged" not in msg


# ---------------------------------------------------------------------------
# The slot note: a separate advisory pass that runs after the verdict
# ---------------------------------------------------------------------------
#
# The note reads files the integrity pass never opened (base copies, living-
# state files) and must not be able to change what ``verify`` returns, however
# those files or the lockfile are shaped.  Every case below builds its own
# tree from the module-level builders, so a script can build the same trees.

import ast  # noqa: E402
import importlib.util  # noqa: E402
import inspect  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
from typing import Callable, NamedTuple  # noqa: E402

from bootstrap._scaffold.lockfile import _emit_lock_yaml  # noqa: E402

_VERIFY_PY = CAIRN_ROOT / "bootstrap" / "verify_integrity.py"
_CAP = 256 * 1024


def _sha(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _store_lock(target: Path, lock: dict) -> None:
    path = target / "dev" / ".cairn" / "cairn-lock.yml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_emit_lock_yaml(lock), encoding="utf-8")


def _edit_lock(target: Path, change: Callable[[dict], None]) -> None:
    lock = read_lockfile(target)
    change(lock)
    _store_lock(target, lock)


def _lock_rec(lock: dict, dst: str) -> dict:
    return next(r for r in lock["files"] if r["dst"] == dst)


def _note_tree(target: Path, specs: list, tokens: dict | None = None) -> None:
    """Write files, base copies and a lockfile for *specs*.

    A spec is a dict: ``dst``, ``installed`` (bytes), ``base`` (bytes, or
    ``None`` for a record with no base copy), ``verbatim``, ``living``.  The
    recorded hashes match the bytes written, so the integrity pass accepts
    every file unless the case then changes something.
    """
    records = []
    for spec in specs:
        dst = spec["dst"]
        installed = spec.get("installed", b"installed text\n")
        base = spec.get("base", installed)
        path = target / dst
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(installed)
        rec = {"dst": dst, "src": dst, "hash": _sha(installed),
               "verbatim": bool(spec.get("verbatim"))}
        if spec.get("living"):
            rec["living_state"] = True
        if base is not None:
            cache = f"dev/.cairn/base/{dst}"
            cache_path = target / cache
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_bytes(base)
            rec["base_cache"] = cache
            rec["base_hash"] = _sha(base)
        records.append(rec)
    _store_lock(target, {"schema": 1, "tokens": dict(tokens or {}),
                         "files": records})


def _base_file(target: Path, dst: str) -> Path:
    return target / "dev" / ".cairn" / "base" / dst


_NO_NOTE = "v._slot_note = lambda *a, **k: None\n"


def _run_verify(target: Path, module_file: Path = _VERIFY_PY, *,
                note: bool = True, patch: str = "", timeout: int = 20):
    """Run ``main(["--target", target])`` of *module_file* in a fresh process.

    A process, not a call: a case that makes the note block would otherwise
    hang the suite, and a timeout turns it into a failure.  ``note=False``
    replaces the note with a no-op, the other half of the verdict comparison.
    *patch* is Python run after the import (to reshape the lockfile as it is
    read, for shapes JSON cannot carry).
    """
    code = (
        "import importlib.util, sys\n"
        f"spec = importlib.util.spec_from_file_location('vi_under_test', {str(module_file)!r})\n"
        "v = importlib.util.module_from_spec(spec)\n"
        "sys.modules['vi_under_test'] = v\n"
        "spec.loader.exec_module(v)\n"
        + patch
        + ("" if note else _NO_NOTE)
        + f"raise SystemExit(v.main(['--target', {str(target)!r}]))\n"
    )
    return subprocess.run(
        [sys.executable, "-c", code], capture_output=True, timeout=timeout)


def _text(data: bytes) -> str:
    return data.decode("utf-8", errors="replace")


def _without_note(text: str) -> str:
    return "\n".join(line for line in text.splitlines()
                     if not line.startswith("slot note:"))


def _note_lines(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.startswith("slot note:")]


_COVERAGE_RE = re.compile(
    r"slot note: files in scope (\d+); checked (\d+); slots checked (\d+), "
    r"listed (\d+), empty \(filled when its module is installed\) (\d+); "
    r"not checked: no base copy (\d+), failed the integrity check (\d+), "
    r"base hash mismatch (\d+), unreadable (\d+)$"
)
_COVERAGE_KEYS = ("in_scope", "checked", "slots_checked", "listed", "empty",
                  "no_base_copy", "failed", "hash_mismatch", "unreadable")


def _coverage(stderr: str) -> dict:
    """The coverage line's figures, by name.  Fails if there is not exactly
    one such line: the note always prints it, once, when it runs."""
    found = [m for m in map(_COVERAGE_RE.match, _note_lines(stderr)) if m]
    assert len(found) == 1, _note_lines(stderr)
    return dict(zip(_COVERAGE_KEYS, map(int, found[0].groups())))


def _clean_tree(target: Path, **extra) -> None:
    """A control file and a victim file, both accepted and both checked."""
    _note_tree(target, [
        {"dst": "ctl.md", "installed": b"control\n"},
        {"dst": "notes.md", "installed": b"victim\n", **extra},
    ])


class _Hostile(NamedTuple):
    """One lockfile or file shape the note must survive without changing the
    verdict.  ``expect`` is the coverage the case must show: the hostile value
    has to reach the note, or the comparison proves nothing."""
    id: str
    build: Callable[[Path], str]      # builds the tree; returns patch code
    expect: dict


def _victim_base(target: Path) -> Path:
    return _base_file(target, "notes.md")


def _set(rec_field: str, value) -> Callable[[Path], str]:
    def build(target: Path) -> str:
        _clean_tree(target)
        _edit_lock(target, lambda lock: _lock_rec(lock, "notes.md").__setitem__(
            rec_field, value))
        return ""
    return build


def _need(feature: str) -> None:
    if not hasattr(os, feature):
        pytest.skip(f"os.{feature} not available")


def _b_dir(target: Path) -> str:
    _clean_tree(target)
    (target / "dev" / ".cairn" / "base" / "adir").mkdir()
    _edit_lock(target, lambda lock: _lock_rec(lock, "notes.md").__setitem__(
        "base_cache", "dev/.cairn/base/adir"))
    return ""


def _b_fifo(target: Path) -> str:
    _need("mkfifo")
    _clean_tree(target)
    _victim_base(target).unlink()
    os.mkfifo(_victim_base(target))
    return ""


def _b_symlink_leaf(target: Path) -> str:
    _need("symlink")
    _clean_tree(target)
    real = _base_file(target, "notes.real.md")
    real.write_bytes(_victim_base(target).read_bytes())
    _victim_base(target).unlink()
    os.symlink(real.name, _victim_base(target))
    return ""


def _b_symlink_parent(target: Path) -> str:
    _need("symlink")
    _clean_tree(target)
    cache = target / "dev" / ".cairn"
    (cache / "realsub").mkdir()
    (cache / "realsub" / "notes.md").write_bytes(b"victim\n")
    os.symlink("../realsub", cache / "base" / "sub")
    _edit_lock(target, lambda lock: _lock_rec(lock, "notes.md").__setitem__(
        "base_cache", "dev/.cairn/base/sub/notes.md"))
    return ""


def _b_outside_target(target: Path) -> str:
    _clean_tree(target)
    (target.parent / "outside.md").write_bytes(b"victim\n")
    _edit_lock(target, lambda lock: _lock_rec(lock, "notes.md").__setitem__(
        "base_cache", "../outside.md"))
    return ""


def _b_outside_base_dir(target: Path) -> str:
    _clean_tree(target)
    (target / "other.md").write_bytes(b"victim\n")
    _edit_lock(target, lambda lock: _lock_rec(lock, "notes.md").__setitem__(
        "base_cache", "other.md"))
    return ""


def _b_over_cap(target: Path) -> str:
    _clean_tree(target)
    big = b"b" * (_CAP + 1)
    _victim_base(target).write_bytes(big)
    _edit_lock(target, lambda lock: _lock_rec(lock, "notes.md").__setitem__(
        "base_hash", _sha(big)))
    return ""


def _b_not_utf8(target: Path) -> str:
    _clean_tree(target)
    bad = b"\xff\xfe not utf-8\n"
    _victim_base(target).write_bytes(bad)
    _edit_lock(target, lambda lock: _lock_rec(lock, "notes.md").__setitem__(
        "base_hash", _sha(bad)))
    return ""


def _t_non_string_key(target: Path) -> str:
    _clean_tree(target)
    return ("_orig = v.read_lockfile\n"
            "def _patched(t):\n"
            "    lock = _orig(t)\n"
            "    lock['tokens'] = {1: 'x'}\n"
            "    return lock\n"
            "v.read_lockfile = _patched\n")


def _i_not_utf8(target: Path) -> str:
    bad = b"\xff\xfe not utf-8\n"
    _note_tree(target, [{"dst": "ctl.md"},
                        {"dst": "notes.md", "installed": bad, "base": b"base\n"}])
    return ""


def _i_over_cap(target: Path) -> str:
    big = b"i" * (_CAP + 1)
    _note_tree(target, [{"dst": "ctl.md"},
                        {"dst": "notes.md", "installed": big, "base": b"base\n"}])
    return ""


_LIVING = "dev/PLANNING.md"


def _living_tree(target: Path, installed: bytes = b"roadmap\n") -> None:
    _note_tree(target, [{"dst": "ctl.md"},
                        {"dst": _LIVING, "installed": installed,
                         "base": b"roadmap\n", "living": True}])


def _l_fifo(target: Path) -> str:
    _need("mkfifo")
    _living_tree(target)
    (target / _LIVING).unlink()
    os.mkfifo(target / _LIVING)
    return ""


def _l_symlink_leaf(target: Path) -> str:
    _need("symlink")
    _living_tree(target)
    (target / "dev" / "live.real.md").write_bytes(b"roadmap\n")
    (target / _LIVING).unlink()
    os.symlink("live.real.md", target / _LIVING)
    return ""


def _l_symlink_parent(target: Path) -> str:
    _need("symlink")
    _living_tree(target)
    (target / "dev").rename(target / "devreal")
    os.symlink("devreal", target / "dev")
    return ""


def _l_directory(target: Path) -> str:
    _living_tree(target)
    (target / _LIVING).unlink()
    (target / _LIVING).mkdir()
    return ""


def _l_over_cap(target: Path) -> str:
    _living_tree(target, b"l" * (_CAP + 1))
    return ""


def _l_not_utf8(target: Path) -> str:
    _living_tree(target, b"\xff\xfe not utf-8\n")
    return ""


_ONE_BAD = {"in_scope": 2, "checked": 1, "unreadable": 1}
_ALL_BAD = {"in_scope": 2, "checked": 0, "unreadable": 2}

_HOSTILE_CASES: list[_Hostile] = [
    _Hostile("base_cache-not-a-string", _set("base_cache", 7), _ONE_BAD),
    _Hostile("base_cache-a-directory", _b_dir, _ONE_BAD),
    _Hostile("base_cache-a-fifo", _b_fifo, _ONE_BAD),
    _Hostile("base_cache-a-symlink", _b_symlink_leaf, _ONE_BAD),
    _Hostile("base_cache-symlinked-parent", _b_symlink_parent, _ONE_BAD),
    _Hostile("base_cache-outside-the-target", _b_outside_target, _ONE_BAD),
    _Hostile("base_cache-outside-base-dir", _b_outside_base_dir, _ONE_BAD),
    _Hostile("base_cache-nul-byte", _set("base_cache", "dev/.cairn/base/no\x00tes.md"), _ONE_BAD),
    _Hostile("base-copy-over-the-cap", _b_over_cap, _ONE_BAD),
    _Hostile("base-copy-not-utf8", _b_not_utf8, _ONE_BAD),
    _Hostile("base_hash-does-not-match", _set("base_hash", "sha256:" + "0" * 64),
             {"in_scope": 2, "checked": 1, "hash_mismatch": 1}),
    _Hostile("base_hash-not-a-string", _set("base_hash", 5),
             {"in_scope": 2, "checked": 1, "hash_mismatch": 1}),
    _Hostile("tokens-not-a-mapping",
             lambda t: (_clean_tree(t), _edit_lock(
                 t, lambda lock: lock.__setitem__("tokens", ["a"])), "")[2],
             _ALL_BAD),
    _Hostile("tokens-non-string-key", _t_non_string_key, _ALL_BAD),
    _Hostile("tokens-non-string-value",
             lambda t: (_clean_tree(t), _edit_lock(
                 t, lambda lock: lock.__setitem__("tokens", {"a": 5})), "")[2],
             _ALL_BAD),
    _Hostile("installed-not-utf8", _i_not_utf8, _ONE_BAD),
    _Hostile("installed-over-the-cap", _i_over_cap, _ONE_BAD),
    _Hostile("living-a-fifo", _l_fifo, _ONE_BAD),
    _Hostile("living-a-symlink", _l_symlink_leaf, _ONE_BAD),
    _Hostile("living-symlinked-parent", _l_symlink_parent, _ALL_BAD),
    _Hostile("living-a-directory", _l_directory, _ONE_BAD),
    _Hostile("living-over-the-cap", _l_over_cap, _ONE_BAD),
    _Hostile("living-not-utf8", _l_not_utf8, _ONE_BAD),
]


def _expected_coverage(expect: dict) -> dict:
    return {key: expect.get(key, 0) for key in _COVERAGE_KEYS}


@pytest.mark.parametrize("case", _HOSTILE_CASES, ids=lambda c: c.id)
def test_no_lockfile_or_file_shape_changes_the_verdict(
    case: _Hostile, tmp_path: Path
) -> None:
    """Whatever the note meets, ``verify`` returns the same code and prints the
    same report as when the note does nothing.  Each case also shows the
    hostile value reached the note and was counted under the expected reason;
    a comparison that never reached the note would pass for any code."""
    target = tmp_path / "repo"
    target.mkdir()
    patch = case.build(target)
    with_note = _run_verify(target, patch=patch)
    without = _run_verify(target, patch=patch, note=False)
    assert (with_note.returncode, _text(with_note.stdout),
            _without_note(_text(with_note.stderr))) == (
        without.returncode, _text(without.stdout),
        _without_note(_text(without.stderr)))
    assert with_note.returncode == 0, _text(with_note.stderr)
    assert _coverage(_text(with_note.stderr)) == _expected_coverage(case.expect)
    assert _note_lines(_text(without.stderr)) == []


def _spy_note(monkeypatch, capsys, calls: list) -> None:
    def spy(*args, **kwargs):
        calls.append(capsys.readouterr())
    monkeypatch.setattr(verify_integrity, "_slot_note", spy)


def test_the_note_runs_after_the_report_on_a_passing_run(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    _clean_tree(tmp_path)
    calls: list = []
    _spy_note(monkeypatch, capsys, calls)
    assert verify_integrity.verify(tmp_path) == 0
    assert len(calls) == 1
    assert "verify_integrity: OK" in calls[0].out


def test_the_note_runs_after_the_report_on_a_failing_run(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    _clean_tree(tmp_path)
    (tmp_path / "notes.md").write_bytes(b"tampered\n")
    calls: list = []
    _spy_note(monkeypatch, capsys, calls)
    assert verify_integrity.verify(tmp_path) == 1
    assert len(calls) == 1
    assert "1 integrity violation(s)" in calls[0].err
    assert "modified (hash mismatch): notes.md" in calls[0].err


def test_a_fail_closed_early_return_never_calls_the_note(
    tmp_path: Path, monkeypatch
) -> None:
    calls: list = []
    monkeypatch.setattr(verify_integrity, "_slot_note",
                        lambda *a, **k: calls.append(a))
    assert verify_integrity.verify(tmp_path) == 1          # no lockfile
    _store_lock(tmp_path, {"files": []})
    assert verify_integrity.verify(tmp_path) == 1          # records no files
    assert calls == []


def test_the_report_comes_before_the_note_in_a_merged_stream(
    tmp_path: Path
) -> None:
    """Stdout is block-buffered when piped and stderr is not, so without a
    flush before the note a merged log shows the note first.  Captured output
    in-process cannot show this; a real pipe can."""
    _clean_tree(tmp_path)
    proc = subprocess.run(
        [sys.executable, str(_VERIFY_PY), "--target", str(tmp_path)],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=20)
    merged = _text(proc.stdout)
    assert proc.returncode == 0
    assert merged.index("verify_integrity: OK") < merged.index("slot note:")


def test_the_note_is_handed_nothing_that_could_change_the_verdict() -> None:
    names = list(inspect.signature(verify_integrity._slot_note).parameters)
    assert names == ["target", "accepted", "living", "tokens", "failed"]
    for name in names:
        assert not re.search(r"violation|skipped|exit|code", name)


class _Boom(Exception):
    pass


def test_an_exception_in_the_note_becomes_one_line_naming_only_its_type(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    _clean_tree(tmp_path)

    def boom(*args, **kwargs):
        raise RuntimeError("\x1b[31msecret from the tree\x1b[0m")

    monkeypatch.setattr(verify_integrity, "_slot_note", boom)
    capsys.readouterr()
    assert verify_integrity.verify(tmp_path) == 0
    err = capsys.readouterr().err
    assert _note_lines(err) == ["slot note: not run (RuntimeError)"]
    assert "secret" not in err and "\x1b" not in err


def test_a_system_exit_in_the_note_is_fenced_and_the_code_is_kept(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    _clean_tree(tmp_path)

    def leave(*args, **kwargs):
        raise SystemExit(3)

    monkeypatch.setattr(verify_integrity, "_slot_note", leave)
    capsys.readouterr()
    assert verify_integrity.verify(tmp_path) == 0
    assert _note_lines(capsys.readouterr().err) == [
        "slot note: not run (SystemExit)"]
    (tmp_path / "notes.md").write_bytes(b"tampered\n")
    assert verify_integrity.verify(tmp_path) == 1


def test_a_keyboard_interrupt_in_the_note_is_not_swallowed(
    tmp_path: Path, monkeypatch
) -> None:
    _clean_tree(tmp_path)

    def interrupt(*args, **kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(verify_integrity, "_slot_note", interrupt)
    with pytest.raises(KeyboardInterrupt):
        verify_integrity.verify(tmp_path)


def test_a_record_with_an_unsafe_base_copy_still_fails_on_its_own(
    tmp_path: Path, capsys
) -> None:
    _clean_tree(tmp_path)
    _edit_lock(tmp_path, lambda lock: _lock_rec(lock, "notes.md").__setitem__(
        "base_cache", "../../etc/passwd"))
    (tmp_path / "notes.md").write_bytes(b"modified after install\n")
    capsys.readouterr()
    assert verify_integrity.verify(tmp_path) == 1
    err = capsys.readouterr().err
    assert "modified (hash mismatch): notes.md" in err
    assert _coverage(err) == _expected_coverage(
        {"in_scope": 2, "checked": 1, "failed": 1})


def test_open_flags_are_built_when_the_note_runs_not_when_the_module_loads(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    tree = ast.parse(_VERIFY_PY.read_text(encoding="utf-8"))
    top_level = [s for s in tree.body
                 if not isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef))]
    named = [n.attr for s in top_level for n in ast.walk(s)
             if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name)
             and n.value.id == "os" and n.attr.startswith("O_")]
    assert named == []
    # A platform without the flags still imports the module and reads files.
    for flag in ("O_NOFOLLOW", "O_NONBLOCK", "O_NOCTTY"):
        monkeypatch.delattr(os, flag, raising=False)
    spec = importlib.util.spec_from_file_location("vi_without_flags", _VERIFY_PY)
    fresh = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fresh)
    _clean_tree(tmp_path)
    capsys.readouterr()
    assert fresh.verify(tmp_path) == 0
    assert _coverage(capsys.readouterr().err) == _expected_coverage(
        {"in_scope": 2, "checked": 2})


def test_one_reader_opens_every_file_the_note_reads() -> None:
    """A second reader (``Path.read_bytes`` on a living-state file) would
    block forever on a FIFO, after the report and before the code reaches
    the caller.  Every read in this module is the integrity loop's own or the
    shared bounded reader's single ``os.open``."""
    tree = ast.parse(_VERIFY_PY.read_text(encoding="utf-8"))
    reads = []
    for func in ast.walk(tree):
        if isinstance(func, ast.FunctionDef):
            for node in ast.walk(func):
                if (isinstance(node, ast.Call)
                        and isinstance(node.func, ast.Attribute)
                        and node.func.attr in {"read_bytes", "read_text", "open"}):
                    reads.append((func.name, node.func.attr))
                elif (isinstance(node, ast.Call)
                        and isinstance(node.func, ast.Name)
                        and node.func.id == "open"):
                    reads.append((func.name, "open"))
    assert sorted(reads) == [("_read_bounded", "open"), ("verify", "read_bytes")]


def _cap_tree(target: Path, base_len: int, installed_len: int) -> None:
    base = b"b" * base_len
    installed = b"i" * installed_len
    _note_tree(target, [{"dst": "sized.md", "installed": installed, "base": base}])


def test_a_file_of_exactly_the_cap_is_read_and_one_byte_more_is_not(
    tmp_path: Path, capsys
) -> None:
    for name, base_len, installed_len, bucket in (
        ("base-at-cap", _CAP, 10, "checked"),
        ("base-over", _CAP + 1, 10, "unreadable"),
        ("installed-at-cap", 10, _CAP, "checked"),
        ("installed-over", 10, _CAP + 1, "unreadable"),
    ):
        target = tmp_path / name
        target.mkdir()
        _cap_tree(target, base_len, installed_len)
        capsys.readouterr()
        assert verify_integrity.verify(target) == 0
        cov = _coverage(capsys.readouterr().err)
        assert cov["in_scope"] == 1 and cov[bucket] == 1, (name, cov)


def test_every_file_in_scope_lands_in_exactly_one_bucket(
    tmp_path: Path, capsys
) -> None:
    _note_tree(tmp_path, [
        {"dst": "checked.md"},
        {"dst": "no-base.md", "base": None},
        {"dst": "bad-base.md"},
        {"dst": "unreadable.md"},
        {"dst": "failed.md"},
        {"dst": "script.py", "verbatim": True, "base": None},
    ])
    (_base_file(tmp_path, "bad-base.md")).write_bytes(b"changed after hashing\n")
    _edit_lock(tmp_path, lambda lock: _lock_rec(lock, "unreadable.md").__setitem__(
        "base_cache", 3))
    (tmp_path / "failed.md").write_bytes(b"modified after install\n")
    capsys.readouterr()
    assert verify_integrity.verify(tmp_path) == 1
    cov = _coverage(capsys.readouterr().err)
    assert cov == _expected_coverage({
        "in_scope": 5, "checked": 1, "no_base_copy": 1, "failed": 1,
        "hash_mismatch": 1, "unreadable": 1})
    assert cov["in_scope"] == (cov["checked"] + cov["no_base_copy"]
                               + cov["failed"] + cov["hash_mismatch"]
                               + cov["unreadable"])


def test_the_coverage_line_is_printed_when_nothing_can_be_checked(
    tmp_path: Path, capsys
) -> None:
    _note_tree(tmp_path, [{"dst": "a.md", "base": None},
                          {"dst": "b.md", "base": None}])
    capsys.readouterr()
    assert verify_integrity.verify(tmp_path) == 0
    err = capsys.readouterr().err
    assert _coverage(err) == _expected_coverage({"in_scope": 2, "no_base_copy": 2})
    assert all(line.startswith("slot note:") for line in err.splitlines())


def test_a_verbatim_record_is_neither_opened_nor_counted(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    """A verbatim record is a script; a script that quotes slot markers in
    code (as the onboarding package does) holds no slots, so the note must
    not touch it."""
    quoted = b'MARKER = "<!-- cairn:slot x -->"\n'
    _note_tree(tmp_path, [{"dst": "tool.py", "installed": quoted,
                           "verbatim": True, "base": None},
                          {"dst": "doc.md"}])
    real_open = os.open
    opened: list[str] = []

    def spy_open(path, *args, **kwargs):
        opened.append(str(path))
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(os, "open", spy_open)
    capsys.readouterr()
    assert verify_integrity.verify(tmp_path) == 0
    monkeypatch.undo()
    assert not any(p.endswith("tool.py") for p in opened), opened
    assert _coverage(capsys.readouterr().err)["in_scope"] == 1


def test_a_living_state_file_is_read_and_counted_like_any_other(
    tmp_path: Path, capsys
) -> None:
    _living_tree(tmp_path)
    capsys.readouterr()
    assert verify_integrity.verify(tmp_path) == 0
    assert _coverage(capsys.readouterr().err) == _expected_coverage(
        {"in_scope": 2, "checked": 2})


def test_a_living_state_flag_outside_the_authorised_set_is_counted_as_failed_and_not_read(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    _note_tree(tmp_path, [{"dst": "ctl.md"}, {"dst": "script.md"}])
    _edit_lock(tmp_path, lambda lock: _lock_rec(lock, "script.md").__setitem__(
        "living_state", True))
    real_open = os.open
    opened: list[str] = []

    def spy_open(path, *args, **kwargs):
        opened.append(str(path))
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(os, "open", spy_open)
    capsys.readouterr()
    assert verify_integrity.verify(tmp_path) == 1
    monkeypatch.undo()
    err = capsys.readouterr().err
    assert "illegal living_state opt-out: script.md" in err
    assert _coverage(err) == _expected_coverage(
        {"in_scope": 2, "checked": 1, "failed": 1})
    assert not any(p.endswith("script.md") for p in opened), opened


@pytest.mark.skipif(not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "symlink"),
                    reason="needs O_NOFOLLOW and symlinks")
def test_a_file_swapped_for_a_symlink_after_the_path_walk_is_refused(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    """The component walk and the open are two steps, so a link swapped in
    between must still be refused: the open itself does not follow links.
    The walk is made to see a plain file, as it would if the swap came after
    it; the base copy's bytes match its recorded hash, so only the open can
    stop the read."""
    _clean_tree(tmp_path)
    base = _victim_base(tmp_path)
    real = base.with_name("notes.real.md")
    real.write_bytes(base.read_bytes())
    base.unlink()
    os.symlink(real.name, base)
    real_lstat = os.lstat

    def lstat_before_the_swap(path, *args, **kwargs):
        if str(path) == str(base):
            return os.stat(real)
        return real_lstat(path, *args, **kwargs)

    monkeypatch.setattr(os, "lstat", lstat_before_the_swap)
    capsys.readouterr()
    assert verify_integrity.verify(tmp_path) == 0
    monkeypatch.undo()
    assert _coverage(capsys.readouterr().err) == _expected_coverage(
        {"in_scope": 2, "checked": 1, "unreadable": 1})
