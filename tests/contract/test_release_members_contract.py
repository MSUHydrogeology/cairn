"""File-level release evidence through real pytest XML and the public comparator.

Promises:
- The release comparator passes a complete report, and fails when a security-required test file is omitted even though pytest passed.
- A failing pytest run stays a failure even when the member comparison passes.
- An adopter-owned slow selection is independent of the required members.
- Refuses an existing report path, malformed or invalid required configuration, and an invalid start time.
- An empty security manifest is never a pass.
- Cairn's own run allows a skipped case only when the manifest's native-only list names that exact test for the other platform and the skip is a genuine pytest.skip; every required file still needs a passing case, and each refusal carries a stable identifier.
- An adopter-owned list stays strict and never reads the manifest.
Sources: release/check_release_test_members.py module docstring; release/RELEASE_PROCESS.md (the release sequence, around lines 115-148); tests/security_manifest.py (NATIVE_ONLY_NODE_IDS and NATIVE_ONLY_POLICY_ID).


Small isolated release-shaped fixtures do not run Cairn's certifying suite.
The independent manifest bytes and expected names come from the real tree.
"""
from __future__ import annotations

import ast
from collections import defaultdict
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from typing import NamedTuple
import xml.etree.ElementTree as ET

import pytest

from tests._repo_root import repository_root

ROOT = repository_root(Path(__file__))
SCRIPT = ROOT / "release/check_release_test_members.py"
DOC = ROOT / "release/RELEASE_PROCESS.md"
MANIFEST = ROOT / "tests/security_manifest.py"
VICTIM = "tests/test_security_lint.py"


@pytest.fixture
def project(tmp_path: Path) -> Path:
    tests = tmp_path / "tests"
    tests.mkdir(parents=True)
    scripts = tmp_path / "release"
    scripts.mkdir()
    shutil.copyfile(SCRIPT, scripts / SCRIPT.name)
    shutil.copyfile(MANIFEST, tests / MANIFEST.name)
    tree = ast.parse(MANIFEST.read_text(encoding="utf-8"))
    family = next(ast.literal_eval(node.value) for node in tree.body
                  if isinstance(node, ast.AnnAssign)
                  and isinstance(node.target, ast.Name)
                  and node.target.id == "SECURITY_FAMILY")
    for name in [*family, "test_security_marker.py"]:
        (tests / name).write_text("def test_pass():\n    assert True\n", encoding="utf-8")
    # The fixture preserves the release option, not the suite's shuffle engine.
    (tmp_path / "conftest.py").write_text(
        'def pytest_addoption(parser):\n'
        '    parser.addoption("--quality-gate-shuffle-seed")\n', encoding="utf-8")
    return tmp_path


def _env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("CAIRN_FULL_SUITE", None)
    env.pop("CAIRN_RELEASE_GATE_ACTIVE", None)
    env.pop("PYTEST_ADDOPTS", None)
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env.get("PATH", "")
    return env


def _sequence(root: Path, *, omit: str | None = None, adopter: bool = False,
              family: str = "xunit2", preexisting: bool = False) -> subprocess.CompletedProcess:
    block = re.search(r"```bash\n(\(\n.*?\n\))\n```", DOC.read_text(), re.S)
    assert block is not None
    command = block.group(1)
    assert "CAIRN_FULL_SUITE=1 python -m pytest tests --quality-gate-shuffle-seed=0" in command
    # Only a tiny fixture is executed. Never set the certification override.
    command = command.replace("CAIRN_FULL_SUITE=1 ", "")
    option = f"--quality-gate-shuffle-seed=0 -o junit_family={family}"
    if omit:
        option += f" --ignore={omit}"
    command = command.replace("--quality-gate-shuffle-seed=0", option)
    if adopter:
        command = command.replace("python release/check_release_test_members.py",
                                  "python release/check_release_test_members.py --required-files required.json")
    if preexisting:
        command = command.replace('report="$report_dir/pytest.xml"',
                                  'report="$report_dir/pytest.xml"\ntouch "$report"')
    return subprocess.run(["bash", "-c", command], cwd=root, env=_env(),
                          capture_output=True, text=True, timeout=30)


@pytest.mark.parametrize("family", ["xunit1", "xunit2"])
def test_actual_pytest_identities_and_documented_sequence(project: Path, family: str):
    result = _sequence(project, family=family)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "release membership: PASS: 15 required files" in result.stdout


