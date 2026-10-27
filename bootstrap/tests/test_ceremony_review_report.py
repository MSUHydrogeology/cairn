"""Tests for what the re-anchor ceremony shows its reader and what it scans.

The reader of a ceremony (a fresh agent, then the Maintainer) trusts the report
the checker prints and the scanners that run over the closure. These nodes pin
the scan coverage and the report's contents against planted lines and against
mutations of the real code, never against a restatement of its own logic.
"""
from __future__ import annotations

import sys
from pathlib import Path

CAIRN_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap import security_check  # noqa: E402
from bootstrap.tests import _gate_preflight as P  # noqa: E402


# ---------------------------------------------------------------------------
# scan coverage
# ---------------------------------------------------------------------------

def test_release_scan_covers_every_python_member_of_the_authority_closure() -> None:
    """The closure decides what a ceremony blesses and runs, yet lives under
    ``bootstrap/tests/``, which the scan globs skip on purpose. So the release
    scan names its Python members itself, and this node compares that list with
    the checker's own declared closure: a member added there and not scanned
    fails here. Two spellings on purpose -- the scan module cannot import test
    code, so only a test can hold them equal."""
    closure_py = {p for p in P.declared_authority_closure() if p.endswith(".py")}
    assert len(closure_py) == 7, closure_py
    scanned = set(security_check.scan_targets())
    missing = sorted(closure_py - scanned)
    assert not missing, f"closure members the release scan skips: {missing}"
    # and nothing else under bootstrap/tests/ rides along (attack fixtures)
    extra = sorted(t for t in scanned
                   if t.startswith("bootstrap/tests/") and t not in closure_py)
    assert not extra, extra


# ---------------------------------------------------------------------------
# the range report: roles, the line scan, and the anchored digest
# ---------------------------------------------------------------------------
#
# Every node builds a real throwaway repository with two commits (anchor and
# candidate) and reads the report the checker derives from them. The oracle is
# git plus the planted line, never a restatement of the scan's own logic.

import os  # noqa: E402
import subprocess  # noqa: E402

import pytest  # noqa: E402

_CLOSURE_PY = ("_gate_preflight.py", "_gate_manifest.py", "_gate_reanchor.py",
               "_gate_transition.py", "_oracle_activation.py", "_oracle.py",
               "_oracle_trust.py")

#: One planted line per pattern. Each must hit its own pattern.
_PLANTED = {
    "process-start": "import subprocess",
    "network": "import urllib.request",
    "dynamic-code": "value = eval(text)",
    "shell-true": "run(cmd, shell=True)",
    "file-write": "target.write_text(data)",
    "nosec": "x = 1  # nosec",
    "shell-command": 'rm -rf "$HOME"',
}


def _fx(repo: Path, *args: str, stdin: bytes | None = None) -> str:
    """Drive the FIXTURE repository with plain git, not with the subject."""
    proc = subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=Fixture",
         "-c", "user.email=fixture@example", "-c", "commit.gpgsign=false",
         "-c", "core.hooksPath=/dev/null", *args],
        input=stdin, capture_output=True, check=False)
    assert proc.returncode == 0, (args, proc.stderr.decode(errors="replace"))
    return proc.stdout.decode(errors="replace").strip()


def _write(repo: Path, rel: str, data: bytes | str, *, mode: int = 0o644) -> None:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data if isinstance(data, bytes) else data.encode())
    path.chmod(mode)


def _make_range(tmp_path: Path, anchor_files: dict, candidate_files: dict,
                *, setup=None) -> tuple[Path, str, str]:
    """A repository whose first commit holds *anchor_files* and whose second
    commit adds or replaces *candidate_files* (a value of None deletes)."""
    repo = tmp_path / "repo"
    repo.mkdir(parents=True)
    _fx(repo, "init", "-q", "-b", "main")
    for rel, data in anchor_files.items():
        _write(repo, rel, data)
    if setup:
        setup(repo)
    _fx(repo, "add", "-A")
    _fx(repo, "commit", "-q", "-m", "anchor")
    anchor = _fx(repo, "rev-parse", "HEAD")
    for rel, data in candidate_files.items():
        if data is None:
            (repo / rel).unlink()
        else:
            _write(repo, rel, data)
    _fx(repo, "add", "-A")
    _fx(repo, "commit", "-q", "-m", "candidate")
    return repo, anchor, _fx(repo, "rev-parse", "HEAD")


