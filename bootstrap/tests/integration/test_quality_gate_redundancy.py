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
    def test_low_overlap_pair_silent(self, qg, tmp_path):
        (tmp_path / "docs" / "methodology").mkdir(parents=True)
        (tmp_path / "docs" / "methodology" / "a.md").write_text(
            "Apple bread carrots dance elephant frogs green house ink "
            "jellyfish kindness ladybug mountain nighttime octopus pizza.\n"
        )
        (tmp_path / "docs" / "methodology" / "b.md").write_text(
            "Yesterday tomorrow zenith xylophone wreath vacuum unique "
            "treasure soldier rainbow quiet panther onyx neutral mystic.\n"
        )
        findings = qg._run_r1_redundancy(
            tmp_path, shingle_size=5, jaccard_threshold=0.75,
        )
        assert findings == []


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


    def test_dunder_methods_not_flagged(self, qg, tmp_path):
        (tmp_path / "scripts").mkdir()
        (tmp_path / "scripts" / "x.py").write_text(
            "class C:\n"
            "    def __init__(self): self.x = 1\n"
            "    def __repr__(self): return 'C'\n"
            "\n"
            "C()\n"
        )
        findings = qg._run_r6_redundancy(tmp_path)
        assert not any("__init__" in f.message for f in findings)
        assert not any("__repr__" in f.message for f in findings)

    def test_private_helper_is_info_not_fail(self, qg, tmp_path):
        # A private (_-prefixed) def without a static reference may
        # be referenced by tests we don't scan; we report it as info,
        # not fail, so the gate stays usable.
        (tmp_path / "scripts").mkdir()
        (tmp_path / "scripts" / "x.py").write_text(
            "def _private_helper():\n"
            "    return 1\n"
        )
        findings = qg._run_r6_redundancy(tmp_path)
        # Should appear at info severity, not fail.
        assert all(
            ("_private_helper" not in f.message) or f.severity == "info"
            for f in findings
        ), [(f.severity, f.message) for f in findings]

    def test_re_exported_def_not_flagged(self, qg, tmp_path):
        # A def whose ONLY in-corpus reference is a package-facade
        # re-export (`from .x import public_api` in the sibling
        # __init__.py) is live, not dead.  Before the ImportFrom
        # branch existed in `_collect_py_defs_and_refs`, the alias
        # nodes of an import were harvested by neither the ast.Name
        # nor the ast.Attribute case, so this shape produced a `fail`.
        (tmp_path / "scripts").mkdir()
        (tmp_path / "scripts" / "x.py").write_text(
            "def public_api():\n"
            "    return 1\n"
        )
        (tmp_path / "scripts" / "__init__.py").write_text(
            "from .x import public_api\n"
        )
        findings = qg._run_r6_redundancy(tmp_path)
        assert not any("public_api" in f.message for f in findings), [
            (f.severity, f.message) for f in findings
        ]

    def test_aliased_re_export_not_flagged(self, qg, tmp_path):
        # Same, with the `as` form -- the shape the engine facade
        # actually uses (`from ._guard import install as
        # _install_engine_guard`).  The def being matched is named by
        # the imported symbol, not by the local rebinding.
        (tmp_path / "scripts").mkdir()
        (tmp_path / "scripts" / "x.py").write_text(
            "def public_api():\n"
            "    return 1\n"
        )
        (tmp_path / "scripts" / "__init__.py").write_text(
            "from .x import public_api as _p\n"
        )
        findings = qg._run_r6_redundancy(tmp_path)
        assert not any("public_api" in f.message for f in findings), [
            (f.severity, f.message) for f in findings
        ]

    def test_import_does_not_silence_an_unreferenced_def(self, qg, tmp_path):
        # Negative control for the ONLY failure direction this
        # detector has: over-suppression.  Harvesting an import must
        # add the *imported symbol* name and nothing else.  Two defs
        # here are genuinely dead; each is named after one of the
        # import statement's other tokens, so a broader harvest goes
        # quiet on real dead code:
        #
        #   * `orphan_alias` collides with the local `as` binding --
        #     it would go silent if `alias.asname` were harvested too.
        #   * `mod_a` collides with the module name -- it would go
        #     silent if `node.module` were harvested too.
        #
        # `thing` is the only name the import legitimately references,
        # and there is no def by that name in the corpus.  The import
        # has no use site in its own file on purpose: that is the
        # facade re-export shape, and it also keeps `orphan_alias` out
        # of the reference set via the ast.Name path, so this test
        # isolates the import harvest.
        (tmp_path / "scripts").mkdir()
        (tmp_path / "scripts" / "x.py").write_text(
            "from mod_a import thing as orphan_alias\n"
        )
        (tmp_path / "scripts" / "y.py").write_text(
            "def orphan_alias():\n"
            "    return 1\n"
            "\n"
            "def mod_a():\n"
            "    return 2\n"
        )
        fails = _failures(qg._run_r6_redundancy(tmp_path))
        messages = [f.message for f in fails]
        assert any("`orphan_alias`" in m for m in messages), messages
        assert any("`mod_a`" in m for m in messages), messages