@pytest.mark.parametrize("omit", [VICTIM, "tests/test_security_marker.py"])
def test_actual_security_omission_fails_after_pytest_passes(project: Path, omit: str):
    result = _sequence(project, omit=omit)
    assert result.returncode != 0
    assert "14 passed" in result.stdout
    assert omit in result.stderr


@pytest.mark.parametrize("omit", [False, True])
def test_adopter_owned_slow_selection_is_independent(project: Path, omit: bool):
    slow = "tests/test_slow.py"
    (project / slow).write_text("def test_slow():\n    assert True\n")
    (project / "required.json").write_text(json.dumps([slow]))
    result = _sequence(project, adopter=True, omit=slow if omit else None)
    assert "passed" in result.stdout
    assert (result.returncode != 0) is omit, result.stdout + result.stderr
    if omit:
        assert slow in result.stderr


def test_pytest_failure_is_preserved_even_if_comparison_passes(project: Path):
    (project / "tests/test_optional.py").write_text(
        "def test_optional():\n    assert False\n")
    result = _sequence(project)
    assert result.returncode == 1
    assert "release membership: PASS" in result.stdout
    assert "1 failed" in result.stdout


def test_documented_sequence_refuses_existing_report_path(project: Path):
    result = _sequence(project, preexisting=True)
    assert result.returncode != 0
    assert "passed" not in result.stdout
    assert "release membership" not in result.stdout + result.stderr


def _xml(*, classname: str = "tests.test_security_lint",
         name: str = "test_ok", outcome: str | None = None) -> ET.Element:
    suite = ET.Element("testsuite", tests="1", failures="0", errors="0", skipped="0")
    case = ET.SubElement(suite, "testcase", classname=classname, name=name)
    if outcome:
        ET.SubElement(case, outcome)
        suite.set({"failure": "failures", "error": "errors", "skipped": "skipped"}[outcome], "1")
    return suite


def _check(root: Path, report: Path, start: int, *, configured: bool = True):
    args = [sys.executable, str(root / "release" / SCRIPT.name), str(report),
            "--started-ns", str(start)]
    if configured:
        args += ["--required-files", str(root / "required.json")]
    return subprocess.run(args, cwd=root, env=_env(), capture_output=True,
                          text=True, timeout=10)


@pytest.fixture
def evidence(project: Path):
    report = project / "report.xml"
    (project / "required.json").write_text(json.dumps([VICTIM]))
    start = time.time_ns()
    ET.ElementTree(_xml()).write(report, encoding="utf-8")
    return project, report, start


def test_minimal_report_passes(evidence):
    root, report, start = evidence
    assert _check(root, report, start).returncode == 0


@pytest.mark.parametrize("fault", [
    "absent", "stale", "future", "malformed", "dtd", "utf16", "symlink", "oversized",
    "empty", "counts", "duplicate", "two-suites", "unknown-class", "ambiguous-class",
    "file-disagrees", "missing-name", "nested-case", "two-outcomes", "no-success",
    "skipped", "failure", "error", "missing-source",
])
def test_report_refusals(evidence, fault: str):
    root, report, start = evidence
    suite = _xml()
    case = suite.find("testcase")
    assert case is not None
    if fault == "absent":
        report.unlink()
    elif fault in {"stale", "future"}:
        stamp = start - 1 if fault == "stale" else time.time_ns() + 10**12
        os.utime(report, ns=(stamp, stamp))
    elif fault == "malformed":
        report.write_text("<broken")
    elif fault == "dtd":
        report.write_text('<!DOCTYPE x [<!ENTITY x "boom">]><testsuite/>')
    elif fault == "utf16":
        report.write_bytes(ET.tostring(suite, encoding="utf-16"))
    elif fault == "symlink":
        target = report.with_name("target.xml")
        report.rename(target)
        report.symlink_to(target)
    elif fault == "oversized":
        with report.open("wb") as handle:
            handle.truncate(32 * 1024 * 1024 + 1)
    elif fault == "missing-source":
        (root / VICTIM).unlink()
    else:
        if fault == "empty":
            suite.remove(case)
            suite.set("tests", "0")
        elif fault == "counts":
            suite.set("tests", "9")
        elif fault == "duplicate":
            suite.append(ET.fromstring(ET.tostring(case)))
            suite.set("tests", "2")
        elif fault == "two-suites":
            container = ET.Element("testsuites")
            container.extend([suite, ET.fromstring(ET.tostring(suite))])
            suite = container
        elif fault == "unknown-class":
            case.set("classname", "not.a.source.file")
        elif fault == "ambiguous-class":
            (root / "tests.test_security_lint.py").write_text("")
        elif fault == "file-disagrees":
            case.set("file", "tests/test_security_marker.py")
        elif fault == "missing-name":
            case.attrib.pop("name")
        elif fault == "nested-case":
            ET.SubElement(case, "testcase")
        elif fault == "two-outcomes":
            ET.SubElement(case, "skipped")
            ET.SubElement(case, "failure")
        elif fault == "no-success":
            case.set("classname", "tests.test_security_marker")
        else:
            suite = _xml(outcome=fault)
        ET.ElementTree(suite).write(report, encoding="utf-8")
    result = _check(root, report, start)
    assert result.returncode != 0, fault
    assert "FAIL" in result.stderr