def _report(repo: Path, anchor: str, head: str) -> dict:
    return P.range_review_report(anchor, head, branch="refs/heads/main",
                                 expected_old=head, repo=repo,
                                 prospective_manifest=b"{}\n")


def _hits(report: dict, path: str | None = None) -> list[tuple]:
    return [(h["path"], h["line"], h["pattern"]) for h in report["scan"]["hits"]
            if path is None or h["path"] == path]


#: Typed by hand, not read from the checker: the files the driver runs beside
#: the closure. If the checker's own list drifted, a shared derivation would
#: drift with it.
_DRIVER_PATHS = ("scripts/repin.py", "scripts/reanchor_ceremony.py",
                 "bootstrap/tests/conftest.py")


def _decides_paths() -> list[str]:
    return sorted(set(P.declared_authority_closure()) | set(_DRIVER_PATHS))


class TestReportRolesAndSchema:

    def test_the_schema_is_the_second_version_and_every_path_has_a_role(
            self, tmp_path):
        repo, a, h = _make_range(
            tmp_path, {"README.md": "x\n", "bootstrap/tests/_oracle.py": "a = 1\n",
                       "scripts/other.py": "a = 1\n"},
            {"bootstrap/tests/_oracle.py": "a = 2\n", "scripts/other.py": "a = 2\n",
             "docs/note.md": "n\n"})
        rep = _report(repo, a, h)
        assert rep["schema"] == "cairn-range-review/v2"
        by_path = {e["display"]: e for e in rep["paths"]}
        assert by_path["bootstrap/tests/_oracle.py"]["role"] == "decides"
        assert by_path["scripts/other.py"]["role"] == "pinned"
        assert by_path["docs/note.md"]["role"] == "other"
        assert by_path["docs/note.md"]["change"] == "added"
        assert by_path["scripts/other.py"]["change"] == "modified"
        assert sum(rep["role_counts"].values()) == len(rep["paths"])

    def test_every_deciding_path_is_labelled_decides(self, tmp_path):
        """The role is the policy; a deciding path labelled anything else is
        scanned as if it did not decide anything."""
        files = {rel: "a = 1\n" for rel in _decides_paths()}
        repo, a, h = _make_range(tmp_path, files,
                                 {rel: "a = 2\n" for rel in files})
        rep = _report(repo, a, h)
        wrong = [e["display"] for e in rep["paths"] if e["role"] != "decides"]
        assert not wrong, wrong
        assert len(rep["by_role"]["decides"]) == len(files)


