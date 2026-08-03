"""Redundancy sub-gate -- R1 (shingle/Jaccard) + R6 (AST unused-def).

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
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
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


def _infos(findings):
    return [f for f in findings if f.severity == "info"]


# ---------------------------------------------------------------------------
# R1 -- shingle / Jaccard
# ---------------------------------------------------------------------------


class TestR1Shingles:
    def test_high_overlap_pair_surfaces(self, qg, tmp_path):
        passage = (
            "The quick brown fox jumps over the lazy dog and "
            "the rain in Spain stays mainly on the plain.\n"
        )
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "a.md").write_text(passage)
        (tmp_path / "doctrine" / "b.md").write_text(passage)
        findings = qg._run_r1_redundancy(
            tmp_path, shingle_size=5, jaccard_threshold=0.75,
        )
        assert any("R1 overlap" in f.message for f in findings), findings

    def test_low_overlap_pair_silent(self, qg, tmp_path):
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "a.md").write_text(
            "Apple bread carrots dance elephant frogs green house ink "
            "jellyfish kindness ladybug mountain nighttime octopus pizza.\n"
        )
        (tmp_path / "doctrine" / "b.md").write_text(
            "Yesterday tomorrow zenith xylophone wreath vacuum unique "
            "treasure soldier rainbow quiet panther onyx neutral mystic.\n"
        )
        findings = qg._run_r1_redundancy(
            tmp_path, shingle_size=5, jaccard_threshold=0.75,
        )
        assert findings == []

    def test_threshold_makes_overlap_visible_or_not(self, qg, tmp_path):
        # Two passages sharing a long common prefix + short different
        # suffixes.  At a low Jaccard threshold the pair surfaces; at
        # a high threshold it does not.  Threshold values picked to
        # bracket the actual computed Jaccard, which depends on the
        # ratio of common shingles to (common + 2*diff) shingles.
        common = (
            "alpha beta gamma delta epsilon zeta eta theta iota kappa "
            "one two three four five six seven eight nine ten "
            "eleven twelve thirteen fourteen fifteen sixteen"
        )
        diff_a = "Xa Xb Xc"
        diff_b = "Yp Yq Yr"
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "a.md").write_text(common + " " + diff_a)
        (tmp_path / "doctrine" / "b.md").write_text(common + " " + diff_b)
        low_t = qg._run_r1_redundancy(
            tmp_path, shingle_size=5, jaccard_threshold=0.40,
        )
        hi_t = qg._run_r1_redundancy(
            tmp_path, shingle_size=5, jaccard_threshold=0.99,
        )
        assert low_t != [] and hi_t == [], (low_t, hi_t)

    def test_shingle_size_change_alters_set(self, qg, tmp_path):
        # Two passages sharing one 5-shingle (visible at size=5) but
        # nothing at size=10.
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "a.md").write_text(
            "alpha beta gamma delta epsilon\n"
        )
        (tmp_path / "doctrine" / "b.md").write_text(
            "alpha beta gamma delta epsilon other words different stuff\n"
        )
        size5 = qg._run_r1_redundancy(
            tmp_path, shingle_size=5, jaccard_threshold=0.10,
        )
        size10 = qg._run_r1_redundancy(
            tmp_path, shingle_size=10, jaccard_threshold=0.10,
        )
        assert size5 != [] and size10 == [], (size5, size10)


# ---------------------------------------------------------------------------
# R6 -- stdlib AST unreferenced-def detection
# ---------------------------------------------------------------------------


class TestR6UnusedDef:
    def test_unreferenced_def_surfaces(self, qg, tmp_path):
        (tmp_path / "scripts").mkdir()
        (tmp_path / "scripts" / "x.py").write_text(
            "def used():\n"
            "    return 1\n"
            "\n"
            "def never_referenced_anywhere():\n"
            "    return 2\n"
            "\n"
            "if True:\n"
            "    used()\n"
        )
        findings = qg._run_r6_redundancy(tmp_path)
        # The "_" prefix would soften severity; this name has no
        # underscore so it should be a fail finding.
        fails = _failures(findings)
        assert any(
            "never_referenced_anywhere" in f.message for f in fails
        ), [f.message for f in fails]

    def test_referenced_def_silent(self, qg, tmp_path):
        # All top-level defs need a reference SOMEWHERE in the scanned
        # corpus to stay silent.  `consumer` calls `helper`; `main`
        # (whitelisted) calls `consumer` -- so both names appear as
        # references and neither flags.
        (tmp_path / "scripts").mkdir()
        (tmp_path / "scripts" / "x.py").write_text(
            "def helper():\n"
            "    return 1\n"
            "\n"
            "def consumer():\n"
            "    return helper()\n"
            "\n"
            "def main():\n"
            "    return consumer()\n"
        )
        findings = qg._run_r6_redundancy(tmp_path)
        assert findings == [], [f.message for f in findings]

    def test_whitelist_suppresses_argparse_callback(self, qg, tmp_path):
        # An argparse `_cmd_*` callback is in the whitelist and must
        # NOT surface even when no static reference exists.
        (tmp_path / "scripts").mkdir()
        (tmp_path / "scripts" / "x.py").write_text(
            "import argparse\n"
            "\n"
            "def _cmd_claim(args):\n"
            "    return 0\n"
            "\n"
            "def main():\n"
            "    p = argparse.ArgumentParser()\n"
            "    sp = p.add_subparsers()\n"
            "    claim = sp.add_parser('claim')\n"
            "    claim.set_defaults(func=_cmd_claim)\n"
            "    return p\n"
        )
        findings = qg._run_r6_redundancy(tmp_path)
        # `_cmd_claim` is whitelisted; `main` is too.  Neither should
        # show up at any severity.
        assert not any("_cmd_claim" in f.message for f in findings)
        assert not any("`main`" in f.message for f in findings)

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