@pytest.mark.parametrize("value", [None, [], {}, [VICTIM, VICTIM], ["../outside.py"],
                                       ["missing.py"], [123], "wrong-type"])
def test_invalid_required_configuration_fails(evidence, value):
    root, report, start = evidence
    config = root / "required.json"
    if value is None:
        config.unlink()
    else:
        config.write_text(json.dumps(value))
    assert _check(root, report, start).returncode != 0


def test_malformed_required_configuration_fails(evidence):
    root, report, start = evidence
    (root / "required.json").write_text("[")
    assert _check(root, report, start).returncode != 0


def test_invalid_start_time_fails(evidence):
    root, report, _start = evidence
    for start in [0, -1, time.time_ns() + 10**12]:
        assert _check(root, report, start).returncode != 0


def test_empty_security_manifest_is_not_a_pass(evidence):
    root, report, start = evidence
    (root / "tests/security_manifest.py").write_text("SECURITY_FAMILY: dict = {}")
    assert _check(root, report, start, configured=False).returncode != 0


# --- Cairn's own run: a skip the native-only list names for the other platform ---
#
# The fixtures below use a small policy of their own, with a digest computed the
# way tests/security_manifest.py computes it, so each test can break exactly one
# thing. The checker reads the policy as literals and never imports the file.
# Refusals are told apart by the stable identifier in square brackets at the end
# of the failure line, never by wording.

ALPHA = "tests/test_alpha.py"
BETA = "tests/test_beta.py"
MARKER = "tests/test_security_marker.py"
REQUIRED = [ALPHA, BETA, MARKER]
NATIVE = {
    "nt": [f"{ALPHA}::test_win_one", f"{ALPHA}::test_win_two",
           f"{BETA}::TestNative::test_win[a-b]"],
    "posix": [f"{ALPHA}::test_posix_one", f"{ALPHA}::test_posix_two",
              f"{BETA}::TestNative::test_posix[a-b]"],
}
POLICY_ROWS = tuple((host, node) for host in ("nt", "posix") for node in NATIVE[host])
HOSTS = ["nt", "posix"]


def _other(host: str) -> str:
    return "posix" if host == "nt" else "nt"


def _digest(rows) -> str:
    try:
        canonical = "".join(f"{host}\t{node}\n" for host, node in rows)
        return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    except (TypeError, ValueError):
        return _digest(POLICY_ROWS)


def _manifest_text(rows=POLICY_ROWS, *, rows_source: str | None = None,
                   digest_source: str | None = None, extra: str = "") -> str:
    """A small manifest. ``rows_source``/``digest_source`` replace the literal text."""
    lines = ["SECURITY_FAMILY: dict = {'test_alpha.py': 1, 'test_beta.py': 2}"]
    if rows_source != "absent":
        lines.append("NATIVE_ONLY_NODE_IDS: tuple = "
                     + (rows_source if rows_source is not None else repr(tuple(rows))))
    if digest_source != "absent":
        lines.append("NATIVE_ONLY_POLICY_ID = "
                     + (digest_source if digest_source is not None else repr(_digest(rows))))
    return "\n".join(lines) + "\n" + extra