class TestLineScan:

    @pytest.mark.parametrize("pattern", sorted(_PLANTED))
    def test_a_planted_line_is_reported_under_its_pattern(self, tmp_path, pattern):
        repo, a, h = _make_range(
            tmp_path, {"bootstrap/tests/_oracle.py": "a = 1\n"},
            {"bootstrap/tests/_oracle.py": "a = 1\n" + _PLANTED[pattern] + "\n"})
        rep = _report(repo, a, h)
        assert _hits(rep) == [("bootstrap/tests/_oracle.py", 2, pattern)], rep["scan"]
        assert rep["scan"]["counts"][pattern] == 1

    def test_a_range_with_no_planted_line_reports_zero_for_every_pattern(
            self, tmp_path):
        """The control: zeros are listed, so an absent pattern is not mistaken
        for one the scan never had."""
        repo, a, h = _make_range(
            tmp_path, {"bootstrap/tests/_oracle.py": "a = 1\n"},
            {"bootstrap/tests/_oracle.py": "a = 1\nb = 2\n"})
        scan = _report(repo, a, h)["scan"]
        assert scan["hits"] == []
        assert scan["counts"] == {name: 0 for name in
                                  [n for n, _ in P.SCAN_PATTERNS] + ["compiled-file"]}
        assert scan["patterns"] == [n for n, _ in P.SCAN_PATTERNS] + ["compiled-file"], (
            "the page prints one line per name here, so a name left out prints no zero")
        assert scan["scanned"] == ["bootstrap/tests/_oracle.py"]

    @pytest.mark.parametrize("line", [
        'if [ -n "$x" ]; then rm -rf "$HOME"; fi',
        "  mv a b",
        "cd x && cp a b",
        "sudo chmod 777 /etc/x",
        "echo y | tee /etc/x",
        "ssh-add -d key",
        "ssh-keygen -p -f key",
        "ln -s a b",
        "true || chown root x",
    ])
    def test_a_shell_command_that_changes_files_or_keys_is_a_hit(self, tmp_path, line):
        repo, a, h = _make_range(
            tmp_path, {"bootstrap/reanchor.sh": "echo hi\n"},
            {"bootstrap/reanchor.sh": "echo hi\n" + line + "\n"})
        assert [x[2] for x in _hits(_report(repo, a, h))] == ["shell-command"], line

    @pytest.mark.parametrize("line", [
        "printf '%s\\n' \"run rm -rf later\"",       # a word inside a string
        "cp = 3",                                      # a variable, not a command
        "ln(x)",
        "(ssh-add -l) lists the keys",                  # brackets and backticks in prose
        "check `ssh-add -l` first",
        "rm.append(y)",
        "# remove it: rm is not run here",
        "farm -x",
    ])
    def test_prose_and_other_languages_do_not_make_a_shell_command_hit(self, tmp_path, line):
        repo, a, h = _make_range(
            tmp_path, {"bootstrap/reanchor.sh": "echo hi\n"},
            {"bootstrap/reanchor.sh": "echo hi\n" + line + "\n"})
        assert _hits(_report(repo, a, h)) == [], line

    def test_every_deciding_path_is_scanned(self, tmp_path):
        files = {rel: "a = 1\n" for rel in _decides_paths()}
        repo, a, h = _make_range(
            tmp_path, files,
            {rel: "a = 1\nimport subprocess\n" for rel in files})
        rep = _report(repo, a, h)
        hit_paths = {p for p, _l, _n in _hits(rep)}
        assert hit_paths == set(files), sorted(set(files) - hit_paths)

    def test_an_unchanged_line_is_not_a_hit_but_a_moved_line_is_added(
            self, tmp_path):
        old = "import subprocess\nx = 1\n"
        repo, a, h = _make_range(
            tmp_path, {"bootstrap/tests/_oracle.py": old},
            {"bootstrap/tests/_oracle.py": "y = 0\nimport subprocess\nx = 1\n"})
        assert _hits(_report(repo, a, h)) == []
        repo2, a2, h2 = _make_range(
            tmp_path / "second", {"bootstrap/tests/_oracle.py": old},
            {"bootstrap/tests/_oracle.py": old + "import subprocess\n"})
        assert [x[2] for x in _hits(_report(repo2, a2, h2))] == ["process-start"]

    def test_scope_covers_the_roster_and_new_files_and_lists_the_rest(
            self, tmp_path):
        line = "import subprocess\n"
        repo, a, h = _make_range(
            tmp_path,
            {"bootstrap/security_check.py": "a = 1\n",       # sensitive roster
             "bootstrap/tests/test_other.py": "a = 1\n",     # an ordinary test
             "docs/guide.md": "a\n"},
            {"bootstrap/security_check.py": "a = 1\n" + line,
             "bootstrap/tests/test_other.py": "a = 1\n" + line,
             "docs/guide.md": "a\n" + line,
             "scripts/new_tool.py": line,                    # new, outside tests
             "bootstrap/tests/test_new.py": line})           # new, but a test
        rep = _report(repo, a, h)
        assert {p for p, _l, _n in _hits(rep)} == {
            "bootstrap/security_check.py", "scripts/new_tool.py"}
        assert rep["scan"]["scanned"] == [
            "bootstrap/security_check.py", "scripts/new_tool.py"]
        # the rest is counted by class, never silently dropped
        assert sum(rep["scan"]["not_line_scanned"].values()) == 3, rep["scan"]

    def test_a_diff_attribute_does_not_hide_a_hit(self, tmp_path):
        """A `-diff` attribute in the candidate's own tree makes git print
        "Binary files differ" and no lines. The scan reads raw blobs, so the
        planted line is still found."""
        repo, a, h = _make_range(
            tmp_path,
            {"bootstrap/tests/_oracle.py": "a = 1\n", ".gitattributes": ""},
            {"bootstrap/tests/_oracle.py": "a = 1\nimport subprocess\n",
             ".gitattributes": "bootstrap/tests/_oracle.py -diff\n"})
        # the instrument can see the hazard: git itself reports no lines
        shown = _fx(repo, "diff", "-U0", a, h, "--", "bootstrap/tests/_oracle.py")
        assert "Binary files" in shown and "import subprocess" not in shown
        assert _hits(_report(repo, a, h)) == [
            ("bootstrap/tests/_oracle.py", 2, "process-start")]

    def test_every_hit_is_kept_and_none_is_truncated(self, tmp_path):
        body = "".join(f"import subprocess  # {i}\n" for i in range(300))
        repo, a, h = _make_range(
            tmp_path, {"bootstrap/tests/_oracle.py": "a = 1\n"},
            {"bootstrap/tests/_oracle.py": "a = 1\n" + body})
        assert len(_report(repo, a, h)["scan"]["hits"]) == 300

    def test_hit_text_is_escaped_like_a_path(self, tmp_path):
        evil = "import subprocess  # \x1b[31mé \\ end\n"
        repo, a, h = _make_range(
            tmp_path, {"bootstrap/tests/_oracle.py": "a = 1\n"},
            {"bootstrap/tests/_oracle.py": "a = 1\n" + evil})
        text = _report(repo, a, h)["scan"]["hits"][0]["text"]
        assert text == P._display_path(evil.rstrip("\n").encode())
        assert "\x1b" not in text and "é" not in text
        assert all(0x20 <= ord(c) < 0x7F for c in text)

    def test_unreadable_oversized_and_special_mode_blobs_are_listed(
            self, tmp_path):
        planted = "import subprocess\n"
        big = ("# filler\n" * 200000) + planted        # over the read limit
        assert len(big) > P.SCAN_MAX_BLOB_BYTES

        repo, a, h = _make_range(
            tmp_path,
            {"bootstrap/tests/_oracle.py": "a = 1\n",
             "bootstrap/tests/_oracle_trust.py": "a = 1\n",
             "bootstrap/tests/_gate_transition.py": "a = 1\n",
             "bootstrap/security_check.py": "a = 1\n"},
            {"bootstrap/tests/_oracle.py": b"a = 1\n\x00\nimport subprocess\n",
             "bootstrap/tests/_oracle_trust.py": big,
             "bootstrap/tests/_gate_transition.py": b"\xff\xfe invalid utf8\n",
             "bootstrap/security_check.py": "a = 1\n" + planted})
        os.chmod(repo / "bootstrap/security_check.py", 0o755)
        link = repo / "scripts" / "link.py"
        link.parent.mkdir(parents=True)
        os.symlink("bootstrap/security_check.py", link)
        _fx(repo, "add", "-A")
        _fx(repo, "commit", "-q", "-m", "specials")
        sub = _fx(repo, "rev-parse", "HEAD")
        _fx(repo, "update-index", "--add", "--cacheinfo",
            f"160000,{sub},scripts/gitlink")
        _fx(repo, "commit", "-q", "-m", "gitlink")
        head = _fx(repo, "rev-parse", "HEAD")
        rep = _report(repo, a, head)
        listed = {(x["path"], x["reason"]) for x in rep["scan"]["listed"]}
        assert ("bootstrap/tests/_oracle.py", "unreadable") in listed
        assert ("bootstrap/tests/_gate_transition.py", "unreadable") in listed
        assert ("bootstrap/tests/_oracle_trust.py", "oversized") in listed
        assert ("bootstrap/security_check.py", "mode 100755") in listed
        assert ("scripts/link.py", "mode 120000") in listed
        assert ("scripts/gitlink", "mode 160000") in listed
        # the one readable file is still scanned
        assert _hits(rep) == [("bootstrap/security_check.py", 2, "process-start")]

    def test_a_deleted_deciding_path_is_listed_as_nothing_added(self, tmp_path):
        repo, a, h = _make_range(
            tmp_path, {"bootstrap/tests/_oracle.py": "a = 1\n"},
            {"bootstrap/tests/_oracle.py": None})
        rep = _report(repo, a, h)
        assert rep["scan"]["listed"] == [
            {"path": "bootstrap/tests/_oracle.py",
             "reason": "deleted, nothing added"}]


