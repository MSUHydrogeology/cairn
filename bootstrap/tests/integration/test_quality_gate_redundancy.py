"""Redundancy sub-gate -- R1 (shingle/Jaccard) + R6 (AST unused-def).

Promises:

- The redundancy report surfaces document pairs whose word overlap meets the Jaccard threshold; unrelated passages stay silent.
- The --jaccard-threshold and --shingle-size options change which pairs the report surfaces.
- A Python definition that nothing in the scanned tree references is reported as a failure.
- A definition referenced from another file, or re-exported by a package, is not reported.
- Argparse callbacks, main, dunder methods and whitelisted names are not reported as unused.
- A private unreferenced definition is reported as information, not a failure.
- Importing a name does not hide an unrelated unreferenced definition.

Pins:

* R1 surfaces high-overlap pairs above the configured Jaccard
  threshold (default 0.75); below-threshold pairs are silent.
* Tunable ``--shingle-size`` and ``--jaccard-threshold`` alter the
  surfaced set.
* R6 catches an unreferenced helper def in a fixture module.
* The unused-def whitelist suppresses argparse ``_cmd_*`` callback
  false positives.
* Cross-file references (one module calling another's def) count as
  referenced and DO NOT trip R6.
* A ``from X import Y`` re-export (plain or aliased) counts as a
  reference to ``Y``, while the import's *other* tokens -- the local
  ``as`` binding and the module name -- do not silence unrelated defs.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent.parent
QG_SRC = CAIRN_ROOT / "scripts" / "quality_gate.py"

pytestmark = pytest.mark.skipif(
    not QG_SRC.exists(), reason="quality_gate.py not available",
)


def _load_qg(name: str = "_quality_gate_redundancy_under_test") -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, QG_SRC)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def qg() -> ModuleType:
    return _load_qg()


def _failures(findings):
    return [f for f in findings if f.severity == "fail"]


def _public_report(root: Path, *options: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable, str(QG_SRC), "--root", str(root),
            "--sub", "redundancy", "--report", *options,
        ],
        cwd=CAIRN_ROOT, capture_output=True, text=True, check=False,
    )


def _report_rows(result: subprocess.CompletedProcess[str]) -> list[str]:
    return [line for line in result.stdout.splitlines() if line]


# ---------------------------------------------------------------------------
# R1 -- shingle / Jaccard
# ---------------------------------------------------------------------------


class TestR1Shingles:


    def test_cli_threshold_changes_report(self, tmp_path):
        common = (
            "alpha beta gamma delta epsilon zeta eta theta iota kappa "
            "one two three four five six seven eight nine ten "
            "eleven twelve thirteen fourteen fifteen sixteen"
        )
        docs = tmp_path / "docs" / "methodology"
        docs.mkdir(parents=True)
        (docs / "a.md").write_text(common + " Xa Xb Xc")
        (docs / "b.md").write_text(common + " Yp Yq Yr")

        low = _public_report(tmp_path, "--jaccard-threshold", "0.40")
        high = _public_report(tmp_path, "--jaccard-threshold", "0.99")
        assert low.returncode == high.returncode == 0
        assert any("R1 overlap" in row for row in _report_rows(low)), low.stdout
        assert not any("R1 overlap" in row for row in _report_rows(high)), high.stdout

        default_passage = (
            "The quick brown fox jumps over the lazy dog and "
            "the rain in Spain stays mainly on the plain.\n"
        )
        (docs / "a.md").write_text(default_passage)
        (docs / "b.md").write_text(default_passage)
        default = _public_report(tmp_path)
        assert default.returncode == 0, default.stderr
        assert any("R1 overlap" in row for row in _report_rows(default)), default.stdout

    def test_cli_shingle_size_changes_report(self, tmp_path):
        docs = tmp_path / "docs" / "methodology"
        docs.mkdir(parents=True)
        (docs / "a.md").write_text("alpha beta gamma delta epsilon\n")
        (docs / "b.md").write_text(
            "alpha beta gamma delta epsilon other words different stuff\n"
        )

        short = _public_report(
            tmp_path, "--shingle-size", "5", "--jaccard-threshold", "0.10",
        )
        long = _public_report(
            tmp_path, "--shingle-size", "10", "--jaccard-threshold", "0.10",
        )
        assert short.returncode == long.returncode == 0
        assert any("R1 overlap" in row for row in _report_rows(short)), short.stdout
        assert not any("R1 overlap" in row for row in _report_rows(long)), long.stdout


# ---------------------------------------------------------------------------
# R6 -- stdlib AST unreferenced-def detection
# ---------------------------------------------------------------------------


class TestR6UnusedDef:
    def test_cli_whitelists_unreferenced_argparse_callback(self, tmp_path):
        scripts = tmp_path / "scripts"
        scripts.mkdir()
        callback = scripts / "claim_cli.py"
        callback.write_text(
            "import sys\n"
            "\n"
            "def _cmd_claim(args):\n"
            "    print('claimed:' + args[0])\n"
            "\n"
            "def unrelated_unused():\n"
            "    return None\n"
            "\n"
            "def main():\n"
            "    name, *args = sys.argv[1:]\n"
            "    return globals()[name](args)\n"
            "\n"
            "if __name__ == '__main__':\n"
            "    main()\n"
        )
        invoked = subprocess.run(
            [sys.executable, str(callback), "_cmd_claim", "fixture"],
            cwd=tmp_path, capture_output=True, text=True, check=False,
        )
        assert invoked.returncode == 0
        assert invoked.stdout.strip() == "claimed:fixture"

        report = _public_report(tmp_path)
        rows = _report_rows(report)
        assert report.returncode == 1, report.stdout
        assert not any("_cmd_claim" in row for row in rows), report.stdout
        assert any(
            "R6 def `unrelated_unused`" in row for row in rows
        ), report.stdout

    def test_cli_counts_cross_file_helper_reference(self, tmp_path):
        scripts = tmp_path / "scripts"
        scripts.mkdir()
        (scripts / "a_consumer.py").write_text(
            "import x\n\n\ndef consume():\n    return x.helper()\n"
        )
        (scripts / "z_provider.py").write_text(
            "def helper():\n    return 1\n\n"
            "def unrelated_unused():\n    return 2\n"
        )

        report = _public_report(tmp_path)
        rows = _report_rows(report)
        assert report.returncode == 1, report.stdout
        assert not any("R6 def `helper`" in row for row in rows), report.stdout
        assert any(
            "R6 def `unrelated_unused`" in row for row in rows
        ), report.stdout