def _native_project(tmp_path: Path, manifest: str | None = None) -> Path:
    (tmp_path / "tests").mkdir(parents=True)
    (tmp_path / "release").mkdir()
    shutil.copyfile(SCRIPT, tmp_path / "release" / SCRIPT.name)
    for path in REQUIRED:
        (tmp_path / path).write_text("def test_pass():\n    assert True\n", encoding="utf-8")
    (tmp_path / "tests/security_manifest.py").write_text(
        _manifest_text() if manifest is None else manifest, encoding="utf-8")
    return tmp_path


Case = tuple[str, str, str | None, str | None]


def _identity(node: str) -> tuple[str, str]:
    """The (classname, name) pytest writes into its JUnit report for a node ID."""
    head, bracket, label = node.partition("[")
    path, *classes, leaf = head.split("::")
    classname = ".".join([path.removesuffix(".py").replace("/", "."), *classes])
    return classname, leaf + bracket + label


def _ok(node: str) -> Case:
    return (*_identity(node), None, None)


def _skip(node: str, kind: str | None = "pytest.skip", outcome: str = "skipped") -> Case:
    return (*_identity(node), outcome, kind)


def _passes(omit: tuple[str, ...] = ()) -> list[Case]:
    return [_ok(f"{path}::test_pass") for path in REQUIRED if path not in omit]


def _report(root: Path, cases: list[Case]) -> tuple[Path, int]:
    start = time.time_ns()
    suite = ET.Element("testsuite", name="pytest")
    counts = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
    for classname, name, outcome, kind in cases:
        case = ET.SubElement(suite, "testcase", classname=classname, name=name)
        counts["tests"] += 1
        if outcome:
            child = ET.SubElement(case, outcome)
            if kind is not None:
                child.set("type", kind)
            counts[{"failure": "failures", "error": "errors", "skipped": "skipped"}[outcome]] += 1
    suite.attrib.update({key: str(value) for key, value in counts.items()})
    report = root / "native-report.xml"
    ET.ElementTree(suite).write(report, encoding="utf-8")
    # The checker refuses a report older than the run's start. Windows stamps a new
    # file from a coarse clock that can read earlier than time.time_ns(), so stamp it.
    stamp = time.time_ns()
    os.utime(report, ns=(stamp, stamp))
    return report, start


class Verdict(NamedTuple):
    status: int
    stdout: str
    stderr: str

    @property
    def code(self) -> str | None:
        found = re.search(r"\[([a-z][a-z0-9-]*)\]\s*\Z", self.stderr)
        return found.group(1) if found else None


def _load_checker(root: Path):
    spec = importlib.util.spec_from_file_location(
        "cairn_release_members_under_test", root / "release" / SCRIPT.name)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def judge(monkeypatch, capsys):
    """Run the checker's public entry. A named host is simulated in process by
    replacing the checker's private host helper (no command option exists for
    it); host=None runs the real command on the real host. A rename of the
    helper is caught by the acceptance tests, which fail for lack of the swap."""
    def run(root: Path, report: Path, start: int, *, host: str | None = None,
            configured: bool = False) -> Verdict:
        if host is None:
            result = _check(root, report, start, configured=configured)
            return Verdict(result.returncode, result.stdout, result.stderr)
        module = _load_checker(root)
        monkeypatch.setattr(module, "_host_tag", lambda: host, raising=False)
        argv = [str(report), "--started-ns", str(start), "--root", str(root)]
        if configured:
            argv += ["--required-files", str(root / "required.json")]
        status = module.main(argv)
        captured = capsys.readouterr()
        return Verdict(status, captured.out, captured.err)
    return run


def _refused(verdict: Verdict, code: str) -> None:
    assert verdict.status != 0, verdict.stdout
    assert verdict.code == code, verdict.stderr


@pytest.mark.parametrize("host", HOSTS)
def test_exact_other_platform_skips_beside_a_pass_are_accepted(tmp_path, judge, host):
    root = _native_project(tmp_path)
    cases = [*_passes(), *(_skip(node) for node in NATIVE[_other(host)])]
    report, start = _report(root, cases)
    verdict = judge(root, report, start, host=host)
    assert verdict.status == 0, verdict.stderr