class TestTrackedCompiledFiles:
    """Python loads a compiled file in place of its source, so a reader of the source is not
    reading what runs.  The scan reports every tracked one, whether or not the range touched it."""

    _PYC = "bootstrap/tests/__pycache__/_oracle.cpython-313.pyc"

    def test_a_compiled_file_added_in_the_range_is_a_hit(self, tmp_path):
        repo, a, h = _make_range(
            tmp_path, {"bootstrap/tests/_oracle.py": "a = 1\n"},
            {self._PYC: b"\x00compiled"})
        rep = _report(repo, a, h)
        assert _hits(rep) == [(self._PYC, 0, "compiled-file")]
        assert rep["scan"]["counts"]["compiled-file"] == 1

    def test_a_compiled_file_the_range_did_not_touch_is_still_a_hit(self, tmp_path):
        repo, a, h = _make_range(
            tmp_path, {"bootstrap/tests/_oracle.py": "a = 1\n", self._PYC: b"\x00compiled"},
            {"README.md": "x\n"})
        assert _hits(_report(repo, a, h)) == [(self._PYC, 0, "compiled-file")]

    def test_a_pycache_folder_and_a_pyc_suffix_each_count_and_lookalikes_do_not(self, tmp_path):
        counted = ["pkg/__pycache__/data.txt", "stale.pyc", "a/b/c.pyc"]
        lookalikes = ["pkg/my__pycache__/data.txt", "notes/pyc.md", "x.pyc.txt", "pycache/x.py"]
        repo, a, h = _make_range(tmp_path, {"README.md": "x\n"},
                                 {rel: b"x\n" for rel in counted + lookalikes})
        assert sorted(p for p, _l, n in _hits(_report(repo, a, h)) if n == "compiled-file") == sorted(counted)

    def test_the_tree_a_hand_ceremony_materializes_holds_the_file_and_the_report_names_it(self, tmp_path):
        """A hand ceremony reads the tree through `raw_tree`, which does not refuse a compiled file
        (`repin` does, for an ordinary one); the report is what tells the reader it is there."""
        repo, a, h = _make_range(
            tmp_path, {"bootstrap/tests/_oracle.py": "a = 1\n"}, {self._PYC: b"\x00compiled"})
        with P.raw_tree(h, repo=repo) as tree:
            assert (tree / self._PYC).read_bytes() == b"\x00compiled"
        assert (self._PYC, 0, "compiled-file") in _hits(_report(repo, a, h))

    def test_a_hostile_compiled_path_is_escaped(self, tmp_path):
        repo, a, h = _make_range(tmp_path, {"README.md": "x\n"},
                                 {"__pycache__/\x1b[31mx.pyc": b"x"})
        (path, _l, _n), = _hits(_report(repo, a, h))
        assert all(0x20 <= ord(c) < 0x7F for c in path) and "\x1b" not in path


