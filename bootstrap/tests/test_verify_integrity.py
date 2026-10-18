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