@pytest.mark.parametrize("host", [None, "nt", "posix"])
def test_real_manifest_accepts_its_own_other_platform_skips(project, judge, host):
    """The real tree's policy and digest are accepted, on the real host and both simulated."""
    tree = ast.parse(MANIFEST.read_text(encoding="utf-8"))
    family = next(ast.literal_eval(node.value) for node in tree.body
                  if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)
                  and node.target.id == "SECURITY_FAMILY")
    rows = next(ast.literal_eval(node.value) for node in tree.body
                if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)
                and node.target.id == "NATIVE_ONLY_NODE_IDS")
    required = {"tests/" + name for name in family} | {MARKER}
    actual = host or ("nt" if os.name == "nt" else "posix")
    by_file: dict[str, list[str]] = defaultdict(list)
    for tag, node in rows:
        if tag == _other(actual) and node.split("::")[0] in required:
            by_file[node.split("::")[0]].append(node)
    pairs = [nodes for nodes in by_file.values() if len(nodes) >= 2]
    assert pairs, "the real policy names no two other-platform tests in one required file"
    cases = [*(_ok(f"{path}::test_pass") for path in sorted(required)),
             *(_skip(node) for node in pairs[0][:2])]
    report, start = _report(project, cases)
    verdict = judge(project, report, start, host=host)
    assert verdict.status == 0, verdict.stderr


@pytest.mark.parametrize("host", HOSTS)
def test_listed_skips_never_stand_in_for_a_passing_case(tmp_path, judge, host):
    root = _native_project(tmp_path)
    skips = [_skip(node) for node in NATIVE[_other(host)] if node.startswith(ALPHA)]
    assert len(skips) == 2
    report, start = _report(root, [*_passes(omit=(ALPHA,)), *skips])
    _refused(judge(root, report, start, host=host), "required-file-no-pass")


@pytest.mark.parametrize("host", HOSTS)
def test_a_skip_on_the_listed_platform_itself_refuses(tmp_path, judge, host):
    root = _native_project(tmp_path)
    report, start = _report(root, [*_passes(), _skip(NATIVE[host][0])])
    _refused(judge(root, report, start, host=host), "skip-same-platform")


@pytest.mark.parametrize("node", [
    f"{ALPHA}::test_unlisted",
    f"{BETA}::TestNative::test_unlisted[a-b]",
    f"{MARKER}::test_win_one",
])
def test_an_unlisted_skip_refuses(tmp_path, judge, node):
    root = _native_project(tmp_path)
    report, start = _report(root, [*_passes(), _skip(node)])
    _refused(judge(root, report, start, host="posix"), "skip-unlisted")


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("kind", ["pytest.xfail", None, "", "pytest.skipped"])
def test_a_skip_that_is_not_a_genuine_pytest_skip_refuses(tmp_path, judge, host, kind):
    root = _native_project(tmp_path)
    report, start = _report(root, [*_passes(), _skip(NATIVE[_other(host)][0], kind=kind)])
    _refused(judge(root, report, start, host=host), "skip-not-genuine")


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("outcome", ["failure", "error"])
def test_a_listed_node_that_fails_or_errors_refuses(tmp_path, judge, host, outcome):
    root = _native_project(tmp_path)
    report, start = _report(
        root, [*_passes(), _skip(NATIVE[_other(host)][0], kind=None, outcome=outcome)])
    _refused(judge(root, report, start, host=host), "required-case-failed")


def test_two_cases_for_one_native_node_refuse(tmp_path, judge):
    node = NATIVE["nt"][2]
    classname, name = _identity(node)
    assert classname == "tests.test_beta.TestNative"
    root = _native_project(tmp_path)
    first = (classname, name, "skipped", "pytest.skip")
    report, start = _report(root, [*_passes(), first])
    assert judge(root, report, start, host="posix").status == 0
    # Same node, spelled with a different class/name split.
    twin = ("tests.test_beta", "TestNative::" + name, "skipped", "pytest.skip")
    report, start = _report(root, [*_passes(), first, twin])
    _refused(judge(root, report, start, host="posix"), "identity-ambiguous")