class TestTheLineComparisonIsBounded:

    def test_a_file_past_the_limit_is_listed_and_every_new_line_is_scanned(self, tmp_path):
        filler = "x = 1\n" * (P._DIFF_MAX_LINES // 2 + 10)
        repo, a, h = _make_range(
            tmp_path, {"bootstrap/tests/_oracle.py": filler},
            {"bootstrap/tests/_oracle.py": filler + "import subprocess\n"})
        rep = _report(repo, a, h)
        assert _hits(rep) == [("bootstrap/tests/_oracle.py", P._DIFF_MAX_LINES // 2 + 11, "process-start")]
        assert {"path": "bootstrap/tests/_oracle.py",
                "reason": "too many lines to compare; every line scanned as added"} in rep["scan"]["listed"]

    def test_a_file_past_the_limit_cannot_hide_a_planted_line_among_moved_ones(self, tmp_path):
        """Counting every line as added means an unchanged line that matches a pattern is a hit
        too: more noise, never less."""
        filler = "x = 1\n" * (P._DIFF_MAX_LINES // 2 + 10)
        repo, a, h = _make_range(
            tmp_path, {"bootstrap/tests/_oracle.py": "import subprocess\n" + filler},
            {"bootstrap/tests/_oracle.py": "import subprocess\n" + filler + "y = 2\n"})
        assert [x[2] for x in _hits(_report(repo, a, h))] == ["process-start"]

    def test_a_large_near_identical_file_is_scanned_in_seconds(self, tmp_path):
        import time
        filler = "x = 1\n" * 60000
        repo, a, h = _make_range(
            tmp_path, {"bootstrap/tests/_oracle.py": filler},
            {"bootstrap/tests/_oracle.py": filler + "z = 3\n"})
        began = time.monotonic()
        _report(repo, a, h)
        assert time.monotonic() - began < 20

    def test_a_file_under_the_limit_is_still_compared_line_by_line_and_not_listed(self, tmp_path):
        repo, a, h = _make_range(
            tmp_path, {"bootstrap/tests/_oracle.py": "import subprocess\nx = 1\n"},
            {"bootstrap/tests/_oracle.py": "import subprocess\nx = 1\ny = 2\n"})
        rep = _report(repo, a, h)
        assert _hits(rep) == [] and rep["scan"]["listed"] == []


class TestAnchoredScanDigest:
    """The Maintainer compares the digest the page prints with the one the
    anchor's own checker prints. So the digest has to move when a candidate
    checker hides a hit, and the anchor's copy has to be the one that is run."""

    def _closure_files(self) -> dict:
        return {f"bootstrap/tests/{n}": (CAIRN_ROOT / "bootstrap/tests" / n)
                .read_bytes() for n in _CLOSURE_PY}

    def _extract(self, repo: Path, commit: str, dest: Path) -> Path:
        dest.mkdir()
        for n in _CLOSURE_PY:
            blob = subprocess.run(
                ["git", "-C", str(repo), "show", f"{commit}:bootstrap/tests/{n}"],
                capture_output=True, check=True).stdout
            (dest / n).write_bytes(blob)
        return dest / "_gate_preflight.py"

    def _digest_from(self, checker: Path, repo: Path, anchor: str,
                     head: str) -> str:
        env = {"PATH": os.environ.get("PATH", ""), "HOME": str(repo)}
        proc = subprocess.run(
            [sys.executable, "-E", "-s", str(checker), "scan-digest",
             "--repo", str(repo), "--anchor", anchor, "--candidate", head],
            capture_output=True, text=True, check=False, env=env)
        assert proc.returncode == 0, proc.stderr
        out = proc.stdout.strip()
        assert len(out) == 64 and all(c in "0123456789abcdef" for c in out), out
        return out

    def _candidate(self, tmp_path, *, hide: bool):
        base = self._closure_files()
        cand = dict(base)
        cand["scripts/repin.py"] = "import subprocess\n"   # the planted line
        if hide:
            guard = b'if __name__ == "__main__":'
            src = base["bootstrap/tests/_gate_preflight.py"]
            assert src.count(guard) == 1
            # rebind before main() runs, so the candidate's scan finds nothing
            cand["bootstrap/tests/_gate_preflight.py"] = src.replace(
                guard, b"SCAN_PATTERNS = ()\n" + guard)
        return _make_range(tmp_path, base, cand)

    def test_the_command_prints_the_digest_of_the_reports_scan(self, tmp_path):
        repo, a, h = self._candidate(tmp_path, hide=False)
        checker = self._extract(repo, a, tmp_path / "anchor-code")
        printed = self._digest_from(checker, repo, a, h)
        assert printed == P.scan_digest(_report(repo, a, h)["scan"])

    def test_with_nothing_hidden_the_anchors_digest_equals_the_candidates(
            self, tmp_path):
        repo, a, h = self._candidate(tmp_path, hide=False)
        anchor_code = self._extract(repo, a, tmp_path / "anchor-code")
        cand_code = self._extract(repo, h, tmp_path / "cand-code")
        assert (self._digest_from(anchor_code, repo, a, h)
                == self._digest_from(cand_code, repo, a, h))

    def test_a_candidate_checker_that_hides_a_hit_gives_an_unequal_digest(
            self, tmp_path):
        repo, a, h = self._candidate(tmp_path, hide=True)
        anchor_code = self._extract(repo, a, tmp_path / "anchor-code")
        cand_code = self._extract(repo, h, tmp_path / "cand-code")
        from_anchor = self._digest_from(anchor_code, repo, a, h)
        from_candidate = self._digest_from(cand_code, repo, a, h)
        assert from_anchor != from_candidate, (
            "the candidate's own scan must not be able to match the anchor's "
            "when it hides a hit")

    def test_the_report_says_whether_the_anchors_own_checker_made_the_scan(
            self, tmp_path):
        """The scan is the anchor's own when the running checker's bytes equal
        the anchor's copy; a range whose anchor holds a different checker says
        a candidate checker made it."""
        repo, a, h = self._candidate(tmp_path / "same", hide=False)
        assert _report(repo, a, h)["scan_checker"] == "anchor"
        files = self._closure_files()
        files["bootstrap/tests/_gate_preflight.py"] += b"\n# an older copy\n"
        repo2, a2, h2 = _make_range(tmp_path / "other", files,
                                    {"README.md": "x\n"})
        assert _report(repo2, a2, h2)["scan_checker"] == "candidate"


class TestRosterFingerprints:

    def test_each_fingerprint_equals_the_one_ssh_keygen_prints(self, tmp_path):
        keys = []
        for n in ("one", "two"):
            kp = tmp_path / n
            subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "",
                            "-f", str(kp), "-C", n], check=True,
                           capture_output=True)
            pub = (tmp_path / f"{n}.pub").read_text().split()
            lf = subprocess.run(["ssh-keygen", "-lf", f"{kp}.pub"], check=True,
                                capture_output=True, text=True).stdout.split()[1]
            keys.append((f"{n}@example", pub[0], pub[1], lf))
        old = "".join(f"{p} {t} {k}\n" for p, t, k, _ in keys[:1])
        new = old + f"{keys[1][0]} {keys[1][1]} {keys[1][2]}\n"
        repo, a, h = _make_range(tmp_path / "r",
                                 {"dev/.cairn/allowed_signers": old},
                                 {"dev/.cairn/allowed_signers": new})
        signers = _report(repo, a, h)["signers"]
        assert signers["anchor"] == [f"{keys[0][0]} ssh-ed25519 {keys[0][3]}"]
        assert signers["candidate"] == sorted(
            f"{p} ssh-ed25519 {fp}" for p, _t, _k, fp in keys)

    def test_an_unparseable_roster_line_is_shown_not_dropped(self, tmp_path):
        repo, a, h = _make_range(
            tmp_path, {"dev/.cairn/allowed_signers": "a@x ssh-ed25519 !!notbase64\n"},
            {"dev/.cairn/allowed_signers": "a@x ssh-ed25519 !!notbase64\n# c\n"})
        assert _report(repo, a, h)["signers"]["candidate"][0].startswith(
            "UNPARSEABLE")


class TestStageTwoReDerivation:

    def test_a_report_with_hits_rederives_to_the_same_digest(self, tmp_path):
        repo, a, h = _make_range(
            tmp_path, {"bootstrap/tests/_oracle.py": "a = 1\n"},
            {"bootstrap/tests/_oracle.py": "a = 1\nimport subprocess\n"})
        first = _report(repo, a, h)
        digest = P.range_report_digest(first)
        again = P.rederive_and_bind(
            a, h, branch="refs/heads/main", expected_old=h,
            confirmed_digest=digest, repo=repo, prospective_manifest=b"{}\n")
        assert P.range_report_digest(again) == digest