MISLABELS = {
    "wrong-class": lambda classname, name: (classname.rsplit(".", 1)[0] + ".TestOther", name),
    "no-class": lambda classname, name: (classname.rsplit(".", 1)[0], name),
    "extra-class": lambda classname, name: (classname + ".TestInner", name),
    "wrong-label": lambda classname, name: (classname, name.replace("a-b", "a-c")),
    "no-label": lambda classname, name: (classname, name.split("[")[0]),
    "extra-label": lambda classname, name: (classname, name + "[x]"),
    "wrong-file": lambda classname, name: (classname.replace("test_beta", "test_alpha"), name),
    "wrong-name": lambda classname, name: (classname, name.replace("test_", "test_x", 1)),
}


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("label", sorted(MISLABELS))
def test_a_mislabelled_identity_is_not_the_listed_node(tmp_path, judge, host, label):
    node = NATIVE[_other(host)][2]
    assert "TestNative" in node and node.endswith("[a-b]")
    classname, name = MISLABELS[label](*_identity(node))
    assert (classname, name) != _identity(node)
    root = _native_project(tmp_path)
    report, start = _report(root, [*_passes(), (classname, name, "skipped", "pytest.skip")])
    _refused(judge(root, report, start, host=host), "skip-unlisted")


def _with_rows(*extra, first=None):
    rows = POLICY_ROWS if first is None else (first, *POLICY_ROWS[1:])
    return tuple(rows) + extra


BAD_ROWS = {
    "row-not-a-pair": _with_rows(("nt", f"{ALPHA}::test_x", "extra")),
    "row-not-a-tuple": _with_rows(["nt", f"{ALPHA}::test_x"]),
    "unknown-host": _with_rows(first=("linux", NATIVE["nt"][0])),
    "host-not-a-string": _with_rows(first=(7, NATIVE["nt"][0])),
    "node-not-a-string": _with_rows(("nt", 7)),
    "empty-node": _with_rows(("nt", "")),
    "non-ascii-node": _with_rows(("nt", f"{ALPHA}::test_é")),
    "newline-node": _with_rows(("nt", f"{ALPHA}::test_x\ntest_y")),
    "duplicate-node": _with_rows(POLICY_ROWS[0]),
    "node-on-both-hosts": _with_rows(("posix", NATIVE["nt"][0])),
    "node-without-a-case": _with_rows(("nt", ALPHA)),
    "node-without-a-python-file": _with_rows(("nt", "tests/test_alpha::test_x")),
    "node-outside-the-project": _with_rows(("nt", "../escape.py::test_x")),
    "node-with-a-backslash": _with_rows(("nt", "tests\\test_alpha.py::test_x")),
    "node-with-an-absolute-file": _with_rows(("nt", "/tests/test_alpha.py::test_x")),
    "node-with-a-noncanonical-file": _with_rows(("nt", "tests//test_alpha.py::test_x")),
    "node-with-an-empty-case": _with_rows(("nt", f"{ALPHA}::")),
}
BAD_MANIFESTS = {
    **{name: _manifest_text(rows) for name, rows in BAD_ROWS.items()},
    "not-a-tuple": _manifest_text(rows_source=repr(list(POLICY_ROWS))),
    "not-a-literal": _manifest_text(rows_source="tuple(())"),
    "policy-absent": _manifest_text(rows_source="absent", digest_source="absent"),
    "nodes-absent": _manifest_text(rows_source="absent"),
    "digest-absent": _manifest_text(digest_source="absent"),
    "digest-not-a-string": _manifest_text(digest_source="7"),
    "not-at-module-level": (
        "SECURITY_FAMILY: dict = {'test_alpha.py': 1, 'test_beta.py': 2}\n"
        f"if True:\n    NATIVE_ONLY_NODE_IDS: tuple = {POLICY_ROWS!r}\n"
        f"NATIVE_ONLY_POLICY_ID = {_digest(POLICY_ROWS)!r}\n"),
}
BAD_DIGESTS = {
    "stale": _manifest_text(digest_source=repr(_digest(POLICY_ROWS[:-1]))),
    "edited-node": _manifest_text(
        _with_rows(first=("nt", f"{ALPHA}::test_edited")),
        digest_source=repr(_digest(POLICY_ROWS))),
    "added-waiver": _manifest_text(
        _with_rows(("nt", f"{ALPHA}::test_added")), digest_source=repr(_digest(POLICY_ROWS))),
    "all-zero": _manifest_text(digest_source=repr("sha256:" + "0" * 64)),
    "bare-hex": _manifest_text(digest_source=repr(_digest(POLICY_ROWS).split(":", 1)[1])),
}
COMPETING = {
    "second-annotated-list": "NATIVE_ONLY_NODE_IDS: tuple = ()\n",
    "plain-rebinding": "NATIVE_ONLY_NODE_IDS = ()\n",
    "augmented": "NATIVE_ONLY_NODE_IDS += (('nt', 'tests/test_alpha.py::test_added'),)\n",
    "second-digest": f"NATIVE_ONLY_POLICY_ID = {_digest(())!r}\n",
    "conditional": "if True:\n    NATIVE_ONLY_NODE_IDS = ()\n",
    "walrus": "(NATIVE_ONLY_NODE_IDS := ())\n",
    "deleted": "del NATIVE_ONLY_NODE_IDS\n",
    "loop-target": "for NATIVE_ONLY_NODE_IDS in ():\n    pass\n",
    "imported": "from elsewhere import NATIVE_ONLY_NODE_IDS\n",
    "aliased-import": "import elsewhere as NATIVE_ONLY_NODE_IDS\n",
    "star-import": "from elsewhere import *\n",
    "function": "def NATIVE_ONLY_NODE_IDS():\n    pass\n",
    "class": "class NATIVE_ONLY_POLICY_ID:\n    pass\n",
    "global-statement": "def _f():\n    global NATIVE_ONLY_NODE_IDS\n",
    "exception-name": "try:\n    pass\nexcept Exception as NATIVE_ONLY_POLICY_ID:\n    pass\n",
    "match-capture": "match 1:\n    case NATIVE_ONLY_NODE_IDS:\n        pass\n",
}


def _accepting_report(root: Path, host: str = "posix") -> tuple[Path, int]:
    return _report(root, [*_passes(), *(_skip(node) for node in NATIVE[_other(host)])])


def test_the_fixture_policy_is_accepted_before_it_is_broken(tmp_path, judge):
    root = _native_project(tmp_path)
    report, start = _accepting_report(root)
    assert judge(root, report, start, host="posix").status == 0


@pytest.mark.parametrize("fault", sorted(BAD_MANIFESTS))
def test_a_malformed_policy_refuses(tmp_path, judge, fault):
    root = _native_project(tmp_path, BAD_MANIFESTS[fault])
    report, start = _accepting_report(root)
    _refused(judge(root, report, start, host="posix"), "policy-malformed")


def test_a_malformed_policy_refuses_even_when_the_report_has_no_skip(tmp_path, judge):
    root = _native_project(tmp_path, BAD_MANIFESTS["unknown-host"])
    report, start = _report(root, _passes())
    _refused(judge(root, report, start, host="posix"), "policy-malformed")


@pytest.mark.parametrize("fault", sorted(BAD_DIGESTS))
def test_a_policy_whose_digest_does_not_match_refuses(tmp_path, judge, fault):
    root = _native_project(tmp_path, BAD_DIGESTS[fault])
    report, start = _accepting_report(root)
    _refused(judge(root, report, start, host="posix"), "policy-digest-mismatch")


@pytest.mark.parametrize("fault", sorted(COMPETING))
def test_competing_bindings_of_the_policy_refuse(tmp_path, judge, fault):
    root = _native_project(tmp_path, _manifest_text(extra=COMPETING[fault]))
    report, start = _accepting_report(root)
    _refused(judge(root, report, start, host="posix"), "policy-bindings-competing")


@pytest.mark.parametrize("host", HOSTS)
def test_an_adopter_owned_list_still_refuses_any_skip(tmp_path, judge, host):
    root = _native_project(tmp_path)
    (root / "required.json").write_text(json.dumps([ALPHA]))
    report, start = _report(root, [_ok(f"{ALPHA}::test_pass"), _skip(NATIVE[_other(host)][0])])
    _refused(judge(root, report, start, host=host, configured=True), "required-case-skipped")


@pytest.mark.parametrize("manifest", [None, "NATIVE_ONLY_NODE_IDS = (", BAD_MANIFESTS["unknown-host"]])
def test_an_adopter_owned_list_never_reads_the_manifest(tmp_path, judge, manifest):
    root = _native_project(tmp_path, manifest or None)
    if manifest is None:
        (root / "tests/security_manifest.py").unlink()
    (root / "required.json").write_text(json.dumps([ALPHA]))
    report, start = _report(root, [_ok(f"{ALPHA}::test_pass")])
    assert judge(root, report, start, host="posix", configured=True).status == 0
